# Clase 7: Diseno de Redes - Criterios, Herramientas Gratuitas y Planificacion

**Duracion:** 2 horas

---

## Objetivos de Aprendizaje

1. Comprender los criterios fundamentales para disenar una red (escalabilidad, disponibilidad, seguridad, rendimiento, presupuesto)
2. Utilizar herramientas gratuitas como draw.io y Filius para crear diagramas de red y simulaciones
3. Disenar esquemas de direccionamiento IP con VLANs y segmentacion
4. Planificar el direccionamiento IP usando IPAM y documentar el diseno de red

---

## Contenido Detallado

### 1. Criterios para disenar una red

Disenar una red no es solo conectar cables. Es un proceso de ingenieria donde se deben considerar multiples factores. Vamos a ver cada criterio con ejemplos concretos.

**Analogia:** Disenar una red es como disenar un sistema de carreteras para una ciudad. No pones calles al azar: piensas cuantos autos pasaran (rendimiento), que rutas alternativas hay si una via se bloquea (disponibilidad), donde pones los semaforos y camaras (seguridad), y cuanto presupuesto tienes para construir.

#### Requisitos del negocio

Antes de dibujar cualquier diagrama, hay que preguntar:

- **Cuantos usuarios?** 10, 100, 1000? Esto determina el tipo de switches y routers.
- **Que aplicaciones usaran?** Solo correo y navegacion? O aplicaciones pesadas como videoconferencia, CAD, servidores de BD?
- **Crecimiento esperado:** La empresa planea duplicar personal el proximo ano? La red debe soportarlo sin rediseno completo.
- **Presupuesto:** Cuanto dinero hay disponible para equipos, cableado, y mantenimiento?

**Ejemplo:** Una empresa de diseno grafico con 20 personas necesita mucho ancho de banda para transferir archivos grandes. Los switches deben ser Gigabit Ethernet como minimo, y el servidor de archivos debe tener conexion de 10 Gbps.

#### Escalabilidad

La red debe poder crecer sin requerir un rediseno completo.

- **Modularidad:** Usar switches apilables o modulares que permitan agregar puertos
- **Subnetting con espacio libre:** Dejar direcciones IP sin usar para nuevos dispositivos
- **Backbone escalable:** El nucleo de la red (core) debe tener suficiente capacidad para el crecimiento esperado

#### Disponibilidad (Redundancia)

Que la red siga funcionando aunque falle un componente. Esto se logra con redundancia.

- **SPOF (Single Point of Failure):** Cualquier componente cuya falla detiene toda la red. Deben eliminarse o minimizarse.
- **Redundancia:** Tener componentes de respaldo. Switches duales, rutas alternativas, fuentes de poder redundantes, enlaces de respaldo.
- **Alta disponibilidad:** Se mide en "nueves": 99.9% (8.7h/anual de caida), 99.99% (52min/anual), 99.999% (5min/anual).

**Ejemplo de diseno redundante:**

```
Sin redundancia (SPOF):
Internet --- [Router1] --- [Switch1] --- [PCs]
  Si Router1 falla, toda la red pierde Internet.

Con redundancia:
Internet --- [Router1] --- [Switch1] --- [PCs]
          \              /
           --- [Router2]
  Si Router1 falla, Router2 toma el control.
```

#### Seguridad

La red debe proteger los datos y recursos.

- **Segmentacion:** Separar areas de la red con diferentes niveles de confianza. Ej: VLANs para separar departamentos.
- **Firewalls:** Filtrar trafico entre segmentos. No dejar que cualquier dispositivo hable con cualquier otro.
- **DMZ:** Zona desmilitarizada para servidores publicos (web, email) que estan separados de la red interna.
- **Control de acceso:** Solo dispositivos autorizados pueden conectarse (802.1X, MAC filtering).
- **Cifrado:** Usar WPA3 para WiFi, HTTPS para web, VPN para acceso remoto.

#### Rendimiento

Que la red sea suficientemente rapida para las aplicaciones que la usan.

- **Ancho de banda:** Capacidad maxima del enlace (100 Mbps, 1 Gbps, 10 Gbps).
- **Latencia:** Tiempo que tarda un paquete en ir de origen a destino. A menor latencia, mejor.
- **Throughput:** Cantidad real de datos transferidos por segundo (suele ser menor que el ancho de banda teorico).
- **QoS (Quality of Service):** Priorizar trafico importante. Ej: dar prioridad a videoconferencias sobre descargas de archivos.

**Regla practica para ancho de banda:**

| Tipo de aplicacion | Ancho de banda recomendado por usuario |
|--------------------|:--------------------------------------:|
| Navegacion + correo | 1-5 Mbps |
| Videoconferencia (Zoom/Teams) | 5-10 Mbps |
| Streaming HD | 10-25 Mbps |
| Transferencia archivos grandes | 100+ Mbps |
| Servidor (por cada servidor) | 1-10 Gbps |

#### Presupuesto

El diseno debe ajustarse al presupuesto disponible.

- **Costos iniciales:** Equipos (switches, routers, cables, patch panels, racks), instalacion.
- **Costos operativos:** Electricidad, mantenimiento, soporte tecnico, licencias, actualizaciones.
- **Balance:** No siempre lo mas caro es lo mejor. Un switch gestionable de marca reconocida puede ser mejor inversion que un switch no gestionable generico, aunque cueste mas.

