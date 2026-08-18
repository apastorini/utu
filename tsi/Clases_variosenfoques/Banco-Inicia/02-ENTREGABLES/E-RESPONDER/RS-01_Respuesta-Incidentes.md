# RS-01 · Plan de Respuesta a Incidentes de Seguridad del Banco
> **Función del MCU 5.0:** Responder (RS.MA — Planificación · RS.MI — Mitigación)
> **ISO/IEC 27001:** A.5.24 (Gestión de incidentes) · A.5.25 (Evaluación de incidentes) · ISO/IEC 27035
> **BCU:** Circular 2227 (riesgo operativo) · Estándares Mínimos de Gestión
> **URCDP:** Ley 18.331 art. 10 · Ley 19.670 art. 38 (base de la respuesta)
> **Nivel del curso:** 🔴 Dominar

## 1. Qué es y por qué existe
El **Plan de Respuesta a Incidentes** define cómo el Banco reacciona cuando ocurre un evento que puede afectar la confidencialidad, integridad o disponibilidad de su información. Es el documento que convierte el pánico en procedimiento: quién hace qué, en qué orden y en qué plazos, desde que se detecta la alerta (DE-02) hasta el cierre y las lecciones aprendidas (RC-04).
En un banco, la velocidad de la primera hora decide el costo final del incidente. La Circular 2227 del BCU (riesgo operativo) y la Ley 19.670 (art. 38) generan obligaciones con plazos estrictos: la URCDP debe recibir la notificación en máximo 72 horas y los procedimientos de minimización deben iniciarse en las primeras 24 horas. Nada de eso es posible sin roles definidos y sin practicar el plan.
Este plan no es estático: se ejercita con simulacros y se corrige con cada incidente real. Un plan que nadie ha probado es, en la práctica, un plan que no existe.
## 2. Marco de referencia
| **Norma** | **Referencia** | **Qué exige** |
|---|---|---|
| **MCU 5.0 (Agesic)** | RS.MA / RS.MI | Planificación de la respuesta y mitigación de incidentes |
| **ISO/IEC 27001:2022** | A.5.24 / A.5.25 · ISO 27035 | Gestión y evaluación de incidentes de seguridad |
| **BCU** | Circular 2227 · EMG | Gestión de riesgo operativo y eventos de pérdida |
| **URCDP** | Ley 19.670 art. 38 · Decreto 64/020 | Iniciar procedimientos en 24 h; comunicar a la URCDP en 72 h |

## 3. Cómo completar esta plantilla (guía de llenado)
1. **Definí evento vs. incidente** con el RSI: criterios claros para que cualquier funcionario sepa cuándo debe reportar.
2. **Armá el equipo de respuesta (CSIRT/CERT del Banco)** con la División TI, Servicios Jurídicos, Comunicaciones, Capital Humano y el DPD; definí suplentes.
3. **Establecé la clasificación de severidad y prioridad** con el Comité de Seguridad: impactos en dinero, datos personales, disponibilidad y reputación.
4. **Definí tiempos objetivo de respuesta** con la División TI y el RSI, y acordalos con el Directorio.
5. **Probalo con un simulacro** dentro de los primeros 90 días de aprobado y registrá los resultados en RC-04.
6. Consultá al **DPD** (vulneraciones de datos) y al **Oficial de Cumplimiento** (eventos de fraude/PLAFT) para las clasificaciones que activan notificaciones legales.
## 4. Plantilla del documento

### ENCABEZADO
| **Campo** | **Valor** |
|---|---|
| **Código** | RS-01 |
| **Título** | Plan de Respuesta a Incidentes de Seguridad |
| **Versión** | 1.0 |
| **Estado** | [Borrador / En revisión / Aprobado] |
| **Fecha de aprobación** | [COMPLETAR] |
| **Elaborado por** | RSI |
| **Revisado por** | Comité de Seguridad de la Información |
| **Aprobado por** | Directorio |
| **Clasificación** | Confidencial |
| **Próxima revisión** | [Fecha, máx. 1 año] |

### 1. Objetivo
Establecer un proceso probado y con plazos para detectar, clasificar, contener, erradicar, recuperar y cerrar los incidentes de seguridad que afecten al Banco, minimizando el impacto y cumpliendo las obligaciones legales.
### 2. Definiciones
| **Término** | **Definición** |
|---|---|
| **Evento** | Ocurrencia observable y no esperada en un sistema (ej. un login fallido masivo, un error de red) que puede o no ser un incidente |
| **Incidente** | Evento que amenaza la confidencialidad, integridad o disponibilidad de la información o los sistemas (compromiso real o probable) |
| **Vulneración de datos** | Incidente que afecta datos personales (activa la notificación de RS-02 / URCDP) |

