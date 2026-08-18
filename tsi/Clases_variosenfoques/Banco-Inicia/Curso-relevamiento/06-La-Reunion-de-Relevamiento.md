# RELEV-06 · La reunión de relevamiento: preparar, conducir, registrar

> **Función del MCU 5.0:** La reunión es el vehículo de la función ID (Identificar): sin conversación con las áreas no hay inventario de activos (ID.AM) ni identificación de riesgos (ID.RA). Un activo que no se detectó en la reunión no existe para el SGSI.
> **ISO/IEC 27001:** Sustenta las cláusulas 4 (contexto de la organización) y 5.2 (política), y el Anexo A en materia de activos (A.8) y de relaciones con las partes interesadas (A.15): el contexto no se redacta, se releva.
> **BCU:** La minuta firmada y las fichas de activo son la evidencia de que el RSI conoce la operación real, requisito del EMG, la Circular 2227 y el RNRCSF art. 492.
> **URCDP:** En la reunión se detectan las bases de datos personales y sus responsables, insumo directo del registro de tratamientos (URCDP-04) y del Documento de Seguridad (URCDP-01).
> **Nivel del curso:** 🟢 Descubrir · 🟡 Practicar · 🔴 Dominar

---

## 1. Antes de la reunión: preparar para ganar

Una reunión de relevamiento no se improvisa. El 80 % del éxito se decide antes de que entre el primer asistente a la sala. Si llegás a la reunión sin saber qué documento del kit vas a alimentar, sin haber leído el dossier del área y sin saber con quién vas a hablar, vas a perder la única oportunidad que el área te va a dar: su tiempo y su atención.

> **Regla de oro:** en el relevamiento, la reunión es el único momento donde podés hacer preguntas en vivo. El resto del ciclo (pedido de evidencia, registro, seguimiento) es trabajo individual. Preparala como si fuera un examen.

> **Recordá verificar contra el organigrama vigente del Banco antes de cada reunión**: las personas y las divisiones cambian, y tu dossier puede quedar desactualizado. Confirmá también los nombres propios con el archivo maestro de capital humano o con el área de Relaciones Institucionales.

### 1.1 Definir el objetivo: qué documento del kit alimenta esta reunión

Cada reunión tiene que responder una pregunta única. No se releva "el banco en general": se releva **algo específico** que alimenta **un documento específico** del kit.

| Documento del kit | Objetivo típico de la reunión | Pregunta única de la reunión |
|---|---|---|
| ID-01 (Inventario de Activos) | Inventariar activos del área | ¿Qué sistemas, bases y archivos son de este proceso? |
| ID-02/ID-03 (riesgos) | Detectar riesgos y controles existentes | ¿Qué podría fallar y cómo se previene hoy? |
| URCDP-04 (ROPA) | Relevar tratamientos de datos personales | ¿Qué datos personales maneja este proceso y para qué? |
| URCDP-01 (Documento de Seguridad) | Comparar medidas declaradas vs reales | ¿Qué medidas de seguridad aplicás de verdad? |
| PR-02 (roles y accesos) | Relevar roles y autorizaciones | ¿Quién tiene acceso a qué y quién lo autoriza? |

Antes de agendar, escribí la pregunta única en una sola línea. Si no podés escribirla, todavía no estás listo para la reunión.

### 1.2 Estudiar el dossier del área (RELEV-04)

En el módulo **RELEV-04** está el dossier por división. Léelo completo antes de la reunión y llevá anotadas las preguntas que te quedaron pendientes. El dossier te dice qué sistemas, bases y procesos pertenecen a cada área; la reunión sirve para **confirmar, corregir y completar** ese mapa, no para empezarlo de cero.

### 1.3 Identificar al interlocutor (RELEV-05)

No es lo mismo relevar al Jefe de División que al jefe de proceso que hace el trabajo todos los días. El módulo RELEV-05 describe los perfiles típicos del Banco:

- El **decisor** (director, jefe de área): aprueba, no conoce el detalle operativo. Sirve para abrir la puerta y validar compromisos.
- El **operativo** (analista, técnico, encargado): conoce el proceso real, los sistemas y los problemas. Es el que te va a dar la evidencia.
- El **técnico de TI** (producción, sistemas, soporte): conoce servidores, bases, redes y backups. Es tu aliado para ID-01 y para las evidencias de BCU.

> **Consejo:** pedí siempre "la persona que hace el trabajo" en la reunión, no solo el jefe. Un jefe describe el proceso como debería ser; el operativo lo describe como es.

### 1.4 Elegir lugar, duración y sponsor

