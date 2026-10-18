# Clase completa v5 — Bearer token al infinito y más allá

**Tema: la falsa sensación de seguridad.**

---

## Índice

1. El conflicto: cada tecnología resuelve algo
2. Antes del bearer: Basic, Digest, Cookies, API keys, SAML, OAuth 1.0
3. El bearer token y la falsa sensación de seguridad
4. JWT: qué es y qué no es
5. Base64: por qué existe y por qué no es cifrado
6. Seguridad dinámica: MFA Step-Up
7. El ecosistema mobile: PKCE, App Attestation, DPoP
8. DPoP vs mTLS
9. Arquitectura: TLS, Gateway, Zero Trust
10. Caso Uruguay: ID Uruguay
11. Cierre

---

## 1. El conflicto: cada tecnología resuelve algo

Cada tecnología de autenticación nació como respuesta a un problema concreto. Ninguna es perfecta: cada una resuelve algo y deja algo abierto.

| Tecnología | Año | Qué resuelve | Qué no resuelve |
|---|---|---|---|
| HTTP Basic | 1999 | Autenticación mínima sin estado | Credencial viaja en cada request |
| HTTP Digest | 2015 | No mandar contraseña en claro | Modelo de credencial en cada request |
| Cookies | 1996-2011 | Recordar quién sos sin repetir contraseña | CSRF, robo por XSS, fijación |
| API keys | 2006 | Identificar aplicaciones | No expira, no distingue permisos |
| SAML 2.0 | 2005 | SSO, identidad federada | XML pesado, difícil en móviles |
| OAuth 1.0 | 2010 | Request robado no reutilizable | Muy difícil de implementar |
| Bearer token | 2012 | Simplicidad, no firmar cada request | Quien tiene el token, lo usa |

**La pregunta no es si el token es seguro, sino qué problema resuelve y qué no.**

---

## 2. Antes del bearer

### HTTP Basic: RFC 2617 (1999)

Manda `usuario:contraseña` en Base64 en cada petición.

- **Qué resuelve:** autenticación mínima sin estado
- **Qué no resuelve:** la credencial viaja en cada request, no hay logout, no hay revocación
- **Se sigue usando:** en sistemas internos y como `client_secret_basic` en OAuth

### HTTP Digest: RFC 7616 (2015)

Manda un hash con un nonce en lugar de la contraseña en claro.

- **Qué resuelve:** no mandar la contraseña en claro
- **Qué no resuelve:** el modelo sigue siendo credencial en cada request
- **Se sigue usando:** prácticamente en desuso

### Cookies: Netscape (1996) → RFC 6265 (2011)

Un identificador de sesión que el navegador guarda y reenvía.

- **Qué resuelve:** recordar quién sos sin repetir la contraseña
- **Qué no resuelve:** CSRF, robo de sesión por XSS, fijación de sesión
- **Se sigue usando:** en navegadores web, con `HttpOnly`, `Secure` y `SameSite`

### API keys: AWS (2006)

Un secreto estático que identifica al cliente.

- **Qué resuelve:** identificar aplicaciones sin un servidor de identidad
- **Qué no resuelve:** no expira, no distingue permisos, si se filtra es impersonación directa
- **Se sigue usando:** en servicios internos y APIs de terceros

### SAML 2.0: OASIS (2005)

Aserciones XML firmadas para federación.

- **Qué resuelve:** SSO entre aplicaciones, identidad federada
- **Qué no resuelve:** XML pesado, difícil de implementar en móviles y SPAs
- **Se sigue usando:** en banca, gobierno y SaaS corporativo

### OAuth 1.0: RFC 5849 (2010)

Firmaba cada request con HMAC-SHA1.

- **Qué resuelve:** un request robado no se podía reutilizar
- **Qué no resuelve:** era muy difícil de implementar bien
- **Se sigue usando:** prácticamente abandonado

---

## 3. El bearer token y la falsa sensación de seguridad

### Bearer token: RFC 6749 y 6750 (2012)

Un string que se presenta en la cabecera `Authorization: Bearer`.

- **Qué resuelve:** simplicidad, no hay que firmar cada request
- **Qué no resuelve:** quien tiene el token, lo usa

### La falsa sensación de seguridad

El bearer token resuelve la **delegación de autorización**. No resuelve:

- **Autorización:** la autorización es otro capítulo
- **Cifrado:** el payload no está cifrado
- **Anti-replay:** interceptado = reutilizado
- **MFA:** la autenticación ya pasó
- **Gestión de sesión:** no hay logout real

