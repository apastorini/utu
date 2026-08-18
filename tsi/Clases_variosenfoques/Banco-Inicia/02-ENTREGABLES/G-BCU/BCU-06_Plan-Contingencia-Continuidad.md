# BCU-06 · Plan de Contingencia y Continuidad del Negocio del Banco

> ⚠️ **Alerta:** este documento menciona **nombres propios del organigrama del Banco** (personas y cargos, abril 2026). Antes de usar el documento, verificá la vigencia de esos nombres contra el organigrama actual.
> **Función del MCU 5.0:** Recuperar (RC.RP — Ejecución del plan de recuperación · RC.CO — Comunicación de la recuperación) · Identificar (ID.IM — Mejora)
> **ISO/IEC 27001:** A.5.29 (Seguridad en redes) · A.5.30 (Preparación de TIC para la continuidad) · Cláusula 8
> **BCU:** Estándares Mínimos de Gestión — Continuidad del negocio · RNRCSF art. 492 (resguardo y pruebas anuales) · Circular 2227
> **URCDP:** Ley 18.331 art. 10 · Ley 19.670 art. 38 (comunicación de vulneraciones en situaciones de contingencia)
> **Nivel del curso:** 🔴 Dominar

## 1. Qué es y por qué existe
La **continuidad del negocio** es el último eslabón del marco de gestión que el BCU evalúa: si todo lo demás falla, la entidad debe poder **seguir operando o recuperarse** dentro de límites aceptables. El Banco, como banco público que otorga crédito hipotecario, gestiona el ahorro y opera un departamento de pagos, tiene un deber de continuidad frente a sus clientes y al sistema financiero. El plan define cómo responder ante fallas tecnológicas, desastres naturales y ciberataques.
El BCU espera que la continuidad sea **proporcional al riesgo y al impacto**: se identifica qué procesos son críticos (BIA), se definen objetivos de recuperación (RTO/RPO), se diseñan planes por escenario y se **prueban al menos una vez al año**. El art. 492 de la RNRCSF suma una exigencia técnica: los resguardos de datos deben permitir reconstruir las operaciones y no pueden verse afectados por un mismo evento, con pruebas anuales de recuperación e integridad.
Además, la continuidad es un momento de máxima exposición para los datos personales: en una contingencia es cuando se pierden, se filtran o se accede indebidamente a datos. El plan debe integrarse con el esquema de incidentes (RS-01) y, cuando corresponda, con la notificación a la URCDP dentro de las 72 horas (URCDP-02). El BCU, por su parte, debe ser informado ante contingencias significativas que afecten la operación.
## 2. Marco de referencia
| **Marco** | **Referencia** | **Qué exige** |
|---|---|---|
| **MCU 5.0 (Agesic)** | RC.RP · RC.CO · ID.IM | Ejecución del plan de recuperación, comunicación de la recuperación y mejora continua |
| **ISO/IEC 27001** | A.5.29 · A.5.30 · Cláusula 8 | Preparación de las TIC para la continuidad, redundancia y pruebas |
| **BCU** | EMG · Continuidad del negocio · RNRCSF art. 492 · Circular 2227 · Circular 2280 | BIA, RTO/RPO, planes por escenario, pruebas anuales, comunicación al BCU |
| **URCDP** | Ley 18.331 art. 10 · Ley 19.670 art. 38 | Proteger los datos durante la contingencia; notificar vulneraciones a la URCDP en plazo |

