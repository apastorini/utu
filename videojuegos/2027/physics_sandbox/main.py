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
