# Clase 21: Control de Acceso Roto

**Duracion:** 2 horas

---

## Objetivos de Aprendizaje

1. Diferenciar claramente entre autenticacion y autorizacion
2. Identificar y explotar vulnerabilidades IDOR (Insecure Direct Object Reference)
3. Comprender Path Traversal y como prevenirlo
4. Implementar RBAC (Role-Based Access Control) correctamente
5. Aplicar el principio de minimo privilegio

---

## Contenido Detallado

### 1. Autenticacion vs. Autorizacion

| Concepto | Definicion | Ejemplo |
|----------|-----------|---------|
| **Autenticacion** | Verificar la identidad del usuario (quien eres) | Login con usuario/contrasena, biometria, 2FA |
| **Autorizacion** | Verificar que el usuario tiene permiso para hacer algo (que puedes hacer) | El usuario admin puede borrar, el viewer solo puede leer |

**Frase clave:** La autenticacion falla cuando alguien que no es quien dice ser accede; la autorizacion falla cuando alguien legitimo accede a lo que no deberia.

### 2. IDOR (Insecure Direct Object Reference)

IDOR ocurre cuando una aplicacion expone referencias directas a objetos internos (IDs, nombres de archivo, claves) y no verifica que el usuario tenga permiso para acceder a ese objeto.

**Ejemplo clasico:**

```python
# VULNERABLE: Sin verificacion de pertenencia
@app.route('/api/factura/<int:factura_id>')
def ver_factura(factura_id):
    factura = database.get_factura(factura_id)
    return jsonify(factura)
    # Cualquier usuario autenticado puede cambiar factura_id y ver facturas ajenas
```

**Ataque:** El atacante cambia `?id=123` a `?id=124` y accede a datos de otro usuario.

### 3. Elevacion de Privilegios

Ocurre cuando un usuario obtiene permisos que no le corresponden.

**Vertical:** Usuario normal obtiene privilegios de admin (ej: modificar rol en la request).

**Horizontal:** Usuario normal accede a datos de otro usuario del mismo nivel.

**Ejemplo de elevacion vertical:**

```python
# VULNERABLE: El rol viene del cliente
@app.route('/api/admin/delete', methods=['POST'])
def delete_user():
    user_role = request.json.get('role')  # El cliente envia 'admin'
    if user_role == 'admin':
        # Ejecutar accion administrativa
        pass
```

### 4. Path Traversal

Path traversal permite al atacante leer archivos fuera del directorio permitido usando `../`.

**Ejemplo vulnerable:**

```python
@app.route('/api/files/<filename>')
def get_file(filename):
    # VULNERABLE: El atacante puede pasar ../../etc/passwd
    with open(f'/var/app/files/{filename}', 'r') as f:
        return f.read()
```

**Ataque:** `GET /api/files/../../../windows/system32/config/sam`

### 5. RBAC (Role-Based Access Control)

RBAC asigna permisos basados en roles. Una implementacion incorrecta es la causa #1 de broken access control.

**Estructura basica de RBAC:**

```
USUARIOS → ROLES → PERMISOS
                ↓
           Acciones permitidas
```

**Modelo de datos:**

```python
# Definicion de roles y permisos
ROLES = {
    'admin': ['crear', 'leer', 'actualizar', 'eliminar', 'gestionar_usuarios'],
    'user': ['crear', 'leer', 'actualizar'],  # Solo sus propios recursos
    'viewer': ['leer'],  # Solo lectura
}
```

### 6. Principio de Minimo Privilegio

Cada usuario/proceso debe tener exactamente los permisos necesarios para realizar su funcion, ni mas ni menos.

**Aplicacion practica:**
- Un viewer no necesita permiso de eliminacion
- Un trabajo batch que solo lee no necesita permisos de escritura
- Un proceso que sirve archivos no necesita ejecutar comandos del sistema
- Los contenedores deben correr como non-root

### 7. OWASP Top 10 - Broken Access Control

Desde 2021, Broken Access Control es la categoria #1 del OWASP Top 10.

**Estadisticas:**
- 94% de las aplicaciones probadas tienen algun tipo de broken access control
- La tasa de incidencia promedio es 3.81%
- Mas de 318,000 ocurrencias de CVEs relacionados

---

