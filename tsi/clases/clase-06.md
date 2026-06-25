# Clase 6: Direccionamiento IP y Subredes (Subnetting)

**Duracion:** 2 horas

---

## Objetivos de Aprendizaje

1. Comprender el formato y estructura de las direcciones IPv4 y su representacion binaria/decimal
2. Dominar el calculo de mascaras de subred, direcciones de red y broadcast
3. Aplicar subnetting y VLSM para disenar esquemas de direccionamiento eficientes
4. Disenar esquemas de direccionamiento IP para escenarios reales con diferentes requerimientos

---

## Contenido Detallado

### 1. Direccion IPv4

Una direccion IPv4 es un numero de 32 bits que identifica de forma unica un dispositivo en una red IP. Se divide en 4 grupos de 8 bits llamados **octetos**.

**Analogia:** Una direccion IP es como la direccion de tu casa. Tiene una parte que identifica tu calle (red) y otra que identifica tu casa especifica (host).

#### Formato y representacion

- **Binario:** 32 bits: `11000000.10101000.00000001.00000001`
- **Decimal:** 4 octetos separados por puntos: `192.168.1.1`
- Cada octeto va de 0 a 255 (porque 8 bits permiten 2^8 = 256 valores: 0 a 255)

**Tabla de valores de bits por posicion en un octeto:**

| Bit 7 | Bit 6 | Bit 5 | Bit 4 | Bit 3 | Bit 2 | Bit 1 | Bit 0 |
|-------|-------|-------|-------|-------|-------|-------|-------|
| 128   | 64    | 32    | 16    | 8     | 4     | 2     | 1     |

**Ejemplo de conversion binario a decimal:**

Para convertir `11000000` a decimal:
```
1*128 + 1*64 + 0*32 + 0*16 + 0*8 + 0*4 + 0*2 + 0*1
= 128 + 64 = 192
```

Para convertir `192` a binario:
```
192 / 2 = 96  residuo 0
 96 / 2 = 48  residuo 0
 48 / 2 = 24  residuo 0
 24 / 2 = 12  residuo 0
 12 / 2 = 6   residuo 1
  6 / 2 = 3   residuo 0
  3 / 2 = 1   residuo 1
  1 / 2 = 0   residuo 1
Leer residuos de abajo arriba: 11000000
```

#### Clases de direcciones (Clasful Addressing)

Originalmente, las IPs se dividian en clases segun el primer octeto:

| Clase | Primer octeto | Bits inicio | Mascara por defecto | Rango | Uso |
|-------|---------------|-------------|---------------------|-------|-----|
| A | 0-127 | 0 | /8 (255.0.0.0) | 0.0.0.0 - 127.255.255.255 | Grandes redes (16M hosts/red) |
| B | 128-191 | 10 | /16 (255.255.0.0) | 128.0.0.0 - 191.255.255.255 | Redes medianas (65K hosts/red) |
| C | 192-223 | 110 | /24 (255.255.255.0) | 192.0.0.0 - 223.255.255.255 | Redes pequeñas (254 hosts/red) |
| D | 224-239 | 1110 | N/A | 224.0.0.0 - 239.255.255.255 | Multicast |
| E | 240-255 | 1111 | N/A | 240.0.0.0 - 255.255.255.255 | Experimental |

Hoy en dia se usa **CIDR** (Classless Inter-Domain Routing) que no depende de las clases, pero es importante conocerlas historicamente.

#### Direcciones publicas vs privadas

Las direcciones **privadas** NO se enrutan en Internet. Se usan dentro de redes locales. Los rangos son:

| Rango privado | Clase equivalente | Cantidad de IPs |
|---------------|-------------------|------------------|
| 10.0.0.0 - 10.255.255.255 | Una clase A | 16,777,216 |
| 172.16.0.0 - 172.31.255.255 | 16 clases B | 1,048,576 |
| 192.168.0.0 - 192.168.255.255 | 256 clases C | 65,536 |

Las direcciones **publicas** son unicas en Internet y deben ser asignadas por un proveedor (ISP o autoridad de registro).

**Analogia:** Las IPs privadas son como los numeros de extension interna de una empresa (marcas 101, 102...). La IP publica es el numero principal de la empresa. Cuando llamas desde afuera, marcas el numero principal y ellos te transfieren a la extension.

#### Tipos especiales de direcciones

- **Loopback:** 127.0.0.1 (localhost) - Representa tu propia computadora. Sirve para probar servicios localmente.
- **Broadcast:** La ultima direccion de cada red. Envia datos a TODOS los dispositivos de la red. Ej: para 192.168.1.0/24, broadcast = 192.168.1.255.
- **Multicast:** 224.0.0.0 - 239.255.255.255 - Envia datos a un grupo especifico de dispositivos.
- **Link-Local:** 169.254.0.0/16 - Auto-asignada cuando no hay DHCP disponible.

