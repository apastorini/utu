# slingshot/main.py
"""Ejecutar desde la carpeta 2027 con:  python -m slingshot.main"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from slingshot.game import SlingshotGame


def main():
    SlingshotGame().run()


if __name__ == "__main__":
    main()