## Ejercicio 1: Explotar y Corregir IDOR en Flask

### Escenario

Una aplicacion de notas permite a los usuarios ver sus notas por ID. El sistema tiene IDOR porque no verifica que la nota pertenezca al usuario.

**Paso 1: Aplicacion vulnerable**

```python
"""
app_idor.py - Aplicacion con IDOR
"""
from flask import Flask, jsonify, request, session
import uuid

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Base de datos simulada
notas_db = {}
usuarios_db = {
    'alice': {'password': 'pass123', 'id': 1},
    'bob': {'password': 'pass456', 'id': 2},
}

# Crear notas de ejemplo
notas_db[1] = [
    {'id': 101, 'titulo': 'Nota secreta de Alice', 'contenido': 'Mi contrasena es alice123'},
    {'id': 102, 'titulo': 'Lista de compras', 'contenido': 'Leche, pan, huevos'},
]
notas_db[2] = [
    {'id': 201, 'titulo': 'Nota de Bob', 'contenido': 'Deberia 1000USD a alguien'},
    {'id': 202, 'titulo': 'Ideas de proyecto', 'contenido': 'App de ciberseguridad'},
]

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username in usuarios_db and usuarios_db[username]['password'] == password:
        session['user_id'] = usuarios_db[username]['id']
        session['username'] = username
        return jsonify({'mensaje': 'Login exitoso', 'usuario': username})
    return jsonify({'error': 'Credenciales invalidas'}), 401

@app.route('/api/notas', methods=['GET'])
def listar_notas():
    if 'user_id' not in session:
        return jsonify({'error': 'No autenticado'}), 401
    user_id = session['user_id']
    notas = notas_db.get(user_id, [])
    return jsonify(notas)

@app.route('/api/notas/<int:nota_id>')
def ver_nota(nota_id):
    if 'user_id' not in session:
        return jsonify({'error': 'No autenticado'}), 401

    # VULNERABLE: Busca la nota por ID sin verificar pertenencia
    for uid, notas in notas_db.items():
        for nota in notas:
            if nota['id'] == nota_id:
                return jsonify(nota)

    return jsonify({'error': 'Nota no encontrada'}), 404

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)
```

**Paso 2: Script de explotacion**

```python
"""
exploit_idor.py - Explotacion de IDOR
"""
import requests

BASE = "http://127.0.0.1:5000"

# 1. Login como Alice
session = requests.Session()
login_data = {'username': 'alice', 'password': 'pass123'}
r = session.post(f"{BASE}/login", json=login_data)
print(f"Login como Alice: {r.json()}")

# 2. Listar notas de Alice (deberia ver solo las suyas)
r = session.get(f"{BASE}/api/notas")
print(f"Notas de Alice: {r.json()}")

# 3. IDOR: Intentar ver nota de Bob (ID 201)
r = session.get(f"{BASE}/api/notas/201")
print(f"IDOR - Nota de Bob vista por Alice: {r.json()}")
```

**Paso 3: Version corregida (verificando pertenencia)**

```python
"""
app_idor_segura.py - Version corregida con control de acceso
"""
from flask import Flask, jsonify, request, session
import uuid

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Base de datos simulada - cada nota registra su dueno
notas_db = {}
usuarios_db = {
    'alice': {'password': 'pass123', 'id': 1},
    'bob': {'password': 'pass456', 'id': 2},
}

# Las notas ahora incluyen user_id
notas_db[1] = [
    {'id': 101, 'user_id': 1, 'titulo': 'Nota secreta de Alice', 'contenido': 'Mi contrasena es alice123'},
    {'id': 102, 'user_id': 1, 'titulo': 'Lista de compras', 'contenido': 'Leche, pan, huevos'},
]
notas_db[2] = [
    {'id': 201, 'user_id': 2, 'titulo': 'Nota de Bob', 'contenido': 'Deberia 1000USD a alguien'},
    {'id': 202, 'user_id': 2, 'titulo': 'Ideas de proyecto', 'contenido': 'App de ciberseguridad'},
]

def login_required(f):
    """Decorador para verificar autenticacion"""
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'No autenticado'}), 401
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username in usuarios_db and usuarios_db[username]['password'] == password:
        session['user_id'] = usuarios_db[username]['id']
        session['username'] = username
        return jsonify({'mensaje': 'Login exitoso', 'usuario': username})
    return jsonify({'error': 'Credenciales invalidas'}), 401

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'mensaje': 'Sesion cerrada'})

@app.route('/api/notas', methods=['GET'])
@login_required
def listar_notas():
    user_id = session['user_id']
    notas = notas_db.get(user_id, [])
    return jsonify(notas)

@app.route('/api/notas/<int:nota_id>', methods=['GET'])
@login_required
def ver_nota(nota_id):
    user_id = session['user_id']

    # CORREGIDO: Verificar que la nota pertenece al usuario
    notas = notas_db.get(user_id, [])
    for nota in notas:
        if nota['id'] == nota_id:
            return jsonify(nota)

    return jsonify({'error': 'Nota no encontrada o acceso denegado'}), 404

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)
```

