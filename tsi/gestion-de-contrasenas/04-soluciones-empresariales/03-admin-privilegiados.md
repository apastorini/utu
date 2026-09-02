# 4.3 Gestión de Administradores con Privilegiados

## Jerarquía de Acceso

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    JERARQUÍA DE ACCESO BHU                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  NIVEL 0: BREAK-GLASS (Emergencia)                                     │
│  ├── Acceso: Múltiples vaults de emergencia                            │
│  ├── Usuarios: 2 personas designadas (CEO + CTO)                       │
│  ├── Activación: Solo con 2 de 3 presentes                            │
│  └── Almacenamiento: Sobre sellado en caja fuerte + USB cifrado       │
│                                                                         │
│  NIVEL 1: SUPER ADMIN                                                  │
│  ├── Acceso: Control total del sistema Vaultwarden                     │
│  ├── Usuarios: 1-2 personas (CTO + Senior IT)                         │
│  ├── Permisos: Admin panel completo                                    │
│  │   ├── Crear/eliminar organizaciones                                │
│  │   ├── Gestionar todos los usuarios                                 │
│  │   ├── Configurar políticas globales                                │
│  │   ├── Ver todos los logs de auditoría                              │
│  │   └── Configurar integraciones (LDAP, SMTP, etc.)                  │
│  └── Restricciones:                                                    │
│      ├── Nunca usar como cuenta diaria                                │
│      ├── Login solo desde terminal seguro                             │
│      ├── 2FA con hardware key obligatoria                             │
│      └── Timeout: 15 minutos                                          │
│                                                                         │
│  NIVEL 2: ADMIN                                                        │
│  ├── Acceso: Gestión de usuarios y colecciones                         │
│  ├── Usuarios: 3-5 personas (IT staff)                                │
│  ├── Permisos:                                                         │
│  │   ├── Agregar/eliminar usuarios                                     │
│  │   ├── Crear/modificar colecciones                                  │
│  │   ├── Asignar permisos a usuarios                                  │
│  │   ├── Ver logs de auditoría (no modificar)                         │
│  │   └── Configurar notificaciones                                    │
│  └── Restricciones:                                                    │
│      ├── No puede eliminar la organización                            │
│      ├── No puede modificar políticas globales                        │
│      └── Acciones requieren 2FA                                       │
│                                                                         │
│  NIVEL 3: MANAGER (por colección)                                     │
│  ├── Acceso: Gestión de su colección                                  │
│  ├── Usuarios: 1 por departamento                                     │
│  ├── Permisos:                                                         │
│  │   ├── Agregar/eliminar miembros de su colección                    │
│  │   ├── Crear/modificar entradas en su colección                     │
│  │   └── Compartir dentro de su colección                             │
│  └── Restricciones:                                                    │
│      ├── No puede ver otras colecciones                               │
│      └── No puede modificar permisos de otros managers                │
│                                                                         │
│  NIVEL 4: USER                                                         │
│  ├── Acceso: Uso de contraseñas asignadas                             │
│  ├── Usuarios: Empleados generales                                    │
│  ├── Permisos:                                                         │
│  │   ├── Usar contraseñas asignadas                                   │
│  │   ├── Crear entradas personales                                    │
│  │   └── Compartir dentro de su colección (si permite)               │
│  └── Restricciones:                                                    │
│      ├── No puede modificar permisos                                  │
│      └── No puede ver otras colecciones                               │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Cuentas de Servicio (Service Accounts)

### ¿Qué son las Cuentas de Servicio?

Son cuentas no-humanas utilizadas por sistemas, aplicaciones y automatizaciones para acceder a credenciales de forma programática.

```
EJEMPLOS DE CUENTAS DE SERVICIO:
├── CI/CD Pipeline → Necesita API keys para despliegue
├── Script de backup → Necesita acceso para respaldar
├── Monitor de uptime → Necesita verificar servicios
├── Aplicación web → Necesita credenciales de BD
├── Integración LDAP → Necesita bind DN
└── Webhook receiver → Necesita verificar eventos
```

### Registro de Cuentas de Servicio

