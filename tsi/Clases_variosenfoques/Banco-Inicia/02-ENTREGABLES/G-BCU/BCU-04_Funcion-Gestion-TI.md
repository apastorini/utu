# BCU-04 · Función de Gestión de Tecnologías de la Información (Primera Línea) del Banco

> ⚠️ **Alerta:** este documento menciona **nombres propios del organigrama del Banco** (personas y cargos, abril 2026). Antes de usar el documento, verificá la vigencia de esos nombres contra el organigrama actual.
> **Función del MCU 5.0:** Proteger (PR) · Detectar (DE) · Recuperar (RC)
> **ISO/IEC 27001:** Cláusula 8 (Operación) · A.5.37, A.8.8, A.8.9, A.8.31 (cambios), A.8.32 (control de cambios), A.8.25-8.28 (desarrollo seguro)
> **BCU:** Estándares Mínimos de Gestión — Función de Gestión de TI · Circular 2227 · Circular 2280 (sistema de pagos)
> **URCDP:** Ley 18.331 art. 10 · Decreto 64/020 arts. 7-8 (privacidad por diseño y por defecto)
> **Nivel del curso:** 🟡 Practicar · 🔴 Dominar

## 1. Qué es y por qué existe
La **Función de Gestión de TI** es la **primera línea de defensa**: el conjunto de procesos, equipos y herramientas con los que el Banco opera, mantiene, protege y evoluciona su tecnología. El BCU espera que la entidad tenga un **gobierno de TI** mínimo: gestión de operaciones, gestión de cambios, gestión de incidentes técnicos, gestión de configuraciones, arquitectura y desarrollo seguro. Esta función es la que implementa los controles que la segunda línea (RSI) supervisa.
En el Banco esta función reside en la **División Tecnología de la Información** del Área Operaciones y TI, con tres departamentos: **Producción** (operación de la plataforma y servicios), **Sistemas** (desarrollo y mantenimiento de aplicaciones) y **Soporte Técnico** (atención a usuarios y puestos de trabajo). A ellos se suma la gestión de arquitectura, la gestión de cambios y las funciones de seguridad técnica que el BCU y Agesic esperan.
La normativa de TI del supervisor exige calidad de servicio y control: los cambios se aprueban y prueban antes de pasar a producción; los incidentes técnicos se registran, clasifican y resuelven con criterios de prioridad; las configuraciones se documentan y se protegen; y el desarrollo de software incorpora seguridad en cada etapa. La Circular 2280 refuerza la calidad de servicio del **Departamento de Sistema de Pagos**, que convive en el Área Operaciones.
## 2. Marco de referencia
| **Marco** | **Referencia** | **Qué exige** |
|---|---|---|
| **MCU 5.0 (Agesic)** | PR.PS (Seguridad de plataformas) · PR.IR (Resiliencia de la infraestructura) · DE.CM (Monitoreo) · RC.RP | Operación protegida, mantenimiento seguro, gestión de cambios e incidentes |
| **ISO/IEC 27001** | Cláusula 8 · A.8.31/A.8.32 (cambios) · A.8.8 (protección contra malware) · A.8.9 (configuración) · A.8.25-8.28 (desarrollo) | Gestión de operaciones con control de cambios, configuraciones y desarrollo seguro |
| **BCU** | EMG · Gestión de TI · Circular 2227 · Circular 2280 (pagos) | Gobierno de TI, calidad de servicio, monitoreo proactivo y continuidad operativa |
| **URCDP** | Ley 18.331 art. 10 · Decreto 64/020 arts. 7-8 | Los sistemas deben garantizar integridad y seguridad; privacidad por diseño y por defecto |

