# Clases del curso de Videojuegos — orden y contenido (2027)

Este documento ordena TODAS las clases y dice, para cada una:

- **Tema** y objetivo.
- **Código del motor** que se construye/usa en esa clase.
- **Juego de ejemplo** que se desarrolla.
- **Dónde está el código** en este `2027/`.

> Cómo leer: el motor (`engine/`) es **uno solo** y va creciendo clase a clase.
> Cada clase añade módulos nuevos y un juego de ejemplo. Los documentos
> `clase_XX_*.md` de esta misma carpeta incluyen el **código completo**
> (motor + ejemplo) de cada etapa, para que ninguna clase quede con fragmentos.

---

## Los dos enfoques del motor

El motor soporta los dos enfoques de trabajo (importante para clases 8 en adelante):

| Enfoque | Clase base | Cuándo usarlo | Ejemplo |
|---|---|---|---|
| **Game Loop** (herencia) | `engine.game_loop.GameLoop` | Demos y juegos de un solo estado | `physics_sandbox/` (clase 12) |
| **Game Scenes** (escenas) | `engine.game_loop.Game` + `engine.ui.Scene` | Juegos con menú, juego, game over, niveles | `arkanoid/`, `platformer/` |

Ambos comparten el mismo bucle `run()`, el mismo `clock`, la misma ventana y los
mismos módulos de assets, audio, spritesheets, tilemaps, cámara, UI, etc.

---

## Orden de las clases

| # | Tema | Código del motor | Juego / ejemplo | Estado |
|---|------|------------------|-----------------|--------|
| 1–4 | Pensar como diseñador + primeros pasos Pygame (ventana, bucle, rectángulos, movimiento, colisiones) | — (Pygame puro) | Ejercicios de rectángulos | ✅ — ver `clase_01_02_pygame_basico.md` y `clase_03_04_rectangulos_colisiones.md` |
| 5 | Delta de tiempo, FPS, teclado evento vs estado, colisiones | — | Ejercicios | ✅ — ver `clase_05_delta_fps_colisiones.md` |
| 6 | Sprites, sonido y animación con spritesheet | — (primer `game_object`) | Ejemplo con sprites | ✅ — ver `clase_06_sprites_sonido_spritesheet.md` |
| 7 | Arkanoid (de un archivo a módulos) | — | Arkanoid básico | ✅ — ver `clase_07_arkanoid.md` |
| 8 | **Reestructuración del motor** (núcleo) | `game_loop`, `ui`, `game_object`, `sprite_sheet`, `asset_manager`, `dialogue_manager`, `utils/` | Arkanoid refactorizado | ✅ `engine/` + `arkanoid/` — ver `clase_08_*.md` |
| 9 | Audio y gestión de niveles | `audio` + `level_loader` + escenas | Arkanoid con vidas/niveles/menú/game over | ✅ — ver `clase_09_*.md` |
| 10–11 | Juegos de plataforma | `tilemap`, `camera` + entidades | Plataformero con Tiled y cámara | ✅ — ver `clase_10_11_*.md` |
| 12 | Física con PyMunk | `physics` (mixin) | Sandbox de físicas (enfoque Game Loop) | ✅ — ver `clase_12_*.md` |
| 13 | Perspectiva isométrica | `iso_tools` | Lucha libre isométrica (`wrestling/`) | ✅ — ver `clase_13_isometrica.md` |
| 14 | Animación avanzada (timeline, grabación, FFmpeg) | `timeline`, `recorder` | Animador (`animator/`) | ✅ — ver `clase_14_animacion.md` |
| 14b | Fondos dinámicos: parallax, vídeo y partículas | `background`, `particle` | `video_demo/` | ✅ — ver `clase_14b_fondos.md` |
| 17–19 | Física de objetos y billar | `physics_object` | Billar (`billiards/`) | ✅ — ver `clase_17_19_billar.md` |
| 20 | Resortes, bloques y destrucción | (reutiliza `physics_object`) | Resortera (`slingshot/`) | ✅ — ver `clase_20_resortera.md` |
| 21–23 | Aventura gráfica | `hotspot`, `inventory`, `cursor`, `dialogue` | `adventure/` | ✅ — ver `clase_21_23_aventura.md` |
| 24–25 | Retos y UI | `challenge`, `ui_elements` | Fútbol verbal (`insult_soccer/`) | ✅ — ver `clase_24_25_futbol_verbal.md` |
| 26 | Fútbol con roles y progresión | (reutiliza `ui_elements`) | Fútbol RPG (`soccer_rpg/`) | ✅ — ver `clase_26_futbol_rpg.md` |

