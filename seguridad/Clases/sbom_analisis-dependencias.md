# SBOM y Análisis de Dependencias en el Ciclo de Desarrollo

## ¿Qué es un SBOM?

Un **SBOM (Software Bill of Materials)** es un inventario formal de todos los componentes de software, dependencias, licencias y metadatos asociados a una aplicación. Funciona como una "lista de ingredientes" que permite:

- **Trazabilidad**: Saber exactamente qué librerías y versiones se usan
- **Vulnerabilidad**: Identificar rápidamente componentes afectados por CVEs
- **Cumplimiento**: Verificar licencias de software
- **Auditoría**: Demonstrar cadena de suministro segura

---

## Estándares de SBOM

### CycloneDX

**CycloneDX** es un estándar moderno optimizado para entornosDevOps yCI/CD.

**Características**:
- Formato JSONB (compactobut estructurado)
- Ligero y fácildelegenerar
- Excelentepara integraciones automatizadas
- Amplio soporteen herramientas (trivy, syft, gradle, maven, npm)

**Usopor desarrolladores**:

```bash
# Usando Syft (generar SBOM)
syft . -o cyclonedx-json > sbom.json

# Usando Trivy (análisis completo)
trivy fs --security-checks vuln,config .

# Plugin Maven
mvn org.cyclonedx:maven-cyclonedx-plugin:makeAggregateBom
```

---

### SPDX

**SPDX** (SoftwarePackage Data Exchange) es el estándar impulsado por la **Linux Foundation**.

**Características**:
- Formato RDF/XML/JSON/YAML
- Más detallado y extensible
- Enfoque en cumplimiento de licencias
- Amplio soporte empresarial

**Usopor desarrolladores**:

```bash
# Generar SBOM SPDX
syft . -o spdx-json > sbom.spdx.json

# Usando spdx-sbom-generator
./generate-spdx -p npm -n proyecto
```

---

## Shift Left: Análisis de Dependencias

El concepto **Shift Left** consiste en mover las pruebas y análisis de seguridad lo más temprano posible en el ciclo de desarrollo (izquierda en la línea temporal), detectando problemas antes de que lleguen a producción.

### Flujo Shift Left para Dependencias

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   DESARROLLO│───▶│   COMMIT   │───▶│   PUSH     │───▶│  CI/CD     │
│   LOCAL    │    │  (pre-commit)│   │  (pre-push)│    │  BUILD    │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
      │                  │                  │                  │
      ▼                  ▼                  ▼                  ▼
  Editor/IDE      git hooks          CI Pipeline       Runtime
  + Linting       + Dependency       + SBOM Gen        + SCA
                  Check              + CVE Scan       + Runtime
```

---

## OWASP Check Dependency

**OWASP Dependency-Check** es una herramienta que analiza proyectos para detectar dependencias con vulnerabilidades conocidas (CVEs).

### Integración con Git Hooks (Pre-Commit/Pre-Push)

#### Pre-Commit Hook (antes de confirmar)

```bash
# .git/hooks/pre-commit
#!/bin/bash

echo "🔍 Ejecutando análisis de dependencias..."

# Ejecutar dependency-check (requiere Java)
dependency-check.sh \
  --project "mi-proyecto" \
  --scan ./src \
  --format JSON \
  --output ./reports

