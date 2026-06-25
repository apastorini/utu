# Clase 8: Simulacion de Redes con Filius y Packet Tracer

**Duracion:** 2 horas

---

## Objetivos de Aprendizaje

1. Comprender la diferencia entre diseno de red (diagramas) y simulacion de red (trafico real)
2. Instalar y utilizar Filius para crear redes virtuales funcionales con PCs, switches, routers y servidores
3. Configurar direccionamiento IP, servicios (HTTP, DHCP) y enrutamiento en un simulador
4. Conocer Cisco Packet Tracer como herramienta profesional de simulacion para certificaciones

---

## Contenido Detallado

### 1. Que es un simulador de redes?

Un simulador de redes es un programa que permite crear una red virtual con dispositivos como PCs, switches, routers y servidores, y luego SIMULAR el trafico de red entre ellos. Los paquetes viajan realmente (de forma virtual) y puedes ver como se comportan.

**Diferencia entre diseno y simulacion:**

| Diseno (draw.io) | Simulacion (Filius/Packet Tracer) |
|---|---|
| Dibuja la red | Hace funcionar la red |
| No envia paquetes | Los paquetes viajan virtualmente |
| No hay configuracion real | Hay que configurar IPs, rutas, servicios |
| Es estatico | Es dinamico (puedes ver el trafico en vivo) |
| Ideal para documentar | Ideal para aprender y probar |

**Analogia:** Un simulador de redes es como un simulador de vuelo. No estas volando un avion real, pero los instrumentos funcionan, el avion responde a tus comandos, y puedes practicar aterrizajes sin estrellar un avion de verdad. Disenar en draw.io es como dibujar el plano de un avion: ves las partes pero no vuela.

**Que se puede hacer en un simulador?**
- Configurar direcciones IP en cada dispositivo
- Hacer pings entre equipos y ver los paquetes ICMP viajando
- Configurar un servidor web y acceder desde un navegador simulado
- Configurar un servidor DHCP para que los PCs obtengan IP automaticamente
- Ver como un router decide por donde enviar un paquete
- Capturar y analizar paquetes (como Wireshark pero mas sencillo)

### 2. Filius - Simulador educativo gratuito

Filius es un simulador de redes creado especificamente para la educacion. Es gratuito, liviano, y muy facil de usar. No requiere conocimientos de comandos de consola real (tiene su propia terminal simplificada).

#### Instalacion

**Descarga:**
1. Ve a https://www.lernsoftware-filius.de/
2. En la seccion "Download", descarga la ultima version (archivo JAR o instalador para Windows)
3. Requiere Java Runtime Environment (JRE) 8 o superior

**Instalacion paso a paso en Windows:**
1. Si no tienes Java: descarga e instala Java desde https://www.java.com/download/
2. Descarga el archivo `Filius-Setup.exe` desde la pagina de Filius
3. Ejecuta el instalador y sigue los pasos (siguiente, siguiente, instalar)
4. Al finalizar, busca "Filius" en el menu de inicio y ejecutalo

**Alternativa si no puedes instalar:** Filius tambien tiene una version online (Webstart) que se ejecuta desde el navegador, aunque requiere Java Webstart. Si no funciona, puedes usar Cisco Packet Tracer (requiere registro gratuito) que tambien es un excelente simulador.

#### Interfaz de Filius

Cuando abres Filius, ves una ventana dividida en varias areas:

```
+--------------------------------------------------+
| Barra de menu (Archivo, Editar, Vista, Ayuda)     |
+--------------------------------------------------+
| [Componentes] [Simulacion]  | Area de trabajo    |
|                             |                    |
| +------------------------+  |                    |
| | Dispositivos de red:   |  |   [PC1]   [PC2]    |
| | - Workstation (PC)     |  |      \     /       |
| | - Server               |  |    [SWITCH]        |
| | - Switch               |  |       |            |
| | - Router               |  |   [SERVIDOR]       |
| | - Modem                |  |                    |
| | - Cable de cobre       |  |                    |
| | - Cable WiFi           |  |                    |
| +------------------------+  |                    |
|                             |                    |
| [Panel de configuracion]    |                    |
| (aparece al hacer clic     |                    |
|  derecho > Configure)      |                    |
+--------------------------------------------------+
| Barra de estado / Consola                         |
+--------------------------------------------------+
```

**Explicacion de cada area:**

1. **Barra de componentes (izquierda):** Aqui estan los dispositivos que puedes arrastrar al area de trabajo. Tienes pestanas para "Components" (dispositivos) y "Simulation" (controles de simulacion).

