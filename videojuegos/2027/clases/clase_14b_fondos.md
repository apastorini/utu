# Clase 14b — Fondos dinámicos: parallax, vídeo y partículas

Objetivo: fondos que se mueven. `engine/background.py` trae
`ParallaxBackground` (capas a distinta velocidad), `FrameBackground`
(reproduce una secuencia de imágenes) y `VideoBackground` (vídeo en
tiempo real con OpenCV, opcional). `engine/particle.py` añade un
sistema de partículas.

El ejemplo es `video_demo/` (enfoque Game Loop): parallax con las
flechas, lluvia/nieve con partículas y un fondo de "vídeo" por frames.

## Motor — código completo de los módulos nuevos

**`engine/background.py`**

```python
"""
engine/background.py

Fondos dinámicos:

- ParallaxBackground: varias capas que se desplazan a distinta velocidad.
- FrameBackground: reproduce una secuencia de imágenes (un "vídeo" exportado
  a frames), sin necesitar librerías externas.
- VideoBackground: vídeo en tiempo real con OpenCV (opcional; si no está
  instalado, se desactiva solo).
"""

import os

import pygame


class ParallaxLayer:
    def __init__(self, image, speed, y=0, repeat_x=True):
        self.image = image
        self.speed = speed
        self.y = y
        self.repeat_x = repeat_x
        self.offset = 0.0

    def update(self, dx):
        self.offset = (self.offset + dx * self.speed) % self.image.get_width()

    def draw(self, surface):
        w = self.image.get_width()
        x = -self.offset
        surface.blit(self.image, (x, self.y))
        if self.repeat_x:
            surface.blit(self.image, (x + w, self.y))


class ParallaxBackground:
    """Conjunto de capas ordenadas de la más lejana a la más cercana."""

    def __init__(self):
        self.layers = []

    def add_layer(self, image, speed, y=0, repeat_x=True):
        self.layers.append(ParallaxLayer(image, speed, y, repeat_x))

    def update(self, dx):
        for layer in self.layers:
            layer.update(dx)

    def draw(self, surface):
        for layer in self.layers:
            layer.draw(surface)


class FrameBackground:
    """Reproduce una carpeta de imágenes (frame_00000.png, frame_00001.png...)."""

    def __init__(self, frames_dir, fps=20):
        self.frames = []
        for name in sorted(os.listdir(frames_dir)):
            if name.lower().endswith((".png", ".jpg", ".bmp")):
                self.frames.append(
                    pygame.image.load(os.path.join(frames_dir, name)).convert()
                )
        self.fps = fps
        self.index = 0
        self.timer = 0.0

    def update(self, dt):
        if not self.frames:
            return
        self.timer += dt
        if self.timer >= 1.0 / self.fps:
            self.timer = 0.0
            self.index = (self.index + 1) % len(self.frames)

    def draw(self, surface):
        if self.frames:
            surface.blit(self.frames[self.index], (0, 0))

    def __len__(self):
        return len(self.frames)


class VideoBackground:
    """
    Fondo de vídeo en tiempo real con OpenCV.

    Si no está instalado `opencv-python`, el objeto queda inactivo y el juego
    puede seguir funcionando con otro fondo.
    """

    def __init__(self, video_path, size=None):
        self.available = False
        self.capture = None
        try:
            import cv2  # noqa: F401
            self._cv2 = cv2
            self.capture = cv2.VideoCapture(video_path)
            self.available = self.capture.isOpened()
        except Exception as e:
            print(f"VideoBackground desactivado (falta OpenCV o el vídeo): {e}")

        self.size = size
        self.surface = None

    def update(self, dt):
        if not self.available:
            return
        ok, frame = self.capture.read()
        if not ok:
            self.capture.set(self._cv2.CAP_PROP_POS_FRAMES, 0)
            ok, frame = self.capture.read()
        if not ok:
            return
        frame = self._cv2.cvtColor(frame, self._cv2.COLOR_BGR2RGB)
        surf = pygame.image.frombuffer(frame.tobytes(),
                                       frame.shape[1::-1], "RGB")
        if self.size:
            surf = pygame.transform.scale(surf, self.size)
        self.surface = surf

    def draw(self, surface):
        if self.surface:
            surface.blit(self.surface, (0, 0))
```

