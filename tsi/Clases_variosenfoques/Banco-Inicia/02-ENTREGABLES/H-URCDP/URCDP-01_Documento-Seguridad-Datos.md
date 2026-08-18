# URCDP-01 · Documento de Seguridad de Datos Personales del Banco
> **Función del MCU 5.0:** Proteger (PR.DS — Seguridad de los datos) · Identificar (ID.AM — Inventario)
> **ISO/IEC 27001:** A.5.9 (Inventario) · A.8.12 (Protección de datos) · A.8.13 (Respaldos) · A.8.15 (Registros de eventos)
> **BCU:** RNRCSF art. 492 (resguardo) · Circular 2227 (riesgo operativo)
> **URCDP:** **Ley 18.331 art. 10** (medidas de seguridad) · **Decreto 64/020 arts. 3 y 4** (medidas y condiciones) · Decreto 414/009
> **Nivel del curso:** 🟡 Practicar · 🔴 Dominar

## 1. Qué es y por qué existe
El **Documento de Seguridad de Datos Personales** es la concreción del principio de seguridad del art. 10 de la Ley 18.331: todo responsable de bases de datos personales debe adoptar las medidas necesarias para garantizar la seguridad y confidencialidad de los datos, y **queda prohibido registrar datos en bases que no reúnan condiciones técnicas de integridad y seguridad**. El documento es la evidencia escrita, base por base, de qué datos trata el Banco y con qué medidas los protege.
El Decreto 64/020 (arts. 3-4) refuerza que las medidas deben ser **necesarias**, no solo idóneas, y que se deben valorar estándares nacionales e internacionales — con referencia expresa al **Marco de Ciberseguridad de Agesic**. Por eso este documento se integra al SGSI: cada base de datos personales se protege con los mismos controles técnicos y organizativos del resto de la información, pero documentada específicamente.
Este documento además: alimenta el **Registro de Operaciones de Tratamiento (ROPA)** que la responsabilidad proactiva de la Ley 19.670 y el enfoque del DPD exigen; sirve de base para las inscripciones de bases ante la URCDP (URCDP-04); y es el primer documento que la URCDP solicita en una inspección. El Banco trata datos de clientes (crédito, ahorro, pagos), de funcionarios (RRHH), de videovigilancia en sucursales y de otras categorías; cada una exige su ficha.
## 2. Marco de referencia
| **Marco** | **Referencia** | **Qué exige** |
|---|---|---|
| **MCU 5.0 (Agesic)** | PR.DS · ID.AM | Inventariar los activos de datos y protegerlos según su clasificación |
| **ISO/IEC 27001** | A.5.9 · A.8.12 · A.8.13 · A.8.15 | Inventario de activos, protección de datos, respaldos y registros |
| **BCU** | RNRCSF art. 492 · Circular 2227 | Resguardo de datos y gestión del riesgo operativo que los involucra |
| **URCDP** | **Ley 18.331 art. 10** · **Decreto 64/020 arts. 3-4** | Medidas necesarias de seguridad por base; condiciones técnicas de integridad y seguridad; estándares nacionales e internacionales |

## 3. Cómo completar esta plantilla (guía de llenado)
1. **Completá el encabezado** con los datos del documento.
2. **Inventariá todas las bases de datos de datos personales** del Banco (no solo las informáticas: también archivos, videovigilancia, legajos).
3. **Para cada base completá una ficha** (sección 4.3): descripción, finalidad, categorías de datos, medidas de seguridad, retención y responsables.
4. **Detallá las medidas de seguridad por dominio**: físicas, lógicas y organizativas (mínimo las que exige el art. 10 y el Decreto 64/020 art. 3).
5. **Definí las políticas de retención y borrado seguro** por categoría de datos.
6. **Construí el ROPA** (Registro de Operaciones de Tratamiento) a partir de las fichas.
7. **Revisá y actualizá** el documento cada vez que cambie una base o un tratamiento, y al menos anualmente.
8. **Conservá la evidencia de la revisión** en el control de cambios.
**A quién consultar en el Banco:** DPD (responsable de este documento y del cumplimiento URCDP); RSI (medidas de seguridad técnica); Gerente de División TI (controles lógicos); División Capital Humano (datos de funcionarios); Departamento de Servicios Generales (videovigilancia y archivo físico); División Servicios Jurídicos Notariales (contratos y encargados).
## 4. Plantilla del documento

