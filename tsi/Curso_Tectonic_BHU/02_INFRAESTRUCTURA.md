# 02 - Infraestructura de Red Virtual: Banco del Sol

## Curso Tectonic Cyber Range - BHU Uruguay

---

## 1. Descripcion General

Este documento describe la infraestructura de red virtual del entorno de laboratorio **"Banco del Sol"**, diseñado para el curso de Tectonic Cyber Range en la Universidad de la República (UdelaR) - BHU Uruguay. El entorno simula una entidad financiera con una topologia de red segmentada en zonas, permitiendo practicas controladas de ciberseguridad ofensiva y defensiva.

El laboratorio esta compuesto por **8 maquinas virtuales** distribuidas en **4 zonas de red**, interconectadas mediante un gateway VPN y reglas de enrutamiento y firewall configuradas.

---

## 2. Topologia de Red

### 2.1 Diagrama de Zonas

```
                        INTERNET SIMULADO (172.16.0.0/24)
                                  |
                            [ VPN Gateway ]
                                  |
                          +-------+-------+
                          |               |
                     MANAGEMENT        DMZ (10.10.1.0/24)
                  (10.10.0.0/24)          |
                          |          +----+----+
                     +----+----+     |         |
                     |         |  WebServer  MailServer
                  Instructor  |
                              |
                    INTERNAL (10.10.2.0/24)
                          |
              +-----------+-----------+
              |           |           |
         FileServer  Database    DomainController
              |
          Workstation
```

### 2.2 Zona DMZ (10.10.1.0/24)

La zona DMZ (Demilitarized Zone) alberga los servidores expuestos directamente a la simulacion de Internet. Estos servidores son los primeros objetivos de ataque y la linea inicial de defensa.

**Servidores en DMZ:**

| VM              | IP              | Servicios Principales                         | Puertos                  |
|-----------------|-----------------|-----------------------------------------------|--------------------------|
| webserver       | 10.10.1.10      | Apache HTTP, Nginx Reverse Proxy              | 80, 443, 8080            |
| mailserver      | 10.10.1.20      | Postfix (SMTP), Dovecot (IMAP/POP3)          | 25, 587, 993, 995, 143   |

**Funcion:** Servidores publicos que procesan solicitudes externas. El webserver aloja la aplicacion web del banco. El mailserver gestiona la comunicacion interna y externa de la entidad.

### 2.3 Zona Interna (10.10.2.0/24)

La zona interna es la red privada donde se encuentran los servidores criticos y las estaciones de trabajo. Acceso restringido solo desde DMZ y Management mediante reglas de firewall especificas.

**Servidores en zona interna:**

| VM                  | IP              | Servicios Principales                                       | Puertos                        |
|---------------------|-----------------|-------------------------------------------------------------|--------------------------------|
| fileserver          | 10.10.2.10      | Samba (SMB), SSH                                            | 445, 139, 22                   |
| database            | 10.10.2.20      | MySQL 8.0, PostgreSQL 15                                    | 3306, 5432                     |
| domaincontroller    | 10.10.2.5       | Samba AD DC, LDAP, Kerberos, DNS                            | 389, 636, 88, 53, 445          |
| workstation         | 10.10.2.100     | Windows 10, RDP, SMB                                         | 3389, 445                      |

**Funcion:** Almacenan datos sensibles del banco. El domain controller gestiona la autenticacion centralizada. La workstation representa el equipo de un empleado y es victima principal de ataques de ingenieria social y movimiento lateral.

### 2.4 Zona de Management (10.10.0.0/24)

Zona reservada para el instructor y la administracion del laboratorio. Acceso total a todas las demas zonas.

| VM           | IP              | Servicios Principales                        | Puertos              |
|--------------|-----------------|----------------------------------------------|----------------------|
| instructor   | 10.10.0.10      | SSH, Nmap, Metasploit, Burp Suite            | 22, Various          |

**Funcion:** Maquina del instructor para monitorear, configurar y administrar el laboratorio. Tiene acceso SSH a todas las VMs y puede observar el trafico de red.

### 2.5 Zona Internet Simulado (172.16.0.0/24)

Zona que simula una red externa no confiable. Aqui se encuentra la maquina atacante.

| VM        | IP              | Servicios Principales                                    | Puertos              |
|-----------|-----------------|----------------------------------------------------------|----------------------|
| attacker  | 172.16.0.10     | Kali Linux, Metasploit, Burp Suite, SQLmap, Nikto       | Various              |

**Funcion:** Maquina de ataque desde la cual se ejecutan las praticas ofensivas del curso. Simula un atacante externo con acceso a la red Internet simulada.

### 2.6 Gateway VPN

El gateway VPN conecta la zona Internet simulada con las zonas internas. Implementa un tunel VPN que permite al atacante acceder a la DMZ y, bajo ciertas condiciones, a la zona interna.

| Componente        | IP Externa         | IP Interna        | Protocolo   |
|-------------------|--------------------|--------------------|-------------|
| VPN Gateway       | 172.16.0.1         | 10.10.1.1 / 10.10.2.1 | WireGuard  |

---

## 3. Configuracion YAML del Laboratorio

A continuacion se presenta la configuracion completa en formato YAML para el laboratorio base **banco_del_sol_base.yml**.

### 3.1 Archivo de Laboratorio: banco_del_sol_base.yml

