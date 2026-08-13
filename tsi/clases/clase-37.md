# Clase 37: Seguridad en Contenedores e Infraestructura como Codigo

**Numero de clase:** 26  
**Duracion:** 2 horas  
**Curso:** Taller de Ciberseguridad Orientada al Desarrollo

---

## Objetivos de Aprendizaje

- Aplicar buenas practicas de seguridad en Dockerfiles
- Escanear imagenes de contenedores en busca de vulnerabilidades
- Escribir configuraciones seguras de infraestructura como codigo (IaC)
- Implementar seguridad en Kubernetes: Pod Security Standards, RBAC, Network Policies
- Usar Checkov para escaneo automatizado de IaC

---

## Contenido Detallado

### 1. Seguridad en Docker (20 min)

**Imagenes base minimas:**
- Usar imagenes oficiales y ligeras como `python:3.11-slim`, `alpine`, `distroless`
- Evitar imagenes como `ubuntu:latest` o `node:latest` que incluyen paquetes innecesarios
- Preferir imagenes con soporte LTS y parches de seguridad

**Principio de no-root:**
- Nunca ejecutar procesos como root dentro del contenedor
- Crear un usuario dedicado con `USER` en el Dockerfile
- Asignar solo los permisos minimos necesarios

**Multi-stage builds:**
- Separar la etapa de compilacion de la etapa de produccion
- Solo copiar artefactos necesarios a la imagen final
- Reducir drasticamente el tamano y superficie de ataque

**Buenas practicas adicionales:**
- Usar `COPY` en vez de `ADD` (ADD descarga URLs y extrae archivos automaticamente)
- Implementar `HEALTHCHECK` para monitorizar el estado del contenedor
- No exponer puertos innecesarios
- Usar `.dockerignore` para excluir archivos sensibles
- Fijar versiones especificas de paquetes

### 2. Dockerfile Seguro - Ejemplo Completo

```dockerfile
# Etapa de construccion (multi-stage)
FROM python:3.11-slim AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Etapa de produccion
FROM python:3.11-slim AS production

# Crear usuario no-root
RUN addgroup --system --gid 1001 appgroup && \
    adduser --system --uid 1001 --gid 1001 appuser

# Instalar solo lo necesario para produccion
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar solo artefactos necesarios desde builder
COPY --from=builder /root/.local /home/appuser/.local
COPY app.py .
COPY templates/ ./templates/

# Configurar PATH
ENV PATH=/home/appuser/.local/bin:$PATH

# Usar usuario no-root
USER appuser

# Healthcheck
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Exponer solo puerto necesario
EXPOSE 5000

CMD ["python", "app.py"]
```

### 3. Escaneo de Imagenes (15 min)

**Trivy (Aqua Security):**
```bash
# Escaneo basico
trivy image python:3.11-slim

# Escaneo con severidad especifica
trivy image --severity CRITICAL,HIGH mi-app:latest

# Escaneo con salida JSON
trivy image --format json --output trivy-report.json mi-app:latest
```

**Docker Scout:**
```bash
docker scout quickview mi-app:latest
docker scout cves mi-app:latest
docker scout recommendations mi-app:latest
```

**Clair:**
```bash
clairctl analyze --docker mi-app:latest
```

### 4. Infraestructura como Codigo (IaC) Segura (15 min)

**Terraform - Buenas practicas:**

```hcl
# Ejemplo seguro: S3 bucket con cifrado y bloqueo de acceso publico
resource "aws_s3_bucket" "secure_bucket" {
  bucket = "mi-bucket-seguro-${var.environment}"
  acl    = "private"

  versioning {
    enabled = true
  }

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }
}

resource "aws_s3_bucket_public_access_block" "block_public" {
  bucket = aws_s3_bucket.secure_bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
```

**CloudFormation - Buenas practicas:**

```yaml
Resources:
  SecureInstance:
    Type: AWS::EC2::Instance
    Properties:
      ImageId: ami-0abcdef1234567890
      InstanceType: t3.micro
      SecurityGroupIds:
        - !Ref SecureSecurityGroup
      BlockDeviceMappings:
        - DeviceName: /dev/xvda
          Ebs:
            Encrypted: true
            VolumeSize: 20
```

### 5. Kubernetes Security (20 min)

**Pod Security Standards (PSS):**

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: secure-ns
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted
```

Niveles:
- **privileged:** Sin restricciones
- **baseline:** Minimamente restrictivo
- **restricted:** Maxima seguridad

**Network Policies:**

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-all
  namespace: secure-ns
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
```

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-api-only
  namespace: secure-ns
spec:
  podSelector:
    matchLabels:
      app: api
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: ingress-nginx
    ports:
    - protocol: TCP
      port: 8080
```

**RBAC (Role-Based Access Control):**

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: secure-ns
  name: pod-reader
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "watch", "list"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: read-pods
  namespace: secure-ns
subjects:
- kind: User
  name: developer
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io
```

