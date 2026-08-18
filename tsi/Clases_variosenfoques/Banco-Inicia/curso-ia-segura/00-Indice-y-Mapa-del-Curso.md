# AISEC-00 · Índice y Mapa del Curso

> **Función del MCU 5.0:** Este curso ejecuta en la práctica las funciones Proteger (PR), Detectar (DE) y Responder (RS) del Marco de Ciberseguridad de Agesic 5.0 aplicadas al uso de inteligencia artificial generativa: sin controles claros sobre qué datos ingresan a una herramienta de IA, dónde se procesan y quién revisa los resultados, no hay uso seguro ni auditable.
> **ISO/IEC 27001:** El curso se vincula a los controles del Anexo A sobre gestión de activos (A.5.9), control de acceso (A.5.15), seguridad de las comunicaciones (A.8), protección contra fugas (A.8.12 prevención de fuga de datos), gestión de incidentes (A.5.24) y cumplimiento (A.5.31/A.5.34). Complementa la **ISO/IEC 42001** (sistema de gestión de la IA) como referencia de gobernanza de sistemas de IA.
> **BCU:** El uso de IA debe quedar documentado en los Estándares Mínimos de Gestión (EMG) y en el RNRCSF: qué herramientas están autorizadas, quién las usa, qué datos pueden recibir y cómo se audita.
> **URCDP:** Este es el corazón normativo del curso: la Ley 18.331 y su reglamentación (Decreto 414/009, Decreto 64/020), la Ley 19.670, el Decreto 66/025 y los requisitos PD.1-PD.8 del MCU 5.0 prohíben tratar datos personales con herramientas que no ofrezcan garantías de seguridad, trazabilidad y minimización.
> **Decreto 66/025:** Obliga al RSI a conocer qué herramientas de IA se usan en la institución, qué datos procesan y a reportar incidentes asociados a ellas al CERTuy cuando corresponda.
> **Nivel del curso:** 🟢 Descubrir · 🟡 Practicar · 🔴 Dominar

---

## 1. Presentación del curso

Bienvenido al curso **"Inteligencia artificial y ciberseguridad: usar la IA bien, sin filtrar nada"**. Vive en la carpeta `curso-ia-segura` y forma parte del kit **Banco-Inicia**.

La premisa de este curso es honesta y realista: **la gente va a usar IA**. Los 300 funcionarios del Banco van a querer escribir correos más rápido, resumir documentos, generar código, analizar reportes y pedir ideas. Si la institución no ofrece una herramienta segura, el personal **de todas formas la va a buscar** — y ahí es donde aparece el riesgo: cuentas personales de ChatGPT, copiar y pegar datos de clientes en sitios web sin control, subir expedientes completos a servicios extranjeros de los que no tenemos ninguna garantía.

Por eso este curso no intenta prohibir la IA. Intenta hacer cuatro cosas:

1. **Explicar qué es realmente** un modelo de lenguaje (un LLM): cómo funciona por dentro, de dónde viene su "saber" y por qué puede equivocarse.
2. **Mostrar las herramientas seguras** que el Banco pone a disposición (agentes de código como OpenCode, interfaces amigables como BigPickle, modelos locales con Ollama y servidores de inferencia como vLLM) y cómo usarlas **sin fuga de información**.
3. **Explicar la ley**: qué dice la normativa uruguaya sobre tratar datos con IA, y qué pasa si copiamos datos de clientes a una herramienta no autorizada.
4. **Hacer la adopción amigable**: guías por perfil (mails, consultas, programación, documentación, seguridad, otros), plantillas de prompts seguros, y un plan de capacitación para 300 funcionarios que evite la tentación de usar herramientas externas.

La idea central es simple: **la IA no es el problema; la IA sin controles es el problema**. Herramienta segura + dato clasificado + revisión humana + evidencia = IA que ayuda. Herramienta anónima + dato de cliente + nadie revisa = incidente de URCDP.

---

## 2. Para quién es este curso

| Perfil | Por qué le sirve |
|---|---|
| Todos los funcionarios (300 personas) | Aprender a usar la herramienta oficial de IA del Banco sin fugar datos, con ejemplos de su propio trabajo diario. |
| Responsables de Seguridad de la Información (RSI) | Conocer los riesgos reales de los LLM (fuga, prompt injection, alucinaciones), cómo controlarlos y cómo demostrar cumplimiento ante Agesic, BCU y URCDP. |
| Personal de TI / Desarrollo | Configurar las herramientas (Ollama, vLLM, OpenCode), implementar el RAG seguro y mantener la evidencia técnica. |
| Oficiales y personal administrativo | Saber qué datos sí y qué datos no pueden pegar en una IA, y cómo redactar prompts seguros. |
| Personal de riesgo y cumplimiento | Entender el marco normativo (Ley 18.331, MCU 5.0 PD/CN, Ley 20.212 art. 74) y las excepciones autorizadas. |

### Qué vas a saber al terminar

- Qué es un LLM, por qué puede "inventar" y por qué lo que usted escribe **queda registrado**.
- Cuáles son las herramientas oficiales del Banco y cuáles **no se pueden usar** (cuentas personales en internet).
- Cómo funciona un **RAG** y por qué permite consultar los documentos del Banco sin entrenar a nadie con ellos.
- Qué dice la ley uruguaya sobre IA y datos personales, y qué pasa si la incumplimos.
- Cómo redactar prompts seguros para correos, consultas, código, documentos y seguridad.
- Qué debe hacer un RSI para auditar el uso de IA y presentar evidencia.
- El plan para que 300 funcionarios adopten la IA segura sin miedo y sin atajos.

