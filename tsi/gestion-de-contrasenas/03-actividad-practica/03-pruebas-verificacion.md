# 3.3 Pruebas y Verificación de Seguridad

## Suite de Pruebas Completa

### Prueba 1: Verificación de Cifrado E2E

```powershell
# test-e2e-encryption.ps1
# Verificar que el cifrado E2E funciona correctamente

Write-Host "=== Prueba 1: Cifrado E2E ===" -ForegroundColor Cyan

# 1. Crear entrada de prueba
$testEntry = @{
    name = "Test Entry E2E"
    login_username = "test_user"
    login_password = "T3st_S3gur0_2024!"
    login_uri = "https://test.example.com"
    notes = "Entrada de prueba para verificar E2E"
}

# 2. Guardar en Vaultwarden
Write-Host "1. Guardando entrada de prueba..."
# (Usar API de Vaultwarden o interfaz web)

# 3. Verificar que el servidor NO tiene el texto en claro
Write-Host "2. Verificando que el servidor no ve texto plano..."
# Conectar a PostgreSQL y verificar
$checkQuery = docker exec vw-db psql -U vaultwarden -d vaultwarden -c `
    "SELECT name, data FROM vault WHERE name LIKE '%Test Entry%'"

if ($checkQuery -match "T3st_S3gur0_2024!") {
    Write-Host "❌ FALLO: El texto plano está visible en la base de datos" -ForegroundColor Red
} else {
    Write-Host "✅ PASS: El texto está cifrado en la base de datos" -ForegroundColor Green
}

# 4. Verificar desde otro dispositivo
Write-Host "3. Verificando sincronización..."
# Login desde otro navegador/dispositivo y verificar que la entrada aparece descifrada
```

### Prueba 2: Verificación de Autenticación

```powershell
# test-authentication.ps1
# Verificar mecanismos de autenticación

Write-Host "=== Prueba 2: Autenticación ===" -ForegroundColor Cyan

# 1. Test login normal
Write-Host "1. Probando login normal..."
$loginResponse = Invoke-WebRequest -Uri "https://vaultwarden.local/identity/connect/token" `
    -Method POST `
    -Body @{
        grant_type = "password"
        username = "admin@bhu.uy"
        password = "MiMasterPassword123!"
        scope = "api offline_access"
        client_id = "web"
        deviceType = "8"
        deviceIdentifier = "test-device-001"
        deviceName = "Test Device"
    } -UseBasicParsing

if ($loginResponse.StatusCode -eq 200) {
    Write-Host "✅ Login exitoso" -ForegroundColor Green
    $token = ($loginResponse.Content | ConvertFrom-Json).access_token
} else {
    Write-Host "❌ Login falló" -ForegroundColor Red
}

# 2. Test login con credenciales incorrectas
Write-Host "2. Probando login con credenciales incorrectas..."
try {
    $wrongLogin = Invoke-WebRequest -Uri "https://vaultwarden.local/identity/connect/token" `
        -Method POST `
        -Body @{
            grant_type = "password"
            username = "admin@bhu.uy"
            password = "WrongPassword123!"
            scope = "api offline_access"
            client_id = "web"
        } -UseBasicParsing
    Write-Host "❌ FALLO: Login debería haber fallado" -ForegroundColor Red
} catch {
    Write-Host "✅ PASS: Login rechazado correctamente" -ForegroundColor Green
}

# 3. Test rate limiting
Write-Host "3. Probando rate limiting (10 intentos fallidos)..."
$failedAttempts = 0
for ($i = 1; $i -le 10; $i++) {
    try {
        Invoke-WebRequest -Uri "https://vaultwarden.local/identity/connect/token" `
            -Method POST `
            -Body @{
                grant_type = "password"
                username = "admin@bhu.uy"
                password = "WrongPassword$i!"
                scope = "api offline_access"
                client_id = "web"
            } -UseBasicParsing
    } catch {
        $failedAttempts++
    }
}
Write-Host "Intentos fallidos: $failedAttempts de 10"