## 3. Cómo completar esta plantilla (guía de llenado)
1. **Completá el encabezado** con los datos del documento.
2. **Realizá el Análisis de Impacto en el Negocio (BIA)** sobre los procesos del Banco (crédito, ahorro, pagos, canales) y definí los RTO/RPO por proceso crítico.
3. **Definí los escenarios de contingencia** (falla tecnológica, desastre natural, ciberataque) y el plan aplicable a cada uno.
4. **Detallá los procedimientos de activación**: quién declara la contingencia, cómo se convoca al equipo, cómo se escala.
5. **Diseñá el plan de resguardo y recuperación de datos** cumpliendo el art. 492 (copias fuera del sitio, claves, pruebas anuales).
6. **Definí las pruebas y simulacros anuales**, con plan, participación y registro de resultados.
7. **Establecé la comunicación al BCU** ante contingencias significativas y a la URCDP/CERTuy ante vulneraciones de datos (URCDP-02).
8. **Integralo con RS-01/RS-02** (incidentes) y con PR-05 (respaldo) y RC-02 (DRP) para no duplicar ni contradecir.
**A quién consultar en el Banco:** Jefe de Riesgos No Financieros (Cra. Melissa Moraes) por el BIA y el marco de continuidad; División TI — Producción (Ing. Daniel Herrera) por los RTO/RPO técnicos y el resguardo; Departamento de Sistema de Pagos (Cr. Guillermo Correa) por la continuidad de pagos; Gerencia General por la declaración de contingencia; Comunicaciones Institucionales por la comunicación de crisis.
## 4. Plantilla del documento

### ENCABEZADO
| **Campo** | **Valor** |
|---|---|
| **Código** | BCU-06 |
| **Título** | Plan de Contingencia y Continuidad del Negocio |
| **Versión** | 1.0 |
| **Estado** | [Borrador / En revisión / Aprobado] |
| **Fecha de aprobación** | [COMPLETAR] |
| **Elaborado por** | RSI / Riesgos No Financieros |
| **Revisado por** | Comité de Seguridad de la Información |
| **Aprobado por** | Directorio |
| **Clasificación** | Uso interno — restringido |
| **Próxima revisión** | [Fecha, máx. 1 año] |

### 1. Objetivo
Establecer el marco de continuidad del negocio del Banco: identificación de procesos críticos, objetivos de recuperación, planes de contingencia por escenario, resguardo de datos y pruebas anuales, en cumplimiento de los Estándares Mínimos de Gestión del BCU y del art. 492 de la RNRCSF.
### 2. Alcance
Aplica a [COMPLETAR: todos los procesos, sistemas, instalaciones y personas del Banco necesarios para sostener los servicios críticos: crédito hipotecario, ahorro, sistema de pagos, canales de atención y administración de clientes], en casa central, sucursales y dependencias.
### 3. Análisis de Impacto en el Negocio (BIA)
| **Proceso crítico** | **Impacto de la interrupción** | **RTO** | **RPO** | **Prioridad** |
|---|---|---|---|---|
| [COMPLETAR: Crédito hipotecario] | [COMPLETAR] | [COMPLETAR] | [COMPLETAR] | [COMPLETAR] |
| [COMPLETAR: Ahorro y depósitos] | [COMPLETAR] | [COMPLETAR] | [COMPLETAR] | [COMPLETAR] |
| [COMPLETAR: Sistema de pagos] | [COMPLETAR] | [COMPLETAR] | [COMPLETAR] | [COMPLETAR] |
| [COMPLETAR: Canales de atención] | [COMPLETAR] | [COMPLETAR] | [COMPLETAR] | [COMPLETAR] |

### 4. Escenarios y estrategias de contingencia
| **Escenario** | **Respuesta** | **Plan asociado** |
|---|---|---|
| **Falla tecnológica** | Activación de respaldo del sitio, recuperación de servicios desde el sitio alternativo | RC-02 (DRP) |
| **Desastre natural / pérdida del sitio** | Operación desde el sitio alternativo y/o trabajo remoto | RC-02, RC-01 |
| **Ciberataque (incluye cifrado de datos)** | Contención, aislamiento, recuperación desde copias limpias, notificación | RS-01, RS-02, URCDP-02 |
| **Interrupción de proveedores/terceros** | Plan de contingencia del proveedor y migración a alternativa | GV-05 |

