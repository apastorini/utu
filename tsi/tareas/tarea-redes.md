# Tarea Grupal: Diseno, Simulacion y Auditoria de Red Corporativa

**Curso:** Taller de Ciberseguridad Orientada al Desarrollo  
**Modulo:** Seguridad en Redes (Clase 10)
**Tipo:** Trabajo grupal (2 personas)  
**Puntaje total:** 100 puntos  

---

## Objetivo

Disenar, simular y auditar una red corporativa aplicando los conceptos de direccionamiento IP, subredes, diseno de redes, simulacion con Filius o Packet Tracer, escaneo con Nmap, y seguridad en redes.

---

## Escenarios disponibles

Cada grupo recibe UN escenario, asignado por el profesor. Hay 8 escenarios:

### 1. PYME de tecnologia (30 empleados)

- 3 departamentos: Desarrollo, Ventas, Administracion
- 1 servidor interno (archivos, base de datos)
- 1 servidor web publico
- Acceso WiFi para invitados

### 2. Clinica medica (50 empleados)

- Recepcion, Consultorios, Laboratorio, Farmacia
- Servidor de historias clinicas (datos sensibles)
- Cumplimiento GDPR (proteccion de datos personales)
- Red separada para dispositivos medicos

### 3. Universidad (2000 estudiantes + 200 empleados)

- 3 edificios (Aulas, Laboratorios, Administracion)
- Biblioteca con acceso a bases de datos academicas
- Laboratorios de computo (200 equipos)
- Servidores academicos (moodle, repositorio, correo)
- Red WiFi por edificio con autenticacion centralizada

### 4. Banco sucursal (40 empleados)

- Atencion al cliente (cajas, ejecutivos)
- Oficinas administrativas
- Boveda / Seguridad (camaras, alarmas, control de acceso)
- Servidores internos (aplicaciones bancarias)
- Conexion encriptada a sede central por VPN

### 5. Tienda retail (3 sucursales)

- Cada sucursal: 10 empleados + cajas POS (punto de venta)
- Servidor central en matriz (ERP, inventario, facturacion)
- Conexion WAN entre sucursales y matriz
- WiFi para clientes en cada sucursal

### 6. Colegio (500 estudiantes + 50 profesores)

- Aulas distribuidas en 3 pisos
- Sala de profesores, Administracion, Biblioteca
- Servidor educativo (plataforma virtual, calificaciones)
- WiFi para estudiantes (filtrado por contenido)
- Laboratorio de informatica (40 equipos)

### 7. Fabrica industrial (100 empleados)

- Oficinas administrativas
- Planta de produccion con dispositivos IoT / SCADA
- Deposito y logistica
- Control de calidad
- Camaras de seguridad (red cerrada)
- Red industrial aislada de red corporativa

### 8. Startup fintech (20 empleados)

- Desarrollo, Operaciones, Cumplimiento
- Servidores en cloud (AWS/Azure) con acceso por VPN
- Conexion a APIs bancarias externas
- Cumplimiento PCI DSS (datos de tarjetas)
- Segmentacion estricta por ambiente (dev, staging, prod)

---

## Parte 1: Diseno de Red (40 puntos)

### 1.1 Diagrama de red (10 puntos)

Crear un diagrama profesional en draw.io (exportar a PNG o SVG) que incluya:

- Topologia completa con todos los dispositivos (hosts, switches, routers, firewalls, access points, servidores)
- Segmentacion VLAN (minimo 4 VLANs) claramente identificada
- DMZ para servidores publicos (accesibles desde internet)
- Firewall en el borde de la red (conexion a internet)
- Red de invitados separada (sin acceso a la red interna)
- Etiquetado claro de interfaces, direcciones IP y VLANs

### 1.2 Plan de direccionamiento IP (10 puntos)

Elaborar una tabla completa con:

| Subred | VLAN | Direccion de red | Mascara CIDR | Broadcast | Rango util | Gateway |
|--------|------|------------------|--------------|-----------|------------|---------|
| ...    | ...  | ...              | ...          | ...       | ...        | ...     |

