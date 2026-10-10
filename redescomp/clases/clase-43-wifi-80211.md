# Clase 43 — Redes inalámbricas 802.11

**Bloque:** E (Enlace) · **Semana:** 15 · **Duración estimada:** 120 min
**Correlativa:** Clase 42 (switch, VLAN, STP) · **Sigue con:** Clase 44 (multimedia)
**Material de referencia:** Tanenbaum cap. 4 · `ACTUALIZACIONES.md` §9

---

## 🎯 Al terminar esta clase vas a poder

1. Explicar por qué una red<Class0> wireless es un problema distinto y por qué en
   ella **no se puede detectar** una colisión.
2. Describir el mecanismo completo del **CSMA/CA** (DCF) paso a paso.
3. Dibujar la **estación oculta** y explicar qué resuelve y qué no resuelve el
   **RTS/CTS**.
4. Explicar qué es el **NAV** y por qué se considera un "segundo sensor" del medio.
5. Comparar las **4 colas de EDCA** y explicar por qué el video no va en la cola de
   voz.
6. Describir el problema de seguridad de **WEP**, qué resuelve WPA3 con **SAE**, y
   qué protege **802.11w**.

> **Prerequisito del examen:** `2008-07 P3` (10 pts — CSMA/CA en modo
> infraestructura), `2006-12 P5` (6 pts — estación oculta), `2007-03 P5` (5 pts —
> CSMA/CA), `2010-07 P2` (8 pts — por qué no CSMA/CD en wireless).

---

# PARTE 1 — TEORÍA

## 1.1 Por qué una red wireless es un problema distinto

En la Clase 41 vimos que **Ethernet cableado** puede usar **CSMA/CD**: detectar
la colisión, abortar, hacer backoff y reintentar. Todo eso funciona porque el
receptor es un **cable**: el que transmite puede **escuchar su propia señal** mientras
transmite, y si oye otra cosa encima, es una colisión.

**En radio ninguna de las tres condiciones se cumple:**

**1. La antena es half-duplex.** Un transceiver de radio **no puede transmitir y
recibir a la vez**. Es como hablar y escuchar al mismo tiempo: no funciona. Y para
detectar una colisión haría falta exactamente eso: hablar y escuchar.

**2. La propia señal enmascera a las demás.** Tu señal llega a la antena a unos
30 dBm (1 vatio). La señal de otro emisor que vuelve por reflexión puede llegar a
−90 dBm. La diferencia es de **120 dB**, que en potencia es un factor de
**10⁶**. Tu propio receptor la ahoga por completo. Detectar la colisión por nivel
de señal es **físicamente imposible** con esta tecnología.

**3. El medio es invisible.** Las ondas se propagan por el aire y **no tienen
frontera**: alguien en la calle, detrás de una pared, transmite en el mismo canal y
vos no lo sabés. En el cable el medio es **punto a punto** y no hay ambigüedad.

> **La conclusión es la clave de toda la clase:** en radio **no se puede DETECTAR
> una colisión**. Entonces el protocolo tiene que hacer lo contrario: **EVITARLA**
> antes de que ocurra. De ahí **A** (*Avoid*) en lugar de **D** (*Detect*).

```
   ETHERNET (cable)                        WI-FI (radio)
   ──────────────                          ──────────────
   CSMA/CD                                  CSMA/CA

   ¿se detectó colisión?                    ¿se puede evitar?
        │                                         │
   SÍ ──┴── NO                              RTS/CTS
        │                                    NAV
   abortar                                 backoff largo
   hacer backoff                           esperar
   reintentar                             oler por el ACK
        │                                         │
   SE DETECTA                                NO SE DETECTA
   la pérdida                                la pérdida
```

## 1.2 Los dos problemas concretos

### La estación oculta (*hidden node*)

```
        ┌───────────────────┐
        │    Router / AP    │
        │        ●          │
        └───┬───────────┬───┘
            │           │
        ┌───┴───┐   ┌───┴───┐
        │   A   │   │   C   │        B más abajo, al
        │       │   │       │        alcance del AP
        └───────┘   └───────┘
                 ╳      │
              se      ┌─┴─┐
            cortan    │ B │    A y C **NO SE VEN**
            entre     └───┘    entre sí: un obstáculo
            ellos
```

**El problema:** A y C están **los dos al alcance del AP**, pero **no se ven entre
sí**. Si A transmite su trama hacia el AP, C **no la escucha**, así que cree que
el medio está libre y **también transmite**. Las dos tramas **chocan en el AP**,
donde de hecho convergen.

> **La analogía correcta:** es una conversación en una sala donde dos personas le
> hablar a alguien al fondo. Ellas no se escuchan entre sí, así que hablan los dos
> al mismo tiempo, y el del fondo entiende la mitad.

**Y el agravante:** el problema **no es** que A y C collagen entre sí (no se
alcanzan). Es que **colisionan en el AP**, que es el punto donde convergen las dos.

**La solución clásica: RTS/CTS** (§1.5). Y la solución moderna: **BSS coloring**,
que agrega un número de color a cada red para que las redes vecinas no se interfieran
sin necesidad de negociar nada (§Actualización).

### La estación expuesta (*exposed terminal*)

El problema inverso, y **RTS/CTS no lo resuelve**:

```
        ┌───────────────────┐
        │    Router / AP    │
        └───┬───────────┬───┘
            │           │
        ┌───┴───┐   ┌───┴───┐
        │   A   │   │   C   │
        └───────┘   └───────┘
           A quiere hablar con B      C quiere hablar con D
           (B está abajo)             (D está en otra parte)

   A y C SÍ se ven entre sí.
   A transmite → C lo oye → C se calla.
   PERO C podría haber transmitido a la vez, sin problema,
   porque C y A van a DESTINOS DISTINTOS.
```

