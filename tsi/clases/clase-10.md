# Clase 10: Seguridad en Redes - Firewalls, IDS/IPS, VLANs y Zero Trust

**Duracion:** 2 horas

---

## Objetivos de Aprendizaje

1. Comprender y configurar firewalls (packet filter, stateful, NGFW) y disenar reglas de filtrado
2. Disenar segmentacion de red con VLANs para aislar trafico por departamentos y reducir la superficie de ataque
3. Explicar el funcionamiento de IDS/IPS (Snort/Suricata) y escribir reglas de deteccion basicas
4. Comprender los fundamentos del modelo Zero Trust (ZTNA) y su diferencia con la seguridad tradicional basada en perimetro

---

## Contenido Detallado

### 1. Firewalls - Primera linea de defensa

#### Que es un firewall?

Un firewall es un sistema de seguridad que controla el trafico de red entrante y saliente basandose en reglas predefinidas. Actua como una barrera entre una red de confianza (interna) y una red no confiable (Internet).

**Analogía:** Un firewall es como el seguridad de un edificio. Revisa a todos los que entran y salen: verifica su identificacion (IP, puerto), revisa que llevan (contenido del paquete), y decide si los deja pasar o no (permitir/denegar). Sin el seguridad, cualquiera podria entrar.

**Que puede hacer un firewall:**
- Permitir o bloquear trafico segun IP origen/destino, puerto, y protocolo
- Mantener estado de las conexiones (saber si un paquete pertenece a una conexion establecida)
- Inspeccionar el contenido de los paquetes en niveles superiores
- Registrar (log) todo el trafico para auditoria

#### Tipos de firewalls

**1. Packet Filter (Filtro de paquetes):**
Es el tipo mas basico. Analiza solo las cabeceras de los paquetes (IP origen, IP destino, puerto, protocolo). No entiende el contexto de la conexion ni el contenido.

Como funciona:
```
Paquete entrante:
  - IP origen: 10.0.0.1
  - Puerto origen: 12345
  - IP destino: 192.168.1.10
  - Puerto destino: 80
  - Protocolo: TCP

Regla: Permitir trafico desde cualquier IP hacia 192.168.1.10:80
Resultado: PERMITIDO (coincide con la regla)
```

Ejemplo: iptables (Linux), ACLs en routers Cisco.

**2. Stateful Firewall (Firewall con estado):**
Mantiene una tabla de estado que registra las conexiones activas. No solo evalua cada paquete individualmente, sino que entiende si pertenece a una conexion establecida.

Como funciona:
```
1. Cliente (10.0.0.1:12345) -> Servidor (192.168.1.10:80) SYN
   Firewall crea entrada en tabla de estado:
     [10.0.0.1:12345 - 192.168.1.10:80] ESTABLECIENDOSE

2. Servidor (192.168.1.10:80) -> Cliente (10.0.0.1:12345) SYN-ACK
   Firewall busca en tabla de estado:
     Encuentra la entrada -> PERMITIDO (es respuesta a conexion existente)

3. Cliente (10.0.0.1:12345) -> Servidor (192.168.1.10:80) ACK
   Firewall actualiza estado:
     [10.0.0.1:12345 - 192.168.1.10:80] ESTABLECIDA

4. Paquete entrante al azar (5.5.5.5 -> 192.168.1.10:80) SYN
   Firewall busca en tabla de estado:
     No encuentra entrada -> DENEGADO (nadie interno inicio esta conexion)
```

Ventaja: Mas seguro que packet filter porque entiende el flujo de la comunicacion.
Ejemplo: Firewalls modernos como Windows Defender Firewall, iptables con conntrack.

**3. Application Layer / Proxy Firewall:**
No solo filtra paquetes, sino que inspecciona el contenido de la aplicacion. Funciona como intermediario (proxy): el cliente se conecta al proxy, y el proxy se conecta al destino.

```
Cliente -> Proxy Firewall -> Servidor
           (inspecciona HTTP, SSL, etc.)
```

Puede:
- Bloquear tipos de archivos especificos (.exe, .zip)
- Inspeccionar SSL (descifrar y re-cifrar)
- Filtrar por URL o categoria web
- Detectar malware en el contenido

**4. Next-Generation Firewall (NGFW):**
Combina todas las capacidades anteriores mas:
- IDS/IPS integrado
- Inspeccion SSL/TLS
- Filtrado por aplicacion (no solo por puerto: reconoce "Facebook" aunque use puerto 443)
- Sandboxing (ejecuta archivos en un entorno aislado para analizarlos)
- Antivirus integrado
- Inteligencia de amenazas (actualizaciones en vivo de IoCs)

Ejemplos: Palo Alto Networks, Fortinet FortiGate, Check Point.

#### Reglas de firewall

Las reglas se evaluan en orden. La primera regla que coincide determina la accion (allow/deny). Si ninguna regla coincide, generalmente se aplica una regla por defecto (denegar todo).

**Formato tipico de una regla:**

| Orden | Accion | Origen | Destino | Puerto | Protocolo | Descripcion |
|---|---|---|---|---|---|---|
| 1 | ALLOW | 192.168.1.0/24 | 192.168.10.10 | 22 | TCP | Permitir SSH a servidor |
| 2 | ALLOW | 192.168.1.0/24 | 192.168.10.10 | 80,443 | TCP | Permitir web a servidor |
| 3 | DENY | any | 192.168.10.10 | any | any | Bloquear todo lo demas |
| 4 | ALLOW | any | any | 53 | UDP | Permitir DNS saliente |

**Regla de oro del firewall:**
- Regla implicita al final: DENY ALL (denegar todo lo que no este explicitamente permitido)
- Esto se llama "principio de minimo privilegio": solo se permite lo necesario

#### DMZ (Zona Desmilitarizada)

La DMZ es un segmento de red separado que contiene servidores accesibles desde Internet (web, email, DNS) pero aislados de la red interna.

**Arquitectura clasica:**

```
                    INTERNET
                       |
              [FIREWALL EXTERNO]
               (Permite HTTP, HTTPS,
                SMTP, DNS hacia DMZ)
                       |
              [ZONA DMZ]
               - Servidor Web
               - Servidor Mail
               - Servidor DNS
                       |
              [FIREWALL INTERNO]
               (Solo permite conexiones
                iniciadas desde red interna)
                       |
              [RED INTERNA]
               - PCs empleados
               - Servidores internos
               - Bases de datos
```