**Paso 4: Verificar la correccion**

```python
"""
test_idor_seguro.py - Verificar que la correccion funciona
"""
import requests

BASE = "http://127.0.0.1:5000"

session = requests.Session()

# Login como Alice
session.post(f"{BASE}/login", json={'username': 'alice', 'password': 'pass123'})

# Intentar ver nota de Bob
r = session.get(f"{BASE}/api/notas/201")
print(f"Intento de IDOR bloqueado: {r.json()}")
# Debe devolver: {'error': 'Nota no encontrada o acceso denegado'} con 404

# Ver nota propia
r = session.get(f"{BASE}/api/notas/101")
print(f"Nota propia accesible: {r.json()}")
```

---

## Ejercicio 2: Implementar RBAC en una API REST con 3 Roles

### Escenario

Implementar un sistema RBAC completo con 3 roles (admin, user, viewer) para una API REST de gestion de documentos.

```python
"""
rbac_api.py - API REST con RBAC completo
"""
from flask import Flask, jsonify, request, session, abort
from functools import wraps
import os

app = Flask(__name__)
app.secret_key = os.urandom(32).hex()

# ============================================================
# CONFIGURACION RBAC
# ============================================================

# Definicion de permisos
PERMISOS = {
    'admin': [
        'documentos:crear', 'documentos:leer', 'documentos:actualizar',
        'documentos:eliminar', 'documentos:listar', 'usuarios:gestionar',
        'reportes:generar', 'configuracion:editar'
    ],
    'user': [
        'documentos:crear', 'documentos:leer', 'documentos:actualizar',
        'documentos:listar'
        # Sin eliminar, sin gestion de usuarios
    ],
    'viewer': [
        'documentos:leer', 'documentos:listar'
        # Solo lectura
    ],
}

# Base de datos de usuarios
USUARIOS = {
    1: {'username': 'admin', 'password': 'admin123', 'role': 'admin'},
    2: {'username': 'juan', 'password': 'user123', 'role': 'user'},
    3: {'username': 'invitado', 'password': 'view123', 'role': 'viewer'},
}

# Base de datos de documentos (simulada)
DOCUMENTOS = {
    1: {'titulo': 'Plan de seguridad', 'contenido': 'Contenido confidencial...', 'owner_id': 1},
    2: {'titulo': 'Reporte mensual', 'contenido': 'Datos del mes...', 'owner_id': 2},
    3: {'titulo': 'Manual de usuario', 'contenido': 'Instrucciones...', 'owner_id': 2},
}

next_doc_id = 4

# ============================================================
# DECORADORES DE SEGURIDAD
# ============================================================

def requiere_permiso(permiso):
    """Decorador que verifica que el usuario tenga un permiso especifico"""
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if 'user_id' not in session:
                return jsonify({'error': 'No autenticado'}), 401

            user_id = session['user_id']
            if user_id not in USUARIOS:
                session.clear()
                return jsonify({'error': 'Usuario no valido'}), 401

            user_role = USUARIOS[user_id]['role']
            user_permisos = PERMISOS.get(user_role, [])

            if permiso not in user_permisos:
                return jsonify({
                    'error': 'Permiso denegado',
                    'detalle': f'Se requiere permiso: {permiso}, rol actual: {user_role}'
                }), 403

            return f(*args, **kwargs)
        return wrapper
    return decorator

def requiere_pertenencia_o_admin(f):
    """Decorador que verifica que el recurso pertenezca al usuario o sea admin"""
    @wraps(f)
    def wrapper(doc_id, *args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'No autenticado'}), 401

        user_id = session['user_id']
        user_role = USUARIOS[user_id]['role']

        if doc_id not in DOCUMENTOS:
            return jsonify({'error': 'Documento no encontrado'}), 404

        # Admin puede acceder a todo
        if user_role == 'admin':
            return f(doc_id, *args, **kwargs)

        # User/viewer solo a sus propios documentos
        if DOCUMENTOS[doc_id]['owner_id'] != user_id:
            return jsonify({'error': 'No tienes permiso para acceder a este documento'}), 403

        return f(doc_id, *args, **kwargs)
    return wrapper

# ============================================================
# RUTAS DE AUTENTICACION
# ============================================================

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username', '')
    password = data.get('password', '')

    for uid, u in USUARIOS.items():
        if u['username'] == username and u['password'] == password:
            session['user_id'] = uid
            session['username'] = username
            session['role'] = u['role']
            return jsonify({
                'mensaje': 'Login exitoso',
                'usuario': username,
                'rol': u['role'],
                'permisos': PERMISOS[u['role']]
            })

    return jsonify({'error': 'Credenciales invalidas'}), 401

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'mensaje': 'Sesion cerrada'})

# ============================================================
# RUTAS DE DOCUMENTOS CON RBAC
# ============================================================

@app.route('/api/documentos', methods=['GET'])
@requiere_permiso('documentos:listar')
def listar_documentos():
    user_id = session['user_id']
    user_role = USUARIOS[user_id]['role']

    if user_role == 'admin':
        # Admin ve todos
        docs = [{'id': k, 'titulo': v['titulo'], 'owner_id': v['owner_id']}
                for k, v in DOCUMENTOS.items()]
    else:
        # User/viewer solo ven los suyos
        docs = [{'id': k, 'titulo': v['titulo'], 'owner_id': v['owner_id']}
                for k, v in DOCUMENTOS.items() if v['owner_id'] == user_id]

    return jsonify(docs)

@app.route('/api/documentos/<int:doc_id>', methods=['GET'])
@requiere_permiso('documentos:leer')
@requiere_pertenencia_o_admin
def obtener_documento(doc_id):
    doc = DOCUMENTOS[doc_id]
    return jsonify(doc)

@app.route('/api/documentos', methods=['POST'])
@requiere_permiso('documentos:crear')
def crear_documento():
    global next_doc_id
    data = request.get_json()
    user_id = session['user_id']

    nuevo_doc = {
        'id': next_doc_id,
        'titulo': data.get('titulo', 'Sin titulo'),
        'contenido': data.get('contenido', ''),
        'owner_id': user_id,
    }
    DOCUMENTOS[next_doc_id] = nuevo_doc
    next_doc_id += 1

    return jsonify(nuevo_doc), 201

@app.route('/api/documentos/<int:doc_id>', methods=['PUT'])
@requiere_permiso('documentos:actualizar')
@requiere_pertenencia_o_admin
def actualizar_documento(doc_id):
    data = request.get_json()
    if 'titulo' in data:
        DOCUMENTOS[doc_id]['titulo'] = data['titulo']
    if 'contenido' in data:
        DOCUMENTOS[doc_id]['contenido'] = data['contenido']
    return jsonify(DOCUMENTOS[doc_id])

@app.route('/api/documentos/<int:doc_id>', methods=['DELETE'])
@requiere_permiso('documentos:eliminar')
@requiere_pertenencia_o_admin
def eliminar_documento(doc_id):
    doc = DOCUMENTOS.pop(doc_id)
    return jsonify({'mensaje': f'Documento {doc_id} eliminado'})

@app.route('/api/usuarios', methods=['GET'])
@requiere_permiso('usuarios:gestionar')
def listar_usuarios():
    # Solo admin puede listar usuarios
    return jsonify([
        {'id': uid, 'username': u['username'], 'role': u['role']}
        for uid, u in USUARIOS.items()
    ])

@app.route('/api/configuracion', methods=['GET', 'PUT'])
@requiere_permiso('configuracion:editar')
def configuracion():
    # Solo admin puede ver/editar configuracion
    return jsonify({'mensaje': 'Configuracion del sistema', 'admin_only': True})

# ============================================================
# PRUEBAS
# ============================================================

def run_tests():
    """Pruebas automatizadas para verificar RBAC"""
    import requests

    base = "http://127.0.0.1:5000"
    test_session = requests.Session()

    def print_test(name, result, expected=True):
        status = "PASS" if result == expected else "FAIL"
        print(f"[{status}] {name}")

    # Test 1: Login como viewer
    r = test_session.post(f"{base}/login", json={'username': 'invitado', 'password': 'view123'})
    print_test("Login viewer", r.status_code == 200)
    data = r.json()
    print(f"  Rol: {data['rol']}, Permisos: {data['permisos']}")

    # Test 2: Viewer intenta crear documento (debe fallar)
    r = test_session.post(f"{base}/api/documentos", json={'titulo': 'Test', 'contenido': 'test'})
    print_test("Viewer no puede crear documentos", r.status_code == 403)

    # Test 3: Viewer puede leer documentos
    r = test_session.get(f"{base}/api/documentos")
    print_test("Viewer puede listar documentos", r.status_code == 200)

    # Test 4: Login como user
    r = test_session.post(f"{base}/login", json={'username': 'juan', 'password': 'user123'})
    print_test("Login user", r.status_code == 200)

    # Test 5: User crea documento
    r = test_session.post(f"{base}/api/documentos", json={'titulo': 'Mi documento', 'contenido': 'Secreto'})
    print_test("User crea documento", r.status_code == 201)

    # Test 6: User intenta eliminar (debe fallar)
    r = test_session.delete(f"{base}/api/documentos/1")
    print_test("User no puede eliminar documentos", r.status_code == 403)

    # Test 7: Login como admin
    r = test_session.post(f"{base}/login", json={'username': 'admin', 'password': 'admin123'})
    print_test("Login admin", r.status_code == 200)

    # Test 8: Admin puede eliminar cualquier documento
    r = test_session.delete(f"{base}/api/documentos/1")
    print_test("Admin puede eliminar cualquier documento", r.status_code == 200)

    # Test 9: Admin puede gestionar usuarios
    r = test_session.get(f"{base}/api/usuarios")
    print_test("Admin lista usuarios", r.status_code == 200)
    print(f"  Usuarios: {r.json()}")

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)
```

