# 4.5 Políticas por Sistema: Regex, Rotación y Generación Automática

## Visión General

Cada sistema/servicio tiene **su propia política de contraseñas** definida por el administrador. El sistema aplica automáticamente estas políticas para:
- **Generar** contraseñas que cumplan la política
- **Validar** contraseñas existentes contra la política
- **Notificar** cuando una contraseña está por vencer
- **Bloquear** contraseñas que no cumplan la política

---

## Arquitectura de Políticas

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    SISTEMA DE POLÍTICAS POR SISTEMA                      │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    SERVIDOR CENTRAL                              │   │
│  │                                                                  │   │
│  │  ┌──────────────────────────────────────────────────────────┐   │   │
│  │  │  Base de Datos de Políticas                               │   │   │
│  │  │                                                           │   │   │
│  │  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │   │   │
│  │  │  │ Linux/SSH   │  │ Windows AD  │  │ Oracle DB   │     │   │   │
│  │  │  │ Policy      │  │ Policy      │  │ Policy      │     │   │   │
│  │  │  │ (regex)     │  │ (regex)     │  │ (regex)     │     │   │   │
│  │  │  └─────────────┘  └─────────────┘  └─────────────┘     │   │   │
│  │  │                                                           │   │   │
│  │  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │   │   │
│  │  │  │ API REST    │  │ Web App     │  │ Email       │     │   │   │
│  │  │  │ Policy      │  │ Policy      │  │ Policy      │     │   │   │
│  │  │  │ (regex)     │  │ (regex)     │  │ (regex)     │     │   │   │
│  │  │  └─────────────┘  └─────────────┘  └─────────────┘     │   │   │
│  │  │                                                           │   │   │
│  │  └──────────────────────────────────────────────────────────┘   │   │
│  │                                                                  │   │
│  │  ┌──────────────────────────────────────────────────────────┐   │   │
│  │  │  Configuración Global                                     │   │   │
│  │  │  - Master password rotation (ej: 180 días)               │   │   │
│  │  │  - Recordatorio antes de vencimiento (ej: 14 días)       │   │   │
│  │  │  - Acciones al vencer (bloquear, notificar, permitir)    │   │   │
│  │  └──────────────────────────────────────────────────────────┘   │   │
│  │                                                                  │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                         │                                               │
│                    Distribuye políticas                                │
│                         │                                               │
│  DISPOSITIVOS DE USUARIOS                                               │
│  ┌─────────────────────┴────────────────────┐                         │
│  │  App Local (vault) recibe políticas y:   │                         │
│  │  - Valida contraseñas contra regex        │                         │
│  │  - Genera según política del sistema      │                         │
│  │  - Muestra días restantes de rotación     │                         │
│  │  - Notifica al usuario antes de vencer   │                         │
│  └───────────────────────────────────────────┘                         │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Plantilla de Política

```json
{
  "system_id": "linux-servers",
  "system_name": "Servidores Linux/SSH",
  "description": "Política para contraseñas de acceso SSH a servidores Linux",
  "enabled": true,
  "created_at": "2026-08-01",
  "updated_at": "2026-08-01",
  "created_by": "admin@bhu.com.uy",
  "password_policy": {
    "min_length": 16,
    "max_length": 128,
    "required_regex": "^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[@$!%*?&#])[A-Za-z\\d@$!%*?&#]{16,}$",
    "description_regex": "Mínimo 16 caracteres, 1 mayúscula, 1 minúscula, 1 número, 1 símbolo (@$!%*?&#)",
    "disallowed_chars": ["'", "\"", "\\", " "],
    "disallowed_patterns": ["password", "admin", "bhu", "root"],
    "entropy_min_bits": 60
  },
  "rotation": {
    "enabled": true,
    "days": 90,
    "warn_days_before": 14,
    "grace_period_days": 7,
    "action_on_expiry": "notify_and_block",
    "allow_extension": true,
    "max_extensions": 2
  },
  "generation": {
    "auto_generate": true,
    "default_length": 20,
    "include_uppercase": true,
    "include_lowercase": true,
    "include_numbers": true,
    "include_symbols": true,
    "excluded_symbols": ["\"", "'", "\\", "`"],
    "algorithm": "crypto-random"
  },
  "notifications": {
    "on_created": ["email"],
    "on_updated": ["email"],
    "on_expiring": ["email", "desktop"],
    "on_expired": ["email", "desktop", "sms"],
    "recipients": ["owner", "manager"]
  },
  "tags": ["linux", "ssh", "servers", "production"],
  "applicable_groups": ["sysadmin", "devops"]
}
```

---

## Políticas Predefinidas por Sistema

### 1. Linux/SSH

| Campo | Valor |
|-------|-------|
| **ID** | `linux-ssh` |
| **Mínimo caracteres** | 16 |
| **Requerido** | `^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#]).{16,}$` |
| **Descripción regex** | 1 mayúscula, 1 minúscula, 1 número, 1 símbolo |
| **Rotación** | 90 días |
| **Notificación** | 14 días antes |
| **Acción al vencer** | Bloquear + notificar |

