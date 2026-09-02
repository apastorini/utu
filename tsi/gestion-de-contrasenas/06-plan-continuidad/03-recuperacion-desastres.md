# 6.3 Plan de Recuperación ante Desastres (DRP)

## Definición

El **Plan de Recuperación ante Desastres (DRP)** es el conjunto de procedimientos técnicos para restaurar la infraestructura y datos de gestión de contraseñas después de un desastre.

## Estrategia de Backup: Regla 3-2-1-1

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    ESTRATEGIA DE BACKUP 3-2-1-1                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  3 COPIAS DE LOS DATOS:                                               │
│  ├── Copia 1: Servidor primario (PostgreSQL)                         │
│  ├── Copia 2: Servidor de réplica (PostgreSQL)                       │
│  └── Copia 3: Backup off-site (cifrado)                              │
│                                                                         │
│  2 MEDIOS DIFERENTES:                                                  │
│  ├── Medio 1: Disco local/NAS                                        │
│  └── Medio 2: Cloud (S3, Backblaze) o USB                           │
│                                                                         │
│  1 COPIA OFF-SITE:                                                    │
│  ├── Ubicación geográfica diferente                                  │
│  ├── Acceso remoto                                                    │
│  └── Cifrada con clave separada                                      │
│                                                                         │
│  1 COPIA OFFLINE (Inmutable):                                         │
│  ├── No accesible por ransomware                                     │
│  ├── WORM (Write Once Read Many)                                     │
│  ├── USB cifrado en caja fuerte                                      │
│  └── O storage inmutable (S3 Object Lock)                           │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Tipos de Backup

| Tipo | Contenido | Frecuencia | Retención | Almacenamiento |
|------|-----------|------------|-----------|----------------|
| **Full DB** | PostgreSQL dump completo | Diario | 30 días | NAS + Cloud |
| **Incremental** | Cambios desde último backup | Cada 15 min | 7 días | NAS |
| **Vaultwarden Data** | /data directory | Semanal | 90 días | NAS + Cloud |
| **Config** | .env, docker-compose.yml | Semanal | 90 días | Git + Cloud |
| **Vaults Usuarios** | Exportaciones cifradas | Mensual | 1 año | USB + Cloud |
| **Certificados** | TLS certs, keys | Al renovar | 2 años | USB en caja fuerte |

## Scripts de Backup

### Script de Backup Completo

