# Clases 10 y 11 — Juegos de plataforma

Objetivo: construir un **plataformero** con:
- Niveles creados en **Tiled** (`.json` + `.tsx`).
- `engine/tilemap.py`: convierte el nivel en grupos de sprites (suelo, colisiones, spawns).
- `engine/camera.py`: scrolling que sigue al jugador.
- Entidades (`Player`, `Enemy`) con gravedad y colisiones.

Se usa el enfoque de **escenas** (`Game` + `Scene`) y `TilemapLoader`
acepta tanto `player_start` como `start_point` para la posición inicial.

## Motor — nuevos módulos (código completo)

**`engine/tilemap.py`**

```python
"""
engine/tilemap.py

Carga niveles creados en Tiled (.json + .tsx/.png) y los convierte en
grupos de sprites listos para el juego.

Devuelve:
    sprite_groups, world_width, world_height, player_start_pos

donde `sprite_groups` es un diccionario con:
    "all_sprites"      -> todos los tiles
    "collision_sprites"-> solo los tiles que colisionan
    "enemies"          -> marcadores de spawn de enemigos (objetos)
    "powerups"         -> marcadores de spawn de power-ups (objetos)

Además, los marcadores de spawn se exponen también como lista en
`sprite_groups["spawns"]` por comodidad.

Es tolerante con los nombres usados en los distintos ejemplos del curso:
acepta `player_start` o `start_point` para la posición inicial del jugador.
"""

import os
import json
import xml.etree.ElementTree as ET

import pygame

from .game_object import GameObject


class Tile(GameObject):
    """Un tile estático del mapa, posicionado por su esquina superior izquierda."""

    def __init__(self, x, y, image):
        super().__init__(x, y, image)
        self.rect = self.image.get_rect(topleft=(x, y))


class Spawn(pygame.sprite.Sprite):
    """Marcador invisible creado a partir de un objeto de Tiled."""

    def __init__(self, x, y, kind, properties=None):
        super().__init__()
        self.image = pygame.Surface((16, 16), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.kind = kind
        self.properties = properties or {}


def _as_bool(value):
    return str(value).lower() in ("true", "1", "yes")


class TilemapLoader:
    def __init__(self, assets_manager):
        self.assets = assets_manager

    def load_level(self, level_json_path):
        try:
            with open(level_json_path, encoding="utf-8") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error fatal al cargar o leer el archivo de nivel: {e}")
            return None, 0, 0, (150, 150)

        tile_width = data["tilewidth"]
        tile_height = data["tileheight"]
        json_dir = os.path.dirname(level_json_path)

        # --- 1. Tileset (imagen + propiedades de tiles) --- #
        tileset_info = data["tilesets"][0]
        first_gid = tileset_info["firstgid"]
        tileset_image_filename = ""
        tile_properties = {}

        if "source" in tileset_info:
            tsx_path = os.path.join(json_dir, tileset_info["source"])
            try:
                root = ET.parse(tsx_path).getroot()
                tileset_image_filename = root.find("image").get("source")
                for tile_node in root.findall("tile"):
                    tile_id = int(tile_node.get("id"))
                    props_node = tile_node.find("properties")
                    if props_node is not None:
                        tile_properties[tile_id] = {}
                        for prop_node in props_node.findall("property"):
                            name = prop_node.get("name")
                            value = prop_node.get("value")
                            if prop_node.get("type") == "bool":
                                value = _as_bool(value)
                            tile_properties[tile_id][name] = value
            except Exception as e:
                print(f"Error al leer el archivo .tsx en '{tsx_path}': {e}")
                return None, 0, 0, (150, 150)
        elif "image" in tileset_info:
            tileset_image_filename = tileset_info["image"]

        if not tileset_image_filename:
            print("Error: no se encontró la imagen del tileset.")
            return None, 0, 0, (150, 150)

        tileset_image_path = os.path.join(json_dir, tileset_image_filename)
        tileset_name = os.path.basename(tileset_image_path)
        self.assets.load_image(tileset_name, tileset_image_path)
        tileset_img = self.assets.get_image(tileset_name)

        tiles = {}
        gid = first_gid
        for y in range(0, tileset_img.get_height(), tile_height):
            for x in range(0, tileset_img.get_width(), tile_width):
                if (x + tile_width <= tileset_img.get_width()
                        and y + tile_height <= tileset_img.get_height()):
                    tiles[gid] = tileset_img.subsurface((x, y, tile_width, tile_height))
                    gid += 1

        # --- 2. Capas --- #
        world_width = data["width"] * tile_width
        world_height = data["height"] * tile_height

        sprite_groups = {
            "all_sprites": pygame.sprite.Group(),
            "collision_sprites": pygame.sprite.Group(),
            "enemies": pygame.sprite.Group(),
            "powerups": pygame.sprite.Group(),
        }
        spawns = []
        player_start_pos = (150, 150)  # posición por defecto a prueba de fallos

        for layer in data["layers"]:
            if layer["type"] == "tilelayer" and "data" in layer:
                layer_collides = False
                for prop in layer.get("properties", []):
                    if prop.get("name") == "collide" and _as_bool(prop.get("value")):
                        layer_collides = True

                for i, gid_val in enumerate(layer["data"]):
                    if gid_val == 0 or gid_val not in tiles:
                        continue

                    pos_x = (i % data["width"]) * tile_width
                    pos_y = (i // data["width"]) * tile_height

                    tile_sprite = Tile(pos_x, pos_y, tiles[gid_val])
                    sprite_groups["all_sprites"].add(tile_sprite)

                    tile_id_in_tileset = gid_val - first_gid
                    props = tile_properties.get(tile_id_in_tileset, {})
                    tile_collides = _as_bool(props.get("collides", props.get("collide", False)))
                    if layer_collides or tile_collides:
                        sprite_groups["collision_sprites"].add(tile_sprite)

            elif layer["type"] == "objectgroup":
                for obj in layer.get("objects", []):
                    self._process_object(obj, sprite_groups, spawns)
                    if obj.get("name") in ("player_start", "start_point"):
                        player_start_pos = (obj["x"], obj["y"])

        sprite_groups["spawns"] = spawns
        return sprite_groups, world_width, world_height, player_start_pos

    # ------------------------------------------------------------------ #
    @staticmethod
    def _process_object(obj, sprite_groups, spawns):
        """Clasifica un objeto de Tiled como enemigo, power-up o ignorado."""
        label = f"{obj.get('name', '')} {obj.get('type', '')}".lower()
        kind = None
        if "enem" in label:
            kind = "enemy"
        elif "power" in label or "potion" in label or "vida" in label or "coin" in label:
            kind = "powerup"

        if kind is None:
            return

        props = {p.get("name"): p.get("value") for p in obj.get("properties", [])}
        spawn = Spawn(obj["x"], obj["y"], kind, props)
        spawns.append(spawn)
        sprite_groups["enemies" if kind == "enemy" else "powerups"].add(spawn)
```

