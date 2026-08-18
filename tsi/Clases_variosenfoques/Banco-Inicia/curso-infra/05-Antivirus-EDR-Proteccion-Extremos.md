# INFRA-05 · Antivirus, EDR y Protección de Extremos

> **Función del MCU 5.0:** Proteger los puntos finales (equipos) de la red contra malware, con detección, respuesta y monitoreo continuo.
> **ISO/IEC 27001:** Anexo A.8.7 Protección contra el malware.
> **BCU:** BCU-03 (protección de datos) — medida técnica de protección de los extremos.
> **URCDP:** URCDP-01 y URCDP-02 — medidas de seguridad técnicas y respuesta ante incidentes de datos personales.
> **Nivel del curso:** 🟢 Descubrir · 🟡 Practicar · 🔴 Dominar

---

## 1. Introducción: la puerta de entrada de los peligros

Imaginá que cada computadora del banco es una **oficina** del edificio. Tiene puertas y ventanas: el correo electrónico, el navegador de Internet, los pendrives que se enchufan, los archivos que se descargan. Por esas puertas puede entrar algo no deseado: un **programa malicioso** (malware).

El malware es como un ladrón que:

- Entra escondido en un archivo adjunto (parece inofensivo).
- Espera a que alguien lo abra para actuar.
- Roba información, cifra los archivos (ransomware) o convierte al equipo en "títere" del atacante.

> **Analogía rápida:** el antivirus es el guardia que revisa la identidad de todos los que entran a la oficina usando **fotos de criminales conocidos** (firmas). El **EDR** es el sistema de cámaras y sensores que vigila *qué hace* la gente dentro de la oficina y puede encerrar a un sospechoso a distancia.

Este archivo te explica malware, antivirus, EDR, sandbox y cómo construir una **política de protección de extremos** con sus evidencias para el kit.

---

## 2. ¿Qué es el malware y por qué llega a los equipos?

### 2.1 Definición

**Malware** (malicious software) es cualquier programa creado con intención dañina. "Programa malicioso" en una palabra.

### 2.2 Cómo llega

| Vía de entrada | Ejemplo |
|---|---|
| **Correo electrónico** | Adjunto infectado, enlace a una página falsa (phishing) |
| **Web** | Descarga de un programa "gratis" que viene con malware escondido |
| **USB y dispositivos** | Pendrive con archivos infectados de otra computadora |
| **Vulnerabilidades** | Un programa viejo sin parches que deja una puerta abierta (enlaza con INFRA-04) |

### 2.3 Tipos de malware

- **Virus:** se pega a un archivo y se propaga cuando se abre.
- **Troyano:** se disfraza de programa legítimo (el "caballo de Troya"): parece útil, pero abre una puerta trasera.
- **Ransomware:** **cifra los archivos** de la víctima y pide rescate para desbloquearlos. El más temido por los bancos.
- **Spyware:** espía en silencio: roba contraseñas, captura pantallas, registra teclas.
- **Phishing con carga:** un correo engañoso que lleva el malware dentro (el anzuelo + el ladrón).
- **Cryptominer:** usa los recursos del equipo para minar criptomonedas del atacante, sin que nadie lo note (rinde poco al atacante, pero deteriora el equipo y consume recursos).

> **Nota:** el malware no "entra solo". Siempre hay una puerta: un clic, una descarga, un USB, una vulnerabilidad. La protección de extremos cierra esas puertas y detecta al que ya pasó.

---

## 3. Antivirus tradicional: la lista de "buscados"

El **antivirus tradicional** funciona comparando los archivos con una base de datos de **firmas** (o hashes).

- **Firma:** una "huella digital" única de cada malware conocido (una secuencia de caracteres calculada del archivo).
- Si el archivo que se va a abrir tiene la huella de un malware conocido → se bloquea o se elimina.

### 3.1 Límites del antivirus de firmas

1. **No detecta lo desconocido:** si el malware es nuevo y nadie lo catalogó, no hay firma. Se llama **malware de día cero** (zero-day).
2. Los atacantes **modifican el archivo** apenas (cambiar unas letras) para que la huella no coincida. Eso se llama *polimorfismo*.
3. Solo mira el archivo en sí, no el **comportamiento**: no nota que un programa legítimo se está comportando de forma rara.

> **Analogía:** el antivirus de firmas tiene las fotos de los ladrones conocidos. Un ladrón nuevo, o uno con barba postiza, pasa desapercibido.

---

## 4. EDR: el sistema de cámaras y respuesta remota

**EDR** (Endpoint Detection and Response) es la evolución del antivirus. En vez de solo mirar las huellas, **vigila el comportamiento** de todo lo que pasa en el equipo.

### 4.1 Qué hace un EDR

