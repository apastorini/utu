# Clases 17 a 19 — Física de objetos y billar

Objetivo: construir objetos físicos **reutilizables** para no repetir
el trabajo de PyMunk. `engine/physics_object.py` aporta
`PhysicsObject`, `add_walls`/`add_static_segment` y **tipos de
colisión** (constantes) para los callbacks.

El ejemplo es un **billar** (enfoque Game Loop): mesa con bordes y
troneras, taco que apunta y carga potencia, y choques con sonido.

## Motor — código completo de los módulos nuevos

**`engine/physics_object.py`**

```python
"""
engine/physics_object.py

Piezas reutilizables de PyMunk para construir juegos físicos (billar,
resortera, minigolf...): cuerpos estáticos (paredes, suelo) y un
`PhysicsObject` genérico listo para usar.

Incluye "tipos de colisión" para que los callbacks de PyMunk sepan qué
chocó contra qué.
"""

import pymunk

from engine.game_object import GameObject
from engine.physics import PhysicsMixin

# Tipos de colisión (se usan en add_collision_handler)
COLLISION_DEFAULT = 1
COLLISION_BALL = 2
COLLISION_BLOCK = 3
COLLISION_PLAYER = 4
COLLISION_WALL = 5


def add_static_segment(space, a, b, thickness=5, elasticity=0.6, friction=0.6,
                       collision_type=COLLISION_WALL):
    seg = pymunk.Segment(space.static_body, a, b, thickness)
    seg.elasticity = elasticity
    seg.friction = friction
    seg.collision_type = collision_type
    space.add(seg)
    return seg


def add_walls(space, width, height, thickness=5, elasticity=0.6, friction=0.6):
    """Crea el marco del mundo (suelo + paredes)."""
    return [
        add_static_segment(space, (thickness, thickness),
                           (thickness, height - thickness), thickness, elasticity, friction),
        add_static_segment(space, (width - thickness, thickness),
                           (width - thickness, height - thickness), thickness, elasticity, friction),
        add_static_segment(space, (thickness, height - thickness),
                           (width - thickness, height - thickness), thickness, elasticity, friction),
        add_static_segment(space, (thickness, thickness),
                           (width - thickness, thickness), thickness, elasticity, friction),
    ]


class PhysicsObject(GameObject, PhysicsMixin):
    """
    GameObject con cuerpo físico (caja o círculo).

    Ejemplo:
        bola = PhysicsObject(x, y, imagen, space=space, shape="circle",
                             radius=12, mass=1, elasticity=0.9,
                             collision_type=COLLISION_BALL)
    """

    def __init__(self, x, y, image, space, mass=1.0, shape="box",
                 elasticity=0.5, friction=0.6, radius=None,
                 collision_type=COLLISION_DEFAULT):
        super().__init__(x, y, image)
        self.original_image = self.image

        if shape == "circle":
            self.init_physics_circle(space, mass, radius or self.rect.width // 2,
                                     elasticity, friction)
        else:
            self.init_physics_box(space, mass, elasticity, friction)

        self.shape.collision_type = collision_type

    def update(self, *args, **kwargs):
        self.update_from_physics()
```

## Juego de ejemplo — código completo

**`billiards/__init__.py`**

```python
# billiards/__init__.py
```

**`billiards/generar_assets.py`**

```python
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
```

**`billiards/game.py`**

