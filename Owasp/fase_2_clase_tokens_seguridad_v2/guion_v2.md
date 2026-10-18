# Guion v2 — Tokens de identidad: de Basic al DPoP

**Clase completa versión 2.0 · Foco: seguridad ofensiva *autorizada* y defensa · Incluye el caso ID Uruguay.**

**Edición 2.0:** Enfoque renovado en "qué es y qué NO es la seguridad con bearer token", con énfasis en seguridad dinámica, PKCE, App Attestation, MFA Step-Up y análisis de riesgo para clientes públicos.

---

## Índice

0. Cómo usar esta clase y reglas de ética/legal
1. El mapa completo: todos los enfoques para abordar la seguridad de APIs
2. Taxonomía de las APIs: qué estamos protegiendo exactamente
3. Historia: de las credenciales al token atado
4. Los protocolos involucrados, de HTTP a DPoP
5. Módulos técnicos (M1–M14)
6. La seguridad de API más allá del token, dominio por dominio
7. Laboratorio paso a paso (con ejemplos)
8. Glosario de atajos
9. Plantilla de reporte responsable
10. Bibliografía
11. Preguntas frecuentes (FAQ)

---

## 0. Cómo usar esta clase y reglas de ética/legal

### Cómo está armada
Cada tecnología (Basic → DPoP) se explica con la misma estructura:

1. **Idea** — qué problema resuelve y cuándo nació (primera aparición).
2. **Guion para explicar** — lo que decís en la charla / clase (texto hablado).
3. **Ejemplo que puedo hacer** — algo concreto, reproducible, sin riesgo.
4. **Vulnerabilidades y cómo comprobarlas** — el "modo seguridad": qué puede fallar y cómo se verifica **en un entorno propio o autorizado**.
5. **Defensa** — qué control mitiga ese fallo y con qué norma se referencia.

**La clase no termina en los tokens.** El documento cubre la seguridad de una API **completa**:
- La **Sección 1** presenta *todos* los enfoques posibles para hablar de seguridad de APIs (30 lentes).
- La **Sección 2** es una **taxonomía**: qué tipos de API existen y qué riesgo trae cada uno.
- La **Sección 3** son los **módulos técnicos de tokens** (M1–M14), de Basic al DPoP.
- La **Sección 4** recorre, **dominio por dominio**, todo lo demás que hay que asegurar.

### Reglas de ética y legal (leé esto antes de cualquier prueba)

> **Regla de oro:** probá vulnerabilidades únicamente contra (a) sistemas que vos construiste, (b) laboratorios diseñados para ser vulnerables, o (c) sistemas para los que tenés **autorización por escrito** y un alcance definido.
>
> Probar autenticación, robar/reutilizar tokens o manipular identificadores de objetos en sistemas de terceros **sin autorización** es acceso no autorizado y es delito.

Buenas prácticas mínimas:
- **Tu cuenta, tu sesión, tu cliente:** observar tu propio token en tu propio navegador es legítimo.
- **Alcance escrito:** si vas a probar algo que no es tuyo, pedí permiso y guardá el correo/RFC de autorización.
- **No exfiltrás datos:** si encontrás algo, demostrá el acceso con el mínimo dato necesario.
- **Divulgación responsable:** reportá al dueño del sistema o a su CERT. En Uruguay: **CERTuy (AGESIC)**.
- **Laboratorios recomendados:** OWASP crAPI, DVGA, OWASP Juice Shop, VAmPI, PortSwigger Web Security Academy.

*Herramientas de la clase:* `curl`, navegador con DevTools, Burp Suite Community / ZAP, `jwt_tool`, `PyJWT` (Python), `docker`, `gitleaks`/`ggshield`.

---

## 1. El mapa completo: todos los enfoques para abordar la seguridad de APIs

No existe **una** forma de mirar la seguridad de una API. Existen muchas, y cada una ilumina algo distinto y esconde el resto.

**Las tres preguntas que ordenan todo:**
- **Familia A — qué se mira:** el objeto de estudio.
- **Familia B — cómo se defiende:** los mecanismos.
- **Familia C — para quién y por qué:** el contexto.

### Familia A — Enfoques según QUÉ se mira

**1.1 Enfoque por capas de arquitectura.**
- *Pregunta central:* ¿en qué capa vive el control y en qué capa vive el atacante?
- *Qué mira:* cliente → red → gateway → autenticación → autorización → lógica de negocio → datos.

**1.2 Enfoque por actor: persona, sistema y delegación.**
- *Pregunta central:* ¿quién invoca la API y en nombre de quién?
- *Qué mira:* humano (browser/app), máquina (M2M), y el caso híbrido de un servicio actuando por una persona.

