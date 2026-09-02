# 3.2 Configuración Detallada de Vaultwarden

## Docker Compose Producción (Hardened)

```yaml
# docker-compose.production.yml
version: '3.8'

services:
  # ============================================
  # Vaultwarden - Servidor Principal
  # ============================================
  vaultwarden:
    image: vaultwarden/server:latest
    container_name: vaultwarden-bhu
    restart: always
    environment:
      # Dominio
      DOMAIN: https://vaultwarden.bhu.uy
      
      # Seguridad
      SIGNUPS_ALLOWED: "false"
      SHOW_PASSWORD_HINT: "false"
      PASSWORD_HINT_ALLOWED: "false"
      INVITATIONS_ALLOWED: "true"
      
      # Admin
      ADMIN_TOKEN: ${ADMIN_TOKEN}
      
      # Base de datos
      DATABASE_URL: postgresql://vaultwarden:${DB_PASSWORD}@db:5432/vaultwarden
      
      # WebSocket
      WEBSOCKET_ENABLED: "true"
      WEBSOCKET_URL: wss://vaultwarden.bhu.uy/hub
      
      # SMTP
      SMTP_HOST: ${SMTP_HOST}
      SMTP_PORT: ${SMTP_PORT}
      SMTP_USERNAME: ${SMTP_USERNAME}
      SMTP_PASSWORD: ${SMTP_PASSWORD}
      SMTP_SECURITY: starttls
      SMTP_FROM: ${SMTP_FROM}
      SMTP_FROM_NAME: "BHU Vaultwarden"
      
      # Adjuntos
      ATTACHMENT_STORAGE_TYPE: file_system
      ATTACHMENT_STORAGE_DIR: /data/attachments
      
      # Rate Limiting
      RATE_LIMIT_FACTOR: 4
      RATE_LIMIT_SECONDS: 30
      
      # Log
      LOG_LEVEL: warn
      
      # HIBP
      HIBP_API_KEY: ${HIBP_API_KEY}
      
      # Templating
      TEMPLATES_FOLDER: /data/templates
      
      # Yubikey
      YUBICO_CLIENT_ID: ${YUBICO_CLIENT_ID}
      YUBICO_SECRET_KEY: ${YUBICO_SECRET_KEY}
    volumes:
      - vw-data:/data
      - vw-config:/config
      - vw-attachments:/data/attachments
    ports:
      - "127.0.0.1:8080:80"
    networks:
      - vw-internal
    depends_on:
      db:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:80/alive"]
      interval: 30s
      timeout: 10s
      retries: 5
      start_period: 30s
    deploy:
      resources:
        limits:
          memory: 1G
          cpus: '1.0'
    security_opt:
      - no-new-privileges:true
    read_only: true
    tmpfs:
      - /tmp
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"

  # ============================================
  # NGINX - Reverse Proxy + TLS
  # ============================================
  nginx:
    image: nginx:alpine
    container_name: vw-nginx
    restart: always
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./config/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./certs:/certs:ro
      - ./config/security-headers.conf:/etc/nginx/security-headers.conf:ro
    networks:
      - vw-internal
    depends_on:
      - vaultwarden
    healthcheck:
      test: ["CMD", "wget", "--spider", "-q", "http://localhost:80/health"]
      interval: 30s
      timeout: 5s
      retries: 3
    deploy:
      resources:
        limits:
          memory: 256M
          cpus: '0.25'

  # ============================================
  # PostgreSQL - Base de Datos
  # ============================================
  db:
    image: postgres:16-alpine
    container_name: vw-db
    restart: always
    environment:
      POSTGRES_DB: vaultwarden
      POSTGRES_USER: vaultwarden
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_INITDB_ARGS: "--encoding=UTF-8 --lc-collate=C --lc-ctype=C"
    volumes:
      - vw-postgres:/var/lib/postgresql/data
      - ./backups:/backups
      - ./config/postgresql.conf:/etc/postgresql/postgresql.conf:ro
    networks:
      - vw-internal
    command: postgres -c config_file=/etc/postgresql/postgresql.conf
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U vaultwarden -d vaultwarden"]
      interval: 10s
      timeout: 5s
      retries: 5
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: '1.5'
    security_opt:
      - no-new-privileges:true
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"

  # ============================================
  # Redis - Cache (Opcional, para HA)
  # ============================================
  redis:
    image: redis:7-alpine
    container_name: vw-redis
    restart: always
    command: redis-server --requirepass ${REDIS_PASSWORD} --maxmemory 256mb --maxmemory-policy allkeys-lru
    volumes:
      - vw-redis:/data
    networks:
      - vw-internal
    healthcheck:
      test: ["CMD", "redis-cli", "-a", "${REDIS_PASSWORD}", "ping"]
      interval: 10s
      timeout: 5s
      retries: 3
    deploy:
      resources:
        limits:
          memory: 256M
          cpus: '0.25'

networks:
  vw-internal:
    driver: bridge
    internal: true  # No acceso externo directo
  vw-external:
    driver: bridge

volumes:
  vw-data:
  vw-config:
  vw-attachments:
  vw-postgres:
  vw-redis:
```

