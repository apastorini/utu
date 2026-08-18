# VPOL-07 · Artificial Intelligence (AI) Acceptable Use Policy

> **Función del MCU 5.0:** Gobernar (GV.OR — políticas; GV.RM — gestión de riesgos) · Proteger (PR.AC, PR.DS — datos)
> **ISO/IEC 27001:** A.5.9 (activos) · A.8.2 (clasificación) · A.8.11 (ocultamiento de datos) · A.8.12 (prevención de fuga)
> **BCU:** EMG — gobierno y control de la información; gestión de riesgos de nuevos canales/tecnologías
> **URCDP:** Ley 18.331 — principios de finalidad, minimización, consentimiento y derecho de acceso/oposición en tratamientos automatizados
> **Nivel del curso:** 🟡 Practicar → 🟠 Avanzar

---

### ENCABEZADO
| **Campo** | **Valor** |
|---|---|
| **Código** | VPOL-07 |
| **Título** | Artificial Intelligence (AI) Acceptable Use |
| **Versión** | 1.0 |
| **Estado** | [Borrador / En revisión / Aprobado] |
| **Fecha de aprobación** | [COMPLETAR] |
| **Elaborado por** | RSI + DPD |
| **Revisado por** | Comité de Seguridad · Comité de Datos |
| **Aprobado por** | Comité de Seguridad de la Información |
| **Clasificación** | Uso interno |
| **Próxima revisión** | [Fecha, máx. 6 meses, dado el ritmo del cambio] |

### 1. Objetivo
Establecer las reglas para el **uso de herramientas de Inteligencia Artificial (IA) generativa y asistentes de IA** en el Banco, maximizando la productividad y **evitando la fuga de información**, los sesgos, las respuestas alucinadas y el incumplimiento normativo.

### 2. Alcance
Aplica a todo el personal que use IA en el marco laboral: asistentes de código (ej. herramientas de IA para desarrollo), chatbots, generadores de texto/imagen, herramientas de análisis, **incluidas las usadas en proyectos del SGSI (ej. agentes de IA para el curso)**. Incluye IA alojada en la nube (SaaS) y modelos desplegados en infraestructura del Banco.

### 3. Clasificación del uso según el riesgo de la información
| Nivel de datos | ¿Se permite ingresar en IA externa? |
|---|---|
| Público | Sí, con normalidad |
| Uso interno | Solo con herramientas **aprobadas** por la Div. TI |
| Confidencial (clientes, datos personales, estratégicos) | **No** salvo autorización expresa del RSI con herramienta aprobada |
| Muy confidencial (credenciales, claves, datos biométricos) | **Prohibido siempre** en herramientas externas |

### 4. Reglas obligatorias
- **No ingresar** datos personales de clientes, información bancaria de personas, claves, tokens o secretos en herramientas de IA externas.
- Usar **solo herramientas autorizadas** por la Div. TI; está prohibido registrarse con cuentas personales en herramientas de trabajo.
- Todo resultado de IA se **revisa manualmente**: puede ser incorrecto o alucinado.
- El código generado por IA debe pasar el **proceso de revisión y escaneo de seguridad** (SDLC, PR-07).
- Las decisiones que afecten derechos de personas **no se pueden delegar en IA** sin control humano (principio de supervisión, en línea con la regulación emergente de IA y la Ley 18.331).
- **Declarar el uso de IA** en informes, productos y entregables cuando sea materialmente relevante.

### 5. Riesgos a mitigar
- **Fuga de información** (prompt en herramientas no controladas).
- **Alucinaciones** (datos inventados en informes, contratos, análisis).
- **Sesgo algorítmico** (resultados discriminatorios).
- **Propiedad intelectual** (contenidos generados sin licencia o con derechos de terceros).
- **Envenenamiento de datos / ataques prompt injection** en asistentes conectados a sistemas del Banco.

### 6. Cumplimiento
El incumplimiento de la regla de **no ingreso de datos confidenciales** se trata como incidente de seguridad (fuga potencial) y puede dar lugar a medidas disciplinarias. El DPD evalúa la obligación de **notificación de vulneración de datos personales** a la URCDP si corresponde (art. 27-bis Ley 18.331).

### 7. Revisión
Dado el dinamismo de la IA, esta política se revisa **cada 6 meses** o ante nuevas herramientas/normas nacionales o internacionales sobre IA.

### Evidencia del kit
| Evidencia | Documento canónico |
|---|---|
| Registro de herramientas de IA aprobadas | GV-04 (inventario de sistemas) |
| Capacitación sobre uso de IA | PR-02 |
| Procedimiento de revisión de código generado | PR-07 (SDLC) |
| Análisis de riesgos del proyecto | GV-03, ID-02 |
