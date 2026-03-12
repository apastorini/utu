# DIAGRAMAS Y VISUALIZACIONES PEDAGÓGICAS

## 1. ARQUITECTURA DE SEGURIDAD EN CAPAS

```
┌─────────────────────────────────────────────────────────────────┐
│                    DEFENSA EN PROFUNDIDAD                       │
│                    (Defense in Depth)                           │
└─────────────────────────────────────────────────────────────────┘

    ┌───────────────────────────────────────────────────┐
    │         CAPA 7: POLÍTICAS Y PROCEDIMIENTOS        │
    │  • Políticas de seguridad                         │
    │  • Capacitación de usuarios                       │
    │  • Respuesta a incidentes                         │
    └───────────────────────────────────────────────────┘
            ┌───────────────────────────────────────┐
            │    CAPA 6: DATOS                      │
            │  • Cifrado en reposo                  │
            │  • DLP (Data Loss Prevention)         │
            │  • Clasificación de datos             │
            └───────────────────────────────────────┘
                    ┌───────────────────────────┐
                    │  CAPA 5: APLICACIÓN       │
                    │  • WAF                    │
                    │  • Input validation       │
                    │  • Secure coding          │
                    └───────────────────────────┘
                            ┌───────────────┐
                            │ CAPA 4: HOST  │
                            │ • Antivirus   │
                            │ • EDR         │
                            │ • Hardening   │
                            └───────────────┘
                                    ┌───┐
                                    │RED│
                                    │IDS│
                                    │FW │
                                    └───┘
                                      │
                                  PERÍMETRO
```

## 2. FLUJO DE AUTENTICACIÓN CON JWT

```
┌──────────┐                                    ┌──────────┐
│ Cliente  │                                    │ Servidor │
└────┬─────┘                                    └────┬─────┘
     │                                               │
     │ 1. POST /login                                │
     │    {username, password}                       │
     │──────────────────────────────────────────────>│
     │                                               │
     │                                               │ 2. Verificar
     │                                               │    credenciales
     │                                               │
     │ 3. 200 OK                                     │
     │    {token: "eyJhbGc..."}                      │
     │<──────────────────────────────────────────────│
     │                                               │
     │ 4. Guardar token                              │
     │    localStorage.setItem('token', ...)         │
     │                                               │
     │ 5. GET /api/datos                             │
     │    Authorization: Bearer eyJhbGc...           │
     │──────────────────────────────────────────────>│
     │                                               │
     │                                               │ 6. Verificar
     │                                               │    firma JWT
     │                                               │
     │ 7. 200 OK                                     │
     │    {datos: [...]}                             │
     │<──────────────────────────────────────────────│
     │                                               │

ESTRUCTURA DEL JWT:
┌────────────────────────────────────────────────────────────┐
│ HEADER.PAYLOAD.SIGNATURE                                   │
├────────────────────────────────────────────────────────────┤
│                                                            │
│ HEADER (Base64):                                           │
│ {                                                          │
│   "alg": "HS256",                                          │
│   "typ": "JWT"                                             │
│ }                                                          │
│                                                            │
│ PAYLOAD (Base64):                                          │
│ {                                                          │
│   "sub": "1234567890",                                     │
│   "name": "Juan Pérez",                                    │
│   "iat": 1516239022,                                       │
│   "exp": 1516242622                                        │
│ }                                                          │
│                                                            │
│ SIGNATURE:                                                 │
│ HMACSHA256(                                                │
│   base64UrlEncode(header) + "." +                          │
│   base64UrlEncode(payload),                                │
│   secret                                                   │
│ )                                                          │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

## 3. ATAQUE MAN-IN-THE-MIDDLE (MITM)

```
SIN CIFRADO (HTTP):
┌─────────┐                                          ┌─────────┐
│ Cliente │                                          │ Servidor│
└────┬────┘                                          └────┬────┘
     │                                                    │
     │ GET /login?user=admin&pass=123                    │
     │───────────────────────────────>                   │
     │                            │                      │
     │                            │                      │
     │                       ┌────▼────┐                 │
     │                       │ Atacante│                 │
     │                       │  (MITM) │                 │
     │                       └────┬────┘                 │
     │                            │                      │
     │                            │ Captura credenciales │
     │                            │ user=admin           │
     │                            │ pass=123             │
     │                            │                      │
     │                            └─────────────────────>│
     │                                                    │
     │<───────────────────────────────────────────────────│
     │                                                    │

