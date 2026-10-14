"""
animator/generar_assets.py

Genera la spritesheet del personaje (clase 14 — animación avanzada).
Se dibuja UN mismo humanoide en varias poses con `g.make_humanoid` y se
colocan las celdas en una sola imagen grande ("hoja.png"). Además se escribe
el JSON en el formato que entiende el motor:

    {
      "spritesheet_path": "hoja.png",
      "animations": {
        "idle":  [{"name": "idle_0", "x":0, "y":0, "width":.., "height":..}, ...],
        "walk":  [...],
        "jump":  [...],
        "punch": [...]
      }
    }

Ejecutar una vez desde la carpeta 2027:

    python animator/generar_assets.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

from herramientas import genlib as g  # noqa: E402

OUT = os.path.join(HERE, "assets", "sprites")
SHEET_NAME = "hoja.png"
JSON_NAME = "personaje.json"

# Tamaño de cada celda de la hoja y del personaje base dentro de la celda.
CELL_W = 120
CELL_H = 160
CHAR_W = 80
CHAR_H = 112

COLORS = dict(
    skin=(238, 195, 154, 255),
    shirt=(70, 130, 220, 255),
    pants=(45, 55, 90, 255),
    hair=(60, 35, 20, 255),
)


def _make_pose(pose, dx=0, dy=0, angle=0.0, scale=1.0):
    """Dibuja un humanoide en `pose` y lo centra (abajo) en una celda CELL_W x CELL_H.

    Los pequeños desplazamientos/rotaciones/reescalados generan los distintos
    fotogramas de cada animación a partir de unas pocas poses base.
    """
    char = g.make_humanoid(CHAR_W, CHAR_H, pose=pose, **COLORS)

    if scale != 1.0:
        char = char.resize(
            (max(1, int(CHAR_W * scale)), max(1, int(CHAR_H * scale))),
            g.Image.BICUBIC,
        )
    if angle:
        char = char.rotate(angle, resample=g.Image.BICUBIC, expand=False)

    cell = g.new(CELL_W, CELL_H)
    px = (CELL_W - char.width) // 2 + dx
    py = (CELL_H - char.height) + dy
    cell.paste(char, (px, py), char)
    return cell


def build_animations():
    """Devuelve {nombre_animacion: [celda, celda, ...]}."""
    return {
        # idle: respiración sutil (sube/baja un par de píxeles).
        "idle": [
            _make_pose("idle"),
            _make_pose("idle", dy=-3),
        ],
        # walk: balanceo lateral + leve rotación del cuerpo.
        "walk": [
            _make_pose("walk", dy=0, angle=0),
            _make_pose("walk", dy=-3, angle=-4),
            _make_pose("walk", dy=0, angle=0),
            _make_pose("walk", dy=-3, angle=4),
        ],
        # jump: agacharse, despegar y flotar.
        "jump": [
            _make_pose("jump", dy=6, scale=1.06),
            _make_pose("jump", dy=-6, scale=0.98),
            _make_pose("jump", dy=-12, angle=-6),
        ],
        # punch: preparar, extender el brazo y recoger.
        "punch": [
            _make_pose("idle"),
            _make_pose("punch", dx=6),
            _make_pose("punch", dx=2),
        ],
    }


def main():
    g.ensure_dir(OUT)

    animations = build_animations()
    n_cols = max(len(v) for v in animations.values())
    n_rows = len(animations)

    sheet = g.new(n_cols * CELL_W, n_rows * CELL_H)
    data = {"spritesheet_path": SHEET_NAME, "animations": {}}

    for row, (anim_name, cells) in enumerate(animations.items()):
        frames = []
        for col, cell in enumerate(cells):
            sheet.paste(cell, (col * CELL_W, row * CELL_H), cell)
            frames.append({
                "name": f"{anim_name}_{col}",
                "x": col * CELL_W,
                "y": row * CELL_H,
                "width": CELL_W,
                "height": CELL_H,
            })
        data["animations"][anim_name] = frames

    sheet_path = os.path.join(OUT, SHEET_NAME)
    json_path = os.path.join(OUT, JSON_NAME)
    g.save_png(sheet, sheet_path)
    with open(json_path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2)

    print("Spritesheet:", sheet_path)
    print("JSON:", json_path)
    for anim_name, frames in data["animations"].items():
        print(f"  {anim_name}: {len(frames)} frames")


if __name__ == "__main__":
    main()
