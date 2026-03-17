# CURSO : Introducción a la seguridad informática


---

## MÓDULO 1: FUNDAMENTOS DE LA SEGURIDAD INFORMÁTICA

### 1.1 Motivación

La ciberseguridad es una disciplina crítica en el mundo digital actual. Cada día se producen ataques cibernéticos que comprometen datos personales, financieros y corporativos.

**Estadísticas relevantes:**
- Gran parte de las brechas de seguridad son causadas por error humano
- El costo alto de solucionar brechas
- El ransomware ataca a una empresa cada 11 segundos

**¿Por qué estudiar ciberseguridad?**
- Alta demanda laboral
- Protección de activos críticos
- Cumplimiento normativo obligatorio
- Defensa de derechos fundamentales (privacidad)


Hablar de los dominios de seguridad informática es, en esencia, hablar de cómo hemos intentado poner orden al caos digital. No surgieron de la nada; son el resultado de décadas de aprendizaje (a veces por las malas) sobre cómo proteger la información.


---

## ¿Cómo surgen los dominios de seguridad?

Originalmente, la "seguridad" era simplemente ponerle una contraseña a una terminal. Sin embargo, a medida que las empresas se digitalizaron, se dieron cuenta de que no bastaba con tecnología. Surgieron hitos clave:

1. **La Necesidad de Estándares:** En los años 90 y principios de los 2000, las organizaciones necesitaban un lenguaje común. De ahí nacieron marcos como la **ISO/IEC 27001**, que estructuró la seguridad en "pedazos" manejables.
2. **El Modelo de ISC²:** La organización tras la certificación CISSP popularizó los **8 Dominios del CBK** (Common Body of Knowledge), que hoy son el estándar de oro para entender esta disciplina.
3. **Evolución de las Amenazas:** Los dominios pasaron de ser puramente técnicos (cifrado) a ser humanos y legales (privacidad, leyes internacionales).

---

## Los 8 Dominios Principales (Modelo CISSP)

Para que una empresa sea segura, debe cubrir estos frentes:

### 1. Gestión de Seguridad y Riesgos

Es el "cerebro" de la operación. Aquí se definen las políticas, el cumplimiento legal (como el GDPR) y se decide cuánto dinero se va a gastar basándose en qué tan probable es que algo salga mal.

### 2. Seguridad de Activos

No puedes proteger lo que no sabes que tienes. Este dominio se encarga de clasificar la información (¿es pública o secreta?) y asegurar que los datos se manejen correctamente durante todo su ciclo de vida.

### 3. Arquitectura e Ingeniería de Seguridad

Aquí es donde entra la ciencia. Se diseñan sistemas resistentes desde la base utilizando modelos matemáticos y principios de ingeniería.

### 4. Seguridad de Redes y Comunicaciones

Se enfoca en los canales por los que viajan los datos. Incluye la protección de firewalls, redes Wi-Fi, segmentación de redes y protocolos de comunicación segura.

### 5. Gestión de Identidad y Acceso (IAM)

El principio de "quién eres y a qué tienes permiso". Controla que solo las personas correctas entren a los sistemas correctos, usando biometría, tarjetas inteligentes o autenticación de múltiples factores (MFA).

### 6. Evaluación y Pruebas de Seguridad

Es el control de calidad. Aquí se hacen **Pentesting** (hackeo ético) y escaneos de vulnerabilidades para encontrar grietas antes de que lo haga un atacante real.

### 7. Operaciones de Seguridad

Es el "día a día". Incluye la detección de intrusos, la respuesta ante incidentes (qué hacer si nos hackean hoy) y el mantenimiento de las copias de seguridad.

### 8. Seguridad en el Desarrollo de Software (AppSec)

Asegura que las aplicaciones que usamos no tengan errores de seguridad desde que se escriben las primeras líneas de código.

---

## Resumen de los Dominios

