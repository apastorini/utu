# Clase: Seguridad en APIs - REST, GraphQL y SOAP

## OWASP API Security, Ataques Conocidos, Herramientas de Chequeo y Pipeline CI/CD Seguro

---

**Versión:** 1.0  
**Fecha:** Abril 2026  
**Proyecto:** Curso de Ciberseguridad - Tarea 1

---

## Tabla de Contenidos

1. ¿Qué es una API?
2. Los 3 Tipos de APIs: REST, GraphQL, SOAP
3. OWASP API Security Top 10 (2023)
4. Seguridad en APIs REST
5. Seguridad en APIs GraphQL
6. Seguridad en APIs SOAP
7. Herramientas de Chequeo y Escaneo
8. SBOM - Software Bill of Materials
9. Pipeline CI/CD con Seguridad
10. Ataques Conocidos por Tipo de API
11. Comparación de Vulnerabilidades
12. Referencias

---

## 1. ¿Qué es una API?

**API (Application Programming Interface)** es un conjunto de reglas que permite que dos aplicaciones se comuniquen entre sí.

### Analogía: El Restaurante

```
┌─────────────────────────────────────────────────────────┐
│                  ANALOGÍA DEL RESTAURANTE               │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Tú (Cliente)          →  Aplicación que pide datos     │
│  Mesero (API)          →  Intermediario que lleva       │
│                           la petición y trae respuesta   │
│  Cocina (Servidor)     →  Sistema que procesa y         │
│                           devuelve datos                │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### ¿Por qué es importante la seguridad en APIs?

- Las APIs son la **puerta de entrada** a los datos y la lógica de negocio
- Las APIs exponen directamente la base de datos y los servicios
- Las APIs no tienen interfaz visual → los atacantes interactúan directamente
- El 91% de las apps tienen al menos 1 vulnerabilidad de API (informe 2024)

---

## 2. Los 3 Tipos de APIs: REST, GraphQL, SOAP

### Comparación General

| Característica | REST | GraphQL | SOAP |
|---------------|------|---------|------|
| **Protocolo** | HTTP/HTTPS | HTTP/HTTPS | HTTP, SMTP, JMS |
| **Formato** | JSON, XML | JSON | XML |
| **Arquitectura** | Recursos (URLs) | Grafo (un endpoint) | Servicios (WSDL) |
| **Flexibilidad** | Media (endpoints fijos) | Alta (cliente elige) | Baja (contrato estricto) |
| **Complejidad** | Baja | Media | Alta |
| **Uso típico** | Web apps, móviles | Apps modernas, microservicios | Enterprise, bancos, legacy |
| **Seguridad** | OAuth, JWT, HTTPS | OAuth, JWT + query depth | WS-Security, TLS |

### REST - Representational State Transfer

Cada recurso tiene una URL:

```
GET    /api/usuarios        → Lista de usuarios
GET    /api/usuarios/5      → Usuario con ID 5
POST   /api/usuarios        → Crear usuario
PUT    /api/usuarios/5      → Actualizar usuario 5
DELETE /api/usuarios/5      → Eliminar usuario 5
```

### GraphQL

Un solo endpoint, el cliente elige qué datos recibir:

```
Endpoint único: POST /graphql

query {
  usuario(id: 5) {
    nombre
    email
    pedidos {
      id
      total
    }
  }
}
```

### SOAP

Contrato estricto definido en WSDL. Usa XML con envelope:

```xml
POST /api/banco
Content-Type: text/xml
SOAPAction: "ObtenerSaldo"

<soap:Envelope>
  <soap:Header>
    <wsse:Security>
      <wsse:UsernameToken>
        <wsse:Username>juan</wsse:Username>
        <wsse:Password>abc123</wsse:Password>
      </wsse:UsernameToken>
    </wsse:Security>
  </soap:Header>
  <soap:Body>
    <banco:ObtenerSaldo>
      <banco:cuenta>12345678</banco:cuenta>
    </banco:ObtenerSaldo>
  </soap:Body>
</soap:Envelope>
```

---

## 3. OWASP API Security Top 10 (2023)

```
┌─────────────────────────────────────────────────────────┐
│           OWASP API SECURITY TOP 10 - 2023              │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  API1:2023  Broken Object Level Authorization (BOLA)    │
│  API2:2023  Broken Authentication                       │
│  API3:2023  Broken Object Property Level Authorization  │
│  API4:2023  Unrestricted Resource Consumption            │
│  API5:2023  Broken Function Level Authorization          │
│  API6:2023  Unrestricted Access to Sensitive Business    │
│             Flows                                       │
│  API7:2023  Server Side Request Forgery (SSRF)          │
│  API8:2023  Security Misconfiguration                   │
│  API9:2023  Improper Inventory Management               │
│  API10:2023 Unsafe Consumption of APIs                  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Descripción de cada vulnerabilidad

| ID | Nombre | Qué es | Ejemplo |
|----|--------|--------|---------|
| **API1** | BOLA | Acceder a objetos de otros usuarios | GET /pedidos/123 (de otro usuario) |
| **API2** | Broken Auth | Autenticación débil o bypass | JWT sin verificar firma |
| **API3** | BOPULA | Exponer propiedades sensibles | GET /usuario/5 devuelve password_hash |
| **API4** | Unrestricted Resources | Sin límites de consumo | 10,000 requests/segundo sin rate limit |
| **API5** | BFLA | Acceder a funciones no autorizadas | Usuario normal accede a /admin/users |
| **API6** | Sensitive Business Flows | Abusar de flujos de negocio | Comprar 1000 items con cupón de 1 uso |
| **API7** | SSRF | Hacer requests desde el servidor | URL param → http://169.254.169.254 |
| **API8** | Misconfiguration | Config insegura por defecto | CORS *, debug mode, headers faltantes |
| **API9** | Inventory Mgmt | APIs viejas/expuestas sin control | API v1 sin auth que nunca se eliminó |
| **API10** | Unsafe API Consumption | Confiar ciegamente en APIs externas | API de terceros comprometida |

---

## 4. Seguridad en APIs REST

### 4.1 Autenticación con JWT

