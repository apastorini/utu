# ID-01 · Inventario de Activos de Información del Banco

> ⚠️ **Alerta:** este documento menciona **nombres propios del organigrama del Banco** (personas y cargos, abril 2026). Antes de usar el documento, verificá la vigencia de esos nombres contra el organigrama actual.
> **Función del MCU 5.0:** Identificar (ID.AM — Gestión de activos)
> **ISO/IEC 27001:** A.5.9 (Inventario de activos de información) · A.5.10 (Propiedad de los activos)
> **BCU:** Estándares Mínimos de Gestión — Riesgo Tecnológico; RNRCSF art. 492 (resguardo de datos)
> **URCDP:** Ley 18.331 art. 10 (medidas de seguridad) · Decreto 414/009 (inscripción de bases de datos)
> **Nivel del curso:** 🟢 Descubrir · 🟡 Practicar

## 1. Qué es y por qué existe
El **Inventario de Activos de Información** es el listado único y actualizado de **todo lo que tiene valor para el Banco y que, si se daña, se pierde o se filtra, provoca daño al banco, a sus clientes o al sistema financiero**. Sin inventario no hay gestión de riesgos posible: no se puede proteger ni medir lo que no se conoce.
El inventario es la **base de datos maestra del SGSI**: de él salen el análisis de riesgos (ID-02/03), el plan de tratamiento (ID-04), la clasificación de la información (PR-03), la declaración de aplicabilidad y las pruebas de continuidad (RC-01/02). También permite responder ante la URCDP qué bases de datos con datos personales trata el banco, y ante el BCU qué activos soportan los procesos críticos.
Los activos no son solo "computadoras y programas": incluyen **procesos, datos, aplicaciones, hardware, redes, servicios prestados por terceros, personas y hasta las instalaciones físicas**. Una sucursal, un funcionario clave o un contrato con un proveedor de pagos son activos tanto como el core bancario.
## 2. Marco de referencia
| **Marco** | **Referencia** | **Qué exige aplicable al Banco** |
|---|---|---|
| **MCU 5.0 (Agesic)** | ID.AM-01 a ID.AM-07 | Inventariar y valorar activos físicos y lógicos, mantener el inventario actualizado, y priorizar los que soportan funciones críticas del negocio |
| **ISO/IEC 27001** | A.5.9, A.5.10 | Inventario de activos y designación de un propietario responsable por cada activo |
| **BCU** | EMG · Riesgo Tecnológico; RNRCSF art. 492; Circ. 2227 | Conocer los activos que soportan los procesos y servicios críticos; resguardo y disponibilidad de la información |
| **URCDP** | Ley 18.331 art. 10; D. 414/009 art. 22 | Identificar las bases de datos con datos personales para inscribirlas y protegerlas según su sensibilidad |

## 3. Cómo completar esta plantilla (guía de llenado)
1. **Definí el alcance:** inventariá todos los activos dentro del alcance del SGSI (GV-02). Empezá por los procesos críticos y sus dependencias.
2. **Identificá por categoría:** recorré cada tipo de activo (procesos, datos, aplicaciones, hardware, redes, servicios externos, personas, instalaciones) y listá los concretos del Banco.
3. **Asigná el propietario:** para cada activo definí un **propietario** (el que decide sobre su uso) y un **custodio** (el que lo opera día a día). Son roles, no personas fijas.
4. **Completá las columnas:** código único, nombre, tipo, propietario, custodia, ubicación, clasificación (PR-03) y dependencias. No dejes columnas vacías.
5. **Clasificá** cada activo según el esquema de clasificación de la información (Pública / Uso interno / Confidencial / Reservada).
6. **Consultá en el Banco:** Gerente de División TI (Bernardo Ureta) por los sistemas y la infraestructura; Jefe de Departamento Sistema de Pagos (Guillermo Correa) por los servicios de pago; cada propietario de proceso de Área Comercial, Operaciones y Administración Financiera; el DPD por las bases con datos personales; y el Depto. Servicios Generales por la seguridad física de sucursales y del datacenter.
7. **Mantenelo vivo:** revisá el inventario al menos semestralmente y ante todo alta/baja de sistemas. El RSI (Área Riesgos) custodia el documento y coordina su actualización.
## 4. Plantilla del documento

