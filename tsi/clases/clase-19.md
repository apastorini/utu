# Clase 19: Exposicion de Datos Sensibles

**Duracion:** 2 horas

---

## Objetivos de Aprendizaje

1. Identificar que constituyen datos sensibles en diferentes contextos
2. Comprender y aplicar cifrado en transito (TLS/SSL) y en reposo (AES, RSA)
3. Reconocer practicas inseguras de manejo de datos sensibles
4. Conocer los principios basicos de normativas: PCI DSS, GDPR, HIPAA

---

## Contenido Detallado

### 1. Que son Datos Sensibles?

Datos sensibles son cualquier informacion que, si se expone, puede causar dano a individuos, organizaciones o sistemas.

#### Categorias de Datos Sensibles

| Categoria | Ejemplos | Regulacion |
|-----------|----------|------------|
| **PII (Personally Identifiable Information)** | Nombre, DNI, email, direccion, telefono, IP | GDPR, CCPA, LGPD |
| **Datos Financieros** | Numero de tarjeta, CVV, cuenta bancaria, saldos | PCI DSS |
| **Datos de Salud** | Historial medico, diagnostico, recetas, seguro medico | HIPAA |
| **Credenciales** | Contrasenas, tokens, claves API, certificados | - |
| **Propiedad Intelectual** | Codigo fuente, secretos comerciales, patentes | - |
| **Datos Biométricos** | Huellas dactilares, reconocimiento facial, ADN | GDPR (categoria especial) |

```
Clasificacion de Datos por Sensibilidad
+--------------------------------------------------+
| ALTA                                               |
| - Credenciales de acceso                          |
| - Datos de pago (NUM, CVV)                        |
| - Datos de salud                                  |
| - Secretos comerciales                            |
+--------------------------------------------------+
| MEDIA                                              |
| - PII (nombre, email, direccion)                  |
| - Historial de transacciones                      |
| - Datos de uso del sistema                        |
+--------------------------------------------------+
| BAJA                                               |
| - Datos publicos                                  |
| - Contenido de sitios web publicos                |
| - Informacion agregada y anonimizada              |
+--------------------------------------------------+
```

### 2. Cifrado en Transito: TLS/SSL

El cifrado en transito protege los datos mientras viajan entre el cliente y el servidor (o entre servidores).

#### Como funciona TLS 1.3

```
CLIENTE                              SERVIDOR
   |                                     |
   |---- ClientHello                  -->|
   |                                     |
   |<--- ServerHello + Certificado    ---|
   |                                     |
   |<--- ServerKeyExchange             --|
   |                                     |
   |---- ClientKeyExchange            -->|
   |  (cifra clave pre-master con       |
   |   clave publica del servidor)      |
   |                                     |
   |---- ChangeCipherSpec             -->|
   |<--- ChangeCipherSpec              --|
   |                                     |
   |===== CANAL CIFRADO ================|
   |<--- Datos protegidos (AES-GCM)   -->
```

#### Conceptos Clave de TLS

