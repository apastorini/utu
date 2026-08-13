# Curso de Ciberseguridad BHU - Instalación y Configuración de Tectonic

## 1. ¿Qué es Tectonic?

Tectonic es un **cyber range** (campo de entrenamiento cibernético) académico desarrollado por el Grupo de Seguridad Informática (GSI) de la Universidad de la República, Uruguay. Permite crear entornos virtuales con múltiples máquinas, redes y servicios para entrenamiento en ciberseguridad.

### Características principales

- **Infrastructure as Code (IaC)**: Toda la infraestructura se define en archivos declarativos (YAML + Ansible).
- **Escenarios reutilizables**: Las configuraciones son versionables y compartibles.
- **Múltiples plataformas**: Soporta Docker (desarrollo/pruebas), Libvirt/KVM (on-premise) y AWS (nube).
- **Monitoreo integrado**: Incluye Elastic SIEM, Caldera (automatización de ataques), Guacamole (acceso web).
- **Automático**: Packer crea imágenes, Terraform despliega infraestructura, Ansible configura.

### Arquitectura por capas

```
Capa 1: Infraestructura física/virtual (Docker, Libvirt, AWS)
Capa 2: IaC (Packer, Terraform, Ansible)
Capa 3: Orquestación Python (CLI de Tectonic)
Capa 4: Servicios (Elastic, Caldera, Guacamole, Moodle, CTFd)
Capa 5: Escenarios (descripciones YAML + playbooks)
```

### Flujo de trabajo típico

1. Escribir `description.yml` con la topología, máquinas, redes y servicios.
2. Escribir `base_config.yml` (Ansible) para configurar la imagen base.
3. Escribir `after_clone.yml` (Ansible) para configurar cada instancia.
4. Ejecutar `tectonic create-images` para generar las imágenes base.
5. Ejecutar `tectonic deploy` para desplegar las instancias.
6. Los alumnos acceden vía SSH/Guacamole a las máquinas `entry_point`.
7. Al finalizar, ejecutar `tectonic destroy` para limpiar.

## 2. Requisitos del Sistema

### Sistemas operativos recomendados

| Sistema | Soporte | Notas |
|---------|---------|-------|
| Linux (Ubuntu 22.04/24.04) | Completo | Plataforma recomendada |
| macOS (Intel/Apple Silicon) | Completo | Vía Docker Desktop |
| Windows con WSL2 | Parcial | Solo Docker, sin Elastic/Caldera |

### En Windows con WSL2

Tectonic funciona en Windows a través de WSL2 (Windows Subsystem for Linux). Siga estos pasos:

1. Instalar WSL2 con Ubuntu:
```powershell
# En PowerShell como Administrador
wsl --install -d Ubuntu-24.04
wsl --set-default-version 2
```

2. Iniciar la terminal WSL2 y continuar con las instrucciones para Linux.

### Requisitos mínimos (Docker)

- CPU: 4 núcleos
- RAM: 8 GB (16 GB recomendados para escenarios con Elastic)
- Disco: 50 GB libres
- Docker Engine 24+ o Docker Desktop
- Python 3.12+
- Terraform 1.5+
- Packer 1.9+

## 3. Instalación Paso a Paso

### Paso 1: Instalar dependencias del sistema (Ubuntu/Debian)

```bash
# Actualizar repositorios
sudo apt update && sudo apt upgrade -y

# Instalar dependencias básicas
sudo apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    git \
    curl \
    wget \
    unzip \
    build-essential \
    libssl-dev \
    libffi-dev \
    sshpass
```

### Paso 2: Instalar Docker

```bash
# Instalar Docker Engine
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Agregar su usuario al grupo docker
sudo usermod -aG docker $USER

# Cerrar sesión y volver a entrar, o ejecutar:
newgrp docker

# Verificar instalación
docker --version
docker run hello-world
```

### Paso 3: Instalar Terraform

```bash
# Descargar Terraform
wget https://releases.hashicorp.com/terraform/1.9.8/terraform_1.9.8_linux_amd64.zip
unzip terraform_1.9.8_linux_amd64.zip
sudo mv terraform /usr/local/bin/
rm terraform_1.9.8_linux_amd64.zip

# Verificar
terraform --version
```

### Paso 4: Instalar Packer

```bash
# Descargar Packer
wget https://releases.hashicorp.com/packer/1.11.2/packer_1.11.2_linux_amd64.zip
unzip packer_1.11.2_linux_amd64.zip
sudo mv packer /usr/local/bin/
rm packer_1.11.2_linux_amd64.zip

# Verificar
packer --version
```

### Paso 5: Crear entorno virtual Python e instalar Tectonic

```bash
# Clonar el repositorio de Tectonic
git clone https://github.com/GSI-Fing-Udelar/tectonic.git
cd tectonic

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Actualizar pip
pip install --upgrade pip

# Instalar Tectonic
pip install tectonic-cyberrange

# Opcional: instalar desde el código fuente (si necesita modificar)
pip install -e .
```

### Paso 6: Configurar claves SSH

```bash
# Generar par de claves SSH (si no existe)
ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -N ""

# Verificar que se crearon
ls -la ~/.ssh/
# id_rsa      (clave privada)
# id_rsa.pub  (clave pública)
```

### Paso 7: Verificar Ansible

