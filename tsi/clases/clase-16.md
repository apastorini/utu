# Clase 16: OWASP Top 10 - Vision General + Inyeccion SQL

**Duracion:** 2 horas

---

## Objetivos de Aprendizaje

1. Conocer la historia y el proposito del OWASP Top 10
2. Identificar los 10 riesgos de seguridad mas criticos en aplicaciones web
3. Comprender en profundidad la inyeccion SQL y sus variantes
4. Implementar mitigaciones efectivas contra inyeccion: prepared statements, parametrizacion, ORM

---

## Contenido Detallado

### 1. Historia del OWASP Top 10

OWASP (Open Web Application Security Project) es una comunidad global sin fines de lucro dedicada a mejorar la seguridad del software. El Top 10 es su proyecto mas conocido: un documento que identifica los 10 riesgos de seguridad mas criticos en aplicaciones web.

**Evolucion:**
- 2003: Primera version
- 2004, 2007, 2010, 2013, 2017: Actualizaciones
- 2021: Version mas reciente (cambio significativo: 3 nuevos items, datos basados en 500,000+ aplicaciones)

```
OWASP Top 10: 2021 vs 2017
+----+----------------------------+----+----------------------------+
|2021| Riesgo                     |2017| Riesgo                     |
+----+----------------------------+----+----------------------------+
| A01| Broken Access Control      | A01| Broken Access Control      |
| A02| Cryptographic Failures     | A02| Cryptographic Failures    |
| A03| Injection                  | A03| Injection (baja del #1)   |
| A04| Insecure Design            | A04| Insecure Design (nuevo)    |
| A05| Security Misconfiguration  | A05| Security Misconfiguration |
| A06| Vulnerable Components      | A06| Vulnerable Components     |
| A07| Auth Failures              | A07| Auth Failures             |
| A08| Software/Data Integrity    | A08| Software/Data Integrity   |
| A09| Logging Failures           | A09| Logging Failures          |
| A10| SSRF                       | A10| SSRF (nuevo)              |
+----+----------------------------+----+----------------------------+
```

### 2. Vision General de los 10 Riesgos (OWASP Top 10 2021)

#### A01: Broken Access Control
Fallos en la autorizacion: usuarios acceden a recursos que no deberian.
- IDOR (Insecure Direct Object References): cambiar un ID en la URL
- Ej: `/api/usuario/123` - cambiar a `/api/usuario/456`

#### A02: Cryptographic Failures
Fallas en cifrado: datos sensibles no cifrados, algoritmos debiles, certificados expirados.
- Ej: Contrasenas almacenadas con MD5, HTTP en vez de HTTPS

#### A03: Injection
Inyeccion de codigo: SQL, NoSQL, OS Command, LDAP.
- **Foco de esta clase:** Inyeccion SQL

#### A04: Insecure Design
Fallas en el diseno arquitectonico del sistema.
- Ej: No tener rate limiting en login, no separar datos por tenant

#### A05: Security Misconfiguration
Configuracion insegura de servidores, BD, frameworks.
- Ej: Default credentials, directorios listables, errores detallados

#### A06: Vulnerable and Outdated Components
Uso de librerias y frameworks con vulnerabilidades conocidas.
- Ej: Log4j, Struts, versiones antiguas de jQuery

#### A07: Identification and Authentication Failures
Fallos en autenticacion: credenciales debiles, sesiones inseguras.
- Ej: Permitir contrasenas debiles, no invalidar sesion al cerrar

#### A08: Software and Data Integrity Failures
Falta de verificacion de integridad en actualizaciones, CI/CD, pipelines.
- Ej: No verificar firma de paquetes, supply chain attacks

#### A09: Security Logging and Monitoring Failures
No registrar eventos de seguridad ni detectar incidentes.
- Ej: No loguear intentos fallidos de login, no tener alertas

#### A10: Server-Side Request Forgery (SSRF)
El servidor realiza peticiones a recursos internos basado en input del usuario.
- Ej: Ataque a metadata de cloud (AWS, GCP, Azure)

### 3. Inyeccion SQL en Profundidad

#### Que es Inyeccion SQL?

