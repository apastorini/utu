# Clase 12: Hardening de Linux Practico con ISOs Gratuitas

**Duracion:** 2 horas

---

## Objetivos de Aprendizaje

1. Descargar e instalar sistemas Linux ligeros (Alpine Linux, Ubuntu Server minimal) en maquinas virtuales
2. Crear y configurar maquinas virtuales en VirtualBox para practicar hardening
3. Aplicar un proceso completo de hardening paso a paso en Alpine Linux
4. Auditar el nivel de hardening antes y despues con Lynis
5. Crear un script de hardening automatizado

---

## Contenido Detallado

### 1. ISOs gratuitas y ligeras recomendadas

Para aprender hardening, lo mejor es empezar con sistemas minimalistas. Cuanto menos tenga el sistema, menos hay que endurecer, y mas claro se ve el efecto de cada cambio.

#### Alpine Linux

**Pagina oficial:** https://alpinolinux.org/downloads/

Alpine Linux es una distribucion Linux extremadamente ligera, disenada con la seguridad en mente desde su origen.

**Caracteristicas principales:**
- ISO de solo ~50MB (la version "Standard")
- Usa musl libc en vez de glibc (menos codigo, menos vulnerabilidades)
- Usa OpenRC en vez de systemd (mas simple, mas facil de auditar)
- Compilado con PIE (Position Independent Executable) y ASLR por defecto
- Stack smashing protection activado por defecto
- Paquetes minimos: instalacion base tiene ~30 paquetes
- Ideal para: contenedores Docker, servidores minimalistas, routers, IoT

**Por que Alpine es "seguro por defecto":**
- El kernel ya viene con protecciones de memoria activadas
- No tiene servicios innecesarios corriendo al iniciar
- La instalacion base no incluye compiladores, editores, ni herramientas de desarrollo
- El gestor de paquetes `apk` verifica firmas digitales

#### Ubuntu Server LTS minimal

**Pagina oficial:** https://ubuntu.com/download/server

La opcion "minimized" del instalador de Ubuntu Server instala solo lo esencial.

**Caracteristicas:**
- ISO de ~200MB (mucho mas que Alpine, pero viene con mas controladores)
- Usa systemd (el estandar en la mayoria de servidores Linux)
- Amplia documentacion y comunidad
- Paquetes .deb y gestor apt
- Ideal para: aprender hardening en un entorno mas "real" (empresarial)

#### Debian netinstall

**Pagina oficial:** https://www.debian.org/distrib/netinst

Instalador de red que descarga solo lo necesario. Muy estable.

**Caracteristicas:**
- ISO de ~300MB
- En el instalador, desmarcar "Debian desktop environment" y no seleccionar paquetes extra
- Ideal para: servidores de produccion que requieren estabilidad extrema

#### DietPi

**Pagina oficial:** https://dietpi.com/

Optimizado para Raspberry Pi y VMs pequenas. Extremadamente ligero.

| Distribucion | Tamano ISO | Init system | Gestor paq. | Dificultad |
|-------------|-----------|-------------|-------------|------------|
| Alpine Linux | ~50 MB | OpenRC | apk | Media |
| Ubuntu Server minimal | ~200 MB | systemd | apt | Baja |
| Debian netinstall | ~300 MB | systemd | apt | Baja |
| DietPi | ~400 MB | systemd | apt | Baja |

**Recomendacion para esta clase:** Usaremos Alpine Linux por ser el mas minimalista y por que el hardening se nota mucho mas (pocos servicios, puntaje Lynis alto desde el inicio).

### 2. Creacion de VM para hardening

Vamos a usar **VirtualBox**, que es gratuito y funciona en Windows, Linux y macOS.

#### Que es una maquina virtual?

Una maquina virtual (VM) es un sistema operativo que corre dentro de otro sistema operativo, como si fuera un programa mas. El sistema "real" se llama **host** y el sistema virtualizado se llama **guest**.

**Analogia:** Es como tener una casa (tu PC) y dentro construir una casa de munecas (la VM). La casa de munecas tiene sus propias habitaciones, puertas y ventanas, pero todo esta contenido dentro de la casa real.

**Por que usar VMs para hardening:**
- No afectas tu sistema principal
- Puedes hacer snapshots (fotos del estado actual) y revertir si algo sale mal
- Puedes tener varias VMs en red (atacante y victima)
- Es gratis y facil de configurar

#### Descargar e instalar VirtualBox

1. Ve a https://www.virtualbox.org/
2. Haz clic en "Download VirtualBox 7.x"
3. Selecciona tu sistema operativo (Windows, Linux, o macOS)
4. Ejecuta el instalador y sigue los pasos (siguiente, siguiente, instalar)

#### Crear VM paso a paso

Sigue estos pasos exactamente. Si nunca creaste una VM, no te preocupes, es como llenar un formulario.

**Paso 1:** Abre VirtualBox y haz clic en "Nueva" (o menu Maquina -> Nueva).

**Paso 2:** Configura la VM:
```
Nombre: hardening-lab
Carpeta: (dejar la que viene por defecto)
ISO Image: (no seleccionar aun, haz clic en "Next")
Tipo: Linux
Version: Linux 2.6 / 3.x / 4.x / 5.x (64-bit)
```

**Paso 3:** Configurar memoria RAM:
```
Tamano de memoria: 512 MB
```
No pongas mas de 512MB para Alpine, no lo necesita. Para Ubuntu Server, 1024MB esta bien.

**Paso 4:** Configurar disco duro:
```
Crear un disco duro virtual ahora
Tamano del disco: 8.00 GB
Tipo de archivo de disco: VDI (VirtualBox Disk Image)
Almacenamiento: Reservado dinamicamente
```
"Reservado dinamicamente" significa que el archivo en tu PC crece a medida que la VM necesita espacio, no ocupa 8GB de inmediato.

**Paso 5:** Configurar red:
```
Selecciona la VM -> Configuracion -> Red
Adaptador 1: NAT
```
Modo NAT significa que la VM comparte la IP de tu PC para salir a Internet, pero no es accesible desde tu red local directamente. Es seguro para practicar.

**Paso 6 (opcional):** Segunda interfaz de red para practicar escaneos:
```
Adaptador 2: Red Interna
Nombre: intnet
```
Esto te permitira conectar dos VMs entre si sin pasar por tu red real.

**Paso 7:** Montar la ISO:
```
Selecciona la VM -> Configuracion -> Almacenamiento
Controlador IDE -> disco vacio -> clic en el icono de disco ->
Seleccionar/crear un disco optico -> elegir el archivo .iso descargado
```

**Paso 8:** Iniciar la VM (clic en Iniciar).

### 3. Instalacion minima de Alpine Linux (paso a paso)

Alpine Linux no tiene instalador grafico como Ubuntu. Se configura todo desde la terminal. No te asustes: es simple si sigues los pasos.

**Paso 1:** Arranca la VM con la ISO de Alpine montada.

**Paso 2:** Al arrancar, veras el menu de Alpine:
```
Welcome to Alpine Linux 3.20
Kernel 6.6.x on an x86_64 (/dev/tty0)

[ boot menu ]
  (1) Alpine Linux 3.20.0
  (2) Alpine Linux 3.20.0 (vanilla)
  (3) Alpine Linux 3.20.0 (hardened)
  (4) System rescue
```

Selecciona la opcion 1 (presiona Enter) o simplemente espera a que arranque por defecto.

