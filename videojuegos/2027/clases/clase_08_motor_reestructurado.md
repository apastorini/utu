# Clase 8 — Reestructuración del motor

Objetivo: dejar de escribir todo en un solo archivo y construir un **motor**
reutilizable. Se separan las responsabilidades en módulos:

- `game_loop`: el bucle principal y (a partir de aquí) el gestor de escenas `Game`.
- `ui`: `Scene` (base de las escenas) y `Button`.
- `game_object`: sprite base con imagen estática o animación.
- `sprite_sheet`: lee el JSON del editor de spritesheets.
- `asset_manager`: carga y sirve sprites/imágenes por nombre.
- `dialogue_manager`: mensajes en pantalla.
- `utils/`: colores, constantes y helpers.

En esta clase el motor soporta **los dos enfoques**: heredar de `GameLoop`
(estilo clásico) o heredar de `Game` y registrar escenas. El Arkanoid pasa a
usar el enfoque de escenas (`menu` → `game` → `game_over`).

> Nota: en la clase 9 se le añade audio y niveles; aquí ya está el código
> completo del Arkanoid para no dejar fragmentos.

## Motor — núcleo (código completo)

**`engine/game_loop.py`**

```python
"""
engine/game_loop.py

Aquí viven los dos "corazones" del motor:

- GameLoop: el bucle clásico. Se usa por herencia (enfoque Game Loop).
- Game: un GameLoop que además entiende de escenas (enfoque Game Scenes).

Los dos comparten el mismo bucle `run()`, la misma gestión de eventos y el
mismo manejo de ventana/clock. La diferencia es SOLO cómo se delega el
trabajo de cada frame.
"""

import pygame


class GameLoop:
    """
    Bucle principal del juego.

    Uso (enfoque Game Loop):
        class MiJuego(GameLoop):
            def __init__(self):
                super().__init__(800, 600, "Mi Juego", 60)

            def handle_specific_events(self, event): ...
            def update_game_logic(self): ...
            def draw_game_elements(self): ...

        MiJuego().run()
    """

    def __init__(self, screen_width=800, screen_height=600, title="Juego", fps=60):
        pygame.init()

        # La música/efectos necesitan el mixer. Si falla, seguimos sin audio.
        try:
            pygame.mixer.pre_init(44100, -16, 2, 512)
            pygame.mixer.init()
        except pygame.error:
            pass

        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.running = True

    # ------------------------------------------------------------------ #
    #  Bucle principal
    # ------------------------------------------------------------------ #
    def _handle_events(self):
        """Recoge los eventos, cierra si toca y los reparte."""
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            # Hook 1: un evento cada vez (estilo clásico de Pygame).
            self.handle_specific_events(event)
        # Hook 2: toda la lista de golpe (estilo escenas).
        self.handle_events(events)

    def _update(self):
        self.update_game_logic()

    def _draw(self):
        self.draw_game_elements()
        pygame.display.flip()

    def run(self):
        """Arranca el bucle. Sale cuando self.running es False."""
        self.running = True
        while self.running:
            self.clock.tick(self.fps)
            self._handle_events()
            self._update()
            self._draw()
        pygame.quit()

    # ------------------------------------------------------------------ #
    #  Hooks para las clases hijas
    # ------------------------------------------------------------------ #
    def handle_specific_events(self, event):
        """Se llama con CADA evento (enfoque Game Loop)."""
        pass

    def handle_events(self, events):
        """Se llama con la LISTA de eventos (enfoque Game Scenes)."""
        pass

    def update_game_logic(self):
        """Actualiza la lógica del juego."""
        pass

    def draw_game_elements(self):
        """Dibuja el juego en self.screen."""
        pass


class Game(GameLoop):
    """
    GameLoop con gestor de escenas (enfoque Game Scenes).

    Las escenas se registran pasando la CLASE (no la instancia); el motor
    las instancia de nuevo cada vez que se entra a ellas. Así el estado se
    reinicia solo al volver al menú, empezar otra partida, etc.

    Uso:
        class MiJuego(Game):
            def __init__(self):
                super().__init__(800, 600, "Mi Juego", 60)
                self.add_scene("menu", MenuScene)
                self.add_scene("juego", JuegoScene)
                self.change_scene("menu")

        MiJuego().run()
    """

    def __init__(self, screen_width=800, screen_height=600, title="Juego", fps=60):
        super().__init__(screen_width, screen_height, title, fps)
        self.scenes = {}
        self.current_scene = None
        self._pending_scene = None  # (nombre, kwargs)

    # ------------------------------------------------------------------ #
    #  Registro y cambio de escenas
    # ------------------------------------------------------------------ #
    def add_scene(self, name, scene_class):
        """
        Registra una escena. `scene_class` debe ser una clase que herede de
        `engine.ui.Scene` y reciba el juego como primer argumento.
        """
        self.scenes[name] = scene_class

    def change_scene(self, name, **kwargs):
        """
        Pide cambiar de escena. El cambio se aplica de forma segura al
        principio de la siguiente actualización (no en medio del dibujado).
        """
        self._pending_scene = (name, kwargs)

    def _apply_pending_scene(self):
        if self._pending_scene is None:
            return

        name, kwargs = self._pending_scene
        self._pending_scene = None

        if self.current_scene is not None and hasattr(self.current_scene, "on_exit"):
            self.current_scene.on_exit()

        scene_class = self.scenes[name]
        self.current_scene = scene_class(self, **kwargs)

        if hasattr(self.current_scene, "on_enter"):
            self.current_scene.on_enter()

    # ------------------------------------------------------------------ #
    #  Delegación en la escena activa
    # ------------------------------------------------------------------ #
    def handle_events(self, events):
        if self.current_scene is not None:
            self.current_scene.handle_events(events)

    def update_game_logic(self):
        self._apply_pending_scene()
        if self.current_scene is not None:
            self.current_scene.update()

    def draw_game_elements(self):
        if self.current_scene is not None:
            self.current_scene.draw(self.screen)
```

