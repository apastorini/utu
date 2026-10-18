# Encuentro 8 — Aplicaciones y problemas complementarios (Práctico 1)

> **Práctico 1, "Aplicaciones y Problemas Complementarios" (1 a 4).**
> Acá la matemática es la misma de antes, pero vestida de problema "de la vida real". El trabajo está en **traducir el enunciado a una ecuación** y después resolver.
> Detallo cada integral y cada derivada.

---

## Aplicación 1 — Caída con resistencia del aire

> La ecuación m·v' = m·g − k·v representa la velocidad v(t) de caída de un cuerpo de masa m, donde g es la gravedad y k < mg una constante de resistencia del aire.
> a) Hallar v(t) con velocidad inicial v(0) = v₀.
> b) Hallar el límite de v(t) cuando t → +∞ (llamado v∞).
> c) ¿Cuánto tarda en alcanzar la velocidad (v∞ + v₀)/2?
> d) Con v₀ = 0, distancia recorrida cuando la velocidad es v∞/2.

**La ecuación, ordenada.** Divido por m:

    v' = g − (k/m)·v   →   v' + (k/m)·v = g.

Es **lineal de primer orden** (Encuentro 3) con a = k/m y b = g.

### a) Hallar v(t)

**Paso 1 — factor integrante.** ∫a dt = ∫(k/m) dt = (k/m)·t (la constante k/m es constante, así que integro una constante → por t):

    μ = e^((k/m)·t).

**Paso 2 — la ecuación se vuelve derivada de producto.**

    ( v·e^((k/m)t) )' = g·e^((k/m)t).

**Paso 3 — integro.** Necesito ∫ g·e^((k/m)t) dt. Uso la tabla (∫ e^(ct) dt = e^(ct)/c) con c = k/m:

    ∫ g·e^((k/m)t) dt = g·e^((k/m)t)/(k/m) = (m·g/k)·e^((k/m)t).

Entonces:

    v·e^((k/m)t) = (m·g/k)·e^((k/m)t) + C.

**Paso 4 — despejo v.** Divido por e^((k/m)t):

    v(t) = m·g/k + C·e^(−(k/m)t).

**Paso 5 — condición inicial.** v(0) = v₀, y e⁰ = 1:

    v₀ = m·g/k + C  →  C = v₀ − m·g/k.

**Solución:**

> v(t) = m·g/k + ( v₀ − m·g/k )·e^(−(k/m)t).

### b) Límite cuando t → +∞

Como k/m > 0, la exponencial e^(−(k/m)t) → 0. Entonces:

> v∞ = límite (t→∞) v(t) = m·g/k.

(Sentido físico: la gravedad empuja y el aire frena; se llega a una velocidad límite en la que se equilibran.)

### c) Tiempo en alcanzar (v∞ + v₀)/2

**Paso 1 — planteo la igualdad.** Con v∞ = mg/k:

    mg/k + (v₀ − mg/k)·e^(−(k/m)t) = ( mg/k + v₀ ) / 2.

**Paso 2 — despejo la exponencial.** Paso mg/k restando:

    (v₀ − mg/k)·e^(−(k/m)t) = (mg/k + v₀)/2 − mg/k = (v₀ − mg/k)/2.

Divido por (v₀ − mg/k) (suponiendo v₀ ≠ mg/k):

    e^(−(k/m)t) = 1/2.

**Paso 3 — aplico ln.**

    −(k/m)·t = ln(1/2) = −ln 2  →  t = (m/k)·ln 2.

### d) v₀ = 0: distancia recorrida cuando v = v∞/2

**Paso 1 — velocidad con v₀ = 0.** Reemplazo en la solución general:

    v(t) = mg/k·( 1 − e^(−(k/m)t) ).

**Paso 2 — instante en que v = v∞/2 = mg/(2k).**

    mg/k·( 1 − e^(−(k/m)t) ) = mg/(2k)  →  1 − e^(−(k/m)t) = 1/2  →  e^(−(k/m)t) = 1/2  →  t = (m/k)·ln 2.

(El mismo tiempo que en el inciso c con v₀ = 0.)

**Paso 3 — la distancia es la integral de la velocidad.** Si x(t) es la posición, x'(t) = v(t), así que

    x(t) = ∫₀^t v(s) ds = ∫₀^t (mg/k)·( 1 − e^(−(k/m)s) ) ds.

