# Clase 26 — Fútbol con roles, atributos y progresión (RPG)

Objetivo: cerrar el curso con un juego que combina **escenas**,
**atributos** y **progresión**. Reutiliza `engine/ui_elements.py`
(clase 24) y las escenas (clase 8).

El ejemplo es `soccer_rpg/` (enfoque Game + Escenas): eliges rol
(Delantero/Mediocampista/Defensor: fija ataque/defensa/energía),
juegas una secuencia de jugadas y ves un resumen con nivel y XP.

## Juego de ejemplo — código completo

**`soccer_rpg/__init__.py`**

```python
# soccer_rpg/__init__.py
```

**`soccer_rpg/game.py`**

```python
# soccer_rpg/game.py
"""
SOCCER RPG — RPG de fútbol por escenas (clase 26).

Enfoque ESCENAS:
    'menu'      -> título y opciones
    'seleccion' -> elegir ROL (Delantero / Mediocampista / Defensor)
    'partido'   -> secuencia de "jugadas" con acciones ataque/pase/defensa
    'resumen'   -> estadísticas y nivel alcanzado

Clase principal: SoccerRpgGame
"""
import os

from engine.game_loop import Game
from engine.asset_manager import AssetManager
from engine.audio import AudioManager
from engine.shared_assets import sfx_path, music_path

from soccer_rpg.scenes.menu_scene import MenuScene
from soccer_rpg.scenes.seleccion_scene import SeleccionScene
from soccer_rpg.scenes.partido_scene import PartidoScene
from soccer_rpg.scenes.resumen_scene import ResumenScene
from soccer_rpg.roles import ROLES  # noqa: F401  (reexport por comodidad)


class SoccerRpgGame(Game):
    def __init__(self):
        super().__init__(900, 600, "Soccer RPG", 60)

        self.game_dir = os.path.dirname(os.path.abspath(__file__))
        self.assets_dir = os.path.join(self.game_dir, "assets", "sprites")

        self.assets = AssetManager()
        self.audio = AudioManager()
        self.load_assets()

        self.add_scene("menu", MenuScene)
        self.add_scene("seleccion", SeleccionScene)
        self.add_scene("partido", PartidoScene)
        self.add_scene("resumen", ResumenScene)
        self.change_scene("menu")

    def load_assets(self):
        imagenes = [
            "campo", "balon", "logo",
            "jugador_delantero", "jugador_mediocampista", "jugador_defensor",
            "jugador_delantero_kick",
            "icono_ataque", "icono_pase", "icono_defensa",
        ]
        for nombre in imagenes:
            try:
                self.assets.load_image(
                    nombre, os.path.join(self.assets_dir, f"{nombre}.png"))
            except Exception as e:  # pragma: no cover
                print(f"Aviso: no se pudo cargar '{nombre}.png': {e}")

        for sonido in ("kick", "whistle", "cheer", "correct", "wrong", "click"):
            self.audio.load_sound(sonido, sfx_path(sonido))
        self.audio.load_music(music_path("soccer"))
```

**`soccer_rpg/roles.py`**

```python
# soccer_rpg/roles.py
"""
Definición de los roles jugables y sus atributos (0-100).

Se separa de `game.py` para evitar importaciones circulares: las escenas
necesitan los roles, pero el juego importa las escenas.
"""

ROLES = {
    "Delantero": {
        "ataque": 88, "defensa": 46, "energia": 85,
        "desc": "Pura potencia ofensiva. Mucho gol, poca defensa.",
        "sprite": "jugador_delantero",
        "color": (225, 60, 60),
    },
    "Mediocampista": {
        "ataque": 66, "defensa": 66, "energia": 95,
        "desc": "Equilibrado. Mueve el equipo y decide las jugadas.",
        "sprite": "jugador_mediocampista",
        "color": (60, 110, 230),
    },
    "Defensor": {
        "ataque": 46, "defensa": 88, "energia": 100,
        "desc": "Muro atras. Corta ataques y aguanta toda la energia.",
        "sprite": "jugador_defensor",
        "color": (60, 180, 110),
    },
}
```

