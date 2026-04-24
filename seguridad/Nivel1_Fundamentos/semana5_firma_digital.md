# FIRMA DIGITAL - GUÍA COMPLETA

---

## ÍNDICE

1. Conceptos Fundamentales
2. Cómo Funciona la Firma Digital
3. Diferencia entre Hash, Cifrado y Firma Digital
4. Algoritmos de Firma Digital
5. Certificados Digitales y Firma Digital
6. Non-Repudio (No Repudio)
7. Sello de Tiempo (Timestamp)
8. Ejemplos Prácticos en Python
9. Firma Digital con Certificados X.509
10. Aplicaciones Prácticas
11. Comparación: Hash vs Cifrado vs Firma Digital

---

## 1. CONCEPTOS FUNDAMENTALES

### 1.1. ¿Qué es la Firma Digital?

La **firma digital** es un mecanismo criptográfico que permite:

```
┌─────────────────────────────────────────────────────────────────┐
│                    FIRMA DIGITAL - DEFINICIÓN                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ✓ Autenticidad: Verifica QUIÉN envió el mensaje               │
│  ✓ Integridad: Verifica que el mensaje NO fue modificado       │
│  ✓ No Repudio: El emisor NO puede negar haber enviado         │
│                                                                 │
│  A diferencia del hash o cifrado, la firma digital             │
│  utiliza criptografía ASIMÉTRICA (par de claves)               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2. Analogía del Mundo Real

```
┌─────────────────────────────────────────────────────────────────┐
│                   ANALOGÍA: SELLO Y FIRMA NOTARIAL              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  MUNDO FÍSICO:                                                 │
│  ─────────────                                                 │
│  1. Un documento es llevado a un notario                       │
│  2. El notario verifica la identidad del firmante              │
│  3. El notario coloca su SELLO OFICIAL                         │
│  4. El sello demuestra que el documento fue autenticado        │
│  5. El notario NO puede negar haber autenticado                │
│                                                                 │
│  MUNDO DIGITAL:                                                │
│  ────────────                                                  │
│  1. Un mensaje es "firmado" digitalmente                       │
│  2. Se verifica que la clave pública pertenece al emisor       │
│  3. Se aplica el SELLO DIGITAL (firma cifrada)                │
│  4. El sello demuestra autenticidad e integridad               │
│  5. El emisor NO puede negar haber enviado                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 1.3. Diferencia Clave: Cifrado vs Firma Digital

| Aspecto | Cifrado | Firma Digital |
|---------|---------|--------------|
| **Propósito** | Confidencialidad | Autenticidad + Integridad |
| **Clave usada** | Clave pública del receptor | Clave privada del emisor |
| **Quién cifra** | Emisor | Emisor (con su clave privada) |
| **Quién descifra** | Receptor (con clave pública) | Receptor (con clave pública del emisor) |
| **¿Oculta contenido?** | Sí | No (el mensaje va en texto plano) |

---

## 2. CÓMO FUNCIONA LA FIRMA DIGITAL

### 2.1. Proceso Completo

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         PROCESO DE FIRMA DIGITAL                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  EMISOR (Alice)                           RECEPTOR (Bob)                    │
│  ─────────────────                         ─────────────────                 │
│                                                                             │
│      Mensaje original                                                    │
│           │                                                               │
│           ▼                                                               │
│  ┌──────────────────┐                                                    │
│  │  CALCULAR HASH   │  SHA-256(mensaje) = H                             │
│  └────────┬─────────┘                                                    │
│           │                                                              │
│           ▼                                                              │
│  ┌──────────────────┐                                                    │
│  │  CIFRAR HASH     │  cifrar(H, clave_privada_Alice) = FIRMA           │
│  │  (con clave      │                                                    │
│  │   privada)       │                                                    │
│  └────────┬─────────┘                                                    │
│           │                                                              │
│           ▼                                                              │
│      Mensaje + Firma                                                    │
│           │                                                               │
│           └───────────────────────┐                                       │
│                                   │ Canal inseguro                       │
│                                   ▼                                       │
│      Mensaje + Firma                                                    │
│           │                                                               │
│           ▼                                                               │
│  ┌──────────────────┐     ┌──────────────────┐                         │
│  │  DESCIFRAR FIRMA │     │  CALCULAR HASH   │                         │
│  │  (con clave      │     │  del mensaje     │ SHA-256(mensaje) = H'    │
│  │   pública_Alice) │     │  recibido        │                         │
│  └────────┬─────────┘     └────────┬─────────┘                         │
│           │                        │                                      │
│           ▼                        ▼                                      │
│      Hash descifrado           Hash calculado                             │
│           │                        │                                      │
│           └───────────┬────────────┘                                       │
│                       ▼                                                   │
│              ┌──────────────────┐                                        │
│              │  ¿H == H'?      │                                        │
│              └────────┬─────────┘                                        │
│                       │                                                   │
│              ┌────────┴────────┐                                         │
│              │                 │                                          │
│         SÍ ✓                 NO ✗                                       │
│         (Válido)        (Mensaje alterado                               │
│                          o firma falsa)                                   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.2. Paso a Paso Detallado

**En el EMISOR (Alice):**

```
PASO 1: Calcular hash del mensaje
┌─────────────────────────────────────────────────────────────────┐
│ mensaje = "Pagar $1000 a Bob"                                   │
│ hash = SHA-256(mensaje)                                         │
│ hash = "3a5b7c..." (256 bits)                                   │
└─────────────────────────────────────────────────────────────────┘

PASO 2: Cifrar el hash con clave privada
┌─────────────────────────────────────────────────────────────────┐
│ firma = cifrar_RSA(hash, clave_privada_Alice)                   │
│ firma = "9f2e8b..." (firma digital)                            │
└─────────────────────────────────────────────────────────────────┘

PASO 3: Enviar
┌─────────────────────────────────────────────────────────────────┐
│ Enviar: [mensaje] + [firma]                                     │
└─────────────────────────────────────────────────────────────────┘
```

