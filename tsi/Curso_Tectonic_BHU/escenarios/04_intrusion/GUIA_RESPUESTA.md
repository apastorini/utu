# GUIA DE RESPUESTA AZUL - Escenario 04: Intrusion y Movimiento Lateral

**Banco del Sol - Tectonic Cyber Range**

---

## Resumen del Escenario

Este escenario simula un ataque completo contra la infraestructura de Banco del Sol, comenzando con la explotacion de una vulnerabilidad de inyeccion SQL en la aplicacion web bancaria y avanzando hasta el escalamiento de privilegios en el dominio Active Directory. Los estudiantes actuan como equipo de respuesta azul y deben detectar, analizar, contener y erradicar la intrusion.

**Duracion estimada:** 3 horas
**Nivel:** Avanzado
**Sistemas afectados:** webserver, database, fileserver, domaincontroller

---

## FASE 1: DETECCION

### 1.1 Fuentes de Informacion Iniciales

Los primeros indicadores de compromiso se encuentran en los logs del webserver. Revisar en este orden:

**Archivos criticos en el webserver:**
- `/var/log/apache2/access.log` - Logs de acceso HTTP
- `/var/log/apache2/error.log` - Errores de Apache/PHP
- `/var/www/html/banco_del_sol/logs/access.log` - Logs de la aplicacion
- `/var/www/html/banco_del_sol/logs/sql_errors.log` - Errores SQL
- `/var/www/html/banco_del_sol/logs/websell_activity.log` - Actividad del webshell

### 1.2 Deteccion de Patrones de SQLi en Apache

Buscar los siguientes patrones en `/var/log/apache2/access.log`:

```
# Patrones de UNION-based SQLi
UNION.*SELECT
UNION%20SELECT

# Patrones de bypass de autenticacion
OR.*'1'='1
OR.*1=1

# Patrones de extraccion de metadata
INFORMATION_SCHEMA
TABLE_NAME.*COLUMN_NAME

# Patrones de extraccion de datos
SELECT.*FROM.*customer_accounts
SELECT.*FROM.*system_users
```

**Comando recomendado para busqueda:**
```bash
grep -iE "UNION.*SELECT|OR.*1.*=.*1|INFORMATION_SCHEMA|SELECT.*FROM" /var/log/apache2/access.log
```

### 1.3 Deteccion de Errores SQL

En `/var/log/apache2/error.log`:
- Errores de sintaxis SQL
- Tablas que no existen (indicando intento de enumeracion)
- Excepciones PDO que revelan estructura de base de datos

### 1.4 Deteccion de Webshell

Verificar archivos en `/var/www/html/banco_del_sol/uploads/`:
- Buscar archivos PHP inusuales en directorios de uploads
- Comparar con la lista de archivos que deberian existir
- El webshell se llama `shell.php` y tiene un patron de comportamiento sospechoso

```bash
ls -la /var/www/html/banco_del_sol/uploads/
find /var/www/html -name "*.php" -newer /var/www/html/banco_del_sol/public/index.php
```

### 1.5 Indicadores de Compromiso (IOCs) - Fase 1

| IOC | Descripcion | Ubicacion |
|-----|-------------|-----------|
| `10.10.1.100` | IP del atacante | Logs de Apache |
| `shell.php` | Webshell | `/var/www/html/banco_del_sol/uploads/` |
| `' OR '1'='1` | Patron SQLi | access.log |
| `UNION SELECT` | SQLi basado en union | access.log |
| `INFORMATION_SCHEMA` | Extraccion de metadata | access.log |

---

## FASE 2: ANALISIS

### 2.1 Reconstruccion de la Cadena de Ataque

La cadena de ataque completa consta de 4 fases. Documentar el timeline:

**Timeline estimado:**
- T+0min: Exploracion inicial del webserver
- T+2min: Deteccion de formulario de login vulnerable
- T+5min: Intentos de SQLi en formulario de login
- T+10min: SQLi exitoso con UNION-based extraction
- T+15min: Obtencion de credenciales de base de datos
- T+20min: Colocacion de webshell en directorio uploads
- T+25min: Establecimiento de reverse shell
- T+30min: Acceso SSH a database con credenciales robadas
- T+35min: Acceso SMB a fileserver
- T+40min: Lectura de archivo de credenciales en fileserver
- T+45min: Acceso a domaincontroller con credenciales de administrator
- T+50min: Creacion de cuenta backdoor
- T+55min: Acceso a SYSVOL/NETLOGON

