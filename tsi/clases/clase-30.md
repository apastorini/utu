# Clase 30: Autenticacion y Autorizacion Avanzada + OAuth2 / OpenID Connect

**Numero de clase:** 20
**Duracion:** 2 horas

## Objetivos de Aprendizaje

- Comprender los roles y flujos de OAuth2
- Diferenciar entre access token, refresh token e ID token
- Implementar OAuth2 con GitHub como provider en Flask
- Crear middleware de autorizacion con validacion de JWT y roles
- Identificar vulnerabilidades en flujos OAuth2 (PKCE, implicit flow)

## Contenido Detallado

### 1. OAuth2: Roles Fundamentales

OAuth2 define cuatro roles:

- **Resource Owner:** El usuario que posee los recursos (sus datos)
- **Client:** La aplicacion que solicita acceso a los recursos
- **Authorization Server:** El servidor que autentica al usuario y emite tokens
- **Resource Server:** El servidor que aloja los recursos protegidos

### 2. Flujos (Grant Types) de OAuth2

| Flujo | Uso | Seguridad |
|-------|-----|-----------|
| Authorization Code | Apps web con backend | Alto (con PKCE) |
| Implicit | SPAs (deprecado) | Bajo (token en URL) |
| Client Credentials | Comunicacion servidor-servidor | Medio |
| Resource Owner Password | Apps propias (legacy) | Bajo (expone credenciales) |
| Authorization Code + PKCE | Apps moviles y SPAs | Alto |

### 3. OpenID Connect (OIDC)

Capa de identidad sobre OAuth2 que agrega:
- **ID Token:** JWT que contiene informacion del usuario autenticado (claims)
- **UserInfo Endpoint:** API para obtener informacion adicional del usuario
- **Discovery:** Documento JSON con configuracion del proveedor

**Tokens en OIDC:**
- **Access Token:** Para acceder a recursos protegidos
- **Refresh Token:** Para obtener nuevos access tokens sin re-autenticar
- **ID Token:** JWT con informacion de identidad del usuario (solo OIDC)

### 4. JWT (JSON Web Tokens)

Estructura: `header.payload.signature`

```json
// Header
{"alg": "RS256", "typ": "JWT", "kid": "key-id-123"}

// Payload (claims)
{
  "sub": "1234567890",
  "name": "Juan Perez",
  "iat": 1516239022,
  "exp": 1516242622,
  "roles": ["admin", "usuario"],
  "iss": "https://auth.example.com"
}
```

### 5. PKCE (Proof Key for Code Exchange)

Protege el flujo Authorization Code contra ataques de interceptacion:

1. El cliente genera un `code_verifier` aleatorio (43-128 chars)
2. Calcula `code_challenge = SHA256(code_verifier)` (o plain)
3. Envia `code_challenge` en la solicitud de autorizacion
4. Al canjear el codigo, envia el `code_verifier`
5. El servidor verifica que coincidan

## Ejercicio 1: OAuth2 con GitHub como Provider en Flask

