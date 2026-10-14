# Clases 3 y 4 — Rectángulos, movimiento y colisiones

Objetivo: trabajar con **rectángulos** (`pygame.Rect`), movimiento,
límites de pantalla y **detección de colisiones** básica.

Son cuatro variantes del mismo ejercicio que van sumando: mover, chocar
contra los bordes y detectar solapamientos entre rectángulos.

## Ejercicios de la clase — código completo

**`clases/paso_a_paso/clase_3_4_a.py`**

```python
import pygame


pygame.init()

#Constantes
ANCHO = 800
ALTO = 600
PANTALLA = pygame.display.set_mode((ANCHO, ALTO))
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
AZUL_OSCURO = (30, 30, 40)



pygame.display.set_caption('Clase 3 y 4')



# Variables para la posición y velocidad del jugador
player_x = ANCHO / 2 - 25
player_y = ALTO / 2 - 25
player_velocidad = 5

ejecutando = True
while ejecutando:
    # --- INPUT ---
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

    # Nueva sección: detectar teclas presionadas
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT]:
        player_x -= player_velocidad
    if teclas[pygame.K_RIGHT]:
        player_x += player_velocidad
    if teclas[pygame.K_UP]:
        player_y -= player_velocidad  # Restamos para subir en el eje Y
    if teclas[pygame.K_DOWN]:
        player_y += player_velocidad  # Sumamos para bajar en el eje Y

    # --- UPDATE (la lógica del juego) ---
    # (Por ahora, el movimiento es nuestra única lógica)

    # --- RENDER ---
    PANTALLA.fill(AZUL_OSCURO)

    # Dibujamos el rectángulo usando nuestras nuevas variables
    pygame.draw.rect(PANTALLA, ROJO, (player_x, player_y, 50, 50))

    pygame.display.flip()

pygame.quit()
```

**`clases/paso_a_paso/clase_3_4_b.py`**

```python
# 1. Importar la librería de pygame
import pygame

from core.Player import Player

# 2. Inicializar pygame
pygame.init()

# 3. Definir el tamaño de la ventana
ANCHO = 800
ALTO = 600
ROJO = (255, 0, 0)
AZUL_OSCURO = (30, 30, 40)
PANTALLA = pygame.display.set_mode((ANCHO, ALTO))

# 4. Ponerle un título a la ventana
pygame.display.set_caption('Clase 3 y 4')

# --- CREAMOS EL OBJETO JUGADOR ---
# Usamos el plano (la clase Player) para crear nuestro jugador
jugador = Player(ANCHO / 2 - 25, ALTO / 2 - 25, 50, 50, ROJO)

ejecutando = True
while ejecutando:
    # --- INPUT ---
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

    # Obtenemos las teclas presionadas
    teclas = pygame.key.get_pressed()

    # --- UPDATE ---
    # Llamamos al método mover de NUESTRO objeto jugador
    jugador.mover(teclas)

    # --- RENDER ---
    PANTALLA.fill(AZUL_OSCURO)

    # Llamamos al método dibujar de NUESTRO objeto jugador
    jugador.dibujar(PANTALLA)

    pygame.display.flip()

pygame.quit()
```

**`clases/paso_a_paso/clase_3_4_c.py`**

```python

import pygame

from core.Player import Player

# 2. Inicializar pygame
pygame.init()

# 3. Definir el tamaño de la ventana
ANCHO = 800
ALTO = 600
ROJO = (255, 0, 0)
AZUL_OSCURO = (30, 30, 40)
PANTALLA = pygame.display.set_mode((ANCHO, ALTO))

# 4. Ponerle un título a la ventana
pygame.display.set_caption('Clase 3 y 4')


# --- ANTES DEL BUCLE PRINCIPAL ---
jugador = Player(ANCHO / 2 - 25, ALTO / 2 - 25, 50, 50, ROJO)
reloj = pygame.time.Clock() # Creamos un objeto Clock

# --- BUCLE PRINCIPAL ---
ejecutando = True
while ejecutando:
    # --- INPUT ---
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

    # Obtenemos las teclas presionadas
    teclas = pygame.key.get_pressed()

    # --- UPDATE ---
    # Llamamos al método mover de NUESTRO objeto jugador
    jugador.mover(teclas)


    # --- RENDER ---
    PANTALLA.fill(AZUL_OSCURO)
    jugador.dibujar(PANTALLA)
    pygame.display.flip()

    # --- CONTROL DE TIEMPO ---
    # Le decimos al reloj que espere lo necesario para que el bucle
    # no se ejecute más de 60 veces por segundo.
    reloj.tick(60)
pygame.quit()
```

**`clases/paso_a_paso/clase_3_4_d.py`**

```python
import random
import pygame

from core.Collectible import Collectible
from core.Player import Player


from utils.Colors import ROJO, AZUL_OSCURO, BLANCO
import random

pygame.init()

# 3. Definir el tamaño de la ventana
ANCHO = 800
ALTO = 600
PANTALLA = pygame.display.set_mode((ANCHO, ALTO))



# 4. Ponerle un título a la ventana
pygame.display.set_caption('Clase 3 y 4')


# --- ANTES DEL BUCLE PRINCIPAL ---
jugador = Player(ANCHO / 2 - 25, ALTO / 2 - 25, 50, 50, ROJO)
reloj = pygame.time.Clock() # Creamos un objeto Clock
fuente = pygame.font.Font(None, 36)

# --- CREAMOS VARIABLES Y OBJETOS ---
jugador = Player(50, 50, 40, 40, ROJO)
moneda = Collectible(300, 300, 30, 30, (255, 223, 0))
reloj = pygame.time.Clock()

puntuacion = 0 # Nuestra variable para la puntuación

# --- BUCLE PRINCIPAL ---
ejecutando = True
while ejecutando:
# --- INPUT ---
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
    # Obtenemos las teclas presionadas
    teclas = pygame.key.get_pressed()
# --- UPDATE ---
    jugador.mover(teclas)
    if jugador.rect.colliderect(moneda.rect):
        puntuacion += 1 # Aumentamos la puntuación en 1
        # Movemos la moneda a una nueva posición aleatoria
        moneda.rect.x = random.randint(0, ANCHO - moneda.rect.width)
        moneda.rect.y = random.randint(0, ALTO - moneda.rect.height)
# --- RENDER --- # 2. RENDERIZAR EL TEXTO
    texto_puntuacion = fuente.render(f"Puntuación: {puntuacion}", True, BLANCO)
    PANTALLA.fill(AZUL_OSCURO)
    jugador.dibujar(PANTALLA)
    moneda.dibujar(PANTALLA)

    # 3. DIBUJAR EL TEXTO EN LA PANTALLA
    PANTALLA.blit(texto_puntuacion, (10, 10))
    # Lo ponemos en la esquina sup. izq.
    pygame.display.flip()
    # --- CONTROL DE TIEMPO ---
    # Le decimos al reloj que espere lo necesario para que el bucle
    # no se ejecute más de 60 veces por segundo.
    reloj.tick(60)

pygame.quit()
```

## Controles

flechas para mover; cada variante añade una idea nueva.

## Cómo ejecutar

Desde la carpeta `2027/`:

```bash
python clases/paso_a_paso/clase_3_4_a.py   # y b, c, d
```