**`engine/ui.py`**

```python
"""
engine/ui.py

Elementos de interfaz reutilizables por cualquier escena.

- Scene: clase base para todas las escenas del juego.
- Button: botón sencillo con estado "hover" y callback.
"""

import pygame


class Scene:
    """
    Clase base para todas las escenas.

    Recibe una referencia al juego (`game`) para poder usar sus gestores
    (assets, audio, screen, change_scene...) y para cambiar de escena.
    """

    def __init__(self, game):
        self.game = game

    # Se llama justo al ENTRAR a la escena (después de crearla).
    def on_enter(self):
        pass

    # Se llama justo al SALIR de la escena.
    def on_exit(self):
        pass

    def handle_events(self, events):
        pass

    def update(self):
        pass

    def draw(self, surface):
        pass


class Button:
    """Botón rectangular con texto, efecto hover y callback."""

    def __init__(self, x, y, width, height, text, callback,
                 font_size=40, color=(50, 50, 80), hover_color=(80, 80, 110),
                 text_color=(255, 255, 255)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.font = pygame.font.Font(None, font_size)
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.callback()

    def draw(self, surface):
        hovered = self.rect.collidepoint(pygame.mouse.get_pos())
        color = self.hover_color if hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        pygame.draw.rect(surface, (20, 20, 30), self.rect, width=2, border_radius=8)
        text_surf = self.font.render(self.text, True, self.text_color)
        surface.blit(text_surf, text_surf.get_rect(center=self.rect.center))
```

**`engine/game_object.py`**

