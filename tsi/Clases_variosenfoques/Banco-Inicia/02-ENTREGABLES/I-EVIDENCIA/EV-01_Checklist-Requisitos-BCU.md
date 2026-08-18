# EV-01 · Checklist de Requisitos del BCU (EMG y normativa complementaria)

> **Función del MCU 5.0:** Gobernar (GV.OC · GV.PO · GV.RR · GV.OV) y todas las funciones, porque el BCU evalúa el SGSI completo.
> **ISO/IEC 27001:** Cláusulas 5–10 y Anexo A (la evidencia BCU coincide con la evidencia ISO).
> **BCU:** Guía de Estándares Mínimos de Gestión (EMG) · RNRCSF art. 492 · Circular 2227 (riesgo operativo) · Circulares 2419-2422 (tercerización) · Circular 2280 (sist. de pagos) · Comunicación 2022/254.
> **URCDP:** la evidencia BCU se comparte con la URCDP (Documento de Seguridad, notificación de vulneraciones).
> **Nivel del curso:** 🔴 Dominar · **Uso:** checklist de trabajo del RSI para auditar internamente el cumplimiento BCU.

---

## 1. Qué es este checklist y cómo usarlo

Este checklist consolida **lo que pide el BCU** y, para cada requisito, te indica **qué documento del kit lo evidencia y en qué sección** (la "nota de dónde mirar"). No es un documento nuevo: es la **herramienta de verificación** que cruza MATRIZ-001, las plantillas BCU-01…06 y el resto del kit.

Cómo usarlo:

1. Marcar cada fila **☐/☑** según el estado.
2. En la columna **"Dónde se evidencia (kit)"**, abrí el documento y la sección indicada.
3. En la columna **"Qué pedir al área"**, usá la evidencia de las plantillas o del checklist EV-02.
4. Si un requisito **no se cumple**, registralo como **brecha** (alimenta ID-02/03/05 y BCU-05) y programá su cierre en GV-04.

> **Nota de terminología:** el BCU agrupa los EMG en 6 ejes: **Gobierno, Marco de Riesgos, Función de Seguridad (2ª línea), Gestión de TI (1ª línea), Auditoría Interna (3ª línea) y Continuidad**. Este checklist sigue esos ejes.

---

## 2. Eje 1 · Gobierno de la ciberseguridad y riesgo tecnológico

| # | Requisito BCU | Dónde se evidencia (kit) | Nota de dónde mirar | Área que debe aportar |
|---|---|---|---|---|
| 1 | Política de administración del riesgo tecnológico aprobada por el Directorio | BCU-01 §4 y §5 | Sección "Compromiso del Directorio" + "Política de administración del riesgo tecnológico" | Directorio · Comité de Seguridad |
| 2 | Estructura de gobierno definida (Comité de Seguridad, roles, canales de reporte) | BCU-01 §6 · GV-03 §4 | "Estructura de gobierno" / matriz de roles del Comité | Comité · RSI |
| 3 | Apetito de riesgo tecnológico declarado y vinculado al riesgo operativo | BCU-01 §7 · BCU-02 §3 | "Apetito de riesgo" y "Apetito y tolerancia al riesgo" (con Circ. 2227) | Directorio · Riesgos |
| 4 | Reporte periódico al Directorio del estado del riesgo y del SGSI | BCU-01 §8 · GV-06 | "Reporte al Directorio" / informe del RSI a la Dirección | RSI |
| 5 | Plan anual de seguridad aprobado y con recursos | GV-04 §4 | Cronograma anual, responsables y recursos | Comité · RSI · Planificación |

---

## 3. Eje 2 · Marco de gestión de riesgos

