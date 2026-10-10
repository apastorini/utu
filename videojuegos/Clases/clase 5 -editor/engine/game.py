import pygame

from engine.game_object import AZUL_OSCURO
from engine.player import Player


class Game:
    def __init__(self):
        self.ANCHO = 800
        self.ALTO = 600
        self.PANTALLA = pygame.display.set_mode((self.ANCHO, self.ALTO))
        pygame.display.set_caption('Spritesheet con Teclas')

        self.jugador = Player(350, 250)
        self.reloj = pygame.time.Clock()
        self.estado_juego = 'jugando'

    def game_loop(self):
        ejecutando = True
        while ejecutando:
            # Obtener el tiempo transcurrido, aunque no lo usemos para la animación
            # es una buena práctica para mantener el bucle constante.
            dt = self.reloj.tick(15)  # Menor FPS para ver mejor el cambio de frame

            # --- INPUT: Siempre procesar eventos ---
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    ejecutando = False

            # --- Lógica del juego ---
            if self.estado_juego == 'jugando':
                teclas = pygame.key.get_pressed()
                self.jugador.mover(teclas)
                # No llamamos a update, ya que el movimiento se encarga de la animación

            # --- Renderizado ---
            self.PANTALLA.fill(AZUL_OSCURO)

            if self.estado_juego == 'jugando':
                self.jugador.draw(self.PANTALLA)

            pygame.display.flip()