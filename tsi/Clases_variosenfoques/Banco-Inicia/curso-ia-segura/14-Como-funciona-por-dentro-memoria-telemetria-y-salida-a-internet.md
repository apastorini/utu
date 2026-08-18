# AISEC-14 · Cómo funciona un modelo "por dentro": ¿manda datos a otro lado? ¿recuerda? ¿puede salir información confidencial a internet?

> **Función del MCU 5.0:** Este módulo responde las dudas más frecuentes sobre el funcionamiento interno de los LLM para poder protegerlos (PR), detectar fugas (DE) y demostrar cumplimiento (CN/PD).
> **ISO/IEC 27001:** Confidencialidad de la información (A.8), gestión de logs (A.8.15-A.8.16), control de comunicaciones (A.8.20-A.8.21) y prevención de fuga de datos (A.8.12).
> **BCU:** Saber exactamente qué hace una herramienta con los datos es parte de la gestión de riesgo operacional y de los EMG.
> **URCDP:** La respuesta honesta a "¿qué pasa con mis datos?" es la base del deber de información (Ley 18.331) y de la seguridad (PD.5).
> **Nivel del curso:** 🟢 Descubrir (público general) · 🔴 Dominar (secciones técnicas)

---

## 1. La pregunta más importante: ¿el modelo manda información a otro lado?

La respuesta honesta es: **depende de cómo esté desplegado y de cuál herramienta esté usando.**

Imaginemos tres "casas" donde puede vivir un modelo:

| ¿Dónde corre el modelo? | ¿Manda datos afuera? | Ejemplo |
|---|---|---|
| **Casa A · En la infraestructura del Banco (Ollama/vLLM local)** | **No.** El modelo corre en servidores propios; el texto entra y sale sin cruzar la frontera del Banco | Modelo instalado en el datacenter local, sin salida a internet |
| **Casa B · En una nube contratada por el Banco con garantías** | **Sí, pero bajo contrato**: los datos van a los servidores del proveedor, con contrato de protección de datos, residencia definida y prohibición de entrenar con ellos | API de un proveedor contratado institucionalmente |
| **Casa C · Una cuenta personal gratis en internet** | **Sí, sin ningún control**: los datos salen al proveedor extranjero sin contrato, pueden guardarse, usarse para entrenar y reproducirse | ChatGPT, Gemini, Claude o Copilot con cuenta personal |

**Regla del Banco: solo Casa A y Casa B están autorizadas. Casa C jamás recibe datos del Banco.**

### ¿Cómo saber en qué "casa" está la herramienta?

1. **Pregunte**: ¿dónde corre el modelo? ¿Quién tiene el contrato?
2. **Revise el registro de herramientas autorizadas** del Banco (módulo 09): si la herramienta no está ahí, no se usa.
3. **Verifique con TI**: el RSI tiene documentado dónde se procesa cada cosa.

---

## 2. ¿El modelo "recuerda"? La verdad sobre la memoria

Esta es una de las confusiones más comunes. Hay que separar **tres memorias distintas**:

### Memoria 1 · El conocimiento entrenado (lo que "aprendió" al fabricarse)

Cuando el modelo se entrenó, "aprendió" patrones de textos públicos. Ese conocimiento **queda fijo en los archivos del modelo** (los parámetros). El modelo no lo "recuerda" de usted: ya venía de fábrica. Tiene una **fecha de corte**: no sabe nada posterior a su entrenamiento.

### Memoria 2 · El contexto de la conversación (lo que "tiene a la vista ahora")

Dentro de una misma conversación, el modelo "ve" lo que se escribió antes en esa sesión, **hasta el límite de la ventana de contexto** (módulo 01). Es como la mesa del ayudante: tiene a la vista los papeles de la conversación actual. **Si cierra la sesión o inicia otra, ese contexto desaparece** (salvo que la herramienta guarde el historial).

### Memoria 3 · Los registros del sistema (logs) — la clave para la seguridad

Esto es lo que más importa: **casi todas las herramientas guardan registros (logs) de las consultas**: quién preguntó, cuándo, qué se envió y qué se respondió. Esos registros:

- Sirven para **auditoría** (por eso el Banco los exige).
- **Pueden ser accesibles al administrador** de la herramienta (en el Banco: el RSI/TI).
- En una herramienta personal, esos registros están **en manos del proveedor externo** (por eso Casa C es peligrosa).