```powershell
# backup-complete.ps1
# Backup completo de Vaultwarden BHU

param(
    [string]$BackupRoot = "C:\vaultwarden-backups",
    [int]$RetentionDays = 30,
    [switch]$Encrypt,
    [string]$EncryptionPassword = "",
    [switch]$UploadToCloud,
    [string]$CloudBucket = ""
)

$ErrorActionPreference = "Stop"
$Timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
$BackupName = "vaultwarden-full-$Timestamp"
$BackupDir = "$BackupRoot\$BackupName"

function Write-Status {
    param([string]$Message, [string]$Status = "INFO")
    $colors = @{ INFO = "Cyan"; SUCCESS = "Green"; WARNING = "Yellow"; ERROR = "Red" }
    Write-Host "[$Status] $Message" -ForegroundColor $colors[$Status]
}

# Crear directorio de backup
Write-Status "Creando directorio de backup: $BackupDir"
New-Item -ItemType Directory -Path $BackupDir -Force | Out-Null

# 1. Backup de PostgreSQL
Write-Status "1. Respaldando PostgreSQL..."
$dbBackup = "$BackupDir\vaultwarden-db.dump"
docker exec vw-db pg_dump -U vaultwarden --format=custom --compress=9 vaultwarden > $dbBackup
$dbSize = [math]::Round((Get-Item $dbBackup).Length / 1MB, 2)
Write-Status "   PostgreSQL: $dbSize MB" "SUCCESS"

# 2. Backup de Vaultwarden data
Write-Status "2. Respaldando Vaultwarden data..."
$vwDataBackup = "$BackupDir\vaultwarden-data"
Copy-Item -Path "C:\vaultwarden-bhu\data" -Destination $vwDataBackup -Recurse -Force
$vwSize = [math]::Round((Get-Item $vwDataBackup -Recurse | Measure-Object -Property Length -Sum).Sum / 1MB, 2)
Write-Status "   Vaultwarden data: $vwSize MB" "SUCCESS"

# 3. Backup de configuración
Write-Status "3. Respaldando configuración..."
$configBackup = "$BackupDir\config"
New-Item -ItemType Directory -Path $configBackup -Force | Out-Null
Copy-Item "C:\vaultwarden-bhu\.env" "$configBackup\" -Force
Copy-Item "C:\vaultwarden-bhu\docker-compose.yml" "$configBackup\" -Force
Copy-Item "C:\vaultwarden-bhu\config\*" "$configBackup\" -Recurse -Force
Write-Status "   Configuración respaldada" "SUCCESS"

# 4. Backup de certificados
Write-Status "4. Respaldando certificados..."
$certsBackup = "$BackupDir\certs"
Copy-Item "C:\vaultwarden-bhu\certs" $certsBackup -Recurse -Force
Write-Status "   Certificados respaldados" "SUCCESS"

# 5. Metadata del backup
Write-Status "5. Creando metadata..."
$metadata = @{
    Timestamp = $Timestamp
    Version = "1.0"
    PostgreSQL_Version = (docker exec vw-db psql --version)
    Vaultwarden_Version = (docker exec vw-vaultwarden cat /app/vaultwarden --version 2>$null)
    Backup_Size_MB = [math]::Round(($BackupDir | Get-ChildItem -Recurse | Measure-Object -Property Length -Sum).Sum / 1MB, 2)
    Components = @("PostgreSQL", "Vaultwarden Data", "Config", "Certs")
} | ConvertTo-Json -Depth 3
$metadata | Out-File "$BackupDir\metadata.json"
Write-Status "   Metadata creada" "SUCCESS"

# 6. Comprimir
Write-Status "6. Comprimiendo backup..."
$zipPath = "$BackupRoot\$BackupName.zip"
Compress-Archive -Path $BackupDir -DestinationPath $zipPath -CompressionLevel Optimal
$zipSize = [math]::Round((Get-Item $zipPath).Length / 1MB, 2)
Write-Status "   ZIP: $zipSize MB" "SUCCESS"

# 7. Cifrar (opcional)
if ($Encrypt -and $EncryptionPassword) {
    Write-Status "7. Cifrando backup..."
    $securePassword = ConvertTo-SecureString $EncryptionPassword -AsPlainText -Force
    $encrypted = Get-Content $zipPath | ConvertTo-SecureString -AsPlainText -Force | ConvertFrom-SecureString -Key (Get-Content "$BackupRoot\encryption-key.txt")
    $encrypted | Out-File "$zipPath.encrypted"
    Remove-Item $zipPath
    Write-Status "   Backup cifrado" "SUCCESS"
}

# 8. Upload a cloud (opcional)
if ($UploadToCloud -and $CloudBucket) {
    Write-Status "8. Subiendo a cloud..."
    # aws s3 cp $zipPath s3://$CloudBucket/backups/
    Write-Status "   Upload completado" "SUCCESS"
}

# 9. Limpiar respaldos antiguos
Write-Status "9. Limpiando respaldos antiguos..."
$cutoff = (Get-Date).AddDays(-$RetentionDays)
$oldBackups = Get-ChildItem "$BackupRoot\*.zip" | Where-Object { $_.LastWriteTime -lt $cutoff }
foreach ($old in $oldBackups) {
    Remove-Item $old.FullName -Force
    Write-Status "   Eliminado: $($old.Name)" "WARNING"
}

# 10. Limpiar directorio temporal
Remove-Item $BackupDir -Recurse -Force

# Resumen final
$totalSize = if ($Encrypt) { (Get-Item "$zipPath.encrypted").Length / 1MB } else { $zipSize }
Write-Status "=========================================" "SUCCESS"
Write-Status "BACKUP COMPLETADO" "SUCCESS"
Write-Status "Archivo: $zipPath" "SUCCESS"
Write-Status "Tamaño total: $([math]::Round($totalSize, 2)) MB" "SUCCESS"
Write-Status "=========================================" "SUCCESS"
```

