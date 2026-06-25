# Clase 9: Escaneo de Redes con Nmap

**Duracion:** 2 horas

---

## Objetivos de Aprendizaje

1. Comprender que es el escaneo de redes, sus usos legitimos y las consideraciones eticas y legales
2. Instalar Nmap y ejecutar escaneos basicos de descubrimiento de hosts y puertos
3. Identificar servicios, versiones y sistemas operativos mediante Nmap
4. Utilizar scripts NSE (Nmap Scripting Engine) para automatizar tareas de auditoria y deteccion de vulnerabilidades

---

## Contenido Detallado

### 1. Que es el escaneo de redes?

El escaneo de redes es el proceso de enviar paquetes a dispositivos en una red para descubrir informacion sobre ellos: si estan activos, que puertos tienen abiertos, que servicios ejecutan, y que sistema operativo usan.

**Analogia:** Escanear una red es como caminar por un edificio de oficinas tocando puertas para ver cuales estan abiertas, mirando los carteles para saber que hay en cada oficina, y escuchando para identificar que actividades se realizan. Un administrador de red hace esto para mantener el inventario y la seguridad; un atacante lo hace para encontrar puntos debiles.

**Usos legitimos del escaneo de redes:**
- **Administracion:** Descubrir dispositivos no autorizados conectados a la red
- **Inventario:** Mantener un registro actualizado de equipos y servicios
- **Auditoria de seguridad:** Identificar puertos abiertos que deberian estar cerrados
- **Pentesting:** Evaluar la postura de seguridad de la organizacion (con permiso)
- **Solución de problemas:** Verificar que un servicio esta accesible

**Regla etica fundamental:**
NUNCA escanees una red que no sea tuya o para la que no tengas autorizacion explicita por escrito. Escanear redes ajenas puede ser ilegal (delito informatico en muchos paises). Siempre obten permiso antes de escanear.

### 2. Introduccion a Nmap

Nmap (Network Mapper) es la herramienta de escaneo de redes mas utilizada del mundo. Es gratuita, de codigo abierto, y funciona en Windows, Linux y Mac.

**Creador:** Gordon Lyon (Fyodor). El libro "Nmap Network Scanning" es la referencia oficial.

**Que puede hacer Nmap:**
- Descubrir hosts activos en una red
- Escanear puertos (TCP y UDP) y determinar su estado
- Identificar servicios y sus versiones (ej: "Apache 2.4.41")
- Detectar el sistema operativo remoto (ej: "Linux 5.4", "Windows 10 Pro")
- Ejecutar scripts automatizados para auditoria (NSE)
- Evadir firewalls y sistemas de deteccion (con tecnicas avanzadas)

#### Instalacion

**En Windows:**
1. Ve a https://nmap.org/download.html
2. Descarga el instalador "nmap-<version>-setup.exe"
3. Ejecuta el instalador (siguiente, siguiente, instalar)
4. Al finalizar, abre una terminal (PowerShell o CMD) y verifica:

```
nmap --version
```

**En Linux (Debian/Ubuntu):**
```
sudo apt update
sudo apt install nmap -y
nmap --version
```

**En Linux (Fedora/RHEL):**
```
sudo dnf install nmap -y
```

**Verificacion:** El comando `nmap --version` debe mostrar algo como:

```
Nmap version 7.95 ( https://nmap.org )
Platform: x86_64-pc-windows-windows
Compiled with: ...
```

#### Sintaxis basica de Nmap

```
nmap [opciones] <target>
```

Donde `<target>` puede ser:
- Una IP: `192.168.1.1`
- Un rango: `192.168.1.1-20`
- Una red CIDR: `192.168.1.0/24`
- Un nombre de dominio: `ejemplo.com`
- Varios targets separados por espacio: `192.168.1.1 192.168.1.2 10.0.0.1`

### 3. Descubrimiento de hosts (Host Discovery)

Antes de escanear puertos, normalmente quieres saber que dispositivos estan encendidos en la red.

#### Ping Scan (`-sn`)

El comando mas basico para descubrir hosts activos:

```
nmap -sn 192.168.1.0/24
```

**Que hace este comando:**
1. Nmap envia una solicitud ICMP Echo Request (ping) a cada IP del rango
2. Si el host responde, se considera "activo"
3. Tambien envia TCP SYN al puerto 443 y TCP ACK al puerto 80
4. En redes locales (LAN), tambien envia ARP request

**Ejemplo de salida:**

