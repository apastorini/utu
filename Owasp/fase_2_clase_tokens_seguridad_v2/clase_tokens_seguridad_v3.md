# Tokens de identidad, de Basic al DPoP — Clase completa v3

**Edición 3.0 · Foco: seguridad ofensiva *autorizada* y defensa · Incluye el caso ID Uruguay.**

**Guion + explicación + laboratorio de seguridad of APIs**
Versión 3.0 · Incluye: PKCE, MFA Step-Up, App Attestation, DPoP, mTLS, Zero Trust, gestión de secretos, threat modeling, seguridad dinámica, Shadow APIs, Single Endpoint, y análisis profundo of riesgos en clientes públicos.

---

## Índice

- 0. Cómo usar esta clase y reglas de ética/legal
- 1. El mapa completo: todos los enfoques para abordar la seguridad of APIs
- 2. Taxonomía de las APIs: qué estamos protegiendo exactamente
- 3. Historia: de las credenciales al token atado
- 4. Los protocolos involucrados, de HTTP a DPoP
- 5. Módulos técnicos (M1–M20): de Basic al DPoP
- 6. La seguridad of API más allá del token: el cuerpo completo, dominio por dominio
- 7. Laboratorio paso a paso (con ejemplos)
- 8. Glosario of atajos
- 9. Plantilla of reporte responsable
- 10. Bibliografía
- 11. Preguntas frecuentes (FAQ)

---

## 0. Cómo usar esta clase y reglas de ética/legal

### Cómo está armada
Cada tecnología (Basic → DPoP) se explica con la misma estructura:

1. **Idea** — qué problema resuelve y cuándo nació (primera aparición).
2. **Guion para explicar** — lo que decís en la charla / clase (texto hablado).
3. **Ejemplo que puedo hacer** — algo concreto, reproducible, sin riesgo.
4. **Vulnerabilidades y cómo comprobarlas** — el "modo seguridad": qué puede fallar y cómo se verifica **en un entorno propio o autorizado**.
5. **Defensa** — qué control mitiga ese fallo y con qué norma se referencia.

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

*Herramientas de la clase:* `curl`, navegador with DevTools, Burp Suite Community / ZAP, `jwt_tool`, `PyJWT` (Python), `docker`, `gitleaks`/`ggshield`.

---

## 1. El mapa completo: todos los enfoques para abordar la seguridad of APIs

No existe **una** forma de mirar la seguridad de una API. Existen muchas, y cada una ilumina algo distinto y esconde el resto.

**Las tres preguntas que ordenan todo:**
- **Familia A — qué se mira:** el objeto de estudio.
- **Familia B — cómo se defiende:** los mecanismos.
- **Familia C — para quién y por qué:** el contexto.

### Familia A — Enfoques según QUÉ se mira

**1.1 Enfoque por capas de arquitectura.**
- *Pregunta central:* ¿en qué capa vive el control y en qué capa vive el atacante?

**1.2 Enfoque por actor: persona, sistema y delegación.**
- *Pregunta central:* ¿quién invoca la API y en nombre de quién?

**1.3 Enfoque por ciclo de vida de la credencial.**
- *Pregunta central:* ¿en qué eslabón se puede robar, reutilizar o perpetuar este token?

**1.4 Enfoque por ciclo de vida del software (shift-left).**
- *Pregunta central:* ¿en qué fase del desarrollo se introduce y se detecta el riesgo?

**1.5 Enfoque por superficie de ataque.**
- *Pregunta central:* ¿desde dónde me atacan y con qué activo?

**1.6 Enfoque por dato y contrato.**
- *Pregunta central:* ¿qué datos cruzan la API y qué promete el contrato?

**1.7 Enfoque por estilo de API.**
- *Pregunta central:* ¿cómo cambian los riesgos según el paradigma?

**1.8 Enfoque por protocolo y transporte.**
- *Pregunta central:* ¿qué garantiza (y qué no) el canal?

**1.9 Enfoque por tipo de consumidor.**
- *Pregunta central:* ¿la API es para mi propio front, para un partner, para el público o para uso interno?

**1.10 Enfoque por modelo of despliegue.**
- *Pregunta central:* ¿dónde corre la API y qué cambia en cada modelo?

**1.11 Enfoque por tipo de identidad (humana vs. no humana).**
- *Pregunta central:* ¿cuántas identidades of máquina tengo frente a las humanas?

### Familia B — Enfoques según CÓMO se defiende

**1.12 Enfoque por paradigma of confianza.**
- *Pregunta central:* ¿confío en *quién sos* (identidad) o en *qué tenés* (posesión/capability)?

**1.13 Enfoque por modelo of autorización.**
- *Pregunta central:* ¿cómo se decide si esta identidad puede hacer esta acción sobre este objeto?

**1.14 Enfoque criptográfico y de gestión de claves.**
- *Pregunta central:* ¿qué firma, qué cifra y quién custodia las claves?

**1.15 Enfoque por control of tráfico.**
- *Pregunta central:* ¿qué límites y políticas aplico al caudal?

**1.16 Enfoque por validación and saneamiento.**
- *Pregunta central:* ¿confío en la entrada? (correcto: no).

**1.17 Enfoque por observabilidad and respuesta.**
- *Pregunta central:* ¿cómo sé que algo pasa, y qué hago cuando pasa?

**1.18 Enfoque por secretos, identidad of máquina and cadena of suministro.**
- *Pregunta central:* ¿dónde viven los secretos y quién los controla?

### Familia C — Enfoques según PARA QUIÉN and POR QUÉ

**1.19 Enfoque por OWASP API Security Top 10.**
- *Pregunta central:* ¿cuál of los diez riesgos tengo hoy y cómo lo pruebo?

