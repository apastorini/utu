# Plan de Estudio: Ciberseguridad y Respuesta a Incidentes para el BHU

**Duracion total:** 36 horas (12 semanas x 3 horas/semana)
**Distribucion:** 1.5 horas teoria + 1.5 horas practica por semana
**Plataforma de laboratorio:** Tectonic Cyber Range
**Clase recomendada:** 8-12 estudiantes

---

## Informacion General

### Equipamiento Requerido por Estudiante

| Elemento | Especificacion minima |
|---|---|
| Computadora personal | 8 GB RAM, 50 GB de espacio libre, navegador actualizado |
| Conectividad | Internet estable (minimo 10 Mbps) |
| Acceso a Tectonic | Credenciales individuales proporcionadas por el instructor |
| Herramientas locales | Nmap (preinstalado o via Kali en VM), Wireshark, navegador con consola de desarrollo |
| Software adicional | VirtualBox o VMware Workstation Player (para escenarios locales complementarios) |

### Materiales Necesarios

- Acceso a la plataforma Tectonic con todos los escenarios preconfigurados
- Cuaderno o documento digital para toma de notas y bitacora de laboratorio
- Acceso a documentacion oficial (OWASP, MITRE ATT&CK, NIST SP 800-61)
- Presentaciones de diapositivas por semana (preparadas por el instructor)
- Guiones de laboratorio paso a paso para cada escenario de Tectonic
- Formato de reporte de incidente (proporcionado por el instructor)

### Criterios de Evaluacion

| Componente | Peso | Descripcion |
|---|---|---|
| Evaluaciones practicas semanales | 40% | Ejercicios en Tectonic, bitacoras de laboratorio, ejercicios de hands-on |
| Evaluacion teorica | 30% | Quizzes semanales, cuestionarios de conceptos, participacion en clase |
| Evaluacion final (Semana 12) | 30% | Simulacro multi-ataque con informe de respuesta a incidentes |

**Nota de aprobacion minima:** 70/100

---

## Semana 1: Fundamentos de Redes y Seguridad

**Duracion:** 3 horas (1.5h teoria + 1.5h practica)

### Temas de Teoria

- Modelo OSI: capas, funciones de cada capa, encapsulamiento y desencapsulamiento
- Suite TCP/IP: correspondencia con el modelo OSI, direcccionamiento IP (IPv4/IPv6), subredes
- Protocolos fundamentales: TCP, UDP, HTTP/HTTPS, DNS, DHCP, ARP, ICMP
- Conceptos basicos de seguridad: CIA (Confidencialidad, Integridad, Disponibilidad), triada de la seguridad
- Introduccion al concepto de amenaza, vulnerabilidad y riesgo
- Panorama de ciberamenazas en el sector financiero uruguayo

### Ejercicio Practico

- **Escenario:** Laboratorio introductorio de Tectonic - Exploracion de red basica
- **Actividad:** Los estudiantes acceden al cyber range Tectonic, exploran la interfaz, ejecutan comandos basicos de red (`ipconfig`, `ping`, `tracert`, `nslookup`) dentro de una maquina virtual asignada. Identifican la topologia de la red local y documentan hallazgos.

### Objetivos de Aprendizaje

1. Explicar cada capa del modelo OSI y su funcion en la comunicacion de datos
2. Diferenciar entre TCP y UDP, y describir el proceso de conexion TCP handshake
3. Configurar e interpretar direcciones IP, mascaras de subred y rutas
4. Identificar los tres componentes de la triada CIA en un contexto bancario
5. Navegar la interfaz de Tectonic y ejecutar comandos basicos de reconocimiento de red

### Evaluacion y Tarea

- Quiz teorico de 15 preguntas sobre modelo OSI y protocolos
- Completar la bitacora de laboratorio con capturas de cada comando ejecutado
- Tarea: investigar y presentar un incidente de ciberseguridad reciente en una entidad financiera (1 pagina)

---

## Semana 2: Infraestructura Bancaria Virtual - Escenario "Banco del Sol"

**Duracion:** 3 horas (1.5h teoria + 1.5h practica)

### Temas de Teoria

- Arquitectura tipica de una entidad bancaria: red perimetral, DMZ, red interna, segmentos de datos
- Componentes de infraestructura: firewalls, servidores web, bases de datos, controladores de dominio, estaciones de trabajo
- Descripcion completa del escenario "Banco del Sol": topologia, activos, servicios desplegados en Tectonic
- Conceptos de segmentacion de red y zonas de seguridad
- Modelos de defensa en profundidad (defense in depth)