Incluir ademas:

- Asignacion de IP especifica a cada dispositivo (servidores, routers, switches de gestion)
- Esquema VLSM si aplica (subredes de distinto tamano segun necesidad)
- Justificacion del tamano elegido para cada subred

### 1.3 Lista de equipamiento (requisito) (--)

Incluir tabla con:

| Dispositivo | Modelo sugerido | Cantidad | Precio estimado (USD) | Motivo de eleccion |
|-------------|-----------------|----------|-----------------------|-------------------|
| ...         | ...             | ...      | ...                   | ...               |

### 1.4 Documento de diseno (6 puntos)

Redactar documento (formato PDF o Markdown) que contenga:

- Descripcion del escenario asignado
- Requisitos del negocio (disponibilidad, escalabilidad, seguridad, presupuesto)
- Decisiones de diseno justificadas (por que cierta topologia, por que ese equipamiento, por que esa segmentacion)
- Topologia logica (VLANs, subredes, protocolos) y fisica (ubicacion de equipos, cableado)
- Estrategia de seguridad detallada:
  - Reglas de firewall (permitir/denegar por origen, destino, puerto)
  - Segmentacion VLAN con ACLs entre VLANs
  - DMZ: que servicios se exponen y como se aislan
  - Acceso WiFi: autenticacion, cifrado, aislamiento de clientes
  - Monitoreo y logging

---

## Parte 2: Simulacion en Filius o Packet Tracer (30 puntos)

### 2.1 Implementacion (10 puntos)

- Crear la topologia completa con los componentes simulados
- Configurar direcciones IP en todos los dispositivos (estaticas y DHCP segun corresponda)
- Configurar rutas estaticas en los routers (o routing inter-VLAN)
- Configurar servidores:
  - **Servidor DHCP**: asignar direcciones a hosts de cada VLAN
  - **Servidor DNS**: resolver nombres locales (ej. `servidor-interno.pyme.local`)
  - **Servidor HTTP**: servir una pagina web en la DMZ

### 2.2 Pruebas de conectividad (8 puntos)

Verificar y documentar:

- **Ping intra-VLAN**: entre dos PCs de la misma VLAN (debe funcionar)
- **Ping inter-VLAN**: entre PCs de distintas VLANs a traves del router (debe funcionar si las ACLs lo permiten)
- **Ping a internet**: desde un PC interno hacia una IP publica simulada
- **Acceso HTTP**: desde un PC externo (internet) al servidor web en la DMZ
- **Acceso HTTP**: desde un PC interno al servidor web en la DMZ

### 2.3 Capturas de pantalla (8 puntos)

Incluir capturas de:

- Topologia completa en el simulador (vision general)
- Tabla de configuracion IP de cada dispositivo
- Resultados de ping exitosos (al menos 4 capturas diferentes)
- Trafico de red capturado durante las pruebas (Wireshark o herramienta integrada)

### 2.4 Video demo (4 puntos)

- Duracion: 3 a 5 minutos
- Contenido:
  - Recorrido por la topologia implementada
  - Demostracion de configuraciones IP
  - Pruebas de conectividad en vivo
  - Acceso a servicios (web, DNS)
- Formato: MP4 o link a video (YouTube, Google Drive, etc.)

---

## Parte 3: Auditoria de Seguridad con Nmap (30 puntos)

### 3.1 Escaneo de la red (10 puntos)

Ejecutar los siguientes escaneos sobre la red simulada (o una red de laboratorio):

```bash
# Descubrimiento de hosts activos
nmap -sn 192.168.1.0/24

# Escaneo de puertos abiertos con deteccion de version
nmap -sS -sV -p- 192.168.1.0/24

# Deteccion de sistema operativo
nmap -O 192.168.1.0/24

# Escaneo con scripts de vulnerabilidad
nmap --script=vuln 192.168.1.0/24
```

Ajustar las direcciones IP segun el plan de direccionamiento propio.

