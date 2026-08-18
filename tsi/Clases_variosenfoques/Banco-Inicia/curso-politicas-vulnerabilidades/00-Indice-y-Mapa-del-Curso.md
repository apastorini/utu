# VPOL-00 · Índice y Mapa del Curso

> **Función del MCU 5.0:** Este curso ejecuta en la práctica las funciones GV (Gobernar) y PR (Proteger) del Marco de Ciberseguridad de Agesic 5.0: sin políticas claras, procesos definidos y controles verificables no hay SGSI auditable.
> **ISO/IEC 27001:** Cada política se vincula a controles del Anexo A (A.5 políticas, A.6 organización, A.8 gestión de activos, A.12 seguridad de operaciones, A.13 seguridad de comunicaciones, A.15 relaciones con proveedores, A.16 gestión de incidentes, A.18 cumplimiento).
> **BCU:** Las políticas y procesos del kit demuestran los Estándares Mínimos de Gestión (EMG) y el RNRCSF: gobierno, gestión de riesgos y continuidad.
> **URCDP:** La redacción de políticas debe contemplar la Ley 18.331 (datos personales) y el régimen de vulneraciones de seguridad.
> **Nivel del curso:** 🟢 Descubrir → 🟡 Practicar → 🔴 Dominar

---

## 1. Presentación del curso

Bienvenido al curso **"Gestión de vulnerabilidades y redacción de políticas, procesos y controles de seguridad"**. Vive en la carpeta `curso-politicas-vulnerabilidades` y forma parte del kit **Banco-Inicia**.

Este curso tiene dos mitades que se complementan:

1. **Gestión de vulnerabilidades (enfoque Uruguay):** qué es una vulnerabilidad, cómo se descubre, prioriza y corrige, qué exigen Agesic, el BCU y la URCDP, y cómo se demuestra el cumplimiento con evidencia.
2. **Redacción de documentos de seguridad:** cómo se escribe una política, un proceso y un control de forma clara, accionable y auditable, usando como base las **15 plantillas de políticas de ISACA** adaptadas al contexto uruguayo y al Marco de Ciberseguridad 5.0.

La lógica es la misma que en todo el kit: **aprendé el concepto → abrí la plantilla → completala con el caso Banco → guardala en la estructura del SGSI → seguilda en la planificación**.

---

## 2. Para quién es este curso

| Perfil | Por qué le sirve |
|---|---|
| Responsable de Seguridad de la Información (RSI) | Redacta, aprueba y supervisa políticas, procesos y controles; gestiona vulnerabilidades como parte de Proteger. |
| Delegado de Protección de Datos (DPD) | Necesita políticas que contemplen datos personales (URCDP-01, notificación de vulneraciones). |
| Oficial de Seguridad / TI | Ejecuta los procesos (parcheo, accesos, respaldos) y debe entender qué se espera de cada control. |
| Auditoría Interna | Evalúa si las políticas están escritas, son coherentes, se cumplen y se evidencian. |
| Consultores del proyecto SGSI | Tienen la base para redactar el "cuerpo normativo" del SGSI del Banco. |

### Qué vas a saber al terminar

- Qué es una vulnerabilidad, qué es un CVE y un CVSS, y cómo se **gestiona el ciclo completo** (identificar → evaluar → priorizar → corregir → verificar) con los plazos que espera Agesic.
- Qué exige cada norma uruguaya (Agesic MCU 5.0, BCU EMG, URCDP Ley 18.331) y **dónde se evidencia** en el kit.
- Cómo se estructura una **política** (objetivo, alcance, roles, reglas, cumplimiento, revisión), un **proceso** (entradas, pasos, salidas, responsables, métricas) y un **control** (objetivo, implementación, evidencia, frecuencia).
- Las **15 plantillas ISACA** y cómo adaptarlas al Banco: desde Aceptable Use hasta Vulnerability Management.
- Tener el **cuerpo normativo completo del Banco** (`politicas/`): 20 políticas, 10 procesos y 13 procedimientos listos para completar, aprobar y evidenciar ante el auditor.

---

## 3. Los módulos del curso