**1.3 Enfoque por ciclo de vida de la credencial.**
- *Pregunta central:* ¿en qué eslabón se puede robar, reutilizar o perpetuar este token?
- *Qué mira:* emisión → transporte → almacenamiento → uso → renovación → revocación → expiración.

**1.4 Enfoque por ciclo de vida del software (shift-left).**
- *Pregunta central:* ¿en qué fase del desarrollo se introduce y se detecta el riesgo?

**1.5 Enfoque por superficie de ataque.**
- *Pregunta central:* ¿desde dónde me atacan y con qué activo?
- *Qué mira:* cliente (token en JS/localStorage) · red (TLS, proxies) · backend (validación de claims) · cadena de suministro (CI, dependencias) · negocio (abuso de flujos).

**1.6 Enfoque por dato y contrato.**
- *Pregunta central:* ¿qué datos cruzan la API y qué promete el contrato?

**1.7 Enfoque por estilo de API.**
- *Pregunta central:* ¿cómo cambian los riesgos según el paradigma (REST, GraphQL, gRPC, SOAP, WebSocket, webhooks)?

**1.8 Enfoque por protocolo y transporte.**
- *Pregunta central:* ¿qué garantiza (y qué no) el canal?

**1.9 Enfoque por tipo de consumidor.**
- *Pregunta central:* ¿la API es para mi propio front, para un partner, para el público o para uso interno?

**1.10 Enfoque por modelo de despliegue.**
- *Pregunta central:* ¿dónde corre la API y qué cambia en cada modelo?

**1.11 Enfoque por tipo de identidad (humana vs. no humana).**
- *Pregunta central:* ¿cuántas identidades de máquina tengo frente a las humanas?

### Familia B — Enfoques según CÓMO se defiende

**1.12 Enfoque por paradigma de confianza.**
- *Pregunta central:* ¿confío en *quién sos* (identidad) o en *qué tenés* (posesión/capability)?

**1.13 Enfoque por modelo de autorización.**
- *Pregunta central:* ¿cómo se decide si esta identidad puede hacer esta acción sobre este objeto?

**1.14 Enfoque criptográfico y de gestión de claves.**
- *Pregunta central:* ¿qué firma, qué cifra y quién custodia las claves?

**1.15 Enfoque por control de tráfico.**
- *Pregunta central:* ¿qué límites y políticas aplico al caudal?

**1.16 Enfoque por validación y saneamiento.**
- *Pregunta central:* ¿confío en la entrada? (correcto: no).

**1.17 Enfoque por observabilidad y respuesta.**
- *Pregunta central:* ¿cómo sé que algo pasa, y qué hago cuando pasa?

**1.18 Enfoque por secretos, identidad de máquina y cadena de suministro.**
- *Pregunta central:* ¿dónde viven los secretos y quién los controla?

### Familia C — Enfoques según PARA QUIÉN y POR QUÉ

**1.19 Enfoque por OWASP API Security Top 10.**
- *Pregunta central:* ¿cuál de los diez riesgos tengo hoy y cómo lo pruebo?

**1.20 Enfoque por framework de threat modeling.**
- *Pregunta central:* ¿qué puede salir mal en este diseño, sistemáticamente?

**1.21 Enfoque por audiencia.**
- *Pregunta central:* ¿a quién le hablo y qué le importa?

**1.22 Enfoque por cumplimiento y regulatorio.**
- *Pregunta central:* ¿qué me exige la norma y cómo se traduce en controles?

**1.23 Enfoque por privacidad y protección de datos.**
- *Pregunta central:* ¿qué datos personales cruzan la API y con qué base legal?

**1.24 Enfoque por modelo de negocio y abuso económico.**
- *Pregunta central:* ¿qué gana un atacante con esta API, más allá de robar datos?

**1.25 Enfoque por madurez y gobierno.**
- *Pregunta central:* ¿en qué nivel estoy y hacia dónde voy?

**1.26 Enfoque por economía del atacante (modelo de amenaza).**
- *Pregunta central:* ¿cuánto le cuesta al atacante y cuánto me cuesta a mí defenderme?

**1.27 Enfoque histórico/evolutivo.**
- *Pregunta central:* ¿por qué cada tecnología nació, qué resolvió y qué dejó abierto?

**1.28 Enfoque académico/formal.**
- *Pregunta central:* ¿qué principios de diseño se están violando?

**1.29 Enfoque por resiliencia y disponibilidad.**
- *Pregunta central:* ¿qué pasa cuando algo falla o me saturan?

