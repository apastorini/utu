# Encuentro 1 — Ecuaciones de variables separables

> **Práctico 1 (Ecuaciones diferenciales), ejercicios 1 y 2.**
> Acá arranca todo: es el método más simple y el que más vas a usar.

---

## Qué teoría necesito (repaso)

Una **ecuación diferencial** es una ecuación donde la incógnita es una **función** y aparecen sus derivadas. Por ejemplo, y' = 2y pide: *"¿qué función y(x) tiene, en cada punto, una pendiente igual a dos veces su propio valor?"*.

Una ecuación de **primer orden** de variables **separables** tiene la forma:

> y' = f(x)·g(y)

Es decir: el lado derecho es **un pedazo que depende solo de x** por **otro pedazo que depende solo de y** (un producto).

**El método (siempre el mismo):**

1. Escribo y' como dy/dx:  dy/dx = f(x)·g(y).
2. **Separo**: mando todo lo que tenga y con dy, y todo lo que tenga x con dx:
    dy / g(y) = f(x) dx.
3. **Integro los dos lados**:
    ∫ dy / g(y) = ∫ f(x) dx.
4. Igualo a una constante C (una sola, del lado de x alcanza).
5. **Despejo y** si se puede (solución explícita); si no, dejo la relación (solución implícita).

> **Detalle importante:** cuando "paso dividiendo" g(y), estoy suponiendo g(y) ≠ 0. Los valores donde g(y) = 0 dan **soluciones constantes** que a veces se pierden. Los reviso aparte.

---

## Ejercicio 1 — variables separables

> Resolver: a) y' = 2y  b) y' = xy  c) y' = y²  d) y' = x(1 + y²)  e) y' = x√y

### 1.a)  y' = 2y

**Paso 1.** Escribo la derivada como cociente:

    dy/dx = 2y

**Paso 2.** Separo (todo lo de y a la izquierda, todo lo de x a la derecha). Paso y dividiendo y dx multiplicando:

    dy / y = 2 dx

**Paso 3.** Integro:

    ∫ dy/y = ∫ 2 dx
    ln|y| = 2x + C

**Paso 4.** Despejo y (aplico exponencial a los dos lados):

    |y| = e^(2x + C) = e^C · e^(2x)

Como e^C es una constante positiva, la llamo K y absorbo también el signo del módulo:

    y = K · e^(2x)      (K ∈ ℝ)

**Paso 5 — verificación.** Derivo y = K e^(2x): y' = 2K e^(2x) = 2·(K e^(2x)) = 2y ✔

> **Comentario.** El caso g(y) = y = 0 da la solución y ≡ 0, que queda incluida en K = 0. Por eso no la perdimos.

### 1.b)  y' = xy

**Paso 1.** dy/dx = x·y.

**Paso 2.** Separo:

    dy/y = x dx

**Paso 3.** Integro:

    ln|y| = x²/2 + C

**Paso 4.** Exponencial:

    y = K · e^(x²/2)

**Paso 5 — verificación.** y' = K · e^(x²/2) · (x) = x·(K e^(x²/2)) = x·y ✔

> **Comentario.** Fijate que acá f(x) = x y g(y) = y. Es el mismo molde que (a), solo con f(x) = x.

### 1.c)  y' = y²

**Paso 1.** dy/dx = y².

**Paso 2.** Separo (ojo: y² va al denominador):

    dy / y² = dx

**Paso 3.** Integro. Recuerdo que ∫ y^(-2) dy = −y^(-1):

    −1/y = x + C

**Paso 4.** Despejo y. Multiplico por −1:  1/y = −x − C = −(x + C). Invierto:

    y = −1/(x + C)

**Paso 5 — verificación.** y = −(x + C)^(−1) → y' = +(x + C)^(−2) = 1/(x + C)². Y y² = 1/(x + C)². Coinciden ✔

> **Comentario / trampa.** Cuando separé dividí por y², así que supuse y ≠ 0. La función y ≡ 0 **también es solución** (0' = 0 = 0²) y **no** aparece en la familia −1/(x + C). Es una solución "extra" que hay que agregar aparte. Regla: cada vez que dividís por algo que se puede anular, revisá el caso "eso = 0".

### 1.d)  y' = x(1 + y²)

**Paso 1.** dy/dx = x·(1 + y²). Acá f(x) = x y g(y) = 1 + y².

**Paso 2.** Separo:

    dy / (1 + y²) = x dx

**Paso 3.** Integro. La integral de la izquierda es el arctan (esto hay que saberlo de memoria):

    arctan(y) = x²/2 + C

**Paso 4.** Despejo y aplicando tangente a los dos lados:

    y = tan(x²/2 + C)

**Paso 5 — verificación.** y' = sec²(x²/2 + C) · (x) = x·sec²(...). Y 1 + y² = 1 + tan²(...) = sec²(...). Entonces y' = x(1 + y²) ✔

> **Comentario.** No hay que tener miedo a la tan: es la única forma de "sacar" el arctan. La solución vale en los intervalos donde el coseno del argumento no se anula.

### 1.e)  y' = x√y

**Paso 1.** dy/dx = x·√y = x·y^(1/2).

**Paso 2.** Separo. Paso √y dividiendo, o sea y^(−1/2) dy:

    y^(−1/2) dy = x dx

**Paso 3.** Integro. ∫ y^(−1/2) dy = 2·y^(1/2) = 2√y:

    2√y = x²/2 + C

**Paso 4.** Despejo. Divido por 2: √y = x²/4 + C/2. Llamo K = C/2 y elevo al cuadrado:

    y = (x²/4 + K)²

**Paso 5 — verificación.** y = (x²/4 + K)². y' = 2(x²/4 + K)·(x/2) = x·(x²/4 + K). Y √y = |x²/4 + K|. Si x²/4 + K ≥ 0, coincide ✔ (ese es el rango donde vale la solución).

> **Comentario / trampa.** Otra vez dividí por √y, así que supuse y > 0. La solución nula y ≡ 0 también sirve y va aparte.

---

## Ejercicio 2 — solución general de separables

> a) y' = y² − 1   b) y·y' + 1 = 0   c) x·e^(2y)·y' − (1 + e^(2y)) = 0

