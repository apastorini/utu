# Guia de Respuesta - Escenario 05: Exfiltracion via DNS Tunneling

## Banco del Sol - Tectonic Cyber Range

**Nivel:** Avanzado  
**Duracion estimada:** 2.5 horas  
**Rol:** Equipo Azul (Defensores)

---

## Fase 1: Deteccion

### 1.1 Alertas iniciales

El escenario presenta una estacion de trabajo que ha sido comprometida y esta exfiltrando datos a traves de consultas DNS. Los indicadores iniciales pueden incluir:

- Reportes de usuarios sobre lento rendimiento de red
- Alertas de monitorizacion de DNS (si esta configurada)
- Consumo inusual de ancho de banda en la interfaz de la workstation
- Logs DNS con volumen anomalamente alto

### 1.2 Revision de logs DNS

El primer paso es revisar los logs de DNS para identificar patrones anomalo.

```bash
# En el domaincontroller (10.10.2.10)
# Revisar el log de consultas DNS
tail -f /var/log/bind/query.log

# Buscar consultas al dominio sospechoso
grep "exfil.attacker.com" /var/log/bind/query.log

# Contar consultas por dominio (ultimas 1000 lineas)
tail -1000 /var/log/bind/query.log | grep -oP '\S+\.exfil\.attacker\.com' | sort | uniq -c | sort -rn

# Contar total de consultas al dominio de exfiltracion
grep -c "exfil.attacker.com" /var/log/bind/query.log
```

### 1.3 Identificar consultas con subdominios largos

Las consultas DNS normales tienen subdominios cortos (15-25 caracteres). Las consultas de exfiltracion tienen subdominios muito largos (60+ caracteres).

```bash
# Buscar consultas con subdominios inusualmente largos
# Los subdominios de exfiltracion contienen base64
grep "exfil.attacker.com" /var/log/bind/query.log | awk '{print length, $0}' | sort -rn | head -20

# Buscar subdominios que parezcan base64
grep -oP '[a-zA-Z0-9_-]{40,}\.exfil\.attacker\.com' /var/log/bind/query.log | head -10
```

### 1.4 Analisis de frecuencia de consultas

```bash
# Contar consultas por minuto al dominio sospechoso
grep "exfil.attacker.com" /var/log/bind/query.log | \
  cut -d: -f1-2 | uniq -c | sort -rn | head -20

# Comparar con trafico DNS normal
# Las consultas normales son ~0.5 por minuto, las de exfiltracion ~19 por minuto
grep "exfil.attacker.com" /var/log/bind/query.log | wc -l
grep -v "exfil.attacker.com" /var/log/bind/query.log | wc -l
```

### 1.5 Detectar abuso de registros TXT

```bash
# Buscar consultas TXT en el trafico DNS
grep -i "TXT" /var/log/bind/query.log | grep "exfil.attacker.com" | head -20

# Contar consultas por tipo de registro
grep "exfil.attacker.com" /var/log/bind/query.log | grep -oP 'IN\s+\w+' | sort | uniq -c | sort -rn
```

### 1.6 Puntos clave de deteccion

Los siguientes patrones indican actividad de DNS tunneling:

1. **Volumen:** Mas de 100 consultas al mismo dominio externo en una hora
2. **Longitud:** Subdominios superiores a 40 caracteres
3. **Frecuencia:** Mas de 10 consultas por minuto al mismo dominio
4. **Tipo de registro:** Predominio de consultas TXT (mas del 80%)
5. **Patron temporal:** Consultas en bursts regulares (2-5 segundos de pausa)
6. **Origen:** Todas las consultas provienen de la misma IP interna (10.10.2.100)

---

## Fase 2: Analisis

### 2.1 Captura de trafico DNS

```bash
# En la workstation o en el domaincontroller
# Iniciar captura de trafico DNS
tcpdump -i any port 53 -w /tmp/dns_capture.pcap

# Dejar capturar durante 2-3 minutos
# Luego detener con Ctrl+C
```

