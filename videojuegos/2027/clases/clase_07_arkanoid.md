# Clase 7 — Arkanoid (de un archivo a módulos)

Objetivo: programar el primer **Arkanoid** completo. Se empieza con todo
en un archivo y luego se **separa en módulos** dentro de
`core_arkanoid/` (`Player`, `Ball`, `Brick`, `SpriteSheet`), con una
segunda versión que ya carga sprites con un spritesheet.

Este es el **antecedente directo** de la reestructuración del motor de la
clase 8 (`engine/` + `arkanoid/` con escenas).

## Juego de ejemplo — código completo

**`clases/paso_a_paso/arkanoid/core_arkanoid/__init__.py`**

```python

```

**`clases/paso_a_paso/arkanoid/core_arkanoid/clase_7_arkanoid.py`**

```python
# game.py
import random

import pygame

from arkanoid.core_arkanoid.Ball import Ball
from arkanoid.core_arkanoid.Brick import Brick
from arkanoid.core_arkanoid.Player import Player
from core.Colors import AZUL_OSCURO, NEGRO, ROJO, BLANCO
from core.utils.utils import ANCHO, ALTO

pygame.init()
pygame.mixer.init() # Inicializamos el mezclador de sonido

# --- CARGAMOS SONIDOS ---
sonido_golpe = pygame.mixer.Sound('../assets/sounds/hit.mp3')

# --- CARGAMOS Y REPRODUCIMOS MÚSICA ---
pygame.mixer.music.load('../assets/music/song18.mp3')
pygame.mixer.music.play(-1)  # El -1 significa que se repetirá en bucle infinito

class Game:

    PANTALLA = pygame.display.set_mode((ANCHO, ALTO))

    # 4. Ponerle un título a la ventana
    pygame.display.set_caption('Arkanoid')


    # Fuente
    fuente = pygame.font.Font(None, 36)
    fuente_grande = pygame.font.Font(None, 72)

    # Creamos una instancia de nuestra nueva clase
    reloj = pygame.time.Clock()  # Creamos un objeto Clock
    puntuacion = 0  # Nuestra variable para la puntuación
    estado_juego = 'jugando'


    NUM_LADRILLOS_FILA = 10



    def __init__(self):


        # Reiniciar todas las variables del juego
        # 5. --- CREAMOS VARIABLES---
        self.jugador = Player(50, 450)
        self.pelota = Ball(50, 350)
        self.puntuacion = 0
        self.NUM_LADRILLOS_FILA = 10
        self.ANCHO_LADRILLO = ANCHO // self.NUM_LADRILLOS_FILA
        self.ladrillos = []
        self.jugador.rect.topleft = (50, 450)  # Posición inicial
        self.estado_juego = 'jugando'  # ¡Volvemos a jugar!
        pygame.mixer.music.play(-1)  # Volvemos a poner la música
        ##


        #Crear ladrillos
        for fila in range(5):  # 5 filas de ladrillos
            for col in range(self.NUM_LADRILLOS_FILA):  # 10 ladrillos por fila
                ladrillo = Brick(col * self.ANCHO_LADRILLO, fila * 40 + 50, self.ANCHO_LADRILLO, 30)
                self.ladrillos.append(ladrillo)

    def game_loop(self):
        # --- BUCLE PRINCIPAL ---
        ejecutando = True
        while ejecutando:
            # --- INPUT PRINCIPAL ---
            # Unificar la captura de eventos en un solo bloque por fotograma
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    ejecutando = False

                # Detectar la tecla espacio solo si estamos en la pantalla de game_over
                if self.estado_juego == 'game_over':
                    if evento.type == pygame.KEYDOWN:
                        if evento.key == pygame.K_SPACE:
                            self.__init__() # Reiniciar juego

            # --- LÓGICA SEGÚN ESTADO ---
            if self.estado_juego == 'jugando':
                teclas = pygame.key.get_pressed()

                # --- UPDATE ---
                self.jugador.mover(teclas)
                self.pelota.update()

                # Colisión pelota con pala
                if self.pelota.rect.colliderect(self.jugador.rect):
                    self.pelota.velocidad_y *= -1
                    self.pelota.rect.bottom = self.jugador.rect.top

                for ladrillo in self.ladrillos[:]:
                    if self.pelota.rect.colliderect(ladrillo.rect):
                        self.ladrillos.remove(ladrillo)
                        self.pelota.velocidad_y *= -1

                if self.pelota.rect.top > ALTO:
                    self.estado_juego = 'game_over'

                # --- RENDER JUGANDO ---
                self.PANTALLA.fill(AZUL_OSCURO)
                self.jugador.dibujar(self.PANTALLA)
                self.pelota.dibujar(self.PANTALLA)
                texto_puntuacion = self.fuente.render(f"Puntuación: {self.puntuacion}", True, BLANCO)
                for ladrillo in self.ladrillos:
                    ladrillo.dibujar(self.PANTALLA)
                self.PANTALLA.blit(texto_puntuacion, (10, 10))

            elif self.estado_juego == 'game_over':
                # --- RENDER GAME OVER ---
                self.PANTALLA.fill(NEGRO)
                texto_game_over = self.fuente_grande.render("GAME OVER", True, ROJO)
                texto_instruccion = self.fuente.render("Presiona ESPACIO para reiniciar", True, BLANCO)

                pos_game_over = texto_game_over.get_rect(center=(ANCHO / 2, ALTO / 2 - 50))
                pos_instruccion = texto_instruccion.get_rect(center=(ANCHO / 2, ALTO / 2 + 50))

                self.PANTALLA.blit(texto_game_over, pos_game_over)
                self.PANTALLA.blit(texto_instruccion, pos_instruccion)

            pygame.display.flip()
            self.reloj.tick(60)

        pygame.quit()

# --- PUNTO DE ENTRADA DEL PROGRAMA ---
# Este bloque debe ir pegado al margen izquierdo, fuera de la clase Game.
if __name__ == "__main__":
    juego = Game()
    juego.game_loop()
```

