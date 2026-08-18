# INFRA-14 · Decreto 66/025 y Obligaciones Normativas de Ciberseguridad

> **Función del MCU 5.0:** Gobernar (GV.RR Roles y responsabilidades, GV.OV Supervisión) y Responder (RS.CO Notificación) — el Decreto 66/025 transforma en **obligación formal** lo que el MCU recomienda como buena práctica.
> **ISO/IEC 27001:** Apoya el compromiso de la dirección (cláusula 5), el cumplimiento de requisitos legales (cláusula 6.1.3) y la notificación de incidentes (A.5.24–A.5.28).
> **BCU:** Complementa la EMG: el banco queda sujeto a un doble deber, ante el BCU (supervisor financiero) y ante Agesic/CERTuy (marco nacional de ciberseguridad).
> **URCDP:** Las obligaciones de notificación de incidentes de este decreto conviven con las de protección de datos (Ley 19.670 / Decreto 64/020).
> **Decreto 66/025:** Este módulo es el **núcleo normativo**: qué dice, a quién obliga, qué hay que hacer y cómo demostrarlo.
> **Nivel del curso:** 🟡 Practicar · 🔴 Dominar

---

## 1. Qué es el Decreto 66/025 y por qué te toca

El **Decreto N.º 66/025** (promulgado el 20/02/2025, publicado el 14/03/2025) reglamenta los cometidos de la **Dirección de Seguridad de la Información (DSI)** de Agesic, que estaban previstos en los artículos 55 de la Ley 18.046, 119 de la Ley 18.172, 73 de la Ley 18.362, 149 de la Ley 18.719 y 78 a 84 de la Ley 20.212.

> **Léelo así:** la Ley 20.212 (arts. 78–84) creó el régimen nacional de ciberseguridad y el **Registro Nacional de Incidentes de Ciberseguridad (RENIC)**. El Decreto 66/025 bajó ese régimen a tierra: dice qué tienen que hacer las entidades públicas en concreto, con plazos y con rendición de cuentas.

### ¿A quién obliga?

El artículo 2 del decreto extiende la aplicación a **todas las entidades públicas** y a los **entes y personas privados que prestan servicios en sectores considerados críticos**. El Banco, por ser banco público (sector financiero / banca, sector crítico según el art. 3.j) y entidad pública, queda **dentro de ambos supuestos**. No hay duda razonable sobre la aplicabilidad al Banco.

---

## 2. Las definiciones que tenés que manejar (art. 3)

| Término del decreto | Qué significa para el RSI |
|---|---|
| Evento de ciberseguridad | Cualquier ocurrencia que pueda comprometer la confidencialidad, integridad o disponibilidad |
| Incidente de ciberseguridad | Evento que efectivamente compromete (o intenta comprometer) la información o los sistemas |
| Hallazgo | Vulnerabilidad o debilidad identificada |
| SOC / CSIRT | Equipos de monitoreo y respuesta: el SOC observa; el CSIRT responde y coordina |
| RENIC | Registro Nacional de Incidentes de Ciberseguridad (Ley 20.212 art. 80) |

> **Regla práctica del RSI:** para el decreto no vale decir "no pasó nada". Si no se notifica un incidente que debía notificarse, el incumplimiento es tan grave como el incidente mismo.

---

## 3. Las obligaciones del Banco (art. 10) y dónde se demuestran

| Literal | Obligación | Cómo se demuestra en el kit |
|---|---|---|
| a | Adoptar medidas de protección apropiadas | PR-01 a PR-08, INFRA-03 a INFRA-06 |
| b | Garantizar la integridad de la información | PR-03 (cifrado), PR-05 (respaldos), INFRA-10 |
| c | **Designar un Responsable de Seguridad de la Información (RSI)** y su equipo | GV-03 (rol del RSI) |
| d | Prevenir y resolver incidentes | RS-01 (respuesta), DE-01/DE-02 (detección) |
| e | Contar con plan de mitigación y recuperación | RC-01 (BCP), RC-02 (DRP), BCU-06 |
| f | Realizar auditorías según el Marco de Ciberseguridad | ID-05 (perfil), BCU-05 (auditoría) |
| g | **Notificar los incidentes al CERTuy** conforme al procedimiento establecido | RS-02 (notificación) |