### 2.2 Analisis con tshark

```bash
# Filtrar solo consultas DNS al dominio sospechoso
tshark -r /tmp/dns_capture.pcap -Y "dns.qry.name contains exfil.attacker.com" -T fields -e frame.time -e dns.qry.name

# Extraer subdominios de las consultas
tshark -r /tmp/dns_capture.pcap -Y "dns.qry.name contains exfil.attacker.com" -T fields -e dns.qry.name | \
  sed 's/.exfil.attacker.com//g' | head -20

# Contar consultas por tipo
tshark -r /tmp/dns_capture.pcap -Y "dns.qry.name contains exfil.attacker.com" -T fields -e dns.qry.type | sort | uniq -c

# Ver respuestas TXT
tshark -r /tmp/dns_capture.pcap -Y "dns.txt && dns.qry.name contains exfil.attacker.com" -T fields -e dns.txt
```

### 2.3 Decodificar datos exfiltrados

Los subdominios contienen datos codificados en base64url (sin padding). Para decodificar:

```bash
# Extraer subdominios y decodificar
tshark -r /tmp/dns_capture.pcap -Y "dns.qry.name contains exfil.attacker.com" -T fields -e dns.qry.name | \
  sed 's/.exfil.attacker.com//g' | \
  sed 's/-[a-f0-9]\{6\}$//' | \
  sed 's/-//g' | \
  while read line; do
    # Agregar padding si es necesario
    padded=$(echo "$line" | sed 's/=$//' && echo "====" | head -c $((4 - ${#line} % 4)))
    echo "$padded" | base64 -d 2>/dev/null
  done | head -50
```

### 2.4 Script de decodificacion completo

```bash
#!/bin/bash
# Script para decodificar datos exfiltrados via DNS tunneling
# Uso: ./decode_exfil.sh <captura.pcap>

PCAP_FILE=$1

if [ -z "$PCAP_FILE" ]; then
    echo "Uso: $0 <archivo.pcap>"
    exit 1
fi

echo "=== Analisis de Exfiltracion DNS Tunneling ==="
echo ""

# 1. Resumen de consultas
echo "--- Resumen ---"
TOTAL=$(tshark -r "$PCAP_FILE" -Y "dns.qry.name contains exfil.attacker.com" 2>/dev/null | wc -l)
echo "Total de consultas al dominio exfil: $TOTAL"

# 2. Top subdominios mas largos
echo ""
echo "--- Subdominios mas largos (posibles datos exfiltrados) ---"
tshark -r "$PCAP_FILE" -Y "dns.qry.name contains exfil.attacker.com" -T fields -e dns.qry.name 2>/dev/null | \
  awk '{print length, $0}' | sort -rn | head -10

# 3. Decodificar primeros 10 chunks
echo ""
echo "--- Primeros 10 chunks decodificados ---"
tshark -r "$PCAP_FILE" -Y "dns.qry.name contains exfil.attacker.com" -T fields -e dns.qry.name 2>/dev/null | \
  sed 's/.exfil.attacker.com//g' | \
  head -10 | \
  while IFS= read -r line; do
    # Extraer solo la parte codificada (despues del primer guion)
    encoded=$(echo "$line" | sed 's/^[0-9]*-//' | sed 's/-[a-f0-9]*$//')
    # Decodificar base64
    decoded=$(echo "$encoded" | tr '_-' '/+' | sed 's/=$//' && printf '%*s' $(( ($(echo -n "$encoded" | wc -c) + 2) / 3 * 4 - $(echo -n "$encoded" | wc -c) )) '' | tr ' ' '=')
    echo "Chunk: $line"
    echo "Decoded: $(echo "$decoded" | base64 -d 2>/dev/null)"
    echo "---"
  done
```

### 2.5 Mapear el canal de command and control