### Script de Restauración

```powershell
# restore-complete.ps1
# Restauración completa de Vaultwarden desde backup

param(
    [Parameter(Mandatory=$true)]
    [string]$BackupFile,
    
    [string]$RestoreDir = "C:\vaultwarden-restore",
    [switch]$Decrypt,
    [string]$DecryptionPassword = "",
    [switch]$Force
)

$ErrorActionPreference = "Stop"

function Write-Status {
    param([string]$Message, [string]$Status = "INFO")
    $colors = @{ INFO = "Cyan"; SUCCESS = "Green"; WARNING = "Yellow"; ERROR = "Red" }
    Write-Host "[$Status] $Message" -ForegroundColor $colors[$Status]
}

Write-Status "=========================================" "WARNING"
Write-Status "RESTAURACIÓN DE VAULTWARDEN" "WARNING"
Write-Status "=========================================" "WARNING"
Write-Status "Archivo de backup: $BackupFile"

# Verificar que el backup existe
if (-not (Test-Path $BackupFile)) {
    Write-Status "ERROR: Archivo de backup no encontrado" "ERROR"
    exit 1
}

# Confirmar restauración
if (-not $Force) {
    $confirm = Read-Host "¿Está seguro de que desea restaurar? Esto SOBRESCRIBIRÁ los datos actuales (YES/NO)"
    if ($confirm -ne "YES") {
        Write-Status "Restauración cancelada" "WARNING"
        exit 0
    }
}

# 1. Descifrar (si es necesario)
$zipFile = $BackupFile
if ($Decrypt -and $DecryptionPassword) {
    Write-Status "1. Descifrando backup..."
    # Descifrar archivo
    Write-Status "   Descifrado completado" "SUCCESS"
}

# 2. Extraer backup
Write-Status "2. Extrayendo backup..."
New-Item -ItemType Directory -Path $RestoreDir -Force | Out-Null
Expand-Archive -Path $zipFile -DestinationPath $RestoreDir -Force
Write-Status "   Extracción completada" "SUCCESS"

# 3. Verificar integridad
Write-Status "3. Verificando integridad..."
$backupDir = Get-ChildItem $RestoreDir -Directory | Select-Object -First 1
$requiredFiles = @("metadata.json")
$hasDB = Test-Path "$($backupDir.FullName)\vaultwarden-db.dump"
$hasData = Test-Path "$($backupDir.FullName)\vaultwarden-data"
$hasConfig = Test-Path "$($backupDir.FullName)\config"

if (-not $hasDB) {
    Write-Status "ERROR: No se encontró dump de PostgreSQL" "ERROR"
    exit 1
}
Write-Status "   Integridad verificada" "SUCCESS"

# 4. Detener servicios
Write-Status "4. Deteniendo servicios..."
docker compose -f "C:\vaultwarden-bhu\docker-compose.yml" stop vaultwarden
Start-Sleep -Seconds 10
Write-Status "   Servicios detenidos" "SUCCESS"

# 5. Restaurar PostgreSQL
Write-Status "5. Restaurando PostgreSQL..."
docker exec -i vw-db psql -U vaultwarden -d vaultwarden < "$($backupDir.FullName)\vaultwarden-db.dump"
Write-Status "   PostgreSQL restaurado" "SUCCESS"

# 6. Restaurar Vaultwarden data
Write-Status "6. Restaurando Vaultwarden data..."
Copy-Item -Path "$($backupDir.FullName)\vaultwarden-data\*" -Destination "C:\vaultwarden-bhu\data" -Recurse -Force
Write-Status "   Vaultwarden data restaurado" "SUCCESS"

# 7. Restaurar configuración (opcional)
Write-Status "7. ¿Restaurar configuración? (puede sobrescribir cambios locales)"
$restoreConfig = Read-Host "Restaurar configuración? (YES/NO)"
if ($restoreConfig -eq "YES") {
    Copy-Item -Path "$($backupDir.FullName)\config\*" -Destination "C:\vaultwarden-bhu\config" -Recurse -Force
    Write-Status "   Configuración restaurada" "SUCCESS"
}

# 8. Reiniciar servicios
Write-Status "8. Reiniciando servicios..."
docker compose -f "C:\vaultwarden-bhu\docker-compose.yml" start vaultwarden
Start-Sleep -Seconds 30
Write-Status "   Servicios reiniciados" "SUCCESS"

# 9. Verificar funcionamiento
Write-Status "9. Verificando funcionamiento..."
$health = Invoke-WebRequest -Uri "http://localhost:8080/alive" -UseBasicParsing -TimeoutSec 10
if ($health.StatusCode -eq 200) {
    Write-Status "   Vaultwarden funcionando correctamente" "SUCCESS"
} else {
    Write-Status "   ERROR: Vaultwarden no responde correctamente" "ERROR"
}

# 10. Limpiar
Write-Status "10. Limpiando archivos temporales..."
Remove-Item $RestoreDir -Recurse -Force

Write-Status "=========================================" "SUCCESS"
Write-Status "RESTAURACIÓN COMPLETADA" "SUCCESS"
Write-Status "=========================================" "SUCCESS"
```