| Concepto | Explicacion |
|----------|------------|
| **Certificado digital** | Documento electronico que vincula una identidad (dominio) con una clave publica, firmado por una CA |
| **CA (Certificate Authority)** | Entidad confiable que emite certificados (Let's Encrypt, DigiCert, GlobalSign) |
| **Handshake TLS** | Proceso inicial donde cliente y servidor acuerdan algoritmos y establecen claves compartidas |
| **Cipher suite** | Conjunto de algoritmos (ej: TLS_AES_256_GCM_SHA384) |
| **Perfect Forward Secrecy (PFS)** | Propiedad donde comprometer la clave privada a largo plazo no permite descifrar sesiones pasadas |

#### Implementacion de HTTPS en Flask

```python
from flask import Flask
import ssl

app = Flask(__name__)

@app.route('/')
def index():
    return "Conexion segura!"

if __name__ == '__main__':
    # Configurar SSL con certificado autofirmado
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain('cert.pem', 'key.pem')
    app.run(ssl_context=context, host='0.0.0.0', port=443)
```

#### Forzar HTTPS en Flask

```python
from flask import Flask, redirect, request

app = Flask(__name__)

@app.before_request
def force_https():
    if not request.is_secure:
        url = request.url.replace('http://', 'https://', 1)
        return redirect(url, code=301)
```

#### Headers de Seguridad para HTTPS

```python
@app.after_request
def add_security_headers(response):
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    return response
```

### 3. Cifrado en Reposo

El cifrado en reposo protege los datos cuando estan almacenados (disco, BD, backups).

#### Cifrado de Base de Datos

```
NIVELES DE CIFRADO EN BD
+-------------------------------------------------------+
| Aplicacion (application-level encryption)              |
| - Datos cifrados antes de enviar a BD                 |
| - Ventaja: la BD nunca ve datos en texto plano         |
| - Desventaja: no se pueden hacer busquedas en esos     |
|   campos sin descifrar                                 |
+-------------------------------------------------------+
| Base de Datos (TDE - Transparent Data Encryption)     |
| - Cifrado a nivel de pagina/archivo de BD             |
| - Transparente para la aplicacion                     |
| - Protege archivos de BD robados                      |
+-------------------------------------------------------+
| Disco/Archivos (FDE - Full Disk Encryption)            |
| - BitLocker, LUKS, FileVault                          |
| - Protege si roban el disco fisico                    |
| - No protege contra acceso via SO (si la BD esta      |
|   montada)                                             |
+-------------------------------------------------------+
```

#### Cifrado de Archivos

```python
# Cifrado de archivo completo con clave derivada de contrasena
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import base64
import os

def encrypt_file(password, input_file, output_file):
    # Derivar clave de la contrasena
    salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    f = Fernet(key)

    # Cifrar archivo
    with open(input_file, 'rb') as f_in:
        data = f_in.read()
    encrypted = f.encrypt(data)

    with open(output_file, 'wb') as f_out:
        f_out.write(salt + encrypted)  # Guardar salt + datos cifrados

def decrypt_file(password, input_file, output_file):
    with open(input_file, 'rb') as f_in:
        salt = f_in.read(16)
        encrypted = f_in.read()

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    f = Fernet(key)

    decrypted = f.decrypt(encrypted)
    with open(output_file, 'wb') as f_out:
        f_out.write(decrypted)
```

### 4. AES vs. RSA: Cuando Usar Cada Uno

| Caracteristica | AES (Simetrico) | RSA (Asimetrico) |
|---------------|----------------|-----------------|
| Claves | Unica clave compartida | Par: publica + privada |
| Velocidad | Muy rapido | Lento (100-1000x mas lento) |
| Tamano de clave | 128, 192, 256 bits | 2048, 4096 bits |
| Uso tipico | Cifrar datos grandes | Intercambiar claves, firmas |
| Cifrado por bloques | 128 bits | Variable (con padding) |

**Regla practica:** Usar RSA para intercambiar claves AES, y AES para cifrar datos.

```
Proceso tipico (hybrid encryption):
1. Generar clave AES aleatoria (256 bits)
2. Cifrar datos con AES-GCM (rapido, datos grandes)
3. Cifrar clave AES con RSA publica del destinatario (solo clave)
4. Enviar: datos_cifrados + clave_aes_cifrada_con_rsa

El destinatario:
1. Descifrar clave AES con su RSA privada
2. Descifrar datos con AES
```

#### AES-256 en Python

```python
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os
import base64

def aes_encrypt(key_hex: str, plaintext: str) -> dict:
    """Cifrar texto con AES-256-GCM"""
    key = bytes.fromhex(key_hex)
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)  # 96 bits recomendado para GCM
    ciphertext = aesgcm.encrypt(nonce, plaintext.encode('utf-8'), None)
    return {
        'nonce': base64.b64encode(nonce).decode('utf-8'),
        'ciphertext': base64.b64encode(ciphertext).decode('utf-8')
    }

def aes_decrypt(key_hex: str, nonce_b64: str, ciphertext_b64: str) -> str:
    """Descifrar texto con AES-256-GCM"""
    key = bytes.fromhex(key_hex)
    nonce = base64.b64decode(nonce_b64)
    ciphertext = base64.b64decode(ciphertext_b64)
    aesgcm = AESGCM(key)
    plaintext = aesgcm.decrypt(nonce, ciphertext, None)
    return plaintext.decode('utf-8')

# Ejemplo de uso
key = os.urandom(32).hex()  # 32 bytes = 256 bits
print(f"Clave AES: {key}")

# Cifrar
result = aes_encrypt(key, "Datos sensibles: Tarjeta 4532-1234-5678-9012")
print(f"Nonce: {result['nonce']}")
print(f"Cifrado: {result['ciphertext']}")

# Descifrar
decrypted = aes_decrypt(key, result['nonce'], result['ciphertext'])
print(f"Descifrado: {decrypted}")
```

#### RSA en Python

```python
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
import base64

# Generar par de claves RSA
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)

public_key = private_key.public_key()

# Cifrar con clave publica
def rsa_encrypt(public_key_pem: bytes, plaintext: str) -> str:
    public_key = serialization.load_pem_public_key(public_key_pem)
    ciphertext = public_key.encrypt(
        plaintext.encode('utf-8'),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return base64.b64encode(ciphertext).decode('utf-8')

# Descifrar con clave privada
def rsa_decrypt(private_key_pem: bytes, ciphertext_b64: str) -> str:
    private_key = serialization.load_pem_private_key(
        private_key_pem,
        password=None,
    )
    ciphertext = base64.b64decode(ciphertext_b64)
    plaintext = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return plaintext.decode('utf-8')

# Uso
pub_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)
priv_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

cifrado = rsa_encrypt(pub_pem, "Mensaje secreto con RSA")
print(f"Cifrado: {cifrado}")
descifrado = rsa_decrypt(priv_pem, cifrado)
print(f"Descifrado: {descifrado}")
```

### 5. Practicas Inseguras

| Practica Insegura | Ejemplo | Consecuencia | Solucion |
|-------------------|---------|-------------|----------|
| Texto plano en BD | `INSERT INTO usuarios VALUES ('admin', 'password123')` | Cualquier leak expone datos | Hashing + cifrado |
| Contrasenas en codigo | `DB_PASSWORD = "admin123"` | Acceso via repositorio | Variables de entorno / Vault |
| Logs expuestos | `logger.info(f"Login: {username}:{password}")` | Datos en logs accesibles | Nunca loguear datos sensibles |
| Datos en URLs | `/api/usuario?token=abc123&role=admin` | Cache, referer, logs | Usar headers Authorization |
| Backups sin cifrar | Backup de BD en S3 sin encriptar | Robo de backup = robo de datos | Cifrar backups |
| Headers inseguros | Sin HSTS, CORS mal configurado | Interceptacion, acceso cross-origin | Configurar headers de seguridad |

### 6. Regulaciones (Mencion)

| Regulacion | Ambito | Sancion Maxima | Requisito Clave |
|------------|--------|---------------|-----------------|
| **PCI DSS** | Datos de tarjetas de pago | $500,000/mes + perdida de licencia | Cifrar datos de tarjeta almacenados |
| **GDPR** | Datos personales de ciudadanos UE | 20M EUR o 4% factura global | Consentimiento, notificacion de brechas |
| **HIPAA** | Datos de salud en EE.UU. | $1.5M/anual | Cifrado, control de acceso, auditoria |

---

## Ejercicio 1: Implementar Cifrado AES-256 en Python para Datos Sensibles

Desarrollar un modulo completo para cifrar datos sensibles antes de almacenarlos.

```python
"""
secure_storage.py - Modulo de cifrado para datos sensibles
Uso: cifrar datos de tarjeta de credito antes de almacenar en BD
"""
import os
import base64
import json
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

class SecureStorage:
    """Clase para manejar cifrado de datos sensibles"""

    def __init__(self, master_key_hex=None):
        """Inicializar con clave maestra. Si no se provee, generar una nueva."""
        if master_key_hex:
            self.master_key = bytes.fromhex(master_key_hex)
            if len(self.master_key) != 32:
                raise ValueError("La clave maestra debe ser 32 bytes (256 bits)")
        else:
            self.master_key = os.urandom(32)

    def get_master_key_hex(self):
        """Obtener clave maestra en hex para almacenar seguramente"""
        return self.master_key.hex()

    def encrypt_data(self, plaintext: str) -> str:
        """
        Cifrar un string de datos sensibles.
        Retorna string JSON con: nonce (b64) + ciphertext (b64)
        """
        aesgcm = AESGCM(self.master_key)
        nonce = os.urandom(12)
        ciphertext = aesgcm.encrypt(nonce, plaintext.encode('utf-8'), None)

        result = {
            'nonce': base64.b64encode(nonce).decode('utf-8'),
            'ct': base64.b64encode(ciphertext).decode('utf-8'),
        }
        return json.dumps(result)

    def decrypt_data(self, encrypted_json: str) -> str:
        """
        Descifrar datos previamente cifrados.
        Recibe el string JSON generado por encrypt_data.
        """
        data = json.loads(encrypted_json)
        nonce = base64.b64decode(data['nonce'])
        ciphertext = base64.b64decode(data['ct'])

        aesgcm = AESGCM(self.master_key)
        plaintext = aesgcm.decrypt(nonce, ciphertext, None)
        return plaintext.decode('utf-8')

class CreditCardProcessor:
    """Procesador de tarjetas que cifra datos antes de almacenar"""

    def __init__(self):
        self.storage = SecureStorage()
        self.cards_db = {}  # Simula BD

    def add_card(self, user_id: str, card_number: str, cvv: str, expiry: str):
        """Almacenar tarjeta cifrada"""
        # NUNCA almacenar CVV completo en BD real (PCI DSS prohibe)
        # Aqui solo como demostracion educativa
        card_data = json.dumps({
            'number': card_number[-4:].zfill(16),  # Solo ultimos 4 digitos
            'cvv_hash': hashlib.sha256(cvv.encode()).hexdigest()[:8],  # Hash del CVV
            'expiry': expiry,
            'issuer': self._detect_issuer(card_number)
        })
        encrypted = self.storage.encrypt_data(card_data)
        self.cards_db[user_id] = encrypted
        return "Tarjeta almacenada de forma segura"

    def get_card_preview(self, user_id: str) -> dict:
        """Obtener datos no sensibles de la tarjeta"""
        if user_id not in self.cards_db:
            return None
        decrypted = self.storage.decrypt_data(self.cards_db[user_id])
        return json.loads(decrypted)

    def _detect_issuer(self, card_number: str) -> str:
        if card_number.startswith('4'):
            return 'Visa'
        elif card_number.startswith(('51', '52', '53', '54', '55')):
            return 'Mastercard'
        elif card_number.startswith('34') or card_number.startswith('37'):
            return 'Amex'
        return 'Unknown'

# --- Demostracion ---
if __name__ == "__main__":
    import hashlib

    processor = CreditCardProcessor()

    # Almacenar tarjeta (simulado)
    result = processor.add_card(
        'user_001',
        '4532123456789012',
        '123',
        '12/28'
    )
    print(result)

    # Recuperar datos (solo ultimos 4 digitos)
    preview = processor.get_card_preview('user_001')
    print(f"Datos recuperados: {json.dumps(preview, indent=2)}")
    # {
    #   "number": "0000000000009012",
    #   "cvv_hash": "a1b2c3d4",
    #   "expiry": "12/28",
    #   "issuer": "Visa"
    # }

    # Verificar que el cifrado es diferente cada vez (nonce aleatorio)
    card_data = '{"number": "0000000000009012", "expiry": "12/28"}'
    enc1 = processor.storage.encrypt_data(card_data)
    enc2 = processor.storage.encrypt_data(card_data)
    print(f"Mismo texto, cifrado 1: {enc1[:50]}...")
    print(f"Mismo texto, cifrado 2: {enc2[:50]}...")
    print(f"Son diferentes: {enc1 != enc2}")  # True por nonce aleatorio

    print("Clave maestra (guardar seguramente):", processor.storage.get_master_key_hex())
```

### Principios aplicados:
1. **AES-256-GCM:** Cifrado autenticado (protege confidencialidad e integridad)
2. **Nonce aleatorio:** Mismo texto plano produce diferente cifrado cada vez
3. **Minimizacion de datos:** Solo almacenar ultimos 4 digitos de tarjeta
4. **Hash de CVV:** No almacenar CVV, solo hash para verificacion
5. **JSON estructurado:** Formato claro para datos cifrados

---

## Ejercicio 2: Auditoria de una App - Identificar Exposicion de Datos Sensibles

**Escenario:** Revisar el siguiente codigo de una aplicacion web y encontrar 5 lugares donde se exponen datos sensibles.

```python
from flask import Flask, request, jsonify, send_file
import sqlite3
import logging

app = Flask(__name__)

# Configurar logging
logging.basicConfig(filename='app.log', level=logging.DEBUG)

@app.route('/api/login')
def login():
    user = request.args.get('user')
    passwd = request.args.get('pass')
    app.logger.debug(f"Login attempt: {user}:{passwd}")  # PROBLEMA 1

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username='{user}' AND password='{passwd}'"
    cursor.execute(query)
    user_data = cursor.fetchone()

    if user_data:
        # Devolver datos del usuario incluyendo password hash
        return jsonify({
            'id': user_data[0],
            'username': user_data[1],
            'password_hash': user_data[2],  # PROBLEMA 2
            'email': user_data[3],
            'credit_card': user_data[4]      # PROBLEMA 3
        })
    return jsonify({'error': 'Login failed'}), 401

@app.route('/api/user/profile')
def profile():
    user_id = request.args.get('id')
    # Sin autenticacion ni autorizacion  # PROBLEMA 4
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users WHERE id={user_id}")
    data = cursor.fetchone()

    # Servir foto de perfil
    return send_file(f'/var/app/photos/{user_id}.jpg')  # PROBLEMA 5
```

### Solucion: Identificacion y Correccion

| # | Problema | Tipo | Correccion |
|---|----------|------|------------|
| 1 | **Log de credenciales** | Exposicion en logs | No loguear contrasenas jamas |
| 2 | **Password hash en respuesta** | Exposicion de hash | No devolver hash de password en APIs |
| 3 | **Tarjeta de credito en respuesta** | Exposicion de datos financieros | Nunca devolver datos de tarjeta completos |
| 4 | **Sin autenticacion/autorizacion** | IDOR / Broken Access Control | Validar token de sesion y propiedad del recurso |
| 5 | **Path traversal en foto** | Exposicion de archivos arbitrarios | Validar path, sanitizar user_id |

### Codigo Corregido

```python
from flask import Flask, request, jsonify, send_file, session
import sqlite3
import logging
import re
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'change-me-in-production')

# Logging sin datos sensibles
logging.basicConfig(filename='app.log', level=logging.INFO)

@app.before_request
def check_authentication():
    # Rutas publicas no requieren auth
    if request.path.startswith('/api/public'):
        return
    if 'user_id' not in session:
        return jsonify({'error': 'No autenticado'}), 401

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username', '')
    password = data.get('password', '')

    # NO loguear contrasenas
    app.logger.info(f"Login attempt for user: {username}")

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # Consulta parametrizada
    cursor.execute(
        "SELECT id, username, email FROM users WHERE username = ? AND password_hash = ?",
        (username, hash_password(password))  # hash antes de comparar
    )
    user = cursor.fetchone()
    conn.close()

    if user:
        session['user_id'] = user[0]
        session['username'] = user[1]
        return jsonify({
            'id': user[0],
            'username': user[1],
            'email': user[2]
            # NO incluir password_hash ni credit_card
        })
    return jsonify({'error': 'Credenciales invalidas'}), 401

@app.route('/api/user/profile')
def profile():
    # Solo puede ver su propio perfil
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'No autenticado'}), 401

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # El usuario solo ve sus propios datos
    cursor.execute(
        "SELECT id, username, email FROM users WHERE id = ?",
        (user_id,)
    )
    data = cursor.fetchone()
    conn.close()

    if not data:
        return jsonify({'error': 'Usuario no encontrado'}), 404

    return jsonify({
        'id': data[0],
        'username': data[1],
        'email': data[2]
    })

@app.route('/api/user/photo')
def user_photo():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'No autenticado'}), 401

    # Validar que user_id es un numero (previene path traversal)
    if not isinstance(user_id, int) or user_id <= 0:
        return jsonify({'error': 'ID invalido'}), 400

    # Construir path seguro
    photo_path = f'/var/app/photos/{user_id}.jpg'

    # Verificar que el archivo existe y esta dentro del directorio permitido
    allowed_dir = os.path.abspath('/var/app/photos')
    abs_path = os.path.abspath(photo_path)

    if not abs_path.startswith(allowed_dir):
        return jsonify({'error': 'Acceso denegado'}), 403

    if not os.path.exists(abs_path):
        return jsonify({'error': 'Foto no encontrada'}), 404

    return send_file(abs_path)

def hash_password(password):
    """Placeholder - usar bcrypt/Argon2 en produccion"""
    import hashlib
    return hashlib.sha256(password.encode()).hexdigest()
```

---

## Ejercicio 3: Configurar HTTPS en Flask con Certificado Autofirmado

**Paso 1: Generar certificado autofirmado con OpenSSL**
```bash
# Generar clave privada y certificado en un solo comando
openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365 -nodes -subj "/CN=localhost"
```

**Paso 2: Aplicacion Flask con HTTPS**
```python
from flask import Flask, jsonify
import ssl

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({
        'message': 'Conexion HTTPS establecida',
        'secure': True
    })

if __name__ == '__main__':
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain('cert.pem', 'key.pem')

    # Forzar TLS 1.2+ solamente
    context.minimum_version = ssl.TLSVersion.TLSv1_2
    context.maximum_version = ssl.TLSVersion.TLSv1_3

    # Cipher suites seguras
    context.set_ciphers('ECDHE+AESGCM:ECDHE+CHACHA20:DHE+AESGCM')
    context.options |= ssl.OP_NO_TLSv1
    context.options |= ssl.OP_NO_TLSv1_1

    print("Servidor HTTPS en https://localhost:443")
    app.run(
        ssl_context=context,
        host='0.0.0.0',
        port=443,
        debug=False
    )
```

**Paso 3: Verificar la configuracion**
```bash
# Verificar certificado
openssl x509 -in cert.pem -text -noout

# Probar conexion con curl
curl -k https://localhost:443/
# -k: ignorar verificacion de certificado autofirmado

# Verificar cifrados soportados
nmap --script ssl-enum-ciphers -p 443 localhost
```

**Paso 4: Para produccion, usar Let's Encrypt (certificados gratuitos y confiables)**
```bash
# Instalar certbot
# Ejecutar para obtener certificado valido
certbot certonly --standalone -d tudominio.com

# Los certificados quedan en:
# /etc/letsencrypt/live/tudominio.com/fullchain.pem
# /etc/letsencrypt/live/tudominio.com/privkey.pem
```

---

## Preguntas y Respuestas

### Pregunta 1
**Cual es la diferencia entre cifrado en transito y cifrado en reposo? De ejemplos de cada uno.**

**Respuesta:** El cifrado en transito protege los datos mientras se mueven entre sistemas (cliente-servidor, servidor-servidor). Ejemplos: HTTPS/TLS, SSH, VPN, WPA3. El cifrado en reposo protege los datos almacenados en disco, BD, backups, archivos. Ejemplos: AES-256 para archivos, BitLocker (disco completo), cifrado de columnas en BD, S3 server-side encryption. Ambos son necesarios para una proteccion completa de datos sensibles.

### Pregunta 2
**Por que AES es preferible sobre RSA para cifrar grandes volumenes de datos?**

**Respuesta:** AES es un cifrado simetrico que opera a nivel de hardware en muchos procesadores (instrucciones AES-NI), haciendolo extremadamente rapido (varios GB/s). RSA es asimetrico y requiere operaciones matematicas complejas (exponenciacion modular con numeros grandes de 2048+ bits), siendo 100-1000 veces mas lento. RSA solo puede cifrar bloques de hasta el tamano de clave menos overhead (245 bytes para RSA 2048), mientras que AES cifra cualquier tamano. La practica estandar: usar RSA para intercambiar una clave AES, y luego AES para cifrar los datos.

### Pregunta 3
**Que es un nonce y por que es importante en AES-GCM?**

**Respuesta:** Un nonce (number used once) es un valor unico que se usa una sola vez con una clave determinada. En AES-GCM, el nonce de 12 bytes se combina con la clave para generar un keystream unico. Es importante porque: (1) si se reutiliza el mismo nonce con la misma clave, un atacante puede recuperar la clave y descifrar todos los mensajes; (2) el nonce debe ser aleatorio o un contador que nunca se repite; (3) en AES-GCM, si nonce se reutiliza, la autenticacion tambien se rompe. Por eso el codigo genera `os.urandom(12)` cada vez que cifra.

### Pregunta 4
**Que datos de tarjeta de credito NO deben almacenarse segun PCI DSS?**

**Respuesta:** Segun PCI DSS, NUNCA deben almacenarse despues de la autorizacion: (1) el codigo de verificacion de la tarjeta (CVV/CVC/CID) - ni siquiera cifrado; (2) los datos de la banda magnetica o chip (track data); (3) el PIN. Si se almacenan numero de tarjeta (PAN), deben estar cifrados con AES, truncados o tokenizados, y solo mostrar los ultimos 4 digitos. El cumplimiento PCI DSS ademas requiere: no almacenar datos de tarjeta innecesarios, mantener inventario de donde se almacenan, y documentar la necesidad de negocio para cada campo.

### Pregunta 5
**Que diferencia hay entre PII y datos personales bajo GDPR?**

**Respuesta:** PII (Personally Identifiable Information) es un termino mas antiguo de EE.UU. que se refiere a informacion que puede identificar directamente a una persona (nombre, SSN, DNI). GDPR usa el termino "datos personales" que es mas amplio: incluye PII mas cualquier informacion relacionada a una persona identificada o identificable, incluyendo datos indirectos como direccion IP, cookies, identificadores de dispositivo, datos de localizacion, preferencias politicas, sindicales, geneticos, biometricos. GDPR ademas categoriza "categorias especiales" (datos sensibles) con proteccion adicional: origen racial, opinion politica, religion, salud, vida sexual, datos geneticos y biometricos.

---

## Tarea / Lectura Recomendada

1. **Leer:** OWASP Cryptographic Storage Cheat Sheet - https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html
2. **Leer:** OWASP Transport Layer Protection Cheat Sheet - https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Protection_Cheat_Sheet.html
3. **Practicar:** Implementar un modulo de cifrado para una app Flask que proteja datos de usuarios usando AES-256-GCM
4. **Profundizar:** Leer sobre PCI DSS v4.0 - https://www.pcisecuritystandards.org/
5. **Experimentar:** Escanear la configuracion TLS de un sitio con SSL Labs (ssllabs.com/ssltest/)
6. **Leer:** Guia de GDPR para desarrolladores de la CNIL - https://www.cnil.fr/en/home



