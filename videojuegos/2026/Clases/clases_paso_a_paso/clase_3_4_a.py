import pygame


pygame.init()

#Constantes
ANCHO = 800
ALTO = 600
PANTALLA = pygame.display.set_mode((ANCHO, ALTO))
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
AZUL_OSCURO = (30, 30, 40)



pygame.display.set_caption('Clase 3 y 4')



# Variables para la posición y velocidad del jugador
player_x = ANCHO / 2 - 25
player_y = ALTO / 2 - 25
player_velocidad = 5

ejecutando = True
while ejecutando:
    # --- INPUT ---
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

    # Nueva sección: detectar teclas presionadas
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT]:
        player_x -= player_velocidad
    if teclas[pygame.K_RIGHT]:
        player_x += player_velocidad
    if teclas[pygame.K_UP]:
        player_y -= player_velocidad  # Restamos para subir en el eje Y
    if teclas[pygame.K_DOWN]:
        player_y += player_velocidad  # Sumamos para bajar en el eje Y

    # --- UPDATE (la lógica del juego) ---
    # (Por ahora, el movimiento es nuestra única lógica)

    # --- RENDER ---
    PANTALLA.fill(AZUL_OSCURO)

    # Dibujamos el rectángulo usando nuestras nuevas variables
    pygame.draw.rect(PANTALLA, ROJO, (player_x, player_y, 50, 50))

    pygame.display.flip()

pygame.quit()