```bash
# Identificar respuestas del servidor C2
tshark -r /tmp/dns_capture.pcap -Y "dns.flags.response == 1 && dns.qry.name contains exfil.attacker.com" -T fields -e dns.txt

# Ver IPs involucradas
tshark -r /tmp/dns_capture.pcap -Y "dns.qry.name contains exfil.attacker.com" -T fields -e ip.src -e ip.dst | sort | uniq -c | sort -rn

# Analizar intervalos entre consultas
tshark -r /tmp/dns_capture.pcap -Y "dns.qry.name contains exfil.attacker.com" -T fields -e frame.time_relative | \
  awk 'NR>1{print $1-prev}{prev=$1}' | sort -n | tail -10
```

### 2.6 Verificar datos en la workstation

```bash
# En la workstation (10.10.2.100)
# Buscar archivos sospechosos
find /home/student -name "*.py" -o -name "*.sh" -o -name "*exfil*" 2>/dev/null
find /tmp -name "*exfil*" -o -name "*dns*" 2>/dev/null

# Revisar scheduled tasks
crontab -l 2>/dev/null
ls -la /etc/cron* 2>/dev/null
systemctl list-timers 2>/dev/null

# Revisar procesos en ejecucion
ps aux | grep -E "python|dns|tunnel"

# Revisar el script de exfiltracion
cat /home/student/dns_tunnel.py
```

---

## Fase 3: Contencion

### 3.1 Bloquear el dominio de exfiltracion

```bash
# En el domaincontroller (10.10.2.10)
# Bloquear el dominio en DNS

# Agregar zona negativa para el dominio
cat >> /etc/bind/named.conf.local << 'EOF'
zone "exfil.attacker.com" {
    type master;
    file "/etc/bind/zones/negativo.exfil.attacker.com.zone";
    allow-query { any; };
};
EOF

# Crear zona negativa
cat > /etc/bind/zones/negativo.exfil.attacker.com.zone << 'EOF'
$TTL 600
@       IN      SOA     ns1.bancodelsol.local. admin.bancodelsol.local. (
                        2025011501      ; Serial
                        3600            ; Refresh
                        900             ; Retry
                        604800          ; Expire
                        600 )           ; Minimum TTL
        
        IN      NS      ns1.bancodelsol.local.

; Bloqueo total del dominio
*       IN      A       127.0.0.1
*       IN      AAAA    ::1
EOF

# Reiniciar DNS
systemctl restart bind9
```

### 3.2 Implementar limites de longitud de consultas DNS

```bash
# En el domaincontroller
# Configurar rate limiting en BIND
cat >> /etc/bind/named.conf.options << 'EOF'
options {
    // ... opciones existentes ...
    
    rate-limit {
        responses-per-second 5;
        window 5;
        slip 1;
        all-per-second 10;
        log-only no;
    };
};
EOF

# Reiniciar DNS
systemctl restart bind9
```

### 3.3 Bloquear resolucion DNS externa

```bash
# En el domaincontroller
# Configurar firewall para bloquear DNS externo
iptables -A OUTPUT -p udp --dport 53 -d 8.8.8.8 -j DROP
iptables -A OUTPUT -p udp --dport 53 -d 8.8.4.4 -j DROP
iptables -A OUTPUT -p tcp --dport 53 -d 8.8.8.8 -j DROP
iptables -A OUTPUT -p tcp --dport 53 -d 8.8.4.4 -j DROP

# Permitir solo DNS interno
iptables -A OUTPUT -p udp --dport 53 -d 10.10.2.10 -j ACCEPT
iptables -A OUTPUT -p tcp --dport 53 -d 10.10.2.10 -j ACCEPT

# Guardar reglas
iptables-save > /etc/iptables/rules.v4
```

### 3.4 Aislar la estacion de trabajo comprometida

