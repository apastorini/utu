# INFRA-03 · Firewalls, DMZ y Segmentación

> **Función del MCU 5.0:** Proteger los activos de información controlando el tráfico de red y separando las zonas de confianza.
> **ISO/IEC 27001:** Anexo A.8.1.1 Control de redes (criterio: aplicable).
> **BCU:** BCU-01 (seguridad de TI), BCU-03 (protección de datos) — medida técnica de control de acceso y segmentación.
> **URCDP:** URCDP-01 — medidas de seguridad técnicas y organizativas apropiadas.
> **Nivel del curso:** 🟢 Descubrir · 🟡 Practicar · 🔴 Dominar

---

## 1. Introducción: el guardia de seguridad de tu banco

Imaginá que el banco es un edificio grande. La gente entra y sale, los empleados trabajan en oficinas, hay una caja fuerte con dinero y documentos. ¿Qué necesita el edificio para funcionar seguro?

- Puertas de entrada.
- Un guardia que mira quién entra y quién sale.
- Reglas claras: quién puede pasar, a qué hora, con qué autorización.

En la red del Banco pasa exactamente lo mismo. La red es el edificio, los datos son el dinero, y el **firewall** es el guardia de seguridad. Todo lo que circula por la red (paquetes de información) pasa por el firewall, y él decide: **permitir** o **denegar**.

Pero el guardia no decide al azar. Decide según **reglas**. Una regla típica sería:

- "Si el paquete viene de la computadora del empleado Juan y va hacia el sistema de legajos, permitir".
- "Si el paquete viene de Internet y va hacia la base de datos de clientes, denegar".

Este archivo te explica desde cero qué es un firewall, qué es una DMZ, qué es la segmentación de red, y cómo todo esto se convierte en **evidencia** para el kit Banco-Inicia (ID, PR, DE, BCU, URCDP).

> **Analogía rápida:** el firewall es el guardia, la DMZ es el vestíbulo cerrado del banco donde atienden a los visitantes, y la segmentación son las puertas internas que separan la caja fuerte del resto del edificio.

---

## 2. ¿Qué es un firewall?

### 2.1 La idea básica

Un **firewall** (en español "cortafuegos") es un dispositivo (o un programa) que se coloca entre dos redes y controla el tráfico según reglas. Puede ser:

- **Hardware:** una caja física con puertos de red (el más común en el banco).
- **Software:** un programa instalado en un servidor o en cada computadora (firewall personal).

### 2.2 Qué es un paquete

Toda la información que viaja por Internet se parte en pedazos pequeños llamados **paquetes**. Cada paquete lleva un sobre con datos:

- **IP origen:** la dirección del que envía.
- **IP destino:** la dirección del que recibe.
- **Puerto origen y destino:** el "número de puerta" del servicio (por ejemplo, el 443 es la puerta de las páginas web seguras; el 25 la del correo saliente).

El firewall lee ese sobre y decide. Pero no todos los firewalls leen la misma cantidad de información. Eso nos lleva al siguiente punto.

### 2.3 Stateless vs Stateful (sin estado y con estado)

- **Firewall stateless (sin memoria):** mira cada paquete por separado, como si no recordara al paquete anterior. Decide solo con IP y puerto. Es simple y rápido, pero fácil de engañar.
- **Firewall stateful (con estado):** recuerda las conversaciones. Si Juan abrió una página web (salió un paquete), el firewall **recuerda** esa conexión y deja volver la respuesta. Se llama **inspección de estado** o **SPI** (Stateful Packet Inspection). Es el estándar en los bancos.

> **Analogía:** el firewall stateless revisa cada carta sin recordar quién escribió antes. El stateful lleva una lista de "conversaciones en curso" y solo deja responder a quien ya está conversando. El de estado es el que conviene para un banco.

### 2.4 Qué es la inspección de paquetes (SPI)

La **inspección de paquetes** es mirar el contenido de cada paquete y su contexto:

1. Leer IP origen y destino.
2. Leer los puertos.
3. Consultar la tabla de conexiones activas (para el stateful).
4. Aplicar la regla que corresponda.

Si el firewall solo mira IP y puerto, se llama **filtrado por capa de red y transporte**. Si además mira el contenido del tráfico (por ejemplo, si es un archivo o una consulta web), hablamos de **filtrado por aplicación**, que es lo que hace un NGFW (siguiente sección).

### 2.5 Reglas allow/deny (permitir / denegar)

Las reglas del firewall son la lista de instrucciones del guardia. Cada regla dice:

| Campo | Ejemplo |
|---|---|
| Origen | 10.10.20.5 (computadora de Juan) |
| Destino | 10.10.30.10 (servidor de legajos) |
| Servicio | TCP 443 (web segura) |
| Acción | PERMITIR (allow) o DENEGAR (deny) |
| Justificación | "Acceso del área Recursos Humanos al sistema de legajos" |

El firewall recorre la lista desde arriba hacia abajo y aplica la **primera regla que coincida** (se llama *first-match*, primera coincidencia). Si ninguna regla coincide, se aplica la regla por defecto: **denegar todo**. Esta filosofía de "lo que no está permitido, está prohibido" se llama **principio de mínimo privilegio**.

---

## 3. Firewall de próxima generación (NGFW)

Un firewall tradicional mira direcciones y puertos. Un **NGFW** (Next-Generation Firewall) hace eso y además:

- **Inspección SSL:** descifra y examina el tráfico HTTPS (el de candadito en el navegador). Así no pasa "de incógnito" el malware escondido en una web "segura".
- **Control por usuario:** en vez de solo IP, identifica a la persona (por ejemplo, por el usuario de la red). Permite reglas del tipo "solo el área de Tesorería accede al core".
- **IPS integrado (Intrusion Prevention System):** detecta y bloquea ataques conocidos en tiempo real, como un policía dentro del edificio que intercepta a un ladrón antes de que actúe. Es una capa más de seguridad.
- **Filtrado por aplicación:** reconoce aplicaciones (navegación, correo, mensajería, redes sociales) y permite bloquearlas por usuario o por horario.

> **Nota de nivel:** en este curso, NGFW se marca 🟡 Practicar: no hace falta configurarlo, pero sí saber qué es y qué evidencia genera (sus logs y reportes).

---

## 4. Zonas de seguridad: Trusted, Untrusted y DMZ

### 4.1 ¿Qué es una zona?

Una **zona** es una parte de la red con el mismo nivel de confianza. El firewall tiene varias "puertas" llamadas **interfaces**, y cada interfaz se asocia a una zona. El tráfico de una zona a otra se regula con reglas.

Las tres zonas clásicas:

| Zona | Confianza | Contenido típico | Qué se permite |
|---|---|---|---|
| **Trusted (confiable)** | Alta | Red interna: escritorios de empleados, servidores core, impresoras | Acceso libre entre equipos internos |
| **Untrusted (no confiable)** | Baja | Internet | Solo lo necesario, casi nada entra |
| **DMZ (zona desmilitarizada)** | Media | Servidores públicos: web, correo, VPN | Expuesta a Internet, aislada de la interna |

### 4.2 La analogía del banco

Imaginá la entrada de una sucursal del Banco:

1. La **calle** es Internet: cualquiera puede caminar por ella. Nadie la controla. Es **Untrusted**.
2. El **vestíbulo cerrado** (vidrio blindado, puerta con portero) es la **DMZ**: los visitantes entran, hablan con el personal de atención, hacen sus trámites, pero **nunca pasan a las oficinas del fondo**.
3. Las **oficinas y la caja fuerte** son la red interna **Trusted**: solo entran empleados con credencial, tarjeta y permiso.

El error grave sería poner la caja fuerte en el vestíbulo. Eso es lo que pasa cuando una base de datos con datos personales queda "pública" en la DMZ.

### 4.3 Regla de oro de la DMZ

- Un servidor de la DMZ **no tiene acceso directo** a la red interna.
- Si la web pública (en la DMZ) es atacada, el atacante queda **atrapado en el vestíbulo**: no llega a las oficinas.

Para que un servidor de la DMZ hable con uno interno (por ejemplo, para consultar un dato), debe pasar por reglas muy específicas del firewall, con puerto, IP y justificación. Nunca "permiso completo".

---

## 5. ¿Qué es la DMZ y por qué la necesita el Banco?

La **DMZ** (Demilitarized Zone, zona desmilitarizada) es una subred separada donde se ponen los servicios que **deben ser visibles desde Internet**. El Banco necesita DMZ para:

- **Banco En Línea** (el portal web de clientes).
- **Correo electrónico** (servidores de correo público).
- **VPN de acceso** (punto de entrada para que empleados o proveedores se conecten de forma segura).

### 5.1 Qué NUNCA debe ir en la DMZ

- **Bases de datos con datos personales** (clientes, empleados, legajos). Los datos personales no se exponen jamás.
- **Active Directory** (el "directorio telefónico" central de usuarios). Si cae, cae la autenticación de todo el banco.
- **Sistemas core** (el corazón de la operación bancaria).

