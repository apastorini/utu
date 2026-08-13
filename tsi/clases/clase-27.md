# Clase 27: Principios de Desarrollo Seguro - Security by Design

**Duracion:** 2 horas

---

## Objetivos de Aprendizaje

1. Comprender la diferencia entre Security by Design y Security by Obscurity
2. Aplicar los principios fundamentales de seguridad en el diseno de software
3. Conocer los OWASP Proactive Controls (C1-C10)
4. Evaluar disenos de arquitectura identificando violaciones a principios de seguridad
5. Implementar patrones de diseno seguro como fail secure, defensa en profundidad

---

## Contenido Detallado

### 1. Security by Design vs. Security by Obscurity

**Security by Design:** La seguridad se incorpora desde las primeras etapas del diseno del software, no como una capa final. Es un enfoque proactivo donde cada decision de diseno considera las implicaciones de seguridad.

**Security by Obscurity:** Confiar en que el sistema es seguro porque sus detalles internos estan ocultos. Ejemplos clasicos: codigo fuente secreto, algoritmos propietarios no publicados, rutas ocultas.

| Aspecto | Security by Design | Security by Obscurity |
|---------|-------------------|----------------------|
| Enfoque | Proactivo (diseno) | Reactivo (ocultamiento) |
| Mecanismo | Controles de seguridad robustos | Dependencia del secreto |
| Si se revela el secreto | El sistema sigue siendo seguro | El sistema se compromete |
| Ejemplo | Cifrado AES con clave secreta | Algoritmo de cifrado secreto |
| Evaluacion | Puede ser auditado publicamente | No puede ser verificado |
| Resultado | Seguridad a largo plazo | Falsa sensacion de seguridad |

**Ley de Shannon (Kerckhoffs):** Un sistema debe ser seguro incluso si todo lo relacionado con el sistema, excepto la clave, es de conocimiento publico.

### 2. Principios Fundamentales de Seguridad

#### Minimo Privilegio (Principle of Least Privilege)

Cada usuario, proceso o sistema debe tener exactamente los permisos necesarios para realizar su funcion, ni mas ni menos.

**Aplicacion:**
- Usuarios solo tienen permisos para sus recursos
- Procesos corren con la minima cuenta necesaria (no root)
- Contenedores sin privilegios (no --privileged)
- APIs exponen solo los endpoints necesarios

#### Defensa en Profundidad (Defense in Depth)

Multiples capas de seguridad. Si una capa falla, la siguiente detiene el ataque.

```
CAPAS DE DEFENSA:
+--------------------------------------------------+
| 1. Firewall perimetral                            |
| 2. WAF (Web Application Firewall)                 |
| 3. Autenticacion + Autorizacion                   |
| 4. Validacion de input + Sanitizacion              |
| 5. Cifrado en transito y reposo                   |
| 6. Logging y monitoreo                            |
| 7. Principio de minimo privilegio                 |
+--------------------------------------------------+
```

#### Superficie de Ataque Minima

Reducir al minimo los puntos de entrada que un atacante puede explotar.

**Como reducir la superficie de ataque:**
- Deshabilitar servicios y puertos no utilizados
- Cerrar endpoints de API no utilizados
- Desactivar funcionalidades innecesarias
- NO exponer informacion interna (versiones, stack traces)
- Usar interfaces minimalistas

#### Fallo Seguro (Fail Secure / Fail Safe)

Cuando un sistema falla, debe hacerlo en un estado seguro (denegar acceso por defecto).

```python
# MAL: Fail open - si falla la verificacion, permite acceso
def check_permission(user, resource):
    try:
        return verify_permission(user, resource)
    except Exception:
        return True  # PELIGROSO: falla a "permitido"

# BIEN: Fail secure - si falla, deniega acceso
def check_permission(user, resource):
    try:
        return verify_permission(user, resource)
    except Exception:
        return False  # SEGURO: falla a "denegado"
```

#### Separacion de Responsabilidades (Separation of Duties)

Ninguna persona o sistema debe tener el control completo de una operacion critica.

**Ejemplos:**
- Quien aprueba un pago no puede ejecutarlo
- Quien despliega codigo no puede aprobar el deploy
- Admin de BD no es el mismo que admin de sistema
- Dos personas necesarias para acceder a una boveda

#### Economia de Mecanismo (Economy of Mechanism)

Los mecanismos de seguridad deben ser simples y pequenos. La complejidad introduce errores.

**Principio:** Un diseno simple es mas facil de auditar, mantener y verificar que uno complejo.

#### Mediacion Completa (Complete Mediation)

