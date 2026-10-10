import pygame
from engine.ui import Scene, Button

class MenuScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.start_button = Button(300, 300, 200, 50, "Jugar", self.start_game)
        self.font = pygame.font.Font(None, 80)
        self.title = self.font.render("ARKANOID", True, (255, 255, 255))

    def start_game(self):
        self.game.change_scene('game')

    def handle_events(self, events):
        for event in events:
            self.start_button.handle_event(event)

    def draw(self, surface):
        surface.fill((13, 20, 56))
        surface.blit(self.title, self.title.get_rect(centerx=surface.get_width()/2, y=150))
        self.start_button.draw(surface)