La web pública puede *consultar* datos, pero la base de datos vive en la red interna, y el acceso se hace por reglas controladas y a través de capas intermedias (servicios de aplicación), no exponiendo la base directamente.

> **Errores comunes de la DMZ:** poner el servidor web y la base en la misma máquina, dar acceso total del servidor DMZ hacia adentro, o dejar servicios administrativos (como el escritorio remoto) expuestos a Internet.

---

## 6. Segmentación de red

### 6.1 ¿Qué es segmentar?

**Segmentar** es partir la red grande en trozos más chicos según función y sensibilidad. Cada trozo se llama **subred** o **VLAN** (Virtual LAN). Como poner puertas internas en el edificio:

- El área de cajas no puede entrar directo a la bóveda.
- Los visitantes no cruzan a las oficinas.
- La cámara de videovigilancia no navega por Internet sin necesidad.

### 6.2 Segmentos típicos del Banco

| Segmento | Función | Sensibilidad |
|---|---|---|
| Core / sistemas centrales | Sistemas críticos bancarios | Muy alta |
| Sucursales | Equipos de atención al público | Media |
| Servicios (DMZ) | Web, correo, VPN | Media |
| Escritorios (usuarios) | Puestos de trabajo | Media |
| WiFi | Red inalámbrica (empleados / visitas separadas) | Baja |
| Impresoras | Dispositivos compartidos | Baja |
| Videovigilancia | Cámaras de seguridad | Media |

La idea: **cada segmento solo puede hablar con lo que necesita**. Una impresora no necesita hablar con el core. Una cámara no necesita salir a Internet. Menos caminos = menos posibilidades de que un atacante se mueva libremente (se dice "contener la lateralidad" o *lateral movement*).

### 6.3 Microsegmentación (mención)

La **microsegmentación** es llevar esto al extremo: reglas para cada aplicación o incluso cada máquina virtual, en vez de por segmento completo. Es un control avanzado (🟡 mención), que hoy muchos proveedores ofrecen por software. Para el kit, alcanza con saber que existe y que reduce todavía más el radio de un incidente.

### 6.4 Políticas por zona

Cada zona tiene su política:

- **Trusted → Trusted:** tráfico interno, permitido con controles de acceso por usuario (enlaza con PR-01).
- **Trusted → DMZ:** permitido para servicios puntuales (web interna, consultas).
- **Untrusted → DMZ:** permitido solo a los servicios públicos (web, correo, VPN), con inspección.
- **Untrusted → Trusted:** denegado por defecto. Solo llega lo que entra por la VPN (autenticada) o por reglas muy puntuales.

---

## 7. Diseño de zonas para el Banco (ejemplo)

| Zona | Contenido | Quién entra | Qué sale |
|---|---|---|---|
| Trusted | Escritorios, servidores internos, Active Directory | Empleados autenticados (dominio), administradores | Hacia DMZ e Internet con proxy, correo, actualizaciones |
| DMZ | Web Banco En Línea, correo, VPN | Público (solo web/correo), conexiones VPN autenticadas | Solo respuestas a las peticiones; nunca hacia el interior sin regla puntual |
| Servidores de datos | Bases de datos, core | Solo aplicaciones autorizadas desde DMZ o Trusted con reglas específicas | Solo lo que la aplicación necesita |

Este diagrama en texto es una **evidencia de diseño** que se guarda con INFRA-03 en el kit.

---

## 8. Reglas del firewall: cómo se escriben bien

### 8.1 Principio de mínimo privilegio

Cada regla debe ser lo más específica posible: una IP origen, una IP destino, un servicio, una justificación. Nada de "permitir todo de todos a todos".

### 8.2 Orden de las reglas (first-match)

El firewall aplica la primera regla que coincide. Por eso:

- Las reglas **más específicas** van arriba.
- Las reglas de **denegar** suelen ir antes que los "permitir amplios".
- Al final, una regla implícita de **denegar todo**.

### 8.3 Reglas de entrada (ingress) y salida (egress)

- **Ingress:** tráfico que entra a la red (desde Internet hacia la DMZ o la interna).
- **Egress:** tráfico que sale (desde la interna hacia Internet). Controlar la salida evita que malware "llame a casa" y que empleados usen servicios no autorizados.

### 8.4 Logging y revisión

- Activar **logging** (registro) de las reglas importantes: quién, de dónde, hacia dónde, cuándo, y si se permitió o denegó.
- **Revisión periódica:** las reglas viejas o sin uso se eliminan. Una regla que ya no se justifica es un agujero.

