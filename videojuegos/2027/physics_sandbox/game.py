# physics_sandbox/game.py
"""
Sandbox de físicas usando el enfoque GAME LOOP (herencia directa de
GameLoop, SIN escenas). Es el ejemplo más claro de que el motor soporta
los dos enfoques.
"""
import pygame
import pymunk

from engine.game_loop import GameLoop
from physics_sandbox.entities import PhysicsCircle, PhysicsBox


class PhysicsGame(GameLoop):
    def __init__(self):
        super().__init__(1280, 720, "Sandbox de Físicas con PyMunk", 60)

        # Espacio de físicas
        self.space = pymunk.Space()
        self.space.gravity = (0, 900)

        self.sprites = pygame.sprite.Group()
        self.create_boundaries()
        self.crear_objetos_iniciales()

        # Arrastrar con el ratón
        self.mouse_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        self.mouse_joint = None
        self.mouse_dragging = False

    def crear_objetos_iniciales(self):
        self.sprites.add(
            PhysicsBox(600, 600, 50, 50, self.space),
            PhysicsBox(600, 550, 50, 50, self.space),
            PhysicsCircle(650, 600, 30, self.space),
        )

    def create_boundaries(self):
        floor = pymunk.Segment(self.space.static_body,
                               (0, self.screen.get_height() - 5),
                               (self.screen.get_width(), self.screen.get_height() - 5), 5)
        floor.elasticity = 0.8
        floor.friction = 1.0

        wall_left = pymunk.Segment(self.space.static_body, (5, 0),
                                   (5, self.screen.get_height()), 5)
        wall_right = pymunk.Segment(self.space.static_body,
                                    (self.screen.get_width() - 5, 0),
                                    (self.screen.get_width() - 5, self.screen.get_height()), 5)

        self.space.add(floor, wall_left, wall_right)

    # ------------------------- Hooks de GameLoop ------------------------- #
    def handle_specific_events(self, event):
        if event.type == pygame.KEYDOWN:
            pos = pygame.mouse.get_pos()
            if event.key == pygame.K_c:
                self.sprites.add(PhysicsCircle(pos[0], pos[1], 30, self.space))
            elif event.key == pygame.K_b:
                self.sprites.add(PhysicsBox(pos[0], pos[1], 50, 50, self.space))

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            query = self.space.point_query_nearest(event.pos, 0, pymunk.ShapeFilter())
            if query and query.shape.body.body_type == pymunk.Body.DYNAMIC:
                shape = query.shape
                self.mouse_joint = pymunk.PivotJoint(
                    self.mouse_body, shape.body,
                    shape.body.world_to_local(event.pos),
                )
                self.mouse_joint.max_force = 70000
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
        self.space.step(1.0 / self.fps)
        self.sprites.update()

    def draw_game_elements(self):
        self.screen.fill((210, 220, 230))
        self.sprites.draw(self.screen)
