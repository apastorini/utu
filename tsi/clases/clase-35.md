# Clase 35: Integrando Seguridad en el Pipeline CI/CD

**Numero de clase:** 25  
**Duracion:** 2 horas  
**Curso:** Taller de Ciberseguridad Orientada al Desarrollo

---

## Objetivos de Aprendizaje

- Comprender como integrar herramientas de seguridad en pipelines de CI/CD
- Distinguir entre las distintas etapas de seguridad en el ciclo de integracion continua
- Implementar quality gates con umbrales de severidad
- Configurar firmado de artefactos y contenedores
- Construir un pipeline completo que falle ante vulnerabilidades criticas

---

## Contenido Detallado

### 1. Repaso de CI/CD (15 min)

**CI/CD** (Integracion Continua / Despliegue Continuo) automatiza la construccion, prueba y despliegue de software. Las plataformas mas comunes son:

- **GitHub Actions:** Workflows basados en YAML con triggers por eventos (push, pull_request, schedule). Ejecuta jobs en runners.
- **GitLab CI:** Archivo `.gitlab-ci.yml` con stages, jobs y runners propios o compartidos.
- **Jenkins:** Servidor de automatizacion extensible via plugins. Usa Jenkinsfile (Declarative o Scripted Pipeline).

Cada una permite ejecutar etapas de seguridad como pasos dentro del pipeline.

### 2. Gateways de Seguridad (15 min)

Un **security gateway** es un punto en el pipeline donde se evaluan criterios de seguridad. Si no se cumplen, el pipeline falla (fail/pass criteria).

Criterios tipicos:
- Vulnerabilidades criticas o altas: **FAIL**
- Cobertura de pruebas de seguridad por debajo del umbral: **FAIL**
- Secretos detectados en el codigo: **FAIL**
- Licencias incompatibles: **WARN** o **FAIL**
- Calidad de codigo por debajo de A en SonarQube: **WARN**

### 3. Etapas del Pipeline Seguro (20 min)

```
commit -> SAST -> SCA -> unit tests -> DAST -> deploy
```

- **SAST (Static Application Security Testing):** Analisis estatico. Examina el codigo fuente sin ejecutarlo. Herramientas: Bandit (Python), Semgrep, SonarQube, CodeQL.
- **SCA (Software Composition Analysis):** Analisis de dependencias. Detecta vulnerabilidades en librerias de terceros. Herramientas: pip-audit, npm audit, OWASP Dependency-Check, Snyk.
- **DAST (Dynamic Application Security Testing):** Analisis dinamico. Prueba la aplicacion en ejecucion. Herramientas: OWASP ZAP, Burp Suite, Nikto.

### 4. Quality Gates y SonarQube (15 min)

**SonarQube** define **Quality Gates** como conjuntos de condiciones que el codigo debe cumplir:

- Umbrales de severidad: Blocker, Critical, Major, Minor, Info
- Condiciones tipicas:
  - "Nuevo codigo: densidad de bugs < 3%"
  - "Vulnerabilidades criticas = 0"
  - "Debt Ratio < 5%"
  - "Cobertura de tests > 80%"

Si el Quality Gate falla, el pipeline se detiene.

### 5. Artefactos Seguros y Firmado de Contenedores (15 min)

**Artefactos seguros:** Los binarios y paquetes generados deben estar firmados para garantizar integridad y autenticidad.

- **Cosign:** Herramienta de Sigstore para firmar contenedores OCI.
- **Notary:** Proyecto de Docker para firmar y verificar imagenes.
- **SLSA (Supply-chain Levels for Software Artifacts):** Framework de niveles de confianza en la cadena de suministro.

Flujo de firmado con Cosign:
```bash
# Generar par de llaves
cosign generate-key-pair

# Firmar imagen
cosign sign --key cosign.key usuario/app:latest

# Verificar
cosign verify --key cosign.pub usuario/app:latest
```

### 6. Pipeline Completo de GitHub Actions con Seguridad (20 min)

Ejemplo de workflow con todas las etapas:

```yaml
name: Secure CI Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  security-checks:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      # --- LINT ---
      - name: Lint with flake8
        run: |
          pip install flake8
          flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics

      # --- SAST con Bandit ---
      - name: SAST - Bandit
        run: |
          pip install bandit
          bandit -r . -f json -o bandit-report.json
          # Fallar si hay vulnerabilidades criticas o altas
          python -c "
import json
with open('bandit-report.json') as f:
    data = json.load(f)
high_confidence_high_severity = [
    r for r in data.get('results', [])
    if r['issue_severity'] == 'HIGH' and r['issue_confidence'] == 'HIGH'
]
if high_confidence_high_severity:
    print(f'ERROR: {len(high_confidence_high_severity)} vulnerabilidades criticas encontradas')
    for r in high_confidence_high_severity:
        print(f'  - {r[\"filename\"]}:{r[\"line_number\"]} {r[\"issue_text\"]}')
    exit(1)
print('SAST: Sin vulnerabilidades criticas')
"

      # --- SCA con pip-audit ---
      - name: SCA - pip-audit
        run: |
          pip install pip-audit
          pip-audit --requirement requirements.txt --desc on
          # Fallar si hay vulnerabilidades con severidad >= critica
          pip-audit --requirement requirements.txt || exit 1

      # --- Unit tests ---
      - name: Unit Tests
        run: |
          pip install pytest pytest-cov
          pytest tests/ --cov=./ --cov-fail-under=80

      # --- DAST con OWASP ZAP ---
      - name: DAST - OWASP ZAP
        if: github.event_name == 'push' && github.ref == 'refs/heads/main'
        run: |
          docker run --rm -v $(pwd):/zap/wrk ghcr.io/zaproxy/zaproxy:stable \
            zap-baseline.py -t https://staging.example.com -r zap-report.html

      # --- Build y firmado de contenedor ---
      - name: Build and Sign Image
        if: github.ref == 'refs/heads/main'
        run: |
          docker build -t $REGISTRY/$IMAGE_NAME:${{ github.sha }} .
          docker push $REGISTRY/$IMAGE_NAME:${{ github.sha }}
          cosign sign --key ${{ secrets.COSIGN_KEY }} $REGISTRY/$IMAGE_NAME:${{ github.sha }}
```

---

## Ejercicio 1: Escribir un GitHub Actions Workflow Completo con Seguridad

**Enunciado:** Escribe un workflow de GitHub Actions completo para una aplicacion Python que incluya: lint, test, SAST con Bandit, SCA con pip-audit, y que FALLE si hay vulnerabilidades criticas.

**Solucion:**

```yaml
name: Secure Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  secure-build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Setup Python 3.11
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

      - name: Lint with flake8
        run: |
          pip install flake8
          flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics

      - name: SAST with Bandit
        run: |
          pip install bandit
          bandit -r . -f json -o bandit-results.json
          python -c "
import json, sys
with open('bandit-results.json') as f:
    report = json.load(f)
results = report.get('results', [])

critical = [r for r in results
            if r['issue_severity'] == 'HIGH' and r['issue_confidence'] == 'HIGH']

if critical:
    for r in critical:
        print(f'CRITICAL: {r[\"filename\"]}:{r[\"line_number\"]} - {r[\"issue_text\"]}')
    print(f'Total criticas: {len(critical)}')
    sys.exit(1)
print('Bandit: no se encontraron vulnerabilidades criticas')
"

      - name: SCA with pip-audit
        run: |
          pip install pip-audit
          pip-audit --requirement requirements.txt
        continue-on-error: false

      - name: Run tests
        run: |
          pip install pytest
          python -m pytest tests/ -v
```

---

## Ejercicio 2: Agregar 5 Gates de Seguridad a un Pipeline Inseguro

**Enunciado:** Dado el siguiente pipeline sin seguridad, agrega 5 gates de seguridad con criterios de aceptacion.

Pipeline original inseguro:
```yaml
name: Insecure Pipeline
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Build
        run: docker build -t app .
      - name: Push
        run: docker push app
      - name: Deploy
        run: kubectl apply -f k8s/
```

**Solucion con 5 gates de seguridad:**

