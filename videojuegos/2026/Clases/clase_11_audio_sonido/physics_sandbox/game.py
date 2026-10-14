import pygame
import pymunk

from entities import PhysicsCircle, PhysicsBox
from motor.game_loop import GameLoop


class PhysicsGame(GameLoop):
    def __init__(self):
        super().__init__(1280, 720, "Sandbox de Físicas con PyMunk", 60)

        # 1. Configuración del Espacio de Físicas
        self.space = pymunk.Space()
        self.space.gravity = (0, 900)  # Gravedad hacia abajo

        self.sprites = pygame.sprite.Group()
        self.create_boundaries()

        # --- AÑADIDO: Creamos objetos al inicio para que la pantalla no esté vacía ---
        self.crear_objetos_iniciales()
        # -------------------------------------------------------------------------

        # 2. Lógica para arrastrar con el ratón
        self.mouse_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        self.mouse_joint = None
        self.mouse_dragging = False

    def crear_objetos_iniciales(self):
        """Crea algunas figuras al inicio para que el sandbox no esté vacío."""
        caja1 = PhysicsBox(600, 600, 50, 50, self.space)
        caja2 = PhysicsBox(600, 550, 50, 50, self.space)
        circulo1 = PhysicsCircle(650, 600, 30, self.space)
        self.sprites.add(caja1, caja2, circulo1)

    def create_boundaries(self):
        """Crea el suelo y las paredes estáticas."""
        # El suelo está 5 píxeles por debajo para que se vean los objetos
        floor = pymunk.Segment(self.space.static_body, (0, self.screen.get_height() - 5),
                               (self.screen.get_width(), self.screen.get_height() - 5), 5)
        floor.elasticity = 0.8
        floor.friction = 1.0

        wall_left = pymunk.Segment(self.space.static_body, (5, 0), (5, self.screen.get_height()), 5)
        wall_right = pymunk.Segment(self.space.static_body, (self.screen.get_width() - 5, 0),
                                    (self.screen.get_width() - 5, self.screen.get_height()), 5)

        self.space.add(floor, wall_left, wall_right)

    def handle_specific_events(self, event):
        if event.type == pygame.KEYDOWN:

            # --- ¡ESTA ES LA CORRECCIÓN! ---
            # Obtenemos la posición del ratón por separado usando pygame.mouse.get_pos()
            # El evento de teclado (KEYDOWN) no tiene el atributo .pos
            pos = pygame.mouse.get_pos()

            if event.key == pygame.K_c:  # 'c' para crear un círculo
                circle = PhysicsCircle(pos[0], pos[1], 30, self.space)
                self.sprites.add(circle)
            if event.key == pygame.K_b:  # 'b' para crear una caja (box)
                box = PhysicsBox(pos[0], pos[1], 50, 50, self.space)
                self.sprites.add(box)
            # ---------------------------------

        # --- Lógica de Agarrar y Soltar ---
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            point_query = self.space.point_query_nearest(event.pos, 0, pymunk.ShapeFilter())
            if point_query and point_query.shape.body.body_type == pymunk.Body.DYNAMIC:
                shape = point_query.shape
                self.mouse_joint = pymunk.PivotJoint(self.mouse_body, shape.body, shape.body.world_to_local(event.pos))
                self.mouse_joint.max_force = 70000  # Aumentamos la fuerza para que no se "rompa"
                self.space.add(self.mouse_joint)
                self.mouse_dragging = True

        elif event.type == pygame.MOUSEMOTION:
            self.mouse_body.position = event.pos

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.mouse_dragging:
                self.space.remove(self.mouse_joint)
                self.mouse_joint = None
                self.mouse_dragging = False

    def update_game_logic(self):
        # 1. Avanzamos la simulación de físicas
        dt = 1.0 / self.fps
        self.space.step(dt)

        # 2. Actualizamos los sprites para que sigan a sus cuerpos físicos
        self.sprites.update()

    def draw_game_elements(self):
        self.screen.fill((210, 220, 230))  # Fondo gris claro
        self.sprites.draw(self.screen)