## PostgreSQL Tuned (postgresql.conf)

```ini
# PostgreSQL Configuration - Vaultwarden BHU
# Optimizado para rendimiento y seguridad

# Memoria
shared_buffers = 512MB
effective_cache_size = 1536MB
work_mem = 16MB
maintenance_work_mem = 128MB

# Escritura
wal_buffers = 16MB
checkpoint_completion_target = 0.9
max_wal_size = 2GB
min_wal_size = 1GB
wal_compression = on

# Consultas
random_page_cost = 1.1
effective_io_concurrency = 200
default_statistics_target = 100

# Conexiones
max_connections = 100
superuser_reserved_connections = 3

# Logging
log_destination = 'stderr'
logging_collector = on
log_directory = 'pg_log'
log_filename = 'postgresql-%Y-%m-%d.log'
log_rotation_age = 1d
log_rotation_size = 100MB
log_min_duration_statement = 1000  # Log queries > 1s
log_checkpoints = on
log_connections = on
log_disconnections = on
log_lock_waits = on

# Seguridad
password_encryption = scram-sha-256
ssl = off  # Terminación TLS en NGINX

# Replicación (para HA)
# max_wal_senders = 5
# wal_level = replica
# hot_standby = on
```

## Configuración de Notificaciones

### Script de Notificaciones Personalizadas

Crear archivo `config/notifications.py`:

```python
#!/usr/bin/env python3
"""
Script de notificaciones para Vaultwarden BHU
Escucha eventos via webhook y envía notificaciones
"""

import smtplib
import json
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler

# Configuración
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "notificaciones@bhu.uy"
SMTP_PASS = "tu_password_smtp"
EMAIL_DESTINO = "admin@bhu.uy"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("vw-notifications")

class NotificationHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            event = json.loads(post_data.decode('utf-8'))
            self.process_event(event)
        except Exception as e:
            logger.error(f"Error procesando evento: {e}")
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"status": "ok"}).encode())
    
    def process_event(self, event):
        event_type = event.get('type', 'unknown')
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        if event_type == 'password_used':
            self.send_notification(
                "Contraseña Utilizada",
                f"Usuario: {event.get('user')}\n"
                f"Contraseña: {event.get('name')}\n"
                f"Fecha: {timestamp}\n"
                f"IP: {event.get('ip')}"
            )
        
        elif event_type == 'password_changed':
            self.send_notification(
                "Contraseña Cambiada",
                f"Usuario: {event.get('user')}\n"
                f"Contraseña: {event.get('name')}\n"
                f"Fecha: {timestamp}\n"
                f"IP: {event.get('ip')}"
            )
        
        elif event_type == 'new_device':
            self.send_notification(
                "Nuevo Dispositivo Detectado",
                f"Usuario: {event.get('user')}\n"
                f"Dispositivo: {event.get('device')}\n"
                f"IP: {event.get('ip')}\n"
                f"Fecha: {timestamp}"
            )
        
        elif event_type == 'failed_login':
            self.send_notification(
                "⚠️ Intento de Login Fallido",
                f"Email: {event.get('email')}\n"
                f"IP: {event.get('ip')}\n"
                f"Fecha: {timestamp}\n"
                f"Acción requerida: Verificar si es legítimo"
            )
    
    def send_notification(self, subject, body):
        msg = MIMEMultipart()
        msg['From'] = f"BHU Vaultwarden <{SMTP_USER}>"
        msg['To'] = EMAIL_DESTINO
        msg['Subject'] = f"[Vaultwarden BHU] {subject}"
        
        msg.attach(MIMEText(body, 'plain', 'utf-8'))
        
        try:
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)
            server.quit()
            logger.info(f"Notificación enviada: {subject}")
        except Exception as e:
            logger.error(f"Error enviando email: {e}")

if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', 9000), NotificationHandler)
    logger.info("Servidor de notificaciones escuchando en puerto 9000")
    server.serve_forever()
```

## Configuración de Backup Automático

### Script de Backup Avanzado

