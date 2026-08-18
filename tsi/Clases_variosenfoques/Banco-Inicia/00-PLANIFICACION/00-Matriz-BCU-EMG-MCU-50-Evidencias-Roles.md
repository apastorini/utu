# Matriz BCU EMG ↔ MCU 5.0 con evidencias, presentación y responsables

> **Código:** MATRIZ-002 · **Versión:** 1.0
> **Objetivo:** juntar en una sola herramienta los **Estándares Mínimos de Gestión del BCU (EMG)** con el **Marco de Ciberseguridad 5.0 de Agesic (MCU 5.0)**, indicando para cada requisito: **qué evidencia tener, cómo presentarla, qué área del Banco es responsable, qué rol la custodia y por qué es esa área la indicada**.
> **Uso:** respuesta rápida a la pregunta del auditor: "¿quién demuestra qué, con qué evidencia, y por qué le toca a esa área?"
> **Relación con el kit:** complementa MATRIZ-001 (qué documento cubre qué norma) y EV-01 (checklist BCU). Los códigos de documento referidos (GV-xx, ID-xx, PR-xx, etc.) viven en `02-ENTREGABLES/`.

---

## 1. Glosario de siglas

| Sigla | Significado | Para qué aparece |
|---|---|---|
| **BCU** | Banco Central del Uruguay | Supervisor del Banco; exige los EMG y el RNRCSF |
| **EMG** | Estándares Mínimos de Gestión relativos a la Seguridad de la Información | Los 6 ejes que el BCU audita (Gobierno, Marco de Riesgos, Función Seguridad, Gestión TI, Auditoría, Continuidad) |
| **RNRCSF** | Recopilación de Normas de Regulación y Control del Sistema Financiero | Normativa BCU donde están el art. 492 (resguardo de datos) y las circulares |
| **Circ. 2227** | Circular del BCU sobre riesgo operativo | Marco de gestión de riesgos que el BCU cruza con la seguridad |
| **Circ. 2280** | Circular del BCU sobre sistema de pagos | Requisitos de monitoreo y seguridad del sistema de pagos |
| **MCU 5.0** | Marco de Ciberseguridad 5.0 de Agesic | Marco de referencia nacional; 72 requisitos en 14 bloques y 6 funciones |
| **Agesic** | Agencia para el Desarrollo del Gobierno de Gestión Electrónica y la Sociedad de la Información y del Conocimiento | Autor del MCU 5.0 y de la Guía de Implementación |
| **CN** | Bloque de requisitos "Cumplimiento normativo y revisión" del MCU 5.0 | CN.1, CN.2, CN.3 |
| **PD** | Bloque de requisitos "Protección de datos personales" del MCU 5.0 | PD.1 … PD.8 |
| **URCDP** | Unidad Reguladora y de Control de Datos Personales | Autoridad de control de la Ley 18.331 |
| **Ley 18.331** | Ley de Protección de Datos Personales y Habeas Data | Fuente de los principios PD.1…PD.8 |
| **SGSI** | Sistema de Gestión de la Seguridad de la Información | Lo que el kit construye (ISO/IEC 27001) |
| **RSI** | Responsable de Seguridad de la Información | Rol 2ª línea que lidera la seguridad y custodia la mayoría de las evidencias |
| **CISO** | Chief Information Security Officer | Equivalente internacional del RSI |
| **DPD** | Delegado de Protección de Datos | Rol que supervisa los requisitos PD y los derechos de los titulares |
| **SIEM** | Security Information and Event Management | Herramienta de monitoreo/correlación (en el kit: Wazuh) |
| **SOC** | Security Operations Center | Equipo/área de monitoreo y respuesta |
| **DMZ** | Zona desmilitarizada (demilitarized zone) | Segmento de red donde se publican servicios |
| **CVE** | Common Vulnerabilities and Exposures | Identificador público de vulnerabilidades |
| **CVSS** | Common Vulnerability Scoring System | Puntaje de severidad de vulnerabilidades |
| **ARCO** | Acceso, Rectificación, Cancelación, Oposición | Derechos de los titulares (en Uruguay: + información, inclusión, supresión, impugnación) |
| **EIPD** | Evaluación de Impacto en la Protección de Datos | Análisis previo de riesgo para nuevos tratamientos |
| **SDLC** | Software Development Life Cycle | Ciclo de vida del desarrollo seguro (PR-07) |
| **BCP / DRP** | Business Continuity Plan / Disaster Recovery Plan | Planes de continuidad y recuperación |