**`soccer_rpg/generar_assets.py`**

```python
"""
soccer_rpg/generar_assets.py

Genera los gráficos del RPG de fútbol (clase 26):
campo, balón, jugadores de distintos colores/roles e iconos de acción.
Ejecutar UNA vez:

    python soccer_rpg/generar_assets.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

from herramientas import genlib as g  # noqa: E402

OUT = os.path.join(HERE, "assets", "sprites")

W, H = 900, 600


def make_campo(w=W, h=H):
    """Campo horizontal con gradiente, líneas y áreas."""
    img = g.new(w, h)
    bg = g.vgrad(w, h, (34, 118, 60), (22, 84, 46))
    img = g.Image.alpha_composite(img, bg)
    d = g.ImageDraw.Draw(img)

    stripe = w // 10
    for i in range(11):
        if i % 2 == 0:
            d.rectangle([i * stripe, 0, i * stripe + stripe, h],
                        fill=(44, 140, 70, 70))

    m = 26
    d.rectangle([m, m, w - m, h - m], outline=(240, 240, 240, 210), width=4)
    d.line([(w // 2, m), (w // 2, h - m)], fill=(240, 240, 240, 210), width=4)
    r = 76
    d.ellipse([w // 2 - r, h // 2 - r, w // 2 + r, h // 2 + r],
              outline=(240, 240, 240, 210), width=4)
    d.ellipse([w // 2 - 6, h // 2 - 6, w // 2 + 6, h // 2 + 6],
              fill=(240, 240, 240, 210))
    # Áreas laterales
    aw, ah = 100, 300
    d.rectangle([m, h // 2 - ah // 2, m + aw, h // 2 + ah // 2],
                outline=(240, 240, 240, 210), width=4)
    d.rectangle([w - m - aw, h // 2 - ah // 2, w - m, h // 2 + ah // 2],
                outline=(240, 240, 240, 210), width=4)
    return img


def make_balon(r=16):
    img = g.make_ball((250, 250, 250, 255), r)
    d = g.ImageDraw.Draw(img)
    size = r * 2
    for fx, fy in [(0.5, 0.34), (0.32, 0.62), (0.68, 0.62)]:
        cx, cy = int(size * fx), int(size * fy)
        pr = max(2, r // 4)
        d.ellipse([cx - pr, cy - pr, cx + pr, cy + pr], fill=(30, 30, 30, 255))
    return img


def _icon(size, color, draw_fn):
    img = g.new(size, size)
    d = g.ImageDraw.Draw(img)
    d.rounded_rectangle([1, 1, size - 2, size - 2], radius=8,
                        fill=color, outline=(20, 20, 30, 255), width=2)
    draw_fn(d, size)
    return img


def icono_ataque(size=56):
    """Flecha hacia arriba-derecha (remate)."""
    color = (210, 70, 70, 255)

    def fn(d, s):
        c = s // 2
        d.polygon([(c, 10), (s - 12, c), (c + 8, c), (c + 8, s - 12),
                   (c - 8, s - 12), (c - 8, c), (12, c)], fill=(255, 235, 235, 255))
    return _icon(size, color, fn)


def icono_pase(size=56):
    """Dos flechas cruzadas (pase)."""
    color = (70, 120, 220, 255)

    def fn(d, s):
        d.line([(14, s - 16), (s - 16, 14)], fill=(235, 240, 255, 255), width=6)
        d.polygon([(s - 12, 8), (s - 8, s - 20), (s - 20, s - 12)],
                  fill=(235, 240, 255, 255))
    return _icon(size, color, fn)


def icono_defensa(size=56):
    """Escudo (defensa)."""
    color = (60, 170, 100, 255)

    def fn(d, s):
        c = s // 2
        d.polygon([(c, 10), (s - 12, 18), (s - 14, c + 6),
                   (c, s - 10), (14, c + 6), (12, 18)],
                  fill=(235, 255, 240, 255))
    return _icon(size, color, fn)


def main():
    g.ensure_dir(OUT)

    g.save_png(make_campo(), os.path.join(OUT, "campo.png"))
    g.save_png(make_balon(), os.path.join(OUT, "balon.png"))

    skin = (232, 194, 158, 255)
    delantero = dict(skin=skin, shirt=(225, 60, 60, 255),
                     pants=(60, 30, 30, 255), hair=(30, 20, 15, 255))
    medio = dict(skin=skin, shirt=(60, 110, 230, 255),
                 pants=(25, 40, 90, 255), hair=(20, 25, 35, 255))
    defensor = dict(skin=skin, shirt=(60, 180, 110, 255),
                    pants=(20, 70, 45, 255), hair=(35, 25, 15, 255))

    g.save_png(g.make_humanoid(80, 116, pose="idle", **delantero),
               os.path.join(OUT, "jugador_delantero.png"))
    g.save_png(g.make_humanoid(80, 116, pose="idle", **medio),
               os.path.join(OUT, "jugador_mediocampista.png"))
    g.save_png(g.make_humanoid(80, 116, pose="idle", **defensor),
               os.path.join(OUT, "jugador_defensor.png"))
    g.save_png(g.make_humanoid(80, 116, pose="kick", **delantero),
               os.path.join(OUT, "jugador_delantero_kick.png"))

    g.save_png(icono_ataque(), os.path.join(OUT, "icono_ataque.png"))
    g.save_png(icono_pase(), os.path.join(OUT, "icono_pase.png"))
    g.save_png(icono_defensa(), os.path.join(OUT, "icono_defensa.png"))

    g.save_png(g.text_image("SOCCER RPG", 56, (255, 240, 120, 255)),
               os.path.join(OUT, "logo.png"))

    print("Assets de soccer_rpg generados en", OUT)


if __name__ == "__main__":
    main()
```