```
Starting Nmap 7.95 ( https://nmap.org )
Nmap scan report for 192.168.1.1
Host is up (0.0012s latency).
Nmap scan report for 192.168.1.10
Host is up (0.0023s latency).
Nmap scan report for 192.168.1.20
Host is up (0.0015s latency).
Nmap done: 256 IP addresses (3 hosts up) scanned in 3.45 seconds
```

En este ejemplo, de 256 IPs posibles en 192.168.1.0/24, solo 3 estaban activas.

#### Escaneo solo ARP (`-sn -PR`)

En tu red local, puedes forzar el uso de ARP, que es mas rapido y confiable:

```
nmap -sn -PR 192.168.1.0/24
```

ARP funciona solo en la misma red fisica (no atraviesa routers). Es el metodo mas rapido porque no necesita esperar respuestas ICMP.

#### Escaneo sin ping (`-Pn`)

A veces los firewalls bloquean los pings ICMP. Si sabes que un host esta activo pero Nmap no lo detecta, usa `-Pn` para saltarte la fase de descubrimiento:

```
nmap -Pn 192.168.1.10
```

Esto asume que el host esta activo y va directamente al escaneo de puertos.

### 4. Escaneo de puertos

El escaneo de puertos es la funcion principal de Nmap. Permite identificar que puertos estan abiertos en un dispositivo.

#### Estados de los puertos

| Estado | Significado |
|--------|-------------|
| **open** | El puerto esta abierto y un servicio esta escuchando |
| **closed** | El puerto esta cerrado (no hay servicio) |
| **filtered** | Un firewall esta bloqueando el acceso al puerto |
| **unfiltered** | El puerto es accesible pero Nmap no puede determinar si esta abierto o cerrado |
| **open\|filtered** | Nmap no puede diferenciar entre abierto o filtrado |
| **closed\|filtered** | Nmap no puede diferenciar entre cerrado o filtrado |

#### Tipos de escaneo TCP

**TCP SYN scan (`-sS`):** Es el escaneo por defecto y mas rapido. Se llama "semi-abierto" (half-open) porque no completa la conexion TCP.

Como funciona:
1. Nmap envia un paquete SYN (como si fuera a iniciar una conexion)
2. Si el puerto esta abierto: el destino responde con SYN-ACK
3. Nmap responde con RST (reset) en lugar de ACK, cerrando la conexion a medias
4. Si el puerto esta cerrado: el destino responde con RST
5. Si el puerto esta filtrado: no hay respuesta o se recibe ICMP unreachable

Ventaja: Rapido y menos detectable (no completa la conexion).
Desventaja: Requiere privilegios de administrador/root.

```
nmap -sS 192.168.1.10
```

**TCP Connect scan (`-sT`):** Completa la conexion TCP de forma normal (three-way handshake completo).

Como funciona:
1. Nmap envia SYN
2. Destino responde SYN-ACK (si abierto)
3. Nmap completa el handshake enviando ACK
4. Luego envia RST para cerrar la conexion

Ventaja: No requiere privilegios especiales.
Desventaja: Mas lento y mas detectable (queda registrado en logs).

```
nmap -sT 192.168.1.10
```

#### Escaneo UDP (`-sU`)

UDP no tiene handshake, por lo que el escaneo es diferente:
- Si no hay respuesta: el puerto puede estar abierto o filtrado (UDP no requiere respuesta)
- Si se recibe ICMP Port Unreachable: el puerto esta cerrado
- Si se recibe una respuesta del servicio: el puerto esta abierto

El escaneo UDP es mas lento porque Nmap debe esperar timeout para determinar que no hay respuesta.

```
nmap -sU 192.168.1.10
```

#### Especificar puertos

**Puertos especificos:**
```
nmap -p 22,80,443 192.168.1.10
```

**Rango de puertos:**
```
nmap -p 1-1000 192.168.1.10
```

**Todos los puertos (1-65535):**
```
nmap -p- 192.168.1.10
```
Advertencia: Escanear los 65535 puertos es muy lento (puede tomar horas).

**Puerto por nombre de servicio:**
```
nmap -p http,https,ssh 192.168.1.10
```

**Top 100 puertos mas comunes:**
```
nmap --top-ports 100 192.168.1.10
```

**Puertos en ambos protocolos:**
```
nmap -p T:22,80,U:53,161 192.168.1.10
```

### 5. Deteccion de servicios y versiones (`-sV`)

Una vez que sabes que puertos estan abiertos, el siguiente paso es identificar que servicio y version se ejecuta en cada puerto.

```
nmap -sV 192.168.1.10
```

**Como funciona:**
1. Nmap se conecta al puerto abierto
2. Envia peticiones especificas segun el servicio sospechado
3. Analiza la respuesta (banner) y la compara con su base de datos de firmas
4. Muestra el nombre del servicio, version y, a veces, informacion adicional