### 2.2 Analisis del Webserver

**Logs de acceso web - Que buscar:**

1. **Patron de escaneo inicial:** Multiples requests a paths comunes de administracion
2. **SQLi en login:** POST requests a `/login.php` con caracteres especiales
3. **SQLi en busqueda:** GET requests a `/search.php` con patrones UNION SELECT
4. **Acceso al webshell:** GET/POST a `/uploads/shell.php`

**Ejemplo de log con SQLi:**
```
10.10.1.100 - - [2024-06-15 10:30:15] "POST /login.php HTTP/1.1" 200 2905
"username=admin'%20UNION%20SELECT%20username,password,email,5%20FROM%20system_users--%20&password="
```

**Archivos de la aplicacion a revisar:**
- `/var/www/html/banco_del_sol/config/database.php` - Credenciales hardcodeadas
- `/var/www/html/banco_del_sol/config/db_connect.php` - Conexion a BD
- `/var/www/html/banco_del_sol/public/login.php` - Script vulnerable

### 2.3 Analisis del Database Server

**Logs de MySQL:**

1. **General Query Log** (`/var/log/mysql/general.log`):
   - Buscar queries con `UNION SELECT`
   - Buscar acceso a `INFORMATION_SCHEMA`
   - Buscar queries desde IP `10.10.1.10` (webserver)
   - Buscar acceso a tablas `system_users` y `mysql.user`

2. **Error Log** (`/var/log/mysql/error.log`):
   - Errores de sintaxis SQL
   - Intentos de acceso no autorizado

3. **Auth Log** (`/var/log/auth.log`):
   - Eventos SSH desde `10.10.1.10`
   - Login exitoso con usuario `bds_webapp`

```bash
# Buscar queries desde webserver
grep "10.10.1.10" /var/log/mysql/general.log

# Buscar queries con patrones sospechosos
grep -iE "UNION|INFORMATION_SCHEMA|mysql.user" /var/log/mysql/general.log
```

### 2.4 Analisis del Fileserver

**Windows Event Logs a revisar:**

1. **Security Log - Event ID 4624 (Logon exitoso):**
   - Tipo 3 (Network): Conexiones SMB/RDP
   - Origen: `10.10.1.10` (webserver)
   - Usuario: `svc_fileserver`

2. **Security Log - Event ID 5140 (Acceso a shares):**
   - Share: `\\*\IT` - Acceso al directorio de documentacion tecnica
   - Archivo: `config_servidores.txt` - Contiene credenciales

3. **Security Log - Event ID 5145 (Acceso a archivos):**
   - Acceso a archivos especificos en comparticiones SMB

```powershell
# Buscar logons desde IP sospechosa
Get-WinEvent -FilterXPath "*[System[EventID=4624]]" -MaxEvents 1000 |
    Where-Object { $_.Properties[18].Value -eq "10.10.1.10" }

# Buscar accesos a shares
Get-WinEvent -FilterXPath "*[System[EventID=5140]]" -MaxEvents 500
```

**Archivo sospechoso en fileserver:**
- `C:\Compartidos\IT\config_servidores.txt` - Contiene credenciales de todos los servidores

### 2.5 Analisis del Domain Controller

**Windows Event Logs a revisar:**

1. **Event ID 4624 (Logon):**
   - Origen: `10.10.2.20` (fileserver)
   - Usuario: `Administrator`
   - Tipo: 3 (Network)

2. **Event ID 4672 (Privilegios especiales):**
   - Usuario: `Administrator`
   - Indica que se usaron privilegios elevados

3. **Event ID 4720 (Usuario creado):**
   - Nuevo usuario: `backup_admin`
   - Creado por: `Administrator`

4. **Event ID 4728 (Miembro agregado a grupo):**
   - Usuario: `backup_admin`
   - Grupo: `Domain Admins`

5. **Event ID 5140/5145 (Acceso a SYSVOL/NETLOGON):**
   - Acceso desde `10.10.2.20`
   - Acceso a archivos de politicas de grupo

