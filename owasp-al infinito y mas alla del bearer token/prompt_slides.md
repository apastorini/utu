# Prompt para generar 15 slides de la charla "Al fin(ito) y más allá del bearer token"

Copia el bloque de abajo y pegalo en la IA generadora de slides (Gamma, Tome, Copilot, Gemini, etc.).

---

```
ROL
Actuá como diseñador de presentaciones técnicas y experto en seguridad de APIs REST.

CONTEXTO
Prepará 15 slides en ESPAÑOL para una charla de ~30-45 minutos titulada
"Al fin(ito) y más allá del bearer token" (juego de palabras con "al infinito
y más allá"). Audiencia: público técnico medio (devs, arquitectos, equipos de
seguridad). No hay demos: es una charla narrada, con tono académico y
OBSERVACIONAL — no se critica a ninguna organización ni persona; los incidentes
se citan como divulgaciones públicas y se analizan como fallas de modelo, no de
equipos.

TONO Y ESTÉTICA
- Un solo mensaje por slide, máximo 5 bullets cortos (máx. 12 palabras c/u).
- Títulos que cuenten una idea, no un tema (ej: "La MFA protege un instante,
  no 30 días" en vez de "MFA en APIs").
- Cada dato o cita lleva la fuente en letra chica al pie (RFC, fecha, URL).
- Estilo visual: limpio, fondo oscuro o neutro, un color de acento, tipografía
  sans-serif, íconos mínimos, diagramas de flujo simples. Nada de cliparts ni
  párrafos pegados de la norma.
- Incluí "Notas del ponente" por slide (3-4 líneas con qué decir).

ESTRUCTURA EXACTA DE LOS 15 SLIDES

1. Portada: título + subtítulo "Un billete al portador llamado token".
2. Definición: bearer token = posesión equivale a autorización ("quien lo
   tiene, lo usa"). Fuente: RFC 6750, octubre de 2012.
3. Antes del bearer: mini-timeline — Basic/Digest (RFC 2617, 1999), cookies
   (RFC 6265, 2011), SAML/WS-Security (2004-2005), OAuth 1.0 firma HMAC
   (RFC 5849, 2010). Problema de cada uno en una línea.
4. El punto de giro: OAuth 2.0 (RFC 6749, oct 2012) nació con DOS tipos de
   token: bearer y mac (borrador de febrero 2012, abandonado). El ecosistema
   eligió simplicidad. Cita al pie del §10.3 de RFC 6749: la norma admite que
   no garantiza que el token le fue emitido al cliente que lo presenta.
5. La familia de tokens (diagrama de flujo): sesión → authorization code
   (un solo uso) → access token (corto) → refresh token (largo, rotación) +
   ID token (OIDC, feb 2014, NO sirve para acceder a recursos).
6. Tabla de roles y vidas: token | para qué | vida | dónde viaja | primera
   aparición (RFC + fecha). Regla destacada: el refresh token jamás viaja a
   la API de recursos.
7. Anatomía de un JWT: header.payload.signature; base64 NO es cifrado; claims
   clave (iss, aud, exp, scope, amr, acr, kid); advertencia "el algoritmo no
   viene del token" (RFC 8725, feb 2020).
8. Transporte: cabecera vs cookie vs query. RFC 6750 (2012) permitía query;
   RFC 9700 (enero 2025) lo prohíbe. Trece años de logs, Referer y CDN.
9. Tesis central (slide destacada): "La MFA no está en la API: está en el
   momento de la emisión". Timeline: password → MFA → emisión → 30 días de
   token → API.
10. Caso persona: niveles de garantía NIST SP 800-63-4 (julio 2025), AAL1-3,
    passkeys/WebAuthn (W3C, 2019) como único factor anti-phishing, step-up con
    acr/amr (RFC 8176, 2017).
11. Los 3 modos en que la MFA no salva a un bearer: fatiga de push
    (MITRE T1621), phishing AiTM, robo de sesión/infostealers.
12. Caso sistema: no hay humano que factorizar. Tabla de mecanismos:
    client credentials (RFC 6749 §4.4), private_key_jwt (RFC 7523),
    mTLS (RFC 8705, 2020), DPoP (RFC 9449, 2023), rotación y vida corta.
13. Tabla comparativa persona vs sistema (5-6 filas: qué se prueba, segundo
    factor, vida típica, fallo típico, revocación) + dato: la mayoría de los
    secretos filtrados son credenciales de máquinas, no de personas
    (GitGuardian, State of Secrets Sprawl 2026).
14. Ataques reales en tarjetas (6): Facebook "View As" 2018 (token mal
    emitido), Okta/Cloudflare 2023 (token no revocado), Codecov 2021 (tokens
    en CI), Uber 2022 (MFA no sobrevive al robo de sesión), BOLA (token
    válido + objeto ajeno, Api1 OWASP 2023), JWT mal validado. Cada tarjeta:
    caso, link de la fuente oficial, lección en una línea.
15. Cierre "más allá del bearer" + 3 mensajes: (a) el token es finito:
    emitir, rotar, revocar; (b) la MFA protege la emisión, no la posesión;
    (c) autenticar es la puerta, autorizar es la cerradura (BOLA). Frase
    final: "Al fin(ito) y más allá: el token se acaba, el riesgo no."
    Incluir QR/URL de bibliografía en las notas.

REGLAS
- No inventes datos, CVEs ni enlaces: si no estás seguro de una fuente, usá
  sólo: RFC 6749, RFC 6750, RFC 7519, RFC 8725, RFC 8705, RFC 9449, RFC 9700,
  RFC 8176, RFC 7662, RFC 7009, RFC 7636, OWASP API Security Top 10 (2023),
  NIST SP 800-63-4 (2025), OpenID Connect Core (2014).
- No incluyas instrucciones de prueba ni reproducción de ataques contra
  sistemas de terceros.
- Salida: una lista numerada 1-15 con: Título del slide, bullets, "Nota del
  ponente", "Fuente al pie".
```