```yaml
# banco_del_sol_base.yml
# Laboratorio: Banco del Sol - Tectonic Cyber Range
# Curso: Ciberseguridad BHU UdelaR
# Autor: Departamento de Ciberseguridad BHU
# Version: 1.0.0

lab:
  name: "Banco del Sol - Base"
  description: "Entorno de laboratorio que simula la infraestructura de red de una entidad financiera uruguaya para praticas de ciberseguridad"
  version: "1.0.0"
  edition: "banco_del_sol_base"
  author: "BHU UdelaR"
  difficulty: "intermediate"
  estimated_duration: "4 horas"

# =============================================================================
# DEFINICION DE REDES
# =============================================================================
networks:

  - name: "mgmt_net"
    description: "Red de gestion - Acceso del instructor"
    type: "managed"
    subnet: "10.10.0.0/24"
    gateway: "10.10.0.1"
    dhcp_range: "10.10.0.100-10.10.0.200"
    bridge: "br-mgmt"
    vlan_id: 100

  - name: "dmz_net"
    description: "Zona DMZ - Servidores expuestos"
    type: "managed"
    subnet: "10.10.1.0/24"
    gateway: "10.10.1.1"
    dhcp_range: "10.10.1.100-10.10.1.200"
    bridge: "br-dmz"
    vlan_id: 200

  - name: "internal_net"
    description: "Red interna - Servidores criticos y estaciones de trabajo"
    type: "managed"
    subnet: "10.10.2.0/24"
    gateway: "10.10.2.1"
    dhcp_range: "10.10.2.100-10.10.2.200"
    bridge: "br-internal"
    vlan_id: 300

  - name: "internet_net"
    description: "Zona Internet simulado - Red externa no confiable"
    type: "managed"
    subnet: "172.16.0.0/24"
    gateway: "172.16.0.1"
    dhcp_range: "172.16.0.100-172.16.0.200"
    bridge: "br-internet"
    vlan_id: 400

# =============================================================================
# DEFINICION DE MAQUINAS VIRTUALES
# =============================================================================
vms:

  # ---------------------------------------------------------------------------
  # VM: instructor
  # Zona: Management (10.10.0.0/24)
  # Funcion: Maquina del instructor para administracion y monitoreo
  # ---------------------------------------------------------------------------
  - name: "instructor"
    description: "Maquina del instructor - Administracion del laboratorio"
    image: "ubuntu-server-22.04"
    os: "linux"
    arch: "amd64"
    resources:
      cpu: 2
      ram: 4096
      disk: 40
    interfaces:
      - network: "mgmt_net"
        ip: "10.10.0.10"
        netmask: "255.255.255.0"
        gateway: "10.10.0.1"
    ssh:
      enabled: true
      port: 22
      user: "instructor"
      auth_method: "key"
      key_path: "keys/instructor_key"
    packages:
      - "nmap"
      - "metasploit-framework"
      - "burpsuite"
      - "wireshark"
      - "tcpdump"
      - "ansible"
      - "python3"
      - "python3-pip"
      - "curl"
      - "git"
    startup_services:
      - "ssh"
      - "snmpd"
    provision:
      - type: "shell"
        script: "scripts/instructor_setup.sh"
      - type: "file"
        source: "configs/instructor/ansible.cfg"
        destination: "/etc/ansible/ansible.cfg"
      - type: "file"
        source: "configs/instructor/hosts"
        destination: "/etc/ansible/hosts"

  # ---------------------------------------------------------------------------
  # VM: attacker
  # Zona: Internet simulado (172.16.0.0/24)
  # Funcion: Maquina de ataque con herramientas ofensivas
  # ---------------------------------------------------------------------------
  - name: "attacker"
    description: "Maquina atacante - Kali Linux con herramientas ofensivas"
    image: "kali-linux-2024.1"
    os: "linux"
    arch: "amd64"
    resources:
      cpu: 4
      ram: 8192
      disk: 80
    interfaces:
      - network: "internet_net"
        ip: "172.16.0.10"
        netmask: "255.255.255.0"
        gateway: "172.16.0.1"
    ssh:
      enabled: true
      port: 22
      user: "kali"
      auth_method: "password"
      password: "kali"
    packages:
      - "metasploit-framework"
      - "burpsuite"
      - "sqlmap"
      - "nikto"
      - "dirb"
      - "hydra"
      - "john"
      - "hashcat"
      - "aircrack-ng"
      - "set"
      - "ettercap-text-only"
      - "responder"
      - "impacket-scripts"
      - "bloodhound"
      - "crackmapexec"
      - "enum4linux"
      - "smbclient"
      - "nmap"
      - "wireshark"
      - "python3"
      - "python3-pip"
    startup_services:
      - "ssh"
      - "postgresql"
    provision:
      - type: "shell"
        script: "scripts/attacker_setup.sh"
      - type: "file"
        source: "configs/attacker/workspace"
        destination: "/home/kali/workspace"

  # ---------------------------------------------------------------------------
  # VM: webserver
  # Zona: DMZ (10.10.1.0/24)
  # Funcion: Servidor web del banco - Apache/Nginx
  # ---------------------------------------------------------------------------
  - name: "webserver"
    description: "Servidor web del Banco del Sol - Apache + Nginx"
    image: "ubuntu-server-22.04"
    os: "linux"
    arch: "amd64"
    resources:
      cpu: 2
      ram: 4096
      disk: 40
    interfaces:
      - network: "dmz_net"
        ip: "10.10.1.10"
        netmask: "255.255.255.0"
        gateway: "10.10.1.1"
      - network: "internal_net"
        ip: "10.10.2.11"
        netmask: "255.255.255.0"
        gateway: "10.10.2.1"
    ssh:
      enabled: true
      port: 22
      user: "webadmin"
      auth_method: "key"
      key_path: "keys/webserver_key"
    packages:
      - "apache2"
      - "nginx"
      - "php8.1"
      - "php8.1-mysql"
      - "php8.1-fpm"
      - "libapache2-mod-php8.1"
      - "certbot"
      - "python3-certbot-nginx"
      - "fail2ban"
      - "ufw"
      - "logwatch"
    startup_services:
      - "apache2"
      - "nginx"
      - "php8.1-fpm"
      - "ssh"
      - "fail2ban"
    provision:
      - type: "shell"
        script: "scripts/webserver_setup.sh"
      - type: "file"
        source: "configs/webserver/apache.conf"
        destination: "/etc/apache2/sites-available/banco_del_sol.conf"
      - type: "file"
        source: "configs/webserver/nginx.conf"
        destination: "/etc/nginx/sites-available/banco_del_sol.conf"
      - type: "file"
        source: "configs/webserver/index.html"
        destination: "/var/www/banco_del_sol/index.html"
      - type: "file"
        source: "configs/webserver/robots.txt"
        destination: "/var/www/banco_del_sol/robots.txt"

  # ---------------------------------------------------------------------------
  # VM: mailserver
  # Zona: DMZ (10.10.1.0/24)
  # Funcion: Servidor de correo electronico del banco
  # ---------------------------------------------------------------------------
  - name: "mailserver"
    description: "Servidor de correo del Banco del Sol - Postfix + Dovecot"
    image: "ubuntu-server-22.04"
    os: "linux"
    arch: "amd64"
    resources:
      cpu: 2
      ram: 4096
      disk: 40
    interfaces:
      - network: "dmz_net"
        ip: "10.10.1.20"
        netmask: "255.255.255.0"
        gateway: "10.10.1.1"
    ssh:
      enabled: true
      port: 22
      user: "mailadmin"
      auth_method: "key"
      key_path: "keys/mailserver_key"
    packages:
      - "postfix"
      - "dovecot-core"
      - "dovecot-imapd"
      - "dovecot-pop3d"
      - "dovecot-sieve"
      - "dovecot-managesieved"
      - "roundcube"
      - "roundcube-mysql"
      - "postfix-mysql"
      - "opendkim"
      - "opendkim-tools"
      - "spamassassin"
      - "clamav"
      - "clamav-daemon"
      - "fail2ban"
      - "ufw"
    startup_services:
      - "postfix"
      - "dovecot"
      - "opendkim"
      - "spamassassin"
      - "clamav-daemon"
      - "ssh"
      - "fail2ban"
    provision:
      - type: "shell"
        script: "scripts/mailserver_setup.sh"
      - type: "file"
        source: "configs/mailserver/postfix/main.cf"
        destination: "/etc/postfix/main.cf"
      - type: "file"
        source: "configs/mailserver/dovecot/dovecot.conf"
        destination: "/etc/dovecot/dovecot.conf"
      - type: "file"
        source: "configs/mailserver/dovecot/10-mail.conf"
        destination: "/etc/dovecot/conf.d/10-mail.conf"
      - type: "file"
        source: "configs/mailserver/dovecot/10-ssl.conf"
        destination: "/etc/dovecot/conf.d/10-ssl.conf"

  # ---------------------------------------------------------------------------
  # VM: fileserver
  # Zona: Interna (10.10.2.0/24)
  # Funcion: Servidor de archivos compartidos con Samba
  # ---------------------------------------------------------------------------
  - name: "fileserver"
    description: "Servidor de archivos del Banco del Sol - Samba SMB"
    image: "ubuntu-server-22.04"
    os: "linux"
    arch: "amd64"
    resources:
      cpu: 2
      ram: 4096
      disk: 80
    interfaces:
      - network: "internal_net"
        ip: "10.10.2.10"
        netmask: "255.255.255.0"
        gateway: "10.10.2.1"
    ssh:
      enabled: true
      port: 22
      user: "fileadmin"
      auth_method: "key"
      key_path: "keys/fileserver_key"
    packages:
      - "samba"
      - "samba-common-bin"
      - "samba-vfs-modules"
      - "cifs-utils"
      - "acl"
      - "attr"
      - "fail2ban"
      - "ufw"
    startup_services:
      - "smbd"
      - "nmbd"
      - "ssh"
      - "fail2ban"
    provision:
      - type: "shell"
        script: "scripts/fileserver_setup.sh"
      - type: "file"
        source: "configs/fileserver/smb.conf"
        destination: "/etc/samba/smb.conf"
      - type: "file"
        source: "configs/fileserver/shares/ventas.conf"
        destination: "/etc/samba/shares/ventas.conf"
      - type: "file"
        source: "configs/fileserver/shares/rrhh.conf"
        destination: "/etc/samba/shares/rrhh.conf"
      - type: "file"
        source: "configs/fileserver/shares/directivos.conf"
        destination: "/etc/samba/shares/directivos.conf"

  # ---------------------------------------------------------------------------
  # VM: database
  # Zona: Interna (10.10.2.0/24)
  # Funcion: Servidor de bases de datos del banco
  # ---------------------------------------------------------------------------
  - name: "database"
    description: "Servidor de bases de datos del Banco del Sol - MySQL + PostgreSQL"
    image: "ubuntu-server-22.04"
    os: "linux"
    arch: "amd64"
    resources:
      cpu: 4
      ram: 8192
      disk: 120
    interfaces:
      - network: "internal_net"
        ip: "10.10.2.20"
        netmask: "255.255.255.0"
        gateway: "10.10.2.1"
    ssh:
      enabled: true
      port: 22
      user: "dbadmin"
      auth_method: "key"
      key_path: "keys/database_key"
    packages:
      - "mysql-server"
      - "mysql-client"
      - "postgresql"
      - "postgresql-contrib"
      - "libpq-dev"
      - "python3-psycopg2"
      - "python3-mysqldb"
      - "fail2ban"
      - "ufw"
    startup_services:
      - "mysql"
      - "postgresql"
      - "ssh"
      - "fail2ban"
    provision:
      - type: "shell"
        script: "scripts/database_setup.sh"
      - type: "file"
        source: "configs/database/mysql/my.cnf"
        destination: "/etc/mysql/mysql.conf.d/custom.cnf"
      - type: "file"
        source: "configs/database/postgresql/postgresql.conf"
        destination: "/etc/postgresql/15/main/conf.d/custom.conf"
      - type: "file"
        source: "configs/database/postgresql/pg_hba.conf"
        destination: "/etc/postgresql/15/main/pg_hba.conf"

  # ---------------------------------------------------------------------------
  # VM: domaincontroller
  # Zona: Interna (10.10.2.0/24)
  # Funcion: Controlador de dominio - Samba AD DC
  # ---------------------------------------------------------------------------
  - name: "domaincontroller"
    description: "Controlador de dominio del Banco del Sol - Samba AD DC"
    image: "ubuntu-server-22.04"
    os: "linux"
    arch: "amd64"
    resources:
      cpu: 2
      ram: 4096
      disk: 40
    interfaces:
      - network: "internal_net"
        ip: "10.10.2.5"
        netmask: "255.255.255.0"
        gateway: "10.10.2.1"
    ssh:
      enabled: true
      port: 22
      user: "dcadmin"
      auth_method: "key"
      key_path: "keys/domaincontroller_key"
    packages:
      - "samba"
      - "samba-dsdb-modules"
      - "samba-vfs-modules"
      - "winbind"
      - "libnss-winbind"
      - "libpam-winbind"
      - "krb5-user"
      - "krb5-config"
      - "ldap-utils"
      - "dns"
      - "bind9"
      - "bind9-utils"
      - "fail2ban"
      - "ufw"
    startup_services:
      - "samba"
      - "bind9"
      - "ssh"
      - "fail2ban"
    provision:
      - type: "shell"
        script: "scripts/domaincontroller_setup.sh"
      - type: "file"
        source: "configs/domaincontroller/samba/ad.conf"
        destination: "/etc/samba/smb.conf"
      - type: "file"
        source: "configs/domaincontroller/krb5.conf"
        destination: "/etc/krb5.conf"
      - type: "file"
        source: "configs/domaincontroller/nsswitch.conf"
        destination: "/etc/nsswitch.conf"

  # ---------------------------------------------------------------------------
  # VM: workstation
  # Zona: Interna (10.10.2.0/24)
  # Funcion: Estacion de trabajo del empleado - Victima principal
  # ---------------------------------------------------------------------------
  - name: "workstation"
    description: "Estacion de trabajo del empleado del Banco del Sol - Windows 10"
    image: "windows-10-22h2"
    os: "windows"
    arch: "amd64"
    resources:
      cpu: 4
      ram: 8192
      disk: 80
    interfaces:
      - network: "internal_net"
        ip: "10.10.2.100"
        netmask: "255.255.255.0"
        gateway: "10.10.2.1"
    rdp:
      enabled: true
      port: 3389
      user: "empleado"
      auth_method: "password"
      password: "BancoDelSol2024!"
    packages:
      - "google-chrome-stable"
      - "microsoft-office-2021"
      - "adobe-reader"
      - "7zip"
      - "putty"
      - "winscp"
      - "sysinternals"
    provision:
      - type: "shell"
        script: "scripts/workstation_setup.ps1"
      - type: "file"
        source: "configs/workstation/desktop"
        destination: "C:/Users/empleado/Desktop"
      - type: "file"
        source: "configs/workstation/documents"
        destination: "C:/Users/empleado/Documents"
      - type: "file"
        source: "configs/workstation/browser_bookmarks"
        destination: "C:/Users/empleado/AppData/Local/Google/Chrome/User Data/Default/Bookmarks"

# =============================================================================
# REGLAS DE ENRUTAMIENTO
# =============================================================================
routing:

  # Regla 1: Management puede acceder a todas las zonas
  - name: "mgmt_full_access"
    description: "La zona de gestion tiene acceso completo a todas las zonas"
    source_zone: "mgmt_net"
    destination_zones:
      - "dmz_net"
      - "internal_net"
    action: "allow"
    priority: 100

  # Regla 2: DMZ puede acceder a zona interna (servicios especificos)
  - name: "dmz_to_internal_services"
    description: "DMZ accede a servicios internos (base de datos, archivos)"
    source_zone: "dmz_net"
    destination_zones:
      - "internal_net"
    services:
      - name: "mysql"
        protocol: "tcp"
        port: 3306
      - name: "postgresql"
        protocol: "tcp"
        port: 5432
      - name: "smb"
        protocol: "tcp"
        port: 445
    action: "allow"
    priority: 200

  # Regla 3: Internet simulado solo accede a DMZ via VPN
  - name: "internet_to_dmz_vpn"
    description: "Internet simulado accede a DMZ a traves del VPN"
    source_zone: "internet_net"
    destination_zones:
      - "dmz_net"
    services:
      - name: "https"
        protocol: "tcp"
        port: 443
      - name: "http"
        protocol: "tcp"
        port: 80
      - name: "smtp"
        protocol: "tcp"
        port: 587
      - name: "submission"
        protocol: "tcp"
        port: 465
      - name: "imaps"
        protocol: "tcp"
        port: 993
    action: "allow"
    priority: 300

  # Regla 4: Internet simulado NO puede acceder directamente a zona interna
  - name: "internet_to_internal_deny"
    description: "Bloqueo de acceso directo de Internet a zona interna"
    source_zone: "internet_net"
    destination_zones:
      - "internal_net"
    action: "deny"
    priority: 400

  # Regla 5: Zona interna puede acceder a Internet simulado (limitado)
  - name: "internal_to_internet_limited"
    description: "Zona interna accede a Internet simulado de forma limitada"
    source_zone: "internal_net"
    destination_zones:
      - "internet_net"
    services:
      - name: "https"
        protocol: "tcp"
        port: 443
    action: "allow"
    priority: 500

  # Regla 6: DMZ puede acceder a Internet simulado
  - name: "dmz_to_internet"
    description: "DMZ accede a Internet simulado para actualizaciones"
    source_zone: "dmz_net"
    destination_zones:
      - "internet_net"
    services:
      - name: "https"
        protocol: "tcp"
        port: 443
      - name: "http"
        protocol: "tcp"
        port: 80
    action: "allow"
    priority: 600

  # Regla por defecto: Denegar todo lo no explicitamente permitido
  - name: "default_deny"
    description: "Politica por defecto - Denegar todo trafico no permitido"
    source_zone: "any"
    destination_zones:
      - "any"
    action: "deny"
    priority: 9999

# =============================================================================
# REGLAS DE ACCESO SSH
# =============================================================================
access_rules:

  ssh_access:

    # Instructor puede SSH a todas las VMs Linux
    - name: "instructor_ssh_all"
      description: "El instructor tiene acceso SSH a todas las maquinas Linux"
      source: "instructor"
      destination:
        - "webserver"
        - "mailserver"
        - "fileserver"
        - "database"
        - "domaincontroller"
        - "attacker"
      port: 22
      auth_method: "key"
      action: "allow"
      priority: 100

    # Attacker puede SSH a DMZ (simula acceso legitimo comprometido)
    - name: "attacker_ssh_dmz"
      description: "Atacante puede SSH a servidores DMZ (simula credenciales comprometidas)"
      source: "attacker"
      destination:
        - "webserver"
        - "mailserver"
      port: 22
      auth_method: "password"
      credentials:
        webserver: "webadmin:webadmin123"
        mailserver: "mailadmin:mailadmin123"
      action: "allow"
      priority: 200

    # Attacker NO puede SSH a zona interna directamente
    - name: "attacker_ssh_internal_deny"
      description: "Atacante NO tiene acceso SSH directo a zona interna"
      source: "attacker"
      destination:
        - "fileserver"
        - "database"
        - "domaincontroller"
      port: 22
      action: "deny"
      priority: 300

  # =============================================================================
  # REGLAS DE FIREWALL (UFW / iptables)
  # =============================================================================
  firewall_rules:

    # --- webserver ---
    webserver:
      - name: "allow_http"
        port: 80
        protocol: "tcp"
        action: "allow"
        direction: "in"
      - name: "allow_https"
        port: 443
        protocol: "tcp"
        action: "allow"
        direction: "in"
      - name: "allow_alt_http"
        port: 8080
        protocol: "tcp"
        action: "allow"
        direction: "in"
      - name: "allow_ssh_mgmt"
        port: 22
        protocol: "tcp"
        source: "10.10.0.0/24"
        action: "allow"
        direction: "in"
      - name: "allow_ssh_dmz"
        port: 22
        protocol: "tcp"
        source: "10.10.1.0/24"
        action: "allow"
        direction: "in"
      - name: "deny_all_inbound"
        action: "deny"
        direction: "in"

    # --- mailserver ---
    mailserver:
      - name: "allow_smtp"
        port: 25
        protocol: "tcp"
        action: "allow"
        direction: "in"
      - name: "allow_submission"
        port: 587
        protocol: "tcp"
        action: "allow"
        direction: "in"
      - name: "allow_smtps"
        port: 465
        protocol: "tcp"
        action: "allow"
        direction: "in"
      - name: "allow_imaps"
        port: 993
        protocol: "tcp"
        action: "allow"
        direction: "in"
      - name: "allow_pop3s"
        port: 995
        protocol: "tcp"
        action: "allow"
        direction: "in"
      - name: "allow_imap"
        port: 143
        protocol: "tcp"
        action: "allow"
        direction: "in"
      - name: "allow_pop3"
        port: 110
        protocol: "tcp"
        action: "allow"
        direction: "in"
      - name: "allow_ssh_mgmt"
        port: 22
        protocol: "tcp"
        source: "10.10.0.0/24"
        action: "allow"
        direction: "in"
      - name: "deny_all_inbound"
        action: "deny"
        direction: "in"

    # --- fileserver ---
    fileserver:
      - name: "allow_smb"
        port: 445
        protocol: "tcp"
        source: "10.10.2.0/24"
        action: "allow"
        direction: "in"
      - name: "allow_netbios"
        port: 139
        protocol: "tcp"
        source: "10.10.2.0/24"
        action: "allow"
        direction: "in"
      - name: "allow_ssh_mgmt"
        port: 22
        protocol: "tcp"
        source: "10.10.0.0/24"
        action: "allow"
        direction: "in"
      - name: "allow_ssh_dmz"
        port: 22
        protocol: "tcp"
        source: "10.10.1.0/24"
        action: "allow"
        direction: "in"
      - name: "deny_all_inbound"
        action: "deny"
        direction: "in"

    # --- database ---
    database:
      - name: "allow_mysql"
        port: 3306
        protocol: "tcp"
        source: "10.10.1.0/24"
        action: "allow"
        direction: "in"
      - name: "allow_postgresql"
        port: 5432
        protocol: "tcp"
        source: "10.10.1.0/24"
        action: "allow"
        direction: "in"
      - name: "allow_ssh_mgmt"
        port: 22
        protocol: "tcp"
        source: "10.10.0.0/24"
        action: "allow"
        direction: "in"
      - name: "deny_all_inbound"
        action: "deny"
        direction: "in"

    # --- domaincontroller ---
    domaincontroller:
      - name: "allow_ldap"
        port: 389
        protocol: "tcp"
        source: "10.10.2.0/24"
        action: "allow"
        direction: "in"
      - name: "allow_ldaps"
        port: 636
        protocol: "tcp"
        source: "10.10.2.0/24"
        action: "allow"
        direction: "in"
      - name: "allow_kerberos"
        port: 88
        protocol: "tcp"
        source: "10.10.2.0/24"
        action: "allow"
        direction: "in"
      - name: "allow_kerberos_udp"
        port: 88
        protocol: "udp"
        source: "10.10.2.0/24"
        action: "allow"
        direction: "in"
      - name: "allow_dns"
        port: 53
        protocol: "tcp"
        source: "10.10.2.0/24"
        action: "allow"
        direction: "in"
      - name: "allow_dns_udp"
        port: 53
        protocol: "udp"
        source: "10.10.2.0/24"
        action: "allow"
        direction: "in"
      - name: "allow_smb"
        port: 445
        protocol: "tcp"
        source: "10.10.2.0/24"
        action: "allow"
        direction: "in"
      - name: "allow_ssh_mgmt"
        port: 22
        protocol: "tcp"
        source: "10.10.0.0/24"
        action: "allow"
        direction: "in"
      - name: "deny_all_inbound"
        action: "deny"
        direction: "in"

    # --- workstation ---
    workstation:
      - name: "allow_rdp"
        port: 3389
        protocol: "tcp"
        source: "10.10.0.0/24"
        action: "allow"
        direction: "in"
      - name: "allow_smb"
        port: 445
        protocol: "tcp"
        source: "10.10.2.0/24"
        action: "allow"
        direction: "in"
      - name: "deny_all_inbound"
        action: "deny"
        direction: "in"

    # --- instructor ---
    instructor:
      - name: "allow_ssh_in"
        port: 22
        protocol: "tcp"
        action: "allow"
        direction: "in"
      - name: "allow_all_out"
        action: "allow"
        direction: "out"

    # --- attacker ---
    attacker:
      - name: "allow_ssh_in"
        port: 22
        protocol: "tcp"
        source: "10.10.0.0/24"
        action: "allow"
        direction: "in"
      - name: "allow_all_out"
        action: "allow"
        direction: "out"

# =============================================================================
# VPN GATEWAY CONFIGURATION
# =============================================================================
vpn:
  type: "wireguard"
  interface: "wg0"

  peers:
    - name: "attacker"
      public_key: "{{ attacker_public_key }}"
      allowed_ips:
        - "172.16.0.10/32"
      endpoint: ""

    - name: "instructor"
      public_key: "{{ instructor_public_key }}"
      allowed_ips:
        - "10.10.0.10/32"
      endpoint: ""

  listen_port: 51820

  # Configuracion de enrutamiento del gateway
  routes:
    - destination: "10.10.1.0/24"
      gateway: "10.10.1.1"
      description: "Ruta hacia zona DMZ"
    - destination: "10.10.2.0/24"
      gateway: "10.10.2.1"
      description: "Ruta hacia zona interna"
    - destination: "10.10.0.0/24"
      gateway: "10.10.0.1"
      description: "Ruta hacia zona de gestion"
    - destination: "172.16.0.0/24"
      gateway: "172.16.0.1"
      description: "Ruta hacia zona Internet"

# =============================================================================
# USUARIOS Y CREDENCIALES
# =============================================================================
users:

  # Usuarios del dominio (Samba AD DC)
  domain_users:
    - username: "administrador"
      password: "Admin@BancoDelSol2024!"
      full_name: "Administrador del Dominio"
      groups:
        - "Domain Admins"
        - "Enterprise Admins"
      description: "Cuenta administrativa principal del dominio"

    - username: "empleado"
      password: "BancoDelSol2024!"
      full_name: "Juan Perez - Gerente de Ventas"
      groups:
        - "Domain Users"
        - "Ventas"
      description: "Empleado del departamento de ventas - Victima principal"

    - username: "soporte"
      password: "Soporte@Banco2024!"
      full_name: "Maria Garcia - Soporte TI"
      groups:
        - "Domain Users"
        - "TI"
      description: "Personal de soporte tecnico"

    - username: "rrhh"
      password: "RRHH@Banco2024!"
      full_name: "Pedro Lopez - RRHH"
      groups:
        - "Domain Users"
        - "RRHH"
      description: "Personal de recursos humanos"

    - username: "directivo"
      password: "Directivo@Banco2024!"
      full_name: "Ana Rodriguez - Directora General"
      groups:
        - "Domain Users"
        - "Directivos"
      description: "Directiva de la entidad"

  # Usuarios locales Linux
  local_users:
    webserver:
      - username: "webadmin"
        password: "webadmin123"
        groups:
          - "sudo"
      - username: "deploy"
        password: "deploy123"
        groups:
          - "www-data"

    mailserver:
      - username: "mailadmin"
        password: "mailadmin123"
        groups:
          - "sudo"
      - username: "postfix"
        shell: "/usr/sbin/nologin"

    fileserver:
      - username: "fileadmin"
        password: "fileadmin123"
        groups:
          - "sudo"

    database:
      - username: "dbadmin"
        password: "dbadmin123"
        groups:
          - "sudo"
      - username: "mysql_user"
        password: "MySQL@Banco2024!"
      - username: "pg_user"
        password: "Postgres@Banco2024!"

    domaincontroller:
      - username: "dcadmin"
        password: "dcadmin123"
        groups:
          - "sudo"

  # Usuarios IMAP/POP3 del mailserver
  mail_users:
    - username: "juan.perez"
      password: "Mail2024!"
      full_name: "Juan Perez"
      mailbox: "juan.perez@bancodelsol.local"

    - username: "maria.garcia"
      password: "Mail2024!"
      full_name: "Maria Garcia"
      mailbox: "maria.garcia@bancodelsol.local"

    - username: "pedro.lopez"
      password: "Mail2024!"
      full_name: "Pedro Lopez"
      mailbox: "pedro.lopez@bancodelsol.local"

# =============================================================================
# SERVICIOS Y CONFIGURACION ADICIONAL
# =============================================================================
services:

  # DNS interno (resuelto por el domain controller)
  dns:
    primary: "10.10.2.5"
    secondary: "8.8.8.8"
    zones:
      - name: "bancodelsol.local"
        type: "forward"
        server: "10.10.2.5"

  # NTP
  ntp:
    server: "10.10.2.5"
    clients:
      - "10.10.1.0/24"
      - "10.10.2.0/24"

  # Monitoreo
  monitoring:
    tool: "prometheus"
    enabled: false
    ports:
      prometheus: 9090
      grafana: 3000

# =============================================================================
# VARIABLES DE ENTORNO Y METADATOS
# =============================================================================
metadata:
  course: "Ciberseguridad - Tectonic Cyber Range"
  institution: "BHU - Universidad de la Republica"
  country: "Uruguay"
  language: "es"
  tags:
    - "banco"
    - "financial"
    - "ciberseguridad"
    - "pentesting"
    - "forense"
    - "defensa"
    - "Active Directory"
    - "Samba"
    - "Linux"
    - "Windows"

variables:
  domain_name: "bancodelsol.local"
  domain_suffix: ".bancodelsol.local"
  timezone: "America/Montevideo"
  country_code: "UY"
  currency: "UYU"
  bank_name: "Banco del Sol S.A."
```

