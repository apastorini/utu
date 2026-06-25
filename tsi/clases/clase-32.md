# Clase 32: Introduccion a DevSecOps y Shift-Left

**Numero de clase:** 22
**Duracion:** 2 horas

## Objetivos de Aprendizaje

- Comprender la evolucion de DevOps hacia DevSecOps
- Entender el movimiento Shift-Left y sus beneficios
- Identificar las etapas de un pipeline CI/CD donde insertar controles de seguridad
- Disenar un pipeline DevSecOps completo con SAST, DAST, SCA, secret scanning y linting
- Evaluar el modelo de madurez DevSecOps

## Contenido Detallado

### 1. Que es DevOps?

DevOps es la combinacion de desarrollo (Dev) y operaciones (Ops) que busca:
- Acelerar la entrega de software
- Automatizar procesos de build, test y deploy
- Fomentar colaboracion entre equipos
- Implementar integracion continua (CI) y despliegue continuo (CD)

**Ciclo DevOps:** Plan -> Code -> Build -> Test -> Release -> Deploy -> Operate -> Monitor

### 2. DevSecOps: Agregar Seguridad a DevOps

DevSecOps integra la seguridad en cada fase del ciclo DevOps, no como una etapa final separada.

**Principios fundamentales:**
- "You build it, you run it, you secure it"
- Seguridad como responsabilidad compartida, no solo del equipo de seguridad
- Automatizacion de controles de seguridad
- Visibilidad y transparencia

### 3. El Movimiento Shift-Left

Shift-Left significa mover las actividades de seguridad hacia la izquierda del timeline del proyecto (mas temprano en el ciclo de desarrollo).

**Beneficios:**
- **Costo menor:** Corregir una vulnerabilidad en produccion cuesta 30x mas que corregirla en desarrollo
- **Parches mas rapidos:** Las vulnerabilidades se detectan antes de llegar a produccion
- **Cultura de seguridad:** Todo el equipo es responsable de la seguridad
- **Menos deuda tecnica de seguridad:** No se acumulan vulnerabilidades sin corregir

**Niveles de Shift-Left:**
1. **Nivel 1 (Requerimientos):** Modelado de amenazas, security stories en backlog
2. **Nivel 2 (Diseno):** Security review de arquitectura, threat modeling
3. **Nivel 3 (Desarrollo):** IDE plugins con linting de seguridad, pre-commit hooks
4. **Nivel 4 (Build):** SAST, SCA, secret scanning automatizados
5. **Nivel 5 (Test):** DAST, penetration testing, fuzzing
6. **Nivel 6 (Staging):** Config hardening, compliance scanning

### 4. Pipeline CI/CD con Seguridad

**Etapas de un pipeline DevSecOps:**

```
Commit --> Lint --> Build --> SAST --> SCA --> Test --> DAST --> Deploy --> Monitor
                (seg)    (seg)    (seg)    (seg)    (seg)
```

**Controles de seguridad por etapa:**

| Etapa | Herramienta | Que detecta |
|-------|-------------|-------------|
| Pre-commit | git-secrets, truffleHog | Secretos en codigo |
| Lint | ESLint + eslint-plugin-security | Codigo inseguro |
| Build | Docker Scout, Trivy | Vulnerabilidades en imagenes |
| SAST | SonarQube, Semgrep, Bandit | Vulnerabilidades en codigo fuente |
| SCA | OWASP Dependency-Check, Snyk | Vulnerabilidades en dependencias |
| DAST | OWASP ZAP, Burp Suite | Vulnerabilidades en app en ejecucion |
| Deploy | Checkov, tfsec | Infraestructura insegura |
| Monitor | SIEM, WAF, Runtime Security | Ataques en produccion |

### 5. Modelo de Madurez DevSecOps

| Nivel | Caracteristicas |
|-------|-----------------|
| 1 - Inicial | Sin seguridad en CI/CD. Seguridad solo en auditorias anuales |
| 2 - Repetible | Seguridad basica: SAST manual, revisores de seguridad asignados |
| 3 - Definido | Automatizacion parcial: SAST y SCA en CI/CD, gate de seguridad basico |
| 4 - Gestionado | Pipeline automatizado completo: SAST, DAST, SCA, secret scanning. Gates en cada etapa |
| 5 - Optimizado | Seguridad continua: monitoreo runtime, feedback loop automatico, threat modeling integrado |

