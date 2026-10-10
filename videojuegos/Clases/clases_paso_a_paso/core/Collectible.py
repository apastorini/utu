import pygame

class Collectible:
    # El constructor. Similar al del jugador, pero sin velocidad.
    def __init__(self, x, y, ancho, alto, color):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.color = color

    # El método para dibujarlo en pantalla
    def dibujar(self, superficie):
        pygame.draw.rect(superficie, self.color, self.rect)