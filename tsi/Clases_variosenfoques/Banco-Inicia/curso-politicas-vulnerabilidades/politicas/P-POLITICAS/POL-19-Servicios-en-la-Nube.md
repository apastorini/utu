# POL-19 · Política de Servicios en la Nube

> **Función del MCU 5.0:** Gobernar (GV.SC — proveedores) · Proteger (PR.DS — datos; PR.AC — acceso)
> **ISO/IEC 27001:** A.5.30 (continuidad en nube) · A.8.2-A.8.3 (dispositivos) · A.5.19-A.5.22 (proveedores) · A.5.34 (datos personales)
> **BCU:** EMG / RNRCSF — la nube se gestiona como servicio de terceros con control del banco
> **URCDP:** Ley 18.331 art. 18 y Decreto 64/020 — transferencias internacionales y garantías de los encargados de tratamiento en la nube
> **Nivel del curso:** 🔴 Dominar

---

### ENCABEZADO
| **Campo** | **Valor** |
|---|---|
| **Código** | POL-19 |
| **Título** | Servicios en la Nube |
| **Versión** | 1.0 |
| **Estado** | [Borrador / En revisión / Aprobado] |
| **Fecha de aprobación** | [COMPLETAR] |
| **Elaborado por** | Div. TI + RSI + DPD |
| **Revisado por** | Comité de Seguridad · Legales |
| **Aprobado por** | Comité de Seguridad de la Información |
| **Clasificación** | Confidencial |
| **Próxima revisión** | [Fecha, máx. 1 año] |

### 1. Objetivo
Regular la **adopción y uso de servicios en la nube** (SaaS, IaaS, PaaS), garantizando que la información del Banco se aloja con proveedores autorizados, con contratos y controles adecuados.

### 2. Alcance
Aplica a todo servicio en la nube que procese, almacene o transmita información del Banco, contratado por cualquier área (incluye shadow IT: servicios no autorizados).

### 3. Reglas obligatorias
- **Autorización previa**: ningún servicio en la nube se usa sin aprobación (POL-11, PRO-13); los servicios no autorizados se detectan y gestionan (POL-02).
- **Evaluación**: se evalúan seguridad, residencia de datos, cumplimiento (URCDP/BCU), disponibilidad y modelo de soporte antes de contratar.
- **Contratos**: cláusulas de seguridad, tratamiento de datos personales (encargado), notificación de incidentes, auditoría, subcontratación y portabilidad (POL-11).
- **Datos personales**: se verifica la base legal de la transferencia (Ley 18.331, Decreto 414/009) y se registra en el inventario del DPD (POL-20).
- **Acceso y credenciales**: identidades corporativas (SSO/MFA), menor privilegio y revisión periódica (POL-04).
- **Cifrado**: datos en reposo y en tránsito cifrados (POL-14); claves gestionadas por el Banco cuando corresponda.
- **Configuración segura**: se siguen las buenas prácticas del proveedor y la política de hardening (POL-15); se audita la configuración.
- **Respaldos**: cobertura conforme a POL-08.
- **Salida**: plan de migración y retiro de datos al finalizar el contrato.

### 4. Responsabilidades
- **Div. TI**: arquitectura, configuración y operación de la nube.
- **RSI**: evaluación de seguridad y seguimiento.
- **DPD**: evaluación de datos personales y EIPD.
- **Compras/Legales**: contratos.

### 5. Cumplimiento y revisión
El uso no autorizado de nube (shadow IT) se gestiona como hallazgo (POL-02). Revisión anual de la política y del inventario de servicios.

### Evidencia del kit
| Evidencia | Documento canónico |
|---|---|
| Inventario de servicios en la nube | GV-04 |
| Contratos y anexos de seguridad | GV-05 |
| EIPD y registros de transferencia | POL-20 |
| Configuración y auditoría de nube | PR-08 |
| Plan de salida | GV-05 |
