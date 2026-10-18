# Al fin(ito) y más allá del bearer token — Guion completo de la charla

**Formato:** charla narrada (sin demos), ~60 minutos versión extendida. El Anexo B indica cómo comprimir a 30.
**Tono:** académico, observacional. No se critica a ninguna organización ni persona: se observan fallas de modelo, todas documentadas en divulgaciones públicas.
**Convención:** en **negrita** se marca el **primer antecedente** de cada concepto (norma, edición y fecha) para que puedas citarlo con precisión. Las citas textuales de RFC están en inglés, tal como aparecen en el documento original.

---

## Cómo usar este guion

- Los párrafos en cursiva son indicaciones para el ponente (tiempo, slide sugerida, énfasis).
- Los párrafos sin marcar son texto hablado: puedes leerlos casi literalmente.
- Cada bloque termina con una **frase de cierre** diseñada para ser el "punto" de la sección.
- La bibliografía consolidada está al final; todos los enlaces son fuentes primarias (rfc-editor.org, owasp.org, nist.gov, blogs oficiales de las organizaciones afectadas).

---

# APERTURA — El billete al portador (≈4 min)

*Slide 1: título. Slide 2: una foto de un billete de banco antiguo al portador vs un string de 512 caracteres.*

Buenas tardes a todos. La charla se llama "Al fin(ito) y más allá del bearer token". El título es un juego de palabras con "al infinito y más allá", y no es casual: vamos a hablar de algo que parece infinito —un token que parece que nunca se acaba— y de lo que hay más allá de él, que es donde de verdad vive la seguridad.

Quiero empezar con una definición que parece obvia y no lo es. Un **bearer token** es un artefacto de seguridad cuya posesión equivale a autorización. La palabra "bearer" viene del derecho mercantil: el **instrumento financiero al portador** es aquel que da derecho a quien lo tiene en la mano, sin necesidad de acreditar identidad alguna. Si perdes un billete, quien lo levanta puede gastarlo. Si perdes un token, quien lo tiene puede usarlo.

Eso está escrito en la norma. **Primera aparición: RFC 6750, "The OAuth 2.0 Authorization Framework: Bearer Token Usage", octubre de 2012.** Su resumen dice, textualmente, que cualquier parte en posesión de un bearer token —un "bearer"— puede usarlo para acceder a los recursos protegidos. No dice "el legítimo propietario". Dice "quien lo tiene".

Hoy vamos a hacer tres cosas. Primero, un poco de historia: qué había antes del bearer token, por qué el mundo lo adoptó a pesar de sus riesgos conocidos. Segundo, anatomía: qué tipos de token existen, dónde nacen y cómo se relacionan entre sí. Y tercero —que es el corazón de la charla—, hablar de autenticación multifactor en APIs: qué pasa cuando la API la invoca una persona, y qué pasa cuando la invoca un sistema, que es la mayoría de las veces.

Y todo esto con un tono que quiero declarar desde ahora: **no voy a criticar a nadie**. Los casos que voy a contar son divulgaciones públicas y responsables. Todos —los equipos afectados, quiero decir— hicieron bien el trabajo de transparencia. Lo que vamos a observar es que el modelo de "quien lo tiene, lo usa" produce consecuencias previsibles. Nadie es el villano: el villano, si existe, es el diseño.

*Pausa breve. Frase de transición:* "Empecemos, como siempre, por el principio: por lo que había antes."

---

# BLOQUE 1 — Antes del bearer: una historia breve de la autenticación en HTTP (≈12 min)

*Slide 3: línea temporal horizontal con hitos. Este bloque funciona muy bien como narración sobre una única diapositiva de timeline.*

## 1.1 HTTP Basic y Digest: las credenciales en cada request

Todo empieza con un problema muy concreto: HTTP es un protocolo sin estado, y la web quería proteger recursos. La primera solución fue simple y, con el diario del lunes, terrorífica: mandar el usuario y la contraseña en cada petición.