---

## 4. Servicios y Puertos por Maquina Virtual

### 4.1 webserver (10.10.1.10)

| Servicio            | Puerto  | Protocolo | Descripcion                                    |
|---------------------|---------|-----------|------------------------------------------------|
| Apache HTTP         | 80      | TCP       | Servidor HTTP principal                        |
| Apache HTTPS        | 443     | TCP       | Servidor HTTPS con certificados autofirmados    |
| Nginx Reverse Proxy | 8080    | TCP       | Proxy inverso para aplicacion interna          |
| SSH                 | 22      | TCP       | Acceso administrativo remoto                   |
| Fail2Ban            | -       | -         | Proteccion contra fuerza bruta                 |

**Aplicacion web:** Pagina principal del Banco del Sol con login, seccion de clientes y area de empleados. Vulnerabilidades intencionalmente incluidas: SQL injection, XSS, directorios expuestos, headers de seguridad debiles.

### 4.2 mailserver (10.10.1.20)

| Servicio        | Puerto | Protocolo | Descripcion                              |
|-----------------|--------|-----------|------------------------------------------|
| SMTP            | 25     | TCP       | Transferencia de correo entrante         |
| SMTP Submission | 587    | TCP       | Envio de correo autenticado              |
| SMTPS           | 465    | TCP       | Envio de correo con TLS                  |
| IMAP            | 143    | TCP       | Acceso a correo (sin cifrar)             |
| IMAPS           | 993    | TCP       | Acceso a correo con TLS                  |
| POP3            | 110    | TCP       | Descarga de correo (sin cifrar)          |
| POP3S           | 995    | TCP       | Descarga de correo con TLS               |
| SSH             | 22     | TCP       | Acceso administrativo remoto             |
| DKIM            | -      | -         | Firma digital de correos                 |
| SpamAssassin    | -      | -         | Filtrado de spam                         |
| ClamAV          | -      | -         | Antivirus de correo                      |