CON CIFRADO (HTTPS):
┌─────────┐                                          ┌─────────┐
│ Cliente │                                          │ Servidor│
└────┬────┘                                          └────┬────┘
     │                                                    │
     │ Handshake TLS                                     │
     │<──────────────────────────────────────────────────>│
     │                                                    │
     │ 🔒 Datos cifrados: a8f3b2c9d1e4...                │
     │───────────────────────────────>                   │
     │                            │                      │
     │                       ┌────▼────┐                 │
     │                       │ Atacante│                 │
     │                       │  (MITM) │                 │
     │                       └────┬────┘                 │
     │                            │                      │
     │                            │ ❌ Solo ve datos     │
     │                            │    cifrados          │
     │                            │    (inútiles)        │
     │                            │                      │
     │                            └─────────────────────>│
     │                                                    │
```

## 4. ARQUITECTURA DE MICROSERVICIOS SEGURA

```
┌────────────────────────────────────────────────────────────────┐
│                         INTERNET                               │
└────────────────────────┬───────────────────────────────────────┘
                         │
                    ┌────▼────┐
                    │   CDN   │ (Cloudflare, Akamai)
                    │  + WAF  │
                    └────┬────┘
                         │
                    ┌────▼────┐
                    │  Load   │
                    │Balancer │
                    └────┬────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
   ┌────▼────┐      ┌────▼────┐     ┌────▼────┐
   │  API    │      │  API    │     │  API    │
   │Gateway 1│      │Gateway 2│     │Gateway 3│
   └────┬────┘      └────┬────┘     └────┬────┘
        │                │                │
        │    ┌───────────┴───────────┐    │
        │    │                       │    │
   ┌────▼────▼────┐         ┌────────▼────▼────┐
   │ Auth Service │         │  Business Logic   │
   │   (OAuth2)   │         │   Microservices   │
   │              │         │                   │
   │ • JWT        │         │ • User Service    │
   │ • MFA        │         │ • Order Service   │
   │ • SSO        │         │ • Payment Service │
   └──────┬───────┘         └─────────┬─────────┘
          │                           │
          │         ┌─────────────────┘
          │         │
     ┌────▼─────────▼────┐
     │   Service Mesh    │
     │   (Istio/Linkerd) │
     │                   │
     │ • mTLS            │
     │ • Rate Limiting   │
     │ • Circuit Breaker │
     └─────────┬─────────┘
               │
     ┌─────────▼─────────┐
     │   Data Layer      │
     │                   │
     │ • PostgreSQL      │
     │ • Redis (cache)   │
     │ • MongoDB         │
     └───────────────────┘