**En el RECEPTOR (Bob):**

```
PASO 4: Obtener clave pública de Alice
┌─────────────────────────────────────────────────────────────────┐
│ (Previamente obtenida de certificado o repositorio de claves)     │
│ clave_publica_Alice = "8d4c1e..."                             │
└─────────────────────────────────────────────────────────────────┘

PASO 5: Descifrar la firma
┌─────────────────────────────────────────────────────────────────┐
│ hash_descifrado = descifrar_RSA(firma, clave_publica_Alice)     │
│ hash_descifrado = "3a5b7c..." (debería ser igual al original)  │
└─────────────────────────────────────────────────────────────────┘

PASO 6: Calcular hash del mensaje recibido
┌─────────────────────────────────────────────────────────────────┐
│ hash_calculado = SHA-256(mensaje_recibido)                      │
│ hash_calculado = "3a5b7c..."                                    │
└─────────────────────────────────────────────────────────────────┘

PASO 7: Comparar
┌─────────────────────────────────────────────────────────────────┐
│ SI hash_descifrado == hash_calculado                            │
│     → Firma VÁLIDA (mensaje auténtico e íntegro)              │
│ SINO                                                             │
│     → Firma INVÁLIDA (mensaje alterado o firma falsificada)    │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. DIFERENCIA ENTRE HASH, CIFRADO Y FIRMA DIGITAL

### 3.1. Comparación Visual

```
┌─────────────────────────────────────────────────────────────────┐
│                    ¿CUÁNDO USAR CADA UNO?                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  PROBLEMA: Quiero enviar un mensaje que solo Bob pueda leer     │
│  SOLUCIÓN: ________________ CIFRADO ________________           │
│            (Confidentiality)                                    │
│                                                                 │
│  PROBLEMA: Quiero que Bob verifique que el mensaje no cambió    │
│  SOLUCIÓN: _________________ HASH __________________           │
│            (Integrity)                                          │
│                                                                 │
│  PROBLEMA: Quiero que Bob sepa que YO envié el mensaje         │
│  SOLUCIÓN: _____________ FIRMA DIGITAL _____________            │
│            (Authentication + Integrity + Non-Repudiation)      │
│                                                                 │
│  PROBLEMA: Quiero todo lo anterior + solo Bob pueda leer        │
│  SOLUCIÓN: ____ CIFRADO + FIRMA DIGITAL (combinados) ____      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2. Tabla Comparativa

| Característica | Hash | Cifrado Simétrico | Cifrado Asimétrico | Firma Digital |
|---------------|------|-------------------|--------------------|----------------|
| **Confidencialidad** | No | Sí | Sí | No |
| **Integridad** | Sí | No | No | Sí |
| **Autenticidad** | No | No | Del receptor | Del emisor |
| **No repudio** | No | No | No | Sí |
| **Clave(s)** | Ninguna | 1 (simétrica) | 2 (públicas/privadas) | 2 (públicas/privadas) |
| **Rendimiento** | Muy rápido | Rápido | Lento | Lento |
| **Uso de clave privada** | No | No | Para descifrar | Para firmar |

### 3.3. Ejemplo Combinado: Cifrado + Firma

```
┌─────────────────────────────────────────────────────────────────┐
│              ENVÍO SEGURO: CIFRADO + FIRMA DIGITAL               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  EMISOR:                                                        │
│  1. Firmo el mensaje con mi clave privada                        │
│  2. Cifro (mensaje + firma) con la clave pública de Bob         │
│  3. Envío el paquete cifrado                                    │
│                                                                 │
│  PAQUETE ENVIADO:                                               │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ [CIFRADO]                                              │    │
│  │   contenido: [mensaje] + [firma]                      │    │
│  │   clave: clave_pública_de_Bob                          │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                 │
│  RECEPTOR:                                                      │
│  1. Descifro con mi clave privada                               │
│  2. Verifico la firma con la clave pública del emisor          │
│  3. Leo el mensaje                                             │
│                                                                 │
│  RESULTADO:                                                     │
│  ✓ Solo Bob puede leer (confidencialidad)                      │
│  ✓ Bob sabe que fui yo (autenticidad)                          │
│  ✓ Bob sabe que no cambió (integridad)                         │
│  ✓ No puedo negar haber enviado (no repudio)                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 4. ALGORITMOS DE FIRMA DIGITAL

### 4.1. Algoritmos Más Comunes

| Algoritmo | Tipo | Tamaño de clave | Uso común |
|-----------|------|-----------------|-----------|
| **RSA** | Asimétrico | 2048-4096 bits | General, certificados X.509 |
| **DSA** | Asimétrico | 1024-3072 bits | Solo firmas digitales |
| **ECDSA** | Curva elíptica | 256-521 bits | Dispositivos móviles, blockchain |
| **EdDSA** | Curva elíptica | 256 bits | Blockchain, mensajes rápidos |
| **RSA-PSS** | Asimétrico | 2048+ bits | Certificados modernos |
| **RSA-PKCS#1 v1.5** | Asimétrico | 2048+ bits | Legacy, aún común |

### 4.2. RSA: El Más Utilizado

```
┌─────────────────────────────────────────────────────────────────┐
│                    FIRMA DIGITAL CON RSA                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ALGORITMO DE FIRMA RSA:                                        │
│  ─────────────────────────────────                              │
│                                                                 │
│  FIRMA:                                                         │
│  firma = mensaje^d mod n                                        │
│           └─ donde (d, n) es la clave privada                   │
│                                                                 │
│  VERIFICACIÓN:                                                  │
│  mensaje' = firma^e mod n                                       │
│             └─ donde (e, n) es la clave pública                  │
│                                                                 │
│  VÁLIDO si mensaje' == hash(mensaje)                           │
│                                                                 │
│  SCHEMA DE RELLENO (Padding):                                   │
│  - PKCS#1 v1.5 (legacy)                                        │
│  - PSS (Probabilistic Signature Scheme) - RECOMENDADO          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 4.3. ECDSA: Más Eficiente

