# Clase 13: Hardening de Docker y Contenedores

**Duracion:** 2 horas

---

## Objetivos de Aprendizaje

1. Comprender las diferencias de seguridad entre contenedores y maquinas virtuales
2. Identificar los principales riesgos de seguridad en entornos Docker
3. Escribir Dockerfiles seguros siguiendo las mejores practicas
4. Hardening del host Docker (daemon) y aplicacion de limites de recursos
5. Auditar la configuracion de Docker con Docker Bench Security
6. Escanear imagenes en busca de vulnerabilidades con Trivy
7. Disenar redes y secretos seguros en entornos multi-contenedor

---

## Contenido Detallado

### 1. Introduccion a contenedores y Docker

#### Que es Docker

Docker es una plataforma de contenedorizacion que permite empaquetar aplicaciones con sus dependencias en unidades estandarizadas llamadas **contenedores**. A diferencia de las maquinas virtuales, los contenedores comparten el kernel del sistema operativo host.

**Analogia:** Una VM es como una casa independiente con su propia infraestructura (tuberias, electricidad). Un contenedor es como un departamento dentro de un edificio: comparte las tuberias y electricidad del edificio (el kernel del host) pero tiene sus propias habitaciones (sistema de archivos, procesos).

#### Contenedores vs VMs

| Caracteristica | Maquina Virtual | Contenedor Docker |
|---------------|-----------------|-------------------|
| Kernel | Propio (cada VM tiene su kernel) | Comparte el kernel del host |
| Aislamiento | Completo (hipervisor) | A nivel de procesos (namespaces) |
| Arranque | Minutos | Segundos |
| Tamanio | GB | MB |
| Consumo | Alto (SO completo por VM) | Bajo (solo bibliotecas necesarias) |
| Seguridad | Barrera fuerte (hipervisor) | Barrera mas debil (mismo kernel) |
| Portabilidad | Dependiente del hipervisor | Estandarizada (imagenes OCI) |

#### Vocabulario basico

- **Imagen:** Plantilla de solo lectura con el sistema de archivos del contenedor. Se construye con un Dockerfile.
- **Contenedor:** Instancia en ejecucion de una imagen. Tiene su propio sistema de archivos, red y procesos.
- **Dockerfile:** Receta en texto plano que define como construir una imagen.
- **docker-compose:** Herramienta para definir y ejecutar aplicaciones multi-contenedor.
- **Registry:** Repositorio de imagenes (Docker Hub, registries privados).

#### Por que la seguridad en contenedores es diferente

Los contenedores comparten el kernel del host. Esto tiene implicaciones profundas para la seguridad:

1. **Misma superficie de kernel:** Una vulnerabilidad en el kernel del host afecta a todos los contenedores y viceversa.
2. **Container escape:** Si un atacante rompe el aislamiento del contenedor, obtiene acceso al host directamente.
3. **Namespaces compartidos:** PID, network, mount, user, UTS, IPC namespaces pueden filtrar informacion entre contenedores.
4. **Cgroups debiles:** Los control groups limitan recursos pero no son una barrera de seguridad solida.
5. **Ejecucion privilegiada:** Por defecto, los procesos dentro del contenedor se ejecutan como root (aunque es root dentro del namespace, no root del host).

---

### 2. Principales riesgos de seguridad en Docker

#### Container escape (salirse del contenedor al host)

Es el riesgo mas grave. Ocurre cuando un proceso dentro del contenedor logra romper el aislamiento y ejecutar codigo en el host. Formas comunes:

- Montar `/var/run/docker.sock` dentro del contenedor (el contenedor obtiene control del daemon Docker del host).
- Ejecucion con `--privileged` (permite acceso a todos los dispositivos del host).
- Montar `/proc` o `/sys` del host (fuga de informacion del kernel).
- Vulnerabilidades de kernel (CVE-2022-0847 "Dirty Pipe", CVE-2024-...).

#### Privilege escalation dentro del contenedor

Incluso sin escapar al host, un atacante puede escalar privilegios dentro del contenedor si:

- El contenedor se ejecuta como root (por defecto).
- Hay binarios SUID disponibles (como `mount`, `su`, `sudo`).
- Hay capabilities peligrosas como `CAP_SYS_ADMIN` o `CAP_DAC_OVERRIDE`.

#### Imagenes con vulnerabilidades

- Imagenes base desactualizadas (Ubuntu 18.04 con paquetes sin parches).
- Dependencias con CVEs conocidos (Log4j, OpenSSL Heartbleed, etc.).
- Uso de tags `latest` que cambian sin control de versiones.

#### Secretos expuestos

- Claves API, contrasenas, tokens hardcodeados en la imagen.
- Variables de entorno usadas para pasar secretos (visibles con `docker inspect`).
- Secretos en capas intermedias de la imagen (incluso si se borran en una capa posterior).

#### Redes mal configuradas

- Todos los puertos expuestos hacia el host y la red externa.
- Contenedores conectados a `--net=host` (comparten la red del host sin aislamiento).
- Sin segmentacion de redes entre frontend, backend y base de datos.

#### Montajes de volumenes peligrosos

Los montajes mas peligrosos son:

- `/var/run/docker.sock` -> Control total del daemon Docker.
- `/proc` -> Fuga de informacion del kernel y procesos del host.
- `/sys` -> Permite modificar parametros del kernel.
- `/dev` -> Acceso a dispositivos del host.
- Directorios del sistema (`/etc`, `/var/log`, `/root`).

#### Ejecucion como root dentro del contenedor

Por defecto, Docker ejecuta procesos como root dentro del contenedor (UID 0). Aunque el root del contenedor esta mappeado al UID 0 del host, si hay un container escape, el atacante ya tiene UID 0 en el host.

---

### 3. Buenas practicas de hardening en Docker (Dockerfile seguro)

#### Usar imagenes base oficiales y ligeras

| Imagen | Tamanio aprox | Uso recomendado |
|--------|--------------|-----------------|
| `alpine:3.19` | ~7 MB | Apps estaticas, scripts, Go, Rust |
| `python:3.11-alpine3.19` | ~50 MB | Aplicaciones Python |
| `node:20-alpine3.19` | ~120 MB | Aplicaciones Node.js |
| `distroless` (gcr.io/distroless) | ~20-50 MB | Solo binario + runtime, sin shell ni gestor de paquetes |
| `scratch` | 0 bytes | Binarios estaticos compilados (Go, Rust) |

Regla general: cuanto mas pequena la imagen, menor superficie de ataque.

#### NO usar `latest`, usar tags especificos

**MAL:**
```dockerfile
FROM python:latest
```

**BIEN:**
```dockerfile
FROM python:3.11-alpine3.19
```

`latest` cambia en cualquier momento. Una imagen que funcionaba hoy puede tener vulnerabilidades manana. Siempre fijar version.

#### Escanear imagenes con Docker Scout o Trivy

```bash
# Docker Scout (integrado en Docker Desktop)
docker scout quickview alpine:3.19

# Trivy (herramienta externa, mas potente)
trivy image python:3.11-alpine3.19
```

#### Ejecutar como no-root: USER appuser

```dockerfile
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser
```

#### Minimizar capas: combinar RUN commands

```dockerfile
# MAL (3 capas)
RUN apk update
RUN apk add curl
RUN rm -rf /var/cache/apk/*

# BIEN (1 capa)
RUN apk update && apk add --no-cache curl
```

El flag `--no-cache` evita que el cache de paquetes quede en la imagen.

#### NO instalar paquetes innecesarios

```dockerfile
# MAL
RUN apk add curl vim git bash openssh

# BIEN (solo lo necesario)
RUN apk add --no-cache --virtual .build-deps gcc musl-dev && \
    pip install --no-cache-dir flask && \
    apk del .build-deps
```

