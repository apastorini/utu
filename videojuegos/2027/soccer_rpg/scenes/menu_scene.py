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
