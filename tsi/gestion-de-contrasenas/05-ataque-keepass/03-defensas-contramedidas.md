# 5.3 Defensas y Contramedidas

## Capas de Defensa para Gestores de Contraseñas

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    DEFENSA EN PROFUNDIDAD                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  CAPA 1: CONTRASEÑA MAESTRA (Primera línea)                           │
│  ├── Longitud ≥20 caracteres                                           │
│  ├── Entropía ≥80 bits                                                 │
│  ├── No reuse en otros sitios                                          │
│  ├── Verificar contra HIBP                                              │
│  └── No compartir jamás                                                │
│                                                                         │
│  CAPA 2: KDF (Key Derivation Function)                                │
│  ├── Argon2id con ≥64MB memoria                                        │
│  ├── ≥3 iteraciones                                                    │
│  ├── Paralelismo ≥4                                                    │
│  └── Salt único por vault                                              │
│                                                                         │
│  CAPA 3: CIFRADO DEL VAULT                                            │
│  ├── AES-256-GCM (autenticado)                                        │
│  ├── Clave derivada de master password                                 │
│  └── Cifrado completo del vault                                        │
│                                                                         │
│  CAPA 4: AUTENTICACIÓN ADICIONAL                                      │
│  ├── 2FA/TOTP                                                          │
│  ├── WebAuthn/FIDO2 (hardware key)                                    │
│  ├── Biometría (Windows Hello)                                        │
│  └── PIN local (clientes)                                              │
│                                                                         │
│  CAPA 5: PROTECCIÓN DEL ARCHIVO                                       │
│  ├── Almacenamiento en ubicación segura                                │
│  ├── Permisos de archivo restringidos                                  │
│  ├── Cifrado del disco donde se almacena                               │
│  └── Backup cifrado                                                    │
│                                                                         │
│  CAPA 6: MONITOREO Y ALERTAS                                          │
│  ├── Alertas de acceso no autorizado                                   │
│  ├── Verificación periódica HIBP                                       │
│  └── Auditoría de cambios                                              │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Defensas Específicas por Tipo de Ataque

### Contra Ataque de Diccionario

| Defensa | Implementación | Efectividad |
|---------|---------------|-------------|
| Contraseña larga (≥20 chars) | Política obligatoria | ⭐⭐⭐⭐⭐ |
| Verificar contra HIBP | Activar en gestor | ⭐⭐⭐⭐ |
| Prohibir palabras comunes | Regla en gestor | ⭐⭐⭐⭐ |
| Argon2id con alta memoria | Configurar en KDF | ⭐⭐⭐⭐⭐ |

### Contra Fuerza Bruta

| Defensa | Implementación | Efectividad |
|---------|---------------|-------------|
| KDF lento (Argon2id) | Configurar parámetros | ⭐⭐⭐⭐⭐ |
| Rate limiting | En servidor web | ⭐⭐⭐ |
| Bloqueo temporal | Después de N intentos | ⭐⭐⭐ |
| Contraseña larga | Política | ⭐⭐⭐⭐⭐ |

### Contra Rainbow Tables

| Defensa | Implementación | Efectividad |
|---------|---------------|-------------|
| Salt único | Automático en gestores modernos | ⭐⭐⭐⭐⭐ |
| KDF con salt | Automático | ⭐⭐⭐⭐⭐ |

### Contra Keyloggers

| Defensa | Implementación | Efectividad |
|---------|---------------|-------------|
| Autofill del gestor | Usar extensión del navegador | ⭐⭐⭐⭐ |
| Biometría/PIN local | Configurar en clientes | ⭐⭐⭐⭐ |
| Hardware key (WebAuthn) | Usar YubiKey | ⭐⭐⭐⭐⭐ |

### Contra Phishing

| Defensa | Implementación | Efectividad |
|---------|---------------|-------------|
| Autofill solo en dominios conocidos | Verificar configuración | ⭐⭐⭐⭐ |
| Verificación de URL | Extensión muestra dominio | ⭐⭐⭐ |
| WebAuthn (no vulnerable a phishing) | Usar hardware key | ⭐⭐⭐⭐⭐ |

## Configuración Recomendada de KeePassXC

### Parámetros de KDF Óptimos

```
CONFIGURACIÓN RECOMENDADA:

Algoritmo de KDF: Argon2id

Parámetros:
├── Iteraciones (Time): 10
├── Memoria: 65536 KB (64 MB)
├── Paralelismo: 4
└── Salt: 32 bytes (automático)

Para maximum seguridad:
├── Iteraciones: 20
├── Memoria: 131072 KB (128 MB)
├── Paralelismo: 4
└── Nota: Aumenta tiempo de apertura ~2-3x

Cifrado:
├── Algoritmo: AES-256-CBC o ChaCha20-Poly1305
└── Transformaciones: 60,000 (para compatibilidad)

Comparación de tiempos:
┌──────────────┬──────────────┬──────────────┐
│ Configuración│ Tiempo apert.│ Resistencia  │
├──────────────┼──────────────┼──────────────┤
│ Default      │ ~0.5 seg     │ Baja         │
│ Recomendada  │ ~2 seg       │ Alta         │
│ Maximum      │ ~5 seg       │ Muy alta     │
└──────────────┴──────────────┴──────────────┘
```

### Verificación de Integridad

