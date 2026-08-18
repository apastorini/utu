# Diseño de Infraestructura: Banco del Sol

## Simulación Bancaria para Entrenamiento en Ciberseguridad

---

## 1. Diagrama de Red

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                          INTERNET (simulada)                                    │
└──────────────────────────────────────────┬──────────────────────────────────────┘
                                           │
                          ┌────────────────┴────────────────┐
                          │     FIREWALL / ROUTER (fw)       │
                          │     10.0.1.1 / 10.0.2.1          │
                          │     iptables + NAT                │
                          └───┬──────────────────────────┬───┘
                              │                          │
          ┌───────────────────┘                          └───────────────────┐
          │  Zona DMZ (10.0.1.0/24)                     │  Zona Interna (10.0.2.0/24)
          │                                              │
          │  ┌──────────┐  ┌──────────┐  ┌──────────┐   │   ┌──────────┐  ┌──────────┐
          │  │ web-srv  │  │ mail-srv │  │ vpn-srv  │   │   │core-bank │  │  db-srv  │
          │  │ 10.0.1.10│  │ 10.0.1.20│  │ 10.0.1.30│   │   │ 10.0.2.10│  │ 10.0.2.20│
          │  │ Nginx    │  │ Postfix  │  │ OpenVPN  │   │   │ Core     │  │ MariaDB │
          │  │ + PHP-FPM│  │ + Dovecot│  │          │   │   │ Banking  │  │         │
          │  └──────┬───┘  └──────┬───┘  └──────┬───┘   │   └────┬─────┘  └────┬────┘
          │         │             │             │        │        │             │
          │         └──────┬──────┘             │        │        └──────┬──────┘
          │                │                    │        │               │
          │         ┌──────┴──────┐             │        │        ┌──────┴──────┐
          │         │  SW DMZ     │             │        │        │  SW INTERNA │
          │         │  (L2 bridge)│             │        │        │  (L2 bridge)│
          │         └──────┬──────┘             │        │        └──────┬──────┘
          │                │                    │        │               │
          │                │                    │        │               │
          │                │                    │        │  ┌──────────┐ │  ┌──────────┐
          │                │                    │        │  │ siem-srv │ │  │ atm-srv  │
          │                │                    │        │  │ 10.0.2.30│ │  │ 10.0.2.40│
          │                │                    │        │  │ Elastic  │ │  │ Simulador│
          │                │                    │        │  │ Stack    │ │  │ Cajero   │
          │                │                    │        │  └──────────┘ │  └──────────┘
          │                │                    │        │               │
          │                │                    │        │        ┌──────┴──────┐
          │                │                    │        │        │ backup-srv  │
          │                │                    │        │        │ 10.0.2.50   │
          │                │                    │        │        │ Restic/BKP  │
          │                │                    │        │        └─────────────┘
          │                │                    │        │
          └────────────────┼────────────────────┼────────┘
                           │                    │
                    ┌──────┴────────────────────┴──────┐
                    │     ZONA DE ESTUDIO              │
                    │     (10.0.3.0/24)                │
                    │                                  │
                    │  ┌──────────────┐  ┌─────────────────┐
                    │  │  attack-ws   │  │  blue-team-ws    │
                    │  │  10.0.3.10   │  │  10.0.3.20       │
                    │  │  Kali Linux  │  │  Ubuntu 24.04    │
                    │  │  (Red Team)  │  │  (Blue Team)     │
                    │  └──────────────┘  └─────────────────┘
                    │
                    └───────────────────────────────────┘
```

### Tabla de Asignación de IPs

| Máquina         | IP              | Red         | MAC (ejemplo)     |
|-----------------|-----------------|-------------|--------------------|
| fw              | 10.0.1.1        | dmz         | 02:42:0a:00:01:01 |
| fw              | 10.0.2.1        | interna     | 02:42:0a:00:02:01 |
| web-srv         | 10.0.1.10       | dmz         | 02:42:0a:00:01:0a |
| mail-srv        | 10.0.1.20       | dmz         | 02:42:0a:00:01:14 |
| vpn-srv         | 10.0.1.30       | dmz         | 02:42:0a:00:01:1e |
| core-bank       | 10.0.2.10       | interna     | 02:42:0a:00:02:0a |
| db-srv          | 10.0.2.20       | interna     | 02:42:0a:00:02:14 |
| siem-srv        | 10.0.2.30       | interna     | 02:42:0a:00:02:1e |
| atm-srv         | 10.0.2.40       | interna     | 02:42:0a:00:02:28 |
| backup-srv      | 10.0.2.50       | interna     | 02:42:0a:00:02:32 |
| attack-ws       | 10.0.3.10       | estudio     | 02:42:0a:00:03:0a |
| blue-team-ws    | 10.0.3.20       | estudio     | 02:42:0a:00:03:14 |

---

## 2. description.yml (Descripción Completa del Escenario)

```yaml
---
# ============================================================
# Banco del Sol - Escenario de simulación bancaria
# Diseñado para entrenamiento en ciberseguridad financiera
# Institución: bhu
# ============================================================

