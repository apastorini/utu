# GV-05 · Gestión de Riesgos de la Cadena de Suministro del Banco

> ⚠️ **Alerta:** este documento menciona **nombres propios del organigrama del Banco** (personas y cargos, abril 2026). Antes de usar el documento, verificá la vigencia de esos nombres contra el organigrama actual.
> **Función del MCU 5.0:** Gobernar (GV.SC — Cadena de suministro)
> **ISO/IEC 27001:** A.5.19 (Seguridad en las relaciones con proveedores) · A.5.20 (Acuerdos con proveedores) · A.5.21 (Gestión de la seguridad de TI en la cadena de suministro) · A.5.22 (Monitoreo y revisión de servicios de proveedores)
> **BCU:** Circulares 2419-2422 (tercerización y subcontratación) · Comunicación 2022/254 (tercerización de actividades en el exterior) · RNRCSF art. 492
> **URCDP:** Ley 18.331 art. 12 y Decreto 64/020 (encargados de tratamiento, cláusulas y transferencias)
> **Nivel del curso:** 🟡 Practicar · 🔴 Dominar

## 1. Qué es y por qué existe
Este documento gestiona los **riesgos de seguridad que provienen de terceros**: proveedores tecnológicos, procesadoras de pagos, centros de datos, nube, custodias, call centers y subcontratistas. El banco delega servicios, pero **no delega responsabilidad**: si un proveedor sufre un incidente con datos de clientes del Banco, la URCDP y el BCU le exigirán al Banco, no al proveedor. La ISO/IEC 27001 lo regula en los controles **A.5.19 a A.5.22** y el MCU 5.0 en la categoría **GV.SC**.
Se usa en **cada alta, renovación o cambio significativo de un contrato con terceros**, y de forma permanente mediante un registro de terceros críticos y evaluaciones periódicas. El BCU exige reglas específicas en las Circulares **2419 a 2422** (tercerización de funciones esenciales y subcontratación) y la **Comunicación 2022/254** para la **tercerización en el exterior**; la URCDP exige, por el **Decreto 64/020**, que los encargados de tratamiento ofrezcan garantías suficientes y que los contratos fijen las cláusulas mínimas de protección de datos.
Sin esta gestión, el SGSI tiene un agujero: muchos incidentes graves de los bancos comienzan en un proveedor con accesos al entorno productivo o a bases de datos de clientes.

## 2. Marco de referencia
| **Requisito** | **MCU 5.0** | **ISO/IEC 27001** | **BCU** | **URCDP** |
|---|---|---|---|---|
| Seguridad en relaciones con proveedores | GV.SC | **A.5.19** | Circ. 2419-2422 | Decreto 64/020 (garantías del encargado) |
| Acuerdos contractuales de seguridad | GV.SC | **A.5.20** | Circ. 2419-2422 | D.64/020 (cláusulas mínimas) |
| Cadena de suministro de TI | GV.SC | **A.5.21** | Circ. 2419-2422 (subcontratación) | D.64/020 (encadenamiento de responsables) |
| Monitoreo y revisión de proveedores | GV.SC | **A.5.22** | Circ. 2419-2422 | D.64/020 (verificación de medidas) |
| Tercerización en el exterior | GV.SC | A.5.19 (riesgo país) | **Com. 2022/254**; autorización previa del BCU | D.64/020 arts. 29-31 (transferencias internacionales) |
| Datos personales en encargados | PR.DS | A.5.20 | RNRCSF art. 492 (resguardo de datos) | Ley 18.331 art. 12; D.64/020 |

## 3. Cómo completar esta plantilla (guía de llenado)
1. **Armá el inventario de terceros críticos** con el Departamento Compras y Contrataciones: procesadoras de pagos, proveedor de nube/datacenter, desarrolladores externos, call centers, custodias de archivo y consultorías con acceso a información.
2. **Clasificá la criticidad** (alta/media/baja) según el acceso a datos, la criticidad del proceso soportado y la dependencia del Banco, consultando al Jefe de Departamento Sistema de Pagos (Cr. Guillermo Correa) y al Jefe de Departamento Producción (Ing. Daniel Herrera).
3. **Evaluá el riesgo del proveedor** en tres ejes: **técnico** (seguridad y controles), **legal** (contratos, datos personales, plazos de notificación) y **de negocio** (solvencia, dependencia, capacidad de respuesta). Usá cuestionarios y evidencias (certificaciones, auditorías, informes de pruebas).
4. **Incorporá las cláusulas mínimas** a cada contrato (apartado 4.5) y revisá que el Oficial de Cumplimiento y el DPD las validen.
5. **Gestioná las tercerizaciones en el exterior** con la debida autorización del BCU (Com. 2022/254) y verificación de las condiciones del país de destino por el DPD.
6. **Controlá la subcontratación**: el tercero principal debe informar y obtener aprobación antes de subcontratar, con las mismas obligaciones.
7. **Seguimiento**: revisión anual de cada tercero crítico, auditorías/inspecciones pactadas y verificación del cumplimiento contractual; documentá los resultados.

