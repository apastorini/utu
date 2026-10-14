# soccer_rpg/scenes/partido_scene.py
"""
Escena del partido: una secuencia de "jugadas" RPG.

En cada jugada elegís una ACCIÓN (ataque / pase / defensa). El resultado se
calcula con tus atributos + azar, mostrando el desenlace, gastando o
reponiendo energía y ganando XP. Al terminar todas las jugadas se pasa a
la escena 'resumen'.
"""
import random

import pygame

from engine.ui import Scene, Button
from engine.ui_elements import Label, Panel, ProgressBar
from soccer_rpg.roles import ROLES

TOTAL_JUGADAS = 8

COSTES = {"ataque": 22, "pase": 10, "defensa": 14}
REGEN = 8


class PartidoScene(Scene):
    def __init__(self, game, rol="Delantero"):
        super().__init__(game)
        self.rol = rol
        self.datos = ROLES.get(rol, ROLES["Delantero"])

        self.max_energia = 100
        self.energia = float(self.datos["energia"])
        self.xp = 0
        self.goles_favor = 0
        self.goles_contra = 0

        self.jugada = 0
        self.estado = "accion"      # accion | resultado
        self.timer = 0.0
        self.mensaje = "Elegi tu accion para la jugada."
        self.ultimo_exito = True
        self.bonus_ataque = 0.0
        self.accion_actual = None

        self.font = pygame.font.Font(None, 32)
        self.font_chico = pygame.font.Font(None, 24)
        self.font_titulo = pygame.font.Font(None, 48)

        self.barra_energia = ProgressBar((30, 544, 260, 22), 100, self.energia,
                                         (240, 200, 60))
        self.barra_xp = ProgressBar((900 - 290, 544, 260, 22), 100, 0,
                                    (120, 190, 255))

        self.botones = {
            "ataque": Button(160, 470, 180, 54, f"Ataque (-{COSTES['ataque']})",
                             lambda: self.elegir_accion("ataque"), font_size=28,
                             color=(150, 50, 50), hover_color=(195, 70, 70)),
            "pase": Button(360, 470, 180, 54, f"Pase (-{COSTES['pase']})",
                           lambda: self.elegir_accion("pase"), font_size=28,
                           color=(45, 75, 150), hover_color=(70, 110, 200)),
            "defensa": Button(560, 470, 180, 54, f"Defensa (-{COSTES['defensa']})",
                              lambda: self.elegir_accion("defensa"), font_size=28,
                              color=(40, 120, 75), hover_color=(60, 165, 105)),
        }

        self.estadio_pelota = pygame.Vector2(450, 300)

    # ------------------------------------------------------------------ #
    def on_enter(self):
        self.game.audio.play_music(volume=0.4)
        self.game.audio.play_sound("whistle")

    # ------------------------------------------------------------------ #
    def elegir_accion(self, accion):
        if self.estado != "accion":
            return
        self.accion_actual = accion
        coste = COSTES[accion]

        # La energía insuficiente penaliza la efectividad.
        penalizacion = 0.0
        if self.energia < coste:
            penalizacion = 0.35
        self.energia = max(0.0, self.energia - coste)

        factor = self._factor(accion) - penalizacion
        prob = min(0.92, max(0.15, 0.25 + 0.65 * factor))
        exito = random.random() < prob

        self._resolver(accion, exito)

        # Reponer energía y cerrar la jugada.
        self.energia = min(self.max_energia, self.energia + REGEN)
        self.jugada += 1
        self.estado = "resultado"
        self.timer = 1.5

    def _factor(self, accion):
        atk = self.datos["ataque"] / 100.0
        dfc = self.datos["defensa"] / 100.0
        if accion == "ataque":
            return atk + self.bonus_ataque
        if accion == "defensa":
            return dfc
        return (atk + dfc) / 2.0

    def _resolver(self, accion, exito):
        self.ultimo_exito = exito
        if accion == "ataque":
            if exito:
                self.goles_favor += 1
                self.xp += 35
                self.mensaje = "¡GOLAZO! Definiste como un crack."
                self.game.audio.play_sound("kick")
                self.game.audio.play_sound("correct")
                self.game.audio.play_sound("cheer")
                self.bonus_ataque = 0.0
            else:
                self.xp += 8
                self.mensaje = "El arquero la saco del angulo. ¡Casi!"
                self.game.audio.play_sound("wrong")
                if random.random() < 0.30:
                    self.goles_contra += 1
                    self.mensaje += " Y encima te convirtieron de contra."
                    self.game.audio.play_sound("wrong")

        elif accion == "pase":
            if exito:
                self.xp += 22
                self.bonus_ataque = 0.12
                self.mensaje = "Gran pase filtrado: tu equipo llega con ventaja."
                self.game.audio.play_sound("correct")
            else:
                self.xp += 5
                self.bonus_ataque = 0.0
                self.mensaje = "El pase salio largo y se perdio la pelota."
                self.game.audio.play_sound("wrong")
                if random.random() < 0.25:
                    self.goles_contra += 1
                    self.mensaje += " El rival lo aprovecho y anoto."
                    self.game.audio.play_sound("wrong")

        else:  # defensa
            if exito:
                self.xp += 26
                self.mensaje = "¡Barriste el ataque rival con solvencia!"
                self.game.audio.play_sound("correct")
            else:
                self.xp += 8
                self.goles_contra += 1
                self.mensaje = "Te superaron en el duelo... gol del rival."
                self.game.audio.play_sound("wrong")

        # Marcar la pelota (efecto visual sencillo)
        self.estadio_pelota.update(450, 300 + (-40 if exito else 40))

    # ------------------------------------------------------------------ #
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.change_scene("menu")
                    return
                if self.estado == "accion":
                    if event.key in (pygame.K_1, pygame.K_a):
                        self.elegir_accion("ataque")
                    elif event.key in (pygame.K_2, pygame.K_p):
                        self.elegir_accion("pase")
                    elif event.key in (pygame.K_3, pygame.K_d):
                        self.elegir_accion("defensa")
            if self.estado == "accion":
                for boton in self.botones.values():
                    boton.handle_event(event)

    def update(self):
        dt = 1.0 / self.game.fps
        self.estadio_pelota += (pygame.Vector2(450, 300) - self.estadio_pelota) * min(1.0, dt * 4)

        self.barra_energia.set(self.energia)
        self.barra_xp.maximum = 100
        self.barra_xp.set(self.xp % 100)

        if self.estado == "resultado":
            self.timer -= dt
            if self.timer <= 0:
                if self.jugada >= TOTAL_JUGADAS:
                    self.game.change_scene(
                        "resumen",
                        rol=self.rol,
                        goles_favor=self.goles_favor,
                        goles_contra=self.goles_contra,
                        xp=self.xp,
                        energia=self.energia,
                    )
                else:
                    self.estado = "accion"
                    self.mensaje = "Elegi tu accion para la jugada."

    # ------------------------------------------------------------------ #
    def _blit(self, surface, nombre, **kwargs):
        try:
            img = self.game.assets.get_image(nombre)
            surface.blit(img, img.get_rect(**kwargs))
        except Exception:
            pass

    def draw(self, surface):
        w, h = surface.get_size()
        try:
            surface.blit(self.game.assets.get_image("campo"), (0, 0))
        except Exception:
            surface.fill((25, 100, 55))

        # Jugador (sprite del rol)
        sprite_rol = self.datos.get("sprite", "jugador_delantero")
        if self.estado == "resultado" and self.accion_actual == "ataque" and self.ultimo_exito:
            sprite_rol += "_kick"
        self._blit(surface, sprite_rol, midbottom=(250, 430))

        self._blit(surface, "balon", center=(int(self.estadio_pelota.x),
                                             int(self.estadio_pelota.y)))

        # Rival sencillo (icono de defensa)
        self._blit(surface, "icono_defensa", center=(650, 300))

        # HUD superior
        Panel((16, 12, w - 32, 74), color=(10, 15, 25, 190),
              border=(240, 240, 240, 200)).draw(surface)
        Label(f"Rol: {self.rol}", (30, 24), size=30, color=(255, 255, 255)).draw(surface)
        Label(f"Jugada {min(self.jugada + (0 if self.estado == 'resultado' else 1), TOTAL_JUGADAS)}"
              f"/{TOTAL_JUGADAS}", (w // 2, 24), size=30,
              color=(255, 240, 140), align="midtop").draw(surface)
        Label(f"XP {self.xp}  |  Nivel {1 + self.xp // 100}",
              (w - 30, 24), size=30, color=(160, 210, 255),
              align="topright").draw(surface)

        # Marcador
        marcador = Label(f"TU EQUIPO {self.goles_favor} - {self.goles_contra} RIVAL",
                         (w // 2, 100), size=34, color=(255, 255, 255),
                         align="midtop")
        marcador.draw(surface)

        # Mensaje de la jugada
        color = (140, 240, 150) if self.ultimo_exito else (255, 160, 150)
        if self.estado == "accion":
            color = (230, 230, 230)
        msg = self.font.render(self.mensaje, True, color)
        surface.blit(msg, msg.get_rect(centerx=w // 2, y=140))

        # Barras
        self.barra_energia.draw(surface)
        self.barra_xp.draw(surface)
        Label("Energia", (30, 568), size=22, color=(255, 240, 200)).draw(surface)
        Label("XP", (900 - 290, 568), size=22, color=(200, 225, 255)).draw(surface)

        # Botones de acción
        for boton in self.botones.values():
            boton.draw(surface)

        # Iconos descriptivos sobre los botones
        self._blit(surface, "icono_ataque", center=(250, 452))
        self._blit(surface, "icono_pase", center=(450, 452))
        self._blit(surface, "icono_defensa", center=(650, 452))

        ayuda = self.font_chico.render(
            "1/A ataque   2/P pase   3/D defensa   ESC menu",
            True, (235, 235, 235))
        surface.blit(ayuda, (12, h - 22))
