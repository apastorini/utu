# arkanoid/scenes/game_scene.py
import pygame
import os
import random
from engine.ui import Scene
from ..entities import Paddle, Ball, Brick, PowerUp
from ..level_loader import load_level_from_file


class GameScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.BLANCO = (255, 255, 255)
        self.AZUL_OSCURO = (13, 20, 56)
        self.ROJO = (255, 0, 0)
        self.font_normal = pygame.font.Font(None, 36)
        self.font_grande = pygame.font.Font(None, 72)

        self.setup_game()

    def setup_game(self):
        # --- CAMBIO CLAVE: Inicializamos las variables de estado PRIMERO ---
        self.estado_juego = 'loading'  # Estado inicial seguro
        self.puntuacion = 0
        self.todos_los_sprites = pygame.sprite.Group()
        self.ladrillos = pygame.sprite.Group()
        self.pelotas = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()

        try:
            # --- Creación de Entidades ---
            pala_img = self.game.assets.get_sprite('main_ss', 'paleta')
            self.pala = Paddle(self.game.screen.get_width() // 2, self.game.screen.get_height() - 40, pala_img)

            bola_img = self.game.assets.get_sprite('main_ss', 'pelota_bocha')
            bola = Ball(self.pala.rect.centerx, self.pala.rect.top - 20, bola_img)

            self.todos_los_sprites.add(self.pala, bola)
            self.pelotas.add(bola)

            level_path = os.path.join(self.game.game_dir, 'levels', 'level_1.txt')
            self.ladrillos = load_level_from_file(level_path, self.game.assets)
            self.todos_los_sprites.add(self.ladrillos)

            # Si todo ha ido bien, el juego puede empezar
            self.estado_juego = 'jugando'

        except (ValueError, KeyError) as e:
            print("\n" + "=" * 60)
            print("ERROR FATAL en 'setup_game': No se encontró un nombre de sprite en el JSON.")
            print(f"Detalle: {e}")
            if 'main_ss' in self.game.assets.spritesheets:
                print("\n--- Sprites Disponibles en 'arkanoid.json' ---")
                spritesheet_data = self.game.assets.spritesheets['main_ss'].data
                available_names = [sprite['name'] for anim in spritesheet_data['animations'].values() for sprite in
                                   anim]
                for name in sorted(available_names): print(f"- {name}")
                print("-------------------------------------------------------")
            print("=" * 60 + "\n")
            self.game.running = False

    def handle_events(self, events):
        if self.estado_juego in ('game_over', 'victoria'):
            for event in events:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.game.change_scene('menu')

    def update(self):
        if self.estado_juego != 'jugando':
            return

        self.todos_los_sprites.update(self.game.screen.get_width(), self.game.screen.get_height())

        for bola in self.pelotas:
            if bola.rect.colliderect(self.pala.rect):
                bola.velocidad_y *= -1;
                bola.rect.bottom = self.pala.rect.top
            ladrillos_golpeados = pygame.sprite.spritecollide(bola, self.ladrillos, False)
            if ladrillos_golpeados:
                ladrillo = ladrillos_golpeados[0]
                bola.velocidad_y *= -1
                if ladrillo.hit():
                    ladrillo.kill();
                    self.puntuacion += ladrillo.value
                    if random.random() < 0.25:
                        try:
                            powerup_img = self.game.assets.get_sprite('main_ss', 'sprite_24')
                            nuevo_powerup = PowerUp(ladrillo.rect.centerx, ladrillo.rect.centery, powerup_img, 'grow')
                            self.powerups.add(nuevo_powerup);
                            self.todos_los_sprites.add(nuevo_powerup)
                        except (ValueError, KeyError):
                            pass

        powerups_cogidos = pygame.sprite.spritecollide(self.pala, self.powerups, True)
        for powerup in powerups_cogidos:
            powerup.activate(self.pala, self.pelotas, self.todos_los_sprites, self.game.assets)

        for bola in self.pelotas.copy():
            if bola.rect.top > self.game.screen.get_height(): bola.kill()

        if not self.pelotas: self.estado_juego = 'game_over'
        if not self.ladrillos: self.estado_juego = 'victoria'

    def draw(self, surface):
        surface.fill(self.AZUL_OSCURO)
        self.todos_los_sprites.draw(surface)

        texto_puntuacion = self.font_normal.render(f"Puntuación: {self.puntuacion}", True, self.BLANCO)
        surface.blit(texto_puntuacion, (10, 10))

        if self.estado_juego == 'game_over':
            self.draw_end_screen(surface, "GAME OVER", "Presiona ESPACIO para volver al menú")
        elif self.estado_juego == 'victoria':
            self.draw_end_screen(surface, "¡VICTORIA!", f"Puntuación Final: {self.puntuacion}")

    def draw_end_screen(self, surface, title, subtitle):
        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180));
        surface.blit(overlay, (0, 0))
        title_surf = self.font_grande.render(title, True, self.BLANCO)
        subtitle_surf = self.font_normal.render(subtitle, True, self.BLANCO)
        title_rect = title_surf.get_rect(centerx=surface.get_width() / 2, centery=surface.get_height() / 2 - 40)
        subtitle_rect = subtitle_surf.get_rect(centerx=surface.get_width() / 2, centery=surface.get_height() / 2 + 20)
        surface.blit(title_surf, title_rect);
        surface.blit(subtitle_surf, subtitle_rect)