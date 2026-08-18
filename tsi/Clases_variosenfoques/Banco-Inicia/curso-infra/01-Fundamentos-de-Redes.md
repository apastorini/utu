# INFRA-01 · Fundamentos de Redes

> **Función del MCU 5.0:** Este módulo entrega los conceptos mínimos de redes (IP, subredes, máscaras, VLAN, NAT, DNS, DHCP) que el Responsable de Seguridad de la Información (RSI) necesita para entender dónde viven los activos y cómo circulan los datos.
> **ISO/IEC 27001:** La red es el "camino" por donde viaja la información. Los controles del Anexo A (gestión de activos, control de acceso, protección de las comunicaciones) dependen de entender cómo está construida la red.
> **BCU:** La normativa de riesgos de tecnología de la información exige conocer y documentar la infraestructura tecnológica; una red mal entendida se documenta mal y se controla peor.
> **URCDP:** El inventario de sistemas y redes del Documento de Seguridad URCDP-01 se llena correctamente solo si quien lo redacta comprende estos fundamentos.
> **Nivel del curso:** 🟢 Descubrir · 🟡 Practicar · 🔴 Dominar

---

## 1. Qué es una red informática

Pensemos en el correo postal. Cuando usted envía una carta, el servicio de correo se encarga de llevarla desde su casa hasta la casa del destinatario. Para eso necesita saber **de dónde sale** (su dirección), **a dónde va** (la dirección del destinatario) y **por qué camino circular** (la ruta del cartero).

Una **red informática** es lo mismo, pero para datos. Es un conjunto de computadoras, servidores, impresoras y otros equipos conectados entre sí que pueden intercambiar información. En lugar de cartas, viajan correos electrónicos, operaciones bancarias, archivos y consultas a sistemas.

Una red es simplemente "varias máquinas conectadas que se hablan entre sí", igual que un barrio entero conectado por un sistema de calles con numeración de casas.

### Por qué el Banco necesita una red

- Para que las sucursales consulten los saldos de los clientes en tiempo real.
- Para que Banco En Línea funcione: cada clic del cliente viaja por una red hasta los servidores del banco.
- Para que los empleados compartan archivos, correo e impresoras.
- Para que los sistemas de seguridad (cámaras, alarmas, monitoreo) envíen sus datos.

Sin red, el banco no podría operar como un banco: cada computadora quedaría aislada y habría que trasladar información en papel o en memorias USB (algo inaceptable por seguridad).

---

## 2. Tipos de red

| Sigla | Nombre | Qué es | Analogía |
|-------|--------|--------|----------|
| LAN | Red de Área Local | Red pequeña dentro de un edificio u oficina | El sistema de calles de un mismo barrio |
| WLAN | Red de Área Local Inalámbrica | La misma LAN pero con WiFi | El barrio conectado por "ondas" |
| WAN | Red de Área Amplia | Red que une sitios lejanos (sucursales con Casa Central) | Las rutas nacionales que unen ciudades |
| VPN | Red Privada Virtual | Túnel cifrado sobre una red pública | Una valija blindada que viaja por el correo común |

En el Banco:
- Cada sucursal tiene una **LAN** (y una **WLAN** para los equipos móviles internos).
- Todas las sucursales se conectan a Casa Central formando una **WAN**.
- Los empleados que trabajan desde su casa usan una **VPN** para entrar a la red del banco de forma segura.

---

## 3. Dirección IP

Una **dirección IP** es la "matrícula" o "número de casa" de un dispositivo dentro de una red. Sin IP, los datos no saben a quién entregarse.

### IPv4

La versión más usada. Son 4 números entre 0 y 255 separados por puntos. Ejemplo: `10.0.0.1`, `172.16.5.20`, `192.168.1.50`.

Una IP se divide en dos partes:
- **Red (network):** identifica a qué barrio pertenece el dispositivo.
- **Host:** identifica al dispositivo dentro de ese barrio.

Ejemplos típicos de IPs privadas (internas del banco):

| Red | Rango privado | Comentario |
|-----|---------------|------------|
| `10.0.0.0/8` | 10.0.0.0 a 10.255.255.255 | Redes grandes de empresas |
| `172.16.0.0/12` | 172.16.0.0 a 172.31.255.255 | Redes medianas |
| `192.168.0.0/16` | 192.168.0.0 a 192.168.255.255 | Redes domésticas y oficinas pequeñas |

Las IPs **privadas** solo existen dentro de la organización; las **públicas** son las que ve Internet. El banco tiene IPs públicas para sus servicios web (como bhu.com.uy) y usa IPs privadas en su interior.

### IPv6

IPv4 se quedó sin direcciones para todo el mundo (unos 4.000 millones). IPv6 fue creado para tener prácticamente infinitas direcciones (se escriben con números y letras, ejemplo: `2001:db8::1`). En el Banco convive con IPv4; el RSI debe saber que existe, pero para el día a día los conceptos de este módulo aplican igual.

---

## 4. Máscara de subred y notación CIDR

