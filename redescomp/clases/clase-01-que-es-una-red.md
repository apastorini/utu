# Clase 1 — ¿Qué es una red de computadores?

**Bloque:** A (Fundamentos) · **Semana:** 1 · **Duración estimada:** 110 min
**Correlativa:** — (primera clase del curso) · **Sigue con:** Clase 2 (los modelos de capas: OSI y TCP/IP)
**Material de referencia:** Tanenbaum cap. 1 (pág. ~1 a ~35 del PDF de tu carpeta) · RFC 1122, RFC 8200, RFC 9293, RFC 8200

---

## 🎯 Al terminar esta clase vas a poder

1. **Definir** qué es una red de computadores y explicar las tres razones por las que existen (comunicar, compartir recursos, economía de escala), calculando el costo por usuario.
2. **Clasificar** una red como PAN, LAN, MAN o WAN, y explicar por qué la clasificación **moderna ya no se basa en el alcance geográfico** sino en la latencia y en la propiedad.
3. **Dibujar** las cinco topologías clásicas (bus, estrella, anillo, malla, árbol, híbrida) y decir qué se usa hoy y por qué.
4. **Asociar** cada dispositivo (host, NIC, hub, switch, router, punto de acceso, módem, firewall, servidor) con **la capa que implementa**, que es la pregunta que más se hace de esta clase.
5. **Distinguir** sin dudar las seis magnitudes: ancho de banda, velocidad de propagación, latencia, retardo total, throughput y jitter, con sus unidades y de qué dependen.
6. **Explicar por qué la velocidad de propagación no cambia con el medio de enlace ni con el ancho de banda**, que es el error conceptual más caro del curso.
7. **Separar** "Internet" de "Web", y ubicar los cuatro hitos que dan contexto al temario.

> **Prerequisito del examen:** — (clase de soporte). Adelanta la **Pregunta 1a del Examen `2009-12`**, que se resuelve completo en la Clase 5.

---

# PARTE 1 — TEORÍA

## 1.1 Qué es una red y por qué existen

### La definición

Tanenbaum define una red de computadores así:

> Un sistema de computadores **interconectados** por una serie de enlaces o nodos, con el fin de **compartir recursos** e **intercambiar información**.

Las tres palabras de esa definición que importan son *interconectados*, *compartir* e *intercambiar*, y las tres se pueden develops por separado:

- **Interconectados**: no alcanza con que dos máquinas estén cerca. Tiene que haber un **medio** (cobre, fibra, aire) y un **dispositivo** que los una (una NIC, un switch). Un montón de equipos sueltos en una habitación no son una red: son un montón de equipos sueltos.
- **Compartir recursos**: una impresora, un disco de 4 TB, una conexión a Internet. El recurso es **físico y único**, y muchos lo usan.
- **Intercambiar información**: no solo datos de la aplicación; también información de control (quién tiene la dirección de quién, qué rutas existen, cómo se negocia un enlace).

```
                     ┌──────────────────────┐
                     │   Recurso compartido │
                     │  (disco / impresora /  │
                     │   salida a Internet)  │
                     └──────────┬───────────┘
                                │
              ┌─────────────────┼─────────────────┐
              │                 │                 │
        ┌─────┴─────┐     ┌─────┴─────┐     ┌─────┴─────┐
        │   H1      │     │   H2      │     │   H3      │
        │ 203.0.113 │     │ 203.0.113 │     │ 203.0.113 │
        │    .11    │     │    .12    │     │    .13    │
        └───────────┘     └───────────┘     └───────────┘
              \                 |                 /
               \________________|________________/
                        red conmutada, 1 Gbps
```

### Las tres razones, en serio

**Razón 1 — Comunicarse.** La razón original. La red existe porque dos personas que están a 400 km de distancia necesitanomiplir el mismo documento, negociar, o curbajo. Antes de la red eso significaba carta (días), teléfono (no escribís), o ir (horas).

**Razón 2 — Compartir recursos Caro.** Un servidor de archivos de 200 TB cuesta lo mismo para 5 usuarios que para 500. Lo que cuesta es el **software** y el **almacenamiento**, no el número de personas que lo leen. Una impresora láser de color cuesta 600 dólares y no tiene sentido tener una en cada escritorio: una sola, en red, y que todos la usen.

**Razón 3 — Economía de escala.** Esta es la que casi no se explica y es la que justifica todo. Definamos:

```
 C_red = costo de poner la red (cableado, switches, NICs, configuración)
 n     = cantidad de usuarios conectados
 C_term = costo del terminal por usuario (la PC, que de todas formas
          ibas a tener)
```

El costo total es `C_total(n) = C_red + n · C_term`. El **costo por usuario** es:

```
 C_usuario(n) = C_red / n  +  C_term
                └────┬────┘    └───┬──┘
              se reparte entre   no depende
                todos los n        de n
```

El primer término **decrece** con `n`; el segundo es constante. Por lo tanto el costo total por usuario **baja al aumentar `n`** y tiene un piso en `C_term`.

```
  costo por usuario
       ▲
       │
   C_term ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─  ← piso: la PC del usuario
       │                              ___________
       │                        _____/
       │                  _____/
       │            _____/        C_red/n  (hiperbola)
       │      _____/
       │  ___/
       │_/
       └──────────────────────────────────────────────► n
         1     5     20    100    1000   10000
```

*Por qué esto importa en redes:* es la razón por la que **comprar una red grande es más barato por usuario que una red chica**, y la razón por la que las ISP te cobran **por ancho de banda y no por usuario**: cuanto más clientes, más usuarios detrás de la misma capacidad, más rentable el enlace.

---

## 1.2 Clasificación por alcance: PAN, LAN, MAN, WAN

El clasificación clásico, el de cualquier libro de texto de los 90, ordena las redes por **distancia geográfica**. Funcionaba, y todavía se usa como primera aproximación. Pero, como vamos a ver en §1.3, **ya no alcanza**.

| Tipo | Significado | Alcance típico | Velocidad | Propiedad |
|---|---|---|---|---|
| **PAN** | *Personal Area Network* — Red de área personal | ~**10 m** (Bluetooth), 1 m (cable) | 1 a 3 Mbps (Bluetooth) | **Privada**, siempre de una sola persona |
| **LAN** | *Local Area Network* — Red de área local | **Hasta ~1 km** (un edificio, un piso, un campus) | **1 Gbps a 100 Gbps** hoy; conmutada | **Privada**, de una organización |
| **MAN** | *Metropolitan Area Network* — Red de área metropolitana | **Una ciudad** (~10 a 50 km) | 1 a 10 Gbps (fibra pública) | **Pública** o departmental (un operador de ciudad) |
| **WAN** | *Wide Area Network* — Red de área amplia | **Países, continentes, el planeta** | 1 Gbps en el backbone, pero **decenas de ms de latencia** | **Mixta**: los backbone son de operadores, el último tramo es de cada uno |

### PAN — lo que tenés en el bolsillo

```
     [ Auriculares ]
           |  Bluetooth / 802.15.1
     [   Celular   ] ~~~~~~~~~ 2,4 GHz ~~~~~~ [ Auriculares ]
           |  (alcance nominal ~10 m, clase 2)
     [  Notebook  ]
```

- **Bluetooth (IEEE 802.15.1)**: clase 2 = ~**10 m**, ~1 Mbps (BR) a 3 Mbps (EDR); con **Bluetooth Low Energy** las tasas caen a kilobits para los sensores.
- **NFC**: 4 cm. No es una red en el sentido clásico: es un enlace de un solo sentido de contacto.
- **IEEE 802.15.4 / Zigbee**: ~10 a 100 m, ~250 kbps, pensado para redes de **muchos** nodos de bajo consumo (medidores, domótica).

### LAN — la red conmutada del edificio o del campus

```
      ┌──────────── LAN 192.168.1.0/24 ────────────┐
      │                                            │
   ┌──┴──┐  ┌──┴──┐  ┌──┴──┐  ┌──┴──┐  ┌──┴──┐    │
   │ H1  │  │ H2  │  │ H3  │  │ H4  │  │ srv │───►│
   └──┬──┘  └──┬──┘  └──┬──┘  └──┬──┘  └──┬──┘    │
      └───────┴────┬────┴───────┴────────┘        │
                   │                                │
             ┌─────┴──────┐                        │
             │  SWITCH   │  1/10/25/40/100 Gbps   │
             └─────┬──────┘                        │
                   │ 1/10/25/40/100 Gbps          │
             ┌─────┴──────┐                        │
             │  R1 (router) ──► otra LAN / Internet│
             └────────────┘                        │
      └────────────────────────────────────────────┘
```

Lo que define una LAN moderna no es solo la distancia: es que es **conmutada**, con lo que desaparece el **dominio de colisión** (cada host tiene el medio para él) y cada puerto es un dominio de colisión y de broadcast separados.

### MAN — la ciudad

El ejemplo canónico fue el **anillo metropolitano de FDDI** (1980s-90s, token ring de fibra a 100 Mbps) y hoy son redes metropolitanas de fibra pública y, en parte, wireless de banda ancha (WiMAX, 5G fixed). La MAN se distingue de la LAN en que **el equipo y la propiedad ya no son los tuyos**: el operador de la ciudad te alquila un puerto.

### WAN — la red del planeta

Internet **es** el ejemplo canónico de WAN. Lo que lo delata, y lo vamos a ver con números en §1.6, es la **latencia**: un RTT típico en Internet está entre 20 ms (dentro del mismo datacenter o la misma ciudad) y 200 ms (entre continentes). Eso es de 3 a 4 órdenes de magnitud por encima de una LAN, y es exactamente la razón por la que los protocolos de Internet están diseñados como están (retransmisiones, control de congestión, ventanas grandes).

---

## 1.3 La frontera que ya no es el alcance: latencia y propiedad

Este es el matiz importante, y el que hace que la clasificación clásica quede corta. La definición de LAN/WAN "por distancia" falla con dos contraejemplos que existen **hoy**:

**Contraejemplo 1 — un enlace por satélite es "LAN" en distancia y "WAN" en todo lo demás.** Un satélite geoestacionario está a 36.000 km de altura. Un enlace de 5 metros entre dos racks está a 5 metros. Sin embargo:

```
  Medida                          Enlace de 5 m     Satélite geoestacionario
  ─────────────────────────────────────────────────────────────────────────────
  Distancia del extremo           2,5 m             36 000 km
  Velocidad de propagación        ~2·10⁸ m/s        ~3·10⁸ m/s (espacio)
  Retardo de propagación (d/s)   12,5 ns           ~250 ms  ⇦ ida
  RTT mínimo                      ~25 µs            ~500 ms
  Latencia comparada              1×                20 000×
```

**500 ms de RTT es la latencia de una WAN.** Y el teléfono tiene 100 ms de latencia humana y se percibe instantáneo. Con 500 ms de ida y vuelta, una conversación por voz es **imposible** sin que se note el retraso. El satélite deellite es el ejemplo perfecto de por qué la latencia es el criterio, no la distancia.

**Contraejemplo 2 — una WAN dentro de una ciudad.** Los operadores montaron *dark fiber* (fibra oscura: la fibra tendida, sin luz, alquilada) entre locales de una misma ciudad, o incluso entre dos puntos de la misma ciudad, y con eso una latencia de **menos de 1 ms** a 10 o 40 Gbps. Eso es, con todas las letras, **una WAN con mejor desempeño que cualquier LAN de 2005**. La distancia es de 5 km y el desempeño es de LAN.

**Contraejemplo 3 — un PAN lento.** Bluetooth tiene ~10 m pero las WAN de fibra de larga distancia tienen una latencia de 2 ms. Alguien con un auricular Bluetooth en la oreja tiene más latencia que alguien con un enlace metro de 10 Gbps.

### El criterio correcto

```
  ┌────────────────────────────┐         ┌────────────────────────────┐
  │   ¿La red es de la que    │         │   ¿La red es de la que    │
  │   soy dueño oArrendé?     │         │   hay UNdueño?            │
  └─────────────┬──────────────┘         └─────────────┬──────────────┘
                │                                       │
          NO ───┴───► WAN / MAN / infraestructura      SÍ ──┴──► LAN o PAN
        (o servicio de un tercero)              (la red es tuya)
```

El criterio que **sí** funciona en 2026 es doble:

| | **latencia** | **propiedad** |
|---|---|---|
| LAN típica | **< 1 ms** (0,1 a 1 ms) | tuya (una organización) |
| MAN típica | **1 a 5 ms** | del operador municipal o del campus |
| WAN típica | **5 a 250+ ms** | de uno o varios operadores |
| PAN | **< 10 ms** (casi 0) | tuya, de una persona |

Y la definición operativa que conviene usar: **una LAN es una red que no atraviesa un router que no es tuyo.** Si para ir de A a B pasás por un router de un operador, es una WAN para vos, por corta que sea la distancia.

---

## 1.4 Topologías