| Dominio | Foco Principal |
| --- | --- |
| **Riesgos** | Estrategia y Leyes |
| **Activos** | Datos y Clasificación |
| **Arquitectura** | Diseño de Sistemas |
| **Redes** | Conectividad Segura |
| **Identidad** | Usuarios y Permisos |
| **Pruebas** | Auditoría y Pentesting |
| **Operaciones** | Monitoreo y Respuesta |
| **Software** | Código Seguro |

---



---

### 1.2 Definiciones Fundamentales: La Tríada CIA

```
┌────────────────────────────────────────────────────────┐
│              TRÍADA CIA DE SEGURIDAD                   │
├────────────────────────────────────────────────────────┤
│                                                        │
│         ┌─────────────────────────────┐               │
│         │   CONFIDENCIALIDAD          │               │
│         │   (Confidentiality)         │               │
│         │                             │               │
│         │ Solo personas autorizadas   │               │
│         │ pueden acceder              │               │
│         └──────────┬──────────────────┘               │
│                    │                                   │
│         ┌──────────┴──────────┐                       │
│         │                     │                       │
│  ┌──────▼──────┐      ┌──────▼──────┐                │
│  │ INTEGRIDAD  │      │DISPONIBILIDAD│                │
│  │ (Integrity) │      │(Availability)│                │
│  │             │      │              │                │
│  │ Datos no    │      │ Acceso cuando│                │
│  │ modificados │      │ se necesita  │                │
│  └─────────────┘      └──────────────┘                │
│                                                        │
└────────────────────────────────────────────────────────┘
```

#### 1.2.1 Confidencialidad (Confidentiality)

**Definición:** Garantizar que la información solo sea accesible por personas autorizadas.

**Ejemplo práctico:**
Un hospital maneja historias clínicas. Solo el médico tratante y el paciente deben poder acceder a esos datos. Si un empleado administrativo puede ver diagnósticos de VIH sin justificación, se viola la confidencialidad.

**Mecanismos de protección:**
- Cifrado de datos (AES-256)
- Control de acceso basado en roles (RBAC)
- Autenticación multifactor (MFA)
- Clasificación de información

**Ejemplo de código - Cifrado en Python:**
```python
from cryptography.fernet import Fernet

# Generar clave
clave = Fernet.generate_key()
cipher = Fernet(clave)

# Cifrar datos sensibles
datos_sensibles = b"Historia clinica: Paciente con diabetes tipo 2"
datos_cifrados = cipher.encrypt(datos_sensibles)

print(f"Datos originales: {datos_sensibles}")
print(f"Datos cifrados: {datos_cifrados}")

# Descifrar
datos_descifrados = cipher.decrypt(datos_cifrados)
print(f"Datos descifrados: {datos_descifrados}")
```

#### 1.2.2 Integridad (Integrity)

**Definición:** Asegurar que la información no ha sido modificada de manera no autorizada.

**Ejemplo práctico:**
Un banco procesa una transferencia de $100. Si un atacante modifica el monto a $100,000 durante la transmisión, se viola la integridad.

**Mecanismos de protección:**
- Funciones hash (SHA-256, SHA-512)
- Firmas digitales
- Checksums
- Control de versiones

**Ejemplo de código - Hash en Python:**
```python
import hashlib

# Documento original
documento = "Transferencia de $100 a cuenta 12345"

# Generar hash SHA-256
hash_original = hashlib.sha256(documento.encode()).hexdigest()
print(f"Hash original: {hash_original}")

# Documento modificado
documento_modificado = "Transferencia de $100000 a cuenta 12345"
hash_modificado = hashlib.sha256(documento_modificado.encode()).hexdigest()
print(f"Hash modificado: {hash_modificado}")

# Verificación de integridad
if hash_original == hash_modificado:
    print("✓ Documento íntegro")
else:
    print("✗ ALERTA: Documento ha sido modificado")
```

#### 1.2.3 Disponibilidad (Availability)

**Definición:** Garantizar que los sistemas y datos estén accesibles cuando se necesiten.

**Ejemplo práctico:**
Un hospital necesita acceder al sistema de historias clínicas 24/7. Si un ataque DDoS tumba el servidor, aunque los datos estén seguros y sin modificar, se viola la disponibilidad.