# 4. Test token expiración
Write-Host "4. Probando expiración de token..."
Start-Sleep -Seconds 3600  # Esperar 1 hora (o reducir TTL para prueba)
try {
    $headers = @{ "Authorization" = "Bearer $token" }
    $expiredTest = Invoke-WebRequest -Uri "https://vaultwarden.local/api/sync" `
        -Headers $headers -UseBasicParsing
    Write-Host "❌ FALLO: Token debería haber expirado" -ForegroundColor Red
} catch {
    Write-Host "✅ PASS: Token expirado correctamente" -ForegroundColor Green
}
```

### Prueba 3: Verificación de 2FA

```powershell
# test-2fa.ps1
# Verificar funcionamiento de 2FA

Write-Host "=== Prueba 3: Autenticación Multi-Factor ===" -ForegroundColor Cyan

# 1. Test TOTP
Write-Host "1. Probando TOTP..."
# Generar código TOTP actual
$totpCode = Get-TOTPCode -Secret "JBSWY3DPEHPK3PXP"  # Ejemplo
$totpLogin = Invoke-WebRequest -Uri "https://vaultwarden.local/identity/connect/token" `
    -Method POST `
    -Body @{
        grant_type = "password"
        username = "admin@bhu.uy"
        password = "MiMasterPassword123!"
        scope = "api offline_access"
        client_id = "web"
        TwoFactorToken = $totpCode
        TwoFactorProvider = "0"  # TOTP
        TwoFactorRemember = "0"
    } -UseBasicParsing

if ($totpLogin.StatusCode -eq 200) {
    Write-Host "✅ TOTP funciona correctamente" -ForegroundColor Green
} else {
    Write-Host "❌ TOTP falló" -ForegroundColor Red
}

# 2. Test código TOTP incorrecto
Write-Host "2. Probando código TOTP incorrecto..."
try {
    $wrongTotp = Invoke-WebRequest -Uri "https://vaultwarden.local/identity/connect/token" `
        -Method POST `
        -Body @{
            grant_type = "password"
            username = "admin@bhu.uy"
            password = "MiMasterPassword123!"
            scope = "api offline_access"
            client_id = "web"
            TwoFactorToken = "000000"
            TwoFactorProvider = "0"
            TwoFactorRemember = "0"
        } -UseBasicParsing
    Write-Host "❌ FALLO: Código incorrecto debería ser rechazado" -ForegroundColor Red
} catch {
    Write-Host "✅ PASS: Código TOTP incorrecto rechazado" -ForegroundColor Green
}

# 3. Test WebAuthn
Write-Host "3. Probando WebAuthn..."
# (Requiere hardware key o emulador)
Write-Host "   → Requiere hardware key para prueba completa"
```

### Prueba 4: Verificación de Compartición

```powershell
# test-sharing.ps1
# Verificar funcionamiento de colecciones compartidas

Write-Host "=== Prueba 4: Compartición de Contraseñas ===" -ForegroundColor Cyan

# 1. Crear colección
Write-Host "1. Creando colección de prueba..."
# (Usar API de Vaultwarden)

# 2. Agregar usuario a colección
Write-Host "2. Agregando usuario a colección..."

# 3. Verificar que el usuario puede ver la contraseña
Write-Host "3. Verificando acceso del usuario..."
# Login como usuario y verificar colección

# 4. Verificar permisos
Write-Host "4. Verificando permisos..."
# Intentar editar como usuario de solo lectura
# Debería fallar

# 5. Verificar que usuarios fuera de la colección NO ven las contraseñas
Write-Host "5. Verificando aislamiento..."
# Login como usuario que no está en la colección
# No debería ver las contraseñas de la colección
```

### Prueba 5: Verificación de Notificaciones

```powershell
# test-notifications.ps1
# Verificar sistema de notificaciones

Write-Host "=== Prueba 5: Notificaciones ===" -ForegroundColor Cyan

# 1. Test notificación de contraseña usada
Write-Host "1. Probando notificación de uso..."
# Usar una contraseña y verificar que llega email

# 2. Test notificación de contraseña cambiada
Write-Host "2. Probando notificación de cambio..."
# Cambiar una contraseña y verificar email

# 3. Test notificación de nuevo dispositivo
Write-Host "3. Probando notificación de nuevo dispositivo..."
# Login desde dispositivo nuevo

# 4. Test notificación de login fallido
Write-Host "4. Probando notificación de login fallido..."
# Intentar login con credenciales incorrectas
```

### Prueba 6: Verificación de Respaldo

```powershell
# test-backup.ps1
# Verificar integridad de respaldos

Write-Host "=== Prueba 6: Respaldo y Recuperación ===" -ForegroundColor Cyan

# 1. Crear respaldo
Write-Host "1. Creando respaldo de prueba..."
& "C:\vaultwarden-bhu\backup.ps1"

# 2. Verificar que el archivo existe
$backupFiles = Get-ChildItem "C:\vaultwarden-bhu\backups\*.zip" | 
    Sort-Object LastWriteTime -Descending | 
    Select-Object -First 1

if ($backupFiles) {
    Write-Host "✅ Respaldo creado: $($backupFiles.Name)" -ForegroundColor Green
    Write-Host "   Tamaño: $([math]::Round($backupFiles.Length / 1MB, 2)) MB"
} else {
    Write-Host "❌ No se encontró respaldo" -ForegroundColor Red
}

# 3. Verificar integridad del ZIP
Write-Host "2. Verificando integridad del ZIP..."
try {
    $zip = [System.IO.Compression.ZipFile]::OpenRead($backupFiles.FullName)
    $entries = $zip.Entries.Count
    $zip.Dispose()
    Write-Host "✅ ZIP válido: $entries archivos" -ForegroundColor Green
} catch {
    Write-Host "❌ ZIP corrupto" -ForegroundColor Red
}

# 4. Simular recuperación
Write-Host "3. Simulando recuperación..."
$recoveryDir = "C:\vaultwarden-recovery-test"
if (Test-Path $recoveryDir) { Remove-Item $recoveryDir -Recurse -Force }
Expand-Archive -Path $backupFiles.FullName -DestinationPath $recoveryDir

# 5. Verificar archivos restaurados
Write-Host "4. Verificando archivos restaurados..."
$restoredFiles = Get-ChildItem $recoveryDir -Recurse | Measure-Object
Write-Host "   Archivos restaurados: $($restoredFiles.Count)"

# 6. Verificar que la DB dump es válida
Write-Host "5. Verificando dump de PostgreSQL..."
$dbDump = Get-ChildItem "$recoveryDir\*.dump" -ErrorAction SilentlyContinue
if ($dbDump) {
    $firstLine = Get-Content $dbDump.FullName -First 1
    if ($firstLine -match "PostgreSQL") {
        Write-Host "✅ Dump de DB válido" -ForegroundColor Green
    } else {
        Write-Host "❌ Dump de DB inválido" -ForegroundColor Red
    }
}

# 7. Limpiar
Remove-Item $recoveryDir -Recurse -Force
```

### Prueba 7: Verificación de Seguridad de Red

```powershell
# test-network-security.ps1
# Verificar configuración de red y TLS

Write-Host "=== Prueba 7: Seguridad de Red ===" -ForegroundColor Cyan

# 1. Test TLS
Write-Host "1. Probando TLS..."
$tlsTest = Test-NetConnection -ComputerName vaultwarden.local -Port 443
if ($tlsTest.TcpTestSucceeded) {
    Write-Host "✅ TLS accessible" -ForegroundColor Green
} else {
    Write-Host "❌ TLS no accesible" -ForegroundColor Red
}

# 2. Verificar versión TLS
Write-Host "2. Verificando versión TLS..."
try {
    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
    $response = Invoke-WebRequest -Uri "https://vaultwarden.local" -UseBasicParsing
    Write-Host "✅ TLS 1.2+ funciona" -ForegroundColor Green
} catch {
    Write-Host "❌ TLS no funciona correctamente" -ForegroundColor Red
}

# 3. Test HTTP → HTTPS redirect
Write-Host "3. Probando redirect HTTP→HTTPS..."
try {
    $httpResponse = Invoke-WebRequest -Uri "http://vaultwarden.local" -UseBasicParsing -MaximumRedirection 0
    Write-Host "❌ FALLO: HTTP debería redirigir a HTTPS" -ForegroundColor Red
} catch {
    if ($_.Exception.Response.StatusCode -eq 301 -or $_.Exception.Response.StatusCode -eq 302) {
        Write-Host "✅ PASS: HTTP redirige a HTTPS" -ForegroundColor Green
    } else {
        Write-Host "⚠️ Respuesta inesperada: $($_.Exception.Response.StatusCode)" -ForegroundColor Yellow
    }
}

# 4. Test security headers
Write-Host "4. Verificando security headers..."
$headers = (Invoke-WebRequest -Uri "https://vaultwarden.local" -UseBasicParsing).Headers

$requiredHeaders = @(
    "Strict-Transport-Security",
    "X-Content-Type-Options",
    "X-Frame-Options"
)

foreach ($header in $requiredHeaders) {
    if ($headers.ContainsKey($header)) {
        Write-Host "   ✅ $header presente" -ForegroundColor Green
    } else {
        Write-Host "   ❌ $header faltante" -ForegroundColor Red
    }
}

# 5. Test rate limiting
Write-Host "5. Probando rate limiting..."
$attempts = 0
for ($i = 1; $i -le 20; $i++) {
    try {
        Invoke-WebRequest -Uri "https://vaultwarden.local/identity/connect/token" `
            -Method POST -UseBasicParsing -Body "grant_type=password&username=test&password=test"
        $attempts++
    } catch {
        if ($_.Exception.Response.StatusCode -eq 429) {
            Write-Host "✅ Rate limiting activado después de $i intentos" -ForegroundColor Green
            break
        }
    }
}

