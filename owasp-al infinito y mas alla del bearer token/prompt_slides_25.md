# Prompt v2 — Generar 25 diapositivas con guion hablado (charla del bearer token)

Esta es la **segunda versión** del prompt de slides. Cambios pedidos:

- **25 diapositivas** (versión extendida, ~50-60 min).
- **Primero** se explica **qué es un bearer token** (2 slides).
- Luego **una sola slide de conceptos de API en círculos** (gateway, MFA, IAM, rate limiting, etc.).
- **La historia ocupa como máximo 3 slides** (reparto del pasado del bearer token).
- **De ahí en adelante, todo es "del bearer token hacia adelante"** (familia de tokens, JWT, MFA, ataques, DPoP, cierre).
- **Cada slide trae el texto que hay que decir** (el guion hablado), listo para leer o pegar en las notas del ponente.

Copiá el bloque de abajo y pegalo en la IA generadora de slides (Gamma, Tome, Copilot, Gemini, etc.). Cada slide ya incluye su guion, así que el generador solo tiene que diagramar el visual y volcar el texto en "Notas del ponente".

---

````
ROL
Actuá como diseñador de presentaciones técnicas y experto en seguridad de APIs REST.

CONTEXTO
Prepará 25 slides en ESPAÑOL para una charla de ~50-60 minutos titulada
"Al fin(ito) y más allá del bearer token" (juego de palabras con "al infinito
y más allá"). Audiencia: público técnico medio (devs, arquitectos, equipos de
seguridad). No hay demos: es una charla narrada, con tono académico y
OBSERVACIONAL — no se critica a ninguna organización ni persona; los incidentes
se citan como divulgaciones públicas y se analizan como fallas de modelo, no de
equipos.

RESTRICCIONES CLAVE DEL ORDEN (respetar exactamente)
- El ORDEN manda: primero ¿qué es un bearer token? (slides 2-3), después UNA
  slide de conceptos de API en círculos (slide 4), después la HISTORIA en un
  MÁXIMO DE 3 SLIDES (slides 5-7), y de ahí en adelante todo es "del bearer
  token hacia adelante" (slides 8-25).
- La historia NUNCA puede superar 3 slides. Si hay que recortar, se recorta ahí.
- La slide de conceptos debe mostrar TODOS los términos como CÍRCULOS
  (diagrama de anillos/órbita alrededor del token), no como lista.

