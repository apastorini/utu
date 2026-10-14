# video_demo/main.py
"""Ejecutar desde la carpeta 2027 con:  python -m video_demo.main"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from video_demo.game import VideoDemoGame


def main():
    VideoDemoGame().run()


if __name__ == "__main__":
    main()
