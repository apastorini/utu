# POL-08 · Política de Continuidad del Negocio y Respaldos

> **Función del MCU 5.0:** Recuperar (RC.RP — planes de recuperación; RC.CO — comunicación) · Proteger (PR.DS — respaldos)
> **ISO/IEC 27001:** A.5.29-A.5.30 (continuidad y redundancia) · A.8.13 (respaldo de información) · A.8.14 (redundancia)
> **BCU:** EMG / RNRCSF — la continuidad del negocio y los respaldos son estándares mínimos de gestión
> **URCDP:** Ley 18.331 art. 10 — los respaldos protegen la disponibilidad e integridad de los datos personales
> **Nivel del curso:** 🔴 Dominar

---

### ENCABEZADO
| **Campo** | **Valor** |
|---|---|
| **Código** | POL-08 |
| **Título** | Continuidad del Negocio y Respaldos |
| **Versión** | 1.0 |
| **Estado** | [Borrador / En revisión / Aprobado] |
| **Fecha de aprobación** | [COMPLETAR] |
| **Elaborado por** | RSI + Continuidad (BCP) + Div. TI |
| **Revisado por** | Comité de Continuidad · Producción |
| **Aprobado por** | Dirección General |
| **Clasificación** | Confidencial |
| **Próxima revisión** | [Fecha, máx. 1 año] |

### 1. Objetivo
Garantizar que el Banco pueda **continuar operando y recuperarse** ante interrupciones (ciberseguridad, desastres, fallas), y que la información crítica se **respalde y se pueda restaurar** dentro de los plazos definidos.

### 2. Alcance
Aplica a procesos y servicios críticos, sistemas, datos, aplicaciones, infraestructura, sedes y personal clave del Banco, y a las pruebas periódicas del plan.

### 3. Objetivos de recuperación
| Sigla | Significado | Valor objetivo |
|---|---|---|
| **RTO** | Tiempo máximo para recuperar el servicio | [COMPLETAR: 24 h] |
| **RPO** | Pérdida máxima de datos aceptable | [COMPLETAR: 24 h] |

### 4. Respaldos
- Todo dato crítico se respalda según frecuencia [COMPLETAR: diaria incremental + semanal completa].
- Los respaldos se **cifran** (POL-14) y se almacenan **fuera del sitio** (sede secundaria o nube contratada).
- Se conservan copias **históricas** para recuperar ante corrupción de datos o ransomware.
- Las **pruebas de restauración** se realizan al menos [COMPLETAR: mensual] y se documentan (PRO-06).
- El acceso a los respaldos se controla (POL-04) y su ejecución se registra (POL-13).

### 5. Plan de continuidad
- Se identifican **procesos críticos** y su prioridad de recuperación (BIA).
- El **BCP/DRP** define estrategias, responsables, sedes alternativas y comunicación de crisis (RC-01…RC-03).
- El plan se **prueba** al menos [COMPLETAR: anualmente] con simulacros y se actualiza.
- Se definen **canales de comunicación de emergencia** y roles de decisión.

### 6. Reglas obligatorias
- Los respaldos no se almacenan en el mismo sitio que los datos originales.
- Un respaldo que **no se probó** no cuenta como respaldo.
- Ante un incidente (POL-07), la recuperación se coordina con el CSIRT para no restaurar máquinas infectadas.
- Las excepciones de cobertura de continuidad se aprueban por el Comité de Continuidad.

### 7. Cumplimiento y revisión
El incumplimiento de los plazos de respaldo o prueba se reporta al Comité. Revisión anual de la política; pruebas periódicas del plan y de restauración.

### Evidencia del kit
| Evidencia | Documento canónico |
|---|---|
| Plan de continuidad | RC-01, RC-02, RC-03 |
| Registro de respaldos | PR-05 |
| Pruebas de restauración | PRO-06, RC-02 |
| Análisis de impacto (BIA) | ID-02, BCU-02 |
| Simulacros realizados | RC-04 |
