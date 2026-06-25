# 🔒 Clase S-01: Seguridad Web con FastAPI y Nginx

**Duración:** 4 horas  
**Objetivo:** Crear una aplicación web segura con FastAPI y configurar Nginx con medidas de protección  
**Proyecto:** API protegida con rate limiting, headers de seguridad y defensa contra ataques comunes

---

## 📚 Contenido Teórico

### 1. Introducción a la Seguridad Web

#### 1.1 Tipos de Ataques Comunes

| Ataque | Descripción | Peligrosidad |
|--------|-------------|--------------|
| **DDoS** | Sobrecarga de servidores con peticiones masivas | ⚠️⚠️⚠️⚠️⚠️ |
| **Slowloris** | Conexiones lentas que agotan recursos | ⚠️⚠️⚠️⚠️ |
| **Brute Force** | Intentos repetidos de autenticación | ⚠️⚠️⚠️ |
| **SQL Injection** | Inyección de código SQL malicioso | ⚠️⚠️⚠️⚠️⚠️ |
| **XSS** | Scripts maliciosos en páginas web | ⚠️⚠️⚠️⚠️ |
| **CSRF** | Acciones no autorizadas en nombre del usuario | ⚠️⚠️⚠️ |

#### 1.2 Capas de Seguridad

```
┌─────────────────────────────────────────────────────────────┐
│                        FIREWALL (Nginx)                     │
│  - Rate Limiting    - Headers de seguridad                  │
│  - Bloqueo IP       - Timeout anti-Slowloris                 │
├─────────────────────────────────────────────────────────────┤
│                      APPLICATION (FastAPI)                   │
│  - Validación input  - Autenticación JWT                    │
│  - Sanitización      - Autorización                          │
├─────────────────────────────────────────────────────────────┤
│                        DATABASE                              │
│  - Permisos mínimos  - Prepared statements                   │
│  - Backups           - Encriptación                          │
└─────────────────────────────────────────────────────────────┘
```

---

## 💻 Contenido Práctico

### 2. Instalación de FastAPI

#### 2.1 Crear Proyecto

```bash
# Crear directorio del proyecto
mkdir mi-app-segura
cd mi-app-segura

# Crear entorno virtual
python -m venv venv

# Activar (Linux/Mac)
source venv/bin/activate

# Activar (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Activar (Windows CMD)
venv\Scripts\activate.bat

# Instalar dependencias
pip install fastapi uvicorn[standard] python-jose[cryptography] passlib[bcrypt] python-multipart pydantic-settings
```

#### 2.2 Estructura del Proyecto

```
mi-app-segura/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── eventos.py
│   └── utils/
│       ├── __init__.py
│       └── security.py
├── nginx/
│   ├── nginx.conf
│   └── sites-available/
│       └── mi-app
├── requirements.txt
└── .env
```

#### 2.3 Archivo requirements.txt

```txt
fastapi==0.109.0
uvicorn[standard]==0.27.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
pydantic-settings==2.1.0
pymongo==4.6.1
python-dotenv==1.0.0
```

---

### 3. Código de la Aplicación FastAPI

#### 3.1 Configuración (config.py)

```python
# app/config.py
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    APP_NAME: str = "Mi App Segura"
    DEBUG: bool = False
    
    # Seguridad
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    ALLOWED_ORIGINS: list[str] = ["https://midominio.com"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()
```

#### 3.2 Modelos/Schemas (models/schemas.py)

```python
# app/models/schemas.py
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UsuarioBase(BaseModel):
    email: EmailStr
    nombre: str

class UsuarioCreate(UsuarioBase):
    password: str = Field(..., min_length=8)

class UsuarioResponse(UsuarioBase):
    id: int
    creado_en: datetime
    
    class Config:
        from_attributes = True

class EventoBase(BaseModel):
    titulo: str = Field(..., min_length=3, max_length=100)
    descripcion: str
    precio: float = Field(..., ge=0)
    ubicacion: str

class EventoCreate(EventoBase):
    pass

class EventoResponse(EventoBase):
    id: int
    organizador_id: int
    fecha: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str
```

