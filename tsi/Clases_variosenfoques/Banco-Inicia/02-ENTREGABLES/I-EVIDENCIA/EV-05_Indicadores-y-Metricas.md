# EV-05 · Indicadores y Métricas del SGSI (cómo definirlos, monitorearlos y darles seguimiento)

> **Función del MCU 5.0:** Gobernar (GV.OV — supervisión) · Detectar (DE.CM — monitoreo continuo) · Identificar (ID.IM — mejora) · Recuperar (RC.RP).
> **ISO/IEC 27001:** Cláusula 9.1 (seguimiento y medición), cláusula 6.2 (objetivos medibles) y cláusula 10 (mejora).
> **BCU:** Guía de Estándares Mínimos de Gestión (EMG) — los seis ejes exigen medir para demostrar; Circular 2280 (indicadores de servicio de sistemas de pago); RNRCSF art. 492.
> **URCDP:** las métricas de protección de datos (capacitación, incidentes, plazos ARCO) alimentan el Documento de Seguridad.
> **Nivel del curso:** 🔴 Dominar · **Uso:** herramienta de trabajo del RSI para definir el tablero de indicadores del SGSI.

---

## 1. Por qué definir indicadores y métricas

**Lo que no se mide no se gestiona** es una frase hecha, pero en el SGSI tiene consecuencias concretas:

1. **El BCU lo pide.** La Guía de EMG evalúa si la entidad supervisada **mide** sus controles y **reporta** resultados. La Circular 2280 exige indicadores de disponibilidad y tiempos de resolución de los sistemas de pago. Sin medición no hay evidencia de gestión.
2. **El MCU 5.0 lo pide.** La función **Gobernar** (GV.OV — supervisión) exige revisar que los objetivos se cumplan; la función **Identificar** (ID.IM — mejora) pide aprender de los resultados. La ISO 27001 lo formaliza en la cláusula 9.1.
3. **El Directorio necesita números, no opiniones.** El Informe del RSI (GV-06) y el Plan Anual (GV-04) se defienden con indicadores: "reducimos X en Y meses" es más fuerte que "estamos mejor".
4. **Permite decidir con datos.** Priorizar inversiones (¿dónde está el mayor riesgo?), detectar desvíos temprano y justificar recursos.
5. **Convierte el trabajo del RSI en evidencia.** Una serie temporal de indicadores es evidencia de gestión ante BCU, Agesic y auditoría (ver EV-01 a EV-03).

> **Regla de oro:** un indicador que no alimenta una decisión o un informe es un número muerto. Definí solo los que vas a **usar** — y cada uno debe tener **fuente de datos**, **frecuencia**, **meta** y **responsable**.

---

## 2. Diferencia entre indicador y métrica (y otros términos)

| Término | Definición | Ejemplo |
|---|---|---|
| **Métrica** | Medición **bruta** de un fenómeno: dato objetivo, sin juicio. | 12 incidentes en el mes · 300 funcionarios capacitados · 92 % de disponibilidad |
| **Indicador (KPI)** | Métrica **con meta y decisión asociada**: mide si se cumple un objetivo. | "MTTR ≤ 8 h para incidentes críticos" · "≥ 95 % de los funcionarios capacitados por año" |
| **Objetivo** | Resultado deseado (de dónde salen los indicadores). | "Reducir los incidentes críticos un 20 % este año" |
| **Meta / Umbral** | Valor o rango que define el éxito de un indicador. | "MTTR < 8 h" · "disponibilidad ≥ 99,5 %" |
| **Línea de base** | Valor inicial antes de mejorar (para medir el cambio). | MTTR en el primer trimestre = 12 h |

### En una frase

- **Métrica** = el termómetro (dato).
- **Indicador (KPI)** = el termómetro **más la meta y la decisión** (¿está bien? ¿qué hacemos?).

