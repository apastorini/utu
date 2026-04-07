# Primeros pasos de Virtualizacion y Hacking Etico

---

## 1. Fundamentos de Virtualizacion

### 1.1. ¿Qué es un Hipervisor?

Un hipervisor es un software que permite crear y ejecutar máquinas virtuales. Actua como capa intermedia entre el hardware físico y los sistemas operativos virtuales.

**Tipos de Hipervisores:**

| Tipo | Nombre | Ejemplos | Caracteristicas |
|------|--------|----------|----------------|
| **Tipo 1 (Bare Metal)** | Nativo | VMware ESXi, Microsoft Hyper-V, Xen | Se instala directamente sobre el hardware. Mayor rendimiento. Usado en servidores de producción. |
| **Tipo 2 (Hosted)** | Hospedado | VirtualBox, VMware Workstation, Parallels | Se instala sobre un sistema operativo existente. Ideal para desarrollo y pruebas. |

VirtualBox es un hipervisor de Tipo 2. Esto significa que necesitamos un sistema operativo base (host) y sobre el se ejecutan las máquinas virtuales (guests).

### 1.2. Diferencias entre Maquinas Virtuales y Contenedores

| Caracteristica | Maquina Virtual | Contenedor |
|---------------|-----------------|------------|
| **Aislamiento** | Completo. Cada VM tiene su propio kernel | Comparte el kernel del host |
| **Arranque** | Minutos | Segundos |
| **Tamaño** | Gigabytes (2-50 GB tipico) | Megabytes |
| **Rendimiento** | Overhead del 5-10% | Overhead mínimo, casi nativo |
| **Sistema operativo** | Cualquier SO | Solo el mismo kernel que el host |
| **Seguridad** | Aislamiento fuerte, permite analisis de malware | Aislamiento mas debil |
| **Casos de uso** | Pentesting, análisis de malware, laboratorio multi-SO | Despliegue de aplicaciones, microservicios |

```
+------------------------------------------+
|              MAQUINA VIRTUAL             |
|  +------------------------------------+  |
|  |  SISTEMA OPERATIVO GUEST           |  |
|  |  +------------------------------+  |  |
|  |  |  APLICACIONES               |  |  |
|  |  +------------------------------+  |  |
|  |  |  LIBRERIAS Y DEPENDENCIAS   |  |  |
|  |  +------------------------------+  |  |
|  |  |  KERNEL (propio)            |  |  |
|  +------------------------------------+  |
|  +------------------------------------+  |
|  |  HIPERVISOR                        |  |
+------------------------------------------+
                  |
                  v
+------------------------------------------+
|         HARDWARE FISICO (HOST)           |
|  CPU | RAM | DISCO | RED                 |
+------------------------------------------+
```

```
+------------------------------------------+
|              CONTENEDOR                  |
|  +------------------------------------+  |
|  |  APLICACION + DEPENDENCIAS        |  |
|  +------------------------------------+  |
+------------------------------------------+
                  |
                  v
+------------------------------------------+
|        MOTOR DE CONTENEDORES             |
|     (Docker, Podman, containerd)         |
+------------------------------------------+
                  |
                  v
+------------------------------------------+
|         KERNEL DEL HOST (compartido)     |
+------------------------------------------+
                  |
                  v
+------------------------------------------+
|         HARDWARE FISICO (HOST)           |
+------------------------------------------+
```

### 1.3. Conceptos Clave de VirtualBox

- **Host (Anfitrion):** Sistema operativo principal instalado en el hardware fisico.
- **Guest (Invitado):** Sistema operativo que se ejecuta dentro de la maquina virtual.
- **Virtual Disk:** Archivo que simula un disco duro fisico para la VM.
- **Snapshot:** Estado guardado de la VM en un momento especifico.
- **NAT:** Network Address Translation, permite salida a internet.
- **Bridged Adapter:** La VM se conecta directamente a la red fisica.
- **Host-Only:** Red privada solo entre host y guests.
- **Internal Network:** Red privada solo entre VMs, sin acceso al host.

---

## 2. Tipos de Redes en VirtualBox

VirtualBox ofrece cinco modos de conectividad de red. Comprender cada uno es fundamental para configurar el laboratorio de pentesting.

### 2.1. No Conectado

**Descripcion:** La VM tiene una tarjeta de red virtual instalada pero no esta conectada a ninguna red.

**Casos de uso:**
- Analisis de malware que no debe comunicarse externamente
- Estudios forenses donde no quieres ninguna comunicacion de red
- Cuando necesita completamente la conectividad

**Configuracion:**
```
VirtualBox > Maquina > Configuracion > Red > Adaptador 1 > No conectado
```

### 2.2. NAT (Network Address Translation)

**Descripcion:** La VM sale a internet a traves de la IP del host. Es el modo por defecto en VirtualBox. Las VMs pueden acceder a internet pero no son accesibles desde el host ni de otras VMs.

**Diagrama:**
```
+----------+       +------------+       +----------+
|  VM      | --->  |  VirtualBox| --->  |  Internet|
|  (10.0.2.15)     |  NAT       |       |          |
+----------+       +------------+       +----------+
                         |
                         v
                    +----------+
                    |  Host    |
                    +----------+
```

