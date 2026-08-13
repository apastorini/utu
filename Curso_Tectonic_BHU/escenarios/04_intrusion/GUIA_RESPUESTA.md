# Guia de Respuesta - Escenario 04: Intrusion y Movimiento Lateral
## Banco del Sol - Curso Tectonic BHU

---

## Fase 1: Deteccion

### 1.1 Revisar logs de acceso web
```bash
# Conectar a blue-team-ws
ssh blue-team-ws@blue-team-ws

# Verificar logs de nginx en web-srv
ssh admin@web-srv "tail -100 /var/log/nginx/banco_access.log"

# Buscar patrones de SQL Injection
ssh admin@web-srv "grep -i 'union\|select\|--\|or.*1.*1\|drop\|insert\|delete' /var/log/nginx/banco_access.log"

# Identificar IPs sospechosas
ssh admin@web-srv "awk '{print $1}' /var/log/nginx/banco_access.log | sort | uniq -c | sort -rn | head -10"

# Verificar errores en la aplicacion
ssh admin@web-srv "tail -50 /var/log/nginx/banco_error.log"
```

### 1.2 Verificar logs de PostgreSQL
```bash
# Verificar logs de PostgreSQL en db-srv
ssh admin@db-srv "tail -100 /var/log/postgresql/postgresql-*-main.log"

# Buscar consultas sospechosas
ssh admin@db-srv "grep -i 'select\|insert\|update\|delete\|drop' /var/log/postgresql/postgresql-*-main.log | tail -50"

# Verificar conexiones activas a PostgreSQL
ssh admin@db-srv "sudo -u postgres psql -c 'SELECT * FROM pg_stat_activity;'"
```

### 1.3 Verificar conexiones SSH activas
```bash
# Verificar sesiones SSH activas en todos los servidores
for host in web-srv db-srv core-bank; do
  echo "=== $host ==="
  ssh admin@$host "who; last -10" 2>/dev/null
done

# Verificar autenticaciones SSH fallidas
ssh admin@db-srv "grep 'Failed' /var/log/auth.log | tail -20"
ssh admin@db-srv "grep 'Accepted' /var/log/auth.log | tail -20"
```

---

## Fase 2: Analisis

### 2.1 Identificar el endpoint vulnerable
```bash
# Verificar la aplicacion Flask
ssh admin@web-srv "curl -s 'http://localhost:5000/buscar?cedula=1'"

# Probar SQL Injection basica
ssh admin@web-srv "curl -s \"http://localhost:5000/buscar?cedula=1' OR '1'='1\""

# Verificar el codigo fuente
ssh admin@web-srv "cat /opt/banco_web/app.py | grep -A5 'query'"
```

### 2.2 Determinar que credenciales fueron extraidas
```bash
# Verificar el archivo de configuracion de la aplicacion
ssh admin@web-srv "cat /opt/banco_web/app.py | grep -i 'password\|DB_'"

# Verificar si hay respuestas HTTP con datos de clientes
ssh admin@web-srv "grep 'cedula\|nombre\|saldo' /var/log/nginx/banco_access.log"

# Verificar la base de datos para ver que datos estan expuestos
ssh admin@db-srv "sudo -u postgres psql -d banco_del_sol -c 'SELECT * FROM clientes LIMIT 5;'"
```

### 2.3 Rastrear el camino del ataque
```bash
# Verificar si hubo movimiento lateral
ssh admin@db-srv "grep 'Accepted' /var/log/auth.log"
ssh admin@core-bank "grep 'Accepted' /var/log/auth.log"

# Verificar archivos modificados
ssh admin@core-bank "find / -mtime -1 -type f 2>/dev/null | head -20"
ssh admin@core-bank "cat /home/admin/flag.txt"

# Verificar procesos sospechosos
ssh admin@db-srv "ps aux | grep -E 'python|nc|netcat'"
```

---

## Fase 3: Contencion