**El punto fino:** la estación expuesta produce una **ineficiencia**, **no una
pérdida**. Y cualquier solución que la arregle (como pedir RTS/CTS para todos los
casos) **empeora** el caso de la estación oculta con más overhead. **Es un
compromiso, y no hay solución limpia.** En un examen, mencionar esto suma.

## 1.3 CSMA/CA: el mecanismo completo (DCF)

DCF = *Distributed Coordination Function*. Es la forma **distribuida** de coordinar
el acceso (no hay punto central que asigne turnos).

### Los 4 espacios inter-trama

Antes de los espacios hay un pequeño **silencio** llamado **SIFS** (*Short Interframe
Space*), que es el más corto. Sirve para las tramas de **control** que tienen que
ir justo después de una de datos, sin que nadie más pueda interrumpir.

```
   ┌───────┬───────┬───────┬───────┐
   │  SIFS │  PIFS │  DIFS │  EIFS │
   ├───────┼───────┼───────┼───────┤
   │ 2μs   │ SIFS+1│ SIFS+2│ SIFS+3│
   │       │       │       │       │
   └───┬───┘   ┌───┘   ┌───┘   ┌───┘
       │       │       │       │
   ACK, CTS,  usado por  se espera  se espera tras
   fragmentos  el punto  ANTES de    un FRAGMENTO
   de un blo-  de acceso  intentar   recibido
   que            transmitir   (exige silencio)
```

| Símbolo | Significado | Uso |
|---|---|---|
| **SIFS** | Short InterFrame Space | respuesta a una trama: **ACK**, **CTS**, fragmentos de un bloque. **Nadie más espera**: es el que garantiza que la respuesta gane el medio. |
| **PIFS** | PCF InterFrame Space | reservado al punto de acceso en modo **puntual** (PCF). Poco usado. |
| **DIFS** | Distributed IFS | lo espera una estación **común** antes de intentar transmitir. |
| **EIFS** | Extended IFS | lo espera una estación que **no entendió** lo que recibió (o recibió un error). Es el más largo: penaliza. |

**El orden importa**: para empezar a transmitir se espera **DIFS**. Para **responder**
se espera **SIFS**, que es **más corto**. Como todas las estaciones usan el mismo
valor de SIFS, la respuesta pasa siempre primero. **Eso es lo que hace posible el
ACK** sin que otra estación se meta.

### Los 6 pasos de la transmisión

```
   1. SENSE          el medio está ocupado?
                       SÍ ──▶ esperar hasta que se libere, y después
                              esperar un DIFS
                       NO ──▶ seguir al paso 2

   2. BACKOFF        elegir un número entero al azar en [0, CW]
                     → lo BAJAR de a uno, uno por cada slot time
                       (slot time = 2 × tiempo de propagación)
                       si el medio se ocupa → pausar el contador
                       y recalcular al desbloquearse
                     Cuando el contador llega a 0:

   3. TRANSMITIR     mandar la trama
                       AHORA PUEDE HABER UNA COLISIÓN Y NO LO VAMOS A SABER

   4. ESPERAR        ¿llega el ACK?
                     SÍ ──▶ listo, se INCREMENTA la CW (para la próxima trama
                            tengo menos ganas de colisionar)
                     NO ──▶ COLISIÓN (inferida)
                            ──▶ RETRANSMITIR
                            ──▶ DOBLAR la CW  ← esto es la detección

   5. RETRANSMITIR   volver al paso 2 (con la CW nueva)
                     hasta llegar a CWmax

   6. LLEGAR A       si se llega a CWmax, se ABANDONA la trama
      CWmax           (no se reintenta más) y se informa error
```

**Los valores de la contention window** (CW), que es lo que hay que saber:

| Intento | CW | Valores posibles | Probabilidad de **colisión** (2 estaciones) |
|---|---|---|---|
| 0 | **16** | 0..15 | 1/16 = 6,25 % |
| 1 | **32** | 0..31 | 1/32 = 3,1 % |
| 2 | **64** | 0..63 | 1/64 = 1,6 % |
| 3 | **128** | 0..127 | 1/128 = 0,78 % |
| 4 | **256** | 0..255 | 0,39 % |
| 5 | **512** | 0..511 | 0,20 % |
| 6 | **1023** | 0..1023 | 0,10 % |
| 7+ | **1023** (CWmax) | 0..1023 | se abandona |

> **El razonamiento detrás de la fórmula:** con dos estaciones que eligen
> **uniformemente al azar** en `[0, CW−1]`, colisionan si eligen **el mismo número**.
> Hay `CW` posibilidades y `CW` pares ordenados, así que la probabilidad de que
> elige **el mismo** es `1/CW`. Con CW = 16 es 1/16; con CW = 32 se **reduce a la
> mitad**. **Por eso la CW se duplica**: cada duplicación **reduce a la mitad** la
> probabilidad de volver a colisionar.

**El ACK es por trama, no acumulado.** Es una diferencia crítica con TCP: en WiFi
**cada trama** que lleva datos es confirmada individualmente. Es lo que permite
saber **cuál** se perdió y retransmitir solo esa.

**Y el principio de por qué no es acumulada:** con ACK acumulado, un solo ACK perdido
haría retransmitir tramas que ya llegaron. Con ACK por trama hay más tráfico de
control, pero **se recupera más rápido**. En una red con colisiones frecuentes, la
recuperación rápida gana.

## 1.4 El NAV: el sensor virtual

El **NAV** (*Network Allocation Vector*) es un **contador virtual** que cada
estación mantiene. Se actualiza con el campo **Duration / ID** del header de cada
trama que se recibe.