**Ejecutar pruebas:**

```bash
# Terminal 1: Iniciar servidor
python rbac_api.py

# Terminal 2: Ejecutar pruebas
# Descomentar run_tests() al final del archivo y ejecutar:
python -c "from rbac_api import *; run_tests()"
```

---

## Ejercicio 3: Path Traversal - Version Vulnerable y Segura

### Escenario

Un endpoint sirve archivos de usuario. La version vulnerable permite path traversal.

**Version vulnerable:**

```python
"""
path_traversal_vulnerable.py
"""
from flask import Flask, send_file, request, jsonify
import os

app = Flask(__name__)
BASE_DIR = os.path.join(os.getcwd(), 'user_files')

@app.route('/api/files/<path:filename>')
def get_file(filename):
    # VULNERABLE: filename puede contener ../ para escapar del directorio
    filepath = os.path.join(BASE_DIR, filename)
    print(f"Intentando leer: {filepath}")
    try:
        return send_file(filepath)
    except FileNotFoundError:
        return jsonify({'error': 'Archivo no encontrado'}), 404
```

**Ataque:** `GET /api/files/../../../etc/passwd`

**Version corregida con path validation:**

```python
"""
path_traversal_seguro.py
"""
from flask import Flask, send_file, request, jsonify, abort
import os

app = Flask(__name__)
BASE_DIR = os.path.abspath(os.path.join(os.getcwd(), 'user_files'))

# Asegurar que el directorio base existe
os.makedirs(BASE_DIR, exist_ok=True)

def safe_path(base_dir, filename):
    """
    Valida y retorna un path seguro dentro de base_dir.
    Previene path traversal resolviendo el path absoluto
    y verificando que este dentro del directorio permitido.
    """
    # 1. Resolver el path absoluto
    absolute_path = os.path.abspath(os.path.join(base_dir, filename))

    # 2. Verificar que el path resuelto este dentro del directorio base
    if not absolute_path.startswith(base_dir + os.sep):
        return None

    # 3. Verificar que el archivo exista
    if not os.path.isfile(absolute_path):
        return None

    return absolute_path

@app.route('/api/files/<path:filename>')
def get_file(filename):
    filepath = safe_path(BASE_DIR, filename)

    if filepath is None:
        return jsonify({'error': 'Archivo no encontrado o acceso denegado'}), 404

    try:
        return send_file(filepath)
    except Exception as e:
        return jsonify({'error': f'Error al leer archivo: {str(e)}'}), 500

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Ejemplo de subida segura de archivos"""
    if 'file' not in request.files:
        return jsonify({'error': 'No se envio archivo'}), 400

    file = request.files['file']

    # 1. Validar nombre de archivo (evitar path traversal en el nombre)
    filename = os.path.basename(file.filename)  # Solo el nombre base, sin directorios
    if not filename:
        return jsonify({'error': 'Nombre de archivo invalido'}), 400

    # 2. Validar extension (opcional, depende del caso)
    allowed_extensions = {'.txt', '.pdf', '.jpg', '.png', '.docx'}
    ext = os.path.splitext(filename)[1].lower()
    if ext not in allowed_extensions:
        return jsonify({'error': f'Extension {ext} no permitida'}), 400

    # 3. Generar nombre unico para prevenir colisiones
    import uuid
    unique_name = f"{uuid.uuid4().hex}{ext}"
    save_path = os.path.join(BASE_DIR, unique_name)

    # 4. Guardar archivo
    file.save(save_path)

    return jsonify({
        'mensaje': 'Archivo subido exitosamente',
        'filename': unique_name,
        'url': f'/api/files/{unique_name}'
    })

# ============================================================
# PRUEBAS
# ============================================================

def test_security():
    """Pruebas de seguridad contra path traversal"""
    import requests

    base = "http://127.0.0.1:5000"

    # Prueba 1: Path traversal simple
    r = requests.get(f"{base}/api/files/../../../etc/passwd")
    print(f"Path traversal simple: {r.status_code} - {r.json()}")

    # Prueba 2: Path traversal con encoding
    r = requests.get(f"{base}/api/files/..%2f..%2f..%2fetc%2fpasswd")
    print(f"Path traversal encoded: {r.status_code} - {r.json()}")

    # Prueba 3: Path traversal con doble encoding
    r = requests.get(f"{base}/api/files/%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd")
    print(f"Path traversal double encoded: {r.status_code} - {r.json()}")

    # Prueba 4: Path traversal con backslash (Windows)
    r = requests.get(f"{base}/api/files/..\\..\\..\\windows\\win.ini")
    print(f"Path traversal backslash: {r.status_code} - {r.json()}")

    # Prueba 5: Acceso legitimo (crear archivo de prueba primero)
    import os
    test_file = os.path.join(os.path.dirname(__file__), 'user_files', 'test.txt')
    os.makedirs(os.path.dirname(test_file), exist_ok=True)
    with open(test_file, 'w') as f:
        f.write('Contenido de prueba')

    r = requests.get(f"{base}/api/files/test.txt")
    print(f"Acceso legitimo: {r.status_code} - {r.text}")

    # Prueba 6: Archivo inexistente
    r = requests.get(f"{base}/api/files/noexiste.txt")
    print(f"Archivo inexistente: {r.status_code} - {r.json()}")

if __name__ == '__main__':
    # Descomentar para probar: test_security()
    app.run(host='127.0.0.1', port=5000, debug=False)
```