Cada acceso a cada recurso debe ser verificado contra una politica de autorizacion. No confiar en resultados de verificaciones anteriores.

```python
# MAL: Verificar solo al inicio de la sesion
@app.route('/api/admin/delete')
def admin_delete():
    # Verificacion solo al login - asume que el usuario sigue siendo admin
    pass

# BIEN: Verificar en CADA operacion
@app.route('/api/admin/delete', methods=['POST'])
@requires_role('admin')  # Se verifica en CADA request
def admin_delete():
    pass
```

### 3. OWASP Proactive Controls (C1-C10)

| Control | Descripcion |
|---------|-------------|
| **C1** | Definir requisitos de seguridad |
| **C2** | Aprovechar frameworks de seguridad existentes |
| **C3** | Proteger datos en transito (TLS 1.2+) y en reposo (cifrado) |
| **C4** | Validar todo input (whitelist, parametrizacion) |
| **C5** | Implementar autenticacion e identidad robusta |
| **C6** | Implementar autorizacion (RBAC, ABAC) en cada endpoint |
| **C7** | Configurar correctamente la seguridad (headers, CORS, CSP) |
| **C8** | Manejar sesiones de forma segura (HttpOnly, Secure, SameSite) |
| **C9** | Proteger contra XSS (escape, CSP, sanitizacion) |
| **C10** | Manejar errores y logging de forma segura |

---

## Ejercicio 1: Redisenar un Sistema de Archivos Compartidos con Security by Design

### Escenario

Un sistema actual de archivos compartidos tiene multiples problemas de seguridad. Redisenarlo aplicando Security by Design.

**Sistema actual (inseguro):**

```python
"""
sistema_archivos_inseguro.py - Sistema con multiples violaciones de seguridad
"""
import os
import shutil
from flask import Flask, request, jsonify, send_file

app = Flask(__name__)

BASE_DIR = '/shared/files'

# Sin autenticacion - cualquiera puede acceder
# Sin autorizacion - cualquiera puede leer/escribir cualquier archivo
# Sin cifrado - archivos en texto plano
# Sin logging - no hay registro de accesos

@app.route('/files/<path:filename>')
def get_file(filename):
    # Puede leer cualquier archivo del sistema
    filepath = os.path.join(BASE_DIR, filename)
    return send_file(filepath)

@app.route('/files/upload', methods=['POST'])
def upload_file():
    # Cualquiera puede subir archivos sin restriccion
    file = request.files['file']
    filepath = os.path.join(BASE_DIR, file.filename)
    file.save(filepath)
    return jsonify({'mensaje': 'Archivo subido'})

@app.route('/files/delete/<path:filename>', methods=['DELETE'])
def delete_file(filename):
    # Cualquiera puede eliminar cualquier archivo
    filepath = os.path.join(BASE_DIR, filename)
    os.remove(filepath)
    return jsonify({'mensaje': 'Archivo eliminado'})
```

**Rediseno aplicando Security by Design:**