**Características:**
- IP automatica: 10.0.2.15 (por defecto, varia segun adaptadores)
- La VM puede navegar, descargar actualizaciones
- El host NO puede acceder a servicios de la VM directamente
- Otras VMs NO pueden comunicarse con esta VM

**Casos de uso:**
- VMs que solo necesitan internet
- Cuando no necesitas acceso desde el host a la VM
- Instalación inicial de sistemas operativos

**Puertos comunes accesibles:**
- 10.0.2.2 = Gateway (normalmente la IP del router real)
- 10.0.2.3 = DNS del host
- 10.0.2.4 a 10.0.2.254 = Servicios del host (si hay port forwarding)

### 2.3. NAT Network

**Descripcion:** Similar a NAT pero permite que multiples VMs se comuniquen entre si. Creas una red NAT aislada donde todas las VMs comparten la misma gateway.

**Diagrama:**
```
+----------+
|  VM Kali |----+
+----------+    |
               v
         +------------+       +----------+
         | NAT Network| --->  |  Internet|
         |  10.0.3.0/24       |          |
         +------------+       +----------+
               ^
+----------+    |
|  VM Meta |----+
+----------+
```

**Configuracion desde terminal:**
Ir a C:\Program Files\Oracle\VirtualBox
```bash
# Crear una red NAT
VBoxManage natnetwork add --netname lab_red --network "10.0.3.0/24" --enable

# Iniciar la red NAT
VBoxManage natnetwork start --netname lab_red

# Ver redes NAT existentes
VBoxManage list natnetworks


```

**Características:**
- Todas las VMs en la misma red NAT pueden verse
- Todas tienen acceso a internet
- El mundo exterior no puede iniciar conexiones hacia las VMs
- IP automatica dentro del rango de la red NAT

**Casos de uso:**
- Laboratorio de pentesting donde las VMs deben comunicarse
- Simulaciones de red donde quieres aislamiento de la red real
- Cuando necesitas que varias VMs tengan internet y se vean entre si

### 2.4. Bridged Adapter (Adaptador Puente)

**Descripcion:** La VM se conecta directamente a la red fisica del host. Recibe una IP del mismo rango DHCP que el host (o configuracion manual).

**Diagrama:**
```
+----------+       +----------+       +------------+
|  VM      | --->  |  Switch   | --->  |  Router    |
|  (192.168.1.50)  |  Fisico   |       |  (Gateway) |
+----------+       +----------+       +------------+
                         |
+----------+             |
|  Host    |-------------+
|  (192.168.1.100)
+----------+
```

**Caracteristicas:**
- La VM recibe IP del DHCP de tu red local
- La VM es visible en tu red local como cualquier otro dispositivo
- El host y la VM se ven mutuamente
- Si tu red tiene internet, la VM tendra internet
- La VM recibe la misma configuracion de red que equipos reales

**Casos de uso:**
- Cuando necesitas que la VM sea accesible desde la red
- Pruebas en entornos que simulan producción
- Si se quiere que otros dispositivos en la red accedan a servicios de la VM

### 2.5. Host-Only Adapter (Solo Anfitrion)

**Descripcion:** Crea una red privada virtual entre el host y las VMs. Las VMs se ven entre si y con el host, pero NO tienen acceso a internet (sin configuracion adicional).

**Diagrama:**
```
+----------+
|  Host    |
|  (192.168.56.1)
+----------+
     |
     +-----> [vboxnet0] (192.168.56.0/24)
              |
     +--------+--------+
     |                 |
+----------+    +----------+
|  VM 1    |    |  VM 2    |
| (56.101) |    | (56.102) |
+----------+    +----------+
```

**Configuración desde terminal:**
```bash
# Ver adaptadores Host-Only existentes
VBoxManage list hostonlyifs

# Crear un adaptador Host-Only
VBoxManage hostonlyif create

# Configurar IP del adaptador
VBoxManage hostonlyif ipconfig vboxnet0 --ip 192.168.56.1 --netmask 255.255.255.0

# Configurar DHCP en el adaptador Host-Only
VBoxManage dhcpserver add --ifname vboxnet0 --ip 192.168.56.1 --netmask 255.255.255.0 --lowerip 192.168.56.101 --upperip 192.168.56.254 --enable
```

**Características:**
- Red privada 192.168.56.0/24 (configurable)
- VMs visibles entre si y con el host
- NO hay acceso automatico a internet
- Aislamiento total de la red externa

**Casos de uso:**
- Laboratorios de pentesting aislados
- Cuando no quieres que las VMs tengan contacto con la red externa
- Entornos de formacion seguros
- analisis de malware

### 2.6. Internal Network (Red Interna)

**Descripcion:** Similar a Host-Only pero sin incluir el host. Solo las VMs pueden comunicarse entre si.

**Diagrama:**
```
+----------+
|  VM 1    |----+
+----------+    |   Red Interna
               v   "pentest_lab"
+----------+    |
|  VM 2    |----+
+----------+
```

