# Clases 24 y 25 — Retos y UI: fútbol de duelo verbal

Objetivo: minijuegos de **reto con tiempo** y más **elementos de UI**.
`engine/challenge.py` implementa un reto de opción múltiple con
temporizador; `engine/ui_elements.py` añade etiquetas, paneles y
barras.

El ejemplo es `insult_soccer/` (enfoque Game + Escenas): un partido por
turnos donde ganas el gol eligiendo la mejor respuesta.

## Motor — código completo de los módulos nuevos

**`engine/challenge.py`**

```python
"""
engine/challenge.py

Reto de opción múltiple con tiempo límite. Sirve para minijuegos de duelo
(por ejemplo, elegir el mejor "insulto" en el fútbol verbal o acertar una
jugada a tiempo).

    reto = Challenge("¿Cuál es la mejor respuesta?",
                     ["opción A", "opción B", "opción C"], correct_index=1,
                     time_limit=5.0)
    reto.start()
"""

import pygame


class Challenge:
    def __init__(self, prompt, options, correct_index, time_limit=5.0,
                 reward=1, penalty=0):
        self.prompt = prompt
        self.options = options
        self.correct_index = correct_index
        self.time_limit = time_limit
        self.reward = reward
        self.penalty = penalty

        self.active = False
        self.time_left = 0.0
        self.selected = 0
        self.result = None  # None=mientras juega, True/False al terminar
        self.font = None

    def start(self):
        self.active = True
        self.time_left = self.time_limit
        self.selected = 0
        self.result = None

    def handle_event(self, event):
        if not self.active:
            return
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_DOWN, pygame.K_s):
                self.selected = (self.selected + 1) % len(self.options)
            elif event.key in (pygame.K_UP, pygame.K_w):
                self.selected = (self.selected - 1) % len(self.options)
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self._answer(self.selected)

    def _answer(self, index):
        self.result = (index == self.correct_index)
        self.active = False

    def update(self, dt):
        if not self.active:
            return
        self.time_left -= dt
        if self.time_left <= 0:
            self.time_left = 0
            self.result = False
            self.active = False

    def draw(self, surface):
        if self.font is None:
            self.font = pygame.font.Font(None, 30)
            self.big = pygame.font.Font(None, 40)
        w, h = surface.get_size()
        panel = pygame.Rect(0, 0, int(w * 0.8), 260)
        panel.center = (w // 2, h // 2)
        if self.result is None:
            self._draw_play(surface, panel)
        else:
            self._draw_result(surface, panel)

    def _draw_play(self, surface, panel):
        layer = pygame.Surface(panel.size, pygame.SRCALPHA)
        layer.fill((10, 10, 20, 220))
        surface.blit(layer, panel.topleft)
        pygame.draw.rect(surface, (255, 255, 255), panel, 3, border_radius=10)

        prompt = self.big.render(self.prompt, True, (255, 255, 255))
        surface.blit(prompt, (panel.x + 20, panel.y + 18))

        # barra de tiempo
        bar = pygame.Rect(panel.x + 20, panel.y + 60, panel.width - 40, 14)
        pygame.draw.rect(surface, (60, 60, 60), bar)
        ratio = max(0.0, self.time_left / self.time_limit)
        fill = pygame.Rect(bar.x, bar.y, int(bar.width * ratio), bar.height)
        color = (80, 220, 80) if ratio > 0.4 else (240, 180, 40) if ratio > 0.2 else (230, 60, 60)
        pygame.draw.rect(surface, color, fill)

        y = panel.y + 92
        for index, option in enumerate(self.options):
            selected = index == self.selected
            rect = pygame.Rect(panel.x + 24, y, panel.width - 48, 34)
            if selected:
                pygame.draw.rect(surface, (60, 80, 160), rect, border_radius=6)
            color = (255, 255, 120) if selected else (220, 220, 220)
            text = self.font.render(option, True, color)
            surface.blit(text, (rect.x + 8, rect.y + 6))
            y += 40

    def _draw_result(self, surface, panel):
        color = (60, 220, 60) if self.result else (230, 70, 70)
        layer = pygame.Surface(panel.size, pygame.SRCALPHA)
        layer.fill((10, 10, 20, 230))
        surface.blit(layer, panel.topleft)
        pygame.draw.rect(surface, color, panel, 4, border_radius=10)
        msg = "¡Bien!" if self.result else "¡Fallaste!"
        text = self.big.render(msg, True, color)
        surface.blit(text, text.get_rect(center=panel.center))
```

