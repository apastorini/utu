# Clase 40: Pruebas de Seguridad y Hacking Etico

**Numero de clase:** 30  
**Duracion:** 2 horas  
**Curso:** Taller de Ciberseguridad Orientada al Desarrollo

---

## Objetivos de Aprendizaje

- Distinguir entre pruebas de penetracion y pruebas automatizadas
- Aplicar metodologia de pentesting: reconocimiento, escaneo, explotacion
- Usar herramientas como nmap, curl, OWASP ZAP, Burp Suite
- Probar ataques comunes contra la app segura
- Demostrar que las defensas implementadas bloquean los ataques

---

## Contenido Detallado

### 1. Pentesting vs. Pruebas Automatizadas (15 min)

| Aspecto | Pentesting Manual | Pruebas Automatizadas |
|---------|------------------|----------------------|
| Alcance | Profundo, especifico | Amplio, general |
| Velocidad | Lenta | Rapida |
| Creatividad | Alta (encadenamiento de vulnerabilidades) | Baja (patrones conocidos) |
| Falsos positivos | Bajos | Pueden ser altos |
| Costo | Alto | Bajo |
| Cobertura | Logica de negocio, bypass creativo | Vulnerabilidades tecnicas comunes |

**Cuando usar cada una:**
- Automatizadas: En CI/CD (SAST, DAST, SCA), escaneos regulares
- Manual: Antes de releases criticos, aplicaciones con logica de negocio compleja, aplicaciones que manejan datos sensibles

### 2. Metodologia de Pentesting (10 min)

```
1. Reconocimiento (Information Gathering)
   -> nmap, whois, dnsrecon, sublist3r

2. Escaneo (Scanning)
   -> nmap -sV, gobuster, nikto, OWASP ZAP

3. Explotacion (Exploitation)
   -> SQLMap, Metasploit, Burp Suite Repeater

4. Post-Explotacion
   -> Escalada de privilegios, persistencia, exfiltracion de datos

5. Reporte
   -> Documentar hallazgos, evidencias, recomendaciones
```

### 3. Herramientas (15 min)

**nmap - Escaneo de puertos y servicios:**
```bash
# Escaneo basico de puertos
nmap -sS -p- localhost

# Escaneo de servicios y versiones
nmap -sV -p 8000 localhost

# Escaneo con scripts de seguridad
nmap -sV --script=http-enum,http-headers -p 8000 localhost
```

**gobuster - Fuzzing de directorios:**
```bash
gobuster dir -u http://localhost:8000 -w /usr/share/wordlists/dirb/common.txt
```

**curl - Pruebas manuales:**
```bash
# GET basico
curl -v http://localhost:8000/health

# POST con datos
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"test"}'

# Con token
curl -H "Authorization: Bearer TOKEN" http://localhost:8000/api/items/
```

**SQLMap - Deteccion de SQL Injection:**
```bash
sqlmap -u "http://localhost:8000/api/items/1" \
  --cookie="access_token=TOKEN" \
  --batch --level=2
```

**OWASP ZAP - DAST automatizado:**
```bash
# Escaneo basico
zap-baseline.py -t http://localhost:8000 -r report.html

# Escaneo completo
zap-full-scan.py -t http://localhost:8000 -r report.html
```

### 4. La App Segura como Objetivo (5 min)

La aplicacion creada en las clases 28-29 tiene las siguientes defensas:

- Autenticacion JWT con refresh tokens
- Hashing de contrasenas con bcrypt
- Validacion de entrada con Pydantic
- Consultas parametrizadas (SQLAlchemy ORM)
- Autorizacion con RBAC (roles user/admin)
- Proteccion IDOR (verificacion de ownership)
- Rate limiting en login
- Security headers
- Logging seguro
- CORS restrictivo

---

## Ejercicio 1: Escanear la App con nmap y OWASP ZAP

**Enunciado:** Ejecutar nmap y OWASP ZAP contra la aplicacion segura, analizar los resultados.

**Solucion paso a paso:**