> **Cómo se usa esta distinción en el kit:** las tablas de BCU-04 (indicadores de servicio), GV-04 (KPIs del plan anual) y GV-06 (indicadores del SGSI) ya definen **indicadores** (métrica + meta). Cuando definas el tablero del Banco, partí de las **métricas** que ya se generan (logs, tickets, planillas) y convertilas en **indicadores** agregándoles meta y responsable.

---

## 3. Cómo definir un buen indicador (método práctico)

Para cada indicador del tablero, completá estas 8 propiedades. Usá la planilla del EV-03 (misma lógica de registro):

| Propiedad | Pregunta que responde | Ejemplo (MTTR de incidentes críticos) |
|---|---|---|
| **Nombre** | ¿Cómo se llama? | Tiempo medio de resolución de incidentes críticos (MTTR) |
| **Objetivo asociado** | ¿Qué objetivo mide? | Reducir el impacto de incidentes |
| **Fórmula** | ¿Cómo se calcula? | Σ horas de resolución de incidentes críticos del mes ÷ cantidad de incidentes críticos del mes |
| **Fuente de datos** | ¿De dónde sale el número? | Registro de incidentes (TheHive / tickets / RS-01) |
| **Frecuencia** | ¿Cada cuánto se mide y reporta? | Mensual al Comité; semestral al Directorio |
| **Meta / Umbral** | ¿Qué es éxito? | ≤ 8 h (críticos); alerta si > 16 h |
| **Responsable** | ¿Quién lo calcula y responde por él? | RSI (con datos de Div. TI) |
| **Decisión / acción** | ¿Qué se hace si falla? | Revisar capacidades del SOC, escalar, plan de mejora |

### Reglas prácticas

- **Mínimo de indicadores:** 1–2 por objetivo del Plan Anual (GV-04), no 20 por función.
- **Preferí ratios y tendencias** a números absolutos sueltos (el % de parches a tiempo vale más que "400 parches").
- **Medí lo que ya se genera solo** (logs, tickets, exports) antes de crear cargas manuales.
- **Fijá la línea de base primero:** 3 meses de datos antes de comprometer una meta.
- **Revisá la meta anualmente** (los umbrales que eran difíciles se vuelven fáciles).

---

## 4. Tablero mínimo de indicadores por función del MCU 5.0

Estos son los indicadores **recomendados** para arrancar. Marcá los que correspondan al Banco, adaptá metas y agregá los específicos de su contexto. (Los que ya figuran en GV-04, BCU-04 o GV-06 están señalados.)

### 4.1 Gobernar (GV) — ¿el SGSI está gobernado?

| Indicador | Fórmula | Fuente | Frecuencia | Meta sugerida |
|---|---|---|---|---|
| Avance del Plan Anual (GV-04) | Iniciativas en plazo ÷ total × 100 | GV-04 | Mensual | ≥ 90 % en plazo |
| Cumplimiento de controles MCU 5.0 | Controles cumplidos ÷ controles aplicables × 100 | ID-05 · MATRIZ-001 | Semestral | Creciente año a año |
| Comités de seguridad realizados | Comités realizados ÷ programados × 100 | Actas del Comité | Trimestral | 100 % |
| Informes del RSI presentados a tiempo | Informes presentados ÷ programados × 100 | GV-06 | Semestral | 100 % |
| Riesgos altos con plan de tratamiento | Riesgos altos con plan ÷ total de riesgos altos × 100 | ID-03 · ID-04 | Trimestral | 100 % |

### 4.2 Identificar (ID) — ¿conocemos nuestros activos y riesgos?

| Indicador | Fórmula | Fuente | Frecuencia | Meta sugerida |
|---|---|---|---|---|
| Activos inventariados y actualizados | Activos con dueño y fecha de revisión ÷ total × 100 | ID-01 · GLPI | Mensual | ≥ 90 % |
| Riesgos reevaluados en plazo | Riesgos revisados en su fecha ÷ riesgos programados × 100 | ID-03 | Trimestral | ≥ 90 % |
| Brechas de inventario detectadas y cerradas | Brechas cerradas ÷ brechas detectadas × 100 | ID-01 · EV-03 | Trimestral | ≥ 80 % |
| % de evidencias obtenidas | Evidencias recibidas ÷ solicitadas × 100 | Planilla EV-03 | Mensual | Creciente a ≥ 90 % |