**`engine/ui_elements.py`**

```python
"""
engine/ui_elements.py

Piezas de interfaz reutilizables para los menús y el HUD: etiquetas,
paneles, barras de progreso y barras de vida.
"""

import pygame


class Label:
    def __init__(self, text, pos, size=32, color=(255, 255, 255),
                 align="topleft", font=None):
        self.text = text
        self.pos = pos
        self.color = color
        self.align = align
        self.font = font or pygame.font.Font(None, size)

    def draw(self, surface):
        image = self.font.render(self.text, True, self.color)
        rect = image.get_rect(**{self.align: self.pos})
        surface.blit(image, rect)
        return rect


class Panel:
    def __init__(self, rect, color=(0, 0, 0, 160), border=None, border_radius=8):
        self.rect = pygame.Rect(rect)
        self.color = color
        self.border = border
        self.border_radius = border_radius

    def draw(self, surface):
        layer = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        layer.fill(self.color)
        surface.blit(layer, self.rect.topleft)
        if self.border:
            pygame.draw.rect(surface, self.border, self.rect, 2,
                             border_radius=self.border_radius)


class ProgressBar:
    def __init__(self, rect, maximum=100, value=100,
                 color=(80, 220, 80), background=(50, 50, 50)):
        self.rect = pygame.Rect(rect)
        self.maximum = maximum
        self.value = value
        self.color = color
        self.background = background

    def set(self, value):
        self.value = max(0, min(self.maximum, value))

    def draw(self, surface):
        pygame.draw.rect(surface, self.background, self.rect, border_radius=4)
        ratio = self.value / self.maximum if self.maximum else 0
        fill = pygame.Rect(self.rect.x, self.rect.y,
                           int(self.rect.width * ratio), self.rect.height)
        pygame.draw.rect(surface, self.color, fill, border_radius=4)
        pygame.draw.rect(surface, (230, 230, 230), self.rect, 2, border_radius=4)


class HealthBar(ProgressBar):
    def draw(self, surface):
        ratio = self.value / self.maximum if self.maximum else 0
        if ratio > 0.5:
            self.color = (80, 220, 80)
        elif ratio > 0.25:
            self.color = (240, 190, 40)
        else:
            self.color = (230, 60, 60)
        super().draw(surface)
```

## Juego de ejemplo — código completo

**`insult_soccer/__init__.py`**

```python
# insult_soccer/__init__.py
```

**`insult_soccer/game.py`**

```python
# insult_soccer/game.py
"""
INSULT SOCCER — fútbol de duelo verbal (clases 24-25).

Enfoque ESCENAS:
    'menu'  -> elegir jugar
    'match' -> partido por turnos de retos verbales (engine.challenge.Challenge)
               El primero en meter 3 goles gana.
    'final' -> resultado y revancha.

Clase principal: InsultSoccerGame
"""
import os

from engine.game_loop import Game
from engine.asset_manager import AssetManager
from engine.audio import AudioManager
from engine.shared_assets import sfx_path, music_path

from insult_soccer.scenes.menu_scene import MenuScene
from insult_soccer.scenes.match_scene import MatchScene
from insult_soccer.scenes.final_scene import FinalScene


class InsultSoccerGame(Game):
    def __init__(self):
        super().__init__(800, 600, "Insult Soccer", 60)

        self.game_dir = os.path.dirname(os.path.abspath(__file__))
        self.assets_dir = os.path.join(self.game_dir, "assets", "sprites")

        self.assets = AssetManager()
        self.audio = AudioManager()
        self.load_assets()

        # Escenas (clases, no instancias).
        self.add_scene("menu", MenuScene)
        self.add_scene("match", MatchScene)
        self.add_scene("final", FinalScene)
        self.change_scene("menu")

    def load_assets(self):
        """Carga las imágenes generadas y los sonidos compartidos."""
        imagenes = {
            "campo": "campo.png",
            "arco": "arco.png",
            "balon": "balon.png",
            "jugador_azul": "jugador_azul.png",
            "jugador_rojo": "jugador_rojo.png",
            "jugador_azul_kick": "jugador_azul_kick.png",
            "jugador_rojo_kick": "jugador_rojo_kick.png",
            "icono_correcto": "icono_correcto.png",
            "icono_fallo": "icono_fallo.png",
            "logo": "logo.png",
        }
        for nombre, archivo in imagenes.items():
            try:
                self.assets.load_image(nombre, os.path.join(self.assets_dir, archivo))
            except Exception as e:  # pragma: no cover - solo si falta un PNG
                print(f"Aviso: no se pudo cargar '{archivo}': {e}")

        for sonido in ("kick", "cheer", "wrong", "correct", "whistle", "click"):
            self.audio.load_sound(sonido, sfx_path(sonido))
        self.audio.load_music(music_path("soccer"))
```

