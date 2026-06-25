# Clase: Gestión de Identidad y Acceso (IAM)

---

## 1. ¿Qué es IAM?

**IAM (Identity and Access Management)** es el conjunto de políticas, tecnologías y procesos que permiten gestionar **quién** puede acceder a **qué recursos**, **bajo qué condiciones** y **qué puede hacer** con ellos.

> La identidad ya no es solo una capa de acceso.
> **Es el perímetro de seguridad.**

### El problema que resuelve

En cualquier organización existen preguntas fundamentales:

- ¿Quién es esta persona/máquina?
- ¿Está autorizada a estar aquí?
- ¿Qué tiene permitido hacer?
- ¿Debería poder acceder a este recurso a las 3 AM desde otro país?

IAM responde todas estas preguntas de forma automatizada y segura.

---

## 2. Los 3 Pilares: AAA

Todo sistema IAM se construye sobre tres conceptos fundamentales:

```
┌────────────────────────────────────────────────────────┐
│                    MARCO AAA                           │
├────────────────────────────────────────────────────────┤
│                                                        │
│  ┌──────────────────┐  ┌──────────────────┐           │
│  │ AUTENTICACIÓN    │  │  AUTORIZACIÓN    │           │
│  │ (Authentication) │  │ (Authorization)  │           │
│  │                  │  │                  │           │
│  │ "¿Quién eres?"   │→ │ "¿Qué puedes     │           │
│  │                  │  │  hacer?"         │           │
│  └──────────────────┘  └──────────────────┘           │
│           │                          │                │
│           └──────────┬───────────────┘                │
│                      │                                │
│              ┌───────▼────────┐                       │
│              │   AUDITORÍA    │                       │
│              │ (Accounting)   │                       │
│              │                │                       │
│              │ "¿Qué hiciste?"│                       │
│              └────────────────┘                       │
│                                                        │
└────────────────────────────────────────────────────────┘
```

### Autenticación (Authentication)

**Verifica la identidad del sujeto.**

Factores de autenticación:

| Factor | Descripción | Ejemplo |
|--------|-------------|---------|
| Algo que sabes | Conocimiento | Contraseña, PIN |
| Algo que tienes | Posesión | Token físico, smartphone, YubiKey |
| Algo que eres | Biometría | Huella digital, Face ID, iris |
| Algo que haces | Comportamiento | Patrones de escritura, voz |
| Dónde estás | Localización | IP, geolocalización |

**MFA (Multi-Factor Authentication):** Combinar 2+ factores diferentes.

### Autorización (Authorization)

**Determina qué acciones puede realizar el sujeto autenticado.**

```
Usuario autenticado → Se evalúan permisos → Se concede o deniega acceso
```

### Auditoría (Accounting)

**Registra y rastrea todas las actividades.**

- ¿Quién accedió?
- ¿A qué recurso?
- ¿Cuándo?
- ¿Desde dónde?
- ¿Qué acción realizó?

---

## 3. Modelos de Control de Acceso

### RBAC - Role-Based Access Control

Los permisos se asignan a **roles**, y los usuarios se asignan a **roles**.

```
┌─────────────┐     ┌──────────────┐     ┌──────────────┐
│   Usuario   │────▶│     Rol      │────▶│   Permisos   │
│  "María"    │     │  "Contador"  │     │ leer:facturas│
└─────────────┘     └──────────────┘     │ escribir:fact│
                      │  "RRHH"     │     │ leer:nomina  │
                      └──────────────┘     └──────────────┘
```

