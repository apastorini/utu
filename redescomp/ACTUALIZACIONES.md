# ACTUALIZACIONES.md — Qué cambió entre 2012 y 2026

> **Este documento es la fuente de verdad de la columna «⚠️ Actualización a 2026» de
> todas las clases.** Cuando escribas una clase, citá de acá. No inventes números
> de RFC: si un número no está en este documento, no lo pongas o poné
> "verificar".
>
> Todos los RFC fueron verificados contra `rfc-editor.org` y
> `datatracker.ietf.org` (octubre 2026). Las cifras de despliegue llevan su
> fuente, porque cambian mes a mes: **en clase, mejor que el alumno las mida
> vivo** en `radar.cloudflare.com`, `stats.google.com/ipv6/`, `w3techs.com`,
> `apnic.labs` que memorizar un número que envejecerá.

---

## 0. Los 14 números que hay que corregir sí o sí

Si tu clase cita alguno de estos, está desactualizada:

| En un curso de 2012 se decía | La referencia actual |
|---|---|
| RFC 2616 (HTTP) | **RFC 9110** (semántica, *Internet Standard*) + **RFC 9112** (sintaxis HTTP/1.1) |
| RFC 793 (TCP) | **RFC 9293** (2022, *Internet Standard*; consolida 793 + 5 updates) |
| RFC 8446 (TLS 1.3) | **RFC 9846** (jul-2026, *Proposed Standard*; absorbe también TLS 1.2) |
| RFC 2460 (IPv6) | **RFC 8200** (2017, *Internet Standard*) |
| RFC 1981 (PMTUD IPv6) | **RFC 8201** (2017) |
| RFC 7752 (BGP-LS) | **RFC 9552** (dic-2023) |
| RFC 6145 (SIIT) | **RFC 7915** (2016) — obsoleta a 6145 |
| RFC 8312 (CUBIC) | **RFC 9438** (ago-2023, *Standards Track*) |
| RFC 4880 (OpenPGP) | **RFC 9580** (jul-2024) |
| RFC 4821 (PLPMTUD) | **RFC 8899** (sep-2020, DPLPMTUD) |
| RFC 3177 (/48 por sitio) | **RFC 6177** (2011) — ya no recomienda /48 por sitio final |
| RFC 6844 (CAA) | **RFC 8659** (2019) |
| RFC 7626 (privacidad DNS) | **RFC 9076** (2021) |
| RFC 3662 (PDB de DiffServ) | **RFC 8622** (2019, LE PHB) |

### Y tres errores frecuentes que **no** son obsoletos sino directamente falsos

| Error frecuente | Realidad |
|---|---|
| "`RFC 8951` = ECN en multihop" | **FALSO.** `RFC 8951` es una aclaración de **EST** (Enrollment over Secure Transport). |
| "`RFC 7560` = ECN++" | **FALSO.** `RFC 7560` (2010, *Informational*) es solo el **documento de problema** de ECN más preciso. La especificación real quedó en **`RFC 9768` (AccECN)**, que actualiza la 3168. |
| "`RFC 8984` depreca el half-duplex Ethernet" | **FALSO.** `RFC 8984` es **JSCalendar**. La deprecación del half-duplex es una decisión de **IEEE 802.3**, y ni siquiera es total. |

---

## 1. HTTP: de HTTP/1.1 a HTTP/3

### Lo que sigue igual — de memoria

- Modelo **petición/respuesta**, protocolo **sin estado** (*stateless*), flujo
  de intermediaries (proxy / gateway / tunnel).
- **Métodos**: GET, HEAD, POST, OPTIONS, PUT, DELETE, TRACE, CONNECT (+ PATCH).
  GET/HEAD/OPTIONS/TRACE son **seguros**; GET/HEAD son **idempotentes**.
- **Códigos de estado** y su clase: 1xx, 2xx, 3xx, 4xx, 5xx. Los del día a día:
  200, 201, 204, 206, 301, 302, 304, 307, 308, 400, 401, 403, 404, 405, 408,
  429, 500, 502, 503, 504.
- **Cabeceras**: `Host` (obligatoria en 1.1), `User-Agent`, `Content-Type`,
  `Content-Length`, `Content-Encoding`, `Accept*`, `Cookie` (RFC 6265),
  `Cache-Control` / `ETag` / `Last-Modified` / `Vary` / `Age`, `Authorization`,
  `Connection`, `Transfer-Encoding: chunked`.
- **PERSISTENTE por defecto** en HTTP/1.1; `Connection: close` es la excepción.
- **Range requests** y **304 Not Modified**.

### Lo que cambió

- **HTTP/1.1 sigue siendo totalmente válido y necesario.** El curso de 2012
  enseñaba RFC 2616 (1999); la especificación vigente es de **2022**.
- **HTTP/2 (`RFC 9113`, 2022)**: multiplexa muchos streams sobre **una sola**
  conexión TCP, eliminando el HOL blocking **a nivel de conexión** (pero no entre
  streams: la pérdida de un stream frena a ese stream).
  - Compresión de cabeceras: **HPACK = `RFC 7541`**, que **sigue vigente** (a
    diferencia de RFC 7540, sí obsoleto).
  - La **prioridad de streams de RFC 7540 quedó deprecada** por RFC 9113 §5.3.
    El frame `PRIORITY` sobrevive por compatibilidad pero está *deprecated*.
    El reemplazo es **`RFC 9218`** (*Extensible Prioritization Scheme*).
- **HTTP/3 (`RFC 9114`, 2022)** + **QUIC**:
  - `RFC 9000` (QUIC, transporte) · `RFC 9001` (TLS sobre QUIC) ·
    `RFC 9002` (recuperación de pérdida y control de congestión) — todos
    mayo-2021, *Proposed Standard*.
  - `RFC 9204` (**QPACK**): compresión de cabeceras, **independiente del orden**
    (a diferencia de HPACK).
  - `RFC 9369` (**QUIC v2**, 2023): no agrega capacidades; existe para
    combatir la **osificación** (middleboxes con IDs de versión fijos).
  - **Corrección conceptual importante frente a 2012: HTTP/3 no solo "usa
    UDP" — reemplaza a TCP por completo.** No hay handshake de 3 vías, no hay
    conexión TCP, no hay retransmisión de conexión; la pérdida se resuelve **por
    stream**.
  - **La negociación es por `Alt-Svc` (`RFC 7838`, 2016)**, no con `Upgrade:`.
    Complementado con los registros DNS **`SVCB`/`HTTPS` (`RFC 9460`, 2023)**, que
    permiten **elegir versión de HTTP antes de conectar**.
