# Clase 38: Secure Code Review - Taller Practico

**Numero de clase:** 27  
**Duracion:** 2 horas  
**Curso:** Taller de Ciberseguridad Orientada al Desarrollo

---

## Objetivos de Aprendizaje

- Comprender el proceso de secure code review y su importancia
- Identificar patrones peligrosos en codigo fuente (Python, JavaScript, Java)
- Aplicar la metodologia OWASP Code Review Guide
- Distinguir entre vulnerabilidades automatizables y las que requieren revision manual
- Corregir vulnerabilidades de seguridad en fragmentos de codigo reales

---

## Contenido Detallado

### 1. Que es un Secure Code Review? (15 min)

El **secure code review** es la revision sistematica del codigo fuente para identificar vulnerabilidades de seguridad antes de que el software llegue a produccion. No es lo mismo que un code review funcional: se enfoca exclusivamente en aspectos de seguridad.

**Objetivos:**
- Identificar vulnerabilidades antes del deploy
- Educar al equipo de desarrollo
- Establecer una linea base de seguridad
- Reducir el costo de corregir errores (es mas barato corregir en desarrollo que en produccion)

**Costo relativo de corregir vulnerabilidades:**
- En desarrollo: 1x
- En pruebas: 10x
- En produccion: 100x
- Despues de un incidente: 1000x

### 2. Checklist de Revision - OWASP Code Review Guide (15 min)

La metodologia OWASP se organiza en categorias:

| Categoria | Que revisar |
|-----------|-------------|
| Validacion de entrada | SQL injection, XSS, command injection, path traversal |
| Autenticacion | Contrasenas en texto plano, JWT debiles, session fixation |
| Autorizacion | IDOR, privilege escalation, missing access controls |
| Criptografia | Algoritmos debiles (MD5, SHA1), claves hardcodeadas, mal manejo de TLS |
| Manejo de errores | Stack traces expuestos, informacion sensible en errores |
| Logging | Informacion sensible en logs (PII, contrasenas) |
| Configuracion | Secretos en codigo, CORS mal configurado, debug habilitado |
| Dependencias | Librerias con vulnerabilidades conocidas |

### 3. Automatizacion vs. Revision Manual (10 min)

**Automatizable (herramientas SAST):**
- SQL injection basico
- XSS reflejado
- Uso de funciones peligrosas (eval, exec)
- Hardcoded secrets
- Algoritmos criptograficos debiles

**Requiere revision manual:**
- Logica de negocio flaws (ej: un usuario puede editar recursos de otro)
- IDOR (Insecure Direct Object References)
- Problemas de autenticacion complejos
- Race conditions
- Vulnerabilidades en flujos de multiple paso

### 4. Patrones Peligrosos a Buscar (10 min)

| Patron | Lenguaje | Riesgo |
|--------|----------|--------|
| `eval()`, `exec()` | Python | Code injection |
| `innerHTML`, `dangerouslySetInnerHTML` | JS/React | XSS |
| `os.system()`, `subprocess.Popen(shell=True)` | Python | Command injection |
| `pickle.loads()` | Python | Deserializacion insegura |
| `JSON.parse()` sin validacion | JS | Prototype pollution |
| `DES`, `MD5`, `SHA1` | Todos | Criptografia debil |
| `"SELECT * FROM users WHERE id = " + id` | Todos | SQL injection |
| `process.env.SECRET_KEY` expuesto | Node | Hardcoded secrets |

### 5. Metodologia (10 min)

```
Entrada -> Procesamiento -> Almacenamiento -> Salida
```

Para cada fragmento de codigo, seguir:
1. **Entrada:** De donde vienen los datos? (request, archivo, red)
2. **Procesamiento:** Que se hace con los datos? (validacion, transformacion)
3. **Almacenamiento:** Donde se guardan? (base de datos, archivos, cache)
4. **Salida:** Como se devuelven? (HTML, JSON, XML, archivos)

---

## Ejercicio 1: Fragmento Python Flask - Login con Vulnerabilidades

**Codigo vulnerable:**

```python
from flask import Flask, request, render_template_string, session, redirect
import sqlite3

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # VULNERABILIDAD 1: SQL Injection
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    cursor.execute(query)
    user = cursor.fetchone()
    conn.close()

    if user:
        session['user'] = username
        # VULNERABILIDAD 2: XSS (reflejado en template)
        return render_template_string(f"<h1>Bienvenido {username}</h1>")
    else:
        return "Credenciales invalidas", 401

if __name__ == '__main__':
    app.run(debug=True)  # VULNERABILIDAD 3: Debug mode habilitado
```

**Vulnerabilidades identificadas:**