```python
# Ejemplo RBAC en Python
from enum import Enum

class Rol(Enum):
    VISITANTE = "visitante"
    USUARIO = "usuario"
    EDITOR = "editor"
    ADMIN = "admin"

PERMISOS_POR_ROL = {
    Rol.VISITANTE: ["leer:publico"],
    Rol.USUARIO: ["leer:publico", "leer:perfil", "escribir:perfil"],
    Rol.EDITOR: ["leer:publico", "leer:perfil", "escribir:perfil",
                 "crear:contenido", "editar:contenido"],
    Rol.ADMIN: ["*"]  # Acceso total
}

def verificar_permiso(usuario_rol, permiso_requerido):
    """Verifica si un rol tiene un permiso específico."""
    permisos = PERMISOS_POR_ROL.get(usuario_rol, [])
    return "*" in permisos or permiso_requerido in permisos
```

**Ventajas:** Simple de administrar, escalable, fácil de auditar.
**Desventajas:** Puede volverse rígido, "role explosion" (demasiados roles).

---

### ABAC - Attribute-Based Access Control

La decisión se basa en **atributos** del usuario, recurso, acción y contexto.

```
POLÍTICA: Permitir acceso SI:
  - usuario.departamento == "finanzas"
  - recurso.tipo == "informe_financiero"
  - contexto.hora BETWEEN 08:00 AND 18:00
  - contexto.mfa == true
  - contexto.ip EN red_corporativa
```

```python
# Ejemplo ABAC en Python
from datetime import datetime

def evaluar_politica_abac(usuario, recurso, contexto):
    """Evalúa una política basada en atributos."""
    reglas = [
        usuario.get("departamento") == "finanzas",
        recurso.get("tipo") == "informe_financiero",
        8 <= contexto.get("hora", 0) <= 18,
        contexto.get("mfa") is True,
        contexto.get("ip", "").startswith("10.0.")
    ]
    return all(reglas)

# Uso
usuario = {"departamento": "finanzas", "rol": "analista"}
recurso = {"tipo": "informe_financiero", "clasificacion": "confidencial"}
contexto = {
    "hora": datetime.now().hour,
    "mfa": True,
    "ip": "10.0.1.50"
}

if evaluar_politica_abac(usuario, recurso, contexto):
    print("Acceso concedido")
else:
    print("Acceso denegado")
```

**Ventajas:** Extremadamente flexible, granular, se adapta a contexto.
**Desventajas:** Complejo de diseñar, difícil de auditar, rendimiento.

---

### Comparación de Modelos

| Modelo | Complejidad | Flexibilidad | Cuándo usarlo |
|--------|-------------|--------------|---------------|
| **DAC** (Discretionary) | Baja | Media | Sistemas pequeños, archivos personales |
| **MAC** (Mandatory) | Alta | Baja | Militar, gobierno, clasificación estricta |
| **RBAC** | Media | Media | Empresas, aplicaciones web, la mayoría de casos |
| **ABAC** | Alta | Alta | Entornos complejos, cloud, compliance estricto |
| **PBAC** (Policy-Based) | Alta | Alta | Regulaciones específicas, sectores financieros |

---

## 4. Protocolos y Estándares IAM

### OAuth 2.0 - Autorización Delegada

Permite que una aplicación acceda a recursos de otra **sin compartir credenciales**.

```
┌──────────┐     ┌──────────┐     ┌──────────────────┐
│Cliente   │     │Usuario   │     │Servidor de       │
│(App)     │     │          │     │Autorización      │
└────┬─────┘     └────┬─────┘     └────────┬─────────┘
     │                │                     │
     │  1. Solicita   │                     │
     │  acceso        │                     │
     │───────────────▶│                     │
     │                │  2. Autoriza        │
     │                │────────────────────▶│
     │                │                     │
     │                │  3. Redirige con    │
     │                │     auth code       │
     │                │◀────────────────────│
     │                │                     │
     │  4. Intercambia│                     │
     │  code por token│                     │
     │─────────────────────────────────────▶│
     │                │                     │
     │  5. Devuelve   │                     │
     │  access token  │                     │
     │◀─────────────────────────────────────│
     │                │                     │
     │  6. Usa token para acceder al recurso│
     │─────────────────────────────────────▶│
```

