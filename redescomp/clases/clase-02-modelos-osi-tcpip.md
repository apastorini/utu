# Clase 2 — Los modelos de capas: OSI y TCP/IP

**Bloque:** A (Fundamentos) · **Semana:** 1 · **Duración estimada:** 110 min
**Correlativa:** Clase 1 (¿qué es una red?) · **Sigue con:** Clase 3 (encapsulación y comparación OSI ↔ TCP/IP)
**Material de referencia:** Tanenbaum cap. 1 §1.4 (pág. ~20 a ~26 del PDF de tu carpeta) · RFC 1122, RFC 8200, RFC 9293, RFC 768

---

## 🎯 Al terminar esta clase vas a poder

1. **Explicar** qué problema resuelve el modelo de capas y por qué la **interfaz** entre capas es la clave de la arquitectura.
2. **Enumerar** las 7 capas de OSI con su **PDU** (unidad de datos de protocolo), sus protocolos representativos y **el problema concreto que resuelve cada una**.
3. **Describir** el modelo TCP/IP diciendo explícitamente por qué hay **4, 5 o 7** capas según el autor que leas, y qué criterio usa cada uno.
4. **Construir** la tabla de comparación OSI ↔ TCP/IP completa y decir **por qué ganó TCP/IP**.
5. **Explicar por qué la unidad de datos cambia de nombre** al bajar de capa (mensaje → segmento → paquete → trama → bit).
6. **Desarrollar** la capa de Presentación con ejemplos concretos: *endianness*, formatos, compresión y cifrado.
7. **Resolver enteros** el Examen `2006-12 P1` y el Examen `2007-03 P1`, con las soluciones oficiales a la vista.

> **Prerequisito del examen:** `2006-12 P1` (5 pts — modelo OSI e hipótesis), `2007-03 P1` (5 pts — modelo TCP/IP), `2011-03 P1` (8 pts — las dos funciones de la capa de red), `2009-02 P2` (10 pts — forwarding vs. routing).

---

# PARTE 1 — TEORÍA

## 1.1 El problema que resuelve el modelo de capas

### El problema

Comunicar dos máquinas por una red es un problema **gigantesco**. Un solo paquete involves decisiones sobre:

- ¿con qué voltaje represento un `1`? ¿con qué ancho de pulso?
- ¿cómo sé dónde empieza y dónde termina una trama?
- ¿cómo llego al host `203.0.113.9` de Montevideo desde uno en Montevideo?
- ¿cómo sé que los 1 500 bytes llegaron todos y en orden?
- ¿qué pasa si elCharacters son un PNG?
- ¿y si el otro host entiende UTF-8 y yo mando ISO-8859-1?

Si **cada comunicación** tuviera que resolver **todas** esas preguntas, no habría redes. Habría que escribir un programa distinto para cada par de máquinas, cada protocolo, cada medio.

### La solución: dividir y especificar

El modelo de capas propone algo que parece obvio una vez que lo oyes pero que no lo es:

```
 ┌──────────────────────────────────────────────────────────────────┐
 │  Dividir el problema en SUBSISTEMAS, y que cada subsistema se   │
 │  comunique con el de arriba y el de abajo ÚNICAMENTE a través   │
 │  de una INTERFAZ definida con precisión.                        │
 └──────────────────────────────────────────────────────────────────┘
```

Cada capa:
- **resuelve un subproblema** y solo ese;
- **usa** un servicio de la capa de abajo;
- **ofrece** un servicio a la capa de arriba;
- **no sabe nada** de lo que hacen las capas de arriba ni de abajo, salvo lo que la interfaz define.

### Por qué la interfaz es la clave

```
   Capa 7  ┌──────────────────────────────────┐
           │  "Te entrego datos de aplicación" │   ← lo que OFRECE
           └──────────────────────────────────┘
   ─────────────────────────────────────────────────  ← la INTERFAZ
           ┌──────────────────────────────────┐
   Capa 6  │  "Datos de presentación"          │   ← lo que USA
           └──────────────────────────────────┘

   La capa 7 sabe que la 6 existe. La 6 sabe que la 7 existe.
   Ninguna de las dos sabe cómo funciona la 5.
```

**Qué compra esto.** Gracias a las interfaces:

- Un fabricante de switches (que implementa capas 1 y 2) **no necesita saber** nada de HTTP. Un fabricante de routers (capas 1 a 3) **no necesita saber** nada de TCP. Se pueden combinar porque la frontera está especificada.
- Se puede **cambiar una implementación** sin tocar las demás. Si el medio pasa de cobre a fibra, cambia la capa 1 y **todo lo demás queda igual**.
- Se puede **especificar y probar** cada capa por separado: un tester que manda tramas Ethernet inválidas está probando la capa 2, no "la red".

**La analogía.** Es el mismo movimiento que el que hizo la ingeniería industrial con la cadena de producción: un tornillo no tiene que saber de qué máquina vino ni a qué máquina va. Lo único que importa es que tenga la rosca estándar. **El estándar de rosca es la interfaz.** Y exactamente igual: un byte que sale de la capa 7 no tiene que saber de qué máquina vino; lo que importa es que cumpla el formato que la capa 6 espera.

### Las dos hipótesis de la ISO (esto es lo que pide el Examen 2006-12)

La ISO no elige las capas por capricho. Hay **dos criterios** explícitos que justifican por qué son 7 y no 4 ni 10:

> **H1.** Las capas deben delimitarse buscando **minimizar el flujo de datos que se intercambia entre capas a través de la interfaz**.
> **H2.** El **número de capas debe ser suficientemente amplio para evitar que diferentes funciones no se requieran colocar en la misma capa**.

**Qué significa H1 y por qué importa.** Si una capa habla mucho con la de arriba, es señal de que la frontera está mal puesta: las dos capas deberían estar fusionadas (o separadas). Un ejemplo: en OSI, la capa de Presentación le pasa "datos de presentación" a la de Sesión, y la de Sesión a la de Transporte. El flujo entre ellas es **el mismo bloque de bytes**, sin ninguna transformación. Por eso la criticism clásica a OSI es que **Presentación y Sesión son separaciones artificiales** que producen mucho tráfico de interfaz para poca funcionalidad. Y esa crítica es **la razón por la que TCP/IP las eliminó**.

**Qué significa H2.** Si metés dos funciones muy distintas en la misma capa, terminás con una capa que hace dos cosas y las hace mal. El ejemplo clásico: en TCP/IP, la capa de Aplicación incluye **HTTP, DNS, SMTP, y también el cifrado (TLS) y la conversión de formatos**, que OSI tenía en 5 y en 6. TCP/IP las fusionó porque en la práctica casi no se usan por separado. H2 dice: eso es un defecto, sí, pero aceptable.

---

## 1.2 El modelo OSI de 7 capas

El modelo OSI (*Open Systems Interconnection*, ISO 7498) es **una arquitectura de referencia**: no es un protocolo, es la especificación de **cómo se especifican** los protocolos. Su valor es que cuando alguien dice "esto es capa 3", todo el mundo sabe de qué habla.

### La tabla que hay que saber de memoria

| # | Capa | **PDU** (*Protocol Data Unit*) | Protocolos representativos | **Qué problema resuelve** |
|---|---|---|---|---|
| **7** | **Aplicación** | **Mensaje** (*message*) | HTTP, DNS, SMTP, SSH, IMAP, FTP | **La red como servicio** para el programa: qué datos pide, con qué sintaxis, con qué semántica |
| **6** | **Presentación** | **Datos de presentación** | Cifrado (TLS/SSL), compresión, JPEG/MPEG, ASCII/Unicode, ASN.1 | **Los datos de un host pueden no ser compatibles con otro**: representación, endianness, formato, cifrado, compresión |
| **5** | **Sesión** | **Datos de sesión** | NetBIOS, RPC, NetBIOS Session Service | **Establecer, mantener y terminar un diálogo** entre dos aplicaciones: sincronización, puntos de recuperación, *checkpoints* |
| **4** | **Transporte** | **Segmento** (*segment*, TCP) / **datagrama de usuario** (UDP) | TCP, UDP, SCTP, QUIC | **Que la aplicación se independice de la red**: entregar a un proceso, con fiabilidad, orden y control de flujo |
| **3** | **Red** | **Paquete** (*packet* / *datagram*) | IP, ICMP, IPv6, ARP, IGMP, IPsec | **Cómo llegar de una red a otra**: direccionamiento lógico, enrutamiento, reenvío |
| **2** | **Enlace de datos** | **Trama** (*frame*) | Ethernet, Wi-Fi 802.11, PPP, HDLC, LLC | **Que dos nodos de un mismo enlace se comuniquen sin errores**: delimitar, detectar errores, ARQ, control de acceso al medio |
| **1** | **Física** | **Bit** | 1000BASE-T, 10GBASE-SR4, RS-232, codificación Manchester, NRZI | **Cómo viajan los bits**: medio físico, señal eléctrica/óptica, conectores, voltajes, sincronismo de reloj |

> La PDU de la capa 7 tiene **dos** nombres según el autor: Tanenbaum la llama **mensaje** (*message*), Kurose la llama **segmento de capa de aplicación**. Si el examen dice "mensaje", usá "mensaje"; si dice "datos", usá "datos de aplicación". Los dos son correctos.

### Lo que hace cada capa, en detalle

## Capa 1 — Física

**Único encargo: que los bits viajen.** Y lo hace sin entender nada de lo que llevan adentro.

