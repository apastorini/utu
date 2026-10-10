# Clase 41 — Acceso al medio: ALOHA, CSMA/CD y CSMA/CA

**Bloque:** E (Capa de Enlace) · **Semana:** 14 · **Duración estimada:** 120 min
**Correlativa:** Clase 40 (corrección de errores y ARQ) · **Sigue con:** Clase 42 (switch, hub, VLAN y STP)
**Material de referencia:** Tanenbaum cap. 3 y 4 · Kurose §5.3 y §5.1.3 · Práctico 5 de 2008 (ejercicios 5, 6 y 8) · IEEE 802.3 · IEEE 802.11

---

## 🎯 Al terminar esta clase vas a poder

1. Explicar por qué un medio compartido necesita un protocolo de acceso al medio, y qué ocurre cuando dos estaciones transmiten a la vez.
2. **Derivar a mano** la eficiencia máxima del ALOHA puro (`1/(2e)`) y la del Slotted-ALOHA (`1/e`), y explicar por qué la segunda es *exactamente* el doble.
3. Derivar la eficiencia del ALOHA con franjas, `N·p·(1−p)^(N−1)`, y encontrar el `p` que la maximiza.
4. Distinguir **CSMA persistente de no persistente** y **con detección de colisión de sin detección**, y decir por qué Ethernet usa una combinación y WiFi la complementaria.
5. Escribir el algoritmo completo de **CSMA/CD**: persistencia 1, detección, jamming, backoff exponencial y la tabla de ventanas.
6. **Derivar los 64 bytes** de trama mínima a partir del slot time de 512 bits y del tiempo de ida y vuelta de la señal.
7. Diferenciar **dominio de colisión** y **dominio de broadcast**, y decir qué cambia al reemplazar un hub por un switch.
8. Resolver completo el **Examen 2007-07 P3** (10 pts) y el **Examen 2010-07 P2** (8 pts).

> **Prerequisito del examen:** `2007-07 P3` (10 pts — diferencia de rendimiento entre ALOHA y Slotted-ALOHA, y tipos de CSMA) · `2010-07 P2` (8 pts — ¿CSMA/CD en una red wireless? ¿y en una Ethernet completamente switcheada?) · `2010-12 P3` (8 pts — dominios de colisión y de broadcast) · `2007-03 P5` (5 pts — CSMA/CA) · `2007-02 P1` (5 pts — diferencias entre Pure ALOHA, Slotted ALOHA y CSMA/CD).

El tema aparece en **9 de los 50 exámenes oficiales** del banco. Es el único del bloque E donde te piden **derivar una fórmula** en vez de solamente describirla.

> ⚠️ Esta clase **no repite nada** de la 38 (framing) ni de la 39 (paridad, checksum y CRC). El contenido de la trama ya está dado; lo que se decide acá es **quién tiene derecho a ponerla en el medio**. Y como la teoría y la práctica se pisan, la aritmética larga está **solo en la Parte 2**: acá va el mecanismo, allá van las cuentas.

---

# PARTE 1 — TEORÍA

## 1.1 El problema: un medio, muchas bocas

Un enlace entre dos puntos no da problemas. El problema aparece cuando el medio es **compartido**: un bus de coaxil, o —hoy, mucho más común— una banda de espectro radioeléctrico.

```
   Topología de medio compartido (bus coaxil)

   [H1]══╗
   [H2]══╬════════╤═══════════════════════════
   [H3]══╣ cable  ║   un solo medio físico
   [H4]══╝        ║   una sola señal a la vez
   [H5]═══════════╝


   Topología compartida (radio: WiFi / celular)

       ( H1 )   ( H2 )   ( H3 )   ( H4 )   ( H5 )
          \       |       |       |       /
           \      |       |       |      /
            ╰─────┴───────┴───────┴─────╯
                 la misma banda de frecuencia
                 para todos, todo el tiempo
```

El medio tiene una propiedad física dura: **solo admite una señal a la vez**. Si H2 y H5 ponen bits al mismo tiempo, al receptor le llega la suma física de ambas: voltajes que se suman, bits que se destruyen. Eso es una **colisión** (*collision*), y el resultado es que nadie recibe nada útil.

```
   H2 transmite:   1 0 1 1 0 0 1 0
   H5 transmite:   0 1 1 0 1 1 0 0      (al mismo tiempo)
   ─────────────────────────────────────
   lo que llega:   1 1 0 1 1 1 1 0      <- basura
```

Y hay un problema peor que la colisión: **aunque nadie esté transmitiendo, dos estaciones pueden decidir transmitir en el mismo instante**, porque ninguna se enteró de la decisión de la otra. No hay ningún cartel en el medio que diga "yo transmito ahora".

Entonces la capa de enlace resuelve dos preguntas distintas, que no hay que confundir:

| Pregunta | Nombre | Qué falla si no se resuelve |
|---|---|---|
| ¿Quién tiene derecho a transmitir **ahora**? | **control de acceso al medio** | colisiones |
| ¿Quién soy, a quién le hablo y dónde termino? | **direccionamiento de enlace** (dirección MAC) | nadie sabe a quién entregar la trama |

Esta clase es de la primera.

## 1.2 Las tres familias de protocolos de acceso

| Familia | Idea | Coste | Ejemplos |
|---|---|---|---|
| **Partición de canal** (*channel partitioning*) | se divide el medio en canales y cada estación tiene el suyo para siempre | se desperdicia capacidad si no todos usan a la vez | FDMA, TDMA, **CDMA** |
| **Toma de turnos** (*taking turns*) | hay un turno explícito, como un testigo | latencia, y hay que castigar a alguien si se cae | token ring, token bus |
| **Acceso aleatorio** (*random access*) | todos compiten a la vez y se resuelve con colisiones y reintentos | colisiones | **ALOHA, CSMA, CSMA/CD** |

Lo que sigue es toda la tercera familia, más CDMA (que es de la primera y aparece en el Práctico 5).

## 1.3 ALOHA puro

Nació en 1970 en la Universidad de Hawái (Abramson), sobre una red de satélite. El **algoritmo** es ridículamente simple: si tenés una trama, **la transmitís ahora**, sin preguntar nada; esperás el ACK; si no llega, asumís que hubo colisión y reintentás **al azar**. Es decir: cero inteligencia.

### El punto clave: la ventana de colisión

Tomemos una trama de duración `T` que una estación empieza a transmitir en `t = 0`:

```
   tiempo ───────────────────────────────────────────────────────►

   H2:  ████████████████
       └─── T ───┘   transmite de t = 0 a t = T

        ╔═══════════════════════════════════════════════╗
        ║  VENTANA DE COLISIÓN:  de t = 0 a t = 2T      ║
        ╚═══════════════════════════════════════════════╝

   Una trama que llega a t = T − 0,001  --> choca (se pisa por detrás)
   Una trama que llega a t = T + 0,001  --> choca (se pisa por delante)
   Una trama que llega a t = 2T + 0,1   --> NO choca (ya terminó)
```

**¿Por qué `2T` y no `T`?** Porque hay dos formas de solaparse:

- **Antes:** otra trama empieza en los últimos `T` segundos de la mía, y se pisa con mi parte final.
- **Después:** otra trama empieza entre `T` y `2T`, y se pisa con **lo que yo emití al comienzo, que todavía está viajando por el cable**.

Ese segundo caso es el que casi todos olvidan, y es la mitad de la eficiencia máxima.

## 1.4 Slotted-ALOHA: ponele un reloj a todos

Slotted-ALOHA (Dave Roberts, 1975) es **el mismo protocolo con una sola modificación**: el tiempo se divide en **ranuras** (*slots*) de tamaño exactamente `T`, y **solo se puede empezar a transmitir en el instante cero de una ranura**. Todas las estaciones comparten el reloj.

```
   ALOHA PURO                             SLOTTED ALOHA
   ───────────                             ──────────────

   H2:  ████████████████                   H2:  ████████████████
       |←────── 2T ────────→|                  |←──── T ────→|
   ═════╪═══════════════════╪══════════    ═════╪═══════════════╪═════════
       0                   T         2T        0      T         2T

   se puede empezar en        se puede empezar SOLO en
   cualquier momento          los bordes de ranura

   ══════════════════════════════════════════════════════════
   ALOHA puro:  ventana = 2T  ───────────────────►
   Slotted:     ventana = T   ◄──── se reduce a la mitad
   ══════════════════════════════════════════════════════════
```

**Y esa es toda la diferencia.** Todo lo demás es idéntico. La consecuencia es aritmética: **la ventana vulnerable se reduce de `2T` a `T`, la probabilidad de sobrevivir se multiplica por `e`, y la eficiencia máxima pasa de `1/(2e)` a `1/e`: exactamente el doble** (la cuenta completa está en §2.2).

## 1.5 ALOHA con franjas: un término medio

Versión intermedia que aparece en el **Práctico 5**: cada estación transmite una trama larga que ocupa **`N` ranuras seguidas**, y solo puede empezar en el instante cero de una ranura.

```
   ═══════╤══════════════════════════════╤═══════════╤══════
         │<----------- T ------------->│           │
   ═══════╧══════════════════════════════╧═══════════╧══════
      ranura 0     ranura 1    ...    ranura N-1   ranura N

   Est. A, bloque que empieza en la ranura 0:
      ████████████████████████████████████████   N ranuras

   Est. B intenta empezar en la ranura k, con 0 < k < N:
                ████████████                      colisión parcial
```

Si dos bloques se pisan **en parte** igual se arruinan, así que la eficiencia no mejora por eso. Lo que hace el esquema es **reducir el riesgo**: entre el inicio del bloque de A y el del de B pueden pasar `N` ranuras completas, y eso agranda la ventana de colisión desde `T` hasta `N·T`. El precio es que cada estación ocupa el medio `N` veces más tiempo.

```
   eficiencia(N, p) = N · p · (1 − p)^(N−1)

     ▲      ▲     ▲           ▲
     │      │     │           └── los otros N−1 bloques no deben
     │      │     │               empezar en las N−1 ranuras que
     │      │     │               yo ocupo
     │      │     └── probabilidad de que YO empiece (Poisson)
     │      └──────── cada bloque ocupa N ranuras de las N disponibles
     └─────────────── eficiencia: fracción del tiempo con al menos
                      un bloque sobreviviente

   máximo en   p = 1/N
   valor       (1 − 1/N)^(N−1)
   límite      N → infinito:   1/e  ≈ 0,368
```

Con `N` chico el máximo es **mayor** que `1/e` (`N = 2` da 0,5) y converge a `1/e` desde arriba. El costo real es que con `N = 2` ocupás el medio el doble de tiempo para la misma probabilidad: la eficiencia mide tramas por ranura, no bits por segundo. La deducción completa está en §2.3.

## 1.6 CSMA: escuchar antes de hablar

ALOHA tiene un desperdicio evidente: **no escucha el medio para decidir**. Eso es **CSMA**: *Carrier Sense Multiple Access*, acceso múltiple con sensesión de portadora.

### 1.6.1 El problema del epsilon

Dos estaciones A y B en un cable de 2.500 m, con `v = 2 × 10⁸ m/s`: la señal de A tarda `τ = 2500 / (2 × 10⁸) = 12,5 µs` en llegar a B.

```
   t = 0,000 µs    A empieza. La señal sale de A.
   t = 6,25 µs     La señal pasa por el punto medio del cable.
   t = 12,5 µs     La señal LLEGA a B.

   Si B está escuchando en t = 12,4 µs   ->  oye a A  ->  espera.   OK
   Si B empieza a transmitir en t = 12,4 µs ->  ¡colisión!
                                             (todavía no oyó nada)

   Ese medio microsegundo de margen es el epsilon.
```

En cable, `ε` puede ser arbitrariamente pequeño pero **siempre positivo**. O sea: **el sentido de portadora elimina todas las colisiones salvo las que caen dentro de una ventana de anchura `ε`**. Como `ε` es infinitésimo frente a `T`, a baja carga la eficiencia de CSMA **se acerca a 1**: un salto de varios órdenes de magnitud respecto de ALOHA. Guardá ese `ε`, porque **es exactamente lo que se rompe en wireless**.

### 1.6.2 Persistente vs. no persistente

| | **1-persistente** (*1-persistent*) | **No persistente** (*non-persistent*) | **p-persistente** (ranurado) |
|---|---|---|---|
| Qué hace si el medio está ocupado | espera **mirando** | espera un tiempo **aleatorio** y vuelve a escuchar | transmite con prob. `p`, con `1−p` espera una ranura |
| Ventaja | no desperdicia medio libre | **casi no hay colisiones** | compromiso continuo |
| Desventaja | si varias esperaban, **todas transmiten a la vez**: colisión garantizada | **regala ancho de banda**: el medio puede quedar libre sin que nadie transmita; en carga alta sube la colisión | parametrizable, en desuso |
| Se usa en | **Ethernet** | redes satelitales | casi nadie |