**`engine/camera.py`**

```python
"""
engine/camera.py

Cámara (scrolling) que sigue a una entidad y limita el desplazamiento
al tamaño del mundo.
"""

import pygame


class Camera:
    def __init__(self, screen_width, screen_height, world_width, world_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.world_width = world_width
        self.world_height = world_height
        self.camera_rect = pygame.Rect(0, 0, screen_width, screen_height)

    def apply(self, entity):
        """Devuelve el Rect de la entidad desplazado por la cámara."""
        return entity.rect.move(self.camera_rect.topleft)

    def apply_rect(self, rect):
        """Igual que apply() pero para un Rect cualquiera."""
        return rect.move(self.camera_rect.topleft)

    def update(self, target):
        """Centra la cámara en el objetivo dentro de los límites del mundo."""
        x = -target.rect.centerx + int(self.screen_width / 2)
        y = -target.rect.centery + int(self.screen_height / 2)

        x = min(0, x)
        y = min(0, y)
        x = max(-(self.world_width - self.screen_width), x)
        y = max(-(self.world_height - self.screen_height), y)

        self.camera_rect.topleft = (x, y)
```


## Juego de ejemplo — Plataformero (código completo)

**`platformer/__init__.py`**

```python
# platformer/__init__.py
```

**`platformer/entities.py`**