**Primera aparición: RFC 2617, "HTTP Authentication: Basic and Digest Access Authentication", junio de 1999.** Basic codifica usuario:contraseña en Base64 —que no es cifrado, es una codificación reversible— y lo manda en la cabecera `WWW-Authenticate`. Digest mejoró esto al enviar un hash en lugar de la contraseña en claro, pero ambos esquemas mantienen el mismo problema de fondo: **las credenciales viajan en cada request, contra cada recurso, y el servidor debe conocerlas o verificarlas cada vez.**

**RFC 2617 fue obsoleto por RFC 7616, en agosto de 2015**, que añadió SHA-256 y modernizó Digest. Pero el patrón no cambió: seguimos hablando de credenciales de larga vida que se reutilizan infinitas veces.

*Cita hablada sugerida:* "Basic es como darle a alguien tu llave de casa para que vaya a revisar una habitación. Le das la llave, no le das el acceso a la habitación."

## 1.2 Cookies y sesiones: el estado en el servidor

El segundo gran intento fue no mandar credenciales en cada request, sino mandar un **identificador de sesión**. El servidor guarda el estado; el navegador sólo repite una cookie.

**Primera aparición: la especificación de cookies de Netscape, 1996.** Después vino **RFC 2109, febrero de 1998**, luego **RFC 2965, octubre de 2000** (que prácticamente no se adoptó) y finalmente **RFC 6265, abril de 2011**, que es la especificación de cookies que usamos hoy.

Este modelo es extraordinariamente seguro para aplicaciones web tradicionales... y extraordinariamente inadecuado para APIs. ¿Por qué? Porque el estado vive en el servidor. Cada sesión es un registro en una base de datos. Cuando tenés tres aplicaciones móviles, quince integraciones de terceros y cuatro servicios internos, el modelo de "sesión en servidor" se convierte en un cuello de botella de estado y de escalabilidad. Y sobre todo: **no delega**. La sesión te autentica a vos frente a tu aplicación; no le permite a un tercero actuar en tu nombre con un alcance limitado.

## 1.3 El mundo XML: SAML y WS-Security

Para los que venimos del mundo enterprise, hay que mencionar el otro linaje. **SAML 1.0 se publicó como estándar OASIS en noviembre de 2002, y SAML 2.0 en marzo de 2005.** **WS-Security llegó como estándar OASIS en 2004.** Estos mecanismos usan aserciones XML firmadas criptográficamente —**XML Digital Signature se estandarizó por el W3C en febrero de 2002 y se publicó como RFC 3275 ese mismo año**— y son, en rigor, más seguros que un bearer token: una aserción firmada está atada a un emisor, a un receptor y a un destinatario concretos.

El problema no era la seguridad. El problema era el peso. Integrar WS-Security entre sistemas heterogéneos era —y sigue siendo— un trabajo enorme. Canonicalización XML, preferencias de algoritmos, prefixes... Para una API moderna en JSON, aquello era artillería pesada contra un mosquitero.

## 1.4 OAuth 1.0: firmar cada request

Aquí aparece el ancestro directo del bearer. **OAuth 1.0 nació como especificación comunitaria en diciembre de 2007 y se publicó como RFC 5849 en abril de 2010.** Su mecanismo es fascinante porque es exactamente lo contrario del bearer: en OAuth 1.0 **no se envía ningún token que se pueda copiar**. En su lugar, cada request se firma con HMAC-SHA1 usando un secreto compartido: el consumidor firma la petición con su clave, el servidor verifica la firma, y listo.

¿Qué ganás con eso? Que **robar una petición no sirve**: la firma está atada al método HTTP, a la URL, a los parámetros. Reusarla en otro contexto la invalida. Es, en el fondo, una demostración de posesión —igual que haría después DPoP—.

¿Y qué perdés? Complejidad brutal. Hay que canonicalizar exactamente cada parámetro, en el mismo orden, con el mismo encoding; el secreto debe estar compartido entre cada par de consumidor y proveedor; y cada nuevo servicio que quiera verificar requests necesita una integración propia. Además, en 2008-2010 el mundo se estaba moviendo a móviles nativos, donde los flujos de OAuth 1.0 —con intercambio de firma de tres leguas— eran una pesadilla de experiencia de usuario.

