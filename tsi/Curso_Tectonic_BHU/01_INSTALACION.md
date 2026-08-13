# Guia de Instalacion - Tectonic Cyber Range

**Curso:** Ciberseguridad y Respuesta a Incidentes para el BHU  
**Plataforma requerida:** Ubuntu 22.04 LTS (recomendado)  
**Ultima actualizacion:** Julio 2026

---

## Indice

1. [Requisitos previos](#1-requisitos-previos)
2. [Instalacion de Docker y Docker Compose](#2-instalacion-de-docker-y-docker-compose)
3. [Instalacion de Python 3.10+ y pip](#3-instalacion-de-python-310-y-pip)
4. [Clonar el repositorio de Tectonic](#4-clonar-el-repositorio-de-tectonic)
5. [Instalar dependencias de Tectonic](#5-instalar-dependencias-de-tectonic)
6. [Configurar tectonic.ini](#6-configurar-tectonicini)
7. [Verificar la instalacion](#7-verificar-la-instalacion)
8. [Primer despliegue de prueba](#8-primer-despliegue-de-prueba)
9. [Solucion de problemas comunes](#9-solucion-de-problemas-comunes)
10. [Requisitos de red y reglas de firewall](#10-requisitos-de-red-y-reglas-de-firewall)

---

## 1. Requisitos previos

### Sistema operativo

- **Ubuntu 22.04 LTS** (recomendado) o distributions basadas en Debian.
- Acceso con privilegios de `sudo`.
-Conexion a internet estable.

### Hardware minimo

| Recurso     | Minimo   | Recomendado |
|-------------|----------|-------------|
| RAM         | 16 GB    | 32 GB       |
| Disco       | 100 GB   | 200 GB SSD  |
| CPU         | 4 nucleos| 8 nucleos   |

> **Nota:** Tectonic levanta multiples contenedores Docker simultaneamente. Con menos de 16 GB de RAM es probable que los escenarios no funcionen correctamente.

### Software requerido

- Docker Engine 20.10+
- Docker Compose v2+
- Python 3.10 o superior
- pip (gestor de paquetes de Python)
- git

---

## 2. Instalacion de Docker y Docker Compose

### 2.1 Actualizar el sistema

```bash
sudo apt update && sudo apt upgrade -y
```

### 2.2 Instalar dependencias de Docker

```bash
sudo apt install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
```

### 2.3 Agregar la clave GPG oficial de Docker

```bash
sudo mkdir -m 0755 -p /etc/apt/keyrings

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
    sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
```

### 2.4 Agregar el repositorio de Docker

```bash
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

### 2.5 Instalar Docker Engine y Docker Compose

```bash
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

### 2.6 Verificar la instalacion de Docker

```bash
docker --version
docker compose version
```

Se espera una salida similar a:

```
Docker version 24.x.x, build xxxxxxx
Docker Compose version v2.x.x
```

### 2.7 Ejecutar Docker sin sudo (opcional pero recomendado)

```bash
sudo usermod -aG docker $USER
newgrp docker
```

> **Importante:** Despues de ejecutar `newgrp docker`, cerrar y abrir una nueva sesion de terminal para que los cambios surtan efecto. Si omites este paso, tendras que usar `sudo` antes de cada comando de Docker.

---

## 3. Instalacion de Python 3.10+ y pip

Ubuntu 22.04 ya incluye Python 3.10 de forma predeterminada. Verificar con:

```bash
python3 --version
```

Si no esta instalado o se necesita una version mas reciente:

```bash
sudo apt install -y python3 python3-pip python3-venv
```

Verificar que pip funciona:

```bash
pip3 --version
```

---

## 4. Clonar el repositorio de Tectonic

### 4.1 Clonar el repositorio principal

```bash
cd ~
git clone https://github.com/GSI-Fing-Udelar/tectonic.git
```

### 4.2 Verificar que el repositorio se clono correctamente

```bash
ls ~/tectonic/
```

Deberia mostrar la estructura del proyecto, incluyendo archivos como `tectonic.py`, `requirements.txt`, `tectonic.ini.example`, entre otros.

---

## 5. Instalar dependencias de Tectonic

### 5.1 Crear el entorno virtual

```bash
python3 -m venv ~/.tectonic
```

### 5.2 Activar el entorno virtual

```bash
source ~/.tectonic/bin/activate
```

El prompt de la terminal deberia cambiar para indicar que el entorno virtual esta activo, algo como:

```
(.tectonic) usuario@ubuntu:~$
```

### 5.3 Actualizar pip dentro del entorno virtual

```bash
pip install --upgrade pip
```

### 5.4 Instalar las dependencias

```bash
pip install -r ~/tectonic/requirements.txt
```

### 5.5 Crear el directorio de escenarios del curso

```bash
mkdir -p ~/Curso_Tectonic_BHU/escenarios
```

---

## 6. Configurar tectonic.ini

### 6.1 Copiar el archivo de configuracion de ejemplo

```bash
cp ~/tectonic/tectonic.ini.example ~/tectonic.ini
```

### 6.2 Editar el archivo de configuracion

```bash
nano ~/tectonic.ini
```

> **Nota:** Puedes usar el editor de texto que prefieras: `nano`, `vim`, `code`, etc.

### 6.3 Parametros基本icos a revisar

Revisar y ajustar los siguientes valores segun tu entorno:

```ini
[general]
# Directorio base donde se almacenan los escenarios
scenarios_path = ~/Curso_Tectonic_BHU/escenarios

# Puerto base para las redes de los escenarios
# Cada escenario asigna subredes a partir de este rango
network_base = 172.20.0.0/16

[docker]
# Interfaz de red del host que sera usada por Docker
# Usar la interfaz principal del sistema
host_interface = docker0

[logging]
# Nivel de verbose: DEBUG, INFO, WARNING, ERROR
level = INFO
```

> **IMPORTANTE:** El parametro `scenarios_path` debe apuntar al directorio `~/Curso_Tectonic_BHU/escenarios` para mantener consistencia con los materiales del curso.

### 6.4 Guardar y cerrar el archivo

Si usas `nano`, presionar `Ctrl+O`, luego `Enter` para guardar, y `Ctrl+X` para salir.

---

## 7. Verificar la instalacion

### 7.1 Verificar que el entorno virtual esta activo

```bash
source ~/.tectonic/bin/activate
```

### 7.2 Verificar que Docker esta funcionando

```bash
docker run hello-world
```

Si ves el mensaje "Hello from Docker!", la instalacion de Docker es correcta.

### 7.3 Verificar que Tectonic se ejecuta

```bash
python3 ~/tectonic/tectonic.py --help
```

Se espera ver la ayuda de la herramienta con los comandos disponibles.

### 7.4 Verificar la conexion de Docker como usuario actual

```bash
docker ps
```

Si obtienes un error de permisos, revisar la seccion de [Solucion de problemas](#9-solucion-de-problemas-comunes).

---

## 8. Primer despliegue de prueba

### 8.1 Activar el entorno virtual (si no esta activo)

```bash
source ~/.tectonic/bin/activate
```

### 8.2 Listar escenarios disponibles

```bash
python3 ~/tectonic/tectonic.py list
```

Esto mostrara los escenarios disponibles en el directorio configurado en `tectonic.ini`.

### 8.3 Desplegar un escenario de prueba

Elegir uno de los escenarios simples disponibles. Por ejemplo:

```bash
python3 ~/tectonic/tectonic.py deploy <nombre_del_escenario>
```

Reemplazar `<nombre_del_escenario>` con el nombre real del escenario que se lists con el comando anterior.

### 8.4 Verificar que el escenario esta corriendo

```bash
docker ps
```

Se espera ver multiples contenedores en estado "Up".

### 8.5 Probar la conectividad

Acceder a los servicios del escenario segun las instrucciones especificas de cada escenario. Generalmente se accede via navegador web a la IP del host en el puerto asignado.

### 8.6 Detener el escenario

```bash
python3 ~/tectonic/tectonic.py destroy <nombre_del_escenario>
```

> **Recomendacion:** Siempre destruir los escenarios despues de usarlos para liberar recursos del sistema.

---

## 9. Solucion de problemas comunes

### 9.1 Error de permisos con Docker

**Sintoma:** Al ejecutar un comando de Docker aparece el error:

```
Got permission denied while trying to connect to the Docker daemon socket
```

**Solucion:**

```bash
sudo usermod -aG docker $USER
newgrp docker
```

Cerrar y volver a abrir la terminal. Si el problema persiste:

```bash
sudo chmod 666 /var/run/docker.sock
```

> **Advertencia:** Cambiar los permisos del socket de Docker con `chmod 666` es una medida temporal. Lo correcto es agregar el usuario al grupo `docker`.

### 9.2 Errores de memoria insuficiente

**Sintoma:** Los contenedores se detienen inmediatamente o el sistema se vuelve muy lento.

**Solucion:**

1. Verificar la memoria disponible:

```bash
free -h
```

2. Cerrar aplicaciones innecesarias para liberar RAM.
3. Si es posible, agregar mas memoria al sistema.
4. Reducir el numero de escenarios simultaneos.

### 9.3 Docker no encuentra la imagen o timeout de descarga

**Sintoma:** El despliegue falla con errores de red o timeout.

**Solucion:**

1. Verificar la conexion a internet:

```bash
ping -c 3 8.8.8.8
```

2. Si estas detras de un proxy, configurar Docker para usarlo:

```bash
sudo mkdir -p /etc/systemd/system/docker.service.d
sudo tee /etc/systemd/system/docker.service.d/proxy.conf <<EOF
[Service]
Environment="HTTP_PROXY=http://proxy:puerto"
Environment="HTTPS_PROXY=http://proxy:puerto"
EOF

sudo systemctl daemon-reload
sudo systemctl restart docker
```

### 9.4 Error: "No such file or directory" al ejecutar Tectonic

**Sintoma:** No encuentra el archivo `tectonic.py` o `tectonic.ini`.

**Solucion:** Verificar las rutas. Asegurarse de que:

- El repositorio esta en `~/tectonic/`
- El archivo de configuracion esta en `~/tectonic.ini`
- El directorio de escenarios existe en `~/Curso_Tectonic_BHU/escenarios/`

### 9.5 Entorno virtual no se activa

**Sintoma:** El comando `source ~/.tectonic/bin/activate` falla.

**Solucion:**

```bash
# Recrear el entorno virtual
rm -rf ~/.tectonic
python3 -m venv ~/.tectonic
source ~/.tectonic/bin/activate
pip install --upgrade pip
pip install -r ~/tectonic/requirements.txt
```

### 9.6 Notas para usuarios de Windows (WSL2)

Si estas ejecutando Ubuntu en WSL2 desde Windows:

1. **Memoria:** WSL2 comparte la memoria RAM con Windows. En el archivo `C:\Users\<tu_usuario>\.wslconfig` puedes limitar o garantizar memoria:

```ini
[wsl2]
memory=12GB
swap=4GB
processors=4
```

2. **Puertos:** Los puertos de WSL2 son accesibles desde Windows directamente via `localhost`. No es necesario configurar port forwarding para pruebas basicas.

3. **Docker Desktop:** Si usas Docker Desktop en Windows con el backend de WSL2, asegurate de que Docker Desktop esta configurado para usar el contexto WSL2. Verificar con:

```bash
docker context ls
```

4. **Archivos en disco:** El rendimiento es mejor cuando los archivos del proyecto estan en el filesystem de Linux (`/home/` o `/root/`), no en un disco montado de Windows (`/mnt/c/`).

5. **Puertos expuestos:** Si necesitas acceder a los servicios del escenario desde el navegador de Windows, usa la IP del host WSL2. Obtenerla con:

```bash
hostname -I
```

---

## 10. Requisitos de red y reglas de firewall

### 10.1 Puertos utilizados por Docker

Tectonic crea redes Docker internas para cada escenario. Los puertos que se exponen dependen de cada escenario, pero comunmente se usan:

| Puerto | Servicio comun         |
|--------|------------------------|
| 80     | HTTP (web servers)     |
| 443    | HTTPS                  |
| 3306   | MySQL                  |
| 5432   | PostgreSQL             |
| 8080   | HTTP alternativo       |
| 22     | SSH                    |

### 10.2 Configurar UFW (Ubuntu Firewall)

Si UFW esta activo, permitir el trafico de Docker:

```bash
# Verificar estado de UFW
sudo ufw status

# Permitir trafico en la interfaz Docker
sudo ufw allow in on docker0

# Permitir los puertos comunmente usados por escenarios
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 8080/tcp
```

### 10.3 Reglas de iptables para Docker

Docker manipula las reglas de iptables automaticamente. Si usas iptables directamente, asegurate de que las reglas de Docker no sean eliminadas. Evitar ejecutar:

```bash
# NO ejecutar esto si usas Docker, puede romper la red de contenedores
sudo iptables -F
```

### 10.4 Redes Docker internas

Cada escenario de Tectonic crea sus propias redes Docker. Para listarlas:

```bash
docker network ls
```

No es necesario configurar estas redes manualmente; Tectonic las gestiona automaticamente.

### 10.5 Acceso desde fuera de la maquina

Si necesitas acceder a los escenarios desde otra maquina en la red local:

1. Verificar que el firewall del host permite el trafico entrante en los puertos necesarios.
2. Usar la IP del host (no `127.0.0.1`) para conectarse.
3. Algunos escenarios pueden requerir configuracion adicional para bindings en `0.0.0.0` en vez de `127.0.0.1`. Revisar la documentacion de cada escenario.

---

## Resumen rapido de comandos

```bash
# Activar entorno virtual
source ~/.tectonic/bin/activate

# Listar escenarios
python3 ~/tectonic/tectonic.py list

# Desplegar escenario
python3 ~/tectonic/tectonic.py deploy <escenario>

# Ver contenedores activos
docker ps

# Detener y eliminar escenario
python3 ~/tectonic/tectonic.py destroy <escenario>

# Desactivar entorno virtual
deactivate
```

---

## Contacto

Para consultas sobre el curso contactar a los docentes del BHU.

Para problemas con Tectonic, abrir un issue en el repositorio:  
https://github.com/GSI-Fing-Udelar/tectonic/issues
