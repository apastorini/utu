# Un enfoque práctico — Cálculo 2 desde los ejercicios

> **Esta carpeta es distinta al resto del curso.** Acá no hay "clases": hay **ejercicios**, y los resolvemos **de a uno, en orden, desde el primero hasta el último**, con toda la teoría que haga falta repetida cada vez.

---

## ¿Qué es esto y para qué sirve?

La carpeta `curso/` está organizada por **temas** (una clase por tema). Está bien para estudiar de corrido, pero cuando te sentás a **hacer un práctico o un examen** te falta lo otro: ver el ejercicio, entender **por qué** se ataca así, y seguir la cuenta hasta el final.

Acá hacemos exactamente eso. El recorrido es:

- **Práctico 1** (Ecuaciones diferenciales)
- **Práctico 2** (Sucesiones)
- **Práctico 3** (Series)
- **Práctico 4** (Integrales impropias)
- **Práctico 5** (Topología en ℝⁿ)
- **Práctico 6** (Funciones, límites y continuidad)
- Después: **parciales y exámenes** de los temas de la segunda parte (diferenciabilidad, extremos, integrales múltiples).

En cada encuentro agarro **uno o dos ejercicios** y hago siempre lo mismo:

1. **El enunciado** (copiado tal cual, con su numeración real).
2. **Qué teoría necesito** — repaso corto y concreto de las definiciones y fórmulas que voy a usar. Aunque ya lo haya explicado en el ejercicio anterior, lo vuelvo a poner.
3. **La resolución paso a paso**, sin saltear cuentas: "Paso 1…, Paso 2…". **Cada vez que hay que derivar o integrar, no lo doy por sabido**: digo qué regla uso y por qué (y si no sabés derivar o integrar, en `00b_derivadas_e_integrales.md` está el repaso desde cero).
4. **La verificación** (cuando se puede, reemplazo y compruebo).
5. **Un comentario** con la moraleja o la trampa.

La idea es que puedas estudiar **con lápiz y papel al lado**, tapando la resolución e intentando primero.

---

## Cómo está numerado

Cada archivo es un **encuentro**. Van en orden:

| Encuentro | Archivo | Qué cubre |
|---|---|---|
| 0 | `00_como_usar.md` | esta guía |
| 0b | `00b_derivadas_e_integrales.md` | **repaso desde cero**: cómo derivar y cómo integrar, con el razonamiento de cada regla |
| 1 | `01_separables.md` | Práctico 1, ej. 1 y 2 (variables separables) |
| 2 | `02_cambio_u_sobre_x.md` | Práctico 1, ej. 3 (cambio u = y/x) |
| 3 | `03_lineales_primer_orden.md` | Práctico 1, ej. 4 (lineales de 1.er orden) |
| 4 | `04_segundo_orden_homogeneas.md` | Práctico 1, ej. 5 (2.º orden homogéneas) |
| 5 | `05_hallar_constantes.md` | Práctico 1, ej. 6, 7 y 8 |
| 6 | `06_segundo_orden_no_homogeneas.md` | Práctico 1, ej. 9 |
| 7 | `07_evaluaciones_practico1.md` | Práctico 1, evaluaciones anteriores |
| 8 | `08_aplicaciones_practico1.md` | Práctico 1, aplicaciones |
| … | … | y así seguimos con los Prácticos 2 a 6 y los exámenes |

*(La tabla se va completando a medida que agregamos encuentros.)*

---

## Notación (todo en texto simple, sin comandos raros)

Para que se lea limpio en cualquier visor:

| Se escribe | Significa |
|---|---|
| y' , y'' | primera y segunda derivada de y |
| x² , x³ , xⁿ | potencias (para exponentes largos uso paréntesis: e^(2x), x^(n−1)) |
| a/b | fracción a sobre b ; con paréntesis si hace falta: (a+b)/c |
| √3 , √(x+1) | raíz cuadrada |
| ∫ f(x) dx | integral indefinida |
| ∫_a^b f(x) dx | integral definida de a hasta b (de a a b) |
| ∫_1^∞ | integral hasta infinito |
| ∑ (de n=1 a ∞) a_n | sumatoria desde n = 1 hasta infinito |
| lim (con x→0) f(x) | límite cuando x tiende a 0 |
| → , ∞ , ≤ , ≥ , ≠ , ≈ | tiende a, infinito, menor o igual, mayor o igual, distinto, aproximadamente |
| α β γ λ θ ρ φ ε δ | letras griegas (alfa, beta, gamma, lambda, theta, rho, fi, épsilon, delta) |
| ∂f/∂x , ∇f | derivada parcial, gradiente |
| ℝ , ℝ² , ℝ³ | reales, plano, espacio |
| A , B , C , K | constantes (uso K cuando la constante es "genérica") |
| { y₁ , y₂ } | conjunto (las llaves **solo** aparecen para conjuntos, nunca como comando) |

> **Importante:** en esta carpeta **no hay ningún comando LaTeX**. Ni `\cdot`, ni `\displaystyle`, ni `$`, ni `\frac`. Toda la matemática está escrita como se dice en voz alta, así que si abrís el archivo en un visor con vista previa o en un editor de texto, se lee igual.

> **Sobre los logaritmos:** cuando aparece ln|y| uso el valor absoluto porque y podría ser negativa. La constante K puede ser **cualquier** real (positivo, negativo o cero).

---

## Una recomendación de uso

- Leé el **enunciado**, tapá el resto y probá.
- Si te trabás, leé **"Qué teoría necesito"** y volvé a intentar.
- Recién ahí mirá la resolución.
- Al final del encuentro, cerrá el archivo y hacé el ejercicio **de nuevo, de memoria**.

¡Vamos!
