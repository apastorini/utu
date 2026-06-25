# Clase 29: Criptografia Aplicada para Desarrolladores

**Numero de clase:** 19
**Duracion:** 2 horas

## Objetivos de Aprendizaje

- Diferenciar entre hash, cifrado y codificacion
- Implementar hashing seguro de contrasenas con bcrypt, argon2 y scrypt
- Implementar cifrado simetrico autenticado con AES-256-GCM
- Comprender los usos de RSA, ECC, HMAC y firmas digitales
- Identificar algoritmos criptograficos debiles (MD5, SHA-1, DES) y reemplazarlos

## Contenido Detallado

### 1. Hash vs Cifrado vs Codificacion

| Operacion | Direccion | Clave | Uso principal |
|-----------|-----------|-------|---------------|
| Hash | Unidireccional | No | Contrasenas, integridad |
| Cifrado | Bidireccional | Si | Confidencialidad |
| Codificacion | Bidireccional | No | Representacion de datos |

**Hash:** Funcion unidireccional. Dado un input, produce un output de longitud fija. No se puede revertir.
- Ejemplos: SHA-256, bcrypt, argon2

**Cifrado:** Transformacion reversible usando una clave.
- Simetrico: misma clave para cifrar y descifrar (AES)
- Asimetrico: claves publica y privada (RSA, ECC)

**Codificacion:** Transformacion sin secreto, totalmente reversible sin clave.
- Ejemplos: Base64, Hex, UTF-8

### 2. Hashing Seguro para Contrasenas

**Caracteristicas de un hash de contrasena:**
- Salt unico por contrasena (previene rainbow tables)
- Factor de costo/work factor (hace lento el ataque de fuerza bruta)
- Resistente a ASIC/GPU (consume mucha memoria)

**Algoritmos recomendados:**
- **Argon2id:** Ganador del Password Hashing Competition (PHC). Mas recomendado.
- **bcrypt:** Ampliamente usado, resistente a FPGA/GPU.
- **scrypt:** Disenado para ser costoso en memoria.

**NO usar:** MD5, SHA-1, SHA-256 (sin salt) para contrasenas.

### 3. Cifrado Simetrico: AES-GCM

AES-GCM (Galois/Counter Mode) proporciona:
- **Confidencialidad:** El mensaje esta cifrado
- **Integridad:** El mensaje no ha sido modificado
- **Autenticacion:** El mensaje proviene de quien tiene la clave

**Componentes:**
- Clave: 256 bits
- IV (Nonce): 12 bytes (recomendado), unico por operacion
- Tag de autenticacion: verifica integridad

### 4. Cifrado Asimetrico

**RSA:** 
- Usa clave publica/privada basada en factorizacion de numeros primos grandes
- Usos: intercambio de claves, firmas digitales
- Tamano minimo recomendado: 2048 bits

**ECC (Elliptic Curve Cryptography):**
- Seguridad equivalente a RSA con claves mucho mas pequenas
- Curva recomendada: Curve25519 (X25519 para intercambio, Ed25519 para firmas)

### 5. Firmas Digitales y HMAC

**Firma digital (RSA/ECDSA):**
- El emisor firma con su clave privada
- Cualquiera verifica con la clave publica del emisor
- Garantiza autenticidad y no repudio

**HMAC (Hash-based Message Authentication Code):**
- Usa una clave secreta compartida + funcion hash
- Garantiza integridad y autenticacion
- No provee no repudio (la clave es compartida)

### 6. Regla de Oro: NO Inventar Criptografia Propia

Razones:
- Los algoritmos criptograficos requieren anos de analisis matematico
- Implementaciones caseras casi siempre tienen vulnerabilidades
- Usar librerias probadas (cryptography, PyCryptodome, libsodium)

## Ejercicio 1: Cifrado AES-256-GCM en Python con Autenticacion