```bash
# En la workstation (10.10.2.100) o desde management
# Matar procesos de exfiltracion
pkill -f dns_tunnel.py
pkill -f exfil_daemon.sh

# Bloquear trafico saliente excepto para respuesta
iptables -A OUTPUT -d 10.10.0.10 -j DROP
iptables -A OUTPUT -p udp --dport 53 -j DROP
iptables -A OUTPUT -p tcp --dport 53 -j DROP

# Desactivar scheduled tasks
crontab -r 2>/dev/null
systemctl stop cron 2>/dev/null
```

### 3.5 Verificar contencion

```bash
# Verificar que las consultas al dominio sospechoso cesaron
# En el domaincontroller
tail -f /var/log/bind/query.log | grep "exfil.attacker.com"
# No deberian aparecer nuevas consultas

# Verificar que el DNS externo esta bloqueado
# Desde cualquier maquina interna
nslookup google.com 8.8.8.8
# Deberia fallar

# Verificar que el DNS interno funciona
nslookup google.com 10.10.2.10
# Deberia funcionar
```

---

## Fase 4: Erradicacion

### 4.1 Eliminar la backdoor de la workstation

```bash
# En la workstation (10.10.2.100)
# Eliminar archivos de exfiltracion
rm -f /home/student/dns_tunnel.py
rm -f /home/student/exfil_daemon.sh
rm -f /home/student/staged_data.txt
rm -f /var/log/exfil_queries.log
rm -f /var/log/exfil_errors.log
rm -f /var/log/exfil_summary.log
rm -f /var/log/exfil_cron.log

# Eliminar scheduled tasks
crontab -r 2>/dev/null
rm -f /etc/cron.d/exfil*
rm -f /var/spool/cron/crontabs/*

# Verificar que no queden procesos
ps aux | grep -E "python|dns|tunnel"
# No deberian aparecer procesos relacionados
```

### 4.2 Verificar persistencia

```bash
# En la workstation
# Revisar todos los puntos de persistencia
crontab -l 2>/dev/null
systemctl list-unit-files | grep enabled
ls -la /etc/systemd/system/
ls -la /etc/init.d/
cat /etc/rc.local 2>/dev/null
ls -la /home/student/.bashrc
ls -la /home/student/.profile

# Buscar archivos modificados recientemente
find / -mtime -1 -type f -name "*.py" -o -name "*.sh" 2>/dev/null | grep -v proc

# Revisar historial de comandos
cat /home/student/.bash_history
cat /root/.bash_history

# Verificar que no hay claves SSH no autorizadas
ls -la /home/student/.ssh/ 2>/dev/null
cat /home/student/.ssh/authorized_keys 2>/dev/null
```

### 4.3 Restaurar configuracion DNS

```bash
# En el domaincontroller
# Eliminar la zona de exfiltracion
rm /etc/bind/zones/exfil.attacker.com.zone
rm /etc/bind/zones/negativo.exfil.attacker.com.zone

# Limpiar named.conf.local
# Eliminar las lineas agregadas para exfiltracion
sed -i '/# EXFIL SERVER/,/^};/d' /etc/bind/named.conf.local
sed -i '/# EXFIL LOGGING/,/^};/d' /etc/bind/named.conf.options

# Reiniciar DNS
systemctl restart bind9

# Verificar que el DNS funciona correctamente
nslookup bancodelsol.local 10.10.2.10
```

### 4.4 Limpiar servidor del atacante

```bash
# En el atacante (10.10.0.10)
# Eliminar zona de exfiltracion
rm /etc/bind/zones/exfil.attacker.com.zone

# Eliminar logs de exfiltracion
rm -rf /root/exfil_logs/
rm -f /root/c2_server.py
rm -f /root/c2_output.log

# Detener servidor DNS del atacante
pkill -f named

# Eliminar configuracion de zona
sed -i '/# EXFIL SERVER/,/^};/d' /etc/bind/named.conf.local
sed -i '/# EXFIL LOGGING/,/^};/d' /etc/bind/named.conf.options
```

