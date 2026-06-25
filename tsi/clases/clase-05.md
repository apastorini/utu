# Clase 5: Fundamentos de Redes - Componentes, Topologias y Modelo OSI/TCP-IP

**Duracion:** 2 horas

---

## Objetivos de Aprendizaje

1. Comprender los componentes fisicos y logicos que forman una red
2. Identificar y diferenciar las topologias de red con sus ventajas y desventajas
3. Entender los modelos OSI (7 capas) y TCP/IP como marcos de referencia
4. Explicar el flujo de datos a traves de las capas usando encapsulamiento

---

## Contenido Detallado

### 1. Que es una red?

Una red de computadoras es un conjunto de dispositivos conectados entre si que pueden compartir informacion y recursos.

**Analogia del sistema de correo:** Imagina que quieres enviar una carta a un amigo en otra ciudad. Tu escribes la carta (datos), la pones en un sobre (encapsulas), escribes la direccion (destino), la llevas al correo (interfaz de red), el correo la transporta por camiones y aviones (medios de transmision), y finalmente llega al destino. Una red funciona igual: tus datos viajan desde tu computadora hasta el destino pasando por diferentes "oficinas de correo" (routers, switches).

**Analogia de las carreteras:** La red es como un sistema de carreteras. Los datos son los autos, las direcciones IP son como las direcciones de las casas, los routers son como las intersecciones donde decides que camino tomar, y los switches son como las calles locales dentro de un vecindario.

```
Componentes basicos de una comunicacion en red:

[Origen] ---> [Medio de transmision] ---> [Destino]
  (emisor)       (cables, wifi)           (receptor)
```

### 2. Componentes fisicos de una red

Cada componente tiene un rol especifico. Vamos a verlos uno por uno con analogias sencillas.

#### NIC (Network Interface Card)

Es la "boca" de la computadora. Sin ella, la computadora no puede hablar con otras. Es una tarjeta (integrada o externa) que permite conectarse a la red.

- **Analogia:** Es como el altavoz y microfono de un telefono. Sin ellos, no puedes comunicarte.
- **Direccion MAC:** Cada NIC tiene una direccion unica e irrepetible a nivel mundial, asignada por el fabricante. Es como tu DNI: identifica tu dispositivo de forma unica. Formato: `00:1A:2B:3C:4D:5E` (6 pares de hexadecimales, 48 bits).
- **Cable o WiFi:** La NIC puede ser ethernet (cable RJ45) o inalambrica (WiFi).

#### Switch

Dispositivo que conecta multiples dispositivos dentro de la MISMA red local (LAN).

- **Analogia:** Es como la mesa de un centro de mensajeria donde trabajan varios mensajeros. Cuando llega un paquete, el mensajero revisa su libreta para saber a que escritorio entregarlo.
- **Como funciona:** El switch mantiene una **tabla MAC** que asocia cada direccion MAC con el puerto fisico donde esta conectado ese dispositivo. Cuando recibe un paquete, busca la MAC destino en su tabla y lo envia solo por el puerto correspondiente.
- **Diferencia con hub:** Un hub repite todo a todos los puertos (como gritar en una habitacion). Un switch solo envia al destino correcto (como susurrar a la persona indicada). El switch es mas eficiente y seguro.

```
Tabla MAC del switch:
+------------+-------------------+
| Puerto     | MAC               |
+------------+-------------------+
| 1          | AA:BB:CC:DD:EE:01 |
| 2          | AA:BB:CC:DD:EE:02 |
| 3          | AA:BB:CC:DD:EE:03 |
+------------+-------------------+
```

#### Router

Dispositivo que conecta DIFERENTES redes entre si. Es el "guardia de trafico" que sabe como llegar a otras redes.

- **Analogia:** Es como una oficina central de correos que sabe como enviar paquetes a diferentes ciudades. No conoce todas las casas (direcciones MAC), pero conoce las rutas hacia otras ciudades (redes).
- **Puerta de enlace (gateway):** Es la direccion IP del router dentro de tu red local. Todos los dispositivos de tu red envian trafico hacia afuera a traves de esta puerta de enlace.
- **Enrutamiento:** El router mantiene una **tabla de enrutamiento** que le dice por donde enviar paquetes segun su direccion IP de destino.

#### Access Point (AP)

Dispositivo que permite conexion inalambrica (Wi-Fi). Extiende la red para que dispositivos sin cable puedan conectarse.

