# Despliegue Profesional del Entorno RBVM en Windows con WSL 2 + Docker Desktop

**Clase Especial | Gestion de Vulnerabilidades por Riesgos - Modulo Practico**

**Autor:** Prof. Adrian Pastarini (TSI)
**Version:** 1.0
**Fecha:** Agosto 2026
**Plataforma:** Windows 10/11 + WSL 2 (Ubuntu) + Docker Desktop
**Objetivo:** Desplegar un entorno de laboratorio aislado, profesional y sin riesgo para la red corporativa.

---

## 1. Objetivos de Aprendizaje

Al finalizar esta clase, el estudiante podra:

1. Configurar WSL 2 + Docker Desktop en Windows de forma segura y aislada.
2. Desplegar CISO Assistant (GRC y Gestion de Riesgo) y DefectDojo (Gestion de Vulnerabilidades) via Docker.
3. Importar reportes de escaneos y practicar con datasets de ejemplo sin tocar sistemas productivos.
4. Comprender como extraer logs e informacion de forma pasiva y segura.

---

## 2. Por que WSL 2 + Docker Desktop en Windows?

| Beneficio | Descripcion |
|-----------|-------------|
| **Aislamiento total** | Los contenedores corren dentro de WSL 2, separados de la red corporativa |
| **127.0.0.1 exclusivo** | Los puertos solo se exponen en localhost, sin acceso externo |
| **Sin VM dedicada** | No requiere VMware/VirtualBox; usa el hipervisor nativo de Windows |
| **Profesional** | Misma herramienta que usan los equipos de DevOps y SRE en produccion |
| **Rapido** | WSL 2 usa el kernel Linux real, sin overhead de virtualizacion completa |
| **Reversible** | Si algo falla, solo eliminas los contenedores y listo |

---

## 3. Requisitos Previos

| Requisito | Verificacion |
|-----------|--------------|
| Windows 10 (build 19041+) o Windows 11 | `winver` en PowerShell |
| Virtualizacion habilitada en BIOS/UEFI | Task Manager > CPU > Virtualizacion: Habilitado |
| Al menos 8 GB de RAM (16 GB recomendado) | `systeminfo` |
| Al menos 25 GB de espacio libre en disco | `Get-PSDrive C` |
| Acceso a Internet para descargar imagenes Docker | `ping google.com` |

---

## 4. Paso 1: Aislamiento y Configuracion Base en Windows

### 4.1 Habilitar WSL 2

Abrir **PowerShell como Administrador** y ejecutar:

```powershell
wsl --install -d Ubuntu
```

**Si WSL no esta habilitado:**

```powershell
# Habilitar WSL
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart

# Habilitar plataforma de maquina virtual
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

# Reiniciar el equipo
Restart-Computer
```

**Despues del reinicio:**

```powershell
# Establecer WSL 2 como version por defecto
wsl --set-default-version 2

# Descargar e instalar Ubuntu
wsl --install -d Ubuntu
```

**Configurar Ubuntu (primera vez):**

```
1. Ubuntu se abre automaticamente despues de la instalacion
2. Crear usuario y contrasena (recordar estas credenciales)
3. Actualizar el sistema:
   sudo apt update && sudo apt upgrade -y
```

### 4.2 Verificar que WSL 2 esta funcionando

```powershell
# Ver version de WSL
wsl --list --verbose

# Salida esperada:
#   NAME      STATE           VERSION
# * Ubuntu    Running         2
```

> **IMPORTANTE:** Si la columna VERSION dice "1" en lugar de "2", ejecutar:
> `wsl --set-version Ubuntu 2`

### 4.3 Instalar Docker Desktop

```
1. Descargar Docker Desktop desde:
   https://www.docker.com/products/docker-desktop/

2. Ejecutar el instalador:
   - Aceptar terminos
   - Marcar: "Use WSL 2 based engine"
   - Marcar: "Add shortcut to desktop"

3. Despues de la instalacion, abrir Docker Desktop:
   - Ir a Settings > General
   - Marcar: "Use the WSL 2 based engine"
   - Ir a Settings > Resources > WSL Integration
   - Activar: Ubuntu (toggle ON)
   - Click "Apply & Restart"
```

**Verificar en PowerShell:**

