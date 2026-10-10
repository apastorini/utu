# Clase 23 — Repaso de transporte + Simulacro 3

**Bloque:** C (Transporte) · **Semana:** 8 · **Duración estimada:** 120 min (repaso 50 + simulacro 70)
**Correlativa:** Clase 22 (taller TCP) · **Sigue con:** Clase 24 (la capa de red: las dos funciones)
**Material de referencia:** Tanenbaum cap. 6 completo · RFC 9293, RFC 5681, RFC 9438, RFC 2018, RFC 7323, RFC 6928, RFC 3168

---

## 🎯 Al terminar esta clase vas a poder

1. Reconstruir de memoria el mapa de las **8 clases** del bloque de transporte (16 a 23).
2. Escribir **de memoria** las fórmulas que aparecen en los exámenes de transporte.
3. Decir los **11 estados** de la máquina de TCP y la condición de cada transición.
4. Completar una tabla **TCP vs. UDP** de 12 filas sin mirar.
5. Identificar y corregir **las 7 confusiones** que más se castigan en este bloque.
6. Resolver un examen completo de 100 puntos en 3 horas: 5 teóricas + 2 problemas.

> **Prerequisito del examen:** **TODOS.** Esta clase cierra el bloque C. El simulacro reproduce
> el formato real (`2011-03`, `2010-12`, `2011-02`): 5 teóricas + 2 problemas de 30 pts,
> 3 horas, **mínimo 15 puntos en teoría para aprobar**.

---

# PARTE 1 — REPASO SINTÉTICO DEL BLOQUE

## 1.1 El mapa del bloque

```
   ┌───────────────────────────────────────────────────────────────────┐
   │ 16 MULTIPLEXACIÓN        2-tupla UDP vs 4-tupla TCP · mux/demux   │
   │ 17 CABECERA TCP          campos · flags · opciones · MSS         │
   │ 18 ESTABLECER/CERRAR     handshake 3-vías · 11 estados · TIME-WAIT│
   │ 19 FIABILIDAD            seq · timers · RTO · BDP · SACK · PSH  │
   │ 20 FLUJO                 rwnd · min(cwnd,rwnd) · zero window     │
   │ 21 CONGESTIÓN            slow start · CA · fast recovery · ECN   │
   │ 22 TALLER                diagramas de intercambio resueltos      │
   │ 23 REPASO + SIMULACRO                                              │
   └───────────────────────────────────────────────────────────────────┘

   UDP = una carta      TCP = telegrama certificado con acuse de recibo

   Las garantías de TCP se COMPRAN con tres mecanismos:
     números de secuencia → orden, sin duplicados, saber qué reenviar
     timers + RTO        → saber CUÁNDO reenviar
     ventana deslizante  → no esperar el ACK antes de seguir mandando
   y se PAGAN con dos controles:
     rwnd → no desbordar al receptor
     cwnd → no saturar la red
```

## 1.2 Las fórmulas que hay que saber de memoria

```
   ① RTO = SRTT + 4 · RTTVAR
          SRTT   ← (1−α)·SRTT + α·R              con α = 7/8
          RTTVAR ← (1−β)·RTTVAR + β·|SRTT − R|    con β = 1/4
          1ª muestra: SRTT = R, RTTVAR = R/2     (piso y techo)

   ② BDP = ancho_de_banda × RTT          [bytes] = [bits/s] × [s] / 8

   ③ ventana efectiva = min(cwnd, rwnd)         ← MÍNIMO, nunca suma

   ④ throughput = min( ventana_efectiva / RTT , ancho_de_banda_del_enlace )

   ⑤ MSS = MTU − 20 (IP) − 20 (TCP) = 1500 − 40 = 1460   (1448 con timestamps)

   ⑥ tiempo = tamaño_del_archivo / throughput

   ⑦ ataque TCP reset:  paquetes = 2³² / ventana = 2³² / 2¹⁴ = 2¹⁸ = 262 144
                        si no se conoce el puerto:  × 2¹⁶ = 65 536 puertos

   ⑧ módulos: puerto 16 bits → 2¹⁶ = 65 536 (0…65 535)
               número de secuencia 32 bits → 2³² = 4 294 967 296

   ⑨ d_trans = L / R
```

## 1.3 Los puertos que hay que saber

| Puerto | Servicio | Proto | Por qué lo importan |
|---|---|---|---|
| **20 / 21** | FTP datos / control | TCP | dos puertos, control separado |
| **22** | SSH | TCP | también `22/udp` y `22/sctp` en IANA |
| **25** | SMTP | TCP | envío, *push* |
| **53** | **DNS** | **UDP y TCP** | ⚠️ los dos: consultas y respuestas grandes / *zone transfer* |
| **67 / 68** | DHCP server / client | UDP | ⚠️ **nunca TCP**: el cliente aún no tiene IP |
| **80** | HTTP | TCP | también `80/udp` y `80/sctp` |
| **110 / 995** | POP3 / POP3S | TCP | *pull*, borra del servidor |
| **143 / 993** | IMAP / IMAPS | TCP | *pull*, sincroniza |
| **161 / 162** | SNMP / trap | **UDP** | dos puertos: consulta y notificación |
| **179** | BGP | TCP | ⚠️ un protocolo de **enrutamiento** sobre transporte **fiable** |
| **443** | **HTTPS** | **TCP y UDP** | ⚠️ el UDP es **HTTP/3 (QUIC)** |
| **853** | DNS sobre TLS (DoT) | TCP | DNS cifrado |
| **546 / 547** | DHCPv6 client / server | UDP | el DHCP de IPv6 |

```
   ⚠️ 53 UDP+TCP   → si solo decís "DNS usa UDP", te falta la mitad
   ⚠️ 443 TCP+UDP  → el UDP es HTTP/3; HTTP/3 NO usa TCP para los datos
   ⚠️ 179 TCP      → BGP necesita fiabilidad
   ⚠️ 67/68 UDP    → DHCP en UDP porque el cliente aún no tiene dirección

   Rango: 16 bits ⇒ 0 … 65 535.   0…1023 = bien conocidos / privilegiados
          (en Unix, `bind()` sobre ellos requiere root)
```

## 1.4 Los flags TCP

```
   ┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┐
   │ NS  │CWR  │ ECE  │ URG │ ACK │ PSH │ RST │ SYN │ FIN │reserv.│
   └─────┬─────┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴─────┘
        │        │     │     │     │     │     │     │  (4 bits)
        │ NS     │     │     │     │     │     │     └─ datos urgentes
        │ (RFC   │     │     │     │     │     └────── último segmento
        │ 3540)  │     │     │     │     └──────────── error: RESET
        │        │     │     │     └────────────────── entrega inmediata
        │        │     │     └──────────────────────── confirma el campo ack
        └────────┴─────┴──────────────────────────────── SYN/FIN abren y cortan
```

| Flag | Significado | Dónde se usa |
|---|---|---|
| **SYN** | sincronizar | abre la conexión (handshake) |
| **ACK** | confirmar | `1` en casi todo lo que sigue al handshake |
| **FIN** | finalizar | media conexión de cierre |
| **RST** | reset | **corta la conexión de inmediato**, sin negociación |
| **PSH** | push | sugiere entregar ya a la aplicación (**no garantiza nada**) |
| **URG** | urgente | activa el *urgent pointer* |
| **ECE / CWR** | control de congestión | **ECN** (`RFC 3168`): ECE=1 "hubo congestión", CWR=1 "bajé mi ventana" |
| **NS** | no-sacudir | extensión: no limpiar el campo ECN al calcular el checksum |

```
   ★ El flag PSH NO garantiza un mensaje por read() (Clase 19 §1.8, 2001-12 Prob. 2)
   ★ RST no se negocia: aborta sin cierre ordenado
   ★ SYN y FIN abren/cortan; ACK y PSH son de "tránsito"
   ★ ECE/CWR existen SOLO por ECN; sin ECN van en 0
```

## 1.5 Los 11 estados de la máquina de TCP

```
   ┌──────────┐
   │  CLOSED  │◄────────────────────────────────────────────┐
   └────┬─────┘                                             │
        │ passive open                  active open          │
   ┌────▼─────┐                          ┌──────────┐         │
   │  LISTEN  │                          │ SYN-SENT │         │
   └────┬─────┘                          └────┬─────┘         │
        │ receive SYN, send SYN+ACK           │ receive SYN+ACK│
   ┌────▼───────────┐◄─────────────────────────┘               │
   │ SYN-RECEIVED   │                                          │
   └────┬───────────┘   receive ACK                           │
   ┌────▼──────────┐   receive FIN y la app todavía no hizo     │
   │ ESTABLISHED  │   close()                                   │
   └──┬────────┬──┘                            ┌─────────────┐ │
      │        │ close()                        │ CLOSE-WAIT  │ │
      │  ┌─────▼──────┐ send FIN                └──────┬──────┘ │
      │  │ FIN-WAIT-1 │◄───────────────────────────────┘ close()
      │  └─────┬──────┘
      │   receive FIN      receive ACK
      │  ┌──────▼─────┐
      │  │  CLOSING  │  cierre simultáneo de los dos lados
      │  └──────┬─────┘
   receive ACK│
   ┌──────▼──────┐
   │ FIN-WAIT-2  │   (ya no manda nada; espera el FIN del otro)
   └──────┬──────┘
   receive FIN
   ┌──────▼──────┐     ┌───────────┐
   │  TIME-WAIT  │────►│ LAST-ACK  │
   │   2 × MSL   │ ACK │           │
   └─────────────┘     └─────┬─────┘
                              │ receive ACK
                              └──► CLOSED
```

**Los once, numerados:** CLOSED, LISTEN, SYN-SENT, SYN-RECEIVED, ESTABLISHED, FIN-WAIT-1,
FIN-WAIT-2, CLOSE-WAIT, CLOSING, LAST-ACK, TIME-WAIT.

```
   ★ TIME-WAIT = 2 × MSL  (Maximum Segment Lifetime)
     ¿Por qué 2×MSL y no 1? Un segmento perdido puede reaparecer como duplicado
     tarde. Si el socket se cerrara a los MSL, ese duplicado con la misma
     4-tupla caería dentro de una conexión NUEVA y corrompería el flujo.
     Con 2×MSL se garantiza que el viejo ya expiró en la red.

   ★ LAST-ACK: mandó su FIN y espera el ACK del FIN ajeno. No es lo mismo que
     TIME-WAIT: acá ya no manda nada.
   ★ CLOSING: cierre simultáneo. Raro, y es el que hay que saber dibujar.
   ★ Un RST en cualquier estado → CLOSED, sin negociación y sin TIME-WAIT.
   ★ Costo: TIME-WAIT retiene un puerto por 2×MSL ⇒ agotamiento de puertos
     efímeros en servidores con muchos clientes cortos.
```

