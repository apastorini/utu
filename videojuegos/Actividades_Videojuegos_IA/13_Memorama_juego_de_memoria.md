# Actividad 13 — Memorama: juego de memoria

**Duración:** 50 min · **Modalidad:** individual · **Entrega:** repo GitHub público

## 1. Objetivos

- Usar **matrices** para guardar las cartas y su estado.
- Implementar la lógica de **voltear dos cartas** y emparejar.
- Barajar con `random.shuffle`.
- Contar movimientos y tiempo para armar un récord.

## 2. Marco teórico

El **memorama** tiene un tablero de cartas boca abajo. En cada turno el jugador voltea dos cartas; si son iguales, quedan descubiertas; si no, se vuelven a tapar. Gana cuando encuentra todos los pares.

Lo representamos con tres matrices del mismo tamaño:

```python
simbolos   # qué hay en cada carta (letras: A B C...)
visible    # True si la carta está descubierta
```

Para armar el mazo: creamos una lista con cada símbolo **dos veces** (para los pares) y la barajamos:

```python
import random
simbolos = list("ABCDEF") * 2      # 12 cartas: 6 pares
random.shuffle(simbolos)
```

Luego la convertimos en matriz 4x3 (o 4x4 con 8 letras). Cada carta se dibuja en una celda; si `visible[fila][col]` es `True`, dibujamos la letra, si no, dibujamos la carta tapada.

La lógica del turno: guardamos la primera carta elegida, esperamos la segunda, comparamos, y si no coinciden las tapamos de nuevo (con un pequeño `pygame.time.wait` para que se vea).

## 3. Paso a paso

```powershell
cd mis-videojuegos
mkdir clase_13_memorama
```

Escribí `clase_13_memorama/memorama.py`:

```python
import random
import sys
import pygame

pygame.init()

ANCHO, ALTO = 800, 600
FILAS, COLS = 3, 4            # 12 cartas, 6 pares
TAM = 140
pantalla = pygame.display.set_mode((ANCHO, ALTO))
reloj = pygame.time.Clock()
fuente = pygame.font.SysFont("arial", 60)

simbolos = list("ABCDEF") * 2
random.shuffle(simbolos)
tablero = [simbolos[i * COLS:(i + 1) * COLS] for i in range(FILAS)]
visible = [[False] * COLS for _ in range(FILAS)]

primera = None       # (fila, col) de la primera carta
segunda = None       # (fila, col) de la segunda carta
pares_encontrados = 0
movimientos = 0
esperando = False    # pausa para mostrar el par antes de taparlo
tiempo_espera = 0

def celda_rect(fila, col):
    ox = (ANCHO - COLS * TAM) // 2
    oy = (ALTO - FILAS * TAM) // 2
    return pygame.Rect(ox + col * TAM, oy + fila * TAM, TAM - 6, TAM - 6)

ejecutando = True
while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        elif evento.type == pygame.MOUSEBUTTONDOWN and not esperando:
            mx, my = pygame.mouse.get_pos()
            for fila in range(FILAS):
                for col in range(COLS):
                    rect = celda_rect(fila, col)
                    if rect.collidepoint(mx, my) and not visible[fila][col]:
                        if primera is None:
                            primera = (fila, col)
                            visible[fila][col] = True
                        elif segunda is None:
                            segunda = (fila, col)
                            visible[fila][col] = True
                            movimientos += 1
                            esperando = True
                            tiempo_espera = pygame.time.get_ticks()
                        break

    # Luego de 700 ms, comparar las dos cartas
    if esperando and pygame.time.get_ticks() - tiempo_espera > 700:
        f1, c1 = primera
        f2, c2 = segunda
        if tablero[f1][c1] == tablero[f2][c2]:
            pares_encontrados += 1
        else:
            visible[f1][c1] = False
            visible[f2][c2] = False
        primera = None
        segunda = None
        esperando = False

    pantalla.fill((25, 25, 45))
    for fila in range(FILAS):
        for col in range(COLS):
            rect = celda_rect(fila, col)
            if visible[fila][col]:
                pygame.draw.rect(pantalla, (60, 150, 90), rect)
                pantalla.blit(fuente.render(tablero[fila][col], True, (255, 255, 255)),
                              (rect.x + 45, rect.y + 25))
            else:
                pygame.draw.rect(pantalla, (70, 70, 130), rect)

    pygame.display.set_caption(f"Memorama - Pares: {pares_encontrados}/6 - Movimientos: {movimientos}")
    pygame.display.flip()
    reloj.tick(30)

    if pares_encontrados == 6:
        print(f"¡Ganaste en {movimientos} movimientos!")
        ejecutando = False

pygame.quit()
sys.exit()
```

## 4. Actividad de cierre (para el commit)

1. **Contador de tiempo:** mostrá los segundos transcurridos (`pygame.time.get_ticks() // 1000`).
2. **Récord:** guardá el mejor resultado (movimientos + tiempo) en un archivo `record.txt`.
3. **Tablero 4x4:** cambiá `FILAS, COLS` a `4, 4` y usá `list("ABCDEFGH") * 2` (8 pares). Ajustá el título.
4. Commit y push:

```powershell
git add .
git commit -m "Clase 13: memorama 4x4 con tiempo y récord"
git push
```

## 5. Usando IA en esta clase (prompts sugeridos)

> **Prompt 1:** "¿Por qué tengo que usar `random.shuffle` sobre una lista con cada símbolo repetido dos veces y no sobre la matriz directamente?"
>
> **Prompt 2:** "Mi memorama permite voltear una tercera carta antes de comparar las dos primeras. ¿Cómo evito eso? Mi código: [pegá el código]."
>
> **Prompt 3:** "Agregá animación de volteo (rotación de la carta) en Pygame."
>
> **Prompt 4:** "¿Cómo hago para que el puntaje penalice los movimientos y el tiempo a la vez?"

## 6. Desafíos para seguir practicando

- Cartas con **imágenes** (`pygame.image.load`) en vez de letras.
- Modo **dificultad**: tablero 6x4 con 12 pares.
- **Multijugador por turnos**: dos jugadores, gana quien encuentra más pares.
- Versión **web** con JavaScript (reutilizá lo de la actividad 7).

## 7. Rúbrica de evaluación

| Criterio | Logrado | En proceso | No logrado |
|---|---|---|---|
| Barajar y matriz | Correcto | Parcial | No |
| Voltear dos cartas | Lógica correcta | Cuenta mal | No |
| Tapar si no coinciden | Funciona | A veces | No |
| Fin del juego y récord | Ambos | Solo fin | Ninguno |
