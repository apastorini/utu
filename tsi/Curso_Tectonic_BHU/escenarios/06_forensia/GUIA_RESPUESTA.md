# GUIA DE RESPUESTA - ESCENARIO 06
# Analisis Forense Digital - Banco del Sol
# Curso Tectonic BHU Uruguay

---

## INDICE

1. [Fase 1: Adquisicion de Evidencia](#fase-1-adquisicion-de-evidencia)
2. [Fase 2: Analisis de Disco](#fase-2-analisis-de-disco)
3. [Fase 3: Analisis de Memoria](#fase-3-analisis-de-memoria)
4. [Fase 4: Analisis de Logs](#fase-4-analisis-de-logs)
5. [Fase 5: Reconstruccion de Linea de Tiempo](#fase-5-reconstruccion-de-linea-de-tiempo)
6. [Fase 6: Elaboracion de Informe Forense](#fase-6-elaboracion-de-informe-forense)

---

## FASE 1: ADQUISICION DE EVIDENCIA

### 1.1 Documentacion de la Escena

Antes de manipular cualquier evidencia digital, documentar la escena fisica:

```bash
# Tomar fotos de la estacion de trabajo (pantalla, teclado, conexiones)
# Documentar estado del sistema (si esta encendido, que muestra en pantalla)
# Anotar numero de serie del equipo y discos duros
# Registrar fecha, hora, y nombre del analista

# Si el equipo esta encendido, NO apagarlo aun
# Capturar informacion en vivo antes de apagar:
# - Capturar pantalla
# - Capturar procesos activos
# - Capturar conexiones de red
# - Capturar contenido de memoria
```

### 1.2 Captura de Evidencia en Vivo (si aplica)

Si el sistema esta encendido, capturar evidencia volatil primero:

```bash
# Capturar procesos activos
ps auxf > /evidence/volatile/process_tree.txt

# Capturar conexiones de red
netstat -tlnp > /evidence/volatile/netstat.txt
ss -tulnp > /evidence/volatile/sockets.txt

# Capturar contenido de memoria
# Usar LiME (Linux Memory Extractor)
insmod lime.ko "path=/evidence/memory_dump.lime format=lime"

# O usar dd si LiME no esta disponible
dd if=/dev/mem of=/evidence/memory_dump.raw bs=1M count=4096

# Capturar cache de ARP
arp -a > /evidence/volatile/arp_cache.txt

# Capturar tablas de enrutamiento
ip route > /evidence/volatile/routes.txt
route -n > /evidence/volatile/routes_legacy.txt
```

### 1.3 Creacion de Imagen Forense del Disco

```bash
# Crear directorio para la imagen
mkdir -p /evidence/disk_images

# Usar dc3dd (variante de dd con verificacion de hash integrada)
dc3dd if=/dev/sda of=/evidence/disk_images/workstation_disk_image.dd \
  hash=sha256 log=/evidence/disk_images/dc3dd.log

# O usar dd con calculo de hash separado
dd if=/dev/sda of=/evidence/disk_images/workstation_disk_image.dd \
  bs=4M status=progress conv=noerror,sync

# Calcular hash SHA256 de la imagen
sha256sum /evidence/disk_images/workstation_disk_image.dd \
  > /evidence/disk_images/workstation_disk_image.dd.sha256

# Calcular hash MD5 como referencia adicional
md5sum /evidence/disk_images/workstation_disk_image.dd \
  > /evidence/disk_images/workstation_disk_image.dd.md5

# Verificar que el hash coincide
cat /evidence/disk_images/workstation_disk_image.dd.sha256
# Salida esperada: <hash>  /evidence/disk_images/workstation_disk_image.dd

# Calcular hash del volcado de memoria
sha256sum /evidence/memory_dumps/workstation_memory.dump \
  > /evidence/memory_dumps/workstation_memory.dump.sha256
```

### 1.4 Montaje de Imagen en Modo Solo Lectura

```bash
# Crear directorio de montaje
mkdir -p /mnt/evidence/disk_image

# Montar imagen en modo solo lectura con loop device
mount -o ro,loop,noexec,nosuid \
  /evidence/disk_images/workstation_disk_image.dd \
  /mnt/evidence/disk_image

# Verificar que se monto correctamente
df -h /mnt/evidence/disk_image
ls -la /mnt/evidence/disk_image/

# Para montar una particion especifica
fdisk -l /evidence/disk_images/workstation_disk_image.dd

# Montar particion especifica (ejemplo: particion 1)
mount -o ro,loop,offset=1048576 \
  /evidence/disk_images/workstation_disk_image.dd \
  /mnt/evidence/disk_image
```

### 1.5 Cadena de Custodia

```bash
# Plantilla de Cadena de Custodia
cat > /evidence/chain_of_custody/caso_001_cadena_custodia.txt << 'EOF'
=================================================================
CADENA DE CUSTODIA DE EVIDENCIA DIGITAL
Banco del Sol - Escenario 06
=================================================================

CASO NRO: CASO-001
FECHA: [DD/MM/AAAA HH:MM]
ANALISTA: [Nombre del Analista]
EQUIPO: [Numero de Serie]

-----------------------------------------------------------------
EVIDENCIA ITEM 001
-----------------------------------------------------------------
Descripcion: Imagen de disco de estacion de trabajo
Tipo: Disco duro
Marca/Modelo: [Marca y modelo]
Numero de Serie: [Numero de serie]
Capacidad: 80GB
Sistema de Archivos: ext4

HASH SHA256: [Hash calculado]
HASH MD5: [Hash calculado]

Fecha y Hora de Adquisicion: [DD/MM/AAAA HH:MM:SS]
Metodo de Adquisicion: dc3dd
Herramienta: dc3dd 1.0+

Cadena de Custodia:
[DD/MM/AAAA HH:MM] - Recibido por: [Nombre]
[DD/MM/AAAA HH:MM] - Almacenado en: [Ubicacion]

Almacenamiento Actual:
Ubicacion: [Direccion fisica]
Acceso: [Quienes tienen acceso]
=================================================================
EOF
```

### 1.6 Consideraciones Legales

```bash
# En Uruguay, la adquisicion de evidencia digital esta regida por:
# - Ley 18.331 (Proteccion de Datos Personales)
# - Decreto 66/025 (Reglamentacion de la Ley 18.331)
# - Ley 19.520 (Delitos Informaticos)

# Puntos clave:
# 1. Autorizacion: Obtener autorizacion escrita antes de realizar la adquisicion
# 2. Proporcionalidad: Solo adquirir evidencia relevante al caso
# 3. Integridad: Mantener hashes verificables en todo momento
# 4. Cadena de custodia: Documentar cada transferencia de evidencia
# 5. Almacenamiento: Guardar evidencia en lugar seguro con control de acceso
# 6. Confidencialidad: Los datos personales deben ser tratados segun Ley 18.331

# Para reportes a CERTuy/URCDP:
# - Contactar a CERTuy (cert@certuy.uy) para incidentes graves
# - Documentar todos los pasos del analisis
# - Preservar evidencia para posible procedimiento judicial
```

---

## FASE 2: ANALISIS DE DISCO

### 2.1 Examinar Estructura de Archivos

```bash
# Montar imagen en modo solo lectura
mount -o ro,loop /evidence/disk_images/workstation_disk_image.dd /mnt/evidence/disk_image

# Listar contenido del disco
ls -la /mnt/evidence/disk_image/

# Buscar archivos ocultos
find /mnt/evidence/disk_image -name ".*" -type f 2>/dev/null

# Buscar archivos en /tmp (donde el atacante dejo artefactos)
ls -la /mnt/evidence/disk_image/tmp/.* 2>/dev/null

# Usar fls (file listing) de The Sleuth Kit
fls -r -d /evidence/disk_images/workstation_disk_image.dd
```

### 2.2 Identificar Archivos Sospechosos

```bash
# Buscar archivos con permisos SUID/SGID
find /mnt/evidence/disk_image -perm -4000 -type f 2>/dev/null
find /mnt/evidence/disk_image -perm -2000 -type f 2>/dev/null

# Buscar archivos ejecutables en directorios inusuales
find /mnt/evidence/disk_image/tmp -type f -executable 2>/dev/null
find /mnt/evidence/disk_image/var/tmp -type f -executable 2>/dev/null

# Buscar archivos con nombres ocultos (punto al inicio)
find /mnt/evidence/disk_image -name ".*" -type f 2>/dev/null

# Buscar archivos modificados recientemente (ultimas 48 horas)
find /mnt/evidence/disk_image -mtime -2 -type f 2>/dev/null

# Buscar archivos creados por el usuario root en /tmp
find /mnt/evidence/disk_image/tmp -user root -type f 2>/dev/null
```

### 2.3 Artefactos Especificos del Ataque

```bash
# Buscar webshell
find /mnt/evidence/disk_image -name "*.php" -type f 2>/dev/null
ls -la /mnt/evidence/disk_image/var/www/html/banco_del_sol/uploads/

# Verificar contenido de webshell
cat /mnt/evidence/disk_image/var/www/html/banco_del_sol/uploads/cmd.php
# Esperado: PHP con shell_exec() y fsockopen()

# Buscar usuario backdoor en /etc/passwd
grep "sysadmin_back" /mnt/evidence/disk_image/etc/passwd
# Esperado: sysadmin_back:x:1099:1099:System Administrator Backdoor:/home/sysadmin_back:/bin/bash

# Verificar /etc/passwd para cambios no autorizados
cat /mnt/evidence/disk_image/etc/passwd
# Comparar con version original del sistema

# Buscar cron jobs sospechosos
ls -la /mnt/evidence/disk_image/etc/cron.d/
cat /mnt/evidence/disk_image/etc/cron.d/backdoor
# Esperado: */5 * * * * root /tmp/.system_backup.sh > /dev/null 2>&1

# Verificar /etc/hosts para dominios C2
grep "172.16.0.100" /mnt/evidence/disk_image/etc/hosts
# Esperado: 172.16.0.100 c2.bancodelsol-internal.com update.bancodelsol.com

# Buscar archivos de datos exfiltrados
ls -la /mnt/evidence/disk_image/tmp/.data_archive.tar.gz
ls -la /mnt/evidence/disk_image/tmp/.stolen_data.txt
ls -la /mnt/evidence/disk_image/tmp/.stolen_data2.txt
cat /mnt/evidence/disk_image/tmp/.data_archive.tar.gz

# Verificar scripts del atacante
cat /mnt/evidence/disk_image/tmp/.system_backup.sh
# Esperado: Script de reverse shell a 172.16.0.100:4444

cat /mnt/evidence/disk_image/tmp/.network_scan.sh
cat /mnt/evidence/disk_image/tmp/.collect_data.sh

# Verificar webshell en tmp
cat /mnt/evidence/disk_image/tmp/.hidden_shell.php
```

### 2.4 Analisis con Sleuth Kit

```bash
# Listar todos los archivos del disco
fls -r -p /evidence/disk_images/workstation_disk_image.dd > /evidence/analysis/file_listing.txt

# Buscar archivos eliminados (inodes no referenciados)
fls -r -d /evidence/disk_images/workstation_disk_image.dd

# Analizar inodos
ils -e /evidence/disk_images/workstation_disk_image.dd

# Buscar archivos con strings interesantes
strings /evidence/disk_images/workstation_disk_image.dd | grep -i "password"
strings /evidence/disk_images/workstation_disk_image.dd | grep -i "172.16.0.100"
strings /evidence/disk_images/workstation_disk_image.dd | grep -i "sysadmin_back"

# Analizar sistema de archivos
fsstat /evidence/disk_images/workstation_disk_image.dd
```

### 2.5 Timeline Analysis con mactime

```bash
# Crear timeline usando mactime (The Sleuth Kit)
# Primero necesitamos los body files de ils
ils -e -m /evidence/disk_images/workstation_disk_image.dd > /evidence/analysis/ils_output.txt

# O usar fls para generar body file
fls -r -m "/" /evidence/disk_images/workstation_disk_image.dd > /evidence/analysis/body.txt

# Generar timeline con mactime
mactime -b /evidence/analysis/body.txt -d > /evidence/analysis/timeline.csv

# Filtrar eventos de las ultimas 24 horas
mactime -b /evidence/analysis/body.txt -d -z UTC | tail -100

# Buscar eventos especificos en la timeline
grep "sysadmin_back" /evidence/analysis/timeline.csv
grep "backdoor" /evidence/analysis/timeline.csv
grep "172.16.0.100" /evidence/analysis/timeline.csv
```

### 2.6 Recuperacion de Archivos Eliminados

```bash
# Usar photorec para recuperar archivos
photorec /evidence/disk_images/workstation_disk_image.dd

# O usar foremost
foremost -i /evidence/disk_images/workstation_disk_image.dd -o /evidence/recovery/

# Usar testdisk para analizar particiones
testdisk /evidence/disk_images/workstation_disk_image.dd
```

### 2.7 Analisis de Artefactos de Navegador

```bash
# Buscar archivos de Firefox
find /mnt/evidence/disk_image -path "*firefox*" -name "places.sqlite" 2>/dev/null
find /mnt/evidence/disk_image -path "*firefox*" -name "cookies.sqlite" 2>/dev/null
find /mnt/evidence/disk_image -path "*firefox*" -name "history.sqlite" 2>/dev/null

# Analizar base de datos SQLite de historial
sqlite3 /mnt/evidence/disk_image/home/maria.garcia/.mozilla/firefox/places.sqlite \
  "SELECT url, title, visit_count, last_visit_date FROM moz_places;"

# Buscar archivos de Chrome/Chromium
find /mnt/evidence/disk_image -path "*chrome*" -name "History" 2>/dev/null
find /mnt/evidence/disk_image -path "*chromium*" -name "History" 2>/dev/null
```

### 2.8 Analisis de Archivos de Email

```bash
# Buscar archivos de email
find /mnt/evidence/disk_image -name "*.eml" -o -name "*.pst" -o -name "*.mbox" 2>/dev/null

# Buscar directorio de Thunderbird
find /mnt/evidence/disk_image -path "*thunderbird*" -name "*.msf" 2>/dev/null

# Analizar archivos mbox
find /mnt/evidence/disk_image -name "*.mbox" -exec grep -l "suspicious" {} \;
```

---

## FASE 3: ANALISIS DE MEMORIA

### 3.1 Identificar Sistema Operativo

```bash
# Identificar el SO del volcado de memoria
volatility -f /evidence/memory_dumps/workstation_memory.dump imageinfo
# Salida esperada: Suggestes: Linux profile

# O usar Volatility 3
volatility3 -f /evidence/memory_dumps/workstation_memory.dump linux.info
```

### 3.2 Analisis de Procesos

```bash
# Listar procesos (Volatility 2)
volatility -f /evidence/memory_dumps/workstation_memory.dump \
  --profile=LinuxProfile pslist

# Listar procesos en formato arbol
volatility -f /evidence/memory_dumps/workstation_memory.dump \
  --profile=LinuxProfile pstree

# Buscar procesos ocultos
volatility -f /evidence/memory_dumps/workstation_memory.dump \
  --profile=LinuxProfile psxview

# Volatility 3
volatility3 -f /evidence/memory_dumps/workstation_memory.dump \
  linux.pslist
volatility3 -f /evidence/memory_dumps/workstation_memory.dump \
  linux.pstree
```

### 3.3 Analisis de Red

```bash
# Escanear conexiones de red activas
volatility -f /evidence/memory_dumps/workstation_memory.dump \
  --profile=LinuxProfile linux_netscan

# Volatility 3
volatility3 -f /evidence/memory_dumps/workstation_memory.dump \
  linux.netscan

# Buscar conexiones establecidas
volatility -f /evidence/memory_dumps/workstation_memory.dump \
  --profile=LinuxProfile linux_netscan | grep ESTABLISHED

# Salida esperada:
# 10.10.2.50:4444  -> 172.16.0.100:9999  ESTABLISHED  (reverse shell)
# 10.10.2.50:4445  -> 172.16.0.100:8080  ESTABLISHED  (nc)
# 10.10.2.50:22    <- 10.10.1.10:44556   ESTABLISHED  (SSH)
```

### 3.4 Analisis de Archivos en Memoria

```bash
# Escanear archivos en memoria
volatility -f /evidence/memory_dumps/workstation_memory.dump \
  --profile=LinuxProfile linux_filescan

# Volatility 3
volatility3 -f /evidence/memory_dumps/workstation_memory.dump \
  linux.filescan

# Buscar archivos sospechosos
volatility -f /evidence/memory_dumps/workstation_memory.dump \
  --profile=LinuxProfile linux_filescan | grep "/tmp/"

# Buscar scripts del atacante
volatility -f /evidence/memory_dumps/workstation_memory.dump \
  --profile=LinuxProfile linux_filescan | grep -E "\.(sh|php|py)$"
```

### 3.5 Extraccion de Procesos

```bash
# Volcar un proceso especifico
volatility -f /evidence/memory_dumps/workstation_memory.dump \
  --profile=LinuxProfile linux_procdump -p 12345 -D /evidence/analysis/processes/

# Volcar todos los procesos
volatility -f /evidence/memory_dumps/workstation_memory.dump \
  --profile=LinuxProfile linux_procdump -D /evidence/analysis/processes/

# Analizar binarios extraidos
file /evidence/analysis/processes/pid.12345.* 
strings /evidence/analysis/processes/pid.12345.* | head -50
```

### 3.6 Extraccion de Credenciales

```bash
# Extraer hashes de password de memoria
volatility -f /evidence/memory_dumps/workstation_memory.dump \
  --profile=LinuxProfile linux_hashdump

# Volatility 3
volatility3 -f /evidence/memory_dumps/workstation_memory.dump \
  linux.hashdump

# Buscar credenciales en memoria
volatility -f /evidence/memory_dumps/workstation_memory.dump \
  --profile=LinuxProfile linux_envars | grep -i "pass"
```

### 3.7 Deteccion de Codigo Inyectado

```bash
# Verificar codigo inyectado en procesos
volatility -f /evidence/memory_dumps/workstation_memory.dump \
  --profile=LinuxProfile linux_proc_maps -p 12345

# Buscar DLLs/librerias sospechosas
volatility -f /evidence/memory_dumps/workstation_memory.dump \
  --profile=LinuxProfile linux_lsof

# Analizar heap de procesos
volatility -f /evidence/memory_dumps/workstation_memory.dump \
  --profile=LinuxProfile linux_heap -p 12345
```

---

## FASE 4: ANALISIS DE LOGS

### 4.1 Logs de Autenticacion (auth.log)

```bash
# Buscar intentos de login fallidos
grep "Failed password" /mnt/evidence/disk_image/var/log/auth.log
# Salida esperada: Intentos desde 203.0.113.50 y 198.51.100.23

# Buscar logins exitosos desde IPs externas
grep "Accepted password" /mnt/evidence/disk_image/var/log/auth.log
# Salida esperada: Login desde 10.10.1.10 (webserver comprometido)

# Buscar acciones de sudo
grep "sudo:" /mnt/evidence/disk_image/var/log/auth.log
# Salida esperada: sysadmin_back ejecutando comandos como root

# Buscar creacion de usuarios
grep "useradd\|adduser" /mnt/evidence/disk_image/var/log/auth.log

# Buscar sesiones SSH
grep "sshd:" /mnt/evidence/disk_image/var/log/auth.log

# Analizar auth.log.1 (rotado)
cat /mnt/evidence/disk_image/var/log/auth.log.1
# Salida esperada: Acceso a archivos sensibles via sudo
```

### 4.2 Logs del Servidor Web (Apache)

```bash
# Buscar SQL injection
grep "OR 1=1\|UNION SELECT\|DROP TABLE\|INSERT INTO" \
  /mnt/evidence/disk_image/var/log/apache2/access.log
# Salida esperada: GET /login.php' OR 1=1-- HTTP/1.1 200

# Buscar acceso a webshell
grep "cmd.php" /mnt/evidence/disk_image/var/log/apache2/access.log
# Salida esperada: GET /uploads/cmd.php?cmd=... HTTP/1.1 200

# Buscar upload de archivos
grep "POST /soporte.php" /mnt/evidence/disk_image/var/log/apache2/access.log

# Buscar IPs sospechosas
grep "172.16.0.100" /mnt/evidence/disk_image/var/log/apache2/access.log

# Analizar User-Agents inusuales
awk '{print $NF}' /mnt/evidence/disk_image/var/log/apache2/access.log | sort | uniq -c | sort -rn

# Buscar en error.log
cat /mnt/evidence/disk_image/var/log/apache2/error.log
# Salida esperada: Errores de SQL injection y PHP warnings
```

### 4.3 Logs del Sistema (syslog)

```bash
# Buscar eventos de firewall
grep "UFW BLOCK" /mnt/evidence/disk_image/var/log/syslog
# Salida esperada: Bloqueos desde 172.16.0.100

# Buscar servicios iniciados
grep "systemd.*Started" /mnt/evidence/disk_image/var/log/syslog

# Buscar actividad de cron
grep "CRON" /mnt/evidence/disk_image/var/log/syslog

# Buscar kernels panics o errores
grep "kernel.*error\|kernel.*panic" /mnt/evidence/disk_image/var/log/syslog
```

### 4.4 Logs de DNS

```bash
# Buscar queries DNS sospechosas
grep "query\|named" /mnt/evidence/disk_image/var/log/syslog

# Buscar dominios C2
grep "172.16.0.100" /mnt/evidence/disk_image/var/log/syslog
```

### 4.5 Logs de dpkg (Instalacion de Paquetes)

```bash
# Buscar instalacion de herramientas sospechosas
grep "netcat\|nmap\|nc\|socat\|cryptcat" /mnt/evidence/disk_image/var/log/dpkg.log
# Salida esperada: Instalacion de netcat-openbsd y nmap

# Buscar instalaciones recientes
grep "install" /mnt/evidence/disk_image/var/log/dpkg.log | tail -20
```

### 4.6 Logs de Base de Datos

```bash
# Si hay acceso a la base de datos PostgreSQL
# Conectar y examinar logs
psql -h 10.10.2.20 -U admin_banco -d banco_del_sol

# Buscar queries sospechosas
SELECT * FROM logs_acceso WHERE ip_origen = '10.10.1.10';
SELECT * FROM logs_acceso WHERE accion LIKE '%SELECT%';

# Buscar COPY commands (posible exfiltracion)
SELECT * FROM logs_acceso WHERE accion LIKE '%COPY%';
```

---

## FASE 5: RECONSTRUCCION DE LINEA DE TIEMPO

### 5.1 Crear Timeline Unificada

```bash
# Recopilar timestamps de todas las fuentes

# Timeline de archivos del disco
mactime -b /evidence/analysis/body.txt -d > /evidence/analysis/timeline_archivos.csv

# Timeline de logs del sistema
# Parsear auth.log
cat /mnt/evidence/disk_image/var/log/auth.log | \
  awk '{print $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11}' | \
  sort > /evidence/analysis/timeline_auth.csv

# Timeline de logs web
cat /mnt/evidence/disk_image/var/log/apache2/access.log | \
  awk '{print $4, $5, $6, $7, $8, $9}' | \
  sort > /evidence/analysis/timeline_web.csv

# Combinar todas las timelines
cat /evidence/analysis/timeline_archivos.csv \
    /evidence/analysis/timeline_auth.csv \
    /evidence/analysis/timeline_web.csv | \
  sort > /evidence/analysis/timeline_unificada.csv
```

### 5.2 Mapeo de Secuencia de Ataque

```bash
# Crear mapeo de ataque paso a paso
cat > /evidence/analysis/secuencia_ataque.txt << 'EOF'
SECUENCIA DEL ATAQUE - BANCO DEL SOL
=====================================

FASE 1: RECONOCIMIENTO (09/Jul/2024 22:15)
- IP: 172.16.0.100
- Accion: Escaneo de directorios via python-requests
- Directorios probados: /admin, /phpmyadmin, /wp-admin, /config, /.env, /server-status
- Resultado: Portal bancario identificado en /

FASE 2: EXPLORACION (10/Jul/2024 10:30)
- IP: 172.16.0.100
- Accion: SQL injection en login.php
- Payload: ' OR 1=1--
- Resultado: Acceso al portal como admin

FASE 3: INSTALACION DE WEBSHELL (10/Jul/2024 10:30)
- IP: 172.16.0.100
- Accion: Upload de webshell via soporte.php
- Archivo: /var/www/html/banco_del_sol/uploads/cmd.php
- Funcionalidad: Ejecucion de comandos remota

FASE 4: RECONOCIMIENTO VIA WEBSHELL (10/Jul/2024 10:30)
- IP: 172.16.0.100
- Comandos ejecutados:
  * id
  * whoami
  * cat /etc/passwd
  * uname -a
  * ls -la /var/www/

FASE 5: MOVIMIENTO LATERAL (10/Jul/2024 15:30)
- Origen: 10.10.1.10 (webserver)
- Destino: 10.10.2.50 (workstation)
- Metodo: SSH con credenciales maria.garcia
- Puerto: 44556

FASE 6: CREACION DE USUARIO BACKDOOR (10/Jul/2024 16:45)
- Accion: Creacion de usuario sysadmin_back
- Permisos: sudo NOPASSWD
- Ubicacion: /etc/passwd, /etc/sudoers.d/sysadmin_back

FASE 7: INSTALACION DE PERSISTENCIA (10/Jul/2024 16:45)
- Cron job: /etc/cron.d/backdoor (cada 5 minutos)
- Script: /tmp/.system_backup.sh (reverse shell)
- Script: /usr/local/bin/system_verify.sh (keepalive)

FASE 8: ACCESO A DATOS SENSIBLES (10/Jul/2024 16:50)
- Acceso a /etc/shadow
- Acceso a /etc/passwd
- Acceso a documentos de maria.garcia
- Acceso a credenciales de backup
- Acceso a configuracion del sistema

FASE 9: EXFILTRACION DE DATOS (10/Jul/2024 16:51)
- Archivos copiados a /tmp/
- Datos: Credenciales, configuracion, documentos
- Compresion: tar.gz en /tmp/.data_archive.tar.gz

FASE 10: BORRADO DE HUELLAS (10/Jul/2024 17:30)
- Logrotate forzado
- Historial de bash borrado
- Logs parcialmente truncados
- Timestamps modificados en archivos criticos
EOF
```

### 5.3 Identificar Sistemas Comprometidos

```bash
# Listar todos los sistemas afectados
cat > /evidence/analysis/sistemas_comprometidos.txt << 'EOF'
SISTEMAS COMPROMETIDOS
======================

1. WORKSTATION (10.10.2.50) - ESTACION DE TRABAJO
   - Usuario backdoor: sysadmin_back
   - Cron job persistente
   - Reverse shell activo
   - Datos exfiltrados

2. WEBSERVER (10.10.1.10) - SERVIDOR WEB
   - Webshell instalada: uploads/cmd.php
   - SQL injection explotada
   - Punto de entrada del atacante

3. ARCHIVOS COMPROMETIDOS EN WORKSTATION:
   - /etc/passwd (usuario backdoor)
   - /etc/hosts (dominio C2)
   - /etc/cron.d/backdoor (persistencia)
   - /tmp/*.sh (herramientas del atacante)
   - /tmp/*.php (webshell)
   - /var/log/* (logs modificados)

CREDENCIALES COMPROMETIDAS:
- maria.garcia / admin123 (SSH)
- admin_banco / B@nc0d3lSol_2024 (BD)
- web_user / W3b_U53r_2024 (BD)
- ops_reader / 0psR34d3r_2024 (BD)
- db_backup / B@ckup_DB#2024 (BD)
EOF
```

---

## FASE 6: ELABORACION DE INFORME FORENSE

### 6.1 Plantilla de Informe Forense

```bash
cat > /evidence/informes/informe_forense_caso_001.md << 'EOF'
# INFORME DE ANALISIS FORENSE DIGITAL
# CASO: CASO-001
# Banco del Sol

## RESUMEN EJECUTIVO

Fecha del informe: [DD/MM/AAAA]
Analista: [Nombre]
Equipo: [Numero de serie]
Cliente: Banco del Sol

### Hallazgos Principales

Se detecto una intrusion en la estacion de trabajo del departamento de
operaciones (workstation, IP 10.10.2.50). El atacante:

1. Exploto una vulnerabilidad de SQL injection en el portal web
2. Instalo una webshell para mantener acceso remoto
3. Se movio lateralmente a la estacion de trabajo via SSH
4. Creo un usuario backdoor con privilegios sudo
5. Establecio persistencia via cron job
6. Accedio a archivos sensibles (credenciales, configuraciones)
7. Exfiltr datos a archivos temporales
8. Intento borrar huellas (logs parciales, timestamps modificados)

### Nivel de Impacto: ALTO

- Datos personales comprometidos (Ley 18.331)
- Credenciales de sistemas criticos expuestas
- Acceso potencial a base de datos de clientes
- Riesgo de movimiento lateral adicional

---

## METODOLOGIA

### Herramientas Utilizadas

- dd / dc3dd: Adquisicion de imagen de disco
- The Sleuth Kit (fls, ils, mactime): Analisis de archivos
- Autopsy: Analisis grafico de imagen
- Volatility: Analisis de memoria
- strings: Extraccion de cadenas
- sqlite3: Analisis de bases de datos SQLite
- grep/awk/sed: Analisis de logs
- sha256sum / md5sum: Verificacion de integridad

### Cadena de Custodia

[Incluir plantilla de cadena de custodia completa]

---

## HALLAZGOS TECNICOS

### HALLAZGO 1: SQL Injection en Portal Web

**Evidencia:**
- Archivo: /var/log/apache2/access.log
- Entrada: GET /login.php' OR 1=1-- HTTP/1.1 200
- IP: 172.16.0.100
- Fecha: 10/Jul/2024 10:30:17

**Analisis:**
El atacante exploto una vulnerabilidad de SQL injection en el formulario
de login del portal bancario. El payload ' OR 1=1-- permitio bypass
de autenticacion.

**Impacto:** Acceso no autorizado al portal bancario.

---

### HALLAZGO 2: Webshell Instalada

**Evidencia:**
- Archivo: /var/www/html/banco_del_sol/uploads/cmd.php
- Hash SHA256: [calcular]
- Permisos: -rw-r--r--

**Analisis:**
Se encontro una webshell PHP que permite ejecucion remota de comandos.
La webshell incluye funcionalidad de reverse shell.

**Impacto:** Acceso remoto persistente al servidor web.

---

### HALLAZGO 3: Usuario Backdoor

**Evidencia:**
- Archivo: /etc/passwd
- Entrada: sysadmin_back:x:1099:1099:System Administrator Backdoor:/home/sysadmin_back:/bin/bash
- Sudoers: /etc/sudoers.d/sysadmin_back

**Analisis:**
Se creo un usuario backdoor sysadmin_back con UID 1099 y privilegios
sudo sin contrasena.

**Impacto:** Acceso persistente con privilegios root.

---

### HALLAZGO 4: Persistencia via Cron Job

**Evidencia:**
- Archivo: /etc/cron.d/backdoor
- Contenido: */5 * * * * root /tmp/.system_backup.sh > /dev/null 2>&1

**Analisis:**
Se instalo un cron job que ejecuta un reverse shell cada 5 minutos
conectando a 172.16.0.100:4444.

**Impacto:** Persistencia y reconexion automatica al servidor C2.

---

### HALLAZGO 5: Exfiltracion de Datos

**Evidencia:**
- Archivos: /tmp/.data_archive.tar.gz, /tmp/.stolen_data.txt, /tmp/.stolen_data2.txt
- Contenido: Credenciales de BD, configuraciones, documentos

**Analisis:**
El atacante copio y comprimio archivos sensibles incluyendo
credenciales de acceso a sistemas y configuraciones criticas.

**Impacto:** Compromiso de credenciales y datos confidenciales.

---

### HALLAZGO 6: Borrado de Huellas

**Evidencia:**
- Logs parcialmente truncados
- Historial de bash borrado
- Timestamps modificados en archivos criticos

**Analisis:**
El atacante intento destruir evidencia modificando timestamps y
truncando logs. Sin embargo, dejo registros en auth.log.1 y otros
archivos que permiten la reconstruccion.

**Impacto:** Intento de obstruccion de investigacion.

---

## EVIDENCIA

### Catalogo de Evidencia

| ID | Descripcion | Hash SHA256 | Ubicacion |
|----|-------------|-------------|-----------|
| E001 | Imagen de disco | [hash] | /evidence/disk_images/ |
| E002 | Volcado de memoria | [hash] | /evidence/memory_dumps/ |
| E003 | Logs servidor web | [hash] | /evidence/log_archives/ |
| E004 | Webshell cmd.php | [hash] | /evidence/artifacts/ |
| E005 | Cron job backdoor | N/A | /evidence/artifacts/ |
| E006 | Datos exfiltrados | [hash] | /evidence/artifacts/ |

---

## CONCLUSIONES

1. La intrusion se originó via SQL injection en el portal web
2. El atacante utilizó multiples tecnicas de persistencia
3. Se comprometieron credenciales de sistemas criticos
4. Se exfiltraron datos personales sujetos a Ley 18.331
5. El atacante intento borrar huellas pero dejo evidencia suficiente

---

## RECOMENDACIONES

### Inmediatas (24-48 horas)

1. Cambiar todas las credenciales comprometidas
2. Eliminar usuario backdoor sysadmin_back
3. Eliminar cron job y scripts del atacante
4. Eliminar webshell
5. Actualizar /etc/hosts
6. Revocar sesiones SSH activas

### Corto Plazo (1-2 semanas)

1. Corregir vulnerabilidad de SQL injection
2. Implementar WAF (Web Application Firewall)
3. Revisar y endurecer configuraciones de SSH
4. Implementar monitoreo de integridad de archivos
5. Actualizar politicas de firewall
6. Capacitacion en seguridad para usuarios

### Largo Plazo (1-3 meses)

1. Implementar segmentacion de red
2. Desplegar sistema de deteccion de intrusiones (IDS)
3. Realizar auditoria de seguridad completa
4. Implementar MFA (autenticacion multifactor)
5. Establecer programa de monitoreo continuo
6. Revisar cumplimiento de Ley 18.331

---

## REPORTES A AUTORIDADES

En caso de confirmarse compromiso de datos personales:

- CERTuy: cert@certuy.uy / +598 2604 2211
- URCDP (Unidad Reguladora y de Control de Datos Personales)
- Ministerio Publico (si hay delito informatico)

Documentacion requerida:
- Este informe forense
- Evidencia preservada con hashes
- Cadena de custodia completa
- Impacto estimado sobre datos personales

---

## APENDICES

### A. Comandos Utilizados

[Lista completa de comandos ejecutados durante el analisis]

### B. Herramientas y Versiones

- dd: coreutils 8.32
- dc3dd: 1.0
- The Sleuth Kit: 4.x
- Volatility: 2.6 / 3.0
- Autopsy: 4.x
- sqlite3: 3.x

### C. Referencias Legales

- Ley 18.331: Proteccion de datos personales
- Decreto 66/025: Reglamentacion
- Ley 19.520: Delitos informaticos
- ISO 27037: Directrices para identificacion, recoleccion, adquisicion y preservacion de evidencia digital
EOF
```

---

## COMANDOS RAPIDOS DE REFERENCIA

### Verificacion de Integridad

```bash
# Verificar hash de imagen de disco
sha256sum -c /evidence/disk_images/workstation_disk_image.dd.sha256

# Verificar hash de memoria
sha256sum -c /evidence/memory_dumps/workstation_memory.dump.sha256
```

### Busqueda Rápida de Artefactos

```bash
# Todos los archivos ocultos en /tmp
find /mnt/evidence/disk_image/tmp -name ".*" -type f 2>/dev/null

# Todos los archivos modificados en las ultimas 48 horas
find /mnt/evidence/disk_image -mtime -2 -type f 2>/dev/null

# Todos los archivos PHP
find /mnt/evidence/disk_image -name "*.php" -type f 2>/dev/null

# Todos los archivos ejecutables
find /mnt/evidence/disk_image -type f -executable 2>/dev/null

# Contenido de /etc/passwd con usuario backdoor
grep sysadmin_back /mnt/evidence/disk_image/etc/passwd

# Cron jobs sospechosos
cat /mnt/evidence/disk_image/etc/cron.d/*

# Conexiones a IP del atacante
grep 172.16.0.100 /mnt/evidence/disk_image/var/log/*
```

### Analisis de Strings

```bash
# Buscar IPs en la imagen
strings /evidence/disk_images/workstation_disk_image.dd | grep -E "^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$"

# Buscar passwords en la imagen
strings /evidence/disk_images/workstation_disk_image.dd | grep -i "password"

# Buscar URLs en la imagen
strings /evidence/disk_images/workstation_disk_image.dd | grep -i "http"

# Buscar comandos sospechosos
strings /evidence/disk_images/workstation_disk_image.dd | grep -i "nc -e\|bash -i\|/dev/tcp"
```
