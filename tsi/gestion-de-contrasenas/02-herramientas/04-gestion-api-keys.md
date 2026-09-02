# 2.4 Gestión de API Keys, Tokens y Credenciales de Sistema

## Tipos de Credenciales de Sistema

### Clasificación

```
┌─────────────────────────────────────────────────────────────┐
│              CREDENCIALES DE SISTEMA                         │
├──────────────────┬──────────────────┬───────────────────────┤
│   API KEYS       │   TOKENS         │   CERTIFICADOS        │
├──────────────────┼──────────────────┼───────────────────────┤
│ - API Key simple │ - JWT (JSON      │ - TLS/SSL             │
│ - Secret Key     │   Web Token)     │ - Client certificates │
│ - Access Key     │ - OAuth tokens   │ - Code signing        │
│ - Service tokens  │ - Session tokens │ - CA certificates     │
│ - Webhook secrets│ - Refresh tokens │                       │
└──────────────────┴──────────────────┴───────────────────────┘
```

## 1. API Keys

### Estructura Típica

```
┌─────────────────────────────────────────────────────┐
│  API KEY EJEMPLO                                    │
├─────────────────────────────────────────────────────┤
│                                                     │
│  sk_live_a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6         │
│  ││   │  │                                      │
│  ││   │  └─ Identificador único (aleatorio)     │
│  ││   └─ Entorno (live = producción)            │
│  │└─ Tipo (sk = secret key)                     │
│  └─ Prefijo (sk = service key)                  │
│                                                     │
│  Prefijos comunes:                                   │
│  - sk_ = Secret Key (privada)                      │
│  - pk_ = Public Key (pública)                      │
│  - ak_ = Access Key                                │
│  - rk_ = Restricted Key                            │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### Almacenamiento Seguro

| Método | Seguridad | Uso Recomendado |
|--------|-----------|-----------------|
| Variable de entorno | ✅✅ | Servidores, CI/CD |
| Gestor de secretos (Vault) | ✅✅✅ | Empresas, producción |
| Archivo .env (local) | ⚠️ | Solo desarrollo local |
| Coded en código fuente | ❌❌❌ | NUNCA |
| Archivo de configuración | ⚠️ | Solo si está cifrado |
| Gestor de contraseñas | ✅✅ | Equipos pequeños |

### Ejemplo: Almacenar API Keys en Vaultwarden

```
Entrada en Vaultwarden:
┌─────────────────────────────────────────────────────┐
│  Nombre: API Key - Stripe (Producción)             │
│  Usuario: sk_live_a1b2c3d4e5f6g7h8i9j0            │
│  Contraseña: [None]                                │
│  Notas:                                            │
│    - Servicio: Stripe                              │
│    - Entorno: Producción                           │
│    - Permisos: Pagos, Suscripciones                │
│    - Rotación: Cada 90 días                        │
│    - Última rotación: 2024-01-15                   │
│    - Responsable: Juan Pérez (TI)                 │
│  URL: https://dashboard.stripe.com/apikeys        │
│  Custom Fields:                                    │
│    - Webhook Secret: whsec_x...                   │
│    - Publishable Key: pk_live_x...                │
└─────────────────────────────────────────────────────┘
```

## 2. JWT (JSON Web Tokens)

### Estructura JWT

```
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.
eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJleHAiOjE1MTYyNDUwMjIsInJvbGUiOiJhZG1pbiJ9.
SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c

