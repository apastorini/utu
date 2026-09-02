import pygame


class Player:
    # El "constructor": se ejecuta UNA VEZ al crear el objeto
    def __init__(self, x, y, ancho, alto, color):
        # self se refiere al objeto específico que se está creando
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.color = color
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
        pygame.draw.rect(superficie, self.color, self.rect)