### 2. Mascara de subred

La mascara de subred es un numero de 32 bits que indica que parte de una direccion IP identifica la RED y que parte identifica el HOST.

**Analogia:** La mascara de subred es como un filtro que separa el codigo postal (red) del numero de casa (host). Con la misma mascara, sabes cuantas casas hay en esa calle.

- Los bits de la mascara en **1** indican la parte de RED
- Los bits de la mascara en **0** indican la parte de HOST

#### Notacion decimal y CIDR

| Notacion decimal | Notacion CIDR | Binario | Cantidad de hosts utiles |
|------------------|---------------|---------|--------------------------|
| 255.0.0.0 | /8 | 11111111.00000000.00000000.00000000 | 16,777,214 |
| 255.255.0.0 | /16 | 11111111.11111111.00000000.00000000 | 65,534 |
| 255.255.255.0 | /24 | 11111111.11111111.11111111.00000000 | 254 |
| 255.255.255.128 | /25 | 11111111.11111111.11111111.10000000 | 126 |
| 255.255.255.192 | /26 | 11111111.11111111.11111111.11000000 | 62 |
| 255.255.255.224 | /27 | 11111111.11111111.11111111.11100000 | 30 |
| 255.255.255.240 | /28 | 11111111.11111111.11111111.11110000 | 14 |
| 255.255.255.248 | /29 | 11111111.11111111.11111111.11111000 | 6 |
| 255.255.255.252 | /30 | 11111111.11111111.11111111.11111100 | 2 |
| 255.255.255.254 | /31 | 11111111.11111111.11111111.11111110 | 0 (enlaces p2p) |
| 255.255.255.255 | /32 | 11111111.11111111.11111111.11111111 | 1 (host unico) |

**Formula de hosts utiles:** `2^n - 2` donde `n` = cantidad de bits de host (los que estan en 0).

Se resta 2 porque la primera direccion del rango es la **direccion de red** y la ultima es el **broadcast**. Ambas no se asignan a dispositivos.

**Ejemplo:** Mascara /24: bits de host = 32 - 24 = 8 bits -> 2^8 - 2 = 254 hosts utiles.
Mascara /28: bits de host = 32 - 28 = 4 bits -> 2^4 - 2 = 14 hosts utiles.

#### Como calcular la direccion de red

La direccion de red se obtiene haciendo AND logico entre la IP y la mascara de subred.

**Regla AND:**
- 1 AND 1 = 1
- 1 AND 0 = 0
- 0 AND 1 = 0
- 0 AND 0 = 0

**Ejemplo:** IP 192.168.1.37 con mascara 255.255.255.224 (/27)

```
IP:       11000000.10101000.00000001.00100101   (192.168.1.37)
Mascara:  11111111.11111111.11111111.11100000   (255.255.255.224)
AND:      -----------------------------------
Red:      11000000.10101000.00000001.00100000   (192.168.1.32)
```

La direccion de red es **192.168.1.32**.

**Broadcast:** Se calcula poniendo todos los bits de host en 1:

```
Red:      11000000.10101000.00000001.00100000   (192.168.1.32)
Bits host:                              ^^^^^   (5 bits)
Broadcast:11000000.10101000.00000001.00111111   (192.168.1.47)
```

**Rango util de hosts:** Desde red + 1 hasta broadcast - 1 = 192.168.1.33 a 192.168.1.46 (14 hosts).

### 3. Subnetting (Creacion de subredes)

Subnetting es el proceso de dividir una red grande en redes mas pequeñas (subredes).

**Por que hacer subnetting?**
- **Organizacion:** Separar departamentos en diferentes subredes
- **Seguridad:** Aislar trafico entre areas (Ventas no ve trafico de RRHH)
- **Rendimiento:** Reducir el dominio de colisiones y broadcast
- **Optimizacion:** Usar las direcciones IP de forma mas eficiente

**Analogia:** Tienes un terreno grande (red /24 con 254 direcciones) y quieres construir 4 casas (subredes) separadas con sus propias direcciones. El subnetting es como dividir el terreno en lotes mas pequeños.

#### Proceso paso a paso para crear subredes del mismo tamano

**Ejemplo completo:** Dividir 192.168.1.0/24 en 4 subredes.

**Paso 1: Determinar cuantos bits de subred se necesitan**

Para N subredes, necesitamos `m` bits donde `2^m >= N`.
Para 4 subredes: 2^2 = 4. Necesitamos 2 bits de subred.

