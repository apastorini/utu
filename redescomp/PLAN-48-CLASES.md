# Plan de 48 clases — Introducción a las Redes de Computadoras (FING, código 1433)

> **Cómo usar este plan.** 48 clases = 16 semanas × 3 clases. Cada clase tiene:
> teoría (con el *qué* y el *por qué*), práctica resuelta paso a paso con el
> razonamiento explícito, y problemas reales de examen de FING resueltos cuando
> el tema aparece en los exámenes publicados.
>
> **Fuente de verdad:** material oficial de FING (1998–2011) + Tanenbaum &
> Wetherall *Redes de computadoras* 5ª ed. (el PDF de tu carpeta) + clases 2020/2021
> de OpenFING.

---

## Aviso importante: esto es un curso de 2011, y el examen es de hoy

El curso dice textualmente *"A partir de 2012 esta asignatura no se dicta más"*, y
fue reemplazado por *Redes de Computadoras (1446)* y *Aspectos Avanzados de Redes
de Computadoras (1448)*. Eso significa:

- **Los exámenes que te pueden tomar son de otro curso, pero el temario es el mismo.**
  La cátedra que hoy da *Redes de Computadoras* es la misma gente (los mismos
  docentes: Sabiguero, Baliosian, Grampín, Rodríguez, Sanguinetti, Vidal…). Por eso
  el estilo de los problemas es idéntico.
- **Todo el temario "clásico" se sigue preguntando**: capas, retardos, subnetting,
  tablas de enrutamiento, TCP, DNS, HTTP, CRC, CSMA/CA, seguridad. Nada de eso se fue.
- **Lo que cambió** son las versiones de los protocolos. Cada clase tiene una
  sección fija titulada **«⚠️ Actualización a 2026»** que dice exactamente qué sigue
  igual, qué cambió, con qué RFC, y qué te pueden preguntar distinto.

Ver `ACTUALIZACIONES.md` para la tabla completa.

---

## Mapa de la materia → dónde se estudia

| Bloque | Clases | Contenido | Peso típico en el examen |
|---|---|---|---|
| **A. Fundamentos** | 1–7 | Redes, modelos OSI/TCP-IP, conmutación, retardo, Nyquist/Shannon, capa física | ~2 preguntas teoría |
| **B. Capa de aplicación** | 8–15 | HTTP, DNS, correo, DHCP, sockets, flujo completo de un web request | ~1 pregunta teoría + problemas de programación |
| **C. Capa de Transporte** | 16–23 | UDP, TCP (cabecera, handshake, fiabilidad, control de flujo y de congestión) | **MUY alta** — 1 pregunta teoría + casi siempre 1 de los 2 problemas |
| **D. Capa de Red** | 24–35 | IPv4, subnetting/VLSM, tablas de enrutamiento, ARP/NAT, DV, LS, OSPF, BGP, fragmentación/MTU, IPv6, ICMP | **MUY alta** — 1 pregunta teoría + casi siempre 1 de los 2 problemas |
| **E. Capa de Enlace** | 36–41 | Framing, CRC/Hamming/paridad, ARQ, acceso al medio, switch/hub/VLAN, 802.11 | ~1 pregunta teoría |
| **F. Servicios, multimedia y seguridad** | 42–48 | RTP/VoIP/jitter, QoS, MPLS, SNMP, criptografía, TLS/PGP/IDS, IP móvil, repaso | ~1 pregunta teoría |

---

## Las 48 clases, una por una

### BLOQUE A — Fundamentos de redes (clases 1–7)

