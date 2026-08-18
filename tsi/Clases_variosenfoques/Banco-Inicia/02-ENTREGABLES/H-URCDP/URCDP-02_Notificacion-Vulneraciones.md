# URCDP-02 · Procedimiento de Notificación de Vulneraciones de Seguridad del Banco
> **Función del MCU 5.0:** Responder (RS.CO — Notificación y comunicación) · Recuperar (RC.CO — Comunicación de la recuperación)
> **ISO/IEC 27001:** A.5.24 (Gestión de incidentes) · A.5.25 (Evaluación y decisiones de incidentes de seguridad)
> **BCU:** Circular 2227 (gestión de incidentes) · Circular 2280 (pagos) · RNRCSF art. 492
> **URCDP:** **Ley 19.670 art. 38** (comunicación de vulneraciones) · **Decreto 64/020 arts. 3-4** (condiciones y plazos) · Ley 18.331 art. 10
> **Nivel del curso:** 🔴 Dominar

## 1. Qué es y por qué existe
La notificación de vulneraciones de seguridad de datos personales es la obligación con **plazos más estrictos** de toda la normativa URCDP. Cuando una vulneración pone en riesgo datos personales, el Banco debe actuar en horas, no en semanas. Este procedimiento define qué es una vulneración, cómo evaluar el riesgo para los titulares, **cuándo** notificar a la URCDP y a los titulares, **qué** notificar y **quién** lo hace.
La base legal es el **art. 38 de la Ley 19.670** y el **Decreto 64/020 (arts. 3-4)**: el responsable o encargado debe comunicar a la URCDP las vulneraciones de seguridad que afecten datos personales, evaluar el riesgo, e informar a los titulares. El **art. 10 de la Ley 18.331** impone además la obligación de evitar la adulteración, pérdida o acceso no autorizado, por lo que la gestión de vulneraciones es también una obligación de seguridad continua.
El procedimiento se integra con el esquema de incidentes de seguridad (RS-01/RS-02): todo incidente que afecte datos personales activa, además del tratamiento técnico, la **evaluación de notificación**. La coordinación con la URCDP y con **CERTuy** (que coordina el curso de acción según el art. 38) se realiza a través del **DPD**, en coordinación con el **RSI**. El incumplimiento de los plazos es la infracción que más frecuentemente sanciona la URCDP.
## 2. Marco de referencia
| **Marco** | **Referencia** | **Qué exige** |
|---|---|---|
| **MCU 5.0 (Agesic)** | RS.CO · RC.CO | Comunicar incidentes internamente y a terceros con procedimientos definidos |
| **ISO/IEC 27001** | A.5.24 · A.5.25 | Gestión de incidentes y evaluación de decisiones de notificación |
| **BCU** | Circular 2227 · Circular 2280 | Gestión de incidentes y comunicación al supervisor cuando corresponda |
| **URCDP** | **Ley 19.670 art. 38** · **Decreto 64/020 arts. 3-4** · Ley 18.331 art. 10 | Iniciar procedimientos en **24 h**; comunicar a la URCDP en **máx. 72 h**; comunicar a los titulares; coordinar con CERTuy |

## 3. Cómo completar esta plantilla (guía de llenado)
1. **Completá el encabezado** con los datos del documento.
2. **Definí qué se considera vulneración** para el Banco y qué incidentes activan la evaluación de notificación.
3. **Diseñá la evaluación de riesgo para los titulares** (confidencialidad, integridad, disponibilidad; sensibilidad de los datos; volumen; mitigaciones).
4. **Fijá los plazos como hitos medibles**: 24 h desde la constatación, 72 h máx. para la comunicación a la URCDP, comunicación inmediata a los titulares.
5. **Redactá el contenido mínimo** de la notificación (art. 38 / Decreto 64/020) en los formularios anexos.
6. **Asigná responsabilidades**: DPD lidera, RSI aporta el análisis técnico, Comunicaciones redacta la comunicación a titulares.
7. **Establecé el registro de vulneraciones** y la coordinación con RS-01 (incidentes) y CERTuy.
8. **Probá el procedimiento** con ejercicios de simulación al menos una vez al año.
**A quién consultar en el Banco:** DPD (lidera la notificación y el vínculo con la URCDP); RSI (análisis técnico del incidente y de la evidencia); División TI (contención y preservación); División Auditoría Interna (revisión del proceso); Comunicaciones Institucionales (comunicado a titulares); División Servicios Jurídicos Notariales (asesoramiento).
## 4. Plantilla del documento

### ENCABEZADO
| **Campo** | **Valor** |
|---|---|
| **Código** | URCDP-02 |
| **Título** | Procedimiento de Notificación de Vulneraciones de Seguridad |
| **Versión** | 1.0 |
| **Estado** | [Borrador / En revisión / Aprobado] |
| **Fecha de aprobación** | [COMPLETAR] |
| **Elaborado por** | DPD |
| **Revisado por** | RSI / Comité de Seguridad de la Información |
| **Aprobado por** | Gerencia General |
| **Clasificación** | Uso interno — restringido |
| **Próxima revisión** | [Fecha, máx. 1 año] |

