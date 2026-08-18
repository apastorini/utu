# PR-07 · Seguridad en el Desarrollo de Software (SDLC) del Banco

> ⚠️ **Alerta:** este documento menciona **nombres propios del organigrama del Banco** (personas y cargos, abril 2026). Antes de usar el documento, verificá la vigencia de esos nombres contra el organigrama actual.
> **Función del MCU 5.0:** Proteger (PR.PS — Procesos de protección) · Identificar (ID.RA — Riesgos)
> **ISO/IEC 27001:** A.8.25 (Ciclo de vida de desarrollo seguro) · A.8.26 (Requisitos de seguridad de las aplicaciones) · A.8.27 (Arquitectura segura) · A.8.28 (Codificación segura) · A.8.31 (Separación de ambientes)
> **BCU:** Estándares Mínimos de Gestión — Función de Gestión de TI
> **URCDP:** Ley 18.331 art. 12 · Decreto 64/020 (privacidad por diseño y por defecto)
> **Nivel del curso:** 🟡 Practicar · 🔴 Dominar

## 1. Qué es y por qué existe
El software que desarrolla o manda a desarrollar el Banco (aplicaciones sobre el **core bancario**, mejoras al **Banco En Línea**, integraciones con el **sistema de pagos**, herramientas internas) es donde la seguridad se gana o se pierde. Arreglar una falla de seguridad después de poner la aplicación en producción cuesta hasta decenas de veces más que evitarla en el diseño, y expone datos de clientes mientras tanto. Por eso la seguridad debe **integrarse en todo el ciclo de desarrollo** (SDLC), no revisarse al final.
Esta política define cómo el Banco construye software seguro: **requisitos de seguridad** desde el inicio, **threat modeling** de los componentes críticos, **revisión de código**, **análisis estático (SAST)** y **dinámico (DAST)**, gestión de **dependencias y SBOM**, **pruebas de seguridad previas a producción** y **ambientes de desarrollo y producción separados**. Aplica tanto al desarrollo interno (División de Sistemas) como a los proveedores que desarrollan para el banco.
Además, la URCDP exige la **privacidad por diseño** (Decreto 64/020): las aplicaciones que tratan datos personales deben incorporar la protección de datos desde el diseño y por defecto. El DPD debe participar en las etapas tempranas de los proyectos que tratan datos personales, con evaluación de impacto (EIPD, URCDP-05) cuando corresponda.
## 2. Marco de referencia
| **Referencia** | **Requisito aplicable** |
|---|---|
| **MCU 5.0 (Agesic)** | PR.PS — procesos y procedimientos de protección (desarrollo seguro) |
| **ISO/IEC 27001:2022** | A.8.25 desarrollo seguro; A.8.26 requisitos de seguridad; A.8.27 arquitectura segura; A.8.28 codificación segura; A.8.31 separación de ambientes |
| **BCU** | EMG · Función de Gestión de TI (primera línea: arquitectura, desarrollo, operación) |
| **URCDP** | Ley 18.331 arts. 10 y 12; Decreto 64/020 (privacidad por diseño y por defecto); EIPD (URCDP-05) |

## 3. Cómo completar esta plantilla (guía de llenado)
1. **Completá el encabezado** (código, versión, fecha). La aprueba el Comité de Seguridad de la Información.
2. **Coordiná con la División de Sistemas** (Jefe de Departamento Sistemas, Lic. Cristian Palo) el proceso de desarrollo actual y dónde insertar los controles.
3. **Definí con Compras y Contrataciones** cómo se aplicará esta política a los **proveedores de desarrollo** (cláusulas contractuales de seguridad — ver PR-08).
4. **Personalizá los apartados [COMPLETAR]** con las herramientas de SAST/DAST/SBOM y los umbrales de aceptación.
5. **Incluí al DPD** en los proyectos que tratan datos personales (privacidad por diseño).
6. **Aprobá, registrá en el control de cambios** y publicá en `02-ENTREGABLES/C-PROTEGER`. Revisá anualmente o al cambiar de plataforma de desarrollo.
## 4. Plantilla del documento

### ENCABEZADO
| **Campo** | **Valor** |
|---|---|
| **Código** | PR-07 |
| **Título** | Seguridad en el Desarrollo de Software (SDLC) |
| **Versión** | 1.0 |
| **Estado** | [Borrador / En revisión / Aprobado] |
| **Fecha de aprobación** | [COMPLETAR] |
| **Elaborado por** | RSI |
| **Revisado por** | Div. Sistemas · DPD · Comité de Seguridad |
| **Aprobado por** | Comité de Seguridad de la Información |
| **Clasificación** | Uso interno |
| **Próxima revisión** | [Fecha, máx. 1 año] |

### 1. Objetivo
Incorporar la seguridad en **todas las etapas del ciclo de vida del software** del Banco —interno o de terceros— de modo que las aplicaciones en producción cumplan los requisitos de seguridad y protección de datos desde el diseño, reduciendo vulnerabilidades y fallas de privacidad.
### 2. Alcance
Aplica a [COMPLETAR: todo desarrollo, mantenimiento, personalización y adquisición de software del Banco —core, Banco En Línea, sistema de pagos, aplicaciones internas, integraciones y APIs—] realizado por la División de Sistemas o por proveedores externos.
### 3. Ciclo de desarrollo seguro (fases)
| **Fase** | **Controles de seguridad** |
|---|---|
| **Requisitos** | Requisitos de seguridad y privacidad por diseño; revisión del DPD si hay datos personales; EIPD si corresponde |
| **Diseño** | Threat modeling de componentes críticos; arquitectura segura; revisión de autenticación y autorización |
| **Codificación** | Guía de codificación segura; análisis estático (SAST) en cada integración |
| **Pruebas** | Pruebas funcionales + seguridad (DAST); prueba de datos enmascarados; pruebas de acceso y control |
| **Despliegue** | Revisión de configuración segura; escaneo de dependencias (SBOM); aprobación de liberación |
| **Operación y mantenimiento** | Monitoreo; gestión de vulnerabilidades (PR-06); parches de la aplicación |

