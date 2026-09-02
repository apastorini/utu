# 1.3 Principios de Criptografía Aplicada a Contraseñas

## Criptografía Simétrica vs Asimétrica

### Simétrica (Misma clave para cifrar y descifrar)

```
┌──────────┐   Clave K    ┌──────────┐
│  Texto   │─────────────►│  Cifrado │
│  Plano   │              │  (AES)   │
└──────────┘              └─────┬────┘
                                │
                           Ciphertext
                                │
                                ▼
┌──────────┐   Clave K    ┌──────────┐
│  Texto   │◄─────────────│  Cifrado │
│  Plano   │              │  (AES)   │
└──────────┘              └──────────┘
```

### Asimétrica (Par de claves: pública + privada)

```
┌──────────┐  Clave Pública   ┌──────────┐
│  Texto   │─────────────────►│  Cifrado │
│  Plano   │                  │  (RSA)   │
└──────────┘                  └─────┬────┘
                                    │
                               Ciphertext
                                    │
                                    ▼
┌──────────┐  Clave Privada   ┌──────────┐
│  Texto   │◄─────────────────│  Cifrado │
│  Plano   │                  │  (RSA)   │
└──────────┘                  └──────────┘
```

## AES-256 (Advanced Encryption Standard)

AES es el estándar de cifrado simétrico utilizado por virtually todos los gestores de contraseñas.

### Especificaciones

| Parámetro | Valor |
|-----------|-------|
| **Tamaño de bloque** | 128 bits |
| **Tamaño de clave** | 128, 192 o 256 bits |
| ** rondas** | 10 (128), 12 (192), 14 (256) |
| **Seguridad** | 256 bits = 2²⁵⁶ operaciones para fuerza bruta |

### Modos de Operación

```
┌─────────────────────────────────────────────────┐
│                  MODOS DE AES                    │
├──────────────┬──────────────────────────────────┤
│  ECB         │  ❌ NO USAR (pattern leakage)   │
│  CBC         │  ⚠️ Aceptable con IV aleatorio  │
│  CTR         │  ✅ Bueno (paralelizable)        │
│  GCM         │  ✅✅ RECOMENDADO (autenticado)  │
│  CCM         │  ✅ Bueno (autenticado)          │
│  SIV         │  ✅✅ Excelente (determinista)   │
└──────────────┴──────────────────────────────────┘
```

### AES-256-GCM (Galois/Counter Mode)

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  Plaintext   │    │  Key (256b)  │    │  IV/Nonce    │
└──────┬───────┘    └──────┬───────┘    └──────┬───────┘
       │                   │                   │
       ▼                   ▼                   ▼
┌──────────────────────────────────────────────────────┐
│                  AES-256-GCM                         │
│                                                      │
│  1. Cifra plaintext → ciphertext (AES-CTR)          │
│  2. Genera authentication tag (GHASH)               │
│                                                      │
└──────────────┬───────────────────────┬───────────────┘
               │                       │
               ▼                       ▼
        ┌─────────────┐        ┌─────────────┐
        │ Ciphertext  │        │ Auth Tag    │
        │ (datos      │        │ (integridad)│
        │  cifrados)  │        │             │
        └─────────────┘        └─────────────┘

Ventaja: Cifra Y autentica (detecta manipulación)
```

## Funciones Hash

### Propiedades Requeridas

| Propiedad | Descripción |
|-----------|-------------|
| **Determinista** | Mismo input → mismo output |
| **Unidireccional** | No se puede invertir (hash → input) |
| **Resistencia a colisiones** | Difícil encontrar dos inputs con mismo hash |
| **Avalancha** | Pequeño cambio en input → cambio grande en output |
| **Pre-image resistance** | Difícil encontrar input dado un hash |

### Comparación de Algoritmos

| Algoritmo | Salida | Velocidad (GPU) | Recomendado |
|-----------|--------|-----------------|-------------|
| MD5 | 128 bits | 150 Ghash/s | ❌ Nunca |
| SHA-1 | 160 bits | 50 Ghash/s | ❌ Obsoleto |
| SHA-256 | 256 bits | 20 Ghash/s | ⚠️ Solo con KDF |
| SHA-512 | 512 bits | 7 Ghash/s | ⚠️ Solo con KDF |
| bcrypt | variable | 18 khash/s | ✅ Bueno |
| scrypt | variable | 1 khash/s | ✅ Bueno |
| Argon2id | variable | <1 khash/s | ✅✅ Excelente |

## HMAC (Hash-based Message Authentication Code)

HMAC combina una función hash con una clave secreta para **autenticar** mensajes.

```
HMAC-SHA256(K, M) = SHA256((K ⊕ opad) || SHA256((K ⊕ ipad) || M))

