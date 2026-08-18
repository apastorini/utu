# RELEV-04 · El dossier por división: qué relevar de cada área

> ⚠️ **Alerta:** este documento menciona **nombres propios del organigrama del Banco** (personas y cargos, abril 2026). Antes de usar el documento, verificá la vigencia de esos nombres contra el organigrama actual.

> **Función del MCU 5.0:** ID.AM Inventario de activos · ID.RA Evaluación de riesgos · DE.CM Monitoreo continuo · PR.DS Protección de datos.
> **ISO/IEC 27001:** A.5 Alcance · A.5.2 Roles · A.5.9 Inventario de activos · A.5.10 Uso aceptable · A.8.1 Responsabilidades · A.8.2 Clasificación de la información · A.5.15 Accesos · A.5.14 Transferencia de información · A.7 Seguridad física.
> **BCU:** RNRCSF art. 492 (resguardo de datos/software/documentación, copias no afectadas por el mismo evento, claves de desencriptación independientes, pruebas anuales de recuperación e integridad) · Circular 2227 (riesgo operacional) · Comunicación 2022/254 (tercerización en el exterior).
> **URCDP:** Ley 18.331 · Ley 19.670 (art. 38 notificación de vulneraciones: URCDP 24 h, titulares 72 h) · Decreto 64/020 · EIPD · Inscripción de bases (URCDP-04).
> **Nivel del curso:** 🔴 Dominar

---

> **Verificar contra el organigrama vigente** (PDF SF.PLE.05, abril 2026): https://www.bhu.com.uy/sobre-bhu/organigrama

---

## 1. Para qué sirve este dossier

Este módulo es **el corazón práctico del relevamiento**: es la lista de cosas que tenés que ir a buscar, preguntar y evidenciar en cada división del Banco. No es un documento teórico: es un **kit de campo**. Lo llevás a cada reunión, lo marcás, lo vas completando.

### 1.1 Qué resuelve

| Problema típico | Cómo lo resuelve este dossier |
|---|---|
| "No sé qué preguntar cuando entro a una reunión" | Cada área tiene su checklist de preguntas listas para decir |
| "Me llevo de todo y después no sé qué es relevante" | Cada área termina con las evidencias mínimas y su formato |
| "No conozco los sistemas de esa división" | Cada área lista los activos típicos (bases, sistemas, infraestructura) |
| "El jefe del área me mira como si viniera de otro planeta" | Cada área dice con quién hablar y qué le importa |
| "Me pierdo con tantas bases de datos" | El Cuestionario de Bases de Datos (sección 16) estandariza el relevamiento |

### 1.2 Cómo usar este documento

1. Antes de la reunión: leé la subsección del área y marcá con ☐ las preguntas que aplicarás.
2. Durante la reunión: hacé las preguntas **exactas** del checklist y anotá la respuesta al lado.
3. Después: pedí las evidencias enumeradas y guardalas en `EST-CARPETAS-001`.
4. Al final del día: **una base de datos = una fila del cuestionario de la sección 16**.

> Regla de oro: **todo lo que no esté escrito, no existe.** Las evidencias son el idioma que entienden TI, Riesgos, Auditoría y el BCU.

### 1.3 Los tres productos que salen de este dossier

| Producto | De qué parte del dossier sale |
|---|---|
| ID-01 Inventario de Activos | De las columnas "activos típicos" + sección 16 |
| ID-03 Análisis de Riesgos | De las preguntas de cada área + sensibilidades de datos |
| URCDP-01 Documento de Seguridad / URCDP-04 Inscripción de bases | Del cuestionario de bases de datos (sección 16) |

---

## 2. Antes de empezar: el kit mínimo por reunión

☐ Este dossier impreso o en pantalla con la sección del área.
☐ Cuaderno / libreta única para anotaciones (nada de papeles sueltos).
☐ El Cuestionario de Bases de Datos (sección 16) en blanco.
☐ Formato de minuta (fecha, asistentes, acuerdos, pendientes).
☐ Carpeta digital del área en `EST-CARPETAS-001` ya creada.
☐ Autorización formal del sponsor (GV-03) para pedir evidencias.
☐ Tarjeta con el guion de apertura del RELEV-05 por si la reunión se pone tensa.

---

## 3. División TI — Depto. Producción

### 3.1 Qué hace el área

Administra la operación de los servidores y el ambiente productivo, incluyendo el mainframe/núcleo central y el resguardo de la información. Garantiza que el banco funcione 24x7 y que las copias de respaldo estén protegidas y sean recuperables.

### 3.2 Activos típicos

- Servidores físicos y virtuales (inventario completo con roles y ubicación).
- Mainframe / core bancario (sistema central de operaciones).
- Ambientes productivos, de pruebas y desarrollo.
- Sistemas de respaldo (backups) y medios magnéticos/cintas.
- Sistema de monitoreo 24x7 (alertas, consolas, turnos).
- Energía, climatización y accesos físicos del datacenter.
- Archivos físicos y documentación de operación.

### 3.3 Preguntas de relevamiento (checklist)

☐ ¿Cuál es el inventario completo de servidores físicos y virtuales y quién lo mantiene?
☐ ¿Qué sistemas críticos corren en cada servidor (core, pagos, web, correo)?
☐ ¿Dónde se resguardan los datos y con qué periodicidad?
☐ ¿Las copias de respaldo residen en ubicaciones no afectadas por el mismo evento (art. 492)?
☐ ¿Las claves de desencriptación de los respaldos están guardadas de forma independiente de las copias?
☐ ¿Cuándo fue la última prueba anual de recuperación e integridad de la totalidad de los datos?
☐ ¿Quién firma y aprueba el resultado de esas pruebas de restauración?
☐ ¿Cómo se monitorea la operación 24x7 y qué se registra?
☐ ¿Qué disponibilidad tienen los sistemas críticos y cómo se mide?
☐ ¿Cómo se gestionan las incidencias de producción y quién decide la escalada?
☐ ¿Qué eventos de mantenimiento dejan registro y con qué trazabilidad?
☐ ¿Existe un procedimiento documentado de respaldo y restauración (PR-05)?

