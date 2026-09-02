# 2.1 Comparativa de Herramientas de Gestión de Contraseñas

## Matriz Comparativa General

| Característica | KeePassXC | Vaultwarden | Passbolt CE | Bitwarden | ProtonPass | Padloc |
|----------------|-----------|-------------|-------------|-----------|------------|--------|
| **Licencia** | GPL-3.0 | AGPL-3.0 | AGPL-3.0 | GPL-3.0 | Propietaria | GPL-3.0 |
| **Costo** | Gratis | Gratis | Gratis | Gratis/Pago | Gratis/Pago | Gratis |
| **Tipo** | Desktop | Self-hosted | Self-hosted | Cloud/Self-hosted | Cloud | Cloud/Self-hosted |
| **Plataformas** | Win/Mac/Linux | Multi (via clientes BW) | Web | Multi | Multi | Multi |
| **Cifrado E2E** | ✅ AES-256 | ✅ AES-256-CBC | ✅ AES-256-GCM | ✅ AES-256 | ✅ AES-256 | ✅ AES-256-GCM |
| **Zero-Knowledge** | ✅ N/A (local) | ✅ | ✅ | ✅ | ✅ | ✅ |
| **KDF** | AES-KDF/Argon2id | PBKDF2/Argon2id | Argon2id | PBKDF2/Argon2id | PBKDF2 | Argon2id |
| **2FA/TOTP** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **WebAuthn/FIDO2** | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| **Biometría** | ❌ | ✅ (via clientes) | ❌ | ✅ (via clientes) | ✅ | ❌ |
| **Generador** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Autofill** | ❌ (manual) | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Compartir** | ❌ (manual) | ✅ Colecciones | ✅ Grupos | ✅ Organizaciones | ✅ | ✅ |
| **Organizaciones** | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **API** | ❌ | ✅ REST API | ✅ REST API | ✅ REST API | ❌ | ✅ |
| **Historial** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Audit Log** | ❌ | ✅ | ✅ | ✅ (pago) | ❌ | ❌ |
| **Auto-hosted** | ✅ (es local) | ✅ Docker | ✅ Docker | ✅ Docker | ❌ | ✅ Docker |
| **Alta Disponibilidad** | ❌ | ✅ (con DB) | ✅ (con DB) | ✅ (oficial) | ✅ (cloud) | ✅ |
| **HIBP Check** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Adjuntos cifrados** | ❌ | ✅ | ✅ | ✅ (pago) | ❌ | ❌ |
| **Max usuarios** | 1 | Ilimitado | Ilimitado | Ilimitado (self-host) | 1 (gratis) | Ilimitado |

## Análisis Detallado por Herramienta

### 1. KeePassXC (Desktop - 100% Local)

```
┌─────────────────────────────────────────────┐
│              KeePassXC                       │
├─────────────────────────────────────────────┤
│  Archivo: vault.kdbx (local)               │
│  Cifrado: AES-256-Rijndael o ChaCha20      │
│  KDF: AES-KDF, Argon2d, Argon2id           │
│  Plugin: KeePassXC-Browser (autofill)      │
│  Sync: Manual ( Dropbox, NFS, USB)         │
│  Costo: $0                                 │
│  Ideal para: Usuarios técnicos, uso        │
│              personal estricto              │
└─────────────────────────────────────────────┘
```

**Ventajas:**
- Control total del archivo vault
- Sin dependencia de servidor
- Open source auditable
- Soporte YubiKey/Hardware keys

**Desventajas:**
- Sin sincronización automática
- Sin compartición granular
- Sin auditoría de uso
- Curva de aprendizaje alta

### 2. Vaultwarden (Self-hosted - Backend Bitwarden)

```
┌─────────────────────────────────────────────┐
│              Vaultwarden                     │
├─────────────────────────────────────────────┤
│  Base: Server oficial Bitwarden (Rust)      │
│  Clientes: Todos los oficiales de BW       │
│  DB: SQLite / PostgreSQL / MySQL / MSSQL   │
│  Cifrado: AES-256-CBC + HMAC               │
│  KDF: PBKDF2, Argon2id                     │
│  Sync: Automática entre dispositivos       │
│  Costo: $0 (sin límite de usuarios)        │
│  Ideal para: PYMEs, equipos, uso familiar   │
└─────────────────────────────────────────────┘
```

**Ventajas:**
- Experiencia idéntica a Bitwarden premium
- Sin costo por usuario
- Todos los clientes oficiales funcionan
- API completa para integraciones
- Soporte 2FA, WebAuthn, TOTP

**Desventajas:**
- Requiere infraestructura propia
- No tiene soporte oficial
- Mantenimiento por cuenta propia

