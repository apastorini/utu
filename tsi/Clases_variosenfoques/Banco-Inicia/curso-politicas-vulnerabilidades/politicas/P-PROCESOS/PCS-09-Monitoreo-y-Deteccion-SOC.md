# PCS-09 · Proceso de Monitoreo y Detección (SOC)

> **Función del MCU 5.0:** Detectar (DE.CM — monitoreo continuo) · Identificar (ID.RA)
> **ISO/IEC 27001:** A.8.15-A.8.16 (registro de eventos y monitoreo) · A.8.12 (protección de logs)
> **BCU:** EMG — monitoreo continuo y capacidad de detección de la actividad de TIC
> **URCDP:** Ley 18.331 art. 10 — los accesos a datos personales se registran y monitorean
> **Nivel del curso:** 🟡 Practicar → 🔴 Dominar
> **Ejecuta:** POL-13 (y POL-06 como apoyo)

---

## 1. Objetivo y alcance
Detectar **oportunamente** la actividad maliciosa, anómala o no autorizada en los sistemas y datos del Banco, generando alertas útiles para la respuesta a incidentes (PCS-03). Aplica a los sistemas, red, accesos, aplicaciones y nube.

## 2. Entradas
- Logs de sistemas, aplicaciones, bases de datos, firewall y nube (POL-13).
- Fuentes de inteligencia de amenazas (CERT-UY, CISA, ISACs).
- Inventario de activos y accesos (ID-01, PCS-04).
- Lista de casos de uso de detección definidos.

## 3. Actividades numeradas

**3.1 — Definir fuentes y casos de uso.**
- **Responsable:** RSI / Operaciones de Seguridad.
- **Pasos:** (a) asegurar que los eventos relevantes llegan al SIEM (inicios de sesión, privilegios, cambios, transfers, malware), (b) definir los casos de uso prioritarios (acceso anómalo, movimiento lateral, exfiltración, malware), (c) mantenerlos actualizados.
- **Salida:** Catálogo de fuentes y casos de uso.
- **Plazo:** En el diseño y con cada cambio relevante.

**3.2 — Recopilar y normalizar eventos.**
- **Responsable:** Operaciones de Seguridad / Div. TI.
- **Pasos:** (a) verificar que los agentes/feed llegan y están alineados a hora, (b) normalizar y correlacionar, (c) proteger los logs de alteración (integridad, retención según PRO-09).
- **Salida:** Flujo de eventos confiable.
- **Plazo:** Continuo; verificación de cobertura mensual.

**3.3 — Correlacionar y generar alertas.**
- **Responsable:** SIEM (automático) + Operaciones.
- **Pasos:** (a) aplicar las reglas de correlación, (b) generar la alerta con contexto (activo, usuario, hora), (c) evitar el ruido (ajustar falsos positivos).
- **Salida:** Alertas priorizadas.
- **Plazo:** En tiempo real / casi tiempo real.

**3.4 — Triaje de alertas.**
- **Responsable:** Analistas de SOC.
- **Pasos:** (a) revisar la alerta y determinar si es un evento real o falso positivo, (b) asignar prioridad, (c) escalar a PCS-03 si es incidente.
- **Salida:** Alerta clasificada y escalada (o descartada con justificación).
- **Plazo:** Críticas: 15 min · altas: 1 h · resto: 24 h.

**3.5 — Investigar y documentar.**
- **Responsable:** Analistas de SOC con RSI.
- **Pasos:** (a) profundizar el contexto (logs, cuentas, hosts), (b) documentar el hallazgo, (c) alimentar el registro de incidentes.
- **Salida:** Hallazgo documentado.
- **Plazo:** Según la prioridad.

**3.6 — Reportar y mejorar.**
- **Responsable:** RSI al Comité.
- **Pasos:** (a) elaborar el reporte de monitoreo (alertas, tiempos, eventos relevantes), (b) ajustar reglas y fuentes según los hallazgos.
- **Salida:** Reporte mensual y mejoras de detección.
- **Plazo:** Mensual.

## 4. Salidas
- Alertas priorizadas y clasificadas.
- Tickets de incidentes escalados.
- Reporte mensual de monitoreo.
- Casos de uso actualizados.

## 5. Responsables del proceso
| Rol | Función |
|---|---|
| **Operaciones de Seguridad (SOC)** | Monitorea, hace triaje e investiga |
| **RSI** | Define casos de uso, coordina y reporta |
| **Div. TI** | Asegura el envío de logs y responde a solicitudes |
| **Dueños de sistemas** | Aportan contexto y accesos |

## 6. Indicadores (KPIs)
- Tiempo medio de detección (MTTD) y de triaje.
- Tasa de falsos positivos.
- % de alertas críticas atendidas en el plazo (meta 100%).
- Cobertura de monitoreo del inventario (meta ≥ 90%).

## 7. Registros que deja
- Logs y alertas del SIEM.
- Tickets de triaje e investigación.
- Reportes de monitoreo.

## 8. Referencias
POL-13 · POL-06 · PRO-07 · PCS-03 · PCS-04.

## 9. Evidencia en el kit
DE-01 / DE-02 (detección y análisis) · RS-01 (incidentes) · reportes SIEM (Wazuh).