## 3. Cómo completar esta plantilla (guía de llenado)
1. **Completá el encabezado** con los datos del documento.
2. **Describí la organización de TI del Banco** con los nombres vigentes del organigrama (Módulo 7) y las funciones de cada departamento.
3. **Formalizá los procesos** de operación, cambios, incidentes técnicos, configuraciones y arquitectura: no describas lo que se hace de palabra, documentalo.
4. **Definí los procedimientos de desarrollo seguro** (SDLC) y su vínculo con PR-07.
5. **Establecé la coordinación con el RSI** (segunda línea) y los canales de escalamiento.
6. **Definí los indicadores de servicio** (disponibilidad, tiempos de resolución, cumplimiento de ventanas de cambio) alineados con la Circular 2280.
7. **Identificá al responsable de cada proceso** (cargo y nombre si corresponde).
**A quién consultar en el Banco:** Gerente de División TI (Lic. Bernardo Ureta) y los Jefes de Departamento Producción (Ing. Daniel Herrera), Sistemas (Lic. Cristian Palo) y Soporte Técnico (Tec. Ariel Presa); RSI por los criterios de seguridad; Jefe de Riesgos No Financieros por el riesgo operacional.
## 4. Plantilla del documento

### ENCABEZADO
| **Campo** | **Valor** |
|---|---|
| **Código** | BCU-04 |
| **Título** | Función de Gestión de Tecnologías de la Información (Primera Línea) |
| **Versión** | 1.0 |
| **Estado** | [Borrador / En revisión / Aprobado] |
| **Fecha de aprobación** | [COMPLETAR] |
| **Elaborado por** | Gerente de División TI |
| **Revisado por** | RSI / Comité de Seguridad de la Información |
| **Aprobado por** | Gerencia General |
| **Clasificación** | Uso interno |
| **Próxima revisión** | [Fecha, máx. 1 año] |

### 1. Objetivo
Definir la organización y los procesos de gestión de TI del Banco —operaciones, cambios, incidentes técnicos, configuraciones, arquitectura y desarrollo seguro— como primera línea de defensa de la seguridad de la información.
### 2. Organización de la División TI
| **Departamento** | **Responsable** | **Función principal** |
|---|---|---|
| **Producción** | [COMPLETAR] | Operación de la plataforma, monitoreo, continuidad técnica |
| **Sistemas** | [COMPLETAR] | Desarrollo y mantenimiento de aplicaciones, integraciones |
| **Soporte Técnico** | [COMPLETAR] | Atención a usuarios, puestos de trabajo, activos de escritorio |
| **Arquitectura y seguridad técnica** | [COMPLETAR] | Diseño de soluciones, estándares, administración de plataformas |

### 3. Gestión de operaciones
a) Monitoreo 24x7 de los servicios críticos [COMPLETAR: sistema central de crédito, canales, pagos, correo, red].
b) Procedimientos de inicio, operación y cierre de servicios y de procesamiento batch.
c) Gestión de capacidades y rendimiento.
d) Coordinación con el Departamento de Sistema de Pagos para el cumplimiento de la Circular 2280.
e) Cumplimiento del art. 492: ejecución del resguardo de datos, custodia de claves de desencriptación y apoyo a las pruebas anuales de recuperación.
### 4. Gestión de cambios
Todo cambio en sistemas, infraestructura o configuración se gestiona mediante [COMPLETAR: comité de cambios / proceso documentado]: solicitud, análisis de riesgo e impacto, aprobación (incluida la del RSI para cambios con impacto en seguridad), ventana de implementación, prueba de retroceso y registro. Los cambios de emergencia siguen el mismo proceso con autorización excepcional.
### 5. Gestión de incidentes técnicos
a) Registro y clasificación de incidentes (severidad, prioridad, impacto).
b) Escalamiento a niveles de soporte y al RSI ante incidentes de seguridad (RS-01).
c) Acuerdos de nivel de servicio internos: tiempos de respuesta y resolución.
d) Análisis de causa raíz y registro de lecciones aprendidas para incidentes mayores.
e) Coordinación con el Departamento de Sistema de Pagos para incidentes de pagos (Circular 2280).
### 6. Gestión de configuraciones
a) Inventario de configuración de hardware, software y parámetros de aplicaciones.
b) Control de versiones y de parámetros de los sistemas.
c) Copias de configuración y de documentación técnica protegidas conforme al art. 492.
d) Revisión periódica de configuraciones frente a estándares (A.8.9).
### 7. Arquitectura y desarrollo seguro
a) La arquitectura define estándares de seguridad por defecto y privacidad por diseño (Decreto 64/020 arts. 7-8).
b) El desarrollo sigue el ciclo seguro (PR-07): análisis de requisitos, modelado de amenazas, revisión de código, pruebas de seguridad y despliegue controlado.
c) Los cambios de aplicaciones pasan a producción solo con las pruebas aprobadas y el alta de seguridad correspondiente.
d) Los accesos a entornos de desarrollo y producción se separan y controlan.
### 8. Coordinación con la segunda línea
La División TI implementa los controles definidos por el RSI, participa en la evaluación de riesgos tecnológicos, aporta evidencia en las auditorías y escala al RSI todo incidente con posible impacto de seguridad. Las decisiones que afecten el perfil de riesgo se toman con el RSI y, cuando corresponde, con el Comité.
### 9. Indicadores de servicio
| **Indicador** | **Definición** | **Meta** |
|---|---|---|
| Disponibilidad de sistemas críticos | % de tiempo operativo en horario de servicio | [COMPLETAR] |
| Cumplimiento de ventanas de cambio | Cambios aprobados y ejecutados sin incidentes | [COMPLETAR] |
| Tiempo medio de resolución de incidentes | MTTR de incidentes críticos | [COMPLETAR] |
| Cumplimiento de pruebas de recuperación | Pruebas del art. 492 ejecutadas y aprobadas | 100 % anual |