- **Analogia:** Es como un repetidor de senal de radio. Tu telefono envía la senal al AP, y el AP la convierte en cableada hacia el switch/router.

#### Cables

- **Cable Ethernet (par trenzado):** Categoria 5 (Cat5): 100 Mbps, Cat5e: 1 Gbps, Cat6: 1-10 Gbps. Tienen conectores RJ45.
- **Fibra optica:** Usa luz para transmitir datos. Mucho mayor velocidad y distancia que el cobre. Inmune a interferencias electromagneticas.
- **Coaxial:** Como el cable de TV. Hoy menos usado en redes de datos.

#### Firewall

Dispositivo (o software) que filtra el trafico de red basado en reglas de seguridad.

- **Analogia:** Es como un guardia de seguridad en la entrada de un edificio. Revisa a todos los que entran y salen, y decide si los deja pasar segun las reglas establecidas.
- **Tipos:** Firewall de red (hardware), firewall de aplicacion (software como iptables, Windows Firewall), WAF (Web Application Firewall).

#### Diagrama de red simple

```
                    INTERNET
                        |
                    [MODEM]
                        |
                    [FIREWALL]
                        |
                    [ROUTER]
                     /    \
                    /      \
              [SWITCH1]  [SWITCH2]
              /    |    \     |
             /     |     \    |
          [PC1]  [PC2]  [AP]  [SERVER]
                           |
                        [LAPTOP]
                         (WiFi)

Componentes: MODEM (convierte senal ISP), FIREWALL (filtra), ROUTER (enruta),
SWITCH (conecta local), AP (WiFi), PC/LAPTOP (usuarios), SERVER (servicios)
```

### 3. Topologias de red

La topologia es la forma en que los dispositivos estan conectados entre si. Hay dos tipos: **fisica** (como estan conectados los cables) y **logica** (como fluyen los datos).

#### Topologia Estrella

Todos los dispositivos se conectan a un punto central (switch/hub).

```
            [PC1]
              |
            [SWITCH]----[PC2]
              |
            [PC3]
```

| Ventajas | Desventajas |
|----------|-------------|
| Si un cable falla, solo ese dispositivo pierde conexion | Si el switch falla, toda la red cae |
| Facil de agregar dispositivos | Requiere mas cable que bus |
| Facil de diagnosticar problemas | |

#### Topologia Bus

Todos los dispositivos comparten un unico cable (bus).

```
[PC1]----[PC2]----[PC3]----[PC4]
                (cable unico)
```

| Ventajas | Desventajas |
|----------|-------------|
| Poco cable, facil instalacion | Si el cable principal falla, toda la red cae |
| Economica para redes pequeñas | Dificil de diagnosticar fallas |
| | Solo un dispositivo puede transmitir a la vez (colisiones) |

#### Topologia Anillo

Cada dispositivo conectado a dos vecinos, formando un circulo.

```
     [PC1]
    /     \
[PC4]     [PC2]
    \     /
     [PC3]
```

| Ventajas | Desventajas |
|----------|-------------|
| Acceso ordenado (token passing) | Si un dispositivo falla, toda la red cae |
| Rendimiento predecible | Dificil de agregar/quitar dispositivos |

#### Topologia Malla

Cada dispositivo conectado a todos los demas (completa) o a varios (parcial).

```
[PC1]----[PC2]
  | \    / |
  |  [PC3] |
  | /   \  |
[PC4]----[PC5]
```

| Ventajas | Desventajas |
|----------|-------------|
| Alta redundancia (rutas alternativas) | Muy costosa por la cantidad de cable |
| Si falla un enlace, hay rutas alternativas | Dificil de instalar y mantener |
| Maxima confiabilidad | No escala bien |

#### Topologia Arbol (Jerarquica)

Combinacion de estrellas conectadas en jerarquia. Es la mas usada en empresas.

```
            [RAIZ]
              |
          [SWITCH]
         /    |    \
     [SW]   [SW]   [SW]
      |      |      |
    [PCs]  [PCs]  [PCs]
```

| Ventajas | Desventajas |
|----------|-------------|
| Escalable: se pueden agregar mas niveles | Si el nodo raiz falla, toda la red cae |
| Facil de administrar por segmentos | Mas cable que topologia estrella simple |
| Segmentacion natural de redes | |

### 4. Modelo OSI (7 Capas)

