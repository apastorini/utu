# 5.1 Actividad: Ataque a KeePass (Análisis Defensivo)

## Objetivo Educativo

Comprender cómo se realizan los ataques de fuerza bruta y diccionario contra gestores de contraseñas locales como KeePass, para **mejorar las defensas** en nuestra implementación.

> **IMPORTANTE**: Esta actividad es **exclusivamente educativa**. Solo se debe realizar en entornos controlados (laboratorio) con contraseñas de prueba. Atacar sistemas ajenos sin autorización es **ILEGAL**.

## Marco Teórico

### ¿Cómo almacena KeePass las contraseñas?

```
┌─────────────────────────────────────────────────────────────┐
│  ARCHIVO KeePass (.kdbx)                                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Cabecera:                                                  │
│  ├── Magic bytes: 0x9AA2D604                               │
│  ├── Versión del formato: 4.1                              │
│  ├── UUID de cifrado: 31c1f286-d327-431c-89c2-fc4e71e83010│
│  │   (AES-KDF o Argon2d/Argon2id)                         │
│  ├── Parámetros del KDF:                                   │
│  │   ├── Rondas/Iteraciones (default: 60,000 para AES-KDF)│
│  │   ├── Salt (32 bytes)                                   │
│  │   └── UUID del algoritmo                                │
│  └── Master Seed (32 bytes)                                │
│                                                             │
│  Datos cifrados (AES-256-CBC o ChaCha20-Poly1305):        │
│  ├── Base de datos de entradas                             │
│  │   ├── Usuario: admin                                    │
│  │   │   └── Contraseña cifrada: [AES-256-CBC]           │
│  │   ├── Usuario: root                                     │
│  │   │   └── Contraseña cifrada: [AES-256-CBC]           │
│  │   └── ...                                               │
│  └── HMAC-SHA256 (verificación de integridad)             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Proceso de Derivación de Clave en KeePass

```
MASTER PASSWORD: "MiPassword123!"
         │
         ▼
┌─────────────────────────────────────────┐
│  PBKDF2-SHA256 o AES-KDF o Argon2id    │
│                                         │
│  Parámetros por defecto (AES-KDF):     │
│  - Rondas: 60,000                      │
│  - Salt: 32 bytes aleatorios           │
│  - UUID: 0xC9D621F6-4B3B-85F1-...     │
│                                         │
│  Parámetros recomendados (Argon2id):   │
│  - Iteraciones: 3                       │
│  - Memoria: 64 MB (65536 KB)          │
│  - Paralelismo: 4                      │
│  - Salt: 32 bytes                      │
│                                         │
└──────────────────┬──────────────────────┘
                   │
                   ▼
         CLAVE DERIVADA (256 bits)
                   │
                   ▼
         Combinación con Master Seed
                   │
                   ▼
         CLAVE FINAL DE CIFRADO
         (AES-256 o ChaCha20)
                   │
                   ▼
         Descifra la base de datos
```

### Tipos de Ataque Posibles

| Ataque | Método | Dificultad | Tiempo Estimado |
|--------|--------|------------|-----------------|
| **Fuerza bruta** | Probar todas las combinaciones | Alta | Años (si contraseña fuerte) |
| **Diccionario** | Lista de palabras comunes | Media | Minutos-Horas |
| **Rainbow tables** | Tablas precalculadas (sin salt) | Imposible* | N/A |
| **Hybrid** | Diccionario + variaciones | Media | Horas-Días |
| **Mask** | Patrón conocido | Baja-Media | Minutos-Horas |
| **Rule-based** | Reglas de transformación | Media | Horas-Días |

> *Rainbow tables son inútiles porque KeePass usa salt único por archivo.

---

## Actividad Paso a Paso (Windows)

### Fase 1: Preparación del Entorno (30 min)

#### Paso 1: Crear Base de Datos de Prueba

```
1. Descargar KeePassXC: https://keepassxc.org/download/
2. Instalar en Windows
3. Crear nueva base de datos:
   - Archivo: C:\lab-seguridad\keepass-test.kdbx
   - Master Password de PRUEBA: "password123"
   - Confirmar: "password123"
   - KDF: AES-KDF (default)
   - Rondas: 60,000 (default)

