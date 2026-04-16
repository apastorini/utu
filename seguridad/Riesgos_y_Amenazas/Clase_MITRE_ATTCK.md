# Clase: MITRE ATT&CK - Conocimiento de Técnicas de Ataque

## Introducción

MITRE ATT&CK (Adversarial Tactics, Techniques & Common Knowledge) es una base de conocimiento globally recognized de tácticas y técnicas de ciberseguridad adversary. Proporciona un lenguaje común para describir cómo los atacantes operan, desde el reconocimiento inicial hasta el logro de sus objetivos.

**Objetivos de aprendizaje:**
1. Comprender la estructura y componentes de ATT&CK
2. Familiarizarse con las tácticas y técnicas documentadas
3. Aplicar ATT&CK en análisis de amenazas y detección
4. Utilizar ATT&CK Navigator para visualización
5. Crear perfiles de amenazas usando ATT&CK
6. Integrar ATT&CK en programas de seguridad

---

## 1. Introducción a MITRE ATT&CK

### 1.1 ¿Qué es ATT&CK?

**ATT&CK** es un marco de trabajo desarrollado por MITRE Corporation que documenta:
- **Tácticas:** Objetivos del atacante en cada fase
- **Técnicas:** Cómo se logran esos objetivos
- **Mitigaciones:** Cómo prevenir o detectar cada técnica
- **Procedimientos:** Implementaciones específicas observadas en el mundo real

### 1.2 Historia y evolución

| Año | Versión | Características |
|-----|---------|-----------------|
| 2013 | PRE-ATT&CK | Técnicas de pre-ataque |
| 2015 | ATT&CK for Enterprise | Matriz inicial (Windows) |
| 2017 | ATT&CK Mobile | Técnicas móviles |
| 2019 | ATT&CK v7 | Expansión, integrations |
| 2021 | ATT&CK v10 | Industrial Control Systems |
| 2024 | ATT&CK v15 | Actualización contínua |

### 1.3 Componentes principales

```
┌─────────────────────────────────────────────────────────────┐
│                  ESTRUCTURA DE ATT&CK                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ MATRIZ ENTERPRISE (Windows, macOS, Linux, Network)  │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ MATRIZ MOBILE (Android, iOS)                         │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ MATRIZ ICS (Industrial Control Systems)              │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ CAPEC (Common Attack Pattern Enumeration)            │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. La Matriz de Tácticas

### 2.1 Tácticas en orden de ataque

| # | Táctica | Código | Descripción | Ejemplo |
|---|---------|--------|-------------|---------|
| 1 | **Reconnaissance** | RECON | Recopilar información sobre objetivos | OSINT, escaneo de red |
| 2 | **Resource Development** | RSRC | Establecer recursos para ataque | Comprar malware, infrastructure |
| 3 | **Initial Access** | INIT | Obtener punto de entrada | Phishing, exploit de servicio |
| 4 | **Execution** | EXEC | Ejecutar código malicioso | Command execution, scripts |
| 5 | **Persistence** | PERS | Mantener acceso | Backdoors, scheduled tasks |
| 6 | **Privilege Escalation** | PRIV | Elevar privilegios | Exploits, password dumping |
| 7 | **Defense Evasion** | EVAS | Evitar detección | Disabling tools, obfuscation |
| 8 | **Credential Access** | CRDL | Robar credenciales | Keylogging, credential dumping |
| 9 | **Discovery** | DISC | Explorar el entorno | Network scanning, account discovery |
| 10 | **Lateral Movement** | LATM | Moverse por la red | RDP, SMB, Pass-the-hash |
| 11 | **Collection** | COLL | Recopilar datos | Screenshots, file collection |
| 12 | **Command and Control** | C2 | Comunicar con C2 | DNS tunneling, HTTPS |
| 13 | **Exfiltration** | EXFL | Extraer datos | FTP, cloud upload |
| 14 | **Impact** | IMPT | Dañar o interrumpir | Ransomware, data destruction |

### 2.2 Flujo de ataque simplificado

```
┌─────────────────────────────────────────────────────────────┐
│              FLUJO DE ATAQUE EN ATT&CK                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐             │
│  │  RECON   │───▶│  RSRC    │───▶│  INIT    │             │
│  │ Gather   │    │ Acquire  │    │ Get in   │             │
│  │ info     │    │ resour.  │    │ network  │             │
│  └──────────┘    └──────────┘    └────┬─────┘             │
│                                         │                   │
│                                         ▼                   │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐             │
│  │   IMPT   │◀───│  EXFL    │◀───│   C2     │             │
│  │ Damage/  │    │ Steal    │    │ Talk to  │             │
│  │ Destroy  │    │ data     │    │ attacker │             │
│  └──────────┘    └──────────┘    └────┬─────┘             │
│                                         │                   │
│         ┌───────────────────────────────┼───────────────┐ │
│         │                               │               │ │
│         ▼                               ▼               ▼ │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐             │
│  │  LATM    │───▶│  COLL    │───▶│  CRDL    │             │
│  │ Spread   │    │ Gather   │    │ Steal    │             │
│  │ through  │    │ target   │    │ creds    │             │
│  │ network  │    │ data     │    │           │             │
│  └────┬─────┘    └──────────┘    └──────────┘             │
│       │                                                      │
│       │              ┌──────────┐    ┌──────────┐           │
│       └─────────────▶│   EXEC   │───▶│   DISC   │           │
│                      │ Run code │    │ Explore  │           │
│                      └────┬─────┘    │ network  │           │
│                           │          └──────────┘           │
│                           │                                │
│                           ▼                                │
│                      ┌──────────┐    ┌──────────┐        │
│                      │   PERS   │◀───│  EVAS    │        │
│                      │ Stay     │    │ Avoid    │        │
│                      │ inside   │    │ detect.  │        │
│                      └──────────┘    └──────────┘        │
│                           │                                │
│                           │          ┌──────────┐          │
│                           └─────────▶│  PRIV   │          │
│                                      │ Escalate│          │
│                                      └──────────┘          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. Técnicas Detalladas por Táctica