---

## Preguntas y Respuestas

### Pregunta 1
**Cual es la diferencia fundamental entre autenticacion y autorizacion? De un ejemplo donde falle cada una.**

**Respuesta:** La autenticacion verifica la identidad (quien eres), mientras que la autorizacion verifica los permisos (que puedes hacer). Ejemplo de falla de autenticacion: un sistema que permite login con contrasenas debiles o sin 2FA, permitiendo que un atacante ingrese como otro usuario. Ejemplo de falla de autorizacion: un usuario normal que accede a `/api/admin/delete` porque el sistema no verifica su rol antes de ejecutar la accion. Ambas deben funcionar correctamente para tener seguridad; una sin la otra es insuficiente.

### Pregunta 2
**Que es IDOR y como se previene? De un ejemplo concreto.**

**Respuesta:** IDOR (Insecure Direct Object Reference) ocurre cuando una aplicacion expone identificadores internos (IDs numericos, UUIDs, nombres de archivo) y no verifica que el usuario tenga permiso para acceder a ese objeto. Ejemplo: `GET /api/factura/123` devuelve la factura sin verificar que pertenezca al usuario autenticado. Prevencion: (1) siempre verificar que el recurso pertenece al usuario antes de devolverlo, (2) usar identificadores no predecibles (UUIDs), (3) implementar controles de acceso a nivel de objeto, (4) nunca confiar en IDs enviados por el cliente sin validacion del lado del servidor.