```python
# ✅ SEGURO - JWT Authentication
from functools import wraps
import jwt

def requiere_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"error": "Token requerido"}), 401
        
        try:
            token = token.split(" ")[1]
            payload = jwt.decode(
                token,
                os.environ.get("SECRET_KEY"),
                algorithms=["HS256"]
            )
            g.usuario_id = payload["user_id"]
            g.usuario_rol = payload["role"]
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expirado"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Token inválido"}), 401
        
        return f(*args, **kwargs)
    return decorated
```

### 4.2 Autorización (BOLA + BFLA)

```python
# ✅ SEGURO - Verificar propiedad del recurso (BOLA)
@app.route('/api/pedidos/<int:pedido_id>')
@requiere_token
def get_pedido(pedido_id):
    pedido = Pedido.query.filter_by(
        id=pedido_id,
        usuario_id=g.usuario_id  # Solo sus propios pedidos
    ).first()
    if not pedido:
        return jsonify({"error": "No encontrado"}), 404
    return jsonify(pedido.to_dict())

# ✅ SEGURO - Verificar rol (BFLA)
def requiere_admin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if g.usuario_rol != "admin":
            return jsonify({"error": "Admin requerido"}), 403
        return f(*args, **kwargs)
    return decorated

@app.route('/api/admin/usuarios')
@requiere_token
@requiere_admin
def listar_usuarios():
    usuarios = Usuario.query.all()
    return jsonify([u.to_dict() for u in usuarios])
```

### 4.3 Rate Limiting

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/api/login', methods=['POST'])
@limiter.limit("5 per minute")  # Máximo 5 logins por minuto
def login():
    # ...

@app.route('/api/buscar')
@limiter.limit("30 per minute")  # Máximo 30 búsquedas por minuto
def buscar():
    # ...
```

### 4.4 Input Validation

```python
from marshmallow import Schema, fields, validate

class CrearUsuarioSchema(Schema):
    nombre = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=8))
    rol = fields.Str(validate=validate.OneOf(["usuario", "editor"]))
    # NO se permite enviar "admin" directamente

@app.route('/api/usuarios', methods=['POST'])
@requiere_token
@requiere_admin
def crear_usuario():
    schema = CrearUsuarioSchema()
    errores = schema.validate(request.json)
    if errores:
        return jsonify({"errores": errores}), 400
    datos = schema.load(request.json)
    # Crear usuario con datos validados...
```

### 4.5 Response Filtering (BOPULA)

```python
# ✅ SEGURO - Solo campos permitidos
def to_dict_public(self):
    return {
        "id": self.id,
        "nombre": self.nombre,
        "email": self.email,
        "role": self.role,
        "created_at": self.created_at.isoformat()
    }
    # NO incluir password_hash ni tokens
```

### 4.6 Checklist de Seguridad REST

| Control | Implementación |
|---------|---------------|
| HTTPS | TLS 1.2+ obligatorio |
| Autenticación | JWT con expiración, OAuth 2.0 |
| BOLA | Verificar propiedad del recurso |
| BFLA | Verificar rol del usuario |
| Rate Limiting | Por IP, por usuario, por endpoint |
| Input Validation | Schema validation, sanitización |
| CORS | Orígenes específicos, no `*` |
| Versionado | /api/v1/, /api/v2/ |

---

## 5. Seguridad en APIs GraphQL

### 5.1 Vulnerabilidades Específicas

| Vulnerabilidad | Descripción | Impacto |
|---------------|-------------|---------|
| **Introspection** | El atacante ve todo el schema | Mapa completo de la API |
| **Query Depth** | Queries anidadas infinitas | DoS del servidor |
| **Query Complexity** | Queries con muchas relaciones | Sobrecarga del servidor |
| **Batch Attacks** | Múltiples operaciones en una query | Bypass de rate limiting |
| **Alias Overloading** | Múltiples aliases para el mismo campo | DoS por duplicación |
| **BOLA en GraphQL** | Acceder a datos de otros | Igual que REST pero con queries |

### 5.2 Introspection

```graphql
# ❌ El atacante descubre TODO el schema
query {
  __schema {
    types { name, fields { name, type { name } } }
  }
}
```

**Protección:**

```python
app.config["GRAPHQL_INTROSPECTION"] = False  # Deshabilitar en producción
```

### 5.3 Query Depth Attack

```graphql
# ❌ Profundidad infinita → DoS
query {
  usuario(id: 1) {
    amigos { amigos { amigos { amigos { ... } } } }
  }
}
```

**Protección - Depth Limiter:**

```python
class DepthLimiter(ValidationRule):
    def __init__(self, max_depth=5):
        self.max_depth = max_depth
        self.current_depth = 0
    
    def enter_field(self, node, *args):
        self.current_depth += 1
        if self.current_depth > self.max_depth:
            self.report_error(
                f"Query depth {self.current_depth} exceeds max {self.max_depth}"
            )
    
    def leave_field(self, node, *args):
        self.current_depth -= 1
```

### 5.4 Query Complexity

```graphql
# ❌ Query compleja → 2,500,000,000 objetos a resolver
query {
  usuarios {
    nombre
    pedidos {
      productos {
        reviews {
          autor { amigos { nombre } }
        }
      }
    }
  }
}
```

**Protección:**

```python
def calcular_complejidad(query, schema):
    MAX_COMPLEJIDAD = 1000
    complejidad = sumar_costos(query)
    if complejidad > MAX_COMPLEJIDAD:
        raise Exception(
            f"Query complexity {complejidad} exceeds max {MAX_COMPLEJIDAD}"
        )
    return complejidad
```

### 5.5 BOLA en GraphQL

```python
# ✅ SEGURO - Resolver verifica autorización
def resolve_pedido(self, info, id):
    usuario_actual = info.context.user
    pedido = Pedido.objects.get(id=id)
    if pedido.usuario_id != usuario_actual.id:
        raise Exception("No autorizado")
    return pedido
```

### 5.6 Batch Attack

```python
# ✅ PROTECCIÓN - Limitar batch size
@app.route('/graphql', methods=['POST'])
def graphql_endpoint():
    data = request.json
    if isinstance(data, list) and len(data) > 10:
        return jsonify({"error": "Batch too large"}), 400
    return procesar_graphql(data)