**El antídoto de la colisión masiva del 1-persistente es el backoff aleatorio** (§1.7). Y el 1-persistente es el elegido en Ethernet porque el medio es rápido y no conviene regalarlo.

### 1.6.3 Con detección de colisión vs. sin detección

Acá está el corte que divide a Ethernet de WiFi, y es lo que te preguntan en `2007-07 P3b`.

| | **Sin detección** (*collision non-detection*) | **Con detección** (*collision detection*, **CD**) |
|---|---|---|
| Qué hace | asume que si hubo colisión el medio está ocupado: espera a que se libere y reintenta | **escucha mientras transmite** y compara lo que manda con lo que vuelve |
| ¿Cómo se entera? | por la **ausencia del ACK** (detección indirecta) | por la **comparación de señales** (detección directa) |
| Coste de una colisión | un **ACK completo**, o sea un RTT entero, del orden de milisegundos | **microsegundos**: aborta al instante |
| Requisito de hardware | ninguno | **una tarjeta que escucha mientras transmite** |

```
   Tarjeta de red en modo CD
   ══════════════════════════════════════════════════

              ┌─────────────┐
  cable  ---> │             ├──->  medio compartido ---+
              │   summer    |                          |
              │  (se suma)  | <--- medio compartido ---+
              └──────┬──────┘
                     │
                     v
               ┌───────────┐
               │COMPARADOR │ --> ¿la suma es igual a lo que
               └───────────┘     mando?  NO --> hay colisión
```

En coaxil o en par trenzado balanceado esto es trivial: la tarjeta transmite por un par y escucha por el mismo par, y como la impedancia del medio es conocida puede distinguir "la señal que yo pongo" de "una señal que se le sumó". La frase para memorizar:

> **CSMA/CD funciona en cable porque la tarjeta puede escuchar el medio mientras transmite. En wireless no puede: la radio es half-duplex por naturaleza y su propia señal enmascara cualquier otra.**

### 1.6.4 La taxonomía completa

Las dos dimensiones son ortogonales, así que hay **cuatro combinaciones**:

| | **Sin detección** | **Con detección** |
|---|---|---|
| **1-persistente** | 1-persistent CSMA | **CSMA/CD** — el de Ethernet por cable |
| **No persistente** | non-persistent CSMA | CSMA/CD no persistente — no se usa en la práctica |

Y si en lugar de **detectar** la colisión el protocolo la **evita**, aparecen las variantes de **evitación** (*collision avoidance*, **CA**): CSMA/CA, que es el caso de 802.11.

### 1.6.5 CSMA/CA: por qué WiFi no puede usar CD

Respuesta corta: **en radio no se puede detectar una colisión mientras se transmite**. Cuatro argumentos:

1. **Autoenmascaramiento físico.** La propia transmisión es de unos 20 dBm (100 mW); la señal de una estación vecina que llega al receptor puede ser de −70 dBm. La diferencia es de **90 dB**, casi **un millón de veces** en potencia. No es un problema de algoritmo: es que la relación señal-ruido lo hace físicamente imposible. Peor: la radio tiene **una sola cadena de recepción** en la misma banda, así que **no puede escuchar mientras transmite**.
2. **La cobertura no es simétrica: la estación oculta.** Dos estaciones no tienen por qué alcanzarse igual. En el caso clásico, A y C **sí llegan a B** pero **no se escuchan entre sí**:

```
                    B
                   / \
                  /   \        A <-> C : NO se escuchan
                 /     \       A -> B : si
                A       C      C -> B : si

   Si A transmite, C no oye nada y cree que el canal está
   libre, así que C transmite, y B recibe dos señales
   superpuestas de las que ninguna le sirve.

   En un cable esto es imposible: si la señal de A llega a B,
   tiene que haber pasado por C. La geometría del cable
   GARANTIZA la simetría. La geometría del radio no.
```

3. **No existe un `T` mínimo acotado.** La corrección de CSMA/CD depende de que la trama sea **más larga que el tiempo de ida y vuelta del medio** (§1.8). En radio hay movilidad, fading y estaciones ocultas: ese tiempo no tiene un límite razonable, la trama mínima tendría que ser gigantesca y el rendimiento se caería a cero. **En cable ese límite existe porque topológicamente el cable tiene largo máximo.**
4. **El modelo de costo está invertido.** En wireless el único que puede juzgar la colisión es el receptor (por el CRC), así que **el emisor tiene que transmitir la trama entera para enterarse**. Si igual vas a transmitirla entera, conviene **evitar** la colisión en lugar de detectarla: esa es literalmente la diferencia entre CD y CA.

Y qué hace CSMA/CA entonces:

```
   802.11: la secuencia de un envio con RTS/CTS

   Estacion A           Estacion B           otras estaciones
       |                     |                       |
       |--- RTS ------------>|                       |  (oyen el RTS)
       |                     |                       |  NAV = duracion
       |<-- CTS -------------|                       |  del RTS (virtual)
       |                     |                       |
       |----- datos -------->|                       |
       |<---- ACK -----------|                       |
```

- **RTS** (*Request to Send*): A anuncia que va a mandar, y cuánto va a durar.
- **CTS** (*Clear to Send*): B confirma, y también anuncia cuánto va a durar.
- **NAV** (*Network Allocation Vector*): un "sentido de portadora virtual" que se guardan las estaciones que oyen el RTS pero no el CTS, para no transmitir durante la transferencia.

Es *evitación* por negociación, no *detección* por medición. Y el detalle final: **en 802.11 el ACK es obligatorio**, porque la única forma segura de saber que la trama llegó bien es que el receptor lo diga.

## 1.7 CSMA/CD: el algoritmo completo

Este es el protocolo de Ethernet por cable. La máquina de estados completa:

```
   ┌─────────────┐
   │   INICIO    │
   └──────┬──────┘
          v
   ┌──────────────────────────────┐
   │ 1. ¿Medio ocupado?          │---- si --> esperar y volver a 1
   │    (carrier sense)          │
   └──────┬──────────────────────┘
          │ no
          v
   ┌──────────────────────────────┐
   │ 2. TRANSMITIR la trama       |<------------------+
   │    escuchando a la vez       |                   |
   └──────┬──────────────────────┘                   |
          |                                           |
     ┌────┴─────────────────────┐                    |
     │ ¿se detecto colision?    |                    |
     └────┬─────────────────────┘                    |
    no   |        | si                               |
         |        v                                  |
         |  ┌─────────────────────────┐              |
         |  │ 3a. DETENERSE           |              |
         |  │ 3b. JAMMING: 32 bits   |              |
         |  │ 3c. esperar IFS 96 bits |              |
         |  │ 3d. r <- rand(0..2^k-1)|              |
         |  │     esperar r slots    |              |
         |  │ 3e. k <- k + 1         |--------------+
         |  └─────────────────────────┘
         v
   ┌──────────────────────────────┐
   │ 4. La trama llego completa   │
   └──────────────────────────────┘
```

**(a) Persistencia 1.** Si el medio está libre, transmite. La unidad de tiempo es el **slot time**.

**(b) Detección de colisión.** Compara la señal que manda (TX) con la que le vuelve del cable (RX). Si no coinciden, hay colisión.

**(c) La secuencia de jamming.** Al detectar la colisión la tarjeta **no se calla**: sigue mandando ruido deliberada durante un mínimo de **32 bits**. ¿Por qué? Porque la trama abortada tiene que ser suficientemente larga para que **todas** las demás estaciones del segmento la sientan como un evento de medio ocupado con trama inválida. Si simplemente cortara, las estaciones más lejos podrían no haberse enterado todavía y se meterían en el próximo slot. El jamming **sella** la colisión en el medio.

```
   Los 32 bits de jamming:

   trama abortada      JAMMING                (>= 32 bits)
   █████████████░░░░░░░░░░░░████████████████████████████
                     └────┘
            el receptor del otro lado ve una ráfaga de
            ruido y descarta la trama por el CRC
```

**(d) El backoff exponencial.** Después del jamming espera un **IFS** (*Inter Frame Space*, 96 bits a 10 Mb/s: el tiempo mínimo para que el medio se considere libre de nuevo) y después un número aleatorio de **ranuras**:

```
   r <- rand( 0 , 2^k - 1 )     k = numero de intento (1 en el primero)

   1er intento      -> k=1  -> r en [0, 1]     ->  2 valores
   2do intento      -> k=2  -> r en [0, 3]     ->  4 valores
   3er intento      -> k=3  -> r en [0, 7]     ->  8 valores
   10mo intento     -> k=10 -> r en [0, 1023]  ->  1024 valores
   11mo en adelante -> k=10 (tope) -> r en [0, 1023]

   (la tabla completa, con los tiempos, está en §2.4)
```

**¿Por qué exponencial?** Si dos estaciones colisionan, **el azar las separa**. Si las dos sortean `r = 0`, vuelven a chocar. El backoff exponencial hace que la probabilidad de que dos estaciones elijan el mismo valor **caiga a cero geométricamente** (`1/2^k` en el intento `k`) conforme se acumulan los intentos, y al mismo tiempo evita que una tercera quede esperando una ventana enorme.

**(e) El tope de 16 intentos.** Si después de **16 intentos** la trama sigue sin salir, se descarta y se reporta como *excessive collisions*. El objetivo es que **un nodo muerto no bloquee el segmento entero**: el corte es mejor que la parálisis.

> **La convención importa.** IEEE 802.3 escribe `r ∈ [0, 2^k − 1]` **con `k` empezando en 1 en el primer intento**. Otros textos (y algunas soluciones de FING) cuentan `k = 0`, y entonces la primera ventana es `[0, 0]`, de una sola opción. **Si el enunciado no aclara, escribí la convención que usás**: eso ya suma puntos.

**Y algo que casi nadie menciona:** si la red está poco congestionada (menos de una colisión cada 1024 tramas), muchas tarjetas usan **backoff no exponencial**: eligen `r` en `[0, 2^k − 1]` con `k` fijo en **10**, siempre. Es una optimización de latencia que no cambia el algoritmo.

## 1.8 El slot time y los 64 bytes

Este es el corazón de por qué existe un tamaño mínimo de trama en Ethernet. La aritmética completa está en §2.5; acá va la lógica.

**Paso 1 — La condición que hay que garantizar.** Para que CSMA/CD funcione, la tarjeta tiene que poder **darse cuenta de que hubo colisión mientras todavía está transmitiendo**. Si la trama terminara antes de que volviera el indicio, el emisor creería que tuvo éxito.

```
   tiempo de transmision de la trama  >=  tiempo de ida y vuelta
```

**Paso 2 — Cuánto tarda la señal en ir y volver.** El peor caso es transmitir hacia la estación **más lejana del segmento**, con el cable recorrido dos veces y las conversiones de los extremos. Si `τ` es el retardo de propagación de **un sentido**, entonces `t_ida_y_vuelta = 2 · τ`.

**Paso 3 — El slot time.** IEEE 802.3 lo fija en **512 tiempos de bit**, sea cual sea la velocidad: `51,2 µs` a 10 Mb/s, `5,12 µs` a 100 Mb/s, `0,512 µs` a 1 Gb/s.

**Paso 4 — Traducir a bytes.** `512 bits / 8 bits por byte = 64 bytes`.

**Ahí está el 64.** No es un número arbitrario ni una constante de interoperabilidad: **es exactamente el tiempo de ida y vuelta de la señal en el peor caso, medido en bits.**

### La misma cuenta en las otras velocidades

| Velocidad | Slot time | `τ` máximo (un sentido) | Distancia máxima teórica | Distancia real con topología |
|---|---|---|---|---|
| 10 Mb/s | 51,2 µs | 25,6 µs | **5120 m** | 2500 m con 5 repetidores |
| 100 Mb/s | 5,12 µs | 2,56 µs | **512 m** | 100 m por segmento con hub (100BASE-TX) |
| 1 Gb/s | 0,512 µs | 0,256 µs | **51,2 m** | 100 m por segmento, con extensión de portadora |

Fijate la fila de 1 Gb/s: **el presupuesto de tiempo se encogió 100 veces** respecto de 10 Mb/s, pero el largo del cable es el mismo. Por eso IEEE 802.3 inventó la **extensión de portadora** (*carrier extension*): en half-duplex a 1 Gb/s la tarjeta mantiene el medio "ocupado" por al menos **4096 tiempos de bit** (4,096 µs), metiendo símbolos que no son datos. Es un parche que existe **precisamente porque el 512 ya no alcanzaba**.

