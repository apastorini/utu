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
