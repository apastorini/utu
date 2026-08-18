# EV-02 · Checklist de Evidencias por Control (qué pedir, con opciones)

> **Función del MCU 5.0:** Todas las funciones: cada evidencia se mapea a un control del MCU 5.0 (y su par ISO 27001 / BCU / URCDP).
> **ISO/IEC 27001:** Anexo A (los controles citados).
> **BCU:** EMG y normativa complementaria (ver EV-01).
> **URCDP:** Documento de Seguridad (URCDP-01) y notificación (URCDP-02).
> **Nivel del curso:** 🔴 Dominar · **Uso:** checklist de trabajo para pedir evidencias durante el relevamiento y las auditorías.

---

## 1. Qué es este checklist y cómo usarlo

Este checklist responde a la pregunta del RSI: **"¿qué evidencia pido para demostrar que este control existe?"** Para cada control se listan **varias opciones de evidencia** — alcanza con **una** (la más fácil de obtener y la que se genera sola, no la que hay que fabricar a mano).

Cómo usarlo:

1. Por cada control, elegí **una** de las opciones (prioridad según RELEV-07: evidencia que se genera sola > evidencia que se arma > testimonial).
2. Pedila al área indicada con la plantilla de correo de RELEV-07.
3. Validala (¿fechada? ¿íntegra? ¿trazable? — atributos de INFRA-08) y guardala en `06-CUMPLIMIENTO` (EST-CARPETAS-001) con la nomenclatura de EV-03.
4. Si no existe ninguna opción → **brecha** (registrar en ID-02/03/05).

> **Regla de oro:** una sola evidencia válida por control es suficiente. No acumules papeles: preferí la **captura de pantalla de un sistema**, el **reporte exportado** o el **documento firmado** antes que un correo que "dice que se hace".

---

## 2. Gobernar (GV)

| Control (MCU 5.0) | Qué se pide demostrar | Opciones de evidencia (elige 1) | Quién la tiene | Doc. del kit |
|---|---|---|---|---|
| GV.PO · Política | Política de seguridad aprobada | (a) Política firmada/aprobada por Directorio (PDF) · (b) Resolución del Directorio · (c) Publicación en intranet con fecha | Comité · Secretaría General | GV-01 |
| GV.RR · Roles | RSI y roles designados | (a) Designación del RSI firmada · (b) Organigrama con rol marcado · (c) Actas de designación | Riesgos · Capital Humano | GV-03 · BCU-03 |
| GV.OV · Supervisión | El SGSI se supervisa | (a) Informe del RSI a la Dirección (GV-06) · (b) Acta de Comité de Seguridad · (c) Minuta de presentación al Directorio | RSI · Comité | GV-06 |
| GV.SC · Cadena de suministro | Riesgos de terceros gestionados | (a) Matriz de proveedores con riesgo · (b) Acuerdos de confidencialidad firmados (PR-08) · (c) Due diligence / evaluaciones de terceros | Compras · Legal | GV-05 · PR-08 |

---

## 3. Identificar (ID)

| Control (MCU 5.0) | Qué se pide demostrar | Opciones de evidencia (elige 1) | Quién la tiene | Doc. del kit |
|---|---|---|---|---|
| ID.AM · Gestión de activos | Inventario de activos | (a) Export del sistema de inventario (GLPI o similar) · (b) Planilla de inventario firmada · (c) Reporte de escaneo de red (Nmap) con fecha | Div. TI · dueños de activos | ID-01 |
| ID.RA · Evaluación de riesgos | Riesgos evaluados | (a) Registro de riesgos (planilla/Eramba) exportado · (b) Matriz de riesgos firmada · (c) Informe de análisis con metodología aplicada | RSI · Riesgos | ID-02 · ID-03 |
| GV.RM · Tratamiento | Plan de tratamiento | (a) Plan de tratamiento con responsables y plazos · (b) Riesgos residuales aceptados por el Comité · (c) Seguimiento de acciones cerradas | RSI · Comité | ID-04 |