```python
"""
engine/game_object.py

Objeto base para todo lo que aparece en pantalla.

Puede representar:
- Un sprite estático (una sola Surface).
- Una animación (lista de Surfaces que se van rotando).
"""

import pygame


class GameObject(pygame.sprite.Sprite):
    """
    Sprite base con soporte de imagen estática o animación por frames.
    """

    def __init__(self, x, y, frames, anim_speed=0.1):
        super().__init__()

        if isinstance(frames, list):
            self.frames = frames
            self.is_animated = True
            self.current_frame = 0
            self.image = self.frames[self.current_frame]
            self.anim_speed = anim_speed  # frames avanzados por tick
            self.anim_timer = 0.0
        else:
            # Una sola Surface => estático
            self.frames = [frames]
            self.is_animated = False
            self.image = frames

        self.rect = self.image.get_rect(center=(x, y))

    def update_animation(self):
        """Avanza el frame de la animación cuando corresponde."""
        if not self.is_animated or len(self.frames) < 2:
            return

        self.anim_timer += self.anim_speed
        if self.anim_timer >= 1:
            self.anim_timer -= 1
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]

    def update(self, *args, **kwargs):
        """Actualización genérica: por defecto solo anima."""
        self.update_animation()

    def draw(self, surface):
        surface.blit(self.image, self.rect)
```

**`engine/sprite_sheet.py`**

```python
"""
engine/sprite_sheet.py

Lee un JSON generado por el editor de spritesheets del curso y permite
recortar sprites sueltos o animaciones completas de la imagen.

El JSON tiene esta forma (resumida):

    {
      "spritesheet_path": "ruta/imagen.png",
      "animations": {
        "idle":        [ {"name": "...", "x": 0, "y": 0, "width": 32, "height": 32}, ... ],
        "walk_right":  [ ... ]
      }
    }

La imagen se busca SIEMPRE junto al JSON (usando solo el nombre de archivo),
para que el proyecto funcione aunque se mueva de carpeta o de equipo.
"""

import os
import json

import pygame


class Spritesheet:
    """Carga y gestiona una spritesheet descrita por un JSON."""

    def __init__(self, json_path):
        with open(json_path, encoding="utf-8") as f:
            self.data = json.load(f)

        # Nos quedamos solo con el nombre de archivo y lo buscamos junto al JSON.
        spritesheet_filename = os.path.basename(self.data["spritesheet_path"])
        json_dir = os.path.dirname(json_path)
        full_image_path = os.path.join(json_dir, spritesheet_filename)

        self.spritesheet = pygame.image.load(full_image_path).convert_alpha()

    def get_sprite(self, name):
        """Devuelve una Surface a partir del nombre del sprite."""
        for anim_list in self.data["animations"].values():
            for sprite_data in anim_list:
                if sprite_data["name"] == name:
                    rect = pygame.Rect(
                        sprite_data["x"],
                        sprite_data["y"],
                        sprite_data["width"],
                        sprite_data["height"],
                    )
                    return self.spritesheet.subsurface(rect)
        raise ValueError(f"Sprite con nombre '{name}' no encontrado en el JSON.")

    def get_animation_frames(self, anim_name):
        """Devuelve la lista de Surfaces (frames) de una animación."""
        if anim_name not in self.data["animations"]:
            raise ValueError(f"Animación '{anim_name}' no encontrada en el JSON.")

        frames = []
        for sprite_data in self.data["animations"][anim_name]:
            rect = pygame.Rect(
                sprite_data["x"],
                sprite_data["y"],
                sprite_data["width"],
                sprite_data["height"],
            )
            frames.append(self.spritesheet.subsurface(rect))
        return frames

    def sprite_names(self):
        """Devuelve todos los nombres de sprite disponibles (útil para depurar)."""
        return sorted(
            sprite["name"]
            for anim_list in self.data["animations"].values()
            for sprite in anim_list
        )
```

**`engine/asset_manager.py`**