```

### 5.7 Checklist de Seguridad GraphQL

| Control | Implementación |
|---------|---------------|
| Introspection | Deshabilitar en producción |
| Query Depth | Máximo 5-10 niveles |
| Query Complexity | Máximo 1000-5000 puntos |
| Batch Limit | Máximo 10 operaciones por request |
| BOLA | Resolver verifica propiedad |
| Rate Limiting | Por IP y por usuario |
| Timeout | Máximo 10s por query |

---

## 6. Seguridad en APIs SOAP

### 6.1 Vulnerabilidades Específicas

| Vulnerabilidad | Descripción | Impacto |
|---------------|-------------|---------|
| **XXE (XML External Entity)** | Inyectar entidades XML para leer archivos | Acceso a archivos del servidor |
| **XML Bomb (Billion Laughs)** | Entities anidadas que expanden exponencialmente | DoS por memoria |
| **WSDL Disclosure** | WSDL expuesto públicamente | Mapa completo del servicio |
| **SOAP Action Spoofing** | Manipular SOAPAction header | Ejecutar operaciones no autorizadas |
| **XML Signature Wrapping** | Manipular firmas XML | Bypass de autenticación |

### 6.2 XXE Attack

```xml
<!-- ❌ VULNERABLE - XXE -->
<soap:Envelope>
  <soap:Body>
    <!DOCTYPE foo [
      <!ENTITY xxe SYSTEM "file:///etc/passwd">
    ]>
    <banco:ObtenerDatos>
      <banco:cuenta>&xxe;</banco:cuenta>
    </banco:ObtenerDatos>
  </soap:Body>
</soap:Envelope>
```

**Protección:**

```python
from defusedxml import defuse_stdlib
defuse_stdlib()  # Deshabilita entidades externas

# O con lxml:
parser = etree.XMLParser(
    resolve_entities=False,
    no_network=True,
    load_dtd=False
)
```

### 6.3 XML Bomb

```xml
<!-- ❌ XML BOMB → 3GB+ en memoria -->
<!DOCTYPE lolz [
  <!ENTITY lol "lol">
  <!ENTITY lol2 "&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;">
  <!ENTITY lol3 "&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;">
  ... hasta lol9
]>
<soap:Body><dato>&lol9;</dato></soap:Body>
```

**Protección:**

```python
parser = etree.XMLParser(
    resolve_entities=False,
    load_dtd=False,
    huge_tree=False,
    entity_loader=False
)
```

### 6.4 WS-Security

```xml
<!-- ✅ SOAP con WS-Security completo -->
<soap:Header>
  <wsse:Security>
    <wsse:UsernameToken>
      <wsse:Username>juan</wsse:Username>
      <wsse:Password Type="...#PasswordDigest">
        K7gNU3sdo+OL0wNhqoVWhr3g6s1xYv72ol/pe/Unols=
      </wsse:Password>
      <wsse:Nonce>WScqanjCEAC4mQoBE07sAQ==</wsse:Nonce>
      <wsu:Created>2026-04-30T10:00:00Z</wsu:Created>
    </wsse:UsernameToken>
    <ds:Signature>...</ds:Signature>
    <wsu:Timestamp>
      <wsu:Created>2026-04-30T10:00:00Z</wsu:Created>
      <wsu:Expires>2026-04-30T10:05:00Z</wsu:Expires>
    </wsu:Timestamp>
  </wsse:Security>
</soap:Header>
```

### 6.5 Checklist de Seguridad SOAP

| Control | Implementación |
|---------|---------------|
| XXE | Deshabilitar entidades externas |
| XML Bomb | Limitar expansión de entities |
| WS-Security | Password digest + firma digital |
| Timestamps | Prevenir replay attacks |
| WSDL | No exponer en producción |
| TLS | HTTPS obligatorio |
| Schema Validation | Validar XML contra XSD |

---

## 7. Herramientas de Chequeo y Escaneo

### 7.1 Panorama General

```
┌─────────────────────────────────────────────────────────┐
│           HERRAMIENTAS DE CHEQUEO DE SEGURIDAD          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │  SAST (Static Application Security Testing)     │   │
│  │  │                                              │   │
│  │  ├── Semgrep        → Análisis de código fuente │   │
│  │  ├── SonarQube      → Calidad + seguridad       │   │
│  │  └── SpotBugs       → Bugs en Java/bytecode     │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │  SCA (Software Composition Analysis)            │   │
│  │  │                                              │   │
│  │  ├── OWASP Dependency-Check → Dependencias Java │   │
│  │  ├── Trivy            → Imágenes + filesystem   │   │
│  │  └── npm audit / safety → Dependencias web/py   │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │  DAST (Dynamic Application Security Testing)    │   │
│  │  │                                              │   │
│  │  ├── OWASP ZAP        → Escaneo de APIs web    │   │
│  │  ├── Burp Suite       → Proxy + scanner        │   │
│  │  └── SoapUI Security  → APIs SOAP/REST          │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 7.2 Semgrep - Análisis Estático de Código

**Qué es:** Herramienta de análisis estático que busca patrones de vulnerabilidades en el código fuente.

**Instalación:**

```bash
pip install semgrep
```

**Uso básico:**

```bash
# Escaneo automático con reglas predefinidas
semgrep scan --config auto .

# Escaneo específico para Python
semgrep scan --config auto --lang python .

# Escaneo para Java
semgrep scan --config auto --lang java .

# Escaneo para JavaScript
semgrep scan --config auto --lang javascript .

# Output en formato JSON (para pipelines)
semgrep scan --config auto --json -o semgrep-results.json .

# Escaneo con reglas de OWASP Top 10
semgrep scan --config p/owasp-top-ten .
```

**Ejemplo de lo que detecta:**

```python
# Semgrep detectará automáticamente:
# ❌ SQL Injection
query = f"SELECT * FROM users WHERE id = {user_id}"

# ❌ Hardcoded secrets
API_KEY = "sk-1234567890abcdef"

# ❌ Deserialización insegura
data = pickle.loads(user_input)

# ❌ Eval con input del usuario
result = eval(user_input)
```

### 7.3 Trivy - Escaneo de Imágenes y Filesystem

**Qué es:** Scanner de vulnerabilidades para contenedores, filesystem, IaC y más.

**Instalación:**

```bash
# Windows (winget)
winget install Trivy

# Linux
sudo apt install trivy

# macOS
brew install trivy
```

