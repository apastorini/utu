# INFRA-00 · Índice y Mapa del Curso

> **Función del MCU 5.0:** Alinear la formación técnica con el Marco de Ciberseguridad de Uruguay (Agesic), en particular los dominios de protección (PR), detección (DE) y respuesta (RS) sobre la red y los activos de información.
> **ISO/IEC 27001:** El curso apoya los controles del Anexo A relacionados con gestión de activos (A.5.9), control de acceso (A.5.15/A.8), protección contra malware y vulnerabilidades (A.8.7/A.8.8), seguridad de redes (A.8.20/A.8.21) y gestión de incidentes (A.5.24).
> **BCU:** Sustenta la evidencia técnica requerida por el Reglamento de Normas de Control sobre Riesgo de TIC (RNRCSF art. 492), la Guía de Estándares Mínimos de Gestión (EMG) y las exigencias de la Estrategia de Monitoreo y Gestión del Riesgo de TIC.
> **URCDP:** Permite documentar medidas técnicas de seguridad exigidas por la Ley 18.331, su modificativa Ley 19.670 y el Decreto 64/020, en especial para datos personales que viajan por la red.
> **Decreto 66/025:** Permite al RSI prepararse para las obligaciones reglamentadas de la Dirección de Seguridad de la Información de Agesic (designación de RSI, notificación de incidentes al CERTuy, trazabilidad y evidencia de la red).
> **Nivel del curso:** 🟢 Descubrir · 🟡 Practicar · 🔴 Dominar

---

## 1. Presentación del curso

Bienvenido al curso **"Infraestructura de red y ciberseguridad desde cero"**. Este curso vive dentro de la carpeta `curso-infra` y forma parte del kit **Banco-Inicia** del Banco Hipotecario del Uruguay.

Este no es un curso de especialistas para especialistas. Es un curso pensado para que el **RSI** y el personal del Banco —aunque nunca hayan tocado un cable de red— terminen sabiendo **qué es una red, cómo se organiza, cómo se observa, cómo se protege y qué hay que pedir para cumplir la norma**.

La idea central es simple: si no entiendes cómo viaja la información dentro del banco, no puedes protegerla. Y si no puedes protegerla, no puedes cumplir con el marco de ciberseguridad de Agesic, las normas del BCU ni la ley uruguaya de protección de datos.

---

## 2. Para quién es este curso

| Perfil | Por qué le sirve |
|---|---|
| Responsables de Seguridad de la Información (RSI) | Necesitan entender la red para evaluar riesgos, responder incidentes, **pedir los controles correctos** y demostrar cumplimiento ante Agesic, BCU y URCDP. |
| Oficiales y personal administrativo | Manejan datos personales y deben saber cómo se protegen esos datos mientras viajan por la red. |
| Personal de TI | Refuerza conceptos que después usará para configurar dispositivos, completar plantillas y mantener evidencia. |
| Personas sin conocimientos previos | El curso empieza desde cero absoluto: no hace falta saber nada de redes para comenzar. |

### Qué vas a saber al terminar

- Qué es una red informática, qué tipos existen dentro del banco y cómo viajan los datos (IP, subredes, máscaras, VLAN, puertos, protocolos).
- Qué hace cada dispositivo de red: switch de capa 2, router de capa 3, firewall, punto de acceso, IDS/IPS, balanceador, VPN, SIEM.
- Cómo se protege la red: firewalls, DMZ, segmentación, hardening, firmware, antivirus/EDR, SAST/DAST, DLP.
- **Cómo observar la red**: monitoreo, SIEM, correlación de logs, umbrales y alarmas.
- **Qué preguntar y qué pedir** en cada área del banco para diagnosticar la infraestructura como RSI.
- Qué obliga el **Decreto 66/025** y cómo preparar la evidencia que espera Agesic y el CERTuy.
- Cómo completar las plantillas del kit relacionadas con la red: inventarios, análisis de riesgo, parches, logs y evidencias.

---

## 3. Los 15 módulos del curso

El curso tiene **15 módulos**, numerados de **INFRA-00** a **INFRA-14**. Esta es la tabla general:

| Módulo | Tema | Nivel | Plantillas/ documentos del kit relacionados |
|---|---|---|---|
| INFRA-00 | Índice y mapa del curso | 🟢 | Todos (es la puerta de entrada) |
| INFRA-01 | Fundamentos de redes (IP, subredes, máscaras, VLAN, NAT, DNS, DHCP, puertos, OSI) | 🟢 | ID-01, ID-02, ID-03, PR-04, GV-02, URCDP-01 |
| INFRA-02 | Dispositivos de red (switch L2, router L3, firewall, AP, IDS/IPS, balanceador, VPN, SIEM) | 🟢 | ID-01, PR-01, PR-04, PR-06, DE-01, DE-02, URCDP-01 |
| INFRA-03 | Firewalls, DMZ y segmentación | 🟡 | ID-01, PR-01, PR-03, DE-01, GV-02, URCDP-01 |
| INFRA-04 | Firmware y hardening de dispositivos | 🟡 | PR-06, ID-04, BCU-03, BCU-04, URCDP-01 |
| INFRA-05 | Antivirus, EDR y protección de extremos | 🟡 | PR-06, BCU-03, DE-02, URCDP-01 |
| INFRA-06 | SAST, DAST, DLP y fuga de datos | 🟡 | PR-07, DE-03, PR-03, URCDP-05 |
| INFRA-07 | Auditoría de la infraestructura actual (11 pasos) | 🔴 | ID-01, ID-03, ID-04, BCU-05, GV-06 |
| INFRA-08 | Evidencias a presentar | 🔴 | GV-01, GV-02, GV-03, BCU-01, BCU-05, URCDP-05 |
| INFRA-09 | Herramientas de simulación (nmap, Wireshark, GNS3, pfSense) | 🔴 | DE-03, DE-02, PR-06 |
| INFRA-10 | Laboratorio paso a paso | 🔴 | Todos los anteriores |
| INFRA-11 | Correspondencia normativa y cómo llenar los documentos | 🔴 | Todos los anteriores + MATRIZ-001 |
| INFRA-12 | Monitoreo, SIEM y alertas: cómo observar la red | 🟡→🔴 | DE-01, DE-02, BCU-04, RS-02 |
| INFRA-13 | Guía de relevamiento: qué preguntar y qué pedir como RSI | 🔴 | GV-06, ID-01, BCU-01, BCU-03, URCDP-01 |
| INFRA-14 | Decreto 66/025 y obligaciones normativas | 🟡→🔴 | GV-03, RS-02, ID-05, MATRIZ-001 |

> **Nota:** los módulos INFRA-12, INFRA-13 e INFRA-14 son los que convierten el curso de "entender la red" en "diagnosticar el banco y cumplir la norma" desde el rol de RSI.

---

## 4. Ruta de aprendizaje recomendada

Se recomienda este camino, que alterna teoría, práctica, observación y obligaciones:

1. **INFRA-00** (este módulo): el mapa del curso.
2. **INFRA-01**: fundamentos de redes (base de todo: IP, subredes, máscaras, VLAN).
3. **INFRA-02**: dispositivos de red (qué hay conectado a la red).
4. **INFRA-03**: firewalls, DMZ y segmentación (cómo se protege la red).
5. **INFRA-04** e **INFRA-05**: firmware, hardening, antivirus y EDR (estado de las defensas).
6. **INFRA-06**: SAST, DAST y DLP (seguridad de aplicaciones y datos).
7. **INFRA-07**: auditoría de la infraestructura actual (cómo diagnosticar el estado real).
8. **INFRA-12**: monitoreo, SIEM y alertas (cómo observar y tener alarmas).
9. **INFRA-08** e **INFRA-11**: evidencias y correspondencia normativa (cómo demostrar).
10. **INFRA-09** e **INFRA-10**: herramientas y laboratorio práctico (todo en acción).
11. **INFRA-13**: guía de relevamiento (qué preguntar y qué pedir en el terreno).
12. **INFRA-14**: Decreto 66/025 (obligaciones reglamentadas de Agesic).

### Pre-requisitos

- Para 🟢 **Descubrir**: ninguno.
- Para 🟡 **Practicar**: haber leído los módulos 🟢 del tema.
- Para 🔴 **Dominar**: haber leído y practicado los módulos anteriores, y tener acceso al laboratorio del módulo INFRA-10.

---

## 5. Cómo usar cada módulo

Cada módulo sigue el mismo patrón. Al leerlo, haz esto:

1. **Lee el módulo completo** de principio a fin, sin prisas. Las analogías sirven para fijar el concepto.
2. **Haz los ejercicios del módulo INFRA-10** cuando llegues al laboratorio. No hace falta una red real: se puede simular.
3. **Completa las plantillas relacionadas** que se indican al final de cada módulo. Por ejemplo, al terminar INFRA-02 debes poder registrar dispositivos en el inventario ID-01.

### Lista de verificación del lector

- ☐ Leí el módulo completo, incluidas las tablas y ejemplos.
- ☐ Hice el laboratorio del módulo INFRA-10 (o lo agendé).
- ☐ Completé las plantillas relacionadas indicadas en "Documentos relacionados".
- ☐ Marqué con fecha quién completó el módulo (para auditoría interna).

---

## 6. Los tres niveles de profundidad

Todo el kit usa tres niveles. En este curso:

- 🟢 **Descubrir** — Saber qué es, por qué importa y cómo se llama cada cosa. Es el nivel de todo el personal.
- 🟡 **Practicar** — Saber aplicarlo: calcular subredes, configurar un dispositivo de prueba, revisar un log. Es el nivel del personal de TI y de quien administra.
- 🔴 **Dominar** — Saber diseñarlo, auditarse, diagnosticarlo y responder ante incidentes. Es el nivel del RSI y de los equipos especializados.

