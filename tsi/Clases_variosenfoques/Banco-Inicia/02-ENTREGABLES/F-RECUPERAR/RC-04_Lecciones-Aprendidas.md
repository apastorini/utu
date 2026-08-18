# RC-04 · Lecciones Aprendidas y Mejora Continua del SGSI del Banco

> ⚠️ **Alerta:** este documento menciona **nombres propios del organigrama del Banco** (personas y cargos, abril 2026). Antes de usar el documento, verificá la vigencia de esos nombres contra el organigrama actual.
> **Función del MCU 5.0:** Identificar (ID.IM — Mejora) · Recuperar (RC.RP — Ejecución del plan de recuperación)
> **ISO/IEC 27001:** Cláusula 10 (Mejora) · A.5.24/A.5.25 (incidentes)
> **BCU:** Circular 2227 (riesgo operativo)
> **URCDP:** Ley 18.331 art. 10 · Ley 19.670 art. 38
> **Nivel del curso:** 🟢 Descubrir · 🟡 Practicar

## 1. Qué es y por qué existe
Este procedimiento cierra el ciclo de vida de un incidente o de un simulacro: convierte la experiencia en **mejoras concretas** del SGSI. Sin lecciones aprendidas, el Banco repetiría los mismos errores en cada crisis: el mismo hallazgo del pentest, la misma demora en la notificación, la misma falla del plan que ya se detectó en el simulacro anterior.
La mejora continua es un requisito explícito: la ISO/IEC 27001 (cláusula 10) exige corregir no conformidades y mejorar el SGSI; el MCU 5.0 (ID.IM) pide que los procesos de ciberseguridad se revisen y mejoren; y la Circular 2227 del BCU espera que los eventos de riesgo operativo produzcan acciones correctivas con seguimiento.
El corazón del proceso es el **informe de lecciones aprendidas** elaborado después de cada incidente o simulacro: qué pasó, por qué pasó (análisis de causa raíz), qué salió bien, qué salió mal y qué se va a cambiar. Las acciones se registran, se les asigna dueño y plazo, y se sigue su estado hasta el cierre en el Comité de Seguridad.
## 2. Marco de referencia
| **Norma** | **Referencia** | **Qué exige** |
|---|---|---|
| **MCU 5.0 (Agesic)** | ID.IM | Mejorar los procesos de ciberseguridad con base en la experiencia |
| **ISO/IEC 27001:2022** | Cláusula 10 | Mejora continua: corrección de no conformidades |
| **BCU** | Circular 2227 | Acciones correctivas derivadas de eventos de riesgo operativo |
| **URCDP** | Ley 18.331 art. 10 · Ley 19.670 art. 38 | Adecuar las medidas de seguridad tras cada vulneración |

## 3. Cómo completar esta plantilla (guía de llenado)
1. **Disparadores del proceso** con el RSI: qué activa un informe de lecciones aprendidas (incidente real de severidad media o mayor, simulacro, hallazgo recurrente, no conformidad de auditoría).
2. **Definí el análisis de causa raíz** con la División TI y los dueños de proceso: método (5 porqués, Ishikawa) y quién lo facilita.
3. **Armá el plan de acciones** con el RSI: acciones correctivas y preventivas, dueño, plazo y prioridad.
4. **Establecé el seguimiento** con el Comité de Seguridad: reporte periódico de estado hasta el cierre.
5. **Definí los indicadores de mejora** con el RSI y la División Planificación Estratégica: métricas de incidentes y de madurez del SGSI.
6. Consultá a **Auditoría Interna** (Cr. Marcelo Jorge) para integrar las no conformidades de auditoría y al **DPD** cuando las lecciones toquen datos personales.
## 4. Plantilla del documento

### ENCABEZADO
| **Campo** | **Valor** |
|---|---|
| **Código** | RC-04 |
| **Título** | Lecciones Aprendidas y Mejora Continua |
| **Versión** | 1.0 |
| **Estado** | [Borrador / En revisión / Aprobado] |
| **Fecha de aprobación** | [COMPLETAR] |
| **Elaborado por** | RSI |
| **Revisado por** | Comité de Seguridad de la Información |
| **Aprobado por** | Directorio |
| **Clasificación** | Uso interno |
| **Próxima revisión** | [Fecha, máx. 1 año] |

### 1. Objetivo
Convertir la experiencia de incidentes, simulacros y auditorías en mejoras concretas y verificables del SGSI del Banco, mediante el análisis de causas, acciones correctivas y preventivas, y su seguimiento hasta el cierre.
### 2. Disparadores del proceso
Se elabora informe de lecciones aprendidas cuando:
- Se produce un incidente de severidad [COMPLETAR: media o mayor] (RS-01).
- Se ejecuta un simulacro de [COMPLETAR: BCP/DRP] con desvíos frente a RTO/RPO.
- Una auditoría (interna, BCU, Agesic) detecta una no conformidad.
- Se detecta un hallazgo recurrente en pruebas (DE-03) o en el monitoreo (DE-02).
- [COMPLETAR: otros criterios definidos por el Comité].
### 3. Informe de lecciones aprendidas (contenido)
| **Sección** | **Contenido** |
|---|---|
| **Resumen** | Qué ocurrió, cuándo, impacto |
| **Línea de tiempo** | Hitos de detección, respuesta y recuperación |
| **Análisis de causa raíz** | Causas de fondo (no solo síntomas) |
| **Qué funcionó** | Controles y decisiones que evitaron más daño |
| **Qué falló** | Desvíos, demoras, controles inexistentes o ineficaces |
| **Acciones correctivas** | Qué se cambia, dueño, plazo, prioridad |
| **Acciones preventivas** | Cómo evitar la recurrencia |
| **Indicadores de seguimiento** | Métricas que demostrarán la mejora |

