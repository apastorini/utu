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
