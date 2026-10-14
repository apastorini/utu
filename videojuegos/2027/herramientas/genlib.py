"""
herramientas/genlib.py

Librería para GENERAR assets del curso (no hace falta descargar nada):

- Audio: sintetizador sencillo (ondas + percusión) y un pequeño "tracker"
  para componer música tipo chiptune. Escribe archivos .wav.
- Gráficos: ayudas sobre Pillow (PIL) para dibujar sprites, fondos,
  personajes y tiles; escribe archivos .png.

Todo el audio se guarda en mono, 22050 Hz, 16 bits para que pese poco.
"""

import os
import re
import wave

import numpy as np

# --------------------------------------------------------------------------- #
#  AUDIO
# --------------------------------------------------------------------------- #
SR = 22050

_A4 = 440.0
_NOTE_SEMITONE = {
    "C": 0, "C#": 1, "DB": 1, "D": 2, "D#": 3, "EB": 3, "E": 4, "F": 5,
    "F#": 6, "GB": 6, "G": 7, "G#": 8, "AB": 8, "A": 9, "A#": 10, "BB": 10, "B": 11,
}


def freq(name):
    """'C4' -> 261.6 Hz. Devuelve 0 si name es None/rest."""
    if name is None:
        return 0.0
    m = re.match(r"([A-Ga-g]#?b?)(-?\d)", str(name))
    if not m:
        return 0.0
    note = m.group(1).upper()
    octave = int(m.group(2))
    semitone = _NOTE_SEMITONE.get(note)
    if semitone is None:
        return 0.0
    steps = (octave - 4) * 12 + (semitone - 9)
    return _A4 * (2 ** (steps / 12.0))


def _envelope(n, attack=0.005, release=0.05):
    env = np.ones(n, dtype=np.float32)
    a = min(n, max(1, int(attack * SR)))
    r = min(n, max(1, int(release * SR)))
    env[:a] *= np.linspace(0, 1, a)
    env[-r:] *= np.linspace(1, 0, r)
    return env


def synth(name, dur, wave="square", vol=0.5, attack=0.005, release=0.05):
    """Genera un tono (o percusión) como array float32."""
    if name in ("kick", "snare", "hat", "clap", "tom"):
        return drum(name, vol)

    n = max(1, int(SR * max(dur, 0.01)))
    t = np.arange(n) / SR
    f = float(name) if isinstance(name, (int, float)) else freq(name)
    if f <= 0:
        return np.zeros(n, dtype=np.float32)

    if wave == "sine":
        w = np.sin(2 * np.pi * f * t)
    elif wave == "triangle":
        w = 2 * np.abs(2 * ((f * t) % 1) - 1) - 1
    elif wave == "saw":
        w = 2 * ((f * t) % 1) - 1
    elif wave == "noise":
        w = np.random.uniform(-1, 1, n)
    else:  # square
        w = np.sign(np.sin(2 * np.pi * f * t))
        # suavizado para que no chille tanto
        w = w * 0.7 + np.sin(2 * np.pi * f * t) * 0.3

    return (w * _envelope(n, attack, release) * vol).astype(np.float32)


def drum(kind, vol=0.7):
    if kind == "kick":
        dur = 0.20
        n = int(SR * dur)
        t = np.arange(n) / SR
        f = 130 * np.exp(-t * 32) + 45
        w = np.sin(2 * np.pi * np.cumsum(f) / SR)
        env = np.exp(-t * 16)
        return (w * env * vol).astype(np.float32)
    if kind == "snare":
        dur = 0.18
        n = int(SR * dur)
        t = np.arange(n) / SR
        noise = np.random.uniform(-1, 1, n)
        tone = np.sin(2 * np.pi * 180 * t)
        env = np.exp(-t * 22)
        return ((0.7 * noise + 0.3 * tone) * env * vol).astype(np.float32)
    if kind == "hat":
        dur = 0.06
        n = int(SR * dur)
        t = np.arange(n) / SR
        noise = np.random.uniform(-1, 1, n)
        env = np.exp(-t * 70)
        return (noise * env * vol * 0.5).astype(np.float32)
    if kind == "clap":
        dur = 0.20
        n = int(SR * dur)
        t = np.arange(n) / SR
        noise = np.random.uniform(-1, 1, n)
        env = np.exp(-t * 30) * (1 + 0.5 * np.sin(2 * np.pi * 30 * t))
        return (noise * env * vol * 0.5).astype(np.float32)
    # tom
    dur = 0.25
    n = int(SR * dur)
    t = np.arange(n) / SR
    f = 200 * np.exp(-t * 12) + 80
    w = np.sin(2 * np.pi * np.cumsum(f) / SR)
    return (w * np.exp(-t * 12) * vol).astype(np.float32)


