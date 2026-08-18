# Módulo 4 · Tu rol: el Responsable de Seguridad de la Información (RSI) en el Banco

> Nivel del curso: 🟡 Practicar → 🔴 Dominar
> Objetivo: saber exactamente **qué hace el RSI**, qué autoridad tiene, ante quién responde y cómo se relaciona con el resto del banco.

---

## 4.1. ¿Quién es el RSI?

El **Responsable de Seguridad de la Información (RSI)** es la persona designada formalmente por la máxima autoridad del Banco para **dirigir, coordinar y supervisar** la seguridad de la información.

Según el modelo que esperan **Agesic** (Marco de Ciberseguridad) y el **BCU** (función de seguridad de la información dentro de los estándares de gestión), el RSI:

- Es **segunda línea de defensa**: no ejecuta TI (eso es primera línea), pero **controla y asesora** a quien la ejecuta.
- Tiene **autoridad formal** otorgada por el Directorio o la Gerencia General (designación documentada).
- Es **independiente** del área que implementa los controles (para poder cuestionarla).
- Reporta periódicamente al **Comité de Seguridad** y al **Directorio**.

> **Modelo de tres líneas:** (1) negocio y TI ejecutan controles → (2) RSI/riesgos supervisan y asesoran → (3) auditoría interna evalúa todo.

---

## 4.2. Funciones del RSI en el Banco (checklist operativo)

### Gobierno y estrategia
- [ ] Mantener la **Política de Seguridad de la Información** vigente y aprobada (GV-01).
- [ ] Proponer el **Plan Anual de Seguridad** y su presupuesto (GV-04).
- [ ] Participar del **Comité de Seguridad** (y convocarlo, si le corresponde).
- [ ] Definir y difundir **normas y procedimientos** de seguridad.
- [ ] Informar periódicamente a la dirección sobre el estado del SGSI (GV-06).

### Riesgos
- [ ] Mantener actualizados el **inventario de activos** (ID-01) y la **evaluación de riesgos** (ID-02/03).
- [ ] Mantener el **plan de tratamiento de riesgos** (ID-04) y la **Declaración de Aplicabilidad**.
- [ ] Asesorar sobre el **apetito de riesgo** aceptado por la dirección.

### Operación y controles
- [ ] Supervisar la implementación de los controles de **Proteger** (PR-01…08).
- [ ] Coordinar la gestión de **vulnerabilidades** y el monitoreo (**Detectar**).
- [ ] Validar la **clasificación de la información** y los **accesos** (menor privilegio, revisión periódica).

### Incidentes y continuidad
- [ ] Dirigir el **Plan de Respuesta a Incidentes** (RS-01).
- [ ] Garantizar la **notificación a URCDP, BCU y CERTuy** en plazo (RS-02).
- [ ] Participar de las pruebas de **continuidad y recuperación** (RC-01/02).

### Cumplimiento y mejora
- [ ] Verificar el cumplimiento normativo (MCU 5.0, BCU, URCDP) y alimentar la **matriz de correspondencia**.
- [ ] Coordinar **auditorías internas de seguridad** (BCU-05) y dar seguimiento a hallazgos.
- [ ] Reportar **indicadores** del SGSI a la dirección (GV-06).

> Todas estas tareas tienen su plantilla en `02-ENTREGABLES/`. El RSI no "inventa" nada: sigue el kit y adapta al Banco.

---

## 4.3. Autoridad, independencia y reporte

| Tema | Práctica recomendada |
|---|---|
| **Designación** | Resolución del Directorio/Gerencia General, con funciones y alcance |
| **Autoridad** | Puede detener una operación crítica de seguridad, requerir información a cualquier área, y proponer sanciones |
| **Independencia** | No debe depender jerárquicamente de la División de TI (para poder controlarla). En el Banco encaja en **Área Riesgos (Riesgos No Financieros)** |
| **Reporte** | Al menos semestral al Comité de Seguridad y anualmente al Directorio (o ante incidentes graves, inmediato) |
| **Dedicación** | Función de dedicación exclusiva o con dedicación significativa, no una "etiqueta" más en un cargo operativo |

---

## 4.4. El RSI y los otros roles de seguridad (quién es quién)

| Rol | Función | ¿Es el RSI? |
|---|---|---|
| **RSI** | Seguridad de la información y ciberseguridad | Sí |
| **Delegado de Protección de Datos (DPD/DPO)** | Cumplimiento de datos personales, derechos ARCO, EIPD | Puede ser la misma persona en organizaciones chicas; en el Banco se recomienda diferenciar |
| **Oficial de Cumplimiento** | Prevención de lavado de activos, normativa BCU (PLA/FT) | No, pero se coordinan |
| **Jefe de Riesgos No Financieros** | Riesgo operacional, de continuidad y reputacional | Es el área donde mejor "vive" el RSI |
| **Auditoría Interna** | Evaluación independiente de los controles | No (es tercera línea) |
| **Gerente de División TI** | Implementación técnica de los controles | No (es primera línea) |

> El Banco ya cuenta con un **Oficial de Cumplimiento** y un **Departamento de Riesgos No Financieros** en el organigrama (ver `07-Organigrama.md`). El RSI debe coordinarse con ambos.

---

## 4.5. La matriz RACI del RSI

**RACI:** Responsable (hace) / Aprobador (Accountable) / Consultado (Consulted) / Informado (Informed).

| Actividad | Directorio | Comité Seg. | RSI | Div. TI | Auditoría |
|---|---|---|---|---|---|
| Aprobar la política | **A** | C | R | C | I |
| Análisis de riesgos | I | C | **R** | C | I |
| Implementar controles técnicos | I | I | A | **R** | I |
| Gestión de incidentes | I | C | **R** | C | I |
| Notificación a URCDP/BCU | I | I | **A** | R | I |
| Auditoría interna | I | I | C | C | **R** |
| Revisión por la dirección | **A** | C | R | C | I |

---

## 4.6. Competencias del RSI

- Conocimiento de **ISO 27001**, **MCU 5.0**, normativa **BCU** y **URCDP**.
- Gestión de **riesgos** (ISO 27005 / metodologías cualitativas).
- Conceptos técnicos: red, sistemas, aplicaciones, nube, cifrado, vulnerabilidades.
- Gestión de **incidentes** y comunicación de crisis.
- Habilidades de **comunicación** y liderazgo (debe convencer a toda la organización).
- Formación continua (certificaciones sugeridas: ISO 27001 Lead Implementer/Auditor, CISM, CISSP).

---

## 4.7. Autoexamen

1. ¿Por qué el RSI debe ser independiente de TI?
2. Nombrá 5 funciones clave del RSI.
3. ¿Qué diferencia hay entre RSI, DPD y Oficial de Cumplimiento?
4. ¿En qué área del organigrama del Banco recomendarías ubicar al RSI y por qué?
5. ¿Qué es la "segunda línea de defensa" y qué rol juega el RSI?

---

**Siguiente:** `05-BCU-Estandares-Minimos-Gestion.md`
**Complemento:** Módulo 8 (`08-Dia-a-Dia-del-RSI.md`) — cómo se vive el rol en la práctica: agenda realista, conversaciones y cómo no quemarte.
