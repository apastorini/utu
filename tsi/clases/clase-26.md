# Clase 26: Componentes con Vulnerabilidades Conocidas + Logging/Monitoreo

**Duracion:** 2 horas

---

## Objetivos de Aprendizaje

1. Comprender la importancia de gestionar dependencias y componentes
2. Usar herramientas SCA (Snyk, Dependabot, OWASP Dependency-Check)
3. Conocer SBOM (Software Bill of Materials) y su utilidad
4. Implementar logging seguro sin exponer datos sensibles
5. Disenar un sistema de monitoreo y deteccion basico

---

## Contenido Detallado

### 1. Componentes con Vulnerabilidades Conocidas

OWASP Top 10 categoria #6: usar componentes con vulnerabilidades conocidas.

**Estadisticas:**
- 90%+ de las aplicaciones usan componentes open source
- En promedio, un proyecto tiene 50+ dependencias directas y 200+ transitivas
- Cada dependencia transitiva es un vector de ataque potencial

**Ejemplos de vulnerabilidades famosas:**

| Vulnerabilidad | Componente | Impacto | Year |
|---------------|-----------|---------|------|
| Log4Shell (CVE-2021-44228) | Log4j 2.x | RCE remoto sin autenticacion | 2021 |
| Struts2 S2-045 | Apache Struts 2 | RCE via Content-Type | 2017 |
| Heartbleed (CVE-2014-0160) | OpenSSL 1.0.1 | Filtracion de memoria | 2014 |
| Spring4Shell (CVE-2022-22965) | Spring Framework | RCE via data binding | 2022 |
| ImageTragick (CVE-2016-3714) | ImageMagick | RCE via imagenes maliciosas | 2016 |

### 2. Software Composition Analysis (SCA)

El SCA es el proceso de identificar y gestionar riesgos en componentes de software de terceros.

**Herramientas SCA:**

| Herramienta | Tipo | Caracteristicas |
|-------------|------|-----------------|
| **Snyk** | SaaS + CLI | Base de datos mas completa, integracion CI/CD, correcciones automaticas |
| **Dependabot** | GitHub integrado | PRs automaticos para actualizar dependencias |
| **OWASP Dependency-Check** | Open source | Analisis local, base de datos NVD, plugins Maven/Gradle |
| **GitHub Dependabot Alerts** | GitHub | Alertas automaticas de vulnerabilidades en dependencias |
| **WhiteSource (Mend)** | SaaS | Gestion completa de licencias y vulnerabilidades |
| **Sonatype Nexus Lifecycle** | SaaS + On-prem | Politicas de seguridad automatizadas |

### 3. SBOM (Software Bill of Materials)

SBOM es un inventario formal y estructurado de todos los componentes que conforman un software.

**Formato SPDX (ISO/IEC 5962):**

```json
{
  "spdxVersion": "SPDX-2.3",
  "dataLicense": "CC0-1.0",
  "name": "MiApp-SBOM",
  "creationInfo": {
    "created": "2024-06-25T10:00:00Z",
    "creators": ["Tool: MiApp-SBOM-Generator"]
  },
  "packages": [
    {
      "name": "Flask",
      "versionInfo": "2.3.0",
      "supplier": "Organization: Pallets Project",
      "downloadLocation": "https://pypi.org/project/Flask/2.3.0/",
      "licenseDeclared": "BSD-3-Clause",
      "copyrightText": "Copyright 2010 Pallets"
    },
    {
      "name": "requests",
      "versionInfo": "2.31.0",
      "supplier": "Organization: Python Software Foundation",
      "licenseDeclared": "Apache-2.0"
    }
  ]
}
```

### 4. Logging Seguro

#### Que NO debe loguearse

- Contrasenas (nunca, jamas)
- Tokens de autenticacion (JWT, API keys, session tokens)
- Datos de tarjetas de credito (PAN, CVV)
- Datos biometricos
- Informacion medica (a menos que sea estrictamente necesario y cifrado)
- Secretos de infraestructura (claves SSH, certificados privados)
- Datos personales no necesarios (GDPR)

#### Que SI debe loguearse

- Intentos de autenticacion (exitosos y fallidos) - sin contrasenas
- Cambios de permisos/roles
- Accesos denegados (403, 401)
- Errores del servidor con detalles tecnicos (sin datos sensibles)
- Operaciones de administrador
- Creacion/eliminacion de recursos
- Cambios en configuracion de seguridad
- Tiempos de respuesta anormales (posible ataque)

#### Logs Estructurados