---

## 4. Proteger (PR)

| Control (MCU 5.0) | Qué se pide demostrar | Opciones de evidencia (elige 1) | Quién la tiene | Doc. del kit |
|---|---|---|---|---|
| PR.AA · Acceso e identidades | Acceso controlado | (a) Reporte de revisión de accesos (fechado) · (b) Alta/baja de usuarios en sistema · (c) Política de accesos firmada + ejemplo de solicitud | Div. TI · Capital Humano | PR-01 |
| PR.AT · Concientización | Personal capacitado | (a) Registro de asistencia a capacitación · (b) Resultado de simulacro de phishing (Gophish) · (c) Calendario de concientización aprobado | RSI · Capital Humano | PR-02 |
| PR.DS · Seguridad de datos | Datos cifrados/clasificados | (a) Matriz de clasificación de datos · (b) Evidencia de cifrado (contenedor VeraCrypt / política de cifrado) · (c) Inventario de claves con custodia | RSI · Div. TI | PR-03 |
| PR.AA-06 / PR.PS · Física | Seguridad física | (a) Planos/perímetros de áreas restringidas · (b) Registro de visitas o de ingreso a sala de servidores · (c) Cámaras y controles de acceso físico documentados | Admin. General · TI | PR-04 |
| PR.IR · Respaldo | Respaldos y restauración | (a) Reporte del sistema de respaldo (éxito/fecha) · (b) Acta de prueba de restauración · (c) Política de respaldo firmada + ejemplo de log | Div. TI | PR-05 · BCU-06 |
| PR.PS · Vulnerabilidades | Parches aplicados | (a) Reporte de escáner de vulnerabilidades (OpenVAS) con fecha · (b) Registro de parches aplicados por equipo · (c) Proceso de parcheo firmado + ejemplo | Div. TI | PR-06 |
| PR.PS · Desarrollo seguro | SDLC seguro | (a) Reporte SAST (Semgrep) o DAST (OWASP ZAP) · (b) Política de desarrollo seguro firmada · (c) Revisión de código con hallazgos cerrados | Div. TI | PR-07 |

---

## 5. Detectar (DE)

| Control (MCU 5.0) | Qué se pide demostrar | Opciones de evidencia (elige 1) | Quién la tiene | Doc. del kit |
|---|---|---|---|---|
| DE.CM · Monitoreo continuo | Se monitorea y registra | (a) Captura del SIEM (Wazuh/Grafana) con fecha · (b) Política de logs con retención (≥12 meses) · (c) Ejemplo de alerta real procesada | Div. TI · RSI | DE-01 |
| DE.AE · Análisis de eventos | Anomalías detectadas | (a) Ejemplo de alerta/incidente analizado · (b) Reglas de correlación configuradas · (c) Informe de detección con acción tomada | Div. TI · RSI | DE-02 |
| DE.CM · Pruebas | Pruebas de seguridad | (a) Reporte de pentest (tercero o interno) · (b) Reporte de escaneo OpenVAS/ZAP · (c) Alcance y plan de pruebas aprobado | RSI · Div. TI | DE-03 |

---

## 6. Responder (RS)

| Control (MCU 5.0) | Qué se pide demostrar | Opciones de evidencia (elige 1) | Quién la tiene | Doc. del kit |
|---|---|---|---|---|
| RS.MA · Gestión de incidentes | Se gestionan incidentes | (a) Caso de incidente en TheHive/tickets con fases · (b) Registro de incidentes con fechas y cierre · (c) Plan de respuesta aprobado + ejemplo | RSI · Div. TI | RS-01 |
| RS.CO · Notificación | Se notifica | (a) Notificación a BCU/CERTuy/URCDP enviada (ejemplo anonimizado) · (b) Procedimiento de notificación firmado · (c) Registro de comunicaciones del incidente | RSI | RS-02 · URCDP-02 |
| RS.AN · Análisis forense | Evidencia preservada | (a) Informe forense · (b) Cadena de custodia documentada · (c) Imagen de disco/memoria resguardada (hash) | RSI · Div. TI | RS-03 |