## 1.6 La tabla TCP vs. UDP — 12 filas

| # | Aspecto | **UDP** | **TCP** |
|---|---|---|---|
| 1 | **Conexión** | sin conexión (*connectionless*) | **con conexión**, 3-vías |
| 2 | **Fiabilidad** | **no**: se pierde y sigue | **sí**: ACK + timers + retransmisión |
| 3 | **Orden** | **no garantizado** | **sí**, por número de secuencia |
| 4 | **Latencia** | **baja**, sin handshake | **1 RTT extra** de handshake |
| 5 | **Control de congestión** | **ninguno** (¡por eso QUIC!) | **sí**: `cwnd`, slow start, ECN |
| 6 | **Control de flujo** | ninguno | **sí**: `rwnd` |
| 7 | **Cabecera** | **8 bytes** (2+2+2+2) | **20 bytes** mínimo, hasta 60 |
| 8 | **Identificación** | **2-tupla** (IP, puerto) *(el kernel usa la 5-tupla)* | **4-tupla** (IP_o, p_o, IP_d, p_d) |
| 9 | **Multiplexación** | **1 socket habla con muchos** a la vez, mismo puerto | **1 conexión por 4-tupla**: 1 socket por conexión |
| 10 | **Checksum** | obligatorio en IPv6, opcional en IPv4 | **siempre obligatorio** |
| 11 | **Frontera de mensaje** | **SÍ**: 1 datagrama = 1 mensaje | **NO**: flujo de bytes; los mensajes los pone la aplicación |
| 12 | **Usos típicos** | DNS, DHCP, SNMP, RTP/VoIP, QUIC (HTTP/3) | HTTP/1.1 y HTTP/2, SSH, SMTP, POP3/IMAP, FTP, BGP |

**Las tres filas donde más se falla:**

```
   Fila 8 — 2-tupla vs 4-tupla:
     UDP  → el socket se identifica con (IP, puerto) ⇒ un solo proceso
            (el servidor DNS, puerto 53) atiende a TODOS los clientes.
     TCP  → cada 4-tupla distinta necesita un socket distinto ⇒ el SO crea
            uno por accept().

   Fila 11 — frontera de mensaje:
     UDP  → cada datagrama es una unidad: leés N bytes, es UN mensaje.
     TCP  → read() puede devolver medio mensaje o dos pegados. PSH no lo
            arregla (Clase 19 §1.8).

   Fila 5 — por qué HTTP/3 necesita QUIC:
     UDP solo no tiene control de congestión, y eso sería grave en Internet.
     QUIC (RFC 9000/9002) reimplementa fiabilidad, control de congestión y
     PLPMTUD ENCIMA de UDP. No es "HTTP/3 usando UDP": es un transporte
     nuevo que compite con TCP.
```

## 1.7 Las tres tablas de memoria en una sola vista

```
   ¿Qué puerto?            ¿Qué flags?              ¿En qué estado?
   ─────────────           ──────────────           ─────────────────────
   DNS     53 UDP/TCP      handshake: SYN,          CLOSED → LISTEN (servidor)
   HTTP    80 TCP          SYN+ACK, ACK              SYN-SENT → SYN-RECEIVED
   HTTPS  443 TCP/UDP      datos: ACK, PSH,          → ESTABLISHED
   SSH     22 TCP          cierre: FIN, ACK          ESTABLISHED → FIN-WAIT-1
   SMTP    25 TCP                                    → FIN-WAIT-2 → TIME-WAIT
   DHCP  67/68 UDP         error: RST                → LAST-ACK → CLOSED
   BGP    179 TCP          sync: ECE, CWR           (también: CLOSING)
   SNMP 161/162 UDP
```

### ⚠️ Actualización a 2026

**Sigue igual — de memoria, no se toca:**
- **4-tupla** identifica una conexión TCP; el socket UDP se trata como **2-tupla**.
- Los **11 estados** son los mismos. **Three-way handshake**, cierre de **4 vías**,
  **TIME-WAIT de 2×MSL**.
- **Números de secuencia de 32 bits**, **ACK acumulativo**, **ventana deslizante**.
- **Los ACKs son de bytes, no de segmentos**: `ack` = próximo byte esperado.
- Sliding window, dupACKs, delayed ACK, Nagle, persist/keepalive, RTO, Jacobson/Karels,
  fast retransmit, slow start, congestion avoidance, fast recovery.
- **MTU/MSS**, opciones en el SYN (MSS, SACK permitted, Timestamps, Window Scale), checksum
  con pseudo-cabecera, descarte de segmentos fuera de ventana.

**Lo que cambió — las correcciones obligatorias del bloque:**

| En 2011 se decía | En 2026 |
|---|---|
| `RFC 793` es TCP | **`RFC 9293`** (2022, *Internet Standard*; consolida 793 + RFC 879, 2873, 6093, 6429, 6528, 6691) |
| Reno / Tahoe | **CUBIC = `RFC 9438`** (2023, *Standards Track*), default de Linux, Windows y Apple; obsolesce `RFC 8312` |
| "quizá BBR" | **BBR nunca fue RFC**: `draft-ietf-ccwg-bbr`, BBRv3, *Experimental*. ⚠️ **`RFC 8312` es CUBIC, no BBR** |
| IW = 1 MSS | **IW = 10 MSS** (`RFC 6928`, 2013) |
| SACK opcional | `RFC 2018` es **comportamiento estándar**; Timestamps + Window Scale = `RFC 7323` (obsolesce `1323`); **PAWS obligatorio** si se activan |
| ECN = `RFC 3168` | `RFC 3168` + **`RFC 9768` AccECN (2026)**; L4S = `RFC 9331` |
| — | **QUIC** (`RFC 9000/9001/9002`, 2021): transporte completo que **reemplaza** a TCP en HTTP/3 |
| — | **MPTCPv1** (`RFC 8684`, 2020): multipath, real pero marginal (~0,4 % de bytes pico) |

⚠️ **Tres errores que NO son obsolescencia sino directamente falsos:**

| Se dice | Realidad |
|---|---|
| "`RFC 8951` = ECN en multihop" | **FALSO**: es una aclaración de **EST** (Enrollment over Secure Transport) |
| "`RFC 7560` = ECN++" | **FALSO**: es solo el **documento de problema** de ECN; la especificación quedó en `RFC 9768` |
| "`RFC 8984` depreca el half-duplex Ethernet" | **FALSO**: `RFC 8984` es **JSCalendar**. La decisión es de **IEEE 802.3**, y ni siquiera es total |

> **Consecuencia para el examen:** los **mecanismos** se preguntan **exactamente igual** que en
> 2011. Lo único que se corrige es **la etiqueta normativa** y, si preguntan por despliegue
> real, quién está en el default (CUBIC, no Reno).

---

# PARTE 2 — LOS ERRORES FRECUENTES

Los siete que más puntos se pierden en los exámenes de transporte.

## Error 1 — "El ACK confirma un segmento"

**❌** "A mandó S2, entonces A2 confirma S2."
**✅** El ACK es **acumulativo y numera bytes**: `ack` = **próximo byte esperado**. Un
`ack = 7120` confirma los 120 bytes del 7000 al 7119 de una sola vez.
**Por qué importa:** si razonás por segmentos, fallás todos los diagramas con pérdida, que es
justo lo que se pregunta (`2011-03 P4`).

## Error 2 — "Si se perdió el primero, mando el segundo otra vez"

**❌** Ante `ack = 7000` repetido, "el que falta es el primero, así que mando el segundo".
**✅** `ack = 7000` significa que **falta a partir del 7000**, o sea el **primero** (S1,
`seq = 7000`). Es el que hay que retransmitir.
**Por qué importa:** arruina el apartado (b) de `2011-03 P4`.

## Error 3 — "El timeout es para detectar la pérdida"

**❌** "TCP usa un timer para saber cuándo se perdió un segmento."
**✅** El timeout existe porque, si el ACK **no llega**, TCP **no puede distinguir** tres cosas:
se perdió el dato, se perdió el ACK, o tardó. Las tres se ven **exactamente igual**. La única
salida es retransmitir, y para eso hay que saber **cuándo** → el timer.
**Por qué importa:** es el apartado (b) de `2010-12 P4`, la pregunta conceptual más fina.

## Error 4 — "Flujo y congestión son lo mismo"

**❌** "Ambos bajan la ventana, así que son lo mismo."
**✅** **Flujo** = el receptor no puede absorber → `rwnd`, lo controla el **receptor** y lo
anuncia en el campo `window`. **Congestión** = la red no puede transportar → `cwnd`, lo
controla el **emisor** estimando, y nadie se lo dice.
**Por qué importa:** `2009-07 P1a` (10 pts) es esta pregunta. Y si bajás `cwnd` cuando el
`rwnd` es 0, **castigás a la red por un problema del receptor** y no arreglás nada.

## Error 5 — "La ventana efectiva es cwnd + rwnd"

**❌** "Se suman porque son cosas distintas."
**✅** Es el **mínimo**: `min(cwnd, rwnd)`. Ambas son **cotas superiores**. Con la suma, el
excedente que la red no tomó se acumularía en el buffer del receptor y lo desbordaría **justo
cuando la red va peor**.
**Por qué importa:** es la mitad de `2011-03 Problema 1c` (12 pts) y aparece en toda
`2009-07 P1a`.

## Error 6 — "Con PSH el receptor lee un mensaje"

**❌** "Puse PSH, así que el `read()` del otro devuelve exactamente el mensaje."
**✅** PSH es **una sugerencia** de "no tengo más datos en el buffer". Es **un bit**: no
transporta información de frontera de mensaje. Si llegan dos segmentos con PSH **fuera de
orden**, el `read()` devuelve **los dos pegados**. Las fronteras las pone la aplicación.
**Por qué importa:** es `2001-12 Problema 2` entero, y es la fuente del error de cualquiera que
programme sockets.

## Error 7 — "La pérdida siempre significa congestión"

**❌** "Se perdió un paquete ⇒ la red está saturada."
**✅** **No.** También por CRC de un enlace, buffer del receptor lleno (control de **flujo**),
ACL/firewall, fragmento descartado en IPv4, corte de un enlace. **TCP asume** que sí, porque
es la apuesta con mejor promedio: castigar a la red de vez en cuando sale más barato que
saturarla.
**Por qué importa:** es `2009-07 P1c`, y revela si entendiste que TCP **infiere** la congestión
en lugar de que se la **notifiquen**.