- Define el **medio** (cobre, fibra, aire, ondas), los **niveles de señal** (voltajes, intensidades, fases), los **conectores**, la **codificación de línea** (NRZI, Manchester, 4B/5B, PAM-4, 1024-QAM) y el **sincronismo** (de dónde saca el reloj el receptor).
- **No detecta errores**, **no sabe si un bit es el primero de una trama**, **no sabe qué hay en el paquete**.

```
  Dos_bits:  1 0 1 1 0 0 1

  En el cable (cobre):
     +3,3V ─┐     ┌─┐   ┌─┐ ┌───┐   ┌─┐
            │     │ │   │ │ │ │ │   │ │
      0 V ───┴─────┴─┴───┴─┴─┴─┴───┴─┴─┴───
       t →

  En la fibra (luz):
     ╱‾‾╲   ╱╲  ╱╲╱╲  ╱‾╾‾╲  ╱╲  ╱‾‾‾‾‾‾
     1  0   1  1  0  0   1

  En el aire (ondas): una sinusoidal cuya FRECUENCIA o FASE cambia.
  El receptor mira la frecuencia → FSK; la fase → PSK; la amplitud → ASK.
```

**Lo importante:** la capa 1 no distingue `1011001` de `0010011`. Solo ve "hay señal" y "no hay señal", o "la fase está en π" y "la fase está en 0".

## Capa 2 — Enlace de datos

Esta capa resuelve **un problema local**: hacer que **dos nodos vecinos** se comuniquen de forma confiable, aunque el medio sea ruidoso.

- **Framing**: delimitar dónde empieza y termina cada trama (preámbulo, flags, byte stuffing, longitudes).
- **Detección de errores**: CRC-32 (Ethernet), checksum (HDLC), paridad.
- **Control de errores** (ARQ): *Stop-and-Wait*, *Go-Back-N*, *Selective Repeat*.
- **Control de acceso al medio**: CSMA/CD, CSMA/CA, *token passing*, ranuras de tiempo.
- **Direccionamiento físico**: direcciones **MAC** de 48 bits, que son **locales al enlace**: se reescriben en **cada** router.

```
  Trama Ethernet (Clase 38 lo desarrolla entero)

  ┌────────┬─────────────┬─────────────┬──────┬────────┬───────┬─────┐
  │Preámb. │  MAC destino │ MAC origen   │ Tipo │ Datos  │  FCS  │ IFG │ bytes
  │  7+1   │   6 bytes    │  6 bytes    │  2   │46..1500│  4    │ 12 │
  └────────┴─────────────┴─────────────┴──────┴────────┴───────┴─────┘
      │         │             │            │        │         │
      │         │             │            │        │         └─ CRC-32
      │         │             │            │        └─ el PAQUETE IP (o LLC)
      │         │             │            └─ 0x0800 = IPv4, 0x86DD = IPv6, 0x0806 = ARP
      │         │             └─ el emisor (cambia en cada router)
      │         └─ a quién va en ESTE enlace (cambia en cada router)
      └─ 10101010... sirve para que el reloj del receptor se sincronice
```

**Lo que la capa 2 NO hace:** no enruta. Un switch de capa 2 no puede llevar un paquete de la LAN A a la LAN B. Esa es la Pregunta 2 del Examen 2009-02 (Clase 3).

## Capa 3 — Red

Esta capa resuelve **el alcance**: cómo llevar un paquete de **una red a otra**.

- **Direccionamiento lógico**: direcciones **IP**, que son **globales**: **no cambian** de router a router (salvo por NAT, que lo rompe justamente por eso).
- **Reenvío** (*forwarding*): copiar cada paquete al puerto de salida correcto según la tabla.
- **Enrutamiento** (*routing*): calcular esas tablas intercambiando información con los vecinos.
- **Protocolos de control**: ICMP, IGMP, y sobre todo el enrutamiento (OSPF, BGP).
- **Fragmentación y reensamblaje**, y MTU.

```
   Red A 192.168.1.0/24            Red B 10.0.0.0/24
   ┌──────────────────┐            ┌──────────────────┐
   │ H1        R1     │            │    R2        H2  │
   │ .25  ───  .1     │════════════│ .1  ───  .25     │
   │ MAC_A  MAC_R1a   │   enlaces  │ MAC_R2b  MAC_B   │
   └──────────────────┘            └──────────────────┘

   El PAQUETE IP mantiene sus direcciones de origen y destino
   (192.168.1.25 → 10.0.0.25) de extremo a extremo.

   Pero las TRAMAS se reescriben en CADA router:
     enlace A-B:  { MAC_R1a , MAC_R2b , 192.168.1.25 , 10.0.0.25 }
     enlace B-H2: { MAC_R2b , MAC_B   , 192.168.1.25 , 10.0.0.25 }
```

**El punto clave, y es la Pregunta 1a del Examen 2009-12 y toda la Pregunta 2 del 2009-02:**

- La **capa 3 es la primera que puede decir "esto no es para mí"**. La capa 2 solo sabe si el destino es su propio puerto o hay que reenviarlo.
- La **dirección de capa 3 es jerárquica y global** (la IP); la de capa 2 es **plana y local** (la MAC).
- Un router **recibe la trama, quita la cabecera de capa 2, mira la cabecera de capa 3, decide, y arma una trama nueva**.

## Capa 4 — Transporte

Resuelve **el último salto lógico**: llevar los datos de una aplicación a **otro proceso** de la máquina de destino, y que la aplicación **no sepa nada** de la red.

- **Multiplexación por puerto**: qué proceso (navegador, correo, SSH) es el destinatario.
- **Fiabilidad**: números de secuencia, ACKs, *timers*, retransmisiones, control de flujo, control de congestión.
- **Orden**: reordenar lo que llegó desordenado.
- **TCP** =connection-oriented, confiable, con control de flujo y de congestión. **UDP** = sin conexión, sin fiabilidad, mínimo.

**Las dos diferencias con la capa 2, que aparecen en el Examen 2009-12 P2:**

| | Capa 2 (enlace) | Capa 4 (transporte) |
|---|---|---|
| Alcance de la fiabilidad | **Por salto** (*hop-by-hop*) | **Extremo a extremo** (*end-to-end*) |
| Confiabilidad | Sí, **si el medio es ruidoso** | **Siempre**, **aunque la red no lo sea** |
| Estado | No necesita estado entre saltos | Estado de la conexión en **ambos** extremos |
| Numeración | Por trama, en el enlace | Por **bytes**, global al flujo |
| Pérdida | Se detecta y se retransmite **por enlace** | La capa intermedia puede perder y **TCP no se entera** hasta que no llega el ACK |

## Capa 5 — Sesión

Resuelve **el diálogo**:

- **Establecer** la sesión: negociar los parámetros (versiones, opciones, prioridades).
- **Sincronizar**: *checkpoints*, para poder retomar si algo falla.
- **Recuperación**: reenviar solo desde el último checkpoint.
- **Terminar** ordenadamente.

**Ejemplo clásico:** NetBIOS (que_session service) y RPC sobre OSI. **En la práctica no se implementan casi nunca como capa separada**: el trabajo de establecer la sesión lo hace TCP (el *three-way handshake*), y la sincronización la hace TLS (los *record* y las alertas) y HTTP/2 (los *streams*). Por eso OSI "sobran" dos capas.

## Capa 6 — Presentación

**Esta es la capa que más se olvida y la que más puntos da si la desarrollás.** Resuelve el problema de **heterogeneidad de representación**:

> **Los datos de un host pueden no ser compatibles con los de otro**, aunque el bit que llega sea el mismo.

Los cuatro problemas concretos:

### (a) *Endianness* — el orden de los bytes

Un entero de 32 bits con valor `0x12345678` se puede guardar de dos maneras:

```
  Big-endian (network byte order, "orden de red"):
      byte[0]=0x12  byte[1]=0x34  byte[2]=0x56  byte[3]=0x78
      ────────┬────────┬────────┬───────────────
              │        │        │
           MSB (peso  2²⁴)  ...          ...  LSB (peso 2⁰)
      Se transmite el byte de MAYOR peso primero.

  Little-endian ("orden de host", Intel/ARM/x86):
      byte[0]=0x78  byte[1]=0x56  byte[2]=0x34  byte[3]=0x12
      byte de MENOR peso primero.

  ─────────────────────────────────────────────────────────────────
  OJO: si no me decís la endianness, el mismo conjunto de 4 bytes
  puede significar 305 419 896  O  201 8915346.

  DECISIÓN: toda estructura de red (IP, TCP, UDP) es BIG-ENDIAN.
  Por eso htons()/htonl()/ntohs()/ntohl() existen en C.
```

### (b) Formatos de caracteres — codificaciones

Un byte `0xE9` puede ser la `é` en **ISO-8859-1**, otra cosa en **Windows-1252**, y **parte de un carácter** en **UTF-8** (donde un carácter ocupa de 1 a 4 bytes). Si el emisor manda ISO-8859-1 y el receptor asume UTF-8, el receptor ve basura. Es el bug más famoso de la historia de la web ("mojibake").

### (c) Formatos de archivo y de estructura de datos

Una imagen JPEG es JPEG, pero un TIFF tiene muchas variantes; un PDF con referencias cruzadas; un `.tar` con o sin padding; una estructura de protocolo con alineamiento de 4 bytes o con padding a 8. Sin capa de presentación, cada aplicación tiene que reinventar la conversión. La alternativa usual es **un formato estándar único**: JSON, XML, ASN.1, protobuf.

### (d) Compresión y cifrado