**`soccer_rpg/scenes/__init__.py`**

```python
# soccer_rpg/scenes/__init__.py
```

**`soccer_rpg/scenes/menu_scene.py`**

```python
# soccer_rpg/scenes/menu_scene.py
import pygame

from engine.ui import Scene, Button


class MenuScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.font_hint = pygame.font.Font(None, 26)

        self.boton_jugar = Button(330, 350, 240, 56, "Jugar", self.jugar,
                                  color=(40, 90, 150), hover_color=(60, 120, 190))
        self.boton_salir = Button(330, 420, 240, 56, "Salir", self.salir)
        self.t = 0.0

    def on_enter(self):
        self.game.audio.play_music(volume=0.4)

    def jugar(self):
        self.game.audio.play_sound("click")
        self.game.audio.play_sound("whistle")
        self.game.change_scene("seleccion")

    def salir(self):
        self.game.audio.play_sound("click")
        self.game.running = False

    def handle_events(self, events):
        for event in events:
            self.boton_jugar.handle_event(event)
            self.boton_salir.handle_event(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.running = False
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    self.jugar()

    def update(self):
        self.t += 1.0 / self.game.fps

    def draw(self, surface):
        w = surface.get_width()
        try:
            surface.blit(self.game.assets.get_image("campo"), (0, 0))
        except Exception:
            surface.fill((25, 100, 55))

        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))
        surface.blit(overlay, (0, 0))

        import math
        try:
            logo = self.game.assets.get_image("logo")
            y = 120 + int(math.sin(self.t * 2) * 6)
            surface.blit(logo, logo.get_rect(centerx=w // 2, y=y))
        except Exception:
            pass

        self._mid(surface, "RPG de futbol por jugadas", 34, 230, (230, 240, 255))
        self._mid(surface, "Elegi tu rol y gana el partido", 26, 278,
                  (180, 220, 190))

        # Balón girando
        try:
            balon = self.game.assets.get_image("balon")
            rotated = pygame.transform.rotate(balon, self.t * 90 % 360)
            surface.blit(rotated, rotated.get_rect(center=(w // 2, 320)))
        except Exception:
            pass

        self.boton_jugar.draw(surface)
        self.boton_salir.draw(surface)

    def _mid(self, surface, texto, size, y, color):
        font = pygame.font.Font(None, size)
        img = font.render(texto, True, color)
        surface.blit(img, img.get_rect(centerx=surface.get_width() // 2, y=y))
```