**Flows principales:**
- Authorization Code Flow (web apps, el más seguro)
- Client Credentials (service-to-service)
- Device Code (dispositivos sin browser)

---

### OpenID Connect (OIDC) - Autenticación sobre OAuth 2.0

Extiende OAuth 2.0 para **autenticación**, no solo autorización.

```
OAuth 2.0 → "Esta app puede leer tu email"
OIDC       → "Este usuario es juan@empresa.com"
```

**Componentes clave:**
- **ID Token:** JWT con información del usuario (nombre, email, sub)
- **UserInfo Endpoint:** API para obtener más datos del usuario
- **Scopes:** `openid`, `profile`, `email`

```python
# Ejemplo: Decodificar ID Token de OIDC
import jwt

def decodificar_id_token(token, public_key):
    """Decodifica y verifica un ID Token OIDC."""
    payload = jwt.decode(
        token,
        public_key,
        algorithms=["RS256"],
        audience="mi-cliente-id",
        issuer="https://accounts.google.com"
    )
    return {
        "sub": payload["sub"],
        "nombre": payload.get("name"),
        "email": payload.get("email"),
        "email_verificado": payload.get("email_verified")
    }
```

---

### SAML 2.0 - SSO Empresarial

Protocolo XML-based para Single Sign-On empresarial.

```
┌──────────┐    ┌────────────┐    ┌────────────┐
│Usuario   │    │SP          │    │IdP         │
│(Browser) │    │(Salesforce)│    │(Azure AD)  │
└────┬─────┘    └─────┬──────┘    └─────┬──────┘
     │                │                  │
     │  1. Accede a   │                  │
     │  Salesforce    │                  │
     │───────────────▶│                  │
     │                │  2. SAML Request │
     │                │─────────────────▶│
     │                │                  │
     │  3. Se autentica (MFA)            │
     │                │◀─────────────────│
     │                │                  │
     │  4. SAML Response (aserción)      │
     │                │◀─────────────────│
     │                │                  │
     │  5. Sesión creada                 │
     │◀───────────────│                  │
```

**Cuándo usar SAML vs OIDC:**
- **SAML:** Enterprise, aplicaciones legacy, SSO corporativo
- **OIDC:** Apps modernas, mobile, APIs, desarrollo nuevo

---

### LDAP / Active Directory

Protocolo para consultar y modificar directorios de usuarios.

```
LDAP (Lightweight Directory Access Protocol)

Directorio = Base de datos jerárquica optimizada para lectura

Estructura típica:
dc=empresa,dc=com
├── ou=Usuarios
│   ├── uid=maria
│   ├── uid=juan
│   └── uid=pedro
├── ou=Grupos
│   ├── cn=admins
│   ├── cn=desarrollo
│   └── cn=rrhh
└── ou=Servicios
    └── uid=app-api
```

---

## 5. IAM en la Nube

### AWS IAM

**Componentes principales:**

