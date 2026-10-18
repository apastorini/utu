# Encuentro 7 — Ejercicios de evaluaciones anteriores (Práctico 1)

> **Práctico 1, "Ejercicios propuestos en evaluaciones anteriores" (1 a 5).**
> Son de **parciales y exámenes reales**, en formato **múltiple opción**. Acá lo importante no es solo llegar a la respuesta, sino **cómo** se resuelve cada uno.
> Usamos todo lo de los encuentros 1 a 6.

---

## Ejercicio 1 — (Primer parcial, segundo semestre 2023)

> Sea y(x) la solución de  y''(x) − y'(x) − 2y(x) = −2x² + 3  con  y(0) = 0, y'(0) = 2. Entonces y(1) vale:
> (A) e² − e⁻¹   (B) e² + e⁻¹   (C) e⁻¹ − e² + 1   (D) (e² − e⁻¹)/(e² + e⁻¹)   (E) e² − 1

**Paso 1 — homogénea.** Característica r² − r − 2 = 0. Busco dos números que multiplicados den −2 y sumados den −1: son −2 y 1 → (r − 2)(r + 1) = 0 → r = 2, −1.

    y_h = A·e^(2x) + B·e^(−x).

**Paso 2 — particular.** f(x) = −2x² + 3 es polinomio de grado 2 → pruebo y_p = a·x² + b·x + c.

    y_p' = 2a·x + b,  y_p'' = 2a.
    y_p'' − y_p' − 2y_p = 2a − (2a x + b) − 2(a x² + b x + c)
                        = −2a·x² + (−2a − 2b)·x + (2a − b − 2c).

Igualo con −2x² + 0·x + 3:

    −2a = −2          →  a = 1
    −2a − 2b = 0      →  −2 − 2b = 0  →  b = −1
    2a − b − 2c = 3   →  2 + 1 − 2c = 3  →  3 − 2c = 3  →  c = 0

    y_p = x² − x.

**Paso 3 — general y condiciones iniciales.**

    y = A·e^(2x) + B·e^(−x) + x² − x.
    y(0) = A + B = 0.
    y' = 2A·e^(2x) − B·e^(−x) + 2x − 1  →  y'(0) = 2A − B − 1 = 2  →  2A − B = 3.

De A + B = 0 tengo B = −A. Entonces 2A − (−A) = 3A = 3 → A = 1, B = −1.

**Paso 4 — y(1).**

    y(1) = e² − e⁻¹ + 1² − 1 = e² − e⁻¹ + 0 = e² − e⁻¹.

**Respuesta: (A).**

---

## Ejercicio 2 — (Examen febrero 2023)

> Ecuación (E):  y'' + 4y' + 4y = r(x). Afirmaciones:
> (I) Si e^(−2x) + x² es solución de (E) entonces r(x) = 4x² + 8x + 2.
> (II) Si r(x) = x² entonces y(x) = e^(−2x) + 3x·e^(−2x) + x² es la única solución de (E) con y(0) = y'(0) = 1.
> (III) Si r(x) = 0 entonces todas las soluciones son y(x) = a·e^(−2x) + b·x·e^(−2x).
> (A) todas verdaderas  (B) solo (III)  (C) solo (I)  (D) solo (I) y (III)

**Dato común:** la homogénea y'' + 4y' + 4y = 0 tiene característica (r + 2)² = 0 → r = −2 doble.

**Analizo (I).** Tomo y = e^(−2x) + x² y calculo y'' + 4y' + 4y.

- Para e^(−2x): es solución de la homogénea, así que su aporte es **0**.
- Para x²: y = x² → y' = 2x → y'' = 2. Entonces y'' + 4y' + 4y = 2 + 4(2x) + 4(x²) = 4x² + 8x + 2.

Como y'' + 4y' + 4y = r(x), queda r(x) = 4x² + 8x + 2. **(I) es verdadera.**

**Analizo (II).** Si r(x) = x², busco una particular. Pruebo y_p = a x² + b x + c:

    y_p' = 2a x + b, y_p'' = 2a.
    y_p'' + 4y_p' + 4y_p = 2a + 4(2a x + b) + 4(a x² + b x + c)
                         = 4a·x² + (8a + 4b)·x + (2a + 4b + 4c).

Igualo con x²:

    4a = 1            →  a = 1/4
    8a + 4b = 0       →  2 + 4b = 0  →  b = −1/2
    2a + 4b + 4c = 0  →  1/2 − 2 + 4c = 0  →  4c = 3/2  →  c = 3/8

Así que la solución general sería:

    y = (a₀ + b₀·x)·e^(−2x) + 1/4·x² − 1/2·x + 3/8.

La función propuesta en (II) tiene parte polinómica **x²** (no 1/4·x² − 1/2·x + 3/8). Mirá: la parte x² de la propuesta, al meterla en el operador, da 4x² + 8x + 2 ≠ x². Por lo tanto **la función propuesta no es solución** de la ecuación. **(II) es falsa.**

**Analizo (III).** Si r(x) = 0, la ecuación es homogénea con raíz doble −2. La solución general es

    y = (a + b·x)·e^(−2x) = a·e^(−2x) + b·x·e^(−2x).

**(III) es verdadera.**

**Respuesta: (D) solo (I) y (III).**

---