```python
# aes_gcm.py - Cifrado autenticado con AES-256-GCM
import os
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.exceptions import InvalidTag


class CifradorAESGCM:
    """
    Implementacion de cifrado simetrico autenticado con AES-256-GCM.
    Proporciona confidencialidad, integridad y autenticacion.
    """

    KEY_SIZE = 32      # 256 bits
    NONCE_SIZE = 12    # 96 bits (recomendado para GCM)

    @staticmethod
    def generar_clave() -> bytes:
        """Genera una clave AES de 256 bits segura."""
        return AESGCM.generate_key(bit_length=256)

    @staticmethod
    def _generar_nonce() -> bytes:
        """Genera un nonce de 12 bytes criptograficamente seguro."""
        return os.urandom(CifradorAESGCM.NONCE_SIZE)

    @staticmethod
    def cifrar(clave: bytes, datos_planos: bytes, aad: bytes = None) -> dict:
        """
        Cifra datos con AES-256-GCM.

        Args:
            clave: Clave de 32 bytes
            datos_planos: Datos a cifrar (bytes)
            aad: Additional Authenticated Data (opcional)

        Returns:
            dict con nonce, ciphertext, tag (todos en base64)
        """
        if len(clave) != CifradorAESGCM.KEY_SIZE:
            raise ValueError(f"Clave debe ser de {CifradorAESGCM.KEY_SIZE} bytes")

        aesgcm = AESGCM(clave)
        nonce = CifradorAESGCM._generar_nonce()

        # cifrar retorna nonce || ciphertext || tag concatenados
        ciphertext = aesgcm.encrypt(nonce, datos_planos, aad or b"")

        # ciphertext incluye nonce al inicio en la version de hazmat
        # pero nosotros manejamos nonce por separado para mayor control
        return {
            'nonce': base64.b64encode(nonce).decode('utf-8'),
            'ciphertext': base64.b64encode(ciphertext).decode('utf-8'),
            'aad': base64.b64encode(aad).decode('utf-8') if aad else None
        }

    @staticmethod
    def descifrar(clave: bytes, datos_cifrados: dict, aad: bytes = None) -> bytes:
        """
        Descifra datos cifrados con AES-256-GCM.

        Args:
            clave: Clave de 32 bytes
            datos_cifrados: dict con nonce, ciphertext (base64)
            aad: Additional Authenticated Data (opcional)

        Returns:
            bytes con los datos descifrados

        Raises:
            InvalidTag: Si el tag de autenticacion no coincide
        """
        if len(clave) != CifradorAESGCM.KEY_SIZE:
            raise ValueError(f"Clave debe ser de {CifradorAESGCM.KEY_SIZE} bytes")

        nonce = base64.b64decode(datos_cifrados['nonce'])
        ciphertext = base64.b64decode(datos_cifrados['ciphertext'])

        if len(nonce) != CifradorAESGCM.NONCE_SIZE:
            raise ValueError(f"Nonce debe ser de {CifradorAESGCM.NONCE_SIZE} bytes")

        aesgcm = AESGCM(clave)

        try:
            datos_planos = aesgcm.decrypt(nonce, ciphertext, aad or b"")
            return datos_planos
        except InvalidTag:
            raise ValueError("ERROR: El tag de autenticacion no coincide. "
                             "Los datos pueden haber sido modificados o la clave es incorrecta.")

    @staticmethod
    def cifrar_texto(clave: bytes, texto: str, aad: str = None) -> dict:
        """Cifra un string de texto."""
        return CifradorAESGCM.cifrar(
            clave,
            texto.encode('utf-8'),
            aad.encode('utf-8') if aad else None
        )

    @staticmethod
    def descifrar_texto(clave: bytes, datos_cifrados: dict, aad: str = None) -> str:
        """Descifra a string de texto."""
        datos = CifradorAESGCM.descifrar(
            clave,
            datos_cifrados,
            aad.encode('utf-8') if aad else None
        )
        return datos.decode('utf-8')


# ============================================================
# EJEMPLO DE USO
# ============================================================
if __name__ == '__main__':
    print("=" * 60)
    print("Cifrado AES-256-GCM - Demostracion")
    print("=" * 60)

    # 1. Generar clave
    clave = CifradorAESGCM.generar_clave()
    print(f"\n[1] Clave generada: {base64.b64encode(clave).decode()[:20]}...")

    # 2. Cifrar un mensaje
    mensaje = "Este es un mensaje secreto. Datos sensibles: API_KEY=sk-12345"
    aad = "metadata:usuario=juan"

    print(f"\n[2] Mensaje original: {mensaje}")
    print(f"    AAD: {aad}")

    cifrado = CifradorAESGCM.cifrar_texto(clave, mensaje, aad)
    print(f"\n[3] Datos cifrados:")
    print(f"    Nonce: {cifrado['nonce'][:20]}...")
    print(f"    Ciphertext: {cifrado['ciphertext'][:30]}...")
    print(f"    AAD: {cifrado['aad']}")

    # 3. Descifrar
    descifrado = CifradorAESGCM.descifrar_texto(clave, cifrado, aad)
    print(f"\n[4] Descifrado correcto: {descifrado}")

    # 4. Probar con AAD incorrecto (debe fallar)
    print(f"\n[5] Prueba de integridad:")
    try:
        CifradorAESGCM.descifrar_texto(clave, cifrado, "aad_incorrecto")
        print("    ERROR: Deberia haber lanzado excepcion")
    except ValueError as e:
        print(f"    OK: Integridad protegida - {str(e)[:50]}...")

    # 5. Probar con clave incorrecta (debe fallar)
    try:
        clave_incorrecta = CifradorAESGCM.generar_clave()
        CifradorAESGCM.descifrar_texto(clave_incorrecta, cifrado, aad)
        print("    ERROR: Deberia haber lanzado excepcion")
    except ValueError as e:
        print(f"    OK: Clave incorrecta rechazada - {str(e)[:50]}...")

    # 6. Cifrar datos binarios (ej: un JSON)
    import json
    datos_json = json.dumps({
        "usuario": "admin",
        "rol": "administrador",
        "permisos": ["leer", "escribir", "eliminar"]
    })
    cifrado_json = CifradorAESGCM.cifrar(clave, datos_json.encode('utf-8'))
    descifrado_json = CifradorAESGCM.descifrar(clave, cifrado_json)
    print(f"\n[6] Cifrado de JSON:")
    print(f"    Original: {datos_json[:50]}...")
    print(f"    Descifrado: {descifrado_json.decode()[:50]}...")
```