### 5. Resguardo de datos (art. 492 RNRCSF)
a) Se resguardan los datos, software y documentación necesarios para reconstruir las operaciones.
b) Las copias se mantienen separadas física y/o lógicamente para no verse afectadas por un mismo evento.
c) Las claves de desencriptación se resguardan con doble control [COMPLETAR: custodio y ubicación].
d) Se designa un responsable del resguardo de categoría superior [COMPLETAR: cargo].
e) Se ejecutan **pruebas anuales de recuperación e integridad** de toda la información, con registro de resultados.
### 6. Activación de la contingencia
a) Cualquier funcionario con conocimiento del evento reporta al canal de activación [COMPLETAR: número/contacto].
b) El [COMPLETAR: Comité de Crisis / Gerencia General] declara la contingencia y activa el plan correspondiente.
c) Se convoca al equipo de continuidad [COMPLETAR: miembros y roles] y se establece el centro de comando.
d) Se registra el evento, las decisiones y el cronograma de recuperación en el informe de contingencia.
### 7. Pruebas y simulacros anuales
| **Prueba** | **Objetivo** | **Frecuencia** | **Alcance** |
|---|---|---|---|
| Recuperación del resguardo (art. 492) | Verificar recuperación e integridad de la información | Anual | [COMPLETAR: toda la información] |
| Simulacro de ciberataque | Ejercitar respuesta ante incidente mayor | Anual | [COMPLETAR] |
| Simulacro de desastre / sitio alternativo | Verificar la operación desde el sitio alternativo | Anual | [COMPLETAR] |
| Simulacro de comunicaciones de crisis | Ejercitar mensajes y canales | Anual | [COMPLETAR] |

Los resultados se documentan, se corrigen las debilidades y se actualiza el plan. El resumen se reporta al Comité y al Directorio.
### 8. Comunicación al BCU y a las autoridades
Ante una contingencia significativa que afecte la operación o los servicios, el Banco comunica al BCU [COMPLETAR: dentro del plazo y por el canal establecidos por el supervisor]. Si la contingencia implica una vulneración de datos personales, se aplica URCDP-02 (inicio de procedimientos en 24 h; comunicación a la URCDP en máx. 72 h; comunicación a los titulares; coordinación con CERTuy).
### 9. Vigencia y revisión
El plan se revisa al menos anualmente o ante cambios significativos (organización, sistemas, procesos, normativa). Los resultados de pruebas y los eventos reales alimentan la mejora continua (ID.IM).
### Control de cambios
| **Versión** | **Fecha** | **Cambio** | **Elaboró** | **Aprobó** |
|---|---|---|---|---|
| 0.1 | [COMPLETAR] | Versión inicial (borrador) | Riesgos No Financieros | — |
| 1.0 | [COMPLETAR] | Aprobación del Directorio | Riesgos No Financieros | Directorio |

## 5. Ejemplo aplicado al Banco (modelo de referencia)
Ejemplo ilustrativo de cómo quedaría completado. Adaptá a la realidad institucional del Banco.
**BIA (ejemplo):** el sistema de crédito hipotecario, el ahorro y el sistema de pagos fueron clasificados como procesos críticos. Para el sistema central de crédito se definió RTO de 4 horas y RPO de 15 minutos; para pagos, RTO de 2 horas en horario de operación (Circular 2280); para canales, RTO de 8 horas. El BIA se actualizó con la participación de las áreas de negocio.
**Resguardo (ejemplo):** la División TI ejecuta respaldos incrementales cada 15 minutos del sistema central hacia un sitio alterno geográficamente separado, con las claves de desencriptación resguardadas bajo doble custodia. En la prueba anual de [fecha], se recuperó la totalidad de la información en [X] horas con verificación de integridad, cumpliendo el art. 492.
**Simulacro (ejemplo):** en [mes] se ejecutó un simulacro de ciberataque de tipo ransomware sobre el entorno de pruebas: se activó el Comité de Crisis, se contuvo el avance, se recuperó desde copias limpias y se practicó la comunicación interna. La lección aprendida (demora en la decisión de desconectar la red) derivó en la actualización de los umbrales de escalamiento.
**Comunicación (ejemplo):** ante una interrupción del portal Banco En Línea por falla del proveedor de nube, el Banco comunicó la contingencia al BCU dentro del plazo, informó a los clientes por los canales disponibles y restableció el servicio dentro del RTO. No hubo exposición de datos personales; de haberla, se habría notificado a la URCDP conforme a URCDP-02.

**Documentos relacionados:** BCU-01 (Gobierno), BCU-02 (Marco de Riesgos), RC-01 (BCP), RC-02 (DRP), RC-03 (Comunicación de crisis), RC-04 (Lecciones aprendidas), RS-01/RS-02 (Incidentes), PR-05 (Respaldo), URCDP-02 (Vulneraciones), GV-05 (Terceros).
