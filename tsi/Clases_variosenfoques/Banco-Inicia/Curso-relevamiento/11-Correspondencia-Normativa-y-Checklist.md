# RELEV-11 · Correspondencia normativa y checklist final

**Verificar contra el organigrama vigente:** los nombres y cargos mencionados en este módulo corresponden al organigrama de abril 2026. Antes de usarlos en la matriz de correspondencia, en el checklist o en el informe final, confirmalos contra la versión vigente publicada por el Banco: los cargos rotan y los nombres cambian sin aviso.

> **Función del MCU 5.0:** este módulo integra las seis funciones GV/ID/PR/DE/RS/RC en una sola vista: demuestra que el relevamiento alimentó cada función (ID.AM, ID.RA, ID.IM, PR.AT, PR.DS, DE.CM, RS.CO, RC.RP) y que el SGSI no tiene eslabones vacíos.
> **ISO/IEC 27001:** la matriz de correspondencia es la evidencia de la cláusula 4 (contexto) y del anexo A: cada requisito de la norma debe poder mostrar dónde se relevó y dónde quedó registrado.
> **BCU:** la matriz sustenta el EMG, el RNRCSF art. 492, la Circular 2227 (riesgo operacional) y los controles de tercerización: el banco puede demostrar qué relevó, qué tiene y qué le falta.
> **URCDP:** la correspondencia cierra el circuito de la Ley 18.331 y la Ley 19.670: ROPA (URCDP-04), notificaciones (URCDP-02), EIPD (URCDP-05) y Documento de Seguridad (URCDP-01).
> **Nivel del curso:** 🟢 Descubrir · 🟡 Practicar · 🔴 **Dominar**

---

## 1. La tabla maestra final

Este es el corazón del cierre: una sola tabla que cruza **cada requisito normativo** con **el área relevada**, **la evidencia obtenida**, **el documento del kit** donde quedó registrado y **el estado**. Cuando esta tabla esté completa, el relevamiento estará demostrado ante cualquier auditor.

Cómo se completa y se lee:

- **Requisito:** el texto literal o abreviado de la norma (MCU 5.0, BCU, URCDP).
- **Área relevada:** la división/departamento del organigrama (verificado) donde se relevó.
- **Evidencia obtenida:** el archivo, el dato o el documento que lo demuestra (RELEV-07).
- **Documento del kit:** el código del kit Banco-Inicia donde quedó registrado (RELEV-08).
- **Estado:** ☐ pendiente de relevar/obtener · ☑ completo con evidencia registrada.

### 1.1 Requisitos del MCU 5.0 (Agesic)

| Requisito | Área relevada | Evidencia obtenida | Documento del kit | Estado |
|---|---|---|---|---|
| ID.AM — Inventario de activos | División TI, División Operaciones, División Canales | Inventario de sistemas, equipos, bases y redes | ID-01 | ☑ |
| ID.AM — Activos de información en territorio | Sucursales y Servicios Generales | Listado de terminales y archivos por sucursal | ID-01 | ☑ |
| ID.RA — Evaluación de riesgos | Área Riesgos (Riesgos No Financieros) | Metodología y análisis por activo | ID-02, ID-03 | ☑ |
| ID.IM — Impacto del negocio | Áreas dueñas de cada proceso | Matriz de impacto de procesos críticos | ID-03 | ☑ |
| PR.AT — Concientización del personal | División Capital Humano | Plan de capacitación y registro de asistencia | PR-02 | ☑ |
| PR.DS — Protección de datos | División TI, DPD | Controles de bases y accesos, cifrado | PR-06, URCDP-01 | ☑ |
| DE.CM — Monitoreo continuo | División TI (Soporte y Producción) | Registro de monitoreo e incidentes | DE-01, DE-02 | ☑ |
| RS.CO — Comunicación de respuesta | Área Riesgos, RSI | Procedimiento de notificación interna | RS-01, RC-03 | ☑ |
| RC.RP — Recuperación | División TI (Producción) | Plan de resguardo y restauración | RC-01, RC-04 | ☑ |

### 1.2 Requisitos del BCU

| Requisito | Área relevada | Evidencia obtenida | Documento del kit | Estado |
|---|---|---|---|---|
| EMG — Gobierno de riesgos y control interno | Directorio, Gerencia General, Área Riesgos | Actas, informes del RSI, organigrama vigente | GV-01…06, BCU-01 | ☑ |
| RNRCSF art. 492 — Gestión de riesgos de TIC | RSI, División TI, Auditoría Interna | Informe del RSI y plan de 18 meses | BCU-02, PLAN-SGSI-001 | ☑ |
| Circular 2227 — Riesgo operacional | División Operaciones, Sistema de Pagos | Procedimientos y registro de eventos | BCU-03, DE-01 | ☑ |
| Riesgo operacional — Continuidad del negocio | División TI, División Operaciones | Plan de continuidad y pruebas | RC-01…04, BCU-04 | ☑ |
| Tercerización y cadena de suministro | Compras y Contrataciones, División Administración | Contratos con terceros y cláusulas de seguridad | GV-05, BCU-06 | ☑ |
| Verificación independiente | Auditoría Interna | Plan de verificación y hallazgos | BCU-05 | ☐ |

