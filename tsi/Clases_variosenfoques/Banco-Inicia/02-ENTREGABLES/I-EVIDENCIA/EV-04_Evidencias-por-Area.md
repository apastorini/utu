# EV-04 · Evidencias por Área, División y Sector (qué esperar y cómo ayudar a que lleguen)

> **Función del MCU 5.0:** Todas las funciones: cada área del Banco es dueña de activos y, por lo tanto, fuente de evidencia.
> **ISO/IEC 27001:** A.5.9 (propiedad de los activos) y cláusula 7.5 (información documentada).
> **BCU:** Los EMG exigen que la evidencia sea provista por la primera línea (TI), validada por la segunda (RSI) y evaluada por la tercera (Auditoría).
> **URCDP:** Las áreas que tratan datos personales deben aportar las medidas de seguridad documentadas.
> **Nivel del curso:** 🔴 Dominar · **Uso:** mapa de trabajo del RSI para pedir evidencias a cada división.

---

## 1. Qué es este documento

Este mapa te dice, **por división/sector/área del Banco**, qué evidencias deberían poder aportar y **cómo ayudarlas para que las entreguen**. Sigue el organigrama del Banco (Módulo 7) y se complementa con EV-02 (qué evidencia pedir por control).

> **Regla de oro:** la evidencia se pide **al dueño del activo/control**, no a quien "tiene buena voluntad". Y se ayuda: darle plantillas, ejemplos y plazos claros aumenta la tasa de respuesta drásticamente.

---

## 2. División Tecnología de la Información (TI) — la mayor fuente de evidencia

### Qué debe poder aportar
| Área/sector | Evidencia esperada (EV-02) | Doc. del kit |
|---|---|---|
| **Producción / Operaciones** | Reportes de respaldo y restauración · Logs de monitoreo (SIEM) · Registro de operaciones | PR-05 · DE-01 · BCU-04 |
| **Sistemas / Desarrollo** | Reportes SAST/DAST · Política de desarrollo seguro · Registro de cambios | PR-07 · BCU-04 |
| **Soporte / Mesa de ayuda** | Registro de incidentes técnicos · Tickets cerrados con tiempo de respuesta | BCU-04 · RS-01 |
| **Seguridad informática (si existe)** | Alertas del SIEM · Gestión de vulnerabilidades · Registro de accesos privilegiados | DE-02 · PR-06 · PR-01 |
| **Arquitectura / Redes** | Diagramas de red · Segmentación (DMZ, VLAN) · Firewalls y reglas · Inventario de red | ID-01 · PR-04 · curso-infra |

### Cómo ayudarlos
1. **Pedirles exportaciones, no capturas**: darles el listado de qué exportar de cada sistema (GLPI, Wazuh, respaldos).
2. **Darles un calendario de pedidos**: agrupar las evidencias por frecuencia (mensual/semestral/anual) para que no les caigan 20 pedidos de golpe.
3. **Ejemplos de formato**: mostrarles una evidencia "modelo" ya validada.
4. **Reunión breve de alineación** una vez al trimestre: qué les falta, qué bloqueos tienen.

---

## 3. División Riesgos (No Financieros) y el RSI

### Qué debe poder aportar
| Evidencia esperada | Doc. del kit |
|---|---|
| Metodología de análisis de riesgos aprobada | ID-02 |
| Registro de riesgos actualizado | ID-03 |
| Plan de tratamiento y riesgos residuales aceptados | ID-04 · BCU-02 |
| Informe del RSI a la Dirección | GV-06 · BCU-01 |
| Actas del Comité de Seguridad | GV-03 |

### Cómo ayudarlos
- Son el propio equipo del RSI: la evidencia la **generan** ellos; el desafío es documentarla. Crear plantillas ya hechas (ID-02/03/04) y guardarlas en el repositorio.

---

## 4. División Auditoría Interna (3ª línea)

### Qué debe poder aportar
| Evidencia esperada | Doc. del kit |
|---|---|
| Programa anual de auditoría de seguridad | BCU-05 |
| Informes de auditoría interna (hallazgos y seguimiento) | BCU-05 |
| Ejecución de la auditoría (criterios, alcance, planillas de trabajo) | BCU-05 · INFRA-07 |