#### Documentacion

La red debe estar documentada para poder mantenerla y solucionar problemas.

- **Diagramas de red:** Topologia fisica (donde estan los equipos) y logica (como se comunican).
- **IPAM (IP Address Management):** Registro de que IP tiene cada dispositivo.
- **Inventario:** Lista de equipos con marca, modelo, numero de serie, firmware, ubicacion.
- **Contrasenas y configuraciones:** Guardadas en un gestor de contrasenas seguro.

### 2. Proceso de diseno de red (metodologia)

El diseno de red sigue un proceso estructurado. Aqui presentamos una metodologia en 7 pasos:

```
PASO 1: Recopilar requisitos
    |
    v
PASO 2: Disenar topologia logica (VLANs, direccionamiento)
    |
    v
PASO 3: Disenar direccionamiento IP (subnetting, VLSM)
    |
    v
PASO 4: Seleccionar equipamiento (switches, routers, APs)
    |
    v
PASO 5: Disenar topologia fisica (cableado, racks, ubicaciones)
    |
    v
PASO 6: Documentar (diagramas, IPAM, inventario)
    |
    v
PASO 7: Simular y validar (opcional, con Filius, Packet Tracer)
```

**Paso 1 - Recopilar requisitos:**
- Numero de usuarios por area/departamento
- Aplicaciones que usaran (peso en la red)
- Requisitos de seguridad (quien puede acceder a que)
- Crecimiento proyectado a 3-5 anos
- Presupuesto disponible

**Paso 2 - Topologia logica:**
- Disenar VLANs: cuantas, que nombre, que departamento
- Disenar la jerarquia: nucleo (core), distribucion, acceso
- Donde van los firewalls, servidores, DMZ

**Paso 3 - Direccionamiento IP:**
- Elegir rango de IPs privadas (10.x.x.x, 172.16.x.x, 192.168.x.x)
- Aplicar VLSM segun necesidades de cada segmento
- Asignar IPs fijas a servidores, routers, switches (reserva)
- Asignar DHCP para estaciones de trabajo

**Paso 4 - Seleccionar equipamiento:**
- Switches: gestionables? PoE? Numero de puertos? Velocidad?
- Routers: capacidad de enrutamiento, VPN? Firewall integrado?
- APs: estandar WiFi (ac, ax/WiFi6), cantidad de antenas, PoE?
- Firewall: throughput, numero de usuarios, features (IPS, antivirus)

**Paso 5 - Topologia fisica:**
- Donde van los racks (centro de cableado)
- Tipo de cable: Cat6 para oficinas, fibra para backbone entre racks
- Distancias maximas: Ethernet 100m, fibra multi-modo 500m, fibra mono-modo 10+ km
- Distribucion de tomas de red por oficina

**Paso 6 - Documentar:**
- Diagramas (draw.io, diagrams.net)
- Planilla de direccionamiento IP (IPAM en Excel o herramienta)
- Inventario de equipos con numeros de serie
- Procedimientos de backup de configuracion

### 3. Herramientas gratuitas para diseno

#### draw.io / diagrams.net

Es una herramienta gratuita de diagramas que funciona online (app.diagrams.net) o descargable como aplicacion de escritorio. Permite crear diagramas de red con iconos profesionales.

**Como usarlo paso a paso:**

1. **Abrir:** Ve a https://app.diagrams.net o descarga la aplicacion
2. **Crear nuevo diagrama:** Haz clic en "Create New Diagram"
3. **Seleccionar plantilla:** En la barra izquierda, busca "Network" o elige "Blank Diagram"
4. **Paletas de iconos:** En la barra lateral izquierda, haz clic en "More Shapes..." y activa:
   - "Networks" - Cisco icons
   - "AWS" / "Azure" - si usas cloud
   - "General" - formas basicas
5. **Dibujar la red:** Arrastra iconos al lienzo
6. **Conectar dispositivos:** Usa la herramienta de flecha (Connect) para dibujar enlaces
7. **Etiquetar:** Haz doble clic en cada icono para escribir el nombre (ej: "Switch-Core", "Router-Principal")
8. **Personalizar:** Cambia colores, tamanos, estilos de linea
9. **Exportar:** File -> Export As -> PNG, PDF, o SVG

**Atajos utiles:**
- Ctrl+D: Duplicar elemento seleccionado
- Ctrl+G: Agrupar elementos
- Ctrl+Shift+C: Copiar estilo
- Ctrl+Shift+V: Pegar estilo

#### Filius

Filius es un simulador de redes educativo, gratuito y muy sencillo. Ideal para principiantes porque no requiere configuracion compleja.

**Caracteristicas:**
- Interfaz grafica simple: arrastrar y soltar componentes
- Permite configurar IPs, mascaras, gateways
- Simula trafico de red (pings, HTTP, DNS)
- Muestra los paquetes viajando en tiempo real
- Funciona en Windows, Linux, Mac

**Instalacion:**
1. Descargar de https://www.lernsoftware-filius.de/ (seccion Download)
2. Ejecutar el instalador (es un archivo JAR, requiere Java)
3. Abrir el programa

**Alternativa online:** Si no quieres instalar, usa simuladores online como "Cisco Packet Tracer" (requiere registro) o "GNS3" (mas avanzado).