**Configuración básica:**

```bash
# Crear archivo de configuración
mkdir -p ~/.trivy
cat > ~/.trivy.yaml << 'EOF'
# Configuración de Trivy
cache:
  dir: /tmp/trivy-cache

scan:
  severity:
    - HIGH
    - CRITICAL
  ignore-unfixed: true

db:
  skip-update: false
EOF
```

**Uso - Escaneo de filesystem:**

```bash
# Escanear directorio completo (solo HIGH y CRITICAL)
trivy fs --severity HIGH,CRITICAL C:\Agesic\

# Escanear con output en tabla
trivy fs --severity HIGH,CRITICAL --format table C:\Agesic\

# Escanear con output en JSON
trivy fs --severity HIGH,CRITICAL --format json -o trivy-results.json C:\Agesic\

# Escanear con ignorar vulnerabilidades no fijadas
trivy fs --severity HIGH,CRITICAL --ignore-unfixed C:\Agesic\
```

**Uso - Escaneo de imagen Docker:**

```bash
# Escanear imagen de Docker
trivy image python:3.11-slim

# Escanear con severity filter
trivy image --severity HIGH,CRITICAL python:3.11-slim

# Escanear y guardar reporte
trivy image --severity HIGH,CRITICAL --format json -o image-report.json python:3.11-slim
```

**Uso - Escaneo de Infrastructure as Code:**

```bash
# Escanear Terraform
trivy config terraform/

# Escanear Kubernetes manifests
trivy config k8s/

# Escanear Dockerfile
trivy config Dockerfile
```

**Ejemplo de output:**

```
┌─────────────────────────────────────────────────────────┐
│ Trivy Scan Results - C:\Agesic\                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ requirements.txt (pip)                                  │
│ ┌──────────┬──────────────┬──────────┬────────────────┐│
│ │ Library  │ Vulnerability│ Severity │ Status         ││
│ ├──────────┼──────────────┼──────────┼────────────────┤│
│ │ requests │ CVE-2023-32681│ CRITICAL │ Fixed in 2.31  ││
│ │ django   │ CVE-2023-36053│ HIGH     │ Fixed in 4.2.4 ││
│ │ pillow   │ CVE-2023-44271│ HIGH     │ Fixed in 10.0  ││
│ └──────────┴──────────────┴──────────┴────────────────┘│
│                                                         │
│ Total: 3 (CRITICAL: 1, HIGH: 2)                        │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 7.4 OWASP Dependency Check (Maven)

**Qué es:** Plugin de Maven que analiza las dependencias del proyecto y busca vulnerabilidades conocidas (CVEs) en la base de datos del NVD.

**Configuración en pom.xml:**

```xml
<project>
    ...
    <build>
        <plugins>
            <!-- OWASP Dependency Check -->
            <plugin>
                <groupId>org.owasp</groupId>
                <artifactId>dependency-check-maven</artifactId>
                <version>9.2.0</version>
                <configuration>
                    <!-- Formatos de reporte -->
                    <formats>
                        <format>HTML</format>
                        <format>JSON</format>
                    </formats>
                    
                    <!-- Suppressions (falsos positivos) -->
                    <suppressionFiles>
                        <suppressionFile>suppressions.xml</suppressionFile>
                    </suppressionFiles>
                    
                    <!-- Severidad mínima para fallar el build -->
                    <failBuildOnCVSS>7</failBuildOnCVSS>
                    
                    <!-- Solo HIGH y CRITICAL -->
                    <failOnError>false</failOnError>
                </configuration>
                <executions>
                    <execution>
                        <goals>
                            <goal>check</goal>
                        </goals>
                    </execution>
                </executions>
            </plugin>
        </plugins>
    </build>
</project>
```

**Ejecución:**

```bash
# Ejecutar el check
mvn org.owasp:dependency-check-maven:check

# Con reporte HTML detallado
mvn org.owasp:dependency-check-maven:check -Dformat=HTML

# Generar reporte JSON
mvn org.owasp:dependency-check-maven:check -Dformat=JSON

# Verificar y fallar el build si hay vulnerabilidades críticas
mvn org.owasp:dependency-check-maven:check -DfailBuildOnCVSS=7
```

**Archivo de suppressions (falsos positivos):**

```xml
<!-- suppressions.xml -->
<?xml version="1.0" encoding="UTF-8"?>
<suppressions xmlns="https://jeremylong.github.io/DependencyCheck/dependency-suppression.1.3.xsd">
    <suppress>
        <!-- Falso positivo: esta librería no usa esa función vulnerable -->
        <notes>Falso positivo - la función vulnerable no se usa</notes>
        <cve>CVE-2023-12345</cve>
    </suppress>
</suppressions>
```

**Ejemplo de reporte:**

```
┌─────────────────────────────────────────────────────────┐
│ Dependency-Check Report                                  │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ Dependencia                    CVE              CVSS    │
│ ────────────────────────────── ──────────────── ──────  │
│ log4j-core-2.14.1.jar          CVE-2021-44228   10.0   │
│ spring-core-5.3.18.jar         CVE-2022-22965    9.8   │
│ jackson-databind-2.13.1.jar    CVE-2022-42003    7.5   │
│                                                         │
│ Found 3 vulnerabilities (CRITICAL: 1, HIGH: 2)         │
│ Build FAILED (failBuildOnCVSS=7)                        │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 7.5 SpotBugs - Análisis de Bytecode Java

**Qué es:** Herramienta de análisis estático que busca bugs potenciales en bytecode Java, incluyendo vulnerabilidades de seguridad.

**Configuración en pom.xml:**

```xml
<project>
    ...
    <build>
        <plugins>
            <!-- SpotBugs -->
            <plugin>
                <groupId>com.github.spotbugs</groupId>
                <artifactId>spotbugs-maven-plugin</artifactId>
                <version>4.8.5.0</version>
                <configuration>
                    <!-- Nivel de esfuerzo: min, default, max -->
                    <effort>Max</effort>
                    
                    <!-- Umbral de reporte: Low, Medium, High -->
                    <threshold>Medium</threshold>
                    
                    <!-- Formato de reporte -->
                    <xmlOutput>true</xmlOutput>
                    <htmlOutput>true</htmlOutput>
                    
                    <!-- Excluir filtros -->
                    <excludeFilterFile>spotbugs-exclude.xml</excludeFilterFile>
                </configuration>
            </plugin>
        </plugins>
    </build>
</project>
```