| # | Clase | Contenido | Problemas de examen asociados |
|---|---|---|---|
| 1 | **¿Qué es una red de computadores?** | Motivación, LAN/MAN/WAN/PAN, topologías, parámetros (BW, latencia, throughput, RTT, jitter), por qué las redes importan | — |
| 2 | **Los modelos de capas: OSI y TCP/IP** | Las 7 capas OSI con sus PDUs; las 4/5 capas TCP-IP; qué problema resuelve cada capa; comparación de ambas columnas | 2006-12 P1 · 2007-03 P1 |
| 3 | **Encapsulación y comparación OSI ↔ TCP/IP** | PDU, encapsulación/desencapsulación paso a paso, diagrama de un byte traveling, qué se "fusiona" en TCP/IP y por qué importa | 2009-02 P2 · 2009-07 P2 |
| 4 | **Conmutación: circuitos, paquetes y mensajes** | Store-and-forward, comparación de las tres, conmutaciónStore-and-forward, por qué Internet usa paquetes, holgura (*headroom*) | 2007-12 P3 |
| 5 | **El retardo en las redes de paquetes** | Los 4 componentes (procesamiento, encolado, transmisión, propagación); ancho de banda ≠ velocidad de propagación; RTT; jitter; throughput; delay×BW | 2009-12 P1 · 2010-02 P5 |
| 6 | **Taller de retardos (todo resuelto)** | Ej. tipo 2011-03 P5 · 2009-12 P1 · 2009-07, con aritmética explícita | **2011-03 P5** · 2009-12 P1 |
| 7 | **Nyquist, Shannon y la capa física** | Teoremas con hipótesis; capacidad del canal; medios; par trenzado/coax/fibra; full vs half duplex; HDLC | 2006-08 P1 · 2007-07 P1 · 2009-03 P5 |
| — | **Simulacro 1** (integrado en c7) | Examen de teoría tipo: capas + física + retardo | — |

> Nota: la clase 7 cierra con el **Simulacro 1**.

### BLOQUE B — Capa de aplicación (clases 8–15)

| # | Clase | Contenido | Problemas de examen asociados |
|---|---|---|---|
| 8 | **Modelo cliente/servidor y HTTP/1.1** | Petición/respuesta; ```
GET /index.html HTTP/1.1```; Host; Connection; persistente vs no persistente; coste en RTT | **2010-07 P1** (página con 10 imágenes) |
| 9 | **HTTP a fondo: mensajes, cookies, caché, versiones** | Métodos; cabeceras; 304; proxies; CDN; HTTP/2 y HTTP/3 (QUIC); cookies y sesión | 2010-07 P1 |
| 10 | **DNS: la base de datos distribuida** | Jerarquía root/TLD/autoritativo; tipos de servidores; Resource Records y sus 5 campos | 2010-02 P1 · 2010-07 P3 |
| 11 | **DNS: iterativo vs recursivo, caché y TTL** | Los dos algoritmos paso a paso; por qué existe el caché; TTL y por qué lo define el autoritativo; DNSSEC | **2010-12 P1** · 2010-07 P3 |
| 12 | **Taller DNS + HTTP (resuelto)** | Ejercicios de examen con los 4 servidores y todos los mensajes | **2010-12 P1b** |
| 13 | **Correo electrónico** | SMTP (push), POP3 e IMAP (pull); MIME; POP3 y el problema del CRLF.CRLF | 2010-03 P2 · 2008-12 P4 |
| 14 | **Sockets: la API de la capa de transporte** | ```
socket/bind/listen/accept/connect/send/recv```; modelo cliente/servidor; código C real | 2010-03 P2 · 2009-07 P1 |
| 15 | **DHCP, configuración y simulación final** | DORA paso a paso; opciones; bootp; **Simulacro 2**: abrir un navegador paso a paso con todas las tramas | **2011-02 P2** (DHCP) |

### BLOQUE C — Capa de transporte (clases 16–23)