### 3.1 Initial Access (Acceso Inicial)

**Objetivo:** Obtener un punto de apoyo en la red.

| Technique ID | Técnica | Descripción |
|--------------|---------|-------------|
| T1566 | Phishing | Envío de mensajes maliciosos |
| T1566.001 | Spearphishing Attachment | Email con adjunto malicioso |
| T1566.002 | Spearphishing Link | Email con link malicioso |
| T1566.003 | Spearphishing by Service | Usando servicios de terceros |
| T1190 | Exploit Public-Facing Application | Vulnerabilidades web |
| T1133 | External Remote Services | VPN, RDP expuesto |
| T1569 | Drive-by Compromise | Exploit desde navegador |
| T1204 | User Execution | Usuario ejecuta algo |
| T0889 | Compromise Software Developer Tools | Supply chain developer |

**Controles para Initial Access:**

| Mitigación | ID | Descripción |
|------------|----|-------------|
| Anti-phishing | M1049 | Detección de phishing |
| Application control | M1038 | Whitelisting de ejecución |
| Network segmentation | M0930 | Segmentar servicios expuestos |
| Restrict Web-based Content | M1021 | Filtrar contenido web peligroso |

### 3.2 Execution (Ejecución)

**Objetivo:** Ejecutar código controlado por el atacante.

| Technique ID | Técnica | Descripción |
|--------------|---------|-------------|
| T1059 | Command and Scripting Interpreter | PowerShell, Python, etc. |
| T1059.001 | PowerShell | Uso de PowerShell |
| T1059.003 | Windows Command Shell | cmd.exe |
| T1059.004 | Unix Shell | bash, sh |
| T1059.006 | Python | Scripts en Python |
| T1106 | Native API | Llamadas directas a APIs |
| T1204.002 | Malicious File | Usuario ejecuta archivo malicioso |
| T1047 | Windows Management Instrumentation | WMI para ejecución |

### 3.3 Persistence (Persistencia)

**Objetivo:** Mantener acceso incluso después de reinicios o cambios.

| Technique ID | Técnica | Descripción |
|--------------|---------|-------------|
| T1547 | Boot or Logon Autostart Execution | Ejecución al inicio |
| T1547.001 | Registry Run Keys/Startup Folder | Modificar Run keys |
| T1053 | Scheduled Task/Job | Tareas programadas |
| T1053.005 | Scheduled Task | Windows Task Scheduler |
| T1543 | Create/Modify System Process | Crear servicios |
| T1543.003 | Windows Service | Crear servicio de Windows |
| T1505 | Server Software Component | Malicious extensions |
| T1556 | Modify Authentication Process | Modificar autenticación |