1. **SQL Injection (Critico):** La concatenacion directa de `username` y `password` en la query SQL permite inyeccion. Un atacante puede enviar `' OR '1'='1` como username para eludir la autenticacion.

2. **XSS Reflejado (Alto):** `render_template_string` con interpolacion directa de `username` permite ejecutar HTML/JavaScript arbitrario. Si un atacante envia `<script>alert('xss')</script>`, se ejecuta en el navegador.

3. **Debug Mode en Produccion (Alto):** `app.run(debug=True)` expone el debugger de Werkzeug y permite ejecutar codigo Python arbitrario si se accede a `/console`.

**Codigo corregido:**

```python
from flask import Flask, request, render_template, session, redirect, abort
import sqlite3
import bcrypt
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', os.urandom(32))
app.config['DEBUG'] = False  # Debug explcitamente deshabilitado

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '')

    if not username or not password:
        abort(400, "Usuario y contrasena requeridos")

    # CORRECCION 1: Consultas parametrizadas
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    query = "SELECT password_hash FROM users WHERE username = ?"
    cursor.execute(query, (username,))
    result = cursor.fetchone()
    conn.close()

    if result is None:
        # Usuario no existe (no revelar si existe o no)
        return "Credenciales invalidas", 401

    password_hash = result[0]

    # CORRECCION 2: Verificar contrasena con bcrypt
    if not bcrypt.checkpw(password.encode('utf-8'), password_hash):
        return "Credenciales invalidas", 401

    session['user'] = username
    # CORRECCION 3: Usar template separado (escapado automatico)
    return render_template('dashboard.html', username=username)

# CORRECCION 4: CSRF protection basica
@app.before_request
def csrf_check():
    if request.method == 'POST':
        token = request.form.get('csrf_token')
        if not token or token != session.get('csrf_token'):
            abort(400, "CSRF token invalido")

if __name__ == '__main__':
    app.run(debug=False)
```

---

## Ejercicio 2: Fragmento Node.js Express - IDOR, Deserializacion, Secretos

**Codigo vulnerable:**

```javascript
const express = require('express');
const app = express();

// VULNERABILIDAD 1: Secretos hardcodeados
const SECRET_KEY = 'my-super-secret-key-12345';
const DB_PASSWORD = 'admin123';

app.use(express.json());

// VULNERABILIDAD 2: Deserializacion insegura
app.post('/api/process', (req, res) => {
  const data = req.body.data;
  // Peligro: permite ejecucion de codigo arbitrario
  const processed = eval('(' + data + ')');
  res.json({ result: processed });
});

// VULNERABILIDAD 3: IDOR - Insecure Direct Object Reference
app.get('/api/users/:id', (req, res) => {
  const userId = req.params.id;
  // No verifica que el usuario autenticado sea el propietario
  const user = db.users.find(u => u.id === userId);
  res.json(user);
});

app.listen(3000);
```

**Vulnerabilidades identificadas:**

1. **Secretos hardcodeados (Critico):** La clave secreta y contrasena de BD estan en el codigo fuente. Cualquiera con acceso al repositorio las obtiene.

2. **Deserializacion insegura con eval (Critico):** `eval()` ejecuta cualquier codigo JavaScript. Un atacante puede enviar `require('child_process').execSync('rm -rf /')` y ejecutar comandos en el servidor.

3. **IDOR (Alto):** El endpoint `/api/users/:id` permite acceder a la informacion de cualquier usuario sin verificar propiedad o permisos. Un atacante puede cambiar el `:id` para acceder a datos de otros usuarios.

**Codigo corregido:**

