# INFRA-12 · Monitoreo, SIEM y Alertas: Cómo Observar la Red

> **Función del MCU 5.0:** Detectar (DE.CM Monitoreo continuo, DE.AE Anomalías) — el monitoreo es la función que convierte la red en "visible". También apoya Responder (RS.MA, RS.AN) al entregar la materia prima de la investigación.
> **ISO/IEC 27001:** Registro de eventos (A.8.15), monitoreo de actividades (A.8.16), protección contra malware (A.8.7) y gestión de incidentes (A.5.24).
> **BCU:** La Estrategia de Monitoreo y Gestión del Riesgo de TIC de la EMG exige ver y registrar lo que pasa en los sistemas que sostienen las operaciones del banco; el monitoreo es su base técnica (BCU-03, BCU-04).
> **URCDP:** El registro y control de accesos es una medida lógica del Documento de Seguridad (URCDP-01) y la base para notificar vulneraciones a tiempo (URCDP-02).
> **Decreto 66/025:** Art. 11.a — las entidades deben mantener **trazabilidad centralizada de eventos de seguridad por al menos 12 meses**; el monitoreo y el SIEM son la herramienta que hace posible ese requisito. También apoya la detección y notificación temprana de incidentes (art. 10.g).
> **Nivel del curso:** 🟡 Practicar · 🔴 Dominar

---

## 1. La idea central: la seguridad que no se ve, no existe

Una red puede tener el mejor firewall, el mejor EDR y todos los parches al día. Si nadie **mira** lo que pasa, un atacante que ya está dentro puede moverse durante semanas sin que nadie se entere. El ransomware más caro de la historia empezó con un acceso que los registros mostraban… pero nadie los leía.

> **Analogía:** la red es un edificio. El firewall es la puerta con seguridad, el EDR es la alarma por puerta. Pero si el vigilante se duerme, ninguna alarma sirve. **El SIEM es el vigilante** que mira todas las cámaras a la vez y avisa cuando algo no cuadra.

Este módulo te enseña:

- Qué es un log y qué cosas del banco generan registros.
- Cómo se centralizan los registros (sin centralización no hay visión).
- Qué es un SIEM, qué es un SOC y qué es un caso de uso (use case).
- Cómo se define un umbral y una alarma sin morir en "falsos positivos".
- Qué debe ver el RSI cada mes para poder reportar a Dirección.

---

## 2. Qué se observa: las fuentes de eventos

Todo dispositivo y sistema que se comporte de forma "útil" puede dejar registros. En un banco, las fuentes mínimas que un SIEM debe cubrir son:

| Fuente | Qué registra | Ejemplo de evento importante |
|---|---|---|
| Firewall (perimetral y zonas) | Tráfico permitido y bloqueado | Bloqueo de conexión saliente sospechosa |
| Switches y routers | Acceso administrativo, cambios de configuración, errores de puerto | Login a un switch desde IP externa |
| Servidores (Windows/Linux) | Inicio de sesión, altas de usuarios, cambios de permisos | Login fuera de horario de una cuenta administrativa |
| Directorio Activo (AD) | Autenticaciones, altas/bajas, cambios de contraseña | Cuenta del director bloqueada tras 20 intentos |
| Antivirus / EDR | Detecciones, cuarentenas, actualizaciones | Malware detectado en una PC de caja |
| Base de datos | Consultas, accesos privilegiados, exports | Export masivo de datos de clientes |
| Aplicaciones (home banking, core) | Transacciones, errores, accesos | Intento de transferencia anómala |
| DLP | Fuga de datos por correo, USB, web | Correo con datos de clientes a dominio externo |
| VPN / acceso remoto | Conexiones, autenticaciones, desconexiones | Conexión VPN desde país extranjero |
| Correo | Mensajes entrantes/salientes, phishing detectado | Correo de suplantación dirigido a gerencia |
| Sistemas físicos (cámaras, acceso) | Entradas a salas, apertura de racks | Apertura del rack de datos fuera de horario |

### La anatomía de un log

Todo registro debe poder responder, como mínimo, a estas preguntas (los ingleses usan las **5 W**):