```
   ┌──────────────────────────────────────────────────────┐
   │                  frame 802.11                       │
   │  ┌─────────┬─────────┬───────────┬────────────────┐  │
   │  │ Frame   │ Duration│   Frame   │   Body         │  │
   │  │ Control │   /ID   │  Address  │                │  │
   │  │ 2 bytes │ 2 bytes │  6 bytes  │                │  │
   │  └─────────┴─────────┴───────────┴────────────────┘  │
   │           ▲                                           │
   │           └── Duration = 300 µs                      │
   │               "el medio está reservado 300 µs más"    │
   └──────────────────────────────────────────────────────┘

   La estación que la escucha hace:   NAV ← 300 µs
   y aunque no oiga NADA más, espera hasta que su NAV llegue a 0.
```

**Los dos sensores del medio:**

| | Sensor | Qué detecta |
|---|---|---|
| **Physical carrier sensing** | el receptor de radio | una señal **real** en el aire |
| **Virtual carrier sensing** | el **NAV** | una **reserva anunciada** por alguien que lo oyó |

**El "virtual" es porque no hay señal: hay un número.** Y es lo que resuelve la
estación oculta: C **no oye** la trama de A (sensor físico inútil), pero **sí oye**
el CTS de B, y ahí actualiza su NAV (sensor virtual).

### Un detalle técnico sobre 802.11

A diferencia de Ethernet, que tiene **una sola MAC** (la de destino), **802.11
tiene hasta 4**:

| Sigla | Significado | Qué es |
|---|---|---|
| **TA** | Transmitter Address | quién **transmite** la trama **por radio** |
| **RA** | Receiver Address | quién la **recibe por radio** |
| **SA** | Source Address |dirección MAC **del origen original** (puede venir de otro enlace) |
| **DA** | Destination Address | dirección MAC **del destino final** (puede estar en otro enlace) |

Las 4 coinciden cuando la trama no se reenvía (uso directo: estación ↔ AP). Se
difieren en el modo **punto a punto / WDS** o cuando un AP hace **puente**: ahí la
**SA** es la del cliente (la que el cliente puso) y la **TA** es la del AP.

> **Esto aparece en el Examen 2011-02 Problema 2** (IP Móvil), que pide
> explícitamente llenar TA, RA, SA y DA en cada segmento. **No lo confundas**: el
> **TA/RA** son de radio, el **SA/DA** son "de red".

## 1.5 RTS/CTS: la solución a la estación oculta

**RTS** = *Request To Send*, **CTS** = *Clear To Send*.

```
   A                 B (AP)                C (oculta)
   │                    │                     │
   │─── RTS ───────────▶│                     │   (no lo oye: está oculto)
   │  Duration=300      │                     │
   │                    │                     │
   │  NAV=300           │                     │
   │                    │◀──── C Sikuku ───────│   (C cree que el medio está libre)
   │                    │      RTS ───────────▶
   │                    │      duration=200   │
   │  NAV=300           │      NAV=200        │
   │                    │                     │
   │                    │──── CTS ───────────▶│   ★ C lo OYE y actualiza NAV
   │  NAV=200           │      duration=250   │
   │                    │      NAV=250        │
   │                    │                     │
   │─── DATA ──────────▶│  (A transmitió)     │
   │  ACK ─────────────▶│                     │
```

**Los 4 pasos y por qué funcionan:**

1. **A manda un RTS** al AP, con un `Duration` que declara cuánto va a durar la
   transacción completa.
2. **El AP responde con un CTS**, también con `Duration`, y **todos los que lo oyen**
   (incluido C) actualizan su NAV.
3. **A manda la DATA**. Como C tiene NAV > 0, **se calla**.
4. **El AP manda el ACK**.

**Tres decisiones de diseño, y las tres se preguntan:**

**a) ¿Por qué el CTS es más corto que el RTS?** Porque el CTS **sólo necesita**
llegar a quien está en la zona de solapamiento (C, que está cerca del AP). El RTS
tiene que llegar **desde A**, que puede estar lejos y atenuarse. **Menos tiempo en el
medio = menos probabilidad de colisión** en el propio RTS/CTS.

**b) ¿Por qué RTS/CTS es opcional?** Porque **cuesta**: son dos tramas extra
(RTS + CTS) por cada trama de datos. Si la trama es chica, el overhead es
mayor que el dato. De ahí el **umbral RTS**: sólo se manda RTS si la trama supera
una longitud mínima.

**c) ¿Y si no hay ningún nodo oculto?** En una red chica donde todos se ven,
RTS/CTS es **puro overhead**. El estándar lo resuelve con el **umbral RTS**, que se
configura (típicamente 500-2000 bytes).

## 1.6 Modo infraestructura

```
   ┌──────────────────────────────────────────────────────────┐
   │  ESS  (Extended Service Set): varias celdas con roaming   │
   │                                                          │
   │  ┌── BSS ──────────┐      ┌── BSS ──────────┐            │
   │  │   ● AP-1        │      │   ● AP-2        │            │
   │  │    │            │      │    │            │            │
   │  │  ▭ ▭ ▭          │      │  ▭ ▭            │            │
   │  │  clientes      │      │  clientes       │            │
   │  └─────────────────┘      └─────────────────┘            │
   │     ESSID: "Red-FING"     mismo ESSID                    │
   │     BSSID: MAC del AP     BSSID distinto                 │
   └──────────────────────────────────────────────────────────┘
```

| Sigla | Significado | Qué es |
|---|---|---|
| **BSS** | Basic Service Set | una celda: **un** AP + sus clientes |
| **ESS** | Extended Service Set | varias BSS con **el mismo ESSID**, para roaming |
| **ESSID** | el "nombre" de la red | lo que ves en la lista de WiFi |
| **BSSID** | la **MAC del AP** | identifica **la celda**, no la red |

### Las tramas de gestión y el proceso de asociación

