# Clase 7 — Nyquist, Shannon y la capa física + Simulacro 1

**Bloque:** A (Fundamentos) · **Semana:** 3 · **Duración estimada:** 120 min
**Correlativa:** Clase 6 (taller de retardos) · **Sigue con:** Clase 8 (HTTP: la web como aplicación de la capa de aplicación)
**Material de referencia:** Tanenbaum cap. 1 §1.1 y §1.6 · Exámenes `sirc0608`, `sirc0707`, `sirc0903`

---

## 🎯 Al terminar esta clase vas a poder

1. **Describir** el único encargo de la capa física y explicar **qué no hace**.
2. **Comparar** los cuatro medios en una tabla con ancho de banda, inmunidad al ruido y alcance.
3. **Distinguir** full duplex de half duplex, con la tabla de qué tecnología usa qué modo.
4. **Enunciar** Nyquist con sus **hipótesis** y calcular la capacidad dado `B` y `V`.
5. **Enunciar** Shannon con sus **hipótesis** y calcular la capacidad con el `S/N` **en lineal**, convirtiendo desde dB.
6. **Explicar** cuándo aplica cada teorema y por qué Shannon queda por debajo de Nyquist.
7. **Describir** ASK, FSK, PSK y **QAM**, y calcular los bits por símbolo de una constelación de `M` puntos.
8. **Hacer** el **Simulacro 1** completo: 5 preguntas teóricas y 2 problemas, con cronómetro.

> **Prerequisito del examen:** `2006-08 P1` (5 pts), `2007-07 P1` (10 pts), `2009-02 P3` (5 pts), `2009-03 P5` (6 pts), `2011-03 P5` (10 pts).

---

# PARTE 1 — TEORÍA

## 1.1 La capa física: qué hace y qué NO hace

La capa física es **la más tonta del modelo y por eso la más fácil de recordar**: no
razona, no mira contenido, no decide. Su único encargo es transmitir **bits**:

```
  ┌─────────────────────────────────────────────────────────────────────┐
  │   La capa física TRANSMITE BITS de un nodo al nodo vecino:          │
  │     1  0  1  1  0  0  1  0  1  1  1  0  →  señal en el medio      │
  │   Nada más. No sabe qué hay adentro del paquete.                    │
  └─────────────────────────────────────────────────────────────────────┘
```

**Lo que la capa física NO hace (y esto es lo que se pregunta):** no distingue un bit de
otro (`10110010` y `01001101` son "lo mismo" para ella, y el significado lo pone la capa 2);
no detecta errores (el CRC es de la capa 2); no reenvía ni enruta (el bit que entra por un
puerto sale por el otro, y nada más); no reconoce direcciones; y no reintenta, no comprime ni
cifra.

**Por qué se llama "física":** porque todo lo que hace depende de la física real — la
velocidad con que la señal viaja por el cobre, la atenuación con la distancia, el
electromagnetismo alrededor, la temperatura. Un enlace de 400 Gbps sobre **fibra multimodo**
tiene un alcance de 100 m, y sobre **fibra monomodo** llega a 40 km: la diferencia es
física.

## 1.2 Los cuatro medios, y por qué la fibra ganó

```
  PAR TRENZADO                          FIBRA ÓPTICA
  ╔══╗   ╔══╗   ╔══╗   ╔══╗             ╭────────────╮
  ║  ║╲╱║  ║╲╱║  ║╲╱║  ║  ║             │ ═══ luz ═══│
  ╚══╝ ╲╚═╝ ╱╚═╝ ╱╚═╝ ╱╚═╝             ╰────────────╯
   se ROTA el campo de uno con el del otro:
   se CANCELA el ruido (crosstalk)
```

| | **Par trenzado** (UTP/STP) | **Coaxial** | **Fibra óptica** | **Inalámbrico** (radio / satélite) |
|---|---|---|---|---|
| **Medio** | cobre, pares trenzados | cobre con malla blindada | luz en vidrio de sílice | ondas de radio o infrarrojo |
| **Truco** | el **trenzado** cancela el *crosstalk*; el blindaje (STP) protege del **EMI** | la malla es el retorno y **apantalla** | **inmune al EMI**: la luz no es campo eléctrico | el medio es **aire**, y es compartido |
| **Ancho de banda** | 10 Mbps → 10 Gbps (Cat 6/8) | ~10 Mbps (TV e internet CATV) | **decenas de Gbps a Tbps** | 10 Mbps (Wi-Fi) a Gbps (5G, Wi-Fi 7) |
| **Alcance sin electrónica** | **100 m** | ~500 m | **40 km (monomodo)** a 100 m (multimodo) | km a 36 000 km |
| **Inmune al ruido** | no | no | **SÍ, totalmente** | no |

### ⚠️ El dato del satélite, que es el mejor ejemplo del curso

```
  d = 36 000 km (altura de un geoestacionario)   s = 3 · 10⁸ m/s (va por aire)
  d_prop de ida = 3,6·10⁷ / 3·10⁸ = 0,12 s = 120 ms      RTT = 240 ms

  ⚠️ 120 ms de latencia es IRRECUPERABLE: es geometría, no ingeniería. Por eso el
     satélite SÍ sirve para STREAMING (tolerás 2 s de arranque) y NO para VoIP
     INTERACTIVO (el humano no aguanta más de 150 ms de ida en una conversación).
```

**Por qué es el ejemplo clave:** un enlace satelital puede tener 50 Mbps y aun así ser
**peor** para una videollamada que una fibra de 1 Gbps. El ancho de banda responde a
*"¿cuánta información por segundo?"* y la latencia a *"¿cuánto tarda?"*: preguntas
distintas, con variables distintas (`R` contra `d/s`). Es el núcleo conceptual de la Clase 5
y lo que se pregunta en el Examen 2009-12 P1a.

## 1.3 Full duplex vs. half duplex (Examen 2009-03 P5)

**Definiciones, con las palabras de la solución oficial:** **full duplex** es que se puede
**transmitir y recibir simultáneamente**; **half duplex** es que se puede transmitir o
recibir, pero **no a la vez**, y se alterna. Es como un teléfono (full duplex: hablás y
escuchás a la vez) contra una radio de baquelita (half duplex: apretás para hablar, soltás
para escuchar).

**La tabla de qué tecnología usa qué modo:**

| Tecnología | Modo | Por qué o con qué matiz |
|---|---|---|
| **Ethernet conmutado** (Fast, Gigabit, 10 GigE) | **FULL DUPLEX** | Cada puerto es un enlace punto a punto dedicado: un par para ir y otro para volver. |
| **Ethernet con hub** (coax compartido, 10BASE legacy) | **HALF DUPLEX** | Un único medio compartido: si dos transmiten a la vez, colisión. Necesita CSMA/CD. |
| **Bluetooth** (802.15) | **HALF DUPLEX** (formalmente) | *Time Division Duplex*: el maestro y los esclavos se turnan en ranuras de 625 µs. Con poca rigurosidad se lo llama full duplex, pero **no es simultáneo real**. |
| **Wi-Fi** (802.11) | **HALF DUPLEX siempre** | El medio es el **aire**, inherentemente compartido. En 802.11 **no existe full duplex**. |
| **Fibra y enlaces seriales** | **FULL DUPLEX** | Suele haber un par (TX/RX) separado por dirección. |
| **DSL** | **FULL DUPLEX** (por frecuencias) | Usa bandas distintas para subida y bajada. |

> ⚠️ **La frase clave para el examen:** Ethernet conmutado es **full duplex**; Wi-Fi es
> **siempre half duplex**. Si el enunciado dice "Ethernet (IEEE 802.3)", la respuesta es
> full duplex en los enlaces conmutados modernos, y half duplex en los hubs antiguos.

### ⚠️ Actualización a 2026 — el half-duplex en Ethernet

**Sigue igual:** Ethernet nació half duplex y se hizo full duplex con el switch; Wi-Fi nunca
tuvo full duplex.

**Cambió:**
- **El half-duplex Ethernet es historia por encima de 1 Gb/s.** A 10 GbE y más el
  full-duplex punto a punto es **obligatorio**. Es una decisión de **IEEE 802.3**, no de la
  IETF: **no existe RFC que lo depreque**. ⚠️ **`RFC 8984` es JSCalendar**, no Ethernet.
- **PERO no desapareció del todo:** **IEEE 802.3cg 10BASE-T1S** (un solo par, para redes
  industriales) es **obligatoriamente half-duplex con PLCA**, y el módulo YANG `csma-cd` de
  `802.3cf` está marcado `status deprecated`.

