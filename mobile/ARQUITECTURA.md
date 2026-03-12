# 🏗️ Arquitectura - Stock Management System

## 1. Visión General

```mermaid
graph TB
    subgraph "Cliente"
        RN["React Native<br/>(iOS/Android)"]
        KT["Kotlin<br/>(Android Nativo)"]
    end
    
    subgraph "API Gateway"
        NG["Nginx<br/>Reverse Proxy"]
    end
    
    subgraph "Backend"
        EXP["Express.js<br/>Node.js"]
        AUTH["Auth Service<br/>OAuth/JWT"]
        STOCK["Stock Service"]
        REPORT["Report Service"]
    end
    
    subgraph "Datos"
        PG["PostgreSQL"]
        REDIS["Redis<br/>Cache"]
    end
    
    subgraph "Integraciones"
        OAUTH["OAuth<br/>Google/LinkedIn/FB"]
        WA["WhatsApp<br/>Twilio"]
        ML["Mercado Libre<br/>API"]
        OCR["Tesseract.js<br/>OCR"]
    end
    
    RN --> NG
    KT --> NG
    NG --> EXP
    EXP --> AUTH
    EXP --> STOCK
    EXP --> REPORT
    AUTH --> OAUTH
    STOCK --> PG
    STOCK --> REDIS
    REPORT --> PG
    STOCK --> WA
    STOCK --> ML
    STOCK --> OCR
```

---

## 2. Decisiones Arquitectónicas (ADR)

### ADR-001: Arquitectura de Microservicios Monolítica

**Decisión:** Usar monolito modular en lugar de microservicios completos

**Razón:**
- Proyecto educativo (complejidad manejable)
- Facilita debugging y deployment
- Permite evolucionar a microservicios después

**Estructura:**
```
backend/
├── src/
│   ├── auth/          # Autenticación
│   ├── users/         # Gestión de usuarios
│   ├── tenants/       # Multi-tenancy
│   ├── stock/         # Gestión de stock
│   ├── providers/     # Proveedores
│   ├── reports/       # Reportes
│   ├── integrations/  # APIs externas
│   └── shared/        # Código compartido
```

---

### ADR-002: MVVM en Mobile + Clean Architecture en Backend

**Decisión:** Separar lógica de presentación, negocio y datos

**Beneficios:**
- Testeable
- Mantenible
- Escalable

**Capas:**

```mermaid
graph LR
    UI["UI Layer<br/>Composables/Activities"]
    VM["ViewModel<br/>State Management"]
    UC["Use Cases<br/>Lógica de Negocio"]
    REPO["Repository<br/>Abstracción de Datos"]
    DS["Data Sources<br/>Local/Remote"]
    
    UI --> VM
    VM --> UC
    UC --> REPO
    REPO --> DS
```

---

### ADR-003: PostgreSQL + Prisma ORM

**Decisión:** PostgreSQL como BD principal + Prisma para ORM

**Razón:**
- PostgreSQL: robusto, open-source, características avanzadas
- Prisma: type-safe, migraciones automáticas, excelente DX

**Schema Principal:**

```mermaid
erDiagram
    USERS ||--o{ TENANTS : owns
    USERS ||--o{ EMPRENDIMIENTOS : manages
    TENANTS ||--o{ EMPRENDIMIENTOS : contains
    EMPRENDIMIENTOS ||--o{ CATEGORIAS : has
    CATEGORIAS ||--o{ ITEMS : contains
    ITEMS ||--o{ MOVIMIENTOS : tracks
    EMPRENDIMIENTOS ||--o{ PROVEEDORES : works_with
    USERS ||--o{ AUDITORIAS : generates
```

---

### ADR-004: JWT + OAuth 2.0 con PKCE

**Decisión:** Autenticación stateless con JWT + OAuth social

**Flujo:**

```mermaid
sequenceDiagram
    participant App
    participant Backend
    participant OAuth as OAuth Provider
    
    App->>OAuth: Inicia login (PKCE)
    OAuth->>App: Retorna authorization code
    App->>Backend: Envía code
    Backend->>OAuth: Intercambia code por token
    OAuth->>Backend: Retorna access token
    Backend->>Backend: Crea JWT
    Backend->>App: Retorna JWT + Refresh Token
    App->>Backend: Usa JWT en requests
```

---

### ADR-005: Redis para Caché y Sesiones

**Decisión:** Redis para caché de datos frecuentes y sesiones

**Uso:**
- Caché de usuarios (TTL: 1 hora)
- Caché de stock (TTL: 5 min)
- Sesiones de admin (TTL: 24 horas)
- Rate limiting

---

### ADR-006: Docker Compose para Desarrollo

**Decisión:** Infraestructura local con Docker Compose

**Servicios:**
```yaml
services:
  postgres:
    image: postgres:15
    ports: 5432
  
  redis:
    image: redis:7
    ports: 6379
  
  backend:
    build: ./backend
    ports: 3000
    depends_on: [postgres, redis]
  
  nginx:
    image: nginx:latest
    ports: 80, 443
```

---

## 3. Flujos Principales

### Flujo: Autenticación

