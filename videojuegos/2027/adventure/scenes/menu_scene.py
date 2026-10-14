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