**Configuracion de dominio:** `bancodelsol.local` - correos de empleados con autenticacion via LDAP contra el domain controller.

### 4.3 fileserver (10.10.2.10)

| Servicio     | Puerto | Protocolo | Descripcion                              |
|--------------|--------|-----------|------------------------------------------|
| SMB/CIFS     | 445    | TCP       | Comparticion de archivos                 |
| NetBIOS      | 139    | TCP       | Nombres NetBIOS sobre TCP/IP             |
| SSH          | 22     | TCP       | Acceso administrativo remoto             |

**Recursos compartidos:**
- `\\fileserver\ventas` - Archivos del departamento de ventas
- `\\fileserver\rrhh` - Archivos del departamento de recursos humanos
- `\\fileserver\directivos` - Archivos de la direccion (restringido)
- `\\fileserver\publico` - Archivos publicos del banco

### 4.4 database (10.10.2.20)

| Servicio     | Puerto | Protocolo | Descripcion                              |
|--------------|--------|-----------|------------------------------------------|
| MySQL        | 3306   | TCP       | Base de datos relacional principal       |
| PostgreSQL   | 5432   | TCP       | Base de datos secundaria                  |
| SSH          | 22     | TCP       | Acceso administrativo remoto             |

**Bases de datos:**
- MySQL: `banco_clientes` (clientes, cuentas, transacciones)
- PostgreSQL: `banco_operaciones` (logs de operaciones, auditoria)