**Regla de oro de la DMZ:** Si un atacante compromete un servidor en la DMZ, NO debe poder acceder a la red interna desde ahi. La DMZ es una zona de confianza intermedia: mas segura que Internet pero menos que la red interna.

#### Ejemplo: Reglas iptables en Linux

iptables es el firewall de linea de comandos en Linux. Controla el trafico a traves de cadenas (chains): INPUT (paquetes entrantes), OUTPUT (salientes), FORWARD (reenviados).

**Reglas basicas:**

```bash
# Limpiar reglas existentes
iptables -F
iptables -X

# Politica por defecto: DENEGAR todo
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT

# Permitir trafico de loopback (localhost)
iptables -A INPUT -i lo -j ACCEPT

# Permitir trafico de conexiones establecidas (stateful)
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# Permitir SSH desde red interna
iptables -A INPUT -s 192.168.1.0/24 -p tcp --dport 22 -j ACCEPT

# Permitir HTTP y HTTPS (servidor web)
iptables -A INPUT -p tcp --dport 80 -j ACCEPT
iptables -A INPUT -p tcp --dport 443 -j ACCEPT

# Permitir DNS saliente (respuestas)
iptables -A INPUT -p udp --sport 53 -j ACCEPT

# Permitir ICMP (ping) limitado
iptables -A INPUT -p icmp --icmp-type echo-request -m limit --limit 10/second -j ACCEPT

# Registrar (log) paquetes denegados
iptables -A INPUT -j LOG --log-prefix "FW-DENIED: " --log-level 4

# Bloquear todo lo demas (por defecto ya esta DROP)
```

**Explicacion:**
- `-A INPUT`: Agrega regla a la cadena INPUT (paquetes destinados a este equipo)
- `-s`: IP origen
- `-p tcp --dport 22`: Protocolo TCP, puerto destino 22
- `-j ACCEPT`: Accion (aceptar)
- `-m state --state ESTABLISHED,RELATED`: Permite respuestas a conexiones que nosotros iniciamos

### 2. Segmentacion con VLANs

#### Repaso de VLANs

Las VLANs (Virtual LANs) permiten dividir un switch fisico en multiples redes logicas. Dispositivos en diferentes VLANs no pueden comunicarse directamente; necesitan un router (o switch de capa 3) para hacerlo.

**Analogia:** Un switch con VLANs es como un edificio de departamentos. Todos comparten la misma estructura fisica (el edificio), pero cada departamento (VLAN) esta separado. Los vecinos del departamento 10 no pueden entrar al departamento 20 sin pasar por la puerta principal (el router).

#### Beneficios de seguridad de las VLANs

1. **Aislamiento de trafico:** Un atacante en la VLAN de invitados no puede ver el trafico de la VLAN de administracion
2. **Reduccion de superficie de ataque:** Si un equipo en VLAN Ventas es comprometido, solo afecta a VLAN Ventas
3. **Contencion de broadcasts:** Los ataques de broadcast (como broadcast storms) quedan limitados a una VLAN
4. **Control de acceso granulado:** A traves de reglas de firewall entre VLANs
5. **Segmentacion por confianza:** Equipos de confianza (IT, servidores) vs equipos no confiables (invitados, IoT)

#### Diseno de segmentacion VLAN para una empresa

| VLAN ID | Nombre | Subred | Dispositivos | Nivel de confianza |
|---|---|---|---|---|
| 10 | Admin-Gerencia | 10.0.10.0/24 | PCs de administracion y gerencia | Alto |
| 20 | IT-Sistemas | 10.0.20.0/24 | PCs de IT, administradores | Muy alto |
| 30 | Ventas | 10.0.30.0/24 | PCs del departamento de ventas | Medio |
| 40 | RRHH | 10.0.40.0/24 | PCs de recursos humanos | Alto (datos sensibles) |
| 50 | Invitados | 10.0.50.0/24 | WiFi para visitas, dispositivos personales | Bajo (solo Internet) |
| 60 | IoT | 10.0.60.0/24 | Camaras, sensores, impresoras | Bajo |
| 70 | Servidores Internos | 10.0.70.0/24 | Servidores AD, archivos, BD | Muy alto |
| 80 | DMZ | 10.0.80.0/24 | Servidores publicos (web, mail) | Intermedio |
| 99 | Gestion | 10.0.99.0/24 | Switches, APs (acceso por SSH/HTTPS) | Critico |

#### Router-on-a-stick

Cuando solo tienes UN cable entre el router y el switch, puedes configurar "router-on-a-stick": el puerto del switch hacia el router es un trunk (802.1Q) que lleva todas las VLANs, y el router tiene subinterfaces virtuales (una por VLAN).

**Configuracion en switch Cisco:**
```
Switch(config)# vlan 10
Switch(config-vlan)# name Admin
Switch(config)# vlan 20
Switch(config-vlan)# name Ventas
Switch(config)# interface fastethernet 0/1
Switch(config-if)# switchport mode access
Switch(config-if)# switchport access vlan 10
Switch(config)# interface fastethernet 0/2
Switch(config-if)# switchport mode access
Switch(config-if)# switchport access vlan 20
Switch(config)# interface fastethernet 0/24
Switch(config-if)# switchport mode trunk  (puerto al router)
```

**Configuracion en router Cisco:**
```
Router(config)# interface fastethernet 0/0.10
Router(config-subif)# encapsulation dot1Q 10
Router(config-subif)# ip address 10.0.10.1 255.255.255.0
Router(config)# interface fastethernet 0/0.20
Router(config-subif)# encapsulation dot1Q 20
Router(config-subif)# ip address 10.0.20.1 255.255.255.0
```

### 3. IDS/IPS (Intrusion Detection/Prevention Systems)

#### Diferencia entre IDS y IPS

| Caracteristica | IDS | IPS |
|---|---|---|
| Posicion en la red | Pasivo (copia del trafico) | Activo (en linea) |
| Accion al detectar | Alerta, registra en log | Alerta Y bloquea |
| Impacto en la red | Ninguno (no toca el trafico) | Puede afectar (si bloquea trafico legitimo) |
| Falsos positivos | Menos problema (solo alerta) | Problema: puede bloquear trafico legitimo |
| Ubicacion tipica | Puerto SPAN (mirror) del switch | Entre el firewall y la LAN |

**Analogia:** El IDS es una camara de seguridad: solo graba y alerta si ve algo sospechoso. El IPS es un guardia de seguridad que te detiene en la puerta.

#### Metodos de deteccion

**1. Deteccion por firmas (Signature-based):**
Busca patrones conocidos de ataques. Similar a un antivirus.

