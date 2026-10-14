# adventure/generar_assets.py
"""
Genera los gráficos de la aventura gráfica "La Llave del Destino" (clases 21-23).

Dibuja con Pillow (a través de herramientas.genlib):
  - 3 fondos de habitación de 1024x640 (sala, biblioteca y bodega).
  - Objetos: llave, poción y puerta.
  - Un personaje/NPC (el anciano de la sala).
  - El título del juego para el menú.

Ejecutar UNA vez:

    python adventure/generar_assets.py
"""

import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

from herramientas import genlib as g  # noqa: E402

W, H = 1024, 640
OUT_FONDOS = os.path.join(HERE, "assets", "fondos")
OUT_OBJETOS = os.path.join(HERE, "assets", "objetos")

NEGRO = (0, 0, 0, 255)


# --------------------------------------------------------------------------- #
#  Fondos de habitación
# --------------------------------------------------------------------------- #
def make_sala(w=W, h=H):
    """Sala principal cálida: chimenea, cuadro, ventana con luna y alfombra."""
    img = g.vgrad(w, h, (104, 70, 48), (52, 34, 24))
    d = g.ImageDraw.Draw(img)
    horizon = int(h * 0.72)

    # Panel de madera (zócalo alto)
    d.rectangle([0, int(h * 0.52), w, horizon], fill=(66, 44, 30, 255))
    for x in range(0, w, 118):
        d.line([(x, int(h * 0.52)), (x, horizon)], fill=(48, 30, 20, 255), width=3)

    # Suelo con tablas en perspectiva
    d.rectangle([0, horizon, w, h], fill=(80, 54, 36, 255))
    for i in range(-7, 8):
        d.line([(w // 2 + i * 62, horizon), (w // 2 + i * 210, h)],
               fill=(62, 40, 26, 255), width=2)
    for j in range(1, 5):
        yy = horizon + int((h - horizon) * (j / 5.0) ** 1.6)
        d.line([(0, yy), (w, yy)], fill=(58, 38, 25, 255), width=2)

    # Alfombra
    d.ellipse([330, 470, 730, 618], fill=(128, 52, 52, 255),
              outline=(86, 32, 32, 255), width=5)
    d.ellipse([380, 495, 680, 600], outline=(190, 150, 90, 255), width=4)

    # Chimenea con fuego
    d.rectangle([52, 250, 300, horizon + 12], fill=(98, 76, 62, 255),
                outline=(44, 30, 22, 255), width=3)
    d.rectangle([96, 322, 256, horizon + 12], fill=(26, 17, 13, 255))
    for i, (col, rad) in enumerate([((255, 120, 30, 230), 0.55),
                                    ((255, 190, 60, 230), 0.34),
                                    ((255, 240, 160, 220), 0.16)]):
        cx, cy = 176, 430 + i * 12
        d.ellipse([cx - 70 * rad, cy - 40 * rad, cx + 70 * rad, cy + 40 * rad],
                  fill=col)
    d.rectangle([40, 238, 312, 262], fill=(122, 94, 72, 255),
                outline=(44, 30, 22, 255), width=3)

    # Cuadro
    d.rectangle([636, 120, 848, 292], fill=(74, 52, 96, 255),
                outline=(186, 154, 92, 255), width=9)
    d.ellipse([672, 156, 812, 256], fill=(156, 108, 60, 255))
    d.polygon([(654, 284), (742, 176), (830, 284)], fill=(90, 122, 92, 255))

    # Ventana con luna
    d.rectangle([368, 96, 556, 286], fill=(28, 38, 78, 255),
                outline=(92, 62, 40, 255), width=11)
    d.line([(462, 100), (462, 282)], fill=(92, 62, 40, 255), width=8)
    d.line([(372, 190), (552, 190)], fill=(92, 62, 40, 255), width=8)
    d.ellipse([416, 122, 470, 176], fill=(240, 240, 210, 255))
    d.ellipse([404, 118, 452, 164], fill=(28, 38, 78, 255))
    for sx, sy in [(500, 140), (520, 220), (400, 240), (440, 250)]:
        d.ellipse([sx, sy, sx + 3, sy + 3], fill=(230, 230, 255, 255))

    return g.add_glow(img, 1, 0.15)


def make_biblioteca(w=W, h=H):
    """Biblioteca fría con estanterías llenas de libros y una mesa central."""
    img = g.vgrad(w, h, (46, 50, 76), (26, 28, 46))
    d = g.ImageDraw.Draw(img)
    horizon = int(h * 0.74)

    # Suelo
    d.rectangle([0, horizon, w, h], fill=(56, 44, 36, 255))
    for j in range(1, 5):
        yy = horizon + int((h - horizon) * (j / 5.0) ** 1.5)
        d.line([(0, yy), (w, yy)], fill=(42, 32, 26, 255), width=2)

    # Estanterías (dos a los lados)
    for sx in (30, 604, 830):
        d.rectangle([sx, 70, sx + 168, horizon], fill=(74, 56, 40, 255),
                    outline=(40, 28, 20, 255), width=4)
        for shelf in range(4):
            top = 92 + shelf * 92
            d.line([(sx + 4, top + 78), (sx + 164, top + 78)],
                   fill=(40, 28, 20, 255), width=5)
            bx = sx + 10
            while bx < sx + 154:
                bw = random.randint(9, 18)
                bh = random.randint(44, 68)
                color = random.choice([
                    (170, 60, 50), (60, 110, 170), (70, 140, 80),
                    (170, 140, 60), (120, 70, 150), (60, 140, 150),
                ])
                d.rectangle([bx, top + 78 - bh, bx + bw, top + 78],
                            fill=color + (255,), outline=(22, 16, 12, 255))
                bx += bw + 3

    # Mesa central
    d.rectangle([420, 452, 720, 486], fill=(96, 62, 36, 255),
                outline=(50, 32, 18, 255), width=4)
    d.rectangle([446, 486, 470, 574], fill=(78, 50, 30, 255), outline=NEGRO, width=3)
    d.rectangle([670, 486, 694, 574], fill=(78, 50, 30, 255), outline=NEGRO, width=3)
    # Libro abierto sobre la mesa
    d.polygon([(520, 452), (568, 442), (568, 470), (520, 480)],
              fill=(232, 226, 208, 255), outline=(80, 60, 40, 255))
    d.polygon([(568, 442), (616, 452), (616, 480), (568, 470)],
              fill=(214, 206, 188, 255), outline=(80, 60, 40, 255))

    # Candelabro con luz cálida
    for cx in (300, 760):
        d.rectangle([cx - 5, 400, cx + 5, 470], fill=(200, 190, 170, 255))
        d.ellipse([cx - 12, 372, cx + 12, 412], fill=(255, 220, 120, 255))
        d.ellipse([cx - 7, 380, cx + 7, 404], fill=(255, 250, 210, 255))

    return g.add_glow(img, 2, 0.2)


def make_bodega(w=W, h=H):
    """Bodega de piedra con arco de la puerta y barriles."""
    img = g.vgrad(w, h, (60, 60, 70), (30, 30, 36))
    d = g.ImageDraw.Draw(img)

    # Muro de piedra (bloques)
    bh, bw = 58, 128
    for row in range(0, int(h * 0.76) // bh + 1):
        offset = (row % 2) * (bw // 2)
        for col in range(-1, w // bw + 1):
            x = col * bw + offset
            y = row * bh
            shade = random.randint(-12, 12)
            col_rgb = tuple(max(0, min(255, c + shade)) for c in (74, 74, 84))
            d.rectangle([x + 2, y + 2, x + bw - 2, y + bh - 2],
                        fill=col_rgb + (255,), outline=(34, 34, 40, 255), width=3)

    # Suelo de tierra
    horizon = int(h * 0.78)
    d.rectangle([0, horizon, w, h], fill=(58, 50, 42, 255))

    # Hueco/marco de la puerta
    d.rectangle([396, 196, 644, 560], fill=(20, 16, 14, 255))
    d.rectangle([382, 182, 658, 200], fill=(96, 92, 100, 255),
                outline=(40, 38, 44, 255), width=3)
    for px in (386, 650):
        d.rectangle([px, 182, px + 12, 560], fill=(84, 80, 90, 255),
                    outline=(40, 38, 44, 255), width=2)

    # Barriles
    for bx, scale in ((120, 1.0), (238, 0.82)):
        bw2, bh2 = int(72 * scale), int(120 * scale)
        x0, y0 = bx, horizon - bh2 + 30
        d.ellipse([x0, y0, x0 + bw2, y0 + 26], fill=(120, 84, 44, 255),
                  outline=(60, 40, 20, 255), width=3)
        d.rectangle([x0, y0 + 12, x0 + bw2, y0 + bh2], fill=(104, 72, 38, 255),
                    outline=(60, 40, 20, 255), width=3)
        d.ellipse([x0, y0 + bh2 - 14, x0 + bw2, y0 + bh2 + 12],
                  fill=(88, 60, 32, 255), outline=(60, 40, 20, 255), width=3)
        for hy in (y0 + 40, y0 + bh2 - 30):
            d.line([(x0, hy), (x0 + bw2, hy)], fill=(70, 70, 78, 255), width=4)

    return g.add_glow(img, 1, 0.12)


# --------------------------------------------------------------------------- #
#  Objetos
# --------------------------------------------------------------------------- #
def make_llave(size=96):
    """Llave dorada brillante."""
    img = g.new(size, size)
    d = g.ImageDraw.Draw(img)
    oro = (236, 196, 70, 255)
    oro_s = (150, 108, 20, 255)
    # Anillo del mango
    d.ellipse([16, 26, 62, 72], outline=oro, width=12)
    d.ellipse([26, 36, 52, 62], outline=oro_s, width=3)
    # Caña
    d.rectangle([54, 44, 88, 56], fill=oro, outline=oro_s, width=3)
    # Dientes
    d.rectangle([76, 56, 88, 72], fill=oro, outline=oro_s, width=3)
    d.rectangle([64, 56, 74, 66], fill=oro, outline=oro_s, width=2)
    # Brillo
    d.line([(58, 48), (84, 48)], fill=(255, 250, 210, 255), width=2)
    return g.add_glow(img, 4, 0.55)


def make_pocion(w=72, h=92):
    """Poción azul en un frasco con corcho."""
    img = g.new(w, h)
    d = g.ImageDraw.Draw(img)
    cx = w // 2
    # Frasco
    d.polygon([(cx - 12, 20), (cx + 12, 20), (cx + 26, 78), (cx - 26, 78)],
              fill=(200, 225, 235, 220), outline=(70, 90, 110, 255))
    d.ellipse([cx - 26, 60, cx + 26, 90], fill=(200, 225, 235, 220),
              outline=(70, 90, 110, 255), width=3)
    # Líquido
    d.polygon([(cx - 17, 44), (cx + 17, 44), (cx + 24, 74), (cx - 24, 74)],
              fill=(70, 140, 240, 255))
    d.ellipse([cx - 24, 60, cx + 24, 88], fill=(70, 140, 240, 255))
    # Brillo del líquido
    d.line([(cx - 10, 50), (cx - 6, 72)], fill=(170, 220, 255, 200), width=3)
    # Cuello y corcho
    d.rectangle([cx - 8, 12, cx + 8, 24], fill=(190, 210, 220, 230),
                outline=(70, 90, 110, 255), width=2)
    d.rectangle([cx - 11, 2, cx + 11, 14], fill=(150, 106, 60, 255),
                outline=(80, 54, 26, 255), width=2)
    return g.add_glow(img, 3, 0.3)


def make_puerta(w=240, h=350):
    """Puerta de madera cerrada con refuerzos de hierro y pomo."""
    img = g.new(w, h)
    d = g.ImageDraw.Draw(img)
    d.rectangle([0, 0, w - 1, h - 1], fill=(102, 68, 38, 255),
                outline=(52, 34, 18, 255), width=7)
    # Tablones verticales
    for x in range(8, w - 8, 38):
        d.line([(x, 8), (x, h - 8)], fill=(78, 50, 28, 255), width=3)
    # Refuerzos de hierro
    for y in (24, h - 62):
        d.rectangle([12, y, w - 12, y + 26], fill=(74, 74, 84, 255),
                    outline=(32, 32, 38, 255), width=3)
        for rx in range(26, w - 20, 46):
            d.ellipse([rx, y + 8, rx + 8, y + 16], fill=(40, 40, 46, 255))
    # Bisagras
    d.rectangle([-4, 60, 34, 84], fill=(74, 74, 84, 255), outline=(30, 30, 36, 255), width=3)
    d.rectangle([-4, h - 96, 34, h - 72], fill=(74, 74, 84, 255), outline=(30, 30, 36, 255), width=3)
    # Pomo dorado
    d.ellipse([w - 58, h // 2 - 14, w - 24, h // 2 + 14],
              fill=(236, 196, 70, 255), outline=(130, 96, 24, 255), width=4)
    return img


def make_npc(w=140, h=250):
    """El anciano de la sala: humanoides con sombrero y barba."""
    def accessory(d, cx, head_cy, head_r, ww, hh):
        d.polygon([(cx - head_r - 6, head_cy - head_r + 4),
                   (cx + head_r + 6, head_cy - head_r + 4),
                   (cx, head_cy - head_r - 30)],
                  fill=(62, 42, 92, 255), outline=(24, 16, 36, 255))
        d.ellipse([cx - head_r - 10, head_cy - head_r - 4,
                   cx + head_r + 10, head_cy - head_r + 12],
                  fill=(62, 42, 92, 255), outline=(24, 16, 36, 255), width=3)
        d.arc([cx - head_r + 2, head_cy, cx + head_r - 2, head_cy + head_r + 12],
              0, 180, fill=(214, 214, 214, 255), width=8)

    return g.make_humanoid(
        w, h,
        skin=(236, 202, 168, 255),
        shirt=(118, 62, 140, 255),
        pants=(54, 44, 62, 255),
        hair=(216, 216, 216, 255),
        pose="idle",
        accessory=accessory,
    )


# --------------------------------------------------------------------------- #
def main():
    g.ensure_dir(OUT_FONDOS)
    g.ensure_dir(OUT_OBJETOS)

    g.save_png(make_sala(), os.path.join(OUT_FONDOS, "sala.png"))
    g.save_png(make_biblioteca(), os.path.join(OUT_FONDOS, "biblioteca.png"))
    g.save_png(make_bodega(), os.path.join(OUT_FONDOS, "bodega.png"))

    g.save_png(make_llave(), os.path.join(OUT_OBJETOS, "llave.png"))
    g.save_png(make_pocion(), os.path.join(OUT_OBJETOS, "pocion.png"))
    g.save_png(make_puerta(), os.path.join(OUT_OBJETOS, "puerta.png"))
    g.save_png(make_npc(), os.path.join(OUT_OBJETOS, "npc.png"))

    g.save_png(g.text_image("La Llave del Destino", 68, (255, 222, 120, 255)),
               os.path.join(OUT_OBJETOS, "titulo.png"))

    print("Assets de adventure generados en", OUT_FONDOS, "y", OUT_OBJETOS)


if __name__ == "__main__":
    main()