### ¿El modelo "aprende de mí" a largo plazo?

**No, no de forma automática.** Un LLM normal no se va "mejorando solo" con lo que usted le escribe. Solo aprende si lo **reentrenan** con datos (y eso es caro y controlado). 

**PERO** (y aquí está el peligro de Casa C): las empresas de IA **sí pueden usar lo que usted escribe para entrenar sus futuros modelos**, si usted no lo desactivó o si el servicio lo permite por defecto. Por eso:

> **Regla del Banco:** en las herramientas oficiales, el uso **no se usa para entrenar modelos** (configuración y contrato lo garantizan). En las cuentas personales, **su texto puede quedar guardado y ser usado para entrenar modelos ajenos.**

---

## 3. ¿Qué pasa exactamente cuando escribo en BigPickle?

Flujo completo, paso a paso:

1. Usted escribe el texto (prompt) en BigPickle.
2. El texto viaja **dentro de la red del Banco** hasta el motor (vLLM → Ollama local, o nube contratada Casa B).
3. El modelo procesa y genera la respuesta.
4. La respuesta vuelve a BigPickle.
5. El sistema guarda un **registro** (usuario, fecha, resumen) para auditoría.

**En ningún paso los datos salen del perímetro del Banco** (en Casa A). Por eso es seguro. La diferencia con una cuenta personal es total: **los datos no cruzan la frontera del Banco, no se usan para entrenar y quedan registrados para auditoría interna.**

---

## 4. Telemetría: ¿la herramienta "llama a casa"?

Algunas herramientas envían **telemetría** (datos técnicos de uso: versión, errores, métricas) a sus fabricantes, aunque el modelo corra localmente. Esto es distinto del contenido: la telemetría suele ser **técnica**, no el texto de los usuarios. Pero debe conocerse y controlarse.

| Herramienta | Comportamiento típico | Qué hacer en el Banco |
|---|---|---|
| **Ollama** | Corre 100% local; la telemetría se puede desactivar con la variable de entorno `OLLAMA_DEBUG=false` o deshabilitando actualizaciones automáticas | Desplegar **sin salida a internet** y con actualizaciones manuales controladas (módulo 13) |
| **vLLM** | Servidor de inferencia que no llama a casa por diseño | Igual, monitorear salidas |
| **OpenCode** | El agente de código usa el modelo que se le configure; verificar qué endpoint usa (local o contratado) | Configurar apuntando al endpoint interno del Banco |
| **Nube contratada (Casa B)** | Envía el texto al proveedor **por contrato**, con garantías documentadas | Tener el contrato, la evaluación de impacto (PD.7) y el registro de tratamiento |

### Cómo verificarlo en la práctica (nivel 🔴)

1. **En el firewall/DLP**: revisar qué dominios tocan las herramientas (módulo 08): `logs de tráfico`.
2. **Con red bloqueada**: probar la herramienta con el datacenter sin salida y confirmar que sigue funcionando (si funciona, no depende de internet).
3. **Con netstat en la estación**: `netstat -ano` muestra las conexiones activas de cada proceso; comprobar si hay conexiones externas inesperadas.
4. **Leer la configuración**: `OLLAMA_HOST`, variables de telemetría, endpoints configurados.

---

## 5. ¿Es viable que salga "salida confidencial" a internet? La respuesta clara

La pregunta exacta del RSI es: **¿puede una respuesta que contiene información confidencial salir del Banco por internet?**

La respuesta: **depende de la clasificación del dato y de la autorización.** Regla de tres niveles:

| Tipo de salida | ¿Es viable? | Condición |
|---|---|---|
| **Respuesta sin datos personales ni confidencialidad** (textos genéricos, resúmenes de información pública) | ✅ Sí | Herramienta autorizada; idealmente local |
| **Respuesta con datos confidenciales internos** (informes de gestión, estrategia, código) | ⚠️ Solo bajo autorización formal | Casa A local, o Casa B contratada con garantías, EIPD aprobado y registro de tratamiento |
| **Respuesta con datos personales de clientes** | ❌ No, salvo proceso excepcional autorizado | Casa A local con base legal y minimización; nunca Casa C |

### El principio rector: clasificación primero

