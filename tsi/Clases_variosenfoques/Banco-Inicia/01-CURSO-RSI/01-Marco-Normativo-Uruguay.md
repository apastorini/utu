# Módulo 1 · El marco normativo uruguayo que obliga al Banco

> Nivel del curso: 🟢 Descubrir
> Objetivo: entender **por qué** el Banco tiene que gestionar la seguridad de la información y **qué leyes, decretos y circulares** lo obligan.

---

## 1.1. ¿Por qué el Banco tiene obligaciones especiales?

El Banco Hipotecario del Uruguay ocupa una posición triple que pocas organizaciones tienen:

1. Es un **banco público del Estado uruguayo** → como organismo estatal debe cumplir los lineamientos de **Agesic** (el Marco de Ciberseguridad 5.0) y la normativa de gobierno electrónico (Decretos 92/014, 66/025 y Ley 20.212).
2. Es una **institución de intermediación financiera supervisada por el BCU** → debe cumplir la Recopilación de Normas de Regulación y Control del Sistema Financiero (RNRCSF), las circulares de riesgo operativo, resguardo de datos y tercerizaciones, y los estándares mínimos de gestión.
3. Trata **datos personales de miles de personas** (clientes, funcionarios, garantías, información crediticia) → es "responsable de tratamiento" ante la **URCDP** (Ley 18.331, Ley 19.670 y sus decretos).

Si el Banco falla en seguridad: multas del BCU, sanciones de la URCDP, perjuicio reputacional, pérdida de confianza y, sobre todo, **daño real a las personas** cuyos datos custodia.

### La "triple responsabilidad" en una tabla

| Organismo | Rol sobre el Banco | Qué exige | Normas clave |
|---|---|---|---|
| **Agesic** | Rectoría en ciberseguridad del Estado | Implementar el **Marco de Ciberseguridad 5.0** (72 requisitos, 6 funciones) | MCU 5.0; Decreto 92/014; Decreto 66/025; Ley 20.212 (arts. 78-79) |
| **BCU** | Supervisor financiero | Gestión del riesgo tecnológico/operativo, resguardo de datos, tercerizaciones, continuidad, sistema de pagos | RNRCSF (art. 492 y ss.); Circular 2227; Circulares 2419-2422; Circular 2280; Estándares Mínimos de Gestión |
| **URCDP** | Autoridad de protección de datos | Tratamiento lícito de datos personales, seguridad, derechos de los titulares, comunicación de vulneraciones | Ley 18.331; Decreto 414/009; Ley 19.670; Decreto 64/020 |

> **Consejo para el curso:** no te asustes con la cantidad de normas. Todas apuntan a lo mismo que vas a construir con el SGSI: **confidencialidad, integridad y disponibilidad (CID)** de la información. El SGSI es la herramienta que demuestra que cumplís todas a la vez.

---

## 1.2. La jerarquía normativa en Uruguay

Para leer cualquier norma correctamente:

```
Constitución de la República
        ↓
Leyes (aprobadas por el Parlamento)
        ↓
Decretos reglamentarios (Poder Ejecutivo)
        ↓
Circulares / Recopilaciones / Comunicaciones (organismos de control: BCU, URCDP)
        ↓
Estándares y guías (Agesic, recomendaciones URCDP)  ← no vinculantes, pero "esperables"
```

**Importante:** las guías (como el Marco de Ciberseguridad de Agesic o las guías de la URCDP) no son leyes, pero los supervisores las usan para **evaluar si tus medidas son adecuadas**. En la práctica, no cumplirlas = no poder demostrar cumplimiento.

---

## 1.3. Las normas que tenés que conocer sí o sí

### A) Protección de datos personales

| Norma | Qué establece |
|---|---|
| **Ley 18.331** (2008) | Ley de Protección de Datos Personales y Acción de Habeas Data. Define principios (licitud, calidad, consentimiento, finalidad, seguridad, reserva), derechos ARCO y el régimen general de tratamiento. |
| **Decreto 414/009** | Reglamentación de la Ley 18.331. Detalla las medidas de seguridad (arts. 7 y 8) y la inscripción de bases de datos. |
| **Ley 19.670** (2018) | Reforma: refuerza la responsabilidad proactiva, obliga a designar **Delegado de Protección de Datos (DPD)** en ciertos casos y crea el régimen de **comunicación de vulneraciones** (art. 38). |
| **Decreto 64/020** | Reglamenta la Ley 19.670: seguridad (arts. 3 y 4), plazos de notificación, evaluaciones de impacto (art. 6 lit. f), privacidad por diseño (arts. 7 y 8). |