institution: bhu
lab_name: banco_del_sol
default_os: ubuntu24

# ============================================================
# Configuración de máquinas invitadas
# ============================================================
guest_settings:

  # ----------------------------------------------------------
  # FIREWALL / ROUTER - Puerta de entrada y segmentación
  # ----------------------------------------------------------
  fw:
    entry_point: yes
    memory: 1024
    vcpu: 1
    disk: 10
    base_os: ubuntu24
    internet_access: yes
    copies: 1
    monitor: yes
    gui: no
    red_team_agent: no
    blue_team_agent: no

  # ----------------------------------------------------------
  # DMZ - Servicios expuestos
  # ----------------------------------------------------------

  # Servidor Web: Banca en línea (Nginx + PHP-FPM)
  web-srv:
    memory: 2048
    vcpu: 2
    disk: 15
    base_os: ubuntu24
    internet_access: no
    copies: 1
    monitor: yes
    gui: no
    red_team_agent: no
    blue_team_agent: no

  # Servidor de Correo: Notificaciones y phishing
  mail-srv:
    memory: 1536
    vcpu: 1
    disk: 15
    base_os: ubuntu24
    internet_access: no
    copies: 1
    monitor: yes
    gui: no
    red_team_agent: no
    blue_team_agent: no

  # Servidor VPN: Acceso remoto seguro
  vpn-srv:
    memory: 1024
    vcpu: 1
    disk: 10
    base_os: ubuntu24
    internet_access: no
    copies: 1
    monitor: yes
    gui: no
    red_team_agent: no
    blue_team_agent: no

  # ----------------------------------------------------------
  # ZONA INTERNA - Núcleo bancario
  # ----------------------------------------------------------

  # Core Banking: Sistema transaccional principal
  core-bank:
    memory: 4096
    vcpu: 2
    disk: 20
    base_os: ubuntu24
    internet_access: no
    copies: 1
    monitor: yes
    gui: no
    red_team_agent: no
    blue_team_agent: no

  # Base de Datos: Almacén de clientes y transacciones
  db-srv:
    memory: 4096
    vcpu: 2
    disk: 40
    base_os: ubuntu24
    internet_access: no
    copies: 1
    monitor: yes
    gui: no
    red_team_agent: no
    blue_team_agent: no

  # SIEM: Centro de monitoreo de seguridad (Elastic Stack)
  siem-srv:
    memory: 8192
    vcpu: 2
    disk: 40
    base_os: ubuntu24
    internet_access: no
    copies: 1
    monitor: yes
    gui: no
    red_team_agent: no
    blue_team_agent: no

  # Simulador de Cajero Automático
  atm-srv:
    memory: 1536
    vcpu: 1
    disk: 10
    base_os: ubuntu24
    internet_access: no
    copies: 1
    monitor: yes
    gui: no
    red_team_agent: no
    blue_team_agent: no

  # Servidor de Backup: Respaldo crítico
  backup-srv:
    memory: 1024
    vcpu: 1
    disk: 30
    base_os: ubuntu24
    internet_access: no
    copies: 1
    monitor: yes
    gui: no
    red_team_agent: no
    blue_team_agent: no

  # ----------------------------------------------------------
  # ZONA DE ESTUDIO - Estaciones de trabajo
  # ----------------------------------------------------------

  # Estación de Ataque (Kali Linux)
  attack-ws:
    entry_point: yes
    memory: 4096
    vcpu: 2
    disk: 30
    base_os: kali
    internet_access: yes
    copies: 1
    monitor: no
    gui: yes
    red_team_agent: yes
    blue_team_agent: no

  # Estación de Defensa (Ubuntu Desktop)
  blue-team-ws:
    entry_point: yes
    memory: 4096
    vcpu: 2
    disk: 30
    base_os: ubuntu24
    internet_access: yes
    copies: 1
    monitor: no
    gui: yes
    red_team_agent: no
    blue_team_agent: yes