### ⚠️ Errores típicos del simulacro (los que no son de este bloque)

```
   ⚠️ No cites "la RFC de TCP" como RFC 793 → es RFC 9293
   ⚠️ No digas "el timeout baja cwnd a cwnd/2" → a 1 MSS (Tahoe y Reno coinciden)
   ⚠️ No digas "3 dupACKs ⇒ cwnd = 1 MSS" en Reno ⇒ cwnd/2 (eso es Tahoe)
   ⚠️ No digas "DNS usa el puerto 53 UDP" solo ⇒ también TCP
   ⚠️ No digas "la cabecera TCP son 20 bytes" sin aclarar "mínimo"
```

---

# PARTE 3 — SIMULACRO 3

> **Instrucciones (reproducción del formato real de FING):**
> - Examen individual, **sin material**, **3 horas**.
> - **5 Preguntas Teóricas** (~40 pts) + **2 Problemas Prácticos** (30 pts cada uno).
> - Aprobación: **60 puntos**.
> - ⚠️ **Es obligatorio responder correctamente al menos 15 puntos en las preguntas
>   teóricas.** Si no llegás a 15 en teoría, no aprobás aunque sumes 60 con los problemas.
> - Empezá cada pregunta y cada problema en una hoja nueva.
> - Dudas de letra solamente; **ninguna** en los últimos 30 minutos.
> - Para los problemas podés suponer que disponés de los tipos básicos (lista, cola, archivo,
>   string) y sus funciones (`tail()`, `crear()`, `concatenar()`).
>
> ⏱️ **Cronómetro sugerido (180 minutos):**
>
> | Etapa | Min | Objetivo |
> |---|---|---|
> | Lectura inicial | 5 | leer entero, elegir por dónde empezar |
> | T1 (10 pts) | 15 | |
> | T2 (10 pts) | 15 | |
> | T3 (8 pts) | 12 | |
> | T4 (10 pts) | 15 | |
> | T5 (8 pts) | 12 | **69 min de teoría, ~46 pts** |
> | Problema 1 (30 pts) | 50 | pseudocódigo estilo C: leer bien el enunciado |
> | Problema 2 (30 pts) | 45 | números: cuentas a la vista, TABLAS antes que prosa |
> | Repaso final | 5 | re-leer los números de los dos problemas |
> | **Total** | **180** | |
>
> **El consejo de la cátedra, y es el que más cuesta aprender:** los problemas prácticos se
> corrigen **por lo que escribiste**, no por lo que pensaste. Si no te da el número exacto,
> **dejá la fórmula y la cuenta a medias** con la unidad anotada: parcialmente es puntos. En
> cambio un apartado en blanco es cero.

---

## 📝 ENUNCIADO DEL SIMULACRO (sin respuestas)

### Preguntas Teóricas

**T1 (10 puntos).** Un protocolo de transporte entrega a la aplicación un flujo de bytes y
promete que **no se pierde nada, no se duplica nada y todo llega en orden**.
a) Explique qué mecanismo permite cumplir cada una de esas tres promesas, y por qué el
`checksum` por sí solo no alcanza.
b) Suponga que el emisor manda un segmento, no recibe el ACK y se vence el timer. Enumere
**todas** las explicaciones posibles de ese fallo y explique por qué el protocolo **no puede
distinguir entre ellas**. ¿Qué decisión queda, y qué falta para poder tomarla?
c) Explique cómo estima el protocolo el valor del timer, y qué ocurre con ese valor tras
varios timeouts consecutivos.

**T2 (10 puntos).** En un protocolo de transporte con control de congestión y de flujo:
a) Diferencie el control de flujo del control de congestión, indicando **qué variable**
representa a cada uno, **quién** la decide y **cómo** se comunica al otro extremo.
b) Escriba la expresión de la ventana efectiva y justifique por qué es un **mínimo** y no una
suma.
c) El receptor anuncia una ventana de recepción igual a cero. Detalle qué hace el emisor, con
qué periodicidad, y justifique por qué esa situación **no** debe tratarse como congestión.
d) Mencione dos causas de pérdida de paquetes que **no** se deban a congestión.

**T3 (8 puntos).** Sobre el protocolo TCP:
a) Escriba los **11 estados** de su máquina de estados.
b) Detalle la secuencia de **mensajes** del establecimiento de una conexión, indicando qué flags
activa cada uno y cómo se numeran los bytes iniciales en ambos sentidos.
c) Explique por qué, tras el cierre ordenado, un extremo permanece en `TIME-WAIT` durante
`2 × MSL`, y qué ocurriría si no lo hiciera.

**T4 (10 puntos).** Compare los dos protocolos de transporte de la familia TCP/IP.
a) Para cada uno de los siguientes aspectos, indique la diferencia: (i) existencia de conexión;
(ii) número de bytes de cabecera; (iii) forma de identificar una comunicación; (iv) manejo de
la pérdida de datos; (v) frontera de mensajes.
b) Explique por qué un protocolo que entrega datagramas sin conexión **no puede** implementar
control de congestión, y qué construcción tecnológica reciente resuelve esa carencia.

**T5 (8 puntos).** Un desarrollador afirma: *"mandé un mensaje con el flag PUSH activado, así
que el programa remoto lo recibirá en una llamada al sistema de lectura distinta de las
demás"*.
a) Argumente por qué la afirmación es incorrecta.
b) Describa un procedimiento de laboratorio que demuestre empíricamente la falsedad de la
afirmación.
c) Indique la práctica correcta para garantizar la separación de mensajes en un protocolo de
aplicación, y nombre un protocolo de transporte que sí tenga noción nativa de mensaje.

### Problemas Prácticos

**Problema 1 (30 puntos) — Programación.**
Un protocolo de transporte de la familia TCP implementa control de congestión y notifica las
pérdidas. Cuando detecta un evento adverso, el emisor **reduce su ventana de congestión** y
entra en un régimen de crecimiento más conservador hasta volver al anterior.

**Primitivas disponibles:**
```
void setVentanaCong(int valor);   // fija el tamaño de la ventana de congestión
int  getVentanaCong();            // lee el tamaño actual
void setUmbral(int valor);        // fija el "umbral" que separa los dos regímenes
int  getUmbral();
void setNotificarPerdida();       // marca los próximos segmentos a enviar con la
                                  // bandera que avisa "hubo pérdida"
```
**Tipos:**
```
Segmento {
  int  puerto_destino, puerto_origen;
  long numero_secuencia;          // número de secuencia del primer byte
  long numero_confirmacion;       // próximo byte esperado por el otro lado
  int  cantidad_datos;            // bytes de datos del segmento
  bool marca_perdida;             // la bandera de "hubo pérdida"
  IP  encapsulated;               // la cabecera IP del paquete que lo trajo
  ...
}
IP {
  IP  origen, destino;
  enum estado_ecn { NO_SOPORTA, SOPORTA, CONGESTION_EXPERIMENTADA }
  ...
}
```
**Se pide:**
- **a) (6 pts)** ¿Qué eventos, en un protocolo **sin** notificaciones explícitas, interpreta
  como indicio de pérdida? Explique cómo distingue un evento grave de uno leve, y qué valor
  toma la ventana de congestión en cada uno.
- **b) (12 pts)** Implemente `int detectarCongestion(Segmento s)`, que devuelve 1 si hay
  congestión y 0 si no. **Si se invoca con `s == NULL`, es porque se venció un timer esperando
  una confirmación.** El protocolo debe: (i) detectar los ACKs duplicados; (ii) resetear el
  contador cuando hay progreso real; (iii) propagar la marca de "hubo pérdida" si el segmento
  recibido la trae; (iv) avisar al otro extremo si la cabecera IP recibida viene marcada por
  un router como congestionada.
- **c) (12 pts)** Implemente `void controlarCongestion(int hayCongestion)`. Ante congestión,
  el protocolo debe dividir por dos la ventana actual y guardar ese valor como **umbral**; fijar
  la ventana en **un MSS**; y volver al régimen de arranque. Sin congestión: en el régimen de
  arranque, **sumar un MSS por cada confirmación recibida** (y cambiar de régimen al superar el
  umbral); en el régimen de evitación, **sumar `MSS² / ventana` por cada confirmación recibida**.
- **d) (2 pts)** El protocolo anuncia en cada segmento el tamaño de su ventana de recepción.
  Explique, en un párrafo, cómo se combina esa ventana de flujo con la de congestión, y qué se
  rompe si alguien las sumara.

**Problema 2 (30 puntos) — Números y diagramas.**
Dos procesos, **A** (IP `10.0.0.1`, puerto `5000`) y **B** (IP `10.0.0.2`, puerto `80`),
mantienen una conexión TCP abierta. El enlace que los une tiene una ventana de transmisión de
**32 KB**.

En un instante dado, A envía a B **cinco** segmentos consecutivos de **24 bytes** de datos cada
uno, sin datos previos sin confirmar. El **primer** segmento tiene número de secuencia `7000`.
Las latencias son aproximadamente uniformes y el valor del timer es **mayor** que el tiempo de
llegada de la primera confirmación.

**Se pide:**
- **a) (8 pts)** Escriba el valor del campo número de secuencia de **cada uno** de los cinco
  segmentos, y el campo número de confirmación de las respuestas de B, asumiendo que **no hay
  pérdidas** y que B no tiene datos que enviar. Dibuje el intercambio completo.
- **b) (10 pts)** Dibuje ahora el intercambio si **se pierde el primer segmento**. Muestre los
  valores de los campos y explique, con las dos señales de la RFC, **qué dos eventos** pueden
  provocar la retransmisión, y **qué valor toma la ventana de congestión** en cada uno.
- **c) (6 pts)** El campo de longitud de ventana de la cabecera TCP tiene 16 bits. Calcule el
  **número máximo de bytes** que puede confirmar en cada paquete el segmento de B con el tamaño
  de ventana indicado, y el **número de segmentos de 24 bytes** que necesitaría para confirmar
  los 120 bytes del apartado (a). Si el protocolo negotiating *escalado de ventana*, ¿cuánto
  cambia?
- **d) (6 pts)** Un atacante que no conoce el puerto origen de A quiere cerrar esa conexión
  mandando un paquete RST. Calcule **cuántos números de puerto** debe adivinar, **cuántos
  números de secuencia** debe probar para cada uno, y **cuánto tiempo** tardaría con un enlace
  de **100 Mbps**, sin considerar tiempos de generación de paquetes. Muestre todas las cuentas.

---

# PARTE 4 — RESOLUCIÓN DEL SIMULACRO

> Todo lo que sigue está en `<details>`. **Resolvé primero el enunciado.**

<details><summary><b>T1 — Resolución (10 pts)</b></summary>

