# Banco-Inicia · Kit para la puesta en marcha del SGSI del Banco Hipotecario del Uruguay

> **Qué es esto:** un curso + taller + biblioteca de plantillas para que el **Banco Hipotecario del Uruguay** diseñe, documente e implemente su **Sistema de Gestión de Seguridad de la Información (SGSI)**, alineado con lo que exigen y esperan **Agesic**, el **BCU** y la **URCDP**.
>
> **Para quién:** el **Responsable de Seguridad de la Información (RSI)**, su equipo, la alta dirección y cualquier persona que deba entender y sostener la seguridad de la información del Banco. **No requiere conocimientos previos**: el README te guía desde cero hasta un nivel experto.

---

## 1. Bienvenida: ¿por qué este material?

El Banco es una institución de intermediación financiera del Estado uruguayo, supervisado por el **Banco Central del Uruguay (BCU)**. Esto significa que está obligado a cumplir simultáneamente con:

| Organismo | Qué exige | Norma de referencia |
|---|---|---|
| **Agesic** (Agencia de Gobierno Electrónico y Sociedad de la Información y del Conocimiento) | Implementar el **Marco de Ciberseguridad 5.0 (MCU 5.0)** para gestionar riesgos de ciberseguridad | MCU 5.0, basado en **NIST CSF 2.0** (6 funciones, 72 requisitos) |
| **BCU** | Aplicar la **Guía de los Estándares Mínimos de Gestión (EMG) relativos a la Seguridad de la Información** para entidades supervisadas | EMG vigentes desde 31/10/2021 (metodología CERT) |
| **URCDP** | Cumplir la normativa de **protección de datos personales** y su régimen de **vulneraciones de seguridad** | Ley 18.331, Ley 19.670, Decreto 64/020 |
| **Agesic · Decreto 66/025** | Reglamenta los cometidos de la **Dirección de Seguridad de la Información de Agesic**: designar RSI, adoptar el MCU, notificar incidentes al CERTuy, trazabilidad ≥12 meses y auditorías según MCU | Decreto 66/025 · Ley 20.212 (arts. 78–84) |
| **ISO/IEC 27001** | Buenas prácticas internacionales de gestión de seguridad de la información (SGSI) | ISO/IEC 27001:2013/2022 |

Este kit traduce ese entramado normativo en **documentos listos para adaptar**, un **camino paso a paso** y una **estructura de carpetas** para que el SGSI del Banco quede operativo y auditable.

---

## 2. Cómo usar este kit (el método)

Pensalo como un **curso autoasistido de 7 módulos** + **46 plantillas de documentos** + **un curso de infraestructura de red (15 módulos)** + **un curso de relevamiento organizacional (12 módulos)** + **un curso de herramientas open source para el RSI (15 módulos)** + **un curso de gestión de vulnerabilidades y redacción de políticas (VPOL-00…VPOL-21, con las 15 plantillas de políticas de ISACA adaptadas a Uruguay)** + **planificación**. La lógica es siempre la misma:

1. **Aprendé el concepto** en los módulos del curso (`01-CURSO-RSI/`).
2. **Entendé qué documento necesitás** según la función del MCU 5.0 o la norma.
3. **Abrí la plantilla** (`.md` editable y su versión `.docx` lista para firmar/aprobar).
4. **Completala con el caso Banco**: cada plantilla incluye un *ejemplo de llenado*.
5. **Guardala** en la estructura de carpetas del SGSI (`00-PLANIFICACION/00-Estructura-Carpetas-SGSI.md`).
6. **Seguila en la planificación** (`00-PLANIFICACION/00-Planificacion-SGSI.md`).

> **Consejo:** no intentes completar todo en una semana. El SGSI se construye por etapas (ver planificación de 18 meses). Empezá por **Gobernar** y **Identificar** (política, alcance, inventario de activos y análisis de riesgos); eso ya te posiciona por encima de la media de las instituciones que recién comienzan.

### 2.1 Los tres niveles de profundidad

Cada documento del curso indica su nivel:

- 🟢 **Nivel 1 · Descubrir** — entendé de qué se trata (sin conocimientos técnicos). Ideal para directivos y personal nuevo.
- 🟡 **Nivel 2 · Practicar** — aprendés a hacerlo (RSI, oficiales de seguridad, TI).
- 🔴 **Nivel 3 · Dominar** — nivel experto: auditorías, mejora continua, integración con riesgos y continuidad.

