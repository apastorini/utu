# wrestling/main.py
"""Ejecutar desde la carpeta 2027 con:  python -m wrestling.main"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from wrestling.game import WrestlingGame


def main():
    WrestlingGame().run()


if __name__ == "__main__":
    main()
