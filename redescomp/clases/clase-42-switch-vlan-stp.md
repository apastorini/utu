# Clase 42 — Switch, hub, VLAN y STP

**Bloque:** E (Capa de Enlace) · **Semana:** 14 · **Duración estimada:** 110 min
**Correlativa:** Clase 41 (acceso al medio: ALOHA, CSMA/CD, CSMA/CA) · **Sigue con:** Clase 43 (redes inalámbricas 802.11)
**Material de referencia:** Tanenbaum cap. 3 (§3.4, 3.6 y 3.7) · IEEE 802.3 · IEEE 802.1D · IEEE 802.1Q · IEEE 802.1w

---

## 🎯 Al terminar esta clase vas a poder

1. Explicar por qué el **hub** produce **un solo dominio de colisión y un solo dominio de broadcast**, y por qué el switch parte el primero pero **no** el segundo.
2. Describir el mecanismo de **self-learning** y ejecutar el **algoritmo de reenvío completo, paso a paso**, llenando la tabla de reenvío después de cada trama.
3. Justificar por qué la tabla necesita **ageing**, y explicar por qué los **300 s son un default de fabricante y no un valor del estándar IEEE**.
4. Armar la tabla **hub vs. switch** completa (dominios, ancho de banda por puerto, duplex y **seguridad**) y sostener por qué un hub es un problema de seguridad, no solo de rendimiento.
5. Explicar qué es una **VLAN** y **por qué sirve**: aislar dominios de broadcast, mover un usuario sin tocar el cable, separar puertos de gestión.
6. Describir la **trama 802.1Q** campo por campo: **tag de 4 bytes**, **VLAN ID de 12 bits (1–4094)**, **C-TAG ()**, **S-TAG ()** y **PVID**; y por qué hace falta un puerto *tagged* y uno *untagged*.
7. Explicar por qué un **loop en capa 2 es una tormenta de broadcast** y por qué los bridges transparentes **no usan TTL**, y ejecutar el algoritmo de **STP**: raíz, puerto raíz, puertos designados y bloqueados.
8. Resolver completo el **Examen 2010-12 P3** (8 pts), el **2008-12 P2** (5 pts) y el **2009-03 P3** (6 pts).

> **Prerequisito del examen:**  (8 pts — hub vs. switch, dominios de colisión y de broadcast, y self-learning: **el corazón de esta clase**) ·  (5 pts — mejoras de performance y seguridad al pasar de hubs a switches) ·  (6 pts — concepto de VLAN 802.1Q y su utilidad).

Los tres aparecen juntos en el mismo bloque del syllabus: **conmutación, segmentación lógica y control de loops**. Esta clase es la bisagra entre la 41 (que habla de colisiones) y la 43 (un medio donde las colisiones no se pueden detectar).

> Esta clase **no repite** ALOHA ni CSMA/CD: ya están en la 41. Acá el medio **ya no es compartido**, así que el problema dejó de ser "quién puede hablar" y pasó a ser "**a quién le hablo**".

---

# PARTE 1 — TEORÍA

## 1.1 El hub: la red que repite (y por eso es una sola red)

Un **hub** es un dispositivo de **capa 1**. No lee direcciones, no decide nada, no tiene memoria: toma la señal eléctrica que entra por un puerto y la **regenera y copia a todos los demás puertos**.

`
 Lo que hace un HUB con la trama que entra por el puerto 3

 ┌───────────────┐
 H3 ───────────►│ │
 (trama de A │ HUB │──────► H1 (no le interesa)
 para B) │ "repite a │──────► H2 (no le importa)
 │ todos" │──────► H4 (no le importa)
 H5 ───────────►│ │──────► H5 (¡ERA PARA EL!)
 └───────────────┘──────► H6 (no le importa)
`

De esa definición sale **todo** lo que el hub es, sin ningún cálculo:

| Consecuencia | Por qué |
|---|---|
| **Un solo dominio de colisión** | todas las señales comparten **el mismo medio eléctrico**. Si H1 y H5 transmiten a la vez, las señales se suman y se destruyen |
| **Un solo dominio de broadcast** | una trama de broadcast se copia a **todos** los puertos, y cada estación copiada la vuelve a copiar a todos los puertos de su hub. Nada la detiene |
| **Sin ancho de banda por puerto** | el ancho de banda es **del medio compartido** y se reparte:  estaciones a  Mbps tienen  Mbps cada una |
| **Half-duplex obligatorio** | un solo medio común: si el puerto escucha lo que él mismo puso, oye su propia señal |
| **Cero seguridad** | todo lo que pasa por el medio es visible en **todos** los puertos, siempre |

> **La frase que hay que saber de memoria:** el hub no es un dispositivo de red con funciones reducidas; es **un pedazo de cable con corriente**. Todo lo demás se deduce de eso.

`
 CON HUB -- 1 dominio de colisión, 1 dominio de broadcast
 [H1]──┐ ┌──► H1
 [H2]──┼──► HUB ════════╤═══ ┼──► H2 las tramas de UNICAST también
 [H3]──┘ │ └──► H3 salen por todos: se desperdicia
 [H4]────────────────────┘ ╲ ancho de banda
 ╱ ╲

 CON SWITCH -- N dominios de colisión, 1 dominio de broadcast
 [H1]──┐ ┌──► H1 colisión propia y sola
 [H2]──┼──► SWITCH ════┬═══ ┼──► H2
 [H3]──┘ │ └──► H3
 [H4]───────────────────┘ ╲ ╱
 (el switch REENVÍA LA TRAMA UNA SOLA VEZ, al puerto
 donde está el destino. Solo el broadcast sale por
 todos: no puede descartarse porque por definición
 todos tienen que oírla)
`

## 1.2 El bridge y el switch

El **bridge** (*puente*) nació para unir **LANs** (grupos de estaciones que comparten un medio), no puertos. La diferencia con el hub es conceptual: **mira la trama y decide**, y tiene exactamente **dos verbos**: reenviar a un puerto concreto (*unicast forwarding*), o reenviar a todos los puertos (*flooding*).

`
 El BRIDGE y sus dos verbos
 ┌────────────┐
 │ Bridge │ "Cuando llega una trama por el puerto X:
 │ tabla de │ 1. APRENDO de dónde vino (memoria)
 │ reenvío │ 2. DECIDO a dónde va (regla)"
 └────────────┘
 ┌──────────────┬───────────┐
 │ MAC destino │ puerto │ ¿De dónde sale la tabla? De la
 ├──────────────┼───────────┤ observación de que toda trama que
 │ 00:1A:...:01 │ 3 │ entra por un puerto viene de la
 │ 00:1A:...:07 │ 5 │ estación conectada a ese puerto.
 └──────────────┴───────────┘ No es configuración: es memoria.

 Filtrado explícito: llega por el puerto 5 una trama de A (destino B),
 y la tabla dice B -> 3
 caso 1: entrada (B, 3) existe -> reenviar por el puerto 3 [1 copia]
 caso 2: entrada (B, 5) existe -> DESCARTAR [0 copias]
 caso 3: no existe entrada (B) -> FLOODING por 1,2,3,4,6 [5 copias]
 El caso 2 es lo que un hub NO puede hacer, y es toda la diferencia
 entre "repetir" y "conmutar".
`

Un **switch** es, estructuralmente, **un bridge con muchos puertos y una matriz de conmutación (*switching fabric*) interna**. La familia 802.3 no distingue: un switch **es** un bridge multipuerto.

`
 Anatomía de un switch
 ┌──────────────────────────────────────────────┐
 │ MATRIZ DE CONMUTACIÓN (switching fabric) │
 │ sin cuello de botella: mucho más rápida │
 │ que los puertos │
 └──┬────────┬────────┬────────┬────────┬────────┘
 │ │ │ │ │
 ┌──┴──┐ ┌──┴──┐ ┌──┴──┐ ┌──┴──┐ ┌──┴──┐
 │puerto│ │puerto│ │puerto│ │puerto│ │puerto│ cada uno con
 │ 1 │ │ 2 │ │ 3 │ │ 4 │ │ 5 │ su buffer
 └─────┘ └─────┘ └─────┘ └─────┘ └─────┘
 │ │ │ │ │
 H1 H2 H3 H4 H5
 ┌────────────────────────────────────────────────────────┐
 │ MAC address table (CAM table) — UNA por VLAN │
 │ 00:1A:2B:3C:4D:01 -> puerto 1 ageing 287 s │
 │ 00:1A:2B:3C:4D:05 -> puerto 5 ageing 12 s │
 └────────────────────────────────────────────────────────┘
`

Tres consecuencias, y las tres salen en el examen:

- **La matriz es mucho más rápida que los puertos.** Por eso **varias comunicaciones pueden ocurrir simultáneamente**: mientras el puerto 1 transmite hacia el 2, el puerto 3 transmite hacia el 4. En un hub es imposible: hay un solo medio.
- **Cada puerto tiene su propio buffer**, así que una ráfaga hacia un destino lento **no bloquea** los otros puertos.
- **Cada puerto es un dominio de colisión independiente** y puede trabajar en **full duplex**. En full duplex **la colisión es físicamente imposible**: no hay medio compartido que la genere.

> **Ojo con el exametero.** La frase "el switch no evita colisiones" es **falsa** y es el error conceptual más repetido del tema. Lo que el switch hace es **eliminar el medio compartido**; como no hay medio compartido, **no hay dónde colisionar**. Mismo resultado, causa distinta.

## 1.3 Self-learning: el algoritmo de reenvío completo

Acá está el corazón de la clase y lo que pide el **Examen 2010-12 P3c**.

> El switch aprende **la dirección MAC origen** de cada trama que entra, y la asocia al **puerto por el que entró**. Todo lo demás —qué hacer con esa trama— es **inferencia**.

**¿Por qué el origen y no el destino?** Porque el origen es **información verificada**: la estación conectada al puerto 3 es, necesariamente, la que puso esa MAC en el campo origen. El destino es lo que **quien manda** quiere que creamos; cualquiera puede poner una MAC cualquiera ahí. Si el switch aprendiera del destino, un solo nodo malicioso poisoning la tabla entera.

**¿Por qué "inferencia"?** Porque cuando el switch **no** encuentra la dirección destino no puede saber a qué puerto va. Lo único razonable es mandarla a **todos menos por el que entró**: devolvérsela al remitente sería entregarle una copia que ya posee. Esa es la definición operativa de **flooding**.

`
 Llega una trama por el PUERTO X, con MAC ORIGEN A y MAC DESTINO B.

 ┌───────────────────────────────────────────────────────────────────┐
 │ PASO 1 APRENDER (siempre, sin condiciones) │
 │ tabla[A] ← X ; temporizador(A) ← ahora │
 ├───────────────────────────────────────────────────────────────────┤
 │ PASO 2 BUSCAR el destino B │
 │ 2.a tabla[B] = Y y Y ≠ X -> reenviar por Y [unicast] │
 │ 2.b tabla[B] = Y y Y = X -> DESCARTAR [filtrado] │
 │ 2.c NO existe tabla[B] -> FLOODING por todos menos X │
 │ 2.d B es broadcast/multicast -> es el caso 2.c: el broadcast │
 │ (FF:FF:FF:.., 01:00:5E:..) nunca está en la tabla, así que │
 │ SIEMPRE inunda. │
 └───────────────────────────────────────────────────────────────────┘
 ⚠️ El orden importa: PRIMERO se aprende el origen, DESPUÉS se decide
 el destino.

 Pseudocode exacto (esto es lo que se escribe en el examen):

 para cada trama que llega por el puerto X:
 A = MAC_ORIGEN(trama) B = MAC_DESTINO(trama)
 tabla[A] = (puerto = X, temporizador = ahora)
 si B es broadcast o multicast:
 para cada puerto P != X: reenviar(trama, P)
 sino si existe tabla[B] con puerto Y:
 si Y != X: reenviar(trama, Y) // UNICAST
 sino: descartar(trama) // era para esta misma LAN
 sino:
 para cada puerto P != X: reenviar(trama, P) // FLOODING

 Regla de implementación: cuando una trama es FILTRADA, no se refresca
 el temporizador de la entrada destino. Solo el paso 1 mantiene viva la
 tabla.

 ¿Por qué el flooding va por todos menos X?
 La trama llegó por X: su emisor ya la tiene y ya la oyó pasar.
 Peor: si X es un hub, la trama vuelve al switch por otro puerto y el
 switch cree que es nueva. Es el mecanismo por el que un solo hub mal
 conectado genera un bucle de reenvíos incluso sin STP.
`