| Módulo | Tema | Nivel | Documentos del kit que alimenta |
|---|---|---|---|
| VPOL-00 | Índice y mapa del curso | 🟢 | Todos (puerta de entrada) |
| VPOL-01 | Gestión de vulnerabilidades en Uruguay | 🟢→🟡 | PR-06, ID-01, BCU-01 |
| VPOL-02 | Cómo se redacta una política de seguridad | 🟡→🔴 | GV-01, PR-01…08 |
| VPOL-03 | Cómo se redacta un proceso de seguridad | 🟡→🔴 | RS-01, DE-01, PR-06 |
| VPOL-04 | Cómo se redacta un control y su evidencia | 🟡→🔴 | EV-01…05, BCU-05 |
| VPOL-05 | Las 15 plantillas ISACA y cómo adaptarlas | 🟡 | Todos (índice de templates) |
| VPOL-06 | Template: Acceptable Use (Company Systems) | 🟡 | GV-01, PR-01 |
| VPOL-07 | Template: AI Acceptable Use | 🟡 | GV-01, PR-02 |
| VPOL-08 | Template: Change Management | 🔴 | PR-07, BCU-04 |
| VPOL-09 | Template: Clear Desk | 🟢 | PR-04, PR-03 |
| VPOL-10 | Template: Cloud Computing Services Usage | 🔴 | GV-05, PR-03 |
| VPOL-11 | Template: Data Backup | 🟡 | PR-05, RC-02 |
| VPOL-12 | Template: Information Classification and Protection | 🟡 | ID-01, PR-03, URCDP-01 |
| VPOL-13 | Template: Information Security Policy | 🟡 | GV-01, BCU-01 |
| VPOL-14 | Template: Logging and Monitoring | 🟡 | DE-01, DE-02 |
| VPOL-15 | Template: Network Security | 🔴 | PR-06, BCU-01, DMZ |
| VPOL-16 | Template: Personnel Security | 🟢 | PR-02, PR-08 |
| VPOL-17 | Template: Removable Media Handling | 🟢 | PR-03, PR-04 |
| VPOL-18 | Template: Third-Party Management | 🔴 | GV-05, PR-08, BCU |
| VPOL-19 | Template: User Access Management | 🟡 | PR-01, PR-03 |
| VPOL-20 | Template: Vulnerability Management | 🔴 | PR-06, DE-01 |
| VPOL-21 | Correspondencia normativa y checklist final | 🔴 | MATRIZ-001, BCU-05, ID-05 |
| VPOL-30 | Cuerpo normativo del Banco: 20 políticas, 10 procesos y 13 procedimientos | 🔴 | GV-01, PR-01…08, RS-01, URCDP-01…06 |

> Los templates (VPOL-06 a VPOL-20) viven en `templates-ISACA/` y son plantillas listas para completar, al estilo de las de `02-ENTREGABLES/`.

> El **cuerpo normativo completo** (VPOL-30) vive en `politicas/`, organizado en tres niveles: `P-POLITICAS/` (POL-01…POL-20, el *qué*), `P-PROCESOS/` (PCS-01…PCS-10, el *cómo con responsables y plazos*) y `P-PROCEDIMIENTOS/` (PRO-01…PRO-13, el *paso a paso*). Cada política y proceso cita los documentos canónicos del kit que evidencia su cumplimiento. Iniciá por `politicas/00-Indice-Cuerpo-Normativo.md`.

---

## 4. Cómo usar las plantillas ISACA

1. Abrí la plantilla en `templates-ISACA/` (`.md` editable).
2. Revisá el encabezado (código, versión, estado) y la sección "Marco de referencia".
3. Completá los `[COMPLETAR]` con la realidad del Banco y los responsables reales.
4. Relacionala con el documento del kit de `02-ENTREGABLES/` que corresponda (la plantilla indica el código).
5. Aprobá, registrá en el control de cambios y publicá.
6. Regenerá el `.docx` con `03-HERRAMIENTAS/md_a_docx.py`.

---

**Siguiente paso:** abrí `VPOL-01-Gestion-de-Vulnerabilidades-en-Uruguay.md` para entender el problema que estas políticas resuelven.
