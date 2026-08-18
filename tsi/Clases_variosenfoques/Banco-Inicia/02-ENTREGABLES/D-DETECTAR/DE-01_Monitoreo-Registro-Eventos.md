# DE-01 · Política de Monitoreo y Registro de Eventos del Banco

> ⚠️ **Alerta:** este documento menciona **nombres propios del organigrama del Banco** (personas y cargos, abril 2026). Antes de usar el documento, verificá la vigencia de esos nombres contra el organigrama actual.
> **Función del MCU 5.0:** Detectar (DE.CM — Monitoreo continuo)
> **ISO/IEC 27001:** A.8.15 (Registro de eventos) · A.8.16 (Monitoreo de actividades)
> **BCU:** Circular 2280 (sistema de pagos) · RNRCSF art. 492 (resguardo de datos)
> **URCDP:** Ley 18.331 art. 10 (medidas de seguridad) · Decreto 64/020
> **Nivel del curso:** 🟡 Practicar

## 1. Qué es y por qué existe
La **Política de Monitoreo y Registro de Eventos** define qué eventos del entorno tecnológico del Banco se registran, cómo se centralizan, cuánto tiempo se retienen, quién puede acceder a ellos y cómo se protege su integridad. Es la base de la función **Detectar** del MCU 5.0: sin registros confiables no se pueden detectar a tiempo los incidentes, ni investigarlos, ni demostrar ante el BCU, Agesic o la URCDP que los controles funcionan.
En un banco que opera sistema de pagos y administra datos personales de cientos de miles de personas, los registros no son un costo: son **evidencia** del cumplimiento normativo y la materia prima del análisis forense ante una intrusión o un fraude. La Circular 2280 del BCU (sistema de pagos) y la RNRCSF (art. 492, resguardo de datos) exigen que la información pueda reconstruirse, y eso solo es posible si los registros son completos, íntegros y resguardados de forma que no se pierdan por el mismo evento que daña a los sistemas de producción.
Por último, esta política protege también a los funcionarios y clientes: el monitoreo se realiza con fines institucionales legítimos, se comunica, y el acceso a los registros se audita para evitar su uso indebido.
## 2. Marco de referencia
| **Norma** | **Referencia** | **Qué exige** |
|---|---|---|
| **MCU 5.0 (Agesic)** | DE.CM (Monitoreo continuo) | Monitoreo continuo del entorno y la red para detectar anomalías |
| **ISO/IEC 27001:2022** | A.8.15 / A.8.16 | Registrar eventos relevantes y monitorear las actividades para detectar incidentes |
| **BCU** | Circular 2280 · RNRCSF art. 492 | Resguardo de datos y registros del sistema de pagos; reconstrucción de operaciones |
| **URCDP** | Ley 18.331 art. 10 · Decreto 64/020 | Medidas de seguridad necesarias para evitar adulteración, pérdida o acceso no autorizado |

## 3. Cómo completar esta plantilla (guía de llenado)
1. **Definí el inventario de fuentes de eventos** con el Jefe de Departamento Producción (Ing. Daniel Herrera) y Sistemas (Lic. Cristian Palo): qué servidores, equipos de red, aplicaciones, bases de datos y endpoints generarán registros.
2. **Acordá los tiempos de retención** con Servicios Jurídicos Notariales y el DPD, respetando los plazos legales y los mínimos de auditoría (en general no menos de 6 a 12 meses para registros de seguridad, y los plazos contables/fiscales para registros de transacciones).
3. **Definí la plataforma SIEM** con la División TI: qué herramientas existen hoy y cuál se contratará para centralizar, correlacionar y alertar.
4. **Establecé la lista de acceso a logs** (quién lee, quién exporta, quién elimina) y aprobala con el RSI y el Comité de Seguridad.
5. **Pautá la sincronización de relojes** (NTP) y el mecanismo de integridad (firma de hash, WORM, registro de autoridad de cambios).
6. Consultá al **RSI** (Riesgos No Financieros) y al **Oficial de Cumplimiento** antes de fijar plazos mínimos de retención para operaciones de pago.
## 4. Plantilla del documento

### ENCABEZADO
| **Campo** | **Valor** |
|---|---|
| **Código** | DE-01 |
| **Título** | Política de Monitoreo y Registro de Eventos |
| **Versión** | 1.0 |
| **Estado** | [Borrador / En revisión / Aprobado] |
| **Fecha de aprobación** | [COMPLETAR] |
| **Elaborado por** | RSI |
| **Revisado por** | Comité de Seguridad de la Información |
| **Aprobado por** | Directorio |
| **Clasificación** | Uso interno |
| **Próxima revisión** | [Fecha, máx. 1 año] |