#### Usar COPY en vez de ADD

`COPY` copia archivos locales al contenedor. `ADD` hace lo mismo pero ademas puede:

- Descargar URLs automaticamente (peligroso: podria cambiar el contenido).
- Extraer archivos tar automaticamente (comportamiento implicito).

```dockerfile
# MAL (ADD puede descargar de internet sin control de version)
ADD https://example.com/script.sh /tmp/

# BIEN (COPY solo copia local)
COPY script.sh /tmp/
```

#### HEALTHCHECK para monitoreo

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:8000/health || exit 1
```

#### No exponer puertos innecesarios

Exponer solo los puertos que la aplicacion necesita.

```dockerfile
EXPOSE 8000
# No exponer 22, 443, etc. si no se usan dentro del contenedor
```

#### Usar multi-stage builds

Las multi-stage builds permiten separar el entorno de compilacion (con todas las herramientas de desarrollo) de la imagen final (solo el binario y runtime).

```dockerfile
# Stage 1: compilacion (con herramientas)
FROM golang:1.21-alpine3.19 AS builder
RUN apk add --no-cache gcc musl-dev
WORKDIR /src
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -o /app/myapp

# Stage 2: imagen final (solo binario)
FROM alpine:3.19
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
COPY --from=builder /app/myapp /app/myapp
USER appuser
EXPOSE 8080
ENTRYPOINT ["/app/myapp"]
```

#### Fijar versiones de paquetes

```dockerfile
# MAL (version variable)
RUN apk add curl

# BIEN (version fija)
RUN apk add curl=8.5.0-r0
```

#### No incluir secretos en imagenes

```dockerfile
# MAL - el secreto queda en la imagen para siempre
ENV API_KEY=sk-123456789
ARG DB_PASSWORD=supersecreto

# BIEN - usar build args externos o secrets de Docker
ARG API_KEY
ENV API_KEY=${API_KEY}

# Aun mejor: usar secrets de BuildKit
# docker build --secret id=api_key,env=API_KEY .
RUN --mount=type=secret,id=api_key echo "Key used during build"
```

#### Ejemplo Dockerfile seguro (completo)

```dockerfile
# ============================================
# Dockerfile seguro para aplicacion Flask
# ============================================

# Stage 1: construir dependencias
FROM python:3.11-alpine3.19 AS builder

RUN apk add --no-cache --virtual .build-deps gcc musl-dev && \
    pip install --no-cache-dir flask gunicorn && \
    apk del .build-deps

# Stage 2: imagen final (solo runtime)
FROM python:3.11-alpine3.19

# Crear usuario no-root
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Establecer directorio de trabajo
WORKDIR /app

# Copiar dependencias desde builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copiar codigo de la aplicacion
COPY app.py .

# Ejecutar como usuario no privilegiado
USER appuser

# Exponer solo el puerto necesario
EXPOSE 8000

# Healthcheck para monitoreo
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:8000/health || exit 1

# Comando de entrada
ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]
```

---

### 4. Hardening del host Docker (docker daemon)

El daemon de Docker (`dockerd`) es el componente central que gestiona contenedores, imagenes, redes y volumenes. Su configuracion es fundamental para la seguridad de todo el sistema.

#### Configuracion en /etc/docker/daemon.json

```json
{
  "icc": false,
  "userns-remap": "default",
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  },
  "live-restore": true,
  "userland-proxy": false,
  "no-new-privileges": true,
  "selinux-enabled": true
}
```

**Explicacion de cada opcion:**

| Opcion | Valor | Explicacion |
|--------|-------|-------------|
| `icc` | `false` | Inter-Container Communication deshabilitada. Los contenedores no pueden comunicarse entre si a menos que esten en la misma red definida por el usuario |
| `userns-remap` | `"default"` | Mapea el UID 0 del contenedor a un UID no privilegiado del host. Si un atacante escapa del contenedor como root, en el host es un usuario sin privilegios |
| `log-driver` | `"json-file"` | Formato de logs estructurado |
| `max-size` | `"10m"` | Cada archivo de log se limita a 10MB (evita DoS por logs) |
| `max-file` | `3` | Solo se conservan 3 archivos de log rotados |
| `live-restore` | `true` | Los contenedores siguen ejecutandose si el daemon se reinicia |
| `userland-proxy` | `false` | Deshabilita el proxy en espacio de usuario para el reenvio de puertos. Usa iptables directamente |
| `no-new-privileges` | `true` | Los procesos dentro del contenedor no pueden ganar nuevos privilegios (via SUID, capabilities, etc.) |
| `selinux-enabled` | `true` | Activa etiquetado SELinux para contenedores (si SELinux esta disponible en el host) |

**Aplicar configuracion:**

```bash
sudo mkdir -p /etc/docker
sudo cp daemon.json /etc/docker/daemon.json
sudo systemctl restart docker

# Verificar que los cambios se aplicaron
docker info | grep -E "(Security|Remap|no-new-privileges)"
```

#### No exponer el socket de Docker

El socket de Docker (`/var/run/docker.sock`) es el punto de control del daemon. **NUNCA** debe montarse dentro de un contenedor a menos que sea absolutamente necesario (como en herramientas de orquestacion tipo Portainer).

```yaml
# PELIGRO: montar el socket da control total del host al contenedor
volumes:
  - /var/run/docker.sock:/var/run/docker.sock
```

Si un atacante obtiene acceso al contenedor, puede ejecutar cualquier comando Docker en el host.

---

### 5. Docker Bench Security

Docker Bench Security es un script que verifica la configuracion de Docker contra el CIS (Center for Internet Security) Benchmark para Docker.

#### Que es

- Script bash que ejecuta cientos de pruebas automatizadas.
- Clasifica los resultados en: PASS, WARNING, INFO.
- Cubre: configuracion del host, configuracion del daemon, contenedores en ejecucion, imagenes, redes, y mas.

#### Instalacion

```bash
git clone https://github.com/docker/docker-bench-security.git
cd docker-bench-security
```

#### Ejecucion

```bash
sudo sh docker-bench-security.sh
```

Para ejecutar solo un grupo especifico:

```bash
sudo sh docker-bench-security.sh -c container_images
sudo sh docker-bench-security.sh -c docker_daemon_configuration
```

#### Interpretar resultados

La salida se ve asi:

```
[INFO] 1 - Host Configuration
[PASS] 1.1  - Ensure a separate partition for containers has been created
[WARN] 1.2  - Ensure the container host has been Hardened
[INFO] 1.3  - Ensure Docker is for the latest version
[PASS] 1.4  - Ensure only trusted users are allowed to control Docker daemon
[INFO] 1.5  - Ensure auditing is configured for the Docker daemon

[INFO] 2 - Docker Daemon Configuration
[PASS] 2.1  - Ensure network traffic is restricted between containers
[WARN] 2.2  - Ensure the Docker daemon is configured to use seccomp profile
[PASS] 2.3  - Ensure that authorization for Docker client commands is enabled
...
```

Cada resultado se interpreta asi:

- **PASS:** La prueba paso, la configuracion es correcta.
- **WARN:** La configuracion no es la ideal (mejorable).
- **INFO:** Informativo, no es una prueba de seguridad directa.

Al final, el script muestra un resumen:

```
[INFO] Checks: 98
[PASS] 52
[WARN] 12
[INFO] 34
```

El objetivo es maximizar los PASS y minimizar los WARN.

---

### 6. Escaneo de imagenes con Trivy

Trivy es un escaner de vulnerabilidades de codigo abierto desarrollado por Aqua Security.

#### Instalacion

```bash
# Windows (PowerShell)
winget install aquasecurity.trivy