## 1.4 Nyquist — el techo del medio limpio

### El teorema

```
  ┌─────────────────────────────────────────────────────────────────────┐
  │                                                                     │
  │        C = 2 · B · log₂(V)          [bits por segundo, bps]       │
  │                                                                     │
  │   B = ancho de banda del enlace, en HERTZ (Hz)                     │
  │   V = cantidad de niveles de señal (estados posibles por símbolo)   │
  │                                                                     │
  └─────────────────────────────────────────────────────────────────────┘
```

### Las hipótesis del teorema (lo que pregunta el Examen 2006-08 P1)

Según la solución oficial, tres:

```
  1. Canal de comunicaciones de ANCHO DE BANDA LIMITADO B, SIN RUIDO de ningún tipo.
  2. La señal transmitida es una SEÑAL DIGITAL de V NIVELES DISCRETOS.
  3. (implícita) El medio transmite 2 SEÑALES por segundo, una por cada cambio de nivel.
```

### El ejemplo canónico de la cátedra, resuelto

Una línea telefónica clásica: `B = 3100 Hz`, `V = 2` (dos niveles: +1 y −1).
`C = 2 · 3100 · log₂(2) = 6200 bps`. El detalle importante: `log₂(2) = 1`, porque con `V = 2`
cada **símbolo** transporta 1 bit; y con 2 símbolos por segundo salen 2 bits por segundo y
por Hz, que es justamente el `2` del `2·B`.

Si el mismo enlace admite **4 niveles** (`V = 4`): `C = 2 · 3100 · log₂(4) = 12 400 bps`. El
ancho de banda **no cambió** (siguen siendo 3100 Hz): lo que cambió fue la **modulación**, y
ahora cada símbolo lleva 2 bits. **Se dobló la velocidad sin tocar el medio.**

### Por qué el factor 2 (la intuición)

En un medio de ancho de banda `B` se pueden mandar **2 señales por segundo** (una por
cada oscilación o cambio de nivel). Cada una vale `log₂(V)` bits, porque tenés `V` estados
posibles y hacen falta `log₂(V)` bits para distinguirlos (2 estados → 1 bit, 4 → 2 bits,
16 → 4 bits).

```
  2 señales/segundo   ×   log₂(V) bits/señal
  ───────────────────────────────────────────────
       =  2 · log₂(V)   bits por segundo y por Hz

  y multiplicando por los B Hz:   C = 2 · B · log₂(V)
```

## 1.5 La modulación: cómo se mandan los bits por el medio

La capa física convierte bits en **señal**; la **modulación** es ese proceso:

```
  ASK (Amplitude Shift Keying) — modula la AMPLITUD
       bit 0:  ─────┐        ┌───────       Con V niveles:
       bit 1:         └────────┘             V amplitudes por símbolo

  FSK (Frequency Shift Keying) — modula la FRECUENCIA
       bit 0:  ~~~~~   (frecuencia baja)     bit 1:  ∿∿∿∿∿ (alta)

  PSK (Phase Shift Keying) — modula la FASE
       bit 0:  ─────   (fase 0°)              bit 1:  ‾‾‾‾‾ (fase 180°)

  QAM (Quadrature Amplitude Modulation) — combina AMPLITUD y FASE
       constelación de puntos: cada PUNTO = un símbolo distinto
       16-QAM = 16 puntos = 4 bits por símbolo
```

### QAM: la estrella del curso

```
  16-QAM (constelación de 16 puntos):

          I (Eje en cuadratura)
          │
      · · ·┼· · ·      ● ●     ← 4 niveles de amplitud en I
      ──────┼──────────────  Q (Eje en fase)
      · · ·┼· · ·      ● ●
          │

  4 puntos en cada cuadrante × 4 cuadrantes = 16 puntos
  bits por símbolo = log₂(16) = 4

  En un canal de 3100 Hz: C = 2 · 3100 · log₂(16) = 24 800 bps
```

**El punto conceptual:** QAM **exploita los dos indicadores** que Nyquist dice que tenés (la
amplitud **y** la fase). Con `A` niveles de amplitud y `F` fases distintas se consigue una
constelación de `M = A · F` puntos, y cada punto vale `log₂(M)` bits. Por eso las
modulaciones reales de alta velocidad (Wi-Fi 5/6/7, 5G, cable) son todas QAM de orden alto:
256-QAM, 1024-QAM, 4096-QAM.

## 1.6 Shannon — el techo del medio ruidoso

### El teorema

```
  ┌─────────────────────────────────────────────────────────────────────┐
  │        C = B · log₂(1 + S/N)          [bits por segundo, bps]      │
  │   B  = ancho de banda del enlace, en HERTZ (Hz)                     │
  │   S  = potencia de la señal;  N = potencia del ruido                │
  │   S/N = relación señal-ruido, EN LINEAL (¡no en dB!)                │
  │                                                                     │
  │   Es la CAPACIDAD del canal: el máximo de bits que pasan           │
  │   LIMPIAMENTE, con corrección de errores tolerable.                 │
  └─────────────────────────────────────────────────────────────────────┘
```

### ⚠️ LA CONVERSIÓN DE dB A LINEAL (el paso que más se olvida)

```
  ┌─────────────────────────────────────────────────────────────────────┐
  │        S/N_lineal = 10 ^ (S/N_dB / 10)                              │
  └─────────────────────────────────────────────────────────────────────┘
```

| S/N (dB) | S/N (lineal) | `log₂(1 + S/N)` | Con `B = 3100 Hz` |
|---|---|---|---|
| 0 dB | 1 | log₂(2) = 1 | 3100 bps |
| **20 dB** | **100** | log₂(101) ≈ 6,66 | ≈ 20 600 bps |
| **30 dB** | **1000** | log₂(1001) ≈ 9,97 | ≈ 30 900 bps |
| 40 dB | 10 000 | log₂(10 001) ≈ 13,29 | ≈ 41 200 bps |

**El ejemplo paso a paso (30 dB → lineal):**

```
  S/N = 30 dB   →   S/N_lineal = 10^(30/10) = 10³ = 1000
  C = 3100 · log₂(1 + 1000) = 3100 · log₂(1001) = 3100 · 9,97 ≈ 30 900 bps

  ⚠️ El error clásico es meter 30 (el dB) en vez de 1000 (el lineal):
     da 3100 · log₂(31) ≈ 15 700 bps, LA MITAD.
```

### Las hipótesis del teorema

(1) El canal tiene ancho de banda limitado `B` (Hz). (2) El ruido es **gaussiano** (blanco,
distribución normal) de potencia `N`. (3) Hay una señal de potencia `S`. (4) El límite **no
son los niveles de señal** (`V` no aparece): son el ancho de banda y el ruido. Ésta es la
diferencia clave con Nyquist.

## 1.7 Nyquist y Shannon juntos: cuándo aplica cada uno

```
  ┌─────────────────────────────────────────────────────────────────────┐
  │   NYQUIST  = techo del medio IDEAL (sin ruido)                     │
  │               C_N = 2 · B · log₂(V)                                 │
  │                                                                     │
  │   SHANNON  = techo del medio REAL (con ruido gaussiano)             │
  │               C_S = B · log₂(1 + S/N)                               │
  │                                                                     │
  │   SIEMPRE:  C_S ≤ C_N                                              │
  └─────────────────────────────────────────────────────────────────────┘
```

```
  capacidad (bps)
     │                    ╭───────────  NYQUIST: 2·B·log₂(V)   (medio sin ruido)
     │                  ╱ │
     │    SHANNON    ╱     │  ← SHANNON SIEMPRE DEBAJO DE NYQUIST;
     │   B·log₂(1+S/N)     │    la distancia entre las dos curvas es el RUIDO
     │  ╱                  │
     │╱                    │
     └─────────────────────┼──────────────►  B (Hz)

  Si S/N → ∞ (ruido despreciable), SHANNON → NYQUIST.
```

**¿Cuándo se aplica cada uno?**

| Situación | Teorema | Por qué |
|---|---|---|
| Medio **limpio** (cobre corto, fibra nueva) | **Nyquist** | El ruido es despreciable; el límite es la modulación (`V` niveles). |
| Medio **ruidoso** (línea telefónica, radio, cobre de largo recorrido) | **Shannon** | El ruido es el factor limitante; el límite es el `S/N`. |
| **Diseño de sistema** | **Los dos** | Nyquist da el techo del hardware y Shannon el techo usable; el diseño real queda **por debajo de Shannon**, y **Nyquist nunca se alcanza**. |