**Paso 1: Iniciar la aplicacion**
```bash
cd secure-api
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

**Paso 2: Escaneo con nmap**
```bash
nmap -sV -p 8000 --script=http-enum,http-headers localhost
```

**Analisis de resultados esperados:**
```
PORT     STATE SERVICE VERSION
8000/tcp open  http    uvicorn 0.27.0
| http-headers:
|   content-type: application/json
|   x-content-type-options: nosniff
|   x-frame-options: DENY
|   x-xss-protection: 1; mode=block
|   strict-transport-security: max-age=31536000; includeSubDomains
|   content-security-policy: default-src 'self'
|   referrer-policy: strict-origin-when-cross-origin
|_  date: ...
```

**Interpretacion:**
- Solo un puerto abierto (8000) = superficie de ataque minima
- Security headers presentes = proteccion contra clickjacking, XSS, MIME sniffing
- Version de uvicorn expuesta = informacion para el atacante (podria ocultarse)
- Sin directorios sensibles detectados

**Paso 3: Escaneo con OWASP ZAP**
```bash
docker run --rm -v $(pwd):/zap/wrk ghcr.io/zaproxy/zaproxy:stable \
  zap-baseline.py -t http://host.docker.internal:8000 -r zap-report.html
```

**Analisis de resultados esperados:**
```
PASS: Anti-CSRF tokens scanner
PASS: Path Traversal scanner
PASS: SQL Injection scanner
PASS: XSS scanner
WARN: Content Security Policy (CSP) could be strengthened
INFO: Server leaks version via Server header
```

**Interpretacion:**
- PASS en las pruebas de inyeccion = las defensas funcionan
- La advertencia de CSP es configuracion mejorable, no vulnerabilidad
- La fuga de version del servidor es informativa, baja prioridad

---

## Ejercicio 2: Probar Ataques Comunes Contra la App Segura

**Enunciado:** Ejecutar ataques de SQL injection, path traversal y XSS, demostrando que la app segura los bloquea.

**Solucion paso a paso:**

**Ataque 1: SQL Injection en login**
```bash
# Intento de SQL injection en username
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin' OR '1'='1", "password":"cualquiera"}'
```

**Resultado esperado:**
```json
{"detail":"Credenciales invalidas"}
```

**Por que falla el ataque:** La app NO concatena el string en la query SQL. Usa SQLAlchemy ORM con consultas parametrizadas:
```python
user = db.query(User).filter(User.username == username).first()
```
Esto escapa automaticamente los caracteres especiales. La inyeccion se convierte en una busqueda literal del username `"admin' OR '1'='1"`.

**Ataque 2: Path traversal en endpoint de archivos**
```bash
# Asumiendo que intentamos leer /etc/passwd (si existiera un endpoint de archivos)
curl -X GET "http://localhost:8000/api/files/read?filename=../../../etc/passwd" \
  -H "Authorization: Bearer TOKEN"
```

**Resultado esperado:** 404 Not Found (el endpoint no existe) o 422 Validation Error.

**Por que falla el ataque:** La app segura no expone endpoints que lean archivos del sistema. Si los tuviera, se implementaria sanitizacion con normalizacion de rutas y verificacion de directorio base.

**Ataque 3: XSS en campos de texto**
```bash
# Registrar un item con codigo JS
TOKEN=$(curl -s -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"TestPass123"}' | \
  python -c "import sys,json; print(json.load(sys.stdin)['access_token'])")

curl -X POST http://localhost:8000/api/items/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"<script>alert(1)</script>","description":"<img src=x onerror=alert(2)>"}'
```

**Resultado esperado:** El item se crea correctamente, pero el contenido se devuelve escapado:
```json
{
  "title": "<script>alert(1)</script>",
  "description": "<img src=x onerror=alert(2)>"
}
```

**Por que falla el ataque:** FastAPI con Pydantic escapa automaticamente los caracteres HTML en las respuestas JSON. El script se almacena como texto inofensivo. Si hubiera un frontend que renderice sin escapar, ahi estaria el riesgo, pero en la API solo se devuelve JSON.

**Ataque 4: Fuerza bruta en login**
```bash
# Script simple de fuerza bruta (debe fallar por rate limiting)
for i in $(seq 1 10); do
  curl -s -X POST http://localhost:8000/auth/login \
    -H "Content-Type: application/json" \
    -d '{"username":"admin","password":"pass'$i'"}' &
