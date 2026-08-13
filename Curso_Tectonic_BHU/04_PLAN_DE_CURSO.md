# Plan de Curso: Capacitación en Ciberseguridad con Tectonic

## Información General

- **Nombre del curso:** Capacitación en Ciberseguridad Práctica con Laboratorios Tectonic
- **Dirigido a:** Personal técnico de BHU
- **Duración:** 12 semanas — 3 horas por semana — 36 horas totales
- **Modalidad:** Teoría + Práctica con laboratorios simulados
- **Prerrequisitos:** Conocimientos básicos de redes (TCP/IP) y sistemas Linux
- **Herramienta principal:** Plataforma Tectonic (lab_edition)

---

## Semana 1: Introducción a Ciberseguridad y Tectonic

### Objetivos de Aprendizaje

1. Comprender los fundamentos de ciberseguridad y el panorama de amenazas actual
2. Familiarizarse con la plataforma Tectonic y su ciclo de vida
3. Configurar el entorno de laboratorio y verificar el correcto funcionamiento
4. Identificar los roles y responsabilidades en un equipo de seguridad

### Contenido Teórico (30 min)

- Definiciones clave: CIA triad, amenazas, vulnerabilidades, exploits, riesgo
- Panorama actual de ciberataques contra el sector financiero
- Marcos de referencia: NIST CSF, MITRE ATT&CK
- Introducción a la plataforma Tectonic y su arquitectura

### Ejercicio Práctico con Tectonic (2 horas)

- Instalación y configuración de Tectonic en la estación de trabajo
- Ejecución de `create-images` para generar las imágenes base del laboratorio
- Despliegue del laboratorio de prueba con `deploy`
- Exploración de los accesos de estudiante y profesor
- Verificación de conectividad entre máquinas virtuales
- Práctica de comandos `list`, `stop`, `start`, `destroy`

### Discusión y Reporte (30 min)

- ¿Por qué es importante la ciberseguridad en una entidad bancaria?
- ¿Qué escenarios de amenaza son más relevantes para BHU?
- Reflexión sobre la importancia de los laboratorios de práctica

### Entregable

- Documento de instalación con capturas de pantalla y registro del proceso

---

## Semana 2: Arquitectura de Red Bancaria

### Objetivos de Aprendizaje

1. Comprender la arquitectura típica de una red bancaria
2. Identificar segmentos de red críticos (DMZ, Core Banking, Back Office)
3. Desplegar y explorar la infraestructura base "Banco del Sol"
4. Mapear la topología de red del laboratorio

### Contenido Teórico (30 min)

- Segmentación de red en entornos bancarios
- DMZ, zonas internas, zonas de administración
- Principios de defense in depth
- Modelo de amenazas bancarias (SWIFT, PCI-DSS)

### Ejercicio Práctico con Tectonic (2 horas)

- Despliegue de la infraestructura base "Banco del Sol"
- Uso de `teacher-access` para obtener credenciales y URLs
- Navegación por las diferentes máquinas virtuales
- Uso de `nmap` para descubrir hosts y servicios activos
- Mapeo de la topología de red con diagrama
- Prueba de conectividad entre segmentos

### Discusión y Reporte (30 min)

- Análisis de la topología descubierta
- ¿Cuáles son los puntos más expuestos?
- Identificación de superficies de ataque

### Entregable

- Diagrama de topología de red del laboratorio con anotaciones

---

## Semana 3: Defensa de Correo Electrónico — Escenario 01 Phishing

### Objetivos de Aprendizaje

1. Reconocer los diferentes tipos de phishing (spear, whaling, clone)
2. Implementar reglas de defensa contra phishing en correo electrónico
3. Analizar cabeceras de correo electrónico en busca de indicadores de compromiso
4. Configurar respuestas automáticas ante intentos de phishing

### Contenido Teórico (30 min)

- Técnicas de phishing utilizadas en el sector financiero
- Análisis de cabeceras de correo (SPF, DKIM, DMARC)
- Indicadores de compromiso en emails maliciosos
- Buenas prácticas de defensa de correo

### Ejercicio Práctico con Tectonic (2 horas)

- Despliegue del escenario `01_phishing`
- Identificación de emails de phishing en la bandeja de entrada
- Análisis de cabeceros de correo con `grep` y `strings`
- Uso de `tshark` para analizar tráfico de descarga de adjuntos maliciosos
- Configuración de reglas de `iptables` para bloquear dominios de phishing
- Reporte de los hallazgos encontrados