```
┌─────────────────────────────────────────────────────────────────┐
│                 FIRMA DIGITAL CON ECDSA                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Ventajas sobre RSA:                                            │
│  ✓ Claves más pequeñas (256 bits vs 2048 bits)                  │
│  ✓ Firma más corta                                              │
│  ✓ Más rápido de generar                                        │
│  ✓ Ideal para dispositivos con recursos limitados               │
│                                                                 │
│  CURVAS COMUNES:                                                │
│  - P-256 (secp256r1) - NIST                                     │
│  - P-384 (secp384r1) - NIST                                     │
│  - Curve25519 - Recomendada por expertos                        │
│                                                                 │
│  EJEMPLO:                                                       │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ Clave RSA: 2048 bits ≈ 256 bytes                       │    │
│  │ Clave ECDSA (P-256): 256 bits ≈ 32 bytes               │    │
│  │                                                         │    │
│  │ MISMO NIVEL DE SEGURIDAD pero 8x más pequeña          │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 5. CERTIFICADOS DIGITALES Y FIRMA DIGITAL

### 5.1. Relación entre Certificado y Firma

```
┌─────────────────────────────────────────────────────────────────┐
│           CERTIFICADO DIGITAL: LA IDENTIDAD DE LA FIRMA           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  PROBLEMA:                                                     │
│  ¿Cómo sé que la clave pública pertenece realmente a Alice?    │
│                                                                 │
│  SOLUCIÓN:                                                     │
│  Un tercero de confianza (CA) firma digitalmente un           │
│  certificado que dice "esta clave pública pertenece a Alice"    │
│                                                                 │
│  ESTRUCTURA:                                                   │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │               CERTIFICADO X.509                         │    │
│  ├─────────────────────────────────────────────────────────┤    │
│  │                                                         │    │
│  │  Sujeto: CN=Alice, O=Empresa...                       │    │
│  │  Clave pública: 8f4a2b...                            │    │
│  │  Validez: 2024-01-01 → 2025-01-01                    │    │
│  │                                                         │    │
│  │  FIRMA DE LA CA:                                       │    │
│  │  [Firma digital de todo lo anterior con                │    │
│  │   la clave privada de la CA]                           │    │
│  │                                                         │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 5.2. Verificación de Firma con Certificados

```
┌─────────────────────────────────────────────────────────────────────────────┐
│              VERIFICACIÓN COMPLETA DE FIRMA DIGITAL                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ESCENARIO: Alice firma un contrato para Bob                                │
│                                                                             │
│  PASO 1: Alice firma                                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ mensaje = "Contrato de compraventa..."                               │   │
│  │ hash = SHA-256(mensaje)                                            │   │
│  │ firma = RSA_sign(hash, clave_privada_Alice)                        │   │
│  │ certificado_Alice = [CN=Alice, clave_pública_Alice, firma_CA]       │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  PASO 2: Bob verifica                                                     │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ 1. Obtener clave pública de CA (en su TrustStore)                  │   │
│  │ 2. Verificar firma del certificado de Alice:                        │   │
│  │    RSA_verify(firma_CA, clave_pública_CA) → OK                    │   │
│  │    → La clave pública en el certificado ES de Alice                │   │
│  │ 3. Extraer clave pública de Alice del certificado                  │   │
│  │ 4. Verificar firma del mensaje:                                    │   │
│  │    RSA_verify(firma, clave_pública_Alice) → OK                    │   │
│  │    → El mensaje FUE enviado por Alice                              │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  RESULTADO:                                                               │
│  ✓ El mensaje es auténtico (de Alice)                                     │
│  ✓ El mensaje no fue alterado                                             │
│  ✓ Alice no puede negar haberlo enviado                                   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 6. NON-REPUDIO (NO REPUDIO)

### 6.1. ¿Qué es?

```
┌─────────────────────────────────────────────────────────────────┐
│                    NON-REPUDIO (NO REPUDIO)                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  DEFINICIÓN:                                                    │
│  El emisor de un mensaje NO puede negar haberlo enviado         │
│  porque solo ÉL tiene acceso a su clave privada.                 │
│                                                                 │
│  IMPORTANCIA LEGAL:                                             │
│  En muchos países, una firma digital válida tiene el mismo      │
│  valor legal que una firma manuscrita.                          │
│                                                                 │
│  EJEMPLO LEGAL:                                                 │
│  ──────────────                                                 │
│  Alice firma digitalmente un contrato de $100,000.              │
│  Later, decide que quiere negar haberlo firmado.                │
│                                                                 │
│  PERO...                                                        │
│  ✓ La firma digital prueba que solo Alice podía firmar          │
│  ✓ La firma digital prueba que el mensaje no cambió           │
│  ✓ Un juez validaría la firma                                  │
│  ✓ Alice NO puede escapar de su compromiso                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 6.2. Requisitos para Non-Repudio