> ✅ = implementado, con assets generados y **probado headless** en esta carpeta.
> Todos los apuntes `clase_XX_*.md` incluyen el **código completo** (motor +
> juego de ejemplo). Los apuntes se pueden regenerar desde el código real con
> `python herramientas/generar_apuntes.py`.

### Assets (gráficos, sonidos y música)

No se descarga nada: los assets se **generan** de forma reproducible.

- Gráficos y audio común: `python herramientas/genlib.py` (crea
  `assets/sonidos/*.wav` y `assets/musica/*.wav`).
- Gráficos de cada juego: `python <juego>/generar_assets.py`
  (por ejemplo `python wrestling/generar_assets.py`).

Los juegos buscan la música y los efectos comunes con
`engine.shared_assets.sfx_path("...")` / `music_path("...")`.

---

## Cómo ejecutar

Desde la carpeta `2027/`:

```bash
# (opcional) entorno
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

# Arkanoid (enfoque de escenas)
python -m arkanoid.main

# Plataformero (escenas + tilemap + cámara)
python -m platformer.main

# Sandbox de físicas (enfoque Game Loop)
python -m physics_sandbox.main

# Clases 13-26
python -m wrestling.main        # isométrica
python -m animator.main         # animación + grabación
python -m video_demo.main       # fondos dinámicos / parallax / partículas
python -m billiards.main        # billar (PyMunk)
python -m slingshot.main        # resortera (PyMunk)
python -m adventure.main        # aventura gráfica (escenas)
python -m insult_soccer.main    # fútbol de duelo verbal (escenas)
python -m soccer_rpg.main       # fútbol RPG (escenas)
```

### Clases 1-7 (ejercicios, Pygame "puro", dentro de `clases/paso_a_paso/`)

```bash
python clases/paso_a_paso/clase_1_2.py
python clases/paso_a_paso/clase_3_4_a.py       # y b, c, d
python clases/paso_a_paso/clase_5_1.py         # y clase_5_2.py
python clases/paso_a_paso/clase_6_a.py

# Clase 7 (Arkanoid): se ejecuta como módulo desde clases/paso_a_paso
cd clases/paso_a_paso
python -m arkanoid.core_arkanoid.clase_7_arkanoid
```

También funciona `python arkanoid/main.py` (cada `main.py` ajusta el `sys.path`).

### Controles

- **Arkanoid**: `←/→` mover, botón "Jugar", `ESC` menú.
- **Plataformero**: `←/→` mover, `SPACE` saltar, `ESC` menú.
- **Sandbox de físicas**: `C` círculo, `B` caja, clic y arrastrar.
- **Lucha isométrica**: `WASD` mover, `J`/`ESPACIO` golpear, `R` revancha.
- **Animador**: `1-4` animación, `ESPACIO` pausa, `R` grabar 3 s.
- **Fondos dinámicos**: `←/→` desplazar, `V` parallax/vídeo, `W` clima.
- **Billar**: click mantenido para cargar, soltar para tirar, `R` reiniciar.
- **Resortera**: arrastrar el pájaro y soltar, `R` reiniciar.
- **Aventura**: click en hotspots; flechas + `ENTER` en los diálogos.

---

## Relación con las carpetas originales

- `2026/` → copia de seguridad del material **anterior** (notebooks y `Clases/`).
  No se ha borrado nada: es exactamente lo que había antes de esta revisión.
- `2027/` → versión nueva y alineada: **un motor único** (`engine/`) + juegos de
  ejemplo + esta guía de clases.

Los notebooks originales están en `2026/notebooks/` y el código original en
`2026/Clases/`.
