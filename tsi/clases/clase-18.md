# Clase 18: Autenticacion y Gestion de Sesiones

**Duracion:** 2 horas

---

## Objetivos de Aprendizaje

1. Identificar problemas comunes de autenticacion en aplicaciones web
2. Implementar almacenamiento seguro de contrasenas con algoritmos modernos
3. Comprender y gestionar sesiones de usuario con JWT y cookies seguras
4. Conocer los principios de MFA y las mejores practicas de OWASP

---

## Contenido Detallado

### 1. Problemas Comunes de Autenticacion

#### Credenciales Debiles
- Contrasenas cortas o sin complejidad
- Contrasenas por defecto (admin/admin, root/toor)
- Reutilizacion de contrasenas entre servicios

#### Fuerza Bruta (Brute Force)
Ataque sistematico probando multiples combinaciones de usuario/contrasena.

```
Tasas de Ataque de Fuerza Bruta
+------------------+------------------------+
| Tipo             | Intentos por segundo   |
+------------------+------------------------+
| Manual           | 1-5                    |
| Script basico    | 100-500                |
| Botnet           | 10,000+                |
| GPGPU (local)    | 1,000,000,000+ (hash) |
+------------------+------------------------+
```

#### Credenciales por Defecto
Dispositivos y software que mantienen credenciales de fabrica sin cambios.

| Dispositivo  | Usuario  | Contrasena |
|-------------|----------|------------|
| Router TP-Link | admin | admin |
| Camara IP Hikvision | admin | 12345 |
| MySQL | root | (vacia) |
| Tomcat | admin | admin |

#### Session Hijacking
Robo del identificador de sesion de un usuario para suplantarlo.

```
Metodos comunes de session hijacking:
1. Sniffing de trafico no cifrado
2. XSS para robar cookies
3. Prediccion de ID de sesion
4. Session fixation
5. Ataque a la red local (ARP spoofing)
```

### 2. Almacenamiento Seguro de Contrasenas

#### Hashing vs. Encriptacion

```
HASHING (unidireccional):
password + salt --> hash_function --> hash_value
Hash -> password: IMPOSIBLE (funcion de un solo sentido)

ENCRIPTACION (bidireccional):
password + clave --> encrypt_function --> ciphertext
ciphertext + clave --> decrypt_function --> password
```

| Caracteristica | Hashing | Encriptacion |
|---------------|---------|-------------|
| Direccion | Un solo sentido | Reversible |
| Uso en passwords | SI (almacenar verificacion) | NO (necesita clave secreta) |
| Clave necesaria? | No (usa salt) | Si (clave de cifrado) |
| Seguridad para passwords | Alta (si el algoritmo es bueno) | Baja (si roban clave, ven todos) |

#### Algoritmos Recomendados

| Algoritmo | Tipo | Iteraciones | Recomendado? |
|-----------|------|-------------|-------------|
| MD5 | Hash | 1 | NO (colisiones conocidas, 2^0.5s) |
| SHA-1 | Hash | 1 | NO (colisiones demostradas 2017) |
| SHA-256/512 | Hash | 1 | NO para passwords (muy rapido para GPU) |
| **bcrypt** | Slow hash | 10-14 | **SI** (diseno especifico para passwords) |
| **PBKDF2** | Slow hash | 310,000+ | **SI** (recomendado por NIST) |
| **Argon2** | Slow hash | variable | **SI** (ganador PHC 2015, el mas moderno) |

#### bcrypt en detalle

bcrypt incluye automaticamente el salt en el output, no necesita almacenamiento separado.

```python
import bcrypt

# Hash de contrasena
password = b"MiPasswordSegura123"
salt = bcrypt.gensalt(rounds=12)  # rounds=12 es un buen balance
hashed = bcrypt.hashpw(password, salt)

print(f"Hash: {hashed}")
# Output: b'$2b$12$Qx4u7Y9yR3zS2wV5kL8j6O5m2n3p4q5r6s7t8u9v0w1x2y3z4A5B6C'

# Verificacion
if bcrypt.checkpw(password, hashed):
    print("Contrasena correcta!")
```