> **El dato que más te afecta (art. 10.g):** la notificación de incidentes al CERTuy es obligatoria y con plazos. La práctica y las guías nacionales apuntan a **notificación temprana** (dentro de las 24 horas de detectado el incidente). El RSI debe tener el procedimiento RS-02 actualizado con los contactos del CERTuy y el RENIC.

---

## 4. Prevención y trazabilidad (art. 11)

| Literal | Obligación | Cómo se demuestra |
|---|---|---|
| a | **Mantener trazabilidad centralizada de los eventos de seguridad por al menos 12 meses** | DE-01 (monitoreo), INFRA-12 (SIEM y retención de logs) |
| b | Proveer la información de sistemas que el CERTuy requiera | INFRA-13 (fichas de infraestructura) |
| c | Informar cambios sustanciales en los sistemas | GV-06 (informe a Dirección), control de cambios |

> **El dato que más te afecta (art. 11.a):** los registros de seguridad deben conservarse **al menos 12 meses**. Si el banco no conserva logs de ese período, ya está incumpliendo el decreto. El SIEM del INFRA-12 es la herramienta que hace esto posible y auditable.

---

## 5. Gestión de incidentes (arts. 12–13)

- **Art. 12:** la entidad debe informar de inmediato los incidentes potenciales al CERTuy, brindar la información que este requiera y reparar las consecuencias.
- **Art. 13:** si el Banco tuviera SOC/CSIRT propio, este debe reportar al CERTuy, participar en la taxonomía nacional de incidentes y mantener mecanismos de escalamiento.

> **Regla práctica:** el RSI debe saber de memoria el flujo de notificación: **detección (DE) → triage → notificación al CERTuy (RS-02) → contención → reporte final**. Ese flujo se prueba con simulaciones al menos una vez al año (DE-03).

---

## 6. Adoptar el MCU y cumplir el perfil asignado (arts. 14–15)

- **Art. 14:** las entidades deben **adoptar el Marco de Ciberseguridad (MCU)** y cumplir el **nivel de madurez mínimo** del perfil que se les asigne.
- **Art. 15:** los perfiles (básico, estándar, avanzado) y los plazos de implementación son asignados por Agesic. La asignación de perfiles y plazos debía realizarse dentro de los 60 días siguientes a la publicación del decreto.

> **Qué significa en la práctica:** el Banco debe conocer su **perfil de ciberseguridad** (ID-05 del kit), medir su madurez en las 6 funciones del MCU 5.0 y llegar al nivel mínimo del perfil asignado dentro del plazo. Esto convierte al MCU de "buena práctica" en **obligación con plazo**.

---

## 7. Auditorías y rendición de cuentas (arts. 16–17)

- **Art. 16:** las auditorías de ciberseguridad se realizan según los lineamientos del MCU.
- **Art. 17:** dentro de los **30 días** de concluida la auditoría, la entidad debe remitir a Agesic un **resumen ejecutivo**; si hay mejoras a realizar, presenta un **plan de acción dentro de los 60 días**.

> **El dato que más te afecta (arts. 16–17):** la auditoría no termina en el informe interno. Hay un **resumen ejecutivo a Agesic en 30 días** y, si corresponde, un **plan de acción en 60 días**. El kit te da la evidencia (BCU-05, ID-05, GV-06) y este curso te enseña a generarla.

---

## 8. Terceros, compras y sanciones (arts. 18–21)

| Artículo | Obligación | Repercusión en el kit |
|---|---|---|
| 18 | Los servicios de terceros deben cumplir el MCU | GV-05 (cadena de suministro), PR-08 (confidencialidad con terceros) |
| 20 | Los procesos de compras públicas deben incluir requisitos de seguridad | Cláusulas de seguridad en contratos (GV-05) |
| 21 | Apercibimiento a entidades incumplidoras y comunicación **semestral a la Asamblea General** | La rendición de cuentas puede llegar a la Asamblea General; el RSI debe dejar rastro de cumplimiento |

> **Además (Decreto 168/026, julio 2026):** se introdujo el **art. 20-BIS**, que refuerza la responsabilidad y las medidas especiales para entidades públicas en materia de procedimiento administrativo (Decretos 222/014 y 500/991) y ajustes que deben informarse a Agesic. Verificá la versión vigente del texto antes de citar el decreto en documentos formales.

