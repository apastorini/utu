# ID-04 · Plan de Tratamiento de Riesgos del Banco

> ⚠️ **Alerta:** este documento menciona **nombres propios del organigrama del Banco** (personas y cargos, abril 2026). Antes de usar el documento, verificá la vigencia de esos nombres contra el organigrama actual.
> **Función del MCU 5.0:** Gobernar (GV.RM — Estrategia de gestión de riesgos) · Identificar (ID.RA — Evaluación de riesgos)
> **ISO/IEC 27001:** Cláusula 6.1.3 (Tratamiento de riesgos) · Cláusula 6.2 (Objetivos de seguridad) · A.6.8 (Seguridad en el desarrollo de políticas) · SoA (Anexo A)
> **BCU:** Circular 2227 (control del riesgo operacional) · EMG · Marco de Riesgos
> **URCDP:** Ley 18.331 art. 10 · Decreto 64/020 (medidas correctivas y preventivas)
> **Nivel del curso:** 🟡 Practicar · 🔴 Aplicar

## 1. Qué es y por qué existe
El **Plan de Tratamiento de Riesgos** es el documento que transforma el análisis (ID-03) en **acciones concretas**: para cada riesgo decidido como "alto" o "crítico" define qué se va a hacer, quién lo hace, con qué presupuesto y para cuándo. Sin este plan, el análisis de riesgos es solo un diagnóstico; con él, el SGSI empieza a reducir exposición real.
La ISO 27001 (cláusula 6.1.3) exige producir un **plan de tratamiento de riesgos** y que la organización apruebe los riesgos residuales. El BCU, por la Circular 2227, espera que el riesgo operacional tenga planes de acción con responsables y plazos, y que se haga seguimiento. Y es el documento que permite al Directorio decidir cuánto invertir: cada acción del plan se traduce en presupuesto.
El plan cubre las **cuatro opciones de tratamiento** (mitigar, transferir, evitar y aceptar), ordena las acciones por prioridad (primero lo crítico), define responsables con sus plazos y presupuesto, y prevé el **seguimiento periódico**. Se cierra con la **Declaración de Aplicabilidad (SoA)**, la tabla que vincula cada control de la norma con su estado en el Banco: qué control se aplica, en qué riesgo se apoya y con qué justificación.
## 2. Marco de referencia
| **Marco** | **Referencia** | **Qué exige aplicable al Banco** |
|---|---|---|
| **MCU 5.0 (Agesic)** | GV.RM-01 a GV.RM-07 | Estrategia de riesgos alineada a los objetivos; acciones para mitigar riesgos, monitorear su efectividad y comunicar los cambios |
| **ISO/IEC 27001** | Cláusula 6.1.3, 6.2; Anexo A (A.6.8) | Plan de tratamiento con responsables y plazos; SoA con justificación de cada control |
| **BCU** | Circular 2227; EMG · Marco de Riesgos | Planes de acción sobre el riesgo operacional con seguimiento y evidencia |
| **URCDP** | Ley 18.331 art. 10 | Medidas técnicas y organizativas adecuadas al riesgo para proteger datos personales |

## 3. Cómo completar esta plantilla (guía de llenado)
1. **Partí del registro de riesgos (ID-03):** todo riesgo **Alto (≥ 8)** o **Crítico (≥ 15)** debe tener una acción de tratamiento. Los bajos pueden quedar como "aceptados" documentados.
2. **Elegí la opción de tratamiento** por riesgo (punto 3): mitigar con controles, transferir (seguro, contrato con cláusulas), evitar (eliminar la actividad) o aceptar (solo si está dentro del apetito).
3. **Priorizá** por nivel de riesgo y por criticidad del activo: primero lo que toca pagos, ahorro y datos personales. El plan debe tener un orden ejecutable, no una lista infinita.
4. **Asigná responsable y plazo** a cada acción, y estimá el presupuesto. Un plan sin responsable y sin fecha es papel, no gestión.
5. **Definí los indicadores de seguimiento** (punto 6): % de acciones cerradas a tiempo, riesgos críticos abiertos, tendencia del nivel de riesgo.
6. **Completá la SoA** (punto 7): recorré los controles del Anexo A (2022) y marcá para cada uno si se aplica ("Aplicado", "No aplicado", "En implementación") y su justificación, vinculándolo a los riesgos del ID-03.
7. **Consultá en el Banco:** el Comité de Seguridad decide prioridades y presupuesto; División TI (Bernardo Ureta) define los controles técnicos; Área Financiera (Soledad Carreres) y Compras (Rosario Larrosa) estiman costos y contrataciones; y los propietarios de activos firman la ejecución de cada acción.
8. **Seguí el plan** en las reuniones trimestrales del Comité y reportá el avance en el informe del RSI (GV-06).
## 4. Plantilla del documento