#### Almacenamiento Seguro
```
NUNCA almacenar:
- Contrasenas en texto plano
- Contrasenas en logs
- Contrasenas en archivos de configuracion
- Contrasenas cifradas (en vez de hasheadas)

SIEMPRE almacenar:
- Hash de la contrasena + salt (bcrypt/Argon2)
- En columna separada de la base de datos
- Con los menores privilegios de acceso posibles
```

### 3. Gestion de Sesiones

#### Tokens JWT (JSON Web Tokens)

JWT es un estandar abierto (RFC 7519) para transmitir informacion entre partes como un objeto JSON compacto y autónomo.

**Estructura de un JWT:**

```
Header.Payload.Signature
```

```
HEADER:
{
  "alg": "HS256",
  "typ": "JWT"
}

PAYLOAD:
{
  "sub": "1234567890",
  "name": "Juan Perez",
  "iat": 1516239022,
  "exp": 1516242622,
  "role": "admin"
}

SIGNATURE:
HMACSHA256(
  base64UrlEncode(header) + "." +
  base64UrlEncode(payload),
  secret_key
)
```

**JWT en formato string:**
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.
eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6Ikp1YW4gUGVyZXoiLCJpYXQiOjE1MTYyMzkwMjIsImV4cCI6MTUxNjI0MjYyMn0.
SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

#### Cookies Seguras

| Atributo | Significado | Recomendacion |
|----------|------------|--------------|
| **HttpOnly** | No accesible desde JavaScript | SIEMPRE (previene XSS robo de cookies) |
| **Secure** | Solo se envia por HTTPS | SIEMPRE |
| **SameSite** | Controla envio cross-site | `Strict` o `Lax` (previene CSRF) |
| **Path** | Limita ruta de envio | Especifico (/api) |
| **Domain** | Limita dominio | Sin comodin si es posible |
| **Max-Age/Expires** | Tiempo de vida | 15-60 min para sesion, mas para recuerdame |

#### OWASP Session Management Cheat Sheet

Recomendaciones clave:

1. **Generar IDs de sesion con fuentes seguras:** `crypto.randomBytes()` en Node, `secrets.token_hex()` en Python
2. **Longitud minima de 128 bits** para el identificador
3. **Expiracion de sesion:** Inactividad (15-30 min), absoluta (8-24 horas)
4. **Regenerar ID de sesion** despues del login exitoso (previene session fixation)
5. **Invalidar sesion** al logout (servidor y cliente)
6. **No exponer ID en URLs** (usar cookies HttpOnly)
7. **Almacen del lado seguro** (no confiar en datos del cliente sin verificar)

### 4. MFA (Multi-Factor Authentication)

Factores de autenticacion:

| Factor | Ejemplo | Descripcion |
|--------|---------|-------------|
| Algo que sabes | Contrasena, PIN | Conocimiento |
| Algo que tienes | Telefono, token fisico, tarjeta | Posesion |
| Algo que eres | Huella dactilar, reconocimiento facial | Herencia |

**TOTP (Time-based One-Time Password):**
```python
import pyotp
import qrcode

# Generar secreto
secret = pyotp.random_base32()
print(f"Secreto: {secret}")
# 'JBSWY3DPEHPK3PXP'

# Generar codigo TOTP (valido 30 segundos)
totp = pyotp.TOTP(secret)
codigo = totp.now()
print(f"Codigo actual: {codigo}")

# Verificar
print(totp.verify(codigo))        # True
print(totp.verify("000000"))      # False
```

---

## Ejercicio 1: Registro y Login con Flask + bcrypt

