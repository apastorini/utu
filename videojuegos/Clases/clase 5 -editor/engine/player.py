import pygame
import os
from engine.game_object import GameObject

# Inicializar Pygame
pygame.init()

class Player(GameObject):
    def __init__(self, x, y):
        # La ruta al JSON de nuestro personaje
        json_path = os.path.join('assets', 'sprites', 'player_animation', 'player.json')
        super().__init__(x, y, json_path=json_path)
        self.velocidad = 5

    def mover(self, keys):
        """
        Controla el movimiento y la animación del jugador.
        """
        if keys[pygame.K_LEFT]:
            # Retroceder en los fotogramas
            self.frame_index -= 1
            # Si llegamos al inicio, volver al final
            if self.frame_index < 0:
                self.frame_index = len(self.animations[self.current_animation]) - 1

        if keys[pygame.K_RIGHT]:
            # Avanzar en los fotogramas
            self.frame_index += 1
            # Si llegamos al final, volver al inicio
            if self.frame_index >= len(self.animations[self.current_animation]):
                self.frame_index = 0

        # No hay movimiento horizontal, solo cambio de fotograma.
        self.rect.x = self.x
        self.rect.y = self.y