**Ejecución:**

```bash
# Generar reporte de SpotBugs
mvn spotbugs:spotbugs

# Generar reporte HTML
mvn spotbugs:spotbugs -Dspotbugs.htmlOutput=true

# Ver en interfaz GUI
mvn spotbugs:gui
```

**Ejemplo de lo que detecta:**

```java
// SpotBugs detectará:

// ❌ SQL Injection potencial
Statement stmt = conn.createStatement();
ResultSet rs = stmt.executeQuery(
    "SELECT * FROM users WHERE id = " + userInput
);

// ❌ Path Traversal potencial
File f = new File(baseDir, userInput);
FileInputStream fis = new FileInputStream(f);

// ❌ Hardcoded password
String password = "admin123";

// ❌ Unused field
private String neverUsed;

// ❌ Null pointer dereference
String x = null;
x.length();  // NPE seguro
```

**Archivo de exclusiones:**

```xml
<!-- spotbugs-exclude.xml -->
<FindBugsFilter>
    <!-- Excluir clases de test -->
    <Match>
        <Class name="~.*Test" />
    </Match>
    <!-- Excluir clase generada -->
    <Match>
        <Class name="com.miapp.generated.DTO" />
    </Match>
</FindBugsFilter>
```

### 7.6 SonarQube - Análisis Continuo de Calidad y Seguridad

**Qué es:** Plataforma de inspección continua de calidad de código que detecta bugs, vulnerabilidades y code smells.

**Instalación con Docker:**

```bash
# Iniciar SonarQube
docker run -d --name sonarqube \
  -p 9000:9000 \
  -e SONAR_ES_BOOTSTRAP_CHECKS_DISABLE=true \
  sonarqube:community

# Acceder en http://localhost:9000
# Usuario: admin / Password: admin
```

**Configurar el scanner (sonar-scanner-cli):**

```bash
# Instalar
npm install -g sonar-scanner

# O descargar de:
# https://docs.sonarsource.com/sonarqube/latest/analyzing-source-code/scanners/sonarscanner/
```

**Configuración del proyecto (sonar-project.properties):**

```properties
# sonar-project.properties

# Identificación del proyecto
sonar.projectKey=mi-api-segura
sonar.projectName=API Segura
sonar.projectVersion=1.0

# Ruta del código fuente
sonar.sources=src/main/java

# Exclusiones
sonar.exclusions=**/test/**,**/generated/**

# Lenguaje
sonar.language=java

# Codificación
sonar.sourceEncoding=UTF-8

# Quality Gate (fallar si hay vulnerabilidades)
sonar.qualitygate.wait=true
```

**Ejecutar análisis:**

```bash
# Ejecutar análisis
sonar-scanner \
  -Dsonar.projectKey=mi-api-segura \
  -Dsonar.sources=src/main/java \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.token=TU_TOKEN_AQUI

# Con Maven
mvn sonar:sonar \
  -Dsonar.projectKey=mi-api-segura \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.token=TU_TOKEN_AQUI
```

**Lo que detecta SonarQube:**

| Categoría | Ejemplo |
|-----------|---------|
| **Vulnerabilidades** | SQL Injection, XSS, Hardcoded passwords |
| **Bugs** | Null pointer, Resource leaks, Dead locks |
| **Code Smells** | Duplicación, complejidad ciclomática alta |
| **Security Hotspots** | Código que necesita revisión manual |
| **Coverage** | Porcentaje de código cubierto por tests |

**Quality Gates:**

```
┌─────────────────────────────────────────────────────────┐
│              SONARQUBE QUALITY GATE                     │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Criterio                       │ Límite │ Estado       │
│  ───────────────────────────────┼────────┼────────────  │
│  Vulnerabilidades              │ 0      │ PASSED ✓     │
│  Bugs                          │ 0      │ PASSED ✓     │
│  Security Hotspots reviewed    │ 100%   │ PASSED ✓     │
│  Coverage                      │ 80%    │ FAILED ✗     │
│  Duplicación                   │ 3%     │ PASSED ✓     │
│  Technical debt ratio          │ 5%     │ PASSED ✓     │
│                                                         │
│  Resultado: FAILED (Coverage below threshold)           │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 7.7 Herramientas para APIs Específicas

| Herramienta | Tipo | Uso |
|-------------|------|-----|
| **Burp Suite** | DAST | Proxy interceptación, scanner de APIs REST |
| **Postman** | Testing | Colecciones de pruebas, Newman para CI/CD |
| **SoapUI** | DAST | Security scans para SOAP y REST |
| **OWASP ZAP** | DAST | Escaneo automático de APIs |
| **InQL** | Testing | Scanner de introspection GraphQL |
| **GraphQL Voyager** | Visualización | Ver el schema de GraphQL |
| **Altair** | Testing | Cliente GraphQL con autocompletado |
| **k8guard** | K8s Security | Auditoría de seguridad en Kubernetes |

---

## 8. SBOM - Software Bill of Materials

### 8.1 ¿Qué es un SBOM?

**SBOM (Software Bill of Materials)** es una lista detallada de todos los componentes, librerías y dependencias que forman parte de un software.

### Analogía: Ingredientes de un Producto

```
┌─────────────────────────────────────────────────────────┐
│                  SBOM = ETIQUETA DEL PRODUCTO            │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Producto alimenticio          Software                  │
│  ────────────────────          ────────                  │
│  Lista de ingredientes    →   Lista de dependencias      │
│  Valores nutricionales    →   Versiones de librerías     │
│  Alergenos                →   Vulnerabilidades conocidas │
│  Fecha de vencimiento     →   Fin de soporte             │
│  Fabricante               →   Proveedor/Mantenedor       │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 8.2 ¿Por qué es importante?

- **Log4Shell (2021):** Las empresas tardaron días en saber si usaban Log4j
- **Con un SBOM:** Sabes en minutos qué componentes usas y si son vulnerables
- **Regulatorio:** EO 14028 (EE.UU.) y regulaciones europeas lo requieren
- **Supply Chain:** Cada librería es un riesgo potencial