## Ejercicio 1: Pipeline CI/CD con 5 Controles de Seguridad (GitHub Actions)

```yaml
# .github/workflows/devsecops-pipeline.yml
# Pipeline CI/CD DevSecOps completo con 5 controles de seguridad

name: DevSecOps Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 6 * * 1'  # Escaneo completo semanal (lunes 6AM)

env:
  PYTHON_VERSION: '3.11'

jobs:
  # =============================================
  # CONTROL 1: LINTING DE SEGURIDAD
  # =============================================
  security-lint:
    name: 'Control 1 - Linting de Seguridad'
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Configurar Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}

      - name: Instalar dependencias
        run: |
          pip install flake8 flake8-bandit flake8-bugbear

      - name: Ejecutar flake8 con plugins de seguridad
        run: |
          flake8 . --count --statistics \
            --select=B,C,E,F,W,T4,B9 \
            --max-complexity=10 \
            --exclude=venv,.git,__pycache__

  # =============================================
  # CONTROL 2: SAST (Static Application Security Testing)
  # =============================================
  sast:
    name: 'Control 2 - SAST con Bandit y Semgrep'
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Configurar Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}

      - name: Instalar herramientas SAST
        run: |
          pip install bandit semgrep

      - name: SAST con Bandit
        run: |
          bandit -r . -f json -o bandit-report.json \
            --confidence-level medium \
            --severity-level medium \
            --skip B101,B105

      - name: SAST con Semgrep
        run: |
          semgrep --config=p/owasp-top-ten \
            --config=p/python \
            --error --strict \
            --output=semgrep-report.json \
            --json .

      - name: Subir reportes SAST
        uses: actions/upload-artifact@v4
        with:
          name: sast-reports
          path: |
            bandit-report.json
            semgrep-report.json

      - name: Fallar si hay vulnerabilidades criticas
        run: |
          python -c "
          import json
          with open('bandit-report.json') as f:
              report = json.load(f)
          high_issues = [i for i in report.get('results', [])
                        if i.get('issue_severity') == 'HIGH']
          if high_issues:
              print(f'ERROR: {len(high_issues)} vulnerabilidades HIGH encontradas')
              for issue in high_issues:
                  print(f'  - {issue[\"filename\"]}:{issue[\"line_number\"]} - {issue[\"issue_text\"]}')
              exit(1)
          "

  # =============================================
  # CONTROL 3: SCA (Software Composition Analysis)
  # =============================================
  sca:
    name: 'Control 3 - SCA con pip-audit'
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Configurar Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}

      - name: Instalar pip-audit
        run: pip install pip-audit

      - name: Escanear dependencias
        run: |
          pip-audit --requirement requirements.txt \
            --strict \
            --desc on \
            --format markdown \
            --output pip-audit-report.md

      - name: Publicar reporte
        uses: actions/upload-artifact@v4
        with:
          name: sca-report
          path: pip-audit-report.md

      - name: Verificar bloqueos
        run: |
          if [ -f pip-audit-report.md ]; then
            if grep -q "CRITICAL\|HIGH" pip-audit-report.md; then
              echo "Vulnerabilidades criticas o altas en dependencias."
              exit 1
            fi
          fi

  # =============================================
  # CONTROL 4: SECRET SCANNING
  # =============================================
  secret-scanning:
    name: 'Control 4 - Secret Scanning'
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Historial completo para truffleHog

      - name: Instalar truffleHog
        run: pip install trufflehog

      - name: Escanear con truffleHog
        run: |
          trufflehog git file://. --only-verified \
            --fail \
            --json > trufflehog-report.json || true

      - name: Publicar reporte
        uses: actions/upload-artifact@v4
        with:
          name: secret-scan-report
          path: trufflehog-report.json

      - name: Verificar resultados
        run: |
          if [ -f trufflehog-report.json ]; then
            if [ "$(cat trufflehog-report.json | wc -l)" -gt 0 ]; then
              echo "Secretos encontrados en el repositorio!"
              cat trufflehog-report.json
              exit 1
            fi
          fi

  # =============================================
  # CONTROL 5: DAST (Dynamic Application Security Testing)
  # =============================================
  dast:
    name: 'Control 5 - DAST con OWASP ZAP'
    runs-on: ubuntu-latest
    needs: [build-and-test]
    if: github.event_name == 'schedule' || github.ref == 'refs/heads/main'

    steps:
      - name: Iniciar aplicacion de prueba
        run: |
          # En un pipeline real, aqui se deploya la app en un entorno de staging
          docker build -t miapp:test .
          docker run -d -p 5000:5000 --name miapp-test miapp:test

      - name: Ejecutar OWASP ZAP Scan
        uses: zaproxy/action-full-scan@v0.10.0
        with:
          target: 'http://localhost:5000'
          cmd_options: '-a -j -T 5'

      - name: Subir reporte ZAP
        uses: actions/upload-artifact@v4
        with:
          name: dast-report
          path: zap-report.html

  # =============================================
  # BUILD, TEST Y DEPLOY
  # =============================================
  build-and-test:
    name: 'Build y Test'
    runs-on: ubuntu-latest
    needs: [security-lint, sast, sca, secret-scanning]

    steps:
      - uses: actions/checkout@v4

      - name: Configurar Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}

      - name: Instalar dependencias
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Ejecutar tests
        run: |
          python -m pytest tests/ \
            --junitxml=test-report.xml \
            --cov=app \
            --cov-report=xml

      - name: Construir paquete
        run: python -m build

      - name: Subir artefacto
        uses: actions/upload-artifact@v4
        with:
          name: build-package
          path: dist/

  deploy:
    name: 'Deploy Seguro'
    runs-on: ubuntu-latest
    needs: [build-and-test, dast]
    if: github.ref == 'refs/heads/main'

    steps:
      - uses: actions/checkout@v4

      - name: Deploy a produccion
        run: |
          # En produccion, usar credenciales de GitHub Secrets
          # No hardcodear nunca
          echo "Desplegando version segura..."
          # ./deploy.sh

      - name: Verificar deploy
        run: |
          curl -f http://produccion.example.com/health || exit 1
```