Partes:
1. Header: {"alg":"RS256","typ":"JWT"}
2. Payload: {"sub":"1234567890","name":"John Doe","role":"admin"}
3. Signature: Firma RSA con clave privada del servidor
```

### Gestión de JWT

| Aspecto | Práctica Recomendada |
|---------|---------------------|
| **Almacenamiento** | HttpOnly cookie (no localStorage) |
| **Expiración** | Access token: 15 min, Refresh: 7 días |
| **Rotación** | Renovar refresh token en cada uso |
| **Revocación** | Blacklist en Redis si logout anticipado |
| **Almacenamiento para testing** | Vaultwarden (con notas de expiración) |

## 3. OAuth Tokens

### Flujo OAuth 2.0

```
┌──────────┐    ┌──────────┐    ┌──────────┐
│  Cliente │    │ Auth     │    │ Resource │
│  (App)   │    │ Server   │    │ Server   │
├──────────┤    ├──────────┤    ├──────────┤
│          │ 1. Redirect    │          │
│          │ a auth server  │          │
│          │───────────────►│          │
│          │                │          │
│          │ 2. User login + consent    │
│          │◄───────────────│          │
│          │                │          │
│          │ 3. Authorization Code     │
│          │◄───────────────│          │
│          │                │          │
│          │ 4. Exchange code for token │
│          │───────────────►│          │
│          │                │          │
│          │ 5. Access Token + Refresh │
│          │◄───────────────│          │
│          │                │          │
│          │ 6. API Request with Token │
│          │──────────────────────────►│
│          │                │          │
│          │ 7. Protected Resource     │
│          │◄──────────────────────────│
└──────────┘                └──────────┘
```

### Almacenamiento de OAuth Tokens

```
┌─────────────────────────────────────────────────────┐
│  ENTRADA VAULTWARDEN: OAuth Token - GitHub          │
├─────────────────────────────────────────────────────┤
│  Nombre: GitHub OAuth Token                        │
│  Usuario: ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx     │
│  Contraseña: [None]                                │
│  Notas:                                            │
│    - Servicio: GitHub                              │
│    - Tipo: Personal Access Token (fine-grained)   │
│    - Permisos: repos:read, workflow:read           │
│    - Expira: 2024-07-15 (90 días)                 │
│    - Responsable: DevOps Team                     │
│  URL: https://github.com/settings/tokens          │
└─────────────────────────────────────────────────────┘
```

## 4. Certificados SSL/TLS

### Tipos de Certificados

| Tipo | Uso | Almacenamiento |
|------|-----|----------------|
| **Server cert** | HTTPS del servidor | Vaultwarden (backup) |
| **Client cert** | Autenticación mutua | Vaultwarden + SO |
| **Code signing** | Firmar software | Hardware security module |
| **CA cert** | Autoridad de certificación | Vault físico + digital |

### Backup de Certificados

```
ESTRUCTURA DE BACKUP:
backups/certificados/
├── 2024-Q1/
│   ├── server.crt          ← Certificado del servidor
│   ├── server.key          ← Clave privada (CIFRADA)
│   ├── ca.crt              ← Certificado CA
│   ├── client-bhu.crt      ← Client cert BHU
│   └── metadata.json       ← Metadatos
├── 2024-Q2/
│   └── ...
└── emergency/
    └── recovery-instructions.md

CIFRADO DE BACKUP:
gpg --symmetric --cipher-algo AES256 \
    --output backups/certificados/2024-Q1.tar.gz.gpg \
    backups/certificados/2024-Q1.tar.gz
```

## 5. Credenciales de Servicios Comunes

### Tabla de Referencia

| Servicio | Tipo de Credencial | Rotación | Almacenamiento |
|----------|-------------------|----------|----------------|
| **AWS** | Access Key + Secret Key | 90 días | Vault + IAM |
| **GitHub** | Personal Access Token | 90 días | Vaultwarden |
| **Stripe** | Secret Key + Publishable | Anual | Vaultwarden |
| **SendGrid** | API Key | 90 días | Vaultwarden |
| **Cloudflare** | API Token | 180 días | Vaultwarden |
| **MySQL** | User + Password | 90 días | Vaultwarden |
| **PostgreSQL** | User + Password | 90 días | Vaultwarden |
| **Redis** | Password/Auth | 90 días | Vaultwarden |
| **SMTP** | User + Password | 90 días | Vaultwarden |
| **LDAP** | Bind DN + Password | 180 días | Vaultwarden |

## 6. HashiCorp Vault (Alternativa Empresarial)

### ¿Cuándo usar HashiCorp Vault?

```
USAR VAULTWARDEN:
├── Equipos < 100 personas
├── Necesitan guardar API keys manualmente
├── No requieren rotación automática
├── Presupuesto: $0
└── Caso de uso: Guardar credenciales estáticas

