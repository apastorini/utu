# Tokens de identidad, de Basic al DPoP — Clase completa

**Guion + explicación + laboratorio de seguridad de APIs**
Versión: 1.0 · Foco: seguridad ofensiva *autorizada* y defensa · Incluye caso ID Uruguay.

---

## Índice

0. [Cómo usar esta clase y reglas de ética/legal](#0-cómo-usar-esta-clase-y-reglas-de-éticolegal)
1. [Enfoques para abordar la seguridad de APIs](#1-enfoques-para-abordar-la-seguridad-de-apis)
2. [Módulos técnicos](#2-módulos-técnicos)
   - [M1 — HTTP Basic / Digest](#m1--http-basic--digest-1999)
   - [M2 — Cookies y sesiones](#m2--cookies-y-sesiones-1996)
   - [M3 — API keys](#m3--api-keys-medios-de-los-2000)
   - [M4 — OAuth 1.0 (firma HMAC)](#m4--oauth-10-firma-hmac-2007--2010)
   - [M5 — Bearer token (OAuth 2.0)](#m5--bearer-token-oauth-20-2012)
   - [M6 — JWT](#m6--jwt-2010--2015)
   - [M7 — OIDC, authorization code, PKCE, ID token](#m7--oidc-authorization-code-pkce-e-id-token-2014)
   - [M8 — Refresh token](#m8--refresh-token-2012)
   - [M9 — mTLS y DPoP (sender-constrained)](#m9--mtls-y-dpop-sender-constrained-2020--2023)
   - [M10 — OWASP API Security Top 10 (laboratorio)](#m10--owasp-api-security-top-10-laboratorio)
   - [M11 — Caso ID Uruguay (laboratorio ético)](#m11--caso-id-uruguay-laboratorio-ético)
3. [Entorno de laboratorio seguro](#3-entorno-de-laboratorio-seguro)
4. [Glosario de atajos](#4-glosario-de-atajos)
5. [Plantilla de reporte responsable](#5-plantilla-de-reporte-responsable)
6. [Bibliografía](#6-bibliografía)

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
> Probar autenticación, robar/reutilizar tokens o manipular identificadores de objetos en sistemas de terceros **sin autorización** es acceso no autorizado y es delito, aunque "sólo sea mirar" o aunque el token lo hayas copiado de tu propio navegador.

Buenas prácticas mínimas:
- **Tu cuenta, tu sesión, tu cliente:** observar tu propio token en tu propio navegador es legítimo; reutilizarlo contra otros recursos o cuentas, no.
- **Alcance escrito:** si vas a probar algo que no es tuyo, pedí permiso y guardá el correo/RFC de autorización.
- **No exfiltrás datos:** si encontrás algo, demostrá el acceso con el mínimo dato necesario (p. ej. tu propio ID), nunca volcás la base.
- **Divulgación responsable:** reportá al dueño del sistema o a su CERT. En Uruguay: **CERTuy (AGESIC)** — https://www.gub.uy/centro-nacional-respuesta-incidentes-seguridad-informatica/
- **Laboratorios recomendados:** OWASP crAPI, DVGA, OWASP Juice Shop, VAmPI, PortSwigger Web Security Academy (labs de JWT y OAuth).

*Herramientas de la clase:* `curl`, navegador con DevTools, Burp Suite Community / ZAP, `jwt_tool`, `PyJWT` (Python), `docker`, `gitleaks`/`ggshield`.

---

## 1. Enfoques para abordar la seguridad de APIs

Antes de elegir "de qué hablo", conviene elegir **con qué lente miro**. Una charla de seguridad de APIs puede organizarse de muchas formas; cada enfoque ilumina cosas distintas y esconde otras. Éstos son los diez enfoques clásicos, con su pregunta central y cuándo conviene usarlos.

### 1.1 Enfoque por capas (arquitectura)

La API es una pila: **cliente → red → gateway → autenticación → autorización → lógica de negocio → datos**. Vas capa por capa preguntando "¿dónde se rompe esto?".

- **Pregunta central:** ¿en qué capa vive el control y en qué capa vive el atacante?
- **Cuándo usarlo:** charlas para arquitectos y equipos mixtos; es el más didáctico.
- **Riesgo de omitirlo:** creer que "arreglé la autenticación" equivale a "arreglé la API" (no: BOLA vive en la capa de autorización/lógica).

### 1.2 Enfoque por actor: persona vs. sistema

¿Quién invoca la API? Una persona (browser/app), otro sistema (M2M), o un servicio en nombre de una persona (delegación).

- **Pregunta central:** ¿qué significa "autenticarse" cuando el invocador no es humano?
- **Cuándo usarlo:** cuando querés hablar de MFA, identidades no humanas y tokens de máquina.
- **Riesgo de omitirlo:** aplicar el modelo de la persona al sistema (pedir "MFA" a un microservicio) o al revés (dejar credenciales eternas en CI).

### 1.3 Enfoque por ciclo de vida del token

Recorrés el token entero: **emisión → transporte → almacenamiento → uso → renovación → revocación → expiración**.

- **Pregunta central:** ¿en qué eslabón se puede robar, reutilizar o perpetuar este token?
- **Cuándo usarlo:** es el enfoque de **esta clase y de la charla**; permite hablar de access token, refresh token, ID token y sus relaciones.
- **Riesgo de omitirlo:** hablar sólo de "cómo se firma" y olvidar la vida útil, la rotación y la revocación (donde ocurren la mayoría de los incidentes reales).

### 1.4 Enfoque por OWASP API Security Top 10

Tomás la lista como checklist: BOLA, Broken Authentication, BOPLA, Unrestricted Resource Consumption, BFLA, Sensitive Business Flows, SSRF, Misconfiguration, Improper Inventory, Unsafe Consumption.

- **Pregunta central:** ¿cuál de los diez riesgos tengo hoy y cómo lo pruebo?
- **Cuándo usarlo:** para una charla práctica o una auditoría; mapea directo a testing.
- **Riesgo de omitirlo:** quedarse en la teoría de tokens sin cubrir autorización, negocio ni configuración.
- **Referencia:** [OWASP API Security Top 10 – 2023](https://owasp.org/API-Security/editions/2023/en/0x11-t10/)

### 1.5 Enfoque por tecnología (histórico/evolutivo)

La línea del tiempo: Basic/Digest → cookies → API keys → OAuth 1.0 → bearer → JWT → OIDC/PKCE → mTLS/DPoP.

- **Pregunta central:** ¿por qué cada tecnología nació, qué resolvió y qué dejó abierto?
- **Cuándo usarlo:** para enseñar fundamentos y "por qué estamos donde estamos" (es el enfoque de la charla).
- **Riesgo de omitirlo:** repetir modas sin entender los trade-offs.

### 1.6 Enfoque por paradigma de confianza

**ACL vs. capabilities; identidad vs. posesión; perimetral vs. Zero Trust.** Un bearer token es una *capability*: acceso por posesión, sin identidad del portador.

- **Pregunta central:** ¿estoy confiando en *quién sos* o en *qué tenés*?
- **Cuándo usarlo:** para dar profundidad conceptual y justificar DPoP/mTLS.
- **Riesgo de omitirlo:** no entender por qué "robar el token" es un ataque completo.

### 1.7 Enfoque por audiencia

| Audiencia | Qué le importa | Cómo contarlo |
|---|---|---|
| Devs | "¿Cómo lo implemento bien?" | Código, librerías, checklist |
| Arquitectos | "¿Cómo diseño el sistema?" | Diagramas, trade-offs, ciclo de vida |
| Pentesters | "¿Cómo lo rompo?" | Metodología, herramientas, payloads (en lab) |
| Management | "¿Cuánto me cuesta?" | Riesgo, casos, cumplimiento |

### 1.8 Enfoque por superficie de ataque

Cliente (token en JS/localStorage) · red (TLS, proxies) · backend (validación de claims) · cadena de suministro (CI, dependencias) · negocio (abuso de flujos).

- **Pregunta central:** ¿desde dónde me atacan y con qué activo?
- **Cuándo usarlo:** cuando querés cubrir fugas "aburridas pero reales" (secretos en repos y CI).
- **Riesgo de omitirlo:** subestimar que la mayoría de los secretos filtrados son de máquinas, no de personas.

### 1.9 Enfoque por cumplimiento / regulatorio

PCI DSS, ISO 27001, el **Marco de Ciberseguridad de Uruguay (AGESIC)**, obligaciones de reporte a CERTuy.

- **Pregunta central:** ¿qué me exige la norma y cómo se traduce en controles de token?
- **Cuándo usarlo:** en contextos de gobierno/empresa regulada (incluye el caso ID Uruguay).

### 1.10 Enfoque por "ataque y defensa" (kill-chain del token)

Cinco momentos: **obtener → transportar → almacenar → usar → renovar**. Para cada uno, qué hace el atacante y qué control lo frena.

- **Pregunta central:** ¿cómo se ve el ataque completo, de punta a punta?
- **Cuándo usarlo:** charlas de seguridad propiamente dichas.

### Tabla comparativa y recomendación

| Enfoque | Pregunta central | Mejor para | Si lo omito… |
|---|---|---|---|
| Capas | ¿Dónde vive el control? | Arquitectos | Confundo authn con authz |
| Actor | ¿Persona o sistema? | MFA / M2M | Aplico mal la MFA |
| Ciclo de vida | ¿En qué eslabón falla? | Charla integral | Olvido rotación/revocación |
| OWASP Top 10 | ¿Qué riesgo tengo? | Auditoría/práctica | Me quedo en teoría |
| Tecnología (histórico) | ¿Por qué nació? | Fundamentos | Repito modas |
| Paradigma de confianza | ¿Identidad o posesión? | Profundidad | No entiendo el riesgo bearer |
| Audiencia | ¿A quién hablo? | Cualquier charla | Pierdo al público |
| Superficie | ¿Desde dónde? | Cubrir fugas reales | Ignoro CI/repos |
| Cumplimiento | ¿Qué me exigen? | Gobierno/regulada | No traduzco norma a control |
| Ataque/defensa | ¿Cómo es la cadena? | Seguridad | Queda teórico |

**Recomendación para esta charla:** enfoque por **ciclo de vida + actor + histórico**, con la **OWASP API Top 10** como atlas de vulnerabilidades y el **estudio de casos** como cierre. Es lo que estructura este documento.

---

## 2. Módulos técnicos

> En cada módulo: **Idea · Guion · Ejemplo práctico · Vulnerabilidades y cómo comprobarlas · Defensa.**
> Recordá: las comprobaciones ofensivas van **sólo** contra laboratorios o entornos autorizados.

---

## M1 — HTTP Basic / Digest (1999)

### Idea
Autenticación HTTP clásica: el cliente manda credenciales (Basic: `usuario:contraseña` en Base64) en **cada** petición. **Primera aparición: RFC 2617, junio de 1999**; Digest añade un hash y un `nonce`; **RFC 7616 (agosto de 2015)** moderniza Digest con SHA-256 y reemplaza a la 2617.

### Guion para explicar
"Basic es como darle a alguien la llave de tu casa para que entre a revisar una habitación: le das la llave, no un permiso para esa habitación. Viaja en cada request, y si mirás el valor, no está cifrado: está codificado. Base64 no es seguridad; es transporte tolerante a caracteres."

### Ejemplo que puedo hacer
```bash
# Endpoint público de práctica (no es un sistema de terceros real)
curl -v -u usuario:clave https://httpbin.org/basic-auth/usuario/clave

# Mirar la cabecera
curl -s -u usuario:clave https://httpbin.org/basic-auth/usuario/clave -D -
```
En el navegador: DevTools → Network → cualquier request con `Authorization: Basic ...` → copiá el valor y decodificalo:
```bash
echo -n "dXN1YXJpbzpjbGF2ZQ==" | base64 -d
```

### Vulnerabilidades y cómo comprobarlas (en tu entorno)
| Vulnerabilidad | Cómo se comprueba (autorizado) |
|---|---|
| Credenciales reutilizadas por request | Interceptá una request con un proxy (Burp/ZAP) en **tu** app y reenviala: sigue autenticando todo el tiempo |
| No hay "logout" real | Guardá la cabecera y usala de nuevo tras "cerrar sesión" en tu app: si sigue funcionando, no hay revocación |
| Base64 ≠ cifrado | Decodificá la cabecera (comando de arriba) |
| Fuerza bruta | En tu app, medí si hay rate-limit/lockout enviando N intentos de tu propio usuario de prueba |
| Credenciales en logs/URLs | Buscá en tus propios logs si aparece el header; en APIs de prueba, probá una URL con user:pass |

### Defensa
TLS obligatorio, migrar a tokens/OIDC, rate-limit y lockout, nunca loguear credenciales, nunca usar Basic en URLs.

---

## M2 — Cookies y sesiones (1996)

### Idea
El servidor guarda el estado y el navegador repite un **identificador de sesión** en una cookie. **Primera aparición: especificación de cookies de Netscape, 1996; RFC 2109 (1998); RFC 6265 (abril de 2011)** es la vigente.

### Guion para explicar
"La sesión en servidor es segura para la web tradicional y mala para APIs: el estado no escala, no delega y no cruza clientes. Pero trae dos problemas clásicos que seguimos viendo: robo de cookie por XSS y CSRF."

### Ejemplo que puedo hacer
- En tu app: login → DevTools → Application → Cookies → observá `HttpOnly`, `Secure`, `SameSite`.
- Con `curl` (tu app): `curl -c cookies.txt -d 'user=...&pass=...' https://TU-APP/login` y luego `curl -b cookies.txt https://TU-APP/perfil`.

### Vulnerabilidades y cómo comprobarlas
| Vulnerabilidad | Cómo se comprueba (autorizado/lab) |
|---|---|
| Cookie sin `HttpOnly` → XSS la lee | En un lab (PortSwigger XSS / Juice Shop) inyectá `document.cookie` y verificá que la sesión es accesible |
| Sin `SameSite` → CSRF | Lab de CSRF de PortSwigger: formulario que dispara una acción autenticada |
| Session fixation | En tu app: fijá vos el valor de la cookie antes del login y verificá si el servidor la respeta |
| Sesión no se invalida al logout | Reutilizá la cookie vieja tras logout: si sirve, no hay revocación |
| Falta de rotación de sesión | Compará el ID de sesión antes y después del login (debería cambiar) |

### Defensa
`HttpOnly` + `Secure` + `SameSite`, rotar el ID en el login, invalidar en el servidor al logout, tiempo de inactividad, tokens CSRF.

---

## M3 — API keys (mediados de los 2000)

### Idea
No tienen RFC: son práctica de industria, popularizadas con la nube (**access keys de AWS, 2006**). Identifican a un sistema, **no autentican a una persona**, y por defecto **no expiran**.

### Guion para explicar
"La API key es el bearer token más usado y menos cuidado del mundo. Es un identificador estático que se mete en un archivo, en una variable de entorno o —peor— en el JavaScript de un frontend, donde cualquiera lo lee. Identifica, no autentica."

### Ejemplo que puedo hacer
```bash
curl -H "X-API-Key: TU_CLAVE_DE_PRUEBA" https://httpbin.org/headers
```
Para mostrar extracción: en **tu propia** web/app, DevTools → Network → buscá `api_key`, `apikey`, `token` en las requests del cliente.

Escaneo de **tus propios** repos (no de terceros):
```bash
# gitleaks o ggshield sobre tu repo
gitleaks detect --source . -v
```

### Vulnerabilidades y cómo comprobarlas
| Vulnerabilidad | Cómo se comprueba |
|---|---|
| Clave hardcodeada en el cliente | DevTools/descompilar tu app; buscá el secreto en el bundle |
| Clave en el repositorio | `gitleaks`, `ggshield`, `trufflehog` sobre tu repo/CI |
| Sin expiración ni rotación | Verificá que la clave sigue funcionando después de meses (tu entorno) |
| Sin scope ni límites | Usá la clave "de solo lectura" para intentar una operación de escritura en tu API |
| Sin rate limit | Enviá N requests a tu endpoint con la misma key y medí 429/423 |

### Defensa
Rotación, revocación, scope, IP allowlist, rate limit, secret manager, detección en CI (secret scanning). Dato para citar: **28,65 M de secretos nuevos en commits públicos de GitHub en 2025 (+34 %)** — [GitGuardian, State of Secrets Sprawl 2026](https://blog.gitguardian.com/the-state-of-secrets-sprawl-2026/).

---

## M4 — OAuth 1.0 (firma HMAC) (2007 / 2010)

### Idea
Antes del bearer, OAuth **firmaba cada request** con HMAC-SHA1 y un secreto compartido. **Especificación comunitaria, diciembre de 2007; RFC 5849, abril de 2010.** El token no se puede copiar y reusar: la firma está atada al método, la URL y los parámetros. Es el ancestro conceptual de DPoP.

### Guion para explicar
"OAuth 1.0 era la antítesis del bearer: nada de mandar un string reutilizable, cada request se firmaba. Más seguro en teoría, carísimo en la práctica: canonicalizar parámetros, secretos compartidos por cada par de servicios, y una pesadilla en móviles. El mundo eligió simplicidad y nació el bearer."

### Ejemplo que puedo hacer
Construir la firma conceptualmente en Python (sin llamar a nadie):
```python
import hmac, hashlib, base64, urllib.parse
method = "GET"
url = "https://api.ejemplo.com/recurso"
params = {"oauth_consumer_key": "key", "oauth_nonce": "abc123", "oauth_timestamp": "1700000000"}
base = "&".join([method, urllib.parse.quote(url, safe=""),
                 urllib.parse.quote("&".join(f"{k}={params[k]}" for k in sorted(params)), safe="")])
signature = base64.b64encode(hmac.new(b"secreto", base.encode(), hashlib.sha1).digest())
print("oauth_signature =", urllib.parse.quote(signature))
```
Mostrá que cambiar **un solo parámetro** invalida la firma: eso es lo que el bearer no tiene.

### Vulnerabilidades y cómo comprobarlas
| Vulnerabilidad | Cómo se comprueba (lab propio) |
|---|---|
| Errores de canonicalización | Alterá el orden/encoding de parámetros y observá si la firma valida o no |
| Secreto compartido filtrado | Si el secreto se filtra, se pueden firmar requests: probá en tu implementación de práctica |
| Sin anti-replay (nonce/timestamp) | Reenviá la misma request firmada dos veces contra tu lab: ¿la acepta? |
| Complejidad de implementación | Compará líneas de código vs. un flujo bearer |

### Defensa
Nonce + timestamp anti-replay, secretos por par, TLS. Hoy: migrar a DPoP en vez de reimplementar OAuth 1.0.

---

## M5 — Bearer token (OAuth 2.0) (2012)

### Idea
OAuth 2.0 separa autorización de autenticación y entrega al cliente un **access token**: un string con alcance y vida. **RFC 6749, octubre de 2012**; su uso bearer, **RFC 6750, octubre de 2012**. La regla: **quien tiene el token, lo usa.** La propia norma lo admite en **RFC 6749 §10.3**: *"This specification does not provide any methods for the resource server to ensure that an access token presented to it by a given client was issued to that client by the authorization server."*

### Guion para explicar
"El bearer ganó por simplicidad: un string en una cabecera, sin firmar cada request, sin secretos compartidos. El precio está escrito en la norma: el servidor de recursos no puede saber si quien presenta el token es a quien se le emitió. Ese es el corazón de esta clase."

### Ejemplo que puedo hacer
```bash
# Con TU token (de tu cuenta / tu entorno)
curl -H "Authorization: Bearer TU_TOKEN" https://httpbin.org/bearer

# Inspeccionar la forma de la cabecera en DevTools de TU app
# Network -> Request Headers -> Authorization: Bearer eyJ...
```
**Demostración de reutilización (sólo tu cuenta, tu entorno):** copiá tu token a un `curl` en otra terminal —atelada al mismo host de tu app— y comprobá que el servidor lo acepta sin más. Eso *es* el punto de la charla; no lo hagas contra terceros.

### Vulnerabilidades y cómo comprobarlas
| Vulnerabilidad | Cómo se comprueba (tu entorno) |
|---|---|
| Replay: el token no está atado al cliente | Copiá el token y usalo desde otro cliente (curl) contra tu API |
| Token en URL/query | Buscá tokens en logs, en el header `Referer` o en el historial (tu app) |
| Vida demasiado larga | Decodificá `exp` (JWT) o medí cuánto sigue vivo un token opaco |
| Sin revocación | Probá tu token después de "cerrar sesión": si sigue válido, no hay revocación (RFC 7009) |
| Sobre-privilegio | Pedí un token con scope amplio en tu client y usá un endpoint fuera del scope mínimo |
| Transporte inseguro | Verificá que tu API sólo acepta HTTPS y rechaza el token por HTTP |

### Defensa
Vida corta, `aud` estricto, scope mínimo, revocación (RFC 7009) e introspección (RFC 7662), nunca en query (**RFC 9700, enero 2025** lo prohíbe), y sender-constrained (M9).

---

## M6 — JWT (2010 / 2015)

### Idea
**JWT (JSON Web Token)**: `header.payload.signature`, base64url. **Primer borrador: 28 de diciembre de 2010; RFC 7519, mayo de 2015** (familia JOSE: JWS 7515, JWE 7516, JWK 7517, JWA 7518). El payload **no está cifrado**: está firmado. El header trae `alg` y `kid`.

### Guion para explicar
"Un JWT es como una credencial plastificada: firmada, no sellada. Cualquiera lee el contenido. Y guarda una trampa: el header dice con qué algoritmo se firmó; si el validador le hace caso al token en lugar de a su configuración, el atacante elige el algoritmo. De ahí salen `alg: none`, la confusión RS256→HS256 y la inyección de `kid`."

### Ejemplo que puedo hacer
Generá y decodificá tu propio JWT (nada de terceros):
```python
# pip install pyjwt
import jwt
token = jwt.encode({"sub": "123", "scope": "read", "iss": "https://mi-lab"}, "secreto", algorithm="HS256")
print(token)
print(jwt.decode(token, "secreto", algorithms=["HS256"]))
```
Decodificá el payload **sin verificar** para ver que base64 no oculta nada:
```bash
python -c "import base64,sys; p=sys.argv[1].split('.')[1]; print(base64.urlsafe_b64decode(p+'='*(-len(p)%4)).decode())" eyJ...
```

### Vulnerabilidades y cómo comprobarlas (en laboratorio propio)

**Montá un lab minúsculo** (Flask) que acepte JWT, para probar los clásicos sin tocar a nadie:

```python
# lab_jwt.py  ->  flask run  (sólo local)
from flask import Flask, request, jsonify
import jwt
app = Flask(__name__)
@app.route("/perfil")
def perfil():
    tok = request.headers.get("Authorization", "").replace("Bearer ", "")
    try:
        # ATAJO VULNERABLE A PROPÓSITO: confía en el alg del token y usa la clave como secreto
        data = jwt.decode(tok, "secreto", algorithms=None, options={"verify_signature": True})
        return jsonify(data)
    except Exception as e:
        return str(e), 401
```

| Ataque | Cómo se comprueba (contra EL LAB de arriba) |
|---|---|
| `alg: none` | Generá un token con `{"alg":"none"}` y sin firma; si el servidor lo acepta, es vulnerable |
| Confusión RS256→HS256 | Si el server verifica con clave pública, intentá firmar con HS256 usando esa clave pública como secreto |
| `kid` injection | Enviá `kid` apuntando a un archivo/ruta conocida; observá si cambia la clave usada |
| Secreto débil (HS256) | Crackeá **tu propio** token con `hashcat`/`jwt_tool` y un diccionario: `jwt_tool eyJ... -C -d rockyou.txt` |
| Sin `exp` / `aud` | Generá un token sin expiración o con otra `aud` y probá si el endpoint lo acepta |
| Firma no verificada | Cambiá un byte del payload sin refirmar; si pasa, no verifica firma |

Con `jwt_tool` (todo contra tu lab):
```bash
git clone https://github.com/ticarpi/jwt_tool
python3 jwt_tool.py eyJ... -M at      # prueba alg none
python3 jwt_tool.py eyJ... -C -d wordlist.txt   # crackea el secreto
```

### Defensa
`alg` **desde la configuración del validador**, nunca del token; verificar `iss`, `aud`, `exp`, `nbf`; claves fuertes; rotación de claves (`kid` correcto); validar contra JWKS; y **RFC 8725 (febrero 2020)** + [OWASP JWT Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html).

---

## M7 — OIDC, authorization code, PKCE e ID token (2014)

### Idea
**OpenID Connect Core 1.0**, final aprobado el **26 de febrero de 2014**, es la capa de identidad sobre OAuth 2.0. Flujo *authorization code*: **RFC 6749 §4.1 (2012)**, código de un solo uso (si se reutiliza, la norma exige denegar y revocar, §4.1.2). **PKCE: RFC 7636, agosto de 2015.** El **ID token** es un JWT que dice *quién* es la persona y *cómo* se autenticó (`auth_time`, `amr`, `acr`) y **no sirve para acceder a recursos**.

### Guion para explicar
"El authorization code es el cupón de un solo uso que cambia un artefacto público —lo que viaja por el navegador— por uno privado. PKCE le agrega un candado: aunque te roben el código, no lo podés canjear sin el verificador. Y el ID token es el DNI que te muestran en la puerta, no el pase que te ponen en la muñeca para entrar al recinto."

### Ejemplo que puedo hacer (flujo, sin llamar a sistemas de terceros)
Con tu propio lab (Keycloak local, o el proyecto de práctica):
```
1) /authorize?response_type=code&client_id=lab&redirect_uri=http://localhost/cb
   &scope=openid&state=RANDOM&code_challenge=...&code_challenge_method=S256
2) el usuario (vos) se autentica en el lab
3) /cb?code=XXXX&state=RANDOM
4) POST /token  code=XXXX + code_verifier=...  -> access_token, id_token, refresh_token
```
Decodificá el **id_token** localmente y mirá `iss`, `aud`, `auth_time`, `amr`, `nonce`.

### Vulnerabilidades y cómo comprobarlas
| Vulnerabilidad | Cómo se comprueba (lab propio / tu integración) |
|---|---|
| Sin PKCE → código interceptable | Repetí el flujo **de tu lab** sin `code_challenge` e intentá canjear el código con otro cliente |
| `redirect_uri` laxa | En tu lab, probá un `redirect_uri` no registrado (p. ej. un subpath o dominio parecido) |
| Falta de `state` → CSRF | Iniciá el login y manipulá/eliminá el `state`: ¿acepta la respuesta? |
| Falta de `nonce` → replay del ID token | Reutilizá un ID token viejo en tu cliente y verificá si valida `nonce`/`auth_time` |
| *Mix-up attack* | En lab con dos IdP, cruzá respuestas entre proveedores |
| ID token usado como access token | Probá mandar el ID token al endpoint de recursos de tu lab: debe rechazarse |
| Rate-limit en login | Enviá N intentos de tu usuario de práctica y medí bloqueo |

### Defensa
PKCE obligatorio (lo exige **RFC 9700**), `redirect_uri` exacta, `state` y `nonce`, validar `iss`/`aud`/`exp`/`nonce` en el RP, no usar el ID token como access token.

---

## M8 — Refresh token (2012)

### Idea
Token de vida larga que **sólo** se usa contra el endpoint de token para obtener nuevos access tokens. **RFC 6749 §§1.5 y 6 (octubre de 2012)**; rotación sugerida en **§10.4**; **RFC 9700 (enero de 2025)** la exige para clientes públicos. Revocación: **RFC 7009, octubre de 2013**.

### Guion para explicar
"El access token es el boleto de la función; el refresh token es la acreditación que te deja pedir uno nuevo sin volver a la taquilla. La rotación convierte al refresh en un artefacto de un solo uso: si un atacante lo usa, el legítimo lo delata."

### Ejemplo que puedo hacer
En tu lab: guardá el refresh token, pedí un access token nuevo y observá si el refresh **cambia** (rotación) y si el viejo queda **inválido** (detección de reuso).

### Vulnerabilidades y cómo comprobarlas
| Vulnerabilidad | Cómo se comprueba (lab/tu integración) |
|---|---|
| Sin rotación | Reutilizá el mismo refresh token dos veces: si ambas funcionan, no hay rotación |
| Sin detección de reuso | Usá el refresh viejo después de rotar: si sigue vivo, no hay detección |
| Vida infinita | Verificá si hay `exp` o política de caducidad absoluta |
| Almacenamiento inseguro | En tu app, buscá el refresh en `localStorage`/almacenamiento sin cifrar del cliente |
| Refresh usado contra la API de recursos | Mandá el refresh a un endpoint de recursos de tu lab: debe rechazarse |

### Defensa
Rotación + detección de reuso, vida absoluta, binding al cliente, almacenamiento seguro, revocación en logout/cambio de contraseña.

---

## M9 — mTLS y DPoP (sender-constrained) (2020 / 2023)

### Idea
Atar el token a su portador. **mTLS + token atado a certificado: RFC 8705, febrero de 2020.** **DPoP: RFC 9449, octubre de 2023.** Con DPoP, el cliente firma cada request con su clave privada; el token sólo sirve presentado con esa prueba.

### Guion para explicar
"Si el problema del bearer es que cualquiera que lo tenga lo usa, la solución es exigir algo más que la posesión. mTLS ata el token al certificado; DPoP ata el token a una clave privada que el cliente prueba en cada request. Es la idea de OAuth 1.0, pero bien integrada. RFC 9700 (2025) ya los recomienda."

### Ejemplo que puedo hacer
DPoP — construí una prueba **conceptual** con Python (sin servidor real):
```python
# La prueba DPoP es un JWT firmado por el CLIENTE con su clave privada
# Header típico: {"typ":"dpop+jwt","alg":"ES256","jwk":{...}}
# Claims: jti (único), htm (método), htu (URL), iat
# El servidor rechaza si htm/htu no coinciden con el request, o si el jti se repite
```
Para una prueba real y segura, levantá **Keycloak en Docker** (soporta DPoP) y hacé el flujo contra tu propio Keycloak.

### Vulnerabilidades y cómo comprobarlas
| Vulnerabilidad | Cómo se comprueba (lab propio) |
|---|---|
| DPoP sin validar `htm`/`htu` | Cambiá el método o la URL del request manteniendo la prueba: ¿lo acepta? |
| Replay de la prueba (`jti`) | Reenviá la misma prueba dos veces: debe rechazarse |
| `ath` ausente | Presentá el access token sin atar la prueba al token (`ath` = hash del access token) |
| Nonce de servidor ignorado | Si el server exige nonce, probá sin él |
| mTLS mal configurado | En tu lab, probá presentar un token atado a un certificado **sin** el certificado: debe fallar |

### Defensa
Validar `htm`, `htu`, `jti` (anti-replay), `ath`, `alg` permitido; rotación de claves; y **RFC 9449 / RFC 8705**.

---

## M10 — OWASP API Security Top 10 (laboratorio)

Éste es el "atlas" para elegir qué probar. Cada ítem con su forma de comprobarlo **en un lab** ([OWASP API Security Top 10 – 2023](https://owasp.org/API-Security/editions/2023/en/0x11-t10/)).

| # | Riesgo | Cómo se comprueba (lab) | Herramienta |
|---|---|---|---|
| API1 | **BOLA** — Broken Object Level Authorization | Con **tu** token, cambiá el ID del objeto por otro del lab (`/api/pedidos/1234` → `5678`) y mirá si devuelve datos ajenos | Burp/Postman + ffuf |
| API2 | **Broken Authentication** | Login sin rate-limit, JWT sin validar, credenciales por defecto | jwt_tool, Burp Intruder |
| API3 | **BOPLA / Mass Assignment** | Mandá campos extra (`"rol":"admin"`, `"saldo":999`) y observá si se aplican | Postman |
| API4 | **Unrestricted Resource Consumption** | Paginación gigante, búsquedas costosas; medí CPU/latencia en tu lab | ab, k6 |
| API5 | **BFLA** — Broken Function Level Authorization | Con usuario normal, llamá endpoints de admin (`/admin/...`) | Postman |
| API6 | **Sensitive Business Flows** | Repetí un flujo (cupón, reintento de pago) más veces de las permitidas | script propio |
| API7 | **SSRF** | Endpoint que recibe una URL: apuntalo a `http://localhost`/metadatos en tu lab | Burp Collaborator |
| API8 | **Misconfiguration** | CORS `*`, errores verbosos, métodos no documentados, TLS débil | nuclei, ZAP |
| API9 | **Improper Inventory** | Versiones viejas (`/v1`, `/beta`, `/swagger`) expuestas | ffuf, gobuster |
| API10 | **Unsafe Consumption** | Confiar en datos de terceros (respuesta de otro servicio) sin validar | manual |

**Laboratorios oficiales/diseñados para romper:** [OWASP crAPI](https://owasp.org/projects/crapi), DVGA, [OWASP Juice Shop](https://owasp.org/www-project-juice-shop/), VAmPI, y los labs de [PortSwigger Web Security Academy](https://portswigger.net/web-security) (JWT, OAuth, BOLA).

---

## M11 — Caso ID Uruguay (laboratorio ético)

### Qué es
**ID Uruguay** es el proveedor de identidad del Estado uruguayo, gestionado por **AGESIC**. Se integra vía **OpenID Connect** y su documentación técnica muestra el *token endpoint* `/oidc/v1/token` con **`token_type` = "Bearer"**, un **ID token** en formato **JWT**, y llamadas a *UserInfo* con `Authorization: Bearer`.

- Documentación oficial: https://www.gub.uy/agencia-gobierno-electronico-sociedad-informacion-conocimiento/comunicacion/publicaciones/documentacion-tecnica-id-uruguay/documentacion-tecnica-id-uruguay/id-0
- Guía "Desarrollo seguro" (AGESIC): https://www.gub.uy/agencia-gobierno-electronico-sociedad-informacion-conocimiento/sites/agencia-gobierno-electronico-sociedad-informacion-conocimiento/files/Desarrollo%20seguro.pdf

### La línea ética, explícita
- **Vos podés** ejecutar el flujo completo **con tu propia cuenta** y **tu propio cliente de desarrollo** (o el de tu organización, con autorización interna). Eso incluye observar tus tokens, decodificar tu ID token y verificar la configuración de *tu* integración.
- **Vos NO podés** (sin autorización escrita de AGESIC): probar `redirect_uri` de otros clientes, atacar al IdP, automatizar intentos, intentar acceder a datos de otras personas, ni "probar qué pasa si cambio el token".
- Si querés evaluar el IdP en sí: coordiná con **AGESIC** y canalizá por **CERTuy** (`https://www.gub.uy/centro-nacional-respuesta-incidentes-seguridad-informatica/`).

### Verificación defensiva de tu integración (permitida y útil)

| Control | Cómo verificarlo en TU cliente | Resultado esperado | Referencia |
|---|---|---|---|
| **PKCE obligatorio** | Revisá tu `authorization` request: `code_challenge` + `code_challenge_method=S256` | Presente y verificado | RFC 7636 / RFC 9700 |
| **`redirect_uri` exacta** | Confirmá que registrás la URI exacta (sin comodines) y que tu app la valida | Coincidencia exacta | RFC 9700 |
| **`state` y `nonce`** | Verificá que tu app genera y valida ambos | Presentes, aleatorios, de un solo uso | OIDC Core |
| **Validación del ID token** | Tu código debe validar `iss`, `aud`, `exp`, `nonce` y la firma contra JWKS | Todo validado | OIDC Core |
| **ID token no se usa como access token** | Buscá en tu código si el ID token se envía a APIs | Nunca | OIDC Core |
| **Vida del access token** | Decodificá tu access token (si es JWT) y mirá `exp` | Corta y acorde al riesgo | RFC 9068 |
| **Rotación de refresh token** | Pedí dos veces seguidas: ¿el refresh cambia y el viejo se invalida? | Rotación + detección de reuso | RFC 9700 |
| **Revocación / logout** | Cerrá sesión y probá si tu token/refresh ya no sirve | Invalidado | RFC 7009 |
| **Transporte** | Verificá TLS y que no se acepten tokens por HTTP ni en query | Sólo HTTPS + header | RFC 9700 |
| **Almacenamiento en tu cliente** | ¿Dónde guarda tu app el token? (memoria/cookie `HttpOnly` mejor que `localStorage`) | Sin acceso por JS | OWASP |

### Guion de la demostración en clase (sin riesgo)
1. Mostrá la **documentación oficial** de ID Uruguay: `token_type: Bearer` e ID token JWT. *(Cero pruebas a nadie.)*
2. En **tu propio** login con tu cuenta, abrí DevTools → Network y mostrá la respuesta del *token endpoint* y la cabecera `Authorization: Bearer` **enmascarando el token**.
3. Decodificá **tu** ID token en https://jwt.io (es cliente: no viaja a ningún servidor) y leé `iss`, `aud`, `exp`, `auth_time`, `amr`.
4. Cerrá sesión y explicá por qué ese cierre debe invalidar los artefactos.
5. Frase: *"No tocamos ningún sistema ajeno: miramos un billete al portador en nuestra propia billetera."*

---

## 3. Entorno de laboratorio seguro

Levantá todo con Docker, sin tocar producción de nadie.

```bash
# OWASP crAPI (API intencionalmente vulnerable, con BOLA, JWT, etc.)
docker compose --file https://raw.githubusercontent.com/OWASP/crAPI/develop/deploy/docker/docker-compose.yml up -d

# DVGA (Damn Vulnerable GraphQL Application)
git clone https://github.com/dolevf/Damn-Vulnerable-GraphQL-Application && cd Damn-Vulnerable-GraphQL-Application
docker build -t dvga . && docker run -d -p 5013:5013 dvga

# Keycloak (OIDC/OAuth real para practicar PKCE, refresh, DPoP)
docker run -d -p 8080:8080 -e KEYCLOAK_ADMIN=admin -e KEYCLOAK_ADMIN_PASSWORD=admin quay.io/keycloak/keycloak:latest start-dev

# Juice Shop (web + API)
docker run -d -p 3000:3000 bkimminich/juice-shop
```

Herramientas: Burp Suite Community o ZAP, `jwt_tool`, `ffuf`/`gobuster`, `nuclei`, `gitleaks`/`ggshield`, Postman/Insomnia, `k6`/`ab`.

---

## 4. Glosario de atajos

| Término | Significado |
|---|---|
| **BOLA / IDOR** | Presentar token válido para acceder a objetos de otro (Api1 OWASP). |
| **BOPLA** | Mass assignment / controlar propiedades que no deberías (Api3). |
| **BFLA** | Llamar funciones para las que no tenés permiso (Api5). |
| **Replay** | Reutilizar un artefacto capturado (token, prueba) sin cambios. |
| **Sender-constrained** | Token que exige prueba de posesión (mTLS, DPoP). |
| **PKCE** | Candado del authorization code para clientes públicos (RFC 7636). |
| **`alg: none` / confusión de alg** | Clases de ataque sobre JWT al confiar en el header del token. |
| **AiTM** | Adversary-in-the-Middle: phishing que roba la sesión ya autenticada. |
| **Infostealer / pass-the-cookie** | Malware que roba cookies/tokens del navegador. |
| **MFA fatigue (T1621)** | Bombardeo de pushes hasta obtener aprobación. |
| **NHI** | Identidad no humana (servicio, CI, device). |
| **JWKS** | Conjunto de claves públicas para validar JWTs. |
| **Diff channel** | *Front channel* (navegador) vs *back channel* (servidor a servidor). |

---

## 5. Plantilla de reporte responsable

```
Asunto: [Divulgación Responsable] Posible <vulnerabilidad> en <sistema>

1. Resumen (2-3 líneas)
2. Impacto estimado (qué datos/acciones compromete)
3. Alcance probado (cuenta propia / cliente de prueba; qué NO se tocó)
4. Pasos de reproducción (mínimos, sin datos de terceros)
5. Evidencia (capturas enmascaradas, timestamps)
6. Recomendación de mitigación
7. Declaración: no se accedió a datos de terceros ni se alteró información
8. Contacto y disponibilidad para coordinar
```

En Uruguay, canal oficial: **CERTuy (AGESIC)** — https://www.gub.uy/centro-nacional-respuesta-incidentes-seguridad-informatica/

---

## 6. Bibliografía

**Normas IETF:** [RFC 2617](https://www.rfc-editor.org/rfc/rfc2617) · [RFC 7616](https://www.rfc-editor.org/rfc/rfc7616) · [RFC 6265](https://www.rfc-editor.org/rfc/rfc6265) · [RFC 5849](https://www.rfc-editor.org/rfc/rfc5849) · [RFC 6749](https://www.rfc-editor.org/rfc/rfc6749) · [RFC 6750](https://www.rfc-editor.org/rfc/rfc6750) · [RFC 6819](https://www.rfc-editor.org/rfc/rfc6819) · [RFC 7009](https://www.rfc-editor.org/rfc/rfc7009) · [RFC 7519](https://www.rfc-editor.org/rfc/rfc7519) · [RFC 7636](https://www.rfc-editor.org/rfc/rfc7636) · [RFC 7662](https://www.rfc-editor.org/rfc/rfc7662) · [RFC 8176](https://www.rfc-editor.org/rfc/rfc8176) · [RFC 8252](https://www.rfc-editor.org/rfc/rfc8252) · [RFC 8705](https://www.rfc-editor.org/rfc/rfc8705) · [RFC 8725](https://www.rfc-editor.org/rfc/rfc8725) · [RFC 9068](https://www.rfc-editor.org/rfc/rfc9068) · [RFC 9449](https://www.rfc-editor.org/rfc/rfc9449) · [RFC 9700](https://www.rfc-editor.org/rfc/rfc9700)

**Identidad y gobierno:** [OpenID Connect Core 1.0](https://openid.net/specs/openid-connect-core-1_0.html) · [NIST SP 800-63-4 (jul 2025)](https://pages.nist.gov/800-63-4/) · [Marco de Ciberseguridad de Uruguay (AGESIC)](https://www.gub.uy/centro-nacional-respuesta-incidentes-seguridad-informatica/tematica/gestion-ciberseguridad)

**OWASP y labs:** [API Security Top 10 2023](https://owasp.org/API-Security/editions/2023/en/0x11-t10/) · [JWT Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html) · [WSTG](https://owasp.org/www-project-web-security-testing-guide/) · [crAPI](https://owasp.org/projects/crapi) · [Juice Shop](https://owasp.org/www-project-juice-shop/) · [PortSwigger Academy](https://portswigger.net/web-security)

**Casos reales:** [Meta "View As" 2018](https://about.fb.com/news/2018/09/security-update/) · [Cloudflare/Okta 2022](https://blog.cloudflare.com/how-cloudflare-mitigated-yet-another-okta-compromise/) · [Codecov 2021](https://about.codecov.io/security-update/) · [GitGuardian Secrets Sprawl 2026](https://blog.gitguardian.com/the-state-of-secrets-sprawl-2026/) · [Uber 2022 (UpGuard)](https://www.upguard.com/blog/what-caused-the-uber-data-breach)

**Uruguay / ID Uruguay:** [Documentación técnica ID Uruguay (gub.uy)](https://www.gub.uy/agencia-gobierno-electronico-sociedad-informacion-conocimiento/comunicacion/publicaciones/documentacion-tecnica-id-uruguay/documentacion-tecnica-id-uruguay/id-0) · [Desarrollo seguro (AGESIC, PDF)](https://www.gub.uy/agencia-gobierno-electronico-sociedad-informacion-conocimiento/sites/agencia-gobierno-electronico-sociedad-informacion-conocimiento/files/Desarrollo%20seguro.pdf) · [CERTuy](https://www.gub.uy/centro-nacional-respuesta-incidentes-seguridad-informatica/)

