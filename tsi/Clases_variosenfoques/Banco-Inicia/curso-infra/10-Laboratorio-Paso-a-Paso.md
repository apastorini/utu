# INFRA-10 · Laboratorio Paso a Paso: Crear, Probar y Explicar un Entorno Simulado

> **Función del MCU 5.0:** Convertir la teoría de las funciones de protección y detección (PR y DE) en práctica: el alumno construye un entorno segmentado, aplica reglas de firewall y captura evidencia de su funcionamiento.
> **ISO/IEC 27001:** Demuestra controles del Anexo A aplicados en la práctica: seguridad de redes (A.13), gestión de vulnerabilidades (A.12.6) y registros de actividad (A.12.4), todos probados en un entorno controlado.
> **BCU:** Prepara la evidencia técnica que exige el RNRCSF (art. 492): segmentación, reglas de firewall documentadas y registros de actividad verificables ante el regulador.
> **URCDP:** Las medidas lógicas y físicas que se prueban en el laboratorio (segmentación, DMZ, firewall, logs) son las que se declaran en el Documento de Seguridad de Datos Personales (URCDP-01).
> **Nivel del curso:** 🟢 Descubrir · 🟡 Practicar · 🔴 Dominar

---

## 1. Objetivo del laboratorio

Este es el módulo "taller" del curso: acá se hace, no se lee. Al terminar, vas a haber construido una **mini-red de banco** con:

- Una **zona interna** donde vive un servidor de datos "interno" (el tesoro del banco).
- Una **DMZ** donde vive un servidor web "público" (el sitio que cualquiera puede visitar).
- Un **Internet simulada** (una red externa de prueba).
- Un **firewall pfSense** que separa las tres redes.
- Un **cliente** que navega, hace pings y escanea con Nmap.
- **Wireshark** para ver qué pasa dentro de los paquetes.

El laboratorio se considera **aprobado** cuando puedas demostrar con evidencia que:

1. El servidor web de la DMZ responde desde Internet simulada.
2. El servidor interno **NO** es alcanzable desde la DMZ (la segmentación funciona).
3. El cliente interno navega hacia Internet simulada.
4. Todas las pruebas quedaron registradas con fecha en el expediente de evidencias.

---

## 2. Paso 0 · Requisitos y descargas

Necesitás una computadora con al menos **8 GB de RAM** (16 GB recomendados) y unos 40 GB de disco libre. Descargá con anticipación, siempre desde los sitios oficiales:

| Elemento | De dónde se obtiene (sitio oficial) | Para qué |
|---|---|---|
| VirtualBox | `virtualbox.org` | Ejecutar las máquinas virtuales |
| ISO de pfSense (instalable) | `pfsense.org` | El firewall del laboratorio |
| ISO de Ubuntu Server (o Debian) | sitio oficial del sistema | Servidor de datos interno |
| ISO de Linux Mint (o Xubuntu) | sitio oficial de la distribución | El cliente con escritorio |
| Wireshark (instalador) | `wireshark.org` | Capturar y analizar paquetes |
| Nmap (Zenmap) | `nmap.org` | Escanear puertos y descubrir dispositivos |

### Lista de verificación antes de empezar

- ☐ Instalé VirtualBox y verifiqué que abre correctamente.
- ☐ Descargué las ISO de pfSense, Ubuntu Server y Linux Mint.
- ☐ Confirmé la RAM disponible de mi equipo (mínimo 8 GB).
- ☐ Tomé nota de la versión de cada software descargado (para ID-01 y PR-06).

---

## 3. Paso 1 · Diseño del laboratorio

### 3.1 El diagrama mental

```
                       [ Internet simulada ]
                       192.168.1.0/24
                               |
                               |  (WAN)
                    [ pfSense firewall ]
                     /                 \
              (LAN)                     (OPT / DMZ)
                 |                           |
        [ Zona interna ]              [ DMZ ]
        10.10.10.0/24                10.10.20.0/24
         - servidor datos            - servidor web
         - cliente interno
```