**La relación, con números:** con `B = 3100 Hz` y `V = 4`, Nyquist da `12 400 bps`, y el
mismo medio con `S/N = 20 dB` da por Shannon `20 650 bps`. Parece que Shannon **supera** a
Nyquist, pero **no están comparados con el mismo `V`**: para igualarlos haría falta
`2·log₂(V) = log₂(101)`, o sea `V ≈ 10`, y con `V ≈ 10` Nyquist da `≈ 20 600 bps`. **Shannon
da el techo REAL; Nyquist, el IDEAL de un medio limpio con una modulación dada.**

## 1.8 Los tres conceptos juntos, y qué cambió hasta 2026

```
  ┌───────────────┬──────────────────┬──────────────────┬──────────────────┐
  │               │  NYQUIST         │  SHANNON         │  RETARDO         │
  │ Pregunta      │ bits por SEGUNDO │ pasan LIMPIAMENTE│ cuánto tarda     │
  │ Fórmula       │ 2·B·log₂(V)      │ B·log₂(1+S/N)    │ L/R  y  d/s      │
  │ Variable clave│ V (niveles)      │ S/N (calidad)    │ R, d, L          │
  │ Modelo        │ medio SIN ruido  │ medio CON ruido  │ cualquier medio  │
  │ Saturado por  │ los NIVELES      │ el RUIDO         │ distancia o R    │
  └───────────────┴──────────────────┴──────────────────┴──────────────────┘
```

### ⚠️ Actualización a 2026 — qué cambió en la capa física

**Sigue igual — de memoria:** **Nyquist** (`C = 2·B·log₂(V)`, medio sin ruido), **Shannon**
(`C = B·log₂(1+S/N)`, ruido gaussiano, `S/N` en lineal), la conversión
`S/N_lineal = 10^(dB/10)`, las definiciones de full y half duplex, las características de los
cuatro medios, y la modulación (ASK, FSK, PSK, QAM).

**Cambió — y esto es lo que hay que contar en 2026:**
- **La fibra se volvió el medio dominante**: el cobre sigue para el último tramo de acceso
  (unos 100 m), pero **todo el backbone y casi todo el centro de datos** es fibra.
- **El half-duplex Ethernet murió en el backbone**, como se explicó en §1.3.
- **Wi-Fi dejó atrás el CSMA/CD por completo**: hoy es **CSMA/CA**, con **OFDMA** (Wi-Fi
  6/6E), **MU-MIMO** y **MLO**. **Wi-Fi 7** (`IEEE 802.11be-2024`, publicado el 22-jul-2025)
  trae 320 MHz de canal y **4096-QAM**: Nyquist con `V = 4096`, o sea `log₂(4096) = 12`
  bits por símbolo. **Wi-Fi 8** (`802.11bn`, objetivo mayo-2028) se enfoca en confiabilidad.
  Un curso de 2012 sobre `802.11n` está **cuatro generaciones** atrás.

> **Consecuencia para el examen:** los **dos teoremas no cambiaron**: son matemáticas, no
> ingeniería. Lo que cambió son las cifras (4096-QAM en Wi-Fi 7) y el medio dominante
> (fibra). Si el enunciado es de Nyquist o Shannon, la fórmula y las hipótesis van
> **exactamente iguales** que en 2011.

---

# PARTE 2 — PRÁCTICA RESUELTA

## 2.1 Ejercicio 1 — Nyquist con 3100 Hz y 4 niveles

**Datos.** Una línea telefónica de **B = 3100 Hz** con una modulación de **V = 4 niveles**.
**a)** ¿Cuál es la capacidad máxima? **b)** ¿Cuántos bits por símbolo?

```
  a) C = 2 · B · log₂(V) = 2 · 3100 · log₂(4) = 2 · 3100 · 2 = 12 400 bps
  b) bits por símbolo = log₂(V) = log₂(4) = 2 bits
```

*Interpretación:* cada 1/6200 de segundo mando un símbolo, y cada símbolo vale 2 bits:
`C = 6200 símbolos/s × 2 bits = 12 400 bps`.

**Variante:** ¿y con **V = 16** (16-QAM)? `C = 2 · 3100 · log₂(16) = 24 800 bps`. El medio
**no cambió**; lo que cambió fue la **modulación**, y con ella los bits por símbolo (de 2 a
4). Ése es el juego de Nyquist: **multiplicar los niveles es multiplicar la velocidad sin
tocar el cable.**

## 2.2 Ejercicio 2 — Shannon con S/N en dB (la conversión a la vista)

**Datos.** Un enlace de **B = 3100 Hz** con ruido de **S/N = 30 dB**. **a)** Convertí el
S/N a lineal. **b)** ¿Cuál es la capacidad máxima?

```
  a) S/N_dB = 30
     S/N_lineal = 10^(30/10) = 10³ = 1000

  b) C = B · log₂(1 + S/N_lineal) = 3100 · log₂(1 + 1000) = 3100 · log₂(1001)
     log₂(1001): como 2¹⁰ = 1024, está apenas por debajo de 10.
        log₂(1001) = 10 + log₂(1001/1024) = 10 + log₂(0,977) ≈ 10 − 0,034 ≈ 9,97
     C = 3100 · 9,97 ≈ 30 900 bps
```

**Interpretación — la moraleja:**

> Con 30 dB de calidad de señal (una relación señal-ruido de 1000 a 1), la línea
> telefónica clásica **no puede pasar de ~31 kbps**, aunque la modulación sea perfecta.
> Ése es el techo de Shannon: **el ruido, no el cable, es el límite**. Por eso los
> módems de la época llegaban a ~33,6 kbps y ahí paraban: no era el cable ni el módem,
> era Shannon.

### ⚠️ Errores típicos del ejercicio 2

- **Meter 30 (dB) en la fórmula en vez de 1000 (lineal).** Da `3100 · log₂(31) ≈ 15 700 bps`: la mitad. **Este es EL error del ejercicio.**
- **Olvidar el `1 +`:** es `log₂(1 + S/N)`, no `log₂(S/N)`.
- **Usar `10^(dB/20)`:** esa es la fórmula de potencia contra amplitud; el `S/N` en redes es
  siempre **potencia**, así que va con `/10`.

## 2.3 Ejercicio 3 — Teórico máximo contra capacidad real

**Datos.** Un enlace tiene `B = 1 MHz`, `S/N = 40 dB` y se modula con `V = 1024`
(1024-QAM, o sea 10 bits por símbolo). **a)** Nyquist. **b)** Shannon. **c)** ¿Cuál manda?

```
  a) Nyquist:  C_N = 2 · 10⁶ · log₂(1024) = 2 · 10⁶ · 10 = 20 Mbps

  b) Shannon:  S/N = 10^(40/10) = 10 000 (lineal)
               C_S = 10⁶ · log₂(1 + 10 000) = 10⁶ · log₂(10 001) ≈ 10⁶ · 13,29
               C_S ≈ 13,3 Mbps

  c) Mandan los dos: la capacidad real es el MÍNIMO, o sea 13,3 Mbps. Los
     20 Mbps son el techo del transmisor; los 13,3 Mbps, el del medio. En la
     práctica la capacidad real es un 50-70 % de Shannon, por atenuación,
     pérdida de sincronismo y overhead de protocolo.
```

## 2.4 Ejercicio 4 — QAM y bits por símbolo

**Datos.** Una constelación QAM tiene **16 puntos** en un enlace de 3100 Hz.

```
  16-QAM = 4 niveles de amplitud × 4 fases  →  M = A · F = 4 · 4 = 16 puntos
  Cada punto = 1 símbolo, y bits por símbolo = log₂(16) = 4 bits

  C = 2 · 3100 · log₂(16) = 2 · 3100 · 4 = 24 800 bps
```

---

# PARTE 3 — PROBLEMAS DE EXAMEN DE FING

## 3.1 Examen 2006-08, Pregunta 1 (5 puntos) — Nyquist y Shannon con sus hipótesis

> **Fuente:** Examen `sirc0608` — 5 de agosto de 2006, Pregunta 1 (5 puntos).
> **Link:** https://www.fing.edu.uy/inco/cursos/redescomp/examenes/sirc0608.pdf

### Enunciado (texto literal del examen)

> Enuncie los resultados de Nyquist y Shannon vistos en el teórico. Comente sobre las
> hipótesis de cada uno de ellos.