**Mecanismos de protección:**
- Redundancia de servidores
- Balanceo de carga
- Backups automáticos
- Planes de recuperación ante desastres (DRP)
- Protección contra DDoS

**Ejemplo de arquitectura de alta disponibilidad:**
```
[Usuario] → [Load Balancer] → [Servidor 1]
                            → [Servidor 2]
                            → [Servidor 3]
                            
[Base de Datos Principal] ← Replicación → [Base de Datos Réplica]
```

---

### 1.3 Tipos de Ataques Comunes y Mecanismos de Protección

#### 1.3.1 Phishing

**Definición:** Técnica de ingeniería social donde el atacante se hace pasar por una entidad confiable para robar credenciales.

**Diagrama de ataque:**

```
┌──────────────────────────────────────────────────────────┐
│            CICLO DE ATAQUE DE PHISHING                   │
└──────────────────────────────────────────────────────────┘

1. PREPARACIÓN
   ┌─────────────────────────────────────┐
   │ Atacante crea:                      │
   │ • Email falso                       │
   │ • Sitio web clonado                 │
   │ • Dominio similar (typosquatting)   │
   └─────────────────┬───────────────────┘
                     │
                     ▼
2. DISTRIBUCIÓN
   ┌─────────────────────────────────────┐
   │ Envío masivo de emails:             │
   │ • 10,000 emails enviados            │
   │ • Tasa de apertura: 20% (2,000)     │
   │ • Tasa de clic: 5% (100)            │
   └─────────────────┬───────────────────┘
                     │
                     ▼
3. ENGAÑO
   ┌─────────────────────────────────────┐
   │ Víctima ingresa credenciales en     │
   │ sitio falso                         │
   └─────────────────┬───────────────────┘
                     │
                     ▼
4. CAPTURA
   ┌─────────────────────────────────────┐
   │ Atacante obtiene:                   │
   │ • Usuario y contraseña              │
   │ • Datos de tarjeta                  │
   │ • Información personal              │
   └─────────────────┬───────────────────┘
                     │
                     ▼
5. EXPLOTACIÓN
   ┌─────────────────────────────────────┐
   │ • Acceso a cuentas bancarias        │
   │ • Robo de identidad                 │
   │ • Venta de datos en dark web        │
   └─────────────────────────────────────┘
```

**Tipos de Phishing:**

1. **Email Phishing:** Correos masivos fraudulentos
2. **Spear Phishing:** Ataques dirigidos a personas específicas
3. **Whaling:** Ataques a ejecutivos de alto nivel
4. **Smishing:** Phishing por SMS
5. **Vishing:** Phishing por llamada telefónica

**Ejemplo real:**
```
De: seguridad@bancoo-uruguay.com (nota la 'o' extra)
Asunto: URGENTE - Verificación de cuenta

Estimado cliente,

Detectamos actividad sospechosa en su cuenta.
Haga clic aquí para verificar: http://banco-falso.com/login

Si no verifica en 24 horas, su cuenta será bloqueada.

Atentamente,
Banco Uruguay
```

**Indicadores de phishing:**
- Dominio sospechoso (bancoo vs banco)
- Urgencia artificial
- Errores ortográficos
- Enlaces que no coinciden con el texto
- Solicitud de credenciales

**Protección:**
- Capacitación de usuarios
- Filtros anti-spam
- Verificación de remitentes (SPF, DKIM, DMARC)
- Autenticación multifactor
- Simulacros de phishing

#### 1.3.2 Malware

**Definición:** Software malicioso diseñado para dañar, explotar o comprometer sistemas.

**Tipos principales:**

1. **Virus:** Se replica adjuntándose a archivos legítimos
2. **Gusanos:** Se propagan automáticamente por la red
3. **Troyanos:** Se disfrazan de software legítimo
4. **Ransomware:** Cifra archivos y exige rescate
5. **Spyware:** Espía actividades del usuario
6. **Rootkits:** Ocultan la presencia de malware
7. **Keyloggers:** Registran pulsaciones de teclado