| Componente | Descripción |
|-----------|-------------|
| **User** | Identidad con credenciales a largo plazo |
| **Role** | Identidad con permisos temporales |
| **Group** | Colección de usuarios |
| **Policy** | Documento JSON que define permisos |
| **Identity Provider** | Federación con directorios externos |

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject"
      ],
      "Resource": "arn:aws:s3:::mi-bucket/*",
      "Condition": {
        "IpAddress": {"aws:SourceIp": "10.0.0.0/8"},
        "Bool": {"aws:MultiFactorAuthPresent": "true"}
      }
    }
  ]
}
```

### Azure AD / Entra ID

**Componentes principales:**

| Componente | Descripción |
|-----------|-------------|
| **Users** | Usuarios (cloud, sincronizados, invitados) |
| **Groups** | Grupos de seguridad y Microsoft 365 |
| **Roles** | Roles administrativos predefinidos y custom |
| **App Registrations** | Identidades de aplicaciones |
| **Managed Identities** | Identidades automáticas para recursos Azure |
| **Conditional Access** | Políticas basadas en señales de riesgo |

### Google Cloud IAM

**Componentes principales:**

| Componente | Descripción |
|-----------|-------------|
| **Principals** | Usuarios, grupos, cuentas de servicio |
| **Roles** | Básicos, predefinidos, custom |
| **Policies** | Vinculan principals con roles en recursos |
| **Service Accounts** | Identidades para aplicaciones |

---

## 6. Flujo Típico de IAM en una Aplicación

```
┌─────────────────────────────────────────────────────────────────┐
│                    FLUJO DE AUTENTICACIÓN                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. Usuario ingresa credenciales                                 │
│         │                                                        │
│         ▼                                                        │
│  2. Servicio de autenticación valida                             │
│         │                                                        │
│         ▼                                                        │
│  3. Se solicita MFA (si está configurado)                        │
│         │                                                        │
│         ▼                                                        │
│  4. Se genera token de sesión (JWT/Opaque)                       │
│         │                                                        │
│         ▼                                                        │
│  5. Token se envía al cliente (cookie/header)                    │
│         │                                                        │
│         ▼                                                        │
│  6. Cada request incluye el token                                │
│         │                                                        │
│         ▼                                                        │
│  7. API Gateway/Proxy valida token y verifica permisos           │
│         │                                                        │
│         ├── Válid → Se procesa la request                        │
│         └── Inválid → 401 Unauthorized / 403 Forbidden           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 7. Escenarios Reales de IAM

### Escenario 1: Onboarding de un nuevo empleado

```
Día 1 - María se une como contadora

RRHH crea el empleado en el sistema HRIS
    │
    ▼
Sincronización automática a Azure AD / Google Workspace
    │
    ├── Se crea cuenta de correo
    ├── Se asigna al grupo "Contabilidad"
    ├── Se le otorga acceso a:
    │   ├── ERP (SAP/Oracle)
    │   ├── Sistema de facturación
    │   ├── Drive compartido del departamento
    │   └── Slack del equipo
    ├── Se fuerza cambio de contraseña en primer login
    └── Se requiere registro de MFA
```

### Escenario 2: Acceso de emergencia (JIT - Just-In-Time)

```
Incidente: Servidor de producción caído a las 2 AM

1. On-call engineer solicita acceso elevado
       │
       ▼
2. Sistema de PAM (Privileged Access Management) evalúa:
   ├── ¿Es horario de guardia? → Sí
   ├── ¿Tiene MFA activo? → Sí
   ├── ¿El incidente está registrado? → Sí (ticket #4521)
       │
       ▼
3. Se concede acceso temporal por 2 horas
   ├── Rol: "Emergency-DBA"
   ├── Duración: 120 minutos
   ├── Scope: Solo servidor prod-db-01
   ├── Sesión grabada para auditoría
       │
       ▼
4. Al vencer el tiempo, acceso se revoca automáticamente
```

### Escenario 3: Offboarding de un empleado

```
María renuncia - último día: 15 de abril

15/04 09:00 - RRHH marca "fin de contrato" en HRIS
       │
       ▼
Workflow automático de offboarding:
   ├── Cuenta de correo → Desactivada (no eliminada)
   ├── Acceso a Slack → Revocado
   ├── Acceso a ERP → Revocado
   ├── Tokens de API → Invalidados
   ├── Sesiones activas → Cerradas (force logout)
   ├── MFA devices → Deregistrados
   ├── Datos personales → Transferidos a supervisor
   ├── Licencias de software → Liberadas
       │
       ▼
Correo de confirmación a RRHH y manager
```

### Escenario 4: Detección de acceso sospechoso

