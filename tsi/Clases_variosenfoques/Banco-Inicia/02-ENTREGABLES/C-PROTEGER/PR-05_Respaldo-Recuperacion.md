# PR-05 · Política de Respaldo y Recuperación de la Información del Banco

> ⚠️ **Alerta:** este documento menciona **nombres propios del organigrama del Banco** (personas y cargos, abril 2026). Antes de usar el documento, verificá la vigencia de esos nombres contra el organigrama actual.
> **Función del MCU 5.0:** Proteger (PR.IR — Resiliencia de la infraestructura tecnológica)
> **ISO/IEC 27001:** A.8.13 (Respaldo de la información) · A.8.10 (Borrado de información)
> **BCU:** **RNRCSF art. 492 (crítico)** — resguardo de datos, software y documentación; claves de desencriptación; pruebas anuales de la totalidad de la información
> **URCDP:** Ley 18.331 art. 10 (medidas de seguridad)
> **Nivel del curso:** 🔴 Dominar

## 1. Qué es y por qué existe
El **art. 492 de la Recopilación de Normas de Regulación y Control del Sistema Financiero (RNRCSF)** del BCU es, para el Banco, la norma de respaldo por excelencia: exige resguardar los **datos, software y documentación** necesarios para reconstruir las operaciones, mantener **copias que no se afecten por un mismo evento** de riesgo, resguardar las **claves de desencriptación**, realizar **pruebas anuales de recuperación e integridad de la totalidad de la información** y contar con un **responsable de la ejecución del resguardo** de categoría superior.
Esta política traduce esa exigencia en un esquema operativo concreto: qué se respalda, con qué frecuencia, dónde se guardan las copias, cómo se protegen (cifrado), cómo se registran y —lo que el BCU mira con más atención— cómo y cuándo se **prueba la restauración**. Un respaldo que nunca se probó no es un respaldo: es una promesa.
En el Banco, la pérdida de datos implicaría no solo incumplimiento normativo y sanciones del BCU, sino la imposibilidad de reconstruir carteras de crédito, saldos de ahorro y operaciones del sistema de pagos: un daño reputacional y financiero irreparable. Esta política es el puente entre la continuidad (RC-01/RC-02) y la operación diaria de la División de TI.
## 2. Marco de referencia
| **Referencia** | **Requisito aplicable** |
|---|---|
| **MCU 5.0 (Agesic)** | PR.IR — resiliencia de la infraestructura tecnológica (respaldo, recuperación y mantenimiento de la capacidad de restauración) |
| **ISO/IEC 27001:2022** | A.8.13 respaldo de la información (copias, restauración, pruebas) |
| **BCU** | **RNRCSF art. 492** (crítico): reconstrucción, copias no afectadas por el mismo evento, claves de desencriptación, pruebas anuales, responsable superior |
| **URCDP** | Ley 18.331 art. 10 (medidas técnicas de seguridad) |

## 3. Cómo completar esta plantilla (guía de llenado)
1. **Completá el encabezado** (código, versión, fecha). La aprueba el Comité de Seguridad de la Información.
2. **Definí con la Div. TI** (Jefe de Departamento Producción, Ing. Daniel Herrera) el inventario de sistemas a respaldar y los RPO/RTO por sistema.
3. **Identificá los sitios de resguardo** (ubicaciones que no se afecten por un mismo evento: otro edificio, otra ciudad).
4. **Personalizá los apartados [COMPLETAR]** con frecuencias, retenciones y responsables reales.
5. **Planificá las pruebas anuales de restauración de la totalidad de la información** y su registro como evidencia ante el BCU.
6. **Coordiná el resguardo de las claves de desencriptación** con PR-03 (KMS y custodia separada).
7. **Aprobá, registrá en el control de cambios** y publicá en `02-ENTREGABLES/C-PROTEGER`. Revisá anualmente y tras cambios mayores de arquitectura.
## 4. Plantilla del documento

### ENCABEZADO
| **Campo** | **Valor** |
|---|---|
| **Código** | PR-05 |
| **Título** | Política de Respaldo y Recuperación de la Información |
| **Versión** | 1.0 |
| **Estado** | [Borrador / En revisión / Aprobado] |
| **Fecha de aprobación** | [COMPLETAR] |
| **Elaborado por** | RSI |
| **Revisado por** | Div. TI · Depto. Producción · Comité de Seguridad |
| **Aprobado por** | Comité de Seguridad de la Información |
| **Clasificación** | Uso interno |
| **Próxima revisión** | [Fecha, máx. 1 año] |

