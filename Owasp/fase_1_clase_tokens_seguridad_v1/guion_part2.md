# BLOQUE 3 — Anatomía: qué se valida realmente (≈8 min)

*Slide 5: un JWT anotado con tres colores (header, payload, firma).*

## 3.1 La anatomía de un JWT

Un JWT es `header.payload.signature`, tres partes separadas por puntos, cada una codificada en base64url. Esto hay que decirlo con cuidado porque hay un error común: **base64 no es cifrado**. Cualquiera puede leer el payload. Un JWT es como una credencial plastificada: está firmada, no sellada. Si necesitás confidencialidad, usás JWE —**JSON Web Encryption, RFC 7516, mayo de 2015**—, que es otra pieza de la familia JOSE (**JWS, RFC 7515**; **JWK, RFC 7517**; **JWA, RFC 7518**; todas mayo de 2015; y **JWT, RFC 7519, mayo de 2015**).

**Primera aparición de la familia:** el primer borrador de JSON Web Token se publicó el **28 de diciembre de 2010**, y la norma maduró cuatro años y medio hasta su RFC en mayo de 2015.

El header lleva, como mínimo, `alg` —el algoritmo de firma—. Y ahí está el origen de una familia entera de ataques que veremos en el Bloque 5: **si el receptor decide cómo verificar en función de lo que dice el token, un atacante puede elegir el algoritmo.** Por eso **RFC 8725 ("JSON Web Token Best Current Practices", febrero de 2020)** y el [cheat sheet de JWT de OWASP](https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html) insisten: **el algoritmo debe venir de la configuración del validador, nunca del token.**

## 3.2 Los claims que importan (y por qué)

- **`iss` (issuer):** quién lo emitió. Debe validarse contra la lista de emisores confiables.
- **`aud` (audience):** para quién es. **Éste es el claim que responde a la pregunta del RFC 6749 §10.3**: si validás `aud` estrictamente, un token robado emitido para otra aplicación no te sirve.
- **`exp` / `nbf` / `iat`:** expiración, "not before", emisión. **`exp` es obligatorio en access tokens según RFC 9068 (mayo de 2021)**.
- **`sub` (subject):** a quién representa.
- **`scope` o `scp`:** qué puede hacer. Mínimo privilegio.
- **`jti` (JWT ID):** identificador único, para anti-replay y revocación por lista.
- **`amr` (Authentication Methods References):** *cómo se autenticó* — "pwd", "mfa", "otp", "hwk". **Primera aparición: RFC 8176, agosto de 2017.** Este claim es la bisagra de todo el Bloque 4: es el puente entre "pasó la MFA" y "el token lo sabe".
- **`acr` (Authentication Context Class Reference):** *a qué nivel de garantía* se autenticó. Es la base del step-up authentication.
- **`kid` (Key ID):** qué clave usó el firmante, en el header.

*Frase hablada:* "Un JWT bien validado responde cuatro preguntas: ¿quién lo emitió?, ¿es para mí?, ¿está vigente?, ¿tiene permiso? Un JWT mal validado sólo responde una: ¿está firmado?"

## 3.3 La checklist mínima de validación

*Slide sugerida: checklist de 8 puntos.*

1. Verificar la firma con la clave pública del emisor — **jamás con una clave que venga del propio token**.
2. Verificar `alg` contra la configuración esperada (rechazar `none`; no mezclar HS/RS).
3. Verificar `iss` contra la lista confiable.
4. Verificar `aud` estrictamente.
5. Verificar `exp` y `nbf` con tolerancia de reloj explícita (pocos segundos, no minutos).
6. Verificar `scope`/`scp` requerido para el endpoint.
7. Verificar restricciones de emisor del cliente, si aplica (`azp`).
8. Luego —y sólo luego— **autorizar a nivel de objeto** (aquí entra el BOLA del Bloque 5).

**La lista va en ese orden a propósito:** los puntos 1–7 son *autenticación e integridad del token*; el punto 8 es *autorización*. Confundirlos es el error más común de la disciplina.