```javascript
const express = require('express');
const jwt = require('jsonwebtoken');
const helmet = require('helmet');

const app = express();
app.use(helmet()); // Seguridad de headers

// CORRECCION 1: Secretos desde variables de entorno
const SECRET_KEY = process.env.JWT_SECRET;
if (!SECRET_KEY) {
  throw new Error('JWT_SECRET no configurado en variables de entorno');
}

app.use(express.json({ limit: '10kb' })); // Limite de tamano

// CORRECCION 2: Validacion segura en vez de eval
app.post('/api/process', (req, res) => {
  const data = req.body.data;

  // Validar que sea un JSON valido
  if (typeof data !== 'string') {
    return res.status(400).json({ error: 'data debe ser un string JSON' });
  }

  try {
    // Usar JSON.parse en vez de eval (mucho mas seguro)
    const parsed = JSON.parse(data);

    // Validar estructura esperada
    if (!parsed || typeof parsed !== 'object') {
      return res.status(400).json({ error: 'Formato invalido' });
    }

    // Procesar solo campos permitidos
    const allowed = ['name', 'email', 'age'];
    const processed = {};
    for (const key of allowed) {
      if (parsed[key] !== undefined) {
        processed[key] = parsed[key];
      }
    }

    res.json({ result: processed });
  } catch (e) {
    res.status(400).json({ error: 'JSON invalido' });
  }
});

// CORRECCION 3: Autenticacion y autorizacion con JWT
function authenticateToken(req, res, next) {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1];

  if (!token) {
    return res.status(401).json({ error: 'Token requerido' });
  }

  jwt.verify(token, SECRET_KEY, (err, user) => {
    if (err) {
      return res.status(403).json({ error: 'Token invalido' });
    }
    req.user = user;
    next();
  });
}

// CORRECCION 4: IDOR - verificar que el usuario sea el propietario
app.get('/api/users/:id', authenticateToken, (req, res) => {
  const userId = parseInt(req.params.id, 10);

  // Verificar que sea el mismo usuario o admin
  if (req.user.id !== userId && req.user.role !== 'admin') {
    return res.status(403).json({ error: 'No autorizado para ver este usuario' });
  }

  const user = db.users.find(u => u.id === userId);
  if (!user) {
    return res.status(404).json({ error: 'Usuario no encontrado' });
  }

  // No exponer campos sensibles
  const { password_hash, ...safeUser } = user;
  res.json(safeUser);
});

app.listen(3000);
```

---

## Ejercicio 3: Fragmento Java Spring - XXE, Path Traversal, Falta de Autorizacion

**Codigo vulnerable:**

```java
import org.springframework.web.bind.annotation.*;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;

@RestController
public class VulnerableController {

    // VULNERABILIDAD 1: XXE - XML External Entity
    @PostMapping("/api/xml/parse")
    public String parseXml(@RequestBody String xmlData) {
        DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
        DocumentBuilder builder = factory.newDocumentBuilder();
        Document doc = builder.parse(new InputSource(new StringReader(xmlData)));
        // Procesa el XML permitiendo entidades externas
        return doc.getDocumentElement().getTextContent();
    }

    // VULNERABILIDAD 2: Path Traversal
    @GetMapping("/api/files/read")
    public String readFile(@RequestParam String filename) {
        // No valida ni sanitiza el nombre del archivo
        Path filePath = Path.of("/app/data/" + filename);
        return Files.readString(filePath);
    }

    // VULNERABILIDAD 3: Falta de autorizacion
    @DeleteMapping("/api/admin/users/{userId}")
    public String deleteUser(@PathVariable Long userId) {
        // No verifica si el usuario autenticado es admin
        userRepository.deleteById(userId);
        return "Usuario eliminado";
    }
}
```

**Vulnerabilidades identificadas:**

1. **XXE (XML External Entity) - Critico:** El parser XML por defecto en Java procesa entidades externas. Un atacante puede enviar un XML que lea archivos del servidor o haga SSRF (Server-Side Request Forgery).

2. **Path Traversal - Alto:** El parametro `filename` se concatenan directamente a la ruta. Un atacante puede usar `../../etc/passwd` para leer archivos fuera del directorio permitido.

3. **Falta de autorizacion - Critico:** El endpoint `DELETE /api/admin/users/{userId}` no verifica que el usuario que realiza la peticion tenga rol de administrador. Cualquier usuario autenticado (o no autenticado) puede eliminar usuarios.

**Codigo corregido:**

