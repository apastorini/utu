# Actividad 4 — Arkanoid

**Duración:** 50 min · **Modalidad:** individual · **Entrega:** repo GitHub público

## 1. Objetivos

- Usar los **rectángulos** de Pygame (`pygame.Rect`) para colisiones.
- Implementar la paleta (paddle), la pelota y sus rebotes.
- Manejar una **lista de ladrillos** que se destruyen.
- Controlar vidas y condición de victoria/derrota.

## 2. Marco teórico

**Arkanoid** (1986) es el clásico *Breakout*: una pelota rebota contra una paleta y destruye ladrillos. Cada vez que la pelota toca un ladrillo, este desaparece y ganás puntos. Si la pelota cae al fondo, perdés una vida.

En Pygame, un **`Rect`** guarda posición y tamaño y tiene métodos muy útiles:

- `pelota.colliderect(pala)` → ¿chocan dos rectángulos?
- `pelota.left`, `pelota.right`, `pelota.top`, `pelota.bottom` → bordes.
- `rect.x`, `rect.y`, `rect.center`, `rect.width` → posición y medidas.

La lógica del rebote:

- Si la pelota toca **pared izquierda o derecha**: invierto la velocidad en x (`vel_x *= -1`).
- Si toca el **techo** o la **paleta**: invierto la velocidad en y.
- Si toca un **ladrillo**: lo elimino e invierto y.

## 3. Paso a paso

```powershell
cd mis-videojuegos
mkdir clase_04_arkanoid
```

Escribí `clase_04_arkanoid/arkanoid.py`:

```python
import sys
import pygame

pygame.init()

ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
reloj = pygame.time.Clock()

pala = pygame.Rect(ANCHO // 2 - 60, ALTO - 40, 120, 15)
pelota = pygame.Rect(ANCHO // 2 - 8, ALTO // 2, 16, 16)
vel_x, vel_y = 5, -5

# Ladrillos: una fila de rectángulos
FILAS, COLS = 4, 10
ladrillos = []
for fila in range(FILAS):
    for col in range(COLS):
        ladrillos.append(pygame.Rect(col * 80 + 5, fila * 30 + 40, 70, 20))

vidas = 3
ejecutando = True

while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

    # Paleta sigue al mouse
    pala.x = pygame.mouse.get_pos()[0] - pala.width // 2
    pala.x = max(0, min(ANCHO - pala.width, pala.x))

    # Mover la pelota
    pelota.x += vel_x
    pelota.y += vel_y

    # Rebotes con paredes
    if pelota.left <= 0 or pelota.right >= ANCHO:
        vel_x *= -1
    if pelota.top <= 0:
        vel_y *= -1
    if pelota.colliderect(pala) and vel_y > 0:
        vel_y *= -1

    # COMPLETÁ: destruir ladrillos
    # for ladrillo in ladrillos[:]:
    #     if pelota.colliderect(ladrillo):
    #         ladrillos.remove(ladrillo)
    #         vel_y *= -1
    #         break

    # Perder vida
    if pelota.bottom >= ALTO:
        vidas -= 1
        pelota.center = (ANCHO // 2, ALTO // 2)
        if vidas == 0:
            ejecutando = False

    # Dibujar
    pantalla.fill((15, 15, 30))
    pygame.draw.rect(pantalla, (90, 180, 255), pala)
    pygame.draw.rect(pantalla, (255, 255, 255), pelota)
    for ladrillo in ladrillos:
        pygame.draw.rect(pantalla, (255, 120, 120), ladrillo)

    pygame.display.set_caption(f"Arkanoid - Vidas: {vidas} - Ladrillos: {len(ladrillos)}")
    pygame.display.flip()
    reloj.tick(60)

pygame.quit()
sys.exit()
```

## 4. Probalo

```powershell
python clase_04_arkanoid/arkanoid.py
```

> La parte de destruir ladrillos está como comentario (COMPLETÁ). Descomentala y probá. Si la pelota queda "pegada" a la paleta, compará tu lógica con la explicación de la sección 6.

## 5. Actividad de cierre (para el commit)

1. **Victoria:** si `len(ladrillos) == 0`, mostrá `"¡Ganaste!"` y terminá el juego.
2. **Puntaje:** sumá 10 puntos por ladrillo y mostralo en el título de la ventana.
3. **Aceleración:** cada vez que se destruyen 5 ladrillos, aumentá `vel_x` y `vel_y`.
4. Commit y push:

```powershell
git add .
git commit -m "Clase 04: arkanoid con ladrillos, vidas y puntaje"
git push
```

## 6. Usando IA en esta clase (prompts sugeridos)

> **Prompt 1:** "¿Qué hace exactamente `for ladrillo in ladrillos[:]` y por qué uso una copia de la lista? Explicámelo."
>
> **Prompt 2:** "La pelota de mi Arkanoid atraviesa los ladrillos. Mi código: [pegá el código]. ¿Cuál puede ser el problema?"
>
> **Prompt 3:** "Agregá que la pelota rebote distinto según dónde toque la paleta (izquierda, centro, derecha)."
>
> **Prompt 4:** "Hacé que cada fila de ladrillos tenga un color distinto y valga distinto puntaje."

## 7. Rúbrica de evaluación

| Criterio | Logrado | En proceso | No logrado |
|---|---|---|---|
| Rebotes paredes/techo | Correctos | Parciales | No rebota |
| Destruir ladrillos | Funciona | A veces | No |
| Paleta con mouse | Fluida | Con saltos | No sigue |
| Vidas y fin de juego | Correctos | Solo uno | Falta |
