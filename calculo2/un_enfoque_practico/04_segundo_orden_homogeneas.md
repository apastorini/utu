# Encuentro 4 — Ecuaciones de segundo orden homogéneas

> **Práctico 1 (Ecuaciones diferenciales), ejercicio 5:**
> a) solución general (1–4) y b) problemas de valores iniciales (1–4).
> Vamos a resolver la cuadrática y a **derivar paso a paso** en cada verificación.

---

## Qué teoría necesito (repaso)

Una ecuación **lineal de segundo orden con coeficientes constantes** y **homogénea**:

> y'' + a·y' + b·y = 0      (a, b números reales)

**El método (polinomio característico):**

1. Propongo soluciones del tipo y = e^(r·x).
2. Derivo (regla de la cadena, y recuerdo que la derivada de e^(rx) es r·e^(rx)):
    y' = r·e^(r·x),   y'' = r²·e^(r·x).
3. Reemplazo y saco factor común e^(r·x) (que nunca es 0):
    e^(r·x)·( r² + a·r + b ) = 0  →  **r² + a·r + b = 0** (ecuación característica).
4. Resuelvo la cuadrática. La fórmula general es:
    r = [ −a ± √( a² − 4b ) ] / 2.
   El **discriminante** es Δ = a² − 4b, y dice el tipo de solución:

| Δ | Raíces | Solución general |
|---|---|---|
| Δ > 0 | r₁, r₂ reales y distintas | y = A·e^(r₁x) + B·e^(r₂x) |
| Δ = 0 | r raíz doble | y = (A + B·x)·e^(r·x) |
| Δ < 0 | r = p ± q·i | y = e^(p·x)·(A·cos(q·x) + B·sen(q·x)) |

> Recordá que i = √(−1), así que √(−4) = 2i, √(−1) = i, etc. En el caso Δ < 0, p = −a/2 y q = √(4b − a²)/2.

**Datos iniciales (PVI):** si me dan y(x₀) y y'(x₀), reemplazo en la solución general y en **su derivada**, y armo un sistema de dos ecuaciones para hallar A y B.

---

# Parte a) Solución general

## 5.a.1)  y'' − 5y' + 6y = 0

**Paso 1.** Característica: r² − 5r + 6 = 0.

**Paso 2 — resuelvo.** Busco dos números que multiplicados den 6 y sumados den 5: son 2 y 3. Entonces

    (r − 2)(r − 3) = 0  →  r₁ = 2, r₂ = 3.

**Paso 3.** Raíces reales distintas:

    y = A·e^(2x) + B·e^(3x)

**Verificación.** y = A e^(2x) + B e^(3x). Derivo (regla de la cadena: (e^(2x))' = 2e^(2x), (e^(3x))' = 3e^(3x)):

    y'  = 2A e^(2x) + 3B e^(3x)
    y'' = 4A e^(2x) + 9B e^(3x)

Reemplazo: y'' − 5y' + 6y = A e^(2x)(4 − 10 + 6) + B e^(3x)(9 − 15 + 6) = A e^(2x)·0 + B e^(3x)·0 = 0 ✔

## 5.a.2)  y'' + y' = 0

**Paso 1.** Característica: r² + r = 0. (Acá a = 1 y b = 0.)

**Paso 2 — resuelvo.** Saco factor común r: r(r + 1) = 0 → r₁ = 0, r₂ = −1.

**Paso 3.** Raíces reales distintas, una es 0 (y e^(0·x) = 1):

    y = A·e^(0·x) + B·e^(−x) = A + B·e^(−x)

**Comentario.** Que aparezca una constante A es esperable: la ecuación no tiene término en y, así que cualquier constante es solución.

## 5.a.3)  y'' + 4y' + 5y = 0

**Paso 1.** Característica: r² + 4r + 5 = 0.

**Paso 2 — discriminante.** Δ = 4² − 4·1·5 = 16 − 20 = −4 < 0. Raíces con la fórmula:

    r = [ −4 ± √(−4) ] / 2 = [ −4 ± 2i ] / 2 = −2 ± i

(cuidado: √(−4) = 2i). Entonces p = −2 y q = 1.

**Paso 3.** Raíces complejas:

    y = e^(−2x)·( A·cos x + B·sen x )

**Comentario.** Es una **oscilación amortiguada**: el coseno y el seno oscilan, y e^(−2x) los apaga.

## 5.a.4)  y'' + 2y' + y = 0

**Paso 1.** Característica: r² + 2r + 1 = 0.

**Paso 2 — resuelvo.** Reconozco el cuadrado de un binomio: r² + 2r + 1 = (r + 1)². Entonces r = −1 **doble** (Δ = 0).

**Paso 3.** Raíz doble:

    y = ( A + B·x )·e^(−x)

> **Ojo:** **no** pongo A·e^(−x) + B·e^(−x) = (A+B)e^(−x), porque eso sería una sola función y perdería una solución. La forma correcta lleva la **x multiplicando**.

---

# Parte b) Problemas de valores iniciales

## 5.b.1)  y'' − 5y' + 6y = 0,  y(1) = e²,  y'(1) = 3e²

**Paso 1 — solución general** (la de 5.a.1) y su derivada:

    y  = A·e^(2x) + B·e^(3x)
    y' = 2A·e^(2x) + 3B·e^(3x)