**Paso 2: Calcular la nueva mascara**

Mascara original: /24 (255.255.255.0) = 24 bits de red
Bits de subred que tomamos: 2 bits de la parte de host
Nueva mascara: 24 + 2 = /26 (255.255.255.192)

**Paso 3: Calcular el incremento (salto entre subredes)**

El incremento es el valor del bit menos significativo de la subred.
Bits de host restantes: 32 - 26 = 6 bits
Incremento: 2^6 = 64 (en el ultimo octeto)
O tambien: 256 - 192 = 64 (donde 192 es el valor del ultimo octeto de la mascara)

**Paso 4: Calcular cada subred**

| Subred | Direccion de red | Primer host | Ultimo host | Broadcast | Mascara |
|--------|------------------|-------------|-------------|-----------|---------|
| 0 | 192.168.1.0 | 192.168.1.1 | 192.168.1.62 | 192.168.1.63 | /26 |
| 1 | 192.168.1.64 | 192.168.1.65 | 192.168.1.126 | 192.168.1.127 | /26 |
| 2 | 192.168.1.128 | 192.168.1.129 | 192.168.1.190 | 192.168.1.191 | /26 |
| 3 | 192.168.1.192 | 192.168.1.193 | 192.168.1.254 | 192.168.1.255 | /26 |

**Verificacion:** Cada subred tiene 2^6 - 2 = 62 hosts utiles. Total: 4 * 62 = 248 hosts (se pierden 6 direcciones por las 4 direcciones de red y 4 broadcasts, pero las direcciones de red y broadcast de la red original ya no existen como tales).

**Diagrama visual de las subredes:**

```
192.168.1.0/24 (red original)
+------------------------------------------------------------------+
|  Subred 0 (/26)  |  Subred 1 (/26)  |  Subred 2 (/26)  |  Subred 3 (/26)  |
|  .0 - .63         |  .64 - .127      |  .128 - .191     |  .192 - .255     |
|  Hosts: .1 - .62  |  Hosts: .65-.126 |  Hosts: .129-.190|  Hosts: .193-.254|
+------------------------------------------------------------------+
```

### 4. VLSM (Variable Length Subnet Mask)

VLSM permite crear subredes de DIFERENTE tamano dentro de una misma red. A diferencia del subnetting fijo (donde todas las subredes tienen la misma mascara), VLSM asigna mascaras segun la necesidad especifica de cada segmento.

**Analogia:** En vez de dividir tu terreno en 4 lotes iguales (subnetting fijo), VLSM te permite hacer lotes de diferentes tamanos: uno grande para la casa principal, uno mediano para el jardin, uno pequeño para el garage.

#### Proceso paso a paso VLSM

**Escenario real:** Una empresa tiene 5 departamentos con diferentes necesidades de hosts:

| Departamento | Hosts necesarios |
|--------------|-----------------:|
| Ventas | 50 |
| RRHH | 25 |
| IT | 10 |
| Gerencia | 5 |
| Invitados (WiFi) | 2 |

Red base: 192.168.1.0/24

**Paso 1: Ordenar los departamentos de MAYOR a MENOR cantidad de hosts**

1. Ventas: 50 hosts
2. RRHH: 25 hosts
3. IT: 10 hosts
4. Gerencia: 5 hosts
5. Invitados: 2 hosts

**Paso 2: Para cada departamento, calcular la mascara necesaria**

La regla es: para `h` hosts, necesitamos el menor `n` (bits de host) tal que `2^n - 2 >= h`.

| Depto | Hosts | Bits host (n) | 2^n - 2 >= h | Mascara CIDR | Mascara decimal |
|-------|------:|:-------------:|:------------:|:------------:|:---------------:|
| Ventas | 50 | 6 | 2^6-2 = 62 >= 50 | /26 | 255.255.255.192 |
| RRHH | 25 | 5 | 2^5-2 = 30 >= 25 | /27 | 255.255.255.224 |
| IT | 10 | 4 | 2^4-2 = 14 >= 10 | /28 | 255.255.255.240 |
| Gerencia | 5 | 3 | 2^3-2 = 6 >= 5 | /29 | 255.255.255.248 |
| Invitados | 2 | 2 | 2^2-2 = 2 >= 2 | /30 | 255.255.255.252 |

**Paso 3: Asignar rangos secuencialmente empezando desde la direccion base**

Empezamos desde 192.168.1.0 y vamos asignando bloques.

**Subred 1 - Ventas (/26):** 64 direcciones (0-63)
- Red: 192.168.1.0/26
- Primer host: 192.168.1.1
- Ultimo host: 192.168.1.62
- Broadcast: 192.168.1.63