## 4. Plantilla del documento

### ENCABEZADO
| **Campo** | **Valor** |
|---|---|
| **Código** | GV-05 |
| **Título** | Gestión de Riesgos de la Cadena de Suministro |
| **Versión** | 1.0 |
| **Estado** | [Borrador / En revisión / Aprobado] |
| **Fecha de aprobación** | [COMPLETAR] |
| **Elaborado por** | RSI |
| **Revisado por** | Comité de Seguridad de la Información / DPD / Oficial de Cumplimiento |
| **Aprobado por** | Gerencia General / Directorio |
| **Clasificación** | Uso interno |
| **Próxima revisión** | [Fecha, máx. 1 año] |

### 1. Objetivo
Gestionar los riesgos de seguridad de la información originados en terceros y en la cadena de suministro del Banco, asegurando que los proveedores cumplan estándares equivalentes a los del banco y que los contratos fijen las garantías y cláusulas mínimas exigidas por el BCU y la URCDP.
### 2. Inventario de terceros críticos
| **N.º** | **Tercero** | **Servicio prestado** | **Datos a los que accede** | **Criticidad** | **Contrato / vigencia** |
|---|---|---|---|---|---|
| [COMPLETAR] | [COMPLETAR] | [COMPLETAR] | [COMPLETAR] | Alta/Media/Baja | [COMPLETAR] |

### 3. Criterios de clasificación de criticidad
- **Alta:** terceros con acceso a datos de clientes, secretos bancarios o sistemas de pagos; falla o incidente que interrumpe servicios esenciales (crédito hipotecario, ahorro, pagos, Banco En Línea).
- **Media:** terceros con acceso parcial o de solo lectura, o que soportan procesos importantes pero sustituibles.
- **Baja:** terceros sin acceso a información sensible ni impacto relevante en operaciones.
### 4. Evaluación de riesgos del proveedor
**4.1 Eje técnico y de seguridad:** [COMPLETAR: certificaciones ISO 27001, controles de acceso, cifrado, gestión de incidentes, pruebas de seguridad, continuidad]. Resultado: [COMPLETAR].
**4.2 Eje legal y normativo:** [COMPLETAR: cláusulas contractuales, protección de datos personales, notificación de vulneraciones, subcontratación, legislación aplicable]. Resultado: [COMPLETAR].
**4.3 Eje de negocio y solvencia:** [COMPLETAR: situación financiera, dependencia del Banco, alternativas en el mercado, capacidad de respuesta]. Resultado: [COMPLETAR].
**4.4 Escala de riesgo y decisión:** Riesgo **Alto** → no contratar o exigir plan de remediación antes del inicio; **Medio** → aceptar con condiciones contractuales y seguimiento reforzado; **Bajo** → aceptar con seguimiento rutinario.
### 5. Cláusulas contractuales mínimas
| **Tema** | **Cláusula mínima exigida** |
|---|---|
| Seguridad de la información | El tercero implementa y mantiene controles de seguridad acordes al riesgo y a la normativa aplicable |
| Resguardo de datos | Garantía del resguardo de datos conforme al art. 492 RNRCSF y al Decreto 64/020 |
| Confidencialidad y secreto bancario | Obligación de confidencialidad que subsiste a la terminación del contrato |
| Datos personales | Tratamiento solo por instrucción del Banco; rol de encargado; derechos ARCO; inscripción ante URCDP [COMPLETAR] |
| Notificación de incidentes | Notificación inmediata (≤ [COMPLETAR] horas) de incidentes y vulneraciones de datos |
| Auditoría e inspección | Derecho del Banco (o auditor externo) a auditar e inspeccionar al tercero y sus instalaciones |
| Subcontratación | Prohibición de subcontratar sin autorización escrita previa del Banco, con las mismas obligaciones |
| Seguridad y retiro de la información | Devolución o destrucción certificada de la información al finalizar el contrato |
| Jurisdicción y legislación | Legislación uruguaya; responsabilidad del tercero por sus subcontratistas |