```markdown
| # | Nombre | Propósito | Permisos | Rotación | Responsable | Estado |
|---|--------|-----------|----------|----------|-------------|--------|
| 1 | svc-cicd | Pipeline CI/CD GitHub | Lectura colección TI | 90 días | DevOps | Activo |
| 2 | svc-backup | Script de respaldo | Lectura todas colecciones | 180 días | IT Admin | Activo |
| 3 | svc-monitor | Monitoreo de uptime | Solo endpoint alive | 365 días | IT Admin | Activo |
| 4 | svc-ldap-sync | Sincronización LDAP | Lectura/escritura usuarios | 180 días | IT Admin | Activo |
| 5 | svc-webhook | Notificaciones | Escritura logs | 90 días | DevOps | Activo |
| 6 | svc-pam | Gestión privilegiada | Admin colección TI | 60 días | CTO | Activo |
```

### Ejemplo: Service Account para CI/CD

```
ENTRADA EN VAULTWARDEN:
┌─────────────────────────────────────────────────────┐
│  Nombre: svc-cicd-github                           │
│  Tipo: Service Account                             │
│  Usuario: svc-cicd@bhu.uy                          │
│  Contraseña: [generada por VW, 32 caracteres]      │
│                                                     │
│  Notas:                                             │
│  - Propósito: Pipeline CI/CD                        │
│  - Permisos: Solo lectura colección TI              │
│  - Rotación: Cada 90 días                          │
│  - Última rotación: 2024-01-15                     │
│  - Próxima rotación: 2024-04-15                    │
│  - Responsable: DevOps Team                        │
│  - Limitaciones:                                   │
│    * No puede modificar usuarios                   │
│    * No puede eliminar colecciones                 │
│    * Solo accede a colección TI                    │
│    * Rate limit: 100 req/hora                      │
│                                                     │
│  Configuración en GitHub Actions:                  │
│  VW_API_KEY: ${{ secrets.VAULTWARDEN_API_KEY }}   │
│  VW_SERVER: https://vaultwarden.bhu.uy            │
│                                                     │
│  Logs de uso:                                       │
│  - 2024-01-15 10:00: checkout credentials        │
│  - 2024-01-15 10:01: read API key Stripe         │
│  - 2024-01-15 10:05: read DB credentials          │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### Script de Rotación Automática de Service Accounts

```powershell
# rotate-service-accounts.ps1
# Rotación automática de credenciales de servicio

param(
    [string]$VaultwardenUrl = "https://vaultwarden.bhu.uy",
    [string]$AdminToken = $env:VW_ADMIN_TOKEN,
    [int]$RotationDays = 90
)

$ErrorActionPreference = "Stop"

function Get-ServiceAccounts {
    param([string]$Url, [string]$Token)
    
    $headers = @{
        "Authorization" = "Bearer $Token"
        "Content-Type" = "application/json"
    }
    
    $response = Invoke-RestMethod -Uri "$Url/api/ciphers" `
        -Headers $headers -Method GET
    
    return $response.data | Where-Object { 
        $_.type -eq 1 -and $_.name -like "svc-*" 
    }
}

function Rotate-ServiceAccount {
    param(
        [string]$Url,
        [string]$Token,
        [object]$Account,
        [int]$MaxAge
    )
    
    $lastRotation = [DateTime]::Parse($Account.creationDate)
    $daysSinceRotation = ((Get-Date) - $lastRotation).Days
    
    if ($daysSinceRotation -ge $MaxAge) {
        Write-Host "Rotating: $($Account.name) (last: $daysSinceRotation days ago)" `
            -ForegroundColor Yellow
        
        # Generar nueva contraseña
        $newPassword = -join ((48..57) + (65..90) + (97..122) + (33,35,36,37,38,42) | 
            Get-Random -Count 32 | ForEach-Object {[char]$_})
        
        # Actualizar en Vaultwarden
        $headers = @{
            "Authorization" = "Bearer $Token"
            "Content-Type" = "application/json"
        }
        
        $updateData = @{
            id = $Account.id
            login = @{
                username = $Account.login.username
                password = $newPassword
            }
            name = $Account.name
        } | ConvertTo-Json
        
        Invoke-RestMethod -Uri "$Url/api/ciphers/$($Account.id)" `
            -Headers $headers -Method PUT -Body $updateData
        
        Write-Host "  ✅ Rotated: $($Account.name)" -ForegroundColor Green
        
        # Actualizar timestamp de rotación
        # (En producción, guardar en vault o base de datos)
        
        return @{
            Account = $Account.name
            NewPassword = $newPassword
            RotatedAt = Get-Date
        }
    } else {
        Write-Host "  ⏭️ Skip: $($Account.name) ($($MaxAge - $daysSinceRotation) days remaining)" `
            -ForegroundColor Gray
        return $null
    }
}