**Paso 3:** Alpine arranca en modo "live". Ves un prompt de login:
```
localhost login: root
```
Escribe `root` y presiona Enter. No hay contrasena.

**Paso 4:** Ya estas dentro del sistema live. Ejecuta el instalador:
```
# setup-alpine
```

**Paso 5:** Responde las preguntas del instalador:

```
Available keyboards: ...
Select keyboard layout: us
Select variant: us

Enter system hostname: hardening-lab

Available interfaces: eth0
Enter interface name: eth0
Ip address for eth0: dhcp

DNS domain name: (Enter - dejar vacio)
DNS nameserver: 8.8.8.8

Enter timezone: UTC

HTTP proxy: (Enter - none)

Mirror: https://dl-cdn.alpinelinux.org
Selecciona un mirror cercano. Si no sabes cual, elige el 1 (dl-cdn).

Setup a user: (Enter - none)  <-- No crear usuario ahora, lo haremos manualmente

Which ssh server: openssh

Allow root ssh login: no

Which disk: sda
How would you like to use it: sys
Erase the above disk and continue: y
```

**Explicacion de las opciones:**
- `hostname`: El nombre de tu maquina en la red
- `dhcp`: Obtiene IP automaticamente
- `8.8.8.8`: DNS de Google (para resolver nombres)
- `openssh`: Instala SSH para acceso remoto
- `sys`: Instalacion completa en disco (no solo en RAM)
- `sda`: El disco virtual que creaste (8GB)

**Paso 6:** Cuando termine la instalacion, te pedira reiniciar:
```
Installation is complete. Please reboot.
# reboot
```

**Paso 7:** Antes de reiniciar, ve a VirtualBox -> Dispositivos -> Unidades Opticas -> Quitar disco de la unidad (para no arrancar de nuevo desde la ISO).

**Paso 8:** Despues del reinicio, inicia sesion:
```
hardening-lab login: root
Password: (la contrasena que configuraste en setup-alpine)
```

**Paso 9:** Verificar que la red funciona:
```bash
ip addr show eth0
```

**Salida esperada:**
```
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 ...
    inet 10.0.2.15/24 brd 10.0.2.255 scope global eth0
```

La IP `10.0.2.15` es tipica del modo NAT de VirtualBox.

```bash
ping -c 3 google.com
```

**Salida esperada:**
```
PING google.com (142.250.80.46): 56 data bytes
64 bytes from 142.250.80.46: seq=0 ttl=118 time=15.2 ms
64 bytes from 142.250.80.46: seq=1 ttl=118 time=14.8 ms
64 bytes from 142.250.80.46: seq=2 ttl=118 time=15.5 ms
```

Si el ping funciona, tienes conexion a Internet. Si no, revisa la configuracion de red en VirtualBox (NAT).

### 4. Hardening de Alpine Linux paso a paso

Una vez que Alpine esta instalado y funcionando, vamos a endurecerlo. Sigue cada paso en orden.

#### Paso 1: Actualizar sistema

Siempre empezamos asegurandonos de tener los ultimos parches de seguridad.

```bash
# Actualizar lista de paquetes
apk update

# Actualizar todos los paquetes instalados
apk upgrade
```

**Salida esperada:**
```
fetch https://dl-cdn.alpinelinux.org/alpine/v3.20/main/x86_64/APKINDEX.tar.gz
(1/2) Upgrading musl (1.2.4-r0 -> 1.2.5-r0)
(2/2) Upgrading busybox (1.36.0-r0 -> 1.36.1-r0)
OK: 32 packages, 0 dirs, 0 files
```

**Explicacion:** `apk update` descarga la lista de paquetes disponibles. `apk upgrade` instala las nuevas versiones. En Alpine, a diferencia de Ubuntu, no hay separacion entre `update` y `upgrade` en cuanto a seguridad - `apk upgrade` actualiza todo.

#### Paso 2: Crear usuario admin

Nunca trabajes como root si no es necesario. Creemos un usuario para administracion.

```bash
# Crear usuario (reemplazar "admin" si quieres otro nombre)
adduser admin

# Te pedira contrasena y algunos datos:
Changing password for admin
New password: (escribe una contrasena segura)
Retype password: (repite)
Password changed
Full name: ()
Room number: ()
Work phone: ()
Home phone: ()
Other: ()
```

```bash
# Agregar al grupo "wheel" (equivalente a sudo)
addgroup admin wheel

# Instalar sudo
apk add sudo

# Configurar sudo para el grupo wheel
echo "%wheel ALL=(ALL) ALL" >> /etc/sudoers
```

**Verificacion:**
```bash
# Probar que sudo funciona
su - admin
sudo whoami
```

**Salida esperada:**
```
root
```

Si `sudo whoami` devuelve `root`, significa que admin puede ejecutar comandos como administrador.

#### Paso 3: Configurar sudo sin NOPASSWD

Asegurarse de que sudo pide contrasena (por defecto ya deberia ser asi):

```bash
# Verificar el archivo sudoers
sudo cat /etc/sudoers
```

Si ves una linea como `%wheel ALL=(ALL) NOPASSWD: ALL`, hay que cambiarla. La linea correcta pide contrasena siempre.

#### Paso 4: Hardening de SSH

SSH es la puerta de entrada al servidor. Hay que asegurarla bien.

```bash
# Editar configuracion de SSH
sudo nano /etc/ssh/sshd_config
```

Buscar y modificar (o agregar) las siguientes lineas:

```
# No permitir login como root
PermitRootLogin no

# Usar solo protocolo 2 (el 1 es inseguro, aunque Alpine ya lo trae asi)
Protocol 2

# Limitar intentos de autenticacion
MaxAuthTries 3

# Desconectar sesiones inactivas despues de 5 minutos (300 segundos)
ClientAliveInterval 300
ClientAliveCountMax 0

# No permitir autenticacion con contrasena vacia
PermitEmptyPasswords no

# Puerto alternativo (opcional, reduce ruido de bots)
Port 2222
```

**ADVERTENCIA sobre el puerto 2222:** Si cambias el puerto SSH, no olvides permitirlo en el firewall y conectarte con `ssh -p 2222 admin@IP`. Si cierras la sesion actual y no configuraste el firewall, te quedaras fuera.

```bash
# Verificar sintaxis de la configuracion
sudo sshd -t

# Si no hay errores, reiniciar SSH
sudo rc-service sshd restart
```

**Salida esperada:**
```
 * Stopping sshd ... [ ok ]
 * Starting sshd ... [ ok ]
```

#### Paso 5: Firewall con iptables

Alpine no trae firewall preconfigurado. Vamos a crear un script con reglas basicas.

```bash
# Instalar iptables
sudo apk add iptables ip6tables

# Crear script de reglas
sudo nano /etc/init.d/firewall-rules
```

Contenido del script:

