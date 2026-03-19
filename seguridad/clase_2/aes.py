from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

# Generar clave de 256 bits (32 bytes)
clave = os.urandom(32)
# Generar IV (Initialization Vector) de 128 bits
iv = os.urandom(16)

# Crear cifrador
cipher = Cipher(
    algorithms.AES(clave),
    modes.CBC(iv),
    backend=default_backend()
)

# Mensaje a cifrar (debe ser múltiplo de 16 bytes)
mensaje = b"Datos confidenciales de la empresa"
# Padding para completar bloque
padding_length = 16 - (len(mensaje) % 16)
mensaje_padded = mensaje + bytes([padding_length] * padding_length)

# Cifrar
encryptor = cipher.encryptor()
mensaje_cifrado = encryptor.update(mensaje_padded) + encryptor.finalize()

print(f"Mensaje original: {mensaje}")
print(f"Mensaje cifrado (hex): {mensaje_cifrado.hex()}")

# Descifrar
decryptor = cipher.decryptor()
mensaje_descifrado = decryptor.update(mensaje_cifrado) + decryptor.finalize()
# Quitar padding
padding_length = mensaje_descifrado[-1]
mensaje_original = mensaje_descifrado[:-padding_length]

print(f"Mensaje descifrado: {mensaje_original}")