```python
# billiards/game.py
"""
BILLAR con PyMunk (clases 17-19).

Enfoque GAME LOOP: hereda directamente de `engine.game_loop.GameLoop`.

Cosas que demuestra este ejemplo:

- Un `pymunk.Space` con gravedad 0 y amortiguación para que las bolas
  acaben parándose.
- Bordes de la mesa construidos con `engine.physics_object.add_static_segment`.
- 6 TRONERAS: zonas circulares; si el centro de una bola entra en una, la
  bola se retira (la blanca vuelve a su sitio).
- El TACO: se apunta con el ratón desde la bola blanca; mantén el clic
  izquierdo para cargar potencia (se ve una `ProgressBar`) y suelta para
  golpear en dirección CONTRARIA al ratón.
- Callbacks de colisión de PyMunk para el sonido de choque.
- Tecla R para reiniciar.

Controles:
    Ratón       apuntar
    Clic izq.   mantener = cargar,  soltar = golpear
    R           reiniciar
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
    COLLISION_WALL,
)
from engine.audio import AudioManager
from engine.particle import ParticleSystem
from engine.shared_assets import sfx_path, music_path
from engine.ui_elements import ProgressBar, Panel

# --------------------------------------------------------------------------- #
#  Geometría (debe coincidir con generar_assets.py)
# --------------------------------------------------------------------------- #
SCREEN_W, SCREEN_H = 1000, 640
PLAY_LEFT, PLAY_TOP, PLAY_RIGHT, PLAY_BOTTOM = 110, 100, 890, 540
POCKET_R = 26
GAP = 48
BALL_R = 16
BALL_MASS = 1.0

BALL_COLORS = [
    (238, 210, 60), (32, 96, 220), (216, 48, 44), (128, 52, 178),
    (242, 142, 34), (34, 150, 66), (150, 40, 40), (26, 26, 30),
    (238, 210, 60), (32, 96, 220), (216, 48, 44), (128, 52, 178),
    (242, 142, 34), (34, 150, 66), (150, 40, 40),
]

WHITE_START = (300, 320)
RACK_APEX = (600, 320)

MAX_IMPULSE = 1500.0
CHARGE_TIME = 1.0  # segundos para cargar al 100 %


def pocket_centers():
    cx = (PLAY_LEFT + PLAY_RIGHT) / 2
    return [
        (PLAY_LEFT, PLAY_TOP), (cx, PLAY_TOP), (PLAY_RIGHT, PLAY_TOP),
        (PLAY_LEFT, PLAY_BOTTOM), (cx, PLAY_BOTTOM), (PLAY_RIGHT, PLAY_BOTTOM),
    ]


def rack_positions():
    """Posiciones de las 15 bolas en triángulo (sin solaparse)."""
    spacing = BALL_R * 2 + 2
    apex_x, cy = RACK_APEX
    out = []
    for row in range(5):
        x = apex_x + row * spacing * math.cos(math.radians(30))
        count = row + 1
        y0 = cy - (count - 1) * spacing / 2
        for j in range(count):
            out.append((x, y0 + j * spacing))
    return out


class Ball(PhysicsObject):
    """Bola de billar: un cuerpo circular con imagen."""

    def __init__(self, x, y, image, space, is_white=False):
        super().__init__(x, y, image, space, mass=BALL_MASS, shape="circle",
                         elasticity=0.92, friction=0.05, radius=BALL_R,
                         collision_type=COLLISION_BALL)
        self.is_white = is_white


class BilliardsGame(GameLoop):
    def __init__(self):
        super().__init__(SCREEN_W, SCREEN_H, "Billar", 60)
        pygame.display.set_caption("Billar")

        self.game_dir = os.path.dirname(os.path.abspath(__file__))
        self.sprites_dir = os.path.join(self.game_dir, "assets", "sprites")

        self.audio = AudioManager()
        self.particles = ParticleSystem()
        self.load_assets()

        self._new_space()
        self.reset()

    # ------------------------------ assets ------------------------------- #
    def load_assets(self):
        sp = self.sprites_dir
        self.img_table = pygame.image.load(os.path.join(sp, "mesa.png")).convert()
        self.img_blanca = pygame.image.load(os.path.join(sp, "blanca.png")).convert_alpha()
        self.ball_imgs = [
            pygame.image.load(os.path.join(sp, f"bola_{i:02d}.png")).convert_alpha()
            for i in range(15)
        ]
        self.img_cue = pygame.image.load(os.path.join(sp, "taco.png")).convert_alpha()
        self.img_shadow = pygame.image.load(os.path.join(sp, "sombra.png")).convert_alpha()
        self.img_shadow = pygame.transform.smoothscale(
            self.img_shadow, (BALL_R * 2 + 6, BALL_R + 5))

        self.font = pygame.font.Font(None, 30)
        self.big = pygame.font.Font(None, 58)
        self.power_bar = ProgressBar((SCREEN_W // 2 - 160, SCREEN_H - 42, 320, 20),
                                     maximum=100, value=0)

        for name in ("bounce", "shot"):
            self.audio.load_sound(name, sfx_path(name))
        self.audio.load_music(music_path("game"))
        self.audio.play_music(loops=-1, volume=0.4)

    # ------------------------------ físicas ------------------------------ #
    def _new_space(self):
        self.space = pymunk.Space()
        self.space.gravity = (0.0, 0.0)
        self.space.damping = 0.6  # las bolas van frenando solas

        self._build_cushions()
        self.pockets = pocket_centers()

        # Sonido al chocar (bolas entre sí y bolas contra las bandas).
        self.space.on_collision(COLLISION_BALL, COLLISION_BALL,
                                post_solve=self._on_impact)
        self.space.on_collision(COLLISION_BALL, COLLISION_WALL,
                                post_solve=self._on_impact)

    def _build_cushions(self):
        """Bandas de la mesa con huecos en las 6 troneras."""
        left, top, right, bottom = PLAY_LEFT, PLAY_TOP, PLAY_RIGHT, PLAY_BOTTOM
        cx = (left + right) / 2
        g = GAP
        segments = [
            ((left + g, top), (cx - g, top)),
            ((cx + g, top), (right - g, top)),
            ((left + g, bottom), (cx - g, bottom)),
            ((cx + g, bottom), (right - g, bottom)),
            ((left, top + g), (left, bottom - g)),
            ((right, top + g), (right, bottom - g)),
        ]
        for a, b in segments:
            add_static_segment(self.space, a, b, thickness=6,
                               elasticity=0.85, friction=0.1,
                               collision_type=COLLISION_WALL)

    def _on_impact(self, arbiter, space, data):
        if arbiter.total_impulse.length > 40:
            now = pygame.time.get_ticks()
            if now - self._last_bounce > 45:
                self._last_bounce = now
                self.audio.play_sound("bounce")

    # ------------------------------- setup ------------------------------- #
    def reset(self):
        for b in getattr(self, "balls", []):
            try:
                self.space.remove(b.shape, b.body)
            except Exception:
                pass

        self.balls = []
        self.white = Ball(*WHITE_START, self.img_blanca, self.space, is_white=True)
        self.balls.append(self.white)
        for i, (x, y) in enumerate(rack_positions()):
            img = self.ball_imgs[i % len(self.ball_imgs)]
            self.balls.append(Ball(x, y, img, self.space))

        self.score = 0
        self.power = 0.0
        self.charging = False
        self._last_bounce = 0
        self.message = ""

    # ------------------------------ eventos ------------------------------ #
    def handle_specific_events(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            self.reset()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self._can_shoot():
                self.charging = True
                self.power = 0.0
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.charging:
                self._shoot()

    def _can_shoot(self):
        return (self.white in self.balls
                and self.white.body.velocity.length < 25)

    def _shoot(self):
        mx, my = pygame.mouse.get_pos()
        bx, by = self.white.body.position
        dx, dy = bx - mx, by - my
        dist = math.hypot(dx, dy) or 1.0
        dx, dy = dx / dist, dy / dist

        power = max(0.08, self.power)
        impulse = power * MAX_IMPULSE
        self.white.body.apply_impulse_at_local_point((dx * impulse, dy * impulse))

        # Nube de tiza en la punta del taco.
        self.particles.emit(bx, by, count=10, color=(210, 230, 255),
                            speed=(30, 120), life=(0.15, 0.35), size=(1, 3),
                            gravity=0.0, angle=math.degrees(math.atan2(-dy, -dx)),
                            spread=40)

        self.audio.play_sound("shot")
        self.charging = False
        self.power = 0.0

    # ------------------------------ lógica ------------------------------- #
    def _pocket(self, ball):
        if ball is self.white:
            ball.body.position = WHITE_START
            ball.body.velocity = (0, 0)
            ball.body.angular_velocity = 0
        else:
            try:
                self.space.remove(ball.shape, ball.body)
            except Exception:
                pass
            if ball in self.balls:
                self.balls.remove(ball)
            self.score += 10
        self.audio.play_sound("bounce")

    def update_game_logic(self):
        dt = 1.0 / self.fps

        if self.charging:
            self.power = min(1.0, self.power + dt / CHARGE_TIME)

        self.space.step(dt)

        for ball in list(self.balls):
            ball.update()
            for (px, py) in self.pockets:
                dx = ball.body.position.x - px
                dy = ball.body.position.y - py
                if dx * dx + dy * dy < POCKET_R * POCKET_R:
                    self._pocket(ball)
                    break

        self.particles.update(dt)
        self.power_bar.set(self.power * 100 if self.charging else 0)

    # ------------------------------ dibujo ------------------------------- #
    def _draw_cue(self):
        mx, my = pygame.mouse.get_pos()
        bx, by = self.white.body.position
        ang = math.atan2(my - by, mx - bx)

        gap = BALL_R + 4 + (self.power * 55 if self.charging else 0)
        length = self.img_cue.get_width()
        cx = bx + math.cos(ang) * (gap + length / 2)
        cy = by + math.sin(ang) * (gap + length / 2)

        img = pygame.transform.rotate(self.img_cue, -math.degrees(ang))
        # momio del taco y línea de puntería
        end = (bx + math.cos(ang) * gap, by + math.sin(ang) * gap)
        pygame.draw.line(self.screen, (255, 255, 255, 90), (bx, by), end, 1)
        self.screen.blit(img, img.get_rect(center=(cx, cy)))

    def draw_game_elements(self):
        self.screen.blit(self.img_table, (0, 0))

        # sombras
        for ball in self.balls:
            self.screen.blit(self.img_shadow,
                             self.img_shadow.get_rect(
                                 center=(ball.rect.centerx + 3, ball.rect.centery + 5)))

        # bolas
        for ball in self.balls:
            self.screen.blit(ball.image, ball.rect)

        if self._can_shoot():
            self._draw_cue()

        self.particles.draw(self.screen)

        # HUD
        Panel((14, 14, 250, 74), color=(0, 0, 0, 150)).draw(self.screen)
        title = self.font.render("BILLAR", True, (255, 225, 120))
        self.screen.blit(title, (26, 22))
        info = self.font.render(
            f"Puntaje: {self.score}   Bolas: {len(self.balls)}", True, (235, 235, 235))
        self.screen.blit(info, (26, 52))

        if self.charging:
            cap = self.font.render(f"Potencia {int(self.power * 100)}%", True,
                                   (255, 255, 255))
            self.screen.blit(cap, (SCREEN_W // 2 - cap.get_width() // 2, SCREEN_H - 66))
            self.power_bar.draw(self.screen)

        hint = self.font.render(
            "Mantén el clic para cargar y suelta para golpear   -   R reiniciar",
            True, (225, 225, 225))
        self.screen.blit(hint, (16, SCREEN_H - 28))

        if self.message:
            banner = self.big.render(self.message, True, (255, 240, 120))
            self.screen.blit(banner, banner.get_rect(center=(SCREEN_W // 2, 60)))
```

**`billiards/main.py`**

```python
# billiards/main.py
"""Ejecutar desde la carpeta 2027 con:  python -m billiards.main"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from billiards.game import BilliardsGame


def main():
    BilliardsGame().run()


if __name__ == "__main__":
    main()
```

## Controles

click mantenido = cargar, soltar = tirar, `R` reiniciar.

## Cómo ejecutar

Desde la carpeta `2027/`:

```bash
python -m billiards.main
```
