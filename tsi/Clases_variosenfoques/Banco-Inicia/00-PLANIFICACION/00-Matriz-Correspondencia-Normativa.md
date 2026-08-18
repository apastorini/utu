# Matriz de Correspondencia Normativa del SGSI del Banco

> **Código:** MATRIZ-001 · **Versión:** 1.0
> **Objetivo:** demostrar que cada entregable del SGSI **cubre simultáneamente** los requisitos del **MCU 5.0 (Agesic)**, los controles de **ISO/IEC 27001**, los estándares del **BCU** y las obligaciones de la **URCDP**. Es la herramienta para responder "¿qué documento cubre qué norma?" en auditorías.

---

## 1. Referencias de funciones/categorías MCU 5.0 usadas

| Función | Categorías principales |
|---|---|
| **GV · Gobernar** | GV.OC Contexto organizativo, GV.RM Estrategia de riesgos, GV.RR Roles y autoridades, GV.PO Política, GV.OV Supervisión, GV.SC Cadena de suministro |
| **ID · Identificar** | ID.AM Gestión de activos, ID.RA Evaluación de riesgos, ID.IM Mejora |
| **PR · Proteger** | PR.AA Identidades y control de acceso, PR.AT Concientización, PR.DS Seguridad de datos, PR.PS Seguridad de plataformas, PR.IR Resiliencia de la infraestructura |
| **DE · Detectar** | DE.CM Monitoreo continuo, DE.AE Análisis de eventos adversos |
| **RS · Responder** | RS.MA Gestión de incidentes, RS.AN Análisis de incidentes, RS.CO Notificación y comunicación, RS.MI Mitigación de incidentes |
| **RC · Recuperar** | RC.RP Ejecución del plan de recuperación, RC.CO Comunicación de la recuperación |

## 2. Referencias ISO/IEC 27001 usadas (Anexo A, edición 2022)

| Control | Tema |
|---|---|
| A.5.1 / A.5.9 / A.5.15 / A.5.19 / A.5.20 / A.5.21 / A.5.22 / A.5.23 / A.5.24 / A.5.25 / A.5.29 / A.5.30 | Políticas, inventario, accesos, incidentes, continuidad, proveedores, terceros |
| A.6.3 / A.6.6 / A.6.7 | Concientización, confidencialidad, teletrabajo |
| A.7.1 / A.7.2 / A.7.5 | Perímetros físicos, ingreso, amenazas |
| A.8.2 / A.8.5 / A.8.7 / A.8.8 / A.8.9 / A.8.10 / A.8.12 / A.8.13 / A.8.15 / A.8.16 | Privilegios, autenticación, malware, gestión de vulnerabilidades, configuración, borrado, prevención de fuga, respaldos, registro de eventos, monitoreo |

## 3. Matriz por entregable

### A · GOBERNAR
| Código | Documento | MCU 5.0 | ISO 27001 | BCU | URCDP |
|---|---|---|---|---|---|
| GV-01 | Política de Seguridad de la Información | GV.PO | A.5.1, 5.2 | EMG · Gobierno | Art. 10 (base) |
| GV-02 | Alcance del SGSI | GV.OC | Cláusula 4.3 | EMG · Gobierno | — |
| GV-03 | Roles, responsabilidades y Comité (RSI, DPD) | GV.RR, GV.OV | 5.2, 5.3, A.5.2 | EMG · Función Seguridad | Ley 19.670 (DPD) |
| GV-04 | Plan Anual de Seguridad de la Información | GV.OV, GV.RM | 6.2 | EMG · Gobierno | — |
| GV-05 | Riesgos de la cadena de suministro (terceros) | GV.SC | A.5.19-5.22 | Circ. 2419-2422, Com. 2022/254 | Decreto 64/020 |
| GV-06 | Informe del RSI a la Dirección | GV.OV | Cláusula 9.3 | EMG · Gobierno | — |