- **Comprimir**: si el medio es caro (enlace satelital) o el tiempo es caro (archivos grandes). *JPEG*, *gzip*, *zstd*, *brotli*.
- **Cifrar**: que solo el destinatario entienda. En la práctica, esto vive en **TLS** (`RFC 8446`, actualizado por `RFC 9846` en 2026), que es "presentación" dentro de la capa de aplicación de TCP/IP.

**La respuesta oficial del Examen 2006-12**, textual:

> *"Busca la solución de problemas particulares, que hacen referencia a la semántica y sintaxis de lo enviado. Por ejemplo la resolución de diferentes representaciones entre máquinas (pto flotante), corresponde a esta capa."*

*Análisis:* el ejemplo que da la cátedra es el **punto flotante**: es exactamente el caso de *endianness* + rango + precisión de la representación de un `float`. El mismo `float` de 4 bytes puede ser `3,14159` en un host y otra cosa en otro si difieren en endianness. La oficial también menciona la **semántica y la sintaxis**, que es más amplio que "el byte": la capa 6 no solo traduce bytes, traduce **significados**.

## Capa 7 — Aplicación

El servicio de red, visto por la aplicación. **No es la aplicación misma**: es el **protocolo** con el que la aplicación habla.

- **Modelo**: cliente/servidor o peer-to-peer.
- **HTTP** (web), **DNS** (nombre ↔ dirección), **SMTP/IMAP/POP3** (correo), **SSH** (shell remoto), **FTP** (transferencia de archivos), **DHCP** (configuración).
- **No sabe nada de la red**: la aplicación le da "mandá estos 300 bytes al host X puerto Y" y no sabe si van por fibra, por satélite o por tres enlaces de 2 Gbps.

---

## 1.3 El modelo TCP/IP: por qué hay 4, 5 o 7 capas

Acá está la diferencia de criterio entre autores, y **el examen puede preguntar exactamente esto**.

### Modelo de 4 capas (Kurose y Ross)

```
  ┌───────────────────────────────────┐
  │           Aplicación              │  HTTP, DNS, SMTP, SSH
  ├───────────────────────────────────┤
  │           Transporte              │  TCP, UDP, QUIC
  ├───────────────────────────────────┤
  │             Internet              │  IP, ICMP, ARP
  ├───────────────────────────────────┤
  │          Acceso a la red          │  Ethernet, Wi-Fi, PPP
  │   (física + enlace de datos)      │  medio, NIC, switch
  └───────────────────────────────────┘
```

Kurose **fusiona física y enlace en una sola capa de "Acceso a la red"** porque en su libro ambas se presentan como "cómo llegan los bits al otro lado del cable", sin distinguir demasiado.

### Modelo de 5 capas (Tanenbaum, y las RFC)

```
  ┌───────────────────────────────────┐
  │           Aplicación              │
  ├───────────────────────────────────┤
  │           Transporte              │
  ├───────────────────────────────────┤
  │               Red                │
  ├───────────────────────────────────┤
  │         Enlace de datos           │
  ├───────────────────────────────────┤
  │            Física                 │
  └───────────────────────────────────┘
```

Tanenbaum **mantiene enlace y física separadas** y **colapsa Aplicación, Sesión y Presentación en una sola**. Y lo dice explícitamente en su libro: la capa de aplicación "oculta las diferencias entre sistemas" y los servicios que OSI le asignaba a 5 y 6 "son pocos y con frecuencia innecesarios", así que **la mayoría de los protocolos que usan no implementan una capa de sesión y de presentaciónseparadas**.

**Y lo mismo dicen las RFC**, que es lo que define la arquitectura real de Internet: **`RFC 1122` (*Requirements for Internet Hosts: Communication Layers*) habla de tres capas** (Internet, Transport, Aplicación) más el acceso al medio; y cuando separa, usa **4** (aplicación, transporte, internet, **acceso a red** con enlace y físico dentro). Lo que **no** hacen las RFC es separar sesión y presentación: **no existen**.

### La tabla de las tres lecturas

| Autor / documento | Capas | dónde entran sesión y presentación |
|---|---|---|
| **ISO 7498** | **7** | Son capas 5 y 6, separadas |
| **Kurose y Ross** | **4** | Fusionadas dentro de Aplicación |
| **Tanenbaum** | **5** | Fusionadas dentro de Aplicación |
| **`RFC 1122`, `RFC 8200`** | **4 o 5** | **No existen como capas**; sus funciones viven en Aplicación |

**El criterio de la diferencia, en una frase:**

```
  ┌─────────────────────┬───────────────────────────────────────────┐
  │ Kurose (4)          │ le da más peso a la TEORÍA: qué problema   │
  │                     │ resuelve cada capa y cuántos bits son      │
  │ Tanenbaum (5) / RFC │ el mínimo razonable.                      │
  │ (5)                │                                           │
  │                     │ Kurose CREEE que capa es "lo que el        │
  │                     │ estudiante necesita ver separada" para    │
  │                     │ entender el problema.                     │
  │                     │                                           │
  │                     │ Tanenbaum y las RFC la ven desde el otro  │
  │                     │ lado: "la arquitectura REAL tiene esta     │
  │                     │ forma". En la realidad de Internet no       │
  │                     │ existe ninguna separación sesión/         │
  │                     │ presentación, porque nadie la necesita.    │
  └─────────────────────┴───────────────────────────────────────────┘
```

**⚠️ Para el examen:** si te preguntan "¿cuántas capas tiene el modelo TCP/IP?", la respuesta más segura es **"depende del autor: Kurose describe 4, Tanenbaum describe 5, y el modelo OSI tiene 7"**, y después **explicá por qué la diferencia está en si se separa enlace de física y en si sesión y presentación existen**. Un alumno que dice "5" y explica el criterio suma más puntos que uno que dice "5" sin explicar.

---

## 1.4 Comparación OSI ↔ TCP/IP

### La tabla completa

| OSI | PDU | TCP/IP (Tanenbaum) | Equivalente en Kurose | Qué pasó con la función |
|---|---|---|---|---|
| **7. Aplicación** | mensaje | **Aplicación** | Aplicación | Se mantiene, pero **absorbe** 5 y 6 |
| **6. Presentación** | datos de presentación | ↑ **Aplicación** | ↑ Aplicación | **No existe como capa.** Cifrado en la biblioteca (TLS), compresión y formatos en las propias apps |
| **5. Sesión** | datos de sesión | ↑ **Aplicación** | ↑ Aplicación | **No existe como capa.** Lo hace TCP (establecer) y TLS (sincronizar) |
| **4. Transporte** | segmento | **Transporte** | Transporte | Se mantiene íntegra: TCP, UDP, QUIC |
| **3. Red** | paquete | **Red** | Internet | Se mantiene íntegra: IP, ICMP, ARP |
| **2. Enlace** | trama | **Enlace de datos** | ↑ Acceso a la red | Se mantiene, aunque Kurose la funda con la 1 |
| **1. Física** | bit | **Física** | ↑ Acceso a la red | Se mantiene |

### Por qué la tabla no es simétrica

Las **tres capas bajas** (1, 2, 3) de OSI coinciden **una a una** con TCP/IP. Eso no es casualidad: son las que se diseñaron juntas en ARPANET.

La **asimetría está arriba**. OSI separó en tres capas (Aplicación, Sesión, Presentación) lo que TCP/IP puso en una, y **la práctica_results dio la razón a TCP/IP**: la(session) y la (presentación) casi nunca se usan por separado. Un navegador web no tiene una "capa de sesión" que pueda quitar: el estado de la sesión HTTP vive en la capa de aplicación, y el cifrado vive en una biblioteca (TLS) que la aplicación usa como una función.

### Por qué ganó TCP/IP

Hay cuatro razones, y todas son históricas, no técnicas:

**Razón 1 — La red funcionó antes de que la teoría estuviera completa.** ARPANET se puso en marcha en 1969 con un modelo de capas de 4 niveles. El modelo OSI se terminó de discutir en la ISO en **1977**, ocho años después. Para entonces la red ya existía, ya funcionaba, y ya tenía protocols instalados en cada host. Cambiar el modelo implicaba recablear laInternet.

**Razón 2 — La ISO tardó 20 años en estandarizar la capa 3.** El protocolo de capa 3 de OSI (CLNP, Connectionless Network Protocol) se llegó a proponer, pero **nunca se desplegó** como protocolo de Internet. La realidad es que la capa 3 de Internet se_estandarizó como **IP** en 1981 (RFC 791), y el nombre de "capa 3 de OSI" quedó vacante. Cuando llegó IPv6 (RFC 8200, 2017), seOi Thinking… pero el grupo OSI ya no tenía influencia real sobre el diseño. **En 2026 no existe "IPv6 de OSI": existe IPv6 de IETF.** Ese es el punto.

**Razón 3 — La competencia práctica.** TCP/IP venía de BSD, corriendo gratis en Unix. OSI venía como una norma ISO, y las implementaciones de la ISO costaban dinero. En 1993 el mundo tenía: TCP/IP gratis, IPX de Novell en las LAN de empresas, y OSI como norma de papel. Ganó la que era gratis.

**Razón 4 — La transição total (1983).** El 1 de enero de 1983 ARPANET hizo el "Flags Day": todos los hosts pasaron a TCP/IP. Eso cerró el protocolo de la comunidad OSI y dejó a TCP/IP como el único.

**Lo que hay que decir de OSI sin menospreciarlo:** OSI **sí aportó conceptos que sobrevivieron sin capas propias**:

- **El nombre "capa"** como unidad de diseño, y el **principio de encapsulación**.
- **El lenguaje de "servicio" e "interfaz"** entre capas: capa 4 *usa* un servicio de la 3 y *ofrece* uno a la 5. Ese vocabulario es universal.
- **El concepto de PDU**: "la unidad de datos de la capa N".
- **La comparación explícita** que permite decir "HTTP es un protocolo de capa 7, TCP de capa 4, Ethernet de capa 2".

**La frase resumen:** *OSI es un buen marco de pensamiento; TCP/IP es una buena arquitectura de red. El pensamiento es lo que se enseña; la arquitectura es lo que se despliega.*

---

## 1.5 La PDU: por qué cambia de nombre al bajar de capa

Este es el punto conceptual central, y es lo que convierte "capas" de una lista en un mecanismo.

```
  Un byte de información que va de un proceso a otro. Eso es TODO
  lo que hay. Lo que cambia es el ENVOLTORIO.

  Cap 7  ┌──────────────────────────────────────────────────┐
         │  MENSAJE        500 bytes de datos de la app    │
         └──────────────────────────────────────────────────┘
                              │  la capa 4 le antepone 20 B
  Cap 4  ┌──────────────────────────────────────────────────┐
         │  SEGMENTO  [20 B hdr TCP] [ 500 B payload ]      │  520 B
         └──────────────────────────────────────────────────┘
                              │  la capa 3 le antepone 20 B
  Cap 3  ┌──────────────────────────────────────────────────┐
         │  PAQUETE  [20 B hdr IP] [ 520 B de segmento ]    │  540 B
         └──────────────────────────────────────────────────┘
                              │  la capa 2 le antepone 18 B
  Cap 2  ┌──────────────────────────────────────────────────┐
         │  TRAMA  [14 B MAC] [540 B][4 B FCS] + 8 preamble │  566 B
         └──────────────────────────────────────────────────┘
                              │  la capa 1 codifica
  Cap 1  │  BITS  ·01001100 10010110 00001011 ...           │
         └──────────────────────────────────────────────────┘
```

**Las tres ideas que hay que extraer:**

1. **Es la misma información.** Los 500 bytes de la aplicación son los mismos de punta a punta, byte por byte, atravesando todas las capas. Lo que cambia es el **envoltorio** y el **nombre** que le da la capa que lo está sosteniendo.

2. **El nombre describe la unidad que esa capa manipula.** La capa 2 manipula **tramas**, entonces llama "trama" a lo que tiene en las manos. La capa 4 manipula **segmentos**, entonces llama "segmento" a lo suyo. No son cinco cosas diferentes: son **la misma cosa vista desde cinco puntos de vista**.

3. **Cada capa solo conoce la de arriba y la de abajo.** El router recibe una trama, quita los 18 bytes de capa 2, y lo que le importa son **solo los 20 bytes de cabecera IP**. Los 20 bytes de TCP y los 500 de aplicación **le son indiferentes**: los copia de un lado al otro sin mirarlos. Ese es el significado operativo de la encapsulación.

**La definición formal de PDU** (*Protocol Data Unit*): la unidad de datos que una capa puede enviar o recibir a la capa de arriba o de abajo. Es la unidad **de un protocolo**, y por eso el nombre: *datos de protocolo*.

**En TCP/IP son menos porque hay menos capas**, pero el mecanismo es idéntico:

```
  Aplicación  : MENSAJE  500 B
  Transporte  : (TCP)  520 B      ← el "segmento TCP" de OSI
  Internet    : (IP)   540 B      ← el "paquete" de OSI
  Acceso red  : (Eth)  566 B      ← la "trama" de OSI
```

### ⚠️ Actualización a 2026

**Sigue igual — de memoria, sin dudar:**
- **Las 7 capas de OSI**, en orden y con sus PDU: mensaje, datos de presentación, datos de sesión, segmento, paquete, trama, bit.
- **El orden de las capas de arriba hacia abajo** y que la capa de aplicación es la única que ve la red como servicio.
- **Las dos hipótesis de la ISO** (minimizar el flujo en las interfaces; no mezclar funciones no relacionadas).
- **Que Presentación y Sesión no existen en TCP/IP**, y la razón: casi no se usan por separado.
- **Que el modelo TCP/IP tiene 4 o 5 capas según el autor**, y que la diferencia está en la capa de acceso a la red.
- **Internet ≠ Web.**

**Cambió o se modificó — y acá es donde hay que estar fino:**

- **La capa 4 ya no es solo TCP y UDP.** Hoy hay **QUIC (`RFC 9000`, 2021)** que es un transporte completo con su propia recuperación de pérdida y su propio control de congestión, y que corre sobre UDP. `HTTP/3` (`RFC 9114`, 2022) **reemplaza a TCP por completo**: no hay handshake de 3 vías, no hay conexión TCP, no hay retransmisión de conexión. ⇒ **Si el examen pregunta "¿qué protocolos hay en la capa de transporte?", la respuesta completa es TCP, UDP, SCTP, DCCP y QUIC** — y el dato que suma es que QUIC está implementado en el espacio de usuario, no en el kernel.
- **La capa 3 tiene dos versiones, y solo una es la "de Internet".** `RFC 8200` — *IPv6 Specification* (2017, *Internet Standard*), que **obsolesce `RFC 2460`**. El curso de 2011 enseñaba IPv6 como algo experimental: hoy es obligatorio entender que IPv4 y IPv6 **coexisten** y que la capa 3 tiene dos formatos de cabecera.
- **ARP sigue existiendo en IPv4 y disappeared en IPv6.** En IPv6 lo reemplaza **NDP (Neighbor Discovery)**, que usa mensajes ICMPv6 (`RFC 4443`) en multicast en vez de ARP en broadcast. ⇒ **En IPv6, la capa 3 tiene resuelta la resolución de direcciones a nivel de protocolo, con detección de direcciones duplicadas (DAD) incluida.**
- **El cifrado de la capa de presentación se mudó de sitio dos veces.** En 2011 se enseñaba SSLv3/TLS 1.0-1.2. Hoy la especificación vigente es **TLS 1.3 (`RFC 8446`, 2018), actualizada por `RFC 9846` (jul-2026)**, y **los TLS 1.0 y 1.1 pasaron a *Historic* (`RFC 8996`, 2021)**: no se renegocian. La "capa de presentación" de OSI, si existiera, sería **una biblioteca (TLS) entre la aplicación y el socket**, no una capa.
- **La capa de enlace ya no tiene half-duplex en redes de área local de alta velocidad.** En IEEE 802.3, el **full-duplex point-to-point es obligatorio a 10 Gb/s y más**. Y hay una novelty que contradice la intuición: **IEEE 802.3cg (10BASE-T1S, para automatización industrial) es obligatoriamente half-duplex**. ⇒ **La división "capa 2 = full duplex" ya no es una regla universal.**
- **Los nombres de las capas cambiaron con la documentación de IETF.** `RFC 1122` sigue hablando de "capa Internet", "capa de transporte", "capa de aplicación" y "acceso a la red". Cuando leés una RFC de IETF, **buscá esas palabras**, no "interred".

> **Consecuencia para el examen:** la estructura de capas **no cambió** en 37 años. Lo que cambió son **los protocolos que las llenan**. Si te preguntan "¿qué hay en la capa N?", contestá con la tabla de la §1.2 y después aclarás "hoy, además de TCP, QUIC" o "hoy, IPv6". Si te preguntan por el modelo, contestá **la arquitectura**, no las versiones.

---

# PARTE 2 — PRÁCTICA RESUELTA

## 2.1 Ejercicio 1 — ¿En qué capa vive cada cosa? (el ejercicio diagnóstico más útil)

**Enunciado.** Ubicar en la capa OSI y en la capa TCP/IP: (a) la dirección MAC; (b) la dirección IP; (c) el número de puerto 443; (d) el `GET /index.html HTTP/1.1`; (e) el CRC-32; (f) el preámbulo `10101010...`; (g) la codificación NRZI; (h) la dirección del registro DNS; (i) el campo `window` de TCP; (j) el `time-to-live`; (k) la tabla de MAC de un switch; (l) el checksum de IP.

**Resolución.**

| Elemento | OSI | TCP/IP | **Por qué** |
|---|---|---|---|
| (a) MAC (48 bits) | **2** Enlace | Acceso a red | Es dirección **de un enlace**: se reescribe en cada router |
| (b) IP (32 bits) | **3** Red | Internet | Es dirección **global**: no cambia de router a router |
| (c) Puerto 443 | **4** Transporte | Transporte | Identifica un **proceso** dentro del host |
| (d) `GET /index.html HTTP/1.1` | **7** Aplicación | Aplicación | Es un mensaje de protocolo de aplicación |
| (e) CRC-32 | **2** Enlace | Acceso a red | Detecta errores **de un enlace**, no del camino |
| (f) Preámbulo `1010...` | **1** Física | Acceso a red | Sincroniza el reloj del receptor: es señal, no datos |
| (g) NRZI | **1** Física | Acceso a red | Es **codificación de línea**: cómo el voltaje representa un bit |
| (h) Registro DNS (nombre → IP) | **7** Aplicación | Aplicación | DNS es un protocolo de aplicación, aunque use la capa 3 por debajo |
| (i) `window` de TCP | **4** Transporte | Transporte | Es **control de flujo** de la conexión |
| (j) TTL de IP | **3** Red | Internet | Evita bucles en la capa que enruta |
| (k) Tabla MAC del switch | **2** Enlace | Acceso a red | Es el estado interno de la función de reenvío |
| (l) Checksum de IP | **3** Red | Internet | Solo verifica **la cabecera**, no los datos |