## 1.4 La tabla de ageing

Una tabla que solo **crece** es una tabla que **se rompe**. El ageing es el olvido programado: sin él, una estación que se muda de puerto deja de ser alcanzable (el switch sigue mandándole al puerto viejo) hasta que **ella misma** mande algo por el nuevo. Eso se llama un *agujero negro* (*black hole*).

`
 Aging MUY CORTO (60 s)
 + la tabla se mantiene chica, un nodo muerto se olvida rápido
 - si la estación transmite cada 100 s, su entrada se borra y el
 próximo mensaje se INUNDA a toda la red

 Aging MUY LARGO (1800 s)
 + pocas entradas se borran por error -> pocas inundaciones
 - la tabla crece, y si alguien mueve máquinas en un patch panel las
 entradas viejas siguen ahí durante 30 minutos

 300 s sale de estimar que una estación de trabajo normal habla al menos
 una vez cada pocos minutos.
`

> **Los 300 s NO son un valor del estándar IEEE.** Son el **default de fabricante** de prácticamente todos los switches comerciales, y es **configurable** (típicamente entre 60 s y 1800 s, y en muchos equipos por VLAN). Decir "el estándar IEEE dice 300 s" es un error; decir "**típicamente 300 s, configurable, default del fabricante**" es lo que se evalúa.

Además, muchos switches tienen **entradas dinámicas** (aprendidas, con temporizador) y **entradas estáticas** (configuradas a mano, que **no expiran nunca**). Una entrada estática mal puesta es un problema de disponibilidad: si asignás la MAC de alguien a un puerto viejo y esa persona se muda, **queda sin red** hasta que alguien corrija la configuración.

## 1.5 Hub vs. switch: la tabla que hay que saber de memoria

Cada fila tiene una causa, no una descripción suelta.

`
 ┌───────────────────────┬──────────────────┬────────────────────────┐
 │ Característica │ HUB │ SWITCH │
 ├───────────────────────┼──────────────────┼────────────────────────┤
 │ Capa OSI que opera │ 1 │ 2 │
 │ Lee la MAC │ NO │ SÍ │
 │ Dominio de colisión │ UNO │ UNO POR PUERTO │
 │ Dominio de broadcast │ UNO │ UNO (salvo VLANs) │
 │ Puertos que salen │ TODOS, siempre │ solo el del destino │
 │ Ancho de banda │ V/N por estación│ V por puerto, a V c/u │
 │ Full duplex │ NO │ SÍ │
 │ Colisiones │ SÍ │ NO (en full duplex) │
 │ Coste por byte útil │ BAJO │ ALTO (se replica) │
 │ Latencia │ ~0 (es cable) │ del orden de µs │
 │ Filtrado │ NO │ SÍ │
 │ SEGURIDAD │ NINGUNA │ el tráfico NO se ve │
 │ SNMP / gestión │ mínimo │ completa │
 └───────────────────────┴──────────────────┴────────────────────────┘
`

**La fila de seguridad merece un párrafo propio.** En un hub la seguridad es literalmente cero: el medio es compartido, así que **cualquiera puede poner un sniffer en cualquier puerto y ver todo el tráfico** (contraseñas en texto claro, claves de WEP/WPA-PSK, cabeceras de las peticiones de sesión).

Con un switch, en régimen, cada trama sale **por un solo puerto**: el del destino. Un atacante en el puerto 3 ve su propio tráfico pero **no** el de la estación del puerto 5. Eso es un salto real.

**Pero — y esto es lo que dice la solución oficial del 2008-12 y hay que repetir — el switch tiene una ventana insecure:**

> **Durante la fase de aprendizaje el switch se comporta exactamente como un hub.** Está inundando tramas para averiguar quién está en qué puerto, y durante esa ventana **un atacante ve todo**.

Y hay un segundo límite, más sutil: si un atacante **inunda la tabla con miles de MAC origen falsas** (*MAC flooding*), el switch agota su memoria de reenvío y **vuelve a inundar por todo**, degradado a hub. ⇒ **El switch no es un mecanismo de autenticación; es, como mucho, un mecanismo de contención del daño.**

## 1.6 VLAN: por qué la red conmutada todavía no alcanza

Después de poner switches queda un problema: una trama de **broadcast** (o de **unicast a un destino desconocido**) sale por **todos** los puertos, así que **el flooding no tiene fronteras**. Consecuencias: con 300 PC, cada broadcast genera 300 copias y cientos de respuestas (ARP, DHCP, mDNS); los servidores de producción reciben tramas que no son para ellos; y un problema en un puerto de un laboratorio inunda la red entera.

Esas dos consecuencias son **la misma causa**, y es justamente lo que rompe la seguridad (§1.5). Por eso el switch no alcanza para segmentar.

Una **VLAN** (*Virtual LAN*, LAN virtual) es **una partición lógica del switch**: un mismo switch físico se comporta como **varios switches independientes**, uno por VLAN.

`
 UN switch, TRES VLANs
 ┌───────────────────────────────────────────────────────────────┐
 │ SWITCH (un solo equipo) │
 │ VLAN 10 (LAB) VLAN 20 (PROD) VLAN 99 (GESTIÓN) │
 │ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ │
 │ │ p1 p2 p3 p4 │ │ p5 p6 p7 │ │ p24 (trunk) │ │
 │ └──────┬──────┘ └──────┬──────┘ └──────┬──────┘ │
 └──────────┼───────────────────┼──────────────────┼────────────┘
 │ │ │
 [H1] [H2] [H3] [H4] [S1] [S2] [consola admin]

 El flooding de una trama de H1:
 ✗ NO sale por p5, p6, p7 (son otra VLAN)
 ✓ sale solo por p2, p3, p4
 El dominio de broadcast se PARTIÓ: ahora hay 3, uno por VLAN.
`

### Las cuatro utilidades, con su porqué

| Utilidad | Explicación |
|---|---|
| **1. Partir el dominio de broadcast** | el flooding se confina a los puertos de la VLAN. Una VLAN lógica puede vivir en un switch con cableado físico |
| **2. Seguridad** | si un usuario de la VLAN 10 pone un sniffer en su puerto, **no ve nada de la VLAN 20**. Es el mismo argumento del switch, pero por encima del switch |
| **3. Mover un usuario sin mover el cable** | la VLAN a la que pertenece el usuario se decide **en el switch**. Si se muda de escritorio, el switch no cambia: cambia **una línea de configuración** |
| **4. Separar puertos de gestión** | las VLAN de gestión (o de voz) separan el tráfico de administración del de datos, de modo que **inundar la VLAN de gestión no lleva a todos los puertos** |

**El punto 3 es el más olvidado y el más usado.** La razón histórica de las VLAN es administrativa: antes, mover a alguien de oficina significaba repatchear cables. Con VLAN, **es configuración**.

### 802.1Q: la trama etiquetada, campo por campo

Si todas las tramas de una VLAN viajan por el mismo puerto, el switch **no necesita poner nada en la trama**. El problema aparece cuando la trama tiene que **atravesar varios switches**: el switch intermedio necesita saber a qué VLAN pertenece. Solución: **un tag de 4 bytes**.

`
 TRAMA NORMAL (sin VLAN) TRAMA 802.1Q (etiquetada)
 ┌────────┬────────┬──────┬──────┬─────┐ ┌────────┬────────┬──────┐
 │ MAC │ MAC │ Ether│ │ FCS │ │ MAC │ MAC │Ether │ T │PCP│
 │ destino│ origen │ type │datos │ 4 B │ │ destino│ origen │type │ A │ │
 │ 6 B │ 6 B │ 2 B │ │ │ │ 6 B │ 6 B │ 2 B │ G │ │
 └────────┴────────┴──────┴──────┴─────┘ └────────┴────────┴──────┘
 │ │ │
 EtherType = 0x0800 (IPv4) │ │ └─ VID: 12 bits (1..4094)
 EtherType = 0x86DD (IPv6) │ └─────── PCP: 3 bits, prioridad
 EtherType = 0x0806 (ARP) └────────────── TCI = 2 bytes
 (16 bits: 3 PCP + 12 VID + 1 CFI)
 tag = 4 bytes (TCI + Ethertype 0x8100)

 ┌───────────────┬──────────────────────────────────────┬─────────┐
 │ TCI (2 B) │ │ TCI (2 B)│
 ├───────┬───────┬───────────────┬──────────────────────┤ │
 │ PCP │ DEI │ VID │ VID │ │
 │ 3 bit │1 bit │ 12 bits │ 12 bits │ │
 └───────┴───────┴───────────────┴──────────────────────┴─────────┘
 │ │ │
 │ │ └── 4094 valores: 1..4094 ; 0 = "sin tag"
 │ └── DEI: indicador de "drop eligible" (usado por TSN)
 └────────── PCP: 0 = Best Effort ... 7 = Voice
`

**El detalle fino que casi nadie menciona:** el tag de 4 bytes es **TPID (2 bytes) + TCI (2 bytes)**. El `Ethertype` original (0x0800, 0x86DD…) **no desaparece**: pasa a ocupar el lugar que tenía el tag. Por eso el campo "Tipo" de una trama con tag es `0x8100`, no `0x0800`.

### C-TAG vs. S-TAG

| Etiqueta |  | Quién la usa | Dónde aparece |
|---|---|---|---|
| **C-TAG** | **** | el **cliente** de la VLAN (la empresa) | primera etiqueta de la trama |
| **S-TAG** | **** | el **proveedor** del servicio (el carrier) | etiqueta **exterior**, que el carrier pone **encima** |

**¿Por qué dos?** Porque en *carrier Ethernet* hay **dos operadores de VLAN en el mismo cable**: el carrier (que agrupa a muchos clientes) y el cliente (que agrupa a sus VLANs). Si ambas usaran  no se sabría cuál termina primero.

`
 Trama con DOBLE etiquetado (carrier Ethernet)
 ┌────────┬────────┬────────┬────────┬────────┬────────┬──────┐
 │ MAC dst│ MAC src│ 88A8 │ VID= │ 8100 │ VID= │0800 │ datos
 │ │ │ (S-TAG)│ 100 │ (C-TAG)│ 10 │ │
 └────────┴────────┴────────┴────────┴────────┴────────┴──────┘
 ▲ ▲
 │ └── el cliente puso VLAN 10
 └── el CARRIER puso VLAN 100
 El carrier ve y cobra por la 100. El cliente ve y cobra por la 10.
`