# ============================================================
# Topología de red
# ============================================================
topology:
  # Red DMZ: Servicios expuestos al exterior
  - name: dmz
    members:
      - fw
      - web-srv
      - mail-srv
      - vpn-srv

  # Red interna: Núcleo bancario protegido
  - name: interna
    members:
      - fw
      - core-bank
      - db-srv
      - siem-srv
      - atm-srv
      - backup-srv

  # Red de estudio: Estaciones de trabajo de alumnos
  - name: estudio
    members:
      - fw
      - attack-ws
      - blue-team-ws

# ============================================================
# Reglas de tráfico entre zonas
# ============================================================
traffic_rules:
  # --- Acceso desde zona de estudio hacia DMZ ---
  - description: "Estudiantes acceden al servidor web por HTTP/HTTPS"
    source: estudio
    destination: web-srv.dmz
    port_range: "80,443"
    protocol: tcp

  - description: "Estudiantes acceden al servidor de correo (IMAP)"
    source: attack-ws.estudio
    destination: mail-srv.dmz
    port_range: 143
    protocol: tcp

  - description: "Estudiantes acceden al servidor VPN (OpenVPN UDP)"
    source: attack-ws.estudio
    destination: vpn-srv.dmz
    port_range: 1194
    protocol: udp

  - description: "Acceso SSH a servidor web desde zona de estudio"
    source: blue-team-ws.estudio
    destination: web-srv.dmz
    port_range: 22
    protocol: tcp

  # --- Acceso desde zona de estudio hacia zona interna ---
  - description: "Blue team accede al SIEM (Kibana)"
    source: blue-team-ws.estudio
    destination: siem-srv.interna
    port_range: 5601
    protocol: tcp

  - description: "Acceso SSH a core-bank para análisis forense"
    source: blue-team-ws.estudio
    destination: core-bank.interna
    port_range: 22
    protocol: tcp

  - description: "Acceso SSH a db-srv para análisis forense"
    source: blue-team-ws.estudio
    destination: db-srv.interna
    port_range: 22
    protocol: tcp

  - description: "Acceso SSH a atm-srv para análisis forense"
    source: blue-team-ws.estudio
    destination: atm-srv.interna
    port_range: 22
    protocol: tcp

  - description: "Acceso SSH a backup-srv para análisis forense"
    source: blue-team-ws.estudio
    destination: backup-srv.interna
    port_range: 22
    protocol: tcp

  # --- Tráfico DMZ -> Interna (legítimo del negocio) ---
  - description: "Web server consulta base de datos"
    source: web-srv.dmz
    destination: db-srv.interna
    port_range: 3306
    protocol: tcp

  - description: "Web server consulta core banking"
    source: web-srv.dmz
    destination: core-bank.interna
    port_range: 8443
    protocol: tcp

  - description: "Mail server envía logs al SIEM"
    source: mail-srv.dmz
    destination: siem-srv.interna
    port_range: 5044
    protocol: tcp

  # --- Tráfico Interna -> Interna ---
  - description: "Core banking consulta base de datos"
    source: core-bank.interna
    destination: db-srv.interna
    port_range: 3306
    protocol: tcp

  - description: "Core banking envía transacciones al ATM"
    source: core-bank.interna
    destination: atm-srv.interna
    port_range: 9090
    protocol: tcp

  - description: "Todos los servidores internos reportan al SIEM"
    source: core-bank.interna
    destination: siem-srv.interna
    port_range: 5044
    protocol: tcp

  - description: "DB server reporta al SIEM"
    source: db-srv.interna
    destination: siem-srv.interna
    port_range: 5044
    protocol: tcp

  - description: "ATM reporta al SIEM"
    source: atm-srv.interna
    destination: siem-srv.interna
    port_range: 5044
    protocol: tcp

  - description: "Backup desde db-srv"
    source: backup-srv.interna
    destination: db-srv.interna
    port_range: 3306
    protocol: tcp

  - description: "Backup desde core-bank"
    source: backup-srv.interna
    destination: core-bank.interna
    port_range: 22
    protocol: tcp

  # --- Tráfico Interna -> DMZ ---
  - description: "Core banking envía emails de notificación"
    source: core-bank.interna
    destination: mail-srv.dmz
    port_range: 587
    protocol: tcp

  # --- ICMP para diagnóstico ---
  - description: "ICMP entre zonas para diagnóstico"
    source: estudio
    destination: dmz
    protocol: icmp

  - description: "ICMP entre zonas para diagnóstico"
    source: estudio
    destination: interna
    protocol: icmp

