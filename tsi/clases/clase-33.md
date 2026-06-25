# Clase 33: SAST - Static Application Security Testing

**Numero de clase:** 23
**Duracion:** 2 horas

## Objetivos de Aprendizaje

- Comprender que es SAST y como funciona (analisis de codigo sin ejecucion)
- Usar herramientas SAST: Bandit, Semgrep, SonarQube
- Diferenciar falsos positivos de verdaderos positivos
- Integrar SAST en IDE y CI/CD
- Crear reglas personalizadas de Semgrep para detectar vulnerabilidades

## Contenido Detallado

### 1. Que es SAST?

SAST (Static Application Security Testing) analiza el codigo fuente, bytecode o binarios de una aplicacion SIN ejecutarlos, buscando patrones que indican vulnerabilidades de seguridad.

**Caracteristicas:**
- White-box testing: tiene acceso completo al codigo fuente
- Se ejecuta temprano en el ciclo de desarrollo (Shift-Left)
- Detecta vulnerabilidades en tiempo de escritura de codigo
- Escalable a proyectos grandes

**Lo que detecta:**
- Inyecciones (SQL, Command, LDAP, XML)
- Cross-Site Scripting (XSS)
- Buffer overflows
- Hardcoded secrets
- Uso de funciones peligrosas
- Configuracion insegura
- Validacion incorrecta de entradas

### 2. Herramientas SAST Populares

| Herramienta | Lenguaje | Tipo | Caracteristicas |
|------------|----------|------|-----------------|
| SonarQube | Multi-lenguaje | Comercial/Community | Analisis continuo, deuda tecnica, quality gates |
| Semgrep | Multi-lenguaje | Open Source | Reglas custom, patrones, integracion CI/CD |
| Bandit | Python | Open Source | Disenado para Python, OWASP Top 10 |
| FindSecBugs | Java (FindBugs plugin) | Open Source | Seguridad para Java/Kotlin |
| Brakeman | Ruby on Rails | Open Source | Especializado en Rails |
| Checkmarx | Multi-lenguaje | Comercial | Cobertura amplia, correlacion de flujos |
| Fortify | Multi-lenguaje | Comercial | Analisis profundo, cumplimiento normativo |

### 3. Falsos Positivos vs. Verdaderos Positivos

| Tipo | Descripcion | Que hacer |
|------|-------------|-----------|
| Verdadero Positivo (TP) | Vulnerabilidad real | Corregir inmediatamente |
| Falso Positivo (FP) | No es vulnerabilidad, el analisis se equivoco | Marcar como falso positivo |
| Verdadero Negativo (TN) | No hay vulnerabilidad y el analisis no reporto | Correcto, sin accion |
| Falso Negativo (FN) | Hay vulnerabilidad pero el analisis no la detecto | El peor caso, mejorar reglas |

**Como reducir falsos positivos:**
- Ajustar niveles de confianza (confidence level)
- Usar reglas especificas del proyecto
- Combinar con revision manual
- Mantener una base de conocimiento de FP conocidos

### 4. SAST vs SCA vs DAST

| Aspecto | SAST | SCA | DAST |
|---------|------|-----|------|
| Que analiza | Codigo fuente | Dependencias | App en ejecucion |
| Cuando | Build/Commit | Build | Testing/Staging |
| Perspectiva | White-box | Componentes | Black-box |
| Detecta | Vulnerabilidades en codigo propio | CVEs en librerias de terceros | Vulnerabilidades en entorno y config |
| Falsos positivos | Altos | Bajos | Medios |

### 5. Integracion en IDE y CI/CD

**IDE:**
- SonarLint (VSCode, IntelliJ, Eclipse)
- Semgrep VSCode Extension
- Bandit como plugin en linter (flake8-bandit)

**CI/CD:**
- GitHub Actions: `semgrep-action`, `bandit-action`
- GitLab CI/CD: `semgrep.gitlab-ci.yml`
- Jenkins: Plugins de SonarQube, Semgrep

## Ejercicio 1: Proyecto Python Vulnerable + Ejecutar Bandit