### Pregunta 3
**Que es path traversal y como se mitiga eficazmente?**

**Respuesta:** Path traversal es una tecnica donde el atacante usa `../` (o variantes como `..%2f`, `....//`, `..\\`) para navegar fuera del directorio permitido y acceder a archivos arbitrarios del sistema. Mitigaciones: (1) no confiar en el input del usuario para construir paths del sistema de archivos, (2) normalizar el path con `os.path.abspath()` y verificar que comience con el directorio base permitido, (3) usar `os.path.basename()` para eliminar componentes de directorio, (4) desactivar el soporte de path traversal en el servidor web, (5) usar identificadores numericos o UUIDs en lugar de nombres de archivo directos.

### Pregunta 4
**Explica el principio de minimo privilegio con un ejemplo practico en una aplicacion web.**

**Respuesta:** El principio de minimo privilegio establece que cada usuario, proceso o sistema debe tener exactamente los permisos necesarios para realizar su funcion, ni mas ni menos. Ejemplo practico en una aplicacion web: (1) los usuarios viewer solo tienen permiso de lectura en documentos especificos, (2) los usuarios user tienen lectura y escritura pero solo en documentos propios, (3) solo los admins tienen permiso de eliminacion y gestion de usuarios. Esto limita el dano potencial: si un atacante compromete una cuenta viewer, no puede modificar ni eliminar datos; si compromete una cuenta user, solo afecta datos de ese usuario, no del sistema completo.