El modelo OSI (Open Systems Interconnection) es un marco conceptual que divide la comunicacion en red en 7 capas. Cada capa tiene una funcion especifica y se comunica con las capas adyacentes.

**Analogia del edificio de oficinas:** Imagina un edificio de 7 pisos. Cada piso hace una tarea especifica:
- Piso 7 (Aplicacion): Donde los usuarios trabajan con programas (WhatsApp, Chrome)
- Piso 6 (Presentacion): Traduce documentos a diferentes idiomas
- Piso 5 (Sesion): Abre y cierra las puertas de las reuniones
- Piso 4 (Transporte): El ascensor que lleva paquetes entre pisos, asegurando que lleguen completos
- Piso 3 (Red): El mapa de la ciudad para saber a donde ir
- Piso 2 (Enlace): El cartero que entrega en la direccion exacta de la casa
- Piso 1 (Fisica): Los cables de luz/carreteras por donde viaja el cartero

| Capa | Nombre | Funcion | Ejemplos | Protocolos |
|------|--------|---------|----------|------------|
| 7 | Aplicacion | Interfaz con el usuario | Navegador web, email, transferencia archivos | HTTP, FTP, SMTP, DNS, DHCP |
| 6 | Presentacion | Traduccion, cifrado, compresion | Convertir datos a formato estandar | SSL/TLS, JPEG, MPEG, ASCII |
| 5 | Sesion | Establece, mantiene y cierra sesiones | Control de dialogo entre aplicaciones | NetBIOS, RPC, PPTP |
| 4 | Transporte | Transporte confiable, control de flujo | Segmentacion de datos, control errores | TCP, UDP |
| 3 | Red | Enrutamiento y direccionamiento logico | Determinar la mejor ruta al destino | IP, ARP, ICMP, OSPF, BGP |
| 2 | Enlace de Datos | Acceso al medio, direccionamiento fisico | Tramas, control de errores, acceso al medio | Ethernet, WiFi, PPP, MAC |
| 1 | Fisica | Transmision de bits a traves del medio | Voltajes, frecuencias, conectores | RJ45, fibra, coaxial, wireless |

#### Explicacion sencilla de cada capa:

- **Capa 7 - Aplicacion:** Es lo que el usuario ve. Cuando abres Chrome y escribes una URL, estas usando HTTP (capa 7). No es la aplicacion en si (Chrome), sino el protocolo que usa.

- **Capa 6 - Presentacion:** Traduce los datos a un formato que la aplicacion pueda entender. Por ejemplo, cuando ves una pagina web, los datos llegan comprimidos y esta capa los descomprime. Tambien maneja cifrado (SSL/TLS).

- **Capa 5 - Sesion:** Administra las sesiones entre aplicaciones. Abre, mantiene y cierra la conexion. Como cuando inicias sesion en un banco: esta capa maneja esa sesion.

- **Capa 4 - Transporte:** Decide COMO enviar los datos. TCP es como una llamada telefonica (confirma que todo llego, ordenado). UDP es como enviar una carta por correo normal (no sabes si llego, pero es mas rapido).

- **Capa 3 - Red:** Decide A DONDE ir. Agrega las direcciones IP de origen y destino. Los routers trabajan aqui, decidiendo la mejor ruta.

- **Capa 2 - Enlace de Datos:** Prepara los datos para el medio fisico. Agrega direcciones MAC. Los switches trabajan aqui. Divide los datos en tramas.

- **Capa 1 - Fisica:** Los bits reales viajando por el cable (unos y ceros convertidos en voltajes o pulsos de luz).

#### Encapsulamiento

Cuando los datos viajan de una computadora a otra, pasan por las capas en orden. En el origen, bajan de la capa 7 a la capa 1. En el destino, suben de la capa 1 a la capa 7.

Cada capa agrega su propia "etiqueta" (cabecera) a los datos. Esto se llama encapsulamiento.