**Tener `Authorization: Bearer` no significa que la API sea segura. Significa que quien tiene el token, entra.**

---

## 4. JWT: qué es y qué no es

### JWT: RFC 7519 (2015)

Tres partes en base64url: `header.payload.signature`.

- **Qué resuelve:** claims autenticables sin estado
- **Qué no resuelve:** el payload no está cifrado, cualquiera lo lee

### La trampa del algoritmo

El header de un JWT dice con qué algoritmo se firmó. Si el validador confía en el `alg` del token en lugar de su propia configuración, un atacante puede elegir el algoritmo:

- `alg: none` — sin firma
- Confusión RS256 → HS256 — usar la clave pública como secreto
- Inyección de `kid` — apuntar a un JWKS controlado por el atacante

**La regla:** la política de verificación sale de la configuración del validador, nunca del token.

---

## 5. Base64: por qué existe y por qué no es cifrado

### El problema que resuelve

Muchos protocolos (HTTP, email SMTP, XML) fueron diseñados para transportar **texto de 7 bits** (ASCII). No pueden transportar bytes arbitrarios directamente:

- Un byte `0xFF` (255) no es un carácter ASCII válido
- Un archivo PDF, una imagen PNG o un certificado X.509 contienen bytes que no son texto ASCII válido

### Cómo funciona

Base64 opera en **grupos de 3 bytes** (24 bits) y los divide en **4 grupos de 6 bits** cada uno:

```
3 bytes = 24 bits
↓ dividir en 4 grupos de 6 bits
4 × 6 bits = 24 bits
```

Cada grupo de 6 bits (valores 0-63) se mapea a un carácter del alfabeto Base64: `A-Z`, `a-z`, `0-9`, `+`, `/`.

### Ejemplo concreto

```
Datos binarios (una imagen):  [0xFF, 0xD8, 0xFF, 0xE0, ...]
                              ↓ Base64
Texto ASCII:                  "/9j/4AAQSkZJRg..."
```

Cualquier sistema que solo entiende texto puede transportar la imagen sin problema. El receptor aplica Base64-decode y recupera los bytes originales.

### La diferencia entre cifrado y codificación

| | Cifrado | Codificación |
|---|---|---|
| **Propósito** | Ocultar información | Representar datos en otro formato |
| **Requiere clave** | Sí | No |
| **Reversible** | Solo con la clave | Siempre, por cualquiera |
| **Seguridad** | Protege confidencialidad | No protege nada |

### Dónde aparece en la seguridad

1. **HTTP Basic**: la cabecera `Authorization: Basic dXN1YXJpbzpjbGF2ZQ==` es `usuario:contraseña` en Base64. Cualquiera que intercepte la cabecera puede leer las credenciales.

2. **JWT**: el payload de un JWT está en base64url. Cualquiera puede leer los claims sin verificar nada:
   ```
   eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjMifQ.signature
   ↑ header           ↑ payload (leíble)
   ```

### La regla

> Base64 es como poner un sobre de papel transparente: cambia la presentación, no el contenido. El lector solo tiene que saber que es Base64 para leer lo que hay dentro.

---

## 6. Seguridad dinámica: MFA Step-Up

### El concepto

La autenticación no es un estado binario de "conectado/desconectado", sino un **flujo continuo** que ajusta el nivel de garantía según la sensibilidad de la operación.

En un sistema con Step-Up:
- El usuario inicia sesión con usuario + contraseña
- Para operaciones normales (ver saldo, consultar datos) es suficiente
- Para operaciones sensibles (transferencias, cambiar contraseña, ver datos personales) la API **exige re-autenticación** en ese momento exacto

### Cómo funciona (RFC 9470)

1. El usuario hace un `POST /api/transferencias` con su bearer token normal
2. La API evalúa: es una operación sensible, y el token dice `acr: pwd` (solo contraseña)
3. La API responde **401** con el header:
   ```
   WWW-Authenticate: Bearer error="insufficient_user_authentication", acr_values="urn:mace:incommon:iap:silver"
   ```
4. El frontend intercepta el 401, redirige al Identity Provider
5. El usuario pasa segundo factor (huella, TOTP, push)
6. El IdP emite un nuevo token con `acr` actualizado
7. El cliente reintenta el POST original con el nuevo token
8. La API lo aprueba

### Los claims involucrados

| Claim | Significado |
|---|---|
| `acr` | Authentication Context Class Reference — qué nivel de autenticación tuvo lugar |
| `amr` | Authentication Methods References — qué métodos se usaron (pwd, otp, mfa) |

