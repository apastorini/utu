# Clase 35: DAST - Dynamic Application Security Testing

**Numero de clase:** 24
**Duracion:** 2 horas

## Objetivos de Aprendizaje

- Comprender que es DAST y como funciona (analisis desde afuera, black-box)
- Usar OWASP ZAP para escanear aplicaciones web vulnerables
- Diferenciar entre DAST autenticado y no autenticado
- Interpretar reportes DAST y clasificar hallazgos por severidad
- Automatizar escaneos DAST via API de ZAP desde Python

## Contenido Detallado

### 1. Que es DAST?

DAST (Dynamic Application Security Testing) analiza una aplicacion en ejecucion desde la perspectiva de un atacante externo. No tiene acceso al codigo fuente (black-box testing).

**Caracteristicas:**
- Black-box: no conoce el codigo fuente interno
- Prueba la aplicacion en su estado real (en produccion o staging)
- Detecta vulnerabilidades en tiempo de ejecucion
- Simula ataques reales contra la aplicacion

**Lo que detecta:**
- Cross-Site Scripting (XSS) reflejado y almacenado
- Inyeccion SQL
- Command Injection
- Path Traversal
- Server-Side Request Forgery (SSRF)
- Cross-Site Request Forgery (CSRF)
- Problemas de configuracion (headers inseguros, TLS debil)
- Exposicion de informacion sensible

### 2. Herramientas DAST

| Herramienta | Tipo | Licencia | Caracteristicas |
|-------------|------|----------|-----------------|
| OWASP ZAP | Proxy + Scanner | Open Source | La mas popular, API completa, plugins |
| Burp Suite | Proxy + Scanner | Community/Pro | La mas usada en pentesting profesional |
| Nikto | Scanner web | Open Source | Rapido, detecta configuracion insegura |
| w3af | Framework | Open Source | Modular, extensible |
| Acunetix | Scanner | Comercial | Cobertura amplia, bajo FP |
| Netsparker | Scanner | Comercial | Confirmacion automatica de vulnerabilidades |

### 3. DAST vs SAST

| Aspecto | SAST | DAST |
|---------|------|------|
| Perspectiva | White-box (ve el codigo) | Black-box (ve desde afuera) |
| Momento | Build / Commit | Testing / Staging / Produccion |
| Acceso | Codigo fuente | URL de la app |
| Falsos positivos | Altos | Medios |
| Cobertura | Lineas de codigo | Endpoints y funcionalidades |
| Detecta | Bugs de codigo | Bugs de ejecucion y configuracion |
| Integracion | CI/CD temprano | CI/CD tardio (staging) |

### 4. Tipos de Escaneo DAST

**Autenticado vs. No Autenticado:**
- **No autenticado:** Escanea solo lo accesible sin login. Menor cobertura.
- **Autenticado:** Escanea areas que requieren sesion de usuario. Mayor cobertura.

**Crawling vs Scanning:**
- **Crawling:** Navega la aplicacion descubriendo endpoints y formularios.
- **Scanning:** Ejecuta ataques contra los endpoints descubiertos.

### 5. Limitaciones de DAST

- **Cobertura limitada:** Solo prueba funcionalidades accesibles via HTTP
- **Falsos positivos:** Algunos ataques pueden no ser aplicables al contexto
- **Lentitud:** Escaneos profundos pueden tomar horas
- **No ve codigo:** No puede detectar vulnerabilidades que no se reflejan en la respuesta HTTP
- **Requiere app funcional:** No sirve en etapas tempranas del desarrollo

## Ejercicio 1: Instalar OWASP ZAP y Escanear App Vulnerable Local

```bash
# ============================================================
# INSTALACION DE OWASP ZAP (Docker)
# ============================================================

# Opcion 1: Usar Docker (recomendado)
docker pull ghcr.io/zaproxy/zaproxy:stable

# Iniciar ZAP en modo daemon (escucha en puerto 8080)
docker run -d \
  --name zap \
  -p 8080:8080 \
  -v zap-data:/home/zap/.ZAP \
  ghcr.io/zaproxy/zaproxy:stable \
  zap.sh -daemon -host 0.0.0.0 -port 8080 -config api.key=changeme

# Opcion 2: Instalar ZAP Desktop
# Descargar de: https://www.zaproxy.org/download/
# Ejecutar el instalador

# ============================================================
# APP VULNERABLE LOCAL (DVWA simplificada en Flask)
# ============================================================
```