**Errores típicos:**

- **Meter la MAC en capa 3.** La MAC es de capa 2, siempre. La IP es de capa 3, siempre. Si el examen te da un paquete con IP `192.168.1.5 → 8.8.8.8` y dos MAC distintas en dos enlaces, lo que cambia es la capa 2 y lo que no cambia es la capa 3. Ese es el heart del Examen 2011-03 Problema 2.
- **Decir que el puerto 443 es de capa 7.** El puerto 443 es un **campo de la cabecera TCP o UDP**, o sea **capa 4**. Lo que corre en el puerto 443 (HTTPS) es de capa 7. La distinción esFields vs. contenido.
- **Meter DNS en capa 3.** DNS corre **encima de UDP, que corre encima de IP**. Es de capa 7 aunque su respuesta (la IP del nombre buscado) sea el insumo de la capa 3.

## 2.2 Ejercicio 2 — Las tres formas de decir lo mismo

**Enunciado.** Expresar el mismo hecho de tres maneras, y decir cuál se usa en cada contexto.

**Resolución.**

```
  HECHO: "un router recibe un paquete destined a 10.0.0.7 y lo reenvía
          por la interfaz eth1, porque en la tabla de reenvío el prefijo
          10.0.0.0/8 tiene como siguiente salto 192.168.1.2 y el mejor
          match es de 16 bits."

  DICIÉNDOLO COMO PROTOCOLO (lenguaje de campos):
    ├─ "El paquete tiene TTL=64 y prefijo destino 10.0.0.7.
    │   Tras longest prefix match en la FIB, la entrada winner es
    │   10.0.0.0/8 con next-hop 192.168.1.2 en eth1.
    │   Se decrementa el TTL a 63 y se recalcula el checksum."

  DICIÉNDOLO COMO CAPAS (lenguaje de la arquitectura):
    ├─ "Eso es capa 3: la capa 2 vio la trama, vio que la MAC destino
    │   es la suya, se la entrega a la capa 3, y la capa 3 decide por
    │   la dirección IP. La capa 3 le devuelve a la 2 'mandala por
    │   eth1'; la 2 la arma con la MAC de eth1 y la transmite."

  DICIÉNDOLO COMO FUNCIONES (forwarding vs. routing):
    ├─ "Eso es FORWARDING: la decisión por paquete usando la tabla.
    │   El ROUTING es lo que puso esa entrada en la tabla."
```

**Por qué importa esto.** El mismo paquete se puede describir con tres vocabularios, y cada uno tiene su lugar:

- El **vocabulario de campos** es el de los **exámenes con figuras**: "indique los campos de la trama".
- El **vocabulario de capas** es el de las **preguntas teóricas**: "qué problema resuelve esta capa".
- El **vocabulario de funciones** es el de la Pregunta 1 del Examen 2011-03 y la Pregunta 2a del 2009-02.

**Si entendés los tres, entendiste la arquitectura.** Si entendés solo uno, memorizaste.

## 2.3 Ejercicio 3 — ¿Por qué no existe "capa de presentación" en Internet?

**Enunciado.** La capa de Presentación de OSI resolvería *endianness*, formatos, compresión y cifrado. En TCP/IP ninguna de esas cuatro cosas tiene una capa propia. **Explicá dónde viven hoy cada una, y decí qué consecuencias tiene que no exista la capa.**

**Resolución paso a paso.**

**Paso 1 — ¿Dónde vive cada función hoy?**

| Función | ¿Dónde está en TCP/IP? | Consecuencia |
|---|---|---|
| *Endianness* de **IP, TCP, UDP** | **Ya está resuelto en la capa 3 y 4**: los campos de longitud de más de 8 bits van en network byte order | Ninguna: se resolvió **diseñando el protocolo** |
| *Endianness* de **los datos** | **En la capa 7**: cada protocolo de aplicación define su representación, y las bibliotecas (JSON, protobuf, DER) la normalizan | Cada protocolo define la suya ⇒ **interoperabilidad a mano** |
| Compresión | En la **capa 7**: `Content-Encoding: gzip, br` en HTTP, o en la 4 (TCP no comprime) | El **endpoint** tiene que soportarlo; si no, el mensaje no se entiende |
| Cifrado | En la **capa 7** (TLS) o en la **capa 3** (IPsec) o en la **4** (DTLS sobre UDP) | Ninguna: se resolvió eligiendo **dónde poner el candado** según el caso |
| Formatos de archivo | En la **capa 7**: JPEG es JPEG, y punto | El formato se **normaliza** por consenso, no por capa |

**Paso 2 — La consecuencia de fondo: la "capa de presentación" nunca fue necesaria como capa.**

Cada función tiene **una** implementación natural, y la red la puso ahí:

- *Endianness*: se resolvió una vez y para siempre en la especificación de IP. No hace falta una capa para decir "esto es big-endian".
- Cifrado: **TLS** resuelve confidencialidad + integridad + autenticación a la vez, y es una biblioteca que se usa en la capa 7. Ya no hay "tres capas de OSI" que programar.
- Compresión: hoy se hace en HTTP como una cabecera, y se negocia. Está donde tiene sentido.

**Paso 3 — El costo de que no exista la capa, que es lo que hay que decir para el punto extra.**

La capa de Presentación de OSI, si existiera, sería **un punto único donde todas las heterogeneidades se resuelven**. Sin ella:

- **Cada aplicación resuelve su propia heterogeneidad**, y eso se nota: un archivo CSV con `;` en vez de `,` rompe un importador. Un JPEG progresivo no lo abre un visor de 2005. Un `float` de 8 bytes en little-endian donde se esperaba 4 en big-endian.
- **No hay un punto único donde auditar la confidencialidad**: si cifrás en la aplicación, el proxy de la empresa no puede inspeccionar; si cifrás en la capa 3 (IPsec), el proxy tampoco.
- **La interoperabilidad es un trabajo manual**, no una propiedad de la arquitectura.

**Paso 4 — Y el contraargumento, que es lo que hace buena la respuesta.**

La razón por la que **funciona igual** es que la heterogeneidad **se movió hacia arriba y hacia el estándar, no hacia una capa**:

```
  OSIPensaba:  heterogeneidad → CAPA DE PRESENTACIÓN (una sola)
  Realidad:     heterogeneidad → PROTOCOLOS Y FORMATOS (muchos)

  ┌─────────────────────┬───────────────────────────────┐
  │ OSI                 │ Realidad                       │
  ├─────────────────────┼───────────────────────────────┤
  │ Una capa            │ Muchos formatos estándar:     │
  │ central             │ JSON, protobuf, DER,           │
  │                     │ PEM, X.509, JPEG, PNG, MP4     │
  │ Un punto de fallo   │ Cada uno resuelve SU caso,     │
  │ si no está          │ y ninguno resuelve todos       │
  └─────────────────────┴───────────────────────────────┘
```

**La frase para el examen:** *no tener una capa de presentación no es un defecto de TCP/IP: es el reconocimiento de que la heterogeneidad de representación nunca fue un problema de red, sino un problema de formatos, y se resolvió con formatos estándar en la aplicación.*

---

# PARTE 3 — PROBLEMAS DE EXAMEN DE FING

## 3.1 ⭐ Examen 2006-12, Pregunta 1 (5 puntos) — el modelo OSI y las hipótesis

> **Fuente:** Examen `sirc0612` — 26 de diciembre de 2006, Pregunta 1 (5 puntos).
> **Link:** https://www.fing.edu.uy/inco/cursos/redescomp/examenes/sirc0612.pdf

### Enunciado (texto del examen)

> Describa el modelo de capas OSI, y las capas que lo integran.

> ⚠️ **Nota sobre el puntaje:** el enunciado oficial dice **5 puntos** (verificado en `sirc0612.txt`), no 10. Tomá 5 como referencia.

### Solución oficial (completa)

> El modelo de referencia OSI (OSI - Open System Interconnection presentado por la ISO - International Standard Organization). Modelo utilizado por la mayoría de los diseñadores.
>
> Las hipótesis manejadas para llegar a 7 capas son las siguientes:
> - Las capas deben delimitarse buscando minimizar el flujo de datos que se intercambia entre capas por la interfaz
> - El número de capas debe ser suficientemente amplio para evitar que diferentes funciones no se requieran colocar en la misma capa.
>
> El modelo de referencia OSI:
>
> **Capa Física**
> - Esta capa tiene la tarea de la transmisión de bits a través de canales de comunicación.
> - Esta capa tiene mucho que ver con las interfaces eléctricas y mecánicas para la transmisión de bits.
>
> **Capa Enlace de Datos**
> - La tarea fundamental es tomar un medio de transmisión, y transformarlo en una línea que parezca libre de errores.
> - En general esto involucra generar frames de datos, y chequear la corrección de los frames llegados, así como pedir retransmisión de frames con errores o perdidos.
>
> **Capa de Red**
> - Se encarga de controlar el funcionamiento de la subred.
> - Su tarea fundamental es encaminar paquetes.
>
> **Capa de Transporte**
> - La función básica de la capa transporte es dar un flujo de datos sin errores ni fallas a la capa sesión.
> - Se generará una conexión por donde se transferirá toda la información, garantizando la no existencia de:
>   - perdida de información
>   - duplicación de información.
>
> **Capa de Sesión**
> - Se busca que dos máquinas diferentes puedan establecer sesiones.
>
> **Capa de Presentación**
> - Busca la solución de problemas particulares, que hacen referencia a la semántica y sintaxis de lo enviado.
> - Por ejemplo la resolución de diferentes representaciones entre máquinas (pto flotante), corresponde a esta capa.
>
> **Capa de Aplicación**
> - En esta capa se tratan aplicaciones que se ejecutan en la red.
> - Como ejemplo podemos tomar transferencia de archivo (ejemplo FTP), Correo Electrónico (SMTP), emulador de terminal TELNET.

