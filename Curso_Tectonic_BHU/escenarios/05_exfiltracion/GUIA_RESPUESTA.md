# Guia de Respuesta - Escenario 05: Exfiltracion de Datos via DNS Tunneling
## Banco del Sol - Curso Tectonic BHU

---

## Fase 1: Deteccion

### 1.1 Detectar trafico DNS inusual
```bash
# Conectar a blue-team-ws
ssh blue-team-ws@blue-team-ws

# Capturar trafico DNS
sudo tcpdump -i any -nn port 53 -w /tmp/dns_detection.pcap &
TCPDUMP_PID=$!
sleep 30
kill $TCPDUMP_PID

# Analizar volumen de trafico DNS
sudo tshark -r /tmp/dns_detection.pcap -q -z io,phs

# Verificar cantidad de consultas DNS
sudo tshark -r /tmp/dns_detection.pcap | wc -l
```

### 1.2 Identificar patron de DNS tunneling
```bash
# Buscar consultas TXT (comunes en DNS tunneling)
sudo tshark -r /tmp/dns_detection.pcap -Y "dns.qry.type == 16" | head -20

# Ver subdominios largos (datos encoded)
sudo tshark -r /tmp/dns_detection.pcap -T fields -e dns.qry.name 2>/dev/null | \
  awk -F. '{print length($1), $0}' | sort -rn | head -20

# Identificar IPs que realizan muchas consultas
sudo tshark -r /tmp/dns_detection.pcap -T fields -e ip.src 2>/dev/null | \
  sort | uniq -c | sort -rn | head -10
```

### 1.3 Verificar logs de DNS
```bash
# Verificar logs de dnsmasq en attack-ws
ssh admin@attack-ws "cat /var/log/dns_tunnel.log | tail -50"

# Verificar trafico DNS en db-srv
ssh admin@db-srv "tcpdump -i any -nn port 53 -c 50 2>/dev/null | head -30"

# Verificar configuracion DNS de db-srv
ssh admin@db-srv "cat /etc/resolv.conf"
```

---

## Fase 2: Analisis

### 2.1 Decodificar trafico DNS tunneling
```bash
# Extraer subdominios de las consultas DNS
sudo tshark -r /tmp/dns_detection.pcap -T fields -e dns.qry.name 2>/dev/null | \
  grep "bancodelsol.lab" | cut -d. -f1 > /tmp/encoded_chunks.txt

# Decodificar chunks base32
while IFS= read -r chunk; do
  echo -n "$chunk" | base32 -d 2>/dev/null
done < /tmp/encoded_chunks.txt

# O usar Python para decodificar
python3 -c "
import base64
with open('/tmp/encoded_chunks.txt') as f:
    for line in f:
        try:
            decoded = base64.b32decode(line.strip() + '==')
            print(decoded.decode('utf-8', errors='ignore'), end='')
        except:
            pass
"
```

### 2.2 Identificar datos exfiltrados
```bash
# Verificar el archivo de datos en db-srv
ssh admin@db-srv "head -10 /var/data/clientes.csv"

# Contar registros
ssh admin@db-srv "wc -l /var/data/clientes.csv"

# Ver tipos de datos
ssh admin@db-srv "head -1 /var/data/clientes.csv"

# Verificar si los datos llegaron al servidor DNS
ssh admin@attack-ws "cat /opt/exfiltrated_data.txt 2>/dev/null | head -20"
```

### 2.3 Evaluar alcance de la exfiltracion
```bash
# Determinar cuantos chunks se enviaron
sudo tshark -r /tmp/dns_detection.pcap -T fields -e dns.qry.name 2>/dev/null | \
  grep "bancodelsol.lab" | wc -l

# Estimar tamano de datos exfiltrados
# Cada chunk base32 de 63 caracteres ~= 38 bytes de datos
CHUNKS=$(sudo tshark -r /tmp/dns_detection.pcap -T fields -e dns.qry.name 2>/dev/null | \
  grep "bancodelsol.lab" | wc -l)
echo "Chunks enviados: $CHUNKS"
echo "Tamano estimado: $((CHUNKS * 38)) bytes"

# Verificar si el CSV completo fue exfiltrado
CSV_SIZE=$(ssh admin@db-srv "wc -c < /var/data/clientes.csv")
echo "Tamano del CSV: $CSV_SIZE bytes"
```