```python
# platformer/entities.py
import pygame

from engine.game_object import GameObject


class Player(GameObject):
    """Jugador con animaciones, gravedad y colisiones contra plataformas."""

    def __init__(self, x, y, assets, scale=(48, 48)):
        self.assets = assets
        self.scale = scale
        self.animations = {
            "idle": self.assets.get_animation("player_ss", "idle"),
            "walk_right": self.assets.get_animation("player_ss", "walk_right"),
            "walk_left": self.assets.get_animation("player_ss", "walk_left"),
        }

        super().__init__(x, y, self.animations["idle"])

        self.velocidad_mov = 4
        self.fuerza_salto = 16
        self.gravedad = 0.7
        self.pos = pygame.math.Vector2(self.rect.center)
        self.vel = pygame.math.Vector2(0, 0)
        self.en_suelo = False
        self.current_animation_name = "idle"
        self.vidas = 3
        self._apply_scale()

    def _apply_scale(self):
        self.image = pygame.transform.scale(self.image, self.scale)
        self.rect = self.image.get_rect(center=self.rect.center)

    def set_animation(self, anim_name):
        if self.current_animation_name != anim_name:
            self.current_animation_name = anim_name
            self.frames = self.animations[anim_name]
            self.current_frame = 0

    def update(self, plataformas=None, *args, **kwargs):
        if plataformas is None:
            plataformas = pygame.sprite.Group()

        self.vel.x = 0
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            self.vel.x = -self.velocidad_mov
            self.set_animation("walk_left")
        elif teclas[pygame.K_RIGHT]:
            self.vel.x = self.velocidad_mov
            self.set_animation("walk_right")
        else:
            self.set_animation("idle")

        if teclas[pygame.K_SPACE] and self.en_suelo:
            self.vel.y = -self.fuerza_salto

        self.vel.y += self.gravedad
        if self.vel.y > 20:
            self.vel.y = 20

        # Movimiento y colisión en X
        self.pos.x += self.vel.x
        self.rect.centerx = round(self.pos.x)
        self._check_collision_x(plataformas)

        # Movimiento y colisión en Y
        self.pos.y += self.vel.y
        self.rect.centery = round(self.pos.y)
        self._check_collision_y(plataformas)

        super().update()  # animación
        self._apply_scale()

    def _check_collision_x(self, plataformas):
        for plat in pygame.sprite.spritecollide(self, plataformas, False):
            if self.vel.x > 0:
                self.rect.right = plat.rect.left
            elif self.vel.x < 0:
                self.rect.left = plat.rect.right
            self.pos.x = self.rect.centerx

    def _check_collision_y(self, plataformas):
        self.en_suelo = False
        for plat in pygame.sprite.spritecollide(self, plataformas, False):
            if self.vel.y > 0:
                self.rect.bottom = plat.rect.top
                self.en_suelo = True
                self.vel.y = 0
            elif self.vel.y < 0:
                self.rect.top = plat.rect.bottom
                self.vel.y = 0
            self.pos.y = self.rect.centery

    def reset(self, x, y):
        self.pos.update(x, y)
        self.rect.center = (x, y)
        self.vel.update(0, 0)


class Enemy(GameObject):
    """
    Enemigo sencillo que patrulla horizontalmente y cae con la gravedad.
    Si no se le pasa imagen, se genera un cuadrado rojo.
    """

    def __init__(self, x, y, image=None):
        if image is None:
            image = pygame.Surface((24, 24), pygame.SRCALPHA)
            pygame.draw.circle(image, (200, 40, 40), (12, 12), 12)
        super().__init__(x, y, image)

        self.vel_x = 2
        self.vel_y = 0
        self.gravedad = 0.7
        self.pos = pygame.math.Vector2(self.rect.center)
        self.en_suelo = False

    def update(self, plataformas=None, *args, **kwargs):
        if plataformas is None:
            plataformas = pygame.sprite.Group()

        self.vel_y += self.gravedad
        if self.vel_y > 20:
            self.vel_y = 20

        self.pos.x += self.vel_x
        self.rect.centerx = round(self.pos.x)
        for plat in pygame.sprite.spritecollide(self, plataformas, False):
            if self.vel_x > 0:
                self.rect.right = plat.rect.left
            else:
                self.rect.left = plat.rect.right
            self.vel_x *= -1
            self.pos.x = self.rect.centerx

        self.pos.y += self.vel_y
        self.rect.centery = round(self.pos.y)
        self.en_suelo = False
        for plat in pygame.sprite.spritecollide(self, plataformas, False):
            if self.vel_y > 0:
                self.rect.bottom = plat.rect.top
                self.en_suelo = True
                self.vel_y = 0
            elif self.vel_y < 0:
                self.rect.top = plat.rect.bottom
                self.vel_y = 0
            self.pos.y = self.rect.centery

        super().update()
```

**`platformer/scenes/__init__.py`**

```python
# platformer/scenes/__init__.py
```

**`platformer/scenes/menu_scene.py`**

```python
# platformer/scenes/menu_scene.py
import pygame

from engine.ui import Scene, Button


class MenuScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.font_title = pygame.font.Font(None, 74)
        self.title = self.font_title.render("MARIO CLONE", True, (255, 255, 255))
        self.start_button = Button(412, 320, 200, 56, "Jugar", self.start_game)

    def on_enter(self):
        self.game.audio.play_music(volume=0.4)

    def start_game(self):
        self.game.change_scene("game")

    def handle_events(self, events):
        for event in events:
            self.start_button.handle_event(event)

    def draw(self, surface):
        surface.fill((92, 148, 252))
        surface.blit(self.title, self.title.get_rect(centerx=surface.get_width() // 2, y=150))
        self.start_button.draw(surface)
```

**`platformer/scenes/game_scene.py`**

