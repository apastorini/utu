# AISEC-03 · Cómo funcionan OpenCode, BigPickle, Ollama y vLLM

> **Función del MCU 5.0:** Las herramientas de IA son activos del Banco. Conocer cómo funcionan permite protegerlas (PR), inventariarlas (ID) y demostrar su control ante auditorías (GV/CN).
> **ISO/IEC 27001:** Gestión de activos (A.5.9), control de acceso (A.5.15/A.8), seguridad en el desarrollo (A.8.25-A.8.28) y gestión de vulnerabilidades (A.8.8). Ninguna herramienta se usa sin autorización y sin registro.
> **BCU:** Las herramientas de IA autorizadas deben estar documentadas en los EMG y el RNRCSF como componentes de la infraestructura de TIC.
> **URCDP:** Para el tratamiento de datos personales, la herramienta debe permitir minimización, trazabilidad y control (PD.5, PD.6). Las herramientas que siguen se eligieron por eso.
> **Nivel del curso:** 🟡 Practicar

---

## 1. La familia de herramientas oficiales del Banco

El Banco no entrega "un chatbot". Entrega un **ecosistema** de herramientas que se complementan y que, bien entendidas, cubren las necesidades de los 300 funcionarios sin que tengan que buscar alternativas en internet.

| Herramienta | Qué es | Quién la usa | Analogía |
|---|---|---|---|
| **OpenCode** | Asistente de código que trabaja **sobre los archivos del Banco**, en la computadora del desarrollador, con autorización para editar y ejecutar en entornos de prueba | Desarrolladores y TI | Un programador junior que lee, edita y prueba los archivos del proyecto con usted, sin copiarlos a ningún lado |
| **BigPickle** | Interfaz amigable en español para **chatear, redactar, resumir y preguntar** usando modelos seguros | Todos los funcionarios | Una ventanilla de ayuda que responde en lenguaje común |
| **Ollama** | Programa que **corre el modelo de IA dentro de la red del Banco** (sin internet) | TI/RSI (administración) | La imprenta propia del Banco: los documentos no salen del edificio |
| **vLLM** | Servidor de **inferencia de alto rendimiento** que sirve las respuestas del modelo a las aplicaciones | TI/RSI (administración) | El motor del edificio que da energía a todas las herramientas |

La idea clave: **BigPickle es la puerta de entrada amigable para todos; OpenCode es la herramienta profesional para código; Ollama y vLLM son la infraestructura que hace que todo funcione adentro del Banco.**

---

## 2. OpenCode: el asistente que trabaja con tus archivos

### Qué es

OpenCode es un **agente de código** que corre en la terminal de la computadora del desarrollador. A diferencia de un chat, OpenCode **puede ver, crear y modificar archivos del proyecto** del Banco, y puede ejecutar comandos en entornos de prueba. Es como tener un colega que "se pone los lentes" sobre el código del Banco.

### Cómo funciona por dentro

1. Usted le da una **instrucción** ("encontrá el bug en el cálculo de intereses y corregilo").
2. OpenCode **explora los archivos** del repositorio local (no los sube a internet).
3. Con el contexto del proyecto, el modelo propone cambios; usted **revisa cada cambio** (diff) y aprueba o rechaza.
4. Solo lo que usted aprueba se escribe en el archivo.

### Garantías de seguridad

- Los archivos del Banco **se procesan en la red del Banco** (modelo servido por Ollama/vLLM local o nube contratada con garantías).
- Nada se envía a cuentas personales de terceros.
- Cada cambio queda **registrado** (qué se tocó, cuándo, quién aprobó): evidencia para auditoría.

### Reglas para el desarrollador

1. Nunca pegar código de clientes o datos reales de producción en una herramienta externa.
2. Probar siempre en **entornos de desarrollo/QA**, nunca en producción.
3. Revisar el **diff** (el detalle de los cambios) antes de aceptar.
4. No autorizar a OpenCode a ejecutar comandos de producción sin supervisión.

---

## 3. BigPickle: la ventanilla amigable para todos

### Qué es

BigPickle es la **interfaz en español** que el funcionario común usa para chatear con la IA del Banco. Sirve para:

- Redactar y mejorar **correos, memorandos y cartas**.
- **Resumir** documentos largos.
- **Explicar** conceptos en lenguaje simple.
- Preparar borradores de informes, presentaciones y comunicaciones.
- Preguntar sobre **procedimientos del Banco** (cuando esté conectada a un RAG con la documentación interna).

### Cómo funciona por dentro

1. El funcionario escribe su solicitud (prompt) en la ventana.
2. La solicitud viaja **solo dentro de la red del Banco** al motor local (Ollama/vLLM).
3. El modelo responde; la respuesta vuelve al funcionario.
4. Todo queda en el **registro de uso** del Banco (quién, cuándo, qué pregunta) para auditoría.