### a) Los tres mecanismos (4 pts)

| Promesa | Mecanismo |
|---|---|
| **Ordenada** | **Números de secuencia** (de bytes) + buffer de reordenamiento en el receptor |
| **Sin duplicados** | el receptor **descarta** lo que ya tiene: `rcv_nxt` es el puntero que avanza |
| **Sin errores** | **checksum** (detecta) + **retransmisión** (corrige) |

**Por qué el checksum no alcanza (1 pt):** detecta que **un** segmento vino mal, pero **no dice
qué bytes se perdieron**. Para retransmitir el correcto necesitás un identificador que sobreviva
al viaje: el número de secuencia. Y sin números tampoco podés evitar duplicados, porque no sabés
qué tienes ya.

### b) Las tres explicaciones posibles (3 pts)

```
   ┌────────────────────────────────────────────────────────────────┐
   │ Se envió S (seq = 7000). Pasó el tiempo. No llegó el ACK.      │
   │   (1) Se perdió el SEGMENTO de datos                           │
   │   (2) Se perdió el ACK                                         │
   │   (3) El ACK no se perdió: simplemente TARDÓ                   │
   └────────────────────────────────────────────────────────────────┘
```

**Por qué no se pueden distinguir (1 pt):** las tres producen **exactamente la misma
observación** en el emisor — la ausencia del ACK. No hay otro canal por el cual enterarse. No
puede retransmitir de inmediato (sería un duplicado puro) ni esperar indefinidamente (si la
pérdida es real, la conexión se cuelga).

**La decisión que queda (1 pt):** la única salida es **retransmitir**. Y para eso hay que
decidir **cuándo** → hace falta un **timer por segmento**. El enunciado dice "tiempo prudencial",
que es literalmente lo que hace el RTO.

### c) La estimación del timer (3 pts)

```
   SRTT   ← (1−α)·SRTT + α·R              con α = 7/8
   RTTVAR ← (1−β)·RTTVAR + β·|SRTT − R|    con β = 1/4
   RTO    = SRTT + 4 · RTTVAR

   Primera muestra:  SRTT = R ;  RTTVAR = R/2 ;  RTO = 3R     (con piso y techo)
```

**Tras varios timeouts consecutivos (1 pt):** el RTO **se duplica** cada vez — ***backoff*
exponencial**: `240 ms → 480 → 960 → 1920`.

**Por qué:** un timeout **no** es evidencia de congestión (puede ser un blackout o un enlace
caído). Subir el RTO dice "esto parece una avería, esperemos más". **No hay que confundirlo**
con el `cwnd`, que sí baja: el `cwnd` protege a la red, el backoff protege al emisor de insistir
contra algo que no responde. **Las dos cosas pasan a la vez.**

> **Tope para 10:** los tres mecanismos + por qué el checksum no alcanza (4), las tres causas +
> "no se pueden distinguir" + retransmitir + el cuándo (3), Jacobson/Karels + backoff (3).

</details>

<details><summary><b>T2 — Resolución (10 pts)</b></summary>

### a) La diferencia (4 pts)

| | **Control de flujo** | **Control de congestión** |
|---|---|---|
| **Variable** | `rwnd` (*receive window*) | `cwnd` (*congestion window*) |
| **La decide** | el **receptor** | el **emisor**, estimando |
| **Se comunica** | en el **campo `window`** de cada segmento (16 bits) | **nadie se lo dice**: se deduce de ACKs y timers |
| **Problema** | el receptor no puede absorber | la red no puede transportar |
| **Síntoma** | el buffer del receptor se llena | los buffers de los **routers** se llenan |

**El punto clave (1 pt de los 4):** el flujo se puede **comunicar** porque el receptor **sabe**
su estado; la congestión **no**, porque el emisor no tiene forma de preguntar a la red ⇒ es una
**hipótesis**, y por eso se deduce de la **pérdida**.

### b) La ventana efectiva (2 pts)

```
   ventana efectiva = min(cwnd, rwnd)
```

**Por qué el mínimo y no la suma (1 pt de los 2):** ambas son **cotas superiores
independientes**. Si las sumaras, el excedente que la red no pudo tomar **se acumularía en el
buffer del receptor y lo desbordaría**, y lo desbordaría **justo cuando la red va peor**:
exactamente cuando el buffer del receptor ya está más lleno. El `min` es el único que garantiza
que **nadie se desborda**.

### c) Ventana de recepción igual a cero (3 pts)

**Qué hace el emisor (2 pts):**

1. La ventana efectiva es `min(cwnd, 0) = 0` ⇒ **no puede enviar datos**.
2. Entra en **persistencia** (`RFC 9293` §8.6): cuando expira el **persist timer**, manda
   ***zero-window probes***.
3. Son de **1 byte**, con periodicidad **exponencial** (empieza en ~un RTO y duplica hasta un
   tope, típicamente ~60 s).
4. Si la respuesta trae `window = 0`, espera otro intervalo y vuelve a sondear; si trae
   `window > 0`, **reanuda**.

**Por qué NO es congestión (1 pt):** la **red está perfecta**: nadie está saturado, no hay
pérdidas, no hay routers con buffer lleno. Lo que está lento es la **aplicación del receptor**,
que no está leyendo. Bajar el `cwnd` **no arreglaría nada** (no puede hacer que una aplicación
lea más rápido) y **castigaría a la red** por un problema ajeno.

### d) Dos pérdidas que no son congestión (1 pt)

Cualquiera dos de: **errores de CRC** en un enlace; **buffer del receptor lleno** (control de
**flujo**, la red estaba perfecta); **descarte por ACL/firewall**; **fragmento descartado** en
IPv4; **corte de un enlace**.

**Justificación que suma:** TCP **asume** que sí, porque es la apuesta con mejor promedio. Ante
la duda entre "red saturada" y "error puntual", **bajar la ventana** cuesta rendimiento en el
caso puntual pero **salva la red** en el caso saturado. El error hacia el otro lado es mucho más
caro (*bufferbloat*, colapso).

> **Tope para 10:** (a) 4 con la observación de que la congestión es hipótesis; (b) 2 con el
> desbordamiento; (c) 3 con tamaño, periodicidad exponencial y la justificación; (d) 1 con dos
> causas.

</details>

<details><summary><b>T3 — Resolución (8 pts)</b></summary>

### a) Los 11 estados (3 pts, ~0,27 c/u)

1. **CLOSED** · 2. **LISTEN** · 3. **SYN-SENT** · 4. **SYN-RECEIVED** ·
5. **ESTABLISHED** · 6. **FIN-WAIT-1** · 7. **FIN-WAIT-2** · 8. **CLOSE-WAIT** ·
9. **CLOSING** · 10. **LAST-ACK** · 11. **TIME-WAIT**

*(Si listaste 10 y te faltó `CLOSING`, o al revés, se descuenta ~0,3: es el estado del cierre
simultáneo y casi todos lo olvidan.)*

### b) El three-way handshake (3 pts)

```
   Cliente                              Servidor
      │                                    │
      │──── SYN  seq=x  ─────────────────▶│   flags = SYN
      │                                    │   "quiero conectar; mis bytes
      │                                    │    empiezan en x"
      │◀──── SYN+ACK  seq=y  ack=x+1 ─────│   flags = SYN,ACK
      │                                    │   "acepto; los míos empiezan en
      │                                    │    y; confirmé hasta x"
      │──── ACK  seq=x+1  ack=y+1 ───────▶│   flags = ACK
      │                                    │
      │        ESTABLISHED  ← 3 mensajes, 1 RTT
```

**Los tres detalles que dan el punto completo:**

1. **SYN consume un número de secuencia.** Por eso `ack = x + 1`, no `ack = x`. Los números
   iniciales los elige **cada uno por su cuenta** (en TCP real, al azar).
2. **Los números son independientes por sentido:** A empieza en `x`, B en `y`.
3. **El 3er mensaje (ACK puro) puede llevar datos**, y en la práctica los lleva: es la primera
   petición HTTP, enviado para no esperar un RTT más.

**El cierre de 4 vías (bonus):**

```
   A ──── FIN, seq=... ─────────────▶ B     A: ESTABLISHED → FIN-WAIT-1
   ◀──── ACK, ack=... ────────────── A     A → FIN-WAIT-2
   ◀──── FIN, seq=... ────────────── B     B → LAST-ACK
   ──── ACK ─────────────────────▶ B      B → CLOSED
                                        A → TIME-WAIT (2×MSL) → CLOSED
```

Cada sentido se cierra **por separado**: por eso 4 mensajes y no 3.

### c) El `TIME-WAIT` de `2 × MSL` (2 pts)

**El problema que resuelve (1 pt):** un segmento puede **reaparecer** como duplicado tarde
(permanece en la red hasta un MSL). Si el socket se cerrara al cabo de 1 MSL, ese duplicado —con
la misma 4-tupla— podría caer dentro de una conexión **nueva** que reutiliza esos puertos, y
**se interpretaría como dato de la conexión nueva**: corrupción silenciosa.

**Por qué 2 × MSL y no 1 (1 pt):** para garantizar que cuando el socket se libera, **ya no pueda
quedar ningún segmento viejo en vuelo**. Con `2 × MSL` se cubre el máximo tiempo de permanencia
**más** el máximo tiempo de demora en la red. `MSL` = *Maximum Segment Lifetime*.

**Costo (bonus):** retiene un puerto por `2 × MSL` ⇒ es la razón del agotamiento de puertos
efímeros (*ephemeral port exhaustion*).

> **Tope para 8:** los 11 estados (3), el handshake con `SYN` consumiendo un número y los
> números independientes (3), el `TIME-WAIT` con el duplicado tardío y el 2×MSL (2).

</details>

<details><summary><b>T4 — Resolución (10 pts)</b></summary>

### a) Las cinco diferencias (5 pts, 1 c/u)

| # | Aspecto | **UDP** | **TCP** |
|---|---|---|---|
| **(i)** | Conexión | **sin conexión** | **con conexión** (3-vías, 1 RTT) |
| **(ii)** | Cabecera | **8 bytes** (origen 2, destino 2, largo 2, checksum 2) | **20 bytes** mínimo, hasta **60** (lo dice el *data offset*, en palabras de 32 bits) |
| **(iii)** | Identificación | **2-tupla** (IP, puerto) *(el kernel usa la 5-tupla)* | **4-tupla** (IP_o, p_o, IP_d, p_d) |
| **(iv)** | Pérdida | **no la detecta**: el datagrama se perdió y sigue | **la detecta** (ACK + timer + `seq`) y **retransmite** |
| **(v)** | Frontera de mensaje | **sí**: 1 datagrama = 1 mensaje | **no**: flujo de bytes; el `read()` puede devolver medio mensaje o dos |