### 6. Tercerización de actividades en el exterior
Toda tercerización de funciones esenciales en el exterior requiere: [COMPLETAR: autorización previa del BCU conforme a la Comunicación 2022/254, evaluación del marco legal y de protección de datos del país de destino por el DPD, y cláusulas que garanticen la disponibilidad de la información y el acceso del supervisor]. Se documenta: [COMPLETAR].
### 7. Subcontratistas
El tercero debe: identificar a sus subcontratistas, informar cualquier cambio y obtener la aprobación del Banco. Las obligaciones de seguridad se trasladan íntegramente mediante [COMPLETAR: contrato o addenda con el subcontratista]. El Banco mantiene un registro de subcontratistas de los terceros críticos.
### 8. Seguimiento y monitoreo
| **Tercero** | **Frecuencia de evaluación** | **Última evaluación** | **Resultado** | **Próxima acción** |
|---|---|---|---|---|
| [COMPLETAR] | [COMPLETAR] | [COMPLETAR] | [COMPLETAR] | [COMPLETAR] |

El RSI consolida anualmente el estado de la cadena de suministro y lo presenta al Comité de Seguridad y en el informe a la Dirección (GV-06). Los hallazgos críticos se tratan como riesgos del SGSI (ID-04).
### 9. Control de cambios
| **Versión** | **Fecha** | **Cambio** | **Elaboró** | **Aprobó** |
|---|---|---|---|---|
| 0.1 | [COMPLETAR] | Versión inicial (borrador) | RSI | — |
| 1.0 | [COMPLETAR] | Aprobación y alta de terceros críticos | RSI | Comité / Gerencia General |

## 5. Ejemplo aplicado al Banco (modelo de referencia)
Ejemplo ilustrativo. Adaptalo a los contratos y proveedores reales del Banco.
**Inventario (ejemplo):** la procesadora de tarjetas de débito y medios de pago (criticidad alta, accede a datos de tarjetahabientes y al sistema de pagos del Banco); el proveedor del centro de datos y servicios de nube (criticidad alta, aloja el core y Banco En Línea); la empresa de desarrollo de software para el canal digital (criticidad media); el call center de atención al cliente (criticidad media, trata datos personales de ahorristas); la custodia de archivos y documentos de garantías hipotecarias (criticidad media); y el proveedor de correo corporativo y productividad (criticidad media).
**Evaluación (ejemplo):** el proveedor de nube acreditó la certificación ISO 27001 y presentó su informe de auditoría del año, pero muestra brechas en la definición de RPO/RTO para el entorno del core hipotecario; se exige la adecuación del plan de continuidad como condición antes de renovar el contrato.
**Cláusula de incidentes (ejemplo):** el contrato con la procesadora de pagos obliga a notificar al Banco cualquier incidente de seguridad en un plazo máximo de 4 horas, y al DPD la vulneración de datos personales dentro del plazo legal de la Ley 19.670, para que el banco cumpla con sus obligaciones de notificación ante BCU y URCDP.
**Tercerización en el exterior (ejemplo):** el Banco evalúa trasladar parte de la infraestructura de Banco En Línea a una nube internacional; antes de contratar, debe obtener la autorización del BCU conforme a la Comunicación 2022/254, y el DPD debe verificar el nivel de protección del país de destino conforme al Decreto 64/020 (transferencias internacionales), documentando la evaluación de impacto.
**Subcontratación (ejemplo):** el call center no puede derivar la atención de consultas de créditos hipotecarios a un subcontratista sin la aprobación previa por escrito de Compras y Contrataciones y del RSI, con las mismas cláusulas de confidencialidad y secreto bancario.

**Documentos relacionados:** GV-02 (Alcance), GV-03 (Roles y Comité), GV-04 (Plan Anual), ID-01 (Activos), ID-03 (Riesgos), PR-08 (Acuerdos de Confidencialidad y Terceros), URCDP-05 (EIPD), MATRIZ-001 (Correspondencia Normativa).