## Ejercicio 2: Diagrama ASCII de Pipeline DevSecOps

```
+-------------------------------------------------------------------+
|                    PIPELINE DEVSECOPS COMPLETO                     |
+-------------------------------------------------------------------+
|                                                                     |
|  [DESARROLLADOR]                                                    |
|       |                                                             |
|       | git commit + git push                                       |
|       v                                                             |
|  +----------+     +------------+     +------------+                 |
|  | PRE-     |     | LINT DE    |     | BUILD      |                 |
|  | COMMIT   | --> | SEGURIDAD  | --> | DEL        |                 |
|  | HOOKS    |     | (flake8 +  |     | PROYECTO   |                 |
|  | (git-    |     | bandit)    |     |            |                 |
|  | secrets) |     +------------+     +------------+                 |
|  +----------+            |                  |                       |
|                          |                  |                       |
|                          v                  v                       |
|                    +------------+     +------------+                 |
|                    | CONTROL 1  |     | CONTROL 2  |                 |
|                    | SAST       |     | SCA        |                 |
|                    | (Semgrep,  |     | (pip-audit,|                 |
|                    | Bandit)    |     | Snyk)      |                 |
|                    +------------+     +------------+                 |
|                          |                  |                       |
|                          +--------+---------+                       |
|                                   |                                 |
|                                   v                                 |
|                            +------------+                           |
|                            | CONTROL 3  |                           |
|                            | SECRET     |                           |
|                            | SCANNING   |                           |
|                            | (truffle-  |                           |
|                            | Hog)       |                           |
|                            +------------+                           |
|                                   |                                 |
|                                   v                                 |
|                            +------------+                           |
|                            | BUILD DE   |                           |
|                            | IMAGEN     |                           |
|                            | DOCKER     |                           |
|                            | (Docker    |                           |
|                            | Scout)     |                           |
|                            +------------+                           |
|                                   |                                 |
|                                   v                                 |
|                            +------------+                           |
|                            | CONTROL 4  |                           |
|                            | DAST       |                           |
|                            | (OWASP ZAP,|                           |
|                            | Nikto)     |                           |
|                            +------------+                           |
|                                   |                                 |
|                                   v                                 |
|                            +------------+                           |
|                            | DEPLOY A   |                           |
|                            | STAGING    |                           |
|                            +------------+                           |
|                                   |                                 |
|                                   v                                 |
|                            +------------+                           |
|                            | CONTROL 5  |                           |
|                            | INFRA      |                           |
|                            | SCANNING   |                           |
|                            | (Checkov,  |                           |
|                            | tfsec)     |                           |
|                            +------------+                           |
|                                   |                                 |
|                                   v                                 |
|                            +------------+                           |
|                            | DEPLOY A   |                           |
|                            | PRODUCCION |                           |
|                            +------------+                           |
|                                   |                                 |
|                                   v                                 |
|                            +------------+                           |
|                            | MONITOR    |                           |
|                            | CONTINUO   |                           |
|                            | (SIEM,     |                           |
|                            | WAF,       |                           |
|                            | Runtime    |                           |
|                            | Security)  |                           |
|                            +------------+                           |
|                                                                     |
+-------------------------------------------------------------------+
|                                                                     |
|  GATES DE SEGURIDAD (Quality Gates):                               |
|  - Si SAST encuentra vulnerabilidades CRITICAS -> FALLA pipeline    |
|  - Si SCA encuentra CVE conocidas -> FALLA pipeline                |
|  - Si secret scanning encuentra secretos -> FALLA pipeline         |
|  - Si DAST encuentra vulnerabilidades HIGH -> REQUIERE aprobacion  |
|  - Si linting de seguridad falla -> FALLA pipeline                 |
|                                                                     |
+-------------------------------------------------------------------+
```