**El detalle que suma en (ii):** los 20 bytes de TCP son `2` (puerto o) + `2` (puerto d) + `4`
(`seq`) + `4` (`ack`) + `1` (*data offset* + reservado) + `1` (flags) + `2` (`window`) + `2`
(checksum) + `2` (urgente) = 20.

**El detalle que suma en (iii):** un socket **UDP** no conectado es único para toda la máquina,
por eso el servidor DNS (53) atiende a **todos** los clientes. En TCP, cada 4-tupla distinta
necesita **un socket distinto**, y por eso el SO crea uno por `accept()`.

### b) Por qué UDP no puede controlar la congestión, y qué lo resuelve (5 pts)

**Por qué no puede (3 pts):** el control de congestión necesita **información sobre el estado de
la red**, y esa información **solo puede llegar si el otro extremo te la manda**.

```
   Congestión = "los routers están llenando sus buffers"
   PERO un datagrama UDP perdido es AMBIGUO:
     ¿se perdió porque se llenó un buffer?  → SÍ hay congestión
     ¿se perdió por un error de CRC?        → NO hay congestión
     ¿se lo descartó un firewall?            → NO hay congestión
   Y UDP no tiene NINGÚN mecanismo para distinguirlo, porque no hay ACK ni timer.
```

O sea: sin ACK no hay **observación**; sin observación no hay **estimación**; sin estimación no
hay control.

**Qué lo resuelve (2 pts):** **QUIC** (`RFC 9000`, `RFC 9001`, `RFC 9002`, 2021), transporte de
**HTTP/3** (`RFC 9114`).

⚠️ **La corrección conceptual importante frente a 2012:** HTTP/3 **no es "HTTP/2 usando UDP"**.
QUIC **reemplaza a TCP por completo**: no hay handshake de 3 vías, no hay conexión TCP, no hay
retransmisión de conexión. La pérdida se resuelve **por stream**. QUIC implementa **fiabilidad,
control de congestión, control de flujo y PLPMTUD** encima de UDP, y usa **TLS 1.3 en los frames
`CRYPTO`** (no en un stream de bytes), lo que además impide que un middlebox que solo entienda
TCP/TCP pueda inspeccionarlo.

**La lección de fondo:** la ausencia de control de congestión en UDP no es un descuido, es **la
razón por la que UDP es simple**; y la razón por la que Internet necesitó una capa que lo
arreglara **es también** la razón por la que existen HTTP/3 y QUIC.

> **Tope para 10:** las cinco diferencias con sus números (5), los tres pasos del "por qué no
> puede" (3), QUIC con la corrección de que **reemplaza** a TCP (2).

</details>

<details><summary><b>T5 — Resolución (8 pts)</b></summary>

### a) Por qué la afirmación es falsa (3 pts)

**El error conceptual (1 pt):** el flag **PUSH no define fronteras de mensaje**. Es **un bit**,
y no existe ningún otro campo en la cabecera que diga "este `read()` debe terminar acá".

**Las tres razones concretas (2 pts):**

1. **TCP es un flujo de bytes.** Por diseño no tiene **mensajes**, tiene bytes. La capa de
   aplicación no ve segmentos: ve una cola de bytes.
2. **Los límites de segmento son invisibles para la aplicación.** Si llegan dos segmentos con
   PSH **en orden inverso** (por reordenamiento), cuando llega el primero el buffer queda
   **contiguo** y un **único** `read()` devuelve **los dos mensajes pegados**.
3. **La segmentación multiplica el efecto.** Si un mensaje es más grande que el MSS queda
   partido en varios segmentos, y el PSH final llega después de bytes ya almacenados.

```
   A: write("hola") → write("chau")         ← dos mensajes de la aplicación
   ┌────────────────┬────────────────┐
   │ "hola"  PSH=1  │ "chau"  PSH=1  │         ← dos segmentos
   └────────────────┴────────────────┘
   B: read() → "holachu"  ← UN read(), dos mensajes  ✗
```

### b) El procedimiento de laboratorio (3 pts)

**Se pide construir un bridge** que interconecte origen y destino y manipule el orden y la
segmentación. Es factible: un bridge es software, y el reordenamiento se implementa con un
**buffer de retardo**.

**(a) Arribo simultáneo de dos mensajes.** El bridge retiene el segmento del mensaje 1 y deja
pasar primero el del mensaje 2:

```
   A ──[MSG1 seq=1000 len=4, PSH]──▶   ┌──────────┐
                                       │  BRIDGE  │ retiene MSG1
   A ──[MSG2 seq=1004 len=4, PSH]──▶   │ (reordena)│──▶ MSG2 primero
                                       └──────────┘
   B: buffer = ["chau"]          ← PSH de MSG2, pero falta MSG1 → NO entrega
   B: buffer = ["hola","chau"]   ← llega MSG1: contiguo
   B: read() → "holachu"         ← UN read(), dos mensajes  ✗
```

**(b) Arribo de un mensaje y parte del siguiente.** Igual, pero el bridge además **parte** el
segundo mensaje y deja pasar primero su primera mitad:

```
   A ──[MSG1 seq=1000 len=4, PSH]──▶   ┌──────────┐
   A ──[MSG2 seq=1004 len=8, PSH]──▶   │  BRIDGE  │──▶ [MSG2 parte 1: "chau c"]
                                       │ (retiene  │──▶ (después) [MSG1 completo]
                                       │  MSG1)    │
   B: buffer = ["chau c"]              ← fuera de orden, NO entrega
   B: buffer = ["hola","chau c"]        ← contiguo → read() = "hola" + "chau c"
```

**El detalle que hace el experimento correcto (1 pt):** el `seq` de los segmentos tiene que ser
**coherente y contiguo** (`MSG2` con `seq = 1004` va justo después de `MSG1`), porque si no el
receptor lo descartaría por estar fuera de ventana y el experimento no probaría nada.

### c) La práctica correcta y un protocolo con noción de mensaje (2 pts)

**La práctica correcta (1 pt):** **poner la frontera en la capa de aplicación**. Tres formas
clásicas:

```
   ① Prefijo de LONGITUD:  [4 bytes: largo][datos...]  → DNS, y las RPC con marshalling
   ② DELIMITADOR:          línea terminada en \r\n     → HTTP, SMTP, POP3
      ⚠️ por eso SMTP y POP3 usan CRLF.CRLF (es 2008-12 P4)
   ③ AUTO-DELIMITACIÓN por longitud mínima + separador → JSON sobre líneas
```

Por eso **HTTP tiene `Content-Length`** (o `Transfer-Encoding: chunked`): es la frontera de
mensaje, porque PUSH no lo es.

**El protocolo con noción nativa de mensaje (1 pt):** **SCTP**. A diferencia de TCP, conserva
las fronteras de mensaje: cada *message* llega como una unidad. Por eso **WebRTC lo eligió para
sus canales de datos**, donde importar un mensaje a medias es inaceptable. ✅ *tema en desuso
como respuesta a un examen de 2011, pero es la solución real hoy.*

> **Tope para 8:** el error conceptual + las tres razones (3), los dos escenarios del laboratorio
> con los `seq` coherentes (3), la práctica de aplicación + SCTP (2).

</details>

<details><summary><b>Problema 1 — Resolución (30 pts)</b></summary>

### a) Los eventos de pérdida (6 pts)

**En un protocolo sin notificaciones explícitas (sin ECN), la pérdida se infiere de dos eventos:**

```
   ┌──────────────────────────────────────────────────────────────────┐
   │ 1. TIMEOUT — se venció el timer esperando una confirmación       │
   │    → no llegó ni la confirmación del segmento siguiente          │
   │      ⇒ pérdida GRAVE, o la ruta se cayó                          │
   │                                                                  │
   │ 2. TRES ACKs DUPLICADOS                                         │
   │    → el siguiente SÍ llegó ⇒ pérdida AISLADA, la red aguanta    │
   └──────────────────────────────────────────────────────────────────┘
```

**La distinción y la ventana (3 + 3 pts):**

| | **3 ACKs duplicados** | **Timeout** |
|---|---|---|
| Qué evidencia | el resto de la ventana llegó igual | no llegó nada |
| Gravedad | **leve**: pérdida aislada | **grave**: masiva o ruta caída |
| `cwnd` nuevo | **`cwnd / 2`** (se parte por la mitad) | **1 MSS** |
| Régimen | sigue en evitación de congestión | vuelve a **arranque lento** |
| Latencia | **1 RTT** (inmediato) | **RTO** (lento) |

**El `umbral` en los dos casos (1 pt de los 6):** `umbral = cwnd_antes / 2`. Es el mismo en
ambos: el punto donde la red empezó a fallar es al que conviene no volver a pasar de una.

⚠️ **La asimetría que más se confunde:** con **3 dupACKs**, **Tahoe** y **Reno** difieren (Tahoe
va a 1 MSS, Reno a `cwnd/2`); con **timeout**, **ambos van a 1 MSS**. Este enunciado pide
explícitamente "un MSS" para congestión, así que la respuesta es **1 MSS en los dos casos**.

**Con ECN hay una tercera vía (bonus):** el router marca `CONGESTION_EXPERIMENTADA` (CE) y eso
**no** es pérdida: no hay paquete perdido y por eso la reducción **no** tiene que ser a 1 MSS.

### b) `detectarCongestion` (12 pts)

