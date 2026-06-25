# Clase 11: Hardening de Sistemas Operativos - Conceptos Fundamentales

**Duracion:** 2 horas

---

## Objetivos de Aprendizaje

1. Comprender que es el hardening, por que es necesario, y como se diferencia del parcheo
2. Identificar las areas principales de hardening en sistemas operativos
3. Conocer los estandares y guias de hardening (CIS Benchmarks, NIST, STIG)
4. Realizar una auditoria inicial con Lynis e interpretar el reporte
5. Aplicar controles basicos de hardening en un servidor Ubuntu

---

## Contenido Detallado

### 1. Que es hardening?

**Definicion:** Hardening (endurecimiento) es el proceso de asegurar un sistema reduciendo su superficie de ataque. Consiste en configurar el sistema operativo y sus servicios de la manera mas segura posible, eliminando todo lo que no sea estrictamente necesario.

**Analogia:** Imagina que acabas de mudarte a una casa nueva. La casa viene con:
- Todas las puertas y ventanas abiertas (servicios por defecto)
- La llave puesta en la cerradura (contrasenas debiles)
- Sin alarmas ni rejas (sin firewall)
- Puertas que no usas (servicios innecesarios)

El hardening es el proceso de: cerrar puertas y ventanas que no necesitas, cambiar las cerraduras, instalar alarmas, y poner rejas. Al final, la casa es mucho mas dificil de invadir.

**Diferencia entre hardening y parcheo:**

| Concepto | Hardening | Parcheo |
|----------|-----------|---------|
| Que hace | Configura el sistema para ser mas seguro | Instala actualizaciones de software |
| Ejemplo | Deshabilitar el usuario root, configurar firewall | `apt upgrade` para instalar parches de seguridad |
| Frecuencia | Una vez al inicio y revision periodica | Continuamente (cada vez que hay parches) |
| Enfoque | Reducir superficie de ataque | Corregir vulnerabilidades conocidas |
| Reversibilidad | Puede romper funcionalidad si no se prueba | Generalmente seguro, rara vez rompe algo |

Ambos son necesarios y complementarios. No sirve de nada tener un sistema parcheado pero con configuraciones inseguras, ni un sistema endurecido pero sin parches.

### 2. Por que es necesario el hardening?

**Estadisticas importantes:**

- Segun el Verizon Data Breach Investigations Report (DBIR), mas del 60% de las brechas de seguridad involucran credenciales debiles o robadas.
- El 95% de los ataques a servidores web explotan configuraciones incorrectas (OWASP).
- La mayoria de los sistemas operativos recien instalados vienen con configuraciones inseguras por defecto.

**Problemas comunes en sistemas recien instalados:**

```
Sistema recien instalado (Ubuntu Server por defecto):
  - Usuario root con contrasena (si configuraste)
  - Servicio SSH escuchando en puerto 22
  - Posibles servicios innecesarios (snapd, cups-browsed, etc.)
  - Sin firewall configurado
  - Sin politicas de contrasenas
  - Sin registro de auditoria
  - Paquetes no utilizados instalados
```

Cada una de estas configuraciones por defecto representa un riesgo. Por eso el hardening es necesario: transforma un sistema "funcional pero inseguro" en un sistema "funcional y seguro".

**Principio de minimo privilegio aplicado al SO:**

El principio de minimo privilegio dice: "cada componente debe tener solo los permisos estrictamente necesarios para cumplir su funcion". Aplicado al SO significa:

- Cada usuario tiene solo los permisos que necesita (no todos son administradores)
- Cada servicio se ejecuta con el usuario minimo necesario (no como root)
- Cada archivo tiene permisos ajustados a su uso (no 777 para todo)
- Cada puerto abierto solo si es necesario para un servicio

### 3. Areas de hardening

A continuacion, las 10 areas principales de hardening en sistemas operativos:

#### Area 1: Gestion de usuarios y cuentas

Consiste en controlar quienes pueden acceder al sistema y como.

**Acciones tipicas:**
- Eliminar o deshabilitar usuarios innecesarios (son los que vienen por defecto: `games`, `lp`, `uucp`, etc. en Linux)
- Renombrar cuentas privilegiadas (ej: cambiar `Administrator` en Windows)
- Configurar politicas de contrasenas: longitud minima, expiracion, historial, complejidad
- Bloqueo por intentos fallidos (fail2ban, pam_tally2)
- Autenticacion de dos factores (2FA) para acceso remoto
- Revisar grupos y membresias (quien esta en `sudo` / `Administrators`)

