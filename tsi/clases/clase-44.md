# Clase 44: Forense Digital - Practica de Preservacion y Analisis de Evidencia

**Numero de clase:** 33  
**Duracion:** 2 horas  
**Curso:** Seguridad de la Informacion

---

## Objetivos de Aprendizaje

- Comprender que es la forense digital, en que se diferencia de una auditoria y por que la evidencia mal preservada no sirve
- Aplicar las 6 fases del proceso forense y la cadena de custodia
- Calcular y verificar hashes (MD5/SHA-256) para probar integridad de un archivo
- Recolectar evidencia en Windows con herramientas nativas: PowerShell, registro, logs de seguridad, papelera de reciclaje
- Construir una imagen forense en la VM de Kali Linux y analizarla con Sleuth Kit (fls, icat, istat)
- Recuperar un archivo borrado y reconstruir una linea de tiempo (timeline)
- Redactar un informe forense defendible con hash, cronologia y conclusiones

---

## Organizacion de la Sesion (2 horas)

| Actividad | Duracion |
|-----------|----------|
| Introduccion teorica: que es la forense y marco legal | 20 min |
| Ejercicio 1: recoleccion de evidencia en Windows | 35 min |
| Ejercicio 2: imagen forense y recuperacion de borrados en Kali | 35 min |
| Ejercicio 3: analisis grafico con Autopsy y timeline | 15 min |
| Glosario, preguntas y cierre | 15 min |

**Entorno necesario:**
- PC con Windows 10/11 (el del alumno, o un laboratorio)
- VirtualBox o VMware con una VM de Kali Linux actualizada
- Opcion: carpeta compartida entre Windows y la VM para pasar archivos

---

## Contenido Detallado

### 1. Que es la Forense Digital? (10 min)

La **forense digital** (o informatica forense) es la disciplina que **identifica, recolecta, preserva, analiza y presenta evidencia digital** de forma que el resultado sea confiable, reproducible y utilizable como prueba.

**Por que existe esta disciplina?** Porque un equipo informatico puede ser modificado sin querer (o a proposito) en segundos: borrar un archivo, apagar la maquina, correr un "limpiador de registros" o simplemente que el sistema sobrescriba un sector con una actualizacion automatica. Si nadie preserva el estado original y demuestra que no cambio, cualquier conclusion es descartable.

**Diferencia con otras actividades de seguridad:**

| Actividad | Objetivo | Trabaja sobre... | Salida |
|-----------|----------|------------------|--------|
| **Forense digital** | Encontrar que paso, cuando y quien, dejando prueba | Evidencia original/copias verificadas | Informe con cadena de custodia |
| **Auditoria** | Verificar cumplimiento de normas y controles | Sistemas y procesos | Hallazgos y recomendaciones |
| **Pentesting** | Demostrar que se puede romper (con autorizacion) | Sistemas vivos, en forma activa | Reporte de vulnerabilidades |
| **Monitoreo** | Detectar incidentes en tiempo real | Trafico y logs en produccion | Alertas |

**La triada CIA aplicada a la evidencia:**

- **Integridad:** el archivo analizado es identico al original -> se demuestra con **hash**
- **Confidencialidad:** solo el equipo de investigacion accede a la evidencia (carpeta de caso, permisos)
- **Disponibilidad:** la evidencia se guarda en soportes que no se pierdan ni se sobrescriban

### 2. Marco Legal, Etica y Orden de Volatilidad (10 min)

**Regla de oro 1: autorizacion.** Solo se forensean equipos propios o con autorizacion escrita del dueno. En Uruguay, el acceso no autorizado a sistemas y la violacion de datos personales estan contemplados en la **Ley 18.331** (Proteccion de Datos Personales) y en la **Ley 20.327** de ciberdelincuencia (acceso ilicito a datos informaticos, Art. 297 BIS del Codigo Penal); los incidentes graves se reportan al **CSIRT.CERT.uy**. En una empresa, ademas, aplica la politica interna de seguridad.

**Regla de oro 2: cadena de custodia.** Es el registro ininterrumpido de quien tuvo la evidencia, cuando y bajo que condiciones.

**Por que es vital?** Si hay un hueco en el registro ("estuvo en la mesa de alguien sin firmar"), la defensa puede alegar que cualquiera pudo alterar el contenido, y la evidencia pierde valor. La cadena de custodia no protege la evidencia: **protege la credibilidad de quien la presenta**.

**Orden de volatilidad (RFC 3227): que recolectar primero.**

| Prioridad | Fuente | Por que va primero |
|-----------|--------|--------------------|
| 1 | Memoria RAM (processos, claves en claro, conexiones) | Desaparece al apagar |
| 2 | Estado de red (tabla ARP, conexiones activas, DHCP) | Cambia cada minuto |
| 3 | Procesos y sesiones activas | Cambian al cerrar sesiones |
| 4 | Logs en memoria / buffers | El sistema los rota y los descarta |
| 5 | Archivos en disco, temporales, swap | Persisten pero se sobrescriben |
| 6 | Logs en disco, `$MFT`, registro | Mas estables |
| 7 | Respaldos, cintas, soportes desconectados | Los mas estables |

