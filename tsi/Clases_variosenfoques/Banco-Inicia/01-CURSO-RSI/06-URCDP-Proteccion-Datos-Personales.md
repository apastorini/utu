# Módulo 6 · Datos personales: obligaciones del Banco ante la URCDP

> Nivel del curso: 🟡 Practicar → 🔴 Dominar
> Objetivo: dominar la normativa de **protección de datos personales** aplicable al Banco: principios, obligaciones formales, seguridad, derechos de los titulares y comunicación de vulneraciones.

---

## 6.1. El marco normativo (memorizalo)

| Norma | Contenido central |
|---|---|
| **Ley 18.331** (2008) | Ley de Protección de Datos Personales y Acción de Habeas Data. Principios y derechos. |
| **Decreto 414/009** | Reglamentación de la Ley 18.331: medidas de seguridad (arts. 7-8), inscripción de bases de datos. |
| **Ley 19.670** (2018) | Reforma: responsabilidad proactiva, **Delegado de Protección de Datos (DPD)**, **comunicación de vulneraciones** (art. 38). |
| **Decreto 64/020** | Reglamenta la Ley 19.670: seguridad (arts. 3-4), plazos de notificación, **evaluaciones de impacto** (art. 6 lit. f), **privacidad por diseño** (arts. 7-8). |
| **Resolución 41/021** | Salvaguardas para **transferencias internacionales** de datos. |

---

## 6.2. Los principios de la Ley 18.331 (arts. 4 a 12)

| Principio | En criollo |
|---|---|
| **Licitud** | Tratar datos solo cuando hay base legal (consentimiento u otra habilitación) |
| **Calidad** | Datos exactos, completos y actualizados |
| **Consentimiento** | Pedir autorización expresa e informada, salvo excepciones legales |
| **Finalidad** | Usar los datos solo para la finalidad declarada |
| **Seguridad** | Medidas necesarias para evitar adulteración, pérdida o acceso no autorizado (art. 10) |
| **Reserva** | Confidencialidad de los datos incluso después de finalizar la relación |

### El principio de seguridad (art. 10) — el que más nos importa

> "El responsable o usuario de la base de datos debe adoptar las medidas que resultaren necesarias para garantizar la seguridad y confidencialidad de los datos personales... **Queda prohibido registrar datos personales en bases de datos que no reúnan condiciones técnicas de integridad y seguridad.**"

El Decreto 64/020 refuerza que las medidas deben ser **necesarias** (no solo "idóneas") y sugiere **valorar la adopción de estándares nacionales e internacionales** — señalando expresamente el **Marco de Ciberseguridad de Agesic**. Es la razón por la que este kit integra MCU 5.0 + URCDP.

---

## 6.3. Obligaciones concretas del Banco (sector público)

Según la URCDP, el Banco como organismo público debe:

1. **Inscribir sus bases de datos** de datos personales ante la URCDP (art. 22 Ley 18.331). → `URCDP-04`
2. Solicitar **consentimiento** (salvo excepciones). → `URCDP-03`
3. Cumplir todos los **principios**.
4. Facilitar el ejercicio de los **derechos ARCO** (Acceso, Rectificación, Cancelación, Oposición) y la **impugnación de valoraciones personales**. → `URCDP-03`
5. Implementar **medidas de seguridad** para el almacenamiento y gestión. → `URCDP-01`
6. Adoptar **cláusulas de tratamiento** en contratos con encargados. → `PR-08`
7. **Capacitar** a los funcionarios en tratamiento de datos. → `PR-02`
8. Contar con **políticas de privacidad** en su sitio web. → `URCDP-01`
9. Si usa **videovigilancia**: cartelería aprobada + inscribir la base. → `PR-04`
10. Designar un **Delegado de Protección de Datos (DPD)**. → `URCDP-06`
11. Realizar **evaluaciones de impacto** cuando corresponda. → `URCDP-05`
12. Comunicar **vulneraciones de seguridad**. → `URCDP-02`

---

## 6.4. Comunicación de vulneraciones de seguridad (art. 38 Ley 19.670 / Decreto 64/020)

Es la obligación con **plazos estrictos**. Resumen operativo:

| Acción | Plazo |
|---|---|
| Iniciar los **procedimientos** para minimizar el impacto desde que se constata el incidente | **24 h** |
| Comunicar a la **URCDP** la vulneración | **máx. 72 h** desde que se conoce (la URCDP recomienda cuanto antes, y en su portal señala el plazo de 24 h para la notificación vía el sistema) |
| Comunicar a los **titulares** de los datos afectados | inmediatamente y pormenorizadamente |
| Coordinar con **CERTuy** | la URCDP coordina el curso de acción |

### Contenido mínimo de la comunicación

- Fecha cierta o estimada de la vulneración y su **naturaleza**.
- **Datos personales afectados** y titulares involucrados.
- **Impactos** potenciales.
- **Medidas adoptadas** o a adoptar.

> **Entregable crítico:** `RS-02` (procedimiento) y `URCDP-02` (formulario/guía). El RSI debe poder notificar **en horas**, no en semanas.

---

## 6.5. El Delegado de Protección de Datos (DPD)

Es **obligatorio** designarlo cuando:
- Se tratan **datos sensibles como negocio principal** (origen racial, preferencias políticas, convicciones religiosas/morales, afiliación sindical, salud o vida sexual), **o**
- Se tratan datos de **más de 35.000 personas** (sumando todas las bases de datos).

El Banco claramente supera los 35.000 titulares → **debe designar DPD** y comunicar la designación a la URCDP vía su sistema de gestión.

### Funciones del DPD
- Supervisar el cumplimiento de la normativa de datos.
- Asesorar sobre evaluaciones de impacto.
- Cooperar con la URCDP.
- Gestionar las solicitudes de derechos.
- Coordinar la comunicación de vulneraciones.

> **Entregable:** `URCDP-06`. Diferenciá DPD (datos personales) de RSI (seguridad de la información); en el Banco se recomienda que sean roles distintos que se coordinan.

---

## 6.6. Evaluación de Impacto en Protección de Datos (EIPD)

Obligatoria (art. 6 lit. f Decreto 64/020) cuando el tratamiento implique, entre otros:
- Datos **sensibles**.
- Datos de **personas vulnerables o especialmente protegidas**.
- Datos de **más de 35.000 personas**.
- **Transferencias** a países no adecuados.
- Datos **biométricos**.
- Toma de **decisiones automatizadas** con efectos jurídicos.

> **Entregable:** `URCDP-05` (plantilla EIPD con ejemplo Banco: p. ej. tratamiento de datos de salud en garantías, videovigilancia en sucursales, Banco En Línea).

---

## 6.7. Privacidad por diseño y por defecto

Desde la concepción de cada producto/proceso que trate datos personales hay que incorporar medidas (Decreto 64/020 arts. 7-8):
- **Minimización** de datos (recoger solo lo necesario).
- **Disociación / seudonimización**.
- Mecanismos para el **ejercicio de derechos**.
- Documentación del **consentimiento**.
- Configuraciones por defecto **privadas**.

---

## 6.8. Autoexamen

1. Nombrá los 4 principios de la Ley 18.331 que consideres más relevantes para seguridad.
2. ¿Qué dice el art. 10 y por qué conecta con el MCU 5.0?
3. ¿Cuáles son los plazos de notificación de una vulneración (24 h / 72 h)?
4. ¿Cuándo es obligatorio designar DPD? ¿Al Banco le corresponde?
5. ¿Qué tratamientos exigen una EIPD?

---

**Siguiente:** `07-Organigrama.md`