```
┌─────────────────────────────────────────────────────────────────┐
│           REQUISITOS PARA QUE UNA FIRMA TENGA NON-REPUDIO       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. ████████████████████████ CLAVE PRIVADA SEGURA              │
│     La clave privada debe estar protegida y bajo control        │
│     exclusivo del firmante.                                     │
│                                                                 │
│  2. ████████████████████████ CERTIFICADO VÁLIDO                │
│     El certificado debe estar vigente y no revocado.            │
│                                                                 │
│  3. ████████████████████████ VERIFICACIÓN EXITOSA              │
│     La firma debe verificar correctamente.                      │
│                                                                 │
│  4. ████████████████████████ POLÍTICA DE FIRMA                 │
│     Debe existir un marco legal que reconozca la firma.         │
│     (ej: eIDAS en EU, leyes de firma digital locales)         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 6.3. Casos de Uso Legal

| Sector | Aplicación | Beneficio |
|--------|-------------|-----------|
| **Banca** | Contratos de préstamos digitales | No repudio en transacciones |
| **Gobierno** | Trámites digitales | Eliminación de papel, trazabilidad |
| **Salud** | Recetas y órdenes médicas | Autenticidad de prescriptions |
| **Legal** | Contratos mercantiles | Validez legal igual a firma física |
| **Impuestos** | Declaración de impuestos | No repudio fiscal |

---

## 7. SELLO DE TIEMPO (TIMESTAMP)

### 7.1. ¿Qué es?

```
┌─────────────────────────────────────────────────────────────────┐
│                    SELLO DE TIEMPO (TIMESTAMP)                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  DEFINICIÓN:                                                    │
│  Prueba criptográfica de que datos existían en un momento       │
│  específico.                                                     │
│                                                                 │
│  PROBLEMA QUE RESUELVE:                                         │
│  ¿Cómo probar que un documento fue firmado ANTES de que         │
│  expirara el certificado?                                        │
│                                                                 │
│  SOLUCIÓN:                                                     │
│  Un tercero de confianza (TSA - Time Stamping Authority)        │
│  emite un sello de tiempo que certifica el momento exacto.      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 7.2. Proceso de Sellado de Tiempo

```
┌─────────────────────────────────────────────────────────────────┐
│                 PROCESO DE SELLO DE TIEMPO                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. Alice calcula hash del documento                             │
│     hash = SHA-256(documento)                                   │
│                                                                 │
│  2. Alice envía hash a TSA                                      │
│     TSA = Time Stamping Authority                                │
│                                                                 │
│  3. TSA devuelve:                                               │
│     ┌─────────────────────────────────────────────────────┐    │
│     │  Sello de Tiempo:                                   │    │
│     │  - Hash del documento                               │    │
│     │  - Fecha/hora: 2024-03-15 14:32:45 UTC             │    │
│     │  - Número de serie único                             │    │
│     │  - Firma del TSA                                    │    │
│     └─────────────────────────────────────────────────────┘    │
│                                                                 │
│  4. Alice guarda:                                               │
│     - Documento original                                        │
│     - Sello de tiempo                                           │
│                                                                 │
│  VALIDEZ:                                                       │
│  Aunque el certificado expire, el sello prueba que el            │
│  documento fue firmado cuando el certificado era válido.        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 7.3. Ejemplo de Uso

```
┌─────────────────────────────────────────────────────────────────┐
│              EJEMPLO: FIRMA DIGITAL CON SELLO DE TIEMPO           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ESCENARIO:                                                     │
│  Alice firma un documento el 15 de marzo de 2024                │
│  Su certificado CADUCA el 30 de marzo de 2024                   │
│  En 2025, ella quiere negar haber firmado                       │
│                                                                 │
│  VERIFICACIÓN:                                                  │
│  1. Certificado de Alice: válido hasta 30/03/2024               │
│  2. Sello de tiempo: 15/03/2024 14:32:45 UTC                   │
│  3. Sello de tiempo < Fecha de expiración ✓                     │
│                                                                 │
│  CONCLUSIÓN:                                                    │
│  La firma fue hecha mientras el certificado era válido.          │
│  El sello de tiempo lo prueba criptográficamente.               │
│  Alice NO puede negar la firma.                                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 8. EJEMPLOS PRÁCTICOS EN PYTHON

### 8.1. Firma Digital Básica con RSA

```python
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, NoEncryption

# ============================================
# PASO 1: GENERAR PAR DE CLAVES RSA
# ============================================

clave_privada = rsa.generate_private_key(
    public_exponent=65537,  # Usualmente 65537
    key_size=2048           # Mínimo recomendado: 2048 bits
)
clave_publica = clave_privada.public_key()

print("✓ Par de claves RSA generado")

# Guardar clave privada (en producción, proteger con contraseña)
with open("clave_privada.pem", "wb") as f:
    f.write(clave_privada.private_bytes(
        encoding=Encoding.PEM,
        format=PrivateFormat.PKCS8,
        encryption_algorithm=NoEncryption()
    ))

# ============================================
# PASO 2: EMISOR FIRMA EL MENSAJE
# ============================================

mensaje = b"""
CONTRATO DE PRESTAMO
====================
Monto: $50,000 USD
Plazo: 24 meses
Tasa: 12% anual
Deudor: Roberto Martinez
Acreedor: Banco XYZ
Fecha: 15 de Marzo de 2024
"""

# Calcular hash del mensaje
from cryptography.hazmat.primitives.asymmetric import utils

# Firmar con RSA-PSS (más seguro que PKCS#1 v1.5)
firma = clave_privada.sign(
    mensaje,
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),  # Función de máscara
        salt_length=padding.PSS.MAX_LENGTH     # Longitud máxima de sal
    ),
    hashes.SHA256()
)

print(f"✓ Mensaje firmado")
print(f"  Hash (SHA-256): {hashes.SHA256()._algorithm_ctx}")
print(f"  Longitud firma: {len(firma)} bytes")

# ============================================
# PASO 3: RECEPTOR VERIFICA LA FIRMA
# ============================================

try:
    clave_publica.verify(
        firma,
        mensaje,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    print("✓ FIRMA VÁLIDA - Mensaje auténtico e íntegro")

except Exception as e:
    print(f"✗ FIRMA INVÁLIDA: {e}")

# ============================================
# PASO 4: PRUEBA - MENSAJE MODIFICADO
# ============================================

mensaje_modificado = b"""
CONTRATO DE PRESTAMO
====================
Monto: $500,000 USD  <-- ALTERADO!
Plazo: 24 meses
Tasa: 12% anual
Deudor: Roberto Martinez
Acreedor: Banco XYZ
Fecha: 15 de Marzo de 2024
"""

try:
    clave_publica.verify(
        firma,
        mensaje_modificado,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    print("✓ Firma válida (INCORRECTO)")
except Exception as e:
    print(f"✗ FIRMA INVÁLIDA - El mensaje fue alterado: {e}")
```