## Ejercicio 3: Script de Automatizacion de Seguridad Local

```python
# devsecops_local.py - Automatizacion de seguridad local (pre-commit)
import os
import sys
import json
import subprocess
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


class DevSecOpsLocal:
    """
    Ejecuta controles de seguridad localmente antes del commit.
    Simula lo que hara el pipeline CI/CD, pero en el entorno del
    desarrollador para feedback inmediato (Shift-Left).
    """

    def __init__(self, repo_path: str = '.'):
        self.repo_path = Path(repo_path)
        self.python_files = list(self.repo_path.rglob('*.py'))
        self.requirements = self.repo_path / 'requirements.txt'
        self.errores = []

    def ejecutar_todo(self) -> bool:
        """Ejecuta todos los controles de seguridad."""
        logger.info("=" * 60)
        logger.info("DEVSECOPS LOCAL - Controles de Seguridad Pre-Commit")
        logger.info("=" * 60)

        controles = [
            ('1. Lint Seguridad (flake8 + bandit)', self._lint_seguridad),
            ('2. SAST (Bandit)', self._sast_bandit),
            ('3. SAST (Semgrep)', self._sast_semgrep),
            ('4. SCA (pip-audit)', self._sca_pip_audit),
            ('5. Secret Scanning', self._secret_scanning),
        ]

        for nombre, control in controles:
            logger.info(f"\n--- {nombre} ---")
            try:
                if control():
                    logger.info(f"  OK: {nombre} pasado")
                else:
                    logger.error(f"  FALLO: {nombre}")
            except Exception as e:
                logger.error(f"  ERROR: {nombre} - {str(e)}")
                self.errores.append(nombre)

        if self.errores:
            logger.info("\n" + "=" * 60)
            logger.error("CONTROLES FALLIDOS:")
            for e in self.errores:
                logger.error(f"  - {e}")
            logger.info("\nCorrige los errores antes de hacer commit.")
            logger.info("Usa 'git commit --no-verify' para saltar (NO RECOMENDADO).")
            return False
        else:
            logger.info("\n" + "=" * 60)
            logger.info("TODOS LOS CONTROLES DE SEGURIDAD PASARON")
            logger.info("=" * 60)
            return True

    def _lint_seguridad(self) -> bool:
        """Ejecuta flake8 con plugins de seguridad."""
        if not self.python_files:
            return True
        result = subprocess.run(
            ['flake8', '--select=B,C,E,F,W,T4,B9', '--statistics', '--count', '.'],
            capture_output=True, text=True, cwd=self.repo_path
        )
        if result.returncode != 0:
            logger.info(result.stdout[:2000])
            return False
        logger.info("  Sin errores de linting de seguridad")
        return True

    def _sast_bandit(self) -> bool:
        """Ejecuta Bandit SAST."""
        if not self.python_files:
            return True
        result = subprocess.run(
            ['bandit', '-r', '.', '-f', 'json', '--confidence-level', 'medium',
             '--severity-level', 'medium'],
            capture_output=True, text=True, cwd=self.repo_path
        )
        try:
            report = json.loads(result.stdout)
            issues = report.get('results', [])
            high = [i for i in issues if i.get('issue_severity') == 'HIGH']
            medium = [i for i in issues if i.get('issue_severity') == 'MEDIUM']

            if high:
                logger.error(f"  {len(high)} vulnerabilidades HIGH encontradas:")
                for issue in high:
                    logger.error(f"    {issue['filename']}:{issue['line_number']} - "
                                f"{issue['issue_text']}")
            if medium:
                logger.info(f"  {len(medium)} vulnerabilidades MEDIUM encontradas")

            logger.info(f"  Total: {len(issues)} issues")
            return len(high) == 0

        except json.JSONDecodeError:
            logger.warning("  Bandit no produjo JSON valido")
            return True

    def _sast_semgrep(self) -> bool:
        """Ejecuta Semgrep con reglas OWASP Top 10 y Python."""
        result = subprocess.run(
            ['semgrep', '--config=p/owasp-top-ten', '--config=p/python',
             '--json', '--error', '--strict', '.'],
            capture_output=True, text=True, cwd=self.repo_path
        )
        if result.returncode != 0 and result.stderr:
            try:
                report = json.loads(result.stdout)
                errors_count = len(report.get('errors', []))
                results_count = len(report.get('results', []))
                if results_count > 0:
                    logger.info(f"  {results_count} hallazgos de Semgrep")
                    for r in report['results'][:5]:
                        logger.info(f"    {r['path']}:{r['start']['line']} - "
                                   f"{r['extra']['message'][:80]}")
                return results_count == 0
            except (json.JSONDecodeError, KeyError):
                return False
        return True

    def _sca_pip_audit(self) -> bool:
        """Ejecuta pip-audit para SCA."""
        if not self.requirements.exists():
            logger.info("  No hay requirements.txt, saltando SCA")
            return True

        result = subprocess.run(
            ['pip-audit', '--requirement', 'requirements.txt', '--strict', '--desc'],
            capture_output=True, text=True, cwd=self.repo_path
        )
        if result.returncode != 0:
            logger.info(result.stdout[:1000])
            return False
        logger.info("  Sin vulnerabilidades conocidas en dependencias")
        return True

    def _secret_scanning(self) -> bool:
        """Ejecuta busqueda de secretos con regex."""
        secret_patterns = [
            (r'-----BEGIN (RSA|EC|OPENSSH|PGP) PRIVATE KEY-----',
             'Clave privada'),
            (r'AKIA[0-9A-Z]{16}', 'AWS Access Key ID'),
            (r'sk_live_[0-9a-zA-Z]+', 'Stripe Live Key'),
            (r'ghp_[0-9a-zA-Z]{36}', 'GitHub Token'),
            (r'(password|passwd|pwd)\s*[=:]\s*["\'].+["\']',
             'Contrasena hardcodeada'),
            (r'api[_-]?key\s*[=:]\s*["\'].+["\']',
             'API Key hardcodeada'),
            (r'secret[_-]?key\s*[=:]\s*["\'].+["\']',
             'Secret Key hardcodeada'),
            (r'token\s*[=:]\s*["\'].+["\']',
             'Token hardcodeado'),
        ]

        found = False
        for pattern, description in secret_patterns:
            result = subprocess.run(
                ['rg', '-n', pattern, '--glob', '!.git', '--glob', '!venv', '.'],
                capture_output=True, text=True, cwd=self.repo_path
            )
            if result.stdout.strip():
                logger.warning(f"  POSIBLE SECRETO: {description}")
                for line in result.stdout.strip().split('\n')[:3]:
                    logger.warning(f"    {line}")
                found = True

        if not found:
            logger.info("  Sin secretos detectados")
            return True
        return False


# ============================================================
# PRE-COMMIT HOOK (instalar en .git/hooks/pre-commit)
# ============================================================

PRE_COMMIT_HOOK = """#!/bin/bash
# Hook pre-commit que ejecuta DevSecOps local
echo "Ejecutando controles de seguridad pre-commit..."
python devsecops_local.py
if [ $? -ne 0 ]; then
    echo "ERROR: Los controles de seguridad fallaron."
    echo "Corrige los errores o usa 'git commit --no-verify' para saltar."
    exit 1
fi
"""


def instalar_precommit_hook():
    """Instala el hook pre-commit."""
    hook_path = Path('.git/hooks/pre-commit')
    hook_path.write_text(PRE_COMMIT_HOOK)
    hook_path.chmod(0o755)
    logger.info("Hook pre-commit instalado en .git/hooks/pre-commit")


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='DevSecOps Local')
    parser.add_argument('--install-hook', action='store_true',
                       help='Instalar hook pre-commit')
    args = parser.parse_args()

    if args.install_hook:
        instalar_precommit_hook()
    else:
        devsecops = DevSecOpsLocal()
        exito = devsecops.ejecutar_todo()
        sys.exit(0 if exito else 1)
```

