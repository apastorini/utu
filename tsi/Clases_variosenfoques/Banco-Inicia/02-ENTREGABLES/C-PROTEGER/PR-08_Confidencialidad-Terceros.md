# PR-08 · Acuerdos de Confidencialidad y Cláusulas de Seguridad con Terceros del Banco

> ⚠️ **Alerta:** este documento menciona **nombres propios del organigrama del Banco** (personas y cargos, abril 2026). Antes de usar el documento, verificá la vigencia de esos nombres contra el organigrama actual.
> **Función del MCU 5.0:** Gobernar (GV.SC — Gestión de riesgos de la cadena de suministro) · Proteger (PR.PS — Procesos)
> **ISO/IEC 27001:** A.6.6 (Acuerdos de confidencialidad) · A.5.19-5.22 (Relaciones con proveedores)
> **BCU:** Circulares 2419 a 2422 (tercerizaciones) · Comunicación 2022/254 · RNRCSF art. 492
> **URCDP:** Ley 18.331 arts. 12 y 29 · Decreto 64/020 (responsabilidad del encargado de tratamiento)
> **Nivel del curso:** 🟡 Practicar · 🔴 Dominar

## 1. Qué es y por qué existe
El Banco no hace todo solo: terceriza desarrollo de software, soporte de sistemas, custodia de documentos, seguridad, limpieza, servicios legales y hasta operaciones del sistema de pagos. Cada tercero con acceso a información del banco es una **extensión de su superficie de riesgo**. El BCU lo sabe y exige (Circulares 2419-2422) que toda tercerización relevante esté **autorizada**, con **evaluación de riesgos** del proveedor y un **contrato mínimo** con cláusulas de seguridad, resguardo de datos, auditoría y subcontratación. La URCDP, por su parte, responsabiliza al banco por el tratamiento de datos personales que hagan sus encargados (Decreto 64/020).
Esta política estandariza dos instrumentos: el **acuerdo de confidencialidad (NDA)**, que firman funcionarios, contratistas y visitas; y las **cláusulas contractuales de seguridad y protección de datos**, que se incorporan a todo contrato con terceros que toquen información del banco. Además define la **matriz de terceros y su criticidad**, para saber a qué proveedores hay que auditar, con qué frecuencia y con qué profundidad.
En el Banco, un proveedor puede ver información de crédito hipotecario, datos personales de clientes o configuraciones del core. Una fuga por tercero se lee ante el BCU y la URCDP como una falla del banco. Por eso estos acuerdos no son "trámites": son el control contractual que respalda todos los controles técnicos de PR-01 a PR-07.
## 2. Marco de referencia
| **Referencia** | **Requisito aplicable** |
|---|---|
| **MCU 5.0 (Agesic)** | GV.SC — gestión de la cadena de suministro y de terceros |
| **ISO/IEC 27001:2022** | A.6.6 acuerdos de confidencialidad; A.5.19 seguridad en las relaciones con proveedores; A.5.20 acuerdos con proveedores; A.5.21 gestión de la seguridad en la cadena de suministro |
| **BCU** | Circulares 2419-2422 (autorización, evaluación y contrato mínimo); Comunicación 2022/254; RNRCSF art. 492 |
| **URCDP** | Ley 18.331 arts. 12 y 29; Ley 19.670; Decreto 64/020 (cláusulas, responsabilidad del encargado, subcontratación) |

## 3. Cómo completar esta plantilla (guía de llenado)
1. **Completá el encabezado** (código, versión, fecha). La aprueba el Comité de Seguridad de la Información.
2. **Levantá la matriz de terceros** con Compras y Contrataciones y con los dueños de los servicios: quién presta qué, con qué acceso y qué criticidad.
3. **Personalizá los apartados [COMPLETAR]** con el modelo de cláusulas aprobado por Servicios Jurídicos Notariales (Dr. Héctor Dotta).
4. **Definí el proceso de evaluación de riesgos del proveedor** con el Jefe de Riesgos No Financieros y el Oficial de Cumplimiento (autorización del BCU cuando corresponda).
5. **Coordiná con el DPD** las cláusulas de protección de datos personales (encargados, subencargados, ARCO, vulneraciones).
6. **Aprobá, registrá en el control de cambios** y publicá en `02-ENTREGABLES/C-PROTEGER`. Revisá anualmente.
## 4. Plantilla del documento

