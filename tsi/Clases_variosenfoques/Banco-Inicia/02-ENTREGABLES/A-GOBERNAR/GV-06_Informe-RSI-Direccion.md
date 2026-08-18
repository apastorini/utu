# GV-06 · Informe del RSI a la Dirección (Revisión por la Dirección del SGSI)

> ⚠️ **Alerta:** este documento menciona **nombres propios del organigrama del Banco** (personas y cargos, abril 2026). Antes de usar el documento, verificá la vigencia de esos nombres contra el organigrama actual.
> **Función del MCU 5.0:** Gobernar (GV.OV — Supervisión del SGSI)
> **ISO/IEC 27001:** Cláusula 9.3 (Revisión por la dirección) · 9.1 (Seguimiento y medición) · 10.2 (No conformidad y acción correctiva)
> **BCU:** Estándares Mínimos de Gestión — Gobierno y supervisión de la ciberseguridad
> **URCDP:** Ley 19.670 art. 38 (deber de notificación) y Decreto 64/020 (supervisión de medidas)
> **Nivel del curso:** 🔴 Dominar

## 1. Qué es y por qué existe
El **Informe del RSI a la Dirección** es la pieza que **cierra el ciclo de gobierno del SGSI**: el RSI rinde cuentas ante el Comité de Seguridad y el Directorio sobre el desempeño del sistema y propone mejoras. La ISO/IEC 27001 lo exige en la **cláusula 9.3** (revisión por la dirección) y el MCU 5.0 en **GV.OV** (supervisión): sin esta revisión periódica y documentada, el SGSI deja de ser un sistema y pasa a ser un conjunto de documentos sin gobierno.
Se produce con **periodicidad semestral** para el Comité de Seguridad y **anual** para el Directorio (y ante incidentes graves o cambios mayores, en forma extraordinaria). El informe resume: resultados de auditorías, incidentes, desvíos, indicadores, estado de los riesgos, cumplimiento normativo, cambios relevantes y recomendaciones. Sobre esa base, la Dirección **decide** (prioriza recursos, aprueba el plan del próximo año) y el acta de la reunión de revisión queda como evidencia formal para BCU, Agesic y URCDP.
Para el Banco es además el vehículo natural para informar al Directorio sobre el riesgo tecnológico y los secretos bancarios de los clientes: la alta dirección necesita saber, en términos ejecutivos y con datos, cómo está la seguridad de los créditos hipotecarios, el ahorro, Banco En Línea y el sistema de pagos.

## 2. Marco de referencia
| **Requisito** | **MCU 5.0** | **ISO/IEC 27001** | **BCU** | **URCDP** |
|---|---|---|---|---|
| Revisión por la dirección | GV.OV | **Cláusula 9.3** | EMG · Gobierno (reporte al Directorio) | — |
| Seguimiento y medición | GV.OV | Cláusula 9.1 | EMG · Gobierno | D.64/020 (verificación de medidas) |
| No conformidades y acciones correctivas | GV.OV, ID.IM | Cláusulas 10.1-10.2 | Circ. 2227 (desvíos operativos) | D.64/020 (subsanación de desvíos) |
| Notificación de vulneraciones | RS.CO | A.5.24 | Circ. 2227 | **Ley 19.670 art. 38** |
| Mejora continua | ID.IM | Cláusula 10.3 | EMG · Gobierno | D.64/020 (revisión de medidas) |

## 3. Cómo completar esta plantilla (guía de llenado)
1. **Consolidá los insumos** del período: resultados de auditorías (internas y externas), registro de incidentes (RS-01/02), indicadores del plan anual (GV-04), estado de riesgos (ID-03/04), hallazgos de cumplimiento y cambios en el SGSI.
2. **Cuantificá** todo lo que se pueda: número de incidentes, tiempos de respuesta, % de riesgos tratados, % de avance del plan, hallazgos abiertos. Los números reemplazan a las opiniones.
3. **Redactá en lenguaje ejecutivo**: el Directorio necesita conclusiones y decisiones, no detalles técnicos. Los anexos pueden llevar el detalle.
4. **Incluí la sección de recomendaciones** con prioridad y recursos estimados: es la base del plan del año siguiente.
5. **Presentalo al Comité de Seguridad** (semestral) y luego al Directorio (anual). Llená el **acta de la reunión de revisión** con las decisiones y responsables.
6. **Dá seguimiento** a las acciones decididas en la siguiente revisión y registralas en el control de cambios. Conservá el informe y el acta como evidencia de auditoría.

