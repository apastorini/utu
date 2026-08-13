# Actividad 8 — Batalla naval (jugador vs IA)

**Duración:** 50 min · **Modalidad:** individual · **Entrega:** repo GitHub público

## 1. Objetivos

- Modelar tableros como **matrices bidimensionales** (listas de listas).
- Colocar barcos **aleatoriamente** respetando el espacio.
- Implementar el juego por **turnos** contra una IA simple.
- Manejar estados: agua, tocado, hundido.

## 2. Marco teórico

**Batalla naval** se juega sobre dos tableros de 10x10. Cada jugador tiene barcos que ocupan varias celdas consecutivas (vertical u horizontal). El objetivo es adivinar dónde están los barcos del rival disparando por coordenadas.

En programación, un tablero es una **matriz**: una lista de filas, donde cada fila es una lista de celdas.

```python
tablero = [["·"] * 10 for _ in range(10)]
# tablero[fila][col] puede ser:
#   "·" agua (no disparado)
#   "B" barco
#   "X" agua disparado (agua)
#   "T" barco tocado
```

Accedemos a una celda con `tablero[fila][col]` (fila = índice del 0 al 9, col = índice del 0 al 9). Los barcos se colocan con `random.randint` hasta que entre en celdas libres.

## 3. Paso a paso

```powershell
cd mis-videojuegos
mkdir clase_08_batalla_naval
```

Escribí `clase_08_batalla_naval/batalla_naval.py`:

```python
import random
import sys
import pygame

pygame.init()

TAM = 36
ANCHO, ALTO = 760, 420
pantalla = pygame.display.set_mode((ANCHO, ALTO))
reloj = pygame.time.Clock()
fuente = pygame.font.SysFont("arial", 16)

def crear_tablero():
    return [["·"] * 10 for _ in range(10)]

def colocar_barcos(tablero, tamaños=(5, 4, 3, 3, 2)):
    for tam in tamaños:
        colocado = False
        while not colocado:
            horizontal = random.choice([True, False])
            if horizontal:
                x = random.randint(0, 9 - tam)
                y = random.randint(0, 9)
                celdas = [(x + i, y) for i in range(tam)]
            else:
                x = random.randint(0, 9)
                y = random.randint(0, 9 - tam)
                celdas = [(x, y + i) for i in range(tam)]
            if all(tablero[cx][cy] == "·" for cx, cy in celdas):
                for cx, cy in celdas:
                    tablero[cx][cy] = "B"
                colocado = True

jugador = crear_tablero()
enemigo = crear_tablero()
colocar_barcos(jugador)
colocar_barcos(enemigo)

# Las "X" y "T" que vamos marcando al disparar
disparos_jugador = crear_tablero()
disparos_enemigo = crear_tablero()
turno_jugador = True
hundidos = 0

def dibujar_tablero(tablero_disparos, ox, oy, ver_barcos=False):
    for fila in range(10):
        for col in range(10):
            celda = tablero_disparos[fila][col]
            color = (30, 60, 120)
            if celda == "X":
                color = (60, 60, 60)
            elif celda == "T":
                color = (220, 60, 60)
            pygame.draw.rect(pantalla, color,
                             (ox + col * TAM, oy + fila * TAM, TAM - 2, TAM - 2))

ejecutando = True
while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        elif evento.type == pygame.MOUSEBUTTONDOWN and turno_jugador:
            mx, my = pygame.mouse.get_pos()
            col = (mx - 10) // TAM
            fila = (my - 10) // TAM
            if 0 <= fila < 10 and 0 <= col < 10 and disparos_enemigo[fila][col] == "·":
                if enemigo[fila][col] == "B":
                    disparos_enemigo[fila][col] = "T"
                    enemigo[fila][col] = "X"
                    print("¡Tocado!")
                else:
                    disparos_enemigo[fila][col] = "X"
                    print("Agua. Turno de la IA...")
                    turno_jugador = False

    # Turno de la IA: dispara a una celda aleatoria
    if not turno_jugador:
        while True:
            fila = random.randint(0, 9)
            col = random.randint(0, 9)
            if disparos_jugador[fila][col] == "·":
                if jugador[fila][col] == "B":
                    disparos_jugador[fila][col] = "T"
                    jugador[fila][col] = "X"
                    print("La IA te tocó un barco.")
                else:
                    disparos_jugador[fila][col] = "X"
                    print("La IA falló. ¡Tu turno!")
                    turno_jugador = True
                break

    pantalla.fill((15, 15, 25))
    pantalla.blit(fuente.render("Tu tablero", True, (255, 255, 255)), (10, 400))
    pantalla.blit(fuente.render("Tablero del enemigo", True, (255, 255, 255)), (400, 400))
    dibujar_tablero(disparos_jugador, 10, 10, ver_barcos=True)
    dibujar_tablero(disparos_enemigo, 400, 10)
    pygame.display.flip()
    reloj.tick(30)

pygame.quit()
sys.exit()
```

## 4. Actividad de cierre (para el commit)

1. **Victoria:** contá cuántos barcos del enemigo quedan en pie y mostrá `"¡Ganaste!"` cuando no quede ninguno. Contá los `"B"` en `enemigo`.
2. **Derrota:** hacé lo mismo con tu propio tablero.
3. **Contador de disparos:** mostrá cuántos disparos necesitaste para ganar (entre menos, mejor).
4. Commit y push:

```powershell
git add .
git commit -m "Clase 08: batalla naval contra la IA con turnos"
git push
```

## 5. Usando IA en esta clase (prompts sugeridos)

> **Prompt 1:** "Explicame qué significa `[["·"] * 10 for _ in range(10)]` y por qué no puedo escribir simplemente `["·"] * 10` copiado 10 veces."
>
> **Prompt 2:** "Mi IA dispara a la misma celda repetidas veces. ¿Cómo hago para que solo dispare a celdas sin disparar?"
>
> **Prompt 3:** "Agregá una IA que después de tocar un barco siga disparando alrededor hasta hundirlo."
>
> **Prompt 4:** "¿Cómo verifico que un barco está hundido (todas sus celdas tocadas) si no guardo la lista de barcos?"

## 6. Desafíos para seguir practicando

- Modo **dos jugadores** en la misma máquina (turnos ocultos).
- Mostrar el tablero del enemigo con las letras A-J y números 1-10.
- Barcos que se **rotan** con la tecla R antes de colocarlos (modo manual).
- La misma batalla pero **en red** (es la actividad 10).

## 7. Rúbrica de evaluación

| Criterio | Logrado | En proceso | No logrado |
|---|---|---|---|
| Tableros en matrices | Correctos | Parciales | No |
| Barcos aleatorios | Sin superponerse | Se superponen | Fijos |
| Turnos | Alternan bien | Se traban | No |
| Victoria/derrota | Detecta ambas | Solo una | No |