```json
{
  "timestamp": "2024-06-25T10:30:00.123Z",
  "level": "WARN",
  "logger": "app.api.auth",
  "message": "Intento de login fallido",
  "context": {
    "user_id": "user_123",
    "ip": "192.168.1.100",
    "user_agent": "Mozilla/5.0...",
    "reason": "contrasena_incorrecta"
  },
  "request_id": "req_abc123",
  "session_id": "sess_xyz789"
}
```

### 5. SIEM y Deteccion de Intrusos

| Sistema | Descripcion |
|---------|-------------|
| **SIEM** (Security Information and Event Management) | Centraliza y correlaciona logs de multiples fuentes para detectar patrones de ataque |
| **IDS** (Intrusion Detection System) | Detecta actividad sospechosa en la red o sistema |
| **IPS** (Intrusion Prevention System) | Detecta y BLOQUEA actividad sospechosa en tiempo real |
| **WAF** (Web Application Firewall) | Protege aplicaciones web de ataques como SQLi, XSS |

**Ejemplos:**
- SIEM: Splunk, ELK Stack (Elasticsearch, Logstash, Kibana), Wazuh
- IDS/IPS: Snort, Suricata
- WAF: ModSecurity, Cloudflare WAF, AWS WAF

---

## Ejercicio 1: Analizar Dependencias con Snyk

### Escenario

Analizar un archivo `requirements.txt` con Snyk CLI para identificar vulnerabilidades y proponer correcciones.

**Paso 1: Crear requirements.txt vulnerable**

```txt
# requirements.txt - Proyecto con dependencias vulnerables
flask==1.0           # Version vulnerable: < 2.3.2
requests==2.20.0     # Version vulnerable: < 2.31.0
django==2.2          # Version vulnerable: < 3.2.23
urllib3==1.24.1      # Version vulnerable: < 1.26.18
pyyaml==5.1          # Version vulnerable: < 6.0
log4j==2.14.0        # Version vulnerable: < 2.17.0 (simulado)
```

**Paso 2: Analizar con Snyk**

```bash
# Instalar Snyk CLI
npm install -g snyk

# Autenticar (requiere cuenta gratuita en snyk.io)
snyk auth

# Probar Snyk (sin conexion)
snyk test --file=requirements.txt --package-manager=pip

# Generar reporte JSON
snyk test --json > snyk-report.json
```

**Paso 3: Script Python para analisis offline (simulado)**