```bash
#!/sbin/openrc-run

description="Firewall rules"

depend() {
    need net
}

start() {
    ebegin "Loading firewall rules"

    # Limpiar reglas existentes
    iptables -F
    iptables -X
    iptables -t nat -F

    # Politicas por defecto: denegar todo lo entrante
    iptables -P INPUT DROP
    iptables -P FORWARD DROP
    iptables -P OUTPUT ACCEPT

    # Permitir loopback (localhost)
    iptables -A INPUT -i lo -j ACCEPT

    # Permitir conexiones establecidas y relacionadas
    iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

    # Permitir SSH (puerto 22, o 2222 si cambiaste)
    iptables -A INPUT -p tcp --dport 22 -j ACCEPT

    # Permitir ICMP (ping) limitado
    iptables -A INPUT -p icmp --icmp-type echo-request -m limit --limit 10/second -j ACCEPT

    # Registrar intentos denegados
    iptables -A INPUT -j LOG --log-prefix "FW-DROP: " --log-level 4

    eend $?
}

stop() {
    ebegin "Unloading firewall rules"

    # Restaurar politicas por defecto (aceptar todo)
    iptables -P INPUT ACCEPT
    iptables -P FORWARD ACCEPT
    iptables -P OUTPUT ACCEPT

    # Limpiar reglas
    iptables -F
    iptables -X
    iptables -t nat -F

    eend $?
}
```

```bash
# Hacer ejecutable el script
sudo chmod +x /etc/init.d/firewall-rules

# Agregar al inicio automatico
sudo rc-update add firewall-rules default

# Iniciar el firewall
sudo rc-service firewall-rules start
```

**Salida esperada:**
```
 * Loading firewall rules ... [ ok ]
```

**Verificacion:**
```bash
# Listar reglas activas
sudo iptables -L -v -n
```

**Salida esperada:**
```
Chain INPUT (policy DROP 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination
    0     0 ACCEPT     all  --  lo     *       0.0.0.0/0            0.0.0.0/0
    0     0 ACCEPT     all  --  *      *       0.0.0.0/0            0.0.0.0/0            state ESTABLISHED,RELATED
    0     0 ACCEPT     tcp  --  *      *       0.0.0.0/0            0.0.0.0/0            tcp dpt:22
    0     0 ACCEPT     icmp --  *      *       0.0.0.0/0            0.0.0.0/0            icmptype 8 limit: avg 10/sec burst 5
    0     0 LOG        all  --  *      *       0.0.0.0/0            0.0.0.0/0            LOG flags 0 level 4 prefix "FW-DROP: "

Chain FORWARD (policy DROP 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination

Chain OUTPUT (policy ACCEPT 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination
```

La politica INPUT es DROP (denegar), y solo permitimos: loopback, conexiones establecidas, SSH (puerto 22), y ping limitado.

#### Paso 6: Deshabilitar servicios innecesarios

```bash
# Listar todos los servicios
rc-service --list

# Ver servicios activos
rc-status --all
```

**Salida tipica en Alpine:**
```
Runlevel: default
  networking                                       [  started  ]
  sshd                                             [  started  ]
  acpid                                            [  started  ]
  crond                                            [  started  ]

Dynamic Runlevel: hotplugged
Dynamic Runlevel: needed/wanted
  syslog                                           [  started  ]
```

Servicios tipicos en Alpine minimo:
- `networking`: necesario (red)
- `sshd`: necesario (SSH)
- `acpid`: solo si necesitas manejo de energia (APM)
- `crond`: solo si necesitas tareas programadas (cron)
- `syslog`: necesario (logs del sistema)

Si ves servicios como `avahi-daemon`, `bluetooth`, `cups`, etc., deshabilitalos:

```bash
# Ejemplo de deshabilitar servicio (si existe)
sudo rc-service avahi-daemon stop
sudo rc-update del avahi-daemon
```

**Explicacion:** `rc-update del` elimina el servicio del nivel de ejecucion "default", por lo que no se iniciara al arrancar. `rc-service stop` lo detiene ahora mismo.

#### Paso 7: Configurar logs y rotacion

```bash
# Instalar logrotate
sudo apk add logrotate

# Crear configuracion de rotacion
sudo nano /etc/logrotate.d/hardening
```

Contenido:
```
/var/log/*.log {
    weekly
    rotate 4
    compress
    delaycompress
    missingok
    notifempty
    postrotate
        rc-service syslog restart 2>/dev/null || true
    endscript
}
```

- `weekly`: Rotar cada semana
- `rotate 4`: Mantener 4 semanas de logs
- `compress`: Comprimir logs viejos (gzip)
- `delaycompress`: No comprimir el mas reciente
- `missingok`: No dar error si no hay log
- `notifempty`: No rotar si el archivo esta vacio

#### Paso 8: Kernel hardening via sysctl

Los parametros del kernel controlan como se comporta el sistema a nivel mas bajo. Vamos a configurar los mas importantes para seguridad.

```bash
# Crear archivo de configuracion
sudo nano /etc/sysctl.d/hardening.conf
```

Contenido:
```
# ==========================================
# Kernel Hardening - Configuracion de red
# ==========================================

# SYN cookies: protege contra SYN flood attacks
net.ipv4.tcp_syncookies=1

# Deshabilitar IP forwarding (no es un router)
net.ipv4.ip_forward=0

# Filtro de camino inverso: evita IP spoofing
net.ipv4.conf.all.rp_filter=1
net.ipv4.conf.default.rp_filter=1

# Ignorar paquetes con opcion source route (ataques de routing)
net.ipv4.conf.all.accept_source_route=0
net.ipv4.conf.default.accept_source_route=0

# Ignorar redirects ICMP (ataques MITM)
net.ipv4.conf.all.accept_redirects=0
net.ipv4.conf.default.accept_redirects=0
net.ipv6.conf.all.accept_redirects=0

# Enviar redirects solo si es necesario (deshabilitar)
net.ipv4.conf.all.send_redirects=0
net.ipv4.conf.default.send_redirects=0

# Proteccion contra TIME-WAIT assassination (RFC 1337)
net.ipv4.tcp_rfc1337=1

# Ignorar pings broadcast (evita ser amplificador en ataques DDoS)
net.ipv4.icmp_echo_ignore_broadcasts=1

# Ignorar pings que no pueden ser respondidos
net.ipv4.icmp_ignore_bogus_error_responses=1

# Registrar paquetes con direcciones imposibles (martians)
net.ipv4.conf.all.log_martians=1
net.ipv4.conf.default.log_martians=1

# ==========================================
# Kernel Hardening - Memoria y ejecucion
# ==========================================

# Deshabilitar core dumps de procesos SUID (evita filtrar memoria)
fs.suid_dumpable=0

# Habilitar ASLR (Address Space Layout Randomization)
# 0=desactivado, 1=randomizacion parcial, 2=completa
kernel.randomize_va_space=2

# Restringir acceso a mensajes del kernel
kernel.dmesg_restrict=1

# Restringir acceso a punteros de kernel
kernel.kptr_restrict=2

# ==========================================
# Kernel Hardening - Modulos
# ==========================================

# Deshabilitar soporte de sistemas de archivos poco usados
# (estos modulos se pueden deshabilitar con install en modprobe.d)

# Solo permitir modulos firmados (en kernels que lo soportan)
# kernel.modules_disabled=1  (CUIDADO: deshabilita carga de modulos)
```

**Explicacion de los parametros mas importantes:**

| Parametro | Que hace | Por que es seguro |
|-----------|----------|------------------|
| `tcp_syncookies=1` | Activa SYN cookies | Protege contra ataques SYN flood |
| `rp_filter=1` | Filtro de ruta inversa | Un paquete debe salir por la misma interfaz por la que llego. Evita spoofing |
| `accept_source_route=0` | Ignora opcion de enrutamiento en IP | Los atacantes podrian redirigir paquetes |
| `accept_redirects=0` | Ignora redirects ICMP | Podrian redirigir trafico a traves de un atacante (MITM) |
| `randomize_va_space=2` | Randomiza direcciones de memoria | Hace mucho mas dificil explotar buffer overflows |
| `suid_dumpable=0` | No guarda core dumps de SUID | Evita que un atacante lea memoria de procesos privilegiados |
| `dmesg_restrict=1` | Solo root puede leer dmesg | Evita que usuarios sin privilegios vean informacion del kernel |