### 3.2 Informe de auditoria (10 puntos)

Documentar los resultados en un informe que incluya:

- **Tabla de dispositivos encontrados**:

| Direccion IP | Hostname | SO detectado | Puertos abiertos | Servicios | Vulnerabilidades potenciales |
|-------------|----------|-------------|------------------|-----------|------------------------------|
| ...         | ...      | ...         | ...              | ...       | ...                          |

- **Analisis de puertos abiertos**: justificar si cada puerto es necesario o deberia cerrarse
- **Vulnerabilidades potenciales**: basadas en los servicios y versiones detectados
- **Recomendaciones inmediatas**: acciones correctivas priorizadas

### 3.3 Propuesta de hardening (8 puntos)

Elaborar un plan de hardening que incluya:

- **Configuracion de firewall**: reglas especificas por interfaz (origen, destino, puerto, protocolo, accion)
- **Cierre de puertos innecesarios**: lista de puertos a bloquear y justificacion
- **Segmentacion adicional**: si el escaneo revelo que hace falta mas aislamiento
- **Monitoreo recomendado**: herramientas (Snort, Suricata, Wazuh), alertas, periodicidad
- **Politica de actualizaciones**: parches, versiones de firmware, ciclo de vida
- **Autenticacion y control de acceso**: 2FA, gestion de credenciales, acceso por SSH con llaves

### 3.4 Informe profesional (2 puntos)

- Formato limpio y organizado (Markdown o PDF)
- Lenguaje tecnico pero claro
- Incluir capturas de pantalla de los escaneos
- Incluir tabla de hallazgos y severidad

---

## Entregables

| Archivo | Descripcion | Formato |
|---------|-------------|---------|
| `diseno-red.md` | Documento de diseno completo | Markdown |
| `diagrama-red.png` o `diagrama-red.pdf` | Diagrama de red (draw.io) | PNG o PDF |
| `plan-ip.md` o `plan-ip.xlsx` | Plan de direccionamiento IP | Markdown o Excel |
| `simulacion.filus` o `.pkt` | Archivo de simulacion | Segun herramienta |
| `capturas/` | Carpeta con capturas de pantalla | PNG/JPG |
| `informe-auditoria.md` | Resultados del escaneo Nmap | Markdown |
| `video-demo.mp4` o link | Video demostrativo (3-5 min) | MP4 o URL |

---

## Rubrica de evaluacion

| Criterio | Puntos |
|----------|--------|
| **Parte 1: Diseno** | **40** |
| Diagrama de red completo y profesional | 10 |
| Plan IP correcto (subredes, VLSM, asignacion) | 10 |
| Segmentacion VLAN adecuada | 8 |
| DMZ y firewall bien ubicados | 6 |
| Justificacion de decisiones de diseno | 6 |
| **Parte 2: Simulacion** | **30** |
| Topologia implementada correctamente | 10 |
| Configuracion IP correcta en todos los dispositivos | 8 |
| Conectividad demostrada (pings, web) | 8 |
| Video demo funcional | 4 |
| **Parte 3: Auditoria** | **30** |
| Escaneo Nmap completo y documentado | 10 |
| Identificacion de vulnerabilidades | 8 |
| Propuesta de hardening | 8 |
| Informe profesional | 4 |
| **Total** | **100** |

---

## Fechas importantes

| Evento | Fecha |
|--------|-------|
| Asignacion de escenarios | Clase 10 |
| Entrega parte 1 (diseno) | Clase 17 |
| Entrega parte 2 (simulacion) | Clase 19 |
| Entrega parte 3 (auditoria) + final | Clase 22 |
| Presentacion en clase | Clase 23 |

---

## Ejemplo parcial: Escenario 1 - PYME de tecnologia

Como referencia, se muestra un ejemplo de diseno para el escenario 1.

### Ejemplo: Plan de direccionamiento IP

