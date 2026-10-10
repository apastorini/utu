import pygame


class SpriteSheet:
    def __init__(self, ruta_archivo):
        self.hoja = pygame.image.load(ruta_archivo).convert_alpha()

    def obtener_imagen(self, x, y, ancho, alto, escala_ancho=None, escala_alto=None, quitar_fondo=False):
        # Creamos la superficie para el recorte
        imagen = pygame.Surface((ancho, alto), pygame.SRCALPHA)
        imagen.blit(self.hoja, (0, 0), (x, y, ancho, alto))

        # --- NUEVA MAGIA PARA BORRAR EL FONDO VIOLETA ---
        if quitar_fondo:
            # Capturamos el color exacto del píxel de la esquina superior izquierda (0,0)
            color_a_borrar = imagen.get_at((0, 0))
            # Le decimos a Pygame que haga transparente todo lo que tenga ese color
            imagen.set_colorkey(color_a_borrar)

        # Escalamos al tamaño final que tendrá en el juego
        if escala_ancho and escala_alto:
            imagen = pygame.transform.scale(imagen, (escala_ancho, escala_alto))

        return imagen