### ENCABEZADO
| **Campo** | **Valor** |
|---|---|
| **Código** | ID-01 |
| **Título** | Inventario de Activos de Información del Banco |
| **Versión** | 1.0 |
| **Estado** | [Borrador / En revisión / Aprobado] |
| **Fecha de aprobación** | [COMPLETAR] |
| **Elaborado por** | RSI |
| **Revisado por** | Comité de Seguridad de la Información |
| **Aprobado por** | Gerencia General |
| **Clasificación** | Confidencial (contiene información sobre infraestructura del banco) |
| **Próxima revisión** | [Fecha, máx. 6 meses] |

### 1. Objetivo
Registrar, de forma única y actualizada, todos los activos de información del Banco dentro del alcance del SGSI, con su propietario, clasificación y dependencias, como base para la gestión de riesgos, la continuidad del negocio y el cumplimiento normativo.
### 2. Categorías de activos inventariadas
| **Nº** | **Tipo de activo** | **Descripción** |
|---|---|---|
| 1 | **Procesos** | Procesos de negocio que transforman información (crédito hipotecario, pagos, ahorro, atención al cliente) |
| 2 | **Datos / Información** | Bases de datos, expedientes, archivos, contratos, registros contables |
| 3 | **Aplicaciones / Software** | Sistemas, plataformas y software de base |
| 4 | **Hardware** | Servidores, equipos de red, puestos de trabajo, dispositivos móviles, ATM |
| 5 | **Redes** | Redes de datos, telecomunicaciones, conexiones con terceros |
| 6 | **Servicios externos** | Servicios provistos por terceros (cloud, mensajería, mantenimiento, impresión) |
| 7 | **Personas** | Funcionarios, roles clave, proveedores con acceso, asesores |
| 8 | **Instalaciones** | Edificios, sucursales, datacenter, áreas de archivo físico |

### 3. Estructura del inventario (columnas obligatorias)
| **Columna** | **Qué se completa** | **Ejemplo** |
|---|---|---|
| **Código** | Identificador único del activo | ACT-APP-012 |
| **Nombre** | Nombre oficial del activo | Core bancario (sistema central) |
| **Tipo** | Categoría del punto 2 | Aplicación |
| **Propietario** | Quién decide sobre el activo | Gerente de División TI |
| **Custodia** | Quién lo opera/custodia día a día | Jefe de Departamento Producción |
| **Ubicación** | Dónde reside (físico/lógico) | Datacenter Banco / sucursales |
| **Clasificación** | Nivel de clasificación de la información | Confidencial |
| **Dependencias** | Activos o servicios de los que depende | Red de datos, energía, servicio cloud |

### 4. Registro de activos
[COMPLETAR: transcribir aquí el inventario completo. Tabla de ejemplo de primer llenado:]
| **Código** | **Nombre** | **Tipo** | **Propietario** | **Custodia** | **Ubicación** | **Clasificación** | **Dependencias** |
|---|---|---|---|---|---|---|---|
| ACT-PRO-001 | [COMPLETAR] | Proceso | [COMPLETAR] | [COMPLETAR] | [COMPLETAR] | [COMPLETAR] | [COMPLETAR] |
| ACT-DAT-001 | [COMPLETAR] | Datos | [COMPLETAR] | [COMPLETAR] | [COMPLETAR] | [COMPLETAR] | [COMPLETAR] |
| ACT-APP-001 | [COMPLETAR] | Aplicación | [COMPLETAR] | [COMPLETAR] | [COMPLETAR] | [COMPLETAR] | [COMPLETAR] |

