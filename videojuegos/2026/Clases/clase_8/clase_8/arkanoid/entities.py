# arkanoid/entities.py
import pygame
import random
from engine.game_object import GameObject


class Paddle(GameObject):
    def __init__(self, x, y, frames):
        super().__init__(x, y, frames)
        self.velocidad = 8

    # --- CAMBIO CLAVE: Se añaden *args para aceptar argumentos extra ---
    def update(self, *args, **kwargs):
        super().update()  # Llama al update del padre para la animación

        # Obtenemos el ancho de la pantalla del primer argumento
        ANCHO_PANTALLA = args[0]

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            self.rect.x -= self.velocidad
        if teclas[pygame.K_RIGHT]:
            self.rect.x += self.velocidad

        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > ANCHO_PANTALLA: self.rect.right = ANCHO_PANTALLA


class Ball(GameObject):
    def __init__(self, x, y, frame):
        super().__init__(x, y, frame)
        self.velocidad_x = 5
        self.velocidad_y = -5
        self.radius = self.rect.width // 2

    # --- CAMBIO CLAVE: Se añaden *args para consistencia ---
    def update(self, *args, **kwargs):
        super().update()

        ANCHO_PANTALLA = args[0]
        ALTO_PANTALLA = args[1]

        self.rect.x += self.velocidad_x
        self.rect.y += self.velocidad_y

        if self.rect.left <= 0 or self.rect.right >= ANCHO_PANTALLA:
            self.velocidad_x *= -1
        if self.rect.top <= 0:
            self.velocidad_y *= -1

    def reset(self, x, y):
        self.rect.center = (x, y)
        self.velocidad_y = -5


class Brick(GameObject):
    def __init__(self, x, y, initial_frame, assets, health=1, sprite_name=""):
        super().__init__(x, y, initial_frame)
        self.assets = assets
        self.health = health
        self.initial_health = health
        self.value = 10 * health
        self.name = sprite_name
        self.base_name = self._get_base_sprite_name()

    def _get_base_sprite_name(self):
        current_name = self.name
        for suffix in ['_roto_1', '_roto_2', '_roto_!']:
            if current_name.endswith(suffix):
                return current_name[:-len(suffix)]
        return current_name

    def hit(self):
        self.health -= 1
        if self.health <= 0:
            return True
        try:
            damage_level = self.initial_health - self.health
            new_sprite_name = f"{self.base_name}_roto_{damage_level}"
            self.image = self.assets.get_sprite('main_ss', new_sprite_name)
        except (ValueError, KeyError):
            print(f"Advertencia: No se encontró el sprite de daño '{new_sprite_name}'.")
        return False


class PowerUp(GameObject):
    def __init__(self, x, y, frames, power_type):
        super().__init__(x, y, frames)
        self.type = power_type
        self.velocidad_y = 3

    # --- CAMBIO CLAVE: Se añaden *args para consistencia ---
    def update(self, *args, **kwargs):
        super().update()
        self.rect.y += self.velocidad_y

    def activate(self, paddle, balls_group, all_sprites_group, assets):
        if self.type == 'grow':
            paddle.rect.inflate_ip(paddle.rect.width * 0.5, 0)
        elif self.type == 'extra_ball':
            try:
                # Usamos un nombre genérico de pelota de tu JSON
                new_ball_img = assets.get_sprite('main_ss', 'pelota_bocha')
                new_ball = Ball(paddle.rect.centerx, paddle.rect.top, new_ball_img)
                balls_group.add(new_ball)
                all_sprites_group.add(new_ball)
            except (ValueError, KeyError):
                print("Advertencia: No se encontró 'pelota_bocha' para el power-up.")