# ============================================================
# Servicios Tectonic
# ============================================================

# Elastic SIEM: Monitoreo de seguridad del entorno
elastic_settings:
  enable: yes
  monitor_type: endpoint
  deploy_default_policy: yes
  vcpu: 2
  memory: 8192
  disk: 30

# Guacamole: Acceso web a las máquinas
guacamole_settings:
  enable: yes
  vcpu: 2
  memory: 2048
  disk: 20

# Caldera: Simulación de ataques automatizados
caldera_settings:
  enable: no
  vcpu: 2
  memory: 2048
  disk: 20
```

---

## 3. Archivo de Edición del Laboratorio (banco_del_sol.yml)

Este archivo se coloca en la raíz del repositorio de labs, al mismo nivel que el directorio `banco_del_sol/`.

```yaml
---
# ============================================================
# Banco del Sol - Edición del Laboratorio
# Parámetros que pueden cambiar por cada edición del curso
# ============================================================

# Nombre del lab base en el repositorio. Obligatorio.
base_lab: banco_del_sol

# Institución que ofrece esta edición. Opcional.
institution: bhu

# Nombre de esta edición. Opcional.
lab_edition_name: banco_del_sol_2025

# Número de instancias a desplegar (una por grupo de alumnos).
instance_number: 1

# Directorio con claves públicas SSH de los profesores.
teacher_pubkey_dir: ./teacher_pubkeys

# Prefijo de usuario para los alumnos.
student_prefix: bhu

# Directorio con claves públicas SSH de los alumnos.
student_pubkey_dir: ./student_pubkeys

# Generar contraseñas pseudo-aleatorias para los alumnos.
create_students_passwords: true

# Semilla para generación de contraseñas y parametrización aleatoria.
random_seed: BHU-BancoDelSol-2025-S3guro

# ----------------------------------------------------------
# Configuración de servicios
# ----------------------------------------------------------

elastic_settings:
  enable: yes
  vcpu: 2
  memory: 8192
  disk: 30

guacamole_settings:
  enable: yes
  vcpu: 2
  memory: 2048
  disk: 20

caldera_settings:
  enable: no
  vcpu: 2
  memory: 2048
  disk: 20

moodle_settings:
  enable: no
```

---

## 4. Configuración de tectonic.ini (Plataforma Docker)

```ini
[config]
platform = docker
lab_repo_uri = ./Curso_Tectonic_BHU
network_cidr_block = 10.0.0.0/16
internet_network_cidr_block = 10.0.0.0/25
services_network_cidr_block = 10.0.0.128/25
ssh_public_key_file = ~/.ssh/id_rsa.pub
configure_dns = no
debug = yes

[ansible]
ssh_common_args = -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -o ControlMaster=auto -o ControlPersist=3600
keep_logs = no
forks = 5
pipelining = no
timeout = 10
collections_and_roles_path = ./tectonic/ansible

[docker]
uri = unix:///var/run/docker.sock
dns = 8.8.8.8

[elastic]
version = 9.1.0
packetbeat_policy_name = Packetbeat
endpoint_policy_name = Endpoint
user_install_packetbeat = tectonic
external_port = 5601

[caldera]
version = 5.3.0
ot_enabled = no
external_port = 8443

[guacamole]
version = 1.6.0
brute_force_protection_enabled = no

[moodle]
version = 5.1.0
site_fullname = BHU Ciberseguridad
site_shortname = BHU-Ciber
admin_email = ciso@bhu.com.uy