```
Regla: Busca la cadena "'; DROP TABLE" en trafico HTTP
Si encuentra: ALERTA (posible SQL injection)
```

Ventaja: Muy preciso, pocos falsos positivos para ataques conocidos.
Desventaja: No detecta ataques nuevos (zero-day) o variantes.

**2. Deteccion por anomalia (Anomaly-based):**
Establece una linea base de comportamiento normal y alerta cuando hay desviaciones.

```
Linea base: El servidor web recibe 100-200 peticiones/minuto
Evento: El servidor web recibe 10000 peticiones/minuto
Alerta: POSIBLE DDoS
```

Ventaja: Puede detectar ataques nuevos.
Desventaja: Muchos falsos positivos (cambios legitimos en el trafico).

**3. Deteccion heuristica:**
Combina tecnicas y analiza comportamiento sospechoso, como un intento de escaneo de puertos:
```
Evento: Host X envia SYN a 50 puertos diferentes en 5 segundos
Accion: ALERTA (posible port scan)
```

#### Herramientas IDS/IPS gratuitas

**Snort:** El IDS/IPS gratuito mas popular. Usa reglas para detectar trafico malicioso.
```
Descarga: https://www.snort.org/
Windows: Instalador .exe
Linux: apt install snort
```

**Regla Snort basica:**
```
alert tcp any any -> any 80 (msg:"SQL Injection"; content:"' OR"; sid:1000001; rev:1;)
```

Partes de la regla:
- `alert`: Accion (alertar)
- `tcp any any -> any 80`: Protocolo, IP origen, puerto origen -> IP destino, puerto destino
- `msg`: Mensaje que se mostrara en la alerta
- `content`: Patron a buscar en el payload
- `sid`: Identificador unico de la regla
- `rev`: Revision de la regla

**Suricata:** Similar a Snort pero mas moderno, usa multi-threading, soporta HTTP/2, TLS 1.3.
```
apt install suricata
```

**Zeek (antes Bro):** No es exactamente IDS/IPS sino un framework de monitoreo de red. Genera logs estructurados de todo el trafico.

#### Ubicacion del IDS/IPS en la red

```
INTERNET
    |
[FIREWALL EXTERNO]
    |
[IPS EN LINEA]   <-- aqui bloquea
    |
[SWITCH] ----- [PUERTO SPAN] ----- [IDS]   <-- aqui solo monitorea
    |
  [LAN]
```

### 4. VPN (Virtual Private Networks)

Una VPN crea un tunel cifrado entre dos puntos a traves de una red no confiable (Internet). El trafico viaja encriptado y nadie puede interceptarlo.

#### Tipos de VPN

**Site-to-Site:** Conecta dos oficinas completas. Ej: Oficina Buenos Aires <-> Oficina Montevideo.

```
[Oficina BA] -----[Internet: tunel IPsec]----- [Oficina MVD]
  PC1                              PC2
  VPN Gateway (router/firewall)    VPN Gateway (router/firewall)
```

**Remote Access:** Un empleado se conecta desde su casa a la oficina.

```
[Empleado en casa] -----[Internet: tunel OpenVPN]----- [Oficina]
  Laptop                                       VPN Server
```

#### Protocolos VPN

| Protocolo | Puertos | Cifrado | Velocidad | Seguridad |
|---|---|---|---|---|
| IPsec IKEv2 | UDP 500, 4500 | AES-256 | Alta | Muy alta |
| OpenVPN | UDP 1194 / TCP 443 | AES-256 | Media | Muy alta |
| WireGuard | UDP 51820 | ChaCha20 | Muy alta | Alta |
| PPTP | TCP 1723 | MPPE-128 | Alta | MUY BAJA (no usar) |
| L2TP/IPsec | UDP 1701 | AES-256 | Media | Alta |

**Recomendacion:** Usar OpenVPN o WireGuard para acceso remoto. WireGuard es mas moderno, rapido y simple.

#### Ejemplo: Configurar servidor OpenVPN basico en Linux

```bash
# Instalar OpenVPN en Ubuntu Server
sudo apt update
sudo apt install openvpn easy-rsa -y

# Configurar la autoridad certificadora (CA)
make-cadir ~/easy-rsa
cd ~/easy-rsa
./easyrsa init-pki
./easyrsa build-ca nopass

# Generar certificado del servidor
./easyrsa gen-req server nopass
./easyrsa sign-req server server

# Generar certificado del cliente
./easyrsa gen-req client1 nopass
./easyrsa sign-req client client1

# Generar Diffie-Hellman params
./easyrsa gen-dh

# Copiar certificados
sudo cp pki/ca.crt pki/issued/server.crt pki/private/server.key pki/dh.pem /etc/openvpn/

# Configuracion del servidor (server.conf)
sudo nano /etc/openvpn/server.conf
```

Contenido de server.conf:
```
port 1194
proto udp
dev tun
ca ca.crt
cert server.crt
key server.key
dh dh.pem
server 10.8.0.0 255.255.255.0
push "redirect-gateway def1 bypass-dhcp"
push "dhcp-option DNS 8.8.8.8"
keepalive 10 120
cipher AES-256-CBC
user nobody
group nogroup
persist-key
persist-tun
status openvpn-status.log
verb 3
```

```bash
# Habilitar IP forwarding y NAT
sudo sysctl -w net.ipv4.ip_forward=1
sudo iptables -t nat -A POSTROUTING -s 10.8.0.0/24 -o eth0 -j MASQUERADE

# Iniciar servidor
sudo systemctl start openvpn@server
sudo systemctl enable openvpn@server
```

### 5. Network Access Control (NAC)

NAC controla que dispositivos pueden conectarse a la red corporativa.

#### 802.1X: Autenticacion por puerto

Estandar IEEE que requiere autenticacion antes de permitir trafico en un puerto del switch.

**Como funciona:**
1. Un PC se conecta al switch
2. El switch bloquea todo el trafico excepto EAP (Extensible Authentication Protocol)
3. El PC envia credenciales (usuario y contrasena, o certificado)
4. El switch consulta a un servidor RADIUS (ej: FreeRADIUS, Windows NPS)
5. Si las credenciales son correctas: el switch abre el puerto, el PC tiene acceso
6. Si no: el puerto permanece bloqueado

**Componentes:**
- **Supplicant:** El cliente (PC, laptop) que solicita acceso
- **Authenticator:** El switch o AP que controla el acceso
- **Authentication Server:** Servidor RADIUS que valida credenciales

### 6. Zero Trust Network Access (ZTNA)