```powershell
docker --version
docker compose version
```

**Verificar desde Ubuntu (WSL):**

```bash
# Abrir Ubuntu y ejecutar:
docker --version
docker compose version
```

> **Si Docker no funciona desde Ubuntu**, reiniciar Docker Desktop y verificar que la integracion con WSL esta activa en Settings > Resources > WSL Integration.

### 4.4 Regla de Aislamiento de Red

Para asegurar que los tableros no queden expuestos a la red LAN o WiFi, **siempre** mapear puertos hacia `127.0.0.1` en los archivos `docker-compose.yml`:

```yaml
# MAL - Expuesto a toda la red:
ports:
  - "8000:8000"

# BIEN - Solo en localhost:
ports:
  - "127.0.0.1:8000:8000"
```

**Verificar que los puertos estan en localhost despues del despliegue:**

```bash
# Desde Ubuntu (WSL):
ss -tlnp | grep -E "8000|8080"

# Salida esperada:
# LISTEN  0  4096  127.0.0.1:8000  0.0.0.0:*
# LISTEN  0  4096  127.0.0.1:8080  0.0.0.0:*
```

> Si la direccion dice `0.0.0.0` en lugar de `127.0.0.1`, el servicio esta expuesto a la red. Revisar el `docker-compose.yml`.

---

## 5. Paso 2: Despliegue de los Componentes

Abrir la **terminal de Ubuntu (WSL)** y ejecutar los siguientes comandos en orden.

### 5.1 CISO Assistant - GRC y Gestion de Riesgo

CISO Assistant es una plataforma open source para gestion de cumplimiento normativo, evaluacion de riesgos y politicas de seguridad. Es el "cuando de mando" del RSI.

```bash
# Clonar el repositorio
git clone --single-branch -b main https://github.com/intuitem/ciso-assistant-community.git

# Entrar al directorio
cd ciso-assistant-community

# Ejecutar el script de despliegue Docker
./docker-compose.sh
```

**Acceso en el navegador:**

```
URL: http://127.0.0.1:8000
```

**Primer login:**

```
1. Abrir http://127.0.0.1:8000 en Chrome/Firefox
2. CISO Assistant crea un usuario admin por defecto
3. Revisar la documentacion para credenciales iniciales
4. Completar el wizard de configuracion inicial
```

**Que hacer en CISO Assistant:**

```
1. Crear un marco normativo (ej: ISO 27001, NIST CSF, PCI DSS)
2. Definir activos de informacion
3. Evaluar riesgos usando la matriz de riesgos
4. Crear controles de seguridad
5. Generar reportes de cumplimiento
```

### 5.2 OWASP DefectDojo - Gestion de Vulnerabilidades

DefectDojo consolida hallazgos de multiples escaneores (Nessus, OpenVAS, Nuclei, Trivy, Burp Suite, etc.) en una sola plataforma con workflow de remediacion.

```bash
# Volver al home
cd ~

# Clonar DefectDojo
git clone https://github.com/DefectDojo/django-DefectDojo.git

# Entrar al directorio
cd django-DefectDojo

# Configurar para release estable
./docker/setEnv.sh release

# Levantar todos los servicios
docker compose up -d
```

**Obtener credenciales de admin:**

```bash
# Esperar a que los contenedores esten listos (puede tomar 1-2 minutos)
# Luego ver las credenciales:
docker compose logs initializer | grep "Admin password:"
```

Salida esperada:

```
Admin password: <contraseña_generada_aleatoriamente>
```

> **ANOTAR ESTA CONTRASENA.** Se usa solo la primera vez; despues se cambia.

**Acceso en el navegador:**

```
URL: http://127.0.0.1:8080
Usuario: admin
Contrasena: <la que aparecio en el log>
```

**Que hacer en DefectDojo:**

```
1. Cambiar contrasena de admin (Profile > Change Password)
2. Crear un "Product" (ej: "App Web Corp v1.0")
3. Crear un "Engagement" (ej: "Escaneo Trimestral Q1")
4. Importar reportes de escaneos (ver Paso 3)
5. Asignar hallazgos a miembros del equipo
6. Seguir el estado: Open > In Progress > Remediated > Verified
```

---

## 6. Paso 3: Extraer Logs e Informacion sin Interferir