```powershell
# Buscar logons desde fileserver
Get-WinEvent -FilterXPath "*[System[EventID=4624]]" -MaxEvents 1000 |
    Where-Object { $_.Properties[18].Value -eq "10.10.2.20" }

# Buscar creacion de usuarios
Get-WinEvent -FilterXPath "*[System[EventID=4720]]" -MaxEvents 100

# Buscar cambios en grupos de seguridad
Get-WinEvent -FilterXPath "*[System[EventID=4728 or EventID=4732]]" -MaxEvents 100
```

### 2.6 Analisis de Red

**Conexiones sospechosas a buscar:**

| Origen | Destino | Puerto | Protocolo | Descripcion |
|--------|---------|--------|-----------|-------------|
| 10.10.1.100 | 10.10.1.10 | 80/443 | HTTP/HTTPS | Ataque web inicial |
| 10.10.1.10 | 10.10.1.100 | 4444 | TCP | Reverse shell |
| 10.10.1.10 | 10.10.2.30 | 3306 | MySQL | Acceso a BD con credenciales robadas |
| 10.10.1.10 | 10.10.2.20 | 445 | SMB | Acceso a fileserver |
| 10.10.1.10 | 10.10.2.10 | 22 | SSH | Acceso a mailserver |
| 10.10.2.20 | 10.10.0.10 | 445 | SMB | Acceso a DC con credenciales robadas |
| 10.10.2.20 | 10.10.0.10 | 3389 | RDP | Acceso remoto a DC |

---

## FASE 3: CONTENCION

### 3.1 Aislamiento del Webserver

**Inmediatamente despues de confirmar el compromise:**

1. **Bloquear trafico entrante al webserver:**
```bash
# En el webserver
sudo ufw deny in
sudo ufw allow out
sudo ufw allow from 10.10.0.0/24  # Permitir solo desde management
```

2. **Bloquear trafico saliente hacia el atacante:**
```bash
# Regla de firewall para bloquear IP del atacante
sudo iptables -A OUTPUT -d 10.10.1.100 -j DROP
sudo iptables -A INPUT -s 10.10.1.100 -j DROP
```

3. **No apagar el servidor** - Preservar evidencia en memoria

### 3.2 Revocacion de Credenciales

**Credenciales comprometidas que deben ser rotadas inmediatamente:**

1. **Credenciales de base de datos:**
```bash
# En el database server
mysql -u root -p
ALTER USER 'bds_webapp'@'10.10.1.10' IDENTIFIED BY 'Nueva_Contrasena_Segura_2024!';
FLUSH PRIVILEGES;
```

2. **Credenciales de servicio en Active Directory:**
```powershell
# En el domaincontroller
Set-ADAccountPassword -Identity svc_fileserver -NewPassword (ConvertTo-SecureString "Nueva_Contrasena_Segura_2024!" -AsPlainText -Force)
Set-ADAccountPassword -Identity svc_webapp -NewPassword (ConvertTo-SecureString "Nueva_Contrasena_Segura_2024!" -AsPlainText -Force)
```

3. **Credenciales de administrator:**
```powershell
# En el domaincontroller
Set-ADAccountPassword -Identity Administrator -ResetPassword -NewPassword (ConvertTo-SecureString "Nueva_Contrasena_Admin_2024!" -AsPlainText -Force)
```

4. **Credenciales de usuario en base de datos:**
```sql
-- En MySQL
UPDATE system_users SET password = 'Nueva_Contrasena_Segura_2024!' WHERE username = 'admin';
UPDATE customer_accounts SET password = 'Nueva_Contrasena_Segura_2024!';
```

### 3.3 Bloqueo de IPs del Atacante

**En todos los firewall y dispositivos de red:**

1. **Webserver:**
```bash
sudo iptables -A INPUT -s 10.10.1.100 -j DROP
sudo iptables -A OUTPUT -d 10.10.1.100 -j DROP
```

2. **Database:**
```bash
sudo iptables -A INPUT -s 10.10.1.100 -j DROP
```

3. **Fileserver:**
```powershell
New-NetFirewallRule -DisplayName "Block Attacker IP" -Direction Inbound -RemoteAddress 10.10.1.100 -Action Block
New-NetFirewallRule -DisplayName "Block Attacker IP Out" -Direction Outbound -RemoteAddress 10.10.1.100 -Action Block
```

4. **Domain Controller:**
```powershell
New-NetFirewallRule -DisplayName "Block Attacker IP" -Direction Inbound -RemoteAddress 10.10.1.100 -Action Block
```

