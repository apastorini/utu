# BCU-02 · Marco de Gestión de Riesgos (Apetito y Adopción de Riesgo Tecnológico) del Banco

> ⚠️ **Alerta:** este documento menciona **nombres propios del organigrama del Banco** (personas y cargos, abril 2026). Antes de usar el documento, verificá la vigencia de esos nombres contra el organigrama actual.
> **Función del MCU 5.0:** Gobernar (GV.RM — Estrategia de riesgos) · Identificar (ID.RA — Evaluación de riesgos)
> **ISO/IEC 27001:** Cláusula 6.1 (Planificación) · ISO/IEC 27005 (gestión del riesgo)
> **BCU:** Estándares Mínimos de Gestión — Marco de gestión de riesgos · Circular 2227 (riesgo operativo)
> **URCDP:** Ley 18.331 art. 10 · Decreto 64/020 art. 6 lit. f (evaluación de impacto, caso de alto riesgo)
> **Nivel del curso:** 🟡 Practicar · 🔴 Dominar

## 1. Qué es y por qué existe
El BCU exige que la gestión del riesgo tecnológico no sea una serie de controles aislados, sino un **marco de gestión** con apetito, tolerancia, proceso formal y decisiones documentadas. Este documento define ese marco: cómo el Banco identifica, evalúa, mide, controla y monitorea los riesgos tecnológicos, y cómo adopta de manera consciente los riesgos residuales que decide aceptar.
El concepto clave de los EMG es la **adopción del riesgo**: un riesgo no tratado plenamente no es una omisión, es una **decisión de negocio** que debe quedar documentada, firmada al nivel adecuado y sujeta a seguimiento. La Circular 2227 integra el riesgo tecnológico dentro del riesgo operativo, por lo que este marco debe alinearse con la gestión de riesgo operativo del Área de Riesgos del Banco.
Sin apetito de riesgo definido no hay manera de juzgar si un nivel de exposición es aceptable. Este documento, con BCU-01 (gobierno), BCU-03 (segunda línea) y la metodología ID-02/ID-03, forma el núcleo que el supervisor revisa ante cualquier incidente: qué riesgo estaba aceptado, quién lo aceptó y con qué fundamento.
## 2. Marco de referencia
| **Marco** | **Referencia** | **Qué exige** |
|---|---|---|
| **MCU 5.0 (Agesic)** | GV.RM · ID.RA | Estrategia de riesgos alineada a los objetivos, evaluación y tratamiento continuo, registro de riesgos |
| **ISO/IEC 27001** | Cláusula 6.1 · ISO/IEC 27005 | Proceso sistemático de identificación, análisis, evaluación y tratamiento; criterios de aceptación |
| **BCU** | EMG · Marco de gestión de riesgos · Circular 2227 | Identificación, medición, control y monitoreo del riesgo operativo/tecnológico; aceptación documentada |
| **URCDP** | Ley 18.331 art. 10 · Decreto 64/020 art. 6 lit. f | Los tratamientos de alto riesgo para los titulares requieren evaluación de impacto previa |

## 3. Cómo completar esta plantilla (guía de llenado)
1. **Completá el encabezado** con los datos del documento.
2. **Definí los niveles de apetito y tolerancia** de forma concreta (umbrales medibles), no con frases genéricas.
3. **Adoptá la metodología de riesgo** de ID-02/ID-03 (matrices de probabilidad e impacto) y citala, no la reproduzcas completa aquí.
4. **Definí la taxonomía de riesgos** tecnológicos propia del Banco (acceso, disponibilidad, integridad, fraude informático, terceros, continuidad, datos personales).
5. **Establecé los niveles de autoridad para aceptar riesgos residuales** (quién puede aceptar qué nivel de exposición).
6. **Vinculá el proceso con la Circular 2227**: alineá plazos, reportes y registros con la gestión de riesgo operativo del Área de Riesgos.
7. **Actualizalo cuando cambie el perfil de riesgo** o la estrategia; no es un documento estático.
**A quién consultar en el Banco:** RSI (segunda línea) y Jefe de Riesgos No Financieros (Cra. Melissa Moraes) por la metodología y la integración con riesgo operativo; Gerente de Área Riesgos (Ec. Laura Zunino) por el apetito institucional; Comité de Seguridad de la Información por la aceptación de riesgos altos; Directorio por los riesgos residuales que excedan su apetito.
## 4. Plantilla del documento

### ENCABEZADO
| **Campo** | **Valor** |
|---|---|
| **Código** | BCU-02 |
| **Título** | Marco de Gestión de Riesgos (Apetito y Adopción de Riesgo) |
| **Versión** | 1.0 |
| **Estado** | [Borrador / En revisión / Aprobado] |
| **Fecha de aprobación** | [COMPLETAR] |
| **Elaborado por** | RSI |
| **Revisado por** | Comité de Seguridad de la Información / Área Riesgos |
| **Aprobado por** | Directorio |
| **Clasificación** | Uso interno |
| **Próxima revisión** | [Fecha, máx. 1 año] |