**Configuración:**
```bash
# Configurar en VirtualBox GUI
# O desde terminal:
VBoxManage modifyvm "nombre_vm" --nic<x> intnet --intnet<nombre>
```

**Características:**
- Las VMs se ven entre si unicamente
- El host NO ve las VMs en esta red
- Internet NO disponible
- Totalmente aislado

**Casos de uso:**
- Simulaciones de ataques entre VMs
- Cuando necesitas redes completamente aisladas
- Escaneos de vulnerabilidades sin riesgo para la red real

---

## 3. Configuración de Red Recomendada para Laboratorio de Pentesting

Para un laboratorio de pentesting funcional necesitas que todas las VMs se vean entre si y que Kali tenga internet para descargar herramientas.

### 3.1. Topologia de Red Propuesta

```
+-------------------------------------------------------+
|                    RED EXTERNA (Bridge/NAT)           |
|                 Internet para Kali Linux              |
+-------------------------------------------------------+
                          |
                          v
+-------------------------------------------------------+
|                    RED INTERNA (Host-Only)            |
|                 192.168.56.0/24                      |
|                                                       |
|  +----------+  +----------+  +----------+  +---------+|
|  | Kali     |  | Meta 2   |  | Meta 3   |  | Ubuntu ||
|  | (56.101) |  | (56.102) |  | (56.103) |  |(56.104)||
|  +----------+  +----------+  +----------+  +---------+|
|                         ^                               |
|                    Atacante                            |
+-------------------------------------------------------+
```

### 3.2. Configuracion Paso a Paso de la Red

#### Paso 1: Crear el Adaptador Host-Only

```bash
# 1. Abrir terminal de comandos

# 2. Crear adaptador Host-Only
VBoxManage hostonlyif create

# 3. Configurar la IP del adaptador (esto sera la gateway para las VMs)
VBoxManage hostonlyif ipconfig "VirtualBox Host-Only Ethernet Adapter #X" --ip 192.168.56.1 --netmask 255.255.255.0

# 4. Habilitar servidor DHCP en el adaptador (Revisar!!!)
VBoxManage dhcpserver add --ifname "VirtualBox Host-Only Ethernet Adapter #X" --ip 192.168.56.1 --netmask 255.255.255.0 --lowerip 192.168.56.101 --upperip 192.168.56.254 --enable

# 5. Verificar que el adaptador esta activo
VBoxManage list hostonlyifs
```

#### Paso 2: Configurar Cada Maquina Virtual

Para cada VM, necesitas configurar dos adaptadores de red:

| Maquina | Adaptador 1 (NAT/Bridge) | Adaptador 2 (Host-Only) |
|---------|-------------------------|------------------------|
| Kali Linux | Bridge o NAT (internet) | Host-Only 192.168.56.101 |
| Metasploitable 2 | Sin conexion o Host-Only | Host-Only 192.168.56.102 |
| Metasploitable 3 | Sin conexion | Host-Only 192.168.56.103 |
| Ubuntu | Bridge o NAT (internet) | Host-Only 192.168.56.104 |
| Windows | Bridge o NAT (internet) | Host-Only 192.168.56.105 |

#### Paso 3: Configurar desde VirtualBox GUI

```
1. Seleccionar la VM > Configuracion
2. Ir a Red > Adaptador 1
   - Habilitar adaptador de red
   - Conectado a: NAT (para Kali) o Puente (Bridge) si prefieres IP estatica en tu red
   - Tipo de adaptador: Intel PRO/1000 MT Desktop (82540EM)

3. Ir a Red > Adaptador 2
   - Habilitar adaptador de red
   - Conectado a: Solo anfitrion (Host-Only)
   - Nombre: VirtualBox Host-Only Network (el que creaste)
   - Tipo de adaptador: Intel PRO/1000 MT Desktop

4. Hacer clic en Aceptar
```

#### Paso 4: Configurar IPs Estaticas en las VMs

**En Kali Linux (Host-Only - eth1 o enp0s3, verificar con ip a):**

```bash
# Ver interfaces de red
ip a

# Editar configuracion de red
sudo nano /etc/network/interfaces

# Agregar o modificar:
auto eth1
iface eth1 inet static
address 192.168.56.101
netmask 255.255.255.0
network 192.168.56.0
broadcast 192.168.56.255

# Reiniciar red
sudo systemctl restart networking
# O en versiones recientes de Kali:
sudo nm-connection-editor
```

**Alternativa moderna usando Netplan (Kali moderno):**

```bash
# Identificar la interfaz
ip a

# Editar configuracion
sudo nano /etc/netplan/00-installer-config.yaml

# Contenido:
network:
  version: 2
  ethernets:
    eth1:
      addresses:
        - 192.168.56.101/24
      nameservers:
        addresses:
          - 8.8.8.8
          - 8.8.4.4

# Aplicar
sudo netplan apply
```

**En Metasploitable 2:**

```bash
# Ver interfaces
ifconfig -a

# Editar configuracion de red
sudo nano /etc/network/interfaces

# Agregar:
auto eth1
iface eth1 inet static
address 192.168.56.102
netmask 255.255.255.0
network 192.168.56.0
broadcast 192.168.56.255

# Reiniciar
sudo /etc/init.d/networking restart
```

