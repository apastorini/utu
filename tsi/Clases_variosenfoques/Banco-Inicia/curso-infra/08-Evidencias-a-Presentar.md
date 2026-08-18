# INFRA-08 · Evidencias a Presentar

> **Función del MCU 5.0:** Demostrar con registros verificables que las funciones del marco se implementan: identificación (ID.AM), protección (PR), detección (DE) y respuesta (RS), de modo que el Banco pueda demostrar su posición de ciberseguridad ante Agesic y el BCU.
> **ISO/IEC 27001:** Sustenta el requisito de evidencia documentada del SGSI (cláusula 7.5), la retención de registros y la auditoría interna (A.9.3), demostrando que los controles existen y funcionan.
> **BCU:** Permite presentar ante el supervisor la evidencia que acompaña el informe del RSI (GV-06) y las auditorías (BCU-05), con registros fechados y trazables del riesgo tecnológico.
> **URCDP:** Acredita ante la Unidad Reguladora y de Control de Datos Personales las medidas de seguridad declaradas en el Documento de Seguridad (URCDP-01) y las notificaciones de vulneraciones (URCDP-02, Ley 19.670 art. 38).
> **Nivel del curso:** 🟢 Descubrir · 🟡 Practicar · 🔴 Dominar

---

## 1. Qué es una evidencia

Una **evidencia** es un registro verificable —una captura, un informe, una configuración, un log o un acta— que demuestra que un control **existe y funciona**.

Sin evidencia, un control declarado es una promesa. Con evidencia, es un hecho comprobable.

> **Analogía:** es como el ticket de compra: no alcanza con decir que pagaste; el ticket lo prueba. El auditor es el que pide el ticket de cada control.

### Por qué importa ante BCU, Agesic (MCU 5.0), URCDP y las auditorías

| ¿Quién pide? | ¿Qué mira? | ¿Con qué evidencia se responde? |
|---|---|---|
| **BCU** (supervisor) | Riesgo tecnológico y controles del RNRCSF | Informes del RSI (GV-06), auditorías (BCU-05), reportes técnicos |
| **Agesic / MCU 5.0** | Implementación del marco nacional | Mapeo de funciones a evidencias (MATRIZ-001) |
| **URCDP** | Medidas del Documento de Seguridad | URCDP-01 actualizado, registros de controles, notificaciones |
| **Auditoría interna** | Que lo documentado sea real | Evidencia técnica de cada control |

---

## 2. Principios de la evidencia

Toda evidencia que se presente debe cumplir estos seis principios:

| Principio | Significa que... | Pregunta que responde |
|---|---|---|
| **Íntegra** | No fue manipulada ni modificada | ¿Sigue siendo el registro original? |
| **Fechada** | Tiene fecha (y si aplica, hora) | ¿Cuándo se tomó? |
| **Trazable** | Se puede conectar al sistema o documento de origen | ¿De dónde salió? |
| **Legible** | Se entiende sin necesidad de explicaciones orales | ¿Qué muestra exactamente? |
| **Respaldada** | Tiene hash o firma digital cuando es posible | ¿Cómo sé que no cambió? |
| **Conservada** | Se guarda con una retención definida | ¿Cuánto tiempo debo guardarla? |

> **Regla de oro:** si una evidencia no tiene fecha o no se entiende qué muestra, **no sirve**. Un auditor la descartará por más que el control exista.

---

## 3. Tabla maestra: evidencia → control → norma → documento del kit

Esta tabla conecta cada evidencia con el control que demuestra, la norma que lo exige y el documento del kit donde se registra.

