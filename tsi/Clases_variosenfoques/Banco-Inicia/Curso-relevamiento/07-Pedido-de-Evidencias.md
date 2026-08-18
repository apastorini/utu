# RELEV-07 · Pedido de evidencias: qué, cómo y cuándo

> **Función del MCU 5.0:** La evidencia es el combustible de la función RS (Responder) y el soporte de ID (Identificar): los controles solo se demuestran con registros verificables. PR.AT (concientización) y DE.CM (monitoreo) se auditan con lo que las áreas entregan, no con lo que declaran.
> **ISO/IEC 27001:** La cláusula 9 (evaluación del desempeño) y la auditoría del sistema (cláusula 9.2) exigen información documentada y trazable: la evidencia relevada sostiene la declaración de aplicabilidad (Anexo A) y el reporte a la dirección.
> **BCU:** El RNRCSF art. 492 (resguardo de datos, software y documentación) y el EMG se demuestran con evidencias: copias de respaldo, pruebas anuales de recuperación e integridad, claves de desencriptación independientes y responsables de categoría superior.
> **URCDP:** La Ley 19.670 y el Decreto 64/020 exigen poder demostrar las medidas de seguridad implementadas: contratos de encargados, EIPD, notificaciones y el Documento de Seguridad (URCDP-01) se prueban con evidencia.
> **Nivel del curso:** 🟢 Descubrir · 🟡 Practicar · 🔴 Dominar

---

## 1. ¿Qué es evidencia útil?

La evidencia no es cualquier documento: es un **registro verificable, fechado, trazable e íntegro** que demuestra que un control existe, que se ejecuta y que queda documentado. El curso hermano **INFRA-08 · Evidencias a presentar** define el estándar de las evidencias del kit; este módulo explica cómo pedirlas en el relevamiento.

### 1.1 Los cuatro atributos de la evidencia

| Atributo | Qué significa | Pregunta de validación |
|---|---|---|
| Verificable | Puede comprobarse con datos objetivos (fechas, valores, nombres) | ¿Se puede cotejar con otra fuente? |
| Fechado | Tiene fecha de generación y de entrega | ¿Cuándo se generó este registro? |
| Trazable | Se sabe quién lo generó, desde qué sistema y para qué proceso | ¿Quién y con qué sistema lo produjo? |
| Íntegro | No fue alterado en el tránsito ni en el archivo | ¿Hay control de versiones y de cambios? |

### 1.2 La prioridad de las evidencias

No todas las evidencias valen lo mismo. Cuando diseñes el pedido, priorizá así:

1. **Evidencia que se genera sola** (logs, configuraciones, reportes automáticos de sistemas): es la más valiosa porque refleja la operación real, sin intervención humana ni "maquillaje".
2. **Evidencia que hay que armar** (informes, procedimientos, instructivos): es útil pero debe generarse con fecha, responsable y control de cambios.
3. **Evidencia testimonial** (lo que dijo una persona): solo como apoyo, nunca como prueba principal.

> **Regla de oro:** **no inventes evidencias.** Si un control no tiene registro, la brecha se registra como tal (alimenta ID-02, ID-03 e ID-05). Fabricar una evidencia es el peor error del SGSI: convierte una brecha solucionable en un hallazgo grave de auditoría.

### 1.3 Relación con INFRA-08

El curso **INFRA-08 · Evidencias a presentar** lista los formatos y contenidos mínimos de las evidencias de infraestructura (configuraciones, respaldos, monitoreo, parches). Cuando pidas evidencia técnica, usá la nomenclatura y los formatos de INFRA-08 para que todo el kit hable el mismo idioma.

> **Recordá verificar contra el organigrama vigente del Banco**: el pedido formal debe dirigirse al área correcta y con el nombre correcto de su responsable; un pedido a un área que ya cambió de nombre o de jefatura se pierde o se demora.

---

## 2. ¿Qué pedir por documento del kit?

