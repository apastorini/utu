# Actividad 3 — El juego de los Cañones (tiro parabólico)

**Duración:** 50 min · **Modalidad:** individual · **Entrega:** repo GitHub público

## 1. Objetivos

- Aplicar **física de movimiento** en un juego (posición, velocidad, gravedad).
- Calcular el **ángulo de tiro** con el mouse usando trigonometría.
- Implementar el **tiro parabólico** (disparo de un proyectil).
- Añadir puntaje y objetos que destruir.

## 2. Marco teórico

En los juegos, el movimiento se calcula así (todo en píxeles por cuadro):

```
posición += velocidad          (cada cuadro)
velocidad += aceleración        (cada cuadro)
```

La **gravedad** es una aceleración que empuja el proyectil hacia abajo. Como la pantalla crece hacia abajo en y, "bajar" es sumar en `y`:

```python
bala["vy"] += GRAVEDAD   # 0.25 cada cuadro
bala["y"] += bala["vy"]
bala["x"] += bala["vx"]
```

Ese movimiento curvo que resulta se llama **parábola** y es la misma física de una pelota, un cañón o un balón.

Para apuntar con el mouse necesitamos **trigonometría**: si el cañón está en el punto `origen` y el mouse en `(mx, my)`, el ángulo es:

```
angulo = atan2(origen_y - my, mx - origen_x)
```

Con el ángulo calculamos la velocidad inicial descompuesta en ejes:

```
vx = potencia * cos(angulo)
vy = -potencia * sin(angulo)   # el menos porque "arriba" es y negativo
```

## 3. Paso a paso

```powershell
cd mis-videojuegos
mkdir clase_03_canones
```

Escribí `clase_03_canones/canones.py`:

```python
import math
import sys
import pygame

pygame.init()

ANCHO, ALTO = 900, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
reloj = pygame.time.Clock()

GRAVEDAD = 0.25
POTENCIA = 22
origen = (90, ALTO - 30)          # posición del cañón
balas = []                        # cada bala es un dict: x, y, vx, vy
blancos = [{"x": x, "ancho": 60, "alto": 40} for x in range(350, 850, 90)]
puntos = 0

def disparar(angulo):
    rad = math.radians(angulo)
    vx = POTENCIA * math.cos(rad)
    vy = -POTENCIA * math.sin(rad)
    balas.append({"x": origen[0], "y": origen[1], "vx": vx, "vy": vy})

ejecutando = True
while ejecutando:
    angulo = 0
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        elif evento.type == pygame.MOUSEMOTION:
            mx, my = pygame.mouse.get_pos()
            angulo = math.degrees(math.atan2(origen[1] - my, mx - origen[0]))
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            disparar(angulo)

    # Física de cada bala
    for b in balas:
        b["x"] += b["vx"]
        b["y"] += b["vy"]
        b["vy"] += GRAVEDAD
        if b["y"] > ALTO - 10:        # rebote en el piso
            b["vy"] *= -0.7
            b["y"] = ALTO - 10

    # Dibujar
    pantalla.fill((25, 25, 45))
    pygame.draw.rect(pantalla, (80, 220, 120), (0, ALTO - 10, ANCHO, 10))
    for blanco in blancos:
        pygame.draw.rect(pantalla, (220, 80, 80),
                         (blanco["x"], ALTO - 90, blanco["ancho"], blanco["alto"]))

    rad = math.radians(angulo)
    pygame.draw.line(pantalla, (240, 200, 60), origen,
                     (origen[0] + 60 * math.cos(rad),
                      origen[1] - 60 * math.sin(rad)), 6)

    for b in balas:
        pygame.draw.circle(pantalla, (240, 240, 240),
                           (int(b["x"]), int(b["y"])), 8)

    pygame.display.set_caption(f"Cañones - Puntos: {puntos}")
    pygame.display.flip()
    reloj.tick(60)

pygame.quit()
sys.exit()
```

## 4. Actividad de cierre (para el commit)

1. **Detección de impacto:** cuando una bala toca un blanco, eliminá el blanco y sumá puntos. Completá este bloque dentro del bucle de física:

```python
for b in balas[:]:
    for blanco in blancos[:]:
        if (blanco["x"] <= b["x"] <= blanco["x"] + blanco["ancho"] and
                ALTO - 90 <= b["y"] <= ALTO - 90 + blanco["alto"]):
            blancos.remove(blanco)
            balas.remove(b)
            puntos += 10
            break
```

2. Cuando no queden blancos, mostrá `"Ganaste"` y terminá el juego.
3. Commit y push:

```powershell
git add .
git commit -m "Clase 03: cañones con física y destrucción de blancos"
git push
```

## 5. Usando IA en esta clase (prompts sugeridos)

> **Prompt 1:** "Explicame con un ejemplo numérico cómo avanza una bala de cañón cuadro a cuadro con gravedad."
>
> **Prompt 2:** "¿Por qué la velocidad inicial en y es `-potencia * sin(angulo)` y no positiva?"
>
> **Prompt 3:** "Agregá a mi juego de cañones un viento horizontal que empuja las balas. Mi código: [pegá el código]."
>
> **Prompt 4:** "Mi bala atraviesa los blancos sin destruirlos. Ayudame a revisar la condición de colisión. Mi código: [pegá el código]."

## 6. Desafíos para seguir practicando

- Que el cañón tenga **munición limitada** (por ejemplo 10 disparos).
- Que los blancos se **muevan** de un lado a otro.
- Que el puntaje dependa de la **cercanía al centro** del blanco.

## 7. Rúbrica de evaluación

| Criterio | Logrado | En proceso | No logrado |
|---|---|---|---|
| Parábola correcta | Curva realista | Se mueve raro | No dispara |
| Apuntar con mouse | Preciso | Aproximado | Fijo |
| Destruir blancos | Funciona | Solo algunos | No funciona |
| Git | Commit claro | Commit confuso | Sin commit |
