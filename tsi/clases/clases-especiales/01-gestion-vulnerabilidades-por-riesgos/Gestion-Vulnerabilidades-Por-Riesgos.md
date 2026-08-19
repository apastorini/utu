# Gestion de Vulnerabilidades Basada en Riesgo (RBVM)

## Guia Completa para el Responsable de Seguridad de la Informacion (RSI)

---

## 1. Introduccion: El Cambio de Paradigma

### Que es RBVM?

La **Gestion de Vulnerabilidades Basada en Riesgo (Risk-Based Vulnerability Management - RBVM)** representa un cambio fundamental en la forma en que las organizaciones identifican, priorizan y remedian las vulnerabilidades de seguridad.

A diferencia del enfoque tradicional que dependia unicamente de la severidad teorica (CVSS), RBVM integra multiples fuentes de datos para priorizar las vulnerabilidades segun el riesgo real que representan para la organizacion.

### Por que es necesario este cambio?

El modelo tradicional presentaba problemas criticos:

- **Sobrecarga de alertas**: El estandar CVSS mide el impacto teorico y la complejidad tecnica, pero no indica si un atacante realmente esta intentando explotarla en el mundo real.

- **Falsas urgencias**: Priorizar un CVSS 9.8 de un servicio aislado sin exploits conocidos puede consumir recursos que deberian usarse en un CVSS 7.5 que ya esta siendo explotado activamente.

- **Desalineacion con el negocio**: Las organizaciones no pueden parchear todo; necesitan enfocarse en lo que realmente importa.

---

## 2. Gestion de Vulnerabilidades Tradicional: El Modelo Clasico

### 2.1 Que es la Gestion de Vulnerabilidades Tradicional?

La gestion tradicional de vulnerabilidades es un enfoque basado unicamente en la **severidad tecnica** de las vulnerabilidades para determinar el orden de remediacion. Su base fundamental es el sistema de puntuacion CVSS (Common Vulnerability Scoring System), que asigna un valor numerico del 0.0 al 10.0 segun el impacto teorico de la vulnerabilidad.

### 2.2 Caracteristicas del Modelo Tradicional

| Caracteristica | Descripcion |
|----------------|-------------|
| **Criterio unico** | Solo se usa CVSS para priorizar |
| **Enfoque reactivo** | Se parchea despues de que se publica un CVE |
| **Sin contexto** | No considera si el activo es critico o esta expuesto |
| **Sin inteligencia** | No consulta si la vulnerabilidad esta siendo explotada |
| **Lista plana** | Todas las vulnerabilidades "altas" se tratan igual |

### 2.3 Flujo del Proceso Tradicional

```
+-------------------------------------------------------------------+
|              FLUJO DE GESTION TRADICIONAL                          |
+-------------------------------------------------------------------+
|                                                                   |
|  1. ESCANEO                                                       |
|     '- Se ejecuta scanner (ej: Nessus, Qualys)                    |
|                          |                                        |
|  2. REPORTE                                                       |
|     '- Se genera listado de vulnerabilidades con CVSS              |
|                          |                                        |
|  3. PRIORIZACION (solo CVSS)                                      |
|     +-- Critico (9.0-10.0) -> Parchear primero                   |
|     +-- Alto (7.0-8.9)     -> Parchear despues                   |
|     +-- Medio (4.0-6.9)    -> Cuando haya tiempo                 |
|     +-- Bajo (0.1-3.9)     -> Ignorar o diferir                  |
|                          |                                        |
|  4. REMEDIACION                                                   |
|     '- Se aplican parches en el orden definido                    |
|                          |                                        |
|  5. FIN                                                           |
|     '- Se repite el ciclo en el proximo escaneo                   |
|                                                                   |
+-------------------------------------------------------------------+
```

### 2.4 Problemas Detallados del Modelo Tradicional

#### Problema 1: Sobrecarga de Alertas (Alert Fatigue)

**Situacion tipica:**
- Un escaneo de una red empresarial mediana puede generar **5,000 a 20,000 vulnerabilidades**
- El equipo de TI tiene capacidad limitada para aplicar parches
- Se genera "fatiga de alertas" donde se ignoran todas las alertas por igual

**Consecuencia:**
- Las vulnerabilidades realmente peligrosas se pierden en el ruido
- El equipo se desmotiva y deja de confiar en las herramientas de seguridad

#### Problema 2: Priorizacion Desalineada con la Realidad

**Ejemplo concreto:**

| Vulnerabilidad | CVSS | Situacion Real | Prioridad Tradicional |
|----------------|------|----------------|----------------------|
| CVE-2024-1234 en servidor de archivos interno | 9.8 | No tiene exploits conocidos, servidor no expuesto a Internet | **ALTA** (por CVSS) |
| CVE-2024-5678 en servidor web publico | 7.5 | Siendo explotada activamente, EPSS 0.85, en CISA KEV | **MEDIA** (por CVSS) |

**Resultado:** Se parchea primero el servidor interno (riesgo bajo) y se ignora el servidor web (riesgo alto).

#### Problema 3: Ausencia de Contexto del Negocio

El modelo tradicional no responde preguntas criticas:
- Este servidor almacena datos de clientes?
- Este sistema es critico para las operaciones del negocio?
- Cuanto costaria una hora de inactividad de este activo?
- Esta expuesto directamente a Internet?

#### Problema 4: No Distingue entre Amenazas Reales y Teoricas

**Dos vulnerabilidades con CVSS 9.0:**
- Una tiene exploits disponibles, esta siendo usada por ransomware, aparece en CISA KEV
- Otra fue descubierta por un investigador en un laboratorio, sin exploits publicos

**En el modelo tradicional:** Ambas tienen la misma prioridad. En RBVM, la primera se parchea en horas; la segunda puede esperar.

### 2.5 Comparativa: Tradicional vs. RBVM

| Aspecto | Tradicional (Solo CVSS) | RBVM (CVSS + EPSS + KEV + Contexto) |
|---------|------------------------|--------------------------------------|
| **Criterio de priorizacion** | Severidad teorica | Riesgo real para el negocio |
| **Fuentes de datos** | Solo NVD/CVSS | NVD + EPSS + KEV + Inteligencia + Contexto |
| **Velocidad de remediacion** | Lenta y uniforme | Rapida para amenazas reales |
| **Eficiencia del equipo** | Baja (mucho ruido) | Alta (enfocado en lo importante) |
| **Reduccion de riesgo** | Limitada | Significativa |
| **Visibilidad ejecutiva** | Metricas tecnicas | Metricas de negocio |
| **Costo operativo** | Alto (parcheo innecesario) | Optimizado |

### 2.6 Por Que Muchas Organizaciones Siguen con el Modelo Tradicional?

1. **Inercia:** "Siempre lo hemos hecho asi"
2. **Falta de conocimiento:** No conocen EPSS ni CISA KEV
3. **Herramientas limitadas:** Algunos scanners comerciales no integran EPSS
4. **Falta de personal:** No hay recursos para implementar un proceso mas complejo
5. **Falsa sensacion de seguridad:** "Parcheamos todo lo critico" no significa que se parchee lo realmente peligroso

---

## 3. La Tridada Moderna de Priorizacion

RBVM se basa en tres pilares fundamentales para la toma de decisiones:

### 3.1 CVSS (Common Vulnerability Scoring System) - Severidad / Impacto

**Que es:** Sistema de puntuacion estandar que mide la gravedad de una vulnerabilidad.

**Que mide:**
- Impacto en confidencialidad
- Impacto en integridad
- Impacto en disponibilidad
- Complejidad de explotacion
- Autenticacion requerida
- Vector de ataque

**Rango:** 0.0 a 10.0

**Limitaciones:**
- Es estatico y teorico
- No considera el contexto del activo
- No indica si existe explotacion activa
- No refleja la probabilidad de ataque

**Uso en RBVM:** Como linea base de severidad, pero NUNCA como unico criterio de decision.

### 3.2 EPSS (Exploit Prediction Scoring System) - Probabilidad Predictiva

**Que es:** Modelo estadistico que calcula la probabilidad de que una vulnerabilidad sea explotada publicamente en los proximos 30 dias.

**Que mide:**
- Probabilidad de explotacion activa (0 a 1, o 0% a 100%)
- Basado en datos historicos de explotaciones
- Actualizado regularmente

**Rango:** 0.0 a 1.0 (0% a 100%)

**Uso en RBVM:**
- EPSS > 0.5 (50%): Alta probabilidad de explotacion -> Prioridad maxima
- EPSS > 0.3 (30%): Probabilidad significativa -> Prioridad alta
- EPSS < 0.05 (5%): Baja probabilidad -> Prioridad baja/media

**Ejemplo practico:**
- Vulnerabilidad A: CVSS 9.8, EPSS 0.02 (poco probable que sea explotada)
- Vulnerabilidad B: CVSS 7.5, EPSS 0.85 (muy probable que sea explotada)
- **Decision:** Vulnerabilidad B tiene prioridad sobre A a pesar de tener menor CVSS.

### 3.3 CISA KEV (Known Exploited Vulnerabilities) - Realidad / Explotacion Activa

**Que es:** Catalogo oficial del CISA (Cybersecurity and Infrastructure Security Agency) que lista vulnerabilidades con evidencia confirmada de ataques reales en curso.

**Que contiene:**
- Vulnerabilidades confirmadas como explotadas activamente
- Fechas de descubrimiento y confirmacion
- Fechas limite de remediacion (Binding Operational Directives)
- Referencias a exploits publicos

**Importancia:**
- Es la fuente de autoridad para vulnerabilidades explotadas activamente
- Las BOD (Binding Operational Directives) son obligatorias para agencias federales de EE.UU., pero son referencia mundial
- Actualizacion frecuente

**Uso en RBVM:**
- Si esta en CISA KEV -> Parchear inmediato (0-24 horas)
- No importa el CVSS si esta confirmado como explotado activamente

---

## 4. Matriz Practica de Decision

### Tabla de Priorizacion

| Escenario | CISA KEV | EPSS | CVSS | Accion Recomendada |
|-----------|----------|------|------|-------------------|
| **Urgencia critica** | En catalogo | Alto (> 0.5) | Cualquier nivel | Parchear de inmediato (0-24 h) |
| **Amenaza inminente** | No | Alto (> 0.3) | Alto / Critico | Prioridad alta (ciclo acelerado) |
| **Riesgo latente** | No | Muy bajo (< 0.05) | Critico (9+) | Parchear en ventana regular o aplicar controles compensatorios |
| **Ruido de fondo** | No | Muy bajo | Bajo / Medio | Monitorear / diferir |