**Regex completa:**
```
^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{16,}$
```

**Ejemplo de contraseña válida:** `Kj$9mNpL2xQw!4rT`

---

### 2. Windows Active Directory

| Campo | Valor |
|-------|-------|
| **ID** | `windows-ad` |
| **Mínimo caracteres** | 14 |
| **Requerido** | `^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*]).{14,}$` |
| **Descripción regex** | 1 mayúscula, 1 minúscula, 1 número, 1 símbolo |
| **Rotación** | 60 días |
| **Notificación** | 10 días antes |
| **Acción al vencer** | Forzar cambio |

**Regex completa:**
```
^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{14,}$
```

**Notas:**
- AD tiene policy de complejidad integrada
- No permite las últimas 24 contraseñas
- Cuenta bloqueada tras 5 intentos fallidos

---

### 3. Oracle Database

| Campo | Valor |
|-------|-------|
| **ID** | `oracle-db` |
| **Mínimo caracteres** | 18 |
| **Requerido** | `^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[_#]).{18,}$` |
| **Descripción regex** | 1 mayúscula, 1 minúscula, 1 número, 1 guión bajo o numeral |
| **Rotación** | 45 días |
| **Notificación** | 7 días antes |
| **Acción al vencer** | Bloquear cuenta |

**Regex completa:**
```
^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[_#])[A-Za-z\d_#]{18,}$
```

**Ejemplo de contraseña válida:** `Db#Admin_2026_Secure!`

---

### 4. API REST (Microservicios)

| Campo | Valor |
|-------|-------|
| **ID** | `api-rest` |
| **Mínimo caracteres** | 32 |
| **Requerido** | `^[A-Za-z\d\-_]{32,64}$` |
| **Descripción regex** | Solo alfanuméricos, guiones y guiones bajos (API keys) |
| **Rotación** | 30 días |
| **Notificación** | 5 días antes |
| **Acción al vencer** | Revocar y regenerar |

**Regex completa:**
```
^[A-Za-z\d\-_]{32,64}$
```

**Ejemplo de contraseña válida:** `aB3$kL9mNpQrStUvWxYz1234567890abcd`

---

### 5. Aplicaciones Web (Bancarias)

| Campo | Valor |
|-------|-------|
| **ID** | `web-apps` |
| **Mínimo caracteres** | 20 |
| **Requerido** | `^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*]).{20,}$` |
| **Descripción regex** | 1 mayúscula, 1 minúscula, 1 número, 1 símbolo |
| **Rotación** | 30 días |
| **Notificación** | 7 días antes |
| **Acción al vencer** | Forzar cambio en próximo login |

**Regex completa:**
```
^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{20,}$
```

**Ejemplo de contraseña válida:** `Banco2026$Secure#Access!`

---

### 6. Email Corporate