```c
/* ---- Estado que persiste entre llamadas (por conexión) ---- */
static long ultimo_ack = -1;      // último numero_confirmacion que vimos avanzar
static int  dupACK        = 0;    // ACKs duplicados consecutivos
#define MSS              1460    // MSS típico en Ethernet; el enunciado no lo da
#define UMBRAL_DUPACK    3

/* Corre en AMBOS extremos: mismo código, roles simétricos. */
int detectarCongestion(Segmento s)
{
    int hayCongestion = 0;                       // 0 = todo bien, 1 = congestión

    if (s == NULL) {
        /* --- Evento 1: TIMEOUT. La señal MÁS grave: o se perdió todo,
               o la ruta se cayó. La forzamos al umbral para unificar el if. --- */
        dupACK        = UMBRAL_DUPACK;
        hayCongestion = 1;
        dupACK        = 0;   // el reset de abajo ya consumió el umbral
    }
    else {
        /* --- Evento 2: ACKs duplicados -> fast retransmit --- */
        if (s->numero_confirmacion > ultimo_ack) {
            /* PROGRESO real: hay que resetear el contador, o un ACK viejo
               dispararía una falsa alarma tres RTT después. */
            ultimo_ack = s->numero_confirmacion;
            dupACK     = 0;
        }
        else if (s->numero_confirmacion == ultimo_ack) {
            dupACK++;                     // ACK repetido
        }
        /* si numero_confirmacion < ultimo_ack: ACK obsoleto (duplicado de un
           ACK viejo). NO cuenta: ignorarlo evita falsos positivos. */

        if (dupACK >= UMBRAL_DUPACK) {    // >= y no ==: si llegan 4 o 5, no nos escapamos
            hayCongestion = 1;
            dupACK        = 0;            // se rearma para la próxima ráfaga
        }

        /* --- Evento 3: ECN, visto POR EL RECEPTOR.
               El router marcó CE. Avisamos al emisor poniendo la marca en lo
               que mandemos de aquí en más. --- */
        if (s->encapsulated.estado_ecn == CONGESTION_EXPERIMENTADA) {
            setNotificarPerdida();
        }
    }

    /* --- Evento 4: ECN, visto POR EL EMISOR.
           El otro ya nos puso la marca: congestión EXPLÍCITA, sin pérdida. --- */
    if (s != NULL && s->marca_perdida) {
        hayCongestion = 1;
    }

    return hayCongestion;
}
```

**Reparto de los 12 puntos:**

| Requisito del enunciado | Dónde está | Pts |
|---|---|---|
| (i) detectar los ACKs duplicados | `== ultimo_ack → dupACK++` y `>= UMBRAL_DUPACK` | 3 |
| (ii) **resetear el contador con progreso real** | `> ultimo_ack → dupACK = 0` | 3 |
| (iii) propagar la marca de "hubo pérdida" | `s->marca_perdida → hayCongestion = 1` | 3 |
| (iv) avisar al otro si llegó marcado por un router | `estado_ecn == CONGESTION_EXPERIMENTADA → setNotificarPerdida()` | 3 |

**⚠️ Tres decisiones que hacen la diferencia entre 9 y 12:**

1. **`>= UMBRAL_DUPACK` y no `==`.** Si llegaran 4 o 5 duplicados seguidos, con `==` te escapás.
   Es robustez, no resultado.
2. **`s == NULL` → no tocar `s->encapsulated`.** Con `s == NULL` no hay cabecera IP: hacer
   `s->encapsulated...` sin proteger es un **null-dereference**. Por eso la vía de ECN está
   **dentro del `else`**.
3. **ACK obsoleto ignorado.** Sin ese `else`, un ACK viejo podría incrementar el contador.

**Variante más robusta del timeout (bonus):**

```c
    bool porTimeout = (s == NULL);
    ...
    if (porTimeout || dupACK >= UMBRAL_DUPACK) { hayCongestion = 1; dupACK = 0; }
```

Funciona igual y **no depende del valor del umbral**: si mañana es 4, no se rompe.

### c) `controlarCongestion` (12 pts)

```c
/* ---- Estado persistente ---- */
enum { ARRANQUE, EVITACION } regimen = ARRANQUE;  // el enunciado pide arrancar en slow start

void controlarCongestion(int hayCongestion)
{
    if (hayCongestion == 1) {

        /* ======== CONGESTIÓN detectada ======== */

        /* Guardamos la mitad de la ventana ACTUAL como umbral: es el punto
           donde la red empezó a fallar, así que es al que no conviene volver. */
        setUmbral(getVentanaCong() / 2);

        /* El enunciado pide volver al régimen de arranque, así que fijamos
           UN MSS. Esto es lo que hacen Tahoe y Reno ante un TIMEOUT.
           Con 3 dupACKs en Reno sería setVentanaCong(getUmbral()). */
        setVentanaCong(MSS);

        regimen = ARRANQUE;
    }
    else {

        /* ======== sin congestión: CRECEMOS la ventana ======== */

        if (regimen == ARRANQUE) {
            /* Por cada confirmación recibida sumamos 1 MSS (lo que pide el
               enunciado). En un RTT llegan cwnd/MSS confirmaciones, así que
               el incremento por RTT es MSS · (MSS/MSS) = MSS: LINEAL. */
            setVentanaCong(getVentanaCong() + MSS);

            /* Al superar el umbral, el crecimiento pasa al otro régimen. */
            if (getVentanaCong() >= getUmbral()) {
                regimen = EVITACION;
            }
        }
        else { /* EVITACION */
            /* +1 MSS por RTT, repartido entre las cwnd/MSS confirmaciones:
                 (MSS) / (cwnd/MSS) = MSS²/cwnd por confirmación
               y en el RTT: (cwnd/MSS)·(MSS²/cwnd) = MSS. Cuadra. */
            setVentanaCong(getVentanaCong()
                           + (MSS * MSS) / getVentanaCong());
        }
    }
}
```

**Reparto de los 12 puntos:**

| Caso | Qué tiene que estar | Pts |
|---|---|---|
| **Congestión** | `umbral = ventana/2` **y** `ventana = MSS` **y** volver a `ARRANQUE` | 4 |
| **Sin congestión, ARRANQUE** | `ventana += MSS` por confirmación | 3 |
| **Sin congestión, EVITACION** | `ventana += MSS²/ventana` por confirmación | 3 |
| **Transición de régimen** | `if (ventana >= umbral) → EVITACION` | 2 |

**Tabla de verificación** — corréla a mano antes de entregar, porque es donde se cuelan los
errores de signo:

```
   MSS = 1460,  umbral inicial = 64 000,  ventana = 1460,  regimen = ARRANQUE

   RTT 1: 1460 + 1460 = 2920    < 64 000  → sigue ARRANQUE
   RTT 2: 2920 + 1460 = 4380    < 64 000  → sigue ARRANQUE
   RTT 3: 4380 + 1460 = 5840    < 64 000  → sigue ARRANQUE
   RTT 4: 5840 + 1460 = 7300    < 64 000  → sigue ARRANQUE
   RTT 5: 7300 + 1460 = 8760    < 64 000  → sigue ARRANQUE

   Ahora: hay congestión.
   umbral  = 8760 / 2 = 4380
   ventana = 1460 (un MSS)
   regimen = ARRANQUE

   RTT+1: 1460 + 1460 = 2920;  2920 <  4380 → sigue ARRANQUE
   RTT+2: 2920 + 1460 = 4380;  4380 >= 4380 → pasa a EVITACION
   RTT+3: 4380 + (1460·1460)/4380 = 4380 + 486 = 4866
          ⚠️ con división entera en C da 486, no 486,6. En producción se
          acumula el residuo (o se usa coma flotante).
```

> ⚠️ **Sobre la división entera:** `(MSS*MSS)/ventana` en C entero trunca: con `MSS = 1460` y
> `ventana = 4380` da `486`. La solución oficial tiene el mismo problema. **Mencionarlo suma**:
> dice que entendiste el algoritmo.

> ⚠️ **Sobre el enunciado:** pide "+ MSS por confirmación" en ARRANQUE, lo que da crecimiento
> **lineal**, no el **exponencial** clásico de Tahoe (que sería `MSS²/ventana` en ambos
> regímenes). Si tu respuesta usa `MSS²/ventana` en los dos, **decí por qué** — está bien
> argumentado.

### d) Cómo se combinan ambas ventanas (2 pts)

```
   ventana efectiva = min( cwnd , rwnd )
```

**Si alguien las sumara** (`cwnd + rwnd`), el excedente que la red no pudo tomar **se acumularía
en el buffer del receptor y lo desbordaría** — y lo desbordaría **justo cuando la red va peor**,
que es justo cuando el buffer del receptor está más lleno. El mínimo es lo único que garantiza
que **nadie se desborda**: ni la red (por `cwnd`) ni el receptor (por `rwnd`).

> **Tope para 30:** (a) 6 con los dos eventos, la distinción grave/leve y los valores de
> `cwnd`; (b) 12 con los cuatro requisitos y los comentarios explicando el porqué; (c) 12 con
> los tres casos y la transición; (d) 2 con el `min` y el argumento del desbordamiento.

</details>

<details><summary><b>Problema 2 — Resolución (30 pts)</b></summary>

### a) Los números y el intercambio sin pérdidas (8 pts)

**Los cinco segmentos.** El `seq` avanza 24 cada vez (el `seq` es el número del **primer byte**):

```
   ┌───────────┬────────────┬───────────────────┬────────┐
   │ Segmento  │ seq        │ Bytes que cubre   │ Largo  │
   ├───────────┼────────────┼───────────────────┼────────┤
   │ S1        │  7000      │ 7000 … 7023       │ 24     │
   │ S2        │  7024      │ 7024 … 7047       │ 24     │
   │ S3        │  7048      │ 7048 … 7071       │ 24     │
   │ S4        │  7072      │ 7072 … 7095       │ 24     │
   │ S5        │  7096      │ 7096 … 7119       │ 24     │
   └───────────┴────────────┴───────────────────┴────────┘
```

**El total:** `5 × 24 = 120` bytes, del **7000** al **7119**. El próximo byte que B espera es
**7120**.

**Las confirmaciones** (una por segmento, como en la solución oficial de `2011-03 P4`):

```
   A1: numero_confirmacion = 7024      confirma S1
   A2: numero_confirmacion = 7048      confirma S2
   A3: numero_confirmacion = 7072      confirma S3
   A4: numero_confirmacion = 7096      confirma S4
   A5: numero_confirmacion = 7120      confirma S5
```

**El diagrama:**

```
    A  (5000)                         Red                        B  (80)
     │                                  │                          │
     │─── S1 seq=7000  len=24 ─────────▶│─────────────────────────▶│
     │─── S2 seq=7024  len=24 ─────────▶│─────────────────────────▶│
     │─── S3 seq=7048  len=24 ─────────▶│─────────────────────────▶│  5 segmentos
     │─── S4 seq=7072  len=24 ─────────▶│─────────────────────────▶│  en vuelo
     │─── S5 seq=7096  len=24 ─────────▶│─────────────────────────▶│
     │                                  │                          │
     │                                  │◀──── A1 conf=7024 ───────│
     │                                  │◀──── A2 conf=7048 ───────│
     │                                  │◀──── A3 conf=7072 ───────│
     │                                  │◀──── A4 conf=7096 ───────│
     │                                  │◀──── A5 conf=7120 ───────│
     │                                  │                          │

   rcv_nxt: 7000 →7024→7048→7072→7096→7120

   Estado final: LastByteAcked = 7120 = LastByteSent → 0 bytes en vuelo
                 ni A ni B tienen nada más que enviar   ✔ fin
```

**Los campos de la cabecera (2 de los 8 puntos):**