---

## 3. Estructura de este repositorio (índice)

```
Banco-Inicia/
├── README.md                                  ← ESTE ARCHIVO: índice y guía del curso
├── 00-PLANIFICACION/                          ← Dónde empezar como proyecto
│   ├── 00-Planificacion-SGSI.md           ← Cronograma paso a paso (18 meses)
│   ├── 00-Estructura-Carpetas-SGSI.md         ← Estructura de carpetas del SGSI operativo
│   └── 00-Matriz-Correspondencia-Normativa.md ← Matriz MCU 5.0 ↔ ISO 27001 ↔ BCU ↔ URCDP
├── 01-CURSO-RSI/                                  ← Los 7 módulos del curso
│   ├── 01-Marco-Normativo-Uruguay.md
│   ├── 02-Marco-Ciberseguridad-50-Agesic.md
│   ├── 03-SGSI-ISO-27001.md
│   ├── 04-Rol-RSI.md
│   ├── 05-BCU-Estandares-Minimos-Gestion.md
│   ├── 06-URCDP-Proteccion-Datos-Personales.md
│   ├── 07-Organigrama.md
│   └── 08-Dia-a-Dia-del-RSI.md
├── 02-ENTREGABLES/                            ← Las plantillas de documentos (md + docx)
│   ├── A-GOBERNAR/      (GV-01 … GV-06)
│   ├── B-IDENTIFICAR/   (ID-01 … ID-05)
│   ├── C-PROTEGER/      (PR-01 … PR-08)
│   ├── D-DETECTAR/      (DE-01 … DE-03)
│   ├── E-RESPONDER/     (RS-01 … RS-03)
│   ├── F-RECUPERAR/     (RC-01 … RC-04)
│   ├── G-BCU/           (BCU-01 … BCU-06)
│   ├── H-URCDP/         (URCDP-01 … URCDP-06)
│   └── I-EVIDENCIA/     (EV-01 … EV-05 · checklists de evidencia BCU, por control, sistematización, por área e indicadores)
├── curso-infra/                    (INFRA-00 … INFRA-14 · curso de redes y ciberseguridad, incluye Decreto 66/025)
├── Curso-relevamiento/             (RELEV-00 … RELEV-11 · curso de relevamiento: agenda, reuniones y evidencias)
├── rsi-tools/                      (TOOLS-00 … TOOLS-14 · curso de herramientas open source para el RSI/CISO)
├── curso-politicas-vulnerabilidades/  (VPOL-00 … VPOL-30 · gestión de vulnerabilidades y redacción de políticas/procesos/controles, con 15 plantillas ISACA en templates-ISACA/ y el cuerpo normativo completo — 20 políticas, 10 procesos y 13 procedimientos — en politicas/)
├── curso-ia-segura/                   (AISEC-00 … AISEC-14 · curso de IA y ciberseguridad: LLMs, OpenCode/BigPickle/Ollama/vLLM, RAG, versionado de modelos offline, normativa uruguaya, plan para 300 funcionarios)
└── 03-HERRAMIENTAS/
    └── md_a_docx.py                          ← Convierte cada plantilla .md en .docx
```

### 3.1 Ruta de aprendizaje recomendada (resumen del índice)

| Orden | Tema | Archivo | Nivel |
|---|---|---|---|
| 1 | El marco normativo uruguayo que te obliga | `01-CURSO-RSI/01-Marco-Normativo-Uruguay.md` | 🟢 |
| 2 | El Marco de Ciberseguridad 5.0 de Agesic (6 funciones, 72 requisitos) | `01-CURSO-RSI/02-Marco-Ciberseguridad-50-Agesic.md` | 🟢→🟡 |
| 3 | Qué es un SGSI y cómo se implementa (ISO 27001) | `01-CURSO-RSI/03-SGSI-ISO-27001.md` | 🟡 |
| 4 | Tu rol: el RSI y el gobierno de la seguridad | `01-CURSO-RSI/04-Rol-RSI.md` | 🟡→🔴 |
| 5 | Lo que el BCU espera de ti (EMG) | `01-CURSO-RSI/05-BCU-Estandares-Minimos-Gestion.md` | 🟡→🔴 |
| 6 | Datos personales: obligaciones ante la URCDP | `01-CURSO-RSI/06-URCDP-Proteccion-Datos-Personales.md` | 🟡→🔴 |
| 7 | El organigrama del Banco y dónde vive cada responsabilidad | `01-CURSO-RSI/07-Organigrama.md` | 🟢 |
| 8 | El día a día del RSI: agenda realista, conversaciones y cómo no quemarte | `01-CURSO-RSI/08-Dia-a-Dia-del-RSI.md` | 🔴 |
| 9 | El plan de trabajo (cronograma) | `00-PLANIFICACION/00-Planificacion-SGSI.md` | 🔴 |
| 10 | Dónde guardar cada cosa (carpetas) | `00-PLANIFICACION/00-Estructura-Carpetas-SGSI.md` | 🟢 |
| 11 | La matriz que demuestra cumplimiento | `00-PLANIFICACION/00-Matriz-Correspondencia-Normativa.md` | 🔴 |