**`insult_soccer/generar_assets.py`**

```python
"""
insult_soccer/generar_assets.py

Genera los gráficos del juego "fútbol de duelo verbal" (clases 24-25):
campo, dos jugadores, balón, arco y logo. Ejecutar UNA vez:

    python insult_soccer/generar_assets.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

from herramientas import genlib as g  # noqa: E402

OUT = os.path.join(HERE, "assets", "sprites")

W, H = 800, 600


def make_campo(w=W, h=H):
    """Campo de fútbol vertical: césped a rayas, líneas, círculo y áreas."""
    img = g.new(w, h)
    bg = g.vgrad(w, h, (46, 140, 66), (30, 104, 52))
    img = g.Image.alpha_composite(img, bg)
    d = g.ImageDraw.Draw(img)

    # Rayas de césped
    stripe = h // 8
    for i in range(9):
        if i % 2 == 0:
            d.rectangle([0, i * stripe, w, i * stripe + stripe],
                        fill=(40, 150, 72, 70))

    # Borde
    m = 28
    d.rectangle([m, m, w - m, h - m], outline=(240, 240, 240, 210), width=4)
    # Línea y círculo central
    d.line([(m, h // 2), (w - m, h // 2)], fill=(240, 240, 240, 210), width=4)
    r = 78
    d.ellipse([w // 2 - r, h // 2 - r, w // 2 + r, h // 2 + r],
              outline=(240, 240, 240, 210), width=4)
    d.ellipse([w // 2 - 6, h // 2 - 6, w // 2 + 6, h // 2 + 6],
              fill=(240, 240, 240, 210))

    # Áreas (arriba y abajo)
    aw, ah = 320, 90
    d.rectangle([w // 2 - aw // 2, m, w // 2 + aw // 2, m + ah],
                outline=(240, 240, 240, 210), width=4)
    d.rectangle([w // 2 - aw // 2, h - m - ah, w // 2 + aw // 2, h - m],
                outline=(240, 240, 240, 210), width=4)
    return img


def make_arco(w=190, h=72):
    """Portería con red."""
    img = g.new(w, h)
    d = g.ImageDraw.Draw(img)
    post = (240, 240, 240, 255)
    edge = (110, 110, 120, 255)
    # Red
    for x in range(12, w - 8, 12):
        d.line([(x, 10), (x, h)], fill=(230, 230, 230, 130), width=1)
    for y in range(10, h, 12):
        d.line([(10, y), (w - 10, y)], fill=(230, 230, 230, 130), width=1)
    # Postes y travesaño
    d.rectangle([0, 0, 10, h], fill=post, outline=edge, width=1)
    d.rectangle([w - 10, 0, w, h], fill=post, outline=edge, width=1)
    d.rectangle([0, 0, w, 10], fill=post, outline=edge, width=1)
    return img


def make_balon(r=15):
    img = g.make_ball((250, 250, 250, 255), r)
    d = g.ImageDraw.Draw(img)
    size = r * 2
    # Manchas negras sencillas
    spots = [(0.5, 0.35), (0.32, 0.62), (0.68, 0.62)]
    for fx, fy in spots:
        cx, cy = int(size * fx), int(size * fy)
        pr = max(2, r // 4)
        d.ellipse([cx - pr, cy - pr, cx + pr, cy + pr], fill=(30, 30, 30, 255))
    return img


def make_icono(texto, color):
    """Icono circular con una letra (para el reto)."""
    size = 44
    img = g.new(size, size)
    d = g.ImageDraw.Draw(img)
    d.ellipse([1, 1, size - 2, size - 2], fill=color, outline=(20, 20, 30, 255),
              width=2)
    f = g.font(26)
    box = d.textbbox((0, 0), texto, font=f)
    d.text(((size - (box[2] - box[0])) / 2 - box[0],
            (size - (box[3] - box[1])) / 2 - box[1]), texto, font=f,
           fill=(255, 255, 255, 255))
    return img


def main():
    g.ensure_dir(OUT)

    g.save_png(make_campo(), os.path.join(OUT, "campo.png"))
    g.save_png(make_arco(), os.path.join(OUT, "arco.png"))
    g.save_png(make_balon(), os.path.join(OUT, "balon.png"))

    skin = (232, 194, 158, 255)
    azul = dict(skin=skin, shirt=(50, 110, 235, 255),
                pants=(240, 240, 245, 255), hair=(40, 30, 20, 255))
    rojo = dict(skin=skin, shirt=(220, 55, 55, 255),
                pants=(60, 40, 40, 255), hair=(25, 20, 15, 255))

    g.save_png(g.make_humanoid(74, 108, pose="idle", **azul),
               os.path.join(OUT, "jugador_azul.png"))
    g.save_png(g.make_humanoid(74, 108, pose="idle", **rojo),
               os.path.join(OUT, "jugador_rojo.png"))
    g.save_png(g.make_humanoid(74, 108, pose="kick", **azul),
               os.path.join(OUT, "jugador_azul_kick.png"))
    g.save_png(g.make_humanoid(74, 108, pose="kick", **rojo),
               os.path.join(OUT, "jugador_rojo_kick.png"))

    # Iconos de resultado del duelo verbal
    g.save_png(make_icono("!", (60, 180, 80, 255)),
               os.path.join(OUT, "icono_correcto.png"))
    g.save_png(make_icono("X", (210, 60, 60, 255)),
               os.path.join(OUT, "icono_fallo.png"))

    g.save_png(g.text_image("INSULT SOCCER", 56, (255, 240, 120, 255)),
               os.path.join(OUT, "logo.png"))

    print("Assets de insult_soccer generados en", OUT)


if __name__ == "__main__":
    main()
```

