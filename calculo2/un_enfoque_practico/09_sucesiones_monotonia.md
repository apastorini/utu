# Encuentro 9 — Sucesiones: monotonía, acotación y convergencia

> **Práctico 2 (Sucesiones), ejercicios 1 y 2.**
> Acá **empieza un tema nuevo**, así que el repaso teórico es largo a propósito. Leelo una vez y después volvé cada vez que lo necesites.

---

## Qué teoría necesito (repaso)

### ¿Qué es una sucesión?

Una **sucesión** es una lista infinita y ordenada de números: a₁, a₂, a₃, … Al número que ocupa el lugar n lo llamo a_n (el **término general**). El índice n recorre los naturales: n = 1, 2, 3, …

### Convergencia (la definición con ε)

Decir que **a_n tiende a L** (o que **el límite es L**), y se escribe límite(n→∞) a_n = L, significa:

> Para **todo** ε > 0 existe un n₀ (que depende de ε) tal que, para **todo** n ≥ n₀, se cumple |a_n − L| < ε.

**Cómo leerlo en castellano:** "a_n está tan cerca de L como yo quiera (más cerca que ε), y se **queda** ahí para todos los n suficientemente grandes". La recta de la izquierda dice "por más chico que elijas el margen ε". La de la derecha dice "a partir de cierto índice, TODOS los términos entran en el margen y no se salen".

- |a_n − L| < ε significa "la distancia entre a_n y L es menor que ε".
- n₀ es "desde qué término empiezo a confiar".

### Monotonía

- **Creciente:** a_(n+1) ≥ a_n para todo n. (cada término es mayor o igual que el anterior)
- **Decreciente:** a_(n+1) ≤ a_n para todo n.
- **Estrictamente** creciente/decreciente si la desigualdad es estricta (con > o <).

**¿Cómo lo estudio?** Dos caminos:
1. **Por la diferencia:** miro el signo de a_(n+1) − a_n. Si es ≤ 0, decreciente; si ≥ 0, creciente.
2. **Por una función:** si a_n = f(n) para una función f(x) derivable, miro el signo de f'(x). Si f'(x) ≤ 0 para x grande, la sucesión es decreciente (al menos a partir de cierto n).

A veces la sucesión **no** es monótona de arranque, pero sí lo es "a partir de cierto n" (eventualmente monótona). Para la convergencia eso alcanza.

### Acotación

- **Acotada superiormente:** existe un número M con a_n ≤ M para todo n.
- **Acotada inferiormente:** existe m con a_n ≥ m para todo n.
- **Acotada:** está acotada arriba **y** abajo; equivalentemente, existe K con |a_n| ≤ K para todo n.

### EL teorema clave de este práctico

> **Si una sucesión es monótona (creciente o decreciente) y acotada, entonces converge.**

Es la herramienta más importante del tema. Fijate que **no** dice a qué converge: eso hay que averiguarlo aparte (por ejemplo, resolviendo una ecuación). Pero garantiza que el límite existe.

### Cómo se calculan límites (reglas de operaciones)

Si a_n → A y b_n → B (finitos), entonces:

- a_n + b_n → A + B
- a_n · b_n → A · B
- a_n / b_n → A / B (si B ≠ 0)
- k·a_n → k·A

Y dos herramientas enormes:

- **Teorema del sándwich (encaje):** si m_n ≤ a_n ≤ M_n y tanto m_n como M_n tienden a L, entonces a_n → L.
- **Producto de algo que tiende a 0 por algo acotado** → 0. (Si a_n → 0 y b_n está acotada, entonces a_n·b_n → 0.)

### Límites "de memoria" (notables)

- 1/n^p → 0 para p > 0.
- x^n → 0 si |x| < 1.
- **n^α / e^n → 0** para cualquier α real (la exponencial le gana a cualquier potencia).
- a^(1/n) → 1 para a > 0 (por ejemplo, 5^(1/n) → 1).
- n^(1/n) → 1.
- (1 + 1/n)^n → e.

### Subsucesiones (lo vamos a usar en el encuentro 11)

Una **subsucesión** se arma eligiendo infinitos términos de la sucesión, respetando el orden: por ejemplo, los de índice par (a_2, a_4, a_6, …) o los de índice impar. Dato útil:

> Si a_n → L, entonces **toda** subsucesión también tiende a L.

(Al revés no vale: puede haber subsucesiones convergentes sin que toda la sucesión converja.)

---

## Ejercicio 1 — monotonía, acotación y convergencia

> Estudiar monotonía, acotación y convergencia de a_n, donde:
> a) a_n = 1 + 1/n   b) a_n = 1 + (−1)^n/n   c) a_n = (n + 1)/n   d) a_n = n/√(n² + 1)   e) a_n = n²/2^n

### 1.a)  a_n = 1 + 1/n

**Monotonía (por la diferencia).**

    a_(n+1) − a_n = (1 + 1/(n+1)) − (1 + 1/n) = 1/(n+1) − 1/n.