Es una tecnica donde el atacante inserta codigo SQL malicioso en los parametros de entrada de una aplicacion, aprovechando que los datos ingresados se concatenan directamente en consultas SQL sin sanitizacion.

```
Entrada del usuario:  ' OR '1'='1
Consulta generada:    SELECT * FROM usuarios WHERE user = '' OR '1'='1' AND pass = 'x'
Resultado:            Devuelve todos los usuarios (bypass de autenticacion)
```

#### Tipos de Inyeccion SQL

**1. Inyeccion en el WHERE (bypass de autenticacion)**
```
SELECT * FROM usuarios WHERE username = 'admin' AND password = 'cualquiercosa' OR '1'='1'
```

**2. Inyeccion UNION (robo de datos)**
```
SELECT nombre, precio FROM productos WHERE id = 1 UNION SELECT username, password FROM usuarios
```

**3. Inyeccion a ciegas (Blind SQL)**
Sin salida visible de datos, el atacante pregunta verdadero/falso.
```
SELECT * FROM productos WHERE id = 1 AND SUBSTRING((SELECT password FROM usuarios WHERE id=1),1,1) = 'a'
```
Si la pagina carga normal, la primera letra es 'a'; si no, es otra.

**4. Time-based Blind SQL**
Similar pero usa retardos:
```
SELECT * FROM productos WHERE id = 1 AND IF(SUBSTRING((SELECT password FROM usuarios WHERE id=1),1,1)='a', SLEEP(5), 0)
```

**5. SQL Injection en INSERT/UPDATE/DELETE**
```
INSERT INTO usuarios VALUES ('admin', 'hacked')  -- Inserta usuario malicioso
UPDATE productos SET precio = 0.01 WHERE id = 1   -- Modifica precio
DELETE FROM usuarios WHERE id = 1                 -- Elimina datos
```

**6. Second-Order SQL Injection**
El payload se almacena en BD y se ejecuta en una consulta posterior.
```
Fase 1: INSERT INTO usuarios (username) VALUES ('admin'--')
Fase 2: SELECT * FROM usuarios WHERE username = 'admin'--'   (Se comenta el resto)
```

#### Consecuencias de la Inyeccion SQL

- **Bypass de autenticacion:** Acceso sin credenciales
- **Robo de datos:** Exfiltracion de BD completas
- **Modificacion de datos:** Alterar registros, precios, saldos
- **Destruccion de datos:** DROP TABLE, DELETE masivo
- **Ejecucion remota de comandos:** En algunos motores (xp_cmdshell en SQL Server)
- **Compromiso total del servidor:** Si la BD se ejecuta con altos privilegios

#### Ejemplo Vulnerable: Python con SQLite

```python
import sqlite3

def login(username, password):
    conn = sqlite3.connect('tienda.db')
    cursor = conn.cursor()
    # VULNERABLE: concatenacion directa
    query = f"SELECT * FROM usuarios WHERE username = '{username}' AND password = '{password}'"
    print(f"Ejecutando: {query}")
    cursor.execute(query)
    return cursor.fetchone() is not None

# Prueba con inyeccion
print(login("admin", "' OR '1'='1"))  # Devuelve True (bypasseado!)
```

#### Ejemplo Vulnerable: Java con JDBC

```java
String username = request.getParameter("username");
String password = request.getParameter("password");

// VULNERABLE
String query = "SELECT * FROM usuarios WHERE username = '" + username + "' AND password = '" + password + "'";
Statement stmt = connection.createStatement();
ResultSet rs = stmt.executeQuery(query);
```

### 4. Mitigaciones

#### Prepared Statements (Consultas Parametrizadas)

**Python con SQLite:**
```python
import sqlite3

def login_seguro(username, password):
    conn = sqlite3.connect('tienda.db')
    cursor = conn.cursor()
    query = "SELECT * FROM usuarios WHERE username = ? AND password = ?"
    cursor.execute(query, (username, password))
    return cursor.fetchone() is not None

# La inyeccion ya no funciona: ' OR '1'='1 se trata como literal
print(login_seguro("admin", "' OR '1'='1"))  # Busca contrasena literal, no bypassea
```