```python
"""
sca_analyzer.py - Simulacion de analisis SCA
"""
import json
import re
from packaging.version import Version, InvalidVersion
from typing import Dict, List, Tuple

# Base de datos de vulnerabilidades simulada
VULNERABILITY_DB = {
    'flask': {
        'min_fixed': '2.3.2',
        'vulnerabilities': [
            {'id': 'CVE-2023-30861', 'severity': 'HIGH',
             'description': 'Possible XSS vulnerability in Flask',
             'affected': '<2.3.2'},
        ]
    },
    'requests': {
        'min_fixed': '2.31.0',
        'vulnerabilities': [
            {'id': 'CVE-2023-32681', 'severity': 'MEDIUM',
             'description': 'Potential bypass of SSL verification',
             'affected': '<2.31.0'},
        ]
    },
    'django': {
        'min_fixed': '3.2.23',
        'vulnerabilities': [
            {'id': 'CVE-2024-27351', 'severity': 'HIGH',
             'description': 'Potential denial-of-service via regex',
             'affected': '<3.2.23'},
        ]
    },
    'urllib3': {
        'min_fixed': '1.26.18',
        'vulnerabilities': [
            {'id': 'CVE-2023-45803', 'severity': 'MEDIUM',
             'description': 'Request body not always validated',
             'affected': '<1.26.18'},
        ]
    },
    'pyyaml': {
        'min_fixed': '6.0',
        'vulnerabilities': [
            {'id': 'CVE-2020-14343', 'severity': 'CRITICAL',
             'description': 'Arbitrary code execution via yaml.load()',
             'affected': '<6.0'},
        ]
    },
}


def parse_requirements(filepath: str) -> List[Dict]:
    """Parse a requirements.txt file"""
    dependencies = []
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and not line.startswith('-'):
                # Parsear: flask==1.0
                match = re.match(r'([a-zA-Z0-9_-]+)\s*==\s*([\d.]+)', line)
                if match:
                    dependencies.append({
                        'name': match.group(1),
                        'version': match.group(2),
                    })
    return dependencies


def analyze_dependencies(dependencies: List[Dict]) -> List[Dict]:
    """Analyze dependencies for known vulnerabilities"""
    results = []
    for dep in dependencies:
        name = dep['name']
        version = dep['version']
        vuln_info = VULNERABILITY_DB.get(name)

        if not vuln_info:
            results.append({
                'name': name,
                'version': version,
                'status': 'NO_KNOWN_VULNERABILITIES',
                'vulnerabilities': [],
                'fixed_version': None,
            })
            continue

        try:
            current = Version(version)
            fixed = Version(vuln_info['min_fixed'])

            if current < fixed:
                results.append({
                    'name': name,
                    'version': version,
                    'status': 'VULNERABLE',
                    'vulnerabilities': vuln_info['vulnerabilities'],
                    'fixed_version': vuln_info['min_fixed'],
                    'recommendation': f"Actualizar {name} de {version} a {vuln_info['min_fixed']}",
                })
            else:
                results.append({
                    'name': name,
                    'version': version,
                    'status': 'OK',
                    'vulnerabilities': [],
                    'fixed_version': None,
                })

        except InvalidVersion:
            results.append({
                'name': name,
                'version': version,
                'status': 'INVALID_VERSION',
                'vulnerabilities': [],
                'fixed_version': None,
            })

    return results


def generate_report(results: List[Dict]):
    """Generate a security report"""
    total = len(results)
    vulnerable = [r for r in results if r['status'] == 'VULNERABLE']
    ok = [r for r in results if r['status'] in ('OK', 'NO_KNOWN_VULNERABILITIES')]

    print("=" * 70)
    print("REPORTE DE ANALISIS SCA")
    print("=" * 70)
    print(f"\nTotal dependencias analizadas: {total}")
    print(f"Dependencias seguras: {len(ok)}")
    print(f"Dependencias VULNERABLES: {len(vulnerable)}")
    print()

    if vulnerable:
        print("VULNERABILIDADES ENCONTRADAS:")
        print("-" * 70)
        for v in vulnerable:
            print(f"\n[!] {v['name']} {v['version']} (arreglado en: {v['fixed_version']})")
            for vuln in v['vulnerabilities']:
                print(f"    CVE: {vuln['id']}")
                print(f"    Severidad: {vuln['severity']}")
                print(f"    Descripcion: {vuln['description']}")
            print(f"    Recomendacion: {v['recommendation']}")

    print("\n" + "=" * 70)
    print("DEPENDENCIAS SEGURAS:")
    print("-" * 70)
    for o in ok:
        print(f"  [+] {o['name']} {o['version']}")

    # Generar JSON
    report = {
        'summary': {
            'total': total,
            'vulnerable': len(vulnerable),
            'safe': len(ok),
        },
        'vulnerabilities': vulnerable,
    }
    print(f"\nReporte JSON generado: snyk_simulated_report.json")
    with open('snyk_simulated_report.json', 'w') as f:
        json.dump(report, f, indent=2)


def generate_fixed_requirements(results: List[Dict], original_file: str, output_file: str):
    """Generate a fixed requirements.txt"""
    fixes = {r['name']: r['fixed_version'] for r in results if r['fixed_version']}

    with open(original_file, 'r') as f_in, open(output_file, 'w') as f_out:
        for line in f_in:
            stripped = line.strip()
            match = re.match(r'([a-zA-Z0-9_-]+)\s*==\s*([\d.]+)', stripped)
            if match and match.group(1) in fixes:
                fixed_line = line.replace(
                    f"=={match.group(2)}",
                    f">={fixes[match.group(1)]}"
                )
                f_out.write(fixed_line)
            else:
                f_out.write(line)

    print(f"\nArchivo corregido generado: {output_file}")


if __name__ == '__main__':
    import sys

    req_file = sys.argv[1] if len(sys.argv) > 1 else 'requirements.txt'

    print(f"Analizando: {req_file}\n")

    dependencies = parse_requirements(req_file)
    results = analyze_dependencies(dependencies)
    generate_report(results)

    # Generar version corregida
    generate_fixed_requirements(results, req_file, 'requirements_fixed.txt')
```

**Ejecutar el analisis:**

```bash
# Crear requirements.txt
# Guardar el contenido vulnerable en requirements.txt

# Ejecutar el analizador
python sca_analyzer.py requirements.txt

# Ver el reporte generado
type snyk_simulated_report.json

# Ver el archivo con dependencias corregidas
type requirements_fixed.txt
```

---

## Ejercicio 2: Logger Seguro en Python

### Escenario

Escribir un sistema de logging que registre eventos de seguridad sin exponer datos sensibles.