- **Cifra real hoy (Cloudflare Radar, Year in Review 2025)**: HTTP/2 **50 %**,
  HTTP/1.x **29 %**, HTTP/3 **21 %**. **HTTP/3 no se adueñó de la web.**
  W3Techs (oct-2026): ~**40,8 % de los sitios** soportan HTTP/3.
  ⚠️ **Trampa metodológica**: si filtrás bots de los datos de Radar, HTTP/3
  aparece cerca de 30 % (los bots hablan HTTP/1.x casi siempre). **Siempre
  declará si incluís bots.**
- Navegadores con HTTP/3 por defecto: Chrome/Edge **87** (nov-2020),
  Firefox **88** (abr-2021), Safari **16** (2020).

---

## 2. TLS

### Lo que sigue igual — de memoria

- **Jerarquía de confianza X.509 / PKI**: AC → intermedia → hoja; validación de
  cadena, SAN, CN. **La PKI sigue siendo el ancla de la autenticidad del
  servidor.** Lo que cambió fue el key exchange, no la PKI.
- Certificados de servidor, autenticación de cliente opcional, ALPN, SNI.
- **Cifrado simétrico**: AES-GCM (y ChaCha20-Poly1305, `RFC 7905`);
  **hash SHA-256**; HKDF; **ECDHE con X25519 o P-256**.
- **AEAD** es obligatorio, no opcional.
- Errores de validación: certificado expirado, CN/SAN que no coincide, cadena no
  confiable, reloj desviado.

### Lo que cambió

- **SSL 2.0 → OBSOLETO** (`RFC 6176`, 2011).
- **SSL 3.0 → OBSOLETO** (`RFC 7568`, 2015, por POODLE).
- **TLS 1.0 y 1.1 → Historic** (`RFC 8996`, 2021, BCP 195). En 2012 se
  enseñaban como negociables.
- **`RFC 9155` (2021):** depreca **MD5 y SHA-1** como hashes de firma en TLS 1.2.
- **TLS 1.3: `RFC 8446` (2018) → `RFC 9846` (11-jul-2026)**, que además absorbe
  TLS 1.2 (`RFC 5246`). Cambios de fondo:
  - **Solo AEAD**: se eliminaron CBC, HMAC-SHA1, MD5, DES/3DES, RC4 y el
    **RSA key transport** estático.
  - El **"cipher suite" se parte en tres**: cifrado del registro (AEAD),
    **key exchange**, y **firma del handshake**.
  - **Latencia: 1-RTT** (o **0-RTT** con PSK / sesión reanudada; vulnerable a
    replay → mitigado con tokens anti-replay; `RFC 8470`).
  - **Solo key exchange efímero (ECDHE) o PSK(+ECDHE)**: **forward secrecy
    obligatorio**.
  - **Compresión eliminada** (CRIME/BREACH), **renegociación eliminada**.
- **QUIC usa TLS 1.3, pero no "TLS 1.3 normal"** (`RFC 9001`): el handshake **no
  va dentro de un stream de bytes** sino en frames `CRYPTO`, así que un middlebox
  que solo entienda TLS/TCP no puede inspeccionarlo; y las claves del transporte
  **se derivan** de los secretos del handshake TLS.
- **DTLS 1.3 = `RFC 9147`** (2022), base de la seguridad de WebRTC.
- **Post-cuántico (nuevo de 2024–2026)**: **`RFC 10024` (ago-2026)** define el key
  agreement híbrido: **X25519MLKEM768**, SecP256r1MLKEM768, SecP384r1MLKEM1024.
  **Aproximadamente la mitad del tráfico HTTPS de 2026** negocia híbrido PQ según
  Cloudflare Radar. `RFC 9794` (2025) da la terminología.
  ⚠️ **`RFC 9846` NO incluye los grupos PQ**: se añaden aparte en RFC 10024. Buen
  ejemplo de extensibilidad vía negociación + registro IANA.
- **DH estático NO da forward secrecy** (Logjam, 2015). Hoy, en TLS 1.3, la FS es
  estructural.

---

## 3. DNS

### Lo que sigue igual — de memoria

- **Jerarquía y delegación**: root → TLD → autoritativo.
- **Iterativo vs. recursivo**. El **stub resolver** del SO consulta **iterativamente**
  al **resolver recursivo**; el recursivo consulta **iterativamente** a los
  autoritativos. Esto no cambió desde 1987.
- **Estructura del mensaje**: ID, flags (`QR`, `Opcode`, `AA`, `TC`, `RD`, `RA`,
  `RCODE`), QDCOUNT/ANCOUNT/NSCOUNT/ARCOUNT, secciones
  Question/Answer/Authority/Additional.
- **RCODE**: NOERROR, FORMERR, SERVFAIL, NXDOMAIN, NOTIMP, REFUSED.
- **Tipos de registro**: A, AAAA, NS, CNAME, MX, SOA, PTR, TXT, SRV, CAA.
  SOA = MNAME, RNAME, serial, refresh, retry, expire, minimum.
- **TTL y caching**.
- **Puertos**: **53 UDP y 53 TCP**; **853** (DoT, `domain-s`).
- **Round-robin / balanceo por varios registros A** — sigue usándose (Chrome y
  Safari lo aleatorizan por privacidad).

### Lo que cambió

- **DoH (`RFC 8484`, 2018) es el cambio mayor.** El DNS del navegador **ya no lo ve
  tu ISP**. Es donde un curso de 2012 (DNS en UDP/53 plano, salto de red con
  `dig`) queda más obsoleto.
  - **Firefox**: rollout de DoH por defecto desde el **25-feb-2020** para
    usuarios de EE.UU. (Cloudflare como resolver de confianza). Verificá el
    estado actual fuera de EE.UU. antes de afirmarlo.
  - **Chrome 83** (may-2020): **no cambia tu resolver** — intenta "subir" tu
    resolver actual a su versión DoH **si está en la lista de proveedores
    conocidos**, con *fallback* a DNS plano. ⇒ "Chrome usa DNS de Google por
    defecto" es **falso**.
- **DoT (`RFC 7858`, 2016)** y **DoQ (`RFC 9250`, 2022)** — DoQ elimina el HOL
  blocking de TCP.