**Java con JDBC:**
```java
String query = "SELECT * FROM usuarios WHERE username = ? AND password = ?";
PreparedStatement stmt = connection.prepareStatement(query);
stmt.setString(1, username);
stmt.setString(2, password);
ResultSet rs = stmt.executeQuery();
```

**Python con MySQL (mysql-connector):**
```python
import mysql.connector
query = "SELECT * FROM usuarios WHERE username = %s AND password = %s"
cursor.execute(query, (username, password))
```

**Node.js con MySQL:**
```javascript
const query = 'SELECT * FROM usuarios WHERE username = ? AND password = ?';
connection.query(query, [username, password], (err, results) => { ... });
```

#### Uso de ORM (Object-Relational Mapping)

Los ORM (SQLAlchemy, Hibernate, Entity Framework, Prisma) generalmente usan parametrizacion internamente, pero no son invulnerables si se usan consultas raw.

```python
# SQLAlchemy (seguro)
usuario = session.query(Usuario).filter(
    Usuario.username == username,
    Usuario.password == password
).first()

 # SQLAlchemy raw (cuidado: requiere parametros explicitos)
session.execute(text("SELECT * FROM usuarios WHERE username = :user"),
                {"user": username})
```

#### Validacion de Entrada (como capa adicional)

```python
import re

def validar_username(username):
    # Solo letras, numeros y guion bajo
    return bool(re.match(r'^[a-zA-Z0-9_]{3,20}$', username))

# Sanitizacion (NO es sustituto de prepared statements)
import html
username_sanitizado = html.escape(username)  # Solo previene XSS, no inyeccion SQL
```

#### Otras Defensas

- **Stored Procedures:** Si se implementan sin SQL dinamico, tambien son seguros
- **Least Privilege en BD:** La cuenta de la app solo debe tener los permisos minimos necesarios (no DROP, no CREATE)
- **WAF (Web Application Firewall):** Reglas para detectar patrones de inyeccion
- **Escapado de caracteres:** Funciona pero es menos confiable que parametrizacion
- **Lista blanca:** Permitir solo valores conocidos (ej: IDs numericos)

---

## Ejercicio 1: Reescribir Codigo Vulnerable con Consultas Parametrizadas

**Codigo vulnerable:**
```python
import sqlite3

conn = sqlite3.connect('inventario.db')
cursor = conn.cursor()

# Crear tabla
cursor.execute('''CREATE TABLE IF NOT EXISTS productos
                  (id INTEGER PRIMARY KEY, nombre TEXT, precio REAL)''')

def buscar_producto(nombre):
    query = f"SELECT * FROM productos WHERE nombre = '{nombre}'"
    cursor.execute(query)
    return cursor.fetchall()

def agregar_producto(nombre, precio):
    query = f"INSERT INTO productos (nombre, precio) VALUES ('{nombre}', {precio})"
    cursor.execute(query)
    conn.commit()

def actualizar_precio(nombre, nuevo_precio):
    query = f"UPDATE productos SET precio = {nuevo_precio} WHERE nombre = '{nombre}'"
    cursor.execute(query)
    conn.commit()
```

**Solucion completa con parametrizacion:**
```python
import sqlite3

conn = sqlite3.connect('inventario.db')
conn.execute("PRAGMA journal_mode=WAL")  # Mejor rendimiento y seguridad en escritura
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS productos
                  (id INTEGER PRIMARY KEY, nombre TEXT, precio REAL)''')

def buscar_producto(nombre):
    query = "SELECT * FROM productos WHERE nombre = ?"
    cursor.execute(query, (nombre,))
    return cursor.fetchall()

def agregar_producto(nombre, precio):
    # Validacion adicional: precio debe ser numero
    if not isinstance(precio, (int, float)):
        raise ValueError("El precio debe ser un numero")
    if not nombre or len(nombre.strip()) == 0:
        raise ValueError("El nombre no puede estar vacio")
    query = "INSERT INTO productos (nombre, precio) VALUES (?, ?)"
    cursor.execute(query, (nombre, precio))
    conn.commit()

def actualizar_precio(nombre, nuevo_precio):
    if not isinstance(nuevo_precio, (int, float)):
        raise ValueError("El precio debe ser un numero")
    query = "UPDATE productos SET precio = ? WHERE nombre = ?"
    cursor.execute(query, (nuevo_precio, nombre))
    conn.commit()

def obtener_productos_seguros():
    """Devuelve productos con campos sanitizados para mostrar"""
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    return productos

# Pruebas
if __name__ == "__main__":
    # Insertar datos de prueba
    agregar_producto("Laptop", 999.99)
    agregar_producto("Mouse", 29.99)

    # Busqueda segura (intento de inyeccion tratado como literal)
    resultados = buscar_producto("' OR '1'='1")  # No devuelve resultados
    print(f"Busqueda inyectada: {resultados}")   # [] - vacio

    resultado_normal = buscar_producto("Laptop")
    print(f"Busqueda normal: {resultado_normal}")  # [(1, 'Laptop', 999.99)]

    print("Sistema seguro contra inyeccion SQL!")
```

