# 4. Los protocolos involucrados, de HTTP a DPoP

Esta sección es la **caja de herramientas** de la charla. Para cada protocolo: **qué es**, **cuándo
apareció**, **cómo funciona a grandes rasgos**, **dónde aparece** en la historia de los tokens y **qué
falla** hay que mirar. No hace falta memorizar cada número de RFC; sí entender **qué problema resuelve
cada pieza** y **en qué capa vive**.

![Los protocolos involucrados, agrupados por capas](img/09_protocol_stack.png)

## 4.1 Red y transporte

### HTTP/1.1, HTTP/2 y HTTP/3 (QUIC)

- **Qué es:** el protocolo de aplicación de la web. Todo lo demás (OAuth, JWT, cookies) **viaja dentro**
  de HTTP.
- **Cómo se usa acá:** los tokens viajan en **cabeceras** (`Authorization`), **cookies** o, mal, en la
  **query string**. Las cabeceras son el lugar correcto.
- **Qué mirar:** *request smuggling*, desincronización entre proxy y backend, y el hecho de que la
  **query string** termina en logs, `Referer` e historial. RFC 9700 (2025) prohíbe el token en la URL.
- **Ejemplo:** `Authorization: Bearer eyJhbGciOiJSUzI1NiIs...`

### TLS / SSL y mTLS

- **Qué es:** la capa que cifra y autentica el canal. **SSL** (Netscape, mediados de los 90) fue el
  origen; hoy hablamos de **TLS 1.2/1.3**. HTTPS es HTTP dentro de TLS.
- **Cómo se usa acá:** sin HTTPS, el bearer token se lee al pasar. **mTLS** (mutual TLS) hace que *ambas*
  partes presenten certificado, lo que da **autenticación fuerte de cliente** y permite **atar el token
  al certificado** (RFC 8705).