**1.30 Enfoque por anti-patrones.**
- *Pregunta central:* ¿qué errores concretos se repiten en la industria?

---

## 2. Taxonomía de las APIs: qué estamos protegiendo exactamente

### 2.1 Por estilo o paradigma

| Estilo | Riesgos característicos |
|---|---|
| **REST** | BOLA/BFLA, over-fetching, versionado laxo, IDOR |
| **GraphQL** | Consultas profundas, *introspection* expuesta, BOLA |
| **gRPC / Protobuf** | Reflexión expuesta, falta de inspección por proxies/WAF |
| **SOAP / XML** | XXE, WS-Security mal configurado |
| **WebSocket** | Autenticación solo al inicio; autorización por mensaje |
| **Webhooks** | SSRF, falta de firma (HMAC), replay |
| **Event-driven** | Autorización por tópico, *event injection* |

### 2.2 Por tipo de consumidor

- **First-party:** tus propios front-ends (SPA, móvil).
- **Interno (servicio a servicio):** tráfico este-oeste.
- **Partner / B2B:** relación contractual.
- **Público / open API:** sin relación previa.
- **Marketplace de terceros:** aplicaciones de otros sobre tus datos.

---

## 3. Historia: de las credenciales al token atado

### 3.1 Era 1 — La credencial viaja en cada request (1993–1999)

**HTTP Basic** (RFC 2617, 1999) y **Digest** (RFC 7616, 2015).

- **Qué resolvía:** autenticación mínima, sin estado.
- **Qué no resolvía:** la credencial viaja una y otra vez.

### 3.2 Era 2 — La federación en XML (2002–2005)

**WS-Security** (OASIS, 2004) y **SAML 2.0** (OASIS, 2005).

- **Qué aportó:** identidad federada, SSO, firmas.
- **Por qué no conquistó las APIs:** XML, verboso, pesado.

### 3.3 Era 3 — La clave estática (2006 en adelante)

**API keys** (AWS, 2006).

- **Qué resolvió:** identificar aplicaciones sin montar un servidor de identidad.
- **Dónde vive la falla:** no expira, no distingue permisos finos, y si se filtra es impersonación directa.

### 3.4 Era 4 — Firmar cada request (2007–2010)

**OAuth 1.0** (RFC 5849, 2010).

- **Qué aportó:** un request robado no se podía reutilizar sin la clave.
- **Por qué se abandonó:** muy difícil de implementar bien.

### 3.5 El giro (octubre de 2012): bearer sí, MAC no

**OAuth 2.0** (RFC 6749) y **bearer token** (RFC 6750).

- El propio OAuth 2.0 **había definido además el tipo `mac`**, pero se **abandonó**.
- **RFC 6749, §10.3:** el servidor de recursos *no puede* confirmar que el token fue emitido al cliente que lo presenta.

### 3.6 La consolidación (2014–2025): ponerle cinturón al bearer

| Año | Aporte | Qué agrega |
|---|---|---|
| 2013 | Revocación de tokens (RFC 7009) | cortar antes de la expiración |
| 2014 | OpenID Connect Core 1.0 | identidad (ID token) sobre OAuth |
| 2015 | JWT (RFC 7519) · PKCE (RFC 7636) · Introspección (RFC 7662) | claims; candado al código; validar tokens opacos |
| 2018 | Token Binding (RFC 8471-8473) | atar el token al canal TLS (sin adopción masiva) |
| 2020 | mTLS atado a certificado (RFC 8705) · JWT BCP (RFC 8725) | tokens *sender-constrained*; reglas de validación JWT |
| 2021 | Perfil JWT para access tokens (RFC 9068) | interoperabilidad; `exp` obligatorio |
| 2023 | DPoP (RFC 9449) | prueba de posesión por request, sin PKI |
| 2025 | RFC 9700 · NIST SP 800-63-4 | mejores prácticas y sender-constrained/PKCE recomendados |

### 3.7 Lo que enseña la historia (cinco moralejas)

1. **Todo token portador es una contraseña portátil.**
2. **La simplicidad gana primero y cobra después.**
3. **Cada capa de esta historia sigue viva.**
4. **La vida del token importa más que su creación.**
5. **El token es una sola pieza.**

---

## 4. Los protocolos involucrados, de HTTP a DPoP

### 4.1 Red y transporte

#### HTTP/1.1, HTTP/2 y HTTP/3 (QUIC)
- Los tokens viajan en **cabeceras** (`Authorization`), **cookies** o, mal, en la **query string**.
- **RFC 9700 (2025)** prohíbe el token en la URL.

