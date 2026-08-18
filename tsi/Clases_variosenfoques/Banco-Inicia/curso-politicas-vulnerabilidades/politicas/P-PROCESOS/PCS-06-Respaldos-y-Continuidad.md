# PCS-06 · Proceso de Respaldos y Continuidad

> **Función del MCU 5.0:** Recuperar (RC.RP — recuperación) · Identificar (ID.BE — continuidad del negocio)
> **ISO/IEC 27001:** A.8.13 (respaldo de la información) · A.5.29-A.5.30 (continuidad de la seguridad de la información)
> **BCU:** EMG — la continuidad de los servicios esenciales se planifica, se prueba y se reporta
> **URCDP:** Ley 18.331 art. 10 — la información debe estar disponible y recuperable de forma segura
> **Nivel del curso:** 🟡 Practicar
> **Ejecuta:** POL-08

---

## 1. Objetivo y alcance
Garantizar que la **información y los sistemas críticos** se respaldan y pueden recuperarse dentro de los objetivos de continuidad (RTO/RPO), y que la continuidad se **prueba** de forma periódica. Aplica a todos los sistemas y datos, incluidos nube e IA.

## 2. Entradas
- Análisis de impacto (BIA) y clasificación de sistemas críticos.
- Objetivos de continuidad (RTO/RPO) por sistema (POL-08).
- Planes de continuidad y de recuperación de desastres.
- Resultados de pruebas anteriores.

## 3. Actividades numeradas

**3.1 — Identificar sistemas y datos críticos.**
- **Responsable:** Jefe de Continuidad con dueños de procesos.
- **Pasos:** (a) revisar el BIA, (b) definir RTO/RPO por sistema, (c) actualizar la clasificación de criticidad.
- **Salida:** Listado de sistemas con RTO/RPO.
- **Plazo:** Anual y ante cambios mayores.

**3.2 — Definir la estrategia de respaldo.**
- **Responsable:** Div. TI.
- **Pasos:** (a) definir alcance (qué se respalda), frecuencia y retención, (b) elegir soportes y ubicaciones (POL-08), (c) aplicar cifrado a los respaldos (POL-14).
- **Salida:** Política operativa de respaldos por sistema.
- **Plazo:** Al diseñar cada sistema y al revisarse anualmente.

**3.3 — Ejecutar respaldos y monitorear.**
- **Responsable:** Div. TI (Operaciones).
- **Pasos:** (a) ejecutar los respaldos según el calendario, (b) verificar la finalización y el log, (c) monitorear fallas y alertar.
- **Salida:** Logs de respaldo verificados.
- **Plazo:** Continuo (según frecuencia de cada sistema).

**3.4 — Probar la restauración.**
- **Responsable:** Div. TI con RSI.
- **Pasos:** (a) restaurar muestras en ambiente de prueba, (b) validar la integridad y el funcionamiento, (c) registrar el resultado.
- **Salida:** Prueba de restauración documentada.
- **Plazo:** Sistemas críticos al menos trimestral; el resto anual.

**3.5 — Probar la continuidad y recuperación.**
- **Responsable:** Jefe de Continuidad + Div. TI.
- **Pasos:** (a) planear el simulacro (alcance, escenario, participantes), (b) ejecutar la recuperación de los sistemas críticos, (c) medir tiempos contra RTO/RPO, (d) documentar lecciones.
- **Salida:** Informe de simulacro con resultados y mejoras.
- **Plazo:** Simulacro integral anual; parciales semestrales.

**3.6 — Mejorar y reportar.**
- **Responsable:** Jefe de Continuidad.
- **Pasos:** (a) elaborar plan de acción de las mejoras, (b) reportar los resultados al Comité.
- **Salida:** Plan de mejora y reporte al Comité.
- **Plazo:** Tras cada simulacro.

## 4. Salidas
- Política operativa de respaldos y calendario.
- Logs y reportes de respaldo.
- Pruebas de restauración y simulacros documentados.
- Reporte de continuidad al Comité.

## 5. Responsables del proceso
| Rol | Función |
|---|---|
| **Jefe de Continuidad** | Coordina BIA, planes y simulacros |
| **Div. TI** | Ejecuta respaldos y restauraciones |
| **RSI** | Valida la seguridad de los respaldos |
| **Dueños de procesos** | Definen criticidad y prioridad de recuperación |
| **Comité de Seguridad / Dirección** | Aprueba planes y evalúa resultados |

## 6. Indicadores (KPIs)
- % de respaldos completados con éxito (meta ≥ 95%).
- Cumplimiento del RPO (pérdida de datos dentro del objetivo).
- Cumplimiento del RTO en simulacros.
- % de simulacros ejecutados según el plan (meta 100%).

## 7. Registros que deja
- Logs de respaldo y pruebas de restauración.
- Informes de simulacro con tiempos.
- Plan de acción de mejoras.

## 8. Referencias
POL-08 · POL-14 · PRO-09 · PCS-03 (recuperación tras incidentes).

## 9. Evidencia en el kit
RC-01…RC-04 (planes y pruebas) · PR-05 (política de respaldos).