Separo y uso la tabla (∫ e^(cs) ds = e^(cs)/c):

    x(t) = (mg/k)·[ s + (m/k)·e^(−(k/m)s) ]₀^t
         = (mg/k)·[ ( t + (m/k)e^(−(k/m)t) ) − ( 0 + (m/k)·1 ) ]
         = (mg/k)·[ t + (m/k)e^(−(k/m)t) − m/k ].

**Paso 4 — evalúo en t = (m/k)·ln 2.** Ahí e^(−(k/m)t) = 1/2:

    x = (mg/k)·[ (m/k)ln 2 + (m/k)(1/2) − m/k ]
      = (mg/k)·(m/k)·[ ln 2 + 1/2 − 1 ]
      = (m²g/k²)·( ln 2 − 1/2 ).

> **Distancia recorrida = (m²·g/k²)·(ln 2 − 1/2).**

---

## Aplicación 2 — Población (ecuación logística)

> La ecuación x' = α·x·(A − x) representa la evolución de una población (α, A > 0).
> a) Demostrar que ninguna solución tiene extremos relativos.
> b) Límite cuando t → +∞ de la solución con x(0) = A/2.
> c) Tiempo para que una población de A/2 se incremente un 50%.

### a) Ninguna solución tiene extremos relativos

Un **extremo relativo** de x(t) ocurriría donde x'(t) = 0 (la tangente horizontal) pero la función no es constante. Miro cuándo se anula x':

    x' = α·x·(A − x) = 0  →  x = 0  o  x = A.

O sea, la derivada solo se anula cuando x = 0 o x = A. Pero x ≡ 0 y x ≡ A son **soluciones constantes** (si x = 0, entonces x' = 0 siempre; si x = A, también). Para una solución **no constante**, x(t) nunca vale 0 ni A (por unicidad: no puede cruzar una solución constante), así que x' nunca se anula. Por lo tanto **no hay extremos relativos**: la población siempre sube o siempre baja. ✔

### b) Límite con x(0) = A/2

**Paso 1 — separo variables.**

    dx / [ x·(A − x) ] = α dt.

**Paso 2 — fracciones simples.** Escribo 1/[x(A−x)] = (1/A)·[ 1/x + 1/(A − x) ]. Verifico juntando: (1/A)·[ (A − x) + x ] / [x(A−x)] = (1/A)·A/[x(A−x)] = 1/[x(A−x)] ✔.

**Paso 3 — integro.** Cada pedazo es de tabla (∫1/u du = ln|u|):

    (1/A)·[ ln|x| − ln|A − x| ] = α·t + C.

(Uso que ∫ dx/(A−x) = −ln|A−x|.) Entonces:

    (1/A)·ln| x/(A − x) | = α·t + C.

**Paso 4 — despejo.** Multiplico por A y aplico exponencial:

    x/(A − x) = K·e^(Aαt).

**Paso 5 — condición inicial x(0) = A/2.**

    (A/2)/(A/2) = 1 = K·e⁰ = K  →  K = 1.

**Paso 6 — despejo x.**

    x = (A − x)·e^(Aαt)  →  x·( 1 + e^(Aαt) ) = A·e^(Aαt)  →  x = A·e^(Aαt)/( 1 + e^(Aαt) ).

Divido numerador y denominador por e^(Aαt):

    x(t) = A / ( 1 + e^(−Aαt) ).

**Paso 7 — límite.** Como Aα > 0, e^(−Aαt) → 0:

> Límite (t→∞) x(t) = A. (La población tiende a la capacidad A.)

### c) Tiempo para que A/2 se incremente un 50%

**Paso 1 — objetivo.** Partiendo de A/2, un aumento del 50% es llegar a:

    (A/2)·(1 + 1/2) = (A/2)·(3/2) = 3A/4.

**Paso 2 — planteo.** Uso x(t) = A/(1 + e^(−Aαt)):

    A / (1 + e^(−Aαt)) = 3A/4  →  1 + e^(−Aαt) = 4/3  →  e^(−Aαt) = 1/3.

**Paso 3 — aplico ln.**

    −Aα·t = ln(1/3) = −ln 3  →  t = (ln 3)/(Aα).

> **Tiempo = (ln 3)/(A·α).**

---

## Aplicación 3 — Represa

> La ecuación u' = −2·λ·t·u² representa la cantidad u(t) de agua en una represa (λ > 0).
> a) Solución con u(0) = u₀ > 0.
> b) Límite cuando t → +∞.
> c) Dado u₁ < u₀, hallar λ para que u(T) = u₁.
> d) Con u₀ = 2 (millones de hl), u₁ = 1,5 y T = 5 días, hallar λ.