La **máscara de subred** indica cuántos bits de la IP pertenecen a la parte de red y cuántos a la parte de host. Es como la línea en un mapa que delimita el barrio.

La **notación CIDR** (ejemplo `/24`) es una forma corta de escribir la máscara: el número indica cuántos bits "1" tiene la máscara.

| Máscara | CIDR | Bits de host | Hosts útiles |
|---------|------|--------------|--------------|
| 255.0.0.0 | /8 | 24 | 16.777.214 |
| 255.255.0.0 | /16 | 16 | 65.534 |
| 255.255.255.0 | /24 | 8 | 254 |
| 255.255.255.128 | /25 | 7 | 126 |
| 255.255.255.192 | /26 | 6 | 62 |
| 255.255.255.224 | /27 | 5 | 30 |
| 255.255.255.240 | /28 | 4 | 14 |

### Cómo se calcula

Hosts útiles = 2 elevado a los bits de host, menos 2.

- Los **2 que se restan** son: la primera IP (dirección de red) y la última (dirección de difusión o broadcast).
- Con `/24` hay 8 bits de host: 2⁸ = 256, menos 2 = **254 hosts útiles**.

### Errores comunes del principiante

- ☐ Confundir la cantidad total de direcciones con la cantidad útil (no contar los menos 2).
- ☐ Calcular hosts con la máscara puesta al revés (contar bits de red como si fueran de host).
- ☐ Usar `255.255.255.0` cuando en realidad se necesita `/26` para una sucursal pequeña.

---

## 5. Subredes: por qué se segmenta

Una **subred** es una división más pequeña de una red. En lugar de tener un solo barrio gigante con todos los vecinos, la red se organiza en varios barrios.

Por qué el banco segmenta:
- **Seguridad:** aísla lo sensible. Una subred para TI, otra para sucursales, otra para la DMZ (zona donde viven los servidores que se exponen a Internet).
- **Control de tráfico:** menos equipos por segmento = menos "ruido" y colisiones.
- **Facilidad de gestión:** se aplican reglas distintas a cada segmento.
- **Contención:** si un equipo se infecta, la infección no salta de subred a subred tan fácilmente.

### Ejemplo numérico paso a paso

Partimos de la red `192.168.10.0/24` (254 hosts). Queremos dividirla en 2 subredes de igual tamaño:

1. Necesitamos 1 bit extra para identificar la subred: máscara `/25` (255.255.255.128).
2. Subred A: `192.168.10.0/25` → hosts útiles de `192.168.10.1` a `192.168.10.126`.
3. Subred B: `192.168.10.128/25` → hosts útiles de `192.168.10.129` a `192.168.10.254`.

Cada subred tiene su propia dirección de red y su propia dirección de broadcast, y **no se superponen**. Ese es justamente el error que hay que evitar: dos subredes que comparten direcciones.

---

## 6. Gateway o puerta de enlace

El **gateway** (puerta de enlace) es la "salida del barrio". Es la dirección IP del router que permite a un dispositivo comunicarse con equipos que están **fuera de su subred**.

Si su computadora tiene IP `192.168.1.10/24`, el gateway típico es `192.168.1.1` (el router). Todo el tráfico que no pertenece a su subred se envía al gateway.

### Errores comunes

- ☐ Poner mal el gateway (por ejemplo, apuntarlo a una IP que no existe): el equipo funciona "en red local" pero no navega.
- ☐ Olvidar configurar el gateway en un servidor nuevo.
- ☐ Confundir el gateway con la IP propia.

---

## 7. DNS: la agenda de la red

El **DNS** (Sistema de Nombres de Dominio) traduce nombres fáciles de recordar (`www.bhu.com.uy`) a direcciones IP (`10.x.x.x` o una IP pública). Es como la agenda del teléfono: usted marca "María", no el número completo.

- Si el DNS falla, el correo interno sigue funcionando por IP, pero "no abre páginas".
- Un DNS apuntando mal es una causa típica de "no navego".

### Errores comunes

- ☐ Configurar el servidor DNS con una IP incorrecta.
- ☐ Usar DNS públicos desde equipos del banco sin autorización (salida de tráfico por un camino que nadie controla).

---

## 8. DHCP: la asignación automática

El **DHCP** entrega automáticamente IP, máscara, gateway y DNS a cada equipo que se conecta. Es como el portero del edificio que le dice a cada visitante qué oficina le corresponde.

- **IP dinámica (DHCP):** la asigna el servidor y puede cambiar. Ideal para puestos de trabajo y equipos móviles.
- **IP estática (fija):** se configura a mano y no cambia. Ideal para servidores, impresoras de red, routers y firewalls.

### Errores comunes

- ☐ Mezclar un rango estático dentro del rango del DHCP: se generan **conflictos de IP** (dos equipos con la misma dirección).
- ☐ No reservar las IPs de los equipos críticos.

---

## 9. VLAN: separar sin cables nuevos

