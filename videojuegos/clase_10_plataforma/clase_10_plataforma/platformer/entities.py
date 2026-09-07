import pygame
from engine.game_object import GameObject


class Player(GameObject):
    def __init__(self, x, y, assets):
        self.assets = assets
        self.animations = {
            'idle': self.assets.get_animation('player_ss', 'idle'),
            'walk_right': self.assets.get_animation('player_ss', 'walk_right'),
            'walk_left': self.assets.get_animation('player_ss', 'walk_left')
        }

        super().__init__(x, y, self.animations['idle'])

        self.velocidad_mov = 4;
        self.fuerza_salto = 16;
        self.gravedad = 0.7
        self.pos = pygame.math.Vector2(x, y);
        self.vel = pygame.math.Vector2(0, 0)
        self.en_suelo = False;
        self.current_animation_name = 'idle'

    def set_animation(self, anim_name):
        if self.current_animation_name != anim_name:
            self.current_animation_name = anim_name
            self.frames = self.animations[anim_name]
            self.current_frame = 0

    def update(self, plataformas, *args, **kwargs):
        self.vel.x = 0
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            self.vel.x = -self.velocidad_mov;
            self.set_animation('walk_left')
        elif teclas[pygame.K_RIGHT]:
            self.vel.x = self.velocidad_mov;
            self.set_animation('walk_right')
        else:
            self.set_animation('idle')

        if teclas[pygame.K_SPACE] and self.en_suelo:
            self.vel.y = -self.fuerza_salto

        self.vel.y += self.gravedad
        if self.vel.y > 20: self.vel.y = 20

        self.pos.x += self.vel.x
        self.rect.centerx = round(self.pos.x)
        self.check_collision_x(plataformas)

        self.pos.y += self.vel.y
        self.rect.centery = round(self.pos.y)
        self.check_collision_y(plataformas)

        super().update()  # Llama a update_animation

        # Redimensionamos la imagen final (los sprites de Mario son grandes)
        self.image = pygame.transform.scale(self.image, (48, 48))
        self.rect = self.image.get_rect(center=self.rect.center)

    def check_collision_x(self, plataformas):
        colisiones = pygame.sprite.spritecollide(self, plataformas, False)
        for plat in colisiones:
            if self.vel.x > 0:
                self.rect.right = plat.rect.left
            elif self.vel.x < 0:
                self.rect.left = plat.rect.right
            self.pos.x = self.rect.centerx

    def check_collision_y(self, plataformas):
        colisiones = pygame.sprite.spritecollide(self, plataformas, False)
        self.en_suelo = False
        for plat in colisiones:
            if self.vel.y > 0:
                self.rect.bottom = plat.rect.top
                self.en_suelo = True;
                self.vel.y = 0
            elif self.vel.y < 0:
                self.rect.top = plat.rect.bottom;
                self.vel.y = 0
            self.pos.y = self.rect.centery