def render_events(events, bpm=120, beats=16, volume=0.9):
    """Mezcla una lista de eventos {'note','beat','dur','wave','vol'}."""
    spb = 60.0 / bpm
    total = int(SR * spb * beats) + SR // 2
    buf = np.zeros(total, dtype=np.float32)
    for ev in events:
        note = ev.get("note")
        if note in (None, "rest"):
            continue
        start = int(SR * ev["beat"] * spb)
        dur = ev.get("dur", 0.5) * spb
        wave = ev.get("wave", "square")
        vol = ev.get("vol", 0.4)
        chunk = synth(note, dur, wave, vol)
        end = min(total, start + len(chunk))
        if start < total:
            buf[start:end] += chunk[: end - start]
    peak = float(np.max(np.abs(buf))) or 1.0
    return (buf / peak * volume).astype(np.float32)


def write_wav(path, samples, sr=SR):
    ensure_dir(os.path.dirname(path))
    data = (np.clip(samples, -1, 1) * 32767).astype("<i2")
    with wave.open(path, "w") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(data.tobytes())


# ----------------------------- Efectos de sonido --------------------------- #
def _env_ar(n, attack, release):
    return _envelope(n, attack, release)


def sfx_blip(f0=880, f1=1320, dur=0.09):
    n = int(SR * dur)
    t = np.arange(n) / SR
    f = np.linspace(f0, f1, n)
    return (np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * _env_ar(n, 0.002, 0.04) * 0.4).astype(np.float32)


def sfx_hit():
    n = int(SR * 0.12)
    t = np.arange(n) / SR
    w = np.random.uniform(-1, 1, n)
    return (w * np.exp(-t * 40) * 0.6).astype(np.float32)


def sfx_jump():
    n = int(SR * 0.18)
    t = np.arange(n) / SR
    f = np.linspace(300, 900, n)
    return (np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 6) * 0.4).astype(np.float32)


def sfx_coin():
    a = synth("B5", 0.06, "square", 0.35)
    b = synth("E6", 0.12, "square", 0.35)
    return np.concatenate([a, b])


def sfx_bounce():
    n = int(SR * 0.12)
    t = np.arange(n) / SR
    f = 500 * np.exp(-t * 20) + 200
    return (np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 20) * 0.5).astype(np.float32)


def sfx_splash():
    n = int(SR * 0.35)
    t = np.arange(n) / SR
    w = np.random.uniform(-1, 1, n)
    return (w * np.exp(-t * 8) * 0.4).astype(np.float32)


def sfx_whistle():
    n = int(SR * 0.4)
    t = np.arange(n) / SR
    f = 1800 + 120 * np.sin(2 * np.pi * 22 * t)
    return (np.sin(2 * np.pi * f * t) * _env_ar(n, 0.01, 0.08) * 0.35).astype(np.float32)


def sfx_cheer():
    n = int(SR * 1.2)
    t = np.arange(n) / SR
    w = np.random.uniform(-1, 1, n)
    env = np.clip(np.sin(np.pi * t / (n / SR)) * 1.5, 0, 1)
    return (w * env * 0.35).astype(np.float32)


def sfx_kick():
    return drum("kick", 0.9)


def sfx_punch():
    a = drum("kick", 0.8)
    b = sfx_hit()
    out = np.zeros(max(len(a), len(b)), dtype=np.float32)
    out[:len(a)] += a
    out[:len(b)] += b * 0.6
    return out


def sfx_explode():
    n = int(SR * 0.5)
    t = np.arange(n) / SR
    w = np.random.uniform(-1, 1, n)
    return (w * np.exp(-t * 6) * 0.6).astype(np.float32)


def sfx_click():
    return synth("A5", 0.04, "square", 0.3)


def sfx_correct():
    return np.concatenate([synth("C5", 0.09, "square", 0.35),
                           synth("E5", 0.09, "square", 0.35),
                           synth("G5", 0.16, "square", 0.35)])


