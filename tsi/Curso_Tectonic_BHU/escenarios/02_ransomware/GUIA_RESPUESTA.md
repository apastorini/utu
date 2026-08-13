# GUIA DE RESPUESTA - ESCENARIO RANSOMWARE

## Banco del Sol - Simulacion de Ataque Ransomware

**Escenario:** 02 - Ransomware
**Objetivo:** Servidor de archivos (fileserver)
**Tipo de ataque:** Cifrado AES-256 de archivos compartidos
**Rol del estudiante:** Equipo azul (defensores)

---

## FASE 1: DETECCION

### 1.1 Alerta inicial

Los usuarios reportan que no pueden acceder a los archivos en las carpetas compartidas del servidor. Los archivos aparecen con extension `.encrypted` y hay un archivo `README_RANSOM.txt` en cada directorio.

### 1.2 Verificar conectividad del fileserver

```powershell
# Desde la estacion de trabajo o consola de administracion
ping fileserver
Test-NetConnection fileserver -Port 445
Test-NetConnection fileserver -Port 3389
```

### 1.3 Listar archivos en shares compartidos

```powershell
# Verificar archivos en Datos_Clientes
dir \\fileserver\Datos_Clientes

# Verificar archivos en Reportes_Financieros
dir \\fileserver\Reportes_Financieros

# Verificar archivos en Recursos_Humanos
dir \\fileserver\Recursos_Humanos

# Buscar archivos cifrados en todos los shares
Get-ChildItem -Path \\fileserver -Recurse -Filter "*.encrypted" -ErrorAction SilentlyContinue
```

### 1.4 Identificar indicadores de ransomware

```powershell
# Buscar notas de rescate
Get-ChildItem -Path \\fileserver -Recurse -Filter "README_RANSOM*" -ErrorAction SilentlyContinue

# Ver contenido de la nota de rescate
Get-Content \\fileserver\Datos_Clientes\README_RANSOM.txt

# Contar archivos cifrados por share
$shares = @("Datos_Clientes", "Reportes_Financieros", "Recursos_Humanos")
foreach ($share in $shares) {
    $encrypted = Get-ChildItem -Path "\\fileserver\$share" -Recurse -Filter "*.encrypted" -ErrorAction SilentlyContinue
    Write-Host "$share: $($encrypted.Count) archivos cifrados"
}
```

### 1.5 Verificar logs de seguridad del fileserver

```powershell
# Conectar al fileserver via RDP o PowerShell remoting
Enter-PSSession -ComputerName fileserver

# Revisar eventos de seguridad recientes
Get-WinEvent -LogName Security -MaxEvents 50 | Format-Table TimeCreated, Id, Message -AutoSize

# Buscar eventos de inicio de sesion (4624 = exitoso, 4625 = fallido)
Get-WinEvent -FilterHashtable @{LogName='Security'; Id=4624} -MaxEvents 20

# Buscar eventos de creacion de procesos (4688)
Get-WinEvent -FilterHashtable @{LogName='Security'; Id=4688} -MaxEvents 20
```

---

## FASE 2: ANALISIS

### 2.1 Conectar al fileserver para analisis

```powershell
# Opcion 1: PowerShell remoting
Enter-PSSession -ComputerName fileserver -Credential (Get-Credential)

# Opcion 2: RDP desde workstation
mstsc /v:fileserver

# Opcion 3: SMB directo
net use \\fileserver\C$ /user:BancoDelSol\cmartinez
```

### 2.2 Analizar la nota de rescate

```powershell
# Leer la nota de rescate
Get-Content C:\Shares\Datos_Clientes\README_RANSOM.txt

# Informacion clave de la nota:
# - Metodo de cifrado: AES-256-CBC
# - Archivos afectados: .csv, .xlsx, .docx, .pdf, .json, .dat, .txt, .log
# - Extension de archivos cifrados: .encrypted
# - Copias de sombra eliminadas (segundo la nota)
# - Backup oculto mencionado: C:\Shares\.backup_hidden\
```

### 2.3 Verificar archivos cifrados

