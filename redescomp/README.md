# Introducción a las Redes de Computadoras — 48 clases de preparación

Material de estudio completo para el examen de **Introducción a las Redes de
Computadoras** (código **1433**) de la Facultad de Ingeniería, Universidad de la
República.

---

## Qué es esto

El curso dice textualmente *"A partir de 2012 esta asignatura no se dicta más"*.
Fue reemplazado por *Redes de Computadoras (1446)* y *Aspectos Avanzados de
Redes de Computadoras (1448)*, **pero es la misma cátedra con los mismos
docentes** (Sabiguero, Baliosian, Grampín, Rodríguez, Sanguinetti, Vidal…). Por
eso:

- Los **50 exámenes oficiales de 1998 a 2011**, con sus soluciones, son la mejor
  guía de qué se pregunta. Y son los que resolvo en las clases.
- El temario **clásico** se sigue preguntando: capas, retardos, subnetting,
  tablas de enrutamiento, TCP, DNS, HTTP, CRC, CSMA/CA, seguridad.
- Lo que **cambió** son las versiones de los protocolos. Cada clase tiene una
  sección fija **«⚠️ Actualización a 2026»**.

---

## ✅ Estado: 48/48 clases completas (finalizado)

| Entregable | Cantidad | Ubicación |
|---|---|---|
| **Clases en markdown** | **48 / 48** | `clases/clase-01-*.md` … `clase-48-*.md` |
| **PDFs individuales** | **48** | `pdf/clase-NN-*.pdf` |
| **Libro completo** | **1** (26 MB) | `pdf/Introduccion-a-las-Redes-de-Computadoras.pdf` |
| **Diagramas SVG** | **28** | insertados automáticamente en los PDFs |
| **Exámenes oficiales resueltos** | 50 exámenes, 1998–2011 | `material-oficial/examenes/` |
| **Simulacros de examen** | 4 (clases 7, 15, 23, 37) + 1 final (clase 48) | dentro de las clases |

**Las últimas 5 clases que se escribieron** (las que faltaban al último corte):

| # | Archivo | Tamaño | Qué trae |
|---|---|---|---|
| 15 | `clase-15-dhcp-simulacro2.md` | 48 k | DORA, lease, T1/T2, `169.254/16`, RARP + **Simulacro 2** completo |
| 43 | `clase-43-wifi-80211.md` | 41 k | CSMA/CA (DCF), estación oculta/expuesta, NAV, RTS/CTS, EDCA, WPA3/SAE |
| 46 | `clase-46-gestion-snmp-netconf.md` | 57 k | Agente/gestor, MIB y OIDs, polling vs. traps, SNMPv3 (USM/VACM), **NETCONF + YANG** |
| 47 | `clase-47-seuridad-criptografia.md` | 56 k | Hash, AES/AEAD, RSA (con las cuentas a la vista), firma digital, PKI/X.509 |
| 48 | `clase-48-seuridad-ipmovil-simulacro.md` | 93 k | TLS, SSH, PGP, túneles/VPN, IDS-IPS-DPI, **IP Móvil** (HA/FA/COA, ruta triangular) + **Simulacro final** |

**Y en la clase 1** se agregó la sección **«PARTE 1 bis — Los diagramas de red»**:
qué información lleva un diagrama (los 8 bloques: identidad, L3, L2, firewall,
NAT/VIP, puertos, **estado operativo real**, metadatos), **qué tipos de diagrama
hay** (físico, lógico, VLAN/STP, firewall/NAT, flujo, secuencia, rack,
direccionamiento), los 6 pasos para hacer uno, y una **checklist**. Todo
conectado con el `VALIDACIÓN PENDIENTE` de tu imagen: la diferencia entre el
estado **de diseño** y el estado **verificado**, y por qué un diagrama sin
fecha, sin fuente y sin estado de verificación *miente con la mejor intención*.

### Cómo usar los PDF

- El **libro completo** (`Introduccion-a-las-Redes-de-Computadoras.pdf`) tiene
  portada, índice general e índice por clase. Es el que conviene para leer en la
  pantalla.
- Los **PDF individuales** sirven para imprimir o para repasar una clase suelta.
- Para **regenerarlos** después de editar cualquier `.md`:

```powershell
cd C:\Utu\utu\redescomp
python tools\build_pdf.py          # los 48 + el libro
python tools\build_pdf.py 27 29    # solo esas clases
python tools\qa.py                # auditoría de estructura y tamaño
python tools\verificar_diagramas.py  # que los diagramas ASCII sigan alineados
```