Zero Trust es un modelo de seguridad que asume que nadie es de confianza, ni siquiera dentro de la red corporativa.

**Lema:** "Never trust, always verify" (Nunca confies, siempre verifica).

#### Principios de Zero Trust

1. **Verificar cada solicitud:** Cada peticion de acceso se evalua como si viniera de Internet abierto, sin importar donde se origina
2. **Acceso con minimos privilegios:** Solo se da acceso a los recursos estrictamente necesarios para cada tarea
3. **Microsegmentacion:** La red se divide en segmentos muy pequenos (incluso por aplicacion), no solo por VLANs
4. **Autenticacion continua:** No basta con autenticarse al inicio; cada solicitud se re-autentica
5. **Monitoreo constante:** Todo el trafico se registra y analiza en busca de anomalias

#### Diferencias con el modelo tradicional

| Modelo Tradicional (Perimetro) | Modelo Zero Trust |
|---|---|
| "Confianza implicita dentro de la red" | "Confianza cero, verificar siempre" |
| Firewall en el perimetro (castillo con foso) | Micro-firewalls entre cada servicio |
| Una vez dentro, acceso a casi todo | Cada acceso se evalua individualmente |
| VPN para acceso remoto | Acceso directo a la aplicacion, no a la red |
| Segmentacion por VLANs | Microsegmentacion por identidad y aplicacion |
| La autenticacion es al inicio | Autenticacion continua |

**Analogía:** El modelo tradicional es un castillo medieval: un muro exterior fuerte, pero una vez dentro, puedes ir a cualquier habitacion. Zero Trust es un edificio moderno: cada puerta tiene su propio lector de tarjetas, y necesitas autorizacion especifica para cada area, incluso si ya estas dentro del edificio.

#### Ejemplo: Google BeyondCorp

Google implemento Zero Trust (BeyondCorp) eliminando la VPN corporativa. En su lugar:
- Cada empleado accede a las aplicaciones internas directamente desde Internet
- El acceso se basa en: identidad del usuario, dispositivo, ubicacion, y contexto
- No importa si estas en la oficina o en un cafe: la verificacion es la misma

**Como implementar Zero Trust paso a paso:**
1. **Identificar:** Mapear todos los recursos (aplicaciones, datos, servicios)
2. **Inventariar:** Saber que usuarios y dispositivos acceden a que
3. **Definir politicas:** Quien puede acceder a que, desde donde, con que dispositivo
4. **Implementar control de acceso:** Microsegmentacion, autenticacion por aplicacion
5. **Monitorear continuamente:** Registrar cada acceso y detectar anomalias

### 7. Monitoreo de red

#### NetFlow/sFlow

Estadisticas de trafico que los switches y routers pueden exportar:
- IPs origen y destino
- Puertos
- Protocolo
- Cantidad de bytes y paquetes
- Timestamps de inicio y fin

**Para que sirve:** Identificar quien consume mas ancho de banda, detectar trafico anomalo, planificar capacidad.

#### SNMP (Simple Network Management Protocol)

Protocolo para monitorear y gestionar dispositivos de red:
- `snmpget`: Obtener un valor especifico (ej: temperatura del switch)
- `snmpwalk`: Obtener todos los valores de una rama OID
- `snmptrap`: El dispositivo envia alertas automaticas (ej: enlace caido)

**Herramientas:** PRTG, Cacti, Zabbix, LibreNMS.

#### SIEM (Security Information and Event Management)

Sistema que centraliza logs de multiples fuentes (firewalls, servidores, aplicaciones) y los correlaciona para detectar incidentes.

```
Fuentes:
  - Firewalls (logs de trafico)
  - Servidores (logs de autenticacion)
  - IDS/IPS (alertas)
  - Aplicaciones (errores, accesos)
        |
        v
  [SIEM]
   Recibe, normaliza, correlaciona
        |
        v
  Alertas, dashboards, reportes
```

**Herramientas gratuitas:** Wazuh, ELK Stack (Elasticsearch, Logstash, Kibana), Splunk Free.

#### Wireshark - Captura de paquetes

Wireshark captura todo el trafico que pasa por una interfaz de red y permite analizar paquete por paquete.

```
apt install wireshark
```
Filtros utiles:
- `ip.addr == 192.168.1.10`: Solo trafico de esa IP
- `tcp.port == 80`: Solo trafico HTTP
- `http.request`: Solo peticiones HTTP
- `arp`: Solo paquetes ARP
- `icmp`: Solo pings

### 8. Buenas practicas de seguridad en redes

1. **Cambiar credenciales por defecto:** Todo equipo nuevo viene con admin/admin o similar. Cambiarlo inmediatamente.
2. **Deshabilitar servicios no necesarios:** Si un servidor no necesita FTP, apagalo. Menos servicios = menos superficie de ataque.
3. **Mantener firmware actualizado:** Los parches de seguridad corrigen vulnerabilidades conocidas.
4. **Segmentar redes:** Usar VLANs y DMZ para separar niveles de confianza.
5. **Monitorear y auditar:** No puedes proteger lo que no ves. Implementa monitoreo continuo.
6. **Tener plan de respuesta a incidentes:** Saber que hacer cuando ocurra una brecha (no "si" ocurre, sino "cuando").
7. **Principio de minimo privilegio:** Cada usuario y servicio debe tener solo los permisos minimos necesarios.
8. **Cifrar todo lo que se pueda:** HTTPS, SSH, VPN, WPA3, cifrado de discos.
9. **Respaldar configuraciones:** Tener backups de configuraciones de switches, routers y firewalls.
10. **Documentar:** Sin documentacion, es imposible mantener la seguridad a largo plazo.

### 9. Ejercicio 1 - Reglas de firewall (iptables)

**Enunciado:** Escribir 10 reglas de firewall iptables para una PYME con los siguientes requisitos:
- Permitir SSH desde la red interna (192.168.1.0/24)
- Permitir HTTP y HTTPS al servidor web en DMZ (10.0.80.10)
- Permitir DNS saliente (consultas a resolvers externos)
- Permitir correo saliente (SMTP al puerto 587)
- Permitir respuestas a conexiones establecidas
- Bloquear todo lo demas (politica por defecto DENY)

##### Solucion

