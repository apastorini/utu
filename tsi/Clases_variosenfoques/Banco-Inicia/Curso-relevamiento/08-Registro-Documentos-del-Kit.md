# RELEV-08 · Registro: de la conversación al documento del kit

> ⚠️ **Alerta:** este documento menciona **nombres propios del organigrama del Banco** (personas y cargos, abril 2026). Antes de usar el documento, verificá la vigencia de esos nombres contra el organigrama actual.

> **Función del MCU 5.0:** Este módulo cierra la cadena de la función ID (Identificar): lo relevado en reuniones y evidencias se vuelca a los documentos del kit (ID-01, ID-02, ID-03, ID-05) para que el SGSI sea auditable. El registro es donde las palabras se vuelven inventario (ID.AM) y riesgo (ID.RA).
> **ISO/IEC 27001:** La cláusula 7.5 (información documentada) exige que los documentos sean identificados, versionados, revisados y protegidos: un activo registrado sin fecha ni responsable no cumple el estándar.
> **BCU:** El RNRCSF art. 492 exige documentación íntegra y resguardada del software, los datos y la documentación; el registro del relevamiento es la base documental que el BCU audita en el EMG y en la Circular 2227.
> **URCDP:** La Ley 19.670 y el Decreto 64/020 exigen el Documento de Seguridad (URCDP-01), el registro de tratamientos (URCDP-04) y la inscripción de bases: todo nace del registro correcto del relevamiento.
> **Nivel del curso:** 🟢 Descubrir · 🟡 Practicar · 🔴 Dominar

---

## 1. El flujo de trabajo: de la conversación al documento

El relevamiento no termina en la reunión ni en la evidencia: termina cuando la información **se registra** en los documentos del kit. Todo lo que no se registra se pierde; todo lo que se registra mal genera un inventario falso.

```
Reunión de relevamiento (RELEV-06)
        │  minuta + frases textuales
        ▼
Ficha de activo / hallazgos (RELEV-06)
        │  activos, riesgos, tratamientos detectados
        ▼
Cruce con la norma (RELEV-02)   ← norma → pregunta → evidencia
        │  ¿qué requisito cubre cada dato?
        ▼
Volcado a las plantillas del kit
        │  ID-01, ID-02/03, URCDP-01, URCDP-04, GV-02, ID-05, MATRIZ-001
        ▼
Archivo en el repositorio (EST-CARPETAS-001)
        │  nomenclatura [CÓDIGO]_[Nombre]_[VXX.X]_[ESTADO]
        ▼
Control de cambios y versiones
        (higiene del registro, sección 8)
```

> **Recordá verificar contra el organigrama vigente del Banco**: cada activo que registres en ID-01 lleva el área dueña y el responsable actuales; si el organigrama cambió, actualizá el inventario antes de firmar versiones nuevas.

### La regla del doble origen

Todo lo que se vuelca al kit tiene **dos orígenes** posibles, y los dos se registran:

1. **Dicho en reunión** → fuente: minuta RELEV-06, con fecha y nombre del interlocutor.
2. **Evidencia recibida** → fuente: planilla RELEV-07, con ID de solicitud y ubicación del repositorio.

Ningún dato del kit debe quedar sin origen. Si no podés rastrear de dónde salió un activo, ese activo no es auditable.

---

## 2. Cómo volcar a ID-01 (Inventario de Activos)

ID-01 es la columna vertebral del SGSI: sin inventario no hay análisis de riesgos, no hay plan de tratamiento y no hay perfil de ciberseguridad. El relevamiento alimenta el inventario activo por activo, con la ficha de activo como borrador.

### 2.1 Las columnas del inventario

| Columna | Qué se registra | De dónde sale |
|---|---|---|
| Tipo de activo | Sistema, aplicación, base de datos, hardware, documento físico, proceso, persona, instalación | Ficha de activo |
| Nombre | Nombre propio y comercial del activo | Reunión (dato concreto, RELEV-06) |
| Área dueña | División o departamento responsable | Minuta + organigrama vigente |
| Proceso | Proceso de negocio al que sirve | Reunión |
| Clasificación CID | Confidencialidad / Integridad / Disponibilidad (A/M/B) | Análisis del RSI con el área |
| Ubicación | Sede central, sucursal, datacenter, nube | Reunión |
| Responsable | Persona que responde por el activo | Reunión + organigrama |
| Sistema asociado | Sistema del que depende o que lo contiene | Reunión |
| Observaciones | Particularidades, accesos, terceros, dependencias | Minuta + evidencias |

