# 2.2 Análisis por Escenarios de Uso

## Escenario 1: Uso Personal (1 usuario)

### Perfil
- Usuario individual
- Dispositivos: PC personal + teléfono móvil
- Necesidades: Contraseñas de email, redes sociales, banca online, compras

### Solución Recomendada

```
┌─────────────────────────────────────────┐
│         USO PERSONAL                    │
├─────────────────────────────────────────┤
│                                         │
│  Opción A: KeePassXC (control total)   │
│  ┌─────────────┐                       │
│  │ vault.kdbx  │ ← Archivo local       │
│  │ (cifrado)   │ ← Copia en USB/Nube   │
│  └─────────────┘                       │
│                                         │
│  Opción B: Bitwarden (comodidad)       │
│  ┌─────────────┐    ┌─────────────┐   │
│  │  Dispositivo │───►│  Servidor   │   │
│  │  (vault)     │    │  Bitwarden  │   │
│  └─────────────┘    └─────────────┘   │
│                                         │
└─────────────────────────────────────────┘
```

### Configuración Mínima de Seguridad

| Elemento | Configuración |
|----------|---------------|
| **Contraseña maestra** | ≥16 caracteres, entropía ≥80 bits |
| **2FA** | TOTP obligatorio |
| **Pin local** | Configurar en clientes móviles |
| **Verificación HIBP** | Activar |
| **Backup** | Exportar vault cifrado periódicamente |
| **Biometría** | Activar en dispositivo móvil |

---

## Escenario 2: PYME (5-50 usuarios)

### Perfil
- Empresa pequeña-mediana
- Departamentos: Administración, Ventas, TI, RRHH
- Necesidades: Compartir credenciales de servicios, redes sociales corporativas, APIs

### Solución Recomendada: Vaultwarden

```
┌─────────────────────────────────────────────────────┐
│              PYME - Vaultwarden                      │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Servidor BHU                                       │
│  ┌─────────────────────────────────────┐           │
│  │  Vaultwarden (Docker)               │           │
│  │  ┌───────────┐  ┌───────────────┐  │           │
│  │  │ API/Auth  │  │  WebSocket    │  │           │
│  │  └───────────┘  └───────────────┘  │           │
│  │  ┌───────────────────────────────┐  │           │
│  │  │       PostgreSQL              │  │           │
│  │  └───────────────────────────────┘  │           │
│  └─────────────────────────────────────┘           │
│                    │                                │
│     ┌──────────────┼──────────────┐               │
│     ▼              ▼              ▼               │
│  ┌──────┐     ┌──────┐     ┌──────┐              │
│  │Admin │     │Ventas│     │  TI  │              │
│  │ 5 usr│     │10 usr│     │ 3 usr│              │
│  └──────┘     └──────┘     └──────┘              │
│                                                     │
│  Estructura de Organización:                        │
│  ├── BHU (Organización)                            │
│  │   ├── Colección: Administración                 │
│  │   ├── Colección: Ventas                         │
│  │   ├── Colección: TI (solo miembros)             │
│  │   ├── Colección: Compartida General             │
│  │   └── Colección: Servicios Compartidos          │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### Configuración de Organización

| Configuración | Valor |
|---------------|-------|
| **Dominio verificado** | bhuru.uy |
| **2FA obligatorio** | Sí (TOTP o WebAuthn) |
| **Rotación de contraseñas** | 90 días (servicios críticos) |
| **Política de contraseñas** | ≥16 caracteres, complejidad |
| **Verificación HIBP** | Habilitada |
| **Política de emergencia** | Break-glass documentado |

### Estructura de Colecciones

```
BHU (Organización)
├── 📁 Administración
│   ├── Contraseñas de administración general
│   ├── Redes sociales corporativas
│   └── Herramientas de gestión
├── 📁 Ventas
│   ├── CRM
│   ├── Herramientas de email
│   └── Redes sociales de ventas
├── 📁 TI (Solo miembros)
│   ├── Servidores
│   ├── APIs de desarrollo
│   ├── Herramientas de monitoreo
│   └── Credenciales de emergencia
├── 📁 Compartida General
│   ├── WiFi corporativa
│   ├── Impresoras
│   └── Herramientas comunes
└── 📁 Servicios Externos
    ├── Hosting
    ├── Dominios
    └── APIs de terceros
```

---

## Escenario 3: Banco / Institución Financiera

### Perfil
- Alta seguridad requerida
- Cumplimiento regulatorio (PCI-DSS, SOX)
- Auditoría completa
- Acceso restringido por roles

### Solución Recomendada: Vaultwarden HA + Hardening

```
┌─────────────────────────────────────────────────────────┐
│          BANCO - Arquitectura HA                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  CDN/WAF                                               │
│  ┌─────────────────────────────────────┐               │
│  │  Cloudflare / AWS WAF               │               │
│  │  - Rate limiting                    │               │
│  │  - DDoS protection                  │               │
│  │  - Geo-filtering                    │               │
│  └─────────────────┬───────────────────┘               │
│                    │                                    │
│  Load Balancer                                              │
│  ┌─────────────────┴───────────────────┐               │
│  │  NGINX (2x - HA)                    │               │
│  │  - TLS 1.3 termination              │               │
│  │  - Certificate pinning              │               │
│  │  - HSTS habilitado                  │               │
│  │  - Rate limiting por IP             │               │
│  └─────────────────┬───────────────────┘               │
│                    │                                    │
│  Vaultwarden Cluster                                             │
│  ┌─────────────────┴───────────────────┐               │
│  │  Vaultwarden (3x réplicas)          │               │
│  │  - Stateless (sin estado local)     │               │
│  │  - Shared storage: /data → NFS/S3   │               │
│  │  - WebSocket connections balanceadas│               │
│  └─────────────────┬───────────────────┘               │
│                    │                                    │
│  Database Cluster                                                │
│  ┌─────────────────┴───────────────────┐               │
│  │  PostgreSQL (Primary + 2 Réplicas)  │               │
│  │  - Streaming replication            │               │
│  │  - Auto-failover (Patroni)          │               │
│  │  - Backups cada 15 min              │               │
│  │  - Encryption at rest               │               │
│  └─────────────────────────────────────┘               │
│                                                         │
│  Almacenamiento                                               │
│  ┌─────────────────────────────────────┐               │
│  │  NFS/S3 (adjuntos, backups)         │               │
│  │  - Cifrado AES-256                  │               │
│  │  - Replicación cross-region         │               │
│  │  - Lifecycle: backup → Cold → Delete│               │
│  └─────────────────────────────────────┘               │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Controles de Seguridad Adicionales

