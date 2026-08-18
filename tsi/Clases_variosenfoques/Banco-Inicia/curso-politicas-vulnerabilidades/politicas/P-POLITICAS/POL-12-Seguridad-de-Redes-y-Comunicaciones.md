# POL-12 · Política de Seguridad de Redes y Comunicaciones

> **Función del MCU 5.0:** Proteger (PR.AC — control de acceso de red; PR.PT — tecnologías de protección) · Detectar (DE.CM)
> **ISO/IEC 27001:** A.8.20-A.8.21 (seguridad de redes y separación) · A.8.22-A.8.23 (transferencia de información) · A.8.28-A.8.29 (canales de comunicación)
> **BCU:** EMG / RNRCSF — protección de la red del sistema de pagos y de los canales de comunicación
> **URCDP:** Ley 18.331 art. 10 — las comunicaciones que transportan datos personales deben estar protegidas
> **Nivel del curso:** 🔴 Dominar

---

### ENCABEZADO
| **Campo** | **Valor** |
|---|---|
| **Código** | POL-12 |
| **Título** | Seguridad de Redes y Comunicaciones |
| **Versión** | 1.0 |
| **Estado** | [Borrador / En revisión / Aprobado] |
| **Fecha de aprobación** | [COMPLETAR] |
| **Elaborado por** | Div. TI + RSI |
| **Revisado por** | Comité de Seguridad · Producción |
| **Aprobado por** | Comité de Seguridad de la Información |
| **Clasificación** | Confidencial |
| **Próxima revisión** | [Fecha, máx. 1 año] |

### 1. Objetivo
Proteger la **infraestructura de red y las comunicaciones** del Banco mediante segmentación, filtrado, cifrado y monitoreo, garantizando que la información circule solo por los canales autorizados.

### 2. Alcance
Aplica a redes LAN/WLAN/WAN, VPN, firewalls, WAF, DMZ, segmentos de sistemas de pago, DNS, correo, telefonía IP, nube y canales con terceros.

### 3. Reglas obligatorias
- **Segmentación**: la red se segmenta por zonas de seguridad (usuario, servidores, pagos, DMZ, gestión) y las comunicaciones entre zonas se controlan por reglas (POL-12/PR-06).
- **Firewall perimetral y DMZ**: todo tráfico entrante pasa por el firewall; los servicios públicos viven en la DMZ.
- **WAF**: las aplicaciones web públicas y Banco En Línea se protegen con WAF (modo bloqueo).
- **Wi-Fi**: redes corporativas con WPA2/WPA3, redes de invitados aisladas y prohibido conectar equipos no autorizados.
- **VPN**: el acceso remoto y la interconexión de sedes usan VPN cifrada y autenticación fuerte (MFA).
- **Cifrado en tránsito**: se exige TLS en comunicaciones sensibles y cifrado en la transmisión de datos personales (POL-14).
- **Control de dispositivos**: los equipos se conectan solo si cumplen las políticas (postura, antivirus, parches).
- **Monitoreo**: el tráfico se observa y registra (POL-13); las anomalías generan alertas (PCS-09).
- **Cambios de red**: toda regla o topología nueva pasa por gestión de cambios (POL-06).

### 4. Responsabilidades
- **Div. TI / Redes**: opera firewalls, segmentación, VPN y WAF.
- **RSI**: define reglas de seguridad y prioriza hallazgos de red.
- **Operaciones de Seguridad**: monitorea y responde a alertas de red.

### 5. Cumplimiento y revisión
Las reglas de firewall sin gestión o los dispositivos no autorizados se tratan como hallazgos. Revisión anual de la política y auditoría periódica de reglas.

### Evidencia del kit
| Evidencia | Documento canónico |
|---|---|
| Diagrama de red y segmentación | PR-06, ID-01 |
| Reglas de firewall/WAF | PR-06, Actividad 45 |
| Registro de cambios de red | POL-06, PR-07 |
| Alertas y logs de red | DE-01, DE-02 |
| Controles de red | CURSO INFRA-00…14 |