def sfx_wrong():
    return np.concatenate([synth("A3", 0.14, "saw", 0.35),
                           synth("F3", 0.22, "saw", 0.35)])


def sfx_type():
    return synth("D6", 0.02, "square", 0.15)


def sfx_shot():
    n = int(SR * 0.15)
    t = np.arange(n) / SR
    f = np.linspace(1200, 200, n)
    return (np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * np.exp(-t * 14) * 0.4).astype(np.float32)


SFX = {
    "blip": sfx_blip,
    "hit": sfx_hit,
    "jump": sfx_jump,
    "coin": sfx_coin,
    "bounce": sfx_bounce,
    "splash": sfx_splash,
    "whistle": sfx_whistle,
    "cheer": sfx_cheer,
    "kick": sfx_kick,
    "punch": sfx_punch,
    "explode": sfx_explode,
    "click": sfx_click,
    "correct": sfx_correct,
    "wrong": sfx_wrong,
    "type": sfx_type,
    "shot": sfx_shot,
}


# -------------------------------- Música ----------------------------------- #
def _arp(notes, start, step, count, wave="square", vol=0.22):
    return [{"note": notes[i % len(notes)], "beat": start + i * step,
             "dur": step * 0.9, "wave": wave, "vol": vol} for i in range(count)]


def _bassline(notes, start, step, count, wave="triangle", vol=0.35):
    return [{"note": notes[i % len(notes)], "beat": start + i * step,
             "dur": step * 0.95, "wave": wave, "vol": vol} for i in range(count)]


def _beat(bpm, beats, kick_every=2, snare_every=2, hat_every=1):
    events = []
    for b in range(0, int(beats)):
        if hat_every and b % hat_every == 0:
            events.append({"note": "hat", "beat": b, "vol": 0.25})
        if kick_every and b % kick_every == 0:
            events.append({"note": "kick", "beat": b, "vol": 0.6})
        if snare_every and b % snare_every == 1:
            events.append({"note": "snare", "beat": b, "vol": 0.5})
    return events


def music_menu():
    ev = _arp(["C5", "E5", "G5", "E5"], 0, 0.5, 16, "triangle", 0.20)
    ev += _bassline(["C3", "A2", "F2", "G2"], 0, 2, 8, "triangle", 0.32)
    ev += _beat(100, 16, kick_every=4, snare_every=4, hat_every=2)
    return render_events(ev, bpm=100, beats=16)


def music_game():
    ev = _arp(["E5", "G5", "B5", "G5", "A5", "G5", "E5", "D5"], 0, 0.25, 32, "square", 0.18)
    ev += _bassline(["E2", "E2", "A2", "A2", "C3", "C3", "B2", "B2"], 0, 1, 16, "triangle", 0.34)
    ev += _beat(140, 16, kick_every=2, snare_every=2, hat_every=1)
    return render_events(ev, bpm=140, beats=16)


def music_wrestling():
    ev = _arp(["A3", "C4", "E4", "A4", "E4", "C4"], 0, 0.5, 24, "saw", 0.20)
    ev += _bassline(["A2", "A2", "G2", "G2", "F2", "F2", "E2", "E2"], 0, 1, 16, "square", 0.34)
    ev += _beat(132, 16, kick_every=2, snare_every=4, hat_every=1)
    return render_events(ev, bpm=132, beats=16)


def music_soccer():
    ev = _arp(["C5", "E5", "G5", "C6", "G5", "E5"], 0, 0.5, 24, "square", 0.20)
    ev += _bassline(["C3", "C3", "G2", "G2", "F2", "F2", "G2", "G2"], 0, 1, 16, "triangle", 0.34)
    ev += _beat(128, 16, kick_every=2, snare_every=2, hat_every=1)
    return render_events(ev, bpm=128, beats=16)


def music_adventure():
    ev = _arp(["A3", "C4", "E4", "D4", "C4", "B3"], 0, 0.75, 24, "triangle", 0.18)
    ev += _bassline(["A2", "F2", "C3", "G2"], 0, 3, 8, "triangle", 0.30)
    ev += _beat(92, 24, kick_every=6, snare_every=6, hat_every=3)
    return render_events(ev, bpm=92, beats=24)