```python
"""
sistema_archivos_seguro.py - Rediseno con Security by Design
"""
import os
import uuid
import hashlib
import hmac
import logging
from datetime import datetime, timezone
from functools import wraps
from typing import Set, Optional

from flask import Flask, request, jsonify, send_file, session, abort, g

app = Flask(__name__)
app.secret_key = os.urandom(32).hex()

# ============================================================
# CONFIGURACION
# ============================================================

STORAGE_DIR = os.path.abspath(os.environ.get('STORAGE_DIR', '/shared/secure_files'))
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
ALLOWED_EXTENSIONS: Set[str] = {'.txt', '.pdf', '.jpg', '.png', '.docx', '.xlsx', '.zip'}
ALLOWED_MIME_TYPES: Set[str] = {
    'text/plain', 'application/pdf', 'image/jpeg', 'image/png',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'application/zip',
}

# ============================================================
# PRINCIPIO 1: MINIMO PRIVILEGIO
# ============================================================

class RBAC:
    """Control de acceso basado en roles con minimo privilegio"""

    ROLES = {
        'admin': {'read', 'write', 'delete', 'manage_users', 'audit'},
        'editor': {'read', 'write'},
        'viewer': {'read'},
    }

    @staticmethod
    def has_permission(user_role: str, permission: str) -> bool:
        return permission in RBAC.ROLES.get(user_role, set())


# ============================================================
# PRINCIPIO 2: DEFENSA EN PROFUNDIDAD
# ============================================================

# CAPA 1: Autenticacion
def require_auth(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Autenticacion requerida'}), 401
        g.user_id = session['user_id']
        g.username = session.get('username', '')
        g.user_role = session.get('role', 'viewer')
        return f(*args, **kwargs)
    return wrapper

# CAPA 2: Autorizacion
def require_permission(permission: str):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if not RBAC.has_permission(g.user_role, permission):
                app.logger.warning(
                    f"Acceso denegado: user={g.username} role={g.user_role} "
                    f"required={permission} resource={request.path}"
                )
                return jsonify({'error': 'Permiso denegado'}), 403
            return f(*args, **kwargs)
        return wrapper
    return decorator

# CAPA 3: Path traversal prevention
def sanitize_filename(filename: str) -> Optional[str]:
    """Previene path traversal - solo permite el nombre base"""
    clean = os.path.basename(filename)
    if not clean or clean.startswith('.'):
        return None
    return clean

# CAPA 4: Validacion de archivos
def validate_file(filename: str, file_size: int) -> bool:
    if file_size > MAX_FILE_SIZE:
        return False
    ext = os.path.splitext(filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        return False
    return True


# ============================================================
# PRINCIPIO 3: FALLO SEGURO
# ============================================================

def safe_get_file(filepath: str) -> Optional[str]:
    """
    PRINCIPIO: Fail secure
    Si algo falla (path invalido, archivo no existe, error de permisos),
    retorna None en lugar de lanzar excepcion que podria revelar informacion.
    """
    try:
        abs_path = os.path.abspath(filepath)

        # Verificar que el path resuelto esta dentro del directorio permitido
        if not abs_path.startswith(os.path.abspath(STORAGE_DIR) + os.sep):
            return None

        if not os.path.isfile(abs_path):
            return None

        # No seguir enlaces simbolicos
        if os.path.islink(abs_path):
            return None

        return abs_path
    except Exception:
        # Fail secure: en caso de error, denegar acceso
        return None


# ============================================================
# PRINCIPIO 4: SEPARACION DE RESPONSABILIDADES
# ============================================================

# Los roles estan claramente separados:
# - viewer: solo lectura
# - editor: lectura y escritura (no puede eliminar)

# ============================================================
# PRINCIPIO 5: MEDIACION COMPLETA
# ============================================================

# Cada endpoint verifica permisos independientemente
# No se asume que porque el usuario esta autenticado tiene permiso


# ============================================================
# PRINCIPIO 6: ECONOMIA DE MECANISMO
# ============================================================

# La logica de autorizacion es simple y directa:
# 1. Verificar autenticacion (who are you?)
# 2. Verificar permiso (what can you do?)
# 3. Ejecutar accion


# ============================================================
# PRINCIPIO 7: SUPERFICIE DE ATAQUE MINIMA
# ============================================================

# Solo los endpoints necesarios estan expuestos
# Sin debug endpoints en produccion
# Sin informacion de version en respuestas


# ============================================================
# LOGGING (OWASP C10)
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('audit.log'),
        logging.StreamHandler(),
    ]
)

def log_action(action: str, resource: str, success: bool, detail: str = ''):
    app.logger.info(
        f"ACTION={action} USER={g.get('username', 'anon')} "
        f"ROLE={g.get('user_role', 'anon')} "
        f"RESOURCE={resource} SUCCESS={success} "
        f"IP={request.remote_addr} DETAIL={detail}"
    )


# ============================================================
# RUTAS SEGURAS
# ============================================================

@app.route('/login', methods=['POST'])
def login():
    """Autenticacion con credenciales verificadas"""
    data = request.get_json()
    # En produccion, verificar contra BD con bcrypt
    username = data.get('username', '')
    password = data.get('password', '')

    # Simulacion de verificacion
    users = {
        'admin': {'password': 'admin123', 'role': 'admin', 'id': 1},
        'editor1': {'password': 'editor123', 'role': 'editor', 'id': 2},
        'viewer1': {'password': 'viewer123', 'role': 'viewer', 'id': 3},
    }

    if username in users and users[username]['password'] == password:
        session['user_id'] = users[username]['id']
        session['username'] = username
        session['role'] = users[username]['role']
        app.logger.info(f"Login exitoso: {username} ({users[username]['role']})")
        return jsonify({
            'mensaje': 'Login exitoso',
            'usuario': username,
            'rol': users[username]['role'],
        })

    app.logger.warning(f"Login fallido: {username}")
    return jsonify({'error': 'Credenciales invalidas'}), 401


@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'mensaje': 'Sesion cerrada'})


@app.route('/api/files', methods=['GET'])
@require_auth
@require_permission('read')
def list_files():
    """
    PRINCIPIO: Minimo privilegio
    - viewer: solo ve sus archivos
    - editor: solo ve sus archivos (o los que creo)
    - admin: puede ver todos
    """
    user_id = g.user_id
    user_role = g.user_role

    files = []
    try:
        for fname in os.listdir(STORAGE_DIR):
            filepath = safe_get_file(os.path.join(STORAGE_DIR, fname))
            if filepath is None:
                continue

            stat = os.stat(filepath)

            # Minimo privilegio: segun rol, ver diferentes archivos
            if user_role == 'admin':
                files.append({
                    'nombre': fname,
                    'tamano': stat.st_size,
                    'creado': datetime.fromtimestamp(stat.st_ctime, tz=timezone.utc).isoformat(),
                    'modificado': datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat(),
                })
            elif user_role in ('editor', 'viewer'):
                # En un sistema real, filtrar por ownership
                files.append({
                    'nombre': fname,
                    'tamano': stat.st_size,
                    # No incluir metadata sensible para viewers
                })
    except FileNotFoundError:
        os.makedirs(STORAGE_DIR, exist_ok=True)

    log_action('LIST_FILES', '/api/files', True, f'found={len(files)}')
    return jsonify({'archivos': files})


@app.route('/api/files/<path:filename>', methods=['GET'])
@require_auth
@require_permission('read')
def get_file(filename):
    """
    PRINCIPIO: Defensa en profundidad
    CAPA 1: Autenticacion (require_auth)
    CAPA 2: Autorizacion (require_permission)
    CAPA 3: Sanitizacion de nombre
    CAPA 4: Path traversal prevention
    """
    # CAPA 3: Sanitizacion
    safe_name = sanitize_filename(filename)
    if safe_name is None:
        log_action('GET_FILE', filename, False, 'invalid_filename')
        return jsonify({'error': 'Nombre de archivo invalido'}), 400

    # CAPA 4: Path traversal y validacion
    filepath = safe_get_file(os.path.join(STORAGE_DIR, safe_name))
    if filepath is None:
        log_action('GET_FILE', filename, False, 'file_not_found_or_blocked')
        return jsonify({'error': 'Archivo no encontrado'}), 404

    log_action('GET_FILE', safe_name, True)
    try:
        return send_file(filepath)
    except Exception:
        log_action('GET_FILE', safe_name, False, 'send_error')
        return jsonify({'error': 'Error al leer archivo'}), 500


@app.route('/api/files/upload', methods=['POST'])
@require_auth
@require_permission('write')
def upload_file():
    """
    PRINCIPIO: Fallo seguro
    Si la validacion falla, NO se guarda el archivo.
    """
    if 'file' not in request.files:
        return jsonify({'error': 'No se envio archivo'}), 400

    file = request.files['file']

    # Validar tamano
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0)

    if size > MAX_FILE_SIZE:
        log_action('UPLOAD', file.filename, False, 'file_too_large')
        return jsonify({'error': f'Archivo demasiado grande (max {MAX_FILE_SIZE//1024//1024}MB)'}), 400

    # Validar extension
    if not validate_file(file.filename, size):
        log_action('UPLOAD', file.filename, False, 'invalid_extension')
        return jsonify({'error': 'Tipo de archivo no permitido'}), 400

    # Generar nombre seguro y unico (previene colisiones y path traversal)
    ext = os.path.splitext(file.filename)[1].lower()
    unique_name = f"{uuid.uuid4().hex}{ext}"

    filepath = os.path.join(STORAGE_DIR, unique_name)

    # Fail secure: validar que el path es seguro
    safe_path = safe_get_file(filepath)
    if safe_path is None:
        log_action('UPLOAD', file.filename, False, 'path_validation_failed')
        return jsonify({'error': 'Error de seguridad al guardar'}), 500

    try:
        file.save(safe_path)

        # Registrar metadata
        log_action('UPLOAD', f"{unique_name} (original: {file.filename})", True)

        return jsonify({
            'mensaje': 'Archivo subido exitosamente',
            'filename': unique_name,
            'original_name': file.filename,
            'size': size,
        }), 201

    except Exception as e:
        log_action('UPLOAD', file.filename, False, f'save_error: {str(e)}')
        return jsonify({'error': 'Error al guardar archivo'}), 500


@app.route('/api/files/<path:filename>', methods=['DELETE'])
@require_auth
@require_permission('delete')
def delete_file(filename):
    """Solo admin puede eliminar (minimo privilegio)"""
    safe_name = sanitize_filename(filename)
    if safe_name is None:
        return jsonify({'error': 'Nombre de archivo invalido'}), 400

    filepath = safe_get_file(os.path.join(STORAGE_DIR, safe_name))
    if filepath is None:
        return jsonify({'error': 'Archivo no encontrado'}), 404

    try:
        os.remove(filepath)
        log_action('DELETE', safe_name, True)
        return jsonify({'mensaje': 'Archivo eliminado'})
    except Exception as e:
        log_action('DELETE', safe_name, False, str(e))
        return jsonify({'error': 'Error al eliminar archivo'}), 500


@app.route('/api/audit/logs', methods=['GET'])
@require_auth
@require_permission('audit')
def get_audit_logs():
    """Solo admin con permiso audit puede ver logs"""
    try:
        with open('audit.log', 'r') as f:
            lines = f.readlines()[-100:]  # Ultimas 100 lineas
        return jsonify({'logs': lines})
    except FileNotFoundError:
        return jsonify({'logs': []})


if __name__ == '__main__':
    os.makedirs(STORAGE_DIR, exist_ok=True)
    print(f"Sistema de archivos seguro iniciado")
    print(f"Directorio de almacenamiento: {STORAGE_DIR}")
    print("Principios aplicados: Minimo privilegio, Defensa en profundidad,")
    print("  Fallo seguro, Separacion de responsabilidades,")
    print("  Mediacion completa, Economia de mecanismo,")
    print("  Superficie de ataque minima")
    app.run(host='127.0.0.1', port=5000)
```

