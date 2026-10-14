
import pygame

from core.Player import Player

# 2. Inicializar pygame
pygame.init()

# 3. Definir el tamaño de la ventana
ANCHO = 800
ALTO = 600
ROJO = (255, 0, 0)
AZUL_OSCURO = (30, 30, 40)
PANTALLA = pygame.display.set_mode((ANCHO, ALTO))

# 4. Ponerle un título a la ventana
pygame.display.set_caption('Clase 3 y 4')


# --- ANTES DEL BUCLE PRINCIPAL ---
jugador = Player(ANCHO / 2 - 25, ALTO / 2 - 25, 50, 50, ROJO)
reloj = pygame.time.Clock() # Creamos un objeto Clock

# --- BUCLE PRINCIPAL ---
ejecutando = True
while ejecutando:
    # --- INPUT ---
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

    # Obtenemos las teclas presionadas
    teclas = pygame.key.get_pressed()

    # --- UPDATE ---
    # Llamamos al método mover de NUESTRO objeto jugador
    jugador.mover(teclas)


    # --- RENDER ---
    PANTALLA.fill(AZUL_OSCURO)
    jugador.dibujar(PANTALLA)
    pygame.display.flip()

    # --- CONTROL DE TIEMPO ---
    # Le decimos al reloj que espere lo necesario para que el bucle
    # no se ejecute más de 60 veces por segundo.
    reloj.tick(60)
pygame.quit()