**Subred 2 - RRHH (/27):** 32 direcciones (64-95)
- Red: 192.168.1.64/27
- Primer host: 192.168.1.65
- Ultimo host: 192.168.1.94
- Broadcast: 192.168.1.95

**Subred 3 - IT (/28):** 16 direcciones (96-111)
- Red: 192.168.1.96/28
- Primer host: 192.168.1.97
- Ultimo host: 192.168.1.110
- Broadcast: 192.168.1.111

**Subred 4 - Gerencia (/29):** 8 direcciones (112-119)
- Red: 192.168.1.112/29
- Primer host: 192.168.1.113
- Ultimo host: 192.168.1.118
- Broadcast: 192.168.1.119

**Subred 5 - Invitados (/30):** 4 direcciones (120-123)
- Red: 192.168.1.120/30
- Primer host: 192.168.1.121
- Ultimo host: 192.168.1.122
- Broadcast: 192.168.1.123

**Nota:** Sobran direcciones desde 192.168.1.124 a 192.168.1.255 para crecimiento futuro.

**Tabla resumen VLSM:**

```
Red base: 192.168.1.0/24
+-------------+--------+----------+-----------------+-----------------+
| Depto       | Hosts  | Mascara  | Rango           | Uso             |
+-------------+--------+----------+-----------------+-----------------+
| Ventas      | 50     | /26      | .0 - .63        | .1 - .62 hosts  |
| RRHH        | 25     | /27      | .64 - .95       | .65 - .94 hosts |
| IT          | 10     | /28      | .96 - .111      | .97 - .110 hosts|
| Gerencia    | 5      | /29      | .112 - .119     | .113 - .118 hst |
| Invitados   | 2      | /30      | .120 - .123     | .121 - .122 hst |
| Reserva     | -      | -        | .124 - .255     | Crecimiento     |
+-------------+--------+----------+-----------------+-----------------+
```

**Diagrama visual VLSM:**

```
192.168.1.0/24
+-------+------+------+------+------+------+------------------------+
|VENTAS | RRHH |  IT  | GER  | INV  |      RESERVA                |
| /26   | /27  | /28  | /29  | /30  |                             |
| 62 h  | 30 h | 14 h | 6 h  | 2 h  |                             |
+-------+------+------+------+------+------------------------+
.0     .64   .96   .112  .120  .124                      .255
```

### 5. CIDR (Classless Inter-Domain Routing)

CIDR reemplazo el sistema de clases (A, B, C) por un sistema sin clase donde la mascara puede ser cualquier valor. Esto permitio:

- **Uso mas eficiente de direcciones:** Antes, si necesitabas 300 direcciones, te daban una clase B (65,534 IPs) y desperdiciabas miles. Con CIDR, puedes obtener un /23 (510 IPs).
- **Agregacion de rutas (route aggregation / supernetting):** Varias redes consecutivas se pueden resumir en una sola ruta.

**Ejemplo de supernetting:**

Si tienes 4 redes /24 consecutivas:
- 192.168.0.0/24
- 192.168.1.0/24
- 192.168.2.0/24
- 192.168.3.0/24

Se pueden resumir en una sola ruta: **192.168.0.0/22**

Esto se llama **route aggregation** y reduce el tamano de las tablas de enrutamiento en Internet.

**Como calcular la ruta resumida:**
1. Escribir las 4 direcciones de red en binario
2. Encontrar donde coinciden todos los bits
3. Contar los bits coincidentes = mascara de la superred

```
192.168.0.0: 11000000.10101000.000000|00.00000000
192.168.1.0: 11000000.10101000.000000|01.00000000
192.168.2.0: 11000000.10101000.000000|10.00000000
192.168.3.0: 11000000.10101000.000000|11.00000000
                                     ^^
                               Coinciden 22 bits -> /22
```

---

## Ejercicio 1: Conversion Binario/Decimal

**Enunciado:** Convierte las siguientes direcciones IP:

a) De binario a decimal: `11000000.10101000.00001010.00000001`
b) De binario a decimal: `10101100.00010000.00000001.00000001`
c) De decimal a binario: `10.0.0.1`
d) De decimal a binario: `172.16.5.100`
e) De binario a decimal: `11111111.11111111.11111111.11111000`

### Solucion

**a) 11000000.10101000.00001010.00000001 -> decimal**

```
11000000 = 1*128 + 1*64 + 0*32 + 0*16 + 0*8 + 0*4 + 0*2 + 0*1 = 192
10101000 = 1*128 + 0*64 + 1*32 + 0*16 + 1*8 + 0*4 + 0*2 + 0*1 = 168
00001010 = 0*128 + 0*64 + 0*32 + 0*16 + 1*8 + 0*4 + 1*2 + 0*1 = 10
00000001 = 0*128 + 0*64 + 0*32 + 0*16 + 0*8 + 0*4 + 0*2 + 1*1 = 1

Resultado: 192.168.10.1
```