```
   ┌────┐              ┌────┐
   │ PC │              │ AP │
   └───┘              └────┘
     │                   │
     │◀── Beacon (cada 100 ms, sin que nadie pregunte) ──│
     │     "existo, mi ESSID es X, soporto tal cosa"      │
     │                   │
     │   Association      │
     ├──────────────────▶│   (si es con seguridad: primero
     │   Request          │    autenticación y se obtiene
     │                   │    una clave)
     │◀──────────────────┤
     │   Association      │
     │   Response         │
     │                   │
     │  [DHCP si la red lo tiene]                        │
     │   ...WEP/WPA handshake si hay seguridad...         │
     │                   │
     │   DATA ◀─────────▶│   ¡AHORA SÍ!: puede mandar datos
```

| Trama | Para qué |
|---|---|
| **Beacon** | el AP **anuncia** su existencia periódicamente. **No requiere** que nadie pregunte. |
| **Probe Request** | el cliente **pregunta** si hay APs disponibles. |
| **Probe Response** | el AP **responde** a un Probe Request. |
| **Association Request** | el cliente **pide** asociarse a esa BSS. |
| **Association Response** | el AP **acepta** (o rechaza). |

> **El Beacon es lo que hace que el roaming funcione**: como se anuncia solo, un
> cliente que se mueve de celda **descubre** la nueva sin que nadie le avise. Y si
> la red tiene **seguridad**, el Beacon **también anuncia si está cifrada** — por
> eso una red WPA2 **no muestra** su ESSID en la lista pública.

## 1.7 EDCA: las 4 colas de acceso

Con EDCA hay **4 colas de prioridad**, cada una con su **CWmin** y **CWmax**:

| Prioridad | Cola | Nombre | CWmin | CWmax | Para qué |
|---|---|---|---|---|---|
| 0 (baja) | AC_BK | **Background** | 1024 | 1024 | descargas, actualizaciones |
| 1 | AC_BE | **Best Effort** | 1024 | 1024 | navegación web |
| 2 | AC_VI | **Video** | 128 | 1024 | streaming |
| 3 (alta) | AC_VO | **Voice** | 16 | 64 | VoIP |

**La regla de oro de EDCA:** dentro de cada cola, el acceso es **como CSMA/CA
normal** (backoff aleatorio entre 0 y CW). Entre colas, la de mayor prioridad
**gana**.

**El detalle fino que se pregunta: ¿por qué el video NO usa la cola de voz?**

Porque **el video no necesita baja latencia, necesita bajo jitter**:

- **Voz**: cada muestra de audio dura 20 ms. Si un paquete tarda 100 ms, la
  conversación **se corta** y se nota muchísimo. La prioridad está en el
  **tiempo estricto**.
- **Video**: un frame que tarda 100 ms en llegar produce un **artefacto visual**
  durante un frame (33 ms a 30 fps). Se nota, pero **se recupera**. Y un frame
  atrasado que llega más tarde **ya no sirve**, así que la prioridad está en el
  **jitter** y en el **tasa**, no en el retardo.

> **Decir esto es lo que diferencia**: los dos son multimedia, los dos tienen
> retardo, pero **el objetivo de QoS es diferente**.

Y sumá el **Block ACK**: en vez de confirmar cada trama, se confirman **varias de
una vez** (con un *bitmap* de cuáles llegaron). Funciona bien en video (donde se
pierde de vez en cuando) pero **no** en voz (donde cada trama es insustituible).

## 1.8 Seguridad

### WEP: no usarlo nunca

```
   Problema 1:  la clave se CIFRA con RC4, pero se transmite
                junto a cada trama. Cualquiera que sniffe un
                paquete obtiene la clave.

   Problema 2:  el vector de inicialización (IV) tiene 24 bits.
                Con muchas tramas se REPETEN, y dos textos
                cifrados con la misma clave y el mismo IV se
                anulan (ataque deKepto/keystream reuse).

   Resultado:    se rompe en minutos con herramientas freely
                disponibles. En 2001 se rompió en tiempo real.
```

### WPA2 (802.11i, 2004)

AES-CCMP, **clave compartida (PSK)** derivada por PBKDF2. Mejora real sobre WEP
(CAMBIA la clave y usa IV de 48 bits), pero **conserva el defecto de fondo**: la
clave se deriva de una **passphrase corta**, y con un **ataque de diccionario
offline** contra el handshake se la puede recuperar. Ése era el punto débil.

### WPA3 y SAE

- **SAE** (*Simultaneous Authentication of Equals*), basado en el protocolo
  **Dragonfly**: la autenticación es **resistente a ataques de diccionario
  offline**. Aunque alguien capture el handshake, **no puede** probar contraseñas
  sin|label interacted con el servidor.
- **802.11w (PMF, Protected Management Frames)**: obligatorio en WPA3. Protege las
  **tramas de administración**, que en WPA2 iban **en claro** y permitían un
  **deauth flood**: un atacante manda tramas de desautenticación falsos y
  **desconecta a los usuarios legítimos**.

| | WPA2 | WPA3 |
|---|---|---|
| Cifrado | AES-CCMP | AES-CCMP |
| Clave | PSK + PBKDF2 (4-way handshake) | **SAE** (Dragonfly) |
| Ataque de diccionario | **posible** (offline) | **imposible** (offline) |
| Tramas de gestión | **en claro** | **protegidas** (802.11w obligatorio) |
| Forward secrecy | **no** | **sí** |

## 1.9 ⚠️ Actualización a 2026

**Sigue igual — de memoria:**
- **CSMA/CA** con DCF, el **backoff aleatorio** en `[0, CW]`, y la **CW que se
  duplica** en cada retransmisión (CWmin = 16, CWmax = 1023).
- **SIFS / PIFS / DIFS / EIFS**, y el hecho de que **SIFS es el más corto** y por
  eso la respuesta pasa siempre antes que un nuevo intento de transmisión.
