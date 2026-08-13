# Actividad 12 — Trivia: juego de preguntas y puntajes

**Duración:** 50 min · **Modalidad:** individual · **Entrega:** repo GitHub público

## 1. Objetivos

- Modelar preguntas con **listas y diccionarios**.
- Implementar una interfaz de opciones clicables.
- Sumar puntaje y manejar **tiempo límite** por pregunta.
- Mostrar el resultado final con mensajes.

## 2. Marco teórico

Un juego de **trivia** (preguntas y respuestas) es ideal para practicar **estructuras de datos**:

```python
preguntas = [
    {
        "pregunta": "¿Cuál es el océano más grande?",
        "opciones": ["Atlántico", "Índico", "Pacífico", "Ártico"],
        "correcta": 2,   # índice de la opción correcta
    },
    ...
]
```

Cada pregunta es un **diccionario** y el banco de preguntas es una **lista de diccionarios**. El juego recorre la lista, dibuja la pregunta y las opciones, espera un clic y compara el índice elegido con `"correcta"`.

Para el **temporizador** usamos el reloj de Pygame: `pygame.time.get_ticks()` devuelve los milisegundos desde que arrancó el juego. Guardamos el tiempo de inicio de cada pregunta y restamos con el actual.

## 3. Paso a paso

```powershell
cd mis-videojuegos
mkdir clase_12_trivia
```

Escribí `clase_12_trivia/trivia.py`:

```python
import sys
import pygame

pygame.init()

ANCHO, ALTO = 900, 650
pantalla = pygame.display.set_mode((ANCHO, ALTO))
reloj = pygame.time.Clock()
fuente = pygame.font.SysFont("arial", 26)
fuente_grande = pygame.font.SysFont("arial", 40)

preguntas = [
    {"pregunta": "¿Cuál es el océano más grande?",
     "opciones": ["Atlántico", "Índico", "Pacífico", "Ártico"],
     "correcta": 2},
    {"pregunta": "¿Quién pintó la Mona Lisa?",
     "opciones": ["Van Gogh", "Da Vinci", "Picasso", "Rembrandt"],
     "correcta": 1},
    {"pregunta": "¿Cuántos lados tiene un hexágono?",
     "opciones": ["5", "6", "7", "8"],
     "correcta": 1},
    {"pregunta": "¿En qué año llegó el hombre a la Luna?",
     "opciones": ["1965", "1969", "1972", "1959"],
     "correcta": 1},
    {"pregunta": "¿Qué lenguaje se usa para escribir este juego?",
     "opciones": ["Java", "C++", "Python", "Ruby"],
     "correcta": 2},
]

# Mezclá las preguntas para que el orden cambie cada vez
import random
random.shuffle(preguntas)

indice = 0
puntaje = 0
tiempo_inicio = pygame.time.get_ticks()
TIEMPO_POR_PREGUNTA = 15000   # 15 segundos
terminado = False
mensaje_final = ""

def dibujar_pregunta(p):
    pantalla.blit(fuente_grande.render(p["pregunta"], True, (255, 255, 255)), (60, 80))
    y = 180
    for i, opcion in enumerate(p["opciones"]):
        rect = pygame.Rect(ANCHO // 2 - 300, y, 600, 45)
        pygame.draw.rect(pantalla, (50, 70, 120), rect)
        pantalla.blit(fuente.render(f"{i + 1}. {opcion}", True, (255, 255, 255)),
                      (rect.x + 15, rect.y + 8))
        y += 60
    return [pygame.Rect(ANCHO // 2 - 300, 180 + i * 60, 600, 45)
            for i in range(len(p["opciones"]))]

ejecutando = True
while ejecutando:
    rects = []
    if not terminado and indice < len(preguntas):
        rects = dibujar_pregunta(preguntas[indice])
        # Barra de tiempo
        restante = TIEMPO_POR_PREGUNTA - (pygame.time.get_ticks() - tiempo_inicio)
        if restante <= 0:
            indice += 1
            tiempo_inicio = pygame.time.get_ticks()
            if indice >= len(preguntas):
                terminado = True
        pygame.draw.rect(pantalla, (120, 200, 80), (60, 600, restante / TIEMPO_POR_PREGUNTA * 780, 15))

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        elif evento.type == pygame.MOUSEBUTTONDOWN and not terminado and rects:
            mx, my = pygame.mouse.get_pos()
            for i, rect in enumerate(rects):
                if rect.collidepoint(mx, my):
                    if i == preguntas[indice]["correcta"]:
                        puntaje += 10
                    indice += 1
                    tiempo_inicio = pygame.time.get_ticks()
                    if indice >= len(preguntas):
                        terminado = True
                    break

    pantalla.fill((20, 20, 40))
    if terminado:
        texto = f"Fin del juego. Puntaje: {puntaje}/{len(preguntas) * 10}"
        pantalla.blit(fuente_grande.render(texto, True, (255, 200, 60)), (60, 250))
        pantalla.blit(fuente.render("Apretá cualquier tecla para salir", True, (255, 255, 255)), (60, 320))
    else:
        pantalla.blit(fuente.render(f"Pregunta {indice + 1}/{len(preguntas)} - Puntaje: {puntaje}",
                                    True, (200, 200, 220)), (60, 30))
        for rect in rects:
            pass  # ya dibujados en dibujar_pregunta
    pygame.display.flip()
    reloj.tick(30)

pygame.quit()
sys.exit()
```

## 4. Actividad de cierre (para el commit)

1. Completá el banco con **10 preguntas** de un tema que te guste (fútbol, historia, ciencia, videojuegos).
2. Sumá **bonificación por velocidad**: si respondés en menos de 5 segundos, ganás 15 puntos.
3. **Niveles de dificultad:** preguntas fáciles (10 pts) y difíciles (20 pts), y mostrá el mensaje "¡Muy bien!" o "¡Te equivocaste!" entre pregunta y pregunta.
4. Commit y push:

```powershell
git add .
git commit -m "Clase 12: trivia con 10 preguntas, tiempo y puntaje"
git push
```

## 5. Usando IA en esta clase (prompts sugeridos)

> **Prompt 1:** "Generame 10 preguntas de historia de los videojuegos en este formato de diccionario Python: [pegá la estructura]."
>
> **Prompt 2:** "¿Cómo agrego un tiempo límite por pregunta en Pygame usando pygame.time.get_ticks()? Mi código: [pegá el código]."
>
> **Prompt 3:** "Hacé que la trivia cargue las preguntas desde un archivo JSON. Mostrame la estructura del JSON y el código para cargarlo."
>
> **Prompt 4:** "Agregá sonidos de acierto y error con pygame.mixer."

## 6. Desafíos para seguir practicando

- Cargar preguntas desde un **archivo** (JSON) para no reescribir código.
- Modo **contra reloj** general (90 segundos para todo).
- Ranking de mejores puntajes guardado en un archivo.
- Conectarla a una API de preguntas (por ejemplo la API pública de trivia).

## 7. Rúbrica de evaluación

| Criterio | Logrado | En proceso | No logrado |
|---|---|---|---|
| Banco de preguntas | 10 o más | 5-9 | Menos |
| Clic en opciones | Correcto | Parcial | No |
| Tiempo por pregunta | Funciona | A veces | No |
| Puntaje final | Correcto | Error de cálculo | No |