**1.20 Enfoque por framework de threat modeling.**
- *Pregunta central:* ¿qué puede salir mal en este diseño, sistemáticamente?

**1.21 Enfoque por audiencia.**
- *Pregunta central:* ¿a quién le hablo y qué le importa?

**1.22 Enfoque por cumplimiento and regulatorio.**
- *Pregunta central:* ¿qué me exige la norma y cómo se traduce en controles?

**1.23 Enfoque por privacidad and protección of datos.**
- *Pregunta central:* ¿qué datos personales cruzan la API y con qué base legal?

**1.24 Enfoque por modelo of negocio and abuso económico.**
- *Pregunta central:* ¿qué gana un atacante con esta API, más allá de robar datos?

**1.25 Enfoque by madurez and gobierno.**
- *Pregunta central:* ¿en qué nivel estoy y hacia dónde voy?

**1.26 Enfoque por economía del atacante (modelo de amenaza).**
- *Pregunta central:* ¿cuánto le cuesta al atacante y cuánto me cuesta a mí defenderme?

**1.27 Enfoque histórico/evolutivo.**
- *Pregunta central:* ¿por qué cada tecnología nació, qué resolvió y qué dejó abierto?

**1.28 Enfoque académico/formal.**
- *Pregunta central:* ¿qué principios de diseño se están violando?

**1.29 Enfoque por resiliencia and disponibilidad.**
- *Pregunta central:* ¿qué pasa cuando algo falla o me saturan?

**1.30 Enfoque por anti-patrones.**
- *Pregunta central:* ¿qué errores concretos se repiten en la industria?

---

## 2. Taxonomía de las APIs: qué estamos protegiendo exactamente

### 2.1 Por estilo o paradigma

| Estilo | Riesgos característicos |
|---|---|
| **REST** | BOLA/BFLA, over-fetching, versionado laxo, IDOR |
| **GraphQL** | Consultas profundas, *introspection* expuesta, BOLA, Single Endpoint |
| **gRPC / Protobuf** | Reflexión expuesta, falta de inspección por proxies/WAF |
| **SOAP / XML** | XXE, WS-Security mal configurado |
| **WebSocket** | Autenticación solo al inicio; autorización por mensaje |
| **Webhooks** | SSRF, falta de firma (HMAC), replay |
| **Event-driven** | Autorización por tópico, *event injection* |

### 2.2 Single Endpoint: el caso especial de GraphQL

**Single Endpoint** es un patrón where todos los recursos se acceden a través de un solo endpoint (típicamente `/graphql`). Esto cambia completamente el modelo de seguridad:

- **Un solo punto de entrada:** Si el endpoint está protegido, todo está protegido. Si no, todo está expuesto.
- **Consultas profundas:** Un atacante puede construir consultas complejas que consuman muchos recursos.
- **Introspection:** Si está expuesta, un atacante puede descubrir todo el schema.
- **No hay URLs para protejer:** No podés aplicar protecciones por URL como en REST.

**Defensas específicas:**
- **Query depth limiting:** Limitar la profundidad de las consultas.
- **Query cost analysis:** Analizar el costo de la consulta antes de ejecutarla.
- **Deshabilitar introspection en producción.**
- **Rate limiting por complejidad:** No solo por número of requests, sino por costo.

### 2.3 Shadow APIs

**Shadow APIs** son APIs that existen en la organización but no están documentadas ni gestionadas. Son un riesgo importante porque:

- **No están en el inventario:** Nadie las protege ni las monitorea.
- **Pueden tener vulnerabilidades conocidas:** Si no se actualizan, pueden tener CVEs sin parchear.
- **Pueden exponer datos sensibles:** Sin controles de acceso adecuados.
- **Pueden ser descubiertas por atacantes:** Escaneando el dominio o analizando el tráfico.

**Cómo encontrar Shadow APIs:**
- **Escaneo pasivo:** Analizar el tráfico de red para descubrir endpoints no documentados.
- **Escaneo activo:** Usar herramientas como `ffuf`, `gobuster` o `nuclei` para descubrir endpoints.
- **Análisis de código:** Buscar definiciones de endpoints en el código fuente.
- **Revisión of logs:** Analizar logs of acceso para encontrar endpoints no documentados.

**Defensas:**
- **API Inventory:** Mantener un inventario actualizado de todas las APIs.
- **API Discovery:** Usar herramientas de descubrimiento continuo.
- **Eliminación of APIs no utilizadas:** Si no se usa, se elimina.

### 2.4 Por tipo de consumidor

- **First-party:** tus propios front-ends (SPA, móvil).
- **Interno (servicio a servicio):** tráfico este-oeste.
- **Partner / B2B:** relación contractual.
- **Público / open API:** sin relación previa.
- **Marketplace de terceros:** aplicaciones de otros sobre tus datos.

---

## 3. Historia: de las credenciales al token atado

### 3.1 Era 1 — La credencial viaja en cada request (1993–1999)

**HTTP Basic** (RFC 2617, 1999) and **Digest** (RFC 7616, 2015).

- **Qué resolvía:** autenticación mínima, sin estado.
- **Qué no resolvía:** the credencial viaja una y otra vez.

### 3.2 Era 2 — The federación en XML (2002–2005)

**WS-Security** (OASIS, 2004) and **SAML 2.0** (OASIS, 2005).

- **Qué aportó:** identidad federada, SSO, firmas.
- **Por qué no conquistó las APIs:** XML, verboso, pesado.

### 3.3 Era 3 — The clave estática (2006 en adelante)

**API keys** (AWS, 2006).

- **Qué resolvió:** identificar aplicaciones sin montar un servidor de identidad.
- **Dónde vive la falla:** no expira, no distingue permisos finos, and si se filtra es impersonación directa.

