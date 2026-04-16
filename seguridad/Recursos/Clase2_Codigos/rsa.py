from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization

# Generar par de claves RSA
clave_privada = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)
clave_publica = clave_privada.public_key()

# Guardar clave privada
pem_privada = clave_privada.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)
with open('clave_privada.pem', 'wb') as f:
    f.write(pem_privada)

# Guardar clave pública
pem_publica = clave_publica.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)
with open('clave_publica.pem', 'wb') as f:
    f.write(pem_publica)

# Cifrar con clave pública
mensaje = b"Mensaje secreto para el destinatario"
mensaje_cifrado = clave_publica.encrypt(
    mensaje,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

print(f"Mensaje cifrado: {mensaje_cifrado.hex()}")

# Descifrar con clave privada
mensaje_descifrado = clave_privada.decrypt(
    mensaje_cifrado,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

print(f"Mensaje descifrado: {mensaje_descifrado}")