| Pregunta | Campo típico |
|---|---|
| ¿Quién? | Usuario, cuenta, IP de origen |
| ¿Qué? | Acción realizada (login, acceso, cambio) |
| ¿Cuándo? | Fecha y hora (¡con zona horaria!) |
| ¿Dónde? | Equipo, servicio, aplicación |
| ¿Desde dónde? | IP, MAC, ubicación física/lógica |

> **Regla práctica del RSI:** si un log no dice quién, qué, cuándo, dónde y desde dónde, no sirve como evidencia. Cuando pidas configurar registros, usa esta lista de 5 preguntas como checklist.

---

## 3. El problema que resuelve el SIEM: los registros dispersos

Imaginá que el banco tiene 300 equipos y cada uno guarda sus registros en su propio disco. Para saber qué pasó a las 03:17 en el servidor de pagos, tendrías que entrar de a uno por servidor. Y lo peor: no podrías **correlacionar** —ver la misma IP atacando primero a un servidor web, después al correo y después a la base de datos—.

La solución tiene tres capas:

1. **Centralización:** todos los registros se envían a un lugar común (el recolector del SIEM o un clúster de logs).
2. **Normalización:** los formatos distintos (Windows, Linux, firewall, app) se convierten a un formato común con los mismos campos.
3. **Correlación y análisis:** el SIEM cruza eventos, aplica reglas, detecta patrones y dispara alertas.

### Cómo llegan los registros al SIEM

| Método | Cómo funciona | Para qué sirve |
|---|---|---|
| Syslog | Protocolo estándar (UDP/TCP puerto 514); el dispositivo "emite" sus logs | Firewalls, routers, switches, servidores Linux |
| Agente | Un programa instalado en el equipo envía eventos | Windows (Event Log), EDR, bases de datos |
| API / plugin | El SIEM consulta el sistema por su interfaz | Nube (AWS/Azure/O365), aplicaciones SaaS |
| Forwarder de archivos | Lee archivos de log planos y los indexa | Aplicaciones propias, logs de aplicaciones web |

> **Analogía:** el SIEM es el centro de vigilancia. Los syslog son las cámaras que ya graban solas; los agentes son cámaras instaladas adentro de cada sala; las APIs son cámaras del edificio vecino al que pedimos imágenes.

### ¿Qué SIEM es realista para el Banco?

No hace falta gastar en un SOC tercerizado para empezar. La madurez se construye por etapas:

| Etapa | Herramienta (código abierto/gratuita) | Qué lográs |
|---|---|---|
| 1 · Centralizar | **Wazuh** o **Elastic Stack (ELK)** o **Graylog** | Todos los logs en un solo lugar, búsqueda rápida |
| 2 · Correlacionar | Reglas de correlación del SIEM elegido | Alertas automáticas por patrón |
| 3 · Analizar | **Zeek** (red), **TheHive** (gestión de casos) | Detección de protocolos, tickets de incidentes |
| 4 · Operar | **Security Onion** (distribución completa) | Sensores + SIEM + análisis en una sola distro |

El laboratorio INFRA-10 ya usa esta familia de herramientas; este módulo te dice qué mirar en cada una.

---

## 4. Casos de uso: qué reglas de alerta se configuran

Una regla de correlación es una condición: "si ocurre X dentro de un período Y, avisá". El arte está en definir condiciones que detecten **comportamiento real** y no ruido. Casos de uso básicos para un banco:

| # | Caso de uso (use case) | Regla típica | ¿Qué puede significar? |
|---|---|---|---|
| 1 | Fuerza bruta (brute force) | 10+ logins fallidos a la misma cuenta en 5 min | Ataque de contraseñas |
| 2 | Login fuera de horario | Login administrativo entre 22:00 y 06:00 | Cuenta comprometida o acción interna |
| 3 | Origen inusual | Login desde IP de país extranjero sin VPN corporativa | Cuenta robada, acceso no autorizado |
| 4 | Movimiento lateral | Una PC de caja intenta conectarse a servidores de datos | Atacante explorando la red |
| 5 | Comando administrativo raro | PowerShell/psexec ejecutado en servidores de producción | Técnica habitual de ransomware |
| 6 | Export masivo | Base de datos exporta >X registros en minutos | Exfiltración de datos |
| 7 | Nuevo servicio | Un servidor abre puerto 445/3389 hacia la red interna | Puerta trasera instalada |
| 8 | DNS sospechoso | Consultas a dominios de phishing conocidos o DGA | Comunicación con C2 (comando y control) |
| 9 | Malware detectado | EDR reporta detección en cualquier equipo | Infección activa |
| 10 | Cambio de configuración crítico | Se modifica regla del firewall perimetral sin ticket | Configuración maliciosa o errónea |