```python
# oauth_github.py - Autenticacion OAuth2 con GitHub en Flask
import os
import json
import requests
import secrets
from urllib.parse import urlencode

from flask import (
    Flask, request, redirect, url_for,
    session, jsonify, render_template_string
)

# ============================================================
# CONFIGURACION
# ============================================================
# Registrar una app en: https://github.com/settings/developers
# OAuth App -> New OAuth App
# Homepage URL: http://localhost:5000
# Authorization callback URL: http://localhost:5000/callback

CLIENT_ID = os.environ.get('GITHUB_CLIENT_ID', '')
CLIENT_SECRET = os.environ.get('GITHUB_CLIENT_SECRET', '')
REDIRECT_URI = 'http://localhost:5000/callback'

# URL de GitHub
GITHUB_AUTH_URL = 'https://github.com/login/oauth/authorize'
GITHUB_TOKEN_URL = 'https://github.com/login/oauth/access_token'
GITHUB_USER_URL = 'https://api.github.com/user'
GITHUB_EMAIL_URL = 'https://api.github.com/user/emails'

# ============================================================
# APP FLASK
# ============================================================

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(32))


@app.route('/')
def home():
    """Pagina principal."""
    usuario = session.get('usuario')
    if usuario:
        return f'''
        <h1>Bienvenido, {usuario['login']}!</h1>
        <img src="{usuario['avatar_url']}" width="100">
        <p>Nombre: {usuario.get('name', 'No disponible')}</p>
        <p>Email: {usuario.get('email', 'No disponible')}</p>
        <p>Bio: {usuario.get('bio', 'No disponible')}</p>
        <a href="/logout">Cerrar sesion</a>
        '''
    return '''
    <h1>Autenticacion con GitHub</h1>
    <p>Haz clic para iniciar sesion con GitHub:</p>
    <a href="/login/github">
        <button>Iniciar sesion con GitHub</button>
    </a>
    '''


@app.route('/login/github')
def login_github():
    """Inicia el flujo OAuth2 redirigiendo a GitHub."""

    # Generar y almacenar state para proteger contra CSRF
    state = secrets.token_urlsafe(16)
    session['oauth_state'] = state

    # Generar PKCE code_verifier y code_challenge
    code_verifier = secrets.token_urlsafe(64)
    session['code_verifier'] = code_verifier

    import hashlib
    import base64
    code_challenge = base64.urlsafe_b64encode(
        hashlib.sha256(code_verifier.encode()).digest()
    ).rstrip('=').decode()

    params = {
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'scope': 'read:user user:email',
        'state': state,
        'code_challenge': code_challenge,
        'code_challenge_method': 'S256'
    }

    auth_url = f'{GITHUB_AUTH_URL}?{urlencode(params)}'
    return redirect(auth_url)


@app.route('/callback')
def callback():
    """Callback que GitHub llama despues de la autenticacion."""

    # Verificar state contra CSRF
    error = request.args.get('error')
    if error:
        return f'Error de autenticacion: {error}', 400

    state_recibido = request.args.get('state')
    state_esperado = session.pop('oauth_state', None)

    if not state_recibido or state_recibido != state_esperado:
        return 'Error: State invalido (posible ataque CSRF)', 400

    # Obtener el codigo de autorizacion
    code = request.args.get('code')
    if not code:
        return 'Error: No se recibio el codigo de autorizacion', 400

    # Intercambiar el codigo por un access token
    code_verifier = session.pop('code_verifier', None)
    token_data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'code': code,
        'redirect_uri': REDIRECT_URI,
    }

    # Si teniamos PKCE, enviar el code_verifier
    if code_verifier:
        token_data['code_verifier'] = code_verifier

    headers = {'Accept': 'application/json'}
    response = requests.post(
        GITHUB_TOKEN_URL,
        data=token_data,
        headers=headers
    )

    if response.status_code != 200:
        return f'Error al obtener token: {response.text}', 400

    token_json = response.json()
    access_token = token_json.get('access_token')
    token_type = token_json.get('token_type', 'bearer')

    if not access_token:
        return f'Error: No se recibio access token: {token_json}', 400

    # Obtener informacion del usuario
    user_headers = {
        'Authorization': f'{token_type} {access_token}',
        'Accept': 'application/json'
    }

    user_response = requests.get(GITHUB_USER_URL, headers=user_headers)
    if user_response.status_code != 200:
        return f'Error al obtener usuario: {user_response.text}', 400

    usuario = user_response.json()

    # Obtener emails (el email principal puede estar en privado)
    email_response = requests.get(GITHUB_EMAIL_URL, headers=user_headers)
    if email_response.status_code == 200:
        emails = email_response.json()
        email_principal = next(
            (e['email'] for e in emails if e['primary']),
            usuario.get('email')
        )
        usuario['email'] = email_principal

    # Guardar usuario en sesion
    session['usuario'] = usuario
    session['access_token'] = access_token

    return redirect(url_for('home'))


@app.route('/logout')
def logout():
    """Cierra sesion."""
    session.clear()
    return redirect(url_for('home'))


@app.route('/api/me')
def api_me():
    """API protegida que requiere autenticacion."""
    usuario = session.get('usuario')
    if not usuario:
        return jsonify({'error': 'No autenticado'}), 401

    return jsonify({
        'login': usuario['login'],
        'name': usuario.get('name'),
        'email': usuario.get('email'),
        'avatar': usuario.get('avatar_url')
    })


if __name__ == '__main__':
    if not CLIENT_ID or not CLIENT_SECRET:
        print("=" * 60)
        print("ERROR: Configura las variables de entorno:")
        print("  set GITHUB_CLIENT_ID=tu_client_id")
        print("  set GITHUB_CLIENT_SECRET=tu_client_secret")
        print("=" * 60)
        print("\nRegistra tu app en: https://github.com/settings/developers")
    else:
        print("Iniciando servidor OAuth2 en http://localhost:5000")
        app.run(debug=True, port=5000)
```