- **Lugar:** sala de reunión del área o videoconferencia. La videoconferencia es aceptable para el primer contacto, pero para relevar procesos complejos es mejor estar cara a cara.
- **Duración:** 45 a 60 minutos. Más de 60 minutos cansa y menos de 45 no alcanza. Si el tema es muy grande, dividilo en dos reuniones.
- **Sponsor presente:** sí, en las dos primeras reuniones de cada división. El sponsor (jefe de área) da contexto, autoriza el pedido de evidencia y muestra que el relevamiento tiene respaldo. Cuando el vínculo esté maduro, reunite directo con el operativo.

### 1.5 Armar el "kit de reunión"

Prepará una carpeta (física o digital) que lleves a todas las reuniones. Que tenga siempre lo mismo:

| Elemento del kit | Para qué sirve |
|---|---|
| Minuta en blanco (plantilla de la sección 6) | Registrar la reunión mientras transcurre |
| Ficha de activo en blanco (plantilla de la sección 6) | Anotar cada activo que surja |
| Lista de evidencias solicitadas (plantilla de la sección 6) | Anotar lo que el área promete entregar |
| Dossier del área (RELEV-04) con tus notas | No repetir preguntas ya respondidas |
| Agenda impresa para repartir | Mantener la reunión enfocada |
| Lista de asistentes | Registrar quién estuvo y quién no |

---

## 2. La invitación: agenda previa y preguntas anticipadas

La invitación no es "¿podemos juntarnos el jueves?". La invitación formal tiene tres partes: **para qué nos juntamos**, **qué agenda vamos a seguir** y **qué preguntas anticipadas queremos responder**. Enviá esta agenda **2 a 3 días antes** de la reunión por tres motivos:

1. **El área se prepara**: el interlocutor llega con la información lista, no a improvisar.
2. **Ahorrás tiempo de reunión**: lo que se responde por escrito antes, no ocupa minutos valiosos.
3. **Anticipás la evidencia**: el área puede empezar a buscar documentos antes de que se los pidas formalmente.

### Plantilla de correo de invitación

```text
Asunto: Reunión de relevamiento SGSI · [División/Área] · [Fecha y hora]

Estimado/a [Nombre] [Apellido]:

En el marco del proyecto de implementación del Sistema de Gestión de
Seguridad de la Información (SGSI) del Banco, te invito a una reunión de
relevamiento del área [División/Área] a tu cargo.

Objetivo de la reunión: conocer en detalle los procesos, sistemas,
bases de datos y archivos del área para completar el Inventario de
Activos (ID-01) y el registro de tratamientos de datos personales
(URCDP-04) del banco.

Fecha: [día] de [mes] de [año], de [HH:MM] a [HH:MM]
Lugar: [sala / enlace de videoconferencia]
Duración estimada: 60 minutos

Agenda:
1. Apertura y presentación (5 min): contexto del relevamiento.
2. Contexto del área (5 min): funciones y procesos principales.
3. Preguntas guía (30 min): activos, sistemas y bases de datos.
4. Evidencias y próximos pasos (10 min): qué documentos se pueden
   entregar y en qué fecha.
5. Cierre (10 min): acuerdos, minuta y compromisos.

Para aprovechar mejor el encuentro, si podés anticipar por escrito
antes de la reunión:
- Listado de sistemas y aplicaciones que usa el área.
- Bases de datos o archivos (físicos o digitales) donde se guardan
  datos de clientes o del personal.
- Documentación existente de procesos (manuales, instructivos).

La reunión es confidencial y el uso de la información relevada es
exclusivamente para el cumplimiento del SGSI del Banco.

¿Te confirma el horario? Quedo atento.

Saludos cordiales,
[Nombre del RSI / facilitador]
Responsable de Seguridad de la Información · Banco
```

---

## 3. La estructura de la reunión en 5 partes

| Parte | Tiempo | Qué se hace | Qué se dice (guion) |
|---|---|---|---|
| 1. Apertura | 5' | Presentar al equipo, explicar el porqué, confirmar la agenda y la confidencialidad | "Gracias por el tiempo. Esto no es una auditoría: queremos conocer el área para que el banco cumpla con las normas de ciberseguridad y protección de datos. Todo lo que conversemos es confidencial y el objetivo es documentar." |
| 2. Contexto | 5' | Que el área cuente su función, sus procesos y sus prioridades | "Contanos en cinco minutos: ¿cuál es la función principal del área, quiénes integran y qué procesos son los críticos?" |
| 3. Preguntas guía | 30' | Recorrer las preguntas del dossier: sistemas, bases, activos, controles | "¿Qué sistemas usan a diario? ¿Dónde se guarda la información de los clientes? ¿Quién autoriza los accesos?" |
| 4. Evidencias y próximos pasos | 10' | Listar qué evidencia se va a pedir y quién la entrega | "De lo que mencionaron, hay tres documentos que nos ayudarían: el manual de [proceso], el listado de [base], y el reporte de [sistema]. ¿Quién los puede facilitar y en qué plazo?" |
| 5. Cierre | 5' | Resumir acuerdos, compromisos, fechas y agradecer | "En resumen: nos comprometieron [X] evidencias para el [fecha]. Les envío la minuta en 48 horas para validar. Gracias." |