---

## Ejercicio 2: Evaluar un Diseno de Arquitectura

### Escenario

Evaluar la siguiente descripcion de arquitectura de un sistema de e-commerce y encontrar 5 violaciones a principios de seguridad, proponiendo correcciones.

**Descripcion del sistema:**

```
Sistema de e-commerce "CompraFacil"

1. Los usuarios se autentican con usuario y contrasena (sin 2FA).
2. La sesion se mantiene con cookies sin HttpOnly ni Secure.
3. El API REST expone endpoints como:
   - GET /api/productos (publico)
   - GET /api/pedidos/{id} (autenticado, devuelve datos del pedido)
   - POST /api/pedidos/{id}/cancelar (autenticado)
   - GET /api/admin/usuarios (autenticado, devuelve todos los usuarios)
4. La base de datos almacena contrasenas en MD5 sin salt.
5. Los logs registran todas las requests incluyendo body completo.
6. El servidor usa HTTP (no HTTPS) en entorno de staging.
7. Los archivos de configuracion con claves de API estan en el repositorio Git.
8. El sistema usa una libreria de procesamiento de imagenes con vulnerabilidades conocidas (CVE-2023-XXXX).
9. No hay rate limiting en el endpoint de login.
10. Cuando ocurre un error, se devuelve el stack trace completo.
```

