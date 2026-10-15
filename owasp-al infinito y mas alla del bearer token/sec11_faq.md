## 11. Preguntas frecuentes (FAQ)

Este anexo reúne, en formato de preguntas y respuestas, los puntos que más se repiten al dar la
charla y los que surgieron al revisarla. Sirve como **material de repaso** para el público y como
**preparación del turno de preguntas** para quien expone. No reemplaza a las secciones anteriores:
las referencia.

### 11.1 ¿Qué es HMAC-SHA1 y por qué importa?

**HMAC** (*Keyed-Hash Message Authentication Code*, RFC 2104) no es un cifrado: es un **código de
autenticación**. Combina **una clave secreta** con **una función de hash** para producir una etiqueta
que prueba **integridad** (nadie cambió el mensaje) y **autenticidad** (lo generó alguien que tiene la
clave):

```
HMAC(K, m) = H( (K ⊕ opad) || H( (K ⊕ ipad) || m ) )
```

- **SHA-1** es el hash (160 bits, NIST 1995). **HMAC-SHA1** es ese MAC con SHA-1.
- Es **simétrico**: la misma clave firma y verifica (a diferencia de RSA/ECDSA, que son asimétricos);
  eso obliga a **distribuir y custodiar el secreto** en ambos extremos.
- **Dónde aparece:** OAuth 1.0 firmaba **cada request** con HMAC-SHA1 (más `nonce` y `timestamp`); en
  JOSE, **HS256/384/512** es HMAC con SHA-256/384/512.
- **Matiz:** SHA-1 está roto para **colisiones** (SHAttered, 2017), pero **HMAC-SHA1 no está roto como
  MAC**. Aun así está **deprecado**: hoy se prefiere **SHA-256**.
- **Por qué se abandonó el firmar-por-request:** no por la cripto, sino por la operación —repartir un
  secreto distinto entre cada par de servicios y **canonicalizar** parámetros (orden, codificación)
  era frágil y muy difícil en móviles y SPAs (ver §3.4).

### 11.2 ¿Base64 es cifrado? ¿Todos los bearer tokens usan base64url?

- **No, base64 no es cifrado.** Es una **codificación**: representa bytes binarios como texto seguro
  para JSON/URL/HTTP. **No tiene clave** y se revierte con dos líneas.
- **No todos los bearer usan base64.** Base64url aparece en **JWT/JOSE** (para `header`, `payload` y
  `signature`). Un **bearer opaco** suele ser **bytes aleatorios**, sin estructura.
- **base64url vs. base64 estándar:** usa `-` y `_` en vez de `+` y `/`, y omite el relleno `=`, para
  viajar seguro en URLs.
- **Qué es cifrado, entonces:** *cifrado* (encryption) transforma los datos **con una clave** para dar
  **confidencialidad**: sin la clave, no se leen. En JOSE, el cifrado real es **JWE**. Un **JWT común
  es JWS: firmado, no sellado** — su payload **lo lee cualquiera** (ver §3 anatomía del JWT y §11.4).

### 11.3 ¿Qué son los claims, y qué son `amr` y `acr`?

- **Claims** son los **campos** (afirmaciones) del payload de un JWT: pares clave/valor. Los estándar
  incluyen `iss` (emisor), `sub` (sujeto), `aud` (audiencia), `exp` (expira), `nbf` (no antes), `iat`
  (emitido), `jti` (id único) y `scope`. Puede haber **claims propios** (cuidado con la PII).
- **`amr`** (*Authentication Method Reference*, RFC 8176): dice **cómo** se autenticó, como lista.
  Ej.: `["pwd","otp"]`, `["pwd","mfa","hwk"]` (llave de hardware), `["swk"]`.
- **`acr`** (*Authentication Context Class Reference*): dice **con qué nivel/contexto** se autenticó
  (una etiqueta que se puede mapear, p. ej., a los niveles AAL de NIST). En corto: **`amr` = con qué
  métodos; `acr` = con qué garantía**.