```powershell
# backup-advanced.ps1
# Respaldo completo de Vaultwarden BHU

param(
    [string]$BackupDir = "C:\vaultwarden-bhu\backups",
    [string]$RetentionDays = 30,
    [switch]$Encrypt,
    [string]$EncryptionKey = ""
)

$ErrorActionPreference = "Stop"

# Funciones
function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logMessage = "[$timestamp] [$Level] $Message"
    Write-Host $logMessage
    Add-Content -Path "$BackupDir\backup.log" -Value $logMessage
}

function Backup-PostgreSQL {
    param([string]$OutputPath)
    Write-Log "Iniciando respaldo de PostgreSQL..."
    
    $container = "vw-db"
    $dbUser = "vaultwarden"
    $dbName = "vaultwarden"
    
    $dump = docker exec $container pg_dump -U $dbUser --format=custom --compress=9 $dbName
    
    $dump | Out-File -FilePath $OutputPath -Encoding UTF8
    
    $size = (Get-Item $OutputPath).Length / 1MB
    Write-Log "PostgreSQL respaldado: $([math]::Round($size, 2)) MB"
}

function Backup-VaultwardenData {
    param([string]$OutputDir)
    Write-Log "Iniciando respaldo de Vaultwarden data..."
    
    $source = "C:\vaultwarden-bhu\data"
    Copy-Item -Path $source -Destination $OutputDir -Recurse -Force
    
    $size = (Get-Item $OutputDir -Recurse | Measure-Object -Property Length -Sum).Sum / 1MB
    Write-Log "Vaultwarden data respaldado: $([math]::Round($size, 2)) MB"
}

function Backup-Config {
    param([string]$OutputDir)
    Write-Log "Iniciando respaldo de configuración..."
    
    $files = @(
        "C:\vaultwarden-bhu\.env",
        "C:\vaultwarden-bhu\docker-compose.yml",
        "C:\vaultwarden-bhu\config\*"
    )
    
    foreach ($file in $files) {
        if (Test-Path $file) {
            Copy-Item -Path $file -Destination $OutputDir -Recurse -Force
        }
    }
    
    Write-Log "Configuración respaldada"
}

function Compress-Backup {
    param([string]$SourcePath, [string]$OutputPath)
    Write-Log "Comprimiendo respaldo..."
    
    Compress-Archive -Path $SourcePath -DestinationPath $OutputPath -CompressionLevel Optimal
    
    $size = (Get-Item $OutputPath).Length / 1MB
    Write-Log "Comprimido: $([math]::Round($size, 2)) MB"
}

function Encrypt-Backup {
    param([string]$FilePath, [string]$Key)
    Write-Log "Cifrando respaldo..."
    
    $secureKey = ConvertTo-SecureString $Key -AsPlainText -Force
    $encrypted = Get-Content $FilePath | ConvertTo-SecureString -AsPlainText -Force | ConvertFrom-SecureString -Key $secureKey
    
    $encrypted | Out-File "$FilePath.encrypted"
    Remove-Item $FilePath
    
    Write-Log "Respaldo cifrado"
}

function Cleanup-OldBackups {
    param([string]$Dir, [int]$Days)
    Write-Log "Limpiando respaldos antiguos (> $Days días)..."
    
    $cutoff = (Get-Date).AddDays(-$Days)
    $oldBackups = Get-ChildItem "$Dir\*.zip" | Where-Object { $_.LastWriteTime -lt $cutoff }
    
    foreach ($backup in $oldBackups) {
        Remove-Item $backup.FullName -Force
        Write-Log "Eliminado: $($backup.Name)"
    }
    
    Write-Log "Limpieza completada. Eliminados: $($oldBackups.Count)"
}

# =====================
# PRINCIPAL
# =====================

$DATE = Get-Date -Format "yyyy-MM-dd_HH-mm"
$BACKUP_NAME = "vaultwarden-full-$DATE"
$WORK_DIR = "$BackupDir\temp\$BACKUP_NAME"

Write-Log "========================================="
Write-Log "INICIO DE RESPALDO: $BACKUP_NAME"
Write-Log "========================================="

try {
    # Crear directorio temporal
    New-Item -ItemType Directory -Path $WORK_DIR -Force | Out-Null
    
    # 1. Respaldo PostgreSQL
    Backup-PostgreSQL -OutputPath "$WORK_DIR\vaultwarden-db.dump"
    
    # 2. Respaldo Vaultwarden data
    Backup-VaultwardenData -OutputDir "$WORK_DIR\data"
    
    # 3. Respaldo configuración
    Backup-Config -OutputDir "$WORK_DIR\config"
    
    # 4. Comprimir
    $zipPath = "$BackupDir\$BACKUP_NAME.zip"
    Compress-Backup -SourcePath "$WORK_DIR\*" -OutputPath $zipPath
    
    # 5. Cifrar (opcional)
    if ($Encrypt -and $EncryptionKey) {
        Encrypt-Backup -FilePath $zipPath -Key $EncryptionKey
    }
    
    # 6. Limpiar temporales
    Remove-Item $WORK_DIR -Recurse -Force
    
    # 7. Limpiar respaldos antiguos
    Cleanup-OldBackups -Dir $BackupDir -Days $RetentionDays
    
    # 8. Verificar integridad
    $finalSize = (Get-Item $zipPath).Length / 1MB
    Write-Log "========================================="
    Write-Log "RESPALDO COMPLETADO EXITOSAMENTE"
    Write-Log "Archivo: $zipPath"
    Write-Log "Tamaño: $([math]::Round($finalSize, 2)) MB"
    Write-Log "========================================="
    
} catch {
    Write-Log "ERROR: $($_.Exception.Message)" "ERROR"
    throw
}
```

