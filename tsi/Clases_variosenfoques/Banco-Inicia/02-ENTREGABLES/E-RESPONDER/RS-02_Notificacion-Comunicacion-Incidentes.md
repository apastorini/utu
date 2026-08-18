# RS-02 · Procedimiento de Notificación y Comunicación de Incidentes del Banco

> ⚠️ **Alerta:** este documento menciona **nombres propios del organigrama del Banco** (personas y cargos, abril 2026). Antes de usar el documento, verificá la vigencia de esos nombres contra el organigrama actual.
> **Función del MCU 5.0:** Responder (RS.CO — Comunicaciones)
> **ISO/IEC 27001:** A.5.24 (Gestión de incidentes)
> **BCU:** Circular 2227 (riesgo operativo)
> **URCDP:** **Ley 19.670 art. 38 · Decreto 64/020 arts. 3-4** (plazos críticos de notificación)
> **Nivel del curso:** 🔴 Dominar

## 1. Qué es y por qué existe
Este procedimiento define **a quién, cómo y en qué plazo** se comunica un incidente de seguridad, tanto hacia adentro del Banco como hacia los organismos de control y los titulares de datos. Es el documento con los plazos más exigentes del SGSI, porque la normativa uruguaya es estricta: la **URCDP** debe recibir la comunicación de una vulneración de datos personales en un máximo de **72 horas** desde que se tiene conocimiento, y los procedimientos para minimizar el impacto deben iniciarse dentro de las **primeras 24 horas** (art. 38 de la Ley 19.670 y Decreto 64/020).
No se trata solo de cumplir plazos: una comunicación mal hecha agrava la crisis (multas, daño reputacional, pérdida de confianza de clientes y del público). El Banco, como banco público, tiene además un canal natural con el BCU (eventos de riesgo operativo, Circular 2227) y con **CERTuy**, que coordina el curso de acción ante incidentes que afecten infraestructuras o servicios del Estado.
Por eso la regla de oro es la **preparación**: las plantillas de notificación, los datos de contacto y la matriz de responsables deben estar listas antes del incidente. El RSI y el DPD deben poder notificar en horas, no en días.
## 2. Marco de referencia
| **Norma** | **Referencia** | **Qué exige** |
|---|---|---|
| **MCU 5.0 (Agesic)** | RS.CO | Establecer y coordinar comunicaciones internas y externas durante la respuesta |
| **ISO/IEC 27001:2022** | A.5.24 | Gestión de incidentes con comunicación a las partes interesadas |
| **BCU** | Circular 2227 | Reporte de eventos de riesgo operativo |
| **URCDP** | **Ley 19.670 art. 38 · Decreto 64/020 arts. 3-4** | Iniciar procedimientos en 24 h; comunicación a la URCDP en máx. 72 h; comunicación a titulares |

## 3. Cómo completar esta plantilla (guía de llenado)
1. **Definí la matriz de notificación** con el RSI, el DPD, Servicios Jurídicos y Comunicaciones: quién notifica a cada destinatario (URCDP, BCU, CERTuy, titulares, prensa, dirección).
2. **Cargá los contactos operativos** (URCDP, CERTuy, BCU, proveedores) con el RSI y verificalos trimestralmente.
3. **Personalizá el contenido mínimo de la notificación** con el DPD, respetando el art. 38: naturaleza, datos afectados, titulares, impactos y medidas.
4. **Fijá los responsables únicos de cada notificación** (RSI, DPD, Comunicaciones) para evitar notificaciones duplicadas o contradictorias.
5. **Probalo en el simulacro** de RS-01: medí el tiempo real de notificación contra el límite de 72 h.
6. Consultá a **Servicios Jurídicos Notariales** (Dr. Héctor Dotta) y al **Oficial de Cumplimiento** para los casos con alcance penal o de fraude.
## 4. Plantilla del documento

### ENCABEZADO
| **Campo** | **Valor** |
|---|---|
| **Código** | RS-02 |
| **Título** | Procedimiento de Notificación y Comunicación de Incidentes |
| **Versión** | 1.0 |
| **Estado** | [Borrador / En revisión / Aprobado] |
| **Fecha de aprobación** | [COMPLETAR] |
| **Elaborado por** | RSI |
| **Revisado por** | DPD · Comité de Seguridad de la Información |
| **Aprobado por** | Directorio |
| **Clasificación** | Confidencial |
| **Próxima revisión** | [Fecha, máx. 1 año] |