```
03:15 AM - Login exitoso de admin@empresa.com

Señales detectadas:
   ├── País: Rusia (el usuario vive en Uruguay)
   ├── IP: 185.220.101.42 (TOR exit node)
   ├── Device: No reconocido
   ├── Hora: Fuera de horario laboral
       │
       ▼
Respuesta automática de Conditional Access:
   ├── Step-up MFA requerido
   ├── Si falla MFA → Acceso denegado + alerta al SOC
   ├── Si pasa MFA → Acceso con permisos reducidos
   └── Evento registrado en SIEM
```

### Escenario 5: Service-to-Service Authentication

```
Microservicio "pagos" necesita acceder a base de datos "transacciones"

┌───────────┐     ┌──────────────┐     ┌──────────────┐
│ Servicio  │     │  Servicio de │     │  Base de     │
│ "pagos"   │────▶│  Identidad   │────▶│  Datos       │
└───────────┘     └──────────────┘     └──────────────┘
     │                   │                    │
     │  1. Solicita      │                    │
     │  token con su     │                    │
     │  identidad        │                    │
     │──────────────────▶│                    │
     │                   │  2. Token JWT      │
     │                   │  con claims:       │
     │                   │  { "sub": "svc-pagos"│
     │                   │    "roles": ["lector"]│
     │                   │    "exp": 3600 }   │
     │◀──────────────────│                    │
     │                   │                    │
     │  3. Conecta con   │                    │
     │  token en header  │                    │
     │───────────────────────────────────────▶│
     │                   │  4. DB valida      │
     │                   │  token y permite   │
     │                   │  solo lectura      │
     │◀───────────────────────────────────────│
```

---

## 8. Herramientas y Tecnologías IAM

### Proveedores de Identidad (IdP)

| Herramienta | Tipo | Uso |
|-------------|------|-----|
| **Azure AD / Entra ID** | Cloud IdP | Enterprise, Microsoft ecosystem |
| **Okta** | Cloud IdP | SSO, MFA, Lifecycle management |
| **Keycloak** | Open Source | Self-hosted, flexible, gratuito |
| **Auth0** | Cloud IdP | Developer-friendly, APIs |
| **AWS Cognito** | Cloud IdP | Apps en AWS, serverless |
| **Google Identity** | Cloud IdP | Google Workspace, Firebase |

### Gestión de Privilegios (PAM)

| Herramienta | Función |
|-------------|---------|
| **CyberArk** | Gestión de credenciales privilegiadas |
| **HashiCorp Vault** | Secrets management, tokens dinámicos |
| **BeyondTrust** | Remote access seguro |
| **AWS Secrets Manager** | Rotación de secretos en AWS |

### Herramientas Open Source

| Herramienta | Función |
|-------------|---------|
| **Keycloak** | Identity provider completo |
| **OpenLDAP** | Directorio LDAP |
| **FreeIPA** | Identidad + políticas (Linux) |
| **Gluu** | Plataforma IAM open source |
| **Casbin** | Motor de autorización (múltiples lenguajes) |

---

## 9. Ruta de Aprendizaje IAM

### Nivel 1: Fundamentos

1. Entender la diferencia entre autenticación y autorización
2. Aprender los factores de autenticación y MFA
3. Comprender el principio de mínimo privilegio
4. Familiarizarse con contraseñas seguras y gestores de contraseñas

### Nivel 2: Protocolos

1. OAuth 2.0 flows (Authorization Code, Client Credentials)
2. OpenID Connect (ID Tokens, UserInfo)
3. SAML 2.0 para SSO empresarial
4. JWT (estructura, firma, verificación)

### Nivel 3: Implementación

1. Configurar un IdP (Keycloak local o Auth0)
2. Implementar login con OAuth 2.0 + OIDC en una app
3. Crear políticas RBAC en código
4. Configurar MFA condicional

### Nivel 4: Cloud IAM

1. AWS IAM: Users, Roles, Policies, STS
2. Azure AD: Conditional Access, Managed Identities
3. GCP IAM: Service Accounts, Organization Policies
4. Implementar workload identity en Kubernetes

### Nivel 5: Avanzado