```bash
#!/bin/bash
# ==============================================
# FIREWALL RULES - PYME
# iptables ruleset basico
# ==============================================

# --- 1. Limpiar reglas existentes ---
iptables -F              # Flush filter table
iptables -t nat -F       # Flush nat table
iptables -X              # Delete custom chains
iptables -t nat -X

# --- 2. Establecer politicas por defecto ---
iptables -P INPUT DROP      # Denegar todo lo entrante
iptables -P FORWARD DROP    # Denegar todo lo reenviado
iptables -P OUTPUT ACCEPT   # Permitir todo lo saliente

# --- 3. Permitir trafico de loopback ---
iptables -A INPUT -i lo -j ACCEPT

# --- 4. Permitir respuestas a conexiones establecidas (stateful) ---
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# --- 5. Permitir SSH desde red interna ---
iptables -A INPUT -s 192.168.1.0/24 -p tcp --dport 22 -j ACCEPT

# --- 6. Permitir HTTP y HTTPS al servidor web en DMZ ---
iptables -A FORWARD -d 10.0.80.10 -p tcp --dport 80 -j ACCEPT
iptables -A FORWARD -d 10.0.80.10 -p tcp --dport 443 -j ACCEPT

# --- 7. Permitir trafico de retorno desde DMZ (respuestas) ---
iptables -A FORWARD -s 10.0.80.10 -m state --state ESTABLISHED,RELATED -j ACCEPT

# --- 8. Permitir DNS saliente (consultas UDP a resolvers externos) ---
iptables -A FORWARD -p udp --dport 53 -j ACCEPT
iptables -A FORWARD -p tcp --dport 53 -j ACCEPT

# --- 9. Permitir correo saliente (SMTP autenticado, puerto 587) ---
iptables -A FORWARD -p tcp --dport 587 -j ACCEPT

# --- 10. Permitir trafico desde red interna hacia Internet ---
iptables -A FORWARD -s 192.168.1.0/24 -m state --state NEW,ESTABLISHED -j ACCEPT

# --- Registrar intentos denegados (logging) ---
iptables -A INPUT -j LOG --log-prefix "FW-INPUT-DROP: " --log-level 4
iptables -A FORWARD -j LOG --log-prefix "FW-FORWARD-DROP: " --log-level 4

# --- Guardar reglas (persistencia en Debian/Ubuntu) ---
iptables-save > /etc/iptables/rules.v4

echo "Reglas de firewall aplicadas correctamente."
```

**Explicacion de cada regla:**

| Regla | Explicacion |
|---|---|
| 1-2 | Limpiamos reglas anteriores y establecemos DROP por defecto (principio de minimo privilegio) |
| 3 | loopback (127.0.0.1) siempre permitido, necesario para servicios locales |
| 4 | Regla stateful: permite paquetes que sean respuestas a conexiones que nosotros iniciamos |
| 5 | SSH solo desde la red interna, no desde Internet |
| 6-7 | Permite trafico hacia el servidor web en DMZ y las respuestas de vuelta |
| 8 | Permite consultas DNS hacia resolvers externos (puerto 53 UDP y TCP) |
| 9 | Permite envio de correo (SMTP autenticado en puerto 587) |
| 10 | Permite que la red interna navegue por Internet |
| Log | Registra intentos denegados para auditoria |

### 10. Ejercicio 2 - Diseno de segmentacion VLAN

**Enunciado:** Disenar la segmentacion VLAN completa para una empresa con:
- 4 departamentos: Ventas (20 personas), RRHH (5 personas), IT (8 personas), Gerencia (3 personas)
- Servidores internos: Active Directory, servidor de archivos
- Servidores publicos: servidor web, servidor de correo
- Red para invitados (WiFi)
- Cada departamento debe estar en su propia VLAN con su propia subred
- Los servidores publicos deben estar en DMZ
- Los servidores internos deben estar en una VLAN separada
- La administracion de equipos de red debe estar en una VLAN de gestion

Asignar IDs de VLAN, subredes, y explicar las reglas de firewall entre VLANs.

##### Solucion

**Paso 1: Disenar el esquema de VLANs**

Usaremos el rango 10.0.0.0/16 para toda la organizacion (suficiente para crecimiento).

| VLAN ID | Nombre | Subred | Mascara | Hosts | Gateway |
|---|---|---|---|---|---|
| 10 | Ventas | 10.0.10.0/24 | 255.255.255.0 | 254 | 10.0.10.1 |
| 20 | RRHH | 10.0.20.0/24 | 255.255.255.0 | 254 | 10.0.20.1 |
| 30 | IT | 10.0.30.0/24 | 255.255.255.0 | 254 | 10.0.30.1 |
| 40 | Gerencia | 10.0.40.0/24 | 255.255.255.0 | 254 | 10.0.40.1 |
| 50 | Invitados | 10.0.50.0/24 | 255.255.255.0 | 254 | 10.0.50.1 |
| 60 | Servidores Internos | 10.0.60.0/24 | 255.255.255.0 | 254 | 10.0.60.1 |
| 70 | DMZ | 10.0.70.0/24 | 255.255.255.0 | 254 | 10.0.70.1 |
| 99 | Gestion | 10.0.99.0/24 | 255.255.255.0 | 254 | 10.0.99.1 |

**Paso 2: Asignacion de IPs por dispositivo**

| Dispositivo | VLAN | IP | Comentario |
|---|---|---|---|
| Router (subif .10) | 10 Ventas | 10.0.10.1 | Gateway VLAN 10 |
| Router (subif .20) | 20 RRHH | 10.0.20.1 | Gateway VLAN 20 |
| Router (subif .30) | 30 IT | 10.0.30.1 | Gateway VLAN 30 |
| Router (subif .40) | 40 Gerencia | 10.0.40.1 | Gateway VLAN 40 |
| Router (subif .50) | 50 Invitados | 10.0.50.1 | Gateway VLAN 50 |
| Router (subif .60) | 60 Servidores Int | 10.0.60.1 | Gateway VLAN 60 |
| Router (subif .70) | 70 DMZ | 10.0.70.1 | Gateway VLAN 70 |
| Router (subif .99) | 99 Gestion | 10.0.99.1 | Gateway VLAN 99 |
| Servidor AD | 60 | 10.0.60.10 | Active Directory / DNS interno |
| Servidor Archivos | 60 | 10.0.60.20 | Archivos compartidos |
| Servidor Web | 70 | 10.0.70.10 | Web publico |
| Servidor Mail | 70 | 10.0.70.20 | Correo publico |
| Switch Core | 99 | 10.0.99.10 | Gestion via SSH |
| Switch Ventas | 99 | 10.0.99.11 | Gestion via SSH |
| Switch RRHH | 99 | 10.0.99.12 | Gestion via SSH |
| AP Inalambrico | 99 | 10.0.99.20 | Gestion del AP |

