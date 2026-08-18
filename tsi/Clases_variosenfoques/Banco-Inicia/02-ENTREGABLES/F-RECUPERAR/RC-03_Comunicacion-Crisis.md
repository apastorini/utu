# RC-03 · Plan de Comunicación de Crisis del Banco

> ⚠️ **Alerta:** este documento menciona **nombres propios del organigrama del Banco** (personas y cargos, abril 2026). Antes de usar el documento, verificá la vigencia de esos nombres contra el organigrama actual.
> **Función del MCU 5.0:** Recuperar (RC.CO — Comunicaciones de recuperación)
> **ISO/IEC 27001:** A.5.24 (Gestión de incidentes)
> **BCU:** Circular 2227 (riesgo operativo)
> **URCDP:** Ley 19.670 art. 38 · Decreto 64/020 (comunicación a titulares)
> **Nivel del curso:** 🟡 Practicar · 🔴 Dominar

## 1. Qué es y por qué existe
El **Plan de Comunicación de Crisis** define cómo el Banco comunica durante una crisis de seguridad, para que los mensajes sean oportunos, veraces, coordinados y consistentes. Una crisis mal comunicada agrava el daño: los clientes no saben qué hacer, la prensa especula, los rumores crecen y la confianza en un banco público —su activo más valioso— se erosiona.
El plan debe distinguir tres públicos con necesidades distintas: los **internos** (funcionarios, que necesitan saber si deben trabajar y cómo), los **institucionales** (URCDP, BCU, CERTuy, que tienen plazos legales y canales propios, ver RS-02) y los **externos** (titulares de datos, clientes, prensa y público en general). La comunicación a los titulares de datos tiene además contenido y plazo legal: el art. 38 de la Ley 19.670 exige comunicarlos de forma inmediata y pormenorizada.
La regla de oro es que **una sola voz** comunique: se definen voceros autorizados, mensajes preparados y un comité de crisis que aprueba cada comunicado. Todo lo demás (URCDP, BCU) se canaliza por los procedimientos técnicos de RS-02.
## 2. Marco de referencia
| **Norma** | **Referencia** | **Qué exige** |
|---|---|---|
| **MCU 5.0 (Agesic)** | RC.CO | Coordinar las comunicaciones de recuperación con las partes interesadas |
| **ISO/IEC 27001:2022** | A.5.24 | Comunicación con las partes interesadas durante incidentes |
| **BCU** | Circular 2227 | Comunicación de eventos de riesgo operativo |
| **URCDP** | **Ley 19.670 art. 38** · Decreto 64/020 | Comunicación inmediata y pormenorizada a los titulares de datos |

## 3. Cómo completar esta plantilla (guía de llenado)
1. **Definí los escenarios de crisis** con el RSI y el Comité: filtración de datos, ransomware, indisponibilidad prolongada, fraude con clientes.
2. **Designá voceros autorizados** con la Gerencia General y Comunicaciones: quién puede hablar, con qué mensajes y qué no se dice jamás.
3. **Prepará plantillas de comunicado** por escenario con Comunicaciones y Legal: versiones cortas y detalladas.
4. **Definí los mensajes internos** con Capital Humano y los jefes de área: instrucciones operativas a funcionarios y sucursales.
5. **Coordiná la comunicación a titulares** con el DPD: contenido, plazos (art. 38) y canales (correo, SMS, sitio web, app).
6. Consultá a **Servicios Jurídicos Notariales** (Dr. Héctor Dotta) para validar todo comunicado externo y a **Comunicaciones** para la relación con prensa y redes.
## 4. Plantilla del documento

### ENCABEZADO
| **Campo** | **Valor** |
|---|---|
| **Código** | RC-03 |
| **Título** | Plan de Comunicación de Crisis |
| **Versión** | 1.0 |
| **Estado** | [Borrador / En revisión / Aprobado] |
| **Fecha de aprobación** | [COMPLETAR] |
| **Elaborado por** | RSI |
| **Revisado por** | Comunicaciones · DPD · Legal |
| **Aprobado por** | Directorio |
| **Clasificación** | Uso interno |
| **Próxima revisión** | [Fecha, máx. 1 año] |

### 1. Objetivo
Garantizar comunicaciones internas y externas coordinadas, veraces y oportunas durante una crisis de seguridad, protegiendo a los titulares de datos, a los funcionarios y la confianza pública en el Banco, y cumpliendo las obligaciones legales.
### 2. Escenarios de crisis
| **Escenario** | **Ejemplo** | **Comunicación prioritaria** |
|---|---|---|
| **Filtración de datos** | Fuga de datos personales de clientes | Titulares (art. 38) + URCDP + prensa |
| **Ransomware** | Cifrado de sistemas críticos | Clientes sobre servicios, funcionarios, BCU |
| **Indisponibilidad prolongada** | Caída de Banco En Línea por más de X horas | Clientes y prensa; instrucciones alternativas |
| **Fraude con clientes** | Transferencias no autorizadas | Afectados directos + BCU + eventualmente prensa |

