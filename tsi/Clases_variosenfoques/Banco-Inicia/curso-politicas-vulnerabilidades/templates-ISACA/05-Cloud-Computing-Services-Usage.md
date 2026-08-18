# VPOL-10 · Cloud Computing Services Usage Policy

> **Función del MCU 5.0:** Gobernar (GV.OR — gestión de riesgos del tercero) · Proteger (PR.DS — seguridad de datos en nube)
> **ISO/IEC 27001:** A.5.19/5.20/5.21 (relaciones con proveedores y TIC) · A.8.11/8.12 (ocultamiento y fuga de datos) · A.12.1
> **BCU:** EMG y Circular 2280 — riesgo de tercerización; control del proveedor de nube
> **URCDP:** Ley 18.331 — transferencia de datos personales, incluso a proveedores en el exterior; notificación de vulneraciones
> **Nivel del curso:** 🔴 Dominar

---

### ENCABEZADO
| **Campo** | **Valor** |
|---|---|
| **Código** | VPOL-10 |
| **Título** | Cloud Computing Services Usage |
| **Versión** | 1.0 |
| **Estado** | [Borrador / En revisión / Aprobado] |
| **Fecha de aprobación** | [COMPLETAR] |
| **Elaborado por** | RSI + Div. TI (Arquitectura) |
| **Revisado por** | DPD · Comité de Riesgos |
| **Aprobado por** | Comité de Seguridad de la Información |
| **Clasificación** | Confidencial |
| **Próxima revisión** | [Fecha, máx. 1 año] |

### 1. Objetivo
Regular la **adopción y el uso de servicios de computación en la nube** (IaaS, PaaS, SaaS) para que la información del Banco esté protegida al mismo nivel (o superior) que en las instalaciones propias, cumpliendo los requisitos del BCU y la URCDP.

### 2. Alcance
Aplica a cualquier servicio de nube que procese, almacene o transmita información del Banco: correo en nube, ERP/SaaS, infraestructura IaaS (VM, contenedores), bases de datos como servicio, copias de seguridad en nube y herramientas SaaS (incluidas las de IA — ver VPOL-07). Aplica también al **uso personal no autorizado** de nubes con datos del Banco.

### 3. Requisitos previos a la adopción (Debida diligencia)
1. **Análisis de riesgo** del proveedor (GV-05 / PR-08): reputación, certificaciones, ubicación de los datos.
2. **Evaluación legal y de datos personales** con el DPD: ¿hay transferencia internacional de datos? ¿se necesita habilitación/autorización de la URCDP?
3. **Requisitos de seguridad mínimos**: cifrado en tránsito y en reposo, MFA obligatoria, control de accesos, auditoría/logs, notificación de incidentes en plazos [COMPLETAR: p. ej. 24–72 h].
4. **Acuerdo de nivel de servicio (SLA)** y plan de salida (exportación y eliminación segura de datos).
5. Aprobación del **Comité de Seguridad**.

### 4. Reglas de configuración segura
- **Cifrado:** datos en reposo con claves gestionadas por el Banco cuando sea posible; en tránsito siempre TLS.
- **Accesos:** MFA obligatoria para consolas de administración; **roles con mínimo privilegio**; revisión trimestral de accesos.
- **Cuentas de servicio:** prohibido usar la cuenta raíz; cada integración con su rol y credencial (tokens, sin claves en el código).
- **Visibilidad:** todos los recursos en nube se integran al **monitoreo (SIEM)** y al **inventario de activos** (ID-01).
- **Prevención de fuga (DLP):** reglas que bloqueen datos confidenciales hacia servicios no autorizados.
- **Configuración pública:** revisión periódica de buckets/VMs/repositorios que hayan quedado **públicos por error** (ej. escaneo de credenciales y de permisos).

### 5. Responsabilidades compartidas
| Recurso | Responsable |
|---|---|
| Instalaciones, hardware, red del proveedor | Proveedor de nube |
| Sistema operativo, contenedores, aplicaciones, datos | Banco |
| Configuración de los servicios usados (SaaS) | Banco (parametrización) |
| Cumplimiento de la Ley 18.331 | Banco (es el responsable del tratamiento) |

### 6. Incidentes y notificación
- Todo incidente en la nube (acceso no autorizado, fuga, pérdida) se trata con el **plan de gestión de incidentes** (RS-01) y se **notifica a la URCDP** si afecta datos personales (art. 27-bis).
- El proveedor debe comprometerse a notificar al Banco los incidentes que lo afecten.

### 7. Cumplimiento y excepciones
- El uso de nubes **no autorizadas** con datos del Banco es una **violación grave** (tratamiento como incidente de fuga).
- Excepciones: autorizadas por el Comité de Seguridad con plazo definido y mitigaciones.

### Evidencia del kit
| Evidencia | Documento canónico |
|---|---|
| Análisis de riesgo y contrato del proveedor | GV-05, PR-08 |
| Inventario de servicios en nube | ID-01, GV-04 |
| Configuración de cifrado y MFA | PR-03, PR-01 |
| Alimentación del SIEM | DE-01 |
| Habilitación URCDP (si corresponde) | URCDP-01 |