**En Metasploitable 3:**

```bash
# Metasploitable 3 es mas moderno, usa systemctl

# Ver interfaces
ip a

# Ir al directorio de configuracion de red
cd /etc/systemd/network

# Crear archivo de configuracion
sudo nano 10-eth1.network

# Contenido:
[Match]
Name=eth1

[Network]
Address=192.168.56.103/24

# Habilitar servicios de red
sudo systemctl enable systemd-networkd
sudo systemctl start systemd-networkd
```

**En Ubuntu Desktop:**

```bash
# Metodo grafico (recomendado para principiantes):
# 1. Clic en icono de red en la barra superior
# 2. Wired Settings > Gear icon
# 3. IPv4: Manual
# 4. Address: 192.168.56.104
# 5. Netmask: 255.255.255.0
# 6. Gateway: 192.168.56.1
# 7. DNS: 8.8.8.8, 8.8.4.4

# Metodo por terminal:
sudo nano /etc/netplan/00-installer-config.yaml

# Contenido:
network:
  version: 2
  renderer: NetworkManager
  ethernets:
    enp0s8:
      addresses:
        - 192.168.56.104/24
      gateway4: 192.168.56.1
      nameservers:
        addresses:
          - 8.8.8.8
          - 8.8.4.4

sudo netplan apply
```

**En Windows:**

```
1. Abrir Panel de Control > Centro de redes
2. Cambiar configuracion del adaptador
3. Doble clic en "VirtualBox Host-Only Network"
4. Propiedades > Protocolo de Internet version 4 (TCP/IPv4)
5. Usar la siguiente direccion IP:
   - IP: 192.168.56.105
   - Mascara: 255.255.255.0
   - Puerta de enlace: 192.168.56.1
   - DNS preferido: 8.8.8.8
   - DNS alternativo: 8.8.4.4
6. Aceptar > Cerrar
```

---

## 4. Vagrant: Herramienta de provisionamiento Automático de Máquinas Virtuales

### 4.1. ¿Qué es Vagrant?

Vagrant es una herramienta que permite crear y configurar entornos de desarrollo reproducibles y ligeros usando archivos de configuracion declarativos. Con Vagrant puedes automatizar la creación de VMs, reduciendo significativamente el tiempo de configuración.

### 4.2. Instalacion de Vagrant

```bash
# En Windows: Descargar desde https://www.vagrantup.com/downloads

# En Kali Linux / Ubuntu:
curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install vagrant

# Verificar instalacion
vagrant --version
```

### 4.3. Comandos básicos de Vagrant

```bash
# Inicializar un nuevo proyecto
vagrant init

# Inicializar con una box especifica
vagrant init kalilinux/rolling

# Iniciar la maquina virtual
vagrant up

# Conectar via SSH
vagrant ssh

# Ver estado de las maquinas
vagrant status

# Recargar la maquina (reiniciar con nueva configuracion)
vagrant reload

# Recargar con provisionamiento
vagrant reload --provision

# Pausar la maquina
vagrant suspend

# Reanudar maquina pausada
vagrant resume

# Apagar la maquina
vagrant halt

# Destruir la maquina y sus recursos
vagrant destroy

# Recargar configuracion sin reiniciar
vagrant reload

# Ver archivos de sincronizacion
vagrant rsync
```

### 4.4. Archivo Vagrantfile

El archivo Vagrantfile define la configuracion de tu entorno:

```ruby
# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  
  # Configuracion comun para todas las VMs
  config.vm.box_check_update = false
  
  # ===== KALI LINUX =====
  config.vm.define "kali" do |kali|
    kali.vm.box = "kalilinux/rolling"
    kali.vm.hostname = "kali-lab"
    kali.vm.network "private_network", ip: "192.168.56.101"
    kali.vm.network "forwarded_port", guest: 80, host: 8080
    kali.vm.provider "virtualbox" do |vb|
      vb.memory = "4096"
      vb.cpus = 2
      vb.name = "Kali-Linux-Lab"
    end
    kali.vm.synced_folder "./data", "/vagrant_data"
  end
  
  # ===== METASPLOITABLE 2 =====
  config.vm.define "meta2" do |meta2|
    meta2.vm.box = "rapid7/metasploitable2"
    meta2.vm.hostname = "metasploitable2"
    meta2.vm.network "private_network", ip: "192.168.56.102"
    meta2.vm.provider "virtualbox" do |vb|
      vb.memory = "1024"
      vb.cpus = 1
      vb.name = "Metasploitable2-Lab"
    end
  end
  
  # ===== METASPLOITABLE 3 =====
  config.vm.define "meta3" do |meta3|
    meta3.vm.box = "rapid7/metasploitable3-ub1404"
    meta3.vm.hostname = "metasploitable3"
    meta3.vm.network "private_network", ip: "192.168.56.103"
    meta3.vm.provider "virtualbox" do |vb|
      vb.memory = "2048"
      vb.cpus = 2
      vb.name = "Metasploitable3-Lab"
    end
  end
  
  # ===== UBUNTU =====
  config.vm.define "ubuntu" do |ubuntu|
    ubuntu.vm.box = "ubuntu/jammy64"
    ubuntu.vm.hostname = "ubuntu-lab"
    ubuntu.vm.network "private_network", ip: "192.168.56.104"
    ubuntu.vm.provider "virtualbox" do |vb|
      vb.memory = "2048"
      vb.cpus = 2
      vb.name = "Ubuntu-Lab"
    end
    ubuntu.vm.provision "shell", inline: <<-SHELL
      apt-get update
      apt-get install -y open-vm-tools-desktop
    SHELL
  end
  
  # ===== WINDOWS =====
  config.vm.define "win10" do |win10|
    win10.vm.box = "gusztavvargadr/windows-10"
    win10.vm.hostname = "windows-lab"
    win10.vm.network "private_network", ip: "192.168.56.105"
    win10.vm.provider "virtualbox" do |vb|
      vb.memory = "4096"
      vb.cpus = 2
      vb.name = "Windows10-Lab"
    end
  end
  
end
```

