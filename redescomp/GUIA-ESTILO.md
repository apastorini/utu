# Guía de estilo y estructura de las clases

Esto es lo que TODA clase debe cumplir. Sin excepciones.

---

## 1. Idioma y tono

- **Español rioplatense, con voseo.** "Si tenés que...", "fijate que...", "acá va...".
  Es como habla la cátedra y como te va a sonar natural leerlo 48 veces.
- **Los términos técnicos en inglés, entre paréntesis la primera vez.**
  Ej: "conmutación por paquetes (*packet switching*)".
- **Nunca digas "en la realidad moderna" ni "actualmente".** Todo lo que sea
  actual va en la caja de **⚠️ Actualización a 2026**, con su RFC.
- **Tratá al lector como alguien inteligente que se informe.** Nada de "es obvio
  que". Si algo es intuitivo, decí *por qué* es intuitivo.

## 2. Estructura obligatoria del archivo

```markdown
# Clase NN — <Título>

**Bloque:** A/B/C/D/E/F · **Semana:** N · **Duración estimada:** 90–120 min
**Correlativa:** <clase anterior> · **Sigue con:** <clase siguiente>
**Material de referencia:** Tanenbaum cap. X (pág. ~Y del PDF de tu carpeta) · RFC NNNN

---

## 🎯 Al terminar esta clase vas a poder

1. ... (verbo observable: "explicar", "calcular", "dibujar", "implementar")
2. ...
3. ...

> **Prerequisito del examen:** <qué pregunta de examen cubre esta clase, con
> código del examen>  — o "— (clase de soporte)"

---

# PARTE 1 — TEORÍA

## 1.x <Subtema>

<Explicación. Con diagramas en ASCII dentro de bloques de código.>

<Por qué importa: conectalo con algo que se pregunta en el examen.>

### ⚠️ Actualización a 2026

**Sigue igual:** ...
**Cambió:** ...
- `RFC NNNN — Título (año)`. Qué hace y por qué te lo pueden preguntar.
**Consecuencia para el examen:** ...

---

# PARTE 2 — PRÁCTICA RESUELTA

## 2.x <Título del ejercicio>

**Enunciado.** ...
**Datos.** ...

**Resolución paso a paso.**

Paso 1 — <qué hago y por qué>
```
<cálculo>
```

<Interpretación del resultado: qué significa físicamente.>

### ⚠️ Errores típicos
- <el error que casi todos cometen y cómo evitarlo>

---

# PARTE 3 — PROBLEMAS DE EXAMEN DE FING

## 3.x <Título del problema>

> **Fuente:** Examen `<código>`, `<letra o solución>`, `<fecha>`.
> **Link:** https://www.fing.edu.uy/inco/cursos/redescomp/examenes/<código>.pdf
> **Texto del examen:** <enunciado literal, entre blockquote>

**Resolución.**

a) ...
   <razonamiento explícito, con las cuentas a la vista>

b) ...

---

# PARTE 4 — CIERRE

## 📌 Resumen en 10 líneas

## ✅ Autoevaluación

Respondé sin mirar. Las respuestas están en `<details>`.

1. ...
<details><summary>Respuesta</summary>

...

</details>

## 🔗 Referencias
- Examen `<código>` — `<qué>`
- Tanenbaum & Wetherall, *Redes de computadoras* 5ª ed., cap. X
- RFC NNNN — `<título>`
- Clase siguiente: `<NN — título>`
```

## 3. Reglas duras

### 3.1 Sobre los problemas de examen
- **Copiá el enunciado literal** de `material-oficial/examenes/txt/<código>.txt`.
  Si el PDF es un escaneo sin texto (los de 2004–2006 a veces), parafraseá y
  marcalo como paráfrasis.
- **Resolvé siempre, completo.** Si un apartado del examen original no tiene
  solución publicada, **desarrollala vos** y marcala como *(solución propia)*.
- **Mostrá la aritmética.** En un problema de retardo, escribí `L/R` con los
  números adentro. En subnetting, escribí la cuenta de hosts + red + broadcast.
  Si alguien puede re-correr tus cuentas y obtener lo mismo, está bien.
