import pygame


class Player:
    def __init__(self, x, y):
        # Cargamos la imagen y obtenemos su rectángulo
        self.image = pygame.image.load('../assets/sprites/paleta.png').convert_alpha()
        self.rect = self.image.get_rect()
        # Posicionamos el rectángulo donde nos digan
        self.rect.topleft = (x, y)
        self.velocidad = 5

    def mover(self, teclas):
        if teclas[pygame.K_LEFT]:
            self.rect.x -= self.velocidad
        if teclas[pygame.K_RIGHT]:
            self.rect.x += self.velocidad




    def dibujar(self, superficie):
        # En lugar de dibujar un rect, dibujamos la imagen en la posición del rect
        superficie.blit(self.image, self.rect)