| Evidencia | Control que demuestra | Norma / referencia | Documento del kit |
|---|---|---|---|
| Inventario y mapa de red | Activos identificados y documentados | MCU ID.AM | ID-01, GV-02 |
| Diagrama de red con zonas y DMZ | Segmentación y aislamiento de la DMZ | MCU ID.AM / PR.AA | GV-02, INFRA-03 |
| Export de reglas de firewall + acta de revisión | Firewall de mínimo privilegio | MCU PR.PS | INFRA-03, GV-03 |
| Baseline de hardening completado | Configuración segura de dispositivos | CIS, MCU PR.PS | INFRA-04 |
| Reporte de parches y firmware | Gestión de vulnerabilidades | MCU PR.PS | PR-06 |
| Consola antivirus/EDR con cobertura y alertas | Protección de extremos | MCU PR.PS | INFRA-05 |
| Reportes SAST/DAST + plan de remediación | Seguridad de aplicaciones | MCU PR.PS | INFRA-06, PR-07 |
| Reporte DLP con eventos bloqueados | Prevención de fuga de datos | MCU PR.DS | INFRA-06, PR-03 |
| Logs y SIEM con cobertura y retención | Monitoreo y detección | MCU DE.CM | DE-01, DE-02 |
| Registros de acceso administrativo y 2FA | Control de acceso | MCU PR.AA, ISO A.9 | PR-01 |
| Respaldos y prueba de restauración | Continuidad y recuperación | MCU PR.IR / RC.RP | PR-05, RC-02 |
| Planillas de riesgos y plan de tratamiento | Gestión de riesgos | MCU GV.RM, ISO A.5 | ID-02, ID-03, ID-04 |
| Documento de Seguridad actualizado | Medidas para datos personales | Ley 18.331, Decreto 64/020 | URCDP-01 |
| Registro de notificaciones de vulneraciones | Transparencia ante incidentes | Ley 19.670, art. 38 | URCDP-02 |
| Reportes de concientización y phishing | Cultura de seguridad | MCU PR.AT | PR-02 |
| Informe de auditoría y lecciones aprendidas | Mejora continua | MCU ID.IM / ID.IM | BCU-05, RC-04 |

---

## 4. Cómo armar el "expediente de evidencia"

La evidencia no se guarda en la carpeta del correo ni en el escritorio: se organiza en un **expediente** que un auditor pueda recorrer sin ayuda.

### Estructura de carpetas

Usa la estructura definida en el documento **00-Estructura-Carpetas-SGSI** del kit. Un ejemplo:

```
Evidencias/
├── 01-Identificacion/          (ID-01, ID-02, ID-03, ID-04)
├── 02-Proteccion/              (PR-01 a PR-07)
├── 03-Deteccion/               (DE-01, DE-02, DE-03)
├── 04-Respaldo-y-Recuperacion/ (RC-01, RC-02, RC-04)
├── 05-Gobierno/                (GV-01 a GV-06, BCU-05)
└── 06-URCDP/                   (URCDP-01, URCDP-02, URCDP-05)
```

### Convención de nombres

Cada archivo de evidencia se nombra con **código + fecha**, para que se ordene solo y no haya versiones confusas:

`PR-06_Reporte-Parches_2026-08-05.pdf`

| Parte | Qué poner | Ejemplo |
|---|---|---|
| Código | El documento del kit al que responde | PR-06 |
| Descripción | Qué es la evidencia | Reporte-Parches |
| Fecha | Año-mes-día | 2026-08-05 |

### Índice de evidencias

Se mantiene una tabla (una fila por evidencia) que permite encontrar y auditar todo:

| Código | Evidencia | Fecha | Versión | Ruta | Vence |
|---|---|---|---|---|---|
| PR-06 | Reporte de parches de la red | 2026-08-05 | 1.2 | `02-Proteccion/PR-06_...` | 2026-11-05 |

### Dónde guardarlas y frecuencia de renovación

- Se guardan en un **repositorio protegido** (acceso restringido, respaldo y control de versiones).
- Cada evidencia tiene una **frecuencia de renovación** definida (mensual, trimestral o anual según el control).
- Se conservan **al menos el período de retención** que fija el SGSI (para datos personales y normativa BCU, suele ser de varios años).

---

## 5. Cómo presentarlas ante un auditor o supervisor

Cuando llega el auditor, el expediente se presenta en este orden:

1. **Resumen ejecutivo**: una página que explica qué controles se auditaron y la conclusión general.
2. **Tabla de correspondencia con normas** (MATRIZ-001): qué norma exige qué y dónde está la evidencia.
3. **Evidencias fechadas**: las capturas, reportes y actas, ordenadas por documento del kit.
4. **Referencias a documentos aprobados**: la política, el procedimiento y el responsable de cada control.

> **Analogía:** es como entregar la carpeta de un paciente al médico: primero el resumen, después los análisis, y cada análisis con su fecha y resultado.

### Buenas prácticas al presentar

- ☐ Cada evidencia tiene **fecha y contexto** (qué sistema, qué alcance, qué herramienta).
- ☐ Las capturas incluyen **fecha y hora visible** y el nombre del sistema.
- ☐ Se citan los **documentos aprobados** (política, procedimiento) de cada control.
- ☐ Se entrega una **tabla índice** al inicio, para que el auditor se oriente.
- ☐ El expediente tiene **versión y responsable** de su mantenimiento.

### Ejemplo de resumen ejecutivo

> "Se verificaron los controles de protección de extremos e infraestructura de red del Banco al 05/08/2026. La evidencia adjunta (INFRA-05, INFRA-07, PR-06) demuestra 100 % de cobertura de antivirus/EDR, reglas de firewall revisadas en el trimestre y parches críticos aplicados dentro de plazo. No se detectaron hallazgos críticos; los tres hallazgos medios cuentan con plan de acción con vencimiento al 15/09/2026."

### Ejemplo de ficha de evidencia

| Campo | Contenido |
|---|---|
| **Documento del kit** | PR-06 |
| **Título** | Reporte de parches de infraestructura |
| **Herramienta / sistema** | Consola de gestión de parches (WSUS) |
| **Alcance** | 42 servidores y 18 dispositivos de red |
| **Fecha de captura** | 2026-08-05 14:30 (UTC-3) |
| **Estado** | Vigente, versión 1.2 |
| **Respaldos** | Hash SHA-256 almacenado en el repositorio |
| **Vencimiento de la próxima renovación** | 2026-09-05 |

---

## 6. Errores comunes

- ✗ **Evidencias sin fecha:** un auditor no puede saber si el control sigue vigente.
- ✗ **Capturas sin contexto:** una imagen recortada sin nombre de sistema ni alcance no prueba nada.
- ✗ **No actualizar:** presentar la evidencia del año pasado como si fuera actual.
- ✗ **Evidencia en correos sueltos:** si no está en el expediente, no existe para la auditoría.
- ✗ **No respaldar la evidencia:** perder el expediente por no tener copia protegida.
- ✗ **Guardar datos sensibles sin protegerlos:** la evidencia misma puede contener datos personales y debe tratarse como confidencial.

---

## 7. Relación con el kit

| Documento | Cómo se conecta |
|---|---|
| **MATRIZ-001** | Tabla maestro que mapea norma → control → evidencia |
| **GV-06 / BCU-05** | Informes del RSI y de auditoría: destinan final de la evidencia |
| **URCDP-01 / URCDP-02** | Documento de Seguridad y notificaciones: evidencia de medidas y de incidentes |
| **00-Estructura-Carpetas-SGSI** | Define dónde se guarda el expediente |
| **ID-01 a ID-04** | Activos y riesgos: origen de muchas evidencias |
| **PR-01 a PR-07** | Controles que generan las evidencias técnicas |

> **Checklist del lector**
> - ☐ Puedo definir qué es una evidencia y los seis principios.
> - ☐ Conozco la tabla evidencia → control → norma → documento del kit.
> - ☐ Sé armar el expediente con estructura, nombres y índice.
> - ☐ Sé cómo presentarlo ante un auditor y qué errores evitar.

---

**Documentos relacionados:** GV-02, GV-06, ID-01, ID-02, ID-03, ID-04, PR-01, PR-02, PR-05, PR-06, PR-07, DE-01, DE-02, RC-02, RC-04, BCU-05, URCDP-01, URCDP-02, MATRIZ-001, EV-01, EV-02, EV-03, EV-04.
