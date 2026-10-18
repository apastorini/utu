# Encuentro 5 — Hallar las constantes a y b

> **Práctico 1 (Ecuaciones diferenciales), ejercicios 6, 7 y 8.**
> Son ejercicios donde te **dan una solución** y hay que encontrar los coeficientes de la ecuación.
> Todo lo que derive, lo explico; todo lo que resuelva (cuadráticas incluidas), también.

---

## Qué teoría necesito (repaso)

Para una ecuación de segundo orden **y'' + a·y' + b·y = 0**, la ecuación característica es

    r² + a·r + b = 0.

**Idea central de este encuentro:** si me dicen "tal función es solución", la **meto en la ecuación** (calculo sus derivadas, reemplazo) y así salen condiciones sobre a y b.

Y para el ejercicio 6 uso otra idea: **dos ecuaciones lineales tienen una solución no nula en común** si sus polinomios característicos comparten una raíz. ¿Por qué? Porque todas las soluciones se arman con exponenciales e^(r·x) (y, si hay raíz doble, con x·e^(r·x)); para que las dos familias se toquen en algo distinto de la función nula, tienen que compartir una r.

---

## Ejercicio 6 — soluciones en común

> Hallar todos los a reales para que y'' + a·y' − 2y = 0  e  y'' − 2y' + a·y = 0 tengan soluciones en común además de y ≡ 0. Resolver las ecuaciones obtenidas.

**Paso 1 — escribo los dos polinomios característicos.**

- Para y'' + a·y' − 2y = 0:   P₁(r) = r² + a·r − 2.
- Para y'' − 2y' + a·y = 0:   P₂(r) = r² − 2·r + a.

**Paso 2 — busco una raíz común.** Si una r es raíz de los dos, entonces también es raíz de la **diferencia** P₁ − P₂. Calculo esa diferencia:

    P₁(r) − P₂(r) = ( r² + a·r − 2 ) − ( r² − 2·r + a )
                  = a·r − 2 + 2·r − a
                  = (a + 2)·r − (a + 2)
                  = (a + 2)·(r − 1)

**Paso 3 — analizo los dos casos.**

**Caso 1: a ≠ −2.** Entonces puedo dividir por (a + 2) y la diferencia se anula solo si r = 1. O sea, la única raíz común posible es r = 1. La impongo en P₁:

    P₁(1) = 1² + a·1 − 2 = a − 1 = 0  →  a = 1.

Verifico en P₂: P₂(1) = 1² − 2·1 + 1 = 0 ✔. Así que **a = 1** sirve.

**Caso 2: a = −2.** Reemplazo en los polinomios:

    P₁(r) = r² − 2·r − 2,   P₂(r) = r² − 2·r − 2.

¡Son **el mismo** polinomio! Entonces la ecuación es la misma, y **todas** las soluciones son comunes. Así que **a = −2** también sirve.

**Paso 4 — resuelvo las ecuaciones obtenidas.**

**Para a = 1.** Las dos ecuaciones son:

- y'' + y' − 2y = 0: característica r² + r − 2 = (r + 2)(r − 1) = 0 → r = −2, 1. Solución:
    y = A·e^(−2x) + B·e^x.
- y'' − 2y' + y = 0: característica r² − 2r + 1 = (r − 1)² = 0 → r = 1 doble. Solución:
    y = (C + D·x)·e^x.

La solución **común** es la que comparten: y = B·e^x (mirá que e^x aparece en las dos).

**Para a = −2.** La ecuación es y'' − 2y' − 2y = 0. Característica r² − 2r − 2 = 0. Uso la **fórmula general** r = [ −a ± √(a² − 4b) ] / 2 con a = −2, b = −2:

    Δ = (−2)² − 4·1·(−2) = 4 + 8 = 12  →  r = [ 2 ± √12 ] / 2 = [ 2 ± 2√3 ] / 2 = 1 ± √3.

Raíces reales distintas, solución general:

    y = A·e^((1 + √3)x) + B·e^((1 − √3)x).

**Respuesta del ejercicio 6:** a = 1 o a = −2.

---

## Ejercicio 7 — que e^x sea solución

> Hallar a ∈ R para que y(x) = e^x sea solución de y'' + a·y' − 2y = 0. Hallar la solución general. Hallar la solución con y(0) = y'(0) = 1.

**Paso 1 — derivo y = e^x.** La exponencial es su propia derivada (esto es de la tabla):

    y  = e^x
    y' = e^x
    y'' = e^x

**Paso 2 — reemplazo en la ecuación.**

    y'' + a·y' − 2y = e^x + a·e^x − 2·e^x = e^x·( 1 + a − 2 ) = e^x·( a − 1 )

Para que sea 0 para todo x (y e^x nunca es 0), necesito:

    a − 1 = 0  →  a = 1.