2. **Area de trabajo (centro):** El lienzo donde armas tu red. Arrastras componentes y los conectas con cables.

3. **Panel de configuracion:** Aparece cuando haces clic derecho en un dispositivo y seleccionas "Configure". Ahi asignas IPs, mascaras, gateways, y configuras servicios.

4. **Consola/Terminal:** Cuando haces clic derecho en un PC y seleccionas "Command line input", se abre una terminal donde puedes ejecutar comandos como `ping`, `ipconfig`, etc.

5. **Control de simulacion:** En la parte superior derecha hay un interruptor "Start simulation". Cuando esta activado (verde), los paquetes realmente viajan y puedes ver las animaciones.

#### Componentes disponibles en Filius

| Componente | Icono | Para que sirve |
|---|---|---|
| Workstation (PC) | Monitor | Estacion de trabajo del usuario. Tiene sistema operativo simulado, puede hacer ping, navegar, etc. |
| Server (Servidor) | Servidor | Puede funcionar como servidor web, DNS, DHCP, o de correo. |
| Switch (no administrable) | Switch | Conecta dispositivos en una misma red. Reenvia tramas por MAC. |
| Switch gestionable | Switch + engranaje | Similar al anterior pero permite configurar VLANs. |
| Router | Router | Conecta diferentes redes. Tiene tabla de enrutamiento. |
| Modem | Modem | Conexion a Internet (simula un modem ADSL o cable). |
| Cable de cobre | Linea | Cable Ethernet para conectar dispositivos. |
| Cable WiFi | Antena | Conexion inalambrica. |
| Cable de fibra optica | Fibra | Para conexiones de alta velocidad. |

### 3. Practica 1 - Red simple en Filius

Vamos a crear nuestra primera red: 3 PCs conectados a un switch, todos en la misma red.

**Objetivo:** Que los PCs puedan comunicarse entre si mediante ping.

#### Paso a paso

**Paso 1:** Abre Filius. Veras un area de trabajo vacia.

**Paso 2:** Arrastra 3 PCs y 1 switch al area de trabajo.
- En la barra izquierda, selecciona la pestana "Components"
- Arrastra 3 veces el icono "Workstation" al area de trabajo
- Arrastra 1 vez el icono "Switch" al area de trabajo
- Organizalos como en el diagrama:

```
[PC1]     [PC2]     [PC3]
   \        |        /
    [SWITCH PRINCIPAL]
```

**Paso 3:** Conecta los PCs al switch con cables de cobre.
- En la barra izquierda, selecciona "Cable connection" (cable de cobre)
- Haz clic en PC1 (aparece un punto de conexion) y arrastra hasta el switch
- Repite para PC2 y PC3

**Paso 4:** Configurar las direcciones IP de cada PC.

**Configurar PC1:**
- Haz clic derecho en PC1 y selecciona "Configure"
- En la pestana "Network", completa:
  - IP address: 192.168.1.1
  - Subnet mask: 255.255.255.0
  - Gateway: 192.168.1.254 (lo usaremos mas adelante)
  - Haz clic en "OK"

**Configurar PC2:**
- Haz clic derecho en PC2 -> "Configure"
  - IP address: 192.168.1.2
  - Subnet mask: 255.255.255.0
  - Gateway: 192.168.1.254
  - OK

**Configurar PC3:**
- Haz clic derecho en PC3 -> "Configure"
  - IP address: 192.168.1.3
  - Subnet mask: 255.255.255.0
  - Gateway: 192.168.1.254
  - OK

**Paso 5:** Verificar conectividad con ping.

Para hacer ping desde PC1 a PC2:
1. Haz clic derecho en PC1
2. Selecciona "Command line input" (o "Terminal")
3. Escribe el comando: `ping 192.168.1.2`
4. Deberias ver una salida como esta:

```
PING 192.168.1.2 (192.168.1.2): 56 data bytes
64 bytes from 192.168.1.2: icmp_seq=1 ttl=128 time=1 ms
64 bytes from 192.168.1.2: icmp_seq=2 ttl=128 time=0 ms
64 bytes from 192.168.1.2: icmp_seq=3 ttl=128 time=0 ms
64 bytes from 192.168.1.2: icmp_seq=4 ttl=128 time=0 ms
--- 192.168.1.2 ping statistics ---
4 packets transmitted, 4 packets received, 0% packet loss
```

Si ves esto, la red funciona. Si no funciona, revisa:
- Que los cables esten conectados correctamente
- Que las IPs esten en el mismo rango (192.168.1.x)
- Que las mascaras sean iguales (255.255.255.0)