### 3.4 Era 4 — Firmar cada request (2007–2010)

**OAuth 1.0** (RFC 5849, 2010).

- **Qué aportó:** un request robado no se podía reutilizar sin la clave.
- **Por qué se abandonó:** muy difícil de implementar bien.

### 3.5 El giro (octubre de 2012): bearer sí, MAC no

**OAuth 2.0** (RFC 6749) and **bearer token** (RFC 6750).

- El propio OAuth 2.0 **había definido además el tipo `mac`**, but se **abandonó**.
- **RFC 6749, §10.3:** el servidor de recursos *no puede* confirmar que the token fue emitido al cliente que lo presenta.

### 3.6 The consolidación (2014–2025): ponerle cinturón al bearer

| Año | Aporte | Qué agrega |
|---|---|---|
| 2013 | Revocación of tokens (RFC 7009) | cortar antes de la expiración |
| 2014 | OpenID Connect Core 1.0 | identidad (ID token) sobre OAuth |
| 2015 | JWT (RFC 7519) · PKCE (RFC 7636) · Introspección (RFC 7662) | claims; candado al código; validar tokens opacos |
| 2018 | Token Binding (RFC 8471-8473) | atar el token al canal TLS (sin adopción masiva) |
| 2020 | mTLS atado a certificado (RFC 8705) · JWT BCP (RFC 8725) | tokens *sender-constrained*; reglas de validación JWT |
| 2021 | Perfil JWT para access tokens (RFC 9068) | interoperabilidad; `exp` obligatorio |
| 2023 | DPoP (RFC 9449) | prueba de posesión por request, sin PKI |
| 2025 | RFC 9700 · NIST SP 800-63-4 | mejores prácticas and sender-constrained/PKCE recomendados |

### 3.7 Lo que enseña la historia (cinco moralejas)

1. **Todo token portador es una contraseña portátil.**
2. **La simplicidad gana primero and cobra después.**
3. **Cada capa de esta historia sigue viva.**
4. **The vida del token importa más que su creación.**
5. **El token es una sola piece.**

---

## 4. Los protocolos involucrados, de HTTP a DPoP

### 4.1 Red and transporte

#### HTTP/1.1, HTTP/2 y HTTP/3 (QUIC)
- Los tokens viajan en **cabeceras** (`Authorization`), **cookies** or, mal, en la **query string**.
- **RFC 9700 (2025)** prohíbe el token en the URL.

#### TLS / SSL y mTLS
- **SSL** (Netscape, mediados of los 90) fue el origen; hoy hablamos de **TLS 1.2/1.3**.
- **mTLS** (mutual TLS) hace que *ambas* partes presenten certificado.

### 4.2 Autenticación HTTP clásica

#### HTTP Basic and Digest (RFC 2617 → RFC 7616)
- Basic manda `usuario:contraseña` en **Base64** (no es cifrado).
- Digest manda un **hash** con *nonce*.

#### Cookies de sesión (RFC 6265)
- El ID de sesión es, en the práctica, **un bearer token guardado en el navegador**.

#### API keys
- Un secreto estático que identifica al cliente (no al usuario).

### 4.3 Federación en XML

#### WS-Security, SAML 2.0 y XML-DSig
- **SAML 2.0** (OASIS, 2005) transporta **aserciones** de identidad firmadas.
- **Qué mirar:** *XML Signature Wrapping*, canonicalización, condiciones ignoradas.

### 4.4 OAuth and OpenID Connect

#### OAuth 1.0 (RFC 5849)
- Firma de cada request with **HMAC-SHA1**.

#### OAuth 2.0 (RFC 6749) and bearer (RFC 6750)
- Cuatro roles: **dueño**, **cliente**, **servidor de autorización**, **servidor de recursos**.

#### El tipo MAC (abandonado)
- **Primera aparición:** borrador de febrero de 2012; **abandonado**.
- **Por qué importa:** es el **eslabón perdido**: lo that hoy reintentan **mTLS** and **DPoP**.

#### PKCE (RFC 7636)
- **Primera aparición:** 2015. Obligatorio en **authorization code** según RFC 9700 (2025).
- **Cómo funciona:** the cliente genera un `code_verifier`, manda su hash (`code_challenge`) al pedir el código, and prueba el `verifier` al canjearlo.

#### OpenID Connect (OIDC Core 1.0)
- Una capa de **identidad** sobre OAuth 2.0. Agrega el **ID token** (un JWT con `iss`, `sub`, `aud`, `exp`, `amr`, `acr`).

#### Introspección (RFC 7662) and revocación (RFC 7009)
- El primero permite que el servidor de recursos **pregunte** al de autorización si un token sigue válido; the segundo permite **revocarlo**.

### 4.5 JOSE: la familia of JWT

- **JWS (RFC 7515):** firma. **JWE (RFC 7516):** cifrado. **JWK (RFC 7517):** claves. **JWA (RFC 7518):** algoritmos. **JWT (RFC 7519):** el token con claims.
- **Está firmado, no cifrado**: the payload se lee.

### 4.6 Atar el token a su portador

#### Token Binding (RFC 8471-8473)
- **Primera aparición:** 2018. Ataba el token al **canal** (TLS) en el que se emitió.
- **Qué pasó:** **sin adopción masiva**; quedó como intento.

#### mTLS atado a certificado (RFC 8705)
- **Primera aparición:** 2020.
- El token queda **ligado al `cnf` (thumbprint) del certificado** del cliente.

#### DPoP (RFC 9449)
- **Primera aparición:** 2023.
- El cliente firma una **prueba** (un JWT propio) with su clave privada, atada al request vía `htm` (método) and `htu` (URL), with `jti` único and `iat`.

