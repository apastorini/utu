# soccer_rpg/main.py
"""Ejecutar desde la carpeta 2027 con:  python -m soccer_rpg.main"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from soccer_rpg.game import SoccerRpgGame


def main():
    SoccerRpgGame().run()


if __name__ == "__main__":
    main()