**Paso 3: Reglas de firewall entre VLANs (en el router/firewall)**

| Origen | Destino | Puerto | Accion | Razón |
|---|---|---|---|---|
| Ventas (10) | Internet | 80, 443 | PERMITIR | Navegacion web |
| Ventas (10) | Servidores Int (60) | 445 (SMB) | PERMITIR | Acceso a archivos |
| Ventas (10) | Servidores Int (60) | 389 (LDAP) | PERMITIR | Autenticacion AD |
| Ventas (10) | DMZ (70) | 80, 443 | PERMITIR | Acceso web interno |
| Ventas (10) | RRHH (20), Gerencia (40), IT (30) | todos | DENEGAR | Ventas no accede a otros dptos |
| RRHH (20) | Internet | 80, 443 | PERMITIR | Navegacion web |
| RRHH (20) | Servidores Int (60) | 445, 389 | PERMITIR | Archivos y AD |
| RRHH (20) | DMZ (70) | 80, 443 | PERMITIR | Web |
| IT (30) | TODAS | todos | PERMITIR | IT administra todo |
| Gerencia (40) | TODAS | todos | PERMITIR | Gerencia tiene acceso completo |
| Invitados (50) | Internet | 80, 443 | PERMITIR | Solo navegacion |
| Invitados (50) | CUALQUIER OTRA | todos | DENEGAR | Sin acceso a red interna |
| DMZ (70) | Servidores Int (60) | todos | DENEGAR | DMZ no inicia conexion a interna |
| Servidores Int (60) | DMZ (70) | 80, 443 | PERMITIR | Servidores internos pueden acceder a DMZ |
| DMZ (70) | Internet | 80, 443, 25 | PERMITIR | Servidores publicos responden |

**Diagrama de flujo:**

```
                     INTERNET
                        |
                   [FIREWALL]
                   Reglas de filtrado
                   entre todas las VLANs
                        |
                   [SWITCH CORE]
                   (Router-on-a-stick
                    con trunk 802.1Q)
        _______________/ | \_______________
       /          |      |      \          \
   [VLAN 10]  [VLAN 20] [VLAN 30] [VLAN 50] [VLAN 70]
    Ventas      RRHH       IT      Invitados    DMZ
    /    \       |         |          |       /    \
   PC1   PC2   PC3..     PC4..      WiFi    Web   Mail

   [VLAN 60]
   Servidores Internos
   /      \
  AD     Archivos

   [VLAN 99]
   Gestion
   /    |    \
Core  Sw10  Sw20
```

### 11. Ejercicio 3 - Analisis de captura de red

**Enunciado:** Dada la siguiente descripcion de una captura de Wireshark, identificar el posible ataque.

**Captura descrita:**

```
Time     Source          Destination     Protocol   Info
0.000    192.168.1.10   192.168.1.1     ARP        Who has 192.168.1.1? Tell 192.168.1.10
0.001    192.168.1.1    192.168.1.10    ARP        192.168.1.1 is at 00:11:22:33:44:55
0.005    192.168.1.20   192.168.1.10    ARP        192.168.1.1 is at AA:BB:CC:DD:EE:FF
0.006    192.168.1.20   192.168.1.1     ARP        192.168.1.10 is at AA:BB:CC:DD:EE:FF
0.010    192.168.1.10   192.168.1.1     ICMP       Echo (ping) request
0.012    192.168.1.20   192.168.1.10    ARP        192.168.1.1 is at AA:BB:CC:DD:EE:FF
0.015    192.168.1.10   192.168.1.20    ICMP       Echo (ping) reply
```

##### Solucion

**Analisis:**

En el tiempo 0.000, PC1 (192.168.1.10) pregunta "Quien tiene la IP 192.168.1.1?" (el gateway).

El gateway REAL (192.168.1.1) responde correctamente en 0.001: "Yo tengo 192.168.1.1 y mi MAC es 00:11:22:33:44:55".

Sin embargo, en 0.005, PC3 (192.168.1.20) envia un ARP FALSO diciendo "192.168.1.1 esta en AA:BB:CC:DD:EE:FF" (la MAC de PC3).

Luego en 0.006, PC3 envia OTRO ARP falso diciendo "192.168.1.10 esta en AA:BB:CC:DD:EE:FF" (tambien su MAC).

**Diagnostico:** Ataque ARP Spoofing (Man-in-the-Middle).

PC3 esta envenenando la tabla ARP de PC1 y del gateway para interceptar el trafico entre ellos.

**Flujo del ataque:**
1. PC3 envia ARP falso a PC1: "El gateway (192.168.1.1) soy yo (MAC: PC3)"
2. PC3 envia ARP falso al gateway: "PC1 (192.168.1.10) soy yo (MAC: PC3)"
3. PC1 envia ping al gateway -> los paquetes van a PC3
4. PC3 recibe el ping de PC1
5. PC3 reenvia el ping al gateway (si quiere pasar desapercibido) -> Man-in-the-Middle
6. El gateway responde a PC3
7. PC3 reenvia la respuesta a PC1

**Evidencias:**
- Respuestas ARP duplicadas para la misma IP con diferentes MAC (00:11:22:33:44:55 vs AA:BB:CC:DD:EE:FF)
- El host 192.168.1.20 no es el gateway pero anuncia ser el gateway
- El host 192.168.1.20 anuncia ser multiples IPs (192.168.1.1 y 192.168.1.10)

**Como detectarlo:**
1. En Wireshark, aplicar filtro `arp.duplicate-address-detected` o buscar respuestas ARP con IP duplicadas
2. Herramientas como `arpwatch` o `snort` pueden alertar sobre estos cambios
3. La tabla ARP de PC1 mostraria que el gateway tiene MAC de PC3 en lugar de la MAC real del router

**Como prevenirlo:**
- **Dynamic ARP Inspection (DAI):** Funcion de switches Cisco que valida respuestas ARP contra el DHCP snooping binding table
- **ARP statico:** En equipos criticos, configurar entradas ARP manuales (no escalable)
- **Segmentacion:** El ataque queda limitado a la misma VLAN
- **Encriptacion:** Si el trafico usa HTTPS/SSH, el atacante intercepta pero no puede leer

### 12. Ejercicio 4 - Reglas Snort para deteccion de ataques

**Enunciado:** Escribir reglas Snort para detectar:
1. Escaneo de puertos (SYN a mas de 10 puertos en 5 segundos)
2. SQL injection en HTTP (patrones comunes)
3. XSS (Cross-Site Scripting) en HTTP

##### Solucion