### 6. Checkov para Escaneo de IaC (15 min)

Checkov analiza Terraform, CloudFormation, Kubernetes, Dockerfile y otros formatos. Usa politicas predefinidas (CKV_*) y personalizadas.

```bash
# Escaneo basico
checkov -d .

# Escaneo con directorio especifico
checkov -d terraform/

# Escaneo de Kubernetes
checkov -f deployment.yaml --framework kubernetes

# Escaneo con salida JSON
checkov -d . --output json -o report.json

# Escaneo con skip de politicas
checkov -d . --skip-check CKV_AWS_52
```

Ejemplo de resultado:
```
Check: CKV_DOCKER_2: "Ensure that HEALTHCHECK is set for container"
        FAILED for resource: Dockerfile
        File: /Dockerfile
        Guide: https://docs.bridgecrew.io/docs/
```

---

## Ejercicio 1: Reescribir un Dockerfile Inseguro

**Enunciado:** Dado el siguiente Dockerfile inseguro, reescribelo siguiendo mejores practicas.

Dockerfile inseguro original:
```dockerfile
FROM ubuntu:latest
RUN apt-get update
RUN apt-get install -y python3 python3-pip curl vim netcat git
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 8000 3000 22
CMD ["python3", "app.py"]
```

**Solucion:**

```dockerfile
# Etapa de construccion
FROM python:3.11-slim AS builder

WORKDIR /build
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Etapa de produccion
FROM python:3.11-slim AS production

# Crear usuario no-root
RUN addgroup --system --gid 1001 appgroup && \
    adduser --system --uid 1001 --gid 1001 appuser

# Instalar solo curl para healthcheck (nada de vim, netcat, git)
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar solo lo necesario desde builder
COPY --from=builder /root/.local /home/appuser/.local
COPY app.py .
COPY templates/ ./templates/

ENV PATH=/home/appuser/.local/bin:$PATH

USER appuser

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000

CMD ["python3", "app.py"]
```

**Cambios realizados y justificacion:**
1. **Imagen base:** Cambie `ubuntu:latest` por `python:3.11-slim` -> imagen oficial, mas pequena y con Python incluido
2. **Multi-stage:** Agregue etapa builder para instalar dependencias por separado
3. **No-root:** Se crea usuario `appuser` y se usa `USER appuser`
4. **Paquetes minimos:** Elimine vim, netcat, git, y herramientas innecesarias
5. **ADD eliminado:** Se usa COPY en vez de ADD
6. **COPY especifico:** Se copia solo lo necesario (no todo el directorio)
7. **Puertos minimos:** Se expone solo el puerto 8000 (elimine 3000 y 22)
8. **HEALTHCHECK:** Agregado para monitorizacion
9. **Apt-get con --no-install-recommends:** Reduce paquetes instalados
10. **Limpieza de cache:** `rm -rf /var/lib/apt/lists/*`

---

## Ejercicio 2: Escribir un docker-compose.yml Seguro

**Enunciado:** Escribe un docker-compose.yml seguro con secrets management y healthchecks para una aplicacion web con base de datos PostgreSQL.

**Solucion:**

```yaml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - APP_ENV=production
      - DB_HOST=db
      - DB_PORT=5432
      - DB_NAME=${DB_NAME:-appdb}
    env_file:
      - .env
    secrets:
      - db_password
      - jwt_secret
    depends_on:
      db:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s
    networks:
      - internal
      - monitoring
    restart: unless-stopped
    # No ejecutar como root
    user: "1001:1001"
    read_only: true
    security_opt:
      - no-new-privileges:true
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE

  db:
    image: postgres:15-alpine
    volumes:
      - pgdata:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=${DB_NAME:-appdb}
    env_file:
      - .env.db
    secrets:
      - db_password
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U appuser -d appdb"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s
    networks:
      - internal
    restart: unless-stopped
    # PostgreSQL corre como usuario no-root por defecto en alpine
    security_opt:
      - no-new-privileges:true
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE

  # Proxy reverso con Traefik (opcional)
  reverse-proxy:
    image: traefik:v2.10
    ports:
      - "443:443"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
    networks:
      - monitoring
    restart: unless-stopped

secrets:
  db_password:
    file: ./secrets/db_password.txt
  jwt_secret:
    file: ./secrets/jwt_secret.txt

volumes:
  pgdata:

networks:
  internal:
    driver: bridge
    internal: true  # Sin acceso externo
  monitoring:
    driver: bridge
```

**Nota:** Archivos de secretos en `./secrets/` deben crearse con permisos 600:
```bash
echo "mi-contrasena-segura" > ./secrets/db_password.txt
chmod 600 ./secrets/db_password.txt
```

---

## Ejercicio 3: Escanear un Dockerfile con Trivy y Corregir Vulnerabilidades

