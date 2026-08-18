# ID-03 · Análisis de Riesgos del caso Banco

> ⚠️ **Alerta:** este documento menciona **nombres propios del organigrama del Banco** (personas y cargos, abril 2026). Antes de usar el documento, verificá la vigencia de esos nombres contra el organigrama actual.
> **Función del MCU 5.0:** Identificar (ID.RA — Evaluación de riesgos)
> **ISO/IEC 27001:** Cláusula 6.1.2 (Evaluación de riesgos de seguridad de la información) · Cláusula 8.2
> **BCU:** Circular 2227 (riesgo operacional) · EMG · Marco de Riesgos
> **URCDP:** Ley 18.331 art. 10 (medidas proporcionales al riesgo) · Decreto 64/020
> **Nivel del curso:** 🟡 Practicar · 🔴 Aplicar

## 1. Qué es y por qué existe
El **Análisis de Riesgos del caso Banco** es la **aplicación concreta** de la metodología ID-02 a los activos reales del banco. Mientras ID-02 dice "cómo medir", este documento entrega el **registro de riesgos**: cada riesgo identificado, con su amenaza, vulnerabilidad, probabilidad, impacto, nivel de riesgo calculado y el tratamiento propuesto. Es el resultado del trabajo de campo.
Es el documento que más le interesa a los supervisores: demuestra que el Banco **conoce sus principales riesgos de ciberseguridad y tiene un orden de prioridad** para atacarlos. El BCU lo evalúa como parte del riesgo operacional (Circ. 2227), Agesic lo cruza con el perfil de ciberseguridad (ID-05) y la URCDP lo usa como evidencia de que las medidas de protección de datos personales son "adecuadas al riesgo" (art. 10).
El registro de riesgos es un **documento vivo**: se actualiza cada vez que cambia la exposición (nueva amenaza, nuevo sistema, incidente, cambio normativo) y siempre en la re-evaluación anual. Un riesgo que no se revisa deja de ser gestión y pasa a ser burocracia.
## 2. Marco de referencia
| **Marco** | **Referencia** | **Qué exige aplicable al Banco** |
|---|---|---|
| **MCU 5.0 (Agesic)** | ID.RA-01 a ID.RA-06 | Identificar amenazas y vulnerabilidades, evaluar el impacto y priorizar los riesgos de los activos críticos |
| **ISO/IEC 27001** | Cláusula 6.1.2, 8.2 | Evaluación de riesgos que considere amenazas, vulnerabilidades y consecuencias, y produzca criterios y niveles de riesgo |
| **BCU** | Circular 2227 | Identificación y medición continua del riesgo operacional de los procesos y sistemas |
| **URCDP** | Ley 18.331 art. 10 | Riesgos sobre datos personales evaluados para dimensionar las medidas de seguridad |

## 3. Cómo completar esta plantilla (guía de llenado)
1. **Tomá la metodología aprobada (ID-02)** y el inventario (ID-01): los riesgos se evalúan sobre activos reales.
2. **Seleccioná los activos a evaluar en esta iteración:** priorizá los críticos (core, sistema de pagos, Banco En Línea, base de clientes, expedientes, datacenter, red de sucursales). No hace falta evaluar todo el inventario en la primera pasada.
3. **Para cada activo, identificá la amenaza** (¿qué puede pasar? — ransomware, filtración, falla, fraude) y la **vulnerabilidad** (¿qué lo habilita? — falta de parches, accesos débiles, tercero sin cláusulas, etc.).
4. **Calificá probabilidad (1-5) e impacto (1-5)** con la escala de ID-02 y calculá el nivel de riesgo con la matriz 5×5.
5. **Proponé el tratamiento** por riesgo (mitigar / transferir / evitar / aceptar — detalle en ID-04), el responsable y el plazo. No escribas "mitigar" sin decir con qué control.
6. **Validá con el propietario del activo** cada riesgo y su tratamiento; los niveles altos y críticos se revisan en el Comité de Seguridad.
7. **Consultá en el Banco:** División TI (Bernardo Ureta, Daniel Herrera) por amenazas y vulnerabilidades técnicas; Área Riesgos (Melissa Moraes) por la calibración; los propietarios de cada proceso; y el DPD por los riesgos sobre datos personales.
8. **Registrá todo en la tabla del punto 4** y subilo al repositorio SGSI. Cada riesgo recibe un ID único.
## 4. Plantilla del documento

### ENCABEZADO
| **Campo** | **Valor** |
|---|---|
| **Código** | ID-03 |
| **Título** | Análisis de Riesgos del caso Banco |
| **Versión** | 1.0 |
| **Estado** | [Borrador / En revisión / Aprobado] |
| **Fecha de aprobación** | [COMPLETAR] |
| **Elaborado por** | RSI |
| **Revisado por** | Área de Riesgos · Comité de Seguridad de la Información |
| **Aprobado por** | Comité de Seguridad de la Información |
| **Clasificación** | Confidencial |
| **Próxima revisión** | [Fecha, máx. 1 año o ante cambios] |