### Y el FCS también es mínimo

```
   ┌──────────────┬────────────┬──────────┬──────────────┐
   │ MAC destino  │ MAC origen │  Tipo    │    FCS       │
   │    6 B       │    6 B     │   2 B    │    4 B       │  = 18 B
   └──────────────┴────────────┴──────────┴──────────────┘
   ┌────────────────────────────────────────────────────────┐
   │              carga útil: 46 bytes mínimo               │
   │  (si el paquete IP es más chico, se rellena con        │
   │   "relleno" para llegar a 64 — de ahí el nombre        │
   │   padding)                                             │
   └────────────────────────────────────────────────────────┘

   6 + 6 + 2 + 46 + 4 = 64 bytes = 512 bits   OK
```

**Detalle con VLAN:** con etiqueta 802.1Q (4 bytes extra) la carga útil mínima baja a 42 bytes y la trama mínima **con etiqueta** es de 68 bytes. El mínimo absoluto sigue siendo 64 bytes **sin** etiqueta.

## 1.9 Dominios de colisión y de broadcast

Se confunden todo el tiempo y aparecen juntos en el examen `2010-12 P3`. Los definimos acá de forma breve; la Clase 42 los desarrolla a fondo con la tabla MAC y el *self-learning*.

| | **Dominio de colisión** | **Dominio de broadcast** |
|---|---|---|
| **Qué es** | las estaciones cuyas señales se superponen si transmiten a la vez | las estaciones que reciben una trama de broadcast |
| **Definido por** | el medio físico compartido | la capacidad de reenviar tramas por todos los puertos |
| **Se rompe con** | el switch (cada puerto es un dominio propio) | la VLAN (o un router) |
| **Máximo teórico** | 2 estaciones (full-duplex) | toda la red local |

```
   CON HUB -- todo es uno

   [H1]──┐
   [H2]──┼──> HUB ═══ 1 dominio de colisión ═══ 1 dominio de broadcast
   [H3]──┘         │                    │
                (todo el tráfico     (todo el tráfico
                 se ve en todas       se ve en todas
                 las bocas)           las bocas)


   CON SWITCH -- el de colisión se parte, el de broadcast no

   [H1]──┐                   ┌──> H1     dominio de colisión
   [H2]──┼──> SWITCH ═══┬═══ ┼──> H2     (uno por puerto,
   [H3]──┘              │     └──> H3      o sea UNO POR CADA)
   [H4]──────────────────┘     ╲   ╱
                             ╲   ╱
                      (las tramas de broadcast salen por TODOS
                       los puertos del mismo dominio de broadcast:
                       el switch no puede descartarlas porque no
                       tiene a quién entregarlas)
```

**Con un hub:** es de capa 1. Copia la señal a **todos** los puertos, sin mirar direcciones y sin decidir nada. Entonces: **un solo dominio de colisión** (comparte el mismo medio eléctrico) **y un solo dominio de broadcast**. Es la red del §1.1, con ALOHA encima.

**Con un switch:** aprende direcciones y decide a qué puerto va cada trama, y eso **parte el medio en un dominio de colisión por puerto**. Pero las tramas de broadcast no se pueden descartar —por definición todos tienen que oírla—, así que **el dominio de broadcast sigue siendo toda la red**. Salvo que existan VLANs.

> **La frase que hay que saber decir:** el switch **no evita colisiones**. Lo que hace es **eliminar el medio compartido**, y por eso es que las colisiones dejan de ser posibles. Son dos afirmaciones muy distintas, y confundirlas es el error conceptual más común del tema.

### ⚠️ Actualización a 2026

**Sigue igual — de memoria, sin dudar:**
- **CSMA/CD**: *exponential backoff*, **slot time = 512 bits**, trama mínima **64 B**, trama máxima **1518 B**, jamming de 32 bits, tope de 16 intentos.
- Formato de trama: preámbulo 7 + SFD 1, MAC destino 6 + MAC origen 6, tipo 2, carga útil, **FCS 4**. **MTU 1500.**
- **ARP (`RFC 826`)**: request en broadcast, reply en unicast. El *gratuitous ARP* sigue usándose (anuncio, DHCP, failover de gateway, VRRP) y sigue siendo una fuente clásica de *ARP spoofing*.
- **MAC learning**: el bridge aprende la MAC **origen** y asocia puerto; **flooding** si el destino es desconocido; **unicast** si se conoce.
- **Loops en capa 2 = broadcast storm**: sigue siendo la razón de ser del STP.

**Cambió o se modificó:**

- **El half-duplex Ethernet es historia por encima de 1 Gb/s.** Es una decisión de **IEEE 802.3**, **no una RFC de IETF**. ⚠️ **No existe ningún RFC que lo depreque**: `RFC 8984` es **JSCalendar**, nada que ver con Ethernet. A 10GbE y por encima el full-duplex punto a punto es obligatorio, y el half-duplex directamente no existe en la especificación de esas velocidades.
- **Pero half-duplex no desapareció del todo.** **IEEE 802.3cg 10BASE-T1S** (*single-pair Ethernet*, para redes PLC industriales sobre un solo par) es **obligatoriamente half-duplex**, con un protocolo de acceso propio, **PLCA**. Y en IETF, el módulo YANG `csma-cd` de `802.3cf` está marcado `status deprecated`. ⇒ **Saber cuándo CSMA/CD sigue existiendo es parte del tema.**
- **`RSTP` (`802.1w`) es el default real**, no el STP clásico. `MSTP` (`802.1s`) para varias instancias de VLAN. Bridge ID con prioridad base **32768**.
- ⚠️ **El "aging de 300 s" de la tabla MAC es un default de FABRICANTE, no un valor mandated por IEEE.** Enseñalá "típicamente 300 s en switches comerciales, configurable", **nunca** "el estándar IEEE dice 300 s".
- **`802.1Q-2022`** es el estándar actual (precedido por `802.1Q-2018`): 2018 abrió el bloque de TSN (`802.1Qbv`, `802.1Qbu` con `802.3br`, `802.1Qci`) y 2022 agregó `802.1Qcc` y `802.1Qcr`. **C-TAG (`0x8100`) vs. S-TAG (`0x88A8`)**: doble etiquetado para *provider bridges*, hoy lo estándar en carrier Ethernet y EVPN-VXLAN. **LAG**: `802.3ad` (2000) pasó a **`802.1AX`**, revisión vigente **`802.1AX-2020`**.

**Consecuencia para el examen:** si preguntan "¿CSMA/CD es necesario hoy?", la respuesta es **no, y ni siquiera existe por encima de 1 Gb/s**. Si preguntan "¿es siempre necesario en Ethernet?", la respuesta es **no: con full-duplex no hay colisión posible** (§3.2). Y si preguntan por el aging, decí "típicamente 300 s, configurable, default del fabricante".

---

# PARTE 2 — PRÁCTICA RESUELTA

> En toda esta parte **se supone que las tramas llegan en un proceso de Poisson** (arribos independientes con probabilidad constante por unidad de tiempo), que es el modelo estándar del libro. Es la única suposición fuerte, y hay que declararla, porque sin ella las cuentas no cierran.

## 2.1 Ejercicio 1 — Derivar la eficiencia del ALOHA puro (`1/(2e)`)

**Enunciado.** Una red de ALOHA puro tiene tramas de duración `T` y las estaciones generan tramas según un proceso de Poisson de tasa `λ`. Calcular la eficiencia y su valor máximo.

**Datos.** `G = λ · T` es la **carga ofrecida** (*offered load*): el número de tramas que el sistema **intenta** poner en el medio durante el tiempo que tarda una trama en entrar.

**Paso 1 — Probabilidad de colisión.** Una trama que envío en `t = 0` tiene ventana de `2T` (§1.3). En esos `2T` segundos pueden llegar `λ · 2T = 2G` tramas ajenas. Para no chocar necesito **cero**:

```
   P(sin colisión) = P(0 arribos en 2T) = e^(−2G)
```

*Interpretación:* es la probabilidad de **supervivencia** de una trama. Si `G = 0,5`, `e^(−1) = 0,368`.

**Paso 2 — Eficiencia.** De cada `G` tramas que el sistema intenta meter por unidad de tiempo de trama, sobrevive la fracción `e^(−2G)`:

```
   S = G · e^(−2G)
   ^   ^
   |   └── fracción que sobrevive sin chocar
   └────── tramas que se intentan meter por unidad de tiempo
```

**Paso 3 — Maximizar.** El factor exponencial siempre es positivo, así que el máximo está donde se anula el factor lineal de la derivada:

```
   S'(G) = e^(−2G) + G · (−2) · e^(−2G)
         = e^(−2G) · (1 − 2G)

   S'(G) = 0   -->   1 − 2G = 0   -->   G* = 1/2

   S''(G) = e^(−2G) · (−2 − 2 + 4G)
   En G = 1/2:   S'' = e^(−1) · (−2) < 0   -->  es MAXIMO
```

**Paso 4 — El valor.**

```
   S_max = (1/2) · e^(−2 · (1/2)) = (1/2) · e^(−1) = 1/(2e)

   1/(2e) = 1 / (2 · 2,71828) = 1 / 5,43656 = 0,18394  ≈  18,4 %
```

**Resultado: la eficiencia máxima del ALOHA puro es `1/(2e) ≈ 0,184`.** O sea: **de cada 5,44 tramas que el medio transporta, solo 1 es válida.** Las otras 4,44 se pierden en colisiones. Ese es el precio de no mirar nunca el medio antes de hablar.

**La misma cuenta sin derivadas** (por si el corrector no admite cálculo):

```
   S(1/2) = 0,5 · e^(−1)   = 0,5 · 0,36788 = 0,18394
   S(0,4) = 0,4 · e^(−0,8) = 0,4 · 0,44933 = 0,17973   <-- menor
   S(0,6) = 0,6 · e^(−1,2) = 0,6 · 0,30119 = 0,18072   <-- menor
```

El argumento sin cálculo: `S = G·e^(−2G)` es el producto de un factor que **crece** y otro que **decrece exponencialmente**, así que hay un único punto de equilibrio; y como `S` tiende a 0 cuando `G` tiende a infinito, ese punto es forzosamente un máximo.

| Carga `G` | Slotted `G·e^(−G)` | Puro `G·e^(−2G)` |
|---|---|---|
| 0,10 | 0,0905 | 0,0819 |
| 0,25 | 0,1947 | 0,1516 |
| **0,50** | **0,3033** | **0,1839 (máximo)** |
| 0,75 | 0,3543 | 0,1673 |
| **1,00** | **0,3679 (máximo)** | 0,1353 |
| 1,50 | 0,3347 | 0,0747 |
| 2,00 | 0,2707 | 0,0366 |

> **Errores típicos:** contar `T` en vez de `2T` (te da `1/e`, que es el número del Slotted); olvidar que hay que maximizar y no solo escribir la función; confundir `G` (un número de tramas por tiempo de trama) con una probabilidad.

## 2.2 Ejercicio 2 — Derivar la eficiencia del Slotted-ALOHA (`1/e`)

**Paso 1 — La ventana vulnerable.** Si solo puedo empezar en los bordes de ranura, dos tramas que empiecen en ranuras distintas **no pueden solaparse**. El único caso de colisión es que **empiecen en la misma ranura**.

```
   ranura 0 │ ranura 1 │ ranura 2 │ ranura 3 │
   ─────────┼──────────┼──────────┼──────────┤
      ▓▓▓▓▓ │          │ ▓▓▓▓▓    │ ▓▓▓▓▓    │
      A     │          │ B        │
      (empieza en 0)     (empieza en 2)
                  ↑
      no hay solapamiento: la ventana de A terminó
      justo cuando empieza B
```

**La ventana pasó de `2T` a `T`. Punto.** Ese es el único cambio.

**Paso 2 — Probabilidad de colisión.**

```
   arribos en una ventana de T segundos:  λ · T = G
   P(sin colisión) = P(0 arribos en T) = e^(−G)
```

**Paso 3 — Eficiencia y máximo.**

```
   S = G · e^(−G)

   S'(G) = e^(−G) − G · e^(−G) = e^(−G) · (1 − G)
   S'(G) = 0   -->   G* = 1

   S_max = 1 · e^(−1) = 1/e = 0,36788  ≈  36,8 %
```

**Paso 4 — Por qué dobla EXACTAMENTE.**

