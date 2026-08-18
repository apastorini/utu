# INFRA-09 · Herramientas para Crear y Simular el Funcionamiento de una Red

> **Función del MCU 5.0:** Proveer un entorno controlado para practicar los controles de las funciones de protección y detección (PR y DE) antes de aplicarlos a la red real del banco, reduciendo el riesgo de error operativo.
> **ISO/IEC 27001:** Respalda los controles del Anexo A sobre adquisición, desarrollo y mantenimiento de sistemas (A.12), seguridad de las telecomunicaciones (A.13) y pruebas de seguridad, que requieren validar configuraciones en entornos aislados.
> **BCU:** Sustenta la capacitación técnica exigida por el RNRCSF (art. 492) y demuestra que el personal valida cambios de configuración en laboratorio antes de llevarlos a los sistemas de producción del banco.
> **URCDP:** El laboratorio permite probar medidas técnicas de seguridad (segmentación, firewall, registros) que la Ley 18.331 y el Decreto 64/020 exigen documentar para proteger datos personales.
> **Nivel del curso:** 🟢 Descubrir · 🟡 Practicar · 🔴 Dominar

---

## 1. Por qué simular una red

Simular una red significa **armar una copia de prueba** de la red del banco, pero en miniatura y sin conexión a los sistemas reales. Es como hacer un ensayo general antes del estreno: se prueban todas las escenas, se detectan los errores y nadie sale lastimado.

Para este curso, simular tiene cuatro ventajas concretas:

- **Aprender sin riesgo.** Podés apagar, borrar y volver a empezar mil veces. Un error en el laboratorio no genera un incidente en el banco.
- **Probar antes de aplicar.** Cualquier cambio de configuración (una regla de firewall, una VLAN, un parche) se valida primero en el simulador. Así el cambio que se aplica en producción llega probado.
- **Generar evidencia.** Las capturas de pantalla, los archivos de configuración exportados y los reportes de escaneo que se obtienen en el laboratorio sirven como evidencia para las plantillas del kit (ID-01, INFRA-03, DE-01, URCDP-01).
- **Explicar a otros.** Cuando tengas que explicarle a un auditor o a tu jefe por qué la red está segmentada, no alcanza con decirlo: alcanza con mostrar las pruebas que hiciste en el laboratorio.

### Qué es lo que NO hay que hacer jamás

- No simular con datos reales de clientes. El laboratorio se alimenta con datos de ejemplo.
- No conectar el laboratorio a la red de producción del banco.
- No usar el laboratorio como si fuera producción (sin respaldo, sin monitoreo, sin reglas).

---

## 2. Simulador, emulador y máquina virtual: tres palabras que conviene entender

Antes de la tabla comparativa, definimos tres términos que se confunden mucho:

| Término | Qué es | Ejemplo |
|---|---|---|
| **Simulador** | Programa que imita el comportamiento de una red con reglas propias, sin ejecutar el sistema operativo real del dispositivo. | Cisco Packet Tracer |
| **Emulador** | Programa que ejecuta el sistema operativo real del dispositivo (por ejemplo, una imagen de router Cisco IOS) sobre un entorno controlado. | GNS3, EVE-NG |
| **Máquina virtual (VM)** | Una computadora completa (sistema operativo y programas) que corre dentro de otra computadora, como un archivo. | VirtualBox, VMware Workstation Player |

Para este curso vas a usar **simuladores** para aprender los conceptos y **máquinas virtuales** para montar servicios reales (firewall pfSense, servidores Linux). El emulador profesional (GNS3, EVE-NG) queda como ampliación para quien quiera practicar con equipos de red reales del banco.

---

## 3. Comparativa de simuladores y emuladores de red