| Control | Implementación |
|---------|----------------|
| **WAF** | Cloudflare/AWS WAF con reglas OWASP |
| **Rate limiting** | 100 req/min por IP, 10 login失败/min |
| **Certificate pinning** | Hash del certificado hardcodeado |
| **HSTS** | max-age=31536000, includeSubDomains |
| **CSP** | Content-Security-Policy estricto |
| **Audit logging** | Todos los eventos a SIEM |
| **Network segmentation** | Vaultwarden en DMZ interna |
| **Encryption at rest** | LUKS/dm-crypt en volúmenes |
| **Backup encryption** | GPG para backups off-site |
| **Incident response** | Runbook documentado |

### Cumplimiento Regulatorio

| Requisito | Implementación |
|-----------|----------------|
| **PCI-DSS 8.3** | Contraseñas ≥12 caracteres, 90 días rotación |
| **PCI-DSS 8.4** | MFA obligatorio para acceso administrativo |
| **SOX** | Audit trail completo, control de acceso |
| **GDPR** | Datos cifrados E2E, right to erasure |

---

## Escenario 4: Empresa Mediana (50-500 usuarios)

### Perfil
- Múltiples sedes o workforces remotos
- Departamentos: TI, RRHH, Ventas, Marketing, Legal, Finanzas
- Integración con Active Directory/LDAP
- Requisitos de compliance

### Solución Recomendada: Vaultwarden HA + LDAP

```
┌─────────────────────────────────────────────────────────┐
│          EMPRESA MEDIANA - Vaultwarden + LDAP            │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Directorio Activo                                       │
│  ┌─────────────────────────────────────┐               │
│  │  Active Directory / LDAP            │               │
│  │  - Usuarios existentes              │               │
│  │  - Grupos por departamento          │               │
│  │  - Políticas de contraseña          │               │
│  └─────────────────┬───────────────────┘               │
│                    │ Sync                               │
│  Vaultwarden                                                    │
│  ┌─────────────────┴───────────────────┐               │
│  │  Vaultwarden (HA)                    │               │
│  │  - Auth via LDAP                     │               │
│  │  - SSO con SAML/OIDC                │               │
│  │  - SCIM para provisioning            │               │
│  │  - Organizaciones por depto          │               │
│  └─────────────────┬───────────────────┘               │
│                    │                                    │
│  Usuarios                                                   │
│  ├── TI (50 usr) → Colección TI                         │
│  ├── RRHH (20 usr) → Colección RRHH                    │
│  ├── Ventas (100 usr) → Colección Ventas               │
│  ├── Marketing (30 usr) → Colección Marketing           │
│  ├── Legal (10 usr) → Colección Legal                   │
│  └── Finanzas (15 usr) → Colección Finanzas            │
│                                                         │
│  Integraciones:                                            │
│  ├── Jira → API para guardar credenciales              │
│  ├── GitLab → Secrets en pipelines                     │
│  ├── CI/CD → Vaultwarden CLI para despliegues          │
│  └── Monitoring → Alertas de uso anómalo               │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Estrategia de Roles

| Rol | Permisos |
|-----|----------|
| **Owner** | Control total de la organización |
| **Admin** | Gestionar usuarios y colecciones |
| **Manager** | Gestionar su colección |
| **User** | Usar contraseñas asignadas |
| **Custom** | Permisos granulares por colección |

---

## Comparativa de Costos por Escenario

| Escenario | Solución | Costo Anual |
|-----------|----------|-------------|
| **Personal** | KeePassXC | $0 |
| **Personal** | Bitwarden cloud | $0-$10 |
| **PYME (20 usr)** | Vaultwarden self-hosted | $0 + infraestructura |
| **PYME (20 usr)** | Bitwarden org | $1,440 ($6/user/mes) |
| **Banco (100 usr)** | Vaultwarden HA | $0 + infraestructura HA |
| **Banco (100 usr)** | Bitwarden enterprise | $7,200 ($6/user/mes) |
| **Empresa (200 usr)** | Vaultwarden HA | $0 + infraestructura HA |
| **Empresa (200 usr)** | Bitwarden enterprise | $14,400 ($6/user/mes) |

> **Conclusión**: Vaultwarden self-hosted ofrece ahorros significativos a partir de 10 usuarios, manteniendo funcionalidad equivalente.

---

> **Actividad**: Diseña la estructura de organizaciones y colecciones para una empresa de 50 personas con 5 departamentos. Define qué contraseñas van en cada colección y quién tiene acceso.