**Ejemplo de salida:**

```
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 8.0p1 Ubuntu 6ubuntu0.1 (Ubuntu Linux; protocol 2.0)
80/tcp   open  http    Apache httpd 2.4.41 ((Ubuntu))
3306/tcp open  mysql   MySQL 8.0.32-0ubuntu0.20.04.1
```

**Por que es importante la deteccion de versiones?**

Conocer la version exacta te permite buscar vulnerabilidades conocidas:
- OpenSSH 8.0p1: tiene CVE-2020-15778 (scp command injection)
- Apache 2.4.41: tiene CVE-2021-41773 (path traversal)
- MySQL 8.0.32: verificar si hay parches de seguridad

**Opcion de agresividad en la deteccion:**

```
nmap -sV --version-intensity 7 192.168.1.10
```

El nivel de intensidad va de 0 (ligero) a 9 (agresivo). Mayor intensidad = mas pruebas = mas exactitud pero mas lento. Por defecto es 7.

### 6. Deteccion de sistema operativo (`-O`)

Nmap puede identificar el sistema operativo remoto analizando las respuestas TCP/IP. Esta tecnica se llama "TCP/IP stack fingerprinting".

```
nmap -O 192.168.1.10
```

**Como funciona:**
Cada sistema operativo implementa el stack TCP/IP de forma ligeramente diferente. Nmap envia una serie de paquetes especiales (SYN, FIN, NULL, etc.) y analiza:
- Los valores TTL iniciales (Linux=64, Windows=128, Cisco=255)
- El tamano de ventana TCP (window size)
- Opciones TCP soportadas (MSS, WScale, Timestamp, etc.)
- Comportamiento ante paquetes malformados

**Ejemplo de salida:**

```
Device type: general purpose
Running: Linux 5.X
OS CPE: cpe:/o:linux:linux_kernel:5.4
OS details: Linux 5.4.0-26-generic
Network Distance: 1 hop
```

**Limitaciones:**
- Requiere privilegios de administrador
- No es 100% exacto (especialmente detras de NAT, balanceadores o firewalls)
- Sistemas muy parcheados o personalizados pueden engañar al fingerprinting
- Se necesita al menos un puerto abierto y uno cerrado para mejor precision

### 7. Scripts NSE (Nmap Scripting Engine)

NSE es una de las caracteristicas mas potentes de Nmap. Permite ejecutar scripts escritos en Lua para automatizar tareas.

#### Categorias de scripts

| Categoria | Descripcion |
|-----------|-------------|
| **auth** | Pruebas de autenticacion (credenciales por defecto) |
| **default** | Scripts basicos que se ejecutan con `-sC` |
| **discovery** | Descubrimiento de informacion adicional |
| **dos** | Pruebas de Denegacion de Servicio (cuidado!) |
| **exploit** | Exploits para vulnerabilidades conocidas |
| **fuzzer** | Pruebas de fuzzing (envio de datos aleatorios) |
| **intrusive** | Scripts que pueden ser detectados o causar impacto |
| **malware** | Deteccion de malware y backdoors |
| **safe** | Scripts seguros (no causan dano ni son intrusivos) |
| **version** | Extension de deteccion de versiones |
| **vuln** | Deteccion de vulnerabilidades conocidas |

#### Ejemplos de uso de NSE

**Escaneo de vulnerabilidades:**
```
nmap --script=vuln 192.168.1.10
```
Este comando ejecuta todos los scripts de la categoria "vuln". Busca vulnerabilidades conocidas como:
- EternalBlue (MS17-010)
- Shellshock
- Slowloris
- Heartbleed

**Enumeracion web:**
```
nmap --script=http-enum 192.168.1.10
```
Enumera directorios y archivos comunes en servidores web (robots.txt, admin, login, etc.)

**Enumeracion SMB (compartidos Windows):**
```
nmap --script=smb-enum-shares 192.168.1.10
```
Enumera los recursos compartidos de una maquina Windows (\\equipo\compartido).

**Escaneo de credenciales por defecto:**
```
nmap --script=ftp-brute 192.168.1.10
```
Prueba credenciales comunes en FTP.

**Scripts personalizados:**
```
nmap --script=/ruta/a/mi-script.nse 192.168.1.10
```

#### Scripts de discovery utiles

```
nmap --script=whois-domain ejemplo.com
nmap --script=dns-brute ejemplo.com
nmap --script=http-headers 192.168.1.10
```

### 8. Opciones de salida

Nmap puede guardar los resultados en varios formatos:

```
nmap -oN resultado.txt 192.168.1.10    # Formato normal (legible)
nmap -oX resultado.xml 192.168.1.10    # Formato XML (procesable)
nmap -oG resultado.gnmap 192.168.1.10  # Formato "grepable" (para scripts)
nmap -oS resultado.txt 192.168.1.10    # Formato "script kiddie" (divertido)
nmap -oA resultado 192.168.1.10        # Todos los formatos (-oN, -oX, -oG)
```

**Ver en pantalla y guardar:**
```
nmap -v -oN resultado.txt 192.168.1.10   # -v verbose, muestra en pantalla
```

### 9. Ejemplos practicos combinados

**Escaneo completo de un host (lento, exhaustivo):**
```
nmap -sS -sV -O -p- 192.168.1.10
```
Esto escanea los 65535 puertos TCP con SYN scan, detecta versiones de servicios y sistema operativo. Es muy completo pero puede tomar horas.

**Escaneo rapido de una red completa:**
```
nmap -sS -sV --top-ports 100 192.168.1.0/24
```
Escanea solo los 100 puertos mas comunes en todos los hosts de la red. Rapido y util.

**Escaneo sin fase de ping:**
```
nmap -Pn -sS -sV 192.168.1.10
```
Asume que el host esta activo y va directo a escanear puertos. Util si el firewall bloquea ICMP.

**Escaneo sigiloso con scripts:**
```
nmap -sS -sV -sC 192.168.1.10
```
`-sC` equivale a `--script=default`, ejecuta los scripts basicos de NSE.

### 10. Escaneo sigiloso (evasion de firewalls/IDS)

Cuando escaneas un sistema protegido, los firewalls o IDS pueden detectar y bloquear tu escaneo. Nmap ofrece tecnicas para evadir estas defensas:

**Fragmentacion (`-f`):**
Divide los paquetes en fragmentos mas pequenos para evadir firewalls que no reensamblan fragmentos:
```
nmap -f 192.168.1.10
```

**Decoy (senuelos, `-D`):**
Anade direcciones IP falsas como origen para confundir al objetivo:
```
nmap -D RND:10 192.168.1.10
```
Esto genera 10 direcciones IP aleatorias como senuelo. El destino vera 11 escaneos simultaneos.

**Spoofing de MAC (`--spoof-mac`):**
Falsifica la direccion MAC (util en redes WiFi donde hay filtrado por MAC):
```
nmap --spoof-mac Cisco 192.168.1.10
```

**ACK scan (`-sA`):**
El escaneo ACK no determina si un puerto esta abierto, sino si esta filtrado. Util para mapear reglas de firewall:
```
nmap -sA 192.168.1.10
```

**Puerto fuente especifico (`--source-port`):**
Algunos firewalls confian en trafico que viene de ciertos puertos (ej: 53 DNS, 20 FTP):
```
nmap --source-port 53 192.168.1.10
```

**Timing (velocidad):**
Controla la velocidad del escaneo para evitar saturar la red o ser detectado:
```
nmap -T0 192.168.1.10   # Paranoid (muy lento, evade IDS)
nmap -T1 192.168.1.10   # Sneaky (sigiloso)
nmap -T2 192.168.1.10   # Polite (educado, usa poco ancho de banda)
nmap -T3 192.168.1.10   # Normal (por defecto)
nmap -T4 192.168.1.10   # Aggressive (agresivo, rapido)
nmap -T5 192.168.1.10   # Insane (muy rapido, puede perder paquetes)
```

### 11. Interpretacion de resultados

#### Tabla de puertos y servicios comunes

| Puerto | Protocolo | Servicio | Peligro si abierto |
|--------|-----------|----------|--------------------|
| 21 | TCP | FTP | Alto: transferencia sin cifrar, credenciales en texto plano |
| 22 | TCP | SSH | Medio: si version es antigua o credenciales debiles |
| 23 | TCP | Telnet | Alto: todo en texto plano, evitable usar SSH |
| 25 | TCP | SMTP | Medio: servidor de correo, posible relay abierto |
| 53 | TCP/UDP | DNS | Bajo si es resolutor; alto si permite transferencia de zona |
| 80 | TCP | HTTP | Bajo si es web publico; alto si es interno sin cifrar |
| 110 | TCP | POP3 | Alto: correo sin cifrar |
| 143 | TCP | IMAP | Alto: correo sin cifrar |
| 443 | TCP | HTTPS | Bajo (cifrado) |
| 445 | TCP | SMB | Alto: vulnerabilidades como EternalBlue |
| 1433 | TCP | MSSQL | Alto: base de datos expuesta |
| 3306 | TCP | MySQL | Alto: base de datos expuesta |
| 3389 | TCP | RDP | Medio-Alto: ataques de fuerza bruta, BlueKeep |
| 5432 | TCP | PostgreSQL | Alto: base de datos expuesta |
| 5900 | TCP | VNC | Alto: si no tiene contrasena |
| 6379 | TCP | Redis | Alto: si no tiene autenticacion |
| 8080 | TCP | HTTP-Proxy | Medio: proxy abierto, tunneling |
| 27017 | TCP | MongoDB | Alto: si no tiene autenticacion |