```python
# app_vulnerable_dast.py - App vulnerable para escaneo DAST
from flask import Flask, request, render_template_string, jsonify
import sqlite3
import subprocess
import os

app = Flask(__name__)

# Inicializar BD
def init_db():
    conn = sqlite3.connect(':memory:')
    conn.execute('''CREATE TABLE usuarios
                    (id INTEGER PRIMARY KEY,
                     username TEXT,
                     password TEXT,
                     email TEXT)''')
    conn.execute("INSERT INTO usuarios VALUES (1, 'admin', 'flag{un3z4k0}', 'admin@test.com')")
    conn.execute("INSERT INTO usuarios VALUES (2, 'user', 'password123', 'user@test.com')")
    conn.commit()
    return conn

db = init_db()


@app.route('/')
def index():
    return '''
    <h1>App Vulnerable para DAST</h1>
    <ul>
        <li><a href="/sqli?user=admin">SQL Injection</a></li>
        <li><a href="/xss?name=test">XSS Reflejado</a></li>
        <li><a href="/command?ip=127.0.0.1">Command Injection</a></li>
        <li><a href="/path?file=test.txt">Path Traversal</a></li>
        <li><a href="/headers">Ver Headers de Seguridad</a></li>
        <li><a href="/form">Formulario Vulnerable</a></li>
    </ul>
    <p>Bandera escondida: <!-- flag{3st0_n0_s3_v3} --></p>
    '''


# ============================================================
# VULNERABILIDAD 1: SQL Injection
# ============================================================
@app.route('/sqli')
def sql_injection():
    user = request.args.get('user', '')
    query = f"SELECT * FROM usuarios WHERE username = '{user}'"

    try:
        cursor = db.execute(query)
        results = cursor.fetchall()
        return f'''
        <h2>SQL Injection</h2>
        <p>Query: {query}</p>
        <p>Resultados: {results}</p>
        <form><input name="user" placeholder="Username"><button>Buscar</button></form>
        '''
    except Exception as e:
        return f'<p>Error: {str(e)}</p>'


# ============================================================
# VULNERABILIDAD 2: XSS Reflejado
# ============================================================
@app.route('/xss')
def xss_reflejado():
    name = request.args.get('name', 'Invitado')
    return f'''
    <h2>XSS Reflejado</h2>
    <p>Hola, {name}!</p>
    <form><input name="name" placeholder="Tu nombre"><button>Saludar</button></form>
    '''


# ============================================================
# VULNERABILIDAD 3: Command Injection
# ============================================================
@app.route('/command')
def command_injection():
    ip = request.args.get('ip', '127.0.0.1')
    try:
        result = subprocess.check_output(f'ping -n 1 {ip}', shell=True, timeout=5)
        return f'<pre>{result.decode()}</pre>'
    except Exception as e:
        return f'<p>Error: {str(e)}</p>'


# ============================================================
# VULNERABILIDAD 4: Path Traversal
# ============================================================
@app.route('/path')
def path_traversal():
    file = request.args.get('file', '')
    try:
        with open(file, 'r') as f:
            content = f.read()
        return f'<pre>{content}</pre>'
    except Exception as e:
        return f'<p>Error: {str(e)}</p>'


# ============================================================
# VULNERABILIDAD 5: Headers de seguridad faltantes
# ============================================================
@app.route('/headers')
def headers():
    return jsonify({
        'mensaje': 'Faltan headers de seguridad',
        'x-frame-options': 'NO PRESENTE',
        'x-content-type-options': 'NO PRESENTE',
        'strict-transport-security': 'NO PRESENTE',
        'content-security-policy': 'NO PRESENTE'
    })


# ============================================================
# VULNERABILIDAD 6: Formulario sin CSRF
# ============================================================
@app.route('/form', methods=['GET', 'POST'])
def formulario():
    if request.method == 'POST':
        nombre = request.form.get('nombre', '')
        comentario = request.form.get('comentario', '')
        return f'<p>Gracias {nombre}. Comentario recibido: {comentario}</p>'
    return '''
    <h2>Formulario sin CSRF</h2>
    <form method="POST">
        <input name="nombre" placeholder="Nombre"><br>
        <textarea name="comentario" placeholder="Comentario"></textarea><br>
        <button>Enviar</button>
    </form>
    '''


# ============================================================
# VULNERABILIDAD 7: Informacion expuesta
# ============================================================
@app.route('/robots.txt')
def robots():
    return '''User-agent: *
Disallow: /admin
Disallow: /config
Disallow: /backup.sql
'''


@app.route('/admin')
def admin():
    return '<h1>Panel de Administracion</h1><p>Usuario: root</p>'


@app.route('/config')
def config():
    return jsonify({
        'db_host': 'localhost',
        'db_name': 'prod_db',
        'db_user': 'root',
        'app_version': '1.0.0-beta',
        'secret_key': 'super-secret-key-12345'
    })


@app.route('/backup.sql')
def backup_db():
    return '''-- Backup de base de datos
CREATE TABLE usuarios (
    id INT PRIMARY KEY,
    username VARCHAR(50),
    password VARCHAR(50),  -- Texto plano!
    email VARCHAR(100)
);
INSERT INTO usuarios VALUES (1, 'admin', 'supersecret', 'admin@example.com');
INSERT INTO usuarios VALUES (2, 'developer', 'devpass123', 'dev@example.com');
'''


if __name__ == '__main__':
    print("=" * 60)
    print("App Vulnerable para escaneo DAST")
    print("Escuchando en: http://localhost:5000")
    print("=" * 60)
    app.run(debug=True, port=5000)
```

**Comandos de escaneo con ZAP:**
```bash
# ============================================================
# ESCANEO CON OWASP ZAP
# ============================================================

# 1. Iniciar la app vulnerable
python app_vulnerable_dast.py

# 2. Escaneo pasivo (solo navega, no ataca)
curl "http://localhost:8080/JSON/pscan/action/enableAllScanners/?apikey=changeme"

# 3. Escaneo activo completo desde linea de comandos
docker run -t ghcr.io/zaproxy/zaproxy:stable \
  zap-full-scan.py \
  -t http://host.docker.internal:5000 \
  -r zap-report.html \
  -x zap-report.xml \
  -m 5 \
  -d

# 4. Escaneo AJAX (para SPAs)
docker run -t ghcr.io/zaproxy/zaproxy:stable \
  zap-ajax-scan.py \
  -t http://host.docker.internal:5000 \
  -r zap-ajax-report.html

# 5. Escaneo con autenticacion
docker run -t ghcr.io/zaproxy/zaproxy:stable \
  zap-full-scan.py \
  -t http://host.docker.internal:5000 \
  -r zap-auth-report.html \
  -U "admin" \
  -P "flag{un3z4k0}"

# 6. Escaneo API (para APIs REST)
docker run -t ghcr.io/zaproxy/zaproxy:stable \
  zap-api-scan.py \
  -t http://host.docker.internal:5000/openapi.json \
  -f openapi \
  -r zap-api-report.html
```