```
Flujo de encapsulamiento al enviar datos:

[Capa 7] Datos del usuario (ej: "Hola")
[Capa 6] Datos formateados
[Capa 5] Datos + control de sesion
[Capa 4] SEGMENTOS: Datos + Puerto origen/destino (TCP/UDP)
[Capa 3] PAQUETES: Segmento + IP origen/destino
[Capa 2] TRAMAS: Paquete + MAC origen/destino + CRC
[Capa 1] BITS: 101001000101... (voltajes/luz)

Visual:
+-----------------------------+
|  Datos de aplicación        |  Capa 7
+-----------------------------+
+--------+--------------------+
|L7 Header|  Datos            |  Capa 6
+--------+--------------------+
+-------+--------+-----------+
|L6 Hdr |L7 Hdr  | Datos     |  Capa 5
+-------+--------+-----------+
+------+-------+--------+----+
|L5 Hdr|L6 Hdr |L7 Hdr  |Dats|  Capa 4
+------+-------+--------+----+
| L4 Header (TCP/UDP)        |  Segmento
+----------------------------+
| L3 Header (IP)             |  Paquete
+----------------------------+
| L2 Header (MAC)  | Trailer |  Trama
+----------------------------+
|  Bits (capa fisica)        |
+----------------------------+
```

### 5. Modelo TCP/IP (4/5 Capas)

El modelo TCP/IP es el modelo PRACTICO que usa Internet. Es mas simple que OSI: tiene 4 o 5 capas (dependiendo de la referencia).

```
Comparacion OSI vs TCP/IP:

Modelo OSI (7)          Modelo TCP/IP (4-5)
+------------------+    +------------------+
| 7. Aplicacion    |    | Aplicacion       |
| 6. Presentacion  |--->| (HTTP, FTP, DNS) |
| 5. Sesion        |    +------------------+
+------------------+    | Transporte       |
| 4. Transporte    |--->| (TCP, UDP)       |
+------------------+    +------------------+
| 3. Red           |--->| Internet / Red   |
|                   |    | (IP, ARP, ICMP)  |
+------------------+    +------------------+
| 2. Enlace        |--->| Acceso a Red     |
| 1. Fisica        |    | (Ethernet, WiFi) |
+------------------+    +------------------+
```

#### Protocolos clave del modelo TCP/IP:

| Protocolo | Capa | Funcion |
|-----------|------|---------|
| HTTP/HTTPS | Aplicacion | Transferencia de paginas web |
| FTP | Aplicacion | Transferencia de archivos |
| SMTP | Aplicacion | Envio de correo electronico |
| DNS | Aplicacion | Traduce nombres (google.com) a IPs (142.250....). Es como la guia telefonica de Internet |
| DHCP | Aplicacion | Asigna automaticamente direcciones IP a los dispositivos. Como el empleado que te da una oficina cuando llegas |
| TCP | Transporte | Protocolo CONFIABLE: confirma recepcion, reenvia paquetes perdidos, ordena los datos. Como una llamada telefónica donde confirmas que escuchaste |
| UDP | Transporte | Protocolo RAPIDO pero NO confiable: no confirma, no reordena. Como enviar un mensaje de voz: si se pierde, se pierde. Usado en streaming, videojuegos, VoIP |
| IP | Internet/Red | Enruta paquetes entre redes usando direcciones IP |
| ARP | Internet/Red | Traduce direcciones IP a direcciones MAC. Como preguntar "cual es la MAC de la IP 192.168.1.1?" |
| ICMP | Internet/Red | Mensajes de error y diagnostico. El comando `ping` usa ICMP |

### 6. Direcciones MAC vs IP

| Caracteristica | MAC | IP |
|----------------|-----|-----|
| **Funcion** | Identifica el dispositivo fisico | Identifica la ubicacion en la red |
| **Capa OSI** | Capa 2 (Enlace de Datos) | Capa 3 (Red) |
| **Formato** | 00:1A:2B:3C:4D:5E (hexadecimal) | IPv4: 192.168.1.1 (decimal) |
| **Longitud** | 48 bits (6 bytes) | IPv4: 32 bits (4 bytes), IPv6: 128 bits |
| **Asignacion** | Por el fabricante (quemada en hardware) | Por administrador o DHCP |
| **Unicidad** | Unica mundialmente (teoricamente) | Unica dentro de su red |
| **Cambio** | Permanente (se puede cambiar por software) | Cambia segun la red a la que te conectes |

**Analogia:** La MAC es como tu nombre completo (no cambia, te identifica desde que naces). La IP es como tu direccion actual (cambia si te mudas).

**IPv4:** 32 bits. Se escribe como 4 numeros decimales separados por puntos: `192.168.1.1`
- Cada numero va de 0 a 255 (8 bits = 1 byte = 1 octeto)
- Ejemplo: `192.168.1.1` -> en binario: `11000000.10101000.00000001.00000001`