### PVID, tagged y untagged: por qué un puerto tiene que ser de las dos cosas

Si **todo** lleva tag, las máquinas que no saben de VLANs (una PC, una impresora, una cámara IP) no pueden entender la trama. Y si **nada** lleva tag, el switch intermedio no sabe a qué VLAN pertenece.

`
 ┌─────────────────────────────────────────────────────────────────┐
 │ PUERTO "ACCESS" (untagged, de usuario final) │
 │ ├─ sale SIN tag │
 │ ├─ el switch le ASIGNA un solo VLAN ID: el PVID │
 │ └─ el usuario nunca ve un tag: su tarjeta no lo pondría │
 │ │
 │ PUERTO "TRUNK" (tagged, entre switches o hacia el router) │
 │ ├─ sale CON tag (0x8100) para todas las VLANs que lo usa │
 │ ├─ el switch NO pone nada a mano: el VLAN ID viaja en la trama │
 │ └─ es lo que permite "router-on-a-stick" │
 └─────────────────────────────────────────────────────────────────┘

 PVID = Port VLAN ID: el VLAN ID que se ASIGNA a las tramas que
 llegan a ese puerto SIN tag.

 Ejemplo: la trama de H1 (VLAN 10)
 H1 ──► [p1, access, PVID=10] ──► [p24, trunk] ──► [router]
 (1) H1 manda SIN tag: es una PC normal, no sabe qué es una VLAN.
 (2) Entra por p1. El switch ve "sin tag, PVID de p1 = 10" y le
 ADJUNTA el tag: [ .. | 8100 | VID=10 | 0800 | IP .. ]
 (3) Sale por p24 (trunk): conserva el tag.
 (4) El router separa por VLAN: 0.10 -> 192.168.10.1/24, 0.20 ->
 192.168.20.1/24. ACÁ termina el dominio de broadcast, porque el
 router NO reenvía broadcast entre interfaces.
 (5) Si el vecino del trunk no tiene esa VLAN en su tabla, se descarta.
`

### Los números del tag

`
 Sin tag : mínimo 64 B máximo 1518 B
 C-TAG : mínimo 68 B máximo 1522 B (+4)
 S+C-TAG : mínimo 72 B máximo 1526 B (+8)

 ⚠️ EL MTU NO CAMBIA: sigue siendo 1500 bytes de payload IP.
 Los 4 bytes salen del relleno (padding) de la trama mínima.
 Proof: 1522 − 18 (cabecera) − 4 (tag) = 1500 bytes de payload.
`

## 1.7 STP y RSTP: por qué la capa 2 necesita un protocolo de control de loops

### El problema: un loop en capa 2 no se muere solo

En IP, un paquete que entra en un lazo **muere**: cada router descuenta el **TTL** y cuando llega a 0 lo descarta. Ese contador es la red de seguridad de la capa 3.

**Los bridges transparentes no tienen nada de eso.** Son *transparentes*: su trabajo es que la red se comporte como si no existieran, así que no pueden tocar nada de la trama. En particular **no decrementan ningún TTL**, porque la trama Ethernet **ni siquiera tiene campo TTL**.

`
 CON UN LOOP EN CAPA 2 (S1 y S2 unidos por DOS enlaces)

 H1
 │
 ┌─┴─┐
 │ │
 [S1]══════════════[S2] dos enlaces entre S1 y S2 (puede
 │ ╲ ╱ │ ser un cable y un puerto del otro switch)
 │ ╲════════╱ │
 [S3]─────────────┘

 H1 manda UNA trama de BROADCAST.
 t0: S1 la recibe por p1 y la reenvía por TODOS los demás puertos.
 t1: S2 la recibe. NO tiene entrada para su origen (es la PRIMERA vez
 que la ve) -> FLOODING por todos sus puertos.
 t2: Vuelve a S1 por OTRO puerto. S1 tampoco la descarta: es la
 entrada de ageing del ORIGEN, y ese origen no es la dirección
 de DESTINO (que es broadcast), así que S1 no la reconoce
 -> la reenvía por todos los puertos menos por donde entró.
 t3: ... y así indefinidamente. La trama NUNCA muere.
`

Lo que mata a la red no es que una trama circule: es que **el número de copias crece** mientras los enlaces se saturan. En régimen permanente cada puerto está al 100 %, los buffers están llenos, la CPU está al 100 % procesando tramas que descarta, y **el switch deja de responder a ping**. Los síntomas característicos: la red entera se cae en el momento en que alguien enchufa un segundo cable entre dos switches, y las tablas MAC **parpadean** (cada MAC aparece en dos o más puertos a la vez, *MAC flapping*).

> **El punto conceptual que se pregunta:** un router **descarta** el paquete porque su TTL llegó a 0. Un bridge **no puede**, porque **no sabe si la trama es "la misma" que ya vio antes**. El spanning tree no evita los loops: **los calcula y les pone una puerta**, de modo que la topología lógica sea un **árbol**, que por definición no tiene bucles.

### Los estados de un puerto

`
 ┌──────────┐
 │ DISABLED │ (administrativamente apagado, o falla el enlace)
 └────┬─────┘
 v
 ┌──────────┐
 ┌──────────►│ BLOCKING │ Recibe BPDUs, NO envía. Es el estado "normal"
 │ └────┬─────┘ de los puertos que NO participan en el árbol.
 │ expira el Procesa tramas de 802.1D. ESTADO SEGURO: ni
 │ temporizador MaxAge escucha datos ni transmite datos.
 │ v
 │ ┌───────────┐
 ├───────────┤ LISTENING │ Cambió la topología. Sigue ENVIANDO BPDUs,
 │ 15 s de └─────┬─────┘ pero YA NO procesa ni reenvía tramas de
 │ Forward Delay datos. Sigue siendo seguro. 15 s más
 │ v
 │ ┌───────────┐
 ├───────────┤ LEARNING │ YA PASA AL AGUA: empieza a llenar la tabla
 │ 15 s └─────┬─────┘ MAC con las tramas que ve, pero AÚN NO
 │ más │ reenvía ninguna.
 │ v
 │ ┌───────────┐
 └───────────┤ FORWARDING│ Estado normal de un puerto que SÍ está en
 └───────────┘ el árbol: envía y recibe datos.

 ⏱️ Temporizadores del STP clásico (802.1D) en sus defaults:
 Hello 2 s (cada cuánto se manda un BPDU)
 Max Age 20 s (sin oír BPDUs => el vecino "murió")
 Forward Delay 15 s (dos veces: Listening->Learning y
 Learning->Forwarding)
`

**El tiempo total de convergencia del STP clásico es de ~30 a 50 segundos**, y esa es la razón por la que **nadie usa STP hoy**: un enlace que se cae y vuelve deja la red parada medio minuto. **RSTP** lo comprime a **sub-segundo** (§1.8).

### Bridge ID: cómo se decide quién manda

`
 BRIDGE ID = 64 bits

 ┌────────────┬────────────────────────────────────────┐
 │ PRIORIDAD │ MAC ADDRESS │
 │ 16 bits │ 48 bits │
 │ (4096 c/u) │ (la MAC de una de sus interfaces) │
 └────────────┴────────────────────────────────────────┘
 32768 = prioridad BASE (el default de 802.1D)
 24576, 16384, 8192, 4096 = los valores "nominales" que se usan para
 forzar que un bridge sea la raíz.
 ⚠️ Tiene que ser múltiplo de 4096. Si ponés 1000, el switch lo ajusta
 a 0, que es el valor más bajo posible: ¡GANA!

 PRIORIDAD BASE = 32768 -> en hexadecimal = 0x8000

 S1: prioridad 32768 (0x8000), MAC 00:00:00:00:00:01 -> 8000.0000.0000.0001
 S2: prioridad 32768 (0x8000), MAC 00:00:00:00:00:02 -> 8000.0000.0000.0002
 S3: prioridad 4096 (0x1000), MAC 00:00:00:00:00:03 -> 1000.0000.0000.0003 <-- RAÍZ
`

**La comparación es numérica, de izquierda a derecha**: primero la prioridad, después la MAC. Por eso para cambiar la raíz **no alcanza con la prioridad**: si dos switches tienen la misma, gana el que tenga la MAC más chica, y eso depende de la marca de la placa, no de vos.

### El algoritmo completo

`
 1. Cada bridge manda BPDUs (Bridge Protocol Data Units) por TODOS sus
 puertos, cada 2 segundos, a la dirección de multicast 01:80:C2:00:00:00.
 Un BPDU lleva: Bridge ID, costo de cada puerto, prioridad de puerto
 y Max Age.

 2. ELECCIÓN DE LA RAÍZ.
 Cada bridge escucha los BPDUs. Si oye un Bridge ID MENOR que el suyo,
 sabe que no es la raíz.
 -> La raíz es el bridge con el Bridge ID más bajo de toda la red.
 No hay votación: es un mínimo.

 3. PUERTO RAÍZ (root port) en cada bridge no-raíz.
 Para cada puerto se calcula el camino a la raíz. Gana el de:
 (a) menor COSTO hasta la raíz
 (b) si hay empate, el que recibió el BPDU con menor Bridge ID
 (c) si hay empate, el de menor ID de puerto emisor
 Ese es el ÚNICO puerto por el que el bridge habla con el resto.

 4. PUERTOS DESIGNADOS en cada segmento.
 En cada LAN (cada enlace entre dos bridges) compiten los bridges
 conectados. Gana el de MENOR Bridge ID: su puerto queda DESIGNATED y
 es el único autorizado a enviar datos hacia ese segmento.

 5. EL ÁRBOL.
 - puertos RAÍZ y DESIGNADOS -> FORWARDING
 - todos los demás -> BLOCKING

 6. El grafo resultante es un ÁRBOL: de cualquier LAN a cualquier otra
 hay EXACTAMENTE UN camino. No puede haber bucle.
`

`
 Topología FÍSICA (con un loop) Topología LÓGICA (el árbol)
 ┌──────┐ ┌──────┐
 │ S1 ├═══════╤═══════╤═══════════►│ S1 │ raíz
 └───┬──┘ │ │ └───┬──┘
 │ ┌───┴───┐ │ │ p1 RAÍZ
 ┌───┴──┐ │ S3 │ │ ┌───┴──┐
 │ S2 ├───┤ ├───┤ │ S2 │
 └───┬──┘ └───┬───┘ │ └───┬──┘
 │ │ │ │ p1 DESIGNATED
 ┌───┴──┐ ┌───┴──┐ │ ┌───┴──┐
 │ S3 │ │ S4 │ │ │ S3 │
 └──────┘ └──────┘ │ └──────┘
 p2 -> BLOCKING
 4 switches, 5 enlaces: el loop ya no existe lógicamente
`

## 1.8 ⚠️ Actualización a 2026

**Sigue igual — de memoria, sin dudar:**
- **Formato de trama**: preámbulo 7 + SFD 1, **MAC destino 6 + MAC origen 6**,  2, payload, **FCS 4**. **MTU 1500**.
- **ARP ()**: request en **broadcast**, reply en **unicast**. El *gratuitous ARP* sigue usándose (anuncio, DHCP, failover de gateway, VRRP) y sigue siendo **fuente clásica de ARP spoofing y cache poisoning**.
- **MAC learning**: aprende la **MAC origen** y asocia puerto; **flooding** si el destino es desconocido; **unicast** si se conoce; **filtrado** si el destino está en el mismo puerto de entrada.
- **802.1Q**: tag de 4 bytes, **VLAN ID de 12 bits (1–4094)**,  = sin tag (PVID).
- **STP/RSTP** y sus estados (Blocking, Listening, Learning, Forwarding), Bridge ID con **prioridad base 32768**.
- **Loops en capa 2 = tormenta de broadcast**: sigue siendo la razón de ser del spanning tree.

