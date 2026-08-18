# DE-02 · Procedimiento de Detección de Anomalías e Intrusiones del Banco

> ⚠️ **Alerta:** este documento menciona **nombres propios del organigrama del Banco** (personas y cargos, abril 2026). Antes de usar el documento, verificá la vigencia de esos nombres contra el organigrama actual.
> **Función del MCU 5.0:** Detectar (DE.CM — Monitoreo continuo · DE.AE — Análisis de eventos adversos)
> **ISO/IEC 27001:** A.8.16 (Monitoreo de actividades)
> **BCU:** Circular 2280 (sistema de pagos)
> **URCDP:** Ley 18.331 art. 10 · Decreto 64/020
> **Nivel del curso:** 🟡 Practicar · 🔴 Dominar

## 1. Qué es y por qué existe
Este procedimiento convierte los **registros** (DE-01) en **alertas accionables**: define los casos de uso de detección, las líneas base, los umbrales de alerta y el flujo de escalamiento para que una anomalía pase de un aviso a una respuesta coordinada (RS-01). Es el corazón operativo de la función **Detectar** del MCU 5.0.
En el Banco los riesgos típicos son el fraude interno y externo (transferencias inusuales, créditos simulados), la infección por malware o ransomware, y la exfiltración de datos personales de clientes. Sin reglas de detección y sin alguien que las administre, los logs acumulados no sirven de nada: el incidente se descubre tarde, cuando el daño ya está hecho y el plazo de 72 horas de la URCDP ya corrió.
El procedimiento no depende solo de la herramienta (EDR/XDR/SIEM): depende de que existan **líneas base** (qué es lo normal), **umbrales** (qué es anómalo) y **turnos de monitoreo** (quién mira y cuándo). La evidencia de que este proceso funciona se presenta ante el BCU (Circular 2280, riesgo operativo) y ante Agesic en las autoevaluaciones del MCU 5.0.
## 2. Marco de referencia
| **Norma** | **Referencia** | **Qué exige** |
|---|---|---|
| **MCU 5.0 (Agesic)** | DE.CM / DE.AE | Monitoreo continuo y análisis de eventos adversos |
| **ISO/IEC 27001:2022** | A.8.16 | Monitoreo de actividades de red y sistemas |
| **BCU** | Circular 2280 | Vigilancia del sistema de pagos y detección de operaciones anómalas |
| **URCDP** | Ley 18.331 art. 10 · Decreto 64/020 | Prevenir el acceso no autorizado y la fuga de datos personales |

## 3. Cómo completar esta plantilla (guía de llenado)
1. **Listá los casos de uso de detección** con el RSI, la División TI y el Dpto. Sistema de Pagos: priorizá los que protegen transferencias, banca en línea y datos de clientes.
2. **Definí líneas base y umbrales** con el Jefe de Departamento Producción (Ing. Daniel Herrera): hay que conocer la operación normal antes de marcar lo anómalo (ej. hora pico, volúmenes esperados).
3. **Documentá las reglas y firmas** que mantiene la plataforma SIEM/EDR (EDR/XDR/SIEM) y el proceso de actualización de firmas.
4. **Definí el escalamiento** con el RSI: quién recibe cada nivel de alerta y en qué horario (24×7 o en horario hábil con guardia pasiva).
5. **Probalo con ejercicios de mesa**: tomá un incidente real o simulado y verificá que la alerta llega y escala.
6. Consultá al **RSI** y al **Oficial de Cumplimiento** para los casos de uso vinculados a fraude y lavado (reportes de operaciones inusuales).
## 4. Plantilla del documento

### ENCABEZADO
| **Campo** | **Valor** |
|---|---|
| **Código** | DE-02 |
| **Título** | Procedimiento de Detección de Anomalías e Intrusiones |
| **Versión** | 1.0 |
| **Estado** | [Borrador / En revisión / Aprobado] |
| **Fecha de aprobación** | [COMPLETAR] |
| **Elaborado por** | RSI |
| **Revisado por** | Comité de Seguridad de la Información |
| **Aprobado por** | Directorio |
| **Clasificación** | Uso interno |
| **Próxima revisión** | [Fecha, máx. 1 año] |