## 4. Plantilla del documento

### ENCABEZADO
| **Campo** | **Valor** |
|---|---|
| **Código** | GV-06 |
| **Título** | Informe del RSI a la Dirección (Revisión por la Dirección) |
| **Versión** | [X.X] |
| **Período que cubre** | [Semestre/Año] |
| **Fecha de emisión** | [COMPLETAR] |
| **Elaborado por** | RSI |
| **Revisado por** | Comité de Seguridad de la Información |
| **Presentado a** | Comité de Seguridad · Directorio |
| **Clasificación** | Confidencial / Uso interno |
| **Próximo informe** | [Fecha] |

### 1. Resumen ejecutivo
[COMPLETAR: 3-5 líneas con la conclusión general del período: ¿el SGSI está funcionando? ¿cuáles son los temas que requieren decisión del Directorio?]
### 2. Resultados de las auditorías
| **Auditoría** | **Período** | **Hallazgos** | **Estado** | **Acciones** |
|---|---|---|---|---|
| [Interna / externa / BCU / Agesic / URCDP] | [COMPLETAR] | [COMPLETAR] | [Abiertos / Cerrados] | [COMPLETAR] |

### 3. Incidentes de seguridad
| **Incidente** | **Fecha** | **Severidad** | **Impacto** | **Tiempo de respuesta (MTTR)** | **Lección aprendida** |
|---|---|---|---|---|---|
| [COMPLETAR] | [COMPLETAR] | [Alta/Media/Baja] | [COMPLETAR] | [COMPLETAR] | [COMPLETAR] |

Incluye las notificaciones realizadas a BCU, URCDP y CERTuy en el período (RS-02).
### 4. Desvíos y no conformidades
| **No conformidad / desvío** | **Cláusula/control afectado** | **Causa raíz** | **Plan de acción** | **Fecha límite** |
|---|---|---|---|---|
| [COMPLETAR] | [COMPLETAR] | [COMPLETAR] | [COMPLETAR] | [COMPLETAR] |

### 5. Indicadores del SGSI (KPIs)
> **Definición de cada KPI (fórmula, fuente, meta, responsable):** EV-05. **Evidencia de respaldo:** EV-03.
| **Indicador** | **Meta** | **Resultado del período** | **Tendencia** |
|---|---|---|---|
| % de avance del Plan Anual (GV-04) | [COMPLETAR] | [COMPLETAR] | [COMPLETAR] |
| % de riesgos altos tratados | [COMPLETAR] | [COMPLETAR] | [COMPLETAR] |
| MTTR de incidentes | [COMPLETAR] | [COMPLETAR] | [COMPLETAR] |
| % de funcionarios capacitados | [COMPLETAR] | [COMPLETAR] | [COMPLETAR] |
| [COMPLETAR] | [COMPLETAR] | [COMPLETAR] | [COMPLETAR] |

### 6. Estado de los riesgos de seguridad de la información
[COMPLETAR: evolución del mapa de riesgos, riesgos residuales aceptados, apetito de riesgo y eventos de riesgo del período, con referencia a ID-02/03 e ID-04.]
### 7. Cumplimiento normativo
| **Norma** | **Estado** | **Observaciones** |
|---|---|---|
| MCU 5.0 (Agesic) | [COMPLETAR] | [COMPLETAR] |
| ISO/IEC 27001 (cláusulas 4-10) | [COMPLETAR] | [COMPLETAR] |
| RNRCSF art. 492 y Circulares BCU | [COMPLETAR] | [COMPLETAR] |
| Ley 18.331 / 19.670 y Decreto 64/020 | [COMPLETAR] | [COMPLETAR] |

