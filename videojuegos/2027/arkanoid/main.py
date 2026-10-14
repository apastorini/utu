# arkanoid/main.py
"""
Ejecutar desde la carpeta 2027 con:
    python -m arkanoid.main
o directamente:
    python arkanoid/main.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from arkanoid.game import ArkanoidGame


def main():
    ArkanoidGame().run()


if __name__ == "__main__":
    main()
