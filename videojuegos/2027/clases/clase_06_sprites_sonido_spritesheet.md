# Clase 6 — Sprites, sonido y animación con spritesheet

Objetivo: usar **sprites**, reproducir **sonido** y **animar** con una
**spritesheet** (recortando fotogramas de una sola imagen).

Aparece el primer `core/` con clases propias (`Player`, `Enemy`,
`Collectible`...) que es el antecedente directo de `engine/game_object.py`
y del concepto de animación del motor.

## Ejercicio y su 'core' — código completo

**`clases/paso_a_paso/clase_6_a.py`**

```python
import pygame

from core.Collectible import Collectible
from core.Enemy import Enemy
from core.Player import Player


from utils.Colors import ROJO, AZUL_OSCURO, BLANCO
import random

pygame.init()
pygame.mixer.init()

# 3. Definir el tamaño de la ventana
ANCHO = 800
ALTO = 600
PANTALLA = pygame.display.set_mode((ANCHO, ALTO))



# 4. Ponerle un título a la ventana
pygame.display.set_caption('Clase 3 y 4')


# --- ANTES DEL BUCLE PRINCIPAL ---
moneda =  Collectible(300, 300, 30, 30, (255, 223, 0))
fuente = pygame.font.Font(None, 36)
reloj = pygame.time.Clock()

# --- CARGAMOS SONIDOS ---
sonido_moneda = pygame.mixer.Sound('assets/sonidos/coin-drop-1.wav')
sonido_golpe = pygame.mixer.Sound('assets/sonidos/hit.mp3')

# --- CARGAMOS Y REPRODUCIMOS MÚSICA ---
pygame.mixer.music.load('assets/musica/music_1.wav')
pygame.mixer.music.play(-1)  # El -1 significa que se repetirá en bucle infinito

# --- CREAMOS VARIABLES Y OBJETOS ---
jugador = Player(50, 50)  # Ya no necesita ancho y alto
#enemigo = Enemy(150, 150)



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
        sonido_moneda.play()  # ¡Reproducimos el sonido!
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

**`clases/paso_a_paso/core/__init__.py`**

```python

```

**`clases/paso_a_paso/core/Player.py`**

```python
import pygame

class Player:
    def __init__(self, x, y):
        # Cargamos la imagen y obtenemos su rectángulo
        self.image = pygame.image.load('assets/mario.jpg').convert_alpha()
        self.rect = self.image.get_rect()
        # Posicionamos el rectángulo donde nos digan
        self.rect.topleft = (x, y)
        self.velocidad = 5

    # Un "método": una función que pertenece a la clase
    def mover(self, teclas):
        if teclas[pygame.K_LEFT]:
            self.rect.x -= self.velocidad
        if teclas[pygame.K_RIGHT]:
            self.rect.x += self.velocidad
        if teclas[pygame.K_UP]:
            self.rect.y -= self.velocidad
        if teclas[pygame.K_DOWN]:
            self.rect.y += self.velocidad

    def dibujar(self, superficie):
        # En lugar de dibujar un rect, dibujamos la imagen en la posición del rect
        superficie.blit(self.image, self.rect)
```

**`clases/paso_a_paso/core/PlayerRect.py`**

```python
import pygame


class PlayerRect:
    # El "constructor": se ejecuta UNA VEZ al crear el objeto
    def __init__(self, x, y, ancho, alto, color):
        # self se refiere al objeto específico que se está creando
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.color = color
        self.velocidad = 5

    # Un "método": una función que pertenece a la clase
    def mover(self, teclas):
        if teclas[pygame.K_LEFT]:
            self.rect.x -= self.velocidad
        if teclas[pygame.K_RIGHT]:
            self.rect.x += self.velocidad
        if teclas[pygame.K_UP]:
            self.rect.y -= self.velocidad
        if teclas[pygame.K_DOWN]:
            self.rect.y += self.velocidad

    def dibujar(self, superficie):
        pygame.draw.rect(superficie, self.color, self.rect)
```

**`clases/paso_a_paso/core/Enemy.py`**

```python
import pygame


class Enemy:
    def __init__(self, x, y, ancho, alto, color):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.color = color
        # Damos al enemigo una velocidad en ambos ejes
        self.velocidad_x = 3
        self.velocidad_y = 3

    def update(self, ancho_pantalla, alto_pantalla):
        # Mover el enemigo
        self.rect.x += self.velocidad_x
        self.rect.y += self.velocidad_y

        # Lógica de rebote (IA Simple)
        if self.rect.left <= 0 or self.rect.right >= ancho_pantalla:
            self.velocidad_x *= -1  # Invertir la dirección horizontal
        if self.rect.top <= 0 or self.rect.bottom >= alto_pantalla:
            self.velocidad_y *= -1  # Invertir la dirección vertical

    def dibujar(self, superficie):
        pygame.draw.rect(superficie, self.color, self.rect)
```

**`clases/paso_a_paso/core/Collectible.py`**

```python
import pygame

class Collectible:
    # El constructor. Similar al del jugador, pero sin velocidad.
    def __init__(self, x, y, ancho, alto, color):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.color = color

    # El método para dibujarlo en pantalla
    def dibujar(self, superficie):
        pygame.draw.rect(superficie, self.color, self.rect)
```

**`clases/paso_a_paso/core/Colors.py`**

```python
ROJO = (255, 0, 0)
AZUL_OSCURO = (30, 30, 40)
BLANCO = (255, 255, 255)
NEGRO = (0,0,0)
```

**`clases/paso_a_paso/core/utils/__init__.py`**

```python

```

**`clases/paso_a_paso/core/utils/utils.py`**

```python
ANCHO = 800
ALTO = 600
```

## Controles

flechas para mover; el personaje se anima y recoge objetos.

## Cómo ejecutar

Desde la carpeta `2027/`:

```bash
python clases/paso_a_paso/clase_6_a.py
```
