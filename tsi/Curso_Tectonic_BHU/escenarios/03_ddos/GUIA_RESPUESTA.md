# GUIA DE RESPUESTA - ATAQUE DDoS SYN FLOOD
## Banco del Sol - Escenario 03

---

## INFORMACION DEL ESCENARIO

| Campo | Valor |
|-------|-------|
| Nombre | DDoS SYN Flood |
| Objetivo | Webserver (10.10.1.10) |
| Tipo de ataque | SYN Flood + Amplificacion DNS |
| Rol del estudiante | Blue Team - Respuesta a Incidentes |
| Duracion estimada | 2 horas |
| Dificultad | Intermedio |

---

## FASE 1: DETECCION

La deteccion temprana es critica para minimizar el impacto del ataque. Los indicadores principales incluyen degradacion del servicio web, incremento anomalo de trafico de red y consumo excesivo de recursos del servidor.

### 1.1 Verificar Estado del Servicio Web

```bash
# Verificar tiempo de respuesta del servidor web
curl -w "Tiempo total: %{time_total}s\nTiempo conexion: %{time_connect}s\nHTTP Code: %{http_code}\n" -o /dev/null -s http://10.10.1.10/

# Verificar si el servicio esta respondiendo
curl -I http://10.10.1.10/ 2>/dev/null | head -5

# Probar pagina de login
curl -s -o /dev/null -w "%{http_code}" http://10.10.1.10/login.html
```

**Indicadores de ataque:**
- Tiempo de respuesta superior a 5 segundos
- Codigo de respuesta 503 o 504
- Timeouts de conexion
- Respuestas incompletas

### 1.2 Verificar Uso de Recursos del Servidor

```bash
# Verificar uso de CPU y memoria
top -bn1 | head -10

# Uso de memoria detallado
free -h

# Uso de disco
df -h

# Procesos con mayor consumo
ps aux --sort=-%cpu | head -10
ps aux --sort=-%mem | head -10
```

**Indicadores de ataque:**
- CPU al 100% o cercano
- Memoria consumida superior al 90%
- Procesos apache2/nginx con alto consumo
- Load average elevado

### 1.3 Verificar Conexiones de Red

```bash
# Estadisticas generales de conexiones TCP
ss -s

# Conexiones en estado SYN_RECV (indicador principal de SYN flood)
ss -tn state syn-recv | wc -l

# Todas las conexiones SYN_RECV
ss -tn state syn-recv

# Conexiones por estado
ss -tn | awk '{print $1}' | sort | uniq -c | sort -rn

# Conexiones establecidas
ss -tn state established | wc -l

# Conexiones en TIME_WAIT
ss -tn state time-wait | wc -l
```

**Indicadores de ataque:**
- Numero elevado de conexiones SYN_RECV (cualquier cantidad superior a 100 es sospechosa)
- Incremento rapido de conexiones totales
- Presencia de miles de conexiones SYN_RECV con pocos ESTABLISHED

### 1.4 Verificar Trafico de Red

```bash
# Capturar trafico SYN entrante (10 segundos)
timeout 10 tcpdump -i any 'tcp[tcpflags] & (tcp-syn) != 0' -c 50

# Contar paquetes SYN por segundo
tcpdump -i any 'tcp[tcpflags] & (tcp-syn) != 0' -c 100 2>/dev/null | wc -l

# Ver interfaces de red y trafico
ip -s link show

# Monitoreo en tiempo real con nload (si esta disponible)
nload eth0
```

**Indicadores de ataque:**
- Mas de 100 paquetes SYN por segundo
- Incremento repentino de trafico de entrada
- Trafico asimetrico (mucho mas RX que TX)

### 1.5 Verificar Tabla de Conntrack

```bash
# Verificar entradas actuales de conntrack
cat /proc/net/nf_conntrack | wc -l

# Verificar maximo permitido
sysctl -n net.netfilter.nf_conntrack_max

# Calcular porcentaje de uso
CURRENT=$(cat /proc/net/nf_conntrack | wc -l)
MAX=$(sysctl -n net.netfilter.nf_conntrack_max)
echo "Uso de conntrack: $CURRENT / $MAX ($(echo "scale=2; $CURRENT * 100 / $MAX" | bc)%)"

# Verificar si hay overflow
dmesg | grep -i "conntrack"
```

