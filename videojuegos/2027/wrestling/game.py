# wrestling/game.py
"""
Juego de LUCHA LIBRE ISOMÉTRICA (clase 13).

Enfoque GAME LOOP (herencia directa de GameLoop, sin escenas).

Lo interesante de este ejemplo es que demuestra:

- `grid_to_iso` / coordenadas de rejilla.
- Orden de dibujado por PROFUNDIDAD (`sort_by_depth`), para que el luchador
  que está "más atrás" se dibuje primero.
- Partículas al golpear, barras de vida, música y efectos.
"""
import math
import os

import pygame

from engine.game_loop import GameLoop
from engine.iso_tools import grid_to_iso
from engine.audio import AudioManager
from engine.particle import ParticleSystem
from engine.shared_assets import sfx_path, music_path
from engine.ui_elements import HealthBar

TILE_W = 96
TILE_H = 48
N = 7  # tamaño de la lona (NxN celdas)


class Wrestler:
    def __init__(self, game, grid_x, grid_y, idle, punch, name, is_player):
        self.game = game
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.idle = idle
        self.punch = punch
        self.name = name
        self.is_player = is_player
        self.max_hp = 100
        self.hp = 100
        self.punch_timer = 0.0
        self.attack_cooldown = 0.0

    # ------------------------------ lógica ------------------------------- #
    def move(self, dx, dy):
        self.grid_x = max(0.4, min(N - 0.4, self.grid_x + dx))
        self.grid_y = max(0.4, min(N - 0.4, self.grid_y + dy))

    def update(self, dt):
        if self.punch_timer > 0:
            self.punch_timer -= dt
        if self.attack_cooldown > 0:
            self.attack_cooldown -= dt

    @property
    def punching(self):
        return self.punch_timer > 0

    def distance_to(self, other):
        return math.hypot(self.grid_x - other.grid_x,
                          self.grid_y - other.grid_y)

    @property
    def depth(self):
        return self.grid_x + self.grid_y

    def screen_pos(self):
        return grid_to_iso(self.grid_x, self.grid_y, TILE_W, TILE_H)

    # ----------------------------- dibujado ------------------------------ #
    def draw(self, surface, origin):
        sx, sy = self.screen_pos()
        px, py = int(origin[0] + sx), int(origin[1] + sy)

        shadow = self.game.shadow
        surface.blit(shadow, shadow.get_rect(center=(px, py - 4)))

        image = self.punch if self.punching else self.idle
        surface.blit(image, image.get_rect(midbottom=(px, py)))

        # Barra de vida flotante
        bar_w = 74
        ratio = max(0.0, self.hp / self.max_hp)
        bx = px - bar_w // 2
        by = py - image.get_height() - 16
        pygame.draw.rect(surface, (30, 30, 30), (bx, by, bar_w, 8))
        color = (70, 150, 255) if self.is_player else (230, 70, 70)
        pygame.draw.rect(surface, color, (bx, by, int(bar_w * ratio), 8))
        pygame.draw.rect(surface, (240, 240, 240), (bx, by, bar_w, 8), 1)