## Ejercicio 2: Hash de Contrasenas con Bcrypt y Verificacion

```python
# password_hashing.py - Hashing seguro de contrasenas con bcrypt, argon2 y scrypt
import bcrypt
import hashlib
import secrets
import string


class HashPasswordBcrypt:
    """
    Implementacion de hashing de contrasenas usando bcrypt.
    bcrypt incluye automaticamente un salt unico y un factor de costo.
    """

    # Factor de costo (2^12 = 4096 iteraciones)
    # A mayor costo, mas seguro pero mas lento
    ROUNDS = 12

    @staticmethod
    def generar_hash(contrasena: str) -> str:
        """
        Genera un hash bcrypt de una contrasena.

        Args:
            contrasena: Contrasena en texto plano

        Returns:
            String con el hash (incluye algoritmo, costo, salt y hash)
        """
        if not contrasena or len(contrasena) < 8:
            raise ValueError("La contrasena debe tener al menos 8 caracteres")

        contrasena_bytes = contrasena.encode('utf-8')
        salt = bcrypt.gensalt(rounds=HashPasswordBcrypt.ROUNDS)
        hash_bytes = bcrypt.hashpw(contrasena_bytes, salt)

        return hash_bytes.decode('utf-8')

    @staticmethod
    def verificar(contrasena: str, hash_almacenado: str) -> bool:
        """
        Verifica una contrasena contra su hash.

        Args:
            contrasena: Contrasena en texto plano a verificar
            hash_almacenado: Hash previamente generado

        Returns:
            True si la contrasena coincide, False en caso contrario
        """
        try:
            contrasena_bytes = contrasena.encode('utf-8')
            hash_bytes = hash_almacenado.encode('utf-8')
            return bcrypt.checkpw(contrasena_bytes, hash_bytes)
        except (ValueError, AttributeError) as e:
            print(f"Error al verificar contrasena: {e}")
            return False

    @staticmethod
    def es_hash_valido(hash_str: str) -> bool:
        """Verifica si un string tiene formato de hash bcrypt valido."""
        # Formato: $2b$12$..............................
        if not hash_str.startswith('$2'):
            return False
        partes = hash_str.split('$')
        if len(partes) != 4:
            return False
        try:
            costo = int(partes[2])
            if costo < 4 or costo > 31:
                return False
        except ValueError:
            return False
        # El hash en base64 debe tener 53 caracteres (22 salt + 31 hash)
        if len(partes[3]) != 53:
            return False
        return True


class HashPasswordArgon2:
    """
    Hashing de contrasenas usando Argon2id (recomendado actualmente).
    """

    @staticmethod
    def generar_hash(contrasena: str) -> str:
        """
        Genera hash con Argon2id.

        Parametros recomendados por OWASP (2024):
        - Memory: 64 MB
        - Time: 3 iteraciones
        - Parallelism: 4 threads
        """
        from argon2 import PasswordHasher
        ph = PasswordHasher(
            time_cost=3,         # 3 iteraciones
            memory_cost=65536,   # 64 MB
            parallelism=4,       # 4 hilos
            hash_len=32,         # 256 bits de salida
            salt_len=16          # 128 bits de salt
        )
        return ph.hash(contrasena)

    @staticmethod
    def verificar(contrasena: str, hash_almacenado: str) -> bool:
        from argon2 import PasswordHasher
        from argon2.exceptions import VerifyMismatchError

        ph = PasswordHasher()
        try:
            return ph.verify(hash_almacenado, contrasena)
        except VerifyMismatchError:
            return False
        except Exception as e:
            print(f"Error al verificar: {e}")
            return False


class HashPasswordScrypt:
    """
    Hashing de contrasenas usando scrypt (stdlib hashlib desde Python 3.6+).
    """

    @staticmethod
    def generar_hash(contrasena: str) -> str:
        """Genera hash con scrypt."""
        if not contrasena or len(contrasena) < 8:
            raise ValueError("La contrasena debe tener al menos 8 caracteres")

        salt = os.urandom(32)
        hash_bytes = hashlib.scrypt(
            password=contrasena.encode('utf-8'),
            salt=salt,
            n=2**14,      # Costo CPU/memoria
            r=8,          # Tamanio de bloque
            p=1,          # Paralelismo
            dklen=64      # Longitud del hash derivado
        )

        # Almacenar salt + hash (formato: salt:hash en hex)
        return f"{salt.hex()}:{hash_bytes.hex()}"

    @staticmethod
    def verificar(contrasena: str, hash_almacenado: str) -> bool:
        try:
            salt_hex, hash_hex = hash_almacenado.split(':')
            salt = bytes.fromhex(salt_hex)
            hash_esperado = bytes.fromhex(hash_hex)

            hash_calculado = hashlib.scrypt(
                password=contrasena.encode('utf-8'),
                salt=salt,
                n=2**14,
                r=8,
                p=1,
                dklen=64
            )
            return hash_calculado == hash_esperado
        except Exception:
            return False


# ============================================================
# DEMOSTRACION
# ============================================================
if __name__ == '__main__':
    import time

    print("=" * 60)
    print("Hashing Seguro de Contrasenas - Demostracion")
    print("=" * 60)

    contrasena = "MiContrasenaMuySegura123!"

    # --- BCRYPT ---
    print("\n[bcrypt]")
    inicio = time.time()
    hash_bcrypt = HashPasswordBcrypt.generar_hash(contrasena)
    tiempo = time.time() - inicio
    print(f"  Hash: {hash_bcrypt[:50]}...")
    print(f"  Tiempo: {tiempo:.3f}s")
    print(f"  Valido: {HashPasswordBcrypt.es_hash_valido(hash_bcrypt)}")
    print(f"  Verificar correcta: {HashPasswordBcrypt.verificar(contrasena, hash_bcrypt)}")
    print(f"  Verificar incorrecta: {HashPasswordBcrypt.verificar('wrong', hash_bcrypt)}")

    # --- ARGON2 ---
    print("\n[argon2]")
    try:
        inicio = time.time()
        hash_argon2 = HashPasswordArgon2.generar_hash(contrasena)
        tiempo = time.time() - inicio
        print(f"  Hash: {hash_argon2[:60]}...")
        print(f"  Tiempo: {tiempo:.3f}s")
        print(f"  Verificar: {HashPasswordArgon2.verificar(contrasena, hash_argon2)}")
    except ImportError:
        print("  argon2-cffi no instalado. pip install argon2-cffi")

    # --- SCRYPT ---
    print("\n[scrypt]")
    inicio = time.time()
    hash_scrypt = HashPasswordScrypt.generar_hash(contrasena)
    tiempo = time.time() - inicio
    print(f"  Hash: {hash_scrypt[:50]}...")
    print(f"  Tiempo: {tiempo:.3f}s")
    print(f"  Verificar: {HashPasswordScrypt.verificar(contrasena, hash_scrypt)}")

    # --- PRUEBA DE FUERZA BRUTA SIMULADA ---
    print("\n" + "=" * 60)
    print("Demostracion de por que bcrypt/argon2 son mejores que SHA-256")
    print("=" * 60)

    # SHA-256 (sin salt) - rapido de calcular
    inicio = time.time()
    for _ in range(10000):
        hashlib.sha256(b"test").hexdigest()
    tiempo_sha256 = time.time() - inicio

    # bcrypt - lento a proposito
    inicio = time.time()
    for _ in range(10):
        HashPasswordBcrypt.generar_hash("test")
    tiempo_bcrypt = time.time() - inicio

    print(f"\nSHA-256: 10,000 hashes en {tiempo_sha256:.3f}s "
          f"({10000/tiempo_sha256:.0f} hashes/s)")
    print(f"bcrypt:  10 hashes en {tiempo_bcrypt:.3f}s "
          f"({10/tiempo_bcrypt:.1f} hashes/s)")
    print(f"Factor de lentitud: {tiempo_bcrypt/tiempo_sha256*1000:.0f}x mas lento por hash")
    print("(Esto hace que ataques de fuerza bruta sean impracticables)")
```