Topología = **la forma física del cableado**. Se estudia porque cada forma tiene un punto único de falla, una costo de cableado y una complejidad de administración diferente.

### (a) Bus — un solo medio compartido

```
   [H1]──┐
   [H2]──┤
   [H3]──┴═══[backbone compartido]═══[H4]──┬───►al backbone
   [H5]──┤                              [H6]──┤
   [H7]──┘                              [H8]──┘
        │
   ┌────┴─────────────────────────────┐
   │  toda la red ve el mismo medio;  │
   │  una terminadora (terminator)     │
   │  poner la señal (resistencia 50Ω) │
   │  al final de cada extremo del bus  │
   └────────────────────────────────────┘
```

| Ventajas | Desventajas |
|---|---|
| **Cabledado mínimo**: un solo cable recorre toda la red | **Un solo punto de falla**: si se corta el backbone, se cae **toda** la red |
| Barato | **Dominio de colisión único**: todo el tráfico se ve; el rendimiento cae con `n` |
| Fácil de extender | Colisiones, lo que obliga a CSMA/CD (ver Clase 41) |
| | Difícil de diagnosticar |

**Dónde se usa hoy:** en las **redes Wi-Fi**: la topología lógica de un punto de acceso es un bus. Todos los clientes comparten el mismo medio y compiten por él.

### (b) Estrella — todo al centro

```
                  ┌──────────┐
                  │  SWITCH  │  (o hub, en el pasado)
                  └────┬─┬───┘
       ┌───────┬───────┼───────┬───────┐
       │       │       │       │       │
     ┌─┴─┐   ┌─┴─┐   ┌─┴─┐   ┌─┴─┐   ┌─┴─┐
     │H1 │   │H2 │   │H3 │   │H4 │   │H5 │
     └───┘   └───┘   └───┘   └───┘   └───┘
```

| Ventajas | Desventajas |
|---|---|
| **Fallo aislado**: si se cae una rama, se cae un host, no la red | **El switch es el punto único de falla** (se mitiga con *stacking* o enlaces redundantes) |
| **Un dominio de colisión por puerto**: rendimiento no cae con `n` | **Cableado**: un cable por host hasta el centro |
| Agregar un host es trivial: un cable a un puerto libre |  |
| **Fácil de diagnosticar**: el puerto caído dice qué host es |  |
| Fácil de segmentar en VLAN |  |

**Dónde se usa hoy:** **toda** LAN conmutada, todo *datacenter*, todoARM conmutado. Es la topología dominante sin discusión.

### (c) Anillo — un lazo

```
              ┌────[R1]────┐
             /             \
        [R5]                [R2]
         │                   │
        [R6]                [R3]
             \             /
              └───[R4]─────┘
        (el paquete recorre el anillo en un sentido)
```

| Ventajas | Desventajas |
|---|---|
| **Retardo predecible**: número fijo de saltos, sin colisiones | **Un punto único de falla**: se corta el anillo, se cae la red |
| Funciona bien con tráfico uniforme y alta carga | **Complejidad**: hay que negociar quién transmite (token) |
| No hay colisiones: el acceso está arbitrationado | Añadir un nodo es más difícil que en estrella |

**Dónde se usa hoy:** el anillo clásico como topología física **murió**. Sobrevive en dos formas:

- **Metro ring / SONET / SDH**: los operadores montan anillos de fibra para protegerse: si se corta un tramo, el anillo se "cierra" por el otro lado en milisegundos. Eso es protección, no eficiencia.
- **Token Ring (802.5)** y **FDDI**: desaparecieron por completo. Se estudian en las clases 40 y 41 como ejemplo histórico del acceso al medio.

### (d) Malla — todos con todos

```
        [R1]────────[R2]
         │ ╲       ╱ │
         │  ╲     ╱  │
         │   ╲   ╱   │
         │    ╲ ╱    │
         │     ╳     │
        [R4]────────[R3]
      (malla completa: 6 enlaces, 3 nodos, cada par unido)
```

| Ventajas | Desventajas |
|---|---|
| **Tolerancia a fallos total**: si cae un enlace, hay camino alternativo | **Costo**: en una malla completa de `n` nodos hay `n(n-1)/2` enlaces |
| **Retardo mínimo**: siempre hay un camino corto | Complejidad de administración: `n²` vecinos que conocer |
| Se puede repartir la carga |  |

**Dónde se usa hoy:**

- **Malla completa** solo con `n` muy chico (2 o 3 nodos): por ejemplo el triángulo de **3 routers de borde de datacenter**, o el router de borde, el de spine y el de borde del otro lado.
- **Malla parcial** en el backbone de los operadores: cada router conecta a **varios** proveedores, no a uno. Es la base de la **política de BGP** (un AS con 3 o 4 eBGP en lugar de uno).

### (e) Árbol — jerarquía

```
                    ┌────────────┐
                    │   RAÍZ     │  router de borde / core
                    └─────┬──────┘
              ┌───────────┴───────────┐
          ┌───┴───┐               ┌───┴───┐
          │  SW1  │               │  SW2  │   switch de distribución
          └───┬───┘               └───┬───┘
       ┌──────┴──────┐          ┌──────┴──────┐
     ┌─┴─┐        ┌─┴─┐      ┌─┴─┐        ┌─┴─┐
     │SA1│        │SA2│      │SB1│        │SB2│   switch de acceso
     └───┘        └───┘      └───┘        └───┘
```

| Ventajas | Desventajas |
|---|---|
| **Escalable**: agregás una hoja y no tocás el centro | El backbone es **punto único de falla** |
| Jerarquía natural =Coara de administración |RAID: un router de backbone lento es un cuello de botella para todo |
| Fácil de segmentar por departamento o por piso | |

**Dónde se usa hoy:** **todo** el *datacenter* y toda la red campus de una universidad grande. Es la estructura de 3 niveles (*access → aggregation → core*) estándar.

### (f) Híbrida — lo que realmente se instala

```
     ┌── backbone: MALLA entre routers ──┐
     │                                   │
  ┌──┴──────┐                       ┌────┴───┐
  │ R1      │═════ MALL A ═══════════│ R2     │
  │ (mesh)  │                       │ (mesh)  │
  └──┬──────┘                       └────┬───┘
     │ ESTRELLA (piso 1)                │ ESTRELLA (piso 2)
  ┌──┴──┬──┬──┐                    ┌──┴──┬──┬──┐
  │PC  │PC │PC │                    │PC  │PC │PC │
  └───┘ └──┘ └──┘                    └───┘ └──┘ └──┘
     ANILLO de fibra del operador (protección)
```

**La topología híbrida es la respuesta a todos los defectos de las otras cinco:**

- La **malla** da redundancia donde la redundancia importa (el backbone): el costo se paga en pocos enlaces.
- La **estrella** da rendimiento y facilidad de diagnóstico donde hay muchos usuarios (el acceso).
- El **anillo** da protección donde el medio es caro y no lo controlás (la fibra del operador).

**Para el examen:** si te preguntan "¿qué topología usa Internet?", la respuesta correcta es **una malla parcial de routers, con los enlaces de los operadores aggregating en puntos de intercambio (IXP)**, y **estrella hacia abajo** en cada red de acceso.

---

## 1.5 Los dispositivos y —esto es lo que más se pregunta— qué capa implementa cada uno

El error clásico es decir "el switch es de capa 3" o "el router hace cosas de capa 2". La tabla que hay que tener en la cabeza es esta:

| Dispositivo | Función | **Capa OSI** | **Capa TCP/IP** | Sabe de IP | Sabe de puertos TCP |
|---|---|---|---|---|---|
| **Repetidor** (*repeater*) | Regenera la señal eléctrica | **1** Física | Acceso a red | no | no |
| **Hub** | Conmutador eléctrico de capa 1: repite a todos los puertos | **1** Física | Acceso a red | no | no |
| **Módem / DTU** | Modula una señal digital sobre el medio analógico | **1** Física | Acceso a red | no | no |
| **NIC** (*network interface card*) | Transmite y recibe tramas en un medio | **1 y 2** (Física + Enlace) | Acceso a red | no | no |
| **Punto de acceso** (AP, Wi-Fi) | Traduce entre medio inalámbrico y Ethernet; hace association, autenticación, cifrado (WPA3) | **2** (Enlace) — y a veces 3 para translated LAN | Acceso a red / red | a veces | no |
| **Switch** / *bridge* | Reenvía tramas por la **tabla MAC**; aprende direcciones; dominio de colisión por puerto | **2** Enlace de datos | Acceso a red | **no** | no |
| **Router** / *gateway* de red | Reenvía paquetes por la **tabla de reenvío IP** (longest prefix match) | **3** Red | Internet | **sí** | no |
| **Firewall** | Filtra por IP, por puerto, y (si es *stateful*) por conexión | **3 y 4** (Red y Transporte) | Internet / Transporte | sí | **sí** |
| **Servidor / host** | Corre las aplicaciones y las implementa | **todas** (1 a 7) | todas | sí | sí |

### Las tres filas que más se confunden

**El switch NO sabe de IP.** Un switch de capa 2 mira el **MAC destino** de la trama, busca en su tabla de reenvío y copia la trama al puerto correspondiente. No le importa si el paquete IP que va adentro dice `8.8.8.8` o `203.0.113.9`. Por eso un switch **no** reemplaza a un router: si le pedís que te lleve a otra red, no puede, porque no sabe qué redes existen. Esa es la Pregunta 2 del Examen 2009-02, y la resolvo en la Clase 3.

**El router NO sabe de puertos.** Un router Cisco de los de antes miraba el campo *protocolo* de la cabecera IP (TCP=6, UDP=17, ICMP=1) para decidir si podía hacer *NAT* o *policing*. Pero no miraba el puerto TCP. Esa es la razón técnica de por qué la NAT rompe el aislamiento de capas (Clase 31), y la Pregunta 4 del Examen 2011-02 la developa.

**El hub es de capa 1, no de capa 2.** Parece un switch ("tiene puertos"), pero no aprende direcciones y no decide: copia la señal a **todos** los puertos. Por eso todos los hosts comparten un único dominio de colisión. Esa distinción es la Pregunta 3 del Examen 2010-12 (Clase 42).

---

## 1.6 Los parámetros de una red — la parte más importante de esta clase

Acá está el contenido que más se confunde en el examen y que hay que tener **absolutamente claro**. Son seis magnitudes, y **casi todas se miden en unidades distintas**.

### La tabla madre

```
  ╔════════════════════╦══════════════════╦═══════════╦══════════════════════════╗
  ║ Magnitud           ║ Símbolo           ║ Unidad    ║ Qué es                    ║
  ╠════════════════════╬══════════════════╬═══════════╬══════════════════════════╣
  ║ Ancho de banda     ║ B, R (bandwidth)  ║ bps       ║ CAPACIDAD del enlace       ║
  ║ Vel. de propagac.  ║ s                 ║ m/s       ║ RAPIDEZ de la SEÑAL        ║
  ║ Latencia           ║                   ║ ms        ║ tiempo de un viaje        ║
  ║ Retardo total      ║ d_end2end         ║ ms        ║ 4 componentes sumados     ║
  ║ Throughput         ║                   ║ bps       ║ bits REALES por segundo   ║
  ║ Jitter             ║ Δl               ║ ms        ║ VARIACIÓN de la latencia  ║
  ╚════════════════════╩══════════════════╩═══════════╩══════════════════════════╝
```

### 1.6.1 Ancho de banda (*bandwidth*)

Es la **capacidad máxima** del enlace, en **bits por segundo** (bps). Define cuánto se puede mandar **como máximo**, no cuánto se manda.

- Es una propiedad del **equipo y del medio**: del transceptor, del puerto, de la modulación.
- **Cambia** con la tecnología: Ethernet pasó de 10 Mbps a 100 Mbps a 1 Gbps a 10 Gbps a 25/40/50/100 Gbps a 400/800 Gbps. Un enlace de 1 Gbps **no puede** mandar 2 Gbps, por más que el cable sea mejor.
- Lo ves en el rótulo de la interfaz: `1000BASE-T`, `10GBASE-SR4`, `100GE`.
- También se usa el mismo término en dos sentidos distintos: "**ancho de banda**" (bps) y "**ancho de banda**" (Hz). **Esto es una fuente perenne de confusiones.** En el contexto de Nyquist y Shannon (Clase 7) el ancho de banda está en **hercios**, no en bits por segundo.

### 1.6.2 Velocidad de propagación (*propagation speed*)

Es la **rapidez con la que viaja la señal por el medio**, en **metros por segundo**. Los valores que hay que tener:

```
  Medio                       Velocidad de propagación
  ───────────────────────────────────────────────────────────────
  Vacío (espacio libre)        c  = 3·10⁸ m/s   (exacta, es la constante de la luz)
  Aire                         ~ 2,998 · 10⁸ m/s  (un 0,07 % menos que el vacío)
  Cobre (UTP/STP, coax)        ~ 2·10⁸ m/s     (un 33 % menos)
  Fibra óptica (silicio)       ~ 2·10⁸ m/s     (un 33 % menos)
  ───────────────────────────────────────────────────────────────
  Conductor eléctrico típico    ~0,6 a 0,7 · c
```

