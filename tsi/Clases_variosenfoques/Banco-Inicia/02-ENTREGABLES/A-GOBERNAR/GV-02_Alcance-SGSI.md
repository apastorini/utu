# GV-02 · Alcance del SGSI del Banco

> ⚠️ **Alerta:** este documento menciona **nombres propios del organigrama del Banco** (personas y cargos, abril 2026). Antes de usar el documento, verificá la vigencia de esos nombres contra el organigrama actual.
> **Función del MCU 5.0:** Gobernar (GV.OC — Contexto de la organización)
> **ISO/IEC 27001:** Cláusulas 4.1 (Contexto) · 4.2 (Partes interesadas) · 4.3 (Determinación del alcance)
> **BCU:** Estándares Mínimos de Gestión — Gobierno de la ciberseguridad
> **URCDP:** Ley 18.331 art. 10 y Decreto 64/020 (base de las medidas de seguridad)
> **Nivel del curso:** 🟢 Descubrir · 🟡 Practicar

## 1. Qué es y por qué existe
El **Alcance del SGSI** define **qué protección alcanza y qué queda fuera**: qué áreas del banco, qué procesos, qué activos de información y qué servicios prestados por terceros quedan cubiertos por el Sistema de Gestión de Seguridad de la Información. Sin alcance, ninguna auditoría puede certificar nada: no se sabría qué se evalúa ni qué se responde.
En el ciclo del SGSI se usa **inmediatamente después de aprobar la Política (GV-01)** y antes de inventariar activos (ID-01) o evaluar riesgos (ID-02): primero se delimita el terreno, después se mide lo que hay sobre él. La norma ISO/IEC 27001 lo exige en su **cláusula 4.3** ("Determinación del alcance") y el MCU 5.0 en la categoría **GV.OC**, junto con el análisis de contexto (4.1) y de partes interesadas (4.2). El BCU lo considera parte del gobierno de la ciberseguridad y la URCDP lo usa como insumo del Documento de Seguridad (URCDP-01).
Un alcance bien redactado es **específico del Banco**: no sirve un texto genérico. Debe reflejar el organigrama real del banco, sus sucursales, la red de canales (incluido **Banco En Línea**), el sistema de pagos y las tercerizaciones. Un alcance ambiguo genera conflictos en las auditorías y deja áreas sin protección asumida.

## 2. Marco de referencia
| **Requisito** | **MCU 5.0** | **ISO/IEC 27001** | **BCU** | **URCDP** |
|---|---|---|---|---|
| Contexto de la organización | GV.OC (categoría Contexto) | Cláusula 4.1 | EMG · Gobierno (conocimiento del entorno) | Decreto 64/020 art. 5 (contexto del tratamiento) |
| Determinación del alcance | GV.OC | **Cláusula 4.3** | EMG · Gobierno (alcance de la función de seguridad) | Ley 18.331 art. 10 (medidas proporcionales al alcance) |
| Partes interesadas | GV.OC | Cláusula 4.2 | EMG · Gobierno (supervisores, clientes) | Ley 18.331 art. 5-6 (titulares de datos) |
| Límites y exclusiones | GV.OC | Cláusula 4.3 (requisitos 4.1, 4.2 no excluibles) | Com. 2022/254 (tercerizaciones) | Decreto 64/020 (responsabilidad del responsable) |
| Base del inventario de activos | ID.AM | A.5.9 | EMG · Riesgo tecnológico | Decreto 414/009 (registro de bases) |

## 3. Cómo completar esta plantilla (guía de llenado)
1. **Analizá el contexto interno y externo** con la División Planificación Estratégica (Cr. Pablo Vargha): misión, visión, objetivos, posición del banco y factores externos (marco legal, sistema financiero, proveedores).
2. **Listá las partes interesadas** y su interés/expectativa en materia de seguridad: BCU, Agesic, URCDP, CERTuy, clientes, funcionarios, proveedores y sociedad en su conjunto.
3. **Describí las áreas incluidas** apoyándote en el organigrama vigente (`07-Organigrama.md`) y consultá a la División Secretaría General por la versión oficial del PDF.
4. **Determiná los procesos incluidos** (crédito hipotecario, ahorro, pagos, canales) con el Jefe de Departamento Sistema de Pagos (Cr. Guillermo Correa) y los responsables de proceso del Área Comercial (Cr. Pablo Liard).
5. **Justificá las exclusiones** por escrito: si algo queda fuera, la norma exige fundamentarlo (exclusiones del alcance), aunque contexto y partes interesadas **nunca** se pueden excluir.
6. **Validá los activos cubiertos** con el Jefe de Departamento Sistemas (Lic. Cristian Palo) y el Área Riesgos (Cra. Melissa Moraes) para que el alcance coincida con el inventario real.
7. **Revisalo con el Comité de Seguridad** y, tras la aprobación del Directorio, registralo en el control de cambios. Actualizalo ante cambios significativos (nueva sucursal, nueva línea de negocio, nueva tercerización).