**b) 10101100.00010000.00000001.00000001 -> decimal**

```
10101100 = 128+0+32+0+8+4+0+0 = 172
00010000 = 0+0+0+16+0+0+0+0 = 16
00000001 = 0+0+0+0+0+0+0+1 = 1
00000001 = 0+0+0+0+0+0+0+1 = 1

Resultado: 172.16.1.1
```

**c) 10.0.0.1 -> binario**

```
10: 10/2=5 r0, 5/2=2 r1, 2/2=1 r0, 1/2=0 r1 -> 00001010
0: 00000000
0: 00000000
1: 00000001

Resultado: 00001010.00000000.00000000.00000001
```

**d) 172.16.5.100 -> binario**

```
172: 172/2=86 r0, 86/2=43 r0, 43/2=21 r1, 21/2=10 r1, 10/2=5 r0, 5/2=2 r1, 2/2=1 r0, 1/2=0 r1 -> 10101100
16: 16/2=8 r0, 8/2=4 r0, 4/2=2 r0, 2/2=1 r0, 1/2=0 r1 -> 00010000
5: 5/2=2 r1, 2/2=1 r0, 1/2=0 r1 -> 00000101
100: 100/2=50 r0, 50/2=25 r0, 25/2=12 r1, 12/2=6 r0, 6/2=3 r0, 3/2=1 r1, 1/2=0 r1 -> 01100100

Resultado: 10101100.00010000.00000101.01100100
```

**e) 11111111.11111111.11111111.11111000 -> decimal**

```
11111111 = 255
11111111 = 255
11111111 = 255
11111000 = 128+64+32+16+8+0+0+0 = 248

Resultado: 255.255.255.248 (mascara /29)
```

---

## Ejercicio 2: Subnetting basico

**Enunciado:** Dada la red 172.16.0.0/16, crear 8 subredes del mismo tamano. Calcular para cada subred: direccion de red, broadcast, rango util de hosts, y mascara.

### Solucion

**Paso 1: Bits necesarios para 8 subredes**

2^m >= 8 -> m = 3 (2^3 = 8)

**Paso 2: Nueva mascara**

Original: /16 (255.255.0.0)
Nueva: 16 + 3 = /19 (255.255.224.0)

**Paso 3: Calculo del incremento**

Bits de host restantes: 32 - 19 = 13 bits
Incremento: 2^13 = 8192 (en el tercer octeto, porque ahi estan los bits de subred)
O tambien: 256 - 224 = 32 en el tercer octeto -> 32 * 256 = 8192 (verificacion)

El incremento por subred en el tercer octeto es de 32 (cada subred salta 32 en el tercer octeto):

**Paso 4: Tabla de las 8 subredes**

| Subred | Direccion de red | Primer host | Ultimo host | Broadcast |
|--------|------------------|-------------|-------------|-----------|
| 0 | 172.16.0.0/19 | 172.16.0.1 | 172.16.31.254 | 172.16.31.255 |
| 1 | 172.16.32.0/19 | 172.16.32.1 | 172.16.63.254 | 172.16.63.255 |
| 2 | 172.16.64.0/19 | 172.16.64.1 | 172.16.95.254 | 172.16.95.255 |
| 3 | 172.16.96.0/19 | 172.16.96.1 | 172.16.127.254 | 172.16.127.255 |
| 4 | 172.16.128.0/19 | 172.16.128.1 | 172.16.159.254 | 172.16.159.255 |
| 5 | 172.16.160.0/19 | 172.16.160.1 | 172.16.191.254 | 172.16.191.255 |
| 6 | 172.16.192.0/19 | 172.16.192.1 | 172.16.223.254 | 172.16.223.255 |
| 7 | 172.16.224.0/19 | 172.16.224.1 | 172.16.255.254 | 172.16.255.255 |

**Verificacion:** Cada subred tiene 2^13 - 2 = 8190 hosts utiles. 8 * 8190 = 65,520 hosts (menos que los 65,534 originales porque se pierden las direcciones de red y broadcast de cada subred).

**Explicacion detallada de la subred 0:**

Red: 172.16.0.0/19
- Mascara binario: 11111111.11111111.11100000.00000000
- Bits de red: 172.16 (fijos)
- Bits de subred: primeros 3 bits del tercer octeto (000)
- Bits de host: ultimos 5 bits del tercer octeto + todo el cuarto octeto = 13 bits