### 3.4 Privilege Escalation (Escalación de Privilegios)

**Objetivo:** Obtener permisos elevados (admin, SYSTEM).

| Technique ID | Técnica | Descripción |
|--------------|---------|-------------|
| T1068 | Exploitation for Privilege Escalation | Aprovechar vulnerabilidad |
| T1055 | Process Injection | Inyectar código en procesos |
| T1548 | Abuse Elevation Control Mechanism | Bypass UAC |
| T1548.002 | Bypass User Account Control | UAC bypass |
| T1075 | Pass the Hash | Usar hash para autenticación |
| T1003 | OS Credential Dumping | Extraer credenciales |
| T1003.001 | LSASS Memory | Dumping de LSASS |
| T1003.002 | Security Account Manager | SAM database |

### 3.5 Defense Evasion (Evasión de Defensas)

**Objetivo:** Evitar ser detectado.

| Technique ID | Técnica | Descripción |
|--------------|---------|-------------|
| T1562 | Impair Defenses | Deshabilitar controles |
| T1562.001 | Disable or Modify Tools | Apagar antivirus |
| T1562.002 | Disable Windows Event Logging | Apagar logging |
| T1070 | Indicator Removal | Borrar evidencia |
| T1070.004 | File Deletion | Borrar archivos |
| T1070.006 | Timestomp | Modificar timestamps |
| T1027 | Obfuscated Files or Information | Ofuscar código |
| T1027.001 | Binary Padding | Añadir bytes a archivos |
| T1036 | Masquerading | Ocultar nombre/ubicación |

### 3.6 Credential Access (Acceso a Credenciales)

**Objetivo:** Robar credenciales de usuarios.

| Technique ID | Técnica | Descripción |
|--------------|---------|-------------|
| T1110 | Brute Force | Fuerza bruta |
| T1110.001 | Password Guessing | Adivinar contraseñas |
| T1110.003 | Password Spraying | Un password para muchos usuarios |
| T1110.004 | Credential Stuffing | Usar credenciales robadas |
| T1056 | Input Capture | Capturar input |
| T1056.001 | Keylogging | Registrar teclas |
| T1003 | Credential Dumping | Extraer credenciales de sistema |
| T1552 | Unsecured Credentials | Buscar credenciales en texto claro |

### 3.7 Lateral Movement (Movimiento Lateral)

**Objetivo:** Moverte por la red hacia otros sistemas.

| Technique ID | Técnica | Descripción |
|--------------|---------|-------------|
| T1021 | Remote Services | Servicios remotos |
| T1021.001 | Remote Desktop Protocol | RDP |
| T1021.002 | SMB/Windows Admin Shares | SMB para copia de archivos |
| T1021.004 | SSH | Secure Shell |
| T1210 | Exploitation of Remote Services | Explotar servicios remotos |
| T1570 | Lateral Tool Transfer | Transferir herramientas |
| T1072 | Software Deployment Tools | Usar herramientas de deploy |
| T1080 | Taint Shared Content | Contaminar contenido compartido |

### 3.8 Collection (Colección)

**Objetivo:** Recopilar datos de interés.

| Technique ID | Técnica | Descripción |
|--------------|---------|-------------|
| T1005 | Data from Local System | Archivos del sistema |
| T1039 | Data from Network Shared Drive | Datos de shares de red |
| T1074 | Data Staged | Preparar datos para exfiltrar |
| T1113 | Screen Capture | Capturas de pantalla |
| T1114 | Email Collection | Colección de emails |
| T1114.002 | Remote Email Collection | Acceso remoto a emails |
| T1056 | Input Capture | Capturar información |

### 3.9 Command and Control (Comando y Control)

**Objetivo:** Comunicarse con sistemas del atacante.

| Technique ID | Técnica | Descripción |
|--------------|---------|-------------|
| T1071 | Application Layer Protocol | Protocolos de aplicación |
| T1071.001 | Web Protocols | HTTP/HTTPS |
| T1071.004 | DNS | DNS como canal C2 |
| T1090 | Proxy | Uso de proxies |
| T1095 | Non-Application Layer Protocol | Protocolos no estándar |
| T1105 | Ingress Tool Transfer | Descargar herramientas |
| T1102 | Web Service | Usar servicios web legítimos |
| T1219 | Remote Access Software | Software de acceso remoto |

### 3.10 Exfiltration (Exfiltración)

**Objetivo:** Extraer datos de la víctima.