- **`EDNS(0)` (`RFC 6891`, 2013, *Internet Standard*)**: añade el pseudo-registro
  `OPT`. Base de DNSSEC, CAA y SVCB/HTTPS.
- **`RFC 7766` (2016)**: los resolvers deben **mantener conexiones TCP abiertas y
  reutilizarlas**; prohibido cerrarla por transacción.
- **`SVCB` / `HTTPS` (`RFC 9460`, 2023)**: el DNS ahora transporta **política de
  transporte** (qué versiones de HTTP, qué IP de hint, qué prioridad), no solo
  direcciones. Habilita descubrir HTTP/3 antes de conectar.
  `RFC 9462` (DDR) permite **descubrir resolvers** en
  `_dns.resolver.arpa` sin configurar nada.
- **DNSSEC**: `RFC 4033-4035` (2005), `RFC 5155` (raíz firmada, 2010),
  `RFC 8080` (EdDSA), `RFC 8901` (multi-signer). **Despliegue**: ~**99,6 % de los
  gTLD** firmados, pero solo **~5–7 % de los dominios (2LD)** con DS.
  ⇒ **Enseñalo como el ejemplo perfecto de "estandarizado en 2005, despliegue
  Still bajo 20 años después".** **No se puede enseñar como "el DNS es seguro
  hoy".**
- **`RFC 8020` (2018):** NXDOMAIN debe tratarse como nombre de error, no como
  dominio válido (evita *domain shadowing*).
- **`RFC 8767` (2020):** se puede **servir caché vencida** cuando el autoritativo
  no responde. Cambio real de la semántica de caché,pensado para resiliencia
  frente a DDoS.
- **CAA (`RFC 8659`, 2019)**: el dominio declara qué AC pueden emitir para él.

---

## 4. TCP

### Lo que sigue igual — de memoria

- **4-tupla** (IP origen, puerto origen, IP destino, puerto destino) identifica
  una conexión TCP.
- **Máquina de estados**: CLOSED → LISTEN / SYN-SENT → SYN-RECEIVED →
  ESTABLISHED → FIN-WAIT-1 / FIN-WAIT-2 → CLOSING → TIME-WAIT → CLOSED.
  **Los 11 estados son los mismos.**
- **Three-way handshake** y **cierre de 4 vías** + **TIME_WAIT de 2×MSL**.
- **Números de secuencia de 32 bits**, **ACK acumulativo**, **ventana deslizante**.
- **Los ACKs son de bytes, no de segmentos**: `seq` = próximo byte esperado.
- **Sliding window, ACK duplicados, delayed ACK, Nagle, persist/keepalive, RTO,
  estimación de RTT (Jacobson/Karels), fast retransmit (3 dup-ACK), slow start,
  congestion avoidance, slow recovery.**
- **MTU/MSS**, negociación de opciones en el SYN (MSS, SACK permitted,
  Timestamps, Window Scale).
- **Checksum** de TCP/UDP con pseudo-cabecera.
- **Descarte de segmentos fuera de ventana.**

### Extensiones vigentes

| Extensión | RFC | Estado |
|---|---|---|
| **SACK** | `RFC 2018` (1996) | *Standards Track*. Sigo siendo comportamiento estándar. |
| **Timestamps + Window Scale** | `RFC 7323` (2014) | Obsolesce RFC 1323. **PAWS es obligatorio** si ambos extremos activan timestamps. |
| **ECN** | `RFC 3168` (2001) | *Proposed Standard*, actualizada por RFC 9768. |
| **AccECN** | `RFC 9768` (2026) | Actualiza la 3168: ECN con feedback más preciso. |
| **ABE** | `RFC 8511` (2018) | Backoff alternativo con ECN. |
| **L4S** | `RFC 9331` (2023) | ECN de umbral bajo para latencia mínima. |
| **PRR** | `RFC 6937` (2013) | **Experimental**, no estándar. |
| **Initial Window = 10 MSS** | `RFC 6928` (2013) | El valor por defecto en Linux/Windows/macOS hoy. |
| **Control de congestión** | `RFC 5681` (2009) | Los cuatro algoritmos: slow start, congestion avoidance, fast retransmit, fast recovery. |
| **CUBIC** | `RFC 9438` (2023) | ***Standards Track***. **NO fue reemplazado** — es el default de Linux, Windows y Apple. Obsolesce RFC 8312. |
| **Roadmap de RFCs de TCP** | `RFC 7414` (2015) | Buen índice para la clase. |

### Lo que cambió

- **`RFC 9293` (2022, *Internet Standard*)** consolida RFC 793 + RFC 879, 2873,
  6093, 6429, 6528, 6691. **Cualquier clase que cite "RFC 793" como la
  especificación de TCP en 2026 está desactualizada.** `RFC 1122` sigue
  definiendo el comportamiento de los hosts.
- **CUBIC es el default global** (RFC 9438). En 2012 se enseñaba Reno/NewReno con
  un "quizá CUBIC".
- **BBR nunca fue RFC**: hoy es `draft-ietf-ccwg-bbr` (grupo CCWG), estado
  *Experimental*, especifica **BBRv3**. Usa en producción tanto en TCP (Linux) como
  en QUIC (Quiche de Chromium, MVFST de Meta). ⚠️ **`RFC 8312` es CUBIC, no BBR.**
  ⇒ **Punto pedagógico: el algoritmo con más despliegue no es el único estándar.**
- **QUIC (`RFC 9000`/`9001`/`9002`)** es un transporte **completo**, con su propia
  recuperación, **PLPMTUD integrado** y control de congestión enchufable, que
  compite con TCP.
- **MPTCPv1 (`RFC 8684`, 2020)**: primer estándar *multipath* de TCP. En Linux
  desde v5.6; desplegado por Apple (Siri, Music, Maps, Wi-Fi Assist) y algunos
  operadores, en >80 países. **Pero el share de tráfico sigue siendo marginal**
  (~0,4 % de bytes pico) y los middleboxes lo degradan. ⇒ **MPTCP es real pero NO
  es la respuesta dominante al multipath** — esa es la **migración de conexión de
  QUIC**.

---

## 5. IPv6 y transición

### Lo que sigue igual — de memoria

- Dirección de **128 bits**, notación hex y compresión con `::`.
- **Cabecera fija de 40 bytes**: Version, Traffic Class, **Flow Label**, Payload
  Length, Next Header, Hop Limit, Src, Dst.
