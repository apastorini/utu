# arkanoid/game.py
import pygame
import os

from arkanoid.scenes.game_scene import GameScene
from arkanoid.scenes.menu_scene import MenuScene
from engine.asset_manager import AssetManager
from engine.audio import AudioManager




class ArkanoidGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Arkanoid Profesional")
        self.clock = pygame.time.Clock()
        self.running = True

        self.game_dir = os.path.dirname(__file__)
        self.assets_dir = os.path.join(self.game_dir, 'assets')  # Apuntamos a 'assets' en general

        # --- CAMBIO CLAVE: Creamos instancias de los gestores ---
        self.assets = AssetManager()
        self.audio_manager = AudioManager()

        self.load_assets()

        if self.running:
            self.setup_scenes()

    def load_assets(self):
        """Ahora también carga los sonidos a través del AudioManager."""
        try:
            sprites_path = os.path.join(self.assets_dir, 'sprites')
            audio_path = os.path.join(self.assets_dir, 'audio')

            # Carga de imágenes y spritesheets
            self.assets.load_spritesheet('main_ss', os.path.join(sprites_path, 'arkanoid.json'))
            self.assets.load_image('ball_img', os.path.join(sprites_path, 'ball.png'))

            # ---  Carga de sonidos ---
            self.audio_manager.load_sound('hit_paddle', os.path.join(audio_path, 'hit_paddle.wav'))
            self.audio_manager.load_sound('hit_brick', os.path.join(audio_path, 'hit_brick.wav'))
            self.audio_manager.load_sound('lose_life', os.path.join(audio_path, 'lose_life.wav'))
            self.audio_manager.load_music(os.path.join(audio_path, 'music.ogg'))

        except Exception as e:
            print(f"Error fatal al cargar assets: {e}")
            self.running = False
    def run(self):
        # 4. El bucle principal delega todo a la escena activa.
        while self.running:
            # ...
            self.current_scene.update()
            self.current_scene.draw(self.screen)
            # ...

    def setup_scenes(self):
        """Crea las instancias de las escenas después de cargar los assets."""
        self.scenes = {
            'menu': MenuScene(self),
            'game': GameScene(self),
            # 'game_over': GameOverScene(self) # Podrías añadir más escenas aquí
        }
        self.current_scene = self.scenes['menu']