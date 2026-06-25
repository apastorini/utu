# Clase 28: Manejo Seguro de Errores y Excepciones

**Numero de clase:** 18
**Duracion:** 2 horas

## Objetivos de Aprendizaje

- Comprender como los errores mal manejados revelan informacion sensible
- Diferenciar entre errores de usuario (4xx) y errores de servidor (5xx)
- Implementar logging seguro que no exponga datos criticos
- Disenar middlewares de manejo de errores para aplicaciones web
- Escribir codigo que maneje excepciones sin filtrar internals

## Contenido Detallado

### 1. Por que los Errores Revelan Informacion

Un manejo inadecuado de errores puede exponer:
- Stack traces completos con rutas de archivos del servidor
- Consultas SQL y estructura de la base de datos
- Versiones de frameworks y librerias
- Nombres de usuarios internos del sistema
- Tokens de autenticacion y claves API
- Variables de entorno y configuracion del servidor

**Ejemplo de fuga de informacion:**
```
Traceback (most recent call last):
  File "C:\\app\\app.py", line 45, in login
    user = db.execute("SELECT * FROM users WHERE username = '%s'" % username)
  File "C:\\app\\database.py", line 120, in execute
    return self.conn.cursor().execute(query)
psycopg2.errors.UndefinedColumn: column "email" does not exist
LINE 1: SELECT * FROM users WHERE username = 'admin' ORDER BY email
```

### 2. Errores Personalizados vs. Genericos

**Errores de usuario (4xx):**
- 400 Bad Request: Datos invalidos enviados por el cliente
- 401 Unauthorized: Autenticacion requerida o fallida
- 403 Forbidden: El usuario no tiene permisos
- 404 Not Found: Recurso inexistente
- 422 Unprocessable Entity: Validacion de datos fallida

**Errores de servidor (5xx):**
- 500 Internal Server Error: Error generico del servidor
- 502 Bad Gateway: Error en proxy/gateway
- 503 Service Unavailable: Servicio temporalmente no disponible

### 3. Logging Seguro de Errores

**Que registrar:**
- ID unico de la transaccion (correlation ID)
- Timestamp
- Tipo de error y mensaje generico
- Usuario (sin datos sensibles)
- Endpoint y metodo HTTP
- Informacion de contexto no sensible

**Que NO registrar:**
- Contrasenas, tokens, API keys
- Datos de tarjetas de credito
- Informacion medica o personal sensible (PII)
- Stack traces completos en produccion
- Consultas SQL con parametros

### 4. Estrategias de Manejo de Excepciones

**Try-Except-Finally:**
```python
try:
    resultado = operacion_riesgosa()
except ValueError as e:
    logger.error("Error de validacion: %s", str(e))
    return {"error": "Dato invalido"}, 400
except DatabaseError as e:
    logger.critical("Error de base de datos: %s", str(e))
    return {"error": "Error interno del servidor"}, 500
finally:
    cerrar_recurso()
```

**No exponer internals:**
- Nunca devolver `repr(e)`, `traceback.format_exc()`, `str(e)` directamente al usuario
- Usar mensajes genericos amigables

## Ejercicio 1: App Flask con Stack Traces - Version Segura

