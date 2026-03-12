# CURSO COMPLETO DE CIBERSEGURIDAD - PARTE 2

## MÓDULO 3: CRIPTOGRAFÍA

### 3.1 Conceptos Fundamentales

#### 3.1.1 ¿Qué es la Criptografía?

**Definición:** Ciencia de proteger información mediante transformaciones matemáticas que la hacen ilegible para personas no autorizadas.

**Objetivos:**
- **Confidencialidad:** Solo el destinatario puede leer el mensaje
- **Integridad:** Detectar modificaciones
- **Autenticación:** Verificar identidad del emisor
- **No repudio:** El emisor no puede negar haber enviado el mensaje

---

### 3.2 Criptografía Simétrica

**Definición:** Usa la misma clave para cifrar y descifrar.

**Ventajas:**
- Muy rápida
- Eficiente para grandes volúmenes

**Desventajas:**
- Distribución segura de claves
- N usuarios necesitan N(N-1)/2 claves

**Algoritmos principales:**
- **AES (Advanced Encryption Standard):** Estándar actual
- **DES (Data Encryption Standard):** Obsoleto
- **3DES:** Obsoleto
- **ChaCha20:** Moderno, usado en TLS

#### Ejemplo Práctico - AES en Python

```python
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
```

#### Ejemplo en PowerShell (Windows)

```powershell
# Cifrar archivo con AES
$Password = ConvertTo-SecureString "MiClaveSegura123!" -AsPlainText -Force
$PasswordBytes = [System.Text.Encoding]::UTF8.GetBytes($Password)

# Crear objeto AES
$AES = New-Object System.Security.Cryptography.AesManaged
$AES.Key = (New-Object System.Security.Cryptography.SHA256Managed).ComputeHash($PasswordBytes)
$AES.IV = (New-Object System.Security.Cryptography.SHA256Managed).ComputeHash($PasswordBytes)[0..15]

# Leer archivo
$PlainText = Get-Content "documento.txt" -Raw
$PlainBytes = [System.Text.Encoding]::UTF8.GetBytes($PlainText)

# Cifrar
$Encryptor = $AES.CreateEncryptor()
$EncryptedBytes = $Encryptor.TransformFinalBlock($PlainBytes, 0, $PlainBytes.Length)
[System.IO.File]::WriteAllBytes("documento.txt.enc", $EncryptedBytes)

Write-Host "Archivo cifrado exitosamente"
```

---

### 3.3 Criptografía Asimétrica

**Definición:** Usa un par de claves: pública (para cifrar) y privada (para descifrar).

**Ventajas:**
- No requiere canal seguro para intercambiar claves
- Permite firmas digitales
- N usuarios solo necesitan N pares de claves

**Desventajas:**
- Mucho más lenta que simétrica
- Claves más largas

**Algoritmos principales:**
- **RSA:** El más usado
- **ECC (Elliptic Curve Cryptography):** Más eficiente
- **DSA:** Para firmas digitales

#### Ejemplo Práctico - RSA en Python

```python
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
```

#### Ejemplo en PowerShell - Generar claves RSA

```powershell
# Generar par de claves RSA
$RSA = New-Object System.Security.Cryptography.RSACryptoServiceProvider(2048)

# Exportar clave pública
$PublicKey = $RSA.ToXmlString($false)
$PublicKey | Out-File "clave_publica.xml"

# Exportar clave privada (proteger este archivo!)
$PrivateKey = $RSA.ToXmlString($true)
$PrivateKey | Out-File "clave_privada.xml"

Write-Host "Claves generadas exitosamente"

# Cifrar mensaje
$Mensaje = "Datos confidenciales"
$MensajeBytes = [System.Text.Encoding]::UTF8.GetBytes($Mensaje)
$MensajeCifrado = $RSA.Encrypt($MensajeBytes, $true)
$MensajeCifradoBase64 = [Convert]::ToBase64String($MensajeCifrado)

Write-Host "Mensaje cifrado: $MensajeCifradoBase64"
```

---

### 3.4 Funciones Hash

**Definición:** Transforman datos de cualquier tamaño en una cadena de longitud fija (digest).

