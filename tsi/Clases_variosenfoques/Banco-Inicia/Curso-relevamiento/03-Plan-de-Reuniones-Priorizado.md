# RELEV-03 · El plan de reuniones priorizado: agenda de 12 semanas

> ⚠️ **Verificar contra el organigrama vigente:** los nombres y cargos de este módulo corresponden al organigrama de abril 2026 (PDF SF.PLE.05, https://www.bhu.com.uy/sobre-bhu/organigrama). El plan de 18 meses corresponde a PLAN-SGSI-001 (F0 gobierno, F1 diagnóstico, F3 activos/riesgos, F8 URCDP transversal, F9 BCU). Antes de ejecutar la agenda, validá nombres, cargos y fases contra las versiones vigentes.
>
> **Función del MCU 5.0:** este módulo organiza la ejecución de las funciones GV e ID (y las primeras entradas de PR/DE/RS/RC) en el tiempo: sin una agenda priorizada, el relevamiento se convierte en una serie de reuniones sin orden ni evidencias.
> **ISO/IEC 27001:** la agenda materializa la cláusula 4 (contexto) y 5 (liderazgo): se arranca por el sponsor y la dirección para bajar el alcance por la cadena de autoridad.
> **BCU:** el orden del relevamiento debe asegurar primero lo que el BCU más vigila: operación y TIC (art. 492, Circular 2227), para que las evidencias de resguardo y recuperación estén listas antes del cierre.
> **URCDP:** la agenda reserva una ola dedicada al negocio para completar el ROPA (URCDP-04) y el Documento de Seguridad (URCDP-01), que dependen de datos que solo entrega la operación comercial.
> **Nivel del curso:** 🔴 Dominar

---

## 1. Principios de priorización

Antes de la agenda, las reglas que la ordenan. Cada principio se explica con un ejemplo real del Banco.

| Principio | Qué dice | Ejemplo Banco |
|---|---|---|
| **Riesgo primero** | Lo que puede causar más daño se releva antes. | El sistema de pagos y el Banco En Línea van antes que el archivo administrativo: una caída de pagos es un incidente de primer nivel. |
| **Dependencia entre documentos** | Primero se releva lo que alimenta a otros documentos. | Sin el inventario de activos (ID-01) no hay análisis de riesgos (ID-03); sin ROPA no hay Documento de Seguridad completo (URCDP-01). |
| **Sponsor primero** | El respaldo se consigue al inicio, no al final. | La resolución de Gerencia General habilita todas las puertas; si arrancás sin ella, cada área te va a recibir a regañadientes. |
| **Quick wins** | Resultados visibles temprano generan confianza. | Cerrar la semana 2 con el inventario preliminar de TI y mostrarlo al Comité demuestra que el proceso funciona. |
| **Cadena de autoridad** | Se baja de arriba hacia abajo, nunca al revés. | Primero Gerente de Área, después Jefe de División, después Gerente de Departamento. Pedir directo al nivel operativo salta la jerarquía y fracasa. |

**Cómo se combinan los principios en una decisión real.** Supongamos que tenés una sola tarde para elegir la primera reunión de la semana 2. La decisión correcta:

1. **Riesgo primero** descarta el archivo administrativo y apunta a TI (sistema de pagos).
2. **Sponsor primero** dice que antes de agendar TI hay que cerrar el kick-off de la semana 1.
3. **Dependencia entre documentos** dice que el inventario de TI (ID-01) va antes que el análisis de riesgos (ID-03).
4. **Quick wins** dice que la primera reunión de TI debe producir algo visible para el Comité.

Resultado: semana 1 = Gerencia General; semana 1-2 = Riesgos No Financieros; semana 3-4 = TI Producción. Cada principio empuja la misma dirección, y eso es lo que hace que el plan sea defendible cuando alguien pregunte "¿por qué primero esto?".

---

## 2. Las tres olas del relevamiento

### Ola 1 (semanas 1-4) · Gobierno y habilitación

**Objetivo:** conseguir respaldo formal, alinear expectativas, conocer hallazgos previos y definir cómo se va a medir el avance.

| Reunión | Área | Qué buscás |
|---|---|---|
| Gerencia General | Sponsor del proyecto | Resolución de inicio, alcance, orden de bajar a las áreas. |
| Área Riesgos → Riesgos No Financieros | Par del RSI | Metodología de riesgos, circuito de cumplimiento, expectativas. |
| Oficial de Cumplimiento | Riesgos No Financieros | Normativa BCU y PLA/FT que se cruza con el SGSI. |
| DPD | Riesgos o Servicios Jurídicos | Registro de tratamientos, inscripciones, requisitos URCDP. |
| Auditoría Interna | 3ª línea | Hallazgos previos, formatos de evidencia que esperan. |
| Planificación Estratégica | Control de Gestión | Proyectos en curso, presupuesto, indicadores del banco. |

### Ola 2 (semanas 3-8) · El corazón operativo

**Objetivo:** inventariar activos, sistemas, bases, procesos, resguardos y contratos. Es la ola que más alimenta ID-01, ID-03 y BCU-01. Se solapa con la Ola 1 (semanas 3-4) porque TI y Operaciones son las áreas más grandes y conviene agendarlas apenas el sponsor lo habilite.

| Reunión | Área | Qué buscás |
|---|---|---|
| División TI | Depto. Producción | Infraestructura, servidores, resguardos, claves. |
| División TI | Depto. Sistemas | Aplicaciones, bases de datos, desarrollo. |
| División TI | Depto. Soporte Técnico | Puestos, incidentes, soporte. |
| División Operaciones | Depto. Procesos | Procedimientos documentados. |
| División Operaciones | Depto. Sistema de Pagos | Operación de pagos y su criticidad. |
| División Operaciones | Depto. Información y Apoyo Comercial | Datos e información de apoyo al negocio. |
| División Operaciones | Depto. Servicios Generales | Instalaciones y seguridad física. |
| Administración Financiera | Contaduría | Registros contables y tributarios. |
| Administración Financiera | Administración General / Compras | Contratos y terceros (PR-08, GV-05). |
| Administración Financiera | Finanzas | Información financiera sensible. |

### Ola 3 (semanas 7-12) · El negocio y el cierre

**Objetivo:** relevar los datos personales en la operación real, las personas, los terceros, y cerrar el ROPA y el Documento de Seguridad. Se solapa con la Ola 2 (semanas 7-8) para aprovechar los hallazgos de TI al preguntarle al negocio.

| Reunión | Área | Qué buscás |
|---|---|---|
| Área Comercial | Banca Persona (Análisis de Préstamos) | Expedientes de crédito, garantías. |
| Área Comercial | Banca Persona (Atención Personalizada) | Trato y consultas con clientes. |
| Área Comercial | Canales y Apoyo Comercial | Sucursales, Banco En Línea, Defensor del Cliente. |
| Capital Humano | Administración y Desarrollo de RRHH | Personas, contratos, concientización (PR.AT). |
| Servicios Jurídicos Notariales | Asesoría legal y notarial | Contratos, normas, DPD. |
| Secretaría General | Gobierno corporativo | Actas, expedientes, formalidades. |
| Seguimiento y Recuperación de Activos | Garantías e Inmuebles / Morosidad | Datos sensibles de deudores y garantías. |

---

## 3. Tabla de agenda por semana

| Semana | Reunión | Área | Con quién (cargo) | Objetivo | Entregable de la reunión | Documento del kit |
|---|---|---|---|---|---|---|
| 1 | Kick-off y sponsor | Gerencia General | Gerente General | Respaldo formal, alcance, mandato | Resolución de inicio, lista de áreas habilitadas | PLAN-SGSI-001, GV-03 |
| 1-2 | Par del RSI | Área Riesgos | Gerente de Riesgos No Financieros | Metodología, apetito, circuito de cumplimiento | Mapa de riesgos existente, acuerdos de trabajo | ID-02, GV-03 |
| 2 | Cumplimiento | Riesgos No Financieros | Oficial de Cumplimiento | Cruce BCU / PLA/FT con el SGSI | Listado de exigencias BCU vigentes | BCU-01, MATRIZ-001 |
| 2-3 | DPD | Riesgos o Jurídico | DPD | Registro de tratamientos e inscripciones | Listado preliminar de bases de datos | URCDP-04 |
| 3 | Auditoría | Auditoría Interna | Jefe de División Auditoría Interna | Hallazgos previos, formato de evidencia | Informe de hallazgos previos, estándar de evidencia | GV-06 |
| 3-4 | Planificación | Planificación Estratégica | Jefe de Depto. Control de Gestión | Proyectos, presupuesto, indicadores | Listado de proyectos de TI en curso | GV-04 |
| 3-4 | Infraestructura | División TI | Gerente de Producción | Servidores, resguardos, claves | Inventario preliminar de infraestructura | ID-01, PR-05, BCU-01 |
| 4-5 | Sistemas | División TI | Gerente de Sistemas | Aplicaciones, bases, desarrollo | Inventario de sistemas y bases de datos | ID-01, PR-03 |
| 5 | Soporte | División TI | Gerente de Soporte Técnico | Puestos, incidentes, soporte | Inventario de puestos, estadística de incidentes | ID-01, DE-01 |
| 5-6 | Procesos | División Operaciones | Gerente de Procesos | Procedimientos documentados | Inventario de procesos operativos | ID-01 |
| 6 | Pagos | División Operaciones | Gerente de Sistema de Pagos | Criticidad de la operación de pagos | Evaluación de criticidad, BIA parcial | RC-01 |
| 6-7 | Información y Servicios | División Operaciones | Gerentes de Información y Servicios Generales | Datos de apoyo, seguridad física | Inventario de datos e instalaciones | ID-01, PR-04 |
| 7 | Contaduría | Administración Financiera | Gerente de Contabilidad y Tributos | Registros contables y tributarios | Inventario de información financiera | ID-01 |
| 7-8 | Compras | Administración Financiera | Gerente de Compras y Contrataciones | Contratos con terceros | Listado de terceros y contratos | PR-08, GV-05 |
| 8 | Finanzas | Administración Financiera | Gerente de Análisis Financiero | Información financiera sensible | Inventario de activos financieros | ID-01 |
| 8-9 | Crédito | Comercial | Gerente de Análisis de Préstamos | Expedientes de crédito, garantías | Inventario de datos de crédito | URCDP-04, ID-01 |
| 9 | Atención | Comercial | Gerente de Atención Personalizada | Trato con clientes | Proceso de atención, datos recabados | URCDP-04 |
| 9-10 | Canales | Comercial | Gerente de Canales de Atención | Sucursales, Banco En Línea | Inventario de canales y datos | URCDP-04, PR-03 |
| 10 | RRHH | Capital Humano | Gerentes de RRHH | Personas y concientización | Plan de capacitación, registros | PR-02 |
| 10-11 | Jurídico | Servicios Jurídicos Notariales | Jefe de División | Contratos, normas, DPD | Dictámenes relevantes, rol DPD | GV-03 |
| 11 | Secretaría | Secretaría General | Jefe de División | Actas y expedientes | Circuito de expedientes | GV-03 |
| 11-12 | Recuperación | Seguimiento y Recuperación | Gerentes de Garantías y Morosidad | Datos sensibles de deudores | Inventario de datos sensibles | URCDP-01, ID-01 |
| 12 | Cierre | Sponsor + Comité | Gerencia General y Comité | Presentar hallazgos y cierre | Informe de relevamiento, plan de tratamiento | GV-06, ID-04 |

---

## 4. Formato de cada reunión

| Elemento | Regla |
|---|---|
| **Duración** | 45-60 minutos. No más. Si sobra tema, agendá una segunda sesión. |
| **Agenda previa por correo** | Se envía 3-5 días antes, con objetivo, temas y documentos del kit a los que apunta. |
| **Invitación formal** | Por el circuito del área (RELEV-01): con copia al sponsor y al responsable del área. |
| **Minuta en 24-48 h** | Se envía al cierre: presentes, temas, acuerdos, pedidos de evidencia con plazo. |
| **Seguimiento semanal** | Revisar cada lunes la planilla de compromisos y evidencias; avisar al Comité de atrasos. |

### 4.1 El ritmo semanal del relevamiento

El plan de 12 semanas no es una lista de reuniones sueltas: es un **ritmo**. Cada semana tiene cuatro momentos fijos:

| Momento | Cuándo | Qué se hace |
|---|---|---|
| Preparación | Lunes | Confirmar agenda de la semana, revisar pendientes de la semana anterior, actualizar la planilla. |
| Reuniones | Martes a jueves | Ejecutar las reuniones agendadas (máximo 2-3 por semana para dejar tiempo de registro). |
| Minutas | Dentro de las 24-48 h | Enviar minuta, pedidos de evidencia y próximos pasos a cada participante y su sponsor. |
| Reporte de avance | Viernes | Un párrafo al Comité: reuniones hechas, evidencias recibidas, riesgos y atrasos. |

**La regla de las dos horas.** Después de cada reunión, reservá dos horas el mismo día para volcar el registro: si lo dejás para la semana siguiente, se pierde la mitad de la información y el área percibe que su tiempo no se valoró.

### 4.2 Cómo se mide el avance del plan

Tres indicadores simples que podés reportar cada viernes al Comité:

| Indicador | Qué mide | Meta |
|---|---|---|
| Reuniones ejecutadas / agendadas | Avance del plan | 90 %+ de lo agendado |
| Evidencias recibidas / pedidas | Flujo real de información | 80 %+ dentro del plazo |
| Documentos del kit iniciados | Resultado sobre el SGSI | Al menos 1 por ola completada |

---

## 5. Prioridades cuando hay poco tiempo

**Los "no negociables"** (si solo tenés tiempo para 4 reuniones, son estas):

| Reunión | Por qué es innegociable |
|---|---|
| TI (Producción + Sistemas) | Aquí vive el inventario de activos (ID.AM), los resguardos y el art. 492. |
| Riesgos No Financieros | Es tu par, tu metodología y tu puente con Cumplimiento. |
| Operaciones (Procesos + Pagos) | Es el corazón operativo que alimenta criticidad y continuidad. |
| DPD | Sin ROPA no hay Documento de Seguridad, y es transversal a todo. |

**Los "postergables"** (se pueden posponer sin romper el SGSI):

| Reunión | Por qué se puede posponer |
|---|---|
| Finanzas y Mercado de Capitales | Relevante, pero su aporte se puede completar con documentación. |
| Secretaría General | Gobierna formalidades; se puede relevar vía documentos. |
| Seguimiento y Recuperación de Activos | Datos sensibles, pero de segundo orden frente a la operación core. |

La regla: **primero lo que alimenta a los documentos maestros** (ID-01, ROPA, BCU-01), después lo que suma detalle. Una agenda perfecta que no se pudo ejecutar vale menos que una agenda chica ejecutada al 100 %.

---

## 6. Cómo lograr el patrocinio y la invitación formal

El plan de reuniones no arranca por casualidad: arranca con una **resolución**. El circuito es:

1. **Resolución de inicio** firmada por Gerencia General: ordena a las áreas colaborar con el relevamiento y designa al RSI. Es el GV-03 en acción.
2. **Comité de Seguridad de la Información** (GV-03): conoce el plan, aprueba la agenda y recibe el reporte de avance. No es una reunión de cortesía: es el órgano que hace ejecutable el plan.
3. **Invitaciones formales por el sponsor de cada área**: la primera invitación a un área la manda (o la firma) Gerencia General o el Gerente de Área, no el RSI solo. A partir de ahí, cada reunión se agenda con el responsable directo.

> **Guion para pedir la resolución al sponsor:**
> *"Estimado/a [nombre]: el relevamiento del SGSI (PLAN-SGSI-001) requiere que las áreas reciban al RSI con carácter formal. Solicitamos una resolución de inicio que habilite las reuniones del plan adjunto, la designación del RSI y el respaldo del Comité de Seguridad de la Información. Este respaldo es el que garantiza que cada área colabore y entregue las evidencias en plazo."*

La **invitación formal** de cada reunión debe contener: motivo (con la norma citada), agenda, duración, participantes y quién convoca. Un modelo:

> **Asunto:** Relevamiento SGSI · Inventario de activos · Depto. [X] · [fecha]
> **Convocante:** Gerencia General (resolución de fecha [XX])
> **Agenda:** 1) Presentación del proyecto (10 min) · 2) Inventario de activos del área (30 min) · 3) Riesgos y evidencias pendientes (20 min)
> **Participantes:** [cargo], RSI, representante de Riesgos.

