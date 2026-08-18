# AISEC-01 · ¿Qué es la IA generativa y qué es un LLM?

> **Función del MCU 5.0:** Comprender el activo que estamos protegiendo (el modelo y los datos que recibe) es la base de la función Proteger (PR). No se puede proteger lo que no se entiende.
> **ISO/IEC 27001:** Los modelos de IA son activos de información. Se clasifican, se inventarían (A.5.9) y se controlan los datos que se les entregan (A.8.12 prevención de fuga de datos).
> **BCU:** Documentar qué es un LLM y cómo se usa permite describir el riesgo de TIC asociado a la IA en los EMG y el RNRCSF.
> **URCDP:** Entender que "todo lo que se escribe queda en el sistema" es la base para respetar la seguridad y confidencialidad exigidas por la Ley 18.331 y el Decreto 64/020.
> **Nivel del curso:** 🟢 Descubrir

---

## 1. La analogía del aprendiz

Imaginemos a un **aprendiz de oficina** que nunca vio un documento del Banco. Antes de empezar, le mostramos **millones de documentos de ejemplo de todo tipo** (correos, informes, códigos, noticias, libros) durante meses. El aprendiz no los memoriza: va aprendiendo patrones de cómo se escriben las frases, cómo se estructuran los correos, qué palabras suelen ir juntas.

Ese aprendiz, sin embargo, **no tiene memoria de los documentos que vio**. No puede repetirlos de memoria. Lo único que tiene es un "instinto" estadístico: si usted le dice "el saldo de la cuenta es...", él va a continuar con la palabra más probable que sigue.

Eso es un **LLM** (Large Language Model, Modelo de Lenguaje Grande): un programa que aprendió patrones del lenguaje a partir de muchísimo texto. **No piensa, no sabe, no recuerda: predice la siguiente palabra.**

---

## 2. Qué significa cada palabra de "LLM"

| Letra | Palabra | Qué significa en simple |
|---|---|---|
| L | Large (grande) | Tiene miles de millones de "conexiones" internas (parámetros). Eso le da riqueza de lenguaje. |
| L | Language (lenguaje) | Trabaja con texto: lee palabras y escribe palabras. |
| M | Model (modelo) | Es un programa matemático que "aprendió" patrones de lenguaje. |

### Cómo procesa un texto: los tokens

Un LLM no lee palabras completas como usted. Lee **trozos de palabras** llamados **tokens**. Por ejemplo, la frase "Buenos días" puede convertirse en tokens como `Buen` + `os` + ` días`. Eso le permite manejar cualquier palabra, incluso las que nunca vio, combinando piezas.

Dato importante para el usuario: **los LLM cobran y miden por tokens**, y lo que usted escribe y lo que el modelo responde se cuentan en tokens. Pero lo que más le importa a usted no es eso: es que **el contexto tiene un límite** (una "ventana de contexto").

### La ventana de contexto

El LLM solo puede "ver" una cantidad finita de texto por conversación. Es como un ayudante con una mesa chica: solo tiene a la vista lo que cabe en la mesa. Si usted pega un expediente de 400 páginas, **no cabe**. Por eso existen técnicas como el **RAG** (módulo AISEC-04) que eligen los pedazos relevantes y solo ponen esos en la mesa.

---

## 3. ¿De dónde viene el "saber" del modelo?

El modelo fue **entrenado** con enormes cantidades de texto de internet y de fuentes públicas, con una técnica que le enseña a completar textos. Tres consecuencias que debe conocer:

1. **El modelo no sabe su trabajo**: solo "completa texto probable". Por eso puede sonar muy seguro y estar equivocado.
2. **El modelo no se actualiza solo**: su conocimiento tiene una fecha de corte. La normativa uruguaya que cambió ayer **no la conoce**, salvo que se la demos en el contexto.
3. **El modelo no "recuerda" lo que usted le escribió antes**: si usted usa una herramienta **no autorizada** de internet, su texto puede ser usado para entrenar futuros modelos o quedar en los servidores de la empresa externa. **Eso es lo que prohibimos en el Banco.**

### Alucinaciones

Cuando el modelo inventa datos que parecen reales (un nombre de cliente que no existe, una fecha, una referencia normativa), se llama **alucinación**. Es el mayor peligro del uso de IA en un banco: **una respuesta bien redactada no es sinónimo de respuesta correcta**. La regla es simple:

> **Todo lo que produce la IA debe ser revisado por una persona antes de usarse. En el Banco, nadie firma ni envía ni ejecuta lo que genera la IA sin revisión humana.**

---

## 4. IA generativa: qué puede y qué no puede

| Puede | No puede |
|---|---|
| Redactar y mejorar textos (correos, informes, cartas) | Asegurar que lo que dice es 100% cierto |
| Resumir documentos largos | Conocer la normativa interna del Banco (salvo que se la demos) |
| Generar código y explicar errores | Ejecutar el código por usted en sistemas del Banco |
| Analizar reportes y detectar patrones | Sustituir la decisión humana (especialmente legal o crediticia) |
| Responder preguntas sobre documentos que le pasemos | Saber quién es un cliente o cuánto debe (salvo que se lo mostremos, y solo si está autorizado) |

---

## 5. Los tres peligros que debe recordar siempre

Antes de avanzar al módulo siguiente, deje grabados estos tres conceptos:

1. **Fuga de información**: si usted pega datos de clientes en una herramienta externa no autorizada, esos datos **salen del Banco** y el Banco ya no puede controlarlos. Eso viola la Ley 18.331 y puede terminar en una sanción de la URCDP y una multa del BCU.
2. **Alucinación**: el modelo inventa. Todo resultado requiere **revisión humana**.
3. **Prompt injection**: un documento malicioso (por ejemplo, un correo recibido o una web) puede intentar "secuestrar" la conversación y hacer que el modelo haga algo que no debe (módulo AISEC-05). Por eso, en el Banco **no se le pide a la IA que actúe sobre texto que no controlamos**.

---

## 6. Conclusión del módulo

- Un LLM es un programa que **predice palabras**, no una persona que sabe.
- Su "saber" viene de textos públicos pasados y **no conoce la interna del Banco**.
- Lo que usted escribe **queda registrado** en la herramienta; en una herramienta externa, fuera de control del Banco.
- La IA **alucina**: todo resultado se revisa antes de usarlo.
- En el Banco se usa la **herramienta oficial** y **nunca datos de clientes en herramientas externas**.

> **Ejercicio de auto-chequeo:** ¿Por qué pegar el padrón de un cliente en una página web de IA "gratis" es más grave que escribirlo en un papel que se destruye? Respuesta: porque el papel se destruye, pero el texto que usted pega en internet puede quedar guardado, usado para entrenar modelos y reproducido en otros países, sin que el Banco pueda recuperarlo ni demostrar que lo protegió (Ley 18.331, art. 9, deber de seguridad).