Como n+1 > n, resulta 1/(n+1) < 1/n, así que la diferencia es **negativa**: **decreciente**.

**Acotación.** a_n es 1 más algo positivo, así que a_n > 1 (acotada inferiormente por 1). Y como 1/n ≤ 1, resulta a_n ≤ 2 (acotada superiormente por 2). Entonces 1 < a_n ≤ 2.

**Convergencia.** Es decreciente y acotada (inferiormente), así que **converge**. El límite: 1/n → 0, entonces

    límite(n→∞) a_n = 1 + 0 = 1.

### 1.b)  a_n = 1 + (−1)^n/n

**Monotonía.** Acá el signo del término (−1)^n/n va saltando: para n par es +1/n y para n impar es −1/n. Calculo los primeros:

    a₁ = 1 − 1 = 0,  a₂ = 1 + 1/2 = 1,5,  a₃ = 1 − 1/3 ≈ 0,67,  a₄ = 1 + 1/4 = 1,25, ...

Sube y baja. Por lo tanto **no es monótona** (ni creciente ni decreciente).

**Acotación.** El término (−1)^n/n está siempre entre −1 y 1 (de hecho entre −1/3 y 1/2 para n grande), así que 0 ≤ a_n ≤ 1,5. Está **acotada**.

**Convergencia.** Aunque no es monótona, el "ruido" (−1)^n/n → 0 (es un término acotado —(−1)^n— por algo que tiende a 0). Entonces

    límite(n→∞) a_n = 1 + 0 = 1.

> **Moraleja:** no monótona no significa no convergente. Acá converge igual.

### 1.c)  a_n = (n + 1)/n

**Paso 1 — simplifico.** (n+1)/n = 1 + 1/n. ¡Es la misma sucesión que 1.a! Así que es **decreciente**, **acotada** (1 < a_n ≤ 2) y **converge a 1**.

(Verificación por diferencia: a_(n+1) − a_n = (n+2)/(n+1) − (n+1)/n = [n(n+2) − (n+1)²]/[n(n+1)] = [n²+2n − n²−2n−1]/[...] = −1/[n(n+1)] < 0 → decreciente.)

### 1.d)  a_n = n/√(n² + 1)

**Monotonía (uso la función).** Tomo f(x) = x/√(x² + 1) y derivo. La escribo como f(x) = x·(x² + 1)^(−1/2) y uso la **regla del producto**:

    f'(x) = 1·(x² + 1)^(−1/2) + x·(−1/2)(x² + 1)^(−3/2)·(2x).

El segundo término viene de la **regla de la cadena**: la derivada de (x² + 1)^(−1/2) es (−1/2)(x² + 1)^(−3/2)·2x. Junto:

    f'(x) = (x² + 1)^(−1/2) − x²(x² + 1)^(−3/2)
          = (x² + 1)^(−3/2)·[ (x² + 1) − x² ]
          = (x² + 1)^(−3/2)·1
          = 1/(x² + 1)^(3/2) > 0.

Como f'(x) > 0, f es creciente, así que a_n = f(n) es **creciente**.

**Acotación.** a_n > 0 y además a_n = n/√(n²+1) < n/√(n²) = n/n = 1. Y el menor es a₁ = 1/√2. Entonces 1/√2 ≤ a_n < 1. **Acotada.**

**Convergencia.** Creciente y acotada ⇒ converge. Límite: divido numerador y denominador por n:

    a_n = n/√(n²+1) = 1/√(1 + 1/n²)  →  1/√(1 + 0) = 1.

Así que **converge a 1**.

### 1.e)  a_n = n²/2^n

**Monotonía (por el cociente, que es más cómodo acá).** Para sucesiones con potencias y factoriales conviene mirar a_(n+1)/a_n:

    a_(n+1)/a_n = [ (n+1)²/2^(n+1) ] / [ n²/2^n ] = (n+1)²/2^(n+1) · 2^n/n² = (n+1)²/(2·n²).

La sucesión **crece** si ese cociente es > 1, y **decrece** si es < 1. Veo cuándo es < 1:

    (n+1)²/(2n²) < 1  ⟺  (n+1)² < 2n²  ⟺  n² + 2n + 1 < 2n²  ⟺  n² − 2n − 1 > 0.

Resuelvo n² − 2n − 1 = 0: n = [2 ± √(4+4)]/2 = 1 ± √2 ≈ 2,41. Como n ≥ 3 > 2,41, la desigualdad vale para **n ≥ 3**. Así que:

- n = 1, 2: sube (a₁ = 0,5; a₂ = 1).
- **n ≥ 3: decrece.**

Entonces **no es monótona**, pero es **decreciente a partir de n = 3** (eventualmente decreciente).

**Acotación.** Todos los términos son positivos (acotada inferiormente por 0), y el mayor es a₃ = 9/8 = 1,125, así que a_n ≤ 9/8. **Acotada.**

**Convergencia.** Eventualmente decreciente y acotada inferiormente ⇒ converge. El límite: la exponencial 2^n le gana a n², así que

    límite(n→∞) n²/2^n = 0.