```python
"""
secure_logger.py - Sistema de logging seguro
"""
import logging
import json
import re
import hashlib
from datetime import datetime, timezone
from typing import Dict, Optional, Any
from flask import Flask, request, g
import uuid

app = Flask(__name__)

# ============================================================
# CONFIGURACION DE LOGGING SEGURO
# ============================================================

class SensitiveDataFilter(logging.Filter):
    """
    Filtro que remueve datos sensibles de los mensajes de log.
    Patrones de datos sensibles que deben ser redactados.
    """

    SENSITIVE_PATTERNS = {
        'password': r'(?i)(password|passwd|pwd|secret|token|api_key|apikey|authorization)\s*[:=]\s*["\']?([^"\'\s&,]+)',
        'credit_card': r'\b(?:\d[ -]*?){13,16}\b',
        'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        'ssn': r'\b\d{3}-\d{2}-\d{4}\b',
        'ip_private': r'\b(10\.\d{1,3}\.\d{1,3}\.\d{1,3}|172\.(1[6-9]|2[0-9]|3[0-1])\.\d{1,3}\.\d{1,3}|192\.168\.\d{1,3}\.\d{1,3})\b',
    }

    def filter(self, record: logging.LogRecord) -> bool:
        """Filtra el mensaje y redacta datos sensibles"""
        if hasattr(record, 'msg') and isinstance(record.msg, str):
            original = record.msg
            for data_type, pattern in self.SENSITIVE_PATTERNS.items():
                record.msg = re.sub(pattern, f'[REDACTED_{data_type}]', record.msg)
            if original != record.msg:
                record.msg += ' [SENSITIVE_DATA_REDACTED]'
        return True


class JSONFormatter(logging.Formatter):
    """Formato JSON estructurado para logs"""

    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
            'message': record.getMessage(),
        }

        # Agregar excepcion si existe
        if record.exc_info and record.exc_info[0]:
            log_entry['exception'] = {
                'type': record.exc_info[0].__name__,
                'message': str(record.exc_info[1]),
                # NO incluir traceback completo en produccion (puede tener datos sensibles)
                'traceback': self.formatException(record.exc_info) if record.levelno <= logging.DEBUG else None,
            }

        # Agregar atributos extra (contexto)
        if hasattr(record, 'extra_data'):
            log_entry['extra'] = record.extra_data

        return json.dumps(log_entry, default=str, ensure_ascii=False)


class SecureLogger:
    """
    Logger seguro que registra eventos sin exponer datos sensibles.
    Proporciona metodos especificos para eventos de seguridad.
    """

    def __init__(self, name: str = 'secure_logger'):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)

        # Evitar duplicacion de handlers
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(JSONFormatter())
            handler.addFilter(SensitiveDataFilter())
            self.logger.addHandler(handler)

    def _sanitize_context(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Sanitiza el contexto eliminando/reemplazando datos sensibles"""
        if not context:
            return {}

        SENSITIVE_KEYS = {'password', 'pass', 'pwd', 'token', 'secret',
                          'api_key', 'api_secret', 'auth', 'authorization',
                          'credit_card', 'card_number', 'cvv', 'ssn', 'pin'}

        sanitized = {}
        for key, value in context.items():
            key_lower = key.lower()
            if any(sk in key_lower for sk in SENSITIVE_KEYS):
                sanitized[key] = '[REDACTED]'
            elif isinstance(value, str) and len(value) > 200:
                sanitized[key] = value[:200] + '... [TRUNCATED]'
            else:
                sanitized[key] = value

        return sanitized

    def auth_event(self, event_type: str, user_id: str, success: bool,
                   ip: str = '', context: Optional[Dict] = None):
        """Registra eventos de autenticacion"""
        extra = {
            'event_type': 'auth',
            'auth_event': event_type,
            'user_id': user_id,
            'success': success,
            'ip': ip,
            'user_agent': context.get('user_agent', '') if context else '',
        }
        # NO registrar contrasenas ni tokens
        if context:
            extra['context'] = self._sanitize_context(context)

        level = logging.INFO if success else logging.WARNING
        self.logger.log(level, f"Auth event: {event_type} - user={user_id} success={success}", extra={'extra_data': extra})

    def access_denied(self, user_id: str, resource: str, action: str,
                      ip: str = '', reason: str = ''):
        """Registra accesos denegados"""
        extra = {
            'event_type': 'access_control',
            'user_id': user_id,
            'resource': resource,
            'action': action,
            'ip': ip,
            'reason': reason,
            'status': 'denied',
        }
        self.logger.warning(f"Access denied: user={user_id} resource={resource} action={action}",
                           extra={'extra_data': extra})

    def data_change(self, user_id: str, resource_type: str, resource_id: str,
                    action: str, changes: Dict[str, Any]):
        """Registra cambios en datos"""
        # NO registrar los valores nuevos de datos sensibles
        safe_changes = self._sanitize_context(changes)

        extra = {
            'event_type': 'data_change',
            'user_id': user_id,
            'resource_type': resource_type,
            'resource_id': resource_id,
            'action': action,
            'changes': safe_changes,
        }
        self.logger.info(f"Data change: {action} on {resource_type}:{resource_id} by {user_id}",
                        extra={'extra_data': extra})

    def security_alert(self, alert_type: str, severity: str, message: str,
                       context: Optional[Dict] = None):
        """Registra alertas de seguridad"""
        extra = {
            'event_type': 'security_alert',
            'alert_type': alert_type,
            'severity': severity,
            'context': self._sanitize_context(context) if context else {},
        }
        level = getattr(logging, severity.upper(), logging.WARNING)
        self.logger.log(level, f"Security alert [{alert_type}]: {message}",
                        extra={'extra_data': extra})

    def error_event(self, error_type: str, message: str, user_id: str = '',
                    exception: Optional[Exception] = None):
        """Registra errores sin exponer datos sensibles"""
        extra = {
            'event_type': 'error',
            'error_type': error_type,
            'user_id': user_id,
        }
        self.logger.error(f"Error: {error_type} - {message}",
                         exc_info=exception,
                         extra={'extra_data': extra})


# ============================================================
# INSTANCIA GLOBAL
# ============================================================

secure_logger = SecureLogger()


# ============================================================
# EJEMPLO DE USO EN FLASK
# ============================================================

@app.before_request
def before_request():
    """Genera un request_id unico para tracking"""
    g.request_id = uuid.uuid4().hex[:16]
    g.start_time = datetime.now()


@app.after_request
def after_request(response):
    """Log de todas las requests (sin datos sensibles)"""
    if hasattr(g, 'start_time'):
        elapsed = (datetime.now() - g.start_time).total_seconds()

        # Solo loggear informacion basica, NO el body completo
        secure_logger.logger.info(
            f"Request: {request.method} {request.path} -> {response.status_code} ({elapsed:.3f}s)",
            extra={'extra_data': {
                'request_id': getattr(g, 'request_id', ''),
                'method': request.method,
                'path': request.path,
                'status': response.status_code,
                'elapsed': f"{elapsed:.3f}s",
                'ip': request.remote_addr,
                # NO incluir: request.data, request.args, request.form (pueden tener datos sensibles)
            }}
        )
    return response


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    # NUNCA loguear la contrasena
    secure_logger.auth_event(
        event_type='login',
        user_id=data.get('username', 'unknown'),
        success=True,  # Simplificado para el ejemplo
        ip=request.remote_addr,
        context={
            'username': data.get('username', ''),
            'user_agent': request.headers.get('User-Agent', ''),
            # password NO se incluye
        }
    )
    return {'mensaje': 'Login exitoso'}


@app.route('/api/datos-sensibles')
def datos_sensibles():
    # Probar que el filtro funciona
    password = "admin123"
    token = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0"
    credit_card = "4532-1234-5678-9012"

    logger.warning(f"Debug: password={password}, token={token}, card={credit_card}")
    # En logs: password=[REDACTED_password], token=[REDACTED_password], card=[REDACTED_credit_card]

    return {'mensaje': 'Revisar logs - datos sensibles deben estar redactados'}


if __name__ == '__main__':
    print("=== DEMOSTRACION DE LOGGER SEGURO ===\n")

    # Demostracion de eventos
    secure_logger.auth_event('login', 'user123', True, '192.168.1.1')
    secure_logger.auth_event('login', 'user456', False, '10.0.0.1',
                            {'reason': 'contrasena_incorrecta'})
    secure_logger.access_denied('user789', '/api/admin/users', 'delete',
                                '192.168.1.100', 'rol_insuficiente')
    secure_logger.data_change('admin', 'user', '123', 'update_role',
                              {'new_role': 'admin', 'old_role': 'user'})
    secure_logger.security_alert('brute_force', 'HIGH',
                                 'Multiple login failures detected',
                                 {'attempts': 50, 'ip': '10.0.0.50', 'timeframe': '5min'})

    # Demostrar redaccion de datos sensibles
    print("\n=== Prueba de redaccion de datos sensibles ===")
    secure_logger.logger.warning("Contrasena incorrecta: password='miPass123' para usuario admin",
                                extra={'extra_data': {}})

    # Iniciar servidor Flask
    print("\n=== Iniciando servidor Flask ===")
    app.run(host='127.0.0.1', port=5000)
```

