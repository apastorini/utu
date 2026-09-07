# arkanoid/main.py
from arkanoid.game import ArkanoidGame


def main():
    """Punto de entrada principal para lanzar el juego."""
    juego = ArkanoidGame()
    juego.run()

if __name__ == '__main__':
    main()