La tabla de abajo es la columna vertebral de tu ciclo de pedidos. Usala como punto de partida y adaptala a cada área. Cada fila indica qué evidencia pedir, en qué formato y qué área la tiene.

| Documento del kit | Evidencia a pedir | Formato sugerido | Área que la tiene |
|---|---|---|---|
| ID-01 (Inventario) | Diagramas de red y arquitectura; listados de sistemas | PDF / Visio / diagrama exportado | Depto. Sistemas, Depto. Producción |
| ID-01 (Inventario) | Inventarios de equipos y activos existentes | Planilla XLSX con fecha | Depto. Soporte Técnico |
| ID-02/ID-03 (Riesgos) | Reportes de disponibilidad y eventos de los últimos 12 meses | PDF de reporte automático | Depto. Producción |
| ID-03 (Riesgos) | Registro de incidentes y resolución | Ticket / planilla de incidentes | Depto. Soporte Técnico |
| PR-01 (política de acceso) | Listados de accesos por usuario y por sistema | XLSX anonimizado, con fecha de corte | Depto. Sistemas |
| PR-02 (roles) | Matriz de roles y funciones aprobada | XLSX / PDF firmado | Depto. Capital Humano, Depto. Sistemas |
| PR-05 (restauración) | Registros de pruebas de restauración de respaldos | PDF con fechas y resultado | Depto. Producción |
| PR-06 (parches) | Reportes de parches aplicados y escaneos de vulnerabilidad | PDF / XLSX con fecha | Depto. Sistemas |
| PR-07 (antivirus/EDR) | Reporte de cobertura y de detecciones | PDF / dashboard exportado | Depto. Soporte Técnico |
| PR-08 (terceros) | Contratos con cláusulas de seguridad de la información | PDF del contrato (cláusulas relevantes) | División Servicios Jurídicos Notariales |
| DE-01 (detección) | Cobertura de logs y configuraciones de SIEM | PDF / captura de consola | Depto. Producción, Depto. Sistemas |
| DE-02 (monitoreo) | Reportes de monitoreo y alarmas de los últimos 6 meses | PDF | Depto. Producción |
| RS-01 (respuesta) | Planes de respuesta a incidentes y ejercicios realizados | PDF con fecha de ejercicio | Depto. Soporte Técnico |
| RC-01 (recuperación) | Planes de contingencia y continuidad | PDF | Depto. Procesos, Depto. Producción |
| BCU-06 (continuidad) | Planes de contingencia, pruebas y resultados | PDF firmado | División Operaciones |
| GV-05 (terceros) | Registro de contratos con proveedores de TI | XLSX | División Administración General |
| URCDP-04 (ROPA) | Listado de bases de datos personales y sus finalidades | XLSX / ROPA | Depto. Información y Apoyo Comercial |
| URCDP-01 (Doc. Seguridad) | Inventario de medidas de seguridad declaradas vs reales | XLSX / PDF | RSI, Oficial de Cumplimiento |

### Cómo leer la tabla

- **Un documento del kit, varias evidencias:** el inventario (ID-01) se sostiene con diagramas, listados y fichas; no con un solo archivo.
- **Una evidencia, varios documentos:** un reporte de disponibilidad sirve a la vez para ID-03 (riesgos) y para BCU-06 (continuidad). Pedilo una sola vez y enlazalo.
- **Área correcta:** la evidencia vive en el área que la genera, no en la que la consume. El que opera el respaldo es Producción; el que firma el contrato es Jurídica.

---

## 3. ¿Cómo pedirlo?

El pedido de evidencias **siempre por escrito**, con correo formal o memorando. Un pedido verbal no deja rastro, no tiene fecha y no se puede hacer seguimiento. La estructura del pedido es siempre la misma:

### 3.1 Estructura del pedido