### 3.4 Cierre del Punto de Apoyo

1. **Eliminar el webshell:**
```bash
sudo rm /var/www/html/banco_del_sol/uploads/shell.php
```

2. **Suspender la cuenta de servicio comprometida:**
```bash
# En database
mysql -u root -p -e "ALTER USER 'bds_webapp'@'10.10.1.10' ACCOUNT LOCK;"
```

3. **Cerrar sesiones activas del atacante:**
```bash
# En webserver
sudo pkill -u www-data
sudo killall -9 python3  # Si hay procesos sospechosos
```

---

## FASE 4: ERRADICACION

### 4.1 Eliminacion del Webshell

```bash
# En webserver
sudo rm /var/www/html/banco_del_sol/uploads/shell.php
sudo rm /tmp/.cache_backup
```

Verificar que no hay otros archivos maliciosos:
```bash
find /var/www/html -name "*.php" -mtime -1 -ls
find /tmp -name ".*" -mtime -1 -ls
```

### 4.2 Parcheo de la Vulnerabilidad

**Corregir la inyeccion SQL en el formulario de login:**

1. **Reemplazar el script vulnerable con version segura:**

```php
<?php
// login.php - VERSION SEGURA
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    header('Location: index.php');
    exit();
}

$username = $_POST['username'];
$password = $_POST['password'];

$host = '10.10.2.30';
$dbname = 'banco_del_sol';
$user = 'bds_webapp';
$pass = 'Nueva_Contrasena_Segura_2024!';

try {
    $pdo = new PDO("mysql:host=$host;dbname=$dbname", $user, $pass);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    // CONSULTA SEGURA: Usar prepared statements
    $stmt = $pdo->prepare("SELECT * FROM customer_accounts WHERE username = :username AND password = :password");
    $stmt->bindParam(':username', $username);
    $stmt->bindParam(':password', $password);
    $stmt->execute();
    $result = $stmt->fetch(PDO::FETCH_ASSOC);

    if ($result) {
        // Login exitoso
        session_start();
        $_SESSION['user'] = $result;
        header('Location: dashboard.php');
        exit();
    } else {
        header('Location: index.php?error=1');
        exit();
    }
} catch(PDOException $e) {
    error_log("Login error: " . $e->getMessage());
    echo "Error de autenticacion. Contacte al administrador.";
}
?>
```

2. **Corregir el script de busqueda:**

```php
<?php
// search.php - VERSION SEGURA
include_once '../config/db_connect.php';

$results = '';
$search_term = '';

if (isset($_GET['q'])) {
    $search_term = $_GET['q'];

    // CONSULTA SEGURA: Usar prepared statements
    $sql = "SELECT id, nombre, email, numero_cuenta, saldo
            FROM customer_accounts
            WHERE nombre LIKE :search1
            OR numero_cuenta LIKE :search2";

    $stmt = $pdo->prepare($sql);
    $searchPattern = "%{$search_term}%";
    $stmt->bindParam(':search1', $searchPattern);
    $stmt->bindParam(':search2', $searchPattern);
    $stmt->execute();
    $rows = $stmt->fetchAll(PDO::FETCH_ASSOC);

    // ... resto del codigo para mostrar resultados
}
?>
```

3. **Remover credenciales hardcodeadas:**
   - Mover credenciales a variables de entorno
   - Usar un vault para gestion de secretos

### 4.3 Eliminacion de Cuentas Backdoor

```powershell
# En domaincontroller
Remove-ADUser -Identity "backup_admin" -Confirm:$false
```

Verificar que no hay cuentas sospechosas:
```powershell
Get-ADUser -Filter * | Select-Object Name, Enabled, LastLogonDate | Sort-Object LastLogonDate -Descending
```

### 4.4 Limpieza de Archivos Temporales

```bash
# En webserver
sudo find /tmp -name ".*" -mtime -1 -delete
sudo find /var/www/html -name "*.php.tmp" -delete

# En database
sudo find /tmp -name "*.sql" -mtime -1 -delete
```

---

## FASE 5: RECUPERACION

### 5.1 Restauracion de Servicios

1. **Webserver:**
```bash
sudo systemctl restart apache2
sudo systemctl status apache2
```

2. **Database:**
```bash
sudo systemctl restart mysql
sudo systemctl status mysql
```