**Paso 6:** Ver el trafico en modo simulacion.

1. En la parte superior derecha, activa el interruptor "Start simulation" (se pondra verde)
2. Repite el ping desde PC1 a PC2
3. Ahora veras animaciones: puntitos moviendose desde PC1 al switch y luego a PC2
4. El switch muestra como aprende la direccion MAC de cada PC

**Paso 7:** Ver la tabla ARP.

En la terminal de PC1, escribe:
```
arp
```

Veras algo como:
```
IP Address      MAC Address
192.168.1.2     AA:BB:CC:DD:EE:02
```

La tabla ARP asocia direcciones IP con direcciones MAC. La primera vez que hiciste ping, se uso ARP para descubrir la MAC de PC2.

### 4. Practica 2 - Red con servidor web en Filius

Ahora agregaremos un servidor web a la red anterior.

**Objetivo:** Configurar un servidor web y acceder a el desde un PC mediante un navegador.

#### Paso a paso

**Paso 1:** Agregar un servidor a la red.
- Arrastra un "Server" (Servidor) al area de trabajo
- Conectalo al switch con un cable de cobre

```
[PC1]     [PC2]     [PC3]    [SERVIDOR WEB]
   \        |        /           /
    [SWITCH PRINCIPAL]----------/
```

**Paso 2:** Configurar la IP del servidor.
- Haz clic derecho en el servidor -> "Configure"
- En la pestana "Network":
  - IP address: 192.168.1.10
  - Subnet mask: 255.255.255.0
  - Gateway: 192.168.1.254
  - OK

**Paso 3:** Habilitar el servicio web en el servidor.
- Con el servidor seleccionado, ve a la pestana "Services" (o haz clic derecho -> "Configure" y busca la pestana de servicios)
- Activa la casilla "Webserver" (Servidor web)
- En el recuadro de contenido HTML, escribe:

```html
<h1>Bienvenido al servidor web de Filius</h1>
<p>Esta es una pagina HTML simple servida por Filius.</p>
<p>Si puedes leer esto, el servidor web funciona correctamente.</p>
```

- Haz clic en "OK"

**Paso 4:** Acceder al servidor web desde PC1.

1. Haz clic derecho en PC1
2. Selecciona "Show web browser" (o "Navegador web")
3. En la barra de direcciones, escribe: `http://192.168.1.10`
4. Presiona Enter
5. Deberias ver la pagina HTML que configuraste

**Paso 5:** Observar los paquetes HTTP en modo simulacion.

1. Activa "Start simulation" si no lo esta
2. Desde PC1, abre el navegador y carga http://192.168.1.10 nuevamente
3. Observa las animaciones:
   - Primero, el PC1 envia una solicitud TCP SYN al servidor (para establecer conexion)
   - El servidor responde con SYN-ACK
   - PC1 envia ACK (conexion establecida, "three-way handshake")
   - PC1 envia la peticion HTTP GET
   - El servidor responde con HTTP 200 OK y el contenido HTML
   - Finaliza la conexion con FIN
4. Cada tipo de paquete se muestra con un color diferente

**Verificacion adicional:**
- Desde PC2, tambien puedes acceder a http://192.168.1.10 (deberia funcionar)
- Desde PC3, intenta hacer `ping 192.168.1.10` para verificar conectividad ICMP

### 5. Practica 3 - Dos redes conectadas por router en Filius

Ahora vamos a crear dos redes separadas y conectarlas mediante un router. Esto es lo que sucede en cualquier red real: diferentes departamentos o sucursales estan en redes diferentes y se comunican a traves de routers.

**Objetivo:** Conectar dos redes diferentes (192.168.1.0/24 y 192.168.2.0/24) mediante un router y verificar que los PCs de una red puedan comunicarse con los de la otra.

#### Paso a paso

**Paso 1:** Crear la Red A (192.168.1.0/24).
- Arrastra 2 PCs y 1 switch al area de trabajo
- Conecta los PCs al switch
- Configura las IPs:
  - PC1-A: 192.168.1.1, mascara 255.255.255.0, gateway 192.168.1.254
  - PC2-A: 192.168.1.2, mascara 255.255.255.0, gateway 192.168.1.254

**Paso 2:** Crear la Red B (192.168.2.0/24).
- Arrastra 2 PCs y 1 switch al area de trabajo
- Conecta los PCs al switch
- Configura las IPs:
  - PC1-B: 192.168.2.1, mascara 255.255.255.0, gateway 192.168.2.254
  - PC2-B: 192.168.2.2, mascara 255.255.255.0, gateway 192.168.2.254