**`clases/paso_a_paso/arkanoid/core_arkanoid/Player.py`**

```python
import pygame


class Player:
    def __init__(self, x, y):
        # Cargamos la imagen y obtenemos su rectángulo
        self.image = pygame.image.load('../assets/sprites/paleta.png').convert_alpha()
        self.rect = self.image.get_rect()
        # Posicionamos el rectángulo donde nos digan
        self.rect.topleft = (x, y)
        self.velocidad = 5

    def mover(self, teclas):
        if teclas[pygame.K_LEFT]:
            self.rect.x -= self.velocidad
        if teclas[pygame.K_RIGHT]:
            self.rect.x += self.velocidad




    def dibujar(self, superficie):
        # En lugar de dibujar un rect, dibujamos la imagen en la posición del rect
        superficie.blit(self.image, self.rect)
```

**`clases/paso_a_paso/arkanoid/core_arkanoid/Ball.py`**

```python
import pygame
from core.utils.utils import ANCHO


class Ball:
    def __init__(self, x, y):
        # 1. Cargar la imagen en una variable temporal
        imagen_original = pygame.image.load('../assets/sprites/ball.png').convert_alpha()

        # 2. Escalar la imagen a un tamaño razonable para una pelota (20x20 píxeles)
        self.image = pygame.transform.scale(imagen_original, (20, 20))

        self.rect = self.image.get_rect(center=(x, y))
        self.velocidad_x = 4
        self.velocidad_y = -4

    def update(self):
        self.rect.x += self.velocidad_x
        self.rect.y += self.velocidad_y

        if self.rect.left <= 0 or self.rect.right >= ANCHO:
            self.velocidad_x *= -1
        if self.rect.top <= 0:
            self.velocidad_y *= -1

    def dibujar(self, superficie):
        superficie.blit(self.image, self.rect)
```

**`clases/paso_a_paso/arkanoid/core_arkanoid/Brick.py`**

```python
import pygame


class Brick:
    # Ahora recibe el ancho y alto deseado como parámetros
    def __init__(self, x, y, ancho, alto):
        imagen_original = pygame.image.load('../assets/sprites/brick.png').convert_alpha()

        # Usamos las variables en lugar de un número fijo
        self.image = pygame.transform.scale(imagen_original, (ancho, alto))
        self.rect = self.image.get_rect(topleft=(x, y))

    def dibujar(self, superficie):
        superficie.blit(self.image, self.rect)
```

