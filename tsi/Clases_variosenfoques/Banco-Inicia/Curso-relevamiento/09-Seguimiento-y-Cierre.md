# RELEV-09 · Seguimiento de compromisos y cierre

> ⚠️ **Alerta:** este documento menciona **nombres propios del organigrama del Banco** (personas y cargos, abril 2026). Antes de usar el documento, verificá la vigencia de esos nombres contra el organigrama actual.

**Verificar contra el organigrama vigente:** los nombres y cargos mencionados en este módulo corresponden al organigrama de abril 2026. Antes de usarlos en un correo, una minuta o un informe oficial, confirmalos contra la versión vigente que publica el Banco: los cargos rotan y los nombres cambian sin aviso.

> **Función del MCU 5.0:** el seguimiento ejecuta la función ID (Identificar) en su fase de maduración y alimenta la gobernanza GV: sin compromisos cerrados, el inventario de activos (ID.AM), la evaluación de riesgos (ID.RA) y el plan de tratamiento (ID-04) quedan en papel.
> **ISO/IEC 27001:** las cláusulas 9 y 10 (evaluación del desempeño y mejora) exigen verificar que lo prometido se cumple: un plan de tratamiento sin seguimiento es una declaración de intenciones, no un control.
> **BCU:** el EMG y la Circular 2227 (riesgo operacional) piden evidencia de gestión: el seguimiento de compromisos es la prueba de que los hallazgos se convierten en acciones y no quedan en la minuta.
> **URCDP:** los compromisos sobre datos personales (Documento de Seguridad, notificaciones de vulneración, EIPD) deben poder rastrearse: la planilla de compromisos es ese rastro.
> **Nivel del curso:** 🟢 Descubrir · 🟡 **Practicar** · 🔴 Dominar

---

## 1. El seguimiento es donde se gana o se pierde el relevamiento

La reunión sin seguimiento es café: dura una hora, deja buena sensación y a los dos días nadie recuerda qué se dijo. El relevamiento no termina cuando se apaga el micrófono: termina cuando **cada compromiso asumido en la reunión está cumplido, con su evidencia y registrado en el documento del kit**.

Pensalo así: en la reunión vos prometiste un marco normativo y el área prometió un dato. Si ninguna de las dos promesas se persigue, no hay intercambio: hay una charla. Y de las charlas no salen inventarios de activos, ni ROPA, ni matrices de riesgo.

### 1.1 La cadena que convierte charlas en documentos

```
Reunión → Minuta (RELEV-06) → Compromisos → Planilla de seguimiento
        → Evidencia (RELEV-07) → Documento del kit (RELEV-08) → Cierre (RELEV-11)
```

Cada eslabón se alimenta del anterior. El eslabón que más se rompe en los proyectos reales es el que va de **compromisos** a **evidencia**: se anota todo, se agradece todo, y después no se vuelve a preguntar. Tu trabajo en este módulo es volver a preguntar, siempre por escrito, hasta que la evidencia exista.

### 1.2 Quién hace el seguimiento

| Rol | Qué hace | Frecuencia |
|---|---|---|
| Dueño del compromiso (el área) | Entrega la evidencia en la fecha comprometida. | — |
| RSI (vos) | Lleva la planilla, recuerda, persigue y registra. | Semanal |
| Sponsor del área | Desbloquea, habilita y refuerza los pedidos formales. | Quincenal |
| Gerencia General / Comité | Recibe informes y escalamientos que no se resolvieron en el área. | Mensual / por excepción |

El seguimiento **no es tarea delegable de un día para el otro**: si lo delegás sin planilla ni criterio, la primera semana todo anda y la tercera el proyecto está dormido. El seguimiento es un rol, no un trámite.

### 1.3 Cuánto cuesta no hacer seguimiento

| Qué pasa si no seguís | Consecuencia concreta |
|---|---|
| El área no entrega | No tenés la evidencia que sustenta ID-01, ID-03 o el ROPA. |
| El área no ve avance | Desmotiva: nadie vuelve a poner fechas si el proyecto "no camina". |
| Perdés el hilo | Rehacés preguntas ya hechas; el área percibe desorden y lo reporta a su jerarquía. |
| No hay cierre | El informe final queda vacío y el Comité pregunta qué pasó con el plan de 18 meses. |
| Se quema la relación | La segunda vuelta (RELEV-11, mantenimiento) te va a costar el doble. |

---

## 2. La planilla de compromisos

La planilla de compromisos es el **único lugar donde duermen las promesas**. Si un compromiso no está en la planilla, no existe. Esta es la plantilla mínima:

```
| ID   | Compromiso                | Responsable | Área              | Fecha comprometida | Estado             | Evidencia asociada        | Último seguimiento |
|------|---------------------------|-------------|-------------------|--------------------|--------------------|---------------------------|--------------------|
| C-01 | Enviar inventario de Banco En Línea | Cr. Viviana Trabuco | Div. Canales | 2026-06-15 | Abierto | ID-01, ficha A-012 | 2026-06-08 |
| C-02 | Compartir política de resguardos | Ing. Daniel Herrera | TI / Producción | 2026-06-20 | Pendiente de evidencia | DE-01 | 2026-06-10 |
| C-03 | Listar bases de datos con datos personales | Lic. Cristian Palo | TI / Sistemas | 2026-07-02 | En curso | URCDP-04, ROPA | 2026-06-12 |
```

Reglas de oro de la planilla:

1. **Una sola planilla.** No existan la "planilla de María" y la "planilla del proyecto". Una fuente de verdad, congelada cada mes para el informe.
2. **Un solo dueño por compromiso.** Si el compromiso es del área, el responsable es una persona nombrada, no "el departamento".
3. **Estado con evidencia, no con fe.** "Cerrado" significa: recibí el documento, lo revisé y quedó registrado en el kit. Si no recibiste nada, el estado es "Pendiente de evidencia" o "Vencido".
4. **Fecha comprometida negociada.** La fecha no la imponés vos: la negocia el área con vos y se registra.
5. **Seguimiento anotado.** Cada recordatorio, llamada y escalada queda registrado en la última columna. Es tu defensa cuando alguien diga "nunca me avisaron".

### 2.1 Estados sugeridos

| Estado | Significado | Cuándo se usa |
|---|---|---|
| Abierto | Compromiso aceptado, fecha dentro de plazo. | Recién asumido en la minuta. |
| En curso | El área ya trabaja en la entrega. | Confirmado por el dueño o por avance parcial. |
| Pendiente de evidencia | El área dice "ya está", pero no mandó el documento. | Mientras no exista el archivo o el dato. |
| Vencido | Pasó la fecha comprometida sin entrega. | Automático el día después de la fecha. |
| Escalado | Subió al sponsor o a la jerarquía. | Aplicaste la regla de escalamiento (sección 5). |
| Cerrado | Evidencia recibida, revisada y registrada en el kit. | Solo con evidencia real. |
| Cancelado | El pedido quedó sin efecto con causa documentada. | El compromiso era innecesario o cambió el alcance. |

> **Consejo:** definí estados con tus aliados (sponsor, Comité) al inicio del proyecto. Si el Comité sabe qué significa "Escalado", la escalada deja de sonar a fracaso y pasa a sonar a transparencia.

---

## 3. Rutinas de seguimiento

El seguimiento no se improvisa: se programa. Tres rutinas fijas, como las comidas del día:

### 3.1 Revisión semanal de pendientes (vos, solo, 30 minutos)

Los lunes, 30 minutos, con la planilla abierta: avanzar estados, marcar vencidos, preparar los correos de la semana. Si esta cita no está en tu agenda, no pasa.

### 3.2 Revisión quincenal con el sponsor (15 a 20 minutos)

Cada dos semanas, reunión breve con el sponsor del área: qué se venció, qué se escaló, qué se necesita desbloquear. No es una reunión de trabajo: es una **reunión de despeje**. Vas con la planilla filtrada por pendientes, no con la planilla entera.

### 3.3 Informe de avance mensual (alimenta GV-06)

Cada mes se emite el informe de avance que se sube a la carpeta del proyecto y que alimenta el **Informe semestral del RSI a Dirección (GV-06)**. Estructura mínima del informe:

```
Informe de avance del relevamiento — Mes/AAAA
1. Resumen ejecutivo (5 líneas máximo).
2. Números del mes: reuniones hechas, compromisos abiertos/vencidos/cerrados.
3. Avances por área (una línea por área).
4. Escalamientos y atrasos con causa.
5. Próximos 30 días.
```

El informe mensual se envía con copia al sponsor y al Comité de Seguridad: es tu evidencia de gestión y tu mejor argumento de presupuesto futuro.

### 3.4 Calendario tipo

| Día | Rutina | Duración | Participantes |
|---|---|---|---|
| Lunes 1 | Revisión semanal de pendientes | 30 min | RSI |
| Lunes 1 | Envío de recordatorios de la semana | 15 min | RSI |
| Miércoles quincena | Reunión con sponsor | 20 min | RSI + Sponsor |
| Viernes | Actualización final de la planilla | 15 min | RSI |
| Último día hábil | Informe de avance mensual | 60 min | RSI → Comité/sponsor |

