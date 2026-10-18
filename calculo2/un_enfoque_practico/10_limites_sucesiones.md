# Encuentro 10 — Límites de sucesiones

> **Práctico 2 (Sucesiones), ejercicio 3, incisos a) a g).**
> Acá hay que aplicar las reglas del repaso: sándwich, racionalización, operaciones con límites y comparación de órdenes. Cada paso está explicado.

---

## Qué teoría necesito (repaso rápido)

Las herramientas que voy a usar todo el rato:

1. **Operaciones:** si a_n → A y b_n → B, entonces a_n + b_n → A + B, a_n·b_n → A·B, a_n/b_n → A/B (B ≠ 0).
2. **Sándwich (encaje):** si −|m_n| ≤ a_n ≤ |m_n| y m_n → 0, entonces a_n → 0. Clásico: usar 1/n y −1/n.
3. **Producto de "algo que va a 0" por "algo acotado" → 0.**
4. **Racionalización:** si tengo √( ) − √( ), multiplico y divido por la conmuta.
5. **Dividir por el término dominante:** en cocientes de polinomios/exponenciales, divido arriba y abajo por lo que domina.
6. **Límites de memoria:** 1/n^p → 0 (p>0); x^n → 0 si |x|<1; a^(1/n) → 1 (a>0); n^α/e^n → 0.

---

## 3.a)  a_n = cos(n)/n

**Razonamiento.** No sé a qué tiende cos(n) (oscila sin patrón), pero **sé que está acotado**:

    −1 ≤ cos(n) ≤ 1   para todo n.

Divido por n (n > 0):

    −1/n ≤ cos(n)/n ≤ 1/n.

Los dos extremos tienden a 0 (1/n → 0 y −1/n → 0). Por el **teorema del sándwich**, el del medio también:

> límite(n→∞) cos(n)/n = 0.

---

## 3.b)  a_n = √(n + 1) − √n

**Razonamiento.** Es ∞ − ∞, un caso indeterminado. El truco es **racionalizar**: multiplico y divido por la **conmuta** √(n+1) + √n.

    a_n = [√(n+1) − √n] · [√(n+1) + √n] / [√(n+1) + √n]

**Arriba** uso la fórmula (a − b)(a + b) = a² − b²:

    [√(n+1)]² − [√n]² = (n + 1) − n = 1.

Entonces:

    a_n = 1 / [ √(n+1) + √n ].

El denominador crece sin límite (≥ √n + √n = 2√n), así que el cociente tiende a 0:

> límite(n→∞) √(n+1) − √n = 0.

---

## 3.c)  a_n = (2n − 5) / (n + 3 − 5^(1/n))

**Razonamiento.** Arriba domina 2n. Abajo, el término "5^(1/n)" tiende a 1 (límite notable: a^(1/n) → 1 para a > 0, y acá a = 5). Así que abajo se comporta como n + 3 − 1 = n. Espero 2.

**Paso 1 — divido arriba y abajo por n** (que es lo que domina).

    a_n = (2 − 5/n) / ( 1 + 3/n − 5^(1/n)/n ).

**Paso 2 — estudio cada pedazo.**
- 5/n → 0 y 3/n → 0.
- **5^(1/n) → 1** (límite notable). Además 5^(1/n) está acotada: para n ≥ 1 vale 1 ≤ 5^(1/n) ≤ 5. Por eso 5^(1/n)/n → 0 (un acotado dividido por n → 0).
- **2 − 5/n → 2.**

**Paso 3 — opero.**

    límite = 2 / (1 + 0 − 0) = 2/1 = 2.

> límite(n→∞) a_n = 2.

---

## 3.d)  a_n = n^p / (α^n + β^n),  con α, β > 0

Acá el límite **depende de los casos**. Llamo m = max(α, β), que es "la base más grande".

**Caso 1: m > 1 (la base mayor a 1).**

Como α ≤ m y β ≤ m, resulta α^n + β^n ≥ m^n (uno de los dos términos es exactamente m^n). Entonces

    0 ≤ n^p/(α^n + β^n) ≤ n^p/m^n.

Y n^p/m^n → 0 para m > 1 (la exponencial domina a cualquier potencia). Por sándwich:

> a_n → 0.

**Caso 2: m < 1 (ambas bases menores a 1).**

Entonces α^n + β^n ≤ 2·m^n, así que

    a_n ≥ n^p / (2·m^n) = (1/2)·n^p·(1/m)^n.