#### Que hacer con los resultados

1. **Identificar puertos abiertos innecesarios:** Si ves FTP (21) abierto y no necesitas FTP, deberias cerrarlo
2. **Actualizar servicios con versiones antiguas:** Apache 2.2, OpenSSH 6.x, etc. necesitan actualizacion
3. **Revisar servicios peligrosos:** Telnet (23), SMB (445), RDP (3389) expuestos a Internet son muy riesgosos
4. **Documentar:** Crear un inventario de servicios por cada host
5. **Corregir configuraciones:** Por ejemplo, si MySQL (3306) esta expuesto a toda la red cuando solo deberia ser accesible desde localhost
6. **Monitorear cambios:** Repetir el escaneo periodicamente para detectar nuevos servicios no autorizados

### 12. Herramientas complementarias

**Zenmap:**
Interfaz grafica oficial de Nmap. Facilita el uso sin recordar comandos:
- Perfiles de escaneo predefinidos (Quick Scan, Intense Scan, etc.)
- Visualizacion de la topologia de red
- Comparacion de resultados de escaneos anteriores

```
zenmap
```

**RustScan:**
Escaneo ultra-rapido escrito en Rust. Escanea todos los puertos en segundos y luego pasa el resultado a Nmap para deteccion de versiones:
```
rustscan -a 192.168.1.10
```

**Masscan:**
Escanea millones de IPs por segundo. Util para escaneos masivos de Internet:
```
masscan 10.0.0.0/8 -p80,443 --rate=10000
```

### 13. Ejercicio 1 - Escaneo basico

**Enunciado:** Escanear tu propia red local (tu PC y otros dispositivos) para descubrir hosts activos y puertos abiertos.

**Requisitos:** Tener Nmap instalado. Trabajar solo en tu propia red.

##### Solucion

**Paso 1:** Descubrir tu propia IP y la red local.

En Windows:
```
ipconfig
```
Busca la linea "IPv4 Address" (ej: 192.168.1.50) y "Subnet Mask" (ej: 255.255.255.0). La red es 192.168.1.0/24.

En Linux:
```
ip addr show
```

**Paso 2:** Descubrir hosts activos en tu red.

```
nmap -sn 192.168.1.0/24
```

**Ejemplo de salida esperada:**

```
Starting Nmap 7.95 ( https://nmap.org ) at 2026-06-25 10:00
Nmap scan report for 192.168.1.1
Host is up (0.0012s latency).
MAC Address: 00:11:22:33:44:55 (Router)
Nmap scan report for 192.168.1.50
Host is up (0.0001s latency).
MAC Address: AA:BB:CC:DD:EE:FF (TUF Gaming)
Nmap scan report for 192.168.1.100
Host is up (0.0034s latency).
MAC Address: 11:22:33:44:55:66 (Raspberry Pi Foundation)
Nmap done: 256 IP addresses (3 hosts up) scanned in 2.45s
```

**Interpretacion:**
- 192.168.1.1: Tu router (MAC de fabricante de router)
- 192.168.1.50: Tu PC
- 192.168.1.100: Un Raspberry Pi (por el fabricante de MAC)

**Paso 3:** Escanear puertos de tu propio PC.

```
nmap -p 1-1000 127.0.0.1
```

**Ejemplo de salida:**

```
PORT     STATE SERVICE
22/tcp   open  ssh
80/tcp   open  http
443/tcp  open  https
3306/tcp open  mysql
```

**Paso 4:** Detectar sistema operativo.

```
nmap -O 127.0.0.1
```

**Ejemplo de salida:**

```
Device type: general purpose
Running: Linux 5.X
OS details: Linux 5.15.0-91-generic
```

**Paso 5:** Escaneo completo de tu PC (puertos comunes).

```
nmap -sS -sV localhost
```

**Ejemplo de salida:**

```
PORT     STATE SERVICE     VERSION
22/tcp   open  ssh         OpenSSH 8.9p1 Ubuntu 3ubuntu0.6
80/tcp   open  http        Apache httpd 2.4.52
443/tcp  open  ssl/http    Apache httpd 2.4.52
3306/tcp open  mysql       MySQL 8.0.35-0ubuntu0.22.04.1
```