#### Cisco Packet Tracer (mencion)

Herramienta profesional educativa de Cisco. Mas potente que Filius pero requiere registro gratuito en Cisco NetAcademy. Permite simular redes complejas con equipos Cisco reales (comandos IOS).

### 4. Ejemplo practico de diseno con draw.io

**Escenario:** PYME de 30 empleados con 3 departamentos, 1 servidor de archivos, 1 firewall, 1 router, 2 switches, acceso a Internet.

**Paso a paso para disenarlo en draw.io:**

**Paso 1:** Abre app.diagrams.net y crea un nuevo diagrama en blanco.

**Paso 2:** En "More Shapes", activa "Networks" y "General".

**Paso 3:** Arrastra los siguientes iconos desde la barra izquierda:
- Un "Cloud" para Internet
- Un "Firewall" (busca en Networks)
- Un "Router" (icono de router Cisco)
- Dos "Switch" (switches de capa 2)
- Un "Server" para el servidor de archivos
- Varios "PC" para las estaciones de trabajo
- Lineas de conexion (Ethernet)

**Paso 4:** Organizalos en el lienzo de arriba a abajo:

```
                    [Internet]
                        |
                    [Firewall]
                        |
                    [Router]
                   /         \
            [Switch1]      [Switch2]
           /    |    \          |
        [PC1] [PC2] [PC3]   [Server]
```

**Paso 5:** Conecta los dispositivos:
- Selecciona la herramienta "Connect" (icono de flecha)
- Haz clic en un dispositivo y arrastra hacia otro
- Las lineas se crean automaticamente

**Paso 6:** Etiqueta cada dispositivo:
- Haz doble clic y escribe el nombre
- Usa colores para grupos: verde para dispositivos de red, azul para PCs, rojo para servidores

**Paso 7:** Agrega notas y leyendas:
- Usa el icono "Text" (T) para agregar texto explicativo
- Crea una leyenda en una esquina: "Rojo = Servidores, Azul = Usuarios, Verde = Red"

**Paso 8:** Exporta el diagrama:
- File -> Export As -> PNG (con fondo blanco)
- Marca "Transparent Background" si prefieres sin fondo

**Resultado visual esperado:**

```
+-----------+
| INTERNET  |
+-----------+
      |
+-----------+
| FIREWALL  |
| Pfsense   |
+-----------+
      |
+-----------+
|  ROUTER   |
| MikroTik  |
+-----------+
      |
------+------
|     |     |
+----------+ +----------+
| SWITCH 1 | | SWITCH 2 |
| Admin    | | Prod     |
+----------+ +----------+
  |  |  |      |  |  |
+--+--+--+   +--+--+--+
|PC1 PC2 PC3| |SRV1 SRV2|
|Admin      | |Prod     |
+-----------+ +---------+
```

### 5. VLANs (Virtual LANs)

Una VLAN (Virtual Local Area Network) permite dividir una red fisica en multiples redes logicas sin cambiar el cableado.

**Analogia:** Imagina un edificio de oficinas con un solo piso (un solo switch). Con VLANs, puedes hacer como si el piso estuviera dividido en habitaciones separadas, aunque todas compartan el mismo espacio fisico. La gente de la habitacion A no puede ver a la de la habitacion B a menos que haya una puerta (router) que las comunique.

**Para que sirven las VLANs?**
- **Segmentacion:** Separar departamentos (Ventas, IT, RRHH) en diferentes redes
- **Seguridad:** El trafico de una VLAN no llega a otra sin pasar por un router/firewall
- **Rendimiento:** Reducir el dominio de broadcast (los broadcasts no cruzan VLANs)
- **Flexibilidad:** Un usuario puede estar en cualquier VLAN sin mover cables

**Ejemplo tipico de VLANs:**

| VLAN ID | Nombre | Red | Proposito |
|:-------:|--------|-----|-----------|
| 10 | Admin | 192.168.10.0/24 | Personal administrativo |
| 20 | IT | 192.168.20.0/24 | Departamento de sistemas |
| 30 | Invitados | 192.168.30.0/24 | WiFi para visitas (sin acceso interno) |
| 99 | Native | - | VLAN de gestion de switches |

**Funcionamiento:**

Cuando un switch recibe un paquete, si tiene VLANs configuradas, solo reenvia el paquete a puertos que pertenecen a la misma VLAN. Para que dispositivos de diferentes VLANs se comuniquen, necesitan un router (o un switch de capa 3) que haga enrutamiento entre VLANs.

**Trunking (802.1Q):**

Cuando conectas dos switches que manejan multiples VLANs, necesitas un **trunk** (enlace troncal) que lleve el trafico de todas las VLANs. El protocolo 802.1Q agrega una etiqueta (tag) a cada trama Ethernet indicando a que VLAN pertenece.

```
Trama Ethernet con tag 802.1Q:
+--------+--------+-------+--------+---------+--------+
| MAC    | MAC    | 802.1Q| Tipo   | Datos   | CRC    |
| Destino| Origen | Tag   |        |         |        |
+--------+--------+-------+--------+---------+--------+
                      |
                 +----+----+
                 | VLAN ID  |
                 | (12 bits)|
                 +---------+
```