- **Matiz clave de la charla:** la API **no sabe** si hubo MFA **salvo** que el emisor ponga `amr`/`acr`
  **y** el validador los **revise**. De ahí el *step-up*: pedir más garantía solo para la operación
  sensible.

### 11.4 ¿Qué es JOSE (JWS, JWE, JWK, JWA, JWT)?

**JOSE** = *JavaScript Object Signing and Encryption*: la **familia** de estándares detrás del JWT.

- **JWS** (RFC 7515): **firma**. **JWE** (RFC 7516): **cifrado**. **JWK** (RFC 7517): **claves**.
- **JWA** (RFC 7518): **algoritmos**. **JWT** (RFC 7519): el **token con claims**.
- **RFC 8725**: buenas prácticas. **RFC 9068**: perfil de JWT para access tokens.
- Todo se codifica en **base64url**. Regla de oro: **JWS = firmado (legible); JWE = cifrado
  (confidencial)**.

### 11.5 ¿Qué relación tienen las versiones de HTTP con el token?

Versiones: **HTTP/0.9**, **1.0 (1996)**, **1.1 (1997)**, **HTTP/2 (2015)**, **HTTP/3 (2022, sobre
QUIC/UDP)**. Lo que **sí** toca al token:

- El header **`Authorization`** y las **cookies** son conceptos de **HTTP** (independientes de la
  versión); todo token viaja **dentro** de HTTP.
- **HTTP/2**: framing binario, **multiplexing** y **compresión de cabeceras (HPACK)**. Comprimir
  cabeceras con secretos habilita ataques de **compresión** (familia BREACH/CRIME); el multiplexing
  cambió cómo aparecen los *request smuggling*.
- **HTTP/3 (QUIC)**: transporte sobre UDP, **QPACK** y **TLS 1.3 obligatorio**; cambia el
  comportamiento de proxies e inspección (misma ceguera que con gRPC binario).
- **Marco de autenticación HTTP**: se reorganizó de **RFC 2617** → **RFC 7235 (2014)** → **RFC 9110
  (2022)**; **Basic** pasó a **RFC 7617** y **Digest** a **RFC 7616**.
- **HTTP/1.1** popularizó el header `Referer`: por eso el token en **query** se filtra a otros sitios.
  **RFC 9700 (2025)** prohíbe el token en la URL.

En síntesis: la versión de HTTP **no crea** el problema del bearer, pero **cambia la superficie**
(compresión de cabeceras, inspección de binario, smuggling, terminación TLS). Ver §4.1.

### 11.6 ¿Qué fue primero: la cookie o Digest?

**La cookie.** El orden de primera aparición pública es:

1. **HTTP Basic** — concepto de 1993; en el RFC 1945 (HTTP/1.0, 1996).
2. **Cookie** — Netscape, idea de **1994**, especificación pública hacia **1996**.
3. **Digest** — estandarizado en el **RFC 2069 (1997)** y luego en el **RFC 2617 (1999)**.

O sea, **la cookie es anterior a la estandarización de Digest**. Digest, además, no manda la
contraseña en claro sino un **hash con un `nonce`** (v1: MD5; el RFC 7616, 2015, admite SHA-256). Pero
el servidor necesita guardar el **HA1**, que es **equivalente a la contraseña**, y el esquema no
protege el cuerpo del mensaje; quedó prácticamente en desuso. Hoy sobrevive sobre todo **Basic**, como
`client_secret_basic` en OAuth. Ver §3.1.

### 11.7 ¿Qué diferencia hay entre mTLS y DPoP?

- **mTLS** (mutual TLS): **ambas** partes presentan certificado. Da **autenticación fuerte de
  cliente** y permite **atar el token al certificado** (RFC 8705): el servidor exige el **mismo
  certificado** en cada llamada. Robar el token **no alcanza**. Costo: **PKI**, rotación de
  certificados y cuidado con proxies/balanceadores que **terminan TLS** y rompen la atadura.