| # | Clase | Contenido | Problemas de examen asociados |
|---|---|---|---|
| 16 | **Multiplexación y UDP** | El problema de varias apps en un host; mux/demux; por qué la conexión TCP es 4-tupla y el socket UDP es 2-tupla; formato UDP; checksum | **2010-12 P2** |
| 17 | **TCP: la cabecera campo por campo** | 20 bytes; ports; seq/ack; offset; flags (FIN/SYN/RST/PSH/ACK/URG); window; checksum; opciones (MSS, SACK, timestamps) | 2011-02 P3 · 2007-03 P4 |
| 18 | **TCP: establecer y cerrar la conexión** | Three-way handshake con números concretos; FIN en ambos sentidos; la máquina de estados completa; SYN flood | 2006-12 P4 · 2009-07 P2 |
| 19 | **TCP: cómo se garantiza la fiabilidad** | Por qué seq y ack; RTO; timers; ventana deslizante; fast retransmit; SACK; por qué el PUSH no garantiza entrega | **2011-03 P4** · 2001-12 |
| 20 | **Control de flujo vs control de congestión** | rwnd vs cwnd; la analogía del Grifo; por qué son dos cosas distintas; elReceiver que no lee | 2009-07 P1 · 2009-12 P5 · 2010-02 P5 |
| 21 | **TCP: control de congestión (slow start, AIMD, ECN)** | Los 4 algoritmos; ventana de congestión y umbral; 3 ACKs duplicados; fast retransmit/recovery; ECN | **2011-03 Problema 1 (el de ECN, 30 pts)** |
| 22 | **Taller TCP: diagramas resueltos** | Ej. 2011-03 P4 con y sin pérdida; agotamiento del buffer; RTT y RTO | **2011-03 P4** |
| 23 | **Repaso transporte + Simulacro 3** | Todos los diagramas TCP clássicos + caso de examen | **2011-03 P4** |

### BLOQUE D — Capa de red (clases 24–35)

| # | Clase | Contenido | Problemas de examen asociados |
|---|---|---|---|
| 24 | **Capa de red: las dos funciones** | Forwarding vs routing; plano de datos vs plano de control; longest prefix match | **2011-03 P1** · 2009-02 P2 · 2010-02 P2 |
| 25 | **Conmutación en la red** | Datagramas vs circuitos virtuales; en banda vs fuera de banda; tabla por flujo vs por prefijo | 2009-02 P4 |
| 26 | **IPv4: el datagrama y las direcciones** | Formato de cabecera; claseful A–E; máscaras; ID de red vs ID de host; direcciones especiales | 2008-12 P2 |
| 27 | **Subnetting paso a paso** | El método de 7 pasos; calcular máscara por hosts; tamaño de subred; broadcast; el caso del "número mágico"; ejemplos worked | **2011-03 Problema 2d** |
| 28 | **VLSM y planes de numeración** | Subredes de tamaño variable;why maximize addresses for future; plan de una empresa con sucursales | **2011-03 P2d** · 2010-12 P2 · 2010-07 P2 |
| 29 | **Taller de subnetting y planes de numeración** | Ejercicios de examen resueltos con la aritmética a la vista | **2011-03 P2d** · 2006-08 P4 · 2008-12 P2 |
| 30 | **Tablas de enrutamiento, next hop y ARP** | Formato de la tabla; longest prefix match con ejemplo; tabla ARP; RARP; gratuitous ARP | **2011-03 Problema 2a,2b** · 2010-03 P1 · 2009-12 P1 |
| 31 | **NAT, PAT y sus tricks** | Traducción de IP y puerto; tabla NAT; por qué rompe el modelo de capas; cómo un servidor público alcanza a uno privado; port forwarding | **2011-02 P4** · **2011-03 Problema 2c** · 2010-03 P1 |
| 32 | **Enrutamiento distance-vector** | Bellman-Ford paso a paso; conteo a infinito; split horizon; poison reverse; hold-down; RIP | **2006-08 P3** · 2008-12 P2 · 2010-02 P2 |
| 33 | **Enrutamiento link-state y OSPF** | Dijkstra con tabla paso a paso; flooding; LSA; los 5 mensajes de OSPF; áreas; por qué hops no es buena métrica | **2009-02 Problema 2a** · 2007-03 P1 · 2010-12 P2 |
| 34 | **BGP y el routing entre operadores** | Sistemas autónomos; path-vector; el "tricky business" del último salto; por qué BGP no puede contar a infinito; RPKI | **2007-03 P2** |
| 35 | **Fragmentación, MTU y path MTU** | MTU; IPv4 fragmenta o tira; DF e ICMP tipo 3 có 4; reensamblaje; path MTU; PMTUD | **2010-12 Problema 2 (30 pts)** |
| 36 | **IPv6** | Cabecera de 40 bytes; 3 tipos de dirección; ICMPv6; Neighbor Discovery vs ARP; DAD; SLAAC; transición | **2010-12 P5** · 2009-12 P5 · 2007-03 P3 |
| 37 | **ICMP, ping y traceroute** | Tipos y códigos de ICMP que hay que saber; TTL; por qué funciona traceroute; los dos sabores | **2011-03 P3** |
| — | **Repaso red + Simulacro 4** (c37) | — | — |