## Preguntas y Respuestas

**P1: Que es DevSecOps y como se diferencia de DevOps?**
R: DevOps se enfoca en acelerar la entrega de software integrando desarrollo y operaciones. DevSecOps agrega seguridad como parte integral del proceso, no como una etapa final. En DevSecOps, la seguridad es responsabilidad de todos (no solo del equipo de seguridad) y se automatiza en cada etapa del pipeline.

**P2: Que significa Shift-Left y cuales son sus beneficios?**
R: Shift-Left significa mover las actividades de seguridad a etapas tempranas del ciclo de desarrollo (requisitos, diseno, codificacion) en lugar de dejarlas para el final. Beneficios: costo de correccion 30x menor, vulnerabilidades detectadas antes de produccion, cultura de seguridad compartida, menos deuda tecnica de seguridad.

**P3: Que 5 controles de seguridad se deben insertar en un pipeline CI/CD?**
R: (1) SAST (Static Analysis) - analisis de codigo fuente en build. (2) SCA (Software Composition Analysis) - analisis de dependencias. (3) Secret Scanning - deteccion de secretos en el repositorio. (4) DAST (Dynamic Analysis) - prueba de seguridad en app en ejecucion. (5) Linting de seguridad - reglas de codigo seguro en el IDE/pre-commit.

