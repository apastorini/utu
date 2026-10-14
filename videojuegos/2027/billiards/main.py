# billiards/main.py
"""Ejecutar desde la carpeta 2027 con:  python -m billiards.main"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from billiards.game import BilliardsGame


def main():
    BilliardsGame().run()


if __name__ == "__main__":
    main()
