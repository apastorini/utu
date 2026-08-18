# AISEC-07 · Guía de prompts seguros por perfil

> **Función del MCU 5.0:** Este módulo convierte las reglas de AISEC-06 en práctica diaria para los 300 funcionarios: cómo pedirle a la IA que ayude sin fugar datos y con resultados verificables (PR-AT, DE).
> **ISO/IEC 27001:** Uso aceptable de los activos (A.5.10-A.5.11) y concienciación del personal (A.6.3).
> **BCU:** El uso correcto y documentado de la IA por el personal es parte de la gestión del riesgo operacional.
> **URCDP:** Los prompts bien redactados respetan minimización y finalidad (PD.3, PD.5).
> **Nivel del curso:** 🟢 Descubrir

---

## 1. Las 5 partes de un buen prompt seguro

Un prompt (solicitud a la IA) bien redactado tiene 5 partes. Cuantas más use, mejor respuesta obtendrá:

1. **Rol**: "Actuá como un oficial de cobranzas..."
2. **Contexto** (sin datos personales): "En un banco uruguayo, con clientes minoristas..."
3. **Tarea**: "...redactá un correo formal para clientes con atraso de 90 días..."
4. **Formato**: "...de 120 palabras, tono firme pero respetuoso, sin amenazas."
5. **Regla de revisión**: "...y recordame qué debo verificar antes de enviar."

> **Regla de seguridad del prompt:** el prompt **nunca lleva datos personales**. Si necesita un ejemplo, anonimice (módulo 06).

---

## 2. Perfil 1 · Oficina y correspondencia (mails, cartas, comunicados)

### Lo que puede pedir
- Redactar y mejorar correos internos y externos (sin datos personales).
- Resumir y estructurar informes, actas, minutas.
- Mejorar redacción y tono de comunicados.
- Generar recordatorios y circulares internas.

### Ejemplo seguro

> **Prompt:** "Actuá como asistente de oficina de un banco uruguayo. Redactá un correo interno breve (80 palabras) que recuerde al personal la obligación de no compartir claves de acceso. Tono cordial e institucional. Al final, listá los 3 puntos que debo verificar antes de enviar."

### Lo que NO hace
- No pegar la lista de destinatarios ni sus correos personales.
- No mencionar deudas, saldos ni datos de clientes en el cuerpo.

---

## 3. Perfil 2 · Consultas y atención al cliente

### Lo que puede pedir
- Modelos de respuesta a consultas frecuentes (sin datos del cliente).
- Guiones de atención telefónica.
- Clasificar y priorizar tipos de consulta (de forma genérica).
- Redactar respuestas a reclamos (borradores anonimizados).

### Ejemplo seguro

> **Prompt:** "Actuá como asesor de atención al cliente de un banco. Redactá un borrador de respuesta a un reclamo por error en un cobro de comisión, con tono empático y formal. No incluyas nombres ni datos de clientes: usá el formato 'Estimado/a cliente'. Terminá con el compromiso de revisión en un plazo."

### Lo que NO hace
- No pegar el historial real de la consulta con datos del cliente.
- No pedirle a la IA que "decida" si el reclamo es válido (eso lo decide una persona con el sistema).

---

## 4. Perfil 3 · Programación y desarrollo (OpenCode)

### Lo que puede pedir
- Explicar qué hace un fragmento de código.
- Detectar bugs en el código del repositorio (entorno de desarrollo).
- Escribir pruebas unitarias.
- Refactorizar código respetando las convenciones del proyecto.
- Revisar seguridad de funciones (buscar inyección, accesos sin validar).

### Ejemplo de prompt (en OpenCode)

> "Analizá el archivo `validar_usuario.py`: buscá vulnerabilidades de inyección SQL y de control de acceso, explicá cada hallazgo y proponé una corrección. Mostrame el diff antes de aplicar cambios."

### Lo que NO hace
- No trabajar con datos reales de producción (usar datos de prueba/QA).
- No aceptar cambios sin revisar el diff.
- No autorizar ejecución de comandos en producción.

---

## 5. Perfil 4 · Documentación y procedimientos

### Lo que puede pedir
- Resumir políticas y procedimientos internos (desde el RAG autorizado).
- Explicar un procedimiento en lenguaje simple.
- Crear índices y ayudas memoria de documentos largos.
- Comparar versiones de documentos.