```snort
# ===============================================
# REGLAS SNORT PARA DETECCION DE ATAQUES
# ===============================================

# -----------------------------------------------
# 1. DETECCION DE ESCANEO DE PUERTOS
# -----------------------------------------------
# Detecta un host que envia SYN a muchos puertos diferentes en poco tiempo
# Usamos umbral (threshold) para limitar a 10 SYN en 5 segundos

alert tcp $EXTERNAL_NET any -> $HOME_NET any \
  (msg:"POSIBLE PORT SCAN - SYN a multiples puertos detectado"; \
   flow:to_server; \
   flags:S; \
   detection_filter:track by_src, count 10, seconds 5; \
   sid:2000001; \
   rev:1; \
   priority:2;)

# -----------------------------------------------
# 2. DETECCION DE SQL INJECTION EN HTTP
# -----------------------------------------------
# Patrones comunes de SQL injection en peticiones HTTP

# SQL Injection basico: ' OR 1=1
alert tcp $EXTERNAL_NET any -> $HTTP_SERVERS $HTTP_PORTS \
  (msg:"SQL INJECTION - ' OR 1=1 detectado"; \
   flow:to_server,established; \
   content:"' OR"; nocase; \
   sid:2000002; \
   rev:1; \
   classtype:web-application-attack;)

# SQL Injection: UNION SELECT
alert tcp $EXTERNAL_NET any -> $HTTP_SERVERS $HTTP_PORTS \
  (msg:"SQL INJECTION - UNION SELECT detectado"; \
   flow:to_server,established; \
   content:"UNION"; nocase; \
   content:"SELECT"; nocase; \
   distance:0; \
   sid:2000003; \
   rev:1; \
   classtype:web-application-attack;)

# SQL Injection: DROP TABLE
alert tcp $EXTERNAL_NET any -> $HTTP_SERVERS $HTTP_PORTS \
  (msg:"SQL INJECTION - DROP TABLE detectado"; \
   flow:to_server,established; \
   content:"DROP TABLE"; nocase; \
   sid:2000004; \
   rev:1; \
   classtype:web-application-attack;)

# SQL Injection: comentarios SQL doble guion
alert tcp $EXTERNAL_NET any -> $HTTP_SERVERS $HTTP_PORTS \
  (msg:"SQL INJECTION - SQL comment (--) detectado"; \
   flow:to_server,established; \
   content:"--"; \
   sid:2000005; \
   rev:1; \
   classtype:web-application-attack;)

# -----------------------------------------------
# 3. DETECCION DE XSS (CROSS-SITE SCRIPTING) 
# -----------------------------------------------
# Deteccion de intentos de inyeccion de JavaScript en parametros HTTP

# XSS basico: <script>alert
alert tcp $EXTERNAL_NET any -> $HTTP_SERVERS $HTTP_PORTS \
  (msg:"XSS - tag <script> detectado"; \
   flow:to_server,established; \
   content:"<script"; nocase; \
   sid:2000006; \
   rev:1; \
   classtype:web-application-attack;)

# XSS: onerror (event handler)
alert tcp $EXTERNAL_NET any -> $HTTP_SERVERS $HTTP_PORTS \
  (msg:"XSS - evento onerror detectado"; \
   flow:to_server,established; \
   content:"onerror"; nocase; \
   sid:2000007; \
   rev:1; \
   classtype:web-application-attack;)

# XSS: onload (event handler)
alert tcp $EXTERNAL_NET any -> $HTTP_SERVERS $HTTP_PORTS \
  (msg:"XSS - evento onload detectado"; \
   flow:to_server,established; \
   content:"onload"; nocase; \
   sid:2000008; \
   rev:1; \
   classtype:web-application-attack;)

# XSS: javascript: protocolo en href
alert tcp $EXTERNAL_NET any -> $HTTP_SERVERS $HTTP_PORTS \
  (msg:"XSS - protocolo javascript: en href detectado"; \
   flow:to_server,established; \
   content:"href="; nocase; \
   content:"javascript:"; nocase; \
   distance:0; \
   sid:2000009; \
   rev:1; \
   classtype:web-application-attack;)

# XSS: document.cookie (robo de cookies)
alert tcp $EXTERNAL_NET any -> $HTTP_SERVERS $HTTP_PORTS \
  (msg:"XSS - document.cookie detectado (posible robo de cookies)"; \
   flow:to_server,established; \
   content:"document.cookie"; nocase; \
   sid:2000010; \
   rev:1; \
   classtype:web-application-attack;)
```

**Explicacion de las reglas:**

**Regla de port scan:**
- `flags:S`: Busca paquetes con flag SYN activado (inicio de conexion)
- `detection_filter:track by_src, count 10, seconds 5`: Si un mismo origen envia 10 SYN en 5 segundos, alerta
- Esto detecta cualquier tipo de escaneo de puertos (SYN scan, Connect scan)

**Reglas de SQL injection:**
- Buscan cadenas tipicas de SQL injection en el contenido HTTP
- `nocase`: Ignora mayusculas/minusculas
- Cada patron simple: `' OR`, `UNION SELECT`, `DROP TABLE`, `--`
- Los atacantes pueden evadir estos patrones con encoding (URL encoding, comentarios SQL), por lo que son reglas basicas

**Reglas de XSS:**
- Detectan tags HTML tipicos de XSS: `<script>`
- Detectan event handlers: `onerror`, `onload`
- Detectan protocolo `javascript:` en enlaces
- Detectan intentos de robo de cookies con `document.cookie`
- Todas buscan en trafico HTTP hacia servidores web ($HTTP_SERVERS)

**Limitaciones de estas reglas:**
- Son reglas basicas. Un atacante puede evadirlas con:
  - URL encoding: `%27%20OR%201%3D1`
  - HTML encoding: `&#60;script&#62;`
  - Variaciones de mayusculas (parcialmente cubierto con nocase)
  - Comentarios SQL: `UN/**/ION SEL/**/ECT`
  - Ofuscacion JavaScript

**Como probar las reglas:**
```bash
# Verificar sintaxis de las reglas
snort -T -c /etc/snort/rules/local.rules

# Ejecutar Snort en modo IDS
snort -A console -q -c /etc/snort/snort.conf -i eth0
```

### 13. Preguntas y Respuestas

#### Pregunta 1
**Cual es la diferencia entre IDS y IPS?**