### 3.2 Tabla de redes

| Red | Dirección | Máscara | Función | Zona |
|---|---|---|---|---|
| Red interna | 10.10.10.0 | /24 (255.255.255.0) | Datos internos del banco (ficticios) | LAN |
| DMZ | 10.10.20.0 | /24 (255.255.255.0) | Servidores expuestos: web de prueba | DMZ |
| Internet simulada | 192.168.1.0 | /24 (255.255.255.0) | Mundo exterior simulado | WAN |

### 3.3 Tabla de IPs de cada máquina

| Máquina | Interfaz / Red | Dirección IP | Puerta de enlace | DNS |
|---|---|---|---|---|
| pfSense | WAN | 192.168.1.254 | 192.168.1.1 (router simulado, opcional) | 8.8.8.8 (simulado) |
| pfSense | LAN | 10.10.10.254 | — | — |
| pfSense | OPT (DMZ) | 10.10.20.254 | — | — |
| Cliente interno | LAN | 10.10.10.10 (DHCP) | 10.10.10.254 | 10.10.10.254 |
| Servidor de datos | LAN | 10.10.10.20 (fija) | 10.10.10.254 | 10.10.10.254 |
| Servidor web | DMZ | 10.10.20.10 (fija) | 10.10.20.254 | 10.10.10.254 |

> **Recordá:** todas estas IPs y datos son **ficticios**. En el laboratorio no se usa ninguna IP ni dato real del banco.

---

## 4. Paso 2 · Crear las máquinas virtuales en VirtualBox

### 4.1 Crear una máquina virtual nueva

1. Abrí VirtualBox y pulsá **Nueva**.
2. Nombre: usá un nombre claro y uniforme, por ejemplo `LAB-FW-pfSense`, `LAB-SRV-Datos`, `LAB-WEB-DMZ`, `LAB-Cliente`.
3. Tipo y versión: según el sistema operativo que vayas a instalar.
4. Memoria: pfSense 2 GB; Ubuntu Server 2 GB; cliente 2 GB.
5. Disco: creá un disco virtual de al menos 20 GB por máquina (dinámico).

### 4.2 Configurar la red de cada VM

En **Configuración → Red**, elegí el adaptador correcto. La red interna y la red host-only son claves para el aislamiento:

| VM | Adaptador 1 | Adaptador 2 |
|---|---|---|
| pfSense | Red interna `labWAN` | Red interna `labLAN` |
| pfSense (adaptador 3) | — | Red interna `labDMZ` (se agrega en el Paso 4) |
| Servidor de datos | Red interna `labLAN` | — |
| Servidor web | Red interna `labDMZ` | — |
| Cliente | Red interna `labLAN` | — |

> **Regla del laboratorio:** todas las VM usan **Red interna**, nunca "Puente" ni "Red NAT", para que el laboratorio quede aislado de la red real del banco.

### 4.3 Instalar los sistemas operativos

1. Montá la ISO en **Configuración → Almacenamiento**.
2. Iniciá la VM y seguí el asistente de instalación.
3. Para los servidores Linux, activá el **OpenSSH server** durante la instalación (te permite conectarte en modo texto).
4. Al terminar, actualizá el sistema operativo de cada VM (**apt update && apt upgrade**) y anotá la versión. Ese dato alimenta PR-06.

---

## 5. Paso 3 · Instalar y configurar pfSense

1. Iniciá la VM de pfSense con la ISO montada.
2. Aceptá el asistente de instalación y elegí la partición automática (la VM es nueva, no hay nada que preservar).
3. Al reiniciar, pfSense pregunta qué interfaz es WAN y cuál LAN:
   - El adaptador conectado a `labWAN` → **WAN** (192.168.1.254).
   - El adaptador conectado a `labLAN` → **LAN** (10.10.10.254).
   - Las que no uses: **ninguna**.