**Interpretacion de resultados:**
```
REPORTE ZAP - HALLZAGOS PRINCIPALES

Alto riesgo:
- SQL Injection (/sqli): Severidad ALTA
  Descripcion: La aplicacion permite inyeccion SQL concatenando
  parametros directamente en la consulta.
  Parametro: user
  Payload: admin' OR '1'='1
  URL: http://localhost:5000/sqli?user=admin' OR '1'='1
  Evidencia: La query devuelve todos los registros de usuarios

- Cross-Site Scripting (XSS) Reflejado (/xss): Severidad ALTA
  Descripcion: El parametro name se refleja sin escapar en HTML.
  Parametro: name
  Payload: <script>alert(1)</script>
  URL: http://localhost:5000/xss?name=<script>alert(1)</script>
  Evidencia: El script se ejecuta en el navegador

- Command Injection (/command): Severidad ALTA
  Descripcion: El parametro ip se pasa a shell=True sin sanitizar.
  Parametro: ip
  Payload: 127.0.0.1 & dir
  URL: http://localhost:5000/command?ip=127.0.0.1%20%26%20dir
  Evidencia: Se ejecuta el comando 'dir'

Medio riesgo:
- Path Traversal (/path): Severidad MEDIA
  Descripcion: El parametro file permite leer archivos fuera del directorio.
  Payload: ../../../etc/passwd
  URL: http://localhost:5000/path?file=../../../etc/passwd
  Evidencia: Contenido del archivo /etc/passwd

- Information Disclosure (/admin, /config, /backup.sql): Severidad MEDIA
  Descripcion: Directorios y archivos sensibles expuestos publicamente.
  Evidencia: /config expone configuracion de BD y secret key.

- Missing Security Headers: Severidad MEDIA
  Headers faltantes:
  - X-Frame-Options (protege contra clickjacking)
  - X-Content-Type-Options (protege contra MIME sniffing)
  - Strict-Transport-Security (fuerza HTTPS)
  - Content-Security-Policy (protege contra XSS)

- X-Frame-Options Header Missing: Severidad MEDIA
  Descripcion: La pagina puede ser cargada en un iframe,
  permitiendo clickjacking.

Bajo riesgo:
- Cookies sin Secure/HttpOnly flag: Severidad BAJA
  Descripcion: Las cookies de sesion no tienen flags de seguridad.
- Server Version Disclosure: Severidad BAJA
  Descripcion: El header Server revela la version del servidor web.
- Informative: robots.txt expone paths sensibles.
```

## Ejercicio 2: ZAP API desde Python para Escaneo Automatizado

