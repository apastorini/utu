# POL-07 · Política de Gestión de Incidentes y Respuesta

> **Función del MCU 5.0:** Detectar (DE) · Responder (RS) · Recuperar (RC)
> **ISO/IEC 27001:** A.5.24-A.5.28 (gestión de incidentes, mejora) · A.8.15-A.8.16 (registros)
> **BCU:** RNRCSF — gestión de incidentes y notificación de eventos de ciberseguridad
> **URCDP:** Ley 18.331 art. 27-bis · Decreto 64/020 — notificación de vulneraciones de datos personales en 72 horas
> **Decreto 66/025:** Notificación de incidentes al CERTuy
> **Nivel del curso:** 🔴 Dominar

---

### ENCABEZADO
| **Campo** | **Valor** |
|---|---|
| **Código** | POL-07 |
| **Título** | Gestión de Incidentes y Respuesta |
| **Versión** | 1.0 |
| **Estado** | [Borrador / En revisión / Aprobado] |
| **Fecha de aprobación** | [COMPLETAR] |
| **Elaborado por** | RSI + CSIRT del Banco |
| **Revisado por** | Comité de Seguridad · Comunicación · Legales |
| **Aprobado por** | Dirección General |
| **Clasificación** | Confidencial |
| **Próxima revisión** | [Fecha, máx. 1 año] |

### 1. Objetivo
Definir cómo el Banco **detecta, clasifica, contiene, erradica, recupera y aprende** de los incidentes de seguridad, protegiendo la evidencia, cumpliendo las obligaciones de notificación (URCDP, CERTuy, BCU) y minimizando el impacto.

### 2. Alcance
Aplica a todo incidente o sospecha de incidente que afecte la confidencialidad, integridad o disponibilidad de la información o los sistemas del Banco, incluidos incidentes de datos personales.

### 3. Clasificación de incidentes
| Nivel | Descripción | Respuesta |
|---|---|---|
| **N1 Crítico** | Impacto alto en negocio o datos (ransomware, fuga masiva, indisponibilidad de servicios críticos) | CSIRT + crisis; notificación según plazos |
| **N2 Alto** | Impacto medio-alto (cuenta comprometida, malware en estaciones) | CSIRT; contención en 4 h |
| **N3 Medio** | Impacto bajo-medio (phishing reportado, escaneo sospechoso) | Respuesta operativa |
| **N4 Bajo** | Sospecha o evento menor | Registro y monitoreo |

### 4. Reglas obligatorias
- **Todo el personal** debe reportar incidentes y sospechas (PRO-04) por el canal establecido, sin demora.
- **No se apagan máquinas ni se "investiga por cuenta propia"** antes de preservar evidencia (orden de volatilidad).
- El CSIRT/RSI es el **único canal oficial** de respuesta; las comunicaciones externas se coordinan con Legales/Comunicación.
- Toda respuesta se **registra** (bitácora de incidentes, PCS-03) y las evidencias se preservan con cadena de custodia.
- **Notificaciones** según plazos legales (PRO-05): URCDP (72 h, datos personales), CERTuy (Decreto 66/025), BCU.
- Las **lecciones aprendidas** se documentan y generan mejoras (RC-04).

### 5. Equipo y funciones
| Rol | Función |
|---|---|
| **RSI** | Conduce la respuesta, decide clasificación y notificaciones |
| **CSIRT / Operaciones de Seguridad** | Analiza, contiene y erradica |
| **Div. TI / Producción** | Recupera servicios y aplica remediación |
| **Legales** | Asesora en obligaciones y comunicación |
| **Comunicación** | Gestiona la comunicación interna/externa |
| **DPD** | Evalúa la notificación de datos personales |

### 6. Cumplimiento
Ocultar o retrasar el reporte de un incidente es falta grave. La no notificación de vulneraciones de datos personales expone al Banco a sanciones de la URCDP (Ley 18.331 art. 39).

### 7. Excepciones y revisión
No aplica excepciones a la obligación de reportar. Revisión anual de la política, del proceso (PCS-03) y de los procedimientos (PRO-04, PRO-05); simulacros periódicos.

### Evidencia del kit
| Evidencia | Documento canónico |
|---|---|
| Bitácora de incidentes | RS-01, DE-02 |
| Procedimiento de respuesta inicial | PRO-04 |
| Procedimiento de notificación | PRO-05 |
| Plan de respuesta y comunicación | RS-01, RS-02 |
| Lecciones aprendidas | RC-04 |