---

## 7. Recuperar (RC)

| Control (MCU 5.0) | Qué se pide demostrar | Opciones de evidencia (elige 1) | Quién la tiene | Doc. del kit |
|---|---|---|---|---|
| RC.RP · Recuperación | Plan de continuidad | (a) BIA con RTO/RPO · (b) Plan de continuidad aprobado · (c) Acta de simulacro de recuperación | RSI · Div. TI · áreas críticas | RC-01 · RC-02 · BCU-06 |
| RC.CO · Comunicación | Comunicación de recuperación | (a) Plan de comunicación de crisis · (b) Ejemplo de comunicación interna/externa · (c) Registro de contacto actualizado | RSI · Comunicación | RC-03 |

---

## 8. URCDP (evidencia específica de protección de datos)

| Requisito | Qué se pide demostrar | Opciones de evidencia (elige 1) | Quién la tiene | Doc. del kit |
|---|---|---|---|---|
| Documento de Seguridad (art. 10) | Medidas de seguridad documentadas | (a) Documento de Seguridad firmado · (b) Inventario de bases + medidas por base · (c) Registro de medidas técnicas (cifrado, accesos, logs) | RSI · DPD | URCDP-01 |
| Notificación de vulneraciones (72 h) | Se notifica en plazo | (a) Notificación a URCDP enviada (ejemplo anonimizado) · (b) Registro de vulneración con fecha de detección/notificación · (c) Procedimiento firmado | RSI · DPD | URCDP-02 |
| Derechos ARCO | Se atienden pedidos | (a) Ejemplo de respuesta a pedido ARCO (anonimizado) · (b) Registro de pedidos con plazo de respuesta · (c) Procedimiento firmado | RSI · DPD | URCDP-03 |
| Inscripción de bases (art. 22) | Bases inscriptas | (a) Comprobante de inscripción ante URCDP · (b) Listado de bases inscriptas · (c) Registro de actualizaciones | RSI · DPD | URCDP-04 |
| EIPD (art. 12) | Evaluación de impacto | (a) Informe EIPD aprobado · (b) Metodología + ejemplo aplicado · (c) Decisión de tratamiento documentada | RSI · DPD | URCDP-05 |
| DPD designado | Delegado existe | (a) Designación del DPD · (b) Comunicación a la URCDP del DPD · (c) Organigrama con rol DPD | Directorio · RSI | URCDP-06 |

---

## 9. Resumen: criterio de elección de evidencia

| Criterio | Preferir | Evitar |
|---|---|---|
| Origen | Evidencia que se genera sola (log, reporte, export) | Evidencia fabricada "a pedido" sin respaldo |
| Formato | Fechada, con autor y trazable (PDF firmado, export, captura con fecha) | Correo suelto, captura sin fecha, documento sin nombre |
| Cantidad | 1 evidencia válida por control | Acumular 5 papeles del mismo control |
| Vigencia | Actualizada en el último ciclo (según frecuencia del control) | Evidencia de hace 3 años sin renovar |

---

## 10. Checklist de cierre del RSI

- ☐ Para cada control del SGSI definí la evidencia que se va a pedir (una opción de la tabla).
- ☐ El pedido se hizo por escrito (plantilla RELEV-07) con el área correcta.
- ☐ Cada evidencia recibida fue validada (fecha, integridad, trazabilidad).
- ☐ Las evidencias están guardadas en `06-CUMPLIMIENTO` con nomenclatura EV-03.
- ☐ Las brechas (controles sin evidencia) están en el registro de riesgos con plan de cierre.
- ☐ El estado por control está actualizado en la MATRIZ-001.

---

**Documentos relacionados:** EV-01, EV-03, EV-04, EV-05, MATRIZ-001, INFRA-08 (estándar de evidencia), RELEV-07 (proceso de pedido), RELEV-11 (tabla maestra requisito→evidencia)
