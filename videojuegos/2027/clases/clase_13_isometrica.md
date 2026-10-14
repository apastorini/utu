# Clase 13 — Perspectiva isométrica

Objetivo: dibujar un mundo con **perspectiva isométrica** (la típica
vista 2:1, como en los juegos de estrategia).

El módulo `engine/iso_tools.py` convierte coordenadas de rejilla
cuadrada a coordenadas de pantalla "en rombo" y al revés, y ordena
los sprites por **profundidad** para que lo que está más atrás se
dibuje primero.

El juego de ejemplo es una **lucha libre isométrica** con el enfoque
**Game Loop** (herencia de `GameLoop`, sin escenas).

## Motor — código completo de los módulos nuevos

**`engine/iso_tools.py`**

```python
"""
engine/iso_tools.py

Herramientas para dibujar en perspectiva isométrica.

La rejilla del mundo es cuadrada (grid_x, grid_y) pero se dibuja "en rombo".
Esta es la conversión clásica de 2:1 (por cada 2 px a lo ancho, 1 px a lo alto).
"""


def grid_to_iso(grid_x, grid_y, tile_width=64, tile_height=32):
    """Convierte una coordenada de rejilla a coordenadas de pantalla (isométrica)."""
    screen_x = (grid_x - grid_y) * (tile_width / 2)
    screen_y = (grid_x + grid_y) * (tile_height / 2)
    return screen_x, screen_y


def iso_to_grid(screen_x, screen_y, tile_width=64, tile_height=32):
    """Convierte coordenadas de pantalla a coordenadas de rejilla (inversa)."""
    grid_x = (screen_x / (tile_width / 2) + screen_y / (tile_height / 2)) / 2
    grid_y = (screen_y / (tile_height / 2) - screen_x / (tile_width / 2)) / 2
    return grid_x, grid_y


class IsoSprite:
    """
    Objeto colocado en una rejilla isométrica.

    Se posiciona por su celda (grid_x, grid_y); el motor calcula la posición
    de pantalla y el orden de dibujado (profundidad) para que lo que está
    "más atrás" se dibuje primero.
    """

    def __init__(self, grid_x, grid_y, image, tile_width=64, tile_height=32,
                 origin=(0, 0)):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.image = image
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.origin = origin
        self.screen_x = 0
        self.screen_y = 0
        self.rect = image.get_rect()
        self.update_screen_rect()

    def update_screen_rect(self):
        sx, sy = grid_to_iso(self.grid_x, self.grid_y,
                             self.tile_width, self.tile_height)
        self.screen_x = sx + self.origin[0]
        self.screen_y = sy + self.origin[1]
        # Se ancla por la base (midbottom) para que "apoye" en el suelo.
        self.rect = self.image.get_rect(midbottom=(self.screen_x, self.screen_y))

    @property
    def depth(self):
        """Clave de orden de dibujado: mayor profundidad = más adelante."""
        return self.grid_x + self.grid_y


def sort_by_depth(sprites):
    """Devuelve los sprites ordenados de atrás hacia adelante."""
    return sorted(sprites, key=lambda s: (s.depth, s.grid_y))
```

**`engine/shared_assets.py`**

```python
"""
engine/shared_assets.py

Los sonidos y la música comunes viven en `2027/assets/` (generados por
`herramientas/genlib.py`). Este módulo da rutas absolutas a esos archivos
desde cualquier juego, sin depender de dónde se ejecute.
"""

import os

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # carpeta 2027


def sfx_path(name):
    """Ruta al efecto de sonido `name` (sin extensión)."""
    return os.path.join(_ROOT, "assets", "sonidos", f"{name}.wav")


def music_path(name):
    """Ruta a la música `name` (sin extensión)."""
    return os.path.join(_ROOT, "assets", "musica", f"{name}.wav")


def shared_dir():
    return os.path.join(_ROOT, "assets")
```

## Juego de ejemplo — código completo

**`wrestling/__init__.py`**

```python
"""Juego de lucha libre isométrica (clase 13)."""
```

**`wrestling/generar_assets.py`**

```python
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
```

**`wrestling/game.py`**

```python
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
```

**`wrestling/main.py`**

```python
# wrestling/main.py
"""Ejecutar desde la carpeta 2027 con:  python -m wrestling.main"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from wrestling.game import WrestlingGame


def main():
    WrestlingGame().run()


if __name__ == "__main__":
    main()
```

## Controles

`WASD` mover, `J`/`ESPACIO` golpear, `R` revancha.

## Cómo ejecutar

Desde la carpeta `2027/`:

```bash
python -m wrestling.main
```