### 4.3 Proteger (PR) — ¿los controles de protección funcionan?

| Indicador | Fórmula | Fuente | Frecuencia | Meta sugerida |
|---|---|---|---|---|
| Funcionarios capacitados (PR-02) | Capacitados ÷ plantilla total × 100 | Registros de asistencia | Anual | ≥ 95 % |
| Tasa de clics en simulacros de phishing | Clics ÷ correos enviados × 100 | Gophish (TOOLS-08) | Trimestral | < 5 % y bajando |
| Parches aplicados en plazo | Parches aplicados en la ventana ÷ parches aplicables × 100 | PR-06 · OpenVAS/Trivy | Mensual | ≥ 95 % en críticos |
| Pruebas de restauración de respaldos (art. 492) | Pruebas ejecutadas y aprobadas ÷ programadas × 100 | PR-05 · BCU-06 | Semestral | 100 % |
| Accesos privilegiados revisados | Cuentas revisadas ÷ cuentas privilegiadas × 100 | PR-01 | Trimestral | 100 % |
| Terceros con evaluación de riesgo vigente | Evaluados ÷ terceros críticos × 100 | GV-05 · PR-08 | Anual | ≥ 90 % |

### 4.4 Detectar (DE) — ¿detectamos a tiempo?

| Indicador | Fórmula | Fuente | Frecuencia | Meta sugerida |
|---|---|---|---|---|
| Tiempo medio de detección (MTTD) | Horas desde ocurrencia hasta detección | Wazuh / SIEM (TOOLS-10) | Mensual | < 4 h (críticos) |
| Alertas cerradas en plazo | Alertas atendidas ÷ alertas generadas × 100 | SIEM · tickets | Mensual | ≥ 90 % |
| Cobertura de monitoreo | Sistemas críticos con logs activos ÷ sistemas críticos × 100 | DE-01 | Trimestral | ≥ 95 % |
| Retención de logs cumplida (≥12 meses) | Logs conservados según política ÷ exigidos | DE-01 | Semestral | 100 % |
| Falsos positivos relevantes | Alertas investigadas ÷ alertas generadas × 100 | SIEM | Mensual | ≥ 80 % investigadas |

### 4.5 Responder (RS) — ¿respondemos y notificamos?

| Indicador | Fórmula | Fuente | Frecuencia | Meta sugerida |
|---|---|---|---|---|
| Tiempo medio de resolución (MTTR) | Σ horas de resolución ÷ incidentes (por severidad) | TheHive / tickets (TOOLS-11) | Mensual | Críticos ≤ 8 h |
| Incidentes cerrados con lecciones aprendidas | Con lecciones ÷ incidentes cerrados × 100 | RS-01 · RC-04 | Mensual | ≥ 80 % |
| Cumplimiento de plazos de notificación | Notificaciones en plazo ÷ notificaciones × 100 | RS-02 · URCDP-02 | Por incidente | 100 % (URCDP 72 h) |
| Reincidencia de incidentes | Incidentes repetidos ÷ total × 100 | Registro de incidentes | Trimestral | Bajando |

### 4.6 Recuperar (RC) — ¿recuperamos la operación?

| Indicador | Fórmula | Fuente | Frecuencia | Meta sugerida |
|---|---|---|---|---|
| RTO cumplido en simulacros | Recuperaciones dentro del RTO ÷ simulacros × 100 | BCU-06 · RC-02 | Anual | 100 % |
| RPO cumplido en pruebas de restauración | Restauraciones dentro del RPO ÷ pruebas × 100 | PR-05 | Semestral | 100 % |
| Disponibilidad de sistemas críticos (Circ. 2280) | Tiempo operativo ÷ tiempo programado × 100 | BCU-04 §9 | Mensual | ≥ 99,5 % |
| Simulacros de continuidad realizados | Simulacros realizados ÷ programados × 100 | BCU-06 §7 | Anual | 100 % |