```mermaid
graph TD
    A["Usuario abre app"] --> B["Selecciona OAuth provider"]
    B --> C["Redirige a provider"]
    C --> D["Usuario autoriza"]
    D --> E["Provider retorna code"]
    E --> F["Backend intercambia code"]
    F --> G{Usuario existe?}
    G -->|No| H["Crea usuario + tenant"]
    G -->|Sí| I["Actualiza último login"]
    H --> J["Genera JWT + Refresh"]
    I --> J
    J --> K["Retorna tokens a app"]
    K --> L["App almacena tokens"]
    L --> M["Usuario en dashboard"]
```

### Flujo: Registrar Stock desde Boleta

```mermaid
graph TD
    A["Usuario toma foto"] --> B["Envía a backend"]
    B --> C["OCR procesa imagen"]
    C --> D["Extrae datos"]
    D --> E["Busca items similares"]
    E --> F["Retorna sugerencias"]
    F --> G["Usuario confirma"]
    G --> H["Crea movimiento entrada"]
    H --> I["Actualiza stock"]
    I --> J["Registra auditoría"]
    J --> K["Notifica cambios"]
```

### Flujo: Admin Revisa Usuario

```mermaid
graph TD
    A["Admin accede panel"] --> B["Autentica con JWT"]
    B --> C{Tiene rol ADMIN?}
    C -->|No| D["Acceso denegado"]
    C -->|Sí| E["Carga lista usuarios"]
    E --> F["Admin selecciona usuario"]
    F --> G["Carga datos completos"]
    G --> H["Registra auditoría"]
    H --> I["Muestra información"]
```

---

## 4. Seguridad

### Capas de Seguridad

```mermaid
graph TB
    subgraph "Nivel 1: Transporte"
        TLS["HTTPS/TLS 1.3"]
    end
    
    subgraph "Nivel 2: Autenticación"
        JWT["JWT Firmado"]
        OAUTH["OAuth 2.0"]
    end
    
    subgraph "Nivel 3: Autorización"
        RBAC["RBAC - Roles"]
        TENANT["Aislamiento Tenant"]
    end
    
    subgraph "Nivel 4: Datos"
        HASH["Bcrypt Passwords"]
        ENC["Encriptación Sensibles"]
    end
    
    subgraph "Nivel 5: Auditoría"
        LOG["Logs de Acceso"]
        AUDIT["Auditoría de Cambios"]
    end
    
    TLS --> JWT
    JWT --> RBAC
    RBAC --> HASH
    HASH --> LOG
```

### Checklist de Seguridad

- ✅ HTTPS en todas las comunicaciones
- ✅ Contraseñas hasheadas (bcrypt)
- ✅ JWT con expiración
- ✅ Refresh tokens seguros
- ✅ CORS configurado
- ✅ Rate limiting
- ✅ Validación de entrada
- ✅ SQL injection prevention (Prisma)
- ✅ XSS prevention
- ✅ CSRF tokens
- ✅ Auditoría de acciones admin
- ✅ Encriptación de datos sensibles

---

## 5. Escalabilidad

### Horizontal Scaling

```mermaid
graph TB
    LB["Load Balancer<br/>Nginx"]
    
    subgraph "Backend Instances"
        B1["Backend 1"]
        B2["Backend 2"]
        B3["Backend 3"]
    end
    
    subgraph "Datos Compartidos"
        PG["PostgreSQL<br/>Primary"]
        REDIS["Redis<br/>Cluster"]
    end
    
    LB --> B1
    LB --> B2
    LB --> B3
    B1 --> PG
    B2 --> PG
    B3 --> PG
    B1 --> REDIS
    B2 --> REDIS
    B3 --> REDIS
```

### Optimizaciones

- Índices en PostgreSQL
- Caché en Redis
- Paginación en listados
- Lazy loading en mobile
- Compresión de imágenes

---

## 6. Deployment

### Desarrollo (Docker Compose)

```bash
docker-compose up -d
# Acceso: http://localhost:3000
```

### Producción (Kubernetes - Opcional)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: stock-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: stock-backend
  template:
    metadata:
      labels:
        app: stock-backend
    spec:
      containers:
      - name: backend
        image: stock-backend:latest
        ports:
        - containerPort: 3000
```

---

## 7. Tecnologías Seleccionadas

| Componente | Tecnología | Razón |
|-----------|-----------|-------|
| Backend | Node.js + Express | Rápido, JavaScript, ecosistema |
| BD | PostgreSQL | Robusto, open-source, ACID |
| ORM | Prisma | Type-safe, migraciones automáticas |
| Caché | Redis | Rápido, in-memory, versátil |
| Mobile | React Native | Multiplataforma, código compartido |
| Android Nativo | Kotlin | Moderno, seguro, interop con Java |
| Autenticación | OAuth 2.0 + JWT | Estándar, seguro, escalable |
| Contenedores | Docker | Reproducibilidad, portabilidad |
| Orquestación | Kubernetes | Escalabilidad, alta disponibilidad |

---

## 8. Próximos Pasos

1. **Clase 1-2:** Setup inicial
2. **Clase 3-4:** Modelos de datos
3. **Clase 5-6:** Autenticación
4. **Clase 7-8:** Multi-tenancy
5. **Clase 9-16:** Features y integraciones