| # | Requisito BCU | Dónde se evidencia (kit) | Nota de dónde mirar | Área que debe aportar |
|---|---|---|---|---|
| 6 | Proceso formal de identificación, evaluación, tratamiento y monitoreo de riesgos | BCU-02 §4 · ID-02 §3 | "Proceso de gestión de riesgos tecnológicos" / metodología ID-02 | RSI · Riesgos |
| 7 | Análisis de riesgos ejecutado (activos, amenazas, vulnerabilidades, probabilidad, impacto) | ID-03 | Registro de riesgos del caso Banco | RSI · TI · Riesgos |
| 8 | Plan de tratamiento de riesgos con responsables y plazos | ID-04 | Plan de tratamiento | RSI · dueños de activos |
| 9 | Aceptación documentada de riesgos residuales (quién acepta y en qué nivel) | BCU-02 §6 | "Aceptación documentada de riesgos residuales" | Comité · Directorio |
| 10 | Taxonomía de riesgos tecnológicos | BCU-02 §5 | "Taxonomía de riesgos tecnológicos" | RSI · Riesgos |
| 11 | Vínculo con el riesgo operativo (Circular 2227) | BCU-02 §7 | "Vínculo con el riesgo operativo" | RSI · Riesgos |

---

## 4. Eje 3 · Función de Seguridad de la Información (2ª línea)

| # | Requisito BCU | Dónde se evidencia (kit) | Nota de dónde mirar | Área que debe aportar |
|---|---|---|---|---|
| 12 | RSI designado, con ubicación orgánica e independencia | BCU-03 §2 y §3 · GV-03 | "Designación y ubicación orgánica" + "Principio de independencia" | Directorio · Riesgos No Financieros |
| 13 | Funciones del RSI definidas (gobierno, riesgos, operación, incidentes, cumplimiento) | BCU-03 §4 · 04-Rol-RSI | "Funciones del RSI" / módulo del rol | RSI |
| 14 | Recursos y dedicación adecuados a la función | BCU-03 §5 | "Dedicación y recursos" | Directorio · Capital Humano |
| 15 | Responsable del resguardo de datos designado (art. 492) | BCU-03 §8 · BCU-06 §5 · PR-05 | "Responsable del resguardo de datos" / "Resguardo de datos" | RSI · TI |
| 16 | Coordinaciones permanentes documentadas (TI, RRHH, legal, URCDP) | BCU-03 §7 | "Coordinaciones permanentes" | RSI · áreas |

---

## 5. Eje 4 · Gestión de TI (1ª línea)

| # | Requisito BCU | Dónde se evidencia (kit) | Nota de dónde mirar | Área que debe aportar |
|---|---|---|---|---|
| 17 | Organización de la División TI formalizada | BCU-04 §2 | "Organización de la División TI" | Div. TI |
| 18 | Gestión de operaciones documentada | BCU-04 §3 | "Gestión de operaciones" | Div. TI |
| 19 | Gestión de cambios con aprobación y prueba | BCU-04 §4 | "Gestión de cambios" | Div. TI |
| 20 | Gestión de incidentes técnicos y escalamiento | BCU-04 §5 · RS-01 | "Gestión de incidentes técnicos" / plan de respuesta | Div. TI · RSI |
| 21 | Gestión de configuraciones (baseline, cambios controlados) | BCU-04 §6 · PR-06 | "Gestión de configuraciones" | Div. TI |
| 22 | Arquitectura y desarrollo seguro (SDLC) | BCU-04 §7 · PR-07 | "Arquitectura y desarrollo seguro" | Div. TI |
| 23 | Indicadores de servicio de TI reportados | BCU-04 §9 | "Indicadores de servicio" | Div. TI |

---

## 6. Eje 5 · Auditoría interna de seguridad (3ª línea)

| # | Requisito BCU | Dónde se evidencia (kit) | Nota de dónde mirar | Área que debe aportar |
|---|---|---|---|---|
| 24 | Programa anual de auditoría de seguridad | BCU-05 §3 | "Plan anual de auditorías de seguridad" | Div. Auditoría Interna |
| 25 | Criterios de auditoría definidos (MCU 5.0, ISO, BCU, URCDP) | BCU-05 §4 | "Criterios de auditoría" | Div. Auditoría Interna |
| 26 | Perfil e independencia de los auditores | BCU-05 §5 | "Perfil e independencia" | Div. Auditoría Interna |
| 27 | Informes al Comité y Directorio + seguimiento de hallazgos | BCU-05 §6, §7 y §8 | "Ejecución e informes", "Clasificación de hallazgos", "Seguimiento de hallazgos" | Div. Auditoría Interna · RSI |