SEGURIDAD POR CAPA:
• CDN/WAF: Protección DDoS, filtrado de ataques
• Load Balancer: SSL termination, health checks
• API Gateway: Autenticación, rate limiting, logging
• Auth Service: Gestión de identidades
• Service Mesh: mTLS entre servicios, observabilidad
• Data Layer: Cifrado en reposo, backups
```

## 5. CICLO DE VIDA DE UN INCIDENTE DE SEGURIDAD

```
┌──────────────────────────────────────────────────────────────┐
│          INCIDENT RESPONSE LIFECYCLE (NIST)                  │
└──────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────┐
    │  1. PREPARACIÓN                                 │
    │  • Políticas y procedimientos                   │
    │  • Herramientas (SIEM, EDR)                     │
    │  • Equipo de respuesta (CSIRT)                  │
    │  • Simulacros                                   │
    └────────────────┬────────────────────────────────┘
                     │
                     ▼
    ┌─────────────────────────────────────────────────┐
    │  2. DETECCIÓN Y ANÁLISIS                        │
    │  • Alertas de SIEM                              │
    │  • Análisis de logs                             │
    │  • Clasificación de severidad                   │
    │  • Determinar alcance                           │
    └────────────────┬────────────────────────────────┘
                     │
                     ▼
    ┌─────────────────────────────────────────────────┐
    │  3. CONTENCIÓN                                  │
    │  • Aislar sistemas afectados                    │
    │  • Bloquear IPs maliciosas                      │
    │  • Deshabilitar cuentas comprometidas           │
    │  • Preservar evidencia                          │
    └────────────────┬────────────────────────────────┘
                     │
                     ▼
    ┌─────────────────────────────────────────────────┐
    │  4. ERRADICACIÓN                                │
    │  • Eliminar malware                             │
    │  • Cerrar vulnerabilidades                      │
    │  • Actualizar sistemas                          │
    │  • Cambiar credenciales                         │
    └────────────────┬────────────────────────────────┘
                     │
                     ▼
    ┌─────────────────────────────────────────────────┐
    │  5. RECUPERACIÓN                                │
    │  • Restaurar desde backups                      │
    │  • Verificar integridad                         │
    │  • Monitoreo intensivo                          │
    │  • Retorno gradual a operación normal           │
    └────────────────┬────────────────────────────────┘
                     │
                     ▼
    ┌─────────────────────────────────────────────────┐
    │  6. LECCIONES APRENDIDAS                        │
    │  • Documentar incidente                         │
    │  • Análisis de causa raíz                       │
    │  • Actualizar procedimientos                    │
    │  • Capacitación del equipo                      │
    └─────────────────────────────────────────────────┘
                     │
                     └──────────┐
                                │
                     ┌──────────▼──────────┐
                     │  MEJORA CONTINUA    │
                     └─────────────────────┘
```

## 6. MODELO DE SEGURIDAD ZERO TRUST

```
┌──────────────────────────────────────────────────────────────┐
│                    MODELO TRADICIONAL                         │
│                   (Castle and Moat)                           │
└──────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────┐
    │          FIREWALL (Perímetro)               │
    │                                             │
    │  ┌───────────────────────────────────────┐  │
    │  │  RED INTERNA (Zona Confiable)        │  │
    │  │                                       │  │
    │  │  ✓ Acceso libre entre recursos       │  │
    │  │  ✓ Confianza implícita               │  │
    │  │  ❌ Si un atacante entra, accede a   │  │
    │  │     todo                              │  │
    │  │                                       │  │
    │  └───────────────────────────────────────┘  │
    │                                             │
    └─────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│                    MODELO ZERO TRUST                          │
│              "Never Trust, Always Verify"                     │
└──────────────────────────────────────────────────────────────┘

    Usuario/Dispositivo
           │
           ▼
    ┌─────────────┐
    │ Verificación│
    │ Identidad   │ ◄─── MFA, Certificados
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐
    │ Verificación│
    │ Dispositivo │ ◄─── Postura de seguridad
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐
    │ Evaluación  │
    │ Contexto    │ ◄─── Ubicación, hora, riesgo
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐
    │ Autorización│
    │ Granular    │ ◄─── Mínimo privilegio
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐
    │ Acceso al   │
    │ Recurso     │ ◄─── Microsegmentación
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐
    │ Monitoreo   │
    │ Continuo    │ ◄─── Análisis de comportamiento
    └─────────────┘

PRINCIPIOS CLAVE:
• Verificar explícitamente
• Usar acceso de mínimo privilegio
• Asumir que hay brechas
```

## 7. FLUJO DE CI/CD SEGURO (DevSecOps)

```
┌──────────────────────────────────────────────────────────────┐
│                  PIPELINE CI/CD SEGURO                        │
└──────────────────────────────────────────────────────────────┘

Developer
    │
    │ git push
    ▼
┌─────────────────────────────────────────────────────────────┐
│ 1. SOURCE CODE MANAGEMENT (GitHub/GitLab)                   │
│    • Branch protection                                      │
│    • Code review obligatorio                                │
│    • Signed commits                                         │
└────────────────┬────────────────────────────────────────────┘
                 │ Webhook
                 ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. BUILD                                                    │
│    ├─ Compilar código                                       │
│    └─ Ejecutar tests unitarios                              │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. SECURITY SCANNING                                        │
│    ├─ SAST (SonarQube)          ◄─ Análisis estático       │
│    ├─ Dependency Check (Snyk)   ◄─ Vulnerabilidades deps   │
│    ├─ Secret Scanning (Gitleaks)◄─ Credenciales expuestas  │
│    └─ License Compliance         ◄─ Licencias permitidas   │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼ ¿Pasa quality gate?
                 │
            ┌────┴────┐
            │   NO    │──> ❌ Build falla
            └─────────┘     Notificar desarrollador
                 │
                 │ SÍ
                 ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. BUILD DOCKER IMAGE                                       │
