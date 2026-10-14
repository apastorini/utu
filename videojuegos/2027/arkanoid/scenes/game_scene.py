# arkanoid/scenes/game_scene.py
import os
import random

import pygame

from engine.ui import Scene
from arkanoid.entities import Paddle, Ball, PowerUp
from arkanoid.level_loader import load_level_from_file

# Lista ordenada de niveles. Al terminar el último, se gana la partida.
LEVELS = ["level_1.txt", "level_2.txt"]


class GameScene(Scene):
    def __init__(self, game, level_index=0):
        super().__init__(game)
        self.level_index = level_index

        self.BLANCO = (255, 255, 255)
        self.AZUL_OSCURO = (13, 20, 56)
        self.font_normal = pygame.font.Font(None, 36)
        self.font_grande = pygame.font.Font(None, 72)
        self.font_pequena = pygame.font.Font(None, 28)

        self.vidas = 3
        if not hasattr(self.game, "puntuacion"):
            self.game.puntuacion = 0

        self.powerups = pygame.sprite.Group()
        self.setup_level()

    # ------------------------------------------------------------------ #
    def setup_level(self):
        self.todos_los_sprites = pygame.sprite.Group()
        self.ladrillos = pygame.sprite.Group()
        self.pelotas = pygame.sprite.Group()

        pala_img = self.game.assets.get_sprite("main_ss", "paleta")
        self.pala = Paddle(self.game.screen.get_width() // 2,
                           self.game.screen.get_height() - 40, pala_img)

        bola_img = self.game.assets.get_sprite("main_ss", "pelota_bocha")
        self.bola = Ball(self.pala.rect.centerx, self.pala.rect.top - 20, bola_img)

        self.todos_los_sprites.add(self.pala, self.bola)
        self.pelotas.add(self.bola)

        level_path = os.path.join(self.game.game_dir, "levels", LEVELS[self.level_index])
        self.ladrillos = load_level_from_file(level_path, self.game.assets)
        self.todos_los_sprites.add(self.ladrillos)

        self.estado_juego = "jugando"

    # ------------------------------------------------------------------ #
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.game.change_scene("menu")

    def update(self):
        if self.estado_juego != "jugando":
            return

        w, h = self.game.screen.get_size()
        self.todos_los_sprites.update(w, h)

        for bola in self.pelotas:
            # Rebote con la pala
            if bola.rect.colliderect(self.pala.rect) and bola.velocidad_y > 0:
                bola.velocidad_y *= -1
                bola.rect.bottom = self.pala.rect.top
                self.game.audio.play_sound("hit_paddle")

            # Rebote con ladrillos
            golpeados = pygame.sprite.spritecollide(bola, self.ladrillos, False)
            if golpeados:
                ladrillo = golpeados[0]
                bola.velocidad_y *= -1
                if ladrillo.hit():
                    ladrillo.kill()
                    self.game.puntuacion += ladrillo.value
                    self.game.audio.play_sound("hit_brick")
                    if random.random() < 0.25:
                        self._spawn_powerup(ladrillo)

        # Recoger power-ups
        for powerup in pygame.sprite.spritecollide(self.pala, self.powerups, True):
            powerup.activate(self.pala, self.pelotas, self.todos_los_sprites, self.game.assets)

        # Pelotas que caen por debajo de la pantalla
        for bola in self.pelotas.copy():
            if bola.rect.top > self.game.screen.get_height():
                bola.kill()

        if not self.pelotas:
            self._perder_vida()

        if not self.ladrillos:
            self._nivel_completado()

    # ------------------------------------------------------------------ #
    def _spawn_powerup(self, ladrillo):
        try:
            powerup_img = self.game.assets.get_sprite("main_ss", "sprite_24")
            nuevo = PowerUp(ladrillo.rect.centerx, ladrillo.rect.centery,
                            powerup_img, "grow")
            self.powerups.add(nuevo)
            self.todos_los_sprites.add(nuevo)
        except (ValueError, KeyError):
            pass

    def _perder_vida(self):
        self.vidas -= 1
        self.game.audio.play_sound("lose_life")
        if self.vidas <= 0:
            self.game.change_scene("game_over", win=False)
        else:
            # Recolocar la bola sobre la pala y seguir jugando
            self.bola = Ball(self.pala.rect.centerx, self.pala.rect.top - 20,
                             self.game.assets.get_sprite("main_ss", "pelota_bocha"))
            self.pelotas.add(self.bola)
            self.todos_los_sprites.add(self.bola)

    def _nivel_completado(self):
        if self.level_index + 1 < len(LEVELS):
            self.game.change_scene("game", level_index=self.level_index + 1)
        else:
            self.game.change_scene("game_over", win=True)

    # ------------------------------------------------------------------ #
    def draw(self, surface):
        surface.fill(self.AZUL_OSCURO)
        self.todos_los_sprites.draw(surface)

        texto = self.font_normal.render(f"Puntuación: {self.game.puntuacion}", True, self.BLANCO)
        surface.blit(texto, (10, 10))

        vidas = self.font_normal.render(f"Vidas: {self.vidas}", True, self.BLANCO)
        surface.blit(vidas, (surface.get_width() - vidas.get_width() - 10, 10))

        nivel = self.font_pequena.render(f"Nivel {self.level_index + 1}/{len(LEVELS)}", True, self.BLANCO)
        surface.blit(nivel, nivel.get_rect(centerx=surface.get_width() // 2, top=15))