---

## 4. Los entregables (plantillas de documentos)

Cada carpeta de `02-ENTREGABLES/` corresponde a una **función del MCU 5.0** (más carpetas específicas para BCU, URCDP y evidencia). Todas las plantillas están en `.md` (para editar con cualquier editor) y tienen su versión **`.docx`** (para el circuito de firma y aprobación).

### A · GOBERNAR (GV) — el marco que decide la dirección
| Código | Documento | Norma principal |
|---|---|---|
| GV-01 | Política de Seguridad de la Información | MCU 5.0 · GV.PO |
| GV-02 | Alcance del SGSI | ISO 27001 (4.3) · BCU EMG |
| GV-03 | Roles, responsabilidades y Comité de Seguridad (incluye RSI) | MCU 5.0 · GV.RR · BCU EMG |
| GV-04 | Plan Anual de Seguridad de la Información | MCU 5.0 · GV.OV · GV.RM |
| GV-05 | Gestión de riesgos de la cadena de suministro (proveedores) | MCU 5.0 · GV.SC · BCU (tercerización) |
| GV-06 | Informe del RSI a la Dirección (supervisión del SGSI) | MCU 5.0 · GV.OV · BCU EMG |

### B · IDENTIFICAR (ID) — saber qué tenemos y qué puede salir mal
| Código | Documento | Norma principal |
|---|---|---|
| ID-01 | Inventario de Activos de Información | MCU 5.0 · ID.AM · ISO 27001 A.5.9 |
| ID-02 | Metodología de Análisis y Evaluación de Riesgos | MCU 5.0 · ID.RA · BCU EMG · ISO 27005 |
| ID-03 | Análisis de Riesgos (caso Banco) — planilla de cálculo | MCU 5.0 · ID.RA |
| ID-04 | Plan de Tratamiento de Riesgos | MCU 5.0 · GV.RM · ISO 27001 A.6.8 |
| ID-05 | Perfil de Ciberseguridad del Banco (estado actual / objetivo) | MCU 5.0 · Perfiles |

### C · PROTEGER (PR) — las defensas
| Código | Documento | Norma principal |
|---|---|---|
| PR-01 | Política de Control de Acceso y Gestión de Identidades | MCU 5.0 · PR.AA |
| PR-02 | Programa de Concientización y Capacitación | MCU 5.0 · PR.AT · BCU |
| PR-03 | Política de Seguridad de Datos (clasificación, cifrado) | MCU 5.0 · PR.DS · URCDP |
| PR-04 | Política de Seguridad Física y del Entorno | MCU 5.0 · PR.AA-06 |
| PR-05 | Política de Respaldo y Recuperación de la Información | MCU 5.0 · PR.IR |
| PR-06 | Gestión de Vulnerabilidades y Parches | MCU 5.0 · PR.PS |
| PR-07 | Seguridad en el Desarrollo de Software (SDLC) | MCU 5.0 · PR.PS |
| PR-08 | Acuerdo de Confidencialidad y Cláusulas con Terceros | MCU 5.0 · GV.SC · BCU |

### D · DETECTAR (DE) — ver lo que pasa
| Código | Documento | Norma principal |
|---|---|---|
| DE-01 | Política de Monitoreo y Registro de Eventos | MCU 5.0 · DE.CM |
| DE-02 | Procedimiento de Detección de Anomalías e Intrusiones | MCU 5.0 · DE.AE |
| DE-03 | Programa de Pruebas de Seguridad (pentest / red team) | MCU 5.0 · DE.CM · BCU |

