# Encuentro 0b — Derivadas e integrales desde cero

> **Este archivo no es un ejercicio: es el "kit de herramientas".** Si no sabés integrar o derivar, leé esto primero y volvé cada vez que en un ejercicio diga "uso tal regla". No hace falta memorizar todo de una: con entender **de dónde sale cada regla** alcanza para seguir.

---

# Parte 1 — Derivar

## 1.1 ¿Qué es derivar?

Derivar es **medir cómo cambia** una función. La derivada f'(x) te dice **la pendiente de la recta tangente** a la gráfica de f en el punto x. En la práctica, derivar es aplicar un conjunto de **reglas** que se aprenden y se combinan.

Escribo f'(x) o y' o dy/dx (las tres formas significan lo mismo).

## 1.2 Las reglas básicas (con el "por qué" y un ejemplo)

| Función | Derivada | Por qué / ejemplo |
|---|---|---|
| constante c | 0 | una recta horizontal no sube ni baja. (7)' = 0 |
| x | 1 | la recta y = x tiene pendiente 1 en todo punto |
| xⁿ | n·x^(n−1) | la potencia "baja" multiplicando y se le resta 1. (x³)' = 3x² ; (x⁵)' = 5x⁴ |
| √x | 1/(2√x) | es x^(1/2) → (1/2)x^(−1/2) = 1/(2√x) |
| eˣ | eˣ | la exponencial es la función igual a su propia derivada |
| eᵘ (u función de x) | eᵘ·u' | **regla de la cadena** (ver abajo) |
| ln x | 1/x | la derivada del logaritmo es 1 sobre x |
| ln|u| | u'/u | regla de la cadena sobre ln |
| sen x | cos x | — |
| cos x | −sen x | ojo con el menos |
| tan x | 1/(cos x)² | — |
| arctan x | 1/(1 + x²) | muy útil cuando aparece 1/(1+y²) |
| constante·f(x) | constante·f'(x) | las constantes no cambian: (5x³)' = 5·3x² = 15x² |
| f(x) + g(x) | f'(x) + g'(x) | derivada de una suma = suma de derivadas |

## 1.3 Producto y cociente

- **Producto:** (f·g)' = f'·g + f·g'.
  *Ejemplo:* (x·sen x)' = 1·sen x + x·cos x = sen x + x·cos x.
- **Cociente:** (f/g)' = (f'·g − f·g') / g².
  *Ejemplo:* (sen x / x)' = (cos x·x − sen x·1)/x².

## 1.4 Regla de la cadena (la más importante)

Si tengo **una función adentro de otra** (una composición), derivo la de afuera y multiplico por la derivada de la de adentro:

> ( f(u) )' = f'(u) · u'

*Ejemplos:*
- ( e^(3x) )' = e^(3x) · (3x)' = e^(3x)·3 = 3e^(3x).
- ( sen(x²) )' = cos(x²) · (x²)' = cos(x²)·2x.
- ( ln(5x) )' = (1/(5x)) · 5 = 1/x.
- ( (2x+1)³ )' = 3(2x+1)² · 2 = 6(2x+1)².

**Cómo reconocerla:** cada vez que ves algo "metido adentro" de paréntesis, raíz, exponencial, log, seno, etc., usás la cadena.

---

# Parte 2 — Integrar

## 2.1 ¿Qué es integrar?

Integrar es **lo contrario de derivar**. Busco una función F(x) cuya derivada sea la que me dan:

> ∫ f(x) dx = F(x) + C   significa   F'(x) = f(x)

La **C** (constante de integración) está porque si F sirve, F + 5 también (la derivada de una constante es 0). Por eso **toda integral indefinida lleva + C**.

**Truco para verificar:** si integré y me quedó F(x) + C, derivo F y tiene que darme lo de adentro. Si da, está bien.

## 2.2 La tabla de integrales (es la tabla de derivadas "al revés")

| Integral | Resultado | Cómo lo pienso |
|---|---|---|
| ∫ c dx | c·x + C | ¿qué se deriva y da la constante c? → c·x |
| ∫ xⁿ dx | x^(n+1)/(n+1) + C  (n ≠ −1) | **regla de la potencia al revés**: subo 1 al exponente y divido por ese nuevo exponente |
| ∫ (1/x) dx | ln|x| + C | ¿qué se deriva y da 1/x? → ln|x| |
| ∫ eˣ dx | eˣ + C | la exponencial se deriva a sí misma |
| ∫ e^(kx) dx | e^(kx)/k + C | le "corrijo" por la derivada del exponente (1/k) |
| ∫ cos x dx | sen x + C | porque (sen x)' = cos x |
| ∫ sen x dx | −cos x + C | porque (−cos x)' = sen x |
| ∫ dx/(1+x²) | arctan x + C | porque (arctan x)' = 1/(1+x²) |
| ∫ f'(x)/f(x) dx | ln|f(x)| + C | "derivada sobre la función" → logaritmo. ¡Aparece muchísimo! |