```python
# proyecto_vulnerable.py - Proyecto con vulnerabilidades para analisis SAST
import hashlib
import os
import subprocess
import sqlite3
import pickle
import yaml
import requests

# ============================================================
# VULNERABILIDAD 1: Hash inseguro (MD5)
# ============================================================

def hash_contrasena_md5(contrasena):
    """Vulnerabilidad: MD5 es debil para contrasenas."""
    return hashlib.md5(contrasena.encode()).hexdigest()


# ============================================================
# VULNERABILIDAD 2: Inyeccion SQL
# ============================================================

def buscar_usuario(nombre):
    """Vulnerabilidad: concatenacion directa en consulta SQL."""
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()

    query = f"SELECT * FROM usuarios WHERE nombre = '{nombre}'"
    cursor.execute(query)  # Inyeccion SQL

    return cursor.fetchall()


# ============================================================
# VULNERABILIDAD 3: Command Injection
# ============================================================

def ejecutar_comando(comando):
    """Vulnerabilidad: ejecuta comandos sin validar."""
    resultado = subprocess.check_output(comando, shell=True)
    return resultado.decode()


# ============================================================
# VULNERABILIDAD 4: Hardcoded password
# ============================================================

DB_PASSWORD = "admin123"  # Contrasena hardcodeada

def conectar_bd():
    """Usa contrasena hardcodeada."""
    conn = sqlite3.connect(f'db://admin:{DB_PASSWORD}@localhost:5432/prod')
    return conn


# ============================================================
# VULNERABILIDAD 5: Pickle inseguro
# ============================================================

def cargar_datos(archivo):
    """Pickle puede ejecutar codigo arbitrario al deserializar."""
    with open(archivo, 'rb') as f:
        return pickle.load(f)  # Inseguro


# ============================================================
# VULNERABILIDAD 6: Uso de eval
# ============================================================

def evaluar_expresion(expresion):
    """eval() ejecuta codigo Python arbitrario."""
    return eval(expresion)


# ============================================================
# VULNERABILIDAD 7: YAML unsafe load
# ============================================================

def cargar_config_yaml(archivo):
    """yaml.load() sin Loader seguro puede ejecutar codigo."""
    with open(archivo, 'r') as f:
        return yaml.load(f)  # yaml.safe_load() es seguro


# ============================================================
# VULNERABILIDAD 8: HTTP en lugar de HTTPS
# ============================================================

def obtener_datos():
    """HTTP sin TLS expone datos en transito."""
    response = requests.get('http://api-insegura.com/data')  # HTTP no HTTPS
    return response.json()


# ============================================================
# VULNERABILIDAD 9: Path Traversal
# ============================================================

def leer_archivo(nombre):
    """Path traversal: no valida que el archivo este en el directorio permitido."""
    with open(nombre, 'r') as f:
        return f.read()


# ============================================================
# VULNERABILIDAD 10: Assert usado como validacion
# ============================================================

def validar_usuario(usuario):
    """assert se desactiva con -O, no es seguro para validacion."""
    assert usuario.rol == 'admin', "No autorizado"  # No usar assert para seguridad
    return True


if __name__ == '__main__':
    print("Proyecto vulnerable para analisis SAST con Bandit")

    # Pruebas (no ejecutar en produccion)
    print(hash_contrasena_md5("test"))
    print(ejecutar_comando("echo test"))
    print(evaluar_expresion("1+1"))
```

**Comandos para analizar con Bandit:**
```bash
# Instalar Bandit
pip install bandit

# 1. Escaneo basico
bandit -r .

# 2. Escaneo con nivel de confianza especifico
bandit -r . --confidence-level high --severity-level high

# 3. Escaneo con formato JSON (para procesamiento)
bandit -r . -f json -o bandit-report.json

# 4. Escaneo excluyendo ciertos tests
bandit -r . --skip B101,B105,B108

# 5. Escaneo con contexto y linea de codigo
bandit -r . -ll -ii -n 5

# 6. Reporte HTML
bandit -r . -f html -o bandit-report.html
```