### ENCABEZADO
| **Campo** | **Valor** |
|---|---|
| **Código** | PR-08 |
| **Título** | Acuerdos de Confidencialidad y Cláusulas de Seguridad con Terceros |
| **Versión** | 1.0 |
| **Estado** | [Borrador / En revisión / Aprobado] |
| **Fecha de aprobación** | [COMPLETAR] |
| **Elaborado por** | RSI |
| **Revisado por** | Div. Servicios Jurídicos Notariales · Compras y Contrataciones · DPD · Comité de Seguridad |
| **Aprobado por** | Comité de Seguridad de la Información |
| **Clasificación** | Uso interno |
| **Próxima revisión** | [Fecha, máx. 1 año] |

### 1. Objetivo
Regular contractualmente la **confidencialidad y la seguridad de la información** que el Banco comparte con funcionarios, contratistas y terceros, de modo que los controles de PR-01 a PR-07 se extiendan a toda la cadena de suministro y se pueda demostrar cumplimiento ante el BCU y la URCDP.
### 2. Alcance
Aplica a [COMPLETAR: todos los proveedores, contratistas, consultores y personas ajenas al Banco que accedan, procesen o custodien información del banco —incluidos los del sistema de pagos, desarrollo de software, soporte, custodia y limpieza— y a todos los funcionarios del Banco]. Aplica a los NDA y a las cláusulas de todo contrato nuevo o renovado.
### 3. Matriz de terceros y criticidad
| **Tercero / servicio** | **Acceso a información** | **Criticidad** | **Evaluación de riesgo** | **Auditoría** |
|---|---|---|---|---|
| [COMPLETAR: proveedor del core] | [COMPLETAR] | [Alta/Media/Baja] | [COMPLETAR: fecha/resultado] | [Frecuencia] |
| [COMPLETAR: soporte del sistema de pagos] | [COMPLETAR] | [Alta/Media/Baja] | [COMPLETAR] | [Frecuencia] |
| [COMPLETAR] | [COMPLETAR] | [Alta/Media/Baja] | [COMPLETAR] | [Frecuencia] |

- La matriz se actualiza al menos anualmente y ante cambios de contrato.
- Los terceros críticos se re-evalúan con la **Comunicación 2022/254 del BCU** y se informa al BCU las tercerizaciones que lo requieran (autorización previa, expresa si es en/desde el exterior).
### 4. Acuerdo de confidencialidad (NDA)
- **Funcionarios:** firman NDA al ingreso (antes del alta de accesos) y se reafirma en la inducción de seguridad (PR-02).
- **Contratistas y pasantes:** firman NDA antes de comenzar actividades.
- **Visitas y proveedores ocasionales:** firman NDA o cláusula equivalente al ingresar a zonas restringidas.
- El NDA incluye: obligación de confidencialidad indefinida, secreto bancario, prohibición de copia y divulgación, devolución/eliminación de información al cese y consecuencias del incumplimiento.
### 5. Cláusulas contractuales con terceros (modelo)
Todo contrato con tercero que trate información del Banco incluye como mínimo:
| **Cláusula** | **Contenido mínimo** |
|---|---|
| **Confidencialidad** | Deber de confidencialidad, secreto bancario y protección de datos |
| **Seguridad de la información** | Cumplir las políticas del Banco (PR-01…PR-07) y medidas técnicas/organizativas adecuadas |
| **Tratamiento de datos personales** | El tercero actúa como **encargado de tratamiento**; finalidad, instrucciones del Banco (responsable), deberes del art. 12/29 URCDP |
| **Notificación de incidentes** | Notificación inmediata (máx. 24-48 h) al Banco de cualquier incidente o vulneración; colaboración en la notificación a la URCDP |
| **Derecho de auditoría** | El Banco puede auditar los controles del tercero (o contratar auditoría) |
| **Subcontratación** | Autorización previa del Banco para subcontratar; responsabilidad solidaria; cumplimiento de las mismas obligaciones |
| **Resguardo y devolución de datos** | Resguardo según art. 492 RNRCSF; devolución y/o borrado seguro al término del contrato |
| **Disposiciones de extinción** | Devolución de información, certificación de borrado, cese de accesos (en coordinación con PR-01) |

