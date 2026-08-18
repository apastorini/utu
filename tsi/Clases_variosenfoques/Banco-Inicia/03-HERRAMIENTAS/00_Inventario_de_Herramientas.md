# Inventario de Herramientas para el SGSI del Banco

> **Código:** HERRAM-001 · **Versión:** 1.0
> **Objetivo:** listar las herramientas (priorizando software libre / de bajo costo) que el Banco puede usar para implementar y sostener cada función del SGSI. Todas son ejemplos: la decisión de compra la toma el Comité según presupuesto y contexto.

---

## 1. Herramientas por función del MCU 5.0

### Gobernar (GV)
| Herramienta | Para qué | Libre/Comercial |
|---|---|---|
| Lista de verificación del MCU 5.0 (Agesic) | Diagnóstico de madurez | Libre (sitio Agesic) |
| Planilla xlsx "Implantación SGSI – Inventario de activos y Evaluación de riesgos" (Agesic) | Inventario + riesgos | Libre (sitio Agesic) |
| Microsoft 365 / SharePoint del Banco | Repositorio documental del SGSI | Comercial (ya en uso) |
| LibreOffice Calc / Excel | Matriz de riesgo, plan de tratamiento, SoA | Libre/Comercial |
| ERP de gestión de riesgos (o planilla) | Registro de riesgos y tratamiento | A definir |

### Identificar (ID)
| Herramienta | Para qué | Libre/Comercial |
|---|---|---|
| **Nmap** + **Zenmap** | Descubrimiento de activos y puertos en red | Libre |
| Inventario de hardware/software del parque (o planilla) | Base del inventario de activos | A definir |
| Diagramas.net (draw.io) | Diagramas de red y de flujos de datos | Libre |
| **GLPI** | Inventario de activos y gestión de incidencias | Libre |
| **Eramba** / **OpenRisk** (o planilla) | Registro de riesgos | Libre |

### Proteger (PR)
| Herramienta | Para qué | Libre/Comercial |
|---|---|---|
| **Bitwarden** / **Vaultwarden** | Gestor de contraseñas y secretos | Libre |
| MFA: **Authenticator** (TOTP) o tokens hardware | Segundo factor para accesos | Libre/Comercial |
| **VeraCrypt** | Cifrado de discos y volúmenes | Libre |
| **OpenSSL** / PowerShell | Cifrado de archivos y gestión de claves | Libre |
| **ClamAV** (con gestión central) o antivirus corporativo | Protección contra malware | Libre/Comercial |
| **Veeam Community / Btrfs / rsync** + almacenamiento externo | Copias de respaldo (PR-05, art. 492) | Libre/Comercial |
| **OpenVAS / Greenbone** | Escaneo de vulnerabilidades (PR-06) | Libre |
| **Trivy** | Escaneo de vulnerabilidades de imágenes/containers | Libre |
| **OWASP ZAP** | Pruebas de seguridad de aplicaciones web (DAST) | Libre |
| **Semgrep** | Análisis estático de código (SAST) | Libre |
| **Gophish** | Simulacros de phishing (PR-02) | Libre |
| **7-Zip** con cifrado | Compresión y cifrado de archivos | Libre |

### Detectar (DE)
| Herramienta | Para qué | Libre/Comercial |
|---|---|---|
| **Wazuh** (SIEM + XDR) | Centralización de logs, correlación, detección de intrusos | Libre |
| **Sysmon** (Windows) + **auditd** (Linux) | Registro detallado de eventos de los endpoints | Libre |
| **Suricata** | Detección de intrusiones en red (IDS/IPS) | Libre |
| **Grafana + Loki/Prometheus** | Monitoreo y paneles de indicadores | Libre |
| **Nessus Essentials** | Escaneo de vulnerabilidades adicional | Freemium |
| Metadefender / Sandbox (opcional) | Análisis de malware | Comercial |

### Responder (RS)
| Herramienta | Para qué | Libre/Comercial |
|---|---|---|
| Sistema de tickets (GLPI / OTRS / TheHive) | Registro y seguimiento de incidentes | Libre |
| **TheHive** + **Cortex** | Gestión de incidentes y análisis | Libre |
| **Volatility** | Análisis forense de memoria (RS-03) | Libre |
| **Autopsy / FTK Imager** | Forense de disco y preservación de evidencia | Libre |
| **Guake/KeePass** | Custodia de credenciales del equipo de respuesta | Libre |

### Recuperar (RC)
| Herramienta | Para qué | Libre/Comercial |
|---|---|---|
| Entornos de recuperación / sitio alternativo | DRP (RC-02) | A definir |
| Simulacros de continuidad (documentados) | Pruebas BCP/DRP | Proceso |
| **Rsync/Restic/BorgBackup** | Respaldos versionados y cifrados | Libre |
| Comunicación de crisis (plantillas + sistema de avisos) | RC-03 | Proceso |

---

## 2. Herramientas ofimáticas para producir los entregables

| Tarea | Herramienta sugerida |
|---|---|
| Editar plantillas `.md` | VS Code, Notepad++, Typora, Obsidian |
| Convertir `.md` a `.docx` | `03-HERRAMIENTAS/md_a_docx.py` (python-docx) o Pandoc |
| Planillas de cálculo (riesgos, SoA, inventario) | Excel / LibreOffice Calc; plantilla oficial Agesic (.xlsx) |
| Diagramas (red, organigrama, procesos) | draw.io, Visio, LibreOffice Draw |
| Actas y firmas | Circuito documental del Banco (firma digital) |

## 3. Buenas prácticas al elegir herramientas

1. **Priorizar por riesgo:** primero lo que mitiga los riesgos más altos del Banco (accesos, respaldos, malware, vulnerabilidades).
2. **Pocas herramientas, bien gestionadas:** mejor consolidar (ej. Wazuh para logs+EDR) que acumular soluciones sin operar.
3. **Probar antes de comprar:** hacer pilotos en ambiente de pruebas.
4. **Verificar soporte y actualizaciones:** las herramientas de seguridad sin parches son un riesgo.
5. **Registrar decisiones:** cada herramienta seleccionada queda documentada en el plan de tratamiento (ID-04) y en el inventario de activos (ID-01).

## 4. Enlaces oficiales de referencia

- Agesic – Guías del Marco de Ciberseguridad 5.0 (incluye planilla SGSI xlsx): `https://www.gub.uy/agencia-gobierno-electronico-sociedad-informacion-conocimiento/comunicacion/publicaciones/guias-sobre-marco-ciberseguridad`
- URCDP – Sistema de gestión en línea (inscripción de bases, DPD): `https://www.gub.uy/unidad-reguladora-control-datos-personales`
- BCU – Recopilación de Normas y circulares: `https://www.bcu.gub.uy`
