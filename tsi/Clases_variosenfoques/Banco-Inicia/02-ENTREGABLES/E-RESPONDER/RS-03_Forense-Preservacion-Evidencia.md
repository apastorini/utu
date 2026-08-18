# RS-03 · Análisis Forense y Preservación de Evidencia del Banco

> ⚠️ **Alerta:** este documento menciona **nombres propios del organigrama del Banco** (personas y cargos, abril 2026). Antes de usar el documento, verificá la vigencia de esos nombres contra el organigrama actual.
> **Función del MCU 5.0:** Responder (RS.AN — Análisis)
> **ISO/IEC 27001:** A.5.28 (Recolección de evidencia)
> **BCU:** Circular 2227 (riesgo operativo) · RNRCSF (investigaciones de fraude)
> **URCDP:** Ley 18.331 art. 10 · Ley 19.670 art. 38
> **Nivel del curso:** 🔴 Dominar

## 1. Qué es y por qué existe
Este procedimiento define cómo el Banco recolecta, preserva y analiza la **evidencia digital** de un incidente de forma tal que sea íntegra, admisible y defendible. Cuando un incidente puede terminar en una sanción del BCU, una denuncia penal (fraude bancario, acceso ilegítimo a datos, sabotaje) o una reclamación de un cliente, lo que se hizo con los datos en las primeras horas determina si esa evidencia vale o no.
El principio central es la **no alteración**: cualquier acción del equipo de respuesta puede destruir evidencia (apagar un servidor, reinstalar un sistema, borrar un archivo). Por eso, antes de contener o limpiar, se preservan copias forenses (imágenes bit a bit), se calculan hashes y se documenta la **cadena de custodia**: quién tocó qué, cuándo y por qué.
En el Banco, la evidencia digital es útil tanto para investigaciones internas (un funcionario que accede a datos de clientes sin autorización) como para la defensa del banco ante reclamaciones y para el apoyo a la justicia penal. La confidencialidad del proceso es clave: solo participan quienes lo necesitan, y todo se documenta.
## 2. Marco de referencia
| **Norma** | **Referencia** | **Qué exige** |
|---|---|---|
| **MCU 5.0 (Agesic)** | RS.AN | Análisis de incidentes con preservación y documentación de la evidencia |
| **ISO/IEC 27001:2022** | A.5.28 | Recolección y custodia de evidencia conforme a requisitos legales |
| **BCU** | Circular 2227 | Investigación de eventos de riesgo operativo y fraude |
| **URCDP** | Ley 18.331 art. 10 · Ley 19.670 art. 38 | Preservar evidencia para la comunicación y defensa de los titulares |

## 3. Cómo completar esta plantilla (guía de llenado)
1. **Definí los roles de forense** con el RSI y Servicios Jurídicos: forense interno (División TI/Riesgos) o externo (contrato con especialista forense), con criterios de cuándo se convoca a cada uno.
2. **Documentá las técnicas de preservación** con la División TI: copias forenses, hashes (SHA-256), registro de tiempo y equipos de captura (write-blockers).
3. **Definí la lista de evidencia a preservar** según el tipo de incidente: logs (DE-01), imágenes de disco, memoria, tráfico de red, correo.
4. **Establecé la cadena de custodia** con Legal: formulario, responsables y custodia física del material.
5. **Pautá la coordinación con autoridades** con Legal: cuándo y cómo se entrega evidencia a la justicia, policía técnica, BCU o URCDP.
6. Consultá a **Auditoría Interna** (Cr. Marcelo Jorge) para casos de fraude interno y a **Capital Humano** para investigaciones disciplinarias de funcionarios.
## 4. Plantilla del documento

### ENCABEZADO
| **Campo** | **Valor** |
|---|---|
| **Código** | RS-03 |
| **Título** | Análisis Forense y Preservación de Evidencia |
| **Versión** | 1.0 |
| **Estado** | [Borrador / En revisión / Aprobado] |
| **Fecha de aprobación** | [COMPLETAR] |
| **Elaborado por** | RSI |
| **Revisado por** | División Servicios Jurídicos Notariales |
| **Aprobado por** | Directorio |
| **Clasificación** | Confidencial |
| **Próxima revisión** | [Fecha, máx. 1 año] |