### Cómo ayudarlos
- Coordinar el calendario de auditorías con el RSI (BCU-05 §9): el RSI aporta el mapa de controles (EV-01/EV-02) y los auditores usan la MATRIZ-001 como base de criterios.

---

## 5. División Capital Humano

### Qué debe poder aportar
| Evidencia esperada | Doc. del kit |
|---|---|
| Registros de asistencia a capacitación de seguridad | PR-02 |
| Acuerdos de confidencialidad firmados por el personal | PR-08 |
| Procesos de alta/baja de personal (accesos) coordinados con TI | PR-01 |
| Resultados de concientización (simulacros) | PR-02 · TOOLS-08 |

### Cómo ayudarlos
- **Darles el material hecho**: las charlas/cursos (PR-02, kit) y la plantilla de registro de asistencia. Si solo tienen que "llenar y firmar", lo hacen.
- Definir con TI el flujo de **baja inmediata de accesos** al cese (evidencia de PR-01).

---

## 6. División Administración General y Seguridad Física

### Qué debe poder aportar
| Evidencia esperada | Doc. del kit |
|---|---|
| Controles de ingreso a instalaciones (registros, visitas, tarjetas) | PR-04 |
| Perímetros y áreas restringidas (planos, cámaras, sala de servidores) | PR-04 |
| Gestión de proveedores de limpieza/seguridad/mantenimiento (acceso a áreas) | PR-04 · GV-05 |

### Cómo ayudarlos
- Pedirles **registros ya existentes** (bitácoras de visitas, planos de cámaras): no pedir que "generen un documento nuevo". La evidencia de control físico casi siempre existe en formato de registro.

---

## 7. División Servicios Jurídicos Notariales y Secretaría General

### Qué debe poder aportar
| Evidencia esperada | Doc. del kit |
|---|---|
| Resoluciones y actas del Directorio (aprobación de políticas) | GV-01 · BCU-01 |
| Contratos y acuerdos de confidencialidad con terceros | PR-08 · GV-05 |
| Normativa interna y designaciones (RSI, DPD) | GV-03 · BCU-03 · URCDP-06 |

### Cómo ayudarlos
- Solicitar las resoluciones **por escrito y con número**, porque son la evidencia formal de gobierno más fuerte.
- Coordinar con Legal la revisión de cláusulas de confidencialidad y protección de datos (PR-08).

---

## 8. Áreas de negocio (Banca Persona, Canales y Apoyo Comercial, etc.)

### Qué debe poder aportar
| Evidencia esperada | Doc. del kit |
|---|---|
| Registro de activos de su área (sistemas, datos, procesos) | ID-01 |
| BIA: impacto de sus procesos de negocio (RTO/RPO) | BCU-06 · RC-01 |
| Riesgos operativos del área (input al registro de riesgos) | ID-03 |
| Procedimientos operativos del área documentados | ID-01 · BCU-04 |

### Cómo ayudarlos
- **Entrevistarlas con preguntas guiadas** (plantillas del Curso-relevamiento, RELEV-03 a 06): la evidencia de negocio se obtiene mejor en reunión que por correo.
- **Devolverles el valor**: explicar que el BIA y el inventario les sirven a ellos (proteger su operación), no es solo un pedido del RSI.

---

## 9. Oficinas y sucursales (red comercial)

### Qué debe poder aportar
| Evidencia esperada | Doc. del kit |
|---|---|
| Controles físicos y de accesos de la sucursal | PR-04 |
| Procedimientos de atención (datos personales de clientes) | URCDP-01 |
| Registro de incidentes locales (reportados al RSI/TI) | RS-01 · RS-02 |
| Capacitación recibida (asistencia) | PR-02 |

### Cómo ayudarlos
- **Plantillas precargadas y simples**: las sucursales no tienen tiempo ni expertise; entregarles un formulario de una página por tema.
- **Un canal único de reporte**: definir a quién avisan (TI o RSI) y cómo (correo, formulario) ante un incidente local.
- **Visitas de relevamiento** con checklist (RELEV-04) en vez de pedidos remotos.