- **Cabeceras de extensión** encadenadas por Next Header (Hop-by-Hop, Routing,
  Fragment, Destination Options, AH, ESP). En IPv6 el Payload Length **excluye**
  las cabeceras de extensión.
- **Ámbitos**: unicast global, **link-local `fe80::/10`**, unique local
  `fc00::/7`, multicast `ff00::/8`. **Site-local está deprecado.**
- **`/64` es la unidad de subred** estándar.
- **ICMPv6 (`RFC 4443`)**: Neighbor Discovery (RS/RA/NS/NA, Redirect),
  **Packet Too Big (tipo 2)**, Destination Unreachable (1), Time Exceeded (3),
  Parameter Problem (4).
- **NDP es "ARP para IPv6"** pero en **multicast sobre ICMPv6**, e incluye
  **autoconfiguración** y **DAD**.
- **Un router IPv6 NO fragmenta.** El **origen** fragmenta.
- **MTU mínimo absoluto de IPv6 = 1280** (`RFC 8200` §5, verificado textualmente).

### Lo que cambió — y acá está la noticia fuerte

- **IPv6 dejó de ser "el futuro".** El **28 de marzo de 2026** el acceso a
  Google por IPv6 **superó el 50 % por primera vez (50,10 %)**.
  - Fuentes: Internet Society Pulse, APNIC (abr-2026), The Register (abr-2026).
  - Otras mediciones: APNIC ~42-43 % (cobertura de capacidad), Cloudflare ~40 %
    (tráfico por bytes), Internet Society Pulse ~43 % agregado.
  - **Es desigual**: líderes Francia ~73 %, India ~72 %, Arabia Saudita ~65 %;
    rezagados Italia ~17 %, España ~10 %, Egipto ~4 %; **China <5 %**.
  - ⇒ **Dato para el aula:** en 2012 el curso decía "IPv6 llega en 10 años". La
    respuesta correcta en 2026 es: "ya pasó la mitad en los usuarios de Google,
    pero es desigual, China sigue en <5 %, y la cifra depende de **qué** midas".
- **El agotamiento de IPv4 es un hecho consumado.** **RIPE NCC hizo su última
  asignación /22 el 25-nov-2019** a las 15:35 CET. APNIC se agotó en abr-2011,
  ARIN en sept-2015, LACNIC en 2020, AfriNIC en abr-2017. RIPE hoy mantiene una
  *waiting list* para un único /24 recuperado.
- **CGNAT (*Carrier-Grade NAT*) es ubicuo en los ISP**: es el nuevo default de la
  capa 3 de acceso y merece una clase propia. Rompe conectividad entrante,
  complica la señalización (SIP/IMS), rompe IPsec y rompe peer-to-peer.
- **NAT64 `RFC 6146` / DNS64 `RFC 6147`** (2011), maduraron. Prefijo bien conocido
  **`64:ff9b::/96` = `RFC 6052`**, `RFC 8880` (`ipv4only.arpa`, 2020).
  **SIIT `RFC 6145` → obsoleto por `RFC 7915`** (2016).
- **464XLAT sigue siendo borrador** (`draft-ietf-v6ops-464xlat`) — la transición
  no cerró.
- **DS-Lite = `RFC 6333`** (2011): dual-stack *stateless* ligero.
- **NDP se amplió en 2026**: **`RFC 9926`** (feb-2026) permite registrar un prefijo
  en los routers vecinos.
- **`RFC 6177` (2011)** ya no recomienda asignar `/48` por sitio final; en la
  práctica los RIR asignan `/48` (a veces `/56`) al **operador**.
- **Por qué NAT rompe IPv6:** NAT depende de direcciones privadas + reescritura de
  puertos para multiplexar. IPv6 tiene espacio de sobra, así que **no necesita
  traducción**; peor, NAT rompe la **extensibilidad extremo a extremo** (cabeceras
  de extensión, mobility), **no es stateful-friendly con IPsec**, y obliga a los
  hosts IPv6-only a usar 464XLAT/PLAT para alcanzar contenido IPv4. ⇒ **La meta de
  IPv6 es eliminar el NAT.**

---

## 6. Fragmentación, MTU y Path MTU

### Lo que sigue igual — de memoria

- **MTU** = la mayor PDU de capa 3 que el enlace transmite sin fragmentar.
- **Ethernet MTU por defecto = 1500**. **Jumbo = 9000** — pero es una **convención,
  no un estándar IEEE**, y se usa sobre todo intra-datacenter y almacenamiento.
  **Nunca** sobre Internet o túneles sin *clamp MSS*.
- **IPv4 fragmenta en los routers (DF=0)**; **IPv6 fragmenta solo en el origen**.
- **ICMPv4 tipo 3 código 4** (Fragmentation Needed and DF was Set) vs.
  **ICMPv6 tipo 2** (Packet Too Big).
- **El PMTU se cachea en el origen**, es **por ruta**, y es **≤ al MTU del salto
  más estrecho**.
- El clásico **"576 bytes mínimo"** en IPv4 viene de RFC 791 y RFC 1122 §3.2.1.

### Lo que cambió

- **`RFC 4821` (2007, *Experimental*) → `RFC 8899` (sep-2020, *Standards Track*):
  DPLPMTUD.** La PMTUD dejó de **depender de ICMP**: el transporte sondea con su
  propio paquete de datos. Es la respuesta canónica al **"PMTUD black hole"**
  (firewalls que filtran ICMP), y es **lo que QUIC usa por defecto**
  (`RFC 9002` §6, PLPMTUD integrado).
- ⚠️ **DPLPMTUD es *loss-based***, lo que introduce ambigüedad entre pérdida por
  MTU y pérdida por congestión. Pocas implementaciones lo soportan (en Linux es
  una opción, no el default del stack TCP).
- **El "9000 → 1500 cliff"** es hoy un problema real y documentado: con **ECMP**,
  el PMTU es **propiedad del camino, no del prefijo**, así que flujos distintos al
  mismo destino pueden tener PMTU distinto.
- **MPLS / VXLAN / IPsec / GRE / WireGuard consumen MTU**: cada overlay baja el
  MTU efectivo. Por eso el desajuste de MTU es **omnipresente** en redes híbridas
  cloud/bare-metal.
- **Hardening de fragmentos IPv6**: `RFC 5722` (2009) prohíbe fragmentos solapados;
  `RFC 6946` (2013) recomienda tratar los **fragmentos atómicos** como no
  fragmentados; `RFC 5095` (2007) deprecó el Routing Header tipo 0.