**Respuesta:** Un IDS (Intrusion Detection System) solo detecta y alerta cuando encuentra trafico malicioso, pero no bloquea el trafico. Opera en modo pasivo, generalmente conectado a un puerto SPAN (mirror) del switch. Un IPS (Intrusion Prevention System) detecta Y bloquea el trafico malicioso en tiempo real, ya que opera en linea (inline) entre el origen y el destino. El IPS puede descartar paquetes, cerrar conexiones, o bloquear IPs automaticamente. La desventaja del IPS es que un falso positivo (bloquear trafico legitimo) puede causar interrupciones en el servicio. Por eso, muchos administradores usan primero un IDS en modo deteccion, ajustan las reglas, y luego pasan a IPS.

#### Pregunta 2
**Que es una DMZ y como se implementa?**

**Respuesta:** Una DMZ (Zona Desmilitarizada) es un segmento de red separado que contiene servidores accesibles desde Internet (web, email, DNS) pero aislados de la red interna. Se implementa tipicamente con dos firewalls: uno externo (entre Internet y la DMZ) que solo permite puertos especificos (80, 443, 25, 53) hacia la DMZ, y uno interno (entre DMZ y red interna) que solo permite conexiones iniciadas desde la red interna hacia la DMZ, pero NUNCA desde la DMZ hacia la red interna. Tambien puede implementarse con un solo firewall con tres interfaces (WAN, DMZ, LAN). La regla de oro: si un atacante compromete un servidor en la DMZ, no debe poder acceder a la red interna.

#### Pregunta 3
**Cual es la diferencia entre un firewall stateful y uno stateless (packet filter)?**

**Respuesta:** Un firewall **stateless** (packet filter) evalua cada paquete de forma independiente, sin recordar conexiones anteriores. Solo mira cabeceras (IP, puerto, protocolo). No sabe si un paquete es respuesta a una conexion legitima o un intento de ataque. Un firewall **stateful** mantiene una tabla de estado con todas las conexiones activas. Sabe si un paquete pertenece a una conexion establecida, es una nueva conexion, o es parte de una conexion relacionada. Por ejemplo, si un cliente interno inicia una conexion HTTP a un servidor web, el firewall stateful automaticamente permite las respuestas del servidor porque sabe que pertenecen a una conexion establecida. Con un firewall stateless, tendrias que agregar reglas explicitas para permitir el trafico de retorno. El stateful es mas seguro y requiere menos reglas.

#### Pregunta 4
**Que es Zero Trust y como se diferencia del modelo de seguridad tradicional?**

**Respuesta:** Zero Trust es un modelo de seguridad que elimina la confianza implicita basada en la ubicacion de red. Su lema es "Never trust, always verify" (nunca confies, siempre verifica). A diferencia del modelo tradicional que confia en todo lo que esta dentro del perimetro de red, Zero Trust requiere verificacion continua para CADA solicitud de acceso, sin importar si viene de dentro o fuera de la red. Se basa en: microsegmentacion (dividir la red en segmentos muy pequenos), acceso con minimos privilegios (solo lo necesario), autenticacion continua (no solo al inicio), y monitoreo constante. Google BeyondCorp es el ejemplo mas conocido. Mientras que el modelo tradicional es como un castillo con muro perimetral (facil de defender pero debil si alguien traspasa el muro), Zero Trust es como un edificio con multiples puertas de seguridad donde cada una requiere autorizacion independiente.

#### Pregunta 5
**Como funciona 802.1X?**

**Respuesta:** 802.1X es un estandar IEEE para control de acceso a la red a nivel de puerto. Funciona con tres componentes: (1) **Supplicant:** El dispositivo que quiere conectarse (PC, laptop), que ejecuta un software cliente, (2) **Authenticator:** El switch o punto de acceso que controla el puerto fisico o virtual, (3) **Authentication Server:** Generalmente un servidor RADIUS (Remote Authentication Dial-In User Service) que valida las credenciales. El proceso: el dispositivo se conecta al switch pero el puerto queda en estado "blocked" (solo permite trafico EAP). El supplicant envia credenciales (usuario y contrasena o certificado) al authenticator, quien las reenvia al servidor RADIUS. Si las credenciales son validas, el servidor RADIUS envia un "accept" y el switch abre el puerto. Si no, el puerto permanece bloqueado.

#### Pregunta 6
**Que es una VPN y para que sirve?**

**Respuesta:** Una VPN (Virtual Private Network) crea un tunel cifrado entre dos puntos a traves de una red no confiable (como Internet). Todo el trafico que viaja por el tunel va encriptado, por lo que nadie puede interceptarlo ni leerlo. Sirve para: (1) Acceso remoto seguro: empleados trabajando desde casa se conectan a la red corporativa como si estuvieran en la oficina, (2) Conexion entre oficinas (Site-to-Site): unir redes de diferentes sucursales de forma segura, (3) Privacidad en redes publicas: proteger el trafico en WiFi de cafes, aeropuertos, hoteles, (4) Bypass de censura o restricciones geograficas. Los protocolos mas recomendados son OpenVPN (maduro, muy seguro) y WireGuard (moderno, rapido, simple). NO se recomienda PPTP porque es inseguro.

---

## Tarea / Lectura Recomendada

1. **Practicar:** Instala iptables en una maquina virtual Linux y configura las reglas del Ejercicio 1. Verifica que funcionan con `nmap` desde otra maquina
2. **Practicar:** Dibuja en draw.io el diagrama de segmentacion VLAN del Ejercicio 2 con todas las VLANs, subredes y reglas de firewall
3. **Practicar:** Descarga e instala Snort en Linux (o prueba online en https://snort.org/). Ejecuta las reglas del Ejercicio 4 contra una maquina vulnerable como Metasploitable 2
4. **Practicar:** Instala Wireshark y captura trafico de tu red mientras haces un escaneo con Nmap. Identifica los paquetes SYN, SYN-ACK y RST
5. **Leer:** "Network Security Bible" de James Doherty - capitulos sobre firewalls y VPNs
6. **Leer:** Documentacion de Snort - https://www.snort.org/documents (manual de reglas)
7. **Leer:** NIST SP 800-207 - "Zero Trust Architecture" (arquitectura Zero Trust)
8. **Leer:** OWASP - "Network Segmentation Cheat Sheet"
9. **Explorar:** WireGuard - https://www.wireguard.com/ (VPN moderna y rapida)
10. **Explorar:** Wazuh - https://wazuh.com/ (SIEM gratuito de codigo abierto)
11. **Proyecto:** Disena la arquitectura de seguridad completa para una empresa de 200 empleados con 6 departamentos, incluyendo: firewall, DMZ, segmentacion VLAN, IDS/IPS, VPN para remotos, y politicas Zero Trust