### Factores Contextuales Adicionales

Ademas de la tridada CVSS-EPSS-CISA KEV, se debe considerar:

1. **Exposicion del activo:**
   - Esta expuesto directamente a Internet?
   - Esta detras de firewall/WAF?
   - Es accesible solo desde la red interna?

2. **Criticidad del negocio:**
   - Que datos almacena/procesa?
   - Que servicios dependen de este activo?
   - Cual es el impacto economico de su caida?

3. **Controles existentes:**
   - Hay controles compensatorios implementados?
   - Se puede segmentar la red?
   - Se puede deshabilitar temporalmente el servicio afectado?

---

## 5. Rol del RSI en RBVM

### 5.1 Responsabilidades Principales

El Responsable de Seguridad de la Informacion debe:

1. **Establecer el proceso:**
   - Definir politicas de gestion de vulnerabilidades
   - Establecer SLAs de remediacion segun el nivel de riesgo
   - Crear el equipo multidisciplinario (seguridad, TI, negocio)

2. **Orquestar la recopilacion de datos:**
   - Configurar y mantener scanners de vulnerabilidades
   - Integrar feeds de inteligencia de amenazas
   - Mantener actualizado el inventario de activos

3. **Priorizar y comunicar:**
   - Aplicar la matriz de decision
   - Comunicar prioridades a los equipos de TI
   - Reportar metricas a la direccion

4. **Supervisar la remediacion:**
   - Seguimiento del cumplimiento de SLAs
   - Verificacion de parches aplicados
   - Documentacion de excepciones y controles compensatorios

### 5.2 Flujo de Trabajo del RSI

```
+---------------------------------------------------------------+
|                    FLUJO RBVM DEL RSI                         |
+---------------------------------------------------------------+
|                                                               |
|  1. DESCUBRIMIENTO                                            |
|     +-- Escaneo de vulnerabilidades (Nessus, OpenVAS, etc.)   |
|     +-- Inventario de activos                                 |
|     +-- Identificacion de activos criticos                    |
|                          |                                    |
|  2. ENRIQUECIMIENTO                                           |
|     +-- Consulta EPSS (modelo predictivo)                     |
|     +-- Consulta CISA KEV (explotacion activa)                |
|     +-- Consulta feeds de inteligencia                        |
|     +-- Contexto del activo (critico, expuesto, etc.)         |
|                          |                                    |
|  3. PRIORIZACION                                              |
|     +-- Aplicar matriz de decision                            |
|     +-- Asignar nivel de prioridad (P1, P2, P3, P4)           |
|     +-- Definir SLA de remediacion                            |
|                          |                                    |
|  4. COMUNICACION                                              |
|     +-- Notificar a equipos de TI                             |
|     +-- Reportar a direccion                                  |
|     +-- Documentar decisiones                                 |
|                          |                                    |
|  5. REMEDIACION                                               |
|     +-- Aplicacion de parches                                 |
|     +-- Implementacion de controles compensatorios            |
|     +-- Verificacion de efectividad                           |
|                          |                                    |
|  6. VERIFICACION Y REPORTING                                  |
|     +-- Re-escaneo para confirmar remediacion                 |
|     +-- Metricas de cumplimiento                              |
|     +-- Lecciones aprendidas                                  |
|                                                               |
+---------------------------------------------------------------+
```

---

## 6. Sitios y Fuentes de Informacion Importantes

### 6.1 Fuentes Oficiales de Vulnerabilidades

| Sitio | URL | Propuesto | Frecuencia |
|-------|-----|-----------|------------|
| **NIST NVD** | https://nvd.nist.gov/ | Base de datos oficial de CVEs con puntuaciones CVSS | Diaria |
| **CISA KEV** | https://www.cisa.gov/known-exploited-vulnerabilities-catalog | Vulnerabilidades confirmadas como explotadas activamente | Semanal |
| **MITRE CVE** | https://cve.mitre.org/ | Repositorio oficial de CVEs | Continua |
| **US-CERT** | https://www.cisa.gov/uscert | Alertas de seguridad del gobierno de EE.UU. | Continua |
| **ENISA** | https://www.enisa.europa.eu/ | Agencia de ciberseguridad de la UE | Continua |

### 6.2 Fuentes de Inteligencia de Amenazas

| Sitio | URL | Propuesto | Tipo |
|-------|-----|-----------|------|
| **VirusTotal** | https://www.virustotal.com/ | Analisis de malware y URLs maliciosas | Gratuito (limitado) |
| **AlienVault OTX** | https://otx.alienvault.com/ | Pulse de amenazas de la comunidad | Gratuito |
| **MISP** | https://www.misp-project.org/ | Plataforma de sharing de indicadores | Open Source |
| **Abuse.ch** | https://abuse.ch/ | Datos de malware, C2, URLs maliciosas | Gratuito |
| **Shodan** | https://www.shodan.io/ | Buscador de dispositivos IoT/expuestos | Freemium |
| **Censys** | https://censys.io/ | Busqueda de certificados y dispositivos | Freemium |

### 6.3 Fuentes de EPSS y Probabilidad de Explotacion

| Sitio | URL | Propuesto |
|-------|-----|-----------|
| **FIRST EPSS** | https://www.first.org/epss/ | Modelo oficial de prediccion de explotacion |
| **EPSS API** | https://api.first.org/data/v1/epss | API para consultas automatizadas |
| **NVD + EPSS** | https://nvd.nist.gov/ (integrado) | CVSS + EPSS en un solo lugar |

### 6.4 Scanners de Vulnerabilidades (Software Libre o Gratuito)

| Herramienta | URL | Plataforma | Costo | Ventajas |
|-------------|-----|------------|-------|----------|
| **OpenVAS/Greenbone** | https://www.greenbone.net/ | Linux | 100% open source | Scanner completo, sin limites de IPs |
| **Nessus Essentials** | https://www.tenable.com/products/nessus/nessus-essentials | Windows/Linux | Gratuito (hasta 16 IPs) | Fácil de usar, plugins actualizados |
| **Nmap + NSE** | https://nmap.org/ | Windows/Linux | 100% open source | Escaneo de red y scripts |
| **Nuclei** | https://github.com/projectdiscovery/nuclei | Windows/Linux | 100% open source | Basado en templates, comunidad activa |
| **Trivy** | https://github.com/aquasecurity/trivy | Windows/Linux | 100% open source | Analisis de contenedores, integracion CI/CD |

### 6.5 Plataformas de Gestion y Dashboard

| Herramienta | URL | Tipo | Plataforma | Uso Principal |
|-------------|-----|------|------------|---------------|
| **DefectDojo** | https://defectdojo.org/ | Open Source | Windows/Linux (Docker) | Gestion de hallazgos de seguridad |
| **TheHive** | https://thehive-project.org/ | Open Source | Windows/Linux (Docker) | Gestion de incidentes |
| **Grafana OSS** | https://grafana.com/ | Open Source | Windows/Linux | Visualizacion y dashboards |
| **Elastic Stack** | https://www.elastic.co/ | Free tier | Windows/Linux | SIEM, busqueda, visualizacion |
| **MISP** | https://www.misp-project.org/ | Open Source | Linux | Sharing de indicadores |

---

## 7. Dashboard Paso a Paso con Software Libre

> **Importante:** Esta guia incluye instrucciones para **Windows** y **Linux** por separado. Todas las herramientas listadas son **gratuitas de forma permanente** (sin periodo de prueba ni licencias temporales). Elija la guia segun su sistema operativo.

### 7.1 Arquitectura del Dashboard

```
+-----------------------------------------------------------------------+
|                    ARQUITECTURA RBVM DASHBOARD (COMPLETA)              |
+-----------------------------------------------------------------------+
|                                                                       |
|  +----------+   +----------+   +----------+   +-----------+          |
|  | SCANNER  |   |   NVD    |   | CISA KEV |   |  SURICATA |          |
|  | (Escaneo)|   |  (CVSS)  |   |(Explotado)|   |  (Red IDS)|          |
|  +----+-----+   +----+-----+   +----+-----+   +-----+-----+          |
|       |               |              |               |                |
|       +---------------+--------------+---------------+                |
|                              |                                        |
|                   +-------------------+                              |
|                   |    DEFECTDOJO     |                              |
|                   | (Consolidacion    |                              |
|                   |  de hallazgos)    |                              |
|                   +--------+----------+                              |
|                            |                                         |
|              +-------------+-------------+                           |
|              |                           |                           |
|    +-------------------+      +-------------------+                 |
|    |    ELASTIC STACK  |      |      GRAFANA      |                 |
|    |  (Indexacion y    |      |   (Dashboard      |                 |
|    |   busqueda)       |      |   visualizacion)  |                 |
|    +-------------------+      +-------------------+                 |
|                                                                       |
|  CAPAS DE SEGURIDAD EN ENDPOINTS:                                    |
|                                                                       |
|  +------------------+  +------------------+  +------------------+    |
|  |     CLAMAV       |  |      YARA        |  |      WAZUH       |    |
|  | (Anti-Malware    |  | (Deteccion de    |  | (HIDS + FIM +    |    |
|  |  Open Source)    |  |  patrones)       |  |  Anti-Ransomware)|    |
|  +------------------+  +------------------+  +------------------+    |
|                                   |                  |               |
|                                   |     +-----------+-------+       |
|                                   |     |  SYSMON (Windows) |       |
|                                   |     +-------------------+       |
|                                                                       |
+-----------------------------------------------------------------------+
```

### 7.2 Resumen de Herramientas por Plataforma

| Componente | Linux | Windows |
|------------|-------|---------|
| **Scanner de vulnerabilidades** | OpenVAS/Greenbone (100% open source) | Nessus Essentials (gratuito, hasta 16 IPs) |
| **Deteccion de intrusiones de red (IDS)** | Suricata (open source, completo) | Suricata (instalador nativo) |
| **Anti-Malware** | ClamAV (open source, sin limites) | ClamWin/ClamAV (frontend gratuito) |
| **Deteccion de patrones de malware** | YARA (open source) | YARA (binario portable) |
| **HIDS + Anti-Ransomware** | Wazuh Manager + Agent | Wazuh Agent + Sysmon |
| **Gestion de hallazgos** | DefectDojo (Docker) | DefectDojo (Docker Desktop) |
| **SIEM + Indexacion** | Elastic Stack (paquetes .tar.gz) | Elastic Stack (instaladores .msi) |
| **Dashboard/Visualizacion** | Grafana OSS (paquete .deb) | Grafana OSS (instalador .msi) |