### 3. Passbolt Community Edition (Self-hosted)

```
┌─────────────────────────────────────────────┐
│              Passbolt CE                     │
├─────────────────────────────────────────────┤
│  Enfoque: Gestión de contraseñas de equipo  │
│  API: REST (GPG-based)                      │
│  Cifrado: OpenPGP (GPG)                    │
│  DB: PostgreSQL / MySQL / MariaDB          │
│  Auth: Local, LDAP, AD, OIDC               │
│  Costo: $0 (Community), Pago (Pro/Enterprise)│
│  Ideal para: Equipos técnicos, DevOps       │
└─────────────────────────────────────────────┘
```

**Ventajas:**
- Enfoque en trabajo en equipo
- GPG para cifrado (estándar abierto)
- Soporte LDAP/Active Directory
- Workflow de aprobación de contraseñas

**Desventajas:**
- Interfaz menos pulida que Bitwarden
- Comunidad más pequeña
- Menos clientes nativos (principalmente extensión)
- Curva de aprendizaje con GPG

### 4. Bitwarden (Cloud / Self-hosted oficial)

```
┌─────────────────────────────────────────────┐
│              Bitwarden                       │
├─────────────────────────────────────────────┤
│  Cloud: bitwarden.com (hosted)              │
│  Self-hosted: docker officiaL              │
│  Cifrado: AES-256-CBC + HMAC               │
│  KDF: PBKDF2 (default), Argon2id (nuevo)  │
│  Precio: $0 (personal), $6/user (org)      │
│  Ideal para: Empresas con soporte oficial  │
└─────────────────────────────────────────────┘
```

**Ventajas:**
- Soporte oficial
- Infraestructura gestionada (cloud)
- Cumplimiento SOC 2, GDPR
- Actualizaciones automáticas

**Desventajas:**
- Costo por usuario en planes organizacionales
- Dependencia del proveedor
- Datos en servidores de terceros

### 5. Proton Pass

```
┌─────────────────────────────────────────────┐
│              Proton Pass                      │
├─────────────────────────────────────────────┤
│  Empresa: Proton (Suiza)                    │
│  Cifrado: E2E con srv4                       │
│  Incluye: Email alias, VPN                  │
│  Precio: $0 (básico), $4.99/mes (premium)  │
│  Ideal para: Usuarios no técnicos           │
└─────────────────────────────────────────────┘
```

### 6. Padloc

```
┌─────────────────────────────────────────────┐
│              Padloc                           │
├─────────────────────────────────────────────┤
│  Tipo: Open source, moderno                 │
│  Cifrado: AES-256-GCM + Argon2id           │
│  Self-hosted: Docker                        │
│  Precio: $0                                 │
│  Ideal para: Usuarios que buscan simplicidad│
└─────────────────────────────────────────────┘
```

## Recomendación por Escenario

| Escenario | Herramienta Recomendada | Razón |
|-----------|------------------------|-------|
| **Uso personal** | KeePassXC o Bitwarden gratis | KeePass = control total; BW = comodidad |
| **Familia (5-10)** | Vaultwarden | Gratis, compartición fácil |
| **PYME (10-50)** | Vaultwarden o Passbolt | Gratis, organización, auditoría |
| **Empresa (50-500)** | Vaultwarden (HA) o Bitwarden org | Escalabilidad, soporte |
| **Desarrolladores** | Vaultwarden + API | Integración con CI/CD |
| **Banco/Alta seguridad** | Vaultwarden + PostgreSQL HA | Control total, compliance |
| **Personal no técnico** | Bitwarden cloud o ProtonPass | Sin configuración, fácil |

## Decisión: ¿Por qué Vaultwarden para BHU?

```
FACTORES DE DECISIÓN PARA BHU:

✅ 100% gratuito (sin límite de usuarios)
✅ Open source (auditable)
✅ Experiencia idéntica a Bitwarden premium
✅ Todos los clientes oficiales (extensión, desktop, móvil)
✅ Biometría (Windows Hello, Touch ID, Face ID)
✅ Organizaciones + Colecciones compartidas
✅ API completa para integraciones
✅ Self-hosted (datos bajo control de BHU)
✅ PostgreSQL para alta disponibilidad
✅ Docker (despliegue estandarizado)
✅ TOTP/WebAuthn/FIDO2 integrado
✅ Sin costo por usuario ni por funcionalidad
✅ Comunidad activa y documentación extensa
```

---

> **Actividad**: Evalúa cada herramienta según los siguientes criterios: costo, facilidad de uso, seguridad, escalabilidad y soporte. Justifica cuál elegirías para una empresa de 30 personas.
