# Actividad 15 — Crear juegos con IA: ingeniería de prompts

**Duración:** 50 min · **Modalidad:** individual · **Entrega:** repo GitHub público

## 1. Objetivos

- Aprender a escribir **buenos prompts** (órdenes) para una IA de programación.
- Usar la IA para **generar**, **mejorar** y **depurar** un juego.
- Aplicar un **método de trabajo**: especificar → generar → probar → iterar.
- Crear un mini-juego nuevo elegido entre varias opciones, usando IA como asistente.

## 2. Marco teórico

Una IA generativa (como ChatGPT, Gemini, Claude o Copilot) no "piensa": **predice texto** según lo que recibe. Por eso la **calidad de la respuesta depende de la calidad de la pregunta (el prompt)**.

Un buen prompt de programación tiene 4 ingredientes:

1. **Rol:** "Actuá como un programador experto en Pygame."
2. **Contexto:** "Estoy aprendiendo, tengo 16 años, uso Python 3 y Pygame 2."
3. **Tarea concreta:** "Creá un juego donde... (describí las reglas exactas)."
4. **Formato de salida:** "Mostrame el código completo en un solo archivo, con comentarios en español."

Luego viene la **iteración**: la primera respuesta casi nunca es perfecta. El ciclo es:

```
Especificar -> Pedir código -> Probar -> Detectar error
      ^                                       |
      +------------ Arreglar con IA <---------+
```

Errores comunes al trabajar con IA:

- Pedir todo de golpe (es mejor por partes).
- No probar el código antes de pedir arreglos.
- Copiar código sin entenderlo.
- No dar contexto (la IA no sabe qué versión, qué librerías, qué errores ves).

> Regla de oro del curso: la IA es el **copiloto**, vos sos el piloto. Si no entendés una línea, no la copies: pedile que te la explique primero.

## 3. Paso a paso

### 3.1 Elegí tu mini-juego

Elegí una de estas opciones (o proponé una propia):

- **Pong:** dos paletas y una pelota (vs una IA simple).
- **Flappy Bird** (sin sprites): un rectángulo que "vuela" esquivando obstáculos.
- **Carrera de autos:** esquivá obstáculos que caen hacia abajo.
- **Gato / Ta-Te-Ti** (Tic-tac-toe) contra la máquina.
- **Simón dice:** memorizar secuencias de colores.

### 3.2 Escribí la especificación

Antes de pedir código, escribí en un archivo `clase_15_ia/especificacion.txt` la idea en tus palabras:

```
Juego: [nombre]
Cómo se juega: ...
Controles: ...
Cómo se gana: ...
Cómo se pierde: ...
Puntaje: ...
Extra (si da tiempo): ...
```

### 3.3 Pedile el código a la IA

Armá un prompt con los 4 ingredientes. Ejemplo para Flappy Bird:

> "Actuá como un programador experto en Pygame. Soy estudiante, uso Python 3.13 y Pygame 2. Creá un mini-juego tipo Flappy Bird sin imágenes: un rectángulo amarillo que salta con ESPACIO y esquiva tubos verdes que vienen de la derecha. Gravedad constante, la pelota no puede salir por arriba ni por abajo (muere), puntaje cada vez que pasa un tubo. Mostrame el código completo en un solo archivo `flappy.py`, con comentarios en español y sin código extra. Explicame las 5 líneas más importantes."

### 3.4 Probalo, depurá, iterá

1. Guardá el código en `clase_15_ia/` y ejecutalo.
2. Si falla, pegale el **error completo** a la IA:

> "Me da este error: [pegá el mensaje completo del traceback]. El código es: [pegá el código]. ¿Qué está mal y cómo lo arreglo?"

3. Si funciona pero "se siente mal" (muy lento, muy difícil), pedí ajustes:

> "Hacé que los tubos estén más separados y que la pelota sea más liviana (menos gravedad)."

4. Repetí hasta que el juego se sienta bien. **Probalo en voz alta mientras jugás**: ¿es divertido? ¿justo?

### 3.5 Documentá

Creá un `README.md` dentro de `clase_15_ia/`:

```markdown
# Mi juego: [nombre]

Hecho con IA asistida en la actividad 15.

## Controles
- ESPACIO: saltar

## Cómo se juega
...

## Qué aprendí
- [algo que entendiste mejor gracias a la IA]
- [algo que la IA hizo mal y tuviste que corregir]
```

## 4. Actividad de cierre (para el commit)

1. Que el juego tenga **al menos un detalle que vos diseñaste** (un color, una regla, un power-up) y no venga del prompt.
2. Commit y push:

```powershell
git add .
git commit -m "Clase 15: mini-juego creado con IA asistida"
git push
```

3. Preparate para contar en la próxima clase: qué pediste, qué falló y qué arreglaste.

## 5. Método de prompts (resumen para copiar)

```
Rol: "Actuá como un programador experto en <librería>."
Contexto: "Soy estudiante, uso <versión>. Es mi primera vez."
Tarea: "<qué juego, reglas, controles, puntaje>."
Formato: "Código completo en un solo archivo, comentarios en español,
          sin código extra, y explicame las líneas clave."
```

Para depurar: **siempre pegá el mensaje de error completo**. La IA no adivina qué pasa.

## 6. Usando IA en esta clase (prompts sugeridos)

> **Prompt de revisión:** "Revisá este código como si fuera un profesor: decime 3 cosas que están bien y 3 que mejoraría. No me des el código arreglado todavía."
>
> **Prompt de explicación:** "Explicame qué hace `pygame.key.get_pressed()` y por qué se usa dentro del while y no dentro del for de eventos."
>
> **Prompt de comparación:** "¿Cuál es la diferencia entre mi código y una versión más limpia? Mi código: [pegá el código]."
>
> **Prompt de ideas:** "Dame 3 power-ups originales para mi juego [nombre] y explicá cómo implementarías cada uno."

## 7. Rúbrica de evaluación

| Criterio | Logrado | En proceso | No logrado |
|---|---|---|---|
| Especificación previa | Escribió el archivo | A medias | No |
| Juego funciona | Corre sin errores | Con errores | No corre |
| Iteración con IA | Probó y arregló 2+ veces | 1 vez | Copió y pegó |
| Entendimiento | Explica las líneas clave | Parcial | No explica |
| Detalle propio | Agregó algo original | Copió todo | Copió todo |
