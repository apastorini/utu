"""
herramientas/generar_apuntes.py

Genera los apuntes de las clases 13 a 26 a partir del CÓDIGO REAL, para que
cada documento contenga siempre el código completo y sincronizado:

- Los módulos del motor que introduce la clase (código completo).
- El juego de ejemplo completo (todos sus archivos .py).
- Cómo ejecutarlo y sus controles.

Uso:  python herramientas/generar_apuntes.py
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLASES = os.path.join(ROOT, "clases")


DOCS = [
    {
        "file": "clase_13_isometrica.md",
        "title": "Clase 13 — Perspectiva isométrica",
        "intro": (
            "Objetivo: dibujar un mundo con **perspectiva isométrica** (la típica\n"
            "vista 2:1, como en los juegos de estrategia).\n\n"
            "El módulo `engine/iso_tools.py` convierte coordenadas de rejilla\n"
            "cuadrada a coordenadas de pantalla \"en rombo\" y al revés, y ordena\n"
            "los sprites por **profundidad** para que lo que está más atrás se\n"
            "dibuje primero.\n\n"
            "El juego de ejemplo es una **lucha libre isométrica** con el enfoque\n"
            "**Game Loop** (herencia de `GameLoop`, sin escenas)."
        ),
        "engine": ["engine/iso_tools.py", "engine/shared_assets.py"],
        "game": [
            "wrestling/__init__.py",
            "wrestling/generar_assets.py",
            "wrestling/game.py",
            "wrestling/main.py",
        ],
        "run": "python -m wrestling.main",
        "controls": "`WASD` mover, `J`/`ESPACIO` golpear, `R` revancha.",
    },
    {
        "file": "clase_14_animacion.md",
        "title": "Clase 14 — Animación avanzada (timeline y grabación)",
        "intro": (
            "Objetivo: **coreografiar** una animación con una línea de tiempo\n"
            "(`engine/timeline.py`) en vez de llenar el bucle de `if`/`elif`, y\n"
            "**grabar** la pantalla a PNG/vídeo (`engine/recorder.py`).\n\n"
            "El juego de ejemplo es un **animador** (enfoque Game Loop) que\n"
            "reproduce animaciones de spritesheet, mueve objetos con *tweens* y\n"
            "graba 3 segundos al pulsar `R`."
        ),
        "engine": ["engine/timeline.py", "engine/recorder.py"],
        "game": [
            "animator/__init__.py",
            "animator/generar_assets.py",
            "animator/game.py",
            "animator/main.py",
        ],
        "run": "python -m animator.main",
        "controls": "`1-4` animación, `ESPACIO` pausa, `R` graba 3 s (PNG/MP4).",
    },
    {
        "file": "clase_14b_fondos.md",
        "title": "Clase 14b — Fondos dinámicos: parallax, vídeo y partículas",
        "intro": (
            "Objetivo: fondos que se mueven. `engine/background.py` trae\n"
            "`ParallaxBackground` (capas a distinta velocidad), `FrameBackground`\n"
            "(reproduce una secuencia de imágenes) y `VideoBackground` (vídeo en\n"
            "tiempo real con OpenCV, opcional). `engine/particle.py` añade un\n"
            "sistema de partículas.\n\n"
            "El ejemplo es `video_demo/` (enfoque Game Loop): parallax con las\n"
            "flechas, lluvia/nieve con partículas y un fondo de \"vídeo\" por frames."
        ),
        "engine": ["engine/background.py", "engine/particle.py"],
        "game": [
            "video_demo/__init__.py",
            "video_demo/generar_assets.py",
            "video_demo/game.py",
            "video_demo/main.py",
        ],
        "run": "python -m video_demo.main",
        "controls": "`←/→` desplazar, `V` parallax/vídeo, `W` clima, `B` ráfaga.",
    },
    {
        "file": "clase_17_19_billar.md",
        "title": "Clases 17 a 19 — Física de objetos y billar",
        "intro": (
            "Objetivo: construir objetos físicos **reutilizables** para no repetir\n"
            "el trabajo de PyMunk. `engine/physics_object.py` aporta\n"
            "`PhysicsObject`, `add_walls`/`add_static_segment` y **tipos de\n"
            "colisión** (constantes) para los callbacks.\n\n"
            "El ejemplo es un **billar** (enfoque Game Loop): mesa con bordes y\n"
            "troneras, taco que apunta y carga potencia, y choques con sonido."
        ),
        "engine": ["engine/physics_object.py"],
        "game": [
            "billiards/__init__.py",
            "billiards/generar_assets.py",
            "billiards/game.py",
            "billiards/main.py",
        ],
        "run": "python -m billiards.main",
        "controls": "click mantenido = cargar, soltar = tirar, `R` reiniciar.",
    },
    {
        "file": "clase_20_resortera.md",
        "title": "Clase 20 — Resortes, bloques y destrucción (resortera)",
        "intro": (
            "Objetivo: un juego tipo *Angry Birds*. Reutiliza\n"
            "`engine/physics_object.py` (de la clase 17) para las paredes, los\n"
            "bloques y el pájaro.\n\n"
            "El ejemplo es `slingshot/` (enfoque Game Loop): arrastras el pájaro\n"
            "para tensar la goma, lo sueltas y derribas bloques y cerdos; los\n"
            "impactos fuertes destruyen (partículas + sonido)."
        ),
        "engine": [],
        "game": [
            "slingshot/__init__.py",
            "slingshot/generar_assets.py",
            "slingshot/game.py",
            "slingshot/main.py",
        ],
        "run": "python -m slingshot.main",
        "controls": "arrastrar el pájaro y soltar; `R` reiniciar.",
    },
    {
        "file": "clase_21_23_aventura.md",
        "title": "Clases 21 a 23 — Aventura gráfica (hotspots, inventario, diálogos)",
        "intro": (
            "Objetivo: una **aventura gráfica** point-and-click.\n"
            "`engine/hotspot.py` (zonas interactivas), `engine/inventory.py`\n"
            "(inventario y objetos), `engine/cursor.py` (puntero propio) y\n"
            "`engine/dialogue.py` (diálogos ramificados).\n\n"
            "El ejemplo es `adventure/` (enfoque **Game + Escenas**): habitaciones\n"
            "conectadas, un NPC con diálogo, una llave y una puerta que se abre\n"
            "solo si la tienes. Se puede **completar**."
        ),
        "engine": [
            "engine/hotspot.py",
            "engine/inventory.py",
            "engine/cursor.py",
            "engine/dialogue.py",
        ],
        "game": [
            "adventure/__init__.py",
            "adventure/game.py",
            "adventure/generar_assets.py",
            "adventure/scenes/__init__.py",
            "adventure/scenes/menu_scene.py",
            "adventure/scenes/juego_scene.py",
            "adventure/scenes/final_scene.py",
            "adventure/main.py",
        ],
        "run": "python -m adventure.main",
        "controls": "click en hotspots; flechas/`WASD` + `ENTER` en los diálogos.",
    },
    {
        "file": "clase_24_25_futbol_verbal.md",
        "title": "Clases 24 y 25 — Retos y UI: fútbol de duelo verbal",
        "intro": (
            "Objetivo: minijuegos de **reto con tiempo** y más **elementos de UI**.\n"
            "`engine/challenge.py` implementa un reto de opción múltiple con\n"
            "temporizador; `engine/ui_elements.py` añade etiquetas, paneles y\n"
            "barras.\n\n"
            "El ejemplo es `insult_soccer/` (enfoque Game + Escenas): un partido por\n"
            "turnos donde ganas el gol eligiendo la mejor respuesta."
        ),
        "engine": ["engine/challenge.py", "engine/ui_elements.py"],
        "game": [
            "insult_soccer/__init__.py",
            "insult_soccer/game.py",
            "insult_soccer/generar_assets.py",
            "insult_soccer/scenes/__init__.py",
            "insult_soccer/scenes/menu_scene.py",
            "insult_soccer/scenes/match_scene.py",
            "insult_soccer/scenes/final_scene.py",
            "insult_soccer/main.py",
        ],
        "run": "python -m insult_soccer.main",
        "controls": "`↑/↓` elegir respuesta, `ENTER` responder.",
    },
    {
        "file": "clase_26_futbol_rpg.md",
        "title": "Clase 26 — Fútbol con roles, atributos y progresión (RPG)",
        "intro": (
            "Objetivo: cerrar el curso con un juego que combina **escenas**,\n"
            "**atributos** y **progresión**. Reutiliza `engine/ui_elements.py`\n"
            "(clase 24) y las escenas (clase 8).\n\n"
            "El ejemplo es `soccer_rpg/` (enfoque Game + Escenas): eliges rol\n"
            "(Delantero/Mediocampista/Defensor: fija ataque/defensa/energía),\n"
            "juegas una secuencia de jugadas y ves un resumen con nivel y XP."
        ),
        "engine": [],
        "game": [
            "soccer_rpg/__init__.py",
            "soccer_rpg/game.py",
            "soccer_rpg/roles.py",
            "soccer_rpg/generar_assets.py",
            "soccer_rpg/scenes/__init__.py",
            "soccer_rpg/scenes/menu_scene.py",
            "soccer_rpg/scenes/seleccion_scene.py",
            "soccer_rpg/scenes/partido_scene.py",
            "soccer_rpg/scenes/resumen_scene.py",
            "soccer_rpg/main.py",
        ],
        "run": "python -m soccer_rpg.main",
        "controls": "elegir con las flechas y `ENTER`.",
    },
]


def read_code(rel_path):
    full = os.path.join(ROOT, rel_path)
    with open(full, encoding="utf-8") as f:
        return f.read().rstrip("\n")


def build_doc(spec):
    lines = []
    lines.append(f"# {spec['title']}\n")
    lines.append(spec["intro"].strip() + "\n")

    if spec["engine"]:
        lines.append("## Motor — código completo de los módulos nuevos\n")
        for rel in spec["engine"]:
            lines.append(f"**`{rel}`**\n")
            lines.append("```python")
            lines.append(read_code(rel))
            lines.append("```\n")

    lines.append("## Juego de ejemplo — código completo\n")
    for rel in spec["game"]:
        lines.append(f"**`{rel}`**\n")
        lines.append("```python")
        lines.append(read_code(rel))
        lines.append("```\n")

    if spec.get("controls"):
        lines.append("## Controles\n")
        lines.append(spec["controls"] + "\n")

    lines.append("## Cómo ejecutar\n")
    lines.append("Desde la carpeta `2027/`:\n")
    lines.append("```bash")
    lines.append(spec["run"])
    lines.append("```\n")
    return "\n".join(lines)


def main():
    os.makedirs(CLASES, exist_ok=True)
    for spec in DOCS:
        content = build_doc(spec)
        path = os.path.join(CLASES, spec["file"])
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print("Escrito", path)
    print(f"\n{len(DOCS)} apuntes generados.")


if __name__ == "__main__":
    main()