### 4. Análisis de causa raíz
Se aplica el método [COMPLETAR: 5 porqués / diagrama de Ishikawa] facilitado por el RSI, con participación de la División TI y los dueños de proceso afectados. El resultado distingue: causa técnica, causa de proceso y causa de gobernanza.
### 5. Plan de acciones correctivas y preventivas
| **N.º** | **Acción** | **Tipo** | **Responsable** | **Plazo** | **Prioridad** | **Estado** |
|---|---|---|---|---|---|---|
| 1 | [COMPLETAR] | [Correctiva / Preventiva] | [COMPLETAR] | [COMPLETAR] | [Alta/Media] | [Abierta] |
| 2 | [COMPLETAR] | [Correctiva / Preventiva] | [COMPLETAR] | [COMPLETAR] | [COMPLETAR] | [COMPLETAR] |

### 6. Seguimiento hasta el cierre
El RSI mantiene el **registro de acciones** y reporta su estado [COMPLETAR: mensualmente / en cada Comité]. Una acción se cierra cuando se evidencia su implementación (evidencia verificable) y, cuando corresponde, se verifica la efectividad [COMPLETAR: re-test, prueba, revisión].
### 7. Actualización de políticas y planes
Las lecciones aprendidas pueden modificar: políticas y procedimientos del SGSI (control de cambios de cada documento), planes de RS-01/RC-01/RC-02, reglas de detección de DE-02, y contenidos de capacitación (PR-02).
### 8. Indicadores de mejora
| **Indicador** | **Fórmula** | **Meta** |
|---|---|---|
| Tiempo medio de detección | Promedio de horas detección-incidencia | [COMPLETAR] |
| Tiempo medio de contención | Promedio de horas | [COMPLETAR] |
| % de acciones correctivas cerradas en plazo | Cerradas / total | [COMPLETAR: ≥ 90 %] |
| % de simulacros sin desvíos críticos | Aprobados / total | [COMPLETAR] |
| Nivel de madurez del MCU 5.0 | Autoevaluación anual | [COMPLETAR: subir 1 nivel] |

### 9. Revisión en el Comité
El Comité de Seguridad revisa [COMPLETAR: semestralmente] los informes de lecciones aprendidas, prioriza las acciones de mayor impacto y eleva al Directorio el informe de estado del SGSI (GV-06).
### 10. Control de cambios
| **Versión** | **Fecha** | **Cambio** | **Elaboró** | **Aprobó** |
|---|---|---|---|---|
| 0.1 | [COMPLETAR] | Versión inicial (borrador) | RSI | — |
| 1.0 | [COMPLETAR] | Aprobación del Directorio | RSI | Directorio |

## 5. Ejemplo aplicado al Banco (modelo de referencia)
Ejemplo ilustrativo. Adaptá a los incidentes y simulacros reales del Banco.
**Caso: simulacro de ransomware (ejemplo):**
- **Resultado:** el simulacro de RS-01/RC-02 del [mes] mostró que la contención demoró 5 horas (objetivo 4 h) porque no estaba claro quién autorizaba el aislamiento del core.
- **Causa raíz (5 porqués):** demora en la decisión → no había procedimiento de aislamiento de emergencia → los roles del plan no incluían la autorización → el plan no se había ejercitado con ese caso.
- **Acciones correctivas:** se agregó al plan el rol de "autorizador de aislamiento" (Gerente Div. TI o suplente) con facultad de decidir sin comité; se actualizó RS-01 (control de cambios).
- **Acciones preventivas:** se incluyó el caso de ransomware en la campaña de concientización (PR-02) y se revisaron las reglas de detección de DE-02 para alertas tempranas.
- **Seguimiento:** las 3 acciones se cerraron en 30 días con evidencia; el simulacro siguiente (90 días) logró contención en 3 h 30 min.
- **Comité:** el caso se presentó en el Comité de Seguridad; el indicador "tiempo de contención" pasó de 5 h a 3 h 30 min y se informó la tendencia al Directorio (GV-06).

**Documentos relacionados:**
- RS-01 (Respuesta a Incidentes) · RS-02 (Notificación) · RS-03 (Forense)
- RC-01 (BCP) · RC-02 (DRP) · RC-03 (Comunicación de Crisis)
- GV-06 (Informe del RSI a la Dirección) · DE-02 (Detección) · PR-02 (Concientización)