**Indicadores de ataque:**
- Conntrack al 80% o mas
- Mensajes de "nf_conntrack: table full" en dmesg
- Paquetes descartados por lack of conntrack entries

### 1.6 Verificar Logs del Servidor Web

```bash
# Ver logs de Apache recientes
tail -50 /var/log/apache2/bancodelsol_access.log

# Contar requests por IP
awk '{print $1}' /var/log/apache2/bancodelsol_access.log | sort | uniq -c | sort -rn | head -20

# Ver errores
tail -50 /var/log/apache2/bancodelsol_error.log

# Ver logs del kernel
tail -50 /var/log/kern.log
```

**Indicadores de ataque:**
- Miles de requests de las mismas IPs o rango de IPs
- IPs con patron 172.16.x.x (spoofed)
- Mensajes de "connection reset" o "timeout"
- Logs de kernel indicando SYN flood

---

## FASE 2: ANALISIS

Una vez detectado el ataque, es necesario analizarlo para determinar su naturaleza, alcance y mejores estrategias de mitigacion.

### 2.1 Capturar Paquetes de Ataque

```bash
# Capturar trafico SYN en archivo pcap
tcpdump -i eth0 -w /tmp/syn_flood.pcap 'tcp[tcpflags] & (tcp-syn) != 0' -c 10000

# Capturar todo el trafico del puerto 80
tcpdump -i eth0 -w /tmp/port80.pcap port 80 -c 5000

# Capturar con filtro de IPs sospechosas
tcpdump -i eth0 -w /tmp/attack.pcap 'src net 172.16.0.0/24 and tcp port 80'
```

### 2.2 Analizar IPs Origen del Ataque

```bash
# Extraer IPs origen de paquetes SYN
tcpdump -r /tmp/syn_flood.pcap -n 'tcp[tcpflags] & (tcp-syn) != 0' 2>/dev/null | \
  awk '{print $3}' | cut -d. -f1-4 | sort | uniq -c | sort -rn | head -30

# Analizar con tshark (si esta disponible)
tshark -r /tmp/syn_flood.pcap -T fields -e ip.src | sort | uniq -c | sort -rn | head -20

# Identificar rango de IPs atacantes
tcpdump -r /tmp/syn_flood.pcap -n 'tcp[tcpflags] & (tcp-syn) != 0' 2>/dev/null | \
  awk '{print $3}' | cut -d. -f1-3 | sort -u
```

**Analisis:**
- Si las IPs pertenecen al rango 172.16.0.0/24, son spoofed
- Un patron de IPs aleatorias indica suplantacion de origen
- Un solo origen indica ataque directo (no DDoS)

### 2.3 Analizar Patron de Ataque

```bash
# Verificar flags TCP de los paquetes
tcpdump -r /tmp/syn_flood.pcap -n -v 'tcp[tcpflags] & (tcp-syn) != 0' 2>/dev/null | head -50

# Verificar tamanos de paquete
tcpdump -r /tmp/syn_flood.pcap -n 'tcp[tcpflags] & (tcp-syn) != 0' 2>/dev/null | \
  awk '{print $NF}' | sort | uniq -c | sort -rn

# Analizar puertos destino
tcpdump -r /tmp/syn_flood.pcap -n 'tcp[tcpflags] & (tcp-syn) != 0' 2>/dev/null | \
  awk '{print $5}' | cut -d. -f5 | sort | uniq -c | sort -rn
```

### 2.4 Identificar Tipo de Ataque

**SYN Flood Basico:**
- Paquetes SYN sin completar el handshake
- Incremento de conexiones SYN_RECV
- Sin paquetes ACK de respuesta

**SYN Flood Distribuido:**
- Multiples IPs origen (spoofed o reales)
- Patron aleatorio de puertos origen
- Trafico masivo entrante

**Amplificacion DNS:**
- Trafico UDP entrante masivo
- Puertos 53 DNS como origen
- Paquetes de respuesta DNS grandes

### 2.5 Medir Impacto