### 8.5 Ejemplo de registro de reglas

| # | Regla | Zona origen | Destino | Puerto | Acción | Justificación | Revisión |
|---|---|---|---|---|---|---|---|
| 10 | Empleados → web pública | Trusted | DMZ (web) | 443 | Permitir | Navegación web segura | 2026-01-15 |
| 20 | Público → web Banco | Untrusted | DMZ (web) | 443 | Permitir | Portal Banco En Línea | 2026-01-15 |
| 30 | DMZ → base de datos | DMZ (web) | Servidores datos | 3306 | Denegar | Las bases nunca se exponen | 2026-01-15 |
| 40 | Todos → todos | Cualquiera | Cualquiera | Cualquiera | Denegar | Regla por defecto | 2026-01-15 |

---

## 9. Alta disponibilidad y failover

Un firewall es un punto crítico: si se cae, todo se detiene. Por eso se instala en **alta disponibilidad (HA)**:

- **Activo/pasivo:** dos firewalls. Uno trabaja (activo), el otro vigila en espera (pasivo). Si el activo falla, el pasivo asume en segundos. Eso se llama **failover**.
- Ventajas: el banco no se queda sin red por falla del guardia; las reglas se sincronizan automáticamente entre ambos.

> **Evidencia:** registrar que existe HA y probar el failover periódicamente es parte de PR-06 (gestión de cambios) y DE-01 (monitoreo).

---

## 10. Errores comunes

1. **Regla any-any:** una regla que dice "permitir desde cualquier IP a cualquier IP, todos los puertos". Es la regla más peligrosa que existe: es como abrir todas las puertas del banco.
2. **Puertos administrativos expuestos a Internet:** dejar el escritorio remoto (RDP), SSH o la consola del firewall abiertos al mundo.
3. **DMZ mal aislada:** el servidor DMZ con acceso libre a la red interna, o la base de datos dentro de la DMZ.
4. **Firewall sin parches:** dispositivo viejo sin actualizar, con vulnerabilidades conocidas.
5. **Logs desactivados:** sin registros no hay evidencia, no se detecta un ataque y no se puede demostrar URCDP-01.
6. **No revisar las reglas:** reglas acumuladas por años, sin justificación y sin dueño.

---

## 11. Relación con el kit y evidencias

La segmentación y las reglas alimentan varios entregables:

| Documento | Cómo aporta INFRA-03 |
|---|---|
| **ID-01 (inventario)** | Los segmentos y zonas son unidades del inventario de activos |
| **ID-02 / ID-03 (riesgos)** | Las brechas entre zonas (o su ausencia) son riesgos |
| **PR-01 (acceso)** | Las reglas del firewall refuerzan el control de acceso |
| **PR-03 (datos)** | La segmentación protege las bases de datos personales |
| **DE-01 (logs)** | Los logs del firewall son fuente de monitoreo |
| **URCDP-01** | El firewall y sus reglas son **medida de seguridad técnica** |
| **BCU-01 / BCU-03** | Medida de control de red y protección de datos |

**Evidencias que se archivan con INFRA-03:**

- Diagrama de zonas y segmentación.
- Lista de reglas del firewall con justificación y revisión (tabla del punto 8.5).
- Registro de alta disponibilidad y prueba de failover.
- Informe de revisión periódica de reglas (fecha, quién revisó, qué cambió).

> **Tip de evidencias:** nunca archiven reglas con contraseñas ni IPs internas si el documento va a salir del banco. Para el kit, usar IPs de ejemplo (10.x.x.x) y marcar el documento "Uso interno".

---

## 12. Actividades de práctica

**Checklist (marcá con ☑ cuando lo tengas):**

- ☐ Dibujé el mapa de zonas del Banco (Trusted, DMZ, Untrusted) en un diagrama.
- ☐ Listé qué servicios públicos van en la DMZ y cuáles jamás.
- ☐ Redacté una tabla de reglas de ejemplo con justificación.
- ☐ Identifiqué en qué segmento vive cada activo del ID-01.
- ☐ Verifiqué que no exista ninguna regla "any-any" en los ejemplos.
- ☐ Guardé el diagrama y la tabla de reglas como evidencia del kit.

---

**Documentos relacionados:** GV-01, GV-03, ID-01, ID-02, ID-03, PR-01, PR-03, DE-01, DE-02, BCU-01, BCU-03, URCDP-01, MATRIZ-001.
