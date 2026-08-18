# RELEV-01 · El Banco por dentro: negocio, cultura y cómo se deciden las cosas

> ⚠️ **Alerta:** este documento menciona **nombres propios del organigrama del Banco** (personas y cargos, abril 2026). Antes de usar el documento, verificá la vigencia de esos nombres contra el organigrama actual.

> ⚠️ **Verificar contra el organigrama vigente:** los nombres y cargos de este módulo corresponden al organigrama de abril 2026 (PDF SF.PLE.05, https://www.bhu.com.uy/sobre-bhu/organigrama). Antes de usarlos en una reunión o en un documento oficial, confirmalos contra la versión vigente: los cargos rotan y los nombres pueden cambiar sin aviso.
>
> **Función del MCU 5.0:** este módulo ejecuta la función ID (Identificar): no se puede inventariar activos (ID.AM) ni evaluar riesgos (ID.RA) sin entender primero qué hace el banco, quién decide y dónde vive la información.
> **ISO/IEC 27001:** comprender el contexto de la organización (cláusula 4) es el primer paso del SGSI: el alcance (GV-02) y los activos (A.8) nacen de conocer el negocio.
> **BCU:** el EMG y la Circular 2227 (riesgo operacional) exigen que el RSI conozca la operación real: no se gestiona un riesgo que no se entiende.
> **URCDP:** los datos personales viven dentro del negocio (clientes, préstamos, ahorro, pagos): este mapa es la base del registro de tratamientos y del Documento de Seguridad (URCDP-01, URCDP-04).
> **Nivel del curso:** 🟢 Descubrir

---

## 1. El negocio del Banco en una página

El Banco Hipotecario del Uruguay es un **banco público especializado** que hoy se organiza alrededor de cuatro grandes negocios. Si sos RSI o consultor, tu primer trabajo no es leer normativa: es poder explicar en cinco minutos **de qué vive el banco**, porque no se protege lo que no se entiende.

| Negocio | Qué hace | Dónde viven los datos que te importan |
|---|---|---|
| Crédito hipotecario | Otorga y gestiona préstamos para vivienda: es el corazón histórico del banco. | Expedientes de crédito, garantías, inmuebles, scoring, morosidad. |
| Ahorro | Capta depósitos y productos de ahorro de socios y clientes. | Cuentas, saldos, identificación del titular, movimientos. |
| Pagos y cobranzas | Gestiona cobros de cuotas, pagos de servicios y el sistema de pagos interbancario. | Transacciones, claves, registros de conciliación. |
| Atención comercial | Canal presencial y digital para vender y atender: sucursales en todo el país y Banco En Línea. | Bases de clientes, consultas, credenciales, canales. |

**Quiénes son sus clientes/socios.** El Banco atiende a personas y a instituciones. Sus socios son el núcleo histórico, y hoy la base de clientes incluye también a quienes usan ahorro, pagos y servicios sin ser titulares de un crédito. Para vos esto significa una cosa: **hay datos personales en todas partes**, desde el formulario de una sucursal hasta el login del Banco En Línea.

**Red de sucursales.** El banco tiene presencia en todo el país. Cada sucursal es un punto físico con terminales, servidores locales, archivos y personas: la seguridad física (PR-04) y la información que se releva en territorio no es solo "de casa central".

**Banco En Línea.** Es el canal digital (web y app) que usan los socios/clientes para consultar y operar. Es, junto al sistema de pagos, el activo que más te van a nombrar en el relevamiento: es donde vive la identidad digital y donde un incidente se nota el mismo día.

**Sistema de pagos interbancario.** El Banco participa del sistema de pagos del país: transferencias, compensación y liquidación. Aquí el riesgo operacional del BCU (Circular 2227) se vuelve concreto: una falla de TIC no es un problema "informático", es un problema de pagos.

> **Por qué el RSI debe entender el negocio antes de relevar.** Pensá en el relevamiento como una auditoría médica: nadie le pide análisis de sangre a un paciente sin antes preguntarle qué le duele y cómo vive. Si llegás a la reunión hablando de "cláusulas y anexos" y no sabés qué es una cuota hipotecaria o cómo se liquida un pago, el área te va a atender por cortesía y te va a dar papeles genéricos. Si, en cambio, demostrás que entendés el negocio, el área te va a mostrar **lo que realmente importa**, y eso es exactamente lo que necesitás para inventariar activos y evaluar riesgos.

---

## 2. El organigrama completo en "español claro"

Organigrama de referencia (abril 2026). Recordá la advertencia inicial: **verificá contra el organigrama vigente** antes de escribir un nombre en un documento oficial.

```
DIRECTORIO
├── Asesor Letrado de Directorio
└── GERENCIA GENERAL
    ├── Área Comercial (Cr. Pablo Liard)
    ├── Área Operaciones y TI
    ├── Área Administración Financiera (Cra. Soledad Carreres)
    ├── Área Riesgos (Ec. Laura Zunino)
    ├── División Secretaría General (Sr. Bruno Alonso)
    ├── División Auditoría Interna (Cr. Marcelo Jorge)
    ├── División Capital Humano (Sr. Pablo Castro)
    ├── División Planificación Estratégica (Cr. Pablo Vargha)
    └── División Servicios Jurídicos Notariales (Dr. Héctor Dotta)
```

| Área / División | Misión en una frase | Para qué te sirve en el relevamiento |
|---|---|---|
| Área Comercial (Cr. Pablo Liard) | Vende y atiende: créditos, ahorro y canales. | Dónde viven los datos personales de la operación comercial y el trato directo con clientes. |
| → División Banca Persona (Cr. Alvaro Gandolfo) | Gestiona el negocio con las personas: análisis y atención. | Depto. Análisis de Préstamos (Marina Damiani): el expediente de crédito. Depto. Atención Personalizada (Alejandro Pereyra): el contacto con el cliente. |
| → División Canales y Apoyo Comercial (Lic. Gustavo Bordoni) | Diseña y opera los canales de atención. | Depto. Canales de Atención (Cra. Viviana Trabuco): sucursales, Banco En Línea, Defensor del Cliente (Lic. Adriana Martínez). |
| Área Operaciones y TI | Opera los sistemas y los procesos del banco. | La 1ª línea de defensa: aquí viven los activos tecnológicos, los resguardos y los procesos. |
| → División TI (Lic. Bernardo Ureta) | Produce, desarrolla y da soporte a los sistemas. | Depto. Producción (Ing. Daniel Herrera): infraestructura. Depto. Sistemas (Lic. Cristian Palo): aplicaciones y bases. Depto. Soporte Técnico (Tec. Ariel Presa): puestos y soporte. |
| → División Operaciones (Ec. Analía Cortizo) | Ejecuta los procesos operativos y de pagos. | Depto. Procesos (Cra. Ana Paletta), Depto. Sistema de Pagos (Cr. Guillermo Correa), Depto. Información y Apoyo Comercial, Depto. Servicios Generales (Ing. Agustín Araujo). |
| Área Administración Financiera (Cra. Soledad Carreres) | Maneja la plata, la contabilidad y las compras. | Contrataciones (terceros), contabilidad y tributos: pistas de auditoría y cadena de suministro (GV-05). |
| → División Contaduría (Cra. Ma. Eugenia Coronel) | Lleva la contabilidad. | Depto. Contabilidad y Tributos (Cra. Ana Karina Rodríguez). |
| → División Administración General (Lic. Rosario Larrosa) | Administra recursos y compras. | Depto. Compras y Contrataciones: los contratos con terceros y proveedores. |
| → División Finanzas y Mercado de Capitales (Cr. Matías Crespo) | Gestiona la liquidez y las finanzas. | Depto. Análisis Financiero: información financiera sensible. |
| Área Riesgos (Ec. Laura Zunino) | Identifica, mide y controla los riesgos. | La 2ª línea de defensa: lugar recomendado del RSI y par natural del Oficial de Cumplimiento. |
| → Depto. Riesgos Financieros (Ec. Gretel Yaffe) | Riesgo de crédito y mercado. | Metodología de riesgos y apetito: referencia para ID-02. |
| → Depto. Riesgos No Financieros (Cra. Melissa Moraes) | Riesgo operacional, seguridad y cumplimiento. | **El par natural del RSI** y el hogar recomendado del rol. Melissa Moraes también es Oficial de Cumplimiento. |
| → División Seguimiento y Recuperación de Activos (Cra. Patricia Amodio) | Recupera créditos y gestiona garantías. | Depto. Gestión de Garantías e Inmuebles (Pablo Lorenzo), Depto. Gestión de Morosidad (Alejandra Olivera): datos muy sensibles. |
| Dependientes de Gerencia General | | |
| → División Secretaría General (Sr. Bruno Alonso) | Da fe, registra y apoya el gobierno corporativo. | Actas, expedientes y formalidades: cómo pedir las cosas por escrito. |
| → División Auditoría Interna (Cr. Marcelo Jorge) | Evalúa y asegura el control interno. | La 3ª línea de defensa: hallazgos previos y expectativas sobre el RSI. |
| → División Capital Humano (Sr. Pablo Castro) | Gestiona a las personas. | Depto. Administración de RRHH (Bernardo Rocha), Depto. Desarrollo de RRHH (Ing. Cecilia Cabrera): concientización (PR.AT) y personas. |
| → División Planificación Estratégica (Cr. Pablo Vargha) | Planifica y mide la gestión. | Depto. Control de Gestión (Cra. Kariné Dolabdjian): metas, indicadores y proyectos. |
| → División Servicios Jurídicos Notariales (Dr. Héctor Dotta) | Asesoría legal y notarial. | Lugar alternativo para el DPD y para resolver cuestiones normativas. |

### 2.1 Cómo leer el organigrama sin marearte

Un organigrama con cuatro niveles asusta, pero se lee con tres preguntas:

1. **¿Qué hace esta área?** (su misión en una frase): ya está en la columna "Misión".
2. **¿Qué información maneja?** (el dato que te interesa relevar): está en la columna "Para qué te sirve".
3. **¿Quién es el nombre de referencia?** (el interlocutor correcto): está en negrita en la última columna.

Las cuatro áreas que vas a visitar en las olas del plan (RELEV-03) son Comercial, Operaciones y TI, Administración Financiera y Riesgos. Las divisiones que cuelgan de Gerencia General (Secretaría, Auditoría, Capital Humano, Planificación, Jurídico) aparecen en la Ola 3, cuando el relevamiento deja de ser técnico y pasa a ser institucional.

> **Regla de oro del mapa de actores:** cada reunión tiene un **responsable** (el que tiene la información), un **sponsor** (el que la habilita) y un **destinatario de la minuta** (el que debe saber que se avanzó). No son siempre la misma persona: el técnico que te muestra el sistema no es quien firma el pedido de evidencia.

---

## 3. Cómo se toman las decisiones

El Banco es un banco público: **las decisiones no se toman en una reunión informal**. Hay un circuito, una jerarquía y una forma de pedir que, si la respetás, te abre todas las puertas; si no, te cierra todas.

**El circuito básico.** El **Directorio** aprueba las políticas y los grandes lineamientos. La **Gerencia General** ejecuta y traduce esas decisiones en acciones. Por debajo, cada nivel (Gerente de Área → División → Departamento) administra su territorio y responde hacia arriba.

**El comité y el Oficial de Cumplimiento.** Existen instancias de gobierno de riesgos y cumplimiento en las que participan las áreas. El Oficial de Cumplimiento (hoy la Cra. Melissa Moraes, en Riesgos No Financieros) vigila que el banco cumpla con las normas. Para el SGSI se propone además un **Comité de Seguridad de la Información** (GV-03), que es donde el relevamiento va a rendir cuentas de avance.

**Formalidad y circuito de expedientes.** En el Banco las cosas se piden y se deciden **por escrito** y quedan en **expedientes**. Nada de "te mando un mensajito y arrancamos": el pedido de una reunión, de un informe o de una evidencia debe entrar por el canal formal.

> **Qué significa para vos:**
> - **Respetar canales:** la invitación formal sale de Gerencia General o del sponsor de área. Nunca aparezcas "de rebote" en el despacho de un Gerente de Área sin el circuito previo.
> - **Sponsor por área:** cada entrevista debe tener un padrino dentro del área que la habilite y que luego reciba la minuta.
> - **Pedir por escrito:** todo pedido de evidencia se hace por nota o correo con copia a quien corresponda. Es la regla que te va a proteger cuando un dato "no aparece".

### 3.1 Un ejemplo de circuito de decisión

Pensá que querés saber qué hace el banco con la nube o con un nuevo sistema externo. El circuito real es más o menos así:

1. El **Departamento** (por ejemplo, Sistemas) identifica la necesidad y arma la propuesta técnica.
2. La **División** (TI) la evalúa y la eleva a su **Gerente de Área** (Operaciones y TI).
3. El **Área** la coordina con las áreas de control: **Riesgos** opina sobre el riesgo, **Compras** arma el proceso de contratación, **Jurídico** revisa el contrato.
4. Si hay datos personales, interviene el **DPD**; si hay riesgo operacional, el **Oficial de Cumplimiento**.
5. La propuesta sube a **Gerencia General** y, si corresponde, al **Directorio** para su aprobación.
6. Todo ese camino queda **registrado en un expediente** con dictámenes, informes y notas de paso.

> **Qué significa para el relevamiento:** no le preguntes a un técnico de un departamento una decisión que solo puede responder un Gerente de Área o el Directorio. Saber en qué nivel vive cada respuesta te ahorra reuniones incómodas y te dice **a quién invitar a qué**. Si el dato es operativo, hablás con el Departamento; si es metodológico, con la División; si es de política, con el Área o Gerencia General.

---

## 4. Cultura organizacional de un banco público uruguayo

| Rasgo cultural | Qué significa | Qué hacer en el relevamiento |
|---|---|---|
| Formalidad | La palabra escrita vale más que la hablada. | Minuta por cada reunión, pedidos por escrito, agradecimientos formales. |
| Prudencia | No se compromete nada que no esté aprobado. | Nunca pedir que "te pasen algo sin compromiso": ofrecé el marco normativo y el pedido formal. |
| Normativa | Todo tiene su fundamento legal. | Siempre citá la norma que justifica tu pedido (MCU 5.0, BCU, URCDP). |
| Jerarquías | La autoridad baja de arriba hacia abajo. | Agendá de arriba hacia abajo y escalá cuando una puerta no se abra. |
| Tiempos | Los plazos se manejan con calma y burocracia. | Planificá con margen, no esperes respuestas inmediatas, confirmá seguimientos. |
| Memoria institucional | Mucha experiencia acumulada en pocas personas. | El técnico con 20 años en el banco es tu mejor fuente de verdad. |

**Un guion para abrir la conversación con cualquier área.** La formalidad no significa frialdad: significa claridad. Un buen arranque de reunión es:

> *"Buen día. Muchas gracias por recibirnos. Como le comentamos por nota, estamos relevando cómo se organiza y qué información maneja el área, en el marco del SGSI que el banco está implementando (MCU 5.0 de Agesic, BCU y URCDP). No venimos a auditar ni a criticar: venimos a aprender cómo trabajan, para que los documentos del sistema de seguridad reflejen la realidad del área y no un modelo teórico. Lo que hoy nos cuente nos sirve para dos cosas: armar el inventario de información y entender qué necesita el área para seguir trabajando segura."*

Ese párrafo baja las defensas porque hace tres cosas: ubica la reunión en un marco formal, aclara que no hay juicio y explica el beneficio concreto para el área.

**Cómo manejar la prudencia y los tiempos.** En un banco público las respuestas demoran y los compromisos se escriben. Reglas simples:

- Nunca presiones por teléfono lo que ya pediste por escrito: solo recordá con una nota cortés.
- Cuando un plazo se vence, avisá por escrito al responsable y al sponsor del área.
- Agradecé formalmente cada evidencia recibida: el reconocimiento abre la siguiente puerta.

---

## 5. Las tres líneas de defensa y dónde vive la seguridad hoy

Pensá la seguridad del banco como un club nocturno con tres controles:

- **1ª línea: el personal del club (TI y Operaciones).** Son quienes hacen el trabajo y previenen problemas todos los días: resguardan los activos, controlan accesos, mantienen los sistemas. En el Banco son el Área Operaciones y TI y las áreas operativas.
- **2ª línea: los encargados de control (Riesgos No Financieros, RSI, DPD).** No hacen el trabajo: lo **controlan**. Definen cómo se hace, miden riesgos y avisan cuando algo se sale de línea. El lugar recomendado para el RSI es **Área Riesgos → Depto. Riesgos No Financieros**, el par natural de la Cra. Melissa Moraes. El **DPD** puede vivir en Riesgos o en Servicios Jurídicos.
- **3ª línea: la auditoría (Auditoría Interna).** Viene de afuera del escenario a revisar que todos hagan lo que dicen que hacen. Evalúa el SGSI y reporta al Directorio.

| Línea | Rol | Dónde en el Banco |
|---|---|---|
| 1ª | Implementa y opera los controles | TI, Operaciones, Comercial, Administración |
| 2ª | Controla, define y asesora | Riesgos No Financieros, RSI, DPD, Oficial de Cumplimiento |
| 3ª | Evalúa de forma independiente | Auditoría Interna |

> **Dónde vive la seguridad hoy.** En la práctica, la seguridad de la información no tiene hoy una unidad central con ese nombre: vive **dispersa** entre TI (la técnica), Riesgos (la metodología), Cumplimiento (las normas) y Auditoría (la evaluación). Tu trabajo como RSI es **ordenar y centralizar el criterio**, no pelearle el territorio a nadie.

---

## 6. Mapa: quién tiene la información que necesito

| Área | Qué información guarda | Quién la conoce mejor |
|---|---|---|
| Análisis de Préstamos | Expedientes de crédito, garantías, scoring. | Marina Damiani (Gerente de Depto.) |
| Atención Personalizada | Consultas y trato con clientes. | Alejandro Pereyra (Gerente de Depto.) |
| Canales de Atención | Sucursales, Banco En Línea, atención. | Cra. Viviana Trabuco (Gerente de Depto.) |
| Producción | Servidores, redes, infraestructura. | Ing. Daniel Herrera (Gerente de Depto.) |
| Sistemas | Aplicaciones, bases de datos, desarrollo. | Lic. Cristian Palo (Gerente de Depto.) |
| Soporte Técnico | Puestos de trabajo, equipos, incidentes. | Tec. Ariel Presa (Gerente de Depto.) |
| Procesos | Procedimientos operativos documentados. | Cra. Ana Paletta (Gerente de Depto.) |
| Sistema de Pagos | Pagos interbancarios y su operación. | Cr. Guillermo Correa (Gerente de Depto.) |
| Servicios Generales | Instalaciones, seguridad física, mantenimiento. | Ing. Agustín Araujo (Gerente de Depto.) |
| Compras y Contrataciones | Contratos con terceros y proveedores. | Gerente de Depto. (Div. Administración General) |
| Contabilidad y Tributos | Registros contables y tributarios. | Cra. Ana Karina Rodríguez (Gerente de Depto.) |
| Riesgos No Financieros | Riesgo operacional, cumplimiento. | Cra. Melissa Moraes (Gerente de Depto. y Oficial de Cumplimiento) |
| Riesgos Financieros | Riesgo de crédito y mercado. | Ec. Gretel Yaffe (Gerente de Depto.) |
| Gestión de Garantías e Inmuebles | Garantías y propiedades del banco. | Pablo Lorenzo (Gerente de Depto.) |
| Gestión de Morosidad | Deudores morosos y recuperación. | Alejandra Olivera (Gerente de Depto.) |
| Capital Humano | Personas, contratos laborales, capacitación. | Bernardo Rocha y Cecilia Cabrera (Gerentes de Depto.) |
| Secretaría General | Actas, expedientes, formalidades. | Sr. Bruno Alonso (Jefe de División) |
| Auditoría Interna | Hallazgos de auditoría previos. | Cr. Marcelo Jorge (Jefe de División) |
| Planificación Estratégica | Proyectos, indicadores, presupuesto. | Cra. Kariné Dolabdjian (Gerente de Depto.) |
| Servicios Jurídicos Notariales | Asesoría legal y contratos. | Dr. Héctor Dotta (Jefe de División) |

---

## 7. Errores comunes

- **Relevar "a ciegas"**: arrancar a preguntar sin saber qué hace cada área. Terminás con una encuesta genérica que nadie valora.
- **No respetar la cadena de autoridad**: pedir directamente a un nivel operativo lo que debe pedirse a un Gerente de Área. Genera fricción y rechazo.
- **Ignorar la formalidad**: pedir evidencias por teléfono o por charla. Si el área no queda comprometida por escrito, el dato no aparece.
- **Creer que la seguridad es "solo de TI"**: los datos personales y los riesgos viven en Comercial, en Pagos y en RRHH. Relevar solo sistemas es inventariar media casa.
- **No validar el organigrama**: usar nombres viejos o cargos ya rotados. Desacredita todo tu trabajo de un golpe.
- **Ir sin objetivo a la reunión**: el área percibe de inmediato que perdés el tiempo, y la próxima invitación se cae.

---

## 8. Ejercicio guiado: dibujá tu mapa de actores

**Objetivo:** que tengas antes de la primera reunión un mapa claro de con quién vas a hablar y en qué orden.

1. **Armá tu cuadro de actores** (papel o planilla):

| Actor | Cargo y área | Sponsor | Qué necesito de él | Prioridad (alta/media) | Primer contacto (fecha) |
|---|---|---|---|---|---|
| Gerencia General | Sponsor del proyecto | — | Resolución de inicio y respaldo | Alta | Semana 1 |
| Cra. Melissa Moraes | Riesgos No Financieros / Oficial de Cumplimiento | Gerencia | Par del RSI, acceso a áreas | Alta | Semana 1-2 |
| ... | | | | | |

2. **Validá cada nombre contra el organigrama vigente** (SF.PLE.05). Tachá y reemplazá los que hayan cambiado.

3. **Trazá el circuito para llegar a cada actor**: quién lo habilita, quién firma la invitación, quién recibe la minuta.

4. **Marcá tus primeros tres contactos** y redactá el correo de presentación: pedí la reunión formal, con agenda previa y la norma que la justifica.

5. **Guardá el mapa** en tu carpeta de proyecto: es la entrada de tu plan de reuniones (RELEV-03).

### 8.1 Guion de presentación por correo

Cuando ya tenés el mapa, el primer contacto se hace por escrito. Un modelo que respeta el circuito del Banco:

> **Asunto:** Relevamiento del SGSI · Solicitud de reunión · Área [X]
>
> *Estimado/a [nombre y cargo]:*
>
> *En el marco de la implementación del Sistema de Gestión de Seguridad de la Información del Banco (PLAN-SGSI-001) y de la resolución de inicio de Gerencia General de fecha [XX], solicitamos amablemente agendar una reunión de 60 minutos con el equipo de [Área/División] para relevar [tema: inventario de información / procesos / sistemas].*
>
> *Adjuntamos la agenda previa y el marco normativo que motiva el pedido (MCU 5.0 de Agesic, normas del BCU y Ley 18.331). Enviaremos la minuta de la reunión en las 48 horas posteriores.*
>
> *Quedamos a disposición para coordinar fecha y hora.*
>
> *Saludos cordiales, [Nombre] · RSI del Banco*

**Qué hacer después de cada contacto:** anotar en el mapa la fecha de envío, la respuesta y la fecha agendada. Si en una semana no hay respuesta, escalá por el sponsor del área con una nota de recordatorio, nunca con presión directa al contacto.

### Lista de verificación del módulo

- ☐ Entiendo el negocio del Banco en una frase y sé explicarlo.
- ☐ Verifiqué los nombres del organigrama contra la versión vigente.
- ☐ Identifiqué las tres líneas de defensa y el lugar recomendado del RSI.
- ☐ Tengo mi mapa de actores con sponsors y prioridades.
- ☐ Sé cómo se piden las cosas por escrito en el Banco.
- ☐ Preparé mi primer correo de presentación formal.

---

**Documentos relacionados:** GV-02, GV-03, ID-01, MATRIZ-001