**Ejemplo de politica de contrasenas en Linux (`/etc/pam.d/common-password`):**
```
password requisite pam_pwquality.so retry=3 minlen=12 difok=3
```
- `minlen=12`: contrasena minima de 12 caracteres
- `difok=3`: al menos 3 caracteres diferentes de la contrasena anterior
- `retry=3`: permite 3 intentos antes de fallar

#### Area 2: Servicios y procesos

Cada servicio corriendo en el sistema es una superficie de ataque potencial. Menos servicios = menor riesgo.

**Acciones tipicas:**
- Listar todos los servicios activos
- Deshabilitar servicios no necesarios (FTP, Telnet, rlogin, rsh, TFTP, NFS, CUPS, etc.)
- Cambiar servicios antiguos por alternativas seguras (SSH en vez de Telnet)
- Configurar servicios para que corran con usuarios no privilegiados
- Usar contenedores o jaulas (chroot) para servicios expuestos

**Comando para listar servicios en Linux:**
```bash
systemctl list-units --type=service --state=running
```

#### Area 3: Permisos de archivos

Los permisos incorrectos pueden exponer informacion sensible o permitir modificaciones no autorizadas.

**Acciones tipicas:**
- Archivos sensibles con permisos minimos (`/etc/shadow` debe ser 600 o 640)
- Buscar archivos con permisos SUID/SGID innecesarios
- Directorios compartidos con permisos restringidos
- Verificar que `/tmp` tenga sticky bit y sea montado con `noexec`
- Archivos de log protegidos contra modificacion

**Busqueda de archivos SUID en Linux:**
```bash
find / -perm -4000 -type f 2>/dev/null
```

#### Area 4: Firewall local

El firewall del sistema controla el trafico de red entrante y saliente.

**Acciones tipicas:**
- Configurar reglas de firewall (iptables/nftables/ufw)
- Politica por defecto: DENY todo lo entrante
- Solo permitir puertos necesarios
- Limitar acceso por IP origen
- Registrar intentos denegados

#### Area 5: Actualizaciones y parches

Mantener el sistema actualizado es crucial para corregir vulnerabilidades conocidas.

**Acciones tipicas:**
- Configurar repositorios de actualizaciones
- Habilitar actualizaciones automaticas de seguridad (unattended-upgrades)
- Establecer politica de actualizacion (ej: parches de seguridad en 24hs, otros en 7 dias)
- Verificar que no hay paquetes con CVE conocidos sin parche

#### Area 6: Logging y auditoria

Sin registros, no puedes detectar ni investigar incidentes.

**Acciones tipicas:**
- Configurar syslog/rsyslog para registros del sistema
- Instalar y configurar auditd para auditoria de eventos
- Enviar logs a un servidor centralizado (SIEM)
- Configurar rotacion de logs (logrotate)
- Proteger logs contra modificacion (logs firmados, permisos 600)

#### Area 7: Kernel hardening

El kernel es el corazon del sistema operativo. Asegurarlo es critico.

**Acciones tipicas:**
- Configurar parametros sysctl para fortalecer la red
- Habilitar ASLR (Address Space Layout Randomization): `kernel.randomize_va_space=2`
- Habilitar Exec Shield / NX (No-Execute) para evitar ejecucion en stack/heap
- Restringir acceso a `/proc` y `/sys`
- Configurar kernel.dmesg_restrict=1 (solo root puede ver mensajes del kernel)
- Deshabilitar modulo de kernel innecesarios (bluetooth, firewire, etc.)

#### Area 8: Cifrado

Proteger datos en reposo y en transito.

**Acciones tipicas:**
- Cifrado de disco completo con LUKS (Linux Unified Key Setup)
- Cifrado de directorios home (eCryptfs, fscrypt)
- Usar SSH en vez de Telnet, rlogin, FTP
- Configurar SSL/TLS en servicios web
- Cifrado de backups

#### Area 9: Eliminacion de software innecesario

Cada paquete instalado es codigo que puede contener vulnerabilidades.

**Acciones tipicas:**
- Instalar solo el minimo necesario (minimal install)
- Eliminar paquetes no utilizados
- En servidores: no instalar entorno grafico, herramientas de desarrollo, compiladores, editores
- Revisar e limpiar paquetes huerfanos (orphans)

**Comando para listar paquetes instalados en Ubuntu:**
```bash
apt list --installed | wc -l
```

Comparativa tipica: Ubuntu Server con instalacion completa: ~600 paquetes. Ubuntu Server minimal: ~200-300 paquetes. Alpine Linux: ~30 paquetes.

#### Area 10: Configuracion de bootloader

Proteger el arranque del sistema para evitar que alguien con acceso fisico pueda obtener una shell de root.