**`clases/paso_a_paso/arkanoid/core_arkanoid/SpriteSheet.py`**

```python
import pygame


class SpriteSheet:
    def __init__(self, ruta_archivo):
        self.hoja = pygame.image.load(ruta_archivo).convert_alpha()

    def obtener_imagen(self, x, y, ancho, alto, escala_ancho=None, escala_alto=None, quitar_fondo=False):
        # Creamos la superficie para el recorte
        imagen = pygame.Surface((ancho, alto), pygame.SRCALPHA)
        imagen.blit(self.hoja, (0, 0), (x, y, ancho, alto))

        # --- NUEVA MAGIA PARA BORRAR EL FONDO VIOLETA ---
        if quitar_fondo:
            # Capturamos el color exacto del píxel de la esquina superior izquierda (0,0)
            color_a_borrar = imagen.get_at((0, 0))
            # Le decimos a Pygame que haga transparente todo lo que tenga ese color
            imagen.set_colorkey(color_a_borrar)

        # Escalamos al tamaño final que tendrá en el juego
        if escala_ancho and escala_alto:
            imagen = pygame.transform.scale(imagen, (escala_ancho, escala_alto))

        return imagen
```

**`clases/paso_a_paso/arkanoid/core_arkanoid/sprite_sheet/__init__.py`**

```python

```

**`clases/paso_a_paso/arkanoid/core_arkanoid/sprite_sheet/Game.py`**