### 2.2 Cómo agrupar por proceso y por área

No ordenes el inventario alfabéticamente: **agrupalos por proceso de negocio y por área dueña**. Así ID-01 se convierte en un mapa de la operación (crédito, ahorro, pagos, canales) y no en una lista de cosas. Cada área del organigrama (Comercial, Operaciones y TI, Administración Financiera, Riesgos, dependencias de Gerencia General) aparece una sola vez como agrupador.

### 2.3 Ejemplo completo (5 líneas)

```text
ID-01 · INVENTARIO DE ACTIVOS · extracto del relevamiento

| Tipo de activo | Nombre | Área dueña | Proceso | CID (C/I/D) | Ubicación | Responsable | Sistema asociado | Observaciones |
|---|---|---|---|---|---|---|---|---|
| Hardware | Servidor del core | Depto. Producción (División TI) | Crédito hipotecario | A/A/A | Datacenter sede central | Ing. Daniel Herrera | Sistema core | Crítico; redundancia a validar (EV-003) |
| Base de datos | Base de Crédito Hipotecario | División Banca Persona | Otorgamiento de crédito | A/A/A | Datacenter (motor: [X]) | Cr. Alvaro Gandolfo | Sistema de crédito | Datos personales: ROPA (URCDP-04) |
| Sistema | Banco En Línea | División Canales y Apoyo Comercial | Banca digital | A/A/A | Datacenter / nube | Lic. Gustavo Bordoni | Core + pasarela de pagos | Canal externo; EIPD pendiente (URCDP-05) |
| Hardware | Firewall perimetral | Depto. Soporte Técnico (División TI) | Red institucional | A/A/A | Datacenter | Tec. Ariel Presa | Red corporativa | Configuración respaldada en [X] |
| Documento físico | Legajos físicos de sucursal | División Banca Persona (sucursales) | Atención presencial | A/M/B | Sucursal [X] | Jefe de sucursal | — | Sin clasificar → riesgo medio (ID-03) |
```

---

## 3. Cómo volcar a URCDP-04 (ROPA e inscripción de bases)

URCDP-04 es el registro de tratamientos de datos personales del Banco: qué bases existen, qué se hace con los datos y bajo qué base legal. Del relevamiento salen las bases reales, sus dueños y sus finalidades.

### 3.1 El registro de tratamientos por base

| Campo | Qué se registra |
|---|---|
| Nombre de la base | Nombre real del sistema o registro |
| Finalidad | Para qué se recolectan los datos |
| Base legal | Ley 18.331, Ley 19.670, consentimiento, obligación legal, interés legítimo |
| Categorías de datos | Datos identificativos, financieros, patrimoniales, sensibles (art. 17 y 18) |
| Interesados | Clientes, socios, empleados, proveedores |
| Destinatarios | Áreas internas, encargados de tratamiento, BCU, organismos públicos |
| Transferencias | Internacionales o a terceros |
| Plazos de retención | Tiempo de conservación y destino al vencer |
| Medidas de seguridad | Medidas técnicas y organizativas aplicadas |
| Inscripción | Estado de la inscripción en el Registro de la URCDP |

### 3.2 Ejemplo completo: Base de Crédito Hipotecario

```text
URCDP-04 · REGISTRO DE TRATAMIENTOS · Base: Crédito Hipotecario

| Campo | Registro |
|---|---|
| Nombre de la base | Base de Crédito Hipotecario |
| Finalidad | Evaluación, otorgamiento, administración y cobranza de créditos hipotecarios |
| Base legal | Ley 18.331; Ley 19.670; relación contractual con el titular |
| Categorías de datos | Identificativos, patrimoniales, financieros, laborales; sin datos sensibles en alta |
| Interesados | Clientes titulares de créditos hipotecarios |
| Destinatarios | División Banca Persona, División Seguimiento y Recuperación de Activos, BCU (información exigida) |
| Transferencias | No hay transferencias internacionales |
| Plazos de retención | Vigencia del crédito + 10 años (obligación BCU), luego supresión o anonimización |
| Medidas de seguridad | Acceso por roles, auditoría de accesos, respaldo diario y prueba anual de restauración |
| Inscripción | Inscripta en el Registro de la URCDP · N° [X] · fecha [DD/MM/AAAA] |
```

