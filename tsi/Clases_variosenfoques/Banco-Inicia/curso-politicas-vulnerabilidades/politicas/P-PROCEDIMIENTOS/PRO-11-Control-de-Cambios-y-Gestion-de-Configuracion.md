# PRO-11 · Procedimiento: Control de Cambios y Gestión de Configuración

> **Función del MCU 5.0:** Gobernar (GV.OR — gestión del cambio) · Proteger (PR.IP — cambios controlados)
> **ISO/IEC 27001:** A.8.31 (gestión de cambios) · A.8.32 (gestión del cambio en TI) · A.8.9 (configuración)
> **BCU:** EMG — el cambio de sistemas se gestiona con aprobación y trazabilidad
> **URCDP:** Ley 18.331 art. 10 — los cambios no pueden debilitar la protección de datos
> **Nivel del curso:** 🟡 Practicar

---

## 1. Objetivo y alcance
Garantizar que **todo cambio** en sistemas, configuración, aplicaciones, red, nube o entorno de IA se **planifique, pruebe, apruebe, implemente y registre**, minimizando fallas y regresiones. Aplica a producción y entornos de prueba relevantes.

## 2. Responsables
- **Solicitante**: describe el cambio y su justificación.
- **Dueño del sistema**: aprueba el cambio de negocio.
- **Div. TI / DevOps**: implementa el cambio.
- **RSI**: evalúa el impacto en seguridad y aprueba los cambios sensibles.
- **Comité de Cambios (CAB)**: aprueba los cambios de mayor riesgo.

## 3. Clasificación de cambios
| Tipo | Ejemplo | Proceso |
|---|---|---|
| **Rutinario** (standard) | Aplicación de parche de seguridad aprobado | Conocido, aprobación previa genérica, se ejecuta y se registra |
| **Normal** | Nueva funcionalidad, actualización de software | Solicitud, prueba, aprobación del CAB |
| **Emergencia** | Corrección de incidente crítico | Aprobación acelerada (2 personas), se documenta después |

## 4. Desarrollo paso a paso
1. **Solicitud**: se describe el cambio, su motivo, impacto esperado, riesgo y plan de retorno (rollback).
2. **Evaluación**: impacto funcional, técnico y de seguridad (¿expone datos?, ¿abre puertos?, ¿cambia accesos?). El RSI evalúa el riesgo.
3. **Pruebas**: el cambio se prueba en ambiente controlado; se validan los controles de seguridad.
4. **Aprobación**: según la clasificación (CAB para los normales; emergencia con doble aprobación).
5. **Programación y ventana**: se define cuándo se implementa (ventana de baja actividad para críticos).
6. **Implementación**: se ejecuta con la participación de quien lo aprueba; se supervisa en producción.
7. **Registro**: fecha, responsable, descripción, pruebas, aprobación, resultado.
8. **Retorno (rollback)**: si falla, se revierte según el plan; se documenta la causa.
9. **Verificación posterior**: el cambio se verifica en un período de observación.

## 5. Relación con la configuración
- La **línea base de configuración** se actualiza con cada cambio aprobado (PRO-03).
- Los cambios a configuraciones de seguridad (firewall, accesos privilegiados, cifrado) requieren **aprobación del RSI**.
- Las configuraciones relevantes se registran en el **control de cambios**.

## 6. Salidas y registros
- Registro de cambios (solicitudes, aprobaciones, implementaciones).
- Planes de retorno y evidencia de pruebas.
- Registro de cambios de emergencia.

## 7. Errores comunes
- Cambios directos en producción sin solicitud.
- No probar el rollback.
- Emergencias sin documentar.
- Cambios de seguridad sin revisión del RSI.

## 8. Referencias y evidencia
POL-15 · PRO-03 · PRO-10. Alimenta: PR-08, auditorías, hallazgos de BCU.