- **El ACK por trama**, no acumulado.
- **NAV**, y el **virtual carrier sensing** como segundo sensor.
- **RTS/CTS** para la estación oculta, **opcional**, con el **CTS más corto** que el
  RTS.
- Los **4 espacios inter-trama** y el **slot time** = 2 × propagación.
- El medio de 802.11 es **half-duplex**: no existe el full-duplex.
- **EDCA**, las **4 colas**, y el **Block ACK**.
- El concepto de **BSS/ESS/ESSID/BSSID**.
- La **estación oculta** y la **estación expuesta**, y que RTS/CTS arregla la
  primera y no la segunda.

**Cambió — y es unaactly qué:**
- **Wi-Fi 6 / 6E (`802.11ax`, 2020)**: **OFDMA** (en uplink **y** downlink),
  **BSS coloring**, 1024-QAM, **TWT** (*Target Wake Time*, para sleepy clients en
  IoT). El **BSS coloring** es lo relevante para esta clase: **resuelve la
  interferencia entre redes vecinas** etiquetando cada una con un color y usando
  **BSSID reutilizado**, en vez de depender de RTS/CTS.
- **Wi-Fi 7 (`802.11be`)**: aprobado por IEEE en **sept-2024**, publicado como
  `IEEE 802.11be-2024` en **jul-2025**. **320 MHz** de canal, **4096-QAM** y **MLO**
  (Multi-Link Operation: usar varias bandas a la vez).
- **Wi-Fi 8 (`802.11bn`)**: en desarrollo, con foco en **reliability**, no en
  throughput.
- **`802.11bt`**: frente nuevo de **criptografía post-cuántica** en WiFi.
- **WPA3** es hoy el estándar recomendado; WPA2 queda como legado aceptable.

> **Consecuencia para el examen:** la Pregunta 3 de `2008-07` (CSMA/CA) y la P5 de
  `2006-12` (estación oculta) **se responden exactamente como en 2012**. Lo único
  que puede cambiar es que te pidan los **valores de CWmin/CWmax** o el **orden
  de los espacios inter-trama**, que no cambiaron.

---

# PARTE 2 — PRÁCTICA RESUELTA

## 2.1 Ejercicio 1 — La estación oculta, paso a paso

**Datos.** AP en el centro. Estaciones **A** y **C** a su alcance (pero no entre
sí), y **B** al otro lado. Las tres quieren enviar.

**Resolución:**

```
   Paso 1:  A detecta el medio libre → transmite su trama a B.
            C NO la oye (está oculta) → cree que el medio está libre.

   Paso 2:  C transmite su trama al AP, AL MISMO TIEMPO que A.
            Las dos tramas LLEGAN AL AP JUNTAS → COLISIÓN en el AP.
            (No colisionan entre sí: nunca se encuentran en el aire.)

   Paso 3:  El AP no les manda ACK a ninguna. Las dos tramas se perdieron.

   Paso 4:  A y C, sin ACK, asumen colisión → retransmiten con CW mayor.
            Como eligen números distintos al azar, esta vez no chocan.

   CON RTS/CTS:  antes de los datos, A manda RTS; el AP responde CTS.
                 C (que no oyó el RTS) SÍ oye el CTS → actualiza su NAV
                 y se calla. No hay colisión.
```

**La frase para el examen:** *"la colisión no ocurre entre A y C sino en el punto
de convergencia, el AP; y el problema es que C no tiene forma de saber que A está
transmitiendo."*

## 2.2 Ejercicio 2 — El cálculo del NAV

**Datos.** A manda un RTS con `Duration = 300 µs`. El CTS del AP trae
`Duration = 250 µs`. El tiempo de propagación entre dos estaciones es **2 µs**.

**Resolución — el NAV de cada estación:**

```
   t = 0        A envía RTS
   t = 2 µs     el AP lo recibe (tras 2 µs de propagación)
   t = 4 µs     el AP envía el CTS
   t = 6 µs     el CTS llega a todos los que lo oyen
```

| Estación | ¿Oye el RTS? | ¿Oye el CTS? | NAV después |
|---|---|---|---|
| **A** | sí (lo emitió) | sí | 250 − (ya pasó algo de tiempo) ≈ 244 µs |
| **B (AP)** | sí | sí (lo emitió) | 250 µs |
| **C (oculta)** | **NO** | **sí** | **250 µs** ← el que lo resuelve |

**Y cuando A manda la DATA:** lleva su propio `Duration`, digamos 200 µs. Todas las
estaciones que lo oyen actualizan su NAV.

**El cálculo del overhead** (que es lo que se pregunta):

```
   Con RTS/CTS, para un dato de 1000 bytes:

      RTS      =  20 bytes de headers  (14 bytes de 802.11 + 4 de FCS)
      CTS      =  14 bytes
      DATA     = 1000 + 30 bytes de headers = 1030 bytes
      ACK      =  14 bytes
      ────────────────────────────────────────
      total    = 1078 bytes

      eficiencia = 1000 / 1078 = 92,8 %

   Con DATA sola (sin RTS/CTS):
      DATA + ACK = 1030 + 14 = 1044
      eficiencia = 1000 / 1044 = 95,8 %
```

**Conclusión, que es el punto del ejercicio:** RTS/CTS **cuesta 3 % de eficiencia**.
Si el umbral RTS está en 500 bytes y la trama es de **100**, el RTS/CTS **no
compensa**: la probabilidad de que esa trama de 100 bytes colisione es muy baja, y
el overhead no vale el riesgo evitado.

## 2.3 Ejercicio 3 — La tabla de CW y la probabilidad de colisión

**Datos.** Dos estaciones. CWmin = 16, CWmax = 1023.

**Resolución:**

