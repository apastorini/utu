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



pygame.display.set_caption('Mi Primer Juego')


# Variables para el bucle
ejecutando = True

while ejecutando:
    # 1. INPUT: Recorremos la lista de eventos
    for evento in pygame.event.get():
        # Si el evento es 'cerrar la ventana', salimos del bucle
        if evento.type == pygame.QUIT:
            ejecutando = False

    # 2. UPDATE: (Aquí irá la lógica del juego en el futuro)
    # Por ahora no hacemos nada

    # 3. RENDER: Dibujamos en la pantalla
    PANTALLA.fill(AZUL_OSCURO)

    # Dibujamos nuestro rectángulo
    # pygame.draw.rect(superficie, color, (x, y, ancho, alto))
    pygame.draw.rect(PANTALLA, ROJO, (ANCHO / 2 - 25, ALTO / 2 - 25, 50, 50))

    pygame.display.flip()

# Salir de pygame y del programa
pygame.quit()