```bash
# Aplicar los cambios sin reiniciar
sudo sysctl -p /etc/sysctl.d/hardening.conf
```

**Salida esperada:**
```
net.ipv4.tcp_syncookies = 1
net.ipv4.ip_forward = 0
net.ipv4.conf.all.rp_filter = 1
...
```

**Verificar que los cambios persisten:**
```bash
sysctl net.ipv4.tcp_syncookies
```
Debe devolver `net.ipv4.tcp_syncookies = 1`.

#### Paso 9: Auditar con Lynis

```bash
# Instalar Lynis
sudo apk add lynis

# Ejecutar auditoria
sudo lynis audit system
```

Analizar el reporte, enfocarse en:
- Hardening Index (deberia ser alto en Alpine, ~70-80)
- Warnings (pocos en Alpine recien instalado)
- Suggestions (implementar las que apliquen)

#### Paso 10: Comparar hardening index antes/despues

Si ejecutaste Lynis antes de aplicar los pasos (en el sistema recien instalado), puedes comparar:

| Aspecto | Antes del hardening | Despues del hardening |
|---------|-------------------|----------------------|
| Hardening Index | ~65-70 | ~85-90 |
| Warnings | ~5-8 | ~1-2 |
| Suggestions | ~15-20 | ~5-8 |
| SSH config | PermitRootLogin yes | PermitRootLogin no |
| Firewall | No configurado | iptables con reglas |
| Kernel params | Por defecto | ASLR, syncookies, etc. |
| Usuarios | Solo root | root + admin con sudo |

### 5. Instalacion minima de Ubuntu Server (alternativa)

Si prefieres practicar hardening en Ubuntu en vez de Alpine, aqui estan los pasos resumidos:

**Paso 1:** Descargar ISO Ubuntu Server LTS desde https://ubuntu.com/download/server

**Paso 2:** Crear VM en VirtualBox (similar a Alpine, pero con 1024MB RAM).

**Paso 3:** Arrancar con ISO, seleccionar idioma (Espanol o Ingles).

**Paso 4:** En el instalador:
```
- Keyboard layout: Spanish o English (US)
- Instalacion: Ubuntu Server (minimized)
- Network: DHCP (automatico)
- Configure proxy: (dejar vacio)
- Mirror: (default)
- Storage: Use entire disk -> sda
- Profile setup:
  - Your name: admin
  - Server name: ubuntu-hardening
  - Username: admin
  - Password: (contrasena segura)
- SSH Setup: Install OpenSSH server (marcar)
- Featured Server Snaps: (ninguno, desmarcar todo)
```

**Paso 5:** Al finalizar, reiniciar y quitar ISO.

**Paso 6:** Aplicar hardening (adaptando comandos):
- `apt` en vez de `apk`
- `systemctl` en vez de `rc-service` y `rc-update`
- Los demas pasos (firewall, sysctl, usuarios, SSH) son iguales

**Diferencias clave entre Alpine y Ubuntu:**

| Aspecto | Alpine | Ubuntu |
|---------|--------|--------|
| Gestor de paquetes | `apk` | `apt` |
| Init system | OpenRC (`rc-service`, `rc-update`) | systemd (`systemctl`) |
| Firewall | iptables directo | ufw (wrapper de iptables) |
| Shell por defecto | ash (compatible con bash) | bash |
| Tamano base | ~30 paquetes | ~300 paquetes |
| Repositorio de paquetes | `apk add <paquete>` | `apt install <paquete>` |

### 6. Herramientas de hardening automatizado

El hardening manual esta bien para aprender, pero en entornos profesionales se automatiza.

#### Lynis (auditoria)

Ya lo usamos. Lynis audita pero no aplica cambios automaticamente.

#### CIS-CAT

Herramienta oficial del Center for Internet Security. Evalua el cumplimiento de CIS Benchmarks de forma automatizada.

```
Descarga: https://learn.cisecurity.org/cis-cat-lite
Requiere: Java Runtime Environment
```

#### OpenSCAP

Herramienta de codigo abierto que automatiza la evaluacion de guias SCAP/STIG.

```bash
# En Ubuntu
sudo apt install openscap-scanner scap-security-guide

# Evaluar contra perfil CIS de Ubuntu
sudo oscap xccdf eval --profile xccdf_org.ssgproject.content_profile_cis \
  --results resultados.xml --report reporte.html \
  /usr/share/xml/scap/ssg/content/ssg-ubuntu2204-ds.xml
```

Esto genera un reporte HTML con todos los controles evaluados (pass/fail).

#### Ansible Hardening Roles (DevSec Hardening Framework)

Roles de Ansible predefinidos para hardening automatizado:

```bash
# Instalar roles de DevSec
ansible-galaxy install devsec.hardening_ssh
ansible-galaxy install devsec.hardening_os
ansible-galaxy install devsec.hardening_firewall

# Ejemplo de playbook.yml
cat > playbook.yml << EOF
---
- hosts: servers
  roles:
    - devsec.hardening_ssh
    - devsec.hardening_os
    - devsec.hardening_firewall
EOF

# Ejecutar
ansible-playbook -i inventario.ini playbook.yml
```

**Ventaja:** Aplicas el mismo hardening a 100 servidores en minutos.

### 7. Ejercicio 1 - Instalacion completa de Alpine en VM

**Enunciado:** Realizar la instalacion completa de Alpine Linux en VirtualBox, configurando red, SSH, y usuarios. Documentar cada paso con comandos.

##### Solucion

A continuacion, los 20 pasos detallados con comandos exactos y lo que se ve en pantalla.