> ⚠️ **Ojo con un detalle que aparece en la solución oficial del Examen `2009-12`:** ahí dice *"s ~ 2×10⁸ m/s **en cobre**"*. Es correcto **para el cobre**. Si algún apunte dice "2×10⁸ en el vacío", es un error: en el vacío la luz va a 3×10⁸ m/s. El número que se usa en los problemas de examen es **2×10⁸ m/s para cobre y fibra**, y **3×10⁸** si el problema habla de un enlace por satélite o por el espacio.

**Lo que la velocidad de propagación NO es:** una capacidad. **No tiene nada que ver con la velocidad a la que se mandan los datos.**

### La tabla que responde la Pregunta 1a del Examen 2009-12

Esta tabla es la respuesta literal a *"Señale las diferencias entre el ancho de banda y la velocidad de propagación en el medio"*. Memoriala como está:

| | **Ancho de banda** | **Velocidad de propagación** |
|---|---|---|
| **Símbolo** | `B` o `R` | `s` |
| **Unidad** | **bps** (bits por segundo) | **m/s** (metros por segundo) |
| **Qué mide** | **Cuántos bits** entran por segundo | **A qué velocidad viaja la señal** |
| **De qué depende** | Del **equipo**: transceptor, puerto, modulación | Del **medio físico**: la física de la propagación |
| **Cambia al cambiar el medio** | **Depende**: 10BASE-T vs 1000BASE-T vs fibra | **No**: es ~2×10⁸ m/s tanto en cobre como en fibra |
| **Cambia con la distancia** | **No** | **No** (la distancia va en el numerador de `d/s`, no en `s`) |
| **Tiene unidad de longitud** | No | **Sí** |
| **Relación con el retardo** | Entra en `d_transmisión = L / B` | Entra en `d_propagación = d / s` |
| **Ejemplo** | "La línea tiene 1 Mbps" | "En ese cable la señal va a 2·10⁸ m/s" |

**Una frase que resume la diferencia y que podés usar en el examen:**

> El **ancho de banda** es una propiedad del **enlace** (cuánta información cabría por segundo, y depende del equipo); la **velocidad de propagación** es una propiedad del **medio** (a qué velocidad física viaja la señal, y depende de la física del medio). **Son ejes perpendiculares**: podés tener un enlace de 100 Mbps por cobre (BW alto, `s` de cobre) o de 100 Mbps por fibra (mismo BW, mismo `s` porque la fibra también da ~2×10⁸ m/s).

### 1.6.3 Latencia

Es el **tiempo que tarda un paquete en ir de A a B**, medido en milisegundos. Es unTIEMPO, no una tasa. Y depende de:

- la distancia,
- el número de saltos (routers) y su velocidad de procesamiento,
- la congestión de la red (cuánto esperó en las colas),
- los enlaces que usa.

**Latencia de ida y vuelta (`RTT`, *Round Trip Time*):** el tiempo que tarda un paquete en ir y volver. Es **el doble de la latencia mínima**, y se mide con `ping`:

```
  Host A                                              Host B
    │                                                     │
    │────────── Echo request (TTL=64) ────────────────────▶│   ida:  40 ms
    │                                                     │
    │◀───────── Echo reply ────────────────────────────────│   vuelta: 45 ms
    │                                                     │
    RTT medido por ping = 40 + 45 = 85 ms
```

**Latencia no es RTT.** Si la latencia de ida es 40 ms, la latencia es 40 ms y el RTT es 80 ms (más el procesamiento). Es el error que aparece en el Ejercicio 2.4.

### 1.6.4 Retardo total (*end-to-end delay*)

Es la **suma de cuatro componentes** que vas a estudiar en detalle en la Clase 5:

```
  d_end2end = d_proc + d_cola + d_transmisión + d_propagación
               \___/     \___/     \__________/     \___________/
              varío      variable   L / R              d / s
              según      según       (NO depende        (NO depende
              el nodo    la cola     del medio)          del paquete)
```

Solo lo dejo enunciado acá; toda la aritmética va en las Clases 5 y 6.

### 1.6.5 Throughput (rendimiento)

Es la **cantidad real de bits por segundo que pasan**, medido durante un intervalo. Siempre cumple:

```
  throughput  ≤  ancho de banda
```

Y es estrictamente menor por cuatro razones:

```
  throughput = ancho de banda × eficiencia

  eficiencia = (bytes de datos útiles) / (bytes totales en el medio)
             = 1 − overhead_de_cabeceras − retrASMisiones − colisiones
```

**Ejemplo con la aritmética:**

```
  Enlace de 1 Gbps = 1 000 000 000 bps
  Overhead de cabeceras (Ethernet 18 + IP 20 + TCP 20 = 58 bytes por cada
  paquete de 1500 bytes de datos) + Retransmisiones (0,5 %) + Colisiones (0)

  eficiencia = (1500 − 58) / 1500 = 1442/1500 = 0,9613
  0,9613 × 1 000 000 000 = 961 000 000 bps

  → El throughput máximo de una conexión TCP sobre 1 GbE es
    ~961 Mbps, NO 1000 Mbps.
```

### 1.6.6 Jitter

Es la **variación de la latencia entre paquetes del mismo flujo**. Se calcula como la desviación (o la diferencia entre máximo y mínimo) de los retardos de paquetes que deberían haber llegado todos juntos.

```
  Tres paquetes del mismo flujo, enviados con 20 ms de separación:

  Paquete 1: 80 ms
  Paquete 2: 95 ms
  Paquete 3: 110 ms

  jitter = 110 − 80 = 30 ms
```

**Por qué importa** (Clase 44 lo desarrolla): en voz y video, **no importa** el retardo absoluto (100 ms de latencia en una voz se notices en el tono, pero no lo rompe); lo que rompe es que **lleguen en ráfagas**. Un códec de audio reproduce cada 20 ms: si el paquete 1 tarda 80 ms y el 2 tarda 110, el buffer se drains dos muestras de golpe. Eso se oye como un **clique**. Por eso RTP lleva **número de secuencia y timestamp**: para detectar, ordenar y rellenar.

---

## 1.7 Historia mínima: cuatro hitos, y la confusión más común del curso

### Los cuatro hitos

```
  Año  Evento
  ─────────────────────────────────────────────────────────────────────
  1969 ARPANET: se conecta el primer enlace entre el UCLA (IMP #1) y el
       SRI (IMP #2). Cuatro nodos en 1971. Cuatro IMP, 50 kbps,
       conmutación de paquetes desde el día uno (Packet Switching was
       the original design, not an afterthought).
  1983 1 de enero: ARPANET adopta TCP/IP como único protocolo.
       "Flags Day": los hosts que seguían con NCP se apagan.
       → TCP/IP no es "el protocolo que se eligió después": es el
       que quedó, y la razón fue la interoperabilidad.
  1991 Tim Berners-Lee publica el primer sitio Web (info.cern.ch) en
       agosto de 1991. La Web es una APLICACIÓN de Internet.
  1996 Se abren los primeros ISPs comerciales. Internet pasa de
       proyecto de investigación a servicio.
  ─────────────────────────────────────────────────────────────────────
  2007 El iPhone. El teléfono pasa de ser un cliente de Internet a ser
       el mayor generador de tráfico. La latencia y el consumo de
       batería se vuelven métricas de primera clase.
```

### Internet NO es la Web — el error conceptual más común

Esta confusión se paga en los exámenes, y es una de las cosas más básicas que hay que tener claras:

```
  ┌─────────────────────────────────────────────────────────────────┐
  │                                                                 │
  │   INTERNET = la RED. La infraestructura.                       │
  │              Un conjunto de redes interconectadas.              │
  │              Protocols: IP, TCP, UDP, ICMP, BGP, ...            │
  │              Identifica COMPUTADORES por dirección IP.          │
  │                                                                 │
  │   LA WEB = una APLICACIÓN que corre sobre Internet.             │
  │            Protocols: HTTP, HTML, URL, cookies.                 │
  │            Identifica DOCUMENTOS por URL.                       │
  │                                                                 │
  │   Analogía: Internet es elCorreo. La Web es una carta.          │
  │   El correo también transporta telegramas, llamadas, paquetes    │
  │   y fotos: esas son otras aplicaciones, no "el correo".         │
  │                                                                 │
  └─────────────────────────────────────────────────────────────────┘
```

**Prueba de que son cosas distintas:** la Web habla **HTTP sobre TCP sobre IP**. Si mañana nadie usa HTTP, la Web muere y **Internet sigue funcionando**: el correo (SMTP), el DNS, el VoIP (RTP), la mensajería, los juegos, SSH, todo sigue andando. **Internet sin Web es una red perfectamente válida.** Al revés no: **Web sin Internet es imposible**, porque la Web está definida encima de IP.

**Lo que cambió:** HTTP/3 (RFC 9114, 2022) ya no corre sobre TCP sino sobre **QUIC sobre UDP**, pero sigue corriendo sobre **IP**. La separación sigue exacta: **Internet es la red, la Web es una aplicación**.

---

### ⚠️ Actualización a 2026

**Sigue igual — de memoria, sin dudar:**
- Los cuatro hitos (1969, 1983, 1991, 1996) y el hecho de que **Internet ≠ Web**.
- Los cuatro componentes del retardo y sus fórmulas (`L/R` y `d/s`).
- La diferencia entre ancho de banda (bps) y velocidad de propagación (m/s).
- Los valores de `s`: ~2×10⁸ m/s en cobre y fibra, ~3×10⁸ en vacío/espacio.
- El criterio de clasificación PAN/LAN/MAN/WAN por alcance, como **primera aproximación**.

**Cambió o se modificó:**

- **IPv6 dejó de ser "el futuro".** El **28 de marzo de 2026** el acceso a Google por IPv6 **superó el 50 % por primera vez (50,10 %)**. APNIC midió ~42-43 % (cobertura de capacidad) y Cloudflare ~40 % (tráfico por bytes). Es desigual: Francia ~73 %, India ~72 %, Arabia Saudita ~65 %; Italia ~17 %, España ~10 %, Egipto ~4 %; China <5 %.
  **⇒ Dato para el aula:** en 2012 el curso decía "IPv6 llega en 10 años". La respuesta correcta en 2026 es "ya pasó la mitad en los usuarios de Google, pero es desigual, China sigue en <5 %, y la cifra depende de **qué** midas".
- **El agotamiento de IPv4 es un hecho consumado.** RIPE NCC hizo su **última asignación /22 el 25-nov-2019**. APNIC se agotó en abr-2011, ARIN en sept-2015, LACNIC en 2020, AfriNIC en abr-2017. Hoy el default de la capa 3 de acceso es el **CGNAT (*Carrier-Grade NAT*)**, que es una WAN con muchísimos clientes detrás de pocas IP públicas.
- **La capacidad de los enlaces de acceso se multiplicó.** Un portátil de 2026 se conecta a 1 Gbps por cable y a Wi-Fi 7 (IEEE 802.11be, aprobado en sept-2024, publicado como **802.11be-2024** el 22-jul-2025) con **320 MHz de canal y 4096-QAM** en la banda de 6 GHz. En los backbone de los operadores se ven **100, 400 y 800 Gbps**, y **el 10GbE+ es full-duplex obligatorio** (decisión de IEEE 802.3, no una RFC).
- **La clasificación "LAN/WAN" se usa menos y la de latencia más.** Los *datacenters* de hoy son "LAN" de 400 Gbps a 200 µs; las redes de acceso 5G tienen 10 ms de latencia y 1 Gbps, que es un perfil "WAN"; el satélite sigue en ~500 ms de RTT.

> **Consecuencia para el examen:** si te preguntan por la clasificación o por los parámetros, **respondé con los conceptos**, no con los números de capacidad. Los números de bps envejecen mal; los conceptos ("el ancho de banda es del equipo, la velocidad de propagación es del medio") no.

---

---

# PARTE 1 bis — LOS DIAGRAMAS DE RED: qué son, qué información llevan y cómo se hacen

> **Por qué esta sección va en la Clase 1 y no al final.** Un diagrama de red es
> **el lenguaje escrito de la materia**: en un examen te pueden pedir *"dibuje la
> topología y complete la tabla de ruteo"*, y en la vida profesional es el
> documento con el que un administrador se comunica con el resto del equipo, con
> el proveedor, y con el cliente. Si no sabés **qué información va** en un
> diagrama, no sabés ni leer el de otro ni escribir el tuyo.

## 1.8 El problema: un diagrama de red no es un dibujito

