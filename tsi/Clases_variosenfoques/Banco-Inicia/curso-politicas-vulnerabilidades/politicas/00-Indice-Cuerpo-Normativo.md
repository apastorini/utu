# VPOL-30 · Cuerpo Normativo del Banco: Políticas, Procedimientos y Procesos

> **Función del MCU 5.0:** Este cuerpo normativo ejecuta las funciones de Gobernar (GV), Proteger (PR) y Responder (RS): cada política establece el *qué*, cada proceso define el *cómo con responsables y plazos*, y cada procedimiento detalla el *paso a paso*.
> **ISO/IEC 27001:** El SGSI se sostiene en políticas (A.5.1), procesos documentados (A.5.22-A.5.23) y procedimientos operativos que dejan evidencia.
> **BCU:** Los Estándares Mínimos de Gestión (EMG) y el RNRCSF exigen un cuerpo normativo completo, formalizado y vigente para el riesgo de TIC.
> **URCDP:** La Ley 18.331 y el Decreto 64/020 requieren políticas y procedimientos de seguridad de datos personales y de notificación de vulneraciones.
> **Nivel del curso:** 🔴 Dominar

---

## 1. Qué es esta carpeta

La carpeta `politicas/` contiene el **cuerpo normativo completo que el Banco Ficticio del Uruguay debe tener** para sostener un SGSI auditable. Se organiza en tres niveles que se complementan:

| Nivel | Código | Pregunta que responde | Formato |
|---|---|---|---|
| **Políticas** | `P-POLITICAS/POL-01 … POL-20` | ¿Qué se debe cumplir? | Estructura de plantilla ISACA (VPOL-06…VPOL-20) |
| **Procesos** | `P-PROCESOS/PCS-01 … PCS-10` | ¿Quién, cuándo y con qué entradas/salidas? | Estructura del módulo VPOL-03 |
| **Procedimientos** | `P-PROCEDIMIENTOS/PRO-01 … PRO-13` | ¿Cuál es el paso a paso detallado? | Estructura operativa con pasos numerados |

La regla de oro de todo el kit:

> **La política dice el destino, el proceso dibuja el mapa y el procedimiento entrega el paso a paso. El control demuestra que se cumplió. Sin los tres niveles, un auditor no puede verificar nada.**

---

## 2. Índice de Políticas (P-POLITICAS/)

| Código | Política | Marco MCU 5.0 | Documento del kit |
|---|---|---|---|
| POL-01 | Seguridad de la Información (madre) | GV, PR, BCU | GV-01, BCU-01 |
| POL-02 | Uso Aceptable de los Sistemas | PR.AC, PR.DS | GV-01, PR-01 |
| POL-03 | Clasificación y Tratamiento de la Información | ID.AM, PR.DS | ID-01, PR-03, URCDP-01 |
| POL-04 | Gestión de Accesos y Privilegios | PR.AC | PR-01, PR-03 |
| POL-05 | Gestión de Vulnerabilidades | PR.PS, DE.CM | PR-06, DE-01 |
| POL-06 | Gestión de Cambios | PR.IP | PR-07, BCU-04 |
| POL-07 | Gestión de Incidentes y Respuesta | RS, DE | RS-01, DE-01, DE-02 |
| POL-08 | Continuidad del Negocio y Respaldos | RC | RC-01…RC-04, PR-05 |
| POL-09 | Seguridad Física y del Entorno | PR.PT | PR-03, PR-04 |
| POL-10 | Seguridad del Personal y Concienciación | PR.AT | PR-02, PR-08 |
| POL-11 | Gestión de Terceros y Proveedores | GV.SC | GV-05, PR-08 |
| POL-12 | Seguridad de Redes y Comunicaciones | PR.AC, PR.PT | PR-06, BCU-01 |
| POL-13 | Monitoreo, Registro y Evidencias (Logging) | DE.CM | DE-01, DE-02 |
| POL-14 | Criptografía y Gestión de Claves | PR.DS | PR-03, BCU-03 |
| POL-15 | Desarrollo Seguro (SDLC) | PR.PS | PR-07, BCU-04 |
| POL-16 | Dispositivos Móviles, Medios Removibles y Trabajo Remoto | PR.AC, PR.DS | PR-03, PR-04, PR-08 |
| POL-17 | Uso Aceptable de Inteligencia Artificial | GV, PR.DS | GV-01, PR-02, templates-ISACA-02 |
| POL-18 | Escritorio y Pantalla Limpia | PR.DS | PR-04, PR-03 |
| POL-19 | Servicios en la Nube | GV.SC, PR.DS | GV-05, PR-03, PR-08 |
| POL-20 | Protección de Datos Personales | PD.1…PD.8, CN | URCDP-01…06, DPD |

