# 3.1 Guía Completa Paso a Paso: Actividad Práctica de Gestión de Contraseñas

## Actividad Final del Curso

### Objetivos de Aprendizaje

Al finalizar esta actividad, el estudiante será capaz de:

1. Instalar y configurar Vaultwarden con Docker Compose y PostgreSQL
2. Configurar una organización con usuarios, colecciones y políticas
3. Implementar autenticación multi-factor (TOTP + WebAuthn)
4. Generar, almacenar y compartir contraseñas seguras
5. Configurar notificaciones de uso y cambios de contraseñas
6. Implementar un plan de respaldo y recuperación
7. Realizar pruebas de seguridad y verificación
8. Analizar fortalezas, debilidades y proponer mejoras

### Marco Teórico Previo (30 min)

Antes de comenzar, revisar los conceptos de:
- Cifrado E2E y zero-knowledge ([1.1](../01-marco-teorico/01-fundamentos-seguridad.md))
- Amenazas comunes ([1.2](../01-marco-teorico/02-amenazas-comunes.md))
- Criptografía aplicada ([1.3](../01-marco-teorico/03-principios-cripografia.md))

### Prerrequisitos

| Requisito | Versión Mínima | Verificación |
|-----------|----------------|--------------|
| Docker | 20.10+ | `docker --version` |
| Docker Compose | 2.0+ | `docker compose version` |
| Conexión a internet | - | `ping google.com` |
| Puerto 80/443 disponible | - | `netstat -an | findstr :80` |
| 4GB RAM mínimo | - | Verificar en Task Manager |
| 10GB espacio en disco | - | `dir C:\` |

---

## Fase 1: Infraestructura Base (45 min)

### Paso 1: Crear Estructura de Directorios

```powershell
# Crear directorio del proyecto
mkdir C:\vaultwarden-bhu
cd C:\vaultwarden-bhu

# Crear subdirectorios
mkdir config
mkdir data
mkdir certs
mkdir backups
mkdir logs
```

### Paso 2: Generar Certificados TLS Auto-firmados (Desarrollo)

```powershell
# Generar clave privada y certificado auto-firmado
# NOTA: En producción, usar certificado de Let's Encrypt o CA interna

# Para Windows (requiere OpenSSL instalado o WSL)
openssl req -x509 -nodes -days 365 -newkey rsa:2048 `
    -keyout certs/vaultwarden.key `
    -out certs/vaultwarden.crt `
    -subj "/C=UY/ST=Montevideo/L=Montevideo/O=BHU/CN=vaultwarden.local"
```

### Paso 3: Crear Archivo de Variables de Entorno

Crear archivo `C:\vaultwarden-bhu\.env`:

```env
# ============================================
# Vaultwarden - Variables de Entorno BHU
# ============================================

# Dominio y URLs
DOMAIN=https://vaultwarden.local
SIGNUPS_ALLOWED=false
SHOW_PASSWORD_HINT=false

# Base de Datos
DATABASE_URL=postgresql://vaultwarden:VLW_S3cur3P@ss_2024!@db:5432/vaultwarden

# Seguridad
ADMIN_TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.TOKEN_ADMIN_AQUI
WEBSOCKET_ENABLED=true
WEBSOCKET_URL=wss://vaultwarden.local/hub

# Cifrado
SENDY_INSTALLATION_ID=00000000-0000-0000-0000-000000000000
SENDY_INSTALLATION_KEY=00000000000000000000000000000000

# Correo (para notificaciones)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=notificaciones@bhu.uy
SMTP_PASSWORD=TU_PASSWORD_SMTP
SMTP_SECURITY=starttls
SMTP_FROM=notificaciones@bhu.uy
SMTP_FROM_NAME=BHU Vaultwarden

# Notificaciones
INVITATIONS_ALLOWED=true
PASSWORD_HINT_ALLOWED=false

# Adjuntos
ATTACHMENT_STORAGE_TYPE=file_system
ATTACHMENT_STORAGE_DIR=/data/attachments

# Log
LOG_LEVEL=warn
EXTENDED_LOGGING=false
```