[ctfd]
version = 3.8.5
admin_email = ciso@bhu.com.uy
```

---

## 5. Descripción de Roles y Especificaciones

### 5.1. Firewall (fw)

| Parámetro | Valor |
|-----------|-------|
| IP | 10.0.1.1 (DMZ) / 10.0.2.1 (Interna) |
| RAM | 1024 MB |
| vCPU | 1 |
| Disco | 10 GB |
| SO | Ubuntu 24.04 |
| Entry point | Sí |

**Rol:** Segmentador de red y punto de control. Administra `iptables`/`nftables` para filtrar tráfico entre las tres zonas (DMZ, interna, estudio). Actúa como gateway para todas las máquinas. Tiene internet simulada para permitir actualizaciones y acceso externo controlado. Es entry point para que el instructor pueda administrar las reglas de firewall durante el escenario.

---

### 5.2. web-srv (Servidor Web)

| Parámetro | Valor |
|-----------|-------|
| IP | 10.0.1.10 (DMZ) |
| RAM | 2048 MB |
| vCPU | 2 |
| Disco | 15 GB |
| SO | Ubuntu 24.04 |
| Monitoreado | Sí (Elastic) |

**Rol:** Simula la banca en línea de Banco del Sol. Ejecuta Nginx + PHP-FPM sirviendo una aplicación web bancaria simplificada. Expone puertos 80/443. Contiene vulnerabilidades intencionadas (SQLi, XSS, autenticación débil) para escenarios de ataque. Los logs de acceso se envían al SIEM para análisis.

**Por qué 2 vCPU / 2 GB RAM:** La aplicación web con PHP-FPM requiere recursos moderados para manejar múltiples peticiones simultáneas y procesar el cifrado TLS.

---

### 5.3. mail-srv (Servidor de Correo)

| Parámetro | Valor |
|-----------|-------|
| IP | 10.0.1.20 (DMZ) |
| RAM | 1536 MB |
| vCPU | 1 |
| Disco | 15 GB |
| SO | Ubuntu 24.04 |
| Monitoreado | Sí (Elastic) |

**Rol:** Servidor de correo interno con Postfix + Dovecot. Simula el sistema de notificaciones por email del banco (notificaciones de transacciones, alertas de seguridad). Se usa como vector de ataque para escenarios de phishing y spear-phishing. Los correos maliciosos pueden contener payloads para escenarios de ingeniería social.

**Por qué 1536 MB / 1 vCPU:** Postfix y Dovecot son ligeros. La carga principal es I/O de disco para buzones, no CPU.

---

### 5.4. vpn-srv (Servidor VPN)

| Parámetro | Valor |
|-----------|-------|
| IP | 10.0.1.30 (DMZ) |
| RAM | 1024 MB |
| vCPU | 1 |
| Disco | 10 GB |
| SO | Ubuntu 24.04 |
| Monitoreado | Sí (Elastic) |

**Rol:** Servidor OpenVPN que simula el acceso remoto seguro que usarían empleados del banco desde sedes externas. Permite escenarios de ataque donde el VPN se ve comprometido (credenciales débiles, split tunneling mal configurado, keyloggers en clientes).

**Por qué 1 GB RAM / 1 vCPU:** OpenVPN es extremadamente ligero. Un solo proceso TLS consume recursos mínimos.

---

### 5.5. core-bank (Core Banking)

| Parámetro | Valor |
|-----------|-------|
| IP | 10.0.2.10 (Interna) |
| RAM | 4096 MB |
| vCPU | 2 |
| Disco | 20 GB |
| SO | Ubuntu 24.04 |
| Monitoreado | Sí (Elastic) |

**Rol:** El corazón del sistema. Simula el sistema transaccional bancario (APIs REST para transferencias, consulta de saldos, gestión de cuentas). Es la máquina de mayor valor en el escenario. Almacena datos financieros sensibles. Si es comprometido, el atacante puede manipular transacciones, exfiltrar datos financieros o instalar ransomware.

**Por qué 4 GB RAM / 2 vCPU:** El servicio transaccional maneja múltiples procesos concurrentes (hilos de transacciones, cifrado de datos, logs) y necesita memoria suficiente para buffers de base de datos embebida.

---

### 5.6. db-srv (Base de Datos)

| Parámetro | Valor |
|-----------|-------|
| IP | 10.0.2.20 (Interna) |
| RAM | 4096 MB |
| vCPU | 2 |
| Disco | 40 GB |
| SO | Ubuntu 24.04 |
| Monitoreado | Sí (Elastic) |

**Rol:** Servidor MariaDB que almacena toda la información del banco: clientes, cuentas, transacciones, historial. Es el objetivo principal para escenarios de exfiltración de datos. Contiene datos sensibles que, si se filtran, constituyen una violación de la Ley 18.331 de Protección de Datos Personales.

**Por qué 4 GB RAM / 2 vCPU / 40 GB disco:** MariaDB necesita memoria para buffers y cache de consultas. El disco amplio simula volúmenes de datos reales de un banco (tablas de clientes, logs de transacciones, índices).

---

### 5.7. siem-srv (SIEM / Elastic Stack)

| Parámetro | Valor |
|-----------|-------|
| IP | 10.0.2.30 (Interna) |
| RAM | 8192 MB |
| vCPU | 2 |
| Disco | 40 GB |
| SO | Ubuntu 24.04 |
| Entry point | Sí |
| Monitoreado | Sí (Elastic interno) |

**Rol:** Centro de monitoreo de seguridad. Ejecuta Elasticsearch + Kibana (desplegado por el servicio Elastic de Tectonic). Recibe logs de todos los servidores (Filebeat/Logstash), datos de red (Packetbeat) y eventos de endpoint (Endpoint Security). Los alumnos de blue team lo usan para detectar y responder a incidentes. Expone Kibana en puerto 5601.

**Por qué 8 GB RAM / 2 vCPU / 40 GB disco:** Elasticsearch es extremadamente consumidor de memoria (requiere heap mínimo de 4 GB). El disco amplo almacena índices de logs y datos de monitoreo históricos.

---

### 5.8. atm-srv (Simulador de Cajero Automático)

| Parámetro | Valor |
|-----------|-------|
| IP | 10.0.2.40 (Interna) |
| RAM | 1536 MB |
| vCPU | 1 |
| Disco | 10 GB |
| SO | Ubuntu 24.04 |
| Monitoreado | Sí (Elastic) |

**Rol:** Simula un cajero automático (ATM) que se comunica con el core banking para procesar retiros y consultas de saldos. Expone una API en puerto 9090. Vulnerabilidades comunes: autenticación débil en protocolo ATM, comunicación sin cifrado, firmware desactualizado. Es un vector de ataque frecuente en la industria financiera.

**Por qué 1536 MB / 1 vCPU:** La aplicación ATM es una API ligera con poca lógica de negocio. Los ATMs reales tienen hardware limitado.

---

### 5.9. backup-srv (Servidor de Backup)

| Parámetro | Valor |
|-----------|-------|
| IP | 10.0.2.50 (Interna) |
| RAM | 1024 MB |
| vCPU | 1 |
| Disco | 30 GB |
| SO | Ubuntu 24.04 |
| Monitoreado | Sí (Elastic) |

**Rol:** Ejecuta tareas de backup automatizadas (Restic o rsync) copiando datos críticos desde db-srv y core-bank. Los backups se almacenan localmente (simulando almacenamiento offsite). Escenarios de ataque: ransomware que cifra y elimina backups, acceso no autorizado para exfiltrar datos de respaldo, eliminación de evidencia forense.

**Por qué 30 GB disco:** Los backups ocupan más espacio que los datos originales (versiones incrementales, duplicados).

---

### 5.10. attack-ws (Estación de Ataque)

| Parámetro | Valor |
|-----------|-------|
| IP | 10.0.3.10 (Estudio) |
| RAM | 4096 MB |
| vCPU | 2 |
| Disco | 30 GB |
| SO | Kali Linux |
| Entry point | Sí |
| GUI | Sí |
| Red Team Agent | Sí |

**Rol:** Estación de trabajo del equipo rojo (alumnos atacantes). Viene preinstalada con herramientas de penetración: Metasploit, Burp Suite, Nmap, SQLmap, John the Ripper, Hydra, Wireshark, Nikto, entre otras. Caldera agent instalado para automatización de ataques. Los alumnos usan esta máquina para planificar y ejecutar ataques contra la infraestructura bancaria.

**Por qué 4 GB RAM / 2 vCPU / 30 GB / GUI:** Kali con escritorio (XFCE) necesita recursos para la GUI. Herramientas como Metasploit y Burp Suite consumen memoria significativa. El disco almacena wordlists, wordlists, exploits y resultados de escaneos.

---

### 5.11. blue-team-ws (Estación de Defensa)

| Parámetro | Valor |
|-----------|-------|
| IP | 10.0.3.20 (Estudio) |
| RAM | 4096 MB |
| vCPU | 2 |
| Disco | 30 GB |
| SO | Ubuntu 24.04 |
| Entry point | Sí |
| GUI | Sí |
| Blue Team Agent | Sí |

**Rol:** Estación de trabajo del equipo azul (alumnos defensores). Herramientas preinstaladas: Wireshark, tcpdump, fail2ban, auditd, Suricata, OSSEC. Los alumnos monitorean tráfico sospechoso, revisan logs en Kibana, investigan alertas del SIEM, realizan análisis forense y ejecutan contramedidas. Caldera agent en modo defensivo para simulación automatizada.

**Por qué 4 GB RAM / 2 vCPU / 30 GB / GUI:** Ubuntu Desktop con herramientas de análisis de seguridad. La GUI permite usar Firefox para acceder a Kibana, y herramientas gráficas como Wireshark para inspección de paquetes.

---

## 6. Estructura de Directorios del Lab

```
Curso_Tectonic_BHU/
├── banco_del_sol/
│   ├── description.yml          # Descripción completa del escenario
│   └── ansible/
│       ├── base_config.yml      # Playbook de configuración base
│       ├── after_clone.yml      # Playbook post-clonación
│       ├── requirements.yml     # Colecciones Ansible requeridas
│       ├── files/
│       │   ├── nginx.conf       # Configuración de Nginx para web-srv
│       │   ├── postfix.cf       # Configuración de Postfix
│       │   ├── dovecot.conf     # Configuración de Dovecot
│       │   ├── openvpn.conf     # Configuración de OpenVPN
│       │   ├── corebank-api.py  # API bancaria simplificada
│       │   ├── atm-api.py       # API del cajero automático
│       │   ├── backup.sh        # Script de backup automatizado
│       │   └── bank-theme/      # Tema para la app web
│       └── variables/
│           └── vars.yml         # Variables del escenario
├── banco_del_sol.yml            # Edición del laboratorio
├── teacher_pubkeys/             # Claves SSH del profesor
│   └── id_rsa.pub
├── student_pubkeys/             # Claves SSH de alumnos
│   └── id_rsa.pub
└── 01_INSTALACION_Y_CONFIGURACION.md
    02_INFRAESTRUCTURA_BANCO_DEL_SOL.md