### 4.7 Factores de autenticación (MFA)

**La MFA protege la emisión, no the uso.**

- **OTP: HOTP (RFC 4226, 2005) and TOTP (RFC 6238, 2011).**
- **Push y notificaciones:** cómodas and **phishable** (fatiga MFA).
- **Passkeys / WebAuthn-FIDO2 (W3C/FIDO):** llaves resistentes al *phishing*.
- **NIST SP 800-63-4 (2025):** marco de identidad digital; empuja lo *phishing-resistant*.

### 4.8 Gestión de identidades and otros estándares

- **SCIM (RFC 7643/7644, 2015):** aprovisionamiento de usuarios.
- **LDAP / Kerberos:** directorios and autenticación **corporativa**.
- **RADIUS:** autenticación de **red** (VPN, Wi-Fi corporativo).
- **Zero Trust (NIST SP 800-207, 2020):** no confiar por estar "dentro"; verificar **cada** solicitud.

---

## 5. Módulos técnicos

### M1 — HTTP Basic / Digest (1999)

#### Idea
Autenticación HTTP clásica: el cliente manda credenciales en **cada** petición.

#### Guion para explain
"Basic es como darle a alguien la llave of tu casa para que entre a revisar una habitación: le das la llave, no un permiso para esa habitación. Viaja en each request, and si mirás el valor, no está cifrado: está codificado. Base64 no es seguridad; es transporte tolerante a caracteres."

#### Vulnerabilidades
- Credenciales reutilizadas por request
- No hay "logout" real
- Base64 ≠ cifrado
- Fuerza bruta
- Credenciales en logs/URLs

#### Defensa
TLS obligatorio, migrar a tokens/OIDC, rate-limit and lockout, nunca loguear credenciales.

---

### M2 — Cookies and sesiones (1996)

#### Idea
El servidor guarda el estado and the navegador repite un **identificador de sesión** en una cookie.

#### Guion para explain
"The sesión en servidor es segura para la web tradicional and mala para APIs: el estado no escala, no delega and no cruza clientes. Pero trae dos problemas clásicos: robo de cookie por XSS and CSRF."

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

#### Guion para explain
"The API key es el bearer token más usado and menos cuidado del mundo. Es un identificador estático that se mete en un archivo, en una variable of entorno or —peor— en el JavaScript de un frontend, donde cualquiera lo lee."

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
Antes del bearer, OAuth **firmaba cada request** with HMAC-SHA1 and un secreto compartido.

#### Guion para explain
"OAuth 1.0 era la antítesis del bearer: nada de mandar un string reutilizable, each request se firmaba. Más seguro en teoría, carísimo en la práctica."

#### Vulnerabilidades
- Errores de canonicalización
- Secreto compartido filtrado
- Sin anti-replay (nonce/timestamp)

#### Defensa
Nonce + timestamp anti-replay, secretos por par, TLS. Hoy: migrar a DPoP.

---

### M5 — Bearer token (OAuth 2.0) (2012)

#### Idea
OAuth 2.0 separa autorización of autenticación and entrega al cliente un **access token**: un string with alcance and vida.

#### Guion para explain
"El bearer ganó por simplicidad: un string en una cabecera, sin firmar cada request, sin secretos compartidos. El precio está escrito en la norma: the servidor de recursos no puede saber si quien presenta el token es a quien se le emitió."

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
**JWT (JSON Web Token)**: `header.payload.signature`, base64url. **Está firmado, no cifrado**: the payload se lee.

#### Guion para explain
"Un JWT es como una credencial plastificada: firmada, no sellada. Cualquiera lee el contenido. Y guarda una trampa: the header dice with qué algoritmo se firmó; si el validador le hace caso al token en lugar of a su configuración, un atacante elige el algoritmo."

#### Vulnerabilidades
- `alg: none` and confusión **RS256→HS256**
- `exp`/`aud`/`iss` sin validar
- Claves débiles crackeables
- `kid` que apunta a un JWKS controlado por el atacante

#### Defensa
`alg` **desde la configuración del validador**, nunca del token; verificar `iss`, `aud`, `exp`, `nbf`; claves fuertes; rotación of claves.

---

### M7 — OIDC, authorization code, PKCE and ID token (2014)

#### Idea
**OpenID Connect Core 1.0** es la capa de identidad sobre OAuth 2.0. **PKCE: RFC 7636, agosto de 2015.** El **ID token** es un JWT that dice *quién* es the persona and *cómo* se autenticó.

#### Guion para explain
"The authorization code es el cupón of un solo uso that cambia un artefacto público por uno privado. PKCE le agrega un candado: aunque te roben el código, no lo podés canjear sin el verificador. Y el ID token es el DNI that te muestran en la puerta, no el pase that te ponen en la muñeca."

#### Vulnerabilidades
- Sin PKCE → código interceptable
- `redirect_uri` laxa
- Falta of `state` → CSRF
- Falta of `nonce` → replay del ID token
- ID token usado como access token

#### Defensa
PKCE obligatorio, `redirect_uri` exacta, `state` and `nonce`, validar `iss`/`aud`/`exp`/`nonce` en el RP.

---

### M8 — Refresh token (2012)

#### Idea
Token of vida larga that **sólo** se usa contra el endpoint of token para obtener nuevos access tokens.

#### Guion para explain
"The access token es el boleto de la función; el refresh token es the acreditación that te deja pedir uno nuevo sin volver a la taquilla. The rotación convierte al refresh en un artefacto of un solo uso."

#### Vulnerabilidades
- Sin rotación
- Sin detección of reuso
- Vida infinita
- Almacenamiento inseguro