### Paso 4: Generar Token de Administrador

```powershell
# Generar token seguro para el admin
# Copiar el resultado y pegarlo en ADMIN_TOKEN del .env
openssl rand -base64 48
```

### Paso 5: Crear Docker Compose

Crear archivo `C:\vaultwarden-bhu\docker-compose.yml`:

```yaml
version: '3.8'

services:
  # ============================================
  # Vaultwarden - Backend de Gestión de Claves
  # ============================================
  vaultwarden:
    image: vaultwarden/server:latest
    container_name: vaultwarden-bhu
    restart: unless-stopped
    environment:
      - DOMAIN=${DOMAIN}
      - SIGNUPS_ALLOWED=${SIGNUPS_ALLOWED}
      - SHOW_PASSWORD_HINT=${SHOW_PASSWORD_HINT}
      - DATABASE_URL=${DATABASE_URL}
      - ADMIN_TOKEN=${ADMIN_TOKEN}
      - WEBSOCKET_ENABLED=${WEBSOCKET_ENABLED}
      - SMTP_HOST=${SMTP_HOST}
      - SMTP_PORT=${SMTP_PORT}
      - SMTP_USERNAME=${SMTP_USERNAME}
      - SMTP_PASSWORD=${SMTP_PASSWORD}
      - SMTP_SECURITY=${SMTP_SECURITY}
      - SMTP_FROM=${SMTP_FROM}
      - SMTP_FROM_NAME=${SMTP_FROM_NAME}
      - INVITATIONS_ALLOWED=${INVITATIONS_ALLOWED}
      - PASSWORD_HINT_ALLOWED=${PASSWORD_HINT_ALLOWED}
      - LOG_LEVEL=${LOG_LEVEL}
    volumes:
      - ./data:/data
      - ./config:/config
      - ./certs:/certs:ro
    ports:
      - "8080:80"
    networks:
      - vaultwarden-net
    depends_on:
      db:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:80/alive"]
      interval: 30s
      timeout: 10s
      retries: 3
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: '0.5'

  # ============================================
  # NGINX - Reverse Proxy + TLS Termination
  # ============================================
  nginx:
    image: nginx:alpine
    container_name: vaultwarden-nginx
    restart: unless-stopped
    ports:
      - "443:443"
      - "80:80"
    volumes:
      - ./config/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./certs:/certs:ro
    networks:
      - vaultwarden-net
    depends_on:
      - vaultwarden

  # ============================================
  # PostgreSQL - Base de Datos
  # ============================================
  db:
    image: postgres:16-alpine
    container_name: vaultwarden-db
    restart: unless-stopped
    environment:
      POSTGRES_DB=vaultwarden
      POSTGRES_USER=vaultwarden
      POSTGRES_PASSWORD=VLW_S3cur3P@ss_2024!
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./backups:/backups
    networks:
      - vaultwarden-net
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U vaultwarden -d vaultwarden"]
      interval: 10s
      timeout: 5s
      retries: 5
    deploy:
      resources:
        limits:
          memory: 1G
          cpus: '1.0'

networks:
  vaultwarden-net:
    driver: bridge

volumes:
  postgres_data:
    driver: local
```

### Paso 6: Configurar NGINX

Crear archivo `C:\vaultwarden-bhu\config\nginx.conf`:

```nginx
events {
    worker_connections 1024;
}

http {
    # Rate Limiting
    limit_req_zone $binary_remote_addr zone=login:10m rate=5r/m;

    # Redirect HTTP → HTTPS
    server {
        listen 80;
        server_name vaultwarden.local;
        return 301 https://$server_name$request_uri;
    }

    # HTTPS Server
    server {
        listen 443 ssl http2;
        server_name vaultwarden.local;

        # TLS Configuration
        ssl_certificate /certs/vaultwarden.crt;
        ssl_certificate_key /certs/vaultwarden.key;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers HIGH:!aNULL:!MD5;
        ssl_prefer_server_ciphers on;

        # Security Headers
        add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
        add_header X-Content-Type-Options nosniff;
        add_header X-Frame-Options DENY;
        add_header X-XSS-Protection "1; mode=block";
        add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https://haveibeenpwned.com https://icons.bitwarden.com; connect-src 'self' wss://vaultwarden.local;";

        # Proxy to Vaultwarden
        location / {
            proxy_pass http://vaultwarden:80;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;

            # WebSocket support
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
        }

        # Rate limit login endpoint
        location /identity/connect/token {
            limit_req zone=login burst=3 nodelay;
            proxy_pass http://vaultwarden:80;
        }

        # Deny access to admin panel from outside
        location /admin {
            #allow 192.168.0.0/16;  # Solo red interna
            #deny all;
            proxy_pass http://vaultwarden:80;
        }
    }
}
```

---

## Fase 2: Despliegue (30 min)

### Paso 7: Levantar los Servicios

```powershell
cd C:\vaultwarden-bhu

# Verificar que Docker está corriendo
docker info

# Levantar servicios
docker compose up -d

# Verificar estado
docker compose ps

# Ver logs
docker compose logs -f vaultwarden
```

### Paso 8: Verificar Funcionamiento

```powershell
# Verificar que todos los contenedores están corriendo
docker ps

# Verificar conexión a base de datos
docker exec vaultwarden-db pg_isready -U vaultwarden

# Verificar que Vaultwarden responde
curl -k https://localhost:8080/alive
```

### Paso 9: Acceder al Panel de Administración

```
1. Abrir navegador: https://vaultwarden.local/admin
2. Ingresar el ADMIN_TOKEN configurado en .env
3. Verificar que el panel de administración funciona
4. Revisar:
   - Usuarios registrados (debería estar vacío)
   - Estadísticas del servidor
   - Configuración de correo
```

---

## Fase 3: Configuración de Usuarios (30 min)

### Paso 10: Crear Organización "BHU"

```
1. Registrar primer usuario (será el Owner):
   - Email: admin@bhu.uy
   - Nombre: Administrador BHU
   - Master Password: [generar ≥20 caracteres]

2. En la web de Vaultwarden:
   - Ir a Settings → Organizations
   - Click "Create Organization"
   - Nombre: BHU
   - Billing Email: admin@bhu.uy
   - Plan: Free (suficiente para empezar)

3. Verificar que la organización se creó correctamente
```

### Paso 11: Crear Estructura de Colecciones

```
Dentro de BHU (Organización), crear:

📁 Administración
   - Propósito: Contraseñas de administración general
   - Miembros: Admin, Gerencia
   - Permisos: Admin = Admin, Gerencia = Edit

📁 Ventas
   - Propósito: Herramientas de ventas
   - Miembros: Equipo de ventas
   - Permisos: Admin = Admin, Ventas = Edit

📁 TI
   - Propósito: Infraestructura y desarrollo
   - Miembros: Equipo de TI
   - Permisos: Admin = Admin, TI = Edit

📁 Compartida General
   - Propósito: WiFi, impresoras, servicios comunes
   - Miembros: Todos
   - Permisos: Admin = Admin, Todos = Solo lectura
```

### Paso 12: Agregar Usuarios de Prueba

```
Invitar usuarios (Settings → Members → Invite):

1. Juan Pérez (TI)
   - Email: juan.perez@bhu.uy
   - Colección: TI, Compartida General
   - Permisos: Manager en TI

2. María García (Ventas)
   - Email: maria.garcia@bhu.uy
   - Colección: Ventas, Compartida General
   - Permisos: User

3. Carlos López (Admin)
   - Email: carlos.lopez@bhu.uy
   - Colección: Todas
   - Permisos: Admin
```

### Paso 13: Agregar Contraseñas de Ejemplo

En la colección "Compartida General":

