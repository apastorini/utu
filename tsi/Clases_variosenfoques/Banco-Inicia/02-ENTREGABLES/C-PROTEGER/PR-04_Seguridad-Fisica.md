# PR-04 · Política de Seguridad Física y del Entorno del Banco

> ⚠️ **Alerta:** este documento menciona **nombres propios del organigrama del Banco** (personas y cargos, abril 2026). Antes de usar el documento, verificá la vigencia de esos nombres contra el organigrama actual.
> **Función del MCU 5.0:** Proteger (PR.AA-06 — Control de acceso físico · PR.PS — Seguridad de plataformas)
> **ISO/IEC 27001:** A.7.1 (Perímetros de seguridad física) · A.7.2 (Ingreso físico) · A.7.3 (Seguridad de oficinas, salas y recursos) · A.7.4 (Monitoreo físico) · A.7.5 (Amenazas físicas y ambientales) · A.7.6 (Trabajo en áreas seguras) · A.7.7 (Escritorio y pantalla limpios)
> **BCU:** RNRCSF · RENAEMSE (resguardo de valores) · EMG · Riesgo tecnológico
> **URCDP:** Ley 18.331 art. 10 · Decreto 64/020 (medidas físicas; videovigilancia con cartelería e inscripción de bases)
> **Nivel del curso:** 🟢 Descubrir · 🟡 Practicar

## 1. Qué es y por qué existe
La seguridad lógica no sirve de nada si un intruso entra al **datacenter** y roba un servidor, o si un incendio en la sala de cómputo destruye el core bancario. La **seguridad física y del entorno** protege a las personas, los activos y las instalaciones del Banco contra amenazas como accesos no autorizados, robo, sabotaje, incendio, inundación y fallas ambientales. Es el complemento indispensable de PR-01 y PR-03.
Esta política define los **perímetros de seguridad** (datacenter, salas de cómputo, sucursales, bóvedas), las reglas de **control de ingreso**, el uso de **videovigilancia** (cumpliendo la normativa de la URCDP: cartelería informativa e inscripción de las bases en el registro de la URCDP), la **protección contra incendios, agua y clima**, la **gestión de activos físicos** (equipos, documentos, dinero), el **escritorio limpio** y el tratamiento de **visitas y contratistas**.
En el Banco la seguridad física tiene dos caras: la bancaria tradicional (bóvedas, valores, efectivo en sucursales, custodia de documentos de crédito) y la tecnológica (datacenter, sala de cómputo, respaldos). Ambas conviven bajo las mismas reglas y se coordinan entre el **Departamento de Servicios Generales** y la División de TI.
## 2. Marco de referencia
| **Referencia** | **Requisito aplicable** |
|---|---|
| **MCU 5.0 (Agesic)** | PR.AA-06 — control de acceso físico; PR.PS — seguridad de plataformas (instalaciones críticas) |
| **ISO/IEC 27001:2022** | A.7.1 a A.7.7 (perímetros, ingreso, oficinas, monitoreo, amenazas ambientales, áreas seguras, escritorio limpio) |
| **BCU** | RNRCSF y RENAEMSE (resguardo físico de valores y documentos); EMG · Riesgo tecnológico |
| **URCDP** | Ley 18.331 art. 10; Decreto 64/020 (medidas físicas); videovigilancia: cartelería (Ley 18.331) e inscripción de bases de datos (art. 22, D.414/009) |

## 3. Cómo completar esta plantilla (guía de llenado)
1. **Completá el encabezado** (código, versión, fecha). La aprueba el Comité de Seguridad de la Información.
2. **Levantá el inventario de instalaciones** con el Departamento de Servicios Generales (Ing. Agustín Araujo) y la Div. Operaciones: datacenter, sala de cómputo, sucursales, archivos, bóvedas.
3. **Definí con el DPD** el tratamiento de la videovigilancia: cartelería visible, inscripción de las bases y plazos de retención de imágenes.
4. **Personalizá los apartados [COMPLETAR]** con los perímetros reales, horarios y responsables por sede.
5. **Coordiná con Riesgos No Financieros** la evaluación de amenazas físicas (incendio, inundación, entorno de la sede central).
6. **Aprobá, registrá en el control de cambios** y publicá en `02-ENTREGABLES/C-PROTEGER`. Revisá anualmente.
## 4. Plantilla del documento

### ENCABEZADO
| **Campo** | **Valor** |
|---|---|
| **Código** | PR-04 |
| **Título** | Política de Seguridad Física y del Entorno |
| **Versión** | 1.0 |
| **Estado** | [Borrador / En revisión / Aprobado] |
| **Fecha de aprobación** | [COMPLETAR] |
| **Elaborado por** | RSI |
| **Revisado por** | Depto. Servicios Generales · Div. TI · DPD · Comité de Seguridad |
| **Aprobado por** | Comité de Seguridad de la Información |
| **Clasificación** | Uso interno |
| **Próxima revisión** | [Fecha, máx. 1 año] |

### 1. Objetivo
Proteger las personas, los activos de información y las instalaciones del Banco contra accesos físicos no autorizados, daños, robo y amenazas ambientales, garantizando la continuidad de las operaciones y el cumplimiento normativo.
### 2. Alcance
Aplica a [COMPLETAR: todas las instalaciones del Banco —sede central, sucursales, datacenter, salas de cómputo, archivos y bóvedas— y a todos los activos físicos que contienen información: servidores, equipos de red, terminales, documentos, medios extraíbles y valores]. Aplica también a funcionarios, visitas, contratistas y proveedores que ingresen a dichas instalaciones.
### 3. Perímetros de seguridad y zonas
| **Zona** | **Instalaciones** | **Nivel de protección** |
|---|---|---|
| **Pública** | Hall de atención, zona de cajeros | Control de acceso mínimo, videovigilancia |
| **Operativa** | Oficinas, sucursales, archivo | Ingreso con credencial, registro de visitas |
| **Restringida** | Sala de cómputo, datacenter, bóvedas | Doble factor físico, registro y trazabilidad, acceso por autorización expresa |