```powershell
# Listar todos los archivos cifrados
Get-ChildItem -Path "C:\Shares" -Recurse -Filter "*.encrypted" |
    Select-Object FullName, Length, LastWriteTime |
    Format-Table -AutoSize

# Contar archivos por directorio
Get-ChildItem -Path "C:\Shares" -Recurse -Directory | ForEach-Object {
    $count = (Get-ChildItem -Path $_.FullName -Filter "*.encrypted" -ErrorAction SilentlyContinue).Count
    [PSCustomObject]@{
        Directorio = $_.FullName
        ArchivosCifrados = $count
    }
} | Format-Table -AutoSize

# Comparar archivos originales vs cifrados
$originalFiles = Get-ChildItem -Path "C:\Shares" -Recurse -File -ErrorAction SilentlyContinue |
    Where-Object { $_.Extension -ne ".encrypted" -and $_.Name -ne "README_RANSOM.txt" }
$encryptedFiles = Get-ChildItem -Path "C:\Shares" -Recurse -Filter "*.encrypted" -ErrorAction SilentlyContinue

Write-Host "Archivos originales: $($originalFiles.Count)"
Write-Host "Archivos cifrados: $($encryptedFiles.Count)"
```

### 2.4 Analizar el log del ransomware

```powershell
# Leer el log completo
Get-Content C:\Shares\.ransom_log.txt

# Buscar patrones especificos en el log
Select-String -Path "C:\Shares\.ransom_log.txt" -Pattern "ENCRYPT"
Select-String -Path "C:\Shares\.ransom_log.txt" -Pattern "BACKUP"
Select-String -Path "C:\Shares\.ransom_log.txt" -Pattern "NOTE"

# Contar operaciones
$encryptCount = (Select-String -Path "C:\Shares\.ransom_log.txt" -Pattern "ENCRYPT:").Count
$backupCount = (Select-String -Path "C:\Shares\.ransom_log.txt" -Pattern "BACKUP:").Count
Write-Host "Archivos cifrados: $encryptCount"
Write-Host "Archivos respaldados: $backupCount"
```

### 2.5 Verificar eliminacion de copias de sombra

```powershell
# Listar copias de sombra actuales
vssadmin list shadows

# Si no hay copias de sombra, el atacante las elimino
# Si hay copias, se pueden usar para recuperar archivos

# Verificar logs de VSS
Get-Content C:\Shares\Logs\vss_deletion_simulation.log -ErrorAction SilentlyContinue
Get-Content C:\Shares\Logs\vss_before_delete.log -ErrorAction SilentlyContinue

# Verificar servicio VSS
Get-Service VSS | Format-Table Name, Status, StartType
```

### 2.6 Analizar persistencia del malware

```powershell
# Verificar entradas de registro de inicio
Get-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
Get-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce"

# Buscar entradas sospechosas
Get-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" |
    Select-Object * -ExcludeProperty PS* |
    ForEach-Object {
        $_.PSObject.Properties | Where-Object {
            $_.Name -notlike "PS*" -and $_.Value -like "*ransom*"
        }
    }

# Verificar servicios sospechosos
Get-Service | Where-Object {$_.DisplayName -like "*ransom*" -or $_.DisplayName -like "*BancDelSol*"}

# Verificar tareas programadas sospechosas
Get-ScheduledTask | Where-Object {$_.TaskName -like "*ransom*" -or $_.TaskName -like "*BancDelSol*"}
```

### 2.7 Analizar el script de ransomware

```powershell
# El script esta en C:\Shares\ransomware_simulator.py
Get-Content C:\Shares\ransomware_simulator.py

# Analizar el script:
# - Identifica el algoritmo de cifrado: AES-256-CBC
# - Crea copias de seguridad en C:\Shares\.backup_hidden\
# - Renombra archivos con extension .encrypted
# - Crea notas README_RANSOM.txt
# - Registra actividad en C:\Shares\.ransom_log.txt
```

### 2.8 Verificar indicadores de red

```powershell
# Revisar indicadores de trafico
Get-Content C:\Shares\Logs\network_indicators.log -ErrorAction SilentlyContinue

# Ver conexiones activas
netstat -ano | findstr "445"
netstat -ano | findstr "3389"
netstat -ano | findstr "5985"

# Ver procesos que usan estas conexiones
Get-Process -Id (netstat -ano | findstr ":445" | ForEach-Object { ($_ -split '\s+')[-1] } | Sort-Object -Unique)
```

### 2.9 Identificar vector de entrada

