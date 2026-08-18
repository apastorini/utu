# ID-05 · Perfil de Ciberseguridad del Banco

> ⚠️ **Alerta:** este documento menciona **nombres propios del organigrama del Banco** (personas y cargos, abril 2026). Antes de usar el documento, verificá la vigencia de esos nombres contra el organigrama actual.
> **Función del MCU 5.0:** Identificar (ID.IM — Estrategia de mejora) · Modelo de perfiles y madurez del MCU 5.0
> **ISO/IEC 27001:** Cláusula 6.2 (Objetivos) · Cláusula 9.1 (Evaluación del desempeño) · A.5.1 (referencia)
> **BCU:** EMG · Marco de Riesgos y Gobierno de Ciberseguridad
> **URCDP:** Ley 18.331 art. 10 (medidas adecuadas) · Decreto 64/020
> **Nivel del curso:** 🟡 Practicar · 🔴 Aplicar

## 1. Qué es y por qué existe
El **Perfil de Ciberseguridad del Banco** es la foto que muestra **dónde está hoy el banco y a dónde quiere llegar** en materia de ciberseguridad, según el modelo del MCU 5.0 de Agesic. Se construye puntuando el estado **actual** y el estado **objetivo** de cada subcategoría de las 6 funciones (GV, ID, PR, DE, RS, RC), usando la escala de madurez y la lista de verificación oficial de Agesic.
Es el documento que permite **medir el progreso**: cada año el Banco re-evalúa su madurez y compara. Así se demuestra mejora continua ante Agesic (que audita con su guía y lista de verificación), se justifican las inversiones (las brechas dicen qué falta) y se prioriza el plan de acción de forma objetiva y no por intuición.
El MCU 5.0 define **tres perfiles de prioridad** —Básico, Estándar y Avanzado— según el riesgo percibido y la tolerancia a la indisponibilidad. Por ser un banco estatal que opera el sistema de pagos y administra el ahorro y el crédito de la población, el Banco debe apuntar al **perfil Avanzado**, con tolerancia de recuperación de **no más de 24 horas** para sus servicios críticos. El perfil recomendado define qué requisitos se implementan primero: los de prioridad alta del perfil Avanzado.
## 2. Marco de referencia
| **Marco** | **Referencia** | **Qué exige aplicable al Banco** |
|---|---|---|
| **MCU 5.0 (Agesic)** | Modelo de perfiles (Básico/Estándar/Avanzado), modelo de madurez, lista de verificación y guía de auditoría | Autoevaluación del estado actual, definición del perfil objetivo y plan de acción por brecha |
| **ISO/IEC 27001** | Cláusula 6.2, 9.1, 10 | Objetivos medibles, monitoreo del desempeño y mejora continua |
| **BCU** | EMG · Marco de Riesgos y Gobierno de Ciberseguridad | Demostrar gestión estructurada del riesgo de ciberseguridad |
| **URCDP** | Ley 18.331 art. 10 | Nivel de madurez suficiente para garantizar la seguridad de los datos personales |

## 3. Cómo completar esta plantilla (guía de llenado)
1. **Descargá la lista de verificación editable del MCU 5.0** (sitio de Agesic) y la guía de auditoría: son la fuente oficial de subcategorías y criterios.
2. **Definí el perfil objetivo con la dirección:** para el Banco se recomienda **Avanzado** (riesgo alto, servicios críticos, tolerancia 24 h). Documentá esa decisión en el encabezado.
3. **Hacé la autoevaluación del estado actual:** puntuá cada subcategoría de las 6 funciones con la escala de madurez 0-5 (punto 3 del documento), con evidencia real (políticas aprobadas, controles implementados, pruebas realizadas). No puntúes "de memoria": cada punto debe tener evidencia.
4. **Mantené fijo el perfil objetivo** mientras puntuás el actual: la brecha es la diferencia entre ambos.
5. **Calculá las brechas** por función y subcategoría, y volcalas en la tabla del punto 5.
6. **Construí el plan de acción por brecha:** para cada brecha, una acción con responsable y plazo. Vinculá las acciones con el plan de tratamiento (ID-04) para no duplicar esfuerzos.
7. **Consultá en el Banco:** el RSI coordina la autoevaluación; División TI (Bernardo Ureta) aporta la evidencia técnica (ID, PR, DE); Área de Riesgos (Melissa Moraes) la de gobierno y riesgos; el DPD la de protección de datos; y el Comité de Seguridad aprueba el perfil y el plan.
8. **Re-evaluá anualmente** y registrá la evolución: el objetivo es que la curva de madurez suba cada año y que las brechas del perfil objetivo se cierren.
## 4. Plantilla del documento