---

## 10. División Finanzas, Contaduría y Planificación

### Qué debe poder aportar
| Evidencia esperada | Doc. del kit |
|---|---|
| Presupuesto de seguridad (recursos asignados) | GV-04 |
| Riesgos financieros/operativos vinculados a la seguridad | ID-03 · BCU-02 |
| BIA de procesos financieros críticos | BCU-06 · RC-01 |

### Cómo ayudarlos
- Pedir la evidencia **en su lenguaje** (presupuesto, riesgo financiero) y enlazarla al informe del RSI (GV-06).

---

## 11. Cómo pedir y hacer seguimiento (resumen práctico)

1. **Un solo pedido consolidado** por área (plantilla RELEV-07), no pedidos sueltos.
2. **Plazo claro** (7–10 días hábiles típico) y **un interlocutor por área**.
3. **Seguimiento en la planilla EV-03**: estado Solicitada → Recibida → Validada → Brecha.
4. **Reunión de alineación trimestral** con los referentes de cada división.
5. **Reforzar positivamente**: agradecer y mostrar cómo se usó su evidencia (en el informe GV-06).
6. **Escalar solo lo urgente**: si un área no responde, subirlo al Comité de Seguridad (GV-03) con el dato objetivo de la planilla.

---

## 12. Matriz resumen: división → evidencias clave → cómo ayudar

| División/Sector | Evidencias clave | Doc. | Cómo ayudarlos |
|---|---|---|---|
| TI (Operaciones/Sistemas/Soporte/Redes) | Respaldos, logs, SDLC, parches, accesos, diagramas | PR-05/07 · DE-01/02 · PR-06/01 · ID-01 | Pedir exports, calendario de pedidos, ejemplos, reunión trimestral |
| Riesgos No Financieros / RSI | Metodología, registro de riesgos, plan, informes | ID-02/03/04 · GV-06 | Plantillas precargadas en el repositorio |
| Auditoría Interna | Programa anual, informes, seguimiento | BCU-05 | Coordinar calendario; MATRIZ-001 como base |
| Capital Humano | Capacitación, confidencialidad, altas/bajas | PR-02 · PR-08 · PR-01 | Material listo para "llenar y firmar" |
| Administración General / Física | Registros de ingreso, perímetros, visitas | PR-04 | Usar registros existentes (bitácoras) |
| Legal / Secretaría General | Resoluciones, contratos, designaciones | GV-01 · PR-08 · GV-03 | Pedido escrito con número de resolución |
| Áreas de negocio | Activos, BIA, riesgos operativos | ID-01 · BCU-06 · ID-03 | Entrevistas guiadas (RELEV-03/05) |
| Sucursales / oficinas | Controles físicos, procedimientos, incidentes | PR-04 · URCDP-01 · RS-01/02 | Formularios de 1 página, canal único, visitas |
| Finanzas / Contaduría / Planificación | Presupuesto, riesgos, BIA financiero | GV-04 · ID-03 · BCU-06 | Hablar su lenguaje, enlazar a GV-06 |

---

## 13. Checklist de cierre del RSI

- ☐ Identifiqué las evidencias clave por división/sector (tabla del §12).
- ☐ Definí un interlocutor por área.
- ☐ Envié pedidos consolidados con plazos claros (RELEV-07).
- ☐ Armé el calendario trimestral de alineación con las divisiones.
- ☐ Las áreas recibieron plantillas/ejemplos para facilitarles la entrega.
- ☐ El seguimiento está en la planilla EV-03.
- ☐ Las brechas por área están registradas y escaladas al Comité si corresponde.

---

**Documentos relacionados:** EV-01, EV-02, EV-03, MATRIZ-001, Módulo 7 (Organigrama), BCU-01…06, GV-03, GV-04, GV-06, PR-01…08, ID-01…05, RS-01/02, RC-01, URCDP-01, Curso-relevamiento (RELEV-03 a 07), curso-infra