- **Qué mirar:** versiones viejas de TLS, certificados mal validados (el error de "ignorar la
  verificación"), terminación TLS que rompe la atadura del token, y *pinning* mal hecho que rompe la app.

### DNS, TCP y QUIC

- **Qué es:** DNS resuelve nombres; TCP transporta; QUIC (sobre UDP) sostiene HTTP/3.
- **Dónde aparece:** en **SSRF** (una API que resuelve una URL arbitraria controlada por el atacante),
  en *DNS rebinding* y en la superficie de red de los gateways.
- **Qué mirar:** APIs que aceptan una **URL** sin lista blanca; resolución interna que el atacante puede
  forzar.

### WebSocket y gRPC (transporte de APIs modernas)

- **Qué es:** WebSocket abre un **canal persistente**; gRPC usa **HTTP/2** con **Protocol Buffers**
  binarios.
- **Qué mirar:** WebSocket suele **autenticar solo al inicio** (el token no se reevalúa por mensaje); gRPC
  suele **no** ser inspeccionado por WAF/ proxy, y expone reflexión y streaming.

## 4.2 Autenticación HTTP clásica

### HTTP Basic y Digest (RFC 2617 → RFC 7616)

- **Qué es:** Basic manda `usuario:contraseña` en **Base64** (no es cifrado). Digest manda un **hash**
  con *nonce*.
- **Primera aparición:** RFC 2617 (1999); actualizado por RFC 7616 (2015, con SHA-256).
- **Dónde vive hoy:** autenticación de **cliente** en OAuth (`client_secret_basic`), sistemas internos.
- **Qué mirar:** Basic sobre HTTP sin TLS; credenciales en logs; reutilización en todas las llamadas.

### Cookies de sesión (RFC 6265)

- **Qué es:** estado que el navegador guarda y reenvía. Creadas por Netscape (1996), estandarizadas en
  RFC 6265 (2011).
- **Cómo se usa acá:** el ID de sesión es, en la práctica, **un bearer token guardado en el navegador**.
- **Qué mirar:** falta de `HttpOnly`, `Secure`, `SameSite`; CSRF; fijación de sesión; XSS que roba la
  cookie.

### API keys

- **Qué es:** un secreto estático que identifica al cliente (no al usuario).
- **Dónde aparece:** servicios internos, APIs de terceros, `.env` y CI.
- **Qué mirar:** claves en repositorios y logs; sin expiración; sin permisos finos; imposibles de rotar
  sin romper todo.

## 4.3 Federación en XML

### WS-Security, SAML 2.0 y XML-DSig

- **Qué es:** **SAML 2.0** (OASIS, 2005) transporta **aserciones** de identidad firmadas; **WS-Security**
  (2004) define cómo firmar/ cifrar mensajes SOAP; **XML-DSig** es la firma XML.
- **Cómo funciona:** el IdP emite una aserción firmada con `Subject`, `Conditions`, `AttributeStatement`;
  la app confía en el IdP y crea sesión.
- **Qué mirar:** *XML Signature Wrapping* y canonicalización, aserciones sin verificar firma,
  condiciones (`NotBefore`/`NotOnOrAfter`) ignoradas, y el famoso *SAML "comment" injection*.
- **Por qué importa hoy:** SAML sigue siendo el rey del **SSO empresarial**. Es XML, pesado, pero
  probado en décadas de banca y gobierno.

## 4.4 OAuth y OpenID Connect

![Familia de tokens y flujo de emisión](img/02_token_family.png)

### OAuth 1.0 (RFC 5849)

- **Primera aparición:** borrador dic. 2007; RFC 5849 en 2010.
- **Cómo funciona:** firma de cada request con **HMAC-SHA1**, `nonce` y `timestamp`.
- **Qué mirar (histórico):** implementación frágil, relojes, secreto en el cliente.
- **Por qué importa:** explica **por qué** OAuth 2.0 eligió la simplicidad del bearer.

### OAuth 2.0 (RFC 6749) y bearer (RFC 6750)

- **Primera aparición:** octubre de 2012.
- **Cómo funciona:** cuatro roles (**dueño**, **cliente**, **servidor de autorización**, **servidor de
  recursos**) y flujos (*grants*) para obtener un **access token**, que se presenta como **bearer**.
- **Qué mirar:** el propio §10.3 (no se puede confirmar a quién se emitió el token); *redirect URI*
  abiertos; el *authorization code* reusable sin PKCE; CSRF en el callback (`state` ausente).

### El tipo MAC (abandonado)

- **Primera aparición:** borrador de febrero de 2012; **abandonado**.
- **Qué proponía:** un token con **prueba de posesión** (el cliente demuestra que tiene una clave).
- **Por qué se cayó:** complejidad de canonicalización e interoperabilidad.
- **Por qué importa:** es el **eslabón perdido**: lo que hoy reintentan **mTLS** y **DPoP**.

### PKCE (RFC 7636)

- **Primera aparición:** 2015. Obligatorio en **authorization code** según RFC 9700 (2025).
- **Cómo funciona:** el cliente genera un `code_verifier`, manda su hash (`code_challenge`) al pedir el
  código, y prueba el `verifier` al canjearlo. Así, un código **robado** no sirve.
- **Qué mirar:** PKCE "en texto plano" (`plain`) en apps públicas; clientes que aceptan códigos sin
  verificar `challenge`.

### OpenID Connect (OIDC Core 1.0)

- **Primera aparición:** final, 26 de febrero de 2014.
- **Cómo funciona:** una capa de **identidad** sobre OAuth 2.0. Agrega el **ID token** (un JWT con
  `iss`, `sub`, `aud`, `exp`, `amr`, `acr`) y el endpoint `UserInfo`.
- **Qué mirar:** validar **firma**, `iss`, `aud`, `exp` y `nonce`; no confundir el **ID token** (para la
  app) con el **access token** (para la API).

### Introspección (RFC 7662) y revocación (RFC 7009)

- **Qué son:** el primero permite que el servidor de recursos **pregunte** al de autorización si un token
  sigue válido; el segundo permite **revocarlo**.
- **Primera aparición:** 2015 y 2013, respectivamente.
- **Qué mirar:** introspección en cada request (costo/latencia) y revocación que en realidad **no se
  propaga** a todas las réplicas.

## 4.5 JOSE: la familia de JWT

![Anatomía de un JWT](img/03_jwt_anatomy.png)

- **JWS (RFC 7515):** firma. **JWE (RFC 7516):** cifrado. **JWK (RFC 7517):** claves. **JWA (RFC 7518):**
  algoritmos. **JWT (RFC 7519):** el token con claims. **JWT BCP (RFC 8725, 2020):** las reglas para no
  equivocarse. **RFC 9068 (2021):** perfil de JWT para access tokens.
- **Cómo funciona:** `header.payload.signature`, todo en **Base64url**. **Está firmado, no cifrado**: el
  payload se lee.
- **Qué mirar:** `alg: none` y confusión **RS256→HS256**; `exp`/`aud`/`iss` sin validar; claves débiles
  crackeables; `kid` que apunta a un JWKS controlado por el atacante.
- **Ejemplo de claim clave:** `amr: ["pwd","otp"]` (RFC 8176) dice **cómo** se autenticó; `acr` dice con
  qué nivel.

## 4.6 Atar el token a su portador

![Del bearer a los tokens sender-constrained](img/07_sender_constrained.png)

### Token Binding (RFC 8471-8473)

- **Primera aparición:** 2018. Ataba el token al **canal** (TLS) en el que se emitió.
- **Qué pasó:** **sin adopción masiva**; quedó como intento. Lección: la teoría correcta no basta si el
  ecosistema no acompaña.

### mTLS atado a certificado (RFC 8705)

- **Primera aparición:** 2020.
- **Cómo funciona:** el token queda **ligado al `cnf` (thumbprint) del certificado** del cliente; el
  servidor exige el certificado en cada llamada. Robar el token **no alcanza**.
- **Qué mirar:** PKI y rotación de certificados; *proxy* o balanceador que rompe el mTLS; validar el
  certificado del lado correcto.

### DPoP (RFC 9449)

- **Primera aparición:** 2023.
- **Cómo funciona:** el cliente firma una **prueba** (un JWT propio) con su clave privada, atada al
  request vía `htm` (método) y `htu` (URL), con `jti` único y `iat`. El servidor valida la prueba y
  **no acepta el token sin ella**. Robar el access token **no sirve**.
- **Qué mirar:** ventana de `iat`, almacenamiento de `jti` para evitar reenvíos, claves de cliente bien
  resguardadas, y que el *resource server* **exija** DPoP (no que lo acepte como opcional).

## 4.7 Factores de autenticación (MFA)

![La MFA protege un instante; el token vive mucho más](img/05_mfa_timeline.png)

**La MFA protege la emisión, no el uso.** El segundo factor se pide una vez; el access token que sale
de ahí puede vivir minutos, días o meses. Entre el login y la última llamada, la MFA ya no opina.

- **OTP: HOTP (RFC 4226, 2005) y TOTP (RFC 6238, 2011).** Códigos de un solo uso basados en un secreto
  compartido; TOTP es el "código de 6 dígitos de 30 segundos".
- **Push y notificaciones:** cómodas y **phishable** (fatiga MFA).
- **Passkeys / WebAuthn-FIDO2 (W3C/FIDO):** llaves resistentes al *phishing*, atadas al **origen**. El
  segundo factor más fuerte del lado persona.
- **NIST SP 800-63-4 (2025):** marco de identidad digital; empuja lo *phishing-resistant* y limita los
  factores débiles (SMS/OTP).

![Persona vs. sistema: dos preguntas distintas](img/06_person_vs_system.png)

**No es lo mismo autenticar personas que sistemas.** Del lado persona, la pregunta es "¿este humano es
quien dice ser, con un segundo factor?". Del lado **sistema**, no hay humano que factorizar: la pregunta
es "¿este *workload* es el que dice ser, y con qué credencial efímera?". Y hay un tercer caso, la
identidad **delegada**: una app que actúa **en nombre** de un usuario (OAuth) — donde el consentimiento,
el `scope` y la revocación son el centro.

- **Lo que ninguna MFA resuelve:** en flujo sistema a sistema no hay factor humano; y **una vez emitido
  el token**, la MFA ya no controla el uso.


## 4.8 Gestión de identidades y otros estándares de contexto

- **SCIM (RFC 7643/7644, 2015):** aprovisionamiento de usuarios entre IdP y aplicaciones. Es una **API**
  con su propio token: otra vez, la cadena de confianza.
- **LDAP / Kerberos:** directorios y autenticación **corporativa**; aparecen detrás del IdP cuando la
  federación es hacia el mundo Windows/AD.
- **RADIUS:** autenticación de **red** (VPN, Wi-Fi corporativo); puede ser un paso previo a la MFA.
- **Zero Trust (NIST SP 800-207, 2020):** no confiar por estar "dentro"; verificar **cada** solicitud.
  Es el paraguas conceptual donde encajan mTLS, DPoP y la autorización por objeto.

## 4.9 Tabla maestra de primeras apariciones

| Mecanismo | Primera aparición | Tipo |
|---|---|---|
| Cookies | 1996 (Netscape) → RFC 6265 (2011) | sesión |
| HTTP Basic / Digest | RFC 2617 (1999) → RFC 7616 (2015) | autenticación |
| WS-Security | OASIS 2004 | firma SOAP |
| SAML 2.0 | OASIS 2005 | federación XML |
| HOTP | RFC 4226 (2005) | OTP |
| OAuth 1.0 | borrador dic. 2007 → RFC 5849 (2010) | delegación firmada |
| JWT | borrador 28 dic. 2010 → RFC 7519 (2015) | token con claims |
| TOTP | RFC 6238 (2011) | OTP |
| OAuth 2.0 + bearer | RFC 6749 y RFC 6750 (oct. 2012) | delegación portadora |
| MAC (token) | borrador feb. 2012 | prueba de posesión (abandonado) |
| Revocación | RFC 7009 (2013) | ciclo de vida |
| OpenID Connect | final 26 feb. 2014 | identidad |
| PKCE | RFC 7636 (2015) | seguridad del código |
| Introspección | RFC 7662 (2015) | validación |
| SCIM | RFC 7643/7644 (2015) | aprovisionamiento |
| amr | RFC 8176 (2017) | claims |
| Token Binding | RFC 8471-8473 (2018) | prueba de posesión (sin adopción) |
| mTLS atado | RFC 8705 (2020) | sender-constrained |
| JWT BCP | RFC 8725 (2020) | buenas prácticas |
| RFC 9068 | 2021 | perfil de access token |
| DPoP | RFC 9449 (2023) | prueba de posesión |
| RFC 9700 | enero 2025 | mejores prácticas OAuth |
| NIST SP 800-63-4 | julio 2025 | identidad digital |

## 4.10 Cómo leer todo esto en una sola imagen

![Ciclo de vida de un token](img/10_lifecycle.png)

Cada protocolo de arriba actúa en una **etapa** del ciclo: **emisión** (OAuth/OIDC/MFA), **transporte**
(TLS/cookies/cabeceras), **uso** (bearer/mTLS/DPoP), **expiración** (`exp`), **rotación** (refresh) y
**revocación** (RFC 7009). Defender una API es **cubrir todas las etapas**, no solo la emisión.