### Control de cambios
| **Versión** | **Fecha** | **Cambio** | **Elaboró** | **Aprobó** |
|---|---|---|---|---|
| 0.1 | [COMPLETAR] | Versión inicial (borrador) | División TI | — |
| 1.0 | [COMPLETAR] | Aprobación de Gerencia General | División TI | Gerencia General |

## 5. Ejemplo aplicado al Banco (modelo de referencia)
Ejemplo ilustrativo de cómo quedaría completado. Adaptá a la realidad institucional del Banco.
**Organización (ejemplo):** la primera línea del Banco está en la División TI del Área Operaciones y TI: Producción opera la plataforma central (sistema de crédito, ahorro, Banco En Línea) con monitoreo 24x7; Sistemas desarrolla y mantiene las aplicaciones con el ciclo de desarrollo seguro; Soporte Técnico atiende a los más de [N] funcionarios y sucursales. El Departamento de Sistema de Pagos reporta a la División Operaciones y coordina con TI la calidad de servicio de pagos.
**Gestión de cambios (ejemplo):** la actualización del sistema central programada para [fecha] se gestionó por el Comité de Cambios: se analizó el impacto sobre el procesamiento de pagos del día, se aprobó con el visto bueno del RSI, se ejecutó en ventana nocturna con plan de retroceso y se registró el resultado. La no-conformidad detectada en la prueba dio lugar a la reprogramación, sin impacto en producción.
**Incidente técnico (ejemplo):** ante la caída del portal Banco En Línea de [fecha], Soporte escaló el incidente a Producción, que lo clasificó como severidad alta, restauró el servicio en [X] minutos dentro del RTO y derivó el análisis de causa raíz al RSI por tratarse de una posible causa de seguridad. Se actualizó el registro de incidentes y se reportó al Comité.
**Art. 492 (ejemplo):** Producción ejecuta el resguardo diario del sistema central con copias fuera del sitio, custodia las claves de desencriptación bajo doble control y participó en la prueba anual de recuperación de [fecha], que confirmó la recuperación íntegra de la información en [X] horas. El responsable del resguardo, de categoría superior, supervisó la prueba.

**Documentos relacionados:** BCU-01 (Gobierno), BCU-03 (Función de Seguridad), PR-05 (Respaldo y Recuperación), PR-06 (Vulnerabilidades), PR-07 (Desarrollo Seguro), DE-01 (Monitoreo), DE-02 (Anomalías), RC-02 (DRP), RS-01 (Incidentes).
