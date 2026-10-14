"""
slingshot/generar_assets.py

Genera los gráficos del juego de RESORTERA (clase 20, estilo Angry Birds)
con Pillow. Se ejecuta una sola vez:

    python slingshot/generar_assets.py

Produce en slingshot/assets/sprites/:
  - fondo.png        : cielo + sol + nubes + colinas + suelo
  - pajaro.png       : pájaro redondo enfadado
  - cerdo.png        : cerdo-objetivo verde
  - bloque_madera.png / bloque_piedra.png / bloque_hielo.png
  - resortera.png    : horquilla de madera (la base mira hacia abajo)
  - sombra.png       : sombra suave
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

from herramientas import genlib as g  # noqa: E402

OUT = os.path.join(HERE, "assets", "sprites")

SCREEN_W, SCREEN_H = 1000, 640
GROUND_Y = 560


def make_background():
    np = g.np
    img = g.vgrad(SCREEN_W, SCREEN_H, (92, 170, 235), (196, 228, 248))
    d = g.ImageDraw.Draw(img)

    # Sol con resplandor.
    sx, sy, sr = 830, 110, 54
    for k in range(6, 0, -1):
        rr = sr + k * 9
        d.ellipse([sx - rr, sy - rr, sx + rr, sy + rr],
                  fill=(255, 245, 190, 22))
    d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(255, 236, 140, 255))

    # Nubes.
    for (cx, cy, s) in [(180, 90, 1.1), (430, 60, 0.8), (640, 140, 1.0), (300, 180, 0.6)]:
        for (dx, dy, r) in [(0, 0, 40), (44, 8, 30), (-44, 10, 28), (20, -18, 26)]:
            d.ellipse([cx + dx * s - r * s, cy + dy * s - r * s,
                       cx + dx * s + r * s, cy + dy * s + r * s],
                      fill=(255, 255, 255, 230))

    # Colinas lejanas.
    d.ellipse([-200, GROUND_Y - 210, 420, GROUND_Y + 120], fill=(120, 190, 110, 255))
    d.ellipse([300, GROUND_Y - 260, 900, GROUND_Y + 120], fill=(104, 178, 96, 255))
    d.ellipse([700, GROUND_Y - 190, 1250, GROUND_Y + 120], fill=(120, 190, 110, 255))

    # Suelo de hierba con una franja de tierra.
    d.rectangle([0, GROUND_Y, SCREEN_W, SCREEN_H], fill=(74, 150, 66, 255))
    d.rectangle([0, GROUND_Y, SCREEN_W, GROUND_Y + 10], fill=(96, 178, 84, 255))
    for _ in range(260):
        x = int(np.random.uniform(0, SCREEN_W))
        y = int(np.random.uniform(GROUND_Y + 12, SCREEN_H))
        d.line([(x, y), (x - 3, y + 5)], fill=(58, 120, 52, 255), width=1)
    return img


def make_bird(size=40):
    img = g.new(size, size)
    d = g.ImageDraw.Draw(img)
    cx = cy = size // 2
    r = size // 2 - 2
    # Cuerpo.
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(224, 58, 48, 255),
              outline=(120, 20, 16, 255), width=2)
    # Barriga clara.
    d.ellipse([cx - r * 0.6, cy - r * 0.1, cx + r * 0.6, cy + r * 0.85],
              fill=(245, 224, 210, 255))
    # Cejas enfadadas.
    d.line([(cx - r * 0.75, cy - r * 0.55), (cx - r * 0.15, cy - r * 0.25)],
           fill=(70, 20, 16, 255), width=3)
    d.line([(cx + r * 0.75, cy - r * 0.55), (cx + r * 0.15, cy - r * 0.25)],
           fill=(70, 20, 16, 255), width=3)
    # Ojos.
    for ex in (cx - r * 0.4, cx + r * 0.4):
        d.ellipse([ex - 5, cy - r * 0.35 - 5, ex + 5, cy - r * 0.35 + 5],
                  fill=(255, 255, 255, 255), outline=(60, 40, 30, 255), width=1)
        d.ellipse([ex - 2, cy - r * 0.35 - 2, ex + 2, cy - r * 0.35 + 2],
                  fill=(20, 20, 20, 255))
    # Pico.
    d.polygon([(cx + r * 0.55, cy + r * 0.05), (cx + r * 1.25, cy + r * 0.25),
               (cx + r * 0.55, cy + r * 0.45)], fill=(240, 160, 30, 255),
              outline=(150, 90, 10, 255))
    # Cola.
    d.polygon([(cx - r, cy - r * 0.2), (cx - r * 1.5, cy - r * 0.6),
               (cx - r * 1.5, cy + r * 0.2)], fill=(180, 40, 34, 255))
    return g.add_glow(img, 2, 0.25)


def make_pig(size=44):
    img = g.new(size, size)
    d = g.ImageDraw.Draw(img)
    cx = cy = size // 2
    r = size // 2 - 2
    # Orejas.
    d.polygon([(cx - r * 0.6, cy - r * 0.7), (cx - r * 0.25, cy - r * 1.15),
               (cx - r * 0.05, cy - r * 0.6)], fill=(96, 176, 84, 255))
    d.polygon([(cx + r * 0.6, cy - r * 0.7), (cx + r * 0.25, cy - r * 1.15),
               (cx + r * 0.05, cy - r * 0.6)], fill=(96, 176, 84, 255))
    # Cabeza.
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(120, 200, 100, 255),
              outline=(52, 110, 44, 255), width=2)
    # Hocico.
    d.ellipse([cx - r * 0.42, cy - r * 0.05, cx + r * 0.42, cy + r * 0.5],
              fill=(150, 222, 130, 255), outline=(52, 110, 44, 255), width=1)
    for nx in (cx - r * 0.18, cx + r * 0.18):
        d.ellipse([nx - 2, cy + r * 0.16 - 3, nx + 2, cy + r * 0.16 + 3],
                  fill=(40, 90, 36, 255))
    # Ojos.
    for ex in (cx - r * 0.42, cx + r * 0.42):
        d.ellipse([ex - 4, cy - r * 0.42 - 4, ex + 4, cy - r * 0.42 + 4],
                  fill=(255, 255, 255, 255), outline=(40, 80, 36, 255), width=1)
        d.ellipse([ex - 2, cy - r * 0.42 - 2, ex + 2, cy - r * 0.42 + 2],
                  fill=(20, 40, 20, 255))
    return g.add_glow(img, 2, 0.25)


def make_slingshot(w=78, h=240):
    """Horquilla de madera: base abajo, dos brazos arriba."""
    img = g.new(w, h)
    d = g.ImageDraw.Draw(img)
    wood = (124, 82, 44, 255)
    dark = (74, 46, 24, 255)

    # Tronco (de abajo hacia el centro).
    d.polygon([(w // 2 - 12, h), (w // 2 + 12, h),
               (w // 2 + 8, h * 0.52), (w // 2 - 8, h * 0.52)], fill=wood)
    # Brazo izquierdo.
    d.polygon([(w // 2 - 8, h * 0.55), (w // 2 + 2, h * 0.5),
               (w * 0.28, h * 0.06), (w * 0.16, h * 0.1)], fill=wood)
    # Brazo derecho.
    d.polygon([(w // 2 + 8, h * 0.55), (w // 2 - 2, h * 0.5),
               (w * 0.72, h * 0.06), (w * 0.84, h * 0.1)], fill=wood)
    # Contornos.
    for pts in ([(w // 2 - 12, h), (w // 2 + 12, h),
                 (w // 2 + 8, h * 0.52), (w // 2 - 8, h * 0.52)],
                [(w // 2 - 8, h * 0.55), (w // 2 + 2, h * 0.5),
                 (w * 0.28, h * 0.06), (w * 0.16, h * 0.1)],
                [(w // 2 + 8, h * 0.55), (w // 2 - 2, h * 0.5),
                 (w * 0.72, h * 0.06), (w * 0.84, h * 0.1)]):
        d.line(pts + [pts[0]], fill=dark, width=3)
    # Gomas en las puntas.
    for px in (w * 0.22, w * 0.78):
        d.ellipse([px - 7, h * 0.06 - 7, px + 7, h * 0.06 + 7],
                  fill=(60, 40, 30, 255))
    return img


def make_shadow(w=54, h=22):
    img = g.new(w, h)
    g.ImageDraw.Draw(img).ellipse([0, 0, w - 1, h - 1], fill=(0, 0, 0, 100))
    return img


def main():
    g.ensure_dir(OUT)

    g.save_png(make_background(), os.path.join(OUT, "fondo.png"))
    g.save_png(make_bird(), os.path.join(OUT, "pajaro.png"))
    g.save_png(make_pig(), os.path.join(OUT, "cerdo.png"))
    g.save_png(make_slingshot(), os.path.join(OUT, "resortera.png"))
    g.save_png(make_shadow(), os.path.join(OUT, "sombra.png"))

    blocks = {
        "madera": (150, 105, 60, 255),
        "piedra": (140, 140, 146, 255),
        "hielo": (150, 205, 235, 255),
    }
    for name, color in blocks.items():
        g.save_png(g.make_block(color, 30, 120), os.path.join(OUT, f"bloque_{name}.png"))

    print("Assets de resortera generados en", OUT)


if __name__ == "__main__":
    main()