```bash
# Comparar metricas antes/durante ataque
# Antes del ataque (baseline):
cat /var/log/bancodelsol/attack/baseline.log

# Durante el ataque:
cat /var/log/bancodelsol/attack/realtime_monitor.log

# Diferencias clave:
# - Conexiones TCP totales
# - Conexiones SYN_RECV
# - Uso de CPU
# - Uso de memoria
# - Paquetes descartados
```

---

## FASE 3: CONTENCION

La contencion busca limitar el impacto del ataque sin necesariamente detenerlo completamente. El objetivo es mantener el servicio operativo.

### 3.1 Activar SYN Cookies

SYN cookies es una contramedida que permite al servidor TCP responder a conexiones SYN sin mantener estado, evitando que la tabla de conexiones se llene.

```bash
# Activar SYN cookies inmediatamente
sysctl -w net.ipv4.tcp_syncookies=1

# Ajustar backlog de conexiones SYN
sysctl -w net.ipv4.tcp_max_syn_backlog=65536

# Reducir reintentos SYN-ACK
sysctl -w net.ipv4.tcp_synack_retries=2

# Verificar que estan activos
sysctl net.ipv4.tcp_syncookies
sysctl net.ipv4.tcp_max_syn_backlog
```

**Explicacion:** SYN cookies permiten al servidor generar un numero de secuencia criptografico basado en la IP origen, puerto origen y timestamp. Si el cliente responde con ACK correcto, la conexion se establece sin haber guardado estado previamente.

### 3.2 Configurar Rate Limiting con iptables

Rate limiting controla cuantas conexiones nuevas puede recibir cada IP por unidad de tiempo.

```bash
# Limpiar reglas previas de rate limiting
iptables -D INPUT -p tcp --syn --dport 80 -m hashlimit --hashlimit-above 25/sec --hashlimit-burst 50 --hashlimit-mode srcip --hashlimit-name flood80 -j DROP 2>/dev/null || true
iptables -D INPUT -p tcp --syn --dport 443 -m hashlimit --hashlimit-above 25/sec --hashlimit-burst 50 --hashlimit-mode srcip --hashlimit-name flood443 -j DROP 2>/dev/null || true

# Rate limiting para SYN en puerto 80
# Maximo 25 SYN/segundo por IP, rafaga de 50
iptables -I INPUT -p tcp --syn --dport 80 -m hashlimit \
  --hashlimit-above 25/sec \
  --hashlimit-burst 50 \
  --hashlimit-mode srcip \
  --hashlimit-name flood80 \
  -j DROP

# Rate limiting para SYN en puerto 443
iptables -I INPUT -p tcp --syn --dport 443 -m hashlimit \
  --hashlimit-above 25/sec \
  --hashlimit-burst 50 \
  --hashlimit-mode srcip \
  --hashlimit-name flood443 \
  -j DROP

# Limitar conexiones totales por IP
iptables -I INPUT -p tcp --dport 80 -m connlimit \
  --connlimit-above 50 \
  --connlimit-mask 32 \
  -j DROP

iptables -I INPUT -p tcp --dport 443 -m connlimit \
  --connlimit-above 50 \
  --connlimit-mask 32 \
  -j DROP
```

### 3.3 Bloquear IPs y Rangos Atacantes

```bash
# Crear conjunto de IPs para bloqueo rapido
ipset create blocked_ips hash:net maxelem 100000 -exist

# Agregar rango de IPs atacantes (spoofed)
ipset add blocked_ips 172.16.0.0/24

# Bloquear IPs individuales identificadas
# ipset add blocked_ips 172.16.0.10
# ipset add blocked_ips 172.16.0.20

# Aplicar bloqueo con iptables
iptables -I INPUT -m set --match-set blocked_ips src -j DROP

# Verificar regla
iptables -L INPUT -n -v | grep blocked_ips
```

**Alternativa sin ipset:**

```bash
# Bloquear rango completo
iptables -I INPUT -s 172.16.0.0/24 -j DROP

# Bloquear IPs individuales
# iptables -I INPUT -s 172.16.0.10 -j DROP
# iptables -I INPUT -s 172.16.0.20 -j DROP
```

### 3.4 Configurar fail2ban para SYN Flood