**Guion para la reunión de cierre de la semana 12:**

> *"Cerramos el relevamiento de 12 semanas. El inventario de activos, el registro de tratamientos y el mapa de riesgos están actualizados. Pasamos los resultados al plan de tratamiento (ID-04) con prioridades por riesgo y las evidencias quedaron registradas para la correspondencia normativa (MATRIZ-001). Los próximos pasos: revisión del Comité, informe a Gerencia General (GV-06) y arranque de la fase de tratamiento."*

**Riesgos del plan y cómo mitigarlos desde el inicio:**

| Riesgo del plan | Señal temprana | Mitigación |
|---|---|---|
| Sin sponsor efectivo | La resolución no se firma o las áreas no responden. | Subir el tema al Comité en la semana 2, no a la semana 8. |
| Calendario que se cae | Reuniones canceladas de último momento. | Agenda de respaldo semanal: si una cae, entra la siguiente de la lista. |
| Áreas que entregan tarde | Evidencias vencidas sin aviso. | Recordatorios por escrito a los 5 días hábiles y copia al sponsor del área. |
| Relevamiento que se estira | La semana 12 se llena de pendientes. | Congelar alcance en la semana 10 y listar el resto como segunda iteración. |
| Comité desinformado | Preguntas repetidas sobre el avance. | Reporte de un párrafo todos los viernes, sin excepción. |