- **Justificá cada suposición.** El examen dice "haga las suposiciones que
  considere necesarias, justificándolas" — hacé eso, en mayúsculas, y decí por qué.
- Si tu solución difiere de la solución oficial, **decilo explícitamente**:
  "Nota: la solución oficial dice X. Mi lectura es Y porque Z."

### 3.2 Sobre las actualizaciones
- **Nunca inventes un número de RFC.** Si no estás seguro, no lo pongas o poné
  "ver RFC 9xxx (buscar)". Preferí verificar.
- Solo poné RFCs que existen de verdad. Formato: `RFC 9293 — TCP (2022)`.
- Distinguí siempre entre **"esto se sigue preguntando"** y **"esto se
  preguntaba en 2011 y ya no"**. En los exámenes viejos hay temas que la cátedra
  hoy no daría (por ejemplo, IP Móvil IPv4 con RARP). Marcá esos con
  ⚠️ **tema en desuso**.

### 3.3 Sobre los diagramas
- **ASCII en bloques de código**, no mermaid ni imágenes. Tiene que verse bien
  en un `.md` plano y en el editor del usuario.
- Para topologías de red, un estilo consistente:

```
   Red A (192.168.1.0/24)          Red B (10.0.0.0/24)
   ┌───────────────────┐           ┌───────────────────┐
   │  H1      R1       │           │  R2       H2      │
   │ .25  ─── .1       │═══════════│ .1  ─── .25        │
   │ MAC_A  MAC_R1     │  enlace   │ MAC_R2  MAC_B      │
   └───────────────────┘           └───────────────────┘
```

- Para diagramas de secuencia (handshakes, ARP, DNS):

```
   Cliente                         Servidor
      │                               │
      │─────── SYN seq=0 ────────────▶│
      │◀────── SYN+ACK seq=0 ack=1 ───│
      │─────── ACK seq=1 ack=1 ──────▶│
```

### 3.4 Sobre el pseudocode
El examen pide "implementar" en un lenguaje de alto nivel. La cátedra acepta
pseudocode estilo C, y en los problemas de sockets espera **C real** con
`socket()`, `bind()`, `sendto()`, `recvfrom()`, `setsockopt()`.
- Si el problema da primitivas, **respetá los nombres y firmas exactos**.
- Si el problema es de sockets, **escribí C que compila** (aunque sea
  pseudocompilable), no pseudocode flojo.

### 3.5 Extensión
- **Mínimo 12.000 caracteres, máximo 35.000.** Las clases densas (subnetting,
  TCP, control de congestión) llegan a 30k. Las de repaso, 15k.
- Si te pasás de 35k, estás metiendo otra clase: cortá.

---

## 4. Sobre el razonamiento (lo que el usuario pidió explícitamente)

> "todo resuelto y explicando el razonamiento de cómo resolverlo"

En cada problema practical, el lector tiene que poder ver **por qué se hace cada
paso**, no solo el resultado. Formato para cada paso:

```
**Paso 3 — Calcular el retardo de transmisión del enlace 2.**

*d_pensamiento:* el paquete entra completo al switch, así que tiene que esperar
a que termine de entrar por el enlace 1 antes de salir por el 2. El retardo de
transmisión se calcula sobre el enlace de SALIDA.

*Ecuación:*
d_trans = L / R₂ = 1000 bits / 100 Mbps = 10 µs

*Interpretación:* 10 microsegundos. Es diminuto comparado con la propagación,
que va a ser de milisegundos.
```

Escribí el razonamiento **en prosa o en cursiva con asteriscos**, nunca como
comentario de código. Y siempre cerrá con la interpretación: *qué significa
físicamente este número*, porque en un examen eso es lo que suma puntos.

---

## 5. Los 3 simulacros

Las clases 7, 15, 23 y 37 llevan un **Simulacro** completo al final:
- Enunciado de las 5 preguntas teóricas + 2 problemas, sin respuestas.
- Debajo, en `<details>`, la resolución completa.
- Con **cronómetro sugerido** y reparto de tiempo.
- Con un **puntaje** y el aviso de "mínimo 15 de 40 en teoría".