- **Síntoma clásico del black hole**: "SSH funciona, algunos sitios HTTPS quedan
  colgados". Diagnóstico: `ping -M do -s <size>` (Linux), `tracepath`.

---

## 7. BGP y enrutamiento

### Lo que sigue igual — de memoria

- **BGP-4 (`RFC 4271`)** sigue siendo la especificación vigente.
- **`AS_PATH` es un *path-vector***: la lista de AS por los que pasa la ruta, y
  **un AS no acepta una ruta cuyo AS_PATH contenga su propio AS**. Eso es lo que
  hace que BGP sea *path-vector* y no *distance-vector*.
- **Sesión sobre TCP/179**: OPEN → OPEN/ACK → UPDATE → KEEPALIVE.
- **eBGP vs. iBGP**; la regla de "no re-anunciar a iBGP lo aprendido de un iBGP"
  obliga al **full-mesh iBGP** → se usan **Route Reflection (`RFC 4456`)**.
- **Atributos**: LOCAL_PREF (↑ mejor), AS_PATH length (↓ mejor), MED (↓ mejor,
  **comparable solo entre rutas del mismo AS vecino**), ORIGIN, Communities
  (`RFC 1997`).
- **"Hot potato"**: cada AS prefiere salir por el eBGP de **menor métrica IGP**.
  **MED** es la herramienta para anular esa preferencia.
- **OSPFv2 (`RFC 2328`)** = link-state, SPF/Dijkstra, áreas, DR election,
  multicast 224.0.0.5/6, TTL 1 en hello.
- **RIPv2 (`RFC 2453`)**: métrica ≤15, poison reverse (16), split horizon,
  triggered updates, hold-down. **Sigue siendo *Internet Standard*, pero está
  deprecado de facto en Internet**: sobrevive en laboratorios y campus.
- **Split horizon, poison reverse, hold-down** en distance-vector.

### Lo que cambió

- **`RFC 9234` (may-2022): BGP sin MD5 de sesión.** Define **roles BGP**
  (Provider / Customer / Peer / Lateral / Internal) declarados en OPEN y UPDATE
  para prevenir y detectar *route leaks*. Reemplaza al `RFC 2385` (MD5 de sesión)
  como mecanismo de referencia.
- **RPKI / ROA**: `RFC 6810` (RTR) y **`RFC 6811`** (BGP Prefix Origin
  Validation). Maduró de idea a **despliegue real**. La seguridad de BGP pasó de
  "confiar en AS_PATH" a "**validar origen con RPKI**".
- **`BGP-LS` → `RFC 9552`** (dic-2023), obsoleta RFC 7752.
- **EVPN (`RFC 7432`) + VXLAN (`RFC 7348`)**: hoy son **el estándar de overlay de
  datacenter**, no solo académico. VXLAN encapsula sobre **UDP/4789**.
- **Segment Routing**: `RFC 8402` (arquitectura, 2018), `RFC 8660` (SR-MPLS),
  **`RFC 8986` (SRv6)**. Es el **sucesor de facto** de MPLS LDP/RSVP-TE en
  despliegues nuevos: *source routing* con SIDs y **estado solo en el borde de
  ingreso**. SRv6 codifica los SIDs en la cabecera IPv6 y **elimina el MPLS por
  completo**.
- **OSPFv3 (`RFC 5340`)**, IS-IS para IPv6 (`RFC 5308`): mecanismos idénticos,
  independientes de IPv6.
- **AS de 32 bits**: `RFC 4893` + `RFC 6793`; notación decimal `RFC 5396`.
  **Ya no existe el problema del AS de 16 bits.**

---

## 8. Ethernet y capa 2 conmutada

### Lo que sigue igual — de memoria

- **Formato de trama**: preámbulo 7 + SFD 1, **MAC destino 6 + MAC origen 6**,
  Ethertype 2, payload, **FCS 4**. **MTU 1500**.
- **CSMA/CD**: *exponential backoff*, **slot time 512 bits**, min frame 64 B,
  max frame 1518 B.
- **ARP (`RFC 826`)**: request en **broadcast**, reply en **unicast**. El
  **gratuitous ARP** sigue usándose (anuncio, DHCP, failover de gateway, VRRP) y
  sigue siendo una **fuente clásica de ARP spoofing / cache poisoning**.
- **MAC learning**: el bridge aprende la **MAC origen** de cada trama, asocia
  puerto; **flooding** si el destino es desconocido; **unicast** si se conoce.
- **802.1Q VLAN**: tag de 4 bytes, **VLAN ID de 12 bits (1–4094)**, `0` = sin tag
  (PVID).
- **STP/RSTP** y sus estados (Blocking, Listening, Learning, Forwarding), Bridge ID
  con prioridad base **32768**.
- **Loops en capa 2 = broadcast storm**: sigue siendo la razón de ser del STP.

### Lo que cambió

- **Half-duplex Ethernet es historia por encima de 1 Gb/s.** Es una decisión de
  **IEEE 802.3**, **no** una RFC de IETF (⚠️ **no existe RFC que lo depreque**;
  `RFC 8984` es JSCalendar). A 10GbE+ el full-duplex point-to-point es
  obligatorio.
- **PERO half-duplex no desapareció del todo**: **IEEE 802.3cg 10BASE-T1S**
  (single-pair Ethernet, PLC industrial) es **obligatoriamente half-duplex** con
  **PLCA**. En IETF, el módulo YANG `csma-cd` de `802.3cf` está marcado
  `status deprecated`.
- **`802.1Q-2022`** es el estándar actual (precedido por 802.1Q-2018). 2018
  rolló los amendments de TSN/gating: **802.1Qbv** (scheduled traffic),
  **802.1Qbu** (frame preemption, con 802.3br), **802.1Qci** (per-stream
  filtering/policing). 2022 agrega **802.1Qcc** (SRP) y **802.1Qcr** (async traffic
  shaping).
- **C-TAG (`0x8100`) vs. S-TAG (`0x88A8`)**: doble etiquetación para *provider
  bridges*; hoy es lo estándar en carrier Ethernet y EVPN-VXLAN.
- **LAG: `802.3ad` (2000) → `802.1AX`**; la revisión actual es **`802.1AX-2020`**.
- **RSTP (`802.1w`) es el default real**; MSTP (`802.1s`) para varias VLAN
  instances.