4. Agregar entradas de prueba:
   ├── 📁 Internet
   │   ├── 📄 Gmail - usuario: test@gmail.com, pass: TestGmail2024!
   │   ├── 📄 Facebook - usuario: test_user, pass: FbPass123!
   │   └── 📄 Amazon - usuario: test@amazon.com, pass: Amz#Secure99
   ├── 📁 Trabajo
   │   ├── 📄 VPN BHU - usuario: vpn_admin, pass: Vpn@BHU2024
   │   └── 📄 SSH Server - usuario: root, pass: R00t@Server!
   └── 📁 Personal
       ├── 📄 WiFi Casa - pass: MiWifiCasa123
       └── 📄 Banco BROU - usuario: 12345678, pass: Brou!Secure#2024

5. Guardar y cerrar KeePassXC
```

#### Paso 2: Crear Wordlist Personalizado

```powershell
# Crear directorio de trabajo
mkdir C:\lab-seguridad\wordlists

# Crear wordlist con contraseñas de prueba
$wordlist = @"
password
password123
Password123
P@ssw0rd
admin
admin123
letmein
welcome
monkey
dragon
master
qwerty
abc123
123456
12345678
password1
Password1
P@ssword1
Welcome1
Test1234
Test@1234
FbPass123
Amz#Secure99
Vpn@BHU2024
R00t@Server!
MiWifiCasa123
Brou!Secure#2024
GmailTest2024
"@

$wordlist | Out-File -FilePath "C:\lab-seguridad\wordlists\common-passwords.txt" -Encoding UTF8

Write-Host "Wordlist creado: C:\lab-seguridad\wordlists\common-passwords.txt" -ForegroundColor Green
Write-Host "Contraseñas en lista: $(($wordlist | Measure-Object).Count)" -ForegroundColor Cyan
```

#### Paso 3: Descargar Herramientas de Análisis

```powershell
# Opción 1: John the Ripper (Windows)
# Descargar desde: https://www.openwall.com/john/
# Extraer a: C:\lab-seguridad\tools\john\

# Opción 2: Hashcat (Windows)
# Descargar desde: https://hashcat.net/hashcat/
# Extraer a: C:\lab-seguridad\tools\hashcat\

# Opción 3: KeePass2John (extraer hash de KeePass)
# Incluido con John the Ripper
# Ubicación: C:\lab-seguridad\tools\john\keepass2john.exe

Write-Host "Herramientas descargadas" -ForegroundColor Green
Write-Host "Verificando..." -ForegroundColor Cyan
& "C:\lab-seguridad\tools\john\john.exe" --version
```

### Fase 2: Extracción del Hash (10 min)

#### Paso 4: Extraer Hash de KeePass

```powershell
# Usar keepass2john para extraer el hash
$keepassFile = "C:\lab-seguridad\keepass-test.kdbx"
$outputFile = "C:\lab-seguridad\keepass-hash.txt"

# Ejecutar keepass2john
& "C:\lab-seguridad\tools\john\keepass2john.exe" $keepassFile | Out-File -FilePath $outputFile -Encoding UTF8

# Ver contenido del hash extraído
Write-Host "=== HASH EXTRAÍDO ===" -ForegroundColor Yellow
Get-Content $outputFile

# El hash se verá algo así (formato simplificado):
# $keepass$*0*60000*32*<salt>*<encrypted_data>*<hmac>
```

**Salida esperada:**
```
$keepass$*0*60000*32*a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6*9a8b7c6d5e4f3g2h1...
```

### Fase 3: Ataque con Diccionario (15 min)

#### Paso 5: Ataque de Diccionario con John the Ripper

```powershell
# Ataque de diccionario básico
Write-Host "=== ATAQUE DE DICCIONARIO ===" -ForegroundColor Red
Write-Host "Archivo KeePass: $keepassFile" -ForegroundColor Cyan
Write-Host "Wordlist: C:\lab-seguridad\wordlists\common-passwords.txt" -ForegroundColor Cyan
Write-Host "Iniciando ataque..." -ForegroundColor Yellow