### 14. Ejercicio 2 - Escaneo de servicios

**Enunciado:** Escanear un servidor web (real o virtual) para identificar servicios, versiones y posibles vulnerabilidades.

##### Solucion

**Paso 1:** Escanear puertos y servicios.

```
nmap -sS -sV -p 1-10000 192.168.1.10
```

**Ejemplo de salida:**

```
PORT     STATE SERVICE     VERSION
22/tcp   open  ssh         OpenSSH 7.6p1 Ubuntu 4ubuntu0.7
80/tcp   open  http        Apache httpd 2.4.29
443/tcp  open  ssl/http    Apache httpd 2.4.29
3306/tcp open  mysql       MySQL 5.7.42
```

**Paso 2:** Investigar vulnerabilidades de las versiones.

**OpenSSH 7.6p1:**
- Buscar: "OpenSSH 7.6 vulnerabilities"
- CVE-2018-15473: User enumeration (permite saber que usuarios existen)
- CVE-2019-6109: Keyboard-interactive authentication vulnerable to timing attacks
- Recomendacion: Actualizar a 8.0+

**Apache 2.4.29:**
- Buscar: "Apache 2.4.29 vulnerabilities"
- CVE-2021-41773 (en realidad afecta 2.4.49, pero verificar)
- CVE-2021-39275: ap_escape_quotes buffer overflow
- Recomendacion: Actualizar a 2.4.54+

**MySQL 5.7.42:**
- Version relativamente reciente (5.7 todavia tiene soporte)
- Verificar si hay CVE criticos para esa version especifica

**Paso 3:** Ejecutar scripts de enumeracion especificos.

```
nmap --script=http-enum 192.168.1.10
```

**Ejemplo de salida:**

```
PORT   STATE SERVICE
80/tcp open  http
| http-enum:
|   /admin/: Possible admin folder
|   /robots.txt: Robots file
|   /wp-content/: WordPress content directory
|   /login.php: Login page
```

**Paso 4:** Verificar headers de seguridad.

```
nmap --script=http-headers 192.168.1.10
```

Revisa si faltan headers de seguridad importantes:
- `Strict-Transport-Security`: Para forzar HTTPS
- `X-Content-Type-Options`: Para evitar MIME sniffing
- `X-Frame-Options`: Para evitar clickjacking
- `Content-Security-Policy`: Para limitar recursos

### 15. Ejercicio 3 - NSE Scripts

**Enunciado:** Ejecutar scripts de vulnerabilidad (categoria vuln) contra un objetivo e interpretar los resultados.

##### Solucion

**Paso 1:** Ejecutar escaneo de vulnerabilidades.

```
nmap --script=vuln 192.168.1.10
```

**Ejemplo de salida (parcial):**

```
PORT   STATE SERVICE
22/tcp open  ssh
| ssh-vuln-cve78: 
|   VULNERABLE:
|   OpenSSH 7.6: Arbitrary file read
|     State: LIKELY VULNERABLE
|     IDs: CVE-2018-15473
|     Description: OpenSSH before 7.8 is vulnerable to user enumeration.
|     
80/tcp open  http
| http-vuln-cve2021-41773: 
|   VULNERABLE:
|   Apache Path Traversal
|     State: LIKELY VULNERABLE
|     IDs: CVE-2021-41773
|     Description: Apache HTTP Server 2.4.49 has a path traversal vulnerability.
|     
| http-slowloris-check: 
|   VULNERABLE:
|   Slowloris DOS attack
|     State: LIKELY VULNERABLE
|     Description: Apache is vulnerable to Slowloris DoS attack.
```

**Paso 2:** Interpretar resultados.

- **LIKELY VULNERABLE:** El script encontro indicios de que la vulnerabilidad existe, pero no esta 100% confirmado
- **VULNERABLE (confirmed):** El confirmo la vulnerabilidad exitosamente
- **Falsos positivos:** A veces Nmap reporta vulnerabilidades que no son reales. Por ejemplo, Slowloris puede reportarse como vulnerable en configuraciones donde el timeout esta configurado correctamente pero el script no espero lo suficiente

**Paso 3:** Verificar falsos positivos manualmente.

Para CVE-2021-41773 (path traversal en Apache):
```
curl -v http://192.168.1.10/cgi-bin/.%2e/%2e%2e/etc/passwd
```

Si el servidor es vulnerable, devolvera el contenido de /etc/passwd. Si no, devolvera 403 Forbidden o 404 Not Found.

**Paso 4:** Documentar los hallazgos.