### B) Ciberseguridad y Estado

| Norma | Qué establece |
|---|---|
| **Marco de Ciberseguridad 5.0 (Agesic, Versión 5.0 – Junio 2026)** | Conjunto de requisitos y buenas prácticas de ciberseguridad, alineado con NIST CSF 2.0. 72 requisitos en 6 funciones: Gobernar, Identificar, Proteger, Detectar, Responder, Recuperar. Es la **referencia** para demostrar seguridad en el sector público. |
| **Decreto 92/014** | Lineamientos sobre centros de datos seguros, correo electrónico y nombres de dominio del Estado. |
| **Decreto 66/025** | Disposiciones sobre seguridad de la información en organismos del Estado. |
| **Ley 20.212** (arts. 78-79) | Refuerza la obligación de medidas de seguridad en el ámbito digital (agenda de transformación digital). |

### C) Sistema financiero (BCU)

| Norma | Qué establece |
|---|---|
| **RNRCSF – art. 492** | Obligación de **resguardo de datos, software y documentación**, con copias que no puedan verse afectadas por un mismo evento, claves de desencriptación resguardadas y **pruebas anuales de recuperación e integridad**. |
| **Circular 2227** | Normas de **gestión del riesgo operativo**: políticas, gestión de incidentes, continuidad, terceros, seguridad de la información. |
| **Circulares 2419-2422** (2022) | Régimen de **tercerizaciones** y de resguardo de datos: evaluación de riesgos del tercero, contrato mínimo, autorización para el exterior, responsable del resguardo. |
| **Circular 2280 / RNSP** | Sistema de pagos: calidad del servicio, seguridad de la información, continuidad operativa, disponibilidad, monitoreo proactivo. El Banco tiene un Departamento de Sistema de Pagos. |
| **Estándares Mínimos de Gestión (EMG)** | Marco que el BCU espera en gobierno de la ciberseguridad, gestión de riesgos, funciones de seguridad de la información y de TI, auditoría y continuidad. |

---

## 1.4. Los "cinco actores" que te van a auditar o preguntar

1. **Agesic** → audita el cumplimiento del MCU 5.0 en organismos del Estado (con listas de verificación y niveles de madurez).
2. **BCU / Superintendencia de Servicios Financieros (SSF)** → supervisa al Banco como institución financiera; pide evidencia de gestión de riesgos y seguridad.
3. **URCDP** → controla el tratamiento de datos personales; recibe la comunicación de vulneraciones y evalúa las medidas de seguridad declaradas al inscribir bases de datos.
4. **CERTuy** (depende de Agesic) → centro nacional de respuesta a incidentes; se coordina ante vulneraciones de datos personales.
5. **Auditoría Interna y Auditoría Externa del Banco** → controlan la gestión, incluyendo al RSI.

---

## 1.5. Qué significa "cumplir" en la práctica

Cumplir no es tener un papel firmado. Es tener **evidencia** de que:

- hay alguien **responsable** (el RSI) y un **comité** que decide;
- hay **políticas** aprobadas por la máxima autoridad;
- se **conocen los activos** y **se evalúan los riesgos**;
- hay **controles implementados** y **evidencia** de que funcionan;
- se **detectan y responden** incidentes;
- se **recupera** la operación y se **mejora** continuamente.

Todo eso que listamos es, precisamente, un **SGSI**. Por eso el módulo siguiente te presenta el marco Agesic y luego el SGSI.

---

## 1.6. Autoexamen

1. ¿Cuáles son los tres organismos que regulan al Banco y qué controla cada uno?
2. ¿Qué es más fuerte: una ley o una guía de Agesic? ¿Por qué entonces cumplimos guías?
3. Nombrá al menos 3 normas de protección de datos y qué aporta cada una.
4. ¿Qué artículo de la RNRCSF obliga al resguardo de datos y qué exige?
5. ¿Por qué un banco público tiene más obligaciones que una empresa privada común?

---

**Siguiente:** `02-Marco-Ciberseguridad-50-Agesic.md`