**Ejemplo de Ransomware - WannaCry (2017):**
- Infectó 200,000+ computadoras en 150 países
- Explotó vulnerabilidad EternalBlue de Windows
- Exigía $300-600 en Bitcoin
- Causó pérdidas de $4 mil millones

**Protección:**
- Antivirus/EDR actualizado
- Parches de seguridad
- Backups offline (regla 3-2-1) (3-2-2-1-0)
- Segmentación de red
- Principio de mínimo privilegio

#### 1.3.3 Ataques de Denegación de Servicio (DoS/DDoS)

**Definición:** Saturar un sistema con tráfico para hacerlo inaccesible.

**Diagrama de ataque DDoS:**

```
┌──────────────────────────────────────────────────────────┐
│              ATAQUE DDoS CON BOTNET                      │
└──────────────────────────────────────────────────────────┘

                    ┌─────────────┐
                    │  ATACANTE   │
                    │ (C&C Server)│
                    └──────┬──────┘
                           │
                           │ Comando de ataque
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
   ┌────▼────┐       ┌────▼────┐       ┌────▼────┐
   │ Bot 1   │       │ Bot 2   │  ...  │ Bot N   │
   │(IoT cam)│       │(Router) │       │(PC)     │
   └────┬────┘       └────┬────┘       └────┬────┘
        │                  │                  │
        │ 1000 req/s       │ 1000 req/s       │ 1000 req/s
        │                  │                  │
        └──────────────────┼──────────────────┘
                           │
                           │ 100,000 req/s total
                           ▼
                    ┌──────────────┐
                    │   SERVIDOR   │
                    │   VÍCTIMA    │
                    │              │
                    │ ❌ SATURADO  │
                    │ ❌ INACCESIBLE│
                    └──────────────┘

Usuarios legítimos
        │
        │ Intento de acceso
        ▼
    ❌ Timeout
    ❌ No responde
```

**Diferencia:**
- **DoS:** Un solo atacante
- **DDoS:** Múltiples atacantes (botnet)

**Tipos de ataques DDoS:**

1. **Volumétricos:** Saturan el ancho de banda
   - UDP Flood
   - ICMP Flood
   - DNS Amplification

2. **De protocolo:** Agotan recursos del servidor
   - SYN Flood
   - Ping of Death

3. **De aplicación:** Atacan la capa 7 (HTTP)
   - HTTP Flood
   - Slowloris

**Ejemplo de ataque DDoS histórico:**
- **Dyn (2016):** Botnet Mirai atacó proveedor DNS
- Afectó: Twitter, Netflix, Reddit, GitHub
- Tráfico: 1.2 Tbps
- Dispositivos IoT comprometidos: 100,000+

**Protección:**
- CDN (Cloudflare, Akamai)
- Rate limiting
- Web Application Firewall (WAF)
- Detección de anomalías
- Capacidad de ancho de banda sobredimensionada

#### 1.3.4 Inyección SQL

**Definición:** Insertar código SQL malicioso en campos de entrada para manipular la base de datos.

**Ejemplo vulnerable:**
```python
# CÓDIGO VULNERABLE - NO USAR
usuario = request.form['usuario']
password = request.form['password']

query = f"SELECT * FROM usuarios WHERE usuario='{usuario}' AND password='{password}'"
cursor.execute(query)
```

**Ataque:**
```
Usuario: admin' OR '1'='1
Password: cualquiercosa
```

**Query resultante:**
```sql
SELECT * FROM usuarios WHERE usuario='admin' OR '1'='1' AND password='cualquiercosa'
```
Esto siempre retorna verdadero, permitiendo acceso sin contraseña.

**Código seguro:**
```python
# CÓDIGO SEGURO - Usar prepared statements
usuario = request.form['usuario']
password = request.form['password']

query = "SELECT * FROM usuarios WHERE usuario=%s AND password=%s"
cursor.execute(query, (usuario, password))
```