## 1.5 OAuth 2.0 y el nacimiento del bearer

La historia del salto está documentada. **OAuth WRAP (Web Resource Authorization Profiles) apareció como borrador en enero de 2010** —la referencia está en las bibliografías informativas de RFC 6749—, y fue el laboratorio donde se probó la idea de "simplemente manda un string corto y simple". De ahí salió **RFC 6749, "The OAuth 2.0 Authorization Framework", octubre de 2012**.

La motivación de OAuth 2.0, escrita en su propia introducción, es separar la autorización de la autenticación: el cliente obtiene *un conjunto diferente de credenciales* que las del usuario. En lugar de la password, obtiene *an access token — a string denoting a specific scope, lifetime, and other access attributes*.

Ahora viene el detalle histórico que casi nadie cuenta y que te va a diferenciar en la charla: **OAuth 2.0 no nació siendo sólo bearer.** Su §7.1, "Access Token Types", define explícitamente **dos** tipos de token:

- el tipo `bearer`, que se usa simplemente incluyendo el string en la petición, y
- el tipo `mac`, que se usa emitiendo una clave MAC junto con el token y **firmando componentes de la petición HTTP** con ella.

El tipo MAC se definía en un borrador de la IETF: **"HTTP Authentication: MAC Access Authentication", con primera versión de febrero de 2012 (referencia `[OAuth-HTTP-MAC]` en RFC 6749)**. Y ese borrador **nunca llegó a ser RFC: fue abandonado.** La historia de por qué se abandonó es la historia de por qué usamos bearer tokens. El ecosistema eligió simplicidad. La firma por request era técnicamente superior, pero el costo de implementación, de operación y de experiencia de usuario fue decisivo. El bearer ganó porque es trivial de implementar: un string en una cabecera HTTP no necesita canonicalización, ni secretos compartidos, ni relojes sincronizados, ni integración por par.

Y con él llegó la norma que lo consagra: **RFC 6750, octubre de 2012**, "Bearer Token Usage".

*Slide sugerida: dos columnas — "Firmar cada request (OAuth 1.0, MAC)" vs "Mandar un string (Bearer)". Columna izquierda: más seguro, más caro. Columna derecha: menos seguro, universal.*

## 1.6 La admisión que cambia el tono de la charla

Acá viene el momento académico de este bloque. El riesgo del bearer no es un descubrimiento posterior ni una falla de implementación: **está reconocido en el corazón mismo de la norma que lo define.**

Cita textual de **RFC 6749, Sección 10.3 (Considerations for Token Holders... Access Tokens)**:

> *"This specification does not provide any methods for the resource server to ensure that an access token presented to it by a given client was issued to that client by the authorization server."*

Traducción libre: *esta especificación no provee ningún método para que el servidor de recursos se asegure de que un access token presentado por un cliente le fue emitido realmente a ese cliente.*

Es decir: desde 2012, el estándar dice en voz alta que **un servidor de recursos no puede distinguir entre el cliente legítimo y quien robó su token.** La validación de firma —si es que la hay— sólo verifica que el token fue emitido por el servidor de autorización. No verifica a quién.

**Frase de cierre del bloque:** *"El bearer token no falló: cumplió exactamente con lo que prometió. Prometió autorizar por posesión, y autoriza por posesión. Todo lo demás —identificar al portador, saber si sigue vigente, saber si el portador debía tenerlo— es trabajo que la norma dejó deliberadamente fuera."*

---

# BLOQUE 2 — La familia de tokens: de dónde nacen y cómo se relacionan (≈14 min)

*Slide 4: diagrama de flujo Authorization Code Grant con los cuatro tokens numerados. Este es el slide más importante de la charla: todo lo demás cuelga de él.*

## 2.1 El mapa: cuatro tokens que nacen en momentos distintos

Un error muy común —incluso entre gente técnica— es hablar de "el token" como si hubiera uno solo. En realidad, un flujo OAuth 2.0 / OIDC moderno genera **hasta cuatro artefactos distintos, en momentos distintos, con vidas distintas y con destinatarios distintos**. Vamos a verlos en orden de aparición en el flujo.

