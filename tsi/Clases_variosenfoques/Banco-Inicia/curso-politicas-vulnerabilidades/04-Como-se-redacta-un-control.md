# VPOL-04 · Cómo se redacta un control y su evidencia

> **Función del MCU 5.0:** Todos los marcos de control (GV, ID, PR, DE, RS, RC) se demuestran con controles y evidencia
> **ISO/IEC 27001:** Anexo A + cláusulas 6.1 y 9.1 (evaluación de controles)
> **BCU:** EMG / RNRCSF — los controles deben ser efectivos y verificables
> **URCDP:** Ley 18.331 art. 10 (medidas de seguridad) — el DPD debe poder demostrar su aplicación
> **Nivel del curso:** 🟡 Practicar → 🔴 Dominar

---

## 1. ¿Qué es un control?

Un **control** es una medida (técnica, organizativa, física o legal) que reduce el riesgo. Responde a la pregunta **"¿cómo aseguramos que se cumple la política?"**.

| Tipo | Ejemplo |
|---|---|
| Preventivo | Firewall, autenticación MFA, política de contraseñas |
| Detectivo | SIEM (Wazuh), antivirus/EDR, revisión de logs |
| Correctivo | Plan de continuidad, respaldos, plan de incidentes |
| Físico | Biometría de acceso al CPD, guardias |
| Organizativo | Políticas, segregación de funciones, capacitación |

## 2. Ficha de un control (formato estándar)

| Campo | Qué va |
|---|---|
| **Código del control** | Ej. PR-06-C1 |
| **Nombre** | Descripción breve y accionable |
| **Objetivo de control** | Riesgo que mitiga (ISO 27001 A.8.8…) |
| **Implementación** | Qué se hizo concretamente (herramienta, configuración, proceso) |
| **Dueño** | Rol responsable |
| **Frecuencia** | Permanente / mensual / anual |
| **Evidencia** | Qué artefacto demuestra que funciona |
| **Resultado** | Conforme / No conforme / En plan de acción |
| **Estado** | Vigente / En revisión / Obsoleto |

## 3. Ejemplo de control bien documentado

| Campo | Valor |
|---|---|
| **Código** | PR-06-C1 |
| **Nombre** | Escaneo mensual de vulnerabilidades sobre la red interna |
| **Objetivo** | A.8.8 gestión de vulnerabilidades técnicas |
| **Implementación** | OpenVAS instalado en la DMZ de gestión, escaneo de los segmentos internos el primer lunes de cada mes |
| **Dueño** | Operaciones de Seguridad |
| **Frecuencia** | Mensual |
| **Evidencia** | Reporte de OpenVAS + ticket de verificación de corrección |
| **Resultado** | Conforme |
| **Estado** | Vigente |

## 4. Qué es evidencia y qué no

**Sí es evidencia:** reporte fechado de escaneo, captura de configuración de firewall, log del SIEM, ticket cerrado, acta de revisión, prueba de restauración, resultado de la revisión de accesos.

**No es evidencia:** "está implementado", "lo vimos funcionar una vez", un archivo sin fecha, una captura sin sistema/versión, un reporte de alguien que no tiene el rol.

> Regla de oro: **la evidencia debe permitir a un tercero (auditor) reconstruir el hecho** con fecha, alcance, herramienta y resultado.

## 5. Los controles se relacionan con las matrices

En el kit, la trazabilidad completa es:

- **Matriz de aplicabilidad** (`ID-05` / `MATRIZ-001`): qué control ISO/BCU aplica a qué área.
- **Política** (template ISACA o documento de `02-ENTREGABLES`): declara el *qué*.
- **Proceso** (VPOL-03): define el *cómo*.
- **Control + evidencia** (EV-01…05, BCU-05): demuestra el *cumplimiento*.
- **Tablero / KPIs** (actividad 43 del curso RSI): muestra la *efectividad* en el tiempo.

## 6. Métricas de controles

| Indicador | Fórmula / criterio |
|---|---|
| % controles vigentes | Controles con evidencia reciente ÷ total aplicable |
| % vulnerabilidades corregidas a tiempo | Corregidas dentro del plazo ÷ total detectadas |
| Tiempo medio de corrección | Suma de días ÷ nº de vulnerabilidades |
| % excepciones aceptadas | Excepciones ÷ total hallazgos |

> **Recuerde:** una política sin proceso es una intención; un proceso sin control es una rutina; un control sin evidencia es una afirmación. El SGSI se sostiene sobre la **triada política + proceso + control/evidencia**.