```powershell
# Revisar eventos de autenticacion
Get-WinEvent -FilterHashtable @{LogName='Security'; Id=4624} -MaxEvents 50 |
    Where-Object {$_.TimeCreated -gt (Get-Date).AddHours(-2)} |
    Format-Table TimeCreated, Message -AutoSize

# Buscar inicios de sesion desde IPs externas
Get-WinEvent -FilterHashtable @{LogName='Security'; Id=4624} -MaxEvents 100 |
    Where-Object {$_.Message -like "*10.10.2.100*"} |
    Format-Table TimeCreated, Message -AutoSize

# Revisar correo del usuario comprometido (mailserver)
# En el mailserver:
# ls /home/cmartinez/Maildir/new/
# cat /home/cmartinez/Maildir/new/1701412200.V802I00458B.mailsrv
```

---

## FASE 3: CONTENCION

### 3.1 Aislar el fileserver

```powershell
# Opcion 1: Deshabilitar la interfaz de red (si hay acceso local)
Disable-NetAdapter -Name "Ethernet" -Confirm:$false

# Opcion 2: Configurar firewall para bloquear trafico
New-NetFirewallRule -DisplayName "BLOCK_ALL_INBOUND" -Direction Inbound -Action Block -Enabled True
New-NetFirewallRule -DisplayName "BLOCK_ALL_OUTBOUND" -Direction Outbound -Action Block -Enabled True

# Opcion 3: Cambiar reglas SMB existentes
Set-NetFirewallRule -DisplayName "SMB-In" -Enabled False

# Opcion 4: Mover el fileserver a VLAN de aislamiento (si se tiene acceso al switch)
# Configuracion del switch: move port X to VLAN quarantine
```

### 3.2 Preservar evidencia antes de contencion

```powershell
# 1. Capturar estado del sistema
systeminfo > C:\Forensics\systeminfo_$(Get-Date -Format 'yyyyMMdd_HHmmss').txt
ipconfig /all > C:\Forensics\network_$(Get-Date -Format 'yyyyMMdd_HHmmss').txt
netstat -ano > C:\Forensics\netstat_$(Get-Date -Format 'yyyyMMdd_HHmmss').txt
tasklist > C:\Forensics\processes_$(Get-Date -Format 'yyyyMMdd_HHmmss').txt

# 2. Exportar logs de eventos
wevtutil epl Security C:\Forensics\security_$(Get-Date -Format 'yyyyMMdd_HHmmss').evtx
wevtutil epl System C:\Forensics\system_$(Get-Date -Format 'yyyyMMdd_HHmmss').evtx
wevtutil epl Application C:\Forensics\application_$(Get-Date -Format 'yyyyMMdd_HHmmss').evtx
wevtutil epl "Windows PowerShell" C:\Forensics\powershell_$(Get-Date -Format 'yyyyMMdd_HHmmss').evtx

# 3. Capturar hash de archivos
Get-ChildItem -Path "C:\Shares" -Recurse -File |
    ForEach-Object {
        [PSCustomObject]@{
            Path = $_.FullName
            MD5 = (Get-FileHash $_.FullName -Algorithm MD5).Hash
            SHA256 = (Get-FileHash $_.FullName -Algorithm SHA256).Hash
            Size = $_.Length
            Modified = $_.LastWriteTime
        }
    } | Export-Csv "C:\Forensics\file_hashes_$(Get-Date -Format 'yyyyMMdd_HHmmss').csv" -NoTypeInformation

# 4. Capturar estado del registro
reg export HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run C:\Forensics\autorun.reg
reg export HKLM\SYSTEM\CurrentControlSet\Services C:\Forensics\services.reg

# 5. Ejecutar script de recopilacion de evidencia (si esta disponible)
powershell -ExecutionPolicy Bypass -File C:\Forensics\collect_evidence.ps1
```

### 3.3 Bloquear cuentas comprometidas

```powershell
# En el Domain Controller
Enter-PSSession -ComputerName domaincontroller

# Bloquear cuenta del usuario comprometido
Disable-ADAccount -Identity cmartinez

# Cambiar contrasena de cuentas criticas
Set-ADAccountPassword -Identity cmartinez -NewPassword (ConvertTo-SecureString "NuevaC@ntrasena2025!" -AsPlainText -Force)

# Forzar cambio de contrasena en proximo inicio
Set-ADUser -Identity cmartinez -ChangePasswordAtLogon $true

# Verificar cuentas activas
Get-ADUser -Filter {Enabled -eq $true} -Properties LastLogonDate |
    Select-Object Name, SamAccountName, LastLogonDate |
    Sort-Object LastLogonDate -Descending
```

### 3.4 Desactivar shares temporalmente

