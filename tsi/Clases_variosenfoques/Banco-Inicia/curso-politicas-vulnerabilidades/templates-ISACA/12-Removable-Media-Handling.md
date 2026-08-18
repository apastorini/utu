# VPOL-17 · Removable Media Handling Policy

> **Función del MCU 5.0:** Proteger (PR.DS — medios; PR.PS) · Recuperar (control de datos)
> **ISO/IEC 27001:** A.8.3 (medios de almacenamiento) · A.8.12 (prevención de fuga) · A.8.10 (eliminación)
> **BCU:** EMG — protección de la información y control de los soportes
> **URCDP:** Ley 18.331 — el extravío de un medio con datos personales es una vulneración notificable
> **Nivel del curso:** 🟢 Descubrir

---

### ENCABEZADO
| **Campo** | **Valor** |
|---|---|
| **Código** | VPOL-17 |
| **Título** | Removable Media Handling |
| **Versión** | 1.0 |
| **Estado** | [Borrador / En revisión / Aprobado] |
| **Fecha de aprobación** | [COMPLETAR] |
| **Elaborado por** | RSI + Div. TI |
| **Revisado por** | Seguridad Física · DPD |
| **Aprobado por** | Comité de Seguridad de la Información |
| **Clasificación** | Uso interno |
| **Próxima revisión** | [Fecha, máx. 1 año] |

### 1. Objetivo
Controlar el **uso, almacenamiento, transporte y destrucción** de los medios extraíbles (pendrives, discos externos, tarjetas SD, cintas, CDs/DVDs) para evitar la fuga de información y el ingreso de malware.

### 2. Alcance
Aplica a todo el personal y a los proveedores, y a todos los medios extraíbles que se conecten a equipos del Banco o transporten información del Banco.

### 3. Reglas de uso
- **Solo medios autorizados** por la Div. TI; los medios personales están **prohibidos** en equipos con información confidencial salvo excepción autorizada.
- **Cifrado obligatorio** para datos confidenciales (nivel 3 y 4 — VPOL-12) en medios extraíbles: [COMPARTIR/COMPLETAR: herramienta de cifrado].
- **Escaneo antivirus** del medio al conectarse (protección Endpoint de la estación).
- **Prohibido:** usar medios extraíbles como almacenamiento principal de información, o dejar datos en pendrives de forma permanente.
- **Prohibido** copiar bases de datos de clientes a medios sin autorización del propietario del activo y del DPD.

### 4. Transporte
- Los medios con datos confidenciales se transportan **cifrados, en contenedor cerrado** y con responsable identificado.
- La **entrega a terceros** se registra (qué, a quién, cuándo) y se rige por VPOL-18.
- Prohibido el transporte por medios de mensajería no autorizados.

### 5. Almacenamiento y destrucción
- Los medios se guardan en **armarios con llave** o caja de seguridad cuando contienen datos sensibles.
- **Destrucción segura:** al final de su vida útil, los medios con datos se **destruyen físicamente** o se borran con método certificado (borrado criptográfico/cifrado + formateo), y se **documenta** la destrucción (acta con testigos).
- Los medios fuera de uso con datos personales se eliminan conforme a la tabla de retención (URCDP-01).

### 6. Pérdida o robo
La pérdida o robo de un medio con **datos personales o confidenciales** se reporta de inmediato como **incidente** (RS-01) y se evalúa la **notificación a la URCDP** (art. 27-bis).

### 7. Responsabilidades y cumplimiento
- **Cada usuario:** responsable del medio que le fue asignado.
- **Div. TI:** administra el inventario de medios, el cifrado y la destrucción.
- **DPD:** evalúa las notificaciones por pérdida de datos personales.
- Incumplimiento: medidas disciplinarias; incidentes de fuga con evaluación de denuncia.

### Evidencia del kit
| Evidencia | Documento canónico |
|---|---|
| Inventario de medios | ID-01 |
| Registro de destrucción | PR-03 / PR-04 |
| Procedimiento de cifrado de medios | PR-03 |
| Notificación de vulneraciones | URCDP-02 |