**`soccer_rpg/scenes/seleccion_scene.py`**

```python
# soccer_rpg/scenes/seleccion_scene.py
"""
Escena de selección de ROL.
Cada rol fija los atributos ataque/defensa/energía del jugador.
"""
import pygame

from engine.ui import Scene, Button
from engine.ui_elements import Label, Panel, ProgressBar
from soccer_rpg.roles import ROLES

_ORDEN = ["Delantero", "Mediocampista", "Defensor"]


class SeleccionScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.font_titulo = pygame.font.Font(None, 60)
        self.font = pygame.font.Font(None, 30)
        self.font_chico = pygame.font.Font(None, 24)

        self.seleccionado = "Delantero"

        self.botones = {}
        x = 40
        for rol in _ORDEN:
            self.botones[rol] = Button(
                x, 470, 250, 56, rol, lambda r=rol: self.elegir(r),
                font_size=32, color=(45, 55, 85), hover_color=(70, 85, 130))
            x += 280

        self.barras = {
            "ataque": ProgressBar((620, 240, 220, 22), 100, 50, (220, 70, 70)),
            "defensa": ProgressBar((620, 300, 220, 22), 100, 50, (70, 180, 100)),
            "energia": ProgressBar((620, 360, 220, 22), 100, 100, (80, 150, 240)),
        }

    def on_enter(self):
        self.game.audio.play_music(volume=0.4)

    def elegir(self, rol):
        self.game.audio.play_sound("click")
        self.game.audio.play_sound("whistle")
        self.game.change_scene("partido", rol=rol)

    def handle_events(self, events):
        for event in events:
            for boton in self.botones.values():
                boton.handle_event(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.change_scene("menu")
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    self.elegir(self.seleccionado)
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    self._mover(-1)
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    self._mover(1)

    def _mover(self, paso):
        i = (_ORDEN.index(self.seleccionado) + paso) % len(_ORDEN)
        self.seleccionado = _ORDEN[i]
        self.game.audio.play_sound("click")

    def update(self):
        datos = ROLES[self.seleccionado]
        self.barras["ataque"].set(datos["ataque"])
        self.barras["defensa"].set(datos["defensa"])
        self.barras["energia"].set(datos["energia"])

    def draw(self, surface):
        try:
            surface.blit(self.game.assets.get_image("campo"), (0, 0))
        except Exception:
            surface.fill((25, 100, 55))
        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        surface.blit(overlay, (0, 0))

        titulo = self.font_titulo.render("Elegi tu ROL", True, (255, 255, 255))
        surface.blit(titulo, titulo.get_rect(centerx=surface.get_width() // 2, y=30))

        datos = ROLES[self.seleccionado]

        # Panel del rol actual
        Panel((40, 110, 500, 330), color=(10, 18, 30, 190),
              border=(240, 240, 240, 200)).draw(surface)

        # Sprite del rol
        try:
            sprite = self.game.assets.get_image(datos["sprite"])
            sprite = pygame.transform.smoothscale(sprite, (140, 202))
            surface.blit(sprite, sprite.get_rect(center=(150, 300)))
        except Exception:
            pygame.draw.rect(surface, datos["color"], (80, 200, 140, 200))

        Label(self.seleccionado, (230, 150), size=42,
              color=(255, 255, 255)).draw(surface)
        self._wrap(surface, datos["desc"], 230, 205, 250,
                   self.font_chico, (200, 215, 235))

        # Atributos
        Label("Ataque", (620, 220), size=28, color=(255, 200, 200)).draw(surface)
        Label("Defensa", (620, 280), size=28, color=(200, 255, 210)).draw(surface)
        Label("Energia", (620, 340), size=28, color=(200, 220, 255)).draw(surface)
        for barra in self.barras.values():
            barra.draw(surface)

        # Botones
        for rol, boton in self.botones.items():
            boton.draw(surface)
            if rol == self.seleccionado:
                pygame.draw.rect(surface, (255, 240, 120), boton.rect, 3,
                                 border_radius=8)

        ayuda = self.font_chico.render(
            "Flechas para elegir rol  |  ENTER para confirmar  |  ESC volver",
            True, (230, 230, 230))
        surface.blit(ayuda, (12, surface.get_height() - 26))

    def _wrap(self, surface, texto, x, y, ancho, font, color):
        palabras = texto.split()
        linea = ""
        for palabra in palabras:
            prueba = (linea + " " + palabra).strip()
            if font.size(prueba)[0] > ancho:
                surface.blit(font.render(linea, True, color), (x, y))
                y += font.get_height() + 2
                linea = palabra
            else:
                linea = prueba
        if linea:
            surface.blit(font.render(linea, True, color), (x, y))
```

