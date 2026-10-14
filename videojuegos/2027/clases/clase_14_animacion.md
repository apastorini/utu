# Clase 14 — Animación avanzada (timeline y grabación)

Objetivo: **coreografiar** una animación con una línea de tiempo
(`engine/timeline.py`) en vez de llenar el bucle de `if`/`elif`, y
**grabar** la pantalla a PNG/vídeo (`engine/recorder.py`).

El juego de ejemplo es un **animador** (enfoque Game Loop) que
reproduce animaciones de spritesheet, mueve objetos con *tweens* y
graba 3 segundos al pulsar `R`.

## Motor — código completo de los módulos nuevos

**`engine/timeline.py`**

```python
"""
engine/timeline.py

Línea de tiempo para animar valores y disparar eventos en el tiempo.

Se usa en la clase 14 (animación avanzada): permite "coreografiar" una
animación por keyframes sin llenar el bucle de `if`/`elif`.
"""


def linear(t):
    return t


def ease_in(t):
    return t * t


def ease_out(t):
    return 1 - (1 - t) * (1 - t)


def ease_in_out(t):
    return t * t * (3 - 2 * t)


EASINGS = {
    "linear": linear,
    "ease_in": ease_in,
    "ease_out": ease_out,
    "ease_in_out": ease_in_out,
}


class TimelineEvent:
    def __init__(self, time, callback, repeat=False, loop_interval=None):
        self.time = time
        self.callback = callback
        self.repeat = repeat
        self.loop_interval = loop_interval or time
        self.fired = False

    def reset(self):
        self.fired = False


class Tween:
    """Interpola un atributo de un objeto entre dos valores en un rango de tiempo."""

    def __init__(self, obj, attr, start, end, start_time, end_time, easing=None):
        self.obj = obj
        self.attr = attr
        self.start = start
        self.end = end
        self.start_time = start_time
        self.end_time = end_time
        self.easing = easing or linear

    def apply(self, time):
        if time <= self.start_time:
            setattr(self.obj, self.attr, self.start)
        elif time >= self.end_time:
            setattr(self.obj, self.attr, self.end)
        else:
            p = (time - self.start_time) / (self.end_time - self.start_time)
            setattr(self.obj, self.attr, self.start + (self.end - self.start) * self.easing(p))


class Timeline:
    """
    Reloj central. Cada frame se llama a `update(dt)`.

    - `add_tween(...)` interpola atributos.
    - `add_event(t, callback)` dispara funciones en un instante.
    - Si `duration` está definido y `loop=True`, se repite sola.
    """

    def __init__(self, duration=None, loop=False):
        self.time = 0.0
        self.duration = duration
        self.loop = loop
        self.active = True
        self.events = []
        self.tweens = []

    def add_event(self, time, callback, repeat=False):
        self.events.append(TimelineEvent(time, callback, repeat))

    def add_tween(self, obj, attr, start, end, start_time, end_time, easing=None):
        self.tweens.append(Tween(obj, attr, start, end, start_time, end_time, easing))

    def update(self, dt):
        if not self.active:
            return
        self.time += dt

        for tween in self.tweens:
            tween.apply(self.time)

        for event in self.events:
            if event.repeat:
                if self.time >= event.time:
                    event.callback()
                    event.time += event.loop_interval
            elif not event.fired and self.time >= event.time:
                event.callback()
                event.fired = True

        if self.duration is not None and self.time >= self.duration:
            if self.loop:
                self.reset()
            else:
                self.active = False

    def reset(self):
        self.time = 0.0
        self.active = True
        for event in self.events:
            event.reset()
```

**`engine/recorder.py`**