### a) Solución con u(0) = u₀

**Paso 1 — separo.**

    du / u² = −2·λ·t·dt.

**Paso 2 — integro.** En la izquierda, regla de la potencia con n = −2: ∫ u^(−2) du = −1/u. En la derecha, ∫ −2λt dt = −λ·t² (saqué la constante −2λ y usé ∫ t dt = t²/2).

    −1/u = −λ·t² + C.

**Paso 3 — despejo.** Multiplico por −1:

    1/u = λ·t² − C.

Llamo K = −C (sigue siendo cualquier constante):

    1/u = λ·t² + K  →  u = 1/( λ·t² + K ).

**Paso 4 — condición inicial u(0) = u₀.** Con t = 0:

    u₀ = 1/K  →  K = 1/u₀.

**Solución:**

> u(t) = 1/( λ·t² + 1/u₀ ) = u₀ / ( 1 + λ·u₀·t² ).

### b) Límite cuando t → +∞

El denominador 1 + λ·u₀·t² → +∞ (con λ > 0), así que:

> Límite (t→∞) u(t) = 0.

### c) Hallar λ para que u(T) = u₁

**Paso 1 — planteo.**

    u₀ / ( 1 + λ·u₀·T² ) = u₁.

**Paso 2 — despejo λ.**

    1 + λ·u₀·T² = u₀/u₁  →  λ·u₀·T² = u₀/u₁ − 1 = (u₀ − u₁)/u₁  →  λ = (u₀ − u₁)/(u₁·u₀·T²).

### d) Números: u₀ = 2, u₁ = 1,5, T = 5

    λ = (2 − 1,5) / (1,5·2·5²) = 0,5 / (1,5·2·25) = 0,5 / 75 = 1/150.

> **λ = 1/150.** (Coincide con la respuesta del práctico.)

---

## Aplicación 4 — Base de soluciones (dimensión 2)

> Para cada ecuación:
> (I) y'' − 3y' + 2y = 0   (II) y'' + 4y' + 4y = 0   (III) 2y'' + 2y' + y = 0
> a) Hallar y₁, y₂ con y₁(0) = 1, y₁'(0) = 0  e  y₂(0) = 0, y₂'(0) = 1, y probar que son linealmente independientes.
> b) Dadas a, b reales, hallar la solución con y(0) = a, y'(0) = b y probar que y = a·y₁ + b·y₂.
> c) Deducir que {y₁, y₂} es base del espacio de soluciones, y que ese espacio tiene dimensión dos.

**Recordatorio — independencia lineal.** Dos funciones son linealmente independientes si ninguna es múltiplo de la otra. Herramienta práctica: el **wronskiano** W(x) = y₁·y₂' − y₁'·y₂. Si W(x) ≠ 0 en algún punto, son independientes. En x = 0, usando los datos:

    W(0) = y₁(0)·y₂'(0) − y₁'(0)·y₂(0) = 1·1 − 0·0 = 1 ≠ 0.

Es el mismo cálculo para las tres ecuaciones: **W(0) = 1**. Así que en las tres, {y₁, y₂} son independientes.

### (I)  y'' − 3y' + 2y = 0

Característica r² − 3r + 2 = (r − 1)(r − 2) = 0 → r = 1, 2. General:

    y = A·e^x + B·e^(2x),   y' = A·e^x + 2B·e^(2x).