| Technique ID | Técnica | Descripción |
|--------------|---------|-------------|
| T1041 | Exfiltration Over C2 Channel | Vía canal de comando |
| T1048 | Exfiltration Over Alternative Protocol | Protocolos alternativos |
| T1048.002 | Exfiltration Over Asymmetric Encrypted Non-C2 Protocol | FTP, etc |
| T1048.003 | Exfiltration Over Command and Control Channel | Mismo canal C2 |
| T1567 | Exfiltration Over Web Service | Cloud storage, etc |
| T1567.002 | Exfiltration to Cloud Storage | Upload a cloud storage |
| T1052 | Exfiltration Over Physical Medium | USB, etc |

### 3.11 Impact (Impacto)

**Objetivo:** Causar daño directo a la organización.

| Technique ID | Técnica | Descripción |
|--------------|---------|-------------|
| T1486 | Data Encrypted for Impact | Ransomware |
| T1489 | Service Stop | Detener servicios |
| T1529 | System Shutdown/Reboot | Apagar sistemas |
| T1530 | Data from Cloud Storage | Robar datos de cloud |
| T1565 | Data Manipulation | Manipular datos |
| T1484 | Domain Trust Modification | Modificar AD trust |
| T1527 | Boot or Logon Initialization Scripts | Scripts de boot |

---

## 4. MITRE ATT&CK Navigator

### 4.1 ¿Qué es ATT&CK Navigator?

Herramienta web para visualizar y personalizar matrices ATT&CK.
- URL: attack.mitre.org/#/techniques Enterprise
- Permite crear capas personalizadas
- Marcar técnicas cubiertas/no cubiertas
- Comparar diferentes perfiles

### 4.2 Uso del Navigador

**Crear una capa personalizada:**

```
1. Acceder a attack.mitre.org/#/navigator
2. Click en "Create Layer"
3. Seleccionar matriz (Enterprise, Mobile, ICS)
4. Filtrar por:
   - Platform (Windows, Linux, macOS)
   - Groups (APT29, FIN7, etc.)
   - Software (Cobalt Strike, Mimikatz)
5. Marcar técnicas con colores:
   - Verde: Controles implementados
   - Rojo: Brechas identificadas
   - Amarillo: Parcialmente cubierto
6. Exportar como JSON o imagen
```

### 4.3 Ejemplo de layer para organización bancaria

```
┌─────────────────────────────────────────────────────────────┐
│  COBERTURA DE CONTROLES ATT&CK - CAPA DE DETECCIÓN          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Tácticas:                                                  │
│  ┌────────────────────────────────────────────────────────┐│
│  │ RECON ██████████████████████████░░░░░░░░░░░░░░░░░░░░░ ││
│  │ [████████████████████] 80% cubierto                     ││
│  └────────────────────────────────────────────────────────┘│
│  ┌────────────────────────────────────────────────────────┐│
│  │ INIT ████████████████████████████░░░░░░░░░░░░░░░░░░░░░ ││
│  │ [██████████████████████] 85% cubierto                   ││
│  └────────────────────────────────────────────────────────┘│
│  ┌────────────────────────────────────────────────────────┐│
│  │ EXEC ██████████████████████████████░░░░░░░░░░░░░░░░░░░ ││
│  │ [████████████████████████] 90% cubierto                ││
│  └────────────────────────────────────────────────────────┘│
│  ┌────────────────────────────────────────────────────────┐│
│  │ PERS ████████████████████████████████████░░░░░░░░░░░░░ ││
│  │ [████████████████████████████] 92% cubierto            ││
│  └────────────────────────────────────────────────────────┘│
│  ┌────────────────────────────────────────────────────────┐│
│  │ C2 ███████████████████████████████████░░░░░░░░░░░░░░░░ ││
│  │ [██████████████████████████████] 88% cubierto           ││
│  └────────────────────────────────────────────────────────┘│
│                                                             │
│  Color:                                                     │
│  ████ = Controles implementados (verde)                     │
│  ░░░░ = Brechas identificadas (rojo)                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. Aplicaciones Prácticas

### 5.1 Purple Team con ATT&CK

```
┌─────────────────────────────────────────────────────────────┐
│              INTEGRACIÓN PURPLE TEAM                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  RED TEAM              │           BLUE TEAM                │
│  (Simula atacante)     │           (Defiende)              │
│                        │                                    │
│  Plan usando ATT&CK ───┼──▶ Seleccionar técnicas a probar   │
│                        │                                    │
│                        │                                    │
│  Ejecuta ataque ───────┼──▶ Detectar y responder            │
│                        │                                    │
│                        │                                    │
│  Reporta resultados ───┼──▶ Analizar cobertura              │
│                        │                                    │
│                        │                                    │
│  ┌─────────────────────┴───────────────────────────────┐  │
│  │           MEJORA CONTINUA DE DETECCIÓN                │  │
│  │                                                       │  │
│  │  1. Identificar gaps de detección                    │  │
│  │  2. Crear reglas de detección (SIEM/EDR)             │  │
│  │  3. Validar que funcionan                          │  │
│  │  4. Documentar en ATT&CK layer                     │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 5.2 Crear Threat Profile con ATT&CK