# Linux
curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sudo sh

# macOS
brew install trivy

# Con Docker
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy image alpine:3.19
```

#### Escaneo de imagenes

```bash
# Escaneo basico
trivy image alpine:latest

# Escaneo por severidad (solo CRITICAL y HIGH)
trivy image --severity=CRITICAL,HIGH python:3.11-slim

# Escaneo ignorando bases de datos sin parche
trivy image --ignore-unfixed python:3.11-slim

# Escaneo con salida JSON para automatizar
trivy image --format json --output report.json alpine:3.19

# Escaneo con salida HTML
trivy image --format html --output report.html alpine:3.19
```

#### Escaneo de sistema de archivos (IaC)

```bash
# Escanear el proyecto actual en busca de vulnerabilidades
trivy fs --severity=CRITICAL .
```

#### Interpretar resultados

```
alpine:3.19 (alpine 3.19.0)
===========================
Total: 3 (UNKNOWN: 0, LOW: 2, MEDIUM: 1, HIGH: 0, CRITICAL: 0)

+---------------+------------------+----------+-----------+---------+------------------+
|   LIBRARY     | VULNERABILITY ID | SEVERITY | INSTALLED | FIXED   |     TITLE        |
+---------------+------------------+----------+-----------+---------+------------------+
| libcrypto3    | CVE-2024-0001    | MEDIUM   | 3.1.4-r0  | 3.1.5   | OpenSSL vuln     |
| libssl3       | CVE-2024-0001    | MEDIUM   | 3.1.4-r0  | 3.1.5   | OpenSSL vuln     |
| zlib          | CVE-2023-45853   | LOW      | 1.3-r0    | 1.3.1   | zlib inflate     |
+---------------+------------------+----------+-----------+---------+------------------+
```

**Columnas:**
- **LIBRARY:** Paquete vulnerable.
- **VULNERABILITY ID:** Identificador CVE.
- **SEVERITY:** CRITICAL, HIGH, MEDIUM, LOW.
- **INSTALLED:** Version instalada.
- **FIXED:** Version en que se corrigio la vulnerabilidad.
- **TITLE:** Breve descripcion.

#### Integrar en CI/CD

```yaml
# Ejemplo de GitHub Actions
- name: Scan image with Trivy
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: 'myapp:latest'
    format: 'sarif'
    output: 'trivy-results.sarif'
    severity: 'CRITICAL,HIGH'
```

---

### 7. Limites de recursos (resource constraints)

Los contenedores sin limites de recursos pueden consumir toda la CPU, memoria o espacio en disco del host, causando una denegacion de servicio (DoS).

#### Limitar memoria

```bash
docker run --memory="256m" --memory-swap="512m" myapp
```

- `--memory`: Memoria maxima que puede usar el contenedor.
- `--memory-swap`: Memoria + swap maximo. Si es igual a memory, no hay swap.
- `--memory-reservation`: Memoria suave (no es un limite estricto, solo se aplica cuando hay presion de memoria).

#### Limitar CPU

```bash
docker run --cpus="0.5" myapp
```

- `--cpus`: Numero de CPUs (0.5 = medio nucleo).
- `--cpu-shares`: Peso relativo (por defecto 1024). Un contenedor con 2048 tiene el doble de prioridad de CPU.
- `--cpuset-cpus`: CPUs especificas (ej: `--cpuset-cpus=0,2`).

#### Limitar reinicios

```bash
docker run --restart=on-failure:3 myapp
```

Politicas de restart:
- `no`: No reiniciar automaticamente (por defecto).
- `on-failure`: Reiniciar si el contenedor sale con codigo de error.
- `always`: Reiniciar siempre (incluso si se detiene manualmente).
- `unless-stopped`: Reiniciar siempre excepto si se detuvo manualmente.

#### Ejemplo completo

```bash
docker run -d \
  --name myapp \
  --memory="256m" \
  --memory-swap="512m" \
  --cpus="0.5" \
  --restart=on-failure:3 \
  --cap-drop=ALL \
  --cap-add=NET_BIND_SERVICE \
  --read-only \
  --tmpfs /tmp:rw,noexec,nosuid,size=64m \
  myapp:1.0
```

---

### 8. Capacidades de Linux (capabilities)

Las capabilities son privilegios granulares del kernel de Linux. En lugar de dar acceso total como root, Docker permite asignar capacidades especificas a un contenedor.

#### Capacidades por defecto en Docker

Docker otorga un subconjunto de capacidades a cada contenedor, como:

- `CHOWN`: Cambiar propietario de archivos.
- `DAC_OVERRIDE`: Omitir controles de permisos.
- `FOWNER`: Omitir restricciones de propietario.
- `KILL`: Enviar se~nales a procesos.
- `NET_BIND_SERVICE`: Vincular puertos por debajo de 1024.
- `NET_RAW`: Usar sockets RAW.
- `SETGID`, `SETUID`: Cambiar GID/UID.
- `SYS_CHROOT`: Llamar a chroot.

#### Eliminar capacidades innecesarias

```bash
# Eliminar todas las capacidades y solo agregar las necesarias
docker run --cap-drop=ALL --cap-add=NET_BIND_SERVICE myapp
```

Si la aplicacion solo necesita escuchar en un puerto, con `NET_BIND_SERVICE` es suficiente. No necesita `SYS_ADMIN`, `DAC_OVERRIDE`, `NET_RAW`, etc.

#### Peligro de --privileged

El flag `--privileged` otorga **todas** las capacidades y da acceso a todos los dispositivos del host. Equivale a ejecutar como root en el host.

```bash
# PELIGRO: equivalente a root del host
docker run --privileged myapp

# Alternativa segura: solo las capacidades necesarias
docker run --cap-drop=ALL --cap-add=NET_BIND_SERVICE myapp
```

---

### 9. Redes seguras en Docker

#### Usar redes definidas por el usuario

Las redes por defecto (`bridge`) no tienen aislamiento entre contenedores. Las redes definidas por el usuario permiten controlar la comunicacion.

```bash
# Crear red aislada (sin acceso externo)
docker network create --internal isolated-net

# Crear red con control de subred
docker network create --subnet=10.10.0.0/16 backend-net

# Conectar contenedor a la red
docker run --network=isolated-net myapp
```

#### Aislar contenedores entre si

```yaml
# docker-compose.yml con redes separadas
services:
  frontend:
    networks:
      - frontend-net
      - backend-net
  api:
    networks:
      - backend-net
      - db-net
  db:
    networks:
      - db-net

networks:
  frontend-net:
    driver: bridge
  backend-net:
    driver: bridge
    internal: true  # sin acceso externo
  db-net:
    driver: bridge
    internal: true
```

Con esta configuracion:
- El frontend solo habla con la API (backend-net).
- La API solo habla con frontend y base de datos.
- La base de datos solo habla con la API y no tiene acceso a Internet.

#### No publicar puertos innecesarios

```bash
# MAL: expone puertos al host
docker run -p 80:80 -p 443:443 -p 3306:3306 myapp

# BIEN: solo exponer lo necesario
docker run -p 80:80 myapp
```

Cada puerto publicado es una entrada al contenedor. Menos puertos, menos superficie de ataque.

---

### 10. Secretos en Docker

#### Diferencia entre formas de pasar datos sensibles

| Metodo | Visible en `docker inspect` | Persiste en la imagen | Recomendado para |
|--------|---------------------------|----------------------|------------------|
| `ENV` en Dockerfile | Si | Si | Configuracion no sensible |
| `ARG` en Dockerfile | Solo durante build | No en imagen final | Datos de compilacion |
| `environment:` en compose | Si | No | Configuracion general |
| Docker Secrets (Swarm) | No | No | Contrasenas, claves |

#### Evitar secretos en imagenes

```dockerfile
# MAL: el secreto queda en la imagen
ENV DB_PASSWORD=supersecreto
ENV API_KEY=sk-12345