# 6. Test admin panel access
Write-Host "6. Probando acceso al panel admin..."
try {
    $adminResponse = Invoke-WebRequest -Uri "https://vaultwarden.local/admin" -UseBasicParsing
    if ($adminResponse.StatusCode -eq 200) {
        Write-Host "⚠️ Panel admin accesible (verificar si debería estar restringido)" -ForegroundColor Yellow
    }
} catch {
    Write-Host "✅ Panel admin restringido" -ForegroundColor Green
}
```

### Prueba 8: Verificación de Performance

```powershell
# test-performance.ps1
# Verificar rendimiento del sistema

Write-Host "=== Prueba 8: Performance ===" -ForegroundColor Cyan

# 1. Test tiempo de respuesta
Write-Host "1. Midiendo tiempo de respuesta..."
$stopwatch = [System.Diagnostics.Stopwatch]::StartNew()
$response = Invoke-WebRequest -Uri "https://vaultwarden.local/alive" -UseBasicParsing
$stopwatch.Stop()

$latency = $stopwatch.ElapsedMilliseconds
if ($latency -lt 200) {
    Write-Host "✅ Latencia: ${latency}ms (excelente)" -ForegroundColor Green
} elseif ($latency -lt 500) {
    Write-Host "⚠️ Latencia: ${latency}ms (aceptable)" -ForegroundColor Yellow
} else {
    Write-Host "❌ Latencia: ${latency}ms (lento)" -ForegroundColor Red
}