```powershell
# En el fileserver
# Deshabilitar shares sin eliminarlos
Get-SmbShare | Where-Object {$_.Name -ne "IPC$" -and $_.Name -ne "ADMIN$"} |
    ForEach-Object {
        Block-SmbShareAccess -Name $_.Name -Force
        Write-Host "Share $($_.Name) bloqueado"
    }

# Verificar shares bloqueados
Get-SmbShareAccess
```

---

## FASE 4: ERRADICACION

### 4.1 Eliminar artefactos del ransomware

```powershell
# 1. Eliminar script de ransomware
Remove-Item -Path "C:\Shares\ransomware_simulator.py" -Force -ErrorAction SilentlyContinue

# 2. Eliminar notas de rescate
Get-ChildItem -Path "C:\Shares" -Recurse -Filter "README_RANSOM*" |
    Remove-Item -Force

# 3. Eliminar log del ransomware
Remove-Item -Path "C:\Shares\.ransom_log.txt" -Force -ErrorAction SilentlyContinue

# 4. Eliminar entrada de registro maliciosa
Remove-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" -Name "RansomService" -Force

# 5. Verificar eliminacion
Get-ChildItem -Path "C:\Shares" -Recurse -Filter "README_RANSOM*" -ErrorAction SilentlyContinue
Get-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" -Name "RansomService" -ErrorAction SilentlyContinue
```

### 4.2 Renombrar archivos cifrados

```powershell
# Restaurar nombres originales de archivos
Get-ChildItem -Path "C:\Shares" -Recurse -Filter "*.encrypted" |
    ForEach-Object {
        $originalName = $_.FullName -replace '\.encrypted$', ''
        Rename-Item -Path $_.FullName -NewName (Split-Path $originalName -Leaf)
        Write-Host "Restaurado: $($_.FullName)"
    }

# Verificar restauracion
Get-ChildItem -Path "C:\Shares" -Recurse -Filter "*.encrypted"
Get-ChildItem -Path "C:\Shares" -Recurse -File |
    Where-Object { $_.Extension -ne ".encrypted" }
```

### 4.3 Recuperar desde copias de sombra (si estan disponibles)

```powershell
# Verificar si hay copias de sombra
vssadmin list shadows

# Si hay copias de sombra disponibles:
# Opcion 1: Usar vssadmin para restaurar archivos individuales
# Nota: vssadmin no permite restaurar archivos individuales directamente
# Se debe usar herramientas de terceros o el siguiente metodo

# Opcion 2: Crear punto de montaje para la copia de sombra
# Identificar el ID de la copia de sombra
$shadowId = (vssadmin list shadows | Select-String "Shadow Copy ID:" | Select-Object -First 1).ToString().Split('{')[1].TrimEnd('}')

# Montar la copia de sombra (requiere herramientas adicionales)
# Usar ShadowExplorer o similar para navegar la copia de sombra

# Opcion 3: Usar PowerShell para restaurar desde VSS
# Crear symbolick link a la copia de sombra
$shadowPath = (vssadmin list shadows | Select-String "Shadow Copy Volume:" | Select-Object -First 1).ToString().Split(':')[1].Trim()
mklink /D C:\VSS_Backup "$shadowPath"

# Copiar archivos desde la copia de sombra
Copy-Item -Path "C:\VSS_Backup\Shares\Datos_Clientes\*" -Destination "C:\Shares\Datos_Clientes\" -Recurse -Force
Copy-Item -Path "C:\VSS_Backup\Shares\Reportes_Financieros\*" -Destination "C:\Shares\Reportes_Financieros\" -Recurse -Force
Copy-Item -Path "C:\VSS_Backup\Shares\Recursos_Humanos\*" -Destination "C:\Shares\Recursos_Humanos\" -Recurse -Force

# Limpiar symbolick link
rmdir C:\VSS_Backup
```

### 4.4 Restaurar desde backup oculto (simulacion)

```powershell
# Los archivos originales estan en C:\Shares\.backup_hidden\
# Esta es la ubicacion donde el ransomware simulado guardo las copias

# Verificar contenido del backup
Get-ChildItem -Path "C:\Shares\.backup_hidden" -Recurse -File

# Restaurar archivos desde el backup
$backupPaths = @(
    "C:\Shares\.backup_hidden\Datos_Clientes",
    "C:\Shares\.backup_hidden\Reportes_Financieros",
    "C:\Shares\.backup_hidden\Recursos_Humanos"
)

foreach ($backupPath in $backupPaths) {
    if (Test-Path $backupPath) {
        $shareName = Split-Path $backupPath -Leaf
        $destination = "C:\Shares\$shareName"

        Copy-Item -Path "$backupPath\*" -Destination $destination -Recurse -Force
        Write-Host "Restaurado: $shareName" -ForegroundColor Green
    }
}

# Verificar restauracion
$shares = @("Datos_Clientes", "Reportes_Financieros", "Recursos_Humanos")
foreach ($share in $shares) {
    $files = Get-ChildItem -Path "C:\Shares\$share" -File -ErrorAction SilentlyContinue
    Write-Host "$share: $($files.Count) archivos restaurados"
}
```