### 3. Clasificación de severidad y prioridad
| **Severidad** | **Descripción** | **Ejemplo Banco** |
|---|---|---|
| **Crítica** | Indisponibilidad de un servicio esencial o compromiso de datos personales masivo | Ransomware en el core, fuga de la base de clientes |
| **Alta** | Impacto significativo en un servicio o fraude mayor | Banco En Línea caído en horario hábil, transferencia fraudulenta |
| **Media** | Impacto acotado, no afecta clientes | Caída de un sistema interno, endpoint infectado aislado |
| **Baja** | Sin impacto operativo relevante | Phishing reportado sin víctimas, falso positivo |

### 4. Equipo de respuesta (roles)
| **Rol** | **Titular sugerido** | **Función en el incidente** |
|---|---|---|
| **Coordinador RSI** | RSI (Riesgos No Financieros) | Conduce la respuesta, decide severidad, comunica |
| **Técnico TI** | División TI (Producción/Sistemas) | Contención, erradicación y recuperación técnica |
| **Legal** | División Servicios Jurídicos Notariales | Asesoría, obligaciones legales, confidencialidad |
| **Comunicaciones** | [COMPLETAR: área de comunicación institucional] | Comunicados internos/externos (RC-03) |
| **DPD** | Delegado de Protección de Datos | Evalúa vulneración de datos y activa RS-02 |
| **Capital Humano** | División Capital Humano | Investigaciones internas, medidas disciplinarias |
| **Oficial de Cumplimiento** | Oficial de Cumplimiento | Eventos de fraude/PLAFT, reportes al BCU |

### 5. Flujo del proceso
7. **Detección y reporte:** el funcionario o el SIEM reporta al RSI. Todo reporte se registra con fecha y hora.
8. **Triage (clasificación):** el RSI determina severidad y prioridad en máximo [COMPLETAR: 30 minutos] y convoca al equipo.
9. **Contención:** el técnico aísla el sistema afectado (desconexión de red, bloqueo de credenciales) para frenar el daño.
10. **Erradicación:** se elimina la causa (malware, cuenta comprometida, backdoor) con evidencia preservada por RS-03.
11. **Recuperación:** se restaura el servicio desde respaldos confiables y se refuerzan controles.
12. **Cierre y lecciones:** se documenta, se elabora el informe y se alimenta RC-04.
### 6. Tiempos de respuesta objetivo
| **Acción** | **Tiempo objetivo** |
|---|---|
| Reporte inicial del incidente | [COMPLETAR: 30 min desde detección] |
| Triage y clasificación | [COMPLETAR: 60 min] |
| Contención (incidente crítico) | [COMPLETAR: 4 h] |
| Inicio de procedimientos de minimización (vulneración) | **24 h** (obligatorio) |
| Notificación a URCDP si corresponde | **72 h** (obligatorio, ver RS-02) |
| Informe preliminar al Comité | [COMPLETAR: 48 h] |

### 7. Cadena de custodia inicial y registro
Todo incidente se registra en el **Registro de Incidentes** (bitácora) con: fecha/hora, descripción, sistemas afectados, severidad, acciones, responsable y estado. Ante incidentes con posible relevancia penal o legal, se aplica la cadena de custodia de RS-03 antes de tocar cualquier evidencia.
### 8. Control de cambios
| **Versión** | **Fecha** | **Cambio** | **Elaboró** | **Aprobó** |
|---|---|---|---|---|
| 0.1 | [COMPLETAR] | Versión inicial (borrador) | RSI | — |
| 1.0 | [COMPLETAR] | Aprobación del Directorio | RSI | Directorio |

## 5. Ejemplo aplicado al Banco (modelo de referencia)
Ejemplo ilustrativo. Adaptá a la operación real del Banco.
**Caso: ransomware en una sucursal (ejemplo):**
- 03:10 — El EDR detecta cifrado masivo en 12 estaciones de la Sucursal Centro y genera alerta crítica (DE-02).
- 03:12 — El analista de monitoreo reporta al RSI (guardia).
- 03:30 — El RSI clasifica como **crítico**, convoca al equipo; el técnico de Producción aísla de red las estaciones afectadas (contención) en 3:50.
- 04:00 — Se identifica el vector de entrada (campaña de phishing) y se bloquea el correo y el dominio; el DPD evalúa que no se afectaron datos personales fuera de esas estaciones.
- 05:30 — Erradicación: se limpian las estaciones; se restaura desde imagen y se cambian credenciales locales.
- 08:30 — Se confirma que el sistema de pagos no fue afectado; el Oficial de Cumplimiento decide que no hay reporte inmediato al BCU, pero se registra el evento operativo.
- 09:00 — Se informa al Comité y al Directorio. Informe preliminar y cierre de la bitácora; posteriormente RC-04 (lecciones aprendidas) actualiza los controles de correo.

**Documentos relacionados:**
- DE-02 (Detección) · RS-02 (Notificación) · RS-03 (Forense)
- RC-01/RC-02 (Continuidad y DRP) · RC-03 (Comunicación de Crisis) · RC-04 (Lecciones)
- BCU-06 (Contingencia) · URCDP-02 (Notificación de Vulneraciones)