1. **Referencia normativa:** qué norma o documento del kit motiva el pedido (MCU 5.0, BCU, URCDP, ID-01, etc.).
2. **Lista exacta de ítems:** qué evidencias concretas se piden, con nombre y alcance.
3. **Formato aceptable:** PDF, XLSX, captura de consola, etc.
4. **Fecha límite:** fecha de entrega comprometida.
5. **A quién entregar:** persona y canal de recepción.
6. **Para qué se usará:** finalidad del SGSI (evitar suspicacias).
7. **Compromiso de confidencialidad:** qué se hará con la evidencia y quién la custodiará.

### 3.2 Plantilla de correo de pedido de evidencias

```text
Asunto: Pedido formal de evidencias SGSI · [División/Área] · Vence [fecha]

Estimado/a [Nombre] [Apellido]:

En el marco del proyecto de SGSI del Banco y de la reunión de
relevamiento del [fecha], y en cumplimiento de lo dispuesto por
[referencia normativa: MCU 5.0 Agesic · EMG/RNRCSF BCU · Ley 19.670
URCDP], te solicito formalmente la entrega de las siguientes
evidencias:

1. [Ítem 1 — nombre exacto y alcance]
   Ej.: "Reporte de parches aplicados al servidor X del core, con
   cobertura del trimestre enero–marzo 2026."
2. [Ítem 2]
3. [Ítem 3]

Formato aceptable: [PDF / XLSX / captura de consola / documento firmado]

Fecha límite de entrega: [DD/MM/AAAA]

Forma de entrega: [correo a la casilla del RSI / carpeta compartida
del proyecto / entrega física en Oficina de Cumplimiento]

Uso de la información: las evidencias se utilizarán exclusivamente
para sustentar el cumplimiento del SGSI del Banco, serán custodiadas
por [RSI / Oficina de Cumplimiento] en el repositorio del proyecto
(EST-CARPETAS-001) y no se divulgarán fuera del alcance normativo.

Quedo a disposición para coordinar la entrega y para recibir tu
consulta sobre cualquier ítem.

Saludos cordiales,
[Nombre del RSI / facilitador] · Banco
```

### 3.3 Cuándo pedir

- **Después de la reunión de relevamiento** (RELEV-06): la evidencia que el área prometió se formaliza dentro de los 2 a 5 días hábiles posteriores.
- **Con fecha de corte clara:** toda evidencia se pide con alcance temporal ("últimos 12 meses", "trimestre en curso") para que sea comparable y verificable.
- **Con recordatorio a mitad del plazo:** no esperes el último día para saber si la entrega está en riesgo. Un recordatorio a los 3-5 días suele destrabar las demoras.

---

## 4. Registro de solicitudes: la planilla de seguimiento

Cada pedido de evidencia se registra en una planilla única. Es tu radar de proyecto: sin esta planilla no sabés qué se pidió, qué falta, qué venció y qué quedó como brecha.

### Plantilla de planilla de seguimiento de evidencias

```text
PLANILLA DE SEGUIMIENTO DE EVIDENCIAS · SGSI Banco
================================================

| ID solicitud | Documento del kit | Ítem pedido | Solicitado a | Fecha de solicitud | Fecha límite | Estado | Ubicación en el repositorio |
|--------------|-------------------|-------------|--------------|--------------------|--------------|--------|-----------------------------|
| EV-001       | ID-01             | Diagrama de red del área | Depto. Sistemas | 10/03/2026 | 24/03/2026 | Recibida | 01-IDENTIFICACION/ID-01/diagramas/ |
| EV-002       | URCDP-04          | Listado de bases y finalidades | Depto. Información y Apoyo Comercial | 10/03/2026 | 24/03/2026 | Solicitada | 06-CUMPLIMIENTO/URCDP/ROPA/ |
| EV-003       | BCU-06            | Resultado de prueba anual de recuperación | Depto. Producción | 10/03/2026 | 31/03/2026 | No existe → brecha | 06-CUMPLIMIENTO/BCU/ |
| EV-004       | PR-06             | Reporte de escaneo de vulnerabilidades | Depto. Sistemas | 12/03/2026 | 02/04/2026 | Validada | 02-PROTECCION/PR-06/ |

ESTADOS DEL CICLO:
Solicitada  →  Recibida  →  Validada
                ↓ (no existe)
             No existe → brecha (alimenta ID-02/ID-03 e ID-05)
```