## 4. Plantilla del documento

### ENCABEZADO
| **Campo** | **Valor** |
|---|---|
| **Código** | GV-02 |
| **Título** | Alcance del SGSI |
| **Versión** | 1.0 |
| **Estado** | [Borrador / En revisión / Aprobado] |
| **Fecha de aprobación** | [COMPLETAR] |
| **Elaborado por** | RSI |
| **Revisado por** | Comité de Seguridad de la Información |
| **Aprobado por** | Directorio |
| **Clasificación** | Uso interno |
| **Próxima revisión** | [Fecha, máx. 1 año] |

### 1. Contexto de la organización
**1.1 Contexto interno.** El Banco es una institución pública de intermediación financiera especializada en [COMPLETAR: vivienda, crédito hipotecario y ahorro]. Su estructura sigue el organigrama oficial (SF.PLE.05): Área Comercial, Área Operaciones y TI, Área Administración Financiera, Área Riesgos y divisiones dependientes de la Gerencia General.
**1.2 Contexto externo.** Factores relevantes: [COMPLETAR: normativa BCU y del sistema financiero, marco de ciberseguridad del Estado (Agesic), protecciones de datos personales (URCDP), situación económica y de mercado, amenazas cibernéticas, proveedores tecnológicos]. Se analizan también las expectativas de [COMPLETAR].
### 2. Partes interesadas
| **Parte interesada** | **Interés / expectativa** | **Requisito de seguridad derivado** |
|---|---|---|
| BCU (supervisor) | Solvencia, gobierno, continuidad del sistema financiero | EMG, RNRCSF art. 492, Circulares 2227 y 2419-2422 |
| Agesic / CERTuy | Cumplimiento del MCU 5.0 y coordinación de ciberseguridad | MCU 5.0; notificación de incidentes |
| URCDP | Protección de datos personales de clientes y funcionarios | Ley 18.331, Ley 19.670, Decreto 64/020 |
| Clientes (titulares de créditos, ahorristas, usuarios de Banco En Línea) | Confidencialidad de datos, disponibilidad del servicio, secreto bancario | Ley de secreto bancario; RNRCSF art. 492 |
| Funcionarios y colaboradores | Confidencialidad, formación y uso correcto de la información | Decreto 64/020 (capacitación) |
| Proveedores y terceros | Cumplimiento de cláusulas de seguridad, continuidad | GV-05; Circulares 2419-2422 |

### 3. Áreas de la organización incluidas
El SGSI alcanza a: [COMPLETAR: Área Comercial, Área Operaciones y TI, Área Administración Financiera, Área Riesgos, y las divisiones de Gerencia General —Auditoría Interna, Capital Humano, Planificación Estratégica, Servicios Jurídicos Notariales y Secretaría General—]. Incluye todas las sucursales del país y los puntos de atención al público, así como los servicios prestados por terceros que traten información del Banco.
### 4. Procesos de negocio incluidos
| **Proceso** | **Código interno [COMPLETAR]** | **Área responsable** |
|---|---|---|
| Otorgamiento y gestión de créditos hipotecarios | [COMPLETAR] | Área Comercial / Riesgos |
| Captación de ahorro y depósitos | [COMPLETAR] | Área Comercial / Administración Financiera |
| Sistema de pagos y operaciones | [COMPLETAR] | Área Operaciones y TI (Dpto. Sistema de Pagos) |
| Canales digitales (Banco En Línea, banca móvil) | [COMPLETAR] | Área Comercial (Canales y Apoyo Comercial) |
| Gestión de garantías e inmuebles | [COMPLETAR] | Área Riesgos (Seguimiento y Recuperación) |
| Gestión de recursos humanos, compras y contrataciones | [COMPLETAR] | Gerencia General / Administración Financiera |
| TI: desarrollo, producción, soporte y seguridad | [COMPLETAR] | Área Operaciones y TI (División TI) |

### 5. Procesos, actividades y activos excluidos (con justificación)
| **Proceso / activo excluido** | **Justificación de la exclusión** | **Revisión prevista** |
|---|---|---|
| [COMPLETAR: ej. sistemas legados en desuso] | [COMPLETAR: bajo riesgo, en proceso de retiro, no tratan información vigente] | [Fecha] |
| [COMPLETAR] | [COMPLETAR] | [Fecha] |