---

## 2. Qué pide cada uno y cómo se relacionan

| Tema | BCU (EMG / RNRCSF) | MCU 5.0 (Agesic) | URCDP (Ley 18.331) |
|---|---|---|---|
| Gobierno | Eje "Gobierno de la ciberseguridad": política aprobada por el Directorio, comité, reportes | Función GV (Gobernar) | Art. 10: medidas decididas desde la dirección |
| Riesgos | Eje "Marco de Gestión de Riesgos" + Circ. 2227 | Función ID (Identificar) | EIPD para tratamientos de riesgo alto |
| Defensas | Eje "Gestión de TI" + art. 492 (resguardo de datos) | Función PR (Proteger) | Art. 10: medidas de seguridad |
| Detección | Circ. 2280 (sistema de pagos), monitoreo | Función DE (Detectar) | Detección de vulneraciones |
| Respuesta | Eje "Gestión de incidentes" + Circ. 2227 | Función RS (Responder) | Notificación de vulneraciones en 72 h |
| Continuidad | Eje "Continuidad" + art. 492 | Función RC (Recuperar) | Recuperación sin pérdida de datos |
| Cumplimiento | Eje "Auditoría Interna" | CN.1, CN.2, CN.3 | Auditoría del tratamiento |
| Datos personales | — (el BCU lo cruza con URCDP) | PD.1 … PD.8 | Ley 18.331, Decreto 64/020 |

> **Regla práctica:** el BCU pregunta "¿gobiernas, riesgas, operas, auditas y continuas?"; Agesic pregunta "¿cumples los 72 requisitos?"; la URCDP pregunta "¿tratas datos personales conforme a la ley?". Este documento muestra las **mismas evidencias** que responden a los tres.

---

## 3. Matrices por función

### Formato de las tablas

Cada fila responde: **requisito → evidencia → cómo presentarla → área responsable → rol → por qué esa área**.

> **Leyenda de roles:** RSI (2ª línea, dueño del SGSI), DPD (delegado de datos), Comité de Seguridad (órgano rector), Div. TI (1ª línea), Riesgos No Financieros (2ª línea de riesgos), Auditoría Interna (3ª línea), RRHH (personas), Legales (jurídico), Sucursales (red comercial).

### 3.1 Función GV · Gobernar

| Requisito | Evidencias a tener | Cómo presentarlas | Área responsable | Rol | Justificación |
|---|---|---|---|---|---|
| Política de seguridad aprobada al más alto nivel (GV.PO) / EMG Gobierno | Política de Seguridad de la Información firmada (GV-01), resolución del Directorio | Documento aprobado + acta del Directorio; versión vigente y control de cambios | Dirección / Comité de Seguridad | Directorio (aprueba) · RSI (redacta) | La política es un acto de gobierno: quien la aprueba debe tener autoridad jerárquica; quien la redacta es el RSI |
| Estructura de gobierno, roles y canales de reporte (GV.RR) / EMG Gobierno | Acta de constitución del Comité de Seguridad, matriz de roles (GV-03), designación del RSI y del DPD | Organigrama de seguridad + actas firmadas + resoluciones de designación | Comité de Seguridad / Riesgos No Financieros | RSI · DPD · Comité | El BCU evalúa quién decide y quién rinde cuentas; la 2ª línea (seguridad y riesgos) es la dueña natural |
| Contexto organizativo y alcance del SGSI (GV.OC) | Alcance del SGSI (GV-02) | Mapa del alcance (áreas, sistemas, sedes) | RSI | RSI | El RSI define qué queda dentro del SGSI para que la auditoría tenga límites claros |
| Supervisión y reporte a la dirección (GV.OV) / EMG Gobierno | Informe del RSI a la Dirección (GV-06), actas de revisión | Informe ejecutivo periódico con estado del SGSI | Comité de Seguridad / Dirección | RSI (presenta) · Directorio (recibe) | El reporte periódico demuestra supervisión activa; es requisito BCU y de ISO 9.3 |
| Estrategia y apetito de riesgo (GV.RM) / EMG Marco de Riesgos + Circ. 2227 | Declaración de apetito de riesgo tecnológico (BCU-02), acta de aprobación | Documento de apetito + acta que lo vincula al riesgo operativo | Riesgos / Comité de Riesgos | Gerente de Riesgos · Comité | El apetito de riesgo es decisión de la alta dirección; la 2ª línea de riesgos lo formaliza |
| Cadena de suministro (GV.SC) / EMG + Circ. 2419-2422 | Registro de proveedores (GV-05), contratos con cláusulas de seguridad (PR-08) | Lista de proveedores + matriz de riesgo por proveedor + contratos firmados | Compras / RSI / Legales | Analista de Compras · RSI · Abogados | Los proveedores entran por Compras pero el riesgo de seguridad lo califica el RSI; Legales materializa las cláusulas |