**`soccer_rpg/scenes/partido_scene.py`**

```python
# soccer_rpg/scenes/partido_scene.py
"""
Escena del partido: una secuencia de "jugadas" RPG.

En cada jugada elegís una ACCIÓN (ataque / pase / defensa). El resultado se
calcula con tus atributos + azar, mostrando el desenlace, gastando o
reponiendo energía y ganando XP. Al terminar todas las jugadas se pasa a
la escena 'resumen'.
"""
import random

import pygame

from engine.ui import Scene, Button
from engine.ui_elements import Label, Panel, ProgressBar
from soccer_rpg.roles import ROLES

TOTAL_JUGADAS = 8

COSTES = {"ataque": 22, "pase": 10, "defensa": 14}
REGEN = 8


class PartidoScene(Scene):
    def __init__(self, game, rol="Delantero"):
        super().__init__(game)
        self.rol = rol
        self.datos = ROLES.get(rol, ROLES["Delantero"])

        self.max_energia = 100
        self.energia = float(self.datos["energia"])
        self.xp = 0
        self.goles_favor = 0
        self.goles_contra = 0

        self.jugada = 0
        self.estado = "accion"      # accion | resultado
        self.timer = 0.0
        self.mensaje = "Elegi tu accion para la jugada."
        self.ultimo_exito = True
        self.bonus_ataque = 0.0
        self.accion_actual = None

        self.font = pygame.font.Font(None, 32)
        self.font_chico = pygame.font.Font(None, 24)
        self.font_titulo = pygame.font.Font(None, 48)

        self.barra_energia = ProgressBar((30, 544, 260, 22), 100, self.energia,
                                         (240, 200, 60))
        self.barra_xp = ProgressBar((900 - 290, 544, 260, 22), 100, 0,
                                    (120, 190, 255))

        self.botones = {
            "ataque": Button(160, 470, 180, 54, f"Ataque (-{COSTES['ataque']})",
                             lambda: self.elegir_accion("ataque"), font_size=28,
                             color=(150, 50, 50), hover_color=(195, 70, 70)),
            "pase": Button(360, 470, 180, 54, f"Pase (-{COSTES['pase']})",
                           lambda: self.elegir_accion("pase"), font_size=28,
                           color=(45, 75, 150), hover_color=(70, 110, 200)),
            "defensa": Button(560, 470, 180, 54, f"Defensa (-{COSTES['defensa']})",
                              lambda: self.elegir_accion("defensa"), font_size=28,
                              color=(40, 120, 75), hover_color=(60, 165, 105)),
        }

        self.estadio_pelota = pygame.Vector2(450, 300)

    # ------------------------------------------------------------------ #
    def on_enter(self):
        self.game.audio.play_music(volume=0.4)
        self.game.audio.play_sound("whistle")

    # ------------------------------------------------------------------ #
    def elegir_accion(self, accion):
        if self.estado != "accion":
            return
        self.accion_actual = accion
        coste = COSTES[accion]

        # La energía insuficiente penaliza la efectividad.
        penalizacion = 0.0
        if self.energia < coste:
            penalizacion = 0.35
        self.energia = max(0.0, self.energia - coste)

        factor = self._factor(accion) - penalizacion
        prob = min(0.92, max(0.15, 0.25 + 0.65 * factor))
        exito = random.random() < prob

        self._resolver(accion, exito)

        # Reponer energía y cerrar la jugada.
        self.energia = min(self.max_energia, self.energia + REGEN)
        self.jugada += 1
        self.estado = "resultado"
        self.timer = 1.5

    def _factor(self, accion):
        atk = self.datos["ataque"] / 100.0
        dfc = self.datos["defensa"] / 100.0
        if accion == "ataque":
            return atk + self.bonus_ataque
        if accion == "defensa":
            return dfc
        return (atk + dfc) / 2.0

    def _resolver(self, accion, exito):
        self.ultimo_exito = exito
        if accion == "ataque":
            if exito:
                self.goles_favor += 1
                self.xp += 35
                self.mensaje = "¡GOLAZO! Definiste como un crack."
                self.game.audio.play_sound("kick")
                self.game.audio.play_sound("correct")
                self.game.audio.play_sound("cheer")
                self.bonus_ataque = 0.0
            else:
                self.xp += 8
                self.mensaje = "El arquero la saco del angulo. ¡Casi!"
                self.game.audio.play_sound("wrong")
                if random.random() < 0.30:
                    self.goles_contra += 1
                    self.mensaje += " Y encima te convirtieron de contra."
                    self.game.audio.play_sound("wrong")

        elif accion == "pase":
            if exito:
                self.xp += 22
                self.bonus_ataque = 0.12
                self.mensaje = "Gran pase filtrado: tu equipo llega con ventaja."
                self.game.audio.play_sound("correct")
            else:
                self.xp += 5
                self.bonus_ataque = 0.0
                self.mensaje = "El pase salio largo y se perdio la pelota."
                self.game.audio.play_sound("wrong")
                if random.random() < 0.25:
                    self.goles_contra += 1
                    self.mensaje += " El rival lo aprovecho y anoto."
                    self.game.audio.play_sound("wrong")

        else:  # defensa
            if exito:
                self.xp += 26
                self.mensaje = "¡Barriste el ataque rival con solvencia!"
                self.game.audio.play_sound("correct")
            else:
                self.xp += 8
                self.goles_contra += 1
                self.mensaje = "Te superaron en el duelo... gol del rival."
                self.game.audio.play_sound("wrong")

        # Marcar la pelota (efecto visual sencillo)
        self.estadio_pelota.update(450, 300 + (-40 if exito else 40))

    # ------------------------------------------------------------------ #
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.change_scene("menu")
                    return
                if self.estado == "accion":
                    if event.key in (pygame.K_1, pygame.K_a):
                        self.elegir_accion("ataque")
                    elif event.key in (pygame.K_2, pygame.K_p):
                        self.elegir_accion("pase")
                    elif event.key in (pygame.K_3, pygame.K_d):
                        self.elegir_accion("defensa")
            if self.estado == "accion":
                for boton in self.botones.values():
                    boton.handle_event(event)

    def update(self):
        dt = 1.0 / self.game.fps
        self.estadio_pelota += (pygame.Vector2(450, 300) - self.estadio_pelota) * min(1.0, dt * 4)

        self.barra_energia.set(self.energia)
        self.barra_xp.maximum = 100
        self.barra_xp.set(self.xp % 100)

        if self.estado == "resultado":
            self.timer -= dt
            if self.timer <= 0:
                if self.jugada >= TOTAL_JUGADAS:
                    self.game.change_scene(
                        "resumen",
                        rol=self.rol,
                        goles_favor=self.goles_favor,
                        goles_contra=self.goles_contra,
                        xp=self.xp,
                        energia=self.energia,
                    )
                else:
                    self.estado = "accion"
                    self.mensaje = "Elegi tu accion para la jugada."

    # ------------------------------------------------------------------ #
    def _blit(self, surface, nombre, **kwargs):
        try:
            img = self.game.assets.get_image(nombre)
            surface.blit(img, img.get_rect(**kwargs))
        except Exception:
            pass

    def draw(self, surface):
        w, h = surface.get_size()
        try:
            surface.blit(self.game.assets.get_image("campo"), (0, 0))
        except Exception:
            surface.fill((25, 100, 55))

        # Jugador (sprite del rol)
        sprite_rol = self.datos.get("sprite", "jugador_delantero")
        if self.estado == "resultado" and self.accion_actual == "ataque" and self.ultimo_exito:
            sprite_rol += "_kick"
        self._blit(surface, sprite_rol, midbottom=(250, 430))

        self._blit(surface, "balon", center=(int(self.estadio_pelota.x),
                                             int(self.estadio_pelota.y)))

        # Rival sencillo (icono de defensa)
        self._blit(surface, "icono_defensa", center=(650, 300))

        # HUD superior
        Panel((16, 12, w - 32, 74), color=(10, 15, 25, 190),
              border=(240, 240, 240, 200)).draw(surface)
        Label(f"Rol: {self.rol}", (30, 24), size=30, color=(255, 255, 255)).draw(surface)
        Label(f"Jugada {min(self.jugada + (0 if self.estado == 'resultado' else 1), TOTAL_JUGADAS)}"
              f"/{TOTAL_JUGADAS}", (w // 2, 24), size=30,
              color=(255, 240, 140), align="midtop").draw(surface)
        Label(f"XP {self.xp}  |  Nivel {1 + self.xp // 100}",
              (w - 30, 24), size=30, color=(160, 210, 255),
              align="topright").draw(surface)

        # Marcador
        marcador = Label(f"TU EQUIPO {self.goles_favor} - {self.goles_contra} RIVAL",
                         (w // 2, 100), size=34, color=(255, 255, 255),
                         align="midtop")
        marcador.draw(surface)

        # Mensaje de la jugada
        color = (140, 240, 150) if self.ultimo_exito else (255, 160, 150)
        if self.estado == "accion":
            color = (230, 230, 230)
        msg = self.font.render(self.mensaje, True, color)
        surface.blit(msg, msg.get_rect(centerx=w // 2, y=140))

        # Barras
        self.barra_energia.draw(surface)
        self.barra_xp.draw(surface)
        Label("Energia", (30, 568), size=22, color=(255, 240, 200)).draw(surface)
        Label("XP", (900 - 290, 568), size=22, color=(200, 225, 255)).draw(surface)

        # Botones de acción
        for boton in self.botones.values():
            boton.draw(surface)

        # Iconos descriptivos sobre los botones
        self._blit(surface, "icono_ataque", center=(250, 452))
        self._blit(surface, "icono_pase", center=(450, 452))
        self._blit(surface, "icono_defensa", center=(650, 452))

        ayuda = self.font_chico.render(
            "1/A ataque   2/P pase   3/D defensa   ESC menu",
            True, (235, 235, 235))
        surface.blit(ayuda, (12, h - 22))
```