### La clave del RSI: menos alertas, mejores alertas

La **fatiga de alertas** ocurre cuando el SIEM dispara 500 avisos por día y el equipo termina ignorándolos todos. La regla de oro:

> **Si el analista ignora la alarma, es como si no existiera.** Mejor 20 alertas que se investigan que 500 que se borran.

Para eso, cada regla debe tener: un nombre claro, una descripción del riesgo, el nivel de severidad, el responsable de investigarla y la acción esperada (mitigar, escalar, archivar). Ese catálogo de reglas se llama **catálogo de casos de uso** y debe revisarse con el equipo (DE-01/DE-02).

---

## 5. Umbrales, líneas de base y anomalías

Un umbral mal puesto genera ruido; uno demasiado alto deja pasar el ataque. La técnica correcta es partir de la **línea de base**: medir el comportamiento normal durante un tiempo y luego definir qué se aparta de ella.

| Concepto | Definición | Ejemplo en el banco |
|---|---|---|
| Línea de base | Volumen/horario/patrón normal de un evento | El core exporta backups todos los sábados 02:00 |
| Anomalía | Desviación significativa de la línea de base | Export de datos un martes 15:00 |
| Umbral | Valor numérico a partir del cual se alerta | >5 intentos de login en 10 minutos |
| Ruido / falso positivo | Alerta que se dispara sin riesgo real | Backup de los sábados marcado como export anómalo |

**Cómo se construye una línea de base en la práctica:**

1. Recolectar eventos durante 30–60 días.
2. Definir rangos normales por fuente (horarios, volúmenes, orígenes).
3. Configurar alertas con **dos niveles**: aviso (info) y alarma (escalable).
4. Ajustar con el tiempo: cada falso positivo se usa para calibrar la regla.

> **Regla práctica:** si una regla genera más del 20% de falsos positivos, está mal calibrada. Se ajusta o se apaga, y eso queda documentado (DE-02).

---

## 6. El ciclo de la alarma: de la alerta a la respuesta

Una alarma no termina en el correo que la avisa. El ciclo completo es:

```
Detección → Triage (¿es real?) → Clasificación → Escalamiento → Respuesta → Cierre con lección
```

| Paso | Qué se hace | Responsable |
|---|---|---|
| Detección | El SIEM dispara la alerta | SIEM / SOC |
| Triage | En <15 min se decide: real, falso positivo, o requiere investigación | Analista SOC / TI |
| Clasificación | Severidad (crítica/alta/media/baja) según impacto posible | Analista SOC |
| Escalamiento | Si es real: activar RS-01 (plan de respuesta a incidentes) y notificar (RS-02) | RSI |
| Respuesta | Contener, erradicar, recuperar | Equipo de respuesta |
| Cierre | Documentar, actualizar el caso de uso, lecciones aprendidas (RC-04) | RSI |

### Cuándo se notifica al CERTuy

El **Decreto 66/025 (art. 10.g)** obliga a las entidades públicas a **notificar incidentes al CERTuy** según el procedimiento que este establezca (y en general la práctica de notificación temprana es la que exigen también BCU y URCDP). Para saber si una alerta amerita notificación, el RSI se pregunta:

- ¿Afecta datos personales? → notificación a URCDP (Ley 19.670 / Decreto 64/020).
- ¿Afecta servicios u operaciones del banco? → BCU (EMG).
- ¿Es un incidente de ciberseguridad de impacto? → CERTuy (Decreto 66/025, art. 3 y 10).

---

## 7. Lo que el RSI debe ver: el reporte mensual de monitoreo