**Propiedades:**
- **Determinista:** Mismo input = mismo output
- **Rápida de calcular**
- **Efecto avalancha:** Pequeño cambio = hash completamente diferente
- **Unidireccional:** Imposible obtener el input del hash
- **Resistencia a colisiones:** Difícil encontrar dos inputs con mismo hash

**Algoritmos:**
- **MD5:** OBSOLETO (colisiones encontradas)
- **SHA-1:** OBSOLETO (colisiones encontradas)
- **SHA-256:** Estándar actual
- **SHA-512:** Más seguro
- **bcrypt:** Para contraseñas
- **Argon2:** Ganador de competencia de hashing de contraseñas

#### Ejemplo Práctico - Verificación de Integridad

```python
import hashlib

def calcular_hash_archivo(ruta_archivo):
    """Calcula SHA-256 de un archivo"""
    sha256 = hashlib.sha256()
    
    with open(ruta_archivo, 'rb') as f:
        # Leer en bloques para archivos grandes
        for bloque in iter(lambda: f.read(4096), b''):
            sha256.update(bloque)
    
    return sha256.hexdigest()

# Calcular hash de archivo descargado
hash_calculado = calcular_hash_archivo('ubuntu-22.04.iso')
print(f"Hash calculado: {hash_calculado}")

# Hash oficial del sitio web
hash_oficial = "84eed0e1c8b8e3bb5c4c8e0e0e0e0e0e0e0e0e0e0e0e0e0e0e0e0e0e0e0e0e0e"

# Verificar integridad
if hash_calculado == hash_oficial:
    print("✓ Archivo íntegro - descarga exitosa")
else:
    print("✗ ADVERTENCIA: Archivo corrupto o modificado")
```

#### Ejemplo - Almacenamiento Seguro de Contraseñas

```python
import bcrypt

# Registrar usuario - hashear contraseña
password = "MiContraseñaSegura123!"
password_bytes = password.encode('utf-8')

# Generar salt y hash
salt = bcrypt.gensalt(rounds=12)  # Factor de trabajo
password_hash = bcrypt.hashpw(password_bytes, salt)

print(f"Hash almacenado en BD: {password_hash}")

# Login - verificar contraseña
password_ingresada = "MiContraseñaSegura123!"
password_ingresada_bytes = password_ingresada.encode('utf-8')

if bcrypt.checkpw(password_ingresada_bytes, password_hash):
    print("✓ Contraseña correcta - acceso concedido")
else:
    print("✗ Contraseña incorrecta - acceso denegado")
```

---

### 3.5 Firma Digital

**Definición:** Mecanismo criptográfico que garantiza autenticidad e integridad de un mensaje.

**Proceso:**
1. Emisor calcula hash del mensaje
2. Emisor cifra el hash con su clave privada (firma)
3. Emisor envía mensaje + firma
4. Receptor descifra firma con clave pública del emisor
5. Receptor calcula hash del mensaje recibido
6. Si ambos hash coinciden → mensaje auténtico e íntegro

#### Ejemplo Práctico - Firma Digital en Python

```python
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

# Generar claves
clave_privada = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)
clave_publica = clave_privada.public_key()

# Mensaje a firmar
mensaje = b"Contrato: Pago de $10,000 a proveedor XYZ"

# EMISOR: Firmar mensaje
firma = clave_privada.sign(
    mensaje,
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
)

print(f"Firma digital: {firma.hex()[:64]}...")

# RECEPTOR: Verificar firma
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
    print("✓ Firma válida - mensaje auténtico")
except:
    print("✗ Firma inválida - mensaje comprometido")

# Intentar con mensaje modificado
mensaje_modificado = b"Contrato: Pago de $100,000 a proveedor XYZ"
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
    print("✓ Firma válida")
except:
    print("✗ Firma inválida - mensaje fue modificado")
```

---

### 3.6 Certificados Digitales y PKI

**PKI (Public Key Infrastructure):** Infraestructura para gestionar certificados digitales.

**Componentes:**
- **CA (Certificate Authority):** Emite certificados
- **RA (Registration Authority):** Verifica identidad
- **Certificado Digital:** Vincula clave pública con identidad
- **CRL (Certificate Revocation List):** Lista de certificados revocados

#### Ejemplo - Generar Certificado SSL/TLS

