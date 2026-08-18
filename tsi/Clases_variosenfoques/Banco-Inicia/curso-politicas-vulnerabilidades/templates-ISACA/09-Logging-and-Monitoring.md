# VPOL-14 · Logging and Monitoring Policy

> **Función del MCU 5.0:** Detectar (DE.AE — análisis; DE.CM — monitoreo continuo)
> **ISO/IEC 27001:** A.8.15 (registro de actividad) · A.8.16 (gestión de eventos) · A.8.17 (protección de logs)
> **BCU:** EMG — detección y trazabilidad; los registros son evidencia ante el BCU
> **URCDP:** Ley 18.331 art. 10 y art. 27-bis — los logs permiten detectar y notificar vulneraciones
> **Nivel del curso:** 🟡 Practicar

---

### ENCABEZADO
| **Campo** | **Valor** |
|---|---|
| **Código** | VPOL-14 |
| **Título** | Logging and Monitoring |
| **Versión** | 1.0 |
| **Estado** | [Borrador / En revisión / Aprobado] |
| **Fecha de aprobación** | [COMPLETAR] |
| **Elaborado por** | Operaciones de Seguridad (SOC) |
| **Revisado por** | RSI |
| **Aprobado por** | Comité de Seguridad de la Información |
| **Clasificación** | Confidencial |
| **Próxima revisión** | [Fecha, máx. 1 año] |

### 1. Objetivo
Definir qué eventos se **registran, conservan y analizan** en los sistemas del Banco, para **detectar** incidentes, **investigar** los ocurridos, **demostrar** el cumplimiento normativo y **mejorar** la seguridad de forma continua.

### 2. Alcance
Aplica a los sistemas que generan registros de seguridad: sistemas operativos, aplicaciones (core, Banco En Línea, pagos), bases de datos, equipos de red, firewalls/WAF, servidores de correo, SIEM, accesos (físicos y lógicos) y servicios en nube.

### 3. Qué se registra (mínimo)
- **Accesos:** intentos exitosos y fallidos (inicio de sesión, cierre, cambios de contraseña), cuentas administradoras/privilegiadas.
- **Autenticación y autorización:** MFA, uso de tokens, cambios de permisos.
- **Cambios de configuración** en equipos de seguridad y sistemas críticos.
- **Operaciones sensibles:** transferencias, altas/bajas de usuarios, accesos a datos de clientes.
- **Fugas de tráfico/reglas de firewall** bloqueadas (denegaciones), ataques web bloqueados por el WAF.
- **Eventos de malware/EDR y alertas del antivirus.**
- **Logs de aplicaciones críticas** y de base de datos (consultas a datos personales).

### 4. Protección de los registros
- **Integridad:** logs **inalterables** (append-only, sellado de tiempo, traslado a un destino protegido).
- **Conservación:** [COMPLETAR: p. ej. mínimo 6 meses en línea y 24 meses archivados], según requisitos del BCU y la URCDP.
- **Acceso restringido:** solo el SOC y el RSI leen logs; las cuentas de lectura se auditan.
- **Centralización:** los logs se remiten al **SIEM (Wazuh)** para correlación y alertas (DE-01).
- **Reloj sincronizado** (NTP) en todas las fuentes para una correlación fiable.

### 5. Monitoreo y respuesta
- El SOC monitorea las alertas del SIEM con **prioridades** (crítico: respuesta inmediata).
- **Casos de uso** prioritarios: accesos anómalos (hora, lugar), múltiples fallas de login (fuerza bruta), escaladas de privilegios, movimiento lateral, exfiltración de datos (DLP).
- Toda alerta confirmada se registra como **incidente** y sigue el plan RS-01.
- Revisión de logs **quincenal** de las cuentas privilegiadas (o al menos mensual) con evidencia.

### 6. Privacidad y datos personales
- El monitoreo de comunicaciones y accesos de empleados se realiza conforme a la Ley 18.331, con finalidad legítima (protección de la información) e información previa a los empleados (VPOL-06).
- Los logs que contengan datos personales (p. ej. accesos a clientes) se tratan bajo la política de retención y eliminación segura.

### 7. Cumplimiento y revisión
La falta de logs o su alteración en sistemas críticos se trata como **incidente grave** y puede configurar obstrucción de auditorías. Revisión anual.

### Evidencia del kit
| Evidencia | Documento canónico |
|---|---|
| SIEM Wazuh y casos de uso | DE-01, DE-02 |
| Procedimiento de respuesta a alertas | RS-01 |
| Política de retención de logs | URCDP-01 (retención) |
| Revisión de cuentas privilegiadas | PR-01 |