Una **VLAN** (Red de Área Local Virtual) permite dividir el tráfico en grupos lógicos **dentro del mismo switch físico**. Es como un edificio con varios ascensores que no se cruzan: los pasajeros usan el mismo edificio, pero cada ascensor tiene su destino.

- Se puede tener una VLAN para TI, otra para sucursales y otra para la DMZ, **sin instalar un switch nuevo por cada grupo**.
- El aislamiento se define por configuración (etiquetas de VLAN), no por cables.

Por qué importa: separa tráfico sensible del tráfico general y permite aplicar reglas de firewall por VLAN. Un switch mal segmentado (todo en una sola VLAN) es un error de seguridad importante.

---

## 10. NAT: privadas a públicas

El **NAT** (Traducción de Direcciones de Red) convierte las IPs privadas internas en una o varias IPs públicas cuando el tráfico sale a Internet. Es el "portero de la embajada": todos los que salen usan la misma puerta pública, y el portero recuerda quién entró para devolverle cada respuesta.

- Sin NAT, las IPs privadas no podrían navegar (Internet no sabe quién es `10.0.0.5`).
- NAT se implementa normalmente en el router o en el **firewall**, por eso en el Banco se asocia el firewall a la salida a Internet.
- El firewall, además, decide **qué** puede salir y entrar, no solo cómo se traduce.

---

## 11. Puertos y protocolos

Cada IP identifica el edificio; el **puerto** identifica la puerta o la ventana dentro del edificio. Es lo que permite que en el mismo servidor convivan el correo y la web.

### TCP y UDP

- **TCP:** conexión con confirmación (como una llamada telefónica con acuse de recibo). Confiable.
- **UDP:** envío rápido sin confirmación (como tirar una pelota por encima de la pared). Ideal para video y DNS.

### Puertos comunes

| Puerto | Protocolo | Servicio |
|--------|-----------|----------|
| 80 | TCP | HTTP (web) |
| 443 | TCP | HTTPS (web segura) |
| 22 | TCP | SSH (administración remota) |
| 53 | TCP/UDP | DNS |
| 3389 | TCP | RDP (escritorio remoto Windows) |

### Modelo OSI simplificado

Podemos resumir el modelo OSI en 5 capas con una analogía postal:

| Capa | Función | Analogía |
|------|---------|----------|
| Aplicación | El dato que el usuario usa (web, correo) | El contenido de la carta |
| Transporte | TCP/UDP: controla que llegue entero | El correo certificado |
| Red | IP: elige el camino y la dirección | El número y la calle |
| Enlace | MAC: entrega al vecino directo | El cartero que toca la puerta |
| Física | Cables, fibra, WiFi | La ruta física de la camioneta |

---

## 12. Errores comunes del principiante (resumen)

- ☐ Máscaras mal calculadas (no restar los 2 hosts).
- ☐ Subredes superpuestas (dos segmentos comparten direcciones).
- ☐ Olvidar configurar el gateway en equipos nuevos.
- ☐ DNS apuntando a una IP equivocada.
- ☐ Confundir IP privada con IP pública.
- ☐ Mezclar rangos estáticos con el rango del DHCP.
- ☐ Dejar todo en una sola VLAN "porque es más fácil".
- ☐ Anotar IPs de memoria sin respaldarlas en el inventario (ID-01).

---

## 13. Relación con el kit Banco-Inicia

| Documento | Cómo ayuda este módulo |
|-----------|------------------------|
| ID-01 (Inventario de Activos) | Registrar cada equipo con su IP, subred y VLAN correctas |
| ID-02 / ID-03 (Riesgos) | Identificar riesgos: segmentación inexistente, DMZ mal configurada, gateway sin proteger |
| PR-04 (Seguridad Física) | Los racks y armarios de Casa Central y sucursales alojan switches y routers; hay que saber qué hay dentro |
| GV-02 (Alcance del SGSI) | Definir qué redes y sistemas quedan dentro del alcance |
| URCDP-01 (Documento de Seguridad) | Llenar la sección de "sistemas y redes" con datos correctos |
| MATRIZ-001 | Los fundamentos permiten completar la matriz de aplicaciones/activos |

---

## 14. Glosario rápido

| Término | Significado simple |
|---------|--------------------|
| IP | Matrícula de un dispositivo en la red |
| Subred | Barrio dentro de la red |
| Máscara | Línea que delimita el barrio |
| CIDR | Forma corta de escribir la máscara (`/24`) |
| Gateway | Salida del barrio hacia afuera |
| DNS | Agenda que convierte nombres en IPs |
| DHCP | Portero que asigna IPs automáticamente |
| VLAN | División lógica del tráfico sin cables nuevos |
| NAT | Traductor de IPs privadas a públicas |
| Puerto | Puerta de entrada/salida del dispositivo |
| Broadcast | Aviso que se envía a todos los vecinos |

---

**Documentos relacionados:** GV-01, GV-02, ID-01, ID-02, ID-03, PR-04, URCDP-01, MATRIZ-001