4. Asigná las direcciones IP en el asistente de consola (opt para "editar manualmente"):
   - WAN: IP estática 192.168.1.254 / 24.
   - LAN: IP estática 10.10.10.254 / 24.
5. Configurá el DNS en pfSense: usá el propio LAN y un resolver de ejemplo (la IP de WAN del gateway simulado). En un laboratorio aislado no hay DNS real: dnsmasq del Paso 5 lo resolverá.
6. Accedé a la interfaz web desde el cliente: escribí `https://10.10.10.254` en el navegador del cliente.
7. Completá el asistente inicial:
   - Hostname: `lab-fw`.
   - DNS servers: la dirección del gateway simulado.
   - **Habilitá DHCP en la LAN** con rango `10.10.10.100` a `10.10.10.200`.
8. Cambiá la contraseña de administrador y guardala en un gestor de contraseñas del laboratorio.

---

## 6. Paso 4 · Configurar la DMZ en pfSense

1. Agregá un **segundo adaptador** a la VM de pfSense en VirtualBox (Red interna `labDMZ`) y reiniciá la VM.
2. En la consola de pfSense, entrá a **Assign Interfaces** y asigná el nuevo adaptador como **OPT1**.
3. En la interfaz web: **Interfaces → OPT1**, marcá "Enable" y asigná IP estática `10.10.20.254/24`.
4. Habilitá también la opción de bloquear tráfico privado si está disponible (protección extra del laboratorio).
5. Creá una regla de **antilockout** si la red interna no está accesible: la regla por defecto para acceso web ya existe en LAN.
6. Aplicá los cambios. La DMZ queda lista para recibir el servidor web del Paso 5.

---

## 7. Paso 5 · Crear los servidores de prueba

### 7.1 Servidor web en la DMZ (Apache o nginx)

En la VM `LAB-WEB-DMZ` (IP fija 10.10.20.10):

1. Instalá nginx: `sudo apt install nginx` (o Apache2: `sudo apt install apache2`).
2. Verificá que el servicio esté activo: `sudo systemctl status nginx`.
3. Creá una página de prueba: editá `/var/www/html/index.html` y escribí `Laboratorio Banco-Inicia - Servidor web DMZ (fecha)`.
4. Probalo localmente: `curl http://localhost`.

### 7.2 Servidor de "datos" en la red interna

En la VM `LAB-SRV-Datos` (IP fija 10.10.10.20):

1. Instalá un servicio de ejemplo, por ejemplo SSH: `sudo apt install openssh-server`.
2. Creá un archivo de prueba de "datos del banco" (ficticios): `echo "DATOS DE PRUEBA - NO REALES" > /home/.../datos.txt`.
3. Anotá la IP y el servicio; este servidor será el que NO debe ser alcanzable desde la DMZ.

### 7.3 Servicio DNS/DHCP opcional (dnsmasq)

En el servidor de datos o en una VM aparte:

1. Instalá `dnsmasq`.
2. Configurá dominios de prueba: `address=/lab.test/10.10.20.10`.
3. Reiniciá el servicio. Esto demuestra DNS funcional en el laboratorio (concepto del INFRA-05).

---

## 8. Paso 6 · Escribir las reglas de firewall en pfSense

En **Firewall → Rules**, creá estas reglas y documentalas. Cada regla lleva una justificación (por qué existe).