```python
"""
engine/asset_manager.py

Gestor centralizado de recursos gráficos (y punto de acceso a sonidos).
Carga cada recurso UNA vez y lo sirve por un nombre clave.
"""

import pygame

from engine.sprite_sheet import Spritesheet


class AssetManager:
    def __init__(self):
        self.spritesheets = {}
        self.images = {}
        self.sounds = {}

    # ---------------------------- Spritesheets ---------------------------- #
    def load_spritesheet(self, name, json_path):
        """Carga un spritesheet desde un JSON y lo guarda con un nombre clave."""
        try:
            self.spritesheets[name] = Spritesheet(json_path)
            print(f"Spritesheet '{name}' cargado desde '{json_path}'")
        except Exception as e:
            print(f"Error al cargar el spritesheet '{name}': {e}")
            raise

    def get_sprite(self, sheet_name, sprite_name):
        """Obtiene un sprite concreto de un spritesheet ya cargado."""
        if sheet_name not in self.spritesheets:
            raise KeyError(f"No se ha cargado un spritesheet con el nombre '{sheet_name}'")
        return self.spritesheets[sheet_name].get_sprite(sprite_name)

    def get_animation(self, sheet_name, anim_name):
        """Obtiene los frames de una animación de un spritesheet ya cargado."""
        if sheet_name not in self.spritesheets:
            raise KeyError(f"No se ha cargado un spritesheet con el nombre '{sheet_name}'")
        return self.spritesheets[sheet_name].get_animation_frames(anim_name)

    # ------------------------------- Imágenes ----------------------------- #
    def load_image(self, name, image_path):
        """Carga una imagen suelta y la guarda con un nombre clave."""
        try:
            self.images[name] = pygame.image.load(image_path).convert_alpha()
            print(f"Imagen '{name}' cargada desde '{image_path}'")
        except Exception as e:
            print(f"Error al cargar la imagen '{name}': {e}")
            raise

    def get_image(self, name):
        """Obtiene una imagen suelta ya cargada."""
        if name not in self.images:
            raise KeyError(f"No se ha cargado una imagen con el nombre '{name}'")
        return self.images[name]
```

**`engine/dialogue_manager.py`**

```python
"""
engine/dialogue_manager.py

Muestra mensajes/diálogos en pantalla, con duración opcional.
"""

import pygame


class DialogueManager:
    def __init__(self, screen, font_size=50, color=(255, 255, 255)):
        self.screen = screen
        self.font = pygame.font.Font(None, font_size)
        self.color = color

        self.active_message = None
        self.message_surface = None
        self.message_rect = None
        self.message_timer = 0
        self.message_duration = 0  # 0 => mensaje permanente

    def show_message(self, text, duration_seconds=0, position="center"):
        """Muestra un mensaje. Si la duración es 0, es permanente."""
        self.active_message = text
        self.message_surface = self.font.render(text, True, self.color)

        screen_rect = self.screen.get_rect()
        if position == "center":
            self.message_rect = self.message_surface.get_rect(center=screen_rect.center)
        elif position == "top":
            self.message_rect = self.message_surface.get_rect(
                centerx=screen_rect.centerx, top=20
            )
        else:
            self.message_rect = self.message_surface.get_rect(center=screen_rect.center)

        self.message_duration = duration_seconds * 1000
        self.message_timer = pygame.time.get_ticks()

    def update(self):
        if self.message_duration > 0:
            if pygame.time.get_ticks() - self.message_timer > self.message_duration:
                self.clear_message()

    def draw(self):
        if self.message_surface:
            self.screen.blit(self.message_surface, self.message_rect)

    def clear_message(self):
        self.active_message = None
        self.message_surface = None
        self.message_duration = 0
```

**`engine/utils/__init__.py`**

```python
"""Utilidades varias del motor (colores, constantes, helpers)."""

from engine.utils.colors import *
from engine.utils.utils import ANCHO, ALTO

__all__ = ["ANCHO", "ALTO"]
```

**`engine/utils/colors.py`**

```python
# engine/utils/colors.py
# Paleta de colores reutilizable en todos los juegos.

NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
VERDE = (0, 200, 0)
AZUL = (0, 0, 255)
AMARILLO = (255, 255, 0)
GRIS = (128, 128, 128)
AZUL_OSCURO = (30, 30, 40)
AZUL_CIELO = (92, 148, 252)
```

**`engine/utils/utils.py`**

```python
# engine/utils/utils.py
# Constantes globales de configuración por defecto.

ANCHO = 800
ALTO = 600
FPS = 60
TITULO = "Motor de Videojuegos"
```

**`engine/utils/load_sprites.py`**