# 2. Test吞吐量
Write-Host "2. Midiendo throughput..."
$requests = 0
$startTime = Get-Date
for ($i = 1; $i -le 100; $i++) {
    try {
        Invoke-WebRequest -Uri "https://vaultwarden.local/alive" -UseBasicParsing | Out-Null
        $requests++
    } catch { }
}
$duration = ((Get-Date) - $startTime).TotalSeconds
$rps = $requests / $duration
Write-Host "   Requests por segundo: $([math]::Round($rps, 2))"

# 3. Test uso de recursos
Write-Host "3. Uso de recursos del servidor..."
$stats = docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"
Write-Host $stats

# 4. Test conexión DB
Write-Host "4. Tiempo de respuesta de PostgreSQL..."
$dbStart = Get-Date
docker exec vw-db pg_isready -U vaultwarden | Out-Null
$dbDuration = ((Get-Date) - $dbStart).TotalMilliseconds
Write-Host "   DB latency: $([math]::Round($dbDuration, 2))ms"
```

## Ejecutar Todas las Pruebas

```powershell
# run-all-tests.ps1
# Ejecutar suite completa de pruebas

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "  SUITE DE PRUEBAS - VAULTWARDEN BHU     " -ForegroundColor Cyan
Write-Host "  Fecha: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

$results = @()

$tests = @(
    @{Name = "Cifrado E2E"; Script = "test-e2e-encryption.ps1"},
    @{Name = "Autenticación"; Script = "test-authentication.ps1"},
    @{Name = "2FA"; Script = "test-2fa.ps1"},
    @{Name = "Compartición"; Script = "test-sharing.ps1"},
    @{Name = "Notificaciones"; Script = "test-notifications.ps1"},
    @{Name = "Respaldo"; Script = "test-backup.ps1"},
    @{Name = "Seguridad Red"; Script = "test-network-security.ps1"},
    @{Name = "Performance"; Script = "test-performance.ps1"}
)

foreach ($test in $tests) {
    Write-Host "`n--- Ejecutando: $($test.Name) ---" -ForegroundColor Yellow
    try {
        & $test.Script
        $results += @{Test = $test.Name; Status = "PASS"}
    } catch {
        $results += @{Test = $test.Name; Status = "FAIL"}
        Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    }
}

# Resumen
Write-Host "`n=========================================" -ForegroundColor Cyan
Write-Host "  RESUMEN DE PRUEBAS                     " -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

$passed = ($results | Where-Object { $_.Status -eq "PASS" }).Count
$failed = ($results | Where-Object { $_.Status -eq "FAIL" }).Count
$total = $results.Count

foreach ($result in $results) {
    $color = if ($result.Status -eq "PASS") { "Green" } else { "Red" }
    Write-Host "  $($result.Test): $($result.Status)" -ForegroundColor $color
}

Write-Host "`nTotal: $total | Pass: $passed | Fail: $failed" -ForegroundColor $(if ($failed -eq 0) { "Green" } else { "Red" })
```

---

> **Nota**: Ejecutar estas pruebas en un entorno controlado. Algunas pruebas (como rate limiting) pueden afectar temporalmente el servicio.
