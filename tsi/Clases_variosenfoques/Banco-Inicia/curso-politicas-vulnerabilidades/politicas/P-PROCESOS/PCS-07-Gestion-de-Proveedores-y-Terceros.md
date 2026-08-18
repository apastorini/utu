# PCS-07 · Proceso de Gestión de Proveedores y Terceros

> **Función del MCU 5.0:** Gobernar (GV.SC — gestión de la cadena de suministro)
> **ISO/IEC 27001:** A.5.19-A.5.22 (relaciones con proveedores, incluida la nube) · A.5.20-A.5.21 (acuerdos y seguimiento)
> **BCU:** EMG / RNRCSF — los terceros que prestan servicios de TIC mantienen el nivel de control del Banco
> **URCDP:** Ley 18.331 art. 18 — garantías de los encargados de tratamiento y transferencias
> **Nivel del curso:** 🟡 Practicar
> **Ejecuta:** POL-11 (y PRO-13 como apoyo)

---

## 1. Objetivo y alcance
Asegurar que los **proveedores y terceros** que acceden a sistemas, información o instalaciones del Banco cumplen un nivel de seguridad equivalente, **antes, durante y al final** de la relación. Aplica a proveedores de TI, nube, mantenimiento, seguridad y otros con acceso.

## 2. Entradas
- Solicitud de contratación con el alcance del acceso/información.
- Cuestionarios de seguridad y certificaciones del proveedor.
- Contratos y anexos de seguridad.
- Reportes de seguimiento e incidentes de proveedores.

## 3. Actividades numeradas

**3.1 — Clasificar el riesgo del proveedor.**
- **Responsable:** RSI con el área contratante.
- **Pasos:** (a) identificar el acceso/información que tendrá, (b) clasificar el riesgo (alto/medio/bajo — PRO-13), (c) registrar el proveedor en el inventario de terceros.
- **Salida:** Proveedor registrado con nivel de riesgo.
- **Plazo:** Antes de la contratación.

**3.2 — Evaluar la seguridad del proveedor.**
- **Responsable:** RSI.
- **Pasos:** (a) aplicar el cuestionario de seguridad según el riesgo, (b) revisar certificaciones (ISO 27001, SOC 2, PCI) y auditorías, (c) para alto riesgo, evaluar in situ o documental profunda, (d) para nube, aplicar la POL-19.
- **Salida:** Evaluación de seguridad con resultado (aprobado / aprobado con condiciones / rechazado).
- **Plazo:** Antes de contratar.

**3.3 — Definir y firmar las cláusulas.**
- **Responsable:** Legales con RSI y DPD.
- **Pasos:** (a) incorporar cláusulas: seguridad, notificación de incidentes, tratamiento de datos personales, subcontratación, auditoría, retorno/destrucción de datos, salida, (b) firmar el contrato y el acuerdo de encargado de tratamiento si aplica.
- **Salida:** Contrato con cláusulas aprobadas (GV-05).
- **Plazo:** Antes del inicio del servicio.

**3.4 — Otorgar el acceso controlado.**
- **Responsable:** Div. TI.
- **Pasos:** (a) crear los accesos con mínimo privilegio y plazo definido, (b) activar MFA, (c) registrar (PRO-01).
- **Salida:** Acceso de proveedor controlado.
- **Plazo:** Con el inicio del contrato.

**3.5 — Supervisar durante la relación.**
- **Responsable:** RSI con el área contratante.
- **Pasos:** (a) recibir y revisar los informes del proveedor (incidentes, SOC, auditoría), (b) verificar el cumplimiento de los SLA y de las cláusulas, (c) gestionar los incidentes del proveedor con PCS-03, (d) revisar los accesos periódicamente (PCS-04).
- **Salida:** Registro de seguimiento del proveedor.
- **Plazo:** Según periodicidad pactada (al menos anual).

**3.6 — Cerrar la relación con salida segura.**
- **Responsable:** RSI + Div. TI + área contratante.
- **Pasos:** (a) revocar todos los accesos, (b) exigir el retorno o destrucción de la información y acreditarlo (PRO-09), (c) verificar la eliminación en la nube (POL-19), (d) registrar el cierre.
- **Salida:** Cierre documentado con acreditación de retorno/destrucción.
- **Plazo:** Al finalizar el contrato.

## 4. Salidas
- Inventario de proveedores con nivel de riesgo (GV-03).
- Evaluaciones y contratos con cláusulas (GV-05).
- Registro de seguimiento y de incidentes de proveedores.
- Acreditación de retorno/destrucción al cierre.

## 5. Responsables del proceso
| Rol | Función |
|---|---|
| **Área contratante / Compras** | Gestiona la relación comercial |
| **RSI** | Evalúa y supervisa la seguridad |
| **Legales** | Redacta y firma las cláusulas |
| **DPD** | Revisa acuerdos de tratamiento de datos |
| **Div. TI** | Gestiona accesos y operación |

## 6. Indicadores (KPIs)
- % de proveedores evaluados antes de contratar (meta 100%).
- % de contratos con cláusulas de seguridad completas (meta 100%).
- % de proveedores con seguimiento vigente (meta 100%).
- Nº de incidentes de proveedores gestionados.

## 7. Registros que deja
- Evaluaciones y contratos.
- Registro de seguimiento.
- Acreditaciones de retorno/destrucción.

## 8. Referencias
POL-11 · POL-19 · PRO-13 · PRO-08 · PRO-09 · PCS-04.

## 9. Evidencia en el kit
GV-05 (contratos y acuerdos) · GV-03 (registro de decisiones) · URCDP-05 (encargados de tratamiento).