### BLOQUE E — Capa de enlace (clases 38–43)

| # | Clase | Contenido | Problemas de examen asociados |
|---|---|---|---|
| 38 | **Capa de enlace: servicios y framing** | Por qué delimitar tramas; framing por conteo, por bytes con byte-stuffing, por bits con bit-stuffing; HDLC; PPP | 2006-12 P2 · 2010-03 P3 |
| 39 | **Detección de errores** | Paridad; paridad 2D; checksum de Internet; **CRC con la aritmética paso a paso** | 2000-02 P2 · 2007-12 P2 · 2010-02 P3 |
| 40 | **Corrección de errores y ARQ** | Hamming (distancia de Hamming, SEC, SECDED); Stop-and-Wait; Go-Back-N; Selective Repeat | 2010-02 P3 · 2009-03 P1 |
| 41 | **Acceso al medio** | ALOHA y Slotted-ALOHA (con el gráfico de rendimiento); CSMA; CSMA/CD; Ethernet; dominios de colisión y broadcast | **2010-12 P3** · 2007-07 P3 |
| 42 | **Switch, hub, VLAN, STP** | Self-learning paso a paso; tabla MAC; ageing; bridge vs switch; 802.1Q; spanning tree | **2010-12 P3** · 2008-12 P2 |
| 43 | **Redes inalámbricas 802.11** | CSMA/CA; estación oculta y RTS/CTS; NAV; EDCA; WPA2 vs WPA3; Wi-Fi 6/7 | **2010-07 P2** · 2007-03 P5 · 2006-12 P5 |

### BLOQUE F — Servicios, multimedia y seguridad (clases 44–48)

| # | Clase | Contenido | Problemas de examen asociados |
|---|---|---|---|
| 44 | **Multimedia: streaming, RTP y VoIP** | RTP/RTCP; jitter buffer; el caso del stream que se corta; MPEG-2 I/P/B; por qué TCP no sirve para tiempo real | **2011-02 Problema 1 (30 pts)** · 2008-12 P5 |
| 45 | **QoS: shaping, policing, DiffServ, MPLS** | Leaky bucket vs token bucket; IntServ vs DiffServ; edge vs core; MPLS etiqueta/LSP/roles | **2007-12 P1** · 2007-12 P2 · 2009-03 P4 |
| 46 | **Gestión de redes: SNMP** | Agente vs gestor; MIB; polling vs traps; SNMPv3; NETCONF | 2010-03 P4 · 2011-02 P4 |
| 47 | **Seguridad: servicios y criptografía** | Confidencialidad / integridad / no repudio; hash; RSA; firma digital; PKI; qué cambió desde 2012 | **2011-02 P1** · 2010-02 P4 · 2010-07 P1 |
| 48 | **Seguridad aplicada + IP móvil + Simulacro final** | TLS/SSL; PGP; tunneling/VPN; IDS/IPS; DPI; ataques típicos; IP Móvil (MN/HA/FA/CN); **simulacro final completo** | **2011-02 Problema 2 (30 pts)** · 2009-07 Problema 1 |

---

## Frecuencia de los temas en los 50 exámenes oficiales (1998–2011)

Conté cada aparición en los exámenes Letra (`eirc*`) y Solución (`sirc*`):