### La regla de oro para el funcionario

> **En BigPickle se escribe como si el correo estuviera a la vista de todos: no se pegan cédulas, saldos, claves, ni datos de clientes. Si necesita trabajar con datos de clientes, primero los anonimiza o los trabaja en los sistemas autorizados.**

BigPickle existe **precisamente** para que no sienta la tentación de abrir una cuenta personal en otra herramienta: si necesita redactar algo, la herramienta segura ya está a un clic.

---

## 4. Ollama: la "imprenta propia" del Banco

### Qué es

**Ollama** es un programa que permite **descargar y ejecutar modelos de lenguaje dentro de la red del Banco**, sin conexión a internet. Es la diferencia entre "mandar los documentos a imprimir afuera" e "imprimir en la imprenta del Banco".

### Por qué importa para la seguridad

- Los **datos nunca salen** del Banco: el modelo corre en servidores propios.
- No hay contrato con un tercero, ni retención de datos externa, ni riesgo de que el texto se use para entrenar modelos ajenos.
- Se pueden usar modelos abiertos (como las familias Llama, Qwen, Mistral) en versiones controladas.

### Limitaciones honestas

- Un modelo local es **menos potente** que los gigantes de la nube. A cambio, ofrece **confidencialidad total**.
- Exige hardware (GPU) y mantenimiento por parte de TI.
- Requiere ser **actualizado** para no quedarse con modelos vulnerables o desactualizados.

### Veredicto para el Banco

Para datos de clientes y documentación interna confidencial: **Ollama local es la opción más segura** porque el dato no viaja. Para tareas sin datos sensibles, se pueden usar los modelos de la nube contratada con garantías (si existen).

---

## 5. vLLM: el motor de alta velocidad

### Qué es

**vLLM** es un **servidor de inferencia**: un programa que expone el modelo (corriendo en Ollama o en su propia arquitectura) como un **servicio** al que las aplicaciones del Banco consultan. Mientras Ollama es la "imprenta", vLLM es la "columna vertebral" que reparte el trabajo para que muchas personas usen la IA a la vez con buena velocidad.

### Qué hace en el ecosistema

1. Recibe las solicitudes de BigPickle, OpenCode y otras aplicaciones.
2. Las encola y las procesa contra el modelo.
3. Devuelve las respuestas con **velocidad y trazabilidad** (cuánto tardó, qué modelo, qué versión).

### Por qué importa para el RSI

- Permite **centralizar** el uso: todo pasa por un único punto auditable.
- Facilita **limitar** quién puede usar qué modelo.
- Sirve para **registrar** el volumen de uso y detectar abusos (alguien pegando datos masivos, horarios anómalos).

---

## 6. Cómo se conecta todo (el flujo de una consulta)

```
Funcionario escribe en BigPickle
        │
        ▼
Solicitud viaja DENTRO de la red del Banco
        │
        ▼
vLLM (motor) → Ollama (modelo local)  [o nube contratada con garantías]
        │
        ▼
Respuesta vuelve al funcionario
        │
        ▼
Registro de uso: quién, cuándo, qué se preguntó (auditoría)
```

En este flujo, **en ningún momento los datos salen de la infraestructura controlada del Banco** (salvo nube contratada con contrato de protección de datos, que se declara y se audita).

---

## 7. ¿Cuál uso para qué? Tabla de decisión rápida

| Necesito | Herramienta |
|---|---|
| Redactar o resumir textos en español, sin tocar código | BigPickle |
| Escribir, revisar o explicar código del Banco | OpenCode |
| Preguntar sobre la documentación interna (políticas, procedimientos) | BigPickle conectado a RAG (AISEC-04) |
| Administrar y actualizar los modelos | Ollama + vLLM (TI/RSI) |
| Probar un modelo nuevo sin salir del Banco | Ollama (descarga local) + pruebas |

---

## 8. Conclusión del módulo

- El Banco ofrece un ecosistema completo: **BigPickle** (todos), **OpenCode** (desarrollo), **Ollama** (modelos locales) y **vLLM** (servidor de inferencia).
- La arquitectura está pensada para **que los datos no salgan del Banco** y para que **todo quede registrado**.
- Si usted necesita una herramienta y el Banco no la ofrece, **no use una personal**: solicítela por el canal de TI/RSI. Usar una herramienta externa con datos del Banco es el incidente que este curso quiere evitar.
- Ninguna herramienta reemplaza la **revisión humana** del resultado.

> **Ejercicio:** Identifique su perfil (funcionario común, desarrollador, RSI). Luego responda: ¿cuál es la herramienta oficial que le corresponde y cuál es la primera tarea que haría con ella esta semana? Traiga esa tarea al módulo AISEC-07 (guía de prompts) para redactarla correctamente.
