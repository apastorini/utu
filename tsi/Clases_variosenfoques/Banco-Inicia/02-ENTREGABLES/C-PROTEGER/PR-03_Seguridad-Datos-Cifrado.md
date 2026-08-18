# PR-03 · Política de Seguridad de Datos: Clasificación, Cifrado y Minimización del Banco
> **Función del MCU 5.0:** Proteger (PR.DS — Seguridad de datos)
> **ISO/IEC 27001:** A.8.12 (Prevención de fuga de datos) · A.8.24 (Uso de criptografía) · A.8.11 (Enmascaramiento de datos)
> **BCU:** RNRCSF art. 492 (resguardo de claves de desencriptación) · EMG · Riesgo tecnológico
> **URCDP:** Ley 18.331 arts. 10 y 12 · Decreto 64/020 (minimización, calidad de datos)
> **Nivel del curso:** 🟡 Practicar · 🔴 Dominar

## 1. Qué es y por qué existe
El banco vive de la información: datos de clientes, créditos hipotecarios, ahorros, garantías, información de contacto y, en muchos casos, datos de riesgo crediticio. La Ley 18.331 (URCDP) obliga al Banco a aplicar **medidas técnicas y organizativas** que garanticen la confidencialidad, integridad y disponibilidad de esos datos, y el BCU exige protegerlos como parte del riesgo operativo. Sin un orden claro de clasificación, no se sabe cuánta protección darle a cada dato ni cómo demostrarla ante los supervisores.
Esta política establece **cómo se clasifican los datos** del Banco (público, uso interno, confidencial, secreto), **cómo se tratan según su clase**, **cuándo y cómo se cifran** (en reposo y en tránsito), cómo se resguardan las **claves de desencriptación** (exigencia del art. 492 de la RNRCSF), cómo se aplican **minimización y anonimización** y cómo se previene la **fuga de datos** (DLP). También fija la **retención y el borrado seguro** para que los datos no vivan más tiempo del necesario.
En el Banco, el dato más sensible está en el **core bancario**: historial de deudores, saldos, garantías hipotecarias y datos personales de clientes. El secreto bancario (Ley 16.713) se suma a la confidencialidad técnica. Esta política es la herramienta para que cualquier dato, en cualquier sistema, base de datos o papel, tenga el nivel de protección que le corresponde.
## 2. Marco de referencia
| **Referencia** | **Requisito aplicable** |
|---|---|
| **MCU 5.0 (Agesic)** | PR.DS — clasificación y tratamiento de datos según sensibilidad; cifrado; minimización |
| **ISO/IEC 27001:2022** | A.8.2 clasificación de la información; A.8.3 manejo de activos; A.8.12 prevención de fuga de datos; A.8.24 uso de criptografía; A.8.11 enmascaramiento |
| **BCU** | RNRCSF art. 492 (resguardo de claves de desencriptación); EMG · Riesgo tecnológico; Circular 2280 (sistema de pagos) |
| **URCDP** | Ley 18.331 arts. 10 y 12; Ley 19.670; Decreto 64/020 (minimización, finalidad, seguridad) |

## 3. Cómo completar esta plantilla (guía de llenado)
1. **Completá el encabezado** (código, versión, fecha). La aprueba el Comité de Seguridad de la Información.
2. **Consolidá la clasificación** con el inventario de activos (ID-01) y con el DPD para los datos personales.
3. **Definí con la Div. TI** los estándares técnicos: cifrado de discos y bases de datos (en reposo), TLS en las comunicaciones (en tránsito) y la solución de **gestión de claves (KMS)**.
4. **Personalizá los apartados [COMPLETAR]** con la herramienta DLP, los plazos de retención reales y los algoritmos aceptados.
5. **Coordiná la tabla de retención y borrado** con el Departamento de Contabilidad y Tributos, Servicios Jurídicos y el Área de Riesgos (obligaciones legales de conservación).
6. **Aprobá, registrá en el control de cambios** y publicá en `02-ENTREGABLES/C-PROTEGER`. Revisá anualmente.
## 4. Plantilla del documento

### ENCABEZADO
| **Campo** | **Valor** |
|---|---|
| **Código** | PR-03 |
| **Título** | Política de Seguridad de Datos: Clasificación, Cifrado y Minimización |
| **Versión** | 1.0 |
| **Estado** | [Borrador / En revisión / Aprobado] |
| **Fecha de aprobación** | [COMPLETAR] |
| **Elaborado por** | RSI |
| **Revisado por** | DPD · Gerente Div. TI · Comité de Seguridad |
| **Aprobado por** | Comité de Seguridad de la Información |
| **Clasificación** | Uso interno |
| **Próxima revisión** | [Fecha, máx. 1 año] |

### 1. Objetivo
Garantizar que la información del Banco se **clasifique, proteja, cifre, minimice y elimine** de acuerdo con su sensibilidad, en cumplimiento de la normativa aplicable (BCU, URCDP y Agesic).
### 2. Alcance
Aplica a [COMPLETAR: toda la información del Banco, en cualquier formato —digital, papel, oral— y en cualquier soporte: bases de datos, archivos, correo, respaldos, documentos en papel, dispositivos móviles y medios extraíbles]. Aplica también a los datos tratados por terceros en nombre del banco.
### 3. Clasificación de la información
| **Clase** | **Ejemplos en el Banco** | **Tratamiento mínimo** |
|---|---|---|
| **Público** | Información de prensa, sitio web institucional | Sin restricciones |
| **Uso interno** | Procedimientos internos, organigrama, minutas | Acceso solo para funcionarios |
| **Confidencial** | Datos de clientes, expedientes de crédito, información comercial | Acceso por función; cifrado; minimización |
| **Secreto** | Secreto bancario, credenciales criptográficas, claves de desencriptación, información de seguridad | Acceso restringido y trazado; cifrado fuerte |