| Nivel | Objetivo | Pregunta que se responde |
|---|---|---|
| 🟢 Descubrir | Reconocer y explicar | ¿Qué es esto y por qué me importa? |
| 🟡 Practicar | Aplicar y configurar | ¿Cómo lo hago en el día a día? |
| 🔴 Dominar | Diseñar, auditar y mejorar | ¿Cómo lo controlo y lo mejoro? |

---

## 7. Estructura de referencia del SGSI

El SGSI (Sistema de Gestión de Seguridad de la Información) del Banco se organiza en carpetas. Este curso vive en:

```
Banco-Inicia\
├── 00-PLANIFICACION\          ← Planificación del kit, calendario, roles
├── 01-CURSO-RSI\              ← Material didáctico general del kit
├── curso-infra\               ← ← ESTE CURSO (INFRA-00 a INFRA-14)
├── Curso-relevamiento\        ← Curso de relevamiento (RELEV-00 a RELEV-11)
└── 02-ENTREGABLES\
    ├── H-URCDP\               ← Cartera de protección de datos personales
    │   └── URCDP-01_Documento-Seguridad-Datos.md … URCDP-06_Delegado-Proteccion-Datos.md
    ├── G-BCU\                  ← Cartera de evidencia ante el BCU (BCU-01 a BCU-06)
    ├── A-GOBERNAR\ … F-RECUPERAR\  ← Funciones del MCU 5.0
    └── ...
```

- **00-PLANIFICACION** te dice cuándo y quién debe hacer qué.
- **01-CURSO-RSI** te da el contexto general del kit Banco-Inicia.
- **02-ENTREGABLES\G-BCU** es donde se guarda la evidencia que espera el BCU.
- **02-ENTREGABLES\H-URCDP** es donde se guarda la evidencia de protección de datos personales.
- **curso-infra** es la parte técnica: el curso de redes que sustenta esa evidencia.

---

## 8. Relación con las normas y organismos

### ¿Quiénes son y por qué importan para la red?

- **MCU 5.0 (Agesic):** el Marco de Ciberseguridad de Uruguay, versión 5.0 (Junio 2026), basado en NIST CSF 2.0. Sus 6 funciones (Gobernar, Identificar, Proteger, Detectar, Responder, Recuperar) y 72 requisitos son la hoja de ruta nacional que las instituciones públicas deben seguir.
- **ISO/IEC 27001:** la norma internacional de gestión de seguridad de la información. Define un SGSI auditable y una lista de controles (Anexo A, edición 2022) contra los que se miden las medidas técnicas de red.
- **BCU:** el Banco Central del Uruguay. Su normativa (RNRCSF art. 492 y la Guía de EMG) obliga a las instituciones financieras a gestionar el riesgo de las TIC y a tener seguridad en las redes donde circulan operaciones.
- **URCDP:** la Unidad Reguladora y de Control de Datos Personales. Aplica la Ley 18.331 y su modificativa Ley 19.670, reguladas por el Decreto 64/020. La red transporta datos personales de clientes y funcionarios; por eso la seguridad de la red es también protección de datos.
- **Decreto 66/025:** reglamenta los artículos 55 de la Ley 18.046, 119 de la Ley 18.172, 73 de la Ley 18.362, 149 de la Ley 18.719 y 78–84 de la Ley 20.212, sobre los cometidos de la **Dirección de Seguridad de la Información de Agesic**. Es el marco que obliga formalmente a designar RSI, adoptar el MCU y notificar incidentes al CERTuy. (Detalle en INFRA-14.)

### Por qué la red es el terreno común

Toda la información del banco —datos de clientes, operaciones, correos, archivos— viaja por la red. Proteger la red es proteger la información. Por eso este curso es el puente entre la parte legal (Decreto 66/025, URCDP, BCU) y la parte técnica (redes y dispositivos).

---

## 9. Cierre del módulo

En este módulo viste el mapa del curso: qué contiene, para quién es, en qué orden leerlo y cómo se conecta con las normas y el SGSI. El siguiente paso es el módulo **INFRA-01 · Fundamentos de Redes**, donde comenzarás desde el principio: qué es una red y cómo viaja la información.

---

**Documentos relacionados:** GV-01, GV-02, GV-03, ID-01, ID-02, ID-03, ID-04, ID-05, PR-01, PR-03, PR-04, PR-05, PR-06, PR-07, DE-01, DE-02, DE-03, RS-01, RS-02, RS-03, RC-01, RC-02, BCU-01, BCU-03, BCU-04, BCU-05, URCDP-01, URCDP-02, URCDP-04, URCDP-05, MATRIZ-001
