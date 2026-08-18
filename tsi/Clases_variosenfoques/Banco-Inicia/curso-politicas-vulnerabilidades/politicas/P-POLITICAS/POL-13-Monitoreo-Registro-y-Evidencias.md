# POL-13 · Política de Monitoreo, Registro y Evidencias (Logging)

> **Función del MCU 5.0:** Detectar (DE.CM — monitoreo continuo; DE.AE — análisis) · Gobernar (GV)
> **ISO/IEC 27001:** A.8.15-A.8.16 (registro y monitoreo) · A.8.10 (supresión de información) · A.8.1 (gestión de vulnerabilidades de logs)
> **BCU:** EMG / RNRCSF — capacidad de detectar eventos y de demostrar trazabilidad
> **URCDP:** Ley 18.331 art. 10 y Decreto 64/020 — los registros permiten detectar e investigar vulneraciones
> **Nivel del curso:** 🔴 Dominar

---

### ENCABEZADO
| **Campo** | **Valor** |
|---|---|
| **Código** | POL-13 |
| **Título** | Monitoreo, Registro y Evidencias |
| **Versión** | 1.0 |
| **Estado** | [Borrador / En revisión / Aprobado] |
| **Fecha de aprobación** | [COMPLETAR] |
| **Elaborado por** | RSI + Operaciones de Seguridad |
| **Revisado por** | Comité de Seguridad · DPD |
| **Aprobado por** | Comité de Seguridad de la Información |
| **Clasificación** | Confidencial |
| **Próxima revisión** | [Fecha, máx. 1 año] |

### 1. Objetivo
Definir **qué se registra, cómo se protege y durante cuánto tiempo** se conservan los registros (logs), y cómo se monitorean para detectar y responder a eventos de seguridad, cumpliendo las normas de protección de datos.

### 2. Alcance
Aplica a sistemas, aplicaciones, equipos de red, bases de datos, seguridad (firewall, WAF, DLP, antivirus, SIEM), accesos y a las herramientas de IA (POL-17).

### 3. Qué se registra
| Fuente | Registro mínimo |
|---|---|
| Accesos y autenticación | Usuario, éxito/fallo, origen, hora |
| Sistemas y servidores | Eventos del SO, servicios, procesos |
| Red y seguridad | Conexiones, reglas disparadas, bloqueos |
| Aplicaciones | Operaciones relevantes, errores |
| Bases de datos | Accesos, cambios, exportaciones |
| Herramientas de IA | Usuario, fecha, herramienta (metadatos) |
| Trabajo remoto / VPN | Conexiones y sesiones |

### 4. Reglas obligatorias
- Los **logs no se pueden borrar ni modificar** sin autorización (protección de integridad; se centralizan en SIEM).
- La **hora se sincroniza** (NTP) para correlacionar eventos.
- **Retención**: [COMPLETAR: mínimo 6 meses; 1 año para eventos de seguridad] según normativa y evidencia de auditoría.
- **Privacidad de logs**: los logs que contienen datos personales se tratan conforme a la POL-20; el contenido sensible se minimiza y su acceso se restringe (POL-04).
- **Monitoreo continuo**: los eventos se correlacionan y analizan (SIEM/Wazuh) y las alertas se gestionan (PCS-09).
- Los **accesos administrativos** se registran de forma reforzada.
- El monitoreo se **comunica al personal** (POL-02) y se ejecuta dentro del marco legal.

### 5. Responsabilidades
- **Operaciones de Seguridad**: gestiona el SIEM y las alertas.
- **Div. TI**: garantiza la generación y retención de logs.
- **RSI**: define la política de retención y accesos a los registros.
- **DPD**: evalúa el tratamiento de datos personales en los logs.

### 6. Cumplimiento y revisión
La ausencia de logs ante un incidente se trata como hallazgo mayor. Revisión anual de la política y de la retención.

### Evidencia del kit
| Evidencia | Documento canónico |
|---|---|
| Configuración del SIEM | DE-01, Actividad 31 |
| Registro de retención | DE-01 |
| Análisis de logs | DE-02, Actividad 33 |
| Política de accesos a logs | POL-04 |
| Reportes de monitoreo | PCS-09 |