### Discusión y Reporte (30 min)

- ¿Cómo se habría detectado este phishing en producción?
- ¿Qué indicadores debimos buscar primero?
- Lecciones aprendidas

### Entregable

- Informe de análisis de phishing con cabeceras y hallazgos

---

## Semana 4: Análisis de Phishing — Deep Dive en Forensics de Correo

### Objetivos de Aprendizaje

1. Realizar análisis forense completo de un correo electrónico malicioso
2. Extraer y analizar payloads adjuntos (macros, scripts, binarios)
3. Correlacionar indicadores de compromiso (IOCs) con amenazas conocidas
4. Generar reportes de IOC estructurados

### Contenido Teórico (30 min)

- Análisis forense de correo electrónico
- Técnicas de evasión en adjuntos de phishing
- Formatos de IOCs (IPs, dominios, hashes, URLs)
- Integración con bases de datos de amenazas

### Ejercicio Práctico con Tectonic (2 horas)

- Continuación del escenario `01_phishing`
- Extracción de adjuntos sospechosos con `foremost`
- Análisis de scripts y binarios con `strings`, `file`, `md5sum`
- Análisis de tráfico de red generado por los adjuntos con `tshark`
- Creación de lista de IOCs (hashes, IPs, dominios)
- Uso de `grep` y `find` para buscar evidencia adicional en el sistema

### Discusión y Reporte (30 min)

- Revisión de IOCs encontrados
- ¿Cómo integrar estos hallazgos en un sistema de defensa?
- Discusión sobre automatización de detección

### Entregable

- Reporte de IOCs en formato estándar (CSV/JSON)

---

## Semana 5: Ransomware — Detección y Respuesta

### Objetivos de Aprendizaje

1. Identificar indicadores de un ataque de ransomware en tiempo real
2. Ejecutar procedimientos de contención ante ransomware
3. Analizar el comportamiento del ransomware en el sistema
4. Implementar reglas de firewall para limitar la propagación

### Contenido Teórico (30 min)

- Tipología de ransomware (encryptors, double extortion, wipers)
- Cadena de ataque del ransomware (infección → propagación → cifrado → extortion)
- MITRE ATT&CK: técnicas de ransomware (T1486, T1490)
- Estrategias de contención y erradicación

### Ejercicio Práctico con Tectonic (2 horas)

- Despliegue del escenario `02_ransomware`
- Detección de la infección inicial con `ps`, `top`, `ss`
- Análisis de procesos maliciosos con `ps aux` y `lsof`
- Identificación de conexiones de red del ransomware con `ss -tunapl`
- Bloqueo de C2 con `iptables`
- Análisis de archivos cifrados con `find` y `file`
- Extracción de muestra del ransomware con `dd` y `strings`
- Generar hashes de evidencia con `sha256sum`

### Discusión y Reporte (30 min)

- ¿Cuándo se detectó el ransomware y cómo?
- ¿Qué acciones de contención fueron efectivas?
- ¿Qué mejoraríamos en la respuesta?

### Entregable

- Timeline del ataque con acciones tomadas y justificación

---

## Semana 6: Recuperación Post-Ransomware

### Objetivos de Aprendizaje

1. Ejecutar procedimientos de restauración desde backups
2. Implementar planes de continuidad de negocio (BCP/DRP)
3. Verificar la integridad de sistemas restaurados
4. Realizar limpieza y sanitización completa del entorno

### Contenido Teórico (30 min)

- Planes de Continuidad del Negocio y Recuperación ante Desastres
- Estrategias de backup: 3-2-1 rule
- Verificación de integridad post-restauración
- Hardening de sistemas tras un incidente

### Ejercicio Práctico con Tectonic (2 horas)

- Identificación de archivos cifrados y sistemas afectados
- Localización de backups con `find`
- Verificación de integridad de backups con `md5sum`/`sha256sum`
- Restauración de archivos críticos
- Limpieza de malware residual con `find`, `grep`, `lsof`
- Verificación de servicios restaurados
- Actualización de reglas de firewall para prevenir re-infección

### Discusión y Reporte (30 min)

- Evaluación del tiempo de recuperación
- ¿Los backups fueron suficientes?
- Recomendaciones para mejorar la resiliencia

### Entregable

- Plan de recuperación documentado con pasos ejecutados

---

## Semana 7: DDoS — Defensa del Servidor Web

### Objetivos de Aprendizaje