### Ejercicio Practico

- **Escenario:** Despliegue e inventariado del escenario "Banco del Sol" en Tectonic
- **Actividad:** Los estudiantes despliegan el escenario completo de Banco del Sol en Tectonic. Realizan un inventariado de activos: identifican todas las maquinas, servicios corriendo en cada una, puertos abiertos y roles asignados. Documentan la topologia de red en un diagrama.

### Objetivos de Aprendizaje

1. Describir la arquitectura de red tipica de un banco y justificar cada segmento
2. Desplegar un escenario completo en la plataforma Tectonic
3. Realizar un inventariado de activos de red de forma sistematica
4. Elaborar un diagrama de topologia que represente la infraestructura virtual
5. Identificar los activos criticos dentro del escenario Bancos del Sol

### Evaluacion y Tarea

- Entregar el diagrama de topologia documentado con IPs, hostnames y servicios
- Quiz practico: identificar 10 activos en el escenario y clasificarlos por criticidad
- Tarea: leer la guia de Nmap (capitulos 1-3) para preparar la Semana 3

---

## Semana 3: Herramientas de Reconocimiento

**Duracion:** 3 horas (1.5h teoria + 1.5h practica)

### Temas de Teoria

- Fases del reconocimiento: activo vs. pasivo
- OSINT (Open Source Intelligence): fuentes publicas, Google dorking, Shodan, Censys
- Herramientas de reconocimiento de red: Nmap (scans SYN, TCP, UDP, version detection, OS fingerprinting)
- Enumeracion DNS: registros A, AAAA, MX, NS, TXT, subdomain enumeration
- Whois y lookup de dominios
- Reconocimiento de servicios web: tecnologias utilizadas, headers HTTP, frameworks

### Ejercicio Practico

- **Escenario:** Reconocimiento completo sobre el escenario "Banco del Sol" en Tectonic
- **Actividad:** Los estudiantes ejecutan escaneos Nmap contra la red del escenario (con autorizacion del instructor). Realizan enumeracion DNS, busqueda Whois, y recopilan informacion OSINT sobre los activos del banco virtual. Documentan todos los hallazgos en un informe de reconocimiento.

### Objetivos de Aprendizaje

1. Ejecutar escaneos Nmap con diferentes tipos de sondas y interpretar los resultados
2. Realizar enumeracion DNS para descubrir subdominios y servicios
3. Utilizar fuentes OSINT para recopilar informacion sobre un objetivo
4. Clasificar y priorizar hallazgos de reconocimiento por nivel de criticidad
5. Redactar un informe de reconocimiento estructurado

### Evaluacion y Tarea

- Entregar informe de reconocimiento del escenario con todos los hallazgos documentados
- Ejercicio practico: encontrar al menos 5 servicios ocultos o no evidentes mediante escaneo avanzado
- Tarea: estudiar los conceptos de phishing y reverse shell para la Semana 4

---

## Semana 4: Escenario 01 - Ataque de Phishing

**Duracion:** 3 horas (1.5h teoria + 1.5h practica)

### Temas de Teoria

- Ingenieria social: tecnicas psicologicas, pretexto, urgencia, autoridad
- Phishing: definicion, variantes (spear phishing, whaling, vishing, smishing)
- Construccion de campanas de phishing: dominios spoofeados, plantillas de correo, Payloads
- Reverse shell: concepto, tipos (bash, python, meterpreter), establecimiento de sesion
- Cifrado de payloads para evadir deteccion basica
- Marco legal: implicaciones del phishing autorizado en entornos controlados

### Ejercicio Practico

- **Escenario 01:** Ataque de phishing completo en "Banco del Sol"
- **Actividad:** Los estudiantes planifican y ejecutan un ataque de phishing simulado contra usuarios del banco virtual. Configuran un servidor de captura, crean un correo de phishing, obtienen una reverse shell cuando la victima interactua. El ataque se realiza exclusivamente dentro del entorno aislado de Tectonic.

### Objetivos de Aprendizaje

1. Explicar las tecnicas psicologicas utilizadas en ataques de phishing
2. Configurar un servidor de phishing funcional dentro de un entorno controlado
3. Generar un payload de reverse shell y establecer una conexion remota
4. Demostrar el impacto de un ataque de phishing en una entidad bancaria
5. Operar dentro de los limites eticos y legales de un entorno de laboratorio