**VLAN nativa (Native VLAN):** Es la VLAN por defecto (normalmente VLAN 1) que no lleva tag 802.1Q en el trunk. Por seguridad, se recomienda cambiar la VLAN nativa a un ID diferente (ej: VLAN 99) y no usarla para datos de usuario.

### 6. Diseno de DMZ

Una DMZ (Zona Desmilitarizada) es un segmento de red que contiene servidores accesibles desde Internet pero que esta separado de la red interna.

**Analogia:** Es como la recepcion de un edificio. Los visitantes (Internet) pueden entrar a la recepcion (DMZ) para dejar paquetes o consultar informacion, pero no pueden pasar a las oficinas internas (red interna) sin autorizacion.

**Arquitectura tipica con dos firewalls:**

```
                            INTERNET
                               |
                    +------------------+
                    |   FIREWALL EXTERNO|
                    |  (Permite HTTP,   |
                    |   HTTPS, DNS, SMTP|
                    |   hacia DMZ)      |
                    +------------------+
                               |
                    +------------------+
                    |   ZONA DMZ       |
                    | [Web Server]     |
                    | [Mail Server]    |
                    | [DNS Server]     |
                    +------------------+
                               |
                    +------------------+
                    |   FIREWALL INTERNO|
                    |  (Solo permite   |
                    |   conexiones      |
                    |   INICIADAS desde |
                    |   red interna)    |
                    +------------------+
                               |
                    +------------------+
                    |   RED INTERNA    |
                    | [PCs] [Servidor] |
                    | [BD] [Impresora] |
                    +------------------+
```

**Reglas de firewall tipicas para DMZ:**

| Origen | Destino | Puerto | Accion | Explicacion |
|--------|---------|--------|--------|-------------|
| Internet | DMZ: Web | 80, 443 | PERMITIR | Usuarios web acceden al servidor |
| Internet | DMZ: Mail | 25, 587 | PERMITIR | Correo entrante |
| Internet | DMZ: DNS | 53 | PERMITIR | Resolucion DNS publica |
| Internet | RED INTERNA | Todos | DENEGAR | Nadie de Internet entra a la red interna |
| DMZ | RED INTERNA | Todos | DENEGAR | Servidores DMZ no inician conexion interna |
| RED INTERNA | DMZ | 80, 443, 22 | PERMITIR | Internos acceden a servidores DMZ |
| RED INTERNA | Internet | Todos | PERMITIR | Internos navegan por Internet |
| RED INTERNA | BD Interna | 3306, 5432 | PERMITIR | Solo servidores internos acceden a BD |

**Regla de oro de la DMZ:** La DMZ es una zona de confianza intermedia. Los servidores en DMZ pueden ser atacados, por lo que deben estar endurecidos (hardened) y aislados. Si un atacante compromete el servidor web en la DMZ, NO debe poder acceder a la red interna desde ahi.

### 7. IPAM (IP Address Management)

IPAM es el proceso de planificar, rastrear y gestionar las direcciones IP en una red. Sin IPAM, es facil asignar IPs duplicadas o quedarse sin espacio.

**Metodos de IPAM:**

| Metodo | Ventajas | Desventajas | Recomendado para |
|--------|----------|-------------|------------------|
| **Excel** | Gratuito, simple | Propenso a errores humanos, sin actualizacion automatica | Redes pequeñas (< 50 dispositivos) |
| **phpIPAM** | Gratuito, web, automatico con DHCP | Requiere servidor web, mantenimiento | Redes medianas (50-500 dispositivos) |
| **NetBox** | Gratuito, completo, DCIM+IPAM | Curva de aprendizaje alta | Redes grandes (+500 dispositivos) |
| **LibreNMS** | Gratuito, monitoreo + IPAM | Mas enfocado en monitoreo | Redes medianas/grandes |

#### Plantilla de Excel basica para IPAM

Puedes crear una planilla con estas columnas:

| IP | Dispositivo | VLAN | Ubicacion | MAC | Notas |
|----|-------------|------|-----------|-----|-------|
| 192.168.1.1 | Router-Cisco | - | Rack 1 | 00:11:22:AA:BB:01 | Gateway |
| 192.168.1.2 | Switch-Core | - | Rack 1 | 00:11:22:AA:BB:02 | Gestion |
| 192.168.1.10 | Servidor-Archivos | 10 | Sala Servidores | AA:BB:CC:DD:EE:10 | IP fija |
| 192.168.1.20 | PC-JuanPerez | 10 | Oficina 201 | AA:BB:CC:DD:EE:20 | DHCP |
| 192.168.2.1 | Switch-Produccion | 20 | Planta Baja | 00:11:22:AA:CC:01 | Gestion |

---

## Ejercicio 1: Disenar red PYME con draw.io

**Enunciado:** Una pequeña empresa de 30 empleados necesita una red con:
- 2 departamentos (Administracion y Produccion)
- 1 servidor de archivos
- Acceso a Internet
- Segmentacion entre departamentos
- Presupuesto limitado (equipos de gama media)

Disena la red usando draw.io y describe el diseno final.

### Solucion

**Instrucciones paso a paso para draw.io:**