---

## Fase 5: Recuperacion

### 5.1 Verificar que no hay exfiltracion activa

```bash
# En el domaincontroller
# Monitorear trafico DNS por 15-30 minutos
tcpdump -i any port 53 -w /var/log/traffic_captures/verification_$(date +%s).pcap &
TCPDUMP_PID=$!

sleep 900  # 15 minutos

kill $TCPDUMP_PID

# Analizar la captura de verificacion
tshark -r /var/log/traffic_captures/verification_*.pcap -Y "dns.qry.name contains exfil.attacker.com" | wc -l
# Deberia ser 0
```

### 5.2 Restaurar configuracion de red

```bash
# En la workstation
# Restaurar resolv.conf original
cat > /etc/resolv.conf << 'EOF'
nameserver 10.10.2.10
search bancodelsol.local
EOF

# Restaurar reglas de firewall
iptables -F
iptables -X
iptables -P INPUT ACCEPT
iptables -P FORWARD ACCEPT
iptables -P OUTPUT ACCEPT
```

### 5.3 Verificar integridad de datos

```bash
# En el database
# Verificar que los registros de clientes estan intactos
mysql -u admin_banco -p'B@nco$2025!Secure' banco_del_sol -e "SELECT COUNT(*) FROM clientes;"
mysql -u admin_banco -p'B@nco$2025!Secure' banco_del_sol -e "SELECT COUNT(*) FROM tarjetas_credito;"

# En el fileserver
# Verificar que los documentos estan intactos
ls -la /srv/samba/Directorio/
ls -la /srv/samba/Legal/
ls -la /srv/samba/Tecnologia/

# Verificar hashes de archivos (si se generaron previamente)
# md5sum /srv/samba/Directorio/*.pdf
```

### 5.4 Actualizar monitoreo DNS

```bash
# En el domaincontroller
# Habilitar logging avanzado de DNS si no esta activo
# Configurar alertas para consultas con subdominios largos
# Configurar alertas para consultas a dominios nuevos

# Crear script de monitoreo DNS
cat > /usr/local/bin/dns_monitor.sh << 'SCRIPT'
#!/bin/bash
# Monitor de DNS para detectar tunneling

THRESHOLD=50  # Maximo de consultas por minuto a un dominio
LONG_THRESHOLD=40  # Longitud maxima de subdominio

while true; do
    # Buscar dominios con muchas consultas
    tail -1000 /var/log/bind/query.log | \
        grep -oP '\S+\.\S+\.\S+\.\S+' | \
        sort | uniq -c | sort -rn | \
        awk -v thresh=$THRESHOLD '$1 > thresh {print "ALERTA: "$2" tiene "$1" consultas"}' | \
        mail -s "DNS Alert - Posible Tunneling" admin@bancodelsol.local 2>/dev/null
    
    sleep 60
done
SCRIPT

chmod +x /usr/local/bin/dns_monitor.sh
nohup /usr/local/bin/dns_monitor.sh &
```

---

## Fase 6: Lecciones Aprendidas

### 6.1 Resumen del incidente

**Vector de ataque:** El atacante comprometio una estacion de trabajo mediante credenciales obtenidas previamente. Utilizo DNS tunneling para exfiltrar datos sensibles de la base de datos bancaria y documentos confidenciales del servidor de archivos.

**Datos comprometidos:**
- Registros de 10 clientes (DNI, nombre, numero de cuenta, saldo)
- Datos de 5 tarjetas de credito (numero, titular, vencimiento, CVV)
- 10 transacciones bancarias
- 7 documentos confidenciales (estrategia corporativa, fusion bancaria, reduccion de personal, demanda legal, auditoria financiera, arquitectura de red, credenciales privilegiadas)

**Metodo de exfiltracion:** DNS tunneling con subdominios codificados en base64, usando registros TXT como canal de command and control.