**La regla de los 5-5-30-10-5:** la pregunta que lleva la reunión es la de la parte 3. Si la apertura, el contexto o el cierre se estiran, la parte central sufre. Controlá el reloj en cada transición.

---

## 4. Técnicas de conducción

### 4.1 Preguntas abiertas vs preguntas cerradas

- **Cerradas** (¿sí o no? ¿cuántos?): sirven para confirmar datos. "¿El sistema funciona 24x7?" → "Sí".
- **Abiertas** (¿cómo? ¿quién? ¿qué pasaría si?): sirven para descubrir procesos. "¿Cómo se procesa una solicitud de crédito hoy?"

En la parte 3 de la reunión, el 70 % de las preguntas deben ser abiertas. Las cerradas quedan para confirmar lo que ya te contaron.

### 4.2 La técnica del "¿cómo lo hacés hoy?"

En vez de preguntar "¿tienen políticas de acceso?", preguntá:

> "Cuando un empleado nuevo entra al área, **cómo lo hacés hoy** para darle acceso al sistema?"

Esta pregunta revela el proceso real, no el declarado: quién pide, quién autoriza, quién da de alta, cuánto tarda y dónde queda el registro. El "cómo lo hacés hoy" es la técnica más rentable del relevamiento: descubre la operación y las brechas en la misma respuesta.

### 4.3 Pedir ejemplos concretos

Los nombres genéricos no sirven para el inventario. Cada vez que el interlocutor diga "el sistema", "la base", "el servidor", pedí lo concreto:

- Nombre del sistema o aplicación.
- Nombre de la base de datos y su motor.
- Marca y modelo del activo (para hardware), o proveedor y versión (para software).
- Ubicación física o lógica (sala de servidores, sede central, sucursal, nube).

> **Ejemplo de diálogo real:** "¿Dónde se guarda la información de los clientes de crédito?" → "En el sistema de crédito." → "¿Cuál es el nombre del sistema? ¿Y la base de datos se llama igual? ¿Está en el datacenter de la sede central o en otro lado?"

### 4.4 Verificación cruzada

Cuando un dato es importante (un activo crítico, un control clave, un acceso especial), confirmalo con al menos **dos personas de áreas distintas**. Por ejemplo: el jefe de proceso dice que el backup es diario; el responsable de TI dice que es nocturno. La verdad suele estar en la conversación entre ambos, y la discrepancia es en sí misma un hallazgo para ID-02/ID-03.

### 4.5 Manejar al que monopoliza la conversación

- **Redirigí con respeto:** "Excelente ese punto, lo anoté. Quería preguntarle también a [nombre del otro asistente]…"
- **Usá la agenda como escudo:** "Vamos bien con la agenda; este tema lo podemos profundizar en el seguimiento."
- **Anotá en "aparcamiento":** un espacio de la minuta para temas que no corresponden al objetivo y se retoman después. No los perdés ni descarrilás la reunión.

### 4.6 Respetar el tiempo

El tiempo del área es prestado. Si la reunión se agota y quedan preguntas, agendá una segunda sesión en el acto, en vez de estirar los 60 minutos. Terminar a tiempo es una señal de profesionalismo que el área va a recordar en el próximo relevamiento.

### 4.7 Tomar notas mientras se habla

La minuta se escribe **en la reunión**, no de memoria al final. Anotá:

- Frases textuales que describen procesos (van entre comillas a la minuta).
- Nombres propios de sistemas, bases y archivos.
- Compromisos: quién, qué, para cuándo.
- Dudas que después verificás por escrito (RELEV-07).

> **Recordá verificar contra el organigrama vigente del Banco**: si el área que estás relevando cambió de responsable o de dependencia, ajustá la ficha del área en el mismo momento y reflejalo en la minuta.

---

## 5. Qué NO preguntar en la primera reunión