1. Abre https://app.diagrams.net y selecciona "Create New Diagram"
2. En "More Shapes", activa "Networks" y arrastra los siguientes elementos:
   - 1 icono de nube (Internet)
   - 1 icono de firewall (puede ser un rectangulo rojo con texto "Firewall")
   - 1 icono de router
   - 2 iconos de switch
   - 1 icono de servidor
   - 1 icono de access point
   - Varios iconos de PC (al menos 4)
3. Organiza en el lienzo de arriba a abajo:

**Diseno final descrito:**

```
Topologia del diseno:

                     INTERNET
                        |
                   [FIREWALL]
                   (Pfsense/OPNsense)
                        |
                    [ROUTER]
                 (MikroTik hEX)
                   /           \
          [SWITCH-ADMIN]    [SWITCH-PROD]
          (TP-Link SG108)   (TP-Link SG108)
          /     |     \          |
       [PC1] [PC2] [PC3]   [SERVIDOR]
       Admin  Admin  Admin   (Archivos)
                              |
                        [SWITCH-PROD]
                        /     |     \
                    [PC4]  [PC5]  [PC6]
                    Prod   Prod   Prod
```

**Segmentacion con VLANs:**
- VLAN 10 - Admin: 192.168.10.0/24 (hasta 254 hosts)
- VLAN 20 - Produccion: 192.168.20.0/24 (hasta 254 hosts)
- VLAN 99 - Gestion: 192.168.99.0/24 (solo equipos de red)

**Asignacion de IPs:**
| Dispositivo | IP | VLAN |
|-------------|----|------|
| Firewall (WAN) | IP publica del ISP | - |
| Firewall (LAN) | 192.168.10.1 | 10 |
| Router | 192.168.10.2 (VLAN 10), 192.168.20.2 (VLAN 20) | 10, 20 |
| Switch-Admin | 192.168.99.10 | 99 |
| Switch-Prod | 192.168.99.20 | 99 |
| Servidor | 192.168.20.10 | 20 |
| PC Admin (DHCP) | 192.168.10.50-100 | 10 |
| PC Prod (DHCP) | 192.168.20.50-100 | 20 |

**Explicacion de la segmentacion:**
- Los PCs de Administracion estan en la VLAN 10
- Los PCs de Produccion y el servidor estan en la VLAN 20
- El router hace enrutamiento entre VLANs (Router-on-a-stick) usando un solo cable al switch principal configurado como trunk 802.1Q
- El firewall filtra el trafico entre VLANs: permite que Admin acceda al servidor (puerto 445 para archivos) pero bloquea otros accesos
- El Access Point (conectado al switch Admin) crea una red WiFi separada para invitados en VLAN 30 sin acceso a recursos internos

---

## Ejercicio 2: Plan de direccionamiento IP para PYME

**Enunciado:** Dado el siguiente diseno de red, crea el plan IP completo:

- Red base: 192.168.0.0/24
- VLAN Admin: /25 (126 hosts)
- VLAN Prod: /26 (62 hosts)
- VLAN Servidores: /28 (14 hosts)
- VLAN DMZ: /29 (6 hosts)
- VLAN Gestion: /30 (2 hosts)

Calcular todas las subredes y asignar IPs a cada dispositivo.

Dispositivos:
- Router: 1 interfaz en cada VLAN
- Firewall: 1 interfaz interna (conectada al router)
- Switch Admin, Switch Prod, Switch Servidores: 1 IP de gestion cada uno
- 2 servidores Web en DMZ
- 2 servidores BD en VLAN Servidores
- PC de Admin: 10 equipos (DHCP)
- PC de Prod: 5 equipos (DHCP)
- AP WiFi: 1 en VLAN Admin
- Impresora de red: 1 en VLAN Admin

### Solucion

**Paso 1: Disenar el esquema VLSM**

Ordenamos de mayor a menor y asignamos bloques consecutivos dentro de 192.168.0.0/24:

| VLAN | Hosts necesarios | Mascara | Bits host | 2^n-2 | Incremento | Red | Rango |
|------|:----------------:|:-------:|:---------:|:-----:|:----------:|-----|-------|
| Admin | 10 PCs + AP + impresora + router + futuros = ~20 (max 126) | /25 | 7 | 126 | 128 | 192.168.0.0/25 | .0 - .127 |
| Prod | 5 PCs + router + futuros = ~10 (max 62) | /26 | 6 | 62 | 64 | 192.168.0.128/26 | .128 - .191 |
| Servidores | 2 servidores BD + router + futuros = ~5 (max 14) | /28 | 4 | 14 | 16 | 192.168.0.192/28 | .192 - .207 |
| DMZ | 2 servidores Web + futuros = ~3 (max 6) | /29 | 3 | 6 | 8 | 192.168.0.208/29 | .208 - .215 |
| Gestion | 3 switches + router + firewall = ~5 (max 2) | /30 | 2 | 2 | 4 | 192.168.0.216/30 | .216 - .219 |

**Nota:** Para gestion, necesitamos al menos 5 IPs (3 switches + 1 router + 1 firewall), pero /30 solo da 2 hosts. Podemos usar un /29 para gestion o simplemente asignar IPs de gestion dentro de la VLAN Admin (ya que los switches se administran desde la red interna). Ajustamos:

| VLAN | Red | Mascara | Hosts utiles |
|------|-----|:-------:|:------------:|
| Admin | 192.168.0.0 | /25 | 126 |
| Prod | 192.168.0.128 | /26 | 62 |
| Servidores | 192.168.0.192 | /28 | 14 |
| DMZ | 192.168.0.208 | /29 | 6 |
| Gestion | 192.168.0.216 | /29 | 6 (uso /29 en vez de /30) |

**Paso 2: Tabla completa de subredes**

| VLAN | ID | Red | Mascara | Broadcast | Rango hosts |
|------|:--:|-----|:-------:|-----------|-------------|
| Admin | 10 | 192.168.0.0/25 | 255.255.255.128 | 192.168.0.127 | .1 - .126 |
| Prod | 20 | 192.168.0.128/26 | 255.255.255.192 | 192.168.0.191 | .129 - .190 |
| Servidores | 30 | 192.168.0.192/28 | 255.255.255.240 | 192.168.0.207 | .193 - .206 |
| DMZ | 40 | 192.168.0.208/29 | 255.255.255.248 | 192.168.0.215 | .209 - .214 |
| Gestion | 99 | 192.168.0.216/29 | 255.255.255.248 | 192.168.0.223 | .217 - .222 |

**Paso 3: Asignacion de IPs por dispositivo**

**VLAN 10 - Admin (192.168.0.0/25):**
| Dispositivo | IP | Tipo | Notas |
|-------------|----|------|-------|
| Router (iface Admin) | 192.168.0.1 | Fija | Gateway de la VLAN |
| Firewall (iface interna) | 192.168.0.2 | Fija | Gestion firewall |
| Access Point | 192.168.0.3 | Fija | AP WiFi |
| Impresora | 192.168.0.4 | Fija | Impresora de red |
| DHCP Pool Admin | 192.168.0.10 - 192.168.0.100 | DHCP | Para 10 PCs + crecimiento |

**VLAN 20 - Prod (192.168.0.128/26):**
| Dispositivo | IP | Tipo | Notas |
|-------------|----|------|-------|
| Router (iface Prod) | 192.168.0.129 | Fija | Gateway de la VLAN |
| DHCP Pool Prod | 192.168.0.130 - 192.168.0.180 | DHCP | Para PCs de produccion |

**VLAN 30 - Servidores (192.168.0.192/28):**
| Dispositivo | IP | Tipo | Notas |
|-------------|----|------|-------|
| Router (iface Serv) | 192.168.0.193 | Fija | Gateway |
| Servidor BD 1 | 192.168.0.194 | Fija | Base de datos primaria |
| Servidor BD 2 | 192.168.0.195 | Fija | Base de datos replica |
| Servidor Archivos | 192.168.0.196 | Fija | Archivos compartidos |

**VLAN 40 - DMZ (192.168.0.208/29):**
| Dispositivo | IP | Tipo | Notas |
|-------------|----|------|-------|
| Router (iface DMZ) | 192.168.0.209 | Fija | Gateway |
| Servidor Web 1 | 192.168.0.210 | Fija | Web server primario |
| Servidor Web 2 | 192.168.0.211 | Fija | Web server secundario |

**VLAN 99 - Gestion (192.168.0.216/29):**
| Dispositivo | IP | Tipo | Notas |
|-------------|----|------|-------|
| Router (iface Gestion) | 192.168.0.217 | Fija | Gestion |
| Switch Admin | 192.168.0.218 | Fija | Gestion via SSH/Web |
| Switch Prod | 192.168.0.219 | Fija | Gestion via SSH/Web |

**Paso 4: Resumen visual del plan IP**

```
192.168.0.0/24
+-------------------+----------------+----------------+------+--------+
| ADMIN /25         | PROD /26       | SERV /28       | DMZ  | GEST   |
| 192.168.0.0-.127 | .128-.191      | .192-.207      | /29  | /29    |
|                   |                |                | .208 | .216   |
+-------------------+----------------+----------------+------+--------+
| .1   Router       | .129 Router    | .193 Router    | .209 | .217   |
| .2   Firewall     | .130-.180 DHCP | .194 BD1       | .210 | .218   |
| .3   AP           |                | .195 BD2       | .211 | .219   |
| .4   Impresora    |                | .196 Archivos  |      |        |
| .10-.100 DHCP     |                |                |      |        |
+-------------------+----------------+----------------+------+--------+
```

---

## Ejercicio 3: Diseno de red con Filius

**Enunciado:** Instrucciones paso a paso para configurar una red simple en Filius y verificar conectividad.

### Solucion paso a paso

**Paso 1: Instalar Filius**

1. Descarga Filius desde https://www.lernsoftware-filius.de/ (seccion "Download")
2. Requiere Java Runtime Environment (JRE) 8 o superior
3. Descarga el archivo JAR y ejecutalo con: `java -jar filius.jar`
4. La interfaz se abre mostrando un area de trabajo vacia

**Alternativa si no puedes instalar:** Usa el simulador online gratuito "Cisco Packet Tracer" (registro en Cisco NetAcademy) o "netlab" online.

**Paso 2: Crear red simple (2 PCs + Switch)**

1. En la barra izquierda, selecciona la pestana "Components" (Componentes)
2. Arrastra 2 "Workstation" (PC) al area de trabajo
3. Arrastra 1 "Switch" (hub/switch) al area de trabajo
4. Arrastra 1 "Cable connection" y conecta:
   - PC1 al Switch
   - PC2 al Switch