**`engine/particle.py`**

```python
"""
engine/particle.py

Sistema de partículas muy simple (chispas, polvo, explosiones...).
Se usa, por ejemplo, al golpear en el Arkanoid, al saltar en el
plataformero o como fondo estrellado.
"""

import random

import pygame


class Particle:
    def __init__(self, x, y, velocity, color, life, size,
                 gravity=0.0, fade=True):
        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2(velocity)
        self.color = color
        self.life = life
        self.max_life = life
        self.size = size
        self.gravity = gravity
        self.fade = fade

    def update(self, dt):
        self.vel.y += self.gravity * dt
        self.pos += self.vel * dt
        self.life -= dt

    @property
    def dead(self):
        return self.life <= 0

    def draw(self, surface):
        if self.size <= 0:
            return
        alpha = 255
        if self.fade:
            alpha = max(0, min(255, int(255 * (self.life / self.max_life))))
        radius = max(1, int(self.size))
        layer = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(layer, (*self.color, alpha), (radius, radius), radius)
        surface.blit(layer, (self.pos.x - radius, self.pos.y - radius))


class ParticleSystem:
    def __init__(self):
        self.particles = []

    def emit(self, x, y, count=20, speed=(60, 220), color=(255, 200, 60),
             life=(0.3, 0.8), size=(2, 5), gravity=250.0, angle=0.0, spread=360.0):
        """Crea un "chorro" de partículas desde (x, y)."""
        for _ in range(count):
            a = angle + random.uniform(-spread / 2, spread / 2)
            s = random.uniform(*speed)
            rad = pygame.math.Vector2(1, 0).rotate(a) * s
            self.particles.append(
                Particle(x, y, (rad.x, rad.y),
                         color if isinstance(color, tuple) else (255, 255, 255),
                         random.uniform(*life), random.uniform(*size), gravity)
            )

    def update(self, dt):
        for p in self.particles:
            p.update(dt)
        self.particles = [p for p in self.particles if not p.dead]

    def draw(self, surface):
        for p in self.particles:
            p.draw(surface)

    def __len__(self):
        return len(self.particles)
```

## Juego de ejemplo — código completo

**`video_demo/__init__.py`**

```python
"""video_demo — Clase 14b: fondos dinámicos (parallax, partículas y "vídeo")."""
```

**`video_demo/generar_assets.py`**