```python
import random
import traceback
import pygame


from arkanoid.core_arkanoid.SpriteSheet import SpriteSheet
from arkanoid.core_arkanoid.sprite_sheet.Ball import Ball
from arkanoid.core_arkanoid.sprite_sheet.Brick import Brick
from arkanoid.core_arkanoid.sprite_sheet.Player import Player
from core.Colors import AZUL_OSCURO, NEGRO, ROJO, BLANCO

from core.utils.utils import ANCHO, ALTO

# Importamos la herramienta para extraer sprites


pygame.init()
pygame.mixer.init()

# --- CARGAMOS SONIDOS ---
try:
    sonido_golpe = pygame.mixer.Sound('../assets/sounds/hit.mp3')
    pygame.mixer.music.load('../assets/music/song18.mp3')
    pygame.mixer.music.play(-1)
except FileNotFoundError:
    print("Advertencia: No se encontraron los archivos de audio en la ruta especificada.")


class Game:
    PANTALLA = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption('Arkanoid')

    fuente = pygame.font.Font(None, 36)
    fuente_grande = pygame.font.Font(None, 72)

    reloj = pygame.time.Clock()

    def __init__(self):
        # 1. Cargamos el spritesheet
        hoja_sprites = SpriteSheet('../../assets/sprites/image_0918c1.png')

        self.NUM_LADRILLOS_FILA = 10
        self.ANCHO_LADRILLO = ANCHO // self.NUM_LADRILLOS_FILA

        # 2. Extraemos las imágenes usando tus coordenadas exactas y quitando el fondo fucsia

        # La pala. Usé valores genéricos, pero si usas el visor puedes poner los exactos:
        imagen_pala = hoja_sprites.obtener_imagen(384, 32, 64, 32, 100, 20, quitar_fondo=True)

        # Ladrillo (Tus medidas: X: 193, Y: 47, Ancho: 30, Alto: 15)
        imagen_ladrillo = hoja_sprites.obtener_imagen(193, 47, 30, 15, self.ANCHO_LADRILLO, 30, quitar_fondo=True)

        # Pelota (Tus medidas: X: 102, Y: 194, Ancho: 21, Alto: 27)
        imagen_pelota = hoja_sprites.obtener_imagen(102, 194, 21, 27, 20, 20, quitar_fondo=True)

        # 3. Inicializamos las variables pasando las imágenes recortadas
        self.jugador = Player(ANCHO // 2 - 50, 450, imagen_pala)
        self.pelota = Ball(50, 350, imagen_pelota)

        self.puntuacion = 0
        self.ladrillos = []
        self.estado_juego = 'jugando'

        if not pygame.mixer.music.get_busy():
            try:
                pygame.mixer.music.play(-1)
            except:
                pass

        # 4. Crear los ladrillos
        for fila in range(5):
            for col in range(self.NUM_LADRILLOS_FILA):
                ladrillo = Brick(col * self.ANCHO_LADRILLO, fila * 40 + 50, imagen_ladrillo)
                self.ladrillos.append(ladrillo)

    def game_loop(self):
        ejecutando = True
        while ejecutando:
            # --- INPUT PRINCIPAL ---
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    ejecutando = False

                if self.estado_juego == 'game_over':
                    if evento.type == pygame.KEYDOWN:
                        if evento.key == pygame.K_SPACE:
                            self.__init__()

            # --- LÓGICA SEGÚN ESTADO ---
            if self.estado_juego == 'jugando':
                teclas = pygame.key.get_pressed()

                # --- UPDATE ---
                self.jugador.mover(teclas)
                self.pelota.update()

                # Colisión pelota con pala
                if self.pelota.rect.colliderect(self.jugador.rect):
                    self.pelota.velocidad_y *= -1
                    self.pelota.rect.bottom = self.jugador.rect.top

                # Colisión pelota con ladrillos
                for ladrillo in self.ladrillos[:]:
                    if self.pelota.rect.colliderect(ladrillo.rect):
                        self.ladrillos.remove(ladrillo)
                        self.pelota.velocidad_y *= -1
                        self.puntuacion += 10

                        try:
                            # Descomenta esto cuando el audio funcione
                            # sonido_golpe.play()
                            pass
                        except:
                            pass

                # Si la pelota cae por debajo del borde inferior
                if self.pelota.rect.top > ALTO:
                    self.estado_juego = 'game_over'

                # --- RENDER JUGANDO ---
                self.PANTALLA.fill(AZUL_OSCURO)

                # Dibujamos en orden: primero ladrillos, luego jugador, luego pelota encima
                for ladrillo in self.ladrillos:
                    ladrillo.dibujar(self.PANTALLA)
                self.jugador.dibujar(self.PANTALLA)
                self.pelota.dibujar(self.PANTALLA)

                # Interfaz
                texto_puntuacion = self.fuente.render(f"Puntuación: {self.puntuacion}", True, BLANCO)
                self.PANTALLA.blit(texto_puntuacion, (10, 10))

            elif self.estado_juego == 'game_over':
                # --- RENDER GAME OVER ---
                self.PANTALLA.fill(NEGRO)
                texto_game_over = self.fuente_grande.render("GAME OVER", True, ROJO)
                texto_instruccion = self.fuente.render("Presiona ESPACIO para reiniciar", True, BLANCO)

                pos_game_over = texto_game_over.get_rect(center=(ANCHO / 2, ALTO / 2 - 50))
                pos_instruccion = texto_instruccion.get_rect(center=(ANCHO / 2, ALTO / 2 + 50))

                self.PANTALLA.blit(texto_game_over, pos_game_over)
                self.PANTALLA.blit(texto_instruccion, pos_instruccion)

            pygame.display.flip()
            self.reloj.tick(60)

        pygame.quit()


# --- PUNTO DE ENTRADA CON DEPURACIÓN ---
if __name__ == "__main__":
    try:
        juego = Game()
        juego.game_loop()
    except Exception as e:
        print("\n" + "=" * 50)
        print("¡EL JUEGO SE CERRÓ POR UN ERROR!")
        print("=" * 50)
        traceback.print_exc()
        print("=" * 50)
        input("Presiona ENTER para salir y corregir el error...")
```

**`clases/paso_a_paso/arkanoid/core_arkanoid/sprite_sheet/Player.py`**

```python
import pygame
from core.utils.utils import ANCHO


class Player:
    def __init__(self, x, y, imagen_recortada):
        # Recibimos la imagen desde el game.py en lugar de cargarla aquí
        self.image = imagen_recortada
        self.rect = self.image.get_rect()

        # Posicionamos el rectángulo donde nos digan
        self.rect.topleft = (x, y)
        self.velocidad = 5

    def mover(self, teclas):
        # Mueve a la izquierda si se presiona la tecla Y si no ha chocado con el borde izquierdo (0)
        if teclas[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocidad

        # Mueve a la derecha si se presiona la tecla Y si no ha chocado con el borde derecho (ANCHO)
        if teclas[pygame.K_RIGHT] and self.rect.right < ANCHO:
            self.rect.x += self.velocidad

    def dibujar(self, superficie):
        # Dibujamos la imagen en la posición del rect
        superficie.blit(self.image, self.rect)
```