### 5.1. Evaluación de riesgos previa al contrato
Antes de la contratación: se evalúa la **solvencia técnica, legal y de seguridad** del proveedor (cuestionario de seguridad, referencias, incidentes previos). Los terceros críticos requieren informe de riesgo aprobado por el RSI y el Oficial de Cumplimiento.
### 6. Responsabilidades
| **Rol** | **Responsabilidad** |
|---|---|
| **Compras y Contrataciones** | Incorporar las cláusulas tipo a todos los contratos; mantener la matriz |
| **Div. Servicios Jurídicos Notariales** | Redacción y revisión legal de NDA y cláusulas |
| **Dueños de servicios** | Identificar terceros, vigilar su desempeño y accesos |
| **RSI** | Evaluación de riesgos de seguridad, auditorías a terceros y seguimiento de incidentes |
| **DPD** | Cláusulas de datos personales y subencargados |
| **Oficial de Cumplimiento** | Coordinación con el BCU por tercerizaciones que requieren autorización |

### 7. Control de cambios
| **Versión** | **Fecha** | **Cambio** | **Elaboró** | **Aprobó** |
|---|---|---|---|---|
| 0.1 | [COMPLETAR] | Versión inicial (borrador) | RSI | — |
| 1.0 | [COMPLETAR] | Aprobación del Comité | RSI | Comité |

## 5. Ejemplo aplicado al Banco (modelo de referencia)
Ejemplo ilustrativo de cómo quedaría el apartado 4 completado. Adaptá al contenido institucional real del Banco.
**Matriz de terceros (ejemplo):**
- **Proveedor de mantenimiento del core bancario:** acceso remoto con MFA al ambiente de soporte, clasificado **Alta criticidad**; evaluación de riesgos anual y auditoría de seguridad cada 2 años.
- **Proveedor de infraestructura del datacenter alternativo:** custodia de respaldos y servidores, **Alta criticidad**; se verifica la **separación geográfica** exigida por el art. 492 RNRCSF.
- **Empresa de custodia de documentos y destrucción:** maneja expedientes "Confidencial" y "Secreto"; contrato con cláusulas de NDA, devolución y certificación de destrucción.
**Cláusulas (ejemplo):**
- El contrato de soporte del **sistema de pagos** incluye: notificación de incidentes en **máx. 24 h**, derecho de auditoría del Banco, prohibición de subcontratar sin autorización y borrado certificado de la información al término del contrato.
- El contrato con el proveedor del **call center / atención** (si aplica) incorpora las cláusulas de **encargado de tratamiento** del Decreto 64/020: instrucciones del Banco como responsable, deber de responder derechos ARCO a través del Banco y notificación de vulneraciones.
**NDA de funcionarios (ejemplo):**
- En el ingreso, cada funcionario firma el NDA antes del alta de sus accesos (se coordina con PR-01); los contratistas de mantenimiento firman NDA en la recepción de cada ingreso a zonas restringidas, junto con el registro de visita (PR-04).

**Documentos relacionados:** GV-01 (Política de Seguridad), GV-05 (Riesgos de la cadena de suministro), PR-01 (Control de Acceso), PR-04 (Seguridad Física), PR-05 (Respaldo), PR-07 (Desarrollo Seguro), URCDP-01 (Seguridad de Datos Personales), RS-02 (Notificación de Incidentes).