Usaré una historia simple: ustedes usan una aplicación de terceros —pongamos una app de notas— que quiere leer sus archivos en un servicio en la nube.

### Paso 0: la sesión de la persona (session cookie)

Antes que nada, la persona inicia sesión en el servicio de nube. Eso genera una **cookie de sesión**. **Primera aparición del concepto de sesión persistente en la web: cookies de Netscape, 1996; estandarizadas en RFC 6265, abril de 2011.** La sesión pertenece a la relación *persona ↔ navegador ↔ servicio*. Es el ancla de identidad de la que después colgará todo lo demás.

### Paso 1: el authorization code (el código de autorización)

La app redirige al navegador al servicio de autorización; la persona aprueba; el navegador vuelve a la app con un **código de corta vida** en la URL.

**Primera aparición: RFC 6749, Sección 4.1, octubre de 2012.**

Características que importan:
- **Es de un solo uso.** RFC 6749 §4.1.2 dice textualmente que, si un código se usa más de una vez, el servidor de autorización **debe** denegar el request y **debería** revocar todos los tokens emitidos con ese código.
- **Se emite en el front channel** (a través del navegador, en la URL).
- **Está atado al client_id y a la redirect_uri.**
- Su propósito: **cambiar un artefacto público por uno privado.** El código viaja por el navegador (visible, potencialmente filtrable); el intercambio posterior ocurre por canal trasero, entre servidores, con autenticación de cliente.

*Nota para el ponente:* éste es el momento de decir "el código de autorización es el token que menos se parece a un token: es un cupón de un solo uso".

### Paso 2: el access token (el que viaja a la API)

En el paso anterior, la app intercambia el código por... esto. El **access token** es el que se presenta ante la API en cada petición.

**Primera aparición como concepto en OAuth: RFC 6749, Sección 5, octubre de 2012. Primera aparición de su forma bearer: RFC 6750, mismo mes.** Si es un JWT, su formato está definido por **RFC 7519 (mayo de 2015)**; si es un access token en formato JWT con perfil de OAuth 2.0, existe desde **RFC 9068, mayo de 2021**.

Características:
- **Vida corta** (minutos u horas; RFC 6749 recomienda expirar, y no fija un máximo —ahí está la trampa: la vida la decide quien implementa).
- **Alcance limitado** (`scope`): sólo lo que se pidió y se aprobó.
- **Es el token que viaja al recurso.** Por eso es el que llamamos bearer: el recurso no lo verifica con el emisor en cada request (normalmente), sólo lo acepta.
- **Audience (`aud`)**: para qué servicio vale.

### Paso 3: el refresh token (el que renueva sin volver a pedir permiso)

Cuando el access token expira, la app necesita continuar sin volver a arrastrar a la persona por toda la pantalla de consentimiento. Ahí entra el **refresh token**: un token de vida larga que sólo se usa contra el endpoint de token, nunca contra la API de recursos.

**Primera aparición: RFC 6749, Secciones 1.5 y 6, octubre de 2012.**

Características y salvaguardas definidas en la norma:
- **Se emite a clientes confidenciales** (o a públicos con restricciones); viaja por canal trasero.
- **Debe mantenerse la vinculación con el cliente** (RFC 6749 §10.4).
- **Rotación de refresh token:** RFC 6749 §10.4 la sugiere como mecanismo de detección de abuso —"el servidor de autorización podría emplear refresh token rotation"—. **RFC 9700, enero de 2025, la convierte en práctica obligatoria para clientes públicos.** La rotación es, en la práctica, el mecanismo que convierte al refresh token en un artefacto de un solo uso: si un atacante lo usa, la rotación del legítimo lo delata.
- **Se puede revocar:** **RFC 7009, octubre de 2013**, "OAuth 2.0 Token Revocation", define el endpoint para hacerlo.

*Cita hablada sugerida:* "El access token es el boleto de entrada al teatro. El refresh token es la acreditación que te deja pedir un boleto nuevo toda la semana sin volver a pasar por la taquilla. Robar una no es robar la otra —pero se relacionan: por eso se rotan juntos."