```python
# app_segura.py - Manejo seguro de errores en Flask
import os
import logging
import traceback
import uuid
from datetime import datetime

from flask import Flask, request, jsonify, g

# ============================================================
# CONFIGURACION DE LOGGING
# ============================================================

LOG_DIR = 'logs'
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(correlation_id)s | %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(LOG_DIR, 'app.log')),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


# Filtro para agregar correlation ID a cada log
class CorrelationFilter(logging.Filter):
    def filter(self, record):
        record.correlation_id = getattr(g, 'correlation_id', 'N/A')
        return True


logger.addFilter(CorrelationFilter())

# ============================================================
# INICIALIZACION DE FLASK
# ============================================================

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = False

# ============================================================
# MIDDLEWARE: Correlation ID y Logging de Requests
# ============================================================

@app.before_request
def before_request():
    g.correlation_id = request.headers.get(
        'X-Correlation-ID',
        str(uuid.uuid4())[:8]
    )
    g.start_time = datetime.now()
    logger.info(
        "Request: %s %s",
        request.method,
        request.path
    )


@app.after_request
def after_request(response):
    duration = (datetime.now() - g.start_time).total_seconds()
    logger.info(
        "Response: %s %s -> %d (%.3fs)",
        request.method,
        request.path,
        response.status_code,
        duration
    )
    return response

# ============================================================
# MANEJADOR DE ERRORES PERSONALIZADO
# ============================================================

@app.errorhandler(400)
def bad_request(error):
    logger.warning("400: %s", str(error))
    return jsonify({
        'error': 'Solicitud incorrecta',
        'tipo': 'error_cliente',
        'correlation_id': g.get('correlation_id', 'N/A')
    }), 400


@app.errorhandler(401)
def unauthorized(error):
    logger.warning("401: Acceso no autorizado")
    return jsonify({
        'error': 'Autenticacion requerida',
        'tipo': 'error_cliente',
        'correlation_id': g.get('correlation_id', 'N/A')
    }), 401


@app.errorhandler(403)
def forbidden(error):
    logger.warning("403: Acceso denegado")
    return jsonify({
        'error': 'No tienes permisos para acceder a este recurso',
        'tipo': 'error_cliente',
        'correlation_id': g.get('correlation_id', 'N/A')
    }), 403


@app.errorhandler(404)
def not_found(error):
    logger.info("404: %s", request.path)
    return jsonify({
        'error': 'Recurso no encontrado',
        'tipo': 'error_cliente',
        'correlation_id': g.get('correlation_id', 'N/A')
    }), 404


@app.errorhandler(422)
def unprocessable(error):
    logger.warning("422: Datos no procesables")
    return jsonify({
        'error': 'Los datos enviados no son procesables',
        'tipo': 'error_cliente',
        'correlation_id': g.get('correlation_id', 'N/A')
    }), 422


@app.errorhandler(500)
def internal_error(error):
    """MANEJO SEGURO: No expone detalles internos al usuario."""
    correlation_id = g.get('correlation_id', 'N/A')
    trace = traceback.format_exc()

    # Log seguro: solo se registra internamente
    logger.critical(
        "Error interno: %s\nCorrelationID: %s\nTraceback:\n%s",
        str(error),
        correlation_id,
        trace
    )

    return jsonify({
        'error': 'Error interno del servidor',
        'tipo': 'error_servidor',
        'correlation_id': correlation_id,
        'mensaje': 'Ocurrio un error inesperado. Nuestro equipo ha sido notificado.'
    }), 500


@app.errorhandler(Exception)
def handle_unhandled(error):
    """Captura cualquier excepcion no manejada."""
    correlation_id = g.get('correlation_id', 'N/A')
    trace = traceback.format_exc()

    logger.critical(
        "Excepcion no manejada: %s\nCorrelationID: %s\nTraceback:\n%s",
        str(error),
        correlation_id,
        trace
    )

    return jsonify({
        'error': 'Error interno del servidor',
        'tipo': 'error_servidor',
        'correlation_id': correlation_id
    }), 500

# ============================================================
# ENDPOINTS
# ============================================================

# Base de datos simulada
USUARIOS = {
    1: {'nombre': 'Juan', 'email': 'juan@example.com'},
    2: {'nombre': 'Maria', 'email': 'maria@example.com'},
}


@app.route('/usuarios/<int:user_id>', methods=['GET'])
def obtener_usuario(user_id):
    """Endpoint que puede lanzar errores."""
    if user_id <= 0:
        return jsonify({'error': 'ID de usuario invalido'}), 400

    usuario = USUARIOS.get(user_id)
    if not usuario:
        return jsonify({'error': 'Usuario no encontrado'}), 404

    return jsonify(usuario)


@app.route('/login', methods=['POST'])
def login():
    """Login que maneja errores de autenticacion."""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'JSON requerido'}), 400

    username = data.get('username', '')
    password = data.get('password', '')

    if not username or not password:
        return jsonify({'error': 'Usuario y contrasena requeridos'}), 400

    if username == 'admin' and password == 'secreto':
        return jsonify({'token': 'token-simulado', 'usuario': username})
    else:
        return jsonify({'error': 'Credenciales invalidas'}), 401


@app.route('/dividir', methods=['GET'])
def dividir():
    """Endpoint que puede lanzar ZeroDivisionError."""
    try:
        a = float(request.args.get('a', 0))
        b = float(request.args.get('b', 0))
        resultado = a / b
        return jsonify({'resultado': resultado})
    except ZeroDivisionError:
        return jsonify({'error': 'No se puede dividir por cero'}), 400
    except (ValueError, TypeError) as e:
        logger.warning("Error de tipo en division: %s", str(e))
        return jsonify({'error': 'Parametos deben ser numeros'}), 400


@app.route('/error-simulado', methods=['GET'])
def error_simulado():
    """Simula un error interno del servidor."""
    try:
        resultado = 1 / 0  # Esto nunca se ejecutara
        return jsonify({'resultado': resultado})
    except Exception:
        raise RuntimeError("Error simulado para demostrar manejo seguro")


if __name__ == '__main__':
    print("=" * 60)
    print("App con manejo seguro de errores")
    print("Correlation IDs rastrean cada request")
    print("Logs en: logs/app.log")
    print("=" * 60)
    app.run(debug=False, port=5000)
```