#### Defensa
Rotación + detección of reuso, vida absoluta, binding al cliente, almacenamiento seguro.

---

### M9 — mTLS and DPoP (sender-constrained) (2020 / 2023)

#### Idea
Atar el token a su portador. **mTLS + token atado a certificado: RFC 8705, febrero de 2020.** **DPoP: RFC 9449, octubre de 2023.**

#### Guion para explain
"Si el problema del bearer es that cualquiera that lo tenga lo usa, the solución es exigir algo más that la posesión. mTLS ata el token al certificado; DPoP ata el token a una clave privada that the cliente prueba en each request."

#### Vulnerabilidades
- DPoP sin validar `htm`/`htu`
- Replay of the prueba (`jti`)
- `ath` ausente
- mTLS mal configurado

#### Defensa
Validar `htm`, `htu`, `jti` (anti-replay), `ath`, `alg` permitido; rotación of claves.

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
| API9 | **Improper Inventory** (incluye Shadow APIs) |
| API10 | **Unsafe Consumption** |

---

### M11 — Caso ID Uruguay (laboratorio ético)

#### Qué es
**ID Uruguay** es el proveedor de identidad del Estado uruguayo, gestionado by **AGESIC**. Se integra vía **OpenID Connect**.

#### Verificación defensiva de tu integración

| Control | Resultado esperado |
|---|---|
| **PKCE obligatorio** | `code_challenge` + `code_challenge_method=S256` |
| **`redirect_uri` exacta** | Coincidencia exacta |
| **`state` and `nonce`** | Presentes, aleatorios, de un solo uso |
| **Validación del ID token** | `iss`, `aud`, `exp`, `nonce` and firma validados |
| **ID token no se usa como access token** | Nunca |
| **Vida del access token** | Corta and acorde al riesgo |
| **Rotación of refresh token** | Rotación + detección of reuso |
| **Revocación / logout** | Invalidado |
| **Transporte** | Sólo HTTPS + header |
| **Almacenamiento en tu cliente** | Sin acceso por JS |

---

### M12 — Seguridad dinámica and MFA Step-Up (NUEVO en v3)

#### Idea
The autenticación **no es un estado binario** of "conectado/desconectado", sino un **flujo continuo** that must exigir re-autenticación según la criticidad de la transacción.

#### Conceptos clave

**MFA Step-Up:** Pedir un segundo factor adicional para operaciones sensibles, incluso si the usuario ya está autenticado. Se implementa with `acr` (Authentication Context Class Reference) and `amr` (Authentication Methods References) en el token.

**Acciones sensibles that merecen Step-Up:**
- Transferencias de dinero
- Cambio of contraseña or email
- Acceso a datos personales sensibles
- Operaciones administrativas
- Descarga of documentos confidenciales

#### Guion para explain
"The MFA no es un interruptor of encendido/apagado. Es más like un ascensor: subís al primer piso with contraseña, pero para subir al piso 20 necesitás una tarjeta especial. Ese es the Step-Up: pedir más garantía solo para la operación sensible."

#### Implementación
- `acr_values` en the solicitud of autorización
- `amr` en the ID token
- Paso-up en the servidor of autorización

---

### M13 — Riesgos en clientes públicos: Mobile (NUEVO en v3)

#### Idea
En aplicaciones móviles and SPAs, the cliente **es controlado por el usuario**, and un atacante puede modificar la aplicación.

**Riesgos específicos of clientes públicos:**
- **Aplicaciones modificadas (tampering):** Un atacante puede modificar el APK/IPA para desactivar SSL pinning, extraer secretos or cambiar el comportamiento
- **Root/Jailbreak:** The dispositivo está comprometido
- **Extracción of secretos:** Un atacante puede descompilar la app and extraer claves hardcodeadas

**Mitigaciones:**
- **App Attestation** (Play Integrity API / DeviceCheck): Verifica that the app no fue modificada
- **PKCE:** Protege el código of autorización
- **DPoP:** Ata el token a una clave privada
- **SSL Pinning:** Cert pinning en the app

#### Guion para explain
"En una app móvil, el atacante tiene el control total of the dispositivo. Puede modificar la app, desactivar protecciones, and extraer secretos. Por eso necesitás defensas additionales: App Attestation para verificar la integridad, PKCE para el código, DPoP para el token."

#### Mitigaciones clave

| Mitigación | Protección |
|---|---|
| **Play Integrity API / DeviceCheck** | Verifica that the app no fue modificada |
| **PKCE** | Protege el código of autorización |
| **DPoP** | Ata el token a una clave privada |
| **SSL Pinning** | Previene MITM |

---

### M14 — Zero Trust and cadena of suministro (NUEVO en v3)

#### Idea
**Zero Trust (NIST SP 800-207, 2020):** No confiar por estar "dentro"; verificar **cada** solicitud.

**Principios:**
- Nunca confíes, siempre verifica
- Acceso with mínimo privilegio
- Asume that the red está comprometida
- Verifica cada solicitud, no solo la primera

#### Cadena of suministro

**Riesgos:**
- Secretos en CI/CD
- Dependencias of terceros
- Bibliotecas with vulnerabilidades

**Defensas:**
- Secret managers (AWS Secrets Manager, HashiCorp Vault)
- SBOM / SCA (Software Bill of Materials)
- Escaneo of secretos en CI (gitleaks, ggshield)

#### Guion para explain
"Zero Trust es dejar de confiar por defecto. Antes, si estabas dentro of the red, confiabas en vos. Ahora, each solicitud se verifica, sin importar de dónde venga. And the cadena of suministro es el nuevo perímetro: si una dependencia tuya tiene una vulnerabilidad, vos también la tenés."