Crear una tabla con:
| Vulnerabilidad | Severidad | Remedio |
|---|---|---|
| CVE-2018-15473 | Media | Actualizar OpenSSH a 7.8+ |
| CVE-2021-41773 | Alta | Actualizar Apache a 2.4.50+ |
| Slowloris | Media | Configurar mod_reqtimeout en Apache |

### 16. Ejercicio 4 - Escaneo de red completa

**Enunciado:** Escanear la red 192.168.1.0/24 (o la del laboratorio) y mapear todos los dispositivos con sus servicios. Crear un inventario en tabla.

##### Solucion

**Paso 1:** Descubrir todos los hosts activos.

```
nmap -sn 192.168.1.0/24
```

**Ejemplo de resultado:**

```
Hosts descubiertos:
- 192.168.1.1 (Router)
- 192.168.1.10 (Servidor Ubuntu)
- 192.168.1.20 (PC Windows)
- 192.168.1.30 (Raspberry Pi)
- 192.168.1.50 (Laptop)
- 192.168.1.100 (Servidor Web)
```

**Paso 2:** Escanear puertos y servicios en cada host.

```
nmap -sS -sV --top-ports 100 192.168.1.1-100
```

**Paso 3:** Crear el inventario en tabla.

```
nmap -sS -sV -O --top-ports 100 -oN inventario.txt 192.168.1.0/24
```

**Paso 4:** Tabla de resultados del inventario.

| IP | Hostname | SO Detectado | Puertos Abiertos | Servicios |
|---|---|---|---|---|
| 192.168.1.1 | router.local | Linux (RouterOS) | 22, 80, 443, 53, 8291 | SSH, HTTP, HTTPS, DNS, Winbox |
| 192.168.1.10 | ubuntu-server | Linux 5.4 | 22, 80, 443, 3306 | SSH, Apache 2.4.41, MySQL 8.0 |
| 192.168.1.20 | PC-JUAN | Windows 10 Pro | 135, 139, 445, 3389 | RPC, SMB, RDP |
| 192.168.1.30 | raspberrypi | Linux 5.10 | 22, 80 | SSH, Apache 2.4.52 |
| 192.192.1.50 | laptop-admin | Windows 11 | 22, 3389 | SSH, RDP |
| 192.168.1.100 | webserver | Linux 5.15 | 22, 80, 443 | SSH, Nginx 1.24 |

**Paso 5:** Analisis de seguridad del inventario.

Observaciones:
- **PC-JUAN (192.168.1.20):** Tiene puerto 3389 (RDP) abierto. Si esta expuesto a Internet, es un riesgo. Deberia estar solo accesible por VPN.
- **Raspberry Pi (192.168.1.30):** Tiene puerto 80 abierto. Verificar que no sea configuracion por defecto.
- **Router:** Tiene servicios de administracion web (80, 443, 8291). El puerto 8291 (Winbox) es especifico de MikroTik. Cambiar credenciales por defecto y limitar acceso por IP.

### 17. Preguntas y Respuestas

#### Pregunta 1
**Cual es la diferencia entre SYN scan (-sS) y Connect scan (-sT)?**

**Respuesta:** La diferencia principal es como manejan la conexion TCP. En SYN scan (-sS), Nmap envia el paquete SYN inicial y si recibe SYN-ACK responde inmediatamente con RST, sin completar el three-way handshake. Se llama "semi-abierto" (half-open). No completa la conexion, por lo que es mas rapido y menos detectable. Requiere privilegios de administrador. En Connect scan (-sT), Nmap completa el three-way handshake completo (SYN, SYN-ACK, ACK) y luego envia RST para cerrar. Es mas lento, mas detectable (queda en logs de aplicaciones), pero no requiere privilegios especiales.

#### Pregunta 2
**Que significa que un puerto aparezca como "filtered"?**

**Respuesta:** Significa que un firewall, filtro de paquetes u otro dispositivo de red esta bloqueando el acceso a ese puerto. Nmap no puede determinar si el puerto esta abierto o cerrado porque los paquetes no llegan a su destino o las respuestas son bloqueadas. Generalmente, un puerto filtered se debe a: (1) un firewall que descarta los paquetes (drop), (2) un filtro que envia respuestas ICMP unreachable, (3) un IDS/IPS que bloquea el escaneo, (4) reglas de ACL en un router. Para intentar superar esto, se pueden usar tecnicas como fragmentacion (-f), decoys (-D) o cambiar el timing (-T0, -T1).

#### Pregunta 3
**Como detecta Nmap el sistema operativo remoto?**