### Por qué importa

La **falsa sensación de seguridad** es pensar que "ya está autenticado = está protegido". Sin Step-Up:
- Un token robado por XSS sirve para cualquier operación
- La MFA solo protege el login, no el uso posterior

Con Step-Up:
- El token robado solo sirve para operaciones de bajo nivel
- Las operaciones sensibles exigen prueba fresca de identidad

**Resumen:** Step-Up es pedir más garantía solo cuando importa, sin fricción para el resto.

---

## 7. El ecosistema mobile: PKCE, App Attestation, DPoP

### El problema

Las apps móviles están en manos del atacante. Pueden modificar el APK, desactivar SSL pinning, extraer secretos. El cliente "Frankenstein" simula ser la app legítima y llama a la API directamente.

### PKCE: RFC 7636 (2015)

El cliente genera un `code_verifier`, envía su hash como `code_challenge`, y prueba el verifier al canjear el código. Si un atacante intercepta el código, no lo puede canjear sin el verifier.

### App Attestation

- **Android:** Play Integrity API
- **iOS:** DeviceCheck / App Attest

Verifica que el binario no fue modificado y emite un token de attestation. La API lo verifica antes de operaciones sensibles.

### DPoP: RFC 9449 (2023)

El cliente genera un par de claves dinámicamente. El token se ata a la clave pública. Cada request incluye un JWT firmado con la clave privada en un header DPoP. Sin PKI, funciona a través de proxies y WAFs.

### Las tres capas juntas

| Capa | Protección |
|---|---|
| App Attestation | El binario es legítimo |
| PKCE | El código no se puede reutilizar |
| DPoP | El token no sirve en otro dispositivo |

El cliente Frankenstein se queda fuera: sin binario legítimo, sin PKCE, sin DPoP.

---

## 8. DPoP vs mTLS

| Característica | mTLS | DPoP |
|---|---|---|
| Capa OSI | Capa 4 (Transporte) | Capa 7 (Aplicación) |
| Mecanismo | Certificado X.509 en TLS | JWT firmado en header HTTP |
| Gestión de claves | Compleja (PKI) | Sin PKI, par dinámico |
| Ideal para | M2M, microservicios | SPAs, móviles |

**mTLS** opera en la capa de transporte: el cliente presenta un certificado X.509 durante el handshake TLS. El token queda atado al certificado vía el claim `cnf`.

**DPoP** opera en la capa de aplicación: el cliente firma cada request con su clave privada. No requiere PKI ni certificados de red.

---

## 9. Arquitectura: TLS, Gateway, Zero Trust

### TLS

Protege el token en tránsito contra ataques Man-in-the-Middle. Pero no protege contra un XSS en el frontend, un token logueado por error en Splunk/Kibana, o un proxy malicioso en el cliente.

### API Gateway

Es la primera línea de defensa:
- Validar la firma del token
- Verificar la expiración (TTL corto)
- Verificar el audience (`aud`)
- Throttling y rate limiting
- Verificar que el token no esté revocado

### Zero Trust

El error común: el gateway valida el token y los microservicios confían ciegamente ("confianza perimetral").

En una arquitectura Zero Trust:
- La identidad del usuario (los claims del JWT) se propaga hacia atrás
- Cada microservicio autoriza la acción según su propia lógica de negocio
- No se confía por estar "dentro" de la red

---

## 10. Caso Uruguay: ID Uruguay

**ID Uruguay** es el proveedor de identidad del Estado uruguayo, gestionado por AGESIC. Se integra vía OpenID Connect.

Riesgos comunes en el ecosistema local:
- Tokens de larga vida sin rotación en integraciones B2B
- SPAs con token en localStorage (robo por XSS)
- Falta de Step-Up para operaciones sensibles

Las mitigaciones de esta charla aplican igual: DPoP, PKCE, Step-Up.

---

## 11. Cierre

**El token se acaba. El riesgo no.**

La falsa sensación de seguridad es pensar que bearer significa seguro. Bearer significa portador.

La seguridad está en el sistema:
- Autorización (no solo autenticación)
- Cifrado (no solo codificación)
- Anti-replay (no solo validez)
- MFA (no solo contraseña)
- Gestión de sesión (no solo emisión)

**Bearer token al infinito y más allá:** el infinito es lo que viene después del bearer. El más allá es la seguridad completa.

---

*Fin de la clase completa v5.*
