# CLASE DE REPASO: Fundamentos de Linux para Pentesting y Conceptos de Redes

---

## OBJETIVOS DE LA CLASE

Al finalizar esta clase, el estudiante será capaz de:

```
┌─────────────────────────────────────────────────────────────────┐
│                    OBJETIVOS DE APRENDIZAJE                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  CONOCIMIENTO                                                   │
│  ────────────                                                   │
│  □ Comprender el modelo OSI y TCP/IP                           │
│  □ Conocer los puertos y servicios más comunes                   │
│  □ Entender qué son CVE y CWE                                  │
│  □ Identificar vulnerabilidades por versiones de servicios       │
│  □ Comprender cómo funciona la comunicación en red              │
│                                                                 │
│  HABILIDADES                                                    │
│  ──────────                                                     │
│  □ Interpretar la salida de comandos de red (ifconfig, ip, etc) │
│  □ Usar comandos de Linux para diagnóstico de red               │
│  □ Ejecutar escaneos básicos con Nmap                          │
│  □ Analizar tablas de enrutamiento                              │
│  □ Comprender la resolución DNS                                 │
│                                                                 │
│  APLICACIÓN                                                    │
│  ──────────                                                     │
│  □ Configurar interfaces de red                                 │
│  □ Diagnosticar problemas de conectividad                      │
│  □ Identificar servicios expuestos en un sistema                 │
│  □ Preparar el entorno para pentesting                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## TABLA DE CONTENIDOS

1. Conceptos Fundamentales de Redes
2. Modelo OSI y TCP/IP
3. Puertos y Servicios
4. Vulnerabilidades Conocidas: CVE y CWE
5. Anatomía de la Comunicación en Red
6. Interfaces de Red y Direcciones
7. Comandos de Linux para Redes
8. Nmap: Guía Completa de Parámetros

---

## 1. CONCEPTOS FUNDAMENTALES DE REDES

### 1.1. ¿Qué es una Red de Computadoras?

Una **red de computadoras** es un conjunto de dispositivos electrónicos (computadoras, servidores, impresoras, móviles, etc.) interconectados que pueden comunicarse entre sí para compartir recursos, información y servicios.

**Analogía sencilla:**
Piensa en una red como el sistema de correo postal. Cada casa tiene una dirección única (dirección IP), existe un sistema de buzones y oficinas de correo (protocolos), y las cartas pueden viajar por diferentes rutas (enrutamiento) para llegar a su destino.

### 1.2. Tipos de Redes por Extensión

| Tipo de Red | Alcance | Ejemplos de Uso |
|-------------|---------|-----------------|
| **PAN** (Personal Area Network) | Pocos metros | Bluetooth entre teléfono y audífonos |
| **LAN** (Local Area Network) | Edificio/casa | Red WiFi de tu hogar u oficina |
| **MAN** (Metropolitan Area Network) | Ciudad | Red de una universidad |
| **WAN** (Wide Area Network) | País/mundo | Internet |
| **GAN** (Global Area Network) | Continentes | Redes satelitales |

### 1.3. Elementos de una Red

```
┌─────────────────────────────────────────────────────────────────┐
│                    ELEMENTOS DE UNA RED                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  DISPOSITIVOS FINALES ( hosts)                                │
│  ├── Computadoras                                                │
│  ├── Teléfonos móviles                                          │
│  ├── Tablets                                                     │
│  └── Impresoras                                                 │
│                                                                 │
│  DISPOSITIVOS INTERMEDIOS                                      │
│  ├── Routers (enrutadores) - Conectan redes diferentes         │
│  ├── Switches (conmutadores) - Conectan dispositivos en LAN   │
│  ├── Access Points - Proporcionan WiFi                         │
│  ├── Firewalls - Filtran tráfico                               │
│  └── Modems - Convierten señales                               │
│                                                                 │
│  MEDIOS DE TRANSMISIÓN                                         │
│  ├── Cables de cobre (Ethernet)                                │
│  ├── Fibra óptica                                               │
│  ├── WiFi (ondas de radio)                                     │
│  └── Satelital                                                  │
│                                                                 │
│  PROTOCOLOS (reglas de comunicación)                           │
│  ├── TCP - Confiable, orientado a conexión                     │
│  ├── UDP - Rápido, sin confirmación                           │
│  ├── IP - Direccionamiento                                     │
│  ├── HTTP - Navegación web                                     │
│  └── DNS - Resolución de nombres                               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. MODELO OSI Y TCP/IP

### 2.1. El Modelo OSI (Open Systems Interconnection)

El modelo OSI es un marco conceptual de 7 capas que describe cómo los datos viajan a través de una red. Cada capa tiene responsabilidades específicas.

```
┌─────────────────────────────────────────────────────────────────┐
│                    MODELO OSI - 7 CAPAS                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   CAPA 7: APLICACIÓN                                          │
│   ═══════════════════════                                      │
│   • Interfaz con aplicaciones de usuario                       │
│   • HTTP, FTP, SMTP, DNS, DHCP                                │
│   • Ejemplo: Tu navegador web                                  │
│   ──────────────────────────────────────────────────────────    │
│                                                                 │
│   CAPA 6: PRESENTACIÓN                                        │
│   ═══════════════════════                                      │
│   • Traducción de formatos de datos                           │
│   • Cifrado, compresión, codificación                         │
│   • Ejemplo: SSL/TLS, JPEG, PNG                               │
│   ──────────────────────────────────────────────────────────    │
│                                                                 │
│   CAPA 5: SESIÓN                                               │
│   ════════════════                                             │
│   • Gestiona conexiones entre aplicaciones                     │
│   • Control de diálogos, sincronización                        │
│   • Ejemplo: NetBIOS, RPC                                     │
│   ──────────────────────────────────────────────────────────    │
│                                                                 │
│   CAPA 4: TRANSPORTE                                          │
│   ═══════════════════════                                      │
│   • Comunicación extremo a extremo                              │
│   • Segmentación, control de flujo                            │
│   • Ejemplo: TCP (confiable), UDP (rápido)                   │
│   ──────────────────────────────────────────────────────────    │
│                                                                 │
│   CAPA 3: RED                                                  │
│   ══════════════                                               │
│   • Enrutamiento entre redes                                   │
│   • Direccionamiento lógico (IP)                               │
│   • Ejemplo: Router, IP                                       │
│   ──────────────────────────────────────────────────────────    │
│                                                                 │
│   CAPA 2: ENLACE DE DATOS                                     │
│   ══════════════════════════                                   │
│   • Transmisión dentro de la red local                        │
│   • Direccionamiento físico (MAC)                             │
│   • Ejemplo: Switch, Ethernet, WiFi                           │
│   ──────────────────────────────────────────────────────────    │
│                                                                 │
│   CAPA 1: FÍSICA                                               │
│   ═════════════════                                            │
│   • Señales eléctricas, ópticas, radio                        │
│   • Cables, conectores, voltajes                              │
│   • Ejemplo: Cable Ethernet, fibra óptica                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2. Comparación OSI vs TCP/IP

| Capa OSI | Capa TCP/IP | Protocolos |
|----------|-------------|-----------|
| Aplicación | Aplicación | HTTP, FTP, SMTP, DNS |
| Presentación | Aplicación | SSL, TLS |
| Sesión | Aplicación | NetBIOS, RPC |
| Transporte | Transporte | TCP, UDP |
| Red | Internet | IP, ICMP |
| Enlace de datos | Acceso a red | Ethernet, ARP |
| Física | Acceso a red | Cables, hubs |

### 2.3. Cómo Viajan los Datos (Encapsulamiento)

```
┌─────────────────────────────────────────────────────────────────┐
│                    ENCAPSULAMIENTO DE DATOS                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Cuando envías datos por la red, cada capa agrega su propia    │
│  "sobre" (cabecera) con información de control:               │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ APLICACIÓN: "Hola, ¿cómo estás?"                        │   │
│  └─────────────────────────────────────────────────────────┘   │
│                           ↓                                    │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ TRANSPORTE: Cabecera TCP (puerto 443)                    │   │
│  │ "Hola, ¿cómo estás?"                                    │   │
│  └─────────────────────────────────────────────────────────┘   │
│                           ↓                                    │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ RED: Cabecera IP (192.168.1.5 → 142.250.80.46)         │   │
│  │ Cabecera TCP                                            │   │
│  │ "Hola, ¿cómo estás?"                                    │   │
│  └─────────────────────────────────────────────────────────┘   │
│                           ↓                                    │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ ENLACE: Cabecera Ethernet (MAC → MAC)                    │   │
│  │ Cabecera IP                                             │   │
│  │ Cabecera TCP                                            │   │
│  │ "Hola, ¿cómo estás?"                                    │   │
│  └─────────────────────────────────────────────────────────┘   │
│                           ↓                                    │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ FÍSICA: Señales eléctricas en el cable                   │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. PUERTOS Y SERVICIOS