---

## Fase 3: Contencion

### 3.1 Bloquear DNS tunneling en firewall
```bash
# Bloquear consultas DNS al servidor atacante
sudo iptables -A OUTPUT -p udp --dport 53 -d <IP_ATTACK_WS> -j DROP
sudo iptables -A OUTPUT -p tcp --dport 53 -d <IP_ATTACK_WS> -j DROP

# Bloquear todo el trafico DNS excepto a servidores legitimos
sudo iptables -A OUTPUT -p udp --dport 53 -d <DNS_LEGITIMO> -j ACCEPT
sudo iptables -A OUTPUT -p udp --dport 53 -j DROP

# Guardar reglas
sudo iptables-save > /etc/iptables/rules.v4
sudo iptables -L -v -n
```

### 3.2 Aislar db-srv
```bash
# Aislar db-srv de la red
ssh admin@db-srv "sudo iptables -A OUTPUT -j DROP"
ssh admin@db-srv "sudo iptables -I OUTPUT -d <IP_BLUE_TEAM> -p tcp --dport 22 -j ACCEPT"

# Verificar aislamiento
ssh admin@db-srv "sudo iptables -L -v -n"

# Matar procesos de tunneling
ssh admin@db-srv "pkill -f iodine"
ssh admin@db-srv "pkill -f dns"
```

### 3.3 Detener servidor DNS atacante
```bash
# Detener dnsmasq y servidor DNS tunneling
ssh admin@attack-ws "sudo systemctl stop dnsmasq"
ssh admin@attack-ws "pkill -f dnscat2"
ssh admin@attack-ws "pkill -f dns_tunnel"

# Verificar que el servidor DNS se detuvo
ssh admin@attack-ws "sudo systemctl status dnsmasq"
```

---

## Fase 4: Evaluar Alcance

### 4.1 Determinar que datos fueron exfiltrados
```bash
# Leer el archivo CSV completo
ssh admin@db-srv "cat /var/data/clientes.csv"

# Contar registros comprometidos
ssh admin@db-srv "tail -n +2 /var/data/clientes.csv | wc -l"

# Identificar tipos de datos
echo "=== Tipos de datos comprometidos ==="
echo "- CEDULAS: Datos de identificacion personal"
echo "- NOMBRES: Nombres completos"
echo "- EMAILS: Direcciones de correo"
echo "- TELEFONOS: Numeros de telefono"
echo "- DIRECCIONES: Direcciones fisicas"
echo "- NUMEROS DE CUENTA: Informacion bancaria"
echo "- SALDOS: Informacion financiera"
```

### 4.2 Identificar personas afectadas
```bash
# Extraer lista de cedulas comprometidas
ssh admin@db-srv "tail -n +2 /var/data/clientes.csv | cut -d, -f1" > /tmp/cedulas_comprometidas.txt

# Contar personas afectadas
wc -l /tmp/cedulas_comprometidas.txt

# Verificar si hay datos adicionales
ssh admin@db-srv "ls -la /var/data/"
ssh admin@db-srv "find /var/data -name '*.csv' -o -name '*.txt' -o -name '*.db'"
```

---

## Fase 5: Reporte

### 5.1 Plantilla de notificacion a URCDP (72 horas)