### ENCABEZADO
| **Campo** | **Valor** |
|---|---|
| **Código** | ID-04 |
| **Título** | Plan de Tratamiento de Riesgos del Banco |
| **Versión** | 1.0 |
| **Estado** | [Borrador / En revisión / Aprobado] |
| **Fecha de aprobación** | [COMPLETAR] |
| **Elaborado por** | RSI |
| **Revisado por** | Comité de Seguridad de la Información |
| **Aprobado por** | Comité de Seguridad · Gerencia General |
| **Clasificación** | Confidencial |
| **Próxima revisión** | [Fecha, máx. 1 año] |

### 1. Objetivo
Definir, priorizar y controlar las acciones para reducir los riesgos de seguridad de la información del Banco a un nivel aceptable, y declarar la aplicabilidad de los controles de la ISO/IEC 27001.
### 2. Alcance
Comprende todos los riesgos del registro ID-03 y los controles del Anexo A aplicables al alcance del SGSI (GV-02), incluidos los servicios de terceros y las bases con datos personales.
### 3. Opciones de tratamiento de riesgos
| **Opción** | **Qué significa** | **Ejemplo en el Banco** |
|---|---|---|
| **Mitigar** | Aplicar controles que reducen probabilidad y/o impacto | Parcheo, respaldo, control de accesos, monitoreo |
| **Transferir** | Trasladar parte del riesgo (seguro, contrato, tercero) | Pólizas cibernéticas; cláusulas en contratos de proveedores |
| **Evitar** | Eliminar la actividad o el activo que genera el riesgo | Retirar un sistema sin mantenimiento |
| **Aceptar** | Asumir el riesgo dentro del apetito, documentándolo | Riesgo bajo en un sistema interno sin datos sensibles |

### 4. Priorización y ejecución
Orden de ejecución: **1º riesgos críticos → 2º riesgos altos → 3º acciones de cumplimiento normativo**. Cada acción se registra en la tabla siguiente y se le asigna responsable, plazo y presupuesto.
### 5. Tabla de tratamiento de riesgos
| **ID (ID-03)** | **Riesgo** | **Nivel** | **Opción** | **Acción / Control** | **Responsable** | **Plazo** | **Presupuesto (UYU)** | **Estado** |
|---|---|---|---|---|---|---|---|---|
| R-001 | [COMPLETAR] | [COMPLETAR] | Mitigar | [COMPLETAR: qué control se implementa] | [COMPLETAR] | [COMPLETAR] | [COMPLETAR] | [Pendiente/En curso/Cerrado] |
| R-002 | [COMPLETAR] | [COMPLETAR] | Transferir | [COMPLETAR: póliza/contrato] | [COMPLETAR] | [COMPLETAR] | [COMPLETAR] | [COMPLETAR] |