### 3.1. ¿Qué es un Puerto?

Un **puerto** es un número de 16 bits (0-65535) que identifica una aplicación o servicio específico en un dispositivo de red. Mientras la dirección IP identifica el dispositivo, el puerto identifica qué aplicación debe recibir los datos.

**Analogía:**
La dirección IP es como la dirección de un edificio de apartamentos. El puerto es como el número del apartamento específico. Así, 192.168.1.1:80 significa "el servicio HTTP en la computadora 192.168.1.1".

### 3.2. Clasificación de Puertos

| Rango | Categoría | Uso |
|-------|-----------|-----|
| 0-1023 | **Puertos bien conocidos** | Servicios fundamentales del sistema |
| 1024-49151 | **Puertos registrados** | Aplicaciones de usuario |
| 49152-65535 | **Puertos dinámicos/privados** | Asignación temporal |

### 3.3. Puertos y Servicios Más Importantes

```
┌─────────────────────────────────────────────────────────────────┐
│              PRINCIPALES PUERTOS Y SERVICIOS                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────┬──────────────────────────────────────┐    │
│  │ PUERTO          │ SERVICIO / DESCRIPCIÓN                │    │
│  ├─────────────────┼──────────────────────────────────────┤    │
│  │ 20, 21          │ FTP - Transferencia de archivos      │    │
│  │ 22              │ SSH - Acceso remoto seguro            │    │
│  │ 23              │ Telnet - Acceso remoto inseguro       │    │
│  │ 25              │ SMTP - Correo saliente               │    │
│  │ 53              │ DNS - Resolución de nombres          │    │
│  │ 67, 68          │ DHCP - Asignación automática de IP  │    │
│  │ 80              │ HTTP - Navegación web                │    │
│  │ 110             │ POP3 - Correo entrante               │    │
│  │ 143             │ IMAP - Correo entrante avanzado     │    │
│  │ 443             │ HTTPS - Navegación web segura        │    │
│  │ 445             │ SMB - Compartición de archivos       │    │
│  │ 3306            │ MySQL - Base de datos                │    │
│  │ 3389            │ RDP - Escritorio remoto Windows      │    │
│  │ 5432            │ PostgreSQL - Base de datos           │    │
│  │ 5900            │ VNC - Escritorio remoto             │    │
│  │ 6379            │ Redis - Base de datos en memoria     │    │
│  │ 8080            │ HTTP Proxy - Web alternativo         │    │
│  │ 27017           │ MongoDB - Base de datos NoSQL       │    │
│  └─────────────────┴──────────────────────────────────────┘    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 3.4. Puertos Típicos en Pentesting

Cuando realizas un pentesting, estos son los puertos que siempre debes verificar:

| Puerto | Servicio | Qué Buscar |
|--------|----------|------------|
| 21 | FTP | Login anónimo, archivos sensibles |
| 22 | SSH | Versión, autenticación por clave |
| 23 | Telnet | Credenciales en texto plano |
| 25 | SMTP | Relay abierto, enumeración de usuarios |
| 53 | DNS | Transferencia de zona, registros |
| 80/443 | HTTP/HTTPS | Vulnerabilidades web |
| 139/445 | SMB | Versión, shares, EternalBlue |
| 1433 | MSSQL | Credenciales por defecto |
| 3306 | MySQL | Inyección SQL, credenciales |
| 3389 | RDP | BlueKeep, credenciales |
| 5432 | PostgreSQL | Credenciales por defecto |

### 3.5. Ver Servicios en tu Sistema

```bash
# Ver todos los servicios escuchando en tu sistema
sudo ss -tulpn


Netid  State   Recv-Q  Send-Q   Local Address:Port    Peer Address:Port  Process
tcp    LISTEN  0       128      0.0.0.0:22           0.0.0.0:*          users:(("sshd",pid=1234,fd=3))
tcp    LISTEN  0       128      127.0.0.1:631        0.0.0.0:*          users:(("cupsd",pid=5678,fd=7))
tcp    LISTEN  0       511      0.0.0.0:3000         0.0.0.0:*          users:(("node",pid=9012,fd=18))
tcp    LISTEN  0       128      [::]:80               [::]:*             users:(("apache2",pid=3456,fd=4))
```

---

## 4. VULNERABILIDADES CONOCIDAS: CVE Y CWE

### 4.1. ¿Qué es CVE?

**CVE (Common Vulnerabilities and Exposures)** es un diccionario de identificadores públicos para vulnerabilidades de seguridad conocidas. Cada CVE tiene un número único que permite referenciar vulnerabilidades específicas.

**Formato:** CVE-AAAA-NNNNNNN

```
CVE-2021-44228
│    │       │
│    │       └── Número de vulnerabilidad específica
│    │
│    └─────────── Año de publicación
│
└────────────────── Identificador del proyecto
```

**Ejemplos:**
- `CVE-2021-44228` - Log4Shell (vulnerabilidad en Log4j)
- `CVE-2017-0144` - EternalBlue (explotado por WannaCry)
- `CVE-2014-0160` - Heartbleed (OpenSSL)
- `CVE-2012-2122` - MySQL Authentication Bypass

### 4.2. ¿Qué es CWE?

**CWE (Common Weakness Enumeration)** es una lista formal de debilidades comunes en software. Describe las causas raíz de las vulnerabilidades, no las vulnerabilidades específicas.

**Ejemplos de CWE:**
| CWE | Nombre | Descripción |
|-----|--------|------------|
| CWE-79 | XSS | Cross-site Scripting |
| CWE-89 | SQLi | SQL Injection |
| CWE-22 | Path Traversal | Inclusión de archivos locales |
| CWE-287 | Auth Bypass | Fallos de autenticación |
| CWE-798 | Hard-coded Credentials | Credenciales codificadas |

### 4.3. Relación entre CVE y CWE

```
┌─────────────────────────────────────────────────────────────────┐
│              RELACIÓN CVE - CWE - CWE                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  CWE (Debilidad)                                               │
│  ════════════════                                              │
│  "¿Cuál es el problema?"                                        │
│  Ejemplo: CWE-89 → SQL Injection                                │
│                                                                 │
│       │                                                        │
│       │ Es la causa raíz de                                    │
│       ▼                                                        │
│  CVE (Vulnerabilidad)                                          │
│  ═══════════════════════                                        │
│  "¿Dónde está el problema específico?"                          │
│  Ejemplo: CVE-2021-44228 → Log4Shell en Apache Log4j          │
│                                                                 │
│       │                                                        │
│       │ Es explotado por                                       │
│       ▼                                                        │
│  Exploit                                                         │
│  ═══════                                                       │
│  "¿Cómo se aprovecha?"                                          │
│  Ejemplo: jndi://sitioMalicioso.com/a → RCE                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 4.4. Base de Datos de Vulnerabilidades

| Base de Datos | URL | Descripción |
|--------------|-----|-------------|
| NVD (National Vulnerability Database) | nvd.nist.gov | Base de datos oficial de CVE de EE.UU. |
| CVE Mitre | cve.mitre.org | Lista oficial de CVEs |
| Exploit-DB | exploit-db.com | Exploits públicos |
| Vulners | vulners.com | Buscador de vulnerabilidades |
| CVE Details | cvedetails.com | Vulnerabilidades por producto |

### 4.5. Cómo Buscar Vulnerabilidades por Servicio

```bash
# Buscar versión específica de OpenSSL
openssl version

# OpenSSL 1.0.1g → Vulnerable a Heartbleed (CVE-2014-0160)

# Buscar en la base de datos
# https://www.cvedetails.com/version/195/

# Con searchsploit (en Kali)
searchsploit openssl 1.0.1


OpenSSL <= 1.0.1g 'Heartbleed' - Memory Leak      | linux/remote/32764.py

# Con nmap scripts
nmap --script vuln --script-args vulns.showall 192.168.56.102
```

---

## 5. ANATOMÍA DE LA COMUNICACIÓN EN RED

### 5.1. Comunicación entre Dos Computadoras en la Misma Red