#### TLS / SSL y mTLS
- **SSL** (Netscape, mediados de los 90) fue el origen; hoy hablamos de **TLS 1.2/1.3**.
- **mTLS** (mutual TLS) hace que *ambas* partes presenten certificado.

### 4.2 Autenticación HTTP clásica

#### HTTP Basic y Digest (RFC 2617 → RFC 7616)
- Basic manda `usuario:contraseña` en **Base64** (no es cifrado).
- Digest manda un **hash** con *nonce*.

#### Cookies de sesión (RFC 6265)
- El ID de sesión es, en la práctica, **un bearer token guardado en el navegador**.

#### API keys
- Un secreto estático que identifica al cliente (no al usuario).

### 4.3 Federación en XML

#### WS-Security, SAML 2.0 y XML-DSig
- **SAML 2.0** (OASIS, 2005) transporta **aserciones** de identidad firmadas.
- **Qué mirar:** *XML Signature Wrapping*, canonicalización, condiciones ignoradas.

### 4.4 OAuth y OpenID Connect

#### OAuth 1.0 (RFC 5849)
- Firma de cada request con **HMAC-SHA1**.

#### OAuth 2.0 (RFC 6749) y bearer (RFC 6750)
- Cuatro roles: **dueño**, **cliente**, **servidor de autorización**, **servidor de recursos**.

#### El tipo MAC (abandonado)
- **Primera aparición:** borrador de febrero de 2012; **abandonado**.
- **Por qué importa:** es el **eslabón perdido**: lo que hoy reintentan **mTLS** y **DPoP**.

#### PKCE (RFC 7636)
- **Primera aparición:** 2015. Obligatorio en **authorization code** según RFC 9700 (2025).
- **Cómo funciona:** el cliente genera un `code_verifier`, manda su hash (`code_challenge`) al pedir el código, y prueba el `verifier` al canjearlo.

#### OpenID Connect (OIDC Core 1.0)
- Una capa de **identidad** sobre OAuth 2.0. Agrega el **ID token** (un JWT con `iss`, `sub`, `aud`, `exp`, `amr`, `acr`).

#### Introspección (RFC 7662) y revocación (RFC 7009)
- El primero permite que el servidor de recursos **pregunte** al de autorización si un token sigue válido; el segundo permite **revocarlo**.

### 4.5 JOSE: la familia de JWT

- **JWS (RFC 7515):** firma. **JWE (RFC 7516):** cifrado. **JWK (RFC 7517):** claves. **JWA (RFC 7518):** algoritmos. **JWT (RFC 7519):** el token con claims.
- **Está firmado, no cifrado**: el payload se lee.

### 4.6 Atar el token a su portador

#### Token Binding (RFC 8471-8473)
- **Primera aparición:** 2018. Ataba el token al **canal** (TLS) en el que se emitió.
- **Qué pasó:** **sin adopción masiva**; quedó como intento.

#### mTLS atado a certificado (RFC 8705)
- **Primera aparición:** 2020.
- El token queda **ligado al `cnf` (thumbprint) del certificado** del cliente.

#### DPoP (RFC 9449)
- **Primera aparición:** 2023.
- El cliente firma una **prueba** (un JWT propio) con su clave privada, atada al request vía `htm` (método) y `htu` (URL), con `jti` único y `iat`.

### 4.7 Factores de autenticación (MFA)

**La MFA protege la emisión, no el uso.**

- **OTP: HOTP (RFC 4226, 2005) y TOTP (RFC 6238, 2011).**
- **Push y notificaciones:** cómodas y **phishable** (fatiga MFA).
- **Passkeys / WebAuthn-FIDO2 (W3C/FIDO):** llaves resistentes al *phishing*.
- **NIST SP 800-63-4 (2025):** marco de identidad digital; empuja lo *phishing-resistant*.

### 4.8 Gestión de identidades y otros estándares

- **SCIM (RFC 7643/7644, 2015):** aprovisionamiento de usuarios.
- **LDAP / Kerberos:** directorios y autenticación **corporativa**.
- **RADIUS:** autenticación de **red** (VPN, Wi-Fi corporativo).
- **Zero Trust (NIST SP 800-207, 2020):** no confiar por estar "dentro"; verificar **cada** solicitud.

---

## 5. Módulos técnicos

### M1 — HTTP Basic / Digest (1999)

#### Idea
Autenticación HTTP clásica: el cliente manda credenciales en **cada** petición.

#### Guion para explicar
"Basic es como darle a alguien la llave de tu casa para que entre a revisar una habitación: le das la llave, no un permiso para esa habitación. Viaja en cada request, y si mirás el valor, no está cifrado: está codificado. Base64 no es seguridad; es transporte tolerante a caracteres."