## 3.4 Dónde se transporta el token (y dónde no)

**RFC 6750, octubre de 2012**, define **tres** transportes: cabecera `Authorization: Bearer` (§2.1), cuerpo `form-encoded` (§2.2) y **query parameter** (§2.3). Los tres están permitidos por la norma de 2012.

Y acá viene el contraste temporal más bonito de la charla: **RFC 9700, "Best Current Practice for OAuth 2.0 Security", enero de 2025 —que reemplazó a RFC 6819 (2013) como documento de mejores prácticas— prohíbe expresamente transportar access tokens en URIs.** Trece años separan la permisión y la prohibición, porque trece años de logs, de cadenas `Referer`, de historiales de navegador y de CDN nos enseñaron dónde terminan los tokens que van en URLs.

También conviene repasar el dilema cabecera vs. cookie:
- **Cabecera:** no la manda el navegador automáticamente → inmune a CSRF por diseño, pero el cliente debe guardarla (y guardarla en `localStorage` la expone a XSS).
- **Cookie `HttpOnly` + `Secure` + `SameSite`:** inmune a XSS para la lectura, pero requiere mitigar CSRF, y aplica a contexto de navegador, no a API de cliente nativo o servidor a servidor.

*Frase de cierre del bloque:* *"Validar un token es fácil si sabés qué preguntas hacer. El problema es que muchas implementaciones se quedan en la primera pregunta —¿está firmado?— y contestan 'sí' a todo lo demás."*

---

# BLOQUE 4 — MFA en APIs: cuando la invoca una persona y cuando la invoca un sistema (≈14 min)

*Este es el bloque central de la charla. No se recorta en la versión de 30 minutos.*

## 4.1 La tesis: la MFA no está en la API

Quiero arrancar este bloque con la idea que justifica el título completo de la charla:

**La autenticación multifactor no ocurre en la API. Ocurre en el momento de la emisión. Después de la MFA, todo lo que la API recibe es un string.**

El flujo real de una persona es: contraseña → MFA en el servidor de autenticación → se emiten tokens → la API recibe el access token. En ese punto, la API **no sabe, y no puede saber**, si la MFA ocurrió. Sólo lo sabe si se lo dicen los claims —`amr`, `acr`, `auth_time`—, y sólo si el emisor los puso ahí y el validador los revisa.

**Consecuencia práctica:** la MFA protege la *generación* del artefacto. No protege la *posesión posterior* del artefacto. Todo el bloque 4 gira alrededor de esa frase.

*Slide sugerida: timeline horizontal: [Password] → [MFA] → [Emisión de token] → [30 días de vida del token] → [API]. Resaltar que la MFA cubre un instante y el token cubre semanas.*

## 4.2 Caso A: la API la invoca una persona

### 4.2.1 El marco normativo

