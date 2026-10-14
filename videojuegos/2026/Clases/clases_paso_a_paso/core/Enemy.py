import pygame


class Enemy:
    def __init__(self, x, y, ancho, alto, color):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.color = color
        # Damos al enemigo una velocidad en ambos ejes
        self.velocidad_x = 3
        self.velocidad_y = 3

    def update(self, ancho_pantalla, alto_pantalla):
        # Mover el enemigo
        self.rect.x += self.velocidad_x
        self.rect.y += self.velocidad_y

        # Lógica de rebote (IA Simple)
        if self.rect.left <= 0 or self.rect.right >= ancho_pantalla:
            self.velocidad_x *= -1  # Invertir la dirección horizontal
        if self.rect.top <= 0 or self.rect.bottom >= alto_pantalla:
            self.velocidad_y *= -1  # Invertir la dirección vertical

    def dibujar(self, superficie):
        pygame.draw.rect(superficie, self.color, self.rect)