│    └─ docker build -t app:v1.0 .                            │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. CONTAINER SCANNING                                       │
│    ├─ Trivy                      ◄─ Vulnerabilidades OS/app │
│    ├─ Clair                      ◄─ Análisis de capas      │
│    └─ Anchore                    ◄─ Políticas de seguridad │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│ 6. PUSH TO REGISTRY                                         │
│    └─ docker push registry.com/app:v1.0                     │
│       • Signed images (Docker Content Trust)                │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│ 7. DEPLOY TO STAGING                                        │
│    └─ kubectl apply -f deployment.yaml                      │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│ 8. DYNAMIC TESTING                                          │
│    ├─ DAST (OWASP ZAP)          ◄─ Pruebas en ejecución    │
│    ├─ Penetration Testing       ◄─ Simulación de ataques   │
│    └─ API Security Testing      ◄─ Fuzzing, injection      │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│ 9. MANUAL APPROVAL                                          │
│    └─ Security team review                                  │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│ 10. DEPLOY TO PRODUCTION                                    │
│     ├─ Blue/Green deployment                                │
│     ├─ Canary release                                       │
│     └─ Rollback automático si falla                         │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│ 11. RUNTIME PROTECTION                                      │
│     ├─ WAF (Web Application Firewall)                       │
│     ├─ RASP (Runtime Application Self-Protection)           │
│     ├─ Container runtime security (Falco)                   │
│     └─ SIEM monitoring                                      │
└─────────────────────────────────────────────────────────────┘
```

## 8. COMPARACIÓN: SIMETRICA VS ASIMETRICA

```
┌──────────────────────────────────────────────────────────────┐
│              CRIPTOGRAFÍA SIMÉTRICA (AES)                    │
└──────────────────────────────────────────────────────────────┘

Alice                                              Bob
  │                                                 │
  │ 1. Ambos tienen la MISMA clave secreta         │
  │    🔑 = "clave123"                              │
  │                                                 │
  │ 2. Alice cifra mensaje                         │
  │    Mensaje: "Hola Bob"                          │
  │    Cifrado: encrypt("Hola Bob", 🔑)            │
  │    = "a8f3b2c9"                                 │
  │                                                 │
  │ 3. Envía mensaje cifrado                       │
  │    "a8f3b2c9"                                   │
  │────────────────────────────────────────────────>│
  │                                                 │
  │                                                 │ 4. Bob descifra
  │                                                 │    decrypt("a8f3b2c9", 🔑)
  │                                                 │    = "Hola Bob"
  │                                                 │

PROBLEMA: ¿Cómo compartir la clave 🔑 de forma segura?

┌──────────────────────────────────────────────────────────────┐
│              CRIPTOGRAFÍA ASIMÉTRICA (RSA)                   │
└──────────────────────────────────────────────────────────────┘

Alice                                              Bob
  │                                                 │
  │                                                 │ 1. Bob genera
  │                                                 │    par de claves
  │                                                 │    🔓 Pública
  │                                                 │    🔐 Privada
  │                                                 │
  │ 2. Bob comparte clave pública                  │
  │    🔓                                           │
  │<────────────────────────────────────────────────│
  │                                                 │
  │ 3. Alice cifra con clave pública de Bob        │
  │    Mensaje: "Hola Bob"                          │
  │    Cifrado: encrypt("Hola Bob", 🔓)            │
  │    = "x9k2m5n8"                                 │
  │                                                 │
  │ 4. Envía mensaje cifrado                       │
  │    "x9k2m5n8"                                   │
  │────────────────────────────────────────────────>│
  │                                                 │
  │                                                 │ 5. Bob descifra
  │                                                 │    con su clave
  │                                                 │    privada
  │                                                 │    decrypt("x9k2m5n8", 🔐)
  │                                                 │    = "Hola Bob"
  │                                                 │

VENTAJA: No necesita canal seguro para intercambiar claves