El RSI no lee 500.000 logs; lee **informes**. El reporte mensual de monitoreo (que alimenta a GV-06 y a BCU-03/BCU-04) debe incluir:

| Indicador | Qué muestra | Fórmula simple |
|---|---|---|
| Eventos totales por fuente | Qué tanto se está registrando | Conteo por fuente de logs |
| Alertas totales | Volumen de actividad sospechosa | Conteo de alertas |
| Alertas por severidad | Distribución del riesgo | Críticas / altas / medias / bajas |
| Falsos positivos | Calidad de las reglas | Falsos positivos / alertas totales |
| Alertas investigadas a tiempo | Disciplina del equipo | Investigadas dentro del SLA / total |
| Incidentes confirmados | Resultado real | Alertas que pasaron a incidente |
| Cobertura de fuentes | Cuánto del banco se observa | Fuentes conectadas / fuentes inventariadas |
| Retención de logs | Cumplimiento del Decreto 66/025 | Logs con ≥12 meses disponibles |

> **Regla práctica:** si el reporte mensual muestra que la cobertura de fuentes baja (hay servidores sin conectar al SIEM), el RSI debe tratarlo como un hallazgo de auditoría, no como una nota a pie de página.

---

## 8. Checklist del RSI sobre monitoreo

| Pregunta | Qué implica |
|---|---|
| ¿Todos los activos críticos envían logs al SIEM? | Cobertura (ID-01 + DE-01) |
| ¿Los logs se conservan ≥12 meses? | Trazabilidad (Decreto 66/025 art. 11.a) |
| ¿El reloj de todos los equipos está sincronizado? | NTP — sin hora única no hay correlación |
| ¿Hay un catálogo de casos de uso documentado? | Reglas con nombre, severidad y responsable |
| ¿Alguien investiga las alertas dentro de un plazo? | SLA de triage |
| ¿El reporte mensual llega a Dirección? | Evidencia para GV-06 y BCU |
| ¿Se prueban las reglas con simulaciones? | El laboratorio INFRA-10 permite disparar eventos |

---

## 9. Ejercicios para practicar (vínculo con INFRA-10)

1. En el laboratorio, configurá el firewall pfSense para enviar sus logs al SIEM (Wazuh/ELK). Verificá que aparezcan.
2. Generá un evento (por ejemplo, 12 logins fallidos con Nmap) y confirmá que el SIEM dispara la regla de fuerza bruta.
3. Definí 5 casos de uso para el Banco con nivel de severidad y responsable (plantilla en DE-02).
4. Armá el reporte mensual de monitoreo con los indicadores de la sección 7, usando datos reales del laboratorio.
5. Probá el ciclo completo: detección → triage → clasificación → escalamiento → cierre con lección aprendida.

---

## 10. Cierre del módulo

"Observar" no es tener logs; es tener **visión**: logs centralizados, reglas que detectan comportamiento anómalo y un equipo que investiga las alertas a tiempo. El SIEM es la herramienta; el SOC o el equipo de TI es el cerebro; el RSI es quien garantiza que el sistema se use, se reporte y se mejore. El siguiente paso natural es INFRA-13 (qué preguntar y qué pedir) e INFRA-14 (obligaciones del Decreto 66/025).

### Checklist del módulo

- ☐ Identifiqué las fuentes de logs del banco y las conecté a la centralización.
- ☐ Definí los primeros casos de uso con severidad y responsable.
- ☐ Establecí líneas de base y umbrales sin caer en fatiga de alertas.
- ☐ Defini el ciclo alarma → triage → escalamiento → respuesta → cierre.
- ☐ Armé el reporte mensual de monitoreo con indicadores.
- ☐ Verifiqué que los logs críticos se conserven ≥12 meses.

---

**Documentos relacionados:** GV-06, ID-01, PR-06, DE-01, DE-02, DE-03, RS-01, RS-02, RC-04, BCU-03, BCU-04, URCDP-01, URCDP-02, INFRA-02, INFRA-10 · Referencias normativas: MCU 5.0 (DE.CM, DE.AE), ISO/IEC 27001 A.8.15/A.8.16, BCU EMG (Estrategia de Monitoreo y Gestión del Riesgo de TIC), Decreto 66/025 arts. 10–13