## Monitoreo y Alertas

### Script de Health Check

```powershell
# health-check.ps1
# Monitoreo de Vaultwarden BHU

param(
    [string]$AlertEmail = "admin@bhu.uy",
    [string]$SlackWebhook = ""
)

function Test-VaultwardenHealth {
    $results = @{}
    
    # 1. Test HTTP
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8080/alive" -UseBasicParsing -TimeoutSec 5
        $results["HTTP"] = $response.StatusCode -eq 200
    } catch {
        $results["HTTP"] = $false
    }
    
    # 2. Test PostgreSQL
    try {
        $dbStatus = docker exec vw-db pg_isready -U vaultwarden 2>&1
        $results["PostgreSQL"] = $dbStatus -match "accepting connections"
    } catch {
        $results["PostgreSQL"] = $false
    }
    
    # 3. Test Redis
    try {
        $redisStatus = docker exec vw-redis redis-cli ping 2>&1
        $results["Redis"] = $redisStatus -match "PONG"
    } catch {
        $results["Redis"] = $false
    }
    
    # 4. Test Docker containers
    $containers = docker ps --format "{{.Names}}:{{.Status}}" 2>&1
    $results["Containers"] = $containers -match "Up"
    
    # 5. Test disk space
    $disk = Get-PSDrive C
    $freeSpaceGB = $disk.Free / 1GB
    $results["DiskSpace"] = $freeSpaceGB -gt 5  # Mínimo 5GB libre
    
    # 6. Test memory
    $memory = Get-CimInstance Win32_OperatingSystem
    $freeMemoryGB = $memory.FreePhysicalMemory / 1MB
    $results["Memory"] = $freeMemoryGB -gt 1  # Mínimo 1GB libre
    
    return $results
}

# Ejecutar health check
$health = Test-VaultwardenHealth
$allHealthy = $health.Values | Where-Object { $_ -eq $false } | Measure-Object | Select-Object -ExpandProperty Count

if ($allHealthy -gt 0) {
    # Alerta
    $failedChecks = $health.GetEnumerator() | Where-Object { $_.Value -eq $false }
    $message = "⚠️ Vaultwarden Health Check FALLÓ`n"
    $message += "Checks fallidos: $($failedChecks.Keys -join ', ')"
    $message += "`nFecha: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
    
    # Email
    $emailParams = @{
        From = "monitoring@bhu.uy"
        To = $AlertEmail
        Subject = "[ALERTA] Vaultwarden Health Check Falló"
        Body = $message
        SmtpServer = "smtp.gmail.com"
        Port = 587
        UseSsl = $true
        Credential = (Get-Credential)
    }
    Send-MailMessage @emailParams
    
    Write-Host "ALERTA ENVIADA: $message" -ForegroundColor Red
} else {
    Write-Host "✅ Todos los checks pasaron" -ForegroundColor Green
}
```

## Scripts de Emergencia

### Script de Failover

```powershell
# failover.ps1
# Failover manual a réplica (si se usa configuración HA)

param(
    [string]$NewPrimary = "vaultwarden-replica"
)

Write-Host "Iniciando failover a $NewPrimary..."

# 1. Detener escritura en primario
docker exec vw-db-primary psql -U vaultwarden -c "SELECT pg_promote();"

# 2. Actualizar configuración para apuntar a réplica
$env:DATABASE_URL = "postgresql://vaultwarden:${DB_PASSWORD}@${NewPrimary}:5432/vaultwarden"

# 3. Reiniciar Vaultwarden con nueva DB
docker compose restart vaultwarden

# 4. Verificar
Start-Sleep -Seconds 10
$health = Invoke-WebRequest -Uri "http://localhost:8080/alive" -UseBasicParsing
if ($health.StatusCode -eq 200) {
    Write-Host "✅ Failover completado exitosamente" -ForegroundColor Green
} else {
    Write-Host "❌ Failover falló - verificar logs" -ForegroundColor Red
}
```

---

> **Nota**: Esta configuración está diseñada para entornos de desarrollo y pruebas. En producción, se requiere:
> - Certificados TLS de CA confiable (Let's Encrypt o interna)
> - Hardening adicional del sistema operativo
> - Monitoreo con Prometheus/Grafana
> - Integración con SIEM
> - Auditoría de seguridad periódica