1. ABAC y políticas basadas en contexto
2. Privileged Access Management (PAM)
3. Identity Governance & Administration (IGA)
4. Zero Trust Architecture y Zero Trust Network Access

### Recursos Recomendados

| Recurso | Tipo | URL |
|---------|------|-----|
| OAuth 2.0 RFC 6749 | Especificación | https://oauth.net/2/ |
| OIDC Core | Especificación | https://openid.net/connect/ |
| AWS IAM Docs | Documentación | https://docs.aws.amazon.com/iam/ |
| Microsoft Entra ID | Documentación | https://learn.microsoft.com/entra/ |
| Keycloak Docs | Documentación | https://www.keycloak.org/documentation |
| Casbin | Librería | https://casbin.org/ |

---

## 10. Los 8 Errores de Diseño IAM Más Comunes

> Cuando el diseño de identidad es débil, todo el sistema queda expuesto.
> Estos errores aparecen constantemente en análisis post-incidente de brechas reales.
> En startups. En empresas globales. En entornos de nube modernos.

### Error 1: Violar el Principio de Mínimo Privilegio por Defecto

**Problema:** Otorgar permisos excesivos desde el inicio "por si acaso".

**Consecuencias:**
- Un compromiso de credenciales permite acceso ilimitado
- Movimiento lateral trivial dentro del sistema
- Difícil detectar actividad maliciosa entre el ruido de permisos amplios

**Ejemplo real:**
```
# ❌ INCORRECTO - Rol con permisos excesivos
{
  "Action": "*",
  "Resource": "*"
}

# ✅ CORRECTO - Solo lo necesario
{
  "Action": [
    "s3:GetObject",
    "s3:PutObject"
  ],
  "Resource": "arn:aws:s3:::mi-bucket/datos/*"
}
```

**Cómo corregirlo:**
- Empezar con cero permisos y agregar solo lo necesario
- Revisar permisos periódicamente
- Implementar acceso JIT (Just-In-Time) para permisos elevados

---

### Error 2: Credenciales Estáticas de Larga Duración

**Problema:** Claves API, tokens o secretos que nunca rotan.

**Consecuencias:**
- Credenciales filtradas en repositorios de código
- Claves hardcodeadas en imágenes de contenedores
- Exfiltración de secretos desde logs o archivos de configuración

**Ejemplo real:**
```
# ❌ INCORRECTO - Clave estática en código
AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

# ✅ CORRECTO - Roles temporales con STS
aws sts assume-role \
  --role-arn arn:aws:iam::123456789012:role/MiRol \
  --role-session-name sesion-temporal \
  --duration-seconds 3600
```

**Cómo corregirlo:**
- Rotar credenciales automáticamente (máximo 90 días)
- Usar roles temporales en lugar de claves estáticas
- Implementar secret managers (AWS Secrets Manager, HashiCorp Vault)
- Escanar repositorios en busca de secretos expuestos

---

### Error 3: Sin MFA en Cuentas Privilegiadas

**Problema:** Administradores y cuentas de alto valor protegidas solo con contraseña.

**Consecuencias:**
- Credenciales de admin robadas por phishing = acceso total
- Fuerza bruta o credential stuffing exitoso sin barrera adicional
- Violación directa de compliance (PCI-DSS, ISO 27001, NIST)

**Cómo corregirlo:**
- MFA obligatorio para TODAS las cuentas con privilegios
- Preferir MFA físico (YubiKey) o aplicaciones autenticadoras
- SMS como último recurso (vulnerable a SIM swapping)
- Implementar acceso condicional basado en riesgo

---

### Error 4: Cuentas de Servicio Sobre-permisionadas

**Problema:** Las cuentas de servicio (service accounts) tienen más permisos de los que necesitan.

**Consecuencias:**
- Si una aplicación es comprometida, el atacante hereda todos los permisos
- Dificultad para auditar qué hace realmente cada servicio
- Violación del principio de separación de responsabilidades