```python
# zap_automation.py - Escaneo automatizado con API de OWASP ZAP
import time
import json
import logging
from typing import Optional, Dict, List
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ZAPAutomation:
    """
    Automatizacion de escaneo DAST usando la API REST de OWASP ZAP.
    ZAP debe estar corriendo en modo daemon (-daemon).
    """

    def __init__(
        self,
        zap_url: str = "http://localhost:8080",
        api_key: str = "changeme"
    ):
        self.zap_url = zap_url.rstrip('/')
        self.api_key = api_key
        self.api_base = f"{self.zap_url}/JSON"
        self.session = requests.Session()
        self.context_id: Optional[int] = None

    def _api_request(self, endpoint: str, params: dict = None) -> dict:
        """Realiza una request a la API de ZAP."""
        if params is None:
            params = {}
        params['apikey'] = self.api_key

        url = f"{self.api_base}/{endpoint}"
        response = self.session.get(url, params=params, timeout=30)

        if response.status_code != 200:
            raise RuntimeError(
                f"Error API ZAP ({response.status_code}): {response.text}"
            )
        return response.json()

    # ==========================================
    # METODOS DE CONFIGURACION
    # ==========================================

    def crear_contexto(self, nombre: str) -> int:
        """
        Crea un contexto en ZAP para aislar el escaneo.

        El contexto define los limites del escaneo: URLs incluidas,
        autenticacion, etc.
        """
        result = self._api_request(
            'context/action/newContext/',
            {'contextName': nombre}
        )
        self.context_id = result.get('contextId')

        if self.context_id:
            logger.info("Contexto creado: %s (ID: %s)", nombre, self.context_id)
        return self.context_id

    def incluir_en_contexto(self, url_pattern: str):
        """Incluye URLs que coinciden con el patron en el contexto."""
        if not self.context_id:
            raise RuntimeError("Debes crear un contexto primero")

        self._api_request('context/action/includeInContext/', {
            'contextName': f'Context{self.context_id}',
            'regex': url_pattern
        })
        logger.info("Patron incluido en contexto: %s", url_pattern)

    def configurar_autenticacion(
        self,
        login_url: str,
        user_field: str,
        password_field: str,
        username: str,
        password: str
    ):
        """
        Configura autenticacion basada en formulario.
        Permite escanear areas que requieren login.
        """
        if not self.context_id:
            raise RuntimeError("Debes crear un contexto primero")

        # Configurar indicador de sesion (lo que aparece cuando hay sesion)
        session_indicator_method = 'response'
        session_indicator_param = 'logout'

        self._api_request('authentication/action/setAuthenticationMethod/', {
            'contextId': self.context_id,
            'authMethodName': 'formBasedAuthentication',
            'authMethodConfigParams': (
                f'loginUrl={login_url}&'
                f'loginRequestData={user_field}%3D%7B%25username%25%7D'
                f'%26{password_field}%3D%7B%25password%25%7D'
            )
        })

        # Configurar credenciales del usuario
        self._api_request('users/action/newUser/', {
            'contextId': self.context_id,
            'name': 'test-user'
        })

        self._api_request('users/action/setAuthenticationCredentials/', {
            'contextId': self.context_id,
            'userId': 0,
            'username': username,
            'password': password
        })

        logger.info("Autenticacion configurada para: %s", login_url)

    # ==========================================
    # METODOS DE ESCANEO
    # ==========================================

    def abrir_url(self, url: str) -> bool:
        """
        Abre una URL en ZAP para que sea explorada (spidered).
        ZAP seguira enlaces y descubrira endpoints.
        """
        result = self._api_request('core/action/accessUrl/', {
            'url': url,
            'followRedirects': True
        })
        logger.info("URL abierta: %s", url)
        return result.get('Result', '').startswith('OK')

    def spider_scan(self, url: str, max_children: int = 10) -> int:
        """
        Ejecuta spider scan para descubrir endpoints.

        Returns:
            ID del scan (para monitorear progreso)
        """
        result = self._api_request('spider/action/scan/', {
            'url': url,
            'maxChildren': max_children,
            'contextId': self.context_id or ''
        })
        scan_id = result.get('scanId')

        if scan_id:
            logger.info("Spider scan iniciado ID: %s para URL: %s", scan_id, url)
        return scan_id

    def active_scan(self, url: str) -> int:
        """
        Ejecuta escaneo activo contra la URL.
        Este es el escaneo que realmente ejecuta ataques.

        Returns:
            ID del scan (para monitorear progreso)
        """
        result = self._api_request('ascan/action/scan/', {
            'url': url,
            'recurse': True,
            'inScopeOnly': True if self.context_id else False,
            'scanPolicyName': ''
        })
        scan_id = result.get('scan')

        if scan_id:
            logger.info("Active scan iniciado ID: %s para URL: %s", scan_id, url)
        return scan_id

    # ==========================================
    # METODOS DE MONITOREO
    # ==========================================

    def esperar_spider(self, scan_id: int, timeout: int = 300):
        """Espera a que el spider scan termine."""
        inicio = time.time()
        while True:
            result = self._api_request('spider/view/status/', {
                'scanId': scan_id
            })
            status = int(result.get('status', 0))
            logger.info("Spider progress: %d%%", status)

            if status >= 100:
                logger.info("Spider scan completado")
                return True

            if time.time() - inicio > timeout:
                raise TimeoutError("Spider scan excedio el tiempo limite")
            time.sleep(5)

    def esperar_active_scan(self, scan_id: int, timeout: int = 600):
        """Espera a que el active scan termine."""
        inicio = time.time()
        while True:
            result = self._api_request('ascan/view/status/', {
                'scanId': scan_id
            })
            status = int(result.get('status', 0))
            logger.info("Active scan progress: %d%%", status)

            if status >= 100:
                logger.info("Active scan completado")
                return True

            if time.time() - inicio > timeout:
                raise TimeoutError("Active scan excedio el tiempo limite")
            time.sleep(5)

    # ==========================================
    # METODOS DE REPORTES
    # ==========================================

    def obtener_alertas(self, risk_level: str = None) -> List[Dict]:
        """
        Obtiene todas las alertas generadas por el escaneo.

        Args:
            risk_level: Filtrar por nivel de riesgo
                        (High, Medium, Low, Informational)

        Returns:
            Lista de alertas con: nombre, riesgo, url, descripcion, solucion
        """
        params = {}
        if risk_level:
            params['riskId'] = {'High': '3', 'Medium': '2',
                                'Low': '1', 'Informational': '0'}.get(risk_level, '')

        result = self._api_request('core/view/alerts/', params)
        return result.get('alerts', [])

    def generar_reporte_html(self) -> str:
        """Genera reporte HTML completo."""
        url = f"{self.zap_url}/OTHER/core/other/htmlreport/"
        params = {'apikey': self.api_key}

        response = self.session.get(url, params=params, timeout=30)
        if response.status_code == 200:
            return response.text
        raise RuntimeError("Error al generar reporte HTML")

    def clasificar_alertas(self) -> Dict:
        """Clasifica alertas por severidad."""
        alertas = self.obtener_alertas()
        clasificacion = {'High': [], 'Medium': [], 'Low': [], 'Informational': []}

        for alerta in alertas:
            riesgo = alerta.get('risk', 'Informational')
            if riesgo in clasificacion:
                clasificacion[riesgo].append(alerta)
            else:
                clasificacion['Informational'].append(alerta)

        return clasificacion


# ============================================================
# EJECUCION COMPLETA DEL ESCANEO AUTOMATIZADO
# ============================================================
if __name__ == '__main__':
    print("=" * 60)
    print("ESCANEO DAST AUTOMATIZADO CON OWASP ZAP")
    print("=" * 60)

    # Verificar que ZAP este corriendo
    TARGET_URL = 'http://host.docker.internal:5000'
    ZAP_URL = 'http://localhost:8080'
    API_KEY = 'changeme'

    try:
        zap = ZAPAutomation(ZAP_URL, API_KEY)

        # 1. Probar conexion con ZAP
        logger.info("1. Verificando conexion con ZAP...")
        version = zap._api_request('core/view/version/')
        logger.info("   ZAP Version: %s", version.get('version', 'desconocida'))

        # 2. Crear contexto
        logger.info("\n2. Creando contexto de escaneo...")
        zap.crear_contexto('Escaneo-DAST-Clase24')
        zap.incluir_en_contexto(f'{TARGET_URL}.*')

        # 3. Abrir URL objetivo
        logger.info("\n3. Abriendo URL objetivo...")
        zap.abrir_url(TARGET_URL)

        # 4. Spider Scan (descubrimiento)
        logger.info("\n4. Ejecutando Spider Scan...")
        spider_id = zap.spider_scan(TARGET_URL, max_children=10)
        if spider_id:
            zap.esperar_spider(spider_id, timeout=120)

        # 5. Active Scan (ataques)
        logger.info("\n5. Ejecutando Active Scan...")
        scan_id = zap.active_scan(TARGET_URL)
        if scan_id:
            zap.esperar_active_scan(scan_id, timeout=300)

        # 6. Obtener y clasificar resultados
        logger.info("\n6. Obteniendo resultados...")
        clasificacion = zap.clasificar_alertas()

        print("\n" + "=" * 60)
        print("RESULTADOS DEL ESCANEO DAST")
        print("=" * 60)

        print(f"\nHIGH: {len(clasificacion['High'])}")
        for a in clasificacion['High']:
            print(f"  - {a.get('alert', 'N/A')}")
            print(f"    URL: {a.get('url', 'N/A')}")

        print(f"\nMEDIUM: {len(clasificacion['Medium'])}")
        for a in clasificacion['Medium']:
            print(f"  - {a.get('alert', 'N/A')}")
            print(f"    URL: {a.get('url', 'N/A')}")

        print(f"\nLOW: {len(clasificacion['Low'])}")
        print(f"INFORMATIONAL: {len(clasificacion['Informational'])}")

        # 7. Generar reporte HTML
        logger.info("\n7. Generando reporte HTML...")
        reporte_html = zap.generar_reporte_html()
        with open('zap-dast-report.html', 'w') as f:
            f.write(reporte_html)
        logger.info("   Reporte guardado: zap-dast-report.html")

    except requests.exceptions.ConnectionError:
        logger.error(
            "No se pudo conectar a ZAP en %s.\n"
            "Asegurate de que ZAP este corriendo en modo daemon:\n"
            "  docker run -d --name zap -p 8080:8080 "
            "ghcr.io/zaproxy/zaproxy:stable "
            "zap.sh -daemon -port 8080 -config api.key=changeme",
            ZAP_URL
        )
    except Exception as e:
        logger.error("Error durante el escaneo: %s", str(e))
```

