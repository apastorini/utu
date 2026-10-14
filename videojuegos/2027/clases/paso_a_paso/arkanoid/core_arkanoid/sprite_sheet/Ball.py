import pygame
from core.utils.utils import ANCHO

class Ball:
    # AQUI ESTA LA CORRECCIÓN: agregamos 'imagen_recortada' a los parámetros
    def __init__(self, x, y, imagen_recortada):
        self.image = imagen_recortada
        self.rect = self.image.get_rect(center=(x, y))
        self.velocidad_x = 4
        self.velocidad_y = -4

    def update(self):
        self.rect.x += self.velocidad_x
        self.rect.y += self.velocidad_y

        # Rebote con las paredes laterales y superior
        if self.rect.left <= 0 or self.rect.right >= ANCHO:
            self.velocidad_x *= -1
        if self.rect.top <= 0:
            self.velocidad_y *= -1

    def dibujar(self, superficie):
        superficie.blit(self.image, self.rect)