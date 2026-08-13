# Guia de Respuesta - Escenario 03: DDoS
## Banco del Sol - Curso Tectonic BHU

---

## Fase 1: Deteccion

### 1.1 Verificar disponibilidad del servidor web
```bash
# Conectar a blue-team-ws
ssh blue-team-ws@blue-team-ws

# Intentar acceder al servidor web
curl -v http://web-srv
curl -s -o /dev/null -w "HTTP Code: %{http_code}\nTime: %{time_total}s\n" http://web-srv

# Verificar conectividad basica
ping -c 5 web-srv
```

### 1.2 Verificar monitoreo de red
```bash
# Revisar logs de monitoreo
cat /var/log/monitor_ddos.log | tail -50

# Verificar trafico de red actual
cat /sys/class/net/eth0/statistics/rx_bytes
cat /sys/class/net/eth0/statistics/tx_bytes

# Verificar conexiones activas
ss -s
ss -ant | head -20
```

### 1.3 Capturar trafico de red
```bash
# Iniciar captura de trafico
sudo tcpdump -i any -nn port 80 -w /tmp/ddos_capture.pcap &
TCPDUMP_PID=$!

# Esperar 30 segundos de captura
sleep 30

# Detener captura
kill $TCPDUMP_PID

# Analizar paquetes capturados
tcpdump -r /tmp/ddos_capture.pcap | head -50
tcpdump -r /tmp/ddos_capture.pcap | grep "SYN" | wc -l
```

---

## Fase 2: Analisis

### 2.1 Analizar patron de ataque SYN flood
```bash
# Verificar conexiones SYN-RECV (indicativo de SYN flood)
ss -ant | grep SYN-RECV | wc -l
ss -ant | grep SYN-RECV | head -20

# Verificar estados de conexion
ss -ant | awk '{print $1}' | sort | uniq -c | sort -rn

# Analizar captura de trafico
tcpdump -r /tmp/ddos_capture.pcap -nn | grep "S" | head -30

# Verificar si hay un patron de IPs repetidas
tcpdump -r /tmp/ddos_capture.pcap -nn | awk '{print $3}' | cut -d. -f1-4 | sort | uniq -c | sort -rn | head -10
```

### 2.2 Analizar patron de ataque HTTP flood
```bash
# Verificar conexiones HTTP activas
ss -ant | grep :80 | wc -l

# Verificar logs de nginx
cat /var/log/nginx/banco_access.log | tail -50
cat /var/log/nginx/banco_error.log | tail -50

# Verificar si hay muchas conexiones desde una IP
cat /var/log/nginx/banco_access.log | awk '{print $1}' | sort | uniq -c | sort -rn | head -10
```

### 2.3 Verificar estado del servidor
```bash
# Verificar uso de CPU y memoria
top -bn1 | head -20

# Verificar procesos de nginx
ps aux | grep nginx

# Verificar conexiones activas
netstat -ant | head -30

# Verificar si el servidor esta respondiendo
curl -s -o /dev/null -w "HTTP Code: %{http_code}\n" http://web-srv
```

---

## Fase 3: Mitigacion

### 3.1 Implementar reglas iptables anti-DDoS
```bash
# Conectar a web-srv
ssh admin@web-srv

# Implementar reglas de proteccion SYN flood
sudo iptables -F
sudo iptables -X

# Permitir conexiones establecidas
sudo iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# Permitir loopback
sudo iptables -A INPUT -i lo -j ACCEPT

# Permitir SSH desde blue-team-ws
sudo iptables -A INPUT -s <IP_BLUE_TEAM> -p tcp --dport 22 -j ACCEPT

# SYN cookies
sudo iptables -A INPUT -p tcp --syn -m limit --limit 1/s --limit-burst 3 -j ACCEPT
sudo iptables -A INPUT -p tcp --syn -j DROP

# Rate limiting por IP
sudo iptables -A INPUT -p tcp --dport 80 -m state --state NEW -m recent --set
sudo iptables -A INPUT -p tcp --dport 80 -m state --state NEW -m recent --update --seconds 60 --hitcount 100 -j DROP

# Loggear paquetes descartados
sudo iptables -A INPUT -j LOG --log-prefix "DDOS-DROP: " --log-level 4

# Guardar reglas
sudo iptables-save > /etc/iptables/rules.v4
sudo iptables -L -v -n
```

### 3.2 Habilitar SYN cookies en el kernel
```bash
# Habilitar SYN cookies
sudo sysctl -w net.ipv4.tcp_syncookies=1
sudo sysctl -w net.ipv4.tcp_max_syn_backlog=2048
sudo sysctl -w net.ipv4.tcp_synack_retries=2
sudo sysctl -w net.ipv4.tcp_syn_retries=5

# Guardar cambios
echo "net.ipv4.tcp_syncookies = 1" | sudo tee -a /etc/sysctl.conf
echo "net.ipv4.tcp_max_syn_backlog = 2048" | sudo tee -a /etc/sysctl.conf
echo "net.ipv4.tcp_synack_retries = 2" | sudo tee -a /etc/sysctl.conf
echo "net.ipv4.tcp_syn_retries = 5" | sudo tee -a /etc/sysctl.conf
```

### 3.3 Configurar fail2ban
```bash
# Verificar estado de fail2ban
sudo fail2ban-client status

# Verificar si hay IPs baneadas
sudo fail2ban-client status nginx-http-auth
sudo fail2ban-client status nginx-botsearch

# Banear manualmente una IP sospechosa
sudo fail2ban-client set nginx-http-auth banip <IP_ATACANTE>

# Verificar configuracion
sudo cat /etc/fail2ban/jail.local
```