**`clases/paso_a_paso/arkanoid/core_arkanoid/sprite_sheet/Ball.py`**

```python
import pygame
from core.utils.utils import ANCHO

class Ball:
    # AQUI ESTA LA CORRECCIÓN: agregamos 'imagen_recortada' a los parámetros
    def __init__(self, x, y, imagen_recortada):
        self.image = imagen_recortada
        self.rect = self.image.get_rect(center=(x, y))
        self.velocidad_x = 4
        self.velocidad_y = -4

    def update(self):
        self.rect.x += self.velocidad_x
        self.rect.y += self.velocidad_y

        # Rebote con las paredes laterales y superior
        if self.rect.left <= 0 or self.rect.right >= ANCHO:
            self.velocidad_x *= -1
        if self.rect.top <= 0:
            self.velocidad_y *= -1

    def dibujar(self, superficie):
        superficie.blit(self.image, self.rect)
```

**`clases/paso_a_paso/arkanoid/core_arkanoid/sprite_sheet/Brick.py`**

```python
# En Brick.py
import pygame

class Brick:
    def __init__(self, x, y, imagen_recortada):
        self.image = imagen_recortada
        self.rect = self.image.get_rect(topleft=(x, y))

    def dibujar(self, superficie):
        superficie.blit(self.image, self.rect)
```

**`clases/paso_a_paso/arkanoid/core_arkanoid/sprite_sheet/visor_sprites.py`**

```python
import pygame

pygame.init()

ruta_imagen = '../../assets/sprites/image_0918c1.png'
imagen = pygame.image.load(ruta_imagen)
pantalla = pygame.display.set_mode((imagen.get_width(), imagen.get_height()))
pygame.display.set_caption("Visor Pro - Haz clic y arrastra para enmarcar el sprite")

ejecutando = True
arrastrando = False
x_inicio, y_inicio = 0, 0
x_fin, y_fin = 0, 0

while ejecutando:
    pantalla.fill((255, 0, 255))  # Fondo fucsia
    pantalla.blit(imagen, (0, 0))

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

        # 1. Cuando presionas el clic, guardamos la esquina superior izquierda
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            arrastrando = True
            x_inicio, y_inicio = evento.pos
            x_fin, y_fin = evento.pos

        # 2. Mientras mueves el ratón sin soltar, actualizamos la esquina opuesta
        elif evento.type == pygame.MOUSEMOTION:
            if arrastrando:
                x_fin, y_fin = evento.pos

        # 3. Al soltar el clic, calculamos el cuadro final e imprimimos los datos
        elif evento.type == pygame.MOUSEBUTTONUP:
            arrastrando = False
            x = min(x_inicio, x_fin)
            y = min(y_inicio, y_fin)
            ancho = abs(x_fin - x_inicio)
            alto = abs(y_fin - y_inicio)
            print(f"Copia esto en tu código -> X: {x}, Y: {y}, Ancho: {ancho}, Alto: {alto}")

    # Dibujamos un rectángulo rojo para que veas qué estás recortando
    if arrastrando:
        x = min(x_inicio, x_fin)
        y = min(y_inicio, y_fin)
        ancho = abs(x_fin - x_inicio)
        alto = abs(y_fin - y_inicio)
        pygame.draw.rect(pantalla, (255, 0, 0), (x, y, ancho, alto), 2)

    pygame.display.flip()

pygame.quit()
```

## Controles

flechas para mover la paleta; `ESC`/cerrar la ventana para salir. (La segunda versión, con sprites cargados de spritesheet, está en `sprite_sheet/Game.py`.)

## Cómo ejecutar

Desde la carpeta `2027/`:

```bash
cd clases/paso_a_paso
python -m arkanoid.core_arkanoid.clase_7_arkanoid
```