### 4.7 URCDP — protección de datos personales

| Indicador | Fórmula | Fuente | Frecuencia | Meta sugerida |
|---|---|---|---|---|
| Pedidos ARCO respondidos en plazo | Respondidos dentro del plazo legal ÷ total × 100 | URCDP-03 | Trimestral | 100 % |
| Bases de datos inscriptas y actualizadas | Bases registradas ÷ bases existentes × 100 | URCDP-04 · ROPA | Trimestral | ≥ 95 % |
| Vulneraciones notificadas en 72 h | Notificadas en plazo ÷ vulneraciones × 100 | URCDP-02 | Por incidente | 100 % |
| Capacitación en protección de datos | Personal capacitado ÷ personal que trata datos × 100 | PR-02 · URCDP-01 | Anual | ≥ 95 % |

---

## 5. Diferencia entre indicadores "de eficacia" y "de esfuerzo" (matiz importante)

| Tipo | Mide | Ejemplo | Ojo |
|---|---|---|---|
| **De esfuerzo / actividad** | Que se **hizo** la tarea | Parches aplicados · capacitaciones dictadas · escaneos ejecutados | Fáciles de medir, pero no garantizan resultado |
| **De eficacia / resultado** | Que la tarea **logró** el objetivo | Reducción de incidentes · mejora de MTTD · % de clics en phishing | Más valiosos, más difíciles de atribuir |

**Regla:** en cada objetivo del Plan Anual (GV-04), definí **al menos un indicador de resultado** por cada uno de esfuerzo. "Aplicamos 300 parches" (esfuerzo) no dice nada si los incidentes siguen igual; "los incidentes críticos bajaron 30 %" (resultado) es lo que demuestra gestión.

---

## 6. Cómo monitorear los indicadores

### 6.1 Fuentes y automatización

- **Automático (mejor):** los sistemas ya generan el dato — SIEM (Wazuh), tickets (TheHive/GLPI), respaldos, escáneres de vulnerabilidades (OpenVAS/Trivy), Gophish, GLPI. Ver curso rsi-tools (TOOLS-04 a 12).
- **Semicargado (bien):** el dato se carga en una planilla viva (una sola fuente, ver EV-03) — p. ej. actas del Comité, informes presentados.
- **Manual (evitar):** cargas a mano sin fuente que lo respalde. Si un indicador se carga a mano siempre, revisá si sirve.

### 6.2 Tablero y reportes

| Destino | Qué se reporta | Frecuencia |
|---|---|---|
| **Comité de Seguridad** | KPIs de riesgo, incidentes, avance del plan, brechas | Mensual / trimestral |
| **División TI** | Disponibilidad, parches, MTTR, alertas (BCU-04 §9) | Mensual |
| **Directorio** | Resumen en el Informe del RSI (GV-06) con tendencias | Semestral / anual |
| **Auditoría interna** | Serie histórica y fuentes de cada indicador | A demanda |

> **Recomendación:** un tablero con **3–5 indicadores clave** ("los que el Directorio recuerda") + un detalle por función para el Comité. Pocos indicadores bien mantenidos valen más que un tablero de 20 que nadie actualiza (mismo criterio que RELEV-11).

### 6.3 Herramientas de tablero (open source)

| Herramienta | Para qué | Módulo |
|---|---|---|
| **Grafana + Loki/Prometheus** | Paneles de monitoreo y logs | TOOLS-10 |
| **Wazuh dashboard** | Alertas y eventos de seguridad | TOOLS-10 |
| **GLPI** | Tickets, inventario y disponibilidad | TOOLS-04 |
| **Eramba / planilla** | Riesgos y tratamientos | TOOLS-05 |
| **LibreOffice Calc / Excel** | Planilla viva de indicadores (si no hay tablero) | TOOLS-03 |

---

## 7. Cómo darle seguimiento (el ciclo)