La pregunta que siempre llega es *"¿qué pongo en el diagrama?"*. La respuesta
corta es: **depende del tipo de diagrama**. Y hay un segundo problema, más sutil
y que en tu imagen quedó escrito con todas las letras: **"VALIDACIÓN PENDIENTE"**.

```
   Lo que pasa en la práctica

   1. Alguien diseña la red y dibuja el diagrama IDEAL.
   2. Se instala.
   3. La realidad se desalinea: una VLAN se agranda, un firewall cambia
      una regla, un balanceador saca un servidor de la rotación,
      un puerto pasa a "depreciado" y nadie actualiza el dibujo.
   4. El diagrama queda MENTIROSO.
   5. Un incidente a las 3 de la mañana se investiga contra un dibujo
      que dice cosas que ya no son ciertas.
```

> **El principio que hay que llevarse:** *un diagrama sin fecha, sin fuente y sin
> estado de verificación es una copia, no un documento.* Por eso la información
> de **estado** (§1.8.2) es tan importante como la de **topología** (§1.8.1): no
> alcanza con dibujar *qué hay*, hay que dibujar *qué está pasando con eso*.

## 1.9 Qué información lleva un diagrama de red

La respuesta que se da en cualquier curso de gestión, y la que hay que saber
escribir, es una lista de **ocho bloques de información**. Vamos uno por uno.

### Bloque 1 — Identidad del elemento

```
   Para CADA activo del diagrama:

   · Nombre formally legible.  NO "el switch de la 3".
                           SÍ  "sw-acceso-p3-01"
   · Marca y modelo.           Cisco C9300-48P
   · Rol o función.            "Distribución — VLANs de usuarios y servidores"
   · Ubicación física.         Rack B4, U24, patch panel PP-A-12
   · ID de inventario / tag.   "ASSET-2019-0442"  ← el que usás para
                                relacionarlo con el inventario, con el
                                sistema de tickets y con el activo en el CMDB
   · Responsable.              "NOC-FING / persona a cargo"
```

> **Por qué el "nombre formal" importa tanto:** es lo que te permite **buscar** el
> equipo en el sistema de inventario, en el CMDB, en el portal de backups y en los
> tickets. Un diagrama con nombres informales es un diagrama **inutilizable** a la
> hora de un incidente, que es la única hora en la que lo vas a necesitar.

### Bloque 2 — L3: direcciones IP, máscara/CIDR y gateway

Este es el bloque **más frecuentemente incompleto** en diagramas caseros, y el que
más se pide en los ejercicios de examen:

```
   ┌──────────────┬─────────────────┬──────────────┬────────────────┐
   │  Elemento    │  Dirección IP   │ Máscara/CIDR │  Gateway       │
   ├──────────────┼─────────────────┼──────────────┼────────────────┤
   │ sw-acceso-   │ 192.168.10.1    │ /24          │ — (es switch)  │
   │  p3-01 (SVI) │                 │ 255.255.255.0│                │
   ├──────────────┼─────────────────┼──────────────┼────────────────┤
   │ srv-dns-01   │ 192.168.10.53   │ /24          │ 192.168.10.1   │
   ├──────────────┼─────────────────┼──────────────┼────────────────┤
   │ rtr-borde-01 │ 192.168.10.254  │ /24          │ — (es router)  │
   │              │ 200.1.1.1       │ /30          │ —              │
   │              │ (doble pila)    │              │                │
   └──────────────┴─────────────────┴──────────────┴────────────────┘

   ★ En un router van TODAS sus interfaces, con su CIDR.
   ★ En un host va su IP + su gateway por defecto.
   ★ En un switch L3 va la SVI (la IP de la VLAN), no la de las tramas.
```

**Lo que hay que saber sobre el CIDR en un diagrama:**

- Escribí **las dos formas**: `/24` **y** `255.255.255.0`. La comunidad técnica
  usa el prefijo; los sistemas de gestión y algunos firewalls lo piden en notación de puntos.
- En un router, el `/30` entre dos routers indica **2 direcciones útiles**
  (`200.1.1.0/30` → `.1` y `.2` útiles, `.0` red y `.3` broadcast).
- **Las VLAN se numeran y se nombran.** En un diagrama: `VLAN 10 = USUARIOS`
  (nombre formal), no "la de los usuarios".

**Y el dato que casi nadie pone y que es el más útil de todos: el rango de DHCP
de cada VLAN.** Es lo que te dice qué IPs se van a|Asignar y cuáles quedan
reservadas para servidores, y es lo primero que se agota.

```
   VLAN 10 USUARIOS    192.168.10.0/24
        gateway .1
        DHCP:  .100 – .240        ← 141 direcciones
        fijas:  .2 – .50  (servidores e impresoras)
        libre:  .51 – .99  y  .241 – .254
```

### Bloque 3 — L2: VLAN, spanned ports, trunk y agregación

```
   VLAN 10 USUARIOS     ── puertos de acceso 1-24
   VLAN 20 SERVIDORES   ── puertos de acceso 25-40
   VLAN 30 VOZ          ── puertos de acceso 41-48, PoE
   VLAN 99 GESTIÓN      ── puerto 48 (management), OLTROs
   ──────────────────────────────────────────────
   Trunk (802.1Q):      uplink al switch de distribución
                        etiqueta 10,20,30,99
   ──────────────────────────────────────────────
   EtherChannel/LAG:    port-channel 1  (uplinks 49-50)
   spanning-tree:       cuál puerto es raíz (root port)
                        cuáles sonAlternate (bloqueados)
```

**Y el dato que hace útil un diagrama de switches: qué puertos están bloqueados
por STP.** Es la causa número uno de "la red anda lenta en ese sector". Un
diagrama de STP vale oro.

### Bloque 4 — Reglas de firewall

Acá es donde los diagramas se vuelven verdaderamente útiles, y donde la mayoría
de los equipos **no documenta**:

```
   ┌──────────────────────────────────────────────────────────────┐
   │  POLÍTICA DE FILTRADO — fw-borde-01                          │
   │  (ordenada: la primera que matchea, gana)                     │
   ├────┬────────┬──────────┬──────────┬──────────┬──────────────┤
   │  # │ Origen │ Destino  │ Puerto   │ Acción   │ Estado       │
   ├────┼────────┼──────────┼──────────┼──────────┼──────────────┤
   │ 10 │ 10.0/8 │ any      │ —        │ ACCEPT   │ activa       │
   │ 20 │ 192.168.10.0/24 │ 10.0.0.0/8 │ 443/TCP │ ACCEPT │ activa │
   │ 30 │ 192.168.10.0/24 │ any      │ 53/UDP   │ ACCEPT       │
   │ 40 │ any    │ 192.168.10.0/24 │ 445/TCP │ DROP │ activa   │
   │ 50 │ any    │ any      │ any      │ DROP     │ activa       │
   └────┴────────┴──────────┴──────────┴──────────┴──────────────┘

   ★ El "estado" de cada regla importa: hay reglas HABILITADAS que están
     ahí solo como respaldo y nunca se probaron.
```

**Los tres datos que hay que poner sí o sí:**

1. **El puerto/protocolo exacto** (443/TCP, 53/UDP), no "el puerto de DNS".
2. **El estado** (activa / deshabilitada / en testing).
3. **La fecha de la última revisión.** Una regla de 2014 que nadie miró es un
   problema de seguridad esperando.

### Bloque 5 — NAT, VIP y balanceadores

```
   ┌──────────────────────────────────────────────────────────────┐
   │  TRADUCCIONES                                                │
   ├────────────────────┬──────────────┬──────────────────────────┤
   │ VIP / IP pública   │ Puerto       │ Destino (pool)           │
   ├────────────────────┼──────────────┼──────────────────────────┤
   │ 200.1.1.10         │ 443/TCP      │ srv-web-01:443  (50%)     │
   │ (NAT 1:1)          │              │ srv-web-02:443  (50%)     │
   │                    │              │ peso: round-robin        │
   ├────────────────────┼──────────────┼──────────────────────────┤
   │ 200.1.1.20         │ 80/TCP       │ srv-web-01:80            │
   │ (DNAT estático)    │              │                          │
   ├────────────────────┼──────────────┼──────────────────────────┤
   │ 200.1.1.0/24       │ (todo)       │ SNAT → 192.168.10.1      │
   │ (pool NAT salida)  │              │ (todos los que salen)    │
   └────────────────────┴──────────────┴──────────────────────────┘

   ★ Un "servicio publicado en Internet" SIEMPRE tiene una VIP (o una IP
     pública) y un puerto. Sin eso, no hay entrada.
   ★ El balanceo puede ser: round-robin, least-connections, IP hash o
     Weighted. Anotá cuál.
```

**Y los dos casos que se confunden:**

- **NAT de salida** (SNAT / masquerade): cambia la IP de **salida** de toda la red
  privada. **No cambia los puertos**.
- **NAT de entrada** (DNAT / port forwarding / VIP): cambia el **destino** de una
  conexión que entra. **SÍ cambia los puertos** si es port forwarding.

Escribilo explícitamente en el diagrama, porque son dos cosas distintas que los
diagramas mezclan todo el tiempo.

### Bloque 6 — Puertos y protocolos de los servicios

```
   ┌──────────────────┬──────────────┬───────────────────┬─────────┐
   │ Servicio          │ Protocolo    │ Puerto(s)         │ Expuesto│
   ├──────────────────┼──────────────┼───────────────────┼─────────┤
   │ SSH               │ TCP          │ 22                │ sí      │
   │ HTTPS (web)      │ TCP          │ 443               │ sí      │
   │ DNS interno      │ UDP+TCP      │ 53                │ no*     │
   │ MySQL             │ TCP          │ 3306              │ no      │
   │ SMTP salida      │ TCP          │ 25  (587)         │ sí      │
   │ IMAP              │ TCP          │ 143 (993 TLS)     │ no      │
   │ SNMP             │ UDP          │ 161 (traps: 162)  │ no      │
   │ NTP               │ UDP          │ 123               │ sí      │
   └──────────────────┴──────────────┴───────────────────┴─────────┘
     * "no" = sólo dentro de la red; pero si el DNS es público, va en 53.
```

**El dato clave: la columna "expuesto".** Un servicio que escucha en `0.0.0.0` y
es alcanzable desde Internet es un **servicio público**, y eso tiene que estar
escrito, porque es una decisión de seguridad tomada por omisión.

### Bloque 7 — Estado operativo real (el "VALIDACIÓN PENDIENTE")

Este es el bloque que casi nunca está, y es el que hace que un diagrama sea
**útil** en vez de decorativo. Para cada activo:

```
   ┌──────────────┬───────────┬───────────┬──────────┬───────────────┐
   │ Activo       │ Estado     │ Verificado│ Última   │ Observación   │
   │              │ (diseño)   │ (realidad)│ cambio   │               │
   ├──────────────┼───────────┼───────────┼──────────┼───────────────┤
   │ sw-acceso-p3 │ activo     │ ✓ ok      │ 2026-05  │ —             │
   │ srv-web-01   │ activo     │ ⚠ validar │ 2026-09  │ carga alta,   │
   │              │            │           │          │ ver balanceo  │
   │ srv-dns-02  │ backup     │ ✗ CAÍDO   │ 2026-11  │ migrar        │
   │ fw-int-01   │ ??         │ ??         │ desconocido│ reemplazar  │
   │             │            │            │           │ en 2027       │
   │ srv-file-01 │ deprecado  │ ✓ ok      │ 2024-03  │ migrar a      │
   │              │            │           │          │ srv-file-02   │
   └──────────────┴───────────┴───────────┴──────────┴───────────────┘

   ESTADOS que hay que saber usar:
     activo       en producción, verificado
     en testing   se está probando, no es para producción
     deprecado    sigue andando pero se va a jubilar
     retirado     dado de baja (no debería estar en el diagrama)
     backup       en espera, no acepta tráfico
     PENDIENTE    ★ lo que dice tu imagen: definido, no comprobado
     DESCONOCIDO  nadie sabe
```

> **El "VALIDACIÓN PENDIENTE" de tu imagen no es una falta del diagrama: es
> información del diagrama.** Es la forma más honesta de dibujar "esto está
> **diseñado** pero **no comprobado**". Un diagrama que no tiene esa categoría
> obliga a elegir entre mentir (ponerlo todo como "activo") o no documentar
> (dejarlo afuera). **Un buen diagrama tiene la categoría, y la usa.**

**Y la diferencia entre estado *de diseño* y estado *verificado* es la clave:**

- **Diseño** = lo que dice el documento de arquitectura.
- **Verificado** = lo que alguien **comprobó mirando el equipo**.

Un diagrama solo con diseño **es un plan, no una descripción de la red**.

### Bloque 8 — Metadatos del propio diagrama

El bloque que casi nadie pone y que hace que el diagrama sea mantenible:

```
   ┌──────────────────────────────────────────────────────────────┐
   │  Documento: DIAGRAMA-RED-FING-v3                            │
   │  Fecha de creación:      2026-03-12                          │
   │  Fecha de última revisión: 2026-09-28   ← SIEMPRE              │
   │  Autor:                  Red 2 (red2@fing.edu.uy)            │
   │  Ámbito:                 Edificio A, niveles 1 a 3           │
   │  FUENTE DE VERDAD:       NetBox + Ansible + exporter SNMP   │
   │  Próxima revisión:       2026-12-15                          │
   │  Clasificación:          USO INTERNO                         │
   └──────────────────────────────────────────────────────────────┘
```

> **La "fuente de verdad" es el dato más importante.** Si el diagrama dice que se
> generó automáticamente desde **NetBox** o desde la **configuración con
> Ansible**, entonces hay una chance real de que esté **al día**. Si fue hecho a
> mano en un día, hay que asumir que está **desactualizado**. Eso cambia cómo lo
> usás en un incidente.

## 1.10 Los tipos de diagrama de red

Ahora sí: **qué tipos hay**. Y la respuesta corta es que **no hay un tipo, hay
varios**, y cada uno responde una pregunta distinta. Un diagrama que intenta
responder todas a la vez es ilegible.

### (a) Topología física (*physical topology*)

**Pregunta que responde:** ¿cómo están conectados **físicamente** los equipos?

```
   ┌──────────────────────────────────────────────────────────────┐
   │                                                              │
   │      sw-acc-01 ── sw-acc-02                                  │
   │           │            │                                     │
   │      sw-acc-03 ── sw-acc-04                                 │
   │           │                                                 │
   │        sw-dis-01  ──► sw-nucleo-01                          │
   │                                                              │
   │   Nodos = equipos. Aristas = cables / enlaces.                │
   │   NO se muestran IPs. NO se muestran VLANs.                  │
   │                                                              │
   └──────────────────────────────────────────────────────────────┘
```

**Para qué:** documentar **cómo pasar un cable**, redundancy física, dónde están
las **_conexiones_ de uplink**, plan de crecimiento de puertos.

**Herramientas:** Visio, draw.io, Lucidchart, y.io (topología automática desde
SNMP/CDP/LLDP).

### (b) Topología lógica (*logical topology*)

**Pregunta que responde:** ¿cómo **circula** el tráfico según el **enrutamiento**?

```
   ┌──────────────────────────────────────────────────────────────┐
   │                                                              │
   │        VLAN 10 ─────┐                                        │
   │                      ▼                                       │
   │                  sw-dis-01 ──── rtr-borde-01 ──► INTERNET   │
   │                      ▲                                       │
   │        VLAN 20 ─────┘                                        │
   │                                                              │
   │   Nodos = segmentos lógicos (subredes/VLANs).                │
   │   Aristas = rutas.                                           │
   │                                                              │
   └──────────────────────────────────────────────────────────────┘
```

**Para qué:** entender **por dónde va** un paquete, calcular **tiempos de
transito**, ver el impacto de un cambio de ruteo.

> **Físico vs. lógico, el ejemplo que lo aclara:** en un edificio con 6 switches
> en cascada (6 saltos), la topología **física** dice "6 saltos"; la **lógica**
> dice "1 salto". Un conmutado es **1 solo dominio de colisión** y **ningún
> salto** para efectos de latencia, aunque haya 6 equipos en el medio. **Y eso es
> exactamente lo que se pregunta en los problemas de retardo de examen.**

### (c) Diagrama de VLAN y spanning tree

**Pregunta que responde:** ¿qué VLAN hay, qué puertos son de acceso y cuáles son
trunk, y qué hace el STP?

```
   ┌──────────────────────────────────────────────────────────────┐
   │  VLAN 10 USUARIOS      VLAN 20 SERVIDORES                   │
   │  ┌───┐  ┌───┐          ┌───┐  ┌───┐                         │
   │  │p1 │  │p2 │          │p3 │  │p4 │                         │
   │  └─┬─┘  └─┬─┘          └─┬─┘  └─┬─┘                         │
   │    └──────┴────────────────┴──────┘                          │
   │           │ trunk 802.1Q (10,20) │                           │
   │           ▼                                                    │
   │      sw-dis-01 (root bridge del dominio)                     │
   │           │                                                    │
   │           ▼                                                    │
   │      sw-nucleo-01                                             │
   │                                                              │
   │   Rutas STP:                                                 │
   │     p1 → sw-dis-01 : FWD (designated)                        │
   │     p2 → sw-dis-01 : FWD (designated)                        │
   │     p4 → sw-dis-01 : BLK  ← alternate, se queda en espera   │
   └──────────────────────────────────────────────────────────────┘
```

**Para qué:** el diagrama **por excelencia del que se queja el usuario final**:
"en este piso la red anda lenta". La respuesta casi siempre es un **puerto
bloqueado por STP** que obliga al tráfico a hacer un rodeo.

### (d) Diagrama de firewall / NAT / seguridad

**Pregunta que responde:** ¿qué pasa con un paquete que entra o sale?

```
   ┌──────────────────────────────────────────────────────────────┐
   │                                                              │
   │  INTERNET                                                     │
   │     │                                                        │
   │     │ 200.1.1.10:443                                          │
   │     ▼                                                        │
   │  ┌──────────┐   regla 20    ┌──────────┐                    │
   │  │ fw-borde │───────────────►│ srv-web  │                    │
   │  │  (NAT +  │   (DNAT + LB)  │  01 y 02 │                    │
   │  │  filtrado│◄───────────────│          │                    │
   │  └────┬─────┘   regla 10    └──────────┘                    │
   │       │                                                        │
   │  ┌────▼─────┐   regla 30   ┌──────────┐                    │
   │  │ rtr-borde│───────────────► srv-dns  │                    │
   │  │ (enrut.) │   SNAT salida └──────────┘                    │
   │  └──────────┘                                                │
   └──────────────────────────────────────────────────────────────┘

   ★ Cada flecha = una regla, con su número.
   ★ El firewall va PRIMERO (la 20 va sobre la 10).
   ★ El router solo enruta: no filtra.
```

**Para qué:** auditar seguridad, entender por qué algo **no** se conecta,
depurar un problema de acceso.

### (e) Diagrama de flujo (*packet flow / traffic path*)

**Pregunta que responde:** ¿**por dónde pasa** este paquete específico?

```
   srv-web-01 ──(a)──► sw-acc-01 ──(b)──► rtr-borde-01
        │                                          │
        │                                    (c) NAT: 192.168.10.11
        │                                          │  → 200.1.1.2:3306
        │                                          ▼
        │                                    fw-borde-01
        │                                          │
        │                                    (d) filtra puerto 3306
        │                                          │  → DROP
        │                                          ▼
        │                                    ✗ NO LLEGA
   ─────────────────────────────────────────────────────────
   (a) L2: src MAC srv-web-01 → dst MAC rtr-borde-01 (trunk)
   (b) L2: src MAC srv-web-01 → dst MAC rtr-borde-01
   (c) SNAT: cambia IP origen y quizá puerto origen
   (d) no hay regla que permita 3306/TCP hacia la LAN → DROP
```

**Para qué:** es **el diagrama de depuración**. Cuando algo no funciona, se
recorre el camino salto a salto: ¿el switch reenvió? ¿el NAT se aplicó? ¿el
firewall dejó pasar? **Cada flecha tiene un punto de falla posible.**

### (f) Diagrama de secuencia (*sequence diagram*)

**Pregunta que responde:** ¿**qué mensajes** se exchanging y **en qué orden**?

```
   Cliente            Servidor DNS         Root         TLD        Autorit.
     │                    │                  │            │            │
     │─ CONSULTA (A) ────▶│                  │            │            │
     │                    │─ iterativa ─────▶│            │            │
     │                    │◀── "ve a .uy" ───│            │            │
     │                    │─ iterativa ────────────────────▶│            │
     │                    │◀── "ve a ns.x" ─────────────────│            │
     │                    │─ iterativa ────────────────────────────────▶│
     │                    │◀── 1.2.3.4, TTL 3600 ─────────────────────│
     │◀── RESPUESTA ──────│                  │            │            │
     │   (cachea 3600s)   │                  │            │            │
```

**Para qué:** es el diagrama de **TCP**, **TLS**, **DHCP**, **ARP**, **OSPF**. Y es
el que vas a tener que **dibujar de memoria** en el examen: el three-way
handshake, el DORA, el hello+hello+req+ack de OSPF.

### (g) Diagrama de rack / *wiring diagram*

**Pregunta que responde:** ¿qué cable va de dónde a dónde, **físicamente**?

```
   ┌───────────────────────── RACK A ─────────────────────────┐
   │ U48 ┤ ══════════ ═                                       │
   │ U47 ┤ ══════════ ═  ← cables al patch panel PP-A         │
   │ U46 ┤ ══════════ ═                                       │
   │  ...                                                        │
   │ U26 ┤ ══════════ ═                                       │
   │ U25 ┤ ┌──────────────┐                                   │
   │ U24 ┤ │ sw-dis-01    │  ← el switch                      │
   │ U23 ┤ └──────────────┘                                   │
   │  ...                                                        │
   │ U03 ┤ ┌──────────────┐                                   │
   │ U02 ┤ │ srv-dns-01   │  ← el servidor                    │
   │ U01 ┤ └──────────────┘                                   │
   └──────────────────────────────────────────────────────────┘

   Cable run sheet:
     A:U47.1 → PP-A:P12  → sw-dis-01 Gi0/24
     A:U46.1 → PP-A:P13  → sw-dis-01 Gi0/25
```

**Para qué:** es el diagrama del **técnico de campo**. No se entiende, no se
discute: se **usa**. Y es el único diagrama que se verifica **con las manos**.

### (h) Diagrama de direccionamiento / addressing

**Pregunta que responde:** ¿cómo está repartido el espacio de direcciones?

```
   ┌──────────────────────────────────────────────────────────────┐
   │  RFC 1918 — espacio privado                                 │
   │                                                              │
   │  10.0.0.0/8          →  10.1.0.0/16    (FING, sede A)      │
   │  10.0.0.0     [       10.2.0.0/16    (FING, sede B)      │
   │                   [   10.3.0.0/16    (laboratorios)      │
   │                                                              │
   │  172.16.0.0/12       →  172.16.1.0/24  (acceso)          │
   │  172.16.0.0      [      172.16.2.0/24  (gestión)          │
   │                   [   172.16.3.0/24  (servidores)        │
   │                                                              │
   │  192.168.0.0/16      →  192.168.1.0/24 (red local, casa)  │
   │  192.168.0.0    [   192.168.0.0/28  (NAT LAN)            │
   │                                                              │
   │  PÚBLICO             →  200.1.1.0/24  (rutable, contratado)│
   └──────────────────────────────────────────────────────────────┘
```

**Para qué:** es **el diagrama de subnetting**. Acá van los `/n`, los gateways,
los rangos de DHCP y las reservas. Y es **literalmente el ejercicio de examen**
del bloque D, dibujado.

## 1.11 Los seis pasos para hacer un diagrama de verdad

Esto es el método, y es lo que hay que hacer cuando te pidan "hacé un diagrama
de esta red":

```
   1. RECOLECTAR    Inventario, contrato con el proveedor, configs,
                    salida de "show inventory", nmap.

   2. CLASIFICAR    ¿Qué pregunta responde este diagrama? Elegí UN tipo
                    (§1.10). Si es un entregable, probablemente hace falta
                    un (a) físico + un (d) de seguridad.

   3. ESQUEMATIZAR  Dibujá los BLOQUES (redes, zonas), no los equipos.
                    Un rectángulo por red, con su CIDR adentro.
                    Después poné los equipos adentro de su bloque.

   4. CONECTAR      Una flecha = un enlace. Etiquetá cada flecha con:
                    · tipo de medio (cobre/fibra)
                    · ancho de banda (100M / 1G / 10G)
                    · VLAN / trunk
                    · longitud estimada

   5. ANOTAR        Aplicá los ocho bloques de §1.9. En este orden:
                    identidad → L3 → L2 → firewall → NAT → puertos →
                    ESTADO → metadatos.

   6. VERIFICAR     ★ El paso que nadie hace. Andá al equipo y comprobá.
                    Lo que no pudiste verificar va marcado
                    "VALIDACIÓN PENDIENTE".
                    Poné la fecha de la verificación.
```

> **El paso 6 es el que convierte un dibujito en un documento.** Es exactamente
> lo que tu imagen estaba marcando: lo que no está verificado, **tiene que estar
> marcado**. Un diagrama sin fecha de verificación y sin marca de "pendiente" es
> un diagrama que **miente con la mejor intención**.

## 1.12 La checklist: ¿mi diagrama está listo?

Usá esto antes de dar por terminado cualquier diagrama:

```
   IDENTIDAD
   [ ] ¿Cada equipo tiene nombre formal, modelo, ubicación y responsable?
   [ ] ¿Cada equipo tiene un ID de inventario?

   L3
   [ ] ¿Cada host tiene IP, máscara/CIDR y gateway?
   [ ] ¿Cada router tiene TODAS sus interfaces con su CIDR?
   [ ] ¿Las dos notaciones de máscara (/24 y 255.255.255.0)?
   [ ] ¿Los rangos de DHCP y las IPs fijas de cada VLAN?

   L2
   [ ] ¿Las VLAN numeradas Y nombradas?
   [ ] ¿Qué puertos son de acceso y cuáles trunk, con qué etiquetas?
   [ ] ¿Qué hace el spanning tree (raíz, puertos bloqueados)?

   SEGURIDAD
   [ ] ¿Las reglas de firewall, con su número y su estado?
   [ ] ¿Los puertos exactos y protocolos de cada servicio?
   [ ] ¿Qué servicios están expuestos a Internet?

   NAT
   [ ] ¿Las VIPs públicas y a qué pool apuntan?
   [ ] ¿El método de balanceo?
   [ ] ¿El NAT de salida (SNAT) y el de entrada (DNAT), por separado?

   ESTADO  ← el bloque que casi todos olvidan
   [ ] ¿El estado real de cada activo (activo / deprecado / caído / pendiente)?
   [ ] ¿Qué está VERIFICADO y qué no?
   [ ] ¿Los unknowns están marcados como desconocidos?

   METADATOS
   [ ] ¿Fecha de última revisión?
   [ ] ¿Autor y fuente de verdad?
   [ ] ¿Próxima revisión agendada?
```

## 1.13 ⚠️ Actualización a 2026

**Sigue igual — de memoria:**
- La necesidad de **documentar en un diagrama** es la misma de siempre.
- Los **cuatro bloques** básicos: L3, L2, seguridad y estado.
- La diferencia entre **topología física** y **lógica**, y por qué en un
  conmutado 6 equipos físicos son 1 salto lógico.
- La importance de la **dirección IP, la máscara y el gateway** en cada nodo.

**Cambió:**

- **El diagrama se genera solo.** Con fuentes como **NetBox**, **phpIPAM**,
  **AWX/Ansible** (que lee la configuración real de los routers) y **Ansible
  Network**, hoy se puede **exportar el diagrama directamente del equipo que
  tiene la verdad**. Eso resuelve de raíz el problema de "el diagrama está viejo".
- **Los diagramas de servicios en la nube (SaaS, balanceo, CDN)** ya no son "la red": son **flujos entre servicios**, y hay que documentarlos igual.
  red": son **flujos entre servicios**, y hay que documentarlos igual.
- **La verificación es automatizable.** Con la observación como código
  (infraestructura como código, pipelines de CI), un diagrama "VALIDACIÓN
  PENDIENTE" puede **dejarse de marcar** porque la verificación es **un test que
  corre siempre**.
- **El bloqueo de STP sigue siendo la causa número uno** de las quejas de
  rendimiento en los edificios: sigue valiendo la pena un diagrama de STP.

> **Para el examen:** el examen **no pide hacer un diagrama profesional de
> producción**, pide **un diagrama de topología con las direcciones, que permita
> resolver tablas de ruteo o de ARP**. Eso es un tipo (a) más un (h). Pero saber
> qué información va es lo que te permite **leer** cualquier topología que te
> den.


# PARTE 2 — PRÁCTICA RESUELTA

## 2.1 Ejercicio 1 — Los seis parámetros en un caso concreto

**Enunciado.** Ana está en Montevideo y hace una videollamada con Ana (sic, con Bea, que está en Frankfurt). La conexión va por fibra, pasa por 11 routers, y el informe de la conexión dice:

```
  Ancho de banda del enlace de la casa:  300 Mbps
  Distancia total del camino (ida):      11 400 km
  Velocidad de propagación en la fibra:  2·10⁸ m/s
  Tamaño medio de un paquete de video:   1 200 bytes
  Retardo medido por ping (RTT):         142 ms
  Retardo medido para el paquete 1:      71 ms
  Retardo medido para el paquete 2:      78 ms
  Retardo medido para el paquete 3:      102 ms
  Pérdidas observadas:                    0,4 %
  Velocidad sostenida de la descarga:    271 Mbps
```

**Se pide:** identificar cada magnitud, decir en qué unidad está, y explicar las dos diferencias que más se confunden.

**Resolución paso a paso.**

**Paso 1 — ¿Cuál es el ancho de banda?**

```
  "Ancho de banda del enlace de la casa: 300 Mbps"
  → 300 · 10⁶ bits por segundo
  → Es la CAPACIDAD MÁXIMA. Está en bps. Es una propiedad del equipo
    (el ONT y el medio).
```

**Paso 2 — ¿Cuál es la velocidad de propagación?**

```
  "Velocidad de propagación en la fibra: 2·10⁸ m/s"
  → Está en m/s. Es la rapidez de la SEÑAL.
  → Es una propiedad de la FIBRA (del medio), no del equipo.
  → Por eso el informe no la reporta en bps: no es una capacidad.
```

**Paso 3 — ¿Cuál es la latencia y cuál es el RTT?**

```
  "Retardo medido por ping (RTT): 142 ms"
  → 142 ms es el Round Trip Time: ida + vuelta.

  "Retardo medido para el paquete 1: 71 ms"
  → 71 ms es la LATENCIA (tiempo de un viaje, de ida).

  Chequeo de coherencia:  71 ms × 2 = 142 ms  ✓
  → El RTT es exactamente el doble. Éste es el control que tenés
    que hacer SIEMPRE que te den latencia y RTT juntos.
```

**Paso 4 — ¿Cuál es el throughput?**

```
  "Velocidad sostenida de la descarga: 271 Mbps"

  271 Mbps  <  300 Mbps  ✓ (el throughput nunca supera el BW)

  eficiencia = 271/300 = 0,9033  →  90,3 %
  La diferencia (9,7 %) se va en:
    - cabeceras: 58 bytes de overhead por cada 1200 de datos
      1200 + 58 = 1258 bytes en el medio
      eficiencia de payload = 1200/1258 = 0,9539
    - pérdidas y retransmisiones: 0,4 % (cada pérdida por TCP obliga
      a retransmitir un segmento entero, y el TCP pierde también la
      ventana durante el RTO)
    - colisiones y, si lo modelás, slots ocupados
```

**Paso 5 — ¿Cuál es el jitter?**

```
  Retardos de tres paquetes del MISMO flujo:
    paquete 1:  71 ms
    paquete 2:  78 ms
    paquete 3: 102 ms

  jitter (medición pico a pico) = 102 − 71 = 31 ms
```

**Interpretación y por qué importa.** El paquete 3 tardó 31 ms más que el paquete 1. Eso no es un problema de ancho de banda: la señal viaja a la misma velocidad. Es un problema de **cola**: somewhere en el camino, 31 ms de espera. En una videollamada de voz, eso produce un desfasaje entre el audio y el video: el labio se ve antes de que se oiga la palabra.

**Paso 6 — La tabla resumen del ejercicio.**

```
  ┌──────────────────────┬────────────────────────┬──────────┐
  │ Magnitud             │ Valor del enunciado    │ Unidad   │
  ├──────────────────────┼────────────────────────┼──────────┤
  │ Ancho de banda       │ 300 Mbps               │ bps      │
  │ Vel. de propagación  │ 2·10⁸                  │ m/s      │
  │ Latencia             │ 71 ms                  │ ms       │
  │ RTT                  │ 142 ms (= 2×71)        │ ms       │
  │ Retardo total        │ 71 ms (el mismo packet)│ ms       │
  │ Throughput           │ 271 Mbps               │ bps      │
  │ Jitter               │ 31 ms                  │ ms       │
  └──────────────────────┴────────────────────────┴──────────┘
```

### ⚠️ Errores típicos de este ejercicio

- **Confundir latencia con RTT.** La latencia es un viaje; el RTT son dos. Si el ping dice 142, la latencia es ~71 (asumiendo camino simétrico).
- **Meter la velocidad de propagación en bps.** Si aparece "2×10⁸ Mbps" es un error de unidades: 2×10⁸ es **m/s**.
- **Decir que el throughput "es 300 Mbps".** No: el throughput es lo que **seNwgets**; el BW es lo que **se puede**.
- **Usar `d/s` con la distancia de ida para el RTT.** `d/s` te da la latencia; para el RTT, `2d/s`.

---

## 2.2 Ejercicio 2 — Velocidad de propagación en cobre vs. fibra

**Datos.** Un enlace de 800 km une dos edificios de una misma ciudad. Hay dos opciones:

- **Opción A**: un haz de **cobre** (UTP Cat 6A).
- **Opción B**: una **fibra óptica monomodo**.

La velocidad de propagación medida por el instalador es:

```
  Cobre (Cat 6A): s = 2,0 · 10⁸ m/s
  Fibra monomodo:  s = 2,04 · 10⁸ m/s
```

**a) ¿Cuál es el retardo de propagación de la señal en cada caso?**
**b) ¿Cuánto tarda un paquete de 5 000 bits en cruzar el enlace, con store-and-forward en un switch de 10 Gbps en cada extremo?**
**c) ¿Conviene pagar la fibra?**

**Resolución.**

**a) Retardo de propagación.**

```
  d = 800 km = 800 000 m

  Opción A (cobre):
    d_prop = d / s = 800 000 m / (2,0 · 10⁸ m/s)
           = 4,0 · 10⁻³ s
           = 0,004 s
           = 4,0 ms

  Opción B (fibra):
    d_prop = d / s = 800 000 m / (2,04 · 10⁸ m/s)
           = 3,9216 · 10⁻³ s
           = 0,0039216 s
           = 3,92 ms
```

**b) Retardo total, con store-and-forward.**

El paquete de 5 000 bits **entra** por un puerto de 10 Gbps del switch de la izquierda y tiene que **entrar entero** antes de que ese switch pueda empezar a mandarlo por el puerto de salida (store-and-forward).

```
  L = 5 000 bits
  R = 10 Gbps = 10 · 10⁹ bits/s

  d_transmisión = L / R = 5 000 / (10 · 10⁹) = 5 · 10⁻⁷ s = 0,0005 ms
  d_proc (switch de 10 Gbps con HER stacking) ≈ 0 (despreciable)

  Opción A (cobre):
    d_total = d_proc + d_transmisión + d_cola + d_prop
            = 0 + 0,0005 ms + 0 (sin cola) + 4,0 ms
            = 4,0005 ms

  Opción B (fibra):
    d_total = 0 + 0,0005 ms + 0 + 3,92 ms
            = 3,9205 ms
```

**c) ¿Conviene pagar la fibra?**

La diferencia es de 0,08 ms **en un viaje**. Con las dos manos atrás y atrás: 0,16 ms de RTT.

```
  Diferencia por viaje: 4,0 − 3,92 = 0,08 ms
  Diferencia en RTT:    2 × 0,08  = 0,16 ms
```

**Respuesta: para latencia, no. La diferencia es despreciable.** La fibra no compra latencia en este caso, y eso es una sorpresa muy frecuente: se supone que "la fibra es más rápida", pero **propagar la señal es un fenómeno físico, y la luz no va más rápido en fibra que en cobre**. Va a 2/3 de la velocidad de la luz en el vacío en los dos casos.

**Pero la fibra sí compra otra cosa**, y esta es la respuesta completa:

```
  ┌────────────────────────┬──────────────┬──────────────┐
  │                        │ COBRE        │ FIBRA        │
  ├────────────────────────┼──────────────┼──────────────┤
  │ Velocidad de prop.     │ 2,00·10⁸     │ 2,04·10⁸     │  ← casi igual
  │ Retardo de prop. (800km)│ 4,00 ms      │ 3,92 ms      │  ← casi igual
  │ Ancho de banda posible │ 10 Gbps      │ 100+ Gbps    │  ← AQUÍ está la diferencia
  │ Alcance sin repetidor  │ ~100 m       │ ~80 km       │  ← y acá
  │ Inmune a EMI           │ no           │ sí           │  │
  │ Peso por metro         │ ~0,05 kg/m   │ ~0,02 kg/m   │  │
  │ Costo del transceiver  │ ~40 USD      │ ~80-400 USD  │  │
  └────────────────────────┴──────────────┴──────────────┘
```

**La moraleja:** la fibra se paga por **ancho de banda**, por **alcance sin electrónica**, y por **inmunidad al ruido electromagnético** — **no por latencia**.

> ⚠️ **Precisión sobre "más rápido":** en los formatos eléctricos de Ethernet (10BASE-T, 100BASE-TX) hay un **retardo de codificación de línea** que la fibra no tiene (MLT-3, 4B/5B y *scrambler* contra NRZI de la fibra). Pero ese retardo es de **nanosegundos a unas decenas de nanosegundos**, no de milisegundos. Para 800 km, es ruido estadístico frente a los 4 ms de propagación.

---

## 2.3 Ejercicio 3 — Por qué la velocidad de propagación NO depende del ancho de banda

