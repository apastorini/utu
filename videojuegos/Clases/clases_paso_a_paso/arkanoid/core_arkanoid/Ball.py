import pygame
from core.utils.utils import ANCHO


class Ball:
    def __init__(self, x, y):
        # 1. Cargar la imagen en una variable temporal
        imagen_original = pygame.image.load('../assets/sprites/ball.png').convert_alpha()

        # 2. Escalar la imagen a un tamaño razonable para una pelota (20x20 píxeles)
        self.image = pygame.transform.scale(imagen_original, (20, 20))

        self.rect = self.image.get_rect(center=(x, y))
        self.velocidad_x = 4
        self.velocidad_y = -4

    def update(self):
        self.rect.x += self.velocidad_x
        self.rect.y += self.velocidad_y

        if self.rect.left <= 0 or self.rect.right >= ANCHO:
            self.velocidad_x *= -1
        if self.rect.top <= 0:
            self.velocidad_y *= -1

    def dibujar(self, superficie):
        superficie.blit(self.image, self.rect)