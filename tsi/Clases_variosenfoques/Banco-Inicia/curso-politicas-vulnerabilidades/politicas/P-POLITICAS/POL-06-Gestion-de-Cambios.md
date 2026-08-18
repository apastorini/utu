# POL-06 · Política de Gestión de Cambios

> **Función del MCU 5.0:** Proteger (PR.IP — mantenimiento) · Gobernar (GV) · Recuperar (RC)
> **ISO/IEC 27001:** A.8.32 (gestión de cambios) · A.8.31 (entorno de desarrollo) · A.8.25-A.8.26 (seguridad en desarrollo)
> **BCU:** RNRCSF / EMG — los cambios no controlados son una causa frecuente de incidentes de TIC
> **URCDP:** Ley 18.331 art. 10 — los cambios deben preservar las medidas de seguridad de los tratamientos
> **Nivel del curso:** 🔴 Dominar

---

### ENCABEZADO
| **Campo** | **Valor** |
|---|---|
| **Código** | POL-06 |
| **Título** | Gestión de Cambios |
| **Versión** | 1.0 |
| **Estado** | [Borrador / En revisión / Aprobado] |
| **Fecha de aprobación** | [COMPLETAR] |
| **Elaborado por** | Div. TI + RSI |
| **Revisado por** | Comité de Cambios · Producción |
| **Aprobado por** | Comité de Cambios / Comité de Seguridad |
| **Clasificación** | Uso interno |
| **Próxima revisión** | [Fecha, máx. 1 año] |

### 1. Objetivo
Garantizar que **todo cambio** en sistemas, aplicaciones, infraestructura, configuraciones y datos se **planifique, apruebe, pruebe, ejecute, documente y pueda revertirse** (rollback), minimizando el impacto en la operación y la seguridad.

### 2. Alcance
Aplica a cambios en: hardware, software (instalación/actualización), configuraciones de red/seguridad, bases de datos, reglas de firewall/WAF/DLP, firmware, entornos de producción y cambios de procedimientos críticos.

### 3. Tipos de cambio
| Tipo | Descripción | Ejemplo |
|---|---|---|
| **Estándar** | Bajo riesgo, preaprobado | Actualización de antivirus de firma |
| **Normal** | Riesgo medio, requiere RFC y aprobación | Cambio de versión de un sistema |
| **Emergencia** | Crítico y urgente (incidente, parche de seguridad) | Parche crítico, mitigación de ataque |

### 4. Reglas obligatorias
- Todo cambio se gestiona mediante **Solicitud de Cambio (RFC)** (PRO-07) y queda registrado.
- Todo cambio **debe tener plan de reversión (rollback)** y prueba previa en homologación cuando aplique.
- Los cambios se ejecutan en **ventanas de mantenimiento** aprobadas y con comunicación a los afectados.
- Los cambios **emergencia** siguen el flujo acelerado (PRO-07) y se documentan posteriormente.
- **Cambios de seguridad** (firewall, DLP, WAF, reglas de acceso) requieren además visto bueno del RSI.
- Prohibido realizar cambios en producción sin aprobación (salvo emergencia declarada con registro).
- Después de cada cambio, se **verifica** la operación y se registra el resultado (éxito/fallo/reversión).

### 5. Cumplimiento
Los cambios no autorizados se investigan como incidente (PCS-03) y pueden dar lugar a medidas disciplinarias.

### 6. Excepciones
Solo por PRO-11, con autorización del Comité de Cambios y del RSI.

### 7. Revisión
Revisión anual; el proceso (PCS-05) se evalúa con métricas (tasa de éxito, rollbacks, cambios emergencia).

### Evidencia del kit
| Evidencia | Documento canónico |
|---|---|
| RFC completas | PR-07, BCU-04 |
| Actas del Comité de Cambios | BCU-04, GV-02 |
| Registro de rollback | PR-07 |
| Plan de prueba | POL-15 (SDLC) |
| Proceso de cambios | PCS-05, PRO-07 |
