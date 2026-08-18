# VPOL-01 · Gestión de Vulnerabilidades en Uruguay

> **Función del MCU 5.0:** Proteger (PR.PS — seguridad de plataformas) · Detectar (DE.CM — monitoreo continuo)
> **ISO/IEC 27001:** A.8.8 (gestión de vulnerabilidades técnicas) · A.8.9 (gestión de configuraciones)
> **BCU:** Estándares Mínimos de Gestión (EMG) · RNRCSF (riesgo tecnológico)
> **URCDP:** Ley 18.331 art. 10 (medidas de seguridad)
> **Nivel del curso:** 🟢 Descubrir → 🟡 Practicar

---

## 1. ¿Qué es una vulnerabilidad?

Una **vulnerabilidad** es una debilidad en un sistema (software, configuración, diseño o proceso) que un atacante puede explotar. No es el ataque: es la **puerta** que el ataque usa.

| Concepto | Qué es | Ejemplo |
|---|---|---|
| **Vulnerabilidad** | Debilidad explotable | Un servidor web sin parche con CVE conocido |
| **Amenaza** | Lo que aprovecha la debilidad | Un atacante que escanea internet buscando ese servidor |
| **Riesgo** | Probabilidad × impacto | Alta probabilidad + alto impacto = riesgo crítico |
| **Exploit** | Programa/paquete que explota la vulnerabilidad | Script público que toma el control |

## 2. CVE y CVSS: el idioma de las vulnerabilidades

- **CVE** (Common Vulnerabilities and Exposures): identificador único de cada vulnerabilidad pública. Ejemplo: `CVE-2021-44228` (Log4Shell). Se publican en el catálogo de MITRE (www.cve.org).
- **CVSS** (Common Vulnerability Scoring System): puntaje de 0 a 10 que indica severidad (crítico ≥ 9.0, alto 7.0–8.9, medio 4.0–6.9, bajo < 4.0).
- El CVSS es un **punto de partida**: la prioridad real se ajusta por contexto (exposición a internet, datos personales, exploit público activo).

## 3. El ciclo de gestión de vulnerabilidades

1. **Identificar:** inventario de activos (ID-01) actualizado + escaneos periódicos.
2. **Evaluar:** cruzar los hallazgos con la base CVE/CVSS y el contexto del activo.
3. **Priorizar:** decidir qué corregir primero según riesgo real (no solo severidad).
4. **Corregir:** aplicar parche, mitigación temporal o aceptar el riesgo con excepción formal.
5. **Verificar:** confirmar que la vulnerabilidad desapareció y que el servicio quedó operativo.
6. **Repetir:** es un proceso continuo, no un evento.

## 4. Qué espera el regulador uruguayo

| Referencia | Qué exige sobre vulnerabilidades |
|---|---|
| **Agesic · MCU 5.0** | PR.PS (seguridad de plataformas: configuración y mantenimiento), DE.CM (monitoreo continuo). Guía: escaneo periódico (recomendado mensual) y corrección según criticidad. |
| **Agesic · CERTuy** | Monitoreo de alertas y coordinación ante vulnerabilidades activas. |
| **BCU · EMG** | Gestión del riesgo tecnológico: identificación, evaluación y tratamiento de vulnerabilidades en el marco de los estándares mínimos. |
| **URCDP · Ley 18.331** | Art. 10: medidas de seguridad técnicas y organizativas para proteger datos personales (el parcheo es una de ellas). |

## 5. Herramientas libres para gestionar vulnerabilidades

| Herramienta | Para qué |
|---|---|
| **OpenVAS / Greenbone** | Escaneo de vulnerabilidades de red e infraestructura |
| **Trivy** | Escaneo de imágenes de contenedores (CVEs) |
| **pip-audit** | Auditoría de dependencias de Python |
| **Bandit / Semgrep** | Análisis estático de código (SAST) |
| **OWASP ZAP** | Pruebas dinámicas sobre aplicaciones web (DAST) |
| **Wazuh** | Detección en tiempo real y correlación (SIEM) |
| **GLPI + plugins** | Inventario de activos (base del proceso) |

> En este kit, el **template VPOL-20 (Vulnerability Management)** transforma esta teoría en política; el **PR-06** de `02-ENTREGABLES` la transforma en documento operativo; y el curso `rsi-tools` (módulos 09 y 10) enseña a usar las herramientas.

## 6. Evidencia que demuestra el cumplimiento

- Escaneos ejecutados (fecha, alcance, herramienta).
- Reportes con CVEs y severidades.
- Registro de corrección (fecha de parcheo) y verificación posterior.
- Excepciones aceptadas con mitigación compensatoria.
- Métricas: % activos escaneados, tiempo medio de corrección, vulnerabilidades críticas abiertas.

> **Regla de oro:** sin inventario no hay escaneo confiable; sin escaneo no hay priorización; sin priorización no hay parcheo; sin verificación no hay evidencia.