### 1.3 Requisitos de la URCDP

| Requisito | Área relevada | Evidencia obtenida | Documento del kit | Estado |
|---|---|---|---|---|
| Documento de Seguridad | RSI, DPD, División TI | Medidas de seguridad documentadas | URCDP-01 | ☑ |
| Registro de tratamientos (ROPA) | Todas las áreas con datos personales | Mapa de bases y finalidades | URCDP-04 | ☑ |
| Inscripción de bases ante URCDP | DPD, División TI | Comunicaciones de inscripción | URCDP-04 | ☐ |
| Notificación de vulneraciones | RSI, DPD, Área Riesgos | Procedimiento 24 h/72 h (art. 38) | URCDP-02 | ☑ |
| EIPD — Evaluación de impacto | DPD, áreas con datos sensibles | Evaluaciones de impacto realizadas | URCDP-05 | ☐ |
| Derechos ARCO | Canales de Atención, DPD | Procedimiento de atención al titular | URCDP-03 | ☑ |
| Delegado de Protección de Datos | RSI, DPD | Designación y funciones documentadas | URCDP-06 | ☑ |

> **Cómo usar esta tabla:** es la entrada principal de la **MATRIZ-001** (Matriz de Correspondencia Normativa del kit). Las filas en estado ☐ son las prioridades de las siguientes fases del plan de 18 meses (sección 3): no son fracasos, son el plan de trabajo.

### 1.4 Cómo construir la tabla paso a paso

La tabla maestra no se llena de una sentada: se construye mientras se releva y se completa al cierre. Este es el orden de trabajo recomendado:

| Paso | Qué hacer | Cuándo |
|---|---|---|
| 1 | Listá los requisitos normativos aplicables por norma (MCU 5.0, BCU, URCDP). | Al inicio, con RELEV-02 |
| 2 | Asigná cada requisito al área donde se puede evidenciar. | Con el mapa de actores (RELEV-01, RELEV-04) |
| 3 | Incorporá a la fila la evidencia solicitada en RELEV-07 y la reunión que la pidió. | Durante el ciclo de reuniones |
| 4 | Registrá el documento del kit donde la evidencia quedó guardada (RELEV-08). | Durante el registro |
| 5 | Marcá ☑ solo cuando exista el archivo recibido y verificado. | Al cierre, con la planilla de RELEV-09 |
| 6 | Pasá las filas en ☐ a la lista de prioridades de la siguiente fase. | En el informe final al Comité |

Esta secuencia garantiza que ninguna fila se llene "a ojo": cada celda nace de una reunión real, de una evidencia pedida por escrito y de un archivo registrado. Una fila completa sin ese recorrido es una declaración sin respaldo, que es exactamente lo que una auditoría de la URCDP, del BCU o de Agesic va a impugnar.

> **Regla de la trazabilidad:** todo el que lea la tabla maestra debe poder seguir el rastro de una fila: del requisito a la reunión (RELEV-06), de la reunión a la evidencia (RELEV-07) y de la evidencia al documento del kit (RELEV-08). Si el rastro se corta en algún punto, la fila vuelve a estado ☐ pendiente.

---

## 2. El checklist de cierre del relevamiento

El cierre se verifica con dos checklists: uno **por área** y otro **por documento del kit**. Ninguna se cierra con buena fe: se cierra con archivo recibido y registrado.

### 2.1 Checklist por área

Para cada área relevada (cada división/departamento del organigrama vigente):

- ☐ Se relevó el área según el dossier de RELEV-04.
- ☐ Se realizó la reunión de relevamiento (RELEV-06) con minuta firmada/validada.
- ☐ Se obtuvo la evidencia solicitada en RELEV-07.
- ☐ Se registró lo relevado en el documento del kit correspondiente (RELEV-08).
- ☐ Se cerró el área con minuta de cierre y se comunicó el resumen (RELEV-10).
- ☐ Los pendientes del área se registraron en la planilla de compromisos con causa (RELEV-09).
- ☐ Los pendientes sin resolver se mapearon como riesgo en ID-03.

### 2.2 Checklist por documento del kit