**Interpretacion del reporte de Bandit:**
```
>> Issue: [B303:blacklist] Use of insecure MD4, MD5, or SHA1 hash function.
   Severity: Medium   Confidence: High
   Location: proyecto_vulnerable.py:13
   12  def hash_contrasena_md5(contrasena):
   13      return hashlib.md5(contrasena.encode()).hexdigest()

>> Issue: [B611:sql_injection] Possible SQL injection vector through string-based query construction.
   Severity: Medium   Confidence: High
   Location: proyecto_vulnerable.py:24
   23      query = f"SELECT * FROM usuarios WHERE nombre = '{nombre}'"
   24      cursor.execute(query)

>> Issue: [B602:subprocess_popen_with_shell_equals_true] subprocess call with shell=True seems safe...
   Severity: High   Confidence: High
   Location: proyecto_vulnerable.py:33
   32  def ejecutar_comando(comando):
   33      resultado = subprocess.check_output(comando, shell=True)

>> Issue: [B105:hardcoded_password_string] Possible hardcoded password: 'admin123'
   Severity: Medium   Confidence: Medium
   Location: proyecto_vulnerable.py:41
   41  DB_PASSWORD = "admin123"

>> Issue: [B301:pickle] Pickle and modules that wrap it can be unsafe...
   Severity: Medium   Confidence: High
   Location: proyecto_vulnerable.py:51
   51      return pickle.load(f)

>> Issue: [B307:eval] Use of possibly insecure function - consider using safer ast.literal_eval.
   Severity: Medium   Confidence: High
   Location: proyecto_vulnerable.py:60
   60      return eval(expresion)

>> Issue: [B506:yaml_load] Use of yaml.load() without a Loader parameter...
   Severity: Medium   Confidence: High
   Location: proyecto_vulnerable.py:69
   69      return yaml.load(f)
```

```python
# proyecto_corregido.py - Version corregida del codigo vulnerable
import hashlib
import os
import subprocess
import sqlite3
import json
import yaml
import requests
from ast import literal_eval

# ============================================================
# CORRECCION 1: Hash seguro con bcrypt/argon2
# ============================================================

import bcrypt

def hash_contrasena(contrasena):
    """OK: Usa bcrypt con salt y factor de costo."""
    return bcrypt.hashpw(
        contrasena.encode(),
        bcrypt.gensalt(rounds=12)
    ).decode()


# ============================================================
# CORRECCION 2: SQL parametrizado
# ============================================================

def buscar_usuario_seguro(nombre):
    """OK: Usa parametros en lugar de concatenacion."""
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM usuarios WHERE nombre = ?",
        (nombre,)
    )
    return cursor.fetchall()


# ============================================================
# CORRECCION 3: Sin shell=True
# ============================================================

def ejecutar_comando_seguro(lista_comandos):
    """OK: Usa lista en lugar de string y shell=False."""
    resultado = subprocess.check_output(lista_comandos, shell=False)
    return resultado.decode()


# ============================================================
# CORRECCION 4: Secretos desde entorno
# ============================================================

def conectar_bd_segura():
    """OK: Lee credenciales de variables de entorno."""
    db_host = os.environ.get('DB_HOST', 'localhost')
    db_user = os.environ.get('DB_USER', 'app')
    db_pass = os.environ.get('DB_PASSWORD', '')

    if not db_pass:
        raise ValueError("DB_PASSWORD no configurada en variables de entorno")

    conn = sqlite3.connect(f'db://{db_user}:****@{db_host}:5432/prod')
    return conn


# ============================================================
# CORRECCION 5: JSON en lugar de Pickle
# ============================================================

def cargar_datos_seguro(archivo):
    """OK: JSON no ejecuta codigo arbitrario."""
    with open(archivo, 'r') as f:
        return json.load(f)


# ============================================================
# CORRECCION 6: literal_eval en lugar de eval
# ============================================================

def evaluar_expresion_segura(expresion):
    """OK: literal_eval solo evalua literales, no ejecuta codigo."""
    try:
        return literal_eval(expresion)
    except (ValueError, SyntaxError):
        return None


# ============================================================
# CORRECCION 7: yaml.safe_load
# ============================================================

def cargar_config_yaml_seguro(archivo):
    """OK: safe_load no permite ejecucion de codigo."""
    with open(archivo, 'r') as f:
        return yaml.safe_load(f)


# ============================================================
# CORRECCION 8: HTTPS
# ============================================================

def obtener_datos_seguro():
    """OK: Usa HTTPS para cifrar la comunicacion."""
    response = requests.get('https://api-segura.com/data')
    return response.json()


# ============================================================
# CORRECCION 9: Path traversal prevenido
# ============================================================

DIRECTORIO_BASE = os.path.abspath('data')

def leer_archivo_seguro(nombre):
    """OK: Valida que el archivo este dentro del directorio permitido."""
    # Sanitizar path
    ruta = os.path.normpath(os.path.join(DIRECTORIO_BASE, nombre))

    # Verificar que este dentro del directorio base
    if not ruta.startswith(DIRECTORIO_BASE):
        raise PermissionError("Acceso denegado: fuera del directorio permitido")

    if not os.path.exists(ruta):
        raise FileNotFoundError("Archivo no encontrado")

    with open(ruta, 'r') as f:
        return f.read()


# ============================================================
# CORRECCION 10: Validacion explicita
# ============================================================

def validar_usuario_seguro(usuario):
    """OK: Validacion explicita, no depende de assert."""
    if not hasattr(usuario, 'rol'):
        return False
    if usuario.rol != 'admin':
        return False
    return True
```