# BIEN: usar build args (no persisten en la imagen)
ARG DB_PASSWORD
ENV DB_PASSWORD=${DB_PASSWORD}

# MEJOR: pasar en tiempo de ejecucion
# docker run -e DB_PASSWORD=supersecreto myapp
```

#### Docker Compose con secrets

```yaml
version: "3.8"
services:
  app:
    image: myapp:1.0
    secrets:
      - db_password
      - api_key

secrets:
  db_password:
    file: ./secrets/db_password.txt
  api_key:
    file: ./secrets/api_key.txt
```

Los archivos en `./secrets/` se montan en `/run/secrets/` dentro del contenedor.

```python
# Leer secreto desde la aplicacion
with open('/run/secrets/db_password', 'r') as f:
    db_password = f.read().strip()
```

---

### 11. docker-compose seguro

#### Buenas practicas en docker-compose.yml

1. **No exponer puertos innecesarios:** Solo los puertos que la aplicacion necesita.
2. **Limitar recursos:** CPU, memoria, reinicios.
3. **Redes separadas:** Diferentes redes para frontend, backend y base de datos.
4. **Secrets management:** Usar `secrets:` para datos sensibles.
5. **Healthchecks:** Monitorear el estado de los servicios.
6. **Restart policies:** Configurar reinicios controlados.
7. **Usuario no-root:** Ejecutar con `user:` en cada servicio.
8. **Solo lectura:** Usar `read_only: true` cuando sea posible.
9. **Capabilities minimas:** `cap_drop: ALL` + `cap_add: NET_BIND_SERVICE`.

#### Ejemplo de docker-compose.yml seguro

```yaml
version: "3.8"

services:
  app:
    build:
      context: ./app
      dockerfile: Dockerfile.secure
    image: myapp:1.0
    user: "1001:1001"
    read_only: true
    tmpfs:
      - /tmp:rw,noexec,nosuid,size=64m
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE
    security_opt:
      - no-new-privileges:true
    deploy:
      resources:
        limits:
          cpus: "0.5"
          memory: 256M
        reservations:
          memory: 128M
    healthcheck:
      test: ["CMD", "wget", "--spider", "http://localhost:8000/health"]
      interval: 30s
      timeout: 3s
      retries: 3
      start_period: 10s
    restart: on-failure:3
    secrets:
      - db_password
    networks:
      - frontend-net
      - backend-net
    depends_on:
      db:
        condition: service_healthy

  db:
    image: postgres:16-alpine
    user: "999:999"
    volumes:
      - pgdata:/var/lib/postgresql/data
    cap_drop:
      - ALL
    cap_add:
      - CHOWN
      - SETUID
      - SETGID
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U appuser"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped
    secrets:
      - db_password
    environment:
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
      POSTGRES_USER: appuser
      POSTGRES_DB: myapp
    networks:
      - backend-net
      - db-net

  redis:
    image: redis:7-alpine
    user: "999:999"
    volumes:
      - redisdata:/data
    cap_drop:
      - ALL
    cap_add:
      - SETUID
      - SETGID
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 5
    restart: unless-stopped
    networks:
      - backend-net
      - db-net

volumes:
  pgdata:
  redisdata:

secrets:
  db_password:
    file: ./secrets/db_password.txt

networks:
  frontend-net:
    driver: bridge
  backend-net:
    driver: bridge
    internal: true
  db-net:
    driver: bridge
    internal: true
```

**Explicacion de las medidas de seguridad aplicadas:**

- **Usuario no-root:** Cada servicio usa `user: "UID:GID"` para no ejecutar como root.
- **read_only:** El sistema de archivos del contenedor es de solo lectura.
- **tmpfs:** Directorios temporales en memoria (sin escribir en disco).
- **cap_drop/cap_add:** Solo las capacidades estrictamente necesarias.
- **no-new-privileges:** Los procesos no pueden escalar privilegios.
- **Limites de recursos:** CPU y memoria acotados.
- **Healthchecks:** Docker sabe si el servicio esta funcionando correctamente.
- **Redes internas:** `db-net` y `backend-net` son internas (sin acceso externo).
- **Secrets:** La contrasena se monta como archivo, no como variable de entorno.
- **Volumenes nombrados:** Para datos persistentes de PostgreSQL y Redis.

---

### 12. Herramientas complementarias

| Herramienta | Funcion | URL / Instalacion |
|-------------|---------|-------------------|
| **Trivy** | Escaneo de vulnerabilidades en imagenes, fs, IaC, k8s | `brew install trivy` / `winget install aquasecurity.trivy` |
| **Docker Bench Security** | Auditoria CIS Benchmark para Docker | `git clone https://github.com/docker/docker-bench-security.git` |
| **Hadolint** | Linter de Dockerfiles | `brew install hadolint` / `docker run --rm -v $PWD:/data hadolint/hadolint hadolint /data/Dockerfile` |
| **Clair** | Escaneo estatico de imagenes en registries | Proyecto de Red Hat, integrado en Quay.io y Harbor |
| **Falco** | Runtime security para contenedores | `curl -fsSL https://falco.org/install | bash` |
| **Docker Scout** | Escaneo integrado en Docker Desktop | `docker scout quickview <image>` |
| **Snyk** | Escaneo de vulnerabilidades en contenedores | `npm install -g snyk && snyk auth` |

---

### 13. Ejercicio 1 - Dockerfile hardening

**Enunciado:** El siguiente Dockerfile es INSEGURO. Reescribirlo siguiendo todas las buenas practicas de seguridad.

```dockerfile
FROM ubuntu:latest

ENV API_KEY=sk-1234567890
ENV DB_PASSWORD=admin123

RUN apt-get update
RUN apt-get install -y python3 python3-pip curl vim git netcat
RUN pip install flask

ADD https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh /wait-for-it.sh

COPY app.py .
COPY entrypoint.sh .

EXPOSE 80
EXPOSE 443
EXPOSE 3306

ENTRYPOINT ["/entrypoint.sh"]
CMD ["python3", "app.py"]
```

##### Solucion

**Problemas identificados:**
1. Usa `ubuntu:latest` (imagen enorme y tag variable).
2. Secretos hardcodeados (`API_KEY`, `DB_PASSWORD`).
3. `apt-get update` sin cache ni limpieza.
4. Paquetes innecesarios (`vim`, `git`, `netcat`).
5. `ADD` descarga URL (no control de version).
6. Se ejecuta como root (no hay `USER`).
7. Expone puertos innecesarios (443, 3306).
8. No hay healthcheck.
9. No hay control de versiones de paquetes.
10. No uso de multi-stage build.

**Dockerfile corregido:**

```dockerfile
# ============================================
# Dockerfile seguro para aplicacion Flask
# ============================================

# Stage 1: construir dependencias
FROM python:3.11-slim-bookworm AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libc6-dev \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir flask gunicorn

# Stage 2: imagen final
FROM python:3.11-slim-bookworm

# Crear usuario no-root
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

# Establecer directorio de trabajo
WORKDIR /app

# Copiar dependencias desde builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copiar solo los archivos necesarios
COPY app.py .
COPY entrypoint.sh .

# Hacer entrypoint ejecutable
RUN chmod +x entrypoint.sh

# NO incluir secretos en la imagen
# Los secretos se pasan en tiempo de ejecucion:
# docker run -e API_KEY=<key> -e DB_PASSWORD=<pass> myapp-secure

# Ejecutar como usuario no privilegiado
USER appuser

# Exponer solo el puerto necesario
EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:8000/health || exit 1

# Comando de entrada
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]
```

