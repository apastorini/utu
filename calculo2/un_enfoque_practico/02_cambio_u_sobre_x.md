# Encuentro 2 — El cambio u = y/x

> **Práctico 1 (Ecuaciones diferenciales), ejercicio 3.**
> Sirve para ecuaciones donde el lado derecho depende del **cociente** y/x.
> Como siempre, cada integral va explicada: tené al lado `00b_derivadas_e_integrales.md`.

---

## Qué teoría necesito (repaso)

Hay ecuaciones de primer orden que **no** son separables tal cual, pero tienen una forma especial: el lado derecho depende **solo del cociente y/x**. Se escriben:

> y' = f( y/x )

**¿Cómo las reconozco?** Miro y'. Si todos los términos de arriba y de abajo tienen el **mismo grado** (en x e y juntos), entonces y' es función de y/x. Ejemplos: y' = (x − y)/(x + y) (todo grado 1), o y' = (x² − y²)/(x² + y²) (todo grado 2).

**El método:**

1. Hago el cambio  u = y/x ,  o sea  y = u·x.
2. Derivo y = u·x con la **regla del producto**: y' = u'·x + u·1 = u + x·u'.
3. Reemplazo: u + x·u' = f(u).
4. Despejo u':  x·u' = f(u) − u  →  u' = [f(u) − u] / x.
5. ¡Ahora es separable! Separo y integro:  du / [f(u) − u] = dx / x.
6. Integro, despejo u, y vuelvo a y con y = u·x.

---

## Ejercicio 3.a)  x²·y' + y(y − x) = 0

**Paso 0 — despejar y'.** De x²y' + y² − xy = 0 saco x²y' = xy − y². Divido por x²:

    y' = (xy − y²)/x² = (y/x) − (y/x)²

**Paso 1 — reconocer.** El lado derecho es función de y/x: con u = y/x,

    y' = u − u² = f(u)

Grado 2 arriba y abajo, así que el método aplica.

**Paso 2 — el cambio.** u = y/x, y = u·x, y' = u + x·u'. Reemplazo:

    u + x·u' = u − u²

**Paso 3 — despejar u'.** Resto u de los dos lados:

    x·u' = −u²
    u' = −u²/x

**Paso 4 — separar e integrar.** Mando u² dividiendo:

    du / u² = − dx / x

Integro los dos lados:

    ∫ u^(−2) du = ∫ (−1/x) dx

- **¿Cómo integro ∫ u^(−2) du?** Regla de la potencia con n = −2: nuevo exponente −1, divido por −1:
    ∫ u^(−2) du = u^(−1)/(−1) = −u^(−1) = −1/u.
- **¿Cómo integro ∫ (−1/x) dx?** Saco la constante −1 afuera y uso la tabla (∫ 1/x dx = ln|x|):
    ∫ (−1/x) dx = −ln|x|.

Entonces:

    −1/u = −ln|x| + C

**Paso 5 — despejar u.** Multiplico por −1:

    1/u = ln|x| − C = ln|x| + K      (llamo K = −C)
    u = 1 / (ln|x| + K)

**Paso 6 — volver a y.** Como y = u·x:

    y = x / (ln|x| + K)

**Verificación (usando la forma de u).** De la solución, u = y/x = 1/(ln|x|+K). Quiero ver que x·u' = −u². Derivo u = (ln|x|+K)^(−1) con la **regla de la cadena** (potencia de algo):

    u' = −(ln|x|+K)^(−2) · (ln|x|+K)' = −(ln|x|+K)^(−2) · (1/x) = −1/[ x·(ln|x|+K)² ]

Entonces x·u' = −1/(ln|x|+K)² = −u² ✔

> **Comentario.** El caso u = 0 (o sea y = 0) resuelve la ecuación, pero lo perdí al dividir por u². La función y ≡ 0 también es solución (0 + 0 − 0 = 0) ✔.

---

## Ejercicio 3.b)  (x + y)·y' = x − y

**Paso 0 — despejar y'.**

    y' = (x − y)/(x + y)

**Paso 1 — reconocer.** Divido arriba y abajo por x:

    y' = [1 − (y/x)] / [1 + (y/x)] = (1 − u)/(1 + u) = f(u)

Todo de grado 1, aplica el cambio.

**Paso 2 — el cambio.** u = y/x, y' = u + x·u':

    u + x·u' = (1 − u)/(1 + u)

**Paso 3 — despejar u'.** Resto u:

    x·u' = (1 − u)/(1 + u) − u

Pongo todo con denominador común (1 + u):

    x·u' = [ (1 − u) − u(1 + u) ] / (1 + u)
         = [ 1 − u − u − u² ] / (1 + u)
         = (1 − 2u − u²) / (1 + u)

**Paso 4 — separar e integrar.**

    (1 + u) / (1 − 2u − u²) · du = dx / x

- **¿Cómo integro ∫ (1+u)/(1 − 2u − u²) du?** Es de la forma "algo sobre una función". Me fijo si el numerador es **casi la derivada del denominador**. Derivo el denominador con la regla de la cadena (es un polinomio, así que término a término):
    (1 − 2u − u²)' = 0 − 2 − 2u = −2(1 + u).
  Es decir (1 + u) = (−1/2)·(−2 − 2u). Entonces mi integral es (−1/2) por "derivada del denominador sobre el denominador", que da logaritmo (patrón ∫ f'/f = ln|f| del repaso):
    ∫ (1+u)/(1 − 2u − u²) du = −1/2·ln|1 − 2u − u²|.
- **¿Cómo integro ∫ dx/x?** Tabla: = ln|x|.

Igualo:

    −1/2·ln|1 − 2u − u²| = ln|x| + C

**Paso 5 — simplificar.** Multiplico por −2:

    ln|1 − 2u − u²| = −2·ln|x| + K

Uso −2·ln|x| = ln(x^(−2)) = ln(1/x²), y aplico exponencial:

    1 − 2u − u² = A / x²

**Paso 6 — volver a y.** Reemplazo u = y/x:

    1 − 2(y/x) − (y/x)² = A/x²

Multiplico todo por x²:

    x² − 2xy − y² = A

**Comentario.** Acá la solución queda **implícita** (no se despeja linda). Eso es una respuesta válida y completa.

---

## Moraleja del encuentro

- El cambio u = y/x se usa cuando y' depende **solo de y/x**: revisá que numerador y denominador tengan **el mismo grado**.
- No te olvides de reemplazar y' por (u + x·u') — es el paso que más se omite.
- Al integrar, buscá el patrón "derivada del denominador sobre el denominador" → logaritmo.
- Si no se despeja, **dejá la solución implícita**.

> **Siguiente encuentro (3):** ecuaciones lineales de primer orden (Práctico 1, ej. 4).
