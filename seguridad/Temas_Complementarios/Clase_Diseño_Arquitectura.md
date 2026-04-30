# Clase: Diseño de Arquitectura de Seguridad

## Desde Fundamentos hasta Arquitectura Avanzada

---

**Versión:** 1.0  
**Fecha:** Abril 2026  
**Proyecto:** Curso de Ciberseguridad

---

## Tabla de Contenidos

1. ¿Qué es Arquitectura de Seguridad?
2. Fundamentos Básicos
3. Componentes de una Arquitectura
4. Capas de Arquitectura
5. Patrones Arquitectónicos
6. Arquitectura de Red
7. Arquitectura de Seguridad Perimetral
8. DMZ y Segmentación
9. Arquitectura Cloud
10. Zero Trust Architecture
11. Microservicios y APIs
12. Contenedores y Orquestación
13. Infraestructura como Código
14. Defensa en Profundidad
15. Diseñar tu Propia Arquitectura (Guía Práctica)
16. Checklist de Arquitectura
17. Referencias y Recursos

---

## 1. ¿Qué es Arquitectura de Seguridad?

### Definición Simple

La **arquitectura de seguridad** es el **plano** que define cómo se protege un sistema informático. Es como el plano de una casa con alarmas, cerraduras y cámaras: define dónde va cada protección y cómo funcionan juntas.

### Analogía: La Casa

```
┌─────────────────────────────────────────────────────────┐
│                    ANALOGÍA DE LA CASA                  │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Elemento de Casa    →   Elemento de Seguridad          │
│                                                         │
│  Terreno con reja    →   Firewall perimetral            │
│  Puerta principal    →   Autenticación (login)          │
│  Cerradura           →   Contraseñas / MFA              │
│  Cámara de seguridad →   Logs / Monitoreo (SIEM)        │
│  Caja fuerte         →   Cifrado de datos               │
│  Habitación privada  →   Segmentación de red            │
│  Guardia de seguridad→   SOC / Equipo de seguridad      │
│  Seguro del hogar    →   Plan de recuperación           │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### ¿Por qué importa?

| Sin Arquitectura | Con Arquitectura |
|------------------|------------------|
| Protecciones al azar | Protecciones planificadas |
| Vulnerabilidades ocultas | Riesgos identificados |
| Difícil de mantener | Fácil de escalar |
| Brechas frecuentes | Defensa coordinada |

---

## 2. Fundamentos Básicos

### 2.1 La Tríada CIA (Repaso)

Toda arquitectura de seguridad protege estos tres pilares:

```
                    ┌───────────────┐
                    │ CONFIDENCIAL  │
                    │ (Solo quien   │
                    │  debe ver)    │
                    └───────┬───────┘
                            │
              ┌─────────────┼─────────────┐
              │             │             │
       ┌──────▼──────┐     │    ┌────────▼───────┐
       │ INTEGRIDAD   │     │    │ DISPONIBILIDAD │
       │ (Sin cambios │     │    │ (Accesible     │
       │  no autor.)  │     │    │  cuando se     │
       └─────────────┘     │    │  necesita)     │
                           │    └────────────────┘
```

### 2.2 Principio de Mínimo Privilegio

Cada componente del sistema solo tiene los permisos **estrictamente necesarios**.

```
❌ MAL: El servidor web puede leer la base de datos COMPLETA
✅ BIEN: El servidor web solo puede ejecutar consultas específicas
```

### 2.3 Defensa en Profundidad (Defense in Depth)

Nunca confiar en una sola protección. Múltiples capas de seguridad:

```
┌─────────────────────────────────────────────────────┐
│              DEFENSA EN PROFUNDIDAD                 │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Capa 7: Datos         → Cifrado, backup            │
│  Capa 6: Aplicación    → WAF, validación input      │
│  Capa 5: Host          → Antivirus, HIDS            │
│  Capa 4: Red Interna   → Segmentación, VLANs        │
│  Capa 3: Perímetro     → Firewall, IDS/IPS          │
│  Capa 2: Red Externa   → DDoS protection            │
│  Capa 1: Física        → Acceso al datacenter       │
│                                                     │
│  Si una capa falla, las otras siguen protegiendo.   │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### 2.4 Principio de Falla Segura (Fail Secure)

Si algo falla, el sistema debe fallar de forma **segura**:

```
❌ MAL: Si el firewall falla, permite TODO el tráfico
✅ BIEN: Si el firewall falla, bloquea TODO el tráfico
```

---

## 3. Componentes de una Arquitectura

### 3.1 Componentes Fundamentales

Todo sistema tiene estos componentes básicos:

```
┌────────────────────────────────────────────────────────┐
│               COMPONENTES BÁSICOS                      │
├────────────────────────────────────────────────────────┤
│                                                        │
│  ┌────────────┐    ┌────────────┐    ┌──────────────┐ │
│  │  CLIENTE   │───▶│  SERVIDOR  │───▶│  BASE DE     │ │
│  │  (Browser) │    │  (App)     │    │  DATOS       │ │
│  └────────────┘    └────────────┘    └──────────────┘ │
│       │                  │                    │        │
│       ▼                  ▼                    ▼        │
│  ¿Quién accede?   ¿Qué hace?          ¿Dónde se        │
│  ¿Está auten-     ¿Está autorizado?   guardan los      │
│  ticado?          ¿Es válido?         datos seguros?   │
│                                                        │
└────────────────────────────────────────────────────────┘
```

### 3.2 Componentes de Seguridad

| Componente | Función | Ejemplo |
|-----------|---------|---------|
| **Firewall** | Controla tráfico de red | iptables, AWS Security Groups |
| **WAF** | Protege aplicaciones web | Cloudflare, ModSecurity |
| **IDS/IPS** | Detecta/previene intrusiones | Snort, Suricata |
| **SIEM** | Centraliza logs y alertas | Splunk, ELK Stack |
| **Load Balancer** | Distribuye carga | Nginx, HAProxy, ALB |
| **Proxy** | Intermediario de red | Squid, Nginx reverse proxy |
| **VPN** | Conexión segura remota | OpenVPN, WireGuard |
| **PKI** | Gestión de certificados | Let's Encrypt, Active Directory CA |

---

## 4. Capas de Arquitectura

### 4.1 Modelo de 3 Capas (Básico)

El modelo más simple y común:

```
┌─────────────────────────────────────────────────────────┐
│                 ARQUITECTURA 3 CAPAS                    │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │  CAPA 1: PRESENTACIÓN (Frontend)                │   │
│  │  - Interfaz de usuario                          │   │
│  │  - HTML, CSS, JavaScript                        │   │
│  │  - React, Angular, Vue                          │   │
│  │  - NO accede directamente a la base de datos    │   │
│  └─────────────────────┬───────────────────────────┘   │
│                        │ HTTP/HTTPS                   │
│  ┌─────────────────────▼───────────────────────────┐   │
│  │  CAPA 2: LÓGICA DE NEGOCIO (Backend/API)        │   │
│  │  - Procesa las reglas del negocio               │   │
│  │  - Autenticación, autorización                  │   │
│  │  - Python, Java, Node.js, C#                    │   │
│  │  - Valida y sanitiza inputs                     │   │
│  └─────────────────────┬───────────────────────────┘   │
│                        │ Conexión BD                  │
│  ┌─────────────────────▼───────────────────────────┐   │
│  │  CAPA 3: DATOS (Database)                       │   │
│  │  - Almacena información                         │   │
│  │  - MySQL, PostgreSQL, MongoDB                   │   │
│  │  - Solo accesible desde la capa de lógica       │   │
│  │  - Cifrado en reposo                            │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 4.2 Seguridad en cada capa

```
Capa Presentación:
├── HTTPS obligatorio
├── Content Security Policy (CSP)
├── Validación en cliente (UI)
└── Protección contra XSS

Capa Lógica:
├── Autenticación (OAuth, JWT)
├── Autorización (RBAC)
├── Validación de inputs
├── Rate limiting
├── Logging
└── Protección contra inyección

Capa Datos:
├── Cifrado en reposo (AES-256)
├── Acceso solo desde backend
├── Backups cifrados
├── Auditoría de queries
└── Mínimo privilegio en cuentas BD
```

### 4.3 Modelo de N Capas (Intermedio)

Para sistemas más complejos:

```
┌─────────────────────────────────────────────────────────┐
│                 ARQUITECTURA N CAPAS                    │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  [Cliente] → [CDN] → [Load Balancer] → [API Gateway]   │
│                                                    │    │
│  ┌──────────────────────────────────────────────┐ │    │
│  │  Servicios (Microservicios)                  │ │    │
│  │  ├── Servicio de Usuarios                    │ │    │
│  │  ├── Servicio de Pagos                       │ │    │
│  │  ├── Servicio de Inventario                  │ │    │
│  │  └── Servicio de Notificaciones              │ │    │
│  └──────────────────────────────────────────────┘ │    │
│                                                    │    │
│  ┌──────────────────────────────────────────────┐ │    │
│  │  Capa de Datos                               │ │    │
│  │  ├── Cache (Redis)                           │ │    │
│  │  ├── Base de datos principal                  │ │    │
│  │  └── Data Warehouse                          │ │    │
│  └──────────────────────────────────────────────┘ │    │
│                                                    │    │
└────────────────────────────────────────────────────────┘
```

---

## 5. Patrones Arquitectónicos

### 5.1 Patrón: Monolito

Todo en un solo servidor/aplicación.

```
┌─────────────────────────────────────┐
│              MONOLITO               │
├─────────────────────────────────────┤
│                                     │
│  ┌───────────────────────────────┐ │
│  │  Servidor Web (Nginx/Apache)  │ │
│  │  ┌─────────────────────────┐  │ │
│  │  │  Aplicación Completa    │  │ │
│  │  │  ├── Autenticación      │  │ │
│  │  │  ├── Usuarios           │  │ │
│  │  │  ├── Pagos              │  │ │
│  │  │  ├── Reportes           │  │ │
│  │  │  └── Admin              │  │ │
│  │  └─────────────────────────┘  │ │
│  │  ┌─────────────────────────┐  │ │
│  │  │  Base de Datos Local    │  │ │
│  │  └─────────────────────────┘  │ │
│  └───────────────────────────────┘ │
│                                     │
│  Ventajas: Simple, fácil deploy     │
│  Desventajas: Escalar difícil,      │
│              un fallo = todo cae    │
└─────────────────────────────────────┘
```

### 5.2 Patrón: Cliente-Servidor

Separación clara entre cliente y servidor.

```
┌──────────────┐         ┌──────────────┐
│   CLIENTE    │         │   SERVIDOR   │
│  (Frontend)  │ ─HTTP─▶ │  (Backend)   │
│              │         │              │
│  - Browser   │         │  - API REST  │
│  - Móvil     │         │  - Base datos│
│  - Desktop   │         │  - Lógica    │
└──────────────┘         └──────────────┘
```

### 5.3 Patrón: Microservicios

Cada función es un servicio independiente.

```
┌─────────────────────────────────────────────────────────┐
│               MICROSERVICIOS                            │
├─────────────────────────────────────────────────────────┤
│                                                         │
│                    ┌───────────────┐                    │
│                    │  API Gateway  │                    │
│                    │  (Kong, NGINX)│                    │
│                    └───────┬───────┘                    │
│                            │                            │
│           ┌────────────────┼────────────────┐           │
│           │                │                │           │
│    ┌──────▼──────┐ ┌──────▼──────┐ ┌───────▼──────┐    │
│    │ Servicio    │ │ Servicio    │ │ Servicio     │    │
│    │ Usuarios    │ │ Pagos       │ │ Inventario   │    │
│    │             │ │             │ │              │    │
│    │ + BD propia │ │ + BD propia │ │ + BD propia  │    │
│    └─────────────┘ └─────────────┘ └──────────────┘    │
│                                                         │
│  Ventajas: Escalar independiente, fallos aislados       │
│  Desventajas: Complejo, necesita orquestación           │
└─────────────────────────────────────────────────────────┘
```

### 5.4 Patrón: Serverless

Sin servidores que administrar.

```
┌─────────────────────────────────────────────────────────┐
│                    SERVERLESS                           │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Usuario → API Gateway → Función Lambda → DynamoDB      │
│                               │                         │
│                        Función Lambda                   │
│                        (solo se ejecuta                 │
│                         cuando hay petición)            │
│                                                         │
│  Ventajas: Sin infraestructura, pago por uso            │
│  Desventajas: Cold starts, vendor lock-in               │
└─────────────────────────────────────────────────────────┘
```

---

## 6. Arquitectura de Red

### 6.1 Componentes de Red

```
┌─────────────────────────────────────────────────────────┐
│               COMPONENTES DE RED                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Internet                                               │
│      │                                                  │
│      ▼                                                  │
│  ┌──────────────────┐                                   │
│  │  Router          │  ← Enruta tráfico entre redes    │
│  └────────┬─────────┘                                   │
│           │                                             │
│  ┌────────▼─────────┐                                   │
│  │  Firewall        │  ← Filtra tráfico (reglas)       │
│  └────────┬─────────┘                                   │
│           │                                             │
│  ┌────────▼─────────┐                                   │
│  │  Switch          │  ← Conecta dispositivos internos  │
│  └────────┬─────────┘                                   │
│           │                                             │
│  ┌────────▼─────────┐  ┌──────────────┐                │
│  │  Servidor Web    │  │  Servidor BD │                │
│  │  (Público)       │  │  (Privado)   │                │
│  └──────────────────┘  └──────────────┘                │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 6.2 Topologías de Red