### 4.5 Restaurar desde backup del sistema (si esta disponible)

```powershell
# Si hay backups de sistema configurados
wbadmin get versions

# Restaurar archivos desde un backup especifico
# wbadmin start recovery -version:<version> -items:C:\Shares -recoverytype:Files

# Nota: En un escenario real, se verificaria la integridad del backup
# antes de restaurar
```

### 4.6 Verificar integridad post-restauracion

```powershell
# Verificar que los archivos existen
Get-ChildItem -Path "C:\Shares" -Recurse -File |
    Select-Object FullName, Length, LastWriteTime |
    Sort-Object FullName |
    Format-Table -AutoSize

# Verificar que no quedan archivos cifrados
Get-ChildItem -Path "C:\Shares" -Recurse -Filter "*.encrypted" -ErrorAction SilentlyContinue

# Verificar hashes de archivos criticos
Get-FileHash "C:\Shares\Datos_Clientes\clientes_activos_2025_Q4.csv" -Algorithm MD5
Get-FileHash "C:\Shares\Reportes_Financieros\balance_general_octubre_2025.xlsx" -Algorithm MD5

# Verificar que el ransomware fue completamente eliminado
Get-Process | Where-Object {$_.ProcessName -like "*ransom*"} -ErrorAction SilentlyContinue
Get-Service | Where-Object {$_.DisplayName -like "*ransom*"} -ErrorAction SilentlyContinue
```

---

## FASE 5: RECUPERACION

### 5.1 Restablecer servicios

```powershell
# 1. Habilitar shares SMB
Get-SmbShare | Where-Object {$_.Name -ne "IPC$" -and $_.Name -ne "ADMIN$"} |
    Unblock-SmbShareAccess -Name $_.Name -Force

# 2. Verificar servicios criticos
Get-Service VSS, WinRM, RemoteRegistry | Format-Table Name, Status, StartType

# 3. Reiniciar servicios si es necesario
Restart-Service VSS -Force
Restart-Service WinRM -Force
```

### 5.2 Restablecer permisos

```powershell
# Verificar permisos de shares
Get-SmbShareAccess -Name "Datos_Clientes"
Get-SmbShareAccess -Name "Reportes_Financieros"
Get-SmbShareAccess -Name "Recursos_Humanos"

# Restablecer permisos si es necesario
Reset-SmbShareAccess -Name "Datos_Clientes"
Reset-SmbShareAccess -Name "Reportes_Financieros"
Reset-SmbShareAccess -Name "Recursos_Humanos"
```

### 5.3 Habilitar cuentas de usuario

```powershell
# En el Domain Controller
Enable-ADAccount -Identity cmartinez

# Forzar cambio de contrasena
Set-ADAccountPassword -Identity cmartinez -NewPassword (ConvertTo-SecureString "C@rlos2025!_Nueva" -AsPlainText -Force) -Reset
Set-ADUser -Identity cmartinez -ChangePasswordAtLogon $true
```

### 5.4 Verificar conectividad

```powershell
# Desde la workstation, verificar acceso a los shares
Test-Path \\fileserver\Datos_Clientes
Test-Path \\fileserver\Reportes_Financieros
Test-Path \\fileserver\Recursos_Humanos

# Intentar leer archivos
Get-Content \\fileserver\Datos_Clientes\clientes_activos_2025_Q4.csv | Select-Object -First 5

# Mapear unidades de red
net use S: \\fileserver\Datos_Clientes /persistent:yes
net use R: \\fileserver\Reportes_Financieros /persistent:yes
```

### 5.5 Monitoreo post-recuperacion