**Pruebas:**
```bash
# Probar errores
curl http://localhost:5000/usuarios/999        # 404
curl http://localhost:5000/usuarios/0          # 400
curl http://localhost:5000/login -X POST -H "Content-Type: application/json" -d "{}"  # 400
curl http://localhost:5000/login -X POST -H "Content-Type: application/json" -d "{\"username\": \"admin\", \"password\": \"mala\"}"  # 401
curl http://localhost:5000/dividir?a=10&b=0    # 400
curl http://localhost:5000/error-simulado      # 500 seguro

# Ver logs
cat logs/app.log
```

## Ejercicio 2: Reescribir Manejador de Errores Vulnerable

```python
# manejador_vulnerable.py - VERSION VULNERABLE (NO USAR)
import traceback
from flask import Flask, request, jsonify

app_vulnerable = Flask(__name__)


@app_vulnerable.route('/usuario/<int:id>')
def obtener_usuario_vulnerable(id):
    try:
        # Simular busqueda en DB
        if id == 1:
            return jsonify({'nombre': 'Admin'})
        raise Exception(
            f"Error en consulta SQL: SELECT * FROM usuarios WHERE id = {id}"
        )
    except Exception as e:
        # MAL: Expone consulta SQL y stacktrace
        return jsonify({
            'error': f'Error: {str(e)}',
            'trace': traceback.format_exc(),
            'ruta': '/app/database.py:120',
            'conexion_db': 'postgresql://user:password@localhost:5432/prod'
        }), 500


# ============================================================
# VERSION CORREGIDA
# ============================================================

import logging
import os

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

app_segura = Flask(__name__)


class BaseDeDatosError(Exception):
    """Excepcion personalizada para errores de BD."""
    pass


@app_segura.route('/usuario/<int:id>')
def obtener_usuario_seguro(id):
    try:
        if id == 1:
            return jsonify({'nombre': 'Admin'})
        raise BaseDeDatosError("Usuario no encontrado en la base de datos")
    except BaseDeDatosError as e:
        logger.error("Error de BD al buscar usuario %d: %s", id, str(e))
        return jsonify({
            'error': 'No se pudo recuperar la informacion del usuario',
            'codigo': 'USUARIO_NO_ENCONTRADO'
        }), 404
    except Exception as e:
        logger.critical(
            "Error inesperado al buscar usuario %d: %s\n%s",
            id,
            str(e),
            traceback.format_exc()
        )
        return jsonify({
            'error': 'Error interno del servidor',
            'codigo': 'ERROR_INTERNO'
        }), 500
```

## Ejercicio 3: Middleware de Manejo de Errores para FastAPI con Logging Seguro

