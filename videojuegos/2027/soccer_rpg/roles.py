# soccer_rpg/roles.py
"""
Definición de los roles jugables y sus atributos (0-100).

Se separa de `game.py` para evitar importaciones circulares: las escenas
necesitan los roles, pero el juego importa las escenas.
"""

ROLES = {
    "Delantero": {
        "ataque": 88, "defensa": 46, "energia": 85,
        "desc": "Pura potencia ofensiva. Mucho gol, poca defensa.",
        "sprite": "jugador_delantero",
        "color": (225, 60, 60),
    },
    "Mediocampista": {
        "ataque": 66, "defensa": 66, "energia": 95,
        "desc": "Equilibrado. Mueve el equipo y decide las jugadas.",
        "sprite": "jugador_mediocampista",
        "color": (60, 110, 230),
    },
    "Defensor": {
        "ataque": 46, "defensa": 88, "energia": 100,
        "desc": "Muro atras. Corta ataques y aguanta toda la energia.",
        "sprite": "jugador_defensor",
        "color": (60, 180, 110),
    },
}