- **DPoP** (RFC 9449, 2023): **sin PKI**. El cliente genera un par de claves; manda
  `Authorization: DPoP <token>` + una cabecera **`DPoP`** con un **JWT firmado por su clave privada**,
  que incluye **`jti`** único (anti-replay), **`htm`** (método) y **`htu`** (URL). El servidor valida
  la prueba y rechaza el token sin ella; robar el access token **no sirve**. Hay que registrar los
  `jti` usados y controlar la ventana de `iat`.

Ver §11.11 (prueba de posesión) y §4 (protocolos).

### 11.8 ¿Por qué una passkey resiste el phishing?

- Una **passkey** es una credencial **WebAuthn/FIDO2** (W3C/FIDO, 2019): un **par de claves** por
  sitio. La **privada** vive en un autenticador (TPM, Secure Enclave, llave de hardware) y **nunca
  sale**; el servidor guarda la **pública**.
- El servidor manda un **desafío**; el autenticador firma `challenge` + `origin`/RP ID; el servidor
  verifica con la pública. **No viaja ningún secreto compartido**.
- **Resiste el phishing por diseño:** el `origin` va **atado criptográficamente** a la firma. Si te
  llevan a `evil.com`, el autenticador **no firma para ese origen** (o firma un dominio que el servidor
  real rechaza). El atacante **no puede reusar** la firma.
- **Contraste:** **TOTP/OTP** se puede **phishear en tiempo real** (AiTM) y **SMS** es el más débil.
  NIST SP 800-63-4 (jul. 2025) empuja los factores *phishing-resistant*. Ver §M10/Bloque 4.

### 11.9 ¿Qué son la fatiga de push, MITRE ATT&CK, AiTM, los infostealers y el pass-the-cookie?

- **Fatiga de push / push bombing:** el atacante **ya tiene la contraseña** y dispara **muchos push**
  hasta que la víctima aprueba uno. Es **MITRE ATT&CK T1621** (*MFA Request Generation*).
- **MITRE ATT&CK:** la **matriz pública de tácticas y técnicas** de adversarios (táctica = por qué;
  técnica = cómo). Las de acá: **T1621** y **T1539** (*Steal Web Session Cookie*).
- **Phishing AiTM** (*adversary-in-the-middle*): un **proxy inverso** entre víctima y sitio real. No
  roba solo la contraseña: **intercepta la sesión ya autenticada** (cookie/token que resultó de la
  MFA). La MFA "pasó", pero el atacante se quedó con la sesión.
- **Infostealer:** **malware** que extrae del navegador **cookies, tokens y credenciales** y los manda
  al atacante.
- **Pass-the-cookie:** **reutilizar** la cookie/token robado **en otro equipo**, sin contraseña ni MFA.
- **"Roban el artefacto":** no roban a la **persona** ni su **contraseña**: roban el **token/cookie**.
  En los tres casos **la MFA hizo su trabajo**; el problema es que el artefacto **se reutiliza** porque
  **no está atado a su portador**. Ver §Bloque 4 y §5.5.

### 11.10 ¿Qué significa "JWT mal validado"?

El token es correcto; el **validador** está mal. Clases típicas:

- **`alg: none`**: si el receptor confía en el `alg` del token y acepta "sin firma", cualquiera forja.
- **Confusión HS/RS**: el token dice `RS256`, pero el código, al cambiar a `HS256`, usa la **clave
  pública como secreto HMAC** (y la pública es pública).
- **Inyección de `kid`**: `kid` apunta a una clave controlada por el atacante.
- **No validar** `iss`, `aud`, `exp`, `nbf` (o aceptar cualquier emisor/audiencia), o **no verificar la
  firma**.

**Regla (RFC 8725 / OWASP):** la política de verificación sale de la **configuración**, nunca del
token. Ver §5.7.

