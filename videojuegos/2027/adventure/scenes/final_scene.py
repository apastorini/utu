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