### 4.5 domaincontroller (10.10.2.5)

| Servicio     | Puerto | Protocolo | Descripcion                              |
|--------------|--------|-----------|------------------------------------------|
| LDAP         | 389    | TCP       | Directorio abierto                       |
| LDAPS        | 636    | TCP       | Directorio cifrado                       |
| Kerberos     | 88     | TCP/UDP   | Autenticacion Kerberos                   |
| DNS          | 53     | TCP/UDP   | Resolucion de nombres                    |
| SMB          | 445    | TCP       | Servicios de dominio                     |
| SSH          | 22     | TCP       | Acceso administrativo remoto             |

**Dominio:** `bancodelsol.local` - Samba Active Directory Domain Controller con usuarios, grupos y politicas de grupo (GPO).

### 4.6 workstation (10.10.2.100)

| Servicio     | Puerto | Protocolo | Descripcion                              |
|--------------|--------|-----------|------------------------------------------|
| RDP          | 3389   | TCP       | Escritorio remoto                        |
| SMB          | 445    | TCP       | Acceso a recursos compartidos            |

**Software instalado:** Google Chrome, Microsoft Office 2021, Adobe Reader, 7-Zip, PuTTY, WinSCP, Sysinternals Suite. **Perfil del usuario:** Empleado del departamento de ventas, con acceso a recursos compartidos de ventas y correo electronico.