## Ejercicio 3 — (Primer parcial, segundo semestre 2022)

> Sea y(x) la solución de  [ y'(x)·e^(x²) ] / x = −2·( 1 + y²(x) )  con  y(0) = 0. Entonces y(√2) vale:
> (A) −e   (B) tan(1 + e²)   (C) tan(1)   (D) 1   (E) tan(e⁻² − 1)

**Paso 1 — acomodo la ecuación.** Multiplico los dos lados por x·e^(−x²) para despejar y':

    y' = −2·(1 + y²)·x·e^(−x²).

**Paso 2 — separo.** Paso (1 + y²) dividiendo y dx multiplicando:

    dy / (1 + y²) = −2x·e^(−x²) dx.

**Paso 3 — integro los dos lados.**

- **Izquierda:** ∫ dy/(1 + y²) = arctan y (tabla: (arctan y)' = 1/(1+y²)).
- **Derecha:** ∫ −2x·e^(−x²) dx. Uso **cambio de variable** t = −x², entonces dt = −2x dx. Queda ∫ e^t dt = e^t = e^(−x²).

Entonces:

    arctan y = e^(−x²) + C.

**Paso 4 — condición inicial y(0) = 0.** arctan 0 = 0, y e^(0) = 1:

    0 = 1 + C  →  C = −1.

Así:

    arctan y = e^(−x²) − 1  →  y = tan( e^(−x²) − 1 ).

**Paso 5 — evalúo en x = √2.** (√2)² = 2:

    y(√2) = tan( e^(−2) − 1 ).

**Respuesta: (E) tan(e⁻² − 1).**

---

## Ejercicio 4 — (Examen julio 2021)

> Ecuación  y'' + α·y' + β·y = 2·e^(3x), con α, β ∈ R. Sabemos que y(x) = x²·e^(3x) es solución. Entonces α + β vale:
> (A) 3   (B) 0   (C) 1   (D) 2   (E) 4

**Paso 1 — la pista clave: resonancia.** El lado derecho es e^(3x). En la prueba educada, para e^(3x) uno intenta C·e^(3x); pero nos dan x²·e^(3x), que es **una potencia más alta** de x. Eso pasa cuando el exponente 3 es **raíz doble** de la característica (hay que multiplicar por x²). Es decir:

    r² + α·r + β = (r − 3)² = r² − 6r + 9.

Comparando: **α = −6, β = 9**.

**Paso 2 — verifico.** Con α = −6, β = 9, la ecuación es y'' − 6y' + 9y = 2e^(3x). Chequeo con y = x²e^(3x):

- y' = 2x·e^(3x) + x²·3e^(3x) = e^(3x)·(2x + 3x²).
- y'' = (2 + 6x)·e^(3x) + (2x + 3x²)·3e^(3x) = e^(3x)·( 2 + 6x + 6x + 9x² ) = e^(3x)·(9x² + 12x + 2).

Ahora y'' − 6y' + 9y = e^(3x)·[ (9x² + 12x + 2) − 6(2x + 3x²) + 9x² ] = e^(3x)·[ 9x² + 12x + 2 − 12x − 18x² + 9x² ] = e^(3x)·2 ✔

**Paso 3 — α + β = −6 + 9 = 3.**

**Respuesta: (A) 3.**

---

## Ejercicio 5 — (Primer parcial, segundo semestre 2018)

> Ecuación con condición inicial:  y' = (y − 2)² / (x + 1)² ,  y(0) = 5/2. Entonces y(1) vale:
> (A) 4   (B) 9/2   (C) 2   (D) 8/3

**Paso 1 — separo.**

    dy / (y − 2)² = dx / (x + 1)².

**Paso 2 — integro.** En los dos lados uso la **regla de la potencia** con exponente −2 (o cambio de variable t = y − 2, t = x + 1):

- ∫ (y − 2)^(−2) dy = (y − 2)^(−1)/(−1) = −1/(y − 2).
- ∫ (x + 1)^(−2) dx = −1/(x + 1).

Entonces:

    −1/(y − 2) = −1/(x + 1) + C.

Multiplico por −1:

    1/(y − 2) = 1/(x + 1) − C.

**Paso 3 — condición inicial.** En x = 0, y = 5/2, entonces y − 2 = 1/2 y 1/(y−2) = 2:

    2 = 1/(0 + 1) − C = 1 − C  →  C = −1.

Así:

    1/(y − 2) = 1/(x + 1) + 1.

**Paso 4 — evalúo en x = 1.**

    1/(y − 2) = 1/2 + 1 = 3/2  →  y − 2 = 2/3  →  y = 2 + 2/3 = 8/3.

**Respuesta: (D) 8/3.**

---

## Moraleja del encuentro

- En múltiple opción, **no adivines**: resolvé y después elegí. Muchas veces el distractor sale de un error típico (olvidar la parte polinómica de y_p, equivocar el signo de C, etc.).
- Reconocé la **resonancia** por el "grado de más" (x²·e^(3x) cuando el RHS es e^(3x)) → te dice que la raíz es doble.
- Con condiciones iniciales, **despejá la constante antes** de evaluar en el punto pedido (como en el ejercicio 5).

> **Siguiente encuentro (8):** las **aplicaciones** (caída con resistencia del aire, población logística, represa, y base de soluciones).