### E · RESPONDER (RS) — reaccionar ante el incidente
| Código | Documento | Norma principal |
|---|---|---|
| RS-01 | Plan de Respuesta a Incidentes de Seguridad | MCU 5.0 · RS.MA · ISO 27035 |
| RS-02 | Procedimiento de Notificación y Comunicación de Incidentes | URCDP (72 h) · BCU · CERTuy |
| RS-03 | Análisis Forense y Preservación de Evidencia | MCU 5.0 · RS.AN |

### F · RECUPERAR (RC) — volver a operar
| Código | Documento | Norma principal |
|---|---|---|
| RC-01 | Plan de Continuidad del Negocio (BCP) | MCU 5.0 · RC.RP · BCU EMG |
| RC-02 | Plan de Recuperación ante Desastres (DRP) | MCU 5.0 · RC.RP |
| RC-03 | Plan de Comunicación de Crisis | MCU 5.0 · RC.CO |
| RC-04 | Lecciones Aprendidas y Mejora Continua | MCU 5.0 · ID.IM · ISO 27001 (10) |

### G · BCU — estándares mínimos de gestión (EMG)
| Código | Documento | Norma principal |
|---|---|---|
| BCU-01 | Gobierno de Ciberseguridad y Política de Administración de Riesgo Tecnológico | BCU EMG (Gobierno) |
| BCU-02 | Marco de Gestión de Riesgos (apetito y adopción de riesgo) | BCU EMG (Marco de Riesgos) |
| BCU-03 | Función de Seguridad de la Información (segunda línea de defensa) | BCU EMG |
| BCU-04 | Función de Gestión de Tecnologías de la Información | BCU EMG |
| BCU-05 | Programa de Auditoría Interna de Seguridad | BCU EMG (Auditoría) |
| BCU-06 | Plan de Contingencia y Continuidad del Negocio | BCU EMG (Continuidad) |

### H · URCDP — protección de datos personales
| Código | Documento | Norma principal |
|---|---|---|
| URCDP-01 | Documento de Seguridad de Datos Personales | Ley 18.331 (art. 10) · Decreto 64/020 |
| URCDP-02 | Procedimiento de Notificación de Vulneraciones de Seguridad | Ley 19.670 (art. 38) · Decreto 64/020 |
| URCDP-03 | Procedimiento de Atención de Derechos ARCO | Ley 18.331 (art. 14–17) |
| URCDP-04 | Inscripción de Bases de Datos ante la URCDP | Ley 18.331 (art. 22) |
| URCDP-05 | Evaluación de Impacto de Protección de Datos (DPIA) | Ley 18.331 (art. 12) · Decreto 64/020 |
| URCDP-06 | Designación del Delegado de Protección de Datos (DPD) | Ley 19.670 |

### I · EVIDENCIA (EV) — checklists de trabajo del RSI
| Código | Documento | Para qué sirve |
|---|---|---|
| EV-01 | Checklist de Requisitos del BCU (EMG y normativa complementaria) | Qué pide el BCU, en qué documento del kit y sección se evidencia |
| EV-02 | Checklist de Evidencias por Control | Qué evidencia pedir por control, con varias opciones (basta una) |
| EV-03 | Sistematización de las Evidencias | Dónde guardar, cómo nombrar y cómo seguir las evidencias |
| EV-04 | Evidencias por Área, División y Sector | Qué evidencia esperar de cada área y cómo ayudarlas a entregarla |
| EV-05 | Indicadores y Métricas del SGSI | Cómo definir, monitorear y dar seguimiento a los indicadores (métrica vs. KPI, metas, tablero por función MCU 5.0) |

---

## 5. Los 7 pasos para generar tu SGSI (resumen ejecutivo)

El detalle completo está en `00-PLANIFICACION/00-Planificacion-SGSI.md`. En una línea:

1. **Apoyo de la dirección** → se aprueba la Política (GV-01) y se designa al RSI (GV-03).
2. **Definir el alcance** → qué áreas, sistemas y procesos quedan dentro (GV-02).
3. **Inventariar y valorar** → activos (ID-01) y riesgos (ID-02/03).
4. **Tratar los riesgos** → plan de tratamiento (ID-04) y controles de Proteger (C).
5. **Vigilar y responder** → Detectar (D) y Responder (E).
6. **Sostener la operación** → Recuperar (F) y continuidad (RC-01/02).
7. **Medir y mejorar** → informes del RSI (GV-06), auditorías (BCU-05), lecciones aprendidas (RC-04).

