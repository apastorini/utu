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