**Duracion estimada:** 45 minutos antes de deteccion.

### 6.2 Mejores practicas de seguridad DNS

1. **Habilitar logging DNS:** Configurar logging detallado de todas las consultas DNS, incluyendo subdominios completos.

2. **Implementar DNS filtering:** Utilizar soluciones de DNS filtering (Pi-hole, Cisco Umbrella, etc.) para bloquear dominios maliciosos conocidos.

3. **Limitar resolucion DNS externa:** Forzar que todos los clientes usen el servidor DNS interno. Bloquear puertas 53 hacia el exterior.

4. **Monitorear patrones anomalos:** Implementar SIEM o reglas de alerta para:
   - Consultas con subdominios superiores a 40 caracteres
   - Mas de 100 consultas por hora al mismo dominio externo
   - Predominio de consultas TXT (mayor al 80%)
   - Consultas a dominios nuevos o poco frecuentes

5. **Implementar DNSSEC:** Para prevenir envenenamiento de cache DNS.

6. **Inspeccion profunda de DNS (DPI):** Utilizar herramientas como Zeek (Bro) o Suricata para analizar el contenido de las consultas DNS.

### 6.3 Implementacion de DLP (Data Loss Prevention)

1. **Clasificacion de datos:** Implementar clasificacion automatica de datos sensibles (DLP tags).

2. **Monitoreo de datos sensibles:** Configurar alertas cuando datos clasificados como sensibles son accedidos o transferidos.

3. **Control de acceso:** Implementar principio de minimo privilegio en el acceso a bases de datos y archivos compartidos.

4. **Cifrado de datos en reposo:** Cifrar datos sensibles en bases de datos y servidores de archivos.

5. **Auditoria de acceso:** Mantener logs detallados de acceso a datos sensibles con retencion de al menos 90 dias.

### 6.4 Controles preventivos recomendados

| Control | Prioridad | Implementacion |
|---------|-----------|----------------|
| DNS logging habilitado | Alta | Configurar inmediatamente |
| Bloqueo DNS externo | Alta | Configurar inmediatamente |
| Monitoreo de trafico DNS | Alta | Implementar en 1 semana |
| Solucion DNS filtering | Media | Implementar en 1 mes |
| DLP basico | Media | Implementar en 2 meses |
| DNSSEC | Baja | Implementar en 6 meses |
| DPI para DNS | Baja | Evaluar para proximo trimestre |

### 6.5 Documentacion del incidente

Para el reporte final del incidente, incluir:

1. **Timeline del incidente:** Desde compromiso inicial hasta erradicacion completa.
2. **Indicadores de compromiso (IoC):** IPs, dominios, hashes, patrones de trafico.
3. **Datos afectados:** Lista completa de registros y documentos comprometidos.
4. **Acciones tomadas:** Cada paso de deteccion, analisis, contencion, erradicacion y recuperacion.
5. **Mejoras implementadas:** Controles agregados para prevenir futuros incidentes.
6. **Lecciones aprendidas:** Que funciono, que no funciono, y que se puede mejorar.

---

## Comandos de referencia rapida

```bash
# DETECCION
grep "exfil.attacker.com" /var/log/bind/query.log
tshark -r capture.pcap -Y "dns.qry.name contains exfil.attacker.com"

# ANALISIS
tshark -r capture.pcap -Y "dns.qry.name contains exfil.attacker.com" -T fields -e dns.qry.name | sed 's/.exfil.attacker.com//g'

# CONTENCION
iptables -A OUTPUT -p udp --dport 53 -d 8.8.8.8 -j DROP
pkill -f dns_tunnel.py

# ERRADICACION
rm -f /home/student/dns_tunnel.py /home/student/exfil_daemon.sh
crontab -r

# RECUPERACION
systemctl restart bind9
tcpdump -i any port 53 -w verification.pcap
```