**Paso 3:** Agregar un router con 2 interfaces.
- Arrastra un "Router" al area de trabajo
- Haz clic derecho en el router -> "Configure"
- Veras que tiene multiples interfaces (eth0, eth1, etc.)
- Configura cada interfaz:

  **Interfaz eth0 (conectada a Red A):**
  - IP: 192.168.1.254
  - Mascara: 255.255.255.0
  - Conecta esta interfaz al switch de la Red A

  **Interfaz eth1 (conectada a Red B):**
  - IP: 192.168.2.254
  - Mascara: 255.255.255.0
  - Conecta esta interfaz al switch de la Red B

**Paso 4:** Diagrama final de la red.

```
RED A (192.168.1.0/24)         RED B (192.168.2.0/24)
                             
[PC1-A]   [PC2-A]              [PC1-B]   [PC2-B]
192.168.1.1  192.168.1.2       192.168.2.1  192.168.2.2
    \       /                       \       /
   [SWITCH A]                     [SWITCH B]
        |                              |
   [ROUTER]                            |
   eth0: 192.168.1.254                 |
   eth1: 192.168.2.254 ---------------/
```

**Paso 5:** Verificar conectividad dentro de cada red.

Desde PC1-A, haz ping a PC2-A:
```
ping 192.168.1.2
```
Debe funcionar (estan en la misma red).

Desde PC1-B, haz ping a PC2-B:
```
ping 192.168.2.2
```
Tambien debe funcionar.

**Paso 6:** Verificar conectividad entre redes (a traves del router).

Desde PC1-A, haz ping a PC1-B:
```
ping 192.168.2.1
```

Si todo esta configurado correctamente, deberias ver:

```
PING 192.168.2.1 (192.168.2.1): 56 data bytes
64 bytes from 192.168.2.1: icmp_seq=1 ttl=127 time=2 ms
64 bytes from 192.168.2.1: icmp_seq=2 ttl=127 time=1 ms
...
```

**Nota sobre el TTL:** Observa que el TTL (Time To Live) es 127. Cuando un paquete pasa por un router, el TTL se decrementa en 1. El valor original era 128 (tipico de Windows), y al pasar por el router baja a 127. Esto es evidencia de que el paquete paso por el router.

**Paso 7:** Ver la tabla de enrutamiento del router.

Haz clic derecho en el router -> "Configure" -> busca la pestana "Routing" o "Enrutamiento". Veras algo como:

```
Destination     Netmask          Gateway         Interface
192.168.1.0     255.255.255.0    0.0.0.0         eth0
192.168.2.0     255.255.255.0    0.0.0.0         eth1
```

El router sabe que:
- Los paquetes destinados a 192.168.1.x deben salir por eth0
- Los paquetes destinados a 192.168.2.x deben salir por eth1
- Si un paquete va a otra red no conocida, lo descarta (a menos que tenga una ruta por defecto)

**Que pasa cuando haces ping de PC1-A a PC1-B (paso a paso):**

1. PC1-A (192.168.1.1) quiere enviar un paquete a PC1-B (192.168.2.1)
2. PC1-A compara: mi IP esta en 192.168.1.0/24, destino esta en 192.168.2.0/24 -> son redes diferentes
3. PC1-A envia el paquete a su gateway (192.168.1.254 = router, eth0)
4. El router recibe el paquete por eth0
5. El router mira la IP destino (192.168.2.1) y busca en su tabla de enrutamiento
6. Encuentra: 192.168.2.0/24 -> eth1
7. El router reenvia el paquete por eth1 hacia el switch B
8. El switch B entrega el paquete a PC1-B
9. PC1-B responde y el proceso se invierte

### 6. Cisco Packet Tracer - Introduccion

Cisco Packet Tracer es el simulador oficial de Cisco para preparacion de certificaciones CCNA. Es mas potente y profesional que Filius, pero tambien mas complejo.

#### Que es Packet Tracer?

- Simulador creado por Cisco Systems
- Permite configurar equipos Cisco REALES con comandos IOS (el sistema operativo de Cisco)
- Usado mundialmente para preparar examenes de certificacion (CCNA, CCNP)
- Incluye: routers, switches, firewalls, PCs, servidores, cables, modulos WiFi
- Gratuito pero requiere registro en Cisco NetAcademy

#### Descarga e instalacion