```python
# app.py - Aplicacion Flask con autenticacion segura
import sqlite3
from flask import Flask, request, jsonify, session, make_response
import bcrypt
import secrets
from datetime import datetime, timedelta
import re

app = Flask(__name__)
# Usar una clave secreta segura, no hardcodeada en produccion
app.config['SECRET_KEY'] = secrets.token_hex(32)
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = True     # Solo HTTPS
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

DB_PATH = 'users.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            mfa_secret TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Validar: min 8 chars, 1 mayuscula, 1 minuscula, 1 numero"""
    if len(password) < 8:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'[0-9]', password):
        return False
    return True

# --- Endpoints ---

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Datos requeridos'}), 400

    username = data.get('username', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '')

    # Validaciones
    if not username or len(username) < 3:
        return jsonify({'error': 'Username debe tener al menos 3 caracteres'}), 400
    if not validate_email(email):
        return jsonify({'error': 'Email invalido'}), 400
    if not validate_password(password):
        return jsonify({'error': 'Password debe tener 8+ caracteres, mayuscula, minuscula y numero'}), 400

    # Hash de contrasena con bcrypt
    password_hash = bcrypt.hashpw(
        password.encode('utf-8'),
        bcrypt.gensalt(rounds=12)
    ).decode('utf-8')

    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO usuarios (email, username, password_hash) VALUES (?, ?, ?)",
            (email, username, password_hash)
        )
        conn.commit()
        return jsonify({'message': 'Usuario registrado exitosamente'}), 201
    except sqlite3.IntegrityError as e:
        return jsonify({'error': 'El usuario o email ya existe'}), 409
    finally:
        conn.close()

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Datos requeridos'}), 400

    username = data.get('username', '').strip()
    password = data.get('password', '')

    conn = get_db()
    cursor = conn.cursor()

    # Consulta parametrizada (segura contra inyeccion SQL)
    cursor.execute(
        "SELECT id, username, password_hash FROM usuarios WHERE username = ?",
        (username,)
    )
    user = cursor.fetchone()
    conn.close()

    if not user:
        return jsonify({'error': 'Credenciales invalidas'}), 401

    # Verificar contrasena con bcrypt
    stored_hash = user['password_hash'].encode('utf-8')
    if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
        # Regenerar sesion (previene session fixation)
        session.clear()
        session.permanent = True
        session['user_id'] = user['id']
        session['username'] = user['username']

        return jsonify({
            'message': 'Login exitoso',
            'user': {'id': user['id'], 'username': user['username']}
        }), 200
    else:
        return jsonify({'error': 'Credenciales invalidas'}), 401

@app.route('/api/logout', methods=['POST'])
def logout():
    # Invalidar sesion
    session.clear()
    response = jsonify({'message': 'Sesion cerrada'})
    # Eliminar cookie de sesion del cliente
    response.set_cookie('session', '', expires=0)
    return response, 200

@app.route('/api/perfil', methods=['GET'])
def perfil():
    # Verificar autenticacion
    if 'user_id' not in session:
        return jsonify({'error': 'No autenticado'}), 401

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, username, email, created_at FROM usuarios WHERE id = ?",
        (session['user_id'],)
    )
    user = cursor.fetchone()
    conn.close()

    if not user:
        session.clear()
        return jsonify({'error': 'Usuario no encontrado'}), 404

    return jsonify({
        'id': user['id'],
        'username': user['username'],
        'email': user['email'],
        'created_at': user['created_at']
    }), 200

if __name__ == '__main__':
    init_db()
    # En produccion: usar HTTPS, debug=False
    app.run(debug=False, host='0.0.0.0', port=5000)
```

### Explicacion del codigo:

1. **bcrypt:** Se usa `gensalt(rounds=12)` - 2^12 = 4096 iteraciones, balance seguridad/rendimiento
2. **Sesiones seguras:** Cookies con HttpOnly, Secure, SameSite=Lax
3. **Regeneracion de sesion:** Se llama a `session.clear()` antes de establecer datos de sesion en login
4. **Politica de contrasenas:** 8+ caracteres, mayuscula, minuscula, numero
5. **Consultas parametrizadas:** Todas las operaciones SQL usan `?` placeholders
6. **Mensajes genericos:** No revelar si el usuario existe ("Credenciales invalidas")
7. **Validacion de email:** Expresion regular para formato basico

---

## Ejercicio 2: Analisis de Token JWT

