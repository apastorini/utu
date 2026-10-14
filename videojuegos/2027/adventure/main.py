# adventure/main.py
"""
Ejecutar desde la carpeta 2027 con:
    python -m adventure.main
o directamente:
    python adventure/main.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from adventure.game import AdventureGame


def main():
    AdventureGame().run()


if __name__ == "__main__":
    main()