1. Ve a https://www.netacad.com/
2. Crea una cuenta gratuita (Cisco NetAcademy account)
3. Inicia sesion y busca "Packet Tracer" en la seccion de cursos
4. Descarga la version para tu sistema operativo
5. Instala siguiendo los pasos
6. Inicia sesion con tu cuenta de NetAcademy al abrirlo

#### Interfaz de Packet Tracer

```
+--------------------------------------------------+
| Barra de menu                                     |
+--------------------------------------------------+
| [Dispositivos]  [Conexiones]  [Escenarios]        |
| +---------+                                       |
| | Routers |  Area de trabajo                      |
| | Switches|                                       |
| | PCs     |   [PC1] ----- [Switch] ----- [PC2]    |
| | Servers |                                       |
| | ...     |                                       |
| +---------+                                       |
|                                                    |
| Panel de configuracion (abajo)                    |
| CLI / GUI / Desktop                                |
+--------------------------------------------------+
```

#### Ejemplo rapido: misma topologia de Filius en Packet Tracer

Vamos a recrear la red simple (2 PCs + switch) en Packet Tracer.

**Paso 1:** Agregar dispositivos.
- En la barra inferior izquierda, selecciona "End Devices"
- Arrastra 2 "PC" al area de trabajo
- Selecciona "Switches"
- Arrastra 1 "Switch 2960" al area de trabajo

**Paso 2:** Conectar dispositivos.
- Selecciona "Connections" (rayo)
- Elige "Copper Straight-Through"
- Haz clic en PC1, selecciona "FastEthernet0"
- Haz clic en el switch, selecciona un puerto (ej: FastEthernet0/1)
- Repite para PC2 -> FastEthernet0/2 del switch

**Paso 3:** Configurar IPs en los PCs.
- Haz clic en PC1 -> pestana "Desktop" -> "IP Configuration"
  - IP: 192.168.1.1, Mask: 255.255.255.0, Gateway: 192.168.1.254
- Haz clic en PC2 -> "Desktop" -> "IP Configuration"
  - IP: 192.168.1.2, Mask: 255.255.255.0, Gateway: 192.168.1.254

**Paso 4:** Hacer ping desde PC1.
- En PC1 -> "Desktop" -> "Command Prompt"
- Escribe: `ping 192.168.1.2`
- Veras las respuestas.

**Comandos basicos de configuracion en routers Cisco (CLI):**

Si agregas un router Cisco 1841 o 4321, puedes configurarlo mediante CLI:

```
Router> enable
Router# configure terminal
Router(config)# interface gigabitethernet 0/0
Router(config-if)# ip address 192.168.1.254 255.255.255.0
Router(config-if)# no shutdown
Router(config-if)# exit
Router(config)# interface gigabitethernet 0/1
Router(config-if)# ip address 192.168.2.254 255.255.255.0
Router(config-if)# no shutdown
Router(config-if)# end
Router# write memory
```

**Explicacion de los comandos:**
- `enable`: Entra al modo privilegiado
- `configure terminal`: Entra al modo de configuracion global
- `interface gigabitethernet 0/0`: Selecciona la interfaz a configurar
- `ip address X.X.X.X Y.Y.Y.Y`: Asigna IP y mascara
- `no shutdown`: Activa la interfaz (por defecto estan apagadas)
- `end`: Vuelve al modo privilegiado
- `write memory`: Guarda la configuracion

### 7. Ejercicios de simulacion

#### Ejercicio 1: Simular una red con DHCP en Filius

**Enunciado:** Configurar un servidor DHCP en Filius para que los PCs obtengan direcciones IP automaticamente.

**Objetivo:** Que los PCs reciban IP, mascara y gateway del servidor DHCP sin configuracion manual.

##### Solucion paso a paso

**Paso 1:** Crear la red base.
- Arrastra 3 PCs y 1 switch al area de trabajo
- Arrastra 1 servidor (actuara como DHCP)
- Conecta todos los dispositivos al switch con cables de cobre

**Paso 2:** Configurar el servidor DHCP.

Haz clic derecho en el servidor -> "Configure":
- IP: 192.168.1.10 (fija, el servidor DHCP necesita IP fija)
- Mascara: 255.255.255.0
- Gateway: 192.168.1.254

En la pestana "Services" o "DHCP":
- Activa "DHCP server"
- Configura:
  - IP starting address: 192.168.1.100 (desde donde empieza a asignar)
  - Number of addresses: 50 (cuantas IPs puede asignar)
  - Subnet mask: 255.255.255.0
  - Default gateway: 192.168.1.254
  - DNS server: 192.168.1.10 (el mismo servidor, opcional)
  - Haz clic en "OK"