```bash
# Generar clave privada
openssl genrsa -out servidor.key 2048

# Generar CSR (Certificate Signing Request)
openssl req -new -key servidor.key -out servidor.csr \
  -subj "/C=UY/ST=Montevideo/L=Montevideo/O=Mi Empresa/CN=www.miempresa.com"

# Autofirmar certificado (para desarrollo)
openssl x509 -req -days 365 -in servidor.csr \
  -signkey servidor.key -out servidor.crt

# Ver contenido del certificado
openssl x509 -in servidor.crt -text -noout
```

#### Ejemplo - Configurar HTTPS en Nginx

```nginx
server {
    listen 443 ssl;
    server_name www.miempresa.com;

    ssl_certificate /etc/nginx/ssl/servidor.crt;
    ssl_certificate_key /etc/nginx/ssl/servidor.key;

    # Configuración segura
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    location / {
        root /var/www/html;
        index index.html;
    }
}
```

---

### 3.7 Protocolos de Encriptación

#### 3.7.1 TLS/SSL (Transport Layer Security)

**Uso:** Proteger comunicaciones web (HTTPS), email (SMTPS), etc.

**Handshake TLS:**
1. Cliente envía "Client Hello" (versiones TLS soportadas, cifrados)
2. Servidor responde "Server Hello" (versión y cifrado elegidos)
3. Servidor envía certificado digital
4. Cliente verifica certificado con CA
5. Intercambio de claves (Diffie-Hellman)
6. Ambos generan claves de sesión simétricas
7. Comunicación cifrada con AES

#### Ejemplo - Verificar TLS de un sitio

```bash
# Ver certificado y versión TLS
openssl s_client -connect www.google.com:443 -tls1_3

# Verificar fecha de expiración
echo | openssl s_client -connect www.google.com:443 2>/dev/null | \
  openssl x509 -noout -dates

# Probar vulnerabilidades SSL/TLS
nmap --script ssl-enum-ciphers -p 443 www.ejemplo.com
```

#### 3.7.2 SSH (Secure Shell)

**Uso:** Acceso remoto seguro a servidores.

**Ejemplo - Configuración segura de SSH:**

```bash
# Generar par de claves
ssh-keygen -t ed25519 -C "mi-email@ejemplo.com"

# Copiar clave pública al servidor
ssh-copy-id usuario@servidor.com

# Configurar servidor SSH (/etc/ssh/sshd_config)
cat << EOF | sudo tee -a /etc/ssh/sshd_config
# Deshabilitar autenticación por contraseña
PasswordAuthentication no

# Solo permitir autenticación por clave
PubkeyAuthentication yes

# Deshabilitar login como root
PermitRootLogin no

# Cambiar puerto (seguridad por oscuridad)
Port 2222

# Solo permitir usuarios específicos
AllowUsers usuario1 usuario2
EOF

# Reiniciar servicio
sudo systemctl restart sshd
```

#### 3.7.3 VPN (Virtual Private Network)

**Protocolos:**
- **OpenVPN:** Código abierto, muy seguro
- **WireGuard:** Moderno, rápido, simple
- **IPSec:** Estándar corporativo

**Ejemplo - Configurar WireGuard:**

```bash
# Instalar WireGuard
sudo apt install wireguard

# Generar claves
wg genkey | tee privatekey | wg pubkey > publickey

# Configurar servidor (/etc/wireguard/wg0.conf)
cat << EOF | sudo tee /etc/wireguard/wg0.conf
[Interface]
PrivateKey = $(cat privatekey)
Address = 10.0.0.1/24
ListenPort = 51820

[Peer]
PublicKey = CLAVE_PUBLICA_CLIENTE
AllowedIPs = 10.0.0.2/32
EOF

# Iniciar VPN
sudo wg-quick up wg0

# Habilitar al inicio
sudo systemctl enable wg-quick@wg0
```

---

### 3.8 Computación Cuántica y Criptografía Post-Cuántica

#### 3.8.1 La Amenaza Cuántica

**Problema:** Las computadoras cuánticas podrán romper RSA y ECC usando el algoritmo de Shor.

**Algoritmos vulnerables:**
- RSA
- Diffie-Hellman
- ECC (Elliptic Curve)

**Algoritmos resistentes:**
- AES (con claves más largas)
- SHA-256/SHA-512

#### 3.8.2 Criptografía Post-Cuántica

**NIST está estandarizando nuevos algoritmos:**

