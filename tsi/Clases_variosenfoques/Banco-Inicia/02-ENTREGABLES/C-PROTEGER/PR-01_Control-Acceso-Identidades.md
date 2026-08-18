# PR-01 · Política de Control de Acceso y Gestión de Identidades del Banco
> **Función del MCU 5.0:** Proteger (PR.AA — Gestión de identidades, credenciales y acceso)
> **ISO/IEC 27001:** A.5.15 (Control de acceso) · A.8.2 (Derechos de acceso privilegiado) · A.8.5 (Gestión de autenticación de usuarios)
> **BCU:** Estándares Mínimos de Gestión — Riesgo tecnológico; RNRCSF art. 492
> **URCDP:** Ley 18.331 art. 10 (medidas de seguridad) · Decreto 64/020
> **Nivel del curso:** 🟡 Practicar · 🔴 Dominar

## 1. Qué es y por qué existe
El **control de acceso** es la primera línea de defensa de un banco: garantiza que cada persona, sistema o proceso solo acceda a los datos y recursos que necesita para cumplir su función. Una gestión deficiente de identidades es la puerta de entrada de la mayor parte de los incidentes internos y externos (cuentas de exfuncionarios que siguen activas, credenciales compartidas, privilegios excesivos que un atacante aprovecha tras comprometer una cuenta).
Esta política define cómo el Banco administra el **ciclo de vida completo de las identidades** (alta, modificación, baja), cómo se asignan los permisos bajo el **principio de menor privilegio**, cómo se autentican los usuarios y cómo se revisan periódicamente los accesos para que nadie tenga más de lo que le corresponde. Sin esta política, las áreas de Sistemas y de Riesgos operarían sin reglas comunes y el banco no podría demostrar ante el BCU, Agesic o la URCDP que controla quién accede a qué.
En el Banco, que custodia el ahorro de miles de familias uruguayas y opera el **core bancario hipotecario**, el **Banco En Línea**, el **sistema de pagos** y bases de datos personales, cada cuenta es un activo. Esta política es obligatoria para funcionarios, contratistas, terceros y cualquier sistema que se conecte a la red del banco, incluso de forma remota.
## 2. Marco de referencia
| **Referencia** | **Requisito aplicable** |
|---|---|
| **MCU 5.0 (Agesic)** | PR.AA — gestión de identidades, credenciales y acceso según perfil; autenticación robusta; revisión de derechos de acceso |
| **ISO/IEC 27001:2022** | A.5.15 control de acceso; A.8.2 acceso privilegiado; A.8.3 restricción de información; A.8.5 autenticación segura; A.8.18 protección de código malicioso |
| **BCU** | EMG · Riesgo tecnológico (gestión de accesos como control crítico); RNRCSF art. 492; Circular 2280 (seguridad del sistema de pagos) |
| **URCDP** | Ley 18.331 art. 10 (medidas de seguridad que garanticen confidencialidad e integridad); Decreto 64/020 art. 21 (medidas técnicas de seguridad) |

## 3. Cómo completar esta plantilla (guía de llenado)
1. **Completá el encabezado** (código, versión, fecha de aprobación). La versión 1.0 la aprueba el Comité de Seguridad de la Información a propuesta del RSI.
2. **Definí con el Área Operaciones y TI** (División TI: Jefes de Sistemas, Producción y Soporte) cuáles son los sistemas críticos a proteger: core bancario, Banco En Línea, sistema de pagos, herramientas de administración.
3. **Coordiná con el Departamento de Información y Apoyo Comercial** y con **División Capital Humano** los procedimientos de alta y baja de funcionarios (el "evento de RRHH" dispara el alta/baja de cuentas).
4. **Personalizá los apartados [COMPLETAR]** con los tiempos reales de revisión de accesos (se recomienda revisión trimestral para cuentas privilegiadas).
5. **Definí la matriz de roles y perfiles** (apartado 4.4) con el Jefe de Riesgos No Financieros y el Oficial de Cumplimiento, para garantizar separación de funciones.
6. **Aprobá, registrá el cambio en el control de cambios** y publicá en la carpeta `02-ENTREGABLES/C-PROTEGER`. Revisá al menos cada año o ante cambios de estructura orgánica.
## 4. Plantilla del documento