```
172.16.0.0:  10101100.00010000.000|00000.00000000
Mascara /19: 11111111.11111111.111|00000.00000000
La barra | separa los bits de subred de los de host

Broadcast: poner todos los bits de host en 1:
            10101100.00010000.000|11111.11111111 = 172.16.31.255
```

---

## Ejercicio 3: VLSM

**Enunciado:** Una empresa tiene 4 departamentos con las siguientes necesidades:

| Departamento | Hosts necesarios |
|--------------|:----------------:|
| Ventas | 50 |
| RRHH | 25 |
| IT | 10 |
| Gerencia | 5 |

Red base: 192.168.1.0/24. Disenar el esquema VLSM.

### Solucion

**Paso 1: Ordenar de mayor a menor necesidad**

1. Ventas: 50 hosts
2. RRHH: 25 hosts
3. IT: 10 hosts
4. Gerencia: 5 hosts

**Paso 2: Calcular mascaras**

| Depto | Hosts | Bits host (n) | 2^n - 2 | Mascara |
|-------|------:|:-------------:|:-------:|:-------:|
| Ventas | 50 | 6 | 62 >= 50 | /26 (255.255.255.192) |
| RRHH | 25 | 5 | 30 >= 25 | /27 (255.255.255.224) |
| IT | 10 | 4 | 14 >= 10 | /28 (255.255.255.240) |
| Gerencia | 5 | 3 | 6 >= 5 | /29 (255.255.255.248) |

**Paso 3: Asignar rangos empezando desde 192.168.1.0**

**Subred 1 - Ventas (/26):** Incremento = 2^6 = 64
- Red: 192.168.1.0/26
- Rango: 192.168.1.0 - 192.168.1.63
- Hosts: 192.168.1.1 a 192.168.1.62
- Broadcast: 192.168.1.63

**Subred 2 - RRHH (/27):** Incremento = 2^5 = 32, empezando en 64
- Red: 192.168.1.64/27
- Rango: 192.168.1.64 - 192.168.1.95
- Hosts: 192.168.1.65 a 192.168.1.94
- Broadcast: 192.168.1.95

**Subred 3 - IT (/28):** Incremento = 2^4 = 16, empezando en 96
- Red: 192.168.1.96/28
- Rango: 192.168.1.96 - 192.168.1.111
- Hosts: 192.168.1.97 a 192.168.1.110
- Broadcast: 192.168.1.111

**Subred 4 - Gerencia (/29):** Incremento = 2^3 = 8, empezando en 112
- Red: 192.168.1.112/29
- Rango: 192.168.1.112 - 192.168.1.119
- Hosts: 192.168.1.113 a 192.168.1.118
- Broadcast: 192.168.1.119

**Tabla resumen:**

```
192.168.1.0/24
+-----------+--------+---------+-------------+---------------------+-------------------+
| Depto     | Hosts  | Mascara | Red         | Rango hosts         | Broadcast         |
+-----------+--------+---------+-------------+---------------------+-------------------+
| Ventas    | 50     | /26     | .0          | .1 - .62            | .63               |
| RRHH      | 25     | /27     | .64         | .65 - .94           | .95               |
| IT        | 10     | /28     | .96         | .97 - .110          | .111              |
| Gerencia  | 5      | /29     | .112        | .113 - .118         | .119              |
| Disponible| -      | -       | .120        | .121 - .254         | .255              |
+-----------+--------+---------+-------------+---------------------+-------------------+
```

**Verificacion de eficiencia:**

Sin VLSM (subnetting fijo en /26 para todos):
- 4 subredes * 62 hosts = 248 hosts disponibles
- Se necesitan: 50 + 25 + 10 + 5 = 90 hosts
- Desperdicio: 248 - 90 = 158 IPs desperdiciadas (63.7%)

Con VLSM:
- Hosts asignados: 62 + 30 + 14 + 6 = 112 hosts disponibles
- Se necesitan: 90 hosts
- Desperdicio: 112 - 90 = 22 IPs desperdiciadas (19.6%)
- Ahorro de 136 IPs comparado con subnetting fijo

**Diagrama de asignacion:**

```
192.168.1.0/24
0        64       96      112    120                   255
+---------+--------+--------+------+-------------------+
| VENTAS  | RRHH   |  IT    | GER  |   DISPONIBLE      |
| /26 62h | /27 30h|/28 14h |/29 6h|                   |
+---------+--------+--------+------+-------------------+
```

---

## Ejercicio 4: Diseno de red para universidad

**Enunciado:** Una universidad tiene 3 edificios. Cada edificio necesita:
- Edificio A: 200 hosts
- Edificio B: 100 hosts
- Edificio C: 50 hosts