| No preguntes | Por qué | Cuándo sí |
|---|---|---|
| Listados exactos de accesos de usuarios | Es información sensible que no se comparte de palabra; debe pedirse por canal formal con justificación y registro | En RELEV-07, por correo/memorando al área de Sistemas |
| Vulnerabilidades conocidas o incidentes recientes | Genera resistencia y no es un dato que el área declare en vivo | En reuniones de trabajo de riesgos (ID-03), con confidencialidad firmada |
| Secretos comerciales o credenciales | Nunca, bajo ninguna circunstancia | No corresponde al SGSI |
| Detalle de configuraciones de seguridad | Es evidencia que debe entregarse por escrito, no describirse de palabra | En RELEV-07, con formato y control de entrega |

La primera reunión **abre el mapa** (qué existe y quién lo maneja). Los **detalles finos** (accesos, configuraciones, vulnerabilidades) se piden después por los canales formales con registro y justificación normativa.

---

## 6. Registro en el momento: las tres plantillas

### 6.1 Minuta de reunión

```text
MINUTA DE REUNIÓN DE RELEVAMIENTO SGSI
======================================

Fecha:            [DD/MM/AAAA]
Hora:             [HH:MM] – [HH:MM]
Lugar:            [sala / videoconferencia]
Documento del kit que alimenta: [ID-01 / ID-03 / URCDP-04 / otro]

ASISTENTES
----------
| Nombre | Cargo/Área | Rol en la reunión |
|--------|-----------|-------------------|
|        |           |                   |

OBJETIVO DE LA REUNIÓN
----------------------
[Una sola frase: qué pregunta se vino a responder.]

HALLAZGOS
---------
1. [Frases textuales del área y datos concretos.]
2. [Nombre del sistema / base / proceso y quién lo mencionó.]

ACTIVOS DETECTADOS (ver ficha de activo por cada uno)
-----------------------------------------------------
| Activo | Tipo | Área dueña | Detalle |
|--------|------|-----------|---------|

COMPROMISOS
-----------
| Compromiso | Responsable | Fecha límite |
|-----------|------------|--------------|

EVIDENCIAS PROMETIDAS
---------------------
| Evidencia | Solicitada a | Formato | Fecha límite |
|----------|-------------|---------|-------------|

APARCAMIENTO (temas para retomar)
---------------------------------
- [Tema que no corresponde al objetivo y se retoma en otra reunión.]

PRÓXIMOS PASOS
--------------
1. Enviar esta minuta para validación (48 h).
2. Pedir formalmente las evidencias (RELEV-07).
3. [Siguiente reunión / entrega del documento del kit.]

--------------------------------------------------
Confeccionó: [Nombre] · Fecha de envío para validación: [DD/MM/AAAA]
```

### 6.2 Ficha de activo

Una ficha por cada activo detectado. Si en una reunión salen cinco activos, son cinco fichas.

```text
FICHA DE ACTIVO · INVENTARIO SGSI (insumo de ID-01)
===================================================

Nombre del activo:    [Ej.: "Base de Crédito Hipotecario"]
Tipo de activo:       [Sistema / Aplicación / Base de datos / Hardware /
                       Documento físico / Proceso / Persona / Instalación]
Área dueña:           [Ej.: División Banca Persona]
Proceso asociado:     [Ej.: Otorgamiento de crédito hipotecario]
Sistema asociado:     [Ej.: Banco En Línea / core / planilla Excel]
Clasificación CID preliminar:
  - Confidencialidad: [Alta / Media / Baja]  Motivo:
  - Integridad:       [Alta / Media / Baja]  Motivo:
  - Disponibilidad:   [Alta / Media / Baja]  Motivo:
Ubicación:            [Sede central / sucursal / datacenter / nube]
Responsable:          [Nombre, cargo, teléfono, correo]
Fecha de detección:   [DD/MM/AAAA]  (reunión del relevamiento)
Fuente:               [Nombre del interlocutor que lo informó]
Observaciones:        [Particularidades: accesos, dependencias, terceros]
Estado:               [Borrador / Confirmado por el área / Validado]
```

### 6.3 Planilla de evidencias solicitadas

```text
PLANILLA DE EVIDENCIAS SOLICITADAS · RELEVAMIENTO SGSI
======================================================

| ID | Documento del kit | Ítem de evidencia | Solicitada a | Fecha de solicitud | Fecha límite | Estado | Ubicación en repositorio |
|----|-------------------|-------------------|--------------|--------------------|--------------|--------|--------------------------|
| EV-001 | ID-01 | Diagrama de red del área | Depto. Sistemas | DD/MM/AAAA | DD/MM/AAAA | Solicitada | 01-IDENTIFICACION/... |
| EV-002 | URCDP-04 | Listado de bases de datos | Depto. Información y Apoyo Comercial | DD/MM/AAAA | DD/MM/AAAA | Solicitada | 06-CUMPLIMIENTO/URCDP/... |

ESTADOS: Solicitada / Recibida / Validada / No existe → brecha
```