```
PARA DETECTAR MODIFICACIONES DEL ARCHIVO:

1. Calcular hash SHA-256 del archivo .kdbx
   certutil -hashfile archivo.kdbx SHA256

2. Guardar hash en ubicación separada
   (Email a ti mismo, USB cifrado, etc.)

3. Verificar periódicamente
   Comparar hash actual con el guardado

4. Si cambia → Posible tampering → No abrir
```

## Defensas para Vaultwarden (Servidor)

### Hardening del Servidor

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    HARDENING VAULTWARDEN                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  RED:                                                                   │
│  ├── Firewall: Solo puertos 80, 443 abiertos                          │
│  ├── VPN para acceso administrativo                                    │
│  ├── IDS/IPS para detectar anomalías                                  │
│  └── Segmentation de red                                               │
│                                                                         │
│  NGINX:                                                                 │
│  ├── TLS 1.3 solamente (deshabilitar 1.0, 1.1, 1.2)                  │
│  ├── HSTS habilitado                                                   │
│  ├── Security headers completos                                        │
│  ├── Rate limiting agresivo en login                                   │
│  ├── WAF (Web Application Firewall)                                    │
│  └── Certificados de CA confiable (no self-signed en prod)            │
│                                                                         │
│  VAULTWARDEN:                                                           │
│  ├── SIGNUPS_ALLOWED=false                                             │
│  ├── SHOW_PASSWORD_HINT=false                                          │
│  ├── PASSWORD_HINT_ALLOWED=false                                       │
│  ├── ADMIN_TOKEN con token seguro                                      │
│  ├── SMTP configurado para notificaciones                              │
│  ├── HIBP habilitado                                                   │
│  └── Rate limiting interno                                             │
│                                                                         │
│  POSTGRESQL:                                                            │
│  ├── SSL forzado (si está en red separada)                            │
│  ├── Usuaria de DB con permisos mínimos                                │
│  ├── Backups automáticos cifrados                                      │
│  ├── Connection pooling (PgBouncer)                                    │
│  └── Monitoreo de queries lentas                                       │
│                                                                         │
│  CONTENEDORES:                                                          │
│  ├── Security: no-new-privileges                                       │
│  ├── Read-only filesystem                                               │
│  ├── Resource limits (CPU, RAM)                                        │
│  ├── Health checks habilitados                                         │
│  └── Logging estructurado                                              │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Monitoreo de Seguridad

```powershell
# security-monitor.ps1
# Monitoreo de seguridad para Vaultwarden

function Get-SecurityMetrics {
    $metrics = @{}
    
    # 1. Login fallidos (última hora)
    $failedLogins = docker logs vw-vaultwarden --since 1h 2>&1 | 
        Select-String "failed login" | Measure-Object
    $metrics["FailedLogins"] = $failedLogins.Count
    
    # 2. IP más activas (últimas 24h)
    $topIPs = docker logs vw-vaultwarden --since 24h 2>&1 | 
        Select-String "login_success" | 
        ForEach-Object { ($_ -split "from ")[1] -split " " } | 
        Group-Object | Sort-Object Count -Descending | Select-Object -First 5
    $metrics["TopIPs"] = $topIPs
    
    # 3. Usuarios más activos
    $activeUsers = docker logs vw-vaultwarden --since 24h 2>&1 | 
        Select-String "login_success" | 
        ForEach-Object { ($_ -split "user ")[1] -split " " } | 
        Group-Object | Sort-Object Count -Descending | Select-Object -First 10
    $metrics["ActiveUsers"] = $activeUsers
    
    # 4. Eventos de seguridad
    $securityEvents = docker logs vw-vaultwarden --since 24h 2>&1 | 
        Select-String "2fa_disabled|vault_exported|password_changed" | 
        Measure-Object
    $metrics["SecurityEvents"] = $securityEvents.Count
    
    return $metrics
}

# Ejecutar y mostrar
$metrics = Get-SecurityMetrics
Write-Host "=== Métricas de Seguridad ===" -ForegroundColor Cyan
Write-Host "Login fallidos (1h): $($metrics.FailedLogins)"
Write-Host "Eventos de seguridad (24h): $($metrics.SecurityEvents)"
```

## Comparación de Resistencia a Ataques

| Configuración | Diccionario | Fuerza Bruta | GPU (Hashcat) |
|---------------|-------------|--------------|---------------|
| KeePass default | ~2 seg | ~4 horas | ~30 min |
| KeePass Argon2id 64MB | ~2 seg | ~12 horas | ~2 horas |
| KeePass Argon2id 128MB | ~2 seg | ~24 horas | ~4 horas |
| Contraseña 20+ chars | No encontrado | >10^10 años | >10^8 años |
| Contraseña 24+ chars | Imposible | Imposible | Imposible |

## Resumen de Mejores Prácticas

| # | Práctica | Prioridad |
|---|----------|-----------|
| 1 | Contraseña maestra ≥20 caracteres | Crítica |
| 2 | Argon2id con ≥64MB memoria | Crítica |
| 3 | 2FA/TOTP obligatorio | Crítica |
| 4 | Hardware key (WebAuthn) para admin | Alta |
| 5 | Verificación HIBP periódica | Alta |
| 6 | Backup cifrado en 3 ubicaciones | Alta |
| 7 | No compartir master password | Crítica |
| 8 | Almacenar vault en ubicación segura | Alta |
| 9 | Monitoreo de accesos | Media |
| 10 | Capacitación continua | Media |

---

> **Actividad**: Basándote en los resultados del ataque (sección 5.1), implementa las defensas recomendadas y verifica que el tiempo de ataque aumenta significativamente.