| Campo | Valor |
|-------|-------|
| **ID** | `email-corporate` |
| **Mínimo caracteres** | 16 |
| **Requerido** | `^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%]).{16,}$` |
| **Descripción regex** | 1 mayúscula, 1 minúscula, 1 número, 1 símbolo |
| **Rotación** | 60 días |
| **Notificación** | 14 días antes |
| **Acción al vencer** | Bloquear + notificar |

**Regex completa:**
```
^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%])[A-Za-z\d!@#$%]{16,}$
```

---

### 7. WiFi Corporativo

| Campo | Valor |
|-------|-------|
| **ID** | `wifi-corporate` |
| **Mínimo caracteres** | 24 |
| **Requerido** | `^[A-Za-z\d\-_]{24,}$` |
| **Descripción regex** | Alfanuméricos, guiones y guiones bajos |
| **Rotación** | 90 días |
| **Notificación** | 14 días antes |
| **Acción al vencer** | Cambiar en todos los dispositivos |

**Regex completa:**
```
^[A-Za-z\d\-_]{24,}$
```

**Nota:** WPA3-Enterprise usa certificados, no contraseñas. Este policy aplica a PSK.

---

### 8. VPN (Acceso Remoto)

| Campo | Valor |
|-------|-------|
| **ID** | `vpn-access` |
| **Mínimo caracteres** | 20 |
| **Requerido** | `^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*]).{20,}$` |
| **Descripción regex** | 1 mayúscula, 1 minúscula, 1 número, 1 símbolo |
| **Rotación** | 30 días |
| **Notificación** | 7 días antes |
| **Acción al vencer** | Desconectar sesión activa + notificar |

**Regex completa:**
```
^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{20,}$
```

---

### 9. Cloud (AWS/Azure/GCP)

| Campo | Valor |
|-------|-------|
| **ID** | `cloud-services` |
| **Mínimo caracteres** | 24 |
| **Requerido** | `^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*]).{24,}$` |
| **Descripción regex** | 1 mayúscula, 1 minúscula, 1 número, 1 símbolo |
| **Rotación** | 30 días |
| **Notificación** | 7 días antes |
| **Acción al vencer** | Revocar credenciales + notificar |

**Regex completa:**
```
^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{24,}$
```

**Nota:** AWS IAM usa Access Keys, no passwords. Este policy aplica a consola web.

---

### 10. Cuentas Personales (Personal)

| Campo | Valor |
|-------|-------|
| **ID** | `personal-accounts` |
| **Mínimo caracteres** | 12 |
| **Requerido** | `^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{12,}$` |
| **Descripción regex** | 1 mayúscula, 1 minúscula, 1 número |
| **Rotación** | 180 días |
| **Notificación** | 30 días antes |
| **Acción al vencer** | Notificar (sin bloquear) |

**Regex completa:**
```
^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{12,}$
```

---

## Resumen de Rotación por Sistema

| Sistema | Rotación (días) | Notificación (días antes) | Acción al vencer | Mínimo caracteres |
|---------|----------------|---------------------------|-------------------|-------------------|
| Linux/SSH | 90 | 14 | Bloquear | 16 |
| Windows AD | 60 | 10 | Forzar cambio | 14 |
| Oracle DB | 45 | 7 | Bloquear | 18 |
| API REST | 30 | 5 | Revocar/regenerar | 32 |
| Web Apps | 30 | 7 | Forzar cambio | 20 |
| Email Corp | 60 | 14 | Bloquear | 16 |
| WiFi Corp | 90 | 14 | Cambiar en todos | 24 |
| VPN | 30 | 7 | Desconectar | 20 |
| Cloud | 30 | 7 | Revocar | 24 |
| Personal | 180 | 30 | Notificar | 12 |

---

## Flujo de Generación Automática

