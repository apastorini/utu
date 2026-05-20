# SEMANA 5: Seguridad Mobile

## Conceptos Fundamentales de Seguridad en Aplicaciones Moviles


---

## INDICE

1. [Introduccion a la Seguridad Mobile](#1-introduccion-a-la-seguridad-mobile)
2. [OWASP Mobile Top 10 — Las 10 Vulnerabilidades Mas Comunes](#2-owasp-mobile-top-10)
3. [OAuth 2.0 — Delegacion de Autenticacion](#3-oauth-20)
4. [Flujos OAuth 2.0](#4-flujos-oauth-20)
5. [PKCE — Proteccion contra Ataques de Intercepcion](#5-pkce)
6. [DPoP — Vinculacion de Token a Dispositivo](#6-dpop)
7. [Access Token, Refresh Token y Bearer Token](#7-tokens)
8. [API Keys — Cuando y Como Usarlas](#8-api-keys)
9. [Client Credentials — Comunicacion Servidor a Servidor](#9-client-credentials)
10. [Certificate Pinning — Fijacion de Certificado](#10-certificate-pinning)
11. [Certificate Attestation — Atestacion de Certificado](#11-certificate-attestation)
12. [HTTPS y Certificados SSL/TLS](#12-https-y-certificados)
13. [Certificado Digital de Persona Fisica](#13-certificado-de-persona-fisica)
14. [Firma de Aplicacion (App Signing)](#14-firma-de-aplicacion)
15. [Verificacion de Certificados al Descargar la App](#15-verificacion-de-certificados-al-descargar)
16. [Hash — Huellas Digitales](#16-hash)
17. [Ofuscacion de Codigo — Protegiendo la Logica](#17-ofuscacion)
18. [Seguridad de Canal — TLS/SSL en la Comunicacion](#18-seguridad-de-canal)
19. [Seguridad de Aplicacion — Proteccion en Tiempo de Ejecucion](#19-seguridad-de-aplicacion)
20. [Zona de Almacenamiento Seguro](#20-almacenamiento-seguro)
21. [Fastlane para CI/CD — Automatizacion de Firma y Distribucion](#21-fastlane)
22. [Resumen — Checklist de Seguridad Mobile](#22-checklist)

---

## 1. INTRODUCCION A LA SEGURIDAD MOBILE

### Por que la seguridad mobile es diferente

La seguridad mobile no es igual a la seguridad web por varias razones:

| Aspecto | Web | Mobile |
|---------|-----|--------|
| **Entorno** | Navegador controlado | Dispositivo del usuario (no controlado) |
| **Distribucion** | URL accesible desde cualquier lugar | Store / APK que se descarga e instala |
| **Codigo** | Corre en servidor, el cliente no ve la logica | El APK se puede decompilar (el codigo viaja al dispositivo) |
| **Estado** | Sin estado (stateless) | El dispositivo guarda estado local |
| **Actualizaciones** | Instantaneas (recargar pagina) | Lentas (pasar por store, usuario debe actualizar) |
| **Almacenamiento** | Cookies/Session | SharedPreferences, SQLite, Keystore, archivos |
| **Red** | HTTPS tipicamente | HTTPS + posibilidad de WiFi publico malicioso |

### Principios fundamentales

1. **Nunca confies en el cliente** — Todo lo que corre en el dispositivo del usuario puede ser manipulado
2. **Defensa en profundidad** — Varias capas de seguridad, no una sola
3. **Minimo privilegio** — Solo pedir los permisos necesarios, solo almacenar lo necesario
4. **Seguridad por disenio** — No agregar seguridad al final, pensar en ella desde la arquitectura
5. **Asumir siempre que te van a decompilar** — El codigo en el dispositivo es publico

---

## 2. OWASP MOBILE TOP 10 — LAS 10 VULNERABILIDADES MAS COMUNES

OWASP (Open Web Application Security Project) publica periodicamente el ranking de las vulnerabilidades mas criticas en aplicaciones moviles. Esta es la lista vigente:

### M1: Uso Incorrecto de Credenciales (Improper Credential Usage)

**Que es:** La app almacena o transmite credenciales (passwords, tokens, API keys) de forma insegura.

**Ejemplos:**
- Guardar password en SharedPreferences sin cifrar
- Incluir API keys hardcodeadas en el codigo
- Enviar tokens por HTTP en vez de HTTPS
- Almacenar tokens en logs

**Como prevenirlo:**
- Usar Android Keystore o EncryptedSharedPreferences
- Nunca hardcodear secrets (usar BuildConfig con gradle, o un backend)
- Siempre HTTPS

### M2: Seguridad Inadecuada en la Suplencia (Inadequate Supply Chain Security)

**Que es:** Usar librerias de terceros sin verificar su seguridad, o versiones vulnerables.

**Ejemplos:**
- Usar una libreria open source con vulnerabilidad conocida (Log4j, etc.)
- Descargar dependencias de fuentes no oficiales
- No actualizar librerias

**Como prevenirlo:**
- Usar herramientas como Snyk, OWASP Dependency-Check, o GitHub Dependabot
- Mantener las dependencias actualizadas
- Preferir librerias oficiales y mantenidas

### M3: Autenticacion y Autorizacion Inseguras (Insecure Authentication/Authorization)

**Que es:** El mecanismo de autenticacion puede ser evadido o es debil.

**Ejemplos:**
- Biometrica sin fallback a password
- Tokens que no expiran
- Autenticacion local insegura (solo del lado del cliente)
- No verificar que el usuario tenga permisos en cada request al servidor

**Como prevenirlo:**
- Autenticacion siempre del lado del servidor
- Tokens con expiracion corta + refresh token
- Validar permisos en cada endpoint del backend
- Biometrica como segundo factor, no unico

### M4: Fuga de Datos No Intencional (Unintended Data Leakage)

**Que es:** La app expone datos sensibles sin querer, a traves de mecanismos del sistema operativo.

**Ejemplos:**
- Datos aparecen en los logs del sistema (Logcat)
- Screenshots de la app quedan en la galeria (no usar `FLAG_SECURE`)
- Datos en clipboard compartidos con otras apps
- Datos en backups de Android

**Como prevenirlo:**
- No loguear datos sensibles (ni siquiera en debug)
- Usar `FLAG_SECURE` en pantallas con datos sensibles
- Limpiar clipboard al salir de la app
- Excluir datos sensibles de los backups con `android:fullBackupContent`

### M5: Cifrado Deficiente (Poor Cryptography)

**Que es:** Usar algoritmos criptograficos debiles o implementaciones incorrectas.

**Ejemplos:**
- Usar MD5 o SHA-1 para hash (rotos)
- Usar AES en modo ECB (no seguro)
- Usar RSA sin padding
- Generar numeros aleatorios con `Random()` en vez de `SecureRandom()`
- Usar cifrado propio (home-grown cryptography)

**Como prevenirlo:**
- No inventar criptografia. Usar las APIs de Android (Android Keystore, Jetpack Security)
- Algoritmos aceptables: AES-GCM, SHA-256, RSA-OAEP, ECDSA
- Usar `SecureRandom()` para generacion aleatoria
- Preferir `Tink` de Google o las recomendaciones de `Conscrypt`

### M6: Comunicacion Insegura (Insecure Communication)

**Que es:** Los datos se transmiten sin cifrar o con cifrado debil.

**Ejemplos:**
- HTTP en vez de HTTPS
- HTTPS con certificado autofirmado sin validacion
- No validar el nombre del host en el certificado
- Deshabilitar SSL Pinning
- Certificado vencido o revocado

**Como prevenirlo:**
- Siempre HTTPS
- Implementar Certificate Pinning
- Validar certificados (no aceptar todos)
- Usar `network_security_config.xml` para configurar dominios de confianza

### M7: Configuracion Incorrecta a Nivel de Plataforma (Improper Platform Usage)

**Que es:** Usar mal las APIs de seguridad que Android provee, o ignorarlas.

**Ejemplos:**
- No usar Android Keystore cuando esta disponible
- Usar `WebView` con JavaScript habilitado sin sanitizar entrada
- Exportar Activities/ContentProviders sin necesidad (`exported=true`)
- No chequear permisos en tiempo de ejecucion

**Como prevenirlo:**
- Conocer las APIs de seguridad de Android (Keystore, BiometricPrompt, EncryptedSharedPreferences)
- `android:exported="false"` por defecto, solo true cuando sea necesario
- Usar `AndroidManifest.xml` correctamente

### M8: Manipulacion Insegura de Datos (Insecure Data Storage)

**Que es:** Almacenar datos sensibles en el dispositivo sin proteccion.

**Ejemplos:**
- SharedPreferences sin cifrar
- SQLite database sin cifrar
- Archivos en almacenamiento externo (SD card)
- Cache de imagenes con datos sensibles

**Como prevenirlo:**
- EncryptedSharedPreferences para preferencias
- Room con SQLCipher para datos estructurados
- Android Keystore para claves
- No guardar datos sensibles en almacenamiento externo
- Cache con `Context.cacheDir` (no accesible por otras apps)

### M9: Configuracion Incorrecta del Servidor (Server-Side Insecurity)

**Que es:** El backend tiene vulnerabilidades que exponen datos de la app.

**Ejemplos:**
- API sin autenticacion
- API sin rate limiting (permiten ataques de fuerza bruta)
- Endpoints que devuelven mas datos de los necesarios
- Inyeccion SQL en el servidor

**Como prevenirlo:**
- Es responsabilidad del backend, pero la app mobile debe exigir estas practicas
- Validar las respuestas del servidor del lado del cliente
- No confiar en que el servidor siempre va a responder correctamente

### M10: Ingenieria Inversa (Reverse Engineering)

**Que es:** Decompilar el APK para entender la logica, robar secrets, o modificar el comportamiento.

**Ejemplos:**
- Decompilar con `jadx`, `apktool`, `dex2jar`
- Leer codigo ofuscado parcialmente
- Modificar el APK y re-firmarlo para inyectar codigo
- Extraer API keys del codigo

**Como prevenirlo:**
- Ofuscacion con ProGuard/R8
- No poner secrets en el codigo
- Verificar la firma de la app en tiempo de ejecucion
- Detectar emuladores/root y responder (con cuidado)
- Usar NDK para logica critica (mas dificil de decompilar)

---

## 3. OAUTH 2.0

### Que es OAuth 2.0

OAuth 2.0 es un **protocolo de autorizacion** que permite a una aplicacion obtener acceso limitado a los recursos de un usuario en otro servicio, sin necesidad de compartir la contrasenia del usuario.

**Analogia:** Es como un **valet parking**. Le das las llaves de tu auto al valet (token), pero solo por tiempo limitado, solo para estacionar (alcance limitado), y si el valet abusa, podes revocar las llaves.

### Actores en OAuth 2.0

```
┌──────────┐                    ┌──────────────┐
│          │                    │              │
│  Usuario  │                    │  App Mobile  │
│  (Dueño  │                    │  (Cliente)   │
│  Recurso)│                    │              │
└────┬─────┘                    └──────┬───────┘
     │                                 │
     │                                 ▼
     │                        ┌────────────────┐
     │                        │                │
     └───────────────────────▶│  Servidor de   │
                              │  Autorizacion  │
                              │                │
                              ├────────────────┤
                              │  Servidor de   │
                              │  Recursos      │
                              │  (API)         │
                              └────────────────┘
```

| Actor | Que es | Ejemplo |
|-------|--------|---------|
| **Resource Owner** | El usuario dueno de los datos | Vos, que tenes fotos en Google |
| **Client** | La app que quiere acceder | Tu app de notas que quiere subir fotos |
| **Authorization Server** | El que da los permisos | Google OAuth, Auth0 |
| **Resource Server** | El que tiene los datos | Google Photos API |

### Terminologia clave

| Termino | Significado |
|---------|-------------|
| **Client ID** | Identificador publico de la app (no es secreto) |
| **Client Secret** | Secreto compartido entre la app y el servidor de autorizacion |
| **Authorization Code** | Codigo temporal que se cambia por un Access Token |
| **Access Token** | Token que permite acceder a recursos protegidos |
| **Refresh Token** | Token para obtener nuevos Access Tokens sin pedir credenciales |
| **Scope** | Que permisos se estan solicitando (read, write, etc.) |
| **Redirect URI** | A donde vuelve el usuario despues de autorizar |
| **Grant** | Tipo de flujo de autorizacion |

---

## 4. FLUJOS OAUTH 2.0

Existen varios "grants" (flujos) en OAuth 2.0. Cada uno se usa en un contexto diferente.

### 4.1 Authorization Code Flow (Flujo de Codigo de Autorizacion)

**Es el mas seguro y recomendado para apps mobile.** El Access Token nunca viaja al dispositivo directamente; viaja un codigo temporal que se canjea en el servidor.

**Paso a paso:**

```
App Mobile              Authorization Server          Resource Server
    │                          │                           │
    │  1. Solicita login       │                           │
    │─────────────────────────▶│                           │
    │                          │                           │
    │  2. Abre navegador       │                           │
    │  (el usuario ve la       │                           │
    │   pagina de login        │                           │
    │   de Google/Facebook)    │                           │
    │                          │                           │
    │  3. Usuario ingresa      │                           │
    │  credenciales            │                           │
    │                          │                           │
    │  4. Authorization Code   │                           │
    │◀─────────────────────────│                           │
    │                          │                           │
    │  5. Code + Client Secret │                           │
    │─────────────────────────▶│                           │
    │                          │                           │
    │  6. Access Token +       │                           │
    │     Refresh Token        │                           │
    │◀─────────────────────────│                           │
    │                          │                           │
    │  7. Access Token         │                           │
    │─────────────────────────────────────────────────────▶│
    │                          │                           │
    │  8. Datos protegidos     │                           │
    │◀─────────────────────────────────────────────────────│
```

**Por que es seguro:** El `Authorization Code` se usa una sola vez y expira rapido. El `Client Secret` nunca se expone al navegador del usuario (solo viaja de servidor a servidor, o en apps mobile via PKCE).

### 4.2 Authorization Code Flow + PKCE (Recomendado para Mobile)

**Variante del Authorization Code Flow disenada especificamente para apps mobile y SPA (Single Page Applications).** Agrega PKCE (Proof Key for Code Exchange) para evitar ataques de intercepcion del codigo de autorizacion.

**Lo veremos en detalle en la seccion 5.**

### 4.3 Implicit Flow (Flujo Implicito — DEPRECADO)

**Ya no se recomienda.** En este flujo, el Access Token se devuelve directamente en la URL de redireccion, sin un codigo intermedio. Era usado por apps mobile y SPAs, pero se considera inseguro porque el token queda expuesto en la URL y en el historial del navegador.

**Remplazado por:** Authorization Code + PKCE.

### 4.4 Client Credentials Flow (Flujo de Credenciales de Cliente)

**No involucra a un usuario.** Es para comunicacion **servidor a servidor** o **app a API interna**. La app se autentica con su `Client ID` + `Client Secret` y obtiene un token directamente.

```
App Mobile / Servidor          Authorization Server
    │                                  │
    │  Client ID + Client Secret       │
    │─────────────────────────────────▶│
    │                                  │
    │  Access Token                    │
    │◀─────────────────────────────────│
    │                                  │
    │  Access Token en cada request    │
    │─────────────────────────────────▶│  (Resource Server)
```

**Cuando se usa:**
- La app necesita acceder a sus propios recursos (no los de un usuario)
- Microservicios que se autentican entre si
- Cron jobs o procesos automatizados

### 4.5 Resource Owner Password Credentials (ROPC) — DEPRECADO

El usuario entrega su usuario y contrasenia directamente a la app, y la app los cambia por un token. **No se recomienda para apps modernas** porque:
- La app ve las credenciales del usuario
- No soporta 2FA
- No se puede revocar parcialmente

### Resumen de flujos

| Flujo | Donde se usa | Tiene PKCE? | Seguridad |
|-------|-------------|-------------|-----------|
| Authorization Code | Web apps con backend | No necesario (secret en servidor) | Alta |
| Authorization Code + PKCE | **Apps mobile, SPAs** | **Si** | **Alta (recomendado)** |
| Implicit | Legacy, deprecado | No | Baja |
| Client Credentials | Server-to-server | No | Alta (no hay usuario) |
| ROPC | Legacy, deprecado | No | Baja |

---

## 5. PKCE (PROOF KEY FOR CODE EXCHANGE)

### Que es PKCE

PKCE (pronunciado "pixie") es una extension del protocolo OAuth 2.0 que protege el flujo Authorization Code contra ataques de intercepcion. Fue creado originalmente para apps mobile, donde no se puede almacenar un `Client Secret` de forma segura.

### El problema que resuelve

En el flujo Authorization Code normal, el `Client Secret` se usa para demostrar que la app que canjea el codigo es la misma que lo solicito. Pero en una app mobile:

- El `Client Secret` puede ser extraido del APK (decompilacion)
- Un atacante podria interceptar el `Authorization Code` (a traves de un esquema de URL personalizado malicioso, por ejemplo) y canjearlo con el `Client Secret` robado

### Como funciona PKCE

En vez de usar un `Client Secret`, PKCE genera un secreto dinamico llamado `code_verifier` y su hash llamado `code_challenge`.

```
App Mobile                          Authorization Server
    │                                        │
    │  1. Genera code_verifier (aleatorio)   │
    │     code_challenge = SHA256(verifier)  │
    │                                        │
    │  2. Solicita login + code_challenge    │
    │────────────────────────────────────────▶│
    │                                        │
    │  (usuario autoriza en navegador)       │
    │                                        │
    │  3. Authorization Code                 │
    │◀────────────────────────────────────────│
    │                                        │
    │  4. Authorization Code + code_verifier │
    │────────────────────────────────────────▶│
    │                                        │
    │  5. Servidor verifica:                  │
    │     SHA256(code_verifier) ==            │
    │     code_challenge?                     │
    │                                        │
    │  6. Access Token                       │
    │◀────────────────────────────────────────│
```

**Por que es seguro:**
- El `code_verifier` solo lo conoce la app que genero la solicitud
- Si un atacante intercepta el `Authorization Code`, no tiene el `code_verifier` y no puede canjearlo
- El `code_challenge` viaja en la solicitud inicial, pero es un hash (no se puede revertir para obtener el verifier)

### Niveles de PKCE

| Metodo | Que hace | Seguridad |
|--------|----------|-----------|
| `S256` | SHA-256 del code_verifier | Alta (recomendado) |
| `plain` | Envia el code_verifier directamente | Baja (no recomendado) |

Siempre usar `S256`.

---

## 6. DPOP (DEMONSTRATION OF PROOF OF POSSESSION)

### Que es DPoP

DPoP (a veces llamado PoP — Proof of Possession) es un mecanismo que permite **vincular un Access Token al dispositivo o cliente que lo solicito**. Esto evita que un token robado pueda ser usado desde otro dispositivo.

### El problema que resuelve

Un Access Token tradicional es un **Bearer Token**: cualquiera que tenga el token puede usarlo (como una llave fisica). Si un atacante intercepta el token (por un proxy malicioso, por ejemplo), puede hacer requests como si fuera el usuario legítimo.

### Como funciona DPoP

```
App Mobile                          API Server
    │                                        │
    │  1. Genera par de claves (priv/pub)    │
    │     Guarda privada en Keystore         │
    │                                        │
    │  2. Solicita token + clave publica     │
    │     (en header DPoP)                   │
    │────────────────────────────────────────▶│
    │                                        │
    │  3. Server emite token "vinculado"     │
    │     a esa clave publica                │
    │◀────────────────────────────────────────│
    │                                        │
    │  4. En cada request:                   │
    │     - Access Token                     │
    │     - DPoP Proof (firma del request    │
    │       con clave privada)               │
    │────────────────────────────────────────▶│
    │                                        │
    │  5. Server verifica:                   │
    │     - Token valido?                    │
    │     - Firma coincide con clave         │
    │       publica asociada al token?       │
    │                                        │
    │  6. Datos protegidos                   │
    │◀────────────────────────────────────────│
```

**Analogia:** El Bearer Token es como una tarjeta de acceso sin foto. Cualquiera que la encuentre puede usarla. DPoP es como una tarjeta con foto: solo la persona de la foto puede usarla.

### Diferencia entre Bearer y DPoP

| Aspecto | Bearer Token | DPoP Token |
|---------|-------------|------------|
| **Que demuestra** | Posesion del token | Posesion del token + clave privada |
| **Reutilizable desde otro dispositivo?** | Si | No |
| **Proteccion contra robo** | Ninguna | Alta |
| **Complejidad** | Baja | Alta |
| **Uso tipico** | APIs publicas | APIs financieras, salud, datos sensibles |

---

## 7. ACCESS TOKEN, REFRESH TOKEN Y BEARER TOKEN

### 7.1 Access Token

**Que es:** Un token que demuestra que tienes permiso para acceder a un recurso protegido. Es como una **credencial temporal**.

**Caracteristicas:**
- Tiene una **vida corta** (tipicamente 15-60 minutos)
- Se envia en cada request al servidor (en header `Authorization: Bearer <token>`)
- Contiene informacion del usuario, permisos (scopes) y expiracion
- El servidor lo valida sin necesidad de llamar a otro servicio (es autocon tenido)

**Formato mas comun:** **JWT** (JSON Web Token)

```
Header: { "alg": "RS256", "typ": "JWT" }
Payload: {
  "sub": "user_123",
  "name": "Juan Perez",
  "iat": 1715000000,
  "exp": 1715003600,
  "scope": "read write"
}
Signature: [firmado con clave privada del servidor]
```

El JWT es un string con tres partes separadas por puntos, codificado en Base64URL:
```
eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJ1c2VyXzEyMyJ9.firma_aqui
```

### 7.2 Refresh Token

**Que es:** Un token que permite obtener **nuevos Access Tokens** sin que el usuario tenga que volver a autenticarse.

**Caracteristicas:**
- Tiene una **vida larga** (dias, semanas, o incluso meses)
- Se almacena de forma **segura** (en el dispositivo, no en el servidor)
- Se envia SOLO al servidor de autorizacion, no a la API de recursos
- Puede ser **revocado** (si el usuario cierra sesion, el servidor invalida el Refresh Token)

**Flujo tipico:**

```
App Mobile                          Auth Server
    │                                        │
    │  (tiene Access Token expirado)         │
    │                                        │
    │  1. Request con Access Token           │
    │  (expirado → 401 Unauthorized)         │
    │◀────────────────────────────────────────│
    │                                        │
    │  2. Refresh Token                      │
    │────────────────────────────────────────▶│
    │                                        │
    │  3. Nuevo Access Token                 │
    │  (opcionalmente nuevo Refresh Token)   │
    │◀────────────────────────────────────────│
    │                                        │
    │  4. Retry request con nuevo token      │
    │────────────────────────────────────────▶│
```

**Rotation de Refresh Token:** Algunos servidores, al dar un nuevo Access Token, tambien renuevan el Refresh Token (rotation). El viejo Refresh Token deja de ser valido. Esto previene que un Refresh Token robado pueda ser usado por siempre.

### 7.3 Bearer Token

**Que es:** Un tipo de Access Token donde la simple **posesion** del token es suficiente para acceder al recurso. Quien tenga el token (the bearer) puede usarlo.

**Por que se llama Bearer:**
- No necesitas demostrar que sos el dueno del token
- Solo necesitas "portarlo" (bear it)
- Como efectivo: quien lo tiene, lo gasta

**Seguridad de Bearer Tokens:**
- Usar siempre HTTPS (si no, el token viaja en texto plano)
- Token de corta duracion
- Almacenarlo seguro en el dispositivo
- No loguearlo, no mostrarlo en la UI

---

## 8. API KEYS

### Que es una API Key

Una API Key es un identificador unico (un string) que se asigna a un cliente (app, desarrollador, empresa) para controlar el acceso a una API. Es como una **credencial de aplicacion**, no de usuario.

### Donde se usan

- APIs publicas (Google Maps, Weather API, TMDB, NewsAPI)
- Servicios de pago por uso
- Identificacion de que app esta haciendo el request

### API Key vs OAuth 2.0

| Aspecto | API Key | OAuth 2.0 |
|---------|--------|-----------|
| **Que identifica** | La aplicacion | El usuario + la aplicacion |
| **Expira** | Generalmente no | Si, tokens expiran |
| **Revocable** | Si (manual) | Si (automatico + manual) |
| **Permisos granulares** | No (todo o nada) | Si (scopes) |
| **Rotacion** | Manual | Automatica (refresh) |

### Problemas de seguridad con API Keys en mobile

**El problema mas grande:** Una API Key incluida en una app mobile puede ser **extraida por decompilacion**. Cualquiera puede descargar el APK, decompilarlo con `jadx`, y encontrar la API Key.

**Practicas recomendadas:**

1. **No poner API Keys en el codigo** — No hardcodear strings, no en `BuildConfig`, no en `gradle.properties`
2. **Proxy server:** No exponer la API Key directamente. La app se comunica con tu servidor, y tu servidor se comunica con la API externa usando la Key. La Key nunca sale de tu servidor.
3. **Restringir por dominio/IP:** Configurar la API externa para que solo acepte requests desde tu servidor (no desde dispositivos moviles)
4. **Ofuscacion como ultimo recurso:** Si no hay otra opcion, ofuscar y no usar nombres obvios (`apiKey`, `secret`)
5. **Rotation periodica:** Si inevitablemente tenes una Key en la app, poder rotarla facilmente

---

## 9. CLIENT CREDENTIALS

### Que es Client Credentials

Es un flujo de OAuth 2.0 donde la **aplicacion se autentica a si misma**, no a un usuario. Se usa para comunicacion **servidor a servidor** o **app a API de backend**.

### Cuando se usa en mobile

Aunque el flujo Client Credentials tipicamente es para servidores, una app mobile puede usarlo para:

- Autenticarse contra su propio backend antes de que el usuario haga login
- Obtener tokens para funcionalidades que no requieren usuario (feature flags, configuracion remota)
- Servicios de analytics, crash reporting

### Como funciona

```
App Mobile                          Auth Server
    │                                        │
    │  POST /token                           │
    │  grant_type=client_credentials          │
    │  client_id=mi_app                      │
    │  client_secret=...                     │
    │────────────────────────────────────────▶│
    │                                        │
    │  Access Token                          │
    │  {                                     │
    │    "access_token": "eyJ...",           │
    │    "token_type": "Bearer",             │
    │    "expires_in": 3600                  │
    │  }                                     │
    │◀────────────────────────────────────────│
```

### Riesgo en mobile

El `client_secret` en una app mobile corre el mismo riesgo que las API Keys: puede ser extraido. Por eso, en mobile se recomienda:

- No usar Client Credentials directamente desde la app si el secret es sensible
- Usar un backend proxy que tenga el secret
- O usar client_id sin secret (public client) con restricciones de IP o fingerprint de la app

---

## 10. CERTIFICATE PINNING

### Que es Certificate Pinning

Certificate Pinning (fijacion de certificado) es una tecnica que asocia un certificado o clave publica especifica con un servidor. La app verifica que el certificado del servidor sea EXACTAMENTE el que espera, no solo que este firmado por una CA confiable.

### El problema que resuelve

Normalmente, HTTPS funciona asi:

```
App ───HTTPS───▶ Servidor
                  │
                  ▼
        Certificado firmado por
        una CA (Certificate Authority)
                  │
                  ▼
        Si la CA confia en el cert,
        la conexion es segura
```

El problema: **Las CAs pueden ser comprometidas.** Si una CA emite un certificado falso para tu dominio, un atacante puede hacer un ataque "Man-in-the-Middle" (MitM) interceptando todo el trafico.

**Ataque MitM sin Pinning:**

```
App ───▶ Proxy Atacante ───▶ Servidor
          │                       │
          │ Cert falso            │ Cert real
          │ firmado por CA        │ firmado por CA
          │ comprometida          │ legitima
          ▼                       ▼
        App confia              Servidor confia
        (no sabe que es         (no sabe del proxy)
         un proxy)
```

### Como funciona Certificate Pinning

La app tiene "incrustado" (embedded) el certificado o la clave publica del servidor. Cuando se conecta, verifica que el certificado del servidor coincida con el que tiene almacenado.

```
App ───▶ Proxy Atacante ───▶ Servidor
  │          │
  │          ▼
  │   Cert falso
  │   (no coincide con
  │    el pin almacenado)
  │          │
  ▼          ▼
App rechaza la conexion
(error SSL/TLS)
```

### Tipos de Pinning

| Tipo | Que se guarda | Que verifica |
|------|--------------|--------------|
| **Certificate Pinning** | El certificado completo | Que el cert sea exactamente el mismo |
| **Public Key Pinning** | Solo la clave publica | Que la clave publica coincida (permite renovar el cert sin cambiar la clave) |

### Implementacion tipica

En Android, se configuran "pins" (huellas digitales SHA-256 de los certificados) para cada dominio. Si el certificado del servidor no coincide con ningun pin, la conexion se rechaza.

### Consideraciones importantes

| Aspecto | Detalle |
|---------|---------|
| **Que hacer si el certificado expira** | Si tenes Certificate Pinning y el cert expira, los usuarios no podran usar la app hasta que la actualicen |
| **Solucion: Public Key Pinning** | Pinear la clave publica en vez del cert. Podes renovar el cert con la misma clave publica sin actualizar la app |
| **Solucion: Multiple pins** | Tener 2 pins: el actual + uno de respaldo (backup pin). Si cambias de CA, seguis teniendo el backup |
| **Actualizacion** | La app debe poder actualizar los pins via configuracion remota (con precaucion: si el mecanismo de actualizacion es inseguro, rompe el proposito) |

### Alternativa moderna: Network Security Config

Android 7+ soporta `network_security_config.xml` donde se puede configurar:

- Que dominios permitir
- Debug overrides
- Certificate Pinning declarativo

**Ventaja:** No requiere codigo, es configuracion XML.

---

## 11. CERTIFICATE ATTESTATION (ATESTACION DE CERTIFICADO)

### Que es

Certificate Attestation es un mecanismo donde el **servidor verifica que la app que se esta conectando es legitima y no ha sido modificada**. Mientras que Certificate Pinning verifica al servidor, Attestation verifica al cliente (la app).

### Android Play Integrity API

Antes llamada SafetyNet Attestation, es el servicio de Google que permite verificar la integridad de una app Android.

**Que verifica:**

| Aspecto | Que chequea |
|---------|-------------|
| **Firma de la app** | Que la app este firmada con la misma key que la version publicada en Play Store |
| **Dispositivo** | Que el dispositivo no este rooteado |
| **Integridad** | Que la app no haya sido modificada (reempaquetada) |
| **Licencia** | Que la app venga de Play Store (no de un APK sideload) |

### Como funciona

```
App Mobile                Play Integrity API           Tu Servidor
    │                            │                         │
    │ 1. Solicita token           │                         │
    │───────────────────────────▶│                         │
    │                            │                         │
    │ 2. Verifica integridad     │                         │
    │    del dispositivo         │                         │
    │    y la firma de la app    │                         │
    │                            │                         │
    │ 3. Token firmado por       │                         │
    │    Google                   │                         │
    │◀───────────────────────────│                         │
    │                            │                         │
    │ 4. Envia token a tu        │                         │
    │    servidor                 │                         │
    │────────────────────────────────────────────────────▶│
    │                            │                         │
    │                            │  5. Verifica firma      │
    │                            │     de Google           │
    │                            │     contra clave        │
    │                            │     publica de Google   │
    │                            │                         │
    │                            │  6. Response:           │
    │                            │     valido / invalido   │
    │◀────────────────────────────────────────────────────│
```

### Que responder cuando el dispositivo no pasa la verificacion

- Opcion suave: Mostrar un warning "No se puede verificar la integridad del dispositivo"
- Opcion media: Bloquear funcionalidades sensibles (pagos, datos personales)
- Opcion dura: No permitir usar la app

### Limitaciones

- Requiere Google Play Services
- No funciona en dispositivos sin Google (China, Kindle, etc.)
- No funciona en el emulador (o requiere configuracion especial)
- Agrega latencia a la primera conexion
- No es gratis a escala masiva (tiene costo despues de cierto volumen)

---

## 12. HTTPS Y CERTIFICADOS SSL/TLS

### Que es HTTPS

HTTPS (HTTP Secure) es la version cifrada de HTTP. Usa TLS (Transport Layer Security) para cifrar la comunicacion entre la app y el servidor.

### Como funciona TLS

```
App Mobile                                         Servidor
    │                                                  │
    │  1. ClientHello                                  │
    │     (versiones TLS, cifrados soportados)         │
    │─────────────────────────────────────────────────▶│
    │                                                  │
    │  2. ServerHello                                  │
    │     (TLS version, cifrado elegido) +             │
    │     Certificado (con clave publica)              │
    │◀─────────────────────────────────────────────────│
    │                                                  │
    │  3. Verifica el certificado:                     │
    │     - Firma de CA?                               │
    │     - Host coincide?                             │
    │     - No expirado?                               │
    │     - No revocado?                               │
    │                                                  │
    │  4. Genera clave simetrica                       │
    │     (Pre-Master Secret)                          │
    │     La cifra con clave publica del servidor      │
    │─────────────────────────────────────────────────▶│
    │                                                  │
    │  5. Servidor descifra con su clave privada       │
    │     Ambos tienen la clave simetrica              │
    │                                                  │
    │  6. Comunicacion cifrada con clave simetrica     │
    │◀════════════════════════════════════════════════▶│
```

### Tipos de certificados SSL/TLS

| Tipo | Verificacion | Costo | Uso |
|------|-------------|-------|-----|
| **DV (Domain Validated)** | Solo que controlas el dominio | Gratis (Let's Encrypt) | APIs, sitios publicos |
| **OV (Organization Validated)** | Verifica la organizacion | Medio | Sitios comerciales |
| **EV (Extended Validation)** | Verificacion exhaustiva de la empresa | Alto | Bancos, gobierno |

### Certificado autofirmado vs CA

| Aspecto | Autofirmado | Firmado por CA |
|---------|------------|----------------|
| **Quien lo firma** | Vos mismo | Una autoridad de confianza |
| **Costo** | Gratis | Gratis (Let's Encrypt) o pago |
| **Seguridad** | El cifrado es igual | El cifrado es igual |
| **Confianza** | Solo si la app lo acepta explicitamente | Confianza automatica |
| **Uso en produccion** | No recomendado | Si |

**En produccion, siempre usar un certificado firmado por una CA de confianza.** Los certificados autofirmados solo son utiles para desarrollo/testing.

### Chain of Trust (Cadena de Confianza)

```
Root CA (ej: DigiCert, Let's Encrypt)
  └── Firmado por Root CA
       │
       ▼
      Intermediate CA
       └── Firmado por Intermediate CA
            │
            ▼
           Tu certificado SSL
```

El dispositivo Android tiene una lista de Root CAs confiables. Cuando recibe un certificado, verifica:

1. El certificado esta firmado por una Intermediate CA
2. La Intermediate CA esta firmada por una Root CA
3. La Root CA esta en la lista de confianza del dispositivo
4. El nombre del host coincide con el dominio del certificado
5. El certificado no esta vencido
6. El certificado no esta revocado (opcional, via CRL u OCSP)

### Certificados en Android

Android actualiza su lista de CAs confiables a traves de **Google Play Services** y las actualizaciones del sistema. Pero apps individuales pueden **restringir que CAs aceptan** usando `network_security_config.xml`.

---

## 13. CERTIFICADO DIGITAL DE PERSONA FISICA

### Que es

Un **certificado digital de persona fisica** es un documento electronico que vincula una identidad real (una persona) con una clave publica. Es el equivalente digital de un DNI o pasaporte.

### Diferencia con certificado SSL

| Aspecto | Certificado SSL | Certificado Persona Fisica |
|---------|----------------|---------------------------|
| **Que identifica** | Un dominio (servidor) | Una persona |
| **Quien lo emite** | CA (Let's Encrypt, DigiCert) | Autoridad de registro (Renaper, AFIP, etc.) |
| **Para que sirve** | Cifrar comunicacion | Firmar documentos, identidad digital |
| **Ejemplos** | El candado en el navegador | Firma digital de contratos, DNI digital |

### Usos en mobile

1. **Firma de documentos** — La app usa el certificado para firmar digitalmente un documento desde el celular
2. **Autenticacion fuerte** — Acceder a un servicio usando el certificado como segundo factor
3. **Identidad digital** — Demostrar quien sos sin compartir datos personales

### Como se usa en Android

Android soporta almacenar certificados de persona en el **Key Store** del sistema (tanto hardware como software). Las apps pueden:

- Acceder a certificados instalados por el usuario
- Usar la biometria (huella, rostro) para autorizar el uso del certificado
- Firmar datos con la clave privada del certificado (sin exponer la clave)

### Ejemplos reales

- **DNI Digital** en Argentina: Certificado emitido por Renaper que permite identificarse desde el celular
- **AFIP / ARCA**: Certificados para acceder a servicios tributarios
- **Firma de contratos**: Apps como DocuSign usan certificados para firma electronica avanzada

---

## 14. FIRMA DE APLICACION (APP SIGNING)

### Que es la firma de APK

Toda app Android debe estar **firmada digitalmente** antes de ser instalada en un dispositivo. La firma garantiza:

1. **Autenticidad:** La app viene de quien dice venir
2. **Integridad:** La app no fue modificada despues de firmada
3. **Actualizaciones seguras:** Solo el dueno de la key de firma puede publicar actualizaciones

### Como funciona

```
APK sin firmar
    │
    ▼
  Se calcula hash del contenido del APK
    │
    ▼
  Se firma el hash con la clave privada del desarrollador
    │
    ▼
  Se empaqueta la firma + certificado (clave publica) en el APK
    │
    ▼
  APK firmado listo para distribuir
```

Cuando el usuario instala el APK:

```
Dispositivo Android recibe APK firmado
    │
    ▼
  Extrae la firma + certificado del APK
    │
    ▼
  Verifica: el hash firmado coincide con el hash del APK?
    │
    ▼
  Verifica: el certificado es confiable?
    (Para apps de Play Store, Google la verifica)
    │
    ▼
  Si todo OK → instala
  Si no → rechaza
```

### Tipos de firmas

| Esquema | Desde Android | Caracteristicas |
|---------|---------------|-----------------|
| **v1 (JAR signing)** | 1.0 | Legacy, basado en firma de JAR |
| **v2 (APK Signature Scheme v2)** | 7.0 | Firma de todo el APK (mas seguro) |
| **v3 (APK Signature Scheme v3)** | 9.0 | Soporta rotacion de key de firma |
| **v4** | 11.0 | Firma incremental para streaming de APK |

**Recomendacion:** Firmar con v2 + v3 minimo.

### Google Play App Signing

Google Play ofrece un servicio donde:
- Vos subis un **Upload Key** (para firmar APKs que subis a Play Console)
- Google firma el APK final con un **App Signing Key** (que solo Google tiene)
- Si perdes tu Upload Key, Google puede generarte una nueva

**Ventaja:** Si perdes la key de firma, Google puede recuperarla. Sin Play Signing, perder la key significa no poder actualizar la app nunca mas.

### Rotacion de Key de Firma

Android 9+ permite cambiar la key de firma de una app (key rotation). Esto es util si:

- La key se ve comprometida
- Queres migrar a un algoritmo mas fuerte
- Perdiste la key anterior

La rotacion solo es posible con v3 signing y la app debe estar firmada con la key anterior + la nueva.

---

## 15. VERIFICACION DE CERTIFICADOS AL DESCARGAR LA APP

### Que pasa cuando descargas una app

Cuando un usuario descarga una app de Google Play Store, ocurre esto:

```
Usuario busca app en Play Store
    │
    ▼
  Play Store verifica:
  - La app esta firmada por el desarrollador
  - La app no tiene malware conocido (Play Protect)
  - El desarrollador es quien dice ser (verificado por Google)
    │
    ▼
  Descarga el APK firmado por Google Play Signing
    │
    ▼
  Instalador de Android (PackageInstaller):
  - Verifica la firma v2/v3 del APK
  - Verifica que coincida con la firma de la app ya instalada
    (si es una actualizacion, la firma debe coincidir)
    │
    ▼
  Se instala la app
```

### Que pasa con APKs descargados de internet (sideloading)

Si descargas un APK de cualquier sitio y lo instalas manualmente:

1. **Android verifica la firma** — Si el APK no esta firmado, no se instala
2. **Android muestra el certificado** — Muestra quien firmo el APK (si es conocido o desconocido)
3. **Play Protect escanea** — Google Play Services escanea el APK antes de instalar
4. **Origen desconocido** — El usuario debe habilitar "Instalar desde origenes desconocidos"

**Riesgos:**
- El APK puede haber sido modificado y re-firmado con otra key
- No hay garantia de que el desarrollador sea legitimo
- Puede contener malware

### Como verificar la firma de un APK manualmente

Se puede extraer y verificar la firma de un APK usando herramientas como:

- `apksigner verify` (Android SDK)
- `jarsigner` (JDK)
- `adb shell pm dump <package> | grep signatures`

### Que es la "firma" en el contexto de certificados al descargar

Cuando Android dice "Firma de la aplicacion", se refiere al **certificado** (clave publica) con el que se firmo el APK. Android muestra:

- **Subject:** A quien pertenece el certificado (nombre del desarrollador)
- **Issuer:** Quien emitió el certificado (podria ser autofirmado)
- **SHA-256:** Huella digital del certificado

Para apps de Play Store con Play App Signing, la firma visible es la de Google, no la del desarrollador original.

---

## 16. HASH

### Que es un hash

Un hash es una **funcion unidireccional** que toma un input de cualquier tamanio y produce un output de tamano fijo (el hash o resumen). Es como una "huella digital" de los datos.

**Propiedades:**
- **Deterministico:** Mismo input → mismo hash
- **Unidireccional:** Del hash no se puede obtener el input original
- **Resistente a colisiones:** Es muy dificil encontrar dos inputs que den el mismo hash
- **Avalancha:** Un cambio minimo en el input cambia completamente el hash

### Tipos de hash

| Algoritmo | Longitud | Seguridad | Uso |
|-----------|----------|-----------|-----|
| **MD5** | 128 bits | ROTO (colisiones demostradas) | No usar |
| **SHA-1** | 160 bits | ROTO (colisiones demostradas) | No usar |
| **SHA-256** | 256 bits | Seguro | El mas usado |
| **SHA-512** | 512 bits | Seguro | Mayor seguridad |
| **bcrypt** | Variable | Seguro (lento a proposito) | Almacenar passwords |
| **Argon2** | Variable | Muy seguro | Almacenar passwords (recomendado) |

### Usos en mobile

| Uso | Que se hashea | Para que |
|-----|--------------|----------|
| **Verificar integridad de APK** | Contenido del APK | Asegurar que no fue modificado |
| **Certificate Pinning** | Clave publica del cert | Identificar un certificado |
| **Almacenar passwords** | Password del usuario | No guardar la password en texto plano |
| **PKCE** | code_verifier → code_challenge | Proteger flujo OAuth |
| **Firma digital** | Hash del documento | Firmar documentos eficientemente |
| **Cache de imagenes** | URL de la imagen | Nombrar archivos de cache |

### Hash vs Cifrado

| Aspecto | Hash | Cifrado |
|---------|------|---------|
| **Direccion** | Unidireccional (no se puede revertir) | Bidireccional (se puede descifrar) |
| **Tamano** | Fijo siempre | Variable (igual al input) |
| **Clave** | No usa clave | Usa clave |
| **Proposito** | Verificar integridad | Proteger confidencialidad |

---

## 17. OFUSCACION DE CODIGO

### Que es la ofuscacion

La ofuscacion es un proceso que transforma el codigo compilado para hacerlo **dificil de entender** para un humano, sin cambiar su comportamiento. Es como ponerle "codigo encriptado" a tu app (pero no es cifrado, sigue siendo ejecutable).

### Que hace la ofuscacion

```
ANTES (codigo original):                     DESPUES (codigo ofuscado):

class LoginManager {                         class a {
    private String apiKey = "abc123";             private String a = "abc123";
    
    public boolean login(String user,             public boolean a(String a, String b) {
        String pass) {                                return b.a(a, b);
        return AuthService.validate(user, pass);   }
    }                                           
    
    public String getToken() {                   public String b() {
        return httpClient.post("/token");            return c.a("/token");
    }                                            }
}                                              }
```

### Herramientas de ofuscacion en Android

| Herramienta | Que hace |
|-------------|----------|
| **ProGuard** | Ofuscador clasico de Android. Renombra clases, metodos y campos. Tambien elimina codigo no usado. |
| **R8** | Reemplazo de ProGuard, integrado en Android Gradle Plugin. Mas rapido y eficiente. Se usa por defecto desde AGP 3.4+. |
| **DexGuard** | Version comercial de ProGuard con protecciones adicionales (cifrado de strings, ofuscacion de control flow, etc.). |

### Que protege la ofuscacion

| Aspecto | Protege? | Nota |
|---------|----------|------|
| Nombres de clases/metodos | **Si** | Los renombra a a, b, c |
| Strings (texto literal) | **No** | Siguen siendo visibles |
| API Keys en strings | **No** | Siguen ahi, solo renombradas |
| Logica de negocio | **Parcial** | Dificulta entenderla, pero no la oculta |
| Librerias de terceros | **Depende** | Si tambien estan ofuscadas |
| Codigo JNI/NDK | **No** (por defecto) | El codigo C/C++ no se ofusca con R8 |

### Lo que NO protege la ofuscacion

Importante: **La ofuscacion no es cifrado.** Un APK ofuscado sigue siendo completamente decompilable con herramientas como `jadx`. La ofuscacion solo hace que el codigo decompilado sea mas dificil de leer, no imposible.

**Lo que NO previene:**
- Extraer strings (API keys, URLs) — Siguen siendo texto plano
- Modificar el APK y re-firmarlo
- Inyectar codigo malicioso
- Analisis estatico del flujo de la app

### Configuracion tipica

En el `build.gradle.kts`:
```kotlin
buildTypes {
    release {
        isMinifyEnabled = true        // Activa R8
        proguardFiles(
            getDefaultProguardFile("proguard-android-optimize.txt"),
            "proguard-rules.pro"
        )
    }
}
```

El archivo `proguard-rules.pro` permite:
- **Keep:** No ofuscar ciertas clases (ej: modelos de datos que usa Gson/Room)
- **KeepNames:** Ofuscar pero mantener el nombre original
- **DontWarn:** Ignorar warnings de librerias

### Buenas practicas

1. **Siempre ofuscar en release** — No hay razon para no hacerlo
2. **Probar la release antes de publicar** — La ofuscacion puede romper cosas (Reflection, librerias)
3. **Guardar los mapping files** — Para poder desofuscar crash reports (Firebase Crashlytics lo usa)
4. **No ofuscar modelos de datos** — Room, Gson, Retrofit necesitan nombres reales para funcionar
5. **Considerar DexGuard si tenes requisitos de seguridad altos** (banca, salud, etc.)

---

## 18. SEGURIDAD DE CANAL

### Que es la seguridad de canal

La seguridad de canal abarca todas las medidas para proteger los datos **mientras se transmiten** entre la app y el servidor. No importa que tan segura sea tu app o tu servidor, si el canal de comunicacion es inseguro, todo es vulnerable.

### Componentes de la seguridad de canal

| Componente | Que protege |
|------------|-------------|
| **TLS 1.2 / 1.3** | Cifrado de la comunicacion |
| **Certificate Validation** | Que el servidor es quien dice ser |
| **Certificate Pinning** | Proteccion contra CAs comprometidas |
| **HSTS** | Forzar HTTPS (evitar downgrade a HTTP) |
| **Cipher Suites** | Algoritmos criptograficos usados |

### Cipher Suites recomendados

Android soporta muchos algoritmos de cifrado. No todos son igual de seguros.

| Algoritmo | Seguridad | Recomendado? |
|-----------|-----------|--------------|
| TLS_AES_128_GCM_SHA256 (TLS 1.3) | Alta | Si |
| TLS_AES_256_GCM_SHA384 (TLS 1.3) | Alta | Si |
| TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256 | Alta | Si (TLS 1.2) |
| TLS_RSA_WITH_AES_128_CBC_SHA | Media | No (RSA key exchange debil) |
| TLS_RSA_WITH_3DES_EDE_CBC_SHA | Baja | No (3DES obsoleto) |
| TLS_NULL_WITH_NULL_NULL | Ninguna | No (sin cifrado) |

### Ataques comunes al canal

| Ataque | Como funciona | Prevencion |
|--------|--------------|------------|
| **Man-in-the-Middle (MitM)** | Atacante se interpone entre app y servidor | TLS + Certificate Pinning |
| **SSL Stripping** | Degrada HTTPS a HTTP | HSTS |
| **Downgrade Attack** | Obliga a usar TLS 1.0 en vez de 1.3 | Deshabilitar TLS viejos |
| **Falso certificado** | CA comprometida emite cert falso | Certificate Pinning |
| **Proxy malicioso** | Proxy corporativo o publico intercepta | No aceptar certificados de terceros |

### Configuracion de seguridad de red en Android

Android provee `network_security_config.xml` donde podes configurar:

- **Dominios de confianza** — Que dominios aceptan HTTPS
- **Pins** — Certificate Pinning
- **Debug overrides** — Permitir certificados autofirmados solo en debug
- **Cleartext traffic** — Deshabilitar HTTP (recomendado: solo HTTPS)

**Recomendacion:** Siempre incluir en `AndroidManifest.xml`:

```xml
<application
    android:networkSecurityConfig="@xml/network_security_config"
    ...
```

Esto funciona incluso sin codigo, solo configuracion.

---

## 19. SEGURIDAD DE APLICACION

### Que es la seguridad de aplicacion

Son las medidas implementadas dentro de la app para protegerse contra ataques, tanto en tiempo de ejecucion como en reposo. La seguridad de aplicacion asume que el dispositivo puede estar comprometido.

### Tecnicas de seguridad de aplicacion

#### 19.1 Deteccion de Root

Un dispositivo rooteado permite a una app maliciosa obtener permisos de superusuario, pudiendo:

- Leer datos de otras apps (incluyendo las tuyas)
- Modificar el comportamiento del sistema
- Instalar certificados falsos
- Hacer debugging de cualquier app

La app puede detectar root verificando:

- Presencia de binarios `su`, `busybox`
- Directorios tipicos de root (`/system/app/Superuser.apk`)
- Propiedades del sistema (ro.debuggable)
- Ejecucion de comandos de root

**Importante:** La deteccion de root puede tener falsos positivos (algunas ROMs custom no rooteadas pueden tener binarios su). Nunca bloquear completamente solo por deteccion de root, sino limitar funcionalidades.

#### 19.2 Deteccion de Emulador

Los atacantes suelen usar emuladores para analizar apps. La deteccion de emulador verifica:

- Numero de telefono (emuladores tienen 1555521xxxx)
- Build properties (ro.product.model, ro.manufacturer)
- IMEI (emuladores tienen valores por defecto)
- Presencia de sensor (emuladores pueden no tenerlos)

**Usar con cuidado:** No todos los emuladores son maliciosos. Desarrolladores legitimos usan emuladores para testing.

#### 19.3 Verificacion de Firma en Tiempo de Ejecucion

La app verifica que su propia firma no haya cambiado:

```kotlin
val firmas = packageManager.getPackageInfo(packageName, PackageManager.GET_SIGNATURES)
val firmaEsperada = "..."
if (firmas.signatures[0].toCharsString() != firmaEsperada) {
    // La app fue modificada, cerrar
}
```

**Para que sirve:** Si un atacante decompila la app, modifica el codigo, y re-firma con su propia key, la app puede detectar que la firma no coincide y negarse a ejecutar.

#### 19.4 Proteccion contra Screen Recording / Screenshots

Usar `FLAG_SECURE` en ventanas con datos sensibles:

- La ventana no aparece en la lista de apps recientes
- No se puede hacer screenshot
- No se puede grabar la pantalla

**Cuando usarlo:** Pantallas de login, datos financieros, informacion personal sensible.

#### 19.5 Limpieza de Datos al Pasar a Background

Cuando la app pasa a segundo plano (onPause/onStop):

- Limpiar el clipboard
- Limpiar campos de texto sensibles
- Cerrar sesion si es necesario
- Bloquear con biometria al volver

#### 19.6 Tiempo de Inactividad (Session Timeout)

- Bloquear la app despues de un tiempo sin actividad (2-5 minutos)
- Requerir autenticacion (biometrica o PIN) para reanudar
- No mantener sesion abierta para siempre

#### 19.7 Anti-Tampering (Anti-Manipulacion)

Verificar que la app no haya sido modificada:

- Verificar checksum de archivos DEX
- Verificar que la app no este siendo debuggeada
- Verificar que no se este ejecutando en un entorno de debugging (ro.debuggable)
- Verificar firmas de librerias nativas (.so)

---

## 20. ALMACENAMIENTO SEGURO

### Donde NO guardar datos sensibles

| Almacenamiento | Seguridad | Que NO guardar ahi |
|---------------|-----------|-------------------|
| SharedPreferences | Baja (sin cifrar) | Tokens, passwords, datos personales |
| SQLite (sin cifrar) | Baja | Datos personales, historial |
| Almacenamiento externo (SD card) | Muy baja | Nada sensible |
| Logcat | Ninguna | Nada sensible (ni en debug) |
| Backup de Android | Variable | Nada sensible sin configurar |
| Cache de imagenes | Baja | Datos en imagenes |

### Donde SI guardar datos sensibles

#### 20.1 Android Keystore

El **Android Keystore** es un almacenamiento seguro de claves criptograficas. Las claves:

- No pueden ser extraidas del dispositivo (en dispositivos con hardware seguro)
- Pueden requerir autenticacion biometrica para usarse
- Son especificas de la app (otras apps no pueden acceder)
- Se pueden almacenar en hardware seguro (TEE — Trusted Execution Environment)

**Que guardar ahi:**
- Claves privadas (para DPoP, firma de documentos)
- Claves simetricas para cifrar datos locales
- Claves para autenticacion biometrica

#### 20.2 EncryptedSharedPreferences

Parte de **Jetpack Security**, es una implementacion de SharedPreferences que cifra automaticamente los datos:

- Los datos se cifran con una clave almacenada en Android Keystore
- Los valores se cifran con AES-256 GCM
- Los nombres de las preferencias se cifran tambien

**Que guardar ahi:**
- Access Tokens
- Refresh Tokens
- Preferencias de configuracion que contengan datos sensibles
- IDs de sesion

#### 20.3 Room + SQLCipher

Para bases de datos SQLite, se puede usar **SQLCipher** (extension de SQLite que cifra toda la base de datos):

- La base de datos completa esta cifrada con AES-256
- Se necesita una clave (guardada en Keystore) para abrirla
- Las queries funcionan igual, el cifrado es transparente
- Si alguien roba el archivo de la BD, solo ve datos cifrados

#### 20.4 Almacenamiento Interno

El almacenamiento interno de Android (`context.filesDir`, `context.cacheDir`) es:

- Accesible solo por la app (no por otras apps)
- Pero si el dispositivo esta rooteado, cualquier app puede leerlo

Por eso, aunque uses almacenamiento interno, los datos sensibles deben estar **cifrados** adicionalmente.

### Tabla de almacenamiento seguro

| Que guardar | Donde | Cifrado |
|------------|-------|---------|
| API Keys | **No en la app** (proxy server) | — |
| Access Token | EncryptedSharedPreferences | AES-256 |
| Refresh Token | EncryptedSharedPreferences | AES-256 |
| Clave privada | Android Keystore | Hardware-backed |
| Password del usuario | **No almacenar** (solo token) | — |
| Datos de usuario | Room + SQLCipher | AES-256 |
| Cache de imagenes | cacheDir | Opcional |
| Logs | **No guardar logs sensibles** | — |

---

## 21. FASTLANE PARA CI/CD

### Que es Fastlane

**Fastlane** es una herramienta open source que automatiza todo el proceso de build, firma, testing y publicacion de apps mobile (Android e iOS). Es como un "Makefile" para tu flujo de distribucion.

### Que problemas resuelve

| Problema | Como lo resuelve Fastlane |
|----------|--------------------------|
| "Me olvide de firmar el APK" | La firma se configura una vez y se ejecuta automaticamente |
| "Tengo que subir manualmente a Play Store" | Fastlane sube automaticamente |
| "Los screenshots estan desactualizados" | Fastlane genera screenshots automaticos |
| "Configurar CI/CD es complicado" | Fastlane se integra con GitHub Actions, Jenkins, etc. |
| "Los builds locales vs CI difieren" | Fastlane estandariza el proceso |

### Componentes de Fastlane

| Componente | Que hace |
|------------|----------|
| **Fastfile** | Define las "lanes" (acciones automatizadas) |
| **Appfile** | Configuracion de la app (bundle id, credenciales) |
| **Match** | Gestion de certificados y perfiles de provisioning (iOS) |
| **Supply** | Sube APKs a Play Store |
| **Screenshot** | Toma capturas automaticas |
| **Gym** | Compila y firma la app |
| **Firebase App Distribution** | Distribuye builds a testers |

### Flujo tipico con Fastlane

```
Desarrollador hace commit
         │
         ▼
  CI/CD (GitHub Actions, GitLab CI, etc.)
         │
         ▼
  Fastlane ejecuta:
  1. gym → build + firma del APK
  2. test → ejecuta tests unitarios y de integracion
  3. screengrab → captura screenshots
  4. supply → sube a Play Store (internal testing)
         │
         ▼
  Play Store → testers internos prueban
         │
         ▼
  Aprobado → Fastlane sube a produccion
```

### Beneficios de seguridad de usar Fastlane en CI/CD

1. **Las claves de firma no estan en las maquinas de los desarrolladores** — Solo en el CI/CD
2. **El proceso es reproducible** — Siempre el mismo resultado
3. **No hay "builds de la maquina de Juan"** — Todos pasan por el mismo pipeline
4. **Se pueden agregar escaneos de seguridad automaticos** (Dependency check, SAST)
5. **Trazabilidad** — Cada build queda registrado con su hash, quien lo ejecuto, etc.

### Ejemplo de estructura

```
fastlane/
├── Fastfile          ← Las acciones automatizadas
├── Appfile           ← Config de la app
└── Matchfile         ← Gestion de certificados
```

### Security Scanning en el pipeline CI/CD

Se pueden integrar herramientas de seguridad en el pipeline de CI/CD para detectar vulnerabilidades antes de publicar:

| Herramienta | Que detecta | Momento |
|------------|-------------|---------|
| **OWASP Dependency-Check** | Vulnerabilidades en librerias de terceros | Antes del build |
| **Snyk** | Vulnerabilidades en dependencias | Antes del build |
| **MobSF (Mobile Security Framework)** | Analisis estatico y dinamico de la app | Despues del build |
| **Qark** | Vulnerabilidades Android comunes | Durante el build |
| **Danger** | Code review automatizado | Durante el PR |

---

## 22. CHECKLIST DE SEGURIDAD MOBILE

### Pre-Desarrollo
- [ ] Definir politicas de seguridad del proyecto
- [ ] Elegir mecanismos de autenticacion (OAuth 2.0 + PKCE)
- [ ] Disenar arquitectura con defensa en profundidad
- [ ] Definir que datos necesita realmente la app (minimo privilegio)

### Desarrollo
- [ ] No hardcodear API Keys, secrets o tokens
- [ ] Usar Android Keystore para claves criptograficas
- [ ] Usar EncryptedSharedPreferences para tokens
- [ ] Usar HTTPS en todas las comunicaciones
- [ ] Implementar Certificate Pinning (con backup pin)
- [ ] Validar entrada del usuario (no confiar en el cliente)
- [ ] No loguear datos sensibles
- [ ] Usar `FLAG_SECURE` en pantallas sensibles
- [ ] Configurar `network_security_config.xml`
- [ ] Configurar `AndroidManifest.xml` con `exported="false"` por defecto

### Pre-Release
- [ ] Ofuscar con R8/ProGuard
- [ ] Ejecutar tests de seguridad (MobSF, Snyk, Dependency-Check)
- [ ] Verificar que no haya secrets en el codigo (git-secrets, truffleHog)
- [ ] Probar la app en un dispositivo sin Google Services
- [ ] Verificar que los permisos pedidos sean los minimos necesarios
- [ ] Probar la app con un proxy (Burp Suite) para verificar que no haya leaks

### CI/CD
- [ ] Configurar Fastlane para builds automatizados
- [ ] Las claves de firma solo en el CI/CD, no en maquinas locales
- [ ] Escaneo de dependencias automatico en cada build
- [ ] Tests unitarios y de integracion pasando antes de publicar

### Publicacion
- [ ] Usar Google Play App Signing
- [ ] Firmar con APK Signature Scheme v2 + v3
- [ ] Verificar que la app pase las revisiones de Play Store
- [ ] Configurar Play Integrity API para verificar integridad

### Post-Release
- [ ] Monitorear crashes y errores de seguridad
- [ ] Tener un plan de respuesta a vulnerabilidades
- [ ] Rotar claves periodicamente
- [ ] Actualizar dependencias regularmente
- [ ] Probar la app con cada nueva version de Android

---

## RESUMEN — MAPA DE CONCEPTOS

```
                    SEGURIDAD MOBILE
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
   AUTENTICACION      COMUNICACION      ALMACENAMIENTO
        │                 │                 │
   ┌────┴────┐       ┌────┴────┐       ┌────┴────┐
   │         │       │         │       │         │
  OAuth    API Key  TLS     Pinning  Keystore  E.S.P.
  +PKCE    +Proxy  1.3     Certs    HW-backed Encrypted
  +DPoP    Server                          SharedPrefs
   │         │       │         │       │         │
  Tokens   Client   Cipher   Play    SQLCipher Room
  Bearer   Creds   Suites  Integrity
  Refresh           HSTS    API
```

**Recordatorio final:** La seguridad no es un producto, es un proceso. No existe la app 100% segura. El objetivo es hacer que atacar tu app sea **tan dificil que el atacante busque un objetivo mas facil**. Cada capa de seguridad que agregues reduce la probabilidad de exito de un ataque.