---

## 7. Errores comunes

- **Arrancar sin sponsor**: la primera reunión sin resolución de Gerencia General condiciona todo lo demás: cada área te va a recibir "de compromiso" y las evidencias no llegan.
- **Agendar sin agenda previa**: llegar sin orden y sin agenda enviada convierte la reunión en una charla y el área pierde confianza.
- **Una reunión gigante por área**: invitar a todo un departamento a una sola sesión diluye el objetivo. Mejor 3-4 reuniones chicas y enfocadas.
- **No escalar por la jerarquía**: pedir datos al nivel operativo sin pasar por el Gerente de Área. Es la causa número uno de fricción en un banco público.
- **No respetar las olas**: relevar el negocio antes de tener el inventario de TI obliga a rehacer el trabajo y a duplicar reuniones.
- **No solapar las olas**: esperar a terminar la Ola 1 para recién agendar TI agrega 4 semanas muertas al plan. El solapamiento es deliberado.
- **Prometer un informe que no llega**: el cierre de la semana 12 debe tener fecha y entregable definidos desde la semana 1, o el proceso se diluye en el seguimiento eterno.
- **Reunirse sin registrar**: una reunión sin minuta ni pedido de evidencia es una visita de cortesía. El plan se mide por documentos iniciados, no por charlas tenidas.
- **Extenderse en cada reunión**: 90 minutos de charla matan el ritmo de las 12 semanas. 45-60 minutos con agenda y freno de horario se respetan mutuamente.
- **Cambiar el alcance a mitad de camino**: si una área quiere sumar temas, anotarlos como pendientes de la segunda iteración, no agrandar la reunión en curso.

### Lista de verificación del módulo

- ☐ Tengo la resolución de inicio firmada por Gerencia General.
- ☐ El Comité de Seguridad de la Información aprobó la agenda (GV-03).
- ☐ Validé nombres y cargos contra el organigrama vigente (SF.PLE.05).
- ☐ Agendé las reuniones de la Ola 1 con invitaciones formales y agenda previa.
- ☐ Preparé la plantilla de minuta y el modelo de pedido de evidencias.
- ☐ Identifiqué los no negociables y tengo plan B si el calendario se complica.
- ☐ Agendé el cierre de la semana 12 con informe al sponsor y al Comité.

---

**Documentos relacionados:** PLAN-SGSI-001, GV-03, GV-04, GV-06, MATRIZ-001