**Acciones tipicas:**
- Configurar contrasena en GRUB
- Deshabilitar arranque desde dispositivos externos (en BIOS/UEFI)
- Configurar Secure Boot
- Establecer contrasena de BIOS/UEFI
- Restringir acceso a la consola fisica

### 4. Estandares y guias de hardening

#### CIS Benchmarks

CIS (Center for Internet Security) publica guias detalladas de hardening para cientos de sistemas operativos y aplicaciones. Son las mas utilizadas a nivel mundial.

**Caracteristicas:**
- Disponibles para: Ubuntu, Debian, RHEL, Windows 10/11/Server, macOS, Cisco, AWS, Azure, etc.
- Cada guia tiene entre 100 y 500 controles especificos
- Los controles se clasifican en niveles:
  - **Nivel 1:** Controles basicos que no afectan la funcionalidad (recomendados para todos)
  - **Nivel 2:** Controles mas estrictos que pueden afectar funcionalidad (entornos de alta seguridad)
- URL: https://www.cisecurity.org/cis-benchmarks/

**Ejemplo de control CIS para Ubuntu:**
```
1.1.1.1 Ensure mounting of cramfs filesystems is disabled (Automated)
  - Nivel: 1
  - Descripcion: Deshabilitar el soporte de sistemas de archivos cramfs
  - Comando: echo "install cramfs /bin/true" >> /etc/modprobe.d/disable.conf
```

#### NIST SP 800-123

Guia del Instituto Nacional de Estandares y Tecnologia de EE.UU. "Guide to General Server Security". Proporciona recomendaciones de alto nivel para asegurar servidores.

#### STIG (Security Technical Implementation Guide)

Desarrolladas por la Defense Information Systems Agency (DISA) del Departamento de Defensa de EE.UU. Son las guias mas estrictas y detalladas.

#### OWASP Hardening Guides

OWASP (Open Web Application Security Project) tiene guias de hardening para aplicaciones web, APIs, y contenedores.

#### Lynis

Lynis no es solo una herramienta de auditoria, sino que tambien proporciona recomendaciones basadas en estandares. Es la herramienta principal que usaremos en esta clase.

### 5. Ciclo de hardening

El hardening no es un evento unico, es un proceso ciclico:

```
Paso 1: EVALUACION INICIAL
  - Auditar estado actual del sistema
  - Identificar configuraciones inseguras
  - Herramientas: Lynis, CIS-CAT, OpenSCAP
  
Paso 2: APLICAR HARDENING
  - Implementar cambios segun guias (CIS, STIG)
  - Priorizar: primero nivel 1, luego nivel 2
  - Automatizar con scripts cuando sea posible
  
Paso 3: PROBAR FUNCIONALIDAD
  - Verificar que los servicios siguen funcionando
  - Probar acceso de usuarios
  - Rollback si algo se rompe
  - "No rompas la produccion"
  
Paso 4: MONITOREO CONTINUO
  - Vigilar logs y alertas
  - Repetir auditorias periodicamente
  - Detectar desviaciones (drift)
  
Paso 5: REPETIR
  - Nuevos servicios requieren nuevas reglas
  - Nuevas vulnerabilidades requieren nuevos controles
  - El hardening es un proceso vivo
```

**IMPORTANTE:** El ciclo mas importante es el Paso 3. Un sistema endurecido pero que no funciona es peor que un sistema funcional pero no endurecido. Siempre prueba en un entorno de staging antes de aplicar a produccion.

### 6. Antes de empezar: snapshots y backups

**Regla de oro del hardening:** Siempre toma un snapshot o backup ANTES de aplicar cambios.

**Por que:**
- Un cambio de hardening puede romper un servicio critico
- Puedes bloquear tu propio acceso (ej: firewall mal configurado, deshabilitaste SSH)
- Necesitas poder revertir rapidamente

**Recomendaciones:**
1. Tomar snapshot de la VM antes de empezar
2. Tener consola fisica o remota (IPMI, iDRAC, iLO) por si bloqueas la red
3. Tener sesion SSH activa mientras pruebas cambios
4. Configurar un cron job que revierta cambios si pierdes acceso (metodo "safe")
5. Documentar cada cambio para poder revertirlo

**Ejemplo de script de "safe changes":**
```bash
#!/bin/bash
# Aplicar cambio y revertir si no hay confirmacion en 60 segundos
cambio() {
    iptables -P INPUT DROP
    sleep 60
    iptables -P INPUT ACCEPT  # Revertir si no se confirma
}

cambio &
echo "Confirma que el firewall no bloqueo tu acceso (s/n):"
read confirmacion
if [ "$confirmacion" = "s" ]; then
    kill %1 2>/dev/null
    echo "Cambio confirmado."
fi
```