### 3.3 Ejercicio resuelto: Base de Socios/Clientes Banco En Línea

En el mismo formato, inventá el registro de la base del canal digital. Relevá en División Canales y Apoyo Comercial la finalidad real, las categorías y el responsable, y completá:

```text
URCDP-04 · REGISTRO DE TRATAMIENTOS · Base: Socios/Clientes Banco En Línea

| Campo | Registro |
|---|---|
| Nombre de la base | Base de Socios/Clientes Banco En Línea |
| Finalidad | Alta, autenticación y operación de la banca en línea; gestión de socios y clientes digitales |
| Base legal | Ley 18.331; Ley 19.670; relación contractual; consentimiento del titular |
| Categorías de datos | Identificativos, de contacto, credenciales de acceso, datos de operaciones |
| Interesados | Socios y clientes del canal digital Banco En Línea |
| Destinatarios | División Canales y Apoyo Comercial, División Operaciones, proveedores de plataforma (encargados) |
| Transferencias | No hay transferencias internacionales |
| Plazos de retención | Vigencia de la relación + plazos legales; baja y depuración según política de retención |
| Medidas de seguridad | Autenticación multifactor, cifrado en tránsito, registro de accesos, EIPD realizada (URCDP-05) |
| Inscripción | Pendiente de inscripción en el Registro de la URCDP → gestionar con Oficial de Cumplimiento |
```

---

## 4. Cómo alimentar ID-02/ID-03 (riesgos)

Los hallazgos de las reuniones son la materia prima del análisis de riesgos. El paso es simple: **un hallazgo malo → un riesgo concreto → una valoración**. Cada riesgo registrado debe tener origen trazable (minuta, evidencia o brecha de la planilla).

### 4.1 Ejemplo: de hallazgo a riesgo

| Hallazgo del relevamiento | Riesgo | Confidencialidad | Integridad | Disponibilidad | Valoración preliminar |
|---|---|---|---|---|---|
| Legajos físicos de sucursal sin clasificar ni custodiar | Divulgación no autorizada de datos personales de clientes | Alta | Media | Baja | Medio |
| No existe registro de prueba anual de restauración | Pérdida de datos ante desastre sin recuperación demostrable | Media | Alta | Alta | Alto |
| Accesos al core sin matriz de roles actualizada | Acceso indebido o excesivo a datos de crédito | Alta | Media | Media | Medio |
| Base de Socios Banco En Línea sin EIPD | Daño a titulares por tratamiento no evaluado | Media | Baja | Baja | Medio |
| Respaldos y claves de encriptación gestionados por la misma área | Indisponibilidad de datos si el evento afecta a ambos | Media | Alta | Alta | Alto |

### 4.2 Del riesgo al plan de tratamiento (ID-04)

Cada riesgo valorado pasa a ID-04 con una opción de tratamiento: mitigar (crear el control), transferir (seguro o tercero), aceptar (con autorización formal del dueño del riesgo) o evitar. El relevamiento no solo detecta riesgos: detecta también **controles que ya existen** (autenticación multifactor, respaldo diario, auditoría de accesos), y esos controles se registran en ID-03 como mitigaciones vigentes.

### 4.3 Del riesgo al perfil (ID-05)

ID-05 (Perfil de ciberseguridad) se alimenta con la foto agregada: cuántos activos críticos sin control, qué categorías de MCU 5.0 (ID.AM, ID.RA, ID.IM, PR.AT, PR.DS, DE.CM, RS.CO, RC.RP) están por debajo del objetivo. Cada brecha de evidencia (RELEV-07) baja el perfil en su categoría y aparece en el plan de mejora.

---

## 5. Cómo alimentar URCDP-01 (Documento de Seguridad)