| Intento | CW | Elecciones | P(choque) | P(éxito en este intento) |
|---|---|---|---|---|
| 0 | 16 | 16 | 1/16 = **6,25 %** | 15/16 = 93,75 % |
| 1 | 32 | 32 | 1/32 = **3,125 %** | 97,9 % |
| 2 | 64 | 64 | 1,56 % | 98,4 % |
| 3 | 128 | 128 | 0,78 % | 99,2 % |
| 4 | 256 | 256 | 0,39 % | 99,6 % |
| 5 | 512 | 512 | 0,195 % | 99,8 % |
| 6 | **1023** | 1023 | 0,098 % | 99,9 % |

**La probabilidad de tener éxito en los primeros k intentos:**

```
   k=1:  1 − 1/16                        = 93,75 %
   k=2:  1 − (1/16)(1/32)                = 99,8 %
   k=3:  1 − (1/16)(1/32)(1/64)          = 99,998 %
```

**El razonamiento que hay que decir:** cada intento **independiente** falla con
probabilidad `1/CW`, así que la probabilidad de fallar **todos** los primeros k es
el **producto**. Como la CW **se duplica**, el producto **decae exponencialmente**:
después de 3 intentos ya es despreciable. **Por eso el backoff exponencial es tan
efectivo** y es el mismo principio que la retransmisión de TCP (clase 20).

## 2.4 Ejercicio 4 — ¿Por qué no se puede detectar la colisión en WiFi?

**Enunciado:** *Explique por qué una estación WiFi no puede detectar una colisión
como lo hace una estación Ethernet.*

**Resolución, los tres motivos:**

1. **Half-duplex físico.** Para detectar una colisión hay que **escuchar mientras se
   transmite**. La antena de radio no puede hacer las dos cosas: es como hablar y
   escuchar a la vez. Ethernet también tiene unaLimitación similar (con CSMA/CD sobre
   cable, se escucha la señal del propio cable, lo que es físicamente distinto).

2. **Enmascaramiento por potencia.** La señal propia llega al receptor a unos 30 dBm
   (1 vatio a 30 cm). Una señal ajena que rebota puede llegar a −90 dBm. La
   diferencia es de **120 dB**, o sea un factor de **10⁶ en potencia**. El ruido
   de la señal propia es **1 millón de veces** mayor: no hay manera de escuchar por
   debajo.

3. **El medio es invisible.** Las ondas atraviesan paredes y no tienen frontera. En
   el cable, el medio es **punto a punto**: lo que sale de tu conector **no puede**
   estar en el conector de otro. En radio, **dos estaciones que no se ven** pueden
   estar usando el mismo canal y **colisionar en un tercero**.

> **La frase que resume la clase:** *en radio no se puede detectar la colisión
> porque no se puede escuchar mientras se transmite y porque la propia señal
> enmascera a las ajenas. Por eso WiFi en vez de detectar, **evita**: con
> backoff largo, con RTS/CTS y con el NAV.*

---

# PARTE 3 — PROBLEMAS DE EXAMEN DE FING

## 3.1 ⭐ Examen 2008-07, Pregunta 3 (10 puntos) — CSMA/CA en modo infraestructura

> **Fuente:** Examen `eirc0807` / `sirc0807`, julio de 2008.
> **Link:** https://www.fing.edu.uy/inco/cursos/redescomp/examenes/sirc0807.pdf

### Enunciado (texto del examen)

> Explique el protocolo de acceso múltiple con evitado de colisiones (CSMA/CA)
> utilizado en las redes inalámbricas IEEE 802.11 (Wi-Fi) trabajando en modo
> infraestructura.

### La solución, en 10 puntos

**1. Por qué evitado y no detección (1 pt).** En radio no se puede detectar una
colisión: el transceiver es **half-duplex** (no transmite y escucha a la vez) y la
potencia de la señal propia enmascera la de los demás (unos 120 dB de diferencia).
Por eso el protocolo **evita** la colisión en lugar de detectarla y recuperar.

**2. El modo infraestructura (2 pts).** Las estaciones son **clientes** de un
**punto de acceso (AP)**. Todas las tramas pasan por el AP, que hace de puente
entre la BSS y el resto de la red. El AP se anuncia periódicamente con **tramas
Beacon** (cada ~100 ms), lo que permite el **roaming**: el cliente que se mueve
descubre la nueva celda sin que nadie le avise. La celda es la **BSS**, con su
**BSSID** (MAC del AP), y varias BSS con el mismo **ESSID** forman un **ESS**.

**3. El mecanismo DCF, paso a paso (4 pts).**

```
   1. Si el medio está libre, esperar un DIFS.
   2. Elegir un entero al azar en [0, CW] y bajarlo de a uno
      por cada slot time. Si el medio se ocupa, pausar el
      contador y recalcular al desbloquearse.
   3. Cuando el contador llega a 0, TRANSMITIR.
      Puede haber colisión y no vamos a enterarnos.
   4. Esperar el ACK (por trama, no acumulado).
      - Si llega: la trama salió bien; se INCREMENTA la CW
        (menos ganas de colisionar).
      - Si NO llega: se infiere COLISIÓN; se RETRANSMITE
        y se DOBLA la CW.
   5. Si se alcanza CWmax, se abandona la trama.
```

**Los valores:** `CWmin = 16`, `CWmax = 1023`. El backoff aleatorio en `[0, CW]`
es lo que **roba el medio sin necesidad de un planificador central**.

**4. Los espacios inter-trama (1 pt).** **SIFS** (el más corto, para las
respuestas: ACK, CTS, fragmentos), **PIFS** (para el punto de acceso en modo
puntual), **DIFS** (antes de intentar transmitir una estación común), **EIFS** (tras
un error o una trama que no se entendió; el más largo, porque penaliza). El
**slot time** = 2 × el tiempo de propagación.

