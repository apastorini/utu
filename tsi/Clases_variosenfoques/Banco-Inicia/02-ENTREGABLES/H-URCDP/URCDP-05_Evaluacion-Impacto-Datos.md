# URCDP-05 · Evaluación de Impacto en Protección de Datos (EIPD / DPIA) del Banco
> **Función del MCU 5.0:** Identificar (ID.RA — Evaluación de riesgos) · Gobernar (GV.RM)
> **ISO/IEC 27001:** Cláusula 6.1 (Planificación) · A.8.12 (Protección de datos)
> **BCU:** Circular 2227 (evaluación de riesgos del riesgo operativo)
> **URCDP:** **Ley 18.331 art. 12** · **Decreto 64/020 art. 6 lit. f** (evaluación de impacto) · Ley 19.670 (responsabilidad proactiva) · Decreto 64/020 arts. 7-8 (privacidad por diseño)
> **Nivel del curso:** 🔴 Dominar

## 1. Qué es y por qué existe
La **Evaluación de Impacto en la Protección de Datos (EIPD o DPIA)** es un análisis previo de los riesgos que un tratamiento de datos personales implica para los derechos y libertades de los titulares. El **art. 12 de la Ley 18.331** establece la evaluación de riesgos como base de las medidas de seguridad, y el **art. 6 lit. f del Decreto 64/020** la hace **obligatoria** cuando el tratamiento implique alto riesgo, incluyendo: datos sensibles, datos de más de 35.000 personas, datos biométricos, decisiones automatizadas con efectos jurídicos, transferencias internacionales a países no adecuados y personas vulnerables o especialmente protegidas.
El Banco realiza tratamientos que **claramente** caen en estos supuestos: el **sistema de crédito hipotecario** trata datos financieros y patrimoniales de decenas de miles de personas y puede incluir datos de salud en garantías; **Banco En Línea** agrupa datos de más de 35.000 usuarios y toma decisiones automatizadas de admisión en línea; la **videovigilancia** de sucursales capta imágenes (datos biométricos implícitos) de personas vulnerables que transitan; y el proceso de **scoring o evaluación de solvencia** puede implicar valoraciones automatizadas de conducta.
La EIPD no es un trámite burocrático: es la herramienta que permite **decidir** si un tratamiento nuevo o modificado es proporcionado, qué medidas minimizan los riesgos y si corresponde consultar previamente a la URCDP. Integrada con la metodología de riesgos del SGSI (ID-02), convierte el cumplimiento legal en parte del diseño de los sistemas, conforme a la privacidad por diseño y por defecto del Decreto 64/020 (arts. 7-8).
## 2. Marco de referencia
| **Marco** | **Referencia** | **Qué exige** |
|---|---|---|
| **MCU 5.0 (Agesic)** | ID.RA · GV.RM | Evaluar riesgos antes de operar y alinear con la estrategia |
| **ISO/IEC 27001** | Cláusula 6.1 · A.8.12 | Evaluación de riesgos para los activos de información y datos |
| **BCU** | Circular 2227 | Evaluación previa de riesgos de los procesos y sistemas |
| **URCDP** | **Ley 18.331 art. 12** · **Decreto 64/020 art. 6 lit. f** · arts. 7-8 | EIPD obligatoria en tratamientos de alto riesgo; consulta previa a la URCDP; privacidad por diseño y por defecto |

