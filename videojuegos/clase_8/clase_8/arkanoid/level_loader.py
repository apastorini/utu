# arkanoid/level_loader.py
import pygame  # Añadimos esta importación
from .entities import Brick


def load_level_from_file(file_path, assets):
    """Carga un nivel desde un archivo de texto y devuelve un grupo de sprites."""
    ladrillos = pygame.sprite.Group()

    # Mapeo de caracteres a nombres de sprites de tu arkanoid.json y vidas
    brick_map = {
        'G': {'name': 'bloque_gris', 'health': 1},
        'M': {'name': 'bloque_marron', 'health': 2},
        'A': {'name': 'bloque_azul', 'health': 3},
        'S': {'name': 'sprite_11', 'health': 1},  # Ejemplo con un sprite genérico
    }

    brick_width, brick_height = 32, 16

    with open(file_path, 'r') as f:
        for j, line in enumerate(f):
            for i, char in enumerate(line.strip()):
                if char in brick_map:
                    data = brick_map[char]
                    sprite_name = data['name']
                    health = data['health']

                    try:
                        brick_img = assets.get_sprite('main_ss', sprite_name)
                        x = i * (brick_width + 4) + 120
                        y = j * (brick_height + 4) + 80

                        # --- CAMBIO CLAVE: Pasamos el 'sprite_name' al constructor ---
                        ladrillo = Brick(x, y, brick_img, assets, health, sprite_name)
                        ladrillos.add(ladrillo)
                    except (ValueError, KeyError) as e:
                        print(f"Error al crear ladrillo desde el nivel: {e}")

    return ladrillos