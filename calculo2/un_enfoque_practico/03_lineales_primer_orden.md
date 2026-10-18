# Encuentro 3 — Ecuaciones lineales de primer orden

> **Práctico 1 (Ecuaciones diferenciales), ejercicio 4:**
> a) homogéneas (1, 2, 3) y b) no homogéneas (1, 2, 3).
> Cada integral, explicada. Apoyate en `00b_derivadas_e_integrales.md`.

---

## Qué teoría necesito (repaso)

Una ecuación **lineal de primer orden** se escribe, en su forma estándar:

> y' + a(x)·y = b(x)

**Homogénea** si b(x) = 0; **no homogénea** si b(x) ≠ 0.

### Caso homogéneo:  y' + a(x)·y = 0

Es separable: y' = −a(x)·y, entonces

    dy/y = −a(x) dx  →  ln|y| = −∫a(x) dx + C  →  y = K·e^(−∫a(x) dx)

La integral de la izquierda (∫ dy/y = ln|y|) sale de la tabla; para despejar aplico la exponencial.

### Caso no homogéneo: **factor integrante**

Busco una función μ(x) que convierta el lado izquierdo en la derivada de un producto. Pruebo

> μ(x) = e^(∫a(x) dx)

y mirá qué pasa: por la **regla del producto**,

    (μ·y)' = μ'·y + μ·y' = μ·a·y + μ·y' = μ·( y' + a·y ) = μ·b

(usé que μ' = μ·a, que es así porque μ = e^(∫a), y al derivar una exponencial por regla de la cadena vuelve a aparecer a). Entonces la ecuación se transforma en:

> ( μ·y )' = μ·b

que se integra directo:  μ·y = ∫ μ·b dx + C  →  y = (1/μ)·[ ∫ μ·b dx + C ].

**Pasos prácticos:**
1. Escribo la ecuación en forma estándar y' + a(x)y = b(x) (divido por el coeficiente de y').
2. Calculo μ = e^(∫a dx).
3. Multiplico y la reescribo como (μ y)' = μ b.
4. Integro y despejo y.

---

# Parte a) Homogéneas

## 4.a.1)  y' + y·cos x = 0

**Paso 1.** Ya está en forma estándar con a(x) = cos x y b = 0.

**Paso 2.** Es separable: dy/y = −cos x dx.

**Paso 3 — integro.**

    ∫ (1/y) dy = ∫ (−cos x) dx

- ∫ (1/y) dy = ln|y| (tabla, porque (ln|y|)' = 1/y).
- **¿Cómo integro ∫ (−cos x) dx?** Saco la constante −1 y uso la tabla al revés: como (sen x)' = cos x, la antiderivada de cos x es sen x. Entonces ∫ (−cos x) dx = −sen x.

Queda:

    ln|y| = −sen x + C

**Paso 4 — despejo.** Exponencial a los dos lados:

    y = K·e^(−sen x)

**Verificación.** Derivo K·e^(−sen x) con la **regla de la cadena** (la exponencial de una función):

    y' = K·e^(−sen x) · (−sen x)' = K·e^(−sen x)·(−cos x) = −cos x·y

Entonces y' + y·cos x = −cos x·y + y·cos x = 0 ✔

## 4.a.2)  x(x − 1)·y' + (1 − 2x)·y = 0

**Paso 1 — forma estándar.** Divido por x(x−1):

    y' + [ (1 − 2x)/(x(x−1)) ]·y = 0

Entonces a(x) = (1 − 2x)/(x(x−1)).

**Paso 2 — simplifico a(x) con fracciones simples.** Busco A y B tales que

    (1 − 2x)/(x(x−1)) = A/x + B/(x−1).

Junto: A(x−1) + Bx = (A+B)x − A debe igualar 1 − 2x. Entonces:
- A + B = −2
- −A = 1  →  A = −1  →  B = −1.

Así que

    a(x) = −1/x − 1/(x−1).

**Paso 3 — factor integrante.** Necesito ∫a dx:

    ∫ a dx = ∫ (−1/x) dx + ∫ (−1/(x−1)) dx = −ln|x| − ln|x−1| = −ln| x(x−1) |

(cada integral es de tabla: ∫ −1/x dx = −ln|x|, y para el otro término, con el patrón ∫ f'/f, ∫ −1/(x−1) dx = −ln|x−1|).

Entonces, por la fórmula de la homogénea,

    y = K·e^(−∫a dx) = K·e^( ln|x(x−1)| ) = K·x(x−1)

(la exponencial cancela al logaritmo).

**Verificación.** y = K·x(x−1). Derivo con regla del producto: y' = K·[ (1)(x−1) + x(1) ] = K(2x−1). Reemplazo en la original:

    x(x−1)·K(2x−1) + (1−2x)·K·x(x−1) = K·x(x−1)·[ (2x−1) + (1−2x) ] = K·x(x−1)·0 = 0 ✔

## 4.a.3)  y' − (2/x)·y = 0

**Paso 1.** a(x) = −2/x, b = 0.

**Paso 2 — separo:** dy/y = (2/x) dx.

**Paso 3 — integro.**

    ∫ (1/y) dy = ∫ (2/x) dx

- ∫ (1/y) dy = ln|y| (tabla).
- ∫ (2/x) dx = 2·∫ (1/x) dx = 2·ln|x| (saqué la constante 2 y usé la tabla). Y 2·ln|x| = ln(x²).

Queda:

    ln|y| = 2·ln|x| + C = ln(x²) + C

**Paso 4 — despejo.** Exponencial:

    y = K·x²

**Verificación.** y = Kx² → y' = 2Kx (regla de la potencia: (x²)' = 2x, por la constante K). Reemplazo:

    2Kx − (2/x)·(Kx²) = 2Kx − 2Kx = 0 ✔

---

# Parte b) No homogéneas

## 4.b.1)  y' + y·cos x = cos x·sen x

**Paso 1.** Forma estándar: a(x) = cos x, b(x) = cos x·sen x.

**Paso 2 — factor integrante.** Necesito ∫cos x dx, que es sen x (tabla al revés). Entonces

    μ(x) = e^(∫cos x dx) = e^(sen x)

**Paso 3 — derivada de producto.**

    ( y·e^(sen x) )' = e^(sen x)·cos x·sen x

**Paso 4 — integro el lado derecho.** Quiero ∫ e^(sen x)·cos x·sen x dx. **Cambio de variable:** llamo t = sen x, entonces dt = cos x dx. Reemplazo:

    ∫ e^(sen x)·cos x·sen x dx = ∫ e^t·t dt

Ahora uso **integración por partes** (∫u dv = uv − ∫v du) con u = t (se simplifica al derivar) y dv = e^t dt (entonces v = e^t):

    ∫ t·e^t dt = t·e^t − ∫ e^t dt = t·e^t − e^t + C = e^t·(t − 1) + C

Vuelvo a la variable x con t = sen x:

    = e^(sen x)·(sen x − 1) + C

Así que

    y·e^(sen x) = e^(sen x)·(sen x − 1) + C

**Paso 5 — despejo.** Divido todo por e^(sen x):

    y = sen x − 1 + C·e^(−sen x)

**Verificación.** Derivo y = sen x − 1 + C·e^(−sen x):
- (sen x)' = cos x.
- (C·e^(−sen x))' = C·e^(−sen x)·(−cos x) (regla de la cadena).
Así que y' = cos x − C·cos x·e^(−sen x) = cos x·( 1 − C·e^(−sen x) ).

Y y·cos x = cos x·( sen x − 1 + C·e^(−sen x) ).

Sumo: cos x·(1 − C·e^(−sen x)) + cos x·(sen x − 1 + C·e^(−sen x)) = cos x·(1 + sen x − 1) = cos x·sen x ✔

## 4.b.2)  x(x − 1)·y' + (1 − 2x)·y + x² = 0

**Paso 1 — forma estándar.** Paso x² a la derecha y divido por x(x−1):

    y' + [ (1 − 2x)/(x(x−1)) ]·y = −x²/(x(x−1)) = −x/(x−1)

Entonces a(x) = (1 − 2x)/(x(x−1)) = −1/x − 1/(x−1) (ya simplificado en 4.a.2), y b(x) = −x/(x−1).

**Paso 2 — factor integrante.** De 4.a.2, ∫a dx = −ln|x| − ln|x−1|, entonces

    μ = e^(∫a dx) = e^(−ln|x| − ln|x−1|) = 1/( x(x−1) )

**Paso 3 — derivada de producto.**

    ( y·1/(x(x−1)) )' = μ·b = [1/(x(x−1))]·[ −x/(x−1) ] = −x/[ x(x−1)² ] = −1/(x−1)²

**Paso 4 — integro.** Quiero ∫ −1/(x−1)² dx. **Cambio de variable** con t = x − 1, dt = dx:

    ∫ −1/(x−1)² dx = ∫ −t^(−2) dt = −·[ t^(−1)/(−1) ] = t^(−1) = 1/t = 1/(x−1)

(usé la regla de la potencia con n = −2). Entonces

    y/(x(x−1)) = 1/(x−1) + C

**Paso 5 — despejo.** Multiplico por x(x−1):

    y = x(x−1)·[ 1/(x−1) + C ] = x + C·x(x−1)

**Verificación.** y = x + Cx(x−1) → y' = 1 + C(2x−1). Reemplazo en la original:

    x(x−1)[1 + C(2x−1)] + (1−2x)[x + Cx(x−1)] + x²

Parte con C: C·x(x−1)(2x−1) + C·x(x−1)(1−2x) = C·x(x−1)·0 = 0.
Parte sin C: x(x−1) + x − 2x² + x² = x² − x + x − 2x² + x² = 0 ✔

## 4.b.3)  y' − (2/x)·y = x⁴

**Paso 1.** Forma estándar ya está: a(x) = −2/x, b(x) = x⁴.

**Paso 2 — factor integrante.** ∫a dx = ∫(−2/x) dx = −2·ln|x| = ln(x^(−2)). Entonces

    μ = e^(ln(x^(−2))) = x^(−2) = 1/x²

**Paso 3 — derivada de producto.**

    ( y·x^(−2) )' = x^(−2)·x⁴ = x²

**Paso 4 — integro.** ∫ x² dx con la regla de la potencia (n = 2): x³/3. Entonces

    y·x^(−2) = x³/3 + C

**Paso 5 — despejo.** Multiplico por x²:

    y = x²·( x³/3 + C ) = x⁵/3 + C·x²

**Verificación.** y = x⁵/3 + Cx² → y' = 5x⁴/3 + 2Cx (regla de la potencia). Reemplazo:

    y' − (2/x)y = 5x⁴/3 + 2Cx − (2/x)(x⁵/3 + Cx²) = 5x⁴/3 + 2Cx − 2x⁴/3 − 2Cx = 3x⁴/3 = x⁴ ✔

---

## Moraleja del encuentro

- **Homogénea** (b = 0): separable → y = K·e^(−∫a dx).
- **No homogénea**: factor integrante μ = e^(∫a dx); la ecuación se vuelve (μ y)' = μ b.
- **Simplificá a(x)** con fracciones simples antes de calcular μ: muchas veces queda un cociente lindo.
- La no homogénea **contiene** a la homogénea: en 4.b.2 aparece C·x(x−1) (la de 4.a.2) más una particular (x).

> **Siguiente encuentro (4):** ecuaciones de segundo orden homogéneas y valores iniciales (Práctico 1, ej. 5).
