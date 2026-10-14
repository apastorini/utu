# soccer_rpg/game.py
"""
SOCCER RPG — RPG de fútbol por escenas (clase 26).

Enfoque ESCENAS:
    'menu'      -> título y opciones
    'seleccion' -> elegir ROL (Delantero / Mediocampista / Defensor)
    'partido'   -> secuencia de "jugadas" con acciones ataque/pase/defensa
    'resumen'   -> estadísticas y nivel alcanzado

Clase principal: SoccerRpgGame
"""
import os

from engine.game_loop import Game
from engine.asset_manager import AssetManager
from engine.audio import AudioManager
from engine.shared_assets import sfx_path, music_path

from soccer_rpg.scenes.menu_scene import MenuScene
from soccer_rpg.scenes.seleccion_scene import SeleccionScene
from soccer_rpg.scenes.partido_scene import PartidoScene
from soccer_rpg.scenes.resumen_scene import ResumenScene
from soccer_rpg.roles import ROLES  # noqa: F401  (reexport por comodidad)


class SoccerRpgGame(Game):
    def __init__(self):
        super().__init__(900, 600, "Soccer RPG", 60)

        self.game_dir = os.path.dirname(os.path.abspath(__file__))
        self.assets_dir = os.path.join(self.game_dir, "assets", "sprites")

        self.assets = AssetManager()
        self.audio = AudioManager()
        self.load_assets()

        self.add_scene("menu", MenuScene)
        self.add_scene("seleccion", SeleccionScene)
        self.add_scene("partido", PartidoScene)
        self.add_scene("resumen", ResumenScene)
        self.change_scene("menu")

    def load_assets(self):
        imagenes = [
            "campo", "balon", "logo",
            "jugador_delantero", "jugador_mediocampista", "jugador_defensor",
            "jugador_delantero_kick",
            "icono_ataque", "icono_pase", "icono_defensa",
        ]
        for nombre in imagenes:
            try:
                self.assets.load_image(
                    nombre, os.path.join(self.assets_dir, f"{nombre}.png"))
            except Exception as e:  # pragma: no cover
                print(f"Aviso: no se pudo cargar '{nombre}.png': {e}")

        for sonido in ("kick", "whistle", "cheer", "correct", "wrong", "click"):
            self.audio.load_sound(sonido, sfx_path(sonido))
        self.audio.load_music(music_path("soccer"))