**Protección:**
- Prepared statements / Parametrized queries
- ORM (Object-Relational Mapping)
- Validación de entrada
- Validación de campos obtenidos de bases de datos u otras fuentes
- Principio de mínimo privilegio en BD
- WAF

#### 1.3.5 Cross-Site Scripting (XSS)

**Definición:** Inyectar scripts maliciosos en páginas web vistas por otros usuarios.

**Tipos:**

1. **Reflected XSS:** El script viene en la URL
2. **Stored XSS:** El script se guarda en la BD
3. **DOM-based XSS:** Manipula el DOM del navegador

**Ejemplo vulnerable:**
```html
<!-- Página vulnerable -->
<h1>Bienvenido <?php echo $_GET['nombre']; ?></h1>
```

**Ataque:**
```
http://sitio.com/bienvenida.php?nombre=<script>alert(document.cookie)</script>
```

**Resultado:** El navegador ejecuta el script y roba las cookies de sesión.

**Código seguro:**
```html
<!-- Escapar HTML -->
<h1>Bienvenido <?php echo htmlspecialchars($_GET['nombre']); ?></h1>
```

**Protección:**
- Escapar salida HTML
- Content Security Policy (CSP)
- HTTPOnly cookies
- Validación de entrada
- Sanitización de datos

---

### 1.4 Introducción a la Privacidad y Protección de Datos Personales

#### 1.4.1 ¿Qué es un Dato Personal?

**Definición:** Cualquier información relacionada con una persona física que sirve para identificarla.

**Ejemplos:**
- **Directos:** Nombre, CI, pasaporte, email
- **Indirectos:** IP, cookies, ubicación GPS
- **Sensibles:** Salud, religión, orientación sexual, biometría

#### 1.4.2 Marco Normativo en Uruguay

**Ley N° 18.331 - Protección de Datos Personales y Acción de Habeas Data**

**Principios fundamentales:**

1. **Consentimiento:** El titular debe autorizar el tratamiento
2. **Finalidad:** Los datos solo se usan para el propósito declarado
3. **Proporcionalidad:** Solo recopilar datos necesarios
4. **Calidad:** Datos exactos y actualizados
5. **Seguridad:** Medidas técnicas y organizativas
6. **Confidencialidad:** No divulgar sin autorización

**Derechos del titular (ARCO):**
- **A**cceso: Ver qué datos tienen sobre mí
- **R**ectificación: Corregir datos incorrectos
- **C**ancelación: Eliminar datos (derecho al olvido)
- **O**posición: Rechazar ciertos tratamientos

**Autoridad de control:** URCDP (Unidad Reguladora y de Control de Datos Personales)

**Sanciones:**
- Multas de hasta 500,000 UI (~$2 millones USD)
- Clausura temporal o definitiva
- Responsabilidad penal

#### 1.4.3 GDPR (Reglamento General de Protección de Datos - UE)

Aunque es europeo, afecta a cualquier empresa que trate datos de ciudadanos de la UE.

**Conceptos clave:**

1. **Privacy by Design:** La privacidad se diseña desde el inicio
2. **Privacy by Default:** Configuración más restrictiva por defecto
3. **Accountability:** Demostrar cumplimiento
4. **Data Protection Officer (DPO):** Responsable de privacidad

**Sanciones:**
- Ecónomicas o 4% de facturación global anual
- Lo que sea mayor

#### 1.4.4 Ejemplo Práctico: Registro de Actividades de Tratamiento (RAT)

```markdown
| Campo | Descripción |
|-------|-------------|
| Nombre del tratamiento | Gestión de clientes |
| Responsable | Empresa XYZ S.A. |
| Finalidad | Facturación y soporte |
| Base legal | Ejecución de contrato |
| Categorías de datos | Nombre, email, teléfono, dirección |
| Destinatarios | Proveedor de hosting (AWS) |
| Transferencias internacionales | Sí - EE.UU. (cláusulas contractuales tipo) |
| Plazo de conservación | 5 años (obligación fiscal) |
| Medidas de seguridad | Cifrado AES-256, MFA, backups diarios |
```

