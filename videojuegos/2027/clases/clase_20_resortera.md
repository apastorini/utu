# Clase 20 — Resortes, bloques y destrucción (resortera)

Objetivo: un juego tipo *Angry Birds*. Reutiliza
`engine/physics_object.py` (de la clase 17) para las paredes, los
bloques y el pájaro.

El ejemplo es `slingshot/` (enfoque Game Loop): arrastras el pájaro
para tensar la goma, lo sueltas y derribas bloques y cerdos; los
impactos fuertes destruyen (partículas + sonido).

## Juego de ejemplo — código completo

**`slingshot/__init__.py`**

```python
# slingshot/__init__.py
```

**`slingshot/generar_assets.py`**

```python
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
```

**`slingshot/game.py`**

```python
# slingshot/game.py
"""
RESORTERA (clase 20, estilo Angry Birds) con PyMunk.

Enfoque GAME LOOP: hereda directamente de `engine.game_loop.GameLoop`.

Qué demuestra:

- Un `pymunk.Space` con gravedad y un suelo estático.
- La RESORTERA: se arrastra el pájaro con el ratón para tensar (con un
  estirón máximo); al soltar, la distancia = potencia y la dirección es la
  CONTRARIA al estirón.
- A la derecha, una torre de bloques (madera / piedra / hielo) y cerdos.
  Si un impacto tiene fuerza suficiente, el bloque o el cerdo se rompe
  (se elimina del espacio, con partículas + sonido).
- HUD con pájaros restantes y objetivos que quedan. Victoria / derrota.
- Tecla R para reiniciar.

Controles:
    Arrastrar el pájaro y soltar   lanzar
    R                              reiniciar
"""
import math
import os

import pygame
import pymunk

from engine.game_loop import GameLoop
from engine.physics_object import (
    PhysicsObject,
    add_static_segment,
    COLLISION_BALL,
    COLLISION_BLOCK,
    COLLISION_PLAYER,
    COLLISION_WALL,
)
from engine.audio import AudioManager
from engine.particle import ParticleSystem
from engine.shared_assets import sfx_path, music_path
from engine.ui_elements import Panel

# --------------------------------------------------------------------------- #
#  Configuración
# --------------------------------------------------------------------------- #
SCREEN_W, SCREEN_H = 1000, 640
GROUND_Y = 560
GRAVITY = 900

ANCHOR = (175, 360)
MAX_STRETCH = 115.0
IMPULSE_PER_PIXEL = 14.0
BIRD_MASS = 2.0
BIRD_R = 20
PIG_R = 22
TOTAL_BIRDS = 3

# material -> (hp, umbral de daño, densidad, color de partículas)
MATERIALS = {
    "madera": (420, 220, 0.6, (170, 120, 70)),
    "piedra": (780, 300, 1.4, (150, 150, 156)),
    "hielo": (220, 160, 0.4, (170, 220, 245)),
    "cerdo": (260, 160, 0.5, (110, 210, 100)),
}

# (x, y, ancho, alto, material)
TOWER = [
    (670, 490, 26, 140, "madera"),
    (810, 490, 26, 140, "madera"),
    (740, 407, 210, 26, "piedra"),
    (695, 349, 22, 90, "hielo"),
    (785, 349, 22, 90, "hielo"),
    (740, 293, 130, 22, "madera"),
    (880, 500, 28, 120, "piedra"),
]
# (x, y)
PIGS = [
    (740, 538),
    (740, 372),
    (740, 260),
]


class SlingshotGame(GameLoop):
    def __init__(self):
        super().__init__(SCREEN_W, SCREEN_H, "Resortera", 60)
        pygame.display.set_caption("Resortera")

        self.game_dir = os.path.dirname(os.path.abspath(__file__))
        self.sprites_dir = os.path.join(self.game_dir, "assets", "sprites")

        self.audio = AudioManager()
        self.particles = ParticleSystem()
        self.load_assets()
        self.reset()

    # ------------------------------ assets ------------------------------- #
    def load_assets(self):
        sp = self.sprites_dir
        self.img_bg = pygame.image.load(os.path.join(sp, "fondo.png")).convert()
        self.img_bird = pygame.image.load(os.path.join(sp, "pajaro.png")).convert_alpha()
        self.img_pig = pygame.image.load(os.path.join(sp, "cerdo.png")).convert_alpha()
        self.img_sling = pygame.image.load(os.path.join(sp, "resortera.png")).convert_alpha()
        self.block_tex = {
            name: pygame.image.load(os.path.join(sp, f"bloque_{name}.png")).convert_alpha()
            for name in ("madera", "piedra", "hielo")
        }

        # Ajustamos los sprites redondos al radio físico.
        self.img_bird = pygame.transform.smoothscale(self.img_bird, (BIRD_R * 2, BIRD_R * 2))
        self.img_pig = pygame.transform.smoothscale(self.img_pig, (PIG_R * 2, PIG_R * 2))

        self.font = pygame.font.Font(None, 30)
        self.big = pygame.font.Font(None, 56)

        for name in ("shot", "explode", "bounce", "cheer"):
            self.audio.load_sound(name, sfx_path(name))
        self.audio.load_music(music_path("wrestling"))
        self.audio.play_music(loops=-1, volume=0.35)

    # ------------------------------ físicas ------------------------------ #
    def _new_space(self):
        self.space = pymunk.Space()
        self.space.gravity = (0.0, GRAVITY)
        self.space.damping = 1.0

        add_static_segment(self.space, (0, GROUND_Y), (SCREEN_W, GROUND_Y),
                           thickness=10, elasticity=0.4, friction=0.9,
                           collision_type=COLLISION_WALL)

        # Daño por impacto (bloques y cerdos).
        damage_pairs = [
            (COLLISION_BALL, COLLISION_BLOCK),
            (COLLISION_BALL, COLLISION_PLAYER),
            (COLLISION_BLOCK, COLLISION_BLOCK),
            (COLLISION_BLOCK, COLLISION_PLAYER),
            (COLLISION_PLAYER, COLLISION_PLAYER),
            (COLLISION_BLOCK, COLLISION_WALL),
            (COLLISION_PLAYER, COLLISION_WALL),
        ]
        for a, b in damage_pairs:
            self.space.on_collision(a, b, post_solve=self._on_hit)

        # Rebotar el pájaro (sonido).
        self.space.on_collision(COLLISION_BALL, COLLISION_WALL,
                                post_solve=self._on_bounce)

    # ------------------------------- setup ------------------------------- #
    def reset(self):
        self._new_space()
        self.particles = ParticleSystem()

        self.blocks = []
        self.pigs = []
        self.to_remove = set()

        self.state = "playing"
        self.birds_left = TOTAL_BIRDS
        self.message = ""
        self.settle_time = 0.6
        self._last_bounce = 0

        self.bird = None
        self.bird_launched = False
        self.dragging = False
        self.pull = (0.0, 0.0)
        self.flight_time = 0.0
        self.rest_timer = 0.0

        self._build_tower()
        self._spawn_bird()

    def _add_block(self, x, y, w, h, material):
        base = self.block_tex[material]
        img = pygame.transform.smoothscale(base, (int(w), int(h)))
        hp, threshold, density, _ = MATERIALS[material]
        mass = max(0.2, w * h * density / 1000.0)
        obj = PhysicsObject(x, y, img, self.space, mass=mass, shape="box",
                            elasticity=0.2, friction=0.9,
                            collision_type=COLLISION_BLOCK)
        obj.breakable = True
        obj.material = material
        obj.hp = hp
        obj.damage_threshold = threshold
        self.blocks.append(obj)
        return obj

    def _add_pig(self, x, y):
        hp, threshold, density, _ = MATERIALS["cerdo"]
        obj = PhysicsObject(x, y, self.img_pig, self.space, mass=0.5,
                            shape="circle", elasticity=0.4, friction=0.9,
                            radius=PIG_R, collision_type=COLLISION_PLAYER)
        obj.breakable = True
        obj.is_pig = True
        obj.material = "cerdo"
        obj.hp = hp
        obj.damage_threshold = threshold
        self.pigs.append(obj)
        return obj

    def _build_tower(self):
        for (x, y, w, h, material) in TOWER:
            self._add_block(x, y, w, h, material)
        for (x, y) in PIGS:
            self._add_pig(x, y)

    def _spawn_bird(self):
        self.bird = PhysicsObject(ANCHOR[0], ANCHOR[1], self.img_bird, self.space,
                                  mass=BIRD_MASS, shape="circle",
                                  elasticity=0.4, friction=0.8,
                                  radius=BIRD_R, collision_type=COLLISION_BALL)
        self.bird.is_bird = True
        self.bird_launched = False
        self.dragging = False
        self.flight_time = 0.0
        self.rest_timer = 0.0

    # ------------------------------ eventos ------------------------------ #
    def handle_specific_events(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            self.reset()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.state == "playing" and self.bird is not None and not self.bird_launched:
                bx, by = self.bird.body.position
                if math.hypot(event.pos[0] - bx, event.pos[1] - by) < 95:
                    self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.dragging:
                self._release()

    def _drag_update(self):
        mx, my = pygame.mouse.get_pos()
        ax, ay = ANCHOR
        dx, dy = mx - ax, my - ay
        dist = math.hypot(dx, dy)
        if dist > MAX_STRETCH:
            dx *= MAX_STRETCH / dist
            dy *= MAX_STRETCH / dist
        tx, ty = ax + dx, ay + dy
        ty = min(ty, GROUND_Y - 30)
        self.bird.body.position = (tx, ty)
        self.bird.body.velocity = (0, 0)
        self.bird.body.angular_velocity = 0
        self.pull = (dx, dy)

    def _release(self):
        self.dragging = False
        if self.bird is None:
            return
        dx, dy = self.pull
        if math.hypot(dx, dy) < 14:
            self.bird.body.position = ANCHOR
            self.pull = (0.0, 0.0)
            return
        # Dirección CONTRARIA al estirón.
        self.bird.body.apply_impulse_at_local_point(
            (-dx * IMPULSE_PER_PIXEL, -dy * IMPULSE_PER_PIXEL))
        self.bird_launched = True
        self.flight_time = 0.0
        self.rest_timer = 0.0
        self.audio.play_sound("shot")

    # ---------------------------- colisiones ----------------------------- #
    def _on_hit(self, arbiter, space, data):
        if self.settle_time > 0:
            return
        imp = arbiter.total_impulse.length
        if imp < 120:
            return
        for shape in arbiter.shapes:
            obj = getattr(shape, "parent", None)
            if obj is None or not getattr(obj, "breakable", False):
                continue
            if obj in self.to_remove:
                continue
            damage = (imp - obj.damage_threshold) * 0.9
            if damage > 0:
                obj.hp -= damage
                if obj.hp <= 0:
                    self.to_remove.add(obj)

    def _on_bounce(self, arbiter, space, data):
        if arbiter.total_impulse.length > 220:
            now = pygame.time.get_ticks()
            if now - self._last_bounce > 60:
                self._last_bounce = now
                self.audio.play_sound("bounce")

    def _destroy(self, obj):
        try:
            self.space.remove(obj.shape, obj.body)
        except Exception:
            pass
        cx, cy = obj.rect.center
        color = MATERIALS.get(obj.material, (200, 200, 200))[3]
        if getattr(obj, "is_pig", False):
            if obj in self.pigs:
                self.pigs.remove(obj)
            color = MATERIALS["cerdo"][3]
        else:
            if obj in self.blocks:
                self.blocks.remove(obj)
        self.audio.play_sound("explode")
        self.particles.emit(cx, cy, count=26, color=color, speed=(60, 280),
                            life=(0.3, 0.75), size=(2, 6), gravity=600,
                            spread=360)

    # ------------------------------ lógica ------------------------------- #
    def _finish_bird(self):
        if self.bird is not None:
            try:
                self.space.remove(self.bird.shape, self.bird.body)
            except Exception:
                pass
            self.bird = None

        if self.state != "playing":
            return
        if self.pigs and self.birds_left > 1:
            self.birds_left -= 1
            self._spawn_bird()
        elif self.pigs:
            self.state = "defeat"
            self.message = "¡Te quedaste sin pájaros!"

    def update_game_logic(self):
        dt = 1.0 / self.fps
        if self.settle_time > 0:
            self.settle_time -= dt

        if self.dragging and self.bird is not None:
            self._drag_update()

        self.space.step(dt)

        # Mientras el pájaro está "cargado" (sin lanzar) lo mantenemos
        # sujeto: si no, la gravedad lo tiraría de la resortera.
        if self.bird is not None and not self.bird_launched:
            if self.dragging:
                self._drag_update()
            else:
                self.bird.body.position = ANCHOR
                self.bird.body.velocity = (0, 0)
                self.bird.body.angular_velocity = 0

        if self.bird is not None:
            self.bird.update()
        for obj in self.blocks:
            obj.update()
        for obj in self.pigs:
            obj.update()

        if self.to_remove:
            for obj in list(self.to_remove):
                self._destroy(obj)
            self.to_remove.clear()

        # ¿Se acabó el vuelo del pájaro actual?
        if self.bird is not None and self.bird_launched and self.state == "playing":
            self.flight_time += dt
            pos = self.bird.body.position
            speed = self.bird.body.velocity.length
            done = (pos.x < -120 or pos.x > SCREEN_W + 120
                    or pos.y > SCREEN_H + 160 or self.flight_time > 10)
            if speed < 25:
                self.rest_timer += dt
                if self.rest_timer > 0.8:
                    done = True
            else:
                self.rest_timer = 0.0
            if done:
                self._finish_bird()

        # Victoria.
        if self.state == "playing" and not self.pigs:
            self.state = "victory"
            self.audio.play_sound("cheer")

        self.particles.update(dt)

    # ------------------------------ dibujo ------------------------------- #
    def _draw_bands(self):
        ax, ay = ANCHOR
        tip_l = (ax - 22, ay - 26)
        tip_r = (ax + 22, ay - 26)
        if self.bird is not None:
            bx, by = self.bird.body.position
        else:
            bx, by = ax, ay - 4
        for tip in (tip_l, tip_r):
            pygame.draw.line(self.screen, (74, 46, 30), tip, (bx, by), 9)
            pygame.draw.line(self.screen, (120, 80, 52), tip, (bx, by), 3)

    def draw_game_elements(self):
        self.screen.blit(self.img_bg, (0, 0))

        # Resortera (delante del pájaro solo por delante del palo).
        self.screen.blit(self.img_sling,
                         self.img_sling.get_rect(midbottom=(ANCHOR[0], GROUND_Y + 6)))
        self._draw_bands()

        for obj in self.blocks:
            self.screen.blit(obj.image, obj.rect)
        for obj in self.pigs:
            self.screen.blit(obj.image, obj.rect)
        if self.bird is not None:
            self.screen.blit(self.bird.image, self.bird.rect)

        self.particles.draw(self.screen)

        # HUD.
        Panel((14, 12, 236, 88), color=(0, 0, 0, 140)).draw(self.screen)
        self.screen.blit(self.font.render("RESORTERA", True, (255, 225, 120)), (26, 20))
        self.screen.blit(
            self.font.render(f"Pájaros: {self.birds_left}", True, (255, 255, 255)),
            (26, 48))
        self.screen.blit(
            self.font.render(f"Cerdos: {len(self.pigs)}/{len(PIGS)}", True,
                             (180, 255, 180)), (26, 74))

        # Fuerza actual mientras se tensa.
        if self.dragging:
            force = min(1.0, math.hypot(*self.pull) / MAX_STRETCH)
            label = self.font.render(f"Fuerza {int(force * 100)}%", True, (255, 255, 255))
            self.screen.blit(label, (SCREEN_W // 2 - label.get_width() // 2, 24))

        hint = self.font.render("Arrastra el pájaro y suelta   -   R reiniciar",
                                True, (235, 235, 235))
        self.screen.blit(hint, (16, SCREEN_H - 28))

        if self.state != "playing":
            if self.state == "victory":
                text, color = "¡VICTORIA!", (140, 255, 140)
            else:
                text, color = self.message or "DERROTA", (255, 140, 140)
            banner = self.big.render(text, True, color)
            rect = banner.get_rect(center=(SCREEN_W // 2, 300))
            pygame.draw.rect(self.screen, (0, 0, 0, 170), rect.inflate(60, 30),
                             border_radius=12)
            self.screen.blit(banner, rect)
```

**`slingshot/main.py`**

```python
# slingshot/main.py
"""Ejecutar desde la carpeta 2027 con:  python -m slingshot.main"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from slingshot.game import SlingshotGame


def main():
    SlingshotGame().run()


if __name__ == "__main__":
    main()
```

## Controles

arrastrar el pájaro y soltar; `R` reiniciar.

## Cómo ejecutar

Desde la carpeta `2027/`:

```bash
python -m slingshot.main
```