## Ejercicio 2: Reglas Personalizadas de Semgrep para Detectar Hardcoded Passwords

```yaml
# semgrep-rules/hardcoded-passwords.yaml
# Reglas Semgrep personalizadas para detectar secretos hardcodeados

rules:
  # =============================================
  # Regla 1: Contrasenas en variables
  # =============================================
  - id: hardcoded-password-variable
    pattern-either:
      - pattern: |
          $VAR = "..."
      - pattern: |
          $VAR = '...'
    patterns:
      - metavariable-regex:
          metavariable: $VAR
          regex: (?i).*(password|passwd|pwd|secret|api_key|apikey).*
      - metavariable-regex:
          metavariable: $VAL
          regex: (?i).*(password|passwd|pwd|secret|api_key|apikey).*
    message: >
      Posible secreto hardcodeado encontrado en la variable $VAR.
      Los secretos deben leerse de variables de entorno o
      un gestor de secretos (Vault, Azure Key Vault).
    severity: ERROR
    languages:
      - python
      - javascript
      - typescript
      - java
      - go
      - ruby
    metadata:
      category: security
      cwe: "CWE-798: Use of Hard-coded Credentials"
      owasp: "A2:2021 - Cryptographic Failures"

  # =============================================
  # Regla 2: Contrasenas en diccionarios de configuracion
  # =============================================
  - id: hardcoded-password-dict
    pattern-either:
      - pattern: |
          {
            ...,
            "$KEY": "...",
            ...
          }
      - pattern: |
          {
            ...,
            '$KEY': '...',
            ...
          }
    patterns:
      - metavariable-regex:
          metavariable: $KEY
          regex: (?i).*(password|passwd|secret|api_key|apikey|token|secret_key).*
      - metavariable-regex:
          metavariable: $VAL
          regex: (?i).*(password|passwd|secret|api_key|apikey|token|secret_key).*
    message: >
      Secreto hardcodeado encontrado en diccionario de configuracion.
      Usa variables de entorno o un gestor de secretos.
    severity: ERROR
    languages:
      - python
      - javascript
      - typescript
      - java
      - ruby

  # =============================================
  # Regla 3: Conexion a BD con contrasena en texto plano
  # =============================================
  - id: hardcoded-db-connection-string
    patterns:
      - pattern-either:
          - pattern: |
              $FUNC("$URL", ...)
          - pattern: |
              $FUNC('$URL', ...)
      - metavariable-regex:
          metavariable: $URL
          regex: (?i).*(postgres|mysql|mongodb|sqlite|oracle)://.*:.*@.*
    message: >
      Conexion a base de datos con credenciales en texto plano
      en la URL de conexion. Las credenciales deben pasarse
      por parametros separados desde variables de entorno.
    severity: WARNING
    languages:
      - python
      - javascript
      - typescript
      - java
      - go

  # =============================================
  # Regla 4: Funciones criptograficas debiles
  # =============================================
  - id: weak-crypto-md5-sha1
    pattern-either:
      - pattern: hashlib.md5(...)
      - pattern: hashlib.sha1(...)
      - pattern: Crypto.Cipher.DES(...)
      - pattern: Crypto.Cipher.ARC4(...)
    message: >
      Uso de algoritmo criptografico debil. MD5 y SHA-1 tienen
      colisiones demostradas. DES y RC4 son vulnerables.
      Usa SHA-256/3 para hash, AES-GCM para cifrado.
    severity: ERROR
    languages:
      - python
    metadata:
      cwe: "CWE-327: Use of a Broken or Risky Cryptographic Algorithm"

  # =============================================
  # Regla 5: SQL Injection detectado
  # =============================================
  - id: sql-injection-concatenation
    pattern-either:
      - pattern: |
          $DB.execute("..." + $VAR + "...")
      - pattern: |
          $DB.execute(f"...{$VAR}...")
      - pattern: |
          $DB.execute('...' + $VAR + '...')
    message: >
      Posible inyeccion SQL detectada. No concatenes variables
      en queries SQL. Usa consultas parametrizadas (? o %s).
    severity: ERROR
    languages:
      - python
    metadata:
      cwe: "CWE-89: SQL Injection"
      owasp: "A3:2021 - Injection"

  # =============================================
  # Regla 6: Debug/INFO en produccion
  # =============================================
  - id: debug-enabled-production
    patterns:
      - pattern: |
          app.run(debug=True, ...)
    message: >
      Modo DEBUG activado. No usar debug=True en produccion.
      Expone stack traces al usuario y permite ejecucion
      remota de codigo.
    severity: ERROR
    languages:
      - python

  # =============================================
  # Regla 7: eval() detectado
  # =============================================
  - id: dangerous-eval
    pattern: eval(...)
    message: >
      Uso de eval() detectado. eval() ejecuta codigo Python
      arbitrario. Usa ast.literal_eval() si necesitas evaluar
      literales, o parseadores especificos.
    severity: ERROR
    languages:
      - python
    metadata:
      cwe: "CWE-95: Eval Injection"
```