| Herramienta | Tipo | Licencia | Qué te permite hacer | Requisitos | Curva de aprendizaje |
|---|---|---|---|---|---|
| **Cisco Packet Tracer** | Simulador didáctico | Gratuito para educación (requiere registro) | Armar topologías con routers, switches, PCs y cables; aprender el lenguaje Cisco IOS | PC básica; 4 GB RAM | 🟢 Muy baja: ideal para empezar |
| **GNS3** | Emulador profesional | Gratuito (open source) | Ejecutar imágenes reales de IOS; integrar VirtualBox, VMware y QEMU para máquinas virtuales | 8–16 GB RAM; CPU con virtualización | 🟡 Media |
| **EVE-NG** (Community Edition) | Emulador web profesional | Gratuito en su edición comunitaria | Subir routers reales, firewalls y VMs; acceso por navegador | 16 GB RAM recomendado; servidor o PC potente | 🟡 Media-alta |
| **VirtualBox** | Hipervisor (máquinas virtuales) | Gratuito (open source) | Correr servidores y clientes completos (Linux, Windows) | 8 GB RAM recomendado | 🟢 Baja |
| **VMware Workstation Player** | Hipervisor (máquinas virtuales) | Gratuito para uso personal | Lo mismo que VirtualBox, con interfaz similar | 8 GB RAM recomendado | 🟢 Baja |
| **pfSense / OPNsense** | Firewall/router real instalable en VM | Gratuito (open source) | Simular la DMZ, reglas de firewall y VPN con un producto de nivel real | 2 GB RAM por VM | 🟡 Media |
| **Ubuntu Server / CentOS con isc-dhcp-server y bind9, o dnsmasq** | Sistema operativo de servidor | Gratuito | Simular servicios DHCP, DNS y DNS-respaldados | 1–2 GB RAM por VM | 🟡 Media |
| **Wireshark** | Analizador de tráfico | Gratuito (open source) | Capturar y examinar paquetes de la red simulada | PC básica | 🟡 Media |
| **Nmap / Zenmap** | Escáner de red | Gratuito (open source) | Descubrir dispositivos y puertos abiertos en la red simulada | PC básica | 🟢 Baja |
| **Gophish** | Plataforma de phishing | Gratuito (open source) | Simular campañas de phishing para concientización (PR-02) | 2 GB RAM por VM | 🟡 Media |
| **Metasploit Framework / Kali Linux** | Suite de pruebas de penetración | Gratuito (open source) | Probar vulnerabilidades de forma controlada (solo en laboratorio) | 2 GB RAM por VM | 🔴 Alta |
| **Visio / draw.io** | Diagramador | Visio comercial; draw.io gratuito | Dibujar el mapa de red y las zonas | PC básica | 🟢 Baja |

> **Regla de oro:** el laboratorio se usa para probar y para aprender. Las herramientas de ataque (Metasploit, Kali) solo se ejecutan dentro del entorno aislado del laboratorio, nunca contra sistemas reales.

---

## 4. Qué necesitás para correr cada herramienta

El requisito más importante es la **memoria RAM**, porque cada máquina virtual consume memoria propia. Una PC de oficina estándar sirve para la fase didáctica; la fase de laboratorio con varias máquinas virtuales pide más recursos.

| Herramienta | RAM mínima | Disco | Observaciones |
|---|---|---|---|
| Packet Tracer | 4 GB (total del equipo) | 500 MB libres | Corre en casi cualquier PC |
| VirtualBox + pfSense | 8 GB (total del equipo) | 20 GB libres | La VM de pfSense usa 2 GB |
| VirtualBox + 2 o 3 VMs simultáneas | 16 GB (total del equipo) | 60 GB libres | El laboratorio completo del INFRA-10 |
| GNS3 con varias VMs | 16 GB (recomendado) | 80 GB libres | Usa imágenes de IOS |
| EVE-NG | 16 GB o más | 100 GB libres | Ideal en un servidor dedicado |
| Wireshark, Nmap | 4 GB (total del equipo) | 500 MB libres | Se instalan en el host o en una VM |

**Si tu equipo no llega a los 16 GB:** hacé el laboratorio con solo dos VM (pfSense + un cliente) y usá Packet Tracer para el resto. Los conceptos se aprenden igual; las pruebas se adaptan.

---

## 5. La combinación recomendada para este curso