---

## 4. Cómo perseguir sin molestar

Hay una diferencia entre **perseguir** y **acosar**. Perseguir es recordar con respeto y con plazo. Acosar es preguntar todos los días sin método. La técnica es el **escalonamiento**: cada etapa tiene su momento, su canal y su tono.

### 4.1 El escalonamiento

| Etapa | Cuándo | Cómo | Quién |
|---|---|---|---|
| 1. Correo recordatorio | 3 días hábiles antes de la fecha | Correo breve, amable, con la fecha y el pedido adjunto. | RSI |
| 2. Llamada breve | 2 días hábiles después del vencimiento | Llamada de 5 minutos: preguntar "¿en qué está? ¿puedo ayudar a desbloquear?" | RSI |
| 3. Escalada al sponsor | 1 semana después del vencimiento | Correo formal al sponsor con el compromiso, la fecha, los recordatorios y la causa. | RSI + Sponsor |

La escalada no es un castigo: es una **herramienta de desbloqueo**. Muchas veces el área no entrega porque un dato depende de otra área o de un sistema viejo, y el sponsor es quien tiene el poder de resolverlo. Por eso en la escalada se describe el **bloqueo**, no la culpa.

### 4.2 Plazos reales y negociados

Nunca pongas vos una fecha "ideal". La fecha es negociada: "¿Cuándo podés tenerlo? ¿Qué necesitás para esa fecha?" Un plazo realista cumplido vale más que un plazo ideal vencido. Si el área te dice "no sé", ofrecé un rango y que elija.

### 4.3 Reuniones breves de 15 minutos

Para pendientes con varias partes, usá reuniones de 15 minutos, de pie o por video, con agenda de tres puntos: qué falta, qué bloquea, fecha nueva. 15 minutos obligan a ir al grano y no se sienten como una pérdida de tiempo del área.

### 4.4 La regla de las 2 semanas

**Ningún compromiso pasa más de 2 semanas sin contacto.** Si a las 2 semanas no hubo entrega ni respuesta, el compromiso está muerto de facto: se re-agenda con causa o se convierte en pendiente formal. Esta regla evita que el proyecto arrastre deudas fantasma durante meses.

---

## 5. Qué hacer con los compromisos vencidos

El compromiso vencido no es un fracaso: es **información**. Alguien no pudo entregar por una causa, y esa causa te dice algo sobre el área, el sistema o el alcance. Tu trabajo es capturarla.

### 5.1 Primero: re-negociar con causa

Antes de cualquier escalada, preguntá: "¿qué pasó?". Si la causa es legítima (un corte de energía, una prioridad de negocio, falta de acceso a un sistema viejo), se negocia una fecha nueva con la causa anotada. La causa anotada es oro: es la base del análisis de riesgos (ID-02/03).

### 5.2 Escalar por jerarquía

Si la causa no es legítima o el bloqueo no se puede resolver en el área, subís el escalonamiento a la etapa 3 (correo al sponsor). Si el sponsor no resuelve en 15 días, subís al siguiente nivel jerárquico con copia al Comité. Siempre por escrito y con el historial de la planilla.

### 5.3 Documentar el atraso como riesgo

Un compromiso que se vence reiteradamente es un **síntoma**. Ese síntoma se convierte en riesgo en ID-02 y ID-03: "el área X no mantiene actualizado el inventario de bases, lo que afecta la inscripción ante la URCDP". Así el atraso deja de ser un problema personal de seguimiento y pasa a ser un riesgo gestionable del banco.

### 5.4 Plantilla de correo de escalamiento

```
Asunto: Escalamiento — Compromiso C-XX · [Área] · [Resumen del compromiso]

Estimado/a [nombre del sponsor]:

Le escribo para solicitar su apoyo con el compromiso C-XX asumido el [fecha]
por [área/responsable], con fecha comprometida el [fecha original].

Situación:
- Compromiso: [descripción]
- Fecha comprometida: [fecha]
- Estado actual: vencido desde el [fecha]
- Acciones realizadas: recordatorio por correo el [fecha], seguimiento
  telefónico el [fecha].
- Bloqueo identificado: [causa declarada por el área o "sin respuesta"]

Este compromiso es necesario para [evidencia/documento del kit que alimenta],
vinculado a [norma: MCU 5.0 ID.AM / BCU Circular 2227 / URCDP].

Solicito su intervención para [desbloquear el acceso / reasignar el
responsable / autorizar la fecha nueva] antes del [fecha límite].

Quedo a las órdenes para ampliar.

Saludos cordiales,
[Nombre] — RSI / Coordinación del proyecto SGSI
```