**Errores que invalidan una investigacion:**

| Error | Consecuencia |
|-------|--------------|
| Trabajar sobre el original (sin copia) | Cualquier herramienta altera fechas de acceso y metadatos |
| Apagar el equipo sin capturar RAM | Se pierde la evidencia mas volatil |
| No calcular hash antes y despues | Nadie puede demostrar que la evidencia no cambio |
| Copiar con Explorer sin registrar | No queda trazabilidad de la copia |
| Falta de fecha/hora sincronizada | Las cronologias no se pueden cruzar |
| Sin cadena de custodia firmada | La evidencia es cuestionable en juicio |

### 3. Las 6 Fases del Proceso Forense (10 min)

```
 1. DETECCION            -> Se detecta el incidente / se recibe la denuncia
        |
 2. AUTORIZACION         -> Permiso escrito, alcance definido, equipo asignado
        |
 3. PRESERVACION         -> Acondicionar el escenario: no apagar, no mover,
        |                   aislar de la red si corresponde (orden de volatilidad)
        v
 4. ADQUISICION          -> Copia bit a bit (imagen forense) + HASH de original
        |                   y de la copia. Cadena de custodia.
        v
 5. ANALISIS             -> SIEMPRE sobre la copia, nunca sobre el original
        |                   (Sleuth Kit, Autopsy, Volatility, registro, logs)
        v
 6. INFORME Y PRESENTACION -> Hallazgos con evidencia citada, cronologia,
                              limitaciones y conclusiones defendibles
```

**Por que separar adquisicion de analisis?** Porque el analista no debe tocar la fuente. Asi el analista de turno puede equivocarse, reintentar y usar herramientas destructivas sin arruinar el caso: siempre trabaja sobre la copia verificada.

### 4. Integridad: Hashing (10 min)

Un **hash** (resumen criptografico) convierte cualquier archivo, de cualquier tamano, en una cadena fija de caracteres. Es la **huella digital del archivo**.

**Propiedades y su por que:**

| Propiedad | Que significa | Por que importa |
|-----------|---------------|-----------------|
| Deterministico | El mismo archivo siempre produce el mismo hash | Permite comparar original vs copia |
| Unidireccional | No se puede invertir el hash para recuperar el archivo | Guardar hashes no expone el contenido |
| Efecto avalancha | Cambiar 1 bit de entrada cambia ~50% del hash | Cualquier alteracion minima es visible |
| Resistencia a colisiones | Dos archivos distintos no deben dar el mismo hash | Nadie puede "reemplazar" un archivo por otro con igual huella |

**Algoritmos:**

| Algoritmo | Tamano | Estado |
|-----------|--------|--------|
| MD5 | 128 bits (32 hex) | Roto para firmas/seguridad; todavia util para deteccion accidental |
| SHA-1 | 160 bits (40 hex) | Depreciado (colisiones publicadas en 2017) |
| **SHA-256** | 256 bits (64 hex) | **Recomendado** para evidencia |
| SHA-512 | 512 bits | Mas lento, uso en respaldos grandes |

**Ejemplo practico:** un archivo `informe.txt` produce siempre `9f86d081...` (SHA-256). Si al copiarlo el hash da otro numero, el archivo cambio y la copia no sirve.

### 5. Imagen Forense (5 min)

Una **imagen forense** es una copia **bit a bit** de un disco o soporte, incluyendo areas que el sistema operativo "no ve" (espacios libres, tablas, sectores ocultos).

| Formato | Descripcion |
|---------|-------------|
| `dd` / raw (.img, .dd) | Copia literal sin metadatos. Simple, universal |
| E01 (EnCase) | Compresiona, calcula hash interno y guarda metadatos del caso |
| AFF | Formato abierto de gran rendimiento |

**Write blocker (bloqueador de escritura):** dispositivo fisico o software que permite leer un disco sin que el sistema pueda escribir en el. **Por que:** montar un disco afectado en modo lectura-escritura haria que Windows escriba en el (cache, `$UsnJrnl`, fechas de acceso) y destruiria evidencia.

**Flujo correcto:** original -> (write blocker) -> imagen -> hash de ambos -> analisis sobre la copia.

### 6. Artefactos de Windows: Donde Mirar (10 min)