### 3. Comité de comunicación de crisis
| **Rol** | **Integrante sugerido** | **Función** |
|---|---|---|
| **Director de comunicaciones** | [COMPLETAR: área de comunicación institucional] | Conduce la estrategia y aprueba mensajes |
| **Vocero principal** | [COMPLETAR: Gerencia General o quien designe] | Única voz autorizada ante prensa |
| **RSI** | RSI | Datos técnicos, severidad y estados de recuperación |
| **DPD** | DPD | Comunicación a titulares y URCDP (RS-02) |
| **Legal** | Servicios Jurídicos | Validación legal de todo comunicado |
| **Capital Humano** | División Capital Humano | Comunicación a funcionarios |

### 4. Voceros autorizados
| **Público** | **Vocero** |
|---|---|
| Prensa / público | [COMPLETAR: vocero principal] |
| Titulares de datos | DPD, en coordinación con Comunicaciones |
| Funcionarios | Gerencia + Capital Humano |
| URCDP / BCU / CERTuy | DPD / Oficial de Cumplimiento / RSI (RS-02) |

**Regla:** ningún funcionario distinto de los autorizados emite declaraciones públicas sobre la crisis. Toda consulta se deriva al vocero.
### 5. Mensajes internos y externos
- **Internos:** estado de la situación, continuidad operativa, procedimientos a seguir, y canal de consultas. Se difunden por [COMPLETAR: intranet, correo institucional, comunicados de jefes].
- **Externos:** reconocimiento de la situación (sin detallar vulnerabilidades), acciones tomadas, canales de atención y recomendaciones. Se difunden por [COMPLETAR: sitio web, redes, prensa, call center].
- **Lo que no se comunica:** datos de clientes, detalles técnicos de la vulnerabilidad, información que comprometa la investigación forense (RS-03) o la seguridad.
### 6. Comunicación a titulares de datos (URCDP)
Cuando la crisis afecte datos personales, se comunica a los titulares de forma **inmediata y pormenorizada** (art. 38 Ley 19.670): naturaleza de la vulneración, datos afectados, riesgos, medidas adoptadas y recomendaciones. Contenido y canal los define el DPD con la plantilla de RS-02.
### 7. Plantillas de comunicado
**Comunicado breve (ejemplo):**
```text
[FECHA] — Comunicado del Banco Hipotecario del Uruguay
Estamos gestionando una situación que afectó [COMPLETAR: breve descripción sin
detalles técnicos]. Hemos tomado medidas inmediatas para proteger la información
de nuestros clientes y estamos trabajando para restablecer los servicios.
Los clientes afectados serán contactados por los canales oficiales del banco.
Por consultas: [COMPLETAR: canales de atención].
```
**Comunicado de filtración a titulares (ejemplo):** seguir la plantilla de RS-02 (naturaleza, datos, impactos, medidas) adaptada a lenguaje claro para el público.
### 8. Registro y control
Toda comunicación se registra con fecha/hora, medio, audiencia y responsable. Las versiones finales se archivan con el expediente del incidente (RS-01). Después de la crisis, el análisis alimenta RC-04.
### 9. Control de cambios
| **Versión** | **Fecha** | **Cambio** | **Elaboró** | **Aprobó** |
|---|---|---|---|---|
| 0.1 | [COMPLETAR] | Versión inicial (borrador) | RSI | — |
| 1.0 | [COMPLETAR] | Aprobación del Directorio | RSI | Directorio |

## 5. Ejemplo aplicado al Banco (modelo de referencia)
Ejemplo ilustrativo. Adaptá a la operación real del Banco.
**Caso: filtración de datos de clientes (ejemplo):**
- 15:00 — Se confirma una filtración que afecta a ~40.000 titulares (ver RS-01/RS-02). El Comité de Crisis se reúne y aprueba la estrategia de comunicación.
- 15:30 — Comunicado interno: se informa a funcionarios y sucursales el estado, se da el guion de respuesta para consultas de clientes y se refuerza el protocolo de no divulgación.
- 16:00 — El DPD prepara la comunicación a los titulares afectados (correo/SMS y aviso en el sitio web y la app) con la plantilla de RS-02, validada por Legal.
- 17:00 — Comunicado externo breve en el sitio web: situación, medidas y canales de atención. Sin detalles técnicos.
- Día 2 — El vocero principal atiende prensa con mensajes aprobados; redes sociales bajo monitoreo con respuestas estándar derivando a los canales oficiales.
- Resultado: una sola voz, mensajes consistentes, cumplido el art. 38 (comunicación inmediata a titulares). El análisis post-crisis alimenta RC-04.

**Documentos relacionados:**
- RS-02 (Notificación de Incidentes) · RS-01 (Respuesta)
- RC-01 (BCP) · RC-02 (DRP) · RC-04 (Lecciones Aprendidas)
- URCDP-02 (Notificación de Vulneraciones) · PR-02 (Concientización)