### Análisis de la solución oficial

**Lo que está muy bien:**

1. **Nombra las dos hipótesis antes de las capas.** Es lo que la pregunta pide: *las hipótesis* que llevan a 7 capas. Muchos alumnos lasListed al final, después de enumerar. La oficial las pone primero, que es lo correcto: primero el criterio, después la aplicación.

2. **La capa de Enlace es la mejor descripción de todas las siete.** *"Tomar un medio de transmisión y transformarlo en una línea que parezca libre de errores"* es una frase excelente: define la capa por **efecto** (que parezca libre de errores) y no por **mecanismo**. Y agrega los tres mecanismos concretos: framing, chequeo, retransmisión.

3. **La capa de Transporte define el objetivo en términos de la de arriba**: *"dar un flujo de datos sin errores ni fallas a la capa sesión"*. Justamente el principio de "cada capa le da a la de arriba lo que esa necesita".

4. **La capa de Presentación da el ejemplo del punto flotante**, que es el mejor ejemplo posible de heterogeneidad de representación.

**Lo que falta o está comprimido — y son los puntos que se ganan:**

1. **No nombra la PDU de cada capa.** La oficial no dice "trama", "paquete", "segmento", "mensaje". **Es el dato más fácil de agregar y el más rápido de verificar: agregalo.**

2. **La capa de Red es muy escueta.** *"Se encarga de controlar el funcionamiento de la subred. Su tarea fundamental es encaminar paquetes."* No menciona: **direccionamiento lógico (IP)**, **reenvío vs. enrutamiento** (que es la Pregunta 1 del Examen 2011-03, 8 puntos), **longest prefix match**, **TTL**.

3. **La capa Física menciona "interfaces eléctricas y mecánicas".** Correcto, pero falta lo que la distingue: **codificación de línea y sincronismo**, y el hecho de que **no detecta errores**. La frase que suma es: *"la capa física no sabe si el bit que acaba de recibir es un dato o un relleno"*.

4. **La capa de Sesión no menciona para qué sirve.** *"Se busca que dos máquinas diferentes puedan establecer sesiones"*. Falta lo importante: **sincronización y puntos de recuperación** (*checkpoints*), que es lo que la distingue de la capa de Transporte (que establece una conexión pero no sincroniza el contenido).

5. **No dice que la ISO no implementa el modelo.** *"Modelo utilizado por la mayoría de los diseñadores"* es cierto y es lo que salva a OSI de ser inútil: **es un modelo de referencia, no una implementación**. Nadie implementa las 7 capas. La frase que suma: *"OSI es un modelo de referencia, una arquitectura para especificar protocolos; ningún producto implementa las 7 capas."*

### Mi respuesta completa (para los 5 puntos oficiales, ampliada)

```
  MODELO OSI (ISO 7498) — arquitectura de REFERENCIA

  LAS DOS HIPÓTESIS que llevan a 7 capas:
   H1. Las capas se delimitan buscando MINIMIZAR el flujo de datos que
       se intercambia entre capas a través de la interfaz.
   H2. El número de capas debe ser lo bastante amplio como para que
       funciones que no se relacionen NO queden en la misma capa.

  ─────────────────────────────────────────────────────────────────

  7. APLICACIÓN      PDU: mensaje/datos
      La red como servicio para el programa.
      HTTP, DNS, SMTP, SSH, FTP.

  6. PRESENTACIÓN    PDU: datos de presentación
      Resuelve que los datos de un host pueden NO ser compatibles
      con los de otro: representación (endianness, punto flotante),
      formato, compresión, cifrado.

  5. SESIÓN          PDU: datos de sesión
      Establecer, mantener y terminar el DIÁLOGO entre dos
      aplicaciones: sincronización y puntos de recuperación.

  4. TRANSPORTE      PDU: segmento (TCP) / datagrama de usuario (UDP)
      Que la aplicación se independice de la red: entrega a un
      proceso, con fiabilidad, orden, control de flujo y de
      congestión.  TCP, UDP.

  3. RED             PDU: paquete / datagrama
      Cómo llegar de una red a otra: direccionamiento lógico (IP),
      reenvío (forwarding) y enrutamiento (routing), TTL.
      IP, ICMP, ARP.

  2. ENLACE DE DATOS PDU: trama / frame
      Que dos nodos de un MISMO enlace se comuniquen sin errores:
      framing, detección (CRC), corrección (ARQ), control de acceso
      al medio.  Direcciones MAC, que son locales al enlace.
      Ethernet, Wi-Fi, PPP.

  1. FÍSICA          PDU: bit
      Que los bits viajen: medio físico, señal eléctrica u óptica,
      conectores, codificación de línea, sincronismo de reloj.
      NO detecta errores, NO sabe qué hay en el paquete.
```

**Qué agregué respecto de la oficial y por qué:**

| Agregado | Por qué suma |
|---|---|
| **La PDU de cada capa** | Es el dato mecánico, y se verifica fácil. 7 datos en una línea cada uno. |
| **"Que parezca libre de errores"** para Enlace | Ya está en la oficial; lo mantuve porque es la mejor frase del conjunto. |
| **La dirección MAC es local al enlace** | Justifica por qué el router reescribe la trama: el puente de la identidad de capa 2. |
| **"No detecta errores"** en Física | Contraste con la capa 2: es lo que hace que la 1 sea tan simple. |
| **Forwarding vs. routing** en Red | Es el contenido de la Pregunta 1 del Examen 2011-03 (8 pts). Decirlo muestra que entendés la capa. |
| **"Modelo de referencia, nadie lo implementa"** | Salva a OSI de ser inútil y es la respuesta a "¿y si OSI es tan bueno?" |

## 3.2 ⭐ Examen 2007-03, Pregunta 1 (5 puntos) — el modelo TCP/IP

> **Fuente:** Examen `sirc0703` — 26 de febrero de 2007, Pregunta 1 (5 puntos).
> **Link:** https://www.fing.edu.uy/inco/cursos/redescomp/examenes/sirc0707.pdf

### Enunciado (texto del examen)

> Describa el modelo de capas TCP/IP.

### Solución oficial (completa)

> El modelo TCP/IP surgió a partir de la red ARPANET, cuyo mayor objetivo de diseño era interconectar varias redes en forma transparente, dicha arquitectura evolucionó en el modelo TCP/IP.
>
> **La capa Host a Red**
> Especifica cómo se envían físicamente los datos a través de la red, que incluye cómo se realiza la señalización eléctrica de los bits mediante los dispositivos de hardware que conectan directamente con un medio de red, como un cable coaxial, un cable de fibra óptica o un cable de cobre de par trenzado. No está definido el protocolo y el mismo puede variar en diferentes implementaciones.
>
> **La capa de Interred**
> Esta capa es la que mantiene unida toda la arquitectura. Permite a los host enviar paquetes a cualquier red y que viajen independientemente del destino (potencialmente otra red). Pueden incluso llegar en diferente orden, en cuyo caso es trabajo de capas superiores, reordenarlos. La capa de interred define un formato de paquetes llamado IP. El trabajo de la capa de interred es que dichos paquetes lleguen a donde corresponde, por lo que el ruteo de los paquetes es el mayor problema. La capa de interred es similar en su funcionamiento a la capa OSI de Red.
>
> **Capa de Transporte**
> Sobre la capa de interred se define la capa de transporte, la misma está diseñada para conectar dos entidades y mantener un enlace de datos. Hay dos protocolos definidos: TCP (Transmission Control Protocol), es un protocolo orientado a conexión, confiable, que permite que un flujo de bytes sea enviado de una máquina a otra sin errores; fragmenta el flujo de bytes y lo pasa a la capa de interred, al llegar a destino reconstruye el flujo de bytes; TCP también maneja el control de flujo para evitar sobrepasar la capacidad de un receptor más lento. El segundo protocolo, UDP (User Datagram Protocol) es un protocolo no confiable sin conexión, para aplicaciones que no necesitan secuenciamiento de paquetes o control de flujo, o aplicaciones donde es más importante transmitir rápido que en forma confiable, como voz o video.
>
> **Capa de aplicación**
> El modelo TCP/IP no tiene capas de sesión o presentación, no se pensó que fueran necesarias, por lo que no fueron incluidas. En la práctica se prueba que son muy poco usadas. Por lo que en el modelo arriba de la capa de transporte se encuentra la capa de aplicación, que contiene todos los protocolos de alto nivel, como TELNET, FTP, SMTP, DNS, NNTP, HTTP, etc.

### Análisis de la solución oficial

**Lo que está muy bien:**

1. **Empieza por el origen histórico**: *"surgió a partir de la red ARPANET, cuyo mayor objetivo de diseño era interconectar varias redes en forma transparente"*. Esa es la razón de diseño de TCP/IP, y es exactamente el criterio de H2 aplicado: la función de la capa de Interred (conectar redes heterogéneas) es **distinta** de la de la capa de Enlace (comunicar dos vecinos), así que van separadas. Si hubieran ido al modelo OSI a ciegas, habrían fusionado red y enlace.