```
USUARIO hace clic en "Generar contraseña para [sistema]"
                    │
                    ▼
┌──────────────────────────────────────────────┐
│  1. Buscar política del sistema              │
│     (ej: linux-ssh)                          │
└──────────────────────────────────────────────┘
                    │
                    ▼
┌──────────────────────────────────────────────┐
│  2. Verificar que el usuario tiene acceso    │
│     a ese sistema (applicable_groups)        │
└──────────────────────────────────────────────┘
                    │
                    ▼
┌──────────────────────────────────────────────┐
│  3. Generar contraseña según política:       │
│     - Longitud: 20 caracteres                │
│     - Incluir: A-Z, a-z, 0-9, símbolos      │
│     - Excluir: ", ', \, `                    │
│     - Verificar contra regex                 │
└──────────────────────────────────────────────┘
                    │
                    ▼
┌──────────────────────────────────────────────┐
│  4. Calcular fecha de vencimiento:           │
│     - Fecha actual + días de rotación        │
│     - Ej: 2026-08-26 + 90 = 2026-11-24     │
└──────────────────────────────────────────────┘
                    │
                    ▼
┌──────────────────────────────────────────────┐
│  5. Guardar en vault local del usuario       │
│     con metadata:                            │
│     - system_id: "linux-ssh"                 │
│     - created_at: "2026-08-26"               │
│     - expires_at: "2026-11-24"               │
│     - rotation_days: 90                      │
│     - auto_generated: true                   │
└──────────────────────────────────────────────┘
                    │
                    ▼
┌──────────────────────────────────────────────┐
│  6. Registrar evento en servidor central     │
│     (log, no la contraseña)                  │
└──────────────────────────────────────────────┘
```

---

## Flujo de Validación

```
USUARIO ingresa o modifica una contraseña
                    │
                    ▼
┌──────────────────────────────────────────────┐
│  1. Identificar a qué sistema pertenece      │
│     (por tags o asignación manual)           │
└──────────────────────────────────────────────┘
                    │
                    ▼
┌──────────────────────────────────────────────┐
│  2. Obtener política del sistema             │
└──────────────────────────────────────────────┘
                    │
                    ▼
┌──────────────────────────────────────────────┐
│  3. Validar contra regex:                    │
│     - ¿Cumple longitud mínima?              │
│     - ¿Cumple caracteres requeridos?         │
│     - ¿No tiene caracteres prohibidos?       │
│     - ¿No contiene patrones prohibidos?      │
│     - ¿Tiene suficiente entropía?            │
└──────────────────────────────────────────────┘
                    │
              ┌─────┴─────┐
              │           │
         VÁLIDA      INVÁLIDA
              │           │
              ▼           ▼
┌─────────────────┐ ┌─────────────────┐
│ Guardar en vault │ │ Mostrar error:  │
│ Registrar evento │ │ - Qué falta     │
│ Notificar (opc)  │ │ - Política      │
└─────────────────┘ │ - Sugerencia    │
                    └─────────────────┘
```

---

## Master Password Rotation

### Configuración Global

```json
{
  "master_password_policy": {
    "min_length": 24,
    "required_regex": "^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[@$!%*?&#])[A-Za-z\\d@$!%*?&#]{24,}$",
    "rotation_days": 180,
    "warn_days_before": 30,
    "grace_period_days": 14,
    "prevent_reuse": 12,
    "action_on_expiry": "force_change",
    "allow_extension": true,
    "max_extensions": 1,
    "extension_days": 7
  }
}
```

### Flujo de Rotación de Master Password

```
DÍA 150 (30 días antes del vencimiento)
                    │
                    ▼
┌──────────────────────────────────────────────┐
│  Notificación por email:                     │
│  "Su master password vence en 30 días.       │
│   Cambie ahora para evitar interrupciones."  │
└──────────────────────────────────────────────┘
                    │
                    ▼
              Espera 14 días
                    │
                    ▼
DÍA 164 (16 días antes)
                    │
                    ▼
┌──────────────────────────────────────────────┐
│  Notificación desktop:                       │
│  "URGENTE: Su master password vence en       │
│   16 días. Cambie ahora."                    │
└──────────────────────────────────────────────┘
                    │
                    ▼
              Espera 16 días
                    │
                    ▼