**Cambió o se modificó — y acá hay que ser preciso:**

1. **El half-duplex Ethernet es historia por encima de 1 Gb/s.** Y hay un doble error que circula:
 - Es una decisión de **IEEE 802.3**, **no una RFC de IETF**. **No existe ninguna RFC que lo depreque.** La que circula como tal, **, es JSCalendar**, y no tiene nada que ver con Ethernet.
 - A 10GbE y por encima el **full duplex punto a punto es obligatorio** y el half-duplex no existe en la especificación de esas velocidades.
 - **PERO half-duplex no desapareció del todo:** **IEEE 802.3cg 10BASE-T1S** (*single-pair Ethernet*, para redes PLC industriales sobre un solo par) es **obligatoriamente half-duplex**, con un protocolo de acceso propio, **PLCA**. Y en IETF, el módulo YANG `csma-cd` de `802.3cf` está marcado `deprecated`. ⇒ **Saber cuándo CSMA/CD sigue existiendo es parte del tema.**

2. **** es el estándar actual (precedido por ): la revisión **2018** abrió el bloque de **TSN** con **** (tráfico programado), **** (preempción de trama, junto con ) y **** (filtrado y policing por stream); la revisión **2022** agregó **** (Stream Reservation Protocol) y **** (*asynchronous traffic shaping*). **Para el examen no cambia nada del tag ni de la VLAN**: cambia **para qué** se usan, porque las VLAN pasaron de ser segmentación de oficina a ser la base de la **red determinista**.

3. **LAG:  (2000) → .** La revisión vigente es ****. Un *Link Aggregation Group* une varios enlaces físicos en uno lógico, para más ancho de banda y redundancia. **No es lo mismo que un spanning tree**: es "usá los dos cables en paralelo", y no genera loops porque el switch decide el puerto por *hash*.

4. **C-TAG () vs. S-TAG ()**: el doble etiquetado pasó de exótico a **estándar en carrier Ethernet y en EVPN-VXLAN**. Y acá va una distinción que se confunde siempre: en el datacenter, **EVPN () sobre VXLAN ()** es el estándar de overlay, y ahí la distribución de VLANs **no la hace 802.1Q**: el tenant se identifica por el **VNI de 24 bits que viaja en el encabezado VXLAN sobre UDP/4789**, y el  queda solo por compatibilidad. **802.1Q etiqueta la trama; VXLAN encapsula y multiplica el MTU.** No son lo mismo.

5. ** () es el default real**, no el STP clásico: la convergencia va de sub-segundo a unos pocos segundos, en vez de los ~30–50 s del 802.1D.  () cuando querés **compartir el árbol entre varias VLANs** y así no tener un spanning tree por VLAN.

6. ⚠️ **El "aging de 300 s" de la tabla MAC es default de FABRICANTE, no un valor mandated por IEEE.** Escribí "típicamente 300 s en switches comerciales, configurable". **Nunca** "el estándar IEEE dice 300 s".

**Consecuencia para el examen:**
- *"¿CSMA/CD es necesario hoy?"* → **no, y ni siquiera existe por encima de 1 Gb/s** (salvo 10BASE-T1S industrial).
- *"¿qué protocolo evita los loops en capa 2?"* → **spanning tree**, y el **default real es RSTP (802.1w)**. Si el enunciado es de 2009/2010 y habla de "STP", respondé el mecanismo del árbol y **agregá una línea** de que hoy converge RSTP.
- *VLAN* → el tag de 4 bytes y el VID de 12 bits **no cambiaron**. Lo que cambió es la **revisión del estándar (802.1Q-2022)** y el doble etiquetado C-TAG/S-TAG.

---

# PARTE 2 — PRÁCTICA RESUELTA

## 2.1 Ejercicio 1 — Self-learning paso a paso con seis tramas

**Enunciado (inventado).** Un switch de 6 puertos tiene los hosts `H1..H6` en los puertos 1..6, con MAC `00:...:01` a `00:...:06`. La tabla arranca vacía. Llegan seis tramas, en orden.

`
 [H1]──p1──┐
 [H2]──p2──┤
 [H3]──p3──┼──► SWITCH A1 = 00:1A:00:00:00:01 (H1, puerto 1)
 [H4]──p4──┤ ... hasta A6 = ...:06 (H6, puerto 6)
 [H5]──p5──┤
 [H6]──p6──┘
 tabla = { } (estado inicial)

 Tramas: 1) p1, de A1 a BROADCAST
 2) p3, de A3 a A1
 3) p5, de A5 a A3
 4) p2, de A2 a A6
 5) p6, de A6 a A1
 6) p1, de A1 a A6
`

**Trama 1.** *Aprende* . *Decide*:  **nunca** está en la tabla ⇒ **flooding** por 2, 3, 4, 5, 6.
→ Es el momento en que la red "se siente como un hub": la primera trama SIEMPRE se inunda, porque el switch no sabe nada todavía.

**Trama 2.* *Aprende* `A → p1`. *Decide*: `B` está en `p3`, y `A ≠ p3` ⇒ **unicast por p3**.
→ Es la **primera** vez que el switch puede hacer unicast sin adivinar.

**Trama 3.* *Aprende* `A → p1`. *Decide*: `C` está en `p4`, `A ≠ p4` ⇒ **unicast por p4**.

**Trama 4.** *Aprende* . *Decide*:  **NO** está en la tabla ⇒ **flooding** por 1, 3, 4, 5, 6.

`
 ⚠️ ERROR CLÁSICO. Muchos escriben "A6 -> puerto X" al ver el flooding.
 NO: el flooding NO aprende nada. Lo único que se aprende en esta
 trama es que A2 está en el puerto 2. Y H6, que recibe la trama por
 el flooding, la descarta: nadie le avisa que la estaba esperando.
`

**Trama 5.** *Aprende*  (por fin habla la estación del puerto 6). *Decide*:  está en  ⇒ **unicast por p1**.

**Trama 6.** *Aprende*  **y refresca su temporizador de ageing**. *Decide*:  está en  ⇒ **unicast por p6**.

### Tabla de verificación

| Trama | Aprende | ¿Destino conocido? | Acción | Puertos de salida | Tabla resultante |
|---|---|---|---|---|---|
| 1 |  | broadcast (nunca) | **flooding** | 2,3,4,5,6 |  |
| 2 |  | sí () | **unicast** | 1 |  |
| 3 |  | sí () | **unicast** | 3 |  |
| 4 |  | **no** | **flooding** | 1,3,4,5,6 |  |
| 5 |  | sí () | **unicast** | 1 |  |
| 6 |  (refresca) | sí () | **unicast** | 6 | (igual) |

**Interpretación física:** de 6 tramas, **2 fueron flooding (10 copias)** y **4 unicast (4 copias)**: 14 copias sobre el medio, de las cuales **10 eran redundantes**. La eficiencia del switch **crece con el tiempo**: a medida que la tabla se puebla, el costo por trama baja de  copias a **una**. Y obsérvese que ** NO está en la tabla**: H4 nunca habló, así que el switch no tiene idea de que existe; si H4 mandara una trama, sería un flooding.

### El caso que falta en las seis tramas: el filtrado

`
 Trama 7: entra por p2, de A4 a A2.

 Paso 1: tabla[A4] <- p2
 Paso 2: B = A2. tabla[A2] = p2. Y = p2 = el puerto de entrada.
 -> Y == X -> DESCARTAR.

 Salida: NINGUN PUERTO. 0 copias.

 ¿Qué es esto físicamente? La trama venía por el mismo cable por el que
 el switch la enviaría. A2, que está en el mismo segmento, ya la oyó
 directamente en el medio. Reenviársela sería duplicarla sin motivo.
 Esto es el FILTRADO: exactamente lo que un hub no puede hacer.
`

### ⚠️ Errores típicos
- **Aprender del destino.** El switch aprende **solo** del origen. Escribir " porque hubo flooding" es el error más caro del ejercicio.
- **No mencionar el caso  → descartar.** El 2010-12 lo escribe como un "y" condicional dentro de un solo inciso; si lo desplegás aparte, sumás.
- **Reenviar el flooding también por el puerto de entrada.** No: por definición.
- **Tratar el broadcast como un caso aparte del "destino desconocido".** Es un caso *particular*: la dirección de broadcast jamás está en la tabla, así que siempre cae en la rama de inundar.
- **Olvidar el ageing.** Cada aprendizaje **refresca** el temporizador.

## 2.2 Ejercicio 2 — El ageing de la tabla

**Enunciado (inventado).** Un switch tiene ageing de 300 s. La estación E habla según un **proceso de Poisson** de tasa λ tramas por segundo. **(a)** ¿En qué instante se elimina su entrada? **(b)** ¿Probabilidad de que siga viva a los 300 s? **(c)** Con λ = 0,005 tramas/s (una cada 200 s), ¿probabilidad de que expire antes de la siguiente trama?

**(a) El instante de expiración.** El temporizador se pone en  (última vez que se vio el origen) y corre; la entrada se elimina cuando llega a 300 s.

`
 t=0 ─────────────────────────────── t=300 s
 │◄──────── 300 s de ageing ────────►│
 └── se ve A5, timer(A5) = 300 └── la entrada se BORRA
`

*Interpretación:* el switch **no hace una pasada de limpieza cada 300 s**: cada entrada tiene **su propio** temporizador, que se reinicia cada vez que se ve esa MAC. Si llega una trama de `A` en `p1`, la entrada se refresca y el reloj vuelve a cero.

**(b) Probabilidad de que la entrada sobreviva.** Sobrevive si y solo si en esos 300 s **no llega ninguna trama** de `A`. Con Poisson, `P = e^(−λT)`. Es la misma fórmula de ALOHA de la clase 41: **la misma matemática para dos cosas distintas** — allá medía tramas que sobrevivían a una colisión, acá entradas que sobreviven a un olvido.

**(c) Con  tramas/s.**

`
 λ = 0,005 tramas/s (una trama cada 1/0,005 = 200 s)
 Exponente: λ · 300 = 0,005 · 300 = 1,5

 e^(1,5) = e · e^(0,5) = 2,71828 × 1,64872 = 4,48169

 P(sobrevive) = e^(−1,5) = 1 / 4,48169 = 0,22313
 P(expira antes de la siguiente) = 1 − 0,22313 = 0,77687 ≈ 77,7 %
`

*Interpretación:* una estación que habla **una vez cada 200 s** tiene casi **4 de cada 5 veces** su entrada **borrada** cuando mande la siguiente trama. Es una consecuencia directa del criterio de diseño: **300 s de ageing para una estación que habla cada 200 s es un valor mal elegido**.

`
 λ (tramas/s) intervalo medio λ·300 P(expira) veredicto
 ───────────── ─────────────── ────── ────────── ─────────
 1 1 s 300 ~0 (e^-300) nunca molesta
 0,1 10 s 30 e^-30 ≈ 9e-14 nunca molesta
 0,01 100 s 3 1 − e^-3 = 0,950 molesta a veces
 0,005 200 s 1,5 0,777 molesta siempre
 0,001 1000 s 0,3 1 − e^-0,3 = 0,259 aceptable
 0,0002 5000 s 0,06 1 − e^-0,06=0,058 aceptable
`