El Documento de Seguridad declara las medidas aplicadas a las bases de datos personales. El relevamiento permite confrontar **lo que el documento declara con lo que el banco realmente hace**:

| Sección de URCDP-01 | Qué completa el relevamiento |
|---|---|
| Identificación de las bases y sus responsables | El listado de bases de URCDP-04, salido de las reuniones |
| Medidas organizativas | Roles y funciones reales relevados (PR-02), procedimientos de acceso |
| Medidas técnicas | Cifrado, respaldo, monitoreo detectados en el relevamiento de TI |
| Medidas de control de acceso | Autorizaciones y revisiones de accesos relevadas |
| Procedimientos de revisión y auditoría | Registros y evidencias que el área entrega y su periodicidad |
| Incidencias y notificación | Canal y responsables de la notificación (Ley 19.670 art. 38) |
| Capacitación | Registros de concientización (PR.AT) existentes en el área |

> **Medidas declaradas vs medidas reales:** si el Documento de Seguridad dice "respaldo diario con prueba anual" pero la evidencia muestra que no hay prueba anual registrada, el documento se corrige a la realidad y la brecha se trata en ID-04. El Documento de Seguridad nunca debe decir más de lo que la evidencia demuestra.

---

## 6. Cómo alimentar GV-02, ID-05 y MATRIZ-001

### 6.1 GV-02 (Alcance del SGSI)

El alcance se define con la evidencia del territorio: qué áreas, procesos, sistemas e instalaciones quedan dentro del SGSI. El relevamiento muestra qué existe (ID-01), qué tan crítico es (ID-03) y dónde están los datos personales (URCDP-04). Con ese mapa se justifica cada inclusión y cada exclusión del alcance, y el mapa se actualiza cuando el alcance cambia.

### 6.2 ID-05 (Perfil de ciberseguridad)

El perfil compara el estado actual (resultado del relevamiento) con el estado objetivo (definido por el Directorio). Cada categoría de MCU 5.0 se puntúa con los datos reales: cobertura de inventario, madurez del análisis de riesgos, controles de protección, monitoreo, respuesta y recuperación. El delta entre "actual" y "objetivo" es la cartera de trabajo de ID-04.

### 6.3 MATRIZ-001 (Norma → requisito → evidencia)

La matriz es el puente de auditoría: cada requisito normativo se enlaza con la evidencia que lo demuestra y con el registro que lo documenta. Del relevamiento salen las **filas nuevas** de la matriz: requisito → pregunta de RELEV-02 → evidencia (ID de la planilla RELEV-07) → ubicación en el repositorio → estado.

---

## 7. Tabla maestra: del insumo al documento del kit

| Insumo del relevamiento | Documento del kit | Sección del documento | Responsable | Carpeta del repositorio |
|---|---|---|---|---|
| Fichas de activo y diagramas | ID-01 | Inventario completo | RSI + áreas dueñas | 01-IDENTIFICACION |
| Hallazgos y brechas | ID-02 | Metodología y criterios de valoración | RSI | 01-IDENTIFICACION |
| Hallazgos y brechas de evidencia | ID-03 | Análisis de riesgos (inventario de riesgos) | RSI | 01-IDENTIFICACION |
| Riesgos valorados | ID-04 | Plan de tratamiento con responsables y plazos | RSI + dueños de riesgo | 01-IDENTIFICACION |
| Estado agregado de controles | ID-05 | Perfil actual vs objetivo por categoría MCU | RSI | 01-IDENTIFICACION |
| Medidas reales de cada área | URCDP-01 | Medidas organizativas, técnicas y procedimientos | DPD + RSI | 06-CUMPLIMIENTO/URCDP |
| Bases detectadas en reuniones | URCDP-04 | Registro de tratamientos por base | DPD | 06-CUMPLIMIENTO/URCDP |
| Mapa de áreas, procesos y sistemas | GV-02 | Alcance del SGSI (inclusiones y exclusiones) | RSI | 00-GOBERNANZA |
| Requisito → pregunta → evidencia | MATRIZ-001 | Filas de correspondencia normativa | RSI | 00-PLANIFICACION |
| Evidencias validadas | (enlaces) | Cualquier documento que las cite | RSI | Según EST-CARPETAS-001 |