**Paso 3:** Configurar los PCs para DHCP (automatico).

Para CADA PC:
- Haz clic derecho en el PC -> "Configure"
- En la pestana "Network", selecciona la opcion "Obtain IP address automatically" (o equivalente)
- Esto hara que el PC envie una solicitud DHCP al iniciar
- Haz clic en "OK"

**Paso 4:** Verificar que los PCs reciben IP.

Enciende la simulacion (Start simulation). Cada PC deberia enviar una solicitud DHCP.

Para ver la IP asignada a un PC:
- Haz clic derecho en PC1 -> "Command line input"
- Escribe: `ipconfig`
- Deberias ver algo como:

```
IP address: 192.168.1.100
Subnet mask: 255.255.255.0
Default gateway: 192.168.1.254
DNS server: 192.168.1.10
```

**Paso 5:** Verificar conectividad.
- Desde PC1 (192.168.1.100), haz ping a PC2 (deberia tener 192.168.1.101)
- Si funciona, el DHCP esta configurado correctamente

**Explicacion de como funciona DHCP (paso a paso):**

Cuando un PC se configura como DHCP, ocurre lo siguiente (DORA process):

1. **Discover:** El PC envia un mensaje broadcast "Hay algun servidor DHCP por ahi?"
2. **Offer:** El servidor DHCP responde "Si, puedo ofrecerte la IP 192.168.1.100"
3. **Request:** El PC dice "Gracias, acepto la IP 192.168.1.100"
4. **Acknowledge:** El servidor confirma "OK, 192.168.1.100 es tuya por 24 horas (lease)"

En Filius, puedes ver estos 4 mensajes si activas la simulacion y observas el trafico entre el PC y el servidor.

#### Ejercicio 2: VLANs en Filius (concepto)

**Enunciado:** Aunque Filius tiene soporte limitado para VLANs, vamos a simular el concepto: crear dos grupos de PCs que NO puedan verse entre si, usando dos switches separados. Luego explicaremos como se haria con VLANs reales.

**Objetivo:** Entender el concepto de segmentacion de red.

##### Solucion paso a paso

**Paso 1:** Crear dos redes separadas (simulando VLAN10 y VLAN20).

**Red A (VLAN 10 - "Administracion"):**
- 2 PCs (PC-A1, PC-A2) + 1 switch
- Red: 192.168.10.0/24
- IPs: PC-A1 = 192.168.10.1, PC-A2 = 192.168.10.2
- Gateway: 192.168.10.254

**Red B (VLAN 20 - "Produccion"):**
- 2 PCs (PC-B1, PC-B2) + 1 switch
- Red: 192.168.20.0/24
- IPs: PC-B1 = 192.168.20.1, PC-B2 = 192.168.20.2
- Gateway: 192.168.20.254

**Paso 2:** No conectar los switches entre si.

```
RED A (VLAN 10)                RED B (VLAN 20)
[PC-A1] [PC-A2]                [PC-B1] [PC-B2]
    \    /                          \    /
  [SWITCH-A]                     [SWITCH-B]
    192.168.10.x                   192.168.20.x
```

**Paso 3:** Verificar que NO hay comunicacion entre VLANs.

Desde PC-A1, intenta hacer ping a PC-B1:
```
ping 192.168.20.1
```

**Resultado:** FALLA. No hay ruta entre las redes porque no hay router que las conecte.

**Explicacion:**

Con VLANs reales (en un switch gestionable), podrias tener AMBOS grupos conectados al MISMO switch fisico, pero separados logicamente:

```
En un switch gestionable con VLANs:

Puerto 1-4: VLAN 10 (Administracion)
Puerto 5-8: VLAN 20 (Produccion)

El switch se comporta como si fueran dos switches separados.
PC-A1 (puerto 1, VLAN 10) NO puede ver a PC-B1 (puerto 5, VLAN 20)
```

**Para que se comuniquen**, necesitarian un router con una interfaz en cada VLAN (router-on-a-stick) o un switch de capa 3. Eso se configura asi en Packet Tracer:

```
En el switch:
Switch(config)# vlan 10
Switch(config-vlan)# name Administracion
Switch(config)# vlan 20
Switch(config-vlan)# name Produccion

Switch(config)# interface fastethernet 0/1
Switch(config-if)# switchport mode access
Switch(config-if)# switchport access vlan 10

Switch(config)# interface fastethernet 0/5
Switch(config-if)# switchport mode access
Switch(config-if)# switchport access vlan 20

Switch(config)# interface fastethernet 0/24
Switch(config-if)# switchport mode trunk  (puerto al router)
```