**IPv6:** 128 bits. Se escribe como 8 grupos de 4 digitos hexadecimales separados por dos puntos:
- Ejemplo: `2001:0db8:85a3:0000:0000:8a2e:0370:7334`
- Se puede abreviar: `2001:db8:85a3::8a2e:370:7334` (los ceros a la izquierda se omiten, y un grupo de ceros consecutivos se reemplaza por `::`)

---

## Ejercicio 1: Identificar Componentes de Red

**Enunciado:** Dado el siguiente diagrama de red, identifica cada componente etiquetado de la A a la J.

```
Diagrama de red:

                         INTERNET
                            |
                           [A]
                            |
                        [B]---[C]
                         |      |
                    +----+      +----+
                    |                 |
                   [D]               [E]
                 /  |  \              |
                /   |   \             |
              [F]  [G]  [H]         [I]
                             \
                              [J]
                          (conexion inalambrica)
```

**Posibles componentes (usar cada uno una vez):**
- Modem, Firewall, Router, Switch, Access Point, PC de escritorio, Servidor, Laptop, Cable Ethernet, Hub

### Solucion

| Etiqueta | Componente | Explicacion |
|----------|------------|-------------|
| **A** | MODEM | Convierte la senal del ISP (Internet) a senal que la red local entiende. Es la puerta de entrada desde Internet |
| **B** | FIREWALL | Filtra el trafico entre Internet y la red interna. Primera linea de defensa |
| **C** | ROUTER | Enruta paquetes entre la red interna y externa. Tiene la tabla de enrutamiento |
| **D** | SWITCH | Conecta los dispositivos de la red local (PCs, servidor) en topologia estrella |
| **E** | SWITCH | Segundo switch para conectar otros dispositivos, incluyendo el servidor |
| **F** | PC DE ESCRITORIO | Computadora de usuario conectada por cable al switch |
| **G** | PC DE ESCRITORIO | Otra computadora de usuario |
| **H** | PC DE ESCRITORIO | Tercera computadora de usuario |
| **I** | SERVIDOR | Provee servicios (archivos, BD, web) a la red |
| **J** | ACCESS POINT | Provee conexion inalambrica. La laptop se conecta via WiFi |

**Nota:** No se uso "Hub" porque los switches son preferibles en disenos modernos. Un hub solo repetiria el trafico a todos los puertos, mientras que un switch lo dirige selectivamente.

---

## Ejercicio 2: Mapeo OSI

**Enunciado:** Clasifica cada una de las siguientes tecnologias/protocolos en la capa del modelo OSI que le corresponde. Justifica brevemente.

Lista: HTTP, TCP, IP, Ethernet, SSL/TLS, UDP, ARP, DNS, DHCP, WiFi (802.11)

### Solucion

| Tecnologia | Capa OSI | Justificacion |
|------------|----------|---------------|
| **HTTP** | 7 - Aplicacion | Protocolo de transferencia de hipertexto. Usado por navegadores para obtener paginas web |
| **SSL/TLS** | 6 - Presentacion (o 5-6) | Cifra los datos de la sesion. Provee seguridad en la capa de presentacion (aunque algunos lo ubican entre sesion y transporte) |
| **DNS** | 7 - Aplicacion | Resuelve nombres de dominio a direcciones IP. El usuario interactua indirectamente con el |
| **DHCP** | 7 - Aplicacion | Asigna direcciones IP automaticamente. Opera a nivel de aplicacion sobre UDP |
| **TCP** | 4 - Transporte | Protocolo orientado a conexion, confiable. Segmenta los datos y asegura su entrega ordenada |
| **UDP** | 4 - Transporte | Protocolo no orientado a conexion, rapido pero no confiable. Sin control de flujo ni recuperacion de errores |
| **IP** | 3 - Red | Protocolo de Internet. Enruta paquetes entre redes usando direcciones logicas (IP) |
| **ARP** | 3 - Red (enlace entre capa 2 y 3) | Traduce direcciones IP a direcciones MAC. Opera en la interfaz entre capa 2 y 3 |
| **Ethernet** | 2 - Enlace de Datos | Define como se formatean los datos en tramas y como se accede al medio fisico. Usa direcciones MAC |
| **WiFi (802.11)** | 1 y 2 - Fisica y Enlace | Define tanto la transmision por ondas de radio (fisica) como el acceso al medio (enlace) |