---

## MÓDULO 2: ÁREAS DE APLICACIÓN DE LA CIBERSEGURIDAD

### 2.1 Dominios de la Ciberseguridad

#### 2.1.1 Seguridad de Red

**Objetivo:** Proteger la infraestructura de comunicaciones.

**Componentes:**
- Firewalls
- IDS/IPS (Intrusion Detection/Prevention Systems)
- VPN (Virtual Private Network)
- Segmentación de red (VLANs)
- Zero Trust Architecture

**Ejemplo práctico - Configurar firewall con iptables:**
```bash
# Bloquear todo el tráfico entrante por defecto
sudo iptables -P INPUT DROP

# Permitir tráfico establecido
sudo iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# Permitir SSH solo desde IP específica
sudo iptables -A INPUT -p tcp --dport 22 -s 192.168.1.100 -j ACCEPT

# Permitir HTTP y HTTPS
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT

# Ver reglas
sudo iptables -L -v
```

#### 2.1.2 Seguridad de Aplicaciones

**Objetivo:** Proteger el software durante todo su ciclo de vida.

**Prácticas:**
- Secure SDLC (Software Development Lifecycle)
- Code review
- SAST (Static Application Security Testing)
- DAST (Dynamic Application Security Testing)
- Dependency scanning

**Ejemplo - Análisis con OWASP ZAP:**
```bash
# Instalar OWASP ZAP
docker pull owasp/zap2docker-stable

# Escanear aplicación web
docker run -t owasp/zap2docker-stable zap-baseline.py \
  -t https://mi-aplicacion.com \
  -r reporte.html
```

#### 2.1.3 Seguridad en la Nube

**Modelos de responsabilidad compartida:**

**IaaS (Infrastructure as a Service):**
- Proveedor: Hardware, red, hipervisor
- Cliente: SO, aplicaciones, datos

**PaaS (Platform as a Service):**
- Proveedor: Todo lo anterior + SO, runtime
- Cliente: Aplicaciones, datos

**SaaS (Software as a Service):**
- Proveedor: Todo
- Cliente: Configuración, datos

**Ejemplo - Configuración segura en AWS:**
```bash
# Habilitar cifrado en bucket S3
aws s3api put-bucket-encryption \
  --bucket mi-bucket \
  --server-side-encryption-configuration '{
    "Rules": [{
      "ApplyServerSideEncryptionByDefault": {
        "SSEAlgorithm": "AES256"
      }
    }]
  }'

# Bloquear acceso público
aws s3api put-public-access-block \
  --bucket mi-bucket \
  --public-access-block-configuration \
    "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true"
```

# Detalle de los Ataques DDoS
1. Volumétricos (Fuerza Bruta de Red)
Su objetivo es enviar tantos datos que "atiborran" la tubería de entrada de internet de la víctima.

UDP Flood: El atacante envía una avalancha de paquetes UDP a puertos aleatorios del servidor. El servidor intenta verificar si hay una aplicación escuchando en ese puerto y, al no encontrarla, responde con un paquete "ICMP Destination Unreachable". Multiplica esto por millones y el servidor se agota respondiendo que "no hay nadie en casa".

ICMP Flood (Ping Flood): Se satura el ancho de banda enviando paquetes de "eco" (ping) lo más rápido posible sin esperar respuesta.

DNS Amplification: Es un ataque de reflexión. El atacante envía pequeñas peticiones DNS a servidores públicos falsificando la IP de la víctima (spoofing). El servidor DNS responde con mucha información a la IP de la víctima.

Una petición de 60 bytes puede generar una respuesta de 3000 bytes. ¡El atacante multiplica su fuerza x50!

2. De Protocolo (Agotamiento de Recursos)
No buscan llenar la tubería, sino consumir la memoria o la capacidad de procesamiento del equipo (firewalls, balanceadores).