```python
"""
engine/recorder.py

Graba la pantalla del juego como una secuencia de PNG y, si está disponible
FFmpeg, la convierte en vídeo (mp4).

Uso típico (clase 14):
    rec = Recorder("salida", fps=30)
    ...
    rec.capture(self.screen)      # cada frame mientras se graba
    rec.export("animacion.mp4")   # al terminar
"""

import os
import shutil
import subprocess

import pygame


class Recorder:
    def __init__(self, output_dir, fps=30):
        self.output_dir = output_dir
        self.fps = fps
        self.frame = 0
        self.frames_dir = os.path.join(output_dir, "frames")
        os.makedirs(self.frames_dir, exist_ok=True)

    def capture(self, surface):
        """Guarda el frame actual. Devuelve la ruta del PNG."""
        path = os.path.join(self.frames_dir, f"frame_{self.frame:05d}.png")
        pygame.image.save(surface, path)
        self.frame += 1
        return path

    def clear(self):
        """Borra los frames grabados y reinicia el contador."""
        for name in os.listdir(self.frames_dir):
            os.remove(os.path.join(self.frames_dir, name))
        self.frame = 0

    def export(self, filename="video.mp4", fps=None, keep_frames=False):
        """Convierte los frames en vídeo con FFmpeg. Devuelve la ruta o None."""
        ffmpeg = shutil.which("ffmpeg")
        if not ffmpeg:
            print("FFmpeg no está instalado o no está en el PATH: se conservan los PNG.")
            return None

        output_path = os.path.join(self.output_dir, filename)
        cmd = [
            ffmpeg, "-y",
            "-framerate", str(fps or self.fps),
            "-i", os.path.join(self.frames_dir, "frame_%05d.png"),
            "-pix_fmt", "yuv420p",
            output_path,
        ]
        try:
            subprocess.run(cmd, check=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"Vídeo exportado en '{output_path}'")
        except subprocess.CalledProcessError as e:
            print(f"Error al exportar el vídeo: {e}")
            return None

        if not keep_frames:
            self.clear()
        return output_path
```

## Juego de ejemplo — código completo

**`animator/__init__.py`**

```python
"""animator — Clase 14: animación avanzada (timeline, grabación y vídeo)."""
```

**`animator/generar_assets.py`**

```python
"""
animator/generar_assets.py

Genera la spritesheet del personaje (clase 14 — animación avanzada).
Se dibuja UN mismo humanoide en varias poses con `g.make_humanoid` y se
colocan las celdas en una sola imagen grande ("hoja.png"). Además se escribe
el JSON en el formato que entiende el motor:

    {
      "spritesheet_path": "hoja.png",
      "animations": {
        "idle":  [{"name": "idle_0", "x":0, "y":0, "width":.., "height":..}, ...],
        "walk":  [...],
        "jump":  [...],
        "punch": [...]
      }
    }

Ejecutar una vez desde la carpeta 2027:

    python animator/generar_assets.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

from herramientas import genlib as g  # noqa: E402

OUT = os.path.join(HERE, "assets", "sprites")
SHEET_NAME = "hoja.png"
JSON_NAME = "personaje.json"

# Tamaño de cada celda de la hoja y del personaje base dentro de la celda.
CELL_W = 120
CELL_H = 160
CHAR_W = 80
CHAR_H = 112

COLORS = dict(
    skin=(238, 195, 154, 255),
    shirt=(70, 130, 220, 255),
    pants=(45, 55, 90, 255),
    hair=(60, 35, 20, 255),
)


def _make_pose(pose, dx=0, dy=0, angle=0.0, scale=1.0):
    """Dibuja un humanoide en `pose` y lo centra (abajo) en una celda CELL_W x CELL_H.

    Los pequeños desplazamientos/rotaciones/reescalados generan los distintos
    fotogramas de cada animación a partir de unas pocas poses base.
    """
    char = g.make_humanoid(CHAR_W, CHAR_H, pose=pose, **COLORS)

    if scale != 1.0:
        char = char.resize(
            (max(1, int(CHAR_W * scale)), max(1, int(CHAR_H * scale))),
            g.Image.BICUBIC,
        )
    if angle:
        char = char.rotate(angle, resample=g.Image.BICUBIC, expand=False)

    cell = g.new(CELL_W, CELL_H)
    px = (CELL_W - char.width) // 2 + dx
    py = (CELL_H - char.height) + dy
    cell.paste(char, (px, py), char)
    return cell


def build_animations():
    """Devuelve {nombre_animacion: [celda, celda, ...]}."""
    return {
        # idle: respiración sutil (sube/baja un par de píxeles).
        "idle": [
            _make_pose("idle"),
            _make_pose("idle", dy=-3),
        ],
        # walk: balanceo lateral + leve rotación del cuerpo.
        "walk": [
            _make_pose("walk", dy=0, angle=0),
            _make_pose("walk", dy=-3, angle=-4),
            _make_pose("walk", dy=0, angle=0),
            _make_pose("walk", dy=-3, angle=4),
        ],
        # jump: agacharse, despegar y flotar.
        "jump": [
            _make_pose("jump", dy=6, scale=1.06),
            _make_pose("jump", dy=-6, scale=0.98),
            _make_pose("jump", dy=-12, angle=-6),
        ],
        # punch: preparar, extender el brazo y recoger.
        "punch": [
            _make_pose("idle"),
            _make_pose("punch", dx=6),
            _make_pose("punch", dx=2),
        ],
    }


def main():
    g.ensure_dir(OUT)

    animations = build_animations()
    n_cols = max(len(v) for v in animations.values())
    n_rows = len(animations)

    sheet = g.new(n_cols * CELL_W, n_rows * CELL_H)
    data = {"spritesheet_path": SHEET_NAME, "animations": {}}

    for row, (anim_name, cells) in enumerate(animations.items()):
        frames = []
        for col, cell in enumerate(cells):
            sheet.paste(cell, (col * CELL_W, row * CELL_H), cell)
            frames.append({
                "name": f"{anim_name}_{col}",
                "x": col * CELL_W,
                "y": row * CELL_H,
                "width": CELL_W,
                "height": CELL_H,
            })
        data["animations"][anim_name] = frames

    sheet_path = os.path.join(OUT, SHEET_NAME)
    json_path = os.path.join(OUT, JSON_NAME)
    g.save_png(sheet, sheet_path)
    with open(json_path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2)

    print("Spritesheet:", sheet_path)
    print("JSON:", json_path)
    for anim_name, frames in data["animations"].items():
        print(f"  {anim_name}: {len(frames)} frames")


if __name__ == "__main__":
    main()
```