### 8.3 Formatos de SBOM

| Formato | Descripción | Herramienta |
|---------|-------------|-------------|
| **CycloneDX** | Estándar de OWASP, ligero | cyclonedx-cli |
| **SPDX** | Estándar Linux Foundation | spdx-tools |
| **SWID** | Estándar NIST | N/A |

### 8.4 Generar SBOM

**CycloneDX con Maven:**

```xml
<!-- pom.xml -->
<plugin>
    <groupId>org.cyclonedx</groupId>
    <artifactId>cyclonedx-maven-plugin</artifactId>
    <version>2.7.11</version>
    <executions>
        <execution>
            <phase>package</phase>
            <goals>
                <goal>makeAggregateBom</goal>
            </goals>
        </execution>
    </executions>
</plugin>
```

```bash
# Generar SBOM
mvn org.cyclonedx:cyclonedx-maven-plugin:makeAggregateBom

# El SBOM se genera en target/bom.xml y target/bom.json
```

**CycloneDX con Python:**

```bash
pip install cyclonedx-bom

# Generar SBOM de dependencias pip
cyclonedx-py -o sbom.json --format json

# Generar SBOM de requirements.txt
cyclonedx-py -i requirements.txt -o sbom.json
```

**CycloneDX con Node.js:**

```bash
npm install -g @cyclonedx/cyclonedx-npm

# Generar SBOM
cyclonedx-npm > sbom.json
```

**CycloneDX con Trivy:**

```bash
# Generar SBOM con Trivy
trivy fs --format cyclonedx -o sbom.json .

# Generar SBOM de imagen Docker
trivy image --format cyclonedx -o sbom.json python:3.11-slim
```

**SPDX con Tern (contenedores):**

```bash
pip install tern

# Generar SBOM SPDX de imagen
tern report -i python:3.11-slim -f spdxtagvalue -o sbom.spdx
```

### 8.5 Ejemplo de SBOM (CycloneDX JSON)

```json
{
  "bomFormat": "CycloneDX",
  "specVersion": "1.5",
  "metadata": {
    "timestamp": "2026-04-30T10:00:00Z",
    "tools": [{ "name": "cyclonedx-maven-plugin", "version": "2.7.11" }],
    "component": {
      "type": "application",
      "name": "mi-api-bancaria",
      "version": "1.0.0"
    }
  },
  "components": [
    {
      "type": "library",
      "name": "spring-core",
      "version": "5.3.18",
      "purl": "pkg:maven/org.springframework/spring-core@5.3.18",
      "licenses": [{ "license": { "id": "Apache-2.0" } }],
      "cpe": "cpe:2.3:a:vmware:spring_framework:5.3.18:*:*:*:*:*:*:*"
    },
    {
      "type": "library",
      "name": "log4j-core",
      "version": "2.14.1",
      "purl": "pkg:maven/org.apache.logging.log4j/log4j-core@2.14.1",
      "vulnerabilities": [
        {
          "id": "CVE-2021-44228",
          "severity": "critical",
          "cvssScore": 10.0
        }
      ]
    }
  ]
}
```

### 8.6 Analizar SBOM con Trivy

```bash
# Analizar SBOM en busca de vulnerabilidades
trivy sbom sbom.json

# Output
┌─────────────────────────────────────────────────────────┐
│ SBOM Analysis Results                                    │
├─────────────────────────────────────────────────────────┤
│ Componente              │ CVE              │ Severidad  │
│ ────────────────────────┼──────────────────┼─────────── │
│ log4j-core:2.14.1      │ CVE-2021-44228   │ CRITICAL   │
│ spring-core:5.3.18     │ CVE-2022-22965   │ HIGH       │
│ jackson-databind:2.13.1│ CVE-2022-42003   │ HIGH       │
│                                                         │
│ Found 3 vulnerabilities                                 │
└─────────────────────────────────────────────────────────┘
```

---

## 9. Pipeline CI/CD con Seguridad

### 9.1 El Ciclo de Seguridad en CI/CD

```
┌─────────────────────────────────────────────────────────────────┐
│                  PIPELINE CI/CD SEGURO                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────────┐ │
│  │  BUILD  │───▶│  TEST   │───▶│  SCAN   │───▶│   DEPLOY    │ │
│  │         │    │         │    │         │    │             │ │
│  │ Compilar│    │ Unit    │    │ SAST    │    │ Staging     │ │
│  │ código  │    │ Tests   │    │ SCA     │    │ Tests E2E   │ │
│  │         │    │ Integ.  │    │ SBOM    │    │ DAST        │ │
│  └─────────┘    └─────────┘    └─────────┘    └─────────────┘ │
│       │              │              │                │         │
│       ▼              ▼              ▼                ▼         │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────────┐ │
│  │ SonarQube│   │ Coverage│    │ Trivy   │    │ Production  │ │
│  │ SpotBugs│    │ > 80%   │    │ Semgrep │    │ Monitor     │ │
│  │         │    │         │    │ SBOM    │    │ Falco       │ │
│  └─────────┘    └─────────┘    └─────────┘    └─────────────┘ │
│                                                                 │
│  Si CUALQUIER scan falla → BUILD FAIL → No se despliega        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 9.2 Pipeline con Jenkins

```groovy
// Jenkinsfile - Pipeline CI/CD con Seguridad