### Solución oficial (textual)

> **Teorema de Nyquist**
> *Hipótesis:*
> · Canal de comunicaciones de ancho de banda limitado H, **sin ruido de ningún tipo**
> · La señal transmitida por el canal es una **señal digital de V niveles discretos**
>
> *Resultado:* La máxima tasa de transmisión de bits alcanzable es **M = 2 H log₂(V)**
>
> **Ley de Shannon**
> *Hipótesis:*
> · Canal de ancho de banda H
> · Canal sometido a **ruido gaussiano de potencia N**
> · Señal de transmisión de potencia **S**
>
> *Resultado:* La capacidad del canal (en bits) tiene un máximo teórico **C = 2 H log₂[1 + S/N]**

### Análisis de la solución oficial

**Lo que está bien:** las hipótesis correctas de cada uno (Nyquist sin ruido y con `V`
niveles; Shannon con ruido gaussiano y potencias `S` y `N`), y las dos fórmulas con sus
variables.

🔴 **Una errata en la oficial:** escribe Shannon como `C = 2 H log₂(1+S/N)`, que es un
error de transcripción: **la fórmula correcta es `C = B · log₂(1 + S/N)`, SIN el 2 delante.**
El `2` es de Nyquist, cuya fórmula (`M = 2·H·log₂(V)`) sí está bien.

**Lo que falta y son los puntos que se ganan:**
1. **No explica cada variable con sus unidades** (Hz, niveles, lineal).
2. **No dice que `S/N` va en lineal, no en dB.**
3. **No relaciona los dos teoremas** (cuándo aplica cada uno).

### Mi respuesta completa (5 puntos)

**Nyquist** — teorema de muestreo sin ruido:

```
  C_N = 2 · B · log₂(V)   [bps]
    · B = ancho de banda del enlace, en HERTZ (Hz)
    · V = cantidad de niveles discretos de la señal

  Hipótesis:
    (1) el canal tiene ancho de banda LIMITADO a B;
    (2) NO hay ruido de ningún tipo;
    (3) la señal es digital, de V niveles;
    (4) (implícita) el medio transmite 2 SEÑALES por segundo, una por cada
        cambio de nivel; de ahí el factor 2.

  Idea: cada símbolo puede estar en uno de V estados, así que vale log₂(V) bits, y caben
  2 símbolos por Hz de ancho de banda.
```

**Shannon** — teorema de la capacidad del canal:

```
  C_S = B · log₂(1 + S/N)   [bps]
    · B = ancho de banda del enlace, en HERTZ (Hz)
    · S = potencia de la señal;  N = potencia del ruido (en W)
    · S/N = relación señal-ruido, EN LINEAL (si viene en dB: 10^(dB/10))

  Hipótesis:
    (1) el canal tiene ancho de banda limitado B;
    (2) el ruido es GAUSSIANO de potencia N;
    (3) hay una señal de potencia S;
    (4) el límite NO son los niveles de señal (V no aparece), sino el ruido.
```

**La relación entre ambos:**

> Nyquist es el techo de un medio **ideal sin ruido** con una modulación dada; Shannon es el
> techo del medio **real con ruido**. **Nyquist se usa para el medio limpio** (diseño del
> transmisor) y **Shannon para el medio real** (diseño del sistema). En la práctica la
> capacidad real está **por debajo de Shannon**, por atenuación, pérdida de sincronismo y
> overhead de protocolo.

### ⚠️ Errores típicos del 2006-08 P1

- **Poner `2 · B · log₂(1+S/N)`** en Shannon: **no lleva el 2**. Y **meter `S/N` en dB** sin
  convertir a lineal.
- **Intercambiar las hipótesis:** decir "Nyquist necesita ruido gaussiano" o "Shannon
  necesita V niveles".
- **No dar las unidades** de `B` (Hz) ni de `V` (niveles).

## 3.2 Examen 2007-07, Pregunta 1, apartado a (10 puntos) — capacidad sobre línea telefónica

> **Fuente:** Examen `sirc0707` — 31 de julio de 2007, Pregunta 1, apartado a.
> **Link:** https://www.fing.edu.uy/inco/cursos/redescomp/examenes/sirc0707.pdf

### Enunciado (texto literal del examen)

> **a)** Si se quiere calcular la máxima capacidad de transmisión de datos sobre una línea
> telefónica, ¿qué teorema visto en el curso se debe aplicar? Justifique y escriba la
> fórmula para calcularla, explicando el significado de las variables en la fórmula y qué
> unidades se suelen utilizar.

### Sobre la solución oficial

El PDF de `sirc0707` **no trae la solución publicada del apartado 1a**: trae el enunciado y
las soluciones de los problemas prácticos. La resolución de abajo es **solución propia**.

### Resolución (solución propia, para los 10 puntos)

**Paso 1 — Qué teorema aplicar: Shannon, no Nyquist.**

> **Justificación:** la línea telefónica es un medio **ruidoso** (par trenzado, susceptible a
> interferencia, diafonía y ruido térmico). Como el ruido **no es despreciable**, Nyquist,
> que asume un medio **sin ruido**, daría un techo optimista. Corresponde la **ley de
> Shannon**, creada exactamente para este caso.

**Paso 2 — La fórmula.**

```
  C = B · log₂(1 + S/N)   [bits por segundo, bps]
```

**Paso 3 — Significado y unidades de cada variable.**

| Variable | Significado | Unidad | Nota |
|---|---|---|---|
| `C` | capacidad: máximo de bits transmitibles **sin errores** | **bps** | Es un techo **teórico**. |
| `B` | ancho de banda del canal | **Hertz (Hz)** | Para una línea telefónica, `B ≈ 3100 Hz`. |
| `S` / `N` | potencia de la señal / del ruido | **W (watts)** | |
| `S/N` | relación señal-ruido, o sea calidad del canal | **adimensional (lineal)** | ⚠️ Si la dan en **decibeles**: `S/N = 10^(dB/10)`. |

**Pasos 4 y 5 — Valores típicos y un ejemplo numérico.**

```
  B = 3100 Hz,  S/N = 30 dB:
      S/N_lineal = 10^(30/10) = 1000
      C = 3100 · log₂(1 + 1000) = 3100 · 9,97 ≈ 30 900 bps
```

*Interpretación:* el máximo teórico de una línea telefónica decente es de unos **30 kbps**.
Por eso los módems de la época llegaban a 33,6 kbps y ahí paraban: **no era el cable ni el
módem, era Shannon**.

### ⚠️ Errores típicos del 2007-07 P1

- **Elegir Nyquist en vez de Shannon** (el error conceptual central). La línea telefónica tiene ruido, así que va Shannon.
- **No justificar por qué NO es Nyquist**, que es lo que pide el enunciado.
- **Meter el S/N en dB** sin convertir. **Olvidar las unidades de `B` (Hz).**

---

# PARTE 4 — SIMULACRO 1

> **Instrucciones (reproducción del formato real de FING):**
> - Individual, **sin material**, **3 horas (180 min)**.
> - **5 Preguntas Teóricas** (~40 pts) + **2 Problemas Prácticos** (30 pts cada uno).
> - Aprobación: **60 puntos**.
> - ⚠️ **Es obligatorio responder correctamente al menos 15 puntos en las preguntas
>   teóricas.** Si no llegás a 15 en teoría, no aprobás aunque sumes 60 con los problemas.
> - Empezá cada pregunta y cada problema en una hoja nueva. Para los problemas podés
>   suponer que disponés de los tipos básicos (lista, cola, archivo, string) y sus funciones.
>
> ⏱️ **Cronómetro sugerido (180 minutos):**
>
> | Etapa | Min | Objetivo |
> |---|---|---|
> | Lectura inicial | 5 | leer entero, elegir por dónde empezar |
> | T1 (10 pts) | 15 | |
> | T2 (10 pts) | 15 | |
> | T3 (8 pts) | 13 | |
> | T4 (8 pts) | 12 | |
> | T5 (4 pts) | 8 | **63 min de teoría, ~40 pts** |
> | Problema 1 (30 pts) | 52 | aritmética larga: dejar la fórmula y la cuenta a medias |
> | Problema 2 (30 pts) | 48 | tablas antes que prosa; re-leer los números |
> | Repaso final | 7 | re-leer los números de los dos problemas |
> | **Total** | **180** | |
>
> **El consejo de la cátedra:** los problemas se corrigen **por lo que escribiste**. Si no te
> da el número exacto, **dejá la fórmula y la cuenta a medias** con la unidad anotada:
> parcialmente es puntos. Un apartado en blanco es cero.