**Cómo corregirlo:**
- Crear un rol por cada servicio con solo los permisos necesarios
- Revisar periódicamente los permisos vs el uso real
- Implementar service mesh con autenticación mutua (mTLS)
- Usar workload identity en entornos cloud

---

### Error 5: Procesos de Baja (Offboarding) Defectuosos

**Problema:** Usuarios que dejan la organización mantienen acceso activo.

**Consecuencias:**
- Ex-empleados con acceso a datos sensibles
- Cuentas huérfanas que nadie monitorea
- Riesgo de insider threat post-empleo

**Estadística alarmante:**
> Según estudios, el 30% de las cuentas de ex-empleados permanecen activas más de 30 días después de la salida.

**Cómo corregirlo:**
- Automatizar la desactivación de accesos al finalizar contrato
- Integrar RRHH con sistemas de identidad
- Realizar auditorías periódicas de cuentas activas
- Implementar proceso de offboarding con checklist

```python
# Ejemplo: Script de verificación de cuentas huérfanas
from datetime import datetime, timedelta

def encontrar_cuentas_huerfanas(usuarios, empleados_activos, dias_umbral=30):
    """Identifica cuentas activas sin empleado asociado."""
    cuentas_huerfanas = []
    fecha_limite = datetime.now() - timedelta(days=dias_umbral)

    for usuario in usuarios:
        if usuario['id'] not in empleados_activos:
            if usuario['ultimo_acceso'] > fecha_limite:
                cuentas_huerfanas.append({
                    'id': usuario['id'],
                    'nombre': usuario['nombre'],
                    'ultimo_acceso': usuario['ultimo_acceso'],
                    'riesgo': 'ALTO'
                })

    return cuentas_huerfanas
```

---

### Error 6: Modelos de Autorización Planos

**Problema:** Todos los usuarios tienen el mismo nivel de acceso o diferenciación mínima.

**Consecuencias:**
- Un usuario comprometido accede a todo el sistema
- Imposible aplicar segmentación de datos sensibles
- No hay contención ante brechas

**Ejemplo:**
```
# ❌ INCORRECTO - Modelo plano
Grupo "empleados" → Acceso a TODO

# ✅ CORRECTO - Modelo jerárquico
Grupo "lectura" → Solo consultar
Grupo "escritura" → Crear y modificar
Grupo "admin" → Gestión de configuración
Grupo "super-admin" → Acceso total (con MFA + aprobación)
```

**Cómo corregirlo:**
- Implementar RBAC (Role-Based Access Control) con roles granulares
- Considerar ABAC (Attribute-Based Access Control) para casos complejos
- Segmentar por sensibilidad de datos
- Implementar el principio de separación de funciones

---

### Error 7: Confianza Ciega en Integraciones de Terceros

**Problema:** Otorgar permisos excesivos a aplicaciones y servicios de terceros sin revisión.

**Consecuencias:**
- OAuth scopes demasiado amplios ("acceso a tu cuenta" = todo)
- APIs de terceros comprometidas = acceso a tus datos
- Cadenas de suministro de software como vector de ataque

**Ejemplo real:**
```
# ❌ INCORRECTO - OAuth con scopes excesivos
Scope: "read:all write:all admin:all"

# ✅ CORRECTO - Solo lo necesario
Scope: "read:perfil write:correo"
```

**Cómo corregirlo:**
- Revisar permisos solicitados por cada integración de terceros
- Implementar allowlist de dominios y scopes autorizados
- Auditar periódicamente las integraciones activas
- Usar tokens con alcance limitado y tiempo de vida corto
- Implementar proxy de API para control centralizado

---

### Error 8: Sin Logging ni Detección de Anomalías

**Problema:** No registrar actividades de identidad ni monitorear comportamientos inusuales.