### 1. Objetivo
Garantizar que el Banco pueda **reconstruir sus operaciones** en caso de pérdida o corrupción de información, mediante respaldos completos, seguros, geográficamente separados y **probados** periódicamente, en cumplimiento del art. 492 de la RNRCSF.
### 2. Alcance
Aplica a [COMPLETAR: toda la información crítica del Banco —core bancario, sistema de pagos, Banco En Línea, bases de datos, archivos de sucursales, respaldos de configuraciones, software y documentación necesaria para reconstruir operaciones—] y a todos los soportes donde se almacene.
### 3. Alcance de los respaldos
| **Sistema** | **RPO objetivo** | **RTO objetivo** | **Frecuencia de respaldo** |
|---|---|---|---|
| Core bancario | [COMPLETAR: ≤ 15 min] | [COMPLETAR: ≤ 4 h] | Continua (logs) + diaria |
| Sistema de pagos | [COMPLETAR] | [COMPLETAR] | Diaria + respaldo en línea |
| Banco En Línea | [COMPLETAR] | [COMPLETAR] | Diaria |
| Bases de datos y servidores | [COMPLETAR] | [COMPLETAR] | Diaria |
| Archivos de sucursales | [COMPLETAR] | [COMPLETAR] | Diaria / semanal |
| Configuraciones y documentación | [COMPLETAR] | [COMPLETAR] | Semanal |

### 4. Esquema de copias
- **Copia primaria** en línea (datacenter del Banco).
- **Copia secundaria** en un **sitio alternativo** que no se vea afectado por el mismo evento (otro edificio / otra ciudad) — exigencia del art. 492.
- **Retención:** [COMPLETAR: diarias 30 días, semanales 12 semanas, mensuales 12 meses, anuales 7 años o según normativa].
- Al menos una copia se mantiene **fuera de línea** (off-site) protegida contra ransomware.
### 4.1. Respaldo cifrado
Todos los respaldos se cifran en reposo con el estándar aprobado (PR-03). Las **claves de desencriptación** se resguardan en custodia separada y bajo doble custodia, en ubicación distinta de los respaldos.
### 5. Pruebas de restauración (obligación crítica del art. 492)
- Se realiza **anualmente una prueba de recuperación e integridad de la totalidad de la información** resguardada (no solo de una muestra).
- Se verifica que los datos restaurados sean **íntegros y utilizables** (validación con conciliación de registros).
- Las pruebas se documentan con: alcance, fecha, sistemas probados, resultados, desviaciones y plan de corrección.
- Adicionalmente, **pruebas parciales trimestrales** de sistemas críticos.
- Las pruebas se reportan al Comité y quedan disponibles para el BCU.
### 6. Registro de respaldos
Se mantiene un **registro de ejecución de respaldos** con: fecha, sistema, tipo de copia, tamaño, destino, resultado (éxito/error) y responsable. Las fallas se atienden en el día y las recurrentes se tratan como incidente (RS-01).
### 7. Responsabilidades
| **Rol** | **Responsabilidad** |
|---|---|
| **Jefe de Depto. Producción** | Ejecutar y operar los respaldos; atención de fallas |
| **Div. TI** | Diseño de la arquitectura de respaldo y del sitio alternativo |
| **Responsable del resguardo (categoría superior)** | Supervisar la ejecución, las pruebas anuales y la custodia de claves [COMPLETAR: nombre/cargo] |
| **RSI** | Supervisión de cumplimiento y evidencia ante supervisores |
| **Comité de Seguridad** | Aprobar RPO/RTO y resultados de las pruebas |

### 8. Control de cambios
| **Versión** | **Fecha** | **Cambio** | **Elaboró** | **Aprobó** |
|---|---|---|---|---|
| 0.1 | [COMPLETAR] | Versión inicial (borrador) | RSI | — |
| 1.0 | [COMPLETAR] | Aprobación del Comité | RSI | Comité |

## 5. Ejemplo aplicado al Banco (modelo de referencia)
Ejemplo ilustrativo de cómo quedaría el apartado 4 completado. Adaptá al contenido institucional real del Banco.
**Esquema de copias (ejemplo):**
- El **core bancario** se respalda de forma continua (log shipping) hacia el **datacenter secundario** ubicado en otro punto de Montevideo, más una copia diaria completa y una copia mensual que se envía a custodia **fuera de la capital**.
- Los respaldos viajan y se almacenan **cifrados (AES-256)**; las **claves de desencriptación** se custodian en la caja de seguridad de la Div. TI, bajo **doble custodia** de dos funcionarios de categoría superior, en un edificio distinto al de los respaldos (cumplimiento del art. 492).
**Prueba anual de restauración (ejemplo):**
- En marzo de 2026 se ejecutó la prueba anual sobre **la totalidad de la información**: se restauraron en un ambiente aislado el core, el sistema de pagos y las bases de datos, se concilió el 100 % de los registros de una fecha de corte y se validó la desencriptación con las claves custodiadas. Resultado: **integridad 100 %**, con una desviación menor de tiempo de restauración en el módulo de archivos de sucursal, corregida en el mes siguiente. El informe quedó en el expediente de evidencia del BCU.
**Simulacro (ejemplo):**
- En el simulacro de continuidad (RC-02) se declaró indisponible el datacenter primario y la operación se recuperó desde el sitio alternativo dentro del RTO acordado (4 h), validando de paso el respaldo continuo del core.

**Documentos relacionados:** GV-01 (Política de Seguridad), PR-03 (Seguridad de Datos y Claves), PR-04 (Seguridad Física), RC-01 (Continuidad del Negocio), RC-02 (Recuperación ante Desastres), DE-01 (Monitoreo), RS-01 (Incidentes).