**Estrella (más común):**
```
         ┌─────┐
         │Switch│
         └──┬──┘
       ┌────┼────┐
       │    │    │
    ┌──┴┐ ┌─┴─┐ ┌┴──┐
    │Srv│ │PC │ │Imp│
    └───┘ └───┘ └───┘
```

**Malla (más resiliente):**
```
  ┌───┐────┬───┐
  │ A │────│ B │
  └─┬─┘    └─┬─┘
    │  ╲  ╱  │
    │   ╳    │
    │  ╱  ╲  │
  ┌─┴─┐    ┌─┴─┐
  │ C │────│ D │
  └───┘    └───┘
```

### 6.3 Protocolos Importantes

| Protocolo | Puerto | Uso | Riesgo |
|-----------|--------|-----|--------|
| HTTP | 80 | Web sin cifrar | Alto (datos en claro) |
| HTTPS | 443 | Web cifrada | Bajo |
| SSH | 22 | Acceso remoto seguro | Medio (fuerza bruta) |
| FTP | 21 | Transferencia archivos | Alto (sin cifrar) |
| SFTP | 22 | Transferencia segura | Bajo |
| DNS | 53 | Resolución nombres | Medio (DNS spoofing) |
| SMTP | 25/587 | Email | Medio (spam, phishing) |
| RDP | 3389 | Escritorio remoto | Alto (ataques frecuentes) |
| SMB | 445 | Compartición archivos | Alto (ransomware) |

---

## 7. Arquitectura de Seguridad Perimetral

### 7.1 Firewall

El primer punto de defensa:

```
┌─────────────────────────────────────────────────────────┐
│                    FIREWALL                             │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  INTERNET                    RED INTERNA                 │
│     │                            │                      │
│     │   ┌──────────────────┐    │                      │
│     ├──▶│    FIREWALL      │───▶│                      │
│     │   │                  │    │                      │
│     │   │  Reglas:         │    │                      │
│     │   │  ✅ Permitir 443 │    │                      │
│     │   │  ✅ Permitir 80  │    │                      │
│     │   │  ❌ Bloquear 445 │    │                      │
│     │   │  ❌ Bloquear 3389│    │                      │
│     │   │  ❌ Todo lo demás│    │                      │
│     │   └──────────────────┘    │                      │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 7.2 Tipos de Firewall

| Tipo | Nivel | Función | Ejemplo |
|------|-------|---------|---------|
| **Packet Filter** | Red (L3/L4) | Filtra por IP, puerto, protocolo | iptables |
| **Stateful** | Red + Estado | Recuerda conexiones establecidas | Cisco ASA |
| **Application (WAF)** | Aplicación (L7) | Inspecciona contenido HTTP | ModSecurity |
| **Next-Gen (NGFW)** | Multi-nivel | Inspección profunda, IDS integrado | Palo Alto |
| **Cloud** | Virtual | Security Groups, NACLs | AWS, Azure |

### 7.3 Reglas de Firewall (Ejemplo)

```
# Ejemplo de reglas de iptables (Linux)

# Política por defecto: BLOQUEAR todo
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT

# Permitir tráfico web (HTTP/HTTPS)
iptables -A INPUT -p tcp --dport 80 -j ACCEPT
iptables -A INPUT -p tcp --dport 443 -j ACCEPT

# Permitir SSH solo desde IP de administración
iptables -A INPUT -p tcp --dport 22 -s 10.0.1.100 -j ACCEPT

# Permitir DNS
iptables -A INPUT -p udp --dport 53 -j ACCEPT

# Permitir conexiones establecidas
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# Log y bloquear todo lo demás
iptables -A INPUT -j LOG --log-prefix "FIREWALL_DROP: "
iptables -A INPUT -j DROP
```

---

## 8. DMZ y Segmentación

### 8.1 ¿Qué es una DMZ?

**DMZ (Demilitarized Zone)** es una red intermedia entre internet y la red interna. Los servicios públicos van aquí, aislados de los datos sensibles.

```
┌─────────────────────────────────────────────────────────┐
│                    ARQUITECTURA CON DMZ                 │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────┐                                       │
│  │  INTERNET    │                                       │
│  └──────┬───────┘                                       │
│         │                                               │
│  ┌──────▼───────┐                                       │
│  │  FIREWALL 1  │  ← Firewall externo/perimetral        │
│  │  (Edge)      │                                       │
│  └──────┬───────┘                                       │
│         │                                               │
│  ╔══════════════╗                                       │
│  ║     DMZ      ║  ← Zona desmilitarizada               │
│  ║              ║                                       │
│  ║  ┌────────┐  ║                                       │
│  ║  │ Serv.  │  ║  ← Servidor Web (público)             │
│  ║  │  Web   │  ║                                       │
│  ║  └────────┘  ║                                       │
│  ║  ┌────────┐  ║                                       │
│  ║  │ Serv.  │  ║  ← Servidor Mail (público)            │
│  ║  │ Mail   │  ║                                       │
│  ║  └────────┘  ║                                       │
│  ╚══════╤═══════╝                                       │
│         │                                               │
│  ┌──────▼───────┐                                       │
│  │  FIREWALL 2  │  ← Firewall interno                   │
│  │  (Internal)  │                                       │
│  └──────┬───────┘                                       │
│         │                                               │
│  ┌──────▼───────┐                                       │
│  │  RED INTERNA │                                       │
│  │              │                                       │
│  │  ┌────────┐  │                                       │
│  │  │ BD     │  │  ← Base de datos (NUNCA en DMZ)       │
│  │  └────────┘  │                                       │
│  │  ┌────────┐  │                                       │
│  │  │ AD/LDAP│  │  ← Directorio (NUNCA en DMZ)          │
│  │  └────────┘  │                                       │
│  └──────────────┘                                       │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 8.2 Reglas de DMZ

| Desde | Hacia | Permitido | Razón |
|-------|-------|-----------|-------|
| Internet | DMZ | Solo 80, 443 | Servidor web público |
| Internet | Red Interna | NUNCA | Aislamiento total |
| DMZ | Internet | Solo respuestas | Respuestas a peticiones |
| DMZ | Red Interna | Solo BD (puerto específico) | El web necesita datos |
| Red Interna | DMZ | Sí | Admin de servidores |
| Red Interna | Internet | Sí (con proxy) | Navegación controlada |