fail2ban monitora logs y bloquea automaticamente IPs con patron sospechoso.

```bash
# Verificar estado de fail2ban
fail2ban-client status

# Ver estado de la jail especifica
fail2ban-client status apache-synflood

# Bloquear IP manualmente
fail2ban-client set apache-synflood banip 172.16.0.10

# Ver IPs bloqueadas
fail2ban-client status apache-synflood | grep "Banned IP"
```

**Configuracion recomendada para SYN flood:**

```ini
# /etc/fail2ban/jail.local
[apache-synflood]
enabled = true
port = http,https
filter = apache-synflood
logpath = /var/log/apache2/bancodelsol_access.log
maxretry = 100
findtime = 10
bantime = 3600
```

### 3.5 Ajustar Parametros TCP del Servidor

```bash
# Reducir timeout de conexiones
sysctl -w net.ipv4.tcp_fin_timeout=15

# Reducir keepalive
sysctl -w net.ipv4.tcp_keepalive_time=60
sysctl -w net.ipv4.tcp_keepalive_intvl=10
sysctl -w net.ipv4.tcp_keepalive_probes=3

# Limitar puertos locales
sysctl -w net.ipv4.ip_local_port_range="1024 32768"

# Habilitar reutilizacion de TIME_WAIT
sysctl -w net.ipv4.tcp_tw_reuse=1

# Limitar maximo de TIME_WAIT
sysctl -w net.ipv4.tcp_max_tw_buckets=10000
```

### 3.6 Implementar Proteccion a Nivel de Red

```bash
# Habilitar proteccion anti-SYN en kernel
sysctl -w net.ipv4.tcp_syncookies=1
sysctl -w net.ipv4.tcp_max_syn_backlog=65536
sysctl -w net.ipv4.tcp_synack_retries=1

# Limitar conexiones nuevas por segundo
iptables -A INPUT -p tcp --syn -m limit --limit 100/s --limit-burst 200 -j ACCEPT
iptables -A INPUT -p tcp --syn -j DROP

# Bloquear paquetes con flags invalidos
iptables -A INPUT -p tcp --tcp-flags ALL NONE -j DROP
iptables -A INPUT -p tcp --tcp-flags ALL ALL -j DROP
iptables -A INPUT -p tcp --tcp-flags ALL FIN,URG,PSH -j DROP
iptables -A INPUT -p tcp --tcp-flags ALL SYN,RST,ACK,FIN,URG -j DROP
iptables -A INPUT -p tcp --tcp-flags SYN,RST SYN,RST -j DROP
iptables -A INPUT -p tcp --tcp-flags SYN,FIN SYN,FIN -j DROP
```

---

## FASE 4: ERADICACION

La erradicacion busca detener completamente el trafico de ataque y verificar que las contramedidas son efectivas.

### 4.1 Verificar Efectividad de Reglas

```bash
# Ver todas las reglas activas
iptables -L INPUT -n -v --line-numbers

# Verificar contadores de paquetes
iptables -L INPUT -n -v | head -20

# Verificar SYN_RECV despues de mitigacion
ss -tn state syn-recv | wc -l

# Comparar con baseline
echo "SYN_RECV actual: $(ss -tn state syn-recv | wc -l)"
echo "SYN_RECV baseline: Ver /var/log/bancodelsol/attack/baseline.log"
```

### 4.2 Monitorear Reduccion de Trafico

```bash
# Capturar trafico SYN actual
tcpdump -i any 'tcp[tcpflags] & (tcp-syn) != 0' -c 20 2>/dev/null

# Verificar que el trafico de ataque disminuyo
# El trafico SYN debe ser significativamente menor

# Verificar que las IPs bloqueadas no pasan
iptables -L blocked_ips -n -v 2>/dev/null || echo "Conjunto blocked_ips activo"
```

### 4.3 Verificar Servicio Web

```bash
# Probar respuesta HTTP
curl -I http://10.10.1.10/

# Verificar tiempo de respuesta
curl -w "Tiempo: %{time_total}s\n" -o /dev/null -s http://10.10.1.10/

# Verificar pagina de login
curl -s -o /dev/null -w "%{http_code}" http://10.10.1.10/login.html

# Verificar que Apache esta funcionando
systemctl status apache2
```