```
┌─────────────────────────────────────────────────────────────────┐
│     COMUNICACIÓN EN RED LOCAL (MISMO SEGMENTO)                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Computadora A                    Computadora B                │
│  ┌───────────────┐               ┌───────────────┐            │
│  │ IP: 192.168.1.10│             │ IP: 192.168.1.20│          │
│  │ MAC: AA:BB:CC │               │ MAC: DD:EE:FF │            │
│  │           │   │               │           │   │            │
│  └─────┬─────┘   │               └─────┬─────┘   │            │
│        │         │                     │         │            │
│        └─────────┼─────────────────────┘         │            │
│                  │                               │            │
│              ┌───┴───────────────────────────────┘            │
│              │                                             │
│              │         SWITCH (Conmutador)                   │
│              │                                             │
│              │         - Lee direcciones MAC                │
│              │         - Reenvía tramas solo al destino     │
│              │                                             │
│              └─────────────────────────────────────────────   │
│                                                                 │
│  PROCESO DE COMUNICACIÓN:                                     │
│  ────────────────────────────                                  │
│                                                                 │
│  1. A quiere enviar a B                                       │
│  2. A verifica que B está en su misma red (misma subred)     │
│  3. A consulta su tabla ARP: "¿Quién tiene IP 192.168.1.20?" │
│  4. B responde con su MAC: "DD:EE:FF"                        │
│  5. A envía trama Ethernet con:                               │
│     • MAC origen: AA:BB:CC                                   │
│     • MAC destino: DD:EE:FF                                   │
│  6. Switch reenvía la trama solo a B                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 5.2. Comunicación entre Redes Diferentes (Via Router)

```
┌─────────────────────────────────────────────────────────────────┐
│     COMUNICACIÓN ENTRE REDES (VIA ROUTER)                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Red Local 1                   Red Local 2                     │
│  ┌─────────────┐              ┌─────────────┐                 │
│  │ PC A        │              │ Servidor B  │                 │
│  │ IP: 192.168.1.10│          │ IP: 10.0.0.50│               │
│  │ GW: 192.168.1.1│          │ GW: 10.0.0.1 │               │
│  └──────┬──────┘              └──────┬──────┘                 │
│         │                           │                         │
│         │ eth0                      │ eth0                    │
│         └─────────┬─────────────────┘                         │
│                   │                                           │
│            ┌──────┴──────┐                                    │
│            │   ROUTER    │                                    │
│            │             │                                    │
│            │ eth0: 192.168.1.1  │                            │
│            │ eth1: 10.0.0.1     │                            │
│            └──────┬──────┘                                    │
│                   │                                           │
│                   │ eth1                                       │
│                   │                                           │
│                   │         INTERNET                          │
│                   │                                           │
│                   └─────────────────────────────────────────  │
│                                                                 │
│  PROCESO DE COMUNICACIÓN:                                     │
│  ────────────────────────────                                  │
│                                                                 │
│  1. A quiere enviar a B (10.0.0.50)                          │
│  2. A detecta que B NO está en su subred                      │
│  3. A envía paquete al Gateway (192.168.1.1)                  │
│  4. Router recibe paquete, ve destino 10.0.0.50               │
│  5. Router busca en tabla de enrutamiento                    │
│  6. Router reenvía por eth1 hacia la otra red                │
│  7. Switch en red 2 entrega al servidor B                     │
│                                                                 │
│  RESPUESTA: El proceso inverso                                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 5.3. El Router de Entrada (Gateway)

El **router de entrada** o **gateway** es el dispositivo que conecta tu red local con Internet. Es el "punto de salida" de tu red hacia el mundo exterior.

```
┌─────────────────────────────────────────────────────────────────┐
│                    EL ROUTER DE ENTRADA                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│                           INTERNET                              │
│                              │                                 │
│                              │ WAN (IP pública)                │
│                              │                                 │
│                     ┌────────┴────────┐                       │
│                     │    ROUTER WIFI    │                       │
│                     │                  │                       │
│                     │  - NAT (traduce IPs)                   │
│                     │  - DHCP (da IPs)                        │
│                     │  - Firewall (filtra)                    │
│                     │  - DNS local                            │
│                     └────────┬────────┘                       │
│                              │ LAN (IP privada)                 │
│                              │                                 │
│              ┌───────────────┼───────────────┐                 │
│              │               │               │                 │
│         ┌────┴────┐    ┌────┴────┐    ┌────┴────┐          │
│         │   PC    │    │  Móvil  │    │ Laptop  │          │
│         │ 192.168.1.10│ │192.168.1.11│ │192.168.1.12│        │
│         └─────────┘    └─────────┘    └─────────┘          │
│                                                                 │
│  FUNCIONES DEL ROUTER:                                        │
│  ──────────────────────                                        │
│                                                                 │
│  1. NAT (Network Address Translation)                         │
│     └── Traduce IP privadas a IP pública                      │
│     └── 192.168.1.10:50000 → 203.0.113.5:50000              │
│                                                                 │
│  2. DHCP                                                      │
│     └── Asigna direcciones IP automáticamente                 │
│     └── Rango: 192.168.1.100 - 192.168.1.200                │
│                                                                 │
│  3. DNS                                                       │
│     └── Resuelve nombres de dominio                           │
│     └── Traduce google.com → 142.250.80.46                   │
│                                                                 │
│  4. Firewall                                                  │
│     └── Filtra tráfico entrante/saliente                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 5.4. Cómo Funciona DNS (Domain Name System)

**DNS** es el "directorio telefónico" de Internet. Traduce nombres de dominio legibles por humanos a direcciones IP que las computadoras usan.

```
┌─────────────────────────────────────────────────────────────────┐
│                    RESOLUCIÓN DNS                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  QUERIES RECURSIVAS                                           │
│  ───────────────────                                           │
│                                                                 │
│  1. Usuario escribe "google.com" en el navegador             │
│                                                                 │
│  2. Computadora consulta al DNS local (router)                 │
│                                                                 │
│  3. Router consulta al DNS del ISP                            │
│                                                                 │
│  4. DNS del ISP consulta a servidores raíz                    │
│                                                                 │
│  5. Servidor raíz dice: "Pregunta a .com TLD"                │
│                                                                 │
│  6. DNS ISP consulta a .com TLD                              │
│                                                                 │
│  7. TLD dice: "Pregunta a ns1.google.com"                    │
│                                                                 │
│  8. DNS ISP consulta a ns1.google.com                         │
│                                                                 │
│  9. ns1.google.com responde: "142.250.80.46"                │
│                                                                 │
│  10. DNS ISP la respuesta y responde al router           │
│                                                                 │
│  11. Router y responde a tu computadora                  │
│                                                                 │
│  12. ¡Navegador conecta a 142.250.80.46!                     │
│                                                                 │
│  TIEMPO DE CACHE TTL:                                         │
│  ────────────────────                                         │
│  • DNS guarda respuestas por tiempo TTL (Time To Live)        │
│  • Típicamente 300 segundos a 24 horas                        │
│  • Reduce latencia y carga de servidores                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 6. INTERFACES DE RED Y DIRECCIONES

### 6.1. ¿Qué es una Interfaz de Red?

Una **interfaz de red** es el punto de conexión lógica de un dispositivo a una red. Puede ser física (tarjeta de red Ethernet, WiFi) o virtual (lo, docker0).

**Interfaces comunes:**
| Interfaz | Tipo | Descripción |
|----------|------|-------------|
| `eth0`, `eth1` | Física | Puertos Ethernet por cable |
| `wlan0`, `wlan1` | Física | Tarjetas WiFi |
| `lo` | Virtual | Loopback (127.0.0.1) |
| `docker0` | Virtual | Bridge de Docker |
| `veth*` | Virtual | Interfaces de contenedores |

### 6.2. Dirección MAC (Media Access Control)

La dirección **MAC** es un identificador único de 48 bits (6 bytes) asignado a cada adaptador de red en fábrica. Es la dirección de la capa 2 (enlace de datos).

**Formato:**
```
AA:BB:CC:DD:EE:FF
│││ │││ │││ │││
│││ │││ │││ │││ └── Byte 6 (fabricante)
│││ │││ │││ ││└────── Byte 5
│││ │││ │││ │└───────── Byte 4
│││ │││ │││ └────────── Byte 3 (NIC específico)
│││ │││ ││└────────────── Byte 2
│││ │││ │└───────────────── Byte 1
│││ ││└────────────────────── OUI (identificador del fabricante)
│││ │└──────────────────────── OUI
││└──────────────────────────── OUI
└────────────────────────────── OUI (primeros 3 bytes)
```

**OUI (Organizationally Unique Identifier):**
- Primeros 3 bytes identifican al fabricante
- AA:BB:CC → ej: Intel, Cisco, etc.

### 6.3. Dirección IP (Internet Protocol)

