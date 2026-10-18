# Encuentro 6 — Ecuaciones de segundo orden NO homogéneas

> **Práctico 1 (Ecuaciones diferenciales), ejercicio 9, incisos a) a h).**
> Todas tienen condiciones iniciales. Son el tipo de ejercicio que **más** aparece en parciales: hay que hacerlo con método y sin apuro.

---

## Qué teoría necesito (repaso)

Una ecuación **lineal de segundo orden no homogénea** con coeficientes constantes:

> y'' + a·y' + b·y = f(x)

**La solución general es:**

> y = y_h + y_p

- **y_h** es la solución general de la **homogénea** (y'' + a·y' + b·y = 0), la resolvés con la característica (Encuentro 4).
- **y_p** es **una** solución particular de la no homogénea completa.

**¿Cómo encuentro una y_p? Con una "prueba educada".** Miro qué forma tiene f(x) y pruebo algo parecido:

| Si f(x) es… | Pruebo y_p = … |
|---|---|
| una constante | una constante k |
| un polinomio de grado n (ej. 3x² − 5x) | otro polinomio del mismo grado (ax² + bx + c) |
| e^(kx) | C·e^(kx) |
| cos(ωx) o sen(ωx) | C·cos(ωx) + D·sen(ωx) |
| una **suma** de cosas | la suma de las pruebas de cada cosa (linealidad) |

**Regla de la resonancia (¡ojo!).** Si lo que pruebo es **justo una solución de la homogénea**, hay que multiplicar por x (y por x² si la raíz es doble). Ejemplo: si y'' + y = cos x, el cos x ya es solución de la homogénea, así que pruebo x·(C cos x + D sen x).

**Después de armar y = y_h + y_p**, aplico las condiciones iniciales reemplazando en x = 0 (o el que toque).

> **Dato útil para a, b, c:** la homogénea y'' + 2y' + 2y = 0 tiene característica r² + 2r + 2 = 0 → r = −1 ± i, así que
> **y_h = e^(−x)·(A·cos x + B·sen x)**.
> Y como las condiciones iniciales de a, b, c son y(0) = 1, y'(0) = 0, voy a necesitar la derivada:
> y_h' = −e^(−x)(A cos x + B sen x) + e^(−x)(−A sen x + B cos x). En x = 0 esto vale **−A + B**.

---

## 9.a)  y'' + 2y' + 2y = cos(2x),  y(0) = 1,  y'(0) = 0

**Paso 1 — la homogénea.** y_h = e^(−x)(A cos x + B sen x) (está arriba).

**Paso 2 — pruebo y_p.** Como f(x) = cos(2x), pruebo

    y_p = C·cos(2x) + D·sen(2x).

**¿Hay resonancia?** La homogénea tiene frecuencia 1 (cos x, sen x), y acá la frecuencia es 2. No coinciden, así que **no** hace falta la x.

**Paso 3 — derivo y_p.** Regla de la cadena: (cos 2x)' = −2 sen 2x, (sen 2x)' = 2 cos 2x:

    y_p'  = −2C·sen(2x) + 2D·cos(2x)
    y_p'' = −4C·cos(2x) − 4D·sen(2x)

**Paso 4 — reemplazo en y'' + 2y' + 2y.**

    (−4C cos 2x − 4D sen 2x) + 2(−2C sen 2x + 2D cos 2x) + 2(C cos 2x + D sen 2x)

Agrupo por cos 2x y sen 2x:

    cos 2x:  −4C + 4D + 2C = −2C + 4D
    sen 2x:  −4D − 4C + 2D = −4C − 2D

Esto tiene que dar cos(2x) = 1·cos 2x + 0·sen 2x:

    −2C + 4D = 1
    −4C − 2D = 0

**Paso 5 — resuelvo el sistema.** De la segunda: −4C = 2D → D = −2C. Reemplazo en la primera:

    −2C + 4(−2C) = −2C − 8C = −10C = 1  →  C = −1/10.

Entonces D = −2(−1/10) = 1/5. Así:

    y_p = −1/10·cos(2x) + 1/5·sen(2x).

**Paso 6 — condiciones iniciales.** y = y_h + y_p. Primero y(0): cos 0 = 1, sen 0 = 0, así que y_h(0) = A y y_p(0) = −1/10:

    y(0) = A − 1/10 = 1  →  A = 11/10.

Ahora y'(0). Ya sabía que y_h'(0) = −A + B. Y derivo y_p: (sen 2x)' = 2 cos 2x, (cos 2x)' = −2 sen 2x:

    y_p' = −1/10·(−2 sen 2x) + 1/5·(2 cos 2x) = 1/5·sen 2x + 2/5·cos 2x  →  y_p'(0) = 2/5.

Entonces:

    y'(0) = (−A + B) + 2/5 = 0  →  B = A − 2/5 = 11/10 − 4/10 = 7/10.

**Solución:**

    y = e^(−x)·( 11/10·cos x + 7/10·sen x ) − 1/10·cos 2x + 1/5·sen 2x.

---

## 9.b)  y'' + 2y' + 2y = sen(2x),  y(0) = 1,  y'(0) = 0

Es igual al 9.a pero con el lado derecho sen(2x). Uso la misma y_p = C cos 2x + D sen 2x, y los mismos coeficientes de antes:

    cos 2x:  −2C + 4D
    sen 2x:  −4C − 2D

Ahora esto debe dar sen(2x) = 0·cos 2x + 1·sen 2x:

    −2C + 4D = 0
    −4C − 2D = 1

**Resuelvo.** De la primera: −2C = −4D → C = 2D. Reemplazo en la segunda:

    −4(2D) − 2D = −8D − 2D = −10D = 1  →  D = −1/10  →  C = −1/5.

    y_p = −1/5·cos(2x) − 1/10·sen(2x).

**Condiciones iniciales.** y_p(0) = −1/5 (el sen 0 se va):

    y(0) = A − 1/5 = 1  →  A = 6/5.

Derivo y_p: (−1/5 cos 2x)' = 2/5 sen 2x ; (−1/10 sen 2x)' = −1/5 cos 2x → y_p'(0) = −1/5.

    y'(0) = (−A + B) − 1/5 = 0  →  B = A + 1/5 = 6/5 + 1/5 = 7/5.

**Solución:**

    y = e^(−x)·( 6/5·cos x + 7/5·sen x ) − 1/5·cos 2x − 1/10·sen 2x.

---

## 9.c)  y'' + 2y' + 2y = cos(2x) + sen(2x),  y(0) = 1,  y'(0) = 0

**Idea (linealidad):** si y_p₁ es particular para cos 2x y y_p₂ lo es para sen 2x, entonces y_p₁ + y_p₂ lo es para la suma. ¡Ya las tengo de 9.a y 9.b!

    y_p = [ −1/10 cos 2x + 1/5 sen 2x ] + [ −1/5 cos 2x − 1/10 sen 2x ]
        = ( −1/10 − 1/5 )·cos 2x + ( 1/5 − 1/10 )·sen 2x
        = −3/10·cos 2x + 1/10·sen 2x.

**Condiciones iniciales.** y_p(0) = −3/10:

    y(0) = A − 3/10 = 1  →  A = 13/10.

Derivo y_p: (−3/10 cos 2x)' = 3/5 sen 2x ; (1/10 sen 2x)' = 1/5 cos 2x → y_p'(0) = 1/5.

    y'(0) = (−A + B) + 1/5 = 0  →  B = A − 1/5 = 13/10 − 2/10 = 11/10.

**Solución:**

    y = e^(−x)·( 13/10·cos x + 11/10·sen x ) − 3/10·cos 2x + 1/10·sen 2x.

---

## 9.d)  y'' + y = 3x² − 5x,  y(0) = 1,  y'(0) = 0

**Paso 1 — homogénea.** r² + 1 = 0 → r = ±i → y_h = A·cos x + B·sen x.

**Paso 2 — pruebo y_p.** f(x) es un polinomio de grado 2, pruebo

    y_p = a·x² + b·x + c.

(No hay resonancia: la homogénea tiene cos y sen, no polinomios.)

**Paso 3 — derivo.** Regla de la potencia:

    y_p'  = 2a·x + b
    y_p'' = 2a

**Paso 4 — reemplazo en y'' + y.**

    2a + (a·x² + b·x + c) = a·x² + b·x + (2a + c)

Igualo con 3x² − 5x + 0:

    a = 3
    b = −5
    2a + c = 0  →  2·3 + c = 0  →  c = −6

    y_p = 3x² − 5x − 6.

**Paso 5 — condiciones iniciales.** y(0) = A·1 + 0 + (−6) = A − 6 = 1 → A = 7.

Derivo toda la y (homogénea + particular):

    y' = −A·sen x + B·cos x + 6x − 5.
    y'(0) = −A·0 + B·1 + 0 − 5 = B − 5 = 0  →  B = 5.

**Solución:**

    y = 7·cos x + 5·sen x + 3x² − 5x − 6.

**Verificación.** y(0) = 7 − 6 = 1 ✔. y'(0) = 5 − 5 = 0 ✔.

---

## 9.e)  y'' + 4y' + 3y = 3e^x + x,  y(0) = 1,  y'(0) = 0

**Paso 1 — homogénea.** r² + 4r + 3 = 0 → busco dos números que multiplicados den 3 y sumados den 4: 1 y 3 → (r + 1)(r + 3) = 0 → r = −1, −3.

    y_h = A·e^(−x) + B·e^(−3x).

**Paso 2 — pruebo y_p.** El lado derecho es 3e^x + x: una exponencial de frecuencia 1 (no es raíz, las raíces son −1 y −3) y un polinomio de grado 1. Pruebo

    y_p = C·e^x + (a·x + b).

**Paso 3 — derivo.**

    y_p'  = C·e^x + a
    y_p'' = C·e^x

**Paso 4 — reemplazo en y'' + 4y' + 3y.**

    C e^x + 4(C e^x + a) + 3(C e^x + a x + b)

Distribuyo y agrupo:

    e^x:  C + 4C + 3C = 8C
    x:    3a
    const: 4a + 3b

Igualo con 3e^x + x = 3e^x + 1·x + 0:

    8C = 3      →  C = 3/8
    3a = 1      →  a = 1/3
    4a + 3b = 0 →  4/3 + 3b = 0  →  3b = −4/3  →  b = −4/9

    y_p = 3/8·e^x + 1/3·x − 4/9.

**Paso 5 — condiciones iniciales.**

    y(0) = A + B + 3/8 − 4/9 = 1.

Calculo 3/8 − 4/9 = 27/72 − 32/72 = −5/72. Entonces A + B = 1 + 5/72 = 77/72.

Derivo toda la y:

    y' = −A·e^(−x) − 3B·e^(−3x) + 3/8·e^x + 1/3.
    y'(0) = −A − 3B + 3/8 + 1/3 = 0.

3/8 + 1/3 = 9/24 + 8/24 = 17/24. Así que −A − 3B = −17/24, o sea A + 3B = 17/24.

**Sistema:**

    A + B = 77/72
    A + 3B = 17/24 = 51/72

Resto: 2B = 51/72 − 77/72 = −26/72 = −13/36 → B = −13/72. Y A = 77/72 − B = 77/72 + 13/72 = 90/72 = 5/4.

**Solución:**

    y = 5/4·e^(−x) − 13/72·e^(−3x) + 3/8·e^x + 1/3·x − 4/9.

**Verificación.** y(0) = 5/4 − 13/72 + 3/8 − 4/9 = (90 − 13 + 27 − 32)/72 = 72/72 = 1 ✔.
y'(0) = −5/4 + 39/72 + 3/8 + 1/3 = (−90 + 39 + 27 + 24)/72 = 0 ✔.

---

## 9.f)  y'' + y = (1 + x)²,  y(0) = 1,  y'(0) = 0

**Paso 1 — homogénea.** y_h = A·cos x + B·sen x.

**Paso 2 — desarrollo el lado derecho.** (1 + x)² = 1 + 2x + x². Es un polinomio de grado 2, pruebo y_p = a x² + b x + c.

**Paso 3 — derivo y reemplazo (igual que 9.d).**

    y_p'' + y_p = 2a + (a x² + b x + c) = a x² + b x + (2a + c).

Igualo con x² + 2x + 1:

    a = 1
    b = 2
    2a + c = 1  →  2 + c = 1  →  c = −1

    y_p = x² + 2x − 1.

**Paso 4 — condiciones iniciales.** y(0) = A + (−1) = 1 → A = 2.

    y' = −A sen x + B cos x + 2x + 2  →  y'(0) = B + 2 = 0  →  B = −2.

**Solución:**

    y = 2·cos x − 2·sen x + x² + 2x − 1.

---

## 9.g)  y'' + 2y' + y = x,  y(0) = 0,  y'(0) = 0

**Paso 1 — homogénea.** r² + 2r + 1 = (r + 1)² = 0 → r = −1 **doble**:

    y_h = (A + B·x)·e^(−x).

**Paso 2 — pruebo y_p.** f(x) = x es polinomio de grado 1: pruebo y_p = a x + b. (La homogénea tiene e^(−x) y x e^(−x), no polinomios, así que no hay resonancia.)

**Paso 3 — derivo y reemplazo.**

    y_p' = a,  y_p'' = 0.
    y_p'' + 2y_p' + y_p = 0 + 2a + (a x + b) = a x + (2a + b).

Igualo con 1·x + 0:

    a = 1,  2a + b = 0  →  2 + b = 0  →  b = −2.

    y_p = x − 2.

**Paso 4 — condiciones iniciales.** y(0) = (A + 0)·1 + (0 − 2) = A − 2 = 0 → A = 2.

Derivo la homogénea con la **regla del producto**: ((A + Bx)e^(−x))' = B·e^(−x) + (A + Bx)·(−e^(−x)) = e^(−x)·(B − A − Bx). Entonces

    y' = e^(−x)·(B − A − Bx) + 1.
    y'(0) = (B − A) + 1 = 0  →  B = A − 1 = 1.

**Solución:**

    y = (2 + x)·e^(−x) + x − 2.

**Verificación.** y(0) = 2 − 2 = 0 ✔. y'(0) = (1 − 2) + 1 = 0 ✔.

---

## 9.h)  y'' + y = cos x,  y(0) = 0,  y'(0) = 1

**Paso 1 — homogénea.** y_h = A·cos x + B·sen x.

**Paso 2 — ¡RESONANCIA!** El lado derecho es cos x, que **ya es solución de la homogénea**. Entonces hay que multiplicar por x. Pruebo:

    y_p = x·( C·cos x + D·sen x ).

**Paso 3 — derivo (regla del producto, dos veces).**

    y_p  = x·(C cos x + D sen x)
    y_p' = (C cos x + D sen x) + x·(−C sen x + D cos x)
    y_p'' = (−C sen x + D cos x) + (−C sen x + D cos x) + x·(−C cos x − D sen x)
          = 2·(−C sen x + D cos x) + x·(−C cos x − D sen x)

(derivé el paréntesis (C cos x + D sen x) → −C sen x + D cos x, dos veces, y el x·(...) una vez más).

**Paso 4 — reemplazo en y'' + y.** Sumo y_p'' + y_p. Los términos con x se cancelan:

    x-part:  x·(−C cos x − D sen x) + x·(C cos x + D sen x) = 0
    resto:   2·(−C sen x + D cos x)

Así que:

    y_p'' + y_p = −2C·sen x + 2D·cos x.

Igualo con cos x = 0·sen x + 1·cos x:

    −2C = 0  →  C = 0
    2D = 1   →  D = 1/2

    y_p = 1/2·x·sen x.

**Paso 5 — condiciones iniciales.** y(0) = A·1 + 0 = A = 0.

    y = 0·cos x + B·sen x + 1/2·x·sen x.
    y' = B·cos x + 1/2·( sen x + x·cos x )   (derivé el producto x·sen x)

    y'(0) = B·1 + 1/2·(0 + 0) = B = 1.

**Solución:**

    y = sen x + 1/2·x·sen x.

**Verificación.** y(0) = 0 ✔. y'(0) = 1 ✔.

---

## Moraleja del encuentro

- Siempre **dos** piezas: y_h (homogénea) + y_p (una particular).
- La forma de y_p la sugiere f(x); si hay **resonancia** (f(x) ya es solución de la homogénea), multiplicás por x.
- Si f(x) es una suma, podés hacer cada parte por separado y sumar (linealidad).
- Recién al final aplicás las condiciones iniciales, y con cuidado con la derivada de y_h (producto).

> **Siguiente encuentro (7):** los ejercicios de **evaluaciones anteriores** (parciales y exámenes) del Práctico 1.