---

## Ejercicio 3: Crear un SBOM Simple para un Proyecto

### Escenario

Crear un generador de SBOM que analice dependencias de un proyecto Python y genere el inventario en formato SPDX.

```python
"""
sbom_generator.py - Generador simple de SBOM
"""
import json
import hashlib
import os
from datetime import datetime, timezone
from typing import Dict, List
import pkg_resources
import re


class SBOMGenerator:
    """
    Genera un Software Bill of Materials (SBOM) en formato SPDX
    para un proyecto Python.
    """

    def __init__(self, project_name: str, project_version: str = "1.0.0"):
        self.project_name = project_name
        self.project_version = project_version
        self.packages = {}

    def scan_installed_packages(self):
        """
        Escanea los paquetes instalados en el entorno actual.
        En produccion, leer requirements.txt o poetry.lock en su lugar.
        """
        for dist in pkg_resources.working_set:
            self.packages[dist.key] = {
                'name': dist.key,
                'version': dist.version,
                'summary': getattr(dist, 'summary', ''),
                'home_page': getattr(dist, 'home_page', ''),
                'license': getattr(dist, 'license', ''),
            }

    def scan_requirements_file(self, filepath: str):
        """Escanea dependencias desde requirements.txt"""
        if not os.path.exists(filepath):
            print(f"Archivo no encontrado: {filepath}")
            return

        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and not line.startswith('-'):
                    match = re.match(r'([a-zA-Z0-9_.-]+)\s*([><=!]+)\s*([\d.*]+)', line)
                    if match:
                        name = match.group(1).lower()
                        version = match.group(3)
                        if name not in self.packages:
                            self.packages[name] = {
                                'name': name,
                                'version': version,
                                'summary': '',
                                'home_page': '',
                                'license': 'NOASSERTION',
                            }

    def generate_spdx(self) -> Dict:
        """Genera el SBOM en formato SPDX 2.3"""
        now = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

        spdx = {
            'spdxVersion': 'SPDX-2.3',
            'dataLicense': 'CC0-1.0',
            'SPDXID': 'SPDXRef-DOCUMENT',
            'name': f'{self.project_name}-{self.project_version}',
            'creationInfo': {
                'created': now,
                'creators': [
                    f'Tool: SBOMGenerator-1.0',
                    f'Organization: MiOrganizacion',
                ],
            },
            'documentNamespace': f'https://spdx.org/spdxdocs/{self.project_name}-{self.project_version}-{hashlib.md5(now.encode()).hexdigest()}',
            'packages': [],
            'relationships': [],
        }

        for pkg_name, pkg_info in self.packages.items():
            pkg_spdxid = f'SPDXRef-Package-{pkg_name}'

            pkg_entry = {
                'name': pkg_name,
                'SPDXID': pkg_spdxid,
                'versionInfo': pkg_info['version'],
                'supplier': 'NOASSERTION',
                'downloadLocation': pkg_info.get('home_page', 'NOASSERTION'),
                'licenseDeclared': self._normalize_license(pkg_info.get('license', 'NOASSERTION')),
                'copyrightText': 'NOASSERTION',
                'summary': pkg_info.get('summary', '')[:200] if pkg_info.get('summary') else 'NOASSERTION',
                'externalRefs': [
                    {
                        'referenceCategory': 'PACKAGE-MANAGER',
                        'referenceType': 'purl',
                        'referenceLocator': f'pkg:pypi/{pkg_name}@{pkg_info["version"]}'
                    }
                ],
            }

            # Si tiene checksum (archivo)
            spdx['packages'].append(pkg_entry)

            # Relacion: proyecto depende del paquete
            spdx['relationships'].append({
                'spdxElementId': 'SPDXRef-DOCUMENT',
                'relationshipType': 'DESCRIBES',
                'relatedSpdxElement': pkg_spdxid,
            })

        return spdx

    def _normalize_license(self, license_str: str) -> str:
        """Normaliza nombres de licencias a formato SPDX"""
        if not license_str or license_str == 'UNKNOWN':
            return 'NOASSERTION'

        license_map = {
            'MIT License': 'MIT',
            'Apache Software License': 'Apache-2.0',
            'BSD License': 'BSD-3-Clause',
            'GNU General Public License v2 or later (GPLv2+)': 'GPL-2.0-or-later',
            'GNU General Public License v3 or later (GPLv3+)': 'GPL-3.0-or-later',
            'Python Software Foundation License': 'PSF-2.0',
            'Mozilla Public License 2.0 (MPL 2.0)': 'MPL-2.0',
        }

        return license_map.get(license_str, license_str)

    def save_spdx(self, filepath: str = 'sbom.json'):
        """Guarda el SBOM en un archivo JSON"""
        spdx = self.generate_spdx()
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(spdx, f, indent=2, ensure_ascii=False)
        print(f"SBOM generado: {filepath}")

    def save_cyclonedx(self, filepath: str = 'sbom.cyclonedx.json'):
        """Genera SBOM en formato CycloneDX (simplificado)"""
        now = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

        cyclonedx = {
            '$schema': 'http://cyclonedx.org/schema/bom-1.5.schema.json',
            'bomFormat': 'CycloneDX',
            'specVersion': '1.5',
            'serialNumber': f'urn:uuid:{hashlib.md5(now.encode()).hexdigest()}',
            'version': 1,
            'metadata': {
                'timestamp': now,
                'tools': [{
                    'vendor': 'MiOrganizacion',
                    'name': 'SBOMGenerator',
                    'version': '1.0',
                }],
                'component': {
                    'type': 'application',
                    'name': self.project_name,
                    'version': self.project_version,
                    'bom-ref': self.project_name,
                }
            },
            'components': [],
        }

        for pkg_name, pkg_info in self.packages.items():
            cyclonedx['components'].append({
                'type': 'library',
                'name': pkg_name,
                'version': pkg_info['version'],
                'purl': f'pkg:pypi/{pkg_name}@{pkg_info["version"]}',
                'bom-ref': f'pkg:{pkg_name}@{pkg_info["version"]}',
                'licenses': [{
                    'license': {
                        'name': self._normalize_license(pkg_info.get('license', 'NOASSERTION'))
                    }
                }] if pkg_info.get('license') else [],
            })

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(cyclonedx, f, indent=2, ensure_ascii=False)
        print(f"SBOM (CycloneDX) generado: {filepath}")


# ============================================================
# USO
# ============================================================

def generate_sbom_for_project():
    """Genera SBOM para el proyecto actual"""
    generator = SBOMGenerator(
        project_name="MiApp",
        project_version="2.1.0"
    )

    # Escanear paquetes instalados
    print("Escaneando paquetes instalados...")
    generator.scan_installed_packages()

    # Si hay requirements.txt, escanearlo tambien
    req_file = 'requirements.txt'
    if os.path.exists(req_file):
        print(f"Escaneando dependencias desde {req_file}...")
        generator.scan_requirements_file(req_file)

    # Generar SBOM en formato SPDX
    print("\nGenerando SBOM...")
    generator.save_spdx('sbom_spdx.json')

    # Generar SBOM en formato CycloneDX
    generator.save_cyclonedx('sbom_cyclonedx.json')

    # Mostrar resumen
    print(f"\nResumen:")
    print(f"  Total paquetes: {len(generator.packages)}")
    print(f"  Licencias unicas: {len(set(p.get('license', 'UNKNOWN') for p in generator.packages.values()))}")

    # Verificar vulnerabilidades conocidas en los paquetes
    total_vulns = check_vulnerabilities(generator.packages)
    print(f"  Posibles vulnerabilidades: {total_vulns}")

    return generator.packages


def check_vulnerabilities(packages: Dict) -> int:
    """Verifica vulnerabilidades conocidas (simplificado)"""
    # En produccion, esto consultaria la API de Snyk o la base de datos NVD
    known_vulnerable = {
        'flask': ['1.0', '1.0.1', '1.0.2', '2.0', '2.1'],
        'requests': ['2.20.0', '2.21.0', '2.22.0'],
        'django': ['2.2', '2.2.1', '3.0', '3.1'],
        'urllib3': ['1.24.1', '1.25', '1.26.0'],
        'pyyaml': ['5.1', '5.2', '5.3'],
    }

    vuln_count = 0
    for pkg_name, pkg_info in packages.items():
        if pkg_name in known_vulnerable:
            if pkg_info['version'] in known_vulnerable[pkg_name]:
                print(f"  [!] {pkg_name} {pkg_info['version']} - POSIBLE VULNERABLE")
                vuln_count += 1

    return vuln_count


if __name__ == '__main__':
    print("=" * 60)
    print("GENERADOR DE SBOM")
    print("=" * 60)

    packages = generate_sbom_for_project()

    # Mostrar primeros paquetes
    print(f"\nPrimeros 10 paquetes:")
    for i, (name, info) in enumerate(sorted(packages.items())[:10]):
        print(f"  {i+1}. {name} == {info['version']} ({info.get('license', 'N/A')})")
```

