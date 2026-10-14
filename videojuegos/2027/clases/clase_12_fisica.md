# Clase 12 — Física con PyMunk

Objetivo: añadir **físicas reales** al motor mediante composición (mixin).
`engine/physics.py` (`PhysicsMixin`) da a cualquier `GameObject` un cuerpo
y un collider de PyMunk (círculo o caja).

El sandbox de físicas es el ejemplo canónico del **enfoque Game Loop**:
hereda directamente de `GameLoop` y sobrescribe sus hooks, sin escenas.

## Motor — nuevo módulo: física (código completo)

**`engine/physics.py`**

```python
"""
engine/physics.py

`PhysicsMixin` añade físicas de PyMunk a un GameObject usando herencia
múltiple:

    class Bola(GameObject, PhysicsMixin):
        def __init__(self, x, y, r, space):
            super().__init__(x, y, imagen)
            self.original_image = self.image
            self.init_physics_circle(space, mass=10, radius=r,
                                     elasticity=0.6, friction=0.8)

        def update(self):
            self.update_from_physics()
"""

import math

import pygame
import pymunk


class PhysicsMixin:
    """Añade un cuerpo/collider de PyMunk a un GameObject."""

    def init_physics_circle(self, space, mass, radius, elasticity, friction):
        """Crea un cuerpo físico circular."""
        moment = pymunk.moment_for_circle(mass, 0, radius)
        self.body = pymunk.Body(mass, moment)
        self.body.position = self.rect.center
        self.shape = pymunk.Circle(self.body, radius)
        self.shape.elasticity = elasticity
        self.shape.friction = friction
        self.shape.parent = self  # referencia inversa al objeto del juego
        space.add(self.body, self.shape)

    def init_physics_box(self, space, mass, elasticity, friction):
        """Crea un cuerpo físico rectangular."""
        size = self.rect.size
        moment = pymunk.moment_for_box(mass, size)
        self.body = pymunk.Body(mass, moment)
        self.body.position = self.rect.center
        self.shape = pymunk.Poly.create_box(self.body, size)
        self.shape.elasticity = elasticity
        self.shape.friction = friction
        self.shape.parent = self
        space.add(self.body, self.shape)

    def update_from_physics(self):
        """Sincroniza la posición y la rotación del sprite con el cuerpo."""
        self.rect.center = self.body.position
        # PyMunk usa radianes; Pygame usa grados.
        self.image = pygame.transform.rotate(
            self.original_image, -math.degrees(self.body.angle)
        )
        self.rect = self.image.get_rect(center=self.rect.center)
```


## Juego de ejemplo — Sandbox de físicas (código completo)

**`physics_sandbox/__init__.py`**

```python
# physics_sandbox/__init__.py
```

**`physics_sandbox/entities.py`**

```python
# physics_sandbox/entities.py
import pygame

from engine.game_object import GameObject
from engine.physics import PhysicsMixin


class PhysicsCircle(GameObject, PhysicsMixin):
    def __init__(self, x, y, radius, space):
        image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(image, (200, 30, 30), (radius, radius), radius)

        super().__init__(x, y, image)
        self.original_image = self.image  # para la rotación

        self.init_physics_circle(space, mass=10, radius=radius,
                                 elasticity=0.6, friction=0.8)

    def update(self, *args, **kwargs):
        self.update_from_physics()


class PhysicsBox(GameObject, PhysicsMixin):
    def __init__(self, x, y, width, height, space):
        image = pygame.Surface((width, height), pygame.SRCALPHA)
        image.fill((30, 30, 200))

        super().__init__(x, y, image)
        self.original_image = self.image

        self.init_physics_box(space, mass=15, elasticity=0.4, friction=0.9)

    def update(self, *args, **kwargs):
        self.update_from_physics()
```

**`physics_sandbox/game.py`**

```python
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
```

**`physics_sandbox/main.py`**

```python
# physics_sandbox/main.py
"""
Ejecutar desde la carpeta 2027 con:
    python -m physics_sandbox.main
o directamente:
    python physics_sandbox/main.py

Requiere: pip install pymunk
Controles: 'C' círculo, 'B' caja, clic + arrastrar, ESC/cerrar ventana para salir.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from physics_sandbox.game import PhysicsGame


def main():
    PhysicsGame().run()


if __name__ == "__main__":
    main()
```