- ☐ ID-01: inventario de activos con sistemas, bases, equipos, redes y archivos por área.
- ☐ ID-02: metodología de riesgos aprobada y aplicada.
- ☐ ID-03: análisis de riesgos de los activos críticos.
- ☐ ID-04: plan de tratamiento con responsables y fechas (los compromisos de RELEV-09 alimentan este plan).
- ☐ ID-05: perfil de ciberseguridad institucional según MCU 5.0.
- ☐ GV-02: alcance del SGSI confirmado con lo relevado.
- ☐ GV-06: insumos para el informe semestral del RSI a Dirección.
- ☐ PR-02: insumos para el programa de concientización.
- ☐ DE-01/DE-02: insumos para monitoreo y gestión de incidentes.
- ☐ URCDP-01: Documento de Seguridad con las medidas relevadas.
- ☐ URCDP-04: bases de datos personales identificadas para inscripción y ROPA.
- ☐ URCDP-05: lista de tratamientos que requieren EIPD.
- ☐ MATRIZ-001: matriz de correspondencia normativa completa con la tabla de la sección 1.
- ☐ PLAN-SGSI-001: avance de las fases del plan actualizado al cierre.

> **Regla del 100 %:** un área puede cerrarse con pendientes, pero no puede cerrarse sin registro. El checklist se marca ☑ cuando existe el archivo, no cuando "el área prometió".

---

## 3. Cómo encaja este curso en el plan general (PLAN-SGSI-001)

El curso de relevamiento no es un apéndice: es el **motor de las fases de identificación** del plan de 18 meses. Cada fase consume los módulos que la alimentan.

| Fase del PLAN-SGSI-001 | Qué hace | Módulos que la alimentan | Documento que produce |
|---|---|---|---|
| F0 · Gobierno | Formaliza el proyecto, rol del RSI, Comité. | RELEV-00, RELEV-01 | GV-01…03, PLAN-SGSI-001 |
| F1 · Diagnóstico | Conoce la organización y su contexto. | RELEV-01, RELEV-02 | GV-02, MATRIZ-001 |
| F3 · Activos y riesgos | Inventaría activos y evalúa riesgos. | RELEV-03…08 | ID-01…04 |
| F8 · URCDP | Cumplimiento de datos personales. | RELEV-04, RELEV-08, RELEV-11 | URCDP-01…06 |
| F9 · BCU | Cumplimiento BCU y riesgo operacional. | RELEV-02, RELEV-11 | BCU-01…06 |
| F10 · Verificar | Auditoría interna y mejora. | RELEV-09, RELEV-11 | BCU-05, GV-06 |

- **F0** necesita a RELEV-00 y RELEV-01 para formalizar el proyecto y conocer el banco.
- **F1** necesita a RELEV-02 para traducir la norma al territorio antes de salir a relevar.
- **F3** consume todo el ciclo operativo (RELEV-03 → 08): agenda, dossiers, reuniones, evidencias y registro.
- **F8 y F9** reciben de RELEV-04 (qué relevar por área) y RELEV-11 (cómo demostrar el cumplimiento).
- **F10** recibe de RELEV-09 y RELEV-11 el material para que Auditoría Interna verifique (BCU-05).

> **Lección clave:** el relevamiento no termina cuando la agenda de 12 semanas termina. Termina cuando cada fase del plan que consume información de territorio tiene la suya. Si la fase F8 (URCDP) no tiene inscripciones, el relevamiento de datos personales está incompleto, aunque las reuniones hayan terminado.

---

## 4. Indicadores del relevamiento

Lo que no se mide no se gestiona. Estos son los indicadores mínimos del relevamiento, con su fórmula, su fuente y su destino.

| Indicador | Cómo se mide | Fuente | Dónde se reporta |
|---|---|---|---|
| Áreas relevadas | Cantidad de áreas con reunión y minuta cerrada / total del alcance | Planilla de reuniones (RELEV-03) | Informe mensual, GV-06 |
| Activos inventariados | Cantidad de registros en ID-01 | ID-01 | Informe mensual, Comité |
| Bases de datos personales registradas | Cantidad de bases en URCDP-04 / ROPA | URCDP-04 | DPD, GV-06 |
| % de evidencias obtenidas | Evidencias recibidas / evidencias solicitadas × 100 | Planilla de compromisos (RELEV-09) | Informe mensual |
| Brechas detectadas | Cantidad de brechas por área registradas | Minutas e ID-03 | Informe final, Comité |
| Compromisos abiertos | Cantidad de compromisos sin cerrar con fecha | Planilla de compromisos | Informe mensual |

Reglas de medición:

- **Mismo día de la reunión:** los datos se cargan el mismo día, no "cuando haya tiempo". La planilla viva es la fuente; el informe mensual solo la resume.
- **Tendencia, no fotos:** un indicador suelto no dice nada. "Evidencias recibidas por mes" subiendo es mejor noticia que un número alto en un mes.
- **Reporte mensual simple:** tres cifras en el informe (reuniones, evidencias, compromisos) valen más que un tablero de 20 indicadores que nadie mantiene.
- **Los indicadores alimentan GV-06:** el informe semestral del RSI a Dirección se construye con estos números: son la prueba de gestión que pide el BCU.