**Paso 3 — solución general con a = 1.** La ecuación es y'' + y' − 2y = 0. Característica:

    r² + r − 2 = 0 → busco dos números que multiplicados den −2 y sumados den 1: son 2 y −1
    → (r + 2)(r − 1) = 0 → r = −2, 1.

Raíces reales distintas:

    y = A·e^(−2x) + B·e^x.

**Paso 4 — el problema de valores iniciales.** Con y(0) = 1 y y'(0) = 1. Primero derivo (regla de la cadena: (e^(−2x))' = −2e^(−2x)):

    y'  = −2A·e^(−2x) + B·e^x.

Reemplazo en x = 0 (e⁰ = 1):

    y(0)  = A + B = 1
    y'(0) = −2A + B = 1

Resto la segunda menos la primera: (−2A + B) − (A + B) = 1 − 1 → −3A = 0 → A = 0. Entonces B = 1.

**Paso 5 — solución.**

    y = e^x.

> **Comentario lindo:** la solución que cumple y(0) = y'(0) = 1 es justo la función e^x que nos dieron al principio. Tiene sentido: y = e^x cumple las dos condiciones.

---

## Ejercicio 8 — que e^(2x)·cos x sea solución

> Hallar a y b reales para que y(x) = e^(2x)·cos x sea solución de y'' + a·y' + b·y = 0. Hallar la solución con y(0) = y'(0) = 1.

**Paso 1 — derivo con la regla del producto.** y = e^(2x)·cos x. Es un producto, así que (f·g)' = f'·g + f·g':

    y' = (e^(2x))'·cos x + e^(2x)·(cos x)'
       = 2·e^(2x)·cos x + e^(2x)·(−sen x)       (usé (e^(2x))' = 2e^(2x) y (cos x)' = −sen x)
       = e^(2x)·( 2·cos x − sen x )

**Paso 2 — segunda derivada (otra vez producto).** y' = e^(2x)·(2 cos x − sen x):

    y'' = (e^(2x))'·(2 cos x − sen x) + e^(2x)·(2 cos x − sen x)'
        = 2·e^(2x)·(2 cos x − sen x) + e^(2x)·( −2 sen x − cos x )
        = e^(2x)·[ (4 cos x − 2 sen x) + (−2 sen x − cos x) ]
        = e^(2x)·( 3 cos x − 4 sen x )

(derivé 2 cos x − sen x término a término: (2 cos x)' = −2 sen x, (sen x)' = cos x, con el signo menos queda −cos x).

**Paso 3 — reemplazo en y'' + a·y' + b·y = 0.**

    e^(2x)·(3 cos x − 4 sen x) + a·e^(2x)·(2 cos x − sen x) + b·e^(2x)·cos x = 0

Saco factor común e^(2x) (nunca es 0) y agrupo por cos x y sen x:

    cos x:  3 + 2a + b
    sen x: −4 − a

Para que se anule para todo x, **cada grupo tiene que ser 0**:

    −4 − a = 0        →  a = −4
    3 + 2a + b = 0    →  3 + 2(−4) + b = 0  →  3 − 8 + b = 0  →  b = 5

Entonces **a = −4, b = 5**.

> Verificación del método: la característica es r² − 4r + 5 = 0, cuyas raíces son r = 2 ± i, y eso produce justamente la solución e^(2x)(A cos x + B sen x). ✔

**Paso 4 — solución general.** La ecuación es y'' − 4y' + 5y = 0, con solución general:

    y = e^(2x)·( A·cos x + B·sen x ).

**Paso 5 — el PVI.** Con y(0) = 1 y y'(0) = 1. Evalúo y en 0 (cos 0 = 1, sen 0 = 0, e⁰ = 1):

    y(0) = 1·(A·1 + B·0) = A = 1.

Ahora la derivada. Uso la regla del producto:

    y' = 2·e^(2x)·(A cos x + B sen x) + e^(2x)·( −A sen x + B cos x ).

En x = 0:

    y'(0) = 2·1·(A) + 1·(B) = 2A + B = 1.

Con A = 1: 2 + B = 1 → B = −1.

**Paso 6 — solución.**

    y = e^(2x)·( cos x − sen x ).

**Verificación.** y(0) = 1·(1 − 0) = 1 ✔. y'(0) = 2·1 + (−1) = 1 ✔.

---

## Moraleja del encuentro

- "Tal función es solución" → **la meto en la ecuación** y agrupo por funciones linealmente independientes (cos vs sen, o potencias de x); igualo cada grupo a 0.
- "Dos ecuaciones con solución en común" → **raíz común** de los polinomios característicos.
- Cuando agrupás en cos x y sen x, obtenés un **sistema**; resolvelo despacio.

> **Siguiente encuentro (6):** ecuaciones de segundo orden **no homogéneas** con condiciones iniciales (Práctico 1, ej. 9, los ocho incisos).