### 4.5. Crear Laboratorio con Vagrant

```bash
# 1. Crear directorio para el laboratorio
mkdir ~/pentest-lab && cd ~/pentest-lab

# 2. Crear archivo Vagrantfile (copiar el contenido anterior)
nano Vagrantfile

# 3. Ver las VMs disponibles
vagrant status

# 4. Iniciar todas las máquinas
vagrant up

# 5. Ver estado
vagrant status

# 6. Conectar a Kali
vagrant ssh kali

# 7. Iniciar solo una máquina específica
vagrant up meta2

# 8. Ver puertos forwards
vagrant port --machine kali
```

---

## 5. Instalación de Sistemas Operativos

### 5.1. Instalación de Kali Linux

**Descripcion:** Kali Linux es la distribucion de pentesting mas popular, basada en Debian. Viene con mas de 600 herramientas preinstaladas.

**Descarga:**
```
https://www.kali.org/get-kali/#kali-virtual-machines
```

**Configuracion recomendada en VirtualBox:**

| Parametro | Valor |
|-----------|-------|
| RAM | 4096 MB (minimo 2048 MB) |
| CPU | 2 nucleos (minimo 1) |
| Disco | 50-80 GB (dinamico) |
| Red Adaptador 1 | Bridge o NAT (internet) |
| Red Adaptador 2 | Host-Only (red laboratorio) |
| S.O. Huesped | Debian 64-bit |

**Pasos de instalacion:**

```
1. VirtualBox > Nueva
2. Nombre: Kali-Linux-Lab
3. Tipo: Linux
4. Version: Debian (64-bit)
5. Memoria: 4096 MB
6. Crear disco duro virtual ahora
7. VDI (VirtualBox Disk Image)
8. Dinamicamente asignado
9. Taille: 60 GB
10. Crear
11. Seleccionar la VM > Configuracion
12. Sistema > Procesador > 2 CPUs
13. Red > Adaptador 1 > NAT (o Bridge para IP en tu red)
14. Red > Adaptador 2 > Host-Only
15. Almacenamiento > Vaciar > Elegir archivo ISO de Kali
16. Iniciar la maquina virtual
17. Seleccionar "Graphical Install"
18. Seguir asistente de instalacion de Debian
19. Al terminar, iniciar sesion:
    - Usuario: root
    - Contraseña: toor (o la que configuraste)
```

### 5.2. Instalacion de Metasploitable 2

**Descripcion:** Maquina virtual vulnerable intencionalmente diseñada para practicar pentesting. Muy antigua (basada en Ubuntu 8.04) pero excelente para aprender.

**Descarga:**
```
https://sourceforge.net/projects/metasploitable/files/Metasploitable2/
```

**Configuracion recomendada:**

| Parametro | Valor |
|-----------|-------|
| RAM | 1024 MB |
| CPU | 1 nucleo |
| Disco | 10 GB |
| Red Adaptador 1 | Host-Only |
| S.O. Huesped | Linux 2.6 (32-bit) |

**Pasos:**

```
1. VirtualBox > Nueva
2. Nombre: Metasploitable2
3. Tipo: Linux
4. Version: Ubuntu (32-bit)
5. Memoria: 1024 MB
6. Crear disco duro > VDI > Dinamico > 10 GB
7. Configuracion > Red > Host-Only
8. Almacenamiento > Asignar ISO de Metasploitable2
9. Iniciar (arranca automaticamente, no requiere instalacion)
10. Credenciales por defecto:
    - Usuario: msfadmin
    - Contraseña: msfadmin
```

**Servicios vulnerables activos por defecto:**

| Puerto | Servicio | Version |
|--------|----------|---------|
| 21 | vsftpd | 2.3.4 |
| 22 | OpenSSH | 4.7p1 |
| 23 | Telnet | - |
| 25 | Postfix | - |
| 53 | BIND | 9.4.2 |
| 80 | Apache | 2.2.8 |
| 111 | RPCbind | - |
| 139 | Samba | 3.0.20 |
| 445 | Samba | 3.0.20 |
| 1433 | PostgreSQL | 8.3 |
| 3306 | MySQL | 5.0.51a |
| 5432 | PostgreSQL | 8.3 |
| 8180 | Apache Tomcat | 5.5 |