#### Vulnerabilidades
- Credenciales reutilizadas por request
- No hay "logout" real
- Base64 ≠ cifrado
- Fuerza bruta
- Credenciales en logs/URLs

#### Defensa
TLS obligatorio, migrar a tokens/OIDC, rate-limit y lockout, nunca loguear credenciales.

---

### M2 — Cookies y sesiones (1996)

#### Idea
El servidor guarda el estado y el navegador repite un **identificador de sesión** en una cookie.

#### Guion para explicar
"La sesión en servidor es segura para la web tradicional y mala para APIs: el estado no escala, no delega y no cruza clientes. Pero trae dos problemas clásicos: robo de cookie por XSS y CSRF."

#### Vulnerabilidades
- Cookie sin `HttpOnly` → XSS la lee
- Sin `SameSite` → CSRF
- Session fixation
- Sesión no se invalida al logout

#### Defensa
`HttpOnly` + `Secure` + `SameSite`, rotar el ID en el login, invalidar en el servidor al logout.

---

### M3 — API keys (mediados de los 2000)

#### Idea
Un secreto estático que identifica al cliente (no al usuario).

#### Guion para explicar
"La API key es el bearer token más usado y menos cuidado del mundo. Es un identificador estático que se mete en un archivo, en una variable de entorno o —peor— en el JavaScript de un frontend, donde cualquiera lo lee."

#### Vulnerabilidades
- Clave hardcodeada en el cliente
- Clave en el repositorio
- Sin expiración ni rotación
- Sin scope ni límites

#### Defensa
Rotación, revocación, scope, IP allowlist, rate limit, secret manager, detección en CI.

---

### M4 — OAuth 1.0 (firma HMAC) (2007 / 2010)

#### Idea
Antes del bearer, OAuth **firmaba cada request** con HMAC-SHA1 y un secreto compartido.

#### Guion para explicar
"OAuth 1.0 era la antítesis del bearer: nada de mandar un string reutilizable, cada request se firmaba. Más seguro en teoría, carísimo en la práctica."

#### Vulnerabilidades
- Errores de canonicalización
- Secreto compartido filtrado
- Sin anti-replay (nonce/timestamp)

#### Defensa
Nonce + timestamp anti-replay, secretos por par, TLS. Hoy: migrar a DPoP.

---

### M5 — Bearer token (OAuth 2.0) (2012)

#### Idea
OAuth 2.0 separa autorización de autenticación y entrega al cliente un **access token**: un string con alcance y vida.

#### Guion para explicar
"El bearer ganó por simplicidad: un string en una cabecera, sin firmar cada request, sin secretos compartidos. El precio está escrito en la norma: el servidor de recursos no puede saber si quien presenta el token es a quien se le emitió."

#### Vulnerabilidades
- Replay: el token no está atado al cliente
- Token en URL/query
- Vida demasiado larga
- Sin revocación
- Sobre-privilegio

#### Defensa
Vida corta, `aud` estricto, scope mínimo, revocación (RFC 7009) e introspección (RFC 7662), nunca en query.

---

### M6 — JWT (2010 / 2015)

#### Idea
**JWT (JSON Web Token)**: `header.payload.signature`, base64url. **Está firmado, no cifrado**: el payload se lee.

#### Guion para explicar
"Un JWT es como una credencial plastificada: firmada, no sellada. Cualquiera lee el contenido. Y guarda una trampa: el header dice con qué algoritmo se firmó; si el validador le hace caso al token en lugar de a su configuración, un atacante elige el algoritmo."

#### Vulnerabilidades
- `alg: none` y confusión **RS256→HS256**
- `exp`/`aud`/`iss` sin validar
- Claves débiles crackeables
- `kid` que apunta a un JWKS controlado por el atacante

#### Defensa
`alg` **desde la configuración del validador**, nunca del token; verificar `iss`, `aud`, `exp`, `nbf`; claves fuertes; rotación de claves.

---

### M7 — OIDC, authorization code, PKCE e ID token (2014)

#### Idea
**OpenID Connect Core 1.0** es la capa de identidad sobre OAuth 2.0. **PKCE: RFC 7636, agosto de 2015.** El **ID token** es un JWT que dice *quién* es la persona y *cómo* se autenticó.

#### Guion para explicar
"El authorization code es el cupón de un solo uso que cambia un artefacto público por uno privado. PKCE le agrega un candado: aunque te roben el código, no lo podés canjear sin el verificador. Y el ID token es el DNI que te muestran en la puerta, no el pase que te ponen en la muñeca."

