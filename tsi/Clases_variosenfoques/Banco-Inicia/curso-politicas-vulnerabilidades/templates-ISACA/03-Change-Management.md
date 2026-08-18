# VPOL-08 · Change Management Policy

> **Función del MCU 5.0:** Proteger (PR.PS — seguridad de plataformas) · Responder/Recuperar (estabilidad y continuidad)
> **ISO/IEC 27001:** A.8.32 (gestión de cambios) · A.8.9 (gestión de configuraciones) · A.12.1 (operaciones)
> **BCU:** EMG — cambios controlados en sistemas de información y pagos; Circular 2280 (sistema de pagos)
> **URCDP:** Ley 18.331 art. 10 — cambios que afecten medidas de seguridad requieren control
> **Nivel del curso:** 🔴 Dominar

---

### ENCABEZADO
| **Campo** | **Valor** |
|---|---|
| **Código** | VPOL-08 |
| **Título** | Change Management |
| **Versión** | 1.0 |
| **Estado** | [Borrador / En revisión / Aprobado] |
| **Fecha de aprobación** | [COMPLETAR] |
| **Elaborado por** | Div. TI (Gobierno de cambios) |
| **Revisado por** | RSI · Jefe de Producción |
| **Aprobado por** | Comité de Seguridad de la Información |
| **Clasificación** | Uso interno |
| **Próxima revisión** | [Fecha, máx. 1 año] |

### 1. Objetivo
Garantizar que **todo cambio** en los sistemas, aplicaciones, redes, configuraciones y controles de seguridad del Banco se **planifique, apruebe, pruebe, documente y revierta** de forma controlada, minimizando el riesgo de interrupción del servicio y de introducción de vulnerabilidades.

### 2. Alcance
Aplica a cambios en: aplicaciones y core bancario, sistema de pagos, base de datos, sistemas operativos, equipos de red y seguridad (firewalls, WAF, SIEM), configuraciones de infraestructura, nube, cambios de parámetros de seguridad y cambios en proveedores de servicios. **No alcanza** a los parches de emergencia de seguridad por vulnerabilidad crítica (se rigen por VPOL-20/PR-06), salvo en lo relativo a ventanas y registro.

### 3. Clasificación de cambios
| Tipo | Características | Ejemplo |
|---|---|---|
| **Estándar** | Pre-aprobado, repetitivo, de bajo riesgo | Alta de usuario con perfil definido |
| **Normal** | Requiere aprobación y ventana | Versión de una aplicación |
| **Emergencia** | Corrección urgente de falla o vulnerabilidad | Parche crítico, rollback por incidente |
| **Mayor** | Alto impacto/riesgo (core, pagos, seguridad) | Migración de core, cambio de firewall |

### 4. Proceso de gestión de cambios (resumen)
1. **Solicitud** de cambio (RFC) con descripción, motivo, riesgo, plan de prueba y de reversión.
2. **Clasificación** del cambio (estándar / normal / emergencia / mayor).
3. **Análisis de riesgo** (incluye impacto en seguridad, continuidad y datos personales).
4. **Aprobación** por el **Comité de Cambios** (y por el RSI cuando afecte controles de seguridad o datos).
5. **Implementación** en la ventana autorizada, siguiendo el plan.
6. **Prueba y verificación** post-cambio (servicio operativo, controles activos).
7. **Registro y cierre** de la RFC con evidencia.

### 5. Reglas de seguridad obligatorias
- Ningún cambio puede **deshabilitar o degradar un control de seguridad** sin aprobación expresa del RSI y plan de compensación.
- Los cambios se prueban primero en **ambiente de homologación**, salvo emergencias justificadas.
- Las configuraciones críticas se versionan y se respalda la configuración previa (para reversión).
- Acceso a producción para implementar cambios: **mínimo privilegio, con registro y auditoría** (VPOL-19 / PR-01).
- Cambios en sistemas que tratan datos personales o de pago requieren verificación de que **no se reduce la protección** (Ley 18.331; BCU pagos).

### 6. Emergencias
- En emergencias, un **grupo reducido autorizado** puede implementar sin esperar el Comité, con **autorización posterior inmediata** y registro completo.
- Toda emergencia se revisa luego para determinar el cambio permanente y las lecciones aprendidas.

### 7. Cumplimiento y excepciones
- El incumplimiento (cambios sin RFC, cambios fuera de ventana sin causa) se trata como **incidente de control interno**.
- Excepciones: solo con aprobación del Comité de Cambios y plazo definido.

### Evidencia del kit
| Evidencia | Documento canónico |
|---|---|
| Procedimiento de cambios y registro de RFC | PR-07 (SDLC) / BCU-04 |
| Bitácora de cambios con aprobaciones | GV-06 (control de cambios) |
| Pruebas en homologación | PR-07 |