## 3. Cómo completar esta plantilla (guía de llenado)
1. **Completá el encabezado** con los datos de la evaluación (una por tratamiento, no una por documento).
2. **Describí el tratamiento** con detalle (qué datos, de quiénes, para qué, por qué medios).
3. **Verificá si la EIPD es obligatoria**: aplicá los criterios del art. 6 lit. f del Decreto 64/020; si es dudoso, documentá la decisión de realizarla o no.
4. **Evaluá necesidad y proporcionalidad**: ¿la finalidad es legítima? ¿es el medio menos intrusivo?
5. **Identificá los riesgos para los titulares** (probabilidad × severidad) con la metodología de ID-02.
6. **Definí las medidas** para mitigar cada riesgo y el riesgo residual resultante.
7. **Someté la evaluación al DPD** para su aprobación y opinión.
8. **Determiná si se consulta a la URCDP** antes de iniciar el tratamiento (riesgo residual alto).
9. **Revisá la EIPD** cuando cambien el tratamiento, la tecnología o el riesgo.
**A quién consultar en el Banco:** DPD (aprueba y lidera la EIPD); RSI (riesgos técnicos); dueño del proceso (Área Comercial para crédito, Canales para Banco En Línea, Servicios Generales para videovigilancia); Gerente de División TI (privacidad por diseño); División Servicios Jurídicos Notariales (marco legal).
## 4. Plantilla del documento

### ENCABEZADO
| **Campo** | **Valor** |
|---|---|
| **Código** | URCDP-05 |
| **Título** | Evaluación de Impacto en Protección de Datos (EIPD / DPIA) |
| **Versión** | 1.0 |
| **Estado** | [Borrador / En revisión / Aprobado] |
| **Fecha de aprobación** | [COMPLETAR] |
| **Elaborado por** | [COMPLETAR: DPD / unidad dueña del tratamiento] |
| **Revisado por** | RSI |
| **Aprobado por** | DPD |
| **Clasificación** | Uso interno — restringido |
| **Próxima revisión** | [Fecha o condición de revisión] |

### 1. Identificación del tratamiento
| **Campo** | **Detalle** |
|---|---|
| **Nombre del tratamiento** | [COMPLETAR] |
| **Unidad responsable** | [COMPLETAR] |
| **Encargados** | [COMPLETAR] |
| **Base de licitud** | [COMPLETAR: consentimiento / ley / contrato / interés público] |
| **Categorías de datos** | [COMPLETAR] |
| **Titulares** | [COMPLETAR: segmento y número estimado] |
| **Transferencias internacionales** | [COMPLETAR] |
| **Inscripción URCDP** | [COMPLETAR: n.º] |

### 2. ¿La EIPD es obligatoria? (Decreto 64/020 art. 6 lit. f)
| **Criterio** | **¿Aplica?** | **Justificación** |
|---|---|---|
| Datos sensibles (salud, origen, religión, etc.) | [Sí / No] | [COMPLETAR] |
| Datos de más de 35.000 personas | [Sí / No] | [COMPLETAR] |
| Datos biométricos | [Sí / No] | [COMPLETAR] |
| Decisiones automatizadas con efectos jurídicos | [Sí / No] | [COMPLETAR] |
| Personas vulnerables o especialmente protegidas | [Sí / No] | [COMPLETAR] |
| Transferencias a países no adecuados | [Sí / No] | [COMPLETAR] |

### 3. Descripción del tratamiento
[COMPLETAR: flujo del tratamiento, fuentes de datos, medios de recolección, sistemas utilizados, accesos, plazo de conservación y destino final de los datos.]
### 4. Necesidad y proporcionalidad
[COMPLETAR: finalidad legítima, alternativas consideradas, minimización de datos, existencia de medios menos intrusivos, expectativa razonable del titular.]
### 5. Identificación y evaluación de riesgos para los titulares
| **N.º** | **Riesgo** | **Datos afectados** | **Probabilidad (1-5)** | **Severidad (1-5)** | **Nivel (P×S)** | **Titular afectado** |
|---|---|---|---|---|---|---|
| 1 | [COMPLETAR: acceso no autorizado] | [COMPLETAR] | [COMPLETAR] | [COMPLETAR] | [COMPLETAR] | [COMPLETAR] |
| 2 | [COMPLETAR: pérdida o robo de equipos] | [COMPLETAR] | [COMPLETAR] | [COMPLETAR] | [COMPLETAR] | [COMPLETAR] |
| 3 | [COMPLETAR: uso indebido / finalidad distinta] | [COMPLETAR] | [COMPLETAR] | [COMPLETAR] | [COMPLETAR] | [COMPLETAR] |