### ENCABEZADO
| **Campo** | **Valor** |
|---|---|
| **Código** | URCDP-01 |
| **Título** | Documento de Seguridad de Datos Personales |
| **Versión** | 1.0 |
| **Estado** | [Borrador / En revisión / Aprobado] |
| **Fecha de aprobación** | [COMPLETAR] |
| **Elaborado por** | DPD |
| **Revisado por** | RSI / Comité de Seguridad de la Información |
| **Aprobado por** | Gerencia General |
| **Clasificación** | Uso interno — restringido |
| **Próxima revisión** | [Fecha, máx. 1 año] |

### 1. Objetivo
Documentar el inventario de bases de datos de datos personales del Banco, las medidas de seguridad aplicadas a cada una, las políticas de retención y borrado y el registro de operaciones de tratamiento (ROPA), en cumplimiento del art. 10 de la Ley 18.331 y de los arts. 3-4 del Decreto 64/020.
### 2. Alcance
Aplica a [COMPLETAR: todas las bases de datos y tratamientos de datos personales del Banco, en soporte digital y físico, cualquiera sea la unidad que los utilice, incluidos los tratamientos por encargados por cuenta del Banco].
### 3. Inventario de bases de datos de datos personales
| **N.º** | **Base de datos** | **Titulares** | **Categorías de datos** | **Finalidad** | **Soporte** |
|---|---|---|---|---|---|
| 1 | [COMPLETAR: Clientes de crédito hipotecario] | [COMPLETAR] | Datos identificatorios, financieros, patrimoniales [COMPLETAR] | Otorgar y gestionar créditos | Digital |
| 2 | [COMPLETAR: Ahorro y depósitos] | [COMPLETAR] | [COMPLETAR] | [COMPLETAR] | Digital |
| 3 | [COMPLETAR: Funcionarios (RRHH)] | [COMPLETAR] | Datos de salud, familiares, laborales | Administración del personal | Digital/Físico |
| 4 | [COMPLETAR: Videovigilancia sucursales] | [COMPLETAR] | Imágenes y sonidos (datos biométricos implícitos) | Seguridad de personas y bienes | Digital |
| 5 | [COMPLETAR: Banco En Línea y canales] | [COMPLETAR] | Datos identificatorios, credenciales, transacciones | Prestación de servicios en línea | Digital |

### 4. Medidas de seguridad por dominio
#### a) Medidas físicas
Acceso restringido a centros de cómputo y archivos, control de visitas, perímetro de las sucursales, protección de puestos de trabajo y eliminación segura de soportes [COMPLETAR: detalles por instalación].
#### b) Medidas lógicas
Control de acceso por perfiles y segregación de funciones, autenticación robusta (incluida autenticación multifactor para accesos críticos), cifrado de datos sensibles en tránsito y en reposo, registro y monitoreo de eventos, resguardo de datos conforme al art. 492 de la RNRCSF y pruebas anuales de recuperación [COMPLETAR].
#### c) Medidas organizativas
Políticas y procedimientos del SGSI, acuerdos de confidencialidad, cláusulas de tratamiento en contratos con encargados, capacitación a funcionarios, protocolo de derechos ARCO (URCDP-03) y procedimiento de vulneraciones (URCDP-02).
### 5. Ficha de base de datos (completar una por base)
| **Campo** | **Detalle** |
|---|---|
| **Nombre de la base** | [COMPLETAR] |
| **Responsable del tratamiento** | Banco — [COMPLETAR: unidad] |
| **Encargados del tratamiento** | [COMPLETAR: empresas o unidades que tratan por cuenta del Banco] |
| **Finalidad** | [COMPLETAR] |
| **Categorías de datos** | [COMPLETAR] |
| **Titulares** | [COMPLETAR: segmento y estimación del número] |
| **Base de licitud** | [Consentimiento / Ley / Contrato / interés público] |
| **Transferencias internacionales** | [COMPLETAR: sí/no, a qué países, salvaguardas] |
| **Medidas de seguridad aplicadas** | [COMPLETAR: físicas, lógicas, organizativas] |
| **Plazo de conservación** | [COMPLETAR: en función de la normativa del Banco] |
| **Borrado / destrucción** | [COMPLETAR: método y responsable] |
| **Inscripción URCDP** | [COMPLETAR: n.º de inscripción y fecha] |
| **EIPD requerida** | [Sí / No — referencia a URCDP-05] |