### 8.3 Segmentación de Red

Dividir la red en zonas aisladas:

```
┌─────────────────────────────────────────────────────────┐
│              SEGMENTACIÓN DE RED                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │  VLAN 10    │  │  VLAN 20    │  │  VLAN 30    │     │
│  │  Usuarios   │  │  Servidores │  │  IoT/OT     │     │
│  │  10.0.10.0  │  │  10.0.20.0  │  │  10.0.30.0  │     │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘     │
│         │                │                │             │
│         └────────────────┼────────────────┘             │
│                          │                             │
│                   ┌──────▼──────┐                       │
│                   │   Core      │                       │
│                   │   Switch    │                       │
│                   │   + FW      │                       │
│                   └─────────────┘                       │
│                                                         │
│  Reglas entre VLANs:                                    │
│  - Usuarios → Servidores: Solo puertos necesarios       │
│  - Usuarios → IoT: BLOQUEADO                            │
│  - IoT → Servidores: Solo MQTT/protocolo específico     │
│  - Servidores → Usuarios: Solo respuestas               │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 9. Arquitectura Cloud

### 9.1 Modelo Compartido de Responsabilidad

En la nube, la seguridad es **compartida**:

```
┌─────────────────────────────────────────────────────────┐
│         RESPONSABILIDAD COMPARTIDA EN LA NUBE            │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌───────────────────────────────────────────────────┐ │
│  │  IaaS (EC2, VMs)                                  │ │
│  │                                                   │ │
│  │  Proveedor: Seguridad DE la nube                  │ │
│  │  - Hardware, red física, hipervisor               │ │
│  │  ┌─────────────────────────────────────────────┐ │ │
│  │  │  Cliente: Seguridad EN la nube              │ │ │
│  │  │  - SO, apps, datos, configuraciones         │ │ │
│  │  │  - Firewall, cifrado, IAM                   │ │ │
│  │  └─────────────────────────────────────────────┘ │ │
│  └───────────────────────────────────────────────────┘ │
│                                                         │
│  ┌───────────────────────────────────────────────────┐ │
│  │  PaaS (RDS, App Service)                          │ │
│  │                                                   │ │
│  │  Proveedor: + SO, runtime, middleware             │ │
│  │  ┌─────────────────────────────────────────────┐ │ │
│  │  │  Cliente: + Apps, datos, configuraciones    │ │ │
│  │  └─────────────────────────────────────────────┘ │ │
│  └───────────────────────────────────────────────────┘ │
│                                                         │
│  ┌───────────────────────────────────────────────────┐ │
│  │  SaaS (Gmail, Salesforce)                         │ │
│  │                                                   │ │
│  │  Proveedor: Casi todo                             │ │
│  │  ┌─────────────────────────────────────────────┐ │ │
│  │  │  Cliente: Datos, acceso, políticas          │ │ │
│  │  └─────────────────────────────────────────────┘ │ │
│  └───────────────────────────────────────────────────┘ │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 9.2 Arquitectura AWS de 3 Tier

```
┌─────────────────────────────────────────────────────────┐
│           ARQUITECTURA AWS 3 TIER                       │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │  VPC (Virtual Private Cloud)                    │   │
│  │                                                 │   │
│  │  ┌─────────────────┐  ┌─────────────────┐      │   │
│  │  │  Public Subnet  │  │  Private Subnet │      │   │
│  │  │  (DMZ)          │  │  (App)          │      │   │
│  │  │                 │  │                 │      │   │
│  │  │  ┌───────────┐  │  │  ┌───────────┐  │      │   │
│  │  │  │   ALB     │  │  │  │   EC2     │  │      │   │
│  │  │  │ (Balance- │  │  │  │  (App     │  │      │   │
│  │  │  │  ader)    │  │  │  │   Server) │  │      │   │
│  │  │  └─────┬─────┘  │  │  └─────┬─────┘  │      │   │
│  │  │        │        │  │        │        │      │   │
│  │  └────────┼────────┘  └────────┼────────┘      │   │
│  │           │                    │                │   │
│  │  ┌────────▼────────────────────▼────────┐       │   │
│  │  │         Private Subnet               │       │   │
│  │  │         (Database)                   │       │   │
│  │  │                                      │       │   │
│  │  │  ┌───────────┐  ┌───────────┐       │       │   │
│  │  │  │    RDS    │  │  Elasti-  │       │       │   │
│  │  │  │  (MySQL)  │  │  Cache    │       │       │   │
│  │  │  └───────────┘  │  (Redis)  │       │       │   │
│  │  │                 └───────────┘       │       │   │
│  │  └──────────────────────────────────────┘       │   │
│  │                                                 │   │
│  │  Internet Gateway → Nat Gateway                 │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  Security Groups (Firewall virtual por instancia):      │
│  - ALB: Permite 80, 443 desde 0.0.0.0/0                │
│  - EC2: Permite 8080 solo desde ALB                    │
│  - RDS: Permite 3306 solo desde EC2                    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 9.3 Arquitectura Azure

```
┌─────────────────────────────────────────────────────────┐
│              ARQUITECTURA AZURE                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │  Azure Virtual Network (VNet)                   │   │
│  │                                                 │   │
│  │  ┌─────────────┐  ┌─────────────┐              │   │
│  │  │  Subnet Web │  │ Subnet App  │              │   │
│  │  │             │  │             │              │   │
│  │  │  ┌───────┐  │  │  ┌───────┐  │              │   │
│  │  │  │App    │  │  │  │App    │  │              │   │
│  │  │  │Gateway│  │  │  │Service│  │              │   │
│  │  │  └───┬───┘  │  │  └───┬───┘  │              │   │
│  │  └──────┼──────┘  └──────┼──────┘              │   │
│  │         │                │                      │   │
│  │  ┌──────▼────────────────▼──────┐               │   │
│  │  │  Subnet Database             │               │   │
│  │  │                              │               │   │
│  │  │  ┌──────────┐  ┌──────────┐  │               │   │
│  │  │  │Azure SQL │  │  Redis   │  │               │   │
│  │  │  │  Cache   │  │  Cache   │  │               │   │
│  │  │  └──────────┘  └──────────┘  │               │   │
│  │  └──────────────────────────────┘               │   │
│  │                                                 │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  Azure Firewall → NSG (Network Security Groups)        │
│  Application Gateway → WAF                             │
│  Azure AD → Identidad y acceso                         │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 10. Zero Trust Architecture

### 10.1 ¿Qué es Zero Trust?

**"Nunca confíes, siempre verifica."**

No importa si la conexión viene de dentro o fuera de la red: **toda** petición debe ser autenticada y autorizada.