Como RSI, tu rol es **recolectar evidencia y reportar**, no modificar sistemas productivos. Aqui se explican las formas seguras y profesionales de obtener datos.

### 6.1 Exportaciones Pasivas de Scanners (SAST/DAST)

El equipo de desarrollo o infraestructura debe enviarte reportes en formatos estandar. Tu rol es **importarlos en DefectDojo**, no acceder directamente a los servidores.

**Formatos que DefectDojo acepta:**

| Formato | Origen | Como obtenerlo |
|---------|--------|----------------|
| **Nessus XML (.nessus)** | Nessus Essentials/OpenVAS | Exportar desde la interfaz web del scanner |
| **SARIF** | GitHub Advanced Security / SonarQube | Descargar desde la plataforma de CI/CD |
| **JSON** | Nuclei, Trivy, OWASP ZAP | Ejecutar el scanner y guardar el output |
| **CSV** | Diversos | Exportar desde la herramienta de origen |
| **PDF** | Cualquier scanner | Descargar reporte generado |

**Proceso tipico:**

```
1. Solicitar al equipo que exporte el reporte
2. El equipo lo deposita en un share de solo lectura
3. Tu lo descargas y lo subes a DefectDojo
4. DefectDojo consolidar automaticamente los hallazgos
```

**Importar en DefectDojo:**

```
1. Ir a Engagements > Import Scan Results
2. Seleccionar el tipo de scanner (Nessus, Trivy, etc.)
3. Subir el archivo
4. DefectDojo procesa y clasifica automaticamente
5. Revisar los hallazgos importados
```

### 6.2 Consultas de Logs de Solo Lectura (SIEM / Cloud)

Si necesitas acceder a logs de servidores productivos, solicitar acceso de **rol Auditor o Security Reader**:

| Plataforma | Rol a solicitar | Que permite |
|------------|-----------------|-------------|
| **AWS** | SecurityAudit o ReadOnlyAccess | Leer CloudTrail, GuardDuty, Inspector |
| **Azure** | Security Reader | Leer Security Center, Sentinel, Defender |
| **GCP** | roles/securitycenter.viewer | Leer Security Command Center |
| **Elasticsearch** | API Token de solo lectura | Consultar indices sin modificar |
| **Splunk** | Rol "user" con permisos de busqueda | Buscar y exportar eventos |

**Si descargas logs manualmente:**

```
1. Usar SFTP seguro (nunca FTP plano)
2. Exportar en formatos .csv o .json
3. Almacenar en una carpeta local en C:\Users\<tu_usuario>\Documents\logs_auditoria\
4. NO subir a repositorios publicos ni compartidos sin cifrar
```

### 6.3 Extraccion de Logs desde Windows (WSL)

Si necesitas extraer logs del propio equipo Windows para practicar:

```powershell
# Exportar Event Log de Windows a archivo
wevtutil epl Security C:\logs_auditoria\security.evtx
wevtutil epl System C:\logs_auditoria\system.evtx
wevtutil epl Application C:\logs_auditoria\application.evtx

# Exportar como texto para analisis
Get-WinEvent -LogName Security -MaxEvents 1000 | Export-Csv C:\logs_auditoria\security.csv
```

Desde WSL, estos archivos se encuentran en:

```bash
# Los archivos de Windows estan en /mnt/c/
cat /mnt/c/logs_auditoria/security.csv | head -20
```

---

## 7. Paso 4: Datos y Logs de Ejemplo para Practicar

Para probar las plataformas sin tocar sistemas reales, usar datasets publicos y reportes de ejemplo.

### 7.1 Logs de Eventos y Ataques

#### Splunk BOTS (Boss of the SOC)

Datasets reales y masivos con trafico de red, logs de Windows Event Logs (Sysmon), autenticaciones y trafico web con ataques simulados.

```
Descarga: https://github.com/splunk/botsv3
Tamaño: ~2.5 GB
Contenido:
- Windows Event Logs (conSysmon)
- Apache/Nginx web logs
- Firewall logs
- Ataques simulados (APT, phishing, ransomware)
- Indicadores de compromiso (IOCs)
```

**Como usarlo:**