```python
# engine/utils/load_sprites.py
# Helper para leer animaciones exportadas desde Piskel.

import json


def load_piskel_animation(json_path):
    """Devuelve (lista_de_rects, nombre_de_imagen) de un JSON de Piskel."""
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)
    frames = []
    for frame_data in data["frames"].values():
        rect = frame_data["frame"]
        frames.append((rect["x"], rect["y"], rect["w"], rect["h"]))
    return frames, data["meta"]["image"]
```


## Juego de ejemplo — Arkanoid (código completo)

**`arkanoid/__init__.py`**

```text
# arkanoid/__init__.py
```

**`arkanoid/entities.py`**

```text
# arkanoid/entities.py
import pygame

from engine.game_object import GameObject


class Paddle(GameObject):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)
        self.velocidad = 8

    def update(self, *args, **kwargs):
        super().update()
        ancho_pantalla = args[0]
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            self.rect.x -= self.velocidad
        if teclas[pygame.K_RIGHT]:
            self.rect.x += self.velocidad
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > ancho_pantalla:
            self.rect.right = ancho_pantalla


class Ball(GameObject):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)
        self.velocidad_x = 5
        self.velocidad_y = -5
        self.radius = self.rect.width // 2

    def update(self, *args, **kwargs):
        super().update()
        ancho_pantalla, alto_pantalla = args[0], args[1]

        self.rect.x += self.velocidad_x
        self.rect.y += self.velocidad_y

        if self.rect.left <= 0 or self.rect.right >= ancho_pantalla:
            self.velocidad_x *= -1
        if self.rect.top <= 0:
            self.velocidad_y *= -1

    def reset(self, x, y):
        self.rect.center = (x, y)
        self.velocidad_x = 5
        self.velocidad_y = -5


class Brick(GameObject):
    def __init__(self, x, y, initial_frame, assets, health=1, sprite_name=""):
        super().__init__(x, y, initial_frame)
        self.assets = assets
        self.health = health
        self.initial_health = health
        self.value = 10 * health
        self.name = sprite_name
        self.base_name = self._get_base_sprite_name()

    def _get_base_sprite_name(self):
        for suffix in ("_roto_1", "_roto_2", "_roto_!"):
            if self.name.endswith(suffix):
                return self.name[: -len(suffix)]
        return self.name

    def hit(self):
        """Resta vida. Devuelve True si el ladrillo debe destruirse."""
        self.health -= 1
        if self.health <= 0:
            return True
        try:
            damage_level = self.initial_health - self.health
            new_sprite_name = f"{self.base_name}_roto_{damage_level}"
            self.image = self.assets.get_sprite("main_ss", new_sprite_name)
        except (ValueError, KeyError):
            print(f"Advertencia: no se encontró el sprite de daño '{new_sprite_name}'.")
        return False


class PowerUp(GameObject):
    def __init__(self, x, y, image, power_type):
        super().__init__(x, y, image)
        self.type = power_type
        self.velocidad_y = 3

    def update(self, *args, **kwargs):
        super().update()
        self.rect.y += self.velocidad_y

    def activate(self, paddle, balls_group, all_sprites_group, assets):
        if self.type == "grow":
            paddle.rect.inflate_ip(paddle.rect.width * 0.5, 0)
        elif self.type == "extra_ball":
            try:
                new_ball_img = assets.get_sprite("main_ss", "pelota_bocha")
                new_ball = Ball(paddle.rect.centerx, paddle.rect.top, new_ball_img)
                balls_group.add(new_ball)
                all_sprites_group.add(new_ball)
            except (ValueError, KeyError):
                print("Advertencia: no se encontró 'pelota_bocha' para el power-up.")
```

**`arkanoid/level_loader.py`**