```
┌─────────────────────────────────────────────────────────┐
│            TRADICIONAL vs ZERO TRUST                    │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  TRADICIONAL (Castle-and-Moat):                         │
│  ┌─────────────────────────────────────┐               │
│  │  ┌───────┐                          │               │
│  │  │FIRE-  │  Todo dentro = confianza │               │
│  │  │WALL   │  ┌────┐ ┌────┐ ┌────┐   │               │
│  │  │       │  │ Srv│ │ PC │ │ PC │   │               │
│  │  └───────┘  └────┘ └────┘ └────┘   │               │
│  │     ▲                               │               │
│  │     │ Si entras, tienes acceso a    │               │
│  │     │ TODO                          │               │
│  └─────┼───────────────────────────────┘               │
│        │                                              │
│  ZERO TRUST:                                          │
│  ┌─────────────────────────────────────┐               │
│  │  ┌────┐    ┌────┐    ┌────┐        │               │
│  │  │Srv │    │ PC │    │ PC │        │               │
│  │  │ 🔒 │    │ 🔒 │    │ 🔒 │        │               │
│  │  └────┘    └────┘    └────┘        │               │
│  │   ↑         ↑         ↑             │               │
│  │  Cada recurso requiere              │               │
│  │  autenticación individual           │               │
│  └─────────────────────────────────────┘               │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 10.2 Pilares de Zero Trust

| Pilar | Descripción | Implementación |
|-------|-------------|----------------|
| **Identidad** | Verificar quién eres | MFA, SSO, Identity Provider |
| **Dispositivos** | Verificar el equipo | Endpoint management, compliance |
| **Red** | Segmentar todo | Micro-segmentación, SASE |
| **Aplicaciones** | Controlar acceso | API Gateway, WAF |
| **Datos** | Proteger la información | Cifrado, DLP, clasificación |
| **Visibilidad** | Monitorear todo | SIEM, analytics, automation |

### 10.3 Arquitectura Zero Trust

```
┌─────────────────────────────────────────────────────────┐
│              ZERO TRUST ARCHITECTURE                    │
├─────────────────────────────────────────────────────────┤
│                                                         │
│                    ┌─────────────────┐                  │
│                    │   Policy Engine │                  │
│                    │   (PDP)         │                  │
│                    │  ┌───────────┐  │                  │
│                    │  │ Evaluar:  │  │                  │
│                    │  │ - Identidad│  │                  │
│                    │  │ - Device  │  │                  │
│                    │  │ - Contexto│  │                  │
│                    │  │ - Riesgo  │  │                  │
│                    │  └───────────┘  │                  │
│                    └────────┬────────┘                  │
│                             │ Decisión                  │
│                    ┌────────▼────────┐                  │
│  Solicitud ──────▶│  Policy Admin   │                  │
│  del usuario      │  Point (PAP)    │                  │
│                   │                 │                  │
│                   │  ✅ Permitir     │                  │
│                   │  ❌ Denegar      │                  │
│                   │  ⚠  Step-up MFA │                  │
│                   └────────┬────────┘                  │
│                            │                          │
│                   ┌────────▼────────┐                  │
│                   │  Enforcement    │                  │
│                   │  Point (PEP)    │                  │
│                   │  (Proxy/Gateway)│                  │
│                   └────────┬────────┘                  │
│                            │                          │
│                   ┌────────▼────────┐                  │
│                   │  Recurso        │                  │
│                   │  (App/Data/Srv) │                  │
│                   └─────────────────┘                  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 10.4 Implementación Práctica

```
Fase 1: Identificar
├── Catalogar todos los activos
├── Mapear flujos de datos
├── Identificar datos sensibles
└── Documentar accesos actuales

Fase 2: Proteger
├── Implementar MFA en todo
├── Segmentar la red
├── Cifrar datos sensibles
└── Implementar PAM (Privileged Access)

Fase 3: Monitorear
├── Centralizar logs (SIEM)
├── Detectar anomalías
├── Automated response
└── Continuous verification

Fase 4: Optimizar
├── Automated policy enforcement
├── Risk-based access
├── Continuous improvement
└── Threat intelligence integration
```

---

## 11. Microservicios y APIs

### 11.1 Arquitectura de Microservicios

```
┌─────────────────────────────────────────────────────────┐
│              MICROSERVICIOS + API GATEWAY               │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │  CLIENTE (Web/Móvil)                            │   │
│  └──────────────────────┬──────────────────────────┘   │
│                         │                              │
│  ┌──────────────────────▼──────────────────────────┐   │
│  │  API GATEWAY                                    │   │
│  │  ├── Autenticación (JWT, OAuth)                 │   │
│  │  ├── Rate Limiting                              │   │
│  │  ├── Routing                                    │   │
│  │  ├── Logging                                    │   │
│  │  └── SSL Termination                            │   │
│  └──────────┬────────────┬────────────┬──────────┘   │
│             │            │            │               │
│  ┌──────────▼──┐  ┌─────▼─────┐  ┌───▼──────────┐   │
│  │ Servicio    │  │ Servicio  │  │ Servicio     │   │
│  │ Usuarios    │  │ Pagos     │  │ Inventario   │   │
│  │             │  │           │  │              │   │
│  │ ┌─────────┐ │  │ ┌───────┐ │  │ ┌──────────┐ │   │
│  │ │  BD     │ │  │ │  BD   │ │  │ │   BD     │ │   │
│  │ │Usuarios │ │  │ │Pagos  │ │  │ │Inventario│ │   │
│  │ └─────────┘ │  │ └───────┘ │  │ └──────────┘ │   │
│  └─────────────┘  └───────────┘  └──────────────┘   │
│                                                         │
│  Cada servicio:                                         │
│  ├── Tiene su propia base de datos                     │
│  ├── Se comunica por API REST o gRPC                   │
│  ├── Se despliega independientemente                   │
│  └── Puede fallar sin afectar a los demás              │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 11.2 Seguridad en APIs

| Protección | Implementación |
|-----------|----------------|
| **Autenticación** | OAuth 2.0, JWT, API Keys |
| **Autorización** | Scopes, RBAC, ABAC |
| **Rate Limiting** | X requests per minute |
| **Input Validation** | Schema validation, sanitización |
| **CORS** | Orígenes permitidos |
| **HTTPS** | TLS obligatorio |
| **Logging** | Request/response audit |

### 11.3 API Gateway - Configuración de Seguridad

```yaml
# Ejemplo: Kong API Gateway - Configuración de seguridad

# Rate Limiting
plugins:
  - name: rate-limiting
    config:
      minute: 100        # 100 requests por minuto
      policy: local
      limit_by: ip