### ENCABEZADO
| **Campo** | **Valor** |
|---|---|
| **Código** | PR-01 |
| **Título** | Política de Control de Acceso y Gestión de Identidades |
| **Versión** | 1.0 |
| **Estado** | [Borrador / En revisión / Aprobado] |
| **Fecha de aprobación** | [COMPLETAR] |
| **Elaborado por** | RSI |
| **Revisado por** | Comité de Seguridad de la Información |
| **Aprobado por** | Comité de Seguridad de la Información |
| **Clasificación** | Uso interno |
| **Próxima revisión** | [Fecha, máx. 1 año] |

### 1. Objetivo
Establecer las reglas para garantizar que el acceso a la información y a los sistemas del Banco sea **autorizado, trazable y revocable**, mediante una gestión ordenada del ciclo de vida de las identidades y la aplicación del principio de menor privilegio.
### 2. Alcance
Aplica a [COMPLETAR: todos los funcionarios, contratistas, pasantes, proveedores y terceros que accedan a los sistemas o instalaciones del Banco; a todas las identidades lógicas (usuarios de red, aplicaciones, base de datos, correo, Banco En Línea) y cuentas de servicio]. Aplica también a los accesos remotos y a los sistemas administrados por terceros que procesen datos del banco.
### 3. Principios
a) **Menor privilegio:** cada usuario recibe solo los permisos necesarios para su función.
b) **Uso individual:** las credenciales son personales e intransferibles; está prohibido compartirlas.
c) **Ciclo de vida gestionado:** toda identidad se crea, modifica y elimina a partir de un evento formal (ingreso, cambio de función, egreso).
d) **Trazabilidad:** toda acción sobre los sistemas debe poder atribuirse a una identidad.
e) **Separación de funciones:** ninguna persona debe concentrar funciones incompatibles (p. ej., autorizar y ejecutar pagos).
### 4. Gestión del ciclo de vida de las identidades
| **Etapa** | **Responsable** | **Regla** |
|---|---|---|
| **Alta** | Div. TI + Capital Humano | Solo con solicitud firmada del jefe del área; identidad única por persona |
| **Modificación** | Div. TI | Cuando cambia la función; se ajustan roles y perfiles |
| **Baja** | Div. TI + Capital Humano | Inmediata al egreso o sanción; se desactiva el mismo día |
| **Reactivación** | Div. TI | Solo con nueva solicitud justificada |

### 4.1. Registro de altas y bajas
Se mantiene un **registro centralizado de identidades** [COMPLETAR: herramienta de gestión de identidades y accesos (IAM) o directorio activo]. La baja de un funcionario se notifica el mismo día del egreso y el acceso se revoca en el plazo máximo de [COMPLETAR: 24 horas].
### 4.2. Autenticación
- Todo acceso requiere **identificación y autenticación** con credenciales individuales.
- Contraseñas: longitud mínima de [COMPLETAR: 12 caracteres], complejidad, prohibición de reutilización de las últimas [COMPLETAR: 5] contraseñas y rotación según riesgo.
- **MFA obligatorio** para: accesos privilegiados, accesos remotos, administración del core bancario y del sistema de pagos.
- Se bloquea la cuenta tras [COMPLETAR: 5] intentos fallidos con procedimiento de desbloqueo controlado.
### 4.3. Cuentas privilegiadas
- Se listan todas las cuentas con privilegios de administrador (sistema, base de datos, red, aplicaciones) en un **registro de cuentas privilegiadas**.
- Se usan cuentas de administración **separadas de las cuentas de uso diario** (cuenta "de trabajo" sin privilegios + cuenta de administración).
- Idealmente se usa una **bóveda de credenciales privilegiadas** (Password Vault) con registro de cada uso.
- Las credenciales privilegiadas se rotan al menos cada [COMPLETAR: 90 días] y ante sospecha de compromiso.
### 4.4. Roles y perfiles de acceso
El Banco define **perfiles tipo** según función (operador de sucursal, oficial de crédito, administrador de sistemas, contador, auditor, etc.) en una matriz de roles aprobada por el Comité. Se aplica **separación de funciones** en los procesos de alta exposición (pagos, aprobación de créditos, modificaciones de parámetros del core).
| **Perfil** | **Sistemas** | **Permisos** | **Criticidad** |
|---|---|---|---|
| [COMPLETAR] | [COMPLETAR] | [COMPLETAR] | [Alta/Media/Baja] |