```text
# arkanoid/level_loader.py
import pygame

from arkanoid.entities import Brick

# Mapeo carácter -> (nombre de sprite en arkanoid.json, vidas)
BRICK_MAP = {
    "G": {"name": "bloque_gris", "health": 1},
    "M": {"name": "bloque_marron", "health": 2},
    "A": {"name": "bloque_azul", "health": 3},
    "S": {"name": "sprite_11", "health": 1},
}

BRICK_WIDTH, BRICK_HEIGHT = 32, 16
OFFSET_X, OFFSET_Y = 120, 80


def load_level_from_file(file_path, assets):
    """Carga un nivel desde un archivo de texto y devuelve un grupo de ladrillos."""
    ladrillos = pygame.sprite.Group()

    with open(file_path, encoding="utf-8") as f:
        for j, line in enumerate(f):
            for i, char in enumerate(line.strip()):
                if char not in BRICK_MAP:
                    continue
                data = BRICK_MAP[char]
                try:
                    brick_img = assets.get_sprite("main_ss", data["name"])
                    x = i * (BRICK_WIDTH + 4) + OFFSET_X
                    y = j * (BRICK_HEIGHT + 4) + OFFSET_Y
                    ladrillos.add(
                        Brick(x, y, brick_img, assets, data["health"], data["name"])
                    )
                except (ValueError, KeyError) as e:
                    print(f"Error al crear ladrillo desde el nivel: {e}")

    return ladrillos
```

**`arkanoid/scenes/__init__.py`**

```text
# arkanoid/scenes/__init__.py
```

**`arkanoid/scenes/menu_scene.py`**

```text
# arkanoid/scenes/menu_scene.py
import pygame

from engine.ui import Scene, Button


class MenuScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.font_title = pygame.font.Font(None, 90)
        self.font_hint = pygame.font.Font(None, 28)
        self.title = self.font_title.render("ARKANOID", True, (255, 255, 255))
        self.hint = self.font_hint.render(
            "Flechas para mover  |  Ratón para elegir  |  ESC para salir",
            True, (170, 180, 220),
        )
        self.start_button = Button(300, 320, 200, 56, "Jugar", self.start_game)
        self.quit_button = Button(300, 390, 200, 56, "Salir", self.quit_game)

    def on_enter(self):
        self.game.audio.play_music(volume=0.4)

    def start_game(self):
        self.game.puntuacion = 0
        self.game.change_scene("game", level_index=0)

    def quit_game(self):
        self.game.running = False

    def handle_events(self, events):
        for event in events:
            self.start_button.handle_event(event)
            self.quit_button.handle_event(event)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.game.running = False

    def update(self):
        pass

    def draw(self, surface):
        surface.fill((13, 20, 56))
        surface.blit(self.title, self.title.get_rect(centerx=surface.get_width() // 2, y=140))
        surface.blit(self.hint, self.hint.get_rect(centerx=surface.get_width() // 2, y=230))
        self.start_button.draw(surface)
        self.quit_button.draw(surface)
```

**`arkanoid/scenes/game_scene.py`**

