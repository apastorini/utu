# 1.2 Amenazas Comunes a las Contraseñas

## Panorama de Amenazas

```
┌─────────────────────────────────────────────────────────────┐
│                    AMENAZAS A CONTRASEÑAS                   │
├──────────────────┬──────────────────┬───────────────────────┤
│   EN EL BORDE    │   EN TRANSITO    │   EN REPOSO           │
├──────────────────┼──────────────────┼───────────────────────┤
│ Keyloggers       │ Sniffing         │ Rainbow Tables        │
│ Screen Capture   │ Man-in-the-Middle│ Fuerza Bruta          │
│ Phishing         │ Downgrade Attack │ Diccionario           │
│ Shoulder Surfing │ Session Hijacking│ Credential Stuffing   │
│ Malware          │ DNS Spoofing     │侧信道 (Side-channel)  │
└──────────────────┴──────────────────┴───────────────────────┘
```

## 1. Fuerza Bruta (Brute Force)

El atacante prueba **todas las combinaciones posibles** de caracteres hasta encontrar la contraseña correcta.

### Cálculo de Tiempo de Ataque

| Longitud | Caracteres | Combinaciones | Tiempo @ 10 Billones/s |
|----------|------------|---------------|------------------------|
| 6 | minúsculas (26) | 308M | 0.03 segundos |
| 8 | mixto (62) | 218T | 21.8 segundos |
| 10 | mixto (62) | 839Q | 83.9 segundos |
| 12 | mixto (62) | 3.22S | 322 segundos |
| 16 | mixto (62) | 4.76×10²⁸ | 151 años |
| 12 | mixto+símbolos (95) | 5.40×10²³ | 1.7 años |

> **Nota**: Los tiempos asumen hardware moderno (GPU). Con contraseñas hash lentas (Argon2id), estos tiempos se multiplican significativamente.

### Contra Medidas
- Contraseñas largas (≥16 caracteres)
- Argon2id con alta memoria (64MB+)
- Rate limiting en servidor
- Bloqueo tras intentos fallidos

## 2. Ataques de Diccionario

El atacante utiliza **listas de palabras comunes** y variaciones para adivinar contraseñas.

### Listas Populares Utilizadas

| Lista | Tamaño | Origen |
|-------|--------|--------|
| rockyou.txt | 14M passwords | Brecha de RockYou (2009) |
| SecLists/Common-Credentials | 20K | Compilación de breaches |
| HaveIBeenPwned | 600M+ hashes | Agregado de breaches |
| weakpass.com | 1B+ | Múltiples fuentes |

### Variantes del Ataque

```
Diccionario Base:
  password
 Password1!        ← Variación con mayúscula + número + símbolo
  Password123!     ← Añadido de números
  P@ssw0rd!        ← Leet speak
  passw0rd         ← Leet speak simplificado
  Password!        ← Símbolo al final
```

### Contra Medidas
- Prohibir palabras del diccionario en contraseñas
- Verificar contra listas de brechas conocidas (HIBP)
- Mínimo 16 caracteres
- Entropía alta (mezcla de tipos de caracteres)

## 3. Rainbow Tables

Tablas precalculadas que almacenan hash → contraseña para acelerar la búsqueda inversa.

### Cómo Funcionan

```
CONSTRUCCIÓN DE LA TABLE:
┌─────────────┐    Hash    ┌──────────────────────────┐
│ "password"  │───────────►│ a]b4f8e2...  → password  │
│ "123456"    │───────────►│ e10adc39...  → 123456    │
│ "admin"     │───────────►│ 21232f29...  → admin     │
│ ...millones │───────────►│ ...          → ...       │
└─────────────┘            └──────────────────────────┘

ATQUE:
┌─────────────┐    Hash    ┌──────────────────────────┐
│ hash_objetivo│───────────►│ Buscar en la table       │
│ e10adc39... │            │ Match: "123456"          │
└─────────────┘            └──────────────────────────┘
```

### Tiempos de Ataque con Rainbow Tables

| Tipo de Hash | Tiempo de Pre-cálculo | Tiempo de Ataque |
|--------------|----------------------|------------------|
| MD5 (sin salt) | Minutos | Milisegundos |
| SHA-1 (sin salt) | Horas | Milisegundos |
| SHA-256 (sin salt) | Días | Milisegundos |
| MD5 + Salt | Impracticable | Impracticable |
| bcrypt | Impracticable | Impracticable |
| Argon2id | Impracticable | Impracticable |

### Contra Medidas
- **Siempre usar salt** aleatorio único por contraseña
- Usar funciones de hash lentas (bcrypt, Argon2id)
- Los gestores modernos usan PBKDF2/Argon2id que hacen rainbow tables inútiles

## 4. Credential Stuffing

El atacante utiliza credenciales filtradas de **otro sitio** para intentar acceder a cuentas del usuario.

```
SITIO A (BRECHA)              SITIO B (OBJETIVO)
┌─────────────┐               ┌─────────────┐
│ usuario@emp │               │ usuario@emp │
│ MiClave123! │──────────────►│ MiClave123! │  ← Reutilización
└─────────────┘  Credential   └─────────────┘
                Stuffing       Acceso exitoso
```