### 4.4 Limpiar Tabla de Conntrack

```bash
# Eliminar entradas viejas
conntrack -F

# O reiniciar modulo de conntrack
modprobe -r nf_conntrack
modprobe nf_conntrack

# Verificar tabla limpiada
cat /proc/net/nf_conntrack | wc -l
```

### 4.5 Verificar Ausencia de Bypass

```bash
# Verificar que no hay reglas que permitan trafico de ataque
iptables -L INPUT -n -v | grep -E "DROP|REJECT"

# Verificar que fail2ban esta activo
fail2ban-client status

# Verificar SYN cookies activos
sysctl net.ipv4.tcp_syncookies

# Verificar que rate limiting esta funcionando
iptables -L INPUT -n -v | grep hashlimit
```

---

## FASE 5: RECUPERACION

La recuperacion busca restaurar el servicio a su estado normal y verificar la integridad del sistema.

### 5.1 Restaurar Parametros TCP

```bash
# Restaurar timeouts normales
sysctl -w net.ipv4.tcp_fin_timeout=30
sysctl -w net.ipv4.tcp_keepalive_time=600
sysctl -w net.ipv4.ip_local_port_range="1024 65535"

# Mantener SYN cookies activos (buena practica)
sysctl -w net.ipv4.tcp_syncookies=1

# Restaurar SYNACK retries (no reducir mas de lo necesario)
sysctl -w net.ipv4.tcp_synack_retries=2
```

### 5.2 Reiniciar Servicios

```bash
# Reiniciar Apache
systemctl restart apache2

# Verificar estado
systemctl status apache2

# Reiniciar fail2ban (opcional, mantiene bans activos)
systemctl restart fail2ban

# Verificar servicios
systemctl list-units --type=service --state=running | grep -E "apache|fail2ban|iptables"
```

### 5.3 Limpiar Reglas Temporales

```bash
# Opcion 1: Mantener reglas de protection (recomendado)
# Las reglas de rate limiting y SYN cookies deben permanecer

# Opcion 2: Limpiar solo bloqueos temporales
# Si se usaron bloqueos agresivos, considerar removerlos
# iptables -D INPUT -s 172.16.0.0/24 -j DROP

# Guardar reglas actuales
iptables-save > /etc/iptables/rules.v4
```

### 5.4 Verificar Integridad del Sistema

```bash
# Verificar archivos criticos
md5sum /etc/apache2/apache2.conf
md5sum /var/www/bancodelsol/index.html

# Verificar que no hay procesos sospechosos
ps aux | grep -E "nc|ncat|netcat|hping|scapy"

# Verificar conexiones establecidas normales
ss -tn state established | wc -l

# Verificar que el servicio responde normalmente
for i in $(seq 1 10); do
  curl -s -o /dev/null -w "Request $i: %{http_code} - %{time_total}s\n" http://localhost/
done
```

### 5.5 Restaurar Metricas Normales

```bash
# Verificar metricas finales
echo "=== Metricas de Recuperacion ==="
echo "CPU: $(top -bn1 | grep 'Cpu(s)' | awk '{print $2}')%"
echo "Memory: $(free | awk '/Mem:/ {printf "%.2f%%", $3/$2 * 100}')"
echo "TCP ESTABLISHED: $(ss -tn state established | wc -l)"
echo "TCP SYN_RECV: $(ss -tn state syn-recv | wc -l)"
echo "TCP TIME_WAIT: $(ss -tn state time-wait | wc -l)"
echo "Conntrack: $(cat /proc/net/nf_conntrack | wc -l)"
echo "=== Fin ==="
```

---

## FASE 6: DOCUMENTACION Y LECCIONES APRENDIDAS

### 6.1 Documentar el Incidente

**Timeline del incidente:**
```
[T+00:00] Ataque inicia (SYN flood contra puerto 80)
[T+01:00] Primer indicador de degradacion detectado
[T+02:00] Deteccion formal del ataque
[T+03:00] Analisis de trafico y identificacion de patron
[T+05:00] Implementacion de SYN cookies
[T+07:00] Configuracion de rate limiting
[T+10:00] Bloqueo de IPs atacantes
[T+15:00] Reduccion significativa del trafico de ataque
[T+20:00] Verificacion de efectividad
[T+30:00] Servicio restaurado a normalidad
[T+60:00] Documentacion completada
```