**Paso 2 — reemplazo en x = 1.** Como e^(2·1) = e² y e^(3·1) = e³:

    A·e² + B·e³ = e²
    2A·e² + 3B·e³ = 3e²

**Paso 3 — divido todo por e²** (así simplifico; en la segunda, e³/e² = e):

    A + B·e = 1
    2A + 3B·e = 3

**Paso 4 — resuelvo el sistema.** De la primera, A = 1 − B·e. Reemplazo en la segunda:

    2(1 − B·e) + 3B·e = 3
    2 − 2B·e + 3B·e = 3
    B·e = 1  →  B = 1/e = e^(−1)

Entonces A = 1 − 1 = 0.

**Paso 5 — solución.**

    y = e^(−1)·e^(3x) = e^(3x − 1)

**Verificación.** y(1) = e^(3−1) = e² ✔. y' = 3e^(3x−1) (regla de la cadena) → y'(1) = 3e² ✔

## 5.b.2)  y'' − 6y' + 5y = 0,  y(0) = 3,  y'(0) = 11

**Paso 1 — característica.** r² − 6r + 5 = 0. Busco dos números que multiplicados den 5 y sumados den −6: son −1 y −5 → (r − 1)(r − 5) = 0 → r = 1, 5. Solución general y derivada:

    y  = A·e^x + B·e^(5x)
    y' = A·e^x + 5B·e^(5x)

**Paso 2 — reemplazo en x = 0** (e⁰ = 1, 5·0 = 0, e⁰ = 1):

    A + B = 3
    A + 5B = 11

**Paso 3 — resto:** la segunda menos la primera → 4B = 8 → B = 2, y entonces A = 1.

**Paso 4 — solución.**

    y = e^x + 2·e^(5x)

**Verificación.** y(0) = 1 + 2 = 3 ✔. y'(0) = 1 + 2·5 = 11 ✔

## 5.b.3)  y'' + 4y' + 5y = 0,  y(0) = 1,  y'(0) = 0

**Paso 1 — solución general** (la de 5.a.3):

    y = e^(−2x)·( A·cos x + B·sen x )

**Paso 2 — derivo con la regla del producto.** Escribo y = (e^(−2x))·(A cos x + B sen x). Entonces

    y' = (e^(−2x))'·(A cos x + B sen x) + e^(−2x)·(A cos x + B sen x)'

- (e^(−2x))' = −2·e^(−2x) (regla de la cadena).
- (A cos x + B sen x)' = A·(−sen x) + B·cos x = −A sen x + B cos x (derivadas de cos y sen).

Junto:

    y' = −2·e^(−2x)·(A cos x + B sen x) + e^(−2x)·( −A sen x + B cos x )

**Paso 3 — reemplazo en x = 0** (cos 0 = 1, sen 0 = 0, e⁰ = 1):

    y(0)  = 1·( A·1 + B·0 ) = A = 1
    y'(0) = −2·( A·1 + B·0 ) + 1·( −A·0 + B·1 ) = B − 2A = 0

De la segunda, B = 2A = 2.

**Paso 4 — solución.**

    y = e^(−2x)·( cos x + 2·sen x )

**Verificación.** y(0) = 1·(1 + 0) = 1 ✔. y'(0) = −2 + 2 = 0 ✔

## 5.b.4)  y'' + 8y' − 9y = 0,  y(1) = 2,  y'(1) = 0

**Paso 1 — característica.** r² + 8r − 9 = 0. Busco dos números que multiplicados den −9 y sumados den 8: son 9 y −1 → (r + 9)(r − 1) = 0 → r = −9, 1. Solución general y derivada:

    y  = A·e^x + B·e^(−9x)
    y' = A·e^x − 9B·e^(−9x)

**Paso 2 — reemplazo en x = 1** (e^(−9·1) = e^(−9)):

    A·e + B·e^(−9) = 2
    A·e − 9B·e^(−9) = 0

**Paso 3 — resuelvo.** De la segunda: A·e = 9B·e^(−9) → A = 9B·e^(−10). Reemplazo en la primera:

    9B·e^(−10)·e + B·e^(−9) = 2
    9B·e^(−9) + B·e^(−9) = 2
    10B·e^(−9) = 2  →  B = 2/(10)·e⁹ = e⁹/5

Entonces A = 9·(e⁹/5)·e^(−10) = 9/(5e).

**Paso 4 — solución.**

    y = 9/(5e)·e^x + e⁹/5·e^(−9x) = (9/5)·e^(x−1) + (1/5)·e^(9−9x)

**Verificación.** y(1) = (9/5)e⁰ + (1/5)e⁰ = 10/5 = 2 ✔. y'(1) = (9/5)e⁰ − (9/5)e⁰ = 0 ✔

---

## Moraleja del encuentro

- Todo se reduce a resolver **r² + a·r + b = 0** y mirar el discriminante (3 casos).
- Δ > 0 → dos exponenciales; Δ = 0 → exponencial por (A + Bx); Δ < 0 → exponencial por (cos, sen).
- En un PVI, **derivá bien** (sobre todo en el caso complejo, con la regla del producto) y armá el sistema.
- Cuando el punto no es x = 0, simplificá dividiendo por la exponencial (como en 5.b.1).

> **Siguiente encuentro (5):** hallar las constantes a y b cuando te dan una solución (Práctico 1, ej. 6, 7 y 8).