```python
# platformer/scenes/game_scene.py
import os

import pygame

from engine.ui import Scene
from engine.tilemap import TilemapLoader
from engine.camera import Camera
from platformer.entities import Player, Enemy


class GameScene(Scene):
    def __init__(self, game):
        super().__init__(game)

        loader = TilemapLoader(self.game.assets)
        level_path = os.path.join(self.game.game_dir, "assets", "sprites", "nivel_1.json")

        result = loader.load_level(level_path)
        if result is None or result[0] is None:
            self.game.change_scene("menu")
            return

        self.sprite_groups, self.world_w, self.world_h, player_start = result

        # Jugador
        self.jugador = Player(player_start[0], player_start[1], self.game.assets)
        self.sprite_groups["all_sprites"].add(self.jugador)

        # Enemigos a partir de los marcadores del tilemap (si los hay)
        self.enemigos = pygame.sprite.Group()
        for spawn in self.sprite_groups.get("spawns", []):
            if spawn.kind == "enemy":
                enemigo = Enemy(spawn.rect.x, spawn.rect.y)
                self.enemigos.add(enemigo)
                self.sprite_groups["all_sprites"].add(enemigo)

        self.camara = Camera(self.game.screen.get_width(),
                             self.game.screen.get_height(),
                             self.world_w, self.world_h)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.game.change_scene("menu")

    def update(self):
        plataformas = self.sprite_groups["collision_sprites"]
        self.sprite_groups["all_sprites"].update(plataformas=plataformas)
        self.camara.update(self.jugador)

        # ¿Hemos llegado al final del nivel?
        if self.jugador.rect.right >= self.world_w - 64:
            self.game.change_scene("game_over", win=True)

        # ¿Nos ha tocado un enemigo?
        if pygame.sprite.spritecollide(self.jugador, self.enemigos, False):
            self.game.change_scene("game_over", win=False)

        # ¿Nos hemos caído del mundo?
        if self.jugador.rect.top > self.world_h:
            self.game.change_scene("game_over", win=False)

    def draw(self, surface):
        surface.fill((92, 148, 252))  # cielo
        for sprite in self.sprite_groups["all_sprites"]:
            surface.blit(sprite.image, self.camara.apply(sprite))
```

**`platformer/scenes/game_over_scene.py`**

```python
# platformer/scenes/game_over_scene.py
import pygame

from engine.ui import Scene, Button


class GameOverScene(Scene):
    def __init__(self, game, win=False):
        super().__init__(game)
        self.win = win
        self.font_grande = pygame.font.Font(None, 80)
        self.menu_button = Button(412, 420, 200, 56, "Menú", self.volver_al_menu)

    def volver_al_menu(self):
        self.game.change_scene("menu")

    def handle_events(self, events):
        for event in events:
            self.menu_button.handle_event(event)

    def draw(self, surface):
        surface.fill((40, 60, 110))
        titulo = "¡NIVEL COMPLETADO!" if self.win else "GAME OVER"
        color = (140, 240, 140) if self.win else (240, 90, 90)
        t = self.font_grande.render(titulo, True, color)
        surface.blit(t, t.get_rect(centerx=surface.get_width() // 2, centery=280))
        self.menu_button.draw(surface)
```

**`platformer/game.py`**

```python
# platformer/game.py
import os

from engine.game_loop import Game
from engine.asset_manager import AssetManager
from engine.audio import AudioManager
from platformer.scenes.menu_scene import MenuScene
from platformer.scenes.game_scene import GameScene
from platformer.scenes.game_over_scene import GameOverScene


class PlatformerGame(Game):
    """
    Plataformero usando el enfoque de ESCENAS + tilemap + cámara.
    """

    def __init__(self):
        super().__init__(1024, 768, "Plataformero", 60)

        self.game_dir = os.path.dirname(__file__)
        self.assets_dir = os.path.join(self.game_dir, "assets", "sprites")

        self.assets = AssetManager()
        self.audio = AudioManager()

        self.load_assets()

        self.add_scene("menu", MenuScene)
        self.add_scene("game", GameScene)
        self.add_scene("game_over", GameOverScene)
        self.change_scene("menu")

    def load_assets(self):
        try:
            self.assets.load_spritesheet("player_ss", os.path.join(self.assets_dir, "mario.json"))
        except Exception as e:
            print(f"Error fatal al cargar assets del jugador: {e}")
            self.running = False

        self.audio.load_music(os.path.join(self.game_dir, "assets", "audio", "music.mp3"))
```

**`platformer/main.py`**

```python
# platformer/main.py
"""
Ejecutar desde la carpeta 2027 con:
    python -m platformer.main
o directamente:
    python platformer/main.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from platformer.game import PlatformerGame


def main():
    PlatformerGame().run()


if __name__ == "__main__":
    main()
```