class WrestlingGame(GameLoop):
    def __init__(self):
        super().__init__(1000, 700, "Lucha Libre Isometrica", 60)
        pygame.display.set_caption("Lucha Libre Isometrica")

        self.game_dir = os.path.dirname(os.path.abspath(__file__))
        self.sprites_dir = os.path.join(self.game_dir, "assets", "sprites")
        self.origin = (500, 150)

        self.audio = AudioManager()
        self.particles = ParticleSystem()
        self.load_assets()
        self.reset()

        self.cpu_timer = 1.0

    # ------------------------------ assets ------------------------------- #
    def load_assets(self):
        self.ring = pygame.image.load(os.path.join(self.sprites_dir, "ring.png")).convert_alpha()
        self.shadow = pygame.image.load(os.path.join(self.sprites_dir, "sombra.png")).convert_alpha()

        rojo_idle = pygame.image.load(os.path.join(self.sprites_dir, "luchador_rojo_idle.png")).convert_alpha()
        rojo_punch = pygame.image.load(os.path.join(self.sprites_dir, "luchador_rojo_punch.png")).convert_alpha()
        azul_idle = pygame.image.load(os.path.join(self.sprites_dir, "luchador_azul_idle.png")).convert_alpha()
        azul_punch = pygame.image.load(os.path.join(self.sprites_dir, "luchador_azul_punch.png")).convert_alpha()

        self.player = Wrestler(self, 3.5, 2.6, rojo_idle, rojo_punch, "Tú", True)
        self.cpu = Wrestler(self, 3.5, 4.4, azul_idle, azul_punch, "CPU", False)

        for name in ("punch", "hit", "cheer", "whistle"):
            self.audio.load_sound(name, sfx_path(name))
        self.audio.load_music(music_path("wrestling"))
        self.audio.play_music(loops=-1, volume=0.4)

        self.big = pygame.font.Font(None, 64)
        self.font = pygame.font.Font(None, 30)
        self.player_bar = HealthBar((24, 24, 320, 26), 100, 100)
        self.cpu_bar = HealthBar((1000 - 24 - 320, 24, 320, 26), 100, 100)

    def reset(self):
        self.player.hp = self.player.max_hp
        self.player.grid_x, self.player.grid_y = 3.5, 2.6
        self.cpu.hp = self.cpu.max_hp
        self.cpu.grid_x, self.cpu.grid_y = 3.5, 4.4
        self.round_over = False
        self.message = ""

    # ------------------------------ eventos ------------------------------ #
    def attack(self, attacker, victim):
        if attacker.attack_cooldown > 0:
            return
        attacker.punch_timer = 0.18
        attacker.attack_cooldown = 0.45
        self.audio.play_sound("punch")

        if attacker.distance_to(victim) <= 1.0:
            victim.hp -= 12
            self.audio.play_sound("hit")
            sx, sy = victim.screen_pos()
            px = self.origin[0] + sx
            py = self.origin[1] + sy - 40
            self.particles.emit(px, py, count=18, color=(255, 210, 90),
                                speed=(80, 260), life=(0.2, 0.5), size=(2, 5))
            if victim.hp <= 0:
                victim.hp = 0
                self.round_over = True
                winner = self.player.name if victim is self.cpu else self.cpu.name
                self.message = f"¡Gana {winner}!  (R para revancha)"
                self.audio.play_sound("cheer")

    def handle_specific_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.reset()
            if not self.round_over and event.key in (pygame.K_j, pygame.K_SPACE):
                self.attack(self.player, self.cpu)

    # ------------------------------ lógica ------------------------------- #
    def update_game_logic(self):
        dt = 1.0 / self.fps
        keys = pygame.key.get_pressed()

        if not self.round_over:
            dx = dy = 0.0
            speed = 3.2 * dt
            if keys[pygame.K_w]:
                dx -= speed
                dy -= speed
            if keys[pygame.K_s]:
                dx += speed
                dy += speed
            if keys[pygame.K_a]:
                dx -= speed
                dy += speed
            if keys[pygame.K_d]:
                dx += speed
                dy -= speed
            if dx or dy:
                self.player.move(dx, dy)

            # IA de la CPU: se acerca y golpea
            self.cpu_timer -= dt
            dist = self.cpu.distance_to(self.player)
            if dist > 1.0:
                step = 1.8 * dt
                self.cpu.move(math.copysign(step, self.player.grid_x - self.cpu.grid_x),
                              math.copysign(step, self.player.grid_y - self.cpu.grid_y))
            elif self.cpu_timer <= 0:
                self.attack(self.cpu, self.player)
                self.cpu_timer = 1.1

        self.player.update(dt)
        self.cpu.update(dt)
        self.particles.update(dt)

        self.player_bar.set(self.player.hp)
        self.cpu_bar.set(self.cpu.hp)

    # ------------------------------ dibujo ------------------------------- #
    def draw_game_elements(self):
        self.screen.blit(self.ring, (0, 0))

        for w in sorted([self.player, self.cpu], key=lambda w: w.depth):
            w.draw(self.screen, self.origin)

        self.particles.draw(self.screen)
        self.player_bar.draw(self.screen)
        self.cpu_bar.draw(self.screen)

        # nombres
        name = self.font.render("TÚ", True, (120, 180, 255))
        self.screen.blit(name, (24, 54))
        name = self.font.render("CPU", True, (255, 120, 120))
        self.screen.blit(name, (1000 - 24 - 60, 54))

        hint = self.font.render("WASD mover   J/ESPACIO golpear   R reiniciar",
                                True, (230, 230, 230))
        self.screen.blit(hint, (24, 700 - 40))

        if self.round_over:
            banner = self.big.render(self.message, True, (255, 240, 120))
            rect = banner.get_rect(center=(500, 340))
            pygame.draw.rect(self.screen, (0, 0, 0, 180), rect.inflate(40, 20),
                             border_radius=10)
            self.screen.blit(banner, rect)