### 6. Medidas para mitigar los riesgos
| **N.º** | **Riesgo** | **Medida prevista** | **Riesgo residual** |
|---|---|---|---|
| 1 | [COMPLETAR] | [COMPLETAR: control técnico, organizativo o físico] | [COMPLETAR] |
| 2 | [COMPLETAR] | [COMPLETAR] | [COMPLETAR] |
| 3 | [COMPLETAR] | [COMPLETAR] | [COMPLETAR] |

### 7. Opinión del DPD
El DPD valida la evaluación, verifica que las medidas sean necesarias y proporcionadas, y resuelve si el tratamiento puede iniciarse y en qué condiciones [COMPLETAR: opinión y firma].
### 8. Consulta previa a la URCDP
Si, aun con las medidas, el riesgo residual es alto, se consulta a la **URCDP antes de iniciar el tratamiento**, acompañando la EIPD [COMPLETAR: resultado de la consulta].
### 9. Revisión
La EIPD se revisa ante cambios significativos del tratamiento, de la tecnología, del marco normativo o del perfil de riesgo. La revisión se registra en el control de cambios.
### Control de cambios
| **Versión** | **Fecha** | **Cambio** | **Elaboró** | **Aprobó** |
|---|---|---|---|---|
| 0.1 | [COMPLETAR] | Versión inicial (borrador) | [COMPLETAR] | DPD |
| 1.0 | [COMPLETAR] | Aprobación del DPD | [COMPLETAR] | DPD |

## 5. Ejemplo aplicado al Banco (modelo de referencia)
Ejemplo ilustrativo de cómo quedaría completado. Adaptá a la realidad institucional del Banco.
**Ejemplo 1 — Videovigilancia en sucursales:** tratamiento de imágenes captadas por cámaras en casa central y sucursales. EIPD obligatoria por datos biométricos implícitos y personas vulnerables (niños, adultos mayores). Riesgos: acceso no autorizado a las grabaciones (controlado con acceso restringido, cifrado y registro), pérdida de imágenes (respaldos), conservación excesiva (borrado automático a los [X] días). Medidas: cartelería aprobada, perímetro físico, control de accesos por perfiles, minimización de puntos de captura, retención limitada. Riesgo residual: bajo. No requiere consulta a la URCDP.
**Ejemplo 2 — Banco En Línea:** tratamiento de datos de más de 35.000 usuarios del portal, con autenticación y decisiones automatizadas de admisión a trámites en línea. EIPD obligatoria por volumen (>35.000) y por decisiones automatizadas con efectos jurídicos. Riesgos: robo de credenciales y acceso a datos de clientes (mitigado con autenticación multifactor, detección de anomalías, monitoreo), filtración de datos (cifrado, minimización), decisión automatizada errónea que perjudique al titular (derecho a impugnación de valoraciones, revisión humana). Riesgo residual: bajo a moderado; se documenta la revisión anual y la actualización ante nuevos servicios.
**Ejemplo 3 — Datos de salud en garantías:** el sistema de crédito hipotecario recibe certificados de incapacidad o información de salud como parte de las garantías en algunos productos. EIPD obligatoria por datos sensibles. Medidas: acceso limitado a los perfiles autorizados, seudonimización cuando es posible, cifrado, registro de accesos, segregación de la información de salud del resto del expediente. Riesgo residual: bajo. Se registró la opinión del DPD y la revisión anual.

**Documentos relacionados:** URCDP-01 (Documento de Seguridad), URCDP-02 (Vulneraciones), URCDP-04 (Inscripción de bases), URCDP-06 (DPD), ID-02 (Metodología de riesgos), BCU-02 (Marco de Riesgos), GV-01 (Política).