### Evaluacion y Tarea

- Demostracion en vivo del ataque de phishing completado
- Bitacora de laboratorio paso a paso con capturas de cada fase del ataque
- Reflexion escrita: que indicadores podrian haber detectado este ataque (1 pagina)

---

## Semana 5: Defensa Contra Phishing - Deteccion y Respuesta

**Duracion:** 3 horas (1.5h teoria + 1.5h practica)

### Temas de Teoria

- Indicadores de compromiso (IOC): IOCs de red, host, correo electronico
- Analisis de logs: logs de correo, logs de proxy, logs de firewall, logs de endpoints
- Herramientas de deteccion: Wazuh, Snort/Suricata, filtrado de correo
- Procedimiento de respuesta a incidentes: NIST SP 800-61 (Preparacion, Deteccion, Contencion, Erradicacion, Recuperacion, Lecciones aprendidas)
- Creacion de reglas de deteccion basadas en el ataque de la Semana 4
- Hardening de correo electronico: SPF, DKIM, DMARC

### Ejercicio Practico

- **Escenario 01 (defensa):** Analisis y respuesta al ataque de phishing
- **Actividad:** Los estudiantes revisan los logs generados durante el ataque de la Semana 4. Identifican IOCs, correlacionan eventos en multiples fuentes de logs, crean reglas de deteccion y documentan el procedimiento de respuesta a incidentes completo para el escenario de phishing.

### Objetivos de Aprendizaje

1. Identificar y clasificar indicadores de compromiso en logs de diferentes fuentes
2. Correlacionar eventos de seguridad para reconstruir la linea de tiempo de un ataque
3. Crear reglas basicas de deteccion en herramientas de seguridad
4. Aplicar el marco NIST SP 800-61 a un incidente de phishing real
5. Redactar un informe de respuesta a incidentes completo

### Evaluacion y Tarea

- Entregar informe de respuesta al incidente de phishing (formato NIST)
- Quiz sobre IOCs y procedimientos de deteccion
- Tarea: investigar tipos de malware y ransomware para la Semana 6

---

## Semana 6: Malware y Ransomware

**Duracion:** 3 horas (1.5h teoria + 1.5h practica)

### Temas de Teoria

- Taxonomia de malware: virus, gusanos, troyanos, RATs, spyware, adware
- Ransomware: evolucion, grupos notorios (LockBit, Conti, BlackCat), modelos RaaS
- Tecnicas de cifrado: simetrico vs. asimetrico, como funciona el cifrado de ransomware
- Analisis de malware: analisis estatico (firmas, strings, hashes) vs. dinamico (sandbox, comportamiento)
- Indicators of Compromise de malware en endpoints y red
- Proteccion de backups y estrategias anti-ransomware

### Ejercicio Practico

- **Escenario 02:** Infeccion y analisis de malware/ransomware en "Banco del Sol"
- **Actividad:** Los estudiantes son expuestos a una muestra de ransomware controlada dentro del entorno Tectonic. Observan el comportamiento de cifrado en archivos del sistema de archivos del banco. Realizan analisis estatico de la muestra (hashes, strings, imports) y analisis dinamico (observacion de comportamiento en sandbox). Identifican los archivos cifrados y los IOCs generados.

### Objetivos de Aprendizaje

1. Clasificar los diferentes tipos de malware y describir sus vectores de propagacion
2. Explicar el mecanismo de cifrado utilizado por el ransomware
3. Ejecutar analisis estatico basico de una muestra de malware
4. Observar y documentar el comportamiento de ransomware en un entorno controlado
5. Identificar IOCs de malware en registros del sistema y de red

### Evaluacion y Tarea

- Informe de analisis de malware: hashes, strings relevantes, comportamiento observado, IOCs
- Ejercicio: proponer un plan de proteccion contra ransomware para el "Banco del Sol"
- Tarea: estudiar tecnicas de ataque DDoS para la Semana 7

---

## Semana 7: DDoS y Ataques a Disponibilidad

**Duracion:** 3 horas (1.5h teoria + 1.5h practica)

### Temas de Teoria

