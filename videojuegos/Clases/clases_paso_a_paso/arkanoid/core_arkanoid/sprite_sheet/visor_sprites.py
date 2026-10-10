import pygame

pygame.init()

ruta_imagen = '../../assets/sprites/image_0918c1.png'
imagen = pygame.image.load(ruta_imagen)
pantalla = pygame.display.set_mode((imagen.get_width(), imagen.get_height()))
pygame.display.set_caption("Visor Pro - Haz clic y arrastra para enmarcar el sprite")

ejecutando = True
arrastrando = False
x_inicio, y_inicio = 0, 0
x_fin, y_fin = 0, 0

while ejecutando:
    pantalla.fill((255, 0, 255))  # Fondo fucsia
    pantalla.blit(imagen, (0, 0))

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

        # 1. Cuando presionas el clic, guardamos la esquina superior izquierda
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            arrastrando = True
            x_inicio, y_inicio = evento.pos
            x_fin, y_fin = evento.pos

        # 2. Mientras mueves el ratón sin soltar, actualizamos la esquina opuesta
        elif evento.type == pygame.MOUSEMOTION:
            if arrastrando:
                x_fin, y_fin = evento.pos

        # 3. Al soltar el clic, calculamos el cuadro final e imprimimos los datos
        elif evento.type == pygame.MOUSEBUTTONUP:
            arrastrando = False
            x = min(x_inicio, x_fin)
            y = min(y_inicio, y_fin)
            ancho = abs(x_fin - x_inicio)
            alto = abs(y_fin - y_inicio)
            print(f"Copia esto en tu código -> X: {x}, Y: {y}, Ancho: {ancho}, Alto: {alto}")

    # Dibujamos un rectángulo rojo para que veas qué estás recortando
    if arrastrando:
        x = min(x_inicio, x_fin)
        y = min(y_inicio, y_fin)
        ancho = abs(x_fin - x_inicio)
        alto = abs(y_fin - y_inicio)
        pygame.draw.rect(pantalla, (255, 0, 0), (x, y, ancho, alto), 2)

    pygame.display.flip()

pygame.quit()