## Ejercicio 3: Clasificar Reporte DAST con 10 Hallazgos y Proponer Correcciones

```python
# analisis_reporte_dast.py - Clasificar y corregir hallazgos DAST
import json


class ReporteDAST:
    """
    Procesa un reporte DAST (OWASP ZAP) y clasifica los hallazgos
    por severidad con acciones de correccion sugeridas.
    """

    CORRECCIONES = {
        'SQL Injection': {
            'severidad': 'Alta',
            'cwe': 'CWE-89',
            'correccion': """
CORRECCION SQL INJECTION:
1. Usar consultas parametrizadas (prepared statements):
   cursor.execute("SELECT * FROM usuarios WHERE username = ?", (user,))

2. Usar un ORM (SQLAlchemy, Django ORM) que maneje parametrizacion
   automaticamente.

3. Validar que los inputs solo contengan caracteres esperados
   (whitelist de caracteres permitidos).

4. Aplicar el principio de minimo privilegio en la cuenta de BD.
"""
        },
        'Cross-Site Scripting (XSS)': {
            'severidad': 'Alta',
            'cwe': 'CWE-79',
            'correccion': """
CORRECCION XSS:
1. Escapar toda salida HTML con html.escape() en Python o
   autoescaping de Jinja2/Flask.

2. Implementar Content-Security-Policy (CSP) header:
   Content-Security-Policy: default-src 'self'

3. No insertar datos del usuario directamente en HTML sin escapar.

4. Usar plantillas con autoescaping (Jinja2, React con JSX).
"""
        },
        'Command Injection': {
            'severidad': 'Alta',
            'cwe': 'CWE-78',
            'correccion': """
CORRECCION COMMAND INJECTION:
1. NUNCA usar shell=True en subprocess con datos del usuario.

2. Usar subprocess con lista de argumentos (sin shell=True):
   subprocess.check_output(['ping', '-n', '1', ip])

3. Validar el formato del input antes de usarlo:
   import ipaddress
   ipaddress.ip_address(ip)  # Lanza error si no es IP valida

4. Preferir librerias Python nativas en lugar de comandos del sistema.
"""
        },
        'Path Traversal': {
            'severidad': 'Media',
            'cwe': 'CWE-22',
            'correccion': """
CORRECCION PATH TRAVERSAL:
1. Normalizar y validar la ruta antes de acceder al archivo:
   ruta = os.path.normpath(os.path.join(BASE_DIR, nombre))
   if not ruta.startswith(BASE_DIR):
       raise PermissionError("Acceso denegado")

2. Mantener un directorio base restringido para archivos.

3. No permitir ".." en los nombres de archivo.

4. Usar indentificadores numericos en lugar de nombres de archivo.
"""
        },
        'Information Disclosure': {
            'severidad': 'Media',
            'cwe': 'CWE-200',
            'correccion': """
CORRECCION INFORMATION DISCLOSURE:
1. No exponer rutas /admin, /config, /backup.sql publicamente.

2. Implementar autenticacion y autorizacion en todas las rutas
   administrativas.

3. No incluir comentarios HTML con informacion sensible.

4. Configurar el servidor para no revelar versiones:
   - Deshabilitar Server header
   - No mostrar stack traces en produccion
   - No incluir versiones en headers HTTP
"""
        },
        'Missing Security Headers': {
            'severidad': 'Media',
            'cwe': 'CWE-693',
            'correccion': """
CORRECCION HEADERS DE SEGURIDAD:
Agregar los siguientes headers en todas las respuestas:

1. X-Frame-Options: DENY
   (Protege contra clickjacking)

2. X-Content-Type-Options: nosniff
   (Protege contra MIME sniffing)

3. Strict-Transport-Security: max-age=31536000; includeSubDomains
   (Fuerza HTTPS)

4. Content-Security-Policy: default-src 'self'
   (Protege contra XSS y data injection)

5. X-XSS-Protection: 0
   (Deshabilitar modo legacy de XSS filter)

6. Referrer-Policy: strict-origin-when-cross-origin
   (Controla informacion enviada en Referer)

En Flask:
    @app.after_request
    def add_security_headers(response):
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['Strict-Transport-Security'] = \
            'max-age=31536000; includeSubDomains'
        response.headers['Content-Security-Policy'] = \
            "default-src 'self'"
        return response
"""
        },
        'CSRF (Cross-Site Request Forgery)': {
            'severidad': 'Media',
            'cwe': 'CWE-352',
            'correccion': """
CORRECCION CSRF:
1. Usar tokens CSRF en todos los formularios:
   Flask-WTF: {{ form.hidden_tag() }}

2. Validar el origen de las requests:
   - Verificar header Origin o Referer
   - Usar SameSite cookie attribute: SameSite=Lax

3. Para APIs: usar tokens en headers personalizados
   (X-CSRF-Token) en lugar de cookies.

4. No aceptar requests POST sin token CSRF valido.
"""
        },
        'Weak Password Policy': {
            'severidad': 'Media',
            'cwe': 'CWE-521',
            'correccion': """
CORRECCION POLITICA DE CONTRASENAS:
1. Implementar requisitos minimos de contrasena:
   - Minimo 8 caracteres
   - Al menos 1 mayuscula, 1 minuscula, 1 numero, 1 especial

2. Usar hash seguro (bcrypt/argon2) para almacenar contrasenas.

3. No almacenar contrasenas en texto plano en BD o backups.

4. Implementar rate limiting en login para prevenir fuerza bruta.
"""
        },
        'SSL/TLS Weak Configuration': {
            'severidad': 'Media',
            'cwe': 'CWE-327',
            'correccion': """
CORRECCION TLS:
1. Usar TLS 1.2 o 1.3 exclusivamente (deshabilitar TLS 1.0/1.1).

2. Usar certificados validos de una CA confiable.

3. Configurar ciphers seguros:
   ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-GCM-SHA256

4. Habilitar HSTS (HTTP Strict Transport Security) con
   preload si es posible.

5. Redirigir todo trafico HTTP a HTTPS automaticamente.
"""
        },
        'Cookie Without Secure/HttpOnly': {
            'severidad': 'Baja',
            'cwe': 'CWE-614',
            'correccion': """
CORRECCION SEGURIDAD DE COOKIES:
1. Agregar Secure flag: la cookie solo se envia por HTTPS.
2. Agregar HttpOnly flag: la cookie no es accesible via JavaScript.
3. Agregar SameSite flag: SameSite=Lax o Strict.
4. Configurar Path y Domain especificos.

En Flask:
    app.config.update(
        SESSION_COOKIE_SECURE=True,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE='Lax',
        SESSION_COOKIE_PATH='/'
    )
"""
        }
    }

    def __init__(self, reporte: dict):
        self.reporte = reporte

    def clasificar_por_severidad(self) -> dict:
        """Clasifica hallazgos por severidad."""
        alertas = self.reporte.get('alerts', [])

        clasificacion = {'Alta': [], 'Media': [], 'Baja': [], 'Info': []}
        for alerta in alertas:
            severidad = alerta.get('risk', 'Info')
            clasificacion[severidad].append(alerta)

        return clasificacion

    def generar_plan_accion(self) -> list:
        """Genera plan de accion priorizado."""
        alertas = self.reporte.get('alerts', [])
        plan = []

        for alerta in alertas:
            nombre = alerta.get('alert', 'Desconocido')
            riesgo = alerta.get('risk', 'Info')
            url = alerta.get('url', 'N/A')
            descripcion = alerta.get('description', 'Sin descripcion')

            correccion = self.CORRECCIONES.get(nombre, {}).get(
                'correccion',
                'No hay correccion predefinida. Revisar manualmente.'
            )

            plan.append({
                'vulnerabilidad': nombre,
                'severidad': riesgo,
                'url': url,
                'descripcion': descripcion[:100],
                'correccion': correccion.strip()
            })

        prioridad = {'Alta': 0, 'Media': 1, 'Baja': 2, 'Info': 3}
        plan.sort(key=lambda x: prioridad.get(x['severidad'], 99))
        return plan


# ============================================================
# EJEMPLO DE REPORTE CON 10 HALLAZGOS
# ============================================================

reporte_ejemplo = {
    "alerts": [
        {
            "alert": "SQL Injection",
            "risk": "Alta",
            "url": "http://localhost:5000/sqli",
            "description": "La aplicacion es vulnerable a SQL Injection",
            "solution": "Usar consultas parametrizadas"
        },
        {
            "alert": "Cross-Site Scripting (XSS)",
            "risk": "Alta",
            "url": "http://localhost:5000/xss",
            "description": "XSS Reflejado en parametro name",
            "solution": "Escapar output con html.escape()"
        },
        {
            "alert": "Command Injection",
            "risk": "Alta",
            "url": "http://localhost:5000/command",
            "description": "Command injection via parametro ip",
            "solution": "No usar shell=True, validar input"
        },
        {
            "alert": "Path Traversal",
            "risk": "Media",
            "url": "http://localhost:5000/path",
            "description": "Path traversal permite leer archivos del sistema",
            "solution": "Validar y restringir rutas de archivos"
        },
        {
            "alert": "Information Disclosure",
            "risk": "Media",
            "url": "http://localhost:5000/config",
            "description": "Endpoint /config expone configuracion sensible",
            "solution": "Proteger con autenticacion"
        },
        {
            "alert": "Missing Security Headers",
            "risk": "Media",
            "url": "http://localhost:5000/",
            "description": "Faltan headers de seguridad en las respuestas",
            "solution": "Agregar X-Frame-Options, CSP, HSTS, etc."
        },
        {
            "alert": "CSRF (Cross-Site Request Forgery)",
            "risk": "Media",
            "url": "http://localhost:5000/form",
            "description": "Formulario POST sin token CSRF",
            "solution": "Implementar tokens CSRF con Flask-WTF"
        },
        {
            "alert": "Weak Password Policy",
            "risk": "Media",
            "url": "http://localhost:5000/",
            "description": "Contrasenas almacenadas en texto plano en backup.sql",
            "solution": "Usar bcrypt para hash de contrasenas"
        },
        {
            "alert": "Cookie Without Secure/HttpOnly",
            "risk": "Baja",
            "url": "http://localhost:5000/",
            "description": "Cookies de sesion sin flags de seguridad",
            "solution": "Agregar Secure, HttpOnly y SameSite flags"
        },
        {
            "alert": "Server Version Disclosure",
            "risk": "Baja",
            "url": "http://localhost:5000/",
            "description": "Header Server revela version de servidor web",
            "solution": "Configurar servidor para ocultar version"
        }
    ]
}


if __name__ == '__main__':
    print("=" * 60)
    print("CLASIFICACION Y CORRECCION DE REPORTE DAST")
    print("=" * 60)

    analizador = ReporteDAST(reporte_ejemplo)
    plan = analizador.generar_plan_accion()

    print(f"\nTotal hallazgos: {len(plan)}")
    print(f"  Altos: {len([p for p in plan if p['severidad'] == 'Alta'])}")
    print(f"  Medios: {len([p for p in plan if p['severidad'] == 'Media'])}")
    print(f"  Bajos: {len([p for p in plan if p['severidad'] == 'Baja'])}")

    print("\n" + "=" * 60)
    print("PLAN DE ACCION PRIORIZADO")
    print("=" * 60)

    for i, item in enumerate(plan, 1):
        print(f"\n{i}. [{item['severidad'].upper()}] {item['vulnerabilidad']}")
        print(f"   URL: {item['url']}")
        print(f"   Descripcion: {item['descripcion']}")
        print(f"   CORRECCION:\n{item['correccion']}")
        print("-" * 60)


# ============================================================
# CODIGO CORREGIDO (version segura de la app vulnerable)
# ============================================================

def generar_app_segura():
    """
    Genera el codigo de la app corregida aplicando todas las
    correcciones del plan de accion.
    """
    codigo = '''
# app_segura_dast.py - Version corregida de la app vulnerable
from flask import Flask, request, render_template_string, jsonify, session
import sqlite3
import subprocess
import os
import html
import re

app = Flask(__name__)

# CORRECCION: Headers de seguridad
@app.after_request
def add_security_headers(response):
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    response.headers['X-XSS-Protection'] = '0'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    # CORRECCION: No revelar version del servidor
    response.headers['Server'] = 'WebServer'
    return response

# CORRECCION: Cookies seguras
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
)

# CORRECCION: Consultas parametrizadas (SQL Injection)
def buscar_usuario(user):
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM usuarios WHERE username = ?",
        (user,)
    )
    return cursor.fetchall()

# CORRECCION: Output encoding (XSS)
@app.route('/xss')
def xss_seguro():
    name = request.args.get('name', 'Invitado')
    name_seguro = html.escape(name)
    return f'<p>Hola, {name_seguro}!</p>'

# CORRECCION: Sin shell=True (Command Injection)
import ipaddress
@app.route('/command')
def command_seguro():
    ip = request.args.get('ip', '')
    try:
        ipaddress.ip_address(ip)
        result = subprocess.check_output(
            ['ping', '-n', '1', ip],
            timeout=5
        )
        return f'<pre>{result.decode()}</pre>'
    except (ValueError, ipaddress.AddressValueError):
        return '<p>IP invalida</p>', 400

# CORRECCION: Path sanitization (Path Traversal)
BASE_DIR = os.path.abspath('data')
@app.route('/path')
def path_seguro():
    file = request.args.get('file', '')
    ruta = os.path.normpath(os.path.join(BASE_DIR, file))
    if not ruta.startswith(BASE_DIR):
        return '<p>Acceso denegado</p>', 403
    if not os.path.exists(ruta):
        return '<p>Archivo no encontrado</p>', 404
    with open(ruta, 'r') as f:
        return f'<pre>{html.escape(f.read())}</pre>'

# CORRECCION: No exponer informacion
@app.route('/config')
def config_seguro():
    # Requiere autenticacion
    if not session.get('admin'):
        return jsonify({'error': 'No autorizado'}), 403
    return jsonify({'mensaje': 'Configuracion protegida'})

# CORRECCION: Proteger rutas sensibles
@app.route('/admin')
def admin_seguro():
    if not session.get('admin'):
        return '<h1>Acceso denegado</h1>', 403
    return '<h1>Panel de Administracion</h1>'

# CORRECCION: Eliminar endpoints que exponen informacion
# /backup.sql eliminado (no exponer backups)
# /robots.txt no expone rutas sensibles
'''
    return codigo
```