```bash
# Ansible se instala como dependencia de Tectonic
ansible --version

# Debe mostrar algo como:
# ansible [core 2.17.x]
# config file = None
```

## 4. Configuración de tectonic.ini

El archivo `tectonic.ini` controla el comportamiento de Tectonic. A continuación se muestra una configuración para plataforma Docker:

```ini
[config]
platform = docker
lab_repo_uri = ./curso_bhu
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

### Explicación de parámetros clave

| Parámetro | Descripción |
|-----------|-------------|
| `platform` | Plataforma de despliegue: `docker`, `libvirt`, o `aws` |
| `lab_repo_uri` | Ruta al directorio que contiene los escenarios |
| `network_cidr_block` | Rango de red principal para los laboratorios |
| `ssh_public_key_file` | Ruta a la clave pública SSH para acceso |
| `configure_dns` | Si se configura DNS interno (`yes`/`no`) |
| `debug` | Modo debug con logs detallados |

## 5. Comandos Básicos de Tectonic

### Listar escenarios disponibles

```bash
tectonic -c tectonic.ini list
```

### Crear imágenes base

```bash
tectonic -c tectonic.ini ruta/al/lab_edition.yml create-images
```

Este comando usa Packer para crear imágenes Docker con el `base_config.yml`.

### Desplegar un escenario

```bash
tectonic -c tectonic.ini ruta/al/lab_edition.yml deploy
```

Crea las instancias, ejecuta `after_clone.yml` y habilita acceso.

### Crear imágenes y desplegar en un solo paso

```bash
tectonic -c tectonic.ini ruta/al/lab_edition.yml deploy --images
```

### Listar instancias desplegadas

```bash
tectonic -c tectonic.ini ruta/al/lab_edition.yml list
```

### Destruir un escenario

```bash
tectonic -c tectonic.ini ruta/al/lab_edition.yml destroy
```

### Obtener información de una instancia

```bash
tectonic -c tectonic.ini ruta/al/lab_edition.yml info
```

### Ver ayuda general

```bash
tectonic --help
tectonic <comando> --help
```

## 6. Acceso a las Máquinas

### SSH directo

Cada máquina marcada con `entry_point: yes` en `description.yml` es accesible por SSH:

```bash
# El comando info muestra las IPs y credenciales
tectonic -c tectonic.ini lab.yml info

# Acceder por SSH
ssh estudiante@<ip-de-la-maquina>
```

Las credenciales por defecto son proporcionadas por Tectonic y varían según la configuración.

### Acceso vía Guacamole (Web)

Si Guacamole está habilitado:

1. Abrir navegador en `http://<host-tectonic>:8080/guacamole`
2. Iniciar sesión con credenciales de estudiante
3. Seleccionar la máquina a la que desea conectarse

### Acceso vía Kibana (Elastic SIEM)

Si Elastic está habilitado:

- URL: `http://<host-tectonic>:5601`
- Credenciales: proporcionadas por `tectonic info`

## 7. Verificación de Instalación

### Verificar que todo funciona correctamente

```bash
# 1. Verificar versiones
python3 --version    # Debe ser >= 3.12
docker --version     # Debe ser >= 24
terraform --version  # Debe ser >= 1.5
packer --version     # Debe ser >= 1.9
ansible --version    # Debe mostrar core 2.17+

# 2. Verificar que Tectonic está instalado
tectonic --help

# 3. Verificar que Docker está funcionando
docker ps

# 4. Probar un escenario simple
cd tectonic
tectonic -c tectonic.ini examples/password_cracking.yml list
```

### Solución de problemas comunes

| Problema | Solución |
|----------|----------|
| `docker: command not found` | Instalar Docker Engine y agregar usuario al grupo docker |
| `terraform: command not found` | Verificar que Terraform está en `/usr/local/bin` |
| `Permission denied` al conectar SSH | Verificar permisos de `~/.ssh/id_rsa` (`chmod 600`) |
| Error de Python `ModuleNotFoundError` | Activar entorno virtual (`source venv/bin/activate`) |
| Packer falla al construir imagen | Verificar que Docker está corriendo (`systemctl start docker`) |
| Elastic no inicia | Asignar más RAM (mínimo 8 GB para Elastic) |

## 8. Estructura de un Escenario Tectonic

```
escenarios/mi_escenario/
├── description.yml          # Descripción YAML del escenario (obligatorio)
├── ansible/
│   ├── base_config.yml      # Playbook para imagen base (obligatorio)
│   ├── after_clone.yml      # Playbook post-clonación (obligatorio)
│   ├── requirements.yml     # Dependencias de colecciones Ansible
│   ├── variables/           # Archivos de variables
│   │   └── vars.yml
│   └── files/               # Archivos estáticos para copiar
├── elastic/                 # Recursos de Elastic (opcional)
│   ├── endpoint/            # Políticas endpoint
│   └── ... 
├── caldera/                 # Recursos de Caldera (opcional)
└── ctfd/                    # Desafíos CTFd (opcional)
```

## 9. Referencias

- [Repositorio Tectonic](https://github.com/GSI-Fing-Udelar/tectonic)
- [Documentación oficial](https://github.com/GSI-Fing-Udelar/tectonic/tree/main/docs)
- [Grupo de Seguridad Informática - Udelar](https://www.fing.edu.uy/inco/grupos/gsi)
- [Página del proyecto](https://www.fing.edu.uy/inco/proyectos/tectonic)