```java
import org.springframework.web.bind.annotation.*;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.security.core.Authentication;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.XMLConstants;
import java.nio.file.Path;
import java.nio.file.Paths;

@RestController
public class SecureController {

    // CORRECCION 1: XXE deshabilitado
    @PostMapping("/api/xml/parse")
    public String parseXml(@RequestBody String xmlData) throws Exception {
        DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();

        // Deshabilitar DOCTYPE para prevenir XXE
        factory.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
        // Deshabilitar entidades externas
        factory.setFeature("http://xml.org/sax/features/external-general-entities", false);
        factory.setFeature("http://xml.org/sax/features/external-parameter-entities", false);
        // Deshabilitar DTDA (Document Type Definition)
        factory.setFeature("http://apache.org/xml/features/nonvalidating/load-external-dtd", false);
        // Deshabilitar XInclude
        factory.setXIncludeAware(false);
        factory.setExpandEntityReferences(false);

        DocumentBuilder builder = factory.newDocumentBuilder();
        Document doc = builder.parse(new InputSource(new StringReader(xmlData)));
        return doc.getDocumentElement().getTextContent();
    }

    // CORRECCION 2: Path traversal prevenido
    @GetMapping("/api/files/read")
    public String readFile(@RequestParam String filename,
                          Authentication auth) throws Exception {

        // Obtener el usuario autenticado
        String username = auth.getName();

        // Sanitizar: permitir solo alfanumerico, punto y guion
        if (!filename.matches("^[a-zA-Z0-9._-]+$")) {
            throw new SecurityException("Nombre de archivo invalido");
        }

        // Resolver ruta canonica y verificar que este dentro del directorio base
        Path baseDir = Paths.get("/app/data").toAbsolutePath().normalize();
        Path filePath = baseDir.resolve(filename).normalize();

        if (!filePath.startsWith(baseDir)) {
            throw new SecurityException("Acceso denegado: fuera del directorio permitido");
        }

        if (!Files.exists(filePath) || Files.isDirectory(filePath)) {
            throw new FileNotFoundException("Archivo no encontrado");
        }

        return Files.readString(filePath);
    }

    // CORRECCION 3: Autorizacion con Spring Security
    @PreAuthorize("hasRole('ADMIN')")
    @DeleteMapping("/api/admin/users/{userId}")
    public String deleteUser(@PathVariable Long userId, Authentication auth) {
        // Solo usuarios con rol ADMIN pueden acceder
        // Spring Security verifica el rol antes de ejecutar el metodo

        // Log de auditoria
        log.info("Usuario {} elimino el usuario {}", auth.getName(), userId);
        userRepository.deleteById(userId);
        return "Usuario eliminado";
    }
}
```

---

## Preguntas y Respuestas

**1. Cual es la diferencia entre un code review funcional y un secure code review?**

El code review funcional verifica que el codigo cumpla con los requisitos de negocio, sea legible y siga las convenciones del equipo. El secure code review se enfoca exclusivamente en vulnerabilidades de seguridad: validacion de entrada, autenticacion, autorizacion, criptografia, manejo seguro de errores, etc.

**2. Que es un IDOR y como se previene?**

IDOR (Insecure Direct Object Reference) ocurre cuando un endpoint expone una referencia directa a un objeto interno (ID de base de datos, nombre de archivo) y no verifica que el usuario tenga permiso para acceder a ese objeto. Se previene con autorizacion: verificar que el usuario autenticado sea propietario o tenga rol adecuado.

**3. Que es una vulnerabilidad XXE y cuando ocurre en Java?**

XXE (XML External Entity) ocurre cuando un parser XML procesa entidades externas definidas en un DOCTYPE. En Java, el parser por defecto (`DocumentBuilderFactory.newInstance()`) tiene las entidades externas habilitadas. Un atacante puede leer archivos del servidor o hacer SSRF. Se previene deshabilitando DOCTYPE y entidades externas.

**4. Por que es peligroso usar `eval()` en JavaScript o Node.js?**

`eval()` ejecuta cualquier string como codigo JavaScript. Esto permite inyeccion de codigo arbitrario. Si un atacante controla parte del string pasado a `eval()`, puede ejecutar comandos del sistema, leer archivos, robar datos, o tomar control del servidor.

**5. Que es path traversal y como se previene en Java?**

Path traversal permite a un atacante leer archivos fuera del directorio permitido usando `../` en la ruta. Se previene: (1) sanitizando el input para eliminar `../`, (2) normalizando la ruta con `toRealPath()` o `normalize()`, (3) verificando que la ruta resultante comience con el directorio base permitido.

**6. Cuales son los 3 tipos de vulnerabilidades mas comunes en aplicaciones web segun OWASP Top 10?**

Broken Access Control (fallas en control de acceso), Cryptographic Failures (fallas criptograficas), e Injection (inyeccion SQL, command, etc.). Estas tres cubren la mayoria de vulnerabilidades encontradas en aplicaciones web.

**7. Que herramientas SAST pueden automatizar parte del secure code review?**

SonarQube, Semgrep, CodeQL (GitHub), Bandit (Python), ESLint con plugins de seguridad (JS/TS), FindSecBugs (Java), FlawFinder (C/C++), Brakeman (Ruby on Rails). Ninguna reemplaza la revision manual, pero automatizan la deteccion de patrones conocidos.

---

## Tarea / Lectura Recomendada

- Leer: OWASP Code Review Guide (https://owasp.org/www-project-code-review-guide/)
- Leer: OWASP Top 10 - 2021 (https://owasp.org/www-project-top-ten/)
- Practicar: Ejecutar Bandit y Semgrep sobre los fragmentos vulnerables de la clase
- Instalar: Una herramienta SAST de tu eleccion y analizar un proyecto propio
- Investigar: Que es un CVE y como se reporta