## Ejercicio 3: Re escribir Codigo Inseguro (MD5/DES -> Algoritmos Modernos)

```python
# criptografia_insegura.py - VERSION INSEGURA (NO USAR)
import hashlib
from Crypto.Cipher import DES
import base64

# ============================================================
# CODIGO INSEGURA - IDENTIFICAR VULNERABILIDADES
# ============================================================

class GestorContrasenasInseguro:
    """WARNING: Esta clase contiene practicas criptograficas inseguras."""

    @staticmethod
    def hash_contrasena_md5(contrasena):
        """MAL: Usa MD5 sin salt."""
        return hashlib.md5(contrasena.encode()).hexdigest()

    @staticmethod
    def cifrar_datos_des(datos, clave):
        """MAL: Usa DES (56 bits, vulnerable a fuerza bruta)."""
        # DES usa claves de 8 bytes (56 bits efectivos)
        clave_des = clave[:8].ljust(8, '\0').encode()
        cipher = DES.new(clave_des, DES.MODE_ECB)
        # PKCS7 padding manual
        padding = 8 - len(datos) % 8
        datos_padded = datos + chr(padding) * padding
        cifrado = cipher.encrypt(datos_padded.encode())
        return base64.b64encode(cifrado).decode()

    @staticmethod
    def hash_archivo_sha1(ruta_archivo):
        """MAL: Usa SHA-1 (vulnerable a colisiones)."""
        sha1 = hashlib.sha1()
        with open(ruta_archivo, 'rb') as f:
            for bloque in iter(lambda: f.read(8192), b''):
                sha1.update(bloque)
        return sha1.hexdigest()


# ============================================================
# VERSION CORREGIDA - ALGORITMOS MODERNOS
# ============================================================

import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class GestorContrasenasSeguro:
    """Version segura usando algoritmos modernos."""

    @staticmethod
    def hash_contrasena(contrasena):
        """OK: Usa bcrypt con salt automatico."""
        import bcrypt
        return bcrypt.hashpw(
            contrasena.encode(),
            bcrypt.gensalt(rounds=12)
        ).decode()

    @staticmethod
    def verificar_contrasena(contrasena, hash_almacenado):
        """OK: Verificacion constante contra timing attacks."""
        import bcrypt
        return bcrypt.checkpw(
            contrasena.encode(),
            hash_almacenado.encode()
        )

    @staticmethod
    def cifrar_datos(datos, clave_maestra_hex):
        """OK: AES-256-GCM con autenticacion."""
        clave = bytes.fromhex(clave_maestra_hex)
        aesgcm = AESGCM(clave)
        nonce = os.urandom(12)
        cifrado = aesgcm.encrypt(nonce, datos.encode(), None)
        return {
            'nonce': base64.b64encode(nonce).decode(),
            'cifrado': base64.b64encode(cifrado).decode()
        }

    @staticmethod
    def descifrar_datos(datos_cifrados, clave_maestra_hex):
        """OK: Descifrado con verificacion de integridad."""
        clave = bytes.fromhex(clave_maestra_hex)
        aesgcm = AESGCM(clave)
        nonce = base64.b64decode(datos_cifrados['nonce'])
        cifrado = base64.b64decode(datos_cifrados['cifrado'])
        return aesgcm.decrypt(nonce, cifrado, None).decode()

    @staticmethod
    def hash_archivo(ruta_archivo):
        """OK: Usa SHA-256 en lugar de SHA-1."""
        sha256 = hashlib.sha256()
        with open(ruta_archivo, 'rb') as f:
            for bloque in iter(lambda: f.read(8192), b''):
                sha256.update(bloque)
        return sha256.hexdigest()

    @staticmethod
    def derivar_clave(contrasena: str, salt: bytes = None) -> tuple:
        """Deriva una clave AES de 256 bits desde una contrasena."""
        if salt is None:
            salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=600000,
        )
        clave = kdf.derive(contrasena.encode())
        return clave.hex(), salt.hex()


# ============================================================
# COMPARACION
# ============================================================
if __name__ == '__main__':
    print("=" * 60)
    print("Migracion de Criptografia Insegura a Moderna")
    print("=" * 60)

    print("\n--- HASH DE CONTRASENAS ---")
    contrasena = "SuperSecreta123"

    # Inseguro
    hash_md5 = GestorContrasenasInseguro.hash_contrasena_md5(contrasena)
    print(f"MD5 (INSEGURO):  {hash_md5} ({len(hash_md5)} chars)")

    # Seguro
    hash_bcrypt = GestorContrasenasSeguro.hash_contrasena(contrasena)
    print(f"bcrypt (SEGURO): {hash_bcrypt[:45]}... ({len(hash_bcrypt)} chars)")

    print("\n--- CIFRADO DE DATOS ---")

    # Inseguro
    cifrado_des = GestorContrasenasInseguro.cifrar_datos_des(
        "Mi numero de tarjeta: 1234-5678-9012-3456",
        "miclave"
    )
    print(f"DES (INSEGURO):   {cifrado_des[:30]}...")

    # Seguro
    clave_maestra = AESGCM.generate_key(bit_length=256)
    cifrado_aes = GestorContrasenasSeguro.cifrar_datos(
        "Mi numero de tarjeta: 1234-5678-9012-3456",
        clave_maestra.hex()
    )
    descifrado = GestorContrasenasSeguro.descifrar_datos(cifrado_aes, clave_maestra.hex())
    print(f"AES-GCM (SEGURO): {cifrado_aes['cifrado'][:30]}...")
    print(f"Descifrado:        {descifrado}")

    print("\n--- TABLA COMPARATIVA ---")
    print(f"{'Algoritmo':<15} {'Estado':<15} {'Razon':<40}")
    print(f"{'MD5':<15} {'NO USAR':<15} {'Colisiones demostradas, 2^18 operaciones'}")
    print(f"{'SHA-1':<15} {'NO USAR':<15} {'Colisiones demostradas (SHAttered)'}")
    print(f"{'DES':<15} {'NO USAR':<15} {'Clave de 56 bits, roto en horas'}")
    print(f"{'RC4':<15} {'NO USAR':<15} {'Vulnerabilidades de sesgo'}")
    print(f"{'3DES':<15} {'NO USAR':<15} {'Lento, reemplazado por AES'}")
    print(f"{'SHA-256/3':<15} {'OK (hash)':<15} {'No usar directo para contrasenas'}")
    print(f"{'bcrypt':<15} {'RECOMENDADO':<15} {'Resistente a ASIC/GPU'}")
    print(f"{'Argon2id':<15} {'RECOMENDADO':<15} {'Ganador PHC, resistente a memoria'}")
    print(f"{'AES-GCM':<15} {'RECOMENDADO':<15} {'Cifrado autenticado, estandar'}")
    print(f"{'RSA-2048':<15} {'OK':<15} {'Para intercambio de claves'}")
    print(f"{'X25519':<15} {'RECOMENDADO':<15} {'Curva eliptica moderna'}")
```