### 3.1 Bloquear IP del atacante
```bash
# Identificar la IP del atacante
ATTACKER_IP=$(ssh admin@web-srv "awk '{print $1}' /var/log/nginx/banco_access.log | sort -u | grep -v '127.0.0.1' | head -1")
echo "IP del atacante: $ATTACKER_IP"

# Bloquear IP en web-srv
ssh admin@web-srv "sudo iptables -A INPUT -s $ATTACKER_IP -j DROP"
ssh admin@web-srv "sudo iptables -L -v -n"

# Bloquear IP en db-srv
ssh admin@db-srv "sudo iptables -A INPUT -s $ATTACKER_IP -j DROP"

# Bloquear IP en core-bank
ssh admin@core-bank "sudo iptables -A INPUT -s $ATTACKER_IP -j DROP"
```

### 3.2 Revocar credenciales comprometidas
```bash
# Cambiar contrasena de PostgreSQL
ssh admin@db-srv "sudo -u postgres psql -c \"ALTER USER dbadmin PASSWORD 'NuevaContrasenaSegura2026!';\""
ssh admin@db-srv "sudo -u postgres psql -c \"ALTER USER admin PASSWORD 'NuevaContrasenaAdmin2026!';\""

# Cambiar contrasena del usuario admin
ssh admin@db-srv "echo 'admin:NuevaContrasenaAdmin2026!' | sudo chpasswd"
ssh admin@core-bank "echo 'admin:NuevaContrasenaCore2026!' | sudo chpasswd"

# Verificar que las credenciales antiguas ya no funcionan
ssh admin@web-srv "curl -s 'http://localhost:5000/buscar?cedula=1'"  # Deberia fallar
```

### 3.3 Deshabilitar el endpoint vulnerable
```bash
# Detener la aplicacion Flask
ssh admin@web-srv "pkill -f 'python3 app.py'"

# Deshabilitar el sitio en nginx
ssh admin@web-srv "sudo rm -f /etc/nginx/sites-enabled/banco"
ssh admin@web-srv "sudo systemctl restart nginx"

# Verificar que el servidor no responde
ssh admin@web-srv "curl -s -o /dev/null -w '%{http_code}' http://localhost:5000/"
```

---

## Fase 4: Erradicacion

### 4.1 Eliminar artefactos del atacante
```bash
# Buscar archivos dejados por el atacante
ssh admin@core-bank "find / -name '*.sh' -o -name '*backdoor*' -o -name '*reverse*' 2>/dev/null"

# Verificar y eliminar archivos sospechosos
ssh admin@core-bank "ls -la /home/admin/"
ssh admin@core-bank "cat /home/admin/flag.txt"
ssh admin@core-bank "rm -f /home/admin/flag.txt"

# Verificar cron jobs sospechosos
ssh admin@core-bank "crontab -l"
ssh admin@db-srv "crontab -l"
```

### 4.2 Verificar integridad del sistema
```bash
# Verificar archivos modificados recientemente
for host in web-srv db-srv core-bank; do
  echo "=== $host ==="
  ssh admin@$host "find /etc -mtime -1 -ls 2>/dev/null"
done

# Verificar procesos activos
ssh admin@web-srv "ps aux | grep -E 'python|nc|netcat|ncat'"
ssh admin@db-srv "ps aux | grep -E 'python|nc|netcat|ncat'"
```

---

## Fase 5: Correccion de Vulnerabilidades

### 5.1 Corregir SQL Injection en Flask
```bash
# Crear version corregida de la aplicacion
ssh admin@web-srv "cat > /opt/banco_web/app_fixed.py << 'PYTHON_EOF'
#!/usr/bin/env python3
from flask import Flask, request, render_template_string
import psycopg2

app = Flask(__name__)

DB_HOST = \"{{ hostvars['db-srv']['ansible_default_ipv4']['address'] | default('10.0.0.4') }}\"
DB_NAME = \"banco_del_sol\"
DB_USER = \"dbadmin\"
DB_PASSWORD = \"NuevaContrasenaSegura2026!\"

def get_db():
    return psycopg2.connect(
        host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD
    )

@app.route('/buscar')
def buscar():
    cedula = request.args.get('cedula', '')
    # CORREGIDO: Consulta parametrizada
    query = \"SELECT * FROM clientes WHERE cedula = %s\"
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute(query, (cedula,))  # Parametros separados
        results = cur.fetchall()
        cur.close()
        conn.close()
        # ... renderizar resultados
    except Exception as e:
        return f'Error: {str(e)}'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
PYTHON_EOF"

# Iniciar la version corregida
ssh admin@web-srv "nohup python3 /opt/banco_web/app_fixed.py &>/dev/null &"
```