### Estadísticas
- El **65%** de las personas reutilizan contraseñas
- En 2024, el credential stuffing causó el **40%** de los ataques exitosos
- Los bots automatizados pueden probar miles de credenciales por minuto

### Contra Medidas
- **Nunca reutilizar contraseñas**
- Usar gestor de contraseñas para generar únicas
- MFA en todas las cuentas importantes
- Verificar contra listas de brechas (HIBP)

## 5. Phishing

Ataque de ingeniería social donde el atacante **suplenta** un sitio legítimo para robar credenciales.

### Variantes

| Tipo | Descripción |
|------|-------------|
| **Email Phishing** | Emails masivos con enlaces falsos |
| **Spear Phishing** | Emails dirigidos a personas específicas |
| **Whaling** | Dirigido a ejecutivos de alto nivel |
| **Vishing** | Phishing por teléfono (voice) |
| **Smishing** | Phishing por SMS |
| **Clone Phishing** | Copia exacta de un email legítimo |

### Defensa del Gestor de Contraseñas

```
┌─────────────┐                    ┌─────────────────┐
│  Sitio Falso │                    │  Sitio Real     │
│  (bank-falso │                    │  (banco.com)    │
│   .com)      │                    │                 │
└──────┬──────┘                    └──────┬──────────┘
       │                                  │
       ▼                                  ▼
  Autofill NO                         Autofill SÍ
  aparece (el gestor                  aparece (el gestor
  reconoce que no es                  reconoce el dominio
  el dominio correcto)                correcto)
```

> **Nota**: Esta es una de las **mayores ventajas** de un gestor de contraseñas sobre recordar contraseñas manualmente.

## 6. Keyloggers (Capturadores de Teclado)

Software o hardware que **registra todas las pulsaciones** del teclado.

### Tipos

| Tipo | Ejemplo | Detección |
|------|---------|-----------|
| **Software** | Trojans, rootkits | Antivirus, EDR |
| **Hardware** | Dispositivos USB inline | Inspección física |
| **Kernel** | Rootkits a nivel de kernel | Difícil, requiere forense |
| **API-based** | Hook de teclado | Difícil, ofusca con protectores |

### Defensa del Gestor de Contraseñas
- **Autofill del navegador**: la contraseña se ingresa sin pulsar teclas
- **Biometría**: no se tipea la master password constantemente
- **PIN local**: descifrado con PIN corto en lugar de master password larga

## 7. Side-Channel Attacks (Ataques por Canal Lateral)

Ataques que explotan **información física** del sistema (tiempo, consumo energético, sonido, etc.).

### Ejemplos en Contraseñas

| Ataque | Vector | Dificultad |
|--------|--------|------------|
| **Timing Attack** | Mide tiempo de comparación de hashes | Media |
| **Acoustic Attack** | Sonido del teclado al escribir | Alta |
| **Power Analysis** | Consumo energético del CPU | Alta |
| **Cache-Timing** | Tiempo de acceso a memoria caché | Media-Alta |

### Contra Medidas
- Comparaciones de hash en tiempo constante
- Ofuscación de procesamiento criptográfico
- Hardware con protección contra side-channels

## 8. Ataques a la Sincronización

```
┌──────────┐         ┌──────────┐         ┌──────────┐
│  PC A    │         │ Servidor │         │  PC B    │
└────┬─────┘         └────┬─────┘         └────┬─────┘
     │   Sync             │   Sync             │
     │◄──────────────────►│◄──────────────────►│
     │                    │                    │
     │  Atacante MITM:    │                    │
     │  ┌─────────────────┴─────────────┐     │
     │  │  Intercepta comunicación TLS  │     │
     │  │  (si certificado comprometido) │     │
     │  └───────────────────────────────┘     │
```

### Contra Medidas
- Certificate pinning
- Verificación de certificados TLS
- Cifrado E2E independiente del canal

## Resumen: Top 10 Contramedidas

| # | Contramedida | Protege contra |
|---|--------------|----------------|
| 1 | Contraseñas ≥16 caracteres | Fuerza bruta |
| 2 | Argon2id / PBKDF2 alto | Rainbow tables, fuerza bruta |
| 3 | Nunca reutilizar | Credential stuffing |
| 4 | MFA obligatorio | Phishing, credential stuffing |
| 5 | Autofill del gestor | Phishing, keyloggers |
| 6 | Cifrado E2E | Brechas de servidor |
| 7 | Verificación HIBP | Credential stuffing |
| 8 | Rate limiting | Fuerza bruta online |
| 9 | Biometría/PIN | Keyloggers, shoulder surfing |
| 10 | Backups cifrados | Pérdida de datos |

---

> **Actividad de Reflexión**: Si un atacante obtiene la base de datos de Vaultwarden (hashes + salts), ¿qué ataques podría realizar? ¿Por qué el cifrado E2E lo protege incluso en este escenario?