**Configuracion en GitHub:**
1. Ir a https://github.com/settings/developers -> OAuth Apps -> New OAuth App
2. Homepage URL: `http://localhost:5000`
3. Authorization callback URL: `http://localhost:5000/callback`
4. Copiar Client ID y Client Secret
5. Ejecutar:
```bash
set GITHUB_CLIENT_ID=tu_client_id
set GITHUB_CLIENT_SECRET=tu_client_secret
python oauth_github.py
```

## Ejercicio 2: Middleware de Autorizacion con JWT y Roles

```python
# jwt_middleware.py - Middleware de autorizacion JWT con roles
import os
import json
import time
import jwt
from functools import wraps
from flask import Flask, request, jsonify, g

# ============================================================
# CONFIGURACION
# ============================================================

# En produccion, usar una clave asimetrica (RS256) o HMAC secreta
JWT_SECRET = os.environ.get('JWT_SECRET', 'mi-clave-secreta-cambiame-en-produccion')
JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION_HOURS = 24

# ============================================================
# UTILIDADES JWT
# ============================================================

class JWTManager:
    """Maneja creacion y validacion de tokens JWT."""

    @staticmethod
    def crear_token(user_id: str, username: str, roles: list) -> str:
        """
        Crea un JWT con informacion del usuario y roles.

        Payload:
            - sub: subject (user_id)
            - username: nombre de usuario
            - roles: lista de roles asignados
            - iat: issued at
            - exp: expiration
            - jti: JWT ID (unico)
        """
        payload = {
            'sub': user_id,
            'username': username,
            'roles': roles,
            'iat': int(time.time()),
            'exp': int(time.time()) + JWT_EXPIRATION_HOURS * 3600,
            'jti': os.urandom(8).hex()
        }
        return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    @staticmethod
    def verificar_token(token: str) -> dict:
        """
        Verifica y decodifica un JWT.

        Returns:
            dict con payload del token

        Raises:
            jwt.ExpiredSignatureError: Token expirado
            jwt.InvalidTokenError: Token invalido
        """
        try:
            payload = jwt.decode(
                token,
                JWT_SECRET,
                algorithms=[JWT_ALGORITHM],
                options={
                    'verify_exp': True,
                    'verify_iat': True,
                    'require': ['sub', 'exp', 'iat', 'roles']
                }
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise PermissionError("Token expirado")
        except jwt.InvalidTokenError as e:
            raise PermissionError(f"Token invalido: {str(e)}")


# ============================================================
# MIDDLEWARE DE AUTORIZACION
# ============================================================

def requerir_autenticacion(f):
    """
    Decorador que requiere autenticacion JWT.
    Extrae el token del header Authorization: Bearer <token>
    """
    @wraps(f)
    def decorada(*args, **kwargs):
        auth_header = request.headers.get('Authorization', '')

        if not auth_header.startswith('Bearer '):
            return jsonify({
                'error': 'Token de autenticacion requerido',
                'codigo': 'AUTH_REQUIRED'
            }), 401

        token = auth_header.split(' ', 1)[1]

        try:
            payload = JWTManager.verificar_token(token)
            # Almacenar datos del usuario en el contexto de la request
            g.usuario = payload
            g.user_id = payload['sub']
            g.user_roles = payload['roles']
        except PermissionError as e:
            return jsonify({
                'error': str(e),
                'codigo': 'TOKEN_INVALIDO'
            }), 401

        return f(*args, **kwargs)
    return decorada


def requerir_roles(roles_permitidos: list):
    """
    Decorador que verifica que el usuario tenga al menos uno de los roles.
    Debe usarse junto con @requerir_autenticacion.

    Uso:
        @app.route('/admin')
        @requerir_autenticacion
        @requerir_roles(['admin'])
        def admin_only():
            ...
    """
    def decorador(f):
        @wraps(f)
        def decorada(*args, **kwargs):
            roles_usuario = g.get('user_roles', [])

            if not any(rol in roles_usuario for rol in roles_permitidos):
                return jsonify({
                    'error': 'No tienes permisos para acceder a este recurso',
                    'codigo': 'FORBIDDEN',
                    'roles_requeridos': roles_permitidos,
                    'roles_usuario': roles_usuario
                }), 403

            return f(*args, **kwargs)
        return decorada
    return decorador


def requerir_permiso(permiso: str):
    """
    Decorador granular que verifica permisos especificos.
    Los permisos se definen como "recurso:accion" (ej: "usuarios:eliminar").
    """
    def decorador(f):
        @wraps(f)
        def decorada(*args, **kwargs):
            permisos_usuario = g.get('permisos', [])

            if permiso not in permisos_usuario:
                return jsonify({
                    'error': f'Permiso "{permiso}" requerido',
                    'codigo': 'PERMISO_DENEGADO'
                }), 403

            return f(*args, **kwargs)
        return decorada
    return decorador


# ============================================================
# APP FLASK DE EJEMPLO
# ============================================================

app = Flask(__name__)


@app.route('/login', methods=['POST'])
def login():
    """Endpoint de autenticacion que devuelve un JWT."""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'JSON requerido'}), 400

    username = data.get('username', '')
    password = data.get('password', '')

    # Simular verificacion de credenciales
    usuarios = {
        'admin': {'password': 'admin123', 'roles': ['admin', 'usuario'], 'nombre': 'Admin'},
        'user1': {'password': 'user123', 'roles': ['usuario'], 'nombre': 'Usuario 1'},
    }

    usuario = usuarios.get(username)
    if not usuario or usuario['password'] != password:
        return jsonify({'error': 'Credenciales invalidas'}), 401

    token = JWTManager.crear_token(
        user_id=username,
        username=usuario['nombre'],
        roles=usuario['roles']
    )

    return jsonify({
        'token': token,
        'token_type': 'Bearer',
        'expires_in': JWT_EXPIRATION_HOURS * 3600,
        'usuario': {
            'username': username,
            'nombre': usuario['nombre'],
            'roles': usuario['roles']
        }
    })


@app.route('/api/public')
def publico():
    """Endpoint publico, no requiere autenticacion."""
    return jsonify({'mensaje': 'Este es un endpoint publico'})


@app.route('/api/perfil')
@requerir_autenticacion
def perfil():
    """Endpoint que requiere autenticacion (cualquier usuario)."""
    return jsonify({
        'user_id': g.user_id,
        'roles': g.user_roles,
        'mensaje': 'Perfil de usuario'
    })


@app.route('/api/admin')
@requerir_autenticacion
@requerir_roles(['admin'])
def admin_panel():
    """Endpoint solo para administradores."""
    return jsonify({
        'mensaje': 'Panel de administracion',
        'usuario': g.usuario
    })


@app.route('/api/usuarios', methods=['GET'])
@requerir_autenticacion
@requerir_roles(['admin', 'usuario'])
def listar_usuarios():
    """Usuarios autenticados pueden ver la lista."""
    return jsonify({
        'usuarios': [
            {'id': 1, 'nombre': 'Juan'},
            {'id': 2, 'nombre': 'Maria'}
        ]
    })


@app.route('/api/usuarios/<int:user_id>', methods=['DELETE'])
@requerir_autenticacion
@requerir_roles(['admin'])
def eliminar_usuario(user_id):
    """Solo admin puede eliminar usuarios."""
    return jsonify({
        'mensaje': f'Usuario {user_id} eliminado'
    })


# ============================================================
# DEMOSTRACION
# ============================================================
if __name__ == '__main__':
    print("=" * 60)
    print("API con Autenticacion JWT y Roles")
    print("=" * 60)
    print("\nEndpoints:")
    print("  POST /login          - Autenticarse")
    print("  GET /api/public      - Publico")
    print("  GET /api/perfil      - Requiere auth")
    print("  GET /api/admin       - Solo admin")
    print("  GET /api/usuarios    - Auth + rol usuario/admin")
    print("  DELETE /api/usuarios/:id - Solo admin")
    print("\nPruebas con curl:")
    print('  # Login como admin:')
    print('  curl -X POST http://localhost:5000/login \\')
    print('    -H "Content-Type: application/json" \\')
    print('    -d "{\\"username\\":\\"admin\\",\\"password\\":\\"admin123\\"}"')
    print('\n  # Usar token:')
    print('  curl http://localhost:5000/api/admin \\')
    print('    -H "Authorization: Bearer <TOKEN>"')
    app.run(debug=True, port=5000)
```