---

## Preguntas y Respuestas

### Pregunta 1
**Que es SCA y por que es importante en el desarrollo de software?**

**Respuesta:** SCA (Software Composition Analysis) es el proceso de identificar y gestionar riesgos en componentes de terceros (open source, librerias comerciales). Es importante porque las aplicaciones modernas usan 50-200+ dependencias, cada una con su propio conjunto de vulnerabilidades. Sin SCA, el equipo de desarrollo no tiene visibilidad de que componentes estan usando, que vulnerabilidades tienen, ni cuando deben actualizarlos. SCA automatiza la deteccion de componentes vulnerables, licencias conflictivas, y genera alertas cuando se descubren nuevas vulnerabilidades en dependencias existentes.

### Pregunta 2
**Que datos NUNCA deben registrarse en logs y por que?**

**Respuesta:** Jamas deben registrarse: (1) contrasenas en texto plano (riesgo de compromiso de cuentas), (2) tokens de autenticacion y API keys (permite acceso no autorizado), (3) datos de tarjetas de credito (viola PCI DSS), (4) datos biometricos y de salud (viola HIPAA, GDPR), (5) secretos de infraestructura (claves SSH, certificados privados), (6) PII innecesaria (direcciones, DNI completos). Incluso en logs internos, si un atacante accede a los logs, obtiene estos datos. La regla es: si no es estrictamente necesario para debugging, no lo loguees. Si es necesario, ofuscalo o tokenizalo.

