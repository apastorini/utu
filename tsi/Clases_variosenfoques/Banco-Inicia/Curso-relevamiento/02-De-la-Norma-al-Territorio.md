# RELEV-02 · De la norma al territorio: qué relevar y por qué

> ⚠️ **Verificar contra el organigrama vigente:** los nombres, áreas y documentos citados corresponden al organigrama de abril 2026 (PDF SF.PLE.05, https://www.bhu.com.uy/sobre-bhu/organigrama) y al catálogo del kit Banco-Inicia. Antes de usar un nombre o un código en un documento oficial, confirmalos contra la versión vigente del banco y del kit.
>
> **Función del MCU 5.0:** este módulo traduce las 6 funciones del MCU 5.0 (GV/ID/PR/DE/RS/RC) y sus 72 requisitos en preguntas concretas para cada área del Banco: el relevamiento es el puente entre la norma y la evidencia.
> **ISO/IEC 27001:** la evidencia es el corazón de la cláusula 9 (evaluación del desempeño) y 10 (mejora): registros verificables, fechados, trazables e íntegros.
> **BCU:** el EMG, el RNRCSF art. 492, la Circular 2227 y la Comunicación 2022/254 se relevan como datos concretos: quién resguarda, cada cuánto se prueba, dónde están las copias y las claves.
> **URCDP:** cada tratamiento de datos personales relevado alimenta el ROPA (URCDP-04), el Documento de Seguridad (URCDP-01) y las notificaciones (URCDP-02).
> **Nivel del curso:** 🟡 Practicar

---

## 1. Idea central: la norma no pide papeles, pide "saber y demostrar"

Pensá el banco como una casa que vas a asegurar. La aseguradora no te pide "el contrato de seguro": te pide **el inventario de lo que hay dentro** (qué muebles, qué valor tienen, dónde están), **los riesgos** (dónde hay riesgo de incendio o robo) y **las medidas** (si tenés alarmas, llaves, detectores). Eso es exactamente lo que hacen MCU 5.0, BCU y URCDP con el Banco: te piden **conocer** la casa (activos y riesgos) y **demostrar** que la cuidás (controles y evidencias).

**La regla de oro del relevamiento:** todo requisito de la norma se traduce en dos cosas:
1. **Una pregunta al área** que ya entienda el negocio (RELEV-01), y
2. **Una evidencia** que demuestre lo que el área respondió.

Si hacés una reunión y no te llevás ni una pregunta nueva ni una evidencia pendiente, esa reunión no sirvió. Esa es la prueba de fuego que vas a aplicar en cada sesión del plan (RELEV-03).

**Analogía del relevamiento como foto de la casa.** El SGSI del Banco no se construye sobre intenciones: se construye sobre una **fotografía real** del estado de la casa. Cada área te entrega una habitación de esa foto: TI te muestra los servidores, Comercial te muestra las bases de clientes, Pagos te muestra las transacciones. Si una habitación no sale en la foto, el seguro (la norma) se entera el día del siniestro: en una auditoría, en una vulneración de datos o en un incidente de pagos.

---

## 2. MCU 5.0 en lenguaje de relevamiento

El MCU 5.0 de Agesic organiza el marco en 6 funciones y 72 requisitos. El relevamiento no busca "llenar requisitos": busca **preguntarle al área el dato real** que demuestra cada función.

| Función MCU 5.0 | Pregunta de relevamiento | Área a preguntar | Evidencia típica |
|---|---|---|---|
| GV · Gobernar | ¿Quién decide sobre la seguridad? ¿Qué políticas existen? | Gerencia General, Riesgos, Planificación Estratégica | Resoluciones, políticas, actas del Comité (GV-01…06) |
| ID · Identificar | ¿Qué activos tenemos? ¿Qué riesgos tiene cada uno? | TI, Operaciones, todas las áreas | Inventario de activos (ID-01), análisis de riesgos (ID-03) |
| PR · Proteger | ¿Cómo protegemos los activos? ¿Quién puede acceder? ¿Hay respaldos? | TI, Operaciones, RRHH, Compras | Políticas de accesos (PR-01), cifrado (PR-03), respaldo (PR-05) |
| DE · Detectar | ¿Cómo nos enteramos de que algo anda mal? | TI (Producción, Sistemas) | Monitoreo y logs (DE-01), anomalías (DE-02), pentest (DE-03) |
| RS · Responder | ¿Qué hacemos cuando pasa algo? ¿A quién avisamos? | Riesgos, Comunicación, TI | Plan de respuesta (RS-01), notificación (RS-02), forense (RS-03) |
| RC · Recuperar | ¿Cómo volvemos a operar después del incidente? | TI, Operaciones, Comercial | Continuidad (RC-01), recuperación (RC-02), crisis (RC-03), lecciones (RC-04) |

**Los cuatro requisitos que más vas a tocar en el relevamiento:**

| Requisito | Qué te pide | Dónde se ve en el Banco |
|---|---|---|
| ID.AM · Inventario de activos | Saber qué activos existen y quién es su dueño. | Departamentos de TI y Operaciones: servidores, apps, bases, datos. |
| ID.RA · Evaluación de riesgos | Saber qué puede salir mal y cuánto importa. | Riesgos Financieros y Riesgos No Financieros: metodología y apetito. |
| PR.AT · Concientización | Que las personas sepan cuidar la información. | Capital Humano (Desarrollo de RRHH): planes de capacitación. |
| DE.CM · Monitoreo continuo | Que haya ojos mirando los sistemas todo el día. | TI (Producción y Sistemas): monitoreo, logs, alertas. |

### 2.1 Guion de conversación con un área técnica

Cuando vas a TI, la función ID está en la mesa todo el tiempo. Un guion probado:

> *"Para el inventario de activos (función ID del MCU 5.0) necesitamos un listado de los sistemas que [su departamento] administra: aplicaciones, servidores, bases de datos y las personas que los mantienen. Después queremos entender qué pasaría si cada uno deja de funcionar una hora: eso nos da la criticidad para los riesgos y la continuidad."*

**Cómo convertir la respuesta en evidencia sin incomodar a nadie:**

1. **Pedí el listado** como "insumo", no como "justificación": *"¿nos pueden compartir la planilla de sistemas que ya deben tener?"*.
2. **Validá el uso real**: *"¿alguno de estos sistemas ya no se usa o quedó de un proyecto viejo?"*.
3. **Cerrá con pedido escrito**: cada respuesta importante queda como evidencia pedida, con fecha y responsable.

**Cómo usar estas tablas en la reunión.** Llevá impresa la tabla de la sección 6. Cuando el área responda, marcá la fila, anotá el nombre de quien respondió y la evidencia pendiente. Así la reunión produce trabajo, no charla.

---

## 3. BCU en lenguaje de relevamiento

| Requisito BCU | Dato a relevar | Área | Evidencia |
|---|---|---|---|
| EMG · Estructura de gestión de riesgos | Cómo se gestiona el riesgo operacional y de TIC en el banco. | Riesgos, TI | Marco de riesgo, roles, informes a Dirección. |
| RNRCSF art. 492 · Resguardo de datos/software/documentación | Qué se resguarda, dónde y con qué procedimiento. | TI (Producción), Operaciones | Procedimiento de resguardo, registros de respaldo (PR-05). |
| art. 492 · Copias no afectadas por el mismo evento | Si las copias están separadas físicamente del dato original. | TI (Producción) | Topología de resguardos: sitios, medios, ubicaciones. |
| art. 492 · Claves de desencriptación independientes | Si las claves para recuperar los datos se guardan aparte. | TI, Seguridad | Custodia de claves, quién las guarda, acceso restringido. |
| art. 492 · Pruebas anuales de recuperación e integridad de la totalidad | Que se pruebe recuperar **todo** al menos una vez por año. | TI (Producción), Operaciones | Calendario de pruebas, informes de resultado, fechas. |
| art. 492 · Responsable de categoría superior | Que alguien de nivel jerárquico superior responda por los resguardos. | Gerencia, TI | Designación formal del responsable. |
| Circular 2227 · Riesgo operacional | Identificar y medir los riesgos operativos, incluidos los de TIC. | Riesgos No Financieros | Mapa de riesgos operacionales, base de incidentes, indicadores. |
| Comunicación 2022/254 · Tercerización en el exterior | Conocer qué proveedores procesan datos fuera de Uruguay y con qué controles. | Compras, TI, Jurídico | Contratos, cláusulas, listado de terceros, evaluaciones (PR-08, GV-05). |

> **Ejemplo concreto de "prueba anual de la totalidad":** si le preguntás a Producción "¿prueban las restauraciones?", la respuesta correcta no es "sí, siempre" sino algo como *"una vez por año restauramos la totalidad de los sistemas en el sitio de contingencia y documentamos el resultado"*. Si la respuesta es *"nunca lo hicimos completo, probamos solo lo crítico"*, anotá eso como **brecha BCU** y pasala al plan de tratamiento (ID-04). No es un fracaso del relevamiento: es exactamente lo que viniste a encontrar.

**Mini-encuesta BCU para el relevamiento de TI.** Cinco preguntas que cubren el art. 492 y la Circular 2227 en menos de veinte minutos:

1. ¿Qué datos, software y documentación se resguardan hoy? ¿Hay un inventario de lo resguardado?
2. ¿Dónde están las copias? ¿Están en un lugar que pueda verse afectado por el mismo evento que el original (mismo edificio, misma sala)?
3. ¿Quién guarda las claves de desencriptación de los resguardos? ¿Están separadas de los datos?
4. ¿Prueban la restauración? ¿Una vez por año, sobre la totalidad, con informe documentado?
5. ¿Quién es el responsable formal de los resguardos? ¿Es una persona de categoría superior?

> **Qué hacer con las respuestas:** cada "no" o "en proceso" es una brecha concreta que va directo al plan de tratamiento (ID-04) y a la matriz de correspondencia (MATRIZ-001). No juzgues: registrá. Tu trabajo es que las brechas se vean, no ocultarlas.

---

## 4. URCDP en lenguaje de relevamiento

| Requisito URCDP | Dato a relevar | Área | Evidencia / documento |
|---|---|---|---|
| Registro de tratamientos (ROPA) | Qué bases/datasets existen, con qué finalidad, qué datos contienen, con quién se comparten, plazo de retención. | Todas las áreas con datos personales | URCDP-04 · ROPA |
| Inscripción de bases en el registro público | Qué bases ya están inscritas ante la URCDP y cuáles faltan. | Áreas con datos, Jurídico | Comprobantes de inscripción (URCDP-04) |
| Documento de Seguridad | Medidas de seguridad aplicadas a cada base de datos. | TI, Operaciones, todas las áreas | URCDP-01 |
| Notificación de vulneraciones | Circuito para avisar: URCDP en 24 h y titulares en 72 h. | Riesgos, TI, Comunicación | URCDP-02 |
| EIPD | Evaluación de impacto cuando un tratamiento es riesgoso (datos sensibles, gran escala, nuevas tecnologías). | Riesgos, TI, Jurídico | URCDP-05 |
| Designación del DPD | Quién es el DPD y a quién reporta. | Riesgos / Jurídico | Designación formal (URCDP-06) |

**Datos sensibles que seguro vas a encontrar en el Banco:** datos de salud (si hay certificados o convenios), datos financieros y patrimoniales (crédito, cuentas), datos de morosidad (reportes de deudores), datos de identificación (cédula, domicilio). Cada uno de estos activa requisitos más exigentes de la Ley 18.331 y su decreto reglamentario 64/020.

**Guion de conversación URCDP con un área comercial.** El área comercial no piensa en "tratamientos": piensa en clientes y en trámites. Hablá su idioma:

> *"Para cumplir con la Ley 18.331 necesitamos saber qué datos de los clientes maneja su área: en qué sistemas los ingresa, con quién los comparte (por ejemplo, el Banco En Línea, la URCDP, otros bancos o proveedores) y cuánto tiempo los conserva. Eso lo volcamos en el registro de tratamientos que el banco presenta ante la URCDP. No es un trámite nuevo: es ordenar lo que ya se hace."*

**Qué buscás detrás de la conversación (en términos de URCDP):**

| Lo que te cuentan | Lo que registrás en el ROPA |
|---|---|
| "Ingresamos la solicitud de crédito con cédula, ingresos y bienes". | Base de datos, categoría de datos (identidad, financieros), finalidad. |
| "La consulta al buró la hacemos con un proveedor". | Cesión a tercero, y si está en el exterior: Comunicación 2022/254. |
| "Guardamos el expediente 10 años". | Plazo de retención y base legal de la conservación. |
| "Los datos están en el sistema de préstamos y en planillas de seguimiento". | Sistemas donde vive la base, y si hay copias no controladas. |

---

## 5. El concepto de evidencia

La evidencia es **la huella verificable de que algo se hizo**. No es "lo que me contaron", sino lo que queda registrado y se puede mostrar a un auditor.

Una evidencia de calidad tiene cuatro atributos:

| Atributo | Significado | Ejemplo |
|---|---|---|
| Verificable | Se puede comprobar de forma independiente. | Un log con fecha y usuario, no "lo hacemos todos los días". |
| Fechado | Tiene fecha inequívoca. | Informe de prueba de restauración del 12/03/2026. |
| Trazable | Se puede seguir de principio a fin. | Del pedido al resultado: quién lo pidió, quién lo hizo, qué pasó. |
| Íntegro | No fue alterado. | Versión firmada o protegida, no un archivo "a mano". |

**Relación con INFRA-08.** En el kit, el curso de infraestructura (INFRA-08) trabaja en detalle cómo se releva y se demuestra la infraestructura del banco. Acá tu tarea es entender el **criterio**: qué cuenta como evidencia y qué no. Si la evidencia no se puede verificar, fechar, trazar y conservar íntegra, no es evidencia: es un favor.

**Cómo se pide (adelanto de RELEV-07).** La evidencia se pide por escrito, con la norma que la justifica y con plazo claro:

> *"Estimado/a [nombre]: en el marco del relevamiento del SGSI (MCU 5.0 función ID, RNRCSF art. 492), solicitamos amablemente nos remitan el informe de la última prueba anual de restauración de la totalidad de los sistemas, o la fecha prevista si aún no se realizó. Plazo: 10 días hábiles. Queda registrado en el plan de evidencias del proyecto."*

**Lo que NO es evidencia (y a menudo se ofrece como tal):**

| Te ofrecen | Por qué no es evidencia | Qué pedir en su lugar |
|---|---|---|
| "Lo hacemos todos los días". | No se puede verificar ni fechar. | Un registro o planilla con fechas y responsables. |
| "Te mando una captura de ahora". | No demuestra que se hace de forma sistemática. | El procedimiento documentado y un ejemplo de ejecución fechado. |
| "Preguntale a [persona], él sabe". | El conocimiento de una persona no es registrable. | El documento firmado o la nota oficial. |
| "Está en el sistema, no hace falta papel". | Sin cómo acceder ni conservarlo, no es trazable. | La ruta de acceso y el respaldo de ese sistema. |

**Cómo se registra cada evidencia recibida.** Al recibirla, anotá en la planilla: código de la evidencia, documento del kit que alimenta, requisito que demuestra, fecha de recepción y responsable. Ese registro es tu mapa de cumplimiento para el cierre (RELEV-11) y para la matriz MATRIZ-001.

---

## 6. Tabla maestra de traducción: requisito → pregunta → documento → evidencia

Usá esta tabla como checklist al preparar cada reunión. Cada fila es una pregunta que le vas a hacer a un área y una evidencia que vas a pedir.

| Requisito | Pregunta exacta para el área | Documento del kit que alimenta | Evidencia esperada |
|---|---|---|---|
| ID.AM · Inventario | ¿Me pueden listar los activos de información de su área (sistemas, bases, datos, contratos, instalaciones)? | ID-01 | Inventario o planilla de activos; ficha de activo firmada |
| ID.RA · Riesgos | ¿Qué podría salir mal con estos activos y quién evalúa ese riesgo? | ID-02, ID-03 | Metodología de riesgo, mapa de riesgos |
| ID.AM + URCDP | ¿Qué bases de datos personales tiene su área y para qué? | URCDP-04 (ROPA) | Listado de bases, finalidad, responsable |
| PR-01 · Accesos | ¿Quién decide quién accede a cada sistema? ¿Quién revoca cuando alguien se va? | PR-01 | Procedimiento de altas/bajas, solicitudes de acceso |
| PR-02 · Concientización | ¿Qué capacitación de seguridad reciben las personas y cada cuánto? | PR-02 | Plan de capacitación, registros de asistencia |
| PR-03 · Datos/cifrado | ¿Dónde se almacenan datos sensibles y cómo se protegen (cifrado, controles de acceso)? | PR-03 | Política de cifrado, listado de sistemas con datos sensibles |
| PR-04 · Seguridad física | ¿Cómo se protegen físicamente los servidores, los archivos y las sucursales? | PR-04 | Procedimiento de acceso a salas, control de visitas |
| PR-05 · Respaldo | ¿Qué se resguarda, con qué frecuencia y dónde se guardan las copias? | PR-05 | Procedimiento y registros de respaldo |
| art. 492 · Pruebas anuales | ¿Prueban la restauración de la totalidad una vez por año? ¿Dónde está el informe? | BCU-01 | Informe de prueba anual de restauración |
| art. 492 · Claves independientes | ¿Quién custodia las claves de desencriptación y están separadas de los datos? | BCU-01 | Procedimiento de custodia de claves |
| DE.CM · Monitoreo | ¿Qué se monitorea y quién revisa las alertas? | DE-01, DE-02 | Logs, consolas, registros de incidentes |
| RS.CO · Notificación | ¿A quién se avisa ante un incidente y en qué plazo? | RS-02, URCDP-02 | Circuito de notificación, planilla de incidentes |
| RC.RP · Recuperación | ¿Cómo se recupera la operación tras una caída? ¿Qué procesos son críticos? | RC-01, RC-02 | BIA/BCP, DRP, pruebas de continuidad |
| PR-08 · Terceros | ¿Qué proveedores acceden a sus datos o sistemas? ¿Hay contrato y evaluación? | PR-08, GV-05 | Listado de terceros, contratos, evaluaciones |
| C. 2022/254 · Exterior | ¿Algún proveedor procesa datos fuera de Uruguay? ¿Qué garantías hay? | PR-08 | Contratos con cláusulas, notificaciones a URCDP |
| BCU EMG | ¿Cómo se informa el riesgo operacional a la Dirección? | GV-06, BCU-01 | Informes de riesgo a Directorio, actas |
| URCDP-01 | ¿Cuáles son las medidas de seguridad de cada base de datos? | URCDP-01 | Documento de Seguridad por base |
| URCDP-02 | ¿Cuál es el procedimiento si hay una vulneración de datos personales? | URCDP-02 | Procedimiento, plantilla de notificación 24 h/72 h |
| RC-03 · Crisis | ¿Cómo se comunica internamente un incidente grave? ¿Quién habla con la prensa y el Directorio? | RC-03, GV-06 | Protocolo de comunicación de crisis |
| PR-06 · Vulnerabilidades | ¿Cómo se detectan y corrigen las vulnerabilidades? ¿Hay proceso de parches? | PR-06 | Inventario de vulnerabilidades, registro de parches |
| PR-07 · Desarrollo seguro | ¿Se siguen buenas prácticas de desarrollo seguro en las aplicaciones propias? | PR-07 | Guía de desarrollo, revisiones de código |
| RC-04 · Lecciones | ¿Se documentan las lecciones aprendidas de cada incidente? | RC-04 | Informes de lecciones, actas de revisión |
| URCDP-05 · EIPD | ¿Hubo alguna evaluación de impacto para tratamientos nuevos o sensibles? | URCDP-05 | Informe de EIPD, decisiones del DPD |
| DE-03 · Pentest | ¿Se realizan pruebas de intrusión sobre los sistemas críticos? ¿Cada cuánto? | DE-03 | Informes de pentest, alcance y fechas |
| GV-05 · Suministro | ¿Cómo se gestionan los riesgos de la cadena de suministro y los proveedores críticos? | GV-05 | Evaluación de proveedores, continuidad de suministro |

### 6.1 Un requisito, de principio a fin (ejemplo guiado)

Tomemos el requisito **"pruebas anuales de recuperación e integridad de la totalidad"** (RNRCSF art. 492) y recorramos todo el camino:

1. **Traducción normativa → pregunta:** de la sección 3 ya tenemos la pregunta: *"¿Prueban la restauración de la totalidad una vez por año?"*.
2. **A quién:** Gerente de Producción (TI).
3. **Qué se espera escuchar:** el procedimiento de resguardo y el calendario de pruebas de restauración.
4. **Evidencia pedida:** informe de la última prueba anual, con fecha, alcance y resultado.
5. **Dónde se registra:** planilla de evidencias y carpeta correspondiente (EST-CARPETAS-001).
6. **Qué documento del kit alimenta:** BCU-01 (resguardos) y MATRIZ-001 (correspondencia).
7. **Qué pasa si no hay evidencia:** la brecha entra al plan de tratamiento (ID-04) con prioridad alta, porque es una exigencia explícita del BCU.

**Repetí este ciclo para cada fila de la tabla maestra** y el relevamiento deja de ser "juntar papeles" y se convierte en un mapa de cumplimiento que se cierra en la correspondencia normativa (RELEV-11).

---

## 7. Errores comunes

- **Preguntar la norma en vez del dato**: "¿Cumplen el MCU 5.0?" es una mala pregunta. "¿Dónde guardan las copias de resguardo y cada cuánto prueban restaurarlas?" es la pregunta que produce evidencia.
- **Confundir conversación con evidencia**: lo que te cuentan en la reunión es el mapa; la evidencia es lo que te remiten por escrito. Nunca cierres la reunión sin un pedido de evidencia registrado.
- **Relevar solo lo que las áreas quieren mostrar**: pedí siempre el listado completo y después validá con el uso real (una base que "no existe" en el papel puede aparecer en un sistema productivo).
- **No distinguir dato personal de dato técnico**: la base de clientes es a la vez un activo ID.AM y un tratamiento URCDP. Si la relevás solo como tecnología, se te pierde el requisito de protección de datos.
- **Prometer plazos que no podés cumplir**: cada pedido de evidencia tiene plazo; cada plazo vencido sin seguimiento destruye tu credibilidad con el área.
- **Guardar las evidencias en tu cabeza**: todo se registra el mismo día en la planilla de evidencias y en la carpeta correspondiente (EST-CARPETAS-001).

### Lista de verificación del módulo

- ☐ Expliqué cada norma (MCU 5.0, BCU, URCDP) en términos de "pregunta + evidencia".
- ☐ Tengo las tablas de traducción a mano para cada reunión.
- ☐ Sé distinguir una evidencia válida de un favor.
- ☐ Preparé la plantilla del pedido escrito de evidencias.
- ☐ Identifiqué los requisitos que más se van a cumplir como brechas (art. 492, ROPA, concientización).

---

**Documentos relacionados:** MATRIZ-001, ID-05, GV-02, ID-01, ID-03, BCU-01, URCDP-01, URCDP-04