### 1. Objetivo
Identificar, analizar y priorizar los riesgos de seguridad de la información del Banco sobre sus activos críticos, aplicando la metodología ID-02, para fundamentar el plan de tratamiento (ID-04).
### 2. Alcance y criterios
Alcance: activos críticos del inventario ID-01 dentro del alcance del SGSI. Criterios de evaluación: escalas y matriz de ID-02. Umbral de atención: riesgos de nivel **Alto (≥ 8)** o **Crítico (≥ 15)**.
### 3. Metodología aplicada
[COMPLETAR: resumir aquí brevemente el método usado según ID-02: enfoque cualitativo, escalas 1-5, matriz 5×5, fuentes de información (entrevistas, resultados de pentest DE-03, análisis de vulnerabilidades PR-06, informe de la auditoría interna BCU-05, incidentes previos).]
### 4. Registro de riesgos
| **ID** | **Activo (ID-01)** | **Amenaza** | **Vulnerabilidad** | **Prob.** | **Imp.** | **Nivel** | **Tratamiento** | **Responsable** | **Plazo** |
|---|---|---|---|---|---|---|---|---|---|
| R-001 | [COMPLETAR] | [COMPLETAR] | [COMPLETAR] | 1-5 | 1-5 | [Bajo/Medio/Alto/Crítico] | [Mitigar/Transferir/Evitar/Aceptar] | [COMPLETAR] | [COMPLETAR] |
| R-002 | [COMPLETAR] | [COMPLETAR] | [COMPLETAR] | 1-5 | 1-5 | [COMPLETAR] | [COMPLETAR] | [COMPLETAR] | [COMPLETAR] |

### 5. Resumen de nivel de riesgo
[COMPLETAR: total de riesgos por nivel (crítico / alto / medio / bajo), distribución por activo y comentario del RSI sobre la tendencia vs. la evaluación anterior.]
### 6. Riesgos aceptados
| **ID** | **Riesgo** | **Nivel** | **Propietario que acepta** | **Fecha de revisión** |
|---|---|---|---|---|
| [COMPLETAR] | [COMPLETAR] | [Bajo/Medio] | [COMPLETAR] | [COMPLETAR] |

### 7. Control de cambios
| **Versión** | **Fecha** | **Cambio** | **Elaboró** | **Aprobó** |
|---|---|---|---|---|
| 0.1 | [COMPLETAR] | Versión inicial | RSI | — |
| 1.0 | [COMPLETAR] | Aprobación del registro de riesgos | RSI | Comité |

## 5. Ejemplo aplicado al Banco (modelo de referencia)
Ejemplo ilustrativo con seis riesgos realistas del Banco. Calificaciones de referencia; cada institución debe calificar según su realidad.
| **ID** | **Activo** | **Amenaza** | **Vulnerabilidad** | **Prob.** | **Imp.** | **Nivel** | **Tratamiento** | **Responsable** | **Plazo** |
|---|---|---|---|---|---|---|---|---|---|
| R-001 | Core bancario | Ransomware que cifra la base de datos central | Parches desactualizados del sistema operativo; respaldos no probados | 3 | 5 | 15 · **Crítico** | Mitigar: parcheo prioritario (PR-06), respaldo probado (PR-05), segmentación y EDR | Jefe Depto. Producción (D. Herrera) | [COMPLETAR: 90 días] |
| R-002 | Base de clientes y expedientes de crédito | Filtración de datos personales | Accesos con privilegios excesivos; falta de cifrado en reposo | 3 | 5 | 15 · **Crítico** | Mitigar: minimización de privilegios (PR-01), cifrado (PR-03), monitoreo (DE-01) | Div. TI | [COMPLETAR: 120 días] |
| R-003 | Sistema de pagos (Banco Pagos) | Falla o caída que detiene pagos a proveedores y obligaciones | Sin prueba de conmutación del sitio alterno; dependencia de un solo proveedor | 3 | 5 | 15 · **Crítico** | Mitigar: prueba de DRP semestral (RC-02), redundancia de enlace, plan de contingencia (BCU-06) | Jefe Depto. Sistema de Pagos (G. Correa) | [COMPLETAR: 60 días] |
| R-004 | Operaciones / personal con acceso | Fraude interno (desvío de fondos o datos) | Segregación de funciones débil; licencias no controladas; sin monitoreo de accesos | 2 | 4 | 8 · **Alto** | Mitigar: segregación de funciones (A.5.3), revisión de accesos (PR-01), registro de eventos (DE-01) | Área de Riesgos | [COMPLETAR: 120 días] |
| R-005 | Servicios de terceros (cloud / mantenimiento) | Fuga de información por proveedor | Contrato sin cláusulas de seguridad; sin control del subcontratista | 3 | 4 | 12 · **Alto** | Transferir: contrato con cláusulas (PR-08, GV-05), seguro; mitigar: auditoría del proveedor | Depto. Compras y Contrataciones | [COMPLETAR: 90 días] |
| R-006 | Banco En Línea | Indisponibilidad del canal digital (DDoS o falla) | Única vía de acceso; sin protección anti-DDoS | 3 | 4 | 12 · **Alto** | Mitigar: protección anti-DDoS, alta disponibilidad, plan de comunicación (RC-03) | Div. TI | [COMPLETAR: 60 días] |

**Comentario del ejemplo:** los tres riesgos críticos (R-001, R-002, R-003) coinciden con los activos que soportan el ahorro, el crédito y los pagos, y con los datos personales de los clientes. Todos tienen responsable y plazo, y pasan al plan de tratamiento ID-04 con su presupuesto y seguimiento.

**Documentos relacionados:** ID-01 (Activos) · ID-02 (Metodología) · ID-04 (Plan de tratamiento) · BCU-02 (Marco de riesgos) · PR-06 (Vulnerabilidades) · URCDP-05 (EIPD) · GV-06 (Informe del RSI).