```powershell
# Monitorear logs de seguridad por 24 horas
# Configurar alertas para eventos similares

# Verificar que no hay actividad sospechosa
Get-WinEvent -FilterHashtable @{LogName='Security'; Id=4624} -MaxEvents 50 |
    Where-Object {$_.TimeCreated -gt (Get-Date).AddHours(-1)} |
    Format-Table TimeCreated, Message -AutoSize

# Verificar que no hay archivos cifrados nuevos
Get-ChildItem -Path "C:\Shares" -Recurse -Filter "*.encrypted" -ErrorAction SilentlyContinue

# Verificar integridad del sistema
sfc /scannow
DISM /Online /Cleanup-Image /RestoreHealth
```

---

## FASE 6: LECCIONES APRENDIDAS

### 6.1 Documentacion del incidente

Crear un informe que incluya:

1. **Resumen ejecutivo**
   - Fecha y hora del incidente
   - Duracion del incidente
   - Impacto en el negocio

2. **Cronologia de eventos**
   - Hora de deteccion
   - Hora de contencion
   - Hora de erradicacion
   - Hora de recuperacion

3. **Indicadores de compromiso (IoC)**
   - Archivos cifrados: lista completa
   - Notas de rescate: ubicacion y contenido
   - Log del ransomware: C:\Shares\.ransom_log.txt
   - Entrada de registro: HKLM\...\Run\RansomService
   - Script de ransomware: C:\Shares\ransomware_simulator.py

4. **Vector de entrada**
   - Phishing al usuario cmartinez
   - Credenciales comprometidas
   - Movimiento lateral via SMB

5. **Acciones tomadas**
   - Contencion del fileserver
   - Preservacion de evidencia
   - Restauracion de archivos
   - Erradicacion del malware

6. **Recomendaciones**
   - Controles de acceso a SMB
   - Monitoreo de movimiento lateral
   - Backups regulares
   - Capacitacion de usuarios

### 6.2 Medidas preventivas

```powershell
# 1. Implementar AppLocker para prevenir ejecucion de scripts
# 2. Configurar监控 de archivos criticos
# 3. Habilitar audit policiy para acceso a archivos
# 4. Configurar backups automatizados con verificacion
# 5. Implementar segmentacion de red
# 6. Capacitacion en seguridad para usuarios
```

### 6.3 Mejoras de seguridad

| Area | Estado Actual | Mejora Propuesta |
|------|--------------|------------------|
| Backups | Manual | Automatizado con verificacion diaria |
| Segmentacion | Plana | VLANs por funcion |
| Monitoreo | Basico | SIEM con alertas automatizadas |
| Acceso SMB | Abierto | Control de acceso basado en roles |
| VSS | Configurado | Verificacion periodica de integridad |
| Capacitacion | Anual | Trimestral con simulacros |

### 6.4 Indicadores para monitoreo futuro

```yaml
# Indicadores a monitorear
file_indicators:
  - "*.encrypted"
  - "README_RANSOM*"
  - ".ransom_log.txt"

process_indicators:
  - "python.exe" (en shares)
  - "vssadmin.exe delete shadows"

network_indicators:
  - SMB lateral movement inusual
  - PowerShell remoting no autorizado

registry_indicators:
  - HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run (valores nuevos)
  - HKLM\SYSTEM\CurrentControlSet\Services (servicios nuevos)
```

---

## COMANDOS DE REFERENCIA RAPIDA

```powershell
# Deteccion
dir \\fileserver\Datos_Clientes
Get-ChildItem -Path \\fileserver -Recurse -Filter "*.encrypted"

# Analisis
Get-Content C:\Shares\.ransom_log.txt
vssadmin list shadows

# Contencion
Disable-NetAdapter -Name "Ethernet"
New-NetFirewallRule -DisplayName "BLOCK_ALL" -Direction Inbound -Action Block

# Erradicacion
Remove-Item -Path "C:\Shares\ransomware_simulator.py" -Force
Remove-ItemProperty -Path "HKLM:\...\Run" -Name "RansomService" -Force

# Recuperacion
Copy-Item -Path "C:\Shares\.backup_hidden\*" -Destination "C:\Shares\" -Recurse -Force
vssadmin list shadows
```

---

## NOTA IMPORTANTE

Este escenario es una **simulacion educativa**. En un incidente real de ransomware:

1. **NO** reinicie el sistema afectado
2. **NO** pague el rescate
3. **SI** preserv evidencia forense
4. **SI** contacte a las autoridades competentes
5. **SI** documente todo el proceso de respuesta

Los archivos originales se encuentran respaldados en:
- **Ubicacion oculta:** `C:\Shares\.backup_hidden\`
- **Copia de sombra:** Verificar con `vssadmin list shadows`
- **Backup del sistema:** Verificar con `wbadmin get versions`