TONO Y ESTÉTICA
- Un solo mensaje por slide, máximo 5 bullets cortos (máx. 12 palabras c/u).
- Títulos que cuenten una idea, no un tema (ej: "La MFA protege un instante,
  no 30 días" en vez de "MFA en APIs").
- Cada dato o cita lleva la fuente en letra chica al pie (RFC, fecha, URL).
- Estilo visual: limpio, fondo oscuro o neutro, un color de acento, tipografía
  sans-serif, íconos mínimos, diagramas de flujo simples. Nada de cliparts ni
  párrafos pegados de la norma.
- Cada slide incluye "GUION (texto para decir)": es el texto que el ponente lee.
  Debe ir tal cual en las "Notas del ponente" (2-4 frases por slide).

ESTRUCTURA EXACTA DE LOS 25 SLIDES (con el guion de cada uno)

1. PORTADA
   Título: "Al fin(ito) y más allá del bearer token".
   Subtítulo: "Un billete al portador llamado token".
   Visual: billete de banco antiguo al portador junto a un string largo.
   GUION: "Buenas tardes. El título juega con 'al infinito y más allá', y no
   es casual: vamos a hablar de algo que parece no acabarse nunca —un token
   que se emite una vez y parece vivir para siempre— y de lo que hay más allá
   de él, que es donde de verdad vive la seguridad. Vamos a ver qué es un
   bearer token, qué conceptos aparecen alrededor de una API y, sobre todo,
   qué pasa cuando la autenticación multifactor tiene que convivir con un
   artefacto que se puede copiar con dos teclas."
   Fuente al pie: —

2. ¿QUÉ ES UN BEARER TOKEN?
   Título: "Un token es un billete al portador: quien lo tiene, entra".
   Bullets: posesión = autorización; "bearer" viene del derecho mercantil;
   no identifica al portador; RFC 6750 (oct. 2012).
   Visual: un billete al portador y la frase "quien lo tiene, lo usa".
   GUION: "Un bearer token es un artefacto de seguridad cuya posesión equivale
   a autorización. La palabra 'bearer' viene del derecho mercantil: un
   instrumento al portador da derecho a quien lo tiene en la mano, sin
   acreditar identidad. Si perdés un billete, quien lo levanta lo gasta. Si se
   filtra un token, quien lo tiene lo usa. No es que el token esté mal
   hecho: está hecho así a propósito."
   Fuente al pie: RFC 6750, "Bearer Token Usage", octubre 2012.

3. LA PROPIEDAD QUE LO DEFINE (Y SU RIESGO)
   Título: "La norma lo admitió primero: no puedo saber a quién le emití esto".
   Bullets: el recurso acepta el token sin verificar al portador; la firma
   prueba el emisor, no el destinatario; el riesgo es de diseño, no de
   implementación.
   Visual: cita textual en grande + fecha.
   GUION: "Esto no lo descubrimos después: está en la propia norma. RFC 6749,
   sección 10.3, dice, textualmente, que la especificación no provee ningún
   método para que el servidor de recursos se asegure de que un access token
   presentado por un cliente le fue emitido realmente a ese cliente. En
   criollo: desde 2012 el estándar dice que un servidor no puede distinguir
   entre el cliente legítimo y quien le robó el token. Por eso el bearer no
   falló: cumplió exactamente lo que prometió."
   Fuente al pie: RFC 6749 §10.3, octubre 2012.

4. EL MAPA DE CONCEPTOS DE UNA API (SLIDE DE CÍRCULOS)
   Título: "Alrededor del token hay un sistema entero".
   Visual obligatorio: diagrama de CÍRCULOS/ANILLOS concéntricos con el token
   en el centro y cada concepto en su propio círculo, conectados por líneas.
   Círculos a incluir: API Gateway · IAM · MFA · Rate Limiting · WAF ·
   API Keys · OAuth 2.0 / OIDC · JWT · Scopes · RBAC / ABAC · Secret Manager ·
   mTLS / DPoP · Observabilidad y auditoría · Zero Trust · Autorización a
   nivel de objeto (BOLA).
   GUION: "Antes de seguir con los tokens, ubiquémonos: una API no es solo el
   token. Alrededor hay un gateway que enruta y aplica cuotas; un IAM que
   administra identidades; la MFA que protege el login; el rate limiting que
   frena la fuerza bruta; un WAF que filtra ataques; API keys para
   integradores; OAuth y OIDC como marco; el JWT como formato; los scopes y
   modelos como RBAC o ABAC para decidir permisos; un secret manager para
   guardar claves; mTLS y DPoP para atar el token a su portador;
   observabilidad y auditoría para ver qué pasa; y Zero Trust como filosofía.
   El token es una pieza del sistema: si lo miramos aislado, no entendemos
   nada."
   Fuente al pie: OWASP API Security Top 10 (2023).

5. HISTORIA (1/3) — ANTES DEL BEARER: BASIC Y COOKIES
   Título: "Primero mandábamos la contraseña; después, una cookie".
   Bullets: Basic manda usuario:contraseña en Base64 por request; Digest
   mejora el hash, no el modelo; la cookie guarda estado en el servidor.
   Visual: timeline horizontal, primeros dos hitos.
   GUION: "Todo empieza con HTTP sin estado. La primera solución fue mandar
   usuario y contraseña en cada petición: Basic, dentro del marco de
   autenticación de HTTP estandarizado en el RFC 2617, de junio de 1999.
   Basic codifica en Base64 —que no es cifrado— y Digest manda un hash con un
   nonce. Pero las credenciales siguen viajando en cada request. El segundo
   intento fue no mandar credenciales, sino un identificador de sesión: la
   cookie, de Netscape (1996), que de hecho es anterior a la estandarización
   de Digest, y que recién se estandarizó en el RFC 6265, en abril de 2011.
   El estado queda en el servidor: seguro para la web tradicional, incómodo
   para APIs que tienen que delegar."
   Fuente al pie: RFC 2617 (1999) / RFC 7616 (2015); RFC 6265 (2011).

6. HISTORIA (2/3) — SAML Y OAUTH 1.0
   Título: "Lo firmado era más seguro; lo simple ganó igual".
   Bullets: SAML 2.0 (OASIS, 2005) y WS-Security (2004) firmaban aserciones
   XML; OAuth 1.0 (RFC 5849, 2010) firmaba cada request con HMAC-SHA1; más
   seguro, más pesado.
   Visual: dos columnas "firmar" vs "coste de integración".
   GUION: "En el mundo enterprise, SAML 2.0, estándar OASIS de marzo de 2005,
   y WS-Security de 2004 usaban aserciones XML firmadas: eran, en rigor, más
   seguros que un bearer. El problema no era la seguridad, era el peso.
   Después llegó OAuth 1.0, especificación comunitaria de diciembre de 2007 y
   RFC 5849 en abril de 2010: no mandaba ningún token copiable, firmaba cada
   request con HMAC-SHA1. Robar una petición no servía. Pero canonicalizar
   parámetros y compartir secretos entre cada par de servicios era una
   pesadilla, sobre todo en móviles."
   Fuente al pie: SAML 2.0 (2005); WS-Security (2004); RFC 5849 (2010).

7. HISTORIA (3/3) — EL PUNTO DE GIRO: BEARER VS. MAC
   Título: "OAuth 2.0 nació con dos tipos de token; el mundo eligió uno".
   Bullets: RFC 6749 (oct. 2012) definía bearer y mac; el tipo mac firmaba
   cada request; el borrador MAC (feb. 2012) se abandonó; ganó la
   simplicidad.
   Visual: dos columnas — "Firmar cada request (mac)" vs "Mandar un string
   (bearer)"; una queda tachada.
   GUION: "Este es el dato histórico que casi nadie cuenta: OAuth 2.0 no nació
   siendo solo bearer. RFC 6749, de octubre de 2012, definía dos tipos: bearer
   y mac. El tipo mac firmaba componentes de cada request, igual que OAuth 1.0
   o que DPoP después. Pero ese borrador nunca llegó a RFC: se abandonó. El
   ecosistema eligió la simplicidad, y con él llegó RFC 6750. La firma por
   request era técnicamente superior; el costo de implementación decidió la
   historia."
   Fuente al pie: RFC 6749 §7.1 (2012); borrador MAC, febrero 2012.

8. LA FAMILIA DE TOKENS: CUÁNTOS SON Y DE DÓNDE SALEN
   Título: "No hay 'un token': hay una familia con roles distintos".
   Bullets: authorization code (un solo uso) → access token (corto) →
   refresh token (largo, rotación) + ID token (identifica, no autoriza).
   Visual: diagrama de flujo Authorization Code Grant con los cuatro tokens
   numerados. Slide clave de la charla.
   GUION: "Un error común es hablar de 'el token' como si fuera uno solo. En
   un flujo moderno nacen hasta cuatro artefactos distintos. El authorization
   code es un cupón de un solo uso que viaja por el navegador. El access token
   es el que se presenta ante la API: vida corta, alcance limitado. El refresh
   token es de vida larga y solo sirve contra el endpoint de token, nunca
   contra la API. Y el ID token, de OpenID Connect, dice quién es la persona y
   cómo se autenticó: no sirve para acceder a recursos. Confundir estos roles
   es el origen de la mayoría de las fallas."
   Fuente al pie: RFC 6749 §4.1 / §5 (2012); OIDC Core, 26 de febrero de 2014.

9. TABLA DE ROLES Y VIDAS
   Título: "Cada token tiene su destinatario y su vida".
   Bullets: código (front channel, un uso) · access (la API, corto) · refresh
   (el endpoint de token, largo, rota) · ID (la app, identifica).
   Visual: tabla token | para qué | vida | dónde viaja | primera aparición.
   Regla destacada: el refresh token jamás viaja a la API de recursos.
   GUION: "Pongámoslo en una tabla. El código de autorización es de un solo
   uso y viaja por el navegador. El access token viaja en cada request a la
   API y debe vivir minutos u horas. El refresh token vive semanas o meses,
   pero solo se presenta al endpoint de token. El ID token va a la aplicación
   cliente, no a la API. Regla para escribir en grande: el refresh token jamás
   viaja a la API de recursos, y el access token jamás se usa para refrescar.
   Son mundos distintos: recursos contra emisión."
   Fuente al pie: RFC 6749 §§1.5, 4.1, 5, 6 (2012); RFC 7009 (2013).

10. ANATOMÍA DE UN JWT
    Título: "Está firmado, no sellado: el payload lo lee cualquiera".
    Bullets: header.payload.signature en base64url; base64 no es cifrado; el
    algoritmo NO se toma del token (RFC 8725).
    Visual: JWT anotado en tres colores (header, payload, firma).
    GUION: "Un JWT son tres partes separadas por puntos, cada una en base64url.
    Cuidado con el error clásico: base64 no es cifrado, cualquiera lee el
    payload. Es como una credencial plastificada: firmada, no sellada; si
    necesitás confidencialidad, va JWE. El header lleva el algoritmo, y ahí
    nace una familia entera de ataques: si el receptor decide cómo verificar
    según lo que dice el token, un atacante elige el algoritmo. La regla, de
    RFC 8725 y de OWASP: la política de verificación sale de la configuración,
    nunca del mensaje."
    Fuente al pie: RFC 7519 (2015); RFC 8725 (feb. 2020).

11. LOS CLAIMS QUE IMPORTAN
    Título: "Un JWT bien validado responde cuatro preguntas".
    Bullets: ¿quién lo emitió? (iss) · ¿es para mí? (aud) · ¿está vigente?
    (exp/nbf) · ¿tiene permiso? (scope); amr/acr dicen cómo se autenticó.
    Visual: las cuatro preguntas con el claim entre paréntesis.
    GUION: "Los claims son el contenido. iss dice quién lo emitió; hay que
    validarlo contra emisores confiables. aud dice para quién es: es el claim
    que responde a la pregunta de la norma, porque si validás aud
    estrictamente, un token robado emitido para otra app no te sirve. exp y
    nbf dicen si está vigente. scope dice qué puede hacer. Y amr y acr, de RFC
    8176, dicen cómo se autenticó: son el puente entre 'pasó la MFA' y 'el
    token lo sabe'."
    Fuente al pie: RFC 7519 (2015); RFC 8176 (2017); RFC 9068 (2021).

12. DÓNDE VIAJA EL TOKEN (Y DÓNDE NO)
    Título: "Trece años tardamos en prohibir el token en la URL".
    Bullets: RFC 6750 permitía cabecera, cuerpo y query; RFC 9700 (enero
    2025) prohíbe tokens en URIs; cabecera vs cookie: XSS vs CSRF.
    Visual: tres transportes, el de query tachado con fecha.
    GUION: "En 2012, RFC 6750 aceptaba tres transportes: cabecera, cuerpo y
    parámetro de query. Trece años después, RFC 9700, las mejores prácticas de
    enero de 2025, prohíbe transportar access tokens en URIs. ¿Por qué el
    cambio? Porque trece años de logs, de cabeceras Referer, de historiales y
    de CDN nos enseñaron dónde terminan los tokens que van en una URL. La
    cabecera no la manda el navegador sola: es inmune a CSRF, pero hay que
    guardarla bien. La cookie protege de XSS con HttpOnly, pero exige mitigar
    CSRF."
    Fuente al pie: RFC 6750 §2 (2012); RFC 9700 (enero 2025).

13. TESIS CENTRAL: LA MFA NO ESTÁ EN LA API
    Título: "La MFA protege un instante; el token vive 30 días".
    Bullets: el flujo real es password → MFA → emisión → token (30 días) →
    API; la API no sabe si hubo MFA salvo que se lo digan los claims.
    Visual: timeline Password → MFA → Emisión → 30 días de token → API.
    GUION: "Esta es la idea que justifica el título. La autenticación
    multifactor no ocurre en la API: ocurre en el momento de la emisión.
    Después de la MFA, todo lo que la API recibe es un string. El flujo real
    es: contraseña, MFA en el servidor de autenticación, emisión de tokens y,
    al final, un access token. La API no sabe, y no puede saber, si hubo MFA;
    solo lo sabe si el emisor puso amr y acr en el token y el validador los
    revisa. La MFA protege la generación del artefacto, no su posesión
    posterior."
    Fuente al pie: NIST SP 800-63-4 (jul. 2025); OIDC Core (2014).

14. MFA DEL LADO PERSONA: NO TODAS SON IGUALES
    Título: "Passkeys son el único factor que sobrevive al phishing".
    Bullets: NIST AAL1-AAL3; WebAuthn/passkeys (W3C, 2019) resisten
    phishing; TOTP se phishea en tiempo real; SMS es el más débil; step-up con
    acr/amr.
    Visual: escala de métodos de mayor a menor garantía.
    GUION: "NIST, en su guía de identidad vigente de julio de 2025, dice algo
    clave: no todos los autenticadores dan la misma garantía, y el nivel debe
    ligarse al riesgo. AAL2 exige dos factores de tipos distintos; AAL3 exige
    prueba criptográfica de posesión de una clave en hardware. WebAuthn y las
    passkeys, recomendación W3C de 2019, resisten el phishing por diseño: el
    desafío está atado al origen. Un OTP se puede phishear en tiempo real, y
    el SMS es el más débil. Y el step-up, con acr y amr, permite pedir más
    garantía solo para la operación sensible."
    Fuente al pie: NIST SP 800-63-4 (jul. 2025); WebAuthn (2019); RFC 8176 (2017).

15. LOS TRES MODOS EN QUE LA MFA NO SALVA AL BEARER
    Título: "La MFA cubre el login, no lo que pasa después".
    Bullets: fatiga de push (MITRE T1621); phishing AiTM roba la sesión ya
    autenticada; infostealers y pass-the-cookie roban el artefacto.
    Visual: tres tarjetas con el ataque y el momento en que ocurre.
    GUION: "Hay tres familias de ataque que la MFA no cubre, porque atacan
    después de la emisión. Uno: fatiga de MFA, o push bombing —MITRE lo
    cataloga como T1621—: el atacante ya tiene la contraseña y dispara pushes
    hasta que la víctima aprueba. Dos: phishing adversary-in-the-middle: ya no
    roba la contraseña, intercepta la sesión completa que resultó de la MFA.
    Tres: infostealers, malware que extrae cookies y tokens del navegador y
    los reutiliza en otro equipo; se llama pass-the-cookie. En los tres, la
    MFA hizo su trabajo; el problema es que el artefacto se reutiliza."
    Fuente al pie: MITRE ATT&CK T1621; T1539; casos públicos 2022.

16. MFA DEL LADO SISTEMA: NO HAY HUMANO QUE FACTORIZAR
    Título: "A una máquina no le podés pedir un segundo factor".
    Bullets: el invocador es microservicio, CI o IoT; no hay usuario; la
    pregunta es qué workload habla y con qué credencial de vida corta;
    mecanismos: client credentials, private_key_jwt, mTLS, DPoP.
    Visual: un engranaje/contenedor en lugar de una persona.
    GUION: "Ahora el otro lado, donde está la mayoría del tráfico real.
    Cuando la API la invoca un microservicio, un job de CI o un dispositivo,
    la pregunta '¿quién es el usuario?' no tiene respuesta, porque no hay
    usuario. Y no hay MFA aplicable: no hay segundo factor que mostrar. La
    pregunta correcta es: ¿qué workload es este, con qué credencial de ciclo
    de vida corto y bajo qué contexto habla? El equivalente funcional del MFA
    para un sistema no es un segundo factor puntual: es una identidad de
    workload fuerte, verificable y de vida corta."
    Fuente al pie: RFC 6749 §4.4 (2012); RFC 7523 (2015); RFC 8705 (2020).

17. PERSONA VS. SISTEMA (TABLA COMPARATIVA)
    Título: "Dos preguntas distintas, no una sola mal aplicada".
    Bullets: persona: ¿quién pasó la MFA? · sistema: ¿qué credencial de vida
    corta me habla? · el fallo típico de cada lado.
    Visual: tabla de 5-6 filas: qué se prueba, segundo factor, artefacto, vida
    típica, fallo típico, revocación.
    GUION: "Pongamos las dos columnas juntas. Para la persona probamos que un
    humano se autenticó ante un proveedor de identidad; el segundo factor es
    una passkey, un OTP o un push; el artefacto es una sesión más un access
    token corto; y el fallo típico es fatiga, AiTM o robo de sesión. Para el
    sistema probamos que un workload concreto pidió el token; no hay segundo
    factor; el artefacto es un token corto o una credencial efímera; y el
    fallo típico son secretos eternos en repos y CI. Aplicar el marco de uno
    al otro es el error más caro de la disciplina."
    Fuente al pie: NIST SP 800-63-4 (2025); GitGuardian Secrets Sprawl 2026.

18. OWASP API TOP 10: EL MAPA DE LO QUE PUEDE SALIR MAL
    Título: "El token es una puerta; los riesgos viven en todo el edificio".
    Bullets: BOLA (Api1) · Broken Authentication (Api2) · BOPLA (Api3) ·
    consumo y versión (Api4/9) · negocio y configuración.
    Visual: los 10 riesgos como capas/mapa, con BOLA destacado en rojo.
    GUION: "OWASP nos da el mapa de lo que puede salir mal. Arriba de todo,
    Api1: BOLA, autorización a nivel de objeto. Sigue Api2, autenticación
    rota; Api3, exposición de propiedades, también llamado mass assignment;
    Api4, consumo sin límites; Api5, autorización a nivel de función; Api6,
    flujos de negocio sensibles; Api7, SSRF; Api8, mala configuración; Api9,
    inventario impropio; y Api10, consumo inseguro de terceros. Ninguno de
    estos es 'el token': son el sistema alrededor del token. Por eso el token
    perfecto no alcanza."
    Fuente al pie: OWASP API Security Top 10, edición 2023.

19. ATAQUES REALES (1/2): SE EMITIÓ MAL, NO SE REVOCÓ, SE FILTRÓ
    Título: "El token funcionó exactamente como estaba diseñado".
    Bullets: Facebook "View As" (2018): token emitido al usuario equivocado;
    Okta/Cloudflare (2023): sesión robada y no revocada; Codecov (2021):
    tokens de CI filtrados.
    Visual: tres tarjetas con caso, fuente y lección en una línea.
    GUION: "Los casos que siguen son divulgaciones públicas y responsables; no
    vamos a señalar a nadie, vamos a observar el modelo. Facebook, 2018: la
    función 'View As' generó un access token del usuario consultado, no del
    espectador, y lo dejó embebido en el HTML; se resetearon unos 90 millones
    de cuentas. Okta y Cloudflare, 2023: en el ataque al sistema de soporte
    de Okta, un session token de un ticket se extrajo y siguió sirviendo,
    porque no se rotó ni se revocó a tiempo. (En enero de 2022 Okta ya había
    sufrido otro incidente; en aquel caso Cloudflare no fue impactado gracias
    a sus llaves de hardware.)
    Codecov, 2021: un script modificado exportó las variables de entorno del
    CI y con ellas los tokens y claves. En los tres, el token no falló:
    funcionó como fue diseñado."
    Fuente al pie: Meta (2018); Cloudflare (2023); Codecov (2021).

20. ATAQUES REALES (2/2): SE REUTILIZÓ, SE AUTORIZÓ MAL, SE VALIDÓ MAL
    Título: "Después de aceptarlo, todavía queda trabajo".
    Bullets: Uber (2022): la MFA no sobrevive al robo de sesión; BOLA: token
    válido, objeto ajeno (~40 % de ataques a APIs); JWT mal validado:
    alg:none, confusión HS/RS, kid.
    Visual: tres tarjetas con caso, fuente y lección en una línea.
    GUION: "Uber, 2022: credenciales de un contratista compradas en un foro, un
    SMS que simulaba al área de IT y la aprobación del push; la MFA protegió el
    instante, pero la sesión se reutilizó. BOLA: el atacante presenta su propio
    token, válido y con MFA si quieren, y cambia el identificador del objeto en
    la URL; funciona, y se estima que ronda el 40 % de los ataques a APIs. Y
    las clases de JWT mal validado: alg:none, confusión RS256 a HS256,
    inyección de kid. Ninguna es culpa del string: son fallas de emisión,
    autorización o verificación."
    Fuente al pie: UpGuard/NYT (2022); OWASP 2023; RFC 8725 (2020).

21. MÁS ALLÁ DEL BEARER: ATAR EL TOKEN A SU PORTADOR
    Título: "Si la posesión no basta, exijamos prueba de posesión".
    Bullets: mTLS + token atado al certificado (RFC 8705, 2020); DPoP firma
    por request con jti/htm/htu (RFC 9449, 2023); RFC 9700 (2025) recomienda
    sender-constrained.
    Visual: dos caminos hacia "token atado a su portador".
    GUION: "Si el problema es que cualquiera que tenga el token lo usa, la
    solución es exigir algo más que la posesión. Hay dos caminos
    estandarizados. mTLS más token atado al certificado, RFC 8705 de 2020: el
    token queda ligado al certificado del cliente, así que robarlo no alcanza
    sin el par de claves. Y DPoP, RFC 9449 de octubre de 2023: el cliente
    firma cada request con su clave privada, con un jti único y los datos del
    método y la URL. No necesita PKI. Y esto ya no es opcional: RFC 9700, de
    2025, recomienda tokens sender-constrained donde sea posible."
    Fuente al pie: RFC 8705 (2020); RFC 9449 (2023); RFC 9700 (2025).

22. REFRESH, ROTACIÓN Y REVOCACIÓN
    Título: "La rotación convierte el refresh en un artefacto de un solo uso".
    Bullets: el refresh rotado delata el reuso; RFC 7009 define la
    revocación; introspección (RFC 7662) para tokens opacos; relación entre
    vida del JWT y revocación.
    Visual: ciclo refresh → nuevo access + nuevo refresh; el refresh viejo
    marcado como inválido.
    GUION: "El refresh token es el que renueva sin volver a pedir permiso, y su
    mejor defensa es la rotación: cada vez que se usa, se emite uno nuevo y el
    viejo se invalida. Si un atacante lo usa, el legítimo lo delata en el
    siguiente intento. RFC 6749 lo sugería en 2012; RFC 9700 lo vuelve
    obligatorio para clientes públicos. Y para lo que hay que cortar antes de
    tiempo está la revocación, RFC 7009 de 2013; y para tokens opacos, la
    introspección, RFC 7662. Regla de oro: no podés tener a la vez un JWT de
    larga vida y la capacidad de revocarlo. Elegí uno."
    Fuente al pie: RFC 6749 §10.4 (2012); RFC 7009 (2013); RFC 9700 (2025).

23. EL TOKEN ES FINITO: EMITIR, ROTAR, REVOCAR
    Título: "El token se acaba; el riesgo no".
    Bullets: vida corta y aud estricto; rotación y revocación; mínimo
    privilegio; detección de anomalías; secret manager para claves de máquina.
    Visual: ciclo de vida circular: emitir → usar → expirar → rotar → revocar.
    GUION: "Juntemos las prácticas. Vida corta y audiencia estricta para el
    access token; rotación y revocación para el refresh; scopes mínimos; y
    observabilidad: ¿este token se usa desde dos países a la vez? Para las
    máquinas, la regla es secreto en un secret manager, rotación automática y
    nada de claves eternas en repos ni en variables de entorno. Y recordá el
    dato que le da urgencia a todo esto: la mayoría de los secretos filtrados
    no son contraseñas de personas, son credenciales de sistemas, y más del 60
    % de los secretos válidos que se detectaron en 2022 seguían activos años
    después."
    Fuente al pie: RFC 9700 (2025); RFC 7009 (2013); GitGuardian 2026.

24. CHECKLIST FINAL PARA LLEVARSE
    Título: "Ocho preguntas antes de dar por segura una API".
    Bullets: ¿el algoritmo viene de la config? · ¿validás iss/aud/exp? · ¿la
    vida es corta? · ¿hay rotación y revocación? · ¿autorizás por objeto? ·
    ¿el token va en cabecera? · ¿la identidad de máquina es de vida corta? ·
    ¿qué logueás?
    Visual: checklist de 8 ítems, estilo tarjeta imprimible.
    GUION: "Ocho preguntas para llevarse. Uno: ¿el algoritmo de verificación
    sale de la configuración y no del token? Dos: ¿validás issuer, audiencia y
    expiración con tolerancia de reloj corta? Tres: ¿el access token vive lo
    que debe vivir? Cuatro: ¿hay rotación y revocación de refresh? Cinco: ¿la
    autorización a nivel de objeto está resuelta, o solo la autenticación?
    Seis: ¿el token viaja en cabecera y nunca en la URL? Siete: ¿las
    identidades de máquina usan credenciales de vida corta y rotación? Ocho:
    ¿qué queda en los logs? Si alguna respuesta te incomoda, ahí está tu
    próximo trabajo."
    Fuente al pie: RFC 8725 (2020); RFC 9700 (2025); OWASP API Top 10 (2023).

25. CIERRE: TRES MENSAJES
    Título: "Al fin(ito) y más allá: el token se acaba, el riesgo no".
    Bullets: (a) el token es finito: emitir, rotar, revocar; (b) la MFA
    protege la emisión, no la posesión; (c) autenticar es la puerta, autorizar
    es la cerradura.
    Visual: tres líneas, nada más; QR o URL de bibliografía al pie.
    GUION: "Cerremos con tres ideas. Primero: el bearer token es finito: se
    emite, se roba, se reutiliza y debe morir; medí su vida, rotalo, revocalo,
    porque la ausencia de expiración ya es una vulnerabilidad. Segundo: la MFA
    protege el momento de la emisión, no los treinta días siguientes; diseñá
    para el robo de artefactos, no solo para el robo de contraseñas; y si tu
    invocador es un sistema, no busques un MFA, buscá identidad de workload de
    vida corta. Tercero: autenticar es la puerta; autorizar es la cerradura; un
    token perfecto no impide BOLA. Al fin(ito) y más allá: la seguridad nunca
    estuvo en el string, estuvo siempre en el sistema. Gracias."
    Fuente al pie: bibliografía consolidada al final.

REGLAS
- No inventes datos, CVEs ni enlaces: si no estás seguro de una fuente, usá
  sólo: RFC 6749, RFC 6750, RFC 7519, RFC 8725, RFC 8705, RFC 9449, RFC 9700,
  RFC 8176, RFC 7662, RFC 7009, RFC 7636, RFC 9068, RFC 7523, OWASP API
  Security Top 10 (2023), NIST SP 800-63-4 (2025), OpenID Connect Core (2014),
  WebAuthn (W3C 2019), MITRE ATT&CK T1621/T1539.
- No incluyas instrucciones de prueba ni reproducción de ataques contra
  sistemas de terceros.
- Todos los conceptos de la slide 4 deben quedar representados como CÍRCULOS,
  no como lista.
- La sección de historia no puede exceder 3 slides (5, 6 y 7).
- Salida: una lista numerada 1-25 con: título del slide, bullets, descripción
  del visual, "GUION (texto para decir)" y "Fuente al pie".
````

---

## Notas de uso

- **Si el generador recorta:** pedile explícitamente "no omitas ninguna slide; son 25 en este orden".
- **El guion ya está escrito:** si tu herramienta de slides no acepta notas largas, copiá la sección `GUION` al campo de notas del ponente y dejá los bullets como texto visible del slide.
- **Coherencia con el resto del material:** este prompt reutiliza las mismas fuentes y fechas que `guion.docx`, `clase_tokens_seguridad.md` y `laboratorio_paso_a_paso.md`.