> **Nota sobre Windows:** OpenVAS no tiene instalador nativo para Windows. En Windows se usa **Nessus Essentials** que es gratuito para hasta 16 IPs activas (suficiente para laboratorios y clases). Para escaneos de mayor alcance, se puede ejecutar OpenVAS en una VM Linux o en WSL2.

---

### Paso 1: Instalar Scanner de Vulnerabilidades

---

#### Opcion A: Linux - Instalar OpenVAS/Greenbone

OpenVAS es 100% open source y funciona exclusivamente en Linux.

##### Instalacion en Ubuntu/Debian

```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar dependencias
sudo apt install -y wget gnupg2 lsb-release

# Instalar Greenbone Community Edition
sudo apt update
sudo apt install -y gvm

# Configurar GVM (toma 10-30 min)
sudo gvm-setup

# Verificar instalacion
sudo gvm-check-setup

# Iniciar servicios
sudo gvm-start
```

##### Acceso por primera vez

1. Abrir navegador en `https://127.0.0.1:9392`
2. Crear usuario administrador
3. Esperar actualizacion de feeds (30-60 min la primera vez)

##### Configuracion inicial

```
1. Administration -> Feed Management -> Actualizar todos los feeds
   - NVT Feed (scripts de escaneo)
   - SCAP Feed (CVSS, CPE, OVAL)
   - CERT Feed
2. Scans -> Tasks -> Nuevo escaneo
3. Seleccionar targets -> Agregar host(s) a escanear
4. Ejecutar escaneo
```

##### Alternativa: OpenVAS en Docker (cualquier distribucion)

```bash
# Ejecutar Greenbone Community Edition en Docker
docker run -d -p 9392:9392 --name greenbone \
  -v gvmd_data:/var/lib/gvm \
  -v openvas_data:/var/lib/openvas \
  -v redis_data:/var/lib/redis \
  greenbone/greenbone-community-edition

# Acceder a https://localhost:9392
```

---

#### Opcion B: Windows - Instalar Nessus Essentials

Nessus Essentials es la version gratuita de Tenable. Es **permanente** (sin expiracion) y cubre **hasta 16 IPs activas**.

##### Paso 1: Descargar

1. Ir a `https://www.tenable.com/products/nessus/nessus-essentials`
2. Completar formulario con email institucional
3. Seleccionar version **Windows x64 (.msi)**
4. Descargar el instalador

##### Paso 2: Instalar

```
1. Ejecutarnessessentials-x.x.x-x64.msi
2. Accept License Agreement
3. Seleccionar carpeta de instalacion (default: C:\Program Files\Tenable\Nessus)
4. Click Install
5. Click Finish cuando termine
```

##### Paso 3: Configurar

```
1. Abrir navegador en https://localhost:8834
2. Accept the security warning (certificado autofirmado)
3. Crear usuario administrador
4. Seleccionar "Nessus Essentials" como tipo de escaneo
5. Ingresar codigo de activacion (llega por email)
6. Esperar descarga de plugins (10-20 min)
```

##### Paso 4: Primer escaneo

```
1. Click "New Scan"
2. Seleccionar "Basic Network Scan"
3. Name: "Primer Escaneo"
4. Target: ingresa IP o rango (ej: 192.168.1.0/24, max 16 IPs)
5. Click "Launch"
6. Esperar resultado (5-30 min segun rango)
```

##### Limitaciones de Nessus Essentials (vs OpenVAS)

| Aspecto | Nessus Essentials | OpenVAS |
|---------|-------------------|---------|
| **Costo** | Gratuito | Gratuito |
| **IPs maximas** | 16 | Ilimitadas |
| **Funciones** | Escaneo basico | Escaneo completo |
| **Plugins** | Actualizados | Actualizados |
| **Ideal para** | Laboratorios, clases | Produccion, organizaciones |

---

### Paso 2: Instalar DefectDojo (Gestion de Hallazgos)

DefectDojo corre en Docker, por lo que funciona igual en ambas plataformas.

---

#### Opcion A: Linux

##### Instalacion con Docker

```bash
# Clonar repositorio
git clone https://github.com/DefectDojo/django-DefectDojo.git
cd django-DefectDojo

# Instalar con Docker Compose
docker-compose -f docker-compose.yml up -d

# Crear usuario inicial
docker-compose exec uwsgi python manage.py createsuperuser
```

##### Configuracion inicial

```
1. Acceder a http://localhost:8080
2. Settings -> System Settings -> Configurar zona horaria y formato
3. Configuration -> Defect Dojo -> Crear Products:
   - "Produccion"
   - "Desarrollo"
4. Crear Engagement (ej: "Escaneo Mensual")
```

##### Importar resultados de OpenVAS

```
1. Engagement -> Import Scan Results
2. Formato: "Greenbone (OpenVAS) CSV"
3. Subir archivo CSV exportado de OpenVAS
4. DefectDojo consolidara automaticamente los hallazgos
```

---

#### Opcion B: Windows

##### Requisito previo: Instalar Docker Desktop

1. Descargar Docker Desktop: `https://www.docker.com/products/docker-desktop/`
2. Ejecutar instalador
3. Seguir asistente (activar WSL2 si se ofrece)
4. Reiniciar si se solicita
5. Abrir Docker Desktop y verificar que este corriendo (icono en barra de tareas)

##### Instalacion de DefectDojo

```powershell
# Abrir PowerShell como Administrador

# Clonar repositorio
git clone https://github.com/DefectDojo/django-DefectDojo.git
cd django-DefectDojo

# Instalar con Docker Compose
docker-compose -f docker-compose.yml up -d

# Crear usuario inicial
docker-compose exec uwsgi python manage.py createsuperuser
```

##### Configuracion inicial

```
1. Acceder a http://localhost:8080
2. Settings -> System Settings -> Configurar zona horaria
3. Configuration -> Defect Dojo -> Crear Products
4. Crear Engagement
```

##### Importar resultados de Nessus

```
1. Engagement -> Import Scan Results
2. Formato: "Nessus"
3. Subir archivo .nessus exportado de Nessus Essentials
4. DefectDojo consolidara los hallazgos
```

---

### Paso 3: Instalar Elastic Stack (SIEM + Indexacion)

---

#### Opcion A: Linux

```bash
# Descargar Elasticsearch
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.10.2-linux-x86_64.tar.gz
tar -xzf elasticsearch-8.10.2-linux-x86_64.tar.gz
cd elasticsearch-8.10.2

# Configurar
nano config/elasticsearch.yml
# Agregar:
# network.host: 0.0.0.0
# discovery.type: single-node

# Iniciar
./bin/elasticsearch

# En otra terminal: Descargar e instalar Logstash
wget https://artifacts.elastic.co/downloads/logstash/logstash-8.10.2-linux-x86_64.tar.gz
tar -xzf logstash-8.10.2-linux-x86_64.tar.gz

# En otra terminal: Descargar e instalar Kibana
wget https://artifacts.elastic.co/downloads/kibana/kibana-8.10.2-linux-x86_64.tar.gz
tar -xzf kibana-8.10.2-linux-x86_64.tar.gz
```

---

#### Opcion B: Windows

##### Paso 1: Instalar Elasticsearch

```
1. Descargar desde https://www.elastic.co/downloads/elasticsearch
   Seleccionar "Windows x64.zip"
2. Extraer el zip en C:\elastic\
3. Abrir PowerShell como Administrador
4. Navegar a la carpeta:
   cd C:\elastic\elasticsearch-8.10.2
5. Iniciar:
   .\bin\elasticsearch.bat
6. Verificar en http://localhost:9200
```

##### Paso 2: Instalar Logstash

```
1. Descargar desde https://www.elastic.co/downloads/logstash
   Seleccionar "Windows x64.zip"
2. Extraer en C:\elastic\
3. Crear archivo C:\elastic\logstash-8.10.2\config\logstash.conf (ver abajo)
4. Iniciar:
   .\bin\logstash.bat -f .\config\logstash.conf
```

##### Paso 3: Instalar Kibana

```
1. Descargar desde https://www.elastic.co/downloads/kibana
   Seleccionar "Windows x64.zip"
2. Extraer en C:\elastic\
3. Editar config\kibana.yml:
   server.port: 5601
   elasticsearch.hosts: ["http://localhost:9200"]
4. Iniciar:
   .\bin\kibana.bat
5. Acceder a http://localhost:5601
```

##### Archivo de configuracion Logstash

Crear `C:\elastic\logstash-8.10.2\config\logstash.conf`:

```
input {
  http {
    port => 5044
  }
}
filter {
  if [type] == "defectdojo" {
    json {
      source => "message"
    }
    date {
      match => ["date", "ISO8601"]
    }
  }
}
output {
  elasticsearch {
    hosts => ["localhost:9200"]
    index => "defectdojo-%{+YYYY.MM.dd}"
  }
}
```

---

### Paso 4: Instalar Grafana (Visualizacion)

---

#### Opcion A: Linux

```bash
# Agregar repositorio
sudo apt-get install -y apt-transport-https software-properties-common wget
wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -
echo "deb https://packages.grafana.com/oss/deb stable main" | sudo tee /etc/apt/sources.list.d/grafana.list

# Instalar
sudo apt-get update
sudo apt-get install grafana

# Iniciar servicio
sudo systemctl start grafana-server
sudo systemctl enable grafana-server
```

---

#### Opcion B: Windows

```
1. Descargar desde https://grafana.com/grafana/download?edition=oss
   Seleccionar "Windows x64.zip" o "Installer (.msi)"
2a. Si es .msi: Ejecutar instalador, seguir asistente
2b. Si es .zip: Extraer en C:\grafana\
3. Abrir PowerShell:
   Si es .msi:
     net start grafana-server
   Si es .zip:
     cd C:\grafana
     .\bin\grafana-server.exe --config=.\conf\custom.ini
4. Acceder a http://localhost:3000
5. Login: admin / admin (cambiar despues)
```

---

**Acceso (ambas plataformas):** `http://localhost:3000` (admin/admin)

### 7.6 Paso 5: Crear el Dashboard

#### Panel 1: Resumen de Vulnerabilidades por Severidad

```
Tipo de grafico: Gauge o Pie Chart
Colores:
- Critico: Rojo (#FF0000)
- Alto: Naranja (#FF8C00)
- Medio: Amarillo (#FFD700)
- Bajo: Verde (#32CD32)
```

#### Panel 2: Vulnerabilidades por EPSS

