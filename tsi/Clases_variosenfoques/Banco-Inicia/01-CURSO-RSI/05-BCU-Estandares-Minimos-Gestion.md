# Módulo 5 · Lo que el BCU espera del Banco: Estándares Mínimos de Gestión y normativa aplicable

> Nivel del curso: 🟡 Practicar → 🔴 Dominar
> Objetivo: entender la expectativa del **Banco Central del Uruguay (BCU)** sobre la seguridad de la información y la gestión de riesgos tecnológicos de una institución financiera como el Banco.

---

## 5.1. El BCU y el Banco

El Banco es supervisado por el BCU. En materia de seguridad de la información, el BCU espera que la institución tenga una **gestión de la seguridad de la información** acorde con su perfil de riesgo y con los estándares internacionales, integrada a la **gestión de riesgos** de la institución (riesgo operacional / tecnológico).

El BCU no "certifica" seguridad, pero **supervisa** y **sanciona** si detecta debilidades. Cuando ocurre un incidente grave, evalúa si la institución tenía el **marco de gestión** adecuado.

### El concepto de "Estándares Mínimos de Gestión (EMG)"

Son los estándares que el BCU toma como referencia para evaluar a las entidades supervisadas. Se inspiran en la metodología **CERT** (Instituto CERT de la Universidad Carnegie Mellon) y en las buenas prácticas internacionales. Cubren, en esencia:

1. **Gobierno** de la ciberseguridad y del riesgo tecnológico.
2. **Marco de gestión de riesgos** (apetito, adopción, tratamiento).
3. **Función de seguridad de la información** (la segunda línea: el RSI).
4. **Función de gestión de TI** (la primera línea: arquitectura, operaciones, desarrollo).
5. **Auditoría interna de seguridad** (tercera línea).
6. **Continuidad del negocio** y recuperación.

> Este kit traduce cada pilar en un **entregable de `02-ENTREGABLES/G-BCU/`** (BCU-01 … BCU-06).

---

## 5.2. Normativa BCU que tenés que conocer (y citar en tus documentos)

### a) Resguardo de datos, software y documentación — RNRCSF art. 492

Exige que la institución:
- Resguarde **datos, software y documentación** necesarios para reconstruir operaciones.
- Mantenga **copias** que no puedan verse afectadas por **un mismo evento** de riesgo (separación física y/o lógica).
- Resguarde las **claves de desencriptación**.
- Realice **pruebas anuales de recuperación e integridad** de los resguardos (de toda la información).
- Cuente con un **responsable de la ejecución del resguardo** (categoría de personal superior).

**Entregable:** `BCU-03` (función de seguridad) y `BCU-06` (continuidad), y en concreto las políticas de respaldo `PR-05` y `RC-02`.

### b) Gestión del riesgo operativo — Circular 2227

La institución debe gestionar el riesgo operativo, que incluye el **riesgo tecnológico**:
- Política de gestión de riesgo operativo aprobada por el Directorio.
- Proceso de **identificación, evaluación, medición, control y monitoreo**.
- Gestión de **incidentes**.
- Gestión de **continuidad de negocio**.
- Gestión de **terceros**.
- **Seguridad de la información** como componente del riesgo operativo.

### c) Tercerizaciones — Circulares 2419 a 2422 y Comunicación 2022/254

- Toda tercerización relevante debe estar **autorizada** (expresa si es en/desde el exterior).
- Se exige **evaluación de riesgos** del proveedor (solvencia técnica, legal, seguridad).
- **Contrato mínimo** con cláusulas de seguridad, resguardo de datos, auditoría, subcontratación.
- Actualización periódica del informe de riesgo.

**Entregable:** `GV-05` (riesgos de la cadena de suministro) y `PR-08` (confidencialidad y cláusulas).

### d) Sistema de pagos — Circular 2280 / RNSP

El Banco opera un **Departamento de Sistema de Pagos**. La normativa exige **calidad de servicio** con indicadores de: confidencialidad de los datos de la transacción, disponibilidad, integridad, **seguridad de la información e informática**, monitoreo y respuesta proactiva a incidentes, y continuidad.

### e) Datos y secretos bancarios

El Banco resguarda información sujeta a **secreto bancario** (Ley 16.713 / normas del sistema financiero). Esto refuerza las obligaciones de confidencialidad y de gestión de terceros.

---

## 5.3. Lo que el BCU espera ver (evidencia)

| Pregunta del supervisor | Evidencia que demuestra |
|---|---|
| ¿Hay gobierno? | Política aprobada, comité, RSI designado, informe a directorio |
| ¿Gestionan riesgos? | Metodología, registro de riesgos, plan de tratamiento |
| ¿Tienen seguridad de la información? | SGSI en marcha, controles implementados |
| ¿Protegen los datos? | Resguardo de datos, claves, pruebas anuales (art. 492) |
| ¿Controlan proveedores? | Registro de terceros, evaluación de riesgos, contratos |
| ¿Responden incidentes? | Plan de incidentes, notificaciones, lecciones aprendidas |
| ¿Aguantan una caída? | BCP/DRP, RTO/RPO definidos, pruebas realizadas |
| ¿Hay control interno? | Auditoría interna con programa de seguridad |

---

## 5.4. Correspondencia con el MCU 5.0 y el SGSI

| Pilar BCU | Función MCU 5.0 | SGSI ISO 27001 | Entregable |
|---|---|---|---|
| Gobierno | GV | 5 (Liderazgo) | BCU-01 |
| Marco de riesgos | ID.RA / GV.RM | 6 (Planificación) | BCU-02 |
| Función de seguridad | GV.RR / GV.OV | 5.2 | BCU-03 |
| Gestión de TI | PR / DE | 8 (Operación) | BCU-04 |
| Auditoría | GV.OV | 9.2 | BCU-05 |
| Continuidad | RC | A.5.29 / 5.30 | BCU-06 |

---

## 5.5. Autoexamen

1. ¿Qué es un "Estándar Mínimo de Gestión" y qué organismo lo aplica?
2. Nombrá 4 obligaciones del art. 492 de la RNRCSF.
3. ¿Qué exige el BCU al tercerizar servicios en/desde el exterior?
4. ¿Qué debe demostrar una institución ante un incidente grave?
5. ¿En qué función del MCU 5.0 encaja la continuidad de negocio?

---

**Siguiente:** `06-URCDP-Proteccion-Datos-Personales.md`