### 3.2 Función ID · Identificar

| Requisito | Evidencias a tener | Cómo presentarlas | Área responsable | Rol | Justificación |
|---|---|---|---|---|---|
| Gestión de activos (ID.AM) / EMG Riesgo Tecnológico | Inventario de activos (ID-01) | Planilla/BD de activos con propietario, criticidad y clasificación; evidencia de actualización trimestral | Div. TI + dueños de negocio | Administrador de Sistemas (carga) · Propietarios (validan) | El inventario nace en TI porque ahí viven los sistemas; cada área confirma sus activos |
| Evaluación de riesgos (ID.RA) / Circ. 2227 | Metodología (ID-02) + análisis ejecutado (ID-03) | Registro de riesgos con probabilidad, impacto, nivel y tratamiento | Riesgos No Financieros / RSI | Analista de Riesgos · RSI | La evaluación de riesgos es una competencia de la 2ª línea de riesgos, con el RSI como especialista técnico |
| Plan de tratamiento (ID.RA / GV.RM) | Plan de tratamiento de riesgos (ID-04) | Planilla con acción, responsable y plazo por riesgo | RSI / dueños de activos | RSI (coordina) · dueños (ejecutan) | Cada riesgo lo trata su dueño; el RSI prioriza y da seguimiento |
| Perfil de ciberseguridad (ID.AM / perfiles) | Perfil de ciberseguridad (ID-05) | Estado actual vs. objetivo por función/categoría del MCU 5.0 | RSI | RSI | El perfil es la foto del cumplimiento MCU 5.0; es insumo del informe al Directorio |
| Mejora y lecciones aprendidas (ID.IM) | Registro de mejoras y lecciones (RC-04) | Actas de revisión post-incidente | Comité de Seguridad | RSI · Comité | La mejora continua cierra el ciclo PDCA y la auditan Agesic y el BCU |

### 3.3 Función PR · Proteger

| Requisito | Evidencias a tener | Cómo presentarlas | Área responsable | Rol | Justificación |
|---|---|---|---|---|---|
| Control de accesos e identidades (PR.AA) / EMG Riesgo Tecnológico | Matriz de accesos y revisión de cuentas (PR-01) | Matriz de perfiles + evidencia de revisión semestral de accesos | Div. TI / RRHH / RSI | Administrador de Sistemas · Analista de RRHH · RSI | Los accesos se otorgan en TI pero se autorizan por el jefe del área y se auditan por el RSI; RRHH gestiona el ciclo laboral (alta/baja) |
| Concientización y capacitación (PR.AT) / EMG Gobierno | Programa de concientización (PR-02) + registros de capacitación | Plan anual + acuses + resultados de simulacros de phishing | RRHH / RSI | Analista de Capacitación · RSI | La cultura de seguridad se construye con RRHH (que tiene el canal con el personal) y la mide el RSI |
| Seguridad de los datos y cifrado (PR.DS) / art. 492 + URCDP | Política de clasificación y cifrado (PR-03), Documento de Seguridad (URCDP-01) | Clasificación de datos + matriz de cifrado + Documento de Seguridad vigente | RSI / DPD / Div. TI | RSI · DPD · Administradores | La protección de datos personales es responsabilidad del DPD; la técnica del cifrado la implementa TI; el RSI une ambos |
| Gestión de vulnerabilidades y parches (PR.PS) / EMG Riesgo Tecnológico | Escaneos y registro de corrección (PR-06) | Reportes de escaneo fechados + ticket de parcheo + verificación | Div. TI / Operaciones de Seguridad | Administrador de Sistemas · Analista SOC | El parcheo es operación de TI (1ª línea); el RSI verifica plazos y excepciones |
| Seguridad física (PR.AA-06 / PR.PS) | Política de seguridad física (PR-04) | Controles de acceso al CPD, registro de visitas, auditorías de escritorio limpio | Seguridad Física | Jefe de Seguridad Física | El CPD y las sedes los custodia Seguridad Física; es su competencia propia |
| Resiliencia de la infraestructura y resguardo (PR.IR) / art. 492 | Política de respaldo (PR-05) + pruebas de restauración | Logs de respaldo + prueba de restauración documentada | Div. TI / Continuidad | Administrador de Respaldos · Jefe de Continuidad | El resguardo de datos es exigencia expresa del art. 492; la ejecución es de TI y el objetivo de recuperación lo fija Continuidad |

