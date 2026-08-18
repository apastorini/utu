# TOOLS-14 · Plan de Adopción y Correspondencia Normativa Final

> **Función del MCU 5.0:** Gobernar (GV.OV, GV.RM): planificar, medir y demostrar; todas las funciones convergen en este módulo de cierre.
> **ISO/IEC 27001:** Cláusula 10 (mejora) y el ciclo PDCA.
> **BCU:** La evidencia consolidada es la que el BCU evalúa en las inspecciones EMG.
> **URCDP:** El repositorio de evidencia consolida el cumplimiento de protección de datos.
> **Nivel del curso:** 🔴 Dominar

---

## 1. Objetivo del módulo

Este módulo cierra el curso: te muestra cómo **pasar del laboratorio a la adopción** en el Banco, cómo mantener el inventario de herramientas actualizado y cómo **demostrar cumplimiento** ante Agesic (MCU 5.0), el BCU (EMG) y la URCDP.

---

## 2. Inventario final de herramientas del curso

| Módulo | Herramienta | Función MCU | Estado sugerido en el Banco |
|---|---|---|---|
| TOOLS-02 | VirtualBox | Entorno | Laboratorio (y en producción si se justifica) |
| TOOLS-03 | Obsidian/Joplin + LibreOffice | GV | Producción (oficina del RSI) |
| TOOLS-04 | Nmap/Zenmap + GLPI | ID | GLPI: producción; Nmap: con autorización |
| TOOLS-05 | Planilla Agesic + Eramba | ID | Producción (marco de riesgos) |
| TOOLS-06 | Vaultwarden/Bitwarden + TOTP | PR | Producción (prioridad alta) |
| TOOLS-07 | VeraCrypt/7-Zip/OpenSSL/GnuPG | PR | Producción |
| TOOLS-08 | Gophish | PR | Con autorización de dirección/legal |
| TOOLS-09 | OpenVAS, Trivy, ZAP, Semgrep | PR/DE | Producción (con alcance autorizado) |
| TOOLS-10 | Wazuh, Suricata, Grafana/Loki, Sysmon | DE | Producción (prioridad alta) |
| TOOLS-11 | TheHive/Cortex, Volatility, Autopsy | RS | Producción (CSIRT) |
| TOOLS-12 | Veeam, rsync, BorgBackup | RC | Producción (prioridad alta) |

> Este inventario se mantiene en **HERRAM-001** (inventario de herramientas del kit) y en **ID-01** (inventario de activos del SGSI).

---

## 3. Hoja de ruta de adopción (plan de 12 meses)

| Mes | Acción | Plantilla que actualizás |
|---|---|---|
| 1 | Aprobar políticas y designar RSI (GV-01, GV-03) | GV-01, GV-03 |
| 2 | Instalar Vaultwarden + TOTP en producción | PR-01, PR-03 |
| 3 | Desplegar Wazuh en los servidores críticos | DE-01, BCU-04 |
| 4 | GLPI + inventario de activos completo | ID-01 |
| 5 | Primer análisis de riesgos formal (planilla Agesic/Eramba) | ID-02, ID-03 |
| 6 | Programa de concientización + primer simulacro | PR-02 |
| 7 | OpenVAS + proceso de parcheo mensual | PR-06 |
| 8 | Respaldos 3-2-1 + primera prueba de restauración | PR-05, RC-02 |
| 9 | TheHive + CSIRT operativo | RS-01, RS-03 |
| 10 | Documento de Seguridad URCDP completo | URCDP-01, URCDP-04 |
| 11 | Primera auditoría interna (autoevaluación MCU 5.0) | BCU-05, ID-05 |
| 12 | Informe del RSI a la Dirección | GV-06 |

---

## 4. Correspondencia normativa final (resumen)

| Requisito | Evidencia que producen las herramientas |
|---|---|
| MCU 5.0 – ID (conocer activos y riesgos) | Nmap/GLPI (TOOLS-04), Eramba/planilla (TOOLS-05) |
| MCU 5.0 – PR (proteger) | Bitwarden, VeraCrypt (TOOLS-06/07), OpenVAS (TOOLS-09) |
| MCU 5.0 – DE (detectar) | Wazuh/Suricata (TOOLS-10) |
| MCU 5.0 – RS (responder) | TheHive/Volatility/Autopsy (TOOLS-11) |
| MCU 5.0 – RC (recuperar) | Veeam/Borg (TOOLS-12) |
| BCU – EMG (gobierno y riesgo TIC) | Eramba (TOOLS-05), Wazuh (TOOLS-10), informe GV-06 |
| URCDP – Documento de Seguridad | Toda la evidencia consolidada (TOOLS-13) |
| URCDP – Notificación 72 h | TheHive + logs (TOOLS-11/10) |
| Decreto 66/025 – CERTuy y trazabilidad | Wazuh + retención ≥12 meses (TOOLS-10) |

Esta matriz se documenta en **MATRIZ-001**.

---

## 5. Mantenimiento: el curso nunca "termina"

- **Actualizar** herramientas y firmas (reglas de Suricata, base de CVE de OpenVAS, actualizaciones de Wazuh) al menos mensualmente.
- **Re-ejecutar** los simulacros de phishing y las pruebas de restauración con periodicidad.
- **Revisar** el inventario de herramientas (HERRAM-001) y el mapa de prioridades (TOOLS-01) cada semestre.
- **Capacitar** a nuevos integrantes del equipo con este mismo curso.

---

## 6. Cómo volcarlo a las plantillas del kit

- **GV-04 (Plan Anual de Seguridad)**: la hoja de ruta de 12 meses se vuelca aquí.
- **GV-06 (Informe del RSI)**: el estado de cada herramienta y su evidencia alimenta el informe a la Dirección.
- **ID-05 (Perfil de Ciberseguridad)**: la madurez por función sube a medida que se adoptan las herramientas.
- **BCU-05 (Auditoría Interna)**: el repositorio de evidencia es la fuente de la auditoría.
- **MATRIZ-001**: la correspondencia final queda documentada.

---

## 7. Lista de verificación del módulo

- ☐ Inventario final de herramientas cargado en HERRAM-001.
- ☐ Hoja de ruta de 12 meses definida en GV-04.
- ☐ Correspondencia normativa consolidada en MATRIZ-001.
- ☐ Responsables y plazos asignados a cada acción.
- ☐ Fecha de revisión semestral del plan agendada.

---

**Documentos relacionados:** GV-04, GV-06, ID-05, BCU-05, MATRIZ-001, HERRAM-001