```
   Segmento de A → B:
   ┌─────────────────────────────────────────────────────────────┐
   │ puerto_origen = 5000   puerto_destino = 80                 │
   │ numero_secuencia = <7000|7024|7048|7072|7096>              │
   │ numero_confirmacion = <lo que B haya confirmado>            │
   │ flags = ACK    longitud_ventana = rwnd de B                │
   │ cantidad_datos = 24                                         │
   └─────────────────────────────────────────────────────────────┘

   Confirmación de B → A:
   ┌─────────────────────────────────────────────────────────────┐
   │ puerto_origen = 80     puerto_destino = 5000               │
   │ numero_secuencia = <n° propio de B>                        │
   │ numero_confirmacion = <7024|7048|7072|7096|7120>           │
   │ flags = ACK    cantidad_datos = 0                          │
   │ longitud_ventana = rwnd de B   ← esto es CONTROL DE FLUJO  │
   └─────────────────────────────────────────────────────────────┘
```

**Suposiciones que hay que declarar (el enunciado las pide):**

1. `cwnd` de A ≥ 5 MSS, así que los 5 segmentos salen **juntos**. La ventana de 32 KB
   (`32 768 B > 120 B`) lo permite de sobra.
2. `rwnd` de B ≥ 120 bytes.
3. Latencias iguales ⇒ las confirmaciones vuelven **en orden**.
4. El timer es mayor que el tiempo de la primera confirmación (del enunciado) ⇒ **no hay
   retransmisión** en este apartado.
5. **El puerto de B es 80** (HTTP): es totalmente normal que sea el servidor.

⚠️ **Salvedad que suma:** con *delayed ACK* las confirmaciones serían `7024`, `7072`, `7120`
(una confirma S1+S2, otra S3+S4, otra S5). **Declaralo** si lo usás: el resultado es equivalente
porque el ACK es acumulativo.

### b) El intercambio con S1 perdido (10 pts)

**Por qué B no puede confirmar nada.** B recibe S2..S5 pero **ninguno empieza en 7000**, que es lo
que espera (`rcv_nxt = 7000`). Los cuatro quedan fuera de orden, `rcv_nxt` **no se mueve**, y B
manda **el mismo** ACK cuatro veces:

```
   ┌─────────────────────────────────────────────────────────────┐
   │ A0: numero_confirmacion = 7000   "sigo esperando el 7000"  │
   └─────────────────────────────────────────────────────────────┘
```

**El diagrama:**

```
    A  (5000)                         Red                        B  (80)
     │                                  │                          │
     │─── S1 seq=7000 len=24 ─────────▶│── ✗ ✗ ✗ (se pierde) ───│
     │─── S2 seq=7024 len=24 ─────────▶│─────────────────────────▶│  ✗ fuera de orden
     │─── S3 seq=7048 len=24 ─────────▶│─────────────────────────▶│  ✗ fuera de orden
     │─── S4 seq=7072 len=24 ─────────▶│─────────────────────────▶│  ✗ fuera de orden
     │─── S5 seq=7096 len=24 ─────────▶│─────────────────────────▶│  ✗ fuera de orden
     │                                  │                          │
     │                                  │◀──── A0 conf=7000 ───────│  dup
     │                                  │◀──── A0 conf=7000 ───────│  dup
     │                                  │◀──── A0 conf=7000 ───────│  dup
     │                                  │◀──── A0 conf=7000 ───────│  dup  ← ¡el 3º!
     │                                  │                          │
     │  ¡3 ACKs DUPLICADOS!              │                          │
     │  → FAST RETRANSMIT               │                          │
     │─── S1' seq=7000 len=24 ─────────▶│─────────────────────────▶│  ✓
     │                                  │  B tiene 7000..7119      │
     │                                  │  todo CONTIGUO           │
     │                                  │◀──── conf=7120 ──────────│  ✔ un solo ACK
```

**Los dos eventos que pueden provocar la retransmisión (3 pts) — los dos, hay que nombrarlos:**

```
   ┌────────────────────────────────────────────────────────────────┐
   │ (a) LLEGADA DEL TERCER ACK DUPLICADO  →  fast retransmit       │
   │     más rápido (≈1 RTT), la ventana baja a la MITAD            │
   │                                                                │
   │ (b) VENCIMIENTO DEL TIMER de S1  →  retransmisión             │
   │     más lento (espera el RTO), la ventana baja a 1 MSS         │
   └────────────────────────────────────────────────────────────────┘
```

**La ventana de congestión en cada uno (4 pts):**

| | **(a) 3 dupACKs** | **(b) Timeout** |
|---|---|---|
| Interpretación | pérdida **aislada**: la red aguantó | pérdida **grave**: no llegó nada |
| `umbral` | `cwnd/2` | `cwnd/2` |
| `cwnd` nuevo | **`cwnd/2`** (Reno) · `1 MSS` (Tahoe) | **`1 MSS`** (Tahoe **y** Reno) |
| Régimen | **evitación de congestión** | **arranque lento** |
| Latencia | **1 RTT** | **RTO** |
| RTO | no se toca | **se duplica** (*backoff*) |

⚠️ **Lo que el enunciado pide explícitamente:** que **qué valor toma la ventana de congestión en
cada uno**. Con **3 dupACKs**, en **Reno** es `cwnd/2` y en **Tahoe** es `1 MSS`; con
**timeout**, **los dos** dan `1 MSS`. Si solo decís "1 MSS", perdés el punto de la distinción.

**Qué pasa cuando llega S1' (3 pts):**

```
   B tenía en su buffer de reordenamiento: S2 (7024..7047), S3 (7048..7071),
                                            S4 (7072..7095), S5 (7096..7119)
   Llega S1' (7000..7023) → el rango 7000..7119 es CONTIGUO
   → B entrega 7000..7119 a la aplicación, ordenado y sin huecos
   → B manda numero_confirmacion = 7120
```

**Un solo ACK final**, no cinco: el ACK acumulativo confirma los 120 bytes de una vez.

**La cuenta total de paquetes (bonus):** en ambos casos, 6 segmentos (5 + 1 retransmisión) + 5
confirmaciones (4 duplicadas + 1 final) = **11 paquetes**; lo que cambia es el **tiempo**.

### c) El campo de longitud de ventana (6 pts)

**Paso 1 — El máximo del campo de 16 bits.**

```
   longitud_ventana: 16 bits → máximo = 2¹⁶ − 1 = 65 535 bytes
```

**Paso 2 — Con la ventana del enunciado.**

```
   ventana del enlace = 32 KB = 32 × 1024 = 32 768 bytes

   32 768 < 65 535   ⇒ el campo de 16 bits PUEDE expresar esa ventana
```

**Paso 3 — Cuántos segmentos de 24 bytes cubre esa ventana.**

```
   El campo window dice "puedo recibir hasta ac bytes a partir del próximo
   que espero". Con window = 32 768:

   32 768 / 24 = 1365,33

   Ojo con el redondeo:
     1365 × 24 = 32 760   (todavía ≤ 32 768)   ← entra
     1366 × 24 = 32 784   (se pasa)             ← no entra

   ⇒ máximo: 1365 segmentos completos de 24 bytes, más 8 bytes de un parcial.

   Y los 120 bytes del apartado (a) entran de sobra:
     32 768 / 120 = 273 segmentos
```

**Paso 4 — Con escalado de ventana (Window Scale).**

```
   El escalado se negocia en el SYN y multiplica el campo por 2^shift.
   Con shift = 7 (habitual en Linux): 65 535 × 2⁷ = 65 535 × 128 = 8 388 480 B ≈ 8 MB
   Con el máximo teórico shift = 14:   65 535 × 16 384 ≈ 1 073 725 440 B ≈ 1 GB
```

**Por qué importa (2 pts de los 6):** con RTT alto y ancho de banda grande, 65 535 es un **techo
real**. Con RTT de 80 ms son `65 535 / 0,080 = 819 kB/s = 6,55 Mbit/s`. El escalado **no es
cosmético**: sin él, un enlace de 100 Mbps es inalcanzable.

### d) El ataque con RST (6 pts)

**Paso 1 — Cuántos números de puerto.**

```
   Puertos TCP posibles = 2¹⁶ = 65 536

   ⇒ En el peor caso hay que adivinar 65 536 números de puerto.
```

**Paso 2 — Cuántos números de secuencia por puerto.**

```
   espacio de secuencia = 2³² = 4 294 967 296
   ventana del enlace    = 32 KB = 32 768 bytes = 2¹⁵

   paquetes por puerto = 2³² / 2¹⁵ = 2¹⁷ = 131 072
```

⚠️ **El cambio respecto del caso de 16 KB:** como la ventana es **32 KB** (y no 16), hace
falta la **mitad** de paquetes: `2¹⁸ = 262 144` pasó a ser `2¹⁷ = 131 072`. **La cuenta de
potencias es la misma, cambia el exponente.** Es el error más fácil de cometer aquí.

**Paso 3 — Bits totales.**

```
   Cada paquete:  cabecera IP 20 bytes + cabecera TCP 20 bytes (sin datos)
                = 40 bytes = 320 bits = 2⁵ × 2⁵ = 2¹⁰ bits

   Para los 65 536 puertos, cada uno con sus 2¹⁷ números:
   total = 2¹⁶ × 2¹⁷ × 2¹⁰ = 2⁴³ bits

   ⓘ En decimal: 2⁴³ = 8 796 093 022 208 bits
                = 8 796 093 022 208 / 8 = 1 099 511 627 776 bytes ≈ 1,1 TB por puerto
```

**Paso 4 — El tiempo con 100 Mbps.**

```
   t = 2⁴³ bits / 100 000 000 bits/s
     = 8 796 093 022 208 / 100 000 000
     = 87 960,93 s
     = 87 960,93 / 3600 h
     = 24,43 horas
     ≈ 1 día
```

**Desglose paso a paso (lo que hay que escribir en el examen):**

```
   Paso 1: 65 536 puertos                    = 2¹⁶
   Paso 2: 131 072 seq por puerto            = 2³² / 2¹⁵ = 2¹⁷
   Paso 3: 320 bits por paquete              = (20 + 20) bytes × 8 = 2¹⁰
   Paso 4: 2¹⁶ × 2¹⁷ × 2¹⁰                  = 2⁴³ ≈ 8,80 · 10¹² bits
   Paso 5: 8,80 · 10¹² / 10⁸ bits/s          = 87 961 s = 24,4 h ≈ 1 día
```

**Interpretación — y el detalle que da puntos.** Con la ventana de **32 KB** (el doble que en
`2010-03`) el ataque sigue siendo **inviable**: casi **un día** de transmisión continua y
perfecta. ⚠️ **Pero ojo con el tiempo real:** el atacante también tiene que **medir** si la
conexión cayó, y eso cuesta un ACK o un timeout por intento. **En un examen, calculá el tiempo de
transmisión pura** — es lo que piden — **y mencioná el costo de detección como observación.**