### 3.4 Función DE · Detectar

| Requisito | Evidencias a tener | Cómo presentarlas | Área responsable | Rol | Justificación |
|---|---|---|---|---|---|
| Monitoreo continuo y registro de eventos (DE.CM) / Circ. 2280 | Política de monitoreo (DE-01) + logs del SIEM | Captura del SIEM con alertas + política de retención de logs | SOC / Operaciones de Seguridad | Analista SOC · Administrador SIEM | El monitoreo es la tarea diaria del SOC; el RSI define qué se monitorea y la retención |
| Análisis de eventos adversos (DE.AE) | Procedimiento de detección (DE-02) + registros de análisis | Casos de uso del SIEM + análisis de alertas con tickets | SOC / RSI | Analista SOC · RSI | El análisis y la priorización de alertas lo hace el SOC; el RSI escala lo crítico |
| Pruebas de seguridad (DE.CM / DE.AE) / EMG Auditoría + CN.3 | Programa de pentest (DE-03) + informes de pruebas | Informe de pentest con alcance, fecha y resultados; plan de corrección | RSI / Div. TI / Auditoría | RSI (coordina) · TI (corrige) · Auditoría (supervisa) | El pentest debe ser independiente de la operación: lo pide y supervisa quien no ejecuta TI |

### 3.5 Función RS · Responder

| Requisito | Evidencias a tener | Cómo presentarlas | Área responsable | Rol | Justificación |
|---|---|---|---|---|---|
| Plan de respuesta a incidentes (RS.MA) / Circ. 2227 | Plan de respuesta (RS-01) + registros de incidentes | Plan aprobado + registro de incidentes con clasificación y tiempos | RSI / SOC / TI | RSI (lidera) · SOC (detecta) · TI (contiene) | El RSI lidera la respuesta porque el incidente cruza todas las áreas; TI ejecuta la contención |
| Notificación y comunicación (RS.CO) / Circ. 2227 + URCDP 72 h | Procedimiento de notificación (RS-02), registro de notificaciones | Cronograma de notificación (fechas detectado → reportado) + actas | RSI / Legales / DPD | RSI · Abogados · DPD | La notificación al BCU y a la URCDP es legal: Legales y el DPD validan plazos y contenido |
| Análisis forense (RS.AN) | Procedimiento forense (RS-03) + cadena de custodia | Preservación de evidencia con registro de cadena de custodia | RSI / Auditoría / SOC | Forense · Auditoría Interna | La evidencia debe ser preservada por personal independiente para que valga en juicio o ante el supervisor |

### 3.6 Función RC · Recuperar

