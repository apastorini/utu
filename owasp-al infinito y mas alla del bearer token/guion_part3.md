# BLOQUE 6 — Más allá del bearer: hacia dónde va todo (≈7 min)

## 6.1 Sender-constrained tokens: atar el token a su portador

Si el problema del bearer es que cualquiera que lo tenga puede usarlo, la solución lógica es **exigir algo más que la posesión**. A eso se le llama *token atado al emisor* (**sender-constrained token**), y hay dos caminos normalizados:

- **mTLS + token atado al certificado** — **RFC 8705, febrero de 2020**: el access token queda ligado al hash del certificado TLS del cliente. Robás el token, pero no podés presentarlo sin el par de claves del certificado.
- **DPoP (Demonstrating Proof of Possession)** — **RFC 9449, octubre de 2023**: el cliente genera una firma por request con su clave privada y un `jti`/`htm`/`htu`/`nonce` que impide replay. No necesita PKI: es DPoP sobre cualquier transporte.

Y la recomendación ya no es optativa: **[RFC 9700, "Best Current Practice for OAuth 2.0 Security", enero de 2025](https://www.rfc-editor.org/rfc/rfc9700)** —que reemplazó a [RFC 6819 (2013)](https://www.rfc-editor.org/rfc/rfc6819)— recomienda explícitamente usar tokens *sender-constrained* (DPoP o mTLS) donde sea posible, además de eliminar el *implicit grant*, eliminar el *password grant* y exigir PKCE en todos los flujos de código de autorización.

*Cita hablada sugerida:* "El IETF tardó trece años en pasarse de 'confiamos en el que lo tenga' a 'mostremos que somos nosotros'. Es una evolución, no una revolución —y eso está bien: los ecosistemas no se cambian de un día para el otro."

## 6.2 Los intentos previos: Token Binding

**Primera aparición: RFC 8471, 8472 y 8473, octubre de 2018.** El protocolo de Token Binding ataba el token al canal TLS. Los navegadores retiraron el soporte y el mecanismo no llegó a adopción práctica. Es una buena anécdota académica: **atar un token a su portador es un problema sociotécnico, no sólo criptográfico —depende de que toda la cadena (navegadores, servidores, proxies) lo soporte.**

## 6.3 OAuth 2.1 (borrador en curso)

El borrador de OAuth 2.1 consolida las lecciones: sin *implicit grant*, sin *password grant*, **sin bearer en query string**, PKCE obligatorio, rotación de refresh tokens. **Primera aparición: borrador del grupo de trabajo OAuth de la IETF, a partir de 2022.**

## 6.4 En el lado de la emisión: passkeys

Si la MFA protege el instante de la emisión, **la mejor mejora posible es fortalecer la emisión**: passkeys/WebAuthn (**W3C Recommendation, marzo de 2019**) como factor primario, alineado con **NIST SP 800-63-4 (julio de 2025)**.

## 6.5 Alrededor del token: el trabajo que la norma no hizo

La charla debe cerrar esta sección con la idea de que **el token es sólo una pieza**, y que la seguridad del sistema se construye alrededor:
- **Mínimo privilegio** (scopes y audiencia estricta).
- **Vida corta + rotación** (refresh rotation: RFC 6749 §10.4 → obligatoria en RFC 9700).
- **Revocación** (RFC 7009) y **introspección** (RFC 7662) cuando hay JWT.
- **Detección de anomalías**: ¿este token se usa desde dos países a la vez?
- **Mapa de riesgos**: [OWASP API Security Top 10, edición 2023](https://owasp.org/API-Security/editions/2023/en/0x11-t10/) — Api1 BOLA, Api2 Broken Authentication, Api3 BOPLA, Api6 Business Logic, Api8 Supply Chain.

*Frase de cierre del bloque:* *"Más allá del bearer no hay un reemplazo mágico: hay capas. El token se atada a su portador, se le acorta la vida, se le vigila el uso y —sobre todo— se le pone una autorización al lado que el token no puede dar por sí solo."*

---

# CIERRE — Tres mensajes (≈4 min)

*Slide: tres líneas, nada más.*

1. **El bearer token es finito: se emite, se roba, se reutiliza y debe morir.** Medí su vida, rotalo, revocalo. La ausencia de `exp` es una vulnerabilidad.
2. **La MFA protege el momento de la emisión, no los treinta días siguientes.** Diseñá para el robo de artefactos —fatiga, AiTM, infostealers—, no sólo para el robo de passwords. Y si tu invocador es un sistema, no busques un MFA: busca identidad de workload con vida corta.
3. **Autenticar es la puerta; autorizar es la cerradura.** Un token perfecto no impide BOLA, no impide mass assignment, no impide abuso de lógica de negocio.

**Frase final (cierra el título):**

> *"Al fin(ito) y más allá: el token se acaba, el riesgo no. Al fin y más allá del bearer token, la seguridad nunca estuvo en el string —estuvo siempre en el sistema."*

*Gracias. Quedo a las preguntas.*

---

# PREGUNTAS FRECUENTES PREVISTAS (guion de Q&A)

**"¿Sirve o no sirve el JWT?"**
Sirve, si su vida es corta, su `aud` es estricto y tenés introspección o rotación para lo que pase después. Es una herramienta de escalabilidad, no un sello de seguridad.

**"¿Entonces hay que volver a OAuth 1.0?"**
No: DPoP es esa idea, mejor integrada y sin canonicalización artesanal. La historia no se repite, se codifica.

**"¿Las cookies son peores que el bearer?"**
Son un bearer distinto: viajan automáticamente, lo cual las hace cómodas y propensas a CSRF, pero `HttpOnly` las protege de la lectura por XSS. Elegí según el contexto —navegador vs. cliente nativo vs. servidor a servidor—.

**"¿MFA para APIs de terceros?"**
La MFA ocurre en tu IdP; el tercero recibe un token con `acr`/`amr`. Si el tercero necesita más garantía, la respuesta es step-up o scope acotado, no "pedirle un SMS a su API".

**"¿API key o OAuth?"**
Si hay un humano detrás o un alcance que varía: OAuth. Si es identificación de un integrador fijo: API key, pero con rotación, revocación y al menos IP allowlist —y nunca en el cliente público.

---

# GLOSARIO

*Termino → definición → primera aparición.*

- **Access token** → Artefacto que se presenta ante la API de recursos para autorizar una petición; define alcance y vida. → **RFC 6749 §5, octubre 2012**; su uso bearer en **RFC 6750, octubre 2012**; perfil JWT en **RFC 9068, mayo 2021**.
- **AAL (Authenticator Assurance Levels)** → Niveles de garantía de un autenticador (AAL1/2/3) definidos por NIST. → **NIST SP 800-63-3, junio 2017**; vigente en **SP 800-63-4, julio 2025**.
- **`acr` (Authentication Context Class Reference)** → Claim que indica el contexto/nivel de autenticación usado. → **OpenID Connect Core 1.0, febrero 2014** (marco), con raíces en OpenID 2.0.
- **`alg`** → Header del JWT que declara el algoritmo de firma; su confianza ciega originó clases enteras de ataques. → **RFC 7519, mayo 2015**.
- **API key** → Identificador estático emitido a un sistema; identifica, no autentica; sin `exp` por defecto. → **Sin RFC: práctica de industria, mediados de los 2000 (access keys de AWS, 2006)**.
- **Authorization code** → Código de un solo uso, emitido en el front channel, intercambiado por tokens por canal trasero. → **RFC 6749 §4.1, octubre 2012**.
- **Bearer token** → Artefacto cuya posesión equivale a autorización: quien lo tiene, lo usa. → **RFC 6750, octubre 2012** (el término de "instrumento al portador" es anterior en derecho mercantil).
- **BOLA (Broken Object Level Authorization)** → Presentar un token válido para acceder a objetos de otro. → **OWASP API Security Top 10, edición 2019**; Api1 en **edición 2023**.
- **BOPLA (Broken Object Property Level Authorization / mass assignment)** → Setear propiedades de objeto que no deberían ser controlables por el cliente (p. ej. `rol`). → **OWASP API Security Top 10, edición 2021 (Api3)**.
- **Capability** → Facultad de acceso que se posee y se puede delegar, sin identificar al portador; el bearer token es una capability digital. → **Marco teórico: Saltzer & Schroeder, "The Protection of Information in Computer Systems", Proc. IEEE, 1975**.
- **Client credentials grant** → Flujo donde un sistema se autentica solo y obtiene un access token. → **RFC 6749 §4.4, octubre 2012**.
- **Cliente confidencial / público** → Confidencial guarda un secreto (servidor); público no puede (app móvil, SPA). → **RFC 6749 §2.1, octubre 2012**.
- **Confused deputy** → Problema en el que un programa con privilegios es engañado para actuar en nombre de un atacante; motivó el diseño de capabilities. → **Norm Hardy, ACM, 1989**.
- **Digest / Basic** → Esquemas de autenticación HTTP; Basic envía credenciales en Base64 por request. → **RFC 2617, junio 1999** (hoy **RFC 7616, agosto 2015**).
- **DPoP (Demonstrating Proof of Possession)** → Token atado a una clave privada del cliente; exige firma criptográfica por request. → **RFC 9449, octubre 2023**.
- **`exp` / `nbf` / `iat`** → Claims de expiración, "no antes de" y emisión. → **RFC 7519, mayo 2015**; `exp` obligatorio para access tokens en **RFC 9068, 2021**.
- **ID token** → JWT que identifica a la persona y cómo se autenticó; va a la app, no a la API de recursos. → **OpenID Connect Core 1.0, aprobado el 26 de febrero de 2014**.
- **Infostealer / pass-the-cookie** → Malware que extrae cookies y tokens del navegador para reutilizar sesiones. → **Familias comerciales desde mediados de los 2010; técnicas catalogadas por MITRE ATT&CK (T1539)**.
- **Introspección** → Endpoint que al validador le dice si un token opaco sigue vigente y qué claims tiene. → **RFC 7662, octubre 2015**.
- **`jti` (JWT ID)** → Identificador único del JWT, para anti-replay y revocación selectiva. → **RFC 7519, mayo 2015**.
- **`kid` (Key ID)** → Header que indica qué clave firmó el token. → **RFC 7517 (JWK), mayo 2015**.
- **JWT (JSON Web Token)** → Token autocontenido con claims en JSON, firmado/cifrado según JOSE. → **Primer borrador: 28 de diciembre de 2010; RFC 7519: mayo de 2015**.
- **JWS / JWE / JWK / JWA** → Firma, cifrado, claves y algoritmos de la familia JOSE. → **RFC 7515 / 7516 / 7517 / 7518, mayo de 2015**.
- **mTLS + token atado a certificado** → El token sólo es válido si el cliente presenta el certificado emparejado. → **RFC 8705, febrero 2020**.
- **MFA / factor de autenticación** → Exigir más de un tipo de factor (conocimiento, posesión, inherencia). → **NIST SP 800-63-1, 2011** (marco moderno); passkeys en **SP 800-63-4, julio 2025**.
- **MFA fatigue / push bombing (T1621)** → Bombardeo de pushes hasta que la víctima aprueba. → **MITRE ATT&CK T1621 (2021)**; casos públicos: Uber 2022.
- **`nonce`** → Valor aleatorio único anti-replay. → **RFC 6749 (`state`, 2012)** y **RFC 7636 (PKCE `code_verifier`, agosto 2015)**.
- **NHI (Non-Human Identity)** → Identidad de máquina/servicio; objeto de la "crisis" de secretos sin ciclo de vida. → **Término popularizado por reportes de industria desde ~2022-2023 (p. ej. GitGuardian 2025-2026)**.
- **OIDC (OpenID Connect)** → Capa de identidad sobre OAuth 2.0; añade ID token y UserInfo. → **OpenID Connect Core 1.0, final el 26 de febrero de 2014**.
- **OAuth 1.0** → Firma HMAC de cada request con secreto compartido. → **Especificación comunitaria, diciembre 2007; RFC 5849, abril 2010**.
- **OAuth 2.0** → Marco de autorización delegada; separa cliente, dueño de recurso y servidor de autorización. → **RFC 6749, octubre 2012**.
- **OAuth 2.1** → Consolidación del borrador: sin implicit, sin password grant, sin bearer en query, PKCE obligatorio. → **Borrador del IETF OAuth WG, desde 2022**.
- **Opaque token** → String no legible por el validador; requiere introspección. → **Modelo previo a OAuth; reglamentado en RFC 7662, octubre 2015**.
- **OTP / TOTP** → Código de un solo uso o basado en tiempo. → **HOTP: RFC 4226 (2005); TOTP: RFC 6238 (2011)**.
- **Passkey** → Par de claves sincronizable que reemplaza a la password; resistente a phishing. → **WebAuthn: Recomendación W3C, marzo 2019; passkeys: FIDO Alliance, 2022**.
- **PKCE** → Verificador/Desafío que impide que un código robado por un cliente público sea canjeado. → **RFC 7636, agosto 2015**; obligatorio en **RFC 9700, enero 2025**.
- **`prompt=login` / step-up** → Exigir re-autenticación o mayor nivel de garantía para una operación. → **OIDC Core, 2014**.
- **Refresh token** → Token largo que obtiene nuevos access tokens sin repetir consentimiento. → **RFC 6749 §§1.5 y 6, octubre 2012**; rotación sugerida en §10.4 y obligatoria para clientes públicos en **RFC 9700, 2025**.
- **Revocación de tokens** → Endpoint para invalidar access/refresh tokens antes de su expiración. → **RFC 7009, octubre 2013**.
- **RFC** → Documento de estándar de la IETF; "BCP" es Best Current Practice. → **IETF; RFC 2026 (1996) define el proceso**.
- **`scope`** → Alcance del permiso otorgado (qué operaciones, qué recursos). → **RFC 6749 §3.3, octubre 2012**.
- **Sender-constrained token** → Token atado a su portador (certificado o clave privada). → **RFC 8705 (2020)** y **RFC 9449 (2023)**; recomendado por **RFC 9700 (2025)**.
- **Session cookie** → Cookie que identifica una sesión en el servidor. → **Netscape, 1996; RFC 6265, abril 2011**.
- **SAML** → Aserción XML federada firmada. → **OASIS SAML 1.0, noviembre 2002; SAML 2.0, marzo 2005**.
- **Token Binding** → Protocolo para atar tokens al canal TLS; sin adopción práctica. → **RFC 8471-8473, octubre 2018**.
- **Token MAC (tipo `mac`)** → Tipo de token de OAuth 2.0 que firmaba cada request; abandonado. → **Borrador `HTTP Authentication: MAC Access Authentication`, febrero 2012 (referencia de RFC 6749); nunca llegó a RFC**.
- **XSS / CSRF** → Inyección de script en página / forzamiento de petición autenticada. Motivan el dilema cookie vs. cabecera. → **Términos de industria popularizados ~2000-2005; mitigaciones: SameSite (RFC 6265bis, 2016-)**.

---

# BIBLIOGRAFÍA

## Normas IETF (fuente primaria)
- [RFC 2617 — HTTP Basic/Digest (1999)](https://www.rfc-editor.org/rfc/rfc2617) · [RFC 7616 (2015)](https://www.rfc-editor.org/rfc/rfc7616)
- [RFC 6265 — HTTP State Management Mechanism / cookies (2011)](https://www.rfc-editor.org/rfc/rfc6265)
- [RFC 5849 — The OAuth 1.0 Protocol (2010)](https://www.rfc-editor.org/rfc/rfc5849)
- [RFC 6749 — The OAuth 2.0 Authorization Framework (oct 2012)](https://www.rfc-editor.org/rfc/rfc6749)
- [RFC 6750 — Bearer Token Usage (oct 2012)](https://www.rfc-editor.org/rfc/rfc6750)
- [RFC 6819 — OAuth 2.0 Threat Model (2013, reemplazado por RFC 9700)](https://www.rfc-editor.org/rfc/rfc6819)
- [RFC 7009 — Token Revocation (2013)](https://www.rfc-editor.org/rfc/rfc7009)
- [RFC 7636 — PKCE (ago 2015)](https://www.rfc-editor.org/rfc/rfc7636)
- [RFC 7515/7516/7517/7518/7519 — JOSE + JWT (may 2015)](https://www.rfc-editor.org/rfc/rfc7519)
- [RFC 7522 — SAML 2.0 Bearer Assertion Profiles for OAuth 2.0 (2015)](https://www.rfc-editor.org/rfc/rfc7522) · [RFC 7523 — JWT para client auth (2015)](https://www.rfc-editor.org/rfc/rfc7523)
- [RFC 7662 — Token Introspection (oct 2015)](https://www.rfc-editor.org/rfc/rfc7662)
- [RFC 8176 — Authentication Method Reference (ago 2017)](https://www.rfc-editor.org/rfc/rfc8176)
- [RFC 8252 — OAuth 2.0 for Native Apps (2017)](https://www.rfc-editor.org/rfc/rfc8252)
- [RFC 8471/8472/8473 — Token Binding (2018)](https://www.rfc-editor.org/rfc/rfc8471)
- [RFC 8705 — mTLS y token atado a certificado (feb 2020)](https://www.rfc-editor.org/rfc/rfc8705)
- [RFC 8725 — JWT Best Current Practices (feb 2020)](https://www.rfc-editor.org/rfc/rfc8725)
- [RFC 9068 — JWT Profile for OAuth 2.0 Access Tokens (may 2021)](https://www.rfc-editor.org/rfc/rfc9068)
- [RFC 9449 — DPoP (oct 2023)](https://www.rfc-editor.org/rfc/rfc9449)
- [RFC 9700 — Best Current Practice for OAuth 2.0 Security (ene 2025)](https://www.rfc-editor.org/rfc/rfc9700)

## Identidad, autenticación y perfiles
- [OpenID Connect Core 1.0](https://openid.net/specs/openid-connect-core-1_0.html) — final el 26 de febrero de 2014 ([anuncio](https://openid.net/the-openid-foundation-launches-the-openid-connect-standard/))
- [NIST SP 800-63-4 — Digital Identity Guidelines (jul 2025)](https://pages.nist.gov/800-63-4/) · [SP 800-63B-4 (autenticación)](https://pages.nist.gov/800-63-4/sp800-63b.html) · [página CSRC](https://csrc.nist.gov/pubs/sp/800/63/4/final)
- [AWS Signature Version 4](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_sigv.html) · [SPIFFE](https://spiffe.io/docs/latest/spiffe-about/overview/)

## OWASP
- [OWASP API Security Top 10 — edición 2023](https://owasp.org/API-Security/editions/2023/en/0x11-t10/) · [proyecto OWASP API Security](https://owasp.org/www-project-api-security/)
- [OWASP JWT Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html) · [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html) · [OWASP REST Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html)

## Incidentes y análisis (fuentes primarias)
- [Meta / Facebook "View As" — actualización oficial (2018)](https://about.fb.com/news/2018/09/security-update/) · [KrebsOnSecurity](https://krebsonsecurity.com/2018/09/facebook-security-bug-affects-90m-users/)
- [Cloudflare — sesión de Okta comprometida (2023)](https://blog.cloudflare.com/how-cloudflare-mitigated-yet-another-okta-compromise/) · [relacionado: Cloudflare y el incidente de Okta de enero de 2022](https://blog.cloudflare.com/cloudflare-investigation-of-the-january-2022-okta-compromise/)
- [Codecov — actualización oficial del incidente (2021)](https://about.codecov.io/security-update/) · [Rapid7](https://www.rapid7.com/blog/post/2021/04/16/codecov-discloses-supply-chain-compromise/)
- [NYT — Uber (2022)](https://www.nytimes.com/2022/09/15/technology/uber-hacking-breach.html) · [UpGuard — análisis](https://www.upguard.com/blog/what-caused-the-uber-data-breach)
- [GitGuardian — State of Secrets Sprawl 2026](https://www.gitguardian.com/state-of-secrets-sprawl-report-2026) · [resumen en blog](https://blog.gitguardian.com/the-state-of-secrets-sprawl-2026/)
- [Salt Security — Api1 BOLA](https://salt.security/blog/api1-2023-broken-object-level-authentication)

## Recursos didácticos
- [MITRE ATT&CK T1621 — MFA Request Generation](https://attack.mitre.org/techniques/T1621/)
- [PortSwigger Web Security Academy — JWT](https://portswigger.net/web-security/jwt)
- [jwt.io — introducción a JWT](https://jwt.io/introduction)

---

# ANEXO A — Ejemplo uruguayo: observación controlada (opcional)

*Objetivo: mostrar, sin invadir ningún sistema, que un token bearer real del ecosistema uruguayo es visible, extraíble de tu propio navegador y reutilizable en principio por cualquiera que lo tenga. La demostración se apoya en documentación oficial —cero riesgo— y, si vos querés, en una observación de tu propia sesión.*

## A.1 La evidencia documental (cero pruebas, cero riesgo)

**ID Uruguay**, el proveedor de identidad del Estado uruguayo que gestiona AGESIC, **documenta públicamente que emite tokens bearer**. Su documentación técnica de integración con OpenID Connect muestra el *token endpoint* `/oidc/v1/token` y la respuesta con **`token_type` = "Bearer"**, además de ejemplos de llamada a UserInfo con **`Authorization: Bearer <token>`** y la aclaración de que el **ID token es un JWT**.

- [ID Uruguay: integración con OpenID Connect (gub.uy)](https://www.gub.uy/agencia-gobierno-electronico-sociedad-informacion-conocimiento/comunicacion/publicaciones/documentacion-tecnica-id-uruguay/documentacion-tecnica-id-uruguay/id-0)
- [AGESIC — guía "Desarrollo seguro" (PDF, gub.uy), con ejemplos `Authorization: Bearer`](https://www.gub.uy/agencia-gobierno-electronico-sociedad-informacion-conocimiento/sites/agencia-gobierno-electronico-sociedad-informacion-conocimiento/files/Desarrollo%20seguro.pdf)

**Guion hablado sugerido (1 minuto):** *"Esto no es teórico. El Estado uruguayo, a través de ID Uruguay, emite tokens bearer con OpenID Connect — está documentado públicamente. Un token de este tipo es un string que viaja en una cabecera HTTP: cualquiera en posesión de ese string, exactamente igual que con el billete al portador, puede usarlo mientras esté vigente. Esa es toda la tesis de esta charla."*

## A.2 La observación controlada (sólo con tu propia cuenta, sólo lectura)

Si querés mostrar en vivo el token saliendo del navegador, este es el protocolo **ético y controlado** que recomendamos. No hay escaneo, no hay fuzzing, no hay peticiones automatizadas, no hay cuentas ajenas:

1. **Usá exclusivamente una cuenta propia** y un flujo de login normal (vía ID Uruguay o cualquier sitio donde seas usuario).
2. **Abrí DevTools → Network**, filtrá por `token` o `authorization`, y localizá la respuesta del *token endpoint* o la petición que lleve la cabecera `Authorization: Bearer ...`.
3. **Copiá SOLO tu propio token** y descifralo localmente (jwt.io es cliente: el token no viaja a ningún servidor, se decodifica en tu navegador) para mostrar los claims: `iss`, `aud`, `exp`, `amr`, `acr`.
4. **Enmascará el token en la pantalla** —mostrá los primeros caracteres y el resto tapado—. Es una charla, no una filtración.
5. **No repliques el token contra ningún endpoint.** El punto de la charla es que *podrías* —basta con enunciarlo—; hacerlo agrega riesgo y no agrega información.
6. **Al terminar, cerrá sesión.** Eso invalida la sesión y, en la mayoría de las implementaciones, hace que el artefacto deje de ser útil.
7. Si el sistema no es tuyo y no tenés autorización, **no hagas ninguna prueba**: alcanza con la documentación de A.1.

**Frase de cierre del anexo:** *"No tocamos ningún sistema: miramos un billete al portador en nuestra propia billetera. Y aun así, vimos exactamente por qué esta charla se llama como se llama."*

## A.3 Alternativa si se quiere demostrar reutilización

Si algún día querés mostrar *reutilización* sin tocar ningún sistema de terceros, la opción correcta es un objetivo **diseñado** para eso: una API deliberadamente vulnerable propia (proyectos tipo OWASP crAPI o similar) corriendo en tu máquina, o un entorno de staging de tu organización. Nunca un sistema productivo de terceros.

---

# ANEXO B — Compresión a 30 minutos

| Bloque | Extendido | A 30 min | Qué se recorta |
|---|---|---|---|
| Apertura | 4 min | 2 min | — |
| 1. Historia | 12 min | 6 min | Sólo Basic/cookies en una línea cada uno, OAuth 1.0 como antítesis, el detalle del tipo `mac` abandonado y la cita de RFC 6749 §10.3. Quitar la nota académica de capabilities. |
| 2. Familia de tokens | 14 min | 7 min | Mantener el mapa de los 4 tokens; recortar opaque vs JWT a "la regla de oro" y fusionar API keys con el caso 5.4. |
| 3. Anatomía | 8 min | 3 min | Quitar la checklist completa: quedarse con "el algoritmo no viene del token" y el transporte (query hoy prohibido por RFC 9700). |
| 4. MFA persona/sistema | 14 min | 10 min | **No se recorta la tesis ni la tabla comparativa.** Acortar la jerarquía de factores y los tres modos de fallo a una sola slide. |
| 5. Ataques | 12 min | 5 min | Quedarse con Facebook 2018 + Codecov 2021 + BOLA como síntesis. Uber y Okta/Cloudflare se mencionan de pasaje en el bloque 4. |
| 6. Futuro | 7 min | 3 min | Sólo DPoP/mTLS + RFC 9700. |
| Cierre | 4 min | 2 min | — |
| Preguntas | — | 2 min | — |
| **Total** | **~75 min** | **~30 min** | |

---

# ANEXO C — Preguntas frecuentes del público (respuestas breves)

*Preparación para el turno de preguntas. La versión extendida, con fuentes, está en la sección 11 de la clase completa (`clase_completa.docx`, "Preguntas frecuentes").*

- **¿Base64 es cifrado?** No: es una **codificación** sin clave. El cifrado real de JOSE es **JWE**. Un **JWT común es JWS: firmado, no sellado** (se lee).
- **¿Todos los bearer usan base64url?** No. Base64url es propio de **JWT/JOSE**; un **token opaco** son bytes aleatorios.
- **¿Qué es HMAC-SHA1?** Un **MAC simétrico** (clave + hash) del RFC 2104. Lo usaba **OAuth 1.0** para firmar cada request en el `nonce`. Deprecado a favor de SHA-256 (**HS256**).
- **¿Qué son `amr` y `acr`?** `amr` (RFC 8176) = **con qué métodos** se autenticó; `acr` = **con qué nivel/garantía**. La API solo sabe que hubo MFA si el emisor los pone y el validador los revisa.
- **¿Qué es JOSE?** La familia: **JWS** (firma), **JWE** (cifrado), **JWK** (claves), **JWA** (algoritmos), **JWT** (token).
- **¿Qué fue primero: la cookie o Digest?** **La cookie** (Netscape, 1994/1996). **Digest** se estandarizó después (RFC 2069 en 1997; RFC 2617 en 1999).
- **¿Bearer es exclusivo de OAuth?** No. El esquema `Bearer` es del **marco HTTP** y lo usa cualquier API. RFC 6749 y RFC 6750 son compañeros pero distintos; y OAuth puede emitir tokens **sender-constrained** (no bearer puro).
- **¿Todos los flujos de OAuth 2 usan token?** Sí, todos emiten **access token**. Implicit y Password (ROPC) están **retirados** por RFC 9700 (2025).
- **¿Qué es un token opaco?** Un string sin claims legibles; se valida por **introspección** (RFC 7662) contra el servidor de autorización.
- **¿Qué es `aud`?** La **audiencia**: para quién es el token. Validarla estricta es lo que responde al §10.3 de RFC 6749.
- **¿Qué es prueba de posesión (PoP)?** Demostrar que se tiene la **clave privada** por request: **mTLS** atado al certificado (RFC 8705) o **DPoP** (RFC 9449). Robar el token no alcanza.
- **¿mTLS o DPoP?** mTLS da identidad fuerte de cliente pero requiere **PKI**; DPoP no necesita PKI y firma cada request con `jti`/`htm`/`htu`.
- **¿Por qué una passkey resiste el phishing?** El `origin` va **atado criptográficamente** a la firma; el autenticador no firma para el sitio falso. El OTP sí se phishea en vivo (AiTM); SMS es el más débil.
- **¿Qué es "JWT mal validado"?** El token es correcto, el validador no: `alg:none`, confusión HS/RS, inyección de `kid`, no validar `iss`/`aud`/`exp`. La política sale de la **config**, no del mensaje (RFC 8725).
- **¿Qué son BOLA, BFLA y BOPLA?** A nivel **objeto**, **función** y **propiedad**, respectivamente (OWASP API1, API5, API3). Autenticar ≠ autorizar.
- **¿Y las versiones de HTTP?** No crean el problema del bearer, pero cambian la superficie: compresión de cabeceras (HPACK/QPACK), inspección de binario, smuggling, terminación TLS. El token en **query** lo prohíbe RFC 9700.
- **El caso de Okta, ¿fue 2022?** El del *session token* de un ticket de soporte fue **octubre de 2023**. El de **enero de 2022** (proveedor de soporte) **no** impactó a Cloudflare, que usaba llaves de hardware.