#### Ejercicio 3: Simular ataque ARP Spoofing en Filius

**Enunciado:** Simular un ataque ARP spoofing (suplantacion ARP) donde un atacante intercepta el trafico entre dos dispositivos.

**Importante:** Este ejercicio es SOLO con fines educativos. Realizar ARP spoofing en redes reales sin permiso es ilegal.

**Objetivo:** Entender como funciona un ataque Man-in-the-Middle (MitM) a nivel de capa 2.

##### Solucion paso a paso

**Paso 1:** Crear la red con 3 PCs.

- PC1 (Victima A): 192.168.1.1
- PC2 (Gateway/Router simulado): 192.168.1.254
- PC3 (Atacante): 192.168.1.3
- 1 switch que conecta a los 3

Diagrama:
```
[PC1 - Victima A]     [PC3 - Atacante]
  192.168.1.1          192.168.1.3
       \                   /
        [SWITCH]
           |
    [PC2 - Gateway]
     192.168.1.254
```

**Paso 2:** Configuracion normal (sin ataque).

- Configura las IPs de cada PC como se indica arriba
- Desde PC1, haz ping a PC2 (192.168.1.254) -> debe funcionar
- Verifica la tabla ARP de PC1: `arp` -> debe mostrar la MAC de PC2

**Paso 3:** Simular el ataque ARP spoofing.

Filius no tiene una herramienta automatica para ARP spoofing, pero podemos simularlo manualmente modificando la tabla ARP:

En PC3 (el atacante):
1. Abre la terminal
2. Ejecuta: `arp -s 192.168.1.254 AA:BB:CC:DD:EE:03` (asigna la IP del gateway a la MAC de PC3)
3. Ahora PC3 le dice a PC1 que el gateway (192.168.1.254) tiene la MAC de PC3

En PC1 (la victima):
1. Verifica su tabla ARP: `arp`
2. Si el ataque funciono, la MAC de 192.168.1.254 ahora es la MAC de PC3

**Explicacion:**

En un ataque ARP spoofing real, el atacante envia mensajes ARP falsos a la red, diciendo:
- "La IP 192.168.1.254 (gateway) tiene mi MAC (la del atacante)"
- "La IP 192.168.1.1 (victima) tiene mi MAC (la del atacante)"

Esto hace que todo el trafico entre la victima y el gateway pase por el atacante, quien puede:
- **Interceptar:** Ver todo el trafico (passive sniffing)
- **Modificar:** Cambiar datos antes de reenviarlos (active modification)
- **Bloquear:** No reenviar los paquetes (denial of service)

**Como prevenir ARP spoofing:**
- **ARP spoofing detection:** Herramientas como Arpwatch, Snort, o Wireshark pueden detectar respuestas ARP anormales
- **ARP staticas:** Configurar entradas ARP estaticas en dispositivos criticos (no escalable en redes grandes)
- **Dynamic ARP Inspection (DAI):** Funcion de switches gestionables que valida respuestas ARP contra el DHCP snooping binding table
- **Segmentacion de red:** Con VLANs, el ataque queda limitado a la misma VLAN
- **Encriptacion:** Si el trafico esta cifrado (HTTPS, SSH, VPN), el atacante no puede leer los datos aunque los intercepte

### 8. Preguntas y Respuestas

#### Pregunta 1
**Cual es la diferencia entre un simulador y un emulador de redes?**

**Respuesta:** Un **simulador** (como Filius) imita el comportamiento de una red a alto nivel. Los comandos son simplificados, los protocolos se implementan de forma basica, y el objetivo es educativo. Un **emulador** (como GNS3 o EVE-NG) ejecuta el sistema operativo REAL de los dispositivos. Por ejemplo, GNS3 puede ejecutar una imagen real de Cisco IOS, con todos los comandos reales y el comportamiento exacto. Los emuladores son mas realistas pero requieren mas recursos (memoria, CPU, imagenes legales de los sistemas operativos). Filius es simulador; Packet Tracer esta a medio camino (simula el comportamiento de IOS pero no ejecuta el sistema real).

#### Pregunta 2
**Para que sirve un servidor DHCP?**