### 7. Ejercicio 1 - Auditoria inicial con Lynis

**Enunciado:** Instalar Lynis en un sistema Linux (Ubuntu), ejecutar una auditoria de seguridad completa, e interpretar el reporte generado.

##### Solucion

**Paso 1: Instalar Lynis**

Lynis puede instalarse desde los repositorios oficiales o desde GitHub.

```bash
# Metodo 1: Desde repositorio (version estable)
sudo apt update
sudo apt install lynis -y

# Verificar instalacion
lynis --version
```

**Salida esperada:**
```
Lynis 3.1.3
Copyright 2007-2024 - CISOfy
Root privileges: Yes
```

**Paso 2: Ejecutar auditoria del sistema**

```bash
sudo lynis audit system
```

Lynis necesita permisos de root para poder leer todos los archivos de configuracion y realizar todas las pruebas. Sin root, muchas pruebas se saltan.

**Paso 3: Interpretar el reporte**

La salida de Lynis es extensa. Se divide en varias secciones:

```
Seccion 1: Informacion del sistema
====================================
  Hostname: ubuntu-server
  OS: Ubuntu 22.04.3
  Kernel: 5.15.0-91-generic
  Processor: x86_64

Seccion 2: Pruebas realizadas
====================================
  Lynis realiza cientos de pruebas organizadas por categorias:
  - AUTH-xxxx: Autenticacion
  - FILE-xxxx: Archivos y permisos
  - KRNL-xxxx: Kernel
  - NETW-xxxx: Red
  - PHP-xxxx: PHP (si esta instalado)
  - PKGS-xxxx: Paquetes
  - PRNT-xxxx: Impresion
  - PROC-xxxx: Procesos
  - SSH-xxxx: SSH
  - FIRE-xxxx: Firewall
  ...
```

**Seccion importante: Warnings y Suggestions**

Al final del reporte, Lynis muestra:

```
=============================================================
  WARNINGS
=============================================================
  [!] No password aging configured (AUTH-9286)
      https://cisofy.com/controls/AUTH-9286/
  [!] No password strength tool installed (AUTH-9262)
      https://cisofy.com/controls/AUTH-9262/
  [!] One or more sysctl values differ (KRNL-5820)
      https://cisofy.com/controls/KRNL-5820/

=============================================================
  SUGGESTIONS
=============================================================
  * Consider hardening SSH configuration (SSH-7408)
    - Set PermitRootLogin to no
    - Set PasswordAuthentication to no
    - Set MaxAuthTries to 3
  * Install a tool like pwgen to generate random passwords (AUTH-9262)
  * Configure sysctl entries (KRNL-5830)
    - Set net.ipv4.tcp_syncookies=1
    - Set net.ipv4.conf.all.rp_filter=1
    - Set net.ipv4.conf.all.accept_source_route=0
  * Consider installing and configuring iptables (FIRE-4512)
```

**Seccion clave: Hardening Index**

```
=============================================================
  HARDENING INDEX
=============================================================
  [>] Tests performed: 245
  [>] Warnings: 12
  [>] Suggestions: 28
  [>] Hardening index: 63/100
```

El Hardening Index es un numero del 0 al 100 que indica que tan endurecido esta el sistema:
- 0-40: Critico. Muchas configuraciones inseguras
- 41-60: Debil. Varias areas requieren atencion
- 61-80: Aceptable. Buen nivel pero hay margen de mejora
- 81-90: Bueno. Sistema bastante seguro
- 91-100: Excelente. Sistema endurecido

**Interpretacion del ejemplo:** Con 63/100, el sistema tiene configuraciones basicas pero le faltan muchas mejoras. Esto es tipico de un Ubuntu recien instalado.

**Paso 4: Guardar el reporte para comparacion futura**

```bash
# Ejecutar y guardar en archivo
sudo lynis audit system --report-file /tmp/lynis-inicial.report

# Ver solo el resumen
sudo lynis audit system --quick
```

**Paso 5: Usar Lynis para verificar controles especificos**

```bash
# Ver estado de una categoria especifica
sudo lynis audit system --tests NETW-4512

# Ver todas las pruebas disponibles
sudo lynis show tests
```

### 8. Ejercicio 2 - CIS Benchmark checklist (10 controles basicos)

**Enunciado:** Dado un servidor Ubuntu recien instalado, aplicar los primeros 10 controles del CIS Benchmark para Ubuntu.

##### Solucion

A continuacion, cada control con su comando y explicacion.