---

## Ejercicio 3: Flujo de Datos - HTTP desde el Navegador al Servidor

**Enunciado:** Explica paso a paso como viaja un paquete HTTP desde que escribes `http://www.ejemplo.com` en tu navegador hasta que el servidor web responde. Usa el modelo TCP/IP (o OSI) para describir cada paso.

### Solucion paso a paso

**Paso 1: El usuario escribe la URL en el navegador**

El usuario ingresa `http://www.ejemplo.com` en la barra de direcciones. Esto ocurre en la capa de APLICACION.

**Paso 2: Resolucion de DNS (Aplicacion)**

El navegador necesita saber la direccion IP de `www.ejemplo.com`. Pregunta al servidor DNS:
- El SO revisa primero la cache local (archivo hosts)
- Si no esta, pregunta al servidor DNS configurado (ej: 8.8.8.8 de Google)
- El DNS responde: `www.ejemplo.com` = `93.184.216.34`

```
[PC] -- "Cual es la IP de www.ejemplo.com?" --> [Servidor DNS]
[PC] <-- "93.184.216.34" ---------------------- [Servidor DNS]
```

**Paso 3: Preparacion en capa de Aplicacion (Capa 7)**

El navegador construye una peticion HTTP:
```http
GET / HTTP/1.1
Host: www.ejemplo.com
User-Agent: Chrome/120.0
```

**Paso 4: Capa de Transporte - TCP (Capa 4)**

Antes de enviar datos, se establece una conexion TCP con el servidor (Three-way handshake):

```
[PC] ---- SYN (seq=100) ---------------> [Servidor]
[PC] <--- SYN-ACK (seq=300, ack=101) --- [Servidor]
[PC] ---- ACK (seq=101, ack=301) ------> [Servidor]

(conexion establecida)
```

Luego, los datos HTTP se dividen en segmentos:
- Se agrega puerto origen (aleatorio, ej: 54321)
- Se agrega puerto destino (80 para HTTP, 443 para HTTPS)
- El segmento TCP tiene: cabecera TCP (20 bytes) + datos HTTP

```
Segmento TCP:
+------------------+------------------+------------------+
| Puerto Origen    | Puerto Destino   | Numero de Seq    |
| (54321)          | (80)             | (101)            |
+------------------+------------------+------------------+
| ACK              | Checksum         | Datos HTTP       |
| (301)            | (X)              | (GET / HTTP/1.1) |
+------------------+------------------+------------------+
```

**Paso 5: Capa de Red - IP (Capa 3)**

Se crea un paquete IP agregando:
- Direccion IP origen: 192.168.1.10 (tu PC)
- Direccion IP destino: 93.184.216.34 (servidor)
- TTL (Time To Live): 64 (numero de saltos maximos)
- Protocolo: 6 (TCP)

```
Paquete IP:
+------------------+------------------+
| IP Origen        | IP Destino       |
| 192.168.1.10     | 93.184.216.34    |
+------------------+------------------+
| TTL: 64          | Protocolo: TCP   |
+------------------+------------------+
| Segmento TCP completo                |
+--------------------------------------+
```

**Paso 6: ARP - Resolucion de MAC (entre Capa 3 y 2)**

La PC necesita saber la direccion MAC de su puerta de enlace (router) para enviar el paquete. Usa ARP:

```
[PC] ----- ARP Request: "Quien tiene la IP 192.168.1.1?" ---> (Broadcast)
[PC] <---- ARP Reply: "Yo, mi MAC es 00:11:22:33:44:55" ---- [Router]
```

**Paso 7: Capa de Enlace - Ethernet (Capa 2)**

Se crea una trama Ethernet agregando:
- MAC origen: AA:BB:CC:DD:EE:10 (tu NIC)
- MAC destino: 00:11:22:33:44:55 (router)
- Tipo: 0x0800 (IPv4)
- CRC (trailer) para deteccion de errores

```
Trama Ethernet:
+------------------+------------------+----------+------------------+
| MAC Destino      | MAC Origen       | Tipo     | Datos (Paquete   |
| 00:11:22:33:44:55| AA:BB:CC:DD:EE:10| 0x0800   | IP completo)     |
+------------------+------------------+----------+------------------+
| CRC (Trailer)                                                      |
+--------------------------------------------------------------------+
```

**Paso 8: Capa Fisica (Capa 1)**