### 11.11 ¿Qué es la prueba de posesión (PoP)?

Idea: para usar el token **no basta tenerlo**; hay que **demostrar que se tiene la clave privada**,
firmando algo **por request**. Implementaciones: **mTLS** atado al certificado (RFC 8705), **DPoP**
(RFC 9449) e históricos como **OAuth 1.0** (HMAC por request) y el tipo **`mac`** (abandonado). Robar
el token **no alcanza** sin la clave privada. Es lo contrario del bearer.

### 11.12 ¿Qué son los tokens opacos, la introspección y el claim `aud`?

- **Token opaco:** string **sin contenido legible** (no es un JWT). No se pueden sacar claims de él;
  hay que **preguntar**. Ventaja: no filtra datos y se revoca fácil; desventaja: cada validación es
  una llamada.
- **Introspección** (RFC 7662): el **servidor de recursos** pregunta al **servidor de autorización**
  (`POST /introspect`) si el token sigue **activo** y con qué `scope`/`sub`. Costo y latencia; la
  revocación debe **propagarse** a las réplicas.
- **`aud`** (*audience*): **para quién** es el token. Validado **estrictamente**, un token robado
  **emitido para otra app** no sirve. Es el claim que **responde al problema del §10.3** de RFC 6749.

### 11.13 ¿Qué son BOLA, BFLA y BOPLA?

- **BOLA** (OWASP API1, *Broken Object Level Authorization*): **autorización a nivel de objeto**. El
  token es válido, pero pedís **otro objeto** (`/orders/456`) y no se chequea **de quién es**. Es el
  riesgo **#1**; ronda ~40 % de los ataques a APIs (IDOR).
- **BOPLA** (OWASP API3, *Broken Object Property Level Authorization*): a nivel de **propiedad/campo**.
  Se exponen o aceptan **campos que no corresponden** (*mass assignment* / *excessive data exposure*):
  el cliente manda `isAdmin:true` o recibe campos de más.
- **BFLA** (OWASP API5, *Broken Function Level Authorization*): a nivel de **función/endpoint**. Un
  usuario común accede a funciones de admin porque el rol no se chequea por **ruta/acción**.

**Regla:** *autenticar* ≠ *autorizar*. El token resuelve **quién**; BOLA/BOPLA/BFLA son **qué puede
hacer sobre qué**. Ver §5.6 y §6.

### 11.14 ¿Todos los flujos de OAuth 2 usan tokens? ¿El bearer es exclusivo de OAuth?

- **Sí: todos los flujos de OAuth 2 emiten un access token.** **Authorization Code** (+ **PKCE**, hoy
  obligatorio para clientes públicos) es el recomendado; **Client Credentials** (§4.4) es **M2M** sin
  usuario; **Implicit** y **Password (ROPC)** están **retirados/deprecados** por **RFC 9700 (2025)**.
- No todos emiten **refresh** (Implicit no) ni involucran **usuario** (Client Credentials), y no todos
  los tokens son **bearer** (pueden ser **sender-constrained**: mTLS/DPoP). Pero **el objetivo de
  OAuth es emitir un access token**.
- **El bearer no es exclusivo de OAuth.** El esquema `Authorization: Bearer` vive en el **marco de
  autenticación HTTP** y lo puede usar cualquier API. **RFC 6749** (OAuth 2.0) y **RFC 6750** (Bearer)
  son compañeros, pero **distintos**; de hecho el propio RFC 6749 definía **`bearer` y `mac`**, y hoy
  OAuth puede emitir tokens **sender-constrained** que **no** son bearer puro. Y **OAuth 1.0** no usaba
  bearer: **firmaba** cada request.

### 11.15 ¿Cuáles son los seis estilos de API y su riesgo característico? (slide 5 de la taxonomía)