> **Regla del mismo día:** la minuta, las fichas y la planilla se completan **el día de la reunión**, aunque estén en borrador. La memoria de la reunión se degrada en horas, no en días.

---

## 7. Después de la reunión: cerrar el ciclo

### 7.1 Enviar la minuta en 24-48 horas

La minuta se envía al área en un máximo de 48 horas, pidiendo corrección y validación:

```text
Asunto: Minuta de reunión de relevamiento · [División/Área] · [Fecha]

Estimado/a [Nombre]:

Adjunto la minuta de la reunión de relevamiento del [fecha]. Como
acordamos, el objetivo era completar [documento del kit].

Te pido revisar el documento y corregir cualquier dato que no esté
bien reflejado (sistemas, bases, responsables, compromisos). Una vez
que confirmes el contenido, quedará firmado como registro del
relevamiento del área. Recuerda: quien corrige, firma el contenido.

Si no recibimos comentarios en 5 días hábiles, se considerará
validada en los términos enviados.

Quedo a disposición para la reunión de seguimiento y el pedido
formal de evidencias.

Saludos cordiales,
[Nombre del RSI / facilitador] · Banco
```

La regla **"quien corrige, firma el contenido"** es clave: la minuta validada por el área deja de ser tu interpretación y pasa a ser un registro institucional que el área reconoce como cierto.

### 7.2 Agradecer y agendar seguimiento

Agradecé explícitamente a los asistentes y agendá la reunión de seguimiento antes de despedirte. El seguimiento tiene una fecha, una hora y una agenda mínima: revisar las evidencias prometidas y profundizar lo que haya quedado abierto.

### 7.3 Volcar a ID-01

Cada ficha de activo validada pasa al Inventario de Activos (ID-01). El módulo **RELEV-08** explica en detalle cómo volcar la conversación al documento del kit, incluyendo las columnas del inventario, los ejemplos completos y la higiene del registro (fechas, versiones, responsables).

### Checklist del cierre

- ☐ Minuta enviada al área en menos de 48 horas.
- ☐ Correcciones del área incorporadas y confirmadas.
- ☐ Agradecimiento enviado a los asistentes.
- ☐ Fichas de activo completadas el mismo día de la reunión.
- ☐ Planilla de evidencias actualizada con lo prometido.
- ☐ Reunión de seguimiento agendada.
- ☐ Activos validados volcados a ID-01 (RELEV-08).

---

## 8. Errores comunes

| Error | Consecuencia | Cómo evitarlo |
|---|---|---|
| Ir sin agenda ni kit de reunión | Reunión difusa, sin datos concretos, activos perdidos | Armar el kit y la agenda antes de invitar (secciones 1 y 2) |
| Entrevistar solo al jefe | Inventario "como debería ser", no real | Pedir que también esté la persona que hace el trabajo |
| Tomar notas "después" | Datos inventados o perdidos, nombres mal escritos | Minuta en el momento, con frases textuales |
| No pedir nombres concretos | Inventario con "el sistema" sin nombre | Aplicar la técnica del dato concreto (sección 4.3) |
| Dejar que alguien monopolice | Evidencia incompleta, personas clave silenciadas | Redirigir con la agenda y el apartamiento |
| Preguntar secretos en la primera reunión | Resistencia del área y cortocircuito del proyecto | Pedir lo fino por canales formales (RELEV-07) |
| No enviar la minuta | Registro que nadie validó = información que no existe | Enviar en 24-48 h y exigir confirmación |
| No actualizar el organigrama | Datos desactualizados en ID-01 y GV-02 | Verificar contra el organigrama vigente del Banco |

---

## 9. Cierre del módulo

Preparaste, condujiste y registraste tu primera reunión de relevamiento: objetivo claro, dossier estudiado, interlocutor identificado, invitación con agenda anticipada, estructura de 5 partes con tiempos, técnicas de conducción, minuta y fichas registradas en el momento y cierre con minuta validada y seguimiento agendado. El siguiente paso es convertir las evidencias prometidas en pedidos formales, en **RELEV-07 · Pedido de evidencias**.

---

**Documentos relacionados:** ID-01, GV-02, GV-03, PR-02