---

## 7. Eje 6 · Continuidad del negocio

| # | Requisito BCU | Dónde se evidencia (kit) | Nota de dónde mirar | Área que debe aportar |
|---|---|---|---|---|
| 28 | BIA (análisis de impacto en el negocio) con RTO/RPO | BCU-06 §3 · RC-01 | "Análisis de Impacto en el Negocio (BIA)" | Negocio (cada área) · RSI |
| 29 | Plan de contingencia con escenarios y estrategias | BCU-06 §4 · RC-02 | "Escenarios y estrategias de contingencia" | RSI · TI · áreas críticas |
| 30 | Resguardo de datos (art. 492 RNRCSF): respaldo y prueba de restauración | BCU-06 §5 · PR-05 · RC-02 | "Resguardo de datos" + PR-05 (respaldos y pruebas) | Div. TI · RSI |
| 31 | Pruebas y simulacros anuales documentados | BCU-06 §7 · RC-02 | "Pruebas y simulacros anuales" | RSI · Div. TI |
| 32 | Comunicación a autoridades (BCU, CERTuy) ante contingencias/incidentes | BCU-06 §8 · RS-02 | "Comunicación al BCU y a las autoridades" | RSI |

---

## 8. Requisitos transversales (aplica en todos los ejes)

| # | Requisito BCU | Dónde se evidencia (kit) | Nota de dónde mirar | Área que debe aportar |
|---|---|---|---|---|
| 33 | Inventario de activos actualizado | ID-01 | Registro completo de activos | Div. TI · dueños de activos |
| 34 | Control de acceso e identidades (menor privilegio, revisión de accesos) | PR-01 | Política de accesos | Div. TI · Capital Humano |
| 35 | Gestión de vulnerabilidades y parches con evidencia | PR-06 | Proceso de parcheo y reportes | Div. TI |
| 36 | Cifrado y gestión de claves | PR-03 | Clasificación de datos y cifrado | RSI · Div. TI |
| 37 | Concientización y capacitación | PR-02 | Programa y registros de asistencia | RSI · Capital Humano |
| 38 | Seguridad física y del entorno | PR-04 | Controles físicos de instalaciones | Admin. General · TI |
| 39 | Tercerización: riesgos y acuerdos con proveedores | GV-05 · PR-08 | Gestión de terceros | Compras · TI · Legal |
| 40 | Monitoreo y registro de eventos (log) | DE-01 · DE-02 | Registros y retención (≥12 meses, Decreto 66/025) | Div. TI · RSI |
| 41 | Respuesta y notificación de incidentes | RS-01 · RS-02 | Plan y procedimiento de notificación | RSI · Div. TI |
| 42 | Gestión de incidentes de datos personales (notificación 72 h) | RS-02 · URCDP-02 | Procedimiento URCDP | RSI · DPD |

---

## 9. Checklist de cierre del RSI

- ☐ Recorrí los 42 requisitos y marqué el estado real de cada uno.
- ☐ Para cada requisito, verifiqué que la sección del documento indicada existe y está completa.
- ☐ Las brechas detectadas están registradas en el registro de riesgos (ID-02/03) con plan de cierre.
- ☐ El estado de cumplimiento está en la MATRIZ-001 (código por documento).
- ☐ Las evidencias asociadas están guardadas según EST-CARPETAS-001 y el EV-03 (sistematización).
- ☐ El resultado alimenta el Informe del RSI a la Dirección (GV-06) y la planificación anual (GV-04).

---

**Documentos relacionados:** BCU-01…BCU-06, MATRIZ-001, ID-01…ID-05, PR-01…PR-08, DE-01…03, RS-01…03, RC-01…04, URCDP-01…06, GV-04, GV-06, EV-02, EV-03, EV-04, EV-05
