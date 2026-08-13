# Guia de Respuesta - Escenario 01: Phishing
## Banco del Sol - Curso Tectonic BHU

---

## Fase 1: Deteccion

### 1.1 Revisar logs de correo electronico
```bash
# Conectar a mail-srv desde blue-team-ws
ssh blue-team-ws@blue-team-ws

# Verificar logs de correo recientes
ssh maria.gonzalez@mail-srv "tail -100 /var/log/mail.log"

# Buscar correos con asuntos sospechosos
ssh maria.gonzalez@mail-srv "grep -i 'urgente\|seguridad\|actualizacion' /var/log/mail.log"

# Identificar el remitente de correos sospechosos
ssh maria.gonzalez@mail-srv "grep 'from=' /var/log/mail.log | tail -20"
```

### 1.2 Verificar alertas del SIEM (si esta configurado)
```bash
# Verificar logs de autenticacion
ssh maria.gonzalez@mail-srv "grep 'failed\|success' /var/log/auth.log | tail -50"

# Verificar procesos activos inusuales
ssh maria.gonzalez@mail-srv "ps aux | grep -E 'nc|netcat|python.*http'"
```

### 1.3 Analizar trafico de red
```bash
# Desde blue-team-ws, capturar trafico
sudo tcpdump -i any -nn port 25 or port 4444 or port 8080 -w /tmp/phishing_capture.pcap

# Ver conexiones activas sospechosas
ss -tlnp | grep -E "4444|8080"
```

---

## Fase 2: Analisis

### 2.1 Examinar headers del correo malicioso
```bash
# Conectar a mail-srv
ssh maria.gonzalez@mail-srv

# Ver el correo completo con headers
mail -H | tail -5
# Seleccionar el correo sospechoso con 'f <numero>'

# Buscar el remitente
grep "From:" /var/mail/maria.gonzalez
grep "Subject:" /var/mail/maria.gonzalez

# Identificar la IP del atacante
grep " Received:" /var/mail/maria.gonzalez
```

### 2.2 Identificar el IOC del archivo malicioso
```bash
# Verificar el payload descargado
find /tmp -name "*.sh" -o -name "*.zip" -ls
find /home -name "*.sh" -ls

# Calcular hash del archivo malicioso
sha256sum /tmp/.cache/credentials.txt

# Verificar contenido del archivo
cat /tmp/.cache/credentials.txt

# Buscar archivos ocultos
find / -name ".*" -type f 2>/dev/null | head -20
```

### 2.3 Verificar reverse shell activo
```bash
# Ver procesos de netcat
ps aux | grep nc
ps aux | grep netcat

# Ver conexiones de red establecidas
ss -tnp | grep ESTABLISHED
netstat -tnp | grep 4444

# Verificar si hay binarios de netcat ejecutandose
find / -name "nc" -o -name "ncat" -o -name "netcat" 2>/dev/null
```

---

## Fase 3: Contencion

### 3.1 Desconectar mail-srv de la red
```bash
# Conectar a mail-srv (si es posible)
ssh maria.gonzalez@mail-srv

# Bloquear todo el trafico de salida con iptables
sudo iptables -A OUTPUT -j DROP
sudo iptables -A INPUT -j DROP
sudo iptables -A FORWARD -j DROP

# Permitir solo SSH desde blue-team-ws
sudo iptables -I INPUT -s <IP_BLUE_TEAM> -p tcp --dport 22 -j ACCEPT
sudo iptables -I OUTPUT -d <IP_BLUE_TEAM> -p tcp --sport 22 -j ACCEPT

# Verificar reglas aplicadas
sudo iptables -L -v -n
```

### 3.2 Deshabilitar servicios comprometidos
```bash
# En mail-srv
sudo systemctl stop postfix
sudo systemctl stop dovecot

# Matar procesos de reverse shell
sudo pkill -f "nc"
sudo pkill -f "netcat"
sudo pkill -f "ncat"
```

### 3.3 Documentar el estado actual
```bash
# Capturar estado del sistema antes de cambios
ps aux > /tmp/evidencia_ps.txt
ss -tlnp > /tmp/evidencia_netstat.txt
netstat -tnp > /tmp/evidencia_conexiones.txt
last -20 > /tmp/evidencia_login.txt
cat /var/log/mail.log > /tmp/evidencia_maillog.txt
```

---

## Fase 4: Erradicacion

### 4.1 Encontrar y eliminar el reverse shell
```bash
# Buscar procesos de netcat
ps aux | grep -E "nc|netcat|ncat"
# Identificar el PID del proceso

# Matar el proceso
sudo kill -9 <PID>

# Buscar y eliminar scripts maliciosos
find / -name "reverse_shell.sh" -delete 2>/dev/null
find / -name "serve_payload.py" -delete 2>/dev/null
find / -name "credentials.txt" -path "*/.cache/*" -delete 2>/dev/null
rm -rf /tmp/.cache
```