### Estados sugeridos y su significado

| Estado | Significado | Acción del RSI |
|---|---|---|
| Solicitada | Se envió el pedido formal, dentro del plazo | Hacer seguimiento a mitad del plazo |
| Recibida | La evidencia llegó, aún no se validó | Validar atributos (sección 1.1) y archivar |
| Validada | Cumple los 4 atributos y cubre el requisito de RELEV-02 | Enlazar al documento del kit |
| No existe → brecha | El control no tiene evidencia | Registrar brecha en ID-02/ID-03 e ID-05 |

> **Una sola planilla:** evita planillas por persona o por reunión. Una única planilla de evidencias (con filtros por área, documento y estado) es la única fuente de verdad del ciclo.

---

## 5. Formatos y repositorio

### 5.1 Dónde guardar

Toda evidencia se archiva en el repositorio del SGSI según **EST-CARPETAS-001 (Estructura de Carpetas)**:

- **00-GOBERNANZA** → GV-* (política, roles, comité).
- **01-IDENTIFICACION** → ID-* (inventario, clasificación, riesgos, perfil).
- **02-PROTECCION** → PR-* (controles técnicos y organizativos).
- **03-DETECCION** → DE-* (logs, SIEM, monitoreo).
- **04-RESPUESTA** → RS-* (incidentes, comunicación).
- **05-RECUPERACION** → RC-* (continuidad, restauración).
- **06-CUMPLIMIENTO** → URCDP, BCU, auditorías.
- **07-MEJORA** → acciones correctivas y mejoras.
- **08-TEMPLATES** → plantillas en blanco.
- **09-ARCHIVO** → documentos cerrados y vencidos.

### 5.2 Nomenclatura de archivos

Cada evidencia se nombra con la nomenclatura del kit:

```text
[CÓDIGO]_[Nombre]_[VXX.X]_[ESTADO].md|docx|pdf|xlsx

Ejemplos:
ID-01_Diagrama-Red-Banca-Persona_V01.0_VALIDADA.pdf
PR-06_Reporte-Parches-Core_V01.2_RECIBIDA.pdf
URCDP-04_Listado-Bases-Datos_V01.0_VALIDADA.xlsx
```

- La versión **cambia** cuando la evidencia se actualiza.
- El estado refleja el ciclo de la planilla (Recibida / Validada).
- **Un solo lugar de verdad:** la evidencia se archiva una sola vez en el repositorio y se enlaza desde los documentos del kit. Nunca guardes dos copias en dos carpetas: se desincronizan y se pierde la trazabilidad.

---

## 6. ¿Qué hacer cuando la evidencia no existe?

La evidencia que no existe es **información, no un fracaso**. Si el control no tiene registro, el relevamiento descubrió una brecha real del banco. Esto es exactamente lo que el proyecto debe encontrar.

### 6.1 El procedimiento

1. Registrá la brecha en la planilla: estado **"No existe → brecha"**.
2. Documentá el control esperado y el control real: qué debería haber y qué hay hoy.
3. Alimentá **ID-02/ID-03** (riesgos): la brecha se convierte en un riesgo con su valoración (por ejemplo, "ausencia de registro de pruebas de restauración" → riesgo medio-alto de pérdida de datos).
4. Alimentá **ID-05** (perfil de ciberseguridad): el control faltante baja el perfil del banco en esa categoría.
5. Proponé el tratamiento en **ID-04** (Plan de Tratamiento): crear el control o aceptar el riesgo, con responsable y plazo.

### 6.2 Qué nunca hacer

| Prohibido | Por qué | Qué hacer en su lugar |
|---|---|---|
| Fabricar la evidencia | Convierte una brecha en fraude; en auditoría es hallazgo grave | Registrar la brecha y su riesgo |
| Pedirle al área que "armé algo para el papel" | Genera evidencia falsa que no sobrevive una auditoría | Pedir el registro real o reconocer su ausencia |
| Aceptar "sí, eso existe" sin registro | Las palabras no prueban controles | Pedir la evidencia o registrar la brecha |
| Ocultar la brecha para "no demorar" | El SGSI pierde credibilidad | Tratarla en ID-04 con responsable y fecha |