**Control 1: Configurar fuente de actualizaciones**

Asegurarse de que el sistema tenga repositorios configurados correctamente para recibir actualizaciones.

```bash
# Verificar repositorios configurados
cat /etc/apt/sources.list

# Si esta vacio o incorrecto, configurar repositorios oficiales de Ubuntu
sudo nano /etc/apt/sources.list
```

Contenido tipico de sources.list para Ubuntu 22.04:
```
deb http://archive.ubuntu.com/ubuntu jammy main restricted universe multiverse
deb http://archive.ubuntu.com/ubuntu jammy-updates main restricted universe multiverse
deb http://archive.ubuntu.com/ubuntu jammy-security main restricted universe multiverse
```

**Control 2: Instalar actualizaciones de seguridad**

```bash
# Actualizar lista de paquetes
sudo apt update

# Instalar actualizaciones de seguridad disponibles
sudo apt upgrade -y

# Verificar que no quedan paquetes por actualizar
apt list --upgradable
```

**Salida esperada:**
```
Listing... Done
(no output means all packages are up to date)
```

**Control 3: Configurar actualizaciones automaticas**

```bash
# Instalar unattended-upgrades
sudo apt install unattended-upgrades -y

# Configurar actualizaciones automaticas solo de seguridad
sudo dpkg-reconfigure --priority=low unattended-upgrades
```

Esto habilita las actualizaciones de seguridad cada 24 horas sin intervencion manual.

**Control 4: Crear usuario no-root para administracion**

```bash
# Crear nuevo usuario (reemplazar 'admin' con el nombre deseado)
sudo adduser admin

# Agregar al grupo sudo (administradores)
sudo usermod -aG sudo admin

# Verificar que el usuario pertenece al grupo sudo
groups admin
```

**Salida esperada:**
```
admin : admin sudo
```

**Control 5: Configurar sudo con contrasena**

Por defecto, Ubuntu ya requiere contrasena para sudo. Verificar que no se configuro NOPASSWD:

```bash
# Verificar configuracion de sudo
sudo visudo

# Buscar lineas como esta (NO debe estar):
# admin ALL=(ALL) NOPASSWD:ALL

# La configuracion segura es:
# admin ALL=(ALL) ALL
```

**Control 6: Deshabilitar login root via SSH**

Editar el archivo de configuracion de SSH:

```bash
sudo nano /etc/ssh/sshd_config
```

Buscar y modificar la linea:
```
# De:
PermitRootLogin yes

# A:
PermitRootLogin no
```

Reiniciar el servicio SSH:
```bash
sudo systemctl restart sshd
```

**Control 7: Configurar PasswordAuthentication (solo cuando haya keys)**

```bash
# Primero generar par de llaves en el cliente
# ssh-keygen -t ed25519 -a 100

# Luego copiar la llave publica al servidor
# ssh-copy-id -i ~/.ssh/id_ed25519.pub admin@servidor

# Finalmente, deshabilitar autenticacion por contrasena
sudo nano /etc/ssh/sshd_config

# Modificar:
# PasswordAuthentication no

sudo systemctl restart sshd
```

**ADVERTENCIA:** No deshabilitar PasswordAuthentication hasta que hayas confirmado que la autenticacion con llaves funciona. Si lo haces antes, te quedaras fuera del servidor.

**Control 8: Usar solo SSH key-based auth**

Este control refuerza el anterior. Ademas de deshabilitar PasswordAuthentication, asegurarse de que:

```bash
# En /etc/ssh/sshd_config:
PubkeyAuthentication yes
AuthorizedKeysFile .ssh/authorized_keys
PasswordAuthentication no
ChallengeResponseAuthentication no
UsePAM no  # Opcional, si se usan solo llaves
```

**Control 9: Configurar fail2ban**

Fail2ban protege contra ataques de fuerza bruta bloqueando IPs que fallan repetidamente la autenticacion.

```bash
# Instalar fail2ban
sudo apt install fail2ban -y

# Crear archivo de configuracion local
sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local

# Configurar proteccion SSH
sudo nano /etc/fail2ban/jail.local
```

Agregar o modificar la seccion SSH:
```
[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log
maxretry = 3
bantime = 3600
findtime = 600
```

- `maxretry = 3`: Bloquear despues de 3 intentos fallidos
- `bantime = 3600`: Bloquear por 1 hora (3600 segundos)
- `findtime = 600`: Ventana de 10 minutos para contar intentos

```bash
# Iniciar fail2ban
sudo systemctl start fail2ban
sudo systemctl enable fail2ban

# Verificar estado
sudo fail2ban-client status sshd
```