# Verificar si hay vulnerabilidades críticas
CRITICAL=$(grep -c '"cwe".*"critical"' ./reports/*.json 2>/dev/null || true)

if [ "$CRITICAL" -gt 0 ]; then
  echo "❌ ERROR: Se encontraron $CRITICAL vulnerabilidades críticas"
  echo "   NO se permite el commit hasta resolverlas"
  exit 1
fi

echo "✅ Análisis completado - Commit permitido"
exit 0
```

#### Pre-Push Hook (antes de subir)

```bash
# .git/hooks/pre-push
#!/bin/bash

echo "🔍 Ejecutando análisis completo de SBOM..."

# 1. Generar SBOM CycloneDX
syft . -o cyclonedx-json > sbom.json

# 2. Ejecutar dependency-check con threshold
dependency-check.sh \
  --project "mi-proyecto" \
  --assembly \
  --failOnHigh \
  --highThreshold 7 \
  --cveValidForHours 24

EXIT_CODE=$?

if [ $EXIT_CODE -ne 0 ]; then
  echo "❌ ERROR: Vulnerabilidades detectadas (threshold excedido)"
  echo "   Corrige los problemas antes de hacer push"
  exit 1
fi

echo "✅ SBOM generado y validado - Push permitido"
exit 0
```

---

## Hooks con npm/np para JavaScript/TypeScript

### Pre-Commit: npm audit en pre-commit

```bash
# Install pre-commit hook
npm install --save-dev pre-commit

# package.json
{
  "pre-commit": [
    "npm audit --audit-level=high",
    "npm run sbom:check"
  ]
}
```

```bash
# Script en package.json
"scripts": {
  "sbom:check": "syft . -o cyclonedx-json | jq '.vulnerabilities[] | select(.severity == \"Critical\")' && exit 1"
}
```

### Pre-Push: Verificación obligatoria

```bash
# Install husky para git hooks
npm install --save-dev husky

# Inicializar husky
npx husky install

# Crear hook pre-push
npx husky add .husky/pre-push 'npm run security:check'

# package.json
"scripts": {
  "security:check": "npm audit --audit-level=high && npm outdated --depth=0"
}
```

---

## Herramientas de Análisis de SBOM y Dependencias

### Herramientas CLI

| Herramienta | Tipo | Lenguaje | Características |
|-------------|------|----------|------------------|
| **Syft** | SBOM Generator | Go | Genera SBOM en múltiples formatos (CycloneDX, SPDX) |
| **Trivy** | SCA + SBOM | Go | Escanea vulnerabilidades y genera SBOM |
| **OWASP Dependency-Check** | SCA | Java | Detecta CVEs en dependencias |
| **npm audit** | SCA | Node.js | Auditoría de paquetes npm |
| **Safety** | SCA | Python | Vulnerabilidades en Python |
| **Bundler-audit** | SCA | Ruby | Gemas con vulnerabilidades en Ruby |
| **Retire.js** | SCA | JS | Librerías JavaScript vulnerables |
| **FOSSA** | SCA/SBOM | Multi | Análisis completo con UI |

### Integraciones CI/CD

| Herramienta | CI Soportada | Función |
|-------------|-------------|---------|
| **GitHub Advisory Database** | GitHub Actions | Alertas de seguridad automáticas |
| **Dependabot** | GitHub | Actualización automática de dependencias |
| **Renovate** | GitHub/GitLab | Automated dependency updates |
| **Snyk** | Multi | SCA + contenedor + IaC |
| **Sonatype Nexus** | Multi | Repository + security |
| ** JFrog Xray** | Multi | Continuous security |

---

## Ejemplo Completo: Git Hooks con Pre-Push

### Estructura del Proyecto

```
mi-proyecto/
├── .husky/
│   └── pre-push
├── src/
├── package.json
└── reports/
```

### Implementación

```bash
# 1. Instalar dependencias
npm install --save-dev @anthropic-ai/claude-code-sbom-tools

# 2. Configurar pre-push hook
cat > .husky/pre-push << 'EOF'
#!/bin/sh

echo "🔒 Verificando seguridad de dependencias..."

# Generar SBOM
echo "📦 Generando SBOM CycloneDX..."
npx syft . -o cyclonedx-json > reports/sbom.json

# Verificar vulnerabilidades
echo "🔍 Escaneando vulnerabilidades..."
npx trivy fs --severity HIGH,CRITICAL --exit-code 1 .

# Verificar licenses
echo "📜 Verificando licencias..."
npx license-checker --failOn "GPLv3,SSPL,AGPL"

echo "✅ Todas las verificaciones pasaron"
EOF

chmod +x .husky/pre-push
```

### Si Hay Error: Bloquea el Push

```bash
# El hook sale con código 1 si hay errores
# Esto bloquea automáticamente el push
exit 1  # Bloquea el push
exit 0  # Permite el push
```

---

## Políticas de Verificación

### Por Nivel de Severidad

| Severity | Acción en Pre-Commit | Acción en Pre-Push |
|----------|---------------------|-------------------|
| **CRITICAL** | Bloquear | Bloquear |
| **HIGH** | Advertir | Bloquear |
| **MEDIUM** | Advertir | Advertir |
| **LOW** | Ignorar | Ignorar |

### Por Tipo de Check

- **CVE Check**: Obligatorio en ambas etapas
- **License Check**: Obligatorio en pre-push
- **SBOM Generation**: En pre-push (versionar el SBOM)
- **Outdated Check**: Opcional, advertír en pre-commit

---

## Mejores Prácticas

1. **Ejecutar análisis localmente** antes de commit/push para evitar ida-y-vuelta
2. **Usar cache local** para acelerar análisis repetidos
3. **Configurar threshold** apropiados por proyecto
4. **Versionar el SBOM** junto con el código ( traceability)
5. **Integrar con CI/CD** como segunda línea de defensa
6. **Automatizar actualizaciones** de dependencias vulnerables (Dependabot/Renovate)
7. **Monitorear advisory databases** para nueva vulnerabilidades

---

## Referencias

- [CycloneDX Specification](https://cyclonedx.org/)
- [SPDX Specification](https://spdx.github.io/spdx-spec/)
- [OWASP Dependency-Check](https://owasp.org/www-project-dependency-check/)
- [Syft](https://github.com/anchore/syft)
- [Trivy](https://aquasecurity.github.io/trivy/)