Donde:
- K = Clave secreta
- M = Mensaje
- opad = 0x5c relleno
- ipad = 0x36 relleno
```

### Uso en Gestores de Contraseñas

| Uso | Descripción |
|-----|-------------|
| **Autenticación de vault** | Verificar que el vault no fue manipulado |
| **Verificación de integridad** | Detectar cambios no autorizados |
| **Token generation** | Generar tokens de sesión seguros |

## RSA (Rivest-Shamir-Adleman)

Criptografía asimétrica basada en la dificultad de factorizar números primos grandes.

### Parámetros Recomendados

| Tamaño de Clave | Seguridad Equivalente | Uso |
|-----------------|----------------------|-----|
| 2048 bits | ~112 bits | ⚠️ Mínimo aceptable |
| 3072 bits | ~128 bits | ✅ Recomendado |
| 4096 bits | ~140 bits | ✅✅ Excelente |

### Uso en Gestores de Contraseñas

```
┌──────────┐                    ┌──────────┐
│  Cliente │                    │ Servidor │
├──────────┤                    ├──────────┤
│          │  1. Genera par     │          │
│  RSA Key │  de claves         │          │
│  Gen     │                    │          │
│          │  2. Envía clave    │          │
│          │  pública al server │          │
│          │───────────────────►│          │
│          │                    │          │
│          │  3. Server cifra   │          │
│          │  datos con clave   │          │
│          │  pública del cliente│         │
│          │◄───────────────────│          │
│          │                    │          │
│  4. Cliente descifra         │          │
│  con clave privada           │          │
└──────────┘                    └──────────┘
```

## Certificados TLS/SSL

### Flujo del Handshake TLS 1.3

```
┌──────────┐                    ┌──────────┐
│  Cliente │                    │  Server  │
├──────────┤                    ├──────────┤
│          │ 1. ClientHello     │          │
│          │   (versiones,      │          │
│          │    cifrados)       │          │
│          │───────────────────►│          │
│          │                    │          │
│          │ 2. ServerHello     │          │
│          │   + Certificate    │          │
│          │   + Key Share      │          │
│          │◄───────────────────│          │
│          │                    │          │
│  3. Verifica certificado     │          │
│  (CA trusted?)               │          │
│          │                    │          │
│          │ 4. Finished        │          │
│          │───────────────────►│          │
│          │                    │          │
│          │ 5. Finished        │          │
│          │◄───────────────────│          │
│          │                    │          │
│  ✅ Conneción segura establecida        │
└──────────┘                    └──────────┘
```

## Entropía y Aleatoriedad

### Fuentes de Entropía

| Fuente | Entropía | Fiabilidad |
|--------|----------|------------|
| `/dev/urandom` (Linux) | Alta | ✅ Excelente |
| `CryptGenRandom` (Windows) | Alta | ✅ Excelente |
| `crypto.randomBytes` (Node.js) | Alta | ✅ Excelente |
| `os.urandom` (Python) | Alta | ✅ Excelente |
| `rand()` (C stdlib) | Baja | ❌ Nunca usar |

### Cálculo de Entropía

```
Entropía = log2(N^L)

Donde:
- N = Tamaño del alfabeto
- L = Longitud de la contraseña

Ejemplos:
- 8 chars minúsculas: log2(26^8) = 37.6 bits
- 12 chars mixtos: log2(62^12) = 71.4 bits
- 16 chars mixtos+símbolos: log2(94^16) = 105.4 bits

Objetivo mínimo: 80 bits de entropía
Objetivo recomendado: 128+ bits de entropía
```

## Salt y IV (Initialization Vector)

### Por qué necesitamos Salt

```
SIN SALT:
┌─────────────┐    SHA-256    ┌──────────────────┐
│ "password"  │──────────────►│ 5e884898da280... │  ← Mismo hash
└─────────────┘               └──────────────────┘     para todos

CON SALT:
┌─────────────┐  Salt + SHA-256  ┌──────────────────┐
│ "password"  │ + "a1b2c3..." ──►│ 3c4e5f6a7b8c9... │  ← Hash único
└─────────────┘                   └──────────────────┘     por usuario

┌─────────────┐  Salt + SHA-256  ┌──────────────────┐
│ "password"  │ + "d4e5f6..." ──►│ 9f8e7d6c5b4a3... │  ← Diferente
└─────────────┘                   └──────────────────┘     salt, diferente hash
```

### IV en AES

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  Plaintext   │    │  Clave AES   │    │  IV Aleatorio│
│  "Hola"      │    │  (256 bits)  │    │  (12 bytes)  │
└──────┬───────┘    └──────┬───────┘    └──────┬───────┘
       │                   │                   │
       ▼                   ▼                   ▼
┌──────────────────────────────────────────────────────┐
│              AES-256-GCM                              │
│                                                      │
│  1. IV genera stream de keystream                    │
│  2. XOR con plaintext → ciphertext                   │
│  3. Genera auth tag                                  │
│                                                      │
└──────────────┬───────────────────────┬───────────────┘
               │                       │
               ▼                       ▼
        ┌─────────────┐        ┌─────────────┐
        │ Ciphertext  │        │ Auth Tag    │
        └─────────────┘        └─────────────┘

IMPORTANTE: IV nunca debe repetirse con la misma clave
```

## Resumen de Algoritmos en Gestores de Contraseñas

| Componente | Algoritmo Recomendado | Uso |
|------------|----------------------|-----|
| **Cifrado de vault** | AES-256-GCM | Cifrar las contraseñas |
| **Derivación de clave** | Argon2id o PBKDF2 | Convertir master password en clave |
| **Hash de autenticación** | HMAC-SHA256 | Verificar identidad del usuario |
| **Integridad** | SHA-256 o BLAKE2 | Verificar que datos no fueron modificados |
| **Transporte** | TLS 1.3 | Cifrar comunicación cliente-servidor |
| **Asimétrico** | RSA-3072 o ECC P-256 | Firma digital, intercambio de claves |

---

> **Actividad de Reflexión**: ¿Por qué gestores como KeePass y Vaultwarden usan múltiples rondas de PBKDF2/Argon2id en lugar de un solo hash? ¿Qué pasaría si usáramos SHA-256 una sola vez?
