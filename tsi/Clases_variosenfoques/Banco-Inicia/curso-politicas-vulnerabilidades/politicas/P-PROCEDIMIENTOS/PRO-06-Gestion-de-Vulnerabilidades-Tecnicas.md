# PRO-06 · Procedimiento: Gestión de Vulnerabilidades Técnicas

> **Función del MCU 5.0:** Proteger (PR.IP — remediación; PR.IP, PR.DS — gestión de vulnerabilidades)
> **ISO/IEC 27001:** A.8.8 (gestión de vulnerabilidades técnicas) · A.8.9 (configuración)
> **BCU:** EMG — gestión continua de vulnerabilidades como control esencial de ciberseguridad
> **URCDP:** Ley 18.331 art. 10 — medidas técnicas (parches) para proteger datos personales
> **Nivel del curso:** 🟡 Practicar → 🔴 Dominar

---

## 1. Objetivo y alcance
Identificar, clasificar, remediar y verificar las **vulnerabilidades técnicas** en los sistemas del Banco, de forma continua y con priorización por riesgo. Aplica a servidores, estaciones, equipos de red, bases de datos, aplicaciones, dispositivos móviles y el entorno de IA (modelos y bibliotecas — curso AISEC-07).

## 2. Responsables
- **Div. TI**: ejecuta escaneos y aplica parches.
- **RSI**: define calendario, prioriza y verifica.
- **Dueños de sistemas**: aprueban la instalación de parches en sistemas críticos.

## 3. Entradas
- Inventario de sistemas y versiones (POL-03, ID-01).
- Líneas base de configuración (PRO-03).
- Avisos de seguridad de fabricantes (CERT-UY, CISA, proveedores).

## 4. Desarrollo paso a paso
1. **Identificar**: se mantiene el inventario actualizado de sistemas, software y versiones.
2. **Escanear**: el RSI coordina escaneos de vulnerabilidades con periodicidad según el riesgo del sistema:
   - Críticos (frontales a Internet, core bancario): **mensual**.
   - Internos importantes: **trimestral**.
   - Otros: **semestral** o ante cambios.
3. **Clasificar**: cada vulnerabilidad se puntúa con **CVSS** y se combina con la criticidad del sistema (matriz de riesgo).
4. **Remediar** según el siguiente esquema (referencia):
| Severidad | Tiempo objetivo de parche |
|---|---|
| Crítica (CVSS ≥ 9.0) | 72 horas / [COMPLETAR] |
| Alta (7.0-8.9) | 15 días |
| Media (4.0-6.9) | 30-90 días |
| Baja (< 4.0) | En el ciclo normal |
5. Cuando no se puede parchear (riesgo de disponibilidad, ventana), se aplican **mitigaciones compensatorias** (protección de red, segmentación, monitoreo) y se registra como **excepción temporal** con vencimiento.
6. **Verificar**: tras el parche se re-escanea para confirmar la remoción.
7. **Reportar**: métricas de vulnerabilidades abiertas, vencidas y tiempos de remediación al Comité.

## 5. Casos especiales
- **Vulnerabilidades activamente explotadas** (KEV): se priorizan de inmediato aunque el CVSS sea menor.
- **Aplicaciones propias y código**: el escaneo se integra al ciclo de desarrollo (POL-15, PRO-10) — SAST/DAST y dependencias.
- **Entorno de IA**: se controlan versiones, dependencias y modelos (curso AISEC-13).

## 6. Salidas y registros
- Registro de escaneos y hallazgos.
- Reporte de vulnerabilidades con severidad y estado.
- Registro de excepciones/compensaciones.
- Métricas al Comité.

## 7. Errores comunes
- Escanear solo algunos sistemas.
- No re-escanear tras parchear.
- No priorizar por riesgo real (solo por CVSS).
- Parches sin prueba en sistemas críticos.

## 8. Referencias y evidencia
POL-03 · POL-05 · POL-15 · PRO-03. Alimenta: PR-03, ID-02, hallazgos BCU.
