# VPOL-15 · Network Security Policy

> **Función del MCU 5.0:** Proteger (PR.AC — control de acceso a la red; PR.PS — seguridad de plataformas) · Detectar
> **ISO/IEC 27001:** A.8.20/8.21/8.22 (seguridad de redes) · A.8.23 (segregación) · A.8.26 (seguridad en desarrollo) · A.8.27
> **BCU:** EMG y Circular 2280 — protección de la red del sistema de pagos; segregación y control de perímetro
> **URCDP:** Ley 18.331 art. 10 — medidas técnicas de seguridad en el transporte y almacenamiento
> **Nivel del curso:** 🔴 Dominar

---

### ENCABEZADO
| **Campo** | **Valor** |
|---|---|
| **Código** | VPOL-15 |
| **Título** | Network Security |
| **Versión** | 1.0 |
| **Estado** | [Borrador / En revisión / Aprobado] |
| **Fecha de aprobación** | [COMPLETAR] |
| **Elaborado por** | Div. TI (Redes) + RSI |
| **Revisado por** | Comité de Seguridad |
| **Aprobado por** | Comité de Seguridad de la Información |
| **Clasificación** | Confidencial |
| **Próxima revisión** | [Fecha, máx. 1 año] |

### 1. Objetivo
Definir cómo se **diseña, protege, segmenta y monitorea** la red del Banco para impedir accesos no autorizados, contener incidentes y proteger los sistemas críticos (core, pagos, Banco En Línea).

### 2. Alcance
Aplica a toda la infraestructura de red del Banco: routers, switches, firewalls, WAF, VPN, Wi-Fi, DMZ, segmentos internos, red de gestión, enlaces a sucursales y proveedores, y redes en nube (VPOL-10).

### 3. Principios de diseño
- **Defensa en profundidad:** múltiples capas (perímetro → DMZ → segmentos internos → hosts).
- **Segregación por zonas de seguridad** (MCU 5.0 / buenas prácticas): internet, DMZ, red interna, red de gestión, red de pagos/core aislada.
- **Menor exposición:** se publica a internet solo lo imprescindible (frontales en DMZ).
- **Ingreso por defecto denegar:** todo tráfico no autorizado expresamente se bloquea (listas de control de acceso y reglas de firewall).
- **IPv4 e IPv6:** las reglas aplican por igual a ambos protocolos; no se publican servicios en IPv6 sin protección equivalente.

### 4. Controles de red obligatorios
- **Firewall perimetral y DMZ** con reglas mínimas y revisión periódica de reglas.
- **WAF** delante de las aplicaciones web públicas (Banco En Línea) en modo bloqueo, con reglas de OWASP (VPOL-15 bis / actividad 45 del curso RSI).
- **Segmentación interna:** la red de producción, la de gestión y la de datos de clientes están aisladas con controles de tránsito.
- **Red Wi-Fi:** separación de red corporativa y de invitados; WPA2/3-Enterprise para la corporativa; prohibido el acceso de invitados a la red interna.
- **VPN:** acceso remoto cifrado y con **MFA obligatoria** (PR-01); perfiles según el nivel de acceso.
- **Seguridad de los enlaces a terceros:** solo servicios autorizados (VPOL-18), sin acceso a segmentos innecesarios.
- **IPv6:** se documentan las zonas y reglas; se bloquea el tránsito no autorizado igual que IPv4.

### 5. NAT / enmascaramiento
- El Banco usa **NAT** para ocultar la red interna y salir a internet con IP pública de rango oficial (PR-NET-01).
- Las zonas internas usan **direcciones privadas (RFC 1918)** e IPv6 con direccionamiento interno; se documenta el esquema de direccionamiento.
- El **enmascaramiento de puertos** (PAT) se configura solo donde sea necesario; los servicios publicados se exponen vía DMZ con reglas específicas, no con mapeo genérico.

### 6. Monitoreo y gestión de red
- Los equipos de red se monitorean (SNMP seguro, SIEM) y sus configuraciones se respaldan (VPOL-11).
- La **gestión** de los equipos se hace por la red de gestión aislada, con accesos restringidos y registrados (VPOL-14).
- Los cambios de red siguen el proceso de **gestión de cambios** (VPOL-08).

### 7. Cumplimiento y revisión
Las reglas de firewall se **revisan trimestralmente** y las que están obsoletas se eliminan. Los accesos abiertos sin justificación se cierran. Revisión anual de la política.

### Evidencia del kit
| Evidencia | Documento canónico |
|---|---|
| Diagrama de red / DMZ | BCU-01 (arquitectura) |
| Reglas de firewall y WAF | PR-06 (configuración) |
| Registro de cambios de red | GV-06, PR-07 |
| Diagrama de red del curso | VPOL-15 / DMZ |