3. **Fileserver:**
```powershell
Restart-Service -Name "LanmanServer"
Restart-Service -Name "LanmanWorkstation"
```

4. **Domain Controller:**
```powershell
Restart-Service -Name "NTDS"
Restart-Service -Name "DNS"
Restart-Service -Name "ADWS"
```

### 5.2 Verificacion de Integridad

**Webserver:**
```bash
# Verificar integridad de archivos del sistema
debsums -c apache2 php*

# Verificar que no hay archivos modificados
find /var/www/html -newer /var/www/html/banco_del_sol/public/index.php -ls

# Verificar procesos
ps aux | grep -E "python|php" | grep -v grep
```

**Database:**
```bash
# Verificar integridad de tablas
mysqlcheck -u root -p banco_del_sol

# Verificar usuarios
mysql -u root -p -e "SELECT user, host FROM mysql.user;"
```

**Fileserver:**
```powershell
# Verificar integridad de shares
Get-SmbShare | Select-Object Name, Path, CurrentUsers

# Verificar archivos criticos
Test-Path "C:\Compartidos\IT\config_servidores.txt"
```

**Domain Controller:**
```powershell
# Verificar integridad de AD
dcdiag /v

# Verificar que SYSVOL esta sincronizado
repadmin /replsummary
```

### 5.3 Monitoreo Post-Incidente

Implementar monitoreo intensivo durante 72 horas:

1. **Webserver:**
```bash
# Monitoreo en tiempo real de logs
tail -f /var/log/apache2/access.log | grep -iE "UNION|SELECT|OR.*1.*=.*1"
```

2. **Database:**
```bash
# Monitoreo de queries
tail -f /var/log/mysql/general.log | grep -iE "UNION|SELECT.*FROM.*mysql"
```

3. **Domain Controller:**
```powershell
# Monitoreo de eventos de seguridad
Get-WinEvent -FilterXPath "*[System[EventID=4720 or EventID=4728 or EventID=4732]]" -MaxEvents 10 -Wait -Timeout 30
```

---

## FASE 6: LECCIONES APRENDIDAS

### 6.1 Fortalecimiento de Aplicaciones Web

**Recomendaciones inmediatas:**

1. **Prepared Statements:** Todas las queries SQL deben usar prepared statements
2. **Validacion de entrada:** Implementar validacion estricta de todos los inputs
3. **WAF (Web Application Firewall):** Implementar ModSecurity o similar
4. **Actualizaciones:** Mantener PHP y dependencias actualizadas
5. **Pruebas de seguridad:** Implementar pruebas de penetracion regulares

**Politica de desarrollo segura:**
- Revision de codigo obligatoria para cambios de seguridad
- Pruebas SAST (Static Application Security Testing) en CI/CD
- Pruebas DAST (Dynamic Application Security Testing) en staging

### 6.2 Segmentacion de Red

**Problemas identificados:**

1. **DMZ a Internal sin restricciones:** El webserver pudo acceder a database y fileserver sin problemas
2. **Credenciales compartidas:** Las mismas credenciales se usaron en multiples sistemas
3. **Monitoreo insuficiente:** No se detecto el movimiento lateral en tiempo real

**Mejoras recomendadas:**

1. **Segmentacion mas estricta:**
   - DMZ: Solo servicios expuestos
   - Internal: Servidores internos con acceso restringido
   - Management: Solo administradores

2. **Credenciales unicas por servicio:**
   - Cada servicio debe tener su propia cuenta de servicio
   - No reutilizar credenciales entre sistemas

3. **Monitoreo de red:**
   - Implementar IDS/IPS en puntos clave
   - Monitoreo de flujo de red (NetFlow)
   - Alertas por conexiones inusuales entre zonas

### 6.3 Gestion de Credenciales

**Problemas encontrados:**

1. **Credenciales hardcodeadas:** Las credenciales de la BD estaban en el codigo PHP
2. **Archivo de credenciales en fileserver:** El archivo `config_servidores.txt` contenia todas las credenciales
3. **Cuentas de servicio con permisos excesivos:** La cuenta de servicio tenia acceso a multiples recursos

**Mejoras recomendadas:**

1. **Vault de secretos:** Usar HashiCorp Vault o Azure Key Vault
2. **Credenciales rotativas:** Implementar rotacion automatica de contrasenas
3. **Least privilege:** Cada cuenta debe tener solo los permisos necesarios
4. **Auditoria de credenciales:** Revision trimestral de todas las cuentas de servicio