---

### M15 — Shadow APIs and Single Endpoint (NUEVO en v3)

#### Shadow APIs
**Shadow APIs** son APIs that existen en the organización but no están documentadas ni gestionadas. Son un riesgo importante because:

- **No están en el inventario:** Nadie las protege ni las monitorea.
- **Pueden tener vulnerabilidades conocidas:** Si no se actualizan, pueden tener CVEs sin parchear.
- **Pueden exponer datos sensibles:** Sin controles of acceso adecuados.

**Cómo encontrar Shadow APIs:**
- **Escaneo pasivo:** Analizar the tráfico de red para descubrir endpoints no documentados.
- **Escaneo activo:** Usar herramientas like `ffuf`, `gobuster` o `nuclei`.
- **Análisis of código:** Buscar definiciones de endpoints en el código fuente.
- **Revisión of logs:** Analizar logs of acceso para encontrar endpoints no documentados.

#### Single Endpoint: el patrón que cambia el modelo of seguridad

**Single Endpoint** es un patrón donde **todos los recursos y operaciones se acceden a través de un solo endpoint**, independientemente del estilo de API. Esto no es exclusivo de GraphQL: también aplica a REST, RPC y SOAP cuando se diseña una API con un único punto de entrada.

##### Single Endpoint en GraphQL

El caso más conocido. Todos los recursos se acceden vía `/graphql`:

- **Un solo punto of entrada:** Si the endpoint está protegido, todo está protegido. Si no, todo está expuesto.
- **Consultas profundas:** Un atacante puede construir consultas complejas that consuman muchos recursos.
- **Introspection:** Si está expuesta, un atacante puede descubrir todo el schema.

**Defensas específicas:**
- **Query depth limiting:** Limitar the profundidad de las consultas.
- **Query cost analysis:** Analizar the costo de la consulta antes of ejecutarla.
- **Deshabilitar introspection en producción.**
- **Rate limiting por complejidad:** No solo por número of requests, sino por costo.

##### Single Endpoint en REST

En REST, el patrón Single Endpoint se da cuando se diseña una API con un único endpoint que recibe todas las operaciones vía POST, usando un parámetro para indicar la acción:

```
POST /api
{
  "action": "getUser",
  "params": { "id": 123 }
}
```

**Riesgos específicos:**
- **No hay semántica HTTP:** Los verbos POST para todo, no se aprovechan los códigos de estado HTTP.
- **Difícil de cachear:** Todo es POST, no se puede usar cache de HTTP.
- **Difícil de proteger:** No se pueden aplicar políticas por URL o método.
- **Difícil de documentar:** OpenAPI no puede documentar este estilo automáticamente.

**Defensas:**
- **Rate limiting por acción:** Identificar la acción en el body y aplicar límites.
- **Validación estricta del body:** Whitelist de acciones permitidas.
- **Autenticación y autorización en cada request:** No asumir que el endpoint único está protegido.

##### Single Endpoint en RPC (gRPC, JSON-RPC, XML-RPC)

En RPC, el patrón Single Endpoint es común: un único endpoint que recibe todas las llamadas a funciones:

```
POST /rpc
{
  "method": "getUser",
  "params": { "id": 123 }
}
```

**Riesgos específicos:**
- **No hay inspección por proxies/WAF:** Los proxies tradicionales no entienden el protocolo RPC.
- **Reflexión expuesta:** Si el servidor expone reflexión, un atacante puede descubrir todos los métodos.
- **Falta of tipado:** Si el tipado es débil, un atacante puede enviar parámetros inesperados.

**Defensas:**
- **Whitelist of métodos:** Solo permitir métodos conocidos.
- **Validación estricta of parámetros:** Tipado fuerte, validación de esquema.
- **Deshabilitar reflexión en producción.**
- **Rate limiting por método:** Aplicar límites específicos por método.

##### Single Endpoint en SOAP

En SOAP, el patrón Single Endpoint es natural: un único endpoint que recibe todos los mensajes SOAP:

```
POST /soap
<soap:Envelope>
  <soap:Body>
    <getUser>
      <id>123</id>
    </getUser>
  </soap:Body>
</soap:Envelope>
```

**Riesgos específicos:**
- **XML vulnerabilities:** XXE, XML Entity Expansion, XPath injection.
- **WS-Security mal configurado:** Si no se configura bien, no protege nada.
- **Difícil de inspeccionar:** Los proxies tradicionales no entienden SOAP.

**Defensas:**
- **Validación estricta of XML:** Prevenir XXE, Entity Expansion.
- **WS-Security bien configurado:** Firma y cifrado of mensajes.
- **Whitelist of operaciones:** Solo permitir operaciones conocidas.
- **Rate limiting por operación:** Aplicar límites específicos por operación.

##### Resumen: Single Endpoint en diferentes estilos

| Estilo | Endpoint único | Riesgo principal | Defensa clave |
|---|---|---|---|
| **GraphQL** | `/graphql` | Consultas profundas, introspection | Query depth, cost analysis |
| **REST** | `/api` (POST todo) | No semántica HTTP, difícil proteger | Rate limiting por acción |
| **RPC** | `/rpc` | No inspección por WAF, reflexión | Whitelist of métodos |
| **SOAP** | `/soap` | XXE, WS-Security mal configurado | Validación XML, WS-Security |

**Guion para explain:**
"Single Endpoint no es solo un problema of GraphQL. Cualquier estilo of API puede tener un único punto of entrada, and eso cambia completamente el modelo of seguridad. En GraphQL son las consultas profundas. En REST es la pérdida of semántica HTTP. En RPC es la falta of inspección. En SOAP son las vulnerabilidades XML. Cada estilo tiene su riesgo específico, but todos comparten un problema: si the endpoint único no está bien protegido, todo lo demás tampoco."