1. Detectar un ataque de denegación de servicio en tiempo real
2. Identificar patrones de tráfico malicioso con herramientas de análisis
3. Implementar reglas de mitigación con iptables
4. Evaluar la efectividad de las contramedidas implementadas

### Contenido Teórico (30 min)

- Tipos de DDoS: volumétrico, de protocolo, de aplicación
- Técnicas de amplificación (DNS, NTP, Memcached)
- Herramientas de detección y mitigación
- Análisis de flujo de tráfico para identificar anomalías

### Ejercicio Práctico con Tectonic (2 horas)

- Despliegue del escenario `03_ddos`
- Captura de tráfico con `tcpdump` durante el ataque
- Análisis de tráfico con `tshark` (estadísticas, conversaciones)
- Identificación de IPs atacantes con `ss` y `netstat`
- Implementación de reglas `iptables` de mitigación:
  - Rate limiting por IP
  - Bloqueo de IPs atacantes
  - Protección de servicios críticos
- Monitoreo de efectividad con `top` y métricas de servidor
- Análisis forense del tráfico de ataque

### Discusión y Reporte (30 min)

- ¿Cuánto tiempo tomó detectar el ataque?
- ¿Las reglas de iptables fueron suficientes?
- Discusión sobre servicios de mitigación DDoS externos

### Entregable

- Análisis del ataque DDoS con gráficas de tráfico y reglas implementadas

---

## Semana 8: Seguridad de Aplicaciones Web — Escenario 04 Intrusion (Detección)

### Objetivos de Aprendizaje

1. Identificar indicadores de intrusión en aplicaciones web
2. Analizar logs de servidor web para detectar actividad maliciosa
3. Reconocer vulnerabilidades comunes en aplicaciones web (OWASP Top 10)
4. Implementar monitoreo de seguridad en aplicaciones

### Contenido Teórico (30 min)

- OWASP Top 10 (2021)
- Técnicas de inyección SQL, XSS,命令执行
- Análisis de logs de servidor web (Apache, Nginx)
- Herramientas de detección de intrusión (IDS/IPS)

### Ejercicio Práctico con Tectonic (2 horas)

- Despliegue del escenario `04_intrusion`
- Análisis de logs de servidor web con `grep` y `awk`
- Detección de patrones de ataque en logs (SQLi, XSS)
- Uso de `nmap` con scripts de vulnerabilidades web
- Análisis de tráfico HTTP con `tshark`
- Identificación de endpoints comprometidos
- Búsqueda de webshells con `find` y `strings`
- Mapeo de la superficie de ataque

### Discusión y Reporte (30 min)

- ¿Qué vulnerabilidades fueron explotadas?
- ¿Cómo se podría haber prevenido la intrusión?
- Priorización de hallazgos según criticidad

### Entregable

- Informe de vulnerabilidades web identificadas con nivel de riesgo

---

## Semana 9: Movimiento Lateral y Escalamiento — Escenario 04 Intrusion (Respuesta)

### Objetivos de Aprendizaje

1. Detectar movimiento lateral entre sistemas de la red
2. Analizar credenciales comprometidas y autenticación sospechosa
3. Implementar estrategias de contención para frenar el escalamiento
4. Ejecutar procedimientos de erradicación completos

### Contenido Teórico (30 min)

- Técnicas de movimiento lateral (Pass-the-Hash, lateral movement)
- Escalamiento de privilegios en entornos Windows y Linux
- MITRE ATT&CK: techniques T1021, T1078, T1134
- Segmentación de red como contramedida

### Ejercicio Práctico con Tectonic (2 horas)

- Continuación del escenario `04_intrusion`
- Análisis de logs de autenticación con `grep` y `journalctl`
- Detección de logins anómalos con `last`, `lastb`
- Monitoreo de conexiones de red con `ss` y `lsof`
- Identificación de procesos sospechosos con `ps aux`
- Bloqueo de IPs y usuarios comprometidos con `iptables`
- Extracción de evidencia de movimiento lateral
- Análisis de archivos de configuración comprometidos

### Discusión y Reporte (30 min)

- ¿Cómo se movió el atacante entre sistemas?
- ¿Qué credenciales fueron comprometidas?
- ¿Qué debimos haber contenido primero?

### Entregable

- Timeline del movimiento lateral con diagrama de propagación

---

## Semana 10: Exfiltración de Datos y DNS Tunneling — Escenario 05 Exfiltración

### Objetivos de Aprendizaje

1. Detectar exfiltración de datos a través de diferentes canales
2. Identificar técnicas de DNS tunneling y covert channels
3. Analizar tráfico de red para detectar patrones de exfiltración
4. Implementar reglas de prevención de exfiltración

