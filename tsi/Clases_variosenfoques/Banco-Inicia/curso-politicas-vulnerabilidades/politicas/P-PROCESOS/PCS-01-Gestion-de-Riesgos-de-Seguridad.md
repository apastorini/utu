# PCS-01 · Proceso de Gestión de Riesgos de Seguridad

> **Función del MCU 5.0:** Gobernar (GV.RM — gestión de riesgos) · Identificar (ID.RA — evaluación de riesgos)
> **ISO/IEC 27001:** A.5.5-A.5.7 (política de riesgos, valoración, tratamiento) · A.5.35 (revisión)
> **BCU:** EMG — la gestión de riesgos de TIC se integra al marco de riesgo del Banco
> **URCDP:** Ley 18.331 y Ley 19.670 — evaluación de impacto en la protección de datos (EIPD)
> **Nivel del curso:** 🔴 Dominar
> **Ejecuta:** POL-01

---

## 1. Objetivo y alcance
Identificar, evaluar, tratar y monitorear los **riesgos de seguridad de la información** que afectan a los activos del Banco, priorizando los recursos. Aplica a todos los procesos, sistemas, servicios y proyectos, incluido el uso de IA (POL-17).

## 2. Entradas
- Inventario de activos y su valoración (ID-01, POL-03).
- Contexto del negocio y objetivos estratégicos.
- Amenazas y vulnerabilidades conocidas (PRO-06, CERT-UY, ISACs).
- Requisitos normativos (BCU, URCDP) y del negocio.
- Incidentes y hallazgos previos.

## 3. Actividades numeradas

**3.1 — Definir contexto y apetito de riesgo.**
- **Responsable:** Comité de Seguridad / Dirección.
- **Pasos:** (a) definir criterios de riesgo aceptable, (b) comunicar el apetito de riesgo.
- **Salida:** Declaración de apetito de riesgo aprobada.
- **Plazo:** Anual y ante cambios de estrategia.

**3.2 — Identificar riesgos y vulnerabilidades.**
- **Responsable:** RSI con dueños de activos.
- **Entrada:** inventario de activos, evaluaciones (PRO-06), threat intelligence.
- **Pasos:** (a) identificar amenazas por activo, (b) registrar cada riesgo en la matriz con activo y proceso afectado, (c) incluir los riesgos de IA y terceros (POL-17, POL-11).
- **Salida:** Registro de riesgos actualizado.
- **Plazo:** Continuo; revisión completa semestral.

**3.3 — Evaluar y priorizar el riesgo.**
- **Responsable:** RSI.
- **Pasos:** (a) estimar probabilidad e impacto según los criterios definidos, (b) calcular el nivel de riesgo, (c) priorizar por nivel y cercanía de materialización.
- **Salida:** Matriz de riesgos con niveles (ID-02).
- **Plazo:** Al menos trimestral; ante cambios importantes, inmediato.

**3.4 — Definir el tratamiento.**
- **Responsable:** RSI con dueños de activos; aprobación del Comité para los riesgos altos.
- **Pasos:** (a) elegir tratamiento: mitigar / transferir / aceptar / evitar, (b) definir el plan de tratamiento (controles, responsable, fecha), (c) para datos personales, decidir la necesidad de EIPD (POL-20, URCDP-04).
- **Salida:** Plan de tratamiento de riesgos aprobado.
- **Plazo:** En cada ciclo de evaluación.

**3.5 — Implementar y monitorear.**
- **Responsable:** Dueños de los planes; RSI hace seguimiento.
- **Pasos:** (a) ejecutar los controles del plan, (b) registrar avance, (c) detectar riesgos residuales o nuevos (incidentes, hallazgos, cambios).
- **Salida:** Estado de tratamiento en el registro de riesgos.
- **Plazo:** Según lo planificado; seguimiento mensual por el RSI.

**3.6 — Reportar y revisar.**
- **Responsable:** RSI al Comité de Seguridad.
- **Pasos:** (a) elaborar el reporte de riesgos (nivel general, evolución, principales exposiciones), (b) revisar el apetito de riesgo, (c) actualizar el plan anual.
- **Salida:** Reporte de riesgos al Comité y a Dirección.
- **Plazo:** Trimestral, más reporte anual formal.

## 4. Salidas
- Registro y matriz de riesgos (ID-02, GV-03).
- Plan de tratamiento con responsables y fechas.
- Reportes de riesgos al Comité.
- EIPD cuando aplica (URCDP-04).

## 5. Responsables del proceso
| Rol | Función |
|---|---|
| **Comité de Seguridad** | Aprueba apetito, tratamiento de riesgos altos y reportes |
| **RSI** | Coordina el proceso y da seguimiento |
| **Dueños de activos** | Identifican riesgos y ejecutan tratamientos |
| **Jefe de Riesgos** | Integra el riesgo de TIC al riesgo global del Banco |
| **DPD** | Evalúa riesgos de datos personales y EIPD |

## 6. Indicadores (KPIs)
- % de riesgos con plan de tratamiento vigente (meta ≥ 90%).
- % de riesgos altos/muy altos sin tratamiento en fecha (meta 0%).
- % de planes de tratamiento cerrados a tiempo.
- Nº de riesgos nuevos detectados por período.

## 7. Registros que deja
- Matriz de riesgos con fechas de revisión.
- Actas del Comité de Seguridad.
- Reportes de riesgos.

## 8. Referencias
POL-01 · POL-20 · PRO-06 · PRO-13 · PCS-02 · PCS-10.

## 9. Evidencia en el kit
ID-02 (matriz de riesgos) · GV-03 (registro de decisiones) · URCDP-04 (EIPD) · BCU-01 (reportes).
