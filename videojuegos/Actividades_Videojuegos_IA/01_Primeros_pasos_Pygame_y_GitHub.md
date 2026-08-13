# Actividad 1 — Primeros pasos: Pygame, Python y GitHub

**Duración:** 50 min · **Modalidad:** individual · **Entrega:** repo GitHub público

## 1. Objetivos

- Configurar Python, Pygame y un repositorio GitHub personal.
- Comprender el **bucle principal** de un videojuego.
- Crear una ventana y mover una figura con el teclado.
- Hacer el primer `commit` y `push` a GitHub.

## 2. Marco teórico

Un videojuego, en su forma más simple, es un programa que repite **sin parar** tres pasos:

1. **Leer la entrada** (teclado, mouse, joystick).
2. **Actualizar el estado** (posiciones, puntajes, vidas).
3. **Dibujar** el resultado en pantalla.

Ese ciclo infinito se llama **bucle de juego** (*game loop*). En Python lo escribimos con un `while True` y un reloj (`Clock`) que limita la velocidad a 60 cuadros por segundo (FPS).

**Pygame** es una biblioteca open source de Python que nos da: ventanas, dibujo de figuras, sonido, teclado, mouse e imágenes. Es ideal para aprender porque cada concepto se ve directamente.

**Git y GitHub**: Git guarda versiones de nuestro código ("fotos" llamadas *commits*). GitHub aloja esas versiones en internet y nos permite tener un portafolio público y trabajar desde cualquier máquina.

## 3. Instalación

```powershell
# Verificá que Python esté instalado
python --version

# Instalá Pygame
pip install pygame

# Verificá la instalación
python -c "import pygame; print(pygame.version.ver)"
```

> Si no tenés Python, descargalo de https://www.python.org/downloads/ y marcá la casilla "Add Python to PATH".

## 4. Paso a paso

### 4.1 Creá tu repositorio GitHub

1. Entrá a https://github.com y creá tu cuenta.
2. Botón **New repository** → nombre: `mis-videojuegos` → **Public** → marcar "Add a README file" → Create.
3. Copiá el enlace HTTPS del repo (queda algo así: `https://github.com/tuusuario/mis-videojuegos.git`).

### 4.2 Descargá el repo y prepará la carpeta de la clase

```powershell
git clone https://github.com/tuusuario/mis-videojuegos.git
cd mis-videojuegos
mkdir clase_01_primeros_pasos
```

### 4.3 Escribí el primer juego

Creá el archivo `clase_01_primeros_pasos/juego.py` con este contenido:

```python
import sys
import pygame

pygame.init()

ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Mi primer juego")
reloj = pygame.time.Clock()

x, y = 100, 100          # posición del cuadrado
velocidad = 5

ejecutando = True
while ejecutando:
    # 1) LEER ENTRADA
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT]:
        x -= velocidad
    if teclas[pygame.K_RIGHT]:
        x += velocidad
    if teclas[pygame.K_UP]:
        y -= velocidad
    if teclas[pygame.K_DOWN]:
        y += velocidad

    # 2) ACTUALIZAR (no hace falta en este juego tan simple)

    # 3) DIBUJAR
    pantalla.fill((20, 20, 40))                    # fondo
    pygame.draw.rect(pantalla, (0, 200, 255), (x, y, 50, 50))
    pygame.display.flip()

    reloj.tick(60)   # máximo 60 FPS

pygame.quit()
sys.exit()
```

### 4.4 Ejecutá el juego

```powershell
python clase_01_primeros_pasos/juego.py
```

Debés ver una ventana azul oscuro con un cuadrado celeste que se mueve con las flechas.

### 4.5 Probalo con IA

Pedile al asistente de IA que **explique** el código, línea por línea, antes de seguir. Luego pedile una variación (ver sección 6).

### 4.6 Publicá en GitHub

```powershell
git add .
git commit -m "Clase 01: primera ventana y movimiento"
git push
```

## 5. Actividad de cierre (para que quede en el commit)

Modificá el juego para que el cuadrado **no pueda salir de la pantalla**:

```python
x = max(0, min(ANCHO - 50, x))
y = max(0, min(ALTO - 50, y))
```

Agregá esta línea justo después de leer el teclado y volvé a probar. Hacé otro commit con el mensaje `Clase 01: límites de pantalla`.

## 6. Usando IA en esta clase (prompts sugeridos)

> **Prompt 1 (entender):** "Explicame línea por línea este código de Pygame, como si tuviera 15 años: [pegá tu código]".
>
> **Prompt 2 (variar):** "Modificá el programa para que el cuadrado cambie de color cada vez que toco una tecla. Mostrame solo el código completo."
>
> **Prompt 3 (depurar):** "El cuadrado no se mueve. Mi código es este: [pegá el código]. ¿Qué está mal?"

> Regla: probá primero, y recién después mostrale el error a la IA. Nunca copies la respuesta sin entenderla.

## 7. Rúbrica de evaluación

| Criterio | Logrado | En proceso | No logrado |
|---|---|---|---|
| Instaló Python y Pygame | Corre sin errores | Instaló pero con ayuda | No instaló |
| Entiende el bucle de juego | Explica los 3 pasos | Lo nombra pero no lo explica | No lo menciona |
| Mueve la figura con el teclado | Funciona | Funciona a medias | No funciona |
| Subió a GitHub | 2 commits con mensajes claros | 1 commit | Sin repo |
