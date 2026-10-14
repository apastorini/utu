# platformer/scenes/game_scene.py
import os

import pygame

from engine.ui import Scene
from engine.tilemap import TilemapLoader
from engine.camera import Camera
from platformer.entities import Player, Enemy


class GameScene(Scene):
    def __init__(self, game):
        super().__init__(game)

        loader = TilemapLoader(self.game.assets)
        level_path = os.path.join(self.game.game_dir, "assets", "sprites", "nivel_1.json")

        result = loader.load_level(level_path)
        if result is None or result[0] is None:
            self.game.change_scene("menu")
            return

        self.sprite_groups, self.world_w, self.world_h, player_start = result

        # Jugador
        self.jugador = Player(player_start[0], player_start[1], self.game.assets)
        self.sprite_groups["all_sprites"].add(self.jugador)

        # Enemigos a partir de los marcadores del tilemap (si los hay)
        self.enemigos = pygame.sprite.Group()
        for spawn in self.sprite_groups.get("spawns", []):
            if spawn.kind == "enemy":
                enemigo = Enemy(spawn.rect.x, spawn.rect.y)
                self.enemigos.add(enemigo)
                self.sprite_groups["all_sprites"].add(enemigo)

        self.camara = Camera(self.game.screen.get_width(),
                             self.game.screen.get_height(),
                             self.world_w, self.world_h)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.game.change_scene("menu")

    def update(self):
        plataformas = self.sprite_groups["collision_sprites"]
        self.sprite_groups["all_sprites"].update(plataformas=plataformas)
        self.camara.update(self.jugador)

        # ¿Hemos llegado al final del nivel?
        if self.jugador.rect.right >= self.world_w - 64:
            self.game.change_scene("game_over", win=True)

        # ¿Nos ha tocado un enemigo?
        if pygame.sprite.spritecollide(self.jugador, self.enemigos, False):
            self.game.change_scene("game_over", win=False)

        # ¿Nos hemos caído del mundo?
        if self.jugador.rect.top > self.world_h:
            self.game.change_scene("game_over", win=False)

    def draw(self, surface):
        surface.fill((92, 148, 252))  # cielo
        for sprite in self.sprite_groups["all_sprites"]:
            surface.blit(sprite.image, self.camara.apply(sprite))
