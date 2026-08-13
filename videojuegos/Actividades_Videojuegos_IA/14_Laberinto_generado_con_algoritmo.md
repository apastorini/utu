# Actividad 14 — Laberinto generado con algoritmo

**Duración:** 50 min · **Modalidad:** individual · **Entrega:** repo GitHub público

## 1. Objetivos

- Representar un laberinto como una **matriz de celdas**.
- Generar laberintos aleatorios con un **algoritmo** (recorrido en profundidad).
- Mover un jugador por el laberinto respetando paredes.
- Agregar cronómetro, meta y récord.

## 2. Marco teórico

Un laberinto puede pensarse como una cuadrícula de celdas donde cada celda tiene cuatro paredes posibles: arriba, abajo, izquierda, derecha. Para generarlo usamos un **algoritmo de recorrido en profundidad (DFS)** con una pila:

1. Empezar en una celda, marcarla como visitada.
2. Mientras haya celdas sin visitar: elegir un vecino al azar, **romper la pared** entre ambas, avanzar, y "recordar" el camino en una pila.
3. Si no hay vecino sin visitar, retroceder (desapilar) hasta encontrar uno.

Ese algoritmo produce un laberinto "perfecto": sin ciclos y con exactamente un camino entre cualquier par de celdas.

En Python la pila es una lista con `.append()` y `.pop()` (LIFO: último en entrar, primero en salir).

Para que el jugador se mueva respetando las paredes, guardamos las paredes como un **conjunto de pares**:

```python
paredes = set()   # cada elemento: ((fila, col), direccion)
# direccion en {"N", "S", "E", "O"}
```

Y para moverse preguntamos: `if ("N" no está en paredes de la celda actual)` puedo ir arriba.

## 3. Paso a paso

```powershell
cd mis-videojuegos
mkdir clase_14_laberinto
```

Escribí `clase_14_laberinto/laberinto.py`:

```python
import random
import sys
import pygame

pygame.init()

FILAS, COLS = 15, 21
TAM = 30
ANCHO = COLS * TAM
ALTO = FILAS * TAM
pantalla = pygame.display.set_mode((ANCHO, ALTO))
reloj = pygame.time.Clock()

# ---------- Generación del laberinto (DFS) ----------
# paredes[fila][col] = conjunto con las direcciones bloqueadas
paredes = [[{"N", "S", "E", "O"} for _ in range(COLS)] for _ in range(FILAS)]
visitadas = [[False] * COLS for _ in range(FILAS)]

def en_rango(fila, col):
    return 0 <= fila < FILAS and 0 <= col < COLS

def generar(fila, col):
    visitadas[fila][col] = True
    pila = [(fila, col)]
    opuestos = {"N": "S", "S": "N", "E": "O", "O": "E"}
    vecinos = {"N": (-1, 0), "S": (1, 0), "E": (0, 1), "O": (0, -1)}

    while pila:
        f, c = pila[-1]
        opciones = []
        for dir, (df, dc) in vecinos.items():
            nf, nc = f + df, c + dc
            if en_rango(nf, nc) and not visitadas[nf][nc]:
                opciones.append((dir, nf, nc))
        if not opciones:
            pila.pop()              # retroceder
            continue
        dir, nf, nc = random.choice(opciones)
        paredes[f][c].discard(dir)              # romper pared
        paredes[nf][nc].discard(opuestos[dir])
        visitadas[nf][nc] = True
        pila.append((nf, nc))

generar(0, 0)

jugador = (0, 0)
inicio = (0, 0)
meta = (FILAS - 1, COLS - 1)
inicio_ticks = pygame.time.get_ticks()

def dibujar_laberinto():
    pantalla.fill((20, 20, 30))
    for fila in range(FILAS):
        for col in range(COLS):
            x, y = col * TAM, fila * TAM
            if "N" in paredes[fila][col]:
                pygame.draw.line(pantalla, (220, 220, 220), (x, y), (x + TAM, y), 2)
            if "S" in paredes[fila][col]:
                pygame.draw.line(pantalla, (220, 220, 220), (x, y + TAM), (x + TAM, y + TAM), 2)
            if "O" in paredes[fila][col]:
                pygame.draw.line(pantalla, (220, 220, 220), (x, y), (x, y + TAM), 2)
            if "E" in paredes[fila][col]:
                pygame.draw.line(pantalla, (220, 220, 220), (x + TAM, y), (x + TAM, y + TAM), 2)

ejecutando = True
while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        elif evento.type == pygame.KEYDOWN:
            f, c = jugador
            if evento.key == pygame.K_UP and "N" not in paredes[f][c]:
                jugador = (f - 1, c)
            elif evento.key == pygame.K_DOWN and "S" not in paredes[f][c]:
                jugador = (f + 1, c)
            elif evento.key == pygame.K_LEFT and "O" not in paredes[f][c]:
                jugador = (f, c - 1)
            elif evento.key == pygame.K_RIGHT and "E" not in paredes[f][c]:
                jugador = (f, c + 1)

    dibujar_laberinto()

    # Jugador (verde)
    x, y = jugador[1] * TAM + 5, jugador[0] * TAM + 5
    pygame.draw.rect(pantalla, (80, 220, 80), (x, y, TAM - 10, TAM - 10))

    # Meta (roja)
    mx, my = meta[1] * TAM + 5, meta[0] * TAM + 5
    pygame.draw.rect(pantalla, (230, 80, 80), (mx, my, TAM - 10, TAM - 10))

    segundos = (pygame.time.get_ticks() - inicio_ticks) // 1000
    pygame.display.set_caption(f"Laberinto - Tiempo: {segundos} s")

    pygame.display.flip()
    reloj.tick(30)

    if jugador == meta:
        print(f"¡Llegaste a la meta en {segundos} segundos!")
        ejecutando = False

pygame.quit()
sys.exit()
```

## 4. Actividad de cierre (para el commit)

1. **Récord:** guardá el mejor tiempo en `record.txt` y mostralo en el título.
2. **Contador de pasos:** mostrá cuántos pasos diste.
3. **Ayuda visual:** pintá de celeste la celda actual y de amarillo la salida con un borde distinto.
4. Commit y push:

```powershell
git add .
git commit -m "Clase 14: laberinto generado con DFS, cronómetro y récord"
git push
```

## 5. Usando IA en esta clase (prompts sugeridos)

> **Prompt 1:** "Explicame con un ejemplo pequeño (3x3) cómo funciona la pila en el algoritmo DFS para generar un laberinto."
>
> **Prompt 2:** "¿Por qué uso un conjunto (`set`) para las paredes y no una lista? ¿Qué gano?"
>
> **Prompt 3:** "Agregá un solucionador automático: que la IA encuentre el camino más corto con BFS y lo dibuje."
>
> **Prompt 4:** "Hacé que el laberinto tenga dos niveles: al llegar a la meta se genera uno más grande y más difícil."

## 6. Desafíos para seguir practicando

- Cambiar de algoritmo de generación (**Prim** o **recursive division**) y comparar resultados.
- Agregar un **solucionador BFS** que trace el camino más corto.
- Monedas escondidas dentro del laberinto que suman tiempo.
- **Modo multijugador en red**: dos jugadores en el mismo laberinto (reutilizá lo de la actividad 10).

## 7. Rúbrica de evaluación

| Criterio | Logrado | En proceso | No logrado |
|---|---|---|---|
| Genera laberinto aleatorio | Correcto | Se traba | No |
| Movimiento sin atravesar paredes | Correcto | Atraviesa | No |
| Meta y cronómetro | Ambos | Solo meta | Falta |
| Récord guardado | Funciona | Parcial | No |
