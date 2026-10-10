# engine/physics.py
import pygame
import pymunk
import math

class PhysicsMixin:
    """
    Un 'mixin' que añade propiedades y métodos de PyMunk a un GameObject.
    No está pensado para ser usado solo, sino en herencia múltiple.
    """
    def init_physics_circle(self, space, mass, radius, elasticity, friction):
        """Inicializa un cuerpo físico circular."""
        moment = pymunk.moment_for_circle(mass, 0, radius)
        self.body = pymunk.Body(mass, moment)
        self.body.position = self.rect.center
        self.shape = pymunk.Circle(self.body, radius)
        self.shape.elasticity = elasticity
        self.shape.friction = friction
        self.shape.parent = self # Guardamos una referencia al objeto del juego
        space.add(self.body, self.shape)

    def init_physics_box(self, space, mass, elasticity, friction):
        """Inicializa un cuerpo físico rectangular."""
        size = self.rect.size
        moment = pymunk.moment_for_box(mass, size)
        self.body = pymunk.Body(mass, moment)
        self.body.position = self.rect.center
        self.shape = pymunk.Poly.create_box(self.body, size)
        self.shape.elasticity = elasticity
        self.shape.friction = friction
        self.shape.parent = self
        space.add(self.body, self.shape)

    def update_from_physics(self):
        """Sincroniza la posición y rotación del sprite con el cuerpo físico."""
        self.rect.center = self.body.position
        # PyMunk usa radianes, Pygame usa grados. Hacemos la conversión para la rotación.
        self.image_rotated = pygame.transform.rotate(self.original_image, -math.degrees(self.body.angle))
        self.image = self.image_rotated
        self.rect = self.image.get_rect(center=self.rect.center)