DÍA 180 (vencimiento)
                    │
                    ▼
┌──────────────────────────────────────────────┐
│  Acción: force_change                        │
│  - App solicita nuevo master password        │
│  - Valida contra política                    │
│  - Verifica que no sea una de las últimas 12 │
│  - Re-cifra vault con nuevo KDF             │
│  - Registra evento en servidor central       │
│  - Notifica a admin                          │
└──────────────────────────────────────────────┘
```

---

## Implementación en Código

### Python: Generador de Contraseñas

```python
import secrets
import string
import re

class PasswordGenerator:
    def __init__(self, policy: dict):
        self.policy = policy

    def generate(self) -> str:
        """Genera contraseña según política del sistema."""
        length = self.policy['generation']['default_length']

        # Construir conjunto de caracteres
        chars = ''
        required = []

        if self.policy['generation']['include_uppercase']:
            chars += string.ascii_uppercase
            required.append(secrets.choice(string.ascii_uppercase))

        if self.policy['generation']['include_lowercase']:
            chars += string.ascii_lowercase
            required.append(secrets.choice(string.ascii_lowercase))

        if self.policy['generation']['include_numbers']:
            chars += string.digits
            required.append(secrets.choice(string.digits))

        if self.policy['generation']['include_symbols']:
            symbols = ''.join(
                c for c in string.punctuation
                if c not in self.policy['generation'].get('excluded_symbols', [])
            )
            chars += symbols
            required.append(secrets.choice(symbols))

        # Generar caracteres restantes
        remaining = length - len(required)
        password_chars = required + [secrets.choice(chars) for _ in range(remaining)]

        # Mezclar
        password_list = list(password_chars)
        secrets.SystemRandom().shuffle(password_list)
        password = ''.join(password_list)

        # Verificar que cumple regex
        regex = self.policy['password_policy']['required_regex']
        if not re.match(regex, password):
            # Regenerar si no cumple
            return self.generate()

        return password

    def validate(self, password: str) -> tuple[bool, list[str]]:
        """Valida contraseña contra política. Retorna (válido, lista_errores)."""
        errors = []

        # Longitud
        min_len = self.policy['password_policy']['min_length']
        max_len = self.policy['password_policy']['max_length']
        if len(password) < min_len:
            errors.append(f"Mínimo {min_len} caracteres")
        if len(password) > max_len:
            errors.append(f"Máximo {max_len} caracteres")

        # Regex
        regex = self.policy['password_policy']['required_regex']
        if not re.match(regex, password):
            errors.append(f"No cumple patrón: {self.policy['password_policy']['description_regex']}")

        # Caracteres prohibidos
        for char in self.policy['password_policy'].get('disallowed_chars', []):
            if char in password:
                errors.append(f"Carácter '{char}' no permitido")

        # Patrones prohibidos
        password_lower = password.lower()
        for pattern in self.policy['password_policy'].get('disallowed_patterns', []):
            if pattern.lower() in password_lower:
                errors.append(f"Patrón '{pattern}' no permitido")

        return (len(errors) == 0, errors)
```

### JavaScript: Verificador de Rotación

```javascript
class RotationChecker {
  constructor(vault, serverPolicies) {
    this.vault = vault;
    this.policies = serverPolicies;
  }

  checkAll() {
    const results = [];

    for (const entry of this.vault.entries) {
      const policy = this.policies.find(p =>
        p.system_id === entry.system_id
      );

      if (!policy || !policy.rotation.enabled) continue;

      const daysUntilExpiry = this.getDaysUntilExpiry(
        entry.expires_at
      );

      results.push({
        entry_id: entry.id,
        title: entry.title,
        system: entry.system_id,
        daysUntilExpiry,
        status: this.getStatus(daysUntilExpiry, policy),
        rotationDays: policy.rotation.days,
        warnDays: policy.rotation.warn_days_before,
        expiresAt: entry.expires_at
      });
    }

    return results.sort((a, b) => a.daysUntilExpiry - b.daysUntilExpiry);
  }