Para no instalar todo de una vez (eso abruma), el curso propone esta combinación en dos fases:

### Fase 1 · Didáctica (con Packet Tracer)

- Objetivo: entender topologías, direcciones IP, subredes y segmentación sin instalar nada pesado.
- Duración sugerida: los módulos INFRA-01 a INFRA-07.
- Resultado: poder dibujar y probar una red de banco en miniatura con routers y switches.

### Fase 2 · Laboratorio real (con VirtualBox + pfSense)

- Objetivo: montar una mini-red funcional con firewall real, DMZ, servidores y cliente, y probar reglas de verdad (módulo INFRA-10).
- Herramientas: VirtualBox, ISO de pfSense, ISO de Linux (Ubuntu Server o Debian), un cliente Windows o Linux, Wireshark y Nmap en el cliente.
- Resultado: evidencia concreta (capturas, reglas, reportes) para completar INFRA-08, ID-01 y URCDP-01.

### Ampliación (solo para quien quiera llegar al nivel 🔴)

- GNS3 o EVE-NG para emular equipos Cisco con imágenes reales.
- Kali Linux para ejercicios controlados de ataque-defensa dentro del laboratorio.
- Gophish para simular campañas de phishing del programa PR-02.

---

## 6. Instalación básica de las herramientas recomendadas (Windows)

Pasos resumidos. Los nombres de dominio oficiales conocidos son `virtualbox.org`, `pfsense.org`, `nmap.org` y `wireshark.org`; siempre descargá desde el sitio oficial y verificá el checksum cuando sea posible.

### 6.1 VirtualBox

1. Entrá al sitio oficial de VirtualBox y descargá el instalador de Windows.
2. Ejecutá el instalador y aceptá los valores por defecto (reiniciá si lo pide).
3. Verificá la instalación abriendo "Oracle VM VirtualBox".
4. Opcional: instalá el paquete "Extension Pack" del mismo sitio (agrega soporte USB y red).

### 6.2 pfSense (ISO)

1. Descargá la ISO instalable de pfSense desde el sitio oficial.
2. En VirtualBox, creá una nueva VM (ver paso a paso en INFRA-10).
3. Montá la ISO como disco óptico e instalá pfSense siguiendo el asistente.
4. Configurá la primera interfaz como WAN y la segunda como LAN.

### 6.3 Servidor Linux (Ubuntu Server)

1. Descargá la ISO de Ubuntu Server (o Debian) desde el sitio oficial.
2. Creá la VM en VirtualBox con 1–2 GB de RAM.
3. Durante la instalación, elegí la opción de servidor (sin escritorio) y dejá activado el servidor SSH.

### 6.4 Wireshark y Nmap

1. Descargá e instalá Wireshark desde `wireshark.org`.
2. Durante la instalación, marcá la opción de instalar Npcap (permite capturar paquetes).
3. Descargá e instalá Nmap desde `nmap.org` (Zenmap es la interfaz gráfica opcional).

### 6.5 draw.io

1. Es una aplicación web; entrás al sitio oficial o descargás la versión de escritorio.
2. Usá la plantilla de "Network" para dibujar el diagrama del laboratorio.

> **Consejo:** anotá la versión instalada de cada herramienta. La versión es un dato que después pedirá el inventario ID-01 y el reporte de parches PR-06.

---

## 7. Tabla de mapeo: herramienta → prueba → evidencia → plantilla del kit

Esta tabla es el puente entre "instalé una herramienta" y "completé un documento del kit". Cada herramienta produce evidencia que alimenta una plantilla.

