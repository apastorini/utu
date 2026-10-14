# Clases 21 a 23 — Aventura gráfica (hotspots, inventario, diálogos)

Objetivo: una **aventura gráfica** point-and-click.
`engine/hotspot.py` (zonas interactivas), `engine/inventory.py`
(inventario y objetos), `engine/cursor.py` (puntero propio) y
`engine/dialogue.py` (diálogos ramificados).

El ejemplo es `adventure/` (enfoque **Game + Escenas**): habitaciones
conectadas, un NPC con diálogo, una llave y una puerta que se abre
solo si la tienes. Se puede **completar**.

## Motor — código completo de los módulos nuevos

**`engine/hotspot.py`**

```python
"""
engine/hotspot.py

Zonas interactivas para aventuras gráficas: una región de la pantalla que
reacciona al pasar/click del ratón (abrir una puerta, coger un objeto,
hablar con un personaje...).
"""

import pygame


class Hotspot:
    def __init__(self, rect, name="", callback=None, cursor="hand",
                 visible=False, color=(255, 255, 0)):
        self.rect = pygame.Rect(rect)
        self.name = name
        self.callback = callback
        self.cursor = cursor
        self.visible = visible
        self.color = color

    def contains(self, pos):
        return self.rect.collidepoint(pos)

    def activate(self):
        if self.callback:
            self.callback(self)

    def handle_event(self, event):
        """Devuelve True si el click cayó dentro de la zona."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.contains(event.pos):
                self.activate()
                return True
        return False

    def draw(self, surface):
        """Dibuja el contorno (solo para depurar)."""
        if self.visible:
            pygame.draw.rect(surface, self.color, self.rect, 2)
```

**`engine/inventory.py`**

```python
"""
engine/inventory.py

Inventario sencillo para aventuras gráficas y RPG.
"""

import pygame


class Item:
    def __init__(self, name, image=None, description="", usable=True):
        self.name = name
        self.image = image
        self.description = description
        self.usable = usable


class Inventory:
    def __init__(self, capacity=8):
        self.capacity = capacity
        self.items = []
        self.selected = None

    def add(self, item):
        if len(self.items) < self.capacity and not self.has(item.name):
            self.items.append(item)
            return True
        return False

    def remove(self, name):
        self.items = [i for i in self.items if i.name != name]
        if self.selected and self.selected.name == name:
            self.selected = None

    def has(self, name):
        return any(i.name == name for i in self.items)

    def get(self, name):
        for i in self.items:
            if i.name == name:
                return i
        return None

    def select(self, name):
        self.selected = self.get(name)

    def handle_event(self, event, origin, slot=56):
        """Permite seleccionar un objeto con click. `origin` = (x, y) del panel."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for index, item in enumerate(self.items):
                rect = pygame.Rect(origin[0], origin[1] + index * slot, slot, slot)
                if rect.collidepoint(event.pos):
                    self.selected = item
                    return item
        return None

    def draw(self, surface, origin, slot=56):
        x, y = origin
        panel = pygame.Rect(x - 6, y - 6, slot + 12,
                            slot * self.capacity + 12)
        pygame.draw.rect(surface, (0, 0, 0, 150), panel, border_radius=6)
        pygame.draw.rect(surface, (220, 220, 220), panel, 2, border_radius=6)

        font = pygame.font.Font(None, 22)
        for index in range(self.capacity):
            rect = pygame.Rect(x, y + index * slot, slot, slot)
            pygame.draw.rect(surface, (70, 70, 90), rect, 1)
            if index < len(self.items):
                item = self.items[index]
                if item.image:
                    img = pygame.transform.scale(item.image, (slot - 10, slot - 10))
                    surface.blit(img, img.get_rect(center=rect.center))
                else:
                    label = font.render(item.name[:6], True, (240, 240, 240))
                    surface.blit(label, label.get_rect(center=rect.center))
                if self.selected is item:
                    pygame.draw.rect(surface, (255, 220, 0), rect, 3)
```

**`engine/cursor.py`**

```python
"""
engine/cursor.py

Cursor personalizado para aventuras gráficas. Se dibuja el puntero nosotros
mismos (en vez del del sistema) para poder cambiar de aspecto cuando está
sobre una zona interactiva (hotspot).
"""

import pygame


class Cursor:
    def __init__(self, normal=None, hover=None, size=22):
        self.size = size
        self.normal = normal or self._make_arrow((255, 255, 255), (0, 0, 0))
        self.hover = hover or self._make_cross((255, 80, 80), (0, 0, 0))
        self.visible = True

    def _make_arrow(self, fill, outline):
        size = self.size * 2
        surf = pygame.Surface((size, size), pygame.SRCALPHA)
        points = [(4, 2), (4, size - 8), (size // 2 - 2, size // 2 + 2), (size - 4, size // 2 + 2)]
        pygame.draw.polygon(surf, fill, points)
        pygame.draw.polygon(surf, outline, points, 2)
        return surf

    def _make_cross(self, fill, outline):
        size = self.size
        surf = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(surf, fill, (size // 2, size // 2), size // 2 - 2)
        pygame.draw.circle(surf, outline, (size // 2, size // 2), size // 2 - 2, 2)
        return surf

    def draw(self, surface, hovered=False):
        if not self.visible:
            return
        pygame.mouse.set_visible(False)
        image = self.hover if hovered else self.normal
        pos = pygame.mouse.get_pos()
        surface.blit(image, image.get_rect(center=pos))
```

**`engine/dialogue.py`**