**IPv4:**
- 32 bits (4 bytes)
- Formato: A.B.C.D (ej: 192.168.1.100)
- Rango: 0.0.0.0 a 255.255.255.255
- Aproximadamente 4,300 millones de direcciones

**IPv6:**
- 128 bits
- Formato: 2001:0db8:85a3:0000:0000:8a2e:0370:7334
- Rango virtually infinito

**Clases IPv4 :**
| Clase | Rango | Uso |
|-------|-------|-----|
| A | 1.0.0.0 - 126.255.255.255 | Redes grandes |
| B | 128.0.0.0 - 191.255.255.255 | Redes medianas |
| C | 192.0.0.0 - 223.255.255.255 | Redes pequeñas |
| D | 224.0.0.0 - 239.255.255.255 | Multicast |
| E | 240.0.0.0 - 255.255.255.255 | Reservado |

### 6.4. Direcciones Privadas y Públicas

```
┌─────────────────────────────────────────────────────────────────┐
│              DIRECCIONES PRIVADAS vs PÚBLICAS                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  DIRECCIONES PRIVADAS (no se enrutan en Internet):             │
│  ───────────────────────────────────────────────────────        │
│                                                                 │
│  10.0.0.0 - 10.255.255.255       → 10.0.0.0/8                │
│  172.16.0.0 - 172.31.255.255    → 172.16.0.0/12              │
│  192.168.0.0 - 192.168.255.255  → 192.168.0.0/16              │
│                                                                 │
│  DIRECCIONES PÚBLICAS (únicas en Internet):                   │
│  ─────────────────────────────────────────────                 │
│                                                                 │
│  Todas las demás direcciones son públicas                      │
│  Ejemplo: 142.250.80.46 (google.com)                         │
│                                                                 │
│  TRADUCCIÓN NAT:                                               │
│  ────────────────                                               │
│                                                                 │
│  Tu red local:                    Internet:                    │
│  192.168.1.10 ──┐                                                │
│  192.168.1.11 ──┼──→ Router ───→ 203.0.113.5                 │
│  192.168.1.12 ──┘        NAT         (IP pública)            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 7. COMANDOS DE LINUX PARA REDES

### 7.1. ifconfig - Configuración de Interfaces

**Propósito:** Mostrar y configurar parámetros de interfaces de red.

```bash
# Ver todas las interfaces y su configuración
ifconfig

：
┌─────────────────────────────────────────────────────────────────┐
│ eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500    │
│         │    │      │        │       │          │               │
│         │    │      │        │       │          └── Maximum Transmission Unit │
│         │    │      │        │       │                                 │
│         │    │      │        │       └─────────── Multicast habilitado  │
│         │    │      │        │                                  │
│         │    │      │        └────────────────── Activo y transmitiendo  │
│         │    │      │                                          │
│         │    │      └────────────────────────── Broadcast activo        │
│         │    │                                                   │
│         │    └────────────────────────────────────── Interfaz arriba      │
│         │                                                        │
│         └────────────────────────────────────────── Nombre de interfaz   │
│                                                                 │
│     inet 192.168.1.100  netmask 255.255.255.0  broadcast 192.168.1.255 │
│     │    │                │               │                       │
│     │    │                │               └──── Dirección de broadcast    │
│     │    │                └──────────────────── Máscara de subred        │
│     │    └─────────────────────────────────────── Dirección IPv4         │
│     └───────────────────────────────────────────── Protocolo: IP (inet)   │
│                                                                 │
│     inet6 fe80::a00:27ff:fe8e:8aa8  prefixlen 64  scopeid 0x20<link> │
│     │    │                                                      │         │
│     │    │                                                      └─ Alcance: Link-local │
│     │    └──────────────────────────────────────────────── IPv6               │
│     └─────────────────────────────────────────────── Protocolo: IPv6        │
│                                                                 │
│     ether 08:00:27:8e:8a:a8  txqueuelen 1000  (ETHERNET)                │
│     │    │                    │                                        │
│     │    │                    └────────────────── Cola de transmisión     │
│     │    └─────────────────────────────────────── Dirección MAC           │
│     └───────────────────────────────────────────── Tipo: Ethernet           │
│                                                                 │
│     RX packets 12345  bytes 1234567 (1.2 MB)                             │
│     │ packets │        │                                              │
│     │         └────────┴── Paquetes recibidos (RX = Receive)           │
│     │                                                                  │
│     │ packets 5432  bytes 987654  (1.0 MB)                            │
│     │ packets │        │                                              │
│     │         └────────┴── Paquetes enviados (TX = Transmit)            │
│     │                                                                  │
│     RX errors 0  dropped 0  overruns 0  frame 0                       │
│     │        │      │       │        │      │                          │
│     │        │      │       │        │      └─ Errores de trama         │
│     │        │      │       │        └────────── Sobretasa              │
│     │        │      │       └─────────────────── Paquetes descartados   │
│     │        │      └──────────────────────────────── Errores           │
│     │        └────────────────────────────────────────── Sin errores      │
│     │                                                                     │
│     TX errors 0  dropped 0  overruns 0  carrier 0                       │
│     │        │      │       │        │                                     │
│     │        │      │       │        └──────────── Señal de portadora     │
│     │        │      │       └──────────────────── Sobretasa TX            │
│     │        │      └──────────────────────────── Paquetes TX descartados │
│     │        └──────────────────────────────────── Errores TX              │
│     │                                                                    │
│     collisions:0                                                        │
│     └─────────────────────────────── Colisiones en el medio              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        │  │      │        │
        │  │      │        └──── Tamaño máximo de paquete
        │  │      └────────────── Interfaz activa
        │  └───────────────────────── Loopback
        └───────────────────────────── Interfaz operativa

    inet 127.0.0.1  netmask 255.0.0.0
    │    │            │
    │    │            └──── 255.0.0.0 = /8 (loopback)
    │    └───────────────── Siempre 127.0.0.1

    inet6 ::1  prefixlen 128  scopeid 0x10<host,loopback>
    │    │                          │
    │    │                          └──── Loopback IPv6
    │    └────────────────────────────── IPv6 loopback
    └───────────────────────────────────── IPv6 para loopback

# Ver solo una interfaz específica
ifconfig eth0

# Activar/desactivar interfaz
sudo ifconfig eth0 up
sudo ifconfig eth0 down

# Cambiar dirección IP (temporal)
sudo ifconfig eth0 192.168.1.50 netmask 255.255.255.0

# Poner interfaz en modo promiscuo (para sniffing)
sudo ifconfig eth0 promisc
```

### 7.2. ip - Manipulación de Redes (Moderno)

**Propósito:** Mostrar y manipular rutas, dispositivos, política de enrutamiento y túneles.

```bash
# Ver todas las interfaces
ip addr

：
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    │ │      │          │        │                    │
    │ │      │          │        │                    └─ Longitud de cola
    │ │      │          │        └──────────────────────── Estado: UNKNOWN
    │ │      │          └────────────────────────────────── Cola: noqueue
    │ │      └────────────────────────────────────────────── MTU: 65536
    │ └────────────────────────────────────────────────────── Flags de la interfaz
    └────────────────────────────────────────────────────────── Número de índice

    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    │   │         │                      │
    │   │         │                      └──── Broadcast MAC
    │   │         └─────────────────────────── MAC (loopback)
    │   └─────────────────────────────────────── Tipo de enlace
    └────────────────────────────────────────────── Nombre de interfaz

    inet 127.0.0.1/8 scope host lo
    │   │           ││    │
    │   │           ││    └──── Scope: host (solo esta máquina)
    │   │           │└────────── Prefixlen: /8 (8 bits de red)
    │   │           └──────────── IPv4
    │   └────────────────────────── IPv4

2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
    │    │         │      │       │         │
    │    │         │      │       │         └─ Cola: pfifo_fast
    │    │         │      │       └─────────── MTU: 1500
    │    │         │      └──────────────────── Flags UP
    │    │         └──────────────────────────── Flags MULTICAST
    │    └────────────────────────────────────── Flags BROADCAST
    │                                              Flags MULTICAST
    │    └─────────────────────────────────────── Flags RUNNING

    link/ether 08:00:27:8e:8a:a8 brd ff:ff:ff:ff:ff:ff
    │   │         │                    │
    │   │         │                    └──── Broadcast MAC
    │   │         └────────────────────────── MAC
    │   └─────────────────────────────────────── Tipo: Ethernet

    inet 192.168.1.100/24 brd 192.168.1.255 scope global dynamic eth0
    │   │                ││    │         │      │      │
    │   │                ││    │         │      │      └─ Nombre interfaz
    │   │                ││    │         │      └───────── Grupo: global
    │   │                ││    │         └─────────────── Broadcast
    │   │                ││    └────────────────────────── Prefixlen
    │   │                │└────────────────────────────────── IPv4
    │   │                └─────────────────────────────────── IPv4
    │   └──────────────────────────────────────────────────── IPv4
    │                                                           
    valid_lft forever preferred_lft forever
    │           │
    │           └──── Tiempo preferido (forever = infinito)
    └──────────────── Tiempo válido (forever = infinito)

    inet6 fe80::a00:27ff:fe8e:8aa8/64 scope link
    │   │                              │    │
    │   │                              │    └──── Scope: link
    │   │                              └─────────── Prefixlen
    │   └──────────────────────────────────────────── IPv6 link-local
    │                                                 
    valid_lft forever preferred_lft forever