```
        S_slotted        G · e^(−G)          evaluado en G = 1
   ───────────────  ────────────────  =  ─────────────────  =  e^(−1)
        S_puro          G · e^(−2G)         evaluado en G = 1/2
                                        (1/2)·e^(−1)

   =  1 · e^(−1)  /  ( (1/2) · e^(−1) )
   =  e^(−1) / ((1/2) e^(−1))
   =  1 / (1/2)
   =  2
```

**La explicación de fondo** es de una frase: **el riesgo se redujo a la mitad**. Como la probabilidad de supervivencia es `e^(−ventana·λ)`, reducir la ventana a la mitad **multiplica por `e` la probabilidad de sobrevivir**; y como además la carga óptima se duplica (`G*` pasa de `1/2` a `1`), el resultado neto es un factor **exactamente 2**. No es aproximación: es `e` en el numerador contra un `1/2` en el denominador. Y un detalle elegante: el sistema ranurado puede (y debe) **ofrecer el doble de carga** para funcionar igual de bien, porque para la misma cantidad de tramas que mete gasta la mitad de tiempo expuesto.

## 2.3 Ejercicio 3 — Práctico 5, ejercicio 8: ALOHA con franjas

> **Fuente:** Práctico 5 de 2008, ejercicio 8 (página 2), basado en la sección 5.3 del libro.

**Enunciado (traducción).** "En la Sección 5.3 se ha proporcionado un resumen de la deducción de la eficiencia de ALOHA con franjas. En este problema completaremos la deducción.
**a.** Recordar que cuando hay `N` nodos activos, la eficiencia de ALOHA con franjas es `Np(1−p)^(N−1)`. Encontrar el valor de `p` que hace máxima esta expresión.
**b.** Utilizando el valor de `p` encontrado en (a), encontrar la eficiencia de ALOHA con franjas suponiendo que `N` se aproxima a infinito. (Pista: `(1 − 1/N)^(N−1)` se aproxima a `1/e` cuando `N` se aproxima a infinito.)"

**Dato.** `p` = probabilidad de que un nodo **empiece** a transmitir en un instante dado.

### Parte a) — el `p` que maximiza

```
   S(p) = N · p · (1 − p)^(N−1)

   dS/dp = N · (1−p)^(N−1)  −  N·p·(N−1) · (1−p)^(N−2)

   Factorizo N · (1−p)^(N−2):
         = N · (1−p)^(N−2) · [ (1−p) − p(N−1) ]

   Como N·(1−p)^(N−2) > 0, igualo a cero el corchete:

         (1−p) − p(N−1) = 0
         1 − p − pN + p = 0
         1 − pN = 0
         p* = 1/N
```

**Respuesta a): `p = 1/N`.** Cada estación empieza uno de cada `N` intentos: exactamente la carga que llena el medio sin pasarse. Es un **máximo** porque `S(0) = 0` y `S(1) = 0` (para `N > 1`) y hay un único punto crítico.

### Parte b) — el límite `N` hacia infinito

```
   S_max(N) = N · (1/N) · (1 − 1/N)^(N−1)
            = 1 · (1 − 1/N)^(N−1)

   ln [ (1 − 1/N)^(N−1) ] = (N−1) · ln(1 − 1/N)

   Para N grande usamos   ln(1 − x) ≈ −x − x²/2 − x³/3   con x = 1/N

       (N−1) · ln(1 − 1/N)
         ≈ (N−1) · ( −1/N − 1/(2N²) − 1/(3N³) )
         =  −(1 − 1/N)  −  (1/2)(1/N − 1/N²) − ...
         -->  −1 − 0 − 0  =  −1          cuando N --> infinito

   Entonces:    (1 − 1/N)^(N−1) --> e^(−1) = 1/e

   S_max(N --> infinito) = 1/e = 0,367879  ≈  36,8 %
```

**Respuesta b): la eficiencia tiende a `1/e`, que es exactamente el valor del Slotted-ALOHA.**

| `N` (ranuras por bloque) | `p* = 1/N` | `S_max = (1−1/N)^(N−1)` | contra `1/e` |
|---|---|---|---|
| 2 | 0,500 | 0,5000 | **+35,9 %** |
| 4 | 0,250 | 0,4219 | **+14,7 %** |
| 8 | 0,125 | 0,3927 | **+6,7 %** |
| 100 | 0,010 | 0,3697 | +0,5 % |
| infinito | → 0 | → 0,3679 (= `1/e`) | 0 |

**Cálculo numérico con `N = 100`:**

```
   p  = 1/100 = 0,01
   S  = 100 · 0,01 · (1 − 0,01)^(99) = 1 · (0,99)^99

      ln(0,99) = −0,0100503
      99 · (−0,0100503) = −0,99498
      e^(−0,99498) = 0,36973

   S = 0,3697   (contra 1/e = 0,3679: apenas 0,5 % por encima)
```

**Interpretación.** Con pocas ranuras por bloque la eficiencia "por ranura" es mejor, pero **cada estación ocupa el medio mucho más tiempo**: con `N = 2` ocupás el medio el doble de tiempo para conseguir la misma probabilidad. La eficiencia mide tramas por ranura, no bits por segundo.

> **Errores típicos:** poner `N(1−p)` en el exponente (el factor `N·p` cuenta cuántas **empiezan**, y el `(1−p)` cuenta cuántas **no empiezan**, `N−1` veces); creer que `p = 1/N` es `p = 1`; y **citar el límite `1/e` sin derivarlo**: en el examen, el paso del logaritmo vale la mitad del punto.

## 2.4 Ejercicio 4 — La tabla de backoff exponencial de CSMA/CD

**Enunciado (inventado).** Una estación de Ethernet de 10 Mb/s tiene un choque. Calculá, para los primeros 8 intentos: el valor máximo de `r`, la cantidad de valores posibles de la ventana y el tiempo máximo que puede esperar.

**Datos.** `slot time = 512 bits = 512 / 10⁷ = 51,2 µs`.

```
   r <- rand( 0 , 2^k − 1 )      k = numero de intento, arrancando en k = 1

   cantidad de valores posibles = (2^k − 1) − 0 + 1 = 2^k
   tiempo maximo de espera = r_max · slot time = (2^k − 1) × 51,2 µs
```

| Intento `k` | `2^k` | `2^k − 1` | valores de `r` | `r` en | t_máx = `(2^k−1)` × 51,2 µs |
|---|---|---|---|---|---|
| 1 | 2 | 1 | **2** | 0 … 1 | **51,2 µs** |
| 2 | 4 | 3 | **4** | 0 … 3 | 153,6 µs |
| 3 | 8 | 7 | **8** | 0 … 7 | 358,4 µs |
| 4 | 16 | 15 | **16** | 0 … 15 | 768,0 µs |
| 5 | 32 | 31 | **32** | 0 … 31 | 1,587 ms |
| 6 | 64 | 63 | **64** | 0 … 63 | 3,226 ms |
| 7 | 128 | 127 | **128** | 0 … 127 | 6,502 ms |
| 8 | 256 | 255 | **256** | 0 … 255 | 13,06 ms |
| 10 | 1024 | 1023 | **1024** | 0 … 1023 | 52,38 ms |
| 11 en adelante | 1024 | 1023 | **1024** | 0 … 1023 | 52,38 ms (tope) |

**Interpretación.** El tiempo máximo **crece por mitad en cada paso** y a partir del intento 10 se congela en 52,4 ms, que es aproximadamente un tiempo de ida y vuelta típico de una red local. Es decir: el protocolo garantiza que ninguna estación espere más que lo que tardaría un paquete en dar una vuelta a la red. Si fuera más, el backoff empezaría a **dominar** el tiempo de respuesta y la red se sentiría lenta por el mecanismo que justamente debía mejorarla.

```
   Si la red no está congestionada (menos de 1 colisión cada
   1024 tramas), muchas tarjetas usan k FIJO = 10 desde el
   primer intento:

   Primer choque -> r en [0, 1023] directamente.
   Ventana 1024 veces mas grande -> probabilidad de choque
   con otra estacion del orden de 1/1024.
```

> **Errores típicos:** empezar `k` en 0 (muchos textos lo hacen, pero IEEE cuenta el primer intento como `k = 1`; **escribí qué convención usás**); calcular `t_máx` como `2^k × slot` en vez de `(2^k − 1) × slot`; y olvidar que el backoff arranca **después** del IFS de 96 bits (9,6 µs a 10 Mb/s).

## 2.5 Ejercicio 5 — El slot time y la trama mínima: derivar los 64 bytes

**Enunciado (inventado, y es el mejor ejercicio conceptual de la clase).** Una red Ethernet de 10 Mb/s tiene un segmento de coaxil de 2.500 m, con velocidad de propagación `2 × 10⁸ m/s`. Cada estación tiene un retardo de transceiver de 0,1 µs en cada extremo.

**a)** Retardo de propagación de un sentido. **b)** Tiempo de ida y vuelta del extremo más lejano. **c)** ¿Qué condición debe cumplir la trama mínima? **d)** ¿Alcanzan 512 bits?

```
   (a) Retardo de propagacion de un sentido

   d = 2.500 m
   v = 2 x 10^8 m/s

   tau = d / v = 2500 / (2 x 10^8) = 12,5 x 10^-6 s = 12,5 µs

   Sumando los dos transceivers (uno en cada extremo):
   tau_total = 12,5 µs + 0,1 µs + 0,1 µs = 12,7 µs


   (b) Ida y vuelta

   t_ida_y_vuelta = 2 · tau_total = 2 · 12,7 µs = 25,4 µs
   (Los dos transceivers ya están incluidos: van uno en cada
    sentido del viaje.)


   (c) La condición. Para detectar una colisión, el indicio tiene
       que VOLVER antes de que la trama termine. Si la trama
       terminara antes, la tarjeta creería que salió bien:

           t_transmision  >=  t_ida_y_vuelta


   (d) Verificacion

   slot time = 512 · T_bit = 512 / (10 x 10^6) = 51,2 µs

   t_transmision (trama de 64 B) = 51,2 µs
   t_ida_y_vuelta               = 25,4 µs
   ─────────────────────────────────────────
   51,2 µs  >=  25,4 µs         OK, ALCANZA
```

### El paso inverso: de la condición al número de bytes

```
   1. La trama mínima debe durar >= el tiempo de ida y vuelta.
   2. IEEE fija el slot time (la unidad de tiempo del backoff,
      igual al tiempo máximo de ida y vuelta) en 512 bits.
   3. Por lo tanto la trama mínima es de 512 bits.
   4. 512 bits / 8 bits por byte = 64 bytes.
```

**Y la comprobación con el diagrama de los 64 bytes:**

```
   H1 (extremo izquierdo)                            H2 (extremo derecho)
      |                                                       |
 t=0  |██████  trama de 64 bytes, 512 bits                 |
      |                                                       |
      |<--------------- 12,7 µs ------------->|              |
      |        (la señal viaja)                |              |
      |                                                       |
      |   H2 empieza a transmitir en t = 51,2 − 12,7 − ε     |
      |                      = 38,5 µs − ε                    |
      |                                                       |
      |                                 ████  H2               |
      |<------ la onda de H2 vuelve ------------|             |
51,2− |                                                       |
  ε    |██████╳██████  <-- acá se cruzan las dos señales      |
      |      COLISION                                        |
      |                                                       |
      |   H1 detecta:  señal_tx distinta de señal_rx          |
      |   -> detiene la trama                                |
      |   -> transmite 32 bits de JAMMING                    |
      |   -> espera 96 bits de IFS                           |
      |   -> sortea r en [0, 2^1 − 1] = [0,1] slots          |
      |   -> reintenta                                       |
```

*Interpretación:* **todo el mecanismo cabe dentro de la trama mínima.** La tarjeta no espera a que termine: aborta en unos 51 µs. Ese es el beneficio de CD frente a la detección indirecta por ACK, que costaría un RTT completo.

```
   La generalización a otras velocidades:

   A 100 Mb/s:   512 / (100 x 10^6) = 5,12 µs
                 -> la distancia máxima cae a
                    (5,12/2) x 10^-6 x 2 x 10^8 = 512 m

   A 1 Gb/s:     512 / (10^9) = 0,512 µs
                 -> la distancia máxima cae a 51,2 m
                 -> INSUFICIENTE para los 100 m del cable
                    -> de ahi la extensión de portadora
                       de IEEE 802.3 (4096 tiempos de bit)
```

