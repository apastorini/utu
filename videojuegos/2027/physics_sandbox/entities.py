# physics_sandbox/entities.py
import pygame

from engine.game_object import GameObject
from engine.physics import PhysicsMixin


class PhysicsCircle(GameObject, PhysicsMixin):
    def __init__(self, x, y, radius, space):
        image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(image, (200, 30, 30), (radius, radius), radius)

        super().__init__(x, y, image)
        self.original_image = self.image  # para la rotación

        self.init_physics_circle(space, mass=10, radius=radius,
                                 elasticity=0.6, friction=0.8)

    def update(self, *args, **kwargs):
        self.update_from_physics()


class PhysicsBox(GameObject, PhysicsMixin):
    def __init__(self, x, y, width, height, space):
        image = pygame.Surface((width, height), pygame.SRCALPHA)
        image.fill((30, 30, 200))

        super().__init__(x, y, image)
        self.original_image = self.image

        self.init_physics_box(space, mass=15, elasticity=0.4, friction=0.9)

    def update(self, *args, **kwargs):
        self.update_from_physics()