```
Diagrama en Filius:

[PC1] ---cable--- [SWITCH] ---cable--- [PC2]
```

**Paso 3: Asignar direcciones IP**

1. Haz clic derecho en PC1 y selecciona "Configure" (Configurar)
2. En la pestana "Network" (Red), asigna:
   - IP: 192.168.1.1
   - Mascara: 255.255.255.0
   - Gateway: 192.168.1.254 (lo asignaremos al router despues)

3. Haz clic derecho en PC2 y selecciona "Configure":
   - IP: 192.168.1.2
   - Mascara: 255.255.255.0
   - Gateway: 192.168.1.254

4. Haz clic en "OK" en ambas configuraciones.

**Paso 4: Verificar conectividad con ping**

1. Haz clic derecho en PC1
2. Selecciona "Command line input" o "Terminal"
3. Escribe: `ping 192.168.1.2`
4. Deberias ver respuestas exitosas (si no, revisa conexiones e IPs)

**Paso 5: Ver el trafico de red en modo simulacion**

1. Arriba a la derecha, hay un interruptor "Start simulation" (Iniciar simulacion)
2. Activarlo (se pondra en verde)
3. Repite el ping desde PC1 a PC2
4. Veras animaciones de paquetes viajando de PC1 al switch y al PC2
5. El switch muestra como aprende las direcciones MAC

**Paso 6: Agregar un servidor web**

1. Arrastra un "Server" (Servidor) al area de trabajo
2. Conectalo al switch con un cable
3. Configura el servidor:
   - Haz clic derecho -> "Configure"
   - IP: 192.168.1.10
   - Mascara: 255.255.255.0
   - Gateway: 192.168.1.254
4. En la pestana "Services" (Servicios), activa "Webserver"
5. Escribe un HTML simple en el recuadro: `<h1>Bienvenido al servidor web</h1>`

**Paso 7: Acceder al servidor web desde PC1**

1. En PC1, abre el navegador web (en Filius, es el icono de navegador en la barra de herramientas de la PC)
2. En la barra de direcciones, escribe: `http://192.168.1.10`
3. Deberias ver la pagina HTML que configuraste en el servidor
4. En modo simulacion, puedes ver los paquetes HTTP viajando

**Paso 8: Agregar un router para salida a Internet (opcional)**

1. Arrastra un "Router" al area de trabajo
2. Conectalo al switch
3. Configura el router:
   - Haz clic derecho -> "Configure"
   - Pestana "Network": IP 192.168.1.254 (sera el gateway)
4. En los PCs, cambia el gateway a 192.168.1.254
5. Para simular Internet, agrega otro switch conectado al router y otro servidor con IP publica (ej: 10.0.0.1)
6. Configura enrutamiento en el router para conectar ambas redes

**Diagrama final en Filius:**

```
[PC1]           [PC2]
192.168.1.1     192.168.1.2
    |                |
    +----[SWITCH]----+
              |
        [SERVIDOR WEB]
         192.168.1.10
              |
         [ROUTER]
         192.168.1.254
              |
         [SWITCH2]
          /        \
    [SRV EXTERNO]  [PC REMOTA]
       10.0.0.1      10.0.0.2
```

**Verificacion final:**
- Desde PC1: ping a 192.168.1.2 (dentro de la misma red) -> debe funcionar
- Desde PC1: ping a 192.168.1.10 (servidor web) -> debe funcionar
- Desde PC1: navegador a http://192.168.1.10 -> debe mostrar la pagina
- Desde PC2: ping a 10.0.0.1 (red externa, via router) -> debe funcionar si el router esta configurado

---

## Preguntas y Respuestas

### Pregunta 1
**Que es una VLAN y para que sirve?**

**Respuesta:** Una VLAN (Virtual Local Area Network) es una tecnologia que permite crear redes logicas independientes dentro de una misma red fisica. Sirve para:
1. **Segmentacion:** Separar departamentos (Ventas, IT, RRHH) en diferentes redes sin necesidad de cableado separado.
2. **Seguridad:** El trafico de una VLAN no llega a otra a menos que pase por un router/firewall con reglas especificas.
3. **Reduccion de broadcast:** Los mensajes broadcast solo se propagan dentro de la VLAN, no a toda la red.
4. **Flexibilidad:** Un usuario puede cambiar de VLAN sin mover cables, solo reconfigurando el puerto del switch.
5. **Optimizacion:** Mejor rendimiento al reducir el tamano de los dominios de colision y broadcast.

### Pregunta 2
**Cual es la diferencia entre topologia fisica y topologia logica?**

**Respuesta:** La **topologia fisica** describe como estan conectados los dispositivos fisicamente (cables, equipos, ubicaciones). Muestra los racks, los patch panels, por donde pasan los cables, las distancias. Es la que ves cuando entras a un centro de datos y ves los cables. La **topologia logica** describe como fluyen los datos y como se comunican los dispositivos a nivel de red, independientemente de la disposicion fisica. Muestra las VLANs, las subredes, las rutas de enrutamiento, los dominios de broadcast. Por ejemplo, fisicamente dos servidores pueden estar en el mismo rack, pero logicamente estar en VLANs diferentes y no poder comunicarse directamente. La topologia logica es la que disenas en tools como draw.io; la fisica la disenas cuando planificas el cableado.