# Ver tabla de enrutamiento
ip route


default via 192.168.1.1 dev eth0 proto dhcp
│     │                 │    │      │
│     │                 │    │      └─ Protocolo: DHCP
│     │                 │    └────────── Interfaz
│     │                 └──────────────── Gateway
│     └─────────────────────────────────── Ruta por defecto (0.0.0.0/0)

192.168.1.0/24 dev eth0 proto kernel scope link src 192.168.1.100
│              │    │  │      │       │
│              │    │  │      │       └──── IP local
│              │    │  │      └────────────── Scope: link
│              │    │  └────────────────────── Kernel
│              │    └────────────────────────── Interfaz
│              └──────────────────────────────── Red local

# Ver vecinos ARP (caché ARP)
ip neigh show


192.168.1.1 dev eth0 lladdr 00:11:22:33:44:55 REACHABLE
│               │    │    │                  │
│               │    │    │                  └──── Estado: REACHABLE
│               │    │    └──────────────────────── MAC del gateway
│               │    └────────────────────────────── Interfaz
│               └────────────────────────────────── IP del gateway

# Ver estadísticas de la interfaz
ip -s link show eth0

# Ver todas las direcciones IPv6
ip -6 addr show
```

### 7.3. ping - Verificar Conectividad

**Propósito:** Enviar paquetes ICMP ECHO_REQUEST para verificar conectividad.

```bash
# Ping básico
ping 8.8.8.8


PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
│    │              │    │
│    │              │    └──── Tamaño del paquete ICMP (56 bytes + 28 de cabecera)
│    │              └────────── Host de destino
│    └────────────────────────── Comando

64 bytes from 8.8.8.8: icmp_seq=1 ttl=118 time=15.2 ms
│    │        │     │       │    │
│    │        │     │       │    └──── Tiempo de respuesta
│    │        │     │       └───────── Time To Live
│    │        │     └────────────────── Número de secuencia
│    │        └────────────────────────── Bytes recibidos
│    └────────────────────────────────── 64 bytes = 56 datos + 8 ICMP

64 bytes from 8.8.8.8: icmp_seq=2 ttl=118 time=14.8 ms
64 bytes from 8.8.8.8: icmp_seq=3 ttl=118 time=15.1 ms

--- 8.8.8.8 ping statistics ---
│
3 packets transmitted, 3 received, 0% packet loss, time 2003ms
│   │           │            │       │       │
│   │           │            │       │       └──── Tiempo total
│   │           │            │       └────────────── Paquetes perdidos
│   │           │            └────────────────────── Paquetes recibidos
│   │           └─────────────────────────────────── Paquetes enviados
│   └──────────────────────────────────────────────── Destino

rtt min/avg/max/mdev = 14.8/15.0/15.2/0.2 ms
│  │  │    │    │    │
│  │  │    │    │    └──── Desviación estándar
│  │  │    │    └────────── Máximo
│  │  │    └─────────────── Promedio
│  │  └──────────────────── Mínimo
│  └────────────────────────── Round Trip Time

# Ping con conteo específico
ping -c 4 192.168.1.1

# Ping continuo (Ctrl+C para detener)
ping -i 2 google.com  # Cada 2 segundos

# Ping con tamaño de paquete específico
ping -s 1000 google.com  # 1000 bytes de datos

# Ping amplio (para descubrimiento)
ping -b 192.168.1.255  # Broadcast
```

### 7.4. traceroute / tracepath - Seguimiento de Ruta

**Propósito:** Mostrar la ruta que siguen los paquetes hasta el destino.

```bash
# Trace route básica
traceroute google.com


traceroute to google.com (142.250.80.46), 30 hops max, 60 byte packets
│          │                  │      │    │
│          │                  │      │    └──── Tamaño de paquete
│          │                  │      └────────── Máximo de saltos
│          │                  └────────────────── Destino
│          └─────────────────────────────────────── Comando

 1  gateway (192.168.1.1)  0.522 ms  0.401 ms  0.381 ms
 │   │                  │        │        │
 │   │                  │        │        └──── Tiempo 3er intento
 │   │                  │        └────────────── Tiempo 2do intento
 │   │                  └──────────────────────── Tiempo 1er intento
 │   └─────────────────────────────────────────── Nombre/IP del salto
 └─────────────────────────────────────────────── Número de salto

 2  10.0.0.1 (10.0.0.1)  5.234 ms  4.892 ms  5.101 ms
 3  * * *
 │  │  │  │
 │  │  │  └──── Tiempo 3er intento
 │  │  └──────── Tiempo 2do intento
 │  └──────────── Tiempo 1er intento
 │  (asteriscos = timeout, no respondió)

 4  72.14.215.85 (72.14.215.85)  15.234 ms  14.892 ms  15.101 ms
    │              │
    │              └─────────────────────────── IP del proveedor
    └─────────────────────────────────────────── Intemediario en la ruta

# tracepath (alternativa sin sudo)
tracepath google.com

# Traceroute con UDP en lugar de ICMP
sudo traceroute -I google.com

# Traceroute con número máximo de saltos
traceroute -m 15 google.com
```

### 7.5. netstat / ss - Estadísticas de Red

**Propósito:** Mostrar conexiones de red, tablas de enrutamiento, estadísticas de interfaces.

```bash
# Ver todas las conexiones con sockets numéricos
netstat -tunap


Active Internet connections (servers and established)
│ │ │ │ │ │
│ │ │ │ │ └── Proceso (PID/Nombre)
│ │ │ │ └──── PID del proceso
│ │ │ └─────── Nombres en lugar de números
│ │ └────────── Mostrar UDP
│ └──────────── Mostrar TCP

Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
│     │      │    │                    │                    │           │
│     │      │    │                    │                    │           └─ Programa
│     │      │    │                    │                    └─────────────── Estado de conexión
│     │      │    │                    └────────────────────────────────────── IP remota
│     │      │    └─────────────────────────────────────────────────────────── IP local
│     │      └──────────────────────────────────────────────────────────────── Bytes en cola TX
│     └──────────────────────────────────────────────────────────────────────── Bytes en cola RX
│
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      1234/sshd: /usr/sbin
│        │       │  │         │               │                      │            │
│        │       │  │         │               │                      │            └─ Nombre del programa
│        │       │  │         │               │                      └─────────────── Estado LISTEN
│        │       │  │         │               └─────────────────────────────────── Puerto remoto (* = cualquiera)
│        │       │  │         └───────────────────────────────────────────────────── Puerto local
│        │       │  │         │
│        │       │  │         └────────────────────────────────────────────────────── IP local (0.0.0.0 = todas)
│        │       │  └─────────────────────────────────────────────────────────────── Cola de envío
│        │       └────────────────────────────────────────────────────────────────── Cola de recepción
│        └────────────────────────────────────────────────────────────────────────── Protocolo

tcp        0      0 192.168.1.100:3000      192.168.1.50:54321       ESTABLISHED  5678/node
│        │       │  │                 │               │                 │         │
│        │       │  │                 │               │                 │         └─ Proceso
│        │       │  │                 │               │                 └───────────── Estado ESTABLISHED
│        │       │  │                 │               └─────────────────────────────── IP cliente
│        │       │  │                 └─────────────────────────────────────────────── IP servidor
│        │       │  └──────────────────────────────────────────────────────────────── Cola TX
│        │       └──────────────────────────────────────────────────────────────────── Cola RX
│        └──────────────────────────────────────────────────────────────────────────── TCP

tcp6       0      0 :::80                   :::*                    LISTEN      9012/apache2
│        │       │  ││  │                                             │
│        │       │  ││  └────────────────────────────────────────────── Puerto
│        │       │  │└───────────────────────────────────────────────── IP (::: = todas IPv6)
│        │       │  └──────────────────────────────────────────────────── IPv6
│        │       └──────────────────────────────────────────────────────── TCP