### 6.4 Deteccion y Respuesta

**Capacidades de deteccion a mejorar:**

1. **SIEM:** Implementar correlacion de eventos entre sistemas
2. **EDR:** Endpoint Detection and Response en todos los servidores
3. **NDR:** Network Detection and Response para monitoreo de red
4. **Playbooks:** Documentar procedimientos de respuesta a incidentes

**Tiempo de respuesta objetivo:**
- Deteccion: < 15 minutos
- Contencion: < 30 minutos
- Erradicacion: < 2 horas
- Recuperacion: < 4 horas

### 6.5 Plan de Accion

| Accion | Responsable | Fecha Limite | Prioridad |
|--------|-------------|--------------|-----------|
| Implementar prepared statements en PHP | Desarrollo | 1 semana | Alta |
| Rotar todas las credenciales | Seguridad | 24 horas | Critica |
| Implementar WAF | Infraestructura | 2 semanas | Alta |
| Revisar segmentacion de red | Red | 1 mes | Media |
| Implementar SIEM avanzado | Seguridad | 2 meses | Alta |
| Capacitacion en desarrollo seguro | RRHH | 1 mes | Media |
| Prueba de penetracion anual | Seguridad | 3 meses | Alta |

---

## Comandos de Referencia Rapida

### Deteccion
```bash
# Buscar SQLi en logs de Apache
grep -iE "UNION.*SELECT|OR.*1.*=.*1|INFORMATION_SCHEMA" /var/log/apache2/access.log

# Buscar webshell
find /var/www/html -name "*.php" -newer /var/www/html/banco_del_sol/public/index.php

# Buscar conexiones sospechosas en MySQL
grep "10.10.1.10" /var/log/mysql/general.log
```

### Contencion
```bash
# Bloquear IP del atacante
sudo iptables -A INPUT -s 10.10.1.100 -j DROP
sudo iptables -A OUTPUT -d 10.10.1.100 -j DROP

# Eliminar webshell
sudo rm /var/www/html/banco_del_sol/uploads/shell.php

# Cerrar sesiones del atacante
sudo pkill -u www-data
```

### Erradicacion
```bash
# Cambiar credenciales de BD
mysql -u root -p -e "ALTER USER 'bds_webapp'@'10.10.1.10' IDENTIFIED BY 'Nueva_Contrasena!';"

# Reiniciar servicios
sudo systemctl restart apache2
sudo systemctl restart mysql
```

### Verificacion
```bash
# Verificar integridad de archivos
find /var/www/html -mtime -1 -ls

# Verificar procesos sospechosos
ps aux | grep -E "python|php" | grep -v grep

# Verificar conexiones de red
netstat -tlnp | grep -E "4444|3306|445"
```

---

## Notas para el Evaluador

### Criterios de Evaluacion

1. **Deteccion (25 puntos):**
   - Identificar patrones SQLi en logs (5 pts)
   - Detectar webshell (5 pts)
   - Detectar movimiento lateral (10 pts)
   - Detectar escalamiento de privilegios (5 pts)

2. **Analisis (25 puntos):**
   - Reconstruir cadena de ataque (10 pts)
   - Identificar credenciales comprometidas (5 pts)
   - Mapear sistemas afectados (5 pts)
   - Correlacionar eventos entre sistemas (5 pts)

3. **Contencion (25 puntos):**
   - Aislar webserver correctamente (10 pts)
   - Revocar credenciales comprometidas (10 pts)
   - Bloquear IPs del atacante (5 pts)

4. **Erradicacion y Recuperacion (25 puntos):**
   - Eliminar webshell (5 pts)
   - Parchear vulnerabilidad SQLi (10 pts)
   - Restablecer todas las credenciales (5 pts)
   - Verificar integridad de sistemas (5 pts)

### Evidencia Esperada

Los estudiantes deben documentar:
1. Timeline completo del ataque
2. Todos los IOCs encontrados
3. Sistemas afectados y nivel de compromiso
4. Acciones de contencion tomadas
5. Credenciales rotadas
6. Verificacion de integridad
7. Recomendaciones de mejora

### Tiempo Limite

El escenario tiene un limite de 3 horas. Despues de este tiempo, se evalua la evidencia recolectada hasta ese momento.
