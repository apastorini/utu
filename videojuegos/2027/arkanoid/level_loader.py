# arkanoid/level_loader.py
import pygame

from arkanoid.entities import Brick

# Mapeo carácter -> (nombre de sprite en arkanoid.json, vidas)
BRICK_MAP = {
    "G": {"name": "bloque_gris", "health": 1},
    "M": {"name": "bloque_marron", "health": 2},
    "A": {"name": "bloque_azul", "health": 3},
    "S": {"name": "sprite_11", "health": 1},
}

BRICK_WIDTH, BRICK_HEIGHT = 32, 16
OFFSET_X, OFFSET_Y = 120, 80


def load_level_from_file(file_path, assets):
    """Carga un nivel desde un archivo de texto y devuelve un grupo de ladrillos."""
    ladrillos = pygame.sprite.Group()

    with open(file_path, encoding="utf-8") as f:
        for j, line in enumerate(f):
            for i, char in enumerate(line.strip()):
                if char not in BRICK_MAP:
                    continue
                data = BRICK_MAP[char]
                try:
                    brick_img = assets.get_sprite("main_ss", data["name"])
                    x = i * (BRICK_WIDTH + 4) + OFFSET_X
                    y = j * (BRICK_HEIGHT + 4) + OFFSET_Y
                    ladrillos.add(
                        Brick(x, y, brick_img, assets, data["health"], data["name"])
                    )
                except (ValueError, KeyError) as e:
                    print(f"Error al crear ladrillo desde el nivel: {e}")

    return ladrillos