#### Vulnerabilidades
- Sin PKCE → código interceptable
- `redirect_uri` laxa
- Falta de `state` → CSRF
- Falta de `nonce` → replay del ID token
- ID token usado como access token

#### Defensa
PKCE obligatorio, `redirect_uri` exacta, `state` y `nonce`, validar `iss`/`aud`/`exp`/`nonce` en el RP.

---

### M8 — Refresh token (2012)

#### Idea
Token de vida larga que **sólo** se usa contra el endpoint de token para obtener nuevos access tokens.

#### Guion para explicar
"El access token es el boleto de la función; el refresh token es la acreditación que te deja pedir uno nuevo sin volver a la taquilla. La rotación convierte al refresh en un artefacto de un solo uso."

#### Vulnerabilidades
- Sin rotación
- Sin detección de reuso
- Vida infinita
- Almacenamiento inseguro

#### Defensa
Rotación + detección de reuso, vida absoluta, binding al cliente, almacenamiento seguro.

---

### M9 — mTLS y DPoP (sender-constrained) (2020 / 2023)

#### Idea
Atar el token a su portador. **mTLS + token atado a certificado: RFC 8705, febrero de 2020.** **DPoP: RFC 9449, octubre de 2023.**

#### Guion para explicar
"Si el problema del bearer es que cualquiera que lo tenga lo usa, la solución es exigir algo más que la posesión. mTLS ata el token al certificado; DPoP ata el token a una clave privada que el cliente prueba en cada request."

#### Vulnerabilidades
- DPoP sin validar `htm`/`htu`
- Replay de la prueba (`jti`)
- `ath` ausente
- mTLS mal configurado

#### Defensa
Validar `htm`, `htu`, `jti` (anti-replay), `ath`, `alg` permitido; rotación de claves.

---

### M10 — OWASP API Security Top 10 (laboratorio)

#### Idea
El "atlas" para elegir qué prober.

#### Los 10 riesgos (edición 2023)

| # | Riesgo |
|---|---|
| API1 | **BOLA** — Broken Object Level Authorization |
| API2 | **Broken Authentication** |
| API3 | **BOPLA** — Broken Property Level Authorization (Mass Assignment) |
| API4 | **Unrestricted Resource Consumption** |
| API5 | **BFLA** — Broken Function Level Authorization |
| API6 | **Sensitive Business Flows** |
| API7 | **SSRF** |
| API8 | **Misconfiguration** |
| API9 | **Improper Inventory** |
| API10 | **Unsafe Consumption** |

---

### M11 — Caso ID Uruguay (laboratorio ético)

#### Qué es
**ID Uruguay** es el proveedor de identidad del Estado uruguayo, gestionado por **AGESIC**. Se integra vía **OpenID Connect**.

#### Verificación defensiva de tu integración

| Control | Resultado esperado |
|---|---|
| **PKCE obligatorio** | `code_challenge` + `code_challenge_method=S256` |
| **`redirect_uri` exacta** | Coincidencia exacta |
| **`state` y `nonce`** | Presentes, aleatorios, de un solo uso |
| **Validación del ID token** | `iss`, `aud`, `exp`, `nonce` y firma validados |
| **ID token no se usa como access token** | Nunca |
| **Vida del access token** | Corta y acorde al riesgo |
| **Rotación de refresh token** | Rotación + detección de reuso |
| **Revocación / logout** | Invalidado |
| **Transporte** | Sólo HTTPS + header |
| **Almacenamiento en tu cliente** | Sin acceso por JS |

---

### M12 — Seguridad dinámica y MFA Step-Up (NUEVO en v2)

#### Idea
La autenticación **no es un estado binario** de "conectado/desconectado", sino un **flujo continuo** que debe exigir re-autenticación según la criticidad de la transacción.

#### Conceptos clave

**MFA Step-Up:** Pedir un segundo factor adicional para operaciones sensibles, incluso si el usuario ya está autenticado. Se implementa con `acr` (Authentication Context Class Reference) y `amr` (Authentication Methods References) en el token.

**Acciones sensibles que merecen Step-Up:**
- Transferencias de dinero
- Cambio de contraseña o email
- Acceso a datos personales sensibles
- Operaciones administrativas
- Descarga de documentos confidenciales

#### Guion para explicar
"La MFA no es un interruptor de encendido/apagado. Es más como un ascensor: subís al primer piso con contraseña, pero para subir al piso 20 necesitás una tarjeta especial. Ese es el Step-Up: pedir más garantía solo para la operación sensible."