---

## 3. Los 15 módulos del curso

El curso tiene **15 módulos**, numerados de **AISEC-00** a **AISEC-14**. Esta es la tabla general:

| Módulo | Tema | Nivel | Plantillas / documentos del kit relacionados |
|---|---|---|---|
| AISEC-00 | Índice y mapa del curso | 🟢 | Todos (es la puerta de entrada) |
| AISEC-01 | ¿Qué es la IA generativa y qué es un LLM? | 🟢 | VPOL-07 (templates-ISACA-02 AI Acceptable Use) |
| AISEC-02 | Marco normativo uruguayo de IA y datos personales | 🟡 | MATRIZ-BCU-EMG, URCDP-01, PD.1-PD.8, CN.1-CN.3 |
| AISEC-03 | Cómo funcionan OpenCode, BigPickle, Ollama y vLLM | 🟡 | PR-06, ID-01, GV-02 |
| AISEC-04 | RAG: consultar los documentos del Banco sin fugar nada | 🟡→🔴 | PR-07, URCDP-05, templates-ISACA-07 |
| AISEC-05 | Riesgos reales: fuga, prompt injection, alucinaciones y shadow IA | 🔴 | DE-01, DE-03, RS-02, templates-ISACA-09 |
| AISEC-06 | Reglas de oro: qué datos sí, qué datos no | 🟢 | templates-ISACA-07, URCDP-04, VPOL-07 |
| AISEC-07 | Guía de prompts seguros por perfil | 🟢 | Todas las plantillas de uso diario |
| AISEC-08 | Guía técnica para TI y RSI: implementación segura | 🔴 | PR-06, ID-04, DE-02, BCU-03, URCDP-01 |
| AISEC-09 | Gobierno y auditoría del uso de IA | 🔴 | GV-01, GV-02, GV-03, EV-01 a EV-05, MATRIZ-BCU-EMG |
| AISEC-10 | Plan de capacitación para 300 funcionarios | 🟡 | 14-Plan-Adopcion-Correspondencia-Final (rsi-tools) |
| AISEC-11 | Preguntas frecuentes, mitos y casos reales | 🟢 | Todas las anteriores |
| AISEC-12 | Correspondencia normativa y checklist final | 🔴 | MATRIZ-BCU-EMG, EV-01 a EV-05 |
| AISEC-13 | Modelos en datacenter sin internet: versionado, catálogo y actualización | 🔴 | GV-02, ID-01, BCU-03, URCDP-01 |
| AISEC-14 | Cómo funciona un modelo por dentro: memoria, telemetría, salida a internet | 🟢→🔴 | templates-ISACA-07, templates-ISACA-09, URCDP-05 |

---

## 4. Ruta de aprendizaje recomendada

Se recomienda este camino, que va de lo conceptual a lo práctico y de lo práctico a lo auditable:

1. **AISEC-00** (este módulo): el mapa del curso.
2. **AISEC-01**: qué es un LLM (base conceptual para entender los riesgos).
3. **AISEC-02**: marco normativo (por qué el dato no se pega en cualquier lado).
4. **AISEC-03**: las herramientas oficiales y cómo usarlas.
5. **AISEC-04**: RAG (la forma segura de consultar los documentos del Banco).
6. **AISEC-05**: riesgos reales (fuga, prompt injection, alucinaciones).
7. **AISEC-06**: reglas de oro (qué datos sí / qué datos no).
8. **AISEC-07**: guía de prompts por perfil (práctica diaria).
9. **AISEC-08** (solo TI/RSI): implementación técnica segura.
10. **AISEC-09** (solo RSI): gobierno y auditoría.
11. **AISEC-10** (todos): plan de adopción para 300 funcionarios.
12. **AISEC-11** y **AISEC-12**: casos, FAQ y checklist final.
13. **AISEC-13** (solo TI/RSI): versionado y actualización de modelos sin internet.
14. **AISEC-14** (todos): memoria, telemetría y qué sale a internet.

> **Nota para el RSI:** los módulos AISEC-02, AISEC-05, AISEC-08, AISEC-09, AISEC-13 y AISEC-14 son los que convierten este curso en evidencia auditable ante Agesic, BCU y URCDP.

---

## 5. Cómo usar este curso en el kit Banco-Inicia

1. **Aprendé el concepto** leyendo el módulo (con las analogías y ejemplos).
2. **Abrí la plantilla** relacionada (por ejemplo `templates-ISACA\02-AI-Acceptable-Use.md`).
3. **Completala con el caso Banco** usando lo aprendido.
4. **Guardala en la estructura del SGSI** y **seguila en la planificación**.
5. **Dejá evidencia** (política firmada, registros de uso, logs, planillas de capacitación) para responder ante URCDP, BCU y Agesic.

La regla de oro de todo el curso, en una frase:

> **En el Banco, la IA se usa con la herramienta oficial, con datos que la política autoriza, y siempre con revisión humana del resultado. Lo que no está autorizado, no se hace — ni "por única vez".**