```
NOTIFICACION DE INCIDENTE DE SEGURIDAD
Banco del Sol - URCDP

Fecha de notificacion: [Fecha]
Plazo: 72 horas desde la deteccion

1. DESCRIPCION DEL INCIDENTE
   Tipo: Exfiltracion de datos via DNS Tunneling
   Fecha: [Fecha del incidente]
   Duracion: [Duracion estimada]

2. DATOS PERSONALES AFECTADOS
   - Cantidad de registros: 100 registros de clientes
   - Tipos de datos:
     * CEDULAS (identificacion personal)
     * NOMBRES COMPLETOS
     * DIRECCIONES DE CORREO ELECTRONICO
     * NUMEROS DE TELEFONO
     * DIRECCIONES POSTALES
     * NUMEROS DE CUENTA BANCARIA
     * SALDOS CUENTAS

3. MECANISMO DEL ATAQUE
   - Exfiltracion via DNS tunneling
   - Datos codificados en consultas DNS TXT
   - Servidor atacante: [IP]

4. PERSONAS AFECTADAS
   - Clientes del banco: 100 personas
   - Empleados: 0

5. MEDIDAS DE PROTECCION
   - Bloqueo del canal de exfiltracion
   - Aislamiento del servidor comprometido
   - Cambio de credenciales
   - Monitoreo de usos indebidos

6. CONTACTO
   Responsable: [Nombre]
   Email: [Email]
   Telefono: [Telefono]

========================================
```

### 5.2 Plantilla de reporte a CERTuy

```
========================================
REPORTE DE INCIDENTE DE SEGURIDAD
Banco del Sol - Incidente #005
========================================

FECHA DEL INCIDENTE: [Fecha]
HORA DE DETECCION: [Hora]
HORA DE CONTENCION: [Hora]

RESUMEN:
Exfiltracion de datos sensibles de 100 clientes via DNS tunneling.
El atacante utilizo consultas DNS para exfiltrar cedulas, nombres,
emails, telefonos, direcciones, numeros de cuenta y saldos.

METODO DE ATAQUE:
- Tunneling via consultas DNS TXT
- Datos codificados en base32
- Servidor DNS controlado por atacante

DATOS COMPROMETIDOS:
- 100 registros de clientes
- Tipos: cedulas, nombres, emails, telefonos, direcciones,
  numeros de cuenta, saldos

IMPACTO:
- 100 clientes potencialmente afectados
- Riesgo de fraude e identidad
- Obligacion de notificacion URCDP

ACCIONES TOMADAS:
1. Bloqueo del canal de exfiltracion
2. Aislamiento del servidor comprometido
3. Preservacion de evidencia
4. Notificacion a URCDP (72 horas)

========================================
```

---

## Fase 6: Prevencion

### 6.1 Implementar filtrado DNS
```bash
# Configurar DNS filtering en el firewall
# Bloquear consultas a DNS servers no autorizados
sudo iptables -A OUTPUT -p udp --dport 53 -d <DNS_AUTORIZADO> -j ACCEPT
sudo iptables -A OUTPUT -p udp --dport 53 -j DROP

# Implementar DNS over HTTPS blocking
sudo iptables -A OUTPUT -p tcp --dport 443 -d <DOH_SERVERS> -j DROP
```

### 6.2 Monitoreo de seguridad DNS
```bash
# Implementar monitoreo de volumen DNS
# Alertar si hay mas de X consultas por minuto
# Implementar deteccion de subdominios largos
# Monitorear consultas TXT inusuales
```

### 6.3 Prevencion de perdida de datos
```bash
# Implementar DLP (Data Loss Prevention)
# Cifrar datos sensibles en reposo
# Implementar segmentacion de red
# Monitorear acceso a datos sensibles
```

### 6.4 Herramientas utilizadas
- tcpdump (captura de trafico)
- tshark (analisis de trafico)
- base32/base64 (decodificacion)
- iptables (contencion)
- dnsmasq/iodine (simulacion del ataque)

### 6.5 Tiempos de respuesta
| Fase | Tiempo Objetivo | Tiempo Real |
|------|----------------|-------------|
| Deteccion | < 30 minutos | [Medir] |
| Analisis | < 2 horas | [Medir] |
| Contencion | < 4 horas | [Medir] |
| Evaluacion | < 8 horas | [Medir] |
| Reporte URCDP | < 72 horas | [Medir] |
| Reporte CERTuy | < 24 horas | [Medir] |