### B · IDENTIFICAR
| Código | Documento | MCU 5.0 | ISO 27001 | BCU | URCDP |
|---|---|---|---|---|---|
| ID-01 | Inventario de Activos de Información | ID.AM | A.5.9 | EMG · Riesgo Tecnológico | — |
| ID-02 | Metodología de Análisis y Evaluación de Riesgos | ID.RA, GV.RM | Cláusula 6.1 (ISO 27005) | Circ. 2227 (riesgo operativo) | Art. 10 / EIPD base |
| ID-03 | Análisis de Riesgos (caso Banco) | ID.RA | 6.1.2, 8.2 | Circ. 2227 | — |
| ID-04 | Plan de Tratamiento de Riesgos | GV.RM | 6.1.3, A.6.8 | Circ. 2227 | — |
| ID-05 | Perfil de Ciberseguridad del Banco | Perfiles / madurez | — | EMG · Marco de Riesgos | — |

### C · PROTEGER
| Código | Documento | MCU 5.0 | ISO 27001 | BCU | URCDP |
|---|---|---|---|---|---|
| PR-01 | Control de Acceso y Gestión de Identidades | PR.AA | A.5.15, A.8.2, A.8.5 | EMG · Riesgo Tecnológico | Art. 10 (accesos) |
| PR-02 | Concientización y Capacitación | PR.AT | A.6.3 | EMG · Gobierno | Art. 29 (capacitar) |
| PR-03 | Seguridad de Datos (clasificación, cifrado) | PR.DS | A.8.12, A.8.24 | Art. 492 (claves) | Art. 10 |
| PR-04 | Seguridad Física y del Entorno | PR.AA-06, PR.PS | A.7.x | RNRCSF / RENAEMSE | Art. 10 (medidas físicas) |
| PR-05 | Respaldo y Recuperación de la Información | PR.IR | A.8.13 | **Art. 492 RNRCSF** | Art. 10 |
| PR-06 | Gestión de Vulnerabilidades y Parches | PR.PS | A.8.8, A.8.9 | EMG · Riesgo Tecnológico | — |
| PR-07 | Desarrollo Seguro (SDLC) | PR.PS | A.8.25-8.28 | EMG · Gestión TI | Privacidad por diseño (D.64/020) |
| PR-08 | Acuerdos de Confidencialidad y Terceros | GV.SC, PR.PS | A.6.6, A.5.20 | Circ. 2419-2422 | Decreto 64/020 (cláusulas) |

### D · DETECTAR
| Código | Documento | MCU 5.0 | ISO 27001 | BCU | URCDP |
|---|---|---|---|---|---|
| DE-01 | Monitoreo y Registro de Eventos | DE.CM | A.8.15, A.8.16 | Circ. 2280 (sist. de pagos) | — |
| DE-02 | Detección de Anomalías e Intrusiones | DE.AE, DE.CM | A.8.16 | Circ. 2280 | — |
| DE-03 | Pruebas de Seguridad (pentest) | DE.CM, PR.PS | A.8.8 | EMG · Auditoría | — |

### E · RESPONDER
| Código | Documento | MCU 5.0 | ISO 27001 | BCU | URCDP |
|---|---|---|---|---|---|
| RS-01 | Plan de Respuesta a Incidentes | RS.MA, RS.MI | A.5.24, A.5.25 (ISO 27035) | Circ. 2227 | Art. 10 |
| RS-02 | Notificación y Comunicación de Incidentes | RS.CO | A.5.24 | Circ. 2227 | **Art. 38 Ley 19.670 / D.64/020** |
| RS-03 | Forense y Preservación de Evidencia | RS.AN | A.5.28 | Circ. 2227 | — |

### F · RECUPERAR
| Código | Documento | MCU 5.0 | ISO 27001 | BCU | URCDP |
|---|---|---|---|---|---|
| RC-01 | Plan de Continuidad del Negocio (BCP) | RC.RP | A.5.29, A.5.30 | **EMG · Continuidad** | — |
| RC-02 | Plan de Recuperación ante Desastres (DRP) | RC.RP | A.8.13 | **Art. 492 + EMG** | — |
| RC-03 | Plan de Comunicación de Crisis | RC.CO | A.5.24 | Circ. 2227 | — |
| RC-04 | Lecciones Aprendidas y Mejora | ID.IM | Cláusula 10 | Circ. 2227 | — |