```bash
# Clonar el repositorio
git clone https://github.com/splunk/botsv3.git
ls botsv3/

# Los archivos .evtx se pueden importar en Wazuh
# Los archivos .csv se pueden importar en Elastic Stack
# Los archivos de red se pueden importar en Suricata
```

#### SecRepo (Samples of Security Related Data)

Repositorio curado de logs de Snort, firewalls, ModSecurity, PCAP y honeypots.

```
URL: https://www.secrepo.com/
Contenido:
- Snort alerts
- Firewall logs (iptables, pf)
- ModSecurity WAF logs
- PCAP files (para practicar con Wireshark)
- Honeypot logs
```

### 7.2 Vulnerabilidades y Reportes Sinteticos para DefectDojo

#### Vulnerable Web Apps (DVWA / Juice Shop)

Ejecutar una app vulnerable localmente, escanearla, y subir el reporte a DefectDojo:

```bash
# OWASP Juice Shop (app vulnerable para practicar)
docker pull bkimminich/juice-shop
docker run -d -p 127.0.0.1:3000:3000 bkimminich/juice-shop

# Acceso: http://127.0.0.1:3000
```

```bash
# Escanear Juice Shop con OWASP ZAP (si esta instalado)
# O con Nuclei (basado en templates):
docker pull projectdiscovery/nuclei
docker run -it projectdiscovery/nuclei -u http://172.17.0.2:3000 -json > report_juice_shop.json

# Escanear con Trivy (vulnerabilidades de contenedor)
docker pull aquasec/trivy
docker run aquasec/trivy image bkimminich/juice-shop > trivy_report.txt
```

#### Archivos de Muestra Incluidos en DefectDojo

Dentro del repositorio clonado de DefectDojo hay una carpeta de pruebas con escaneos de ejemplo listos para importar:

```bash
# Listar escaneos de ejemplo
ls ~/django-DefectDojo/unittests/scans/

# Contenido (varia segun version):
# - nessus/
# - trivy/
# - burp/
# - sonarqube/
# - checkmarx/
# - npm-audit/
# - qualitative/
```

**Importar un reporte de ejemplo:**

```
1. Abrir DefectDojo en http://127.0.0.1:8080
2. Crear un Product > Engagement
3. Ir a Engagements > Import Scan Results
4. Seleccionar tipo de scanner
5. Arrastrar un archivo de unittests/scans/
6. DefectDojo procesa automaticamente
7. Revisar los hallazgos clasificados
```

---

## 8. Comandos de Mantenimiento

### Detener todos los servicios

```bash
# Detener DefectDojo
cd ~/django-DefectDojo
docker compose down

# Detener CISO Assistant
cd ~/ciso-assistant-community
docker compose down
```

### Eliminar todos los datos y empezar de cero

```bash
# Eliminar contenedores, volúmenes y datos
cd ~/django-DefectDojo
docker compose down -v

cd ~/ciso-assistant-community
docker compose down -v

# Eliminar imagenes descargadas (opcional, libera espacio)
docker system prune -a
```

### Ver estado de los servicios

```bash
# Ver contenedores corriendo
docker ps

# Ver logs en tiempo real
docker compose logs -f

# Ver uso de recursos
docker stats
```

### Actualizar las plataformas

```bash
# Actualizar CISO Assistant
cd ~/ciso-assistant-community
git pull
./docker-compose.sh

# Actualizar DefectDojo
cd ~/django-DefectDojo
git pull
docker compose up -d --build
```

---

## 9. Arquitectura del Entorno

```
+----------------------------------------------------------+
|                 WINDOWS 10/11 (Host)                     |
|                                                          |
|  +---------------------------------------------------+  |
|  |              WSL 2 (Ubuntu)                        |  |
|  |                                                    |  |
|  |  +------------------+   +------------------+      |  |
|  |  | CISO Assistant   |   |  DefectDojo      |      |  |
|  |  | :8000            |   |  :8080           |      |  |
|  |  | (GRC + Riesgos)  |   |  (Vuln Mgmt)     |      |  |
|  |  +------------------+   +------------------+      |  |
|  |           |                    |                   |  |
|  |           +----> 127.0.0.1 <---+                  |  |
|  |                  (localhost)                       |  |
|  +---------------------------------------------------+  |
|                                                          |
|  Navegador Chrome/Firefox                                |
|  http://127.0.0.1:8000  --> CISO Assistant              |
|  http://127.0.0.1:8080  --> DefectDojo                  |
|                                                          |
+----------------------------------------------------------+

Red: NO EXPUESTA - todos los servicios en 127.0.0.1
```

