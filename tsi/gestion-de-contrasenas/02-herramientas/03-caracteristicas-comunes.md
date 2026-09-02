# 2.3 Características Comunes de Herramientas de Gestión de Contraseñas

## Funcionalidades Esenciales (Must-Have)

### 1. Generador de Contraseñas Seguras

```
┌─────────────────────────────────────────────────────┐
│            GENERADOR DE CONTRASEÑAS                  │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Longitud: [====●============] 24 caracteres       │
│                                                     │
│  Tipos de caracteres:                               │
│  [✓] Mayúsculas (A-Z)                             │
│  [✓] Minúsculas (a-z)                             │
│  [✓] Números (0-9)                                │
│  [✓] Símbolos (!@#$%^&*)                          │
│                                                     │
│  Opciones avanzadas:                                │
│  [✓] Evitar caracteres ambiguos (0, O, l, 1)     │
│  [✓] Evitar caracteres repetidos consecutivos    │
│  [✓] Incluir al menos uno de cada tipo           │
│  [ ] Pasphrase (palabras concatenadas)           │
│                                                     │
│  Resultado: Kx$9mP#vL2nQ!wR7tY4jB8              │
│  Entropía: 158.4 bits ✅                          │
│  [Copiar] [Regenerar] [Guardar en vault]          │
│                                                     │
└─────────────────────────────────────────────────────┘
```

**Parámetros Recomendados:**

| Parámetro | Mínimo | Recomendado | Excelente |
|-----------|--------|-------------|-----------|
| Longitud | 12 | 16 | 20-24 |
| Entropía | 60 bits | 80 bits | 128+ bits |
| Mayúsculas | 1 | 2+ | Todas |
| Minúsculas | 1 | 2+ | Todas |
| Números | 1 | 2+ | Todos |
| Símbolos | 1 | 2+ | Todos |
| Sin repetidos | No | Sí | Sí |
| Sin ambiguos | No | Sí | Sí |

### 2. Almacenamiento Seguro (Vault)

```
VAULT ESTRUCTURA:
├── 🏠 Vault Personal
│   ├── 📁 Internet
│   │   ├── 📄 Google (gmail.com)
│   │   ├── 📄 Facebook
│   │   └── 📄 Amazon
│   ├── 📁 Redes Corporativas
│   │   ├── 📄 LinkedIn Company
│   │   └── 📄 Twitter BHU
│   ├── 📁 Banca
│   │   ├── 📄 BROU
│   │   └── 📄 Itaú
│   ├── 📁 Email
│   │   ├── 📄 Outlook BHU
│   │   └── 📄 Gmail personal
│   ├── 📁 Servicios
│   │   ├── 📄 Hosting UY
│   │   └── 📄 Dominio .uy
│   └── 📁 Notas Seguras
│       └── 📄 Códigos de recuperación
│
├── 🏢 BHU (Organización)
│   ├── 📁 Colección: General
│   │   ├── 📄 WiFi Oficina
│   │   └── 📄 Impresora Principal
│   ├── 📁 Colección: Ventas
│   │   ├── 📄 CRM Salesforce
│   │   └── 📄 Herramienta Email
│   └── 📁 Colección: TI
│       ├── 📄 Server Principal
│       └── 📄 API GitHub
│
└── 🔐 Vault Oculto (si soporta)
    └── 📁 Emergencia
        └── 📄 Códigos de recuperación
```

### 3. AutoFill (Autocompletado)

```
FLUJO DE AUTOFILL:

1. Usuario visita sitio web
   │
   ▼
2. Extensión detecta campo de contraseña
   │
   ▼
3. Icono de Vaultwarden aparece en campo
   │
   ▼
4. Click en icono → Lista de credenciales para ese dominio
   │
   ▼
5. Selección → Credenciales se autocompletan
   │
   ▼
6. Si 2FA requerido → Prompt para código TOTP
```

### 4. Sincronización Multi-Dispositivo