**Perfil para FIN7 (grupo cibercriminal):**

```
┌─────────────────────────────────────────────────────────────┐
│  THREAT PROFILE: FIN7                                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  DESCRIPCIÓN:                                               │
│  - Grupo cibercriminal activo desde ~2013                   │
│  - Motivación: Beneficio financiero                         │
│  - GEO: Principalmente Europa y USA                         │
│  - Industria: Retail, restaurantes, banca                   │
│                                                             │
│  TTP PRINCIPALES (según ATT&CK):                            │
│                                                             │
│  [X] RECON: T1595 - Active Scanning                        │
│  [X] RECON: T1592 - Gather Victim Host Information         │
│  [X] INIT: T1566 - Phishing                                │
│  [X] INIT: T1566.001 - Spearphishing Attachment            │
│  [X] EXEC: T1059 - Command and Scripting Interpreter        │
│  [X] EXEC: T1059.003 - Windows Command Shell                │
│  [X] PERS: T1547 - Boot or Logon Autostart Execution        │
│  [X] PRIV: T1003 - OS Credential Dumping                    │
│  [X] CRDL: T1003.001 - LSASS Memory                        │
│  [X] LATM: T1021 - Remote Services                         │
│  [X] LATM: T1021.002 - SMB/Windows Admin Shares            │
│  [X] C2: T1071 - Application Layer Protocol                  │
│  [X] C2: T1573 - Encrypted Channel                          │
│  [X] IMPT: T1486 - Data Encrypted for Impact (Ransomware)   │
│                                                             │
│  SOFTWARE ASOCIADO:                                          │
│  - Carbanak (backdoor)                                      │
│  - Cobalt Strike (commercial)                               │
│  - PowerShell scripts custom                                │
│                                                             │
│  MITIGACIONES RECOMENDADAS:                                 │
│  - M1040 - Behavior Prevention on Endpoint                  │
│  - M1021 - Restrict Web-based Content                       │
│  - M1017 - User Training                                    │
│  - M1026 - Privileged Account Management                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 5.3 Mapeo de Detection Rules a ATT&CK

**Ejemplo de mapeo para SIEM:**

| Technique | Technique Name | Detection Rule | Status |
|-----------|----------------|---------------|--------|
| T1566.001 | Spearphishing Attachment | `src_email_contains_malicious_attachment AND dest_user_count > 5` | Implemented |
| T1059.003 | Windows Command Shell | `process_name=cmd.exe AND parent_process=microsoft_word` | Implemented |
| T1547.001 | Registry Run Keys | `registry_key=HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run` | Partial |
| T1003.001 | LSASS Memory | `process_name=lsass.exe AND remote_memory_access` | Implemented |
| T1047 | WMI | `process_parent=powershell.exe AND process_cmd=*WMI*` | Implemented |

---

## 6. ATT&CK en Diferentes Contextos

### 6.1 ATT&CK Enterprise

**Plataformas cubiertas:**
- Windows
- macOS
- Linux
- Cloud (Office 365, Google Workspace, AWS, Azure, Azure AD)
- Network

### 6.2 ATT&CK Mobile

| Táctica | Técnicas clave |
|---------|----------------|
| Initial Access | Phishing, Drive-by, Supply Chain |
| Persistence | App auto-start, credentials access |
| Collection | Location, audio, camera, clipboard |
| Exfiltration | SMS, phone call, cloud exfil |

### 6.3 ATT&CK ICS

**Sectores:** Energía, agua, manufactura, transporte

| Táctica | Relevancia ICS |
|---------|---------------|
| Initial Access | IT/OT convergence, spearphishing |
| Execution | Modbus, engineering software |
| Persistence | PLC ladder logic, historian |
| Impact | HMI manipulation, process disruption |

---

## 7. Taller Práctico: Análisis de Incidente con ATT&CK

### 7.1 Escenario

Se detecta actividad sospechosa en un servidor Windows de una empresa bancaria:

```
Log Activity Detected:
1. PowerShell executing encoded commands
2. SMB connection to suspicious IP
3. LSASS access from non-system process
4. New registry Run key created
5. Outbound DNS queries to unusual domain
```

### 7.2 Mapeo a ATT&CK

| # | Actividad observada | Technique ID | Technique Name | Táctica |
|---|---------------------|--------------|----------------|---------|
| 1 | PowerShell encoded | T1059.001 | PowerShell | Execution |
| 2 | SMB connection | T1021.002 | SMB/Windows Admin Shares | Lateral Movement |
| 3 | LSASS access | T1003.001 | LSASS Memory | Credential Access |
| 4 | Registry Run key | T1547.001 | Registry Run Keys/Startup Folder | Persistence |
| 5 | DNS queries | T1071.004 | DNS | Command and Control |

### 7.3 Análisis de ATT&CK Navigator

```
┌─────────────────────────────────────────────────────────────┐
│  CAPA DE INCIDENTE - ATAQUE DETECTADO                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [X] EXEC - T1059.001 (PowerShell) - DETECTADO ✓           │
│  [X] LATM - T1021.002 (SMB) - DETECTADO ✓                  │
│  [X] CRDL - T1003.001 (LSASS) - DETECTADO ✓                │
│  [X] PERS - T1547.001 (Registry) - DETECTADO ✓             │
│  [X] C2 - T1071.004 (DNS) - DETECTADO ✓                    │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐  │
│  │ GAPS IDENTIFICADAS:                                  │  │
│  │ - No se detectó el movimiento lateral inicial        │  │
│  │ - No se identificó la técnica de descarga inicial    │  │
│  └─────────────────────────────────────────────────────┘  │
│                                                             │
│  RECOMENDACIONES:                                           │
│  1. Mejorar detección de PowerShell obfuscated             │
│  2. Monitorizar tráfico SMB lateral                        │
│  3. Investigar DNS exfiltration patterns                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 8. Recursos y Herramientas