**Principales mejoras aplicadas:**

| Aspecto | Antes | Despues |
|---------|-------|---------|
| Imagen base | `ubuntu:latest` (tag variable, ~200MB) | `python:3.11-slim-bookworm` (tag fijo, ~120MB) |
| Construccion | Una sola etapa | Multi-stage (imagen final mas pequena) |
| Paquetes | `vim`, `git`, `netcat`, `curl` innecesarios | Solo `gcc`, `libc6-dev` en builder, eliminados en etapa final |
| Secretos | `ENV API_KEY=...` hardcodeado | No hay secretos en la imagen |
| Usuario | root (por defecto) | `appuser` (no-root) |
| Puertos | 80, 443, 3306 (innecesarios) | Solo 8000 |
| Healthcheck | No tiene | Configurado con HEALTHCHECK |
| Cache | No se limpia | `--no-cache-dir`, `rm -rf /var/lib/apt/lists/*` |
| ADD | Descarga URL sin control | COPY desde builder |

---

### 14. Ejercicio 2 - Docker Bench Security

**Enunciado:** Instalar Docker Bench Security, ejecutarlo, interpretar los resultados y corregir al menos 5 hallazgos criticos.

##### Solucion

**Paso 1: Clonar e instalar**

```bash
git clone https://github.com/docker/docker-bench-security.git
cd docker-bench-security
```

**Paso 2: Ejecutar auditoria inicial**

```bash
sudo sh docker-bench-security.sh
```

**Paso 3: Salida tipica (parcial)**

```
[INFO] 1 - Host Configuration
[WARN] 1.1  - Ensure a separate partition for containers has been created
[PASS] 1.2  - Ensure the container host has been Hardened
[INFO] 1.3  - Ensure Docker is for the latest version
[PASS] 1.4  - Ensure only trusted users are allowed to control Docker daemon

[INFO] 2 - Docker Daemon Configuration
[WARN] 2.1  - Ensure network traffic is restricted between containers
[WARN] 2.2  - Ensure the Docker daemon is configured to use seccomp profile
[INFO] 2.3  - Ensure that authorization for Docker client commands is enabled
...

[INFO] 4 - Container Images and Build File
[WARN] 4.1  - Ensure a user for the container has been created
[WARN] 4.2  - Ensure that containers use trusted base images
...

[INFO] 5 - Container Runtime
[WARN] 5.1  - Ensure that, if applicable, an AppArmor profile is enabled
[WARN] 5.4  - Ensure containers are not running with privileged flag
[WARN] 5.7  - Ensure privileged ports are not mapped within containers
[WARN] 5.12 - Ensure the container's root filesystem is mounted as read only
[WARN] 5.19 - Ensure containers are restricted from acquiring new privileges
[WARN] 5.25 - Ensure the container is restricted from additional capabilities
[WARN] 5.31 - Ensure that the host's process namespace is not shared
```

**Paso 4: Resumen tipico**

```
[INFO] Checks: 98
[PASS] 45
[WARN] 28
[INFO] 25
```

**Paso 5: Correcciones aplicadas**

A continuacion, 5 correcciones para hallazgos criticos comunes:

**Correccion 1: Restringir trafico entre contenedores (test 2.1)**

```bash
# Configurar /etc/docker/daemon.json
sudo mkdir -p /etc/docker
sudo tee /etc/docker/daemon.json << EOF
{
  "icc": false,
  "userns-remap": "default",
  "no-new-privileges": true,
  "live-restore": true
}
EOF
sudo systemctl restart docker
```

**Correccion 2: Usar usuario no-root en contenedores (test 4.1)**

```bash
# En el Dockerfile de cada contenedor:
RUN groupadd -r appgroup && useradd -r -g appgroup appuser
USER appuser
```

**Correccion 3: No ejecutar con --privileged (test 5.4)**

```bash
# Usar capabilities especificas en vez de --privileged
docker run --cap-drop=ALL --cap-add=NET_BIND_SERVICE myapp
```

**Correccion 4: Sistema de archivos de solo lectura (test 5.12)**

```bash
docker run --read-only --tmpfs /tmp:rw,noexec,nosuid,size=64m myapp
```

**Correccion 5: Restringir nuevas capacidades (test 5.19)**

```bash
# En docker run
docker run --security-opt=no-new-privileges:true myapp

# En docker-compose.yml
security_opt:
  - no-new-privileges:true
```

**Paso 6: Ejecutar auditoria despues de correcciones**

```bash
sudo sh docker-bench-security.sh
```

**Resumen esperado despues de correcciones:**

```
[INFO] Checks: 98
[PASS] 68  (+23 respecto al inicial)
[WARN] 8   (-20 respecto al inicial)
[INFO] 22
```

---

### 15. Ejercicio 3 - Trivy scan

**Enunciado:** Escanear 3 imagenes (alpine:latest, python:3.11-slim, una propia). Mostrar vulnerabilidades encontradas y como remediarlas.

##### Solucion

**Paso 1: Escanear alpine:latest**

```bash
trivy image alpine:latest
```

**Salida tipica:**

```
alpine:latest (alpine 3.21.0)
==============================
Total: 2 (UNKNOWN: 0, LOW: 1, MEDIUM: 1, HIGH: 0, CRITICAL: 0)

+----------+------------------+----------+-----------+---------+------------------------------------+
| LIBRARY  | VULNERABILITY ID | SEVERITY | INSTALLED | FIXED   | TITLE                              |
+----------+------------------+----------+-----------+---------+------------------------------------+
| busybox  | CVE-2024-0001    | MEDIUM   | 1.36.1    | 1.36.2  | busybox: denial of service         |
| musl     | CVE-2023-1234    | LOW      | 1.2.5     | 1.2.6   | musl: minor information leak       |
+----------+------------------+----------+-----------+---------+------------------------------------+
```

**Remediacion:** Actualizar alpine a la version mas reciente o fijar una version parcheada.

```bash
# Verificar si hay version mas reciente
docker pull alpine:3.21

# O fijar una version sin vulnerabilidades conocidas
docker pull alpine:3.20.3
```

**Paso 2: Escanear python:3.11-slim**

```bash
trivy image --severity=CRITICAL,HIGH python:3.11-slim
```

**Salida tipica:**

```
python:3.11-slim (debian 12.0)
===============================
Total: 5 (CRITICAL: 1, HIGH: 4)

+------------+------------------+----------+-----------+---------+----------------------------------------+
| LIBRARY    | VULNERABILITY ID | SEVERITY | INSTALLED | FIXED   | TITLE                                  |
+------------+------------------+----------+-----------+---------+----------------------------------------+
| libc6      | CVE-2024-1000    | CRITICAL | 2.36-9   | 2.36-10 | glibc: buffer overflow in ...          |
| openssl    | CVE-2024-2000    | HIGH     | 3.0.11   | 3.0.12  | openssl: denial of service             |
| libssl3    | CVE-2024-2000    | HIGH     | 3.0.11   | 3.0.12  | openssl: denial of service             |
| curl       | CVE-2024-3000    | HIGH     | 7.88.1   | 7.88.2  | curl: heap buffer overflow             |
| zlib       | CVE-2023-4000    | HIGH     | 1.2.13   | 1.2.13.1| zlib: integer overflow                 |
+------------+------------------+----------+-----------+---------+----------------------------------------+
```

**Remediacion:**

```bash
# Opcion 1: Actualizar la imagen base
docker pull python:3.11-slim-bookworm  # version mas actualizada

# Opcion 2: Aplicar parches en el Dockerfile
RUN apt-get update && apt-get upgrade -y && rm -rf /var/lib/apt/lists/*

# Opcion 3: Usar alpine en vez de slim
FROM python:3.11-alpine3.19  # menos vulnerabilidades
```