| Artefacto | Ubicacion | Que contiene | Por que importa |
|-----------|-----------|--------------|-----------------|
| `$MFT` | Raiz de la particion NTFS | Tabla maestra: todos los archivos, fechas, tamano | Ve archivos aunque esten borrados |
| Prefetch | `C:\Windows\Prefetch\*.pf` | Ultimos programas ejecutados en el equipo | Prueba de que un programa corrio |
| AmCache | `HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Amcache` | Ejecuciones y hashes de binarios | Refuerza Prefetch con hashes |
| Registro USBSTOR | `HKLM\SYSTEM\CurrentControlSet\Enum\USBSTOR` | USB conectados: marca, modelo, numero de serie | Prueba fisica de que un pendrive estuvo ahi |
| Teclas `Run` | `HKLM/HKCU\...\CurrentVersion\Run` | Programas que arrancan con el sistema | Persistencia de malware |
| Eventos de seguridad | Log `Security` (Event Viewer) | 4624/4625 logins, 4688 procesos, 1102 limpieza de log | Quien entro, que ejecuto, si borro evidencia |
| LNK y Jump Lists | `AppData\Roaming\Microsoft\Windows\Recent` | Accesos directos con ruta original y fecha | Muestra archivos abiertos aunque se hayan movido |
| Papelera de reciclaje | `C:\$Recycle.Bin` | `$I` (ruta, tamano, fecha) y `$R` (contenido) | "Borrar" no borra: deja copia y metadata |
| `$UsnJrnl` | Raiz NTFS | Historial de cambios de archivos | Cronologia de creacion/modificacion/borrado |
| SRUM | `C:\Windows\System32\sru\SRUDB.dat` (y `HKLM\...\NetworkList` para redes) | Consumo de red y energia por aplicacion | Que app hablo por la red, cuando y cuanto |
| Historial de navegador | `AppData\Local\...` | URLs visitadas, descargas | Contexto del incidente |
| Copias de volumen | `C:\System Volume Information` | Snapshots anteriores | Pueden contener la version previa de un archivo "borrado" |

### 7. Herramientas por Plataforma (5 min)

| Plataforma | Herramienta | Para que |
|------------|-------------|----------|
| Windows | PowerShell (`Get-FileHash`, `Get-WinEvent`, `wevtutil`, `reg`) | Recolectar y exportar sin instalar nada |
| Windows | `certutil -hashfile` | Hash rapido desde CMD |
| Windows | FTK Imager (gratuito) | Crear imagenes forenses con hash |
| Windows | Sysinternals (Autoruns, Procmon, Strings) | Persistencia, actividad, cadenas |
| Kali | **Sleuth Kit** (`fls`, `icat`, `istat`, `fsstat`, `mactime`) | Analisis por linea de comandos |
| Kali | **Autopsy** | Interfaz grafica de Sleuth Kit: browse, buscar, timeline |
| Kali | Volatility 3 | Analisis de volcados de memoria (RAM) |
| Kali | `photorec` / `testdisk` | Recuperacion por firmas de archivos |
| Kali | `bulk_extractor`, `binwalk` | Extraer IPs, passwords, archivos incrustados |
| Kali | Wireshark / `tcpdump` | Analisis de capturas de red (pcap) |

---

## Ejercicio 1: Preservar y Recolectar Evidencia en Windows (35 min)

**Enunciado:** Simular un incidente ("un empleado borro un documento confidencial"), preservar la evidencia con hash, recolectar los artefactos de Windows que prueban que el archivo existio y estuvo en la maquina, y dejar todo documentado con cadena de custodia.

**Solucion paso a paso:**

**Paso 1: Crear la estructura del caso**

Abrir **PowerShell como administrador** (clic derecho en Inicio > "Terminal (administrador)") y ejecutar:

```powershell
$caso = "C:\Casos\Caso-2026-001"
New-Item -ItemType Directory -Path "$caso\01-Original","$caso\02-Adquisicion","$caso\03-Analisis","$caso\04-Informe","$caso\05-Hashes" -Force | Out-Null
(Get-Date -Format "yyyy-MM-dd HH:mm:ss") + " - Apertura de caso" | Out-File "$caso\04-Informe\bitacora.txt"
```

**Por que:** misma estructura que se usa en casos reales. Separar original, adquisicion y analisis evita que se mezcle la fuente con el trabajo.

**Paso 2: Crear la evidencia (el "incidente")**

```powershell
# Documento "confidencial"
$doc = "$caso\01-Original\nomina-secreta.txt"
@("NOMINA CONFIDENCIAL - ULUTA S.A.",
  "Empleado: Juan Perez - Sueldo: 45.000",
  "No distribuir") | Out-File $doc -Encoding utf8

# Carpeta simulada de un pendrive
New-Item -ItemType Directory "$caso\01-Original\usb-simulado" -Force | Out-Null
"clave wifi: practica2026" | Out-File "$caso\01-Original\usb-simulado\notas.txt"
Get-ChildItem "$caso\01-Original" -Recurse -File
```

**Paso 3: Sellar la evidencia con hash ANTES de tocar nada**

```powershell
Get-FileHash "$caso\01-Original\nomina-secreta.txt" -Algorithm SHA256 |
  Format-List | Out-File "$caso\05-Hashes\hash-origen.txt"
Get-Content "$caso\05-Hashes\hash-origen.txt"
```

**Salida esperada (orientativa):**

```
Algorithm : SHA256
Hash      : 3f2a9c... (64 caracteres hexadecimales)
Path      : C:\Casos\Caso-2026-001\01-Original\nomina-secreta.txt
```

**Por que:** ese valor es la huella del archivo. Si mas adelante el hash da distinto, algo cambio y hay que declararlo.

**Paso 4: Copia de trabajo y verificacion**