---

## 9. Plan de acción del Banco ante el Decreto 66/025

| Paso | Acción | Plazo sugerido | Documento del kit |
|---|---|---|---|
| 1 | Confirmar el RSI designado y su equipo | Inmediato | GV-03 |
| 2 | Verificar el perfil asignado por Agesic y el nivel de madurez actual | 30 días | ID-05 |
| 3 | Confirmar retención de logs ≥12 meses o planificarla | 60 días | DE-01, INFRA-12 |
| 4 | Actualizar el procedimiento de notificación al CERTuy/RENIC | 60 días | RS-02 |
| 5 | Verificar cláusulas de seguridad con terceros | 90 días | GV-05, PR-08 |
| 6 | Programar auditoría según MCU y preparar resumen ejecutivo (30 días) y plan de acción (60 días) | 120 días | BCU-05, ID-05 |
| 7 | Actualizar la matriz de correspondencia normativa con el decreto | 30 días | MATRIZ-001 |

---

## 10. Relación con las demás normas (el mapa completo)

| Norma | Qué aporta | Dónde se cruza con el decreto |
|---|---|---|
| MCU 5.0 (Agesic) | Estructura de funciones y requisitos | Art. 14 (adoptar el MCU y el perfil) |
| Ley 20.212 | Régimen nacional, RENIC | Arts. 78–84 reglamentados por el decreto |
| BCU EMG / RNRCSF art. 492 | Gobierno, riesgo tecnológico, continuidad | La supervisión financiera exige lo mismo que el decreto, desde otro ángulo |
| URCDP (Ley 18.331, 19.670, Decreto 64/020) | Datos personales, vulneraciones | Las notificaciones conviven: incidente = aviso a CERTuy + URCDP según corresponda |
| ISO/IEC 27001 | SGSI y controles | La cláusula 6.1.3 exige cumplir requisitos legales: el decreto es uno de ellos |

---

## 11. Checklist del RSI ante el Decreto 66/025

- ☐ Confirmé que el Banco está comprendido (art. 2) y por qué (entidad pública + sector financiero).
- ☐ El RSI está designado por escrito (art. 10.c) → GV-03.
- ☐ Conozco el procedimiento de notificación al CERTuy y el RENIC (art. 10.g) → RS-02.
- ☐ Verifiqué la retención de logs ≥12 meses (art. 11.a) → DE-01, INFRA-12.
- ☐ Tengo el perfil de ciberseguridad asignado y medí la madurez (arts. 14–15) → ID-05.
- ☐ La auditoría sigue los lineamientos del MCU y sé los plazos de 30/60 días (arts. 16–17).
- ☐ Los contratos con terceros incluyen cumplimiento del MCU (art. 18) → GV-05.
- ☐ La matriz de correspondencia normativa incluye el decreto → MATRIZ-001.

---

## 12. Cierre del módulo

El Decreto 66/025 convierte la ciberseguridad del Banco en **obligación formal con plazos y rendición de cuentas**: RSI designado, MCU adoptado con perfil de madurez, notificación al CERTuy, logs de 12 meses y auditorías que se reportan a Agesic. Este módulo cierra el curso de infraestructura: ya sabés cómo se arma la red (INFRA-01 a 06), cómo se audita (INFRA-07), qué se observa (INFRA-12), qué se pregunta (INFRA-13) y ahora, qué exige la norma con fuerza de decreto.

### Checklist del módulo

- ☐ Leí el decreto completo (texto vigente en IMPO) y este resumen.
- ☐ Identifiqué las obligaciones que ya se cumplen y las que faltan.
- ☐ Cargué las obligaciones en la matriz de correspondencia (MATRIZ-001).

---

**Documentos relacionados:** GV-03, GV-05, GV-06, ID-05, DE-01, DE-02, RS-02, BCU-05, URCDP-02, MATRIZ-001 · Referencias internas: INFRA-12, INFRA-13 · Referencias externas: Decreto 66/025 (IMPO), Ley 20.212 arts. 78–84, Decreto 168/026 (art. 20-BIS), Marco de Ciberseguridad 5.0 (Agesic)