**Enunciado.** Dos proveedores ofrecen enlaces para el mismo trayecto de 50 km:

| | Proveedor A | Proveedor B |
|---|---|---|
| Ancho de banda | 100 Mbps | 1 Gbps |
| **Velocidad de propagación medida** | **2,0 · 10⁸ m/s** | **2,0 · 10⁸ m/s** |
| Latencia medida (ping, 1x) | 5,0 ms | 5,0 ms |

Un alumno le pregunta al proveedor: "¿el enlace más rápido no debería llegar antes?". **Justificá por qué la respuesta del proveedor es la correcta, y qué pasa con el RTT y con el throughput.**

**Resolución paso a paso.**

**Paso 1 — Qué determina `s`.**

La velocidad de propagación la determina la **velocidad de la perturbación electromagnética en el medio**, que es una propiedad de la **electricidad y la óptica del material**:

```
  ──────────────────────────────────────────────────────────────────
  VACÍO / AIRE    el campo E y el campo B se propagan juntos, a c
                  = 3·10⁸ m/s. No hay medio que "frenar" nada.
  ──────────────────────────────────────────────────────────────────
  COBRE           los electrones libres arrastran a los ligados
                  al mover el campo E. Resultado neto: ~0,6 a 0,7 c
  ──────────────────────────────────────────────────────────────────
  FIBRA (Si)      la luz refracta con índice n ≈ 1,48. v = c/n.
                  3·10⁸ / 1,48 = 2,03·10⁸ m/s
  ──────────────────────────────────────────────────────────────────
  ```

**En los tres casos, `s` depende de una constante del material y de nada más.**

**Paso 2 — Qué determina `R` (ancho de banda).**

`R` lo determina **cuántos bits se pueden codificar por unidad de tiempo sobre esa señal**:

```
  10 Mbps   = 1 símbolo cada 100 ns   (o 2 símbolos cada 200 ns con 2 niveles)
  1 Gbps    = 1 símbolo cada 1 ns
```

Y **el reloj del transceptor es una consecuencia de la electrónica del circuito**, no de la física del medio. El medio dice "la perturbación viaja a 2×10⁸ m/s"; el circuito dice "y yo puedo modular 10⁹ cambios por segundo sobre esa perturbación".

**Paso 3 — La analogía del caño.**

```
   ┌──────────┐                                            ┌──────────┐
   │  Grifo   │ ═══════════════════════════════════════════ │ Depósito │
   │ 1 CLIQUE │        ← 50 km de caño de 20 mm            │          │
   └──────────┘                                            └──────────┘
     (mucha presión)          (el medio)              (mucho caudal)

  ▸ Abrir la llave más rápido (más caudal, más ancho de banda) NO
    hace que el agua llegue antes por el caño. El tiempo de viaje lo
    fija la longitud del caño y la velocidad del fluido.

  ▸ El caudal sí cambia CUÁNTA agua llega por segundo.
```

**Paso 4 — Qué pasa entonces con los números.**

```
  Distancia = 50 km = 50 000 m
  s        = 2,0 · 10⁸ m/s

  d_prop = 50 000 / (2·10⁸) = 2,5 · 10⁻⁴ s = 0,25 ms  ← IGUAL en A y en B

  ───────────────────────────────────────────────────────────────
                        R      d_trans (L=1500B)   throughput máx.
  Proveedor A        100 Mbps  120 µs            ≈  96 Mbps
  Proveedor B         1 Gbps    12 µs            ≈ 961 Mbps
  ───────────────────────────────────────────────────────────────
  d_prop                    0,25 ms          0,25 ms   ← IGUAL
  ───────────────────────────────────────────────────────────────
```

```
  Con 11 routers en el camino y d_proc despreciable:

  RTT (sin cola) = 2 · (11 · 0,25 ms) = 2 · 2,75 ms = 5,5 ms
  → IGUAL para A y para B.
```

**Interpretación — y esta es la frase para el examen:**

> **El ancho de banda dice cuántos datos entran por segundo; la velocidad de propagación dice a qué velocidad viaja la información.** Un enlace de 1 Gbps **no es "50 veces más rápido"**: es 50 veces más **ancho**. Un paquete **individual** tarda **exactamente lo mismo** en los dos casos, porque su **retardo de transmisión** sí es 10 veces menor (12 µs contra 120 µs), pero ese componente es **diminuto comparado con la propagación** (0,25 ms). Lo que el ancho de banda cambia de verdad es el **throughput**: cuántos bytes por segundo lográs mover **por unidad de tiempo**, no cuánto tardás en llegar.

**Paso 5 — El corolario que aparece en los exámenes: el BDP.**

Como el RTT **no depende** del ancho de banda, y el ancho de banda **sí** determina cuántos datos podés mandar por unidad de tiempo, el número de bytes que están "en vuelo" en un momento dado es:

```
  BDP (bandwidth-delay product) = R · RTT

  Proveedor A:  100 · 10⁶ bps × 5,5 · 10⁻³ s = 550 000 bits = 68,75 kB
  Proveedor B:   1 · 10⁹ bps × 5,5 · 10⁻³ s = 5 500 000 bits = 687,5 kB
```

**Derivación paso a paso para A:**

```
  R   = 100 · 10⁶ bits/s
  RTT = 5,5 · 10⁻³ s

  BDP = 100 · 10⁶ bits/s × 5,5 · 10⁻³ s
      = 100 · 5,5 · 10⁶ ⁻³ bits
      = 550 · 10³ bits
      = 550 000 bits
      = 550 000 / 8 bytes
      = 68 750 bytes
      ≈ 68,75 kB
```

**Interpretación del BDP.** En el proveedor B, para llenar el tubo de punta a punta tenés que tener **687,5 kB en vuelo**. Si tu ventana de TCP es de 128 kB (el `rwnd` típico por defecto hace años), **nunca llenás el enlace**: mandás 128 kB, esperás el ACK, y la tubería queda medio vacía. **Por eso un enlace rápido con RTT largo necesita una ventana grande**: es el motivo por el que `Window Scale` (RFC 7323) existe, y por el que las conexiones de larga distancia tienen throughput limitado por la ventana y no por el ancho de banda. Se desarrolla entero en las Clases 5 y 6.

---

# PARTE 3 — PROBLEMAS DE EXAMEN DE FING

## 3.1 Mapa de los problemas de examen del Bloque A

Antes de resolver nada, el mapa. Esto es lo que vas a encontrar en los exámenes del bloque:

| Examen | Pregunta | Tema | Dónde se resuelve |
|---|---|---|---|
| `2006-12` | P1 (5 pts) | Modelo OSI y las hipótesis de las 7 capas | **Clase 2** |
| `2007-03` | P1 (5 pts) | El modelo TCP/IP | **Clase 2** |
| `2009-02` | P2 (10 pts) | Forwarding vs. routing; flooding en broadcast | **Clase 3** |
| `2009-02` | P3 (5 pts) | FDMA y TDMA | **Clase 7** |
| `2009-02` | P4 (9 pts) | Datagramas vs. circuitos virtuales | **Clase 4** |
| `2009-03` | P5 (6 pts) | Full duplex vs. half duplex | **Clase 7** |
| `2006-08` | P1 (5 pts) | Resultados de Nyquist y Shannon con hipótesis | **Clase 7** |
| `2007-07` | P1 (10 pts) | Capacidad máxima sobre línea telefónica (Shannon) | **Clase 7** |
| `2007-12` | P3 (10 pts) | Conmutación de circuitos, paquetes y mensajes | **Clase 4** |
| `2009-12` | P1 (10 pts) | Componentes del retardo; BW vs. `s`; congestión | **Clase 5** (adelanto acá) |
| `2011-03` | P2 (6 pts) | Congestión, pérdidas y retardo | **Clase 5** |
| `2011-03` | P5 (10 pts) | Retardo end-to-end, 3 enlaces y 2 conmutadores | **Clase 6** |

**Nota sobre los puntajes:** el enunciado de `2006-12 P1` y de `2007-03 P1` dice **5 puntos** cada una en el PDF oficial (no 10). Lo verifiqué en `sirc0612.txt` y en `sirc0703.txt`. Tomá esos números como referencia.

## 3.2 ⭐ Adelanto: la Pregunta 1a del Examen 2009-12 (resuelta aquí, se repite en la Clase 5)

> **Fuente:** Examen `sirc0912` — 18 de diciembre de 2009, Pregunta 1 (10 puntos), apartado a).
> **Link:** https://www.fing.edu.uy/inco/cursos/redescomp/examenes/sirc0912.pdf

### Enunciado (texto del examen)

> Identifique los componentes del retardo en las redes de paquetes, y señale cuáles son los más significativos. En particular:
> **a)** Señale las diferencias entre el ancho de banda y la velocidad de propagación en el medio.
> **b)** ¿En qué componente del retardo influye la congestión?

### Solución oficial (apartado a)

> a) B es la capacidad de los puertos del dispositivo (switch o router), por ejemplo Ethernet, STM-1, mientras que s es una característica del medio, por ejemplo s ~ 2×10⁸ m/seg en cobre.

### Análisis de la solución oficial

La respuesta oficial es **correcta y corta**, y contiene exactamente las dos ideas que hay que decir:

1. **`B` es la capacidad de los puertos del dispositivo** (switch o router), es decir, del **equipo**.
2. **`s` es una característica del medio**, por ejemplo `s ≈ 2×10⁸ m/s` en cobre.

**Lo que le falta y hay que agregar para el punto completo** (no restan si no lo decís, pero el profesor espera que completes):

- **Las unidades**: `B` en **bps**, `s` en **m/s**. Es la diferencia formal y la que hace que no sean la misma magnitud.
- **Que son ejes perpendiculares**: podés tener el mismo `s` con distinto `B` (cobre a 100 Mbps y a 10 Gbps) y distinto `s` con el mismo `B`.
- **Que `s` NO cambia con el medio de enlace en el sentido de "más rápido"**: tanto cobre como fibra dan ~2×10⁸ m/s. Lo que cambia con el medio es la **capacidad** y el **alcance**.
- **La consecuencia**: `d_transmisión = L/R` (no depende del medio) vs. `d_propagación = d/s` (no depende del paquete).

> ⚠️ **Detalle sobre la solución oficial:** dice `s ~ 2×10⁸ m/s` **en cobre**, que es correcto. Si lo generalizás a "en el medio" sin aclarar, cuidado: en el vacío y en el espacio es 3×10⁸ m/s, y en el aire es 2,998×10⁸. Para problemas de examen de fibra y cobre, usá **2×10⁸**; para un enlace por satélite, **3×10⁸**.

### Mi respuesta completa para 10 puntos (o los 4 del apartado a)

```
  ANCHO DE BANDA (B o R)
    - unidad: bits por segundo (bps)
    - qué es: la CAPACIDAD MÁXIMA de transferir datos por el enlace
    - de qué depende: del EQUIPO (puerto, transceiver, modulación).
      Ethernet de 1 Gbps, STM-1 de 2,048 Mbps, 100 GbE.
    - no depende de: la longitud del enlace, del medio físico.
    - aparece en:  d_transmisión = L / R

  VELOCIDAD DE PROPAGACIÓN (s)
    - unidad: metros por segundo (m/s)
    - qué es: a qué velocidad física viaja la SEÑAL por el medio
    - de qué depende: del MEDIO FÍSICO (la física del material).
      Cobre ~2·10⁸ m/s, fibra ~2·10⁸ m/s, vacío 3·10⁸ m/s.
    - no depende de: la longitud del enlace, del equipo, del
      ancho de banda.
    - aparece en:  d_propagación = d / s

  CONCLUSIÓN
  Son magnitudes DISTINTAS, de UNIDADES DISTINTAS y que dependen de
  COSAS DISTINTAS: una del equipo y una del medio. El ancho de banda
  NO es "la velocidad a la que viaja la información": es la cantidad
  de información por segundo. La velocidad de propagación es la
  rapidez del mezzo físico. Un enlace de 1 Gbps por cobre y otro de
  1 Gbps por fibra tienen el MISMO ancho de banda y la MISMA
  velocidad de propagación, pero eso NO SIGNIFICA que se comporten
  igual: difieren en atenuación, en alcance sin repetidores y en
  inmunidad al ruido electromagnético.
```

### Apartado b) — adelanto (se resuelve entero en la Clase 5)

> **Solución oficial:** *"El retardo de encolamiento depende del nivel de congestión del router."*

Interpretado: la congestión **no** actúa sobre el retardo de transmisión ni sobre el de propagación (esos dependen de `L`, `R`, `d` y `s`, que no cambian con la carga). Actúa sobre el **retardo de encolamiento**, porque es el único componente que depende de **cuánta gente está delante tuyo en la cola**. Y si la cola se llena, aparecen **pérdidas**.

**La cadena completa, que es lo que pide el apartado:**

