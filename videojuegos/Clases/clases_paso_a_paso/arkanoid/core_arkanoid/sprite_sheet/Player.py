import pygame
from core.utils.utils import ANCHO


class Player:
    def __init__(self, x, y, imagen_recortada):
        # Recibimos la imagen desde el game.py en lugar de cargarla aquí
        self.image = imagen_recortada
        self.rect = self.image.get_rect()

        # Posicionamos el rectángulo donde nos digan
        self.rect.topleft = (x, y)
        self.velocidad = 5

    def mover(self, teclas):
        # Mueve a la izquierda si se presiona la tecla Y si no ha chocado con el borde izquierdo (0)
        if teclas[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocidad

        # Mueve a la derecha si se presiona la tecla Y si no ha chocado con el borde derecho (ANCHO)
        if teclas[pygame.K_RIGHT] and self.rect.right < ANCHO:
            self.rect.x += self.velocidad

    def dibujar(self, superficie):
        # Dibujamos la imagen en la posición del rect
        superficie.blit(self.image, self.rect)