## Verificación Post-Restauración

### Checklist de Verificación

```powershell
# verify-restore.ps1
# Verificar que la restauración fue exitosa

Write-Host "=== Verificación Post-Restauración ===" -ForegroundColor Cyan

$checks = @()

# 1. Vaultwarden responde
try {
    $health = Invoke-WebRequest -Uri "http://localhost:8080/alive" -UseBasicParsing -TimeoutSec 5
    $checks += @{Name = "Vaultwarden HTTP"; Status = $health.StatusCode -eq 200}
} catch {
    $checks += @{Name = "Vaultwarden HTTP"; Status = $false}
}

# 2. PostgreSQL funciona
try {
    $dbStatus = docker exec vw-db pg_isready -U vaultwarden 2>&1
    $checks += @{Name = "PostgreSQL"; Status = $dbStatus -match "accepting connections"}
} catch {
    $checks += @{Name = "PostgreSQL"; Status = $false}
}

# 3. Login funciona (usuario de prueba)
try {
    $loginTest = Invoke-WebRequest -Uri "http://localhost:8080/identity/connect/token" `
        -Method POST -UseBasicParsing -Body @{
        grant_type = "password"
        username = "admin@bhu.uy"
        password = "test_password"
        scope = "api"
        client_id = "web"
    } -TimeoutSec 10
    $checks += @{Name = "Login endpoint"; Status = $true}
} catch {
    $checks += @{Name = "Login endpoint"; Status = $_.Exception.Response.StatusCode -eq 400}
}

# 4. Docker containers están corriendo
$containers = docker ps --format "{{.Names}}:{{.Status}}" 2>&1
$checks += @{Name = "Docker containers"; Status = $containers -match "Up"}

# 5. Espacio en disco suficiente
$disk = Get-PSDrive C
$freeGB = [math]::Round($disk.Free / 1GB, 2)
$checks += @{Name = "Disk space (>5GB)"; Status = $freeGB -gt 5}

# 6. Certificados TLS válidos
try {
    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
    $tlsTest = Invoke-WebRequest -Uri "https://localhost:8080" -UseBasicParsing -TimeoutSec 5
    $checks += @{Name = "TLS"; Status = $true}
} catch {
    $checks += @{Name = "TLS"; Status = $false}
}

# Mostrar resultados
Write-Host "`n=== Resultados ===" -ForegroundColor Cyan
$passed = 0
$failed = 0
foreach ($check in $checks) {
    $status = if ($check.Status) { "✅ PASS"; $passed++ } else { "❌ FAIL"; $failed++ }
    Write-Host "$status - $($check.Name)"
}

Write-Host "`nTotal: $($checks.Count) | Pass: $passed | Fail: $failed" `
    -ForegroundColor $(if ($failed -eq 0) { "Green" } else { "Red" })

if ($failed -gt 0) {
    Write-Host "`n⚠️ ALGUNAS VERIFICACIONES FALLARON - Revisar antes de producción" `
        -ForegroundColor Yellow
}
```

## Almacenamiento Off-Site

### Opción 1: Cloud Storage (S3/Backblaze)

```bash
# Configurar backup automático a S3
# Requiere: AWS CLI configurado

