# 1.1 Fundamentos de Seguridad en Gestión de Contraseñas

## ¿Qué es un Gestor de Contraseñas?

Un gestor de contraseñas es una aplicación diseñada para almacenar, generar y gestionar credenciales de acceso de forma segura. En lugar de recordar decenas de contraseñas, el usuario solo necesita recordar **una contraseña maestra** (master password) que desbloquea el "vault" (bóveda) donde se almacenan todas las demás credenciales.

### Componentes Fundamentales

```
┌─────────────────────────────────────────────────────┐
│              GESTOR DE CONTRASEÑAS                  │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌──────────────┐    ┌──────────────────────┐      │
│  │   Vault      │    │  Contraseña Maestra  │      │
│  │  (Bóveda)    │◄───│  (Master Password)   │      │
│  │  Cifrada     │    │  Única que memorizas │      │
│  └──────┬───────┘    └──────────────────────┘      │
│         │                                           │
│         ▼                                           │
│  ┌──────────────┐    ┌──────────────────────┐      │
│  │  Generator   │    │  AutoFill            │      │
│  │  de Claves   │    │  (Autocompletado)    │      │
│  │  Aleatorias  │    │  Navegador/App       │      │
│  └──────────────┘    └──────────────────────┘      │
│                                                     │
│  ┌──────────────┐    ┌──────────────────────┐      │
│  │  Compartir   │    │  Sincronización      │      │
│  │  Seguro      │    │  Entre Dispositivos  │      │
│  └──────────────┘    └──────────────────────┘      │
│                                                     │
└─────────────────────────────────────────────────────┘
```

## Cifrado de Extremo a Extremo (E2E)

El cifrado E2E significa que los datos se cifran **en el dispositivo del usuario** antes de enviarse al servidor. El servidor **nunca** ve la información en texto plano.

### Flujo del Cifrado E2E

```
USUARIO                          SERVIDOR                    USUARIO
(Paciente A)                                                    (Paciente B)

Contraseña "MiClave123"
        │
        ▼
┌───────────────┐
│ Derivación    │
│ de Clave      │  ← Master Password + Salt
│ (PBKDF2/Argon2)│
└───────┬───────┘
        │
        ▼
┌───────────────┐
│ Clave de      │  ← 256 bits (AES-256)
│ Cifrado       │
└───────┬───────┘
        │
        ▼
┌───────────────┐
│ Cifrar datos  │  ← Texto plano → Ciphertext
│ (AES-256-GCM) │
└───────┬───────┘
        │
        │ Datos cifrados (ciphertext)
        │
        ▼
┌───────────────┐
│   Almacenar   │──── Almacena ciphertext
│   en Vault    │     (nunca ve texto plano)
└───────────────┘
```

## Modelo Zero-Knowledge

El modelo zero-knowledge garantiza que el proveedor del servicio **no puede acceder** al contenido de las contraseñas almacenadas, ni siquiera bajo coacción legal.

### Propiedades del Zero-Knowledge

| Propiedad | Descripción |
|-----------|-------------|
| **Cifrado en cliente** | Todo el cifrado/descifrado ocurre en el dispositivo del usuario |
| **Clave maestra nunca sale** | La master password no se transmite jamás al servidor |
| **Servidor solo ve hashes** | El servidor almacena un hash de la master password para autenticación |
| **No hay acceso de emergencia** | Ni siquiera el administrador del servidor puede ver las contraseñas |
| **Plausible deniability** | Es posible tener vaults ocultos que el servidor no puede detectar |

### Flujo de Autenticación Zero-Knowledge

```
┌──────────────────┐                    ┌──────────────────┐
│     CLIENTE      │                    │     SERVIDOR     │
├──────────────────┤                    ├──────────────────┤
│                  │                    │                  │
│ 1. Master Pass   │                    │                  │
│    "MiClave123"  │                    │                  │
│        │         │                    │                  │
│        ▼         │                    │                  │
│ 2. PBKDF2/Argon2 │                    │                  │
│    (100K+ iter)  │                    │                  │
│        │         │                    │                  │
│        ▼         │                    │                  │
│ 3. Auth Key ─────│─── Envía hash ────►│ Verifica hash    │
│    (para auth)   │                    │ contra almacenado│
│                  │                    │                  │
│ 4. Master Key ───│  NUNCA se envía   │  (no la recibe)  │
│    (para cifrar) │  al servidor       │                  │
│                  │                    │                  │
└──────────────────┘                    └──────────────────┘
```

## Derivación de Claves

La derivación de claves convierte una contraseña en una clave criptográfica utilisable. Es una función intencionalmente **lenta** para dificultar ataques de fuerza bruta.

### PBKDF2 (Password-Based Key Derivation Function 2)

```
Clave = PBKDF2(Contraseña, Salt, Iteraciones, Longitud_Clave)

Parámetros recomendados:
- Iteraciones: ≥ 100,000 (recomendado: 600,000+ para SHA-256)
- Salt: 16 bytes aleatorios
- Longitud de clave: 256 bits (32 bytes)
```