**Enunciado:** Dado el siguiente Dockerfile, ejecuta Trivy (simulado) para identificar vulnerabilidades y propone correcciones.

Dockerfile con vulnerabilidades:
```dockerfile
FROM node:14
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 3000
USER root
CMD ["node", "app.js"]
```

**Solucion - Analisis y correcciones:**

**Paso 1: Resultado del escaneo con Trivy**

Trivy detectaria:
- Node 14 contiene CVE conocidas (fecha de soporte finalizada)
- `npm install` no usa `--only=production`, incluye devDependencies
- `USER root` ejecuta el contenedor con privilegios maximos
- No hay HEALTHCHECK
- No se usan multi-stage builds
- npm audit no se ejecuto antes del build

**Paso 2: Dockerfile corregido**

```dockerfile
# Etapa de construccion
FROM node:20-alpine AS builder

WORKDIR /build
COPY package*.json ./
RUN npm ci --only=production

# Etapa de produccion
FROM node:20-alpine AS production

# Crear usuario no-root
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

WORKDIR /app

# Copiar solo node_modules de produccion
COPY --from=builder /build/node_modules ./node_modules
COPY app.js .
COPY public/ ./public/

USER appuser

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:3000/health || exit 1

EXPOSE 3000

CMD ["node", "app.js"]
```

**Cambios:**
1. Node 14 -> Node 20-alpine (imagen mantenida, mas pequena)
2. Multi-stage build (separar dependencias)
3. `npm ci --only=production` (instalacion reproducible, solo produccion)
4. Usuario no-root (appuser)
5. HEALTHCHECK agregado
6. COPY especificos en vez de COPY . .
7. `.dockerignore` recomendado:

```
node_modules
npm-debug.log
.git
.gitignore
.env
*.md
tests/
```

---

## Preguntas y Respuestas

**1. Por que es mejor usar imagenes slim o alpine en vez de full?**

Las imagenes slim/alpine tienen menor superficie de ataque porque incluyen menos paquetes y herramientas. Menos paquetes significa menos vulnerabilidades potenciales. Ademas, son mas rapidas de descargar y ocupan menos espacio en disco.

**2. Que problema de seguridad tiene usar `USER root` en un contenedor?**

Ejecutar como root dentro del contenedor significa que si un atacante compromete la aplicacion, obtiene control total del contenedor. Ademas, si hay un escape de contenedor, el atacante podria obtener privilegios de root en el host. Siempre se debe usar un usuario no-root con `USER`.

**3. Que es Checkov y que tipo de recursos analiza?**

Checkov es una herramienta de analisis estatico para IaC (Infrastructure as Code). Analiza Terraform, CloudFormation, Kubernetes, Dockerfile, ARM, Bicep, Serverless, entre otros. Aplica politicas predefinidas de seguridad y compliance (CIS, GDPR, PCI-DSS).

**4. Cual es la diferencia entre Pod Security Standards (PSS) y Pod Security Policies (PSP)?**

PSP fue deprecated en Kubernetes 1.21 y eliminado en 1.25. PSS es el reemplazo oficial. PSS define tres niveles (privileged, baseline, restricted) que se aplican mediante Admission Controllers nativos o herramientas como Kyverno o OPA Gatekeeper.

**5. Que son las Network Policies en Kubernetes y para que sirven?**

Network Policies son reglas que controlan el trafico de red entre pods. Por defecto, todos los pods pueden comunicarse entre si. Las Network Policies permiten implementar el principio de minimo privilegio: solo permitir trafico explicito y denegar todo lo demas.

**6. Que practica insegura representa usar `ADD` en vez de `COPY` en un Dockerfile?**

`ADD` tiene comportamientos adicionales como descargar URLs y extraer archivos comprimidos automaticamente. Si se usa `ADD` con una URL, el contenedor podria descargar codigo malicioso sin verificacion. `COPY` solo copia archivos locales y es mas predecible y seguro.

**7. Como se manejan secretos en docker-compose de forma segura?**

Usando el bloque `secrets:` en docker-compose que monta archivos en `/run/secrets/`. Los secretos se definen con `file: ./secrets/mi_secreto.txt` y se referencian en servicios con `secrets: [mi_secreto]`. Esto evita poner contraseñas en variables de entorno del archivo compose.

---

## Tarea / Lectura Recomendada

- Leer: Docker security best practices (https://docs.docker.com/develop/security-best-practices/)
- Leer: CIS Benchmark for Docker (https://www.cisecurity.org/benchmark/docker)
- Practicar: Escanear tu propia imagen de Docker con Trivy y corregir vulnerabilidades
- Leer: Kubernetes Pod Security Standards (https://kubernetes.io/docs/concepts/security/pod-security-standards/)
- Practicar: Ejecutar Checkov en una configuracion de Terraform propia