### 4.2 Eliminar archivos maliciosos
```bash
# Buscar archivos temporales sospechosos
find /tmp -name "*.sh" -delete
find /var/tmp -name "*.sh" -delete

# Verificar y limpiar cron jobs sospechosos
crontab -l
crontab -r

# Verificar scripts de inicio
ls -la /etc/init.d/
ls -la /etc/systemd/system/
```

### 4.3 Limpiar usuario comprometido
```bash
# Cambiar contrasena del usuario afectado
sudo passwd maria.gonzalez

# Verificar que no haya claves SSH adicionales
ls -la /home/maria.gonzalez/.ssh/
cat /home/maria.gonzalez/.ssh/authorized_keys
```

---

## Fase 5: Recuperacion

### 5.1 Restaurar configuracion limpia
```bash
# Restaurar configuracion de postfix
sudo cp /etc/postfix/main.cf.bak /etc/postfix/main.cf
# O reconstruir desde cero con la configuracion segura

# Reiniciar servicios
sudo systemctl start postfix
sudo systemctl start dovecot

# Verificar que los servicios funcionan
sudo systemctl status postfix
sudo systemctl status dovecot
```

### 5.2 Verificar integridad del sistema
```bash
# Verificar archivos modificados
debsums --changed 2>/dev/null
# O manualmente
find /etc -mtime -1 -ls

# Verificar que no haya procesos sospechosos
ps aux | grep -E "nc|netcat|python.*http"
ss -tlnp | grep -E "4444|8080"

# Verificar integridad de binarios del sistema
md5sum /usr/bin/nc /usr/bin/netcat
```

### 5.3 Restablecer monitoreo
```bash
# Iniciar servicios de monitoreo
sudo systemctl start rsyslog

# Verificar que los logs estan funcionando
tail -f /var/log/mail.log &
```

---

## Fase 6: Documentacion

### 6.1 Plantilla de reporte de incidente

```
========================================
REPORTE DE INCIDENTE DE SEGURIDAD
Banco del Sol - Incidente #001
========================================

FECHA DEL INCIDENTE: [Fecha]
HORA DE DETECCION: [Hora]
HORA DE CONTENCION: [Hora]
DURACION TOTAL: [Duracion]

RESUMEN:
Ataque de phishing dirigido al servidor de correo electronico
del Banco del Sol. El atacante envio correos maliciosos que
contenian enlaces a payloads de reverse shell.

INDICADORES DE COMPROMISO (IOCs):
- IP del atacante: [IP]
- Remitente del correo: seguridad@bancodelsol.com
- Asunto del correo: [URGENTE] Actualizacion de Seguridad Requerida
- Hash del payload: [SHA256]
- Puerto de reverse shell: 4444
- Puerto del servidor HTTP: 8080

IMPACTO:
- Servidor de correo comprometido
- Credenciales de usuario potencialmente expuestas
- Posible acceso no autorizado a correos

ACCIONES TOMADAS:
1. [Fecha/Hora] Deteccion del incidente
2. [Fecha/Hora] Contencion - Desconexion del servidor
3. [Fecha/Hora] Erradicacion - Eliminacion de malware
4. [Fecha/Hora] Recuperacion - Restauracion de servicios
5. [Fecha/Hora] Verificacion de integridad

LECCIONES APRENDIDAS:
- [Leccion 1]
- [Leccion 2]
- [Leccion 3]

RECOMENDACIONES:
1. [Recomendacion 1]
2. [Recomendacion 2]
3. [Recomendacion 3]

========================================
```

---

## Fase 7: Lecciones Aprendidas

### 7.1 Puntos de mejora
- Implementar filtros de correo mas estrictos (SPF, DKIM, DMARC)
- Capacitar a empleados sobre phishing
- Implementar segmentation de red para el servidor de correo
- Monitoreo activo de logs de correo
- Politicas de contrasenas mas robustas
- Implementar soluciones anti-phishing

### 7.2 Herramientas utilizadas para deteccion
- swaks (para simular el ataque)
- tcpdump (para captura de trafico)
- grep (para analisis de logs)
- netstat/ss (para conexiones activas)
- ps (para procesos activos)
- iptables (para contencion)

### 7.3 Tiempos de respuesta
| Fase | Tiempo Objetivo | Tiempo Real |
|------|----------------|-------------|
| Deteccion | < 15 minutos | [Medir] |
| Analisis | < 30 minutos | [Medir] |
| Contencion | < 1 hora | [Medir] |
| Erradicacion | < 2 horas | [Medir] |
| Recuperacion | < 4 horas | [Medir] |