#### Implementación
- `acr_values` en la solicitud de autorización
- `amr` en el ID token
- Paso-up en el servidor de autorización

---

### M13 — Riesgos en clientes públicos: Mobile (NUEVO en v2)

#### Idea
En aplicaciones móviles y SPAs, el cliente **es controlado por el usuario**, y un atacante puede modificar la aplicación.

**Riesgos específicos de clientes públicos:**
- **Aplicaciones modificadas (tampering):** Un atacante puede modificar el APK/IPA para desactivar SSL pinning, extraer secretos o cambiar el comportamiento
- **Root/Jailbreak:** El dispositivo está comprometido
- **Extracción de secretos:** Un atacante puede descompilar la app y extraer claves hardcodeadas

**Mitigaciones:**
- **App Attestation** (Play Integrity API / DeviceCheck): Verifica que la app no fue modificada
- **PKCE:** Protege el código de autorización
- **DPoP:** Ata el token a una clave privada
- **SSL Pinning:** Cert pinning en la app

#### Guion para explicar
"En una app móvil, el atacante tiene el control total del dispositivo. Puede modificar la app, desactivar protecciones, y extraer secretos. Por eso necesitás defensas adicionales: App Attestation para verificar la integridad, PKCE para el código, DPoP para el token."

#### Mitigaciones clave

| Mitigación | Protección |
|---|---|
| **Play Integrity API / DeviceCheck** | Verifica que la app no fue modificada |
| **PKCE** | Protege el código de autorización |
| **DPoP** | Ata el token a una clave privada |
| **SSL Pinning** | Previene MITM |

---

### M14 — Zero Trust y cadena de suministro (NUEVO en v2)

#### Idea
**Zero Trust (NIST SP 800-207, 2020):** No confiar por estar "dentro"; verificar **cada** solicitud.

**Principios:**
- Nunca confíes, siempre verifica
- Acceso con mínimo privilegio
- Asume que la red está comprometida
- Verifica cada solicitud, no solo la primera

#### Cadena de suministro

**Riesgos:**
- Secretos en CI/CD
- Dependencias de terceros
- Bibliotecas con vulnerabilidades

**Defensas:**
- Secret managers (AWS Secrets Manager, HashiCorp Vault)
- SBOM / SCA (Software Bill of Materials)
- Escaneo de secretos en CI (gitleaks, ggshield)

#### Guion para explicar
"Zero Trust es dejar de confiar por defecto. Antes, si estabas dentro de la red, confiabas en vos. Ahora, cada solicitud se verifica, sin importar de dónde venga. Y la cadena de suministro es el nuevo perímetro: si una dependencia tuya tiene una vulnerabilidad, vos también la tenés."

---

## 6. La seguridad de API más allá del token

### 6.1 Autorización a nivel de objeto (BOLA)
La pregunta no es si el token es válido, sino si esta identidad puede tocar este objeto.

### 6.2 Validación de entrada
Inyección (SQL/NoSQL/comandos), SSRF, XXE, deserialización insegura, mass assignment.

### 6.3 Gateway y control de tráfico
Cuotas, rate limiting, gestión de bots, geo/IP policy.

### 6.4 Inventario
Versiones viejas y APIs fantasma que siguen vivas.

### 6.5 Cadena de suministro
Secretos en CI y dependencias de terceros.

### 6.6 Observabilidad y respuesta
Logs, trazas, métricas, SIEM, detección de anomalías, revocación, respuesta a incidentes.

### 6.7 Cumplimiento y privacidad
En Uruguay: Ley 18.331, Decreto 66/025, reporte a CERTuy.

### 6.8 Resiliencia
DoS/DDoS, consumo de recursos, circuit breakers, degradación elegante.

---

## 7. Laboratorio paso a paso

### Laboratorio 1: Decodificar un JWT
```python
import jwt
token = jwt.encode({"sub": "123", "scope": "read", "iss": "https://mi-lab"}, "secreto", algorithm="HS256")
print(token)
print(jwt.decode(token, "secreto", algorithms=["HS256"]))
```

### Laboratorio 2: Probar PKCE
```
1) /authorize?response_type=code&client_id=lab&redirect_uri=http://localhost/cb
   &scope=openid&state=RANDOM&code_challenge=...&code_challenge_method=S256
2) el usuario (vos) se autentica en el lab
3) /cb?code=XXXX&state=RANDOM
4) POST /token  code=XXXX + code_verifier=...  -> access_token, id_token, refresh_token
```