Estados de conexión TCP:
│
├─ LISTEN         → Esperando conexiones entrantes
├─ ESTABLISHED    → Conexión activa
├─ SYN_SENT       → SYN enviado, esperando respuesta
├─ SYN_RECV       → SYN recibido, handshake en progreso
├─ FIN_WAIT1      → FIN enviado, esperando terminación
├─ FIN_WAIT2      → Esperando FIN del otro lado
├─ TIME_WAIT      → Esperando antes de cerrar
├─ CLOSE          → Socket cerrado
├─ CLOSE_WAIT     → Esperando cierre remoto
├─ LAST_ACK       → Último ACK antes de cerrar
└─ CLOSING        → Cerrándose

# ss (moderno, más rápido que netstat)
ss -tunap

# Ver solo conexiones establecidas
ss -tn state established

# Ver sockets escuchando
ss -tln

# Ver conexiones con proceso
ss -tlnp

# Ver conexiones a un puerto específico
ss -tln | grep :80
```

### 7.6. arp - Tabla ARP

**Propósito:** Mostrar y manipular caché ARP (mapeo IP a MAC).

```bash
# Ver tabla ARP
arp -a


? (192.168.1.1) at 00:11:22:33:44:55 [ether] on eth0
│ │       │        │              │     │
│ │       │        │              │     └────── Interfaz
│ │       │        │              └──────────── Tipo: ethernet
│ │       │        └───────────────────────────── Dirección MAC
│ │       └─────────────────────────────────────── Dirección IP
│ └─────────────────────────────────────────────── Host desconocido (?)

# Ver tabla ARP sin resolución de nombres
arp -an

# Añadir entrada estática
sudo arp -s 192.168.1.50 00:11:22:33:44:55

# Eliminar entrada
sudo arp -d 192.168.1.50

# Ver con detalles
ip neigh show
```

### 7.7. dig - Consultas DNS

**Propósito:** Consultar información de registros DNS.

```bash
# Consulta básica de IP
dig google.com


; <<>> DiG 9.18.1 <<>> google.com
;; global options: +cmd
│ │ │ │ │
│ │ │ │ └─────────────────────────────────────────── Opciones globales
│ │ │ └───────────────────────────────────────────── Query de google.com
│ │ └─────────────────────────────────────────────── Versión de dig
│ └───────────────────────────────────────────────── Header de respuesta

;; Got answer:
│ │
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 12345
│ │     │        │          │
│ │     │        │          └─────── ID de transacción
│ │     │        └─────────────────── Estado: NOERROR (sin errores)
│ │     └────────────────────────────── Opcode: QUERY
│ └─────────────────────────────────────── Header marker

;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1
│       │   │  │  │  │    │     │       │       │       │
│       │   │  │  │  │    │     │       │       │       └────── Registros adicionales
│       │   │  │  │  │    │     │       │       └────────────── Registros de autoridad
│       │   │  │  │  │    │     │       └────────────────────── Respuestas (ANSWER)
│       │   │  │  │  │    │     └──────────────────────────────── Queries
│       │   │  │  │  │    └────────────────────────────────────── Additional flag
│       │   │  │  │  └─────────────────────────────────────────── Recursive Available
│       │   │  │  └────────────────────────────────────────────── Recursive Desired
│       │   │  └────────────────────────────────────────────────── Query Response flag
│       │   └───────────────────────────────────────────────────── Standard Query
│       └─────────────────────────────────────────────────────────── Response flag

;; QUESTION SECTION:
;google.com.                     IN      A
│         │         │     │
│         │         │     └──────────────────── Tipo: A (dirección IPv4)
│         │         └──────────────────────────── Clase: IN (Internet)
│         └───────────────────────────────────── Dominio queried

;; ANSWER SECTION:
google.com.              299     IN      A       142.250.80.46
│          │        │    │ │     │
│          │        │    │ │     └─────────────── IP
│          │        │    │ └────────────────────── Tipo A
│          │        │    └──────────────────────── TTL (segundos)
│          │        └───────────────────────────── IP del servidor autoritativo
│          └───────────────────────────────────── Dominio resuelto

;; Query time: 15 ms
;; SERVER: 192.168.1.1#53(192.168.1.1)
│           │      │ │
│           │      │ └──── Puerto
│           │      └──────── Servidor DNS usado
│           └──────────────── Tiempo de query

;; WHEN: Thu Mar 24 10:00:00 UTC 2026
;; MSG SIZE  rcvd: 55

# Consulta de registro MX (mail)
dig mx gmail.com

# Consulta de registro NS (nameservers)
dig ns google.com

# Consulta de registro TXT
dig txt google.com

# Consulta inversa (IP a nombre)
dig -x 142.250.80.46

# Consulta corta (solo IP)
dig +short google.com

# Especificar servidor DNS
dig @8.8.8.8 google.com

# Ver todas las consultas DNS del sistema
cat /etc/resolv.conf
```

### 7.8. host - Resolución DNS Simple

```bash
# Resolución básica
host google.com


google.com has address 142.250.80.46
google.com has address 142.250.80.78
│      │     │        │
│      │     │        └─────────── IPs encontradas
│      │     └────────────────────── Tipo A
│      └────────────────────────────── Dominio

google.com mail is handled by 10 aspmx.l.google.com.
│      │    │       │      │
│      │    │       │      └────────────── Servidor MX
│      │    │       └────────────────────── Prioridad
│      │    └─────────────────────────────── Tipo MX
│      └─────────────────────────────────── Dominio

# Resolución inversa
host 142.250.80.46


46.80.250.142.in-addr.arpa domain name pointer mail-yb1-f42.google.com.
```

### 7.9. nslookup - Consultas DNS

```bash
# Consulta interactiva
nslookup


> server 8.8.8.8
│     │
│     └────────────────────────── Servidor DNS a usar

Default Server:  dns.google
Address:  8.8.8.8

> google.com
│    │
│    └────────────────────────── Dominio a consultar

Server:  dns.google
Address:  8.8.8.8

Non-authoritative answer:
Name:    google.com
Addresses:  142.250.80.46
          142.250.80.78

> exit

# Consulta directa
nslookup google.com
```

### 7.10. curl / wget - Transferencia de Datos

```bash
# Descargar página web
curl http://example.com

# Descargar archivo
wget http://example.com/file.zip

# Ver headers HTTP
curl -I http://example.com


HTTP/1.1 200 OK
│     │    │
│     │    └────── Código de estado
│     └────────────── Versión HTTP

Accept-Ranges: bytes
Cache-Control: max-age=604800
Content-Type: text/html; charset=UTF-8
Date: Thu, 24 Mar 2026 10:00:00 GMT
ETag: "2.0-5d5c3f5a"
Server: ECS (sec/9792)
X-Cache: HIT
│   │
│   └──────────────── Headers personalizados del servidor

# Ver headers con wget
wget -S http://example.com

# Petición POST
curl -X POST http://api.example.com \
  -H "Content-Type: application/json" \
  -d '{"key": "value"}'

# Con cookies
curl -b cookies.txt http://example.com

# Con headers personalizados
curl -H "Authorization: Bearer token123" \
     -H "User-Agent: Mozilla/5.0" \
     http://example.com

# Seguir redirecciones
curl -L http://example.com

# Guardar salida
curl -o output.html http://example.com
```

---

## 8. NMAP: GUÍA COMPLETA DE PARÁMETROS

### 8.1. ¿Qué es Nmap?

**Nmap (Network Mapper)** es la herramienta de escaneo de red más poderosa y utilizada del mundo. Permite descubrir hosts y servicios en una red mediante el envío de paquetes y análisis de respuestas.

### 8.2. Sintaxis Básica

```bash
nmap [Tipo de Escaneo] [Opciones] [Objetivo]

# Ejemplos básicos
nmap 192.168.1.1              # Escaneo simple
nmap 192.168.1.1-254          # Rango de IPs
nmap 192.168.1.0/24           # Red completa (CIDR)
nmap -p 80,443 192.168.1.1   # Puertos específicos
nmap -sV 192.168.1.1          # Detección de versiones
```

### 8.3. Especificación de Objetivos

```bash
# Host individual
nmap 192.168.1.1

# Múltiples hosts separados por espacios
nmap 192.168.1.1 192.168.1.2 192.168.1.3

# Rango de IPs
nmap 192.168.1.1-254

# Red completa (notación CIDR)
nmap 192.168.1.0/24

# Archivo con lista de hosts
nmap -iL hosts.txt