---

## 5. Qué sigue después del relevamiento

El relevamiento es la puerta de entrada; las siguientes etapas consumen lo relevado. Este es el orden recomendado, cada paso con su documento del kit:

| Siguiente paso | Qué hace | Documento | Prioridad |
|---|---|---|---|
| Evaluación de riesgos | Aplicar la metodología ID-02 a los activos inventariados. | ID-03 | Alta |
| Plan de tratamiento | Priorizar y asignar responsables y fechas a los riesgos. | ID-04 | Alta |
| Inscripción de bases ante URCDP | Comunicar y registrar las bases con datos personales. | URCDP-04 | Alta |
| Perfil de ciberseguridad | Evaluar el nivel de madurez contra MCU 5.0. | ID-05 | Media |
| Programa de concientización | Diseñar y ejecutar PR-02 con lo detectado. | PR-02 | Media |
| Verificación con Auditoría Interna | Que la 3ª línea valide el SGSI. | BCU-05 | Media |
| Revisión por la dirección | Informe semestral del RSI con resultados. | GV-06 | Periódica |

> **La regla de la continuidad:** cada documento del kit que se completa en estas etapas debe poder rastrearse hasta una evidencia del relevamiento. Si un riesgo de ID-03 no tiene detrás un dato relevado, ese riesgo es una opinión, no un análisis.

---

## 6. Mantenimiento y segunda vuelta

El relevamiento no es una campaña única: es una **actividad periódica**. El territorio cambia y el inventario envejece.

### 6.1 Cuándo se actualiza

- **Revisión anual:** ciclo completo o actualización dirigida, según el plan (GV-04, PLAN-SGSI-001).
- **Cambio de negocio:** nuevo producto, nueva línea de crédito, nuevo canal de atención.
- **Nuevo sistema:** alta o baja de un sistema, una base o una plataforma.
- **Reorganización:** cambios de estructura, de responsables o de ubicación de los datos.
- **Incidente relevante:** después de un incidente o una brecha, se vuelve a relevar la zona afectada.
- **Cambio normativo:** nueva circular del BCU, actualización del MCU o modificación de la normativa de la URCDP.

### 6.2 Cómo programar la segunda vuelta

- **Calendario fijo:** la revisión anual se agenda en el plan anual (GV-04) con fecha y responsable, y se informa al Comité.
- **Gatillos automáticos:** cada alta de sistema o reorganización dispara una actualización mínima de ID-01 y URCDP-04.
- **Responsables:** el RSI coordina; los referentes por área (los embajadores de RELEV-10) ejecutan la actualización en su área; el DPD valida lo de datos personales.

### 6.3 Quién la ejecuta

| Tarea | Responsable |
|---|---|
| Coordinación y planilla de la segunda vuelta | RSI |
| Actualización del inventario de su área | Referente del área |
| Validación de datos personales | DPD |
| Revisión de metodología y riesgos | Área Riesgos No Financieros |
| Verificación independiente | Auditoría Interna (BCU-05) |

> **Consejo de cierre:** guardá los dossiers y minutas de la primera vuelta (RELEV-04, RELEV-06). La segunda vuelta no parte de cero: parte de "qué cambió desde la última vez". Eso la hace más rápida, más barata y mucho más creíble.

---

## 7. Errores comunes

- **Tabla maestra incompleta o en jerga**: llenar la matriz solo con códigos de norma sin evidencia real. Cada fila necesita su área, su evidencia y su documento del kit.
- **Marcar ☑ sin archivo**: el estado "completo" sin la evidencia guardada es una mentira que la auditoría va a encontrar.
- **Cerrar por reuniones, no por documentos**: "nos vimos con todos" no es cierre; es el principio del cierre.
- **Olvidar los gatillos de actualización**: no programar la segunda vuelta ni los disparadores (nuevo sistema, reorganización) deja el inventario muerto a los 6 meses.
- **Medir sin fuente**: indicadores que nadie carga o que se calculan dos veces distinto. La planilla viva es la fuente única.
- **Entregar sin socializar**: presentar la matriz final al Comité sin que las áreas hayan visto su fila. Las sorpresas generan defensivas y la matriz pierde validez.
- **No conectar con el plan**: el relevamiento que no alimenta las fases F3/F8/F9 es un ejercicio intelectual. Todo lo relevado debe aterrizar en ID-03, URCDP-04 y BCU-05.
- **Confiar en el organigrama viejo**: usar nombres y cargos no verificados invalida la matriz de un golpe. Verificá contra el organigrama vigente antes de firmar el informe final.

---

**Documentos relacionados:** MATRIZ-001, ID-05, BCU-05, GV-06, URCDP-04, EV-01, EV-02, EV-04, EV-05
