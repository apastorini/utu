# En Brick.py
import pygame

class Brick:
    def __init__(self, x, y, imagen_recortada):
        self.image = imagen_recortada
        self.rect = self.image.get_rect(topleft=(x, y))

    def dibujar(self, superficie):
        superficie.blit(self.image, self.rect)