### 4.5. Revisión periódica de accesos
- Revisión de accesos **privilegiados**: cada [COMPLETAR: 90 días], por el dueño del activo junto con Div. TI.
- Revisión de accesos **de usuarios**: al menos cada [COMPLETAR: 6 meses], por cada jefe de departamento sobre su equipo.
- El resultado se documenta y las cuentas sin justificar se desactivan en [COMPLETAR: 5 días hábiles].
### 4.6. Acceso remoto
- Solo mediante **VPN con MFA** y conexiones cifradas.
- Autorizado por el jefe de departamento y habilitado por Div. TI.
- Prohibido para tareas que no tengan autorización explícita; se registra la sesión [COMPLETAR: sí/no y herramienta].
### 4.7. Responsabilidades
| **Rol** | **Responsabilidad** |
|---|---|
| **Dueño del activo (área usuaria)** | Definir y aprobar los accesos de su equipo; revisión periódica |
| **Div. TI** | Implementar, administrar y revocar los accesos; gestión técnica de identidades |
| **RSI** | Supervisar el cumplimiento, analizar excepciones y reportar al Comité |
| **Div. Capital Humano** | Notificar altas, modificaciones y bajas del personal |
| **Auditoría Interna** | Evaluar periódicamente la efectividad del control de accesos |

### 5. Cumplimiento y excepciones
Toda excepción requiere la aprobación del dueño del activo y del RSI, con **fecha de vencimiento** y mitigaciones compensatorias. El incumplimiento se trata según el régimen disciplinario del Banco.
### 6. Control de cambios
| **Versión** | **Fecha** | **Cambio** | **Elaboró** | **Aprobó** |
|---|---|---|---|---|
| 0.1 | [COMPLETAR] | Versión inicial (borrador) | RSI | — |
| 1.0 | [COMPLETAR] | Aprobación del Comité | RSI | Comité |

## 5. Ejemplo aplicado al Banco (modelo de referencia)
Ejemplo ilustrativo de cómo quedaría el apartado 4 completado. Adaptá al contenido institucional real del Banco.
**Autenticación (ejemplo):**
- Los funcionarios de sucursal acceden al core con usuario individual + contraseña de 12 caracteres y, para operaciones de alta sensibilidad, segundo factor.
- Los administradores de la Div. TI que gestionan el core bancario y el sistema de pagos usan **MFA con token o llave física (hardware)**. Los accesos remotos de desarrollo y soporte (incluidos proveedores) exigen **VPN + MFA** y se auditan mensualmente.
- Las cuentas de servicio de integración entre sistemas (core → sistema de pagos → Banco En Línea) están registradas, con contraseñas rotadas cada 90 días y almacenadas en la bóveda de credenciales.
**Separación de funciones (ejemplo):**
- Un jefe de departamento de la Div. Operaciones puede **cargar** una transferencia del sistema de pagos, pero la **autorización** de pago exige una identidad distinta (segundo firmante). El oficial de crédito aprueba el préstamo pero no puede modificarlo luego del desembolso sin permiso de la Div. Sistemas.
- Los auditores internos disponen de perfiles de **solo lectura** y sus sesiones se registran por separado para preservar la independencia de la tercera línea.
**Revisión de accesos (ejemplo):**
- Cada 90 días el Gerente de Div. TI revisa con el RSI las cuentas privilegiadas; en 2026 se detectó que una cuenta de administración de un ex-proveedor seguía activa: se desactivó en el día y se corrigió el procedimiento de baja para terceros, acorde con PR-08.

**Documentos relacionados:** GV-01 (Política de Seguridad), ID-01 (Inventario de Activos), ID-02/03 (Riesgos), PR-04 (Seguridad Física), PR-08 (Confidencialidad y Terceros), RS-01 (Incidentes), DE-01 (Monitoreo y Registro).