```yaml
name: Secured Pipeline
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  secure-build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      # Gate 1: Secret scanning
      - name: Gate 1 - Secret Scanning
        run: |
          pip install truffleHog
          trufflehog --max_depth=1 file://. || exit 1
        continue-on-error: false

      # Gate 2: SAST
      - name: Gate 2 - SAST with CodeQL
        uses: github/codeql-action/analyze@v2
        with:
          category: "/language:python"
        continue-on-error: false

      # Gate 3: SCA
      - name: Gate 3 - Dependency Check
        run: |
          pip install pip-audit
          pip-audit --requirement requirements.txt
        continue-on-error: false

      - name: Build
        run: docker build -t app .

      # Gate 4: Image scan
      - name: Gate 4 - Container Image Scan
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: 'app'
          format: 'table'
          exit-code: '1'
          severity: 'CRITICAL,HIGH'

      - name: Push
        run: docker push app

      # Gate 5: IaC scan
      - name: Gate 5 - IaC Scan with Checkov
        run: |
          pip install checkov
          checkov -d k8s/ --framework kubernetes
        continue-on-error: false

      - name: Deploy
        run: kubectl apply -f k8s/
```

**Criterios de aceptacion:**
1. Gate 1 (Secret Scanning): No se permiten secretos en el repositorio. FAIL si se encuentra alguno.
2. Gate 2 (SAST): Vulnerabilidades de seguridad en codigo = 0. FAIL si se detectan.
3. Gate 3 (SCA): Dependencias con vulnerabilidades = 0. FAIL si alguna es conocida.
4. Gate 4 (Image Scan): La imagen del contenedor no debe tener vulnerabilidades CRITICAL o HIGH. FAIL si las tiene.
5. Gate 5 (IaC Scan): La configuracion de Kubernetes debe cumplir con CIS benchmarks. FAIL si hay fallos criticos.

---

## Ejercicio 3: Script Python que Lee Reporte de Bandit y Decide si el Pipeline Pasa o Falla

**Enunciado:** Crear un script Python que lea el reporte JSON de Bandit y decida si el pipeline pasa o falla basado en reglas configurables.

**Solucion:**

```python
#!/usr/bin/env python3
"""
gate_bandit.py - Lee el reporte JSON de Bandit y decide si el pipeline pasa o falla.

Uso:
    python gate_bandit.py bandit-report.json
    python gate_bandit.py bandit-report.json --fail-on HIGH --min-confidence HIGH

Reglas por defecto:
    - Fallar si hay vulnerabilidades HIGH/HIGH (severity/confidence)
    - Fallar si hay mas de 10 vulnerabilidades MEDIUM
"""

import json
import sys
import argparse


def cargar_report(path):
    with open(path) as f:
        return json.load(f)


def evaluar(report, fail_on_severity, min_confidence, max_medium):
    results = report.get('results', [])
    total = len(results)

    severities = {'LOW': 1, 'MEDIUM': 2, 'HIGH': 3}
    confidences = {'LOW': 1, 'MEDIUM': 2, 'HIGH': 3}

    severidad_minima = severities.get(fail_on_severity.upper(), 3)
    confianza_minima = confidences.get(min_confidence.upper(), 1)

    fallos = []
    advertencias = []

    for r in results:
        sev = r['issue_severity'].upper()
        conf = r['issue_confidence'].upper()
        sev_score = severities.get(sev, 0)
        conf_score = confidences.get(conf, 0)

        if sev_score >= severidad_minima and conf_score >= confianza_minima:
            fallos.append(r)
        elif sev == 'MEDIUM':
            advertencias.append(r)

    print(f"Total de hallazgos: {total}")
    print(f"Fallos (severidad>={fail_on_severity}, confianza>={min_confidence}): {len(fallos)}")
    print(f"Advertencias (MEDIUM): {len(advertencias)}")

    if len(advertencias) > max_medium:
        print(f"LIMITE EXCEDIDO: {len(advertencias)} advertencias (maximo: {max_medium})")
        fallos.extend(advertencias)

    if fallos:
        print(f"\n--- FALLOS DETECTADOS ---")
        for f in fallos:
            print(f"  [{f['issue_severity']}/{f['issue_confidence']}] "
                  f"{f['filename']}:{f['line_number']} - {f['issue_text']}")
        print(f"\nResultado: FAIL (se encontraron {len(fallos)} vulnerabilidades criticas)")
        return False

    print("\nResultado: PASS")
    return True


def main():
    parser = argparse.ArgumentParser(
        description='Quality Gate para reportes de Bandit')
    parser.add_argument('report', help='Ruta al archivo bandit-report.json')
    parser.add_argument('--fail-on', default='HIGH',
                        choices=['LOW', 'MEDIUM', 'HIGH'],
                        help='Severidad minima para fallar (default: HIGH)')
    parser.add_argument('--min-confidence', default='HIGH',
                        choices=['LOW', 'MEDIUM', 'HIGH'],
                        help='Confianza minima requerida (default: HIGH)')
    parser.add_argument('--max-medium', type=int, default=10,
                        help='Maximo de vulnerabilidades MEDIUM permitidas (default: 10)')

    args = parser.parse_args()

    try:
        report = cargar_report(args.report)
    except FileNotFoundError:
        print(f"Error: No se encontro el archivo {args.report}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: El archivo {args.report} no es JSON valido")
        sys.exit(1)

    if evaluar(report, args.fail_on, args.min_confidence, args.max_medium):
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()
```