### 3.4 Evidencias a pedir

| Evidencia | Formato sugerido |
|---|---|
| Inventario de servidores | XLSX con rol, ubicación física/lógica, SO, criticidad |
| Política / procedimiento de backup | DOCX o PDF vigente con fecha |
| Registros de pruebas de restauración | PDF de acta con fecha, responsable y resultado |
| Reportes de disponibilidad | PDF/XLSX mensual (uptime por sistema) |
| Planos o esquema del datacenter | PDF/CAD con zonas de acceso |

### 3.5 Con quién hablar

**Ing. Daniel Herrera** (Jefe de Depto. Producción) — operación y resguardos. **Lic. Bernardo Ureta** (División TI) — para autorizar acceso a evidencias sensibles.

### 3.6 Particularidades y trampas

- **Trampa del backup teórico:** te muestran la política pero no los registros de prueba. El art. 492 exige prueba anual de la totalidad. Pedí el acta con fecha.
- **Trampa de la misma sala:** copias "en dos racks" del mismo datacenter no cumplen el art. 492 (mismo evento). Preguntá si hay sitio remoto.
- **Trampa de las claves:** si las claves de desencriptación están junto a las cintas, el resguardo no sirve. Preguntá quién las custodia.
- El mainframe suele ser el activo más crítico: si no sabés si el core es un mainframe, preguntá "¿cuál es el sistema que no puede caerse nunca?".

---

## 4. División TI — Depto. Sistemas

### 4.1 Qué hace el área

Desarrolla, mantiene y administra las aplicaciones del banco: el core, Banco En Línea, el sistema de pagos, contabilidad, CRM y demás sistemas internos. Gestiona la base de datos y el ciclo de vida del software.

### 4.2 Activos típicos

- Core bancario (aplicación principal de negocio).
- Banco En Línea (canal web/app para clientes).
- Sistema de pagos interbancarios.
- Sistema de contabilidad y tesorería.
- CRM / sistema comercial.
- Gestores de bases de datos (Oracle, SQL Server, etc.) con sus bases.
- Repositorio de código y herramientas de desarrollo.
- Sistemas de prueba (entornos QA) y de desarrollo.

### 4.3 Preguntas de relevamiento (checklist)

☐ ¿Cuál es el inventario completo de aplicaciones del banco?
☐ ¿Qué versión tiene cada aplicación y quién la actualiza?
☐ ¿Qué bases de datos existen, qué contienen y quién es su administrador?
☐ ¿Cómo se gestiona el proceso de desarrollo seguro (PR-07) y quién lo revisa?
☐ ¿Cómo se hacen los despliegues a producción y quién los autoriza?
☐ ¿Qué accesos a bases de datos tienen los desarrolladores (producción incluida)?
☐ ¿Cómo se manejan las credenciales y las contraseñas de sistemas?
☐ ¿Banco En Línea está conectado a qué sistemas de respaldo y cómo se autentica a los clientes?
☐ ¿Qué datos personales de clientes maneja cada sistema (para EIPD URCDP-05)?
☐ ¿Existe inventario de API y de integraciones entre sistemas?
☐ ¿Cómo se documentan las aplicaciones y su arquitectura?
☐ ¿Qué controles de cifrado en tránsito y en reposo tienen las bases (PR-03)?

### 4.4 Evidencias a pedir

| Evidencia | Formato sugerido |
|---|---|
| Inventario de aplicaciones y versiones | XLSX con sistema, versión, responsable, criticidad |
| Inventario de bases de datos | XLSX con nombre, sistema, ubicación, administrador |
| Proceso de desarrollo y despliegue | DOCX/PDF (etapas, aprobaciones, QA) |
| Matriz de accesos a bases y sistemas | XLSX con usuario, sistema, rol, fecha |
| Diagrama de arquitectura y APIs | PDF / Visio / DrawIO |

### 4.5 Con quién hablar

**Lic. Cristian Palo** (Jefe de Depto. Sistemas) — aplicaciones y bases. **Lic. Bernardo Ureta** (División TI) — visión transversal.

### 4.6 Particularidades y trampas

- **Trampa de la sombra:** hay sistemas que nadie inventarió ("eso lo hizo un consultor hace años"). Preguntá por aplicaciones "históricas o en planilla".
- **Trampa de los desarrolladores con acceso a producción:** es el clásico hallazgo de auditoría. Preguntá quién puede consultar/modificar datos en producción y por qué.
- **Trampa de las copias de bases:** los backups de desarrollo suelen tener datos reales de clientes sin proteger. Preguntá qué contienen los ambientes de prueba.
- Banco En Línea es el activo con más superficie de ataque pública: cruzá su relevamiento con el curso INFRA.

---

## 5. División TI — Depto. Soporte Técnico

### 5.1 Qué hace el área

Gestiona los equipos de los usuarios (endpoints), la mesa de ayuda, el parcheo de sistemas, el antivirus/EDR y las altas, bajas y modificaciones de accesos. Es la primera línea de la operación de seguridad.

### 5.2 Activos típicos

- Estaciones de trabajo (PCs) y notebooks del personal.
- Servidores de dominio / directorio activo (usuarios y grupos).
- Antivirus / EDR y consola de gestión.
- Sistema de parcheo y despliegue de software.
- Mesa de ayuda / servicio de tickets.
- Proceso de altas y bajas de acceso (PR-01).
- Herramientas de inventario de hardware y software.

### 5.3 Preguntas de relevamiento (checklist)