**Salida esperada:**
```
Status for the jail: sshd
|- Filter
|  |- Currently failed: 0
|  |- Total failed: 0
|  `- File list:    /var/log/auth.log
`- Actions
   |- Currently banned: 0
   |- Total banned: 0
   `- Banned IP list:
```

**Control 10: Deshabilitar servicios innecesarios**

```bash
# Listar servicios activos
systemctl list-units --type=service --state=running

# Identificar servicios innecesarios (depende del proposito del servidor)
# Servicios tipicamente innecesarios en un servidor:
# - cups-browsed (impresion)
# - avahi-daemon (zeroconf/mDNS)
# - bluetooth (si no se usa)
# - whoopsie (error reporting)

# Deshabilitar servicios innecesarios
sudo systemctl stop cups-browsed
sudo systemctl disable cups-browsed

sudo systemctl stop avahi-daemon
sudo systemctl disable avahi-daemon

# Verificar que el servicio ya no esta activo
systemctl is-active cups-browsed
```

**Salida esperada:**
```
inactive
```

**Resumen de los 10 controles aplicados:**

| # | Control | Comando principal | Verificacion |
|---|---|---|---|
| 1 | Fuente de actualizaciones | `cat /etc/apt/sources.list` | Repositorios configurados |
| 2 | Actualizar sistema | `sudo apt update && sudo apt upgrade -y` | Sin paquetes upgradable |
| 3 | Actualizaciones automaticas | `sudo apt install unattended-upgrades` | Servicio activo |
| 4 | Usuario no-root | `sudo adduser admin` | `groups admin` muestra sudo |
| 5 | sudo con contrasena | `sudo visudo` | Sin NOPASSWD |
| 6 | Deshabilitar root SSH | `PermitRootLogin no` en sshd_config | `grep PermitRootLogin /etc/ssh/sshd_config` |
| 7 | PasswordAuthentication | `PasswordAuthentication no` | Solo con llaves |
| 8 | Key-based auth | `PubkeyAuthentication yes` | `ssh-keygen` en cliente |
| 9 | fail2ban | `sudo apt install fail2ban` | `fail2ban-client status sshd` |
| 10 | Deshabilitar servicios | `sudo systemctl disable <servicio>` | `systemctl is-active <servicio>` |

### 9. Ejercicio 3 - Comparativa antes/despues con nmap

**Enunciado:** Escanear el sistema con nmap antes del hardening, aplicar cambios, y escanear de nuevo para comparar.

##### Solucion

**Paso 1: Escaneo inicial (antes del hardening)**

Desde otra maquina (o desde el mismo sistema si es practica local):

```bash
# Escanear puertos abiertos
nmap -sS -sV -p- 192.168.1.10
```

**Salida tipica antes del hardening:**
```
Starting Nmap 7.95 ( https://nmap.org ) at 2026-06-25 10:00
Nmap scan report for 192.168.1.10
Host is up (0.0012s latency).
Not shown: 65530 closed ports
PORT     STATE SERVICE     VERSION
21/tcp   open  ftp         vsftpd 3.0.3
22/tcp   open  ssh         OpenSSH 8.9p1 Ubuntu
80/tcp   open  http        Apache httpd 2.4.52
111/tcp  open  rpcbind     2-4 (RPC #100000)
3306/tcp open  mysql       MySQL 8.0.35
```

**Interpretacion:** El sistema tiene 5 puertos abiertos. Los servicios FTP (21), rpcbind (111), y MySQL (3306) son accesibles desde la red. FTP transmite credenciales en texto plano, rpcbind expone informacion del sistema, y MySQL no deberia estar accesible desde afuera.

**Paso 2: Aplicar hardening**

Aplicar los controles del Ejercicio 2 y ademas:

```bash
# Deshabilitar FTP si no es necesario
sudo systemctl stop vsftpd
sudo systemctl disable vsftpd

# Configurar firewall basico
sudo ufw --force enable
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh  # (o puerto personalizado)
sudo ufw allow http
sudo ufw allow https

# Verificar reglas
sudo ufw status verbose
```

**Salida del firewall:**
```
Status: active
Logging: on (low)
Default: deny (incoming), allow (outgoing)
New profiles: skip

To                         Action      From
--                         ------      ----
22/tcp                     ALLOW       Anywhere
80/tcp                     ALLOW       Anywhere
443/tcp                    ALLOW       Anywhere
22/tcp (v6)                ALLOW       Anywhere (v6)
80/tcp (v6)                ALLOW       Anywhere (v6)
443/tcp (v6)               ALLOW       Anywhere (v6)
```

**Paso 3: Escaneo despues del hardening**

```bash
nmap -sS -sV -p- 192.168.1.10
```

**Salida esperada despues del hardening:**
```
Starting Nmap 7.95 ( https://nmap.org ) at 2026-06-25 11:00
Nmap scan report for 192.168.1.10
Host is up (0.0012s latency).
Not shown: 65532 filtered ports
PORT     STATE SERVICE     VERSION
22/tcp   open  ssh         OpenSSH 8.9p1 Ubuntu
80/tcp   open  http        Apache httpd 2.4.52
443/tcp  open  ssl/http    Apache httpd 2.4.52
```

**Paso 4: Tabla comparativa**

| Aspecto | Antes del hardening | Despues del hardening |
|---------|-------------------|----------------------|
| Puertos abiertos | 21, 22, 80, 111, 3306 | 22, 80, 443 |
| Puertos filtrados | 0 | 65532 |
| Servicios innecesarios | FTP, rpcbind, MySQL expuesto | Solo SSH, HTTP, HTTPS |
| Firewall | Desactivado | Activado (UFW) |
| SSH root login | Permitido | Denegado |
| Password auth SSH | Permitido | Deshabilitado |
| Actualizaciones | Manual | Automaticas |
| fail2ban | No instalado | Instalado y activo |
| Superficie de ataque total | 5 puertos + root login + sin firewall | 3 puertos + solo usuarios + firewall |

**Interpretacion de resultados:**

Antes del hardening, un atacante podia:
1. Conectarse por FTP y capturar credenciales (texto plano)
2. Intentar fuerza bruta SSH contra el usuario root
3. Explotar rpcbind para enumerar informacion del sistema
4. Atacar MySQL directamente (posible fuerza bruta de bases de datos)

Despues del hardening, el atacante solo ve:
1. SSH en puerto 22 (protegido por fail2ban, solo con llaves, sin root)
2. HTTP/HTTPS (servicios publicos, pero monitoreados)

**Reduccion de superficie de ataque:** Se paso de 5 servicios expuestos a 3, y los 3 son necesarios para el funcionamiento del servidor. Ademas, los que quedaron tienen protecciones adicionales.

### 10. Preguntas y Respuestas

#### Pregunta 1
**Cual es la diferencia entre hardening y parcheo?**

**Respuesta:** El hardening y el parcheo son dos practicas complementarias pero diferentes. El parcheo consiste en instalar actualizaciones de software para corregir vulnerabilidades conocidas. Por ejemplo, si Apache lanza la version 2.4.55 corrigiendo una vulnerabilidad, actualizar a esa version es parcheo. El hardening, en cambio, consiste en cambiar configuraciones para hacer el sistema mas seguro, independientemente de las versiones de software. Por ejemplo, deshabilitar el login root, configurar un firewall, o eliminar servicios innecesarios es hardening. El parcheo es reactivo (corrige problemas conocidos), mientras que el hardening es proactivo (reduce el riesgo general). Ambos son necesarios: un sistema parcheado pero mal configurado sigue siendo vulnerable, y un sistema endurecido pero sin parches tiene vulnerabilidades conocidas sin corregir.

#### Pregunta 2
**Que son los CIS Benchmarks y para que sirven?**

**Respuesta:** Los CIS Benchmarks son guias de hardening desarrolladas por el Center for Internet Security (CIS). Son documentos detallados que contienen cientos de recomendaciones de seguridad especificas para diferentes sistemas operativos, aplicaciones y plataformas en la nube. Cada recomendacion (llamada "control") incluye: una descripcion del riesgo, el comando o configuracion para implementarla, y un metodo de verificacion. Los controles se clasifican en Nivel 1 (recomendados para todos, no afectan funcionalidad) y Nivel 2 (para entornos de alta seguridad, pueden afectar funcionalidad). Sirven como checklist para auditors y administradores: puedes tomar el benchmark de Ubuntu, por ejemplo, e ir aplicando control por control hasta endurecer completamente el sistema. Son el estandar de facto en la industria para hardening.

#### Pregunta 3
**Por que es importante deshabilitar servicios innecesarios?**

**Respuesta:** Cada servicio que corre en un sistema operativo es una superficie de ataque potencial. Un servicio es un programa que escucha en un puerto y procesa peticiones de red o locales. Cada servicio puede tener vulnerabilidades (bugs, fallos de seguridad), configuraciones inseguras, o credenciales por defecto. Si un servicio no es necesario, no hay razon para correrlo y exponerse a esos riesgos. Por ejemplo, si un servidor web no necesita FTP, deshabilitar vsftpd elimina el riesgo de que alguien explote una vulnerabilidad en vsftpd, o de que intercepte credenciales FTP en texto plano, o de que suba archivos maliciosos al servidor. Es el principio de minimo privilegio aplicado a servicios: solo ejecutar lo minimo necesario para la funcion del sistema.

#### Pregunta 4
**Que es el principio de minima instalacion?**

**Respuesta:** El principio de minima instalacion (o minimal install) consiste en instalar solo los paquetes estrictamente necesarios para la funcion del sistema, y nada mas. Cuando instalas un sistema operativo, los instaladores ofrecen opciones como "Ubuntu Server" (minimo) vs "Ubuntu Desktop" (con GUI, LibreOffice, juegos, etc.). Un servidor deberia instalarse siempre con la opcion minima. Ademas, despues de la instalacion, no se deben instalar paquetes innecesarios como: entornos graficos (X11, Wayland), herramientas de desarrollo (gcc, make) a menos que sean necesarias, servidores de bases de datos si no se usan, impresoras CUPS, servicios bluetooth, etc. Cada paquete adicional es: (1) mas codigo que puede tener vulnerabilidades, (2) mas servicios que pueden activarse, (3) mas superficie de ataque, (4) mas recursos consumidos. Una instalacion tipica de Ubuntu Server tiene ~300 paquetes. Alpine Linux puede tener ~30. Menos es mas seguro.

#### Pregunta 5
**Para que sirve Lynis?**

**Respuesta:** Lynis es una herramienta de auditoria de seguridad para sistemas Linux (y tambien macOS, BSD, Solaris). Realiza cientos de pruebas automaticas en todas las areas de hardening: autenticacion, configuracion de SSH, permisos de archivos, parametros del kernel, firewall, paquetes instalados, servicios activos, etc. Al finalizar, genera un reporte con: (1) Warnings: problemas de seguridad encontrados (ej: contrasenas sin expiracion), (2) Suggestions: recomendaciones para mejorar (ej: instalar fail2ban, configurar sysctl), (3) Hardening Index: puntuacion del 0 al 100 que resume el nivel de hardening del sistema. Lynis NO aplica cambios por si mismo, solo audita y recomienda. Sirve para: evaluar el estado actual del sistema, identificar areas debiles, guiar el proceso de hardening, medir la mejora a lo largo del tiempo (hardening index antes vs despues).

#### Pregunta 6
**Que riesgo tiene hacer hardening sin probar los cambios en un entorno de pruebas?**

**Respuesta:** Hacer hardening directamente en produccion sin probar puede causar multiples problemas graves: (1) bloqueo de acceso al sistema: si configuras mal el firewall (ej: olvidaste permitir SSH), te quedas fuera del servidor, (2) rotura de servicios: deshabilitar un servicio que parece innecesario pero que otro servicio necesita (ej: deshabilitar rpcbind puede romper NFS), (3) cambios en permisos: restringir permisos de un archivo puede romper una aplicacion que necesita leerlo, (4) configuracion de kernel: cambiar parametros sysctl puede afectar el rendimiento o la estabilidad del sistema, (5) actualizaciones automaticas: un parche puede romper compatibilidad con una aplicacion critica. Por eso el lema del hardening es: "primero en staging, luego en produccion, y siempre con snapshot". Si no hay entorno de pruebas, al menos tener un snapshot para revertir rapidamente y probar cada cambio de forma aislada.

---

## Tarea / Lectura Recomendada

1. **Practicar:** Instala Ubuntu Server en una VM (VirtualBox) y ejecuta `sudo lynis audit system`. Anota el Hardening Index inicial
2. **Practicar:** Aplica los 10 controles del Ejercicio 2 en tu VM. Luego ejecuta Lynis de nuevo y compara el Hardening Index
3. **Practicar:** Haz el escaneo con nmap antes y despues del hardening (Ejercicio 3). Documenta la reduccion de puertos abiertos
4. **Leer:** CIS Benchmark para Ubuntu 22.04 (descargar de https://www.cisecurity.org/cis-benchmarks/) - revisar los controles de Nivel 1
5. **Leer:** Lynis documentation - https://cisofy.com/documentation/lynis/
6. **Leer:** NIST SP 800-123 - "Guide to General Server Security" (disponible gratuitamente)
7. **Explorar:** OpenSCAP - https://www.open-scap.org/ (herramienta de auditoria basada en SCAP)
8. **Explorar:** DevSec Hardening Framework - https://devsec.io/ (roles de Ansible para hardening automatizado)
9. **Proyecto:** Crea un checklist de hardening personalizado para tu sistema operativo favorito, basado en CIS Benchmarks y Lynis
