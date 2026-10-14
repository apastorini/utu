# Videojuegos 2027 — motor único + juegos de ejemplo + apuntes

Versión nueva y **alineada** del material: un solo motor (`engine/`) que soporta
los dos enfoques (Game Loop y Game Scenes), juegos de ejemplo completos y los
apuntes de cada clase.

- La copia del material anterior está en `../2026/` (no se ha borrado nada).
- La guía de clases (orden y contenido) está en `clases/00_orden_y_guia.md`.

## Estructura

```
2027/
├─ engine/              # EL MOTOR (uno solo, igual para todos los juegos)
│  ├─ game_loop.py      # GameLoop (herencia) + Game (gestor de escenas)
│  ├─ ui.py             # Scene + Button
│  ├─ game_object.py    # sprite estático o animado
│  ├─ sprite_sheet.py   # lector de spritesheets (JSON + PNG)
│  ├─ asset_manager.py  # carga de imágenes/sprites por nombre
│  ├─ audio.py          # música y efectos
│  ├─ physics.py        # PhysicsMixin (PyMunk)
│  ├─ tilemap.py        # niveles de Tiled -> grupos de sprites
│  ├─ camera.py         # scrolling
│  ├─ dialogue_manager.py
│  ├─ iso_tools.py      # (13)  perspectiva isométrica
│  ├─ timeline.py       # (14)  líneas de tiempo / tweens
│  ├─ recorder.py       # (14)  grabar frames -> PNG/vídeo
│  ├─ background.py     # (14b) parallax / fondo de vídeo
│  ├─ particle.py       # (14b) sistema de partículas
│  ├─ physics_object.py # (17)  cuerpos de PyMunk reutilizables
│  ├─ hotspot.py        # (21)  zonas interactivas
│  ├─ inventory.py      # (21)  inventario
│  ├─ cursor.py         # (21)  cursor personalizado
│  ├─ dialogue.py       # (21)  diálogos ramificados
│  ├─ challenge.py      # (24)  retos con tiempo
│  ├─ ui_elements.py    # (24)  etiquetas, paneles, barras
│  ├─ shared_assets.py  # rutas a los assets comunes
│  └─ utils/            # colores, constantes, helpers
├─ assets/              # sonidos y música comunes (generados)
│  ├─ sonidos/*.wav
│  └─ musica/*.wav
├─ herramientas/        # generación de assets y de apuntes
│  ├─ genlib.py         # sintetizador de audio + dibujo con Pillow
│  └─ generar_apuntes.py
├─ arkanoid/            # ejemplo: ESCENAS + audio + niveles
├─ platformer/          # ejemplo: ESCENAS + tilemap + cámara
├─ physics_sandbox/     # ejemplo: GAME LOOP (sin escenas)
├─ wrestling/           # (13)  isométrica  — GAME LOOP
├─ animator/            # (14)  animación   — GAME LOOP
├─ video_demo/          # (14b) fondos     — GAME LOOP
├─ billiards/           # (17-19) billar   — GAME LOOP
├─ slingshot/           # (20)  resortera  — GAME LOOP
├─ adventure/           # (21-23) aventura — ESCENAS
├─ insult_soccer/       # (24-25) fútbol verbal — ESCENAS
├─ soccer_rpg/          # (26)  fútbol RPG — ESCENAS
├─ clases/              # apuntes por clase (con el código completo)
├─ requirements.txt
└─ README.md
```

## Ejecutar

```bash
pip install -r requirements.txt

# Núcleo (clases 8-12)
python -m arkanoid.main
python -m platformer.main
python -m physics_sandbox.main

# Clases 13-26
python -m wrestling.main
python -m animator.main
python -m video_demo.main
python -m billiards.main
python -m slingshot.main
python -m adventure.main
python -m insult_soccer.main
python -m soccer_rpg.main
```

## Assets: no hay que descargar nada

Los gráficos, sonidos y música se **generan** (de forma reproducible):

```bash
python herramientas/genlib.py          # sonidos + música comunes en assets/
python wrestling/generar_assets.py     # gráficos de ese juego (igual en los demás)
```

- **Sonidos comunes**: `blip, hit, jump, coin, bounce, splash, whistle, cheer,
  kick, punch, explode, click, correct, wrong, type, shot`.
- **Música común**: `menu, game, wrestling, soccer, adventure, calm`.
- El audio se sintetiza con `numpy` + el módulo `wave`; los gráficos se dibujan
  con `Pillow`. No se necesita conexión a internet.
- El audio es **opcional**: si no hay tarjeta de sonido, el juego sigue.
- El fondo de **vídeo en tiempo real** (`VideoBackground`) requiere
  `opencv-python`; si no está, se desactiva solo (el ejemplo `video_demo` usa
  igualmente un fondo "vídeo" hecho con una secuencia de PNG).

## Apuntes por clase

En `clases/` están `clase_01_*.md` … `clase_26_*.md`, cada uno con el **código
completo** del motor y del juego/ejercicio de esa etapa (las clases 1–7 no
tienen motor todavía: son ejercicios de Pygame "puro").

Los apuntes de las **clases 1–7 y 13–26** se generan desde el código real:

```bash
python herramientas/generar_apuntes.py
```

(Los de las clases **8–12** son redactados a mano y no los sobrescribe el
generador.)

## Los dos enfoques, en 3 líneas

```python
# Enfoque 1: Game Loop (herencia)
from engine.game_loop import GameLoop
class MiJuego(GameLoop):
    def update_game_logic(self): ...
    def draw_game_elements(self): ...

# Enfoque 2: Game Scenes
from engine.game_loop import Game
class MiJuego(Game):
    def __init__(self):
        super().__init__(800, 600, "Mi juego", 60)
        self.add_scene("menu", MenuScene)
        self.change_scene("menu")
```