#### 3.3 Utilidades de Seguridad (utils/security.py)

```python
# app/utils/security.py
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.config import get_settings

settings = get_settings()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    return encoded_jwt

def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = decode_token(token)
    user_id: int = payload.get("sub")
    
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )
    
    return {"user_id": user_id, "email": payload.get("email")}
```

#### 3.4 Routers (routers/eventos.py)

```python
# app/routers/eventos.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.models.schemas import EventoCreate, EventoResponse
from app.utils.security import get_current_user

router = APIRouter(prefix="/api/eventos", tags=["eventos"])

# Base de datos simulada
eventos_db = []

@router.get("/", response_model=List[EventoResponse])
async def listar_eventos():
    return eventos_db

@router.get("/{evento_id}", response_model=EventoResponse)
async def obtener_evento(evento_id: int):
    for evento in eventos_db:
        if evento["id"] == evento_id:
            return evento
    raise HTTPException(status_code=404, detail="Evento no encontrado")

@router.post("/", response_model=EventoResponse, status_code=status.HTTP_201_CREATED)
async def crear_evento(
    evento: EventoCreate,
    current_user: dict = Depends(get_current_user)
):
    nuevo_evento = {
        "id": len(eventos_db) + 1,
        **evento.model_dump(),
        "organizador_id": current_user["user_id"],
        "fecha": "2024-03-15T20:00:00"
    }
    eventos_db.append(nuevo_evento)
    return nuevo_evento

@router.delete("/{evento_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_evento(
    evento_id: int,
    current_user: dict = Depends(get_current_user)
):
    for i, evento in enumerate(eventos_db):
        if evento["id"] == evento_id:
            if evento["organizador_id"] != current_user["user_id"]:
                raise HTTPException(status_code=403, detail="No autorizado")
            eventos_db.pop(i)
            return
    raise HTTPException(status_code=404, detail="Evento no encontrado")
```

#### 3.5 Router de Autenticación (routers/auth.py)

```python
# app/routers/auth.py
from fastapi import APIRouter, HTTPException, status
from datetime import timedelta
from app.models.schemas import UsuarioCreate, UsuarioResponse, Token, LoginRequest
from app.utils.security import hash_password, verify_password, create_access_token
from app.config import get_settings

router = APIRouter(prefix="/api/auth", tags=["autenticacion"])
settings = get_settings()

# Base de datos simulada de usuarios
usuarios_db = {}

@router.post("/register", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
async def registrar(usuario: UsuarioCreate):
    if usuario.email in usuarios_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )
    
    hashed_pw = hash_password(usuario.password)
    
    nuevo_usuario = {
        "id": len(usuarios_db) + 1,
        "email": usuario.email,
        "nombre": usuario.nombre,
        "password_hash": hashed_pw,
        "creado_en": "2024-01-01T00:00:00"
    }
    
    usuarios_db[usuario.email] = nuevo_usuario
    
    return {
        "id": nuevo_usuario["id"],
        "email": nuevo_usuario["email"],
        "nombre": nuevo_usuario["nombre"],
        "creado_en": nuevo_usuario["creado_en"]
    }

@router.post("/login", response_model=Token)
async def login(login_data: LoginRequest):
    usuario = usuarios_db.get(login_data.email)
    
    if not usuario or not verify_password(login_data.password, usuario["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(
        data={"sub": usuario["id"], "email": usuario["email"]},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    return {"access_token": access_token, "token_type": "bearer"}
```

#### 3.6 Aplicación Principal (main.py)

```python
# app/main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.config import get_settings
from app.routers import auth, eventos

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

# Exception Handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Error de validación",
            "errors": exc.errors()
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Error interno del servidor"}
    )

# Include Routers
app.include_router(auth.router)
app.include_router(eventos.router)

@app.get("/")
async def root():
    return {"message": "API de Eventos", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

#### 3.7 Archivo .env

```env
SECRET_KEY=tu-clave-secreta-muy-larga-y-compleja-aqui-2024
DEBUG=False
ALLOWED_ORIGINS=["https://midominio.com", "https://www.midominio.com"]
```

---

### 4. Instalación de Nginx

#### 4.1 Instalación en Ubuntu/Debian

```bash
# Actualizar paquetes
sudo apt update && sudo apt upgrade -y