## Preguntas y Respuestas

**P1: Que es DAST y como funciona?**
R: DAST (Dynamic Application Security Testing) es una tecnica de analisis de seguridad que prueba una aplicacion en ejecucion desde afuera (black-box), simulando ataques reales. Funciona enviando requests HTTP maliciosos a la aplicacion y analizando las respuestas para detectar vulnerabilidades como XSS, SQL Injection, Command Injection y problemas de configuracion.

**P2: Cual es la diferencia principal entre SAST y DAST?**
R: SAST (Static) analiza el codigo fuente sin ejecutarlo, es white-box, se ejecuta temprano (build/commit), y detecta vulnerabilidades en el codigo mismo. DAST (Dynamic) analiza la aplicacion en ejecucion, es black-box, se ejecuta tarde (staging/produccion), y detecta vulnerabilidades en la configuracion y comportamiento en tiempo real. Son complementarios.

**P3: Que tipos de escaneo DAST existen?**
R: (1) No autenticado: escanea solo lo accesible sin login. (2) Autenticado: usa credenciales para acceder a areas protegidas. (3) Crawling: navega la app descubriendo endpoints y formularios. (4) Scanning (activo): ejecuta ataques contra los endpoints descubiertos. (5) API scanning: disenado para APIs REST/GraphQL.