| Subred | VLAN | Direccion de red | Mascara CIDR | Broadcast | Rango util | Hosts |
|--------|------|------------------|--------------|-----------|------------|-------|
| Desarrollo | 10 | 192.168.10.0 | /25 | 192.168.10.127 | 192.168.10.1 - 192.168.10.126 | 126 |
| Ventas | 20 | 192.168.20.0 | /26 | 192.168.20.63 | 192.168.20.1 - 192.168.20.62 | 62 |
| Administracion | 30 | 192.168.30.0 | /27 | 192.168.30.31 | 192.168.30.1 - 192.168.30.30 | 30 |
| Servidores Internos | 40 | 192.168.40.0 | /28 | 192.168.40.15 | 192.168.40.1 - 192.168.40.14 | 14 |
| DMZ | 50 | 192.168.50.0 | /29 | 192.168.50.7 | 192.168.50.1 - 192.168.50.6 | 6 |
| Invitados | 99 | 192.168.99.0 | /28 | 192.168.99.15 | 192.168.99.1 - 192.168.99.14 | 14 |

### Ejemplo: Topologia

```
Internet
    |
[Firewall Borde] (MikroTik RB4011)
    |
    +-- [DMZ: Servidor Web] (192.168.50.2)
    |
[Firewall Interno]
    |
[Switch Core] (Cisco SG350-28)
    |
    +-- VLAN 10 - Desarrollo [Switch Acceso SG250-8]
    |       +-- PC1, PC2, ..., PC15
    |
    +-- VLAN 20 - Ventas [Switch Acceso SG250-8]
    |       +-- PC1, PC2, ..., PC8
    |
    +-- VLAN 30 - Administracion [Switch Acceso SG250-8]
    |       +-- PC1, PC2, PC3
    |
    +-- VLAN 40 - Servidores Internos
    |       +-- Servidor Archivos (192.168.40.2)
    |       +-- Servidor BD (192.168.40.3)
    |       +-- Servidor DHCP/DNS (192.168.40.4)
    |
    +-- VLAN 99 - Invitados
            +-- [Access Point Ubiquiti UAP-AC-LR]
                    +-- Clientes WiFi
```

### Ejemplo: Equipamiento sugerido

| Dispositivo | Modelo | Cant. | Precio (USD) | Motivo |
|------------|--------|-------|-------------|--------|
| Router/Firewall | MikroTik RB4011 | 1 | $180 | Router y firewall todo-en-uno, buen rendimiento, RouterOS con VLANs y reglas de firewall, bajo costo |
| Switch Core | Cisco SG350-28 | 1 | $350 | Gestionable, VLANs, ACLs, LACP, 28 puertos Gigabit |
| Switch Acceso | Cisco SG250-08 | 3 | $120 c/u | Gestionable, compacto, PoE para APs, 8 puertos |
| Access Point | Ubiquiti UAP-AC-LR | 1 | $90 | Largo alcance, VLAN por SSID, captive portal para invitados |
| Servidor Interno | Dell PowerEdge T150 | 1 | $800 | Xeon, 16 GB RAM, RAID 1, ideal para entorno PYME |
| Servidor Web | Raspberry Pi 4 (4GB) | 1 | $75 | Suficiente para un sitio web corporativo de bajo trafico |

### Recomendaciones de seguridad

- Regla de firewall: bloquear todo el trafico entrante desde internet excepto puertos 80 y 443 hacia la DMZ
- Regla de firewall: bloquear trafico desde Invitados (VLAN 99) hacia cualquier VLAN interna
- Regla de firewall: permitir solo trafico HTTP/HTTPS desde DMZ hacia Servidor BD (puerto 3306) si es necesario
- Aislar la VLAN de Servidores: solo los puertos necesarios abiertos, acceso administrativo solo por SSH desde VLAN Administracion
- Implementar 802.1Q trunking entre switches para transportar todas las VLANs
- DHCP snooping en switches de acceso para prevenir rogue DHCP servers
- Port security en puertos de acceso (max 1-2 MACs por puerto)

---

*Documento generado para el curso Taller de Ciberseguridad Orientada al Desarrollo.*