### Pregunta 3
**Que es un SBOM y para que sirve en seguridad?**

**Respuesta:** Un SBOM (Software Bill of Materials) es un inventario formal y estructurado de todos los componentes que conforman un software, incluyendo nombres, versiones, licencias, y relaciones de dependencia. Sirve para: (1) identificar rapidamente si una vulnerabilidad recien descubierta afecta al software, (2) gestionar licencias y cumplimiento legal, (3) facilitar auditorias de seguridad, (4) cumplir con requisitos regulatorios (EE.UU. orden ejecutiva 14028 requiere SBOM para software gubernamental), (5) mantener un inventario preciso de la superficie de ataque del software.

### Pregunta 4
**Cual es la diferencia entre dependencias directas y transitivas? Por que son importantes ambas?**

**Respuesta:** Dependencias directas son las que el proyecto incluye explicitamente (ej: `pip install requests`). Dependencias transitivas son las que las dependencias directas requieren a su vez (requests depende de urllib3, que depende de...). Ambas son importantes porque: una vulnerabilidad en una dependencia transitiva (como la de Log4j en aplicaciones Java que usaban ElasticSearch o Kafka) puede comprometer toda la aplicacion. El equipo de desarrollo muchas veces no sabe que dependencias transitivas tiene. Herramientas SCA como Snyk o Dependabot analizan el arbol completo de dependencias, no solo las directas.

