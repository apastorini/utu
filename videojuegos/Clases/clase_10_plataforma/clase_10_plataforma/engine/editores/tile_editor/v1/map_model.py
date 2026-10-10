# map_model.py
import os
import math
import json
from PIL import Image


class MapModel:
    """Gestiona todos los datos y la lógica del mapa, sin interfaz de usuario."""

    def __init__(self):
        self.all_tiles = {}
        self.tile_hashes = {}
        self.gid_counter = 0
        self.layers = []
        self.properties = {}
        self.file_path = None
        self.reset()

    def reset(self):
        self.all_tiles.clear()
        self.tile_hashes.clear()
        self.gid_counter = 0
        self.layers = []
        self.properties = {"width_pixels": 800, "height_pixels": 600}
        self.add_layer("Capa de Fondo", layer_type='tilelayer', tile_size=32)

    def add_layer(self, name, layer_type='tilelayer', tile_size=32, image_path=None):
        if any(l['name'] == name for l in self.layers):
            raise ValueError(f"El nombre de capa '{name}' ya existe.")

        new_layer = {"name": name, "type": layer_type, "visible": True, "blocking": False}

        if layer_type == "tilelayer":
            width_in_tiles = self.properties['width_pixels'] // tile_size
            height_in_tiles = self.properties['height_pixels'] // tile_size
            tile_data = {"gid": -1, "blocking": False}
            new_layer.update({"tile_size": tile_size,
                              "data": [[tile_data.copy() for _ in range(width_in_tiles)] for _ in
                                       range(height_in_tiles)]})
        elif layer_type == 'imagelayer':
            new_layer.update({"image_path": image_path, "offset": [0, 0]})
        elif layer_type == 'objectgroup':
            new_layer["data"] = []

        self.layers.append(new_layer)
        return new_layer

    def remove_layer(self, index):
        if 0 <= index < len(self.layers):
            del self.layers[index]

    def move_layer(self, index, direction):
        new_index = index + direction
        if 0 <= index < len(self.layers) and 0 <= new_index < len(self.layers):
            self.layers.insert(new_index, self.layers.pop(index))
            return new_index
        return index

    def process_image_for_palette(self, path, tile_size):
        img = Image.open(path).convert("RGBA")
        new_tiles_found = 0
        for y in range(0, img.height, tile_size):
            for x in range(0, img.width, tile_size):
                tile = img.crop((x, y, x + tile_size, y + tile_size))
                if tile.getbbox() is None: continue

                tile_hash = hash(tile.tobytes())
                if tile_hash not in self.tile_hashes.values():
                    self.gid_counter += 1
                    gid = self.gid_counter
                    self.tile_hashes[gid] = tile_hash
                    self.all_tiles[gid] = tile
                    new_tiles_found += 1
        return new_tiles_found

    def paint_tile(self, layer_index, grid_x, grid_y, gid):
        if not (0 <= layer_index < len(self.layers)): return False
        layer = self.layers[layer_index]
        if layer['type'] != 'tilelayer': return False

        width_in_tiles = len(layer['data'][0]) if layer.get('data') else 0
        height_in_tiles = len(layer.get('data', []))

        if 0 <= grid_x < width_in_tiles and 0 <= grid_y < height_in_tiles:
            if layer['data'][grid_y][grid_x]['gid'] != gid:
                layer['data'][grid_y][grid_x]['gid'] = gid
                return True
        return False

    def toggle_tile_blocking(self, layer_index, grid_x, grid_y):
        if not (0 <= layer_index < len(self.layers)): return False
        layer = self.layers[layer_index]
        if layer['type'] != 'tilelayer': return False
        width_in_tiles = len(layer['data'][0]) if layer.get('data') else 0
        height_in_tiles = len(layer.get('data', []))
        if 0 <= grid_x < width_in_tiles and 0 <= grid_y < height_in_tiles:
            layer['data'][grid_y][grid_x]['blocking'] = not layer['data'][grid_y][grid_x]['blocking']
            return True
        return False

    def add_object(self, layer_index, x, y, gid):
        if not (0 <= layer_index < len(self.layers)): return
        layer = self.layers[layer_index]
        if layer['type'] != 'objectgroup': return
        layer['data'].append({"gid": gid, "x": x, "y": y})

    def get_save_data(self):
        sorted_tiles = sorted(self.all_tiles.items())
        gid_map = {old_gid: new_gid for new_gid, (old_gid, _) in enumerate(sorted_tiles)}

        tile_size = next((l.get('tile_size', 16) for l in self.layers if l['type'] == 'tilelayer'), 16)
        cols = 16;
        rows = math.ceil(len(sorted_tiles) / cols) if sorted_tiles else 1
        final_tileset_img = Image.new('RGBA', (cols * tile_size, rows * tile_size))

        for new_gid, (old_gid, tile_img) in enumerate(sorted_tiles):
            row, col = divmod(new_gid, cols)
            final_tileset_img.paste(tile_img.resize((tile_size, tile_size)), (col * tile_size, row * tile_size))

        layers_to_save = []
        for layer in self.layers:
            new_layer = layer.copy()
            if new_layer['type'] == 'tilelayer':
                # Guardar el objeto completo, mapeando solo el gid
                new_layer['data'] = [
                    [{'gid': gid_map.get(tile['gid'], -1), 'blocking': tile['blocking']} for tile in row] for row in
                    new_layer['data']]
            elif new_layer['type'] == 'objectgroup':
                new_layer['data'] = [{"gid": gid_map.get(obj['gid'], -1), "x": obj['x'], "y": obj['y']} for obj in
                                     new_layer['data']]
            elif new_layer['type'] == 'imagelayer' and self.file_path and new_layer.get('image_path'):
                json_dir = os.path.dirname(self.file_path)
                try:
                    new_layer['image_path'] = os.path.relpath(new_layer['image_path'], json_dir).replace('\\', '/')
                except ValueError:
                    new_layer['image_path'] = new_layer['image_path']
            layers_to_save.append(new_layer)

        return {"properties": self.properties, "layers": layers_to_save}, final_tileset_img, tile_size

    def load_from_json(self, data, json_path):
        self.reset()
        self.properties = data['properties']
        self.file_path = json_path
        json_dir = os.path.dirname(json_path)

        if 'tileset' in data and 'path' in data['tileset']:
            tileset_path = os.path.join(json_dir, data['tileset']['path'])
            tile_size = data['tileset']['tile_size']
            if not os.path.exists(tileset_path): raise FileNotFoundError(
                f"No se encontró el tileset: {data['tileset']['path']}")
            self.process_image_for_palette(tileset_path, tile_size)
            gid_map_load = {i: gid for i, gid in enumerate(sorted(self.all_tiles.keys()))}
        else:
            gid_map_load = {}

        loaded_layers = data['layers']
        for layer in loaded_layers:
            if layer['type'] == 'tilelayer':
                # Convertir de formato antiguo (int) a nuevo (dict) si es necesario
                if layer['data'] and isinstance(layer['data'][0][0], int):
                    layer['data'] = [[{"gid": gid_map_load.get(gid, -1), "blocking": False} for gid in row] for row in
                                     layer['data']]
                else:  # Formato nuevo
                    layer['data'] = [
                        [{"gid": gid_map_load.get(tile.get('gid', -1), -1), "blocking": tile.get('blocking', False)} for
                         tile in row] for row in layer['data']]

            elif layer['type'] == 'objectgroup':
                layer['data'] = [{"gid": gid_map_load.get(obj.get('gid', -1), -1), "x": obj['x'], "y": obj['y']} for obj
                                 in layer['data']]
            elif layer['type'] == 'imagelayer':
                img_path = layer.get('image_path')
                if img_path and not os.path.isabs(img_path):
                    layer['image_path'] = os.path.normpath(os.path.join(json_dir, img_path))
        self.layers = loaded_layers