**Paso 1:** Descargar Alpine Standard ISO (https://alpinelinux.org/downloads/).

**Paso 2:** Crear VM en VirtualBox:
```
Nombre: hardening-lab
Tipo: Linux
Version: Linux 2.6/3.x/4.x/5.x (64-bit)
RAM: 512 MB
Disco: 8 GB (VDI, dinamico)
Red: NAT
```

**Paso 3:** Montar ISO e iniciar VM.

**Paso 4:** Arranca Alpine. Ves el menu de boot.
```
Lo que ves en pantalla:
[ Booting Alpine Linux... ]
[ ok ] Setting up networking
...
localhost login: _
```

**Paso 5:** Login como `root` (sin contrasena).
```
localhost login: root
localhost:~#
```

**Paso 6:** Ejecutar instalador.
```
localhost:~# setup-alpine
```

**Paso 7-16:** Responder preguntas del instalador:
```
Select keyboard layout: us
Select variant: us
Enter system hostname: hardening-lab
Available interfaces: eth0
Enter interface name: eth0
Ip address for eth0: dhcp
DNS domain name: (Enter)
DNS nameserver: 8.8.8.8
Enter timezone: UTC
HTTP proxy: (Enter)
Mirror: 1 (dl-cdn.alpinelinux.org)
Setup a user: (Enter - none)
Which ssh server: openssh
Allow root ssh login: no
Which disk: sda
How would you like to use it: sys
Erase the above disk and continue: y
```

**Paso 17:** Al finalizar la instalacion:
```
Installation is complete. Please reboot.
localhost:~# reboot
```

**Paso 18:** Expulsar ISO (VirtualBox -> Dispositivos -> Unidades Opticas -> Quitar disco).

**Paso 19:** Al reiniciar, login como root con la contrasena que configuraste:
```
hardening-lab login: root
Password: (tu contrasena)
hardening-lab:~#
```

**Paso 20:** Verificar instalacion:
```bash
# Ver sistema operativo
cat /etc/alpine-release

# Ver red
ip addr show eth0

# Ver paquetes instalados
apk list --installed | wc -l

# Probar conexion
ping -c 1 google.com
```

**Salida esperada:**
```
3.20.0
2: eth0: ... inet 10.0.2.15/24 ...
32
PING google.com (142.250.80.46): 56 data bytes
64 bytes from 142.250.80.46: seq=0 ttl=118 time=15.2 ms
```

**Resumen:** Alpine Linux instalado con exito. Tiene 32 paquetes, IP 10.0.2.15, conexion a Internet.

### 8. Ejercicio 2 - Hardening completo de Alpine

**Enunciado:** Aplicar los 10 pasos de hardening a Alpine Linux. Documentar cada comando y su proposito.

##### Solucion

**Paso 1: Actualizar sistema**
```bash
# Proposito: Instalar los ultimos parches de seguridad
apk update && apk upgrade
```

**Paso 2: Crear usuario admin**
```bash
# Proposito: No trabajar como root
adduser admin
addgroup admin wheel
apk add sudo
echo "%wheel ALL=(ALL) ALL" >> /etc/sudoers
```

**Paso 3: Hardening de SSH**
```bash
# Proposito: Asegurar acceso remoto
sudo nano /etc/ssh/sshd_config
# Cambiar: PermitRootLogin no
#         MaxAuthTries 3
#         ClientAliveInterval 300
#         ClientAliveCountMax 0

sudo rc-service sshd restart
```

**Paso 4: Firewall con iptables**
```bash
# Proposito: Controlar trafico de red
sudo apk add iptables
sudo nano /etc/init.d/firewall-rules
# (escribir el script del contenido detallado)
sudo chmod +x /etc/init.d/firewall-rules
sudo rc-update add firewall-rules default
sudo rc-service firewall-rules start
```

**Paso 5: Deshabilitar servicios innecesarios**
```bash
# Proposito: Reducir superficie de ataque
rc-status --all
# Si hay servicios innecesarios:
# sudo rc-service acpid stop
# sudo rc-update del acpid
```

**Paso 6: Logrotate**
```bash
# Proposito: Gestion de logs segura
sudo apk add logrotate
sudo nano /etc/logrotate.d/hardening
# (configurar rotacion semanal)
```

**Paso 7: Kernel hardening (sysctl)**
```bash
# Proposito: Fortalecer parametros del kernel
sudo nano /etc/sysctl.d/hardening.conf
# (agregar todos los parametros del contenido detallado)
sudo sysctl -p /etc/sysctl.d/hardening.conf
```

**Paso 8: Instalar y ejecutar Lynis**
```bash
# Proposito: Auditar el nivel de hardening
sudo apk add lynis
sudo lynis audit system
# Anotar: Hardening Index, Warnings, Suggestions
```

**Paso 9: Configurar fail2ban (adicional)**
```bash
# Proposito: Bloquear IPs con intentos fallidos
sudo apk add fail2ban
sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
sudo nano /etc/fail2ban/jail.local
# Habilitar seccion [sshd]
# maxretry = 3
# bantime = 3600

sudo rc-service fail2ban start
sudo rc-update add fail2ban default
```

**Paso 10: Verificar cambios**
```bash
# Verificar reglas de firewall
sudo iptables -L -n

# Verificar puertos abiertos
sudo netstat -tlnp

# Verificar configuracion SSH
sudo sshd -T | grep -E "(permitrootlogin|maxauthtries)"

# Verificar sysctl
sudo sysctl kernel.randomize_va_space
```

**Resultado esperado:**
```
kernel.randomize_va_space = 2
```
ASLR activado en modo completo (2).

### 9. Ejercicio 3 - Auditoria con Lynis antes/despues

**Enunciado:** Ejecutar Lynis antes del hardening, guardar el reporte, aplicar hardening, ejecutar Lynis de nuevo, y comparar los resultados.

##### Solucion

**Paso 1: Lynis antes del hardening (inmediatamente despues de instalar Alpine)**

```bash
# Ejecutar auditoria inicial
sudo lynis audit system --report-file /tmp/lynis-antes.report
```

**Resumen tipico de Alpine recien instalado:**
```
Hardening index : 67/100
Tests performed: 233
Warnings: 6
Suggestions: 18
```

**Warnings comunes en Alpine recien instalado:**
```
[!] No password aging configured (AUTH-9286)
[!] System has no active firewall (FIRE-4512)
[!] SSH PermitRootLogin is set to yes (SSH-7408)
[!] No password strength tool installed (AUTH-9262)
[!] One or more sysctl values differ from scan profile (KRNL-5820)
[!] No tool for core dumps analysis installed (FILE-7524)
```

**Paso 2: Aplicar hardening (los 10 pasos del Ejercicio 2).**

**Paso 3: Lynis despues del hardening**

```bash
sudo lynis audit system --report-file /tmp/lynis-despues.report
```

**Resumen tipico despues del hardening:**
```
Hardening index : 88/100
Tests performed: 237
Warnings: 2
Suggestions: 7
```

**Warnings que persisten (tipicamente):**
```
[!] No password aging configured (AUTH-9286) <- requiere instalar y configurar shadow
[!] No password strength tool installed (AUTH-9262) <- instalar pwgen o cracklib
```

**Paso 4: Tabla comparativa**

| Indicador | Antes del hardening | Despues del hardening | Mejora |
|-----------|-------------------|----------------------|--------|
| Hardening Index | 67/100 | 88/100 | +21 puntos |
| Warnings | 6 | 2 | -4 |
| Suggestions | 18 | 7 | -11 |
| Tests realizados | 233 | 237 | +4 (nuevas pruebas posibles) |
| Firewall | No detectado | iptables activo | Nuevo |
| SSH PermitRootLogin | yes | no | Corregido |
| Kernel params | Por defecto | Optimizados | Corregido |
| Fail2ban | No instalado | Instalado y activo | Nuevo |

**Paso 5: Interpretacion**

- El Hardening Index subio 21 puntos, de 67 (aceptable) a 88 (bueno-muy bueno).
- Los warnings se redujeron de 6 a 2. Los que quedan son menores (politica de contrasenas).
- Las suggestions bajaron de 18 a 7. Las que quedan son para un nivel 2 de hardening.
- Alpine parte de una base mas segura que Ubuntu (67 vs ~63 de Ubuntu), pero igual hay margen de mejora.

**Posibles mejoras adicionales (para llegar a 95+):**
1. Configurar politicas de contrasenas (pw quality, aging)
2. Instalar y configurar AIDE (deteccion de cambios en archivos)
3. Configurar rsyslog para enviar logs a un servidor central
4. Deshabilitar modulos del kernel (USB, Bluetooth, etc.)
5. Configurar auditd para auditoria de eventos

### 10. Ejercicio 4 - Escaneo remoto del sistema endurecido

**Enunciado:** Desde otra maquina (host o VM), escanear la VM endurecida con nmap para verificar que los puertos innecesarios estan cerrados y que la configuracion de seguridad es correcta.

##### Solucion

**Paso 1: Obtener la IP de la VM endurecida**

```bash
# En la VM Alpine
ip addr show eth0
```

**Salida:**
```
2: eth0: ... inet 10.0.2.15/24 ...
```

La IP es `10.0.2.15` (en modo NAT). Desde el host (tu PC), no puedes acceder directamente a 10.0.2.15 por que NAT aísla la VM.

**Solucion:** Para poder escanear desde el host, necesitas:
1. Cambiar la red a "Bridge" (Adaptador puente) en VirtualBox, o
2. Crear una segunda VM conectada por "Red Interna"

**Para este ejercicio, usaremos modo Bridge:**

1. Apagar la VM: `sudo poweroff`
2. En VirtualBox: Configuracion -> Red -> Adaptador 1 -> "Adaptador puente"
3. Iniciar la VM de nuevo
4. Verificar la nueva IP: `ip addr show eth0` (ahora sera una IP de tu red local, ej: 192.168.1.x)

**Paso 2: Desde el host (tu PC), escanear la VM**

```bash
# Escaneo de puertos completo (65535 puertos TCP)
nmap -sS -sV -p- 192.168.1.x

# Reemplazar 192.168.1.x con la IP real de la VM
```

**Salida esperada (con hardening aplicado):**
```
Starting Nmap 7.95 ( https://nmap.org ) at 2026-06-25 10:00
Nmap scan report for 192.168.1.x
Host is up (0.0012s latency).
Not shown: 65534 filtered ports
PORT      STATE SERVICE VERSION
22/tcp    open  ssh     OpenSSH 9.3 (protocol 2.0)
2222/tcp  open  ssh     OpenSSH 9.3 (protocol 2.0)  <-- si cambiaste puerto
```

**Analisis:**
- Solo el puerto SSH (22 y/o 2222) esta abierto
- Los 65534 puertos restantes aparecen como "filtered" (firewall los bloquea)
- No hay FTP, HTTP, ni otros servicios

**Paso 3: Escaneo de deteccion de SO**

```bash
nmap -O 192.168.1.x
```

**Salida esperada:**
```
Device type: general purpose
Running: Linux 6.X
OS CPE: cpe:/o:linux:linux_kernel:6.6
OS details: Linux 6.6.0 (Alpine Linux)
Network Distance: 1 hop
```

Notar que nmap detecta que es Alpine ("Linux 6.6.0 (Alpine Linux)"). Si quieres ocultar esto, puedes modificar los valores TTL del kernel, pero es una medida avanzada.

**Paso 4: Escaneo de scripts basicos**

```bash
nmap -sC 192.168.1.x
```

**Salida esperada:**
```
PORT     STATE SERVICE
22/tcp   open  ssh
| ssh-hostkey: 
|   256 SHA256:abcdef1234567890 (ED25519)
|_  256 SHA256:1234567890abcdef (RSA)
| ssh-auth-methods: 
|   Supported authentication methods: 
|     publickey
|_    password
```

**Paso 5: Escaneo UDP (puertos comunes)**

```bash
sudo nmap -sU --top-ports 20 192.168.1.x
```

**Salida esperada:**
```
PORT      STATE         SERVICE
53/udp    closed        domain
67/udp    open|filtered dhcps
68/udp    open|filtered dhcpc
123/udp   closed        ntp
161/udp   closed        snmp
```

Solo DHCP (puertos 67-68) puede aparecer como open|filtered, que es normal para un cliente DHCP.

**Paso 6: Verificar version de SSH (que no sea vulnerable)**

```bash
nmap -sV --script=ssh2-enum-algos 192.168.1.x
```

**Salida esperada:**
```
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.3 (protocol 2.0)
| ssh2-enum-algos: 
|   kex_algorithms: (9)
|       curve25519-sha256
|       ecdh-sha2-nistp256
|       ...
|   server_host_key_algorithms: (3)
|       rsa-sha2-512
|       ...
```

**Paso 7: Tabla comparativa de escaneo**

| Prueba | Resultado | Interpretacion |
|--------|-----------|----------------|
| Escaneo de puertos (-p-) | Solo 22/tcp abierto | Firewall bloquea el resto |
| Deteccion de SO (-O) | Linux 6.6 (Alpine) | SO detectado correctamente |
| Scripts NSE (-sC) | SSH host key, auth methods | No se encontraron vulnerabilidades |
| Escaneo UDP | Solo DHCP visible | Sin servicios UDP innecesarios |
| SSH algorithms | Algoritmos modernos | OpenSSH 9.3 usa cifrados seguros |

**Conclusion:** El sistema endurecido solo expone el servicio SSH. Los firewalls bloquean cualquier intento de conexion a otros puertos. Esto es lo que queremos lograr con hardening: minimizar la superficie de ataque al maximo.

### 11. Ejercicio 5 - Crear script de hardening automatizado

**Enunciado:** Escribir un script bash que automatice los pasos de hardening para Alpine Linux.

##### Solucion

```bash
#!/bin/bash
# ==============================================
# Script: hardening-alpine.sh
# Descripcion: Automatiza el hardening basico de Alpine Linux
# Uso: sudo ./hardening-alpine.sh
# ==============================================

# Verificar que se ejecuta como root
if [ "$(id -u)" -ne 0 ]; then
    echo "ERROR: Este script debe ejecutarse como root (sudo)."
    exit 1
fi

echo "=========================================="
echo "Iniciando hardening de Alpine Linux"
echo "=========================================="

# --------------------------------------------------
# Paso 1: Actualizar sistema
# --------------------------------------------------
echo "[1/10] Actualizando sistema..."
apk update && apk upgrade -y

# --------------------------------------------------
# Paso 2: Crear usuario admin (si no existe)
# --------------------------------------------------
echo "[2/10] Creando usuario admin..."
if ! id -u admin >/dev/null 2>&1; then
    adduser -D admin
    echo "admin:CambiarContra123!" | chpasswd  # CAMBIAR CONTRASENA!
    addgroup admin wheel
else
    echo "     Usuario admin ya existe."
fi

# Instalar sudo y configurar
apk add sudo
if ! grep -q "^%wheel ALL=(ALL) ALL" /etc/sudoers; then
    echo "%wheel ALL=(ALL) ALL" >> /etc/sudoers
fi

# --------------------------------------------------
# Paso 3: Hardening de SSH
# --------------------------------------------------
echo "[3/10] Configurando hardening de SSH..."
SSHD_CONFIG="/etc/ssh/sshd_config"

# Hacer backup
cp "$SSHD_CONFIG" "${SSHD_CONFIG}.bak"

# Aplicar configuraciones
sed -i 's/^PermitRootLogin.*/PermitRootLogin no/' "$SSHD_CONFIG"
sed -i 's/^#PermitRootLogin.*/PermitRootLogin no/' "$SSHD_CONFIG"
sed -i 's/^MaxAuthTries.*/MaxAuthTries 3/' "$SSHD_CONFIG"
sed -i 's/^#MaxAuthTries.*/MaxAuthTries 3/' "$SSHD_CONFIG"
sed -i 's/^ClientAliveInterval.*/ClientAliveInterval 300/' "$SSHD_CONFIG"
sed -i 's/^#ClientAliveInterval.*/ClientAliveInterval 300/' "$SSHD_CONFIG"
sed -i 's/^ClientAliveCountMax.*/ClientAliveCountMax 0/' "$SSHD_CONFIG"
sed -i 's/^#ClientAliveCountMax.*/ClientAliveCountMax 0/' "$SSHD_CONFIG"
sed -i 's/^PermitEmptyPasswords.*/PermitEmptyPasswords no/' "$SSHD_CONFIG"

# Verificar sintaxis y reiniciar
sshd -t && rc-service sshd restart

# --------------------------------------------------
# Paso 4: Firewall con iptables
# --------------------------------------------------
echo "[4/10] Configurando firewall..."
apk add iptables ip6tables

# Crear script de firewall
cat > /etc/init.d/firewall-rules << 'EOF'
#!/sbin/openrc-run
description="Firewall rules"
depend() { need net; }
start() {
    ebegin "Loading firewall rules"
    iptables -F; iptables -X; iptables -t nat -F
    iptables -P INPUT DROP
    iptables -P FORWARD DROP
    iptables -P OUTPUT ACCEPT
    iptables -A INPUT -i lo -j ACCEPT
    iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
    iptables -A INPUT -p tcp --dport 22 -j ACCEPT
    iptables -A INPUT -p icmp --icmp-type echo-request -m limit --limit 10/second -j ACCEPT
    iptables -A INPUT -j LOG --log-prefix "FW-DROP: " --log-level 4
    eend $?
}
stop() {
    ebegin "Unloading firewall rules"
    iptables -P INPUT ACCEPT
    iptables -P FORWARD ACCEPT
    iptables -P OUTPUT ACCEPT
    iptables -F; iptables -X; iptables -t nat -F
    eend $?
}
EOF

chmod +x /etc/init.d/firewall-rules
rc-update add firewall-rules default
rc-service firewall-rules start

# --------------------------------------------------
# Paso 5: Servicios innecesarios
# --------------------------------------------------
echo "[5/10] Revisando servicios innecesarios..."
# Detener solo si existen
for svc in acpid; do
    if rc-service "$svc" status 2>/dev/null; then
        rc-service "$svc" stop
        rc-update del "$svc"
        echo "     Servicio $svc deshabilitado."
    fi
done

# --------------------------------------------------
# Paso 6: Logrotate
# --------------------------------------------------
echo "[6/10] Configurando logrotate..."
apk add logrotate
cat > /etc/logrotate.d/hardening << 'EOF'
/var/log/*.log {
    weekly
    rotate 4
    compress
    delaycompress
    missingok
    notifempty
    postrotate
        rc-service syslog restart 2>/dev/null || true
    endscript
}
EOF

# --------------------------------------------------
# Paso 7: Kernel hardening (sysctl)
# --------------------------------------------------
echo "[7/10] Configurando parametros del kernel..."
cat > /etc/sysctl.d/hardening.conf << 'EOF'
net.ipv4.tcp_syncookies=1
net.ipv4.ip_forward=0
net.ipv4.conf.all.rp_filter=1
net.ipv4.conf.default.rp_filter=1
net.ipv4.conf.all.accept_source_route=0
net.ipv4.conf.default.accept_source_route=0
net.ipv4.conf.all.accept_redirects=0
net.ipv4.conf.default.accept_redirects=0
net.ipv6.conf.all.accept_redirects=0
net.ipv4.conf.all.send_redirects=0
net.ipv4.conf.default.send_redirects=0
net.ipv4.tcp_rfc1337=1
net.ipv4.icmp_echo_ignore_broadcasts=1
net.ipv4.icmp_ignore_bogus_error_responses=1
net.ipv4.conf.all.log_martians=1
net.ipv4.conf.default.log_martians=1
fs.suid_dumpable=0
kernel.randomize_va_space=2
kernel.dmesg_restrict=1
kernel.kptr_restrict=2
EOF

sysctl -p /etc/sysctl.d/hardening.conf

# --------------------------------------------------
# Paso 8: Fail2ban
# --------------------------------------------------
echo "[8/10] Instalando fail2ban..."
apk add fail2ban
if [ -f /etc/fail2ban/jail.conf ] && [ ! -f /etc/fail2ban/jail.local ]; then
    cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
fi

# Habilitar proteccion SSH en fail2ban
cat > /etc/fail2ban/jail.d/sshd.local << 'EOF'
[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log
maxretry = 3
bantime = 3600
findtime = 600
EOF

rc-service fail2ban start
rc-update add fail2ban default

# --------------------------------------------------
# Paso 9: Instalar Lynis
# --------------------------------------------------
echo "[9/10] Instalando Lynis..."
apk add lynis

# --------------------------------------------------
# Paso 10: Ejecutar auditoria final
# --------------------------------------------------
echo "[10/10] Ejecutando auditoria final..."
lynis audit system --quick

echo ""
echo "=========================================="
echo "Hardening completado!"
echo "Ejecuta 'sudo lynis audit system' para ver el reporte completo."
echo "=========================================="
```

**Como usar el script:**

```bash
# 1. Guardar el script en la VM
nano hardening-alpine.sh
# (pegar el contenido, guardar con Ctrl+X, Y, Enter)

# 2. Hacerlo ejecutable
chmod +x hardening-alpine.sh

# 3. Ejecutar como root
sudo ./hardening-alpine.sh
```

**IMPORTANTE:** Antes de ejecutar el script, cambia la contrasena del usuario admin en la linea:
```bash
echo "admin:CambiarContra123!" | chpasswd  # CAMBIAR ESTO!
```
Por una contrasena segura.

**Que hace el script:**
1. Actualiza el sistema (apk update && apk upgrade)
2. Crea usuario admin con sudo
3. Configura SSH hardening (PermitRootLogin no, MaxAuthTries 3, etc.)
4. Configura firewall iptables
5. Deshabilita servicios innecesarios
6. Configura logrotate
7. Aplica parametros sysctl de hardening
8. Instala y configura fail2ban
9. Instala Lynis
10. Ejecuta auditoria final

### 12. Preguntas y Respuestas

#### Pregunta 1
**Por que Alpine Linux es considerado seguro por defecto?**

**Respuesta:** Alpine Linux se diseno con seguridad como prioridad. Varias caracteristicas lo hacen mas seguro que otras distribuciones por defecto: (1) Usa musl libc en lugar de glibc. musl es una implementacion mas simple y moderna de la biblioteca C estandar, con menos lineas de codigo y por lo tanto menor superficie de ataque. (2) Todos los paquetes se compilan con PIE (Position Independent Executables) y stack smashing protection, lo que dificulta la explotacion de buffer overflows. (3) ASLR (Address Space Layout Randomization) esta activado por defecto con `kernel.randomize_va_space=2`. (4) La instalacion base minimiza tiene solo ~30 paquetes, frente a ~300+ de Ubuntu Server, lo que reduce drasticamente la superficie de ataque. (5) No tiene servicios innecesarios corriendo por defecto. (6) Usa OpenRC en lugar de systemd, que es mas simple y tiene menos lineas de codigo. Sin embargo, ninguna distribucion es 100% segura "out of the box": el hardening siempre es necesario.

#### Pregunta 2
**Cual es la diferencia entre apk y apt?**

**Respuesta:** `apk` es el gestor de paquetes de Alpine Linux (Alpine Package Keeper), mientras que `apt` es el gestor de Debian/Ubuntu (Advanced Package Tool). Las principales diferencias: (1) Comandos: en `apk` se usa `apk add <paquete>` para instalar, `apk del <paquete>` para eliminar; en `apt` se usa `apt install <paquete>` y `apt remove <paquete>`. (2) Actualizacion: `apk update` actualiza la lista, `apk upgrade` actualiza los paquetes; en `apt` es `apt update` y `apt upgrade`. (3) Busqueda: `apk search <termino>` vs `apt search <termino>`. (4) Formato de paquetes: `apk` usa .apk, `apt` usa .deb. (5) Dependencias: `apk` resuelve dependencias de forma mas agresiva (posiblemente rompiendo paquetes). (6) Atomicidad: `apk` garantiza que las operaciones son atomicas (o se completa todo o no se hace nada), mientras que `apt` puede quedar en un estado inconsistente si se interrumpe. En general, `apt` es mas tolerante y facil de usar, mientras que `apk` es mas minimalista y rapido.

#### Pregunta 3
**Que hace `kernel.randomize_va_space=2`?**

**Respuesta:** Este parametro del kernel controla ASLR (Address Space Layout Randomization). ASLR es una tecnica de seguridad que randomiza las direcciones de memoria donde se cargan las diferentes partes de un proceso: el codigo (text), las variables (data/bss), la pila (stack), y el monticulo (heap). Los valores posibles son: 0 = desactivado (no hay randomizacion, las direcciones son predecibles), 1 = randomizacion parcial (solo stack, mmap, y shared memory se randomizan; el heap no se randomiza completamente). 2 = randomizacion completa (stack, mmap, shared memory, y heap se randomizan con maxima entropia). El valor 2 es el mas seguro porque hace mucho mas dificil explotar vulnerabilidades de corrupcion de memoria (buffer overflows, use-after-free, etc.). Sin ASLR, un atacante sabe exactamente donde estan las funciones y variables del programa, y puede saltar a direcciones especificas. Con ASLR activado, las direcciones cambian cada vez que se ejecuta un proceso, por lo que el atacante no puede predecir donde caera su exploit. Alpine Linux ya trae `randomize_va_space=2` por defecto.

#### Pregunta 4
**Para que sirve `rp_filter`?**

**Respuesta:** `rp_filter` (Reverse Path Filtering) es un parametro del kernel que controla la validacion de la ruta de origen de los paquetes IP. Cuando esta activado (valor 1), el kernel verifica que la direccion IP de origen de un paquete entrante sea accesible a traves de la misma interfaz por la que llego. En otras palabras: si un paquete llega por la interfaz eth0 diciendo "vengo de la IP 10.0.0.1", el kernel consulta la tabla de enrutamiento y verifica que para llegar a 10.0.0.1, la ruta correcta sea a traves de eth0. Si la ruta correcta es por otra interfaz (eth1, por ejemplo), el paquete se descarta. Esto previene ataques de IP spoofing, donde un atacante envia paquetes con una direccion de origen falsa. Sin `rp_filter`, un atacante podria enviar paquetes desde una red externa haciendose pasar por un dispositivo de la red interna. Con `rp_filter=1`, estos paquetes falsos se descartan automaticamente. Se recomienda activarlo en todas las interfaces (`net.ipv4.conf.all.rp_filter=1`).

#### Pregunta 5
**Por que cambiar el puerto SSH ayuda a la seguridad?**

**Respuesta:** Cambiar el puerto SSH del puerto por defecto (22) a un puerto no estandar (ej: 2222, 8022, 22022) ayuda a reducir el "ruido" de ataques automatizados en Internet. La mayoria de los bots y scripts de ataque escanean el puerto 22 por defecto buscando servicios SSH. Si cambias el puerto, esos ataques automatizados no encuentran tu servicio SSH porque buscan en el puerto equivocado. Sin embargo, esto NO es una medida de seguridad real contra un atacante determinado: cualquiera que haga un escaneo de puertos completo (nmap -p-) encontrara tu SSH en cualquier puerto donde este escuchando. Por eso se llama "security through obscurity" (seguridad por oscuridad) y no debe ser la unica medida de proteccion. Es util como complemento a: PermitRootLogin no, autenticacion por llaves, fail2ban, y firewall restrictivo. La combinacion de cambiar puerto + fail2ban + solo llaves es muy efectiva contra ataques automatizados.

#### Pregunta 6
**Que diferencia hay entre OpenRC y systemd en terminos de seguridad?**

**Respuesta:** OpenRC (usado por Alpine) y systemd (usado por Ubuntu, Debian, Fedora) son sistemas de inicio (init systems) que gestionan servicios. En terminos de seguridad: (1) Complejidad: OpenRC es mucho mas simple (~15,000 lineas de codigo en C/shell) que systemd (~1.3 millones de lineas). Menos codigo significa menor superficie de ataque y menos vulnerabilidades potenciales. (2) Aislamiento: systemd ofrece caracteristicas de seguridad avanzadas como `PrivateTmp`, `ProtectSystem`, `NoNewPrivileges`, `CapabilityBoundingSet` que OpenRC no tiene. (3) Sandboxing: systemd tiene integracion con namespaces de Linux (PID, network, mount, user) para aislar servicios, mientras que en OpenRC esto requiere configuracion manual. (4) Logging: systemd tiene journald con logs estructurados y firmados; OpenRC usa syslog tradicional. (5) Tamaño: systemd es un ecosistema enorme que incluye init, logging, DNS resolver (systemd-resolved), NTP (systemd-timesyncd), y mas. Cada componente adicional es superficie de ataque. En resumen: OpenRC es mas seguro por simplicidad (menos codigo, menos bugs), mientras que systemd ofrece mas herramientas de seguridad pero con mayor complejidad. Para un servidor minimalista, OpenRC es preferible.

---

## Tarea / Lectura Recomendada

1. **Practicar:** Instala Alpine Linux en VirtualBox siguiendo los pasos del Ejercicio 1. Toma un snapshot antes de aplicar hardening
2. **Practicar:** Aplica manualmente los 10 pasos de hardening del Ejercicio 2. Documenta cada cambio
3. **Practicar:** Ejecuta Lynis antes y despues del hardening. Compara el Hardening Index
4. **Practicar:** Desde tu PC host, escanea la VM endurecida con nmap (Ejercicio 4). Verifica los puertos
5. **Practicar:** Ejecuta el script de hardening automatizado (Ejercicio 5) en una segunda VM limpia. Compara los resultados con el hardening manual
6. **Leer:** Documentacion oficial de Alpine Linux - https://docs.alpinelinux.org/ (Wiki y manual de instalacion)
7. **Leer:** CIS Benchmark para Alpine Linux (si existe, o la guia generica de hardening para Linux)
8. **Leer:** "Unix and Linux System Administration Handbook" - capitulos sobre seguridad y hardening
9. **Explorar:** DevSec Hardening Framework (Ansible roles) - https://devsec.io/
10. **Explorar:** OpenSCAP - https://www.open-scap.org/ (herramienta de auditoria automatizada)
11. **Explorar:** Lynis Enterprise - https://cisofy.com/lynis/ (version enterprise con reporting centralizado)
12. **Proyecto:** Crea una VM con Ubuntu Server minimal y aplica el mismo proceso de hardening. Compara las diferencias con Alpine Linux en cuanto a: numero de paquetes, servicios activos, Hardening Index de Lynis, y puertos abiertos antes/despues