**Token dado:**
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.
eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6Ikp1YW4gUGVyZXoiLCJyb2xlIjoidXNlciIsImlhdCI6MTcwMDAwMDAwMCwiZXhwIjoxNzAwMDAzNjAwfQ.
kQk7X5mN2z8L6y2sY5w9K4p3n2m1b6c5d4e3f2g1h0i9j8k7l6m5n4o3p2
```

### Analisis paso a paso:

**Paso 1: Decodificar Header**
```python
import base64
import json

def decode_base64url(s):
    padding = 4 - len(s) % 4
    if padding != 4:
        s += '=' * padding
    return base64.urlsafe_b64decode(s)

header_b64 = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
header = json.loads(decode_base64url(header_b64))
print(json.dumps(header, indent=2))
# {
#   "alg": "HS256",      # HMAC con SHA-256
#   "typ": "JWT"         # Tipo: JWT
# }
```

**Paso 2: Decodificar Payload**
```python
payload_b64 = "eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6Ikp1YW4gUGVyZXoiLCJyb2xlIjoidXNlciIsImlhdCI6MTcwMDAwMDAwMCwiZXhwIjoxNzAwMDAzNjAwfQ"
payload = json.loads(decode_base64url(payload_b64))
print(json.dumps(payload, indent=2))
# {
#   "sub": "1234567890",    # Subject (ID del usuario)
#   "name": "Juan Perez",   # Nombre
#   "role": "user",         # Rol (user/admin)
#   "iat": 1700000000,      # Issued At (fecha emision)
#   "exp": 1700003600       # Expiration (fecha expiracion, 1 hora despues)
# }
```

**Paso 3: Verificar Firma**
```python
import hmac
import hashlib

signature_b64 = "kQk7X5mN2z8L6y2sY5w9K4p3n2m1b6c5d4e3f2g1h0i9j8k7l6m5n4o3p2"

# Calcular firma esperada (necesitamos la clave secreta)
secret_key = "mi_clave_secreta_super_segura"
message = f"{header_b64}.{payload_b64}"
expected_signature = hmac.new(
    secret_key.encode('utf-8'),
    message.encode('utf-8'),
    hashlib.sha256
).digest()

expected_b64 = base64.urlsafe_b64encode(expected_signature).rstrip('=').decode('utf-8')

print(f"Firma dada:      {signature_b64}")
print(f"Firma esperada:  {expected_b64}")
print(f"Firma valida:    {signature_b64 == expected_b64}")
```

**Paso 4: Verificar Claims de Seguridad**
- **iat:** 1700000000 -> Fecha emision: 2023-11-14 (fecha pasada)
- **exp:** 1700003600 -> Fecha expiracion: 2023-11-14 + 1h
- La expiracion debe verificarse: si `time.time() > exp`, rechazar token
- El **rol es "user"**, pero deberia validarse contra la BD
- El token NO tiene `nbf` (Not Before) ni `jti` (JWT ID)

**Paso 5: Ataque potencial - None Algorithm**
Si el servidor acepta `"alg": "none"`, el atacante puede modificar el header:
```json
// Header modificado
{ "alg": "none", "typ": "JWT" }

// Cualquier payload con role: admin
{ "sub": "123", "name": "Juan Perez", "role": "admin", "iat": 1700000000, "exp": 9999999999 }