```python
"""
video_demo/generar_assets.py

Genera los gráficos de la clase 14b (fondos dinámicos):

- Tres capas de PARALLAX: cielo, montañas y árboles (se repiten en horizontal
  de forma continua para que el bucle no muestre costuras).
- Una SECUENCIA de 24 fotogramas `assets/frames/frame_00.png ... frame_23.png`
  que simula un "vídeo" (un sol que recorre el cielo sobre el mar con olas).

Ejecutar una vez desde la carpeta 2027:

    python video_demo/generar_assets.py
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

from herramientas import genlib as g  # noqa: E402

W, H = 960, 600
LAYERS_DIR = os.path.join(HERE, "assets", "layers")
FRAMES_DIR = os.path.join(HERE, "assets", "frames")
N_FRAMES = 24


# --------------------------------------------------------------------------- #
#  Capas de parallax
# --------------------------------------------------------------------------- #
def make_sky():
    """Cielo con degradado y nubes (se repite en horizontal)."""
    img = g.vgrad(W, H, (110, 175, 235), (205, 232, 255))
    d = g.ImageDraw.Draw(img)
    cloud = (255, 255, 255, 235)
    for cx, cy, s in ((140, 90, 1.0), (520, 150, 0.8), (820, 70, 1.2)):
        # Se dibuja también desplazada ±W para que el borde empalme.
        for dx in (-W, 0, W):
            for k in range(5):
                r = 26 * s
                x = cx + dx - 70 * s + k * 35 * s
                y = cy + (4 if k % 2 else -4) * s
                d.ellipse([x - r, y - r * 0.7, x + r, y + r * 0.7], fill=cloud)
    return img


def make_mountains():
    """Silueta de montañas periódica (frecuencias enteras => sin costura)."""
    img = g.new(W, H)
    d = g.ImageDraw.Draw(img)
    xs = g.np.arange(W)

    def ridge(base, amps):
        h = g.np.full(W, float(base))
        for k, (freq, amp, phase) in enumerate(amps):
            h = h - amp * g.np.sin(2 * math.pi * freq * xs / W + phase)
        return h

    back = ridge(H * 0.70, [(1, 70, 0.5), (3, 35, 1.7), (5, 16, 0.2)])
    pts_back = [(int(x), int(y)) for x, y in zip(xs, back)]
    d.polygon(pts_back + [(W, H), (0, H)], fill=(88, 108, 140, 255))

    front = ridge(H * 0.80, [(1, 95, 2.1), (2, 40, 0.6), (4, 20, 1.1)])
    pts_front = [(int(x), int(y)) for x, y in zip(xs, front)]
    d.polygon(pts_front + [(W, H), (0, H)], fill=(58, 78, 104, 255))
    d.line(pts_front, fill=(90, 112, 140, 255), width=3)
    return img


def make_trees():
    """Árboles repetidos de forma continua en horizontal."""
    img = g.new(W, H)
    d = g.ImageDraw.Draw(img)
    rng = g.np.random.default_rng(7)
    base_y = int(H * 0.82)
    for _ in range(16):
        x = float(rng.uniform(0, W))
        th = float(rng.uniform(70, 130))
        green = tuple(int(c) for c in rng.uniform([24, 70, 32], [56, 130, 66])) + (255,)
        dark = g.shade(green, 0.75)
        for dx in (-W, 0, W):
            tx = int(x + dx)
            d.rectangle([tx - 4, base_y - 10, tx + 4, base_y + 14],
                        fill=(86, 54, 28, 255))
            d.polygon([(tx, base_y - th), (tx - 26, base_y + 4), (tx + 26, base_y + 4)],
                      fill=green)
            d.polygon([(tx, base_y - th * 0.55), (tx - 32, base_y + 8), (tx + 32, base_y + 8)],
                      fill=dark)
    return img


# --------------------------------------------------------------------------- #
#  Secuencia de "vídeo"
# --------------------------------------------------------------------------- #
def _lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def make_frame(i):
    """Fotograma i de N_FRAMES: un sol recorriendo el cielo sobre el mar."""
    t = i / N_FRAMES
    horizon = int(H * 0.60)
    day = math.sin(math.pi * t)  # 0 en los extremos, 1 en el centro.

    top = _lerp((36, 52, 120), (92, 172, 232), day)
    bottom = _lerp((246, 168, 110), (206, 228, 252), day)
    sky = g.vgrad(W, horizon, top + (255,), bottom + (255,))

    sea = g.vgrad(W, H - horizon, (34, 74, 134), (10, 30, 66))

    img = g.new(W, H)
    img.paste(sky, (0, 0))
    img.paste(sea, (0, horizon))
    d = g.ImageDraw.Draw(img)

    # Sol en un arco.
    sun_x = int(W * 0.5 + (t - 0.5) * W * 0.65)
    sun_y = int(horizon - 30 - 230 * math.sin(math.pi * t))
    for r, alpha in ((70, 40), (52, 90), (38, 160)):
        glow = g.new(2 * r, 2 * r)
        g.ImageDraw.Draw(glow).ellipse([0, 0, 2 * r - 1, 2 * r - 1],
                                       fill=(255, 230, 150, alpha))
        img.paste(glow, (sun_x - r, sun_y - r), glow)
    d.ellipse([sun_x - 26, sun_y - 26, sun_x + 26, sun_y + 26],
              fill=(255, 246, 190, 255))

    # Olas del mar: líneas sinusoidales cuya fase cambia con el fotograma.
    sea_h = H - horizon
    for k in range(14):
        y = horizon + 6 + k * (sea_h - 12) / 14.0
        amp = 2 + k * 0.7
        phase = i * 0.6 + k * 0.9
        pts = [(x, int(y + amp * math.sin(2 * math.pi * x / 130.0 + phase)))
               for x in range(0, W + 1, 6)]
        alpha = 120 + k * 6
        d.line(pts, fill=(150, 200, 240, min(255, alpha)), width=2)

    # Reflejo del sol sobre el agua.
    if 0 <= sun_x < W:
        for k in range(10):
            y = horizon + 8 + k * (sea_h - 16) / 10.0
            w = 18 + k * 4
            d.line([(sun_x - w, int(y)), (sun_x + w, int(y))],
                   fill=(255, 240, 190, 150), width=3)

    return img


def main():
    g.ensure_dir(LAYERS_DIR)
    g.ensure_dir(FRAMES_DIR)

    g.save_png(make_sky(), os.path.join(LAYERS_DIR, "cielo.png"))
    g.save_png(make_mountains(), os.path.join(LAYERS_DIR, "montanas.png"))
    g.save_png(make_trees(), os.path.join(LAYERS_DIR, "arboles.png"))

    for i in range(N_FRAMES):
        g.save_png(make_frame(i), os.path.join(FRAMES_DIR, f"frame_{i:02d}.png"))

    print("Capas de parallax en", LAYERS_DIR)
    print(f"{N_FRAMES} fotogramas de video en", FRAMES_DIR)


if __name__ == "__main__":
    main()
```