**Paso 3: Escanear imagen propia**

Primero construir una imagen propia:

```bash
# Crear un Dockerfile simple
cat > Dockerfile.test << EOF
FROM node:18
WORKDIR /app
COPY package.json .
RUN npm install
COPY . .
EXPOSE 3000
CMD ["node", "app.js"]
EOF

# Construir la imagen
docker build -t myapp:test -f Dockerfile.test .

# Escanear
trivy image --severity=CRITICAL,HIGH myapp:test
```

**Salida tipica:**

```
myapp:test (debian 11.0)
========================
Total: 12 (CRITICAL: 3, HIGH: 9)

+----------------+------------------+----------+-----------+---------+-----------------------------------+
| LIBRARY        | VULNERABILITY ID | SEVERITY | INSTALLED | FIXED   | TITLE                             |
+----------------+------------------+----------+-----------+---------+-----------------------------------+
| nodejs         | CVE-2024-5000    | CRITICAL | 18.18.0   | 18.18.1 | nodejs: remote code execution     |
| libc6          | CVE-2024-1000    | CRITICAL | 2.31-13   | 2.31-14 | glibc: buffer overflow            |
| openssl        | CVE-2024-2000    | CRITICAL | 1.1.1n    | 1.1.1o  | openssl: RCE                      |
| ...            | ...              | HIGH     | ...       | ...     | ...                               |
+----------------+------------------+----------+-----------+---------+-----------------------------------+
```

**Remediacion de la imagen propia:**

1. Cambiar imagen base a `node:20-alpine3.19` (menos vulnerabilidades).
2. Actualizar dependencias de Node.js (`npm audit fix`).
3. Aplicar multi-stage build.
4. Solo copiar archivos necesarios (no `COPY . .`).

**Dockerfile corregido:**

```dockerfile
FROM node:20-alpine3.19 AS builder
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --only=production

FROM node:20-alpine3.19
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY app.js .
USER appuser
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:3000/health || exit 1
CMD ["node", "app.js"]
```

**Verificar que las vulnerabilidades se redujeron:**

```bash
docker build -t myapp:secure -f Dockerfile.secure .
trivy image --severity=CRITICAL,HIGH myapp:secure
```

Idealmente, la imagen corregida deberia tener 0 vulnerabilidades CRITICAL y HIGH.

---

### 16. Ejercicio 4 - docker-compose seguro

**Enunciado:** Crear un docker-compose.yml para una app web con Flask (Python) + PostgreSQL + Redis, aplicando todas las medidas de seguridad (usuario no-root, redes separadas, limites, healthchecks, secrets).

##### Solucion

**Estructura del proyecto:**

```
proyecto-seguro/
  app/
    Dockerfile.secure
    app.py
    requirements.txt
  secrets/
    db_password.txt
  docker-compose.yml
  .env
```

**Archivo app/Dockerfile.secure:**

```dockerfile
# ============================================
# Dockerfile seguro - Aplicacion Flask
# ============================================

FROM python:3.11-alpine3.19 AS builder

RUN apk add --no-cache --virtual .build-deps gcc musl-dev && \
    pip install --no-cache-dir --user flask gunicorn psycopg2-binary redis && \
    apk del .build-deps

FROM python:3.11-alpine3.19

RUN addgroup -S appgroup && adduser -S appuser -G appgroup

WORKDIR /app

COPY --from=builder /root/.local /home/appuser/.local
COPY app.py .
COPY requirements.txt .

ENV PATH=/home/appuser/.local/bin:$PATH

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:8000/health || exit 1

ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:8000", "-w", "2", "app:app"]
```

**Archivo app/app.py:**

```python
import os
import redis
import psycopg2
from flask import Flask, jsonify

app = Flask(__name__)

def get_db_connection():
    db_password = open('/run/secrets/db_password').read().strip()
    return psycopg2.connect(
        host=os.environ.get('DB_HOST', 'db'),
        dbname=os.environ.get('DB_NAME', 'myapp'),
        user=os.environ.get('DB_USER', 'appuser'),
        password=db_password
    )

def get_redis_connection():
    return redis.Redis(
        host=os.environ.get('REDIS_HOST', 'redis'),
        port=6379,
        decode_responses=True
    )

@app.route('/health')
def health():
    return jsonify({'status': 'ok'}), 200

@app.route('/')
def index():
    return jsonify({'message': 'Hello from secure Flask app!'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
```

**Archivo app/requirements.txt:**

```
flask==3.0.0
gunicorn==21.2.0
psycopg2-binary==2.9.9
redis==5.0.1
```

**Archivo secrets/db_password.txt:**

```
changeme_secure_password_12345
```

**Archivo docker-compose.yml:**

```yaml
version: "3.8"

services:
  app:
    build:
      context: ./app
      dockerfile: Dockerfile.secure
    image: flask-app-secure:1.0
    user: "1001:1001"
    read_only: true
    tmpfs:
      - /tmp:rw,noexec,nosuid,size=64m
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE
    security_opt:
      - no-new-privileges:true
    deploy:
      resources:
        limits:
          cpus: "0.5"
          memory: 256M
        reservations:
          memory: 128M
    healthcheck:
      test: ["CMD", "wget", "--spider", "http://localhost:8000/health"]
      interval: 30s
      timeout: 3s
      retries: 3
      start_period: 10s
    restart: on-failure:3
    secrets:
      - db_password
    environment:
      DB_HOST: db
      DB_NAME: myapp
      DB_USER: appuser
      REDIS_HOST: redis
    networks:
      - frontend-net
      - backend-net
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    ports:
      - "8000:8000"

  db:
    image: postgres:16-alpine
    user: "999:999"
    volumes:
      - pgdata:/var/lib/postgresql/data
    cap_drop:
      - ALL
    cap_add:
      - CHOWN
      - SETUID
      - SETGID
    security_opt:
      - no-new-privileges:true
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U appuser -d myapp"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 20s
    restart: unless-stopped
    secrets:
      - db_password
    environment:
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
      POSTGRES_USER: appuser
      POSTGRES_DB: myapp
    networks:
      - backend-net
      - db-net

  redis:
    image: redis:7-alpine
    user: "999:999"
    volumes:
      - redisdata:/data
    cap_drop:
      - ALL
    cap_add:
      - SETUID
      - SETGID
    security_opt:
      - no-new-privileges:true
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 5
    restart: unless-stopped
    networks:
      - backend-net
      - db-net

volumes:
  pgdata:
  redisdata:

secrets:
  db_password:
    file: ./secrets/db_password.txt

networks:
  frontend-net:
    driver: bridge
  backend-net:
    driver: bridge
    internal: true
  db-net:
    driver: bridge
    internal: true
```

**Resumen de medidas de seguridad:**

| Medida | Donde se aplica |
|--------|-----------------|
| Usuario no-root | `user:` en cada servicio + `USER` en Dockerfile |
| Sistema de archivos solo lectura | `read_only: true` en app |
| Directorios temporales en RAM | `tmpfs:` para /tmp |
| Capacidades minimas | `cap_drop: ALL` + `cap_add:` solo lo necesario |
| Sin nuevos privilegios | `security_opt: no-new-privileges:true` |
| Limites de recursos | `deploy.resources.limits` |
| Healthchecks | `healthcheck:` en cada servicio |
| Redes internas | `internal: true` en backend-net y db-net |
| Secretos | `secrets:` con archivos externos |
| Dependencias con healthcheck | `depends_on.condition: service_healthy` |

**Para ejecutar:**

