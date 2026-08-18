# PCS-02 · Proceso de Gestión de Vulnerabilidades

> **Función del MCU 5.0:** Identificar (ID.RA — vulnerabilidades) · Proteger (PR.IP — remediación) · Detectar (DE.CM)
> **ISO/IEC 27001:** A.8.8 (gestión de vulnerabilidades técnicas) · A.5.15 (controles de acceso) · A.8.9 (configuración)
> **BCU:** EMG — la gestión continua de vulnerabilidades es un control esencial del riesgo de TIC
> **URCDP:** Ley 18.331 art. 10 — las vulnerabilidades técnicas se remedian para proteger datos personales
> **Nivel del curso:** 🟡 Practicar → 🔴 Dominar
> **Ejecuta:** POL-05 (y PRO-06 / PRO-03 como apoyo)

---

## 1. Objetivo y alcance
Detectar, priorizar, remediar y verificar las **vulnerabilidades técnicas** de los activos del Banco de forma continua, con plazos según el riesgo. Aplica a servidores, estaciones, red, aplicaciones, bases de datos, nube y entorno de IA.

## 2. Entradas
- Inventario de activos y software (ID-01, POL-03).
- Resultados de escaneos (OpenVAS/Trivy u otras herramientas) y verificaciones de configuración (PRO-03).
- Avisos de seguridad (CERT-UY, CISA KEV, proveedores).
- Reportes de aplicación (SAST/DAST/SCA — PRO-10).

## 3. Actividades numeradas

**3.1 — Mantener el inventario actualizado.**
- **Responsable:** Div. TI con apoyo del RSI.
- **Pasos:** (a) registrar todo activo, software y versión, (b) revisar inventario al menos trimestral.
- **Salida:** Inventario vigente.
- **Plazo:** Continuo.

**3.2 — Escanear según criticidad.**
- **Responsable:** RSI / Operaciones de Seguridad.
- **Pasos:** (a) ejecutar escaneo de vulnerabilidades con la frecuencia del activo (críticos mensual, internos trimestral, otros semestral), (b) verificar desvíos de configuración, (c) registrar hallazgos.
- **Salida:** Reporte de hallazgos por activo.
- **Plazo:** Según calendario definido en PRO-06.

**3.3 — Priorizar cada vulnerabilidad.**
- **Responsable:** RSI.
- **Pasos:** (a) puntuar con CVSS, (b) ajustar por contexto: exposición, datos que procesa, explotación activa (KEV), (c) asignar severidad final y plazo.
- **Salida:** Lista priorizada de vulnerabilidades.
- **Plazo:** Dentro de las 48 h del hallazgo.

**3.4 — Definir el tratamiento.**
- **Responsable:** RSI con dueños de sistemas.
- **Pasos:** (a) elegir: parchear / mitigación compensatoria / excepción temporal justificada, (b) registrar la decisión y el plazo.
- **Salida:** Plan de remediación.
- **Plazo:** Al priorizar.

**3.5 — Remediar.**
- **Responsable:** Div. TI (Administradores de sistemas, DevOps).
- **Pasos:** (a) aplicar parche en la ventana definida con el proceso de cambios (PCS-05), (b) o implementar la mitigación compensatoria, (c) registrar en el ticket.
- **Salida:** Ticket de remediación.
- **Plazo:** Crítica 72 h · Alta 15 días · Media 30-90 días (referencia, según PRO-06).

**3.6 — Verificar y cerrar.**
- **Responsable:** RSI.
- **Pasos:** (a) re-escanear el activo, (b) confirmar que la vulnerabilidad desapareció, (c) cerrar el hallazgo.
- **Salida:** Hallazgo cerrado con evidencia.
- **Plazo:** 5 días hábiles tras la remediación.

**3.7 — Reportar y medir.**
- **Responsable:** RSI al Comité.
- **Pasos:** (a) calcular métricas (vulnerabilidades abiertas, vencidas, tiempos de remediación), (b) reportar.
- **Salida:** Reporte mensual de gestión de vulnerabilidades.
- **Plazo:** Mensual.

## 4. Salidas
- Reportes de escaneo y verificación.
- Lista priorizada y plan de remediación.
- Registro de excepciones/compensaciones.
- Métricas al Comité.

## 5. Responsables del proceso
| Rol | Función |
|---|---|
| **RSI** | Coordina, prioriza, verifica y reporta |
| **Div. TI** | Escanea, remedia y mantiene el inventario |
| **Dueños de sistemas** | Aprueban ventanas y tratamientos |
| **Comité de Seguridad** | Revisa métricas y excepciones significativas |

## 6. Indicadores (KPIs)
- % de vulnerabilidades críticas remediadas en 72 h (meta ≥ 90%).
- % de vulnerabilidades vencidas (meta ≤ 5%).
- Cobertura de escaneo del inventario (meta 100%).
- Tiempo medio de remediación por severidad.

## 7. Registros que deja
- Reportes de escaneo y tickets.
- Registro de excepciones.
- Reporte mensual de métricas.

## 8. Referencias
POL-05 · PRO-03 · PRO-06 · PRO-10 · PCS-01 · PCS-05.

## 9. Evidencia en el kit
PR-06 (política de vulnerabilidades) · DE-01 (detección) · ID-02 (matriz de riesgos) · reportes de escaneo.
