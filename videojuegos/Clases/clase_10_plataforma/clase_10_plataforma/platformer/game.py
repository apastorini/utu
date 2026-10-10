import pygame
import os

from dialogue_manager import DialogueManager
from engine.asset_manager import AssetManager
from scenes.game_scene import GameScene
from scenes.menu_scene import MenuScene


class PlatformerGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1024, 768))  # Una pantalla más grande
        pygame.display.set_caption("Plataformero de Mario")
        self.clock = pygame.time.Clock()
        self.running = True

        self.game_dir = os.path.dirname(__file__)
        self.assets_dir = os.path.join(self.game_dir, 'assets', 'sprites')

        self.assets = AssetManager()
        self.dialogue_manager = DialogueManager(self.screen)
        self.load_assets()

        if self.running:
            self.scenes = {'menu': MenuScene(self), 'game': GameScene(self)}
            self.current_scene = self.scenes['menu']

    def load_assets(self):
        try:
            self.assets.load_spritesheet('player_ss', os.path.join(self.assets_dir, 'mario.json'))
        except Exception as e:
            print(f"Error fatal al cargar assets de personajes: {e}")
            self.running = False

    def run(self):
        if not self.running: return
        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT: self.running = False

            self.current_scene.handle_events(events)
            self.current_scene.update()
            self.current_scene.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()

    def change_scene(self, scene_name):
        if scene_name == 'game': self.scenes['game'] = GameScene(self)
        self.current_scene = self.scenes[scene_name]