| Herramienta | Qué te permite probar | Qué evidencia podés exportar | Plantilla / módulo del kit relacionado |
|---|---|---|---|
| Packet Tracer | Topologías, subredes, segmentación didáctica | Captura de pantalla del diagrama y de pings | INFRA-03, INFRA-04, GV-02 |
| VirtualBox | Máquinas virtuales aisladas | Captura de la lista de VMs y de las redes internas | ID-01, ID-05 |
| pfSense | Firewall, DMZ, DHCP, reglas, VPN | Export de configuración XML, salida de `pfctl -sr`, capturas de reglas | INFRA-03, ID-01, PR-06, DE-01 |
| Ubuntu Server + dnsmasq | Servicios DHCP y DNS simulados | Captura de configuración (`/etc/dnsmasq.conf`) y de consultas | INFRA-05, ID-01, DE-01 |
| Wireshark | Tráfico de red real, paquetes | Archivo de captura **.pcap** con fecha y filtro aplicado | DE-01, DE-02, INFRA-08 |
| Nmap / Zenmap | Puertos abiertos, dispositivos vivos | Reporte en texto, XML o HTML del escaneo | ID-03, ID-04, INFRA-09 |
| Gophish | Campañas de concientización | Reporte de la campaña con resultados | PR-02 |
| Kali / Metasploit | Vulnerabilidades controladas | Reporte de explotación y capturas de sesión | ID-04, RS-02, RS-03 |
| draw.io / Visio | Documentación del diseño de red | Archivo del diagrama y export a PDF/PNG | GV-02, ID-01, INFRA-03 |

**Regla de la evidencia:** toda captura debe tener fecha visible (de la computadora o anotada en el nombre del archivo). Sin fecha, para un auditor no existe.

---

## 8. Seguridad del laboratorio

El laboratorio es una herramienta de aprendizaje, pero también es una red con servicios corriendo. Para que sea seguro por diseño:

- **Aislarlo de la red real del banco.** Usá "Red interna" o "Host-only" en VirtualBox. Nunca "Puente" (bridged) hacia la red corporativa.
- **No conectar a producción.** El laboratorio no comparte cable ni Wi-Fi con los sistemas del banco.
- **No usar datos reales de clientes.** Todo dato en el laboratorio es ficticio: clientes de ejemplo, cuentas de ejemplo, contraseñas de ejemplo.
- **Restringir el acceso.** Solo el personal autorizado puede usar las VMs del laboratorio.
- **Reiniciar a estado limpio.** Si una VM se compromete durante un ejercicio de ataque, se restaura desde una copia de seguridad (snapshot) y se sigue adelante.
- **Documentar.** El diagrama del laboratorio y sus IPs se guardan como parte de ID-01 y GV-02.

---

## 9. Cierre del módulo

En este módulo viste por qué simular, qué herramientas existen, cuáles necesitás y cómo se conecta cada una con la evidencia del kit. Ahora tenés el mapa de herramientas. El siguiente paso es el módulo **INFRA-10 · Laboratorio Paso a Paso**, donde vas a construir la mini-red del banco y a probarla con tus propias manos.

### Checklist del módulo

- ☐ Entiendo la diferencia entre simulador, emulador y máquina virtual.
- ☐ Elegí la combinación de herramientas para mi equipo (Packet Tracer y/o VirtualBox).
- ☐ Verifiqué que mi equipo tiene la RAM suficiente (8 GB para lo básico, 16 GB para el laboratorio completo).
- ☐ Instalé al menos VirtualBox y descargué las ISOs de pfSense y Linux.
- ☐ Sé qué evidencia produce cada herramienta y dónde la guardo.
- ☐ Confirmé que el laboratorio quedará aislado de la red real del banco.

---

**Documentos relacionados:** GV-01, GV-02, GV-03, GV-04, GV-06, ID-01, ID-02, ID-03, ID-04, ID-05, PR-01, PR-02, PR-03, PR-04, PR-05, PR-06, PR-07, PR-08, DE-01, DE-02, DE-03, RS-01, RS-02, RS-03, RC-01, RC-02, RC-03, RC-04, BCU-01, BCU-02, BCU-03, BCU-04, BCU-05, BCU-06, URCDP-01, URCDP-02, URCDP-03, URCDP-04, URCDP-05, URCDP-06, MATRIZ-001 · Referencias internas: INFRA-01, INFRA-02, INFRA-03, INFRA-04, INFRA-05, INFRA-06, INFRA-07, INFRA-08, INFRA-09, INFRA-10
