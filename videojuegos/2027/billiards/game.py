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