- ⚠️ **El "aging de 300 s" de la tabla MAC es default de FABRICANTE, no un valor
  mandated por IEEE.** Enseñá "típicamente 300 s en switches comerciales,
  configurable", **no** "el estándar IEEE dice 300 s".

---

## 9. Wi-Fi / 802.11

### Lo que sigue igual — de memoria

- **CSMA/CA** sigue siendo **el método de acceso** fundamental. En 802.11
  **no existe full-duplex**: el medio es inherentemente compartido.
- **DCF**: backoff exponencial, IFS (SIFS/DIFS/EIFS), **NAV**, RTS/CTS opcional.
- **EDCA**: 4 colas de acceso (VO, VI, BE, BK) + Block ACK.
- **RTS/CTS** sigue resolviendo el **hidden node problem**. El **exposed
  terminal** sigue sin resolverse del todo.
- Tramas de gestión: Beacon, Probe, Auth, Assoc, Deassoc. **BSSID/DSN**.
- Bandas: 2,4 GHz (alcance, interferencia), 5 GHz (capacidad), 6 GHz (más
  capacidad, menos penetración).

### Lo que cambió

- **Wi-Fi 6/6E (`802.11ax`, 2020)**: **OFDMA** (UL y DL), **BSS coloring**, 1024-QAM,
  **TWT** (Target Wake Time), MU-MIMO.
- **Wi-Fi 7 (`802.11be`)**: aprobado por IEEE SA en **sept-2024**, publicado como
  **`IEEE 802.11be-2024`** el **22-jul-2025**. **Wi-Fi CERTIFIED 7** (Wi-Fi
  Alliance, ene-2024). Features: **320 MHz**, **4096-QAM**, **MLO** (Multi-Link
  Operation), EHT-OFDMA, HARQ opcional.
- **Wi-Fi 8 (`802.11bn`)**: TGbn establecido nov-2023, objetivo mayo-2028. El foco
  está en **reliabilidad**, no en throughput.
- **WPA3 (2018)**: **SAE** (Simultaneous Authentication of Equals, basado en
  Dragonfly) reemplaza el 4-way handshake PSK de WPA2, resistente a ataques de
  diccionario offline. **802.11w (PMF)** pasa a ser **obligatorio**.
- **`802.11bt` — criptografía post-cuántica en WiFi**: PAR de sept-2025, objetivo
  **2029**. Frente nuevo.
- Un curso 2012 sobre **802.11n** está **4 generaciones** atrás.

---

## 10. Movilidad (el tema "IP Móvil")

### Lo que sigue igual — de memoria

- **4-tupla identifica conexión TCP**; **Connection ID identifica conexión QUIC**.
- **NAT rebinding** (cambio de puerto por un NAT) **rompe TCP**, **no rompe QUIC**.
- **Happy Eyeballs**: hacer v4 y v6 **en paralelo** con un timer, no
  secuencialmente. **`RFC 8305`** (2017, obsoleta RFC 6555).
- **IPv6 no tiene proxy ARP** (usa NDP): por eso IPv6 favorece el modelo
  extremo a extremo.

### Lo que cambió — y acá hay que reencuadrar

- **Mobile IPv4 (`RFC 5944`, 2010) y Mobile IPv6 (`RFC 6275`, 2011) siguen
  formalmente en Standards Track: NO están obsoletos. El punto es que NO SE
  DESPLEGAN.** El mundo real usa **VPN**, **CGN** y **migración de conexión**.
- **Proxy ARP (`RFC 1027`)** sigue existiendo en VPNs site-to-site, pero es cada
  vez más un **anti-patrón** de la era IPv4-NAT que IPv6 elimina.
- **QUIC connection migration (`RFC 9000` §9)** es la respuesta de la industria a
  la movilidad **en la capa de transporte**. El texto de la RFC dice explícitamente
  que el diseño permite que las conexiones sobrevivan a cambios de topología o de
  mapeo de direcciones, **como los que causa el NAT rebinding**.
- **El `Connection ID` (`RFC 9000` §5.1) es el cambio de paradigma**: la identidad
  de la conexión **deja de ser la IP**. Eso habilita (a) migración de conexión,
  (b) NAT rebinding sin romper, (c) balanceo en servidores, (d) CID de largo 0 si
  solo usás la 5-tupla (y entonces no hay migración).
- ⇒ **Recomendación para el curso: reencuadrar, no eliminar.** Explicar **por qué
  la movilidad IP no se desplegó** (complejidad, middleboxes, CGN, roaming
  inter-tecnología) **es más valioso** que los mecanismos home-agent/care-of-address.

---

## 11. Gestión de redes

### Lo que sigue igual — de memoria

- El **modelo SNMP**: **gestor / NMS** ↔ **agente** en el dispositivo.
- **Polling** (`GET` / `GETNEXT`, *pull*) + **traps / notificaciones** (*push*).
- **MIB**: jerarquía de **OIDs**, ASN.1 / SMIv2. **MIB-II** = `1.3.6.1.2.1`.
- **Community strings** (v1/v2c) vs. **USM users** (v3).
- **NETCONF**: XML sobre **SSH**, RPCs `<get>`, `<get-config>`, `<edit-config>`,
  `<copy-config>`, `<commit>`, `<lock>`; datastores **running / candidate /
  startup**.

### Lo que cambió

- **NETCONF (`RFC 6241`, 2011) + YANG (`RFC 7950`, 2016, *Internet Standard*)**
  pasaron de propuesta a **el estándar de facto para configuración automatizada**.
  Están en Cisco IOS XE/NX-OS, Juniper Junos, Arista EOS, Nokia SR OS, Huawei VRP.
- **NMDA (`RFC 8342`, 2018)**, **RESTCONF (`RFC 8040`, 2017)**,
  **YANG-Push (`RFC 8639`/`8640`/`8641`, 2019)**: habilitan **telemetría
  *streaming* (push)**, no solo polling.
- **gNMI** (Google, no-IETF) es el competidor práctico de NETCONF en los vendors
  grandes.
- **SNMPv3**: `RFC 3411` (arquitectura), **`RFC 3414` (USM)**,
  **`RFC 3415` (VACM)**, `RFC 3413` (aplicaciones), `RFC 3416` (operaciones),
  `RFC 6353` (transporte TLS), `RFC 7860` (HMAC-SHA-2 en USM),
  `RFC 9456` (actualización del transporte TLS).