*Interpretación física:* el umbral de "molesto" está alrededor de `M/2`, es decir, cuando la estación habla **una vez cada ~300 s o menos seguido**. Ahí la tabla se llena de entradas que mueren y renacen, y cada renacimiento cuesta **una inundación completa**.

**(d) Qué pasa en la red cuando la entrada expiró.**  manda su trama con destino `B`: la entrada de `B` ya no está, así que `B` es un **destino desconocido** ⇒ **flooding** por los puertos 1, 2, 3, 4, 6; los demás la reciben y la descartan; y el switch **aprende**  con 300 s de reloj. **El flooding es el precio de la incertidumbre, y se paga una sola vez por cada olvido.**

> **Consecuencia de diseño, y es la del Examen 2009-03 P3:** en una red con VLANs, ese flooding **queda confinado a los puertos de la VLAN**. Por eso el ageing no es una "pequeña pérdida de rendimiento", sino el detonante de la razón por la que la VLAN es una medida de **seguridad**: la fuga se produce, pero **no sale de la VLAN**.

## 2.3 Ejercicio 3 — Partir una VLAN y saber qué tags van por dónde

**Enunciado (inventado).** Un switch  de 24 puertos:

`
 VLAN 10 "PRODUCCIÓN" -> puertos 1 a 16 (access, untagged)
 VLAN 20 "OFICINAS" -> puertos 17 a 22 (access, untagged)
 VLAN 99 "GESTIÓN" -> puerto 23 (access, untagged)
 puerto 24 -> TRUNK, con las VLANs 10, 20 y 99
 PVID por defecto del puerto 24 = 10.

 Router R: 0.10 -> 192.168.10.1/24
 0.20 -> 192.168.20.1/24
 0.99 -> 192.168.99.1/24 (configuración "router-on-a-stick")
`

**(a) Trama de  (p1, VLAN 10) hacia  (p20), ambos access de la VLAN 10.**

`
 (1) P1 manda: [ Dst | Src | 0800 | IP ] SIN tag (una PC no sabe de VLANs)
 (2) Entra por p1 SIN tag. El switch aplica el PVID = 10 y ADJUNTA el tag:
 [ Dst | Src | 8100 | VID=10 | 0800 | IP ]
 (3) Sale por p20, que es access de VLAN 10: le QUITA el tag.
 P20 recibe una trama normal, sin saber que hubo VLAN.

 💡 Ambos puertos están en la MISMA VLAN, así que la comunicación
 FUNCIONA sin tocar el router. El switch no rutea: solo reenvía
 dentro de la VLAN.
`

**(b) La misma trama de  hacia un servidor en la VLAN 20.**

`
 P1 ─► [p1 access VLAN10] ─► [p24 trunk] ─► [R] ─► [p18 access VLAN20] ─► S1

 (1) P1 manda SIN tag. (2) p1 aplica PVID=10 -> tag VID=10.
 (3) p24 es trunk: el tag VIAJA intacto: la trama sale con VID=10.
 (4) El router recibe 8100/VID=10, la mete en la subinterfaz 0.10, le
 saca el tag y decide por IP que va a 192.168.20.x. Para eso hace
 un ROUTE y reinyecta por 0.20.
 (5) R emite por 0.20 CON el tag VID=20.
 (6) Entra por p18 (access, PVID=20): coincide, el switch le saca el
 tag y lo entrega a S1.

 ⚠️ La trama CAMBIÓ DE VLAN en el router. Eso es posible porque el
 ROUTER es de CAPA 3 y por lo tanto ACABA el dominio de broadcast. Sin
 router, P1 y S1 estarían en dominios distintos y no se hablarían jamás.
`

**(c) Una trama de BROADCAST de  (un ARP request).**

`
 (1) P1 manda: [ FF:FF:FF:FF:FF:FF | ... | 0800 | ARP request ]
 (2) p1 pone el tag VID=10.
 (3) El switch busca en la TABLA: el destino FF:FF:FF:FF:FF:FF NO está
 (jamás está) -> FLOODING.
 (4) Pero el flooding se hace DENTRO DE LA VLAN 10 solamente:
 sale por p2, p3, ..., p16 (los otros access de VLAN 10)
 sale por p24 (el trunk, con el tag)
 ✗ NO sale por p17..p22 (VLAN 20)
 ✗ NO sale por p23 (VLAN 99)
 (5) En el router: entra por 0.10 con destino broadcast. Un router NO
 reenvía broadcast entre interfaces -> no sale por 0.20 ni 0.99.
 (6) Vuelve por p24 un reply ARP unicast: se despeja el tag y sigue
 por la tabla como cualquier unicast.

 💡 ESO son "varios dominios de broadcast en una misma red switcheada".
`

**(d) Una trama que llega por el trunk p24 SIN tag, y una con tag VLAN 30.**

`
 SIN tag: el switch consulta el PVID del puerto 24 = 10, y la TRATA PASA
 A SER DE LA VLAN 10. ¿Por qué existe el PVID? Porque un trunk puede
 tener una "VLAN nativa" untagged, usada para un único VLAN: es típico
 del router-on-a-stick de un fabricante que tiene una IP en el trunk y
 subinterfaz en el resto.

 Con tag VLAN 30 (que el switch no conoce):
 El switch busca VLAN 30 en su tabla de VLANs. NO EXISTE.
 -> La trama se DESCARTA.
 💡 Es una medida de SEGURIDAD, no un accidente: un router mal
 configurado, o un atacante en la trunk, no puede inyectar tramas
 en VLANs que el switch no tiene configuradas.
`

**Los números, otra vez.**

`
 Sin tag : mínimo 64 B máximo 1518 B
 C-TAG : mínimo 68 B máximo 1522 B (+4)
 S+C-TAG : mínimo 72 B máximo 1526 B (+8)

 MTU de la carga IP: 1500 SIEMPRE, con tag o sin tag.
 Proof: una trama de 1522 B con tag tiene
 1522 − 18 (cabecera) − 4 (tag) = 1500 bytes de payload.
 Misma MTU: el tag se "comió" relleno, no payload.
`

### ⚠️ Errores típicos
- Creer que el switch **rutea** entre VLANs. **No**: sin router, la VLAN 10 y la VLAN 20 **no se hablan**, aunque estén en el mismo switch físico.
- Olvidar que el flooding **sí** se confina a la VLAN. Es el mecanismo real de la seguridad de VLAN, y es lo que dice la solución oficial del 2009-03.
- Decir "el PVID es el VLAN ID del trunk". No: el PVID es **por puerto**, e indica **qué VLAN se asume cuando llega una trama sin tag**.
- Confundir **access** con **untagged**: access es *untagged* **y pertenece a una sola VLAN**; trunk es *tagged* y puede llevar muchas.

## 2.4 Ejercicio 4 — Dibujar el árbol de STP y decidir qué puertos se bloquean

**Enunciado (inventado).** Tres switches full-duplex en triángulo, costos de enlace **iguales**:

`
 ┌─────────┐
 │ SW1 │ prioridad 32768, MAC 00:00:00:00:00:01
 └──┬───┬──┘
 │ │
 e1 │ │ e2
 ┌────┘ └────┐
 │ │
 ┌──┴──┐ ┌──┴──┐
 │ SW2 │ │ SW3 │
 └─────┘ └─────┘
 prio 32768 prio 32768
 MAC ...0002 MAC ...0003

 Enlaces: SW1-SW2 (e1), SW1-SW3 (e2), SW2-SW3 (e3). Costo: 100 c/u.
`

**Paso 1 — Bridge ID.** Las tres prioridades son iguales (32768 = valor por defecto), así que desempata la MAC: `00:11:22:33:44:55` es el menor.

**Paso 2 — Raíz.** Raíz = el Bridge ID **menor** ⇒ **SW1 es la raíz**.
*(Interpretación: como los tres tienen prioridad default, la raíz la decide la MAC del fabricante. Por eso existe el comando de cambiar la prioridad: en una red real no podés depender de qué placa quedó con la MAC más baja.)*

**Paso 3 — Puertos raíz.**

`
 En la RAÍZ (SW1): todos sus puertos con vecino son DESIGNATED.
 No tiene puerto raíz: no necesita camino a sí misma.
 p(e1): DESIGNATED p(e2): DESIGNATED

 En SW2:
 - p(e1) hacia SW1: costo = 100 (directo), BID emisor 8000...0001
 - p(e3) hacia SW3: costo = 100 + 100 = 200, BID emisor 8000...0003
 Gana el de MENOR COSTO -> p(e1) = PUERTO RAÍZ (no se bloquea)

 En SW3:
 - p(e2) hacia SW1: costo 100
 - p(e3) hacia SW2: costo 200
 -> p(e2) = PUERTO RAÍZ (no se bloquea)
`

**Paso 4 — Designados en el enlace SW2–SW3.** En el segmento  compiten SW2 y SW3; gana el de **menor Bridge ID**:  (SW2) ⇒ su  queda **DESIGNATED** y el de SW3 queda en **BLOCKING**.

**Paso 5 — Regla final y dibujo del árbol.** Regla: un puerto se bloquea si su camino al raíz **no es el de menor coste**; todo lo demás → `forwarding`.

`
 ┌──────────────────────────────────────────────────────────────┐
 │ ESTADO FINAL │
 │ SW1 (RAÍZ) │
 │ / \ │
 │ p(e1) p(e2) <- ambos DESIGNATED, FORWARDING │
 │ / \ │
 │ SW2 SW3 │
 │ p(e1) RAÍZ p(e2) RAÍZ <- ambos FORWARDING │
 │ | | │
 │ p(e3) p(e3) │
 │ DESIGNATED ████████ BLOCKING <<<<< AQUÍ SE CORTA │
 │ FORWARD (recibe BPDUs, no manda datos) │
 └──────────────────────────────────────────────────────────────┘

 Puertos bloqueados: SOLO SW3.p(e3) (1 de 6)

 VERIFICACIÓN: en una topología conexa de N bridges y M enlaces, el
 spanning tree bloquea SIEMPRE (M − (N − 1)) puertos.
 Acá: 3 − (3 − 1) = 1. ✔ Cuadra con lo que dibujamos.
`

### (e) La variante: ¿y si SW3 tuviera prioridad 4096?

`
 SW3: prioridad 4096 = 0x1000 -> 1000.0000.0000.0003
 Raíz = MENOR Bridge ID: 1000.0000.0000.0003 <-- AHORA EL MENOR
 ==> SW3 PASA A SER LA RAÍZ

 SW3 (RAÍZ)
 / \
 p(e2) / \ p(e3)
 DESIGN / \ DESIGN
 FORWARD FORWARD
 / \
 SW1 SW2
 p(e2) ROOT p(e3) ROOT
 FORWARD FORWARD
 | |
 p(e1) DESIGN p(e1) ██████ BLOCKING
 FORWARD (el enlace e1 se corta del lado de SW2)
`

El árbol **cambió de forma**, pero el número de puertos bloqueados es el mismo (1). Ese invariante vale para cualquier red conexa.

### (f) ¿Y si se cae el enlace ?

`
 t0: e1 se cae.
 t≈20 s: SW1 y SW2 dejan de oír BPDUs el uno del otro durante Max Age
 (= 20 s) y se dan cuenta de que el vecino "murió".
 t+ : SW2 recibe por e3 los BPDUs de SW3 y recalcula; el enlace e3,
 que estaba bloqueado, se desbloquea y pasa a ser el camino.
 t≈20-50 s con STP clásico: se elige la raíz nueva y se recalculan los
 puertos.

 ⏱️ Con STP clásico (802.1D): 30 a 50 segundos de red parada.
 Con RSTP (802.1w, el default real): sub-segundo a unos segundos,
 porque los puertos "edge" no pasan por Listening/Learning y porque
 los puertos no-edge notifican el cambio al vecino por *proposal* en
 vez de esperar el Max Age.
`