# Instalar Nginx
sudo apt install nginx -y

# Verificar instalación
nginx -v

# Iniciar y habilitar
sudo systemctl start nginx
sudo systemctl enable nginx

# Verificar estado
sudo systemctl status nginx
```

#### 4.2 Instalación en CentOS/RHEL

```bash
# Instalar EPEL
sudo yum install epel-release -y

# Instalar Nginx
sudo yum install nginx -y

# Iniciar y habilitar
sudo systemctl start nginx
sudo systemctl enable nginx
```

#### 4.3 Instalación en macOS

```bash
# Con Homebrew
brew install nginx

# Iniciar
brew services start nginx

# Verificar
nginx -v
```

---

### 5. Configuración de Seguridad de Nginx

#### 5.1 Configuración Completa de Nginx

```bash
# Crear directorio para configuraciones
sudo mkdir -p /etc/nginx/sites-available
sudo mkdir -p /etc/nginx/sites-enabled

# Editar configuración principal
sudo nano /etc/nginx/nginx.conf
```

```nginx
# /etc/nginx/nginx.conf

user www-data;
worker_processes auto;
pid /run/nginx.pid;
error_log /var/log/nginx/error.log;

# Cargar módulos
load_module /usr/lib/nginx/modules/ngx_http_limit_conn_module.so;
load_module /usr/lib/nginx/modules/ngx_http_limit_req_module.so;

events {
    worker_connections 1024;
    use epoll;
    multi_accept on;
}