```powershell
Copy-Item "$caso\01-Original\*" "$caso\02-Adquisicion\" -Recurse
$orig = Get-FileHash "$caso\01-Original\nomina-secreta.txt" -Algorithm SHA256
$copia = Get-FileHash "$caso\02-Adquisicion\nomina-secreta.txt" -Algorithm SHA256
if ($orig.Hash -eq $copia.Hash) { "OK: la copia es identica al original" }
else { "FALLO: la copia difiere del original" }
Get-ChildItem "$caso\02-Adquisicion" -Recurse -File |
  Get-FileHash -Algorithm SHA256 |
  Export-Csv "$caso\05-Hashes\hashes-adquisicion.csv" -NoTypeInformation
```

**Por que:** todo el analisis posterior se hace sobre `02-Adquisicion`. El original queda intacto.

**Paso 5: Simular el borrado por el "atacante"**

```powershell
Add-Type -AssemblyName Microsoft.VisualBasic
[Microsoft.VisualBasic.FileIO.FileSystem]::DeleteFile($doc,'OnlyErrorDialogs','SendToRecycleBin')
Test-Path $doc    # False: ya no existe en su carpeta
```

**Por que:** borrado normal, el mismo que hace un usuario. **Leccion: borrar no borra.** Windows mueve el archivo a `$Recycle.Bin` y deja dos registros: `$I...` (ruta original, tamano y fecha) y `$R...` (el contenido real).

**Paso 6: Recolectar informacion volatil primero**

```powershell
$ev = "$caso\03-Analisis"
Get-Date -Format "yyyy-MM-dd HH:mm:ss" | Out-File "$ev\fecha-hora.txt"
systeminfo | Out-File "$ev\systeminfo.txt"
ipconfig /all | Out-File "$ev\ipconfig.txt"
arp -a | Out-File "$ev\arp.txt"
netstat -ano | Out-File "$ev\netstat.txt"
tasklist /svc | Out-File "$ev\tasklist.txt"
Get-Process | Sort-Object WS -Descending | Select-Object -First 30 Name,Id,WS |
  Format-Table | Out-File "$ev\procesos.txt"
```

**Por que cada uno:**

| Comando | Que prueba |
|---------|------------|
| `fecha-hora` | Hora local para cruzar cronologias con otros equipos |
| `systeminfo` | SO, parches, ultimo arranque, dominio |
| `ipconfig /all` | IP, MAC, DNS, gateway: a que red pertenecia el equipo |
| `arp -a` | Que equipos veia la maquina (movimiento lateral) |
| `netstat -ano` | Conexiones activas: posible canal de salida de datos o C2 |
| `tasklist /svc` | Procesos con sus servicios (procesos sospechosos) |
| `procesos` | Los 30 procesos que mas memoria usan |

**Paso 7: Historial de dispositivos USB**

```powershell
reg query "HKLM\SYSTEM\CurrentControlSet\Enum\USBSTOR" /s | Out-File "$ev\usbstor.txt"
reg query "HKLM\SYSTEM\MountedDevices" /s | Out-File "$ev\mounted.txt"
Get-Content "$ev\usbstor.txt" | Select-String "FriendlyName|USBSTOR"
```

**Salida esperada (orientativa):**

```
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Enum\USBSTOR\Disk&Ven_SanDisk&Prod_Cruzer_Blade...
    FriendlyName    REG_SZ    SanDisk Cruzer Blade USB Device
```

**Por que:** aunque el pendrive ya este desconectado, el registro conserva marca, modelo y **numero de serie**. Es la firma fisica de que ese dispositivo estuvo conectado en esa PC.

**Paso 8: Exportar los logs de seguridad y persistencia**

```powershell
# Requiere PowerShell como administrador
wevtutil epl Security "$ev\seguridad.evtx" /q:"*[System[(EventID=4624 or EventID=4625 or EventID=4688 or EventID=1102)]]"
wevtutil epl System "$ev\sistema.evtx"

Get-WinEvent -Path "$ev\seguridad.evtx" |
  Select-Object TimeCreated,Id,@{n='Detalle';e={($_.Message -replace "`r?`n",' ').Substring(0,[Math]::Min(120,$_.Message.Length))}} |
  Format-Table -AutoSize | Out-File "$ev\eventos.txt" -Width 300

# Persistencia: que arranca con el equipo
reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /s | Out-File "$ev\run-usuario.txt"
reg query "HKLM\Software\Microsoft\Windows\CurrentVersion\Run" /s | Out-File "$ev\run-maquina.txt"

# Programas ejecutados recientemente
New-Item -ItemType Directory "$ev\prefetch" -Force | Out-Null
Copy-Item C:\Windows\Prefetch\*.pf "$ev\prefetch\" -Force -ErrorAction SilentlyContinue
(Get-ChildItem "$ev\prefetch").Count
```

**Que significan los EventIDs:**

| EventID | Significado | Por que importa |
|---------|-------------|-----------------|
| 4624 | Inicio de sesion exitoso | Quien entro y cuando |
| 4625 | Inicio de sesion fallido | Intentos de fuerza bruta |
| 4688 | Se creo un nuevo proceso | Que programa ejecuto (con detalle si hay auditoria) |
| 1102 | Alguien limpio el log de seguridad | **Advertencia de encubrimiento** |

