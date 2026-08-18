# Plan de Implementación del SGSI del Banco (2026-2028)

> **Código:** PLAN-SGSI-001 · **Versión:** 1.0 (borrador para aprobación)
> **Elaborado por:** RSI (responsable de este kit) · **Aprobado por:** Comité de Seguridad / Directorio
> **Horizonte:** 18 meses (ej. ago-2026 a ene-2028) · **Actualización:** trimestral

---

## 1. Objetivo del plan

Implementar de forma progresiva el **SGSI del Banco** de modo que la institución pueda demostrar, ante **Agesic (MCU 5.0)**, el **BCU (estándares mínimos de gestión)** y la **URCDP (protección de datos)**, que gestiona la seguridad de la información de forma **sistemática, documentada y auditable**.

## 2. Principios de ejecución

1. **Empezar por Gobernar e Identificar** (política, alcance, activos, riesgos): es lo que exige la norma y lo que desbloquea todo lo demás.
2. **Documentar a la vez que se hace**: cada actividad deja su evidencia (el entregable correspondiente).
3. **Riesgo primero**: no se "certifican papeles", se gestionan riesgos reales.
4. **Lo mínimo viable pero completo**: cada documento nace completo y útil, no perfecto.
5. **Revisión continua**: indicadores, auditoría interna y revisión por la dirección cada año.

## 3. Fases, actividades y entregables

### Fase 0 · Preparación y gobierno (Mes 0-1)
| # | Actividad | Responsable | Entregable |
|---|---|---|---|
| 0.1 | Presentar el proyecto a la dirección y lograr el respaldo formal | RSI / Gerencia General | Resolución de inicio |
| 0.2 | Constituir el **Comité de Seguridad de la Información** | Directorio / Gerencia | Acta de constitución + roles (GV-03) |
| 0.3 | **Designar al RSI** (resolución) y al **DPD** (comunicar a URCDP) | Directorio | Resolución (GV-03, URCDP-06) |
| 0.4 | Aprobar la **Política de Seguridad de la Información** | Directorio | GV-01 aprobada |
| 0.5 | Definir el alcance preliminar del SGSI | RSI + Comité | GV-02 (borrador) |

### Fase 1 · Diagnóstico y contexto (Mes 1-2)
| # | Actividad | Responsable | Entregable |
|---|---|---|---|
| 1.1 | Análisis de contexto (interno/externo) y partes interesadas | RSI | Documento de contexto (sección de GV-02) |
| 1.2 | Diagnóstico de cumplimiento del **MCU 5.0** con la lista de verificación de Agesic | RSI + consultores | Perfil actual (ID-05) |
| 1.3 | Diagnóstico de cumplimiento **BCU** y **URCDP** | RSI + DPD | Gaps (alimentan BCU-01, URCDP-01) |
| 1.4 | Inventario inicial de procesos y áreas (organigrama) | RSI | Mapa de procesos (parte de ID-01) |

### Fase 2 · Marco documental (Mes 2-4)
| # | Actividad | Responsable | Entregable |
|---|---|---|---|
| 2.1 | Modelo documental y control de versiones | RSI | GV-GOB-03 (gestión documental) + estructura de carpetas |
| 2.2 | Política de **protección de datos personales** | DPD | URCDP-01 |
| 2.3 | Normas complementarias: clasificación de información, uso aceptable | RSI | ID-ASS-02, PR-01 |
| 2.4 | Política de **control de accesos** y de **seguridad física** | RSI + TI | PR-01, PR-04 |
| 2.5 | Programa de **capacitación y concientización** | RSI + Capital Humano | PR-02 |

### Fase 3 · Identificar: activos y riesgos (Mes 3-5)
| # | Actividad | Responsable | Entregable |
|---|---|---|---|
| 3.1 | **Inventario de activos** por proceso (hardware, software, datos, servicios, personas) | RSI + responsables de proceso | ID-01 |
| 3.2 | **Clasificación** de la información (confidencialidad/integridad/disponibilidad) | RSI | ID-01 (columnas) + ID-ASS-02 |
| 3.3 | Adoptar la **metodología de riesgos** (cualitativa, MCU/ISO 27005) | RSI | ID-02 |
| 3.4 | Talleres de **evaluación de riesgos** por área | RSI + áreas | ID-03 (registro de riesgos) |
| 3.5 | Definir **perfil objetivo** de ciberseguridad | Comité | ID-05 (objetivo) |
| 3.6 | Mapa de **terceros** y evaluación de proveedores críticos | RSI + Compras | GV-05, PR-08 |

