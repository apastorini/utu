# VPOL-18 · Third-Party Management Policy

> **Función del MCU 5.0:** Gobernar (GV.RM — riesgos de terceros) · Proteger (PR.AC/PR.DS — límites y datos)
> **ISO/IEC 27001:** A.5.19 (seguridad en las relaciones con proveedores) · A.5.20 (acuerdos) · A.5.21/5.22/5.23 (cadena de suministro TIC)
> **BCU:** EMG y Circular 2280 — control de la tercerización de servicios del sistema de pagos; responsabilidad indelegable
> **URCDP:** Ley 18.331 — el proveedor es "encargado de tratamiento"; el Banco es el responsable
> **Nivel del curso:** 🔴 Dominar

---

### ENCABEZADO
| **Campo** | **Valor** |
|---|---|
| **Código** | VPOL-18 |
| **Título** | Third-Party Management |
| **Versión** | 1.0 |
| **Estado** | [Borrador / En revisión / Aprobado] |
| **Fecha de aprobación** | [COMPLETAR] |
| **Elaborado por** | Compras + RSI + DPD |
| **Revisado por** | Comité de Seguridad · Comité de Riesgos |
| **Aprobado por** | Comité de Seguridad de la Información |
| **Clasificación** | Confidencial |
| **Próxima revisión** | [Fecha, máx. 1 año] |

### 1. Objetivo
Gestionar el **riesgo de los terceros** (proveedores, outsourcing, consultores, servicios en nube, mensajería, mantenimiento) que acceden a información o sistemas del Banco, garantizando que cumplan el mismo nivel de seguridad y que la responsabilidad final siga siendo del Banco.

### 2. Alcance
Aplica a todos los terceros con acceso a información, sistemas, redes o instalaciones del Banco, incluyendo proveedores de TI, proveedores de nube, soporte técnico, desarrolladores externos, servicios de limpieza/seguridad, y sus **subcontratistas**.

### 3. Clasificación de terceros por riesgo
| Nivel | Tipo de tercero | Tratamiento |
|---|---|---|
| **Crítico** | Core, pagos, nube, desarrollo, SOC externo | Due diligence reforzada, auditoría, cláusulas de seguridad y notificación |
| **Medio** | Proveedores con acceso a datos confidenciales | Contrato con cláusulas; revisión anual |
| **Bajo** | Sin acceso significativo | Registro y política de acceso |

### 4. Proceso (resumen)
1. **Debida diligencia** previa: reputación, certificaciones (ISO 27001), incidentes previos, ubicación de datos.
2. **Análisis de riesgo** del servicio tercerizado (GV-03 / GV-05).
3. **Contrato con cláusulas de seguridad** obligatorias:
   - Confidencialidad y protección de datos (como encargado de tratamiento, Ley 18.331).
   - Seguridad de la información y notificación de incidentes en [COMPLETAR: p. ej. 24 h].
   - Derechos de **auditoría** del Banco y de los organismos de control.
   - Cumplimiento de normas del BCU cuando aplique.
   - **Subcontratación** solo con autorización previa.
   - Plan de salida/desvinculación con devolución o destrucción de datos.
4. **Alta de accesos mínimos** para el personal del tercero (VPOL-19/PR-01) con MFA.
5. **Monitoreo y revisión** periódica del cumplimiento del contrato.
6. **Cierre/renovación** con evaluación del desempeño de seguridad.

### 5. Acceso físico y remoto de terceros
- Acompañamiento/registro en instalaciones; acceso remoto solo por canales controlados (VPN con MFA) y con alcance limitado.
- Los técnicos de soporte acceden **solo a lo necesario** y sus acciones se registran (VPOL-14).

### 6. Subcontratistas (cadena de suministro)
- El proveedor debe notificar y obtener aprobación para subcontratar; la responsabilidad por los subcontratistas recae en el proveedor principal.
- Los subcontratistas que accedan a datos personales quedan sujetos a las mismas cláusulas.

### 7. Cumplimiento y revisión
- Si un tercero no cumple las cláusulas de seguridad, se aplican los mecanismos contractuales (plan de acción, sanciones, desvinculación).
- Revisión anual de la lista de terceros y de los contratos vigentes.

### Evidencia del kit
| Evidencia | Documento canónico |
|---|---|
| Registro de terceros | GV-05 |
| Contratos con cláusulas de seguridad | PR-08 |
| Análisis de riesgo del tercero | GV-03, ID-02 |
| Informe de seguimiento de proveedores | GV-05 / BCU-03 |