```bash
# Iniciar todos los servicios
docker compose up -d

# Verificar estado
docker compose ps
docker compose logs app

# Verificar healthchecks
docker compose ps --format "table {{.Name}}\t{{.Status}}"

# Detener
docker compose down -v  # -v elimina volumenes
```

---

### 17. Ejercicio 5 - Hadolint

**Enunciado:** Analizar un Dockerfile con Hadolint y corregir todas las advertencias.

##### Solucion

**Paso 1: Instalar Hadolint**

```bash
# Usando Docker (mas facil, no requiere instalacion)
alias hadolint='docker run --rm -i -v ${PWD}:/data hadolint/hadolint < Dockerfile'

# O instalacion local (Linux/macOS)
# brew install hadolint
# or: wget https://github.com/hadolint/hadolint/releases/latest/download/hadolint-Linux-x86_64
```

**Paso 2: Dockerfile original (con problemas)**

```dockerfile
FROM ubuntu

MAINTAINER developer@example.com

RUN apt-get update
RUN apt-get install python3
RUN apt-get install python3-pip
RUN pip install flask

ADD app.py /app/
ADD https://example.com/script.sh /tmp/

EXPOSE 80
EXPOSE 443

CMD python app.py
```

**Paso 3: Ejecutar Hadolint**

```bash
hadolint Dockerfile.insecure
```

**Salida tipica de Hadolint:**

```
Dockerfile.insecure:1 DL3007 Using latest is prone to M311 error if the image will ever be updated. Pin the version explicitly.
Dockerfile.insecure:3 DL4000 MAINTAINER is deprecated. Use LABEL instead.
Dockerfile.insecure:5 DL3009 Delete the apt-get lists after installing something.
Dockerfile.insecure:5 DL3015 Avoid additional packages by specifying `--no-install-recommends`.
Dockerfile.insecure:6 DL3009 Delete the apt-get lists after installing something.
Dockerfile.insecure:6 DL3015 Avoid additional packages by specifying `--no-install-recommends`.
Dockerfile.insecure:7 DL3009 Delete the apt-get lists after installing something.
Dockerfile.insecure:8 DL3013 Pin versions in pip.
Dockerfile.insecure:10 DL3020 Use COPY instead of ADD for files.
Dockerfile.insecure:11 DL3027 Do not use apt-get update alone in RUN instruction.
Dockerfile.insecure:13 DL3059 Multiple consecutive RUN instructions. Consider consolidation.
Dockerfile.insecure:14 DL3059 Multiple consecutive RUN instructions. Consider consolidation.
Dockerfile.insecure:15 DL3025 Use arguments JSON notation for CMD and ENTRYPOINT.
```

**Explicacion de cada advertencia:**

| Codigo | Advertencia | Significado |
|--------|-------------|-------------|
| DL3007 | `latest` tag | Usar tag especifico en vez de `latest` |
| DL4000 | MAINTAINER deprecated | Usar `LABEL maintainer=...` |
| DL3009 | No limpiar apt lists | Agregar `rm -rf /var/lib/apt/lists/*` |
| DL3015 | `--no-install-recommends` | Evita paquetes recomendados innecesarios |
| DL3013 | Pin versions in pip | Fijar versiones de paquetes pip |
| DL3020 | COPY vs ADD | Usar COPY para archivos locales |
| DL3027 | apt-get update alone | Combinar `apt-get update` con `install` |
| DL3059 | Multiple RUN | Combinar RUN commands en uno solo |
| DL3025 | JSON notation | Usar `["python", "app.py"]` en vez de `python app.py` |

**Paso 4: Dockerfile corregido**

```dockerfile
FROM python:3.11-slim-bookworm

LABEL maintainer="dev@example.com" \
      version="1.0" \
      description="Aplicacion Flask segura"

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-pip \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir flask==3.0.0

RUN groupadd -r appgroup && useradd -r -g appgroup appuser

WORKDIR /app

COPY app.py .

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:8000/health || exit 1

CMD ["python", "app.py"]
```

**Paso 5: Verificar que ya no hay advertencias**

```bash
hadolint Dockerfile.secure
```

Salida esperada: sin errores ni advertencias.

**Resumen de correcciones aplicadas:**

| Codigo Hadolint | Correccion aplicada |
|-----------------|---------------------|
| DL3007 | `python:3.11-slim-bookworm` en vez de `ubuntu` |
| DL4000 | `LABEL maintainer=` en vez de `MAINTAINER` |
| DL3009 | `rm -rf /var/lib/apt/lists/*` |
| DL3015 | `--no-install-recommends` |
| DL3013 | `flask==3.0.0` (version fija) |
| DL3020 | `COPY` en vez de `ADD` para archivos locales |
| DL3027 | `apt-get update && apt-get install` combinados |
| DL3059 | RUN combinados en una sola instruccion |
| DL3025 | `CMD ["python", "app.py"]` en notacion JSON |

---

### 18. Preguntas y Respuestas

#### Pregunta 1

**Cual es la principal diferencia de seguridad entre un contenedor y una maquina virtual?**

**Respuesta:** La principal diferencia radica en el nivel de aislamiento. Una maquina virtual tiene su propio kernel, por lo que un ataque que comprometa el kernel de la VM no afecta al host directamente (hay una barrera completa gracias al hipervisor). Un contenedor, en cambio, comparte el kernel del host. Si un atacante logra escapar del contenedor (container escape) o explota una vulnerabilidad del kernel, puede comprometer el host completo. Ademas, las VMs tienen un hipervisor que anade una capa adicional de aislamiento, mientras que los contenedores usan namespaces y cgroups, que son mecanismos del kernel de Linux disenados para aislamiento de procesos, no como barreras de seguridad completas. Por eso, en entornos de alta seguridad, se recomienda ejecutar contenedores dentro de VMs (como hace Kubernetes con kubelet en nodos virtualizados).

#### Pregunta 2

**Que es un container escape y como se produce?**

**Respuesta:** Un container escape es un ataque en el que un proceso que se ejecuta dentro de un contenedor logra romper el aislamiento del contenedor y ejecutar codigo en el sistema host. Las formas mas comunes de lograrlo son: (1) Montar `/var/run/docker.sock` dentro del contenedor, lo que permite controlar el daemon Docker del host (y ejecutar contenedores privilegiados en el host). (2) Ejecutar el contenedor con `--privileged`, que da todas las capacidades de Linux y acceso a dispositivos del host. (3) Montar directorios sensibles del host como `/proc` o `/sys`, que pueden filtrar informacion o permitir modificar parametros del kernel. (4) Vulnerabilidades conocidas del kernel como CVE-2022-0847 (Dirty Pipe) o CVE-2024-1086 que permiten escalar privilegios. La prevencion incluye: no montar el socket de Docker, no usar `--privileged`, usar `userns-remap`, mantener el kernel actualizado, y ejecutar con `no-new-privileges`.

#### Pregunta 3

**Por que no se debe ejecutar como root dentro de un contenedor?**

**Respuesta:** Ejecutar como root dentro de un contenedor es peligroso por varias razones: (1) Aunque el root del contenedor (UID 0) no es el mismo que el root del host gracias a los namespaces de usuario, si ocurre un container escape, el atacante ya tiene UID 0 en el contenedor y puede escalar a root del host mas facilmente. (2) Sin `userns-remap`, el UID 0 del contenedor se mapea al UID 0 del host, dando acceso root directo si se rompe el aislamiento. (3) Los procesos root dentro del contenedor pueden modificar archivos del sistema, instalar paquetes, cambiar configuraciones, y realizar actividades maliciosas sin restricciones. (4) Docker Bench Security y CIS Benchmark recomiendan explicitamente crear un usuario no-root. La solucion es usar `USER appuser` en el Dockerfile, crear el usuario con `adduser` (Alpine) o `useradd` (Debian), y asignarle solo los permisos necesarios para ejecutar la aplicacion.