**Solucion: Violaciones y Correcciones**

| # | Violacion | Principio violado | Correccion |
|---|-----------|-------------------|------------|
| 1 | **Contrasenas en MD5 sin salt** | Security by Design (cifrado debil) | Usar bcrypt (cost=12), Argon2id, o PBKDF2 con salt. MD5 puede romperse en segundos con tablas rainbow o GPUs. |
| 2 | **Cookies sin HttpOnly ni Secure** | Defensa en profundidad | Configurar `HttpOnly=True, Secure=True, SameSite=Lax`. Esto protege contra robo de cookies via XSS y asegura que solo se envien por HTTPS. |
| 3 | **GET /api/pedidos/{id} sin verificacion de pertenencia** | Minimo privilegio / IDOR | Verificar que el pedido pertenece al usuario autenticado. Solo admin deberia poder ver pedidos de otros usuarios. Implementar `@require_ownership` decorator. |
| 4 | **GET /api/admin/usuarios accesible sin rol admin** | Minimo privilegio / Mediacion completa | Requerir explícitamente rol admin con un decorador `@require_role('admin')`. No asumir que un endpoint con "admin" en la URL es seguro. |
| 5 | **Logs con body completo de requests** | Minimo privilegio (datos) | Filtrar datos sensibles (contrasenas, tokens, tarjetas) de los logs. Usar logging estructurado con campos especificos, no el body completo. |
| 6 | **HTTP sin HTTPS en staging** | Defensa en profundidad | Forzar HTTPS en TODOS los entornos. Usar certificados de Let's Encrypt incluso en staging. Configurar HSTS. |
| 7 | **Claves de API en repositorio Git** | Security by Design (secretos) | Usar variables de entorno o un vault de secretos (HashiCorp Vault, AWS Secrets Manager). Agregar patrones al .gitignore. Rotar claves comprometidas. |
| 8 | **Libreria vulnerable sin actualizar** | Defensa en profundidad | Implementar SCA (Snyk, Dependabot). Actualizar la libreria a la version parcheada. Si no hay parche, buscar alternativa. |
| 9 | **Sin rate limiting en login** | Defensa en profundidad | Implementar rate limiting (5 intentos/minuto por IP, 10 intentos/hora por usuario). Usar Flask-Limiter o equivalente. Bloquear IP despues de N intentos fallidos. |
| 10 | **Stack traces en respuestas de error** | Superficie de ataque minima | Devolver mensajes genericos ("Error interno del servidor"). Loggear el stack trace completo en el servidor para debugging. |