### 3.1. Requisitos de seguridad y threat modeling
- Todo proyecto define requisitos de seguridad en la etapa de requisitos [COMPLETAR: plantilla de requisitos].
- Para los componentes que procesan pagos, créditos o datos personales se realiza **threat modeling** (p. ej. STRIDE) con revisión del RSI.
### 4. Análisis estático (SAST) y dinámico (DAST)
- **SAST:** análisis de código en cada integración/commit con herramienta [COMPLETAR: herramienta SAST, incluidas opciones open source].
- **DAST:** pruebas de seguridad sobre la aplicación en ejecución previas a producción.
- **Umbral de aceptación:** no se libera a producción con hallazgos críticos o altos [COMPLETAR: umbral].
### 5. Gestión de dependencias y SBOM
- Se mantiene un **inventario de dependencias (SBOM)** por aplicación.
- Se escanean las dependencias contra bases de datos de vulnerabilidades (CVE) en cada ciclo.
- Las dependencias sin mantenimiento (abandonadas) se reemplazan o se registran como excepción con mitigación.
### 6. Pruebas de seguridad previas a producción
- Verificación de: autenticación, control de acceso, validación de entradas, gestión de sesiones, cifrado y registro de eventos.
- Revisión de **datos de prueba**: solo datos enmascarados/anonimizados, nunca datos reales de clientes (PR-03).
- Pruebas de integración segura con el core y el sistema de pagos.
### 7. Separación de ambientes
- **Desarrollo, prueba (homologación) y producción** son ambientes separados, con redes y accesos distintos (A.8.31).
- El acceso a producción es restringido y trazado (PR-01); los desarrolladores no modifican producción directamente.
- Los datos de producción nunca se copian a ambientes de prueba sin enmascaramiento previo.
### 8. Integración con el área de Sistemas y con proveedores
- La División de Sistemas actúa como **primera línea**: implementa y verifica los controles.
- Los **proveedores de desarrollo** deben cumplir esta política; sus entregables se verifican con los mismos controles (SAST/DAST/SBOM) y las obligaciones se incorporan al contrato (PR-08).
- El RSI realiza **revisiones de seguridad** en los hitos del proyecto.
### 9. Responsabilidades
| **Rol** | **Responsabilidad** |
|---|---|
| **Div. Sistemas** | Aplicar los controles del ciclo; herramientas SAST/DAST; gestión del SBOM |
| **Jefe de proyecto / dueño del producto** | Incluir requisitos de seguridad en la planificación |
| **DPD** | Privacidad por diseño; EIPD en proyectos con datos personales |
| **RSI** | Revisar threat modeling y resultados de pruebas; aprobar la liberación desde lo funcional de seguridad |
| **Compras y Contrataciones** | Incorporar estas obligaciones en los contratos con proveedores |

### 10. Control de cambios
| **Versión** | **Fecha** | **Cambio** | **Elaboró** | **Aprobó** |
|---|---|---|---|---|
| 0.1 | [COMPLETAR] | Versión inicial (borrador) | RSI | — |
| 1.0 | [COMPLETAR] | Aprobación del Comité | RSI | Comité |

## 5. Ejemplo aplicado al Banco (modelo de referencia)
Ejemplo ilustrativo de cómo quedaría el apartado 4 completado. Adaptá al contenido institucional real del Banco.
**Desarrollo del Banco En Línea (ejemplo):**
- El proyecto de renovación del **Banco En Línea** incorporó desde los requisitos: MFA para clientes en operaciones de alta sensibilidad, límites de sesión, y **privacidad por diseño** (solo se muestran los datos mínimos necesarios en pantalla). El DPD participó en el diseño y se realizó una **EIPD** por el tratamiento de datos personales.
- En cada integración se ejecutó **SAST**; en el ambiente de homologación se realizó **DAST** antes de la liberación. El **SBOM** de las bibliotecas front-end detectó una dependencia con vulnerabilidad alta, que se actualizó antes de salir a producción.
**Integración con el sistema de pagos (ejemplo):**
- La nueva API de consulta de saldos para el **sistema de pagos** se modeló con **threat modeling**; se identificó un riesgo de exposición excesiva en la respuesta de la API, que se corrigió en el diseño (devolver solo el dato mínimo). Se probó en ambiente separado y se liberó con umbral de aceptación sin hallazgos críticos.
**Proveedor de desarrollo (ejemplo):**
- El contrato con el proveedor del nuevo módulo de **gestión de garantías** incorpora las cláusulas de PR-08: entrega de resultados de SAST, cumplimiento de esta política y derecho de auditoría. Los entregables se verificaron antes del pago del hito final.

**Documentos relacionados:** GV-01 (Política de Seguridad), PR-03 (Seguridad de Datos), PR-06 (Vulnerabilidades), PR-08 (Confidencialidad y Terceros), DE-01 (Monitoreo), URCDP-05 (EIPD).