**`soccer_rpg/scenes/resumen_scene.py`**

```python
# soccer_rpg/scenes/resumen_scene.py
"""
Escena de resumen: estadísticas del partido y nivel alcanzado.
"""
import pygame

from engine.ui import Scene, Button
from engine.ui_elements import Label, Panel, ProgressBar


class ResumenScene(Scene):
    def __init__(self, game, rol="Delantero", goles_favor=0, goles_contra=0,
                 xp=0, energia=100):
        super().__init__(game)
        self.rol = rol
        self.goles_favor = goles_favor
        self.goles_contra = goles_contra
        self.xp = xp
        self.energia = energia
        self.nivel = 1 + xp // 100
        self.victoria = goles_favor > goles_contra

        self.font_grande = pygame.font.Font(None, 72)
        self.font = pygame.font.Font(None, 34)
        self.font_chico = pygame.font.Font(None, 26)

        self.boton_otra = Button(300, 470, 300, 54, "Jugar otra vez",
                                 self.otra_vez, color=(45, 90, 150),
                                 hover_color=(70, 120, 195))
        self.boton_menu = Button(300, 532, 300, 50, "Volver al menu", self.menu)

        self.barra_xp = ProgressBar((300, 400, 300, 22), 100, xp % 100,
                                    (120, 190, 255))

    def on_enter(self):
        self.game.audio.play_music(volume=0.4)
        if self.victoria:
            self.game.audio.play_sound("cheer")
        else:
            self.game.audio.play_sound("wrong")

    def otra_vez(self):
        self.game.audio.play_sound("click")
        self.game.change_scene("seleccion")

    def menu(self):
        self.game.audio.play_sound("click")
        self.game.change_scene("menu")

    def handle_events(self, events):
        for event in events:
            self.boton_otra.handle_event(event)
            self.boton_menu.handle_event(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.change_scene("menu")
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    self.otra_vez()

    def update(self):
        self.barra_xp.set(self.xp % 100)

    def draw(self, surface):
        surface.fill((12, 24, 40))
        w = surface.get_width()

        titulo = "¡GANASTE!" if self.victoria else ("EMPATE" if
                 self.goles_favor == self.goles_contra else "PERDISTE")
        color = (140, 240, 150) if self.victoria else (
            (255, 230, 140) if self.goles_favor == self.goles_contra
            else (255, 130, 130))
        t = self.font_grande.render(titulo, True, color)
        surface.blit(t, t.get_rect(centerx=w // 2, y=30))

        # Panel de estadísticas
        Panel((250, 130, 400, 250), color=(0, 0, 0, 150),
              border=(240, 240, 240, 220)).draw(surface)

        Label("RESUMEN DEL PARTIDO", (w // 2, 146), size=30,
              color=(200, 220, 255), align="midtop").draw(surface)

        filas = [
            ("Rol", self.rol),
            ("Goles a favor", str(self.goles_favor)),
            ("Goles en contra", str(self.goles_contra)),
            ("Experiencia (XP)", str(self.xp)),
            ("Nivel alcanzado", str(self.nivel)),
            ("Energia final", f"{int(self.energia)}%"),
        ]
        y = 188
        for etiqueta, valor in filas:
            Label(etiqueta, (275, y), size=28, color=(210, 220, 235)).draw(surface)
            Label(valor, (625, y), size=28, color=(255, 240, 180),
                  align="topright").draw(surface)
            y += 30

        Label("Progreso al siguiente nivel", (w // 2, 378), size=24,
              color=(180, 210, 245), align="midtop").draw(surface)
        self.barra_xp.draw(surface)

        self.boton_otra.draw(surface)
        self.boton_menu.draw(surface)
```

**`soccer_rpg/main.py`**

```python
# soccer_rpg/main.py
"""Ejecutar desde la carpeta 2027 con:  python -m soccer_rpg.main"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from soccer_rpg.game import SoccerRpgGame


def main():
    SoccerRpgGame().run()


if __name__ == "__main__":
    main()
```

## Controles

elegir con las flechas y `ENTER`.

## Cómo ejecutar

Desde la carpeta `2027/`:

```bash
python -m soccer_rpg.main
```