```python
"""
engine/dialogue.py

Diálogos con ramificaciones (árbol de conversación) y, opcionalmente, la
posibilidad de generar respuestas con IA. Si no hay IA disponible, el juego
funciona igual con los nodos escritos a mano.

Ejemplo de uso:

    nodes = {
        "start": DialogueNode("¡Hola! ¿Qué quieres?", speaker="NPC",
                              choices=[("Comprar", "comprar"), ("Adiós", None)]),
        "comprar": DialogueNode("Aquí tienes.", speaker="NPC"),
    }
    box.start(nodes, "start")
"""

import textwrap

import pygame


class DialogueNode:
    def __init__(self, text, speaker="", choices=None, action=None, portrait=None):
        self.text = text
        self.speaker = speaker
        self.choices = choices or []   # lista de (etiqueta, siguiente_nodo_o_None)
        self.action = action           # callback opcional al entrar
        self.portrait = portrait


class DialogueBox:
    def __init__(self, screen, font_size=26, height=170, width_ratio=0.9):
        self.screen = screen
        self.width = int(screen.get_width() * width_ratio)
        self.height = height
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.midbottom = (screen.get_width() // 2, screen.get_height() - 10)
        self.font = pygame.font.Font(None, font_size)
        self.small = pygame.font.Font(None, font_size - 4)
        self.nodes = {}
        self.current = None
        self.lines = []
        self.choice_index = 0
        self.active = False

    def start(self, nodes, start="start"):
        self.nodes = nodes
        self.active = True
        self._go_to(start)

    def _go_to(self, name):
        self.current = self.nodes.get(name)
        self.choice_index = 0
        if self.current:
            if self.current.action:
                self.current.action(self.current)
            self.lines = textwrap.wrap(self.current.text, 52)

    def handle_event(self, event):
        if not self.active or not self.current:
            return
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self._confirm()
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                if self.current.choices:
                    self.choice_index = (self.choice_index + 1) % len(self.current.choices)
            elif event.key in (pygame.K_UP, pygame.K_w):
                if self.current.choices:
                    self.choice_index = (self.choice_index - 1) % len(self.current.choices)

    def _confirm(self):
        if self.current and self.current.choices:
            _, nxt = self.current.choices[self.choice_index]
            if nxt is None:
                self.active = False
            else:
                self._go_to(nxt)
        else:
            self.active = False

    def draw(self):
        if not self.active or not self.current:
            return
        panel = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        panel.fill((0, 0, 0, 200))
        self.screen.blit(panel, self.rect.topleft)
        pygame.draw.rect(self.screen, (240, 240, 240), self.rect, 3, border_radius=8)

        x = self.rect.x + 16
        y = self.rect.y + 12
        if self.current.speaker:
            name = self.font.render(self.current.speaker, True, (255, 220, 90))
            self.screen.blit(name, (x, y))
            y += name.get_height() + 4
        for line in self.lines:
            text = self.font.render(line, True, (240, 240, 240))
            self.screen.blit(text, (x, y))
            y += text.get_height() + 2

        for index, (label, _) in enumerate(self.current.choices):
            color = (255, 255, 120) if index == self.choice_index else (200, 200, 200)
            text = self.small.render(("> " if index == self.choice_index else "  ") + label,
                                     True, color)
            self.screen.blit(text, (x + 20, y + index * (self.small.get_height() + 2)))
```

## Juego de ejemplo — código completo

**`adventure/__init__.py`**

```python
# adventure/__init__.py
"""Aventura gráfica (clases 21-23) del curso de videojuegos 2027."""
```

**`adventure/game.py`**

```python
# adventure/game.py
"""
La Llave del Destino — aventura gráfica (clases 21-23).

Enfoque de ESCENAS del motor: 'menu' -> 'juego' (habitaciones) -> 'final'.

La escena 'juego' usa las piezas de aventura del motor:
hotspots, inventario, cursor propio y diálogos con opciones.
"""

import os

from engine.game_loop import Game
from engine.asset_manager import AssetManager
from engine.audio import AudioManager
from engine.shared_assets import sfx_path, music_path

from adventure.scenes.menu_scene import MenuScene
from adventure.scenes.juego_scene import JuegoScene
from adventure.scenes.final_scene import FinalScene


class AdventureGame(Game):
    def __init__(self):
        super().__init__(1024, 640, "La Llave del Destino", 60)

        self.game_dir = os.path.dirname(__file__)
        self.assets_dir = os.path.join(self.game_dir, "assets")

        self.assets = AssetManager()
        self.audio = AudioManager()

        self.load_assets()

        # Registramos las escenas por CLASE; el motor las instancia al entrar.
        self.add_scene("menu", MenuScene)
        self.add_scene("juego", JuegoScene)
        self.add_scene("final", FinalScene)
        self.change_scene("menu")

    # ------------------------------------------------------------------ #
    def load_assets(self):
        """Carga fondos, objetos y audio. Si falta algo, se avisa y se sigue."""
        imagenes = {
            "sala": os.path.join(self.assets_dir, "fondos", "sala.png"),
            "biblioteca": os.path.join(self.assets_dir, "fondos", "biblioteca.png"),
            "bodega": os.path.join(self.assets_dir, "fondos", "bodega.png"),
            "llave": os.path.join(self.assets_dir, "objetos", "llave.png"),
            "pocion": os.path.join(self.assets_dir, "objetos", "pocion.png"),
            "puerta": os.path.join(self.assets_dir, "objetos", "puerta.png"),
            "npc": os.path.join(self.assets_dir, "objetos", "npc.png"),
            "titulo": os.path.join(self.assets_dir, "objetos", "titulo.png"),
        }
        for nombre, ruta in imagenes.items():
            try:
                self.assets.load_image(nombre, ruta)
            except Exception as e:  # noqa: BLE001
                print(f"Aviso: no se pudo cargar la imagen '{nombre}': {e}")

        # Sonidos y música compartidos (si no existen, el audio lo ignora).
        for nombre in ("click", "coin", "type", "correct", "wrong"):
            self.audio.load_sound(nombre, sfx_path(nombre))
        self.audio.load_music(music_path("adventure"))
```