http {
    # =============================================================================
    # SEGURIDAD BÁSICA
    # =============================================================================
    
    # Ocultar versión de Nginx
    server_tokens off;
    
    # No mostrar errores personalizados que revelen información
    proxy_hide_header X-Powered-By;
    fastcgi_hide_header X-Powered-By;
    
    # Permitir solo los métodos HTTP necesarios
    limit_except GET POST PUT DELETE OPTIONS {
        deny all;
    }
    
    # =============================================================================
    # RATE LIMITING - Protección contra DDoS y Brute Force
    # =============================================================================
    
    # Zona de memoria para limitar conexiones simultáneas (10MB = ~160,000 IPs)
    limit_conn_zone $binary_remote_addr zone=addr:10m;
    
    # Zona de memoria para limitar peticiones por segundo
    # rate=5r/s = 5 peticiones por segundo
    limit_req_zone $binary_remote_addr zone=one:10m rate=5r/s;
    
    # Zona separada para el API (más restrictiva)
    limit_req_zone $binary_remote_addr zone=api:10m rate=3r/s;
    
    # =============================================================================
    # BUFFER SIZE - Prevención de ataques por overflow
    # =============================================================================
    
    client_body_buffer_size 16k;
    client_header_buffer_size 1k;
    client_max_body_size 8m;
    large_client_header_buffers 4 8k;
    
    # =============================================================================
    # TIMEOUTS - Defensa contra Slowloris
    # =============================================================================
    
    # Tiempo máximo para leer el cuerpo de la petición
    # Si el cliente es muy lento, se corta la conexión
    client_body_timeout 5s;
    
    # Tiempo máximo para leer las cabeceras (headers)
    client_header_timeout 5s;
    
    # Tiempo que una conexión puede estar "viva" sin hacer nada
    keepalive_timeout 5s;
    
    # Tiempo máximo para enviar la respuesta al cliente
    send_timeout 5s;
    
    # =============================================================================
    # CABECERAS DE SEGURIDAD (Headers)
    # =============================================================================
    
    # Previene MIME type sniffing
    add_header X-Content-Type-Options "nosniff" always;
    
    # Previene clickjacking
    add_header X-Frame-Options "SAMEORIGIN" always;
    
    # Protección XSS
    add_header X-XSS-Protection "1; mode=block" always;
    
    # Política de referencia
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    
    # Content Security Policy (CSP)
    # Ajusta según tu aplicación
    add_header Content-Security-Policy "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline';" always;
    
    # Permissions Policy
    add_header Permissions-Policy "geolocation=(), microphone=(), camera=()" always;
    
    # =============================================================================
    # CONFIGURACIÓN DE LOGS
    # =============================================================================
    
    log_format security '$remote_addr - $remote_user [$time_local] '
                        '"$request" $status $body_bytes_sent '
                        '"$http_referer" "$http_user_agent" '
                        '$request_time';
    
    access_log /var/log/nginx/access.log security;
    error_log /var/log/nginx/error.log warn;
    
    # =============================================================================
    # GZIP COMPRESSION
    # =============================================================================
    
    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types text/plain text/css text/xml application/json application/javascript 
               application/rss+xml application/atom+xml image/svg+xml;
    
    # =============================================================================
    # CONFIGURACIÓN GENERAL
    # =============================================================================
    
    include /etc/nginx/mime.types;
    default_type application/octet-stream;
    
    # Configuración de envío de archivos
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    types_hash_max_size 2048;
    
    # Incluir configuraciones de sitios
    include /etc/nginx/sites-enabled/*;
}
```

#### 5.2 Configuración del Sitio (Virtual Host)

```nginx
# /etc/nginx/sites-available/mi-app

# Servidor principal (HTTP)
server {
    listen 80;
    server_name midominio.com www.midominio.com;
    
    # Redirigir HTTP a HTTPS
    return 301 https://$server_name$request_uri;
}

# Servidor HTTPS
server {
    listen 443 ssl http2;
    server_name midominio.com www.midominio.com;
    
    # =============================================================================
    # CERTIFICADO SSL
    # =============================================================================
    
    ssl_certificate /etc/letsencrypt/live/midominio.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/midominio.com/privkey.pem;
    
    # Configuración SSL moderna
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    
    # OCSP Stapling
    ssl_stapling on;
    ssl_stapling_verify on;
    resolver 8.8.8.8 8.8.4.4 valid=300s;
    resolver_timeout 5s;
    
    # HSTS (HTTP Strict Transport Security)
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    
    # =============================================================================
    # ARCHIVOS ESTÁTICOS
    # =============================================================================
    
    root /var/www/mi-app/dist;
    index index.html;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    # Cache de archivos estáticos
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2)$ {
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    # =============================================================================
    # API - FastAPI (Uvicorn en puerto 8000)
    # =============================================================================
    
    location /api/ {
        # Rate limiting para API (más estricto)
        limit_req zone=api burst=10 nodelay;
        
        # Máximo 5 conexiones simultáneas por IP para API
        limit_conn addr 5;
        
        # Proxy al backend FastAPI
        proxy_pass http://127.0.0.1:8000;
        
        # Headers para el proxy
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Request-ID $request_id;
        
        # Timeouts del proxy
        proxy_connect_timeout 30s;
        proxy_send_timeout 30s;
        proxy_read_timeout 30s;
        
        # No buffering para respuestas grandes
        proxy_buffering off;
    }
    
    # =============================================================================
    # DOCUMENTACIÓN DE API (FastAPI Docs)
    # =============================================================================
    
    location /docs {
        proxy_pass http://127.0.0.1:8000/docs;
        proxy_set_header Host $host;
    }
    
    location /redoc {
        proxy_pass http://127.0.0.1:8000/redoc;
        proxy_set_header Host $host;
    }
    
    # =============================================================================
    # SEGURIDAD ADICIONAL
    # =============================================================================
    
    # Denegar acceso a archivos ocultos
    location ~ /\. {
        deny all;
        access_log off;
        log_not_found off;
    }
    
    # Denegar acceso a archivos de configuración
    location ~ \.(env|config|ini|yml|yaml)$ {
        deny all;
        access_log off;
        log_not_found off;
    }
    
    # Rate limiting por sesión (para login)
    location /api/auth/login {
        # Límite muy estricto para login (2 intentos por segundo)
        limit_req zone=api burst=3 nodelay;
        
        proxy_pass http://127.0.0.1:8000/api/auth/login;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /api/auth/register {
        limit_req zone=api burst=3 nodelay;
        
        proxy_pass http://127.0.0.1:8000/api/auth/register;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

### 6. Configuración de Systemd para FastAPI

```bash
# Crear archivo de servicio
sudo nano /etc/systemd/system/mi-app.service
```

```ini
[Unit]
Description=Mi App Segura - FastAPI
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/home/user/mi-app-segura
Environment="PATH=/home/user/mi-app-segura/venv/bin"
ExecStart=/home/user/mi-app-segura/venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000 --workers 4
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal

# Seguridad
NoNewPrivileges=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/home/user/mi-app-segura

[Install]
WantedBy=multi-user.target
```

```bash
# Recargar systemd, iniciar y habilitar
sudo systemctl daemon-reload
sudo systemctl start mi-app
sudo systemctl enable mi-app

# Verificar estado
sudo systemctl status mi-app
```

---

### 7. Instalar Certificados SSL con Let's Encrypt

```bash
# Instalar Certbot
sudo apt install certbot python3-certbot-nginx -y

# Generar certificado
sudo certbot --nginx -d midominio.com -d www.midominio.com

# Verificar renovación automática
sudo certbot renew --dry-run

# O añadir a crontab
sudo crontab -e
# Añadir línea:
# 0 0 * * * certbot renew --quiet
```

---

### 8. Verificar Configuración

```bash
# Probar configuración de Nginx
sudo nginx -t

# Recargar Nginx
sudo systemctl reload nginx

# Ver logs de seguridad
sudo tail -f /var/log/nginx/access.log | grep -E "5(00|29|21)|403|444"

# Monitorear conexiones activas
watch -n 1 'ss -s'
```

---

## 🛠️ Ejercicios Prácticos

### Ejercicio 1: Probar Rate Limiting
- Enviar múltiples peticiones rápidas y observar respuesta 429

### Ejercicio 2: Verificar Headers de Seguridad
```bash
curl -I https://midominio.com
```
Verificar que aparezcan: X-Frame-Options, X-Content-Type-Options, etc.

### Ejercicio 3: Test Slowloris
```bash
# Instalar slowloris
pip install slowloris

# Ejecutar ataque de prueba (solo en tu servidor)
slowloris midominio.com
```
Observar cómo Nginx corta las conexiones lentas.

### Ejercicio 4: Configurar Fail2Ban
```bash
sudo apt install fail2ban -y
sudo systemctl enable fail2ban
```

---

## 🚀 Proyecto de la Clase

### Sistema Completo de Seguridad

```
┌─────────────────────────────────────────────────────────────────┐
│                        INTERNET                                  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      NGINX (Firewall)                            │
│  - Rate Limiting: 5 req/s, burst 10                             │
│  - Timeouts: 5s anti-Slowloris                                  │
│  - Headers: X-Frame-Options, CSP, HSTS                          │
│  - SSL/TLS: TLS 1.2+ con cipher moderno                         │
│  - Bloqueo IP: fail2ban                                          │
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTPS (443)
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                  FASTAPI (Uvicorn)                               │
│  - JWT Authentication                                            │
│  - Validación de Input con Pydantic                             │
│  - CORS configurado                                              │
│  - Manejo de errores seguro                                      │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      BASE DE DATOS                               │
│  - MongoDB/PostgreSQL con permisos mínimos                       │
│  - Contraseñas hasheadas (bcrypt)                                │
│  - Prepared statements                                            │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📚 Recursos Adicionales

- [Nginx Security Best Practices](https://nginx.org/en/docs/security_contacts.html)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Mozilla SSL Configuration Generator](https://ssl-config.mozilla.org/)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)

---

## Checklist de Seguridad

- [ ] Nginx instalado y configurado
- [ ] Rate limiting activo
- [ ] Timeouts anti-Slowloris configurados
- [ ] Headers de seguridad añadidos
- [ ] SSL/TLS configurado con Let's Encrypt
- [ ] FastAPI con autenticación JWT
- [ ] Contraseñas hasheadas con bcrypt
- [ ] Validación de input activa
- [ ] Logs configurados
- [ ] Fail2Ban instalado
- [ ] Backups programados