**Como ejecutar las reglas personalizadas:**
```bash
# Ejecutar Semgrep con reglas personalizadas
semgrep --config=semgrep-rules/hardcoded-passwords.yaml --error --strict .

# Ejecutar con output JSON
semgrep --config=semgrep-rules/hardcoded-passwords.yaml --json -o semgrep-hallazgos.json .

# Ejecutar combinando reglas personalizadas y publicas
semgrep --config=semgrep-rules/ --config=p/owasp-top-ten --config=p/python .

# Ejecutar en modo CI (solo mostrar hallazgos)
semgrep --config=semgrep-rules/hardcoded-passwords.yaml --ci .
```

## Ejercicio 3: Analisis y Correccion de Reporte SonarQube

```python
# sonarqube_analysis.py - Script para procesar reporte de SonarQube
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AnalizadorSonarQube:
    """
    Procesa un reporte de SonarQube en formato JSON y prioriza
    las vulnerabilidades para correccion.
    """

    def __init__(self, reporte_json: str):
        with open(reporte_json, 'r') as f:
            self.reporte = json.load(f)

    def priorizar_vulnerabilidades(self) -> list:
        """
        Prioriza vulnerabilidades por severidad y tipo.
        Retorna lista ordenada por criticidad.
        """
        issues = self.reporte.get('issues', [])

        prioridad = {
            'BLOCKER': 0,
            'CRITICAL': 1,
            'MAJOR': 2,
            'MINOR': 3,
            'INFO': 4
        }

        vulnerabilidades = []
        for issue in issues:
            if issue.get('type') == 'VULNERABILITY':
                vulnerabilidades.append({
                    'severidad': issue.get('severity', 'INFO'),
                    'mensaje': issue.get('message', ''),
                    'archivo': issue.get('component', ''),
                    'linea': issue.get('line', 0),
                    'regla': issue.get('rule', ''),
                    'prioridad': prioridad.get(
                        issue.get('severity', 'INFO'), 99
                    ),
                    'esfuerzo': issue.get('effort', '0min')
                })

        vulnerabilidades.sort(key=lambda x: x['prioridad'])
        return vulnerabilidades

    def resumen_ejecutivo(self) -> dict:
        """Genera resumen del reporte."""
        issues = self.reporte.get('issues', [])

        resumen = {
            'total_issues': len(issues),
            'total_vulnerabilidades': 0,
            'total_bugs': 0,
            'total_code_smells': 0,
            'por_severidad': {'BLOCKER': 0, 'CRITICAL': 0,
                             'MAJOR': 0, 'MINOR': 0, 'INFO': 0},
            'por_tipo': {}
        }

        for issue in issues:
            tipo = issue.get('type', 'UNKNOWN')
            severidad = issue.get('severity', 'INFO')

            resumen['por_severidad'][severidad] = \
                resumen['por_severidad'].get(severidad, 0) + 1

            if tipo == 'VULNERABILITY':
                resumen['total_vulnerabilidades'] += 1
            elif tipo == 'BUG':
                resumen['total_bugs'] += 1
            elif tipo == 'CODE_SMELL':
                resumen['total_code_smells'] += 1

            resumen['por_tipo'][tipo] = \
                resumen['por_tipo'].get(tipo, 0) + 1

        return resumen


# ============================================================
# EJEMPLO DE REPORTE SIMULADO DE SONARQUBE
# ============================================================

reporte_ejemplo = {
    "issues": [
        {
            "type": "VULNERABILITY",
            "severity": "BLOCKER",
            "message": "Use of hardcoded password in database connection",
            "component": "src/database.py",
            "line": 42,
            "rule": "python:S1313",
            "effort": "5min"
        },
        {
            "type": "VULNERABILITY",
            "severity": "CRITICAL",
            "message": "Make sure using the literal expression is safe here",
            "component": "src/utils.py",
            "line": 15,
            "rule": "python:S1523",
            "effort": "2min"
        },
        {
            "type": "VULNERABILITY",
            "severity": "MAJOR",
            "message": "Use of MD5 hash function is not recommended",
            "component": "src/auth.py",
            "line": 23,
            "rule": "python:S2070",
            "effort": "10min"
        },
        {
            "type": "BUG",
            "severity": "MAJOR",
            "message": "This function does not return a value in all paths",
            "component": "src/process.py",
            "line": 87,
            "rule": "python:S935",
            "effort": "5min"
        },
        {
            "type": "VULNERABILITY",
            "severity": "MINOR",
            "message": "Use of assert without error message",
            "component": "src/validators.py",
            "line": 34,
            "rule": "python:S1871",
            "effort": "1min"
        },
        {
            "type": "VULNERABILITY",
            "severity": "CRITICAL",
            "message": "This code uses SQL concatenation instead of prepared statements",
            "component": "src/queries.py",
            "line": 55,
            "rule": "python:S2077",
            "effort": "15min"
        },
        {
            "type": "CODE_SMELL",
            "severity": "MAJOR",
            "message": "Function has too many parameters (8 > 5)",
            "component": "src/handlers.py",
            "line": 120,
            "rule": "python:S107",
            "effort": "20min"
        }
    ]
}


def corregir_vulnerabilidades_prioritarias():
    """
    Demostracion de correccion de las 5 vulnerabilidades
    mas criticas del reporte.
    """
    analizador = AnalizadorSonarQube(reporte_ejemplo)
    resumen = analizador.resumen_ejecutivo()

    logger.info("RESUMEN DEL REPORTE SONARQUBE:")
    logger.info(f"  Total issues: {resumen['total_issues']}")
    logger.info(f"  Vulnerabilidades: {resumen['total_vulnerabilidades']}")
    logger.info(f"  Bugs: {resumen['total_bugs']}")
    logger.info(f"  Code Smells: {resumen['total_code_smells']}")
    logger.info(f"  Por severidad: {resumen['por_severidad']}")

    priorizadas = analizador.priorizar_vulnerabilidades()

    logger.info("\nTOP 5 VULNERABILIDADES A CORREGIR:")
    for i, vuln in enumerate(priorizadas[:5], 1):
        logger.info(f"\n  {i}. [{vuln['severidad']}] {vuln['mensaje']}")
        logger.info(f"     Archivo: {vuln['archivo']}:{vuln['linea']}")
        logger.info(f"     Esfuerzo estimado: {vuln['esfuerzo']}")
        logger.info(f"     Regla: {vuln['regla']}")

    # Plan de accion
    logger.info("\n--- PLAN DE ACCION ---")
    logger.info("""
    1. BLOCKER - Contrasena hardcodeada (database.py:42)
       ACCION: Mover a variable de entorno/Vault.
       CODIGO:
         # Antes: DB_PASSWORD = "admin123"
         # Despues: DB_PASSWORD = os.environ['DB_PASSWORD']

    2. CRITICAL - eval() en utils.py:15
       ACCION: Reemplazar con ast.literal_eval().
       CODIGO:
         # Antes: resultado = eval(expresion)
         # Despues: resultado = ast.literal_eval(expresion)

    3. CRITICAL - SQL concatenation (queries.py:55)
       ACCION: Usar consultas parametrizadas.
       CODIGO:
         # Antes: cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
         # Despues: cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))

    4. MAJOR - MD5 hash (auth.py:23)
       ACCION: Reemplazar con bcrypt o Argon2.
       CODIGO:
         # Antes: hashlib.md5(password.encode()).hexdigest()
         # Despues: bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    5. MINOR - assert sin mensaje (validators.py:34)
       ACCION: Reemplazar con validacion explicita.
       CODIGO:
         # Antes: assert user.is_admin
         # Despues: if not user.is_admin: raise PermissionError("No autorizado")
    """)


if __name__ == '__main__':
    # Simular el reporte de SonarQube
    with open('sonarqube-report.json', 'w') as f:
        json.dump(reporte_ejemplo, f, indent=2)

    corregir_vulnerabilidades_prioritarias()
```

