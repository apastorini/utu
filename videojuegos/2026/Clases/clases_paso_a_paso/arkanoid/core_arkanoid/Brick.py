import pygame


class Brick:
    # Ahora recibe el ancho y alto deseado como parámetros
    def __init__(self, x, y, ancho, alto):
        imagen_original = pygame.image.load('../assets/sprites/brick.png').convert_alpha()

        # Usamos las variables en lugar de un número fijo
        self.image = pygame.transform.scale(imagen_original, (ancho, alto))
        self.rect = self.image.get_rect(topleft=(x, y))

    def dibujar(self, superficie):
        superficie.blit(self.image, self.rect)