- Ataques a la disponibilidad: concepto y impacto en el sector financiero
- DDoS (Distributed Denial of Service): arquitectura de botnets, protocolos de command and control
- Tipos de ataque DDoS de capa 3/4: SYN flood, UDP flood, ICMP flood
- Tipos de ataque DDoS de capa 7: HTTP flood, Slowloris, amplificacion DNS/NTP
- Tecnicas de mitigacion: rate limiting, blacklist/whitelist, WAF, CDNs, scrubbing centers
- Analisis de trafico DDoS: firmas de ataque, deteccion con Snort/Suricata

### Ejercicio Practico

- **Escenario 03:** Ataque DDoS y mitigacion en servicios del "Banco del Sol"
- **Actividad:** Los estudiantes ejecutan un ataque SYN flood controlado contra el servidor web del banco virtual. Miden el impacto en disponibilidad (tiempo de respuesta, caida del servicio). Luego implementan reglas de mitigacion en el firewall y/o WAF, y verifican la efectividad de las defensas. Compara metricas antes y despues de la mitigacion.

### Objetivos de Aprendizaje

1. Explicar la diferencia entre ataques DDoS de volumen, protocolo y aplicacion
2. Ejecutar un ataque SYN flood controlado y medir su impacto
3. Analizar trafico de red para identificar firmas de ataque DDoS
4. Implementar reglas de mitigacion en firewalls y WAFs
5. Documentar un proceso de respuesta ante un ataque DDoS

### Evaluacion y Tarea

- Informe con metricas de impacto y mitigacion (antes/despues)
- Ejercicio: configurar al menos 3 reglas de mitigacion diferentes y probar su efectividad
- Tarea: revisar OWASP Top 10 para preparar la Semana 8

---

## Semana 8: Ataques a Aplicaciones Web

**Duracion:** 3 horas (1.5h teoria + 1.5h practica)

### Temas de Teoria

- OWASP Top 10 (edicion mas reciente): descripcion de cada vulnerabilidad
- SQL Injection: tipos (basic, blind, union-based, time-based), impacto, prevencion
- Cross-Site Scripting (XSS): reflejado, almacenado, DOM-based
- Directory Traversal / Path Traversal: tecnicas y consecuencias
- Broken Authentication y Session Management
- Intro a herramientas: Burp Suite, SQLMap, Dirb/Gobuster
- Secure coding practices y validacion de input

### Ejercicio Practico

- **Escenario 04:** Ataques a la aplicacion web del "Banco del Sol"
- **Actividad:** Los estudiantes identifican y explotan vulnerabilidades en la aplicacion web bancaria del escenario. Ejecutan SQL Injection para extraer datos de la base de datos, inyectan XSS en formularios, realizan directory traversal para acceder a archivos del servidor. Utilizan Burp Suite para interceptar y modificar peticiones HTTP.

### Objetivos de Aprendizaje

1. Identificar las vulnerabilidades del OWASP Top 10 en una aplicacion real
2. Ejecutar un ataque de SQL Injection manual y con herramientas automatizadas
3. Demostrar el impacto de XSS reflejado y almacenado
4. Utilizar Burp Suite para el analisis de trafico web
5. Proponer soluciones de codigo seguro para cada vulnerabilidad encontrada

### Evaluacion y Tarea

- Informe de pruebas de penetracion web: cada vulnerabilidad, paso a paso, evidencia y remediacion
- Quiz sobre OWASP Top 10 y tecnicas de inyeccion
- Tarea: estudiar tecnicas de movimiento lateral para la Semana 9

---

## Semana 9: Movimiento Lateral y Escalada de Privilegios

**Duracion:** 3 horas (1.5h teoria + 1.5h practica)

### Temas de Teoria

- Movimiento lateral (Lateral Movement): tecnicas en el MITRE ATT&CK (T1021, T1550, T1570)
- Pivot: concepto, encapsulamiento de trafico, port forwarding
- Pass-the-Hash / Pass-the-Ticket: captura y reutilizacion de credenciales
- Escalada de privilegios: explotacion de configuraciones, kernel exploits, UAC bypass
- Herramientas: Mimikatz, CrackMapExec, Evil-WinRM, Chisel, ligolo-ng
- Kerberoasting y ataque AS-REP en entornos Active Directory
- Detectores y monitoreo: logs de Windows Event, Sysmon, Wazuh

### Ejercicio Practico