### Laboratorio 3: Verificar DPoP
Construí una prueba **conceptual** con Python:
```python
# La prueba DPoP es un JWT firmado por el CLIENTE con su clave privada
# Header típico: {"typ":"dpop+jwt","alg":"ES256","jwk":{...}}
# Claims: jti (único), htm (método), htu (URL), iat
# El servidor rechaza si htm/htu no coinciden con el request, o si el jti se repite
```

---

## 8. Glosario de atajos

| Término | Significado |
|---|---|
| **Bearer token** | Credencial portadora: quien lo tiene, lo usa |
| **JWT** | JSON Web Token: token con claims en JSON |
| **JWS** | JSON Web Signature: firma |
| **JWE** | JSON Web Encryption: cifrado |
| **PKCE** | Proof Key for Code Exchange: candado al código de autorización |
| **DPoP** | Demonstrating Proof of Possession: prueba de posesión por request |
| **mTLS** | Mutual TLS: ambas partes se autentican con certificado |
| **BOLA** | Broken Object Level Authorization: autorización rota a nivel de objeto |
| **BFLA** | Broken Function Level Authorization: autorización rota a nivel de función |
| **MFA** | Multi-Factor Authentication: autenticación multifactor |
| **Step-Up** | Pedir más garantía para operaciones sensibles |
| **Zero Trust** | Nunca confíes, siempre verifica |
| **App Attestation** | Verificación de integridad de la app |

---

## 9. Plantilla de reporte responsable

```markdown
# Reporte de vulnerabilidad

## Resumen
[Descripción breve de la vulnerabilidad]

## Severidad
[Crítica / Alta / Media / Baja]

## Pasos para reproducir
1. [Paso 1]
2. [Paso 2]
3. [Paso 3]

## Impacto
[Qué puede hacer un atacante]

## Recomendación
[Cómo mitigar]

## Fecha
[Fecha del reporte]

## Contacto
[Tu información de contacto]
```

---

## 10. Bibliografía

- [RFC 6749](https://datatracker.ietf.org/doc/html/rfc6749) — OAuth 2.0 Authorization Framework
- [RFC 6750](https://datatracker.ietf.org/doc/html/rfc6750) — Bearer Token Usage
- [RFC 7519](https://datatracker.ietf.org/doc/html/rfc7519) — JSON Web Token (JWT)
- [RFC 7636](https://datatracker.ietf.org/doc/html/rfc7636) — PKCE
- [RFC 8705](https://datatracker.ietf.org/doc/html/rfc8705) — mTLS-based token binding
- [RFC 9449](https://datatracker.ietf.org/doc/html/rfc9449) — DPoP
- [RFC 9700](https://datatracker.ietf.org/doc/html/rfc9700) — OAuth 2.0 Security Best Current Practice
- [OWASP API Security Top 10 (2023)](https://owasp.org/API-Security/editions/2023/en/0x11-t10/)
- [NIST SP 800-63-4](https://pages.nist.gov/800-63-4/sp800-63-4.html) — Digital Identity Guidelines
- [OpenID Connect Core 1.0](https://openid.net/specs/openid-connect-core-1_0.html)
- [WebAuthn (W3C)](https://www.w3.org/TR/webauthn-2/)
- [MITRE ATT&CK](https://attack.mitre.org/)
- [AGESIC / CERTuy](https://www.gub.uy/centro-nacional-respuesta-incidentes-seguridad-informatica/)

---

## 11. Preguntas frecuentes (FAQ)

### ¿El bearer token es seguro?
Depende de cómo se use. Un bearer token con vida corta, scope mínimo, revocación y transporte seguro es razonablemente seguro. Pero no es suficiente por sí solo.

### ¿Qué es mejor: JWT o token opaco?
Depende. Los JWT son más eficientes (no requieren introspección) pero más difíciles de revocar. Los tokens opacos son más fáciles de revocar pero requieren introspección.

### ¿PKCE es necesario para todos los flujos?
PKCE es obligatorio para el flujo de código de autorización según RFC 9700 (2025). Para otros flujos, no aplica.

### ¿DPoP es mejor que mTLS?
DPoP es más fácil de implementar (no requiere PKI). mTLS es más seguro pero más complejo de gestionar.

### ¿La MFA protege al token?
No. La MFA protege el momento de la emisión, no los treinta días siguientes. Para eso se necesita Step-Up o DPoP.

### ¿Qué es Zero Trust?
Es un paradigma de seguridad que propone "nunca confiar, siempre verificar". No confiar por estar dentro de la red.

### ¿Qué es BOLA?
Broken Object Level Authorization: un atacante presenta su propio token, válido, y cambia el identificador del objeto en la URL para acceder a datos ajenos.

---

*Fin del guion v2.*