# Hosts aleatorios (para pruebas)
nmap -iR 10

# Excluir hosts
nmap 192.168.1.0/24 --exclude 192.168.1.1
nmap 192.168.1.0/24 --excludefile exclude.txt
```

### 8.4. Técnicas de Escaneo de Puertos

```bash
# TCP SYN scan (-sS) - REQUIERE ROOT, sigiloso
# Envía SYN, si recibe SYN-ACK el puerto está abierto
# No completa el handshake, más sigiloso
sudo nmap -sS 192.168.1.1

# TCP connect scan (-sT) - No requiere root
# Completa el handshake TCP completo
nmap -sT 192.168.1.1

# UDP scan (-sU) - Lento pero necesario
# Envía paquetes UDP, si no responde probablemente abierto
sudo nmap -sU 192.168.1.1

# TCP ACK scan (-sA) - Solo detecta si hay firewall
# Útil para mapear reglas de firewall
nmap -sA 192.168.1.1

# Window scan (-sW) - Variante de ACK
nmap -sW 192.168.1.1

# Maquez scan (-sM) - Scan de TCP FIN/NULL/XMAS
nmap -sM 192.168.1.1

# No ping (-Pn) - No enviar ping inicial
# Saltar detección de hosts
nmap -Pn 192.168.1.1

# Ping sweep (-sn) - Solo descubrir hosts, no escanear puertos
# Muy rápido para descubrimiento de red
nmap -sn 192.168.1.0/24
```

### 8.5. Especificación de Puertos

```bash
# Escaneo por defecto (los 1000 puertos más comunes)
nmap 192.168.1.1

# Puertos específicos
nmap -p 80 192.168.1.1           # Solo puerto 80
nmap -p 80,443 192.168.1.1      # Puertos 80 Y 443
nmap -p 80-100 192.168.1.1      # Rango 80 a 100
nmap -p 80,443,8080 192.168.1.1 # Puertos específicos

# Todos los puertos (1-65535)
nmap -p- 192.168.1.1

# Puertos rápidos (los 100 más comunes)
nmap -F 192.168.1.1

# Rangos especiales
nmap -p - 192.168.1.1            # Todos los puertos
nmap -p U:53,T:80 192.168.1.1   # UDP 53 Y TCP 80

# Servicios conocidos
nmap --top-ports 100 192.168.1.1  # Top 100 puertos más comunes
```

### 8.6. Detección de Servicios y Versiones

```bash
# Detección de versiones (-sV)
# Intenta identificar versión exacta del servicio
nmap -sV 192.168.1.1


PORT     STATE  SERVICE         VERSION
│   │       │    │         │
│   │       │    │         └────────── Versión detectada
│   │       │    └─────────────────── Nombre del servicio
│   │       └────────────────────────── Estado
│   └──────────────────────────────── Puerto

22/tcp   open   ssh             OpenSSH 7.4 (protocol 2.0)
│    │      │    │         │
│    │      │    │         └────────── Versión del servicio
│    │      │    └──────────────────── Servicio conocido
│    │      └────────────────────────── Estado: abierto
│    └──────────────────────────────── Puerto

80/tcp   open   http            Apache httpd 2.4.6 ((CentOS))
443/tcp  open   ssl/https       Apache httpd 2.4.6

# Detección agresiva (-A) - Incluye SO, versiones, scripts y traceroute
nmap -A 192.168.1.1

# Detección de SO (-O) - Intenta identificar el sistema operativo
sudo nmap -O 192.168.1.1


OS details: Linux 4.15 (Ubuntu 18.04)
│
Aggressive OS guesses: Linux 4.15 (87%), 
                       Linux 3.13 (87%), 
                       Linux 3.2 - 4.9 (86%)
│
OS accuracy: 87%
```

### 8.7. Nmap Scripting Engine (NSE)

NSE permite ejecutar scripts para detección avanzada, vulnerabilidad y explotación.

```bash
# Scripts por defecto (-sC) - Ejecuta los scripts básicos
nmap -sC 192.168.1.1

# Scripts específicos
nmap --script=http-enum 192.168.1.1           # Enumerar directorios web
nmap --script=ssh-hostkey 192.168.1.1         # Llaves SSH
nmap --script=banner 192.168.1.1              # Banner grabbing
nmap --script=dns-zone-transfer 192.168.1.1    # Transferencia de zona DNS

# Scripts de vulnerabilidades
nmap --script=vuln 192.168.1.1


PORT   STATE SERVICE
445/tcp open  microsoft-ds

Host script results:
|_smb-vuln-ms10-061: 
|   VULNERABLE
|   Security Update for SMB (CVE-2010-1234)
|_  This vulnerability allows remote attackers to execute arbitrary code

# Categorías de scripts
nmap --script=auth 192.168.1.1        # Scripts de autenticación
nmap --script=broadcast 192.168.1.1   # Scripts broadcast
nmap --script=brute 192.168.1.1      # Fuerza bruta
nmap --script=default 192.168.1.1     # Scripts por defecto
nmap --script=discovery 192.168.1.1   # Descubrimiento
nmap --script=dos 192.168.1.1         # Denegación de servicio
nmap --script=exploit 192.168.1.1     # Explotación
nmap --script=external 192.168.1.1    # Scripts externos
nmap --script=fuzzer 192.168.1.1     # Fuzzing
nmap --script=intrusive 192.168.1.1  # Scripts intrusivos
nmap --script=malware 192.168.1.1    # Detección de malware
nmap --script=safe 192.168.1.1       # Scripts seguros
nmap --script=version 192.168.1.1    # Detección de versiones
nmap --script=vuln 192.168.1.1      # Vulnerabilidades

# Scripts específicos útiles para pentesting
nmap --script=smb-vuln-ms17-010 192.168.1.1  # EternalBlue
nmap --script=http-enum,http-title 192.168.1.1 -p 80  # Enum web
nmap --script=ssl-enum-ciphers 192.168.1.1 -p 443  # Cifrados SSL
nmap --script=mysql-info 192.168.1.1 -p 3306  # Info MySQL

# Ver scripts disponibles
ls /usr/share/nmap/scripts/ | grep -i "http"

# Múltiples scripts con patrones
nmap --script="http-*" 192.168.1.1  # Todos los de HTTP
nmap --script="vuln and not intrusive" 192.168.1.1
```

### 8.8. Opciones de Salida

```bash
# Salida normal (-oN)
nmap -oN scan.txt 192.168.1.1

# Salida XML (-oX) - Para herramientas automatizadas
nmap -oX scan.xml 192.168.1.1

# Salida Grepable (-oG) - Para grep
nmap -oG scan.gnmap 192.168.1.1

# formato Grepable:
# Nmap scan report for 192.168.1.1
# Host: 192.168.1.1 ()    Status: Up
# Host: 192.168.1.1 ()    Ports: 22/open/tcp//ssh//OpenSSH 7.4/
#                                                │ │    │    │
#                                                │ │    │    └─── Service
#                                                │ │    └────────── Estado
#                                                │ └───────────────── Puerto
#                                                └─────────────────── Protocolo

# Todos los formatos (-oA)
nmap -oA scan_resultado 192.168.1.1

# Append a archivo existente
nmap -oN scan.txt --append-output 192.168.1.2

# Aumentar verbosidad (-v, -vv, -vvv)
nmap -v 192.168.1.1
nmap -vv 192.168.1.1
nmap -vvv 192.168.1.1

# Modo silencioso (no output hasta final)
nmap -oN /dev/null 192.168.1.1
```

### 8.9. Optimización de Rendimiento

```bash
# Timing (0-5, más alto más rápido pero más ruidoso)
nmap -T0 192.168.1.1   # Paranoico (para evadir IDS)
nmap -T1 192.168.1.1   # Sigiloso
nmap -T2 192.168.1.1   # Polite (más lento, menos impacto)
nmap -T3 192.168.1.1   # Normal (por defecto)
nmap -T4 192.168.1.1   # Agresivo (buen balance)
nmap -T5 192.168.1.1   # Loco (muy rápido, muy ruidoso)

# Paralelismo
nmap --min-parallelism 50 192.168.1.1    # Mínimo de probes paralelos
nmap --max-parallelism 100 192.168.1.1  # Máximo de probes paralelos

# Tiempos de espera
nmap --max-scan-delay 10ms 192.168.1.1  # Retraso máximo entre probes
nmap --initial-rtt-timeout 1000ms 192.168.1.1

# Paquetes por segundo
nmap --min-rate 1000 192.168.1.1  # Mínimo 1000 paquetes/segundo
nmap --max-rate 10000 192.168.1.1 # Máximo 10000 paquetes/segundo