**P4: Cual es la diferencia entre SAST y DAST?**
R: SAST (Static Application Security Testing) analiza el codigo fuente sin ejecutarlo, detectando vulnerabilidades en el codigo mismo (inyecciones, XSS, etc.). DAST (Dynamic Application Security Testing) analiza la aplicacion en ejecucion desde afuera, detectando vulnerabilidades en la configuracion y el comportamiento en tiempo real. SAST es "white-box" (ve el codigo), DAST es "black-box" (no ve el codigo).

**P5: Que es un "quality gate" en un pipeline DevSecOps?**
R: Un quality gate es un punto de control en el pipeline donde se evaluan metricas de seguridad y calidad. Si no se cumplen los criterios (ej: vulnerabilidades criticas, cobertura de tests insuficiente, secretos detectados), el pipeline se detiene y el cambio no avanza a la siguiente etapa. Ejemplos: "no permitir vulnerabilidades HIGH en SAST", "no permitir CVEs conocidos en dependencias".

**P6: Por que es importante que la seguridad sea responsabilidad compartida en DevSecOps?**
R: En modelos tradicionales, la seguridad es responsabilidad exclusiva del equipo de seguridad, que revisa al final del ciclo. Esto crea cuellos de botella y conflictos. En DevSecOps, desarrolladores, operaciones y seguridad colaboran desde el inicio, con herramientas automatizadas que permiten a los desarrolladores detectar y corregir vulnerabilidades sin depender del equipo de seguridad.

**P7: Que es el modelo de madurez DevSecOps y cuales son sus niveles?**
R: Es un marco para evaluar que tan integrada esta la seguridad en el ciclo DevOps. Niveles: (1) Inicial - sin seguridad en CI/CD. (2) Repetible - SAST manual basico. (3) Definido - automatizacion parcial con SAST y SCA. (4) Gestionado - pipeline completo con gates en cada etapa. (5) Optimizado - seguridad continua con monitoreo runtime y feedback loop automatico.

## Tarea / Lectura Recomendada

1. **OWASP DevSecOps Guideline:**
   https://owasp.org/www-project-devsecops-guideline/

2. **OWASP Software Assurance Maturity Model (SAMM):**
   https://owaspsamm.org/

3. **DevSecOps en GitHub Actions:**
   https://docs.github.com/en/actions/security-guides

4. **Docker Security Scanning:**
   https://docs.docker.com/scout/

5. **Tarea practica:** Crear un pipeline DevSecOps para una app Node.js con ESLint + SonarCloud + Snyk + ZAP.

6. **Tarea practica:** Evaluar la madurez DevSecOps de un proyecto real usando el modelo de 5 niveles y proponer mejoras especificas.