```
  Más tráfico offered → colas más largas → retardo de encolamiento ↑ → retardo total ↑
                                                          │
                                                          └─→ si la cola se llena:
                                                              PERDIDAS
```

---

# PARTE 4 — CIERRE

## 📌 Resumen en 10 líneas

1. **Red** = computadores interconectados por un medio, para compartir recursos e intercambiar información. Tres motivos: comunicar, compartir lo caro, y **economía de escala** (`C_red/n` decrece con `n`).
2. **PAN / LAN / MAN / WAN** por alcance: ~10 m, ~1 km, una ciudad, el planeta. **En 2026 el criterio útil es latencia + propiedad**: una red es LAN si no pasa por un router que no es tuyo.
3. **Latencia es el criterio moderno**: 500 ms de RTT de un satélite a 36.000 km es "WAN" aunque la distancia sea la de un edificio; una fibra de operador dentro de una ciudad da 0,5 ms a 100 km, que es mejor que cualquier LAN de 2005.
4. **Topologías**: bus (cable mínimo, un punto de falla), estrella (falla aislada, un dominio de colisión por puerto), anillo (retardo predecible, un punto de falla), malla (redundancia, `n(n-1)/2` enlaces), árbol (jerarquía), **híbrida (lo que se instala: malla arriba, estrella abajo, anillo para protección)**.
5. **Cada dispositivo, su capa**: hub/repetidor/módem = **1**; NIC = **1 y 2**; switch/AP = **2**; router = **3**; firewall stateful = **3 y 4**; servidor = todas.
6. **Ancho de banda** (`B`, **bps**) = capacidad del **equipo**, aparece en `L/B`.
7. **Velocidad de propagación** (`s`, **m/s**) = rapidez de la señal en el **medio**, aparece en `d/s`. **Cobre ≈ fibra ≈ 2·10⁸ m/s; vacío ≈ 3·10⁸ m/s.**
8. **Latencia** = un viaje; **RTT = dos viajes** (≈ `2d/s` sin colas). **Throughput** = lo real, siempre `< ancho de banda`, por cabeceras, retransmisiones y colisiones. **Jitter** = la variación entre paquetes del mismo flujo.
9. **`BDP = R · RTT`** = los bits que caben en el enlace durante un RTT = los que tenés que tener "en vuelo". Enlace rápido + RTT largo ⇒ **ventana grande obligatoria** o el ancho de banda no se aprovecha.
10. **Internet ≠ Web**: Internet es la red (IP, TCP, BGP); la Web es una aplicación (HTTP, HTML, URL). **Internet sin Web funciona; Web sin Internet no.**

## ✅ Autoevaluación

Respondé sin mirar. Las respuestas están en `<details>`.

**1.** Una red de 800 km a 1 Gbps y otra de 800 km a 10 Mbps. ¿Cuál tarda más en llegar un paquete de 1500 bytes?

<details><summary>Respuesta</summary>

**Ninguna de las dos, si la fibra es la misma.** El retardo de propagación es `d/s` y no depende de `R`.

```
  d = 800 000 m, s = 2,0 · 10⁸ m/s
  d_prop = 800 000 / 2,0·10⁸ = 4,0 ms   (igual en las dos redes)
```

Lo único que cambia es el retardo de transmisión, que es diminuto al lado de la propagación:

```
  A 10 Mbps: d_trans = 12 000 bits / 10 · 10⁶ = 1 200 µs = 1,2 ms
  A  1 Gbps: d_trans = 12 000 bits / 10 · 10⁹ =    12 µs = 0,012 ms

  Total a 10 Mbps: 1,2 + 4,0  = 5,2 ms
  Total a  1 Gbps: 0,012 + 4,0 = 4,012 ms
```

O sea: **el enlace de 10 Mbps tarda 1,19 ms más**, y ese 1,19 ms es 100 % transmisión, 0 % propagación. Lo que cambia de verdad es el throughput, no la latencia.

</details>

**2.** En una red con 500 Mbps de ancho de banda y un throughput medido de 380 Mbps, ¿cuál es el más alto, el ancho de banda o la velocidad de propagación? ¿Se puede responder la segunda sin más datos?

<details><summary>Respuesta</summary>

El ancho de banda es 500 Mbps. Es el número que tenemos, y es una **capacidad**.

La **velocidad de propagación no se puede calcular** con esos datos: es una propiedad del medio y hace falta saber cuál es. Si el medio es cobre o fibra, es ~2·10⁸ m/s; si es un enlace por satélite, ~3·10⁸ m/s.

**No son comparables**, justamente por eso: uno está en bps y el otro en m/s. La pregunta "cuál es más alto" no tiene sentido entre ellos. Lo que sí tiene sentido es la pregunta del Examen 2009-12: **¿de qué depende cada uno?** — `B` del equipo, `s` del medio.

Y la eficiencia: `380/500 = 76 %`. Los 24 % que faltan son cabeceras, retransmisiones por pérdidas, y slots perdidos por colisiones.

</details>

**3.** ¿Por qué un auricular Bluetooth es un PAN y un enlace de fibra entre dos edificios a 4 km es una WAN?

<details><summary>Respuesta</summary>

Por la **propiedad** y, en parte, por la latencia.

- El auricular es **tuyo**, de una sola persona, con latencia sub-milisegundo. Tenés el medio y el equipo: es un PAN.
- El enlace de fibra de 4 km **no es tuyo**: es de un operador. Para vos es infraestructura de terceros, como el backbone de Internet. Y si es fibra oscura conmutada de un operador, la latencia puede ser de 0,3 a 2 ms, que es "de WAN" para vos por propiedad aunque el número sea de LAN.

El alcance (10 m contra 4 km) coincide con la clasificación clásica, pero **lo que define la frontera es que uno es tuyo y el otro no**.

</details>

**4.** Un switch tiene 8 puertos y un hub tiene 8. ¿Cuántos dominios de colisión hay en cada caso?

<details><summary>Respuesta</summary>

- **Switch: 8 dominios de colisión y 1 dominio de broadcast.** Cada puerto es un dominio de colisión separado: solo hay una estación en cada segmento, así que **nunca hay colisión** (y por eso no hace falta CSMA/CD por encima de 1 Gbps).
- **Hub: 1 dominio de colisión y 1 dominio de broadcast.** El hub es un repetidor multi-puerto: repite la señal eléctrica a los 8 puertos. Las tres tramas que se mandan al mismo tiempo **colisionan**, y todas las estaciones los ven.

El hub es de **capa 1** por eso: no aprende direcciones, no decide a qué puerto va la trama, solo amplifica. El switch es de **capa 2** porque mantiene una tabla de MACs y decide.

</details>

**5.** Explicá con tus palabras por qué el ancho de banda y la velocidad de propagación son perpendiculares.

<details><summary>Respuesta</summary>

Porque uno describe **cuánto por segundo** y el otro **a qué velocidad**, y dependen de objetos distintos:

- El **ancho de banda** depende del **equipo**: de la electrónica del transceptor, del reloj, de la modulación. Podés subirlo de 100 Mbps a 10 Gbps **sin tocar el cable**.
- La **velocidad de propagación** depende del **medio**: de la física del material. Podés cambiar de cobre a fibra y sube de 2,00 a 2,04·10⁸ m/s: **un 2 %**, mientras que el ancho de banda habría que multiplicarlo por 1000.

La analogía: el ancho de banda es el **caudal** de un caño (litros por segundo) y `s` es la **velocidad del agua dentro** del caño. Abrir la válvula más rápido aumenta el caudal y no cambia la velocidad con que el agua recorre el caño. Por eso un paquete **individual** tarda lo mismo en los dos casos.

</details>

**6.** Una aplicación de video tiene un throughput de 8 Mbps en un enlace de 20 Mbps. ¿Cuánto del ancho de banda se está desaprovechando y a qué lo atribuís?

<details><summary>Respuesta</summary>

```
  desaprovechado = 20 − 8 = 12 Mbps
  eficiencia = 8/20 = 40 %
```

**Ese 60 % no es "ancho de banda desperdiciado"**: es la **sobrecarga del enlace**, que es lo que permite que la latencia sea baja. Si la aplicación usara el 100 %, la cola del búfer del router sería infinita y el retardo se dispararía. El 60 % de holgura es **la inversión en latencia**.

Las causas del 40 % sin ser simplemente "no aprovechar el 100 %":
- el video tiene **tasa variable** (VBR): entre fotogramas clave transmite mucho, entre ellos poco;
- los **ACK** de TCP van en sentido contrario y también ocupan el enlace (aunque en general el upload es menor);
- las **cabeceras** de cada paquete;
- si hay otros usuarios en el mismo enlace, compiten.

</details>

**7.** ¿Qué es el jitter de un enlace de 20 Mbps? ¿Puede ser 20 Mbps?

<details><summary>Respuesta</summary>

No, **nunca**, y el error está en las unidades.

El **jitter** es una medida de **variación temporal**, así que su unidad es de **tiempo**: milisegundos, microsegundos. Un jitter de 20 Mbps es dimensionalmente imposible.

Lo que sí puede ser 20 es el ancho de banda del enlace (bps) o la **variación del throughput** en el tiempo (por ejemplo, que la velocidad baje de 20 a 8 Mbps), pero eso ya no se llama jitter: se llama **variación de ancho de banda** o **fairness**, y se mide mal en redes de acceso.

Si el enunciado de un examen te da "jitter" con unidades de bits por segundo, es un error tipográfico del enunciado o estás confundiendo throughput con jitter.

</details>

**8.** Dime dos razones por las que la clasificación LAN/MAN/WAN **ya no** se puede hacer solo por la distancia.

<details><summary>Respuesta</summary>

**Razón 1 — La latencia no sigue a la distancia.** Un satélite geoestacionario está a 36.000 km y a 800 km un cable de cobre tiene **mayor** latencia que un enlace de fibra de 4 km. Y al revés: dos racks a 5 metros pueden estar unidos por un enlace de 400 Gbps a 50 µs, mientras que una conexión celular a 200 metros tiene 40 ms de latencia. **La distancia no predice la latencia**; el número de saltos intermedios y la tecnología del enlace sí.

**Razón 2 — La frontera es de propiedad, no de geografía.** Un *dark fiber* de operador dentro de una ciudad es una WAN con mejor desempeño que cualquier LAN. Y un PAN (Bluetooth, 10 m) tiene peor latencia que algunas WAN de fibra. Lo que define la frontera es **si el enlace es tuyo o de un tercero**, y eso es una decisión administrativa, no física.

Por eso la clasificación que se usa en la práctica es por **latencia observada** (< 1 ms = LAN, 1-5 ms = MAN, > 5 ms = WAN) y por **propiedad**.

</details>

## 🔗 Referencias

**Exámenes**
- Examen `sirc0612` (26-dic-2006) — P1 (5 pts): modelo OSI y las hipótesis de las 7 capas → **Clase 2**
- Examen `sirc0703` (26-feb-2007) — P1 (5 pts): el modelo TCP/IP → **Clase 2**
- Examen `sirc0902` (2-feb-2009) — P2 (10 pts): forwarding vs. routing y flooding → **Clase 3**
- Examen `sirc0912` (18-dic-2009) — P1 (10 pts): componentes del retardo, `B` vs. `s`, congestión → **Clase 5**
- Examen `sirc1103` (21-feb-2011) — P2 (6 pts): congestión, pérdidas y retardo → **Clase 5**
- Examen `sirc1103` — P5 (10 pts): retardo end-to-end con 3 enlaces y 2 conmutadores → **Clase 6**

**Bibliografía**
- Tanenbaum & Wetherall, *Redes de computadoras*, 5ª ed., **cap. 1** "¿Qué es una red?" (pág. ~1 a ~35 del PDF de tu carpeta) — es la fuente de la definición y de los parámetros
- Tanenbaum & Wetherall, **cap. 2** "La capa física" (pág. ~36 a ~75) — medios y moduladores, que se usan en la Clase 7
- Kurose & Ross, *Computer Networking: A Top-Down Approach* — los capítulos 1 y 2 tienen la misma distinción `bandwidth` vs. `propagation speed` y el `bandwidth-delay product`

**RFCs**
- `RFC 1122` — *Requirements for Internet Hosts: Communication Layers* (1989): define las capas de la pila TCP/IP **con enlace separado** (5 capas)
- `RFC 8200` — *Internet Protocol, Version 6 (IPv6) Specification* (2017, *Internet Standard*; obsoleta RFC 2460)
- `RFC 9293` — *Transmission Control Protocol* (2022, *Internet Standard*; consolida RFC 793)
- `RFC 7323` — *TCP Extensions for High Performance* (2014): *Window Scale* y *Timestamps*, que son lo que hace posible un BDP grande
- `RFC 9000` — *QUIC: A UDP-Based Multiplexed and Secure Transport* (2021): el ejemplo moderno de que una capa de transporte **no** tiene que ser TCP

**Clase siguiente:** 2 — Los modelos de capas: OSI y TCP/IP