**`insult_soccer/scenes/__init__.py`**

```python
# insult_soccer/scenes/__init__.py
```

**`insult_soccer/scenes/menu_scene.py`**

```python
# insult_soccer/scenes/menu_scene.py
import pygame

from engine.ui import Scene, Button


class MenuScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.font_title = pygame.font.Font(None, 78)
        self.font_hint = pygame.font.Font(None, 26)

        self.boton_jugar = Button(300, 340, 200, 56, "Jugar", self.jugar)
        self.boton_salir = Button(300, 410, 200, 56, "Salir", self.salir)
        self.t = 0.0

    def on_enter(self):
        self.game.audio.play_music(volume=0.4)

    def jugar(self):
        self.game.audio.play_sound("click")
        self.game.audio.play_sound("whistle")
        self.game.change_scene("match")

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
        try:
            surface.blit(self.game.assets.get_image("campo"), (0, 0))
        except Exception:
            surface.fill((30, 110, 55))

        # Oscurecer para que se lea el texto
        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))
        surface.blit(overlay, (0, 0))

        try:
            logo = self.game.assets.get_image("logo")
            surface.blit(logo, logo.get_rect(centerx=surface.get_width() // 2, y=120))
        except Exception:
            self._text_center(surface, "INSULT SOCCER", 78, 130, (255, 240, 120))

        self._text_center(surface, "Futbol de duelo verbal", 34, 230, (230, 240, 255))
        self._text_center(surface, "Primero en meter 3 goles gana", 26, 275,
                          (180, 220, 190))

        # Balón que bota
        try:
            balon = self.game.assets.get_image("balon")
            import math
            y = 300 + int(math.sin(self.t * 3) * 10)
            surface.blit(balon, balon.get_rect(center=(surface.get_width() // 2, y)))
        except Exception:
            pass

        self.boton_jugar.draw(surface)
        self.boton_salir.draw(surface)

    def _text_center(self, surface, texto, size, y, color):
        font = pygame.font.Font(None, size)
        img = font.render(texto, True, color)
        surface.blit(img, img.get_rect(centerx=surface.get_width() // 2, y=y))
```