### 1. Objetivo
Garantizar que todo incidente de seguridad se comunique a las partes interesadas correspondientes de forma oportuna, completa y coordinada, cumpliendo los plazos legales y protegiendo los intereses del Banco y de los titulares de datos.
### 2. Alcance
Aplica a todo incidente de seguridad del Banco [COMPLETAR: incluyendo los que afecten datos personales, sistema de pagos, servicios de banca y servicios tercerizados]. Distingue notificación de **comunicación pública** (RC-03).
### 3. Matriz de notificación (interna y externa)
| **Destinatario** | **Cuándo** | **Plazo** | **Responsable** |
|---|---|---|---|
| **Comité de Seguridad / Gerencia** | Incidentes severidad alta y crítica | [COMPLETAR: 2 h] | RSI |
| **Directorio** | Incidentes críticos | [COMPLETAR: 24 h] | RSI |
| **DPD** | Cualquier indicio de vulneración de datos personales | Inmediato | RSI / detectores |
| **URCDP** | Vulneración de datos personales | **Máx. 72 h** desde el conocimiento | DPD |
| **Titulares de datos** | Vulneración con riesgo para los titulares | Inmediatamente y pormenorizadamente | DPD + Comunicaciones |
| **CERTuy** | Incidentes que afecten infraestructura/servicios del Estado o cuando la URCDP lo coordine | [COMPLETAR] | RSI |
| **BCU** | Eventos de riesgo operativo relevantes (Circular 2227) | [COMPLETAR] | Oficial de Cumplimiento |
| **Fuerzas de seguridad / justicia** | Delitos (fraude, intrusión) | [COMPLETAR] | Legal |

### 4. Contenido mínimo de la notificación a la URCDP
- Fecha cierta o estimada de la vulneración y su **naturaleza**.
- **Datos personales afectados** y titulares involucrados.
- **Impactos** potenciales.
- **Medidas adoptadas o a adoptar** para mitigar y corregir.
### 5. Responsables de la notificación
| **Notificación** | **Responsable único** |
|---|---|
| URCDP | DPD |
| Titulares | DPD, en coordinación con Comunicaciones |
| BCU | Oficial de Cumplimiento |
| CERTuy | RSI |
| Prensa / público | Comunicaciones (ver RC-03) |

Ninguna notificación externa se realiza sin la validación previa de **Legal**.
### 6. Plantilla de comunicado
```text
[FECHA] — Comunicación de vulneración de seguridad de datos personales
Entidad: Banco Hipotecario del Uruguay
Fecha/hora de conocimiento: [COMPLETAR]
Naturaleza de la vulneración: [COMPLETAR]
Datos afectados: [COMPLETAR]
Titulares afectados: [COMPLETAR] (número y perfil)
Impactos potenciales: [COMPLETAR]
Medidas adoptadas: [COMPLETAR]
Medidas a adoptar: [COMPLETAR]
Contacto institucional: [COMPLETAR]
Firma: DPD / RSI
```
### 7. Registro y control
Toda notificación se registra en el Registro de Incidentes (RS-01) con: fecha/hora de envío, destinatario, medio y copia del contenido. Los registros se conservan conforme a DE-01 y a las normas de retención aplicables.
### 8. Control de cambios
| **Versión** | **Fecha** | **Cambio** | **Elaboró** | **Aprobó** |
|---|---|---|---|---|
| 0.1 | [COMPLETAR] | Versión inicial (borrador) | RSI | — |
| 1.0 | [COMPLETAR] | Aprobación del Directorio | RSI · DPD | Directorio |

## 5. Ejemplo aplicado al Banco (modelo de referencia)
Ejemplo ilustrativo. Adaptá a la operación real del Banco.
**Caso: acceso no autorizado a la base de datos de clientes (ejemplo):**
- 08:00 — Se detecta una exportación anómala de la base de clientes (DE-02). El RSI clasifica como incidente crítico y **activa el reloj de 72 h**.
- 08:15 — Se informa al DPD (inmediato). El DPD confirma que hay **datos personales** (nombres, cédulas, datos de contacto y de préstamos) → **vulneración de datos**.
- 08:30 — Se inician los procedimientos de minimización (bloqueo de credenciales, revisión de respaldos) dentro de la **primera hora** (cumple el límite de 24 h del art. 38).
- 12:00 — El equipo de investigación confirma alcance: ~40.000 titulares. El DPD prepara la notificación a la **URCDP**.
- 15:00 — Se envía la notificación a la URCDP (7 horas desde el conocimiento, muy por debajo del máximo de 72 h). Se coordina con CERTuy el curso de acción.
- Día 2 — Comunicación pormenorizada a los titulares afectados (correo y sitio web) con recomendaciones, validada por Legal. Se evalúa el informe a prensa según RC-03.
- Día 3 — El Oficial de Cumplimiento reporta el evento de riesgo operativo al BCU. Informe final al Directorio.
**Contactos a verificar (ejemplo):** sistema de gestión de la URCDP (notificación en línea), CERTuy (csirt@gub.uy), BCU (Superintendencia de Instituciones Financieras), proveedor del SIEM.

**Documentos relacionados:**
- RS-01 (Respuesta a Incidentes) · RS-03 (Forense)
- RC-03 (Comunicación de Crisis) · URCDP-02 (Notificación de Vulneraciones)
- BCU-01 (Gobierno de Ciberseguridad) · PR-02 (Concientización)