### 1. Objetivo
Definir el proceso de gestión de riesgos tecnológicos del Banco —identificación, evaluación, tratamiento, monitoreo y reporte— y las reglas de apetito, tolerancia y aceptación documentada de riesgos residuales, en cumplimiento de los Estándares Mínimos de Gestión del BCU y la Circular 2227.
### 2. Alcance
Aplica a [COMPLETAR: todos los riesgos tecnológicos del Banco, incluidos los derivados de terceros, de los procesos de negocio soportados por tecnología, de los datos personales y de la operación del sistema de pagos], como componente del riesgo operativo.
### 3. Apetito y tolerancia al riesgo
a) **Apetito de riesgo:** cantidad y tipo de riesgo tecnológico que el Banco está dispuesto a asumir para cumplir sus objetivos estratégicos [COMPLETAR: declaración y niveles por categoría].
b) **Tolerancia:** desviación máxima aceptada respecto del apetito, expresada en umbrales medibles (horas de indisponibilidad, número de incidentes, montos de pérdida, casos de exposición de datos).
c) **Declaraciones de tolerancia por categoría:** [COMPLETAR: tabla con categoría, indicador, umbral, responsable de monitoreo].
### 4. Proceso de gestión de riesgos tecnológicos
a) **Identificación:** inventario de riesgos a partir de los activos (ID-01), los procesos y el análisis de amenazas y vulnerabilidades.
b) **Evaluación:** análisis de probabilidad e impacto conforme a la metodología ID-02; se calcula el riesgo inherente y el residual.
c) **Tratamiento:** mitigación (controles), transferencia (seguros o contratos), evitación o **aceptación documentada**.
d) **Monitoreo:** indicadores de riesgo (KRI), revisión periódica y actualización del registro de riesgos.
e) **Reporte:** el estado de los riesgos y su tratamiento se reporta al Comité y al Directorio conforme a BCU-01.
### 5. Taxonomía de riesgos tecnológicos
| **Categoría** | **Ejemplos para el Banco** |
|---|---|
| Acceso y identidad | Credenciales comprometidas, privilegios excesivos, ingeniería social |
| Disponibilidad | Caída de sistemas críticos (crédito, ahorro, pagos), RTO/RPO |
| Integridad de datos | Alteración de registros de préstamos, corrupción de bases |
| Fraude informático | Estafas en canales, pagos no autorizados, manipulación de información |
| Terceros y cadena de suministro | Proveedores de TI, tercerizaciones (Circ. 2419-2422) |
| Continuidad | Pérdida del sitio, desastre natural, ciberataque con cifrado |
| Datos personales | Acceso indebido, filtración, incumplimiento de derechos ARCO |
| Cumplimiento | Incumplimiento normativo BCU, URCDP, Agesic |

### 6. Aceptación documentada de riesgos residuales
Todo riesgo residual que se decida aceptar se documenta en el Registro de Riesgos con: descripción, nivel de exposición, tratamiento aplicado, justificación de la aceptación, responsable, vigencia y fecha de revisión. Los niveles de autoridad para aceptar son [COMPLETAR: tabla con nivel de riesgo y autoridad: bajo=Jefe de Riesgos No Financieros; medio=RSI y Comité; alto=Comité y Directorio]. No se acepta un riesgo cuya materialización violaría la ley o pondría en peligro la estabilidad de la entidad.
### 7. Vínculo con el riesgo operativo (Circular 2227)
El proceso aquí definido es parte de la gestión de riesgo operativo del Banco: los riesgos tecnológicos se incorporan al registro de riesgo operativo, los incidentes tecnológicos se gestionan bajo el mismo esquema de incidentes y las pérdidas por eventos tecnológicos se registran y reportan conforme a la Circular 2227.
### 8. Registros y controles asociados
Registro de Riesgos Tecnológicos, Declaraciones de Aceptación de Riesgos, Indicadores de Riesgo (KRI), Informes al Comité y al Directorio, Evaluaciones de Impacto en Protección de Datos (URCDP-05) cuando el tratamiento implique alto riesgo para los titulares.
### Control de cambios
| **Versión** | **Fecha** | **Cambio** | **Elaboró** | **Aprobó** |
|---|---|---|---|---|
| 0.1 | [COMPLETAR] | Versión inicial (borrador) | RSI | — |
| 1.0 | [COMPLETAR] | Aprobación del Directorio | RSI | Directorio |

## 5. Ejemplo aplicado al Banco (modelo de referencia)
Ejemplo ilustrativo de cómo quedaría completado. Adaptá a la realidad institucional del Banco.
**Apetito (ejemplo):** "El Banco tiene apetito bajo por los riesgos de exposición de datos personales de clientes y por la indisponibilidad de los sistemas que soportan el crédito hipotecario, el ahorro y el sistema de pagos. No se aceptan riesgos que comprometan la continuidad de estos servicios por más de 4 horas en horario de operación."
**Tolerancia (ejemplo):**
| **Categoría** | **Indicador** | **Umbral** | **Monitoreo** |
|---|---|---|---|
| Disponibilidad | RTO de sistema central | ≤ 4 horas | División TI / RSI |
| Datos personales | Casos de exposición no autorizada | ≤ 5 casos/año | DPD |
| Fraude | Pérdida por fraude informático | ≤ USD 50.000/año | Riesgo Operacional |
| Incumplimiento | Hallazgos de auditoría sin corregir | 0 críticos al cierre | Auditoría Interna |

**Aceptación documentada (ejemplo):** en 2026 se detectó que el portal de atención al cliente (Banco En Línea) no contaba con autenticación multifactor para un segmento de usuarios. El riesgo residual (acceso indebido a datos de clientes por robo de credenciales) fue evaluado como ALTO y, en lugar de aceptarlo, se incorporó al Plan de Tratamiento de Riesgos con fecha de cierre [fecha]. La decisión quedó registrada y firmada por el Comité.
**Integración con Circular 2227 (ejemplo):** la pérdida operacional asociada a un incidente de TI se reporta al esquema de riesgo operativo con el evento, el importe y las lecciones aprendidas, y alimenta el registro único de eventos.

**Documentos relacionados:** BCU-01 (Gobierno), BCU-03 (Función de Seguridad), ID-01 (Activos), ID-02 (Metodología), ID-03 (Análisis de riesgos), ID-04 (Plan de tratamiento), ID-05 (Perfil de ciberseguridad), URCDP-05 (EIPD), GV-05 (Cadena de suministro).