---

## 5. Tabla Resumen de Redes

| Zona          | Subred          | Gateway        | VLAN | Proposito                        |
|---------------|-----------------|----------------|------|----------------------------------|
| Management    | 10.10.0.0/24    | 10.10.0.1      | 100  | Acceso del instructor            |
| DMZ           | 10.10.1.0/24    | 10.10.1.1      | 200  | Servidores expuestos             |
| Internal      | 10.10.2.0/24    | 10.10.2.1      | 300  | Servidores criticos y victimas   |
| Internet Sim. | 172.16.0.0/24   | 172.16.0.1     | 400  | Red externa no confiable         |

---

## 6. Flujo de Trafico

```
[Attacker] --> [VPN Gateway] --> [DMZ: Web/Mail] --> [Internal: DB/FileServer/DC]
                                                      |
                                              [Workstation - Victima]

[Instructor] --> [VPN Gateway] --> [Todas las VMs] (monitoreo/administracion)
```

---

## 7. Notas para el Instructor

### 7.1 Acceso al Laboratorio
- El instructor accede via SSH a la VM `instructor` (10.10.0.10) o directamente via consola virtual.
- Desde la VM instructor puede monitorear todo el trafico con `tcpdump` o `wireshark`.
- El acceso SSH a todas las VMs esta configurado con llaves publicas.