### 3.1. Etiquetado y tratamiento
Toda información debe **etiquetarse** con su clase [COMPLETAR: metadatos, carátulas, asunto de correo]. El tratamiento de cada clase (copia, transmisión, impresión, destrucción) se ajusta a la tabla de la sección 3.
### 4. Cifrado
### 4.1. Cifrado en reposo
- Bases de datos del core bancario, Banco En Línea y sistema de pagos: **cifradas en reposo** con algoritmos aprobados [COMPLETAR: AES-256].
- Discos y respaldos de servidores y equipos portátiles: cifrado completo (disco entero).
- Medios extraíbles y móviles: cifrado obligatorio.
### 4.2. Cifrado en tránsito
- Todas las comunicaciones externas: **TLS 1.2 mínimo** [COMPLETAR: preferentemente 1.3].
- Conexiones internas sensibles (core → sistema de pagos): cifradas o por redes segmentadas.
- Acceso remoto: VPN con cifrado aprobado.
### 4.3. Gestión de claves criptográficas
- Se usa una **plataforma de gestión de claves (KMS)** con custodia centralizada [COMPLETAR].
- Las **claves de desencriptación se resguardan** en un lugar **separado** de los datos cifrados y bajo doble custodia (cumplimiento del art. 492 RNRCSF).
- Rotación de claves: al menos cada [COMPLETAR: 12 meses] o ante compromiso.
- La pérdida de una clave de desencriptación se trata como **incidente crítico** (RS-01).
### 5. Minimización y anonimización
- Se recolecta solo lo **necesario y pertinente** para la finalidad (art. 10 URCDP).
- Para pruebas y desarrollos se usan **datos enmascarados o anonimizados**, nunca datos reales de clientes (se coordina con PR-07).
- Los datos que dejen de ser necesarios se **anonimizan o eliminan** según la tabla de retención.
### 6. Prevención de fuga de datos (DLP)
- Se implementa control DLP en correo, web y medios extraíbles [COMPLETAR: herramienta / mecanismo].
- Reglas que detectan envío de clases "Confidencial" y "Secreto" a destinos externos no autorizados.
- Almacenamiento de datos en la nube personal o servicios no autorizados: **prohibido**.
### 7. Retención y borrado seguro
| **Tipo de dato** | **Plazo de retención** | **Borrado** |
|---|---|---|
| Expedientes de crédito | [COMPLETAR: según normativa] | Borrado seguro / destrucción física |
| Datos personales de clientes | [COMPLETAR] | Borrado seguro al vencer el plazo o cesar la finalidad |
| Respaldo de seguridad | Según PR-05 | Sobrescritura segura / criptoborrado |

- Borrado lógico: sobrescritura múltiple o criptoborrado de discos; **destrucción física** certificada para discos y papel "Secreto".
### 8. Responsabilidades
| **Rol** | **Responsabilidad** |
|---|---|
| **Dueño de los datos (área usuaria)** | Clasificar y etiquetar; autorizar accesos y transmisiones |
| **Div. TI** | Implementar cifrado, KMS, DLP y borrado técnico |
| **DPD** | Cumplimiento URCDP: minimización, anonimización, EIPD |
| **RSI** | Supervisar el cumplimiento y las excepciones |
| **Auditoría Interna** | Evaluar la efectividad del control |

### 9. Control de cambios
| **Versión** | **Fecha** | **Cambio** | **Elaboró** | **Aprobó** |
|---|---|---|---|---|
| 0.1 | [COMPLETAR] | Versión inicial (borrador) | RSI | — |
| 1.0 | [COMPLETAR] | Aprobación del Comité | RSI | Comité |

## 5. Ejemplo aplicado al Banco (modelo de referencia)
Ejemplo ilustrativo de cómo quedaría el apartado 4 completado. Adaptá al contenido institucional real del Banco.
**Clasificación (ejemplo):**
- El **historial de deudores del Banco** y la información de garantías hipotecarias se clasifican como **Secreto** (secreto bancario): acceso restringido al personal de crédito y cobranzas, con trazabilidad por usuario.
- Los **expedientes de crédito en trámite** y los datos de contacto de clientes son **Confidenciales**.
- Los **procedimientos operativos de sucursal** (no financieros) son de **Uso interno**.
**Cifrado (ejemplo):**
- La base de datos del **core bancario** está cifrada en reposo con AES-256; las conexiones del **Banco En Línea** y del **sistema de pagos** usan TLS 1.3.
- Las **claves de desencriptación** de los respaldos se guardan en la caja fuerte de custodia de la Div. TI, bajo **doble custodia** (dos funcionarios de categoría superior), en un edificio **distinto** al que aloja los respaldos, cumpliendo el art. 492 de la RNRCSF.
- En 2026, durante la prueba anual de restauración (PR-05), se comprobó la recuperación de las claves desde la custodia y la correcta desencriptación de los respaldos.
**Minimización y DLP (ejemplo):**
- Los desarrollos de prueba del sistema de pagos usan **datos enmascarados**, nunca datos reales de clientes.
- El DLP del correo bloquea el envío de planillas con datos personales a cuentas personales; en 2026 bloqueó 47 intentos y se derivaron los casos recurrentes a concientización (PR-02).

**Documentos relacionados:** GV-01 (Política de Seguridad), ID-01 (Inventario de Activos), PR-01 (Control de Acceso), PR-05 (Respaldo y Recuperación), PR-07 (Desarrollo Seguro), DE-01 (Monitoreo), URCDP-01 (Seguridad de Datos Personales).