SYN Flood: Explota el "saludo de tres vías" de TCP. El atacante envía peticiones de conexión (SYN), el servidor responde (SYN-ACK) y reserva memoria esperando la confirmación final del cliente, que nunca llega. El servidor se queda con miles de conexiones "a medias" hasta que se bloquea.

Ping of Death: Se envían paquetes IP malformados o más grandes que el máximo permitido (65,535 bytes). Al intentar reensamblarlos, el sistema operativo de la víctima se desborda y se congela (BSOD).

3. De Aplicación (Capa 7)
Son los más sofisticados porque imitan el comportamiento humano y son difíciles de detectar.

HTTP Flood: Consiste en solicitar repetidamente páginas web o archivos pesados. Obliga al servidor a realizar consultas a la base de datos y renderizar páginas hasta que colapsa.

Slowloris: El atacante abre muchas conexiones HTTP pero envía los datos extremadamente lento (byte a byte). Mantiene las líneas ocupadas el mayor tiempo posible, impidiendo que usuarios reales puedan entrar.

🔐 Seguridad: Validación, Sanitización y Escapado
Aquí es donde solemos confundirnos. Vamos a diferenciarlos con una analogía de una carta:

Concepto	Analogía	Definición Técnica
Validación	¿Es esto una carta?	Comprobar si el dato cumple el formato esperado (ej. ¿es un email?, ¿es un número?). Si no cumple, se rechaza.
Sanitización	Quitar el polvo o veneno	Limpiar la entrada eliminando partes peligrosas (ej. borrar etiquetas <script>).
Escapado	Poner la carta tras un vidrio	Convertir caracteres especiales en texto inofensivo para que el navegador no los ejecute (ej. transformar < en &lt;).
Conceptos Específicos:
Escapar salida HTML: Es la defensa número 1 contra XSS (Cross-Site Scripting). Si un usuario comenta: <script>alert(1)</script>, el escapado lo muestra literalmente en pantalla en lugar de ejecutar la ventana de alerta.

Validación de entrada: Ocurre en el "lado del servidor". Es asegurar que si pides una "Edad", el usuario no te envíe una palabra o un código SQL.

Sanitización de datos: Se usa cuando necesitas permitir algo de formato (como negritas en un post) pero quieres eliminar scripts maliciosos.

HTTPOnly Cookies: Una bandera de seguridad para las cookies. Si está activa, el código JavaScript del navegador no puede leer la cookie. Esto evita que un atacante robe tu sesión mediante un script.

Content Security Policy (CSP): Una capa de seguridad adicional que le dice al navegador: "Solo confía en scripts que vengan de mi propio dominio o de Google Analytics". Bloquea cualquier script malicioso externo que intente ejecutarse.



## Ejemplo Práctico: Registro de Usuario (Python/FastAPI)
Imagina que recibes el nombre de un usuario. Aquí aplicamos las capas de seguridad:

Python
from fastapi import FastAPI, HTTPException
import html

app = FastAPI()

@app.post("/registro")
async def registrar_usuario(nombre: str):
    # 1. VALIDACIÓN: ¿El nombre tiene un largo razonable y no tiene caracteres raros?
    if len(nombre) > 50 or not nombre.isalnum():
        raise HTTPException(status_code=400, detail="Nombre inválido")

    # 2. SANITIZACIÓN: Limpiamos espacios extra o normalizamos
    nombre_limpio = nombre.strip().capitalize()

    # 3. ESCAPADO (Al mostrarlo en el HTML):
    # Si el usuario mandó algo como <script>, se convierte en &lt;script&gt;
    nombre_seguro = html.escape(nombre_limpio)
    
    return {"mensaje": f"Hola {nombre_seguro}, bienvenido!"}
⚡ ¿Cómo se hace un DoS desde una sola máquina?
Un ataque DoS (Denial of Service) desde una sola computadora busca agotar los recursos del servidor mediante la eficiencia, no necesariamente mediante el ancho de banda. Como no tienes una botnet de 10,000 PCs, tienes que ser "inteligente" para que tu pequeña capacidad de procesamiento venza a la del servidor.

