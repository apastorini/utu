# TOOLS-00 · Índice y Mapa del Curso

> **Función del MCU 5.0:** Dar al RSI/CISO un cajón de **herramientas open source** para ejecutar las seis funciones del Marco de Ciberseguridad 5.0 (Gobernar, Identificar, Proteger, Detectar, Responder, Recuperar) con software libre y sin costo de licencia.
> **ISO/IEC 27001:** Las herramientas apoyan los controles del Anexo A: gestión de activos (A.5.9), control de acceso y contraseñas (A.5.15–A.5.18), cifrado (A.8.24), protección contra malware (A.8.7), gestión de vulnerabilidades (A.8.8), registro y seguimiento (A.8.15–A.8.17), gestión de incidentes (A.5.24–A.5.28) y continuidad (A.5.29).
> **BCU:** Sustenta la evidencia técnica y documental que exigen la Guía de Estándares Mínimos de Gestión (EMG), el RNRCSF (art. 492) y la Circular 2227 (riesgo operacional).
> **URCDP:** Permite documentar y demostrar medidas de seguridad para datos personales (Ley 18.331, Ley 19.670, Decreto 64/020): inventarios, análisis de riesgo, cifrado, registros y notificación de vulneraciones.
> **Decreto 66/025:** Prepara al RSI para demostrar ante Agesic/CERTuy trazabilidad, evidencia y respuesta a incidentes.
> **Nivel del curso:** 🟢 Descubrir · 🟡 Practicar · 🔴 Dominar

---

## 1. Presentación del curso

Bienvenido al curso **"rsi-tools: caja de herramientas open source para el RSI/CISO del Banco"**. Este curso vive en la carpeta `rsi-tools` y forma parte del kit **Banco-Inicia**.

Este curso es **100% práctico**: su objetivo es que instales, configures y empieces a usar herramientas **open source (gratuitas, sin licencia)** que te ayuden a hacer el trabajo del RSI uruguayo: conocer tus activos, medir tus riesgos, proteger la información, detectar incidentes, responder y demostrar cumplimiento ante **Agesic (MCU 5.0)**, el **BCU (EMG)** y la **URCDP**.

Cada módulo es un **paso a paso** que podés seguir en tu propia PC, con comandos copiables, capturas de referencia y una lista de qué documento del kit alimenta con esa herramienta.

---

## 2. Para quién es este curso

| Perfil | Por qué le sirve |
|---|---|
| RSI / CISO del Banco | Es el destinatario principal: necesita herramientas concretas para gobernar, identificar, proteger, detectar, responder y recuperar. |
| Oficial de seguridad (segunda línea) | Ejecuta en el día a día los controles: monitoreo, parches, cifrado, concientización. |
| Personal de TI | Instala y administra las herramientas; este curso le da el "por qué" normativo de cada una. |
| Auditores internos / externos | Entienden qué herramientas pueden usarse como fuente de evidencia. |
| Personas sin conocimientos previos | El curso arranca desde cero: se explica qué es una máquina virtual, qué es un SIEM, etc. |

### Qué vas a saber al terminar

- Preparar un **entorno de trabajo** (VirtualBox + una máquina virtual Linux y Windows) para probar herramientas sin romper tu PC.
- **Cargar el marco normativo** (MCU 5.0, EMG del BCU, normas URCDP) en un repositorio documental ordenado.
- Instalar y usar herramientas para **cada función del MCU 5.0**.
- Generar **evidencia** con esas herramientas y volcarla a las plantillas del kit.
- Correlacionar cada herramienta con **requisitos normativos** concretos (qué le demostrás a Agesic, al BCU y a la URCDP).

---

## 3. Los 15 módulos del curso

El curso tiene **15 módulos**, numerados de **TOOLS-00** a **TOOLS-14**. Esta es la tabla general:

| Módulo | Tema | Nivel | Plantillas/documentos del kit relacionados |
|---|---|---|---|
| TOOLS-00 | Índice y mapa del curso | 🟢 | Todos (es la puerta de entrada) |
| TOOLS-01 | Mapa de herramientas del RSI (qué herramienta cubre cada función y qué instalar primero) | 🟢 | MATRIZ-001, ID-05, HERRAM-001 |
| TOOLS-02 | Entorno base: VirtualBox + máquina virtual Linux y Windows | 🟡 | PR-04, PR-06 |
| TOOLS-03 | Cargar el marco normativo (MCU 5.0, EMG BCU, URCDP, Decreto 66/025) en el repositorio | 🟡 | GV-01, GV-02, GV-03, MATRIZ-001 |
| TOOLS-04 | Inventario de activos: Nmap/Zenmap + GLPI | 🟡 | ID-01, ID-02, URCDP-01 |
| TOOLS-05 | Gestión de riesgos: planilla Agesic + Eramba/OpenRisk | 🟡→🔴 | ID-02, ID-03, ID-04, ID-05 |
| TOOLS-06 | Contraseñas y secretos: Bitwarden/Vaultwarden + TOTP | 🟡 | PR-01, PR-03, BCU-03 |
| TOOLS-07 | Cifrado: VeraCrypt, 7-Zip, OpenSSL, GnuPG | 🟡 | PR-03, URCDP-01, URCDP-05 |
| TOOLS-08 | Concientización: Gophish (simulacros de phishing) + ZAP/Zoom alternativas | 🟡 | PR-02 |
| TOOLS-09 | Vulnerabilidades y parches: OpenVAS, Trivy, Wazuh vulnerability, OWASP ZAP, Semgrep | 🔴 | PR-06, PR-07, DE-03, BCU-04 |
| TOOLS-10 | Detección y monitoreo: Wazuh SIEM/XDR, Suricata, Grafana/Loki, Sysmon | 🔴 | DE-01, DE-02, BCU-04 |
| TOOLS-11 | Respuesta a incidentes: TheHive + Cortex, IRIS DFIR, Volatility, Autopsy | 🔴 | RS-01, RS-02, RS-03 |
| TOOLS-12 | Recuperación y respaldo: Veeam/rsync/BorgBackup | 🟡 | RC-01, RC-02, BCU-06 |
| TOOLS-13 | Evidencia para URCDP: Documento de Seguridad, ROPA, notificación | 🔴 | URCDP-01…URCDP-06 |
| TOOLS-14 | Plan de adopción y correspondencia normativa final | 🔴 | GV-04, GV-06, MATRIZ-001, ID-05 |

