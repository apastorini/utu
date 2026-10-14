"""
billiards/generar_assets.py

Genera los gráficos del juego de BILLAR (clases 17-19) con Pillow.
Se ejecuta una sola vez:

    python billiards/generar_assets.py

Produce en billiards/assets/sprites/:
  - mesa.png    : fondo + paño verde + bordes de madera + troneras
  - blanca.png  : bola blanca
  - bola_00.png ... bola_14.png : 15 bolas de colores
  - taco.png    : taco (la punta está en el extremo IZQUIERDO)
  - sombra.png  : sombra suave para dar volumen a las bolas
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

from herramientas import genlib as g  # noqa: E402

OUT = os.path.join(HERE, "assets", "sprites")

# --------------------------------------------------------------------------- #
#  Geometría de la mesa (los mismos números están en game.py)
# --------------------------------------------------------------------------- #
SCREEN_W, SCREEN_H = 1000, 640
PLAY_LEFT, PLAY_TOP, PLAY_RIGHT, PLAY_BOTTOM = 110, 100, 890, 540
RAIL = 40
OUTER = (PLAY_LEFT - RAIL, PLAY_TOP - RAIL, PLAY_RIGHT + RAIL, PLAY_BOTTOM + RAIL)
POCKET_R = 26
GAP = 48
BALL_R = 16

BALL_COLORS = [
    (238, 210, 60), (32, 96, 220), (216, 48, 44), (128, 52, 178),
    (242, 142, 34), (34, 150, 66), (150, 40, 40), (26, 26, 30),
    (238, 210, 60), (32, 96, 220), (216, 48, 44), (128, 52, 178),
    (242, 142, 34), (34, 150, 66), (150, 40, 40),
]


def pocket_centers():
    """Centros de las 6 troneras (4 esquinas + 2 centrales)."""
    cx = (PLAY_LEFT + PLAY_RIGHT) / 2
    return [
        (PLAY_LEFT, PLAY_TOP), (cx, PLAY_TOP), (PLAY_RIGHT, PLAY_TOP),
        (PLAY_LEFT, PLAY_BOTTOM), (cx, PLAY_BOTTOM), (PLAY_RIGHT, PLAY_BOTTOM),
    ]


def make_table():
    """Mesa completa: sala oscura + madera + paño verde con troneras."""
    np = g.np
    img = g.vgrad(SCREEN_W, SCREEN_H, (30, 26, 38), (9, 8, 13))
    d = g.ImageDraw.Draw(img)

    ox0, oy0, ox1, oy1 = OUTER

    # Sombra de la mesa sobre el suelo.
    d.rounded_rectangle([ox0 + 8, oy0 + 14, ox1 + 8, oy1 + 14],
                        radius=30, fill=(0, 0, 0, 140))

    # Borde de madera.
    d.rounded_rectangle([ox0, oy0, ox1, oy1], radius=28,
                        fill=(124, 76, 40, 255), outline=(56, 30, 12, 255), width=5)

    # Vetas de la madera.
    for i in range(90):
        yy = oy0 + 6 + int(np.random.uniform(0, (oy1 - oy0) - 12))
        shade = int(np.random.uniform(-22, 22))
        d.line([(ox0 + 8, yy), (ox1 - 8, yy)],
               fill=(124 + shade, 76 + shade // 2, 40 + shade // 3, 90), width=1)

    # Paño verde.
    d.rectangle([PLAY_LEFT, PLAY_TOP, PLAY_RIGHT, PLAY_BOTTOM], fill=(22, 116, 56, 255))

    # Textura (ruido) del paño.
    for _ in range(7000):
        x = int(np.random.uniform(PLAY_LEFT, PLAY_RIGHT))
        y = int(np.random.uniform(PLAY_TOP, PLAY_BOTTOM))
        v = int(np.random.uniform(-16, 16))
        d.point((x, y), fill=(22 + v, 116 + v, 56 + v, 255))

    # Línea central y puntos de saque.
    midx = (PLAY_LEFT + PLAY_RIGHT) / 2
    d.line([(midx, PLAY_TOP), (midx, PLAY_BOTTOM)], fill=(16, 96, 46, 255), width=2)
    d.ellipse([midx - 3, (PLAY_TOP + PLAY_BOTTOM) / 2 - 3,
               midx + 3, (PLAY_TOP + PLAY_BOTTOM) / 2 + 3], fill=(230, 230, 230, 200))

    # Cushion (interior) más oscuro.
    d.rectangle([PLAY_LEFT, PLAY_TOP, PLAY_RIGHT, PLAY_BOTTOM],
                outline=(12, 78, 36, 255), width=4)

    # Diamantes decorativos en la madera.
    for i in range(1, 8):
        x = PLAY_LEFT + (PLAY_RIGHT - PLAY_LEFT) * i / 8
        for yy in (oy0 + RAIL // 2, oy1 - RAIL // 2):
            d.polygon([(x, yy - 5), (x + 5, yy), (x, yy + 5), (x - 5, yy)],
                      fill=(240, 235, 210, 220))
    for j in range(1, 4):
        y = PLAY_TOP + (PLAY_BOTTOM - PLAY_TOP) * j / 4
        for xx in (ox0 + RAIL // 2, ox1 - RAIL // 2):
            d.polygon([(xx, y - 5), (xx + 5, y), (xx, y + 5), (xx - 5, y)],
                      fill=(240, 235, 210, 220))

    # Troneras (agujeros oscuros).
    for (px, py) in pocket_centers():
        r = POCKET_R + 6
        d.ellipse([px - r, py - r, px + r, py + r], fill=(10, 10, 14, 255))
        d.ellipse([px - r, py - r, px + r, py + r],
                  outline=(58, 34, 16, 255), width=3)

    return img


def make_cue(length=270, thickness=14):
    """Taco de billar horizontal. La PUNTA queda en el extremo izquierdo."""
    img = g.new(length, thickness)
    d = g.ImageDraw.Draw(img)
    h = thickness
    # Cuerpo (madera clara, ligeramente cónico).
    d.polygon([(0, h / 2 - 3), (length, h / 2 - 7),
               (length, h / 2 + 7), (0, h / 2 + 3)], fill=(168, 112, 58, 255))
    d.line([(0, h / 2), (length, h / 2)], fill=(198, 150, 92, 255), width=2)
    # Virola blanca.
    d.rectangle([10, h / 2 - 4, 22, h / 2 + 4], fill=(238, 236, 228, 255))
    # Punta azulada.
    d.rectangle([0, h / 2 - 3, 10, h / 2 + 3], fill=(46, 96, 200, 255))
    # Culata.
    d.rectangle([length - 44, h / 2 - 7, length, h / 2 + 7], fill=(64, 36, 20, 255))
    d.line([(length - 44, h / 2 - 7), (length - 44, h / 2 + 7)],
           fill=(230, 220, 200, 255), width=2)
    return img


def make_shadow(w=44, h=26):
    """Sombra elíptica suave."""
    img = g.new(w, h)
    d = g.ImageDraw.Draw(img)
    d.ellipse([0, 0, w - 1, h - 1], fill=(0, 0, 0, 110))
    return img


def main():
    g.ensure_dir(OUT)

    g.save_png(make_table(), os.path.join(OUT, "mesa.png"))

    g.save_png(g.make_ball((248, 248, 242, 255), BALL_R),
               os.path.join(OUT, "blanca.png"))
    for i, color in enumerate(BALL_COLORS):
        g.save_png(g.make_ball(color + (255,), BALL_R),
                   os.path.join(OUT, f"bola_{i:02d}.png"))

    g.save_png(make_cue(), os.path.join(OUT, "taco.png"))
    g.save_png(make_shadow(), os.path.join(OUT, "sombra.png"))

    print("Assets de billar generados en", OUT)


if __name__ == "__main__":
    main()
