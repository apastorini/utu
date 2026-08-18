# PCS-05 · Proceso de Gestión de Cambios

> **Función del MCU 5.0:** Gobernar (GV.OR — gestión del cambio) · Proteger (PR.IP — cambios controlados)
> **ISO/IEC 27001:** A.8.31-A.8.32 (gestión del cambio y de TI) · A.8.9 (configuración)
> **BCU:** EMG — todo cambio en sistemas se gestiona con aprobación, prueba y trazabilidad
> **URCDP:** Ley 18.331 art. 10 — los cambios no pueden debilitar la protección de datos
> **Nivel del curso:** 🟡 Practicar
> **Ejecuta:** POL-06 (y PRO-11 como apoyo)

---

## 1. Objetivo y alcance
Planificar, aprobar, implementar y registrar **todo cambio** sobre sistemas, aplicaciones, red, configuración, nube y entorno de IA, reduciendo fallas e impactos no previstos. Aplica a producción y a entornos relevantes.

## 2. Entradas
- Solicitud de cambio (RFC) con justificación e impacto esperado.
- Resultados de pruebas y plan de retorno.
- Ventanas de cambio aprobadas.
- Clasificación del cambio (rutinario / normal / emergencia).

## 3. Actividades numeradas

**3.1 — Solicitar el cambio.**
- **Responsable:** Solicitante (área o Div. TI).
- **Pasos:** (a) documentar descripción, motivo, activos afectados, impacto en negocio y riesgo, (b) definir el plan de retorno (rollback), (c) enviar la RFC.
- **Salida:** RFC registrada.
- **Plazo:** Con la anticipación que exija su categoría.

**3.2 — Evaluar el impacto y el riesgo.**
- **Responsable:** Dueño del sistema + RSI.
- **Pasos:** (a) evaluar impacto funcional y técnico, (b) evaluar el riesgo de seguridad (¿expone datos?, ¿abre puertos?, ¿cambia accesos?), (c) definir la categoría final del cambio.
- **Salida:** RFC evaluada con riesgo y categoría.
- **Plazo:** 2-5 días hábiles según categoría.

**3.3 — Probar.**
- **Responsable:** Div. TI / Desarrollo con QA.
- **Pasos:** (a) probar en ambiente controlado, (b) validar que los controles de seguridad se mantienen (PRO-10, PRO-03), (c) registrar los resultados.
- **Salida:** Evidencia de pruebas.
- **Plazo:** Antes de la aprobación.

**3.4 — Aprobar.**
- **Responsable:** CAB para cambios normales; RSI para cambios de seguridad; doble aprobación para emergencias.
- **Pasos:** (a) revisar RFC, riesgo y pruebas, (b) decidir aprobar / rechazar / diferir, (c) registrar la decisión.
- **Salida:** RFC aprobada con firmas.
- **Plazo:** Según el calendario del CAB (reunión periódica).

**3.5 — Implementar en la ventana.**
- **Responsable:** Div. TI / DevOps.
- **Pasos:** (a) ejecutar el cambio en la ventana definida, (b) supervisar la implementación, (c) en caso de falla, ejecutar el plan de retorno.
- **Salida:** Cambio implementado (o revertido).
- **Plazo:** En la ventana aprobada.

**3.6 — Verificar y cerrar.**
- **Responsable:** Dueño del sistema + RSI.
- **Pasos:** (a) verificar el funcionamiento en producción, (b) confirmar que la seguridad no se degradó, (c) cerrar la RFC con el resultado.
- **Salida:** RFC cerrada con resultado.
- **Plazo:** 5 días hábiles tras la implementación.

## 4. Salidas
- RFC con historial completo (solicitud, evaluación, pruebas, aprobación, implementación, cierre).
- Registro de cambios de emergencia.
- Ventanas de cambio y calendario del CAB.

## 5. Responsables del proceso
| Rol | Función |
|---|---|
| **Solicitante** | Describe y justifica el cambio |
| **Dueño del sistema** | Evalúa impacto y aprueba el negocio |
| **CAB (Comité de Cambios)** | Aprueba los cambios normales |
| **RSI** | Evalúa y aprueba el riesgo de seguridad |
| **Div. TI / DevOps** | Prueba e implementa |

## 6. Indicadores (KPIs)
- % de cambios aprobados que fallan en producción (meta < 5%).
- % de cambios con RFC documentada (meta 100%).
- Tiempo medio de implementación de emergencias.
- % de cambios revertidos con éxito.

## 7. Registros que deja
- RFC y actas del CAB.
- Evidencias de pruebas.
- Registro de implementaciones y retornos.

## 8. Referencias
POL-06 · PRO-10 · PRO-11 · PCS-02 (parches) · PCS-07 (proveedores).

## 9. Evidencia en el kit
PR-07 (registro de cambios) · BCU-04 · auditorías de cambios.