```
Tipo de grafico: Bar Chart
Eje X: Rangos de EPSS (0-0.1, 0.1-0.3, 0.3-0.5, 0.5-0.7, 0.7-1.0)
Lineas de referencia:
- Linea roja en 0.5 (Alta probabilidad)
- Linea naranja en 0.3 (Probabilidad significativa)
```

#### Panel 3: Vulnerabilidades en CISA KEV

```
Tipo de grafico: Table
Columnas: CVE ID, Titulo, Fecha KEV, CVSS, Estado, Dias desde KEV
Colores: Rojo (>24h sin parche), Amarillo (24-72h), Verde (parcheado)
```

#### Panel 4: Evolucion Temporal

```
Tipo de grafico: Time Series
Lineas: Nuevas (rojo), Parcheadas (verde), Pendientes (naranja)
```

#### Panel 5: Top 10 Activos Mas Vulnerables

```
Tipo de grafico: Bar Chart horizontal
Ordenar de mayor a menor, colorear por severidad predominante
```

#### Panel 6: SLA de Remediacion

```
Metricas: % P1 en <24h, % P2 en <7d, % P3 en <30d
Colores: >90% verde, 70-90% amarillo, <70% rojo
```

#### Panel 7: Eventos de Red - Deteccion de Anomalias (Suricata)

```
Tipo de grafico: Time Series + Table
Metricas:
- Alertas de IDS por hora/dia
- Top 10 IPs origen de alertas
- Top 10 tipos de amenaza (clasificacion Suricata)
- Trafico anomalo detectado (volumen inusual)

Colores por severidad:
- Rojo: Intrusion confirmada
- Naranja: Sospechoso alto
- Amarillo: Sospechoso medio
- Verde: Informativo
```

#### Panel 8: Deteccion de Malware (ClamAV + YARA)

```
Tipo de grafico: Gauge + Table
Metricas:
- Archivos escaneados (total)
- Archivos infectados detectados
- Archivos limpiados automaticamente
- Ultima actualizacion de firmas
- Top 10 archivos sospechosos

Colores:
- Rojo: Infeccion activa
- Verde: Sistema limpio
```

#### Panel 9: Comportamiento Anomalo y Anti-Ransomware (Wazuh)

```
Tipo de grafico: Alert Stream + Bar Chart
Metricas:
- Alertas de integridad de archivos (FIM)
- Cambios en registros criticos del sistema
- Procesos inusuales detectados
- Intentos de cifrado masivo (ransomware)
- Actividad fuera de horario laboral
- Top 10 agentes con mas alertas

Colores:
- Rojo: Intento de ransomware / cambio critico
- Naranja: Comportamiento anomalo
- Amarillo: Cambio no autorizado
- Verde: Todo normal
```

---

### 7.7 Paso 6: Escaneo de Red y Deteccion de Anomalias (Suricata)

Suricata es un motor de deteccion de intrusiones (IDS/IPS) open source que analiza el trafico de red en tiempo real. Detecta escaneos de puertos, malware, intrusions y comportamientos anomales de red.

**Que detecta:**
- Escaneo de puertos y redes
- Intentos de explotacion de vulnerabilidades
- Comunicacion con servidores C2 (Command and Control)
- Descarga de malware
- Exfiltracion de datos
- Trafico cifrado sospechoso
- Firmas de amenazas conocidas (Snort/Suricata rules)

---

#### Opcion A: Linux

##### Instalacion en Ubuntu/Debian

```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Suricata
sudo apt install -y suricata

# Descargar reglas actualizadas (OISF)
sudo suricata-update

# Verificar instalacion
suricata --build-info | grep "Suricata version"
```

##### Configuracion basica

Editar `/etc/suricata/suricata.yaml`:

```yaml
# Interfaz de red a monitorear
vars:
  address-groups:
    HOME_NET: "[192.168.0.0/16,10.0.0.0/8]"
    EXTERNAL_NET: "!$HOME_NET"

# Habilitar alertas
outputs:
  - fast:
      enabled: yes
      filename: fast.log
      append: yes
  - eve-log:
      enabled: yes
      filetype: regular
      filename: eve.json
      types:
        - alert
        - anomaly
        - http
        - dns
        - tls
        - files

# Motor de deteccion
detect:
  profile: medium
  custom-values:
    toclient-src-groups: 100
    toclient-dst-groups: 100
```

##### Ejecutar en modo IDS (monitoreo)

```bash
# Ejecutar Suricata en modo pasivo (solo detecta, no bloquea)
sudo suricata -c /etc/suricata/suricata.yaml -i eth0

# Ver alertas en tiempo real
sudo tail -f /var/log/suricata/fast.log
```

##### Ejecutar en modo IPS (bloquea automaticamente)

```bash
# Requiere NFQUEUE para bloqueo activo
sudo suricata -c /etc/suricata/suricata.yaml -i eth0 --nfqueue

# Configurar iptables para redirigir trafico
sudo iptables -A FORWARD -j NFQUEUE --queue-num 0
```

##### Ver resultados en Eve JSON

```bash
# Ver alertas en formato estructurado
sudo cat /var/log/suricata/eve.json | jq 'select(.event_type=="alert")'

# Ver anomalias de red
sudo cat /var/log/suricata/eve.json | jq 'select(.event_type=="anomaly")'

# Ver conexiones sospechosas
sudo cat /var/log/suricata/eve.json | jq 'select(.event_type=="dns")'
```

---

#### Opcion B: Windows

##### Instalacion

```
1. Descargar desde https://suricata.io/download/
   Seleccionar "Windows Installer" (.exe)
2. Ejecutar el instalador
3. Seguir asistente (default: C:\Program Files\Suricata)
4. Durante la instalacion, seleccionar componentes:
   - Suricata engine
   - Reglas base
   - Herramientas de linea de comandos
```

##### Configuracion

```
1. Navegar a C:\Program Files\Suricata\
2. Editar suricata.yaml con un editor de texto (como Administrador):
   - Cambiar vars HOME_NET por tu rango de red
   - Configurar outputs (fast.log, eve.json)
3. Descargar reglas actualizadas:
   .\suricata-update.exe
```

##### Ejecutar

```powershell
# Abrir PowerShell como Administrador

# Modo IDS (monitoreo pasivo)
cd "C:\Program Files\Suricata"
.\suricata.exe -c suricata.yaml -i "Ethernet" -v

# Ver alertas en tiempo real
Get-Content .\fast.log -Wait
```

##### Verificar reglas cargadas

```powershell
# Listar reglas activas
.\suricata.exe -c suricata.yaml --list-keywords | Select-String "alert"

# Contar reglas por clasificacion
Select-String -Path .\rules\*.rules -Pattern "^alert" | Group-Object { $_.Line -replace '.*classtype:([^;]+);.*','$1' } | Sort-Object Count -Descending
```

---

### 7.8 Paso 7: Controles Anti-Malware (ClamAV + YARA)

#### 7.8.1 ClamAV - Antivirus Open Source

ClamAV es un antivirus open source que detecta virus, malware, troyanos y otros programas maliciosos. Funciona en Windows y Linux.

---

##### Linux - Instalacion y Uso

```bash
# Instalar ClamAV
sudo apt install -y clamav clamav-daemon

# Actualizar firmas (IMPORTANTE: hacerlo antes de usar)
sudo freshclam

# Verificar actualizaciones
sudo freshclam --check-version

# Escanear un directorio completo
sudo clamscan -r /home

# Escanear y limpiar automaticamente infectados
sudo clamscan -r --remove /home

# Escanear archivos comprimidos
sudo clamscan -r --unzip /var/www

# Escanear todo el sistema (largo)
sudo clamscan -r --bell --move=/tmp/clam-infected /
```

##### Programar escaneos automaticos con cron

```bash
# Escaneo diario a las 3:00 AM
crontab -e

# Agregar linea:
0 3 * * * /usr/bin/clamscan -r --move=/var/quarantine --log=/var/log/clamav/scan-$(date +\%Y\%m\%d).log /home /var/www /tmp
```

---

##### Windows - Instalacion y Uso

```
1. Descargar ClamWin desde https://www.clamwin.com/
   (ClamAV no tiene interfaz nativa para Windows, ClamWin es el frontend gratuito)
2. Ejecutar clamwin-0.x-setup.exe
3. Seguir asistente
4. Durante instalacion, seleccionar:
   - Actualizar firmas automaticamente
   - Integrar con Explorer (click derecho -> escanear)
```

##### Escaneo desde linea de comandos (Windows)

```powershell
# Navegar a la carpeta de ClamWin
cd "C:\Program Files (x86)\ClamWin\bin"

# Escanear una carpeta
.\clamscan.exe -r "C:\Users"

# Escanear y eliminar infectados
.\clamscan.exe -r --remove "C:\Users\Downloads"

# Generar reporte
.\clamscan.exe -r --log="C:\logs\clamav-report.txt" "C:\"
```

##### Programar escaneos en Windows

```
1. Abrir Programador de Tareas (taskschd.msc)
2. Crear tarea nueva
3. Nombre: "Escaneo ClamAV Diario"
4. Trigger: Diariamente a las 3:00 AM
5. Accion: Iniciar programa
   Programa: "C:\Program Files (x86)\ClamWin\bin\clamscan.exe"
   Argumentos: -r --remove --log="C:\logs\clamav.log" "C:\Users" "C:\Windows\Temp"
6. Guardar
```

---

#### 7.8.2 YARA - Deteccion de Patrones de Malware

YARA es una herramienta de identificacion y clasificacion de malware basada en patrones de texto o binario. Es como "regex para malware".

---

##### Instalacion en Ambas Plataformas

**Linux:**
```bash
# Instalar YARA
sudo apt install -y yara

# Verificar
yara --version
```

**Windows:**
```
1. Descargar desde https://github.com/VirusTotal/yara/releases
   Seleccionar: yara-x.x.x-win64.zip
2. Extraer en C:\yara\
3. Agregar al PATH del sistema:
   - Click derecho en "Este Equipo" -> Propiedades
   - Variables de entorno -> Path -> Editar
   - Agregar: C:\yara
4. Verificar en PowerShell:
   yara --version
```

##### Crear reglas YARA

Crear archivo `malware_rules.yar`:

```
rule Ransomware_Extension_Change
{
    meta:
        description = "Detecta cambios masivos de extensiones de archivos (ransomware)"
        author = "RSI"
        date = "2026-01-01"
        severity = "critical"

    strings:
        $ext1 = ".locked" ascii nocase
        $ext2 = ".encrypted" ascii nocase
        $ext3 = ".crypto" ascii nocase
        $ext4 = ".crypted" ascii nocase
        $ext5 = ".enc" ascii nocase
        $ransom_note = "YOUR FILES HAVE BEEN ENCRYPTED" ascii nocase

    condition:
        3 of ($ext*) or $ransom_note
}

rule Suspicious_Powershell_Execution
{
    meta:
        description = "Detecta ejecucion sospechosa de PowerShell"
        author = "RSI"
        severity = "high"

    strings:
        $ps1 = "powershell.exe" ascii nocase
        $ps2 = "-enc" ascii nocase
        $ps3 = "bypass" ascii nocase
        $ps4 = "hidden" ascii nocase
        $ps5 = "downloadstring" ascii nocase
        $ps6 = "invoke-expression" ascii nocase
        $ps7 = "iex" ascii nocase

    condition:
        $ps1 and 2 of ($ps3, $ps4, $ps5, $ps6, $ps7)
}

rule Credential_Dump_Tool
{
    meta:
        description = "Detecta herramientas de extraccion de credenciales"
        author = "RSI"
        severity = "high"

    strings:
        $mimikatz = "mimikatz" ascii nocase
        $procdump = "procdump" ascii nocase
        $psexec = "psexec" ascii nocase
        $hashdump = "hashdump" ascii nocase
        $lsass = "lsass" ascii nocase

    condition:
        $mimikatz or $hashdump or ($lsass and 2 of ($procdump, $psexec))
}
```

##### Ejecutar YARA

**Linux:**
```bash
# Escanear un directorio con reglas
yara malware_rules.yar /home/user/Downloads

# Escanear archivos individuales
yara malware_rules.yar suspicious_file.exe

# Buscar recursivamente
yara -r malware_rules.yar /var/www
```

**Windows:**
```powershell
# Escanear directorio
yara malware_rules.yar "C:\Users"

# Escanear archivo especifico
yara malware_rules.yar "C:\Users\Downloads\sospechoso.exe"

# Buscar recursivamente
yara -r malware_rules.yar "C:\"
```

---

### 7.9 Paso 8: Anti-Ransomware y Comportamiento Anomalo (Wazuh)

Wazuh es una plataforma de seguridad open source que combina:
- **HIDS** (Host-based Intrusion Detection System)
- **FIM** (File Integrity Monitoring) - detecta cambios en archivos criticos
- **Comportamiento anomalo** - detecta patrones inusuales
- **Anti-ransomware** - detecta cifrado masivo de archivos
- **Cumplimiento normativo** - verifica configuraciones

**Que detecta especificamente contra ransomware:**
- Cambios masivos en extensiones de archivos
- Modificaciones en registros del sistema
- Creacion de archivos .onion o .lockbit
- Procesos que cifran archivos rapidamente
- Eliminacion de copias de seguridad (VSS)
- Actividad fuera de horario laboral

---

#### Opcion A: Linux - Wazuh Manager + Agent

##### Instalar Wazuh Manager

```bash
# Agregar repositorio Wazuh
curl -sO https://packages.wazuh.com/4.7/wazuh-key.gpg
sudo cp wazuh-key.gpg /usr/share/keyrings/wazuh-keyring.gpg

echo "deb [signed-by=/usr/share/keyrings/wazuh-keyring.gpg] https://packages.wazuh.com/4.x/apt/ stable main" | sudo tee /etc/apt/sources.list.d/wazuh.list

# Instalar
sudo apt update
sudo apt install -y wazuh-manager

# Iniciar
sudo systemctl start wazuh-manager
sudo systemctl enable wazuh-manager
```

##### Configurar deteccion de ransomware

Editar `/var/ossec/etc/ossec.conf`:

```xml
<ossec_config>
  <!-- File Integrity Monitoring -->
  <syscheck>
    <frequency>3600</frequency>
    <scan_on_start>yes</scan_on_start>
    
    <!-- Monitorear directorios criticos -->
    <directories check_all="yes" realtime="yes">/home,/root,/etc</directories>
    <directories check_all="yes" realtime="yes">/var/www,/var/lib</directories>
    
    <!-- Alertas en tiempo real -->
    <alert_new_files>yes</alert_new_files>
    
    <!-- Ignorar archivos normales -->
    <ignore>/etc/mtab</ignore>
    <ignore type="sregex">.log$|.swp$</ignore>
  </syscheck>

  <!-- Comando para ejecutar ante sospecha de ransomware -->
  <command>
    <name>firewall-drop</name>
    <executable>firewall-drop.sh</executable>
    <expect>srcip</expect>
    <timeout_allowed>yes</timeout_allowed>
  </command>

  <!-- Regla personalizada anti-ransomware -->
  <rule>
    <rule id="100100" level="12">
      <if_sid>550</if_sid>
      <match>modified</match>
      <description>ALERTA: Cambio detectado en archivo critico - posible ransomware</description>
    </rule>
  </rule>
</ossec_config>
```

##### Ver alertas

```bash
# Ver alertas en tiempo real
tail -f /var/ossec/logs/alerts/alerts.log

# Ver alertas de integridad
grep "syscheck" /var/ossec/logs/alerts/alerts.log

# Ver alertas criticas
grep "level: 12" /var/ossec/logs/alerts/alerts.log
```

---

#### Opcion B: Windows - Wazuh Agent + Sysmon

##### Instalar Wazuh Agent

```
1. Descargar desde https://packages.wazuh.com/4.x/windows/
   Seleccionar: wazuh-agent-4.x-x.msi
2. Ejecutar el instalador
3. Durante instalacion, configurar:
   - Wazuh Manager IP: [IP del servidor Wazuh]
   - Agente grupo: "windows"
4. Iniciar servicio:
   net start wazuhsvc
```

##### Instalar Sysmon (complemento para deteccion avanzada)

Sysmon es una herramienta de Microsoft que monitorea procesos, conexiones de red y cambios en archivos/registros. Wazuh lo usa para deteccion avanzada.

```
1. Descargar Sysmon desde https://docs.microsoft.com/en-us/sysinternals/downloads/sysmon
2. Descargar reglas de SwiftOnSecurity:
   https://raw.githubusercontent.com/SwiftOnSecurity/sysmon-config/master/sysmonconfig-export.xml
3. Ejecutar como Administrador:
   sysmon.exe -accepteula -i sysmonconfig-export.xml
4. Verificar:
   sysmon.exe -status
```

##### Configurar Wazuh Agent para usar Sysmon

Editar `C:\Program Files (x86)\ossec-agent\ossec.conf`:

```xml
<ossec_config>
  <!-- Integrar logs de Sysmon -->
  <localfile>
    <location>Microsoft-Windows-Sysmon/Operational</location>
    <log_format>eventchannel</log_format>
  </localfile>

  <!-- Monitorear cambios en archivos criticos -->
  <syscheck>
    <frequency>3600</frequency>
    <directories realtime="yes" check_all="yes">C:\Users</directories>
    <directories realtime="yes" check_all="yes">C:\Windows\System32\config</directories>
    <directories realtime="yes" check_all="yes">C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup</directories>
  </syscheck>
</ossec_config>
```

##### Verificar estado

```powershell
# Verificar servicio Wazuh
Get-Service wazuhsvc

# Ver logs del agente
Get-Content "C:\Program Files (x86)\ossec-agent\logs\*.log" -Tail 50

# Verificar Sysmon
Get-Service Sysmon
Get-WinEvent -LogName "Microsoft-Windows-Sysmon/Operational" -MaxEvents 10
```

---

#### 7.9.1 Reglas Anti-Ransomware Personalizadas

Crear archivo `/var/ossec/etc/rules/local_rules.xml` (Linux) o `C:\Program Files (x86)\ossec-agent\rules\local_rules.xml` (Windows):

```xml
<group name="ransomware,">
  <!-- Detectar cambio masivo de extensiones -->
  <rule id="100200" level="12">
    <if_sid>550</if_sid>
    <frequency>10</frequency>
    <timepan>60</timespan>
    <match>file</match>
    <description>RANSOMWARE: Multiples archivos modificados en 1 minuto - posible cifrado masivo</description>
    <group>ransomware,pci_dss_11.4,</group>
  </rule>

  <!-- Detectar eliminacion de copias de seguridad -->
  <rule id="100201" level="12">
    <if_sid>553</if_sid>
    <match>shadow|backup|vssadmin</match>
    <description>RANSOMWARE: Intento de eliminar copias de seguridad del sistema</description>
    <group>ransomware,</group>
  </rule>

  <!-- Detectar extensiones tipicas de ransomware -->
  <rule id="100202" level="14">
    <if_sid>550</if_sid>
    <regex>\.(locked|encrypted|crypto|crypted|enc|lockbit|ryuk|conti|darkside)$</regex>
    <description>RANSOMWARE CRITICO: Archivo con extension de ransomware detectado</description>
    <group>ransomware,critical,</group>
  </rule>

  <!-- Detectar proceso sospechoso de cifrado -->
  <rule id="100203" level="14">
    <if_sid>550</if_sid>
    <match>aes256|rsa2048|encrypt|cipher</match>
    <description>RANSOMWARE CRITICO: Proceso ejecutando operaciones de cifrado</description>
    <group>ransomware,critical,</group>
  </rule>

  <!-- Actividad fuera de horario -->
  <rule id="100204" level="8">
    <if_sid>550</if_sid>
    <time>19:00 - 07:00</time>
    <frequency>5</frequency>
    <timepan>30</timepan>
    <description>ANOMALIA: Actividad fuera de horario laboral en archivos criticos</description>
    <group>anomaly,</group>
  </rule>
</group>
```

---

### 7.10 Paso 9: Integrar Todo en el Dashboard de Grafana

#### Panels Adicionales para las Nuevas Capas

##### Panel Suricata: Alertas de Red por Hora

```
Tipo: Time Series
Fuente: Elasticsearch (indice suricata-*)
Metrica: Conteo de alertas por hour
Segmentar por: clasificacion de amenaza
```

##### Panel ClamAV: Estado de Proteccion

```
Tipo: Stat
Metricas:
- Total de archivos escaneados (ultima semana)
- Infecciones detectadas
- Ultima actualizacion de firmas
- % de sistemas protegidos
```

##### Panel Wazuh: Alertas Anti-Ransomware

```
Tipo: Alert List
Filtro: group = ransomware OR group = anomaly
Ordenar: severity DESC
Mostrar: timestamp, rule.description, agent.name, rule.level
```

##### Panel Integrado: Vista de Seguridad General

```
Tipo: Singlestat / Gauge
Metricas consolidadas:
- Vulnerabilidades criticas pendientes (Rojo/Naranja/Verde)
- Alertas de red activas
- Infecciones de malware
- Alertas de comportamiento anomalo
- Estado de todos los agentes Wazuh
```