done
```

**Resultado esperado:** Despues de 5 intentos, retorna 429 Too Many Requests:
```json
{"detail":"Limite de requests excedido. Maximo: 5 por 60s"}
```

**Por que falla el ataque:** El rate limiter cuenta los intentos por IP y bloquea despues de 5 requests en 60 segundos.

---

## Ejercicio 3: Usar Burp Suite Proxy para Interceptar y Modificar Requests

**Enunciado:** Configurar Burp Suite como proxy, interceptar un request de login y modificar parametros.

**Solucion paso a paso:**

**Paso 1: Configurar Burp Suite**
1. Abrir Burp Suite (Community Edition es suficiente)
2. Ir a la pestana Proxy > Options
3. Por defecto escucha en 127.0.0.1:8080
4. Ir a Proxy > Intercept y hacer clic en "Intercept is on"

**Paso 2: Configurar el cliente para usar el proxy**
```bash
# Con curl usando proxy
curl -x http://127.0.0.1:8080 \
  -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"TestPass123"}'
```

En Burp Suite, interceptar el request y modificarlo:
- Cambiar el body a `{"username":"admin","password":"WrongPass"}`
- Hacer clic en "Forward" para enviar el request modificado

**Analisis:**
- El request modificado debe ser rechazado con 401 si las credenciales son invalidas
- La app no tiene vulnerabilidas de logica en la autenticacion
- Burp permite ver los headers de seguridad en la respuesta

**Paso 3: Probar manipulacion de JWT**
1. Interceptar un request autenticado
2. Modificar el token JWT (cambiar el payload en base64)
3. Observar que la firma no valida y retorna 401

```bash
# Obtener token
TOKEN=$(curl -s -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"TestPass123"}' | \
  python -c "import sys,json; print(json.load(sys.stdin)['access_token'])")

# Decodificar payload (JWT es base64url)
PAYLOAD=$(echo $TOKEN | cut -d. -f2 | base64 -d 2>/dev/null || \
  echo $TOKEN | cut -d. -f2 | python -c "import sys,base64; print(base64.urlsafe_b64decode(sys.stdin.read() + '=='))")
echo $PAYLOAD
# {"sub":"1","exp":...,"type":"access","iat":...}

# Modificar sub y re-encodear (la firma no va a validar)
# El servidor detectara la manipulacion y retornara 401
```

---

## Ejercicio 4: Demostrar que la App NO es Vulnerable

**Enunciado:** Recorrer cada defensa implementada y demostrar que bloquea un ataque especifico.

**Solucion:**

| Defensa | Ataque que bloquea | Evidencia |
|---------|-------------------|-----------|
| Validacion Pydantic | Inyeccion de tipos, buffer overflow | Request con tipos invalidos retorna 422 |
| SQLAlchemy ORM | SQL injection | Username `' OR '1'='1` no altera la query |
| Password hashing (bcrypt) | Exposicion de contrasenas | BD almacena hash, no texto plano |
| JWT con firma HMAC | Manipulacion de token | Token modificado retorna 401 |
| Verificacion de ownership (IDOR) | Acceso a recursos ajenos | Cambiar item_id de otro usuario retorna 403 |
| Role checker (RBAC) | Escalada de privilegios | Usuario user no puede acceder a rutas admin |
| Rate limiting | Fuerza bruta | 5+ intentos por minuto retorna 429 |
| Security headers | Clickjacking, XSS reflectivo | Headers presentes en cada respuesta |
| CORS restrictivo | CSRF desde origenes no autorizados | Request desde otro origen es bloqueado por navegador |
| Logging seguro | Exposicion de datos sensibles en logs | Contrasenas y tokens son redactados |

**Demostracion en vivo del flujo completo:**

```bash
# 1. Escaneo inicial - SOLO un puerto abierto
nmap -p- localhost

# 2. Intento de SQL injection
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"'\'' OR 1=1 --","password":"x"}'
# Respuesta: 401 Credenciales invalidas

# 3. Registro con contrasena debil
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","username":"test","password":"123"}'
# Respuesta: 422 Validation Error

# 4. Acceso sin token
curl http://localhost:8000/api/items/
# Respuesta: 401 Unauthorized