**5. El control del nodo oculto (2 pts).** Un **nodo oculto** es una estación que
**no escucha** a otra aunque esté a su alcance del AP; si ambas transmiten, sus
tramas **colisionan en el AP**. La solución son las tramas opcionales **RTS**
(*Request To Send*) y **CTS** (*Clear To Send*): el CTS **no lo emite quien pide**
sino el **AP**, que seLocated más cerca de todas, y por eso llega incluso a la
estación oculta. Quien escucha el CTS actualiza su **NAV** (*Network Allocation
Vector*), un contador virtual con la **duración declarada** en la trama, y espera.
El RTS y el CTS son **opcionales** porque cuestan ancho de banda; se usan según el
**umbral RTS**.

**Frase de cierre que suma puntos:** "el **NAV** funciona como un **segundo sensor**
del medio: el *physical carrier sensing* detecta la señal real, y el *virtual
carrier sensing* (el NAV) detecta una reserva anunciada por otro. Entre los dos,
una estación sabe cuándo puede hablar."

## 3.2 Examen 2006-12, Pregunta 5 (6 puntos) — la estación oculta

> **Enunciado:** Describa el problema de "la estación oculta" que se presenta en las
> redes inalámbricas.

**La solución, en 6 puntos:**

**La definición (1 pt).** En una red wireless en modo infraestructura, dos
estaciones pueden estar **dentro del alcance del punto de acceso** pero **fuera del
alcance entre sí** (por muro, por distancia, por orientación de antena). Decimos
que una es **oculta** respecto de la otra.

**El síntoma (2 pts).** Si la estación A transmite, la estación oculta C **no lo
escucha**, así que cree que el medio está libre y **transmite también**. Las dos
tramas **se superponen en el punto de acceso**, que es donde convergen. La
**colisión ocurre en el AP**, no entre las dos estaciones — que es lo confuso del
tema.

**Por qué es culpa de CSMA/CA y no del medio (1 pt).** El CSMA/CA protege contra
las colisiones que las estaciones **detectan** por other's silence. Pero la
estación oculta no puede detectar nada: **no escucha la señal**. No es que el
protocolo falle, es que **no tiene información**.

**La solución (2 pts).** **RTS/CTS**: la estación que va a transmitir pregunta
primero con un **RTS**; el AP responde con un **CTS**. El **CTS es más corto y lo
emite el AP**, que está en el centro geométrico de la red, así que **también lo
recibe la estación oculta**. Al oírlo, la estación oculta actualiza su **NAV** y
**se abstiene de transmitir**. Con esto, la estación oculta **no transmite nunca
en el medio**, y desaparece la interferencia. El RTS/CTS es **opcional**: se activa
sólo cuando el tamaño de la trama supera el **umbral RTS**, porque su costo en
ancho de banda sólo se justifica con tramas grandes.

**Lo que NO resuelve (el punto fino, 1 pt).** El problema del **nodo expuesto** es
**el inverso**: dos estaciones que se ven entre sí, pero que van a destinos
distintos. Una se calla innecesariamente. El RTS/CTS **no lo resuelve**, porque la
condición de que el CTS llegue no cambia nada. Es una limitación conocida del
protocolo, y no tiene solución limpia.

## 3.3 Examen 2007-03, Pregunta 5 (5 puntos) — CSMA/CA

> **Enunciado:** Describa el mecanismo de acceso al medio CSMA/CA (Carrier Sense
> Multiple Access With Collision Avoidance).

**La solución, en 5 puntos.** Es el mismo desarrollo que en §3.1, en formato
corto:

1. **La idea:** cada estación **escucha** el medio; si está libre, espera un **DIFS**
   y luego espera un **tiempo aleatorio** (backoff) antes de transmitir, para
   reducir la probabilidad de que dosstations hablen a la vez.
2. **El backoff:** entero aleatorio en `[0, CW]`; CW arranca en 16 y se **duplica**
   en cada intento fallido hasta 1023. Esto es lo que **evita** la colisión.
3. **La confirmación:** cada trama de datos se confirma con un **ACK individual**; si
   no llega, se asume colisión y se reintenta con CW mayor.
4. **El RTS/CTS** como mecanismo complementario para el nodo oculto.
5. **El NAV** para reservar el medio frente a estaciones que no pueden oír la señal
   directa.

> **Tope para 5 puntos:** los 5 puntos con el nombre de cada parámetro.

---

# PARTE 4 — CIERRE

## 📌 Resumen

1. En radio **no se puede detectar** una colisión: el transceiver es half-duplex y
   la señal propia enmascera a las ajenas (~120 dB). Por eso WiFi **evita**, no
   detecta.
2. **CSMA/CA (DCF)**: sense → DIFS → backoff aleatorio en `[0, CW]` → transmitir →
   esperar ACK. Sin ACK ⇒ colisión ⇒ **duplicar CW** y reintentar.
3. **CWmin = 16, CWmax = 1023**. La probabilidad de colisión con 2 estaciones es
   `1/CW`, y **duplicar la CW la reduce a la mitad**.
4. **SIFS** es el espacio más corto, y por eso **las respuestas pasan siempre
   antes** que un nuevo intento de transmisión.
5. El **ACK de WiFi es por trama**, no acumulado: se recupera más rápido.
6. **Estación oculta**: dos estaciones al alcance del AP que **no se ven entre sí**;
   colisionan **en el AP**.
7. **RTS/CTS** la resuelve: el CTS lo emite el AP, que está más cerca de todos, y lo
   oyen hasta las estaciones ocultas. **Es opcional**, con **umbral RTS**.
8. El **NAV** es un sensor **virtual** del medio: guarda la duración **declarada** en
   las tramas.