---

## 4.1 El repaso que hay que tener delante antes del simulacro

**Las fórmulas, de memoria:**

```
  d_transmisión = L/R            (L en BITS,  R en bps)          clases 5-6
  d_propagación = d/s            (d en METROS, s en m/s)          clases 5-6
  BDP           = R · RTT        (bits en vuelo)                 clases 5-6 y 19
  latencia    ≈ RTT/2            (solo con camino simétrico)      clases 5-6
  Nyquist:  C = 2 · B · log₂(V)                                 esta clase
  Shannon:  C = B · log₂(1 + S/N)    (S/N EN LINEAL)             esta clase
  dB → lineal:  S/N = 10^(dB/10)                                 esta clase
  QAM:  bits por símbolo = log₂(M)  (M = puntos de la constelación) esta clase
```

**OSI contra TCP/IP, y las PDU:** en OSI son 7 capas y las PDU son **mensaje → segmento →
paquete → trama → bit**; en TCP/IP son **4 capas** (Aplicación, Transporte, Internet,
Acceso), que se leen **5** si partís Acceso en Enlace y Física. Correspondencia: OSI 7-5 ↔
Aplicación, OSI 4 ↔ Transporte, OSI 3 ↔ Internet, OSI 2-1 ↔ Acceso.

⚠️ El modelo TCP/IP se cuenta como **4 capas** (Acceso, Internet, Transporte, Aplicación) o
como **5** si separás Acceso en Enlace y Física. La cátedra lo explica en la Clase 2.

**Las tres técnicas de conmutación:**

| | Circuito | Paquetes (store-and-forward) | Mensajes |
|---|---|---|---|
| Conexión | sí | no (o circuito virtual) | no |
| Unidad | flujo continuo | paquete de tamaño fijo | mensaje completo |
| Reserva recursos | **sí** | **no** | **no** |
| Retardo | fijo y predecible | variable, con cola | muy variable |
| Orden | sí | **no** | **no** |

**Los parámetros que se confunden entre sí:** `R` (ancho de banda, **bps**, del equipo),
`s` (velocidad de propagación, **m/s**, del medio), **latencia** (un viaje de ida, ≈ `RTT/2`
si el camino es simétrico), **RTT** (ida y vuelta, lo mide `ping`), **throughput**
(`min(R, ventana/RTT)`) y **jitter** (`R_máx − R_mín`).

## 4.2 Los 8 errores más frecuentes del Bloque A

| # | El error | Lo correcto | Por qué |
|---|---|---|---|
| 1 | Meter `R` (bps) en `d/s`. | `d/s` solo lleva `d` (m) y `s` (m/s). | `s` es del **medio**; `R` del **equipo**. |
| 2 | Confundir `R` con `s`. | `R` en bps, `s` en m/s. | "Cuánta info/s" contra "qué tan rápido viaja". |
| 3 | Poner `n·d_proc` con `n` enlaces. | Con `n` enlaces hay `n−1` routers. | Los extremos A y B son hosts. |
| 4 | Poner `2·B·log₂(1+S/N)`. | Shannon es `B·log₂(1+S/N)`, **sin el 2**. | El `2` es de Nyquist. |
| 5 | Meter `S/N` en dB. | Convertir: `10^(dB/10)`. | Shannon pide el cociente **lineal**. |
| 6 | Confundir latencia con RTT. | `latencia ≈ RTT/2` **solo** con camino simétrico. | Ida y vuelta pueden diferir. |
| 7 | Decir que el jitter es el retardo. | Jitter = **variación** del retardo. | Retardo alto y constante no rompe el audio; el jitter sí. |
| 8 | Decir que la fibra es "más rápida". | La fibra tiene `s` apenas mayor y mucha más **alcance**. | `s` es casi igual; cambia la atenuación: 100 m contra 100 km. |
| 8 | Decir que la fibra es "más rápida" que el cobre. | La fibra tiene `s` apenas mayor y mucha más **alcance**. | `s` es casi igual; cambia la atenuación: 100 m contra 100 km. |

## 4.3 Enunciado del simulacro (sin respuestas)

### Preguntas Teóricas

**T1 (10 puntos).** En una red de paquetes, un paquete de longitud `L` cruza un medio.
a) Identifique los **componentes del retardo** y diga cuáles son los más significativos.
b) Diferencie el **ancho de banda** de la **velocidad de propagación** en el medio.
c) ¿En qué componente del retardo influye la **congestión**?

**T2 (10 puntos).** En una red de conmutación de paquetes:
a) Explique los conceptos de **congestión**, **pérdida** y **retardo**, y cómo se
   relacionan entre sí.
b) Una red pierde paquetes. Mencione **dos causas de pérdida que no sean por
   congestión**, y explique por qué un protocolo de transporte como TCP no puede
   distinguirlas.

**T3 (8 puntos).** Dos usuarios comparten un canal de comunicación.
a) Indique el significado de **FDMA** y de **TDMA**, y explique el principio de operación
   de cada uno.
b) ¿Son equitativos? ¿En qué sentido de "equitativo" se parecen a la conmutación por
   circuitos y en cuál a la de paquetes?

**T4 (8 puntos).** Sobre las tecnologías de transmisión:
a) Indique en qué consisten el modo **full duplex** y el modo **half duplex**.
b) Especifique para **Ethernet (IEEE 802.3)** y para **Wi-Fi (IEEE 802.11)** qué modo se
   usa y justifique. Explique por qué en uno de los dos el otro modo es imposible.

**T5 (4 puntos).** Compare la conmutación por **circuito**, por **paquetes** y por
**mensajes**: indique para cada una si reserva recursos en la red y qué unidad de datos
transmite.

### Problemas Prácticos

**Problema 1 (30 puntos) — Retardos.** Un paquete de `L = 12 000 bits` viaja de A hasta B
por **cuatro enlaces** unidos por **tres conmutadores**.

```
  ┌────┐     e1     ┌────┐     e2     ┌────┐     e3     ┌────┐     e4     ┌────┐
  │  A │══════════▶│SW1 │══════════▶│SW2 │══════════▶│SW3 │══════════▶│ B │
  └────┘          └────┘          └────┘          └────┘          └────┘
```

| Enlace | `R` | `d` (todos con `s = 2·10⁸ m/s`) |
|---|---|---|
| `e1` | 2 Mbps | 500 km |
| `e2` | 100 Mbps | 200 km |
| `e3` | 100 Mbps | 2000 km |
| `e4` | 1 Gbps | 50 km |

Cada conmutador retarda cada paquete `d_proc = 4 µs`. No hay retardo de cola.

**a)** Escriba la fórmula general del retardo total extremo a extremo, indicando cuántas
veces aparece cada término y **por qué** esas cantidades.
**b)** Calcule el retardo total con la aritmética a la vista, y diga qué componente domina y
qué porcentaje representa.
**c)** Suponga ahora `R₁ = R₂ = R₃ = R₄ = R = 100 Mbps`, `d_proc = 0`, y que cada
conmutador **transmite inmediatamente cada bit que recibe, sin esperar a que llegue el
paquete completo**. Escriba el nuevo retardo, explique **por qué** mejora respecto de (b) y
**en qué condición dejaría de mejorar**.
**d)** Calcule el RTT de la conexión y el *bandwidth-delay product* del enlace `e2`.

**Problema 2 (30 puntos) — Nyquist, Shannon, encapsulación y capas.** Dos sedes unidas por
un enlace de radio de **B = 500 kHz**, con **S/N = 40 dB** y modulación **16-QAM**. Cada
router tiene `d_proc = 3 µs`.

**a)** Escriba la fórmula de **Nyquist** con el significado y las unidades de cada
variable, y calcule la capacidad máxima del enlace con esa modulación.
**b)** Escriba la fórmula de **Shannon**, **convierta el S/N a lineal** mostrando la cuenta,
y calcule la capacidad máxima. Explique cuál de los dos resultados manda y por qué.
**c)** Para un mensaje de aplicación de 1200 bytes que viaja por capa 2, 3 y 4 (Ethernet,
IP, TCP), calcule el **tamaño de cada PDU** con cabeceras típicas (Ethernet 18 B, IP 20 B,
TCP 20 B) y la **eficiencia** resultante. Diga qué capa se ocupa de qué.
**d)** Mencione las **capas del modelo OSI** y sus **PDU**, y diga en cuál se ubica cada uno
de los cálculos anteriores (capacidad, retardo, tamaño del segmento). Justifique.