# Ejecutar John the Ripper con wordlist
& "C:\lab-seguridad\tools\john\john.exe" `
    --format=keepass `
    --wordlist="C:\lab-seguridad\wordlists\common-passwords.txt" `
    $outputFile

# Ver resultados
Write-Host "`n=== RESULTADOS ===" -ForegroundColor Green
& "C:\lab-seguridad\tools\john\john.exe" --show $outputFile
```

**Salida esperada:**
```
password123     (keepass-test.kdbx)

1 password hash cracked, 0 left
```

#### Paso 6: Ataque de Diccionario con Hashcat

```powershell
# Convertir hash para Hashcat (formato diferente)
# Hashcat usa formato: keepass → mode 13400

Write-Host "=== ATAQUE CON HASHCAT ===" -ForegroundColor Red

# Ejecutar Hashcat
& "C:\lab-seguridad\tools\hashcat\hashcat.exe" `
    -m 13400 `
    -a 0 `
    $outputFile `
    "C:\lab-seguridad\wordlists\common-passwords.txt" `
    --force

# Ver resultados
& "C:\lab-seguridad\tools\hashcat\hashcat.exe" `
    -m 13400 `
    $outputFile `
    --show
```

### Fase 4: Ataque con Fuerza Bruta (20 min)

#### Paso 7: Ataque de Fuerza Bruta con John

```powershell
# Ataque de fuerza bruta (probar todas las combinaciones cortas)
Write-Host "=== ATAQUE DE FUERZA BRUTA ===" -ForegroundColor Red
Write-Host "Esto puede tardar mucho tiempo..." -ForegroundColor Yellow

# Fuerza bruta con incremento (4-6 caracteres)
& "C:\lab-seguridad\tools\john\john.exe" `
    --format=keepass `
    --incremental `
    --min-length=1 `
    --max-length=10 `
    $outputFile

# Verificar resultados
& "C:\lab-seguridad\tools\john\john.exe" --show $outputFile
```

#### Paso 8: Ataque con Máscara (Patrón Conocido)

```powershell
# Si sabemos que la contraseña tiene patrón conocido
# Ejemplo: 8 caracteres que empiezan con mayúscula
Write-Host "=== ATAQUE CON MÁSCARA ===" -ForegroundColor Red

# Máscara: ?u?l?l?l?l?l?d?d (Mayúscula + 5 minúsculas + 2 números)
& "C:\lab-seguridad\tools\john\john.exe" `
    --format=keepass `
    --mask='?u?l?l?l?l?l?d?d' `
    $outputFile

# Máscara para contraseñas que contienen patrones comunes
# Ejemplo: Palabra + número + símbolo
& "C:\lab-seguridad\tools\john\john.exe" `
    --format=keepass `
    --mask='?w?d?d?d?s' `
    --wordlist="C:\lab-seguridad\wordlists\common-passwords.txt" `
    $outputFile
```

### Fase 5: Ataque con Reglas (15 min)

#### Paso 9: Ataque con Reglas de Transformación

```powershell
# Las reglas transforman las palabras del wordlist
# Ejemplo: agregar números, cambiar mayúsculas, etc.

Write-Host "=== ATAQUE CON REGLAS ===" -ForegroundColor Red

# Crear archivo de reglas personalizado
$rules = @"
# Reglas básicas
:
l
u
c
C
$1
$2
$3
$!
$@
$#
$1!
$1@
$1#
t0
r0
"@

$rules | Out-File -FilePath "C:\lab-seguridad\wordlists\rules.txt" -Encoding UTF8