> Regla de oro: **la seguridad es un proceso, no un proyecto**. El SGSI nunca "termina"; se revisa y mejora continuamente (ciclo PDCA de ISO 27001).

---

## 6. Herramientas del kit

- `03-HERRAMIENTAS/md_a_docx.py` — convierte automáticamente a `.docx` los documentos `.md` del curso, la planificación y las **46 plantillas canónicas** de `02-ENTREGABLES/` más los **15 módulos del curso de infraestructura** (`curso-infra/`), los **12 módulos del curso de relevamiento** (`Curso-relevamiento/`), los **15 módulos del curso de herramientas RSI** (`rsi-tools/`), los **22 módulos del curso de políticas y vulnerabilidades** (`curso-politicas-vulnerabilidades/`, incluidos los 15 templates ISACA y el cuerpo normativo de `politicas/` — 20 políticas, 10 procesos y 13 procedimientos) y los **15 módulos del curso de IA y ciberseguridad** (`curso-ia-segura/`) (la lista de documentos está en `03-HERRAMIENTAS/canonicos.txt`). Requiere Python 3 y `python-docx` (ya instalados en este entorno). Uso:
  ```
  python 03-HERRAMIENTAS/md_a_docx.py
  ```
- Cada plantilla `.md` puede editarse con cualquier editor (VS Code, Notepad++, etc.) y luego regenerar el `.docx`.
- Para la planilla de riesgos (ID-03) podés usar la **plantilla oficial de Agesic** "Implantación SGSI – Inventario activos y Evaluación riesgos (.xlsx)" descargable desde el sitio de Agesic.

---

## 7. Referencias oficiales

| Recurso | Enlace |
|---|---|
| Marco de Ciberseguridad 5.0 (Agesic) | https://www.gub.uy/agencia-gobierno-electronico-sociedad-informacion-conocimiento/comunicacion/publicaciones/marco-ciberseguridad-50 |
| Guía de implementación MCU 5.0 | https://www.gub.uy/agencia-gobierno-electronico-sociedad-informacion-conocimiento/comunicacion/publicaciones/guia-implementacion-del-mcu-50 |
| Guía SGSI de Agesic (inventario de activos y riesgos .xlsx) | https://www.gub.uy/agencia-gobierno-electronico-sociedad-informacion-conocimiento/comunicacion/publicaciones/guias-sobre-marco-ciberseguridad |
| BCU · EMG (Estándares Mínimos de Gestión) | https://www.bcu.gub.uy/Servicios-Financieros-SSF/Paginas/Estandares-Minimos-No-Bancarias.aspx |
| URCDP · Guía de vulneraciones de seguridad | https://www.gub.uy/unidad-reguladora-control-datos-personales |
| Ley 18.331 (protección de datos personales) | https://www.impo.com.uy/bases/leyes/18331-2008 |
| Decreto 64/020 | https://www.redipd.org/sites/default/files/2020-03/decreto-64-020-reglamento-ley-19670.pdf |
| Organigrama del Banco | https://www.bhu.com.uy/sobre-bhu/organigrama |

---

## 8. Glosario rápido

- **SGSI / ISMS** — Sistema de Gestión de Seguridad de la Información.
- **RSI** — Responsable de Seguridad de la Información (segunda línea de defensa).
- **MCU 5.0** — Marco de Ciberseguridad de Agesic, versión 5.0 (basado en NIST CSF 2.0).
- **EMG** — Estándares Mínimos de Gestión del BCU.
- **URCDP** — Unidad Reguladora y de Control de Datos Personales.
- **CERTuy** — Centro Nacional de Respuesta a Incidentes de Seguridad Informática.
- **CID** — Confidencialidad, Integridad y Disponibilidad.
- **PDCA** — Planificar, Hacer, Verificar, Actuar.
- **DPD** — Delegado de Protección de Datos.
- **ARCO** — Acceso, Rectificación, Cancelación (supresión), Oposición.
- **BCP / DRP** — Continuidad del Negocio / Recuperación ante Desastres.

---

**Siguiente paso:** abrí `00-PLANIFICACION/00-Planificacion-SGSI.md` para arrancar con el cronograma, o `01-CURSO-RSI/01-Marco-Normativo-Uruguay.md` para aprender la base normativa.