# Autenticación JWT
  - name: jwt
    config:
      claims_to_verify:
        - exp            # Verificar expiración

# IP Restriction
  - name: ip-restriction
    config:
      allow:
        - 10.0.0.0/8     # Solo red interna

# Bot Detection
  - name: bot-detection
    config:
      allow:
        - googlebot
        - bingbot
      deny:
        - bad-bot

# Request Size Limit
  - name: request-size-limiting
    config:
      allowed_payload_size: 1  # 1 MB máximo
```

---

## 12. Contenedores y Orquestación

### 12.1 Contenedores (Docker)

```
┌─────────────────────────────────────────────────────────┐
│                    CONTENEDORES                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │  Host (Sistema Operativo)                       │   │
│  │                                                 │   │
│  │  ┌─────────────┐ ┌─────────────┐ ┌───────────┐ │   │
│  │  │ Contenedor 1│ │ Contenedor 2│ │ Contenedor│ │   │
│  │  │ ┌─────────┐ │ │ ┌─────────┐ │ │ 3         │ │   │
│  │  │ │  App    │ │ │ │  App    │ │ │ ┌───────┐ │ │   │
│  │  │ │ + Libs  │ │ │ │ + Libs  │ │ │ │  App  │ │ │   │
│  │  │ └─────────┘ │ │ └─────────┘ │ │ └───────┘ │ │   │
│  │  └─────────────┘ └─────────────┘ └───────────┘ │   │
│  │                                                 │   │
│  │  Container Runtime (Docker/containerd)          │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  vs Máquinas Virtuales:                                 │
│  - Más ligero (comparte kernel del host)               │
│  - Inicio más rápido                                   │
│  - Menos overhead                                      │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 12.2 Seguridad en Contenedores

| Riesgo | Mitigación |
|--------|-----------|
| Imagen con vulnerabilidades | Escanear con Trivy, Snyk |
| Contenedor como root | Ejecutar como usuario no-root |
| Secretos expuestos | Usar Docker Secrets, Vault |
| Red sin aislar | Network policies |
| Recursos ilimitados | CPU/Memory limits |

### 12.3 Dockerfile Seguro

```dockerfile
# ❌ INSEGURO
FROM ubuntu:latest
COPY . /app
RUN chmod 777 /app
CMD ["python", "app.py"]

# ✅ SEGURO
# Usar imagen específica (no latest)
FROM python:3.11-slim

# Crear usuario no-root
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copiar solo lo necesario
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=appuser:appuser . /app
WORKDIR /app

# Ejecutar como usuario no-root
USER appuser

# No usar puertos privilegiados (<1024)
EXPOSE 8080

CMD ["python", "app.py"]
```

### 12.4 Kubernetes - Arquitectura

```
┌─────────────────────────────────────────────────────────┐
│                 KUBERNETES CLUSTER                      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────────────────┐                            │
│  │  Control Plane (Master) │                            │
│  │                         │                            │
│  │  ┌───────────┐          │                            │
│  │  │ API Server│  ← Punto de entrada                  │
│  │  └─────┬─────┘          │                            │
│  │        │                │                            │
│  │  ┌─────▼─────┐ ┌──────▼──────┐                      │
│  │  │ etcd      │ │ Scheduler   │                      │
│  │  │ (Estado)  │ │ (Distribuye)│                      │
│  │  └───────────┘ └─────────────┘                      │
│  │                         │                            │
│  │  ┌──────────────────────▼──────┐                    │
│  │  │  Controller Manager         │                    │
│  │  │  (Mantiene estado deseado)  │                    │
│  │  └─────────────────────────────┘                    │
│  └─────────────────────────┘                            │
│                                                         │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐    │
│  │   Worker 1   │ │   Worker 2   │ │   Worker 3   │    │
│  │              │ │              │ │              │    │
│  │ ┌──────────┐ │ │ ┌──────────┐ │ │ ┌──────────┐ │    │
│  │ │ Pod 1    │ │ │ │ Pod 3    │ │ │ │ Pod 5    │ │    │
│  │ │ Pod 2    │ │ │ │ Pod 4    │ │ │ │ Pod 6    │ │    │
│  │ └──────────┘ │ │ └──────────┘ │ │ └──────────┘ │    │
│  │              │ │              │ │              │    │
│  │ kubelet      │ │ kubelet      │ │ kubelet      │    │
│  └──────────────┘ └──────────────┘ └──────────────┘    │
│                                                         │
│  Security en Kubernetes:                                │
│  ├── RBAC (quién puede hacer qué)                      │
│  ├── Network Policies (tráfico entre pods)             │
│  ├── Pod Security Standards                            │
│  ├── Secrets management                                │
│  └── Service Accounts                                  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 12.5 Network Policies en Kubernetes

```yaml
# Solo el frontend puede comunicarse con el backend
# El backend solo puede comunicarse con la BD

apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: backend-policy
spec:
  podSelector:
    matchLabels:
      app: backend
  policyTypes:
    - Ingress
    - Egress
  ingress:
    # Solo pods con label app=frontend pueden conectarse
    - from:
        - podSelector:
            matchLabels:
              app: frontend
      ports:
        - protocol: TCP
          port: 8080
  egress:
    # Solo puede conectarse a la base de datos
    - to:
        - podSelector:
            matchLabels:
              app: database
      ports:
        - protocol: TCP
          port: 5432
    # Permitir DNS
    - to: []
      ports:
        - protocol: UDP
          port: 53
```

---

## 13. Infraestructura como Código (IaC)

### 13.1 ¿Qué es IaC?

Definir infraestructura en código en lugar de configurarla manualmente.

```
Antes (Manual):                    Ahora (IaC):
┌──────────────────┐               ┌──────────────────┐
│ 1. Crear VM en   │               │ 1. Escribir código│
│    consola AWS   │               │    Terraform      │
│ 2. Configurar FW │               │                  │
│    manualmente   │               │ 2. terraform apply│
│ 3. Instalar SW   │               │    (automático)   │
│ 4. Configurar red│               │                  │
│                  │               │ Reproducible,     │
│ Problema: No es  │               │ versionable,      │
│ reproducible     │               │ auditable         │
└──────────────────┘               └──────────────────┘
```

### 13.2 Terraform - Ejemplo de Infraestructura Segura

```hcl
# main.tf - Infraestructura AWS segura

# VPC con subnets públicas y privadas
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name        = "secure-vpc"
    Environment = "production"
  }
}

