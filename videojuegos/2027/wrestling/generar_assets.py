"""
wrestling/generar_assets.py

Genera los gráficos del juego de lucha libre isométrica (clase 13).
Ejecutar una vez:

    python wrestling/generar_assets.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

from herramientas import genlib as g  # noqa: E402

OUT = os.path.join(HERE, "assets", "sprites")


def make_ring_screen(w=1000, h=700, n=7, tile_w=96, tile_h=48):
    """Arena isométrica completa (fondo + cuadrilátero + cuerdas + público)."""
    np = g.np
    img = g.new(w, h)
    # Fondo: pabellón oscuro con público (puntitos)
    bg = g.vgrad(w, h, (20, 16, 40), (40, 20, 60))
    d = g.ImageDraw.Draw(bg)
    for _ in range(1400):
        x = int(np.random.uniform(0, w))
        y = int(np.random.uniform(0, h * 0.55))
        r = int(np.random.uniform(1, 3))
        c = tuple(int(v) for v in np.random.uniform(60, 200, 3))
        d.ellipse([x, y, x + r, y + r], fill=c + (255,))
    img = g.Image.alpha_composite(img, bg)
    d = g.ImageDraw.Draw(img)

    ox, oy = w // 2, 150

    def iso(gx, gy):
        return (ox + (gx - gy) * (tile_w / 2), oy + (gx + gy) * (tile_h / 2))

    # Plataforma (lona) con grosor
    top = [iso(0, 0), iso(n, 0), iso(n, n), iso(0, n)]
    thickness = 46
    left = [iso(0, n), iso(n, n), (iso(n, n)[0], iso(n, n)[1] + thickness),
            (iso(0, n)[0], iso(0, n)[1] + thickness)]
    right = [iso(n, n), iso(n, 0), (iso(n, 0)[0], iso(n, 0)[1] + thickness),
             (iso(n, n)[0], iso(n, n)[1] + thickness)]
    d.polygon(left, fill=(120, 30, 40, 255), outline=(0, 0, 0, 255))
    d.polygon(right, fill=(150, 40, 50, 255), outline=(0, 0, 0, 255))
    # lona
    d.polygon(top, fill=(220, 210, 200, 255), outline=(90, 90, 90, 255))
    # cuadros de la lona
    for i in range(n + 1):
        d.line([iso(i, 0), iso(i, n)], fill=(200, 190, 180, 255))
        d.line([iso(0, i), iso(n, i)], fill=(200, 190, 180, 255))
    # círculo central
    cx, cy = iso(n / 2, n / 2)
    for rr in (90, 60):
        d.ellipse([cx - rr * 1.4, cy - rr * 0.7, cx + rr * 1.4, cy + rr * 0.7],
                  outline=(180, 40, 50, 255), width=4)

    # Postes y cuerdas en las 4 esquinas
    corners = [iso(0, 0), iso(n, 0), iso(n, n), iso(0, n)]
    post_h = 150
    for (px, py) in corners:
        d.rectangle([px - 6, py - post_h, px + 6, py], fill=(60, 60, 70, 255),
                    outline=(0, 0, 0, 255), width=2)
    rope_colors = [(240, 240, 240, 255), (240, 60, 60, 255), (60, 80, 240, 255)]
    for level in range(3):
        yy = int(post_h * (0.35 + level * 0.28))
        pts = [(px, py - yy) for (px, py) in corners]
        d.line(pts + [pts[0]], fill=rope_colors[level], width=4, joint="curve")
    return img


def main():
    g.ensure_dir(OUT)

    g.save_png(make_ring_screen(), os.path.join(OUT, "ring.png"))

    skin = (230, 190, 150, 255)
    rojo = dict(skin=skin, shirt=(210, 50, 50, 255),
                pants=(140, 30, 30, 255), hair=(30, 20, 10, 255))
    azul = dict(skin=skin, shirt=(60, 110, 230, 255),
                pants=(30, 60, 150, 255), hair=(20, 20, 30, 255))
    for name, colors in (("rojo", rojo), ("azul", azul)):
        g.save_png(g.make_humanoid(72, 104, pose="idle", **colors),
                   os.path.join(OUT, f"luchador_{name}_idle.png"))
        g.save_png(g.make_humanoid(72, 104, pose="punch", **colors),
                   os.path.join(OUT, f"luchador_{name}_punch.png"))

    # Sombra
    sh = g.new(72, 28)
    g.ImageDraw.Draw(sh).ellipse([0, 0, 71, 27], fill=(0, 0, 0, 120))
    g.save_png(sh, os.path.join(OUT, "sombra.png"))

    # Logo
    g.save_png(g.text_image("LUCHA ISO", 72, (255, 220, 90, 255)),
               os.path.join(OUT, "logo.png"))
    print("Assets de wrestling generados en", OUT)


if __name__ == "__main__":
    main()