```text
# arkanoid/scenes/game_scene.py
import os
import random

import pygame

from engine.ui import Scene
from arkanoid.entities import Paddle, Ball, PowerUp
from arkanoid.level_loader import load_level_from_file

# Lista ordenada de niveles. Al terminar el último, se gana la partida.
LEVELS = ["level_1.txt", "level_2.txt"]


class GameScene(Scene):
    def __init__(self, game, level_index=0):
        super().__init__(game)
        self.level_index = level_index

        self.BLANCO = (255, 255, 255)
        self.AZUL_OSCURO = (13, 20, 56)
        self.font_normal = pygame.font.Font(None, 36)
        self.font_grande = pygame.font.Font(None, 72)
        self.font_pequena = pygame.font.Font(None, 28)

        self.vidas = 3
        if not hasattr(self.game, "puntuacion"):
            self.game.puntuacion = 0

        self.powerups = pygame.sprite.Group()
        self.setup_level()

    # ------------------------------------------------------------------ #
    def setup_level(self):
        self.todos_los_sprites = pygame.sprite.Group()
        self.ladrillos = pygame.sprite.Group()
        self.pelotas = pygame.sprite.Group()

        pala_img = self.game.assets.get_sprite("main_ss", "paleta")
        self.pala = Paddle(self.game.screen.get_width() // 2,
                           self.game.screen.get_height() - 40, pala_img)

        bola_img = self.game.assets.get_sprite("main_ss", "pelota_bocha")
        self.bola = Ball(self.pala.rect.centerx, self.pala.rect.top - 20, bola_img)

        self.todos_los_sprites.add(self.pala, self.bola)
        self.pelotas.add(self.bola)

        level_path = os.path.join(self.game.game_dir, "levels", LEVELS[self.level_index])
        self.ladrillos = load_level_from_file(level_path, self.game.assets)
        self.todos_los_sprites.add(self.ladrillos)

        self.estado_juego = "jugando"

    # ------------------------------------------------------------------ #
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.game.change_scene("menu")

    def update(self):
        if self.estado_juego != "jugando":
            return

        w, h = self.game.screen.get_size()
        self.todos_los_sprites.update(w, h)

        for bola in self.pelotas:
            # Rebote con la pala
            if bola.rect.colliderect(self.pala.rect) and bola.velocidad_y > 0:
                bola.velocidad_y *= -1
                bola.rect.bottom = self.pala.rect.top
                self.game.audio.play_sound("hit_paddle")

            # Rebote con ladrillos
            golpeados = pygame.sprite.spritecollide(bola, self.ladrillos, False)
            if golpeados:
                ladrillo = golpeados[0]
                bola.velocidad_y *= -1
                if ladrillo.hit():
                    ladrillo.kill()
                    self.game.puntuacion += ladrillo.value
                    self.game.audio.play_sound("hit_brick")
                    if random.random() < 0.25:
                        self._spawn_powerup(ladrillo)

        # Recoger power-ups
        for powerup in pygame.sprite.spritecollide(self.pala, self.powerups, True):
            powerup.activate(self.pala, self.pelotas, self.todos_los_sprites, self.game.assets)

        # Pelotas que caen por debajo de la pantalla
        for bola in self.pelotas.copy():
            if bola.rect.top > self.game.screen.get_height():
                bola.kill()

        if not self.pelotas:
            self._perder_vida()

        if not self.ladrillos:
            self._nivel_completado()

    # ------------------------------------------------------------------ #
    def _spawn_powerup(self, ladrillo):
        try:
            powerup_img = self.game.assets.get_sprite("main_ss", "sprite_24")
            nuevo = PowerUp(ladrillo.rect.centerx, ladrillo.rect.centery,
                            powerup_img, "grow")
            self.powerups.add(nuevo)
            self.todos_los_sprites.add(nuevo)
        except (ValueError, KeyError):
            pass

    def _perder_vida(self):
        self.vidas -= 1
        self.game.audio.play_sound("lose_life")
        if self.vidas <= 0:
            self.game.change_scene("game_over", win=False)
        else:
            # Recolocar la bola sobre la pala y seguir jugando
            self.bola = Ball(self.pala.rect.centerx, self.pala.rect.top - 20,
                             self.game.assets.get_sprite("main_ss", "pelota_bocha"))
            self.pelotas.add(self.bola)
            self.todos_los_sprites.add(self.bola)

    def _nivel_completado(self):
        if self.level_index + 1 < len(LEVELS):
            self.game.change_scene("game", level_index=self.level_index + 1)
        else:
            self.game.change_scene("game_over", win=True)

    # ------------------------------------------------------------------ #
    def draw(self, surface):
        surface.fill(self.AZUL_OSCURO)
        self.todos_los_sprites.draw(surface)

        texto = self.font_normal.render(f"Puntuación: {self.game.puntuacion}", True, self.BLANCO)
        surface.blit(texto, (10, 10))

        vidas = self.font_normal.render(f"Vidas: {self.vidas}", True, self.BLANCO)
        surface.blit(vidas, (surface.get_width() - vidas.get_width() - 10, 10))

        nivel = self.font_pequena.render(f"Nivel {self.level_index + 1}/{len(LEVELS)}", True, self.BLANCO)
        surface.blit(nivel, nivel.get_rect(centerx=surface.get_width() // 2, top=15))
```

**`arkanoid/scenes/game_over_scene.py`**