## Ejercicio 3: Identificar Vulnerabilidades en Flujo OAuth2 Inseguro

```python
# oauth_inseguro.py - Flujo OAuth2 con vulnerabilidades (IDENTIFICARLAS)

# ============================================================
# VERSION INSEGURA - IDENTIFICAR LAS VULNERABILIDADES
# ============================================================

"""
VULNERABILIDADES EN EL FLUJO ABAJO DOCUMENTADO:

1. IMPLICIT FLOW: El access token se devuelve en el fragmento de la URL.
   Cualquier script en la pagina (incluso de terceros) puede leerlo.
   Solucion: Usar Authorization Code + PKCE.

2. SIN PKCE: No se genera code_verifier/code_challenge, permitiendo
   un ataque de interceptacion si alguien obtiene el codigo de autorizacion.

3. SIN STATE: No se valida el parametro state, permitiendo ataques CSRF
   donde un atacante inicia el flujo y el usuario completa la autenticacion
   sin saberlo.

4. REDIRECT URI SIN VALIDACION: No se valida que la redirect_uri coincida
   con la registrada, permitiendo open redirect attacks.

5. TOKEN EN FRAGMENTO DE URL: El token queda en el historial del navegador
   y puede ser expuesto en el Referer header.

6. SIN EXPIRACION DE TOKEN: El access token no tiene expiracion (sin 'exp').

7. SCOPE EXCESIVO: Se solicitan mas permisos de los necesarios.
"""

# Ejemplo de flujo implicito inseguro:
FLUJO_IMPLICITO_INSEGURO = """
1. El usuario hace clic en "Login con Proveedor"
2. Se redirige a:
   https://proveedor.com/auth?response_type=token
   &client_id=app123
   &redirect_uri=http://cliente.com/callback
   &scope=read+write+delete+admin
   (SIN state, SIN PKCE, scope excesivo)
3. El usuario se autentica en el proveedor
4. El proveedor redirige a:
   http://cliente.com/callback#access_token=eyJhbGci...
   &token_type=Bearer
   &expires_in=3600
   (TOKEN EN FRAGMENTO - cualquier script JS lo lee)
5. JavaScript del cliente lee el token del fragmento
6. CUALQUIER extension del navegador o script malicioso
   en la pagina puede leer tambien el token
"""


# ============================================================
# VERSION CORREGIDA - FLUJO AUTHORIZATION CODE + PKCE + STATE
# ============================================================

FLUJO_SEGURO = """
1. El usuario hace clic en "Login con Proveedor"
2. El cliente genera:
   - state (token aleatorio contra CSRF)
   - code_verifier (secreto, 43-128 chars)
   - code_challenge = SHA256(code_verifier) en base64url
3. Se redirige a:
   https://proveedor.com/auth?response_type=code
   &client_id=app123
   &redirect_uri=https://cliente.com/callback
   &scope=read
   &state=abc123def456
   &code_challenge=E9Melhoa2OhCJdB6PpA8B...
   &code_challenge_method=S256
4. El usuario se autentica en el proveedor
5. El proveedor redirige a:
   https://cliente.com/callback?code=eyJhbGciOiJSUzI1NiI...
   &state=abc123def456
6. El servidor valida que state coincida con el almacenado
7. El servidor intercambia code + code_verifier por tokens:
   POST https://proveedor.com/token
   grant_type=authorization_code
   &code=eyJhbGciOiJSUzI1...
   &code_verifier=dBjftJeZ4CVP-mB92K27uhbUJU1p1r...
   &client_id=app123
   &client_secret=********
   &redirect_uri=https://cliente.com/callback
8. El proveedor verifica:
   - El code_verifier coincide con code_challenge original
   - El client_id y client_secret son validos
   - La redirect_uri coincide con la registrada
9. Se devuelve access_token + refresh_token (opcional)
10. El servidor (no el navegador) almacena el token
"""


# ============================================================
# CHECKLIST DE SEGURIDAD PARA OAUTH2/OIDC
# ============================================================

def checklist_seguridad_oauth():
    """Lista de verificacion para implementar OAuth2/OIDC segura."""
    return """
CHECKLIST DE SEGURIDAD OAUTH2:

[ ] 1. Usar Authorization Code Flow + PKCE (NUNCA Implicit Flow)
[ ] 2. Generar y validar 'state' contra CSRF
[ ] 3. Generar code_verifier aleatorio y code_challenge=S256
[ ] 4. Validar que redirect_uri coincida exactamente con la registrada
[ ] 5. Solicitar solo los scopes minimos necesarios (principio de minimo privilegio)
[ ] 6. Validar 'aud' (audience) en el token JWT
[ ] 7. Validar 'iss' (issuer) en el token JWT
[ ] 8. Verificar firma del ID Token (JWT)
[ ] 9. Verificar expiracion del token
[ ] 10. Almacenar tokens en httpOnly cookies, no en localStorage
[ ] 11. Rotar refresh tokens en cada uso
[ ] 12. Usar HTTPS exclusivamente (nunca HTTP para tokens)
[ ] 13. No exponer client_secret en frontend
[ ] 14. Implementar rate limiting en endpoints de token
[ ] 15. Revocar tokens cuando el usuario cierra sesion

VULNERABILIDADES COMUNES:
- Token en URL (implicit flow)
- Sin validacion de state (CSRF)
- Sin PKCE (interceptacion de codigo)
- Sin validacion de redirect_uri (open redirect)
- Scopes excesivos (privilegio elevado)
- Token sin expiracion (token permanente)
- Almacenar token en localStorage (XSS -> token robado)
- No validar firma JWT (token falsificado)
- No validar audience (token reutilizado en otro servicio)
"""


def main():
    print("=" * 60)
    print("Analisis de Seguridad OAuth2")
    print("=" * 60)

    reporte = checklist_seguridad_oauth()
    print(reporte)

    print("\n--- EJERCICIO PRACTICO ---")
    print("Corrige el siguiente flujo inseguro:")
    print(FLUJO_IMPLICITO_INSEGURO)

    print("\nTu solucion debe implementar:")
    print("1. Authorization Code + PKCE")
    print("2. State parameter anti-CSRF")
    print("3. Validacion de redirect_uri")
    print("4. Scope minimo necesario")
    print("5. Token en backend (httpOnly cookie)")


if __name__ == '__main__':
    main()
```

