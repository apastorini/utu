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
        "file": "clase_01_02_pygame_basico.md",
        "title": "Clases 1 y 2 — Pensar como diseñador y primeros pasos con Pygame",
        "intro": (
            "Objetivo: **pensar como diseñador** y dar los primeros pasos con Pygame:\n"
            "abrir una ventana, montar el **bucle principal** (game loop), dibujar\n"
            "formas y mover un rectángulo con el teclado.\n\n"
            "En esta etapa **todavía no hay motor**: es Pygame \"puro\", todo en un\n"
            "archivo. A partir de la clase 8 esto se convertirá en `engine/`."
        ),
        "engine": [],
        "code_title": "Ejercicio de la clase — código completo",
        "game": ["clases/paso_a_paso/clase_1_2.py"],
        "run": "python clases/paso_a_paso/clase_1_2.py",
        "controls": "flechas para mover el rectángulo; cerrar la ventana para salir.",
    },
    {
        "file": "clase_03_04_rectangulos_colisiones.md",
        "title": "Clases 3 y 4 — Rectángulos, movimiento y colisiones",
        "intro": (
            "Objetivo: trabajar con **rectángulos** (`pygame.Rect`), movimiento,\n"
            "límites de pantalla y **detección de colisiones** básica.\n\n"
            "Son cuatro variantes del mismo ejercicio que van sumando: mover, chocar\n"
            "contra los bordes y detectar solapamientos entre rectángulos."
        ),
        "engine": [],
        "code_title": "Ejercicios de la clase — código completo",
        "game": [
            "clases/paso_a_paso/clase_3_4_a.py",
            "clases/paso_a_paso/clase_3_4_b.py",
            "clases/paso_a_paso/clase_3_4_c.py",
            "clases/paso_a_paso/clase_3_4_d.py",
        ],
        "run": "python clases/paso_a_paso/clase_3_4_a.py   # y b, c, d",
        "controls": "flechas para mover; cada variante añade una idea nueva.",
    },
    {
        "file": "clase_05_delta_fps_colisiones.md",
        "title": "Clase 5 — Delta de tiempo, FPS, teclado y colisiones",
        "intro": (
            "Objetivo: que el movimiento **no dependa de los FPS** usando el\n"
            "**delta de tiempo** (`dt`), controlar la velocidad con el reloj, y\n"
            "distinguir los **eventos** de teclado (`KEYDOWN`, un evento puntual) del\n"
            "**estado** de las teclas (`pygame.key.get_pressed()`, continuo).\n\n"
            "También se afinan las colisiones vistas en la clase anterior."
        ),
        "engine": [],
        "code_title": "Ejercicios de la clase — código completo",
        "game": [
            "clases/paso_a_paso/clase_5_1.py",
            "clases/paso_a_paso/clase_5_2.py",
        ],
        "run": "python clases/paso_a_paso/clase_5_1.py   # y clase_5_2.py",
        "controls": "flechas/teclas según el ejercicio; se muestra el FPS en pantalla.",
    },
    {
        "file": "clase_06_sprites_sonido_spritesheet.md",
        "title": "Clase 6 — Sprites, sonido y animación con spritesheet",
        "intro": (
            "Objetivo: usar **sprites**, reproducir **sonido** y **animar** con una\n"
            "**spritesheet** (recortando fotogramas de una sola imagen).\n\n"
            "Aparece el primer `core/` con clases propias (`Player`, `Enemy`,\n"
            "`Collectible`...) que es el antecedente directo de `engine/game_object.py`\n"
            "y del concepto de animación del motor."
        ),
        "engine": [],
        "code_title": "Ejercicio y su 'core' — código completo",
        "game": [
            "clases/paso_a_paso/clase_6_a.py",
            "clases/paso_a_paso/core/__init__.py",
            "clases/paso_a_paso/core/Player.py",
            "clases/paso_a_paso/core/PlayerRect.py",
            "clases/paso_a_paso/core/Enemy.py",
            "clases/paso_a_paso/core/Collectible.py",
            "clases/paso_a_paso/core/Colors.py",
            "clases/paso_a_paso/core/utils/__init__.py",
            "clases/paso_a_paso/core/utils/utils.py",
        ],
        "run": "python clases/paso_a_paso/clase_6_a.py",
        "controls": "flechas para mover; el personaje se anima y recoge objetos.",
    },
    {
        "file": "clase_07_arkanoid.md",
        "title": "Clase 7 — Arkanoid (de un archivo a módulos)",
        "intro": (
            "Objetivo: programar el primer **Arkanoid** completo. Se empieza con todo\n"
            "en un archivo y luego se **separa en módulos** dentro de\n"
            "`core_arkanoid/` (`Player`, `Ball`, `Brick`, `SpriteSheet`), con una\n"
            "segunda versión que ya carga sprites con un spritesheet.\n\n"
            "Este es el **antecedente directo** de la reestructuración del motor de la\n"
            "clase 8 (`engine/` + `arkanoid/` con escenas)."
        ),
        "engine": [],
        "code_title": "Juego de ejemplo — código completo",
        "game": [
            "clases/paso_a_paso/arkanoid/core_arkanoid/__init__.py",
            "clases/paso_a_paso/arkanoid/core_arkanoid/clase_7_arkanoid.py",
            "clases/paso_a_paso/arkanoid/core_arkanoid/Player.py",
            "clases/paso_a_paso/arkanoid/core_arkanoid/Ball.py",
            "clases/paso_a_paso/arkanoid/core_arkanoid/Brick.py",
            "clases/paso_a_paso/arkanoid/core_arkanoid/SpriteSheet.py",
            "clases/paso_a_paso/arkanoid/core_arkanoid/sprite_sheet/__init__.py",
            "clases/paso_a_paso/arkanoid/core_arkanoid/sprite_sheet/Game.py",
            "clases/paso_a_paso/arkanoid/core_arkanoid/sprite_sheet/Player.py",
            "clases/paso_a_paso/arkanoid/core_arkanoid/sprite_sheet/Ball.py",
            "clases/paso_a_paso/arkanoid/core_arkanoid/sprite_sheet/Brick.py",
            "clases/paso_a_paso/arkanoid/core_arkanoid/sprite_sheet/visor_sprites.py",
        ],
        "run": "cd clases/paso_a_paso\npython -m arkanoid.core_arkanoid.clase_7_arkanoid",
        "controls": "flechas para mover la paleta; `ESC`/cerrar la ventana para salir. (La segunda versión, con sprites cargados de spritesheet, está en `sprite_sheet/Game.py`.)",
    },
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
    for enc in ("utf-8", "cp1252", "latin-1"):
        try:
            with open(full, encoding=enc) as f:
                return f.read().rstrip("\n")
        except UnicodeDecodeError:
            continue
    with open(full, encoding="utf-8", errors="replace") as f:
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

    code_title = spec.get("code_title", "Juego de ejemplo — código completo")
    lines.append(f"## {code_title}\n")
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