```text
# arkanoid/scenes/game_over_scene.py
import pygame

from engine.ui import Scene, Button


class GameOverScene(Scene):
    def __init__(self, game, win=False):
        super().__init__(game)
        self.win = win
        self.font_grande = pygame.font.Font(None, 90)
        self.font_normal = pygame.font.Font(None, 36)
        self.menu_button = Button(300, 380, 200, 56, "Menú", self.volver_al_menu)

    def volver_al_menu(self):
        self.game.change_scene("menu")

    def handle_events(self, events):
        for event in events:
            self.menu_button.handle_event(event)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.game.change_scene("menu")

    def draw(self, surface):
        surface.fill((13, 20, 56))
        titulo = "¡VICTORIA!" if self.win else "GAME OVER"
        color = (120, 230, 120) if self.win else (240, 90, 90)
        t = self.font_grande.render(titulo, True, color)
        surface.blit(t, t.get_rect(centerx=surface.get_width() // 2, centery=220))

        p = self.font_normal.render(f"Puntuación final: {self.game.puntuacion}",
                                    True, (255, 255, 255))
        surface.blit(p, p.get_rect(centerx=surface.get_width() // 2, centery=300))

        self.menu_button.draw(surface)
```

**`arkanoid/game.py`**

```text
# arkanoid/game.py
import os

from engine.game_loop import Game
from engine.asset_manager import AssetManager
from engine.audio import AudioManager
from arkanoid.scenes.menu_scene import MenuScene
from arkanoid.scenes.game_scene import GameScene
from arkanoid.scenes.game_over_scene import GameOverScene


class ArkanoidGame(Game):
    """
    Arkanoid usando el enfoque de ESCENAS:
    'menu' -> 'game' (niveles) -> 'game_over'
    """

    def __init__(self):
        super().__init__(800, 600, "Arkanoid", 60)

        self.game_dir = os.path.dirname(__file__)
        self.assets_dir = os.path.join(self.game_dir, "assets")

        self.assets = AssetManager()
        self.audio = AudioManager()
        self.puntuacion = 0

        self.load_assets()

        # Registramos las escenas (clases, no instancias).
        self.add_scene("menu", MenuScene)
        self.add_scene("game", GameScene)
        self.add_scene("game_over", GameOverScene)
        self.change_scene("menu")

    def load_assets(self):
        """Carga imágenes, spritesheets y sonidos del Arkanoid."""
        sprites_path = os.path.join(self.assets_dir, "sprites")
        audio_path = os.path.join(self.assets_dir, "audio")

        try:
            self.assets.load_spritesheet("main_ss", os.path.join(sprites_path, "arkanoid.json"))
            self.assets.load_image("ball_img", os.path.join(sprites_path, "ball.png"))
        except Exception as e:
            print(f"Error fatal al cargar imágenes: {e}")
            self.running = False

        # El audio es opcional: si falta un archivo, seguimos jugando.
        self.audio.load_sound("hit_paddle", os.path.join(audio_path, "hit_paddle.wav"))
        self.audio.load_sound("hit_brick", os.path.join(audio_path, "hit_brick.wav"))
        self.audio.load_sound("lose_life", os.path.join(audio_path, "lose_life.wav"))
        self.audio.load_music(os.path.join(audio_path, "music.mp3"))
```

**`arkanoid/main.py`**

```text
# arkanoid/main.py
"""
Ejecutar desde la carpeta 2027 con:
    python -m arkanoid.main
o directamente:
    python arkanoid/main.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from arkanoid.game import ArkanoidGame


def main():
    ArkanoidGame().run()


if __name__ == "__main__":
    main()
```

**`arkanoid/levels/level_1.txt`**

```text
GGGGGGGGGG
GMMMMMMMMG
MMAAAAAAMM
MMAAAAAAMM
GMMMMMMMMG
GGGGGGGGGG
```

**`arkanoid/levels/level_2.txt`**

```text
GGGGGGGGGGGG
GAAAAAAAAAAG
GMMSSSSSSMMG
GMMAAAAAAMMG
GMMMMMMMMMMG
GGGGGGGGGGGG
```