pipeline {
    agent any

    environment {
        SONAR_HOST = 'http://localhost:9000'
        SONAR_TOKEN = credentials('sonar-token')
        TRIVY_SEVERITY = 'HIGH,CRITICAL'
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build') {
            steps {
                echo '=== COMPILANDO PROYECTO ==='
                sh 'mvn clean compile -DskipTests'
            }
        }

        stage('Unit Tests') {
            steps {
                echo '=== EJECUTANDO TESTS UNITARIOS ==='
                sh 'mvn test'
                junit 'target/surefire-reports/*.xml'
            }
        }

        stage('SonarQube Analysis') {
            steps {
                echo '=== ANÁLISIS SONARQUBE ==='
                sh """
                    mvn sonar:sonar \
                      -Dsonar.projectKey=mi-api-segura \
                      -Dsonar.host.url=${SONAR_HOST} \
                      -Dsonar.token=${SONAR_TOKEN}
                """
            }
        }

        stage('SpotBugs') {
            steps {
                echo '=== SPOTBUGS - ANÁLISIS DE BYTECODE ==='
                sh 'mvn spotbugs:spotbugs'
                archiveArtifacts 'target/spotbugsXml.xml'
                publishHTML([
                    reportDir: 'target/site/spotbugs',
                    reportFiles: 'spotbugs.html',
                    reportName: 'SpotBugs Report'
                ])
            }
        }

        stage('Semgrep - SAST') {
            steps {
                echo '=== SEMGREP - ANÁLISIS ESTÁTICO ==='
                sh 'semgrep scan --config auto --json -o semgrep-results.json .'
                archiveArtifacts 'semgrep-results.json'
            }
        }

        stage('OWASP Dependency Check - SCA') {
            steps {
                echo '=== OWASP DEPENDENCY CHECK ==='
                sh 'mvn org.owasp:dependency-check-maven:check'
                archiveArtifacts 'target/dependency-check-report.html'
                publishHTML([
                    reportDir: 'target',
                    reportFiles: 'dependency-check-report.html',
                    reportName: 'Dependency Check Report'
                ])
            }
        }

        stage('Trivy - Filesystem Scan') {
            steps {
                echo '=== TRIVY - ESCANEO DE FILESYSTEM ==='
                sh "trivy fs --severity ${TRIVY_SEVERITY} --format table ."
                sh "trivy fs --severity ${TRIVY_SEVERITY} --format json -o trivy-fs-results.json ."
                archiveArtifacts 'trivy-fs-results.json'
            }
        }

        stage('Generate SBOM') {
            steps {
                echo '=== GENERANDO SBOM ==='
                sh 'mvn org.cyclonedx:cyclonedx-maven-plugin:makeAggregateBom'
                sh 'trivy fs --format cyclonedx -o sbom-trivy.json .'
                archiveArtifacts 'target/bom.xml'
                archiveArtifacts 'target/bom.json'
                archiveArtifacts 'sbom-trivy.json'
            }
        }

        stage('Analyze SBOM') {
            steps {
                echo '=== ANALIZANDO SBOM ==='
                sh 'trivy sbom target/bom.json --severity HIGH,CRITICAL'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo '=== CONSTRUYENDO IMAGEN DOCKER ==='
                sh 'docker build -t mi-api-segura:${BUILD_NUMBER} .'
            }
        }

        stage('Trivy - Docker Image Scan') {
            steps {
                echo '=== TRIVY - ESCANEO DE IMAGEN ==='
                sh "trivy image --severity ${TRIVY_SEVERITY} mi-api-segura:${BUILD_NUMBER}"
                sh "trivy image --severity ${TRIVY_SEVERITY} --format json -o trivy-image-results.json mi-api-segura:${BUILD_NUMBER}"
                archiveArtifacts 'trivy-image-results.json'
            }
        }

        stage('Quality Gate') {
            steps {
                echo '=== QUALITY GATE ==='
                echo 'Verificar que todos los scans pasaron'
                echo 'Si algún scan encontró vulnerabilidades críticas → FAIL'
            }
        }

        stage('Deploy to Staging') {
            steps {
                echo '=== DEPLOY A STAGING ==='
                sh "docker run -d --name api-staging -p 8080:8080 mi-api-segura:${BUILD_NUMBER}"
            }
        }

        stage('DAST - OWASP ZAP') {
            steps {
                echo '=== DAST - OWASP ZAP ==='
                sh """
                    docker run -v \$(pwd):/zap/wrk/:rw \
                      ghcr.io/zaproxy/zaproxy:stable \
                      zap-api-scan.py -t http://host.docker.internal:8080/api/v1/openapi.json \
                      -f openapi -r zap-report.html
                """
                archiveArtifacts 'zap-report.html'
            }
        }

        stage('Deploy to Production') {
            when {
                branch 'main'
            }
            steps {
                echo '=== DEPLOY A PRODUCCIÓN ==='
                echo 'Solo si todos los scans pasaron y es rama main'
                sh "docker run -d --name api-prod -p 443:8080 mi-api-segura:${BUILD_NUMBER}"
            }
        }
    }

    post {
        always {
            echo '=== LIMPIEZA ==='
            cleanWs()
        }
        success {
            echo 'Pipeline exitoso - Todos los controles de seguridad pasaron'
        }
        failure {
            echo 'Pipeline fallido - Revisar logs de seguridad'
            mail to: 'equipo-seguridad@empresa.com',
                 subject: "Pipeline FALLIDO - Build #${BUILD_NUMBER}",
                 body: "Revisar Jenkins: ${env.BUILD_URL}"
        }
    }
}
```

### 9.3 Pipeline Visual - Flujo de Seguridad

```
┌─────────────────────────────────────────────────────────────────┐
│                    FLUJO DE SEGURIDAD CI/CD                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Developer                                                      │
│     │                                                           │
│     │ git push                                                  │
│     ▼                                                           │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ JENKINS PIPELINE                                        │   │
│  │                                                         │   │
│  │  1. BUILD                                               │   │
│  │     └── mvn clean compile                               │   │
│  │                                                         │   │
│  │  2. UNIT TESTS                                          │   │
│  │     └── mvn test (coverage > 80%)                       │   │
│  │                                                         │   │
│  │  3. SONARQUBE                                           │   │
│  │     ├── Vulnerabilidades = 0                            │   │
│  │     ├── Bugs = 0                                        │   │
│  │     ├── Security Hotspots reviewed = 100%               │   │
│  │     └── Coverage > 80%                                  │   │
│  │                                                         │   │
│  │  4. SPOTBUGS                                            │   │
│  │     └── Bugs de seguridad en bytecode                   │   │
│  │                                                         │   │
│  │  5. SEMGREP                                             │   │
│  │     └── semgrep scan --config auto                      │   │
│  │                                                         │   │
│  │  6. OWASP DEPENDENCY CHECK                              │   │
│  │     └── mvn org.owasp:dependency-check-maven:check      │   │
│  │                                                         │   │
│  │  7. TRIVY FILESYSTEM                                    │   │
│  │     └── trivy fs --severity HIGH,CRITICAL               │   │
│  │                                                         │   │
│  │  8. GENERAR SBOM                                        │   │
│  │     └── cyclonedx-maven-plugin                          │   │
│  │                                                         │   │
│  │  9. ANALIZAR SBOM                                       │   │
│  │     └── trivy sbom bom.json                             │   │
│  │                                                         │   │
│  │  10. BUILD DOCKER IMAGE                                 │   │
│  │      └── docker build                                   │   │
│  │                                                         │   │
│  │  11. TRIVY IMAGE                                        │   │
│  │      └── trivy image --severity HIGH,CRITICAL           │   │
│  │                                                         │   │
│  │  12. DEPLOY STAGING                                     │   │
│  │                                                         │   │
│  │  13. DAST (OWASP ZAP)                                   │   │
│  │      └── zap-api-scan.py                                │   │
│  │                                                         │   │
│  │  14. DEPLOY PRODUCTION (solo si todo pasó)              │   │
│  │                                                         │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  Si CUALQUIER paso falla → BUILD FAIL → No deploy              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 9.4 Resumen de Herramientas en el Pipeline