### Contenido Teórico (30 min)

- Técnicas de exfiltración de datos
- DNS tunneling: cómo funciona y por qué es efectivo
- Análisis de patrones de tráfico para detección
- DLP (Data Loss Prevention) conceptos básicos

### Ejercicio Práctico con Tectonic (2 horas)

- Despliegue del escenario `05_exfiltracion`
- Captura de tráfico DNS con `tcpdump` y `tshark`
- Análisis de consultas DNS sospechosos (nombres largos, alta frecuencia)
- Identificación de patrones de exfiltración con `tshark`
- Análisis de tráfico HTTP/HTTPS con `tshark` y `grep`
- Bloqueo de dominios/servidores de exfiltración con `iptables`
- Extracción de datos exfiltrados con `strings`
- Análisis de logs de DNS con `grep` y `awk`

### Discusión y Reporte (30 min)

- ¿Cómo se detectó la exfiltración?
- ¿Qué volumen de datos fue comprometido?
- ¿Qué medidas de DLP podrían prevenirlo?

### Entregable

- Análisis del canal de exfiltración con evidencia capturada

---

## Semana 11: Análisis Forense Digital — Escenario 06 Forensia

### Objetivos de Aprendizaje

1. Ejecutar un proceso forense completo siguiendo estándares
2. Crear y verificar imágenes forenses de disco y memoria
3. Extraer evidencia clave usando herramientas forenses
4. Mantener la cadena de custodia de evidencia digital

### Contenido Teórico (30 min)

- Metodología forense (NIST SP 800-86)
- Cadena de custodia y preservación de evidencia
- Herramientas del forensic toolkit
- Análisis de memoria vs análisis de disco

### Ejercicio Práctico con Tectonic (2 horas)

- Despliegue del escenario `06_forensia`
- Creación de imagen de disco con `dd` y verificación con `md5sum`
- Análisis de particiones con `mmls`
- Listado de archivos con `fls` y extracción con `icat`
- Análisis de memoria con Volatility3 (procesos, conexiones, artefactos)
- File carving con `foremost` para recuperar archivos eliminados
- Análisis de strings con `strings` en binarios sospechosos
- Identificación de tipos de archivo con `file`
- Búsqueda de artefactos de navegación y archivos temporales

### Discusión y Reporte (30 min)

- ¿Qué evidencia clave se encontró?
- ¿Se mantuvo la cadena de custodia?
- ¿Qué artefactos fueron más reveladores?

### Entregable

- Informe forense completo con cadena de custodia documentada

---

## Semana 12: Simulacro de Crisis y Evaluación Final

### Objetivos de Aprendizaje

1. Integrar todos los conocimientos en un escenario de crisis combinado
2. Ejecutar un procedimiento de respuesta a incidentes completo
3. Demostrar competencia en análisis forense y contención
4. Presentar hallazgos de forma clara y profesional

### Contenido Teórico (30 min)

- Gestión de crisis en ciberseguridad
- Comunicación durante un incidente
- Lecciones aprendidas y mejora continua
- Preparación para certificaciones

### Ejercicio Práctico con Tectonic (2 horas)

- Escenario combinado que integra:
  - Detección de phishing inicial
  - Propagación de malware/ransomware
  - Movimiento lateral
  - Exfiltración de datos
  - Ataque DDoS simultáneo
- Ejecución de respuesta a incidentes en tiempo real:
  1. Detección y análisis
  2. Contención (iptables, bloqueo)
  3. Erradicación
  4. Recuperación
  5. Documentación
- Cada equipo presenta su respuesta y hallazgos

### Discusión y Reporte (30 min)

- Presentación de hallazgos por equipos
- Evaluación cruzada entre equipos
- Reflexión final sobre el curso
- Planificación de capacitación continua

### Entregable

- Informe completo de respuesta al incidente con timeline, evidencia y recomendaciones

---

## Criterios de Evaluación

| Criterio | Porcentaje | Descripción |
|---|---|---|
| **Práctica en laboratorio** | 40% | Participación activa en ejercicios Tectonic, uso correcto de herramientas, capacidad de ejecutar comandos de forma autónoma |
| **Informes y reportes** | 30% | Calidad de los entregables, análisis crítico, formato profesional, documentación de hallazgos |
| **Evaluación final (Semana 12)** | 30% | Desempeño en el simulacro de crisis integrador, capacidad de respuesta bajo presión, presentación de resultados |