### Ejemplo con RAG

> "Resumí la política de protección de datos PD-01 en una página, en lenguaje simple para personal no técnico. Citá las secciones en las que te basás."

### Lo que NO hace
- No subir documentos no autorizados al RAG.
- No usar el resultado sin verificar las citas contra el documento original.

---

## 6. Perfil 5 · Seguridad y ciberseguridad

### Lo que puede pedir
- Redactar comunicados de concienciación.
- Preparar borradores de políticas y procedimientos (plantillas).
- Explicar conceptos técnicos (phishing, ransomware) en lenguaje simple.
- Redactar simulacros de phishing internos (genéricos, sin datos reales).
- Ayudar a redactar el reporte de un incidente (sin datos de clientes ni técnicas que convengan ocultar).

### Ejemplo seguro

> "Actuá como especialista en ciberseguridad de un banco uruguayo. Redactá una infografía simple (bajo el título 'Cómo detectar un phishing') con 5 señales de alerta y qué hacer. Sin datos internos."

### Lo que NO hace
- No copiar logs, credenciales ni datos de incidentes reales al chat.
- No revelar datos técnicos sensibles de la red del Banco.
- No usar la IA como "fuente normativa": verificar siempre contra la normativa oficial (AISEC-02).

---

## 7. Perfil 6 · Otros usos (riesgo, cumplimiento, legales, comunicación)

### Lo que puede pedir
- Borradores de informes de riesgo (sin datos personales).
- Estructura de matrices y presentaciones.
- Lluvia de ideas de mejora de procesos.
- Redacción de minutas de reuniones.
- Traducción y mejora de textos institucionales.

### Ejemplo seguro

> "Actuá como analista de cumplimiento de un banco uruguayo. Prepará el índice de un informe trimestral de gestión de riesgos de TIC según los dominios del MCU 5.0 (GV, ID, PR, DE, RS, RC)."

### Lo que NO hace
- No ingresar datos de clientes ni información reservada de auditoría.
- No usar la IA para "opiniones legales": el borrador lo revisa un profesional.

---

## 8. Plantillas de prompts listas para usar

### Correo interno (sin datos)
```
Actuá como [rol] de un banco uruguayo. Redactá un [tipo de texto] de
[extensión] sobre [tema], tono [tipo], dirigido a [audiencia].
Terminá listando qué debo verificar antes de enviar.
```

### Resumen de documento (RAG)
```
Resumí [documento] en [máximo de palabras] para [audiencia].
Basate solo en el documento y citá las secciones usadas.
Indicá qué información debería verificar contra la fuente.
```

### Mejora de redacción (sin datos)
```
Mejorá la redacción del siguiente texto sin cambiar el sentido y sin
agregar datos: [texto anonimizado].
```

### Explicación simple
```
Explicá [concepto] como si yo tuviera [nivel de conocimiento],
con una analogía de la vida diaria, en [extensión].
```

---

## 9. Errores comunes que se deben evitar

| Error | Por qué es un error | Solución |
|---|---|---|
| Pegar datos reales "para que quede más claro" | Fuga de datos | Anonimizar o quitar el dato |
| Aceptar la respuesta sin revisar | Alucinación | Verificar contra la fuente / sistema |
| Pedir decisiones (aprobar crédito, resolver reclamo) | La IA no decide | La persona decide con el sistema |
| Usar la IA como fuente normativa directa | Desactualización / invención | Verificar en la norma oficial |
| No pedir formato | Respuesta larga y desordenada | Especificar rol, extensión y tono |

---

## 10. Conclusión del módulo

- Un buen prompt tiene **rol, contexto, tarea, formato y regla de revisión**.
- Cada perfil (correo, consultas, programación, documentación, seguridad, otros) tiene su propia guía, pero la **misma regla de seguridad**: sin datos personales, con revisión humana.
- La IA **no decide ni opina legalmente**: redacta borradores que una persona revisa.
- Si el prompt que necesita llevar datos personales... **entonces ese uso requiere proceso autorizado y no se hace por chat** (AISEC-08/09).

> **Ejercicio:** Redacte un prompt para su primera tarea real de la semana usando las 5 partes y la plantilla de su perfil. Guárdelo en la planilla de capacitación (AISEC-10) como evidencia de su aprendizaje.
