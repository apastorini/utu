import pygame

class Player:
    def __init__(self, x, y):
        # Cargamos la imagen y obtenemos su rectángulo
        self.image = pygame.image.load('assets/mario.jpg').convert_alpha()
        self.rect = self.image.get_rect()
        # Posicionamos el rectángulo donde nos digan
        self.rect.topleft = (x, y)
        self.velocidad = 5

    # Un "método": una función que pertenece a la clase
    def mover(self, teclas):
        if teclas[pygame.K_LEFT]:
            self.rect.x -= self.velocidad
        if teclas[pygame.K_RIGHT]:
            self.rect.x += self.velocidad
        if teclas[pygame.K_UP]:
            self.rect.y -= self.velocidad
        if teclas[pygame.K_DOWN]:
            self.rect.y += self.velocidad

    def dibujar(self, superficie):
        # En lugar de dibujar un rect, dibujamos la imagen en la posición del rect
        superficie.blit(self.image, self.rect)