**Explicacion de la solucion:**
1. Se reemplazo la concatenacion `f"...{variable}"` por `?` placeholders
2. Los valores se pasan como tupla separada: `cursor.execute(query, (valor1, valor2))`
3. La BD trata los valores como datos literales, no como parte del SQL
4. Se agregaron validaciones de tipo y contenido como capa adicional
5. Se elimino la posibilidad de que un payload malicioso modifique la consulta

---

## Ejercicio 2: Identificar y Corregir 3 Tipos de Inyeccion

**Fragmento vulnerable:**
```python
import os
import subprocess

# Contexto: herramienta de administracion de servidores

def get_user_info(user_id):
    # CONSULTA 1
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE id = {user_id}"
    cursor.execute(query)
    return cursor.fetchone()

def ping_host(host):
    # CONSULTA 2 (OS Command Injection)
    result = subprocess.run(f"ping -n 3 {host}", shell=True, capture_output=True)
    return result.stdout

def find_user_ldap(search_term):
    # CONSULTA 3 (LDAP Injection)
    import ldap
    conn = ldap.initialize('ldap://ldap.company.com')
    base_dn = 'ou=users,dc=company,dc=com'
    filter_str = f'(uid={search_term})'
    result = conn.search_s(base_dn, ldap.SCOPE_SUBTREE, filter_str)
    return result
```

### Identificacion de Vulnerabilidades

| Consulta | Tipo de Inyeccion | Explicacion |
|----------|-------------------|-------------|
| Consulta 1 | **SQL Injection** | `user_id` se concatena directamente. Atacante puede enviar `1 UNION SELECT username, password FROM admins` |
| Consulta 2 | **OS Command Injection** | `host` se pasa a shell. Atacante puede enviar `google.com & del /F /Q C:\Windows\System32\*` |
| Consulta 3 | **LDAP Injection** | `search_term` se concatena en filtro LDAP. Atacante puede enviar `*)(uid=*))(|(uid=*` para listar todos los usuarios |

### Solucion Completa

```python
import os
import subprocess
import sqlite3
import ldap
import re

# CONFIGURACION
DB_PATH = 'users.db'

def get_user_info(user_id):
    """CORREGIDO: SQL Injection mitigado con parametrizacion"""
    if not isinstance(user_id, int):
        try:
            user_id = int(user_id)
        except (ValueError, TypeError):
            return None

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE id = ?"
    cursor.execute(query, (user_id,))
    return cursor.fetchone()

def ping_host(hostname):
    """CORREGIDO: Command Injection mitigado sin shell=True"""
    # Validar que solo contiene caracteres permitidos para un hostname
    if not re.match(r'^[a-zA-Z0-9\.\-]+$', hostname):
        return b"Error: hostname invalido"

    # Usar lista de argumentos en vez de string con shell=True
    result = subprocess.run(
        ["ping", "-n", "3", hostname],
        capture_output=True,
        timeout=10
    )
    return result.stdout

def find_user_ldap(search_term):
    """CORREGIDO: LDAP Injection mitigado con escapado"""
    # Escapar caracteres especiales LDAP
    def escape_ldap(s):
        # LDAP special characters: * ( ) \ NUL
        chars_to_escape = ['\\', '*', '(', ')', '\x00']
        for c in chars_to_escape:
            s = s.replace(c, '\\' + c)
        return s

    conn = ldap.initialize('ldap://ldap.company.com')
    base_dn = 'ou=users,dc=company,dc=com'

    # Escapar el termino de busqueda
    safe_term = escape_ldap(search_term)
    filter_str = f'(uid={safe_term})'

    # Alternativa mas segura: filtro de lista blanca
    # Solo buscar por atributos especificos con validacion
    if not re.match(r'^[a-zA-Z0-9_\-\s]+$', search_term):
        return "Error: caracteres no permitidos en la busqueda"

    result = conn.search_s(base_dn, ldap.SCOPE_SUBTREE, filter_str)
    return result
```