---

## 4.4 Resolución del simulacro

### T1 (10 puntos) — Componentes del retardo, BW contra propagación, congestión

```
  d_end2end = Σ ( d_proc + d_cola + d_transmisión + d_propagación )
```

**a)** Los **cuatro componentes** son: (1) **procesamiento** `d_proc` (CRC, leer la
cabecera, buscar el puerto de salida); (2) **encolamiento** `d_cola` (espera en la cola del
enlace de salida); (3) **transmisión** `d_trans = L/R` (meter el paquete entero en el
cable); (4) **propagación** `d_prop = d/s` (la señal recorriendo el medio).

**Los más significativos** son `d_transmisión` y `d_propagación`: son los únicos
**calculables** con los datos del enunciado (`L`, `R`, `d`, `s`) y los que **dominan** en
enlaces de cualquier longitud relevante. `d_proc` es despreciable (microsegundos) y `d_cola`
no se puede calcular a priori, porque depende del estado de la cola.

**b)** El **ancho de banda** `R` se mide en **bps** y depende del **equipo** (puerto,
transceptor, modulación); aparece en `d_trans = L/R`. La **velocidad de propagación** `s` se
mide en **m/s** y depende del **medio físico**; aparece en `d_prop = d/s`. Duplicar el ancho de
banda reduce `d_trans` a la mitad y **no cambia** `d_prop`: un enlace de 1 Gbps no es "50
veces más rápido" que uno de 100 Mbps, es 50 veces más **ancho**.

**c)** La congestión influye **solo en el retardo de encolamiento** `d_cola`, que es el
único componente que depende del estado de la cola, y la congestión **es** el estado de la
cola. La cadena: más tráfico → las colas se agrandan → `d_cola` sube → el retardo total
sube; y si la cola desborda el buffer, aparecen **pérdidas**. Los otros tres (`d_proc`,
`d_trans`, `d_prop`) no dependen de la carga.

### T2 (10 puntos) — Congestión, pérdidas y retardo

**a)** **Congestión:** escasez, **durante un período de tiempo**, de los **recursos
compartidos** para procesar todos los paquetes que los pretenden usar (capacidad de
procesamiento y buffers de los routers, y ancho de banda de los enlaces). Se manifiesta en
**pérdidas y/o retardos**. **Pérdida:** un paquete **se descarta cuando no encuentra lugar
en un buffer**; es **irreversible**, porque IP no reintenta. **Retardo:** el tiempo que
tarda un paquete en ir de un nodo al siguiente, con sus cuatro componentes.

**La relación:** la **congestión es la causa**; el **retardo de cola** y la **pérdida** son
los **dos síntomas** y vienen del mismo mecanismo. Primero aparece el retardo (la cola
crece) y después, si se desborda el buffer, la pérdida.

**b)** Dos causas que **no** son por congestión: un **checksum o CRC incorrecto** por un
error del medio, y un **descarte por ACL o firewall**, o porque el **TTL llega a 0**, o
porque se perdió un **fragmento** en IPv4.

**Por qué TCP no las distingue:** un paquete perdido es un paquete perdido; para TCP los tres
casos son **lo mismo**, y no hay forma de saber *por qué* se perdió desde el emisor. Por eso
su reacción (reducir la ventana) es **conservadora en unos casos y correcta en otros**.

### T3 (8 puntos) — FDMA y TDMA

**a)** **FDMA** (*Frequency Division Multiple Access*): divide el **espectro de frecuencias**
en sub-bandas y asigna **una sub-banda fija a cada usuario**, que la usa **todo el tiempo**.
**TDMA** (*Time Division Multiple Access*): un usuario usa **toda la banda disponible** pero
**solo en su ranura de tiempo** (*timeslot*), que se repite periódicamente.

```
  FDMA (eje vertical = frecuencia; cada usuario tiene su franja fija)

  ┌─────────┬─────────┬─────────┬─────────┐
  │ usuario 1 │ usuario 2 │ usuario 3 │ usuario 4 │
  │    ⋮    │    ⋮    │    ⋮    │    ⋮    │  ← el tiempo corre hacia
  │    ⋮    │    ⋮    │    ⋮    │    ⋮    │    abajo: cada uno transmite
  └─────────┴─────────┴─────────┴─────────┘     a la vez, en su banda

  TDMA (eje horizontal = tiempo; cada usuario tiene su ranura fija)

  ┌────┬────┬────┬────┐┌────┬────┬────┬────┐
  │ u1 │ u2 │ u3 │ u4 ││ u1 │ u2 │ u3 │ u4 │   tiempo →
  └────┴────┴────┴────┘└────┴────┴────┴────┘
   cada ranura usa toda la banda
```


**b)** Los dos son **equitativos y estáticos**: a cada usuario se le asigna siempre la misma
fracción del recurso, sin reparto dinámico. Se parecen a la **conmutación por circuitos**
(asignación fija) y no a la de paquetes, que no reserva nada y aprovecha el canal
**estadísticamente**, desperdiciando menos capacidad cuando hay usuarios inactivos.

### T4 (8 puntos) — Full duplex y half duplex

**a)** **Full duplex:** se puede **transmitir y recibir a la vez**. **Half duplex:** se
puede transmitir o recibir, pero **no simultáneamente** (se alternan por turnos).

**b)** **Ethernet (IEEE 802.3) con switch: full duplex.** Cada puerto es un enlace punto a
punto dedicado, con un par para transmitir y otro para recibir, así que no hay colisión. (En
los **hubs** antiguos, half duplex con CSMA/CD.) **Wi-Fi (IEEE 802.11): siempre half
duplex.** El medio es el **aire**, inherentemente compartido.

**Por qué en Wi-Fi el otro modo es imposible:** una radio **no puede transmitir y recibir a
la vez en la misma banda**, así que **no puede detectar una colisión mientras transmite**:
nadie "oye" el choque. Por eso Wi-Fi usa **CSMA/CA** en lugar de CSMA/CD: en vez de
detectar la colisión *después* de que ocurrió, la **evita** de antemano, con el tiempo de
espera aleatorio (*backoff*), el **NAV** (*Network Allocation Vector*) y el **RTS/CTS**
opcional, que resuelve el nodo oculto.

### T5 (4 puntos) — Las tres técnicas de conmutación

| | Circuito | Paquetes | Mensajes |
|---|---|---|---|
| **Unidad** | flujo continuo de datos | paquete de tamaño fijo | mensaje completo |
| **Recursos** | **sí** (reserva ancho de banda y buffers en cada nodo) | **no** (mejor esfuerzo) | **no** |

- **Circuito:** se establece un camino y se **reservan** recursos, como una línea telefónica
  dedicada: retardo fijo y predecible, pero desperdicia capacidad cuando el usuario está
  callado.
- **Paquetes:** cada paquete se enruta por separado, **sin reservar**: aprovecha el canal
  estadísticamente, con retardo variable y posibles pérdidas.
- **Mensajes:** se transmite el mensaje entero, todo o nada, sin conexión ni reserva.

### Problema 1 (30 puntos) — Retardos · Resolución

**a) Fórmula general y conteo de términos.** Con `n = 4` enlaces hay **4** términos de
`d_trans` y **4** de `d_prop`; con `k = 3` conmutadores hay **3** de `d_proc` y **3** de
`d_cola` (que aquí valen 0).

```
  d_end2end = Σ_{i=1..4} [ d_proc + d_cola + L/R_i + d_i/s_i ]
            = 3·d_proc + (L/R₁+L/R₂+L/R₃+L/R₄) + (d₁/s₁+d₂/s₂+d₃/s₃+d₄/s₄)

  ⚠️ El d_proc va 3 VECES (uno por conmutador), NO 4: hay 4 enlaces pero
     solo 3 conmutadores; A y B son sistemas terminales.
```

**b) Cálculo del retardo total con la aritmética a la vista.**