---

### 7.11 Scripts de Integracion EPSS

```python
import requests
import json
from datetime import datetime, timedelta

def get_epss_score(cve_id):
    url = f"https://api.first.org/data/v1/epss?cve={cve_id}"
    response = requests.get(url)
    data = response.json()
    if data['data']:
        return data['data'][0]['epss']
    return None

def get_top_epss(limit=100):
    url = f"https://api.first.org/data/v1/epss?limit={limit}"
    response = requests.get(url)
    return response.json()['data']

def enrich_vulnerabilities(vuln_list):
    enriched = []
    for vuln in vuln_list:
        cve_id = vuln['cve_id']
        epss = get_epss_score(cve_id)
        vuln['epss'] = epss
        if epss and epss > 0.5:
            vuln['risk_level'] = 'CRITICO'
        elif epss and epss > 0.3:
            vuln['risk_level'] = 'ALTO'
        elif epss and epss > 0.05:
            vuln['risk_level'] = 'MEDIO'
        else:
            vuln['risk_level'] = 'BAJO'
        enriched.append(vuln)
    return enriched
```

### 7.8 Script CISA KEV

```python
import requests
from datetime import datetime

CISA_KEV_URL = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"

def get_kev_catalog():
    response = requests.get(CISA_KEV_URL)
    return response.json()

def check_cve_in_kev(cve_id, kev_catalog):
    for vuln in kev_catalog['vulnerabilities']:
        if vuln['cveID'] == cve_id:
            return {
                'in_kev': True,
                'vendor': vuln['vendorProject'],
                'product': vuln['product'],
                'vulnerability_name': vuln['vulnerabilityName'],
                'date_added': vuln['dateAdded'],
                'due_date': vuln['dueDate'],
                'known_ransomware_campaign_use': vuln['knownRansomwareCampaignUse']
            }
    return {'in_kev': False}
```

---

## 8. Metricas Clave para el Dashboard

### 8.1 Metricas de Efectividad

| Metrica | Formula | Meta |
|---------|---------|------|
| **MTTR** | Tiempo promedio entre deteccion y remediacion | P1: <24h, P2: <7d, P3: <30d |
| **% KEV remediadas a tiempo** | (KEV remediadas antes de due date / Total KEV) x 100 | 100% |
| **Cobertura de escaneo** | (Activos escaneados / Total activos) x 100 | >95% |
| **Tasa de recurrencia** | (Vulnerabilidades recurrentes / Total vulns) x 100 | <10% |
| **Vulnerabilidades por activo** | Total vulns / Total activos | Tendencia a la baja |

### 8.2 Metricas de Priorizacion

| Metrica | Descripcion |
|---------|-------------|
| **Distribucion por nivel de riesgo** | Cantidad de vulns por nivel (Critico, Alto, Medio, Bajo) |
| **EPSS Promedio** | Promedio de scores EPSS del portafolio |
| **Vulnerabilidades en KEV** | Cantidad de vulns que deben parchearse inmediatamente |
| **Ratio explotacion activa** | % de vulns con EPSS > 0.3 o en KEV |

---

## 9. Automatizacion y Orquestacion

### 9.1 Integracion CI/CD

```yaml
stages:
  - build
  - scan
  - deploy

vulnerability_scan:
  stage: scan
  script:
    - nuclei -u $TARGET_URL -t cves/ -json -o results.json
    - python scripts/enrich_with_epss.py results.json
    - python scripts/check_kev.py results.json
  only:
    - main
```

### 9.2 Notificaciones Automaticas

```python
import smtplib
from email.mime.text import MIMEText

def send_critical_alert(vuln_data):
    msg = MIMEText(f"""
    ALERTA CRITICA: Nueva vulnerabilidad detectada
    CVE: {vuln_data['cve_id']}
    Severidad: {vuln_data['severity']}
    EPSS: {vuln_data['epss']}
    En CISA KEV: {vuln_data['in_kev']}
    Accion requerida: {vuln_data['action']}
    """)
    msg['Subject'] = f"[RBVM] ALERTA CRITICA - {vuln_data['cve_id']}"
    msg['From'] = "rbvm@empresa.com"
    msg['To'] = "rsi@empresa.com"
    with smtplib.SMTP('smtp.empresa.com', 587) as server:
        server.starttls()
        server.login("rbvm@empresa.com", "password")
        server.send_message(msg)
```

---

## 10. Datos Simulados para Demostracion en Clase

> **Nota para instructores:** Si no tiene datos reales de vulnerabilidades de una organizacion, puede utilizar las siguientes fuentes de datos ficticios/simulados para crear demos completas del dashboard RBVM.

### 10.1 Por que usar datos simulados?

En un entorno de ensenanza o demostracion:
- No se cuenta con una infraestructura real de TI para escanear
- No se tienen informes de vulnerabilidades reales
- Se necesita mostrar el flujo completo de RBVM
- Se requieren metricas variadas para ilustrar distintos escenarios

Los datos simulados permiten:
- Crear dashboards completos y visualmente realistas
- Calcular metricas como MTTR, EPSS promedio, cumplimiento de SLA
- Ejercitar las herramientas (Grafana, DefectDojo, Elastic Stack)
- Ensenar a interpretar y tomar decisiones basadas en los datos

### 10.2 Fuente 1: NVD Test Data (NIST)

El NIST NVD provee datos de prueba oficiales en formato JSON que replican la estructura real del NVD.

**URL:** https://nvd.nist.gov/vuln/data-feeds

**Como usarlo:**
1. Descargar los archivos JSON feeds (son archivos historicos completos)
2. Filtrar por fecha o severidad para crear subconjuntos
3. Importar en la base de datos del dashboard

### 10.3 Fuente 2: Datos EPSS de Ejemplo

La API de EPSS permite obtener datos reales que pueden usarse como base para simulaciones.

**URL:** https://api.first.org/data/v1/epss

```bash
# Obtener las 100 vulnerabilidades con mayor EPSS (datos reales)
curl "https://api.first.org/data/v1/epss?limit=100" -o epss_sample.json
```

### 10.4 Fuente 3: CISA KEV (Datos Reales para Simulacion)

El catalogo KEV es publico y contiene datos reales.

**URL:** https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json

**Simulacion:** Puede tomar 50-100 CVEs del catalogo y asignarles estados ficticios (parcheado, pendiente, en proceso).

### 10.5 Fuente 4: Script Generador de Datos Simulados

Para una demostracion completa, puede usar este script Python que genera un dataset ficticio pero realista:

```python
import json
import random
from datetime import datetime, timedelta

# === CONFIGURACION ===
NUM_ACTIVOS = 150
NUM_VULNERABILIDADES = 800
DIAS_HISTORICO = 90

# === ACTIVOS SIMULADOS ===
def generar_activos(n):
    activos = []
    tipos = [
        {"tipo": "servidor_web", "criticidad": "alta", "expuesto_internet": True},
        {"tipo": "servidor_app", "criticidad": "alta", "expuesto_internet": False},
        {"tipo": "servidor_bd", "criticidad": "critica", "expuesto_internet": False},
        {"tipo": "estacion_trabajo", "criticidad": "media", "expuesto_internet": False},
        {"tipo": "impresora", "criticidad": "baja", "expuesto_internet": False},
        {"tipo": "firewall", "criticidad": "critica", "expuesto_internet": True},
        {"tipo": "switch", "criticidad": "media", "expuesto_internet": False},
        {"tipo": "servidorcorreo", "criticidad": "alta", "expuesto_internet": True},
        {"tipo": "nas", "criticidad": "media", "expuesto_internet": False},
    ]
    for i in range(n):
        tipo_info = random.choice(tipos)
        activos.append({
            "id": f"ASSET-{i+1:04d}",
            "hostname": f"{tipo_info['tipo']}-{i+1:03d}.empresa.local",
            "ip": f"10.0.{random.randint(1,20)}.{random.randint(1,254)}",
            "tipo": tipo_info["tipo"],
            "criticidad": tipo_info["criticidad"],
            "expuesto_internet": tipo_info["expuesto_internet"],
            "sistema_operativo": random.choice(["Ubuntu 22.04", "Windows Server 2022", "CentOS 8", "Debian 11"]),
            "ultima_actualizacion": (datetime.now() - timedelta(days=random.randint(1, 90))).strftime("%Y-%m-%d")
        })
    return activos

# === CVEs SIMULADOS ===
def generar_cves(n):
    cves = []
    patrones_cve = [
        {"cve_base": "CVE-2024", "vendor": "Apache", "producto": "HTTP Server", "tipo": "XSS", "cvss_range": (4.0, 8.5), "epss_range": (0.01, 0.85)},
        {"cve_base": "CVE-2024", "vendor": "Microsoft", "producto": "Windows", "tipo": "Privilege Escalation", "cvss_range": (5.0, 9.8), "epss_range": (0.02, 0.90)},
        {"cve_base": "CVE-2024", "vendor": "OpenSSL", "producto": "TLS", "tipo": "Information Disclosure", "cvss_range": (3.0, 7.0), "epss_range": (0.01, 0.40)},
        {"cve_base": "CVE-2024", "vendor": "Linux", "producto": "Kernel", "tipo": "Buffer Overflow", "cvss_range": (6.0, 9.5), "epss_range": (0.05, 0.75)},
        {"cve_base": "CVE-2024", "vendor": "Cisco", "producto": "IOS", "tipo": "Remote Code Execution", "cvss_range": (7.0, 10.0), "epss_range": (0.10, 0.95)},
        {"cve_base": "CVE-2024", "vendor": "VMware", "producto": "vSphere", "tipo": "Sandbox Escape", "cvss_range": (6.5, 9.0), "epss_range": (0.03, 0.60)},
        {"cve_base": "CVE-2024", "vendor": "PostgreSQL", "producto": "Server", "tipo": "SQL Injection", "cvss_range": (5.5, 9.0), "epss_range": (0.02, 0.55)},
        {"cve_base": "CVE-2024", "vendor": "WordPress", "producto": "Core", "tipo": "CSRF", "cvss_range": (3.0, 6.5), "epss_range": (0.01, 0.30)},
    ]
    kev_simulados = ["CVE-2024-3400", "CVE-2024-21762", "CVE-2024-1709", "CVE-2024-20353", "CVE-2024-23897", "CVE-2024-27198"]
    for i in range(n):
        patron = random.choice(patrones_cve)
        num_aleatorio = random.randint(1000, 9999)
        cve_id = f"{patron['cve_base']}-{num_aleatorio}"
        cvss = round(random.uniform(*patron['cvss_range']), 1)
        epss = round(random.uniform(*patron['epss_range']), 3)
        in_kev = cve_id in kev_simulados or (random.random() < 0.05)
        tiene_exploit = epss > 0.3 or in_kev or (random.random() < 0.15)
        cves.append({
            "cve_id": cve_id,
            "vendor": patron["vendor"],
            "producto": patron["producto"],
            "tipo_vulnerabilidad": patron["tipo"],
            "cvss": cvss,
            "epss": epss,
            "in_cisa_kev": in_kev,
            "tiene_exploit_conocido": tiene_exploit,
            "fecha_publicacion": (datetime.now() - timedelta(days=random.randint(30, 365))).strftime("%Y-%m-%d"),
            "descripcion": f"{patron['tipo']} en {patron['vendor']} {patron['producto']}"
        })
    return cves

# === HALLAZGOS SIMULADOS ===
def generar_hallazgos(activos, cves, num_hallazgos):
    hallazgos = []
    estados = ["pendiente", "en_proceso", "parcheado", "excepcion_aprobada", "control_compensatorio"]
    pesos = [0.30, 0.15, 0.35, 0.10, 0.10]
    for i in range(num_hallazgos):
        activo = random.choice(activos)
        cve = random.choice(cves)
        fecha_deteccion = datetime.now() - timedelta(days=random.randint(1, DIAS_HISTORICO))
        estado = random.choices(estados, weights=pesos)[0]
        if estado == "parcheado":
            dias_mttr = random.randint(1, 30)
        else:
            dias_mttr = None
        if cve["in_cisa_kev"]:
            if estado != "parcheado":
                prioridad = "P1-CRITICA"
            else:
                prioridad = "P1-CRITICA"
        elif cve["epss"] > 0.5 and cve["cvss"] >= 7.0:
            prioridad = "P1-CRITICA"
        elif cve["epss"] > 0.3 or cve["cvss"] >= 9.0:
            prioridad = "P2-ALTA"
        elif cve["epss"] > 0.05 or cve["cvss"] >= 7.0:
            prioridad = "P3-MEDIA"
        else:
            prioridad = "P4-BAJA"
        hallazgos.append({
            "id": f"VULN-{i+1:05d}",
            "activo_id": activo["id"],
            "cve_id": cve["cve_id"],
            "cvss": cve["cvss"],
            "epss": cve["epss"],
            "in_cisa_kev": cve["in_cisa_kev"],
            "criticidad_activo": activo["criticidad"],
            "expuesto_internet": activo["expuesto_internet"],
            "fecha_deteccion": fecha_deteccion.strftime("%Y-%m-%d"),
            "estado": estado,
            "prioridad_rsvm": prioridad,
            "dias_mttr": dias_mttr,
            "asignado_a": random.choice(["TI-Infra", "TI-BD", "TI-Redes", "Seguridad"])
        })
    return hallazgos

# === GENERAR DATASET COMPLETO ===
def generar_dataset_completo():
    print("Generando activos simulados...")
    activos = generar_activos(NUM_ACTIVOS)
    print("Generando CVEs simulados...")
    cves = generar_cves(NUM_VULNERABILIDADES)
    print("Generando hallazgos de escaneo...")
    hallazgos = generar_hallazgos(activos, cves, NUM_VULNERABILIDADES)
    total_vulns = len(hallazgos)
    vulns_parcheadas = sum(1 for h in hallazgos if h["estado"] == "parcheado")
    vulns_pendientes = sum(1 for h in hallazgos if h["estado"] == "pendiente")
    vulns_en_kev = sum(1 for h in hallazgos if h["in_cisa_kev"])
    mttr_values = [h["dias_mttr"] for h in hallazgos if h["dias_mttr"] is not None]
    mttr_promedio = sum(mttr_values) / len(mttr_values) if mttr_values else 0
    dist_prioridad = {}
    for h in hallazgos:
        p = h["prioridad_rsvm"]
        dist_prioridad[p] = dist_prioridad.get(p, 0) + 1
    dist_severidad = {"Critico": 0, "Alto": 0, "Medio": 0, "Bajo": 0}
    for h in hallazgos:
        if h["cvss"] >= 9.0: dist_severidad["Critico"] += 1
        elif h["cvss"] >= 7.0: dist_severidad["Alto"] += 1
        elif h["cvss"] >= 4.0: dist_severidad["Medio"] += 1
        else: dist_severidad["Bajo"] += 1
    dataset = {
        "metadata": {
            "fecha_generacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "periodo_dias": DIAS_HISTORICO,
            "total_activos": NUM_ACTIVOS,
            "total_vulnerabilidades": total_vulns
        },
        "metricas": {
            "mttr_promedio_dias": round(mttr_promedio, 1),
            "vulnerabilidades_parcheadas": vulns_parcheadas,
            "vulnerabilidades_pendientes": vulns_pendientes,
            "vulnerabilidades_en_kev": vulns_en_kev,
            "porcentaje_remediacion": round((vulns_parcheadas / total_vulns) * 100, 1),
            "distribucion_prioridad": dist_prioridad,
            "distribucion_severidad": dist_severidad
        },
        "activos": activos,
        "hallazgos": hallazgos
    }
    return dataset

if __name__ == "__main__":
    dataset = generar_dataset_completo()
    with open("rbvm_dataset_simulado.json", "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)
    print(f"\n=== RESUMEN ===")
    print(f"Activos: {dataset['metadata']['total_activos']}")
    print(f"Vulnerabilidades: {dataset['metadata']['total_vulnerabilidades']}")
    print(f"MTTR Promedio: {dataset['metricas']['mttr_promedio_dias']} dias")
    print(f"% Remediation: {dataset['metricas']['porcentaje_remediacion']}%")
    print(f"En CISA KEV: {dataset['metricas']['vulnerabilidades_en_kev']}")
    print(f"\nSeveridad: {dataset['metricas']['distribucion_severidad']}")
    print(f"Prioridad: {dataset['metricas']['distribucion_prioridad']}")
```

### 10.6 Fuente 5: Generadores de Datos en Linea

#### Mockaroo (https://www.mockaroo.com/)

Generador de datos ficticios con esquemas personalizables.

**Campos sugeridos:**

| Campo | Tipo | Ejemplo |
|-------|------|---------|
| cve_id | Custom Pattern | CVE-2024-[0-9]{4,6} |
| cvss | Number (0-10, 1 decimal) | 7.5 |
| epss | Number (0-1, 3 decimales) | 0.456 |
| severity | Custom List | Critical, High, Medium, Low |
| asset_name | Custom List | srv-web-01, srv-db-03, etc. |
| asset_ip | IP Address | 10.0.1.50 |
| status | Custom List | Pending, In Progress, Patched, Exception |
| days_open | Number (1-90) | 15 |

#### Faker (Python Library)

```python
from faker import Faker
import json

fake = Faker()

def generar_vulnerabilidades_faker(n=1000):
    vulns = []
    for _ in range(n):
        vulns.append({
            "cve_id": f"CVE-2024-{fake.random_number(digits=5)}",
            "cvss": round(fake.pyfloat(min_value=0.0, max_value=10.0), 1),
            "epss": round(fake.pyfloat(min_value=0.0, max_value=1.0), 3),
            "severity": fake.random_element(["Critical", "High", "Medium", "Low"]),
            "asset_ip": fake.ipv4(),
            "asset_hostname": fake.hostname(),
            "status": fake.random_element(["Pending", "In Progress", "Patched", "Exception"]),
            "date_found": fake.date_between(start_date="-90d", end_date="today").strftime("%Y-%m-%d"),
            "assigned_to": fake.random_element(["TI-Infra", "TI-DB", "TI-Red", "Seguridad"])
        })
    return vulns

datos = generar_vulnerabilidades_faker(1000)
with open("vulnerabilidades_faker.json", "w") as f:
    json.dump(datos, f, indent=2)
```

### 10.7 Fuente 6: CVEs Reales Cruzados con EPSS Real

```python
import requests
import json
import random

nvd_url = "https://services.nvd.nist.gov/rest/json/cves/2.0?resultsPerPage=50"
nvd_data = requests.get(nvd_url).json()

for vuln in nvd_data['vulnerabilities']:
    cve_id = vuln['cve']['id']
    epss_url = f"https://api.first.org/data/v1/epss?cve={cve_id}"
    epss_data = requests.get(epss_url).json()
    if epss_data.get('data'):
        vuln['epss'] = epss_data['data'][0]['epss']
    else:
        vuln['epss'] = 0.0
    vuln['simulated_asset'] = {
        "hostname": f"srv-{cve_id.split('-')[2]}.empresa.local",
        "criticidad": random.choice(["alta", "media", "baja"]),
        "expuesto_internet": random.choice([True, False])
    }
    vuln['simulated_status'] = random.choice(["pendiente", "en_proceso", "parcheado"])

with open("nvd_con_epss_simulado.json", "w") as f:
    json.dump(nvd_data, f, indent=2)
```

### 10.8 Resumen de Fuentes de Datos Simulados

| Fuente | Tipo | Ventaja | Ideal Para |
|--------|------|---------|------------|
| **NVD Data Feeds** | JSON/CSV | Estructura oficial del NVD | Importar en Elastic/DefectDojo |
| **EPSS API** | API REST | Datos reales de probabilidad | Enriquecer CVEs simulados |
| **CISA KEV** | JSON | Catalogo real de explotadas | Simular alertas criticas |
| **Script Generador** | Python | Control total del dataset | Demo completa desde cero |
| **Mockaroo** | Web App | Sin codigo, interfaz grafica | Generar datasets rapidos |
| **Faker** | Python Lib | Rapido y flexible | Prototipos rapidos |
| **NVD + EPSS cruzado** | API | Datos reales + simulacion | La mezcla mas realista |

---

## 11. Mejores Practicas

### 11.1 Proceso

1. **Inventario de activos primero:** No se puede proteger lo que no se conoce
2. **Escaneo regular:** Minimo semanal para activos criticos, mensual para el resto
3. **Contexto del negocio:** Siempre considerar la criticidad del activo
4. **Comunicacion constante:** Mantener informados a stakeholders
5. **Documentacion:** Registrar todas las decisiones y excepciones

### 11.2 Tecnicas

1. **No depender solo de CVSS:** Siempre cruzar con EPSS y CISA KEV
2. **Automatizar lo repetible:** Escaneos, consultas EPSS, alertas
3. **Segmentar la red:** Limitar el movimiento lateral de atacantes
4. **Controles compensatorios:** Cuando no se puede parchear inmediatamente
5. **Verificacion post-remediacion:** Siempre re-escanear despues de aplicar parches