## Preguntas y Respuestas

**P1: Cual es la diferencia entre OAuth2 y OpenID Connect?**
R: OAuth2 es un protocolo de autorizacion que permite a una aplicacion acceder a recursos en nombre de un usuario sin compartir credenciales. OpenID Connect es una capa de identidad sobre OAuth2 que agrega el ID Token (un JWT con informacion del usuario autenticado). OAuth2 da acceso (scopes), OIDC da identidad (claims como nombre, email).

**P2: Por que el Implicit Flow esta deprecado y que lo reemplaza?**
R: El Implicit Flow devuelve el access token en el fragmento de la URL (#access_token=...), lo que expone el token al historial del navegador, extensiones, y cualquier script en la pagina. Fue reemplazado por Authorization Code + PKCE, que intercambia un codigo temporal por tokens mediante una llamada backend-backend, manteniendo los tokens fuera del navegador.

**P3: Que es PKCE y contra que ataque protege?**
R: PKCE (Proof Key for Code Exchange) es un mecanismo donde el cliente genera un `code_verifier` secreto, envía un `code_challenge` (hash del verifier) al iniciar el flujo, y luego presenta el `code_verifier` al canjear el codigo. Protege contra ataques de interceptacion donde un atacante obtiene el codigo de autorizacion pero no puede canjearlo sin el verifier.

**P4: Que informacion contiene un JWT y como se valida su autenticidad?**
R: Un JWT contiene tres partes codificadas en base64url separadas por puntos: Header (algoritmo y tipo), Payload (claims como sub, exp, roles, issuer), y Signature (firma). La autenticidad se valida verificando la firma con la clave publica (RS256) o secreta (HS256) del emisor, y verificando que exp (expiration), nbf (not before), iss (issuer) y aud (audience) sean correctos.

**P5: Que son access token, refresh token e ID token y cual es la diferencia?**
R: Access token: credencial que permite acceder a recursos protegidos (vida corta, minutos/horas). Refresh token: credencial para obtener nuevos access tokens sin re-autenticar al usuario (vida larga, dias/meses). ID token: JWT que contiene informacion de identidad del usuario (solo en OIDC), no se usa para acceder a recursos.

**P6: Como funciona el parametro 'state' en OAuth2 y contra que protege?**
R: El parametro 'state' es un valor aleatorio unico generado por el cliente antes de redirigir al usuario al proveedor OAuth. Cuando el proveedor redirige de vuelta, incluye el mismo 'state'. El cliente verifica que coincida con el que genero. Esto protege contra CSRF (Cross-Site Request Forgery), evitando que un atacante fuerce a un usuario a completar un flujo OAuth2 sin su consentimiento.

**P7: Que es un ataque de "open redirect" en OAuth2 y como se previene?**
R: Ocurre cuando el servidor OAuth no valida estrictamente la `redirect_uri` y permite redirigir a URLs arbitrarias. Un atacante puede modificar la redirect_uri para que apunte a su servidor malicioso, capturando el codigo de autorizacion. Se previene validando que la redirect_uri coincida exactamente (caracter por caracter) con la URI registrada para ese client_id.

## Tarea / Lectura Recomendada

1. **RFC 6749 - The OAuth 2.0 Authorization Framework:**
   https://datatracker.ietf.org/doc/html/rfc6749

2. **RFC 7636 - Proof Key for Code Exchange (PKCE):**
   https://datatracker.ietf.org/doc/html/rfc7636

3. **OpenID Connect Specification:**
   https://openid.net/specs/openid-connect-core-1_0.html

4. **JWT.io - Debugger y documentacion:**
   https://jwt.io/

5. **Auth0 Learning Resources:**
   https://auth0.com/learn

6. **Tarea practica:** Implementar login con Google OAuth2 en Flask usando `google-auth` y validacion de ID Token JWT.

7. **Tarea practica:** Configurar Keycloak localmente y conectar una app Flask usando `python-keycloak`.