1. **CRYSTALS-Kyber:** Encapsulación de claves
2. **CRYSTALS-Dilithium:** Firmas digitales
3. **FALCON:** Firmas digitales
4. **SPHINCS+:** Firmas digitales basadas en hash

**Ejemplo conceptual:**
```python
# Biblioteca experimental de criptografía post-cuántica
# pip install liboqs-python

from oqs import KeyEncapsulation

# Usar algoritmo resistente a computación cuántica
kem = KeyEncapsulation("Kyber512")

# Generar claves
public_key = kem.generate_keypair()

# Encapsular secreto
ciphertext, shared_secret_client = kem.encap_secret(public_key)

# Desencapsular
shared_secret_server = kem.decap_secret(ciphertext)

# Ambos secretos deben coincidir
assert shared_secret_client == shared_secret_server
print("✓ Intercambio de claves post-cuántico exitoso")
```

---

## MÓDULO 4: HERRAMIENTAS DE SEGURIDAD

### 4.1 Nmap - Escaneo de Redes

**Definición:** Herramienta de código abierto para descubrimiento de redes y auditoría de seguridad.

#### Instalación

```bash
# Ubuntu/Debian
sudo apt install nmap

# Windows (descargar de nmap.org)
# macOS
brew install nmap
```

#### Ejemplos Prácticos

```bash
# Escaneo básico de host
nmap 192.168.1.1

# Escaneo de rango de red
nmap 192.168.1.0/24

# Detectar sistema operativo
sudo nmap -O 192.168.1.1

# Escaneo de servicios y versiones
nmap -sV 192.168.1.1

# Escaneo completo (todos los puertos)
nmap -p- 192.168.1.1

# Escaneo sigiloso (SYN scan)
sudo nmap -sS 192.168.1.1

# Detectar vulnerabilidades con scripts NSE
nmap --script vuln 192.168.1.1

# Escaneo rápido de puertos comunes
nmap -F 192.168.1.1

# Guardar resultados en formato XML
nmap -oX resultados.xml 192.168.1.0/24
```

#### Laboratorio Práctico

```bash
# Crear red de prueba con Docker
docker network create lab-network

# Levantar contenedor vulnerable (Metasploitable)
docker run -d --name vulnerable --network lab-network vulnerables/metasploit-vulnerable-apps

# Escanear desde otro contenedor
docker run --rm --network lab-network instrumentisto/nmap \
  -sV -p- vulnerable
```

---

### 4.2 Wireshark / tcpdump - Análisis de Tráfico

#### tcpdump - Captura en línea de comandos

```bash
# Capturar todo el tráfico en interfaz eth0
sudo tcpdump -i eth0

# Capturar solo tráfico HTTP
sudo tcpdump -i eth0 port 80

# Capturar tráfico de/hacia IP específica
sudo tcpdump -i eth0 host 192.168.1.100

# Guardar captura en archivo
sudo tcpdump -i eth0 -w captura.pcap

# Leer archivo de captura
tcpdump -r captura.pcap

# Capturar solo paquetes SYN (inicio de conexión)
sudo tcpdump -i eth0 'tcp[tcpflags] & tcp-syn != 0'

# Capturar tráfico DNS
sudo tcpdump -i eth0 port 53

# Mostrar contenido en ASCII
sudo tcpdump -i eth0 -A port 80
```

#### Wireshark - Análisis gráfico

**Filtros útiles:**
```
# Tráfico HTTP
http

# Tráfico de IP específica
ip.addr == 192.168.1.100

# Solo paquetes SYN
tcp.flags.syn == 1 && tcp.flags.ack == 0

# Contraseñas en texto plano (FTP, HTTP Basic Auth)
ftp.request.command == "PASS" || http.authbasic

# Tráfico cifrado (TLS/SSL)
ssl || tls

# Errores TCP
tcp.analysis.flags
```

#### Laboratorio - Capturar credenciales HTTP

```bash
# Terminal 1: Iniciar captura
sudo tcpdump -i lo -w http-login.pcap port 8000

# Terminal 2: Servidor web simple
python3 -m http.server 8000

# Terminal 3: Enviar credenciales (simulación)
curl -u usuario:password123 http://localhost:8000

# Analizar captura
tcpdump -r http-login.pcap -A | grep -i "authorization"
```