### 3.4 Limitar conexiones por IP
```bash
# Limitar conexiones simultaneas por IP
sudo iptables -A INPUT -p tcp --dport 80 -m connlimit --connlimit-above 50 -j REJECT

# Limitar tasa de nuevas conexiones
sudo iptables -A INPUT -p tcp --dport 80 -m state --state NEW -m limit --limit 50/s --limit-burst 100 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 80 -m state --state NEW -j DROP
```

---

## Fase 4: Recuperacion

### 4.1 Verificar restauracion del servicio
```bash
# Verificar que nginx esta corriendo
sudo systemctl status nginx

# Verificar que el servidor responde
curl -s -o /dev/null -w "HTTP Code: %{http_code}\nTime: %{time_total}s\n" http://web-srv

# Verificar conectividad
ping -c 5 web-srv

# Verificar que no hay conexiones sospechosas
ss -ant | grep SYN-RECV
ss -ant | awk '{print $1}' | sort | uniq -c | sort -rn
```

### 4.2 Monitorear para detectar re-ataques
```bash
# Iniciar monitoreo continuo
sudo tcpdump -i any -nn port 80 -w /tmp/post_mitigation.pcap &

# Verificar logs de nginx
tail -f /var/log/nginx/banco_access.log &

# Verificar estado del sistema
watch -n 5 'ss -s; echo "---"; ss -ant | awk "{print \$1}" | sort | uniq -c | sort -rn'
```

### 4.3 Restablecer configuracion normal
```bash
# Si es necesario, restaurar reglas iptables normales
sudo iptables -F
sudo iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
sudo iptables -A INPUT -i lo -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT
sudo iptables -A INPUT -j DROP

# Guardar reglas
sudo iptables-save > /etc/iptables/rules.v4
```

---

## Fase 5: Reporte

### 5.1 Plantilla de reporte de incidente

```
========================================
REPORTE DE INCIDENTE DE SEGURIDAD
Banco del Sol - Incidente #003
========================================

FECHA DEL INCIDENTE: [Fecha]
HORA DE DETECCION: [Hora]
HORA DE MITIGACION: [Hora]
DURACION TOTAL: [Duracion]

RESUMEN:
Ataque DDoS contra el servidor web del Banco del Sol. Se utilizaron
ataques SYN flood (hping3) y HTTP flood (slowloris) para hacer
inaccesible el servicio web.

IMPACTO:
- Servidor web inaccesible durante [duracion]
- Usuarios afectados: [cantidad]
- Servicios afectados: Banca Online

TIPO DE ATAQUE:
- SYN flood: [duracion]
- HTTP flood (slowloris): [duracion]

INDICADORES DE COMPROMISO:
- IP del atacante: [IP]
- Patron de trafico: [descripcion]
- Conexiones SYN-RECV: [cantidad maxima]

ACCIONES TOMADAS:
1. [Fecha/Hora] Deteccion del ataque
2. [Fecha/Hora] Mitigacion con iptables
3. [Fecha/Hora] Habilitacion de SYN cookies
4. [Fecha/Hora] Configuracion de fail2ban
5. [Fecha/Hora] Verificacion de restauracion

LECCIONES APRENDIDAS:
- [Leccion 1]
- [Leccion 2]
- [Leccion 3]

RECOMENDACIONES:
1. Implementar CDN para proteccion DDoS
2. Coordinar con ISP para filtrado de trafico
3. Implementar BCP (Business Continuity Plan)
4. Realizar pruebas de resistencia DDoS

========================================
```

### 5.2 Plantilla de notificacion al ISP

```
ASUNTO: Solicitud de Mitigacion DDoS - Banco del Sol

Estimado equipo de soporte:

Se esta experimentando un ataque DDoS contra nuestro servidor web.
Detalles del ataque:
- IP objetivo: [IP del servidor web]
- Tipo de ataque: SYN flood + HTTP flood
- Hora de inicio: [Hora]
- IP atacante: [IP del atacante]

Solicitamos:
1. Filtrado de trafico desde la IP atacante
2. Monitoreo de trafico hacia nuestra red
3. Soporte para mitigacion del ataque

Attentamente,
[Nombre]
Banco del Sol
```

---

## Fase 6: Prevencion a Largo Plazo

### 6.1 Implementar CDN
- Considerar Cloudflare, AWS CloudFront u otro proveedor CDN
- Configurar reglas de firewall en el CDN
- Habilitar proteccion DDoS del proveedor

### 6.2 Coordinacion con ISP
- Establecer protocolo de respuesta con el ISP
- Configurar BGP flowspec si es posible
- Implementar Blackhole routing como ultima opcion

### 6.3 Business Continuity Plan
- Documentar procedimientos de respuesta a DDoS
- Establecer tiempos de respuesta objetivo
- Implementar failover a servidores de respaldo
- Realizar simulacros periodicamente

### 6.4 Herramientas utilizadas
- hping3 (para SYN flood)
- slowloris (para HTTP flood)
- tcpdump (para analisis de trafico)
- iptables (para mitigacion)
- fail2ban (para proteccion automatizada)
- sysctl (para configuracion del kernel)
- curl (para verificacion de servicio)

### 6.5 Tiempos de respuesta
| Fase | Tiempo Objetivo | Tiempo Real |
|------|----------------|-------------|
| Deteccion | < 5 minutos | [Medir] |
| Analisis | < 15 minutos | [Medir] |
| Mitigacion | < 30 minutos | [Medir] |
| Recuperacion | < 1 hora | [Medir] |
| Reporte | < 2 horas | [Medir] |