### 5.2 Implementar WAF basico
```bash
# Instalar y configurar ModSecurity (opcional)
ssh admin@web-srv "sudo apt-get install -y libapache2-mod-security2"

# Configurar reglas basicas de proteccion
ssh admin@web-srv "sudo cp /etc/modsecurity/modsecurity.conf-recommended /etc/modsecurity/modsecurity.conf"
ssh admin@web-srv "sudo sed -i 's/SecRuleEngine DetectionOnly/SecRuleEngine On/' /etc/modsecurity/modsecurity.conf"
```

---

## Fase 6: Reporte

### 6.1 Plantilla de reporte de incidente

```
========================================
REPORTE DE INCIDENTE DE SEGURIDAD
Banco del Sol - Incidente #004
========================================

FECHA DEL INCIDENTE: [Fecha]
HORA DE DETECCION: [Hora]
HORA DE CONTENCION: [Hora]
DURACION TOTAL: [Duracion]

RESUMEN:
Ataque de intrusion y movimiento lateral. El atacante exploto una
vulnerabilidad SQL Injection en la aplicacion web Flask, extraeo
credenciales de la base de datos PostgreSQL, accedio via SSH a
db-srv y core-bank, y planto una bandera de prueba.

VULNERABILIDAD EXPLOTADA:
- SQL Injection en endpoint /buscar
- Credenciales en texto plano en configuracion
- Sin validacion de entrada

IMPACTO:
- Datos de clientes expuestos (10 registros)
- Acceso no autorizado a 3 servidores
- Credenciales comprometidas

INDICADORES DE COMPROMISO:
- IP del atacante: [IP]
- Endpoint vulnerable: /buscar?cedula=
- Credenciales comprometidas: dbadmin, admin

ACCIONES TOMADAS:
1. [Fecha/Hora] Deteccion en logs de nginx
2. [Fecha/Hora] Bloqueo de IP del atacante
3. [Fecha/Hora] Revocacion de credenciales
4. [Fecha/Hora] Correccion de vulnerabilidad
5. [Fecha/Hora] Verificacion de integridad

LECCIONES APRENDIDAS:
- Implementar consultas parametrizadas
- No almacenar credenciales en texto plano
- Implementar WAF
- Monitorear trafico entre servidores

========================================
```

### 6.2 Timeline del ataque

| Hora | Fase | Descripcion |
|------|------|-------------|
| [H1] | Reconocimiento | Escaneo nmap del servidor web |
| [H2] | Explotacion | SQL Injection via sqlmap |
| [H3] | Exfiltracion | Extraccion de credenciales |
| [H4] | Movimiento Lateral | SSH a db-srv |
| [H5] | Movimiento Lateral | SSH a core-bank |
| [H6] | Planta | Flag file en core-bank |
| [H7] | Deteccion | Blue team detecta actividad |
| [H8] | Contencion | Bloqueo IP y revocacion |

### 6.3 Herramientas utilizadas
- sqlmap (para SQL Injection)
- nmap (para reconocimiento)
- sshpass (para SSH automatizado)
- curl (para pruebas HTTP)
- iptables (para contencion)
- grep/awk (para analisis de logs)

### 6.4 Tiempos de respuesta
| Fase | Tiempo Objetivo | Tiempo Real |
|------|----------------|-------------|
| Deteccion | < 30 minutos | [Medir] |
| Analisis | < 1 hora | [Medir] |
| Contencion | < 2 horas | [Medir] |
| Erradicacion | < 4 horas | [Medir] |
| Correccion | < 8 horas | [Medir] |
| Reporte | < 24 horas | [Medir] |