### 1. Objetivo
Detectar oportunamente comportamientos anómalos o intrusiones en los sistemas y redes del Banco y convertirlos en alertas gestionadas que alimenten el Plan de Respuesta a Incidentes (RS-01).
### 2. Alcance
Aplica a [COMPLETAR: todos los sistemas monitoreados según DE-01, incluyendo la red, los endpoints, las aplicaciones de banca y el sistema de pagos].
### 3. Casos de uso de detección
| **Caso de uso** | **Señal a detectar** | **Ejemplo Banco** |
|---|---|---|
| **Login anómalo** | Acceso desde país inusual, horario atípico, cuenta comprometida | Cliente de Banco En Línea entra desde el exterior sin viaje previo |
| **Transferencia inusual** | Monto, destinatario o frecuencia fuera de línea base | Orden de pago de alto valor a una cuenta nueva |
| **Malware** | Firma de malware, comportamiento de ransomware | Cifrado masivo de archivos en una estación de sucursal |
| **Exfiltración** | Salida de datos en volumen hacia el exterior | Exportación masiva de la base de clientes a un disco o nube |
| **Uso indebido de privilegios** | Comando administrativo inusual | Un DBA lee datos de clientes fuera de su función |

### 4. Correlación y alertas
[COMPLETAR: reglas de correlación del SIEM], niveles de severidad (información / baja / media / alta / crítica), y canal de alerta (correo, ticket, consola). Toda alerta se registra con: fecha, origen, descripción, sistema afectado y responsable de la acción.
### 5. Umbrales y líneas base
[COMPLETAR: describir la línea base de cada caso de uso y los umbrales. Ej. más de 5 intentos de login fallidos en 10 minutos desde la misma IP = alerta media]. Las líneas base se recalculan [COMPLETAR: semestralmente] o ante cambios significativos de operación.
### 6. Escalamiento a respuesta (RS-01)
| **Severidad** | **Quién recibe** | **Tiempo objetivo de análisis** |
|---|---|---|
| Baja | Analista de monitoreo | [COMPLETAR: 4 h hábiles] |
| Media | Analista + RSI | [COMPLETAR: 2 h] |
| Alta | RSI + Div. TI | [COMPLETAR: 1 h] |
| Crítica | Comité / RSI convoca RS-01 | [COMPLETAR: inmediato] |

Las alertas confirmadas como incidente pasan al Plan de Respuesta (RS-01). Las descartadas se documentan como falsos positivos para calibrar las reglas.
### 7. Herramientas EDR/XDR/SIEM
[COMPLETAR: nombre de las herramientas, versión, responsabilidad de administración y proceso de actualización de firmas y reglas]. El mantenimiento de firmas es [COMPLETAR: automático / manual] y se verifica [COMPLETAR: diariamente].
### 8. Control de cambios
| **Versión** | **Fecha** | **Cambio** | **Elaboró** | **Aprobó** |
|---|---|---|---|---|
| 0.1 | [COMPLETAR] | Versión inicial (borrador) | RSI | — |
| 1.0 | [COMPLETAR] | Aprobación del Comité | RSI | Directorio |

## 5. Ejemplo aplicado al Banco (modelo de referencia)
Ejemplo ilustrativo. Adaptá a la operación real del Banco.
**Líneas base (ejemplo):**
- **Banco En Línea:** pico de logins de 8:00 a 13:00 (días hábiles); volumen mensual de transferencias de aproximadamente [X] por cliente.
- **Sucursales:** jornada hábil de 13:00 a 17:00; pocos accesos fuera de ese rango.
- **Red:** tráfico de sucursales concentrado en horario hábil; accesos VPN de funcionarios fuera de horario solo para áreas autorizadas.
**Umbrales (ejemplo):**
- 5 o más logins fallidos a Banco En Línea en 10 minutos → alerta media → se bloquea la IP y se avisa al área de banca.
- Transferencia de más de [X] UI a un beneficiario nuevo → alerta alta → revisión del Oficial de Cumplimiento.
- Detección de cifrado de 10+ archivos por minuto en un endpoint → alerta crítica → se aísla el equipo y se convoca RS-01.
- Salida de más de 100 MB desde el segmento de base de datos → alerta alta → investigación por exfiltración.
**Escalamiento (ejemplo):** el analista del SIEM confirma una alerta crítica a las 03:12 y activa la guardia del RSI, quien a las 03:40 convoca la respuesta según RS-01. A las 05:00 se aisló el endpoint afectado. El incidente se registra y se notifica conforme a RS-02.
**Calibración (ejemplo):** el 30% de las alertas del primer trimestre fueron falsos positivos de la regla de login geográfico; se ajustó la regla y se recalculó la línea base en la revisión de DE-01/DE-02 del mes siguiente.

**Documentos relacionados:**
- DE-01 (Monitoreo y Registro de Eventos)
- RS-01 (Respuesta a Incidentes) · RS-02 (Notificación) · RS-03 (Forense)
- PR-06 (Gestión de Vulnerabilidades) · BCU-04 (Gestión TI)