### Paso 4: el ID token (que no es un token de acceso)

Y acá aparece el confundido más famoso de la fiesta. **OpenID Connect, primera aparición: especificaciones finales aprobadas por la OpenID Foundation el 26 de febrero de 2014** (borradores en circulación desde 2012). OIDC añade sobre OAuth 2.0 un **ID token**: un **JWT** que responde a la pregunta *"¿quién es esta persona y cómo se autenticó?"*, no *"¿qué puede hacer?"*.

Características que debés enfatizar:
- **Va dirigido a la aplicación cliente, no a la API de recursos.** Lleva `aud` = el client_id de la app.
- **Contiene claims de autenticación**: `sub`, `auth_time`, `amr`, `acr`.
- **Nunca debe usarse para acceder a recursos.** Ese es el trabajo del access token. Mezclarlos es un error clásico de implementación.

*Cita hablada sugerida:* "El ID token es el documento de identidad que te muestran en la puerta. El access token es el pase que te ponen en la muñeca para entrar al recinto. Si confundís los dos, vas a intentar entrar a los conciertos mostrando el DNI."

### El refresh token nunca va a la API de recursos

Regla que conviene escribir en una slide enorme: **el refresh token jamás viaja a la API de recursos; el access token jamás debería usarse para refrescar.** Son mundos distintos: recursos vs. emisión.

## 2.2 Los tokens que no son OAuth: API keys

Hasta acá todo es OAuth/OIDC. Pero la mayoría de las APIs del mundo no usan OAuth: usan **API keys**.

- **Primera aparición:** no hay un RFC. Es práctica de industria, popularizada a mediados de los 2000 con la computación en la nube —las *access keys* de Amazon Web Services, disponibles desde el lanzamiento de AWS en 2006, son el arquetipo—, y masificada por proveedores como Stripe, Twilio y compañía.
- **Qué son:** un identificador estático, casi siempre un par `key_id` + `secret`, emitido a un *sistema*, no a una persona.
- **Qué NO son:** no autentican a un usuario, no llevan `exp` por defecto, no llevan `scope` a menos que el proveedor lo implemente. **Una API key es identificación, no autenticación.**
- **Por qué importan en la charla:** porque son el bearer token más extendido y más ignorado. Se meten en código fuente, en apps móviles (donde son extraíbles), en variables de entorno, en frontends.

**Dato para citar en el Bloque 5:** GitGuardian detectó **28,65 millones de secretos nuevos** en commits públicos de GitHub sólo en 2025 (un aumento del 34 % interanual), y sus datos indican que **más del 60 % de los secretos que confirmó como válidos en 2022 seguían activos y explotables años después** ([State of Secrets Sprawl 2026](https://www.gitguardian.com/state-of-secrets-sprawl-report-2026)).

## 2.3 Opaque vs. autocontenido: el dilema de la revocación

El último eje de este bloque es la gran bifurcación técnica:

**Token opaco** — un string arbitrario que el servidor de recursos **no puede leer**. Para validarlo debe consultarlo: **introspección, primera aparición: RFC 7662, octubre de 2015**.
- Ventaja: revocación inmediata, estado centralizado, fácil de entender.
- Costo: cada petición implica una llamada de validación (o caché con política de expiración), y el servidor de recursos depende de red.

**Token autocontenido (JWT)** — el servidor de recursos **lo verifica localmente** con la clave pública del emisor.
- Ventaja: cero estado, cero ida y vuelta, escala magníficamente.
- Costo: **no se puede revocar antes de su expiración** sin mecanismos adicionales. Por eso la vida del access token en JWT debe ser corta, y por eso la rotación del refresh token importa tanto.

**La regla de oro que conviene escribir en una slide:** *"No podés tener a la vez un JWT de larga vida y la capacidad de revocarlo. Elegí uno de los dos."*

*Frase de cierre del bloque:* *"Un token no es un monolito. Es una familia con roles distintos: el código entra, el access token opera, el refresh token renueva, el ID token identifica. La mayoría de las fallas que vamos a ver después nacen de confundir estos roles —o de darles vidas que no corresponden—."*