```
📄 WiFi Oficina BHU
   - Usuario: BHU-WiFi
   - Contraseña: W1f1_S3gur4_BHU_2024!
   - Notas: Red corporativa, cambiar cada 180 días
   - URL: N/A

📄 Impresora Principal
   - Usuario: admin
   - Contraseña: Pr1nt3r_BHU_2024
   - Notas: HP LaserJet, piso 2

📄 Portal de Email
   - Usuario: soporte@bhu.uy
   - Contraseña: [generar]
   - URL: https://mail.bhu.uy
```

En la colección "TI":

```
📄 Server Principal (Proxmox)
   - Usuario: root
   - Contraseña: [generar 24 caracteres]
   - Notas: 192.168.1.10, acceso SSH

📄 GitHub BHU
   - Usuario: bhu-devops
   - Contraseña: [generar]
   - Notas: Organización BHU en GitHub
   - URL: https://github.com/bhu-uy

📄 API Stripe (Producción)
   - Usuario: sk_live_[key]
   - Contraseña: [None]
   - Notas: Secret key de producción, rotar cada 90 días
   - URL: https://dashboard.stripe.com/apikeys
```

---

## Fase 4: Seguridad Avanzada (30 min)

### Paso 14: Configurar 2FA (TOTP)

Para cada usuario:

```
1. Ir a Settings → Security → Two-step login
2. Habilitar "Authenticator App"
3. Escanear QR code con Google Authenticator/Authy
4. Ingresar código de verificación
5. Guardar códigos de recuperación en vault seguro
6. Verificar que funciona cerrando sesión y reingresando
```

### Paso 15: Configurar WebAuthn/FIDO2

```
1. Ir a Settings → Security → Two-step login
2. Habilitar "Security Key"
3. Click "Manage"
4. Insertar YubiKey o usar Windows Hello
5. Tocar el botón del hardware key
6. Nombrar la clave (ej: "YubiKey 5 - Juan Pérez")
7. Verificar funcionamiento
```

### Paso 16: Configurar Biometría (Windows Hello)

```
1. Descargar Bitwarden Desktop para Windows
2. Instalar y abrir
3. Login con credenciales
4. Ir a Settings → Security
5. Habilitar "Unlock with Windows Hello"
6. Verificar: cerrar app → reabrir → pedirá Windows Hello
```

### Paso 17: Configurar Verificación HIBP

```
1. Ir a Settings → Security
2. Habilitar "Have I Been Pwned"
3. Verificar contraseñas existentes contra HIBP
4. Corregir las que aparezcan en brechas conocidas
```

---

## Fase 5: Notificaciones (20 min)

### Paso 18: Configurar Notificaciones por Correo

El .env ya tiene configurado SMTP. Verificar:

```powershell
# Verificar conexión SMTP
docker exec vaultwarden-bhu curl -v smtp://smtp.gmail.com:587

# Probar enviando email de invitación a un usuario
# Settings → Members → Invite → enviar invitación
```

### Paso 19: Configurar Notificaciones de Uso

```
Para cada usuario, configurar:

1. Settings → Notifications
2. Habilitar:
   - "Password used" → Notificar cuando se use una contraseña
   - "Password changed" → Notificar cuando se cambie
   - "Password shared" → Notificar cuando se comparta
   - "New device" → Notificar login desde dispositivo nuevo
   - "2FA reminder" → Recordatorio para configurar 2FA

3. Verificar que las notificaciones llegan por correo
```

### Paso 20: Configurar Webhooks (Opcional - Avanzado)

```
Para integración con sistemas internos:

1. Crear script receptor de webhooks
2. Configurar en Vaultwarden:
   - SETTINGS__WEBSOCKET_ENABLED=true
   - SETTINGS__WEBSOCKET_URL=wss://vaultwarden.local/hub
3. Las notificaciones llegan via WebSocket
4. Procesar con script personalizado para:
   - Log en SIEM
   - Alertas en Slack/Teams
   - Auditoría en base de datos
```

---

## Fase 6: Respaldo y Recuperación (20 min)

### Paso 21: Configurar Respaldo Automático

Crear script `C:\vaultwarden-bhu\backup.ps1`:

```powershell
# ============================================
# Script de Respaldo Vaultwarden BHU
# ============================================

$BACKUP_DIR = "C:\vaultwarden-bhu\backups"
$DATE = Get-Date -Format "yyyy-MM-dd_HH-mm"
$BACKUP_NAME = "vaultwarden-backup-$DATE"

Write-Host "Iniciando respaldo: $BACKUP_NAME"

# 1. Respaldar base de datos
Write-Host "1. Respaldo de PostgreSQL..."
docker exec vaultwarden-db pg_dump -U vaultwarden vaultwarden | `
    Out-File "$BACKUP_DIR\$BACKUP_NAME-db.sql"

# 2. Respaldar vault de Vaultwarden
Write-Host "2. Respaldo de Vaultwarden data..."
Copy-Item -Path "C:\vaultwarden-bhu\data" `
    -Destination "$BACKUP_DIR\$BACKUP_NAME-data" -Recurse

# 3. Respaldar configuración
Write-Host "3. Respaldo de configuración..."
Copy-Item -Path "C:\vaultwarden-bhu\config" `
    -Destination "$BACKUP_DIR\$BACKUP_NAME-config" -Recurse
Copy-Item -Path "C:\vaultwarden-bhu\.env" `
    -Destination "$BACKUP_DIR\$BACKUP_NAME.env"

# 4. Comprimir
Write-Host "4. Comprimiendo..."
Compress-Archive -Path "$BACKUP_DIR\$BACKUP_NAME-*" `
    -DestinationPath "$BACKUP_DIR\$BACKUP_NAME.zip"

# 5. Limpiar archivos temporales
Remove-Item "$BACKUP_DIR\$BACKUP_NAME-*" -Recurse

# 6. Verificar tamaño
$size = (Get-Item "$BACKUP_DIR\$BACKUP_NAME.zip").Length / 1MB
Write-Host "Respaldo completado: $BACKUP_NAME.zip ($([math]::Round($size, 2)) MB)"

# 7. Mantener solo últimos 7 respaldos
$backups = Get-ChildItem "$BACKUP_DIR\*.zip" | Sort-Object LastWriteTime -Descending
if ($backups.Count -gt 7) {
    $backups | Select-Object -Skip 7 | Remove-Item -Force
    Write-Host "Respaldos antiguos eliminados"
}
```

### Paso 22: Programar Respaldo Diario

```powershell
# Crear tarea programada para respaldo diario a las 2:00 AM
$action = New-ScheduledTaskAction `
    -Execute "powershell.exe" `
    -Argument "-File C:\vaultwarden-bhu\backup.ps1"

$trigger = New-ScheduledTaskTrigger `
    -Daily -At 2am

$settings = New-ScheduledTaskSettingsSet `
    -StartWhenAvailable `
    -DontStopOnIdleEnd

Register-ScheduledTask `
    -TaskName "Vaultwarden Backup" `
    -Action $action `
    -Trigger $trigger `
    -Settings $settings `
    -Description "Respaldo diario de Vaultwarden BHU"
```

### Paso 23: Probar Recuperación

```powershell
# Simular recuperación en una carpeta temporal
$RECOVERY_DIR = "C:\vaultwarden-recovery-test"

# 1. Crear directorio temporal
mkdir $RECOVERY_DIR

# 2. Restaurar respaldo
Expand-Archive -Path "$BACKUP_DIR\latest-backup.zip" -DestinationPath $RECOVERY_DIR

# 3. Verificar integridad
Get-ChildItem $RECOVERY_DIR -Recurse | Measure-Object

# 4. Restaurar base de datos (simulación)
# docker exec -i vaultwarden-db psql -U vaultwarden vaultwarden < $RECOVERY_DIR\*-db.sql