### Pregunta 5
**Como implementarias un sistema de control de acceso robusto en una API REST?**

**Respuesta:** Un sistema robusto incluye: (1) autenticacion fuerte (JWT con expiration corto, refresh tokens, 2FA opcional), (2) un modelo de permisos granular (no solo roles, sino permisos especificos como `documentos:leer`, `documentos:eliminar`), (3) verificacion en cada endpoint usando decoradores/middleware (nunca solo en el frontend), (4) verificacion de pertenencia del recurso (el usuario solo accede a sus propios recursos a menos que sea admin), (5) logging de todos los accesos denegados para deteccion de ataques, (6) pruebas automatizadas que verifiquen que cada rol solo puede hacer lo que debe, (7) revision periodica de la matriz de permisos.

### Pregunta 6
**Cual es el riesgo de confiar en el rol que el cliente envia en la request?**

**Respuesta:** Confiar en el rol enviado por el cliente es extremadamente peligroso porque cualquier atacante puede modificar la request para enviar un rol de admin. Ejemplo: un sistema que lee `request.json.get('role')` para determinar si el usuario es admin. Un atacante simplemente envia `{"role": "admin"}` en el body de la request y obtiene privilegios administrativos. La unica fuente confiable del rol debe ser el servidor, obtenido de la sesion del usuario o del token JWT firmado, nunca de parametros que el cliente pueda manipular.

---

## Tarea / Lectura Recomendada

1. **Leer:** OWASP Authorization Cheat Sheet - https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html
2. **Leer:** OWASP Access Control Cheat Sheet - https://cheatsheetseries.owasp.org/cheatsheets/Access_Control_Cheat_Sheet.html
3. **Practicar:** PortSwigger - Access Control labs: https://portswigger.net/web-security/access-control
4. **Leer:** OWASP Insecure Direct Object Reference Prevention - https://cheatsheetseries.owasp.org/cheatsheets/Insecure_Direct_Object_Reference_Prevention_Cheat_Sheet.html
5. **Practicar:** Implementar RBAC en un proyecto propio usando decoradores en Python o middleware en Express/Spring
6. **Experimentar:** Usar Burp Suite para interceptar requests de una app vulnerable a IDOR y modificar parametros



