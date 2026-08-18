# POL-17 · Política de Uso Aceptable de Inteligencia Artificial

> **Función del MCU 5.0:** Gobernar (GV.OR — políticas; GV.RM — riesgos) · Proteger (PR.AC, PR.DS — datos)
> **ISO/IEC 27001:** A.5.9 (activos) · A.8.2 (clasificación) · A.8.12 (prevención de fuga) · ISO/IEC 42001 (gobernanza de IA) como referencia
> **BCU:** EMG — gobierno y control de la información; riesgos de nuevas tecnologías
> **URCDP:** Ley 18.331 — finalidad, minimización, consentimiento y derechos en tratamientos automatizados; PD.1-PD.8 del MCU 5.0
> **Nivel del curso:** 🟡 Practicar → 🔴 Dominar

---

### ENCABEZADO
| **Campo** | **Valor** |
|---|---|
| **Código** | POL-17 |
| **Título** | Uso Aceptable de Inteligencia Artificial |
| **Versión** | 1.0 |
| **Estado** | [Borrador / En revisión / Aprobado] |
| **Fecha de aprobación** | [COMPLETAR] |
| **Elaborado por** | RSI + DPD |
| **Revisado por** | Comité de Seguridad · Comité de Datos |
| **Aprobado por** | Comité de Seguridad de la Información |
| **Clasificación** | Uso interno |
| **Próxima revisión** | [Fecha, máx. 6 meses] |

### 1. Objetivo
Establecer las reglas para el **uso de herramientas de IA** en el Banco, maximizando la productividad y **evitando la fuga de información**, las alucinaciones, los sesgos y el incumplimiento normativo (ver curso `curso-ia-segura`).

### 2. Alcance
Aplica a todo el personal que use IA en el marco laboral: asistentes de código (OpenCode), interfaces en español (BigPickle), modelos locales (Ollama/vLLM), herramientas de nube contratadas y cualquier otra herramienta de IA.

### 3. Clasificación del uso según el riesgo de la información
| Nivel de datos | ¿Se permite ingresar en IA externa? |
|---|---|
| Público | Sí, con normalidad |
| Uso interno | Solo con herramientas **aprobadas** por la Div. TI |
| Confidencial (clientes, datos personales, estratégicos) | **No** salvo autorización expresa del RSI con herramienta aprobada |
| Muy confidencial (credenciales, claves, datos biométricos) | **Prohibido siempre** en herramientas externas |

### 4. Reglas obligatorias
- Usar **solo herramientas autorizadas** (registro de herramientas de IA); prohibido usar cuentas personales para trabajo.
- **No ingresar** datos personales de clientes, información bancaria de personas, claves o secretos en IA externa.
- Si se necesitan datos, **anonimizar** primero; ante la duda, consultar al DPD.
- Todo resultado de IA se **revisa manualmente** (puede ser incorrecto o alucinado).
- El código generado por IA pasa el **proceso de revisión y escaneo** (POL-15, SDLC).
- Las decisiones que afecten derechos de personas **no se delegan en IA** sin control humano.
- **Declarar el uso de IA** en informes y entregables cuando sea materialmente relevante.
- Los **modelos** se gestionan con versionado, verificación y prueba (curso AISEC-13/AISEC-14).

### 5. Riesgos a mitigar
- Fuga de información (prompt en herramientas no controladas).
- Alucinaciones (datos inventados en informes, contratos, análisis).
- Sesgo algorítmico y decisiones sin supervisión.
- Prompt injection y envenenamiento de datos en asistentes conectados a sistemas.
- Propiedad intelectual de contenidos generados.

### 6. Cumplimiento
El incumplimiento de la regla de **no ingreso de datos confidenciales** se trata como incidente de seguridad y puede requerir **notificación a la URCDP** (Decreto 64/020, PRO-05). El DPD evalúa la obligación de notificar.

### 7. Revisión
Dado el dinamismo de la IA, se revisa **cada 6 meses** o ante nuevas herramientas o normas sobre IA.

### Evidencia del kit
| Evidencia | Documento canónico |
|---|---|
| Registro de herramientas de IA aprobadas | GV-04, curso AISEC-09 |
| Capacitación sobre IA segura | PR-02, PRO-12, curso AISEC-10 |
| Procedimiento de revisión de código generado | POL-15 |
| Registro de modelos (versiones, hashes) | curso AISEC-13 |
| Análisis de riesgos del uso de IA | ID-02, GV-03 |