### 5.3. Instalacion de Metasploitable 3

**Descripcion:** Version moderna de Metasploitable, basada en Ubuntu 14.04. Incluye mas servicios modernos y vulnerabilidades actualizadas.

**Descarga:**
```
https://github.com/rsmusllp/breaching-defense/blob/main/MetaSploitable3.md
https://app.vagrantup.com/rapid7/boxes/metasploitable3-ub1404
```

**Instalacion con Vagrant (recomendado):**

```bash
# Metodo 1: Vagrant (mas rapido)
mkdir metasploitable3 && cd metasploitable3
vagrant init rapid7/metasploitable3-ub1404
vagrant up

# Metodo 2: Descarga directa (buscar en GitHub rapid7/metasploitable3)
# Requiere construir desde fuente o buscar builds pre-configuradas
```

**Configuracion manual en VirtualBox:**

| Parametro | Valor |
|-----------|-------|
| RAM | 2048 MB |
| CPU | 2 nucleos |
| Disco | 60 GB |
| Red | Host-Only |
| S.O. Huesped | Linux 64-bit (Ubuntu 14.04) |

**Credenciales Metasploitable 3:**

```
Usuario: vagrant
Contraseña: vagrant

Usuario: msfadmin
Contraseña: msfadmin

Usuario: root
Contraseña: toor
```

**Servicios vulnerables:**

| Puerto | Servicio | Vulnerabilidad |
|--------|----------|----------------|
| 22 | SSH |Credenciales debiles |
| 80 | HTTP | Aplicaciones web vulnerables |
| 443 | HTTPS | SSL mal configurado |
| 445 | SMB | MS17-010 (EternalBlue) |
| 3306 | MySQL | Credenciales por defecto |
| 5432 | PostgreSQL | Credenciales por defecto |
| 8080 | Tomcat | Manager app expuesta |
| 9200 | Elasticsearch |API expuesta sin auth |
| 27017 | MongoDB | Sin autenticacion |

### 5.4. Instalacion de Ubuntu

**Descarga:**
```
https://ubuntu.com/download/desktop
```

**Configuracion:**

| Parametro | Valor |
|-----------|-------|
| RAM | 2048 MB |
| CPU | 2 nucleos |
| Disco | 25 GB |
| Red Adaptador 1 | NAT (internet) |
| Red Adaptador 2 | Host-Only |

**Pasos:**

```
1. VirtualBox > Nueva > Ubuntu (64-bit)
2. RAM: 2048 MB, Disco: 25 GB
3. Asignar ISO de Ubuntu
4. Instalar con interfaz grafica
5. Configurar usuario y contraseña
6. Instalar VMware Tools o Guest Additions al terminar
```

### 5.5. Instalacion de Windows

**Descarga (evaluacion de 90 dias):**
```
https://developer.microsoft.com/en-us/windows/downloads/virtual-machines/
```

**Configuracion:**

| Parametro | Valor |
|-----------|-------|
| RAM | 4096 MB |
| CPU | 2 nucleos |
| Disco | 60 GB |
| Red Adaptador 1 | NAT |
| Red Adaptador 2 | Host-Only |

**Pasos:**

```
1. VirtualBox > Nueva > Windows 10 (64-bit)
2. RAM: 4096 MB, Disco: 60 GB
3. Asignar ISO de Windows
4. Instalar normalmente
5. Instalar Guest Additions al terminar
6. Configurar IP estatica en Host-Only adapter
```

---

## 6. Validacion de Conectividad y Configuracion de Red

Despues de instalar todas las VMs, es importante verificar que la conectividad esta correctamente configurada.

### 6.1. Verificar Conectividad desde Kali Linux

```bash
# 1. Ver todas las interfaces de red
ip a
# o
ifconfig -a

# 2. Verificar que tienes IP en la red Host-Only (192.168.56.101)
ip addr show eth1

# 3. Probar conectividad al gateway (host)
ping 192.168.56.1 -c 4

# 4. Probar conectividad entre VMs
ping 192.168.56.102 -c 4  # Metasploitable 2
ping 192.168.56.103 -c 4  # Metasploitable 3
ping 192.168.56.104 -c 4  # Ubuntu
ping 192.168.56.105 -c 4  # Windows

# 5. Verificar salida a internet (importante para Kali)
ping 8.8.8.8 -c 4

# 6. Verificar resolución DNS
ping google.com -c 4
nslookup google.com

# 7. Ver tabla de enrutamiento
ip route
# Ver output esperado:
# default via 10.0.2.2 dev eth0  (o tu gateway de internet)
# 192.168.56.0/24 dev eth1 proto kernel scope link src 192.168.56.101
```

### 6.2. Verificar Conectividad a Metasploitable