### Pregunta 5
**Como se implementa un logging seguro en una aplicacion Flask?**

**Respuesta:** Para logging seguro en Flask: (1) implementar un filtro de logging que detecte y redacte patrones de datos sensibles (contrasenas, tokens, tarjetas de credito), (2) usar formato JSON estructurado para facilitar el analisis posterior, (3) nunca loguear el body completo de las requests (puede contener datos sensibles), (4) usar metodos especificos para eventos de seguridad (login, access denied, cambios de rol) que automaticamente excluyan campos sensibles, (5) configurar niveles de log apropiados (INFO para eventos normales, WARNING para sospechas, ERROR para fallos), (6) incluir un request_id unico en cada log para correlacionar eventos de una misma sesion.

### Pregunta 6
**Que es Log4Shell y como se relaciona con la gestion de componentes?**

**Respuesta:** Log4Shell (CVE-2021-44228) es una vulnerabilidad critica en Log4j 2.x que permite ejecucion remota de codigo sin autenticacion. La vulnerabilidad existia desde 2013 pero fue descubierta en diciembre 2021. Se relaciona con la gestion de componentes porque: (1) Log4j estaba presente en miles de aplicaciones como dependencia directa o transitiva, (2) muchas organizaciones no tenian un inventario (SBOM) de donde se usaba Log4j, (3) la correccion requirio actualizar a Log4j 2.17.0+, pero muchas aplicaciones no podian actualizar porque usaban versiones embedidas o dependencias transitivas que no se actualizaban, (4) demostro la importancia del SCA: si las organizaciones hubieran tenido visibilidad completa de sus dependencias, habrian podido responder mas rapido.

---

## Tarea / Lectura Recomendada

1. **Leer:** OWASP Dependency Check - https://owasp.org/www-project-dependency-check/
2. **Practicar:** Crear cuenta en Snyk (snyk.io) y analizar un proyecto real
3. **Leer:** OWASP Logging Cheat Sheet - https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html
4. **Practicar:** Configurar Dependabot en un repositorio GitHub
5. **Leer:** SBOM Guide - CISA: https://www.cisa.gov/sbom
6. **Experimentar:** Generar SBOM para el proyecto actual usando el codigo del ejercicio 3
7. **Profundizar:** Investigar el formato CycloneDX vs SPDX para SBOM
8. **Leer:** OWASP Top 10:2021 - A06:2021 Vulnerable and Outdated Components