### 5. Activos críticos
[COMPLETAR: marcar con un indicador los activos que soportan procesos críticos (crédito, pagos, continuidad operativa). Estos serán priorizados en ID-03.]
### 6. Mantenimiento y revisión
El inventario se revisa [COMPLETAR: semestralmente y ante cambios mayores]. Toda alta o baja de un activo se registra en un plazo máximo de [COMPLETAR: 10 días hábiles] por su custodio.
### 7. Control de cambios
| **Versión** | **Fecha** | **Cambio** | **Elaboró** | **Aprobó** |
|---|---|---|---|---|
| 0.1 | [COMPLETAR] | Versión inicial (levantamiento de activos) | RSI | — |
| 1.0 | [COMPLETAR] | Aprobación del inventario | RSI | Gerencia General |

## 5. Ejemplo aplicado al Banco (modelo de referencia)
Ejemplo ilustrativo con activos realistas del Banco para guiar el primer llenado. Verificá nombres, versiones y dependencias reales antes de aprobar.
**Activos críticos identificados (extracto):**
| **Código** | **Nombre** | **Tipo** | **Propietario** | **Custodia** | **Ubicación** | **Clasificación** | **Dependencias** |
|---|---|---|---|---|---|---|---|
| ACT-PRO-001 | Proceso de otorgamiento de créditos hipotecarios | Proceso | Área Comercial (Pablo Liard) | Depto. Análisis de Préstamos | Todas las sucursales | Confidencial | Core bancario, Banco En Línea, base de clientes |
| ACT-DAT-001 | Base de datos de clientes y expedientes de crédito | Datos | Div. TI | Depto. Producción | Datacenter Banco | Confidencial | Core bancario, respaldo (PR-05) |
| ACT-APP-001 | Core bancario (sistema central) | Aplicación | Div. TI | Depto. Producción | Datacenter Banco | Confidencial | Red de datos, energía, base de datos |
| ACT-APP-002 | Banco En Línea (banca por internet) | Aplicación | Div. TI | Depto. Sistemas | Datacenter Banco + DMZ | Confidencial | Core bancario, autenticación, red internet |
| ACT-APP-003 | Sistema de pagos del Banco (Banco Pagos) | Aplicación | Div. Operaciones | Depto. Sistema de Pagos (Guillermo Correa) | Datacenter Banco | Reservada | Core bancario, red BCU, RNRCSF Circ. 2280 |
| ACT-HW-001 | Servidores del datacenter | Hardware | Div. TI | Depto. Producción | Datacenter Banco | Uso interno | Energía, clima, red |
| ACT-NET-001 | Red LAN/WAN del Banco | Red | Div. TI | Depto. Soporte Técnico | Datacenter + sucursales | Confidencial | Todos los sistemas |
| ACT-SER-001 | Servicio de nube / hosting de tercero | Servicio externo | Div. TI | Depto. Producción | Proveedor externo | Confidencial | Acuerdo de nivel de servicio (GV-05) |
| ACT-PER-001 | Equipo de producción y soporte crítico | Personas | Div. Capital Humano | Depto. Producción | Datacenter | Confidencial | Plan de continuidad |
| ACT-INS-001 | Sucursales y cajeros automáticos (ATM) | Instalaciones | Depto. Servicios Generales (Agustín Araujo) | Sucursales | Todo el país | Uso interno | Red de datos, seguridad física |

**Notas del ejemplo:** cada activo crítico tiene dependencias que disparan controles: el core depende de respaldo (PR-05) y continuidad (RC-02); el sistema de pagos depende de la normativa BCU Circ. 2280; la base de clientes dispara los controles de la URCDP (URCDP-01/04). El inventario debe cruzar con ID-03 para identificar riesgos por activo.

**Documentos relacionados:** GV-02 (Alcance del SGSI) · ID-02 (Metodología de riesgos) · ID-03 (Análisis de riesgos) · PR-03 (Clasificación de la información) · PR-05 (Respaldo) · URCDP-04 (Inscripción de bases de datos).