> ⚠️ **Nunca corras `tools/limpiar.py`.** El script de limpieza de caracteres
> de limpieza puede borrar identificadores dentro de los `backticks` de código y dejar
> huecos como *"funciona con , y como cualquier archivo"*. Para buscar caracteres
> raros usá `tools/revisar_raros.py`, que **solo informa** y no modifica nada.


## Estructura

```
redescomp/
├── README.md                    ← estás acá
├── PLAN-48-CLASES.md            el plan completo: 48 clases, bloques, cronograma
├── BANCO-EXAMENES.md            índice de los 50 exámenes por tema
├── ACTUALIZACIONES.md           qué cambió 2012→2026, con RFC verificados
├── GUIA-ESTILO.md               cómo está escrita cada clase
├── clases/                      las 48 clases, una por archivo .md
├── material-oficial/            los exámenes y prácticos descargados
│   ├── examenes/*.pdf           50 PDFs (letra + solución)
│   ├── examenes/txt/*.txt       el texto extraído, más fácil de buscar
│   └── practicos/               los 8 prácticos oficiales de 2008
├── pdf/                         los PDFs generados
└── tools/                       scripts de extracción, limpieza y compilación
```

## Las 48 clases

| Bloque | Clases | Contenido |
|---|---|---|
| **A. Fundamentos** | 1–7 | Redes, modelos OSI/TCP-IP, conmutación, retardo, Nyquist/Shannon |
| **B. Capa de aplicación** | 8–15 | HTTP, DNS, correo, DHCP, sockets, flujo de un web request |
| **C. Capa de transporte** | 16–23 | UDP, TCP (cabecera, handshake, fiabilidad, control de flujo y congestión) |
| **D. Capa de red** | 24–37 | IPv4, subnetting/VLSM, tablas de ruteo, ARP, NAT, DV, LS/OSPF, BGP, MTU, IPv6, ICMP |
| **E. Capa de enlace** | 38–43 | Framing, CRC/paridad/checksum, ARQ, acceso al medio, switch/VLAN, 802.11 |
| **F. Servicios y seguridad** | 44–48 | RTP/VoIP/jitter, QoS/MPLS, SNMP, criptografía, TLS/PGP/IDS, IP Móvil |

Cada clase tiene: **teoría con diagramas ASCII**, **⚠️ Actualización a 2026**,
**práctica resuelta con el razonamiento explícito**, **problemas reales de
examen de FING resueltos paso a paso**, **ejercicios extra inventados**, y cierre
con **resumen + autoevaluación con respuestas**.

## Formato del examen

- **3 horas**, individual, **sin material**.
- Aprobación con **60 de 100 puntos**.
- **Obligatorio acertar al menos 15 puntos en las preguntas teóricas.** Si no,
  no aprobás aunque sumes 60 con los problemas.
- Estructura desde 2008: **5 preguntas teóricas** (~40 pts) + **2 problemas
  prácticos** (~60 pts, 30 cada uno).

Los dos problemas prácticos son siempre de uno de estos dos tipos:

- **Tipo A — Programación en pseudocode.** Te dan primitivas y tipos ya
  definidos y te piden implementar funciones. No hay compilador: se evalúa que
  detectes los casos y tomes las decisiones correctas.
  *Ej: ECN + control de congestión (2011-03), Path MTU con ICMP (2010-12),
  `connectCheaper()` con sockets UDP (2010-12), VoIP con buffer de jitter
  (2011-02).*
- **Tipo B — Topología de red con números.** Te dan una figura con routers,
  subredes, direcciones IP y MAC, y te piden tablas de enrutamiento, ARP paso a
  paso, qué cambia con NAT, subdivisión de bloques de direcciones, y diagramas de
  tramas. *Ej: NAT + ARP + subredes (2011-03), subnetting + distance-vector +
  tunneling (2010-07), IP Móvil (2011-02).*

## Lo más importante que hay que saber

Conté cada tema en los 50 exámenes oficiales. Esto es lo que más se repite:

1. **TCP** — cabecera, handshake, números de secuencia, control de flujo y de
   congestión. Aparece en 14 exámenes.