- **Escenario 04 (continuacion):** Movimiento lateral dentro de la red del "Banco del Sol"
- **Actividad:** Partiendo de una sesion comprometida (obtenida en la Semana 8), los estudiantes escalan privilegios en la maquina inicial, extraen credenciales, y se desplazan lateralmente hacia otros hosts de la red interna. Establecen pivotes para alcanzar segmentos no accesibles directamente. Documentan cada salto y cada credencial obtenida.

### Objetivos de Aprendizaje

1. Explicar las tecnicas de movimiento lateral mas comunes en entornos corporativos
2. Extraer credenciales de una maquina comprometida
3. Establecer un pivot para acceder a otros segmentos de red
4. Escalar privilegios en un sistema Windows utilizando tecnicas conocidas
5. Detectar actividades de movimiento lateral en logs de Windows Event y Sysmon

### Evaluacion y Tarea

- Diagrama de movimiento lateral: cada paso, cada host, cada credencial utilizada
- Ejercicio: crear reglas de deteccion para las tecnicas utilizadas
- Tarea: estudiar tecnicas de exfiltracion de datos para la Semana 10

---

## Semana 10: Exfiltracion de Datos y Command and Control

**Duracion:** 3 horas (1.5h teoria + 1.5h practica)

### Temas de Teoria

- Exfiltracion de datos: concepto, motivacion, tecnicas comunes
- DNS Tunneling: como funciona, herramientas (dnscat2, iodine), deteccion
- Exfiltracion via HTTPS/HTTPS: canales covertos, cifrado para evadir DLP
- Command and Control (C2): arquitectura, canales de comunicacion, frameworks (Cobalt Strike, Sliver, Havoc)
- Evasion de deteccion: ofuscacion, comunicacion legitimizada, living-off-the-land
- Defensa: monitoreo DNS, inspeccion de trafico TLS, analisis de comportamiento de red
- DLP (Data Loss Prevention): politicas, herramientas, dificultades de implementacion

### Ejercicio Practico

- **Escenario 05:** Exfiltracion de datos criticos del "Banco del Sol"
- **Actividad:** Los estudiantes configuran un canal de exfiltracion mediante DNS tunneling para extraer datos de la base de datos del banco hacia un servidor externo controlado. Tambien establecen un canal C2 para mantener acceso persistente. Implementan monitoreo DNS y de red para detectar estas actividades. Comparan trafico normal vs. trafico de exfiltracion.

### Objetivos de Aprendizaje

1. Explicar los principales vectores de exfiltracion de datos
2. Configurar un canal de exfiltracion mediante DNS tunneling
3. Establecer una sesion de Command and Control persistente
4. Identificar patrones de trafico que indican exfiltracion
5. Proponer politicas y controles DLP para prevenir la fuga de datos financieros

### Evaluacion y Tarea

- Informe de exfiltracion: metodo utilizado, volumen de datos extraidos, IOC generados
- Ejercicio: crear reglas DNS para detectar tunneling y comparar trafico normal vs. malicioso
- Tarea: preparar material para el analisis forense de la Semana 11

---

## Semana 11: Analisis Forense Digital

**Duracion:** 3 hours (1.5h teoria + 1.5h practica)

### Temas de Teoria

- Investigacion forense digital: principios, marco legal, cadena de custodia
- Adquisicion de evidencia: adquisicion en vivo vs. mortuoria, formatos (E01, RAW)
- Analisis de memoria: Volatility Framework, identificacion de procesos, inyeccion de codigo, conexiones de red
- Analisis de disco: recuperacion de archivos eliminados, analisis de registros, timeline analysis
- Herramientas forenses: Volatility, Autopsy, FTK Imager, Sleuth Kit
- Preservacion de evidencia: hashing, documentacion, transporte seguro
- Reporte forense: estructura, formato, presentacion de hallazgos

### Ejercicio Practico

- **Escenario 06:** Investigacion forense post-incidente en "Banco del Sol"
- **Actividad:** Los estudiantes reciben dumps de memoria y disco generados durante los ataques de las semanas anteriores. Utilizan Volatility para analizar la memoria: identifican procesos maliciosos, conexiones de red activas, archivos inyectados, y reconstruyen la linea de tiempo del ataque. Extraen evidencia clave y la documentan siguiendo la cadena de custodia.

### Objetivos de Aprendizaje

1. Aplicar los principios de investigacion forense digital y la cadena de custodia
2. Ejecutar analisis de memoria con Volatility para identificar actividad maliciosa
3. Reconstruir una linea de tiempo de ataque a partir de evidencia digital
4. Extraer y preservar evidencia de forma forensicamente valida
5. Redactar un informe forense que pueda utilizarse como evidencia