**`adventure/generar_assets.py`**

```python
# adventure/generar_assets.py
"""
Genera los gráficos de la aventura gráfica "La Llave del Destino" (clases 21-23).

Dibuja con Pillow (a través de herramientas.genlib):
  - 3 fondos de habitación de 1024x640 (sala, biblioteca y bodega).
  - Objetos: llave, poción y puerta.
  - Un personaje/NPC (el anciano de la sala).
  - El título del juego para el menú.

Ejecutar UNA vez:

    python adventure/generar_assets.py
"""

import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

from herramientas import genlib as g  # noqa: E402

W, H = 1024, 640
OUT_FONDOS = os.path.join(HERE, "assets", "fondos")
OUT_OBJETOS = os.path.join(HERE, "assets", "objetos")

NEGRO = (0, 0, 0, 255)


# --------------------------------------------------------------------------- #
#  Fondos de habitación
# --------------------------------------------------------------------------- #
def make_sala(w=W, h=H):
    """Sala principal cálida: chimenea, cuadro, ventana con luna y alfombra."""
    img = g.vgrad(w, h, (104, 70, 48), (52, 34, 24))
    d = g.ImageDraw.Draw(img)
    horizon = int(h * 0.72)

    # Panel de madera (zócalo alto)
    d.rectangle([0, int(h * 0.52), w, horizon], fill=(66, 44, 30, 255))
    for x in range(0, w, 118):
        d.line([(x, int(h * 0.52)), (x, horizon)], fill=(48, 30, 20, 255), width=3)

    # Suelo con tablas en perspectiva
    d.rectangle([0, horizon, w, h], fill=(80, 54, 36, 255))
    for i in range(-7, 8):
        d.line([(w // 2 + i * 62, horizon), (w // 2 + i * 210, h)],
               fill=(62, 40, 26, 255), width=2)
    for j in range(1, 5):
        yy = horizon + int((h - horizon) * (j / 5.0) ** 1.6)
        d.line([(0, yy), (w, yy)], fill=(58, 38, 25, 255), width=2)

    # Alfombra
    d.ellipse([330, 470, 730, 618], fill=(128, 52, 52, 255),
              outline=(86, 32, 32, 255), width=5)
    d.ellipse([380, 495, 680, 600], outline=(190, 150, 90, 255), width=4)

    # Chimenea con fuego
    d.rectangle([52, 250, 300, horizon + 12], fill=(98, 76, 62, 255),
                outline=(44, 30, 22, 255), width=3)
    d.rectangle([96, 322, 256, horizon + 12], fill=(26, 17, 13, 255))
    for i, (col, rad) in enumerate([((255, 120, 30, 230), 0.55),
                                    ((255, 190, 60, 230), 0.34),
                                    ((255, 240, 160, 220), 0.16)]):
        cx, cy = 176, 430 + i * 12
        d.ellipse([cx - 70 * rad, cy - 40 * rad, cx + 70 * rad, cy + 40 * rad],
                  fill=col)
    d.rectangle([40, 238, 312, 262], fill=(122, 94, 72, 255),
                outline=(44, 30, 22, 255), width=3)

    # Cuadro
    d.rectangle([636, 120, 848, 292], fill=(74, 52, 96, 255),
                outline=(186, 154, 92, 255), width=9)
    d.ellipse([672, 156, 812, 256], fill=(156, 108, 60, 255))
    d.polygon([(654, 284), (742, 176), (830, 284)], fill=(90, 122, 92, 255))

    # Ventana con luna
    d.rectangle([368, 96, 556, 286], fill=(28, 38, 78, 255),
                outline=(92, 62, 40, 255), width=11)
    d.line([(462, 100), (462, 282)], fill=(92, 62, 40, 255), width=8)
    d.line([(372, 190), (552, 190)], fill=(92, 62, 40, 255), width=8)
    d.ellipse([416, 122, 470, 176], fill=(240, 240, 210, 255))
    d.ellipse([404, 118, 452, 164], fill=(28, 38, 78, 255))
    for sx, sy in [(500, 140), (520, 220), (400, 240), (440, 250)]:
        d.ellipse([sx, sy, sx + 3, sy + 3], fill=(230, 230, 255, 255))

    return g.add_glow(img, 1, 0.15)


def make_biblioteca(w=W, h=H):
    """Biblioteca fría con estanterías llenas de libros y una mesa central."""
    img = g.vgrad(w, h, (46, 50, 76), (26, 28, 46))
    d = g.ImageDraw.Draw(img)
    horizon = int(h * 0.74)

    # Suelo
    d.rectangle([0, horizon, w, h], fill=(56, 44, 36, 255))
    for j in range(1, 5):
        yy = horizon + int((h - horizon) * (j / 5.0) ** 1.5)
        d.line([(0, yy), (w, yy)], fill=(42, 32, 26, 255), width=2)

    # Estanterías (dos a los lados)
    for sx in (30, 604, 830):
        d.rectangle([sx, 70, sx + 168, horizon], fill=(74, 56, 40, 255),
                    outline=(40, 28, 20, 255), width=4)
        for shelf in range(4):
            top = 92 + shelf * 92
            d.line([(sx + 4, top + 78), (sx + 164, top + 78)],
                   fill=(40, 28, 20, 255), width=5)
            bx = sx + 10
            while bx < sx + 154:
                bw = random.randint(9, 18)
                bh = random.randint(44, 68)
                color = random.choice([
                    (170, 60, 50), (60, 110, 170), (70, 140, 80),
                    (170, 140, 60), (120, 70, 150), (60, 140, 150),
                ])
                d.rectangle([bx, top + 78 - bh, bx + bw, top + 78],
                            fill=color + (255,), outline=(22, 16, 12, 255))
                bx += bw + 3

    # Mesa central
    d.rectangle([420, 452, 720, 486], fill=(96, 62, 36, 255),
                outline=(50, 32, 18, 255), width=4)
    d.rectangle([446, 486, 470, 574], fill=(78, 50, 30, 255), outline=NEGRO, width=3)
    d.rectangle([670, 486, 694, 574], fill=(78, 50, 30, 255), outline=NEGRO, width=3)
    # Libro abierto sobre la mesa
    d.polygon([(520, 452), (568, 442), (568, 470), (520, 480)],
              fill=(232, 226, 208, 255), outline=(80, 60, 40, 255))
    d.polygon([(568, 442), (616, 452), (616, 480), (568, 470)],
              fill=(214, 206, 188, 255), outline=(80, 60, 40, 255))

    # Candelabro con luz cálida
    for cx in (300, 760):
        d.rectangle([cx - 5, 400, cx + 5, 470], fill=(200, 190, 170, 255))
        d.ellipse([cx - 12, 372, cx + 12, 412], fill=(255, 220, 120, 255))
        d.ellipse([cx - 7, 380, cx + 7, 404], fill=(255, 250, 210, 255))

    return g.add_glow(img, 2, 0.2)


def make_bodega(w=W, h=H):
    """Bodega de piedra con arco de la puerta y barriles."""
    img = g.vgrad(w, h, (60, 60, 70), (30, 30, 36))
    d = g.ImageDraw.Draw(img)

    # Muro de piedra (bloques)
    bh, bw = 58, 128
    for row in range(0, int(h * 0.76) // bh + 1):
        offset = (row % 2) * (bw // 2)
        for col in range(-1, w // bw + 1):
            x = col * bw + offset
            y = row * bh
            shade = random.randint(-12, 12)
            col_rgb = tuple(max(0, min(255, c + shade)) for c in (74, 74, 84))
            d.rectangle([x + 2, y + 2, x + bw - 2, y + bh - 2],
                        fill=col_rgb + (255,), outline=(34, 34, 40, 255), width=3)

    # Suelo de tierra
    horizon = int(h * 0.78)
    d.rectangle([0, horizon, w, h], fill=(58, 50, 42, 255))

    # Hueco/marco de la puerta
    d.rectangle([396, 196, 644, 560], fill=(20, 16, 14, 255))
    d.rectangle([382, 182, 658, 200], fill=(96, 92, 100, 255),
                outline=(40, 38, 44, 255), width=3)
    for px in (386, 650):
        d.rectangle([px, 182, px + 12, 560], fill=(84, 80, 90, 255),
                    outline=(40, 38, 44, 255), width=2)

    # Barriles
    for bx, scale in ((120, 1.0), (238, 0.82)):
        bw2, bh2 = int(72 * scale), int(120 * scale)
        x0, y0 = bx, horizon - bh2 + 30
        d.ellipse([x0, y0, x0 + bw2, y0 + 26], fill=(120, 84, 44, 255),
                  outline=(60, 40, 20, 255), width=3)
        d.rectangle([x0, y0 + 12, x0 + bw2, y0 + bh2], fill=(104, 72, 38, 255),
                    outline=(60, 40, 20, 255), width=3)
        d.ellipse([x0, y0 + bh2 - 14, x0 + bw2, y0 + bh2 + 12],
                  fill=(88, 60, 32, 255), outline=(60, 40, 20, 255), width=3)
        for hy in (y0 + 40, y0 + bh2 - 30):
            d.line([(x0, hy), (x0 + bw2, hy)], fill=(70, 70, 78, 255), width=4)

    return g.add_glow(img, 1, 0.12)


# --------------------------------------------------------------------------- #
#  Objetos
# --------------------------------------------------------------------------- #
def make_llave(size=96):
    """Llave dorada brillante."""
    img = g.new(size, size)
    d = g.ImageDraw.Draw(img)
    oro = (236, 196, 70, 255)
    oro_s = (150, 108, 20, 255)
    # Anillo del mango
    d.ellipse([16, 26, 62, 72], outline=oro, width=12)
    d.ellipse([26, 36, 52, 62], outline=oro_s, width=3)
    # Caña
    d.rectangle([54, 44, 88, 56], fill=oro, outline=oro_s, width=3)
    # Dientes
    d.rectangle([76, 56, 88, 72], fill=oro, outline=oro_s, width=3)
    d.rectangle([64, 56, 74, 66], fill=oro, outline=oro_s, width=2)
    # Brillo
    d.line([(58, 48), (84, 48)], fill=(255, 250, 210, 255), width=2)
    return g.add_glow(img, 4, 0.55)


def make_pocion(w=72, h=92):
    """Poción azul en un frasco con corcho."""
    img = g.new(w, h)
    d = g.ImageDraw.Draw(img)
    cx = w // 2
    # Frasco
    d.polygon([(cx - 12, 20), (cx + 12, 20), (cx + 26, 78), (cx - 26, 78)],
              fill=(200, 225, 235, 220), outline=(70, 90, 110, 255))
    d.ellipse([cx - 26, 60, cx + 26, 90], fill=(200, 225, 235, 220),
              outline=(70, 90, 110, 255), width=3)
    # Líquido
    d.polygon([(cx - 17, 44), (cx + 17, 44), (cx + 24, 74), (cx - 24, 74)],
              fill=(70, 140, 240, 255))
    d.ellipse([cx - 24, 60, cx + 24, 88], fill=(70, 140, 240, 255))
    # Brillo del líquido
    d.line([(cx - 10, 50), (cx - 6, 72)], fill=(170, 220, 255, 200), width=3)
    # Cuello y corcho
    d.rectangle([cx - 8, 12, cx + 8, 24], fill=(190, 210, 220, 230),
                outline=(70, 90, 110, 255), width=2)
    d.rectangle([cx - 11, 2, cx + 11, 14], fill=(150, 106, 60, 255),
                outline=(80, 54, 26, 255), width=2)
    return g.add_glow(img, 3, 0.3)


def make_puerta(w=240, h=350):
    """Puerta de madera cerrada con refuerzos de hierro y pomo."""
    img = g.new(w, h)
    d = g.ImageDraw.Draw(img)
    d.rectangle([0, 0, w - 1, h - 1], fill=(102, 68, 38, 255),
                outline=(52, 34, 18, 255), width=7)
    # Tablones verticales
    for x in range(8, w - 8, 38):
        d.line([(x, 8), (x, h - 8)], fill=(78, 50, 28, 255), width=3)
    # Refuerzos de hierro
    for y in (24, h - 62):
        d.rectangle([12, y, w - 12, y + 26], fill=(74, 74, 84, 255),
                    outline=(32, 32, 38, 255), width=3)
        for rx in range(26, w - 20, 46):
            d.ellipse([rx, y + 8, rx + 8, y + 16], fill=(40, 40, 46, 255))
    # Bisagras
    d.rectangle([-4, 60, 34, 84], fill=(74, 74, 84, 255), outline=(30, 30, 36, 255), width=3)
    d.rectangle([-4, h - 96, 34, h - 72], fill=(74, 74, 84, 255), outline=(30, 30, 36, 255), width=3)
    # Pomo dorado
    d.ellipse([w - 58, h // 2 - 14, w - 24, h // 2 + 14],
              fill=(236, 196, 70, 255), outline=(130, 96, 24, 255), width=4)
    return img


def make_npc(w=140, h=250):
    """El anciano de la sala: humanoides con sombrero y barba."""
    def accessory(d, cx, head_cy, head_r, ww, hh):
        d.polygon([(cx - head_r - 6, head_cy - head_r + 4),
                   (cx + head_r + 6, head_cy - head_r + 4),
                   (cx, head_cy - head_r - 30)],
                  fill=(62, 42, 92, 255), outline=(24, 16, 36, 255))
        d.ellipse([cx - head_r - 10, head_cy - head_r - 4,
                   cx + head_r + 10, head_cy - head_r + 12],
                  fill=(62, 42, 92, 255), outline=(24, 16, 36, 255), width=3)
        d.arc([cx - head_r + 2, head_cy, cx + head_r - 2, head_cy + head_r + 12],
              0, 180, fill=(214, 214, 214, 255), width=8)

    return g.make_humanoid(
        w, h,
        skin=(236, 202, 168, 255),
        shirt=(118, 62, 140, 255),
        pants=(54, 44, 62, 255),
        hair=(216, 216, 216, 255),
        pose="idle",
        accessory=accessory,
    )


# --------------------------------------------------------------------------- #
def main():
    g.ensure_dir(OUT_FONDOS)
    g.ensure_dir(OUT_OBJETOS)

    g.save_png(make_sala(), os.path.join(OUT_FONDOS, "sala.png"))
    g.save_png(make_biblioteca(), os.path.join(OUT_FONDOS, "biblioteca.png"))
    g.save_png(make_bodega(), os.path.join(OUT_FONDOS, "bodega.png"))

    g.save_png(make_llave(), os.path.join(OUT_OBJETOS, "llave.png"))
    g.save_png(make_pocion(), os.path.join(OUT_OBJETOS, "pocion.png"))
    g.save_png(make_puerta(), os.path.join(OUT_OBJETOS, "puerta.png"))
    g.save_png(make_npc(), os.path.join(OUT_OBJETOS, "npc.png"))

    g.save_png(g.text_image("La Llave del Destino", 68, (255, 222, 120, 255)),
               os.path.join(OUT_OBJETOS, "titulo.png"))

    print("Assets de adventure generados en", OUT_FONDOS, "y", OUT_OBJETOS)


if __name__ == "__main__":
    main()
```