2. **La capa Interred está muy bien descrita**: *"permite a los host enviar paquetes a cualquier red y que viajen independientemente del destino"*, *"pueden incluso llegar en diferente orden, en cuyo caso es trabajo de capas superiores, reordenarlos"*. La observación de que **IP es un servicio sin orden** y de que eso es una decisión de diseño (a cambio de robustez en el camino) vale por sí sola varios puntos.

3. **TCP vs. UDP con la razón de la elección**: UDP es para *"aplicaciones donde es más importante transmitir rápido que en forma confiable, como voz o video"*. La oficial entiende que UDP no es "TCP malo": es una **decisión de diseño** para un caso concreto.

4. **"El modelo TCP/IP no tiene capas de sesión o presentación... en la práctica se prueba que son muy poco usadas."** Esa es la respuesta a la pregunta implícita "¿por qué TCP/IP tiene menos capas?", y la oficial la responde con la evidencia.

**Lo que falta o está comprimido:**

1. **"Host a Red" en vez de "Acceso a red".** Es el nombre de Tanenbaum. Kurose lo llama **"Acceso a la red"** y lo trata como **una** capa que incluye física y enlace. Si el examen dice "4 capas", decí "acceso a red" y aclarás que incluye las dos bajas de OSI. La oficial usa el nombre de Tanenbaum, coherente con que la cátedra usa Tanenbaum como libro de referencia.

2. **La capa Interred no menciona ARP.** Y ARP es de **capa 3** (o de 2½, según el autor: resuelve una dirección de capa 3 con una de capa 2, y por eso Tanenbaum lo pone en la capa de red). La oficial tampoco menciona **ICMP**, que es la otra pieza fundamental de capa 3.

3. **No dice "TCP/IP tiene 4 o 5 capas según el autor".** Este es el punto que la oficial no toca y que un buen examen sí podría pedir. Si la respuesta dice "4 capas" y el libro de la cátedra tiene 5, hay un problema. Hay que resolverlo.

4. **No nombra las PDU.** Mismo faltante que en el 2006-12.

5. **No menciona los otros protocolos de transporte.** Hoy hay **SCTP** y **QUIC** (`RFC 9000`), y QUIC es el dato de 2026.

### Mi respuesta completa (para los 5 puntos)

```
  MODELO TCP/IP — 4 capas (Kurose) o 5 capas (Tanenbaum) según
  cómo se separe la capa de acceso a la red.

  ORIGEN: surgió de ARPANET, cuyo objetivo de diseño era
  interconectar redes HETEROGÉNEAS de forma transparente. Por eso
  la capa de Red (Interred) es distinta de la de Enlace y no
  puede fusionarse con ella.

  ─────────────────────────────────────────────────────────────────

  4. APLICACIÓN
     PDU: mensaje
     Los protocolos de alto nivel: HTTP, DNS, SMTP, FTP, SSH, DHCP.
     NO tiene capas de sesión ni de presentación: sus funciones
     viven acá (el cifrado, en la biblioteca TLS; los formatos, en
     los protocolos de aplicación). En la práctica casi nunca se
     usan por separado, y por eso no se separaron.

  3. TRANSPORTE
     PDU: segmento (TCP) / datagrama de usuario (UDP)
     Conecta dos ENTIDADES (procesos), no dos máquinas. Entrega un
     flujo de bytes de un proceso a otro, independiente de la red.
     - TCP: orientado a conexión, confiable, con control de flujo
       y de control de congestión. Numeración de bytes.
     - UDP: sin conexión, no confiable, mínimo (8 bytes de cabecera).
       Para voz, video y DNS: donde importa la oportunidad más que
       la garantía.
     - SCTP y QUIC (RFC 9000) también son capa 4.

  2. INTERNET / INTERRED
     PDU: paquete / datagrama
     Es la capa que MANTIENE UNIDA la arquitectura: el objetivo
     de ARPANET. Entrega paquetes "best effort" a cualquier
     destino, INDEPENDIENTEMENTE del camino: los paquetes pueden
     perderse, duplicarse o llegar en orden distinto, y eso es
     problema de las capas superiores.
     Define el formato IP. Direccionamiento lógico jerárquico.
     Reenvío (forwarding) y enrutamiento (routing).
     IP, ICMP, ARP (que resuelve IP a partir de la MAC del enlace).
     Es la equivalente a la capa 3 de OSI.

  1. HOST A RED / ACCESO A LA RED
     PDU: trama (enlace) y bit (física)
     Especifica cómo se envían físicamente los datos: señalización
     eléctrica de los bits con el hardware que conecta al medio
     (coaxial, fibra, par trenzado). NO ESTÁ DEFINIDO UN PROTOCOLO
     único: varía por implementación.
     Incluye la capa física (medio, señal, conectores) y la de
     enlace (framing, MAC, CRC, acceso al medio).
```

**Qué agregué respecto de la oficial y por qué:**

| Agregado | Por qué suma |
|---|---|
| **ARP e ICMP en la capa Internet** | Son las dos piezas que hacen que la capa funcione. La oficial solo menciona IP. |
| **"Es la capa que mantiene unida la arquitectura"** | Está en la oficial y es la mejor frase: define la capa por su **para qué histórico**. La repetí arriba porque es el corazón de la pregunta. |
| **"Conecta dos entidades, no dos máquinas"** | Es lo que distingue la capa 4 de la 3, y es lo que justifica que exista como capa separada. |
| **SCTP y QUIC** | El dato de 2026. Si el examen es de la cátedra actual, mentionar QUIC muestra que la lectura es actual. |
| **"NO ESTÁ DEFINIDO UN PROTOCOLO único"** | Está en la oficial y es un punto clave: es la capa donde todo es implementación. |
| **La nota 4 vs. 5** | Resuelve la ambigüedad antes de que te la planteen. |

---

# PARTE 4 — CIERRE

## 📌 Resumen

1. El modelo de capas existe para que **cada subsistema se comunique con el de arriba y el de abajo solo por una interfaz**. Eso permite que un fabricante de switches y otro de routers se entiendan.
2. **H1**: minimizar el flujo de datos a través de las interfaces. **H2**: funciones que no se relacionan no deben estar en la misma capa.
3. **Las 7 de OSI** con su PDU: **Aplicación** (mensaje) · **Presentación** (datos de presentación) · **Sesión** (datos de sesión) · **Transporte** (segmento) · **Red** (paquete) · **Enlace** (trama) · **Física** (bit).
4. **TCP/IP tiene 4 (Kurose), 5 (Tanenbaum) o 7 (OSI)** según el autor: la diferencia está en si se separa enlace de física, y en que **Sesión y Presentación no existen**.
5. **Presentación resuelve que los datos de un host pueden no ser compatibles con los de otro**: *endianness*, formatos, compresión, cifrado. En TCP/IP eso vive en Aplicación (y en TLS).
6. **Sesión** = diálogo: sincronización y puntos de recuperación. **Transporte** = flujo confiable a un proceso. La diferencia es contenido, no transporte.
7. **La PDU cambia de nombre** porque es la misma información con distinto envoltorio y cada capa nombra lo que tiene en las manos.
8. **Ganó TCP/IP** porque la red funcionó antes de que la teoría estuviera lista, porque OSI tardó 20 años en estandarizar la capa 3, porque TCP/IP era gratis, y porque en 1983 nadie quiso dar marcha atrás.
9. **OSI no se implementa**: es un marco de pensamiento. **El vocabulario** (capa, PDU, servicio, interfaz) sí es universal y es lo que hay que aprender.
10. **Internet ≠ Web**: Internet es la red (IP, TCP, BGP); la Web es una aplicación (HTTP, HTML, URL).

## ✅ Autoevaluación

**1.** ¿Por qué el modelo de capas no es "un capricho de la ISO"?

<details><summary>Respuesta</summary>

Porque resuelve un problema real: **la comunicación entre dos máquinas es un problema gigantesco** que involucra decisiones de señal eléctrica, delimitación de tramas, direccionamiento global, fiabilidad, orden, representación de datos y semántica de la aplicación.

Si cada comunicación tuviera que resolver todo eso, habría que escribir un programa distinto para cada par de máquinas, cada medio y cada protocolo. Al dividirlo en subsistemas y especificar **una interfaz entre cada par**, se consigue que:

- un fabricante de switches no sepa nada de HTTP;
- cambiar el cable no obligue a cambiar el software;
- se pueda probar y estandarizar cada capa por separado.

**La interfaz es lo que compra todo**: es el equivalente al estándar de rosca de la industria mecánica.

</details>

**2.** ¿Por qué TCP/IP fusionó Sesión y Presentación en Aplicación, si la hipótesis H2 dice que funciones distintas no deberían estar en la misma capa?

<details><summary>Respuesta</summary>

Porque **H2 es un criterio de diseño, no una ley**, y se aplicó con criterio económico y evidence.

- La evidencia: en la práctica **casi ninguna aplicación implementa sesión y presentación por separado**. El navegador no tiene una "capa de sesión" removible. El cifrado lo hace una biblioteca (TLS) dentro de la aplicación. La compresión es una cabecera HTTP.
- El argumento de H1: como las dos capas casi no hacen nada entre sí (el flujo de datos entre Presentación y Sesión es el mismo bloque de bytes, sin transformación), mantenerlas separadas produce **tráfico de interfaz sin funcionalidad**. Eso es exactamente lo que H1 dice evitar.
- El argumento económico: separar capas cuesta implementación, especificación y coordinación entre стандарт committees. Si la funcionalidad es cero, el costo no se paga.

