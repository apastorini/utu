# VPOL-05 · Las 15 plantillas ISACA y cómo adaptarlas

> **Función del MCU 5.0:** Las plantillas de ISACA cubren las funciones de Gobernar y Proteger, y alimentan la evidencia de todas las demás
> **ISO/IEC 27001:** Cada plantilla se vincula a controles del Anexo A
> **BCU:** Los EMG requieren políticas formalizadas para el riesgo tecnológico
> **URCDP:** Las plantillas deben completarse contemplando la Ley 18.331
> **Nivel del curso:** 🟡 Practicar

---

## 1. Qué son estas plantillas

ISACA publica un **kit de plantillas de políticas de seguridad** (ISACA Policy Template Package) que sirve como punto de partida profesional para armar el cuerpo normativo de un SGSI. Este curso incluye las **15 plantillas**, adaptadas a:

- El **contexto uruguayo**: Agesic (MCU 5.0, CERTuy), BCU (EMG, sistema de pagos), URCDP (Ley 18.331).
- El **Banco Ficticio del Uruguay** y su estructura (RSI, DPD, Comité de Seguridad, Div. TI, Seguridad Física).
- El **kit Banco-Inicia** (`02-ENTREGABLES/`, `03-HERRAMIENTAS/canonicos.txt`): cada plantilla indica qué documento canónico del kit la respalda.

## 2. Las 15 plantillas y su equivalencia con el kit

| Nº | Plantilla ISACA | Archivo | Documento del kit equivalente |
|---|---|---|---|
| 1 | Acceptable Use (Company Systems) Policy | `01-Acceptable-Use-Company-Systems.md` | GV-01, PR-01 |
| 2 | AI Acceptable Use Policy | `02-AI-Acceptable-Use.md` | GV-01, PR-02, GV-04 |
| 3 | Change Management Policy | `03-Change-Management.md` | PR-07, BCU-04 |
| 4 | Clear Desk Policy | `04-Clear-Desk.md` | PR-04, PR-03 |
| 5 | Cloud Computing Services Usage Policy | `05-Cloud-Computing-Services-Usage.md` | GV-05, PR-03, PR-08 |
| 6 | Data Backup Policy | `06-Data-Backup.md` | PR-05, RC-02 |
| 7 | Information Classification and Protection Policy | `07-Information-Classification-and-Protection.md` | ID-01, PR-03, URCDP-01 |
| 8 | Information Security Policy | `08-Information-Security.md` | GV-01, BCU-01 |
| 9 | Logging and Monitoring Policy | `09-Logging-and-Monitoring.md` | DE-01, DE-02 |
| 10 | Network Security Policy | `10-Network-Security.md` | PR-06, BCU-01, DMZ |
| 11 | Personnel Security Policy | `11-Personnel-Security.md` | PR-02, PR-08 |
| 12 | Removable Media Handling Policy | `12-Removable-Media-Handling.md` | PR-03, PR-04 |
| 13 | Third-Party Management Policy | `13-Third-Party-Management.md` | GV-05, PR-08 |
| 14 | User Access Management Policy | `14-User-Access-Management.md` | PR-01, PR-03 |
| 15 | Vulnerability Management Policy | `15-Vulnerability-Management.md` | PR-06, DE-01 |

## 3. Metodología de adaptación (mismo proceso para todas)

1. Abrí la plantilla `.md` en `templates-ISACA/`.
2. Completá el **encabezado** (código VPOL-NN, versión 1.0, estado, fecha).
3. Ajustá el **alcance** a la realidad del Banco (áreas, sedes, proveedores, activos).
4. Personalizá cada `[COMPLETAR]`: plazos, responsables, herramientas, métricas.
5. Verificá la columna "Evidencia del kit" y generá/adjuntá esa evidencia si corresponde.
6. Someté a **revisión del Comité de Seguridad** y luego a **aprobación**.
7. Publicá en el SGSI y registrá en el control de cambios (GV-06).
8. Regenerá el `.docx` con `03-HERRAMIENTAS/md_a_docx.py` para la versión formal.

## 4. Prioridad de implementación sugerida

Si se empieza desde cero, este orden cubre lo esencial primero:

1. **Information Security Policy** (08) — la política madre.
2. **User Access Management** (14) — accesos, el riesgo más frecuente.
3. **Vulnerability Management** (15) — el foco del curso.
4. **Acceptable Use** (01) — uso aceptable de los sistemas.
5. **Change Management** (03) — estabilidad y trazabilidad de cambios.
6. **Data Backup** (06) — continuidad.
7. **Logging and Monitoring** (09) — detectar.
8. El resto según el plan de tratamiento de riesgos.

## 5. Formato interno de cada plantilla

Cada plantilla comparte la misma estructura que los documentos de `02-ENTREGABLES/`:

- **Encabezado** (código, título, versión, estado).
- **Marco de referencia** (Agesic / ISO 27001 / BCU / URCDP).
- **Secciones normativas** (objetivo, alcance, roles, reglas) con `[COMPLETAR]`.
- **Cumplimiento, excepciones y revisión**.
- **Evidencia del kit** (qué documento/s canónico/s la respaldan).

---

**Siguiente paso:** abrí las plantillas una por una en `templates-ISACA/`, o empezá por la prioridad sugerida en el punto 4.