| Etapa | Herramienta | Qué detecta |
|-------|------------|-------------|
| **SAST** | Semgrep, SonarQube, SpotBugs | Bugs, vulnerabilidades en código |
| **SCA** | OWASP Dependency Check, Trivy | Dependencias vulnerables |
| **SBOM** | CycloneDX | Inventario de componentes |
| **Container** | Trivy image | Vulnerabilidades en imagen Docker |
| **DAST** | OWASP ZAP | Vulnerabilidades en API en ejecución |
| **IaC** | Trivy config | Errores en Terraform/K8s |

---

## 10. Ataques Conocidos por Tipo de API

### 10.1 Tabla Comparativa de Ataques

| Ataque | REST | GraphQL | SOAP |
|--------|------|---------|------|
| **BOLA** | ✅ Muy común | ✅ Común | ⚠️ Posible |
| **SQL Injection** | ✅ Común | ⚠️ Posible | ⚠️ Posible |
| **XSS** | ✅ Común | ⚠️ Posible | ❌ Raro |
| **XXE** | ❌ Raro | ❌ Raro | ✅ Muy común |
| **XML Bomb** | ❌ No aplica | ❌ No aplica | ✅ Común |
| **Query Depth** | ❌ No aplica | ✅ Muy común | ❌ No aplica |
| **Query Complexity** | ❌ No aplica | ✅ Muy común | ❌ No aplica |
| **Batch Attack** | ⚠️ Posible | ✅ Común | ❌ No aplica |
| **Introspection** | ❌ No aplica | ✅ Común | ⚠️ WSDL |
| **SSRF** | ✅ Común | ✅ Común | ⚠️ Posible |
| **Rate Limit Bypass** | ✅ Común | ✅ Común | ⚠️ Posible |
| **Replay Attack** | ⚠️ Sin nonce | ⚠️ Sin nonce | ✅ Con WS-Security |

### 10.2 Diagrama de Ataque: BOLA en REST

```
1. Usuario legítimo se loguea → recibe JWT
2. Hace request normal: GET /api/pedidos/123 → ve su pedido
3. Atacante modifica el ID: GET /api/pedidos/124 → ve pedido de OTRA persona
4. Automatiza con Intruder: id de 1 a 10000 → TODOS los pedidos expuestos
```

### 10.3 Diagrama de Ataque: XXE en SOAP

```
1. Atacante craft XML malicioso con entidad externa
2. Servidor parsea el XML → resuelve entidad → lee archivo del sistema
3. Respuesta incluye contenido del archivo comprometido
```

### 10.4 Diagrama de Ataque: Query Depth en GraphQL

```
1. Schema tiene relaciones circulares: Usuario → Amigos → Usuarios
2. Atacante envía query profundamente anidada (5+ niveles)
3. Exponencial: 100^5 = 10 billones de objetos a resolver
4. CPU 100%, memoria agotada → servidor cae (DoS)
```

---

## 11. Comparación de Vulnerabilidades

### 11.1 Nivel de Riesgo por Tipo de API

```
REST:      ████████████████████████████░░  Muy alto
           - Más expuesto (más endpoints)
           - BOLA es el #1

GraphQL:   ████████████████████████░░░░  Alto
           - Un solo endpoint = más difícil de mapear
           - Pero introspection da todo el schema

SOAP:      ████████████████████░░░░░░░░  Medio-Alto
           - Contrato estricto (WSDL) limita ataques
           - Pero XXE y XML Bomb son muy efectivos
```

### 11.2 Protecciones Cruzadas

| Protección | REST | GraphQL | SOAP |
|-----------|------|---------|------|
| HTTPS/TLS | ✅ | ✅ | ✅ |
| Autenticación | ✅ JWT/OAuth | ✅ JWT/OAuth | ✅ WS-Security |
| Rate Limiting | ✅ | ✅ | ✅ |
| Input Validation | ✅ | ✅ | ✅ |
| Logging | ✅ | ✅ | ✅ |
| Error Handling | ✅ | ✅ | ✅ |

---

## 12. Referencias

| Recurso | URL |
|---------|-----|
| OWASP API Security Top 10 | https://owasp.org/API-Security/editions/2023/en/0x00-toc/ |
| REST Security Cheat Sheet | https://cheatsheetseries.owasp.org/cheatsheets/REST-Security-Cheat-Sheet.html |
| GraphQL Security | https://graphql.org/learn/security/ |
| WS-Security | https://www.oasis-open.org/standards#wssecurity |
| XXE Prevention | https://cheatsheetseries.owasp.org/cheatsheets/XML_External_Entity_Prevention_Cheat_Sheet.html |
| Semgrep Docs | https://semgrep.dev/docs/ |
| Trivy Docs | https://aquasecurity.github.io/trivy/ |
| SonarQube Docs | https://docs.sonarsource.com/sonarqube/ |
| OWASP Dependency Check | https://jeremylong.github.io/DependencyCheck/ |
| CycloneDX | https://cyclonedx.org/ |
| SBOM Framework | https://www.ntia.gov/sbom |
| Jenkins Pipeline | https://www.jenkins.io/doc/book/pipeline/ |

---

*Documento creado exclusivamente con fines educativos. Parte del curso de ciberseguridad.*