### Fase 4 · Tratar riesgos y desplegar controles de protección (Mes 5-9)
| # | Actividad | Responsable | Entregable |
|---|---|---|---|
| 4.1 | **Plan de tratamiento de riesgos** (mitigar/transferir/evitar/aceptar) | RSI + Comité | ID-04 |
| 4.2 | **Declaración de Aplicabilidad (SoA)** | RSI | GV-RIS-03 |
| 4.3 | Controles técnicos: accesos, endpoint, parches, vulnerabilidades, respaldos, red, cifrado | Div. TI | PR-01, PR-05, PR-06, PR-TEC |
| 4.4 | **Desarrollo seguro** (SDLC) para sistemas propios | Div. TI (Sistemas) | PR-07 |
| 4.5 | **Seguridad física**: datacenter, sucursales, videovigilancia | Servicios Generales | PR-04 |
| 4.6 | **Resguardo de datos** conforme RNRCSF art. 492 + claves + pruebas | Div. TI (Producción) | PR-05, RC-02 |

### Fase 5 · Detectar y monitorear (Mes 7-12)
| # | Actividad | Responsable | Entregable |
|---|---|---|---|
| 5.1 | Centralización de **logs** y monitoreo de eventos | Div. TI | DE-01 |
| 5.2 | Detección de anomalías e intrusión (SIEM/EDR) | Div. TI | DE-02 |
| 5.3 | Programa de **gestión de vulnerabilidades** y escaneos | Div. TI | PR-06, DE-02 |
| 5.4 | **Pruebas de seguridad** (pentest) anuales | RSI + externos | DE-03 |

### Fase 6 · Responder y notificar (Mes 8-10)
| # | Actividad | Responsable | Entregable |
|---|---|---|---|
| 6.1 | **Plan de respuesta a incidentes** y equipo CSIRT interno | RSI + TI | RS-01 |
| 6.2 | **Procedimiento de notificación** (URCDP 72h/24h, BCU, CERTuy) | RSI + DPD | RS-02, URCDP-02 |
| 6.3 | **Forense y preservación de evidencia** | RSI + Auditoría | RS-03 |
| 6.4 | Simulacros de incidentes (phishing, ransomware, filtración) | RSI | Evidencias de simulacro |

### Fase 7 · Continuidad y recuperación (Mes 9-12)
| # | Actividad | Responsable | Entregable |
|---|---|---|---|
| 7.1 | Análisis de impacto al negocio (**BIA**) y definición de **RTO/RPO** | RSI + Riesgos No Financieros | RC-01 (BIA) |
| 7.2 | **Plan de Continuidad de Negocio (BCP)** | Riesgos No Financieros + áreas | RC-01 |
| 7.3 | **Plan de Recuperación ante Desastres (DRP)** y resguardo de datos | Div. TI (Producción) | RC-02 |
| 7.4 | **Plan de comunicación de crisis** | Comunicación institucional | RC-03 |
| 7.5 | **Pruebas**: recuperación de resguardos (art. 492), BCP, DRP | RSI + áreas | Informes de prueba |

### Fase 8 · Cumplimiento URCDP (transversal, Mes 2-8)
| # | Actividad | Responsable | Entregable |
|---|---|---|---|
| 8.1 | Relevar **bases de datos** y **registro de tratamientos (ROPA)** | DPD | URCDP-04 |
| 8.2 | **Inscribir bases de datos** ante la URCDP (declarando medidas de seguridad) | DPD | Confirmaciones de inscripción |
| 8.3 | Procedimientos **ARCO** y atención de solicitudes | DPD | URCDP-03 |
| 8.4 | **EIPD** para tratamientos de alto riesgo | DPD | URCDP-05 |
| 8.5 | Política de **privacidad web** y consentimientos | DPD + TI | URCDP-01 (anexo) |

### Fase 9 · Cumplimiento BCU (transversal, Mes 4-10)
| # | Actividad | Responsable | Entregable |
|---|---|---|---|
| 9.1 | **Gobierno de ciberseguridad** y riesgo tecnológico | Directorio + RSI | BCU-01 |
| 9.2 | **Marco de gestión de riesgos** y apetito | Área Riesgos | BCU-02 |
| 9.3 | **Función de seguridad de la información** (RSI) formalizada | Área Riesgos | BCU-03 |
| 9.4 | **Función de gestión de TI** (operaciones, cambios, vulnerabilidades) | Div. TI | BCU-04 |
| 9.5 | **Auditoría interna** de seguridad | Auditoría Interna | BCU-05 |
| 9.6 | **Continuidad** y pruebas (plan de contingencia) | RSI + Riesgos | BCU-06 |

