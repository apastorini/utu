import pygame
import random

from core.Collectible import Collectible
from core.Enemy import Enemy
from core.Player import Player
from utils.Colors import ROJO, AZUL_OSCURO, BLANCO, NEGRO

# 2. Inicializar pygame
pygame.init()

# 3. Definir el tamaño de la ventana
ANCHO = 800
ALTO = 600
PANTALLA = pygame.display.set_mode((ANCHO, ALTO))

# 4. Ponerle un título a la ventana
pygame.display.set_caption('Clase 5')

# --- CREAMOS EL OBJETO JUGADOR ---
jugador = Player(ANCHO / 2 - 25, ALTO / 2 - 25)
enemigo = Enemy(150, 150, 40, 40, (180, 50, 50))  # Un color rojo oscuro
fuente = pygame.font.Font(None, 36)
fuente_grande = pygame.font.Font(None, 72)  # Una fuente más grande
# Creamos una instancia de nuestra nueva clase
moneda = Collectible(100, 100, 30, 30, (255, 223, 0))  # Un color dorado
reloj = pygame.time.Clock()  # Creamos un objeto Clock
puntuacion = 0  # Nuestra variable para la puntuación
estado_juego = 'jugando'

# --- BUCLE PRINCIPAL ---
ejecutando = True
while ejecutando:
    # --- INPUT ---
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                # Reiniciar todas las variables del juego
                puntuacion = 0
                jugador.rect.topleft = (50, 50)  # Posición inicial
                enemigo.rect.topleft = (random.randint(0, ANCHO - 40), 0)  # Posición aleatoria
                estado_juego = 'jugando'  # ¡Volvemos a jugar!

    # El código se divide según el estado del juego
    if estado_juego == 'jugando':
        # --- INPUT ---
        teclas = pygame.key.get_pressed()

        # --- UPDATE ---
        jugador.mover(teclas)
        enemigo.update(ANCHO, ALTO)

        # Colisión con moneda
        if jugador.rect.colliderect(moneda.rect):
            puntuacion += 1
            # Movemos la moneda a una nueva posición aleatoria
            moneda.rect.x = random.randint(0, ANCHO - moneda.rect.width)
            moneda.rect.y = random.randint(0, ALTO - moneda.rect.height)

        # ¡NUEVA COLISIÓN CON ENEMIGO!
        if jugador.rect.colliderect(enemigo.rect):
            estado_juego = 'game_over'  # ¡Cambiamos el estado!

        # --- RENDER ---
        PANTALLA.fill(AZUL_OSCURO)
        jugador.dibujar(PANTALLA)
        texto_puntuacion = fuente.render(f"Puntuación: {puntuacion}", True, BLANCO)
        enemigo.dibujar(PANTALLA)  # Dibujamos al enemigo
        moneda.dibujar(PANTALLA)
        # 3. DIBUJAR EL TEXTO EN LA PANTALLA
        PANTALLA.blit(texto_puntuacion, (10, 10))  # Lo ponemos en la esquina sup. izq.


    elif estado_juego == 'game_over':

        PANTALLA.fill(NEGRO)

        # Renderizar textos

        texto_game_over = fuente_grande.render("GAME OVER", True, ROJO)

        texto_instruccion = fuente.render("Presiona ESPACIO para reiniciar", True, BLANCO)

        # Centrar los textos en la pantalla

        pos_game_over = texto_game_over.get_rect(center=(ANCHO / 2, ALTO / 2 - 50))

        pos_instruccion = texto_instruccion.get_rect(center=(ANCHO / 2, ALTO / 2 + 50))

        # Dibujar los textos

        PANTALLA.blit(texto_game_over, pos_game_over)

        PANTALLA.blit(texto_instruccion, pos_instruccion)

    pygame.display.flip()

    # --- CONTROL DE TIEMPO ---
    # Le decimos al reloj que espere lo necesario para que el bucle
    # no se ejecute más de 60 veces por segundo.

    reloj.tick(60)
pygame.quit()