```
  L = 12 000 bits

  e1: R₁ = 2·10⁶,  d₁ = 5·10⁵ m,  s₁ = 2·10⁸
     d_trans = 12 000/2·10⁶  = 6,0·10⁻³ s =  6,000 ms
     d_prop  = 5·10⁵/2·10⁸   = 2,5·10⁻³ s =  2,500 ms   subtotal  8,500 ms

  e2: R₂ = 10⁸,  d₂ = 2·10⁵ m
     d_trans = 12 000/10⁸    = 1,2·10⁻⁴ s =  0,120 ms
     d_prop  = 2·10⁵/2·10⁸   = 1,0·10⁻³ s =  1,000 ms   subtotal  1,120 ms

  e3: R₃ = 10⁸,  d₃ = 2·10⁶ m
     d_trans = 12 000/10⁸    = 1,2·10⁻⁴ s =  0,120 ms
     d_prop  = 2·10⁶/2·10⁸   = 1,0·10⁻² s = 10,000 ms   subtotal 10,120 ms

  e4: R₄ = 10⁹,  d₄ = 5·10⁴ m
     d_trans = 12 000/10⁹    = 1,2·10⁻⁵ s =  0,012 ms
     d_prop  = 5·10⁴/2·10⁸   = 2,5·10⁻⁴ s =  0,250 ms   subtotal  0,262 ms

  d_proc total = 3 × 4 µs = 0,012 ms        d_cola total = 0

  d_end2end = 8,500 + 1,120 + 10,120 + 0,262 + 0,012 = 20,014 ms
```


**Qué componente domina y qué porcentaje:**

```
  d_propagación  = 2,500 + 1,000 + 10,000 + 0,250 = 13,750 ms  →  68,7 %  ◄── DOMINA
  d_transmisión  = 6,000 + 0,120 +   0,120 + 0,012 =  6,252 ms  →  31,2 %
  d_procesamiento                                        0,012 ms  →   0,06 %
  TOTAL                                                   20,014 ms  → 100 %

  El enlace e3 aporta 10,120 ms (50,6 %) y es el más lento por distancia;
  el e1 aporta 8,500 ms y es el de menor ancho de banda. Son dos cuellos de
  botella distintos: uno por distancia, el otro por ancho de banda.
```

**c) Cut-through (reenvío al vuelo), `R` uniforme y `d_proc = 0`.**

```
  R₁ = R₂ = R₃ = R₄ = R = 100 Mbps = 10⁸ b/s, y cada conmutador transmite
  cada bit apenas lo recibe.

  d_end2end = 1 · (L/R) + Σ_{i=1..4} (d_i/s_i)
            = 12 000/10⁸ + (5·10⁵ + 2·10⁵ + 2·10⁶ + 5·10⁴)/2·10⁸
            = 1,2·10⁻⁴ s + (2,85·10⁶ / 2·10⁸) s
            = 0,00012 s + 0,01425 s
            = 0,01437 s = 14,370 ms
```

**Por qué mejora, y en qué condición dejaría:**

> En store-and-forward cada conmutador debe **recibir el paquete completo** antes de emitirlo
> por el enlace siguiente (necesita leer la MAC destino), así que cada enlace intermedio
> aporta **otro `L/R` en serie**. Con cut-through el conmutador **no espera**: reenvía cada
> bit apenas lo recibe, así que **los `L/R` se pisan en vez de sumarse** y queda **uno solo**,
> y además desaparece el `d_proc`.
>
> **Condición:** el cut-through solo funciona si `R_entrada = R_salida` en **todos** los
> enlaces (aquí se cumple: los cuatro son 100 Mbps). Si un conmutador recibiera más rápido
> de lo que transmite (`R₁ = 1 Gbps` y `R₂ = 100 Mbps`), se acumularía cola y **volvería a
> comportarse como store-and-forward**, y además propagaría la congestión antes de tiempo
> (*congestion crunch*).

> ⚠️ **Ojo al comparar (b) con (c):** los dos resultados no son comparablesdirectly,
> porque en (b) los `R` y las `d` son heterogéneos y en (c) todo es 100 Mbps. La comparación
> justa es "a igual topología", y ahí la mejora es `(n−1)·(L/R) + k·d_proc`.

**d) RTT y BDP del enlace `e2`.**

```
  Latencia de ida por e2 = 1,000 + 0,120 = 1,120 ms
  RTT (camino simétrico) ≈ 2 × 1,120 = 2,240 ms = 2,24 s
  BDP = R₂ × RTT = 10⁸ × 2,24 = 2,24·10⁸ bits = 28 000 000 bytes = 28 MB

  ⚠️ El BDP NO depende del tamaño del paquete, sino de R y del RTT. Con un RTT de 2,24 s el
     enlace necesita 28 MB "en vuelo" para llenarse: eso exige una ventana enorme, y de ahí
     `RFC 7323` (*Window Scale*).
```

**Puntos:** (a) fórmula y conteo (8), (b) aritmética (10), (c) cut-through (8), (d) RTT y BDP (4).

### Problema 2 (30 puntos) — Nyquist, Shannon, encapsulación, capas · Resolución

**a) Nyquist: fórmula, variables y cálculo.**

```
  C_N = 2 · B · log₂(V)   [bps]
  · B = ancho de banda del enlace, en HERTZ (Hz).  Aquí B = 500 kHz = 5·10⁵ Hz.
  · V = niveles de la señal (estados por símbolo). Con 16-QAM, V = 16.

  C_N = 2 · 5·10⁵ · log₂(16) = 2 · 5·10⁵ · 4 = 4·10⁶ bps = 4 Mbps
```

**b) Shannon: fórmula, conversión del S/N y cálculo.**

```
  C_S = B · log₂(1 + S/N)   [bps],  con S/N EN LINEAL

  1) Convertir de dB a lineal:
        S/N_dB = 40
        S/N_lineal = 10^(40/10) = 10⁴ = 10 000

  2) Aplicar Shannon:
        C_S = 5·10⁵ · log₂(1 + 10 000) = 5·10⁵ · log₂(10 001)

  3) El logaritmo: 2¹³ = 8192 y 2¹⁴ = 16384, así que 10 001 está entre
     ambos y log₂(10 001) ≈ 13,29.

  4) C_S = 5·10⁵ · 13,29 ≈ 6,64·10⁶ bps ≈ 6,64 Mbps
```

**Cuál manda y por qué:**

> La capacidad real de un enlace es el **mínimo de los dos techos**, y en la práctica no
> alcanza ninguno: los medios reales **siempre tienen ruido**, y además hay pérdida de
> sincronismo, atenuación y overhead, así que los sistemas reales se **diseñan al 50-70 % de
> Shannon**.
>
> En este caso el enunciado **fija la modulación** (`V = 16`), así que Nyquist da 4 Mbps y el
> cuello es el **transmisor**; el piso que impone la calidad del medio es Shannon, con
> 6,64 Mbps.

**c) Tamaño de las PDU y eficiencia.** Con cabecera TCP de 20 B, IP de 20 B y trama
Ethernet de 18 B (preámbulo y FCS incluidos):

```
  Capa 4 (Transporte):  segmento TCP = 1200 + 20 = 1220 bytes
  Capa 3 (Red):         paquete IP   = 1220 + 20 = 1240 bytes
  Capa 2 (Enlace):      trama        = 1240 + 18 = 1258 bytes
  Eficiencia  η = 1200 / 1258 ≈ 0,954  →  95,4 %
```

**Qué capa se ocupa de qué:** la **capa 2** arma la trama (MAC y CRC); la **capa 3** arma el
paquete (IP y enrutamiento); la **capa 4** arma el segmento (puertos, secuencia y checksum);
y la **capa 1** transmite los bits por el medio.

**d) Las capas del modelo OSI, sus PDU y dónde caen los cálculos.**

```
  Capa OSI      PDU                ¿Qué calcula?
  ───────────────────────────────────────────────────────────────────
  7-5 Aplicación, mensaje           — (los datos del usuario)
  4 Transporte  segmento            — el tamaño del segmento (apartado c)
  3 Red         paquete             — el retardo extremo a extremo
  2 Enlace      trama               — el tamaño de la trama (apartado c)
  1 Física      bit                 — la CAPACIDAD: Nyquist y Shannon
```

**Justificación:** la **capacidad** (Nyquist y Shannon) es propiedad de la **capa física**,
porque depende solo del medio y del transceptor. El **retardo extremo a extremo** es un
concepto de la **capa 3 (Red)**: es el tiempo que tarda un **paquete** en viajar de un nodo
a otro. El **tamaño del segmento** depende de la **capa 4 (Transporte)**, que agrega la
cabecera TCP.

---

# PARTE 5 — CIERRE

## 📌 Resumen