### 3.1. Perímetro del datacenter y la sala de cómputo
- Cerramiento con **puertas de acceso controlado** (tarjeta o biométrica), pisos técnicos sellados y detección de apertura.
- Acceso solo para personal autorizado de la Div. TI y mantenimiento certificado, con **registro de cada ingreso**.
- Las **sucursales** cuentan con zonas de atención con vidrios de seguridad y cajeros protegidos.
### 4. Control de ingreso
- Todo funcionario usa **credencial institucional** para ingresar a zonas operativas.
- **Visitas y contratistas:** registro en la recepción, identificación con documento, **acompañamiento permanente** en zonas restringidas y firma del acuerdo de confidencialidad (PR-08).
- Los accesos físicos se **revocan** al egreso o cambio de función, en coordinación con Capital Humano y PR-01.
### 5. Videovigilancia
- Cámaras en: perímetro, recepción, zonas de cajeros, acceso al datacenter y bóvedas [COMPLETAR: ubicación exacta].
- **Cumplimiento URCDP:** cartelería visible que informa la existencia de videovigilancia; las imágenes son una base de datos **inscrita en el registro de la URCDP** (URCDP-04).
- Retención de imágenes: [COMPLETAR: 30 días] salvo requerimiento judicial o de auditoría.
- Las imágenes solo se consultan con autorización (RSI, Seguridad, Auditoría, Justicia) y queda registro del acceso.
### 6. Protección contra incendios, agua y clima
- **Detección y extinción:** detectores de humo y sistemas de extinción (gas limpio) en el datacenter; matafuegos según norma en todas las instalaciones [COMPLETAR: empresa de mantenimiento].
- **Agua:** el datacenter se ubica lejos de cañerías, con detección de fugas y piso técnico impermeable.
- **Clima:** aire acondicionado de precisión con monitoreo de temperatura y humedad y alarmas al personal de Producción.
- Inspección y pruebas de sistemas contra incendio: al menos [COMPLETAR: 2 veces al año].
### 7. Gestión de activos físicos
- Equipos: alta y baja registradas; los equipos fuera de servicio se **borran de forma segura** (PR-03) antes de retirarlos.
- Documentos: los de clase "Confidencial" y "Secreto" se archivan en **armarios con llave o bóveda** y se destruyen de forma certificada.
- Medios extraíbles: prohibidos en zonas restringidas salvo autorización; se registran entradas y salidas.
### 8. Escritorio y pantalla limpios
- Al retirarse, todo funcionario **bloquea su pantalla** (Ctrl+Alt+Supr / Win+L) y retira documentos confidenciales.
- No quedan documentos "Confidencial" o "Secreto" a la vista ni impresiones desatendidas al final de la jornada.
### 9. Responsabilidades
| **Rol** | **Responsabilidad** |
|---|---|
| **Depto. Servicios Generales** | Perímetros, control de acceso físico, mantenimiento, videovigilancia |
| **Div. TI (Producción)** | Seguridad del datacenter, ambiente, acceso a sala de cómputo |
| **RSI** | Supervisión, autorización de excepciones, revisión de accesos físicos |
| **DPD** | Cumplimiento URCDP de la videovigilancia |
| **Jefes de sucursal** | Aplicación de la política en cada sucursal |

### 10. Control de cambios
| **Versión** | **Fecha** | **Cambio** | **Elaboró** | **Aprobó** |
|---|---|---|---|---|
| 0.1 | [COMPLETAR] | Versión inicial (borrador) | RSI | — |
| 1.0 | [COMPLETAR] | Aprobación del Comité | RSI | Comité |

## 5. Ejemplo aplicado al Banco (modelo de referencia)
Ejemplo ilustrativo de cómo quedaría el apartado 4 completado. Adaptá al contenido institucional real del Banco.
**Perímetro del datacenter (ejemplo):**
- El datacenter del Banco cuenta con puerta con **tarjeta + PIN** (doble factor físico), registro automático de ingresos y **videovigilancia con cartelería** visible. Solo ingresan los administradores de Producción autorizados y el técnico de mantenimiento de climatización, acompañados.
- En 2026 se hizo la prueba anual de simulacro de incendio: el sistema de gas limpio se activó en la zona de prueba y el corte de energía de respaldo (UPS + generador) se verificó sin afectar el core bancario.
**Videovigilancia y URCDP (ejemplo):**
- La sucursal central instaló cámaras nuevas en la zona de cajeros con **cartel informativo** aprobado por el DPD; la base de imágenes se inscribió ante la URCDP y se fijó retención de 30 días. Los accesos al video quedan registrados en bitácora y se controlan trimestralmente.
**Escritorio limpio (ejemplo):**
- Los expedientes de crédito en trámite (clase "Confidencial") se guardan en archivadores con llave al cierre; los terminales de sucursal se bloquean automáticamente a los 5 minutos de inactividad. Las impresoras de red no emiten documentos sin que el funcionario autorizado los retire.

**Documentos relacionados:** GV-01 (Política de Seguridad), PR-01 (Control de Acceso), PR-03 (Seguridad de Datos), PR-05 (Respaldo), PR-08 (Terceros), URCDP-04 (Inscripción de Bases), ID-01 (Inventario de Activos).