| Nº | Interfaz | Origen | Destino | Puerto | Acción | Justificación |
|---|---|---|---|---|---|---|
| R1 | WAN (Internet simulada) | 192.168.1.0/24 | 10.10.20.10 (DMZ) | 443, 80 (TCP) | Permitir | El sitio web público debe ser accesible desde Internet simulada |
| R2 | WAN (Internet simulada) | cualquiera | resto | cualquiera | Denegar | Todo lo demás del exterior queda bloqueado |
| R3 | OPT1 (DMZ) | 10.10.20.0/24 | 10.10.10.0/24 (LAN) | cualquiera | Denegar | La DMZ jamás accede a la red interna (protección de datos) |
| R4 | OPT1 (DMZ) | 10.10.20.0/24 | Internet simulada (WAN) | 80, 443 | Permitir | El servidor web puede salir a actualizarse/consultar servicios |
| R5 | LAN (interna) | 10.10.10.0/24 | Internet simulada (WAN) | cualquiera | Permitir | El cliente interno navega y el servidor de datos opera |
| R6 | LAN (interna) | 10.10.10.0/24 | 10.10.20.0/24 (DMZ) | 80, 443 | Permitir | El personal interno consulta el sitio web interno vía DMZ |
| R7 | Cualquier interfaz | resto | resto | cualquiera | Denegar | Regla por defecto: lo que no está permitido, está prohibido |

> **Regla de seguridad del laboratorio:** pfSense aplica la regla **implícita de denegar** todo lo que no tenga una regla explícita de permitir. Eso es exactamente lo que hace un firewall de verdad.

Después de aplicar las reglas, obtené la evidencia de reglas activas:

```
pfctl -sr
```

Guardá la salida completa en el expediente de evidencias (Paso 9). Esta salida demuestra el control de firewall ante un auditor.

---

## 9. Paso 7 · Probar desde el cliente

Desde el cliente interno (`LAB-Cliente`), con las herramientas instaladas (Nmap, Wireshark):

### Prueba A · El web server de la DMZ responde

1. Abrí el navegador y entrá a `http://10.10.20.10`. Debe mostrar la página del laboratorio.
2. Verificá por línea de comandos: `curl -I http://10.10.20.10` (esperás respuesta HTTP 200 OK).
3. Capturá la pantalla con la hora visible.

### Prueba B · El servidor interno NO es alcanzable desde la DMZ

Esta prueba se hace desde un equipo de la DMZ. Si no tenés un equipo DMZ aparte, usá el propio servidor web:

1. Desde el servidor web (10.10.20.10) intentá: `ping 10.10.10.20`.
2. Esperá **timeout** (no debe responder).
3. Intentá conectarte por SSH: `ssh usuario@10.10.10.20` → debe fallar.
4. Capturá la salida: demuestra que la regla R3 funciona y que la DMZ no toca los datos internos.

### Prueba C · El cliente interno navega

1. Desde el cliente (10.10.10.10) ejecutá: `ping 192.168.1.254` (el WAN del firewall, simula llegar al exterior).
2. Abrí en el navegador del cliente el sitio web de la DMZ (vía regla R6).
3. Capturá ambas salidas.

### Prueba D · Descubrimiento con Nmap

1. Escaneá la DMZ desde el cliente: `nmap -sP 10.10.20.0/24` (descubre qué está vivo).
2. Escaneá puertos del web server: `nmap -sS 10.10.20.10`.
3. Guardá el reporte (Zenmap permite exportar en HTML/XML). Este reporte alimenta ID-03 e ID-04.

---

## 10. Paso 8 · Ver con Wireshark qué pasa

1. En el cliente, abrí Wireshark y seleccioná la interfaz de red interna.
2. Desde otro terminal, hacé un ping al servidor web: `ping 10.10.20.10`.
3. En Wireshark, usá el filtro `icmp` para ver los paquetes del ping.
4. Ahora abrí el sitio web en el navegador y usá el filtro `http` (o `tcp.port == 80`) para ver la comunicación.
5. Explicá qué ves:
   - **ICMP Echo Request / Echo Reply**: el ping de ida y vuelta (cliente → web → cliente).
   - **TCP three-way handshake**: SYN, SYN-ACK, ACK cuando el navegador inicia la conexión.
   - **HTTP GET / 200 OK**: el navegador pide la página y el servidor la entrega.
6. Guardá la captura como archivo **.pcap** con nombre fechado, por ejemplo `cap-2026-08-05-ping-web.pcap`.