1. La **capa física** solo transmite **bits**: no detecta errores, no reenvía, no reintenta.
2. Los cuatro medios: **par trenzado** (100 m, sensible al EMI), **coaxial** (~10 Mbps), **fibra** (inmune al EMI, 100 km), **inalámbrico** (aire compartido).
3. **Full duplex** = transmitir y recibir a la vez; **half duplex** = por turnos. **Ethernet conmutado es full duplex; Wi-Fi es siempre half duplex.**
4. **Nyquist**: `C = 2·B·log₂(V)`, medio **sin ruido**, techo de la modulación.
5. **Shannon**: `C = B·log₂(1+S/N)`, medio **con ruido gaussiano**, `S/N` **en lineal** (`10^(dB/10)`), **sin el 2 delante**.
6. **Shannon siempre queda por debajo de Nyquist**, y el diseño real queda por debajo de Shannon.
7. **QAM** combina amplitud y fase: una constelación de `M` puntos vale `log₂(M)` bits por símbolo.
8. Con **`n` enlaces** y **`k` conmutadores**: `k·d_proc + n·(L/R) + n·(d/s)`. **Cut-through** deja **un solo** `L/R`.
9. **Satélite**: 120 ms de ida, irrecuperables. El mejor ejemplo de por qué ancho de banda y latencia son cosas distintas.
10. Nyquist es `2·B·log₂(V)` y Shannon `B·log₂(1+S/N)`: **nunca se mezclan.**

## ✅ Autoevaluación

Respondé sin mirar. Las respuestas están en `<details>`.

**1.** Un enlace de cobre de 3 km soporta 100 Mbps, con `s = 2·10⁸ m/s`. ¿Cuánto tarda la **propagación** de un bit? ¿Y la **transmisión** de un paquete de 1500 bytes? Si duplico el ancho de banda, ¿cambia la propagación?

<details><summary>Respuesta</summary>

`d_prop = 3000 / 2·10⁸ = 15 µs` y `d_trans = 12 000 / 10⁸ = 120 µs`. Al duplicar el ancho de
banda, `d_prop` **NO cambia** (sigue en 15 µs, porque `d/s` no contiene `R`) y `d_trans` baja
a la mitad, a 60 µs.

</details>

**2.** ¿Por qué la velocidad de propagación es casi la misma en cobre y en fibra, si la
fibra "gana"? ¿Qué gana entonces?

<details><summary>Respuesta</summary>

Porque `s` depende de las propiedades electromagnéticas del material: cobre ≈ 2,00·10⁸ m/s y
fibra de sílice ≈ 2,04·10⁸ m/s. **Un 2 % de diferencia**, que sobre 1000 km son 0,1 ms.

Lo que gana la fibra es la **atenuación** (26 dB/km contra los 20 del cobre) y por eso el
**alcance sin electrónica**: 100 km en monomodo contra 100 m en cobre. No es "más rápida":
es más **alcance** y más **ancho de banda**, con el mismo `d/s`.

</details>

**3.** Un canal tiene `B = 4000 Hz` y `S/N = 20 dB`. ¿Cuál es la capacidad de Shannon?

<details><summary>Respuesta</summary>

`S/N = 10^(20/10) = 100` y `C = 4000 · log₂(101) = 4000 · 6,66 ≈ 26 600 bps`. Ojo: el
enunciado da **20 dB**, no 30. Y **Shannon es un techo teórico**: en la práctica la capacidad
real está al **50-70 %**, por atenuación, sincronismo, errores de constelación y overhead.

</details>

**4.** ¿Por qué la fibra es inmune al **EMI**, y por qué el par trenzado también reduce el
ruido si es cobre?

<details><summary>Respuesta</summary>

La fibra transmite **luz**, no campo eléctrico. La luz no es un campo electromagnético que se
pueda acoplar a un cable vecino, así que es **inmune al EMI** y a las descargas y
interferencias de radio. El cobre, en cambio, **sí** es campo eléctrico. El **par trenzado**
combate el ruido de dos formas: el **trenzado** hace que la interferencia externa afecte a
los **dos** hilos por igual, y como la señal se recibe como **diferencia**, se **cancela**; y
el **blindaje** (STP) agrega una malla metálica que hace de jaula de Faraday.

</details>

**5.** Si duplico la longitud del paquete, ¿qué componente del retardo cambia? ¿Y si duplico
la distancia? ¿Y el ancho de banda?

<details><summary>Respuesta</summary>

- **Duplico `L`:** cambia **solo `d_transmisión`** (se duplica); no cambia `d_prop`, ni
  `d_proc` (el CRC es de hardware), ni `d_cola`.
- **Duplico `d`:** cambia **solo `d_propagación`** (se duplica).
- **Duplico `R`:** cambia **solo `d_transmisión`**, que se reduce a la **mitad**.

**Las dos frases de examen:** "el ancho de banda nunca cambia la propagación" y "la distancia
nunca cambia la transmisión".

</details>

**6.** ¿En cuál de las tres técnicas de conmutación se **reservan** recursos y por qué tiene
un precio?

<details><summary>Respuesta</summary>

Solo el **circuito** reserva recursos (ancho de banda y buffers) en cada nodo del camino;
paquetes y mensajes son de "mejor esfuerzo" (*best effort*).

**El precio:** los recursos reservados quedan **ocupados** aunque el usuario no envíe nada,
así que se desperdicia capacidad; a cambio se garantiza retardo fijo. Paquetes aprovecha el
canal **estadísticamente** y es más eficiente con carga variable, a costa de retardo variable.

</details>

**7.** ¿Por qué no se puede implementar full duplex en Wi-Fi, y por qué usa CSMA/CA en vez
de CSMA/CD?

<details><summary>Respuesta</summary>

Porque el medio es el **aire**, inherentemente compartido: una radio **no puede transmitir
y recibir al mismo tiempo** en la misma banda, así que **no puede detectar una colisión
mientras transmite**. Por eso usa **CSMA/CA**: en vez de detectar la colisión *después*, la
**evita** con el *backoff* aleatorio, el **NAV** (*Network Allocation Vector*) y el
**RTS/CTS** opcional, que resuelve el **nodo oculto**. Es **siempre half duplex**.

</details>

**8.** ¿Cuál de los ocho errores es el más caro? Da un ejemplo numérico.

<details><summary>Respuesta</summary>

Meter **`S/N` en dB donde va en lineal** (o poner el `2` delante de la fórmula de Shannon).
En el Problema 2 del simulacro: `C = 5·10⁵ · log₂(1+40) ≈ 2,68 Mbps` en vez de
`C = 5·10⁵ · log₂(1+10 000) ≈ 6,64 Mbps`: **la mitad**. El otro caro es **poner `n·d_proc`
con `n` enlaces**: debe ser `(n−1)·d_proc`, porque los extremos del camino son sistemas
terminales, no dispositivos de conmutación.

</details>

## 🔗 Referencias

**Exámenes**
- `sirc0608` (5-ago-2006) — **P1 (5 pts): Nyquist y Shannon con sus hipótesis**. §3.1.
- `sirc0707` (31-jul-2007) — **P1 (10 pts): capacidad máxima sobre línea telefónica**. §3.2.
- `sirc0902` (2-feb-2009) — P3 (5 pts): FDMA y TDMA. Simulacro 1, T3.
- `sirc0903` (20-feb-2009) — P5 (6 pts): full duplex contra half duplex. §1.3 y T4.
- `sirc0912` (18-dic-2009) — P1 (10 pts): componentes del retardo, BW contra propagación, congestión. Clase 5 §3.1 y T1.
- `sirc1103` (21-feb-2011) — P2 (6 pts): congestión, pérdidas y retardo. Clase 5 §3.2 y T2.
- `sirc0712` (dic-2007) — P2 (4 pts): datagramas contra circuitos virtuales. T5.

**Bibliografía**
- Tanenbaum & Wetherall, *Redes de computadoras*, 5ª ed., cap. 1 §1.1 (la capa física y los medios) y §1.6 (el espectro inalámbrico).

**Normas (no RFC)**
- ⚠️ **Nyquist y Shannon no tienen RFC**: son resultados matemáticos, no protocolos. La capa
  física y la de enlace se estandarizan por **IEEE** (802.3, 802.11, 802.1Q); la capa
  física es **anterior a Internet**.
- `IEEE 802.11be-2024` — Wi-Fi 7, publicada el 22-jul-2025 (320 MHz y 4096-QAM).
- `IEEE 802.3cg` — 10BASE-T1S, obligatoriamente half-duplex con PLCA.

**Clases relacionadas**
- Clase 5 y 6 (el retardo y su taller) · Clase 8 (HTTP) · Clase 19 (BDP) · Clase 38 y 39 (capa de enlace).