### 7.2 Seguimiento de Ataques
- Los logs de autenticacion de todas las VMs se centralizan en `/var/log/auth.log` (Linux) y en el domain controller.
- El mailserver registra todos los intentos de login IMAP/POP3.
- El fileserver registra accesos SMB en `/var/log/samba/log.smbd`.
- La workstation guarda logs de RDP en el Visor de Eventos de Windows.

### 7.3 Restablecimiento del Entorno
- Cada VM tiene un script de provision que puede re-ejecutarse para restaurar el estado inicial.
- Los datos de las bases de datos se pueden restaurar desde los dumps en `/opt/backups/`.
- Los usuarios del dominio se re-crean ejecutando `ansible-playbook reset_domain.yml`.

### 7.4 Redes y Routing
- Las reglas de enrutamiento se aplican via `iptables` en el host o en el gateway VPN.
- Para agregar nuevas reglas, modificar la seccion `routing` del YAML y ejecutar `tectonic apply`.
- Las reglas de firewall en cada VM se aplican via `ufw` (Linux) o `Windows Firewall` (Windows).

### 7.5 Modificaciones Comunes
- Para agregar una nueva VM: copiar un bloque existente en la seccion `vms` y ajustar la IP.
- Para abrir un nuevo puerto: agregar una regla en la seccion `firewall_rules` de la VM correspondiente.
- Para agregar un usuario del dominio: agregar entrada en `users.domain_users` y ejecutar provisioning.