---

## 7. Cierre del ciclo: recepción, validación y archivo

Cuando la evidencia llega, el ciclo no termina: se cierra con tres pasos.

### 7.1 Confirmar la recepción

Al recibir cada evidencia, enviá un correo corto confirmando:

```text
Asunto: Confirmación de recepción de evidencia EV-00X

Estimado/a [Nombre]:

Confirmo la recepción de la evidencia [nombre] para [documento del
kit]. Estamos validando que cubra el requisito normativo de
[MCU 5.0 / BCU / URCDP] y te confirmaremos el resultado.

Muchas gracias por la gestión.

[Nombre del RSI / facilitador] · Banco
```

### 7.2 Validar que cubre el requisito

Cada evidencia se contrasta contra el requisito mapeado en **RELEV-02** (norma → pregunta → evidencia). Si la evidencia no cubre el requisito completo, se devuelve al área con una nota corta explicando qué falta, sin generar fricción: "la evidencia cubre [X], falta [Y] para cerrar el requisito [Z]".

### 7.3 Archivar y actualizar la planilla

- Archivá en la carpeta correcta según EST-CARPETAS-001, con la nomenclatura estándar.
- Actualizá la planilla: estado **Recibida → Validada**, ubicación del repositorio.
- Enlazá la evidencia desde el documento del kit que sustenta (RELEV-08).

### Checklist del ciclo de evidencias

- ☐ Cada pedido fue formal, por escrito y con fecha límite.
- ☐ Todos los pedidos están en la planilla única de seguimiento.
- ☐ Se hicieron recordatorios a mitad del plazo.
- ☐ Cada evidencia recibida fue confirmada y validada contra RELEV-02.
- ☐ La evidencia inexistente se registró como brecha en ID-02/ID-03 e ID-05.
- ☐ Todo está archivado en EST-CARPETAS-001 con nomenclatura estándar.

---

## 8. Errores comunes

| Error | Consecuencia | Cómo evitarlo |
|---|---|---|
| Pedir evidencia de palabra | No hay rastro, fecha ni seguimiento | Siempre correo formal o memorando (sección 3) |
| Pedir sin fecha límite | Entregas infinitas que bloquean el plan de 12 semanas | Fecha límite en cada pedido |
| No registrar en la planilla | Se pierden pedidos y vencer | Planilla única, actualizada el día del pedido |
| Aceptar evidencia sin validar | Requisitos que "se cerraron" con evidencia insuficiente | Validar contra RELEV-02 antes de dar por cerrado |
| Guardar en dos lugares | Versiones desincronizadas, trazabilidad perdida | Un solo lugar de verdad (EST-CARPETAS-001) |
| Fabricar o aceptar evidencia inventada | Riesgo grave de auditoría y pérdida de credibilidad del SGSI | Registrar como brecha y tratarla en ID-04 |
| Pedir al área equivocada | Demoras y malas relaciones | Verificar el organigrama vigente del Banco antes de pedir |
| No agradecer la entrega | Se erosiona la colaboración del área | Confirmación de recepción siempre |

---

## 9. Cierre del módulo

Pediste evidencias útiles (verificables, fechadas, trazables, íntegras), supiste qué pedir por cada documento del kit, usaste el correo formal con la estructura completa, registraste cada pedido en la planilla única, archivaste en EST-CARPETAS-001 con nomenclatura estándar y convertiste la evidencia inexistente en brecha tratada. El siguiente paso es convertir toda la conversación y las evidencias en documentos del kit: **RELEV-08 · Registro: de la conversación al documento del kit**.

---

**Documentos relacionados:** ID-01, PR-06, DE-01, ID-04, EST-CARPETAS-001, INFRA-08