| Estilo | Cómo es | Riesgo característico | Por qué |
|---|---|---|---|
| **REST** | recursos + verbos HTTP | **BOLA / IDOR** | Expone **IDs de objeto** en la URL; si no se valida **de quién es**, cambiando el ID se ve lo ajeno. |
| **GraphQL** | un endpoint, consulta del cliente | **query depth / sobre-exposición** | Consultas profundas = DoS y campos que no querías exponer. |
| **gRPC** | HTTP/2 + protobuf binario | **WAF no inspecciona** | El cuerpo binario no lo parsean los WAF/proxies genéricos. |
| **SOAP** | XML + WSDL | **XXE** | Parsear XML con **entidades externas** habilita XXE/SSRF. |
| **WebSocket** | canal persistente | **auth solo al inicio** | El *handshake* autentica una vez; después no se reevalúa por mensaje. |
| **Webhooks / eventos** | push del servidor a una URL | **SSRF / replay** | Se llama a una **URL elegida por el cliente** y los eventos deben **verificarse por firma**. |

Idea: **la receta de REST no se copia y pega**; cada estilo necesita su propio modelo de amenaza.

### 11.16 ¿Dónde viaja el token, y por qué la MFA "no está en la API"? (slides 13 y 14)

- **Dónde viaja:** RFC 6750 (2012) admitía **cabecera `Authorization`**, **cuerpo** del formulario y
  **query string** (`?access_token=...`). La **query** es un desastre: termina en **logs**, en
  `Referer`, en el **historial** y en **cachés**. Por eso **RFC 9700 (2025) prohíbe tokens en URIs**.
  La **cabecera** es **inmune a CSRF**; la **cookie** (con `HttpOnly`) protege de **XSS** pero exige
  mitigar **CSRF** (`SameSite`, token anti-CSRF).
- **La MFA no está en la API:** el flujo es `password → MFA → emisión → token (vive mucho) → API`. La
  MFA ocurre **una vez** en el servidor de autenticación; después la API solo recibe un **string**. La
  API **no sabe** que hubo MFA salvo por `amr`/`acr`. Conclusión: **la MFA protege la generación del
  artefacto, no su posesión posterior.**

### 11.17 Persona vs. sistema (slide 18)

| | **Persona** | **Sistema (M2M)** |
|---|---|---|
| Qué se prueba | que un **humano** se autenticó ante un IdP | que un **workload** pidió el token |
| Segundo factor | passkey / OTP / push | **no existe** |
| Artefacto | sesión + access token corto | token corto o **credencial efímera** |
| Vida típica | minutos-horas | **muy corta**, rotada |
| Fallo típico | fatiga, AiTM, robo de sesión | **secretos eternos** en repos/CI |
| Revocación | cerrar sesión / revocar | rotar credencial |

Mecanismos del lado sistema: `client_credentials` (RFC 6749 §4.4), `private_key_jwt` (RFC 7523),
**mTLS** (RFC 8705), **DPoP** (RFC 9449). Ver §Bloque 4.

### 11.18 Checklist final y cierre (slides 26 y 28)

**Checklist (8 preguntas):** (1) ¿la verificación del `alg` sale de la **config**? (2) ¿validás
`iss`/`aud`/`exp` con tolerancia corta? (3) ¿el access token vive lo que debe? (4) ¿hay **rotación y
revocación** del refresh? (5) ¿la **autorización a nivel de objeto** (BOLA) está resuelta? (6) ¿el
token va en **cabecera** y nunca en la URL? (7) ¿las **identidades de máquina** usan credenciales de
vida corta? (8) ¿qué queda en los **logs**?

**Cierre (tres mensajes):** (1) el token es **finito**: emitir, rotar, revocar —la ausencia de `exp`
ya es vulnerabilidad; (2) la **MFA protege la emisión, no la posesión**: diseñá para el robo de
artefactos; (3) **autenticar es la puerta, autorizar es la cerradura** —un token perfecto no impide
BOLA. Frase final: *la seguridad nunca estuvo en el string; estuvo siempre en el sistema.*