```python
# middleware_errores.py - Middleware de manejo de errores para FastAPI
import logging
import traceback
import uuid
from datetime import datetime
from typing import Callable

from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import json

# ============================================================
# CONFIGURACION DE LOGGING
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(name)s | %(correlation_id)s | %(message)s',
    handlers=[
        logging.FileHandler('logs/fastapi.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("fastapi_seguro")


class CorrelationFilter(logging.Filter):
    def filter(self, record):
        record.correlation_id = getattr(record, 'correlation_id', 'N/A')
        return True


logger.addFilter(CorrelationFilter())

# ============================================================
# MIDDLEWARE DE SEGURIDAD
# ============================================================

class ManejoErroresMiddleware(BaseHTTPMiddleware):
    """
    Middleware que:
    1. Asigna correlation ID a cada request
    2. Mide tiempos de respuesta
    3. Captura excepciones y las registra sin exponer internals
    4. Clasifica errores en 4xx (usuario) y 500 (servidor)
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        correlation_id = request.headers.get(
            'X-Correlation-ID',
            str(uuid.uuid4())[:8]
        )
        request.state.correlation_id = correlation_id
        start_time = datetime.now()

        try:
            response = await call_next(request)
            duration = (datetime.now() - start_time).total_seconds()

            logger.info(
                "Request: %s %s -> %d (%.3fs)",
                request.method,
                request.url.path,
                response.status_code,
                duration,
                extra={'correlation_id': correlation_id}
            )
            return response

        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds()
            trace = traceback.format_exc()

            # Clasificar el error
            status_code = self._clasificar_error(e)

            # Log seguro (interno)
            logger.critical(
                "Error: %s | Path: %s | Status: %d | Duracion: %.3fs\n%s",
                str(e),
                request.url.path,
                status_code,
                duration,
                trace,
                extra={'correlation_id': correlation_id}
            )

            # Respuesta segura (al usuario)
            return JSONResponse(
                status_code=status_code,
                content=self._respuesta_segura(
                    status_code,
                    correlation_id,
                    request.url.path
                )
            )

    def _clasificar_error(self, error: Exception) -> int:
        """Clasifica la excepcion en codigo HTTP apropiado."""
        error_name = type(error).__name__

        errores_400 = [
            'ValueError', 'TypeError', 'KeyError', 'IndexError',
            'ValidationError', 'AssertionError'
        ]
        errores_401 = ['AuthenticationError', 'PermissionDenied']
        errores_404 = ['NotFoundError', 'FileNotFoundError']
        errores_403 = ['AuthorizationError']

        if error_name in errores_401:
            return 401
        elif error_name in errores_404:
            return 404
        elif error_name in errores_403:
            return 403
        elif error_name in errores_400:
            return 400
        else:
            return 500

    def _respuesta_segura(
        self,
        status_code: int,
        correlation_id: str,
        path: str
    ) -> dict:
        """Genera respuesta segura sin exponer detalles internos."""
        respuestas = {
            400: {
                'error': 'Solicitud incorrecta',
                'mensaje': 'Los datos enviados no son validos'
            },
            401: {
                'error': 'No autorizado',
                'mensaje': 'Se requiere autenticacion'
            },
            403: {
                'error': 'Acceso denegado',
                'mensaje': 'No tienes permisos para este recurso'
            },
            404: {
                'error': 'No encontrado',
                'mensaje': 'El recurso solicitado no existe'
            },
            422: {
                'error': 'Datos no procesables',
                'mensaje': 'Los datos enviados no pueden ser procesados'
            }
        }

        base = respuestas.get(status_code, {
            'error': 'Error interno del servidor',
            'mensaje': 'Ocurrio un error inesperado. Nuestro equipo ha sido notificado.'
        })

        base['correlation_id'] = correlation_id
        base['tipo'] = 'error_cliente' if status_code < 500 else 'error_servidor'
        return base


# ============================================================
# MODELOS Y ENDPOINTS
# ============================================================

from pydantic import BaseModel, EmailStr

class UsuarioRequest(BaseModel):
    nombre: str
    email: EmailStr
    edad: int

app = FastAPI(title="API Segura")
app.add_middleware(ManejoErroresMiddleware)


@app.get("/")
def root():
    return {"mensaje": "API con manejo seguro de errores"}


@app.get("/usuarios/{user_id}")
def obtener_usuario(user_id: int):
    if user_id <= 0:
        raise ValueError("ID de usuario invalido")
    if user_id == 999:
        raise FileNotFoundError("Usuario no encontrado")
    return {"id": user_id, "nombre": "Usuario Ejemplo"}


@app.post("/usuarios")
def crear_usuario(usuario: UsuarioRequest):
    if usuario.edad < 0 or usuario.edad > 150:
        raise ValueError("Edad fuera de rango")
    return {"mensaje": "Usuario creado", "usuario": usuario}


@app.get("/error-500")
def error_500():
    """Simula un error interno."""
    raise RuntimeError("Error simulado interno")


@app.get("/error-401")
def error_401():
    raise PermissionError("Autenticacion fallida")


if __name__ == "__main__":
    import uvicorn
    print("API iniciada en http://localhost:8000")
    print("Documentacion en http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

**Pruebas con curl:**
```bash
curl http://localhost:8000/usuarios/1
curl http://localhost:8000/usuarios/999
curl http://localhost:8000/usuarios/-1
curl http://localhost:8000/error-500
curl http://localhost:8000/error-401
```

## Preguntas y Respuestas

**P1: Por que los stack traces son peligrosos si se muestran al usuario?**
R: Los stack traces revelan rutas absolutas del servidor (C:\\app\\src\\...), versiones de librerias, nombres de archivos, estructura del proyecto, consultas SQL, y a veces datos de configuracion. Un atacante usa esta informacion para identificar vulnerabilidades especificas del entorno.

**P2: Que informacion se debe incluir en un log de error y cual se debe excluir?**
R: Incluir: timestamp, correlation ID, endpoint, metodo HTTP, tipo de error, nombre de usuario (sin datos sensibles). Excluir: contrasenas, tokens, API keys, numeros de tarjeta, informacion medica, datos biometricos, y cualquier PII (Personally Identifiable Information).

**P3: Cual es la diferencia entre errores 4xx y 5xx?**
R: 4xx (Error de Cliente): El problema esta en la solicitud del cliente (400 Bad Request, 401 Unauthorized, 404 Not Found). 5xx (Error de Servidor): El servidor fallo al procesar una solicitud valida (500 Internal Server Error, 502 Bad Gateway). Los 4xx pueden dar mensajes detallados al usuario; los 5xx deben ser genericos.

**P4: Como se implementa un correlation ID y para que sirve?**
R: Un correlation ID es un identificador unico generado por request (generalmente UUID). Se asigna al inicio de cada solicitud HTTP y se propaga a traves de todos los sistemas involucrados (APIs, bases de datos, logs). Sirve para correlacionar logs de diferentes componentes y facilitar la depuracion.

**P5: Que es el principio de "fail securely" y como se aplica al manejo de errores?**
R: "Fail securely" significa que cuando ocurre un error, el sistema debe fallar a un estado seguro por defecto, no a un estado que exponga informacion o conceda acceso. En manejo de errores: capturar excepciones, registrar el error internamente, y mostrar un mensaje generico al usuario sin revelar detalles tecnicos.

**P6: Cual es la diferencia entre usar `raise` y retornar un codigo de error?**
R: `raise` interrumpe el flujo normal y propaga la excepcion hacia arriba en la pila de llamadas, permitiendo que un manejador centralizado la capture. Retornar un codigo de error requiere que cada llamador verifique manualmente el resultado, lo que es propenso a errores. Para APIs web, es mejor usar excepciones con un middleware centralizado.

**P7: Por que no se debe usar `debug=True` en produccion en Flask?**
R: `debug=True` activa el depurador interactivo de Werkzeug que muestra stack traces completos en el navegador y permite ejecutar codigo Python arbitrario en el servidor. Esto expone informacion critica y representa un riesgo de seguridad severo.

## Tarea / Lectura Recomendada

1. **OWASP Error Handling Cheat Sheet:**
   https://cheatsheetseries.owasp.org/cheatsheets/Error_Handling_Cheat_Sheet.html

2. **OWASP Logging Cheat Sheet:**
   https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html

3. **Documentacion de manejo de errores en FastAPI:**
   https://fastapi.tiangolo.com/tutorial/handling-errors/

4. **Tarea practica:** Agregar al middleware de FastAPI un sistema de notificaciones (Slack/email) que alerte al equipo cuando ocurran errores 500.

5. **Tarea practica:** Crear un decorador Python `@manejar_errores_seguro` que envuelva cualquier funcion y maneje sus excepciones de forma segura, con logging automatico.