---

## Preguntas y Respuestas

**1. Que diferencia hay entre SAST y DAST?**

SAST (Static Application Security Testing) analiza el codigo fuente sin ejecutarlo, identificando vulnerabilidades en etapas tempranas del desarrollo. DAST (Dynamic Application Security Testing) prueba la aplicacion en ejecucion, detectando vulnerabilidades en tiempo real que solo son visibles cuando la app esta funcionando.

**2. Que es un Quality Gate y como se usa en SonarQube?**

Un Quality Gate es un conjunto de condiciones que el codigo debe cumplir para pasar el control de calidad. En SonarQube se define con umbrales como "nuevo codigo: vulnerabilidades criticas = 0" o "cobertura > 80%". Si no se cumple, el pipeline falla y no se despliega.

**3. Por que es importante firmar contenedores en un pipeline?**

El firmado de contenedores garantiza la integridad y autenticidad de la imagen. Evita que un atacante modifique la imagen en el registro (supply-chain attack). Con Cosign se usa criptografia de clave publica/privada y se puede verificar antes de desplegar.

**4. Que es SLSA y que niveles existen?**

SLSA (Supply-chain Levels for Software Artifacts) es un framework de confianza en la cadena de suministro. Niveles: SLSA 1 (build documentada), SLSA 2 (build con controles), SLSA 3 (build aislada y reproducible), SLSA 4 (build con integridad total y auditoria).

**5. Como se configura un fail criterion en GitHub Actions para que el pipeline se detenga si hay vulnerabilidades?**

Se usa `exit(1)` en scripts o `continue-on-error: false` en pasos. Herramientas como `pip-audit` retornan codigo de salida != 0 si encuentran vulnerabilidades. Bandit requiere un script wrapper que lea el JSON y decida.

**6. Que es SCA y que herramientas se usan?**

SCA (Software Composition Analysis) analiza las dependencias de terceros para detectar vulnerabilidades conocidas, licencias incompatibles y malware. Herramientas: pip-audit, npm audit, OWASP Dependency-Check, Snyk, Trivy.

**7. Cual es la diferencia entre severity y confidence en Bandit?**

Severity indica el impacto potencial de la vulnerabilidad (LOW, MEDIUM, HIGH). Confidence indica la certeza del analisis (LOW, MEDIUM, HIGH). Una vulnerabilidad HIGH/HIGH es critica y debe detener el pipeline. HIGH/LOW puede ser un falso positivo.

---

## Tarea / Lectura Recomendada

- Leer: OWASP Cheat Sheet para CI/CD Security (https://cheatsheetseries.owasp.org/cheatsheets/CI_CD_Security_Cheat_Sheet.html)
- Leer: SLSA Specification (https://slsa.dev/spec/v1.0/)
- Practicar: Configurar un repositorio de prueba con GitHub Actions y Bandit siguiendo el ejercicio 1
- Investigar: Cosign y Sigstore para firmado de imagenes
- Preparacion: Traer un Dockerfile propio para la clase 26