---

## Ejercicio 3: Reescribir una Funcion Fail Secure

### Escenario

Reescribir la siguiente funcion que maneja archivos para que sea "fail secure" (cuando falla, deniega acceso en lugar de permitirlo).

**Funcion original (fail open - insegura):**

```python
"""
Funcion original con fail open.
Si ocurre cualquier error, permite el acceso por defecto.
"""
import os

def read_user_file(user_id, filename):
    """
    Lee un archivo de usuario.
    VULNERABILIDAD: Si algo falla, retorna el contenido del archivo.
    """
    base_path = f"/var/app/users/{user_id}/files"

    try:
        filepath = os.path.join(base_path, filename)

        # Verificar que el archivo existe
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                content = f.read()
                return content

        # Intenta con mayusculas si no existe
        alt_filename = filename.upper()
        alt_filepath = os.path.join(base_path, alt_filename)
        if os.path.exists(alt_filepath):
            with open(alt_filepath, 'r') as f:
                content = f.read()
                return content

        return "Archivo no encontrado"

    except Exception as e:
        # FAIL OPEN: Si ocurre un error (ej: path traversal bloqueado),
        # devuelve el archivo de todas formas
        print(f"Error: {e}")
        try:
            with open(filepath, 'r') as f:
                return f.read()
        except:
            return f"Error al leer archivo: {e}"
```

**Funcion corregida (fail secure):**

