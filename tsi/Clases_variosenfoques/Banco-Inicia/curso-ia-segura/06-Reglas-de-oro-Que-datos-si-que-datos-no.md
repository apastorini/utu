# AISEC-06 · Reglas de oro: qué datos sí y qué datos no

> **Función del MCU 5.0:** Este módulo traduce los principios de protección de datos (PD.2 veracidad, PD.3 finalidad, PD.5 seguridad, PD.6 reserva) en reglas prácticas y memorizables para el personal del Banco.
> **ISO/IEC 27001:** Clasificación de la información (A.5.12-A.5.13) y prevención de fuga de datos (A.8.12).
> **BCU:** La correcta clasificación de los datos que entran a la IA es parte de la gestión de riesgo operacional documentable en los EMG.
> **URCDP:** Minimización, finalidad y confidencialidad (Ley 18.331 arts. 9-10 y 27) aplicadas a la ventana de chat.
> **Nivel del curso:** 🟢 Descubrir

---

## 1. La tabla que todos deben conocer

Esta es la tabla que todo funcionario debe tener a la vista. **Cuando use la IA oficial (BigPickle, OpenCode, etc.), los datos verdes están bien; los datos amarillos exigen permiso o anonimización; los datos rojos nunca entran por chat.**

### 🟢 Datos SEGUROS de ingresar (sin datos personales)

| Dato | Ejemplo |
|---|---|
| Textos propios sin datos de personas | Un borrador de correo genérico, un comunicado, un informe sin nombres |
| Ideas, lluvia de ideas, borradores | "Ayudame a estructurar una presentación sobre control interno" |
| Contenido público conocido | Normativa publicada, noticias, fechas oficiales |
| Texto anonimizado | "Cliente de la sucursal 5 con 90 días de mora" (sin nombre, cédula ni saldo) |
| Estructuras y formatos | Plantillas, modelos de documentos sin contenido real |

### 🟡 Datos CONDICIONADOS (requieren permiso, anonimización o proceso formal)

| Dato | Qué hacer antes |
|---|---|
| Documentos internos del Banco | Verificar clasificación; usar el RAG autorizado, no el chat abierto |
| Datos de clientes anonimizados | Confirmar que no permite identificar a la persona (art. 4 Ley 18.331) |
| Código del Banco | Usar solo OpenCode en entorno de desarrollo; nunca en herramientas externas |
| Listados internos (no personales) | Revisar si contienen información que pueda combinarse para identificar a alguien |

### 🔴 Datos PROHIBIDOS de ingresar

| Dato | Por qué |
|---|---|
| Nombres y apellidos de clientes | Dato personal (Ley 18.331) |
| Cédula, RUT, pasaporte | Dato personal de identificación |
| Saldos, deudas, garantías, cupos | Dato financiero personal / secreto bancario |
| Historial de operaciones | Dato personal sensible |
| Claves, PIN, tokens, contraseñas | Credencial de acceso |
| Números de cuenta, tarjetas | Dato financiero personal |
| Datos de salud | Dato sensible con protección reforzada (Decreto 414/009) |
| Expedientes judiciales, denuncias | Dato sensible |
| Información de empleados (sueldos, salud, disciplinaria) | Dato personal de terceros |
| Secretos comerciales / estrategia del Banco | Confidencialidad institucional |
| Documentos clasificados "reservado" | Clasificación del Banco |

> **Regla simple para no equivocarse:** **"Si el dato identifica o puede identificar a una persona, no entra por el chat."** Cuando no esté seguro, consulte con su jefe, con TI o con el DPD.

---

## 2. La prueba de los 3 segundos

Antes de pegar cualquier texto en la IA, haga mentalmente la **prueba de los 3 segundos**:

1. **¿Identifica a alguien?** (nombre, cédula, dirección, empresa unipersonal, teléfono) → ❌ no entra.
2. **¿Es confidencial del Banco?** (secreto comercial, estrategia, código, informes reservados) → ❌ no entra sin proceso.
3. **¿Lo escribiría en una cartelera pública?** Si la respuesta es no → ❌ no entra por chat.

Si cualquiera de las tres respuestas es "sí", **no pegue el dato**: anonimice, use el sistema oficial, o consulte.

---

## 3. Anonimizar: la técnica que salva el día

Cuando necesite trabajar con un ejemplo que incluye datos de clientes, **anonimice** antes de ingresarlo. Reemplace:

- Nombre → "Cliente A"
- Cédula → "XXXXXXXX-X"
- Saldo → "s/x"
- Cuenta → "CUENTA-0001"

Ejemplo:
> **Mal:** "Redactá un correo a Juan Pérez, cédula 3.123.456-7, que tiene 4.500 USD de deuda en la tarjeta."
>
> **Bien:** "Redactá un correo formal a un cliente con una deuda de 90 días por un monto de mediana importancia, tono firme pero cordial."

> **Importante:** anonimizar no es "poner las iniciales" ni "borrar solo el nombre". Si con la combinación de datos restantes alguien puede identificar a la persona (por ejemplo, "cliente de la sucursal 5, médico, 74 años, con 6 propiedades"), sigue siendo dato personal. Ante la duda, consulte al DPD.

---

## 4. Reglas de oro resumidas (para imprimir)

1. **Herramienta oficial siempre**: nada de cuentas personales de IA con datos del Banco.
2. **Dato que identifica = no entra**: la prueba de los 3 segundos.
3. **Anonimice** antes de usar ejemplos.
4. **La IA redacta, la persona verifica**: todo resultado se revisa (alucinaciones).
5. **Documentos internos → RAG autorizado**, no chat abierto.
6. **Código → OpenCode en entorno de desarrollo**, nunca en herramientas externas.
7. **Ante la duda, pregunte**: jefe, TI/RSI o DPD.
8. **Nunca "solo por esta vez"**: las excepciones se piden y se autorizan por escrito.

---

## 5. Conclusión del módulo

- Los datos se clasifican en **verde (seguros), amarillo (condicionados) y rojo (prohibidos)**.
- La **prueba de los 3 segundos** evita la gran mayoría de las fugas.
- La **anonimización** es la herramienta diaria para trabajar con ejemplos.
- Ante la duda, se consulta: nadie es sancionado por preguntar; sí se investiga la fuga silenciosa.

> **Ejercicio:** Clasifique las siguientes frases en 🟢/🟡/🔴: (1) "Cliente con 90 días de mora en sucursal 3"; (2) "Juan Pérez, 4.500 USD de deuda"; (3) "Borrador de correo de bienvenida a nuevos clientes" (sin datos); (4) "código del módulo de liquidación de intereses". Respuestas al final del módulo 12.