### ENCABEZADO
| **Campo** | **Valor** |
|---|---|
| **Código** | ID-05 |
| **Título** | Perfil de Ciberseguridad del Banco |
| **Versión** | 1.0 |
| **Estado** | [Borrador / En revisión / Aprobado] |
| **Fecha de aprobación** | [COMPLETAR] |
| **Elaborado por** | RSI con el apoyo de División TI y Área de Riesgos |
| **Revisado por** | Comité de Seguridad de la Información |
| **Aprobado por** | Comité de Seguridad · Gerencia General |
| **Clasificación** | Uso interno |
| **Próxima revisión** | [Fecha, máx. 1 año] |

### 1. Objetivo
Establecer el perfil de ciberseguridad actual y objetivo del Banco según el MCU 5.0, identificar las brechas de madurez y definir el plan de acción para cerrarlas.
### 2. Perfil seleccionado
| **Campo** | **Valor** |
|---|---|
| **Perfil objetivo** | [Básico / Estándar / **Avanzado (recomendado)**] |
| **Justificación** | El Banco es un banco estatal, administra ahorro y crédito de la población y opera el sistema de pagos: riesgo alto y servicios críticos, por lo que la tolerancia de recuperación máxima es de 24 horas corridas |
| **Fecha de autoevaluación** | [COMPLETAR] |

### 3. Escala de madurez (modelo MCU 5.0)
| **Nivel** | **Nombre** | **Descripción** |
|---|---|---|
| 0 | Inexistente | No existe práctica ni evidencia |
| 1 | Inicial | Prácticas ad-hoc, sin proceso definido ni documentado |
| 2 | Gestionado | Proceso definido, documentado y con responsables, pero sin medir |
| 3 | Definido | Proceso estandarizado, con indicadores y aplicado en toda la organización |
| 4 | Medido | El proceso se mide, analiza y reporta regularmente |
| 5 | Optimizado | El proceso se mejora continuamente con datos y mejores prácticas |

### 4. Autoevaluación por función
[COMPLETAR: completar una fila por función y por subcategoría prioritaria. Formato de referencia:]
| **Función** | **Subcategoría (MCU 5.0)** | **Actual (0-5)** | **Objetivo (0-5)** | **Brecha** | **Evidencia** |
|---|---|---|---|---|---|
| **GV** | GV.PO — Política | [0-5] | [0-5] | [COMPLETAR] | GV-01 aprobada |
| **GV** | GV.OV — Supervisión | [0-5] | [0-5] | [COMPLETAR] | Informes GV-06 |
| **ID** | ID.AM — Gestión de activos | [0-5] | [0-5] | [COMPLETAR] | ID-01 |
| **ID** | ID.RA — Evaluación de riesgos | [0-5] | [0-5] | [COMPLETAR] | ID-02/03 |
| **PR** | PR.AT — Concientización | [0-5] | [0-5] | [COMPLETAR] | PR-02 |
| **PR** | PR.PS — Seguridad de plataformas | [0-5] | [0-5] | [COMPLETAR] | PR-06, PR-05 |
| **DE** | DE.CM — Monitoreo continuo | [0-5] | [0-5] | [COMPLETAR] | DE-01 |
| **RS** | RS.MA — Gestión de incidentes | [0-5] | [0-5] | [COMPLETAR] | RS-01 |
| **RC** | RC.RP — Ejecución del plan de recuperación | [0-5] | [0-5] | [COMPLETAR] | RC-01/02 |