### Evaluacion y Tarea

- Informe forense completo: hallazgos, evidencia, hashes, linea de tiempo, conclusiones
- Ejercicio: identificar al menos 3 artefactos forenses criticos en el dump de memoria
- Tarea: prepararse para el simulacro final de la Semana 12 (estudiar todos los escenarios)

---

## Semana 12: Simulacro Final y Evaluacion

**Duracion:** 3 horas (1.5h teoria/review + 1.5h practica evaluativa)

### Temas de Teoria

- Revision integral de los 11 temas anteriores (session rapida de repaso, 45 minutos)
- Metodologia de respuesta a incidentes: repaso del ciclo completo NIST
- Consideraciones eticas y legales de la ciberseguridad en Uruguay
- Proximos pasos: certificaciones recomendadas (CompTIA Security+, CEH, OSCP), comunidad de ciberseguridad, recursos de aprendizaje continuo
- Retroalimentacion grupal sobre el curso

### Ejercicio Practico - Evaluacion Final

- **Escenario:** Simulacro combinado multi-ataque en "Banco del Sol"
- **Actividad:** Los estudiantes enfrentan un escenario integrado que combina multiples tecnicas vistas durante el curso. El escenario incluye: phishing inicial que conduce a compromiso de endpoint, movimiento lateral, escalada de privilegios, exfiltracion de datos, y evidencia forense residual. Los estudiantes deben:
  1. Detectar y analizar el ataque (reconocimiento forense)
  2. Contener el incidente (aislar sistemas comprometidos)
  3. Erradicar la amenaza (eliminacion de persistencia)
  4. Recuperar los sistemas
  5. Redactar un informe completo de respuesta a incidentes

### Objetivos de Aprendizaje

1. Integrar multiples tecnicas de ataque y defensa en un escenario realista
2. Aplicar el marco NIST de respuesta a incidentes de forma completa
3. Demostrar competencia en todas las areas cubiertas durante el curso
4. Redactar un informe profesional de respuesta a incidentes
5. Evaluar criticamente las propias capacidades y areas de mejora

### Evaluacion

- **Simulacro practico (20%):** Evaluacion en vivo del desempeño en el escenario
- **Informe de respuesta a incidentes (10%):** Documento escrito que incluye:
  - Resumen ejecutivo
  - Linea de tiempo del incidente
  - Indicadores de compromiso identificados
  - Acciones de contencion, erradicacion y recuperacion
  - Recomendaciones de mejora
  - Evidencia forense adjunta

---

## Resumen del Curso

| Semana | Tema Principal | Escenario Tectonic | Horas |
|---|---|---|---|
| 1 | Fundamentos de Redes y Seguridad | Lab introductorio | 3 |
| 2 | Infraestructura Bancaria Virtual | Banco del Sol (despliegue) | 3 |
| 3 | Herramientas de Reconocimiento | Banco del Sol (reconocimiento) | 3 |
| 4 | Escenario 01: Phishing | Phishing + reverse shell | 3 |
| 5 | Defensa Contra Phishing | Respuesta al phishing | 3 |
| 6 | Malware y Ransomware | Escenario 02 | 3 |
| 7 | DDoS y Ataques a Disponibilidad | Escenario 03 | 3 |
| 8 | Ataques a Aplicaciones Web | Escenario 04 (web) | 3 |
| 9 | Movimiento Lateral y Escalada | Escenario 04 (lateral) | 3 |
| 10 | Exfiltracion y C2 | Escenario 05 | 3 |
| 11 | Analisis Forense Digital | Escenario 06 | 3 |
| 12 | Simulacro Final y Evaluacion | Escenario combinado | 3 |
| | **TOTAL** | | **36** |

### Notas Finales

- Todos los escenarios de Tectonic se ejecutan en entornos aislados. Ningun ataque se realiza contra sistemas reales.
- Los estudiantes deben firmar un acuerdo de uso etico antes de iniciar el curso.
- El instructor tiene acceso total a los registros de actividad de cada estudiante en la plataforma Tectonic.
- Se recomienda que los escenarios se reinicien entre semanas para garantizar un punto de partida limpio.
- Los informes deben entregarse en formato digital (PDF o Markdown) con la estructura proporcionada por el instructor.