```python
"""
Funcion corregida con fail secure.
Si ocurre cualquier error, deniega el acceso.
"""
import os
import logging

logger = logging.getLogger(__name__)


def read_user_file_safe(user_id: int, filename: str) -> str:
    """
    Lee un archivo de usuario de forma segura.
    PRINCIPIO: Fail secure - si algo falla, deniega acceso.

    Args:
        user_id: ID del usuario (debe ser positivo)
        filename: Nombre del archivo (solo nombre base)

    Returns:
        Contenido del archivo o mensaje de error.

    Raises:
        No lanza excepciones al llamador; siempre retorna un string.
    """
    # 1. Validar parametros de entrada
    if not isinstance(user_id, int) or user_id <= 0:
        logger.warning(f"user_id invalido: {user_id}")
        return "Error: Acceso denegado"

    if not filename or not isinstance(filename, str):
        logger.warning(f"filename invalido: {filename}")
        return "Error: Acceso denegado"

    # 2. Sanitizar nombre de archivo (prevenir path traversal)
    safe_filename = os.path.basename(filename)
    if not safe_filename:
        logger.warning(f"filename vacio despues de sanitizar: {filename}")
        return "Error: Acceso denegado"

    # 3. Construir path base seguro
    base_path = os.path.abspath(f"/var/app/users/{user_id}/files")
    filepath = os.path.abspath(os.path.join(base_path, safe_filename))

    # 4. Verificar que el path resuelto esta dentro del directorio permitido
    #    (prevenir path traversal con ../)
    if not filepath.startswith(base_path + os.sep):
        logger.warning(f"Path traversal detectado: user={user_id} path={filepath}")
        return "Error: Acceso denegado"

    # 5. Intentar leer el archivo con fail secure
    try:
        if not os.path.isfile(filepath):
            logger.info(f"Archivo no encontrado: user={user_id} file={safe_filename}")
            return "Error: Archivo no encontrado"

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        logger.info(f"Archivo leido exitosamente: user={user_id} file={safe_filename} size={len(content)}")
        return content

    except PermissionError:
        logger.error(f"Permiso denegado al leer archivo: user={user_id} file={safe_filename}")
        return "Error: Acceso denegado"

    except FileNotFoundError:
        logger.info(f"Archivo no encontrado (race condition): user={user_id} file={safe_filename}")
        return "Error: Archivo no encontrado"

    except UnicodeDecodeError:
        logger.warning(f"Archivo binario no soportado: user={user_id} file={safe_filename}")
        return "Error: Formato de archivo no soportado"

    except OSError as e:
        # Fail secure: cualquier error de E/S deniega acceso
        logger.error(f"Error de E/S al leer archivo: user={user_id} file={safe_filename} error={e}")
        return "Error: Acceso denegado"

    except Exception as e:
        # Fail secure: cualquier error desconocido deniega acceso
        logger.error(f"Error desconocido al leer archivo: user={user_id} file={safe_filename} error={e}")
        return "Error: Acceso denegado"


def read_user_file_readable(user_id: int, filename: str) -> tuple:
    """
    Version alternativa que retorna (contenido, error) en lugar de strings.
    Mas facil de integrar en APIs REST.
    """
    result = read_user_file_safe(user_id, filename)

    if result.startswith("Error:"):
        return None, result
    return result, None


# ============================================================
# PRUEBAS
# ============================================================

def test_fail_secure():
    """Pruebas de la funcion fail secure"""

    tests = [
        # (user_id, filename, expected_prefix)
        (0, "test.txt", "Error:"),        # user_id invalido
        (-1, "test.txt", "Error:"),       # user_id negativo
        (1, "", "Error:"),                # filename vacio
        (1, None, "Error:"),              # filename None
        (1, "../../etc/passwd", "Error:"), # path traversal
        (1, ".../.../.../etc/passwd", "Error:"), # path traversal alternativo
        (1, "archivo_inexistente.txt", "Error:"), # archivo no existe
    ]

    print("=" * 60)
    print("PRUEBAS: Fail Secure")
    print("=" * 60)

    all_passed = True
    for user_id, filename, expected in tests:
        result = read_user_file_safe(user_id, filename)
        passed = result.startswith(expected)
        status = "PASS" if passed else "FAIL"
        if not passed:
            all_passed = False
        print(f"[{status}] user_id={user_id}, filename={filename!r}")
        print(f"       Esperado: {expected}")
        print(f"       Obtenido: {result[:80]}...")
        print()

    if all_passed:
        print("Todas las pruebas pasaron.")
    else:
        print("Algunas pruebas fallaron.")


def compare_fail_open_vs_fail_secure():
    """Comparacion directa de comportamientos"""

    print("=" * 60)
    print("COMPARACION: Fail Open vs Fail Secure")
    print("=" * 60)

    scenarios = [
        ("Path traversal: ../../../etc/passwd", 1, "../../../etc/passwd"),
        ("Usuario invalido: user_id=-1", -1, "test.txt"),
        ("Archivo inexistente", 1, "no_existe.txt"),
        ("Nombre vacio", 1, ""),
        ("Caracteres especiales", 1, "..\\..\\..\\windows\\win.ini"),
    ]

    for scenario, user_id, filename in scenarios:
        print(f"\nEscenario: {scenario}")
        print(f"  Fail Open (original):   Permitiria acceso (inseguro)")
        print(f"  Fail Secure (corregido): {read_user_file_safe(user_id, filename)}")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    test_fail_secure()
    print()
    compare_fail_open_vs_fail_secure()
```

---

## Preguntas y Respuestas

### Pregunta 1
**Cual es la diferencia fundamental entre Security by Design y Security by Obscurity? De un ejemplo de cada uno.**

**Respuesta:** Security by Design incorpora la seguridad en la arquitectura del sistema desde el principio, usando mecanismos robustos y verificables. Ejemplo: usar AES-256 con clave gestionada por un HSM (Hardware Security Module). Security by Obscurity confia en mantener secretos los detalles internos del sistema. Ejemplo: ocultar la ruta de administracion en `/secretadmin123/` en lugar de implementar autenticacion y autorizacion. La diferencia crucial: si el atacante descubre el "secreto" en Security by Obscurity, el sistema queda completamente comprometido; en Security by Design, el sistema sigue siendo seguro porque los controles de seguridad son intrinsecos, no dependen del ocultamiento.

### Pregunta 2
**Explica el principio de defensa en profundidad con un ejemplo practico en una aplicacion web.**

**Respuesta:** Defensa en profundidad significa tener multiples capas de seguridad independientes, de modo que si una capa falla, la siguiente detiene el ataque. Ejemplo para una aplicacion web: CAPA 1 - Firewall de red que solo permite puertos 80/443. CAPA 2 - WAF (Web Application Firewall) que bloquea SQLi y XSS. CAPA 3 - Autenticacion con 2FA. CAPA 4 - Autorizacion RBAC en cada endpoint. CAPA 5 - Validacion de input en el servidor (parametrizacion, sanitizacion). CAPA 6 - CSP headers que limitan ejecucion de scripts. CAPA 7 - Logging y monitoreo que detectan patrones anomalos. CAPA 8 - Cifrado en reposo de datos sensibles. Si un atacante evade el WAF, la autenticacion lo detiene. Si evade la autenticacion, la autorizacion limita que puede hacer.