> **Errores típicos:** dividir solo por 2 sin justificar por qué (decí "la colisión tiene que aparecer en el receptor **antes** de que el emisor termine"); olvidar el tiempo de transmisión de la trama y comparar solo propagación contra 512 bits (la condición es `t_tx >= 2·tau`); y confundir 512 **bits** con 512 **bytes**.

## 2.6 Ejercicio 6 — CDMA: los ejercicios 5 y 6 del Práctico 5

> **Fuente:** Práctico 5 de 2008, ejercicios 5 y 6 (página 1).
> CDMA = *Code Division Multiple Access*, acceso múltiple por división de código. Es un protocolo de **partición de canal**: en vez de dividir el tiempo o la frecuencia, divide el **espacio de códigos**.

**La regla de oro.** Cada bit de dato `d_i` se codifica multiplicándolo, bit a bit, por un código de `M` chips del emisor:

```
   Z_(i,m) = d_i · c_m          m = 1 ... M

   c_m en {+1, −1}      <- el codigo del emisor, M valores
   d_i en {+1, −1}      <- el bit de dato, representado con signo
```

**Convención del libro (importante):** para hacer la aritmética, **un bit de dato `0` se representa como `−1`**, no como `0`.

### Ejercicio 5 — emisor único con código (1, −1, 1, −1, 1, −1)

**Enunciado (traducción).** "Considérese el ejemplo de emisor único CDMA de la Figura 5.11. ¿Cuál sería la salida del emisor (para los dos bits de datos mostrados) si el código CDMA del emisor fuera (1, −1, 1, −1, 1, −1)?"

**Datos.** `M = 6` porque el código tiene 6 valores. Cada bit produce **6 chips**, y con 2 bits la salida tiene **12 valores**. La tabla completa, para los cuatro pares posibles (así leés el que muestre tu edición):

| bits mostrados | `d_0` | `d_1` | salida ranura 0 (6 chips) | salida ranura 1 (6 chips) |
|---|---|---|---|---|
| **1 1** | +1 | +1 | `1 −1 1 −1 1 −1` | `1 −1 1 −1 1 −1` |
| **1 0** | +1 | −1 | `1 −1 1 −1 1 −1` | `−1 1 −1 1 −1 1` |
| **0 1** | −1 | +1 | `−1 1 −1 1 −1 1` | `1 −1 1 −1 1 −1` |
| **0 0** | −1 | −1 | `−1 1 −1 1 −1 1` | `−1 1 −1 1 −1 1` |

**Ejemplo desarrollado, el caso "1 0":**

```
   d_0 = 1   ->  Z_0 = 1 · (1, −1, 1, −1, 1, −1) = ( 1, −1,  1, −1,  1, −1)
   d_1 = −1  ->  Z_1 = −1 · (1, −1, 1, −1, 1, −1) = (−1,  1, −1,  1, −1,  1)

   Salida completa (12 chips):
     ( 1, −1,  1, −1,  1, −1, |  −1,  1, −1,  1, −1,  1 )
      └────── dato 1 ──────┘   └────── dato 0 ──────┘
```

**Interpretación — la idea que hay que escribir en el examen:** el segundo bloque es **exactamente el negativo** del primero. Mandar un `0` es mandar **el código dado vuelta**, no "no mandar nada". Eso es lo que permite después **separar** a los emisores: el receptor multiplica por el mismo código y el `−1` le queda como signo.

**La decodificación, para verificar que el sistema funciona:**

```
   d_reconstruido = (1/M) · suma de  Z_(i,m) · c_m

   Ranura 0 (d_0 = 1):
     1/6 · (1·1 + (−1)(−1) + 1·1 + (−1)(−1) + 1·1 + (−1)(−1))
   = 1/6 · (1 + 1 + 1 + 1 + 1 + 1) = 1/6 · 6 = 1     OK

   Ranura 1 (d_1 = −1):
     1/6 · ((−1)(1) + (1)(−1) + (−1)(1) + (1)(−1) + (−1)(1) + (1)(−1))
   = 1/6 · (−6) = −1                                    OK
```

*Interpretación:* **la suma da `+M` o `−M`**, y al dividir por `M` sale `+1` o `−1`. El componente clave es que **cada chip se multiplica por sí mismo** (`c_m · c_m = c_m² = 1`), así que el código aporta siempre `+M` de energía útil.

### Ejercicio 6 — el emisor 2

**Enunciado (traducción).** "Considérese el emisor 2 de la Figura 5.12. ¿Cuál es la salida del emisor al canal (antes de que se añada a la señal del emisor 1) `Z_m`?"

**Datos.** El emisor 2 tiene los bits de datos `(−1, +1)` (es decir, "0 1") y su propio código, también de 6 chips. Tomemos `c₂ = (1, −1, −1, −1, −1, 1)`.

```
   Datos:   d_0 = −1          d_1 = +1

   Ranura 0:
     Z_0 = (−1) · (1, −1, −1, −1, −1, 1) = (−1, +1, +1, +1, +1, −1)

   Ranura 1:
     Z_1 = (+1) · (1, −1, −1, −1, −1, 1) = ( 1, −1, −1, −1, −1,  1)

   Salida Z_m:
     (−1, +1, +1, +1, +1, −1, |  1, −1, −1, −1, −1,  1 )
```

### Continuación natural — el agregado y por qué CDMA funciona *(solución propia)*

Esta parte no está en el enunciado del práctico, pero es **la pregunta que de verdad importa**: ¿cómo se separan las señales si van mezcladas por el mismo canal? **El canal es aditivo**: todas las señales se suman en el aire.

```
   S_(i,m) = Z1_(i,m) + Z2_(i,m)

   Ranura 0:  (−1, 1, 1, 1, 1, −1)  +  (0, 0, 0, 0, 0, 0)
              emisor 1 (d=−1)           emisor 2 (d=−1)
            = (−1, 1, 1, 1, 1, −1)

   Ranura 1:  (0, 0, 0, 0, 0, 0)      +  (1, −1, −1, −1, −1, 1)
              emisor 1 (d=−1)           emisor 2 (d=+1)
            = ( 1, −1, −1, −1, −1,  1)
```

**Decodificar con el código del emisor 2 (ranura 1):**

```
   S·c2 = 1·1 + (−1)(−1) + (−1)(−1) + (−1)(−1) + (−1)(−1) + 1·1
        = 1 + 1 + 1 + 1 + 1 + 1 = 6

   d2_reconstruido = 6/6 = 1     OK,  el emisor 2 mandaba un 1
```

**Decodificar con el código del emisor 1 (ranura 1):**

```
   c1 = (1, 1, 1, −1, 1, −1),   S_(1,·) = (1, −1, −1, −1, −1, 1)

   S·c1 = 1·1 + (−1)·1 + (−1)·1 + (−1)(−1) + (−1)·1 + 1·(−1)
        = 1 − 1 − 1 + 1 − 1 − 1 = −2

   d1_reconstruido = −2/6 = −1/3     NO es ni +1 ni −1
```

**Ese `−1/3` es la interferencia del otro emisor.** Y acá está la lección, que vale más que el ejercicio:

> **CDMA solo funciona si los códigos de los emisores son ORTOGONALES**, es decir, si su **producto interno es cero**: `⟨c₁, c₂⟩ = Σ c₁(m)·c₂(m) = 0`.

```
   ⟨c1, c2⟩ = (1)(1) + (1)(−1) + (1)(−1) + (−1)(−1) + (1)(−1) + (−1)(1)
             =  1  −  1  −  1  +  1  −  1  −  1
             =  −2        NO es cero.  NO ortogonales
```

Con un código del emisor 2 que **sí** sea ortogonal con `c₁ = (1, 1, 1, −1, 1, −1)`, por ejemplo `c₂' = (1, −1, 1, −1, −1, 1)`:

```
   ⟨c1, c2'⟩ = (1)(1) + (1)(−1) + (1)(1) + (−1)(−1) + (1)(−1) + (−1)(1)
              =  1  −  1  +  1  +  1  −  1  −  1
              =  0          OK, ORTOGONALES

   Ahora, decodificando con c2', la contribución del emisor 1
   desaparece EXACTAMENTE y la del emisor 2 sigue dando +6:
        d2_reconstruido = 6/6 = 1     OK
```

**El resumen, en tres frases para copiar en el examen:**
1. La salida de un emisor CDMA es el producto, chip a chip, del bit de dato por su código: `Z_(i,m) = d_i · c_m`.
2. El canal es **aditivo**: todos los emisores se suman y el receptor ve una sola señal.
3. Cada receptor recupera sus datos **multiplicando por su propio código**; para que la señal de los otros emisores desaparezca, los códigos deben ser **ortogonales**.

> **Errores típicos:** usar `0` y `1` en vez de `+1` y `−1` (con `d = 0` la salida sería todo ceros y no distinguirías "mandó un 0" de "no mandó nada"); olvidar el factor `1/M` (sin normalizar obtenés `6` o `−6`, no `1` o `−1`); y confundir el código del emisor con la tasa de chips (el código tiene que ser **ortogonal con todos los demás** de la célula, y eso es lo que asigna la estación base).

## 2.7 Ejercicio 7 — ¿Por qué Ethernet conmutada no usa ALOHA?

**Enunciado (inventado).** En un laboratorio hay un switch de 24 puertos 100BASE-TX y ocho PCs. (a) ¿Cuál es el ancho de banda agregado del que disponen las ocho máquinas? (b) ¿Y si las ocho se conectan a un hub de 8 puertos? (c) Explicá por qué CSMA/CD es imprescindible en (b) y no aporta nada en (a).

**(a) Con switch.** Cada puerto es un dominio de colisión **separado**, y en 100BASE-TX el modo por defecto es **full-duplex**.

```
   8 puertos x 100 Mb/s = 800 Mb/s de suma agregada en un sentido
   (y otros 800 Mb/s en el sentido contrario: son enlaces
    independientes, no un bus de 800).

   Limite real: el uplink al resto de la red. Si es 1 GbE,
   topa en 1000; si es 100BASE-TX, topa en 100.
```

**Respuesta: `8 × 100 = 800 Mb/s` agregados, o sea 100 Mb/s dedicados por máquina.**

**(b) Con hub.** El hub es de capa 1: repite la señal a **todos** los puertos. Las ocho máquinas comparten un único medio de 100 Mb/s. El reparto ideal (sin colisiones) sería `100 / 8 = 12,5 Mb/s` por máquina, pero eso es teórico. Hagamos una estimación con el **mejor caso posible**: un medio ranurado, que es el techo del carrier sense.

```
   k = 8 estaciones, Slotted ALOHA (que es el techo):
      p* = 1/(2k − 1) = 1/15 = 0,0667
      S  = p · (1−p)^(2(k−1)) = 0,0667 · (0,9333)^14
      (0,9333)^14 = e^(14 · ln 0,9333) = e^(14 · (−0,06899))
                 = e^(−0,9659) = 0,3807
      S  = 0,0667 · 0,3807 = 0,0254  ->  2,54 %

   100 Mb/s x 0,0254 = 2,54 Mb/s   <- alcanzable en el mejor
                                         caso teórico
```

**Respuesta: 100 Mb/s totales, y en la práctica bastante menos que los 12,5 Mb/s ideales por máquina.**

**(c) Por qué CSMA/CD sí en (b) y no en (a).** En (b) las ocho estaciones comparten un medio físico: dos pueden transmitir en el mismo instante y sus señales se suman en el cable. **Sin el mecanismo de CD no hay forma de detectar el choque**, y esperar un ACK es cien veces más lento. En (a) no hay nada que detectar, porque **no existe medio compartido**:

```
   Enlace H1 <-> switch, full-duplex:

   H1 ----------->  (una direccion)
   H1 <-----------  (la otra direccion)

   H1 transmite: su señal va SOLO al switch.
   El switch transmite al mismo tiempo: su señal va SOLO a H1.

   Los dos flujos usan caminos FISICOS DISTINTOS y en
   direcciones opuestas. No se superponen. No hay colisión.
   CSMA/CD seria codigo muerto.
```

**Y por qué no es "el switch learning lo impide":** el *self-learning* resuelve un problema **distinto**: decidir **a qué puertos** reenviar una trama.

```
   Flooding  !=  colision

   Flooding:   la MISMA trama sale por muchos puertos, UNA DESPUES
               DE OTRA. En el medio hay una sola señal a la vez.
               Nadie choca con nadie.

   Colisión:   DOS tramas de fuentes distintas se superponen en
               UN MISMO medio en el MISMO instante.
```

El switch learning no evita colisiones; **el switch evita que exista un medio compartido**. Son dos afirmaciones distintas y la segunda es la que hay que argumentar.