**Indicadores de Compromiso (IOCs):**
- IPs origen: 172.16.0.0/24 (spoofed)
- Patron: SYN sin completar handshake
- Puertos objetivo: 80, 443
- Volumen: 5000+ paquetes SYN/segundo

**Metricas de impacto:**
- Tiempo de respuesta: incremento de 200ms a 5+ segundos
- Disponibilidad del servicio: degradada ~40%
- Conexiones SYN_RECV: pico de 5000+
- CPU: al 100% durante el ataque

### 6.2 Analisis de Respuesta

**Que funciono bien:**
- Deteccion temprana del ataque
- SYN cookies se activaron rapidamente
- Rate limiting redujo trafico significativamente

**Que se pudo mejorar:**
- Falta monitoreo proactivo de trafico SYN
- No habia alertas automaticas configuradas
- Parametros TCP no estaban optimizados previamente

**Tiempo de respuesta:**
- Deteccion: 2 minutos
- Contencion: 5 minutos
- Recuperacion: 10 minutos
- Total: 17 minutos

### 6.3 Recomendaciones de Mejora

**Corto plazo:**
1. Configurar monitoreo continuo de trafico SYN
2. Establecer alertas automaticas para patrones de ataque
3. Documentar procedimientos de respuesta a DDoS
4. Implementar dashboards de metricas de red

**Mediano plazo:**
1. Implementar solucion CDN con proteccion DDoS
2. Configurar BGP Flowspec para mitigacion en capa de red
3. Implementar segmentacion de red mas granular
4. Establecer acuerdos con proveedor de Internet para filtrado

**Largo plazo:**
1. Adquirir solucion anti-DDoS dedicada
2. Implementar arquitectura de alta disponibilidad
3. Realizar simulacros periodicos de DDoS
4. Establecer capacidades de absorcion de ataques

### 6.4 Herramientas de Monitoreo a Implementar

```
- tcpdump/tshark: Analisis de paquetes
- iftop/nethogs: Monitoreo de trafico en tiempo real
- ss/netstat: Analisis de conexiones
- vnstat: Estadisticas de trafico historicas
- collectd: Recoleccion de metricas del sistema
- Grafana/Influxdb: Dashboards de visualizacion
- fail2ban: Proteccion automatica contra abuso
- iptables/nftables: Control de acceso a nivel de red
```

---

## COMANDOS RAPIDOS DE REFERENCIA

### Deteccion
```bash
ss -s && ss -tn state syn-recv | wc -l
top -bn1 | head -5
tcpdump -i any 'tcp[tcpflags] & (tcp-syn) != 0' -c 20
```

### Contencion
```bash
sysctl -w net.ipv4.tcp_syncookies=1
iptables -I INPUT -p tcp --syn --dport 80 -m hashlimit --hashlimit-above 25/sec --hashlimit-burst 50 --hashlimit-mode srcip --hashlimit-name flood -j DROP
fail2ban-client set apache-synflood banip IP_ATACANTE
```

### Verificacion
```bash
curl -I http://localhost/
ss -tn state syn-recv | wc -l
iptables -L INPUT -n -v | head -20
```

---

## NOTAS PARA EL INSTRUCTOR

1. **Preparacion:** Verificar que todas las maquinas estan configuradas correctamente antes de iniciar
2. **Inicio del ataque:** El ataque comienza 10 minutos despues de la clonacion
3. **Guia:** Permitir que los estudiantes intenten detectar el ataque antes de dar pistas
4. **Puntos clave:** SYN cookies, rate limiting, iptables son los conceptos mas importantes
5. **Extension:** Si el tiempo lo permite, proponer mitigaciones adicionales como CDN
6. **Evaluacion:** Usar el rubrico de scoring del archivo banco_del_sol_ddos.yml

---

*Guia de respuesta para escenario DDoS SYN Flood - Banco del Sol*
*BHU Uruguay - Curso de Ciberseguridad*
*Fecha: 2026-07-13*