### 2.a)  y' = y² − 1

**Paso 1.** dy/dx = (y² − 1). El lado derecho depende solo de y; es separable con f(x) = 1.

**Paso 2.** Separo:

    dy / (y² − 1) = dx

**Paso 3.** Necesito integrar 1/(y² − 1). Uso **fracciones simples**. Como y² − 1 = (y−1)(y+1),

    1/(y² − 1) = 1/2 · [ 1/(y−1) − 1/(y+1) ]

Integro:

    1/2 · [ln|y−1| − ln|y+1|] = x + C
    1/2 · ln| (y−1)/(y+1) | = x + C

**Paso 4.** Multiplico por 2 y aplico exponencial:

    | (y−1)/(y+1) | = e^(2x + 2C) = A·e^(2x)      (A > 0)

Absorbo el signo en la constante (A ahora puede ser cualquier real no nulo):

    (y−1)/(y+1) = A·e^(2x)

**Paso 5.** Despejo y. Multiplico cruzado:

    y − 1 = A·e^(2x)·(y + 1)
    y − 1 = A·e^(2x)·y + A·e^(2x)
    y − A·e^(2x)·y = 1 + A·e^(2x)
    y·(1 − A·e^(2x)) = 1 + A·e^(2x)
    y = (1 + A·e^(2x)) / (1 − A·e^(2x))

**Verificación (rápida, en un punto).** Con A = 0 queda y = 1. Reemplazo: y' = 0 y y² − 1 = 1 − 1 = 0 ✔. Con A = 1 y x = 0: y = (1+1)/(1−1) → se va a infinito; tiene sentido porque ahí el denominador se anula (y = 1 es asíntota).

> **Comentario / trampa.** Al separar dividí por (y² − 1), así que excluí y = 1 e y = −1. Esas dos constantes son **soluciones** (1' = 0 = 1² − 1 ✔; (−1)' = 0 = 1 − 1 ✔). La familia general las recupera como casos límite (A → 0 da y = 1), pero conviene mencionarlas.

### 2.b)  y·y' + 1 = 0

**Paso 1.** Despejo y':  y·y' = −1  →  y' = −1/y.

**Paso 2.** Separo:

    y dy = −dx

**Paso 3.** Integro:

    y²/2 = −x + C

**Paso 4.** Despejo:

    y² = −2x + 2C = −2x + K
    y = ±√(K − 2x)

> **Comentario.** Es una familia de "medias parábolas" acostadas. El signo ± es porque y aparece al cuadrado. La constante K se ajusta con las condiciones iniciales.

### 2.c)  x·e^(2y)·y' − (1 + e^(2y)) = 0

**Paso 1.** Despejo el término con y':

    x·e^(2y)·y' = 1 + e^(2y)

**Paso 2.** Separo: paso x dividiendo al otro lado y e^(2y) al lado de y:

    e^(2y) / (1 + e^(2y)) · dy = dx / x

**Paso 3.** Integro la izquierda. Hago el cambio t = 1 + e^(2y), entonces dt = 2·e^(2y) dy, o sea e^(2y) dy = dt/2:

    ∫ e^(2y)/(1 + e^(2y)) dy = 1/2 · ln(1 + e^(2y))

La derecha es ln|x|. Queda:

    1/2 · ln(1 + e^(2y)) = ln|x| + C

**Paso 4.** Multiplico por 2 y aplico exponencial:

    ln(1 + e^(2y)) = 2 ln|x| + 2C
    1 + e^(2y) = K·x²         (llamé K = e^(2C))

**Paso 5.** Despejo y:

    e^(2y) = K·x² − 1
    2y = ln(K·x² − 1)
    y = 1/2 · ln(K·x² − 1)

**Verificación.** Derivo: y' = 1/2 · (2Kx)/(Kx² − 1) = Kx/(Kx² − 1). Reemplazo en la ecuación original x·e^(2y)·y' − (1 + e^(2y)): como e^(2y) = Kx² − 1, queda x·(Kx²−1)·[Kx/(Kx²−1)] − (Kx²−1+1) = Kx² − Kx² = 0 ✔

> **Comentario.** Este ejercicio muestra el truco típico cuando aparece e^(algo): el cambio t = 1 + e^(algo) para integrar. Vale el rango donde Kx² − 1 > 0.

---

## Moraleja del encuentro

- Reconocer "f(x) por g(y)" es el 80% del trabajo: mirá si **podés separar** la x de la y.
- Siempre **una sola constante** C.
- Cada vez que dividís por una expresión que se puede anular, **revisá esa solución aparte** (las constantes y ≡ c).
- Al final, si podés, **verificá derivando**. Es rápido y te saca de dudas.

> **Siguiente encuentro (2):** el cambio u = y/x para ecuaciones donde el lado derecho depende solo del cociente y/x (Práctico 1, ej. 3).