**El contraejemplo, que es lo que hay que saber decir:**

```
   Switch --- hub --- H1
               |
               +--- H2      <- aca SI hay colision,
               +--- H3          y SI hace falta CSMA/CD
               +--- H4

   El hub crea un dominio de colisión por debajo del switch.
   CSMA/CD no desaparece: se traslada al segmento del hub.
   Ese es el motivo por el que la solución del examen 2010-07
   dice "si alguna computadora trabaja en modo half-duplex,
   si, en esa conexión computadora-switch se utilizará
   CSMA/CD".
```

---

# PARTE 3 — PROBLEMAS DE EXAMEN DE FING

## 3.1 ⭐ Examen 2007-07, Pregunta 3 (10 puntos) — el problema central de la clase

> **Fuente:** Examen `sirc0707` / `eirc0707`, Pregunta 3, 31 de julio de 2007.
> **Link:** https://www.fing.edu.uy/inco/cursos/redescomp/examenes/sirc0707.pdf

### Enunciado (texto literal del examen)

> **Pregunta 3 (10 puntos)**
>
> a) Indique cual es la diferencia de performance entre ALOHA и Slotted-ALOHA en el caso de carga normal. Justifique.
>
> b) Que tipos de protocolos CSMA hay. Describa cual es la diferencia entre ellos.

> ⚠️ **Nota sobre la solución oficial:** el PDF publicado de `sirc0707` **no incluye solución para las preguntas teóricas** (solo trae la de los Problemas 1 y 2). Las dos partes que siguen están desarrolladas por mí, a partir de la derivación de la Parte 2, y se marcan **(solución propia)**. Lo que se corrige es el razonamiento, no una fórmula oficial.

### Parte a) — la diferencia de rendimiento

**Respuesta corta, la que hay que escribir primero:**

> Slotted-ALOHA tiene el **doble de rendimiento** que ALOHA puro: su eficiencia máxima es `1/e ≈ 36,8 %` contra `1/(2e) ≈ 18,4 %` de ALOHA puro.

**Justificación completa.** El razonamiento tiene tres pasos y conviene hacer los tres:

**Paso 1 — Qué significa "carga normal".** La red ofrece tramas a una **tasa constante e independiente** (proceso de Poisson), que es el supuesto estándar. Si la tasa es `λ` y la trama dura `T`, la carga ofrecida es `G = λ·T`.

**Paso 2 — La ventana de colisión, que es donde está toda la diferencia.**

```
   ALOHA PURO
   ──────────
   Yo transmito de t = 0 a t = T.

   Cualquier trama que llegue a t entre 0 y 2T me destruye:
     · de 0 a T    -> se solapa por detrás
     · de T a 2T   -> se solapa por delante (mi frente todavía viaja)
   ─────────────────────────────────────────────────────────────
   VENTANA = 2T


   SLOTTED-ALOHA
   ─────────────
   Solo puedo empezar en t = 0, T, 2T, ...

   Dos tramas que empiecen en ranuras distintas NO pueden solaparse.
   La única colisión posible es empezar en la MISMA ranura.
   ─────────────────────────────────────────────────────────────
   VENTANA = T
```

**Paso 3 — La cuenta.**

```
   Probabilidad de que llegue una trama durante una ventana de W
   segundos, siendo lambda la tasa de arribos:
       numero medio de arribos = lambda · W
       P(ninguno)              = e^(−lambda · W)

   ALOHA puro   (W = 2T):
       P(sobrevive) = e^(−lambda · 2T) = e^(−2G)
       eficiencia  S = G · e^(−2G)
       dS/dG = 0  -->  G* = 1/2
       S_max = (1/2)·e^(−1) = 1/(2e) = 0,184

   Slotted      (W = T):
       P(sobrevive) = e^(−lambda · T) = e^(−G)
       eficiencia  S = G · e^(−G)
       dS/dG = 0  -->  G* = 1
       S_max = 1 · e^(−1) = 1/e = 0,368
```

**La respuesta "por qué exactamente el doble", que es lo que el "Justifique" está pidiendo:**

```
   La ventana se redujo a la mitad (de 2T a T), así que para la
   misma carga G la probabilidad de sobrevivir pasó de e^(−2G)
   a e^(−G): un factor e a favor. Pero además la carga que
   maximiza el rendimiento se duplicó (G* pasó de 1/2 a 1),
   y eso aporta otro factor 2:

       S_slotted(1)  /  S_puro(1/2)  =  1·e^(−1)  /  (0,5·e^(−1))
                                    =  2
```

**Consecuencia práctica:** ALOHA puro **nunca puede pasar del 18,4 % de la capacidad del medio**, por más vacía que esté la red. Slotted-ALOHA llega al 36,8 %. Ninguno de los dos es aceptable en producción, y esa es exactamente la razón por la que Ethernet no usa ALOHA: usa **carrier sense**, que elimina casi todas las colisiones salvo las de duración `ε` (§1.6.1).

| | ALOHA puro | Slotted-ALOHA |
|---|---|---|
| Cuándo se puede transmitir | en cualquier instante | **solo al comienzo de una ranura** |
| Sincronización | ninguna | reloj común o preámbulo |
| Ventana vulnerable | `2T` | `T` |
| Probabilidad de sobrevivencia | `e^(−2G)` | `e^(−G)` |
| Carga óptima `G*` | 0,5 | 1 |
| **Eficiencia máxima** | **`1/(2e)` = 0,184** | **`1/e` = 0,368** |
| Tramas por segundo a 10 Mb/s con 64 B | 14 680 | 29 360 |

### Parte b) — los tipos de CSMA y sus diferencias *(solución propia)*

**Respuesta corta:** hay dos ejes de clasificación, **persistencia** y **detección de colisión**, que dan **cuatro combinaciones**.

**Eje 1 — ¿Qué hace la estación mientras encuentra el medio ocupado?**

| Tipo | Comportamiento | Ventaja | Desventaja |
|---|---|---|---|
| **1-persistente** | espera mirando; transmite en cuanto el medio queda libre | no desperdicia medio libre | varias que esperaban transmiten a la vez, y hay colisión |
| **No persistente** | espera un tiempo **aleatorio** y vuelve a escuchar | casi no hay colisiones | regala ancho de banda: el medio puede quedar libre sin que nadie transmita |
| **p-persistente** (medios ranurados) | transmite con prob. `p`, con prob. `1−p` espera una ranura | compromiso continuo | parametrizable pero en desuso |

**Eje 2 — ¿Qué hace la estación cuando hay colisión?**

| Tipo | Comportamiento | Consecuencia |
|---|---|---|
| **Sin detección** | espera a que el medio se libere y reintenta | cada colisión cuesta un **ACK** completo, o sea un RTT entero |
| **Con detección** | aborta la trama, emite **jamming** y hace **backoff exponencial** | la colisión se detecta en microsegundos y solo se pierde lo transmitido |

| | **Sin detección** | **Con detección** |
|---|---|---|
| **1-persistente** | 1-persistent CSMA | **CSMA/CD** — Ethernet por cable |
| **No persistente** | non-persistent CSMA | CSMA/CD no persistente — no se usa en la práctica |

**La diferencia de fondo entre "con detección" y "sin detección"** (la frase que más puntos vale):

> En un medio **cableado**, la tarjeta puede **escuchar mientras transmite** y comparar lo que manda con lo que vuelve: si no coinciden, hubo colisión. Eso es **detección directa**, y cuesta microsegundos.
>
> En un medio donde **no** se puede escuchar mientras se transmite (radio), o donde **las estaciones no se escuchan entre sí** (estación oculta), no hay detección directa. La única forma de enterarse es **no recibir el ACK**: detección **indirecta**, por ausencia, que cuesta un RTT entero.
>
> Esa es la razón de que exista **CSMA/CD** para el cable y **CSMA/CA** para wireless: cuando no podés **detectar** la colisión, tenés que **evitarla**, y eso se hace haciendo que los demás se callen (RTS/CTS, NAV y ACK obligatorio en 802.11).

**Para cerrar:** en la práctica, la Ethernet conmutada full-duplex **no usa ninguno de los dos**, porque no hay colisión posible (§3.2). Y en los medios cableados compartidos la combinación que se usa es **1-persistente con detección**: persistencia 1 porque el medio es rápido y no conviene regalarlo, y detección porque el cable la permite.

## 3.2 ⭐ Examen 2010-07, Pregunta 2 (8 puntos) — CSMA/CD en wireless y en Ethernet conmutada

> **Fuente:** Examen `sirc1007` / `eirc1007`, Pregunta 2, 27 de julio de 2010.
> **Link:** https://www.fing.edu.uy/inco/cursos/redescomp/examenes/sirc1007.pdf

### Enunciado (texto literal del examen)

> **Pregunta 2 (8 puntos)**
>
> a) ¿Es recomendable utilizar CSMA/CD en una red wireless 802.11? Justifique.
>
> b) En un medio Ethernet completamente switcheado, ¿es necesario utilizar CSMA/CD? Justifique su respuesta.

### Parte a) — ¿CSMA/CD en una red wireless 802.11?

**Solución oficial (del PDF):**

> a) No, pues CSMA/CD está especificado tal que aun en el peor caso, o sea, una estación transmitiendo la trama más corta permitida y destinada a la estación más alejada "en el cable" y ésta comenzando a transmitir un tiempo epsilon arbitrariamente pequeño y positivo antes que llegue el primer bit de la trama, comience también a transmitir, todas las estaciones se enteran de la colisión. En el caso de redes wireless 802.11 existen varios casos, y no necesariamente "extremos" en los que no podemos asegurar que todas las estaciones se escuchen entre sí, detectando así las colisiones que pudiesen ocurrir al transmitir dos o más estaciones pertenecientes a la misma BSS con un solapamiento al menos parcial en el tiempo. Un ejemplo "clásico" es "el problema de la estación oculta".

**Análisis de la solución oficial.** El razonamiento es correcto y muy bien elegido por la cátedra: reconstruye el **peor caso** de CSMA/CD (la estación más lejana empezando un `ε` antes de que llegue el primer bit) y muestra que **en un medio cableado ese peor caso está garantizado por la geometría**, mientras que en 802.11 **no existe tal extremo**: hay pares de estaciones que no se escuchan entre sí.

**Lo que yo le agrego** (argumentos distintos y complementarios; sumarlos sube el puntaje):