### 8.2. Firma Digital con ECDSA

```python
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

# ============================================
# FIRMA DIGITAL CON ECDSA (más eficiente)
# ============================================

# Generar claves ECDSA usando curva P-256
clave_privada = ec.generate_private_key(ec.SECP256R1(), default_backend())
clave_publica = clave_privada.public_key()

# Mensaje a firmar
mensaje = b"Transferencia de $10,000 a cuenta 123456789"

# FIRMA
firma = clave_privada.sign(
    mensaje,
    ec.ECDSA(hashes.SHA256())
)

print(f"✓ Mensaje firmado con ECDSA")
print(f"  Algoritmo: ECDSA con curva P-256 (secp256r1)")
print(f"  Hash: SHA-256")
print(f"  Longitud firma: {len(firma)} bytes")

# VERIFICACIÓN
try:
    clave_publica.verify(firma, mensaje, ec.ECDSA(hashes.SHA256()))
    print("✓ FIRMA VÁLIDA")
except Exception as e:
    print(f"✗ FIRMA INVÁLIDA: {e}")
```

### 8.3. Comparación RSA vs ECDSA

```python
import time
from cryptography.hazmat.primitives.asymmetric import rsa, ec
from cryptography.hazmat.primitives import hashes

# ============================================
# COMPARACIÓN DE RENDIMIENTO
# ============================================

mensaje = b"Mensaje de prueba para comparar algoritmos" * 100

# RSA-2048
inicio = time.time()
clave_rsa = rsa.generate_private_key(public_exponent=65537, key_size=2048)
firma_rsa = clave_rsa.sign(mensaje, padding.PKCS1(), hashes.SHA256())
tiempo_rsa = time.time() - inicio

# ECDSA P-256
inicio = time.time()
clave_ec = ec.generate_private_key(ec.SECP256R1())
firma_ec = clave_ec.sign(mensaje, ec.ECDSA(hashes.SHA256()))
tiempo_ec = time.time() - inicio

print(f"""
╔══════════════════════════════════════════════════════════════╗
║           COMPARACIÓN RSA vs ECDSA                          ║
╠══════════════════════════════════════════════════════════════╣
║  RSA-2048:              {tiempo_rsa:.4f}s    │ Clave: 2048 bits  ║
║  ECDSA P-256:            {tiempo_ec:.4f}s    │ Clave: 256 bits   ║
╠══════════════════════════════════════════════════════════════╣
║  ECDSA es ~{tiempo_rsa/tiempo_ec:.1f}x más rápido                                ║
║  Con el MISMO nivel de seguridad                             ║
╚══════════════════════════════════════════════════════════════╝
""")
```

---

## 9. FIRMA DIGITAL CON CERTIFICADOS X.509

### 9.1. Crear CA y Certificado para Firma