---

## 6. El cierre del ciclo de relevamiento

El relevamiento se cierra, no se abandona. El cierre tiene tres pasos:

### 6.1 Cruce contra RELEV-02 y RELEV-07

Cada requisito relevable que definiste en **RELEV-02** (norma → territorio) debe tener evidencia pedida en **RELEV-07** y evidencia recibida en la planilla de compromisos. Checklist del cruce:

- ☐ Cada requisito de la matriz de RELEV-02 tiene al menos un compromiso asociado.
- ☐ Cada compromiso cerrado tiene su evidencia guardada en la carpeta correcta del kit.
- ☐ Los compromisos sin cerrar están identificados como pendientes con causa.
- ☐ Los pendientes se mapean a un riesgo (ID-02/03) o a una tarea del plan de 18 meses.

### 6.2 El informe final de relevamiento

Estructura mínima del informe de cierre:

```
INFORME FINAL DE RELEVAMIENTO — SGSI Banco
1. Portada y resumen ejecutivo.
2. Objetivo y alcance del relevamiento (GV-02).
3. Metodología: agenda de 12 semanas (RELEV-03), entrevistas, evidencia.
4. Resultados por área:
   - Qué se relevó.
   - Qué se obtuvo (evidencias, documentos).
   - Brechas detectadas.
   - Pendientes con causa.
5. Correspondencia normativa (resumen de la tabla maestra de RELEV-11).
6. Anexos: minutas, planilla de compromisos, inventario de evidencias.
```

### 6.3 Socializar el informe antes de entregarlo

Nunca mandes el informe final sin que las áreas lo hayan visto. Cada área revisa lo que dice sobre ella: corrige errores, desactiva sorpresas y convierte al área en coautora. El informe socializado no genera defensivas en el Comité; el informe sorpresa sí.

---

## 7. Cómo presentar el informe de cierre al Comité y a la Dirección

El informe al Comité/Dirección no es el informe completo: es una **síntesis de decisiones**. Usá esta tabla resumen por área:

| Área relevada | Reuniones | Evidencias obtenidas | Brechas | Pendientes prioritarios |
|---|---|---|---|---|
| División Banca Persona | 4 | 9 | 2 | Inventario de expedientes de crédito |
| División Canales y Apoyo Comercial | 3 | 7 | 3 | Ficha técnica de Banco En Línea |
| División TI | 6 | 15 | 5 | Política de resguardos documentada |
| División Operaciones | 4 | 11 | 4 | Procedimiento de pagos interbancarios |
| ... | | | | |

### 7.1 Prioridades para la siguiente etapa

Presentá los próximos pasos con su documento del kit y su prioridad:

| Próximo paso | Documento | Prioridad |
|---|---|---|
| Evaluación de riesgos con metodología | ID-03 | Alta |
| Plan de tratamiento de riesgos | ID-04 | Alta |
| Inscripción de bases de datos ante URCDP | URCDP-04 | Alta |
| Perfil de ciberseguridad institucional | ID-05 | Media |
| Verificación con Auditoría Interna | BCU-05 | Media |

### 7.2 Guion de presentación de 3 minutos

```
"Señores miembros del Comité: concluimos el relevamiento del territorio.
Relevamos N áreas, obtuvimos M evidencias y detectamos P brechas, la mayoría
en [nombre de la brecha más grande]. Los próximos tres meses nos enfocamos en
la evaluación de riesgos y en la inscripción de las bases de datos personales
ante la URCDP. El detalle completo está en el informe que acompaña esta nota,
con la correspondencia normativa por requisito."
```

---

## 8. Errores comunes

- **Reunión sin minuta y sin compromisos**: si no quedó escrito, no pasó.
- **Planilla con estados "en proceso" para siempre**: un estado cómodo no avanza el proyecto. Forzá fechas.
- **Perseguir solo por teléfono**: el seguimiento informal no deja rastro. Todo por escrito, con copia.
- **No escalar a tiempo**: esperar un mes para avisar al sponsor convierte un atraso menor en un proyecto en riesgo.
- **Escalar sin causa**: subir un problema sin saber qué lo bloquea solo genera ruido y desgasta al sponsor.
- **Cerrar compromisos sin evidencia**: "me dijo que ya está" no es un cierre. El cierre es el archivo recibido y registrado.
- **Presentar el informe sin socializar**: el Comité no debería ser la primera vez que el área ve lo que se escribió de ella.
- **Olvidar la segunda vuelta**: el relevamiento no es una campaña única: se mantiene y se repite (RELEV-11, sección 6).

---

**Documentos relacionados:** ID-04, GV-06, BCU-05, RC-04