### G · BCU
| Código | Documento | MCU 5.0 | ISO 27001 | BCU | URCDP |
|---|---|---|---|---|---|
| BCU-01 | Gobierno de Ciberseguridad y Riesgo Tecnológico | GV.OC/PO/RR | 5, A.5.1 | **EMG · Gobierno** | — |
| BCU-02 | Marco de Gestión de Riesgos (apetito) | GV.RM, ID.RA | 6.1 | **EMG · Marco de Riesgos** | — |
| BCU-03 | Función de Seguridad de la Información (2ª línea) | GV.RR, GV.OV | 5.2 | **EMG · Función Seguridad** | — |
| BCU-04 | Función de Gestión de TI (1ª línea) | PR/DE | 8 | **EMG · Gestión TI** | — |
| BCU-05 | Programa de Auditoría Interna de Seguridad | GV.OV | 9.2 | **EMG · Auditoría** | — |
| BCU-06 | Plan de Contingencia y Continuidad | RC | A.5.29 | **EMG · Continuidad** | — |

### H · URCDP
| Código | Documento | MCU 5.0 | ISO 27001 | BCU | URCDP |
|---|---|---|---|---|---|
| URCDP-01 | Documento de Seguridad de Datos Personales | PR.DS | A.8.12 | — | **Ley 18.331 art. 10; D.64/020** |
| URCDP-02 | Notificación de Vulneraciones de Seguridad | RS.CO | A.5.24 | Circ. 2227 | **Ley 19.670 art. 38; D.64/020** |
| URCDP-03 | Atención de Derechos ARCO | — | — | — | **Ley 18.331 arts. 14-17** |
| URCDP-04 | Inscripción de Bases de Datos | ID.AM | A.5.9 | — | **Ley 18.331 art. 22; D.414/009** |
| URCDP-05 | Evaluación de Impacto de Protección de Datos (EIPD) | ID.RA | 6.1 | — | **Ley 18.331 art. 12; D.64/020 art. 6.f** |
| URCDP-06 | Designación del Delegado de Protección de Datos | GV.RR | 5.3 | — | **Ley 19.670; D.64/020** |

### I · EVIDENCIA
| Código | Documento | MCU 5.0 | ISO 27001 | BCU | URCDP |
|---|---|---|---|---|---|
| EV-01 | Checklist de Requisitos del BCU | GV.OC/PO/RR · todas | 5–10 | **EMG (6 ejes) · art. 492 · Circ. 2227** | — |
| EV-02 | Checklist de Evidencias por Control | GV, ID, PR, DE, RS, RC | Anexo A | EMG · art. 492 | arts. 10, 12, 14-17, 22, 38 |
| EV-03 | Sistematización de las Evidencias | GV.OV | Cláusula 7.5 | EMG | Documento de Seguridad |
| EV-04 | Evidencias por Área, División y Sector | GV.RR · todas | A.5.9 | EMG | art. 10 |
| EV-05 | Indicadores y Métricas del SGSI | GV.OV · ID.IM · DE.CM · RC.RP | 9.1 | **EMG · Circ. 2280 · art. 492** | arts. 10, 38 |

## 4. Cómo usar esta matriz

1. En cada auditoría (Agesic, BCU, URCDP, interna) buscá el **código de documento** y verificá la evidencia.
2. Cuando un supervisor pregunte por un requisito (ej. "¿resguardo de datos?"), la matriz te dice: **PR-05 + RC-02 + BCU-06**.
3. Actualizá la matriz cuando: se agregue un documento, cambie una norma o cambie el alcance.

## 5. Verificación de cobertura (resumen)

- **MCU 5.0:** cubiertas las 6 funciones (GV, ID, PR, DE, RS, RC) con al menos 3 documentos por función.
- **ISO 27001:** cláusulas 4-10 + Anexo A (temas organizacionales, personas, físicas, tecnológicas).
- **BCU:** EMG (gobierno, marco de riesgos, función seguridad, gestión TI, auditoría, continuidad) + RNRCSF art. 492 + circulares (2227, 2419-2422, 2280).
- **URCDP:** principios, seguridad (art. 10), DPD, inscripción de bases, EIPD, ARCO, vulneraciones.