### Pregunta 3
**Que es una DMZ y por que es importante para la seguridad?**

**Respuesta:** Una DMZ (Zona Desmilitarizada) es un segmento de red separado que contiene servidores accesibles desde Internet (servidores web, email, DNS). Es importante porque actua como zona de amortiguacion: si un atacante compromete un servidor en la DMZ, NO tiene acceso directo a la red interna. La arquitectura tipica tiene dos firewalls: uno entre Internet y la DMZ (permite trafico entrante a servicios publicos), y otro entre la DMZ y la red interna (solo permite conexiones iniciadas desde la red interna hacia la DMZ, pero nunca al reves). Esto implementa el principio de **defense in depth** (defensa en profundidad): multiples capas de seguridad. Incluso si un atacante vulnera el primer firewall y el servidor web, aun tiene que pasar el segundo firewall para llegar a los datos internos.

### Pregunta 4
**Que criterios se deben considerar al disenar una red?**

**Respuesta:** Los criterios principales son:
1. **Requisitos del negocio:** Cuantos usuarios, que aplicaciones usan, crecimiento esperado.
2. **Escalabilidad:** La red debe poder crecer sin rediseno completo. Dejar espacio en IPs y slots en switches.
3. **Disponibilidad:** Eliminar SPOF (Single Point of Failure) con redundancia de equipos y rutas.
4. **Seguridad:** Segmentacion con VLANs, firewalls, DMZ, control de acceso, cifrado WiFi.
5. **Rendimiento:** Ancho de banda suficiente, baja latencia, QoS para trafico critico.
6. **Presupuesto:** Balance entre calidad y costo. Equipos gestionables, cableado categoría adecuada.
7. **Documentacion:** Diagramas, plan IP, inventario, configuraciones backup.
8. **Mantenibilidad:** Equipos estandarizados, facil de diagnosticar y reparar.

### Pregunta 5
**Para que sirve un IPAM y cuando deberia usar uno?**

**Respuesta:** Un IPAM (IP Address Management) es un sistema para planificar, rastrear y gestionar las direcciones IP de una red. Sirve para:
1. **Evitar duplicados:** Saber que IPs estan asignadas y a que dispositivo.
2. **Optimizar uso:** Identificar espacios libres y evitar desperdicio de direcciones.
3. **Documentar:** Tener un registro centralizado de todas las IPs, dispositivos, ubicaciones.
4. **Auditar:** Saber que IP tenia un dispositivo cuando ocurrio un incidente.
5. **Planificar:** Facilitar el diseno de nuevas subredes (VLSM).

Deberias usar un IPAM cuando tu red tiene mas de 50 dispositivos, o cuando varias personas administran la red, o cuando necesitas cumplir con requisitos de auditoria. Para redes pequeñas, una planilla de Excel puede ser suficiente. Para redes medianas/grandes, herramientas como phpIPAM (gratuito) o NetBox son recomendables.

### Pregunta 6 (Adicional)
**Que es el trunking 802.1Q y como funciona?**

**Respuesta:** El trunking 802.1Q es un protocolo que permite que un solo cable lleve trafico de MULTIPLES VLANs entre dos switches, o entre un switch y un router. Funciona agregando una etiqueta (tag) de 4 bytes a cada trama Ethernet que indica a que VLAN pertenece. Cuando un switch recibe una trama por un puerto trunk, sabe exactamente a que VLAN debe entregarla. Esto permite que un solo enlace fisico transporte el trafico de todas las VLANs, en lugar de necesitar un cable separado por cada VLAN. El estandar 802.1Q soporta hasta 4094 VLANs (IDs 1-4094). La VLAN nativa (normalmente VLAN 1) no lleva tag en el trunk, por lo que ambos extremos deben acordar cual es la VLAN nativa para evitar problemas de seguridad.

---

## Tarea / Lectura Recomendada

1. **Practicar:** Descarga draw.io y disena la red de tu casa o de la institucion donde estudias, incluyendo VLANs y direccionamiento IP
2. **Practicar:** Instala Filius y crea una red con 3 PCs, 2 switches, 1 router y 1 servidor web. Configura todo y verifica conectividad
3. **Practicar:** Crea una plantilla de IPAM en Excel con 50 filas y completa los datos de tu red local
4. **Leer:** "Cisco Networking Essentials" de Troy McMillan (capitulos sobre diseno de LAN)
5. **Leer:** Documentacion de phpIPAM (https://phpipam.net/) para entender como funciona un IPAM profesional
6. **Leer:** RFC 1918 - "Address Allocation for Private Internets" (los rangos de IPs privadas)
7. **Leer:** IEEE 802.1Q - "Virtual LANs" (estandar de VLANs, aunque es tecnico, busca resumenes didacticos)
8. **Explorar:** Cisco Packet Tracer - Registrate en Cisco NetAcademy (gratuito) y explora el simulador para practicar configuraciones avanzadas
9. **Ver:** Video "Network Design Methodology" en YouTube de Keith Barker o NetworkChuck (en ingles con subtitulos)
10. **Proyecto final del modulo:** Disena la red completa de una empresa mediana (50 usuarios) con 4 departamentos, DMZ, servidores, y documenta todo: diagrama en draw.io, plan IP en Excel, y simulacion basica en Filius