**Linealidad:** puedo separar sumas y sacar constantes afuera:

> ∫ ( a·f(x) + b·g(x) ) dx = a·∫f(x) dx + b·∫g(x) dx

## 2.3 Regla de la potencia, con ejemplos (la vas a usar todo el tiempo)

    ∫ xⁿ dx = x^(n+1)/(n+1) + C

- ∫ x dx = ∫ x¹ dx = x²/2 + C  (n = 1 → x²/2).
- ∫ x⁴ dx = x⁵/5 + C.
- ∫ y^(−2) dy = y^(−1)/(−1) + C = −1/y + C  (n = −2).
- ∫ y^(−1/2) dy = y^(1/2)/(1/2) + C = 2√y + C.
- **Ojo:** n = −1 está excluido (daría dividir por 0). Ese caso es justamente ∫(1/x)dx = ln|x|.

## 2.4 El cambio de variable (sustitución) — el método estrella

Se usa cuando adentro de la integral hay una función y "casi" su derivada. La idea:

> Llamo t (o u) a la parte "de adentro", calculo dt = (derivada de esa parte) dx, y reemplazo TODO para que la integral quede en la variable t.

**Pasos:**
1. Elijo t = (la parte que complica, o la de adentro).
2. Calculo dt/dt... mejor dicho: derivo t respecto de la variable y escribo dt = t'·dx (por ejemplo, si t = x², entonces dt = 2x dx).
3. Reemplazo en la integral: todo lo que tenga esa variable lo cambio por t o por dt.
4. Integro en t (más simple).
5. Vuelvo a la variable original.

*Ejemplo guiado:* ∫ 2x·e^(x²) dx.
- t = x² (la parte de adentro). Entonces dt = 2x dx.
- La integral ya tiene "2x dx" → lo reemplazo por dt: queda ∫ e^t dt.
- ∫ e^t dt = e^t + C.
- Vuelvo: e^(x²) + C. **Verifico:** (e^(x²))' = e^(x²)·2x ✔ (coincide con lo de adentro).

*Ejemplo:* ∫ cos x·sen x dx.
- t = sen x → dt = cos x dx.
- ∫ t dt = t²/2 + C.
- Vuelvo: (sen x)²/2 + C = sen²x/2 + C.

## 2.5 Integración por partes (cuando hay producto de dos cosas distintas)

Sale de la regla del producto. La fórmula:

> ∫ u dv = u·v − ∫ v du

**Cuándo:** hay un producto donde una parte "se simplifica" al derivarla (típico: polinomio por exponencial, log, seno). Elegís u = la que conviene derivar, y dv = el resto.

*Ejemplo guiado:* ∫ t·e^t dt.
- u = t → du = dt.
- dv = e^t dt → v = e^t.
- Fórmula: ∫ t e^t dt = t·e^t − ∫ e^t dt = t·e^t − e^t + C = e^t(t − 1) + C.
- **Verifico:** (e^t(t−1))' = e^t(t−1) + e^t·1 = e^t·t ✔.

## 2.6 Fracciones simples (para dividir polinomios)

Si tengo que integrar un cociente de polinomios, a veces el denominador se **factoriza** y el cociente se parte en pedacitos más simples.

*Ejemplo:* ∫ dy/(y² − 1). Como y² − 1 = (y−1)(y+1), escribo

    1/(y² − 1) = A/(y−1) + B/(y+1)

Igualo numeradores: 1 = A(y+1) + B(y−1). Dando valores: con y = 1 → 1 = 2A → A = 1/2; con y = −1 → 1 = −2B → B = −1/2. Entonces

    1/(y² − 1) = 1/2 · [ 1/(y−1) − 1/(y+1) ]

Y ahora cada pedazo se integra con la tabla: ∫1/(y−1) dy = ln|y−1|, ∫1/(y+1) dy = ln|y+1|.

---

# Resumen mental para cualquier ejercicio

- ¿Veo una **suma**? Integro/derivo término a término.
- ¿Veo una **constante multiplicando**? La saco afuera (en integral) o la dejo multiplicando (en derivada).
- ¿Veo **algo adentro de algo** al derivar? → regla de la cadena.
- ¿Veo **derivada sobre función** al integrar? → logaritmo.
- ¿Veo **producto de dos cosas** al integrar? → por partes.
- ¿Veo **cociente de polinomios**? → fracciones simples.
- Después de integrar, **derivo para verificar**.

> Con esto ya podés leer cualquier paso de los encuentros: cada vez que aparezca una integral o una derivada, voy a decir **qué regla uso y por qué**.

---

## Y ahora sí, ¿seguimos?

Volvé al `01_separables.md`, que ya lo reescribí con todos los detalles.
