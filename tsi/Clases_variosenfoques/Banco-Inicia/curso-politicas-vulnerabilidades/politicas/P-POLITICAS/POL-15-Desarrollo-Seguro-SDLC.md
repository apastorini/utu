# POL-15 · Política de Desarrollo Seguro (SDLC)

> **Función del MCU 5.0:** Proteger (PR.PS — seguridad de plataformas y aplicaciones)
> **ISO/IEC 27001:** A.8.25-A.8.28 (seguridad en desarrollo) · A.8.31 (entornos) · A.8.9 (configuraciones)
> **BCU:** EMG / RNRCSF — el desarrollo de software (interno y externo) debe ser seguro desde el diseño
> **URCDP:** Ley 18.331 art. 10 y 27 — las aplicaciones que tratan datos personales deben garantizar seguridad por diseño
> **Nivel del curso:** 🔴 Dominar

---

### ENCABEZADO
| **Campo** | **Valor** |
|---|---|
| **Código** | POL-15 |
| **Título** | Desarrollo Seguro (SDLC) |
| **Versión** | 1.0 |
| **Estado** | [Borrador / En revisión / Aprobado] |
| **Fecha de aprobación** | [COMPLETAR] |
| **Elaborado por** | Div. Desarrollo + RSI |
| **Revisado por** | Comité de Seguridad · QA |
| **Aprobado por** | Comité de Seguridad de la Información |
| **Clasificación** | Confidencial |
| **Próxima revisión** | [Fecha, máx. 1 año] |

### 1. Objetivo
Incorporar la **seguridad en todo el ciclo de vida del software** (análisis, diseño, desarrollo, pruebas, despliegue, mantenimiento y retiro), reduciendo vulnerabilidades en las aplicaciones del Banco.

### 2. Alcance
Aplica a todo el desarrollo de software (interno, contratado o de proveedores), aplicaciones nuevas y existentes, código, dependencias, contenedores, APIs, bases de datos e integraciones.

### 3. Reglas obligatorias por etapa
| Etapa | Control |
|---|---|
| **Requisitos** | Requisitos de seguridad y privacidad desde el inicio (security/privacy by design) |
| **Diseño** | Modelado de amenazas (STRIDE) y diseño seguro; revisión de arquitectura |
| **Desarrollo** | Estándares de codificación segura (OWASP ASVS), repositorios con control de versiones |
| **Análisis estático (SAST)** | Escaneo de código (Bandit, Semgrep) en cada integración |
| **Dependencias** | Auditoría de dependencias (pip-audit, Trivy, Gitleaks para secretos) |
| **Pruebas** | Pruebas de seguridad (DAST/OWASP ZAP), pruebas funcionales y de regresión |
| **Despliegue** | Cambios mediante POL-06, entornos separados (dev/QA/prod), hardening de configuración |
| **Mantenimiento** | Gestión de vulnerabilidades (POL-05) y revisión continua |
| **Retiro** | Baja segura de servicios y datos |

### 4. Entornos
- Separación estricta entre **desarrollo, homologación y producción**.
- Prohibido usar **datos reales de clientes** en entornos de prueba (se usan datos sintéticos/anonimizados — POL-20).
- Accesos a los entornos según POL-04 (menor privilegio).

### 5. Código y herramientas de IA
- El código generado o asistido por IA pasa el **mismo proceso de revisión y escaneo** que el código manual (POL-17, curso AISEC).
- El código no se sube a herramientas externas no autorizadas (POL-02, POL-17).

### 6. Responsabilidades
- **Desarrollo**: codifica de forma segura y corrige hallazgos.
- **QA**: ejecuta y verifica pruebas de seguridad.
- **RSI**: define estándares y prioriza hallazgos de seguridad.
- **DPD**: evalúa la protección de datos en las aplicaciones.

### 7. Cumplimiento y revisión
Las aplicaciones con vulnerabilidades críticas no se despliegan a producción. Revisión anual de la política y de los estándares.

### Evidencia del kit
| Evidencia | Documento canónico |
|---|---|
| Estándares de codificación | PR-07 |
| Resultados SAST/DAST | PR-07, Actividades 05-08 |
| Auditoría de dependencias | Actividad 06 |
| Modelado de amenazas | Actividad 13 |
| Gestión de cambios | POL-06, PR-07 |
| Datos de prueba anonimizados | POL-20 |