---

## Preguntas y Respuestas

### Pregunta 1
**Por que usar prepared statements es la mejor defensa contra inyeccion SQL? Que hace internamente?**

**Respuesta:** Los prepared statements separan la estructura SQL de los datos. Internamente, el motor de BD compila la consulta con los placeholders (`?`) primero (definiendo la estructura fija), y luego los parametros se pasan como datos literales. Esto significa que aunque el parametro contenga comillas o palabras SQL, se tratara como un valor literal, no como parte del comando SQL. Es la mejor defensa porque aborda la causa raiz: la mezcla de codigo con datos.

### Pregunta 2
**Es suficiente con validar las entradas del usuario para prevenir inyeccion SQL?**

**Respuesta:** No. La validacion de entrada es una capa de defensa util, pero no debe ser la unica. Los atacantes encuentran formas de evadir filtros (encoding, bypass de regex, caracteres Unicode). Ademas, la validacion protege contra ataques conocidos pero no necesariamente contra variantes nuevas. La defensa principal debe ser prepared statements/parametrizacion, con la validacion de entrada como capa adicional (defense in depth).

### Pregunta 3
**Que es un ataque de "Second-Order SQL Injection" y por que es mas dificil de detectar?**

**Respuesta:** En el second-order SQL injection, el payload malicioso se almacena en la BD en una primera operacion (ej: registro de usuario con nombre que contiene codigo SQL) y se ejecuta en una consulta posterior (ej: al buscar usuarios por nombre). Es mas dificil de detectar porque: (1) las herramientas de escaneo solo ven la consulta actual, no la historia de los datos; (2) el desarrollador asume que los datos de la BD son "seguros" (cuando deberia tratarlos como no confiables igual que los inputs); (3) las mitigaciones en el punto de entrada no protegen si la segunda consulta tambien es vulnerable.

### Pregunta 4
**Los ORM (como SQLAlchemy o Hibernate) protegen automaticamente contra inyeccion SQL?**

**Respuesta:** Generalmente si, cuando se usan correctamente. Los ORM generan consultas parametrizadas internamente. Sin embargo, la proteccion se pierde si se usan funciones "raw" del ORM (ej: `execute()` con concatenacion de strings), o si se usan caracteristicas como `text()` en SQLAlchemy sin parametros. El desarrollador debe evitar las opciones que permiten SQL sin parametrizar y siempre pasar valores como parametros separados.

### Pregunta 5
**Cual es la diferencia entre inyeccion SQL y NoSQL? Mencione una similitud.**

**Respuesta:** La diferencia principal es el lenguaje: la inyeccion SQL ataca bases relacionales con SQL; la inyeccion NoSQL ataca bases documentales (MongoDB, CouchDB) usando su sintaxis de consulta ($where, $ne, $regex). La similitud: ambas ocurren cuando los datos del usuario se concatenan directamente en la construccion de la consulta sin sanitizacion ni parametrizacion. La mitigacion es conceptualmente la misma: usar el API parametrizada que provee el driver de la BD.

---

## Tarea / Lectura Recomendada

1. **Leer:** OWASP Top 10 2021 - https://owasp.org/Top10/
2. **Leer:** OWASP SQL Injection Prevention Cheat Sheet - https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html
3. **Practicar:** PortSwigger Web Security Academy - SQL Injection Labs (gratuito) - https://portswigger.net/web-security/sql-injection
4. **Profundizar:** Leer sobre inyeccion en diferentes motores de BD (MySQL, PostgreSQL, SQL Server, Oracle)
5. **Herramienta:** Probar OWASP ZAP para escanear una app de prueba en busca de inyeccion SQL