La trama se convierte en bits (unos y ceros) y se transmite por el cable Ethernet como variaciones de voltaje. Si es WiFi, se modula en ondas de radio.

```
10101010 11001100 00110101 ... (los bits viajan por el medio fisico)
```

**Paso 9: Viaje a traves de la red**

```
[Tu PC] --(cable)--> [Switch] --(cable)--> [Router local]
   El switch ve la MAC destino, busca en su tabla y reenvia al puerto del router

[Router local] --(Internet)--> [Router ISP] --(Internet)--> [Router del servidor]
   Cada router examina la IP destino, consulta su tabla de enrutamiento,
   decrementa el TTL, y reenvia al siguiente salto

[Router del servidor] --(cable)--> [Switch] --(cable)--> [Servidor web]
```

**Paso 10: Desencapsulamiento en el servidor**

El servidor recibe los bits y hace el proceso inverso:

| Capa | Accion |
|------|--------|
| 1. Fisica | Convierte bits en trama |
| 2. Enlace | Verifica MAC destino (es suya?), verifica CRC, extrae paquete IP |
| 3. Red | Verifica IP destino (es suya?), extrae segmento TCP |
| 4. Transporte | Verifica puerto destino 80, ensambla segmentos, verifica checksum, pasa datos HTTP |
| 7. Aplicacion | Servidor web (Apache/Nginx) procesa la peticion HTTP GET y prepara la respuesta |

**Paso 11: Respuesta del servidor**

El servidor genera la respuesta HTTP (ej: pagina HTML) y el proceso se invierte: los datos viajan del servidor al cliente siguiendo el mismo camino de encapsulamiento/desencapsulamiento.

```
[Servidor] <--- Todo el proceso inverso ---> [Tu PC]
   HTTP 200 OK + HTML                         Navegador renderiza pagina
```

**Diagrama completo del recorrido:**

```
ORIGEN (Tu PC)
+--------+  HTTP Request: GET / HTTP/1.1
| App    |  Datos
+--------+
| TCP    |  Segmento: puerto 54321 -> 80
+--------+
| IP     |  Paquete: 192.168.1.10 -> 93.184.216.34
+--------+
| MAC    |  Trama: MAC PC -> MAC Router
+--------+
| Bits   |  10101010...
+--------+
    |
    v
[Switch local] (reenvia por MAC)
    |
    v
[Router local] (reenvia por IP, decrementa TTL)
    |
    v
[Internet] (multiples routers intermediarios)
    |
    v
[Router del servidor]
    |
    v
[Switch del servidor]
    |
    v
DESTINO (Servidor Web)
+--------+
| Bits   |  10101010...
+--------+
| MAC    |  Verifica MAC, extrae IP
+--------+
| IP     |  Verifica IP destino, extrae TCP
+--------+
| TCP    |  Verifica puerto 80, ensambla datos
+--------+
| App    |  HTTP Request recibida
+--------+
    |    Procesa peticion, genera respuesta
    v
    (El servidor envía la respuesta siguiendo el mismo camino inverso)
```

---

## Preguntas y Respuestas

### Pregunta 1
**Cual es la diferencia entre un hub y un switch?**

**Respuesta:** Un hub es un dispositivo "tonto" que simplemente repite la senal que recibe por un puerto a TODOS los demas puertos. No tiene inteligencia: cuando recibe un paquete, lo envía por todos los puertos menos por el que llego. Esto genera colisiones y trafico innecesario. Un switch es "inteligente": mantiene una tabla MAC que asocia direcciones MAC con puertos especificos, y solo envía el paquete al puerto donde esta el destinatario. Esto reduce colisiones y mejora el rendimiento y la seguridad. En una red con hub, cualquier dispositivo puede ver todo el trafico; con switch, solo ve su propio trafico.

### Pregunta 2
**Para que sirve un router?**

**Respuesta:** Un router conecta DIFERENTES redes entre si. Su funcion principal es **enrutar** paquetes: decide la mejor ruta para que un paquete llegue de la red de origen a la red de destino. Por ejemplo, cuando envías un paquete desde tu casa a un servidor en otro pais, el router examina la direccion IP de destino, consulta su tabla de enrutamiento, y reenvía el paquete al siguiente router en el camino. Ademas, el router suele hacer NAT (Network Address Translation) para que multiples dispositivos compartan una sola IP publica, y funciona como puerta de enlace (gateway) predeterminada de tu red local.