- **OpenID Connect Core 1.0** (final aprobado el **26 de febrero de 2014**) es el protocolo que, sobre OAuth 2.0, convierte "el usuario pasó la MFA" en "aquí tenés un ID token con `auth_time` y `acr`".
- **NIST SP 800-63, "Digital Identity Guidelines"**, en su primera edición desde **2011** (800-63-1), define el marco de niveles de garantía. La versión **800-63-3 (junio de 2017)** introdujo los **AAL (Authenticator Assurance Levels)**: AAL1, AAL2 y AAL3. **La edición vigente es SP 800-63-4, publicada en julio de 2025** ([suite completa](https://pages.nist.gov/800-63-4/), [800-63B-4: autenticación](https://pages.nist.gov/800-63-4/sp800-63b.html)).
- **`amr`: RFC 8176, agosto de 2017.**

Lo que dice NIST —y es la idea académica que te conviene enunciar— es que **no todos los autenticadores dan la misma garantía**, y que el nivel de garantía debe estar ligado al riesgo de la operación. De ahí salen dos conceptos:

- **AAL2** exige dos factores de tipos distintos.
- **AAL3** exige prueba criptográfica de posesión de una clave en hardware y resistencia a la suplantación del verificador —es decir, passkeys/WebAuthn en la práctica.

### 4.2.2 Jerarquía de métodos (para una slide de "no todos los MFA son iguales")

1. **WebAuthn / passkeys / FIDO2** — **WebAuthn llegó a Recomendación del W3C en marzo de 2019**. Resistencia al phishing por diseño: el desafío está ligado al origen, así que un sitio falso no puede usarlo. Es el único factor que sobrevive al phishing clásico.
2. **TOTP (OTP de tiempo)** — mejor que nada, pero es un código que se puede phishear en tiempo real (y los ataques AiTM exactamente eso hacen).
3. **SMS** — el más débil de los aceptables; expuesto a SIM swapping y a intercepción. NIST en 800-63B-4 lo trata con cautelas según el escenario de riesgo.
4. **Push de aplicación** — cómodo, pero creado con un agujero conocido: la fatiga. Ver 4.5.

**Passkeys**: alineados con **NIST SP 800-63-4 (julio de 2025)**, que incorporó explícitamente los *syncable authenticators* (passkeys sincronizables) a la taxonomía.

### 4.2.3 Step-up: la MFA no es un evento único

Concepto académico importante: **step-up authentication**. No autenticás una vez para todo; autenticás con más fuerza según el riesgo de la operación.

- `acr` y `auth_time` permiten a la API —o al servidor de autorización— preguntar: *¿esta transferencia se autoriza con una sesión autenticada hace seis horas o con una autenticación de menos de dos minutos y a nivel AAL3?*
- OIDC permite exigir re-autenticación (`prompt=login`) y fijar un `acr_values` deseado.
- En términos de tokens: una operación sensible debería exigir **emitir un token nuevo**, con `acr` elevado, en ese momento —no reutilizar el token de la sesión de la mañana.

*Cita hablada sugerida:* "El step-up es la diferencia entre exigir el DNI en la puerta del país y exigirlo en la puerta del banco central. Misma identidad, distinto umbral."

### 4.2.4 Los tres modos en que la MFA no salva a un bearer

Aquí es donde la teoría se encuentra con los incidentes reales. Hay exactamente tres familias de ataque que la MFA no cubre, porque atacan *después* de la emisión:

**1. Fatiga de MFA (push bombing).** El atacante ya tiene la contraseña, dispara pushes repetidos hasta que la víctima, harta, aprueba. **MITRE ATT&CK lo registra como T1621, "Multi-Factor Authentication Request Generation".** Caso público emblemático: **Uber, septiembre de 2022** —credenciales de un contratista compradas en un foro, y luego un mensaje de texto suplantando al área de IT para que el empleado aprobara el prompt ([NYT](https://www.nytimes.com/2022/09/15/technology/uber-hacking-breach.html), [UpGuard](https://www.upguard.com/blog/what-caused-the-uber-data-breach)).

**2. Adversary-in-the-Middle (AiTM).** El phishing ya no roba la password: intercepta la *sesión completa* resultante de la MFA. El atacante queda con un token ya autenticado y la víctima no se entera.

**3. Robo de sesión / infostealers.** Malware que extrae cookies y tokens del navegador. La familia de ataques se llama "pass-the-cookie": se pega la sesión en otro navegador y el servidor no distingue nada. Familias como RedLine, Raccoon o Vidar están orientadas exactamente a esto.

**Síntesis para la slide:** *"La MFA protege el instante de la emisión. Todo lo que ocurre después —fatiga, intercepción, robo de artefactos— queda fuera de su alcance."*

## 4.3 Caso B: la API la invoca un sistema

Ahora el otro lado, que es donde está la mayoría del tráfico real de las APIs y donde menos se piensa.

### 4.3.1 El cambio de pregunta

Cuando el invocador es un microservicio, un job de CI, un dispositivo IoT o una integración de un tercero, **la pregunta "¿quién es el usuario?" no tiene respuesta, porque no hay usuario.** La pregunta correcta es: **¿qué workload es este, con qué credenciales de ciclo de vida corto, y bajo qué contexto está hablando?**

**No hay MFA aplicable.** No hay un segundo factor que mostrar: no hay persona, no hay dispositivo con pantalla, no hay "momento de autenticación". Por eso la afirmación que quiero que se lleven es:

**El equivalente funcional del MFA para sistemas no es un segundo factor puntual: es la posesión de una identidad de workload fuerte, verificable y de vida corta.**

### 4.3.2 Los mecanismos, con su primera aparición

| Mecanismo | Qué aporta | Primera aparición |
|---|---|---|
| **Client credentials grant** — el sistema se autentica solo y obtiene un access token | El estándar mínimo para máquina | RFC 6749 §4.4, octubre 2012 |
| **Asertión JWT firmada del cliente (`private_key_jwt`)** | Autenticación de cliente con clave privada en vez de secreto compartido | RFC 7523, 2015 |
| **mTLS: identidad por certificado + token atado al certificado** | La posesión del token no basta: hay que presentar el certificado emparejado | RFC 8705, febrero de 2020 |
| **DPoP: token atado a una clave privada del cliente** | Lo mismo, sin la infraestructura de certificados; prueba de posesión por request | RFC 9449, octubre de 2023 |
| **Firma de requests estilo HMAC por petición (AWS SigV4)** | El retorno, en el fondo, a la idea de OAuth 1.0: firmar cada request | práctica de industria (AWS Signature Version 4, documentada desde 2014) |
| **Identidad de workload (SPIFFE/SPIRE, federación de identidad en la nube)** | Identidad emitida por infraestructura, con rotación automática | SPIFFE, proyecto CNCF (2017-) |
| **Credenciales temporales tipo STS** | Secretos de minutos en lugar de años | práctica de industria (AWS STS, 2011-) |
| **Rotación automática y mínimo privilegio** | El "MFA continuo" del sistema | NIST SP 800-63-4 (2025) para personas; ISO 27001/Gestión de secretos para máquinas |

### 4.3.3 El dato que le da urgencia al bloque

**GitGuardian enmarcó su último informe explícitamente alrededor de la "crisis de identidades no humanas (NHI)"**: la inmensa mayoría de los secretos filtrados no son passwords de personas, son credenciales de sistemas —API keys, tokens de CI, claves cloud—, y **más del 60 % de los secretos válidos detectados en 2022 seguían activos años después** ([State of Secrets Sprawl 2026](https://www.gitguardian.com/state-of-secrets-sprawl-report-2026)).

*Cita hablada sugerida:* "Nos pasamos años peleando con la MFA para las personas, mientras las máquinas seguían usando llaves eternas guardadas en un archivo de texto."

## 4.4 Tabla comparativa (slide de cierre del bloque)

| Eje | Persona | Sistema |
|---|---|---|
| Qué se prueba | Que un humano se autenticó ante un IdP | Que un workload concreto pidió este token |
| Segundo factor | Passkey / OTP / push (NIST AAL2-AAL3) | No aplica: clave privada + certificado + contexto |
| Artefacto resultante | Sesión (larga) + access token (corta) + refresh token | Access token corto o credencial efímera |
| Vida típica | Minutos a horas (access token) | Minutos; rotación automática |
| Revocación | Endpoint de revocación (RFC 7009) y logout | Rotación/revocación de claves y de identidad |
| Fallo típico | Fatiga MFA, AiTM, infostealers | Secretos eternos en CI/repos, sin rotación |
| Dónde se decide | El IdP, al emitir (`acr`, `amr`) | El emisor de identidad de workload y su política |

*Frase de cierre del bloque:* *"Para la persona, la pregunta es '¿quién pasó la MFA?'. Para el sistema, la pregunta es '¿qué credencial de qué vida corta me está hablando, y de qué contexto viene?'. Aplicar el marco de uno al otro es el error más caro de la disciplina."*

---

# BLOQUE 5 — Ataques reales con bearer tokens: observación, no señalamiento (≈12 min)

*Framing inicial obligatorio, léelo casi literal:*

> "Los casos que siguen son todos divulgaciones públicas y responsables. Los equipos que los reportaron hicieron bien su trabajo. No voy a decir 'esto estuvo mal hecho' —voy a decir 'esto es lo que produce el modelo de seguridad por posesión'. Si algo enseñan estos casos es que el token funcionó exactamente como estaba diseñado para funcionar: si lo tenés, entrás. El fallo nunca está en el string."

## 5.1 Token emitido mal en el cliente — Facebook, septiembre de 2018

**Qué pasó:** una interacción de tres bugs en la función *"View As"* —que muestra tu perfil como lo ve otro usuario— hizo que el cargador de videos generara un access token **no del espectador, sino del usuario consultado**, y lo dejara embebido en el HTML de la página. Los atacantes lo extrajeron de ahí.
**Resultado:** 50 millones de access tokens reseteados y, precautoriamente, otros 40 millones: unas 90 millones de cuentas obligadas a volver a iniciar sesión.
**Fuente:** [actualización oficial de Meta](https://about.fb.com/news/2018/09/security-update/) · [análisis de KrebsOnSecurity](https://krebsonsecurity.com/2018/09/facebook-security-bug-affects-90m-users/).
**Lección académica:** el token era perfectamente válido, estaba perfectamente firmado, y **no debía existir para ese usuario**. La validación criptográfica no cubre errores de emisión.

## 5.2 Token robado y no revocado — Okta / Cloudflare, octubre de 2023

**Qué pasó:** en la brecha del sistema de soporte de Okta, un *session token* que un empleado de Cloudflare había incluido en un ticket de soporte fue extraído. Cloudflare confirmó después que **el atacante usó esa sesión** —con privilegios administrativos— para acceder a sus sistemas el 18 de octubre de 2023, y que la cadena se debió a que esos tokens no se rotaron ni revocaron tras el incidente inicial. **No es la primera vez:** en enero de 2022 Okta ya había sufrido un incidente en el que quedó comprometido un proveedor de soporte; en ese caso Cloudflare **no fue impactado** porque usaba **llaves de hardware** para MFA.
**Fuente:** [blog de Cloudflare (2023)](https://blog.cloudflare.com/how-cloudflare-mitigated-yet-another-okta-compromise/) · [blog de Cloudflare sobre el incidente de 2022](https://blog.cloudflare.com/cloudflare-investigation-of-the-january-2022-okta-compromise/).
**Lección académica:** un bearer robado tiene la vida que ustedes le hayan dado. **La revocación y la rotación son parte de la seguridad del token, no un "nice to have"** ([RFC 7009, octubre de 2013](https://www.rfc-editor.org/rfc/rfc7009)).

## 5.3 El bearer que vive en la cadena de suministro — Codecov, 2021

**Qué pasó:** un atacante modificó el script `Bash Uploader` de Codecov —presente en su imagen de Docker— durante aproximadamente dos meses (desde fines de enero de 2021). La modificación añadía una línea que **exportaba todas las variables de entorno del job de CI** a un servidor remoto. Quienes ejecutaban el script en su pipeline filtraban sus tokens, claves AWS, deploy keys y credenciales de Git.
**Fuente:** [post oficial de Codecov](https://about.codecov.io/security-update/) · [análisis de Rapid7](https://www.rapid7.com/blog/post/2021/04/16/codecov-discloses-supply-chain-compromise/).
**Lección académica:** aquí **no hay persona que autenticar con MFA**. El token pertenece a un sistema, vive en una variable de entorno y no tiene "segundo factor" posible. Su única defensa es vida corta, rotación, mínimo privilegio y detección de fugas. Es el ejemplo perfecto para cerrar la distinción del Bloque 4.

## 5.4 Los secretos eternos — datos de campo

**Qué dicen los datos:** [GitGuardian State of Secrets Sprawl 2026](https://blog.gitguardian.com/the-state-of-secrets-sprawl-2026/): **28,65 millones de secretos nuevos** en commits públicos de GitHub en 2025 (+34 % interanual, el mayor salto registrado); **1,27 millones** de secretos sólo de servicios de IA; y más del **60 % de los secretos válidos de 2022 seguían activos** años después.
**Lección académica:** el bearer más extendido del mundo —la API key hardcodeada— no tiene `exp`. **La ausencia de expiración es, en sí misma, una vulnerabilidad de diseño.**

## 5.5 La MFA no sobrevive al robo de la sesión — Uber, septiembre de 2022

**Qué pasó:** credenciales de un contratista externo aparecieron en un mercado de la dark web; el atacante las usó, se topó con MFA, y resolvió la situación enviándole al empleado un SMS suplantando al equipo de IT, hasta obtener la aprobación del prompt. Después, acceso a las consolas internas (AWS, G Suite, etc.).
**Fuentes:** [NYT](https://www.nytimes.com/2022/09/15/technology/uber-hacking-breach.html) · [UpGuard](https://www.upguard.com/blog/what-caused-the-uber-data-breach).
**Lección académica:** ver 4.5. **La MFA protege el instante de la emisión; el artefacto emitido se reutiliza sin MFA.** Y el ataque ni siquiera fue técnico: fue social, contra el humano que aprobaba el factor.

*Nota de tono:* aquí enfatizá que este caso **no** es "la MFA falló". Es "la MFA hizo lo que puede hacer, que es proteger un momento; el modelo la trata como si protegiera eternamente".

## 5.6 Token válido, autorización ausente — BOLA

**Qué es:** el atacante presenta su propio token —válido, auténtico, con MFA si quieren— y cambia el identificador del objeto en la URL: `/api/pedidos/1234` → `/api/pedidos/5678`. Y funciona.
**Primera aparición del término: OWASP API Security Top 10, edición 2019 (Api1: Broken Object Level Authorization); sigue en primera posición en la [edición 2023](https://owasp.org/API-Security/editions/2023/en/0x11-t10/).**
**Datos de campo:** se estima que **en torno al 40 % de los ataques a APIs** involucran BOLA ([Salt Security](https://salt.security/blog/api1-2023-broken-object-level-authentication)).
**Lección académica:** **es el mejor argumento posible de la charla.** Un bearer token —incluso un bearer token perfecto con DPoP y mTLS— **no autoriza objetos**. La autorización a nivel de objeto es una capa distinta, y es donde vive el fallo API1. Si tu charla tuviera un solo takeaway técnico, sería éste.

## 5.7 Implementación defectuosa de JWT — las clases, no los vendors

Como el objetivo es observar sin señalar, este punto se plantea como **clases de atque** con fuentes neutras:

- **`alg: none`** — el atacante reescribe el header para eliminar la firma; si el validador confía en el claim `alg`, acepta el token.
- **Confusión de algoritmos RS256 → HS256** — el validador, en vez de verificar con la clave pública, usa la clave pública como secreto HMAC, que está... publicada.
- **Inyección de `kid`** — el validador elige la clave de verificación según el `kid` que trae el token.
- **Otra clave de vida de `exp` ausente o con tolerancias gigantes.**

**Fuentes neutras:** [RFC 8725 (JWT BCP), febrero de 2020](https://www.rfc-editor.org/rfc/rfc8725) · [OWASP JWT Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html) · [PortSwigger Web Security Academy – JWT](https://portswigger.net/web-security/jwt).
**Lección académica:** estos fallos no son del token; son de **quien confía en el contenido que trae el token para decidir cómo verificarlo**. La regla: *la política de verificación sale de la configuración, no del mensaje.*

## 5.8 Síntesis del bloque

*Slide: los seis casos en una columna, y en la otra la misma respuesta.*

Todos distintos, y el patrón es idéntico: **el token se comportó como fue diseñado.** Facebook: se generó mal. Okta/Cloudflare: no se revocó. Codecov: vivía donde podía fugarse. Uber: se reutilizó después de la MFA. BOLA: se validó bien, pero la autorización era de otro nivel. JWT: se verificó con una política dictada por el mensaje.

*Frase de cierre del bloque:* *"La seguridad no está en el string. Está en cómo se emite, dónde se guarda, cuánto vive, cómo se revoca y qué se hace después de aceptarlo."*
