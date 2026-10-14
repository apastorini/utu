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