## Preguntas y Respuestas

**P1: Que es SAST y en que se diferencia de DAST?**
R: SAST (Static Application Security Testing) analiza el codigo fuente sin ejecutarlo, detectando vulnerabilidades en el codigo mismo. DAST (Dynamic Application Security Testing) analiza la aplicacion en ejecucion desde afuera. SAST es white-box (ve el codigo completo) y funciona temprano en el ciclo; DAST es black-box (solo ve respuestas HTTP) y requiere la app desplegada.

**P2: Que es un falso positivo en SAST y como se maneja?**
R: Un falso positivo es un resultado que SAST marca como vulnerabilidad pero que en realidad no lo es en el contexto del proyecto. Se maneja: (1) verificando manualmente el resultado, (2) marcandolo como falso positivo en la herramienta, (3) ajustando las reglas para reducir ruido, (4) manteniendo un registro de FP conocidos.

**P3: Cual es la diferencia entre SAST y SCA?**
R: SAST analiza el codigo fuente propio de la aplicacion en busca de vulnerabilidades de diseno e implementacion. SCA (Software Composition Analysis) analiza las dependencias y librerias de terceros en busca de vulnerabilidades conocidas (CVE). SAST usa analisis de patrones y flujo de datos; SCA compara versiones de paquetes contra bases de datos de vulnerabilidades.