# Security Group restrictivo
resource "aws_security_group" "web" {
  name        = "web-sg"
  description = "Security group for web servers"
  vpc_id      = aws_vpc.main.id

  # Solo permitir HTTPS desde internet
  ingress {
    description = "HTTPS from internet"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # SSH solo desde IP de administración
  ingress {
    description = "SSH from admin IP"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["10.0.1.100/32"]  # IP específica
  }

  # No permitir HTTP (redirigir a HTTPS)
  # ingress para puerto 80 NO existe

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# S3 Bucket cifrado
resource "aws_s3_bucket" "data" {
  bucket = "mi-empresa-datos-prod"

  # Cifrado obligatorio
  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "aws:kms"
      }
    }
  }

  # Bloquear acceso público
  public_access_block_configuration {
    block_public_acls       = true
    block_public_policy     = true
    ignore_public_acls      = true
    restrict_public_buckets = true
  }

  # Logging de accesos
  logging {
    target_bucket = "mi-empresa-logs"
    target_prefix = "s3-access-logs/"
  }
}
```

### 13.3 Herramientas IaC

| Herramienta | Lenguaje | Uso |
|-------------|----------|-----|
| **Terraform** | HCL | Multi-cloud |
| **CloudFormation** | YAML/JSON | AWS |
| **ARM Templates** | JSON/JSON | Azure |
| **Pulumi** | Python, TS, Go | Multi-cloud |
| **Ansible** | YAML | Configuración |

---

## 14. Defensa en Profundidad - Arquitectura Completa

### 14.1 Arquitectura Empresarial Completa

```
┌─────────────────────────────────────────────────────────────────┐
│              ARQUITECTURA DE SEGURIDAD COMPLETA                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  CAPA 1: PERÍMETRO EXTERNO                                      │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  DNS Protection (Cloudflare/AWS Route53)                │   │
│  │  ├── DNSSEC habilitado                                  │   │
│  │  ├── DDoS protection                                    │   │
│  │  └── WAF (Web Application Firewall)                     │   │
│  └─────────────────────┬───────────────────────────────────┘   │
│                        │                                       │
│  CAPA 2: RED PERIMETRAL                                         │
│  ┌─────────────────────▼───────────────────────────────────┐   │
│  │  Next-Gen Firewall (NGFW)                               │   │
│  │  ├── IPS/IDS                                          │   │
│  │  ├── Deep Packet Inspection                           │   │
│  │  └── Geo-blocking                                     │   │
│  └─────────────────────┬───────────────────────────────────┘   │
│                        │                                       │
│  CAPA 3: DMZ                                                  │
│  ┌─────────────────────▼───────────────────────────────────┐   │
│  │  Load Balancer + API Gateway                            │   │
│  │  ├── SSL Termination                                    │   │
│  │  ├── Rate Limiting                                      │   │
│  │  ├── Authentication (OAuth/JWT)                         │   │
│  │  └── Routing to services                                │   │
│  └─────────────────────┬───────────────────────────────────┘   │
│                        │                                       │
│  CAPA 4: APLICACIÓN                                             │
│  ┌─────────────────────▼───────────────────────────────────┐   │
│  │  Microservicios (Containerizado)                        │   │
│  │  ├── Service Mesh (mTLS)                                │   │
│  │  ├── Input Validation                                   │   │
│  │  ├── RBAC por servicio                                  │   │
│  │  └── Secrets Management (Vault)                         │   │
│  └─────────────────────┬───────────────────────────────────┘   │
│                        │                                       │
│  CAPA 5: DATOS                                                  │
│  ┌─────────────────────▼───────────────────────────────────┐   │
│  │  Bases de Datos + Storage                               │   │
│  │  ├── Cifrado en reposo (AES-256)                        │   │
│  │  ├── Cifrado en tránsito (TLS 1.3)                      │   │
│  │  ├── Access Control estricto                            │   │
│  │  └── Backup cifrado + inmutable                         │   │
│  └─────────────────────┬───────────────────────────────────┘   │
│                        │                                       │
│  CAPA 6: MONITOREO (TRANSVERSAL)                                │
│  ┌─────────────────────▼───────────────────────────────────┐   │
│  │  SIEM + SOC                                             │   │
│  │  ├── Logs centralizados                                 │   │
│  │  ├── Detección de anomalías (ML)                        │   │
│  │  ├── Automated Response (SOAR)                          │   │
│  │  └── Threat Intelligence                                │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 15. Diseñar tu Propia Arquitectura (Guía Práctica)

### 15.1 Paso 1: Entender los Requisitos

Antes de diseñar, responde:

| Pregunta | Ejemplo de respuesta |
|----------|---------------------|
| ¿Qué protege la arquitectura? | Una aplicación web de e-commerce |
| ¿Qué datos maneja? | Datos personales, tarjetas de crédito |
| ¿Cuántos usuarios? | 10,000 concurrentes |
| ¿Disponibilidad requerida? | 99.9% (8.76h de downtime/año) |
| ¿Compliance? | PCI-DSS, GDPR |
| ¿Presupuesto? | Medio (cloud optimizado) |

### 15.2 Paso 2: Identificar Activos

```
Activos a proteger:
├── Datos de usuarios (emails, contraseñas, direcciones)
├── Datos de pago (tarjetas de crédito)
├── Código fuente de la aplicación
├── Base de datos de productos
└── Logs del sistema
```

### 15.3 Paso 3: Modelar Amenazas (STRIDE)

| Amenaza | Impacto | Mitigación |
|---------|---------|------------|
| **S**poofing (suplantación) | Acceso no autorizado | MFA, certificados |
| **T**ampering (manipulación) | Datos alterados | Firmas digitales, hash |
| **R**epudiation (negación) | No se puede auditar | Logs inmutables |
| **I**nformation Disclosure | Fuga de datos | Cifrado, DLP |
| **D**enial of Service | Servicio caído | Rate limiting, CDN |
| **E**levation of Privilege | Acceso admin | Mínimo privilegio, RBAC |

### 15.4 Paso 4: Diseñar la Arquitectura