- **Telemetría continua:** registra procesos, archivos, conexiones de red, teclas, uso de memoria. Es como tener cámaras en cada rincón.
- **Detección por comportamiento:** detecta **anomalías** (patrones sospechosos): un programa de oficina que de repente cifra miles de archivos, o un proceso que intenta conectarse a una IP desconocida.
- **Respuesta remota:** el equipo de seguridad puede **aislar** (desconectar de la red) un equipo infectado desde la consola, sin ir físicamente. Contiene el incidente en segundos.
- **Búsqueda proactiva (hunting):** permite investigar si un atacante ya estuvo ("¿alguna vez se ejecutó X?").

### 4.2 EDR vs antivirus

| Característica | Antivirus tradicional | EDR |
|---|---|---|
| Base de firmas | Sí | Sí (también) |
| Detección de comportamiento | No | Sí |
| Visión continua del equipo | No | Sí |
| Respuesta remota (aislar) | No | Sí |
| Búsqueda en el pasado | Limitada | Sí |

> **Conclusión del curso:** el antivirus avisa "este archivo es malo". El EDR avisa "este equipo está haciendo algo raro, lo aíslo ahora mismo". En un banco se necesitan **ambos** (hoy la mayoría de los EDR incluyen antivirus).

### 4.3 Mención de XDR

**XDR** (Extended Detection and Response) extiende la visión del EDR a todo: correo, red, nube, servidores. En vez de mirar cada equipo por separado, **correlaciona** los datos de todos lados para ver la historia completa de un ataque. Es una mejora evolutiva (🟡 mención) que el banco puede adoptar según presupuesto.

---

## 5. EPP y NGAV: de la firma al machine learning

- **EPP** (Endpoint Protection Platform): la "plataforma completa" que incluye antivirus, firewall personal y control de dispositivos.
- **NGAV** (Next-Generation Antivirus): antivirus moderno que suma **machine learning**: aprende de millones de archivos para predecir si uno es malicioso aunque nunca lo haya visto. Reduce la dependencia de las firmas.

> **Concepto:** ya no alcanza con "¿lo vi antes?" (firma). Ahora también se pregunta "¿se parece a lo malo?" (machine learning) y "¿se está comportando mal?" (EDR). Esas tres respuestas juntas dan protección.

---

## 6. Sandbox: el laboratorio de pruebas

El **sandbox** (caja de arena) es un **entorno aislado** donde se ejecuta un archivo sospechoso para ver qué hace, sin riesgo para la red real.

- Un archivo adjunto dudoso se abre dentro del sandbox.
- Se observa su comportamiento unos minutos.
- Si intenta cosas raras (crear archivos, conectarse a Internet, cifrar datos), se lo marca como malicioso.
- La red real no se contamina: es como probar una sustancia en un laboratorio blindado antes de tocarla.

> **Analogía:** los bomberos queman un material en un contenedor a prueba de fuego para ver cómo reacciona, antes de usarlo en el edificio.

---

## 7. Política de protección de extremos

Una política clara es la base de todo. Debe decir:

### 7.1 Instalación obligatoria

- Todos los equipos (escritorios, notebooks, servidores, quioscos) deben tener el antivirus + EDR instalado y **activo**.
- No se permite "desinstalarlo porque molesta". Las bajas de cobertura deben ser excepcionales, autorizadas y con justificación.

### 7.2 Exclusiones controladas

- A veces hay que **excluir** un archivo o proceso del análisis (porque da falsos positivos o afecta el rendimiento).
- Las exclusiones se piden con justificación, se aprueban por un responsable y se **revisan periódicamente**. Nunca se agregan exclusiones "para probar".

### 7.3 Actualización y escaneos

- Las firmas se actualizan automáticamente (mínimo diario).
- Escaneo completo periódico (por ejemplo, semanal en horario nocturno) y escaneo al conectar dispositivos extraíbles.

### 7.4 Aislamiento automático y respuesta

- Ante una detección crítica, el equipo se **aísla automáticamente** de la red (o lo hace el equipo de seguridad a mano).
- Hay un **procedimiento de respuesta ante detección** que define quién hace qué y en qué orden (enlaza con **RS-01**).

---

## 8. Monitoreo del EDR

El EDR tiene una **consola** donde el equipo de seguridad ve:

- **Alertas:** eventos sospechosos con severidad (baja, media, alta, crítica).
- **Estado de los equipos:** cobertura, última actualización de firmas, último escaneo.
- **Línea de tiempo:** qué pasó en cada equipo antes, durante y después de un evento.

### 8.1 Correlación con SIEM

Los logs del EDR pueden enviarse al **SIEM** (el centro de monitoreo que junta logs de toda la red, enlaza con **DE-01/DE-02**). Así una alerta del EDR se cruza con el log del firewall (INFRA-03) y se ve el cuadro completo: "este equipo descargó X del firewall y luego intentó conectarse a tal IP".

### 8.2 Reportes

Reportes útiles:

- Cobertura de endpoints (porcentaje protegido).
- Alertas del mes y cómo se resolvieron.
- Cantidad de equipos aislados y motivo.
- Estado de las exclusiones.

---

## 9. Endpoints especiales

No todos los extremos son una computadora de escritorio:

- **Servidores:** protección con configuraciones especiales (no se reinician cuando quieren; a veces el antivirus debe tolerar cargas de trabajo altas).
- **Quioscos de sucursal:** equipos de autoservicio (consulta de saldos, impresión de recibos). Se protegen y se **restringen** (solo la aplicación autorizada, nada más). Se pueden gestionar con **whitelisting** (solo se ejecuta lo permitido).
- **Cajeros / ATM (mención):** equipos muy especiales con requerimientos normativos propios y aislados de la red general.
- **Tablets y celulares:** se protegen con **MDM** (Mobile Device Management), que permite administrar la flota de dispositivos móviles: instalación de apps permitidas, cifrado, borrado a distancia si se pierde.

---

## 10. Checklist de implementación

- ☐ Inventario de todos los endpoints y cuántos tienen antivirus + EDR activo.
- ☐ Cobertura objetivo: 100% de los equipos de la organización (documentar el % real).
- ☐ Antivirus y EDR activos y con firmas actualizadas.
- ☐ Lista de **exclusiones** revisada y con justificación aprobada.
- ☐ Procedimiento de **triaje de alertas** (quién las revisa y cómo se cierran).
- ☐ **Simulacros de ransomware** periódicos (enlaza con **PR-02** y **Gophish**): enviar un correo falso y un archivo "carnada" para probar que la protección detecta y que el personal no cae en el phishing.
- ☐ Prueba de **restauración**: verificar que los backups permiten recuperar archivos cifrados por ransomware (si no se puede restaurar, la defensa está incompleta).

---

## 11. Errores comunes

1. **Cobertura incompleta:** equipos viejos, de pruebas o de proveedores sin protección. Un solo equipo sin proteger es una puerta abierta.
2. **Exclusiones excesivas:** exclusiones "de memoria", sin justificar, que dejan zonas sin analizar.
3. **No revisar la consola:** el EDR instalado pero nadie mira las alertas. Es como tener cámaras apagadas.
4. **Alertas ignoradas:** alertas que "son falsos positivos" sin investigar. A veces un falso positivo es un ataque real disimulado.
5. **No probar la restauración:** confiar en los backups sin nunca restaurar. El ransomware se combate con backups reales y probados.
6. **Sin procedimiento de respuesta:** cuando suena la alarma, nadie sabe qué hacer.

---

## 12. Relación con el kit y evidencias

| Documento | Aporte |
|---|---|
| **GV-04** | Política de protección de malware y extremos |
| **ID-01** | Inventario de endpoints cubiertos por el EDR |
| **PR-01** | Control de acceso y cuentas en los equipos |
| **PR-02** | Simulacros de phishing y ransomware |
| **PR-06** | Actualización de firmas y de la plataforma EDR |
| **DE-01 / DE-02** | Monitoreo y correlación con SIEM |
| **RS-01** | Procedimiento de respuesta ante una detección |
| **RS-02** | **Notificación a URCDP** si el incidente afecta datos personales |
| **BCU-03** | Protección de los datos en los extremos |
| **URCDP-01** | Medidas de seguridad técnicas |
| **URCDP-02** | Notificación de incidentes de datos personales |

### 12.1 Evidencias que se archivan con INFRA-05

- **Reporte de cobertura** extraído de la consola (cantidad de equipos, % con antivirus + EDR activo, última actualización).
- **Políticas** de protección de endpoints (escaneos, exclusiones, aislamiento).
- **Procedimiento de respuesta ante detección** (quién, qué, cómo, a quién notificar — incluye RS-02).
- Registro de **simulacros** (fecha, resultado, acciones).
- Registro de **pruebas de restauración**.

> **Tip de evidencias:** las capturas de la consola del EDR (sin datos sensibles) son la evidencia más contundente: muestran cobertura, alertas resueltas y acciones tomadas.

---

## 13. Actividades de práctica

**Checklist final:**

- ☐ Elaborar un reporte de cobertura de endpoints (real o de ejemplo).
- ☐ Escribir la política de exclusiones con plantilla de justificación.
- ☐ Definir el procedimiento de respuesta ante una alerta crítica (5 pasos).
- ☐ Planificar un simulacro de ransomware con Gophish (enlace PR-02).
- ☐ Verificar la ruta de notificación a URCDP si el incidente afecta datos personales (RS-02).
- ☐ Guardar todas las evidencias en la carpeta del kit.

---

**Documentos relacionados:** GV-04, ID-01, PR-01, PR-02, PR-06, DE-01, DE-02, RS-01, RS-02, BCU-03, URCDP-01, URCDP-02, MATRIZ-001.