### Fase 10 · Verificar y mejorar (Mes 12-14)
| # | Actividad | Responsable | Entregable |
|---|---|---|---|
| 10.1 | **Auditoría interna del SGSI** (primera vuelta) | Auditoría Interna | BCU-05 (informe) |
| 10.2 | **Revisión por la dirección** | Directorio + Comité | GV-06 (informe del RSI) |
| 10.3 | Medición de **indicadores** y metas | RSI | P-MET-01 |
| 10.4 | Cierre de no conformidades | RSI + áreas | Plan de acciones correctivas |

### Fase 11 · Segundo ciclo de mejora (Mes 14-18)
| # | Actividad | Responsable | Entregable |
|---|---|---|---|
| 11.1 | Re-evaluación de riesgos (actualización) | RSI | ID-03 (v2) |
| 11.2 | Re-diagnóstico MCU 5.0 (avance de madurez) | RSI | ID-05 (v2) |
| 11.3 | Decisión sobre **certificación ISO 27001** | Directorio | Resolución |
| 11.4 | Plan anual siguiente | RSI | GV-04 (año 2) |

## 4. Cronograma resumido (18 meses)

```
Fase                M0 M1 M2 M3 M4 M5 M6 M7 M8 M9 M10 M11 M12 M13 M14 M15 M16 M17 M18
F0 Gobierno         ██
F1 Diagnóstico         ██ ██
F2 Marco doc              ██ ██
F3 Activos/Riesgos           ██ ██ ██
F4 Tratar/Proteger                 ██ ██ ██ ██
F5 Detectar                               ██ ██ ██ ██ ██
F6 Responder                                      ██ ██ ██
F7 Continuidad                                        ██ ██ ██ ██
F8 URCDP              ██ ██ ██ ██ ██ ██ ██
F9 BCU                      ██ ██ ██ ██ ██ ██
F10 Verificar                                                     ██ ██
F11 Mejora                                                               ██ ██ ██ ██
```

## 5. Recursos necesarios

| Recurso | Detalle |
|---|---|
| **Personas** | RSI (dedicado), DPD (dedicado o compartido), 1-2 oficiales de seguridad, apoyo de Div. TI (2 personas), Capital Humano, Compras, Auditoría |
| **Presupuesto** | Herramientas (SIEM/EDR/escaneo, backup), pentest, capacitación, consultoría de acompañamiento (opcional) |
| **Herramientas sugeridas** | Ver `03-HERRAMIENTAS/00_Inventario_de_Herramientas.md` |

## 6. Indicadores clave (KPI) del proyecto

| KPI | Meta a 12 meses | Meta a 18 meses |
|---|---|---|
| % de entregables del kit completados y aprobados | ≥ 60% | ≥ 90% |
| % de activos inventariados y clasificados | ≥ 80% | ≥ 95% |
| % de riesgos críticos con plan de tratamiento | 100% | 100% |
| Madurez MCU 5.0 (promedio) | +1 nivel | +2 niveles |
| Bases de datos inscritas en URCDP | 100% de las obligatorias | 100% + mantenimiento |
| Pruebas de resguardo de datos (art. 492) | 1 realizada | 2 realizadas |
| Simulacros de incidentes | 2 | 4 |
| % de funcionarios capacitados en seguridad | 50% | 90% |

## 7. Riesgos del proyecto

| Riesgo | Mitigación |
|---|---|
| Falta de respaldo de la dirección | Aprobación formal en Fase 0; informe mensual de avance |
| RSI sin dedicación | Resolución de dedicación; no asignar tareas operativas de TI |
| Falta de disponibilidad de áreas | Talleres acotados; sponsor por cada área |
| Presupuesto insuficiente | Priorizar controles de riesgo alto; herramientas open source |
| Cambios de personal | Documentar todo (este kit es la memoria); matriz de responsables |

## 8. Aprobación

| Rol | Nombre | Firma | Fecha |
|---|---|---|---|
| RSI | | | |
| Jefe de Riesgos No Financieros | | | |
| Gerente de Área Riesgos | | | |
| Gerente General / Directorio | | | |