| Tema | Apariciones | Clases donde se estudia |
|---|---|---|
| Retardos / BW / RTT | 9 | 5, 6 |
| Subnetting / planes de numeración / VLSM | 11 | 26–29 |
| Tablas de enrutamiento / next hop | 8 | 30 |
| TCP (cabecera, handshake, control) | 14 | 17–22 |
| ARP / NAT / Ethernet + IP + MAC | 10 | 30, 31, 42 |
| Enrutamiento DV / LS / OSPF / BGP / Dijkstra | 10 | 32–34 |
| HTTP / Web | 6 | 8, 9 |
| DNS | 6 | 10–12 |
| Acceso al medio (ALOHA/CSMA) / switch / hub | 9 | 41–43 |
| Detección/corrección de errores (CRC, paridad, Hamming) | 7 | 39, 40 |
| Programación (pseudocode, sockets) | 12 | 21, 22, 44 |
| Seguridad (cripto, TLS, PGP, IDS) | 9 | 47, 48 |
| IPv6 | 5 | 36 |
| Fragmentación / MTU / ICMP | 5 | 35, 37 |
| Multimedia / RTP / QoS / jitter | 6 | 44, 45 |
| Modelo de capas | 5 | 2, 3 |
| Nyquist / Shannon / duplex | 4 | 7 |
| Correo (SMTP/POP3/IMAP) | 4 | 13 |
| Gestión de redes (SNMP) | 3 | 46 |
| IP Móvil | 3 | 48 |
| Conmutación (circuitos/paquetes/mensajes) | 3 | 4 |

---

## Estructura de cada archivo de clase

```
clase-NN-<slug>.md
├── Encabezado (número, título, bloque, semana, duración)
├── 🎯 Objetivos  (qué debés saber hacer al terminar)
├── 📖 Teoría
│   ├── conceptos con DIAGRAMA ASCII
│   ├── por qué importa (conectar con el examen)
│   └── ⚠️ Actualización a 2026  (qué sigue igual / qué cambió / con qué RFC)
├── 🧮 Práctica guiada  (ejemplos resueltos, con el RAZONAMIENTO explícito)
├── 📝 Problemas de examen de FING  (enunciado literal + resolución paso a paso)
├── ✅ Resumen / autoevaluación (10 preguntas de repaso con respuestas)
└── 🔗 Referencias (examen, Tanenbaum cap. X, RFC, clase siguiente)
```

Los archivos de clase se escriben en español rioplatense (voseo), que es como
habla el curso, con los términos técnicos en inglés cuando así se usan en la cátedra.

---

## Cronograma semanal sugerido

| Semana | Clases | Tema |
|---|---|---|
| 1 | 1, 2, 3 | Qué es una red · Modelos OSI y TCP/IP · Encapsulación |
| 2 | 4, 5, 6 | Conmutación · Retardos · **Taller de retardos** |
| 3 | 7, 8, 9 | Nyquist/Shannon + **Simulacro 1** · HTTP · HTTP a fondo |
| 4 | 10, 11, 12 | DNS · DNS resolución · **Taller DNS/HTTP** |
| 5 | 13, 14, 15 | Correo · Sockets · DHCP + **Simulacro 2** |
| 6 | 16, 17, 18 | UDP/mux · Cabecera TCP · Handshake y cierre |
| 7 | 19, 20, 21 | Fiabilidad TCP · Control de flujo/congestión · **Congestión + ECN** |
| 8 | 22, 23, 24 | **Taller TCP** · **Simulacro 3** · Capa de red: forwarding/routing |
| 9 | 25, 26, 27 | Datagramas vs VC · IPv4 · **Subnetting** |
| 10 | 28, 29, 30 | VLSM · **Taller subnetting** · Tablas de enrutamiento + ARP |
| 11 | 31, 32, 33 | NAT · Distance-vector · Link-state/OSPF |
| 12 | 34, 35, 36 | BGP · Fragmentación/MTU · IPv6 |
| 13 | 37, 38, 39 | ICMP/ping/traceroute + **Simulacro 4** · Framing · CRC/paridad/checksum |
| 14 | 40, 41, 42 | ARQ/Hamming · Acceso al medio · Switch/VLAN/STP |
| 15 | 43, 44, 45 | 802.11 · Multimedia/RTP/VoIP · QoS/MPLS |
| 16 | 46, 47, 48 | SNMP · Criptografía · **Seguridad + IP móvil + Simulacro final** |

---

## Orden de trabajo

1. ✅ Descargar los 50 exámenes oficiales (1998–2011) con soluciones
2. ✅ Descargar los 8 prácticos oficiales (2008)
3. ✅ Extraer texto de todo
4. ✅ Levantar el plan de 48 clases
5. Investigar actualizaciones 2012→2026 (RFCs, estado de protocolos)
6. Escribir las 48 clases
7. Escribir el banco de ejercicios extra tipo examen
8. Simulacros completos cronometrados a 3 horas