> **Para el auditor:** el pcap con fecha y el filtro aplicado demuestran que se monitorea el tráfico (DE-01) y que se puede reconstruir una conversación completa (DE-02).

---

## 11. Paso 9 · Registrar TODO como evidencia

Toda evidencia se guarda en el **expediente de evidencias** del módulo INFRA-08. Convención de nombres: `fecha-actividad-tipo` (por ejemplo, `2026-08-05-reglas-pfSense.txt`).

| Evidencia | Cómo se obtiene | Formato sugerido |
|---|---|---|
| Diagrama del laboratorio | draw.io o Visio | PNG/PDF |
| Salida de `pfctl -sr` | consola del firewall | TXT |
| Salida de `ipconfig` / `ifconfig` de cada VM | consola de cada VM | TXT |
| Resultados de Nmap | Zenmap → export | HTML/XML/TXT |
| Captura de la página web de la DMZ | captura de pantalla | PNG |
| Prueba de que la DMZ no alcanza interna | captura del timeout | PNG/TXT |
| Captura de Wireshark | Wireshark → guardar como | PCAP |
| Fecha y versión de cada software | registro manual | TXT (para ID-01, PR-06) |

Cada evidencia lleva: **fecha, quién la generó, qué prueba demuestra y a qué regla o red corresponde**.

---

## 12. Paso 10 · Ejercicios adicionales opcionales (nivel 🔴)

Cuando el laboratorio básico funcione, ampliá con estos ejercicios:

- **Servidor DHCP/DNS propio:** reemplazá el DHCP de pfSense por `dnsmasq` y verificá que el cliente obtiene IP del servidor propio (INFRA-05).
- **VPN site-to-site:** cloná el pfSense, creá un segundo laboratorio y configurá una VPN entre ambos (INFRA-07). Probá que una red alcanza a la otra solo a través del túnel.
- **Ataque controlado (SSH bruteforce):** con una VM Kali en el laboratorio, probá un ataque de fuerza bruta contra el servidor de datos usando **solo IPs ficticias**. Verificá que las conexiones fallidas quedan en los logs (`/var/log/auth.log`) y que la alerta aparece. Esto entrena RS-02 y RS-03.
- **Gophish:** montá Gophish y enviá una campaña de phishing de prueba a buzones ficticios del laboratorio (PR-02).
- **IDS/IPS de prueba:** instalá Suricata o Snort en el pfSense y observá cómo se registra el tráfico sospechoso (INFRA-08).

> **Advertencia:** todo ejercicio de ataque se hace únicamente contra las VM del laboratorio, nunca contra equipos reales. Las herramientas de ataque no se instalan en el equipo de trabajo.

---

## 13. Explicá lo que pasa (para tu jefe o un auditor)

Este laboratorio no es solo "hacer clic": es aprender a explicar. Estas son las respuestas tipo para las preguntas que te van a hacer:

- **¿Qué hace el firewall?** Es la puerta con reglas. Separa tres mundos (Internet, DMZ, interna) y solo deja pasar el tráfico que está permitido. Todo lo demás, bloqueado (regla R7).
- **¿Por qué la DMZ no llega a la red interna?** Porque la regla R3 lo prohíbe. Aunque un atacante comprometa el servidor web, no puede saltar a la zona donde están los datos. Esa es la base de la segmentación.
- **¿Qué evidencia demuestra cada cosa?** El `pfctl -sr` muestra las reglas cargadas; el ping con timeout muestra que DMZ → interna está bloqueado; el reporte de Nmap muestra los puertos abiertos; el pcap muestra el tráfico real.
- **¿Y los datos personales?** El laboratorio no usa datos reales, pero el diseño (DMZ separada, firewall, logs) es el mismo diseño que protege los datos reales en el banco. Por eso este ejercicio alimenta URCDP-01: demuestra que las medidas lógicas existen y se prueban.

---

## 14. Errores comunes del laboratorio