**La respuesta completa es "H2 tiene una excepción, y la excepción es cuando una de las funciones no se usa"**. OSI se argumenta por qué esas dos capas existían; TCP/IP se argumenta por qué no.

</details>

**3.** ¿Qué es el *endianness* y por qué es problema de la capa de presentación?

<details><summary>Respuesta</summary>

El ***endianness*** es el **orden en que se guardan los bytes de un número multi-byte en memoria**.

```
  0x12345678  en big-endian (network byte order):
      [0x12] [0x34] [0x56] [0x78]

  0x12345678  en little-endian (orden de x86/ARM):
      [0x78] [0x56] [0x34] [0x12]
```

Los mismos 4 bytes significan **305419896** o **2018915346** según el endianness.

Es problema de la capa de presentación porque es un caso exacto de **"los datos de un host pueden no ser compatibles con otro"**: el bit llega perfecto, la red funcionó perfecto, pero el **significado** es otro.

La red resolvió una parte (los campos de IP, TCP y UDP son big-endian por definición, y por eso existen `htons()`/`htonl()` en C), pero los **datos de la aplicación** siguen en el endianness del host, y por eso la biblioteca de cada protocolo tiene que convertir.

</details>

**4.** En el modelo TCP/IP de Tanenbaum, ¿la capa de Enlace existe? ¿Y en el de Kurose?

<details><summary>Respuesta</summary>

- En **Tanenbaum (5 capas)**: **sí**, es la capa 2, separada de la física.
- En **Kurose (4 capas)**: **no como capa independiente**: está fusionada con la física en lo que él llama **"Acceso a la red"** (*Access Network*), que incluye medio físico, señal, conectores, y también framing, MAC, CRC y acceso al medio.

El nombre "Host a Red" que usa la solución oficial del Examen 2007-03 es el de Tanenbaum. Si el examen dice "4 capas", lo coherente es "Acceso a red" (Kurose); si dice "5 capas", "Host a Red" (Tanenbaum).

**Lo que no cambia en ningún autor**: enlace y red van separadas. Y esa separación es la que sostiene la Pregunta 2 del Examen 2009-02 (forwarding vs. flooding) y la Pregunta 2 del Examen 2011-03.

</details>

**5.** Si HTTP es de capa 7 y el puerto 443 es de capa 4, ¿cómo es posible que "HTTPS sea de capa 7"?

<details><summary>Respuesta</summary>

Porque **el puerto 443 es un campo de la cabecera** (capa 4), y **HTTPS es un protocolo completo** (capa 7) que viaja por encima.

```
  HTTPS  = el protocolo de aplicación (capa 7):
           GET / HTTP/2  +  cabeceras +  TLS
                      ↓ viaja en
  TCP    = capa 4:  puerto destino = 443
                      ↓ viaja en
  IP     = capa 3
                      ↓ viaja en
  Ethernet = capa 2
```

Cuando alguien dice "**puerto 443**", se refiere al **número en un campo de la cabecera TCP o UDP**: eso es capa 4. Cuando dice "**HTTPS**", se refiere al **protocolo de aplicación** que usa ese puerto: eso es capa 7, aunque el puerto esté registrado para HTTPS por convención del IANA.

**No hay contradicción**: el protocolo está en la capa 7, y **además** hay un campo en la capa 4 que apunta a él. Es el mismo mecanismo de "el puerto identifica el proceso" que se estudia en la Clase 16.

</details>

**6.** Un paquete que pasa por 5 routers, ¿cuántas cabeceras IP tiene y cuántas tramas Ethernet tiene?

<details><summary>Respuesta</summary>

```
  1 cabecera IP          → la MISMA de punta a punta: no cambia
                           (salvo TTL y checksum, que se reescriben)
  6 cabeceras Ethernet   → UNA POR ENLACE:
      1) H ──► R1        (trama con MAC_H y MAC_R1a)
      2) R1 ──► R2       (trama con MAC_R1b y MAC_R2a)
      3) R2 ──► R3       (trama con MAC_R2b y MAC_R3a)
      4) R3 ──► R4       (trama con MAC_R3b y MAC_R4a)
      5) R4 ──► R5       (trama con MAC_R4b y MAC_R5a)
      6) R5 ──► H'       (trama con MAC_R5b y MAC_H')
  = 6 enlaces, 6 tramas
```

**6 tramas, 1 paquete.** Y esa es exactamente la asimetría fundamental del modelo: **la capa 3 direcciona extremos, la capa 2 direcciona saltos**. Cada router "abre" la trama, saca la PDU de capa 3, le baja el TTL, la mete en una trama nueva con las MACs del siguiente enlace, y la manda.

El TTL va a ser 1 en la última trama (el último router lo decrementa a 0 y lo descarta si no es el destino), así que el **valor del TTL es lo único de la cabecera IP que cambia en tránsito** (más el checksum, que hay que recalcular).

</details>

**7.** El modelo OSI tiene 7 capas y el TCP/IP tiene 4. ¿Cuál es "mejor" y por qué?

<details><summary>Respuesta</summary>

**Ninguno, para su propósito.** Y esa es la respuesta con más puntos.

- **TCP/IP es mejor como arquitectura de red**, porque **funciona**: es lo que se desplegó, es lo que escala a miles de millones de dispositivos, y tiene 37 años de evolución probada en producción.
- **OSI es mejor como marco de pensamiento**, porque separa conceptos que en TCP/IP están mezclados (presentación y cifrado no son la misma cosa; y sin embargo están ambos en Aplicación), y porque da un vocabulario común.

**Lo que hay que decir para cerrar:** OSI no perdió porque fuera peor técnicamente. Perdió porque (1) la red ya existía cuando el modelo se terminó, (2) tardó 20 años en producir un protocolo de capa 3 desplegable, (3) vino con coste de licencia, y (4) en 1983 el mundo entero pasó a TCP/IP.

**Y el dato histórico que lo demuestra**: **no existe "IPv6 de OSI"**. Hay RFC 8200, del IETF. Cuando OSI desapareció del diseño de Internet, nadie lo notó, porque otra capa ya cubría esas funciones. Y eso, en cierto modo, **es el mayor triunfo de la arquitectura OSI**: demostró que las capas esenciales eran correctas, aunque su propio marco quedara en el papel.

</details>

**8.** En el modelo TCP/IP, ¿dónde vive la función "detectar y retransmitir un paquete perdido"?

<details><summary>Respuesta</summary>

**En la capa de Transporte (TCP), no en la capa de Enlace.** Y la razón es un argumento de arquitectura, no de gusto.

La capa de Enlace **sí** detecta y retransmite, pero **por salto** (*hop-by-hop*):

- el enlace (H, R1) detecta que la trama de (H, R1) llegó mal, y la retransmite, y su vida termina ahí;
- si la trama llegó bien a R1 y R1 la mandó a R2, y **se perdió en R2**, entonces la capa de enlace de (H, R1) **nunca se entera**: no hay número de secuencia que atraviese los routers, no hay ACK que vuelva, y no hay forma de distinguir "se perdió" de "tardó".

Para que la fiabilidad funcione **de extremo a extremo**, tiene que estar en una capa que vea **todos** los saltos. Eso es la capa de Transporte.

**Esta es la Pregunta 2 del Examen 2009-12** (10 puntos): *"En una red de paquetes arbitraria, ¿es posible implementar un servicio de transmisión confiable en capa de enlace? Justifique."* La respuesta es **no**, y el argumento es exactamente este.

</details>

## 🔗 Referencias

**Exámenes**
- Examen `sirc0612` (26-dic-2006) — P1 (5 pts): modelo OSI e hipótesis · P2 (10 pts): framing · P4 (10 pts): handshake TCP
- Examen `sirc0703` (26-feb-2007) — P1 (5 pts): el modelo TCP/IP · P4 (10 pts): campos de TCP y UDP
- Examen `sirc1103` (21-feb-2011) — P1 (8 pts): las dos funciones de la capa de red
- Examen `sirc0902` (2-feb-2009) — P2 (10 pts): forwarding vs. routing y flooding
- Examen `sirc0912` (18-dic-2009) — P2 (10 pts): servicio confiable en transporte vs. enlace

**Bibliografía**
- Tanenbaum & Wetherall, *Redes de computadoras*, 5ª ed., **cap. 1 §1.4** "El modelo de capas" (pág. ~20 a ~26 del PDF de tu carpeta) — el modelo de 5 capas y las PDU
- Tanenbaum & Wetherall, **cap. 1 §1.5** "El modelo OSI" — las siete capas y la crítica a OSI
- Kurose & Ross, *Computer Networking: A Top-Down Approach*, cap. 1 — el modelo de 4 capas
- ISO/IEC 7498-1 — *Information technology — Open Systems Interconnection — Reference model* — la norma del modelo OSI

**RFCs**
- `RFC 1122` — *Requirements for Internet Hosts: Communication Layers* (1989): define la arquitectura TCP/IP **con enlace separado** y **sin** capas de sesión ni presentación
- `RFC 8200` — *Internet Protocol, Version 6* (2017, *Internet Standard*): la capa 3 de Internet hoy; obsolesce RFC 2460
- `RFC 9293` — *Transmission Control Protocol* (2022, *Internet Standard*; consolida RFC 793)
- `RFC 768` — *User Datagram Protocol* (1980): la cabecera de UDP en 8 bytes
- `RFC 9000` — *QUIC* (2021): el transporte moderno que **no** es TCP, y que vive en la capa 4

**Clase siguiente:** 3 — Encapsulación y comparación OSI ↔ TCP/IP