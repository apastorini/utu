# Módulo 2 · El Marco de Ciberseguridad 5.0 de Agesic (MCU 5.0)

> Nivel del curso: 🟢 Descubrir → 🟡 Practicar
> Objetivo: dominar la **herramienta central** que el Banco debe usar para demostrar seguridad ante Agesic y como referencia ante BCU y URCDP.

---

## 2.1. ¿Qué es el MCU 5.0?

El **Marco de Ciberseguridad del Uruguay versión 5.0** (publicado por Agesic, Versión 5.0 – Junio 2026) es un conjunto de **requisitos normativos y buenas prácticas** que toda organización (pública o privada) puede adoptar para gestionar sus riesgos de ciberseguridad.

Está alineado con el **NIST Cybersecurity Framework 2.0** (Estados Unidos) y con la normativa nacional de seguridad de la información y protección de datos personales.

Datos clave:

- **72 requisitos**, organizados en **6 funciones** del ciclo de vida de la ciberseguridad.
- Incluye un **modelo de madurez** (para saber dónde estás y a dónde vas).
- Define **3 perfiles** para priorizar: **Básico (B)**, **Estándar (E)** y **Avanzado (A)**.
- Tiene **apartados especiales** para sectores críticos: **salud** y **sistema de pagos** (el Banco opera pagos → le aplica).
- Es **compatible** con la implementación de un **SGSI** (ISO/IEC 27001) y con la normativa de URCDP. No son cosas en competencia: se refuerzan.

> **Regla de oro:** el MCU 5.0 te dice **qué** gestionar; el SGSI te da el **cómo** (proceso, documentación, mejora continua). Se implementan juntos.

---

## 2.2. Las 6 funciones (el "ciclo de vida" de la ciberseguridad)

El Marco ordena las actividades de ciberseguridad como un **ciclo continuo**:

```
         ┌────────── GV  (Gobernar)
         │                 ↓
         │          ID  (Identificar)
         │                 ↓
         │          PR  (Proteger)
         │                 ↓
         │          DE  (Detectar)
         │                 ↓
         │          RS  (Responder)
         │                 ↓
         └────── RC  (Recuperar)  → vuelve a Gobernar
```

| Función | Qué busca | Ejemplos de categorías |
|---|---|---|
| **GV · Gobernar** | Que la dirección establezca política, roles y estrategia de riesgo | Contexto organizativo (GV.OC), estrategia de gestión de riesgos (GV.RM), roles y responsabilidades (GV.RR), políticas (GV.PO), supervisión (GV.OV), cadena de suministro (GV.SC) |
| **ID · Identificar** | Conocer los activos, el negocio y los riesgos | Gestión de activos (ID.AM), evaluación de riesgos (ID.RA), mejora (ID.IM) |
| **PR · Proteger** | Implantar las defensas | Identidades y control de acceso (PR.AA), concientización (PR.AT), seguridad de datos (PR.DS), seguridad de plataformas (PR.PS), resiliencia de la infraestructura (PR.IR) |
| **DE · Detectar** | Encontrar anomalías e incidentes temprano | Monitoreo continuo (DE.CM), análisis de eventos adversos (DE.AE) |
| **RS · Responder** | Reaccionar y mitigar | Gestión de incidentes (RS.MA), análisis de incidentes (RS.AN), notificación y comunicación (RS.CO), mitigación de incidentes (RS.MI) |
| **RC · Recuperar** | Restaurar la operación | Ejecución del plan de recuperación (RC.RP), comunicación de la recuperación (RC.CO) |

Cada función se divide en **categorías** y cada categoría en **subcategorías** (resultados concretos). A cada subcategoría el Marco le asigna **requisitos**, **prioridad** según el perfil y **referencias** a normas (ISO 27001, NIST 800-53, etc.).

---

## 2.3. Perfiles y modelo de madurez

### Perfiles (para priorizar)

| Perfil | Riesgo percibido | Tolerancia a la indisponibilidad |
|---|---|---|
| **Básico** | Bajo | Recuperación "al mejor esfuerzo" |
| **Estándar** | Moderado, alta dependencia de TIC | No más de 48 h corridas |
| **Avanzado** | Alto (servicios críticos) | No más de 24 h corridas |

El Banco, por ser banco y operar sistema de pagos, debe aspirar a **perfil Avanzado**, aunque arranque priorizando los requisitos de prioridad alta del perfil que hoy tenga.

### Modelo de madurez

Permite puntuar cada subcategoría (ej. niveles 1 a 5, de "no implementado" a "optimizado"). El flujo típico:

1. Hacé un **diagnóstico** (estado actual) con la lista de verificación de Agesic.
2. Definí el **perfil objetivo**.
3. Compará y construí el **plan de acción**.
4. Re-evaluá cada año (mejora continua).

> **Entregable asociado:** `ID-05_Perfil-Ciberseguridad.md` (estado actual / objetivo).

---

## 2.4. Guías oficiales de apoyo (usalas en el proyecto)

Agesic publica material de apoyo que el Banco debe usar directamente:

- **Marco de Ciberseguridad 5.0** (el documento normativo).
- **Guía de implementación del MCU 5.0** → cómo implementar y evidenciar cada requisito.
- **Guía de auditoría del MCU 5.0** + **Lista de Verificación** (archivo editable) → así audita Agesic.
- **Guía para la implementación de un SGSI** + **planilla editable "Implantación SGSI – Inventario de activos y Evaluación de riesgos"** (.xlsx).
- **Guía sobre indicadores para un SGSI** → métricas.
- **Guía para la gestión de vulnerabilidades** → proceso de vulnerabilidades.
- **Guía de interpretación del Decreto 92/014** → centros de datos seguros, correo, dominios.
- **Matriz RACI** de Agesic → quién decide/informa en cada actividad.

> Todas están disponibles en el sitio de Agesic (ver enlaces en el README). Son el material de lectura del RSI.

---

## 2.5. MCU 5.0 ↔ SGSI: cómo se combinan en la práctica

| Pregunta | MCU 5.0 | SGSI (ISO 27001) |
|---|---|---|
| ¿Qué gestionar? | 72 requisitos por función | 93 controles en 4 dominios |
| ¿Cómo se implementa? | Guías de implementación + perfiles | Cláusulas 4-10 + Anexo A |
| ¿Cómo se mide? | Modelo de madurez + lista de verificación | Auditorías internas + revisión por la dirección |
| ¿Cómo se demuestra? | Autoevaluación y auditorías de Agesic | Certificación (opcional) o auditorías |

En este kit cada **entregable** de `02-ENTREGABLES/` declara qué requisito del MCU 5.0, qué control ISO 27001 y qué norma BCU/URCDP cubre (ver `00-Matriz-Correspondencia-Normativa.md`).

---

## 2.6. Autoexamen

1. ¿Cuántos requisitos tiene el MCU 5.0 y en cuántas funciones se organizan?
2. ¿Cuáles son las 6 funciones y qué pregunta responde cada una?
3. ¿Qué perfil debe aspirar el Banco y por qué?
4. ¿Qué es el modelo de madurez y para qué sirve?
5. ¿Cómo se relaciona el MCU 5.0 con un SGSI ISO 27001?

---

**Siguiente:** `03-SGSI-ISO-27001.md`