| Error | Síntoma | Cómo evitarlo |
|---|---|---|
| Interfaces mal asignadas en pfSense | El firewall no responde en la IP esperada | Asigná interfaces una por una y anotá qué adaptador es qué |
| Firewall bloqueando todo | El cliente no navega ni hace ping | Revisá las reglas R1 a R7: si no hay regla de permitir, se bloquea |
| DHCP en la red equivocada | El cliente recibe una IP fuera de su rango | Verificá en Interfaces → LAN que DHCP esté habilitado en 10.10.10.0/24 |
| Olvidar reglas de salida | El web server no puede salir a Internet simulada | Sin regla de salida en DMZ (R4), las conexiones de salida se cortan |
| Capturas sin fecha | Evidencia inválida para auditoría | Nombre de archivo con fecha: `2026-08-05-...` |
| Conectar por "Puente" (bridged) | El laboratorio aparece en la red real del banco | Usar siempre **Red interna** o host-only |
| Usar datos reales de clientes | Incumplimiento de la Ley 18.331 | Todo dato del laboratorio es ficticio |

---

## 15. Cómo este laboratorio te entrena para llenar las plantillas

| Plantilla | Qué aprendiste en el laboratorio |
|---|---|
| ID-01 (Inventario de activos) | Registrar cada VM con su IP, red, sistema operativo, versión y responsable |
| ID-03 (Riesgos) | Los resultados de Nmap muestran puertos y servicios que son fuentes de riesgo |
| PR-06 (Parches) | El registro de versiones y actualizaciones de cada VM es el reporte de parches |
| DE-01 (Logs) | Los logs de pfSense, de `/var/log/auth.log` y los pcaps son registros de actividad |
| URCDP-01 (Medidas de seguridad) | Segmentación, DMZ y firewall son medidas lógicas que se declaran en el Documento de Seguridad |
| BCU-05 (Auditorías) | Poder explicar la segmentación con evidencia es exactamente lo que un auditor pide |

---

## 16. Cierre del módulo

Construiste una red completa en miniatura, la probaste, capturaste evidencia y aprendiste a explicarla. Ese es el nivel 🔴 de este curso: no solo saber qué es una DMZ, sino poder demostrar que la DMZ funciona y por qué. El siguiente módulo, **INFRA-11 · Correspondencia Normativa**, te enseña a volcar toda esta evidencia en los documentos del kit (URCDP-01, ID-01, PR-06) y a presentarla ante URCDP, BCU y Agesic.

### Checklist final del laboratorio

- ☐ Construí las 3 redes (interna, DMZ, Internet simulada) en VirtualBox.
- ☐ Configuré pfSense con WAN, LAN y OPT (DMZ).
- ☐ Instalé el web server en la DMZ y el servidor de datos en la interna.
- ☐ Documenté las reglas R1 a R7 en una tabla.
- ☐ Las 4 pruebas (A, B, C, D) pasaron y quedaron capturadas.
- ☐ Guardé todas las evidencias con fecha en el expediente (INFRA-08).
- ☐ Puedo explicar qué hace el firewall, por qué la DMZ no llega a la interna y qué evidencia lo demuestra.

---

**Documentos relacionados:** GV-01, GV-02, GV-03, GV-04, GV-06, ID-01, ID-02, ID-03, ID-04, ID-05, PR-01, PR-02, PR-03, PR-04, PR-05, PR-06, PR-07, PR-08, DE-01, DE-02, DE-03, RS-01, RS-02, RS-03, RC-01, RC-02, RC-03, RC-04, BCU-01, BCU-02, BCU-03, BCU-04, BCU-05, BCU-06, URCDP-01, URCDP-02, URCDP-03, URCDP-04, URCDP-05, URCDP-06, MATRIZ-001 · Referencias internas: INFRA-01, INFRA-02, INFRA-03, INFRA-04, INFRA-05, INFRA-06, INFRA-07, INFRA-08, INFRA-09, INFRA-10