```
Ejemplo: Arquitectura para E-Commerce

┌─────────────────────────────────────────────────────────┐
│                                                         │
│  Internet                                               │
│      │                                                  │
│      ▼                                                  │
│  ┌──────────────────┐                                   │
│  │  Cloudflare CDN  │  ← DDoS protection, WAF           │
│  └────────┬─────────┘                                   │
│           │                                             │
│  ┌────────▼─────────┐                                   │
│  │  ALB (AWS)       │  ← Load Balancing, SSL            │
│  └────────┬─────────┘                                   │
│           │                                             │
│  ┌────────▼─────────────────────────────┐               │
│  │  ECS/EKS (Contenedores)              │               │
│  │                                      │               │
│  │  ┌──────────┐ ┌──────────┐ ┌──────┐ │               │
│  │  │ Frontend │ │   API    │ │ Admin│ │               │
│  │  │ (React)  │ │ Gateway  │ │ Panel│ │               │
│  │  └──────────┘ └────┬─────┘ └──────┘ │               │
│  │                    │                 │               │
│  │  ┌─────────────────┼──────────────┐ │               │
│  │  │  ┌──────┐ ┌────▼────┐ ┌─────┐ │ │               │
│  │  │  │ Cat. │ │  Pagos  │ │Users│ │ │               │
│  │  │  │ álogo│ │ Service │ │ Srv │ │ │               │
│  │  │  └──────┘ └────┬────┘ └─────┘ │ │               │
│  │  │                │              │ │               │
│  │  │  ┌─────────────▼──────────┐   │ │               │
│  │  │  │  Redis Cache           │   │ │               │
│  │  │  └────────────────────────┘   │ │               │
│  │  └───────────────────────────────┘ │               │
│  └──────────────────┬──────────────────┘               │
│                     │                                  │
│  ┌──────────────────▼──────────────────┐               │
│  │  Private Subnet (Database)          │               │
│  │                                      │               │
│  │  ┌──────────────┐ ┌──────────────┐  │               │
│  │  │  RDS MySQL   │ │  S3 Buckets  │  │               │
│  │  │  (Cifrado)   │ │  (Cifrado)   │  │               │
│  │  └──────────────┘ └──────────────┘  │               │
│  └──────────────────────────────────────┘               │
│                                                         │
│  Monitoring (transversal):                               │
│  ├── CloudWatch (métricas)                              │
│  ├── CloudTrail (auditoría)                             │
│  └── GuardDuty (threat detection)                       │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 15.5 Paso 5: Documentar

Crear un documento que incluya:

1. **Diagrama de arquitectura** (como el de arriba)
2. **Flujo de datos** (cómo viajan los datos)
3. **Puntos de seguridad** (dónde está cada protección)
4. **Controles de acceso** (quién puede acceder a qué)
5. **Plan de recuperación** (qué hacer si algo falla)

### 15.6 Paso 6: Validar

| Verificación | Cómo |
|-------------|------|
| ¿Hay una sola capa de seguridad? | Debe haber defensa en profundidad |
| ¿Los datos sensibles están cifrados? | En reposo y en tránsito |
| ¿Hay logging de todo? | SIEM centralizado |
| ¿Se puede escalar? | Auto-scaling configurado |
| ¿Hay backup? | Automático, cifrado, testeado |
| ¿Se puede recuperar? | Plan de DR documentado y probado |

---

## 16. Checklist de Arquitectura

### 16.1 Checklist Básico (Para tareas y proyectos simples)

| # | Verificación | Cumple |
|---|-------------|--------|
| 1 | ¿Hay autenticación en el sistema? | ☐ |
| 2 | ¿Las contraseñas están hasheadas? | ☐ |
| 3 | ¿Se usa HTTPS/TLS? | ☐ |
| 4 | ¿Hay firewall configurado? | ☐ |
| 5 | ¿La base de datos no es accesible desde internet? | ☐ |
| 6 | ¿Hay backup de los datos? | ☐ |
| 7 | ¿Los inputs del usuario se validan? | ☐ |
| 8 | ¿Hay logs de actividad? | ☐ |

### 16.2 Checklist Intermedio

| # | Verificación | Cumple |
|---|-------------|--------|
| 9 | ¿MFA implementado? | ☐ |
| 10 | ¿RBAC configurado? | ☐ |
| 11 | ¿Segmentación de red? | ☐ |
| 12 | ¿WAF activo? | ☐ |
| 13 | ¿Cifrado en reposo de datos? | ☐ |
| 14 | ¿Rate limiting en APIs? | ☐ |
| 15 | ¿Scan de vulnerabilidades automático? | ☐ |
| 16 | ¿Secrets management (no hardcodeados)? | ☐ |

### 16.3 Checklist Avanzado

| # | Verificación | Cumple |
|---|-------------|--------|
| 17 | ¿Zero Trust implementado? | ☐ |
| 18 | ¿SIEM con detección de anomalías? | ☐ |
| 19 | ¿SOAR (respuesta automatizada)? | ☐ |
| 20 | ¿Threat intelligence integrado? | ☐ |
| 21 | ¿Infrastructure as Code? | ☐ |
| 22 | ¿Compliance automatizado? | ☐ |
| 23 | ¿Disaster Recovery probado? | ☐ |
| 24 | ¿Penetration testing regular? | ☐ |

---

## 17. Referencias y Recursos

### 17.1 Frameworks de Arquitectura

| Framework | Descripción | URL |
|-----------|-------------|-----|
| **NIST SP 800-53** | Controles de seguridad | https://csrc.nist.gov/publications/detail/sp/800-53 |
| **NIST Zero Trust** | Guía Zero Trust | https://csrc.nist.gov/publications/detail/sp/800-207 |
| **MITRE ATT&CK** | Técnicas de ataque | https://attack.mitre.org |
| **OWASP ASVS** | Verification Standard | https://owasp.org/www-project-application-security-verification-standard |
| **CIS Controls** | 18 controles esenciales | https://www.cisecurity.org/controls |
| **ISO 27001** | Estándar internacional | https://www.iso.org/isoiec-27001-information-security.html |

### 17.2 Herramientas de Diagramado

| Herramienta | Uso | URL |
|-------------|-----|-----|
| **Draw.io** | Diagramas gratuitos | https://app.diagrams.net |
| **Lucidchart** | Diagramas profesionales | https://www.lucidchart.com |
| **Miro** | Diagramas colaborativos | https://miro.com |
| **PlantUML** | Diagramas como código | https://plantuml.com |
| **AWS Architecture Icons** | Iconos oficiales AWS | https://aws.amazon.com/architecture/icons |

### 17.3 Recursos de Aprendizaje

| Recurso | Tipo | URL |
|---------|------|-----|
| **AWS Well-Architected** | Framework de AWS | https://aws.amazon.com/architecture/well-architected |
| **Azure Architecture Center** | Patrones Azure | https://learn.microsoft.com/azure/architecture |
| **Google Cloud Architecture** | Patrones GCP | https://cloud.google.com/architecture |
| **Cloud Security Alliance** | Guías cloud | https://cloudsecurityalliance.org |

---

## Apéndice: Imágenes de Referencia

> Las siguientes imágenes de referencia están disponibles en la carpeta:
> `Recursos/Arquitectura_Imagenes/`
>
> Para agregar imágenes, colócalas en esa carpeta y referencia su nombre aquí.

---

*Documento creado exclusivamente con fines educativos. Parte del curso de ciberseguridad.*
