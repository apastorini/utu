# arkanoid/game.py
import os

from engine.game_loop import Game
from engine.asset_manager import AssetManager
from engine.audio import AudioManager
from arkanoid.scenes.menu_scene import MenuScene
from arkanoid.scenes.game_scene import GameScene
from arkanoid.scenes.game_over_scene import GameOverScene


class ArkanoidGame(Game):
    """
    Arkanoid usando el enfoque de ESCENAS:
    'menu' -> 'game' (niveles) -> 'game_over'
    """

    def __init__(self):
        super().__init__(800, 600, "Arkanoid", 60)

        self.game_dir = os.path.dirname(__file__)
        self.assets_dir = os.path.join(self.game_dir, "assets")

        self.assets = AssetManager()
        self.audio = AudioManager()
        self.puntuacion = 0

        self.load_assets()

        # Registramos las escenas (clases, no instancias).
        self.add_scene("menu", MenuScene)
        self.add_scene("game", GameScene)
        self.add_scene("game_over", GameOverScene)
        self.change_scene("menu")

    def load_assets(self):
        """Carga imágenes, spritesheets y sonidos del Arkanoid."""
        sprites_path = os.path.join(self.assets_dir, "sprites")
        audio_path = os.path.join(self.assets_dir, "audio")

        try:
            self.assets.load_spritesheet("main_ss", os.path.join(sprites_path, "arkanoid.json"))
            self.assets.load_image("ball_img", os.path.join(sprites_path, "ball.png"))
        except Exception as e:
            print(f"Error fatal al cargar imágenes: {e}")
            self.running = False

        # El audio es opcional: si falta un archivo, seguimos jugando.
        self.audio.load_sound("hit_paddle", os.path.join(audio_path, "hit_paddle.wav"))
        self.audio.load_sound("hit_brick", os.path.join(audio_path, "hit_brick.wav"))
        self.audio.load_sound("lose_life", os.path.join(audio_path, "lose_life.wav"))
        self.audio.load_music(os.path.join(audio_path, "music.mp3"))