```python
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import datetime

# ============================================
# PASO 1: CREAR CA (AUTORIDAD CERTIFICADORA)
# ============================================

# Generar clave de la CA
ca_clave_privada = rsa.generate_private_key(public_exponent=65537, key_size=4096)
ca_clave_publica = ca_clave_privada.public_key()

# Crear certificado de la CA
ca_certificado = (
    x509.CertificateBuilder()
    .subject_name(x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "UY"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Montevideo"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Mi CA Personal"),
        x509.NameAttribute(NameOID.COMMON_NAME, "Mi CA Raíz"),
    ]))
    .issuer_name(x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "UY"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Mi CA Personal"),
        x509.NameAttribute(NameOID.COMMON_NAME, "Mi CA Raíz"),
    ]))
    .public_key(ca_clave_publica)
    .serial_number(x509.random_serial_number())
    .not_valid_before(datetime.datetime.utcnow())
    .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=3650))  # 10 años
    .add_extension(
        x509.BasicConstraints(ca=True, path_length=None),
        critical=True,
    )
    .add_extension(
        x509.KeyUsage(
            digital_signature=True,
            key_cert_sign=True,
            crl_sign=True,
            key_encipherment=False,
            content_commitment=False,
            data_encipherment=False,
            key_agreement=False,
            encipher_only=False,
            decipher_only=False,
        ),
        critical=True,
    )
    .sign(ca_clave_privada, hashes.SHA256())
)

print("✓ CA creada con certificado autofirmado")

# Guardar CA
with open("mi_ca.crt", "wb") as f:
    f.write(ca_certificado.public_bytes(serialization.Encoding.PEM))

# ============================================
# PASO 2: CREAR CERTIFICADO PARA ALICE
# ============================================

# Clave de Alice
alice_clave_privada = rsa.generate_private_key(public_exponent=65537, key_size=2048)
alice_clave_publica = alice_clave_privada.public_key()

# Crear CSR (Certificate Signing Request) - simplificado aquí
# En producción usaríamos un CSR formal

# Crear certificado de Alice firmado por la CA
alice_certificado = (
    x509.CertificateBuilder()
    .subject_name(x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "UY"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Empresa XYZ"),
        x509.NameAttribute(NameOID.COMMON_NAME, "Alice García"),
        x509.NameAttribute(NameOID.EMAIL_ADDRESS, "alice@ejemplo.com"),
    ]))
    .issuer_name(ca_certificado.subject)  # Firmado por la CA
    .public_key(alice_clave_publica)
    .serial_number(x509.random_serial_number())
    .not_valid_before(datetime.datetime.utcnow())
    .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=365))  # 1 año
    .add_extension(
        x509.BasicConstraints(ca=False, path_length=None),
        critical=True,
    )
    .add_extension(
        x509.KeyUsage(
            digital_signature=True,    # ← PUEDE FIRMAR DIGITALMENTE
            content_commitment=True,   # ← PUEDE FIRMAR PARA NO-REPUDIO
            key_encipherment=False,
            data_encipherment=False,
            key_agreement=False,
            key_cert_sign=False,
            crl_sign=False,
            encipher_only=False,
            decipher_only=False,
        ),
        critical=True,
    )
    .sign(ca_clave_privada, hashes.SHA256())
)

print("✓ Certificado de Alice creado (firmado por CA)")

# Guardar certificado de Alice
with open("alice.crt", "wb") as f:
    f.write(alice_certificado.public_bytes(serialization.Encoding.PEM))

# Guardar clave de Alice (PROTEGE ESTO!)
with open("alice_clave_privada.key", "wb") as f:
    f.write(alice_clave_privada.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.BestAvailableEncryption(b"contraseña_segura")
    ))
```

### 9.2. Verificar Firma con Certificado

```python
from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.x509.oid import SignatureAlgorithmOID

# Cargar certificados
with open("mi_ca.crt", "rb") as f:
    ca_cert = x509.load_pem_x509_certificate(f.read())

with open("alice.crt", "rb") as f:
    alice_cert = x509.load_pem_x509_certificate(f.read())

# ============================================
# VERIFICAR FIRMA CON CERTIFICADO
# ============================================

def verificar_firma_con_certificado(mensaje, firma, certificado, ca_cert):
    """Verifica una firma digital usando un certificado X.509"""

    # 1. Verificar que el certificado fue firmado por la CA
    try:
        ca_cert.public_key().verify(
            certificado.signature,
            certificado.tbs_certificate_bytes,
            padding.PKCS1(hashes.SHA256())
        )
        print("✓ Certificado de Alice es válido (firmado por CA)")
    except Exception as e:
        print(f"✗ Certificado inválido: {e}")
        return False

    # 2. Verificar que el certificado no ha expirado
    ahora = datetime.datetime.utcnow()
    if ahora < certificado.not_valid_before_utc or ahora > certificado.not_valid_after_utc:
        print("✗ Certificado expirado")
        return False
    print("✓ Certificado vigente")

    # 3. Verificar propósito de la firma
    key_usage = certificado.extensions.get_extension_for_class(x509.KeyUsage)
    if not key_usage.value.digital_signature:
        print("✗ Certificado no puede usarse para firma digital")
        return False
    print("✓ Certificado tiene capacidad de firma digital")

    # 4. Verificar la firma del mensaje
    try:
        certificado.public_key().verify(
            firma,
            mensaje,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        print("✓ FIRMA VÁLIDA - El mensaje fue firmado por el titular del certificado")
        return True
    except Exception as e:
        print(f"✗ FIRMA INVÁLIDA: {e}")
        return False

# Ejemplo de uso
# mensaje = b"Contrato..."
# firma = ...  # La firma de Alice
# verificar_firma_con_certificado(mensaje, firma, alice_cert, ca_cert)
```

---

## 10. APLICACIONES PRÁCTICAS

### 10.1. Firmar Documentos PDF

```python
# Usando PyPDF2 y cryptography (ejemplo conceptual)
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography import x509
import datetime

def firmar_pdf(ruta_pdf, clave_privada, certificado):
    """
    Firma digitalmente un PDF (ejemplo simplificado)
    En producción usar bibliotecas como PyPDF2 o pikepdf
    """

    # 1. Leer el PDF
    with open(ruta_pdf, "rb") as f:
        contenido_pdf = f.read()

    # 2. Calcular hash del PDF
    hash_pdf = hashes.Hash(hashes.SHA256())
    hash_pdf.update(contenido_pdf)
    digest = hash_pdf.finalize()

    # 3. Firmar el hash
    firma = clave_privada.sign(
        digest,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    # 4. Crear objeto de firma (en producción, incrustar en PDF)
    firma_digital = {
        "pdf_hash": digest.hex(),
        "firma": firma.hex(),
        "certificado": certificado.public_bytes(
            cryptography.hazmat.primitives.serialization.Encoding.DER
        ),
        "fecha": datetime.datetime.utcnow().isoformat(),
        "algoritmo": "RSA-PSS with SHA-256"
    }

    return firma_digital

def verificar_pdf(ruta_pdf, firma_digital, certificado):
    """Verifica la firma de un PDF"""

    # 1. Leer PDF
    with open(ruta_pdf, "rb") as f:
        contenido_pdf = f.read()

    # 2. Recalcular hash
    hash_pdf = hashes.Hash(hashes.SHA256())
    hash_pdf.update(contenido_pdf)
    digest_actual = hash_pdf.finalize()

    # 3. Verificar coincide con hash firmado
    digest_firmado = bytes.fromhex(firma_digital["pdf_hash"])

    if digest_actual != digest_firmado:
        return False, "El PDF ha sido modificado"

    # 4. Verificar firma del hash
    try:
        certificado.public_key().verify(
            bytes.fromhex(firma_digital["firma"]),
            digest_firmado,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True, "Firma válida"
    except:
        return False, "Firma inválida"
```