```

---

## 7. Despliegue

### Paso 1: Crear imágenes base

```bash
cd tectonic
tectonic -c tectonic.ini ../Curso_Tectonic_BHU/banco_del_sol.yml create-images
```

### Paso 2: Desplegar el escenario

```bash
tectonic -c tectonic.ini ../Curso_Tectonic_BHU/banco_del_sol.yml deploy
```

### Paso 3 (alternativo): Crear imágenes y desplegar en un solo paso

```bash
tectonic -c tectonic.ini ../Curso_Tectonic_BHU/banco_del_sol.yml deploy --images
```

### Paso 4: Verificar despliegue

```bash
tectonic -c tectonic.ini ../Curso_Tectonic_BHU/banco_del_sol.yml list
```

### Paso 5: Destruir al finalizar

```bash
tectonic -c tectonic.ini ../Curso_Tectonic_BHU/banco_del_sol.yml destroy
```

---

## 8. Notas de Seguridad y Cumplimiento

Este escenario simula un entorno bancario real y debe respetar las siguientes normativas uruguayas:

- **BCU - Estándares Mínimos de Seguridad:** El SIEM debe estar activo y centralizando logs de todos los servidores críticos.
- **Ley 18.331 - Protección de Datos Personales:** Los datos simulados de clientes en db-srv no deben ser exportados fuera del entorno.
- **AGESIC - Marco de Ciberseguridad:** La segmentación de red (DMZ / interna / estudio) refleja las recomendaciones de zonificación.
- **NIST CSF / ISO 27001:** El escenario permite practicar las 5 funciones del NIST (Identificar, Proteger, Detectar, Responder, Recuperar).

---

## 9. Escenarios de Entrenamiento Vinculados

Con esta infraestructura se pueden ejecutar los siguientes escenarios (directorios en `Curso_Tectonic_BHU/escenarios/`):

| # | Escenario | Ataque | Defensa |
|---|-----------|--------|---------|
| 01 | Phishing | Spear-phishing vía mail-srv | Detección en SIEM, bloqueo en firewall |
| 02 | Ransomware | Cifrado en core-bank + eliminación de backups | Respuesta a incidentes, restauración |
| 03 | DDoS | Ataque de denegación a web-srv | Mitigación, rate limiting, WAF |
| 04 | Intrusión | Pivot desde web-srv hacia core-bank | Detección lateral movement, containment |
| 05 | Exfiltración | Extracción de datos desde db-srv | DLP, monitoreo de tráfico anómalo |
| 06 | Forensia | Análisis post-incidente | Investigación, cadena de custodia |