- **La posición de la propia IETF (Netconf WG, 2024)**, textual: *"SNMP & MIBs
  **nunca alcanzaron tracción significativa** en la industria **para
  configuración**… esperamos una **disminución significativa** de despliegues de
  SNMP en los próximos 10 años"*.
- **La realidad**: SNMP sigue siendo el rey del **polling de métricas**;
  NETCONF/YANG es el rey de la **configuración** y de la **telemetría
  estructurada**.
- **BMP (`RFC 7854`)** para monitorear BGP desde fuera; **IPFIX (`RFC 7011`)** para
  flujos; **Network Telemetry Framework (`RFC 9232`)**.
- ⇒ **Reencuadrar honestamente:** SNMP es *legacy* para configuración e
  **irreemplazable todavía** para polling. La comparación SNMP vs YANG
  (MIB vs modelo, pull vs push, *CLI scraping*) es un excelente ejercicio.

---

## 12. Multimedia y QoS

### Lo que sigue igual — de memoria

- **RTP (`RFC 3550`, 2003)** — **sin cambios desde 2003**, sigue *Internet
  Standard*. Y **RTCP** para feedback y monitorización.
- **RTP**: número de secuencia, timestamp de muestreo, **SSRC**, payload type,
  header extension. **RTCP**: SR/RR/SDES/BYE/APP.
- **SRTP (`RFC 3711`)** = confidencialidad + integridad + anti-replay.
- **Modelo I/P/B + GOP + intervalo de keyframe + jitter buffer + delay de
  decodificación** — **exactamente igual en 2026**; lo que cambió son los códecs
  concretos.
- **DSCP / PHB**: **EF** (Expedited Forwarding), **AF** (AF11..AF43),
  Default/BE, CS. **Marking en el borde** + PHB en cada hop.
- **Policing vs shaping**: policing con token bucket (descarta o remarkea lo que
  excede, sin buffer); shaping con cola + token bucket (retrasa y suaviza,
  introduce latencia). **Ingress policing + egress shaping** sigue siendo la
  arquitectura. **Esto no cambió.**
- **H.264/AVC** como fallback universal de decodificación.

### Lo que cambió

- **RTP base no cambió**, pero se le añadieron **header extensions
  (`RFC 8285`, 2017, obsoleta RFC 5285)** y **RTCP XR (`RFC 3611`)**.
- **SRTP es obligatorio en WebRTC** — la seguridad de RTP dejó de ser opcional.
  **DTLS-SRTP** es la base de la seguridad de WebRTC.
- **Códecs — acá es donde un curso 2012 más se desactualiza:**
  | Códec | Situación 2026 | Dónde vive |
  |---|---|---|
  | **MPEG-2** | sigue vivo, pero confinado | TV digital de broadcast (DVB-T/S, ATSC), DVD, video de contribución |
  | **MPEG-4 Part 2** | reemplazado por H.264; irrelevante | — |
  | **H.264/AVC** | ~**84-85 %** de producción; el fallback universal | todas partes |
  | **H.265/HEVC** | ~**65 %** de producción; **nativo en Apple** |Attention: royalties (Access Advance, Nokia, InterDigital) |
  | **AV1** (2018) | ~**17-19 %** de producción → ~**57 %** de alcance combinado fin de 2026; **Netflix ~30 %** de su streaming (dic-2025); **YouTube >75 %** del video de alta resolución | royalty-free |
  | **VVC/H.266** | **<5 %**, atascado por licencias | casi nadie lo despacha |
- **IntServ (`RFC 2211`/`2212`/`2213`, 1997) ≈ NO se despliega a escala.** El
  problema fundamental —mantener **estado por flujo en cada router**— es
  insostenible. **RSVP sí se usa** en RSVP-TE (`RFC 3209`) para traffic
  engineering de MPLS. ⇒ **Enseñá IntServ como el modelo que no escaló, y
  DiffServ como el que ganó.**
- **DiffServe ganó**: `RFC 2474` (DS field), `RFC 2475` (arquitectura),
  **`RFC 3246` (EF)**, `RFC 2597` (AF), `RFC 4594` (guidelines de clases de
  servicio), `RFC 8622` (LE PHB, obsoleta RFC 3662).
- **MPLS**: `RFC 3031` (arquitectura), `RFC 3032` (label stack), `RFC 4364`
  (MPLS VPN). **Sigue desplegándose masivamente en carriers**, pero su **plano
  de control se está moviendo a Segment Routing**.
- **MPLS en datacenter fue reemplazado por EVPN-VXLAN.**

---

## 13. Seguridad: qué enseñar de "integridad / no repudio" en 2026

### Lo que sigue igual — de memoria

- **Hash: SHA-256** (nunca MD5 ni SHA-1).
- **Simétrico: AES-GCM / ChaCha20-Poly1305.**
- **Firma: RSA-PSS / ECDSA P-256 / Ed25519.**
- **Key agreement: X25519 ECDHE** (o híbrido ML-KEM).
- **PKI X.509**: cadena AC → intermedia → hoja, **SAN**, validación.
- **Forward secrecy** con (EC)DHE o PSK. **AEAD** (confidencialidad + integridad
  en uno). **HKDF**.
- **DH vs ECDHE**: ambos dan FS; **DH estático NO da FS** (Logjam).
- **No repudio = firma + identidad vinculable** (certificado cliente, PGP, o
  infraestructura: DNSSEC / RPKI).

### Lo que cambió

- **RSA key transport eliminado** en TLS 1.3. **RSA-PSS** es el modo de firma
  moderno; el `PKCS#1 v1.5` es legacy.
- **ML-KEM híbrido (`RFC 10024`, ago-2026)** es el nuevo key agreement de facto.
- **SHA-1 formalmente retracted**: NIST lo retiró para firmas en 2011;
  **SHAttered (2017)** halló colisiones prácticas. **`RFC 9155` (2021)** depreca
  explícitamente **MD5 y SHA-1** en TLS 1.2. **MD5 roto** desde 2004 (rogue CA en
  2008).
- **Ed25519 es el default en SSH** (`RFC 8709`, 2020) y creciente en X.509.
- **HTTP Message Signatures (`RFC 9421`, 2024)**: firma de *componentes* de un
  mensaje HTTP, resistente a transformaciones de intermediarios. Es
  integridad/no-repudio **a nivel de mensaje HTTP**.