> **Un insumo, un dueño de registro:** cada documento del kit tiene un responsable único que consolida los insumos. El RSI consolida ID-01 a ID-05 y GV-02; el DPD consolida URCDP-01 y URCDP-04. Evitá que dos personas vuelquen la misma información por separado.

---

## 8. Higiene del registro

El registro profesional no es solo completar plantillas: es mantener la disciplina de la información documentada. Estas son las reglas que evitan que el kit se pudra con el tiempo.

| Regla | Práctica |
|---|---|
| Fechar todo | Toda versión lleva fecha de emisión y de actualización |
| Versionar | V01.0 inicial; V01.1 corrección menor; V02.0 cambio sustancial |
| Nombrar responsables | Cada cambio registra quién lo hizo y quién lo aprobó |
| No dejar datos en correos | Los datos del relevamiento viajan a la minuta/planilla, nunca quedan solo en el hilo de correo |
| Un solo lugar de verdad | La versión oficial vive en el repositorio (EST-CARPETAS-001); los borradores se identifican como tales y se archivan o eliminan |
| Control de cambios | Registrar qué cambió, por qué y en qué versión (tabla de control en cada documento) |
| Revisión periódica | Revisar cada documento del kit contra la realidad al menos semestralmente o ante cambios de organigrama |
| Respaldo del repositorio | El repositorio del SGSI también se respalda y se prueba (mismo estándar que pide el art. 492) |

### Ejemplo de tabla de control de cambios

```text
CONTROL DE CAMBIOS · ID-01 (extracto)
| Versión | Fecha | Cambio | Realizó | Aprobó |
|---------|-------|--------|---------|--------|
| V01.0   | 10/03/2026 | Carga inicial del relevamiento de Banca Persona | [RSI] | [Jefe División] |
| V01.1   | 24/03/2026 | Corrección área dueña de la Base de Crédito Hipotecario | [RSI] | [Área] |
| V02.0   | 15/05/2026 | Incorporación de Banco En Línea y activos de TI | [RSI] | [Comité de Seguridad] |
```

---

## 9. Errores comunes del registro

| Error | Consecuencia | Cómo evitarlo |
|---|---|---|
| Registrar solo en la memoria | La información se pierde con la rotación de personal | Volcar todo en el kit, con origen trazable |
| Volcar solo lo que se entendió | Inventario incompleto que "desaparece" activos | Volcar desde la minuta y la ficha, no desde el recuerdo |
| No fechar ni versionar | Imposible auditar; no se sabe qué versión es vigente | Tabla de control de cambios en cada documento |
| Duplicar información en dos documentos | Versiones que se contradicen | Un solo lugar de verdad + enlaces |
| No actualizar versiones al corregir | Circula una versión vieja como oficial | Versionar cada cambio, archivar las anteriores |
| Copiar de memoria a ID-01 sin verificar organigrama | Áreas y responsables desactualizados | Verificar contra el organigrama vigente del Banco |
| Guardar la evidencia solo en el correo | Pérdida del vínculo requisito→evidencia | Archivar en EST-CARPETAS-001 y enlazar en la matriz |
| Dejar los datos personales en notas sueltas | Riesgo de fuga durante el propio relevamiento | Los datos van al ROPA y al Documento de Seguridad, cifrados y con acceso restringido |

---

## 10. Cierre del módulo

Cerraste la cadena completa: la conversación de la reunión se volcó a ID-01 con columnas y ejemplos completos, las bases personales se registraron en URCDP-04 con el formato ROPA, los hallazgos se convirtieron en riesgos valorados para ID-02/ID-03/ID-04/ID-05, las medidas reales alimentaron URCDP-01, el mapa alimentó GV-02 y la matriz MATRIZ-001, y todo quedó fechado, versionado y en un solo lugar de verdad. El relevamiento ya no es conversación: es el territorio documentado del SGSI del Banco.

---

**Documentos relacionados:** ID-01, ID-02, ID-03, ID-04, ID-05, URCDP-01, URCDP-04, GV-02, MATRIZ-001