**`insult_soccer/scenes/match_scene.py`**

```python
# insult_soccer/scenes/match_scene.py
"""
Escena del partido: duelos verbales por turnos.

En cada turno aparece un reto de opción múltiple (engine.challenge.Challenge).
- Acierta  -> el balón avanza y metes gol (sfx kick + cheer).
- Falla    -> gol del rival (sfx wrong).
El primero en llegar a 3 goles gana y se pasa a la escena 'final'.
"""
import random

import pygame

from engine.ui import Scene
from engine.ui_elements import Label, Panel
from engine.challenge import Challenge

# Puntos de meta (jugador ataca arriba, rival abajo).
META_JUGADOR = (400, 78)
META_RIVAL = (400, 522)
CENTRO = (400, 300)

TIME_LIMIT = 6.0
GOLES_PARA_GANAR = 3


RETOS = [
    {
        "prompt": "El rival suelta: '¡Juegas como mi abuela!'",
        "opciones": [
            "Tu abuela al menos entiende el fuera de juego",
            "Gracias, me entrenó ella",
            "¿Y tú por qué miras tanto a mi abuela?",
        ],
        "correcta": 0,
    },
    {
        "prompt": "El rival dice: '¡No corrés ni para el autobús!'",
        "opciones": [
            "El autobús me espera, tú llegas tarde a todo",
            "Cierto, prefiero el tren",
            "Autobús... ¿cuál?",
        ],
        "correcta": 0,
    },
    {
        "prompt": "El rival se burla: '¡Tus botines son de plástico!'",
        "opciones": [
            "Y aun así te ganan los de plástico",
            "Los compré en oferta, gracias",
            "Son reciclados, cuido el planeta",
        ],
        "correcta": 0,
    },
    {
        "prompt": "El rival grita: '¡Eres más lento que una tortuga!'",
        "opciones": [
            "Y aun así te llego a la pelota antes",
            "Me gustan las tortugas",
            "La tortuga gana la carrera al final",
        ],
        "correcta": 0,
    },
    {
        "prompt": "El rival dice: '¡Apostaría mi casa a que pierdes!'",
        "opciones": [
            "Empieza a hacer las valijas",
            "No apuestes, es de mala educación",
            "¿Me la vendes barata?",
        ],
        "correcta": 0,
    },
    {
        "prompt": "El rival se ríe: '¡Hasta el arco se aburre contigo!'",
        "opciones": [
            "El arco tiene miedo de tus remates",
            "El arco y yo somos amigos",
            "Los arcos no sienten nada",
        ],
        "correcta": 0,
    },
    {
        "prompt": "El rival afirma: '¡Tú no sabes ni tirar un penal!'",
        "opciones": [
            "Mírame ahora y toma nota",
            "Los penales son de cobarde",
            "¿Me enseñas tú?",
        ],
        "correcta": 0,
    },
    {
        "prompt": "El rival dice: '¡Mi equipo juega mejor sin ti... digo, sin mí!'",
        "opciones": [
            "Se te trabó la lengua y el cerebro",
            "Hablás solo, ¿eh?",
            "Sin ti juegan mejor, es verdad",
        ],
        "correcta": 0,
    },
    {
        "prompt": "El rival se burla: '¡Ese peinado no ayuda a correr!'",
        "opciones": [
            "A mi peinado le sobra velocidad para dos",
            "El peinado va conmigo a todos lados",
            "Y el tuyo sí que vuela... la peluca",
        ],
        "correcta": 0,
    },
    {
        "prompt": "El rival reta: '¡A que no la metes ni en sueños!'",
        "opciones": [
            "Estoy despierto y ya vas perdiendo",
            "Sueño con la victoria, es distinto",
            "¿Contamos ovejas o goles?",
        ],
        "correcta": 0,
    },
]


class MatchScene(Scene):
    def __init__(self, game):
        super().__init__(game)

        self.font_grande = pygame.font.Font(None, 64)
        self.font = pygame.font.Font(None, 34)
        self.font_chico = pygame.font.Font(None, 26)

        self.marcador_jugador = 0
        self.marcador_rival = 0

        self.retos = list(RETOS)
        random.shuffle(self.retos)
        self.reto_idx = 0

        self.challenge = None
        self.estado = "espera"     # espera | jugada | resultado
        self.timer = 0.9
        self.mensaje = "¡Que empiece el duelo!"
        self.ultimo_acierto = True

        self.balon = pygame.Vector2(CENTRO)
        self.balon_objetivo = pygame.Vector2(CENTRO)
        self.kick_timer = 0.0

    # ------------------------------------------------------------------ #
    def on_enter(self):
        self.game.audio.play_music(volume=0.4)
        self.game.audio.play_sound("whistle")

    def on_exit(self):
        pass

    # ------------------------------------------------------------------ #
    def _nuevo_reto(self):
        reto = self.retos[self.reto_idx % len(self.retos)]
        self.reto_idx += 1
        self.challenge = Challenge(
            reto["prompt"], reto["opciones"], reto["correcta"],
            time_limit=TIME_LIMIT,
        )
        self.challenge.start()
        self.estado = "jugada"
        self.mensaje = "¡Responde rapido!"
        self.balon_objetivo.update(CENTRO)
        self.kick_timer = 0.0

    def _resolver(self, correcto):
        self.ultimo_acierto = bool(correcto)
        if correcto:
            self.game.audio.play_sound("correct")
            self.game.audio.play_sound("kick")
            self.game.audio.play_sound("cheer")
            self.marcador_jugador += 1
            self.mensaje = "¡GOL de tu equipo!"
            self.balon_objetivo.update(META_JUGADOR)
            self.kick_timer = 0.5
        else:
            self.game.audio.play_sound("wrong")
            self.marcador_rival += 1
            self.mensaje = "Respuesta floja... gol del rival"
            self.balon_objetivo.update(META_RIVAL)

        self.estado = "resultado"
        self.timer = 1.6

    # ------------------------------------------------------------------ #
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.game.change_scene("menu")
                return
            if self.estado == "jugada" and self.challenge is not None:
                self.challenge.handle_event(event)

    def update(self):
        dt = 1.0 / self.game.fps
        self.balon += (self.balon_objetivo - self.balon) * min(1.0, dt * 5.0)
        if self.kick_timer > 0:
            self.kick_timer -= dt

        if self.estado == "espera":
            self.timer -= dt
            if self.timer <= 0:
                self._nuevo_reto()

        elif self.estado == "jugada":
            if self.challenge is not None and self.challenge.active:
                self.challenge.update(dt)
            if self.challenge is not None and self.challenge.result is not None:
                self._resolver(self.challenge.result)

        elif self.estado == "resultado":
            self.timer -= dt
            if self.timer <= 0:
                if (self.marcador_jugador >= GOLES_PARA_GANAR or
                        self.marcador_rival >= GOLES_PARA_GANAR):
                    self.game.change_scene(
                        "final",
                        goles_jugador=self.marcador_jugador,
                        goles_rival=self.marcador_rival,
                    )
                else:
                    self._nuevo_reto()

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
            surface.fill((30, 110, 55))

        # Porterías
        self._blit(surface, "arco", midbottom=(400, 90))
        arc2 = None
        try:
            arc2 = pygame.transform.flip(self.game.assets.get_image("arco"), False, True)
            surface.blit(arc2, arc2.get_rect(midtop=(400, 510)))
        except Exception:
            pass

        # Jugadores
        kick_local = self.kick_timer > 0
        jug_azul = "jugador_azul_kick" if kick_local else "jugador_azul"
        jug_rojo = "jugador_rojo_kick" if kick_local else "jugador_rojo"
        bx = int(self.balon.x)
        self._blit(surface, jug_azul, midbottom=(bx - 70, 470))
        self._blit(surface, jug_rojo, midbottom=(bx + 70, 470))

        # Balón
        self._blit(surface, "balon", center=(bx, int(self.balon.y)))

        # Marcador (engine.ui_elements)
        panel = Panel((w // 2 - 190, 12, 380, 58),
                      color=(10, 15, 25, 190), border=(240, 240, 240, 255))
        panel.draw(surface)
        marcador = Label(
            f"TU {self.marcador_jugador}   -   {self.marcador_rival} RIVAL",
            (w // 2, 41), size=40, color=(255, 255, 255), align="center",
        )
        marcador.draw(surface)
        meta = Label(f"Primero a {GOLES_PARA_GANAR}", (w // 2, 78),
                     size=22, color=(255, 240, 140), align="center")
        meta.draw(surface)

        # Mensaje de estado
        if self.mensaje:
            color = (140, 240, 150) if self.ultimo_acierto else (255, 150, 140)
            msg = self.font.render(self.mensaje, True, color)
            surface.blit(msg, msg.get_rect(centerx=w // 2, y=100))

        # Reto activo / resultado del reto
        if self.challenge is not None and self.estado in ("jugada", "resultado"):
            self.challenge.draw(surface)

        # Ayuda
        ayuda = self.font_chico.render(
            "Flechas/W-S elegir   ENTER responder   ESC menu",
            True, (235, 235, 235),
        )
        surface.blit(ayuda, (12, h - 30))

        # Icono del último resultado del duelo verbal
        if self.estado == "resultado":
            icono = "icono_correcto" if self.ultimo_acierto else "icono_fallo"
            self._blit(surface, icono, center=(bx - 70, 400))
```