// Firma: "" (vacia)
// Token resultante: eyJhbGciOiAibm9uZSIsICJ0eXAiOiAiSldUIn0.eyJzdWIiOiIxMjMiLCJuYW1lIjoiSnVhbiBQZXJleiIsInJvbGUiOiJhZG1pbiIsImlhdCI6MTcwMDAwMDAwMCwiZXhwIjo5OTk5OTk5OTk5fQ.
```

Conclusión: el token usa HS256 (simetrico), el payload contiene rol "user", expira en 1 hora. Las vulnerabilidades potenciales incluyen: clave secreta debil (ataque de diccionario), algoritmo none, rol definido en el token (podria modificarse).

---

## Preguntas y Respuestas

### Pregunta 1
**Cual es la diferencia fundamental entre hashing y encriptacion en el contexto de contrasenas?**

**Respuesta:** El hashing es unidireccional: una vez que se genera el hash, no se puede revertir para obtener la contrasena original. La encriptacion es bidireccional: los datos cifrados pueden descifrarse con la clave correcta. Para contrasenas, SIEMPRE debe usarse hashing (con salt y algoritmo lento como bcrypt/Argon2), NUNCA encriptacion. Si alguien roba la clave de encriptacion, puede descifrar todas las contrasenas. Con hashing, incluso si roban la BD, las contrasenas no pueden recuperarse (solo mediante fuerza bruta del hash individual).

### Pregunta 2
**Que es CSRF y como se previene con cookies seguras?**

**Respuesta:** CSRF (Cross-Site Request Forgery) es un ataque donde el atacante enga~na al navegador de la victima para que envie una peticion no deseada a un sitio donde la victima esta autenticada. Ejemplo: si estas logueado en tu banco y visitas un sitio malicioso, ese sitio puede enviar un POST para transferir dinero usando tu sesion activa. La defensa principal es el atributo `SameSite` en cookies: `SameSite=Strict` evita que la cookie se envie en peticiones de otros orígenes. Tambien se usan tokens CSRF (generados por servidor, validados en cada formulario/API).

### Pregunta 3
**Que es session fixation y como se previene?**

**Respuesta:** Session fixation es un ataque donde el atacante establece (fija) el ID de sesion de la victima antes de que esta se autentique. Si la aplicacion no regenera el ID despues del login, el atacante conoce el ID de sesion valido y puede suplantar a la victima. Prevencion: despues de un login exitoso, la aplicacion debe regenerar/emitir un nuevo ID de sesion. En Flask: `session.clear()` seguido de establecer los datos. En general: `session_regenerate_id()`.

### Pregunta 4
**JWT es inherentemente seguro? Que practicas debe seguirse para usarlo correctamente?**

**Respuesta:** JWT no es inherentemente seguro; la seguridad depende de como se implementa. Practicas necesarias: (1) usar algoritmos asimetricos (RS256/ES256) en vez de simetricos (HS256) cuando multiples servicios verifican el token; (2) verificar siempre la firma (nunca aceptar "alg: none"); (3) validar exp, nbf, iat; (4) incluir jti (JWT ID) unico para prevenir replay; (5) usar HTTPS para evitar interceptacion; (6) almacenar JWT en HttpOnly cookie, no en localStorage (vulnerable a XSS); (7) rotar claves periodicamente; (8) no incluir datos sensibles en el payload (solo se codifica en base64, no se cifra).

### Pregunta 5
**Cuando usar bcrypt vs Argon2? Cual es la recomendacion actual?**

**Respuesta:** Argon2 es el algoritmo mas moderno (ganador del Password Hashing Competition 2015) y recomendado por OWASP como primera opcion. Sin embargo, bcrypt sigue siendo ampliamente usado y es seguro si se configura con rounds >= 10. Argon2 tiene tres variantes: Argon2d (resistente a GPU), Argon2i (resistente a side-channel), Argon2id (híbrido, recomendado). La recomendacion actual: usar Argon2id si la libreria esta disponible (ej: `argon2-cffi` en Python). Si no, bcrypt con rounds 12 es perfectamente aceptable. Lo importante es no usar algoritmos rapidos (MD5, SHA-256 directo, SHA-512 directo) para contrasenas.

---

## Tarea / Lectura Recomendada

1. **Leer:** OWASP Authentication Cheat Sheet - https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html
2. **Leer:** OWASP Session Management Cheat Sheet - https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html
3. **Leer:** JWT.io - Debugger y documentacion - https://jwt.io/
4. **Practicar:** Implementar login con MFA (TOTP) en Flask usando la libreria `pyotp`
5. **Profundizar:** Leer "Introduction to JWT" de Auth0 - https://auth0.com/learn/json-web-tokens
6. **Experimentar:** Usar Burp Suite para interceptar y analizar tokens JWT en una app de prueba