**`adventure/scenes/__init__.py`**

```python
# adventure/scenes/__init__.py
```

**`adventure/scenes/menu_scene.py`**

```python
# adventure/scenes/menu_scene.py
import pygame

from engine.ui import Scene, Button
from engine.ui_elements import Label, Panel


class MenuScene(Scene):
    """Menú principal: usa Button y elementos de ui_elements (Label/Panel)."""

    def __init__(self, game):
        super().__init__(game)
        self.screen = game.screen
        w = self.screen.get_width()

        self.title = Label("LA LLAVE DEL DESTINO", (w // 2, 150),
                           size=64, color=(255, 222, 120), align="center")
        self.subtitle = Label("Aventura grafica  ·  Clases 21-23", (w // 2, 214),
                              size=28, color=(206, 206, 236), align="center")
        self.hint = Label("Clic en objetos y flechas  ·  Flechas/Enter en los dialogos  ·  ESC salir",
                          (w // 2, 566), size=22, color=(168, 178, 208),
                          align="center")
        self.panel = Panel((w // 2 - 160, 292, 320, 188),
                           color=(16, 16, 30, 190), border=(120, 120, 160))
        self.play_button = Button(w // 2 - 130, 318, 260, 60, "Jugar",
                                  self.start_game, font_size=42)
        self.quit_button = Button(w // 2 - 130, 398, 260, 60, "Salir",
                                  self.quit_game, font_size=42)

    # ------------------------------------------------------------------ #
    def on_enter(self):
        self.game.audio.play_music(loops=-1, volume=0.4)

    def start_game(self):
        self.game.audio.play_sound("click")
        self.game.change_scene("juego")

    def quit_game(self):
        self.game.audio.play_sound("click")
        self.game.running = False

    # ------------------------------------------------------------------ #
    def handle_events(self, events):
        for event in events:
            self.play_button.handle_event(event)
            self.quit_button.handle_event(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.running = False
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    self.start_game()

    def update(self):
        pass

    # ------------------------------------------------------------------ #
    def draw(self, surface):
        # Fondo: la sala atenuada si esta disponible.
        if "sala" in self.game.assets.images:
            surface.blit(self.game.assets.get_image("sala"), (0, 0))
            overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
            overlay.fill((6, 6, 18, 175))
            surface.blit(overlay, (0, 0))
        else:
            surface.fill((16, 14, 32))

        if "titulo" in self.game.assets.images:
            titulo = self.game.assets.get_image("titulo")
            surface.blit(titulo, titulo.get_rect(centerx=surface.get_width() // 2,
                                                 centery=150))
        else:
            self.title.draw(surface)

        self.subtitle.draw(surface)
        self.panel.draw(surface)
        self.play_button.draw(surface)
        self.quit_button.draw(surface)
        self.hint.draw(surface)
```