### 11.19 ¿Cuáles son los distintos puntos de vista para abordar una API?

Se ordenan en **tres familias** (qué / cómo / para quién), y están desarrollados en §1:

- **Familia A — qué se mira:** capas de arquitectura; actor (persona/sistema/delegación); **ciclo de
  vida de la credencial**; ciclo de vida del software (*shift-left*); superficie de ataque; dato y
  contrato (OpenAPI/AsyncAPI); **estilo de API**; protocolo y transporte; tipo de consumidor; modelo
  de despliegue; **identidad humana vs. no humana (NHI)**.
- **Familia B — cómo se defiende:** paradigma de confianza (identidad vs. posesión); modelo de
  autorización (RBAC/ABAC/ReBAC/PBAC, OPA); criptografía y gestión de claves (JOSE/PKI/KMS/HSM);
  control de tráfico (gateway, rate limiting); validación y saneamiento; observabilidad y respuesta;
  secretos, identidad de máquina y cadena de suministro.
- **Familia C — para quién y por qué:** OWASP API Top 10; *threat modeling* (STRIDE, LINDDUN…);
  audiencia (devs/arquitectos/seguridad/management); cumplimiento (ISO 27001, PCI, NIST; en Uruguay,
  Ley 18.331, Decreto 66/025, CERTuy); privacidad; negocio y abuso económico; madurez y gobierno
  (SAMM); economía del atacante; histórico/evolutivo; académico/formal (Saltzer & Schroeder);
  resiliencia; anti-patrones.

**Combinación recomendada:** histórico + ciclo de vida (hilo narrativo), actor + autorización
(corazón), OWASP + estilo de API (atlas), threat modeling + SDLC (cómo se trabaja),
cumplimiento/privacidad/negocio (por qué importa). Ver §1 y su tabla comparativa.

### 11.20 Los tres casos reales, en detalle

- **Facebook "View As" (2018).** Interacción de **tres bugs**: el *video uploader* aparecía en "View
  As"; usaba SSO y generaba un access token con permisos de la app móvil; y **generaba el token no del
  espectador sino del usuario consultado**, dejándolo **embebido en el HTML**. Los atacantes pivotaban
  de cuenta en cuenta (~50M tokens reseteados; ~90M cuentas re-login). Lección: **se emitió al usuario
  equivocado**; el token funcionó como fue diseñado. Ver §5.1.
- **Okta / Cloudflare (octubre de 2023).** Ataque al **sistema de soporte de Okta**: los atacantes
  accedieron a archivos de tickets y **secuestraron un session token** de un ticket creado por un
  empleado de Cloudflare; con esa sesión (privilegios administrativos) accedieron a sistemas el **18 de
  octubre de 2023**. Cloudflare detectó y contuvo. **No es la primera vez:** en **enero de 2022** Okta
  ya había sufrido otro incidente (un proveedor de soporte comprometido) y en ese caso Cloudflare **no
  fue impactado** porque usaba **llaves de hardware** para MFA. Lección: un bearer robado **vive lo que
  le hayan dado**; la **rotación y la revocación** (RFC 7009) son parte de la seguridad. Ver §5.2.
- **Codecov (2021).** Un error en el build de la **imagen Docker** expuso una **clave HMAC** de una
  service account; con ella se modificó el **Bash Uploader** servido desde GCS para **exportar las
  variables de entorno del CI** (`$(env)` + `git remote -v`) a un servidor del atacante (31/1/2021 a
  1/4/2021). Se detectó porque un cliente **comparó el SHA256** del script. Lección: **tokens/claves
  del CI filtrados**; cadena de suministro. Ver §5.3.

> **Nota de método:** todos los casos se citan como **divulgaciones públicas** y se analizan como
> **fallas de modelo**, nunca como críticas a organizaciones o personas.