9. **EDCA** tiene **4 colas**; el video **no** usa la cola de voz porque la voz es
   **sensible al retardo** y el video al **jitter**.
10. **WPA3/SAE** resuelve el ataque de diccionario offline de WPA2; **802.11w**
    protege las tramas de administración (contra *deauth flood*).

## ✅ Autoevaluación

**1.** ¿Por qué una estación WiFi no puede detectar una colisión como sí hace una
Ethernet?

<details><summary>Respuesta</summary>

Por **dos** razones físicas. Primera: el transceiver de radio es **half-duplex**, no
puede transmitir y escuchar a la vez, y detectar una colisión exige exactamente eso.
Segunda: aunque pudiera, la **señal propia** llega al receptor a unos 30 dBm y una
señal ajena rebotada puede llegar a −90 dBm: **120 dB de diferencia**, un factor
de **10⁶ en potencia**. La propia señal ahoga por completo la de los demás. En
cable el problema es distinto: la señal del cable es la misma que se envía, y el
dominio de colisión es **punto a punto**, así que se puede comparar.

</details>

**2.** Una estación elige un backoff de 24 en un intento donde la CW es 64. ¿Cuál es
la probabilidad de que otra estación elija el mismo y colisionen?

<details><summary>Respuesta</summary>

**1/64 = 1,5625 %**. Si ambas eligen uniformemente al azar en `[0, 63]`, hay
**64** posibilidades para cada una y **64** pares ordenados, de los cuales **1** es
`(24, 24)`. Por eso la probabilidad es exactamente `1/CW`. Y por eso **duplicar la
CW** — pasar de 64 a 128 — la **reduce a la mitad**, que es el mecanismo
completo del backoff exponencial.

</details>

**3.** ¿Por qué el `REQUEST` de DHCP va por broadcast aunque el cliente ya sepa la IP
del servidor? ¿Y qué tiene que ver esto con el CSMA/CA?

<details><summary>Respuesta</summary>

Porque el `REQUEST` es el **único** mecanismo por el que los servidores que hicieron
`OFFER` y **no** fueron elegidos se enteran de que perdieron, y así liberan la
dirección que habían reservado. Si fuera unicast, cada uno creería que ganó.

Con el CSMA/CA la analogía es el **RTS/CTS**: el `REQUEST` de DHCP es
funcionalmente un "anuncio para todos" y el CTS es el que llega a las estaciones que
no oían el primero. En ambos casos, **anunciar el resultado a todo el mundo para
que los perdedores liberen recursos** es la razón de ser del broadcast.

</details>

**4.** ¿Qué diferencia hay entre una estación oculta y una estación expuesta? ¿Cuál
resuelve el RTS/CTS?

<details><summary>Respuesta</summary>

**Oculta**: A y C están al alcance del AP pero **no se ven entre sí**. Si ambas
transmiten, sus tramas **colisionan en el AP**. Es una **pérdida real**.

**Expuesta**: A y C **sí** se ven, pero van a destinos distintos. Cuando A
transmite, C se calla **innecesariamente**. Es una **ineficiencia**, no una
pérdida.

El **RTS/CTS resuelve la estación oculta**, porque el CTS lo emite el AP y llega a
las dos. **No resuelve la expuesta**: el problema es que C se calla de más, y el
RTS/CTS no cambia esa condición. Peor: activarlo sin necesidad agrega overhead al
caso frecuente.

</details>

**5.** ¿Por qué el video no usa la cola de prioridad más alta (AC_VO) que la voz?

<details><summary>Respuesta</summary>

Porque **el objetivo de QoS es distinto**. La voz es **sensible al retardo**: cada
muestra dura 20 ms y si un paquete tarda 100 ms la conversación se corta y se nota
mucho. El video es **sensible al jitter y a la tasa**: un frame que tarda 100 ms
produce un artefacto durante un frame (~33 ms a 30 fps), se nota pero **se
recupera**. Además, un frame que llega tarde ya **no sirve** para nada, así que
priorizar el tiempo no ayuda: hay que priorizar que llegue **completo** el mayor
número de frames. Por eso el video va a AC_VI y no a AC_VO.

</details>

**6.** ¿Qué es el NAV y por qué se lo llama "virtual carrier sensing"?

<details><summary>Respuesta</summary>

El **NAV** (*Network Allocation Vector*) es un contador que cada estación mantiene
actualizando con el campo **Duration/ID** de cada trama que recibe. Le dice "el medio
está reservado por tanto tiempo más".

Se lo llama **virtual** porque **no detecta ninguna señal**: es un número, no una
medición de energía. Es el complemento del **physical carrier sensing** (que sí
detecta la señal real en el aire). Los dos juntos dan a la estación la información
completa: el sensor físico le dice si hay alguien transmitiendo ahora, y el virtual
le dice si alguien **reservó** el medio para un rato.

Es especialmente útil contra la estación oculta, que no puede usar el sensor
físico para nada pero **sí** oye el CTS y actualiza su NAV.

</details>

## 🔗 Referencias

- **Examen `eirc0807` / `sirc0807`** — Pregunta 3 completa (10 pts, CSMA/CA en infraestructura)
- **Examen `eirc0612` / `sirc0612`** — Pregunta 5 (6 pts, estación oculta)
- **Examen `eirc0703` / `sirc0703`** — Pregunta 5 (5 pts, CSMA/CA)
- **Examen `eirc1007` / `sirc1007`** — Pregunta 2 (8 pts, por qué no CSMA/CD en wireless)
- **Tanenbaum & Wetherall**, *Redes de computadoras* 5ª ed., cap. 4 (subcapa MAC)
- **`ACTUALIZACIONES.md` §9** — Wi-Fi 6/7/8, BSS coloring, WPA3/SAE, 802.11bt
- **Clase siguiente:** 44 — Multimedia: streaming, RTP y VoIP