#### Pregunta 4

**Para que sirve `--cap-drop=ALL` al ejecutar un contenedor?**

**Respuesta:** `--cap-drop=ALL` elimina todas las capacidades de Linux del contenedor. Las capacidades son privilegios granulares del kernel (hay ~40 capacidades como CAP_NET_BIND_SERVICE, CAP_SYS_ADMIN, CAP_DAC_OVERRIDE). Por defecto, Docker otorga un subconjunto de capacidades a cada contenedor, lo que puede ser mas de lo necesario. Al eliminar todas con `--cap-drop=ALL` y luego agregar solo las estrictamente necesarias con `--cap-add=NET_BIND_SERVICE` (por ejemplo), se aplica el principio de minimo privilegio. Esto significa que si un atacante compromete la aplicacion dentro del contenedor, tendra capacidades muy limitadas: no podra cambiar permisos de archivos (CAP_DAC_OVERRIDE), no podra montar sistemas de archivos (CAP_SYS_ADMIN), no podra enviar senales a otros procesos (CAP_KILL), etc. Es una de las medidas de hardening mas efectivas y faciles de implementar.

#### Pregunta 5

**Que es Docker Bench Security y que tipo de pruebas realiza?**

**Respuesta:** Docker Bench Security es un script de codigo abierto que automatiza la auditoria de seguridad de un entorno Docker contra el CIS (Center for Internet Security) Benchmark para Docker. Fue creado por Docker Inc. y la comunidad. Realiza aproximadamente 100 pruebas organizadas en categorias: (1) Configuracion del host (particiones separadas, hardening del sistema, version de Docker). (2) Configuracion del daemon Docker (`icc`, `userns-remap`, `seccomp`, live-restore). (3) Archivos de configuracion (permisos de daemon.json, certificados TLS). (4) Imagenes y Dockerfiles (usuario no-root, imagenes confiables, healthchecks). (5) Contenedores en ejecucion (privilegios, capacidades, read-only, redes, recursos). (6) Redes (segmentacion, puertos expuestos). (7) Operaciones de Docker (swarm mode, logging). Cada prueba devuelve PASS, WARNING o INFO. Al final, el objetivo es maximizar los PASS y corregir los WARNING.

#### Pregunta 6

**Como evitar que los secretos queden almacenados en la imagen de Docker?**

**Respuesta:** Hay varias tecnicas para evitar que los secretos queden en la imagen: (1) NO usar `ENV` con valores hardcodeados en el Dockerfile, ya que esos valores persisten en todas las capas de la imagen. (2) Usar `ARG` para pasar valores en tiempo de build (no persisten en la imagen final, pero si en las capas intermedias a menos que se use multi-stage build). (3) Usar `docker build --secret` con BuildKit: `RUN --mount=type=secret,id=my_secret` que monta el secreto solo durante la ejecucion de ese RUN y no queda en ninguna capa. (4) En tiempo de ejecucion, pasar secretos con `-e` o `--env-file` en `docker run`. (5) En docker-compose, usar `secrets:` con archivos externos, que se montan en `/run/secrets/` dentro del contenedor. (6) Usar un vault externo (HashiCorp Vault, AWS Secrets Manager) y autenticarse desde la aplicacion. La regla de oro es: ningun secreto debe estar escrito en el Dockerfile o en el codigo fuente.

#### Pregunta 7

**Que es un multi-stage build y como mejora la seguridad?**

**Respuesta:** El multi-stage build es una caracteristica de Docker que permite usar multiples instrucciones `FROM` en un mismo Dockerfile, donde cada `FROM` inicia una nueva etapa (stage). Solo los archivos copiados explicitamente con `COPY --from=` pasan a la etapa final. Esto mejora la seguridad porque: (1) La imagen final solo contiene lo necesario para ejecutar la aplicacion, sin herramientas de compilacion como compiladores, debuggers, o paquetes de desarrollo que aumentan la superficie de ataque. (2) Los secretos o claves usados en la etapa de compilacion no estan presentes en la etapa final. (3) La imagen final es mucho mas pequena (ej: 800MB -> 120MB), lo que reduce la superficie de ataque y acelera los despliegues. (4) Es mas facil auditar la imagen final porque tiene menos componentes. Ejemplo: en el stage 1 se compila un binario de Go con todas las herramientas de desarrollo; en el stage 2 solo se copia el binario compilado a una imagen `scratch` o `alpine` sin compilador, shell, ni gestor de paquetes.

#### Pregunta 8

**Que es el principio de minimo privilegio aplicado a contenedores y como se implementa?**

**Respuesta:** El principio de minimo privilegio establece que un contenedor debe tener solo los permisos estrictamente necesarios para funcionar, nada mas. En Docker se implementa combinando varias tecnicas: (1) Usuario no-root (`USER appuser` en el Dockerfile). (2) Eliminar capacidades innecesarias (`--cap-drop=ALL --cap-add=NET_BIND_SERVICE`). (3) Sistema de archivos de solo lectura (`--read-only`) con directorios temporales en tmpfs (`--tmpfs /tmp:rw,noexec,nosuid`). (4) Restriccion de nuevos privilegios (`--security-opt=no-new-privileges:true`). (5) Limitar recursos (CPU, memoria, reinicios). (6) Redes aisladas y con alcance minimo (solo las redes necesarias para la comunicacion del servicio). (7) No exponer puertos innecesarios. (8) Volumenes montados con permisos minimos (read-only cuando sea posible). (9) Usar `userns-remap` para mapear el root del contenedor a un UID no privilegiado del host. El objetivo es que incluso si un atacante compromete la aplicacion, el dano que pueda causar sea minimo.

---

## Tarea / Lectura Recomendada

1. **Practicar:** Escribir un Dockerfile seguro para una aplicacion existente (Node.js, Python, Go). Aplicar todas las buenas practicas: multi-stage, no-root, minimizar capas, healthcheck, etc. Comparar el tamano de la imagen antes y despues.

2. **Practicar:** Ejecutar Docker Bench Security en tu entorno Docker local. Identificar al menos 5 WARNINGs y corregirlos. Documentar el proceso con capturas de la salida antes y despues.

3. **Practicar:** Escanear todas las imagenes en tu sistema local con Trivy: `trivy image --severity=CRITICAL,HIGH $(docker images --format "{{.Repository}}:{{.Tag}}" | grep -v "<none>")`. Para cada imagen con vulnerabilidades criticas, determinar que imagen base actualizada soluciona el problema.

4. **Practicar:** Crear un docker-compose.yml para una aplicacion de 3 capas (frontend, API, base de datos) con todas las medidas de seguridad: redes separadas, usuarios no-root, limites de recursos, healthchecks, y secrets.

5. **Practicar:** Usar Hadolint para analizar 3 Dockerfiles diferentes (uno propio, uno de un proyecto open source, y uno de ejemplo). Corregir todas las advertencias y documentar los cambios.

6. **Leer:** CIS Docker Benchmark oficial - https://www.cisecurity.org/benchmark/docker/ (documento completo de referencia).

7. **Leer:** Documentacion oficial de seguridad de Docker - https://docs.docker.com/engine/security/ (todas las paginas: seccomp, AppArmor, userns-remap, etc.).

8. **Leer:** OWASP Docker Security Cheat Sheet - https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html

9. **Explorar:** Falco (runtime security) - https://falco.org/docs/ (instalar y probar reglas de deteccion de container escape).

10. **Explorar:** Trivy - escaneo de IaC y Kubernetes - `trivy k8s --severity=CRITICAL,HIGH cluster` (si tienes acceso a un cluster).