### ⚠️ Errores típicos
- **Olvidar el desempate por MAC.** Si dos switches tienen la misma prioridad (lo normal), el menor Bridge ID **no** es "el primero" sino el de MAC más baja.
- **Poner un puerto raíz en la raíz.** La raíz **no tiene puerto raíz**: tiene todos designados.
- **Confundir "designado" con "más cercano a la raíz".** En un segmento, el designado es el de **menor Bridge ID entre los conectados a ese segmento**, no el más cercano a la raíz.
- **Bloquear el enlace de los dos lados.** El enlace se bloquea en **un solo lado**. Es el error más visible en un diagrama.
- **No verificar con la fórmula (M − (N−1)).** Si el diagrama y la fórmula no dan el mismo número de puertos bloqueados, hay un error.

---

# PARTE 3 — PROBLEMAS DE EXAMEN DE FING

## 3.1 Examen 2010-12, Pregunta 3 (8 puntos) — hub, switch y self-learning

> **Fuente:** Examen  — 17 de diciembre de 2010. Solución oficial: .
> **Link:** https://www.fing.edu.uy/inco/cursos/redescomp/examenes/sirc1012.pdf
> **Texto del examen (literal):**
>
> **a)** Considere una red de varios nodos interconectados por un hub, ¿cuál es el dominio de colisión y cuál es el de broadcast? Justifique.
>
> **b)** Si en la red anterior cambiamos el hub por un switch. ¿Se modifican los dominios de colisión y broadcast? ¿De qué manera?
>
> **c)** Describa el mecanismo de self-learning que utilizan los switches.

Este es **el problema central de la clase**. Los tres incisos se corrigen con el mismo par de ideas: *el hub es cable, el switch es memoria*.

### Parte a) (~3 puntos)

**Solución oficial (texto):**

> a) El dominio de colisión y el dominio de broadcast son iguales y abarcan a todos los nodos de la red. Esto se debe a que el hub no implementa ningún protocolo de acceso al medio y simplemente reenvía todas las tramas por todas las interfaces.

**Análisis.** ✅ Está bien: nombra los dos dominios, dice que abarcan todos los nodos y da **la causa**. ⚠️ Lo que le falta, y son puntos: (1) no dice **qué es** cada dominio, solo que son "iguales"; (2) no dice **por qué** el de colisión es único (mismo medio eléctrico); (3) no dice **por qué** el de broadcast es único (la trama se replica sin filtro, y las copias también se replican).

**Mi respuesta, desarrollada:**

> **a)** Con un hub, el **dominio de colisión y el de broadcast son ambos únicos y abarcan toda la red**.
>
> - **Colisión:** el hub es de **capa 1**, repite la señal eléctrica a todos los puertos. Todas las estaciones comparten **el mismo medio**, así que si dos transmiten a la vez sus señales se superponen y ninguna llega bien. Es **un solo dominio de colisión**, y es half-duplex por definición.
> - **Broadcast:** una trama de broadcast se copia a **todos** los puertos del hub; cada estación que la recibe (si está en otro hub de la red) la reenvía a todos los suyos. **Nada la detiene**, así que llega a **todas** las estaciones: **un solo dominio de broadcast**.

*"No implementa ningún protocolo de acceso al medio" es la causa raíz:* si el hub hiciera algo más que repetir, o bien filtraría tramas y dejaría de ser de capa 1, o bien regularía el acceso y dejaría de ser un medio compartido. Un hub es **un medio compartido con reiteración**, y por eso hereda de ese medio las dos propiedades: colisión sí, frontera no.

### Parte b) (~3 puntos)

**Solución oficial (texto):**

> b) En el caso de un switch existe un dominio de colisión por cada interfaz del switch, por lo que en este caso cada enlace con los nodos tendrá su propio dominio de colisión. El switch impediría que ocurran colisiones. El dominio de broadcast sigue abarcando a todos los nodos de la red.

**Análisis.** ✅ Lo que está bien: (1) dice explícitamente **un dominio de colisión POR INTERFAZ**; (2) dice que **el dominio de broadcast no cambia**; (3) agrega "el switch impediría que ocurran colisiones", que es lo que la mayoría no dice.

⚠️ **Matices que valen puntos, y acá la oficial es algo imprecisa:**
1. **"El switch impediría que ocurran colisiones"** es correcto **solo en full duplex**. En half-duplex un puerto de switch sigue siendo un dominio de colisión con CSMA/CD, y ahí sí pueden occurir colisiones (las *colisiones tardías*). Lo correcto: *el switch no comparte medio, así que en full duplex no hay colisión posible; en half-duplex cada puerto sigue siendo un dominio de colisión propio, con su propio CSMA/CD, **aislado** de los demás.*
2. **Falta decir POR QUÉ no cambia el dominio de broadcast.** La razón es fuerte y sostiene todo lo de VLAN: **una trama de broadcast no puede descartarse**, porque por definición tiene que llegar a todos. El switch no tiene dirección destino que consultar para saber a quién entregarla.
3. **Falta la advertencia de qué pasa si hay un hub debajo.** Si cuelgo un hub de un puerto del switch, **dentro de ese hub hay colisiones otra vez**, y ninguna VLAN lo arregla.

**Mi respuesta (más completa que la oficial):**

> **b)** Sí, se modifica **uno de los dos**:
>
> - **Dominio de colisión: se PARTE en N.** El switch tiene un dominio de colisión **por puerto**, porque cada puerto es un enlace punto a punto con su propio medio. En **full duplex** no hay medio compartido y por lo tanto **la colisión es físicamente imposible**; en **half-duplex** cada puerto es un dominio de colisión propio con su propio CSMA/CD, **aislado** de los demás. (Lo que el switch hace es **eliminar el medio compartido**, no "evitar colisiones".) ⚠️ Si cuelgo un hub de un puerto, **dentro de ese hub vuelve a haber un único dominio de colisión**.
> - **Dominio de broadcast: NO se modifica.** Sigue siendo **toda la red**. Una trama de broadcast () **no puede descartarse**, porque por definición todos tienen que oírla; el switch no tiene dirección de destino que consultar para saber a quién entregarla, así que **la reenvía por todos los puertos**. Lo único que parte el dominio de broadcast es una **VLAN** o un **router**.

### Parte c) (~2 a 3 puntos)

**Solución oficial (texto):**

> c) El mecanismo de self-learning funciona de la siguiente manera:
> - Inicialmente la tabla del switch está vacía.
> - Cuando llega una trama del nodo A con destino B a través de la interfaz X:
> - Anotamos en la tabla que se puede llegar a A a través de la interfaz X.
> - Si hay un registro (B, Y) en la tabla, y X distinto de Y, reenviamos la trama por Y.
> - Si no existe el registro, reenviamos la trama por todas las interfaces excepto X.

**Análisis.** ✅ Lo que está bien y hay que applausear: (1) dice que **la tabla arranca vacía**, que es lo que hace que la primera trama siempre sea flooding y lo que conecta con "el switch arranca como un hub" (que dice la oficial del 2008-12); (2) la definición de la tabla es **origen → puerto**; (3) el **"y X distinto de Y"** del segundo inciso **es el filtrado**, aunque no lo nombre; (4) el tercer inciso dice "**todas las interfaces excepto X**". Exacto.

⚠️ **Lo que falta, y son puntos:**
1. **El caso  no está escrito**: está escondido en un "y". Si lo escribís aparte, decís "si la entrada dice que B está en el mismo puerto por el que entró, la trama se descarta, porque el destino ya la oyó". Ese es el **filtrado**.
2. **No dice que se aprende SOLO del origen.** Es lo más importante: si aprendiera del destino, un atacante podría envenenar la tabla con una sola trama. Y también explica por qué el flooding **no** enseña nada.
3. **No dice nada del ageing / temporizador.** Cada anotación va con un temporizador que expirar la entrada.
4. **No dice que el broadcast/multicast siempre se inunda**, que es un subcaso del tercer inciso (jamás están en la tabla).

**Mi respuesta, completa y ordenada:**

> **c)** El switch mantiene una **tabla de reenvío** (*forwarding table*, o CAM table) que asocia **dirección MAC → puerto**, con un **temporizador de ageing** por entrada.
>
> 1. **Inicialmente la tabla está vacía.** Por eso, al arrancar, el switch se comporta como un hub: inunda todo hasta aprender.
> 2. **Aprendizaje (siempre, en primer lugar):** ante cualquier trama que llega por el puerto **X**, se anota `A → X`, donde **A es la dirección MAC origen**, y se **reinicia el temporizador de ageing** de esa entrada. Se aprende **solo del origen**, porque el origen es información verificada por el cable (quien está en el puerto X es, necesariamente, quien puso esa MAC); el destino es solo lo que el emisor **quiere** que creamos.
> 3. **Decisión del destino, con B = MAC destino:**
> - Si **B es broadcast o multicast** (jamás está en la tabla): se reenvía por **todos los puertos menos X** (*flooding*).
> - Si **existe  y **: se reenvía por el puerto **Y** (unicast, una sola copia).
> - Si **existe  y **: se **descarta** la trama (el destino está en el mismo segmento por el que llegó; ya la oyó) — esto es el **filtrado**.
> - Si **no existe entrada para B**: se reenvía por **todos los puertos menos X** (*flooding*), porque no se sabe a dónde va. El flooding **no aprende nada**: el switch solo aprende del paso 2.
> 4. **Ageing:** cada entrada tiene un temporizador (típicamente **300 s**, default de fabricante y configurable) que se reinicia cada vez que se ve esa MAC. Si expira, la entrada se borra, y la próxima trama con ese destino vuelve a ser un flooding.

**Reparto orientativo de los 8 puntos** (el enunciado no lo publica):

| Inciso | Peso | Lo que no puede faltar |
|---|---|---|
| a) | ~3 | los dos dominios = **toda la red**; la causa: el hub es capa 1 y repite todo |
| b) | ~3 | colisión → **uno por puerto**; broadcast → **sigue toda la red**, porque el broadcast no se puede descartar; de paso, full duplex no tiene colisión |
| c) | ~2 | tabla vacía; **aprende del origen**; unicast si conoce, **flooding por todos menos X** si no; el "**y X distinto de Y**" es el filtrado |

## 3.2 Examen 2008-12, Pregunta 2 (5 puntos) — qué mejora reemplazo hubs por switches

> **Fuente:** Examen  — 20 de diciembre de 2008.
> **Link:** https://www.fing.edu.uy/inco/cursos/redescomp/examenes/sirc0812.pdf
> **Texto del examen (literal):**
>
> **Pregunta 2 (5 puntos)** Explique que posibles mejora introduce la sustitución de hubs por switches, en cuanto a performance y seguridad en las redes LAN.

### Solución oficial (extracto textual)

