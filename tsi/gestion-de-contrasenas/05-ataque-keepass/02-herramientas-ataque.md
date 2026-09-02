# 5.2 Herramientas de Análisis para Windows

## Herramientas Principales

### 1. John the Ripper

**Propósito**: Cracker de contraseñas multi-formato

```
DESCARGA E INSTALACIÓN:
1. Ir a: https://www.openwall.com/john/
2. Descargar "john-1.9.0-jumbo-1-win64.zip"
3. Extraer a: C:\tools\john\
4. Verificar: C:\tools\john\john.exe --version
```

**Comandos Esenciales para KeePass:**

```powershell
# Extraer hash de KeePass
keepass2john.exe archivo.kdbx > hash.txt

# Ataque de diccionario
john.exe --format=keepass --wordlist=wordlist.txt hash.txt

# Fuerza bruta (incremental)
john.exe --format=keepass --incremental hash.txt

# Ataque con máscara
john.exe --format=keepass --mask='?u?l?l?l?l?l?d?d' hash.txt

# Ver resultados
john.exe --show hash.txt

# Resetear progreso (si se interrumpe)
john.exe --restore=hash.txt
```

**Formatos Soportados:**

| Formato | Comando | Descripción |
|---------|---------|-------------|
| KeePass 1.x | `--format=keepass` | KeePass .kdb |
| KeePass 2.x | `--format=keepass` | KeePass .kdbx |
| KeePass KDBX4 | `--format=keepass` | KeePass 2.47+ |

### 2. Hashcat

**Propósito**: Cracker de contraseñas acelerado por GPU

```
DESCARGA E INSTALACIÓN:
1. Ir a: https://hashcat.net/hashcat/
2. Descargar "hashcat-6.2.6.7z"
3. Extraer a: C:\tools\hashcat\
4. Verificar: C:\tools\hashcat\hashcat.exe --version
5. Requisito: GPU NVIDIA o AMD con soporte OpenCL
```

**Comandos para KeePass:**

```powershell
# Modo KeePass: 13400
# Ataque de diccionario
hashcat.exe -m 13400 -a 0 hash.txt wordlist.txt

# Fuerza bruta
hashcat.exe -m 13400 -a 3 hash.txt ?a?a?a?a?a?a?a?a

# Máscara personalizada
hashcat.exe -m 13400 -a 3 hash.txt ?u?l?l?l?l?l?d?d

# Reglas
hashcat.exe -m 13400 -a 0 hash.txt wordlist.txt -r rules/best64.rule

# Ver resultados
hashcat.exe -m 13400 hash.txt --show
```

**Máscaras de Hashcat:**