**`video_demo/game.py`**

```python
# video_demo/game.py
"""
Clase 14b — Fondos dinámicos.

Enfoque GAME LOOP (herencia directa de `GameLoop`, sin escenas).

Demuestra:

- `engine.background.ParallaxBackground`: tres capas (cielo, montañas,
  árboles) que se desplazan a distinta velocidad con las flechas.
- `engine.background.FrameBackground`: reproduce la secuencia de fotogramas
  como si fuera un vídeo (un sol moviéndose sobre el mar).
- `engine.particle.ParticleSystem`: lluvia / nieve sobre la escena.

Controles:
    IZQUIERDA / DERECHA -> desplazar el fondo
    V                   -> alternar parallax / "vídeo"
    W                   -> alternar clima: nieve / lluvia / despejado
    B                   -> soltar una ráfaga de partículas (efecto "bounce")
    ESC                 -> salir
"""
import os
import random

import pygame

from engine.game_loop import GameLoop
from engine.background import ParallaxBackground, FrameBackground
from engine.particle import ParticleSystem
from engine.audio import AudioManager
from engine.asset_manager import AssetManager
from engine.shared_assets import sfx_path, music_path

WIDTH = 960
HEIGHT = 600
SCROLL_SPEED = 320.0  # píxeles/segundo al desplazar con las flechas

WEATHER_CYCLE = ["snow", "rain", "clear"]
WEATHER_LABEL = {"snow": "nieve", "rain": "lluvia", "clear": "despejado"}


class VideoDemoGame(GameLoop):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, "Fondos dinamicos (clase 14b)", 60)
        pygame.display.set_caption("Fondos dinamicos — clase 14b")

        self.game_dir = os.path.dirname(os.path.abspath(__file__))
        layers_dir = os.path.join(self.game_dir, "assets", "layers")
        frames_dir = os.path.join(self.game_dir, "assets", "frames")

        # --------------------------- audio ---------------------------- #
        self.audio = AudioManager()
        self.audio.load_sound("bounce", sfx_path("bounce"))
        self.audio.load_sound("click", sfx_path("click"))
        self.audio.load_music(music_path("game"))
        self.audio.play_music(loops=-1, volume=0.4)

        # --------------------------- imágenes ------------------------- #
        self.assets = AssetManager()
        self.assets.load_image("cielo", os.path.join(layers_dir, "cielo.png"))
        self.assets.load_image("montanas", os.path.join(layers_dir, "montanas.png"))
        self.assets.load_image("arboles", os.path.join(layers_dir, "arboles.png"))

        self.parallax = ParallaxBackground()
        self.parallax.add_layer(self.assets.get_image("cielo"), 0.15, 0)
        self.parallax.add_layer(self.assets.get_image("montanas"), 0.5, 0)
        self.parallax.add_layer(self.assets.get_image("arboles"), 1.0, 0)

        # ------------------------ fondo "vídeo" ----------------------- #
        self.frame_bg = FrameBackground(frames_dir, fps=12)

        # -------------------------- partículas ------------------------ #
        self.particles = ParticleSystem()

        # ---------------------------- estado -------------------------- #
        self.mode = "parallax"          # "parallax" | "video"
        self.weather = "snow"
        self.current_fps = 0.0

        self.font = pygame.font.Font(None, 26)
        self.small = pygame.font.Font(None, 22)

    # ------------------------------------------------------------------ #
    #  Eventos
    # ------------------------------------------------------------------ #
    def handle_specific_events(self, event):
        if event.type != pygame.KEYDOWN:
            return
        if event.key in (pygame.K_ESCAPE, pygame.K_q):
            self.running = False
        elif event.key == pygame.K_v:
            self.mode = "video" if self.mode == "parallax" else "parallax"
            self.audio.play_sound("click")
        elif event.key == pygame.K_w:
            self._cycle_weather()
        elif event.key == pygame.K_b:
            self._burst()

    def _cycle_weather(self):
        idx = (WEATHER_CYCLE.index(self.weather) + 1) % len(WEATHER_CYCLE)
        self.weather = WEATHER_CYCLE[idx]
        self.audio.play_sound("click")

    def _burst(self):
        """Pequeña explosión de partículas de colores (demuestra emit)."""
        self.audio.play_sound("bounce")
        self.particles.emit(
            WIDTH // 2, HEIGHT // 2, count=60,
            color=(255, 210, 90), speed=(120, 360), life=(0.4, 0.9),
            size=(2, 6), gravity=500, angle=270, spread=180,
        )

    # ------------------------------------------------------------------ #
    #  Lógica
    # ------------------------------------------------------------------ #
    def update_game_logic(self):
        dt = 1.0 / self.fps
        keys = pygame.key.get_pressed()

        # Desplazamiento del parallax con las flechas.
        dx = 0.0
        if keys[pygame.K_RIGHT]:
            dx += SCROLL_SPEED * dt
        if keys[pygame.K_LEFT]:
            dx -= SCROLL_SPEED * dt
        self.parallax.update(dx)

        # El "vídeo" avanza siempre (para que retome donde iba al volver).
        self.frame_bg.update(dt)

        self._spawn_weather()
        self.particles.update(dt)

        self.current_fps = self.clock.get_fps()

    def _spawn_weather(self):
        if self.weather == "rain":
            self.particles.emit(
                random.uniform(0, WIDTH), -6, count=3,
                color=(165, 205, 255), speed=(10, 40), life=(0.5, 0.9),
                size=(1, 2), gravity=1500, angle=90, spread=20,
            )
        elif self.weather == "snow":
            self.particles.emit(
                random.uniform(0, WIDTH), -6, count=2,
                color=(242, 246, 255), speed=(4, 20), life=(2.5, 4.5),
                size=(2, 4), gravity=28, angle=90, spread=60,
            )

    # ------------------------------------------------------------------ #
    #  Dibujo
    # ------------------------------------------------------------------ #
    def draw_game_elements(self):
        if self.mode == "video":
            self.frame_bg.draw(self.screen)
        else:
            self.parallax.draw(self.screen)

        self.particles.draw(self.screen)
        self._draw_hud()

    def _draw_hud(self):
        mode_label = "'video'" if self.mode == "video" else "parallax"
        lines = [
            f"Modo: {mode_label}   (V alterna)",
            f"Clima: {WEATHER_LABEL[self.weather]}   (W alterna)",
            f"FPS: {self.current_fps:0.1f}",
        ]
        y = 14
        for line in lines:
            shadow = self.font.render(line, True, (0, 0, 0))
            text = self.font.render(line, True, (255, 255, 255))
            self.screen.blit(shadow, (16, y + 2))
            self.screen.blit(text, (14, y))
            y += 28

        controls = "FLECHAS desplazar   V video/parallax   W clima   B rafaga   ESC salir"
        hint = self.small.render(controls, True, (240, 240, 240))
        shadow = self.small.render(controls, True, (0, 0, 0))
        self.screen.blit(shadow, (16, HEIGHT - 26))
        self.screen.blit(hint, (14, HEIGHT - 28))
```

**`video_demo/main.py`**

```python
# video_demo/main.py
"""Ejecutar desde la carpeta 2027 con:  python -m video_demo.main"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from video_demo.game import VideoDemoGame


def main():
    VideoDemoGame().run()


if __name__ == "__main__":
    main()
```

## Controles

`←/→` desplazar, `V` parallax/vídeo, `W` clima, `B` ráfaga.

## Cómo ejecutar

Desde la carpeta `2027/`:

```bash
python -m video_demo.main
```