---

## 3. Índice de Procesos (P-PROCESOS/)

| Código | Proceso | Política que ejecuta | Evidencia que produce |
|---|---|---|---|
| PCS-01 | Gestión de Riesgos de Seguridad | POL-01 | Matriz de riesgos (ID-02, GV-03) |
| PCS-02 | Gestión de Vulnerabilidades | POL-05 | Escaneos, tickets, verificación |
| PCS-03 | Gestión de Incidentes | POL-07 | Registro de incidentes, notificaciones |
| PCS-04 | Gestión de Accesos e Identidades | POL-04 | Solicitudes, revisiones, altas/bajas |
| PCS-05 | Gestión de Cambios | POL-06 | RFC, actas, ventanas de cambio |
| PCS-06 | Respaldos y Continuidad | POL-08 | Logs de backup, pruebas de restauración |
| PCS-07 | Gestión de Proveedores | POL-11 | Evaluación, contratos, seguimiento |
| PCS-08 | Protección de Datos Personales | POL-20 | Registro de tratamientos, EIPD, DPD |
| PCS-09 | Monitoreo y Detección (SOC) | POL-13 | Alertas, tickets SOC, reportes |
| PCS-10 | Auditoría y Mejora Continua | POL-01 | Plan de auditoría, hallazgos, PDCA |

---

## 4. Índice de Procedimientos (P-PROCEDIMIENTOS/)

| Código | Procedimiento | Proceso relacionado |
|---|---|---|
| PRO-01 | Alta, modificación y baja de usuarios | PCS-04 |
| PRO-02 | Revisión periódica de accesos y privilegios | PCS-04 |
| PRO-03 | Configuración segura de estaciones y servidores (hardening) | PCS-02 |
| PRO-04 | Respuesta ante incidentes de seguridad | PCS-03 |
| PRO-05 | Notificación de vulneraciones de datos personales | PCS-03, PCS-08 |
| PRO-06 | Gestión de vulnerabilidades técnicas | PCS-02 |
| PRO-07 | Antivirus / EDR y respuesta a malware | PCS-09, PCS-03 |
| PRO-08 | Ingreso y egreso de personal y terceros | PCS-04, PCS-07 |
| PRO-09 | Clasificación, custodia, retención y destrucción de la información | PCS-08 |
| PRO-10 | Desarrollo seguro de software y código con IA | PCS-05, POL-15, POL-17 |
| PRO-11 | Control de cambios y gestión de configuración | PCS-05 |
| PRO-12 | Concientización, capacitación y simulacros | PCS-08, POL-10 |
| PRO-13 | Evaluación de seguridad de terceros y proveedores | PCS-07 |

---

## 5. Cómo usar esta carpeta

1. **Leé la política** (nivel 1): fija el *qué* y las reglas obligatorias.
2. **Revisá el proceso** (nivel 2): define *quién hace qué, con qué entrada y qué salida, en qué plazo*.
3. **Ejecutá el procedimiento** (nivel 3): da el *paso a paso* operativo.
4. **Registrá la evidencia**: cada paso que produce un registro (ticket, log, acta, reporte) es la prueba de cumplimiento.
5. **Adaptá y aprobá**: los `[COMPLETAR]` se llenan con la realidad del Banco y se someten al Comité de Seguridad.
6. **Convertí a DOCX** con `03-HERRAMIENTAS/md_a_docx.py` para la versión formal.

---

## 6. Prioridad de implementación

Si el Banco arranca de cero, este orden cubre lo esencial:

1. **POL-01** (madre) → 2. **POL-03** (clasificación) → 3. **POL-04** (accesos) → 4. **POL-05** (vulnerabilidades) → 5. **POL-07** (incidentes) → 6. **POL-08** (continuidad) → 7. **POL-20** (datos personales) → 8. **POL-06** (cambios) → 9. el resto.
10. En paralelo: **PCS-03** (incidentes), **PCS-02** (vulnerabilidades) y **PCS-04** (accesos), con sus procedimientos PRO-04/PRO-05, PRO-03 y PRO-01/PRO-02.

> **Recuerde:** una política sin proceso es papel mojado; un proceso sin procedimiento es ambiguo; un procedimiento sin evidencia es invisible ante el auditor. El cuerpo normativo completo es la base del SGSI.