### Pregunta 3
**Que es el principio de "fallo seguro" y por que es importante? Da un ejemplo de codigo.**

**Respuesta:** El principio de fallo seguro (fail secure) establece que cuando un sistema falla, debe hacerlo en un estado seguro, tipicamente denegando el acceso en lugar de permitiendolo. Es importante porque los errores son inevitables, y un sistema que "falla abierto" (fail open) puede permitir accesos no autorizados cuando ocurre una excepcion. Ejemplo: en lugar de `try: verificar() except: return True` (fail open - permite acceso si falla la verificacion), se debe usar `try: verificar() except: return False` (fail secure - deniega acceso si falla la verificacion). Similarmente, al leer archivos, si ocurre un error de path traversal o permisos, se debe denegar el acceso en lugar de intentar leer el archivo de todas formas.

### Pregunta 4
**Cuales son los OWASP Proactive Controls mas importantes para un desarrollador backend?**

**Respuesta:** Los 5 mas importantes para backend: (1) **C4 - Validar todo input**: nunca confiar en datos del cliente, usar whitelist de caracteres permitidos, parametrizar consultas SQL, validar tipos y rangos. (2) **C6 - Implementar autorizacion**: verificar permisos en CADA endpoint (no solo al login), implementar RBAC/ABAC, nunca confiar en roles enviados por el cliente. (3) **C7 - Configurar seguridad**: security headers (HSTS, CSP, X-Frame-Options), CORS con whitelist, TLS 1.2+, eliminar configuraciones por defecto. (4) **C9 - Proteger contra XSS**: escapar output segun contexto (HTML, atributo, JS, URL, CSS), usar plantillas con autoescape, implementar CSP. (5) **C10 - Manejo de errores y logging seguro**: nunca devolver stack traces al cliente, loggear eventos de seguridad sin datos sensibles, implementar auditoria.

### Pregunta 5
**Como se aplica el principio de minimo privilegio en una API REST?**

**Respuesta:** En una API REST, el minimo privilegio se aplica en multiples niveles: (1) **Por endpoint**: cada endpoint requiere un permiso especifico (ej: `documentos:eliminar`), no solo un rol. (2) **Por recurso**: los usuarios solo acceden a sus propios recursos a menos que tengan permiso global (admin). (3) **Por metodo**: GET solo lectura, POST creacion, PUT actualizacion, DELETE eliminacion. Un viewer solo tiene GET, un editor GET+POST+PUT, admin todos. (4) **Por campo**: algunos campos solo son visibles para ciertos roles (ej: admin ve email completo, viewer solo email parcial). (5) **Por accion**: operaciones masivas (exportar todos los usuarios, eliminar en lote) requieren permisos adicionales. La implementacion tipica usa decoradores como `@require_permission('documentos:leer')` y verificacion de pertenencia.

### Pregunta 6
**Cual es la relacion entre la superficie de ataque y la seguridad de una aplicacion?**

**Respuesta:** La superficie de ataque es el conjunto de todos los puntos por los que un atacante puede interactuar con el sistema. A mayor superficie de ataque, mayor probabilidad de encontrar una vulnerabilidad explotable. La relacion es directamente proporcional: mas endpoints, mas puertos, mas funcionalidades, mas librerias, mas configuraciones = mas oportunidades para el atacante. Para reducir la superficie de ataque: (1) deshabilitar servicios no utilizados, (2) cerrar endpoints de API que no se usan, (3) minimizar las librerias y dependencias, (4) no exponer informacion interna (versiones, stack traces), (5) usar autenticacion y autorizacion para reducir la superficie accesible a usuarios no autenticados, (6) implementar principios de "secure by default" donde las funcionalidades peligrosas esten deshabilitadas hasta que se configuren explicitamente.

---

## Tarea / Lectura Recomendada

1. **Leer:** OWASP Proactive Controls - https://owasp.org/www-project-proactive-controls/
2. **Leer:** OWASP Cheat Sheet Series - https://cheatsheetseries.owasp.org/
3. **Leer:** "Security by Design Principles" (Microsoft) - https://learn.microsoft.com/en-us/azure/well-architected/security/security-principles
4. **Practicar:** Realizar un threat modeling de una aplicacion simple usando STRIDE
5. **Leer:** OWASP ASVS - Application Security Verification Standard - https://owasp.org/www-project-application-security-verification-standard/
6. **Profundizar:** Investigar el modelo STRIDE (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege)
7. **Evaluar:** Elegir un proyecto personal o laboral y evaluar cuantos principios de seguridad cumple
8. **Leer:** "The Security Development Lifecycle" de Microsoft (SDL)