Red base: 10.0.0.0/16. Disenar subredes eficientes usando VLSM.

### Solucion

**Paso 1: Ordenar por necesidad**

1. Edificio A: 200 hosts
2. Edificio B: 100 hosts
3. Edificio C: 50 hosts

**Paso 2: Calcular mascaras**

| Edificio | Hosts | Bits host | Calculo | Mascara |
|----------|:-----:|:---------:|:-------:|:-------:|
| A | 200 | 8 | 2^8-2=254 >= 200 | /24 (255.255.255.0) |
| B | 100 | 7 | 2^7-2=126 >= 100 | /25 (255.255.255.128) |
| C | 50 | 6 | 2^6-2=62 >= 50 | /26 (255.255.255.192) |

**Paso 3: Asignar rangos desde 10.0.0.0/16**

**Subred A - /24:** El incremento es 1 en el tercer octeto (2^8 = 256 en el ultimo octeto)
- Red: 10.0.0.0/24
- Rango: 10.0.0.0 - 10.0.0.255
- Hosts: 10.0.0.1 a 10.0.0.254
- Broadcast: 10.0.0.255

**Subred B - /25:** El incremento es 128 en el ultimo octeto, empezando en 10.0.1.0
- Red: 10.0.1.0/25
- Rango: 10.0.1.0 - 10.0.1.127
- Hosts: 10.0.1.1 a 10.0.1.126
- Broadcast: 10.0.1.127

**Subred C - /26:** El incremento es 64 en el ultimo octeto, empezando en 10.0.1.128
- Red: 10.0.1.128/26
- Rango: 10.0.1.128 - 10.0.1.191
- Hosts: 10.0.1.129 a 10.0.1.190
- Broadcast: 10.0.1.191

**Tabla resumen:**

| Edificio | Hosts | Mascara | Red | Rango hosts | Broadcast | Uso |
|----------|:-----:|:-------:|-----|-------------|-----------|-----|
| A | 200 | /24 | 10.0.0.0 | 10.0.0.1 - 10.0.0.254 | 10.0.0.255 | Red principal |
| B | 100 | /25 | 10.0.1.0 | 10.0.1.1 - 10.0.1.126 | 10.0.1.127 | Segundo edificio |
| C | 50 | /26 | 10.0.1.128 | 10.0.1.129 - 10.0.1.190 | 10.0.1.191 | Tercer edificio |
| Libre | - | - | 10.0.1.192 | 10.0.1.193 - 10.0.255.254 | 10.0.255.255 | Futura expansion |
| Libre | - | - | 10.0.2.0 | 10.0.2.1 - 10.0.255.254 | 10.0.255.255 | Mas espacio |

**Diagrama de asignacion:**

```
10.0.0.0/16
+------------+-----------------+-----------------+---------------------------+
| EDIF A     | EDIF B          | EDIF C          |  LIBRE PARA EXPANSION     |
| /24 (254h) | /25 (126h)      | /26 (62h)       |                           |
| 10.0.0.0   | 10.0.1.0        | 10.0.1.128      | 10.0.1.192 - 10.0.255.255|
+------------+-----------------+-----------------+---------------------------+

Espacio libre total: 10.0.2.0/16 - 10.0.1.192 = ~65,000 IPs disponibles
```

**Verificacion de que cabe en la red base /16:**

La red base 10.0.0.0/16 abarca desde 10.0.0.0 hasta 10.0.255.255.
Nuestras subredes usan: 10.0.0.0 - 10.0.1.191 (menos de 2 de los 256 posibles /24). Cabe sobradamente.

---

## Preguntas y Respuestas

### Pregunta 1
**Cual es la diferencia entre una direccion IP publica y una privada?**

**Respuesta:** Una direccion IP **publica** es unica en todo Internet y debe ser asignada por un ISP o autoridad de registro (IANA/RIR). Los routers en Internet saben como llegar a ella. Una direccion IP **privada** solo es valida dentro de una red local y NO se enruta en Internet. Los rangos privados son 10.0.0.0/8, 172.16.0.0/12, y 192.168.0.0/16. Los dispositivos con IP privada acceden a Internet a traves de NAT (Network Address Translation) en el router, que traduce la IP privada a la IP publica del router. Es como en un edificio de oficinas: tienes una direccion postal publica (la del edificio) y numeros de extension internos (privados) que solo funcionan dentro del edificio.

### Pregunta 2
**Que significa la notacion /24 en una direccion IP como 192.168.1.0/24?**