---

## 10. Flujo de Trabajo del RSI

```
1. RECIBIR reportes de escaneos (Nessus, Trivy, ZAP, etc.)
         |
2. IMPORTAR en DefectDojo
         |
3. CONSOLIDAR y CLASIFICAR hallazgos
         |
4. CONSULTAR EPSS + CISA KEV para priorizar
         |
5. ASIGNAR a los equipos de remediacion
         |
6. SEGUIR progreso en CISO Assistant
         |
7. GENERAR reportes ejecutivos para direccion
```

---

## 11. Solucion de Problemas Comunes

| Problema | Causa | Solucion |
|----------|-------|----------|
| `wsl --install` no funciona | Windows anterior a build 19041 | Actualizar Windows o habilitar manualmente WSL |
| Docker no inicia en WSL | Integracion no activada | Settings > Resources > WSL Integration > ON en Ubuntu |
| Puerto ya en uso | Otro servicio usando el puerto | `netstat -ano | findstr :8000` y terminar el proceso |
| `docker compose` no funciona | Version antigua de Docker | Actualizar Docker Desktop a ultima version |
| Contenedor no accede a internet | Proxy corporativo | Configurar proxy en Docker: Settings > Resources > Proxies |
| Credenciales de DefectDojo olvidadas | -- | `docker compose logs initializer \| grep "Admin password:"` |
| WSL ocupa mucho espacio | Imagenes Docker acumuladas | `docker system prune -a` |

---

## 12. Referencias

| Recurso | URL |
|---------|-----|
| WSL 2 Documentation | https://learn.microsoft.com/en-us/windows/wsl/ |
| Docker Desktop | https://www.docker.com/products/docker-desktop/ |
| CISO Assistant | https://github.com/intuitem/ciso-assistant-community |
| OWASP DefectDojo | https://github.com/DefectDojo/django-DefectDojo |
| OWASP Juice Shop | https://github.com/juice-shop/juice-shop |
| Splunk BOTS v3 | https://github.com/splunk/botsv3 |
| SecRepo | https://www.secrepo.com/ |
| OWASP ZAP | https://www.zaproxy.org/ |
| Nuclei | https://github.com/projectdiscovery/nuclei |
| Trivy | https://github.com/aquasecurity/trivy |

---

## 13. Glosario

| Termino | Definicion |
|---------|------------|
| **WSL 2** | Windows Subsystem for Linux 2, kernel Linux real corriendo en Windows |
| **Docker** | Plataforma de contenedores para empaquetar y ejecutar aplicaciones |
| **Container** | Unidad aislada de software que incluye todo lo necesario para ejecutarse |
| **GRC** | Gobernanza, Riesgo y Cumplimiento (Governance, Risk, Compliance) |
| **SIEM** | Sistema de Gestion de Eventos e Informacion de Seguridad |
| **HIDS** | Sistema de Deteccion de Intrusiones basado en Host |
| **IDS** | Sistema de Deteccion de Intrusiones (Intrusion Detection System) |
| **FIM** | Monitoreo de Integridad de Archivos (File Integrity Monitoring) |
| **SAST** | Analisis Estatico de Seguridad en Codigo Fuente |
| **DAST** | Analisis Dinamico de Seguridad en Aplicaciones |
| **EPSS** | Sistema de Puntuacion de Probabilidad de Explotacion |
| **CISA KEV** | Catalogo de Vulnerabilidades Explotadas Conocidas |
| **CVSS** | Sistema de Puntuacion de Vulnerabilidades Comunes |
| **RSI** | Recursos de Seguridad de la Informacion |
| **CSV** | Valores Separados por Comas (formato de datos) |
| **SARIF** | Static Analysis Results Interchange Format |
| **PCAP** | Paquete capturado (Packet Capture) |
| **APT** | Amenaza Persistente Avanzada (Advanced Persistent Threat) |
| **C2** | Command and Control (servidor de comando y control de malware) |
| **IOC** | Indicador de Compromiso (Indicator of Compromise) |

---

**Fin del documento**