**Respuesta:** Un servidor DHCP (Dynamic Host Configuration Protocol) asigna automaticamente direcciones IP y otra configuracion de red (mascara, gateway, DNS) a los dispositivos cuando se conectan a la red. Sirve para: (1) evitar configurar manualmente cada dispositivo, (2) evitar conflictos de IP duplicadas, (3) reutilizar IPs cuando los dispositivos se desconectan, (4) centralizar la administracion de direccionamiento. Sin DHCP, en una empresa con 500 PCs, alguien tendria que configurar manualmente cada uno y llevar un registro de que IP tiene cada cual.

#### Pregunta 3
**Que comando se usa para ver la tabla ARP en Windows y en Linux?**

**Respuesta:** En ambos sistemas se usa el comando `arp -a`. Tambien se puede usar `arp` sin argumentos para ver la sintaxis. En Windows, `arp -a` muestra la tabla ARP completa. En Linux, tambien se puede usar `ip neigh` (neighbor table) que es el comando moderno equivalente. La tabla ARP muestra las asociaciones entre direcciones IP y direcciones MAC de los dispositivos con los que nos hemos comunicado recientemente.

#### Pregunta 4
**Que hace el router cuando recibe un paquete destinado a otra red?**

**Respuesta:** El router realiza los siguientes pasos: (1) Recibe el paquete por una interfaz, (2) Examina la direccion IP de destino, (3) Consulta su tabla de enrutamiento para encontrar la ruta mas especifica que coincida con el destino, (4) Si encuentra una ruta, decrementa el TTL (Time To Live) del paquete, (5) Recalcula el checksum, (6) Reenvia el paquete por la interfaz de salida correspondiente, (7) Si no encuentra una ruta, descarta el paquete y envia un mensaje ICMP "Destination Unreachable" al origen. Este proceso se llama "forwarding" (reenvio) y es la funcion principal de un router.

#### Pregunta 5
**Cual es la diferencia principal entre Filius y Cisco Packet Tracer?**

**Respuesta:** Las diferencias principales son: (1) **Complejidad:** Filius es mucho mas simple e intuitivo, ideal para principiantes; Packet Tracer es mas complejo y profesional. (2) **Comandos:** Filius usa comandos simplificados; Packet Tracer usa comandos reales de Cisco IOS. (3) **Protocolos:** Packet Tracer soporta muchos mas protocolos (OSPF, EIGRP, STP, etc.). (4) **Costo:** Ambos son gratuitos, pero Packet Tracer requiere registro en Cisco NetAcademy. (5) **Uso:** Filius es para aprender conceptos basicos; Packet Tracer es para preparar certificaciones CCNA. (6) **VLANs:** Packet Tracer tiene soporte completo de VLANs, trunking, VTP; Filius tiene soporte limitado.

#### Pregunta 6
**Que es el three-way handshake en TCP?**

**Respuesta:** Es el proceso de tres pasos para establecer una conexion TCP entre dos dispositivos: (1) **SYN:** El cliente envia un paquete con el flag SYN (synchronize) activado, indicando que quiere iniciar una conexion, junto con un numero de secuencia inicial (ISN). (2) **SYN-ACK:** El servidor responde con un paquete que tiene los flags SYN y ACK activados, confirmando la recepcion y enviando su propio numero de secuencia. (3) **ACK:** El cliente envia un paquete ACK final confirmando. A partir de este momento, la conexion esta establecida y pueden intercambiarse datos. En Filius, puedes ver este proceso cuando un PC se conecta a un servidor web (los tres paquetes se muestran antes de la peticion HTTP GET).

---

## Tarea / Lectura Recomendada

1. **Practicar:** Descarga Filius y reproduce las 3 practicas de esta clase (red simple, servidor web, dos redes con router)
2. **Practicar:** Disena en Filius una red con 4 PCs, 2 switches y 1 router. Configura 2 redes diferentes (192.168.10.0/24 y 192.168.20.0/24) y verifica conectividad entre ellas
3. **Practicar:** Configura un servidor DHCP en Filius y haz que 3 PCs obtengan IP automaticamente. Verifica las IPs asignadas
4. **Explorar:** Registrate en Cisco NetAcademy (gratis) y descarga Packet Tracer. Recrea la misma topologia de la Practica 3
5. **Leer:** "Packet Guide to Core Network Protocols" de Bruce Hartpence - capitulo sobre ARP
6. **Leer:** RFC 2131 - Dynamic Host Configuration Protocol (DHCP)
7. **Ver:** Video "Filius Network Simulator Tutorial" en YouTube (buscar en ingles o espanol)
8. **Profundizar:** Investiga la diferencia entre hubs, switches y routers. En Filius, prueba conectar PCs con un hub (si esta disponible) y observa la diferencia en el trafico