**Paso 9: Leer la papelera de reciclaje (el archivo "borrado")**

```powershell
function Leer-Papelera {
  param([string]$Ruta)
  $b = [System.IO.File]::ReadAllBytes($Ruta)
  if ($b.Length -lt 28) { return }
  $tam   = [BitConverter]::ToInt64($b, 8)
  $ft    = [BitConverter]::ToInt64($b, 16)
  $fecha = [DateTime]::FromFileTime($ft)
  $len   = [BitConverter]::ToInt32($b, 24)
  $orig  = [System.Text.Encoding]::Unicode.GetString($b, 28, [Math]::Min($len*2, $b.Length-28))
  [PSCustomObject]@{ Original = $orig; Tamano = $tam; FechaBorrado = $fecha }
}

Get-ChildItem 'C:\$Recycle.Bin' -Force -Recurse -Filter '$I*' -ErrorAction SilentlyContinue |
  ForEach-Object { Leer-Papelera $_.FullName } | Format-Table -AutoSize |
  Out-File "$ev\papelera.txt" -Width 300
Get-Content "$ev\papelera.txt"
```

**Salida esperada (orientativa):**

```
Original                                       Tamano  FechaBorrado
--------                                       ------  ------------
C:\Casos\Caso-2026-001\01-Original\nomina-...  82      07/10/2026 14:32:10
```

**Por que:** se recupera la **ruta original, el tamano y la fecha exacta de borrado** sin necesidad de herramientas externas. El contenido real esta en el archivo hermano `$R...` (se puede copiar y leer tal cual).

**Paso 10: Sellar el caso con hash final y cadena de custodia**

```powershell
Get-ChildItem "$caso\01-Original","$caso\02-Adquisicion" -Recurse -File |
  Get-FileHash -Algorithm SHA256 |
  Export-Csv "$caso\05-Hashes\hashes-final.csv" -NoTypeInformation
Get-Content "$caso\05-Hashes\hashes-adquisicion.csv" | Select-Object -First 3
```

**Plantilla de cadena de custodia:**

```
CADENA DE CUSTODIA
Caso: Caso-2026-001
Evidencia N: 001 - Disco logico "carpeta de caso" y artefactos exportados
Descripcion: Copia de nomina-secreta.txt y artefactos de Windows
Hash SHA-256 (origen): 3f2a9c... (ver 05-Hashes\hash-origen.txt)
Recolectado por: [Nombre y firma]
Fecha y hora: 2026-10-07 14:05 (UTC-3)
Lugar origen: PC Windows 11 - IP 192.168.1.25
Almacenado en: C:\Casos\Caso-2026-001
Transferido a: [Nombre y firma] - fecha - motivo
Observaciones: El original fue borrado a las 14:32 y recuperado de la papelera
```

---

## Ejercicio 2: Imagen Forense y Recuperacion de Archivos Borrados en Kali (35 min)

**Enunciado:** Construir en la VM de Kali una imagen forense de un "pendrive" simulado, borrar un archivo, sellar la imagen con hash y recuperar el archivo borrado con Sleuth Kit sin montar la imagen en modo escritura.

**Solucion paso a paso:**

**Paso 0: Preparar la VM**

1. En VirtualBox: seleccionar la VM de Kali > **Configurar > Red > Conectar en: Puente (Bridged Adapter)**.
   **Por que:** con "NAT" la VM esta oculta atras del equipo anfitrion y no puede ver la red casera; con "Puente" obtiene IP propia en la misma red.
2. Iniciar Kali y abrir una terminal:

```bash
sudo apt update && sudo apt install -y sleuthkit autopsy dosfstools
mkdir -p ~/caso-forense && cd ~/caso-forense
```

**Paso 1: Crear el "pendrive" del incidente**

```bash
dd if=/dev/zero of=usb.img bs=1M count=64 status=progress
mkfs.vfat -F 32 usb.img
sudo mount -o loop usb.img /mnt
echo "Informe confidencial: proyecto UTU 2026" | sudo tee /mnt/informe.txt
echo "wifi: practica2026 / router admin: admin123" | sudo tee /mnt/notas.txt
ls -la /mnt
```

**Por que FAT32:** es el sistema de archivos tipico de un pendrive, y TSK lo analiza directamente. La imagen `usb.img` es una **copia bit a bit** de ese pendrive simulado.

**Paso 2: Simular el borrado y cerrar la imagen**

```bash
sudo rm /mnt/notas.txt
sync
sudo umount /mnt
sha256sum usb.img | tee usb.sha256
```

**Por que:** al "borrar" en FAT32 el sistema solo marca el cluster como libre en la tabla y pone `0xE5` en la entrada del directorio; **el contenido sigue ahi hasta que algo lo sobrescriba**. Ese es el fundamento fisico de la recuperacion de borrados. El `sha256sum` sella la imagen: cualquier cambio posterior se detecta.

**Paso 3: Listar el contenido de la imagen (sin montarla)**

```bash
fsstat usb.img | head -20
fls -r usb.img
fls -r -d usb.img
```