### 11.3 Organizacionales

1. **Politica clara:** Definir SLAs por nivel de riesgo
2. **Responsabilidades asignadas:** Quien es responsable de que
3. **Escalamiento definido:** Que pasa cuando no se cumplen SLAs
4. **Metricas y reporting:** Medir y reportar regularmente
5. **Mejora continua:** Revisar y optimizar el proceso trimestralmente

---

## 12. Checklist de Implementacion RBVM

### Fase 1: Fundamentos (Semanas 1-4)

- [ ] Inventario de activos completo y actualizado
- [ ] Definicion de activos criticos
- [ ] Instalacion de scanner de vulnerabilidades
  - **Linux:** OpenVAS/Greenbone (`sudo apt install gvm`)
  - **Windows:** Nessus Essentials (descargar desde tenable.com)
- [ ] Primer escaneo completo
- [ ] Clasificacion de vulnerabilidades iniciales

### Fase 2: Enriquecimiento (Semanas 5-8)

- [ ] Integracion de feeds EPSS
- [ ] Integracion de CISA KEV
- [ ] Instalacion de DefectDojo (Docker en ambas plataformas)
- [ ] Importacion de resultados historicos
- [ ] Configuracion de alertas

### Fase 3: Visualizacion (Semanas 9-12)

- [ ] Instalacion de Elastic Stack
  - **Linux:** Paquetes .tar.gz
  - **Windows:** Paquetes .zip desde elastic.co
- [ ] Instalacion de Grafana
  - **Linux:** Paquete .deb desde repositorio
  - **Windows:** Instalador .msi o .zip desde grafana.com
- [ ] Creacion de dashboards
- [ ] Configuracion de reportes automaticos
- [ ] Capacitacion del equipo

### Fase 4: Automatizacion (Semanas 13-16)

- [ ] Scripts de enriquecimiento automatico
- [ ] Integracion con sistemas de ticketing
- [ ] Notificaciones automaticas
- [ ] Reportes ejecutivos automaticos
- [ ] Revision y optimizacion del proceso

---

## 13. Recursos Adicionales

### Documentacion Oficial

- NIST SP 800-40 - Guide to Enterprise Patch Management
- CISA Binding Operational Directive 22-01
- FIRST EPSS Documentation
- OpenVAS Documentation

### Comunidades

- OWASP (https://owasp.org/)
- SANS Institute (https://www.sans.org/)
- DefectDojo Community (https://github.com/DefectDojo/django-DefectDojo)

### Certificaciones Relacionadas

- CISSP (Certified Information Systems Security Professional)
- CEH (Certified Ethical Hacker)
- CompTIA Security+
- GIAC (Global Information Assurance Certification)

---

## 14. Glosario

### A

**Alert Fatigue (Fatiga de Alertas):** Condicion en la que los profesionales de seguridad se vuelven insensibles a las alertas debido al exceso de notificaciones, provocando que ignoren tanto alertas falsas como alertas reales criticas.

**APT (Advanced Persistent Threat - Amenaza Persistente Avanzada):** Grupo de atacantes, generalmente patrocinado por un estado-nacion, que mantiene acceso no autorizado a una red durante un periodo prolongado de tiempo.

**Asset (Activo):** Cualquier recurso de TI que tiene valor para la organizacion: servidores, estaciones de trabajo, bases de datos, aplicaciones, dispositivos de red, etc.

**Asset Criticality (Criticidad del Activo):** Nivel de importancia de un activo para las operaciones del negocio. Determina la prioridad de proteccion y remediacion.

### B

**BOD (Binding Operational Directive):** Directiva operativa vinculante emitida por el CISA que establece requisitos obligatorios para las agencias federales de EE.UU. La BOD 22-01 requiere la remediacion de vulnerabilidades en el catalogo KEV.

### C

**CISA (Cybersecurity and Infrastructure Security Agency):** Agencia del gobierno de EE.UU. encargada de la proteccion de la infraestructura critica y ciberseguridad nacional.

**CISA KEV (Known Exploited Vulnerabilities):** Catalogo oficial del CISA que lista vulnerabilidades con evidencia confirmada de explotacion activa en el mundo real.

**Compensating Control (Control Compensatorio):** Medida de seguridad alternativa implementada cuando no es posible aplicar un parche o correccion directa. Ejemplo: segmentacion de red, WAF, IPS.

**CVSS (Common Vulnerability Scoring System):** Sistema abierto de puntuacion para calificar la gravedad de las vulnerabilidades de seguridad. Rango: 0.0 a 10.0.

**CVE (Common Vulnerabilities and Exposures):** Sistema de identificacion estandar para vulnerabilidades de seguridad publicamente conocidas. Ejemplo: CVE-2024-12345.

### D

**Dashboard (Tablero de Control):** Visualizacion grafica de metricas y KPIs clave que permite a los tomadores de decisiones entender rapidamente el estado de seguridad.

**Due Date (Fecha Limite):** Fecha establecida por el CISA KEV para la remediacion de una vulnerabilidad. Generalmente 14 a 28 dias desde la fecha de adicion al catalogo.

### E

**EPSS (Exploit Prediction Scoring System):** Modelo estadistico desarrollado por FIRST que estima la probabilidad de que una vulnerabilidad sea explotada publicamente en los proximos 30 dias. Rango: 0 a 1.

**Exploit:** Codigo, tecnica o metodo que aprovecha una vulnerabilidad para obtener acceso no autorizado o ejecutar codigo malicioso.

**Exposure (Exposicion):** Grado en que un activo es accesible desde fuentes externas (Internet, red publica, etc.).

### F

**False Positive (Falso Positivo):** Alerta o hallazgo de seguridad que indica incorrectamente la existencia de una vulnerabilidad o amenaza.

**Feed (Canal de Datos):** Fuente continua de datos de seguridad que se integra automaticamente en las herramientas de gestion (ej: feed de NVD, feed de EPSS).

### G

**Grafana:** Plataforma open source de visualizacion y monitoreo que permite crear dashboards interactivos a multiples fuentes de datos.

**Greenbone/OpenVAS:** Plataforma de escaneo de vulnerabilidades open source (Open Vulnerability Assessment Scanner).

### H

**Hallazgo (Finding):** Resultado de un escaneo de seguridad que identifica una vulnerabilidad, configuracion incorrecta o debilidad en un activo.

### I

**IOC (Indicator of Compromise - Indicador de Compromiso):** Artefacto forense que indica una intrusion potencial en un sistema: IPs maliciosas, hashes de malware, dominios C2, etc.

### K

**KEV (Known Exploited Vulnerabilities):** Ver CISA KEV.

### L

**Lateral Movement (Movimiento Lateral):** Tecnica utilizada por atacantes para desplazarse a traves de una red despues de obtener acceso inicial, escalando privilegios y comprometiendo mas sistemas.

### M

**MTTR (Mean Time to Remediate):** Tiempo promedio que toma una organizacion para corregir una vulnerabilidad desde que es detectada hasta que es remediada.

**MISP (Malware Information Sharing Platform):** Plataforma open source para el sharing y distribucion de indicadores de amenazas (IOCs) entre organizaciones.

### N

**NIST (National Institute of Standards and Technology):** Instituto de estandares y tecnologia de EE.UU. que publica marcos de referencia de ciberseguridad (NIST CSF, SP 800-53, etc.).

**NVD (National Vulnerability Database):** Base de datos oficial del NIST que contiene informacion detallada sobre CVEs, incluyendo puntuaciones CVSS, configuraciones CPE y referencias.

### P

**Patch (Parche):** Actualizacion de software que corrige una o mas vulnerabilidades de seguridad.

**Penetration Testing (Prueba de Penetracion):** Evaluacion autorizada de seguridad que simula un ataque real para identificar vulnerabilidades explotables.

### R

**RBVM (Risk-Based Vulnerability Management):** Gestion de vulnerabilidades basada en riesgo. Enfoque que prioriza las vulnerabilidades segun el riesgo real usando CVSS + EPSS + CISA KEV + contexto del activo.

**Remediation (Remediacion):** Accion correctiva para eliminar o mitigar una vulnerabilidad: parche, configuracion, control compensatorio, etc.

**Risk (Riesgo):** Probabilidad de que una amenaza explote una vulnerabilidad y el impacto resultante para la organizacion. Formula: Riesgo = Amenaza x Vulnerabilidad x Impacto.

### S

**SLA (Service Level Agreement - Acuerdo de Nivel de Servicio):** Compromiso formal sobre el tiempo maximo de respuesta o remediacion. Ejemplo: P1 en 24 horas, P2 en 7 dias.

**Scanner (Escanner):** Herramienta automatizada que identifica vulnerabilidades en sistemas, redes o aplicaciones.

**SIEM (Security Information and Event Management):** Sistema que recopila, analiza y correlaciona eventos de seguridad en tiempo real para detectar amenazas.

### T

**Threat Intelligence (Inteligencia de Amenazas):** Informacion recopilada y analizada sobre amenazas de seguridad actuales, incluyendo actores, tecnicas, procedimientos e indicadores.

### V

**Vulnerability (Vulnerabilidad):** Debilidad o falla en un sistema que puede ser explotada por una amenaza para comprometer la seguridad.

**Vulnerability Assessment (Evaluacion de Vulnerabilidades):** Proceso sistematico de identificacion, clasificacion y priorizacion de vulnerabilidades en una organizacion.

### W

**WAF (Web Application Firewall):** Firewall de aplicaciones web que filtra y monitorea el trafico HTTP/HTTPS entre una aplicacion web e Internet, protegiendo contra ataques como SQL injection y XSS.

---

## 15. Conclusion

La Gestion de Vulnerabilidades Basada en Riesgo no es opcional en el panorama de ciberseguridad actual. Las organizaciones que no adopten este enfoque estaran:

1. **Sobrecargadas** de alertas que no representan riesgo real
2. **Desenfocadas** en vulnerabilidades que nunca seran explotadas
3. **Expuestas** a amenazas que si estan siendo explotadas activamente

El RSI debe liderar esta transformacion, implementando:

- **La tridada CVSS-EPSS-CISA KEV** para la priorizacion
- **Herramientas de software libre** para la automatizacion
- **Dashboards accionables** para la toma de decisiones
- **Procesos documentados** para la consistencia

La inversion en RBVM no es un costo, es una inversion en la resiliencia del negocio.

---

**Autor:** Clase Especial de TSI
**Fecha:** Agosto 2026
**Version:** 2.0