**`adventure/scenes/juego_scene.py`**

```python
# adventure/scenes/juego_scene.py
"""
Escena de juego de la aventura grafica.

Tres habitaciones conectadas (sala -> biblioteca -> bodega) con:
  - hotspots clicables (NPC, llave, pocion y puerta),
  - salidas de flecha (este / oeste / norte / sur),
  - inventario visible,
  - cursor propio que cambia sobre los hotspots,
  - dialogos con opciones (DialogueBox).

Objetivo: coger la LLAVE en la biblioteca y abrir la PUERTA de la bodega.
"""

import pygame

from engine.ui import Scene
from engine.hotspot import Hotspot
from engine.inventory import Inventory, Item
from engine.cursor import Cursor
from engine.dialogue import DialogueBox, DialogueNode
from engine.particle import ParticleSystem
from engine.ui_elements import Label, Panel

INVENTARIO_ORIGEN = (18, 122)
SLOT = 56


class JuegoScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.screen = game.screen
        self.ancho = game.screen.get_width()
        self.alto = game.screen.get_height()

        # Piezas de aventura del motor.
        self.inventory = Inventory(capacity=6)
        self.cursor = Cursor()
        self.dialogue = DialogueBox(game.screen)
        self.particles = ParticleSystem()

        # Estado de la partida.
        self.recogidos = set()       # objetos ya cogidos (llave, pocion)
        self.hotspots = []           # zonas clicables de la habitacion actual
        self.objetos = []            # (imagen, rect) a dibujar encima del fondo
        self.salidas = []            # (Hotspot, direccion)
        self.hovered = None
        self.mensaje = ""
        self.mensaje_t = 0.0
        self._pending_final = False

        self.font = pygame.font.Font(None, 32)
        self.label_hab = Label("", (self.ancho // 2, 26), size=36,
                               color=(255, 236, 180), align="center")
        self.label_inv = Label("Inventario", (14, 98), size=24,
                               color=(226, 220, 190))

        self._cargar_habitacion("sala")

    # ================================================================== #
    #  Construccion de habitaciones
    # ================================================================== #
    def _add_hotspot(self, name, rect, callback):
        hs = Hotspot(rect, name=name, callback=callback)
        self.hotspots.append(hs)
        return hs

    def _add_objeto(self, nombre, rect):
        img = self.game.assets.get_image(nombre)
        if img.get_size() != rect.size:
            img = pygame.transform.smoothscale(img, rect.size)
        self.objetos.append((img, rect))

    def _add_salida(self, direccion, rect, destino):
        hs = Hotspot(rect, name="salida_" + direccion,
                     callback=lambda _hs: self._ir(destino))
        hs.direccion = direccion
        self.salidas.append((hs, direccion))
        self.hotspots.append(hs)

    def _cargar_habitacion(self, nombre):
        self.habitacion = nombre
        self.hotspots = []
        self.objetos = []
        self.salidas = []
        self.hovered = None
        self._pending_final = False

        self.fondo = self.game.assets.get_image(nombre)

        if nombre == "sala":
            self.label_hab.text = "Sala principal"
            self._add_objeto("npc", pygame.Rect(448, 300, 140, 250))
            self._add_hotspot("npc", pygame.Rect(428, 292, 180, 280),
                              self._hablar_npc)
            self._add_salida("este", pygame.Rect(938, 236, 86, 176), "biblioteca")

        elif nombre == "biblioteca":
            self.label_hab.text = "Biblioteca"
            self._add_salida("oeste", pygame.Rect(0, 236, 86, 176), "sala")
            self._add_salida("norte", pygame.Rect(452, 0, 120, 84), "bodega")
            if "llave" not in self.recogidos:
                r = pygame.Rect(624, 424, 96, 96)
                self._add_objeto("llave", r)
                self._add_hotspot("llave", r.inflate(28, 28), self._coger_llave)

        elif nombre == "bodega":
            self.label_hab.text = "Bodega"
            self._add_salida("sur", pygame.Rect(452, 556, 120, 84), "biblioteca")
            rp = pygame.Rect(400, 205, 240, 350)
            self._add_objeto("puerta", rp)
            self._add_hotspot("puerta", rp, self._usar_puerta)
            if "pocion" not in self.recogidos:
                r2 = pygame.Rect(150, 430, 72, 92)
                self._add_objeto("pocion", r2)
                self._add_hotspot("pocion", r2.inflate(30, 24), self._coger_pocion)

    # ================================================================== #
    #  Acciones de los hotspots
    # ================================================================== #
    def _ir(self, destino):
        self.game.audio.play_sound("click")
        self._cargar_habitacion(destino)

    def _coger_llave(self, _hs):
        if self.inventory.add(Item("llave", self.game.assets.get_image("llave"),
                                   "Abre la puerta de la bodega")):
            self.recogidos.add("llave")
            self.game.audio.play_sound("coin")
            self._set_mensaje("Has cogido la LLAVE dorada.")
            self.particles.emit(672, 470, count=28, color=(255, 212, 70),
                                speed=(60, 210), life=(0.4, 0.9))
            self._cargar_habitacion("biblioteca")

    def _coger_pocion(self, _hs):
        if self.inventory.add(Item("pocion", self.game.assets.get_image("pocion"),
                                   "Una pocion azul que reanima")):
            self.recogidos.add("pocion")
            self.game.audio.play_sound("coin")
            self._set_mensaje("Has cogido una POCION azul.")
            self.particles.emit(186, 470, count=24, color=(90, 170, 255),
                                speed=(50, 180), life=(0.4, 0.9))
            self._cargar_habitacion("bodega")

    def _usar_puerta(self, _hs):
        if self.inventory.has("llave"):
            self.game.audio.play_sound("correct")
            nodos = {"start": DialogueNode(
                "Giras la llave dorada... CLIC. La puerta se abre hacia la salida.",
                "Puerta", choices=[("Salir", None)],
                action=lambda _n: self.game.audio.play_sound("type"))}
            self._pending_final = True
        else:
            self.game.audio.play_sound("wrong")
            nodos = {"start": DialogueNode(
                "La puerta esta cerrada con llave. Tiene que haber una por aqui...",
                "Puerta", choices=[("Vale", None)],
                action=lambda _n: self.game.audio.play_sound("type"))}
        self.dialogue.start(nodos, "start")

    def _hablar_npc(self, _hs):
        self.game.audio.play_sound("click")
        nodos = {
            "start": DialogueNode(
                "Buenas, viajero. Que se te ofrece?", "Anciano",
                choices=[("Donde hay una llave?", "llave"),
                         ("Como salgo de aqui?", "salir"),
                         ("Nada, gracias.", None)],
                action=lambda _n: self.game.audio.play_sound("type")),
            "llave": DialogueNode(
                "Una llave dorada duerme en la biblioteca, al ESTE.", "Anciano",
                choices=[("Gracias.", "gracias"), ("Y la salida?", "salir")],
                action=lambda _n: self.game.audio.play_sound("type")),
            "salir": DialogueNode(
                "Al este la biblioteca; al norte de ella, la bodega. Alli esta la puerta.",
                "Anciano", choices=[("Entendido.", None)],
                action=lambda _n: self.game.audio.play_sound("type")),
            "gracias": DialogueNode(
                "Buena suerte, forastero.", "Anciano",
                choices=[("Adios.", None)],
                action=lambda _n: self.game.audio.play_sound("type")),
        }
        self.dialogue.start(nodos, "start")

    # ================================================================== #
    def _set_mensaje(self, texto):
        self.mensaje = texto
        self.mensaje_t = 3.0

    # ================================================================== #
    def _dialogue_click(self, pos):
        """Selecciona una opcion del dialogo con el raton (o avanza)."""
        d = self.dialogue
        if not d.current:
            return
        x = d.rect.x + 16
        y = d.rect.y + 12
        if d.current.speaker:
            y += d.font.get_height() + 4
        y += len(d.lines) * (d.font.get_height() + 2)
        alto = d.small.get_height() + 2
        for i, _choice in enumerate(d.current.choices):
            rect = pygame.Rect(x + 20, y + i * alto, d.width - 40, alto)
            if rect.collidepoint(pos):
                d.choice_index = i
                break
        d._confirm()

    def handle_events(self, events):
        for event in events:
            # Mientras hay dialogo, todo va al cuadro de dialogo.
            if self.dialogue.active:
                self.dialogue.handle_event(event)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self._dialogue_click(event.pos)
                continue

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.game.change_scene("menu")
                return

            # Seleccionar objeto del inventario (no dispara hotspots).
            if self.inventory.handle_event(event, INVENTARIO_ORIGEN, SLOT) is not None:
                self.game.audio.play_sound("click")
                continue

            for hs in self.hotspots:
                if hs.handle_event(event):
                    break

    # ================================================================== #
    def update(self):
        dt = 1.0 / max(1, self.game.fps)
        self.particles.update(dt)

        if self.mensaje_t > 0:
            self.mensaje_t = max(0.0, self.mensaje_t - dt)

        # Hotspot bajo el cursor (para cambiar el puntero).
        self.hovered = None
        if not self.dialogue.active:
            pos = pygame.mouse.get_pos()
            for hs in self.hotspots:
                if hs.contains(pos):
                    self.hovered = hs
                    break

        # Al cerrar el dialogo de la puerta abierta, pasamos a la escena final.
        if self._pending_final and not self.dialogue.active:
            self._pending_final = False
            self.game.change_scene("final")

    # ================================================================== #
    def _draw_arrow(self, surface, rect, direccion, hovered):
        color = (255, 236, 120) if hovered else (226, 196, 90)
        cx, cy = rect.center
        s = 26
        if direccion == "este":
            pts = [(cx - s, cy - s), (cx + s, cy), (cx - s, cy + s)]
        elif direccion == "oeste":
            pts = [(cx + s, cy - s), (cx - s, cy), (cx + s, cy + s)]
        elif direccion == "norte":
            pts = [(cx - s, cy + s), (cx, cy - s), (cx + s, cy + s)]
        else:  # sur
            pts = [(cx - s, cy - s), (cx, cy + s), (cx + s, cy - s)]
        pygame.draw.polygon(surface, color, pts)
        pygame.draw.polygon(surface, (52, 34, 12), pts, 3)

    def draw(self, surface):
        surface.blit(self.fondo, (0, 0))

        for img, rect in self.objetos:
            surface.blit(img, rect)

        for hs, direccion in self.salidas:
            self._draw_arrow(surface, hs.rect, direccion, self.hovered is hs)

        self.particles.draw(surface)

        # HUD: nombre de habitacion + inventario.
        self.label_hab.draw(surface)
        self.label_inv.draw(surface)
        self.inventory.draw(surface, INVENTARIO_ORIGEN, SLOT)

        # Aviso temporal.
        if self.mensaje_t > 0:
            panel = Panel((self.ancho // 2 - 270, 66, 540, 46),
                          color=(0, 0, 0, 170), border=(230, 210, 140))
            panel.draw(surface)
            texto = self.font.render(self.mensaje, True, (255, 240, 200))
            surface.blit(texto, texto.get_rect(center=(self.ancho // 2, 66 + 23)))

        self.dialogue.draw()
        self.cursor.draw(surface, hovered=self.hovered is not None)
```

