# AISEC-10 · Plan de capacitación para 300 funcionarios

> **Función del MCU 5.0:** Este módulo implementa la concienciación del personal (PR.AT) y la gobernanza (GV) del uso de IA a escala: 300 funcionarios deben saber usar la herramienta oficial y respetar las reglas de datos.
> **ISO/IEC 27001:** Concienciación y formación (A.6.3): el personal debe estar formado y registrar la formación recibida.
> **BCU:** La formación del personal en riesgos de TIC es parte de los EMG y del RNRCSF.
> **URCDP:** La capacitación en protección de datos (incluida la IA) es parte de la responsabilidad proactiva (Ley 19.670).
> **Nivel del curso:** 🟡 Practicar

---

## 1. El desafío: 300 funcionarios, distintos perfiles

La capacitación no puede ser una sola charla. Los 300 funcionarios se dividen en grupos con necesidades distintas:

| Grupo | Tamaño aprox. | Necesidad de capacitación |
|---|---|---|
| Oficina y administrativos | ~200 | Usar BigPickle para correos, resúmenes y consultas; reglas de datos (AISEC-06) |
| Atención al cliente | ~40 | Respuestas y guiones seguros, sin datos de clientes |
| Desarrollo / TI | ~30 | OpenCode, RAG, implementación (AISEC-08) |
| Riesgo, cumplimiento, legales, RRHH | ~20 | EIPD, política, casos sensibles (AISEC-02/09) |
| Dirección | ~10 | Gobierno, indicadores, aprobación de la política |

---

## 2. Los objetivos de la capacitación

1. Que todos **sepan usar** la herramienta oficial (BigPickle y la propia de su perfil).
2. Que todos **sepan qué datos no entran** al chat (reglas de oro).
3. Que nadie **sienta la tentación** de usar herramientas externas (porque la oficial funciona bien).
4. Que todos **revisen** los resultados (alucinaciones).
5. Que el Banco **registre** la capacitación como evidencia.

---

## 3. Estrategia de adopción: "iluminar el camino, no apagar la luz"

El mayor riesgo de fuga viene de los funcionarios que usan IA personal porque **no saben que existe una oficial** o porque la oficial **les parece difícil**. La estrategia:

1. **Comunicación clara**: anuncio de dirección explicando por qué existe la herramienta oficial y por qué no se usan cuentas personales.
2. **Herramienta sencilla**: BigPickle en español, sin tecnicismos, lista para el primer uso en 5 minutos.
3. **Canal de ayuda**: un grupo/chat interno de soporte donde preguntar sin vergüenza.
4. **Ejemplos reales del propio trabajo**: cada área practica con sus casos (correos, resúmenes, código).
5. **Reconocimiento**: destacar buenos usos seguros (no castigar el error honesto, sí investigar la fuga silenciosa).
6. **Feedback**: encuestas de satisfacción y mejoras mensuales de la herramienta.

---

## 4. Cronograma sugerido (8 semanas)

| Semana | Actividad | Responsable |
|---|---|---|
| 1 | Anuncio de dirección + publicación de la política | Dirección |
| 2 | Formación general (módulos 01, 02, 03, 06, 07) para todos | RSI + RRHH |
| 3 | Práctica guiada con BigPickle (grupos de 30) | TI / formadores |
| 4 | Formación por perfil (desarrollo con OpenCode, atención, etc.) | TI |
| 5 | Formación de RSI/TI (módulos 04, 05, 08, 09) | RSI / externos |
| 6 | Simulacros y ejercicios (clasificar datos, detectar intentos de fuga) | RSI |
| 7 | Evaluación y encuestas | RRHH |
| 8 | Informe de resultados a dirección + ajustes | RSI |

---

## 5. Materiales de la capacitación (para cada participante)

| Material | Contenido |
|---|---|
| Guía rápida de 1 página | Reglas de oro (AISEC-06) + cómo abrir BigPickle |
| Manual del módulo 07 | Plantillas de prompts por perfil |
| Video de 10 minutos | Cómo funciona la IA del Banco y por qué no se usan cuentas externas |
| Postér de escritorio | Tabla 🟢/🟡/🔴 de datos |
| Tarjeta de incidentes | Qué hacer si detecta un uso indebido o un hallazgo |
| Planilla de firma | Registro de que recibió y comprendió la política |

---

## 6. Registro de capacitación (evidencia)

Cada participante firma el registro donde consta:

- Fecha de la capacitación.
- Módulos recibidos.
- Comprensión de las reglas de datos (evaluación corta).
- Aceptación de la política de uso aceptable de IA.

Este registro es evidencia de:
- A.6.3 (ISO 27001) — formación del personal.
- PR.AT (MCU 5.0) — concienciación.
- Ley 19.670 — responsabilidad proactiva.
- EMG / RNRCSF — gestión del riesgo de TIC.

---

## 7. La evaluación: ¿la gente entendió?

| Pregunta de evaluación | Respuesta correcta esperada |
|---|---|
| ¿Puedo pegar la cédula de un cliente para que la IA redacte el correo? | No |
| ¿Qué hago si necesito un ejemplo con datos? | Anonimizar o preguntar al DPD |
| ¿Puedo usar ChatGPT personal si no tengo tiempo? | No: usar la herramienta oficial o pedir ayuda |
| ¿La IA me dice siempre la verdad? | No: revisar siempre (alucinación) |
| ¿A quién aviso si veo un uso indebido? | RSI / DPD / jefe (según procedimiento) |

---

## 8. Cómo mantener el hábito (después de la semana 8)

- **Recordatorios mensuales** (ejemplo: "recuerde: los datos de clientes no entran por chat").
- **Píldoras de 5 minutos** en reuniones de área.
- **Casos reales internos** contados de forma anónima.
- **Mejoras mensuales** de la herramienta según feedback.
- **Auditoría periódica** de uso y reporte de indicadores a dirección.

---

## 9. Conclusión del módulo

- 300 funcionarios requieren una capacitación **por perfiles, escalonada y con registro**.
- La mejor protección contra la fuga es una **herramienta oficial que funcione bien** + reglas claras + apoyo constante.
- La capacitación queda **registrada como evidencia** ante URCDP, BCU y Agesic.
- El mensaje central: **"La IA se usa, se usa bien, y se usa con la herramienta del Banco."**

> **Ejercicio (RRHH/RSI):** Adapte el cronograma de 8 semanas a su institución, defina los grupos y las personas responsables, y prepare la planilla de firma de capacitación con los campos del punto 6.