### 8. Cambios significativos
[COMPLETAR: cambios en el organigrama, nuevas tecnologías o servicios, altas/bajas de terceros críticos, cambios de normativa, cambios en el alcance (GV-02).]
### 9. Conclusiones y recomendaciones
| **Prioridad** | **Recomendación** | **Recursos estimados** | **Plazo** |
|---|---|---|---|
| Alta | [COMPLETAR] | [COMPLETAR] | [COMPLETAR] |
| Media | [COMPLETAR] | [COMPLETAR] | [COMPLETAR] |
| Baja | [COMPLETAR] | [COMPLETAR] | [COMPLETAR] |

### 10. Acta de la reunión de revisión por la dirección
| **Dato** | **Contenido** |
|---|---|
| Fecha y hora | [COMPLETAR] |
| Lugar / modalidad | [COMPLETAR] |
| Participantes | [COMPLETAR: Directorio, Gerente General, Comité, RSI, DPD, Auditoría] |
| Decisiones adoptadas | [COMPLETAR: aprobaciones, prioridades, recursos asignados] |
| Acciones acordadas | [COMPLETAR: acción / responsable / fecha] |
| Próxima revisión | [COMPLETAR] |

### 11. Control de cambios
| **Versión** | **Fecha** | **Cambio** | **Elaboró** | **Aprobó** |
|---|---|---|---|---|
| 0.1 | [COMPLETAR] | Borrador del informe del período | RSI | — |
| 1.0 | [COMPLETAR] | Versión final presentada al Directorio | RSI | Comité / Directorio |

## 5. Ejemplo aplicado al Banco (modelo de referencia)
Ejemplo ilustrativo. Adaptalo a los datos reales del período.
**Resumen ejecutivo (ejemplo):** durante el semestre el SGSI se consolidó como marco de gobierno de la seguridad del Banco. Se cerraron [COMPLETAR] de los [COMPLETAR] hallazgos de la auditoría interna de seguridad, no se registraron incidentes que comprometieran el secreto bancario y se avanzó al [COMPLETAR] % del Plan Anual. Los temas que requieren decisión del Directorio son la inversión en MFA para accesos remotos y la autorización de la tercerización en el exterior de parte de la infraestructura de Banco En Línea.
**Auditorías (ejemplo):** la División Auditoría Interna (Cr. Marcelo Jorge) ejecutó la auditoría de control de accesos al core bancario, con [COMPLETAR] hallazgos (uno de criticidad media en la revisión de usuarios con privilegios de la División TI, ya con plan de remediación). La URCDP verificó el cumplimiento del Documento de Seguridad y los contratos con encargados de tratamiento.
**Incidentes (ejemplo):** se gestionaron [COMPLETAR] incidentes en el período: dos campañas de phishing dirigidas a funcionarios de sucursales (bloqueadas por el filtro y reportadas), un incidente de disponibilidad de Banco En Línea de [COMPLETAR] minutos (MTTR dentro de meta) y un acceso no autorizado menor a un sistema interno, contenido sin impacto en datos de clientes. No se requirió notificación a BCU ni a URCDP.
**Indicadores (ejemplo):** avance del Plan Anual [COMPLETAR] % (meta [COMPLETAR] %); riesgos altos con plan de tratamiento [COMPLETAR] %; funcionarios capacitados en ciberseguridad [COMPLETAR] % (incluidas las sucursales); pruebas de restauración de respaldos del sistema de pagos y del core hipotecario [COMPLETAR] %.
**Recomendaciones (ejemplo):** (1) Alta: aprobar el presupuesto para implementar MFA en los accesos administrativos al core y a los sistemas de pagos; (2) Alta: autorizar el proceso ante el BCU para la tercerización en el exterior de la infraestructura de Banco En Línea, con la EIPD que conducirá el DPD; (3) Media: reforzar el programa de concientización en las sucursales con mayor exposición a intentos de fraude.
**Acta (ejemplo):** en la reunión del [COMPLETAR], el Directorio aprobó el informe, priorizó las recomendaciones de criticidad alta, asignó recursos del presupuesto de la División TI (Lic. Bernardo Ureta) y fijó la próxima revisión para [COMPLETAR].

**Documentos relacionados:** GV-01 (Política), GV-02 (Alcance), GV-03 (Roles y Comité), GV-04 (Plan Anual), ID-03 (Riesgos), RS-01/02 (Incidentes), BCU-05 (Auditoría de Seguridad), EV-05 (Indicadores y Métricas), MATRIZ-001 (Correspondencia Normativa).