---

### M16 — PKCE Detallado (NUEVO en v3)

#### Idea
PKCE (Proof Key for Code Exchange) es un mecanismo de seguridad for proteger el flujo de código of autorización en clientes públicos.

#### Cómo funciona

1. **The cliente genera un `code_verifier`:** Un string aleatorio of 43-128 caracteres.
2. **Calcula el `code_challenge`:** SHA256 del `code_verifier`, codificado en base64url.
3. **Envía el `code_challenge` en la solicitud of autorización.**
4. **Cuando se recibe el código, envía el `code_verifier` en la solicitud of token.**
5. **The servidor verifica that el `code_verifier` corresponde al `code_challenge`.**

#### Guion para explain
"PKCE es como un candado de bicicleta: the código de autorización es the bicicleta, and el code_verifier es the llave. Aunque te roben the bicicleta, sin the llave no podés usarla."

#### Vulnerabilidades
- PKCE en texto plano (`plain`)
- Aceptar códigos sin verificar `challenge`

#### Defensa
Usar siempre `S256` (SHA256), nunca `plain`.

---

### M17 — DPoP Detallado (NUEVO en v3)

#### Idea
DPoP (Demonstrating Proof of Possession) ata el token a una clave privada that the cliente prueba en each request.

#### Cómo funciona

1. **The cliente genera un par de claves:** Una clave privada and una clave pública.
2. **Crea una prueba DPoP:** Un JWT firmado with la clave privada, with claims `jti`, `htm`, `htu`, `iat`.
3. **Envía the prueba with cada request:** En el header `DPoP`.
4. **The servidor verifica the prueba:** Que el `jti` no se haya usado, que el `htm` y `htu` coincidan con el request.

#### Guion para explain
"DPoP es like un sello de goma: the token es the documento, and the prueba DPoP es the sello. Sin the sello, the documento no vale."

#### Vulnerabilidades
- DPoP sin validar `htm`/`htu`
- Replay of the prueba (`jti`)
- Claves of cliente mal protegidas

#### Defensa
Validar `htm`, `htu`, `jti` (anti-replay), `ath`, `alg` permitido.

---

### M18 — App Attestation Detallado (NUEVO en v3)

#### Idea
App Attestation es un mecanismo for verificar that the app móvil no ha sido modificada.

#### Cómo funciona

1. **The app solicita un token de attestation:** Al servidor of attestation (Play Integrity API o DeviceCheck).
2. **The servidor verifica the integridad of the app:** Firma, certificado, etc.
3. **The servidor devuelve un token de attestation:** The app envía este token a tu servidor.
4. **Tu servidor verifica the token:** Con el servidor de attestation.

#### Guion para explain
"App Attestation es like un control de seguridad en el aeropuerto: verifica that the app es legítima, no modificada, and viene of una fuente confiable."

#### Plataformas
- **Android:** Play Integrity API
- **iOS:** DeviceCheck / App Attest

#### Vulnerabilaciones
- Root/Jheelbreak
- SSL pinning desactivado
- Extraer tokens of attestation

#### Defensa
Verificar the token of attestation en cada solicitud sensible.

---

### M19 — Token Binding and RFC 8705 (NUEVO en v3)

#### Idea
Token Binding ata el token a su portador usando criptografía asimétrica.

#### Token Binding (RFC 8471-8473)
- **Primera aparición:** 2018.
- **Ataba el token al canal TLS** en el que se emitió.
- **Sin adopción masiva:** Quedó como intento.

#### mTLS atado a certificado (RFC 8705)
- **Primera aparición:** 2020.
- **El token queda ligado al `cnf` (thumbprint) del certificado** del cliente.

#### Guion para explain
"Token Binding es like un pasaporte con foto: the token es the pasaporte, and el certificado es the foto. Sin the foto, the pasaporte no vale."

---

### M20 — OWASP API Top 10 Detallado (NUEVO en v3)

#### API1 — BOLA
**Broken Object Level Authorization:** Un atacante presenta su propio token, válido, and cambia el identificador del objeto en the URL.

**Cómo probar:** Con the token de tu cuenta, cambia the ID del objeto por otro.

**Defensa:** Verificar the autorización a nivel of objeto en each solicitud.

#### API2 — Broken Authentication
**Fallas en the autenticación:** Passwords débiles, MFA no implementado, tokens mal validados.

**Cómo probar:** Fuerza bruta, JWT mal validado, credenciales por defecto.

**Defensa:** MFA, rate limit, validación estricta of tokens.

#### API3 — BOPLA
**Broken Property Level Authorization:** Mass Assignment, campos no documentados.

**Cómo prober:** Enviar campos extra en the solicitud.

**Defensa:** Whitelist of campos permitidos.

#### API4 — Unrestricted Resource Consumption
**Consumo sin límites:** Paginación gigante, búsquedas costosas.

**Cómo prober:** Enviar parámetros of paginación extremos.

**Defensa:** Límites estrictos en paginación and búsqueda.

#### API5 — BFLA
**Broken Function Level Authorization:** Acceder a funciones administrativas with un usuario normal.

**Cómo prober:** Llamar endpoints de administración with un usuario normal.

**Defensa:** Verificar the rol del usuario en each solicitud.

#### API6 — Sensitive Business Flows
**Abuso of flujos de negocio:** Cupones, reintentos of pago, creación masiva de cuentas.

**Cómo prober:** Repetir un flujo más veces of las permitidas.

**Defensa:** Límites por usuario, detección of abuso.

#### API7 — SSRF
**Server-Side Request Forgery:** Una API that recibe una URL and la fetch.

