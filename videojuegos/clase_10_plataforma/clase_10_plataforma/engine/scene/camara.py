# engine/camera.py
import pygame

class Camera:
    """
    Gestiona el desplazamiento (scrolling) del mundo del juego.
    Sigue a una entidad objetivo y calcula el offset para el dibujado.
    """
    def __init__(self, screen_width, screen_height, world_width, world_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.world_width = world_width
        self.world_height = world_height
        self.camera_rect = pygame.Rect(0, 0, screen_width, screen_height)

    def apply(self, entity):
        """Devuelve el Rect de la entidad desplazado por la cámara."""
        return entity.rect.move(self.camera_rect.topleft)

    def update(self, target):
        """Centra la cámara en el objetivo, con límites para no salirse del mundo."""
        x = -target.rect.centerx + int(self.screen_width / 2)
        y = -target.rect.centery + int(self.screen_height / 2)

        # Límites de la cámara
        x = min(0, x)  # No desplazarse más allá del borde izquierdo
        y = min(0, y)  # No desplazarse más allá del borde superior
        x = max(-(self.world_width - self.screen_width), x)   # No desplazarse más allá del borde derecho
        y = max(-(self.world_height - self.screen_height), y)  # No desplazarse más allá del borde inferior

        self.camera_rect.topleft = (x, y)