**`insult_soccer/scenes/final_scene.py`**

```python
# insult_soccer/scenes/final_scene.py
import pygame

from engine.ui import Scene, Button
from engine.ui_elements import Label, Panel


class FinalScene(Scene):
    def __init__(self, game, goles_jugador=0, goles_rival=0):
        super().__init__(game)
        self.goles_jugador = goles_jugador
        self.goles_rival = goles_rival
        self.ganaste = goles_jugador > goles_rival

        self.font_grande = pygame.font.Font(None, 84)
        self.font = pygame.font.Font(None, 40)

        self.boton_revancha = Button(280, 400, 240, 54, "Revancha", self.revancha)
        self.boton_menu = Button(280, 466, 240, 54, "Menú", self.menu)
        self.t = 0.0

    def on_enter(self):
        self.game.audio.play_sound("whistle")
        if self.ganaste:
            self.game.audio.play_sound("cheer")
        else:
            self.game.audio.play_sound("wrong")

    def revancha(self):
        self.game.audio.play_sound("click")
        self.game.change_scene("match")

    def menu(self):
        self.game.audio.play_sound("click")
        self.game.change_scene("menu")

    def handle_events(self, events):
        for event in events:
            self.boton_revancha.handle_event(event)
            self.boton_menu.handle_event(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.change_scene("menu")
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    self.revancha()

    def update(self):
        self.t += 1.0 / self.game.fps

    def draw(self, surface):
        surface.fill((12, 24, 40))
        w = surface.get_width()

        titulo = "¡VICTORIA!" if self.ganaste else "DERROTA"
        color = (140, 240, 150) if self.ganaste else (255, 120, 120)
        img = self.font_grande.render(titulo, True, color)
        surface.blit(img, img.get_rect(centerx=w // 2, y=140))

        panel = Panel((w // 2 - 160, 250, 320, 70),
                      color=(0, 0, 0, 160), border=(240, 240, 240, 255))
        panel.draw(surface)
        marcador = Label(f"{self.goles_jugador}  -  {self.goles_rival}",
                        (w // 2, 285), size=52, color=(255, 255, 255),
                        align="center")
        marcador.draw(surface)

        sub = "Tu equipo" if self.ganaste else "El rival"
        sub += " gano el duelo verbal"
        s = self.font.render(sub, True, (210, 220, 235))
        surface.blit(s, s.get_rect(centerx=w // 2, y=336))

        self.boton_revancha.draw(surface)
        self.boton_menu.draw(surface)
```

**`insult_soccer/main.py`**

```python
# insult_soccer/main.py
"""Ejecutar desde la carpeta 2027 con:  python -m insult_soccer.main"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from insult_soccer.game import InsultSoccerGame


def main():
    InsultSoccerGame().run()


if __name__ == "__main__":
    main()
```

## Controles

`↑/↓` elegir respuesta, `ENTER` responder.

## Cómo ejecutar

Desde la carpeta `2027/`:

```bash
python -m insult_soccer.main
```