1. **Cargar:** cada indicador se actualiza en su frecuencia (fuente única).
2. **Revisar:** el RSI consolida y compara contra la meta y la **tendencia** (no solo el valor del mes).
3. **Escalar:** los desvíos pasan al Comité con datos objetivos (qué pasó, causa, plan).
4. **Decidir:** el Comité aprueba acciones (recursos, cambio de metas, plan de mejora).
5. **Cerrar el ciclo:** las acciones alimentan el Plan Anual (GV-04), el Informe del RSI (GV-06) y las lecciones aprendidas (RC-04). Los cambios de metas quedan registrados (control de cambios de GV-04).

### Semáforo de seguimiento

| Estado | Criterio | Acción |
|---|---|---|
| 🟢 | Meta cumplida o mejor | Mantener; revisar meta el próximo ciclo |
| 🟡 | Desvío < 30 % de la meta | Plan de acción del responsable, seguimiento mensual |
| 🔴 | Desvío ≥ 30 % | Escalar al Comité; plan de recuperación con fecha |

---

## 8. Errores comunes al definir indicadores

- **Medir sin fuente:** números que "parecen" o se cargan de memoria. Sin fuente no es evidencia.
- **Indicadores sin meta:** "reportamos el MTTR" no es un KPI; "MTTR ≤ 8 h" sí.
- **Medir esfuerzo y venderlo como resultado:** "300 parches" no demuestra seguridad (ver §5).
- **Tablero de 20 indicadores que nadie mantiene:** menos es más (ver §6.2).
- **Meta imposible o regalada:** ambas destruyen la utilidad del indicador.
- **No revisar los indicadores:** el tablero debe evolucionar con el SGSI (se agregan/retiran indicadores en cada revisión anual).
- **Indicadores que no alimentan a nadie:** cada KPI debe tener destino (Comité, Directorio, auditoría) — si no, se elimina.

---

## 9. Cómo volcarlo a las plantillas del kit

- **GV-04 (Plan Anual):** los indicadores de avance y resultado del plan (§6 de GV-04).
- **GV-06 (Informe del RSI):** el tablero resumido con tendencias (§5 de GV-06).
- **BCU-04 (Gestión TI):** indicadores de servicio de la División TI (§9 de BCU-04, Circular 2280).
- **BCU-06 (Continuidad):** cumplimiento de pruebas, RTO/RPO (§7 de BCU-06).
- **EV-03 (Sistematización):** el registro de cada indicador (fuente, frecuencia, meta, responsable) se guarda como la planilla de evidencias.
- **ID-05 (Perfil de Ciberseguridad):** la evolución de madurez MCU 5.0 se respalda con la serie de indicadores.
- **MATRIZ-001:** el vínculo de cada indicador con el control/norma que demuestra.

---

## 10. Checklist de cierre del RSI

- ☐ Definí 1–2 indicadores por objetivo del Plan Anual (GV-04).
- ☐ Cada indicador tiene las 8 propiedades del §3 (fórmula, fuente, frecuencia, meta, responsable, decisión).
- ☐ Hay al menos un indicador de **resultado** por cada uno de **esfuerzo** (§5).
- ☐ Los indicadores cubren las 6 funciones del MCU 5.0 (tablero §4) + los ejes EMG del BCU (EV-01).
- ☐ Cada indicador tiene fuente de datos (automática si es posible) y destino de reporte.
- ☐ El seguimiento usa el semáforo del §7 y alimenta GV-04, GV-06 y el Comité.
- ☐ El registro de indicadores está guardado según EV-03 y respaldado (TOOLS-12).

---

**Documentos relacionados:** GV-04, GV-06, BCU-04, BCU-06, ID-05, ID-03, ID-04, PR-02, PR-05, PR-06, DE-01, RS-01, RS-02, RC-04, URCDP-01…04, MATRIZ-001, EV-01, EV-03, RELEV-11, rsi-tools (TOOLS-04, 05, 10, 11)