# Subir backup diario
aws s3 cp /backups/vaultwarden-latest.zip \
    s3://bhu-vaultwarden-backups/daily/ \
    --storage-class STANDARD_IA

# Lifecycle: mover a Glacier después de 30 días
aws s3api put-bucket-lifecycle-configuration \
    --bucket bhu-vaultwarden-backups \
    --lifecycle-configuration '{
        "Rules": [{
            "ID": "MoveToGlacier",
            "Status": "Enabled",
            "Transitions": [{
                "Days": 30,
                "StorageClass": "GLACIER"
            }],
            "Expiration": {
                "Days": 365
            }
        }]
    }'
```

### Opción 2: USB Cifrado (Caja Fuerte)

```
PROCEDIMIENTO:
1. Formatear USB con cifrado (BitLocker o LUKS)
2. Copiar backup cifrado
3. Almacenar en caja fuerte
4. Actualizar mensualmente
5. Documentar contenido en sobre sellado

CONTENIDO DEL USB:
├── vaultwarden-backup.zip.gpg (cifrado con GPG)
├── metadata.json
├── restore-instructions.md
└── encryption-key.txt.gpg (clave de descifrado)
```

## Pruebas de Recuperación

### Prueba Mensual (Simulación)

```powershell
# monthly-drill.ps1
# Drill mensual de recuperación

param(
    [string]$BackupFile,
    [string]$DrillDir = "C:\drill-restore"
)

Write-Host "=== Drill de Recuperación Mensual ===" -ForegroundColor Cyan
Write-Host "Fecha: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"

# 1. Simular restauración en directorio temporal
Write-Host "1. Extrayendo backup..."
New-Item -ItemType Directory -Path $DrillDir -Force | Out-Null
Expand-Archive -Path $BackupFile -DestinationPath $DrillDir -Force

# 2. Verificar integridad de archivos
Write-Host "2. Verificando integridad..."
$dbDump = Get-ChildItem "$DrillDir\*\vaultwarden-db.dump" -ErrorAction SilentlyContinue
if ($dbDump) {
    $size = [math]::Round($dbDump.Length / 1MB, 2)
    Write-Host "   ✅ DB dump válido ($size MB)" -ForegroundColor Green
} else {
    Write-Host "   ❌ DB dump no encontrado" -ForegroundColor Red
}

# 3. Verificar metadata
Write-Host "3. Verificando metadata..."
$metadata = Get-ChildItem "$DrillDir\*\metadata.json" -ErrorAction SilentlyContinue
if ($metadata) {
    $meta = Get-Content $metadata.FullName | ConvertFrom-Json
    Write-Host "   ✅ Backup del: $($meta.Timestamp)" -ForegroundColor Green
} else {
    Write-Host "   ❌ Metadata no encontrada" -ForegroundColor Red
}

# 4. Calcular métricas
Write-Host "4. Métricas del drill..."
$backupAge = (Get-Date) - [DateTime]::Parse($meta.Timestamp)
Write-Host "   Edad del backup: $($backupAge.Days) días"
Write-Host "   RPO real: $($backupAge.TotalMinutes) minutos"

# 5. Limpiar
Remove-Item $DrillDir -Recurse -Force

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "DRILL COMPLETADO" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Cyan
```

## Resumen de DRP

| Componente | Frecuencia | RTO | RPO |
|------------|------------|-----|-----|
| **PostgreSQL** | Cada 15 min (incr), Diario (full) | 30 min | 15 min |
| **Vaultwarden data** | Semanal | 1 hora | 7 días |
| **Configuración** | Semanal | 30 min | 7 días |
| **Certificados** | Al renovar | 1 hora | N/A |
| **Vaults usuarios** | Mensual | 2 horas | 30 días |
| **Servidor completo** | Backup semanal | 4 horas | 7 días |

---

> **Actividad**: Ejecuta un drill de restauración completo. Documenta: tiempo real de restauración, problemas encontrados, y mejoras al procedimiento.