  getDaysUntilExpiry(expiresAt) {
    const now = new Date();
    const expiry = new Date(expiresAt);
    const diff = expiry - now;
    return Math.ceil(diff / (1000 * 60 * 60 * 24));
  }

  getStatus(daysUntilExpiry, policy) {
    if (daysUntilExpiry <= 0) return 'EXPIRED';
    if (daysUntilExpiry <= policy.rotation.warn_days_before) return 'WARNING';
    return 'OK';
  }

  getExpiringSoon(days = 14) {
    return this.checkAll().filter(r =>
      r.daysUntilExpiry <= days && r.status !== 'EXPIRED'
    );
  }

  getExpired() {
    return this.checkAll().filter(r => r.status === 'EXPIRED');
  }
}
```

---

## Configuración desde Admin Dashboard

### Pantalla de Edición de Política

```
╔══════════════════════════════════════════════════════════════╗
║  EDITAR POLÍTICA: Linux/SSH Servers                         ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Nombre: [Linux/SSH Servers                        ]         ║
║  Descripción: [Política para servidores Linux vía SSH ]     ║
║                                                              ║
║  ─── POLÍTICA DE CONTRASEÑA ─────────────────────────────── ║
║                                                              ║
║  Mínimo caracteres: [16]                                     ║
║  Máximo caracteres: [128]                                    ║
║                                                              ║
║  Regex requerida:                                            ║
║  [^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#]).{16,}$]  ║
║                                                              ║
║  [✓] Mayúsculas requeridas                                   ║
║  [✓] Minúsculas requeridas                                   ║
║  [✓] Números requeridos                                      ║
║  [✓] Símbolos requeridos                                     ║
║                                                              ║
║  Símbolos permitidos: [@$!%*?&#]                             ║
║  Caracteres prohibidos: ['"\`\ ]                             ║
║  Patrones prohibidos: [password, admin, bhu, root]           ║
║                                                              ║
║  ─── ROTACIÓN ───────────────────────────────────────────── ║
║                                                              ║
║  [✓] Rotación habilitada                                     ║
║  Días de rotación: [90]                                      ║
║  Avisar antes de: [14] días                                  ║
║  Período de gracia: [7] días                                 ║
║  Acción al vencer: [Bloquear + Notificar ▼]                 ║
║  Permitir extensión: [✓]                                     ║
║  Máximo extensiones: [2]                                     ║
║                                                              ║
║  ─── GENERACIÓN ─────────────────────────────────────────── ║
║                                                              ║
║  [✓] Generación automática habilitada                        ║
║  Longitud por defecto: [20]                                  ║
║  Incluir: [✓] Mayúsculas  [✓] Minúsculas                    ║
║           [✓] Números      [✓] Símbolos                     ║
║  Símbolos excluidos: ["'\`]                                 ║
║                                                              ║
║  ─── NOTIFICACIONES ─────────────────────────────────────── ║
║                                                              ║
║  Al crear:    [✓] Email  [ ] Desktop  [ ] SMS               ║
║  Al modificar:[✓] Email  [ ] Desktop  [ ] SMS               ║
║  Al vencer:   [✓] Email  [✓] Desktop  [ ] SMS               ║
║  Al expirar:  [✓] Email  [✓] Desktop  [ ] SMS               ║
║                                                              ║
║  ─── GRUPOS APLICABLES ─────────────────────────────────── ║
║                                                              ║
║  [✓] sysadmin    [✓] devops    [ ] developers               ║
║  [ ] analysts    [ ] hr        [ ] finance                  ║
║                                                              ║
║  ─── TAGS ──────────────────────────────────────────────── ║
║                                                              ║
║  [linux] [ssh] [servers] [production] [+ agregar]           ║
║                                                              ║
║         [Cancelar]  [Guardar Política]                       ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

---

## Integración con API Server

### Endpoint: Obtener Políticas

```python
# Flask API
@app.route('/api/v1/policies', methods=['GET'])
@require_auth
def get_policies():
    """Retorna políticas aplicables al usuario autenticado."""
    user_groups = get_user_groups(current_user)

    policies = Policy.query.filter(
        Policy.enabled == True,
        Policy.applicable_groups.contains(user_groups)
    ).all()

    return jsonify({
        'policies': [p.to_dict() for p in policies],
        'master_password_policy': get_master_password_policy()
    })
```

### Endpoint: Validar Contraseña

```python
@app.route('/api/v1/policies/validate', methods=['POST'])
@require_auth
def validate_password():
    """Valida una contraseña contra la política de un sistema."""
    data = request.json
    system_id = data['system_id']
    password = data['password']

    policy = Policy.query.filter_by(system_id=system_id).first()
    if not policy:
        return jsonify({'error': 'Política no encontrada'}), 404

    is_valid, errors = PasswordGenerator(policy.to_dict()).validate(password)

    return jsonify({
        'valid': is_valid,
        'errors': errors,
        'policy': policy.to_dict()
    })
```

### Endpoint: Generar Contraseña

```python
@app.route('/api/v1/policies/generate', methods=['POST'])
@require_auth
def generate_password():
    """Genera una contraseña según la política de un sistema."""
    data = request.json
    system_id = data['system_id']

    policy = Policy.query.filter_by(system_id=system_id).first()
    if not policy:
        return jsonify({'error': 'Política no encontrada'}), 404

    generator = PasswordGenerator(policy.to_dict())
    password = generator.generate()

    # Registrar evento (sin la contraseña)
    log_event('password_generated', {
        'user': current_user.id,
        'system': system_id,
        'length': len(password)
    })

    return jsonify({
        'password': password,
        'expires_at': calculate_expiry(policy.rotation.days),
        'policy': policy.to_dict()
    })
```

---

## Monitoreo de Cumplimiento

### Dashboard de Cumplimiento

```
╔══════════════════════════════════════════════════════════════╗
║  DASHBOARD DE CUMPLIMIENTO DE POLÍTICAS                       ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Total contraseñas: 347                                      ║
║  Cumplen política:  312 (89.9%)                              ║
║  No cumplen:        35 (10.1%)                               ║
║                                                              ║
║  ─── POR SISTEMA ────────────────────────────────────────── ║
║                                                              ║
║  Linux/SSH     ████████████████████░░░  85% (51/60)         ║
║  Windows AD    █████████████████████░░  92% (83/90)         ║
║  Oracle DB     ██████████████████████░  96% (24/25)         ║
║  API REST      ████████████████████░░░  88% (44/50)         ║
║  Web Apps      ██████████████████████░  97% (29/30)         ║
║  Email Corp    ████████████████████░░░  87% (26/30)         ║
║  WiFi Corp     ████████████████████░░░  90% (18/20)         ║
║  VPN           █████████████████████░░  93% (28/30)         ║
║  Cloud         ████████████████████░░░  89% (16/18)         ║
║  Personal      ███████████████████████ 100% (19/19)         ║
║                                                              ║
║  ─── POR ESTADO ────────────────────────────────────────── ║
║                                                              ║
║  Vigentes:      285 (82.1%)  🟢                              ║
║  Por vencer:     27 (7.8%)   🟡 (próximos 14 días)          ║
║  Vencidas:       12 (3.5%)   🔴                              ║
║  No válidas:     23 (6.6%)   🔴 (no cumple política)        ║
║                                                              ║
║  ─── ÚLTIMAS 24 HORAS ──────────────────────────────────── ║
║                                                              ║
║  Contraseñas generadas:     15                               ║
║  Contraseñas rotadas:        8                               ║
║  Intentos fallidos:          3                               ║
║  Notificaciones enviadas:   42                               ║
║                                                              ║
║         [Exportar Reporte]  [Ver Alertas]                     ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

---

> **Actividad**: Diseña una política de contraseñas para 5 sistemas de tu empresa/institución. Define regex, rotación, generación y notificaciones para cada uno. Implementa el validador en Python o JavaScript.
