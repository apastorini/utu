import pygame


class Enemy:
    def __init__(self, x, y):
        self.image = pygame.image.load('assets/koopa.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.velocidad_x = 3


    def update(self, ancho_pantalla, alto_pantalla):
        pass


    def dibujar(self, superficie):
        superficie.blit(self.image, self.rect)