def music_calm():
    ev = _arp(["C4", "E4", "G4", "B4", "G4", "E4"], 0, 1.0, 16, "triangle", 0.16)
    ev += _bassline(["C3", "A2", "F2", "G2"], 0, 4, 4, "triangle", 0.28)
    return render_events(ev, bpm=80, beats=24)


MUSIC = {
    "menu": music_menu,
    "game": music_game,
    "wrestling": music_wrestling,
    "soccer": music_soccer,
    "adventure": music_adventure,
    "calm": music_calm,
}


# --------------------------------------------------------------------------- #
#  GRÁFICOS (Pillow)
# --------------------------------------------------------------------------- #
from PIL import Image, ImageDraw, ImageFilter, ImageFont  # noqa: E402


def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)


def new(w, h, color=(0, 0, 0, 0)):
    return Image.new("RGBA", (int(w), int(h)), color)


def save_png(img, path):
    ensure_dir(os.path.dirname(path))
    img.save(path)


def vgrad(w, h, top, bottom, alpha=255):
    base = new(w, h)
    d = ImageDraw.Draw(base)
    for y in range(h):
        t = y / max(1, h - 1)
        c = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3)) + (alpha,)
        d.line([(0, y), (w, y)], fill=c)
    return base


def shade(color, factor):
    return tuple(max(0, min(255, int(c * factor))) for c in color[:3]) + tuple(color[3:])


def add_glow(img, radius=3, strength=0.6):
    glow = img.filter(ImageFilter.GaussianBlur(radius))
    out = new(img.width, img.height)
    out = Image.alpha_composite(out, glow)
    out = Image.alpha_composite(out, img)
    return out


def font(size):
    for name in ("arial.ttf", "DejaVuSans.ttf", "LiberationSans-Regular.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except Exception:
            continue
    return ImageFont.load_default()


def text_image(text, size=48, color=(255, 255, 255, 255)):
    f = font(size)
    tmp = Image.new("RGBA", (10, 10))
    d = ImageDraw.Draw(tmp)
    box = d.textbbox((0, 0), text, font=f)
    w, h = box[2] - box[0] + 8, box[3] - box[1] + 8
    img = new(w, h)
    d = ImageDraw.Draw(img)
    d.text((4 - box[0], 4 - box[1]), text, font=f, fill=color)
    return img


def outline_ellipse(draw, box, fill, outline=(0, 0, 0, 255), width=2):
    draw.ellipse(box, fill=fill, outline=outline, width=width)


def make_ball(color, radius, outline=(0, 0, 0, 255), highlight=True):
    r = int(radius)
    size = r * 2
    img = new(size, size)
    d = ImageDraw.Draw(img)
    d.ellipse([0, 0, size - 1, size - 1], fill=color, outline=outline, width=2)
    if highlight:
        hx, hy = r - r * 0.35, r - r * 0.4
        d.ellipse([hx - r * 0.25, hy - r * 0.25, hx + r * 0.25, hy + r * 0.25],
                  fill=(255, 255, 255, 160))
    return add_glow(img, 2, 0.3)


def make_block(color, w, h, border=(0, 0, 0, 255), bevel=True):
    img = new(w, h)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, w - 1, h - 1], fill=color, outline=border, width=2)
    if bevel:
        d.line([(2, 2), (w - 3, 2)], fill=shade(color, 1.3), width=2)
        d.line([(2, 2), (2, h - 3)], fill=shade(color, 1.3), width=2)
        d.line([(2, h - 3), (w - 3, h - 3)], fill=shade(color, 0.6), width=2)
    return img