**Cómo prober:** Apuntar the URL a localhost or metadatos.

**Defensa:** Lista blanca of URLs permitidas.

#### API8 — Misconfiguration
**Mala configuración:** CORS `*`, errores verbosos, métodos no documentados.

**Cómo prober:** Escanear the API with nuclei o ZAP.

**Defensa:** Configuración estricta, deshabilitar métodos no usados.

#### API9 — Improper Inventory
**Inventario impropio:** Versiones viejas, APIs fantasma, Shadow APIs.

**Cómo prober:** Buscar versiones viejas (`/v1`, `/beta`).

**Defensa:** Inventario actualizado, eliminar APIs no usadas.

#### API10 — Unsafe Consumption
**Consumo inseguro of terceros:** Confiar en datos of otro servicio sin validar.

**Cómo prober:** Manipular the respuesta of un servicio de terceros.

**Defensa:** Validar all datos externos.

---

## 6. La seguridad of API más allá del token

### 6.1 Autorización a nivel of objeto (BOLA)
The pregunta no es si el token es válido, sino si this identidad puede tocar este objeto.

### 6.2 Validación of entrada
Inyección (SQL/NoSQL/comandos), SSRF, XXE, deserialización insegura, mass assignment.

### 6.3 Gateway and control of tráfico
Cuotas, rate limiting, gestión of bots, geo/IP policy.

### 6.4 Inventario
Versiones viejas and APIs fantasma that siguen vivas.

### 6.5 Cadena of suministro
Secretos en CI and dependencias of terceros.

### 6.6 Observabilidad and respuesta
Logs, trazas, métricas, SIEM, detección of anomalías, revocación, respuesta a incidentes.

### 6.7 Cumplimiento and privacidad
En Uruguay: Ley 18.331, Decreto 66/025, reporte a CERTuy.

### 6.8 Resiliencia
DoS/DDoS, consumo of recursos, circuit breakers, degradación elegante.

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
Construí una prueba **conceptual** with Python:
```python
# The prueba DPoP es un JWT firmado por el CLIENTE with su clave privada
# Header típico: {"typ":"dpop+jwt","alg":"ES256","jwk":{...}}
# Claims: jti (único), htm (método), htu (URL), iat
# The servidor rechaza si htm/htu no coinciden con el request, or si the jti se repite
```

---

## 8. Glosario of atajos

| Término | Significado |
|---|---|
| **Bearer token** | Credencial portadora: quien lo tiene, lo usa |
| **JWT** | JSON Web Token: token with claims en JSON |
| **JWS** | JSON Web Signature: firma |
| **JWE** | JSON Web Encryption: cifrado |
| **PKCE** | Proof Key for Code Exchange: candado al código of autorización |
| **DPoP** | Demonstrating Proof of Possession: prueba of posesión por request |
| **mTLS** | Mutual TLS: ambas partes se autentican with certificado |
| **BOLA** | Broken Object Level Authorization: autorización rota a nivel of objeto |
| **BFLA** | Broken Function Level Authorization: autorización rota a nivel of función |
| **MFA** | Multi-Factor Authentication: autenticación multifactor |
| **Step-Up** | Pedir más garantía para operaciones sensibles |
| **Zero Trust** | Nunca confíes, siempre verifica |
| **App Attestation** | Verificación of integridad de the app |
| **Shadow API** | API no documentada ni gestionada |
| **Single Endpoint** | Todos the recursos through un solo endpoint |
| **REST Single Endpoint** | `POST /api` con acción en el body |
| **RPC Single Endpoint** | `POST /rpc` con método en el body |
| **SOAP Single Endpoint** | `POST /soap` con operación SOAP |
| **gRPC** | RPC binario sobre HTTP/2 |
| **JSON-RPC** | RPC ligero sobre JSON |
| **XML-RPC** | RPC sobre XML |
| **WS-Security** | Seguridad para mensajes SOAP |

---

## 9. Plantilla of reporte responsable

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
[Tu información of contacto]
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
Depende de cómo se use. Un bearer token with vida corta, scope mínimo, revocación and transporte seguro es razonablemente seguro. Pero no es suficiente por sí solo.

### ¿Qué es mejor: JWT or token opaco?
Depende. Los JWT son más eficientes (no requieren introspección) but más difíciles of revocar. Los tokens opacos son más fáciles of revocar but requieren introspección.

### ¿PKCE es necesario para todos the flujos?
PKCE es obligatorio para el flujo of código of autorización según RFC 9700 (2025). Para otros flujos, no aplica.

### ¿DPoP es mejor that mTLS?
DPoP es más fácil of implementar (no requiere PKI). mTLS es más seguro but más complejo of gestionar.

### ¿The MFA protege al token?
No. The MFA protege el momento of the emisión, no los treinta días siguientes. Para eso se necesita Step-Up or DPoP.

### ¿Qué es Zero Trust?
Es un paradigma of seguridad that propone "nunca confiar, siempre verificar". No confiar por estar dentro of the red.

### ¿Qué es BOLA?
Broken Object Level Authorization: un atacante presenta su propio token, válido, and cambia el identificador del objeto en the URL para acceder a datos ajenos.

### ¿Qué es una Shadow API?
Una API that existe en the organización but no está documentada ni gestionada. Nadie las protege ni las monitorea.

### ¿Qué es un Single Endpoint?
Un patrón where todos los recursos se acceden a través de un solo endpoint, como en GraphQL. Cambia completamente el modelo of seguridad.

### ¿Qué es App Attestation?
Un mecanismo for verificar that the app móvil no ha sido modificada. Se usa en Android (Play Integrity API) and iOS (DeviceCheck / App Attest).

---

*Fin del guion v3.*