> El principio de funcionamiento de los hubs es que todo el tráfico que ingresa por un puerto, es enviado por todos los demás puertos del dispositivo, aunque en la mayoría de los casos el tráfico estará dirigido a uno sólo de dichos puertos. Los switches, por el contrario, al "entender" de direcciones MAC redirigen las tramas que ingresan por un puerto al puerto por donde se alcanza la máquina destino de la misma. **No debemos olvidar que éste es el comportamiento en régimen de un switch. En la fase de arranque y apendizaje, se comporta como un hub** a los efectos de ir aprendiendo qué direcciones son alcanzables en cada puerto. Por otro lado, los switches incorporan buffers en cada puerto así como una matriz de conmutación de por lo menos un orden de velocidad mayor a la de los puertos. De esta forma, en un switch podemos tener múltiples comunicaciones simultáneas (a diferencia de un hub), ellas full-duplex y cada puerto de un switch puede ser un sólo dominio de colisión (frente al único dominio de colisión que significa un hub) todo lo que redunda en un aumento notorio de la performance de la red. Por otro lado, la mejora en cuanto a seguridad está basada en que, en un switch funcionando en régimen, el tráfico sólo es enviado al puerto donde está conectada la máquina destino del mismo, lo que permite "ocultar" el dicho tráfico al resto de las máquinas conectadas al switch. También la implementación de VLANs puede ser una medida que colabore a la seguridad en una red switcheada.

### Análisis de la solución oficial

✅ **Es una solución muy buena.** Tres cosas que hay quer sí o sí, porque son ideas que dan puntos:

1. **"En la fase de arranque y aprendizaje, se comporta como un hub."** Es **la mejor frase de la solución** y casi ningún alumno la dice. Dice que **la mejora de seguridad no es total ni inmediata**: hay una ventana insecure al arrancar.
2. **"Buffers en cada puerto" + "matriz de conmutación de por lo menos un orden de velocidad mayor".** No dice solo "más rápido": da la **causa** (matriz más rápida que los puertos + buffers por puerto), que es lo que permite explicar **por qué** hay comunicaciones simultáneas.
3. **"VLANs como medida de seguridad."** Adelanta el tema de la VLAN (que es el 2009-03 P3, de tres meses después) y conecta las dos preguntas del mismo bloque.

⚠️ **Lo que le falta:** (1) **no cuantifica el ganho de ancho de banda** (con  estaciones el hub da  y el switch da  a cada una): es una línea y vale puntos; (2) no precisa el caso half-duplex frente a full-duplex, aunque lo insinúa con "full-duplex"; (3) no menciona que el switch **duplica el tráfico interno** al procesarlo en la matriz, aunque en 5 puntos eso es detalle.

### Mi respuesta, estructurada para 5 puntos

**a) Performance (~3 puntos)**

> **Con un hub**, la trama que entra por un puerto sale por **todos** los demás, y la red es **un único medio compartido**:
> - **Un solo dominio de colisión**: todas las estaciones comparten el mismo medio; el ancho de banda se **divide** ( por estación), las tramas se **duplican** ( copias de cada trama, de las cuales  se descartan), y hay colisiones con CSMA/CD.
> - **Half-duplex**: no se puede transmitir y recibir a la vez.
>
> **Con un switch**, en régimen:
> - **Aprende las direcciones MAC** y **envía cada trama por un solo puerto**, el del destino. Se elimina el desperdicio: la trama deja de multiplicarse.
> - **Cada puerto es un dominio de colisión independiente** y trabaja en **full duplex**. En full duplex **no hay colisión posible**, porque no hay medio compartido. Con  estaciones, el ancho de banda **por estación pasa de  a **.
> - **Buffer por puerto y una matriz de conmutación más rápida que los puertos**, lo que permite **varias comunicaciones simultáneas** sin que una bloquee a las otras.
>
> ⚠️ **El matiz que hay que decir:** un switch recién arrancado tiene la tabla vacía y **se comporta como un hub** hasta aprender. Las tramas iniciales se inundan. La mejora es de régimen, no de arranque.

**b) Seguridad (~2 puntos)**

> **Con un hub**, el medio es compartido: **todo el tráfico que pasa por él es visible en todos los puertos**, sin excepción. Cualquier estación puede ver (con un sniffer) el tráfico de todas las demás: contraseñas, claves, cabeceras. Seguridad **cero**.
>
> **Con un switch**, en régimen, **cada trama sale solo por el puerto de su destino**: el tráfico de una estación **no es visible** desde los otros puertos. Eso es una mejora real y directa.
>
> **Pero no alcanza como mecanismo de seguridad:**
> - Durante el **aprendizaje** el switch inunda, y en esa ventana se ve todo.
> - Un atacante que **inunda la tabla con MAC falsas** (*MAC flooding*) agota la memoria de reenvío y **degrada el switch a hub**.
> - El switch **no autentica a nadie**: cualquiera que enchufe un cable entra a la red.
>
> **Sí hay un refuerzo estructural:** las **VLANs**, que particionan lógicamente el switch en varios dominios de broadcast independientes y **confinan el flooding** dentro de cada VLAN. Con eso, lo que no es unicast se queda en su VLAN, y el tráfico de una VLAN no es visible desde los puertos de otra.

> **Nota sobre el tamaño de esta pregunta:** 5 puntos y **ninguna aritmética**. Es una pregunta de **fundamentos bien enunciados**. Si te quedás pensando en cuentas, no llegás. Decí **qué cambia** (de "medio compartido" a "enlace punto a punto con memoria") y **por qué** eso mejora cada una de las dos cosas.

## 3.3 Examen 2009-03, Pregunta 3 (6 puntos) — el concepto de VLAN

> **Fuente:** Examen  — 20 de febrero de 2009.
> **Link:** https://www.fing.edu.uy/inco/cursos/redescomp/examenes/sirc0903.pdf
> **Texto del examen (literal):**
>
> **Pregunta 3 (6 puntos)** Explique el concepto VLAN (p.e. 802.1q) y comente sobre su utilidad.

> ⚠️ **Nota sobre el puntaje:** el PDF asigna **6 puntos** a esta pregunta (y trae su solución oficial). Algunas recopilaciones del banco la listan como 10. **Se corrige 6**, y eso no cambia la respuesta.

### Solución oficial (texto)

> Es una tecnología que nos permite tener más de un dominio de broadcast en una misma red switcheada. Se trata de una mejora que se puede incorporar a la red de manera transparente para los usuarios finales ya que la configuración corre por cuenta de los administradores de la misma. La utilidad radica en que se puede tener "varias redes" LAN soportadas por el mismo equipamiento y donde la pertenencia de cada puerto a cada VLAN se puede ajustar bajo demanda. Al poder distinguir qué puertos de un switch pertenecen a qué VLAN, indirectamente es una mejora respecto a seguridad, en particular en lo que refiere a tráfico no unicast y también en el caso de falta de determinadas entradas en las tablas que asocian dirección MAC con puerto.

### Análisis de la solución oficial

✅ **Lo que está muy bien:**
1. **"Más de un dominio de broadcast en una misma red switcheada."** Definición en una línea y **exactamente correcta**. Con esa frase ya tenés el punto central.
2. **"La pertenencia de cada puerto a cada VLAN se puede ajustar bajo demanda."** Dice lo esencial: la VLAN es una **atribución de puertos**, y se cambia por configuración. Es lo que permite mover un usuario sin tocar el cable.
3. **"Tráfico no unicast"** es la idea más fina de toda la solución, y casi nadie la encuentra. Significa: el problema de seguridad de un switch no es el unicast (que va dirigido a un solo puerto), sino **el flooding** (broadcast, multicast y unicast a destino desconocido). La VLAN **no cambia el unicast**: lo confina.

⚠️ **Lo que le falta:** (1) **no desarrolla 802.1Q**, pese a que el enunciado dice "(p.e. 802.1q)": ni el tag de 4 bytes, ni el VID, ni el C-TAG; (2) **no dice por qué** el broadcast se confina (que el switch etiqueta la trama y el flooding se hace **dentro** de la VLAN); (3) no menciona el **router-on-a-stick** ni el **PVID**.

### Mi respuesta completa (6 puntos)

**a) Qué es (2 puntos)**

> Una **VLAN** (*Virtual LAN*, LAN virtual) es una **partición lógica** de la red conmutada: un mismo **switch físico** se comporta como **varios switches independientes**, uno por VLAN, según a qué VLAN pertenece cada puerto. La pertenencia **no la define el cable ni la estación**: la define la **configuración del switch**.
>
> Para que la trama sobreviva a varios switches, 802.1Q **agrega un tag de 4 bytes** a la trama Ethernet, que lleva el **VLAN ID** (12 bits, valores 1 a 4094) y una prioridad de 3 bits. El `TPID` pasa a ser `0x8100` (C-TAG) en vez de `0x0800`. Un puerto **access** (de usuario) quita el tag; un puerto **trunk** lo conserva.

**b) Para qué sirve (4 puntos)**

> **1. Parte el dominio de broadcast.** Sin VLAN hay **un solo** dominio de broadcast en todo el switch, y las tramas de broadcast se replican a **todos** los puertos. Con VLAN hay **uno por VLAN**: el flooding se hace **dentro de la VLAN**, o sea, por los puertos **de esa VLAN solamente**. Eso reduce el ruido (ARP, DHCP, mDNS) y permite que una sola  lógica conviva con otras en el mismo switch.
>
> **2. Seguridad.** El tráfico no unicast (broadcast y multicast) es el que sale por **todos** los puertos, y el unicast a un destino **desconocido** (que no está en la tabla MAC) también se inunda. Ese flooding es el que un atacante ve. La VLAN **confina ese flooding dentro de la VLAN**: lo que no sale de la VLAN no se ve desde los puertos de las otras, y el unicast entre dos puertos de la misma VLAN tampoco se ve desde fuera.
>
> **3. Mover un usuario sin mover el cable.** La configuración es del switch. Si el usuario se muda de escritorio, su cable va al mismo patch panel y **lo que cambia es la línea de configuración** que asigna ese puerto a una VLAN. Antes de las VLAN, mover a alguien significaba repatchear el cableado.
>
> **4. Segmentar la gestión.** Las VLANs permiten separar el tráfico de administración del de datos, de modo que **inundar la red de gestión no llena de tráfico todos los puertos** del switch.

**c) El mecanismo (por qué funciona lo de la seguridad)**

> El switch etiqueta cada trama con el VLAN ID y, cuando decide inundar, **solo inunda por los puertos de esa VLAN**: las tramas de otra VLAN no se mezclan. Y el dominio de broadcast **se cierra** porque un **router** (o una subinterfaz de router, el *router-on-a-stick*) **no reenvía tramas de broadcast entre interfaces**. Es el router, y no la VLAN, el que realmente termina el dominio de broadcast entre VLANs distintas.

### ⚠️ Las dos frases que hay que decir de memoria
> **"VLAN es lo que hace que un switch pueda ser varias redes."**
>
> Y si te sobra tiempo: **"La VLAN no evita el flooding; lo confina."** Esa distinción es la que separa una respuesta de 6 de una de 4.

---

# PARTE 4 — CIERRE

## 📌 Resumen en 10 líneas