def make_humanoid(w=48, h=72, skin=(240, 200, 160, 255), shirt=(60, 120, 220, 255),
                  pants=(40, 40, 60, 255), hair=(60, 40, 20, 255), pose="idle",
                  accessory=None):
    """Personaje simple pero resultón. pose: idle|walk|jump|punch|kick."""
    img = new(w, h)
    d = ImageDraw.Draw(img)
    cx = w // 2
    head_r = int(w * 0.22)
    head_cy = head_r + 4

    # piernas
    leg_y = int(h * 0.62)
    leg_w = max(4, w // 8)
    spread = 4 if pose == "walk" else 2
    d.rounded_rectangle([cx - leg_w - spread, leg_y, cx - spread + 2, h - 2],
                        radius=3, fill=pants, outline=(0, 0, 0, 255))
    d.rounded_rectangle([cx + spread - 2, leg_y, cx + leg_w + spread, h - 2],
                        radius=3, fill=pants, outline=(0, 0, 0, 255))
    if pose == "kick":
        d.rounded_rectangle([cx + 2, leg_y - 6, cx + w - 4, leg_y + 8],
                            radius=3, fill=pants, outline=(0, 0, 0, 255))

    # torso
    torso_top = head_cy + head_r - 2
    d.rounded_rectangle([cx - w * 0.28, torso_top, cx + w * 0.28, leg_y + 2],
                        radius=6, fill=shirt, outline=(0, 0, 0, 255))

    # brazos
    arm_y = torso_top + 4
    if pose == "punch":
        d.rounded_rectangle([cx + w * 0.24, arm_y, cx + w * 0.5, arm_y + 8],
                            radius=3, fill=skin, outline=(0, 0, 0, 255))
    else:
        d.rounded_rectangle([cx - w * 0.42, arm_y, cx - w * 0.22, leg_y - 4],
                            radius=4, fill=skin, outline=(0, 0, 0, 255))
        d.rounded_rectangle([cx + w * 0.22, arm_y, cx + w * 0.42, leg_y - 4],
                            radius=4, fill=skin, outline=(0, 0, 0, 255))

    # cabeza
    d.ellipse([cx - head_r, head_cy - head_r, cx + head_r, head_cy + head_r],
              fill=skin, outline=(0, 0, 0, 255), width=2)
    # pelo
    d.arc([cx - head_r, head_cy - head_r, cx + head_r, head_cy + head_r],
          180, 360, fill=hair, width=5)
    # ojos
    eye_y = head_cy - 1
    d.ellipse([cx - head_r * 0.45 - 1, eye_y - 2, cx - head_r * 0.45 + 1, eye_y + 1], fill=(20, 20, 20, 255))
    d.ellipse([cx + head_r * 0.45 - 1, eye_y - 2, cx + head_r * 0.45 + 1, eye_y + 1], fill=(20, 20, 20, 255))

    if accessory:
        accessory(d, cx, head_cy, head_r, w, h)
    return img


def make_tile(top_color, side_color, w=64, h=32):
    """Tile isométrico (rombo) con un lateral para dar volumen."""
    img = new(w, h + 16)
    d = ImageDraw.Draw(img)
    top = [(w // 2, 0), (w, h // 2), (w // 2, h), (0, h // 2)]
    left = [(0, h // 2), (w // 2, h), (w // 2, h + 16), (0, h // 2 + 16)]
    right = [(w // 2, h), (w, h // 2), (w, h // 2 + 16), (w // 2, h + 16)]
    d.polygon(left, fill=shade(side_color, 0.7), outline=(0, 0, 0, 255))
    d.polygon(right, fill=shade(side_color, 0.85), outline=(0, 0, 0, 255))
    d.polygon(top, fill=top_color, outline=(0, 0, 0, 255))
    return img


def make_starfield(w, h, count=120, bg=(8, 10, 30, 255)):
    img = new(w, h, bg)
    d = ImageDraw.Draw(img)
    for _ in range(count):
        x = int(np.random.uniform(0, w))
        y = int(np.random.uniform(0, h))
        r = int(np.random.uniform(1, 3))
        c = int(np.random.uniform(150, 255))
        d.ellipse([x, y, x + r, y + r], fill=(c, c, 255, 255))
    return img


# --------------------------------------------------------------------------- #
#  Generación de assets compartidos
# --------------------------------------------------------------------------- #
def generate_common_assets(base_dir):
    """Escribe los efectos de sonido e música comunes en base_dir."""
    sfx_dir = os.path.join(base_dir, "assets", "sonidos")
    music_dir = os.path.join(base_dir, "assets", "musica")
    ensure_dir(sfx_dir)
    ensure_dir(music_dir)

    for name, fn in SFX.items():
        write_wav(os.path.join(sfx_dir, f"{name}.wav"), fn())

    for name, fn in MUSIC.items():
        write_wav(os.path.join(music_dir, f"{name}.wav"), fn())

    print(f"Assets comunes generados en {sfx_dir} y {music_dir}")


if __name__ == "__main__":
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    generate_common_assets(here)