# RTT
nmap --defeat-rst-ratelimit 192.168.1.1  # Ignorar rate limit de RST
```

### 8.10. Opciones de Red

```bash
# Especificar interfaz
nmap -e eth0 192.168.1.1

# Especificar dirección IP de origen
nmap -S 192.168.1.50 192.168.1.1

# Usar proxy
nmap --proxies http://proxy:8080 192.168.1.1

# Fragmentar paquetes (para evadir IDS)
nmap -f 192.168.1.1              # Fragmentos de 8 bytes
nmap --mtu 16 192.168.1.1        # MTU personalizado

# Spoofear dirección MAC
nmap --spoof-mac Cisco 192.168.1.1

# DNS personalizado
nmap --dns-servers 8.8.8.8,1.1.1.1 192.168.1.1

# No hacer resolución DNS inversa
nmap -n 192.168.1.1              # Más rápido
nmap -R 192.168.1.1              # Siempre resolver (por defecto)
```

### 8.11. Opciones de Evasion y Firewall

```bash
# No hacer ping (-Pn)
# Muy importante si el firewall bloquea ICMP
nmap -Pn 192.168.1.1

# Detectar y evadir firewall/IDS
nmap --script=firewalk 192.168.1.1

# Enviar checksums incorrectas
nmap --badsum 192.168.1.1

# Randomizar objetivos
nmap --randomize-hosts 192.168.1.1-10

# Decoys (señuelos)
nmap -D 192.168.1.5,192.168.1.6,ME 192.168.1.1
# ME = tu IP real, los otros son señuelos

# Scan IPv6
nmap -6 fe80::1 eth0
```

### 8.12. Ejemplos Prácticos Completos

```bash
# ============================================
# ESCANEO BÁSICO DE RED
# ============================================

# Descubrir todos los hosts en la red local
nmap -sn 192.168.1.0/24 -oG - | grep "Up$" | cut -d" " -f2

# ============================================
# ESCANEO COMPLETO DE UN SERVIDOR
# ============================================

# Todos los puertos + versiones + scripts + detección de SO
sudo nmap -p- -sV -sC -O -A 192.168.1.100 -oA escaneo_completo

# ============================================
# ESCANEAR PARA PENTESTING WEB
# ============================================

nmap -p 80,443,8080,8443 \
     -sV \
     --script=http-enum,http-title,http-headers,ssl-enum-ciphers \
     192.168.1.100 -oA escaneo_web

# ============================================
# ESCANEO PARA BUSCAR VULNERABILIDADES
# ============================================

# Scripts de vulnerabilidades conocidas
nmap --script=vuln -p- 192.168.1.100

# EternalBlue (MS17-010)
nmap -p445 --script=smb-vuln-ms17-010 192.168.1.100

# Heartbleed (CVE-2014-0160)
nmap -p443 --script=ssl-heartbleed 192.168.1.100

# ============================================
# ESCANEO RÁPIDO VS ESCANEO SILENCIOSO
# ============================================

# Rápido (5 segundos aproximadamente)
nmap -T5 -F 192.168.1.0/24

# Silencioso (varios minutos)
sudo nmap -T1 -sS -p- -Pn 192.168.1.0/24

# ============================================
# INTERPRETAR RESULTADOS
# ============================================

# Estados de puertos:
# open    → Servicio escuchando y aceptando conexiones
# closed  → Puerto accesible pero sin servicio
# filtered→ Firewall filtrando el puerto
# unfiltered → Puerto accesible pero no se puede determinar estado

# Ver resultados guardados
cat escaneo_completo.nmap     # Formato normal
cat escaneo_completo.xml      # Formato XML
cat escaneo_completo.gnmap    # Formato Grepable

# Convertir XML a HTML
xsltproc escaneo_completo.xml -o informe.html
```

### 8.13. Cheat Sheet de Nmap

```
┌─────────────────────────────────────────────────────────────────┐
│                    NMAP CHEAT SHEET                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  DESCUBRIMIENTO DE HOSTS                                        │
│  ───────────────────────────                                     │
│  nmap -sn 192.168.1.0/24        Ping sweep                    │
│  nmap -Pn 192.168.1.1            Sin ping                      │
│                                                                 │
│  ESCANEO DE PUERTOS                                            │
│  ────────────────────────                                      │
│  nmap -p 80 192.168.1.1          Puerto específico            │
│  nmap -p 80-443 192.168.1.1      Rango de puertos             │
│  nmap -p- 192.168.1.1            Todos los puertos             │
│  nmap -F 192.168.1.1             Puertos rápidos               │
│                                                                 │
│  TÉCNICAS DE ESCANEO                                          │
│  ────────────────────────                                      │
│  nmap -sS 192.168.1.1            SYN scan (root)               │
│  nmap -sT 192.168.1.1            TCP connect                   │
│  nmap -sU 192.168.1.1            UDP scan (root)              │
│  nmap -sA 192.168.1.1            ACK scan                      │
│                                                                 │
│  DETECCIÓN                                                    │
│  ─────────                                                    │
│  nmap -sV 192.168.1.1            Versiones                     │
│  nmap -O 192.168.1.1             Sistema operativo             │
│  nmap -A 192.168.1.1             Todo (agresivo)              │
│                                                                 │
│  SCRIPTS                                                       │
│  ────────                                                      │
│  nmap -sC 192.168.1.1            Scripts por defecto           │
│  nmap --script=vuln 192.168.1.1  Scripts de vulnerabilidades   │
│  nmap --script="http-*" 192.168.1.1  Scripts HTTP              │
│                                                                 │
│  SALIDA                                                        │
│  ──────                                                        │
│  nmap -oN result.txt 192.168.1.1   Normal                     │
│  nmap -oX result.xml 192.168.1.1   XML                        │
│  nmap -oG result.gnmap 192.168.1.1 Grepable                   │
│  nmap -oA result 192.168.1.1       Todos                      │
│                                                                 │
│  OPTIMIZACIÓN                                                  │
│  ───────────                                                   │
│  nmap -T4 192.168.1.1             Timing rápido                │
│  nmap -T1 192.168.1.1             Timing sigiloso              │
│  nmap -v 192.168.1.1              Verboso                      │
│  nmap -vv 192.168.1.1             Muy verboso                 │
│                                                                 │
│  OPCIONES ESPECIALES                                          │
│  ────────────────────────                                      │
│  nmap -Pn 192.168.1.1              Sin ping                    │
│  nmap -f 192.168.1.1              Fragmentar paquetes          │
│  nmap -D SE 192.168.1.1            Decoys                      │
│  nmap -S 192.168.1.50 192.168.1.1 Spoofear IP                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## RESUMEN Y CONCLUSIONES

```
┌─────────────────────────────────────────────────────────────────┐
│                    PUNTOS CLAVE DE LA CLASE                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. MODELO OSI                                                  │
│     └── 7 capas que gobiernan la comunicación en red           │
│     └── Cada capa tiene responsabilidades específicas           │
│                                                                 │
│  2. PUERTOS Y SERVICIOS                                        │
│     └── 0-1023: Sistema, 1024-49151: Aplicaciones             │
│     └── Cada servicio tiene puertos asignados                   │
│     └── Conocer puertos comunes es esencial para pentesting    │
│                                                                 │
│  3. CVE Y CWE                                                  │
│     └── CVE: Identificador de vulnerabilidad específica       │
│     └── CWE: Debilidad genérica (causa raíz)                  │
│     └── Siempre verificar versiones contra bases de CVE       │
│                                                                 │
│  4. COMUNICACIÓN EN RED                                        │
│     └── Misma red: ARP → MAC → Switch                        │
│     └── Diferente red: IP → Router → NAT                     │
│     └── DNS traduce nombres a IPs                             │
│                                                                 │
│  5. COMANDOS DE LINUX                                          │
│     └── ifconfig/ip: Ver interfaces y IPs                      │
│     └── netstat/ss: Ver conexiones activas                     │
│     └── ping/traceroute: Diagnosticar conectividad             │
│     └── dig/nslookup: Consultar DNS                            │
│                                                                 │
│  6. NMAP                                                       │
│     └── Herramienta fundamental para pentesting                │
│     └── Múltiples técnicas de escaneo                          │
│     └── NSE permite automatización y detección avanzada       │
│                                                                 │
│  PRÓXIMOS PASOS:                                              │
│  ───────────────                                               │
│  • Practicar con máquinas virtuales                            │
│  • Familiarizarse con la salida de cada comando                │
│  • Realizar escaneos en entornos controlados                  │
│  • Documentar hallazgos                                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---


