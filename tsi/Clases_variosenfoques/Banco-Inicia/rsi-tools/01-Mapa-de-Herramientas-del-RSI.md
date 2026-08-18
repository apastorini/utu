# TOOLS-01 · Mapa de Herramientas del RSI

> **Función del MCU 5.0:** Vista general de cómo las herramientas open source cubren las seis funciones (GV, ID, PR, DE, RS, RC) y cómo priorizar la instalación.
> **ISO/IEC 27001:** El mapa conecta herramientas con controles del Anexo A para no instalar "por instalar": cada herramienta responde a un control.
> **BCU:** La Guía de EMG pide evidencia concreta; el mapa ordena qué herramienta produce cada evidencia.
> **URCDP:** El mapa identifica qué herramientas ayudan a las medidas de seguridad de datos personales.
> **Nivel del curso:** 🟢 Descubrir

---

## 1. La idea central

Un RSI/CISO no necesita 50 herramientas: necesita **la herramienta justa para cada problema**, instalada una vez, bien configurada, y con su evidencia documentada. Este curso instala **~15 herramientas open source** distribuidas así:

| Función MCU 5.0 | Herramienta (módulo) | Qué resuelve |
|---|---|---|
| GV · Gobernar | Repositorio documental + matriz (TOOLS-03) | Organiza normas y documentos del SGSI |
| ID · Identificar | Nmap/Zenmap, GLPI (TOOLS-04) · planilla riesgos, Eramba (TOOLS-05) | Qué tengo, qué puede salir mal |
| PR · Proteger | Bitwarden/TOTP (TOOLS-06) · VeraCrypt/7-Zip/OpenSSL (TOOLS-07) · Gophish (TOOLS-08) · OpenVAS/Trivy/ZAP/Semgrep (TOOLS-09) | Contraseñas, cifrado, personas, vulnerabilidades |
| DE · Detectar | Wazuh, Suricata, Grafana/Loki, Sysmon (TOOLS-10) | Ver lo que pasa, alertar |
| RS · Responder | TheHive/Cortex, Volatility, Autopsy (TOOLS-11) | Reaccionar, investigar, preservar |
| RC · Recuperar | Veeam/rsync/BorgBackup (TOOLS-12) | Volver a operar |

---

## 2. Prioridad de instalación (según el SGSI)

El SGSI se construye por etapas. Por eso el curso sugiere este orden de instalación:

1. **TOOLS-02** (entorno base) — sin esto no podés probar nada de forma aislada.
2. **TOOLS-03** (repositorio normativo) — primero el marco, después las herramientas.
3. **TOOLS-04 y TOOLS-05** (inventario y riesgos) — primero conocer qué tenés.
4. **TOOLS-06 y TOOLS-07** (contraseñas y cifrado) — controles de bajo costo y alto impacto.
5. **TOOLS-09** (vulnerabilidades) — parchar lo que hay.
6. **TOOLS-10** (SIEM) — observar.
7. **TOOLS-08, 11, 12, 13** — el resto en paralelo.

> **Regla de oro:** no instales todo el mismo día. Cada herramienta debe estar **justificada** (¿qué requisito cumple?), **documentada** (¿qué evidencia produce?) y **probada** (¿funciona en tu entorno?).

---

## 3. Requisitos mínimos del puesto de trabajo del RSI

| Recurso | Mínimo | Recomendado |
|---|---|---|
| RAM | 8 GB | 16 GB |
| Disco libre | 30 GB | 60 GB |
| CPU | 4 núcleos | 8 núcleos |
| Virtualización | Activar VT-x/AMD-V en BIOS | Idem |
| Sistema operativo | Windows 10/11 o Linux | Windows 11 Pro o Ubuntu LTS |

Si tu PC no llega a los 16 GB, adaptá el laboratorio: corré una VM por vez (TOOLS-02 explica cómo).

---

## 4. Licencias y reglas de uso

Todas las herramientas del curso son **open source o free**:

| Herramienta | Licencia | Nota |
|---|---|---|
| VirtualBox | GPL | Gratuito, de Oracle |
| Linux (Ubuntu/Debian) | GPL | Sistema base de las VMs |
| Nmap/Zenmap | GPL | Escaneo de red |
| GLPI | GPL | Inventario y tickets |
| Eramba / OpenRisk | AGPL / GPL | Registro de riesgos |
| Bitwarden / Vaultwarden | GPL / GPL | Gestor de contraseñas |
| VeraCrypt | Apache 2.0 | Cifrado de discos |
| Gophish | MIT | Simulacros de phishing |
| OpenVAS (Greenbone) | GPL | Escáner de vulnerabilidades |
| Trivy | Apache 2.0 | Vulnerabilidades de contenedores |
| OWASP ZAP | Apache 2.0 | Pruebas web (DAST) |
| Semgrep | LGPL | Análisis estático (SAST) |
| Wazuh | GPL | SIEM/XDR |
| Suricata | GPL | IDS/IPS |
| Grafana / Loki | AGPL | Monitoreo |
| TheHive / Cortex | AGPL | Gestión de incidentes |
| Volatility | GPL | Forense de memoria |
| Autopsy | Apache 2.0 | Forense de disco |
| BorgBackup | BSD | Respaldo |

> **Importante para el Banco:** verificar siempre con el Comité de Seguridad y el área legal los términos de cada licencia antes de usarlas en producción. Este curso las instala en un entorno de laboratorio de aprendizaje.

---

## 5. Cómo cargar "cosas de BCU, MCU y URCDP"

Un error común del RSI es tener las herramientas y no tener las **normas** cargadas. El módulo TOOLS-03 te enseña a armar un **repositorio normativo** ordenado, donde descargás y guardás:

- **MCU 5.0** y su guía de implementación (sitio de Agesic).
- **Guía EMG del BCU** (Estándares Mínimos de Gestión) y el RNRCSF art. 492.
- **Ley 18.331, Ley 19.670, Decreto 64/020** (protección de datos).
- **Decreto 66/025** (cometidos de Agesic en seguridad).
- **Circular 2227** del BCU (riesgo operacional).

Cada norma se guarda con un código y se enlaza a las plantillas del kit (MATRIZ-001 las cruza todas).

---

## 6. Lista de verificación del módulo

- ☐ Identifiqué qué herramienta cubre cada función del MCU 5.0.
- ☐ Defini mi orden de instalación según la prioridad del SGSI.
- ☐ Verifiqué que mi PC cumple los requisitos mínimos.
- ☐ Revisé las licencias con el Comité de Seguridad / legal.
- ☐ Guardé el acceso a los sitios oficiales de descarga (solo fuentes oficiales).

---

**Documentos relacionados:** MATRIZ-001, ID-05, HERRAM-001, GV-04