**Salida esperada (orientativa):**

```
$ fls -r usb.img
v/d 3: (Volume Label)
r/r 12: informe.txt

$ fls -r -d usb.img
r/r * 13: notas.txt
```

**Como se lee:** `r/r` = archivo regular (`d/d` = directorio). El **`*` marca un archivo borrado** y el numero que sigue (`13`) es su **inode** (direccion dentro de la imagen). Si el formato tiene guiones (ej. `13-128`), usalo completo tal cual.

**Por que funciona sin montar:** `fls` solo lee la imagen. Montarla en modo lectura-escritura haria que Linux escriba en ella (journal, fechas) y destruiria la evidencia.

**Paso 4: Recuperar el archivo borrado**

```bash
istat usb.img 13          # metadata: fechas de creacion, modificacion, acceso, tamano
icat usb.img 13 > notas-recuperadas.txt
cat notas-recuperadas.txt
sha256sum notas-recuperadas.txt
```

**Salida esperada:**

```
wifi: practica2026 / router admin: admin123
```

**Si `icat` devuelve el archivo vacio o falla:** la zona fue sobrescrita o el inode cambio. Reintenta con el numero exacto que imprime `fls -r -d usb.img`; como alternativa, usa `photorec usb.img` (recupera por firmas) o el Ejercicio 3 (Autopsy). **Leccion:** cuanto mas se usa el equipo despues del borrado, menos se recupera.

**Paso 5: Verificar que el original sigue intacto**

```bash
sha256sum -c usb.sha256
```

**Salida esperada:** `usb.img: OK`

**Por que:** demuestra que todo el analisis se hizo sin alterar la imagen. Es el mismo principio del Paso 3 del Ejercicio 1, ahora aplicado a un disco.

**Paso 6: Reconstruir la linea de tiempo (timeline)**

```bash
fls -r -m / usb.img > bodyfile.txt
mactime -b bodyfile.txt > timeline.txt
cat timeline.txt
grep -i "notas" timeline.txt
```

**Por que:** `mactime` ordena por fecha todos los eventos (creacion `c`, modificacion `m`, acceso `a`, cambio de metadatos `b`) usando los cuatro tiempos MACB. En un caso real ahi se responde **"que paso primero"**: si un archivo se modifico antes o despues de que entro el USB.

**Paso 7: Pasar artefactos de Windows a la VM (opcional pero recomendado)**

Tres formas, de mas simple a mas robusta:

```bash
# Opcion A - Carpeta compartida (VirtualBox: Dispositivos > Carpetas compartidas)
sudo mount -t vboxsf Casos /mnt/caso

# Opcion B - Red en modo puente: copiar desde Windows
#   En Windows (PowerShell):  scp -r C:\Casos\Caso-2026-001 kali@192.168.1.100:~/

# Opcion C - Pasar la USB fisica a la VM (Dispositivos > USB > marcar el dispositivo)
```

**Por que:** el incidente ocurre en Windows y el analisis grafico es mejor en Kali; hay que mover la evidencia **con su hash viajando junto** para verificarla al llegar:

```bash
# Recalcular los hashes en Kali y compararlos con el CSV exportado desde Windows
# (sha256sum -c no sirve aca: el CSV tiene columnas Algorithm,Hash,Path)
find /mnt/caso -type f -exec sha256sum {} \; > hashes-kali.txt
while read h f; do
  grep -qi "$h" hashes-adquisicion.csv && echo "OK     $f" || echo "DIFFER $f"
done < hashes-kali.txt
```

---

## Ejercicio 3: Analisis Grafico con Autopsy (15 min)

**Enunciado:** Repetir el analisis anterior usando la interfaz grafica de Autopsy, para ver como trabaja un analista en la practica (y como se veria un informe automatico).

**Solucion paso a paso:**

**Paso 1:** En la terminal de Kali:

```bash
# El locker (donde Autopsy guarda sus datos) en tu home, sin sudo:
# el puerto 9999 no requiere privilegios
autopsy -d ~/caso-autopsy -p 9999
# Abrir Firefox: http://localhost:9999
```

Si la version instalada es la GUI (Autopsy 4), usar el menu **Aplicaciones > Forensics > Autopsy** en vez de la terminal.

**Paso 2:** En la interfaz web:
1. **New Case** > nombre `Caso-2026-001`, fecha, investigador, descripcion
2. **Add Image** > ruta absoluta `/home/kali/caso-forense/usb.img` (o `pwd` dentro de la carpeta para copiar la ruta), tipo "Disk Image"
3. Esperar a que termine el ingest (indexado)

**Paso 3:** Explorar:
- **File Activity** > *Deleted Files*: debe aparecer `notas.txt`
- **File System** > navegar el volumen y abrir `informe.txt`
- **Timeline**: filtrar por fecha y ver los eventos MACB
- **Keyword Search**: buscar `wifi` o `admin123`

**Paso 4:** Exportar los resultados (Results > Export) y adjuntarlos al informe.