Y (1/m) > 1, así que (1/m)^n → ∞ y domina a n^p (cualquier potencia, aunque sea negativa). El cociente se va a infinito:

> a_n → +∞.

**Caso 3: m = 1 (al menos una base vale exactamente 1).**

Entonces el denominador tiende a un número positivo finito (1 si una de las bases es 1, 2 si las dos valen 1). Es decir, el denominador "se comporta" como la constante c = 1 o c = 2. Entonces a_n se comporta como n^p / c:

- si p > 0: **a_n → +∞**.
- si p = 0: **a_n → 1/c** (o sea 1 si solo una base vale 1, o 1/2 si las dos valen 1).
- si p < 0: **a_n → 0** (porque n^p = n^|p| → 0).

> **Resumen:** con m = max(α, β): si m > 1 da 0; si m < 1 da +∞; si m = 1 da +∞, 1/c o 0 según p > 0, p = 0, p < 0.

---

## 3.e)  a_n = sen(1/n) · cos(n)

**Razonamiento.** Es un producto: por un lado sen(1/n), que **tiende a 0** (porque 1/n → 0 y sen(0) = 0), y por otro cos(n), que **no tiene límite pero está acotado** (−1 ≤ cos n ≤ 1). Regla: **0 × acotado = 0**.

**Paso 1 — acoto.**

    |sen(1/n)·cos(n)| ≤ |sen(1/n)| · 1 = |sen(1/n)|.

**Paso 2 — veo que va a 0.** Como 1/n → 0 y sen es continua en 0 (sen(0) = 0), entonces sen(1/n) → 0. Por tanto, por sándwich:

> límite(n→∞) sen(1/n)·cos(n) = 0.

---

## 3.f)  a_n = n^α / e^n,  con α ∈ R

**Razonamiento:** la exponencial crece **más rápido** que cualquier potencia, así que da 0.

**Paso 1 — divido por n^α** para aislar la exponencial (sí, el caso es simple pero quiero mostrarte el método):

    a_n = 1 / [ e^n / n^α ].

**Paso 2 — veo que e^n/n^α → ∞.** Si α ≤ 0 es claro (n^α no crece o decrece). Si α > 0, uso el **prueba del cociente**: llamo b_n = e^n/n^α y calculo

    b_(n+1)/b_n = e^(n+1)/n^α · n^α/(e^n)·... 

mejor dicho: b_(n+1)/b_n = [e^(n+1)/(n+1)^α]·[n^α/e^n] = e·[ n/(n+1) ]^α = e·(1 + 1/n)^(−α) → e·1 = e > 1.

Si el cociente tiende a un número mayor que 1, la sucesión crece y **tiende a ∞**. Entonces a_n = 1/b_n → 0.

> límite(n→∞) n^α/e^n = 0.

---

## 3.g)  a_n = (3^n + (−2)^n) / (3^(n+1) + (−2)^(n+1))

**Razonamiento.** Lo que domina arriba y abajo es 3^n (porque 3 > 2). **Divido todo por 3^n:**

    a_n = [ 1 + ((−2)/3)^n ] / [ 3 + (−2)·((−2)/3)^n ].

**¿Por qué sale así?**
- 3^n/3^n = 1 y (−2)^n/3^n = (−2/3)^n.
- En el denominador: 3^(n+1)/3^n = 3, y (−2)^(n+1)/3^n = (−2)·(−2)^n/3^n = (−2)·(−2/3)^n.

**Ahora tomo límites.** Como |−2/3| < 1, la potencia (−2/3)^n → 0. Entonces:

    límite = (1 + 0)/(3 + 0) = 1/3.

> límite(n→∞) a_n = 1/3.

---

## Moraleja del encuentro

- **Tierra adentro, no lo mires:** a veces no sabés a qué tiende una parte, pero si está **acotada** y la otra va a 0, el producto da 0 (3.a, 3.e).
- **Racionalizá** cuando tengas diferencias de raíces (3.b).
- **Dividí por el término dominante**: potencia sobre potencia (comparar coeficientes), o exponencial sobre exponencial (comparar bases) (3.c, 3.g).
- **Compara órdenes:** exponencial >> potencia >> logaritmo. Esa jerarquía resuelve 3.f y 3.d.

> **Siguiente encuentro (11):** subsucesiones, límites de subsucesiones y **puntos de aglomeración** (Práctico 2, ej. 4 y 5).