### 8.1 Herramientas oficiales

| Herramienta | URL | Propósito |
|-------------|-----|-----------|
| ATT&CK Navigator | attack.mitre.org | Visualización de matrices |
| ATT&CK Workbench | mitre-attack.github.io/attack-navigator | Crear layers personalizados |
| ATT&CK UI | attack.mitre.org | Exploración de técnicas |
| CTI Friday | YouTube | Actualizaciones y tutoriales |

### 8.2 Integraciones comunes

| Plataforma | Integración ATT&CK |
|------------|-------------------|
| Splunk | ATT&CK SPL searches |
| Microsoft Sentinel | AttackIQ workbook |
| Elastic | Detection rules |
| Palo Alto XSIAM | ATT&CK-based analytics |
| IBM QRadar | offense mapping |
| MITRE Engenuity | Center for Threat-Informed Defense |

---

## Resumen

MITRE ATT&CK es fundamental porque:

1. **Estandariza** el lenguaje de seguridad a nivel global
2. **Documenta** el "cómo" de los atacantes reales
3. **Permite** comparar capacidades de detección
4. **Facilita** la comunicación entre equipos
5. **Guía** el desarrollo de controles y detecciones
6. **Evoluciona** continuamente con nuevas amenazas

ATT&CK no es un framework de compliance, sino una fuente de conocimiento basada en adversarios reales que ayuda a construir defenses más efectivas.

---

**Material complementario:**
- MITRE ATT&CK Navigator (attack.mitre.org)
- MITRE ATT&CK Eye (blog con updates)
- STIX/TAXII para threat intelligence feeds
- Repositorio de detection rules

**Ejercicio práctico:**
1. Investigar un APT conocido (APT41, FIN7, Lazarus)
2. Mapear sus TTPs a ATT&CK
3. Crear una capa en ATT&CK Navigator
4. Identificar gaps de detección en tu organización

**Referencias:**
- attack.mitre.org
- MITRE ATT&CK Primer
- Building Cyber Resilience with ATT&CK (MITRE)