| Requisito | Evidencias a tener | Cómo presentarlas | Área responsable | Rol | Justificación |
|---|---|---|---|---|---|
| Continuidad del negocio (RC.RP) / EMG Continuidad | Plan de continuidad (RC-01, BCU-06) | BCP aprobado + RTO/RPO definidos | Comité de Continuidad / Riesgos | Jefe de Continuidad · Comité de Crisis | La continuidad es un programa corporativo; se gobierna en el Comité de Continuidad |
| Recuperación ante desastres (RC.RP) / art. 492 | Plan de recuperación (RC-02) + pruebas | Ejercicios de recuperación documentados con resultados | Div. TI / Continuidad | Administrador de Sistemas · Jefe de Continuidad | El DRP lo ejecuta TI (tiene la infraestructura) y lo valida Continuidad |
| Comunicación de crisis (RC.CO) | Plan de comunicación (RC-03) | Matriz de mensajes y canales + simulación de crisis | Comunicación Institucional | Dir. de Comunicación · Comité de Crisis | La comunicación externa es competencia de Comunicación Institucional; el RSI aporta el contenido técnico |

---

## 4. Requisitos transversales: CN (Cumplimiento normativo y revisión)

| Requisito MCU 5.0 | Evidencias a tener | Cómo presentarlas | Área responsable | Rol | Justificación |
|---|---|---|---|---|---|
| **CN.1** Cumplir con los requisitos normativos | Matriz de requisitos legales (MATRIZ-001/002), revisión de normativa vigente, registro de cumplimiento | Matriz con norma → documento → evidencia → responsable + fecha de revisión | RSI / Legales | RSI · Abogados | El cumplimiento normativo es transversal: Legales identifica la norma aplicable y el RSI la traduce en controles |
| **CN.2** Realizar auditorías independientes de seguridad | Programa de auditoría interna de seguridad (BCU-05) + informes de auditoría | Informe de auditoría independiente + plan de acción con seguimiento | Auditoría Interna | Auditor Interno · Comité de Auditoría | La independencia exige que el auditor no dependa de la función auditada (3ª línea) |
| **CN.3** Revisar regularmente mediante pruebas de intrusión y evaluación de vulnerabilidades | Programa de pentest (DE-03), escaneos de vulnerabilidades (PR-06) | Informes de pruebas de intrusión fechados + reporte de vulnerabilidades y su corrección | RSI / Div. TI / Auditoría | RSI (coordina) · TI (corrige) · Auditoría (valida) | Las pruebas deben ser independientes y periódicas: las contrata el RSI, las ejecuta un tercero y la corrección la hace TI |

---

## 5. Requisitos transversales: PD (Protección de datos personales)