(Cuidado: recordá que es la exponencial con base mayor que 1 la que domina; por eso da 0.)

---

## Ejercicio 2 — encontrar n₀ para cada ε

> Las sucesiones convergen a L. Para ε = 1; 0,1; 0,01, hallar el **primer** n₀ tal que ∀n ≥ n₀ se cumpla |a_n − L| < ε.
> a) a_n = 1/n   b) a_n = n/(n+1)   c) a_n = (−1)^n/n   d) a_n = 1/n!   e) a_n = 2n/(n³ + 1)

**La idea:** planteo la desigualdad |a_n − L| < ε, la resuelvo para n, y busco el **menor natural** a partir del cual se cumple. Conviene "despejar n".

### 2.a)  a_n = 1/n,  L = 0

    |1/n − 0| = 1/n < ε  ⟺  n > 1/ε.

El menor entero que cumple n > 1/ε es n₀ = parte entera de 1/ε, más 1.

- ε = 1: n > 1 → **n₀ = 2**.
- ε = 0,1: n > 10 → **n₀ = 11**.
- ε = 0,01: n > 100 → **n₀ = 101**.

### 2.b)  a_n = n/(n+1),  L = 1

Primero simplifico la distancia:

    |n/(n+1) − 1| = | (n − (n+1))/(n+1) | = | −1/(n+1) | = 1/(n+1).

Entonces la condición es:

    1/(n+1) < ε  ⟺  n + 1 > 1/ε  ⟺  n > 1/ε − 1.

- ε = 1: n > 0 → **n₀ = 1** (vale para todo n ≥ 1).
- ε = 0,1: n > 10 − 1 = 9 → **n₀ = 10**.
- ε = 0,01: n > 100 − 1 = 99 → **n₀ = 100**.

> Chequeo con ε = 0,01: a₁₀₀ = 100/101, y |a₁₀₀ − 1| = 1/101 ≈ 0,0099 < 0,01 ✔. Y con n = 99: 1/100 = 0,01, que **no** es < 0,01. Bien, n₀ = 100.

### 2.c)  a_n = (−1)^n/n,  L = 0

    |(−1)^n/n − 0| = 1/n < ε  ⟺  n > 1/ε.

Igual que 2.a:

- ε = 1: **n₀ = 2**.
- ε = 0,1: **n₀ = 11**.
- ε = 0,01: **n₀ = 101**.

### 2.d)  a_n = 1/n!,  L = 0

Acá no se despeja tan fácil (n! crece muy rápido); pruebo valores.

    |1/n! − 0| = 1/n! < ε  ⟺  n! > 1/ε.

- ε = 1: n! > 1. Como 1! = 1 (no es > 1) y 2! = 2 > 1 → **n₀ = 2**.
- ε = 0,1: n! > 10. 3! = 6 < 10, 4! = 24 > 10 → **n₀ = 4**.
- ε = 0,01: n! > 100. 4! = 24 < 100, 5! = 120 > 100 → **n₀ = 5**.

> Chequeo con ε = 0,01: 1/5! = 1/120 ≈ 0,00833 < 0,01 ✔; y 1/4! = 1/24 ≈ 0,0417, no. Correcto.

### 2.e)  a_n = 2n/(n³ + 1),  L = 0

    |2n/(n³ + 1)| < ε  ⟺  2n < ε·(n³ + 1).

Conviene tantear (a mano) porque es una cúbica.

- ε = 1: 2n < n³ + 1 ⟺ n³ − 2n + 1 > 0. Con n = 1: 1 − 2 + 1 = 0 (no). Con n = 2: 8 − 4 + 1 = 5 > 0 → **n₀ = 2**.
- ε = 0,1: 20n < n³ + 1 ⟺ n³ − 20n + 1 > 0. Con n = 4: 64 − 80 + 1 = −15 (no). Con n = 5: 125 − 100 + 1 = 26 > 0 → **n₀ = 5**.
- ε = 0,01: 200n < n³ + 1 ⟺ n³ − 200n + 1 > 0. Con n = 14: 2744 − 2800 + 1 = −55 (no). Con n = 15: 3375 − 3000 + 1 = 376 > 0 → **n₀ = 15**.

> Chequeo con ε = 0,01: a₁₄ = 28/2745 ≈ 0,0102 > 0,01; a₁₅ = 30/3376 ≈ 0,00889 < 0,01 ✔.

---

## Moraleja del encuentro

- Para la **monotonía**: la diferencia (a_(n+1) − a_n) si es simple; el cociente o la derivada si hay potencias/factoriales.
- **El teorema:** monótona + acotada ⇒ converge. Pero el valor del límite se calcula aparte.
- "No monótona" no implica "no converge" (mirá 1.b).
- Para el **n₀**: planteá |a_n − L| < ε, despejá n (o tanteá si es incómodo), y tomá el menor entero que cumple.

> **Siguiente encuentro (10):** calcular límites de sucesiones (Práctico 2, ej. 3), con sándwich, racionalización y comparación de órdenes.