**`animator/game.py`**

```python
# animator/game.py
"""
Clase 14 — Animación avanzada.

Enfoque GAME LOOP (herencia directa de `GameLoop`, sin escenas).

Puntos que demuestra este ejemplo:

- Carga de una spritesheet con JSON (`engine.sprite_sheet.Spritesheet`) y
  reproducción de varias animaciones (idle / walk / jump / punch).
- COREOGRAFÍA con `engine.timeline.Timeline`: tweens de posición y escala
  (el personaje camina, la pelota rebota, el sol gira y late) más EVENTOS
  (rebotes que suenan, un giro del personaje a mitad de ciclo).
- Grabación con `engine.recorder.Recorder`: la tecla R graba 3 segundos y
  exporta a vídeo (si hay FFmpeg; si no, deja los PNG).

Controles:
    1 / 2 / 3 / 4 -> idle / walk / punch / jump
    ESPACIO       -> pausar / reanudar el timeline
    R             -> grabar 3 segundos
    ESC           -> salir
"""
import math
import os

import pygame

from engine.game_loop import GameLoop
from engine.sprite_sheet import Spritesheet
from engine.timeline import Timeline, EASINGS
from engine.recorder import Recorder
from engine.audio import AudioManager
from engine.shared_assets import sfx_path, music_path

WIDTH = 960
HEIGHT = 640
GROUND_Y = 560


class Actor:
    """Personaje animado: posición, escala y fotograma actual."""

    def __init__(self, x, y, anim="idle"):
        self.x = float(x)
        self.y = float(y)
        self.scale = 1.0
        self.anim = anim
        self.frame_index = 0
        self.frame_timer = 0.0
        self.flip = False
        # Valores auxiliares que la Timeline interpola.
        self.walk_x = 0.0

    def set_anim(self, name):
        if name != self.anim:
            self.anim = name
            self.frame_index = 0
            self.frame_timer = 0.0


class Ball:
    """Pelota que rebota: la Timeline interpola `height` (altura sobre el suelo)."""

    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.height = 0.0
        # Dos rampas (subida/bajada) que en el dibujo se combinan con min()
        # para lograr un rebote limpio sin que los tweens se pisen.
        self.height_up = 0.0
        self.height_down = 0.0

    @property
    def paint_height(self):
        return min(self.height_up, self.height_down)


class Sun:
    """Sol giratorio: la Timeline interpola ángulo, altura y escala."""

    def __init__(self, x, base_y):
        self.x = float(x)
        self.base_y = float(base_y)
        self.angle = 0.0
        self.scale = 1.0
        self.height = 0.0
        self.height_up = 0.0
        self.height_down = 0.0
        self.scale_up = 1.0
        self.scale_down = 1.0

    @property
    def paint_height(self):
        return min(self.height_up, self.height_down)

    @property
    def paint_scale(self):
        return min(self.scale_up, self.scale_down)


class AnimatorGame(GameLoop):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, "Animador (clase 14)", 60)
        pygame.display.set_caption("Animador — clase 14")

        self.game_dir = os.path.dirname(os.path.abspath(__file__))
        sprites_dir = os.path.join(self.game_dir, "assets", "sprites")

        # --------------------------- audio ---------------------------- #
        self.audio = AudioManager()
        self.audio.load_sound("click", sfx_path("click"))
        self.audio.load_sound("bounce", sfx_path("bounce"))
        self.audio.load_music(music_path("calm"))
        self.audio.play_music(loops=-1, volume=0.4)

        # --------------------------- sprites -------------------------- #
        self.sheet = Spritesheet(os.path.join(sprites_dir, "personaje.json"))
        self.animations = {
            name: self.sheet.get_animation_frames(name)
            for name in self.sheet.data["animations"]
        }
        self.anim_fps = 8.0

        # --------------------------- objetos -------------------------- #
        self.hero = Actor(160, GROUND_Y, anim="walk")
        self.ball = Ball(690, GROUND_Y)
        self.sun = Sun(810, 150)

        # ------------------------- coreografía ------------------------ #
        self._build_timeline()

        # ------------------------ estado de UI ------------------------ #
        self.paused = False
        self.recording = False
        self.record_timer = 0.0
        self.recorder = None
        self.record_message = ""

        self.font = pygame.font.Font(None, 28)
        self.small = pygame.font.Font(None, 22)
        self.big = pygame.font.Font(None, 40)

        # Fondo precalculado (gradiente).
        self.background = self._make_background()

    # ------------------------------------------------------------------ #
    #  Coreografía (Timeline)
    # ------------------------------------------------------------------ #
    def _build_timeline(self):
        """
        Un único timeline en bucle de 8 s. Como `Tween` fija su valor incluso
        fuera de su rango, usamos atributos distintos para cada tramo y los
        combinamos al dibujar (truco nunca-miente con min()).
        """
        duration = 8.0
        self.timeline = Timeline(duration=duration, loop=True)

        # --- personaje: cruza la pantalla de izquierda a derecha --------- #
        # Empieza y termina FUERA de pantalla, así el salto del bucle no se ve.
        self.hero.x = -120.0
        self.timeline.add_tween(self.hero, "x", -120.0, 1080.0,
                                0.0, duration, easing=EASINGS["linear"])

        # --- pelota: rebota (dos rampas + min) --------------------------- #
        self.ball.height_up = 0.0
        self.ball.height_down = 260.0
        self.timeline.add_tween(self.ball, "height_up", 0.0, 260.0,
                                0.0, 0.75, easing=EASINGS["ease_out"])
        self.timeline.add_tween(self.ball, "height_down", 260.0, 0.0,
                                0.75, 1.5, easing=EASINGS["ease_in"])

        # --- sol: gira, sube/baja y late (posición + escala) ------------- #
        self.sun.height_up = 0.0
        self.sun.height_down = 45.0
        self.sun.scale_up = 1.0
        self.sun.scale_down = 1.35
        self.timeline.add_tween(self.sun, "angle", 0.0, 360.0,
                                0.0, duration, easing=EASINGS["linear"])
        self.timeline.add_tween(self.sun, "height_up", 0.0, 45.0,
                                0.0, 2.0, easing=EASINGS["ease_in_out"])
        self.timeline.add_tween(self.sun, "height_down", 45.0, 0.0,
                                2.0, 4.0, easing=EASINGS["ease_in_out"])
        self.timeline.add_tween(self.sun, "scale_up", 1.0, 1.35,
                                0.0, 2.0, easing=EASINGS["ease_in_out"])
        self.timeline.add_tween(self.sun, "scale_down", 1.35, 1.0,
                                2.0, 4.0, easing=EASINGS["ease_in_out"])

        # --- eventos ----------------------------------------------------- #
        # Rebotes de la pelota: uno cada 0.75 s dentro del ciclo.
        t = 0.75
        while t < duration:
            self.timeline.add_event(t, self._on_bounce)
            t += 0.75
        # Giro del personaje y "click" a mitad de ciclo.
        self.timeline.add_event(duration / 2, self._on_midpoint)

    def _on_bounce(self):
        self.audio.play_sound("bounce")

    def _on_midpoint(self):
        self.hero.flip = not self.hero.flip
        self.audio.play_sound("click")

    # ------------------------------------------------------------------ #
    #  Fondo
    # ------------------------------------------------------------------ #
    def _make_background(self):
        surface = pygame.Surface((WIDTH, HEIGHT))
        top = (32, 44, 84)
        bottom = (120, 170, 220)
        for y in range(HEIGHT):
            t = y / (HEIGHT - 1)
            color = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
            pygame.draw.line(surface, color, (0, y), (WIDTH, y))
        return surface

    # ------------------------------------------------------------------ #
    #  Eventos
    # ------------------------------------------------------------------ #
    def handle_specific_events(self, event):
        if event.type != pygame.KEYDOWN:
            return
        if event.key in (pygame.K_ESCAPE, pygame.K_q):
            self.running = False
        elif event.key == pygame.K_1:
            self.hero.set_anim("idle")
            self.audio.play_sound("click")
        elif event.key == pygame.K_2:
            self.hero.set_anim("walk")
            self.audio.play_sound("click")
        elif event.key == pygame.K_3:
            self.hero.set_anim("punch")
            self.audio.play_sound("click")
        elif event.key == pygame.K_4:
            self.hero.set_anim("jump")
            self.audio.play_sound("click")
        elif event.key == pygame.K_SPACE:
            self.paused = not self.paused
            self.timeline.active = not self.paused
            self.audio.play_sound("click")
        elif event.key == pygame.K_r:
            self.start_recording()

    # ------------------------------------------------------------------ #
    #  Grabación
    # ------------------------------------------------------------------ #
    def start_recording(self):
        if self.recording:
            return
        out_dir = os.path.join(self.game_dir, "grabacion")
        self.recorder = Recorder(out_dir, fps=self.fps)
        self.recorder.clear()
        self.recording = True
        self.record_timer = 3.0
        self.record_message = "grabando..."
        print(f"Grabando 3 s en '{out_dir}' ...")

    def _finish_recording(self):
        self.recording = False
        result = self.recorder.export("animacion.mp4")
        if result:
            self.record_message = "video exportado"
        else:
            self.record_message = "PNG guardados (sin ffmpeg)"
        print(self.record_message)

    # ------------------------------------------------------------------ #
    #  Lógica
    # ------------------------------------------------------------------ #
    def update_game_logic(self):
        dt = 1.0 / self.fps

        self.timeline.update(dt)

        # Avance de fotogramas de la animación actual.
        if not self.paused:
            frames = self.animations[self.hero.anim]
            self.hero.frame_timer += dt
            if self.hero.frame_timer >= 1.0 / self.anim_fps:
                self.hero.frame_timer = 0.0
                self.hero.frame_index = (self.hero.frame_index + 1) % len(frames)

        if self.recording:
            self.record_timer -= dt
            if self.record_timer <= 0:
                self._finish_recording()

    # ------------------------------------------------------------------ #
    #  Dibujo
    # ------------------------------------------------------------------ #
    def draw_game_elements(self):
        self.screen.blit(self.background, (0, 0))

        # Suelo.
        pygame.draw.rect(self.screen, (58, 120, 70),
                         (0, GROUND_Y, WIDTH, HEIGHT - GROUND_Y))
        pygame.draw.line(self.screen, (30, 80, 45),
                         (0, GROUND_Y), (WIDTH, GROUND_Y), 3)

        self._draw_sun()
        self._draw_ball()
        self._draw_hero()
        self._draw_hud()

        if self.recording:
            self.recorder.capture(self.screen)

    def _draw_sun(self):
        cx = int(self.sun.x)
        cy = int(self.sun.base_y - self.sun.paint_height)
        radius = int(34 * self.sun.paint_scale)

        # Rayos giratorios.
        for i in range(12):
            angle = math.radians(self.sun.angle + i * 30)
            x1 = cx + math.cos(angle) * (radius + 6)
            y1 = cy + math.sin(angle) * (radius + 6)
            x2 = cx + math.cos(angle) * (radius + 20)
            y2 = cy + math.sin(angle) * (radius + 20)
            pygame.draw.line(self.screen, (255, 230, 120), (x1, y1), (x2, y2), 4)

        pygame.draw.circle(self.screen, (255, 210, 70), (cx, cy), radius)
        pygame.draw.circle(self.screen, (255, 245, 190), (cx, cy), radius, 3)

    def _draw_ball(self):
        cx = int(self.ball.x)
        cy = int(GROUND_Y - self.ball.paint_height)
        radius = 22

        # Sombra en el suelo (crece cuando la pelota está baja).
        shadow_w = int(40 - self.ball.paint_height * 0.06)
        shadow_w = max(14, shadow_w)
        pygame.draw.ellipse(self.screen, (40, 70, 45),
                            (int(self.ball.x) - shadow_w // 2, GROUND_Y - 6,
                             shadow_w, 10))

        pygame.draw.circle(self.screen, (214, 60, 60), (cx, cy), radius)
        pygame.draw.circle(self.screen, (255, 255, 255),
                           (cx - radius // 3, cy - radius // 3), radius // 3)
        pygame.draw.circle(self.screen, (30, 30, 30), (cx, cy), radius, 2)

    def _draw_hero(self):
        frames = self.animations[self.hero.anim]
        frame = frames[self.hero.frame_index % len(frames)]

        scale = max(0.2, self.hero.scale)
        size = (int(frame.get_width() * scale), int(frame.get_height() * scale))
        image = pygame.transform.smoothscale(frame, size)
        if self.hero.flip:
            image = pygame.transform.flip(image, True, False)

        rect = image.get_rect(midbottom=(int(self.hero.x), GROUND_Y + 2))
        self.screen.blit(image, rect)

    def _draw_hud(self):
        lines = [
            f"Animacion: {self.hero.anim}  (fotograma {self.hero.frame_index})",
            f"Timeline: {'EN PAUSA' if self.paused else 'activo'}   t={self.timeline.time:0.2f}s",
        ]
        if self.recording:
            lines.append(f"REC  {max(0.0, self.record_timer):0.1f}s")
        elif self.record_message:
            lines.append(self.record_message)

        y = 16
        for line in lines:
            text = self.font.render(line, True, (255, 255, 255))
            shadow = self.font.render(line, True, (0, 0, 0))
            self.screen.blit(shadow, (18, y + 2))
            self.screen.blit(text, (16, y))
            y += 30

        controls = "1 idle   2 walk   3 punch   4 jump   ESPACIO pausa   R graba 3s"
        hint = self.small.render(controls, True, (235, 235, 235))
        self.screen.blit(hint, (16, HEIGHT - 28))

        if self.recording:
            pygame.draw.circle(self.screen, (230, 40, 40), (WIDTH - 30, 30), 12)
            pygame.draw.circle(self.screen, (255, 255, 255), (WIDTH - 30, 30), 12, 2)
```

**`animator/main.py`**

```python
# animator/main.py
"""Ejecutar desde la carpeta 2027 con:  python -m animator.main"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from animator.game import AnimatorGame


def main():
    AnimatorGame().run()


if __name__ == "__main__":
    main()
```

## Controles

`1-4` animación, `ESPACIO` pausa, `R` graba 3 s (PNG/MP4).

## Cómo ejecutar

Desde la carpeta `2027/`:

```bash
python -m animator.main
```