### Escala de calificación

- **90-100%:** Excelente — Dominio completo de herramientas y metodología
- **80-89%:** Muy Bueno — Sólido conocimiento con áreas de mejora menores
- **70-79%:** Bueno — Comprensión adecuada, requiere refuerzo en algunas áreas
- **60-69%:** Aceptable — Conocimientos básicos, necesita práctica adicional
- **<60%:** Insuficiente — Requiere cursar nuevamente el programa

---

## Certificaciones Recomendadas

Tras completar el curso, se recomienda que el personal busque las siguientes certificaciones para validar y expandir sus conocimientos:

| Certificación | Organismo | Enfoque |
|---|---|---|
| **CompTIA Security+** | CompTIA | Fundamentos de ciberseguridad, ampliamente reconocida |
| **CEH (Certified Ethical Hacker)** | EC-Council | Hacking ético y análisis de vulnerabilidades |
| **CISSP (Certified Information Systems Security Professional)** | (ISC)² | Gestión y arquitectura de seguridad |
| **CHFI (Computer Hacking Forensic Investigator)** | EC-Council | Análisis forense digital |
| **CompTIA CySA+** | CompTIA | Análisis de seguridad y defensa |
| **GCIH (GIAC Certified Incident Handler)** | GIAC/SANS | Respuesta a incidentes |
| **GCFE (GIAC Certified Forensic Examiner)** | GIAC/SANS | Investigación forense avanzada |
| **CompTIA PenTest+** | CompTIA | Pruebas de penetración |
| **OSCP (Offensive Security Certified Professional)** | OffSec | Pruebas de penetración avanzadas |
| **CCSP (Certified Cloud Security Professional)** | (ISC)² | Seguridad en la nube |

---

## Recursos y Referencias

### Marcos y Estándares

| Recurso | URL | Descripción |
|---|---|---|
| **NIST Cybersecurity Framework** | https://www.nist.gov/cyberframework | Marco de referencia para gestión de riesgos de ciberseguridad |
| **NIST SP 800-86** | https://csrc.nist.gov/publications/detail/sp/800-86/final | Guía de integración de técnicas forenses |
| **MITRE ATT&CK** | https://attack.mitre.org | Base de conocimiento de tácticas y técnicas de adversarios |
| **OWASP Top 10** | https://owasp.org/www-project-top-ten/ | Principales vulnerabilidades de aplicaciones web |
| **CIS Benchmarks** | https://www.cisecurity.org/cis-benchmarks | Benchmarks de configuración segura |

### Organismos de Respuesta a Incidentes

| Organismo | País | Descripción |
|---|---|---|
| **CERTuy** | Uruguay | Equipo de Respuesta ante Incidentes de Seguridad Informática de Uruguay |
| **AGESIC** | Uruguay | Agencia de Gobierno Electrónico e Informática y Conocimiento |
| **US-CERT** | Estados Unidos | Equipo de respuesta de emergencias de computadoras de EE.UU. |
| **FIRST** | Global | Forum of Incident Response and Security Teams |
| **MeliCERTes** | Latinoamérica | Red de CSIRTs de Latinoamérica |

### Documentación de Herramientas

| Herramienta | Referencia |
|---|---|
| **Tectonic** | Documentación oficial de Tectonic lab_edition |
| **Wireshark** | https://www.wireshark.org/docs/ |
| **Nmap** | https://nmap.org/book/ |
| **Volatility** | https://github.com/volatilityfoundation/volatility3 |
| **Sleuth Kit** | https://sleuthkit.org/sleuthkit/ |
| **John the Ripper** | https://openwall.com/john/ |
| **Hashcat** | https://hashcat.net/wiki/ |

### Libros Recomendados

- *The Art of Deception* — Kevin Mitnick
- *Incident Response & Computer Forensics* — Jason Luttgens
- *Network Security Assessment* — Chris McNab
- *Hacking: The Art of Exploitation* — Jon Erickson
- *Practical Malware Analysis* — Michael Sikorski

### Plataformas de Práctica Adicionales

- **Hack The Box:** https://www.hackthebox.com
- **TryHackMe:** https://tryhackme.com
- **PicoCTF:** https://picoctf.org
- **OverTheWire (Bandit):** https://overthewire.org/wargames/bandit/
- **CyberDefenders:** https://cyberdefenders.org

---

*Plan de Curso — Capacitación en Ciberseguridad con Tectonic — BHU*
*Versión 1.0 — 2026*
