"""
soccer_rpg/generar_assets.py

Genera los gráficos del RPG de fútbol (clase 26):
campo, balón, jugadores de distintos colores/roles e iconos de acción.
Ejecutar UNA vez:

    python soccer_rpg/generar_assets.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

from herramientas import genlib as g  # noqa: E402

OUT = os.path.join(HERE, "assets", "sprites")

W, H = 900, 600


def make_campo(w=W, h=H):
    """Campo horizontal con gradiente, líneas y áreas."""
    img = g.new(w, h)
    bg = g.vgrad(w, h, (34, 118, 60), (22, 84, 46))
    img = g.Image.alpha_composite(img, bg)
    d = g.ImageDraw.Draw(img)

    stripe = w // 10
    for i in range(11):
        if i % 2 == 0:
            d.rectangle([i * stripe, 0, i * stripe + stripe, h],
                        fill=(44, 140, 70, 70))

    m = 26
    d.rectangle([m, m, w - m, h - m], outline=(240, 240, 240, 210), width=4)
    d.line([(w // 2, m), (w // 2, h - m)], fill=(240, 240, 240, 210), width=4)
    r = 76
    d.ellipse([w // 2 - r, h // 2 - r, w // 2 + r, h // 2 + r],
              outline=(240, 240, 240, 210), width=4)
    d.ellipse([w // 2 - 6, h // 2 - 6, w // 2 + 6, h // 2 + 6],
              fill=(240, 240, 240, 210))
    # Áreas laterales
    aw, ah = 100, 300
    d.rectangle([m, h // 2 - ah // 2, m + aw, h // 2 + ah // 2],
                outline=(240, 240, 240, 210), width=4)
    d.rectangle([w - m - aw, h // 2 - ah // 2, w - m, h // 2 + ah // 2],
                outline=(240, 240, 240, 210), width=4)
    return img


def make_balon(r=16):
    img = g.make_ball((250, 250, 250, 255), r)
    d = g.ImageDraw.Draw(img)
    size = r * 2
    for fx, fy in [(0.5, 0.34), (0.32, 0.62), (0.68, 0.62)]:
        cx, cy = int(size * fx), int(size * fy)
        pr = max(2, r // 4)
        d.ellipse([cx - pr, cy - pr, cx + pr, cy + pr], fill=(30, 30, 30, 255))
    return img


def _icon(size, color, draw_fn):
    img = g.new(size, size)
    d = g.ImageDraw.Draw(img)
    d.rounded_rectangle([1, 1, size - 2, size - 2], radius=8,
                        fill=color, outline=(20, 20, 30, 255), width=2)
    draw_fn(d, size)
    return img


def icono_ataque(size=56):
    """Flecha hacia arriba-derecha (remate)."""
    color = (210, 70, 70, 255)

    def fn(d, s):
        c = s // 2
        d.polygon([(c, 10), (s - 12, c), (c + 8, c), (c + 8, s - 12),
                   (c - 8, s - 12), (c - 8, c), (12, c)], fill=(255, 235, 235, 255))
    return _icon(size, color, fn)


def icono_pase(size=56):
    """Dos flechas cruzadas (pase)."""
    color = (70, 120, 220, 255)

    def fn(d, s):
        d.line([(14, s - 16), (s - 16, 14)], fill=(235, 240, 255, 255), width=6)
        d.polygon([(s - 12, 8), (s - 8, s - 20), (s - 20, s - 12)],
                  fill=(235, 240, 255, 255))
    return _icon(size, color, fn)


def icono_defensa(size=56):
    """Escudo (defensa)."""
    color = (60, 170, 100, 255)

    def fn(d, s):
        c = s // 2
        d.polygon([(c, 10), (s - 12, 18), (s - 14, c + 6),
                   (c, s - 10), (14, c + 6), (12, 18)],
                  fill=(235, 255, 240, 255))
    return _icon(size, color, fn)


def main():
    g.ensure_dir(OUT)

    g.save_png(make_campo(), os.path.join(OUT, "campo.png"))
    g.save_png(make_balon(), os.path.join(OUT, "balon.png"))

    skin = (232, 194, 158, 255)
    delantero = dict(skin=skin, shirt=(225, 60, 60, 255),
                     pants=(60, 30, 30, 255), hair=(30, 20, 15, 255))
    medio = dict(skin=skin, shirt=(60, 110, 230, 255),
                 pants=(25, 40, 90, 255), hair=(20, 25, 35, 255))
    defensor = dict(skin=skin, shirt=(60, 180, 110, 255),
                    pants=(20, 70, 45, 255), hair=(35, 25, 15, 255))

    g.save_png(g.make_humanoid(80, 116, pose="idle", **delantero),
               os.path.join(OUT, "jugador_delantero.png"))
    g.save_png(g.make_humanoid(80, 116, pose="idle", **medio),
               os.path.join(OUT, "jugador_mediocampista.png"))
    g.save_png(g.make_humanoid(80, 116, pose="idle", **defensor),
               os.path.join(OUT, "jugador_defensor.png"))
    g.save_png(g.make_humanoid(80, 116, pose="kick", **delantero),
               os.path.join(OUT, "jugador_delantero_kick.png"))

    g.save_png(icono_ataque(), os.path.join(OUT, "icono_ataque.png"))
    g.save_png(icono_pase(), os.path.join(OUT, "icono_pase.png"))
    g.save_png(icono_defensa(), os.path.join(OUT, "icono_defensa.png"))

    g.save_png(g.text_image("SOCCER RPG", 56, (255, 240, 120, 255)),
               os.path.join(OUT, "logo.png"))

    print("Assets de soccer_rpg generados en", OUT)


if __name__ == "__main__":
    main()