Antes de preguntar "¿puede salir?", pregunte **"¿qué es este dato?"** (módulo 06):

1. Si es **público o interno sin restricción** → puede procesarse en herramientas autorizadas, idealmente locales.
2. Si es **confidencial** → solo infraestructura local o nube contratada con garantías, y con registro.
3. Si es **personal de clientes** → solo con base legal, minimización, EIPD y herramienta que lo garantice. En la práctica: **Casa A local.**

> **La salida a internet no es buena ni mala en sí misma: es una decisión de riesgo.** El Banco decide quién puede salir, con qué datos y con qué garantías. Lo que nunca está bien es que un funcionario decida solo mandar datos confidenciales a una herramienta no autorizada.

### Ventajas y desventajas honestas de cada opción

| Opción | Ventaja | Desventaja |
|---|---|---|
| **Local (Casa A)** | Confidencialidad total, sin contrato, sin salida | Modelos menos potentes, requiere hardware, actualización manual (módulo 13) |
| **Nube contratada (Casa B)** | Modelos más potentes, cero mantenimiento de GPU | Datos salen del Banco (con contrato), dependencia del proveedor, requiere auditoría |
| **Cuenta personal (Casa C)** | Gratis y "fácil" | Fuga total, sin contrato, sin control, prohibida |

---

## 6. Mitos que este módulo aclara de una vez

| Mito | Verdad |
|---|---|
| "El modelo aprende de lo que le escribo" | No automáticamente; pero en cuentas personales su texto **puede usarse para entrenar** modelos ajenos |
| "Si borro la conversación, no queda nada" | Los **logs del sistema** pueden conservar registros; en cuentas personales, los guarda el proveedor |
| "Como corre local, no llama a casa" | En general sí (Ollama local no llama), pero hay que **verificar telemetría y salidas** con logs |
| "La nube contratada es igual que la cuenta personal" | **No**: la nube contratada tiene contrato, garantías, residencia y registro; la cuenta personal no tiene nada de eso |
| "Si la herramienta responde, significa que no salió nada" | Falso: una herramienta externa (Casa C) responde precisamente porque **envió el texto afuera** |

---

## 7. El cuaderno de "¿qué hace mi herramienta?" (para el RSI)

Para cada herramienta del Banco, documente y guarde como evidencia:

| Campo | Respuesta |
|---|---|
| ¿Dónde corre el modelo? | Local / nube contratada (detalle) |
| ¿Los datos salen del Banco? | Sí / No (detalle, con qué garantías) |
| ¿El texto se usa para entrenar? | Sí / No (cláusula del contrato o configuración) |
| ¿Guarda logs? ¿De qué? | Sí, metadatos / contenido (detalle) |
| ¿Tiene telemetría? ¿Se desactivó? | Sí / No (detalle) |
| ¿Quién puede ver los logs? | RSI, TI, administradores |
| ¿Está en el registro de herramientas autorizadas? | Sí / No |
| ¿Tiene EIPD aprobado (si trata datos personales)? | Sí / No |

Este cuaderno es parte del Documento de Seguridad y de la evidencia de gobierno (módulo 09).

---

## 8. Conclusión del módulo

- **¿Manda datos a otro lado?** Depende de la "casa": local no; nube contratada sí (con contrato); cuenta personal sí (sin control). Solo Casa A y B están autorizadas.
- **¿Recuerda?** Hay tres memorias: el conocimiento de fábrica (fijo), el contexto de la sesión (temporal) y los **logs** (permanentes, y en cuentas personales los controla el proveedor).
- **¿Puede salir información confidencial a internet?** Solo con autorización formal, con la herramienta y garantías correctas, y según la clasificación del dato.
- **¿Hay que revisar la telemetría?** Sí: un despliegue "local" se confirma verificando que no hay salidas, no solo por confiar en el nombre.
- **La herramienta oficial se eligió para que estas respuestas sean favorables**: datos adentro, uso no entrenado, logs auditables.

> **Ejercicio:** Complete el cuaderno del punto 7 para las herramientas oficiales de su institución. Luego, responda en una frase: ¿por qué una cuenta personal de una herramienta de IA nunca puede recibir datos del Banco? (Respuesta guía: porque el texto sale sin contrato, sin garantías, sin base legal y sin forma de responder a los derechos del titular.)