| Requisito MCU 5.0 | Qué exige | Evidencias a tener | Cómo presentarlas | Área responsable | Rol | Justificación |
|---|---|---|---|---|---|---|
| **PD.1** Principio de legalidad | Tratar datos conforme a la Ley 18.331; bases inscriptas en URCDP | Listado de bases de datos personales (URCDP-01), resolución de inscripción en URCDP | Constancias de inscripción + inventario de bases por sistema | RSI / DPD / Legales | DPD (lidera) · RSI (inventario) · Abogados (valida) | La inscripción y el cumplimiento legal de las bases es función propia del DPD; el RSI aporta el inventario de sistemas |
| **PD.2** Principio de veracidad | Datos actualizados, veraces, adecuados y relevantes | Procedimientos de actualización de datos de clientes, registros de corrección | Evidencia del flujo de actualización de datos + registros | Áreas de negocio / DPD | Analista de Datos · DPD | Los datos los alimenta el área de negocio que los captura; el DPD supervisa la calidad según la finalidad |
| **PD.3** Principio de finalidad | Usar los datos solo para la finalidad declarada | Declaraciones de finalidad en formularios, revisión de usos | Formularios con finalidad declarada + controles de uso | DPD / Legales / Negocio | DPD · Abogados | La finalidad se declara legalmente; el DPD verifica que los usos no se desvíen |
| **PD.4** Principio de previo consentimiento informado | Consentimiento libre, previo e informado; no preseleccionado; revocable | Formularios de consentimiento (no premarcados), registro de consentimientos, mecanismo de revocación | Ejemplo de formulario + registro de consentimientos + evidencia del canal de revocación | DPD / Canales / Legales | DPD (lidera) · Diseñador de Canales · Abogados | El consentimiento se recaba en los canales de captura (web, sucursal); el DPD define los textos y Legales los valida; el decreto 414/009 exige opciones no premarcadas |
| **PD.5** Principio de seguridad de los datos | Medidas técnicas/organizativas; notificación de vulneraciones a URCDP en 72 h | Documento de Seguridad (URCDP-01), registro de incidentes, evidencia de notificación a URCDP | Documento de Seguridad vigente + cronograma de notificación (fecha constatada → fecha notificada ≤ 72 h) | RSI / DPD / SOC | RSI (seguridad) · DPD (notifica) · SOC (detecta) | La seguridad de los datos es el punto donde se cruzan el RSI (técnica) y el DPD (legal); la notificación es obligación legal del responsable |
| **PD.6** Principio de reserva | Confidencialidad: acceso solo a quien corresponde | Matrices de acceso a datos personales, cláusulas de confidencialidad | Matriz de accesos por base + acuerdos de confidencialidad firmados | Div. TI / RRHH / DPD | Administrador de Sistemas · RRHH · DPD | La reserva se garantiza con accesos (TI) y acuerdos (RRHH); el DPD verifica el tratamiento |
| **PD.7** Principio de responsabilidad proactiva | Privacidad por diseño y por defecto; EIPD | EIPD de nuevos tratamientos, criterios de privacidad por diseño, designación del DPD | EIPD aprobada + acta de designación del DPD | DPD / Div. TI / RSI | DPD (asesora) · TI (implementa) · RSI (integra) | La privacidad por diseño se decide al construir sistemas: DPD asesora, TI la implementa en el SDLC |
| **PD.8** Derechos de los titulares | Garantizar los derechos (información, acceso, actualización/rectificación, inclusión, supresión, impugnación); respuesta en 5 días hábiles | Procedimiento de atención de derechos (URCDP-03), registro de solicitudes y respuestas, evidencia de cumplimiento de plazos | Procedimiento aprobado + planilla de solicitudes con fechas de recepción y respuesta + indicadores de plazo | DPD / Canales de Atención | DPD (lidera) · Analista de Atención al Cliente | Las solicitudes de los titulares llegan por los canales de atención al cliente; el DPD define el procedimiento y mide los plazos |

---

## 6. Cómo presentar las evidencias (formato común)

Toda evidencia debe permitir a un tercero **reconstruir el hecho**. Formato mínimo recomendado (ver EV-03):

1. **Nombre estándar:** `EVI-AAAA-MM-DD-NN-descripcion.ext` (ej. `EVI-2026-03-10-01-escaneo-vuln-OpenVAS.pdf`).
2. **Metadatos:** fecha cierta, alcance, herramienta/sistema, responsable, resultado.
3. **Formato:** PDF firmado o captura con fecha visible para documentos; reportes nativos para técnicos; actas firmadas para decisiones.
4. **Ubicación:** estructura de carpetas del SGSI (EV-03) + bitácora del RSI (GV-06).
5. **Presentación al supervisor/auditor:** tabla resumen por requisito (la de este documento) + carpeta de evidencias indexada + relato de 1 minuto por evidencia (qué muestra y por qué cumple).

> **Plantillas de respaldo:** cada evidencia se apoya en un documento del kit (`02-ENTREGABLES/`). Usá MATRIZ-001 para saber qué documento cubre qué norma y EV-02 para saber qué evidencia pedir por control.

---

## 7. Resumen ejecutivo para el auditor

| Pregunta del auditor | Respuesta de 1 línea |
|---|---|
| ¿Quién gobierna? | Directorio aprueba, Comité de Seguridad decide, RSI ejecuta (GV) |
| ¿Quién identifica riesgos? | Riesgos No Financieros + RSI (ID) |
| ¿Quién protege? | Div. TI ejecuta, RSI verifica, DPD supervisa datos personales (PR) |
| ¿Quién detecta? | SOC monitorea, RSI define y escala (DE) |
| ¿Quién responde? | RSI lidera, TI contiene, Legales/DPD notifican (RS) |
| ¿Quién recupera? | TI restaura, Continuidad valida, Comunicación informa (RC) |
| ¿Quién cumple? | Legales + RSI mapean la norma; Auditoría Interna audita (CN) |
| ¿Quién protege los datos? | DPD lidera; RSI y TI implementan (PD) |