### Pregunta 3
**Que es una direccion MAC y para que sirve?**

**Respuesta:** Una direccion MAC (Media Access Control) es un identificador unico de 48 bits asignado por el fabricante a cada tarjeta de red (NIC). Se representa como 12 digitos hexadecimales en grupos de 2: `00:1A:2B:3C:4D:5E`. Los primeros 3 pares (OUI) identifican al fabricante; los ultimos 3 pares son un numero unico asignado por el fabricante. Sirve para identificar **dispositivos fisicos** dentro de una red local (LAN). Los switches la usan para saber por que puerto enviar los datos. Es comparable a un numero de serie o DNI del dispositivo: teorica y practicamente es unico a nivel mundial.

### Pregunta 4
**Cual es la diferencia entre TCP y UDP?**

**Respuesta:** TCP (Transmission Control Protocol) es **orientado a conexion y confiable**. Antes de enviar datos, establece una conexion (three-way handshake), numera los segmentos, confirma la recepcion, reenvia paquetes perdidos, y entrega los datos en orden. Es como una llamada telefonica: sabes que la otra persona esta escuchando y puedes confirmar que entendio. Se usa para navegacion web (HTTP), email (SMTP), transferencia de archivos (FTP). UDP (User Datagram Protocol) es **no orientado a conexion y no confiable**. Envia datagramas sin establecer conexion, sin confirmacion, sin reenvio. Es como enviar un correo ordinario: lo envias pero no sabes si llego. Es mas rapido y con menos sobrecarga. Se usa para streaming, videollamadas, videojuegos online, DNS, donde la velocidad importa mas que la confiabilidad absoluta.

### Pregunta 5
**Que capa del modelo OSI maneja el enrutamiento?**

**Respuesta:** La **Capa 3 - Red** (Network layer) es la encargada del enrutamiento. Esta capa agrega las direcciones IP de origen y destino a los paquetes, y los routers (que trabajan en esta capa) deciden la mejor ruta para que cada paquete llegue a su destino. El protocolo principal de esta capa es IP (Internet Protocol), y los protocolos de enrutamiento como OSPF, BGP, RIP tambien operan aqui. La capa 3 es responsable de la entrega de paquetes de extremo a extremo a traves de multiples redes, mientras que la capa 2 (Enlace) solo entrega dentro de una misma red local.

### Pregunta 6 (Adicional)
**Que significa "encapsulamiento" en redes?**

**Respuesta:** Encapsulamiento es el proceso mediante el cual cada capa del modelo OSI/TCP/IP agrega su propia informacion de control (cabecera) a los datos que recibe de la capa superior. Es como empacar un regalo en varias cajas: pones el regalo (datos) en una caja (capa 4), luego esa caja dentro de otra mas grande (capa 3), y asi hasta tener varias capas de empaque. En el destino, se hace el proceso inverso (desencapsulamiento): se abren las cajas una por una hasta llegar al regalo original. Cada capa agrega informacion especifica: puertos (capa 4), IPs (capa 3), MACs (capa 2). Esto permite que cada capa pueda hacer su trabajo independientemente de las demas.

---

## Tarea / Lectura Recomendada

1. **Leer:** "Computer Networking: A Top-Down Approach" de Kurose & Ross (Capitulos 1-2) - Explica redes desde la capa de aplicacion hacia abajo, muy didactico
2. **Practicar:** Usa el comando `ipconfig /all` (Windows) o `ifconfig` (Linux) para ver tu direccion IP, MAC, gateway y servidores DNS en tu computadora
3. **Practicar:** Usa `ping google.com` y `tracert google.com` (Windows) o `traceroute` (Linux) para ver la ruta que siguen tus paquetes
4. **Practicar:** Usa `arp -a` (Windows) para ver la tabla ARP de tu computadora (IPs y MACs de dispositivos en tu red local)
5. **Leer:** RFC 1180 - "A TCP/IP Tutorial" (documento clasico y accesible en espanol/ingles)
6. **Visualizar:** Buscar en YouTube "How the Internet Works" de Los Alamos National Laboratory (video clasico y didactico)
7. **Herramienta:** Descargar Wireshark (gratuito) y capturar trafico de red: abre el programa, selecciona tu interfaz de red, filtra por "http" y observa los paquetes en tiempo real (no compartas capturas con informacion sensible)