**`adventure/scenes/final_scene.py`**

```python
# adventure/scenes/final_scene.py
import random

import pygame

from engine.ui import Scene, Button
from engine.particle import ParticleSystem


class FinalScene(Scene):
    """Pantalla de victoria: la puerta se abrio y escapa de la bodega."""

    def __init__(self, game):
        super().__init__(game)
        self.screen = game.screen
        self.ancho = game.screen.get_width()
        self.alto = game.screen.get_height()

        self.particles = ParticleSystem()
        self.t = 0.0
        self.font_big = pygame.font.Font(None, 108)
        self.font = pygame.font.Font(None, 38)
        self.font_small = pygame.font.Font(None, 26)

        self.menu_button = Button(self.ancho // 2 - 150, 452, 300, 62,
                                  "Volver al menu", self._volver, font_size=36)

    # ------------------------------------------------------------------ #
    def on_enter(self):
        self.game.audio.play_sound("cheer")
        for _ in range(3):
            self._estallido()

    def _volver(self):
        self.game.audio.play_sound("click")
        self.game.change_scene("menu")

    def _estallido(self):
        color = random.choice([(255, 210, 90), (120, 220, 255),
                               (255, 120, 160), (150, 255, 150)])
        self.particles.emit(random.randint(120, self.ancho - 120),
                            random.randint(40, 160), count=18, color=color,
                            speed=(50, 200), life=(0.8, 1.8), gravity=140)

    # ------------------------------------------------------------------ #
    def handle_events(self, events):
        for event in events:
            self.menu_button.handle_event(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self._volver()
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    self._volver()

    def update(self):
        dt = 1.0 / max(1, self.game.fps)
        self.t += dt
        if random.random() < 0.3:
            self._estallido()
        self.particles.update(dt)

    # ------------------------------------------------------------------ #
    def draw(self, surface):
        surface.fill((16, 14, 34))

        # Halo radial detras del titulo.
        halo = pygame.Surface((520, 260), pygame.SRCALPHA)
        for i in range(10, 0, -1):
            alpha = int(8 * i)
            pygame.draw.ellipse(halo, (255, 210, 110, alpha),
                                halo.get_rect().inflate(-i * 24, -i * 12))
        surface.blit(halo, halo.get_rect(center=(self.ancho // 2, 240)))

        self.particles.draw(surface)

        titulo = self.font_big.render("VICTORIA!", True, (255, 224, 110))
        surface.blit(titulo, titulo.get_rect(center=(self.ancho // 2, 236)))

        linea1 = self.font.render("Abriste la puerta y escapaste de la bodega.",
                                  True, (238, 238, 244))
        surface.blit(linea1, linea1.get_rect(center=(self.ancho // 2, 330)))

        linea2 = self.font_small.render(
            "Has completado la aventura: llave -> puerta -> libertad.",
            True, (186, 190, 220))
        surface.blit(linea2, linea2.get_rect(center=(self.ancho // 2, 382)))

        self.menu_button.draw(surface)
```

**`adventure/main.py`**

```python
# adventure/main.py
"""
Ejecutar desde la carpeta 2027 con:
    python -m adventure.main
o directamente:
    python adventure/main.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from adventure.game import AdventureGame


def main():
    AdventureGame().run()


if __name__ == "__main__":
    main()
```

## Controles

click en hotspots; flechas/`WASD` + `ENTER` en los diálogos.

## Cómo ejecutar

Desde la carpeta `2027/`:

```bash
python -m adventure.main
```