☐ ¿Cómo se inventarían los endpoints y cuántos hay en total?
☐ ¿Qué cobertura de antivirus/EDR tienen los equipos y cómo se verifica?
☐ ¿Cómo y con qué periodicidad se aplican parches de seguridad (PR-06)?
☐ ¿Cuánto tarda en promedio un equipo en recibir un parche crítico?
☐ ¿Cómo funciona la mesa de ayuda y qué incidentes de seguridad se reportan ahí?
☐ ¿Cómo se gestionan las altas y bajas de accesos cuando entra o sale un funcionario?
☐ ¿Cuándo se revisan los accesos de los usuarios y quién los autoriza (PR-01)?
☐ ¿Existe control de dispositivos extraíbles (pendrives, discos externos)?
☐ ¿Cómo se gestionan las cuentas de administrador y sus privilegios?
☐ ¿Hay estaciones de trabajo de uso público en sucursales y qué restricciones tienen?
☐ ¿Qué registro se lleva de los equipos dados de baja y su información?
☐ ¿Cómo se manejan los funcionarios que usan equipos personales (BYOD)?

### 5.4 Evidencias a pedir

| Evidencia | Formato sugerido |
|---|---|
| Reporte de parches (cobertura por equipo) | XLSX/PDF generado por la herramienta |
| Cobertura de antivirus/EDR | PDF de la consola (porcentaje de equipos protegidos) |
| Procedimiento de gestión de accesos | DOCX/PDF (PR-01) |
| Inventario de endpoints | XLSX con equipo, usuario, ubicación, SO |
| Proceso de altas/bajas de acceso | DOCX/PDF con responsables y plazos |

### 5.5 Con quién hablar

**Tec. Ariel Presa** (Jefe de Depto. Soporte Técnico). **Lic. Bernardo Ureta** (División TI) para cruces con Producción y Sistemas.

### 5.6 Particularidades y trampas

