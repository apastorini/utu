# PRO-13 · Procedimiento: Evaluación de Seguridad de Terceros y Proveedores

> **Función del MCU 5.0:** Gobernar (GV.SC — gestión de la cadena de suministro)
> **ISO/IEC 27001:** A.5.19-A.5.22 (relaciones con proveedores, en nube e ITSM) · A.5.19 (acuerdos)
> **BCU:** EMG / RNRCSF — los servicios de terceros deben mantener el nivel de control exigido al Banco
> **URCDP:** Ley 18.331 art. 18 — los encargados de tratamiento deben dar las mismas garantías
> **Nivel del curso:** 🟡 Practicar

---

## 1. Objetivo y alcance
Asegurar que los **terceros y proveedores** que acceden a sistemas, datos o instalaciones del Banco cumplan un nivel de seguridad equivalente, antes y durante la relación. Aplica a proveedores de TI, nube, mantenimiento, limpieza, seguridad y otros con acceso a información o instalaciones.

## 2. Responsables
- **Compras / Área contratante**: gestiona la relación comercial.
- **RSI**: define y ejecuta la evaluación de seguridad.
- **Legales**: incorpora las cláusulas al contrato.
- **DPD**: revisa los acuerdos de tratamiento de datos personales.

## 3. Desarrollo paso a paso

### 3.1 Antes de contratar
1. El **área contratante** informa a **RSI** del nuevo proveedor y del acceso/información que tendrá.
2. **RSI clasifica el riesgo** según: acceso a información (¿datos personales? ¿críticos?), acceso a sistemas, presencia en sitio, tipo de servicio.
3. **RSI evalúa** al proveedor según el riesgo:
   - **Cuestionario de seguridad** (madurez, certificaciones — ISO 27001, SOC 2, PCI —, incidentes).
   - Proveedores de alto riesgo: **revisión documental o evaluación en sitio** si corresponde.
   - **Nube**: se aplica además la POL-19 y la evaluación del proveedor de nube.
4. Se definen los **requisitos contractuales**: cláusulas de seguridad, notificación de incidentes, tratamiento de datos personales, auditoría, subcontratación, destrucción/retorno de datos, cláusula de salida.
5. **Legales** incorpora las cláusulas; el contrato se aprueba antes del acceso.

### 3.2 Durante la relación
6. Los accesos del proveedor se gestionan como cualquier usuario: **mínimo privilegio, plazo definido, MFA** (PRO-01, PRO-08).
7. Se supervisan los **informes del proveedor** (informe de incidentes, SOC/auditoría) según la periodicidad pactada.
8. Los **incidentes del proveedor** que afecten al Banco se gestionan con PRO-04.
9. Se revisan los **niveles de servicio** y el cumplimiento contractual de seguridad.

### 3.3 Fin de la relación
10. Se ejecuta el **retiro de accesos** del proveedor.
11. El proveedor **devuelve o destruye** la información del Banco y lo acredita (PRO-09).
12. Se verifica la eliminación en la nube (POL-19).

## 4. Clasificación del riesgo del proveedor (referencia)
| Riesgo | Criterio | Evaluación |
|---|---|---|
| **Alto** | Datos personales masivos, sistemas críticos, nube de información | Cuestionario + revisión documental + cláusulas reforzadas |
| **Medio** | Acceso a información confidencial o a sistemas no críticos | Cuestionario + cláusulas |
| **Bajo** | Sin acceso a información sensible | Cuestionario mínimo |

## 5. Salidas y registros
- Registro de proveedores evaluados con su riesgo (GV-03).
- Cuestionarios y evaluaciones.
- Contratos con cláusulas de seguridad (GV-05).
- Acuerdos de encargado de tratamiento.

## 6. Errores comunes
- Contratar sin evaluación "por urgencia".
- No supervisar al proveedor después de contratarlo.
- Cláusulas genéricas sin notificación de incidentes.
- Proveedores con accesos que nunca se revocan.

## 7. Referencias y evidencia
POL-11 · POL-19 · PRO-08 · PRO-09. Alimenta: GV-03, GV-05, URCDP-05.