# Ejecutar ataque con reglas
& "C:\lab-seguridad\tools\john\john.exe" `
    --format=keepass `
    --wordlist="C:\lab-seguridad\wordlists\common-passwords.txt" `
    --rules `
    $outputFile

# Ver resultados
& "C:\lab-seguridad\tools\john\john.exe" --show $outputFile
```

### Fase 6: Análisis de Resultados (10 min)

#### Paso 10: Documentar Resultados

Crear archivo `C:\lab-seguridad\reporte-ataque.md`:

```markdown
# Reporte de Análisis Defensivo - KeePass

## Configuración de Prueba
- **Archivo**: keepass-test.kdbx
- **KDF**: AES-KDF (60,000 rondas)
- **Contraseña de prueba**: password123
- **Herramientas**: John the Ripper, Hashcat

## Resultados de Ataques

### 1. Diccionario (John the Ripper)
- **Wordlist**: common-passwords.txt (30 palabras)
- **Tiempo**: ~2 segundos
- **Resultado**: ✅ Contraseña crackeada: "password123"
- **Velocidad**: ~15,000 intentos/segundo

### 2. Diccionario (Hashcat)
- **Wordlist**: common-passwords.txt
- **Tiempo**: ~3 segundos
- **Resultado**: ✅ Contraseña crackeada
- **Velocidad**: ~25,000 intentos/segundo (GPU)

### 3. Fuerza Bruta
- **Rango**: 1-10 caracteres
- **Tiempo estimado**: 4 horas (para 8 caracteres mixtos)
- **Velocidad**: ~15,000 intentos/segundo

### 4. Máscara (Patrón conocido)
- **Patrón**: ?u?l?l?l?l?l?d?d
- **Tiempo**: ~10 minutos
- **Resultado**: No encontrada (no coincide con patrón de prueba)

### 5. Reglas de Transformación
- **Reglas**: 15 transformaciones básicas
- **Tiempo**: ~30 segundos
- **Resultado**: ✅ Contraseña crackeada

## Conclusiones

### Lo que funcionó (para el atacante)
1. Diccionario con contraseñas comunes: Rápido y efectivo
2. Reglas de transformación: Amplían significativamente el wordlist
3. Ataque exitoso: Contraseña débil "password123"

### Lo que NO funcionó (defensa)
1. El KDF con 60,000 rondas ralentizó pero no impidió el ataque
2. Rainbow tables: Inútiles gracias al salt único
3. Argon2id: Habría sido mucho más lento

### Recomendaciones de Defensa
1. ✅ Usar contraseñas largas (≥20 caracteres)
2. ✅ Usar Argon2id en lugar de AES-KDF
3. ✅ Aumentar iteraciones/memoria del KDF
4. ✅ Activar 2FA adicional si es posible
5. ✅ Almacenar archivo .kdbx en ubicación segura

## Métricas de Seguridad

| Métrica | Valor Actual | Valor Recomendado |
|---------|-------------|-------------------|
| KDF | AES-KDF 60K rondas | Argon2id 64MB |
| Longitud contraseña | 11 caracteres | ≥20 caracteres |
| Entropía | ~60 bits | ≥80 bits |
| Tiempo de ataque | ~2 segundos | >10 años |
```

---

## Preguntas de Reflexión

1. ¿Por qué las rainbow tables son inútiles contra KeePass?
2. ¿Cómo cambiaría el tiempo de ataque si usáramos Argon2id con 64MB de memoria?
3. ¿Qué pasaría si la contraseña fuera "xK9#mP$vL2nQ!wR7tY4jB8" (24 caracteres)?
4. ¿Qué otras defensas podrían implementarse además del KDF?
5. ¿Cómo se compara esto con el ataque a Vaultwarden (donde el vault está en el servidor)?

---

> **Nota**: Esta actividad demuestra por qué la longitud y complejidad de la contraseña maestra son CRÍTICAS. Una contraseña débil puede ser crackeada en segundos, sin importar qué KDF se use.