- **Cruzar con el curso hermano INFRA** (`curso-infra\`): el relevamiento de TI de este dossier se complementa con los módulos INFRA-01 a INFRA-11.
- **Trampa del parche impuesto al papel:** "aplicamos todos los parches" sin reporte de la herramienta = no es evidencia. Pedí el reporte.
- **Trampa de las bajas que no se hacen:** funcionarios que se fueron y mantienen accesos activos. Preguntá cuántas cuentas inactivas hay.
- Los pendrives y el correo son el canal de fuga clásico de datos personales: preguntá por la política de dispositivos extraíbles.

---

## 6. División Operaciones — Depto. Procesos

### 6.1 Qué hace el área

Documenta y administra el mapa de procesos del banco, los manuales de procedimientos y los flujos operativos. Es la memoria escrita de cómo se hace el trabajo.

### 6.2 Activos típicos

- Mapa de procesos (macroprocesos, procesos y subprocesos).
- Manuales de procedimientos operativos.
- Flujogramas de operaciones (crédito, pagos, atención).
- Indicadores y métricas de proceso.
- Documentos de instrucciones operativas.

### 6.3 Preguntas de relevamiento (checklist)

☐ ¿Dónde está el mapa de procesos del banco y qué cobertura tiene?
☐ ¿Qué procesos tratan datos personales de clientes y cuáles son?
☐ ¿Qué manuales de procedimientos existen y cuándo se actualizaron por última vez?
☐ ¿Cómo se aprueban y versionan los documentos de proceso?
☐ ¿Qué procesos son críticos para el negocio (candidatos a BIA/RC-01)?
☐ ¿Cómo se identifican los riesgos en los procesos (riesgo operacional Circular 2227)?
☐ ¿Existen procesos tercerizados y dónde está documentado (PR-08, GV-05)?
☐ ¿Cómo se controla la segregación de funciones en los flujos?
☐ ¿Qué controles de calidad/reconciliación tienen los procesos?
☐ ¿Quién es responsable de actualizar cada procedimiento?
☐ ¿Cómo se comunican los cambios de proceso al personal?
☐ ¿Qué indicadores se monitorean y qué evidencia dejan?

### 6.4 Evidencias a pedir

| Evidencia | Formato sugerido |
|---|---|
| Mapa de procesos | PDF/Visio (macro a subproceso) |
| Manuales de procedimientos | DOCX/PDF con versión y fecha |
| Flujogramas de operaciones | PDF/Visio |
| Listado de procesos críticos | XLSX con criticidad y responsable |

### 6.5 Con quién hablar

**Cra. Ana Paletta** (Jefe de Depto. Procesos). **Ec. Analía Cortizo** (División Operaciones).

### 6.6 Particularidades y trampas

- **Trampa del proceso ideal vs. real:** el manual dice una cosa y la operación hace otra. Preguntá "¿qué se hace cuando el manual no contempla el caso?".
- El mapa de procesos es insumo directo del BIA (RC-01): identificá en esta etapa los procesos críticos para no re-preguntar después.
- Si el área se siente "atacada" por preguntar cómo se hacen las cosas, aclarale que el relevamiento no audita su trabajo, lo documenta.

---

## 7. División Operaciones — Depto. Sistema de Pagos

### 7.1 Qué hace el área

Opera el sistema de pagos del banco, incluidas las operaciones interbancarias y el ciclo de pagos y cobranzas. Es un proceso de negocio crítico con riesgos financieros y de continuidad altos.

### 7.2 Activos típicos

- Aplicación / módulo de sistema de pagos.
- Operaciones interbancarias (conexiones con otros bancos y el BCU).
- Archivos de pagos y cobranzas.
- Conciliaciones bancarias.
- Calendarios de ventana de operación (cut-offs).
- Procedimientos de contingencia del ciclo de pagos.

### 7.3 Preguntas de relevamiento (checklist)

☐ ¿Cuál es el ciclo completo de una operación de pago y qué sistemas intervienen?
☐ ¿Qué conexiones interbancarias existen y cómo se protegen?
☐ ¿Cómo se autentican y autorizan las operaciones de pago?
☐ ¿Qué pasa si el sistema de pagos cae en una ventana operativa (continuidad)?
☐ ¿Existen resguardos específicos de los archivos de pagos?
☐ ¿Cómo se concilian los movimientos y con qué frecuencia?
☐ ¿Qué controles de detección de fraude hay en el ciclo de pagos?
☐ ¿Quiénes tienen acceso a generar y aprobar pagos (segregación de funciones)?
☐ ¿Qué registros (logs) quedan de cada operación de pago?
☐ ¿El sistema de pagos está contemplado en los planes de continuidad (RC-01/RC-02)?
☐ ¿Cómo se gestionan los pagos hacia/desde el exterior (tercerización, Comunicación 2022/254)?
☐ ¿Qué datos de clientes intervienen en los archivos de pago?

### 7.4 Evidencias a pedir

| Evidencia | Formato sugerido |
|---|---|
| Procedimientos de pagos | DOCX/PDF con versiones |
| Resguardos específicos del sistema | XLSX/PDF de configuraciones de backup |
| Plan de continuidad del ciclo de pagos | DOCX/PDF |
| Matriz de accesos a operaciones de pago | XLSX con rol y autorizaciones |
| Registro de conciliaciones | PDF/XLSX de conciliaciones realizadas |

### 7.5 Con quién hablar

**Cr. Guillermo Correa** (Jefe de Depto. Sistema de Pagos). **Ec. Analía Cortizo** (División Operaciones).

### 7.6 Particularidades y trampas

- **Riesgo alto:** cualquier falla aquí impacta en clientes y en la red interbancaria. El BCU mira este proceso con lupa.
- **Trampa de la segregación:** si la misma persona genera y aprueba un pago, es un hallazgo grave. Preguntá quién puede hacer ambas cosas.
- La ventana de pago (cut-off) define el RTO (tiempo objetivo de recuperación): anotá cuánto tiempo máximo puede estar caído el sistema.

---

## 8. División Operaciones — Depto. Información y Apoyo Comercial

### 8.1 Qué hace el área

Produce reportes e información de apoyo para el negocio comercial, y administra bases de datos de clientes y su explotación analítica.

### 8.2 Activos típicos

- Bases de datos de clientes (información comercial).
- Repositorios de reportes e informes.
- Herramientas de BI / analítica.
- Tableros de indicadores comerciales.
- Información derivada de la operación crediticia y de ahorro.

### 8.3 Preguntas de relevamiento (checklist)

☐ ¿Qué bases de datos de clientes maneja el área y con qué finalidad?
☐ ¿Qué datos personales (y sensibles) contienen esos reportes?
☐ ¿Quiénes pueden acceder a las bases de información comercial?
☐ ¿Cómo se anonimizan o minimizan los datos en los reportes?
☐ ¿Dónde se almacenan los reportes y quién los archiva?
☐ ¿Cuánto tiempo se conserva la información comercial?
☐ ¿Cómo se atienden las solicitudes de los clientes sobre sus datos (ARCO, URCDP-03)?
☐ ¿Las bases de clientes están inscriptas en URCDP (URCDP-04)?
☐ ¿Cómo se comparte información comercial con otras áreas o terceros?
☐ ¿Qué controles hay sobre la descarga de información a planillas?

### 8.4 Evidencias a pedir

| Evidencia | Formato sugerido |
|---|---|
| Inventario de bases de información | XLSX con nombre, contenido, responsable |
| Muestra de reportes con datos | XLSX/PDF (enmascarado para la evidencia) |
| Registro de inscripción URCDP | PDF de la URCDP (URCDP-04) |
| Procedimiento de solicitudes ARCO | DOCX/PDF |

### 8.5 Con quién hablar

Jefe del Depto. Información y Apoyo Comercial (no nominado en el organigrama vigente, verificar). **Ec. Analía Cortizo** (División Operaciones).

### 8.6 Particularidades y trampas

- **Trampa de la planilla que circula:** los reportes en Excel con datos reales de clientes que se mandan por correo son un clásico riesgo de fuga. Preguntá quién los recibe.
- La información comercial es el activo que más dispara obligaciones URCDP: cada base = una inscripción.
- Datos combinados de crédito + ahorro + pagos hacen al cliente "visible" de forma completa: la sensibilidad es mayor que la suma de las partes.

---

## 9. División Operaciones — Depto. Servicios Generales

### 9.1 Qué hace el área

Administra la seguridad física de las instalaciones: sucursales, datacenter, videovigilancia, control de accesos físico, gestión de residuos y logística de instalaciones.

### 9.2 Activos típicos

- Edificios, sucursales y oficinas en todo el país.
- Datacenter y salas de equipos.
- Sistema de videovigilancia (CCTV).
- Control de accesos físico (tarjetas, lectores, guardias).
- Registros de ingreso y egreso de personas y de terceros.
- Residuos y destrucción de documentación con datos personales.
- Alarmas, control de incendio, UPS/generadores.

### 9.3 Preguntas de relevamiento (checklist)

☐ ¿Qué perímetro físico protege las instalaciones críticas (datacenter, tesorería)?
☐ ¿Cómo funciona el control de acceso físico y quién lo administra (PR-04)?
☐ ¿Cómo se registra el ingreso de personal y de terceros (proveedores, técnicos)?
☐ ¿Qué zonas están cubiertas por videovigilancia y cuánto se conservan las grabaciones?
☐ ¿Quién revisa las grabaciones y bajo qué procedimiento?
☐ ¿Cómo se gestionan las tarjetas de acceso de funcionarios que se retiran?
☐ ¿Cómo se protege la información impresa con datos personales (expedientes en papel)?
☐ ¿Cómo se destruyen los residuos con información sensible (destructora/incineración)?
☐ ¿Qué medidas de protección contra incendio e inundación tiene el datacenter?
☐ ¿Existe backup de energía (UPS, generador) y con qué autonomía?
☐ ¿Cómo se custodian los equipos en tránsito y los medios de resguardo?
☐ ¿Las sucursales tienen procedimiento de seguridad al cierre y apertura?

### 9.4 Evidencias a pedir

| Evidencia | Formato sugerido |
|---|---|
| Planos de instalaciones | PDF/CAD con zonas de acceso |
| Registros de ingreso/egreso | XLSX/PDF (persona, fecha, hora, destino) |
| Política de videovigilancia | DOCX/PDF con plazos de retención |
| Procedimiento de gestión de residuos | DOCX/PDF |
| Reporte de control de accesos físico | XLSX/PDF |

### 9.5 Con quién hablar

**Ing. Agustín Araujo** (Jefe de Depto. Servicios Generales). **Ec. Analía Cortizo** (División Operaciones).

### 9.6 Particularidades y trampas

- **Trampa del papel en la calle:** expedientes de préstamos (datos personales muy sensibles) que salen de la sucursal sin sobre cerrado ni registro. Preguntá cómo viajan.
- La seguridad física y la lógica se cruzan: un pendrive robado de un escritorio es un incidente de datos personales.
- Videovigilancia + datos personales = el registro de cámaras también es una base de datos URCDP.

---

## 10. Área Comercial — División Banca Persona y División Canales y Apoyo Comercial

### 10.1 Qué hace el área

Es el negocio: otorga crédito hipotecario, administra expedientes de préstamos y legajos de clientes, atiende en sucursales y call center, y opera el canal Banco En Línea. Maneja los datos personales más sensibles del banco.

### 10.2 Activos típicos

- Expedientes de préstamos hipotecarios (papel y digital).
- Legajos de clientes (datos personales y patrimoniales).
- Sistema de crédito / originación de préstamos.
- Banco En Línea (clientes que operan por web/app).
- Call center / atención telefónica y sus grabaciones.
- Sucursales y cajas de atención.
- Contratos, consentimientos y solicitudes firmadas.

### 10.3 Preguntas de relevamiento (checklist)

☐ ¿Dónde se almacenan los expedientes de préstamos y en qué formato (papel/digital)?
☐ ¿Qué datos personales y sensibles se recaban para un crédito hipotecario?
☐ ¿Existe consentimiento informado documentado para el tratamiento de esos datos?
☐ ¿El sistema de crédito está inscripto en URCDP (URCDP-04)?
☐ ¿Se realizó una Evaluación de Impacto (EIPD, URCDP-05) del proceso de crédito?
☐ ¿Quiénes acceden a los legajos de clientes y con qué justificación?
☐ ¿Cómo se gestionan los datos de clientes en Banco En Línea (autenticación, sesión)?
☐ ¿Cómo se resguardan las grabaciones del call center y por cuánto tiempo?
☐ ¿Cómo se maneja la atención en sucursal de clientes (datos visibles en mostrador)?
☐ ¿Qué controles hay sobre el acceso a información crediticia por parte del personal?
☐ ¿Cómo se conservan los contratos y consentimientos y cuánto tiempo?
☐ ¿Cómo se atienden las solicitudes ARCO de clientes comerciales (URCDP-03)?

### 10.4 Evidencias a pedir

| Evidencia | Formato sugerido |
|---|---|
| Inventario de expedientes | XLSX con tipo, ubicación, volumen |
| Sistema de crédito: descripción funcional | DOCX/PDF |
| Modelo de consentimiento informado | PDF/DOCX del formulario real |
| Contrato tipo con cláusula de datos | PDF (enmascarado si es necesario) |
| Procedimiento de atención de ARCO | DOCX/PDF |
| Registro de EIPD (si existe) | DOCX/PDF (URCDP-05) |

### 10.5 Con quién hablar

**Cr. Alvaro Gandolfo** (División Banca Persona), **Marina Damiani** (Depto. Análisis de Préstamos), **Alejandro Pereyra** (Depto. Atención Personalizada), **Lic. Gustavo Bordoni** (División Canales y Apoyo Comercial), **Cra. Viviana Trabuco** (Depto. Canales de Atención), **Lic. Adriana Martínez** (Defensor del Cliente), **Cr. Pablo Liard** (Área Comercial).

### 10.6 Particularidades y trampas

- **Es el área con datos más sensibles:** el expediente hipotecario revela situación patrimonial, de ingresos y personal. Priorizá el EIPD (URCDP-05).
- **Trampa del mostrador:** en sucursal, los datos de un cliente se ven en pantalla mientras atiende al de al lado. Preguntá por pantallas y privacidad en mostrador.
- **Trampa del archivo papel:** los expedientes en papel no se respaldan y nadie los inventaría como "base de datos". Contalos y ponelos en el inventario.
- El Defensor del Cliente (Adriana Martínez) es un aliado clave: recibe quejas sobre datos y atención que sirven de insumo de riesgo.

---

## 11. Área Administración Financiera — Contaduría, Administración General y Finanzas

### 11.1 Qué hace el área

Administra la contabilidad y tributos, las compras y contrataciones con proveedores, y las finanzas y el mercado de capitales (tesorería y análisis financiero).

### 11.2 Activos típicos

- Sistema contable / ERP contable.
- Sistema de tesorería y finanzas.
- Expedientes de compras y contratos con proveedores.
- Base de proveedores (alta, datos, pagos).
- Información financiera y presupuestal.
- Servicios tercerizados (limpieza, seguridad, TI, consultoría).

### 11.3 Preguntas de relevamiento (checklist)

☐ ¿Cuál es el sistema contable del banco y dónde residen sus datos?
☐ ¿Qué información financiera sensible se maneja y quién la consulta?
☐ ¿Cómo se administran los proveedores y dónde está el registro completo?
☐ ¿Los contratos con proveedores incluyen cláusulas de seguridad de la información (PR-08)?
☐ ¿Qué proveedores acceden a datos o sistemas del banco (tercerización)?
☐ ¿Hay servicios tercerizados con datos en el exterior (Comunicación 2022/254)?
☐ ¿Cómo se evalúan los riesgos de la cadena de suministro (GV-05)?
☐ ¿Qué controles hay sobre la información financiera enviada a entes reguladores?
☐ ¿Cómo se gestiona la tesorería y qué medidas protegen las operaciones financieras?
☐ ¿Qué accesos tienen los usuarios del sistema contable y cómo se segregan funciones?
☐ ¿Cómo se conservan los comprobantes y cuánto tiempo?
☐ ¿Qué pasa con la información de proveedores cuando finaliza un contrato?

### 11.4 Evidencias a pedir

| Evidencia | Formato sugerido |
|---|---|
| Inventario de sistemas contables | XLSX con sistema, datos, responsable |
| Contratos con cláusulas de seguridad | PDF (sección específica) |
| Listado de proveedores | XLSX con categoría y criticidad |
| Matriz de servicios tercerizados | XLSX con proveedor, servicio, datos, ubicación |
| Registro de evaluación de proveedores | DOCX/PDF (GV-05) |

### 11.5 Con quién hablar

**Cra. Soledad Carreres** (Área Administración Financiera), **Cra. Ma. Eugenia Coronel** (División Contaduría), **Cra. Ana Karina Rodríguez** (Depto. Contabilidad y Tributos), **Lic. Rosario Larrosa** (División Administración General), **Cr. Matías Crespo** (División Finanzas y Mercado de Capitales).

### 11.6 Particularidades y trampas

- **Trampa del proveedor con acceso:** el proveedor de limpieza que entra al datacenter, el consultor con cuenta de red. Tercerización = riesgo de cadena de suministro (GV-05).
- **Trampa del contrato sin cláusula:** muchos contratos antiguos no mencionan seguridad de la información. Marcá cuáles hay que renegociar (PR-08).
- Compras y contrataciones es la puerta de entrada de los terceros: ganártelo (RELEV-05, perfil "el de terceros") facilita todo el resto.

---

## 12. Área Riesgos — Riesgos Financieros, Riesgos No Financieros, Cumplimiento, Seguimiento y Recuperación de Activos

### 12.1 Qué hace el área

Identifica y gestiona los riesgos financieros y no financieros, incluyendo el riesgo operacional y de ciberseguridad; cumple la normativa de PLA/FT; y recupera activos morosos y administra garantías e inmuebles.

### 12.2 Activos típicos

- Matrices de riesgo (financiero, operacional, legal, reputacional, ciberseguridad).
- Políticas de gestión de riesgos y de cumplimiento.
- Base de clientes morosos (datos personales).
- Expedientes de garantías e inmuebles.
- Informes al directorio y a entes reguladores.
- Procedimientos PLA/FT (debida diligencia, PEP).

### 12.3 Preguntas de relevamiento (checklist)

☐ ¿Dónde están las matrices de riesgo y quién las actualiza?
☐ ¿Cómo se evalúa el riesgo operacional (Circular 2227)?
☐ ¿Existe una metodología de evaluación de riesgos de seguridad de la información (ID-02/ID-03)?
☐ ¿Qué riesgos de ciberseguridad están identificados y con qué criticidad?
☐ ¿Qué políticas de cumplimiento existen y cómo se monitorean?
☐ ¿Qué controles PLA/FT operan y qué sistemas los soportan?
☐ ¿Dónde vive la base de clientes morosos y qué datos personales contiene?
☐ ¿Quiénes acceden a la información de morosos y garantías?
☐ ¿Existen planes de continuidad y cómo se prueban (RC-01)?
☐ ¿Cómo se reporta el riesgo a la Gerencia General y al Directorio (GV-06)?
☐ ¿La Oficial de Cumplimiento recibe reportes de incidentes de seguridad?
☐ ¿Qué acciones de concientización en riesgos se hacen al personal (PR-02)?

### 12.4 Evidencias a pedir

| Evidencia | Formato sugerido |
|---|---|
| Matrices de riesgo | XLSX con riesgo, probabilidad, impacto, tratamiento |
| Planes de continuidad | DOCX/PDF (RC-01/RC-02) |
| Políticas de cumplimiento | DOCX/PDF vigentes |
| Procedimientos PLA/FT | DOCX/PDF |
| Inventario de bases de morosos | XLSX (nombre, contenido, responsable) |

### 12.5 Con quién hablar

**Ec. Laura Zunino** (Área Riesgos), **Ec. Gretel Yaffe** (Depto. Riesgos Financieros), **Cra. Melissa Moraes** (Depto. Riesgos No Financieros y Oficial de Cumplimiento), **Cra. Patricia Amodio** (División Seguimiento y Recuperación de Activos), **Pablo Lorenzo** (Depto. Gestión de Garantías e Inmuebles), **Alejandra Olivera** (Depto. Gestión de Morosidad).

### 12.6 Particularidades y trampas

- **Aquí está tu par natural:** la Cra. Melissa Moraes es el RSI recomendado. Con ella vas a coordinar todo el relevamiento de riesgos.
- **Trampa de la matriz desactualizada:** la matriz existe pero nadie la actualizó este año. Preguntá la fecha de última revisión.
- La base de morosos es un activo de datos personales con carga reputacional fuerte: tratarla con cuidado URCDP.
- Riesgos No Financieros + Oficial de Cumplimiento son la segunda línea: ahorrate duplicar preguntas, pedile lo que ya tienen relevado.

---

## 13. División Capital Humano

### 13.1 Qué hace el área

Administra los legajos de los funcionarios, las altas y bajas, las capacitaciones, y los acuerdos de confidencialidad del personal.

### 13.2 Activos típicos

- Legajos de funcionarios (datos personales).
- Sistema de RRHH (nómina, ausentismo, evaluación).
- Registro de capacitaciones.
- Acuerdos de confidencialidad y de uso aceptable firmados.
- Proceso de altas y bajas de personal.
- Evaluaciones de desempeño y expedientes disciplinarios.

### 13.3 Preguntas de relevamiento (checklist)

☐ ¿Dónde se guardan los legajos de funcionarios y en qué formato?
☐ ¿Qué sistema de RRHH existe y quién lo administra?
☐ ¿Qué datos personales y sensibles contiene el legajo (salud, disciplina, banco)?
☐ ¿Cómo se gestionan las altas y bajas de funcionarios (y de sus accesos)?
☐ ¿Todos los funcionarios firman acuerdo de confidencialidad?
☐ ¿Existe un programa de concientización en ciberseguridad (PR-02)?
☐ ¿Cómo se registra la asistencia a capacitaciones?
☐ ¿Quiénes pueden consultar los legajos y con qué autorización?
☐ ¿Cómo se conservan los legajos de exfuncionarios y cuánto tiempo?
☐ ¿La información de RRHH está inscripta en URCDP (URCDP-04)?
☐ ¿Cómo se manejan las contrataciones de terceros y sus cláusulas?
☐ ¿Qué controles hay sobre la información de nómina y salarios?

### 13.4 Evidencias a pedir

| Evidencia | Formato sugerido |
|---|---|
| Registro de capacitaciones | XLSX con curso, fecha, asistencia |
| Acuerdos de confidencialidad firmados | PDF (muestra) |
| Procedimiento de altas/bajas | DOCX/PDF |
| Plan anual de concientización | DOCX/PDF (PR-02) |
| Inventario de legajos | XLSX con cantidad y formato |

### 13.5 Con quién hablar

**Sr. Pablo Castro** (División Capital Humano), **Bernardo Rocha** (Depto. Administración de RRHH), **Ing. Cecilia Cabrera** (Depto. Desarrollo de RRHH).

### 13.6 Particularidades y trampas

- **Trampa del legajo abierto:** papeles con datos médicos y salariales en escritorios compartidos. Preguntá cómo se archivan físicamente.
- El plan de concientización (PR-02) se construye con el calendario de capacitaciones de Capital Humano: coordiná.
- Las bajas de personal que no disparan la baja de accesos es un hallazgo clásico: cruzá con Soporte Técnico.

---

## 14. División Auditoría Interna

### 14.1 Qué hace el área

Audita la gestión y los controles del banco, emite informes con hallazgos y recomendaciones y da seguimiento a su cumplimiento. Es la tercera línea de defensa.

### 14.2 Activos típicos

- Informes de auditoría (internos y de entes externos).
- Papeles de trabajo y hallazgos.
- Plan anual de auditoría.
- Seguimiento de recomendaciones pendientes.
- Observaciones de auditorías del BCU y de la URCDP.

### 14.3 Preguntas de relevamiento (checklist)

☐ ¿Qué informes de auditoría recientes cubren sistemas y seguridad de la información?
☐ ¿Cuáles fueron los hallazgos principales de los últimos dos años?
☐ ¿Qué recomendaciones siguen pendientes y desde cuándo?
☐ ¿Qué observaciones de BCU, URCDP o Agesic recibió el banco?
☐ ¿Existe un plan anual de auditoría que contemple TI?
☐ ¿Cómo auditan los accesos y la gestión de cambios?
☐ ¿Qué controles recomienda Auditar para el área de TI?
☐ ¿Hay hallazgos sobre resguardo de información o pruebas de restauración?
☐ ¿Cómo se da seguimiento al cumplimiento de las recomendaciones?
☐ ¿Qué documentos de control de TI se auditan con más frecuencia?

### 14.4 Evidencias a pedir (con autorización del sponsor)

| Evidencia | Formato sugerido |
|---|---|
| Informes de auditoría recientes | PDF (con autorización expresa) |
| Plan anual de auditoría | PDF/DOCX |
| Listado de recomendaciones pendientes | XLSX con estado y fecha |
| Observaciones de entes reguladores | PDF (con autorización) |

### 14.5 Con quién hablar

**Cr. Marcelo Jorge** (División Auditoría Interna). Gestioná el acceso a evidencias vía el sponsor (GV-03), porque la confidencialidad de los informes es sensible.

### 14.6 Particularidades y trampas

- **Es el insumo de oro del RSI:** los hallazgos de auditoría te dicen dónde están los riesgos ya conocidos. No los pidas "de prepo": explicá que el RSI los necesita para priorizar el plan (GV-04).
- **Trampa del ego de auditoría:** auditoría es la tercera línea y puede ver al RSI como un competidor. Mostrá que el relevamiento suma (defensa en profundidad), no que invade su terreno.
- Todo lo que recojas de auditoría debe tener **autorización formal** y manejarse con máxima confidencialidad.

---

## 15. División Planificación Estratégica y Divisiones de Apoyo

### 15.1 Qué hace el área

Define los objetivos institucionales, el presupuesto y los proyectos; y las divisiones jurídicas y de secretaría gestionan contratos, resoluciones, escrituras y la documentación oficial del banco.

### 15.2 Activos típicos

- Plan estratégico y objetivos institucionales.
- Presupuesto y planes anuales.
- Portafolio de proyectos.
- Contratos y resoluciones.
- Escrituras y documentación notarial.
- Archivo y gestión documental (papel y digital).
- Actas de directorio y comunicaciones oficiales.

### 15.3 Preguntas de relevamiento (checklist)

☐ ¿Cuáles son los objetivos estratégicos que impactan en tecnología y seguridad (GV-04)?
☐ ¿Qué proyectos en curso tienen componente tecnológico o de datos?
☐ ¿El presupuesto contempla inversión en ciberseguridad?
☐ ¿Dónde se archivan los contratos y resoluciones y en qué formato?
☐ ¿Cómo se gestiona el archivo documental (papel y digital)?
☐ ¿Qué escrituras y documentos notariales se conservan y dónde?
☐ ¿Quiénes pueden acceder al archivo y con qué registro?
☐ ¿Cómo se protegen los documentos oficiales del banco (actas, resoluciones)?
☐ ¿Los contratos con terceros incluyen cláusulas de seguridad (PR-08)?
☐ ¿Cuánto tiempo se conserva cada categoría documental?
☐ ¿Existen proyectos de digitalización o migración en curso?
☐ ¿Cómo se gestiona la documentación del directorio?

### 15.4 Evidencias a pedir

| Evidencia | Formato sugerido |
|---|---|
| Plan estratégico | PDF/DOCX |
| Presupuesto aprobado | XLSX/PDF |
| Listado de proyectos en curso | XLSX con estado y responsable |
| Tabla de retención documental | XLSX con plazos por categoría |
| Modelo de contrato con cláusula de seguridad | PDF (sección específica) |

### 15.5 Con quién hablar

**Cr. Pablo Vargha** (División Planificación Estratégica), **Cra. Kariné Dolabdjian** (Depto. Control de Gestión), **Dr. Héctor Dotta** (División Servicios Jurídicos Notariales), **Sr. Bruno Alonso** (División Secretaría General).

### 15.6 Particularidades y trampas

- El plan estratégico y el presupuesto son insumo directo del **Plan Anual (GV-04)**: sin conocerlos, el plan de seguridad no se alinea con el negocio.
- **Trampa del archivo eterno:** documentos que se conservan "por las dudas" sin tabla de retención = riesgo de datos personales acumulados sin motivo. Preguntá por plazos.
- La gestión documental define qué se digitaliza y qué se destruye: enlaza con el proceso de destrucción de Servicios Generales.

---

## 16. El cuestionario de bases de datos (reutilizable)

Cada vez que aparezca una base de datos, un sistema con datos, un archivo físico de datos o un registro (expedientes, legajos, grabaciones, videovigilancia), completá una fila de esta tabla. Este cuestionario alimenta directamente **URCDP-04 (inscripción de bases / ROPA)**, **ID-01 (inventario de activos)** y **URCDP-01 (Documento de Seguridad)**.

### 16.1 Tabla de relevamiento de bases de datos

| # | Nombre de la base | Finalidad | Sistema asociado | Categorías de datos | ¿Datos personales? ¿Sensibles? | Quién accede | Dónde vive (ubicación física/lógica) | Nivel de sensibilidad (B/M/A) | Plazo de retención | ¿Inscripta en URCDP? | Medidas de seguridad |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | | | | | | | | | | | |
| 2 | | | | | | | | | | | |
| 3 | | | | | | | | | | | |
| 4 | | | | | | | | | | | |
| 5 | | | | | | | | | | | |
| 6 | | | | | | | | | | | |
| 7 | | | | | | | | | | | |
| 8 | | | | | | | | | | | |
| 9 | | | | | | | | | | | |
| 10 | | | | | | | | | | | |

### 16.2 Instrucciones de llenado

1. **Una fila por base de datos** detectada, aunque sea en papel (expedientes, legajos) o en registros (grabaciones, cámaras).
2. "Categorías de datos": datos de identificación, contacto, económicos, patrimoniales, de salud, judiciales, biográficos, etc.
3. "¿Datos sensibles?": los del art. 17 de la Ley 18.331 (origen racial/étnico, salud, religión, etc.) y los de alta sensibilidad para el negocio (situación crediticia).
4. "Dónde vive": servidor/BD/sala/ubicación remota; anotá si hay copias fuera.
5. "Nivel de sensibilidad": B (baja), M (media), A (alta) — según impacto de una filtración.
6. "Plazo de retención": de la tabla de retención documental o de la política interna; si no existe, anotar "sin definir" (es un hallazgo).
7. "¿Inscripta en URCDP?": verificar en la URCDP (Sí/No/Pendiente). Si No → planificar URCDP-04.
8. "Medidas de seguridad": cifrado, accesos, respaldos, minimización, controles físicos.

### 16.3 Preguntas para completar cada fila (checklist)

☐ ¿Cuál es el nombre exacto de la base o sistema?
☐ ¿Para qué se usa y qué negocio soporta?
☐ ¿Qué sistema o aplicación la alimenta?
☐ ¿Qué categorías de datos contiene (detallar personales y sensibles)?
☐ ¿Quiénes pueden acceder y con qué rol?
☐ ¿Dónde está físicamente y lógicamente (servidor, BD, nube, sala)?
☐ ¿Qué impacto tendría si se filtra o se pierde?
☐ ¿Cuánto tiempo se conserva y por qué?
☐ ¿Está inscripta en URCDP (URCDP-04)?
☐ ¿Qué medidas de seguridad la protegen (cifrado, accesos, respaldo)?

---

## 17. Errores comunes al relevar por división

| Error | Consecuencia | Cómo evitarlo |
|---|---|---|
| Preguntar sin haber leído nada del área | El entrevistado pierde confianza | Leé la sección del dossier antes de la reunión |
| Aceptar "sí, tenemos todo" sin evidencia | El informe no resiste una auditoría | Pedí siempre la evidencia, no la palabra |
| Saltar de área en área sin orden | Datos repetidos y bases sin relevar | Seguí el orden del dossier y el cuestionario 16 |
| Tratar a una sola persona como "dueño de todo" | Se pierden sistemas sombra | Hablá con jefe y con un operador de cada área |
| Tomar el relevamiento como un interrogatorio | El área se cierra y no colabora | Usá el guion del RELEV-05: dar antes de pedir |
| No anotar quién dijo qué | Imposible validar después | Minuta con nombres y fechas al cierre |
| Dejar pendientes sin fecha | El dossier queda viejo en una semana | Checklist de seguimiento semanal |

---

## 18. Plan de acción del dossier

☐ Confirmar organigrama vigente (PDF SF.PLE.05) y contactos de cada área.
☐ Agenda de entrevistas por división (orden sugerido: TI primero, Riesgos segundo, resto por disponibilidad).
☐ Crear carpeta por área en `EST-CARPETAS-001`.
☐ Aplicar checklist de cada sección 3 a 15.
☐ Completar el cuestionario de bases de datos (sección 16) en una sola planilla.
☐ Consolidar en ID-01 (inventario de activos) e ID-03 (análisis de riesgos).
☐ Identificar bases no inscriptas para URCDP-04.
☐ Enviar resumen de hallazgos al sponsor (GV-03) y al RSI (GV-06).

---

**Documentos relacionados:** ID-01 · ID-03 · URCDP-01 · URCDP-04 · PR-06 · PR-08 · GV-05 · PR-01 · PR-02 · PR-03 · PR-04 · PR-05 · PR-07 · RC-01 · RC-02 · GV-04 · GV-06 · EST-CARPETAS-001