- **y₁** (y₁(0)=1, y₁'(0)=0): A + B = 1 ; A + 2B = 0 → resto: B = −1 → A = 2. **y₁ = 2e^x − e^(2x)**.
- **y₂** (y₂(0)=0, y₂'(0)=1): A + B = 0 ; A + 2B = 1 → B = 1 → A = −1. **y₂ = −e^x + e^(2x)**.

### (II)  y'' + 4y' + 4y = 0

Característica (r + 2)² = 0 → r = −2 doble. General:

    y = (A + B·x)·e^(−2x).

Su derivada (regla del producto): y' = B·e^(−2x) − 2(A + Bx)e^(−2x) = e^(−2x)·( B − 2A − 2B·x ). En x = 0: y(0) = A ; y'(0) = B − 2A.

- **y₁**: A = 1 ; B − 2A = 0 → B = 2. **y₁ = (1 + 2x)·e^(−2x)**.
- **y₂**: A = 0 ; B − 0 = 1 → B = 1. **y₂ = x·e^(−2x)**.

### (III)  2y'' + 2y' + y = 0

Divido por 2: y'' + y' + (1/2)y = 0. Característica r² + r + 1/2 = 0. Con la fórmula:

    Δ = 1² − 4·(1/2) = 1 − 2 = −1  →  r = [ −1 ± √(−1) ] / 2 = −1/2 ± (1/2)i.

Raíces complejas (p = −1/2, q = 1/2). General:

    y = e^(−x/2)·( A·cos(x/2) + B·sen(x/2) ).

Derivada (regla del producto):

    y' = −1/2·e^(−x/2)(A cos(x/2) + B sen(x/2)) + e^(−x/2)( −A/2·sen(x/2) + B/2·cos(x/2) ).

En x = 0 (cos 0 = 1, sen 0 = 0): y(0) = A ; y'(0) = −A/2 + B/2 = (B − A)/2.

- **y₁**: A = 1 ; (B − 1)/2 = 0 → B = 1. **y₁ = e^(−x/2)·( cos(x/2) + sen(x/2) )**.
- **y₂**: A = 0 ; B/2 = 1 → B = 2. **y₂ = 2·e^(−x/2)·sen(x/2)**.

### b) y = a·y₁ + b·y₂ cumple las condiciones

Sea Y(x) = a·y₁(x) + b·y₂(x). Por **linealidad** (la ecuación es lineal y homogénea), Y es solución. Además:

    Y(0) = a·y₁(0) + b·y₂(0) = a·1 + b·0 = a.
    Y'(0) = a·y₁'(0) + b·y₂'(0) = a·0 + b·1 = b.

O sea, Y es una solución con exactamente los datos y(0) = a, y'(0) = b. Como el **problema de valores iniciales tiene solución única** (teorema de existencia y unicidad para estas ecuaciones), la solución con esos datos es Y. Por lo tanto:

> y(x) = a·y₁(x) + b·y₂(x).

### c) {y₁, y₂} es base; dimensión 2

- **Generan:** por el inciso b), **cualquier** solución y (con algún y(0) = a, y'(0) = b) se escribe como a·y₁ + b·y₂. Así que {y₁, y₂} genera el espacio de soluciones.
- **Son independientes:** el wronskiano en 0 es 1 ≠ 0, así que ninguna es múltiplo de la otra.

Un conjunto que genera e es independiente es una **base**. Entonces {y₁, y₂} es base del espacio de soluciones, y como tiene 2 elementos:

> **El espacio de soluciones tiene dimensión 2.**

---

## Moraleja del encuentro

- En aplicaciones, primero **traducí** el enunciado a una EDO (casi siempre separable o lineal de primer orden). Fijate en las palabras: "velocidad inicial" → dato v(0); "límite cuando t→∞" → mirá la exponencial.
- Las **integrales que aparecen** (∫ e^(ct) dt, ∫ u^(−2) du, fracciones simples) son todas de la tabla del repaso 0b.
- "Base" y "dimensión" salen de: **linealidad** (combinaciones son soluciones), **independencia** (wronskiano ≠ 0) y **unicidad** (los datos iniciales determinan la solución).

---

## Práctico 1 completo ✅

Llegaste al final del **Práctico 1 (Ecuaciones diferenciales)**: variables separables, cambio u = y/x, lineales, segundo orden (homogéneas y no homogéneas), ejercicios de exámenes y aplicaciones.

> **Próximo:** Práctico 2 (Sucesiones). Va a estar en `09_practico2_...`. Si querés, seguimos con el mismo nivel de detalle.
