"""
video_demo/generar_assets.py

Genera los gráficos de la clase 14b (fondos dinámicos):

- Tres capas de PARALLAX: cielo, montañas y árboles (se repiten en horizontal
  de forma continua para que el bucle no muestre costuras).
- Una SECUENCIA de 24 fotogramas `assets/frames/frame_00.png ... frame_23.png`
  que simula un "vídeo" (un sol que recorre el cielo sobre el mar con olas).

Ejecutar una vez desde la carpeta 2027:

    python video_demo/generar_assets.py
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

from herramientas import genlib as g  # noqa: E402

W, H = 960, 600
LAYERS_DIR = os.path.join(HERE, "assets", "layers")
FRAMES_DIR = os.path.join(HERE, "assets", "frames")
N_FRAMES = 24


# --------------------------------------------------------------------------- #
#  Capas de parallax
# --------------------------------------------------------------------------- #
def make_sky():
    """Cielo con degradado y nubes (se repite en horizontal)."""
    img = g.vgrad(W, H, (110, 175, 235), (205, 232, 255))
    d = g.ImageDraw.Draw(img)
    cloud = (255, 255, 255, 235)
    for cx, cy, s in ((140, 90, 1.0), (520, 150, 0.8), (820, 70, 1.2)):
        # Se dibuja también desplazada ±W para que el borde empalme.
        for dx in (-W, 0, W):
            for k in range(5):
                r = 26 * s
                x = cx + dx - 70 * s + k * 35 * s
                y = cy + (4 if k % 2 else -4) * s
                d.ellipse([x - r, y - r * 0.7, x + r, y + r * 0.7], fill=cloud)
    return img


def make_mountains():
    """Silueta de montañas periódica (frecuencias enteras => sin costura)."""
    img = g.new(W, H)
    d = g.ImageDraw.Draw(img)
    xs = g.np.arange(W)

    def ridge(base, amps):
        h = g.np.full(W, float(base))
        for k, (freq, amp, phase) in enumerate(amps):
            h = h - amp * g.np.sin(2 * math.pi * freq * xs / W + phase)
        return h

    back = ridge(H * 0.70, [(1, 70, 0.5), (3, 35, 1.7), (5, 16, 0.2)])
    pts_back = [(int(x), int(y)) for x, y in zip(xs, back)]
    d.polygon(pts_back + [(W, H), (0, H)], fill=(88, 108, 140, 255))

    front = ridge(H * 0.80, [(1, 95, 2.1), (2, 40, 0.6), (4, 20, 1.1)])
    pts_front = [(int(x), int(y)) for x, y in zip(xs, front)]
    d.polygon(pts_front + [(W, H), (0, H)], fill=(58, 78, 104, 255))
    d.line(pts_front, fill=(90, 112, 140, 255), width=3)
    return img


def make_trees():
    """Árboles repetidos de forma continua en horizontal."""
    img = g.new(W, H)
    d = g.ImageDraw.Draw(img)
    rng = g.np.random.default_rng(7)
    base_y = int(H * 0.82)
    for _ in range(16):
        x = float(rng.uniform(0, W))
        th = float(rng.uniform(70, 130))
        green = tuple(int(c) for c in rng.uniform([24, 70, 32], [56, 130, 66])) + (255,)
        dark = g.shade(green, 0.75)
        for dx in (-W, 0, W):
            tx = int(x + dx)
            d.rectangle([tx - 4, base_y - 10, tx + 4, base_y + 14],
                        fill=(86, 54, 28, 255))
            d.polygon([(tx, base_y - th), (tx - 26, base_y + 4), (tx + 26, base_y + 4)],
                      fill=green)
            d.polygon([(tx, base_y - th * 0.55), (tx - 32, base_y + 8), (tx + 32, base_y + 8)],
                      fill=dark)
    return img


# --------------------------------------------------------------------------- #
#  Secuencia de "vídeo"
# --------------------------------------------------------------------------- #
def _lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def make_frame(i):
    """Fotograma i de N_FRAMES: un sol recorriendo el cielo sobre el mar."""
    t = i / N_FRAMES
    horizon = int(H * 0.60)
    day = math.sin(math.pi * t)  # 0 en los extremos, 1 en el centro.

    top = _lerp((36, 52, 120), (92, 172, 232), day)
    bottom = _lerp((246, 168, 110), (206, 228, 252), day)
    sky = g.vgrad(W, horizon, top + (255,), bottom + (255,))

    sea = g.vgrad(W, H - horizon, (34, 74, 134), (10, 30, 66))

    img = g.new(W, H)
    img.paste(sky, (0, 0))
    img.paste(sea, (0, horizon))
    d = g.ImageDraw.Draw(img)

    # Sol en un arco.
    sun_x = int(W * 0.5 + (t - 0.5) * W * 0.65)
    sun_y = int(horizon - 30 - 230 * math.sin(math.pi * t))
    for r, alpha in ((70, 40), (52, 90), (38, 160)):
        glow = g.new(2 * r, 2 * r)
        g.ImageDraw.Draw(glow).ellipse([0, 0, 2 * r - 1, 2 * r - 1],
                                       fill=(255, 230, 150, alpha))
        img.paste(glow, (sun_x - r, sun_y - r), glow)
    d.ellipse([sun_x - 26, sun_y - 26, sun_x + 26, sun_y + 26],
              fill=(255, 246, 190, 255))

    # Olas del mar: líneas sinusoidales cuya fase cambia con el fotograma.
    sea_h = H - horizon
    for k in range(14):
        y = horizon + 6 + k * (sea_h - 12) / 14.0
        amp = 2 + k * 0.7
        phase = i * 0.6 + k * 0.9
        pts = [(x, int(y + amp * math.sin(2 * math.pi * x / 130.0 + phase)))
               for x in range(0, W + 1, 6)]
        alpha = 120 + k * 6
        d.line(pts, fill=(150, 200, 240, min(255, alpha)), width=2)

    # Reflejo del sol sobre el agua.
    if 0 <= sun_x < W:
        for k in range(10):
            y = horizon + 8 + k * (sea_h - 16) / 10.0
            w = 18 + k * 4
            d.line([(sun_x - w, int(y)), (sun_x + w, int(y))],
                   fill=(255, 240, 190, 150), width=3)

    return img


def main():
    g.ensure_dir(LAYERS_DIR)
    g.ensure_dir(FRAMES_DIR)

    g.save_png(make_sky(), os.path.join(LAYERS_DIR, "cielo.png"))
    g.save_png(make_mountains(), os.path.join(LAYERS_DIR, "montanas.png"))
    g.save_png(make_trees(), os.path.join(LAYERS_DIR, "arboles.png"))

    for i in range(N_FRAMES):
        g.save_png(make_frame(i), os.path.join(FRAMES_DIR, f"frame_{i:02d}.png"))

    print("Capas de parallax en", LAYERS_DIR)
    print(f"{N_FRAMES} fotogramas de video en", FRAMES_DIR)


if __name__ == "__main__":
    main()