2. **Subnetting y planes de numeración** — 11 exámenes.
3. **Programación en pseudocode** — 12 exámenes, y son 60 de los 100 puntos.
4. **ARP / NAT / Ethernet+IP+MAC** — 10 exámenes.
5. **Tablas de enrutamiento y next hop** — 8 exámenes.
6. **Enrutamiento DV / LS / OSPF / BGP / Dijkstra** — 10 exámenes.
7. **Acceso al medio, switch, hub** — 9 exámenes.
8. **Retardos, ancho de banda, RTT** — 9 exámenes.
9. **Seguridad** — 9 exámenes.
10. **Detección y corrección de errores (CRC, paridad, Hamming)** — 7 exámenes.

Y las tres clases donde más se concentran los 30 puntos: **clase 22** (taller
TCP, con el problema de 2011-03), **clase 29** (taller de subnetting) y
**clases 30-31** (tablas de ruteo, ARP y NAT, con el otro problema de 2011-03).

## Los videos de OpenFING

El curso de OpenFING que me pasaste tiene 3 clases de laboratorio. Los más útiles
para el temario están en los cursos hermanos:

| Curso | Qué hay |
|---|---|
| [`redes-2024`](https://open.fing.edu.uy/courses/redes-2024/) | 3 clases: los 2 obligatorios + enrutamiento dinámico |
| [`redes-2021`](https://open.fing.edu.uy/courses/redes-2021/) | **20 clases** teórico-prácticas: retardos, HTTP, DNS, sockets, transporte, TCP, capa de red, IPv4 |
| [`redes-2020`](https://open.fing.edu.uy/courses/redes-2020/) | **25 clases**: lo mismo más **algoritmos de enrutamiento**, OSPF, BGP, y ejemplo de conteo a infinito |
| [`redes`](https://open.fing.edu.uy/courses/redes/) | 23 clases teóricas de 2013, incluyendo IPv6 |

**Los más valiosos para vos** son las clases 18 y 20 de `redes-2020` (repaso de
algoritmos de enrutamiento) y la 15 de `redes-2021` (resolución de un ejercicio de
examen sobre TCP), porque muestran **cómo los profesores encaran los problemas**.

## Compilar los PDF

```powershell
python tools\build_pdf.py            # las 48 clases + el libro completo
python tools\build_pdf.py 21         # solo la clase 21
python tools\build_pdf.py 21-23      # clases 21 a 23
```

Salida en `pdf/`:
- `Redes-Computadoras-Clase-NN.pdf`, una por clase.
- `Introduccion-a-las-Redes-de-Computadoras.pdf`, el **libro completo** con
  portada e índice, para imprimir o leer offline.

Usa Chrome o Edge en modo headless, así que no necesita LaTeX ni nada extra.

## Otros scripts

```powershell
python tools\extract.py <carpeta-pdfs> <carpeta-salida>   # extrae texto de PDFs
python tools\limpiar.py .                                  # limpia artefactos de escritura
python tools\topng.py <pdfs> <salida> [zoom]               # rasteriza para revisión
```

## La bibliografía

- **Tanenbaum & Wetherall**, *Redes de computadoras*, **5ª edición** — es el PDF
  en `C:\Utu\utu\1406-Intro.Redes.Computadora\`. Es el libro de referencia del
  curso y cada clase apunta al capítulo correspondiente.
- El curso usaba además **Kurose & Ross**, *Computer Networking: A Top-Down
  Approach*, 4ª ed. Los **prácticos oficiales de 2008** (`material-oficial/practicos/`)
  son directamente ejercicios de ese libro: paridad, CRC, CDMA, eficiencia de
  ALOHA.
- **Comer**, *Internetworking with TCP/IP*; **Bertsekas & Gallager**, *Data
  Networks*; **Stallings**, *Data and Computer Communications*.

## Nota sobre las actualizaciones

`ACTUALIZACIONES.md` es la fuente de verdad de todas las columnas «⚠️
Actualización a 2026». **Todos los números de RFC fueron verificados** contra
`rfc-editor.org` y `datatracker.ietf.org` en octubre de 2026.

Si vas a citar un RFC en el examen y no está en ese documento, **verificalo**.
La sección §0 lista los 14 números que cambiaron y tres errores frecuentes
(`RFC 8951` NO es de ECN, `RFC 7560` NO es ECN++, y **no existe** un RFC que
depreque el half-duplex Ethernet — eso es IEEE 802.3).

Las cifras de despliegue (qué porcentaje usa HTTP/3, cuánta gente tiene IPv6)
**cambian mes a mes**. Si querés una cifra fresca, medila vos:
`radar.cloudflare.com`, `stats.google.com/ipv6/`, `w3techs.com`, `apnic.labs`.