## Preguntas y Respuestas

**P1: Cual es la diferencia entre hash, cifrado y codificacion?**
R: Hash es unidireccional (no se puede revertir), cifrado es bidireccional con clave (se puede descifrar con la clave correcta), codificacion es totalmente reversible sin clave (Base64, hex). Para contrasenas se usa hash, para datos confidenciales se usa cifrado, para representar datos binarios como texto se usa codificacion.

**P2: Por que MD5 y SHA-1 no son seguros para hash de contrasenas?**
R: MD5 tiene colisiones demostrables en 2^18 operaciones. SHA-1 tiene colisiones demostradas (ataque SHAttered, 2017). Ademas, ambos son rapidos de calcular, lo que permite ataques de fuerza bruta a alta velocidad. Para contrasenas se necesitan algoritmos lentos (con factor de costo) como bcrypt, argon2 o scrypt.

**P3: Que es AES-GCM y que ventajas tiene sobre modos como ECB o CBC?**
R: AES-GCM (Galois/Counter Mode) proporciona cifrado autenticado: confidencialidad (no se puede leer), integridad (no se puede modificar) y autenticacion (solo quien tiene la clave puede generar texto cifrado valido). A diferencia de ECB (que filtra patrones) y CBC (que requiere padding y es vulnerable a padding oracle attacks), GCM es un modo AEAD que verifica automaticamente la integridad.