1. **Hub** = capa 1: repite a todos los puertos. **Un** dominio de colisión, **un** dominio de broadcast, **cero** seguridad.
2. **Bridge** = mira la trama y tiene **dos verbos**: reenviar a un puerto, o **inundar** por todos.
3. **Switch** = un bridge con muchos puertos, buffer por puerto y una matriz de conmutación más rápida que los puertos.
4. **Self-learning**: el switch aprende la **MAC origen** y la asocia al puerto de entrada. Todo lo demás es **inferencia**.
5. El algoritmo: **(1) aprender A → X**; **(2)** si `B` está en el puerto `Y` y `Y ≠ X`, unicast por `Y`; si `Y == X`, **descartar** (filtrado); si no está, **flooding por todos menos X**.
6. **Ageing**: sin él, un nodo que se muda deja de ser alcanzable. **300 s es default de fabricante**, no un valor de IEEE.
7. **Switch**: cada puerto es su propio dominio de colisión (**en full duplex la colisión es imposible**) y el ancho de banda es `1 Gbps` por estación en vez de `100 Mbps` compartidos. Pero el dominio de broadcast **sigue siendo toda la red**.
8. **VLAN**: partición lógica del switch. El **tag 802.1Q** son 4 bytes (TCI + ) con **VID de 12 bits (1–4094)**; C-TAG vs. S-TAG (); **PVID** para las tramas sin tag.
9. **Loop en capa 2 = tormenta de broadcast**, y los bridges transparentes **no usan TTL**: por eso existe el **spanning tree** (raíz con menor Bridge ID = prioridad 32768 + MAC, puerto raíz, puertos designados, y el resto en **blocking**).
10. En 2026: **half-duplex muerto por encima de 1 Gb/s** (decisión de **IEEE**, no RFC de IETF), ****, **** para LAG, **RSTP (802.1w)** como default real, y **C-TAG/S-TAG** en carrier Ethernet y EVPN-VXLAN.

## ✅ Autoevaluación

Respondé sin mirar. Las respuestas están en `<details>`.

**1.** ¿Por qué un hub tiene **un solo** dominio de colisión **y** un solo dominio de broadcast? Dos frases, una para cada uno.

<details><summary>Respuesta</summary>

**Colisión:** el hub es de capa 1 y repite la señal eléctrica a todos los puertos, así que todas las estaciones comparten **el mismo medio físico**. Si dos transmiten a la vez, las señales se superponen en ese medio y ninguna llega bien.

**Broadcast:** una trama de broadcast se copia a todos los puertos **sin ningún filtro**, y las copias que llegan a otras estaciones también se reenvían. **Nada la detiene**, porque para descartarla haría falta saber quién la pidió, y eso no está en la trama.

Las dos propiedades vienen de la misma causa: **un medio compartido no tiene fronteras**.

</details>

**2.** Llega por el puerto 5 una trama con MAC origen `A` y MAC destino `B`. La tabla dice `B → p4`. ¿Qué hace el switch?

<details><summary>Respuesta</summary>

**Aprende**  (y le pone o renueva el temporizador de ageing).

**Después** busca : está en la tabla, pero en el puerto 5, que es **el mismo por el que entró** (). Entonces **descarta la trama**.

Ese es el caso de **filtrado**: el destino  está en el mismo segmento que el emisor, así que ya oyó la trama directamente por el medio. Reenviársela sería una copia inútil. Es exactamente lo que un hub no puede hacer.

Ojo: el switch **no descarta la trama completa**, descarta el **reenvío**. El aprendizaje del paso 1 ya ocurrió.

</details>

**3.** ¿Por qué el switch aprende la MAC **origen** y no la **destino**?

<details><summary>Respuesta</summary>

Porque **el origen es información verificada por el cable**: si una trama entra por el puerto 3, es porque la estación conectada al puerto 3 la mandó, y esa estación puso su propia MAC en el campo origen. Es una garantía física.

El **destino**, en cambio, es solo lo que **quien manda quiere que creamos**. Si el switch aprendiera del destino, un solo atacante que mandara tramas con la MAC de otra estación **venenaría la tabla** y desviaría todo su tráfico. Es el mismo problema que el *ARP spoofing*, pero en la tabla del switch.

De ahí una consecuencia: **el flooding no aprende nada**, porque en un flooding la dirección destino es broadcast o una MAC desconocida.

</details>

**4.** En el ageing de 300 s, ¿por qué una estación que transmite una vez cada 200 s "pierde" su entrada aproximadamente el 78 % de las veces? Calculá.

<details><summary>Respuesta</summary>

Con un proceso de Poisson de tasa `λ`, la probabilidad de **cero** arribos en un intervalo de longitud `T` es `e^(−λT)`.

`
 λ = 1/200 = 0,005 tramas/s
 T = 300 s

 P(sobrevive) = e^(−0,005 · 300) = e^(−1,5) = 1/4,48169 = 0,2231
 P(expira antes) = 1 − 0,2231 = 0,7769 ≈ 77,7 %
`

O sea: la estación habla cada 200 s, pero la tabla olvida a los 300 s. **El intervalo de habla es menor que el de olvido**, así que es más probable que el reloj venza antes de la próxima trama. Cuando la trama llega, es un **flooding**.

La lección de diseño: el ageing tiene que ser **mayor** que el intervalo de habla esperado, o la tabla se llena de entradas que mueren y renacen.

</details>

**5.** Explicá por qué el dominio de broadcast **no** se parte al cambiar un hub por un switch, y qué sí lo parte.

<details><summary>Respuesta</summary>

Porque una **trama de broadcast no puede descartarse**: por definición, tiene que llegar a **todas** las estaciones del dominio. El switch, para decidir, necesita consultar la dirección destino en su tabla, y la dirección destino de un broadcast () **nunca está en la tabla**: no identifica a ninguna estación. No hay a quién "entregarle" la trama de forma selectiva, así que la manda por todos los puertos.

**Lo que sí lo parte:** una **VLAN** (el flooding se confina a los puertos de esa VLAN) y un **router** (no reenvía broadcast entre interfaces, así que es el router el que realmente termina el dominio de broadcast entre subredes).

Y el error al revés: lo que **sí** se parte al cambiar el hub por un switch es el **dominio de colisión**, porque cada puerto pasa a ser un enlace punto a punto.

</details>

**6.** ¿Qué son el **C-TAG** () y el **S-TAG** (), y por qué hay dos?

<details><summary>Respuesta</summary>

Son los dos  que 802.1Q usa para señalar una trama etiquetada, y existen porque en *carrier Ethernet* hay **dos operadores de VLAN en el mismo cable**:

- **C-TAG ()**: la pone el **cliente** (la empresa que se conecta). Es la etiqueta de la **VLAN del cliente**.
- **S-TAG ()**: la pone el **proveedor** (el carrier). Es la etiqueta de la **VLAN del carrier**, que es la unidad por la que factura.

Si ambas usaran  no se sabría cuál termina primero, porque las dos etiquetas son estructuralmente idénticas. El S-TAG va **encima** (más externo) del C-TAG.

El doble etiquetado es hoy **estándar en carrier Ethernet y en EVPN-VXLAN**, que es el overlay de datacenter por defecto (EVPN  + VXLAN ).

</details>

**7.** ¿Por qué un loop en capa 2 es mucho más grave que uno en capa 3?

<details><summary>Respuesta</summary>

Porque **no hay TTL**.

Un router **descarta** el paquete cuando su TTL llega a cero: el contador es la red de seguridad de la capa 3, y garantiza que un paquete perdido en un lazo **muere solo**.

Un bridge transparente **no puede tocar nada de la trama** (para eso es transparente), así que **no decrementa ningún TTL** — y la trama Ethernet **ni siquiera tiene campo TTL**. Por eso una trama de broadcast que entra en un lazo **circula para siempre**, y además **se multiplica** en cada switch que la reenvía, porque cada copia es tratada como una trama nueva. El resultado es saturación de todos los puertos, buffers llenos, CPU al 100 % y **el switch deja de responder**: una tormenta de broadcast (*broadcast storm*).

Por eso existe el **spanning tree**: no evita los loops, **los calcula y pone una puerta** en ellos.

</details>

**8.** En una red con tres switches en triángulo, todos con prioridad 32768 y costos de enlace iguales, ¿cuántos puertos quedan bloqueados y por qué número?

<details><summary>Respuesta</summary>

**Uno.**

En una topología conexa de  bridges y  enlaces, el spanning tree **bloquea siempre  puertos**. Con  y  (triángulo):

`
 3 − (3 − 1) = 3 − 2 = 1 puerto bloqueado
`

Y se puede verificar **quién**: la raíz es el de **menor Bridge ID** = menor **prioridad**. Con las tres prioridades iguales (32768), gana el de **MAC más baja**. Ese switch (la raíz) tiene todos sus puertos **designated**; los otros dos tienen cada uno un **puerto raíz** (el que va hacia la raíz) y, en el enlace entre ellos, **el de menor Bridge ID queda designated y el otro se bloquea**.

**Ojo:** el enlace se bloquea **en un solo lado**. Bloquearlo de los dos lados es el error más visible en un diagrama.

</details>

## 🔗 Referencias

- **Examen ** (17-dic-2010) — **Pregunta 3 (8 pts)**: dominio de colisión y de broadcast con hub; qué cambia con switch; mecanismo de self-learning. Con solución oficial. **Problema central de esta clase.**
- **Examen ** (20-dic-2008) — **Pregunta 2 (5 pts)**: mejoras de performance y seguridad al sustituir hubs por switches. Con solución oficial.
- **Examen ** (20-feb-2009) — **Pregunta 3 (6 pts)**: concepto de VLAN (802.1Q) y su utilidad. Con solución oficial.
- **Examen ** (26-feb-2007) — Pregunta 2 (10 pts): bridge, flooding y bucles; la solución oficial es el **árbol de cubrimiento**, o sea **STP**. **Es el examen del banco más cercano a §1.7.**
- **Tanenbaum & Wetherall**, *Redes de computadoras* 5ª ed., cap. 3 (§3.4 "La capa de red del enlace de datos: switches", §3.6 y §3.7) y cap. 1 (repetidores, puentes y switches)
- **IEEE 802.3** — Ethernet: formato de trama, tabla de reenvío, ageing, dominios de colisión. **No es una RFC de IETF**: es un estándar del IEEE.
- **IEEE 802.1D** — Spanning Tree Protocol: Bridge ID (prioridad base 32768 + MAC), BPDUs, estados Blocking/Listening/Learning/Forwarding, temporizadores (Hello 2 s, Max Age 20 s, Forward Delay 15 s).
- **IEEE 802.1w** — **RSTP**: Rapid Spanning Tree Protocol, hoy el default real de los switches.
- **IEEE 802.1s** — **MSTP**: Multiple Spanning Tree, para compartir un árbol entre varias VLANs.
- **IEEE 802.1Q-2022** — VLANs y el tag de 4 bytes; revisión actual (precedida por `802.1Q-2018`, que abrió TSN con `802.1Qbv` + `802.1Qbu` y `802.1Qci`; 2022 agregó `802.1Qcc` y `802.1Qcr`).
- **IEEE 802.1AX-2020** — Link Aggregation (LAG), sucesión de  (2000).
- **IEEE 802.3cg** — 10BASE-T1S: el único caso industrial donde el **half-duplex sigue siendo obligatorio** (con PLCA). La eliminación del half-duplex por encima de 1 Gb/s es una decisión de **IEEE**, **no una RFC de IETF** (⚠️  es JSCalendar, no Ethernet).
- **RFC 826** — ARP: request en broadcast, reply en unicast; es quien sufre el dominio de broadcast.
- **RFC 7432** — EVPN · **RFC 7348** — VXLAN (encapsulado sobre UDP/4789): el estándar de overlay de datacenter, donde el tenant se identifica por **VNI** y no por 802.1Q.
- **Clase anterior:** 41 — Acceso al medio: ALOHA, CSMA/CD y CSMA/CA
- **Clase siguiente:** 43 — Redes inalámbricas 802.11: CSMA/CA, estación oculta, NAV, RTS/CTS, EDCA y seguridad