**P4: Que es Bandit y que tipo de vulnerabilidades detecta?**
R: Bandit es una herramienta SAST disenada especificamente para Python. Detecta: uso de funciones peligrosas (eval, exec, pickle), hashes inseguros (MD5, SHA-1), inyecciones SQL, hardcoded passwords, command injection, uso de assert para seguridad, configuraciones inseguras (debug=True), y otras vulnerabilidades del OWASP Top 10.

**P5: Como se crea una regla personalizada en Semgrep?**
R: Una regla Semgrep es un archivo YAML que define: (1) id unico de la regla, (2) pattern o patterns que describen el codigo a buscar (usando metavariables como $VAR, $EXPR), (3) message que se mostrara al encontrar el patron, (4) severity (ERROR, WARNING, INFO), (5) languages a los que aplica, (6) metadata opcional (CWE, OWASP).

**P6: Por que es importante integrar SAST en el IDE y no solo en CI/CD?**
R: Integrar SAST en el IDE permite que el desarrollador reciba feedback inmediato mientras escribe codigo, en lugar de esperar al pipeline CI/CD. Esto sigue el principio Shift-Left: corregir la vulnerabilidad cuando el contexto del codigo esta fresco, reduciendo el tiempo y costo de correccion.

**P7: Que es SonarQube y que son los "Quality Gates"?**
R: SonarQube es una plataforma de analisis continuo de calidad y seguridad de codigo. Los Quality Gates son conjuntos de criterios (ej: "0 vulnerabilidades BLOCKER", "cobertura de tests > 80%") que determinan si el codigo es aceptable. Si no se cumple el quality gate, el pipeline CI/CD se detiene y el cambio no se despliega.

## Tarea / Lectura Recomendada

1. **Bandit Documentation:**
   https://bandit.readthedocs.io/en/latest/

2. **Semgrep Registry (Reglas publicas):**
   https://semgrep.dev/explore

3. **Semgrep Writing Rules:**
   https://semgrep.dev/docs/writing-rules/overview/

4. **SonarQube Security Rules:**
   https://rules.sonarsource.com/

5. **OWASP Source Code Analysis Tools:**
   https://owasp.org/www-community/Source_Code_Analysis_Tools

6. **Tarea practica:** Crear 3 reglas Semgrep adicionales para detectar: (a) uso de `requests` sin timeout, (b) archivos temporales en directorios inseguros, (c) comparacion de contrasenas sin timing-safe comparison.

7. **Tarea practica:** Configurar SonarQube en Docker y ejecutar analisis sobre el proyecto vulnerable de la clase, corrigiendo las 10 vulnerabilidades.