### 6. Seguimiento e indicadores
- **Frecuencia de seguimiento:** [COMPLETAR: trimestral en el Comité de Seguridad].
- **Indicadores:** (a) % de acciones cerradas en plazo; (b) número de riesgos críticos abiertos; (c) % de riesgos altos/críticos con tratamiento aprobado; (d) variación del nivel de riesgo vs. la evaluación anterior.
- **Riesgos residuales:** todo riesgo que queda luego del tratamiento se documenta en la sección de riesgos aceptados de ID-03.
### 7. Declaración de Aplicabilidad (SoA) — resumen
La SoA completa se gestiona como anexo (GV-07) y recorre los **93 controles del Anexo A 2022**. Formato de la tabla:
| **Control** | **Estado** | **Aplicado / No aplicado** | **Justificación (vinculación con riesgo)** |
|---|---|---|---|
| A.5.9 Inventario de activos | [Aplicado/En implementación/No aplicado] | [COMPLETAR] | Cubre ID-01; mitiga riesgos sobre el core y la base de clientes |
| A.5.15 Control de acceso | [COMPLETAR] | [COMPLETAR] | Mitiga R-002 y R-004 (accesos, fraude interno) |
| A.6.3 Concientización | [COMPLETAR] | [COMPLETAR] | Reduce riesgo de phishing/ingeniería social |
| A.7.1 Perímetros físicos | [COMPLETAR] | [COMPLETAR] | Protege datacenter y sucursales |
| A.8.7 Protección contra malware | [COMPLETAR] | [COMPLETAR] | Mitiga R-001 (ransomware) |
| A.8.13 Copias de respaldo | [COMPLETAR] | [COMPLETAR] | Mitiga R-001/R-003; exigido por RNRCSF art. 492 |

### 8. Control de cambios
| **Versión** | **Fecha** | **Cambio** | **Elaboró** | **Aprobó** |
|---|---|---|---|---|
| 0.1 | [COMPLETAR] | Versión inicial | RSI | — |
| 1.0 | [COMPLETAR] | Aprobación del plan de tratamiento | RSI | Comité |

## 5. Ejemplo aplicado al Banco (modelo de referencia)
Ejemplo ilustrativo de cómo se tratan los riesgos del ejemplo de ID-03.
| **ID** | **Riesgo** | **Nivel** | **Opción** | **Acción** | **Responsable** | **Plazo** | **Presupuesto (UYU)** | **Estado** |
|---|---|---|---|---|---|---|---|---|
| R-001 | Ransomware en el core | Crítico | Mitigar | Parcheo priorizado del core y bases; implementación de EDR; prueba trimestral de restauración de respaldos | Jefe Depto. Producción (D. Herrera) | 90 días | [COMPLETAR: 8.000.000] | En curso |
| R-002 | Filtración de datos personales | Crítico | Mitigar | Revisión y minimización de privilegios en la base de clientes; cifrado en reposo de expedientes | Div. TI | 120 días | [COMPLETAR: 12.000.000] | Pendiente |
| R-003 | Falla del sistema de pagos | Crítico | Mitigar | Prueba semestral de conmutación a sitio alterno; redundancia de enlaces con proveedor | Jefe Depto. Sistema de Pagos (G. Correa) | 60 días | [COMPLETAR: 6.500.000] | En curso |
| R-004 | Fraude interno | Alto | Mitigar | Segregación de funciones en operaciones; revisión trimestral de accesos; monitoreo de sesiones privilegiadas | Área de Riesgos | 120 días | [COMPLETAR: 3.000.000] | Pendiente |
| R-005 | Fuga por tercero | Alto | Transferir | Nuevo contrato con cláusulas de seguridad y póliza cibernética; auditoría anual del proveedor de nube | Compras y Contrataciones | 90 días | [COMPLETAR: 4.500.000] | En curso |
| R-006 | Indisponibilidad de Banco En Línea | Alto | Mitigar | Contratación de protección anti-DDoS; arquitectura de alta disponibilidad | Div. TI | 60 días | [COMPLETAR: 5.000.000] | Pendiente |

**Seguimiento (ejemplo):** el Comité revisa el plan trimestralmente. Indicador objetivo del primer año: cerrar el 100 % de las acciones críticas y reducir el número de riesgos críticos de 3 a 0. El avance se reporta en GV-06.
**SoA (ejemplo):** por cada control del Anexo A se marca estado y justificación. Por ejemplo, A.8.13 (respaldo) = "Aplicado" y su justificación cita el RNRCSF art. 492 y el riesgo R-001; A.6.8 (desarrollo de políticas de seguridad) = "Aplicado" y cubre GV-01/PR-08.

**Documentos relacionados:** ID-03 (Análisis de riesgos) · ID-02 (Metodología) · GV-07 (SoA) · BCU-02 (Marco de riesgos) · PR-01…08 (controles de protección) · GV-06 (Informe del RSI).