### 10.2. Firmar Mensajes en APIs

```python
# Ejemplo: Firmar mensajes en una API REST
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
import base64
import json
import time

class FirmadorMensajes:
    """Clase para firmar mensajes de API"""

    def __init__(self, clave_privada_path, certificado_path):
        # Cargar clave privada (protegida con passphrase)
        with open(clave_privada_path, "rb") as f:
            self.clave_privada = serialization.load_pem_private_key(
                f.read(),
                password=None  # En producción: password.encode()
            )

        # Cargar certificado
        with open(certificado_path, "rb") as f:
            self.certificado = x509.load_pem_x509_certificate(f.read())

    def crear_firma(self, payload):
        """
        Crea un payload firmado para API
        Incluye: timestamp, nonce, payload, firma
        """

        # Generar nonce único
        nonce = os.urandom(16).hex()

        # Timestamp actual
        timestamp = int(time.time())

        # Crear mensaje a firmar
        mensaje = json.dumps({
            "nonce": nonce,
            "timestamp": timestamp,
            "payload": payload
        }, sort_keys=True)

        # Calcular hash
        hash_mensaje = hashes.Hash(hashes.SHA256())
        hash_mensaje.update(mensaje.encode())
        digest = hash_mensaje.finalize()

        # Firmar hash
        firma = self.clave_privada.sign(
            digest,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

        # Construir envelope
        envelope = {
            "nonce": nonce,
            "timestamp": timestamp,
            "payload": payload,
            "firma": base64.b64encode(firma).decode(),
            "certificado": self.certificado.public_bytes(
                serialization.Encoding.DER
            ).hex()
        }

        return envelope

    @staticmethod
    def verificar_firma(envelope, clave_publica):
        """Verifica una firma de API"""

        # Extraer componentes
        nonce = envelope["nonce"]
        timestamp = envelope["timestamp"]
        payload = envelope["payload"]
        firma = base64.b64decode(envelope["firma"])

        # Verificar timestamp (no mayor a 5 minutos)
        ahora = int(time.time())
        if abs(ahora - timestamp) > 300:
            return False, "Timestamp expirado"

        # Reconstruir mensaje
        mensaje = json.dumps({
            "nonce": nonce,
            "timestamp": timestamp,
            "payload": payload
        }, sort_keys=True)

        # Calcular hash
        hash_mensaje = hashes.Hash(hashes.SHA256())
        hash_mensaje.update(mensaje.encode())
        digest = hash_mensaje.finalize()

        # Verificar firma
        try:
            clave_publica.verify(firma, digest, padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ), hashes.SHA256())
            return True, "Firma válida"
        except:
            return False, "Firma inválida"

# Uso:
# firmador = FirmadorMensajes("mi_clave.key", "mi_cert.crt")
# mensaje = {"action": "transferir", "monto": 1000}
# envelope = firmador.crear_firma(mensaje)
```

### 10.3. Firmar Transacciones de Blockchain (Concepto)

```python
# Conceptual: Cómo funcionan las firmas en blockchain
# (simplificado para Bitcoin/ Ethereum)

from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes, serialization

def generar_par_claves_blockchain():
    """Genera clave para wallet de blockchain"""

    # Usar curva elíptica secp256k1 (la de Bitcoin)
    clave_privada = ec.generate_private_key(ec.SECP256K1())

    # La clave pública se deriva matemáticamente
    clave_publica = clave_privada.public_key()

    # En blockchain, la dirección se deriva de la clave pública
    # (hash + encoding específico)
    return clave_privada, clave_publica

def firmar_transaccion(transaccion, clave_privada):
    """
    Firma una transacción de blockchain
    """

    # La transacción se "serializa" a bytes
    datos_transaccion = serializar_transaccion(transaccion)

    # Se calcula hash
    hash_tx = hashes.Hash(hashes.SHA256())
    hash_tx.update(datos_transaccion)
    digest = hash_tx.finalize()

    # Se firma con clave privada (usando ECDSA)
    firma = clave_privada.sign(
        digest,
        ec.ECDSA(hashes.SHA256())
    )

    return firma

# En Bitcoin, la firma sigue el formato DER
# y se combina con el flag SIGHASH para indicar qué partes se firman
```

---

## 11. COMPARACIÓN FINAL: HASH vs CIFRADO vs FIRMA DIGITAL