```bash
# Desde Kali, verificar que Metasploitables responden
ping 192.168.56.102 -c 4
ping 192.168.56.103 -c 4

# Verificar puertos abiertos en Metasploitable 2
nmap -sT 192.168.56.102 -p 1-1000

# Verificar puertos abiertos en Metasploitable 3
nmap -sT 192.168.56.103 -p 1-1000

# Escaneo rápido de todos los puertos
nmap -p- 192.168.56.102
nmap -p- 192.168.56.103
```

### 6.3. Configuracion de Puerto de Red en Windows (si aplica)

```powershell
# Abrir PowerShell como Administrador

# Ver adaptadores de red
Get-NetAdapter

# Ver configuracion IP
Get-NetIPAddress

# Ver tabla de enrutamiento
route print

# Probar conectividad
Test-Connection 192.168.56.1
Test-NetConnection 192.168.56.102
```

### 6.4. Verificar que Todas las VMs Estan en la Misma Red

```bash
# Script para verificar todas las VMs (ejecutar desde Kali)
#!/bin/bash

echo "=== VERIFICACION DE RED DEL LABORATORIO ==="
echo ""

hosts=("192.168.56.1:Host (Gateway)" "192.168.56.101:Kali" "192.168.56.102:Metasploitable2" "192.168.56.103:Metasploitable3" "192.168.56.104:Ubuntu" "192.168.56.105:Windows")

for entry in "${hosts[@]}"; do
    IFS=':' read -r ip desc <<< "$entry"
    echo -n "Probando $desc ($ip)... "
    if ping -c 1 -W 2 $ip > /dev/null 2>&1; then
        echo "OK"
    else
        echo "FALLO"
    fi
done

echo ""
echo "=== VERIFICACION DE SERVICIOS EN METASPLOITABLE 2 ==="
nmap -sV 192.168.56.102 -p 21,22,23,80,139,445,3306,5432 --open

echo ""
echo "=== VERIFICACION DE SERVICIOS EN METASPLOITABLE 3 ==="
nmap -sV 192.168.56.103 -p 22,80,443,445,3306,5432,8080,9200 --open
```

---

## 7. Instalación de OWASP Juice Shop

### 7.1. ¿Qué es OWASP Juice Shop?

Es una aplicacion web intencionalmente vulnerable que abarca todo el Top 10 de OWASP. Es una forma moderna y completa de practicar pentesting web.

### 7.2. Instalación en Kali Linux

```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Node.js (si no esta)
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt install -y nodejs

# Verificar versiones
node --version
npm --version

# Instalar Git
sudo apt install -y git

# Clonar repositorio de Juice Shop
cd /opt
sudo git clone https://github.com/juice-shop/juice-shop.git

# Entrar al directorio
cd juice-shop

# Instalar dependencias
npm install

# Ejecutar en modo produccion
npm start

# La aplicacion estara disponible en:
# http://localhost:3000
```

### 7.3. Instalación como Docker Container (Alternativa Recomendada)

```bash
# Instalar Docker
sudo apt install -y docker.io
sudo systemctl enable docker
sudo systemctl start docker

# Agregar usuario al grupo docker
sudo usermod -aG docker $USER
# Cerrar sesion y volver a entrar para aplicar cambios

# Descargar imagen de Juice Shop
docker pull bkimminich/juice-shop

# Ejecutar contenedor
docker run -d --name juice-shop -p 3000:3000 bkimminich/juice-shop

# Verificar que esta corriendo
docker ps

# Ver logs
docker logs juice-shop

# Acceder desde el navegador
# http://192.168.56.101:3000
```

### 7.4. Verificar Instalación

```bash
# Desde Kali
curl http://localhost:3000

# Desde otra maquina
curl http://192.168.56.101:3000

# Probar con navegador grafico
firefox http://localhost:3000
```


---

## 8. Ciclo de Hacking - Metodología de Pentesting

El proceso de pentesting sigue un ciclo estructurado que garantiza una evaluación completa y profesional.

### 8.1. Las Fases del Hacking Etico

```
+------------------------------------------------------------+
|                                                            |
|   +---------+     +---------+     +-----------+            |
|   |RECON    |---->| SCAN    |---->| ENUMERAC  |            |
|   |OCIMIENTO|     | VULNERAB|     | ACION     |            |
|   +---------+     +---------+     +-----------+            |
|        ^                                   |               |
|        |                                   v               |
|   +---------+     +---------+     +-----------+            |
|   |REPORTES|     |EXPLOTAC |---->| ACCESO    |            |
|   |         |     | ION     |     | MANTENIDO |            |
|   +---------+     +---------+     +-----------+            |
|                                                            |
+------------------------------------------------------------+
```

### 8.2. Fase 1: Reconocimiento (Recon)

**Objetivo:** Recopilar la máxima información posible sobre el objetivo.

**Tipos:**

**Reconocimiento Pasivo:**
- Busquedas en Google (Google Dorking)
- Redes sociales
- DNS lookups
- WHOIS queries
- Informacion pública

**Reconocimiento Activo:**
- Escaneo de puertos
- Ping sweeps
- Reconocimiento de servicios
- Traceroutes

**Herramientas en Kali:**

