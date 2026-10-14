# soccer_rpg/scenes/seleccion_scene.py
"""
Escena de selección de ROL.
Cada rol fija los atributos ataque/defensa/energía del jugador.
"""
import pygame

from engine.ui import Scene, Button
from engine.ui_elements import Label, Panel, ProgressBar
from soccer_rpg.roles import ROLES

_ORDEN = ["Delantero", "Mediocampista", "Defensor"]


class SeleccionScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.font_titulo = pygame.font.Font(None, 60)
        self.font = pygame.font.Font(None, 30)
        self.font_chico = pygame.font.Font(None, 24)

        self.seleccionado = "Delantero"

        self.botones = {}
        x = 40
        for rol in _ORDEN:
            self.botones[rol] = Button(
                x, 470, 250, 56, rol, lambda r=rol: self.elegir(r),
                font_size=32, color=(45, 55, 85), hover_color=(70, 85, 130))
            x += 280

        self.barras = {
            "ataque": ProgressBar((620, 240, 220, 22), 100, 50, (220, 70, 70)),
            "defensa": ProgressBar((620, 300, 220, 22), 100, 50, (70, 180, 100)),
            "energia": ProgressBar((620, 360, 220, 22), 100, 100, (80, 150, 240)),
        }

    def on_enter(self):
        self.game.audio.play_music(volume=0.4)

    def elegir(self, rol):
        self.game.audio.play_sound("click")
        self.game.audio.play_sound("whistle")
        self.game.change_scene("partido", rol=rol)

    def handle_events(self, events):
        for event in events:
            for boton in self.botones.values():
                boton.handle_event(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.change_scene("menu")
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    self.elegir(self.seleccionado)
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    self._mover(-1)
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    self._mover(1)

    def _mover(self, paso):
        i = (_ORDEN.index(self.seleccionado) + paso) % len(_ORDEN)
        self.seleccionado = _ORDEN[i]
        self.game.audio.play_sound("click")

    def update(self):
        datos = ROLES[self.seleccionado]
        self.barras["ataque"].set(datos["ataque"])
        self.barras["defensa"].set(datos["defensa"])
        self.barras["energia"].set(datos["energia"])

    def draw(self, surface):
        try:
            surface.blit(self.game.assets.get_image("campo"), (0, 0))
        except Exception:
            surface.fill((25, 100, 55))
        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        surface.blit(overlay, (0, 0))

        titulo = self.font_titulo.render("Elegi tu ROL", True, (255, 255, 255))
        surface.blit(titulo, titulo.get_rect(centerx=surface.get_width() // 2, y=30))

        datos = ROLES[self.seleccionado]

        # Panel del rol actual
        Panel((40, 110, 500, 330), color=(10, 18, 30, 190),
              border=(240, 240, 240, 200)).draw(surface)

        # Sprite del rol
        try:
            sprite = self.game.assets.get_image(datos["sprite"])
            sprite = pygame.transform.smoothscale(sprite, (140, 202))
            surface.blit(sprite, sprite.get_rect(center=(150, 300)))
        except Exception:
            pygame.draw.rect(surface, datos["color"], (80, 200, 140, 200))

        Label(self.seleccionado, (230, 150), size=42,
              color=(255, 255, 255)).draw(surface)
        self._wrap(surface, datos["desc"], 230, 205, 250,
                   self.font_chico, (200, 215, 235))

        # Atributos
        Label("Ataque", (620, 220), size=28, color=(255, 200, 200)).draw(surface)
        Label("Defensa", (620, 280), size=28, color=(200, 255, 210)).draw(surface)
        Label("Energia", (620, 340), size=28, color=(200, 220, 255)).draw(surface)
        for barra in self.barras.values():
            barra.draw(surface)

        # Botones
        for rol, boton in self.botones.items():
            boton.draw(surface)
            if rol == self.seleccionado:
                pygame.draw.rect(surface, (255, 240, 120), boton.rect, 3,
                                 border_radius=8)

        ayuda = self.font_chico.render(
            "Flechas para elegir rol  |  ENTER para confirmar  |  ESC volver",
            True, (230, 230, 230))
        surface.blit(ayuda, (12, surface.get_height() - 26))

    def _wrap(self, surface, texto, x, y, ancho, font, color):
        palabras = texto.split()
        linea = ""
        for palabra in palabras:
            prueba = (linea + " " + palabra).strip()
            if font.size(prueba)[0] > ancho:
                surface.blit(font.render(linea, True, color), (x, y))
                y += font.get_height() + 2
                linea = palabra
            else:
                linea = prueba
        if linea:
            surface.blit(font.render(linea, True, color), (x, y))