```
┌────────────────────────────────────────────────────────────────────────────────┐
│                           COMPARACIÓN COMPLETA                                   │
├────────────────────────────────────────────────────────────────────────────────┤
│                                                                                │
│  ╔═══════════════════════════════════════════════════════════════════════════╗ │
│  ║                          HASH (Resumen)                                   ║ │
│  ╠═══════════════════════════════════════════════════════════════════════════╣ │
│  ║ Input:  "Hola mundo" (cualquier tamaño)                                  ║ │
│  ║ Output: "a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9..."   ║ │
│  ║                   (256 bits - tamaño fijo)                                ║ │
│  ╠═══════════════════════════════════════════════════════════════════════════╣ │
│  ║ Propósito: INTEGRIDAD                                                    ║ │
│  ║ ¿Puedo saber quién lo escribió?        NO                               ║ │
│  ║ ¿Puedo saber si cambió?                SÍ                               ║ │
│  ║ ¿Oculta el contenido?                   NO                               ║ │
│  ║ ¿Se puede revertir?                     NO (unidireccional)             ║ │
│  ╚═══════════════════════════════════════════════════════════════════════════╝ │
│                                                                                │
│  ╔═══════════════════════════════════════════════════════════════════════════╗ │
│  ║                      CIFRADO ASIMÉTRICO                                   ║ │
│  ╠═══════════════════════════════════════════════════════════════════════════╣ │
│  ║ Cifrar:   datos + clave_pública_receptor → texto_cifrado                ║ │
│  ║ Descifrar: texto_cifrado + clave_privada_receptor → datos               ║ │
│  ╠═══════════════════════════════════════════════════════════════════════════╣ │
│  ║ Propósito: CONFIDENCIALIDAD                                             ║ │
│  ║ ¿Puedo saber quién lo escribió?        NO                               ║ │
│  ║ ¿Puedo saber si cambió?                NO                               ║ │
│  ║ ¿Oculta el contenido?                   SÍ                               ║ │
│  ║ ¿Solo el receptor puede leer?            SÍ                               ║ │
│  ╚═══════════════════════════════════════════════════════════════════════════╝ │
│                                                                                │
│  ╔═══════════════════════════════════════════════════════════════════════════╗ │
│  ║                       FIRMA DIGITAL                                       ║ │
│  ╠═══════════════════════════════════════════════════════════════════════════╣ │
│  ║ Firmar:   hash(datos) + clave_privada_emisor → firma                    ║ │
│  ║ Verificar: firma + clave_pública_emisor → ¿hash(datos)==hash(original)? ║ │
│  ╠═══════════════════════════════════════════════════════════════════════════╣ │
│  ║ Propósito: AUTENTICIDAD + INTEGRIDAD + NO-REPUDIO                       ║ │
│  ║ ¿Puedo saber quién lo escribió?        SÍ                               ║ │
│  ║ ¿Puedo saber si cambió?                SÍ                               ║ │
│  ║ ¿Oculta el contenido?                   NO                               ║ │
│  ║ ¿El emisor puede negar?                 NO                               ║ │
│  ╚═══════════════════════════════════════════════════════════════════════════╝ │
│                                                                                │
│  ╔═══════════════════════════════════════════════════════════════════════════╗ │
│  ║              CIFRADO + FIRMA DIGITAL (Combinados)                        ║ │
│  ╠═══════════════════════════════════════════════════════════════════════════╣ │
│  ║ 1. Firmar datos con clave_privada_emisor                                ║ │
│  ║ 2. Crear paquete = [datos] + [firma]                                    ║ │
│  ║ 3. Cifrar paquete con clave_pública_receptor                             ║ │
│  ╠═══════════════════════════════════════════════════════════════════════════╣ │
│  ║ Propósito: TODO - CONFIDENCIALIDAD + AUTENTICIDAD + INTEGRIDAD         ║ │
│  ║ ✓ Solo el receptor lee el contenido                                      ║ │
│  ║ ✓ El receptor sabe quién envió                                            ║ │
│  ║ ✓ El receptor sabe que no cambió                                         ║ │
│  ║ ✓ El emisor no puede negar                                                ║ │
│  ╚═══════════════════════════════════════════════════════════════════════════╝ │
│                                                                                │
└────────────────────────────────────────────────────────────────────────────────┘
```

---

## RESUMEN RÁPIDO

```
┌─────────────────────────────────────────────────────────────────┐
│                    FIRMA DIGITAL - RESUMEN                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ¿QUÉ ES?:                                                      │
│  Mecanismo criptográfico que prueba AUTENTICIDAD, INTEGRIDAD     │
│  y NON-REPUDIO de un mensaje o documento digital.               │
│                                                                 │
│  ¿CÓMO FUNCIONA?:                                               │
│  1. Calcular hash del mensaje                                    │
│  2. Cifrar hash con CLAVE PRIVADA del emisor                    │
│  3. Enviar mensaje + firma                                      │
│  4. Receptor descifra firma con CLAVE PÚBLICA del emisor        │
│  5. Receptor compara: hash_descifrado == hash_calculado         │
│                                                                 │
│  ¿QUÉ GARANTIZA?:                                               │
│  ✓ Autenticidad: ¿Quién envió? (la clave pública lo identifica)│
│  ✓ Integridad: ¿Cambió el mensaje? (hashs diferentes)         │
│  ✓ No repudio: ¿Puede negar? (solo él tiene la clave privada) │
│                                                                 │
│  ALGORITMOS:                                                    │
│  • RSA (2048+ bits) - Más común                                  │
│  • ECDSA (256+ bits) - Más eficiente                            │
│  • DSA (solo firmas)                                            │
│                                                                 │
│  APLICACIONES:                                                  │
│  • Contratos digitales                                           │
│  • Facturación electrónica                                       │
│  • Software firmado                                              │
│  • Transacciones bancarias                                       │
│  • Documentos legales                                            │
│                                                                 │
│  CERTIFICADOS X.509:                                            │
│  Vinculan una clave pública a una identidad real.                │
│  Son firmados por una CA de confianza.                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

**Documento creado:** Firma Digital - Guía Completa  
**Extracted from:** Nivel1_Fundamentos/semana_2.md  
**Fecha:** 2026
