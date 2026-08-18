# PCS-03 · Proceso de Gestión de Incidentes

> **Función del MCU 5.0:** Detectar (DE.AE) · Responder (RS.RP, RS.CO) · Recuperar (RC.RP)
> **ISO/IEC 27001:** A.5.24-A.5.28 (planificación y gestión de incidentes) · A.5.25 (evaluación)
> **BCU:** EMG / RNRCSF — gestión y notificación de incidentes cibernéticos al supervisor
> **URCDP:** Decreto 64/020 — notificación de vulneraciones de datos personales en 72 h
> **Nivel del curso:** 🔴 Dominar
> **Ejecuta:** POL-07 (y PRO-04 / PRO-05 como apoyo)

---

## 1. Objetivo y alcance
Detectar, clasificar, contener, erradicar y recuperar los **incidentes de seguridad** con trazabilidad, minimizando el impacto y cumpliendo las obligaciones de notificación. Aplica a todos los sistemas, datos e instalaciones, incluido el entorno de IA.

## 2. Entradas
- Alertas de monitoreo y SIEM (POL-13, PCS-09).
- Reportes del personal, proveedores y terceros.
- Avisos externos (CERT-UY, BCU, ISACs).
- Registro de incidentes previos y lecciones aprendidas.

## 3. Actividades numeradas

**3.1 — Registrar y clasificar.**
- **Responsable:** Mesa de Ayuda / RSI.
- **Pasos:** (a) recibir el reporte con datos mínimos (qué, cuándo, dónde, evidencia), (b) registrar en el registro de incidentes, (c) clasificar por nivel (leve/moderado/grave/crítico) y tipo (malware, phishing, acceso no autorizado, fuga, DDoS).
- **Salida:** Ticket de incidente con nivel asignado.
- **Plazo:** Inmediato; primera evaluación en 30 min.

**3.2 — Contener.**
- **Responsable:** RSI (CERT interno) con Div. TI.
- **Pasos:** (a) aislar lo afectado (red, cuentas, servicios), (b) preservar evidencia (logs, imágenes, muestras), (c) evitar la propagación.
- **Salida:** Incidente contenido; evidencia preservada.
- **Plazo:** Según nivel (crítico: inmediato).

**3.3 — Investigar (causa raíz y alcance).**
- **Responsable:** RSI con apoyo forense si aplica.
- **Pasos:** (a) analizar logs, correos y artefactos, (b) determinar causa raíz y alcance (datos, sistemas, usuarios afectados), (c) documentar la línea de tiempo.
- **Salida:** Análisis de causa raíz y alcance.
- **Plazo:** Moderados: 48 h · graves/críticos: en curso continuo.

**3.4 — Evaluar obligaciones de notificación.**
- **Responsable:** DPD (datos personales) y RSI (BCU).
- **Pasos:** (a) determinar si hay datos personales comprometidos y riesgo para titulares, (b) notificar a la URCDP en 72 h si aplica (PRO-05), (c) reportar al BCU los incidentes cibernéticos relevantes.
- **Salida:** Notificaciones emitidas y registradas.
- **Plazo:** 72 h (URCDP) · según normativa BCU.

**3.5 — Erradicar y recuperar.**
- **Responsable:** Div. TI con RSI.
- **Pasos:** (a) eliminar la causa (malware, acceso, configuración), (b) restaurar desde respaldos limpios (PCS-06), (c) validar el funcionamiento y vigilar recaídas.
- **Salida:** Servicio restaurado y verificado.
- **Plazo:** Según el plan de recuperación del incidente.

**3.6 — Cerrar y aprender.**
- **Responsable:** RSI.
- **Pasos:** (a) documentar el informe final (línea de tiempo, causa raíz, impacto, acciones), (b) definir plan de acción de mejoras, (c) comunicar lecciones al personal (PRO-12).
- **Salida:** Informe de incidente y plan de mejora.
- **Plazo:** 10 días hábiles tras la recuperación.

## 4. Salidas
- Registro de incidentes completo (RS-01).
- Informes de incidente y análisis de causa raíz.
- Notificaciones a URCDP/BCU.
- Plan de acción de mejoras.

## 5. Responsables del proceso
| Rol | Función |
|---|---|
| **Mesa de Ayuda** | Primer registro y contacto |
| **RSI (CERT interno)** | Investigación, contención y cierre |
| **Div. TI** | Aislamiento, erradicación y recuperación |
| **DPD** | Notificación a la URCDP |
| **Comité de Incidentes / Dirección** | Decisiones críticas y comunicación |
| **Comunicación** | Comunicación externa si aplica |

## 6. Indicadores (KPIs)
- Tiempo medio de detección (MTTD) y de respuesta (MTTR).
- % de incidentes con análisis de causa raíz (meta ≥ 80% de graves).
- % de notificaciones a URCDP dentro de 72 h (meta 100%).
- % de incidentes recurrentes (meta: decreciente).

## 7. Registros que deja
- Tickets e informe de incidentes.
- Registro de notificaciones.
- Lecciones aprendidas y plan de acción.

## 8. Referencias
POL-07 · POL-13 · PRO-04 · PRO-05 · PCS-06 · PCS-09.

## 9. Evidencia en el kit
RS-01 (registro de incidentes) · DE-01/DE-02 (detección) · URCDP-03 (notificaciones) · BCU (reportes).