USAR HASHICORP VAULT:
├── Equipos > 100 personas
├── Necesitan rotación automática de secretos
├── Requieren Dynamic Secrets (DB credentials)
├── Necesitan PKI interno
├── Presupuesto: $0 (OSS) o $ enterprise
└── Caso de uso: Infraestructura de nivel enterprise
```

### Características de HashiCorp Vault

| Característica | Descripción |
|----------------|-------------|
| **Dynamic Secrets** | Genera credenciales efímeras (ej: usuario DB temporal) |
| **Secrets Engine** | Plugins para AWS, Azure, GCP, databases, etc. |
| **PKI** | Genera certificados TLS internos automáticamente |
| **Transit** | Cifrado como servicio (sin almacenar claves) |
| **Audit Logging** | Log completo de todas las operaciones |
| **Policies** | Control granular de acceso por path |

### Ejemplo: Dynamic Secrets en Vault

```
┌──────────┐    ┌──────────┐    ┌──────────┐
│  App     │    │  Vault   │    │ Database │
├──────────┤    ├──────────┤    ├──────────┤
│          │ 1. Solicita credencial     │
│          │───────────────►│          │
│          │                │ 2. Crea usuario temporal   │
│          │                │──────────►│
│          │                │          │
│          │ 3. Retorna:    │          │
│          │ user: temp_xyz │          │
│          │ pass: A1b2C3   │          │
│          │ TTL: 1 hora    │          │
│          │◄───────────────│          │
│          │                │          │
│  4. App usa credencial    │          │
│          │──────────────────────────►│
│          │                │          │
│  5. Después de 1 hora:   │          │
│  - Vault revoca usuario  │          │
│  - Credencial expira     │          │
│          │                │──────────►│
│          │                │ 6. Elimina usuario         │
└──────────┘                └──────────┘
```

## 7. Políticas de Gestión de API Keys

### Checklist de Seguridad

| # | Política | Prioridad |
|---|----------|-----------|
| 1 | Nunca commitear API keys en código fuente | Crítica |
| 2 | Usar variables de entorno o gestor de secretos | Crítica |
| 3 | Rotar keys cada 90 días | Alta |
| 4 | Usar permisos mínimos necesarios (least privilege) | Alta |
| 5 | Monitorear uso de API keys | Alta |
| 6 | Tener procedimiento de revocación | Alta |
| 7 | Diferenciar keys por entorno (dev/staging/prod) | Media |
| 8 | Usar rate limiting en APIs | Media |
| 9 | Logging de todas las llamadas API | Media |
| 10 | Documentar todas las keys activas | Media |

### Plantilla de Registro de API Keys

```markdown
| # | Servicio | Key Name | Entorno | Permisos | Expira | Responsable | Última Rotación |
|---|----------|----------|---------|----------|--------|-------------|-----------------|
| 1 | AWS | BHU-Prod-Admin | Prod | Admin | 2024-04-15 | Juan P. | 2024-01-15 |
| 2 | GitHub | BHU-CICD | Prod | repos:read | 2024-07-15 | DevOps | 2024-01-15 |
| 3 | Stripe | BHU-Pagos | Prod | payments | 2025-01-15 | Finanzas | 2024-01-15 |
| 4 | SendGrid | BHU-Email | Prod | mail.send | 2024-10-15 | TI | 2024-01-15 |
```

## 8. Git y Secretos

### .gitignore para Secretos

```gitignore
# Archivos de configuración con secretos
.env
.env.local
.env.production
*.pem
*.key
*.p12
*.pfx

# Vault files
*.kdbx
*.kdbx.lock

# Vaultwarden data
vw-data/
docker-compose.override.yml

# API Keys
*secret*
*token*
*credential*
```

### Pre-commit Hook (Detectar Secretos)

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Instalar: pip install git-secrets
# Configurar: git secrets --install
# Agregar patrones: git secrets --add 'AKIA[0-9A-Z]{16}'
# Agregar patrones: git secrets --add 'sk_live_[a-zA-Z0-9]+'

git secrets --scan --staged
if [ $? -ne 0 ]; then
    echo "ERROR: Secret detectado en el commit"
    echo "Revisa los archivos marcados arriba"
    exit 1
fi
```

## Resumen

| Tipo de Credencial | Almacenamiento Recomendado | Rotación |
|--------------------|-----------------------------|----------|
| API Keys simples | Vaultwarden | 90 días |
| JWT Secret | Variable de entorno + Vault | Al compilar |
| OAuth Tokens | Vaultwarden + refresh automático | Según expiración |
| Certificados TLS | Vaultwarden (backup) + SO | 1 año |
| DB Credentials | HashiCorp Vault (dynamic) | 1 hora (dynamic) |
| SSH Keys | Vaultwarden + hardware key | 1 año |
| Encryption Keys | Hardware Security Module | Nunca (si HSM) |

---

> **Actividad**: Audita todas las API keys y tokens de tu proyecto. Registra cada una en Vaultwarden con las siguientes notas: servicio, permisos, expiración, responsable, y procedimiento de revocación.