# 5. Acceso con token manipulado
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIn0.firma" \
  http://localhost:8000/api/items/
# Respuesta: 401 Unauthorized

# 6. Fuerza bruta
for i in $(seq 1 6); do
  curl -s -o /dev/null -w "%{http_code}\n" \
    -X POST http://localhost:8000/auth/login \
    -H "Content-Type: application/json" \
    -d "{\"username\":\"admin\",\"password\":\"pass$i\"}"
done
# Output: 401, 401, 401, 401, 401, 429

# 7. IDOR
TOKEN=$(curl -s -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"TestPass123"}' | \
  python -c "import sys,json; print(json.load(sys.stdin)['access_token'])")

curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/items/9999
# Respuesta: 404 Not Found (item no existe)

# 8. Security headers
curl -s -D - http://localhost:8000/health | head -n 20
# Output incluye: x-content-type-options, x-frame-options, etc.
```

```bash
# 9. Escaneo completo con OWASP ZAP (simulado)
echo "Resumen del reporte ZAP:"
echo "  SQL Injection: PASS (0 alertas)"
echo "  XSS: PASS (0 alertas)"
echo "  Path Traversal: PASS (0 alertas)"
echo "  CSRF: PASS (0 alertas)"
echo "  Security Headers: PASS (todos presentes)"
echo "  Resultado: No se encontraron vulnerabilidades criticas"
```

---

## Preguntas y Respuestas

**1. Cual es la diferencia entre pentesting manual y automatizado?**

El pentesting manual es realizado por un humano que puede encadenar vulnerabilidades, entender logica de negocio y encontrar fallos creativos. El automatizado usa herramientas que buscan patrones conocidos y es mas rapido pero menos profundo. Ambos se complementan.

**2. Que informacion proporciona nmap sobre la app y por que es util para un atacante?**

nmap revela: puertos abiertos, servicios y versiones, sistema operativo, scripts HTTP habilitados. Para un atacante, esto permite identificar posibles vectores de ataque (ej: version desactualizada de uvicorn, directorios expuestos).

**3. Por que SQLAlchemy ORM previene SQL injection?**

SQLAlchemy ORM usa consultas parametrizadas (prepared statements). Los valores de los parametros se envian por separado de la estructura SQL. El motor de BD trata los parametros como datos, no como codigo SQL ejecutable, haciendo imposible la inyeccion.

**4. Que es Burp Suite y como se usa en pentesting?**

Burp Suite es un proxy de interceptacion que se coloca entre el navegador y el servidor. Permite interceptar, inspeccionar y modificar requests HTTP/S. Incluye herramientas como Repeater (repetir requests), Intruder (ataques de fuerza bruta), Scanner (vulnerabilidades), Decoder.

**5. Que demostro el rate limiting en el ejercicio de fuerza bruta?**

Demostro que despues de 5 intentos de login en 60 segundos, el servidor retorna 429 Too Many Requests. Esto hace que los ataques de fuerza bruta sean impracticables: probar 10,000 contrasenas tomarias 33 horas minimo.

**6. Por que el JWT no puede ser manipulado aunque el payload sea visible?**

El JWT tiene tres partes: header, payload y signature. El payload esta solo codificado en base64 (no cifrado), cualquiera puede leerlo. Pero la firma se genera con una clave secreta que solo el servidor conoce. Si se modifica el payload, la firma no coincide y el servidor rechaza el token.

**7. Que es OWASP ZAP y que tipo de pruebas realiza?**

OWASP ZAP (Zed Attack Proxy) es una herramienta DAST (Dynamic Application Security Testing) de codigo abierto. Realiza pruebas de SQL injection, XSS, path traversal, CSRF, configuracion insegura, y mas. Puede ejecutarse en modo automatico (zap-baseline, zap-full-scan) o manual.

---

## Tarea / Lectura Recomendada

- Ejecutar OWASP ZAP contra la app segura y analizar el reporte generado
- Leer: OWASP Testing Guide (https://owasp.org/www-project-web-security-testing-guide/)
- Leer: Metodologia de pentesting de PTES (http://www.pentest-standard.org/)
- Practicar: Usar Burp Suite Repeater para modificar requests JWT
- Preparacion: Tener listos los proyectos para la clase 31