**Consecuencias:**
- No se detecta acceso desde ubicaciones inusuales
- Imposible reconstruir la cadena de ataque post-incidente
- No se alertan comportamientos anómalos de cuentas

**Cómo corregirlo:**
- Registrar TODOS los eventos de autenticación y autorización
- Implementar detección de anomalías basada en comportamiento
- Alertar sobre:
  - Accesos fuera de horario laboral
  - Múltiples intentos fallidos
  - Accesos desde ubicaciones geográficas inusuales
  - Volumen de descargas anormal
  - Uso de credenciales desde múltiples IPs

```python
# Ejemplo: Detección de anomalías básicas
import logging
from collections import defaultdict

class DetectorAnomaliasIAM:
    def __init__(self):
        self.accesos_por_usuario = defaultdict(list)
        self.horario_laboral = range(8, 18)
        self.paises_habituales = set()

    def registrar_acceso(self, usuario, hora, pais, ip):
        self.accesos_por_usuario[usuario].append({
            'hora': hora,
            'pais': pais,
            'ip': ip
        })

        alertas = []

        # Acceso fuera de horario
        if hora not in self.horario_laboral:
            alertas.append(f"ACCESO FUERA DE HORARIO: {usuario} a las {hora}")

        # País no habitual
        if pais not in self.paises_habituales:
            alertas.append(f"ACCESO DESDE PAÍS INUSUAL: {usuario} desde {pais}")

        # Múltiples IPs
        accesos_recientes = self.accesos_por_usuario[usuario][-10:]
        ips_unicas = len(set(a['ip'] for a in accesos_recientes))
        if ips_unicas > 3:
            alertas.append(f"MÚLTIPLES IPs PARA: {usuario} ({ips_unicas} IPs)")

        return alertas

# Uso
detector = DetectorAnomaliasIAM()
alertas = detector.registrar_acceso(
    usuario="admin@empresa.com",
    hora=3,
    pais="RU",
    ip="185.220.101.42"
)
for alerta in alertas:
    logging.warning(alerta)
```

---

## 11. Estrategia de Seguridad IAM Recomendada

La estrategia de seguridad más sólida a menudo comienza con algo simple:

1. **Diseñar el acceso con disciplina**
   - Mínimo privilegio desde el inicio
   - Revisión periódica de permisos

2. **Monitorear identidades continuamente**
   - Logs de autenticación y autorización
   - Detección de anomalías automatizada

3. **Tratar los permisos como infraestructura crítica**
   - Versionar cambios de permisos
   - Revisar cambios con proceso de aprobación
   - Automatizar siempre que sea posible

---

## 12. Checklist de Auditoría IAM

### Autenticación
- [ ] MFA obligatorio en todas las cuentas privilegiadas
- [ ] Política de contraseñas robusta
- [ ] Bloqueo de cuentas tras intentos fallidos
- [ ] Sesiones con tiempo de expiración

### Autorización
- [ ] Principio de mínimo privilegio aplicado
- [ ] Roles definidos y documentados
- [ ] Separación de funciones implementada
- [ ] Revisión de permisos periódica (trimestral)

### Credenciales
- [ ] Sin credenciales estáticas en código
- [ ] Rotación automática de secretos
- [ ] Uso de roles temporales
- [ ] Secret manager implementado

### Gobernanza
- [ ] Proceso de onboarding automatizado
- [ ] Proceso de offboarding automatizado
- [ ] Auditoría de cuentas huérfanas mensual
- [ ] Inventario actualizado de cuentas de servicio

### Monitoreo
- [ ] Logs de autenticación centralizados
- [ ] Detección de anomalías activa
- [ ] Alertas de acceso inusual configuradas
- [ ] Revisión de logs periódica

---

## Pregunta para la Comunidad

> **¿Cuál error de diseño IAM has visto más frecuentemente en sistemas reales o revisiones de seguridad?**

---

*Documento creado para fines educativos. Basado en análisis post-incidente de brechas reales en múltiples industrias.*
