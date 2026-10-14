import pygame
import json
import os
import xml.etree.ElementTree as ET
from .game_object import GameObject


class Tile(GameObject):
    """
    Clase que representa un único tile estático en el mapa.
    Hereda de GameObject para tener un 'rect' y una 'image'.
    """

    def __init__(self, x, y, image):
        # Llama al constructor de GameObject, pero lo posiciona por la esquina (topleft)
        super().__init__(x, y, image)
        self.rect = self.image.get_rect(topleft=(x, y))


class TilemapLoader:
    """
    El cargador de niveles. Lee un archivo .json de Tiled, procesa sus capas
    y devuelve grupos de sprites listos para ser usados en el juego.
    """

    def __init__(self, assets_manager):
        self.assets = assets_manager

    def load_level(self, level_json_path):
        """
        Método principal que lee un archivo JSON de Tiled y construye el mundo del juego.
        Devuelve: un diccionario de grupos de sprites, el ancho y alto del mundo, y la posición de inicio del jugador.
        """
        try:
            with open(level_json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error fatal al cargar o leer el archivo de nivel: {e}")
            return None, 0, 0, (0, 0)

        tile_width = data['tilewidth']
        tile_height = data['tileheight']

        # --- 1. Cargar la información y la imagen del Tileset ---
        tileset_info = data['tilesets'][0]
        first_gid = tileset_info['firstgid']
        json_dir = os.path.dirname(level_json_path)

        tileset_image_filename = ""
        tile_properties = {}

        # Tiled puede guardar el tileset en un archivo .tsx externo. Debemos leerlo.
        if 'source' in tileset_info:
            tsx_path = os.path.join(json_dir, tileset_info['source'])
            try:
                tree = ET.parse(tsx_path)
                root = tree.getroot()
                image_node = root.find('image')
                tileset_image_filename = image_node.get('source')

                # Leer propiedades de tiles individuales (ej: un tile específico que sea 'collidable')
                for tile_node in root.findall('tile'):
                    tile_id = int(tile_node.get('id'))
                    props_node = tile_node.find('properties')
                    if props_node is not None:
                        tile_properties[tile_id] = {}
                        for prop_node in props_node.findall('property'):
                            name = prop_node.get('name')
                            value = prop_node.get('value')
                            prop_type = prop_node.get('type', 'string')
                            if prop_type == 'bool':
                                tile_properties[tile_id][name] = (value.lower() == 'true')
                            else:
                                tile_properties[tile_id][name] = value
            except Exception as e:
                print(f"Error al leer el archivo .tsx en '{tsx_path}': {e}")
                return None, 0, 0, (0, 0)

        # Si el tileset está incrustado en el JSON
        elif 'image' in tileset_info:
            tileset_image_filename = tileset_info['image']

        if not tileset_image_filename:
            print("Error: No se pudo encontrar la ruta a la imagen del tileset en los datos de Tiled.")
            return None, 0, 0, (0, 0)

        # Construir la ruta final y cargar la imagen del tileset
        tileset_image_path = os.path.join(json_dir, tileset_image_filename)
        tileset_name = os.path.basename(tileset_image_path)
        self.assets.load_image(tileset_name, tileset_image_path)
        tileset_img = self.assets.get_image(tileset_name)

        # Cortar el tileset en un diccionario de imágenes de tiles
        tiles = {}
        gid = first_gid
        for y in range(0, tileset_img.get_height(), tile_height):
            for x in range(0, tileset_img.get_width(), tile_width):
                if x + tile_width <= tileset_img.get_width() and y + tile_height <= tileset_img.get_height():
                    tiles[gid] = tileset_img.subsurface((x, y, tile_width, tile_height))
                    gid += 1

        # --- 2. Construir las Capas del Nivel ---
        world_width = data['width'] * tile_width
        world_height = data['height'] * tile_height

        sprite_groups = {
            "all_sprites": pygame.sprite.Group(),
            "collision_sprites": pygame.sprite.Group()
        }
        player_start_pos = (150, 150)  # <-- Posición por defecto a prueba de fallos

        for layer in data['layers']:
            # Procesar capas de tiles
            if layer['type'] == 'tilelayer' and 'data' in layer:
                layer_collides = False
                if 'properties' in layer:
                    for prop in layer['properties']:
                        if prop.get('name') == 'collide' and str(prop.get('value')).lower() == 'true':
                            layer_collides = True
                            break

                for i, gid_val in enumerate(layer['data']):
                    if gid_val == 0 or gid_val not in tiles: continue

                    tile_image = tiles[gid_val]
                    pos_x = (i % data['width']) * tile_width
                    pos_y = (i // data['width']) * tile_height

                    tile_sprite = Tile(pos_x, pos_y, tile_image)
                    sprite_groups["all_sprites"].add(tile_sprite)

                    tile_id_in_tileset = gid_val - first_gid
                    tile_collides = tile_properties.get(tile_id_in_tileset, {}).get('collides', False)

                    if layer_collides or tile_collides:
                        sprite_groups["collision_sprites"].add(tile_sprite)

            # Procesar capas de objetos para encontrar al jugador
            elif layer['type'] == 'objectgroup':
                for obj in layer.get('objects', []):
                    if obj.get('name') == 'player_start':
                        player_start_pos = (obj['x'], obj['y'])

        return sprite_groups, world_width, world_height, player_start_pos