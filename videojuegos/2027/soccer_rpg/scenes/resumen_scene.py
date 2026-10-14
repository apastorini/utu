# soccer_rpg/scenes/resumen_scene.py
"""
Escena de resumen: estadísticas del partido y nivel alcanzado.
"""
import pygame

from engine.ui import Scene, Button
from engine.ui_elements import Label, Panel, ProgressBar


class ResumenScene(Scene):
    def __init__(self, game, rol="Delantero", goles_favor=0, goles_contra=0,
                 xp=0, energia=100):
        super().__init__(game)
        self.rol = rol
        self.goles_favor = goles_favor
        self.goles_contra = goles_contra
        self.xp = xp
        self.energia = energia
        self.nivel = 1 + xp // 100
        self.victoria = goles_favor > goles_contra

        self.font_grande = pygame.font.Font(None, 72)
        self.font = pygame.font.Font(None, 34)
        self.font_chico = pygame.font.Font(None, 26)

        self.boton_otra = Button(300, 470, 300, 54, "Jugar otra vez",
                                 self.otra_vez, color=(45, 90, 150),
                                 hover_color=(70, 120, 195))
        self.boton_menu = Button(300, 532, 300, 50, "Volver al menu", self.menu)

        self.barra_xp = ProgressBar((300, 400, 300, 22), 100, xp % 100,
                                    (120, 190, 255))

    def on_enter(self):
        self.game.audio.play_music(volume=0.4)
        if self.victoria:
            self.game.audio.play_sound("cheer")
        else:
            self.game.audio.play_sound("wrong")

    def otra_vez(self):
        self.game.audio.play_sound("click")
        self.game.change_scene("seleccion")

    def menu(self):
        self.game.audio.play_sound("click")
        self.game.change_scene("menu")

    def handle_events(self, events):
        for event in events:
            self.boton_otra.handle_event(event)
            self.boton_menu.handle_event(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.change_scene("menu")
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    self.otra_vez()

    def update(self):
        self.barra_xp.set(self.xp % 100)

    def draw(self, surface):
        surface.fill((12, 24, 40))
        w = surface.get_width()

        titulo = "¡GANASTE!" if self.victoria else ("EMPATE" if
                 self.goles_favor == self.goles_contra else "PERDISTE")
        color = (140, 240, 150) if self.victoria else (
            (255, 230, 140) if self.goles_favor == self.goles_contra
            else (255, 130, 130))
        t = self.font_grande.render(titulo, True, color)
        surface.blit(t, t.get_rect(centerx=w // 2, y=30))

        # Panel de estadísticas
        Panel((250, 130, 400, 250), color=(0, 0, 0, 150),
              border=(240, 240, 240, 220)).draw(surface)

        Label("RESUMEN DEL PARTIDO", (w // 2, 146), size=30,
              color=(200, 220, 255), align="midtop").draw(surface)

        filas = [
            ("Rol", self.rol),
            ("Goles a favor", str(self.goles_favor)),
            ("Goles en contra", str(self.goles_contra)),
            ("Experiencia (XP)", str(self.xp)),
            ("Nivel alcanzado", str(self.nivel)),
            ("Energia final", f"{int(self.energia)}%"),
        ]
        y = 188
        for etiqueta, valor in filas:
            Label(etiqueta, (275, y), size=28, color=(210, 220, 235)).draw(surface)
            Label(valor, (625, y), size=28, color=(255, 240, 180),
                  align="topright").draw(surface)
            y += 30

        Label("Progreso al siguiente nivel", (w // 2, 378), size=24,
              color=(180, 210, 245), align="midtop").draw(surface)
        self.barra_xp.draw(surface)

        self.boton_otra.draw(surface)
        self.boton_menu.draw(surface)