Aquí tienes las técnicas más comunes:

1. Slowloris (El ataque de "bajo y lento")
Es el más efectivo desde una sola máquina. En lugar de enviar muchos datos, abres cientos de conexiones HTTP al servidor y las dejas abiertas.

Cómo funciona: Envías cabeceras HTTP incompletas. El servidor mantiene la conexión abierta esperando el resto de la petición.

El efecto: Cada servidor tiene un límite máximo de conexiones simultáneas (ej. 200). Si tú ocupas las 200 con tu laptop, nadie más puede entrar.

2. Fork Bomb (Ataque local)
Este no es contra un servidor remoto, sino contra la propia máquina donde se ejecuta. Es una función que se llama a sí misma dos veces, creando procesos infinitos hasta que el CPU y la RAM se agotan en segundos.

Ejemplo en Bash: :(){ :|:& };: (No lo ejecutes, bloqueará tu PC).

3. SYN Flood (Si el servidor es débil)
Si tienes una conexión rápida, puedes usar herramientas como hping3 para enviar paquetes SYN con una IP de origen falsa (spoofing).

Comando educativo: sudo hping3 -S --flood -V -p 80 [IP_DESTINO]

El servidor se queda esperando confirmaciones de IPs que no existen hasta agotar su tabla de conexiones.

4. ReDoS (Regular Expression DoS)
Este es un ataque de capa de aplicación. Envías una cadena de texto muy específica a un formulario que use una "Expresión Regular" mal diseñada en el servidor.

El efecto: El servidor entra en un bucle de cálculo exponencial intentando validar tu texto, llevando el uso de CPU al 100% con un solo envío.

⚠️ Nota de Seguridad
Como profesional , recuerda que realizar estos ataques contra sistemas ajenos sin autorización es ilegal. La mejor forma de aprender es montando tu propio servidor local (en una VM o Docker) y tratar de "tumbarlo" para ver cómo reaccionan los logs y el firewall.


Configuración de Defensa en Nginx
1. Limitar Conexiones y Peticiones
Esto evita que una sola IP sature el servidor. Si alguien intenta abrir 500 conexiones, Nginx simplemente las rechazará.

Nginx
http {
    # Creamos una zona en memoria para rastrear IPs (10MB alcanzan para 160,000 IPs)
    limit_conn_zone $binary_remote_addr zone=addr:10m;
    limit_req_zone $binary_remote_addr zone=one:10m rate=5r/s;

    server {
        location / {
            # Máximo 10 conexiones simultáneas por IP
            limit_conn addr 10;
            
            # Máximo 5 peticiones por segundo, con un "margen" (burst) de 10
            limit_req zone=one burst=10 nodelay;
        }
    }
}
2. Combatir el Slowloris (Ajuste de Timeouts)
El Slowloris gana porque el servidor espera "eternamente" a que el cliente termine de hablar. Vamos a acortar esa paciencia.

Nginx
# Tiempo máximo para leer el cuerpo de la petición (si es muy lento, se corta)
client_body_timeout 5s;

# Tiempo máximo para leer las cabeceras (headers)
client_header_timeout 5s;

# Tiempo que una conexión puede estar "viva" sin hacer nada
keepalive_timeout 5s;

# Tiempo máximo para enviar la respuesta al cliente
send_timeout 5s;
🧱 El WAF (Web Application Firewall)
Mientras que Nginx detiene el tráfico "pesado", un WAF (como Cloudflare o AWS WAF) analiza el "contenido" del tráfico.

Un WAF puede detectar patrones:

Reputación de IP: Si la IP de la máquina atacante ya ha sido reportada por otros ataques, el WAF la bloquea antes de que llegue a tu servidor.

Geofencing: Si tu aplicación es solo para Uruguay y recibes un ataque desde una IP de otro continente, puedes bloquear ese país entero con un clic.

Reglas de Capa 7: Puede identificar si una petición HTTP tiene cabeceras malformadas típicas de herramientas de ataque automático.

