# GUIA DE RESPUESTA - Escenario 01: Phishing y Reverse Shell
## Equipo Azul (Defensa) - Banco del Sol

---

**Escenario:** 01_phishing
**Plataforma:** Tectonic Cyber Range
**Duracion estimada:** 1 hora 30 minutos
**Nivel:** Principiante-Intermedio

---

## INDICE

1. [Contexto del escenario](#1-contexto-del-escenario)
2. [Fase 1: Deteccion](#2-fase-1-deteccion)
3. [Fase 2: Analisis](#3-fase-2-analisis)
4. [Fase 3: Contencion](#4-fase-3-contencion)
5. [Fase 4: Erradicacion](#5-fase-4-erradicacion)
6. [Fase 5: Recuperacion](#6-fase-5-recuperacion)
7. [Fase 6: Lecciones aprendidas](#7-fase-6-lecciones-aprendidas)
8. [Plantilla de informe](#8-plantilla-de-informe)

---

## 1. Contexto del escenario

### Situacion

El equipo de seguridad del Banco del Sol ha recibido una alerta no especifica sobre posible actividad sospechosa en la red. No se tiene informacion inicial sobre que paso, cuando, ni que sistemas estan afectados. Su equipo (equipo azul) debe investigar, determinar el alcance del incidente y responder adecuadamente.

### Infraestructura relevante

| VM | IP | Rol | Sistema |
|---|---|---|---|
| attacker | 172.16.0.10 | Maquina atacante (externa) | Kali Linux |
| webserver | 10.10.1.10 | Servidor web del banco | Ubuntu 22.04 |
| mailserver | 10.10.1.20 | Servidor de correo | Ubuntu 22.04 |
| workstation | 10.10.2.100 | Equipo del empleado victima | Ubuntu 22.04 |
| fileserver | 10.10.2.10 | Servidor de archivos | Ubuntu 22.04 |
| database | 10.10.2.20 | Servidor de bases de datos | Ubuntu 22.04 |
| domaincontroller | 10.10.2.5 | Controlador de dominio/DNS | Ubuntu 22.04 |

### Credenciales de acceso

| VM | Usuario | Contrasena | Puerto SSH |
|---|---|---|---|
| workstation | empleado | empleado123 | 22 |
| workstation | soporte | soporte123 | 22 |
| webserver | webadmin | webadmin123 | 22 |
| mailserver | mailadmin | mailadmin123 | 22 |
| attacker | kali | kali | 22 |

### Cuentas de correo

| Usuario | Email | Contrasena IMAP |
|---|---|---|
| Juan Perez | juan.perez@bancodelsol.local | Mail2024! |
| Maria Garcia | maria.garcia@bancodelsol.local | Mail2024! |
| Pedro Lopez | pedro.lopez@bancodelsol.local | Mail2024! |

---

## 2. Fase 1: Deteccion

El objetivo de esta fase es identificar que ha ocurrido un incidente de seguridad. Debe examinar multiples fuentes de logs y sistemas para detectar indicadores de compromiso (IOC).

### Paso 1.1: Revisar logs del servidor de correo (mailserver)

Conectarse al mailserver:

```bash
ssh mailadmin@10.10.1.20
# Contrasena: mailadmin123
```

Revisar el log de correo en busca de mensajes sospechosos:

```bash
# Ver los ultimos 100 registros del mail log
sudo tail -100 /var/log/mail.log
```

**Que buscar:**
- Correos enviados desde dominios sospechosos (no bancodelsol.local)
- Correos con asuntos de phishing ("verificacion", "actualizacion", "seguridad")
- Correos con Reply-To diferente al From
- Intentos de login IMAP/POP3 fallidos seguidos de exitos

```bash
# Buscar correos con asuntos tipicos de phishing
grep -i "verifique\|actualizacion\|seguridad\|cuenta\|bloqueo" /var/log/mail.log

# Buscar correos con remitentes sospechosos
grep -i "bancodel-sol\|bancodelsol.com\|outlook.com\|gmail.com" /var/log/mail.log

# Buscar envios hacia juan.perez (la victima)
grep "juan.perez" /var/log/mail.log

# Buscar intentos de login fallidos
grep -i "failed\|authentication\|login" /var/log/mail.log

# Buscar IPs externas que se conectaron
grep -E "from [0-9]+\.[0-9]+\.[0-9]+\.[0-9]+" /var/log/mail.log
```

**Salida esperada (indicador de phishing):**

```
2026-07-13T10:30:15 mailserver postfix/smtp[12345]: ABC123: to=<juan.perez@bancodelsol.local>, relay=none, delay=0.5, status=sent (250 Ok)
```

Tambien revisar el log de envio registrado por el escenario:

```bash
sudo cat /var/log/phishing_email_sent.log
```

### Paso 1.2: Revisar logs del servidor web (webserver)

Conectarse al webserver:

```bash
ssh webadmin@10.10.1.10
# Contrasena: webadmin123
```

Revisar los access logs de Apache:

```bash
# Ver los ultimos 200 registros de acceso
sudo tail -200 /var/log/apache2/bancodelsol_access.log

# O si esta en el log default
sudo tail -200 /var/log/apache2/access.log
```

**Que buscar:**
- Solicitudes a `/descargar.php` (la pagina maliciosa)
- Solicitudes desde la IP de la workstation (10.10.2.100)
- Solicitudes GET a archivos sospechosos
- User-Agent del navegador del empleado

```bash
# Buscar accesos a la pagina de phishing
grep "descargar.php" /var/log/apache2/bancodelsol_access.log
grep "descargar.php" /var/log/apache2/access.log 2>/dev/null

# Buscar accesos desde la workstation
grep "10.10.2.100" /var/log/apache2/bancodelsol_access.log

# Buscar solicitudes POST (login)
grep "POST" /var/log/apache2/bancodelsol_access.log

# Buscar codigos de respuesta 200 (descargas exitosas)
grep " 200 " /var/log/apache2/bancodelsol_access.log | grep "descargar"

# Extraer IPs mas activas
awk '{print $1}' /var/log/apache2/bancodelsol_access.log | sort | uniq -c | sort -rn | head -20
```

**Salida esperada (indicador de descarga del payload):**

```
10.10.2.100 - - [13/Jul/2026:10:35:22 -0300] "GET /descargar.php?token=seg_bds_jul2026 HTTP/1.1" 200 1234 "-" "Mozilla/5.0"
```

### Paso 1.3: Revisar la workstation comprometida

Conectarse a la workstation:

```bash
ssh empleado@10.10.2.100
# Contrasena: empleado123
```

**Verificar procesos sospechosos:**

```bash
# Listar todos los procesos con usuario
ps aux

# Buscar procesos sospechosos
ps aux | grep -i "update\|updater\|heartbeat\|nc\|ncat\|/bin/sh\|/bin/bash.*-c"

# Buscar procesos ejecutados por el usuario empleado
ps -u empleado -f

# Buscar procesos en /tmp
ps aux | grep "/tmp/"
```

**Que buscar:**
- Procesos ejecutando scripts desde `/tmp/.sys_update/`
- Procesos bash con comandos de red
- Procesos con nombres genericos como "updater.sh"
- Procesos en background sin terminal asociada

**Verificar archivos sospechosos:**

```bash
# Buscar directorios ocultos en /tmp
ls -la /tmp/ | grep "^\."

# Buscar archivos ocultos recursivamente en /tmp
find /tmp -name ".*" -type f 2>/dev/null
find /tmp -name ".*" -type d 2>/dev/null

# Ver contenido de directorios sospechosos
ls -la /tmp/.sys_update/
cat /tmp/.sys_update/config.dat
cat /tmp/.sys_update/payload_exec.log
cat /tmp/.sys_update/activity.log

# Verificar si hay directorios adicionales ocultos
ls -la /tmp/.hidden_data/ 2>/dev/null
cat /tmp/.hidden_data/session.dat 2>/dev/null
```

**Que buscar:**
- Directorio `/tmp/.sys_update/` con archivos config.dat, updater.sh
- Directorio `/tmp/.hidden_data/` con session.dat
- Archivos de log del payload

**Verificar archivos descargados:**

```bash
# Ver archivos en la carpeta de descargas
ls -la ~/Descargas/

# Buscar archivos PDF sospechosos
find ~/Descargas -name "*.pdf" -o -name "*.exe" -o -name "*.sh" -o -name "*.elf" 2>/dev/null

# Ver contenido del archivo descargado (si es texto)
cat ~/Descargas/verificar_cuenta.pdf 2>/dev/null
```

**Verificar /etc/hosts:**

```bash
# Ver el archivo de hosts (buscando entradas anadidas)
cat /etc/hosts
grep "bancodel-sol" /etc/hosts
```

**Que buscar:**
- Entrada `10.10.1.10 bancodel-sol.com.uy` (dominio falso mapeado al webserver)

**Verificar cron jobs:**

```bash
# Ver cron jobs del usuario empleado
crontab -l

# Ver cron jobs del usuario soporte
crontab -u soporte -l 2>/dev/null

# Verificar cron jobs del sistema
ls -la /etc/cron.*
cat /etc/crontab
```

**Que buscar:**
- Cron job que ejecuta `/tmp/.sys_update/updater.sh`
- Cualquier cron job que ejecute scripts desde /tmp

**Verificar logs de autenticacion:**

```bash
# Ver ultimos registros
sudo tail -50 /var/log/auth.log

# Buscar sesiones abiertas
grep "session opened" /var/log/auth.log

# Buscar ejecucion de cron
grep "CRON" /var/log/auth.log
```

**Verificar /etc/hosts modificado:**

```bash
# Ver las entradas actuales
cat /etc/hosts

# Buscar entradas que no deberian estar ahi
grep -v "^#\|^$" /etc/hosts
```

### Paso 1.4: Verificar conectividad de red desde la workstation

```bash
# Ver conexiones activas
ss -tunap

# Buscar conexiones a puertos inusuales
ss -tunap | grep -E "4444|5555|6666|1337"

# Ver conexiones establecidas
ss -tunap | grep ESTABLISHED

# Ver todos los puertos que estan escuchando
ss -tlnp
```

**Que buscar:**
- Conexion ESTABLISHED hacia 172.16.0.10:4444 (reverse shell al atacante)
- Cualquier proceso escuchando en puertos altos (4444, 5555, 6666)

### Paso 1.5: Resumen de indicadores encontrados en la Fase 1

Complete esta tabla con los hallazgos:

| # | IOC | Fuente | Severidad |
|---|---|---|---|
| 1 | Correo desde soporte@bancodel-sol.com.uy | mailserver/mail.log | Alta |
| 2 | Asunto "Actualizacion de seguridad" | mailserver/mail.log | Media |
| 3 | Descarga de /descargar.php desde 10.10.2.100 | webserver/access.log | Alta |
| 4 | Directorio /tmp/.sys_update/ | workstation | Alta |
| 5 | Cron job updater.sh | workstation/crontab | Alta |
| 6 | Entrada en /etc/hosts | workstation | Media |
| 7 | Archivo verificar_cuenta.pdf | workstation/Descargas | Alta |
| 8 | Proceso bash en background | workstation/ps | Media |

---

## 3. Fase 2: Analisis

El objetivo de esta fase es determinar que ocurrio exactamente, como funciono el ataque, y cual es su alcance completo.

### Paso 2.1: Analizar el correo de phishing (mailserver)

```bash
# Conectar al mailserver
ssh mailadmin@10.10.1.20

# Buscar el correo en el buzón de juan.perez
sudo find /home/juan.perez/Maildir -name "*.mail" -exec cat {} \; 2>/dev/null

# Tambien buscar en /var/mail si se uso mbox
sudo cat /var/mail/juan.perez 2>/dev/null

# Buscar el correo en la cola de Postfix
sudo find /var/spool/postfix/maildrop -type f -exec cat {} \; 2>/dev/null

# Buscar todos los correos recientes en el sistema
sudo find /var/mail /home/*/Maildir -type f -mmin -120 2>/dev/null
```

**Analisis de headers del correo de phishing:**

Extraer y analizar los headers del correo malicioso. Los headers revelan:

```
From: soporte@bancodel-sol.com.uy          <- Dominio falso (guion en "bancodel-sol")
Reply-To: soporte-tecnico@outlook.com      <- Reply-To different (indicio de phishing)
To: juan.perez@bancodelsol.local           <- Victima identificada
Subject: Actualizacion de seguridad - Verifique su cuenta  <- Tactica de urgencia
X-Mailer: Microsoft Outlook 16.0          <- User-Agent falso (enviado desde Linux)
```

**Preguntas clave del analisis:**

1. El dominio del remitente es legitimo?
   - No: `bancodel-sol.com.uy` (con guion) vs `bancodelsol.com.uy` (sin guion)

2. El Reply-To coincide con el From?
   - No: Reply-To apunta a outlook.com (dominio publico)

3. El asunto usa tacticas de urgencia o miedo?
   - Si: "Actualizacion de seguridad", "Verifique su cuenta", implicando consecuencias

4. Que enlace contiene el correo?
   - http://10.10.1.10/descargar.php?token=seg_bds_jul2026
   - El dominio IP apunta al webserver del banco (DMZ)

### Paso 2.2: Analizar la descarga del payload (webserver)

```bash
# Conectar al webserver
ssh webadmin@10.10.1.10

# Ver todos los accesos a descargar.php
grep "descargar.php" /var/log/apache2/bancodelsol_access.log

# Ver el log de descargas registrado por PHP
sudo tail -50 /var/log/apache2/bancodelsol_error.log 2>/dev/null

# Verificar el payload que se entrego
cat /var/www/banco_del_sol/payload.bin
cat /var/www/banco_del_sol/descargar.php

# Calcular hash del payload
sha256sum /var/www/banco_del_sol/payload.bin

# Verificar el tamanio del payload
ls -la /var/www/banco_del_sol/payload.bin
ls -la /var/www/banco_del_sol/descargar.php
```

**Que determinar:**
- Que archivo se descargo (nombre, tamanio, hash)
- Desde que IP se descargo
- Cuando se realizo la descarga
- Si hubo multiples descargas

### Paso 2.3: Analizar el compromiso de la workstation

```bash
# Conectar a la workstation
ssh empleado@10.10.2.100

# Reconstruir la linea de tiempo del ataque
echo "=== LINEA DE TIEMPO ==="

# 1. Cuando se descargo el archivo
ls -la --time=full-iso ~/Descargas/verificar_cuenta.pdf

# 2. Cuando se creo el directorio sospechoso
ls -la --time=full-iso /tmp/.sys_update/

# 3. Cuando se modifico /etc/hosts
stat /etc/hosts

# 4. Cuando se creo el cron job
sudo grep "empleado" /var/log/auth.log | grep CRON

# 5. Cuando se ejecuto el payload
cat /tmp/.sys_update/payload_exec.log
cat /tmp/.sys_update/activity.log

# 6. Proceso activo del malware
ps aux | grep "updater\|heartbeat\|/tmp/.sys_update"

# 7. Conexiones de red activas
ss -tunap | grep -v "127.0.0.1"

# 8. Tabla ARP (para ver si hay spoofing)
arp -a
```

**Analisis de archivos del payload:**

```bash
# Ver configuracion del malware
cat /tmp/.sys_update/config.dat

# Ver script de persistencia
cat /tmp/.sys_update/updater.sh

# Ver log de ejecucion
cat /tmp/.sys_update/payload_exec.log

# Ver log de actividad completa
cat /tmp/.sys_update/activity.log

# Ver datos exfiltrados simulados
cat /tmp/.hidden_data/session.dat 2>/dev/null

# Ver cron log
cat /tmp/.sys_update/cron.log 2>/dev/null
```

**Reconstruir la cadena de ataque:**

```
1. [MAIL] Correo phishing enviado desde soporte@bancodel-sol.com.uy
   -> juan.perez@bancodelsol.local
   Hora: ~10:30

2. [WEB] Juan Perez hizo click en el enlace
   -> GET http://10.10.1.10/descargar.php?token=...
   -> Archivo descargado: verificar_cuenta.pdf
   Hora: ~10:35

3. [WORKSTATION] Juan ejecuto el archivo descargado
   -> Se creo /tmp/.sys_update/
   -> Se ejecuto updater.sh en background
   -> Se creo cron job para persistencia
   -> Se modifico /etc/hosts
   Hora: ~10:36

4. [RED] El payload intento reverse shell
   -> Conexion hacia 172.16.0.10:4444
   Hora: ~10:36
```

### Paso 2.4: Verificar si hay propagacion adicional

```bash
# Desde la workstation, verificar si hay conexiones a otros hosts internos
ss -tunap | grep ESTABLISHED

# Verificar si hay archivos sospechosos en otros directorios
find /home/empleado -name ".*" -type f 2>/dev/null
find /var/tmp -name ".*" -type f 2>/dev/null

# Verificar si se instalaron paquetes no autorizados
dpkg -l | grep -i "nc\|ncat\|netcat\|socat" 2>/dev/null

# Verificar historial de comandos del usuario
cat /home/empleado/.bash_history 2>/dev/null
cat /root/.bash_history 2>/dev/null
```

---

## 4. Fase 3: Contencion

El objetivo es detener la propagacion del incidente sin destruir evidencia.

### Paso 3.1: Aislar la workstation de la red

**IMPORTANTE: NO apagar la maquina. Primero aislar, luego analizar.**

```bash
# Conectar a la workstation
ssh empleado@10.10.2.100

# Bloquear todo el trafico saliente excepto SSH (para mantener acceso)
sudo iptables -F
sudo iptables -P INPUT ACCEPT
sudo iptables -P FORWARD DROP
sudo iptables -P OUTPUT DROP

# Permitir solo SSH desde el instructor
sudo iptables -A INPUT -s 10.10.0.10/32 -p tcp --dport 22 -j ACCEPT
sudo iptables -A OUTPUT -d 10.10.0.10/32 -p tcp --sport 22 -j ACCEPT

# Permitir trafico loopback
sudo iptables -A INPUT -i lo -j ACCEPT
sudo iptables -A OUTPUT -o lo -j ACCEPT

# Verificar las reglas aplicadas
sudo iptables -L -v -n

echo "[CONTENCION] Workstation aislada de la red. Trafico bloqueado."
```

**Alternativa con UFW:**

```bash
# Si UFW esta habilitado
sudo ufw deny out
sudo ufw allow in from 10.10.0.10 to any port 22
sudo ufw status verbose
```

### Paso 3.2: Matar los procesos maliciosos

```bash
# En la workstation

# Identificar el PID del proceso updater
UPDATE_PID=$(pgrep -f "updater.sh")
echo "PID del proceso malicioso: $UPDATE_PID"

# Matar el proceso
sudo kill -9 $UPDATE_PID 2>/dev/null
sudo pkill -f "updater.sh"
sudo pkill -f "sys_update"

# Verificar que los procesos murieron
ps aux | grep -i "update\|heartbeat" | grep -v grep

echo "[CONTENCION] Procesos maliciosos terminados."
```

### Paso 3.3: Eliminar el cron job malicioso

```bash
# En la workstation

# Ver y eliminar cron jobs sospechosos
crontab -l
crontab -r 2>/dev/null

# Si hay cron jobs especificos, editar con crontab -e
echo "" | crontab -

echo "[CONTENCION] Cron jobs eliminados."
```

### Paso 3.4: Bloquear la IP del atacante en el firewall

```bash
# En la workstation

# Bloquear la IP del atacante
sudo iptables -A OUTPUT -d 172.16.0.10 -j DROP
sudo iptables -A INPUT -s 172.16.0.10 -j DROP

echo "[CONTENCION] IP del atacante bloqueada: 172.16.0.10"
```

### Paso 3.5: Cambiar contraseñas comprometidas

```bash
# En la workstation
sudo passwd empleado
# Ingresar nueva contrasena fuerte

# En el mailserver, cambiar contrasena de juan.perez
ssh mailadmin@10.10.1.20
sudo passwd juan.perez
# Ingresar nueva contrasena fuerte
```

### Paso 3.6: Documentar el estado de contencion

```bash
# En la workstation, ejecutar el script de recopilacion de evidencia
sudo bash /opt/recopilar_evidencia.sh

# Verificar donde se guardo
ls -la /opt/evidencia/
```

---

## 5. Fase 4: Erradicacion

El objetivo es eliminar completamente los artefactos del ataque del sistema.

### Paso 5.1: Eliminar archivos maliciosos de la workstation

```bash
# En la workstation

# Eliminar el directorio principal del malware
sudo rm -rf /tmp/.sys_update/

# Eliminar directorios adicionales ocultos
sudo rm -rf /tmp/.hidden_data/

# Verificar que no queden rastros
find /tmp -name ".*" -type d 2>/dev/null
find /tmp -name ".*" -type f 2>/dev/null

echo "[ERRADICACION] Archivos maliciosos eliminados de /tmp"
```

### Paso 5.2: Restaurar /etc/hosts

```bash
# En la workstation

# Eliminar la entrada maliciosa
sudo sed -i '/bancodel-sol\.com\.uy/d' /etc/hosts

# Verificar que quedo limpio
cat /etc/hosts

echo "[ERRADICACION] /etc/hosts restaurado"
```

### Paso 5.3: Eliminar el archivo descargado

```bash
# En la workstation

# Eliminar el PDF malicioso descargado
rm -f ~/Descargas/verificar_cuenta.pdf

# Verificar que no queden archivos sospechosos
ls -la ~/Descargas/

echo "[ERRADICACION] Archivo descargado eliminado"
```

### Paso 5.4: Verificar la limpieza completa

```bash
# En la workstation

echo "=== VERIFICACION DE LIMPIEZA ==="

# 1. No hay procesos sospechosos
echo "Procesos sospechosos:"
ps aux | grep -i "update\|heartbeat\|/tmp/" | grep -v grep
echo "(debe estar vacio)"

# 2. No hay directorios ocultos en /tmp
echo "Directorios ocultos en /tmp:"
find /tmp -name ".*" -type d 2>/dev/null
echo "(debe estar vacio)"

# 3. /etc/hosts esta limpio
echo "Entradas en /etc/hosts:"
grep -v "^#\|^$" /etc/hosts
echo "(no debe haber entradas bancodel-sol)"

# 4. No hay cron jobs maliciosos
echo "Cron jobs:"
crontab -l 2>/dev/null
echo "(debe estar vacio o sin updater)"

# 5. No hay archivos descargados
echo "Archivos en Descargas:"
ls -la ~/Descargas/
echo "(no debe haber verificar_cuenta.pdf)"

# 6. No hay conexiones a la IP del atacante
echo "Conexiones activas:"
ss -tunap | grep -v "127.0.0.1" | grep ESTABLISHED
echo "(no debe haber conexiones a 172.16.0.10)"

echo "=== VERIFICACION COMPLETADA ==="
```

### Paso 5.5: Eliminar artefactos del servidor web

```bash
# En el webserver
ssh webadmin@10.10.1.10

# Eliminar el payload y la pagina de descarga
sudo rm -f /var/www/banco_del_sol/descargar.php
sudo rm -f /var/www/banco_del_sol/payload.bin

# Verificar
ls -la /var/www/banco_del_sol/

echo "[ERRADICACION] Artefactos eliminados del webserver"
```

### Paso 5.6: Revisar cuentas de correo comprometidas

```bash
# En el mailserver
ssh mailadmin@10.10.1.20

# Verificar que no hay reglas de forwarding sospechosas
sudo postconf -n | grep "transport_maps\|virtual_maps\|alias_maps"

# Verificar que no hay usuarios fantasma
grep "juan.perez\|maria.garcia\|pedro.lopez" /etc/passwd

# Verificar logs de login sospechosos
grep -i "login\|authenticate" /var/log/mail.log | tail -20
```

---

## 6. Fase 5: Recuperacion

El objetivo es restaurar los sistemas a su estado normal y verificar que funcionan correctamente.

### Paso 6.1: Restaurar conectividad de la workstation

```bash
# En la workstation

# Restaurar reglas de firewall a estado normal
sudo iptables -F
sudo iptables -P INPUT ACCEPT
sudo iptables -P FORWARD ACCEPT
sudo iptables -P OUTPUT ACCEPT

# Verificar conectividad
ping -c 3 10.10.1.10
ping -c 3 10.10.2.5
ping -c 3 8.8.8.8

echo "[RECUPERACION] Conectividad restaurada en workstation"
```

### Paso 6.2: Verificar servicios criticos

```bash
# En la workstation, verificar que los servicios basicos funcionan
systemctl status ssh
systemctl status rsyslog

# Verificar que el usuario puede hacer login
ssh empleado@10.10.2.100

# Verificar que el usuario puede acceder al correo
# (desde la workstation, verificar conectividad al mailserver)
nc -zv 10.10.1.20 993

# Verificar que puede acceder al servidor web
curl -s -o /dev/null -w "%{http_code}" http://10.10.1.10/

echo "[RECUPERACION] Servicios verificados"
```

### Paso 6.3: Verificar que el webserver funciona normalmente

```bash
# En el webserver
ssh webadmin@10.10.1.10

# Verificar que Apache esta corriendo
sudo systemctl status apache2

# Verificar que la pagina principal funciona
curl -s http://localhost/ | head -20

# Verificar que NO hay archivos maliciosos
ls -la /var/www/banco_del_sol/ | grep -i "descargar\|payload"
echo "(debe estar vacio)"

echo "[RECUPERACION] Webserver verificado"
```

### Paso 6.4: Verificar que el mailserver funciona normalmente

```bash
# En el mailserver
ssh mailadmin@10.10.1.20

# Verificar Postfix
sudo systemctl status postfix

# Verificar Dovecot
sudo systemctl status dovecot

# Verificar que los usuarios pueden autenticarse
# (usar un cliente IMAP como thunderbird o un comando simple)
echo "Verificacion de servicios completada"

echo "[RECUPERACION] Mailserver verificado"
```

### Paso 6.5: Monitoreo intensivo post-recuperacion

Configurar monitoreo temporal para detectar recurrencia:

```bash
# En la workstation, monitorear conexiones durante 5 minutos
timeout 300 ss -tunap -c 1 | grep -v "127.0.0.1"

# Monitorear procesos nuevos cada 10 segundos
for i in $(seq 1 30); do
    echo "=== $(date) ==="
    ps aux | grep -i "update\|nc\|ncat" | grep -v grep
    sleep 10
done

# Monitorear archivos nuevos en /tmp
inotifywait -m -r /tmp/ -e create -e modify --timeout 300 2>/dev/null
```

---

## 7. Fase 6: Lecciones aprendidas

### Preguntas para discusion grupal

1. **Deteccion:** Cuanto tiempo tardo en detectarse el incidente? Que fuentes de logs fueron mas utiles?

2. **Analisis:** Como se determino el vector de entrada? Que tecnicas de analisis fueron mas efectivas?

3. **Contencion:** Fue correcta la decision de aislar la workstation sin apagarla? Por que?

4. **Erradicacion:** Todos los artefactos del ataque fueron eliminados? Como se verifico?

5. **Prevencion:** Que controles adicionales preventivos implementariamos?

### Controles preventivos recomendados

| Control | Descripcion | Prioridad |
|---|---|---|
| Filtros SPF/DKIM/DMARC | Autenticacion de correo electronico | Alta |
| Capacitacion de empleados | Simulacros de phishing periodicos | Alta |
| Proxy web con filtrado | Bloqueo de descargas ejecutables | Alta |
| EDR en endpoints | Deteccion de comportamiento malicioso | Alta |
| Segmentacion de red | Limitar movimiento lateral | Media |
| Monitorizacion de logs | SIEM centralizado con alertas | Media |
| Politica de contrasenas | Contrasenas fuertes y MFA | Media |
| Restriccion de /tmp | No ejecutar archivos desde /tmp | Baja |

### Mapeo con MITRE ATT&CK

| Fase | Tecnica | ID MITRE |
|---|---|---|
| Reconocimiento | Recopilacion de emails del banco | T1589 |
| Acceso Inicial | Spearphishing Link | T1566.002 |
| Ejecucion | Script interprete (bash) | T1059.004 |
| Persistencia | Cron Job | T1053.003 |
| Evasion | Archivos ocultos en /tmp | T1564.001 |
| Acceso a Credenciales | Archivos de configuracion locales | T1552.001 |
| Descubrimiento | Enumeracion de archivos locales | T1083 |
| Exfiltracion | Canal de C2 sobre TCP | T1071.001 |

---

## 8. Plantilla de informe

Utilizar esta plantilla para documentar el incidente:

```
============================================================
INFORME DE INCIDENTE DE SEGURIDAD
Banco del Sol - Escenario 01: Phishing
============================================================

1. RESUMEN EJECUTIVO
   Tipo: Phishing con reverse shell
   Severidad: ALTA
   Fecha de deteccion: [fecha]
   Sistemas afectados: workstation (10.10.2.100)
   Estado: CONTENIDO y ERRADICADO

2. LINEA DE TIEMPO
   [hora] - Correo de phishing recibido por juan.perez
   [hora] - Victima hizo click en el enlace
   [hora] - Payload descargado en workstation
   [hora] - Reverse shell establecida
   [hora] - Incidente detectado por equipo azul
   [hora] - Workstation aislada de la red
   [hora] - Procesos maliciosos terminados
   [hora] - Artefactos eliminados
   [hora] - Sistemas restaurados

3. VECTOR DE ATAQUE
   - Correo de phishing con enlace malicioso
   - Remitente falsificado: soporte@bancodel-sol.com.uy
   - Dominio falso con guion (bancodel-sol vs bancodelsol)
   - Payload servido via HTTP desde webserver comprometido

4. INDICADORES DE COMPROMISO (IOC)
   RED:
   - IP atacante: 172.16.0.10
   - Puerto reverse shell: 4444
   - URL maliciosa: http://10.10.1.10/descargar.php
   
   HOST:
   - Directorio: /tmp/.sys_update/
   - Archivos: config.dat, updater.sh, activity.log
   - Cron job: system_update_check
   - Entrada /etc/hosts: 10.10.1.10 bancodel-sol.com.uy
   - Archivo: ~/Descargas/verificar_cuenta.pdf
   
   EMAIL:
   - De: soporte@bancodel-sol.com.uy
   - Reply-To: soporte-tecnico@outlook.com
   - Asunto: Actualizacion de seguridad - Verifique su cuenta

5. ACCIONES DE CONTENCION
   - Aislamiento de red via iptables
   - Terminacion de procesos maliciosos
   - Eliminacion de cron jobs
   - Bloqueo de IP del atacante

6. ERRADICACION
   - Eliminacion de /tmp/.sys_update/
   - Eliminacion de /tmp/.hidden_data/
   - Restauracion de /etc/hosts
   - Eliminacion de descargar.php y payload.bin
   - Eliminacion de verificar_cuenta.pdf

7. RECUPERACION
   - Restauracion de conectividad
   - Verificacion de servicios
   - Cambio de credenciales comprometidas
   - Monitoreo intensivo post-recuperacion

8. RECOMENDACIONES
   - Implementar filtros SPF/DKIM/DMARC
   - Capacitacion anti-phishing para empleados
   - Proxy web con filtrado de descargas
   - EDR en endpoints
   - Segmentacion de red mejorada

9. EVIDENCIA ADJUNTA
   - Logs de mailserver (mail.log)
   - Logs de webserver (access.log)
   - Logs de workstation (auth.log, syslog)
   - Captura de procesos y conexiones
   - Archivos del payload recuperados

============================================================
```

---

## Comandos rapidos de referencia

### Conectarse a cada VM

```bash
ssh empleado@10.10.2.100          # Workstation (victima)
ssh webadmin@10.10.1.10           # Webserver
ssh mailadmin@10.10.1.20          # Mailserver
ssh kali@172.16.0.10              # Attacker
ssh instructor@10.10.0.10         # Instructor
```

### Comandos de emergencia

```bash
# Buscar todo lo sospechoso de una vez
echo "=== SCAN RAPIDO DE INCIDENTES ===" && \
grep -r "phishing\|malware\|backdoor\|reverse" /var/log/ 2>/dev/null && \
ps aux | grep -E "nc|ncat|python.*4444|bash.*-i" && \
ss -tunap | grep -E "4444|5555|6666" && \
find /tmp /var/tmp -name ".*" -type f 2>/dev/null && \
crontab -l 2>/dev/null && \
cat /etc/hosts | grep -v "^#" | grep -v "^$"
```

### Script automatico de deteccion

```bash
#!/bin/bash
# Script de deteccion rapida de phishing indicators
# Ejecutar en la workstation como usuario root

echo "[1] Procesos sospechosos:"
ps aux | grep -iE "update|heartbeat|/tmp/|nc |ncat" | grep -v grep

echo "[2] Archivos ocultos en /tmp:"
find /tmp -name ".*" -type f 2>/dev/null

echo "[3] Cron jobs:"
crontab -l 2>/dev/null
ls -la /etc/cron.d/ 2>/dev/null

echo "[4] /etc/hosts modificado:"
grep -v "^#" /etc/hosts | grep -v "^$"

echo "[5] Conexiones de red:"
ss -tunap | grep -v "127.0.0.1"

echo "[6] Archivos recientes en Descargas:"
ls -la ~/Descargas/ 2>/dev/null

echo "[7] Log reciente de syslog:"
tail -20 /var/log/syslog 2>/dev/null
```

---

*Guia de respuesta - Escenario 01 Phishing*
*Banco del Sol - Tectonic Cyber Range - BHU Uruguay*
*Version 1.0 - Julio 2026*