**Por que:** Autopsy usa exactamente las mismas librerias de Sleuth Kit, pero agrega busqueda, timeline automatica, hashes de catalogo y exportacion. **Importante:** en el informe siempre se documenta la herramienta y version usada, para que otro analista pueda repetir el analisis y obtener lo mismo (reproducibilidad).

---

## Ejercicio 4: Informe Forense (entregable, 10 min)

**Enunciado:** Redactar un informe de una pagina por evidencia, siguiendo esta estructura:

```
INFORME FORENSE - Caso 2026-001
1. RESUMEN EJECUTIVO      -> Que paso, en 5 lineas, sin tecnicismos
2. ALCANCE Y AUTORIZACION -> Que equipo, quien autorizo, fecha
3. METODOLOGIA            -> Fases aplicadas, herramientas y versiones
4. EVIDENCIA RECIBIDA     -> Tabla: descripcion, hash SHA-256, custodio
5. HALLAZGOS              -> Nro, artefacto, evidencia citada, interpretacion
6. CRONOLOGIA             -> Fecha/hora (UTC-3), evento, fuente
7. CONCLUSIONES           -> Solo lo que la evidencia respalda
8. LIMITACIONES           -> Que NO se pudo determinar y por que
9. ANEXOS                 -> Hashes, cadena de custodia, capturas
```

**Solucion paso a paso:**

1. Recopilar los productos de los Ejercicios 1 y 2: `hashes.txt`, `cadena-custodia.txt`, la salida de `fls`, los `$I` de la papelera, el `istat` de los inodos y las capturas de pantalla.
2. Escribir primero la seccion 4 (Evidencia recibida): sin la tabla de hashes no hay informe, porque es lo que demuestra que nada cambio desde el recoleo.
3. Cargar los hallazgos en la seccion 5 con el formato *artefacto -> evidencia citada -> interpretacion*, citando el archivo o comando exacto que lo respalda.
4. Armar la cronologia (seccion 6) ordenando por fecha/hora los eventos de las fuentes distintas (registro, papelera, `$MFT`, logs) y anotando en cada linea la fuente.
5. Redactar las conclusiones **solo con lo que la evidencia sostiene**; lo que no se pudo probar va en "Limitaciones".
6. Pegar en Anexos el contenido de `hashes.txt`, la cadena de custodia y las salidas de `fls`/`istat`.
7. Releer marcando toda afirmacion que no tenga evidencia atras y borrarla o moverla a Limitaciones.

**Ejemplo de hallazgo bien escrito (y su contraparte mala):**

```
MAL:  "El empleado borro archivos para ocultar lo que hizo."
BIEN: "El archivo nomina-secreta.txt fue enviado a la papelera de
       reciclaje el 07/10/2026 14:32:10 (fuente: registro $I de la
       papelera, anexo 4). La intencion no puede determinarse con
       la evidencia disponible."
```

**Por que:** un informe forense se sostiene solo con hechos verificables. Afirmar intenciones sin evidencia hace que todo el trabajo pierda credibilidad.

---

## Glosario

| Termino | Definicion | Por que importa |
|---------|------------|-----------------|
| **Evidencia digital** | Cualquier dato almacenado o transmitido por medios electronicos | Es lo unico que sostiene la conclusion |
| **Hash / resumen criptografico** | Huella digital de un archivo (SHA-256) | Demuestra que el archivo no cambio |
| **Cadena de custodia** | Registro ininterrumpido de quien tuvo la evidencia | Sin ella la evidencia es cuestionable |
| **Imagen forense** | Copia bit a bit de un disco | Permite analizar sin tocar el original |
| **Write blocker** | Dispositivo que impide escribir sobre la fuente | Evita destruir evidencia al leerla |
| **Orden de volatilidad** | Prioridad de recoleccion segun que datos desaparecen primero | Si apagas antes de capturar RAM, se pierde |
| **Inode** | Numero unico de un archivo dentro del sistema de archivos | Es la direccion que se usa para recuperarlo con `icat` |
| **MACB** | Modify, Access, Change, Birth: los 4 tiempos de un archivo | Base de cualquier cronologia |
| **Timeline / cronologia** | Eventos ordenados por fecha y hora | Responde "que paso primero" |
| **$MFT** | Tabla maestra NTFS con todos los archivos | Existen aunque los archivos esten borrados |
| **Prefetch** | Cache de Windows sobre programas ejecutados | Prueba de ejecucion de software |
| **Artefacto** | Resto utilizable que deja un programa o el SO | Casi siempre evidencia sin buscar |
| **AmCache** | Base de Windows con hashes de binarios ejecutados | Refuerza Prefetch con hashes |
| **USBSTOR** | Clave del registro con historial de USB | Identifica pendrives por serie |
| **EventID** | Numero de un evento del registro de Windows | 4624 login, 1102 limpieza de log |
| **Papelera ($I/$R)** | Registros de la papelera: metadata y contenido | "Borrar" solo mueve el archivo |
| **`$UsnJrnl`** | Journal NTFS de cambios de archivos | Historial de creaciones y borrados |
| **Volatil** | Dato que desaparece al apagar (RAM, conexiones) | Hay que capturarlo primero |
| **Sleuth Kit (TSK)** | Suite CLI de analisis forense | Estandar de la industria |
| **Autopsy** | GUI sobre Sleuth Kit | Analisis visual, busqueda y timeline |
| **Volatility** | Framework de analisis de RAM | Encuentra claves, procesos y malware en memoria |
| **File carving** | Recuperar archivos por firmas sin metadata | Cuando la tabla esta destruida |
| **DD / raw** | Formato de imagen sin compresion | Universal y fiel al original |
| **E01** | Formato de imagen con hash interno | Integridad embebida + compresion |
| **Degaussing** | Borrado magnetico con campo fuerte | Destruye evidencia irreversiblemente |
| **ISO 27037** | Guia internacional para evidencia digital | Define como recolectar bien |
| **Taint / contaminacion** | Alteracion accidental de la evidencia | Invalida todo el analisis |
| **Reproducibilidad** | Que otro analista obtenga lo mismo | Garantia cientifica del informe |
| **Dump / volcado** | Copia completa de la memoria RAM | Unica forma de ver datos en claro en ejecucion |