**Respuesta:** La notacion /24 es la notacion **CIDR** que indica cuantos bits de la direccion IP corresponden a la parte de **red** (los primeros 24 bits). El resto (32 - 24 = 8 bits) corresponden a la parte de **host**. Equivale a la mascara de subred 255.255.255.0. /24 significa que los primeros 3 octetos identifican la red y el ultimo octeto identifica los hosts. Una red /24 tiene 2^8 - 2 = 254 direcciones utiles para hosts. Cuanto mayor es el numero despues de la barra, mas bits son de red y menos hosts disponibles. /8 = 16M hosts, /16 = 65K hosts, /24 = 254 hosts, /30 = 2 hosts.

### Pregunta 3
**Cuantos hosts utiles tiene una red /28?**

**Respuesta:** Una red /28 tiene 32 - 28 = 4 bits para hosts. La cantidad de direcciones totales es 2^4 = 16. Se resta 2 (direccion de red y broadcast), entonces 16 - 2 = **14 hosts utiles**. La mascara es 255.255.255.240. El incremento entre subredes /28 es de 16. Por ejemplo, las subredes /28 dentro de 192.168.1.0/24 serian: .0-.15, .16-.31, .32-.47, etc.

### Pregunta 4
**Para que sirve la mascara de subred?**

**Respuesta:** La mascara de subred sirve para **separar la parte de red de la parte de host** en una direccion IP. Se usa para:
1. **Determinar la direccion de red:** Haciendo AND logico entre la IP y la mascara, obtenemos la red a la que pertenece el dispositivo.
2. **Saber si dos dispositivos estan en la misma red:** Si dos IPs con sus mascaras dan la misma direccion de red, estan en la misma red local y pueden comunicarse directamente. Si no, necesitan un router.
3. **Definir el tamano de la red:** La mascara determina cuantos hosts caben en esa red.
4. **Segmentar redes:** Permite crear subredes mas pequeñas a partir de una red grande.

Sin la mascara de subred, un dispositivo no podria saber si debe enviar un paquete directamente a otro dispositivo (switch) o si debe enviarlo al router para que lo enrute a otra red.

### Pregunta 5
**Que es la direccion de broadcast y como se calcula?**

**Respuesta:** La direccion de broadcast es una direccion especial que permite enviar un paquete a **TODOS** los dispositivos de una red. Cuando envias un paquete a esta direccion, todos los dispositivos de esa red lo reciben. Se calcula poniendo todos los bits de host en 1 (binario) dentro de la direccion de red. Ejemplo: para la red 192.168.1.0/26 (mascara 255.255.255.192):
- Bits de host: 32 - 26 = 6 bits
- Red: 192.168.1.0 = 11000000.10101000.00000001.00000000
- Host bits en 1: 11000000.10101000.00000001.00111111 = 192.168.1.63
Alternativamente: broadcast = direccion de red + (2^n - 1) donde n = bits de host. Para /26: 0 + (64 - 1) = 63. La direccion de broadcast es 192.168.1.63.

### Pregunta 6 (Adicional)
**Que es NAT y por que se usa con direcciones privadas?**

**Respuesta:** NAT (Network Address Translation) es un proceso en el router que traduce las direcciones IP privadas de los dispositivos internos a una direccion IP publica (o un conjunto de ellas) para acceder a Internet. Cuando un dispositivo con IP privada (ej: 192.168.1.10) quiere acceder a Internet, el router:
1. Cambia la IP origen privada por la IP publica del router
2. Cambia el puerto origen para identificar a que dispositivo devolver la respuesta
3. Mantiene una tabla de traduccion para saber a quien devolver cada respuesta
Esto permite que cientos de dispositivos compartan una sola IP publica, solucionando el problema de escasez de direcciones IPv4.

---

## Tarea / Lectura Recomendada

1. **Leer:** "IP Subnetting" de Todd Lammle (capitulos en cualquier libro de redes CCNA)
2. **Practicar:** Usar la herramienta online "Subnet Calculator" (https://www.subnet-calculator.com/) para verificar tus calculos
3. **Practicar:** En tu computadora, ejecuta `ipconfig /all` y determina tu direccion IP, mascara, red, broadcast y puerta de enlace
4. **Practicar:** Resolver al menos 10 ejercicios de subnetting de diferentes tamanos (sitios como subnetting.org o subnettingpractice.com)
5. **Practicar:** Calcular a mano las subredes para 10.0.0.0/8 en 32 subredes, y verificar con calculadora online
6. **Leer:** RFC 4632 - "Classless Inter-domain Routing (CIDR): The Internet Address Assignment and Aggregation Plan"
7. **Herramienta:** Descargar "SolarWinds Subnet Calculator" (gratuita) o usar la de "TP-Link Subnet Calculator" online