### 6. Políticas de retención y borrado
a) Los datos se conservan solo durante el plazo necesario para la finalidad y los plazos legales de conservación del Banco [COMPLETAR: plazos por categoría].
b) Al vencimiento del plazo se procede al borrado o disociación de forma segura (destrucción física de soportes, borrado con sobrescritura o destrucción certificada de discos).
c) Las imágenes de videovigilancia se conservan el plazo máximo autorizado por la URCDP [COMPLETAR: plazo] y luego se eliminan.
d) El borrado se registra y se puede auditar.
### 7. Registro de operaciones de tratamiento (ROPA)
El ROPA del Banco incluye, por tratamiento: responsable y encargados, finalidades, categorías de datos y de titulares, destinatarios, transferencias internacionales, plazos y medidas de seguridad. Se mantiene actualizado bajo la supervisión del DPD y es la base para las inscripciones (URCDP-04) y para responder a la URCDP.
### 8. Responsables y encargados
El Banco es responsable de los tratamientos de datos de sus clientes y funcionarios. Los encargados que tratan datos por cuenta del Banco se identifican en el ROPA y sus contratos incluyen las cláusulas de tratamiento exigidas [COMPLETAR: vínculo con GV-05 y PR-08]. El Banco solo transfiere datos fuera del país conforme a la Resolución 41/021 de la URCDP.
### 9. Revisión y actualización
Este documento se revisa al menos anualmente y ante cualquier cambio de base, tratamiento, tecnología o normativa. Las revisiones se registran en el control de cambios.
### Control de cambios
| **Versión** | **Fecha** | **Cambio** | **Elaboró** | **Aprobó** |
|---|---|---|---|---|
| 0.1 | [COMPLETAR] | Versión inicial (borrador) | DPD | — |
| 1.0 | [COMPLETAR] | Aprobación de Gerencia General | DPD | Gerencia General |

## 5. Ejemplo aplicado al Banco (modelo de referencia)
Ejemplo ilustrativo de cómo quedaría completado. Adaptá a la realidad institucional del Banco.
**Base de ejemplo — Clientes de crédito hipotecario:** base digital del sistema central de crédito, responsable el Banco (Área Comercial), con datos identificatorios, de contacto, financieros, patrimoniales y de garantías (incluidos datos de salud en certificados de incapacidad cuando corresponda). Finalidad: otorgar, administrar y cobrar los créditos hipotecarios. Encargados: [COMPLETAR: empresa de evaluación de riesgos, estudio de tasaciones]. Medidas: control de acceso por perfiles con segregación de funciones, registro de eventos, cifrado en tránsito, respaldos diarios fuera del sitio (art. 492), acuerdos de confidencialidad. Conservación: plazo del crédito más los plazos legales de archivo del Banco; luego borrado seguro certificado. Inscripción URCDP: N.º [COMPLETAR].
**Videovigilancia (ejemplo):** base de imágenes captadas en casa central y sucursales con la cartelería aprobada, finalidad de seguridad de personas y bienes, acceso restringido al personal de seguridad autorizado, conservación máxima de [COMPLETAR] días y borrado automático posterior. Se requiere EIPD por el tratamiento de datos de las personas que transitan las sucursales.
**ROPA (ejemplo):** el ROPA consolida [N] tratamientos, incluyendo los de datos de funcionarios (División Capital Humano), que se mantiene actualizado por el DPD y se presenta ante la URCDP cuando se solicita.

**Documentos relacionados:** URCDP-02 (Vulneraciones), URCDP-03 (ARCO), URCDP-04 (Inscripción de bases), URCDP-05 (EIPD), URCDP-06 (DPD), GV-01 (Política), GV-05/PR-08 (Terceros), PR-05 (Respaldo).
