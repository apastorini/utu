# animator/main.py
"""Ejecutar desde la carpeta 2027 con:  python -m animator.main"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from animator.game import AnimatorGame


def main():
    AnimatorGame().run()


if __name__ == "__main__":
    main()