**La defensa (bonus):** el **`ISN` aleatorio** (número de secuencia inicial generado con un PRNG
criptográficamente seguro) hace que el atacante **no pueda predecir** el `seq`, y el ataque real
pasa a requerir **1 intento** en vez de 2¹⁷. Sumado a **PAWS** (`RFC 7323`) y a la **validación de
RST** (*blind reset*), el ataque que sobrevive es el **inyectado desde la red local**, no el
hijack desde Internet — y ese se corta con cifrado (TLS) o control de acceso a nivel de red.

> **Tope para 30:** (a) 8 con los cinco `seq`, los cinco `numero_confirmacion`, el diagrama y los
> campos de cabecera; (b) 10 con los cuatro dupACKs `7000`, el `7120` final, los dos eventos y
> los valores de `cwnd` en cada uno; (c) 6 con `2¹⁶ − 1 = 65 535`, la cuenta de segmentos y el
> efecto del escalado; (d) 6 con `2¹⁶`, `2¹⁷ = 131 072`, `320 bits` y el tiempo.

</details>

---

## 📌 Tablero de respuestas del simulacro (para el auto control)

| Pregunta | Máx. | Lo que no puede faltar |
|---|---|---|
| T1 | 10 | los tres mecanismos · las tres causas indistinguibles · Jacobson/Karels · backoff |
| T2 | 10 | `rwnd`/`cwnd` con quién decide · `min()` justificado · sonda de 1 byte exponencial · 2 pérdidas no congestivas |
| T3 | 8 | los 11 estados · handshake con `SYN` consumiendo un número · `TIME-WAIT` 2×MSL |
| T4 | 10 | 8 vs 20 bytes · 2-tupla vs 4-tupla · por qué no puede controlar congestión · QUIC reemplaza a TCP |
| T5 | 8 | PSH no da fronteras · los dos escenarios del laboratorio · `Content-Length` · SCTP |
| **Teoría** | **40** | **mínimo 15 para aprobar** |
| Problema 1 | 30 | los 2 eventos · los 4 requisitos de `detectarCongestion` · los 3 casos de `controlarCongestion` · el `min` |
| Problema 2 | 30 | los 5 `seq` · los 5 `conf` · los 4 dupACKs · los 2 eventos con `cwnd` · `2¹⁷` y el tiempo |
| **Total** | **100** | **aprobación: 60** |

## ✅ Autoevaluación del bloque

**1.** ¿Cuántos estados tiene la máquina de TCP y cuáles son los dos que casi todos olvidan?

<details><summary>Respuesta</summary>

**11.** Los dos que casi todos olvidan son **CLOSING** (cierre simultáneo: un extremo recibe el
FIN del otro antes que el ACK de su propio FIN) y **LAST-ACK** (mandó su FIN y espera el ACK del
FIN ajeno). Son los dos estados "raros" y por eso son los que se pierden.

</details>

**2.** Un segmento recibido tiene `numero_secuencia = 7024` y 24 bytes de datos. ¿Qué valor
debe traer la confirmación de B, y qué se confirmó con ella?

<details><summary>Respuesta</summary>

`numero_confirmacion = 7048`: "recibí hasta 7047 inclusive". El segmento cubre 7024..7047, así
que está confirmado. El próximo byte esperado es **7048**.

</details>

**3.** ¿Por qué la ventana efectiva es `min(cwnd, rwnd)` y no la suma?

<details><summary>Respuesta</summary>

Porque ambas son **cotas superiores independientes**: no se puede mandar más de lo que la red
aguanta (`cwnd`) ni más de lo que el receptor aguanta (`rwnd`). Con la suma, el excedente que la
red no pudo tomar se acumularía en el buffer del receptor y lo desbordaría **justo cuando la red
va peor**: el peor momento posible. El `min` garantiza que **nadie se desborda**.

</details>

**4.** Un emisor manda un segmento, no recibe ACK y vence el timer. ¿Qué tres cosas pueden
estar pasando?

<details><summary>Respuesta</summary>

(1) Se perdió el **segmento** de datos, (2) se perdió el **ACK**, (3) el ACK no se perdió:
simplemente **tardó**. **TCP no puede distinguirlas**, porque en las tres lo único que observa es
la ausencia del ACK. Por eso la única salida es retransmitir, y por eso hace falta un timer para
decidir **cuándo**.

</details>

**5.** Con 3 ACKs duplicados, ¿qué valor toma `cwnd` en Tahoe y en Reno? ¿Y con timeout?

<details><summary>Respuesta</summary>

Con **3 dupACKs**: Tahoe `cwnd = 1 MSS` (vuelve a arranque lento), Reno `cwnd = cwnd/2` (fast
recovery, no corta la ventana a cero). Con **timeout**: **ambos** `cwnd = 1 MSS`, y además el RTO
**se duplica**. La asimetría es el punto clave del tema.

</details>

**6.** ¿Qué es el BDP y por qué importa?

<details><summary>Respuesta</summary>

**BDP** = *Bandwidth-Delay Product* = `ancho_de_banda × RTT`: los bytes que están "en vuelo" si
el emisor llena el enlace sin pausa. Importa porque **para usar toda la capacidad de un enlace la
ventana tiene que ser ≥ BDP**. Con menos, el enlace queda ocioso: un enlace de 100 Mbps con
ventana de 64 KB y RTT 80 ms rinde 6,55 Mbit/s.

</details>

**7.** Nombra dos razones por las que UDP no puede implementar control de congestión, y qué lo
resuelve hoy.

<details><summary>Respuesta</summary>

(1) **No hay realimentación**: sin ACK no hay observación del estado de la red. (2) **La pérdida
es ambigua**: un datagrama perdido puede ser por buffer lleno (congestión) o por CRC, firewall o
corte de enlace (no congestión), y UDP no tiene forma de distinguirlo. Lo resuelve **QUIC**
(`RFC 9000`/`9001`/`9002`, 2021), transporte de **HTTP/3**, que reimplementa fiabilidad, control
de congestión, control de flujo y PLPMTUD **encima de UDP** y **reemplaza a TCP por completo** (no
es "HTTP/2 sobre UDP").

</details>

**8.** ¿Y qué cambió entre 2011 y 2026 en todo el bloque?

<details><summary>Respuesta</summary>

La **etiqueta normativa** y el **despliegue real**; los **mecanismos** no cambian:

- La especificación de TCP es **`RFC 9293`** (2022), no `RFC 793`.
- El control de congestión por defecto es **CUBIC** (`RFC 9438`, *Standards Track*), no
  Reno/Tahoe; **BBR nunca fue RFC** (`draft-ietf-ccwg-bbr`, y `RFC 8312` **es CUBIC**, no BBR).
- El Initial Window es **10 MSS** (`RFC 6928`), no 1.
- **SACK** (`RFC 2018`) es norma; **Timestamps + Window Scale** (`RFC 7323`) hacen obligatorio
  **PAWS** si se activan.
- **ECN** sigue siendo `RFC 3168` + **`RFC 9768`** (AccECN, 2026); L4S = `RFC 9331`.
- **QUIC** (`RFC 9000`–`9002`) es un transporte completo que compite con TCP, y **MPTCPv1**
  (`RFC 8684`) extiende la fiabilidad a varias rutas.

Los números de secuencia de 32 bits, el ACK acumulativo de bytes, los timers,
Jacobson/Karels, la ventana deslizante, los 4 algoritmos de congestión, los 11 estados y el
`TIME-WAIT` de 2×MSL **se preguntan exactamente igual**.

</details>

## 🔗 Referencias

- **Examen `sirc1103`** — P1 (10) forwarding vs. routing · P3 (6) traceroute · **P4 (10) ★ 4 segmentos de 20 bytes desde 1100** · P5 (10) retardo end-to-end · Problema 1 (30) ECN + pseudocode · Problema 2 (30) NAT + ARP + subredes
- **Examen `sirc1012`** — P1 (8) DNS y TTL · P2 (8) mux/demux UDP · P3 (8) hub vs. switch · **P4 (8) números de secuencia y timers** · P5 (8) IPv6 y ND · Problema 1 (30) `connectCheaper()` con sockets UDP · Problema 2 (30) MTU, fragmentación y Path MTU
- **Examen `sirc1102`** — P1 (10) confidencialidad/integridad/no repudio · P2 (10) DHCP · P3 (10) campos de TCP y UDP · P4 (10) NAT · Problema 1 (30) VoIP con jitter buffer · Problema 2 (30) IP Móvil
- **Examen `sirc1002`** — P2 (8) forwarding vs. routing · P3 (8) paridad 2D · P4 (8) firma digital · P5 (8) jitter
- **Examen `sirc0912`** — P2 (10) fiabilidad en transporte vs. enlace · P3 (8) "hops" como métrica
- **Examen `sirc0907`** — **P1 (10) flujo vs. congestión + detección + si toda pérdida es congestión** · P2 (8) three-way handshake y cuándo usar UDP · P3 (8) ARP · P4 (8) RPF e IGMP · P5 (6) confidencialidad vs. integridad
- **Examen `sirc1003`** — P1 (30) subredes + ARP · **Problema 2 (30) ataque TCP reset** · P5 (8) TCP en inalámbricas
- **Examen `sirc0112`** — Problema 1: dos conexiones por un router que pierde · Problema 2: el flag PUSH
- **Examen `sirc0807`** — P2 (10) los cuatro algoritmos de control de congestión
- **Tanenbaum & Wetherall**, *Redes de computadoras* 5ª ed., cap. 6 completo (pág. ~570–620 del PDF)
- **`RFC 9293`** — TCP (2022, *Internet Standard*) · **`RFC 5681`** — TCP Congestion Control (2009)
- **`RFC 9438`** — CUBIC (2023, *Standards Track*) · **`RFC 6928`** — IW = 10 MSS
- **`RFC 2018`** — SACK · **`RFC 7323`** — Timestamps, Window Scale, PAWS · **`RFC 3168`** + **`RFC 9768`** — ECN y AccECN · **`RFC 9331`** — L4S
- **`RFC 9000`/`9001`/`9002`** — QUIC · **`RFC 9114`** — HTTP/3 · **`RFC 8684`** — MPTCPv1
- **`PLAN-48-CLASES.md`** y **`BANCO-EXAMENES.md`** — dónde está cada problema y qué se preguntaba
- **Clase siguiente:** 24 — La capa de red: las dos funciones (forwarding vs. routing)