### 1. Objetivo
Establecer el procedimiento para detectar, evaluar, notificar y registrar las vulneraciones de seguridad que afecten datos personales, cumpliendo los plazos del art. 38 de la Ley 19.670 y del Decreto 64/020, y coordinar con la URCDP, CERTuy y los titulares afectados.
### 2. Alcance
Aplica a [COMPLETAR: toda vulneración de seguridad que afecte datos personales tratados por el Banco o por sus encargados, cualquiera sea el medio (digital o físico) y la unidad afectada]. Incluye vulneraciones de confidencialidad, integridad y disponibilidad.
### 3. Qué es una vulneración de datos personales
Es toda infracción de la seguridad que provoque, de forma accidental o ilícita, la **destrucción, pérdida, alteración, comunicación o acceso no autorizado** de datos personales. Ejemplos para el Banco: filtración de datos de clientes por correo erróneo, robo de equipos con datos, acceso no autorizado a la base de créditos, ataque de ransomware con cifrado de bases, pérdida de soportes físicos de legajos.
### 4. Evaluación de riesgo para los titulares
Ante una vulneración, se evalúa si existe **riesgo para los derechos y libertades de los titulares**, considerando: tipo de datos (sensibles o no), naturaleza y gravedad, volumen y categoría de titulares afectados, facilidad de identificación de las personas, duración de la exposición y medidas aplicadas para reducir el impacto. Esta evaluación se registra por escrito y la realiza el DPD con el RSI.
### 5. Plazos y acciones
| **Acción** | **Plazo** | **Responsable** |
|---|---|---|
| Detectar y **constatar** la vulneración | Inmediato | RSI / División TI |
| Iniciar los **procedimientos** para minimizar el impacto | **Dentro de las 24 h** desde la constatación | RSI + DPD |
| Evaluar el riesgo para los titulares | Inmediato | DPD |
| **Comunicar a la URCDP** | **Máximo 72 h** desde que se conoce | DPD |
| **Comunicar a los titulares** | Inmediatamente y pormenorizadamente | DPD + Comunicaciones |
| Coordinar con **CERTuy** | Conforme lo disponga la URCDP | DPD |

### 6. Contenido mínimo de la notificación a la URCDP
a) Fecha cierta o estimada de la vulneración y su **naturaleza**.
b) **Datos personales afectados** y categoría de titulares involucrados.
c) **Impactos** potenciales sobre los titulares.
d) **Medidas adoptadas o a adoptar** para mitigar la vulneración.
e) Información de contacto del DPD del Banco.
### 7. Comunicación a los titulares
Cuando la vulneración implique un alto riesgo para los titulares, se les comunica de forma individual, en lenguaje claro y pormenorizado: qué ocurrió, qué datos se vieron afectados, qué consecuencias puede tener, qué medidas tomó el Banco y qué puede hacer el titular para protegerse. Si la comunicación individual no fuera posible [COMPLETAR: se utiliza comunicación pública por los medios del Banco].
### 8. Coordinación con CERTuy
En los casos que la URCDP disponga, se coordina el curso de acción con CERTuy, especialmente en vulneraciones de gran escala o con impacto sistémico.
### 9. Registro de vulneraciones
El DPD mantiene un **registro de vulneraciones** con: fecha, descripción, categorías de datos afectadas, número de titulares, evaluación de riesgo, decisiones de notificación (a URCDP, a titulares, a BCU) con sus fechas, medidas adoptadas y estado. El registro se conserva y se revisa periódicamente.
### 10. Coordinación con incidentes de seguridad (RS-01/RS-02)
Todo incidente se gestiona primero conforme al esquema de incidentes (contención, preservación de evidencia, comunicación interna). Si el incidente afecta datos personales, se activa **simultáneamente** este procedimiento. La notificación al BCU (cuando corresponda) no sustituye la notificación a la URCDP.
### 11. Simulacros y mejora
El procedimiento se ejercita con simulacros al menos una vez al año. Las vulneraciones reales se analizan para extraer lecciones aprendidas y mejorar los controles.
### Control de cambios
| **Versión** | **Fecha** | **Cambio** | **Elaboró** | **Aprobó** |
|---|---|---|---|---|
| 0.1 | [COMPLETAR] | Versión inicial (borrador) | DPD | — |
| 1.0 | [COMPLETAR] | Aprobación de Gerencia General | DPD | Gerencia General |

## 5. Ejemplo aplicado al Banco (modelo de referencia)
Ejemplo ilustrativo de cómo quedaría completado. Adaptá a la realidad institucional del Banco.
**Caso de ejemplo (ejemplo Banco):** el día 03/05/2026 la División TI detectó el acceso no autorizado a una base de datos de la sucursal virtual con datos de contacto de [N] clientes. El RSI constató el incidente a las 10:00 y lo comunicó al DPD. El DPD y el RSI iniciaron las medidas de contención (revocación de credenciales, revisión de accesos) **dentro de las 24 h**. La evaluación determinó que los datos expuestos (nombre, correo y cédula, sin datos financieros) implicaban un riesgo moderado para los titulares.
**Notificación (ejemplo):** el DPD comunicó la vulneración a la URCDP a través del sistema de gestión el 05/05/2026 (dentro de las 72 h desde el conocimiento), indicando fecha del incidente, datos afectados, titulares involucrados, impacto potencial y medidas adoptadas. Se comunicó a los titulares por correo electrónico, pormenorizadamente, con recomendaciones de seguridad. La URCDP coordinó el curso de acción con CERTuy. El caso se registró en el registro de vulneraciones y dio lugar a la corrección del control de accesos.
**Simulacro (ejemplo):** en [mes] se ejecutó un simulacro de vulneración de datos personales (robo de un equipo portátil cifrado) para validar los plazos de 24 h y 72 h y la calidad del contenido de la notificación. Se identificó una demora en la recopilación de la información técnica, que se corrigió definiendo plantillas precargadas y un canal directo DPD-RSI.

**Documentos relacionados:** RS-01 (Incidentes), RS-02 (Notificación de incidentes), URCDP-01 (Documento de Seguridad), URCDP-03 (ARCO), URCDP-06 (DPD), BCU-06 (Continuidad), GV-01 (Política).