---

## Preguntas y Respuestas

**1. Por que no se puede analizar directamente el disco afectado?**

Porque cualquier sistema operativo escribe constantemente: cache, logs, fechas de acceso, temporales. En minutos alteraria metadatos y podria sobrescribir los mismos sectores borrados que queremos recuperar. Por eso se trabaja sobre una imagen verificada con hash.

**2. Cual es la diferencia entre MD5 y SHA-256 y cual usar?**

MD5 genera 32 caracteres y su estructura esta rota (existen colisiones practicas). SHA-256 genera 64 caracteres y no tiene colisiones conocidas. Para evidencia se usa SHA-256; MD5 todavia sirve como comprobacion accidental de integridad, nunca como prueba criptografica.

**3. Borre un archivo y no esta en la papelera. Se puede recuperar?**

Depende. El sistema operativo solo marca el espacio como libre; el dato persiste hasta que se sobrescriba. Con Sleuth Kit (`fls -d` + `icat`) o `photorec` se puede recuperar si no se escribio encima. Cada escritura posterior reduce las probabilidades: por eso hay que aislar el equipo y actuar rapido.

**4. Que demuestra el evento 1102 en un log de seguridad?**

Que alguien (un usuario administrador o un atacante) limpio explicitamente el registro de auditoria. En una investigacion es una bandera roja: hay intencion de ocultar actividad. No prueba el delito, pero cambia por completo la interpretacion de los logs faltantes.

**5. Si la copia y el original tienen el mismo hash, eso prueba que la copia es identica?**

Si, con un nivel de certeza altisimo: dos archivos distintos con el mismo SHA-256 no existen practicamente. Es la razon por la que el hash viaja junto a la evidencia en cada transferencia.

**6. El equipo sigue encendido, no se apago. Que hago primero?**

Primero capturar memoria (orden de volatilidad): volcado de RAM con DumpIt/FTK Imager, luego estado de red y procesos, y recien ahi apagar o aislar. Si no hay herramientas de volcado, al menos exportar netstat, procesos y logs antes de apagar.

**7. La fecha de modificacion de un archivo prueba quien lo modifico?**

No. Prueba **cuando** cambio, no quien lo hizo. La atribucion requiere cruzar con logs de autenticacion (4624), procesos ejecutados (4688), LNK/Recent y, si existe, informacion de la cuenta de usuario y la estacion de trabajo. Un timestamp aislado es evidencia incompleta.

**8. Es legal hacer practicas forenses en el aula?**

Si, siempre que se trabaje sobre equipos propios, maquinas virtuales o imagenes de prueba provistas por el docente, y con autorizacion explicita del dueno del equipo. Aplicar estas tecnicas sobre equipos o redes ajenos sin permiso configura acceso no autorizado, tipificado por la legislacion vigente.

---

## Tarea / Lectura Recomendada

1. **Practicar:** Repetir el Ejercicio 1 completo en una VM de Windows de prueba (se puede descargar una VM de Windows 11 para desarrollo de Microsoft) y entregar la carpeta de caso con `hashes-final.csv` y la cadena de custodia firmada.
2. **Practicar:** Crear una segunda imagen en Kali con un sistema de archivos NTFS (`mkfs.ntfs`) y recuperar dos archivos borrados, comparando el output de `fls` con el de FAT32.
3. **Leer:** RFC 3227 - *Guidelines for Evidence Collection and Archiving*: https://www.rfc-editor.org/rfc/rfc3227
4. **Leer:** NIST SP 800-86 - *Guide to Integrating Forensic Techniques into Incident Response*.
5. **Leer:** ISO/IEC 27037 - *Identification, collection, acquisition and preservation of digital evidence*.
6. **Ver:** caso practico de Autopsy oficial: https://www.sleuthkit.org/autopsy/
7. **Investigar:** Volatility 3 con un volcado de memoria publico para practica (ej. los de https://github.com/volatilityfoundation/volatility3 y repos de capturas DFRWS).
8. **Reflexionar:** Escribir 5 reglas propias de "como no perder evidencia" a partir de la tabla de errores que invalidan una investigacion.