**P4: Que significa "no inventar criptografia propia"?**
R: Significa que los desarrolladores no deben implementar sus propios algoritmos criptograficos ni modificar los existentes. Los algoritmos criptograficos requieren anos de analisis matematico por parte de expertos. Implementaciones caseras casi siempre contienen vulnerabilidades sutiles (timing attacks, problemas de padding, generacion debil de numeros aleatorios). Usar librerias probadas como `cryptography`, `libsodium` o `PyCryptodome`.

**P5: Que es un "salt" en el contexto de hashing de contrasenas y por que es necesario?**
R: Un salt es un valor aleatorio unico que se agrega a cada contrasena antes de hacer el hash. Sin salt, dos usuarios con la misma contrasena tendrian el mismo hash, y los atacantes pueden usar rainbow tables (tablas precomputadas de hashes). Con salt unico, cada hash es diferente incluso para la misma contrasena, haciendo inutiles las rainbow tables.

**P6: Cual es la diferencia entre HMAC y una firma digital?**
R: HMAC usa una clave secreta compartida entre emisor y receptor para autenticar mensajes (garantiza integridad y autenticacion, pero no no-repudio porque ambos conocen la clave). Las firmas digitales (RSA/ECDSA) usan un par de claves publica/privada: el emisor firma con su clave privada y cualquiera verifica con la clave publica, lo que proporciona no-repudio.

**P7: Por que AES-256 es recomendado sobre AES-128?**
R: AES-128 proporciona 128 bits de seguridad, que es suficiente contra ataques clasicos pero vulnerable a ataques cuanticos (que reducen la seguridad a 64 bits mediante el algoritmo de Grover). AES-256 proporciona 256 bits de seguridad (128 contra ataques cuanticos). Para datos que deben permanecer seguros a largo plazo (10+ anos), se recomienda AES-256.

## Tarea / Lectura Recomendada

1. **OWASP Cryptographic Storage Cheat Sheet:**
   https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html

2. **OWASP Password Storage Cheat Sheet:**
   https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html

3. **Documentacion de la libreria `cryptography` de Python:**
   https://cryptography.io/en/latest/

4. **Password Hashing Competition (Argon2):**
   https://www.password-hashing.net/

5. **Tarea practica:** Implementar un sistema de cifrado de archivos que cifre un archivo con AES-GCM, almacene el nonce y ciphertext, y permita descifrarlo solo si la clave es correcta y el archivo no ha sido modificado.

6. **Tarea practica:** Investigar y escribir un resumen del ataque SHAthered contra SHA-1 y como afecta a Git (que usa SHA-1 para identificar commits).