```bash
# Consultas WHOIS
whois empresa.com

# Informacion DNS
dig empresa.com
dig -x 192.168.56.102
nslookup empresa.com

# Buscar subdominios
amass enum -passive -d empresa.com

# Google Dorking
# site:empresa.com
# filetype:pdf
# intitle:"admin" "login"
# inurl:admin

# Recopilar emails
theHarvester -d empresa.com -b all
```

### 8.3. Fase 2: Escaneo (Scanning)

**Objetivo:** Identificar puertos abiertos, servicios y vulnerabilidades.

```bash
# Escaneo TCP completo
nmap -sT -p- -A 192.168.56.102

# Escaneo UDP
nmap -sU -p- 192.168.56.102

# Escaneo con deteccion de servicios
nmap -sV 192.168.56.102

# Escaneo con scripts de vulnerabilidades
nmap --script vuln 192.168.56.102

# Escaneo de vulnerabilidades especificas
nmap --script smb-vuln-ms17-010 192.168.56.103
```

### 8.4. Fase 3: Enumeración

**Objetivo:** Extraer información detallada de los servicios identificados.

```bash
# Enumerar SMB
enum4linux 192.168.56.102

# Enumerar HTTP
nikto -h http://192.168.56.102

# Enumerar FTP
hydra -l ftp -P /usr/share/wordlists/rockyou.txt ftp://192.168.56.102

# Enumerar SNMP
snmpwalk -c public -v1 192.168.56.102
```

### 8.5. Fase 4: Explotacion

**Objetivo:** Aprovechar las vulnerabilidades encontradas para obtener acceso.

```bash
# Usar Metasploit Framework
msfconsole

# Dentro de msfconsole:
search exploit_name
use exploit/path/to/exploit
show options
set RHOSTS 192.168.56.102
set RPORT 445
exploit

# Con searchsploit (buscar exploits de exploit-db)
searchsploit vsftpd 2.3.4
searchsploit samba 3.0.20
```

### 8.6. Fase 5: Acceso y Mantenimiento

**Objetivo:** Consolidar el acceso obtenido y escalar privilegios.

```bash
# Dentro de meterpreter:
shell
# Obtener shell

# Escalada de privilegios en Linux
uname -a
cat /etc/issue
find / -perm -4000 2>/dev/null

# Escalada de privilegios en Windows
systeminfo
whoami /priv
wmic qfe get Caption,Description,HotFixID,InstalledOn
```

### 8.7. Fase 6: Reportes

**Objetivo:** Documentar hallazgos de manera profesional.

---

## 9. Herramientas de Kali Linux

### 9.1. Nmap - Mapeo de Red y Escaneo de Puertos

*Descripción:** La herramienta de exploracion de red y descubrimiento de hosts mas utilizada del mundo. Permite descubrir hosts, puertos abiertos, servicios y sistemas operativos.

**Comandos Fundamentales:**

```bash
# Escaneo básico de un host
nmap 192.168.56.102

# Escaneo de rango de red completo
nmap 192.168.56.0/24

# Escaneo de puertos especificos
nmap -p 22,80,443,3306 192.168.56.102

# Escaneo de todos los puertos
nmap -p- 192.168.56.102

# Escaneo con deteccion de servicios y versiones
nmap -sV 192.168.56.102

# Escaneo con deteccion de SO
nmap -O 192.168.56.102

# Escaneo agresivo (todas las opciones)
nmap -A 192.168.56.102

# Escaneo silencioso (syn scan, menos detectable)
nmap -sS 192.168.56.102

# Escaneo UDP
nmap -sU 192.168.56.102

# Escaneo con scripts de vulnerabilidades
nmap --script vuln 192.168.56.102

# Escaneo con timing (0=paranoico, 5=locooo)
nmap -T4 192.168.56.102

# Guardar resultados en diferentes formatos
nmap -oA resultado_scan 192.168.56.102
# -oN normal.txt
# -oX xml.xml
# -oG grepeable.txt
```

**Ejemplos Prácticos con Metasploitable:**

```bash
# 1. Descubrir todos los hosts en la red
nmap -sn 192.168.56.0/24

# 2. Identificar SO y servicios de Metasploitable 2
nmap -A -T4 192.168.56.102

# 3. Buscar vulnerabilidades conocidas en puertos abiertos
nmap --script "vuln" 192.168.56.102

# 4. Escanear todos los puertos rapidamente
nmap -p- -T5 192.168.56.102

# 5. Usar scripts de enumeration de servicios
nmap --script=banner,http-enum,ftp-anon 192.168.56.102

# 6. Escaneo para EternalBlue (MS17-010)
nmap -p445 --script=smb-vuln-ms17-010 192.168.56.103
```

**Interpretación de Resultados:**

```
PORT     STATE SERVICE  VERSION
21/tcp   open  ftp      vsftpd 2.3.4
22/tcp   open  ssh      OpenSSH 4.7p1
80/tcp   open  http     Apache httpd 2.2.8
445/tcp  open  netbios-ssn Samba smbd 3.X
3306/tcp open  mysql    MySQL 5.0.51a

STATE:
- open: Puerto aceptando conexiones
- filtered: Firewall filtrando el puerto
- closed: Puerto accesible pero sin servicio

```