1. **Es físicamente imposible, no solo poco confiable.** La solución oficial razona sobre la **alcancibilidad** de la señal. El argumento más fuerte es de otra naturaleza: **una radio no puede recibir en la misma banda mientras transmite**. Su propia señal llega al frente del receptor con unos 20 dBm (100 mW); una señal co-canal de una estación vecina llega típicamente con −70 dBm. La diferencia es de **90 dB, es decir cerca de un millón de veces en potencia**, y el receptor no tiene forma de separar lo que él mismo emite de lo que entra del canal. **No es que el protocolo sea malo: es que la física lo impide.**
2. **CSMA/CD necesita un tiempo de ida y vuelta acotado, y la radio no lo tiene.** La corrección de CSMA/CD depende de que la trama mínima sea **más larga que el tiempo de ida y vuelta del medio** (§1.8). En un cable ese tiempo está fijado por el largo máximo del segmento: por eso el estándar puede declarar "la trama mínima son 512 bits". En radio hay movilidad, fading, estaciones ocultas, y el presupuesto de tiempo no tiene un mínimo razonable: **la trama mínima tendría que ser gigantesca y el rendimiento se iría a cero**. En resumen, **la condición que hace funcionar a CSMA/CD no es verificable en radio**.
3. **El modelo de costo está invertido.** En CSMA/CD el emisor aborta al detectar, así que la energía desperdiciada es **una fracción de trama**. En wireless el único que puede juzgar la integridad de la trama es **el receptor** (por el CRC), así que el emisor tiene que **transmitir la trama entera** para enterarse. Si vas a transmitir entera de todos modos, **evitarla es infinitamente mejor que detectarla**. De ahí el nombre: CSMA/**CA**.
4. **El sentido de portadora sí funciona, la detección no.** Matiz importante: en 802.11 una estación **sí puede** escuchar el medio antes de transmitir (carrier sense). Lo que no puede es **detectar una colisión mientras transmite**. Por eso 802.11 conserva el "CSMA" y cambia el "CD" por "CA": **RTS/CTS y NAV** para silenciar a las estaciones vecinas, **backoff exponencial** para las colisiones que igual ocurren, y **ACK obligatorio**.

**Respuesta redactada para el examen:**

> No es recomendable, y en la práctica es imposible.
>
> **Primero**, porque una radio es half-duplex por naturaleza: no puede recibir en la misma banda mientras transmite, y su propia señal (unos 20 dBm) enmascara por cerca de 90 dB cualquier transmisión ajena. La detección de colisión durante la transmisión es físicamente inviable.
>
> **Segundo**, porque CSMA/CD garantiza la detección en el peor caso gracias a que en un medio cableado toda estación que recibe la señal de otra necesariamente está en el mismo medio, y a que el tiempo de ida y vuelta está acotado por el largo máximo del segmento (de ahí los 512 bits de trama mínima). En 802.11 ninguna de las dos condiciones se cumple: la estación oculta rompe la simetría de cobertura, y no hay cota de propagación utilizable.
>
> **Tercero**, porque en radio el emisor no puede juzgar la colisión: solo el receptor puede, por CRC, con lo cual hay que enviar la trama entera para enterarse. Detectar sería tirar la trama a la basura después de gastarla.
>
> **Por eso 802.11 usa CSMA/CA**: en lugar de detectar la colisión, la evita. Hace RTS/CTS para que las estaciones vecinas asignen un NAV y se callen, espera un backoff exponencial aleatorio, y exige un ACK del receptor. El sentido de portadora sí se conserva: lo que no se puede es la detección.

### Parte b) — ¿CSMA/CD en una Ethernet completamente switcheada?

**Solución oficial (del PDF):**

> b) Si hablamos de un medio completamente switcheado (sin presencia de hubs) y por lo tanto una sola computadora por puerto de switch y si asumimos que todos los puertos de los switches así como las tarjetas de red de las computadoras conectadas a ellas están configuradas para trabajar en modo full-duplex, no es necesario utilizar CSMA/CD. Si alguna computadora trabaja en modo half-duplex, sí, en esa conexión "computadora-switch" se utilizará CSMA/CD.

**Análisis de la solución oficial.** Es correcta y además es cuidadosa: **no dice "no es necesario", dice "no es necesario *si y solo si* se cumplen dos condiciones** — (1) no hay hubs, una máquina por puerto; y (2) todo en full-duplex. Y cierra con el matiz que muchos alumnos se pierden: **si una máquina queda en half-duplex, CSMA/CD vuelve**. Esa última frase es la que hay que repetir.

**Mi desarrollo — por qué no hay colisión, y por qué no es "porque el switch lo impide".**

El error más común es decir *"el switch no deja que se colisionen"*. Eso mezcla dos mecanismos distintos. La respuesta correcta tiene cuatro pasos:

**Paso 1 — Qué es una colisión.** Dos señales que se superponen **en el mismo medio físico en el mismo instante**. La definición ya dice "mismo medio". Si no hay medio compartido, no hay definición aplicable.

**Paso 2 — Qué hace el full-duplex.** En un enlace punto a punto full-duplex, cada sentido es un camino físico independiente:

```
   H1 ======>  switch     (dirección A: de la estación al switch)
   H1 <=====  switch     (dirección B: del switch a la estación)

   Son dos medios separados. H1 y H2 no comparten NADA:
   H1 transmite hacia el switch por el par 1-2 del cable de H1,
   H2 transmite hacia el switch por el par 1-2 del cable de H2.

   Que las señales lleguen al switch al mismo instante NO es
   una colisión: el switch tiene un puerto de entrada distinto
   para cada una. Lo que hay es COLA, que es otro problema
   (control de flujo, capa 2), y se resuelve con buffers.
```

**Paso 3 — Conclusión.** En un enlace full-duplex punto a punto, cada estación tiene **un dominio de colisión de tamaño 1**: ella sola. La colisión **no es improbable ni rara: es geométricamente imposible**, porque requeriría que dos señales compartieran un medio, y no hay medio compartido. **CSMA/CD sería código muerto**: la máquina escucharía, compararía su señal con la que vuelve, concluiría eternamente que "todo bien", y esperaría una colisión que no puede ocurrir.

**Paso 4 — qué papel juega el switch learning.** El *self-learning* resuelve un problema **distinto**: **decidir a qué puertos reenviar cada trama**.

```
   Flooding (dominio de BROADCAST, no de colisión):
   la MISMA trama sale por varios puertos, UNA DESPUES DE OTRA.
   En cada instante hay una sola señal en el medio. Nadie choca.

   Colisión (dominio de COLISIÓN):
   DOS tramas de fuentes distintas, superpuestas en un medio
   compartido, en el MISMO instante.

   +-----------------------------------------------------+
   | flooding  = desperdicio de tiempo                     |
   | colisión  = simultaneidad en un medio compartido     |
   | Son ejes distintos y NO se pueden confundir.          |
   +-----------------------------------------------------+
```

El learning evita el flooding de unicast (que desperdicia ancho de banda), pero **no tiene absolutamente nada que ver con las colisiones**. Decir "el switch evita las colisiones" es correcto solo en el sentido indirecto de que **elimina el medio compartido**; dicho así, es impreciso y el corrector lo va a marcar.

**Respuesta redactada para el examen:**

> No es necesario. **Porque no hay colisión posible, y no porque el switch la impida.** Una colisión exige que dos señales se superpongan en un mismo medio físico en el mismo instante. En una Ethernet conmutada full-duplex, cada enlace es punto a punto y cada sentido es un camino independiente, así que cada puerto es un dominio de colisión de tamaño 1 y la colisión es geométrically imposible.
>
> **El self-learning resuelve otro problema**: decidir a qué puertos reenviar cada trama. Sin él, las tramas unicast de destino desconocido se inundarían por todos los puertos. Eso es *flooding*, la misma trama saliendo por varios puertos uno después de otro: un desperdicio de ancho de banda, **no una colisión**, que exige simultaneidad sobre un medio compartido. Confundir ambos conceptos es el error típico de esta pregunta.
>
> **Condiciones y contraejemplo:** el resultado vale bajo las dos hipótesis de la solución oficial: una sola máquina por puerto (sin hubs) y todo en full-duplex. Si hay un hub debajo del switch, ese tramo vuelve a ser un único dominio de colisión compartido y el CSMA/CD regresa ahí. Y si una sola tarjeta queda en half-duplex, en ese enlace específico se usa CSMA/CD, con colisiones tardías (*late collisions*) que aparecen a los 512 tiempos de bit de la trama mínima.

## 3.3 Examen 2007-02, Pregunta 1 (5 puntos) — Pure ALOHA, Slotted ALOHA y CSMA/CD

> **Fuente:** Examen `eirc0702`, Pregunta 1, febrero de 2007.
> **Enunciado:** "Que diferencias tienen Pure ALOHA, Slotted ALOHA y CSMA/CD."

Es la pregunta comparativa clásica y es casi un resumen de la clase:

| | **Pure ALOHA** | **Slotted ALOHA** | **CSMA/CD** |
|---|---|---|---|
| **Escucha el medio antes de transmitir** | no | no | **sí** |
| **Cuándo puede empezar** | en cualquier instante | **solo al inicio de una ranura** | en cuanto el medio está libre |
| **Sincronización** | ninguna | reloj común | ninguna |
| **Ventana de colisión** | `2T` | `T` | `ε` (prácticamente cero) |
| **Detecta la colisión** | no (por ausencia de ACK) | no (por ausencia de ACK) | **sí, durante la transmisión** |
| **Reacción** | retransmitir al azar tras esperar | retransmitir al azar tras esperar | **abortar, jamming y backoff exponencial** |
| **Reintentos** | al azar, sin cota | al azar, sin cota | exponencial, **tope 16** |
| **Hardware especial** | ninguno | reloj | **tarjeta que escucha mientras transmite** |
| **Eficiencia máxima** | `1/(2e)` = 18,4 % | `1/e` = 36,8 % | cercana al 100 % a baja carga |
| **Medio típico** | satélite (ALOHAnet) | sistemas ranurados | coaxil y par trenzado de Ethernet |

**La frase de síntesis (2 puntos fáciles):** la evolución de los tres es **"cada uno le agrega una pieza al anterior"**. A Slotted se le agrega un reloj, que reduce la ventana de `2T` a `T` y duplica el rendimiento. A CSMA/CD se le agrega el sentido de portadora, que elimina la ventana casi por completo (de `T` a `ε`), y la detección en línea, que hace que la colisión cueste microsegundos en vez de un RTT. **CSMA/CD no es "otro ALOHA": es ALOHA con los sentidos y los oídos puestos.**

## 3.4 Examen 2010-12, Pregunta 3 a) y b) (8 puntos) — dominios de colisión y de broadcast

> **Fuente:** Examen `sirc1012`, Pregunta 3, diciembre de 2010.
> *(El apartado c), el de self-learning, es de la Clase 42 y no se resuelve acá.)*
> **Enunciado:** "a) Considere una red de varios nodos interconectados por un hub, ¿cuál es el dominio de colisión y cuál es el de broadcast? Justifique. b) Si en la red anterior cambiamos el hub por un switch. ¿Se modifican los dominios de colisión y broadcast? ¿De qué manera?"

**a) Con hub: los dos dominios son iguales y abarcan toda la red.** El hub es un dispositivo de **capa 1**: no implementa ningún protocolo de acceso al medio, no aprende direcciones y no decide nada, se limita a repetir la señal eléctrica por todos los puertos. Como todos los puertos comparten el mismo medio físico, las señales de todas las estaciones se superponen (**un único dominio de colisión**); y como todo se reenvía por todos los puertos, toda trama de broadcast o de destino desconocido llega a todos (**un único dominio de broadcast**).

**b) Con switch: el dominio de colisión se parte en uno por puerto; el de broadcast no cambia.**

| | Con hub | Con switch |
|---|---|---|
| **Dominio de colisión** | uno, con todos los nodos | **uno por puerto**; con full-duplex, de tamaño 1 |
| **Dominio de broadcast** | uno, con todos los nodos | **uno, igual**: el switch reenvía las tramas de broadcast por todos los puertos |

**Por qué se parte el de colisión.** El switch es de **capa 2**: aprende direcciones MAC y decide a qué puerto reenviar cada trama. Al hacerlo, **elimina el medio compartido** y lo reemplaza por enlaces punto a punto independientes. Cada puerto es un medio físico propio, con sus dos emisores (la estación y la tarjeta del switch). Por lo tanto **cada puerto es un dominio de colisión**, y las colisiones solo pueden ocurrir entre la estación conectada a ese puerto y el switch.

**Por qué el de broadcast NO cambia.** Una trama de broadcast tiene destino `FF:FF:FF:FF:FF:FF`: **por definición todos tienen que oírla**. El switch no tiene información para descartarla, así que la reenvía por **todos los puertos del mismo dominio de broadcast**. Lo único que acota ese dominio son las **VLAN** (Clase 42): una etiqueta 802.1Q crea dominios de broadcast lógicos independientes dentro del mismo switch.

```
   +------------------------------------------------------+
   |  LA FRASE QUE HAY QUE DECIR                         |
   |                                                      |
   |  El switch parte el DOMINIO DE COLISION porque        |
   |  elimina el medio compartido.                         |
   |                                                      |
   |  El switch NO parte el DOMINIO DE BROADCAST porque    |
   |  no puede descartar una trama que es por definicion   |
   |  para todos.                                          |
   +------------------------------------------------------+
```

> **Nota sobre la solución oficial de 2010-12:** la cátedra escribe "el switch impediría que ocurran colisiones". Como discutimos en §3.2, esa redacción es **imprecisa**: el switch no *impide* colisiones, **elimina la condición que las hace posibles** (el medio compartido). En una red con hubs colgados del switch **sí hay colisiones**. La respuesta correcta es "un dominio de colisión por puerto", que es lo que dice también la solución oficial de `2010-07`.

## 3.5 Examen 2007-03, Pregunta 5 (5 puntos) — CSMA/CA

> **Fuente:** Examen `sirc0703`, Pregunta 5, marzo de 2007.
> **Enunciado:** "Describa el mecanismo de acceso al medio CSMA/CA (Carrier Sense Multiple Access With Collission Avoidance)."

**Solución oficial (del PDF), extractada:**

> Uno de los primeros protocolos diseñados para LAN inalámbricas fue CSMA/CA o MACA. La idea es que el emisor estimula al receptor enviando una trama corta, de forma que las estaciones cercanas puedan detectar la transmisión y evitar transmitir durante el envío de una trama de datos. [...] Considere que A quiere enviar una trama a B: comienza enviando una trama del tipo RTS a B, esta trama corta contiene el largo de la trama que sigue. Luego B responde con una trama CTS. [...] Cualquier estación escuchando un RTS está cercana a A y no debe enviar datos para que A reciba el CTS sin interferencia. Cualquier estación cercana a B no debe enviar datos para que A pueda realizar el envío de datos sin interferencia.

**Análisis de la solución oficial.** Está impecable y es exactamente lo que hay que saber:

1. **RTS/CTS es el corazón**: A avisa, B confirma, y ambos anuncian la **duración** de la transferencia siguiente.
2. **La asimetría del aviso es la clave**: el RTS lo oyen las estaciones **cerca de A**; el CTS lo oyen las estaciones **cerca de B**. Cada grupo silencia a su lado.
3. **El NAV**: una estación que escucha el RTS pero no el CTS **igual deduce que hay un envío en curso** y se calla el tiempo anunciado en el RTS. Ese temporizador virtual es el **NAV** (*Network Allocation Vector*), un "sentido de portadora virtual".
4. **Los dos casos que la solución menciona y que valen puntos extra**: (a) una estación C que escucha el RTS pero no el CTS y que gracias al NAV se calla; (b) **dos estaciones que envían RTS al mismo tiempo al mismo receptor**, colisión inevitable que se resuelve con el backoff aleatorio.
5. **MACA y CSMA/CA no son lo mismo**: MACA (1978) es el antepasado; 802.11 lo extendió con el ACK obligatorio y los espacios entre tramas.

**Lo que le agrego** (la Clase 43 lo desarrolla en detalle): los **IFS** (SIFS, DIFS, EIFS) que dan prioridad a las tramas de control sobre las de datos —con `SIFS = 10 µs` y `DIFS = SIFS + 2 × aSlotTime` en las PHY OFDM— y la **ventana de backoff** `CW` de 802.11, que va de `CWmin = 15` a `CWmax = 1023` en pasos `CW = 2^n − 1` con `n` de 4 a 10. O sea: **la misma idea exponencial que en CSMA/CD**, con el rango `[0, CW]` en vez de `[0, 2^k − 1]`.

---

# PARTE 4 — CIERRE

## 📌 Resumen

1. **Medio compartido** = un solo medio para varios. Si dos transmiten a la vez, las señales se **superponen** y nadie recibe nada: **colisión**.
2. **ALOHA puro**: transmite de inmediato. Ventana vulnerable de **`2T`**. Eficiencia `G·e^(−2G)`, máximo en `G = 1/2`, valor **`1/(2e) ≈ 18,4 %`**.
3. **Slotted-ALOHA**: solo al inicio de una ranura. La ventana cae a **`T`**, la supervivencia se multiplica por `e`, la carga óptima se duplica, y el resultado es **`1/e ≈ 36,8 %`**: **exactamente el doble**.
4. **ALOHA con franjas**: `S(N,p) = N·p·(1−p)^(N−1)`, máximo en **`p = 1/N`**, valor `(1−1/N)^(N−1)` que **tiende a `1/e`** cuando `N` tiende a infinito.
5. **CSMA = escuchar antes de hablar.** Elimina todas las colisiones salvo las que caen dentro de una ventana `ε`, porque el sentido de portadora **siempre** tiene un retraso.
6. **Persistencia:** **1-persistente** no desperdicia medio libre (Ethernet); **no persistente** casi no colisiona pero regala ancho de banda; **p-persistente**, un compromiso, no se usa.
7. **Detección:** **con detección** (CSMA/CD) solo es posible en cable, porque la tarjeta escucha mientras transmite; **sin detección**, la colisión se detecta por la **ausencia de ACK** y cuesta un RTT entero.
8. **CSMA/CD**: 1-persistente, detección, **jamming de 32 bits**, **backoff exponencial `r ∈ [0, 2^k − 1]`** y tope de **16 intentos**. En radio no se puede: de ahí **CSMA/CA** (RTS/CTS, NAV, ACK obligatorio).
9. **Slot time = 512 bits**, y la **trama mínima = 64 bytes** porque es exactamente el tiempo de ida y vuelta de la señal en el peor caso. A 10 Mb/s son 51,2 µs; a 1 Gb/s, 0,512 µs, insuficiente para 100 m: de ahí la extensión de portadora.
10. **Con switch full-duplex no hay colisión** porque **no hay medio compartido** (no porque el switch la "impida"), y el **dominio de broadcast sigue siendo toda la red** hasta que una VLAN lo parta.

## ✅ Autoevaluación

**Respondé sin mirar. Las respuestas están en `<details>`.**

**1.** ¿Por qué la ventana de colisión del ALOHA puro mide `2T` y no `T`? Dibujá el caso de una trama que empieza justo después de que terminó la tuya.

<details><summary>Respuesta</summary>

Porque hay **dos** formas de solaparse. Si otra trama empieza **antes** de que termine la mía, se pisa con mi parte final. Si empieza **después**, se pisa con la parte inicial, porque **lo que yo emití al comienzo todavía está viajando por el cable**: en un cable la propagación no es instantánea, así que el principio de mi trama sigue en el medio durante `T` segundos más.

</details>

**2.** Slotted-ALOHA duplica exactamente el rendimiento de ALOHA puro. Demostralo con las fórmulas.

<details><summary>Respuesta</summary>

ALOHA puro: `S = G·e^(−2G)`, máximo en `G = 1/2`, valor `(1/2)·e^(−1)`.
Slotted: `S = G·e^(−G)`, máximo en `G = 1`, valor `1·e^(−1)`.

La razón es `1·e^(−1) / ((1/2)·e^(−1)) = 2`. Cancelan las dos contribuciones: la reducción de la ventana de `2T` a `T` multiplica la supervivencia por `e`, y la duplicación de la carga óptima aporta el otro factor 2. Exactamente 2, sin aproximaciones.

</details>

**3.** ¿Qué valor de `p` maximiza `N·p·(1−p)^(N−1)`? Mostrá la derivación.

<details><summary>Respuesta</summary>

`p = 1/N`. Se obtiene derivando y despejando:

```
   S' = N·(1−p)^(N−2)·[(1−p) − p(N−1)] = 0
   (1−p) = p(N−1)   -->   1 − p = pN − p   -->   1 = pN   -->   p = 1/N
```

Y es un máximo porque `S(0) = 0` y `S(1) = 0` (para `N > 1`), de modo que el único punto crítico tiene que ser el máximo.

</details>

**4.** ¿Por qué el emisor tiene que seguir enviando bits después de detectar una colisión? ¿Qué son esos 32 bits?

<details><summary>Respuesta</summary>

Porque tiene que **sellar** la colisión en el medio. Son los **32 bits de jamming**: una ráfaga de ruido deliberada. Si la tarjeta simplemente cortara la transmisión, las estaciones que están más lejos del cable podrían no haberse enterado todavía de que el medio estaba ocupado y podrían meterse en el slot siguiente. El jamming garantiza que todas las estaciones del segmento registren el evento como "medio ocupado con trama inválida", antes de que empiece el próximo slot time.

</details>

**5.** ¿De dónde sale el número 512 del slot time, y por qué el mismo número sirve a 10, 100 y 1000 Mb/s?

<details><summary>Respuesta</summary>

De la condición de que la trama mínima debe durar al menos lo que tarda la señal en **ir y volver** del extremo más lejano del segmento, para que el indicio de colisión vuelva antes de que termine la trama. Como esa condición se expresa en **tiempos de bit** y no en segundos, el número es el mismo a todas las velocidades: **512 tiempos de bit**. Lo que cambia es el tiempo absoluto: 51,2 µs a 10 Mb/s, 5,12 µs a 100 Mb/s, 0,512 µs a 1 Gb/s. Y por eso a 1 Gb/s 512 bits ya no alcanzan para los 100 m del cable: de ahí la extensión de portadora a 4096 tiempos de bit.

</details>

**6.** En Ethernet conmutada full-duplex, ¿por qué no hay colisiones? ¿Tiene algo que ver con que el switch aprenda direcciones?

<details><summary>Respuesta</summary>

No tiene colisiones porque **no hay medio compartido**: cada enlace es punto a punto y cada sentido es un camino físico independiente, así que cada puerto es un dominio de colisión de tamaño 1 y la colisión es geométricamente imposible.

El self-learning **no tiene nada que ver**: resuelve el problema de **a qué puertos reenviar la trama**. Sin él, los unicast de destino desconocido se inundarían por todos los puertos. Eso es *flooding*, un desperdicio de ancho de banda, **no una colisión** (que exige simultaneidad sobre un medio compartido).

</details>

**7.** ¿Por qué no se puede usar CSMA/CD en 802.11? Dá **dos** razones que no sean la misma.

<details><summary>Respuesta</summary>

(1) **Física**: una radio no puede recibir en la misma banda mientras transmite, y su propia señal (unos 20 dBm) supera en unos 90 dB a cualquier transmisión co-canal. La detección durante la transmisión es inviable, no difícil.

(2) **Geometría y temporal**: CSMA/CD garantiza la detección en el peor caso porque en cable toda estación que recibe la señal de otra está en el mismo medio (se rompería con estación oculta) y porque el tiempo de ida y vuelta tiene cota (fijada por el largo máximo del segmento). En radio ninguna de las dos condiciones se cumple, así que **la condición que hace funcionar a CSMA/CD no es verificable**.

Una tercera: en radio solo el receptor puede juzgar la colisión, por CRC, así que hay que mandar la trama entera para enterarse. Detectar sería tirarla después de gastarla; por eso conviene **evitar**.

</details>

**8.** Un switch tiene un hub conectado en uno de sus puertos, con tres PCs colgando. ¿Dónde hay colisión?

<details><summary>Respuesta</summary>

Solo **debajo del hub**. El hub es de capa 1 y repite la señal a todos sus puertos, así que las tres PCs y el propio switch comparten **un** dominio de colisión. Ahí hace falta CSMA/CD (si el enlace es half-duplex) y ahí es donde aparecen las colisiones tardías.

En el resto de la red, los puertos del switch son dominios de colisión independientes. Y el **dominio de broadcast sigue siendo todo el conjunto**, porque las tramas de broadcast salen por todos los puertos del switch.

</details>

## 🔗 Referencias

- **Examen `sirc0707` / `eirc0707`** — Pregunta 3 (10 pts): rendimiento ALOHA contra Slotted-ALOHA, y tipos de CSMA. **Sin solución oficial publicada** para las preguntas teóricas.
- **Examen `sirc1007` / `eirc1007`** — Pregunta 2 (8 pts): CSMA/CD en wireless y en Ethernet conmutada. Con solución oficial.
- **Examen `eirc0702`** — Pregunta 1 (5 pts): diferencias entre Pure ALOHA, Slotted ALOHA y CSMA/CD.
- **Examen `sirc1012`** — Pregunta 3 (8 pts): dominios de colisión y de broadcast con hub y switch (apartados a y b).
- **Examen `sirc0703`** — Pregunta 5 (5 pts): CSMA/CA y RTS/CTS. · `sirc0807` — Pregunta 3: CSMA/CA en modo infraestructura (Clase 43).
- **Práctico 5 de 2008** — Ejercicios 5 y 6 (CDMA) y ejercicio 8 (eficiencia de ALOHA con franjas).
- **Tanenbaum & Wetherall**, *Redes de computadoras* 5ª ed., cap. 3 y cap. 4 (§4.1, subcapa MAC: ALOHA, Slotted ALOHA, CSMA, Ethernet); cap. 6 y 7 para la discusión de por qué el acceso aleatorio no funciona en radio.
- **Kurose & Ross**, *Computer Networking: A Top-Down Approach* — §5.3 (ALOHA, Slotted ALOHA, CSMA, CSMA/CD) y §5.1.3 (CDMA)
- **IEEE 802.3** — Ethernet: slot time, trama mínima, jamming, backoff binario exponencial, extensión de portadora. **No es una RFC de IETF**: es un estándar del IEEE.
- **IEEE 802.11** — CSMA/CA, DCF, IFS, NAV, RTS/CTS, EDCA.
- **IEEE 802.3cg** — 10BASE-T1S, el único caso industrial donde el half-duplex sigue siendo obligatorio (con PLCA).
- **IEEE 802.1Q-2022**, **802.1w** (RSTP) y **802.1AX-2020** — VLAN, spanning tree y agregación de enlaces (Clase 42).
- **RFC 826** — ARP (request en broadcast, reply en unicast), que es quien sufre el dominio de broadcast.
- **Clase anterior:** 40 — Corrección de errores y ARQ (Hamming, Go-Back-N, Selective Repeat)
- **Clase siguiente:** 42 — Switch, hub, VLAN y STP: self-learning paso a paso, tabla MAC, ageing, STP/RSTP