### 1. Objetivo
Recolectar, preservar y analizar la evidencia digital de los incidentes de seguridad de forma íntegra, documentada y admisible, para apoyar la respuesta (RS-01), las obligaciones legales (RS-02) y las acciones disciplinarias, administrativas o penales que correspondan.
### 2. Alcance
Aplica a [COMPLETAR: todo incidente de severidad alta o crítica, fraude, acceso no autorizado a datos personales y denuncias]. La evidencia abarca sistemas propios y, cuando corresponda, equipos de funcionarios y registros de terceros.
### 3. Principios de preservación
- **No alterar la evidencia:** ninguna acción técnica sobre el sistema afectado sin evaluar primero su impacto probatorio.
- **Copias forenses:** trabajar siempre sobre copias bit a bit; el original queda sellado y custodiado.
- **Hashes:** calcular y registrar el hash (SHA-256) de cada evidencia antes y después del análisis.
- **Cadena de custodia:** documentar cada transferencia de custodia con nombre, fecha, hora y motivo.
- **Registro de relojes:** verificar la sincronización de tiempo (DE-01) para que las marcas de tiempo sean confiables.
### 4. Qué evidencia preservar
| **Tipo de incidente** | **Evidencia prioritaria** |
|---|---|
| **Intrusión / malware** | Imagen de disco y memoria del/los equipo/s afectados, logs del SIEM, tráfico de red |
| **Acceso no autorizado a datos** | Logs de autenticación y de base de datos, sesiones activas, auditoría del IAM |
| **Fraude / transferencia inusual** | Registros transaccionales, evidencia del sistema de pagos, correos y mensajes |
| **Phishing / ingeniería social** | Correos originales (cabeceras completas), sitios imitación, registros de apertura |
| **Denuncia interna** | Registros de acceso del funcionario, correo, dispositivos de la estación de trabajo |

### 5. Roles del análisis forense
| **Rol** | **Titular sugerido** | **Función** |
|---|---|---|
| **Coordinador forense** | RSI | Decide qué se preserva, convoca y coordina el proceso |
| **Forense interno** | División TI (perfil designado) | Ejecuta preservación y análisis en casos de severidad media/baja |
| **Forense externo** | Proveedor contratado | Casos complejos, sensibles o con impacto legal, con autorización escrita |
| **Legal** | División Servicios Jurídicos | Valida la cadena de custodia y la entrega a autoridades |
| **DPD** | Delegado de Protección de Datos | Determina el alcance de datos personales afectados |

### 6. Coordinación con autoridades
[COMPLETAR: criterios para dar intervención a la justicia, la Policía Técnica, el BCU o la URCDP; la entrega de evidencia se hace siempre a través de Legal y con oficio/resolución según corresponda]. El forense prepara el informe técnico que acompañará la comunicación.
### 7. Confidencialidad del proceso
El proceso forense es **confidencial**: solo participan los roles autorizados; los resultados se comunican por canales seguros; el material de evidencia se custodia en lugar con acceso restringido y registrado. El incumplimiento de la confidencialidad se trata conforme al régimen disciplinario del Banco.
### 8. Control de cambios
| **Versión** | **Fecha** | **Cambio** | **Elaboró** | **Aprobó** |
|---|---|---|---|---|
| 0.1 | [COMPLETAR] | Versión inicial (borrador) | RSI | — |
| 1.0 | [COMPLETAR] | Aprobación del Directorio | RSI · Legal | Directorio |

## 5. Ejemplo aplicado al Banco (modelo de referencia)
Ejemplo ilustrativo. Adaptá a la operación real del Banco.
**Caso: acceso indebido de un funcionario a datos de clientes (ejemplo):**
- El DPD recibe una denuncia de un cliente que encontró datos propios en poder de un tercero. Se abre investigación.
- **Preservación:** el RSI ordena congelar los registros de acceso del funcionario sospechoso: se extraen los logs del IAM y del SGBD y se calcula el hash SHA-256 de cada exportación; se registra la cadena de custodia.
- **Análisis:** el forense interno verifica que el funcionario consultó 1.500 fichas de clientes entre [fechas], fuera de su función, con horarios y sesiones coincidentes con su usuario.
- **Coordinación:** Legal evalúa la relevancia penal (art. 302 y ss. C.P., acceso ilegítimo) y coordina con la Policía Técnica la entrega de la evidencia con oficio. El DPD evalúa si corresponde comunicar la vulneración a la URCDP (RS-02): se determina que no hubo fuga fuera del banco, pero igual se documenta la decisión.
- **Confidencialidad:** el caso se manejó solo entre RSI, DPD, Legal y Capital Humano; los resultados del informe se conservan bajo acceso restringido.
**Caso: intrusión externa (ejemplo):** ante una intrusión detectada por el SIEM, antes de "limpiar" el servidor se realiza la imagen forense con write-blocker; el original se custodia sellado. El informe forense se adjunta a la notificación al BCU y a la eventual denuncia penal.

**Documentos relacionados:**
- RS-01 (Respuesta a Incidentes) · RS-02 (Notificación)
- DE-01 (Registros) · DE-02 (Detección)
- PR-01 (Accesos) · URCDP-02 (Notificación de Vulneraciones)