### Argon2id (Recomendado actualmente)

```
Clave = Argon2id(Contraseña, Salt, Iteraciones, Memoria, Paralelismo)

Parámetros recomendados:
- Iteraciones (time): 3
- Memoria: 64 MB (65536 KB)
- Paralelismo: 4 threads
- Salt: 16 bytes
- Longitud de clave: 32 bytes
```

### Comparación PBKDF2 vs Argon2id

| Característica | PBKDF2 | Argon2id |
|----------------|--------|----------|
| **Resistencia a GPU/ASIC** | Baja | Alta |
| **Uso de memoria** | Mínimo | Alto (configurable) |
| **Uso de CPU** | Alto | Alto |
| **Uso de paralelismo** | No | Sí |
| **Recomendación actual** | Aceptable | Preferido |
| **Adoptado por** | Bitwarden, KeePass | 1Password, KeePass (opcional) |

## Almacenamiento: Local vs Remoto vs Híbrido

### Opción 1: Solo Local (KeePass)

```
┌─────────────────┐
│  PC del Usuario  │
│  ┌─────────────┐ │
│  │  vault.kdbx │ │  ← Archivo local cifrado
│  │  (cifrado)  │ │
│  └─────────────┘ │
└─────────────────┘

Ventajas: Control total, sin dependencia de red
Desventajas: Sin sincronización, sin respaldo automático
```

### Opción 2: Solo Remoto (Bitwarden cloud)

```
┌─────────────────┐         ┌─────────────────┐
│  PC del Usuario  │◄───────►│  Servidor       │
│                  │  Sync   │  Bitwarden      │
└─────────────────┘         └─────────────────┘

Ventajas: Sincronización automática, acceso desde cualquier lugar
Desventajas: Dependencia del proveedor, riesgo de breach del servidor
```

### Opción 3: Híbrida (Vaultwarden autoalojado)

```
┌─────────────────┐         ┌─────────────────┐
│  PC del Usuario  │◄───────►│  Vaultwarden    │
│  (caché local)  │  Sync   │  (servidor      │
└─────────────────┘         │   propio BHU)   │
                            └────────┬────────┘
                                     │
                            ┌────────▼────────┐
                            │   PostgreSQL    │
                            │   (datos)       │
                            └─────────────────┘

Ventajas: Control total + Sincronización + Sin costos de licencia
Desventajas: Requiere infraestructura y mantenimiento propio
```

## Autenticación Multi-Factor (MFA)

### Tipos de MFA

| Tipo | Descripción | Seguridad | Ejemplo |
|------|-------------|-----------|---------|
| **TOTP** | Código temporal de 6 dígitos | Media-Alta | Google Authenticator, Authy |
| **SMS** | Código enviado por SMS | Baja | No recomendado |
| **Email** | Código enviado por correo | Baja | No recomendado |
| **WebAuthn/FIDO2** | Llave física o biometría | Alta | YubiKey, Windows Hello |
| **Push** | Notificación en app móvil | Media | Duo Mobile |

### WebAuthn / FIDO2 (Estándar Moderno)

```
┌──────────┐              ┌──────────┐              ┌──────────┐
│  Usuario │              │ Navegador│              │ Servidor │
├──────────┤              ├──────────┤              ├──────────┤
│          │  1. Solicita │          │  2. Challenge│          │
│          │◄─────────────│◄─────────│◄─────────────│          │
│          │              │          │              │          │
│  Touch ID│  3. Biometría│          │              │          │
│  o YubiKey│─────────────►│          │              │          │
│          │              │  4. Firma│  5. Verifica │          │
│          │              │─────────►│─────────────►│          │
│          │              │          │  6. Acceso   │          │
│          │              │          │─────────────►│          │
└──────────┘              └──────────┘              └──────────┘
```

## Resumen de Conceptos Clave

| Concepto | Definición |
|----------|------------|
| **Vault** | Bóveda cifrada donde se almacenan las contraseñas |
| **Master Password** | Contraseña maestra que desbloquea el vault |
| **E2E** | Cifrado de extremo a extremo, el servidor nunca ve datos en claro |
| **Zero-Knowledge** | Modelo donde el proveedor no puede acceder a los datos |
| **Salt** | Valor aleatorio añadido a la contraseña antes de hashear |
| **KDF** | Función de derivación de claves (PBKDF2, Argon2id) |
| **TOTP** | Código temporal basado en tiempo (cambia cada 30s) |
| **WebAuthn** | Estándar de autenticación con llaves físicas o biometría |
| **HIBP** | Have I Been Pwned - servicio de verificación de brechas |
| **Breach** | Fuga de datos de credenciales |

---

> **Actividad de Reflexión**: ¿Por qué es importante que la contraseña maestra NUNCA se envíe al servidor? ¿Qué pasaría si un atacante obtuviera la base de datos del servidor Vaultwarden?