### 5. Resumen de brechas por función
| **Función** | **Promedio actual** | **Promedio objetivo** | **Brecha total** | **Prioridad** |
|---|---|---|---|---|
| GV | [COMPLETAR] | [COMPLETAR] | [COMPLETAR] | [Alta/Media] |
| ID | [COMPLETAR] | [COMPLETAR] | [COMPLETAR] | [COMPLETAR] |
| PR | [COMPLETAR] | [COMPLETAR] | [COMPLETAR] | [COMPLETAR] |
| DE | [COMPLETAR] | [COMPLETAR] | [COMPLETAR] | [COMPLETAR] |
| RS | [COMPLETAR] | [COMPLETAR] | [COMPLETAR] | [COMPLETAR] |
| RC | [COMPLETAR] | [COMPLETAR] | [COMPLETAR] | [COMPLETAR] |

### 6. Plan de acción por brecha
| **Brecha** | **Acción propuesta** | **Control vinculado (ISO)** | **Responsable** | **Plazo** |
|---|---|---|---|---|
| [COMPLETAR] | [COMPLETAR] | [COMPLETAR] | [COMPLETAR] | [COMPLETAR] |

### 7. Control de cambios
| **Versión** | **Fecha** | **Cambio** | **Elaboró** | **Aprobó** |
|---|---|---|---|---|
| 0.1 | [COMPLETAR] | Primera autoevaluación | RSI | — |
| 1.0 | [COMPLETAR] | Aprobación del perfil y plan de acción | RSI | Comité |

## 5. Ejemplo aplicado al Banco (modelo de referencia)
Ejemplo ilustrativo de una autoevaluación inicial realista: un banco que recién arma su SGSI. Puntajes de referencia.
| **Función** | **Subcategoría** | **Actual** | **Objetivo** | **Brecha** | **Evidencia** |
|---|---|---|---|---|---|
| **GV** | GV.PO — Políticas | 1 | 3 | 2 | Política GV-01 recién aprobada |
| **GV** | GV.OV — Supervisión | 1 | 3 | 2 | RSI designado; informe semestral a definir |
| **ID** | ID.AM — Activos | 2 | 3 | 1 | Inventario ID-01 inicial, sin cruzar con todos los procesos |
| **ID** | ID.RA — Riesgos | 1 | 3 | 2 | Primera evaluación ID-03 en curso |
| **PR** | PR.AT — Concientización | 1 | 3 | 2 | Sin programa formal PR-02 |
| **PR** | PR.PS — Seguridad de plataformas | 2 | 3 | 1 | Antivirus y firewall; sin EDR ni segmentación completa |
| **DE** | DE.CM — Monitoreo | 1 | 3 | 2 | Sin SIEM; logs parciales |
| **RS** | RS.MA — Gestión de incidentes | 1 | 3 | 2 | Sin plan RS-01 aprobado |
| **RC** | RC.RP — Ejecución del plan de recuperación | 2 | 3 | 1 | Respaldos del core; DRP sin probar |

**Plan de acción (ejemplo):** con el objetivo en nivel 3 ("Definido") y perfil Avanzado, las acciones prioritarias del primer año son: aprobar RS-01 (respuesta a incidentes), implementar el programa PR-02 (concientización), contratar un SIEM (DE-01) y probar el DRP del sistema de pagos (RC-02). Cada una con responsable y plazo, y alineada a los riesgos R-001, R-003 y R-006 de ID-03.
**Evolución esperada (ejemplo):** año 1 promedio actual ≈ 1,5; año 2 objetivo ≥ 2,5; año 3 consolidar el perfil Avanzado con promedio ≥ 3,5 y sin brechas en las subcategorías de los activos críticos.

**Documentos relacionados:** ID-01 (Activos) · ID-02/03 (Riesgos) · ID-04 (Tratamiento) · GV-06 (Informe del RSI) · BCU-01 (Gobierno de ciberseguridad) · DE-01 (Monitoreo) · RS-01 (Respuesta a incidentes) · RC-02 (DRP).