### 1. Objetivo
Garantizar que los eventos relevantes de los sistemas del Banco se registren de forma completa, íntegra y centralizada, de modo de detectar incidentes a tiempo, investigarlos y demostrar cumplimiento normativo.
### 2. Alcance
Aplica a [COMPLETAR: todos los sistemas de la División TI, sucursales, Banco En Línea, sistema de pagos, base de datos de clientes, y los servicios tecnológicos tercerizados]. Incluye eventos de seguridad, operación y transacciones.
### 3. Fuentes de registros
| **Fuente** | **Ejemplos de eventos a registrar** | **Responsable** |
|---|---|---|
| **Servidores** | Arranques, apagados, cambios de configuración, instalación de software, errores de sistema | Div. TI / Producción |
| **Red** | Flujos de red, conexiones bloqueadas, cambios en firewalls y routers | Div. TI |
| **Aplicaciones** | [COMPLETAR: Banco En Línea, core bancario, sistema de pagos]: autenticaciones, transacciones, errores de aplicación | Div. TI / Sistemas |
| **Base de datos** | Altas/bajas/modificaciones de registros, accesos administrativos, intentos fallidos | Div. TI |
| **Endpoints** | Inicios de sesión, procesos, dispositivos conectados, detecciones de antivirus/EDR | Div. TI / Soporte |
| **Accesos (IAM)** | [COMPLETAR: inicios de sesión exitosos y fallidos, cambios de privilegios, bloqueos de cuenta] | RSI + Div. TI |

### 4. Centralización y SIEM
[COMPLETAR: herramienta SIEM (ej. Wazuh, Splunk, Elastic, ArcSight)], flujo de envío de logs, filtros de eventos, y retención en el concentrador. Todo evento de seguridad se envía al SIEM en [COMPLETAR: tiempo máximo, ej. 5 minutos] y se correlaciona con las reglas de DE-02.
### 5. Retención de registros
| **Tipo de registro** | **Retención mínima** | **Fundamento** |
|---|---|---|
| Eventos de seguridad | [COMPLETAR: 12 meses] | Investigación y auditoría |
| Operaciones y transacciones | [COMPLETAR: según normativa BCU y contable] | Reconstrucción de operaciones |
| Accesos y autenticaciones | [COMPLETAR: 12 meses] | Control de accesos |
| Registros del sistema de pagos | [COMPLETAR: según Circular 2280] | BCU |

### 6. Integridad y resguardo de los registros
Los registros se firman/anoniman de forma de detectar alteraciones (hash, almacenamiento de solo escritura), y se resguardan conforme al art. 492 de la RNRCSF en un medio [COMPLETAR: separado del sitio primario], con claves de desencriptación custodiadas por [COMPLETAR: rol].
### 7. Gestión de relojes
Todos los sistemas sincronizan su reloj contra una fuente NTP autorizada por la División TI, con tolerancia máxima de [COMPLETAR: 2 segundos], para que los registros sean ordenables y admisibles como evidencia.
### 8. Acceso a los registros
[COMPLETAR: roles autorizados: administradores del SIEM, RSI, oficiales de la División TI; cada acceso se registra y audita]. Prohibido leer logs de clientes sin base legal. Se aplica el principio de mínimo privilegio.
### 9. Control de cambios
| **Versión** | **Fecha** | **Cambio** | **Elaboró** | **Aprobó** |
|---|---|---|---|---|
| 0.1 | [COMPLETAR] | Versión inicial (borrador) | RSI | — |
| 1.0 | [COMPLETAR] | Aprobación del Directorio | RSI | Directorio |

## 5. Ejemplo aplicado al Banco (modelo de referencia)
Ejemplo ilustrativo. Adaptá a la infraestructura real y a los nombres vigentes del organigrama.
**Fuentes registradas (ejemplo):**
- Servidores: Core bancario, Banco En Línea, autenticadores, correo interno.
- Red: firewalls perimetrales, VPN de acceso remoto, conmutadores de sucursales.
- Aplicaciones: Banco En Línea, sistema de pagos (Dpto. Sistema de Pagos, Cr. Guillermo Correa), homebanking y app móvil.
- Bases de datos: SGBD de clientes y de préstamos hipotecarios.
- Endpoints: estaciones de trabajo con EDR del Dpto. Soporte Técnico (Tec. Ariel Presa).
- Accesos: IAM corporativo, directorio activo y puntos de venta de sucursales.
**Retención (ejemplo):** 12 meses para eventos de seguridad y accesos; 10 años para registros contables de operaciones de préstamo conforme a la normativa aplicable; plazos de la Circular 2280 para el sistema de pagos.
**Integridad y resguardo (ejemplo):** el SIEM escribe los registros en almacenamiento de solo adición (append-only); se calcula un hash por bloque de registros; diariamente se replica a la cinta/bóveda de respaldo que se custodia en sitio alternativo con claves separadas, cumpliendo el art. 492 de la RNRCSF.
**Relojes (ejemplo):** NTP autorizado sincronizado contra el servicio horario nacional; tolerancia de 2 segundos.
**Acceso (ejemplo):** solo el administrador del SIEM y el RSI leen los registros; el Oficial de Cumplimiento puede solicitar exportaciones fundadas; toda consulta queda logueada y se audita semestralmente por Auditoría Interna (Cr. Marcelo Jorge).

**Documentos relacionados:**
- DE-02 (Detección de Anomalías e Intrusiones)
- RS-01 (Respuesta a Incidentes) · RS-03 (Forense y Evidencia)
- PR-05 (Respaldo y Recuperación) · RC-02 (DRP)
- BCU-04 (Gestión TI) · URCDP-01 (Documento de Seguridad de Datos)
