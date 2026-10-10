# Banco de exámenes oficiales — índice por tema

Todos los archivos están en `material-oficial/examenes/`.
- `eircYYMM.pdf` = **Letra** (el examen tal cual, sin soluciones)
- `sircYYMM.pdf` = **Solución** (el examen con las respuestas de la cátedra)
- `scdtYYMM.pdf` = Communication Data Theory (material permitido, 1998-2002)

**Los .txt en `material-oficial/examenes/txt/` son el texto extraído** — usá esos,
son más fáciles de leer que los PDF.

## Cómo están armados los exámenes

- **3 horas**, individual, **sin material**.
- Aprobación con **60/100 puntos**.
- **Obligatorio acertar al menos 15 puntos en las preguntas teóricas** (si no, no
  apruebas aunque sumes 60 con los problemas). Ojo con esto.
- Estructura típica desde 2008:
  - **5 Preguntas Teóricas** — 5 a 10 pts cada una, ~40 pts total.
  - **2 Problemas Prácticos** — 30 pts cada uno, 60 pts total.

### Los dos problemas prácticos siempre son de este tipo

**Tipo A — Programación / pseudocode de un protocolo.**
Te dan un contexto ("ECN notifica congestión…", "se desea un sistema que…), te dan
primitivas y tipos de datos ya definidos, y te piden implementar funciones.
No hay compilador: se escribe en pseudocode estilo C. Lo que se corrige es que
detectes los casos, inicialices el estado y tomes las decisiones correctas.

Ejemplos: ECN + control de congestión (2011-03 P1), protocolo de página web
anti-spam vía HTTP (2009-07 P2), balanceo de carga con variante de NAT (2008-12 P1),
Path MTU con ICMP (2010-12 P2), VoIP con buffer de jitter (2011-02 P1), sockets
UDP para elegir AP más barato (2010-12 P1).

**Tipo B — Topología de red con números.**
Te dan una figura con routers, subredes, direcciones IP y MAC. Y te piden:
tablas de enrutamiento, ARP paso a paso, qué cambia con NAT, subdivision de un
bloque de direcciones, campos de cabecera, diagramas de tramas.

Ejemplos: NAT + ARP + subredes (2011-03 P2), subnetting + distance-vector +
tunneling (2010-07 P2), topología con 6 routers y 3 LANs (2006-08 P1), IP móvil
(2011-02 P2), fragmentación y reensamblaje (2006-12 P1).

---

## Índice por tema

### Retardos, ancho de banda, RTT, jitter
| Examen | Qué | Dónde |
|---|---|---|
| **2011-03** (`sirc1103`) | P5: retardo end-to-end con 3 enlaces y 2 conmutadores; y el caso "store-and-forward" optimizado | `txt/sirc1103.txt` líneas 148–199 |
| 2009-12 (`sirc0912`) | P1: componentes del retardo, ancho de banda vs velocidad de propagación, congestión | `txt/sirc0912.txt` ~l.117 |
| 2010-07 (`sirc1007`) | P1: secuencia de pasos de cargar una página con HTTP no persistente | `txt/sirc1007.txt` ~l.23 |
| 2010-02 (`sirc1002`) | P5: jitter vs retardo | `txt/sirc1002.txt` ~l.82 |
| 2009-03 (`sirc0903`) | P5: full duplex vs half duplex | |

### Modelos de capas
| Examen | Qué |
|---|---|
| 2006-12 (`sirc0612`) | P1: modelo OSI y las hipótesis de las 7 capas |
| 2007-03 (`sirc0703`) | P1: modelo TCP/IP |
| 2009-02 (`sirc0902`) | P2: forwarding vs routing + flooding |
| 2011-03 (`sirc1103`) | P1: las dos funciones clave de la capa de red |

### Conmutación (circuitos / paquetes / mensajes)
| Examen | Qué |
|---|---|
| 2007-12 (`sirc0712`) | P3: comparación de los tres + características |
| 2009-02 (`sirc0902`) | P4: conmutación por datagramas vs circuitos virtuales |
| 2009-07 (`sirc0907`) | P2: distancia entre "hops" como métrica, ¿es la mejor? |

### Nyquist, Shannon, capa física
| Examen | Qué |
|---|---|
| 2006-08 (`sirc0608`) | P1: resultados de Nyquist y Shannon con sus hipótesis |
| 2007-07 (`sirc0707`) | P1: capacidad máxima sobre línea telefónica (Shannon), con fórmula y unidades |
| 2009-02 (`sirc0902`) | P3: FDMA y TDMA, principio de operación |
| 2009-03 (`sirc0903`) | P5: full duplex vs half duplex y qué tecnología usa cada una |

### Subnetting / planes de numeración
| Examen | Qué |
|---|---|
| **2011-03** (`sirc1103`) | P2d: dividir 100.100.100.0/24 para 70 puestos + 15 servidores maximizando direcciones futuras |
| 2010-12 (`sirc1007`) | P2a: 220.10.10.28/30 con LANs de hasta 120 hosts; y /21 para 123 dir por LAN |
| 2010-07 (`sirc1007`) | P2: subredes LAN2 y LAN3 con 250 hosts desde 192.168.2.0/23 |
| 2008-12 (`sirc0812`) | P2: plan de numeración + NAT + tunneling |
| 2006-08 (`sirc0608`) | P4: 200.40.224.0/25 subdividido en redes de 18, 11 y 9 hosts |
| 2010-03 (`sirc1003`) | P1: tres subredes /24 interconectadas con R1 y R2 |

### Tablas de enrutamiento, next hop, ARP
| Examen | Qué |
|---|---|
| **2011-03** (`sirc1103`) | P2a-b: tabla de R1 y del host H + secuencia ARP completa |
| 2010-03 (`sirc1003`) | P1: ARP entre dos hosts, con todas las MAC e IP |
| 2009-12 (`sirc0912`) | P1: tablas de R1 y R2 con conectividad extremo a extremo |
| 2010-02 (`sirc1002`) | P2: funciones clave de la capa de red |
| 2008-07 (`sirc0807`) | P1: tabla de R1 con distancia en hops |
| 2007-12 (`sirc0712`) | P2a: ARP en red con dos hosts, LAN y router |

### NAT
| Examen | Qué |
|---|---|
| **2011-02** (`sirc1102`) | P4: NAT, por qué rompe el aislamiento de capas, las 3 soluciones para alcanzar un servidor privado |
| **2011-03** (`sirc1103`) | P2c: qué campos cambia R1 en cada sentido + tabla NAT |
| 2010-03 (`sirc1003`) | P1: subredes privadas + ARP + NAT overview |
| 2008-12 (`sirc0812`) | P1: variante de NAT para balanceo de carga entre 3 servidores |

### Enrutamiento: distance-vector
| Examen | Qué |
|---|---|
| 2006-08 (`sirc0608`) | P3: funcionamiento del algoritmo distance-vector, ventajas y desventajas |
| 2008-12 (`sirc0812`) | P2: red de 4 nodos, distance-vector, tabla paso a paso |
| 2010-02 (`sirc1002`) | P2: la misma topología de 4 nodos con la misma tabla |
| 2010-07 (`sirc1007`) | P2b: distance-vector con distancia en hops |
| 2010-12 (`sirc1103`) | P3: OSPF/BGP y ejemplo de conteo a infinito |

### Enrutamiento: link-state, Dijkstra, OSPF
| Examen | Qué |
|---|---|
| 2009-02 (`sirc0902`) | Problema 2a: ejecutar Dijkstra paso a paso desde el nodo u |
| 2007-03 (`sirc0703`) | P1: los 5 mensajes de OSPF |
| 2007-03 (`sirc0703`) | Problema 2: analizar link-state en topología con enlaces paralelos |
| 2009-12 (`sirc0912`) | P3: ¿"hops" es buena métrica? |

### Enrutamiento: BGP
| Examen | Qué |
|---|---|
| 2007-03 (`sirc0703`) | P2: un bridge con política LAN origen == destino; enrutamiento jerárquico, IGP con jerarquías |

### IPv4, fragmentación, MTU
| Examen | Qué |
|---|---|
| **2010-12** (`sirc1012`) | Problema 2 (30 pts): MTU, fragmentación, Path MTU + **implementar el algoritmo de descubrimiento** |
| 2006-12 (`sirc0612`) | P3: por qué fragmentar en capa 3, cómo funciona en IPv4, problemas, y **algoritmo de reensamblaje** |
| 2011-03 (`sirc1103`) | P3: traceroute (usa TTL + ICMP tipo 11) |

### IPv6
| Examen | Qué |
|---|---|
| **2010-12** (`sirc1012`) | P5: stacks de referencia IPv4 vs IPv6, coexistencia, ND vs ARP con ≥4 cambios |
| 2009-12 (`sirc0912`) | P5: 2 protocolos de ICMPv6 con NS/NA (DAD, NDP) y comparación con IPv4 |
| 2010-07 (`sirc1007`) | P5: los 3 modelos de comunicación y los 3 tipos de dirección + los 3 esquemas de transición |
| 2007-03 (`sirc0703`) | P3: RARP, para qué escenario |

### ICMP, ping, traceroute
| Examen | Qué |
|---|---|
| **2011-03** (`sirc1103`) | P3: principio de funcionamiento del comando traceroute, tipos de mensaje, nodos que colaboran |
| 2010-12 (`sirc1012`) | P2: tabla de tipos y códigos de ICMP tipo 3 (muy útil de memorizar) |
| 2006-08 (`sirc0608`) | P2: por qué ARP y cómo funciona |

### TCP
| Examen | Qué |
|---|---|
| **2011-03** (`sirc1103`) | P4: 4 segmentos de 20 bytes desde seq 1100, con y sin pérdida del primero — **el diagrama clásico** |
| **2011-03** (`sirc1103`) | Problema 1 (30 pts): ECN + detección y control de congestión **en pseudocode** |
| 2011-02 (`sirc1102`) | P3: campos más importantes de segmentos TCP y UDP |
| 2006-12 (`sirc0612`) | P4: three-way handshake y cierre, TPDU |
| 2009-07 (`sirc0907`) | P2: three-way handshake + cuándo usar UDP en vez de TCP |
| 2009-03 (`sirc0903`) | P1: Go-Back-N |
| 2010-02 (`sirc1002`) | P5: control de flujo de TCP |
| 2009-12 (`sirc0912`) | P2: servicio confiable en transporte vs enlace |
| 2009-07 (`sirc0907`) | P1: control de flujo vs control de congestión, cómo detecta TCP la congestión |
| 2008-07 (`sirc0807`) | P2: los 4 algoritmos de control de congestión de TCP |
| 2001-12 (`sirc0112`) | Problema 1: dos conexiones TCP por un solo router que pierde paquetes |
| 2001-12 (`sirc0112`) | Problema 2: por qué PUSH no garantiza un mensaje por vez en el destino |
| 2010-03 (`sirc1003`) | P5: TCP en redes inalámbricas, el problema principal |
| 2010-03 (`sirc1003`) | Problema 2: ataque TCP reset — rango de puertos y probabilidad |

### UDP y sockets
| Examen | Qué |
|---|---|
| **2010-12** (`sirc1012`) | P2: mux/demux de sockets UDP (3 preguntas concretas) vs TCP |
| **2010-12** (`sirc1012`) | Problema 1 (30 pts): `connectCheaper()` — protocolo, máquinas de estado e **implementación con sockets UDP en C** |
| 2001-02 (`sirc0102`) | P2: puente que traduce UDP↔TCP |
| 2001-02 (`sirc0102`) | P3: dispositivo de N puertos con buffers, learning de direcciones |

### HTTP / aplicación web
| Examen | Qué |
|---|---|
| 2010-07 (`sirc1007`) | P1: página HTML con texto y 10 imágenes, HTTP no persistente — **todos los pasos** |
| 2009-07 (`sirc0907`) | Problema 2: cliente de correo anti-spam vía HTTP — **programación** |
| 2008-12 (`sirc0812`) | P4: POP3 y el mecanismo CRLF.CRLF |

### DNS
| Examen | Qué |
|---|---|
| **2010-12** (`sirc1012`) | P1: TTL del RR, quién lo define, unidades; y los pasos de una consulta A |
| 2010-07 (`sirc1007`) | P3: resolución iterativa completa sin caché en ningún servidor |
| 2010-02 (`sirc1002`) | P1: qué es DNS y su función |
| 2007-07 (`sirc0707`) | P4: función del DNS y protocoloinvolucrado |
| 2009-07 (`sirc0907`) | P2a: implementar la consulta DNS por UDP |

### Correo electrónico
| Examen | Qué |
|---|---|
| 2010-03 (`sirc1003`) | P2: arquitectura del correo, roles y protocolos |
| 2008-12 (`sirc0812`) | P4: POP3, control vs datos, CRLF.CRLF |
| 2006-12 (`sirc0612`) | — (ver `sirc0112` P2 para el problema de PUSH) |

### Capa de enlace: framing y errores
| Examen | Qué |
|---|---|
| 2006-12 (`sirc0612`) | P2: por qué framing, técnica en canal orientado a bit y orientado a byte |
| 2010-02 (`sirc1002`) | P3: paridad en dos dimensiones, detección de errores |
| 2007-12 (`sirc0712`) | P2: leaky bucket y token bucket |
| 2007-03 (`sirc0703`) | Problema 1: protocolo de capa 2 en enlace punto a punto, formato de trama |
| 2007-12 (`sirc0712`) | P4: fragmentación transparente vs no transparente |

### Acceso al medio
| Examen | Qué |
|---|---|
| **2010-12** (`sirc1012`) | P3: hub vs switch, dominio de colisión y broadcast, self-learning |
| 2007-07 (`sirc0707`) | P3: ALOHA vs Slotted-ALOHA (rendimiento), tipos de CSMA y diferencias |
| 2010-07 (`sirc1007`) | P2: ¿CSMA/CD en wireless? ¿CSMA/CD en Ethernet switcheada? |
| 2007-03 (`sirc0703`) | P5: CSMA/CA |
| 2008-12 (`sirc0812`) | P2: hub vs switch, performance y seguridad |

### Redes inalámbricas
| Examen | Qué |
|---|---|
| 2008-07 (`sirc0807`) | P3: CSMA/CA en modo infraestructura |
| 2006-12 (`sirc0612`) | P5: estación oculta |
| 2010-03 (`sirc1003`) | P5: TCP sobre redes inalámbricas y móviles |

### VLAN, STP, bridge
| Examen | Qué |
|---|---|
| 2009-03 (`sirc0903`) | P3: VLAN 802.1Q y utilidad |
| 2003-12 (`sirc0312`) | Problema: switch y reenvío |
| 2007-03 (`sirc0703`) | P2: bridge con política por LAN origen/destino |
| 2000-07 (`sirc0007`) | Problema 1: programa que recibe todas las tramas de una LAN |

### SNMP / gestión
| Examen | Qué |
|---|---|
| 2010-03 (`sirc1003`) | P4: conceptos agente y gestor |
| 2011-02 (`sirc1102`) | P2: DHCP, intercambio de mensajes |
| 2007-12 (`sirc0712`) | P5: router de ingreso y egreso en MPLS |

### Multimedia
| Examen | Qué |
|---|---|
| **2011-02** (`sirc1102`) | Problema 1 (30 pts): VoIP — tamaño del datagrama, mínimo `p`, promedio ponderado, **implementación** |
| 2008-12 (`sirc0812`) | P5: ¿Ip/TCP para tiempo real? Bajo qué hipótesis sí |
| 2008-07 (`sirc0807`) | Problema 1: audio redundante desde 3 fuentes con RTP, **implementación** |
| 2010-07 (`sirc1007`) | Problema 1: MPEG-2 I/P/B frames |

### QoS / MPLS / shaping
| Examen | Qué |
|---|---|
| 2007-12 (`sirc0712`) | P1: leaky bucket vs token bucket |
| 2007-12 (`sirc0712`) | P2: conmutación de circuitos/paquetes/mensajes |
| 2007-12 (`sirc0712`) | P5: MPLS, router de ingreso y egreso |
| 2009-03 (`sirc0903`) | P4: DiffServ, edge vs core, campo de IPv4 para marcar |
| 2010-07 (`sirc1007`) | P4: arquitectura DiffServ, funciones de edge y core |
| 2006-08 (`sirc0608`) | P5: conceptos de MPLS: etiqueta, LSP, roles |

### Seguridad
| Examen | Qué |
|---|---|
| **2011-02** (`sirc1102`) | P1: confidencialidad, integridad, no repudio + diagrama con clave pública |
| 2011-02 (`sirc1102`) | P2: DHCP |
| 2009-07 (`sirc0907`) | P5: confidencialidad vs integridad |
| 2009-02 (`sirc0902`) | P1: SSL/TLS, qué clave tiene el certificado |
| 2010-02 (`sirc1002`) | P4: firma digital en correo |
| 2009-07 (`sirc0907`) | P4: RPF en multicast |
| 2009-12 (`sirc0912`) | P4: funciones de hash, propiedades de seguridad, ejemplo |
| 2008-07 (`sirc0807`) | P1: IDS, los dos grandes tipos |
| 2008-07 (`sirc0807`) | P5: 3 ventajas y 2 desventajas de IPv6 |
| 2006-12 (`sirc0612`) | Problema 2: hacker que secuestra www.intrusos.com.ar |
| 2009-02 (`sirc0902`) | Problema 1: adaptador para encriptar servicios legados |

### IP móvil
| Examen | Qué |
|---|---|
| **2011-02** (`sirc1102`) | Problema 2 (30 pts): IP Móvil — campos MAC/IP por segmento, routing triangular, tunneling escalable |
| 2008-12 (`sirc0812`) | P3: arquitectura de IP Móvil, componentes y roles |
| 2007-07 (`sirc0707`) | P5: arquitectura y funcionamiento de IP Móvil |

### Convexidades raras
| Examen | Qué |
|---|---|
| 2008-07 (`sirc0807`) | P4: plano de datos vs plano de control, control en banda vs fuera de banda |
| 2000-08 (`sirc0008`) | Problema 1: routing por aprendizaje reverso con.tables |
| 2000-07 (`sirc0007`) | Problema 2: protocolo fiable sobre 3 subredes con MTU distinta |
| 2001-02 (`sirc0102`) | Problema 1: dos tarjetas de red en el mismo host |

---

## Los 3 simulacros que hay que saber hacer completos

### Simulacro A — el examen de 2011-03 (el más representativo)
- T1 (8): forwarding vs routing y cómo interactúan
- T2 (6): congestión, pérdidas, retardo
- T3 (6): traceroute
- T4 (10): TCP 4 segmentos con y sin pérdida
- T5 (10): retardo end-to-end, y con store-and-forward optimizado
- P1 (30): ECN → `TCP_congDetection` + `TCP_congControl`
- P2 (30): NAT + ARP + subredes desde /24

### Simulacro B — el examen de 2010-12
- T1 (8): DNS, TTL y resolución
- T2 (8): mux/demux UDP vs TCP
- T3 (8): hub vs switch, dominios, self-learning
- T4 (8): seq y timers en TCP
- T5 (8): IPv6 vs IPv4, ND vs ARP
- P1 (30): `connectCheaper()` — protocolo + máquinas de estado + sockets UDP en C
- P2 (30): MTU, fragmentación, path MTU + implementación del algoritmo

### Simulacro C — el examen de 2011-02
- T1 (10): confidencialidad / integridad / no repudio + diagrama
- T2 (10): DHCP
- T3 (10): campos de TCP y UDP
- T4 (10): NAT + capas + soluciones para llegar a un privado
- P1 (30): VoIP, jitter, promedio ponderado, implementación
- P2 (30): IP Móvil completo