> **Nota:** los módulos TOOLS-09 a TOOLS-11 son los de mayor valor técnico (vulnerabilidades, detección y respuesta); TOOLS-13 es el que convierte la evidencia técnica en cumplimiento URCDP.

---

## 4. Ruta de aprendizaje recomendada

Se recomienda este camino:

1. **TOOLS-00** (este módulo): el mapa del curso.
2. **TOOLS-01**: mapa de herramientas (qué instalar primero, en qué orden).
3. **TOOLS-02**: preparar el entorno (VirtualBox + VMs). Base de todos los laboratorios.
4. **TOOLS-03**: cargar el marco normativo en tu repositorio documental.
5. **TOOLS-04** e **TOOLS-05**: inventario de activos y riesgos (funciones ID).
6. **TOOLS-06** y **TOOLS-07**: contraseñas y cifrado (función PR).
7. **TOOLS-08**: concientización (PR-02).
8. **TOOLS-09**: vulnerabilidades y parches.
9. **TOOLS-10**: SIEM y monitoreo (función DE).
10. **TOOLS-11**: respuesta a incidentes (función RS).
11. **TOOLS-12**: respaldo y recuperación (función RC).
12. **TOOLS-13** y **TOOLS-14**: evidencia URCDP y plan de adopción final.

### Pre-requisitos

- Para 🟢 **Descubrir**: ninguno.
- Para 🟡 **Practicar**: una PC con al menos 8 GB de RAM (16 GB recomendados) y 30 GB de disco libre.
- Para 🔴 **Dominar**: haber completado los módulos 🟡 anteriores y tener el entorno del TOOLS-02 funcionando.

---

## 5. Cómo usar cada módulo

Cada módulo sigue el mismo patrón:

1. **Qué es la herramienta y para qué sirve** (contexto, sin tecnicismos).
2. **Instalación paso a paso** (comandos copiables y opciones de descarga).
3. **Primeros pasos / configurar** (cómo hacer la primera tarea útil).
4. **Cómo volcarlo a las plantillas del kit** (evidencia).
5. **Lista de verificación** del módulo.

Reglas de oro del curso:

- **Todo en entorno aislado**: las herramientas de ataque y escaneo solo se ejecutan en las VMs del laboratorio, nunca contra la red de producción del Banco.
- **Sin datos reales**: el laboratorio se alimenta con datos de ejemplo.
- **Evidencia primero**: cada herramienta que configures debe poder mostrar algo (captura, reporte, log) para las plantillas.

---

## 6. Los tres niveles de profundidad

- 🟢 **Descubrir** — Saber qué es cada herramienta, por qué importa y qué problema resuelve.
- 🟡 **Practicar** — Instalarla y hacer la primera tarea útil.
- 🔴 **Dominar** — Configurarla a nivel de producción, automatizarla y demostrar cumplimiento.

---

## 7. Estructura de referencia del SGSI

El curso `rsi-tools` vive al nivel raíz del kit:

```
Banco-Inicia\
├── 00-PLANIFICACION\
├── 01-CURSO-RSI\
├── curso-infra\
├── Curso-relevamiento\
├── rsi-tools\                    ← ← ESTE CURSO (TOOLS-00 a TOOLS-14)
└── 02-ENTREGABLES\
    ├── H-URCDP\                  ← Plantillas de protección de datos
    ├── G-BCU\                    ← Plantillas BCU
    ├── A-GOBERNAR\ … F-RECUPERAR\  ← Funciones del MCU 5.0
    └── ...
```

---

## 8. Relación con las normas y organismos

- **Agesic (MCU 5.0):** las seis funciones del marco se cubren con herramientas: Gobernar (documentos, matriz), Identificar (inventario, riesgos), Proteger (contraseñas, cifrado, parches), Detectar (SIEM, IDS), Responder (tickets, forense), Recuperar (respaldo, continuidad).
- **BCU:** la evidencia que piden los EMG (inventarios, monitoreo, gestión de vulnerabilidades, auditoría interna) se produce con estas herramientas.
- **URCDP:** Documento de Seguridad, ROPA, análisis de riesgo y notificación de vulneraciones se alimentan con datos de estas herramientas.
- **Decreto 66/025:** la trazabilidad (≥12 meses) y la respuesta ante el CERTuy se sustentan con el SIEM y la gestión de incidentes.

---

## 9. Cierre del módulo

Viste el mapa del curso `rsi-tools`. El siguiente paso es **TOOLS-01 · Mapa de herramientas del RSI**, donde vas a decidir qué instalar primero según la prioridad del SGSI.

---

**Documentos relacionados:** MATRIZ-001, ID-05, HERRAM-001, GV-01, GV-02, GV-03, GV-04, GV-06, ID-01, ID-02, ID-03, ID-04, PR-01, PR-02, PR-03, PR-06, PR-07, DE-01, DE-02, DE-03, RS-01, RS-02, RS-03, RC-01, RC-02, BCU-03, BCU-04, BCU-06, URCDP-01, URCDP-02, URCDP-05
