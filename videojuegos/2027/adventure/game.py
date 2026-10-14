# adventure/game.py
"""
La Llave del Destino — aventura gráfica (clases 21-23).

Enfoque de ESCENAS del motor: 'menu' -> 'juego' (habitaciones) -> 'final'.

La escena 'juego' usa las piezas de aventura del motor:
hotspots, inventario, cursor propio y diálogos con opciones.
"""

import os

from engine.game_loop import Game
from engine.asset_manager import AssetManager
from engine.audio import AudioManager
from engine.shared_assets import sfx_path, music_path

from adventure.scenes.menu_scene import MenuScene
from adventure.scenes.juego_scene import JuegoScene
from adventure.scenes.final_scene import FinalScene


class AdventureGame(Game):
    def __init__(self):
        super().__init__(1024, 640, "La Llave del Destino", 60)

        self.game_dir = os.path.dirname(__file__)
        self.assets_dir = os.path.join(self.game_dir, "assets")

        self.assets = AssetManager()
        self.audio = AudioManager()

        self.load_assets()

        # Registramos las escenas por CLASE; el motor las instancia al entrar.
        self.add_scene("menu", MenuScene)
        self.add_scene("juego", JuegoScene)
        self.add_scene("final", FinalScene)
        self.change_scene("menu")

    # ------------------------------------------------------------------ #
    def load_assets(self):
        """Carga fondos, objetos y audio. Si falta algo, se avisa y se sigue."""
        imagenes = {
            "sala": os.path.join(self.assets_dir, "fondos", "sala.png"),
            "biblioteca": os.path.join(self.assets_dir, "fondos", "biblioteca.png"),
            "bodega": os.path.join(self.assets_dir, "fondos", "bodega.png"),
            "llave": os.path.join(self.assets_dir, "objetos", "llave.png"),
            "pocion": os.path.join(self.assets_dir, "objetos", "pocion.png"),
            "puerta": os.path.join(self.assets_dir, "objetos", "puerta.png"),
            "npc": os.path.join(self.assets_dir, "objetos", "npc.png"),
            "titulo": os.path.join(self.assets_dir, "objetos", "titulo.png"),
        }
        for nombre, ruta in imagenes.items():
            try:
                self.assets.load_image(nombre, ruta)
            except Exception as e:  # noqa: BLE001
                print(f"Aviso: no se pudo cargar la imagen '{nombre}': {e}")

        # Sonidos y música compartidos (si no existen, el audio lo ignora).
        for nombre in ("click", "coin", "type", "correct", "wrong"):
            self.audio.load_sound(nombre, sfx_path(nombre))
        self.audio.load_music(music_path("adventure"))