```
┌──────────┐    ┌──────────┐    ┌──────────┐
│   PC     │    │ Servidor │    │  Móvil   │
│ Windows  │◄──►│Vaultwarden│◄──►│  iOS/    │
│          │    │          │    │ Android  │
└──────────┘    └──────────┘    └──────────┘
     │                              │
     ▼                              ▼
┌──────────┐                  ┌──────────┐
│  Navegador│                  │  App     │
│  Chrome/  │                  │  Nativa  │
│  Firefox  │                  │          │
└──────────┘                  └──────────┘

Sincronización:
- Instantánea (WebSocket push)
- Offline: caché local + sync al reconectar
- Conflicso: última escritura gana (con merge)
```

### 5. Compartición Segura

```
COMPARTIR CONTRASEÑA:

┌─────────────┐                 ┌─────────────┐
│  Usuario A  │                 │  Usuario B  │
│  (origen)   │                 │  (destino)  │
└──────┬──────┘                 └──────┬──────┘
       │                               │
       │  1. Selecciona contraseña    │
       │  2. Elige colección/grupo    │
       │  3. Asigna permisos          │
       │  4. Confirma                 │
       ▼                               │
┌──────────────────────────────────────────┐
│           COLECCIÓN COMPARTIDA           │
│  ┌──────────────────────────────────┐   │
│  │  📄 Contraseña de CRM           │   │
│  │  - Creador: Admin               │   │
│  │  - Acceso: Ventas, TI           │   │
│  │  - Permisos: Solo lectura       │   │
│  │  - Cifrado: E2E (mismo vault)   │   │
│  └──────────────────────────────────┘   │
│                                          │
│  Permisos disponibles:                   │
│  - Solo lectura                         │
│  - Lectura + Ocultar                    │
│  - Edición (solo algunas)               │
│  - Administración completa              │
└──────────────────────────────────────────┘
```

## Funcionalidades Avanzadas (Nice-to-Have)

### 6. Verificación de Brechas (HIBP)

```
┌─────────────────────────────────────────────────────┐
│         VERIFICACIÓN HIBP                            │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Has Been Pwned Check:                              │
│                                                     │
│  Tu contraseña: kx$9mP#vL2nQ!wR7tY4jB8            │
│  Hash SHA-1: 3B92A4B1C7D8E9F0A1B2C3D4E5F6A7B8C9D0│
│                                                     │
│  API HIBP:                                          │
│  GET /range/A1B2C...                                │
│  Respuesta: No found ✅                             │
│                                                     │
│  Resultado: ✅ Contraseña segura                     │
│  Apariciones en brechas: 0                          │
│  Última verificación: 2024-01-15                    │
│                                                     │
│  Verificación automática:                           │
│  [✓] Al guardar contraseña                         │
│  [✓] Periódicamente (cada 30 días)                 │
│  [✓] Al importar desde otro gestor                 │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### 7. Historial de Contraseñas

```
HISTORIAL DE CONTRASEÑA "Google (gmail.com)":

┌──────┬─────────────┬──────────────┬───────────┐
│ #    │ Fecha       │ Contraseña   │ Acción    │
├──────┼─────────────┼──────────────┼───────────┤
│ 5    │ 2024-01-15  │ Kx$9mP#vL2  │ Actual    │
│ 4    │ 2023-10-01  │ M8nQ!wR7tY  │ Rotación  │
│ 3    │ 2023-07-15  │ P9kL$2mN#x  │ Rotación  │
│ 2    │ 2023-04-01  │ J5hG!3fD@s  │ Brecha    │
│ 1    │ 2023-01-15  │ AbCd1234!   │ Creación  │
└──────┴─────────────┴──────────────┴───────────┘

Importancia:
- Auditar quién cambió qué y cuándo
- Recuperar contraseña anterior si error
- Detectar accesos no autorizados
```

### 8. Notificaciones y Auditoría

```
SISTEMA DE NOTIFICACIONES:

┌─────────────────────────────────────────────────────┐
│  📧 Notificación: "Contraseña compartida"           │
│  Fecha: 2024-01-15 14:30                           │
│  Usuario: Admin → Juan Pérez                       │
│  Contraseña: CRM Salesforce                        │
│  Colección: Ventas                                 │
│  Acción: Compartida con permiso de lectura         │
├─────────────────────────────────────────────────────┤
│  📧 Notificación: "Contraseña débil detectada"      │
│  Fecha: 2024-01-15 15:00                           │
│  Usuario: María García                             │
│  Contraseña: Facebook (personal)                   │
│  Entropía: 42 bits (mínimo: 60)                   │
│  Acción: Recomendada cambio                        │
├─────────────────────────────────────────────────────┤
│  📧 Notificación: "Brecha detectada"               │
│  Fecha: 2024-01-15 16:00                           │
│  Usuario: Carlos López                             │
│  Contraseña: LinkedIn (personal)                   │
│  Brecha: Adobe 2023                               │
│  Acción: Cambio inmediato recomendado              │
└─────────────────────────────────────────────────────┘
```

### 9. Recuperación de Emergencia

```
OPCIONES DE RECUPERACIÓN:

┌─────────────────────────────────────────────────────┐
│  1. CONTRASEÑA DE EMERGENCIA                        │
│     - 2da contraseña maestra                        │
│     - Solo para emergencias                         │
│     - Almacenada en vault físico seguro             │
│                                                     │
│  2. RECUPERACIÓN POR CONTACTO                       │
│     - Designar 2 contactos de confianza             │
│     - Juntos pueden desbloquear vault               │
│     - Shamir's Secret Sharing (si soporta)         │
│                                                     │
│  3. BACKUP CIFRADO                                  │
│     - Exportar vault cifrado                        │
│     - Almacenar en USB + cloud cifrado             │
│     - Documentar procedimiento de importación       │
│                                                     │
│  4. BREAK-GLASS (Empresas)                          │
│     - Cuenta administrativa de emergencia           │
│     - Acceso solo con 2 admins                      │
│     - Documentado y en sobre sellado               │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### 10. Integración con Herramientas

| Herramienta | Integración | Descripción |
|-------------|-------------|-------------|
| **Navegadores** | Extensión | Chrome, Firefox, Safari, Edge |
| **Terminal** | CLI | `bw` (Bitwarden CLI), `vaultwarden-cli` |
| **Git** | .gitignore | No commitear vaults |
| **CI/CD** | Secrets | GitHub Actions, GitLab CI |
| **IDE** | Plugin | VS Code, JetBrains |
| **SO** | Biometría | Windows Hello, Touch ID |
| **Móvil** | AutoFill iOS/Android | Sistema nativo |
| **LDAP/AD** | Sync | Sincronización de usuarios |

## Checklist de Evaluación

Al evaluar una herramienta de gestión de contraseñas, verifica:

| # | Característica | KeePassXC | Vaultwarden | Bitwarden |
|---|---------------|-----------|-------------|-----------|
| 1 | Generador configurable | ✅ | ✅ | ✅ |
| 2 | Cifrado E2E | ✅ | ✅ | ✅ |
| 3 | 2FA/TOTP | ✅ | ✅ | ✅ |
| 4 | WebAuthn/FIDO2 | ✅ | ✅ | ✅ |
| 5 | Autofill navegador | ✅ (plugin) | ✅ | ✅ |
| 6 | Sincronización auto | ❌ | ✅ | ✅ |
| 7 | Compartir contraseñas | ❌ | ✅ | ✅ |
| 8 | Organizaciones | ❌ | ✅ | ✅ |
| 9 | Verificación HIBP | ✅ | ✅ | ✅ |
| 10 | Historial | ✅ | ✅ | ✅ |
| 11 | Auditoría | ❌ | ✅ | ✅ (pago) |
| 12 | API | ❌ | ✅ | ✅ |
| 13 | Biometría | ❌ | ✅ | ✅ |
| 14 | Adjuntos cifrados | ❌ | ✅ | ✅ (pago) |
| 15 | Exportación | ✅ | ✅ | ✅ |

---

> **Actividad**: Para cada característica listada, evalúa su importancia en una empresa de 30 personas. Clasifícalas en "imprescindible", "deseable" y "opcional".
