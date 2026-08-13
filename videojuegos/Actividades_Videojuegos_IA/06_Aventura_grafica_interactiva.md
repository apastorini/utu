# Actividad 6 — Aventura gráfica interactiva

**Duración:** 50 min · **Modalidad:** individual · **Entrega:** repo GitHub público

## 1. Objetivos

- Entender cómo se construye una **historia interactiva** (narrativa ramificada).
- Modelar escenas como un **diccionario de nodos**.
- Implementar **menús de opciones** clicables.
- Diseñar una aventura con al menos 5 escenas.

## 2. Marco teórico

Una **aventura gráfica** es un juego donde lo importante es la historia y las decisiones del jugador. Juegos famosos: *Monkey Island*, *Indiana Jones*, *Day of the Tentacle*.

La estructura clásica es un **grafo de escenas** (nodos conectados):

```
          /-> cueva -> tesoro (FIN)
inicio --|
          \-> río -> aldea (FIN)
```

En Python, cada escena es un diccionario con el texto y sus opciones. Cada opción apunta a otra escena:

```python
historia = {
    "inicio": {
        "texto": "Estás en la selva. Escuchás ruido entre los árboles.",
        "opciones": [("Ir a investigar", "cueva"), ("Seguir el sendero", "rio")],
    },
    "cueva": { "texto": "...", "opciones": [...] },
}
```

El juego es un bucle que: dibuja el texto, dibuja botones, espera un clic y cambia de escena. Cuando una escena no tiene opciones, terminó la aventura.

## 3. Paso a paso

```powershell
cd mis-videojuegos
mkdir clase_06_aventura_grafica
```

Escribí `clase_06_aventura_grafica/aventura.py`:

```python
import sys
import pygame

pygame.init()

ANCHO, ALTO = 900, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
reloj = pygame.time.Clock()
fuente = pygame.font.SysFont("arial", 26)

# ====== HISTORIA: completá los textos que faltan ======
historia = {
    "inicio": {
        "texto": "Estás en la selva. Escuchás un ruido entre los árboles.",
        "opciones": [("Ir a investigar", "cueva"), ("Seguir el sendero", "rio")],
    },
    "cueva": {
        "texto": "Dentro de la cueva hay un cofre dorado. Un mono lo custodia.",
        "opciones": [("Hablar con el mono", "mono"), ("Abrir el cofre a escondidas", "cofre")],
    },
    "mono": {
        "texto": "El mono habla: '¡Dame una banana y el tesoro será tuyo!'",
        "opciones": [("Dar la banana", "tesoro"), ("Negarme", "inicio")],
    },
    "tesoro": {
        "texto": "¡Ganaste el tesoro legendario de la selva! Fin de la aventura.",
        "opciones": [],
    },
    # COMPLETÁ: agregá las escenas "rio" y "cofre"
}
# ======================================================

escena = "inicio"

def dibujar_botones(opciones):
    botones = []
    y = ALTO - 40 * len(opciones) - 20
    for texto, _ in opciones:
        rect = pygame.Rect(ANCHO // 2 - 200, y, 400, 34)
        pygame.draw.rect(pantalla, (60, 60, 130), rect)
        pantalla.blit(fuente.render(texto, True, (255, 255, 255)), (rect.x + 12, rect.y + 6))
        botones.append((rect, texto))
        y += 44
    return botones

def dibujar_texto(texto, limite=45):
    palabras = texto.split()
    lineas, actual = [], ""
    for p in palabras:
        if len(actual) + len(p) + 1 > limite:
            lineas.append(actual)
            actual = p
        else:
            actual = actual + " " + p
    lineas.append(actual)
    y = 150
    for linea in lineas:
        pantalla.blit(fuente.render(linea, True, (255, 255, 255)), (80, y))
        y += 34

ejecutando = True
while ejecutando:
    opciones = historia[escena]["opciones"]
    botones = dibujar_botones(opciones)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        elif evento.type == pygame.MOUSEBUTTONDOWN and opciones:
            mx, my = pygame.mouse.get_pos()
            for i, (rect, _) in enumerate(botones):
                if rect.collidepoint(mx, my):
                    escena = opciones[i][1]   # ir a la escena elegida
                    if not historia[escena]["opciones"]:
                        print("La aventura terminó.")
                    break

    pantalla.fill((20, 30, 20))
    pantalla.blit(fuente.render("AVENTURA EN LA SELVA", True, (255, 200, 60)), (80, 60))
    dibujar_texto(historia[escena]["texto"])
    dibujar_botones(opciones)
    pygame.display.flip()
    reloj.tick(30)

pygame.quit()
sys.exit()
```

## 4. Actividad de cierre (para el commit)

1. Completá las escenas que faltan (`rio` y `cofre`) para que la aventura tenga **al menos 6 escenas**.
2. Agregá un **inventario** simple: una variable global, por ejemplo `tiene_banana = True`, y que algunas opciones solo aparezcan si tenés el objeto (pista: la condición puede filtrar las opciones antes de dibujarlas).
3. Cambiá el fondo de pantalla según la escena (bosque, cueva, río) usando colores distintos.
4. Commit y push:

```powershell
git add .
git commit -m "Clase 06: aventura gráfica con 6 escenas e inventario"
git push
```

## 5. Usando IA en esta clase (prompts sugeridos)

> **Prompt 1:** "Generame una aventura gráfica de 8 escenas ambientada en un barco pirata, en este formato de diccionario Python: [pegá la estructura de `historia`]."
>
> **Prompt 2:** "¿Cómo agrego un inventario con objetos que se ganan y se usan en este juego? Mi código: [pegá el código]."
>
> **Prompt 3:** "¿Qué es un 'punto caliente' (hotspot) en las aventuras gráficas clásicas y cómo lo podría simular con rectángulos clicables?"
>
> **Prompt 4:** "Revisá mi historia y decime qué escenas están desconectadas (no hay forma de llegar a ellas)."

## 6. Desafíos para seguir practicando

- Agregar **imágenes** por escena con `pygame.image.load`.
- Convertir la aventura en un juego **web** con HTML (se ve en la actividad 7).
- Agregar **efectos de sonido** al elegir opciones.
- Que el jugador tenga **vidas** que pierde con decisiones malas.

## 7. Rúbrica de evaluación

| Criterio | Logrado | En proceso | No logrado |
|---|---|---|---|
| Estructura de escenas | 6+ conectadas | 3-5 | 1-2 |
| Navegación con clic | Fluida | Con fallas | No funciona |
| Inventario | Implementado | Parcial | No |
| Historia y creatividad | Buena y coherente | Aceptable | Básica |