Write-Host "Prueba de recuperación completada"
```

---

## Fase 7: Verificación Final (15 min)

### Paso 24: Checklist de Verificación

| # | Verificación | Estado | Notas |
|---|-------------|--------|-------|
| 1 | Vaultwarden accesible en https://vaultwarden.local | ☐ | |
| 2 | Login exitoso con credenciales de admin | ☐ | |
| 3 | Organización "BHU" creada | ☐ | |
| 4 | 3 colecciones creadas | ☐ | |
| 5 | 3 usuarios de prueba invitados | ☐ | |
| 6 | 3 contraseñas de ejemplo creadas | ☐ | |
| 7 | 2FA (TOTP) configurado en admin | ☐ | |
| 8 | WebAuthn configurado | ☐ | |
| 9 | Biometría (Windows Hello) funciona | ☐ | |
| 10 | HIBP habilitado | ☐ | |
| 11 | Notificaciones por correo funcionan | ☐ | |
| 12 | Respaldo manual ejecutado exitosamente | ☐ | |
| 13 | Recuperación desde backup verificada | ☐ | |
| 14 | NGINX con TLS funcionando | ☐ | |
| 15 | Rate limiting en login activo | ☐ | |
| 16 | PostgreSQL con health check | ☐ | |
| 17 | Todos los contenedores con restart policy | ☐ | |
| 18 | Documentación de procedimientos completa | ☐ | |

### Paso 25: Prueba de Uso Diario

```
Simular un día de uso:

1. Mañana:
   - Login con Windows Hello ✅
   - Abrir navegador → extensión auto-login ✅
   - Acceder a correo corporativo ✅

2. Durante el día:
   - Compartir contraseña de WiFi con nuevo empleado ✅
   - Recibir notificación de uso ✅
   - Generar contraseña nueva para servicio ✅

3. Tarde:
   - Cambiar contraseña que apareció en HIBP ✅
   - Verificar que el cambio se sincronizó ✅
   - Revisar log de auditoría ✅

4. Cierre:
   - Verificar respaldo automático ✅
   - Revisar alertas de seguridad ✅
```

---

## Fase 8: Análisis Final (20 min)

### Paso 26: Evaluación de Fortalezas y Debilidades

| Aspecto | Fortaleza | Debilidad | Mejora Propuesta |
|---------|-----------|-----------|------------------|
| **Seguridad** | Cifrado E2E, zero-knowledge | Single point of failure (servidor) | Implementar HA con réplicas |
| **Disponibilidad** | Backup automático | Sin failover automático | Docker Swarm + Auto-failover |
| **Usabilidad** | Biometría, autofill | Curva de aprendizaje inicial | Capacitación + documentación |
| **Escalabilidad** | Sin límite usuarios | PostgreSQL puede ser bottleneck | Connection pooling (PgBouncer) |
| **Auditoría** | Log de eventos | Sin integración SIEM | Exportar a Elastic/SIEM |
| **Costo** | $0 licencias | Costo de infraestructura | Cloud vs On-premise |
| **Compliance** | GDPR ready | Falta certificación formal | Auditoría externa |

### Paso 27: Preguntas de Reflexión

1. ¿Qué pasaría si el servidor Vaultwarden queda destruido?
2. ¿Cómo recuperarían los usuarios sus contraseñas si olvidan la master password?
3. ¿Qué pasa si un administrador malicioso accede al panel de admin?
4. ¿Cómo se compara esta solución con un gestor comercial como 1Password?
5. ¿Qué mejoras implementarías para un banco real?

### Paso 28: Documentación de Entrega

Crear documentación que incluya:

```
entrega-actividad/
├── 01-estructura-archivos/       ← Capturas de pantalla
├── 02-configuracion/             ← Archivos .env, docker-compose.yml
├── 03-usuarios/                  ← Lista de usuarios y colecciones
├── 04-contraseñas/               ← Capturas de contraseñas creadas
├── 05-seguridad/                 ← Capturas de 2FA, WebAuthn
├── 06-notificaciones/            ← Capturas de emails recibidos
├── 07-respaldos/                 ← Script y verificación
├── 08-analisis/                  ← Fortalezas/debilidades/mejoras
└── README.md                     ← Índice de la entrega
```

---

> **Tiempo total estimado: 3.5 horas**
>
> **Nota**: Esta actividad debe realizarse en un entorno controlado (laboratorio). En producción, se requiere hardening adicional, certificados de CA confiable, y monitoreo continuo.