| Carácter | Significado |
|----------|-------------|
| `?l` | Minúsculas (a-z) |
| `?u` | Mayúsculas (A-Z) |
| `?d` | Números (0-9) |
| `?s` | Símbolos (!@#$%^&*) |
| `?a` | Todos los caracteres |
| `?b` | Bytes (0x00-0xff) |

### 3. KeePass2John

**Propósito**: Extraer hash de archivos KeePass para John the Ripper

```powershell
# Uso básico
keepass2john.exe archivo.kdbx

# Guardar en archivo
keepass2john.exe archivo.kdbx > hash.txt

# Con contraseña personalizada
keepass2john.exe -p "contraseña" archivo.kdbx
```

### 4. CeWL

**Propósito**: Generar wordlists personalizados desde sitios web

```powershell
# Instalación (requiere Python y Ruby)
pip install cewl

# Generar wordlist desde sitio web
cewl https://ejemplo.com -w wordlist.txt -d 3 -m 5

# Parámetros:
# -d: profundidad de enlaces
# -m: longitud mínima de palabras
# -w: archivo de salida
```

### 5. Crunch

**Propósito**: Generar wordlists basados en patrones

```powershell
# Instalación
# Descargar desde: https://github.com/crunchsec/crunch/releases

# Generar contraseñas de 6 caracteres (a-z, 0-9)
crunch 6 6 abcdefghijklmnopqrstuvwxyz0123456789 -o wordlist.txt

# Generar con patrón
crunch 8 8 -t @@@@%%%% -o wordlist.txt
# @ = minúscula
# , = mayúscula
# % = número
# ^ = símbolo
```

## Configuración del Laboratorio

### Estructura de Directorios

```
C:\lab-seguridad\
├── tools\
│   ├── john\
│   │   ├── john.exe
│   │   ├── keepass2john.exe
│   │   └── run\
│   │       ├── rules\
│   │       │   ├── best64.rule
│   │       │   ├── d3ad0ne.rule
│   │       │   └── rockyou-30000.rule
│   │       └── wordlists\
│   │           ├── common.txt
│   │           ├── password.lst
│   │           └── top-1000.txt
│   ├── hashcat\
│   │   ├── hashcat.exe
│   │   └── rules\
│   │       ├── best64.rule
│   │       ├── OneRuleToRuleThemAll.rule
│   │       └── d3ad0ne.rule
│   └── keepass2john\
│       └── keepass2john.exe
│
├── wordlists\
│   ├── common-passwords.txt
│   ├── custom-wordlist.txt
│   └── rules.txt
│
├── targets\
│   ├── easy-test.kdbx         (contraseña: password)
│   ├── medium-test.kdbx       (contraseña: Test1234)
│   ├── hard-test.kdbx         (contraseña: xK9#mP$vL2nQ!wR7)
│   └── extreme-test.kdbx      (contraseña:随机 24 chars)
│
├── results\
│   ├── easy-results.txt
│   ├── medium-results.txt
│   └── hard-results.txt
│
├── reports\
│   ├── reporte-easy.md
│   ├── reporte-medium.md
│   └── reporte-hard.md
│
└── scripts\
    ├── extract-hash.ps1
    ├── attack-dictionary.ps1
    ├── attack-bruteforce.ps1
    └── analyze-results.ps1
```

### Scripts Automatizados

#### Script de Extracción de Hash

```powershell
# extract-hash.ps1
# Extraer hash de archivos KeePass

param(
    [string]$KeePassFile,
    [string]$OutputDir = "C:\lab-seguridad\results"
)

$johnPath = "C:\lab-seguridad\tools\john\keepass2john.exe"
$outputFile = "$OutputDir\$([System.IO.Path]::GetFileNameWithoutExtension($KeePassFile))-hash.txt"

Write-Host "=== Extracción de Hash ===" -ForegroundColor Cyan
Write-Host "Archivo: $KeePassFile" -ForegroundColor White

# Verificar que el archivo existe
if (-not (Test-Path $KeePassFile)) {
    Write-Host "ERROR: Archivo no encontrado" -ForegroundColor Red
    exit 1
}

# Extraer hash
& $johnPath $KeePassFile | Out-File -FilePath $outputFile -Encoding UTF8

# Verificar que se extrajo
if (Test-Path $outputFile) {
    $hashContent = Get-Content $outputFile
    Write-Host "Hash extraído exitosamente" -ForegroundColor Green
    Write-Host "Archivo de hash: $outputFile" -ForegroundColor White
    Write-Host "Contenido: $hashContent" -ForegroundColor Yellow
} else {
    Write-Host "ERROR: No se pudo extraer el hash" -ForegroundColor Red
}
```

#### Script de Ataque Completo

```powershell
# attack-all.ps1
# Ejecutar múltiples ataques contra KeePass

param(
    [string]$HashFile,
    [string]$ResultsDir = "C:\lab-seguridad\results"
)

$johnPath = "C:\lab-seguridad\tools\john\john.exe"
$wordlistDir = "C:\lab-seguridad\wordlists"

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "  ATAQUE COMPLETO A KEEPASS              " -ForegroundColor Cyan
Write-Host "  Hash file: $HashFile" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

# Ataque 1: Diccionario básico
Write-Host "`n--- Ataque 1: Diccionario Básico ---" -ForegroundColor Yellow
$startTime = Get-Date
& $johnPath --format=keepass --wordlist="$wordlistDir\common-passwords.txt" $HashFile
$duration = (Get-Date) - $startTime
Write-Host "Tiempo: $($duration.TotalSeconds) segundos" -ForegroundColor Gray

# Ataque 2: Diccionario con reglas
Write-Host "`n--- Ataque 2: Diccionario + Reglas ---" -ForegroundColor Yellow
$startTime = Get-Date
& $johnPath --format=keepass --wordlist="$wordlistDir\common-passwords.txt" --rules $HashFile
$duration = (Get-Date) - $startTime
Write-Host "Tiempo: $($duration.TotalSeconds) segundos" -ForegroundColor Gray

# Ataque 3: Fuerza bruta (4-8 caracteres)
Write-Host "`n--- Ataque 3: Fuerza Bruta (4-8 chars) ---" -ForegroundColor Yellow
$startTime = Get-Date
& $johnPath --format=keepass --incremental --min-length=4 --max-length=8 $HashFile
$duration = (Get-Date) - $startTime
Write-Host "Tiempo: $($duration.TotalSeconds) segundos" -ForegroundColor Gray

# Ataque 4: Máscara (mayúscula + 5 minúsculas + 2 números)
Write-Host "`n--- Ataque 4: Máscara ---" -ForegroundColor Yellow
$startTime = Get-Date
& $johnPath --format=keepass --mask='?u?l?l?l?l?l?d?d' $HashFile
$duration = (Get-Date) - $startTime
Write-Host "Tiempo: $($duration.TotalSeconds) segundos" -ForegroundColor Gray

# Resumen
Write-Host "`n=========================================" -ForegroundColor Cyan
Write-Host "  RESUMEN DE ATAQUES                     " -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

$results = & $johnPath --show $HashFile
Write-Host "Contraseñas encontradas:" -ForegroundColor Green
Write-Host $results
```

#### Script de Análisis de Seguridad

```powershell
# analyze-keepass.ps1
# Analizar la fortaleza de un archivo KeePass

param(
    [string]$KeePassFile
)

Write-Host "=== Análisis de Seguridad KeePass ===" -ForegroundColor Cyan

# 1. Verificar que es un archivo KeePass válido
$magicBytes = [System.IO.File]::ReadAllBytes($KeePassFile)[0..3]
$magicHex = ($magicBytes | ForEach-Object { '{0:X2}' -f $_ }) -join ' '

if ($magicHex -eq "03 D9 A2 9A 67 01 4D 11") {
    Write-Host "✅ Archivo KeePass válido (KDBX4)" -ForegroundColor Green
} elseif ($magicHex -eq "03 D9 A2 9A 67 01 4D 06") {
    Write-Host "✅ Archivo KeePass válido (KDBX3)" -ForegroundColor Green
} else {
    Write-Host "❌ No parece un archivo KeePass válido" -ForegroundColor Red
}

# 2. Analizar cabecera (simplificado)
Write-Host "`n--- Información del Archivo ---" -ForegroundColor Yellow
$fileInfo = Get-Item $KeePassFile
Write-Host "Tamaño: $([math]::Round($fileInfo.Length / 1KB, 2)) KB"
Write-Host "Última modificación: $($fileInfo.LastWriteTime)"

# 3. Recomendaciones
Write-Host "`n--- Recomendaciones de Seguridad ---" -ForegroundColor Yellow
Write-Host "1. Usar Argon2id en lugar de AES-KDF"
Write-Host "2. Aumentar iteraciones/memoria del KDF"
Write-Host "3. Usar contraseña maestra ≥20 caracteres"
Write-Host "4. Habilitar 2FA si es posible"
Write-Host "5. Almacenar archivo en ubicación segura"
Write-Host "6. Crear respaldo cifrado periódicamente"
```

## Wordlists Recomendados

### Para Pruebas de Laboratorio

| Wordlist | Tamaño | Propósito |
|----------|--------|-----------|
| `common-passwords.txt` | 100 | Pruebas rápidas |
| `top-1000.txt` | 1,000 | Análisis básico |
| `rockyou.txt` (recortado) | 10,000 | Análisis intermedio |
| `SecLists/Common-Credentials` | 20,000 | Análisis avanzado |

### Generar Wordlist Personalizado

```powershell
# Generar wordlist basado en información de la empresa
# (Para uso defensivo: verificar que empleados no usen contraseñas predecibles)

$companyWords = @(
    "bhu",
    "bhu2024",
    "BHU",
    "Bhu2024",
    "oficina",
    "servidor",
    "admin",
    "produccion",
    "desarrollo"
)

$commonSuffixes = @(
    "123",
    "!",
    "2024",
    "2023",
    "#1",
    "@123"
)

$wordlist = @()
foreach ($word in $companyWords) {
    foreach ($suffix in $commonSuffixes) {
        $wordlist += "$word$suffix"
        $wordlist += "$word$($suffix.ToUpper())"
    }
}

$wordlist | Sort-Object -Unique | Out-File `
    -FilePath "C:\lab-seguridad\wordlists\company-specific.txt" `
    -Encoding UTF8

Write-Host "Wordlist generado: $($wordlist.Count) palabras únicas"
```

## Resultados Esperados por Nivel de Contraseña

| Nivel | Ejemplo | Tiempo Diccionario | Tiempo Fuerza Bruta |
|-------|---------|-------------------|---------------------|
| **Muy débil** | `password` | <1 segundo | <1 segundo |
| **Débil** | `Password1` | <5 segundos | ~1 minuto |
| **Media** | `P@ssw0rd123` | ~30 segundos | ~1 hora |
| **Fuerte** | `xK9#mP$vL2nQ` | No encontrado | >1 año |
| **Muy fuerte** | 24 chars aleatorios | Imposible | >siglos |

---

> **Nota**: Todas las herramientas deben usarse solo en entornos de laboratorio. El uso no autorizado contra sistemas ajenos es ilegal.
