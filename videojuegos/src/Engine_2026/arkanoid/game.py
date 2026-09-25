# arkanoid/game.py
import pygame
import os
from engine.asset_manager import AssetManager
# ASUMIENDO que tus escenas están en arkanoid/scenes/
from .scenes.menu_scene import MenuScene
from .scenes.game_scene import GameScene


class ArkanoidGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Arkanoid Profesional")
        self.clock = pygame.time.Clock()
        self.running = True

        # --- Inicializamos TODAS las variables de estado aquí ---
        self.game_dir = os.path.dirname(__file__)
        self.assets_dir = os.path.join(self.game_dir, 'assets', 'sprites')
        self.assets = AssetManager()
        self.scenes = {}
        self.current_scene = None  # Se asignará después de cargar los assets

        # --- Carga de assets y configuración de escenas ---
        self.load_assets()

        # Solo si la carga fue exitosa, creamos las escenas
        if self.running:
            self.setup_scenes()

    def load_assets(self):
        try:
            self.assets.load_spritesheet('main_ss', os.path.join(self.assets_dir, 'arkanoid.json'))
            self.assets.load_image('ball_img', os.path.join(self.assets_dir, 'ball.png'))
        except Exception as e:
            print(f"Error fatal al cargar assets: {e}")
            self.running = False

    def setup_scenes(self):
        """Crea las instancias de las escenas después de cargar los assets."""
        self.scenes = {
            'menu': MenuScene(self),
            'game': GameScene(self),
            # 'game_over': GameOverScene(self) # Podrías añadir más escenas aquí
        }
        self.current_scene = self.scenes['menu']

    def run(self):
        # Si la inicialización falló, no hacemos nada.
        if not self.running or self.current_scene is None:
            print("No se pudo iniciar el juego debido a un error de carga.")
            return

        while self.running:
            self.clock.tick(60)

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

            self.current_scene.handle_events(events)
            self.current_scene.update()
            self.current_scene.draw(self.screen)

            pygame.display.flip()

        pygame.quit()

    def change_scene(self, scene_name):
        if scene_name in self.scenes:
            # Re-inicializamos la escena del juego para reiniciar el nivel
            if scene_name == 'game':
                self.scenes['game'] = GameScene(self)
            self.current_scene = self.scenes[scene_name]
        else:
            print(f"Error: Escena '{scene_name}' no encontrada.")