**P4: Cuales son las limitaciones principales de DAST?**
R: (1) Cobertura limitada a funcionalidades accesibles via HTTP. (2) Falsos positivos: algunos ataques pueden no ser aplicables. (3) Lentitud: escaneos profundos pueden tomar horas. (4) No detecta vulnerabilidades que no se reflejan en la respuesta HTTP (como business logic flaws). (5) Requiere la aplicacion funcionando y desplegada.

**P5: Que es OWASP ZAP y que funcionalidades principales tiene?**
R: OWASP ZAP (Zed Attack Proxy) es una herramienta DAST open source mantenida por OWASP. Funcionalidades: proxy interceptador, spider (crawling), escaneo activo, escaneo pasivo, soporte para autenticacion, API REST para automatizacion, plugins extensibles, generacion de reportes, modo daemon para CI/CD.

**P6: Que es un escaneo DAST autenticado y por que es importante?**
R: Un escaneo autenticado usa credenciales de usuario (username/password o token) para navegar areas protegidas de la aplicacion despues del login. Es importante porque muchas vulnerabilidades solo existen en zonas autenticadas (perfil de usuario, panel de admin, configuracion). Sin autenticacion, la cobertura del escaneo es significativamente menor.

**P7: Como se clasifican los hallazgos en un reporte DAST y como se priorizan?**
R: Los hallazgos se clasifican por severidad: Alta (SQLi, XSS, Command Injection - corregir inmediatamente), Media (Path Traversal, Information Disclosure, Missing Headers - corregir pronto), Baja (Cookie flags, Server disclosure - corregir cuando sea posible), Informational. La priorizacion se basa en: severidad, exploitabilidad, impacto en el negocio, y si el activo esta expuesto a Internet.

## Tarea / Lectura Recomendada

1. **OWASP ZAP Documentation:**
   https://www.zaproxy.org/docs/

2. **OWASP ZAP API Reference:**
   https://www.zaproxy.org/docs/api/

3. **OWASP ZAP Full Scan Docker:**
   https://github.com/zaproxy/zaproxy/wiki/Docker

4. **Burp Suite Community Edition:**
   https://portswigger.net/burp/communitydownload

5. **Nikto Web Scanner:**
   https://github.com/sullo/nikto

6. **OWASP Testing Guide:**
   https://owasp.org/www-project-web-security-testing-guide/

7. **Tarea practica:** Instalar DVWA (Damn Vulnerable Web Application) en Docker y ejecutar un escaneo DAST completo con ZAP, clasificando y corrigiendo los hallazgos.

8. **Tarea practica:** Crear un script que automatice el escaneo DAST de 3 URLs diferentes usando la API de ZAP y genere un reporte comparativo.



