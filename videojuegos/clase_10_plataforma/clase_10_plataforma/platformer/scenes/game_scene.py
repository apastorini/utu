import pygame
import os


from engine.ui import Scene
from engine.tilemap import TilemapLoader
from entities import Player
from scene.camara import Camera



class GameScene(Scene):
    def __init__(self, game):
        super().__init__(game)

        loader = TilemapLoader(self.game.assets)
        level_path = os.path.join(self.game.game_dir, 'assets', 'sprites', 'nivel_1.json')

        result = loader.load_level(level_path)
        if result is None:
            self.game.running = False;
            return

        self.sprite_groups, world_w, world_h, player_start_pos = result

        # Creamos al jugador en la posición definida en Tiled
        self.jugador = Player(player_start_pos[0], player_start_pos[1], self.game.assets)
        self.sprite_groups["all_sprites"].add(self.jugador)

        self.camara = Camera(self.game.screen.get_width(), self.game.screen.get_height(), world_w, world_h)

    def update(self):
        if not self.game.running: return
        self.sprite_groups["all_sprites"].update(plataformas=self.sprite_groups["collision_sprites"])
        self.camara.update(self.jugador)

    def draw(self, surface):
        if not self.game.running: return
        surface.fill((92, 148, 252))  # Color cielo
        for sprite in self.sprite_groups["all_sprites"]:
            surface.blit(sprite.image, self.camara.apply(sprite))

    def handle_events(self, events):
        pass