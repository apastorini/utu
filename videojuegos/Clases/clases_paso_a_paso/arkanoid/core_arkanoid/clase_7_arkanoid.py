# game.py
import random

import pygame

from arkanoid.core_arkanoid.Ball import Ball
from arkanoid.core_arkanoid.Brick import Brick
from arkanoid.core_arkanoid.Player import Player
from core.Colors import AZUL_OSCURO, NEGRO, ROJO, BLANCO
from core.utils.utils import ANCHO, ALTO

pygame.init()
pygame.mixer.init() # Inicializamos el mezclador de sonido

# --- CARGAMOS SONIDOS ---
sonido_golpe = pygame.mixer.Sound('../assets/sounds/hit.mp3')

# --- CARGAMOS Y REPRODUCIMOS MÚSICA ---
pygame.mixer.music.load('../assets/music/song18.mp3')
pygame.mixer.music.play(-1)  # El -1 significa que se repetirá en bucle infinito

class Game:

    PANTALLA = pygame.display.set_mode((ANCHO, ALTO))

    # 4. Ponerle un título a la ventana
    pygame.display.set_caption('Arkanoid')


    # Fuente
    fuente = pygame.font.Font(None, 36)
    fuente_grande = pygame.font.Font(None, 72)

    # Creamos una instancia de nuestra nueva clase
    reloj = pygame.time.Clock()  # Creamos un objeto Clock
    puntuacion = 0  # Nuestra variable para la puntuación
    estado_juego = 'jugando'


    NUM_LADRILLOS_FILA = 10



    def __init__(self):


        # Reiniciar todas las variables del juego
        # 5. --- CREAMOS VARIABLES---
        self.jugador = Player(50, 450)
        self.pelota = Ball(50, 350)
        self.puntuacion = 0
        self.NUM_LADRILLOS_FILA = 10
        self.ANCHO_LADRILLO = ANCHO // self.NUM_LADRILLOS_FILA
        self.ladrillos = []
        self.jugador.rect.topleft = (50, 450)  # Posición inicial
        self.estado_juego = 'jugando'  # ¡Volvemos a jugar!
        pygame.mixer.music.play(-1)  # Volvemos a poner la música
        ##


        #Crear ladrillos
        for fila in range(5):  # 5 filas de ladrillos
            for col in range(self.NUM_LADRILLOS_FILA):  # 10 ladrillos por fila
                ladrillo = Brick(col * self.ANCHO_LADRILLO, fila * 40 + 50, self.ANCHO_LADRILLO, 30)
                self.ladrillos.append(ladrillo)

    def game_loop(self):
        # --- BUCLE PRINCIPAL ---
        ejecutando = True
        while ejecutando:
            # --- INPUT PRINCIPAL ---
            # Unificar la captura de eventos en un solo bloque por fotograma
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    ejecutando = False

                # Detectar la tecla espacio solo si estamos en la pantalla de game_over
                if self.estado_juego == 'game_over':
                    if evento.type == pygame.KEYDOWN:
                        if evento.key == pygame.K_SPACE:
                            self.__init__() # Reiniciar juego

            # --- LÓGICA SEGÚN ESTADO ---
            if self.estado_juego == 'jugando':
                teclas = pygame.key.get_pressed()

                # --- UPDATE ---
                self.jugador.mover(teclas)
                self.pelota.update()

                # Colisión pelota con pala
                if self.pelota.rect.colliderect(self.jugador.rect):
                    self.pelota.velocidad_y *= -1
                    self.pelota.rect.bottom = self.jugador.rect.top

                for ladrillo in self.ladrillos[:]:
                    if self.pelota.rect.colliderect(ladrillo.rect):
                        self.ladrillos.remove(ladrillo)
                        self.pelota.velocidad_y *= -1

                if self.pelota.rect.top > ALTO:
                    self.estado_juego = 'game_over'

                # --- RENDER JUGANDO ---
                self.PANTALLA.fill(AZUL_OSCURO)
                self.jugador.dibujar(self.PANTALLA)
                self.pelota.dibujar(self.PANTALLA)
                texto_puntuacion = self.fuente.render(f"Puntuación: {self.puntuacion}", True, BLANCO)
                for ladrillo in self.ladrillos:
                    ladrillo.dibujar(self.PANTALLA)
                self.PANTALLA.blit(texto_puntuacion, (10, 10))

            elif self.estado_juego == 'game_over':
                # --- RENDER GAME OVER ---
                self.PANTALLA.fill(NEGRO)
                texto_game_over = self.fuente_grande.render("GAME OVER", True, ROJO)
                texto_instruccion = self.fuente.render("Presiona ESPACIO para reiniciar", True, BLANCO)

                pos_game_over = texto_game_over.get_rect(center=(ANCHO / 2, ALTO / 2 - 50))
                pos_instruccion = texto_instruccion.get_rect(center=(ANCHO / 2, ALTO / 2 + 50))

                self.PANTALLA.blit(texto_game_over, pos_game_over)
                self.PANTALLA.blit(texto_instruccion, pos_instruccion)

            pygame.display.flip()
            self.reloj.tick(60)

        pygame.quit()

# --- PUNTO DE ENTRADA DEL PROGRAMA ---
# Este bloque debe ir pegado al margen izquierdo, fuera de la clase Game.
if __name__ == "__main__":
    juego = Game()
    juego.game_loop()