# =====================
# PRINCIPAL
# =====================

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "  ROTACIÓN DE SERVICE ACCOUNTS            " -ForegroundColor Cyan
Write-Host "  $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

$accounts = Get-ServiceAccounts -Url $VaultwardenUrl -Token $AdminToken
Write-Host "Service accounts encontrados: $($accounts.Count)"

$rotated = @()
foreach ($account in $accounts) {
    $result = Rotate-ServiceAccount -Url $VaultwardenUrl -Token $AdminToken `
        -Account $account -MaxAge $RotationDays
    if ($result) { $rotated += $result }
}

Write-Host "`n=========================================" -ForegroundColor Cyan
Write-Host "  RESUMEN                               " -ForegroundColor Cyan
Write-Host "  Total accounts: $($accounts.Count)" -ForegroundColor Cyan
Write-Host "  Rotated: $($rotated.Count)" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

# Enviar reporte por email
if ($rotated.Count -gt 0) {
    $report = $rotated | ForEach-Object { 
        "$($_.Account): rotado a las $($_.RotatedAt)" 
    } | Out-String
    
    Send-MailMessage -From "vaultwarden@bhu.uy" `
        -To "admin@bhu.uy" `
        -Subject "[Vaultwarden] Service Accounts Rotation Report" `
        -Body $report `
        -SmtpServer "smtp.gmail.com" `
        -Port 587 -UseSsl
}
```

## Gestión de Credenciales de Emergencia (Break-Glass)

### Concepto Break-Glass

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    BREAK-GLASS ACCOUNTS                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ¿QUÉ SON?                                                             │
│  Cuentas de emergencia que permiten acceso al sistema cuando las       │
│  credenciales normales no funcionan (olvido master password,           │
│  compromiso de cuenta admin, desastre自然).                            │
│                                                                         │
│  ¿CUÁNDO SE USAN?                                                      │
│  ├── Master password de admin perdida                                  │
│  ├── Cuenta admin comprometida                                         │
│  ├── 2FA no disponible (hardware key perdida)                         │
│  ├── Servidor principal inaccesible                                   │
│  └── Emergencia de seguridad                                           │
│                                                                         │
│  ¿QUIÉN CONTROLA?                                                      │
│  ├── 2 personas designadas (CEO + CTO)                                │
│  ├── Ambas deben estar presentes                                       │
│  ├── Documento en sobre sellado en caja fuerte                        │
│  └── Copia digital cifrada en USB en otra ubicación                   │
│                                                                         │
│  PROTECCIONES:                                                          │
│  ├── Cuenta limitada a emergencias específicas                         │
│  ├── Logging completo de cada uso                                      │
│  ├── Notificación inmediata a todo el equipo directivo                 │
│  ├── Requiere justificación escrita                                    │
│  └── Revisión post-incidente obligatoria                               │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Procedimiento Break-Glass

```
PASO 1: VERIFICAR EMERGENCIA
├── ¿Es realmente una emergencia?
├── ¿Se agotaron todas las alternativas?
├── ¿Hay al menos 2 autorizadas presentes?
└── Documentar justificación

PASO 2: ACCEDER AL SOBRE
├── Localizar sobre sellado en caja fuerte
├── Verificar sellos intactos
├── Ambas personas firmar acta de apertura
└── Registrar fecha, hora y motivo

PASO 3: EJECUTAR RECUPERACIÓN
├── Seguir instrucciones del sobre
├── Usar credenciales de emergencia
├── Realizar acción necesaria
└── Documentar cada paso

PASO 4: CERRAR EMERGENCIA
├── Cambiar todas las credenciales comprometidas
├── Revocar sesiones activas
├── Verificar integridad del sistema
├── Actualizar sobre con nuevas credenciales
├── Re-sellar y devolver a caja fuerte
└── Crear reporte de incidente

PASO 5: POST-INCIDENTE
├── Reunión de revisión (within 48h)
├── Actualizar procedimientos si es necesario
├── Capacitación adicional si fue error humano
└── Mejoras de prevención
```

### Contenido del Sobre Break-Glass

```
CONTENIDO DEL SOBRE (Sellado):
═══════════════════════════════════════════════════
CREDENCIALES DE EMERGENCIA - BHU VAULTWARDEN
═══════════════════════════════════════════════════

CUENTA DE EMERGENCIA:
  Email: breakglass-emergency@bhu.uy
  Master Password: [GENERAR 32+ CARACTERES]

ADMIN TOKEN:
  [GENERAR TOKEN SEGURO]

PANEL ADMIN:
  URL: https://vaultwarden.bhu.uy/admin
  Token: [ADMIN TOKEN]

INSTRUCCIONES:
1. Ir a https://vaultwarden.bhu.uy/admin
2. Ingresar Admin Token
3. Ir a Users
4. Seleccionar usuario afectado
5. Click "Reset Password"
6. Crear nueva master password
7. Comunicar nueva contraseña al usuario
8. Documentar en acta

CONTACTOS AUTORIZADOS:
  - CEO: [Nombre] - [Teléfono]
  - CTO: [Nombre] - [Teléfono]
  - IT Admin: [Nombre] - [Teléfono]

CÓDIGO DE VERIFICACIÓN:
  [Código de 6 dígitos para verificar identidad]

FECHA DE ÚLTIMA ACTUALIZACIÓN: [FECHA]
PRÓXIMA REVISIÓN: [FECHA + 90 días]
═══════════════════════════════════════════════════
```

## Auditoría de Administradores

### Log de Auditoría Obligatorio

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    AUDITORÍA DE ADMINISTRADORES                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  EVENTOS QUE SE REGISTRAN:                                             │
│  ├── Login/logout de admin                                             │
│  ├── Cambios en configuración global                                   │
│  ├── Creación/eliminación de usuarios                                  │
│  ├── Cambios en permisos                                               │
│  ├── Acceso a logs de auditoría                                        │
│  ├── Uso de break-glass account                                        │
│  ├── Exportación de datos                                              │
│  ├── Cambios en políticas de seguridad                                 │
│  └── Cualquier acción irreversible                                     │
│                                                                         │
│  FORMATO DEL LOG:                                                       │
│  [Timestamp] [Admin] [Acción] [Detalles] [IP] [Resultado]            │
│                                                                         │
│  EJEMPLO:                                                              │
│  2024-01-15 14:30:00 | admin@bhu.uy | CREATE_USER |                  │
│  juan.perez@bhu.uy added to Ventas | 192.168.1.50 | SUCCESS          │
│                                                                         │
│  RETENCIÓN: 2 años mínimo                                              │
│  ALMACENAMIENTO: Base de datos separada + exportación mensual         │
│  ACCESO: Solo super admin puede ver logs completos                     │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Dashboard de Auditoría

```
┌─────────────────────────────────────────────────────────────────────────┐
│  DASHBOARD DE AUDITORÍA - VAULTWARDEN BHU                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  📊 RESUMEN HOY                                                         │
│  ├── Logins exitosos: 45                                               │
│  ├── Logins fallidos: 3 ⚠️                                             │
│  ├── Contraseñas usadas: 120                                           │
│  ├── Contraseñas cambiadas: 5                                          │
│  ├── Nuevos dispositivos: 2                                            │
│  └── 2FA habilitado: 1                                                 │
│                                                                         │
│  🚨 ALERTAS ACTIVAS                                                    │
│  ├── Login fallido desde IP desconocida (192.168.5.100)               │
│  │   Usuario: admin@bhu.uy                                            │
│  │   Hora: 14:30                                                      │
│  │   Acción: Verificar si es legítimo                                │
│  │                                                                    │
│  ├── 2FA deshabilitado por usuario                                    │
│  │   Usuario: test@bhu.uy                                            │
│  │   Hora: 14:15                                                      │
│  │   Acción: Re-habilitar y verificar                                │
│  │                                                                    │
│  └── Exportación de vault detectada                                   │
│      Usuario: maria.garcia@bhu.uy                                    │
│      Hora: 13:45                                                      │
│      Acción: Verificar motivo                                         │
│                                                                         │
│  📈 TENDENCIA SEMANAL                                                  │
│  ├── Lunes:    ████████████ 89%                                       │
│  ├── Martes:   ███████████ 82%                                        │
│  ├── Miércoles:████████████ 91%                                       │
│  ├── Jueves:   ████████████ 88%                                       │
│  ├── Viernes:  ███████████ 84%                                        │
│  ├── Sábado:   ██ 12% (fines de semana bajo uso)                     │
│  └── Domingo:  █ 5%                                                   │
│                                                                         │
│  🔍 ÚLTIMOS 10 EVENTOS                                                │
│  ├── 14:32 | login_success | admin@bhu.uy | 192.168.1.10            │
│  ├── 14:30 | password_used | juan.perez@bhu.uy | GitHub             │
│  ├── 14:28 | login_success | maria.garcia@bhu.uy | 192.168.1.20    │
│  ├── 14:25 | password_changed | carlos.lopez@bhu.uy | CRM          │
│  ├── 14:20 | new_device | ana.rodriguez@bhu.uy | iPhone 15         │
│  ├── 14:15 | login_failed | admin@bhu.uy | 192.168.5.100 ⚠️        │
│  ├── 14:10 | password_shared | juan.perez@bhu.uy → maria.garcia    │
│  ├── 14:05 | 2fa_enabled | pedro.sanchez@bhu.uy | TOTP             │
│  ├── 14:00 | login_success | laura.fernandez@bhu.uy | 192.168.1.30│
│  └── 13:55 | password_used | admin@bhu.uy | WiFi Oficina           │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Gestión de API Keys de Administradores

### Políticas para API Keys de Admin

| Requisito | Valor |
|-----------|-------|
| **Almacenamiento** | Vaultwarden (nunca en código o archivos) |
| **Rotación** | 30 días (más frecuente que usuarios estándar) |
| **Permisos** | Mínimos necesarios (least privilege) |
| **Rate limiting** | 50 req/hora (vs 100 de usuarios normales) |
| **Monitoreo** | Cada llamada loggeada |
| **Revocación** | Inmediata si comprometida |
| **Uso** | Solo para automatizaciones críticas |

### Ejemplo: API Key de Admin para Scripts

```
ENTRADA EN VAULTWARDEN:
┌─────────────────────────────────────────────────────┐
│  Nombre: admin-api-key-readonly                    │
│  Tipo: API Key (Admin)                             │
│  Key: vw_admin_readonly_xxxxxxxxxxxxxxxx           │
│                                                     │
│  Notas:                                             │
│  - Permisos: Solo lectura (no escritura)           │
│  - Alcance: Todas las colecciones                  │
│  - Uso: Scripts de auditoría y reportes            │
│  - Rotación: Cada 30 días                         │
│  - Rate limit: 50 req/hora                        │
│  - IP whitelist: Solo desde servidor de monitoreo  │
│                                                     │
│  Uso en script:                                     │
│  $env:VW_API_KEY = "vw_admin_readonly_xxx"        │
│  Invoke-RestMethod -Uri "$url/api/ciphers" `       │
│    -Headers @{Authorization="Bearer $env:VW_API_KEY"}│
│                                                     │
└─────────────────────────────────────────────────────┘
```

## Resumen de Mejores Prácticas

| # | Mejor Práctica | Prioridad |
|---|---------------|-----------|
| 1 | Usar cuentas de admin solo para administración | Crítica |
| 2 | 2FA con hardware key obligatoria para admin | Crítica |
| 3 | Timeout de sesión: 15 minutos | Alta |
| 4 | Logging completo de acciones de admin | Alta |
| 5 | Rotación de credenciales de admin: 30 días | Alta |
| 6 | IP whitelist para acceso admin | Media |
| 7 | Separar cuentas personales y de admin | Alta |
| 8 | Break-glass account con procedure documentado | Crítica |
| 9 | Auditoría periódica de permisos de admin | Alta |
| 10 | Capacitación continua en seguridad | Media |

---

> **Actividad**: Diseña un procedimiento de break-glass para tu empresa. Define: quiénes son los titulares, qué credenciales se guardan, dónde se almacenan, y cómo se verifica la emergencia.