Nota: las cláusulas 4.1 (contexto) y 4.2 (partes interesadas) **no admiten exclusión**. Toda exclusión debe ser coherente con el propósito del banco y no eludir responsabilidades legales.
### 6. Activos de información cubiertos
Quedan cubiertos: información de clientes (datos personales, datos financieros, secretos bancarios), información comercial y de crédito, registros contables y financieros, información tecnológica (código fuente, configuraciones, claves), información de gobernanza y la información de terceros custodiada por el Banco. El detalle completo se mantiene en el Inventario de Activos (ID-01).
### 7. Límites físicos, organizacionales y tecnológicos
- **Físicos:** [COMPLETAR: sede central, sucursales, centros de datos propios y de terceros, archivos y custodia física].
- **Organizacionales:** dependencias del organigrama, funcionarios, contratistas y proveedores con acceso.
- **Tecnológicos:** [COMPLETAR: red corporativa, aplicaciones (incluido Banco En Línea), infraestructura, nube y servicios externos].
### 8. Actualización del alcance
Este alcance se revisa al menos anualmente o ante: cambios en el organigrama, apertura de sucursales o canales, incorporación de terceros críticos, nuevas líneas de negocio o cambios normativos relevantes.
### 9. Control de cambios
| **Versión** | **Fecha** | **Cambio** | **Elaboró** | **Aprobó** |
|---|---|---|---|---|
| 0.1 | [COMPLETAR] | Versión inicial (borrador) | RSI | — |
| 1.0 | [COMPLETAR] | Aprobación del Directorio | RSI | Directorio |

## 5. Ejemplo aplicado al Banco (modelo de referencia)
Ejemplo ilustrativo de cómo quedaría completado. Adaptalo al estado real del banco.
**Contexto externo (ejemplo):** el Banco opera como institución financiera pública supervisada por el BCU, sujeta al secreto bancario y a la Recopilación de Normas de Regulación y Control del Sistema Financiero. Como organismo del Estado, cumple el Marco de Ciberseguridad 5.0 de Agesic y las directivas de CERTuy, además de la Ley 18.331 y su decreto reglamentario 64/020 en materia de datos personales. Factores económicos, el aumento de la ciberdelincuencia financiera y la evolución de los pagos digitales condicionan el perfil de riesgo.
**Partes interesadas (ejemplo):** el BCU espera gobierno y continuidad; Agesic y CERTuy esperan alineación al MCU 5.0 y notificación de incidentes; la URCDP espera el cumplimiento de datos personales; los clientes hipotecarios y ahorristas esperan que sus secretos bancarios y credenciales de Banco En Línea estén protegidos y que los servicios estén disponibles; los funcionarios esperan herramientas seguras y capacitación.
**Áreas incluidas (ejemplo):** todas las áreas del organigrama oficial: Área Comercial (Cr. Pablo Liard), Área Operaciones y TI (División TI a cargo del Lic. Bernardo Ureta y División Operaciones a cargo de la Ec. Analía Cortizo), Área Administración Financiera (Cra. Soledad Carreres), Área Riesgos (Ec. Laura Zunino), y las divisiones de Gerencia General (Auditoría Interna, Capital Humano, Planificación Estratégica, Servicios Jurídicos Notariales, Secretaría General). Incluye sucursales y los servicios tercerizados con tratamiento de información.
**Procesos incluidos (ejemplo):** otorgamiento y gestión de créditos hipotecarios; captación de ahorro y depósitos; el sistema de pagos del banco (Jefe de Departamento Sistema de Pagos, Cr. Guillermo Correa); los canales Banco En Línea y atención personalizada (Cra. Viviana Trabuco y Sr. Alejandro Pereyra); la gestión de garantías e inmuebles (Sr. Pablo Lorenzo) y la gestión de morosidad (Sra. Alejandra Olivera).
**Exclusiones justificadas (ejemplo):** los sistemas legados de préstamos ya dados de baja en producción (no tratan datos vigentes; permanecen en archivo histórico fuera de línea) y los soportes de prensa y comunicación institucional no confidenciales, que se rigen por normas de difusión y no por el SGSI.

**Documentos relacionados:** GV-01 (Política), GV-03 (Roles y Comité), ID-01 (Inventario de Activos), BCU-01 (Gobierno de Ciberseguridad), URCDP-01 (Documento de Seguridad), MATRIZ-001 (Correspondencia Normativa).