**Respuesta:** Nmap usa una tecnica llamada "TCP/IP stack fingerprinting". Cada sistema operativo implementa el stack TCP/IP de forma ligeramente diferente. Nmap envia una serie de hasta 16 paquetes especiales (SYN, FIN, NULL, Xmas, ACK, etc.) y analiza las respuestas. Analiza parametros como: TTL inicial (64 en Linux, 128 en Windows, 255 en equipos Cisco), tamano de ventana TCP (window size), opciones TCP anunciadas (MSS, Window Scale, Timestamp, SACK, etc.), comportamiento ante paquetes malformados (SYN a puerto cerrado, FIN sin SYN, etc.), y patrones de retransmision. Luego compara estas respuestas con su base de datos de firmas (nmap-os-db) para encontrar la coincidencia mas cercana.

#### Pregunta 4
**Que es NSE (Nmap Scripting Engine) y para que sirve?**

**Respuesta:** NSE es un motor de scripts integrado en Nmap que permite automatizar tareas de auditoria mediante scripts escritos en Lua. Sirve para: (1) Deteccion de vulnerabilidades conocidas (categoria vuln), (2) Enumeracion de recursos (categoria discovery, como http-enum que lista directorios web), (3) Pruebas de autenticacion (categoria auth, como pruebas de credenciales por defecto), (4) Explotacion de vulnerabilidades (categoria exploit), (5) Deteccion de malware (categoria malware). Los scripts se organizan en categorias y se ejecutan con --script=categoria. Actualmente hay mas de 600 scripts incluidos en Nmap.

#### Pregunta 5
**Como evitar ser detectado al escanear una red?**

**Respuesta:** Para evitar ser detectado, se pueden usar varias tecnicas, pero ninguna es 100% efectiva: (1) Usar timing lento (-T0 o -T1) para no saturar la red y evitar alarmas por velocidad, (2) Fragmentar paquetes (-f) para evadir firewalls que no reensamblan, (3) Usar decoys (-D RND:5) para mezclar tu IP con senuelos, (4) Escanear desde un solo puerto especifico (--source-port 53) que algunos firewalls no filtran, (5) Usar escaneos TCP ACK (-sA) en lugar de SYN (-sS) para parecer trafico normal, (6) Spoofear la direccion MAC (--spoof-mac), (7) Usar proxys o VPNs para ocultar la IP real. Importante: incluso con todas estas tecnicas, un IDS/IPS bien configurado puede detectar el escaneo. La unica forma "segura" de no ser detectado es no escanear.

#### Pregunta 6
**Que es Zenmap y en que se diferencia de Nmap por linea de comandos?**

**Respuesta:** Zenmap es la interfaz grafica oficial de Nmap. Las principales diferencias son: (1) No requiere recordar comandos: tiene perfiles predefinidos (Quick Scan, Intense Scan, Ping Scan, etc.), (2) Muestra los resultados en formato visual, incluyendo un mapa de topologia de red, (3) Permite comparar resultados de diferentes escaneos (funcion "Compare Results"), (4) Almacena el historial de escaneos, (5) Es util para principiantes o para quienes prefieren interfaz grafica. En el fondo, Zenmap ejecuta los mismos comandos Nmap que usarias en terminal, solo que los construye automaticamente segun las opciones que selecciones. Para uso profesional, la linea de comandos ofrece mas control y flexibilidad, ademas de poder automatizar escaneos con scripts.

---

## Tarea / Lectura Recomendada

1. **Practicar:** Escanea tu propia red local con los comandos de esta clase. Identifica cuantos dispositivos hay, que puertos tienen abiertos y que sistemas operativos usan
2. **Practicar:** Instala una maquina virtual vulnerable (Metasploitable 2 o DVWA) y practica todos los tipos de escaneo aprendidos
3. **Practicar:** Ejecuta `nmap --script=vuln` contra Metasploitable 2 y documenta las vulnerabilidades encontradas
4. **Leer:** "Nmap Network Scanning" de Gordon Lyon (Fyodor) - el libro oficial de Nmap
5. **Leer:** Documentacion oficial de Nmap en https://nmap.org/docs.html
6. **Leer:** OWASP Testing Guide - capitulo sobre "Network Testing" (escaneo de puertos en pentesting)
7. **Explorar:** Prueba Zenmap (la interfaz grafica) para escaneos visuales
8. **Explorar:** Investiga RustScan como alternativa rapida a Nmap para escaneo inicial
9. **Ver:** Serie de videos "Nmap for Ethical Hackers" en YouTube (buscar en espanol o ingles)
10. **Advertencia:** NO escanees redes ajenas sin permiso explicito. Practica solo en tus propios equipos o en entornos de laboratorio autorizados