HÍBRIDO (TLS/SSL):
1. Usar RSA para intercambiar clave simétrica
2. Usar AES para cifrar datos (más rápido)
```

## 9. ATAQUE DE FUERZA BRUTA - VISUALIZACIÓN

```
┌──────────────────────────────────────────────────────────────┐
│           ATAQUE DE FUERZA BRUTA A PASSWORD                  │
└──────────────────────────────────────────────────────────────┘

Atacante intenta todas las combinaciones posibles:

Password: 4 dígitos numéricos (0000-9999)
Espacio de búsqueda: 10^4 = 10,000 combinaciones

Intento 1: 0000 ❌
Intento 2: 0001 ❌
Intento 3: 0002 ❌
...
Intento 1234: 1234 ✓ ¡ENCONTRADO!

Tiempo: 1234 intentos × 0.1 seg = 123.4 segundos

┌──────────────────────────────────────────────────────────────┐
│              COMPLEJIDAD DE CONTRASEÑAS                      │
└──────────────────────────────────────────────────────────────┘

Tipo                  Caracteres  Longitud  Combinaciones  Tiempo*
─────────────────────────────────────────────────────────────────
Solo números          10          4         10^4           < 1 min
Solo minúsculas       26          6         26^6           5 min
Alfanumérico          62          8         62^8           2 días
+ Símbolos            94          10        94^10          63 años
+ Símbolos            94          12        94^12          475,000 años

* Asumiendo 1 billón de intentos/segundo

DEFENSA:
• Longitud mínima: 12 caracteres
• Complejidad: Mayúsculas + minúsculas + números + símbolos
• Rate limiting: Máximo 5 intentos por minuto
• Account lockout: Bloquear tras 10 intentos fallidos
• MFA: Segundo factor de autenticación
```

## 10. ANATOMÍA DE UN ATAQUE DE PHISHING

```
┌──────────────────────────────────────────────────────────────┐
│                  EMAIL DE PHISHING                           │
└──────────────────────────────────────────────────────────────┘

De: seguridad@bancoo-uruguay.com  ◄─── 🚩 Dominio falso (bancoo vs banco)
Para: victima@ejemplo.com
Asunto: URGENTE - Verificación de cuenta ◄─── 🚩 Urgencia artificial

Estimado cliente,                      ◄─── 🚩 Saludo genérico

Detectamos actividad sospechosa en su cuenta.
Por favor, verifique su identidad haciendo clic aquí:

[Verificar Cuenta Ahora]                ◄─── 🚩 Botón malicioso
 └─> http://banco-falso.com/login      ◄─── 🚩 URL sospechosa

Si no verifica en 24 horas, su cuenta será bloqueada.
                                        ◄─── 🚩 Amenaza

Atentamente,
Banco Uruguay                           ◄─── 🚩 Sin firma digital

┌──────────────────────────────────────────────────────────────┐
│              PÁGINA FALSA DE LOGIN                           │
└──────────────────────────────────────────────────────────────┘

http://banco-falso.com/login           ◄─── 🚩 HTTP (no HTTPS)

┌────────────────────────────────────┐
│  🏦 Banco Uruguay                  │  ◄─── Logo robado
├────────────────────────────────────┤
│                                    │
│  Usuario: [____________]           │
│                                    │
│  Contraseña: [____________]        │
│                                    │
│  [  Ingresar  ]                    │
│                                    │
└────────────────────────────────────┘
         │
         │ Víctima ingresa credenciales
         ▼
┌────────────────────────────────────┐
│  Atacante captura:                 │
│  • Usuario: juan.perez             │
│  • Contraseña: MiPass123           │
│  • IP: 192.168.1.100               │
│  • Navegador: Chrome               │
└────────────────────────────────────┘
         │
         │ Redirige a sitio real
         ▼
https://www.banco-uruguay.com
(Víctima no sospecha nada)

INDICADORES DE PHISHING:
✓ Verificar remitente completo
✓ Pasar mouse sobre enlaces (sin hacer clic)
✓ Buscar errores ortográficos
✓ Verificar HTTPS y certificado
✓ Contactar directamente a la empresa
```

Estos diagramas pueden ser renderizados en Markdown viewers o convertidos a imágenes para presentaciones.