- **OpenPGP: `RFC 9580` (2024)** reemplaza RFC 4880.
- **La lección de 2026:** **integridad/autenticidad es *relativa a un ancla de
  confianza*, y hay un ancla distinta por ámbito**:

  | Ámbito | Ancla | RFC |
  |---|---|---|
  | Transporte web | PKI / CA (X.509) | `RFC 8446`→`9846` |
  | DNS | DNSSEC + Root KSK | `RFC 4033-4035`, `5155` |
  | Enrutamiento | RPKI / ROA | `RFC 6811` |
  | Capa 2 | 802.1X / MAB, Port Security | — |
  | Email | S/MIME o PGP | `RFC 9580` |

  Un curso que sólo enseña "integridad = HTTPS" se queda corto.
- **El no-repudio real es raro y costoso**: requiere clave privada controlada por
  el firmante + identidad vinculable. **DNSSEC y RPKI son no-repudio de
  *infraestructura*** (quién originó un nombre o un prefijo), no de una persona.

---

## 14. Programación y sockets

### Lo que sigue igual — de memoria

- **Berkeley/POSIX sockets**: `socket()`, `bind()`, `listen()`, `accept()`,
  `connect()`, `send()`, `recv()`, `setsockopt()`, `select()`/`poll()`/`epoll()`.
  **Esto no cambió**: Go, Rust, Node y Python lo envuelven, pero el kernel sigue
  siendo BSD sockets.
- `AF_INET` / `AF_INET6` / `AF_UNIX`, `SOCK_STREAM` / `SOCK_DGRAM`.
  `sockaddr_in` / `sockaddr_in6`.
- **TCP = 4-tupla**; **socket UDP = 2-tupla**.
- **Modelo cliente-servidor** con `listen`/`accept`.
- **Pseudocódigo de control de congestión**: sigue siendo **el mejor ejercicio de
  redes**. Los problemas de examen de FING que piden "implementar la detección y
  el control de congestión" son exactamente de este tipo.

### Lo que cambió

- **La herramienta de laboratorio por defecto pasó de `tcpdump` a Wireshark**
  (libpcap/npcap, filtros de display, y **descodificación built-in de HTTP/3, QUIC,
  TLS 1.3, DNSSEC, DoH**). `tcpdump` sigue para captura masiva/headless.
- **Sniffear HTTP/3 es más difícil**: va cifrado en el cable con claves derivadas
  de TLS 1.3, y las cabeceras HTTP/3 van en QPACK. Necesitás **instrumentación
  en el endpoint** (registro de QUIC con claves de depuración, o un proxy MITM).
  ⇒ **Es un cambio real de la pedagogía del sniffing.**
- **IPv6 dual-stack / v4-mapped addresses** (`::ffff:a.b.c.d`,
  `IPV6_V6ONLY=0`) es un tema obligatorio de cualquier curso de sockets hoy: es la
  razón de una larga lista de vulnerabilidades de clase y de la complejidad del
  dual-stack.
- ⚠️ **Matiz sobre la 2-tupla de UDP:** la clave de demux real en el kernel es la
  **5-tupla** `(proto, srcIP, srcPort, dstIP, dstPort)`. La "2-tupla (IP, puerto)"
  es la simplificación clásica para un socket UDP *no conectado*. **En 2026 hay
  que añadir**: QUIC multiplexa muchas conexiones en el **mismo 5-tupla** vía
  **Connection ID** (`RFC 9000` §5.1, `RFC 8085`).

---

## 15. Puertos bien conocidos — todos verificados contra el registro IANA

| Puerto | Servicio | Nota |
|---|---|---|
| 20/21 | FTP | datos/controla |
| **22** | SSH | también `22/udp` y `22/sctp` |
| **25** | SMTP | también `25/udp` |
| 53 | DNS | `53/tcp` + `53/udp` |
| **67 / 68** | DHCP server / client | `bootps` / `bootpc`. **DHCPv6 usa 546/547** |
| **80** | HTTP | también `80/udp` y `80/sctp` |
| 110 / 995 | POP3 / POP3S | ambos también `udp` registrados, uso real TCP |
| 143 / 993 | IMAP / IMAPS | `imap` **solo tcp** |
| 161 / 162 | SNMP / SNMP-trap | |
| **179** | BGP | también `179/udp` y `179/sctp` |
| 443 | HTTPS | **también `443/udp` = HTTP/3** y `443/sctp` |
| 465 | submissions | TLS implícito, deprecada por ESMTP AUTH |
| 587 | submission | SMTP con AUTH |
| **853** | DoT | `domain-s` |
| 1194 | OpenVPN | |
| 1812/1813 | RADIUS | |
| 51820 | WireGuard | |

---

## 16. Cronología para contar en clase

| Año | Hecho |
|---|---|
| 2011 | RFC 6177 (fin del /48 por sitio) · DNS64/NAT64 · MIPv6 · NETCONF |
| 2013 | RFC 6928 (IW=10 MSS) · RFC 6891 (EDNS(0)) |
| 2014 | RFC 7230-7235 reescriben HTTP/1.1 |
| 2015 | RFC 7568 (SSL 3.0 obsoleto) · HPACK (RFC 7541) |
| 2016 | RFC 7748 (X25519) · RFC 8305 (Happy Eyeballs) · RFC 8684 (MPTCP) |
| 2017 | RFC 8200 (IPv6) · RFC 8201 (PMTUD IPv6) · RFC 7838 (Alt-Svc) |
| 2018 | RFC 8446 (TLS 1.3) · RFC 8312 (CUBIC) · RFC 8511 (ABE) · WPA3 |
| **2019** | **RIPE NCC agota IPv4** (25-nov) |
| 2020 | RFC 8484 (DoH) · RFC 8899 (DPLPMTUD) · RFC 8767 (caché stale) · Wi-Fi 6E |
| 2021 | RFC 9000/9001/9002 (QUIC) · RFC 8996 (depreca TLS 1.0/1.1) · RFC 9002 (BBR en el draft) |
| 2022 | RFC 9110/9112/9113/9114 (HTTP) · RFC 9293 (TCP) · RFC 8032 (CUP) |
| 2023 | RFC 9438 (CUBIC *Standards Track*) · RFC 9331 (L4S) · RFC 9460 (SVCB/HTTPS) |
| 2024 | RFC 9580 (OpenPGP) · RFC 9421 (HTTP Message Signatures) · **Wi-Fi 7** |
| **2026** | **IPv6 >50 % en Google** (mar) · RFC 9846 (TLS 1.3) · **RFC 10024 (PQ híbrido)** · RFC 9768 (AccECN) |
