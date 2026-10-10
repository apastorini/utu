# Clase 29 — Taller de subnetting y planes de numeración

**Bloque:** D (Capa de Red) · **Semana:** 10 · **Duración estimada:** 120 min
**Correlativa:** Clase 28 (VLSM y planes de numeración) · **Sigue con:** Clase 30 (tablas de enrutamiento, next hop y ARP)
**Material de referencia:** Tanenbaum cap. 5 · RFC 1918 (privadas) 🔍 · RFC 4632 (CIDR) 🔍 · RFC 6177 · RFC 8200

> 🔍 = RFC **no verificado** en `ACTUALIZACIONES.md`: no lo cites sin confirmarlo.
> Esta clase es **de taller**: la única teoría nueva es el recuadro de fórmulas.

---

## 🎯 Al terminar esta clase vas a poder

1. Escribir de memoria las cinco fórmulas del subnetting.
2. Dividir un bloque en subredes iguales con el **prefijo más largo** que alcance.
3. Aplicar VLSM a un `/16` con cinco necesidades distintas, con la aritmética a la vista.
4. Resolver **entero** los cuatro problemas de plan de numeración que más se repiten en FING.
5. Reconstruir una topología de 6 routers desde los datos de una tabla y sacar sus tablas de enrutamiento.
6. Decidir si un conjunto de prefijos se puede **sumarizar**, y hasta dónde.

> **Prerequisito del examen:** `2011-03 Problema 2d` · `2010-12 P2a-i` · `2010-07 P2a-i` · `2006-08 Problema 1` · `2006-08 P4` · `2008-12 P2a-i`.

---

# PARTE 1 — EL RECUADRO QUE HAY QUE COPIAR AL EXAMEN

```
 ╔══════════════════════════════════════════════════════════════════════════╗
 ║  hosts necesarios H   →   2^h − 2 ≥ H   →   h = ceil(log2(H + 2))     ║
 ║  →  prefijo = 32 − h                                                      ║
 ║                                                                          ║
 ║  cantidad de subredes  =  2^(bits de host que quedan)                    ║
 ║  tamaño del bloque     =  2^(32 − prefijo)                               ║
 ║  dir. de red           =  (dir / tamaño) · tamaño     (división entera) ║
 ║  broadcast             =  dir de red + tamaño − 1                        ║
 ║  rango de hosts        =  [ dir de red + 1 ,  broadcast − 1 ]            ║
 ║  puntero de VLSM       =  primer múltiplo de "tamaño" ≥ puntero actual   ║
 ╚══════════════════════════════════════════════════════════════════════════╝
```

**Tres aclaraciones, porque son las tres trampas del examen:**

1. **El `− 2` es de red y broadcast**, no un margen de seguridad: `/27` son **30**
   utilizables, y por eso 16 direcciones pedidas **no** entran en un `/27`.
2. **`2^(32 − prefijo)` es el tamaño del bloque, no el de los hosts.** `/25` son
   128 direcciones totales; de ahí el error de creer que "alcanza para 250 hosts".
3. **El puntero se redondea hacia arriba al siguiente múltiplo del tamaño.** Si no
   sos múltiplo, perdés todo el tramo hasta el múltiplo siguiente. Por eso el paso
   1 (ordenar de mayor a menor) es obligatorio.

```
  EJEMPLO DE REDONDEO DEL PUNTERO
  puntero = 192.168.1.160,  bloque pedido /26 (tamaño 64)
    160 / 64 = 2,5   →   no es múltiplo   →   siguiente = 3 × 64 = 192
    Se pierden 32 direcciones (.160 – .191). Con un bloque /27 (32) no se pierde nada.
```

---

# PARTE 2 — EJERCICIOS DEL TALLER

## 2.1 Ejercicio 1 — `192.168.10.0/24` en cuatro subredes iguales

**Enunciado.** Dividí `192.168.10.0/24` en **cuatro** subredes iguales. Decidí
entre `/26` y `/27` y justificá.

**Paso 1 — cuántas subredes necesito.** 4 = `2^2`, o sea **2 bits** de la parte
de host hay que convertir en bits de subred.

**Paso 2 — el prefijo.** El `/24` tiene 8 bits de host. Robamos 2:

```
  prefijo = 24 + 2 = /26      (equivalente: h = 6 host bits, prefijo = 32 − 6 = 26)
  Subredes:  2^2 = 4  ✓        Tamaño: 2^(32−26) = 2^6 = 64 direcciones
  Utilizables por subred: 64 − 2 = 62      Total utilizable: 4 × 62 = 248
  Chequeo: 4 × 64 = 256 = el /24 entero  ✓
```

**Paso 3 — ¿y `/27`?** Un `/27` son `2^3 = 8` subredes de 32 direcciones
(30 utilizables cada una). O sea: `8 × 30 = 240` utilizables, repartidos en
**ocho** subredes en vez de cuatro.

```
  ┌────────────┬────────┬──────────────┬───────────────┬──────────────────────┐
  │ Opción     │ Subred │ Tam. subred   │ Utilizables   │ ¿Sirve?              │
  ├────────────┼────────┼──────────────┼───────────────┼──────────────────────┤
  │ /25        │   2    │ 128           │ 126 c/u       │ ✗ NO ALCANZA (4)     │
  │ /26        │   4    │  64           │ 62 c/u        │ ✓ la correcta       │
  │ /27        │   8    │  32           │ 30 c/u        │ ✓ pero sobre-dimensionada │
  │ /28        │  16    │  16           │ 14 c/u        │ ✓ pero 12 de sobra  │
  └────────────┴────────┴──────────────┴───────────────┴──────────────────────┘
```

**La justificación, en una frase:** el subnetting clásico **roba el mínimo número
de bits posible**, o sea usa el **prefijo más largo** que todavía produzca las
subredes pedidas.

**Con `/26` las cuatro quedan:**

```
  192.168.10.0/26    .0   – .63    red .0    | bc .63   | hosts .1   – .62
  192.168.10.64/26   .64  – .127   red .64   | bc .127  | hosts .65  – .126
  192.168.10.128/26  .128 – .191   red .128  | bc .191  | hosts .129 – .190
  192.168.10.192/26  .192 – .255   red .192  | bc .255  | hosts .193 – .254
```

**⚠️ Error típico:** elegir `/27` "porque es más chico y parece más seguro". No es
seguridad: es desperdicio.

## 2.2 Ejercicio 2 — VLSM de `172.16.0.0/16` para 500, 250, 100, 50 y 25 hosts

**Enunciado.** Del bloque `172.16.0.0/16` sacar subredes para 500, 250, 100, 50 y
25 hosts (más **1 dirección de router** en cada una). Plan alineado, cuentas de
desperdicio y mayor prefijo libre.

**Paso 1 — ordenar de mayor a menor:** 501 → 251 → 101 → 51 → 26.

**Paso 2 — los prefijos.**

```
  501:  2^8 − 2 = 254 < 501 ✗   2^9 − 2 = 510 ≥ 501 ✓  →  h = 9  →  /23  (512 dir)
  251:  2^7 − 2 = 126 < 251 ✗   2^8 − 2 = 254 ≥ 251 ✓  →  h = 8  →  /24  (256 dir)
  101:  2^6 − 2 =  62 < 101 ✗   2^7 − 2 = 126 ≥ 101 ✓  →  h = 7  →  /25  (128 dir)
   51:  2^5 − 2 =  30 <  51 ✗   2^6 − 2 =  62 ≥  51 ✓  →  h = 6  →  /26  ( 64 dir)
   26:  2^4 − 2 =  14 <  26 ✗   2^5 − 2 =  30 ≥  26 ✓  →  h = 5  →  /27  ( 32 dir)
```

⚠️ Ningún `2^h − 2` alcanza en el primer intento: en los cinco casos hay que subir
un exponente. Es lo que hace este ejercicio engañoso.

**Paso 3 — asignación con el puntero**, con la alineación verificada:

```
  puntero = 172.16.0.0

  /23  tamaño 512   inicio = 0 ✓                    →  172.16.0.0/23     puntero → 172.16.2.0
  /24  tamaño 256   inicio = 512 ✓  (512/256 = 2)   →  172.16.2.0/24     puntero → 172.16.3.0
  /25  tamaño 128   inicio = 768 ✓  (768/128 = 6)   →  172.16.3.0/25     puntero → 172.16.3.128
  /26  tamaño  64   inicio = 896 ✓  (896/64 = 14)   →  172.16.3.128/26   puntero → 172.16.3.192
  /27  tamaño  32   inicio = 960 ✓  (960/32 = 30)   →  172.16.3.192/27   puntero → 172.16.3.224

  172.16.0.0/16
  ├─  .0.0/23      500 hosts  gw 172.16.0.1     (.0.0 – .1.255)
  ├─  .2.0/24      250 hosts  gw 172.16.2.1     (.2.0 – .2.255)
  ├─  .3.0/25      100 hosts  gw 172.16.3.1     (.3.0 – .3.127)
  ├─  .3.128/26     50 hosts  gw 172.16.3.129   (.3.128 – .3.191)
  ├─  .3.192/27     25 hosts  gw 172.16.3.193   (.3.192 – .3.223)
  └─  .3.224/27 LIBRE  +  4.0/22 · 8.0/21 · 16.0/20 · 32.0/19 · 64.0/18 · 128.0/17
```

**Cuentas finales.**

```
  Consumidas:  512 + 256 + 128 + 64 + 32 = 992  de 65 536
  Libres:      65 536 − 992 = 64 544   (98,5 %)
  Desperdicio dentro de los bloques:
     (510 − 501) + (254 − 251) + (126 − 101) + (62 − 51) + (30 − 26)
       =    9   +     3    +     25    +    11   +    4    =  52
  Red + broadcast: 5 redes × 2 = 10
  Total no utilizable = 62            Eficiencia = 65 474 / 65 536 = 99,9 %
  Mayor prefijo libre contiguo: 172.16.128.0/17 (32 768) — un /17 dentro de un /16
     ocupa 2^(24−17) = 128 unidades del tercer octeto, y .128 es la última válida
```

**Con FLSM el mismo plan no existe:** las cinco subredes serían `/23` (512 dir) =
2560 direcciones, y el `/16` entraría justo, sin margen para ni un enlace. Con VLSM
entran las cinco **y** sobra el 98,5 %.

## 2.3 ⭐ Ejercicio 3 (de examen) — `2011-03` Problema 2 d

> **Fuente:** Examen 21 de febrero de 2011, `sirc1103`, Problema 2 (30 pts), d.
> **Link:** https://www.fing.edu.uy/inco/cursos/redescomp/examenes/sirc1103.pdf

**Enunciado (literal).**

> Se adquiere para la Red A el bloque de direcciones IP públicas `100.100.100.0/24`,
> y los administradores deciden aislar la red de servidores de los puestos de
> trabajo. Especifique las subredes del bloque mencionado que cumplan con este
> requerimiento y permitan dejar la mayor cantidad posible de direcciones IP para
> uso futuro. Mencione las modificaciones necesarias en el router R1 y su nueva
> tabla de enrutamiento.

**Contexto.** Red A privada con **15 servidores** y **70 puestos**; R1 traduce con
`220.10.10.30` sobre `220.10.10.28/30`. Ahora compran un bloque **público**.

### a) Los prefijos

```
  Red            Hosts  + gw  =  a direccionar   2^h − 2   h   prefijo  bloque
  ─────────────────────────────────────────────────────────────────────────────────
  PUESTOS          70  +  1  =      71          2^7−2=126 ✓  7   /25     128 dir
                              2^6 − 2 = 62 < 71 ✗
  SERVIDORES       15  +  1  =      16          2^5−2= 30 ✓  5   /27      32 dir
                              2^4 − 2 = 14 < 16 ✗   ← el error típico
```

### b) La asignación con el puntero

```
  puntero = 100.100.100.0

  /25  tamaño 128   inicio = menor múltiplo de 128 ≥ 0    = 0     → 100.100.100.0/25
  /27  tamaño  32   inicio = menor múltiplo de  32 ≥ 128  = 128   → 100.100.100.128/27

  100.100.100.0/24
  ├─ .0     /25   PUESTOS    red .0    bc .127  hosts .1   – .126  gw .1
  ├─ .128   /27   SERVIDORES red .128  bc .159  hosts .129 – .158  gw .129
  └─ .160 ────────── LIBRE 96 dir = 100.100.100.160/26 + 100.100.100.224/27
```

### c) La tabla de enrutamiento nueva de R1

```
  Red destino / Máscara      Gateway (next hop)     Distancia
  ───────────────────────────────────────────────────────────────
  100.100.100.0/25            C – Directamente conectado    1
  100.100.100.128/27          C – Directamente conectado    1
  220.10.10.28/30             C – Directamente conectado    1
  0.0.0.0/0                   220.10.10.29                 2
```

**Las modificaciones en R1, en orden:**

1. **Una interfaz por subred** (o dos sub-interfaces de VLAN). Antes tenía una
   sola para la red A.
2. **Se elimina el NAT.** Los hosts ya son alcanzables por dirección pública;
   seguir traduciendo "sobre-vendería" las públicas recién compradas, y rompería
   la señalización de los servidores (que es justamente lo que se quiere aislar
   y proteger).
3. **La ruta por defecto y la interfaz WAN no cambian.**
4. Cada subred **conserva su gateway**: `100.100.100.1` y `100.100.100.129`.

### d) El análisis: ¿esto **maximiza** lo que queda para el futuro?

Este es el apartado que más puntos da, porque el enunciado pide **justificar** y
no basta con decir "así me quedó".

```
  ┌───────────────────────┬───────────┬──────────┬──────────┬────────────────┐
  │ Plan                  │ Puestos   │ Servidor │ Total    │ Libre del /24  │
  ├───────────────────────┼───────────┼──────────┼──────────┼────────────────┤
  │ OFICIAL  /25 + /27    │   128     │    32    │   160    │ 96 (37,5 %)    │
  │ "Cómodo" /25 + /26    │   128     │    64    │   192    │ 64 (25,0 %)    │
  │ "Apretado" /25 + /28  │   128     │ 14 < 16  │ inválido │ no sirve       │
  │ "Simétrico" /26 + /26 │ 62 < 71   │    64    │ inválido │ no sirve       │
  └───────────────────────┴───────────┴──────────┴──────────┴────────────────┘

  Desperdicio DENTRO de los bloques:
    OFICIAL   (126 − 71) + (30 − 16) = 55 + 14 =  69
    "CÓMODO"  (126 − 71) + (62 − 16) = 55 + 46 = 101
    Diferencia a favor de la oficial: 32 direcciones = el doble de libres.
```

**Conclusión, y acá es donde se verifica en vez de copiar:**

> **La oficial dice `/25` y `/27`. Verifiqué la cuenta y es correcta, y además es la
> *única* solución posible**: `/26` no alcanza para 71 utilizables y `/28` no alcanza
> para 16. No hay margen en los prefijos, solo en el **orden** de asignación.
>
> **Mi lectura, que es la que suma puntos:** "dejar la mayor cantidad posible para
> uso futuro" tiene dos lecturas, y la oficial cumple las dos: gasta el mínimo hoy
> (160 de 256) **y** deja un remanente que se descompone limpiamente.
> `100.100.100.160`–`100.100.100.255` son 96 direcciones contiguas =
> `100.100.100.160/26` + `100.100.100.224/27`, justo lo que hace falta para dos LANs
> futuras de hasta 62 y de hasta 30 hosts. Con `/26` para los servidores, el libre
> quedaría partido en `.160/28` + `.176/27` + `.208/27` = 8 + 32 + 32: tres
> bloques inservibles por separado.
>
> O sea: **lo que el profesor quiere ver no es "la oficial está bien", sino "la
> oficial es correcta porque el mínimo de cada prefijo la obliga, y además produce
> un remanente alineado que sirve para el segundo reading del objetivo"**.

**⚠️ Errores típicos:** `/28` para los servidores; no contar el router (`+1` en
cada subred); dejar el NAT puesto; olvidar `0.0.0.0/0` en la nueva tabla (sin ella
los hosts de las subredes nuevas no salen a Internet, que era el objetivo).

## 2.4 ⭐ Ejercicio 4 (de examen) — `2010-07` Problema 2 a-i

> **Fuente:** Examen 27 de julio de 2010, `sirc1007`, Problema 2, parte a-i.

**Enunciado (literal).**

> Asigne las direcciones de red a las subredes LAN2 y LAN3 utilizando el prefijo
> de dirs. IP privadas mencionado anteriormente, asumiendo que se conectarán hasta
> 250 hosts por subred.

Datos: prefijo **`192.168.2.0/23`** para las dos sucursales; el ISP asignó
`220.10.10.28/30` al enlace WAN de R1. LAN1 y los enlaces entre routers ya están
numerados.

**Solución oficial.** *"Para cada subred se necesitan como máximo 250 (hosts) + 1
(router) = 251 direcciones IP por LAN. Entonces cada subred necesita utilizar una
`/24`: LAN 2 `192.168.2.0/24` · LAN 3 `192.168.3.0/24`"*.

**Mi resolución, con las dos cuentas que hay que dar.**

```
  250 hosts + 1 router = 251 direcciones pedidas
  + red y broadcast  ⇒  el bloque necesita ≥ 253 direcciones

  2^7 = 128  < 253   ✗   (/25 NO alcanza: son 128, no 256)
  2^8 = 256  ≥ 253   ✓   →  h = 8  →  prefijo = 32 − 8 = /24
  /24 = 256 direcciones totales, 254 utilizables.   254 ≥ 251 ✓  (sobran 3)

  ¿Cuántas subredes entran en el /23?
    Por bits:   el /23 deja 32 − 23 = 9 bits de subred; un /24 usa 8 de ellos;
                quedan 1 bit  →  2^1 = 2 subredes
    Por tamaño: 2^(32−23) = 512 direcciones ;  512 / 256 = 2 subredes   ✓
```

**Asignación con el puntero.**

```
  puntero = 192.168.2.0

  /24  tamaño 256   inicio = 0 ✓                    →  192.168.2.0/24  (LAN2) gw .2.1
        puntero = 256
  /24  tamaño 256   inicio = 256 ✓  (256/256 = 1)   →  192.168.3.0/24  (LAN3) gw .3.1
        puntero = 512 = 192.168.4.0

  Cuentas:  total /23 = 512 ; consumido 2 × 256 = 512  →  LIBRE: 0
            no utilizable = 2 redes × 2 (red+bc) + 2 redes × 3 (sobrantes) = 10
            eficiencia = (512 − 10) / 512 = 98,0 %
```

**El comentario que vale puntos:** el bloque queda **al 100 % de ocupación**. Si la
empresa supiera que necesitaría una tercera sucursal, debería haber pedido un
`/22`; el enunciado no lo dice, así que la respuesta correcta es usar el `/23`
entero. Pero **mencionar el costo de oportunidad del plan** es lo que demuestra que
entendiste el ejercicio, no solo la cuenta.

**⚠️ Errores típicos:** usar `/25` "porque 250 < 256" (`/25` son 128 direcciones; el
número que importa es `2^(32−prefijo) ≥ 253`); pedir un `/23` por subred (un `/23`
no es una LAN: son 512 direcciones, y la unidad es `/24` porque es lo que **cabe**);
contar los hosts del enlace WAN, que viene del bloque del ISP y no del `/23`.

## 2.5 ⭐ Ejercicio 5 (de examen) — `2010-12` Problema 2 a-i

> **Fuente:** Examen 1 de agosto de 2008, `sirc0807`, Problema 2, parte a-i (el
> banco de exámenes lo indexa también bajo `sirc1007`).

**Enunciado (literal).**

> Realice un plan de numeración de las subredes LAN3, 4 y 5 utilizando el prefijo
> de dirs. IP públicas mencionado anteriormente, asumiendo que no se conectan más
> de 120 hosts por subred. ¿Cuántas subredes se pueden numerar de acuerdo a su
> plan de numeración?

Datos: prefijo **`147.10.8.0/21`**; la red corporativa tiene sede central y
sucursal, con `220.10.10.13/30` y `220.10.20.14/30` en las interfaces WAN.

**Solución oficial.** *"Para cada subred se necesitan como máximo **120 + 1 + 2 =
123** direcciones IP por LAN."* → plan A: LAN3 `147.10.8.0/25`, LAN4
`147.10.8.128/25`, LAN5 `147.10.9.0/25`; plan B: LAN3 `147.10.8.0/25`, LAN4
`147.10.9.0/25`, LAN5 `147.10.10.0/25`. *"Según este plan se cuenta con `2^4 = 16`
subredes /25."*

**El `+2` de la oficial:** 120 hosts + 1 router + **2 de reserva** para crecimiento
inmediato de cada LAN (no red ni broadcast, que ya están dentro del `2^h`). Si no
lo decís, parece un error de suma.

**La aritmética del prefijo.**

```
  120 hosts + 1 router + 2 reserva = 123 direcciones pedidas
  + red y broadcast  ⇒  el bloque necesita ≥ 125 direcciones

  2^6 =  64  < 125   ✗   NO ALCANZA
  2^7 = 128  ≥ 125   ✓   →  h = 7  →  prefijo = 32 − 7 = /25
  /25 = 128 direcciones, 126 utilizables.   126 ≥ 123 ✓  (sobran 3 utilizables)

  Variante con el mínimo estricto (120 + 1 = 121, sin la reserva):
  121 + 2 = 123  ⇒  2^7 = 128 ≥ 125 ✓  →  ¡también /25!  La reserva NO cambia
  el prefijo: sirve para el futuro, no para la cuenta.
```

**¿Cuántas subredes da el plan?** Las dos cuentas, y hay que dar las dos:

```
  Por tamaño:  2^(32 − 21) = 2^11 = 2048 direcciones ; 2048 / 128 = 16 subredes /25
  Por bits:    el /21 deja 32 − 21 = 11 bits de subred.
               un /25 usa  32 − 25 =  7 de esos bits.
               Quedan     11 − 7  =  4 bits  →  2^4 = 16   ✓
```

**Asignación con el puntero (el plan A de la oficial):**

```
  puntero = 147.10.8.0

  /25  inicio = 0 ✓                     →  147.10.8.0/25     puntero → 147.10.8.128
  /25  inicio = 128 ✓  (128/128 = 1)    →  147.10.8.128/25   puntero → 147.10.9.0
  /25  inicio = 256 ✓  (256/128 = 2)    →  147.10.9.0/25     puntero → 147.10.9.128

  LIBRE desde 147.10.9.128: 13 subredes /25 = 1 664 direcciones
  Cuentas:  total /21 = 2048 ; consumido 3 × 128 = 384 ; libre 1 664 = 13 /25
            desperdicio interno = 3 × (126 − 123) = 9   eficiencia = 97,7 %
```

**⚠️ Por qué la oficial prefiere el plan A (lo que más suma):**

```
  PLAN A:  LAN3 .8.0/25 · LAN4 .8.128/25 · LAN5 .9.0/25
           LAN3 + LAN4 = 147.10.8.0/24  ← SUMARIZA (0 es múltiplo de 256)
           ⇒ R2 necesita 2 rutas hacia la empresa.

  PLAN B:  LAN3 .8.0/25 · LAN4 .9.0/25 · LAN5 .10.0/25
           ⇒ R2 necesita 3 rutas. NO SE PUEDE sumarizar: para resumir LAN4
             (.9.0–.9.127) y LAN5 (.10.0–.10.127) harían falta 256 direcciones
             arrancando en .8.0 o en .10.0, y .9.0 no es ninguno de los dos.

  O sea: "la solución no es única, pero no todas son equivalentes: el plan tiene
  que optimizar no solo las direcciones sino la cantidad de rutas" — y eso se
  decide en el paso 3, no en el paso 2.
```

## 2.6 ⭐ Ejercicio 6 (de examen) — `2006-08` Problema 1: seis routers

> **Fuente:** Examen 5 de agosto de 2006, `sirc0608`, Problema 1 (30 pts).
> **Aclaración:** el problema original es una figura. **Adaptamos la figura a texto**:
> routers, enlaces, direcciones y default gateway (192.168.1.254 y 192.168.2.254)
> son los del examen; la métrica es el costo de enlace de la tabla del enunciado,
> reasignado de forma consistente con las soluciones oficiales de los apartados b)
> y e) del mismo examen. La topología de abajo reproduce **exactamente** las dos
> respuestas oficiales de `traceroute` (ver §2.6 c).

### La topología

```
        LAN1 192.168.1.0/24                      LAN2 192.168.2.0/24
        gw 192.168.1.254                         gw 192.168.2.254
        ┌──────────────────────┐                  ┌──────────────────────┐
        │ PC1 .1   PC2 .2     │                  │ PC5 .1   PC6 .2     │
        │    \      /         │                  │    \      /         │
        │     \    /          │                  │     \    /          │
        │      R1             │                  │      R2             │
        └──────────────────────┘                  └──────────────────────┘

              ╱10.10.13/30 (c2)          ╲10.10.24/30 (c4)
             ╱      R1 .1 · R3 .3        ╲    R1 .4 · R2 .2
            ╱                             ╲
   10.10.15/30 (c1)                     10.10.26/30 (c1)
   R1 .1 — R5 .5                          R2 .2 — R6 .6
          ╲                                  ╱
           ╲       10.10.34/30 (c2)        ╱
            ╲    R3 .3 — R4 .4           ╱
             ╲                            ╱
      ┌──────┴──────┐    10.10.36/30 (c4)
      │     R4      │    R3 .3 — R6 .6
      └──────┬──────┘            │
             │                   │
      10.10.45/30 (c1)           │
      R4 .4 — R5 .5              │
                       10.10.56/30 (c1)
                       R5 .5 — R6 .6

  Enlaces y costos (los del enunciado):
    10.10.13  R1.1  – R3.3     10.10.15  R1.1 – R5.5      10.10.24  R1.4 – R2.2
    10.10.26  R2.2  – R6.6     10.10.34  R3.3 – R4.4      10.10.36  R3.3 – R6.6
    10.10.45  R4.4  – R5.5     10.10.56  R5.5 – R6.6
```

### a) Tablas de enrutamiento de los seis routers

Formato de la cátedra: **Red destino / Máscara · Gateway (next hop) · Distancia**.

```
  R1                                    R2
  192.168.1.0/24   C – Directamente conectado  1     192.168.2.0/24  C – Directamente conectado 1
  192.168.2.0/24   10.10.15.5                 3     192.168.1.0/24  10.10.26.6                3

  R3                                    R4
  192.168.1.0/24   10.10.13.1                 2     192.168.1.0/24  10.10.45.5                2
  192.168.2.0/24   10.10.36.6                 5     192.168.2.0/24  10.10.45.5                3

  R5                                    R6
  192.168.1.0/24   10.10.15.1                 1     192.168.1.0/24  10.10.56.5                2
  192.168.2.0/24   10.10.56.6                 2     192.168.2.0/24  10.10.26.2                1
```

**Cómo se calcularon, con Dijkstra sobre la matriz de costos** (elementales 1, 2 y
4). El más caro de todos, R3 hacia LAN2:

```
  R3 → LAN2:   vía R6 = 4 + 1 = 5   ✓   vía R1 = 2 + 3 = 5   vía R4 = 2 + 3 = 5
  Empate en los tres; con empate gana el vecino de menor dirección de enlace:
  R6 (10.10.36.6) ✓  — que es lo que dice la oficial, con costo 5.

  Y el que define la tabla de R2, el corazón del ejercicio:
  R2 → LAN1:   vía R6 = 1 + 1 + 1 = 3  ✓      vía R1 (directo) = 4   peor
  ⇒ R2 usa 10.10.26.6 con distancia 3   (la oficial dice 10.10.26.6)  ✓
```

### b) Tablas de enrutamiento de los hosts

**Todos los hosts de LAN1** (`.1.1` … `.1.254`) y de LAN2 (`.2.1` … `.2.254`):

```
  Red destino / Máscara   Gateway (next hop)          Distancia
  192.168.1.0/24          C – Directamente conectado        1
  0.0.0.0/0               192.168.1.254                     2      ← hosts de LAN1

  Red destino / Máscara   Gateway (next hop)          Distancia
  192.168.2.0/24          C – Directamente conectado        1
  0.0.0.0/0               192.168.2.254                     2      ← hosts de LAN2
```

⚠️ **Un host tiene una entrada por red local más la default**, nunca más: si un
host tiene **dos** interfaces, tiene **dos** redes locales y una default, y el
*longest prefix match* decide por cuál sale cada destino (Clase 30).

### c) Verificación contra las soluciones oficiales

**Enrutamiento normal.** La oficial: *"el camino de menor costo de 192.168.2.0/24
a 192.168.1.0/24 es R2 → R6 → R5 → R1"*:

```
  PC6 (LAN2) → R2 → R6 → R5 → R1 → PC2 (LAN1)
  Interfaces que reporta traceroute:  192.168.2.254 · 10.10.26.6 · 10.10.56.5
                                    · 10.10.15.1 · 192.168.1.2
  Suma: 4 enlaces.  En mis tablas R2 usa 10.10.26.6 (d=3), R6 usa 10.10.56.5
  (d=2), R5 usa 10.10.15.1 (d=1).   ✓ COINCIDE
```

**Si se cae R4.** La oficial: *"la respuesta es la misma, pues R4 no es utilizado
en el camino de ida"* → **el `traceroute` no cambia una línea**. En mis tablas
ningún next hop apunta a `10.10.34.4` ni a `10.10.45.4`. ✓ COINCIDE

**Si se cae R5.** La oficial da `R2 → R6 → R3 → R1` con interfaces
`192.168.2.254 · 10.10.26.6 · 10.10.36.3 · 10.10.13.1`:

```
  Con R5 caído, R6 ya no puede ir por 10.10.56.5, así que su next hop a LAN1 pasa
  a ser R3 por 10.10.36.3 (d = 4 + 2 = 6); R3 mantiene 10.10.13.1 (d = 2).
  Camino:  192.168.2.254 · 10.10.26.6 · 10.10.36.3 · 10.10.13.1 · destino
  ✓ COINCIDE con la solución oficial, interfaz por interfaz.
```

**Ese es el mejor detalle del problema:** la tabla de enrutamiento no dice "el
camino más corto a la LAN", sino "el camino más corto **al vecino más barato**".
Cuando R5 se cae, R3 —que antes era un rodeo— pasa a ser la primera opción de R6.
Por eso los apartados d) y e) hablan de *convergencia*, no de tablas fijas.

---

# PARTE 3 — EJERCICIOS EXTRA (dificultad creciente)

## 3.1 Ejercicio 7 — VLSM con cinco redes y tres enlaces

**Enunciado.** De `172.20.0.0/16`: LAN de **300**, **120** y **60** hosts, más
**tres enlaces punto a punto**.

```
  301 → 2^8 − 2 = 254 < 301 ✗ ; 2^9 − 2 = 510 ≥ 301 ✓  →  /23  (512 dir)
  121 → 2^7 − 2 = 126 ≥ 121 ✓                          →  /25  (128 dir)
   61 → 2^6 − 2 =  62 ≥  61 ✓                          →  /26  ( 64 dir)
    2 → 2^2 − 2 =   2 ≥   2 ✓                          →  /30  (  4 dir)  ×3

  puntero = 172.20.0.0
  /23  inicio = 0    ✓                 → 172.20.0.0/23     puntero → 172.20.2.0
  /25  inicio = 512  ✓ (512/128 = 4)   → 172.20.2.0/25     puntero → 172.20.2.128
  /26  inicio = 640  ✓ (640/64 = 10)  → 172.20.2.128/26   puntero → 172.20.2.192
  /30  inicio = 704  ✓ (704/4 = 176)  → 172.20.2.192/30   puntero → 172.20.2.196
  /30  inicio = 708  ✓ (708/4 = 177)  → 172.20.2.196/30   puntero → 172.20.2.200
  /30  inicio = 712  ✓ (712/4 = 178)  → 172.20.2.200/30   puntero → 172.20.2.204

  Consumidas:  512 + 128 + 64 + 4 + 4 + 4 = 716  de 65 536
  Libres:      65 536 − 716 = 64 820   (98,9 %)
  Desperdicio interno: (510−301) + (126−121) + (62−61) + 0 + 0 + 0 = 209 + 5 + 1 = 215
  Libre a partir de 172.20.2.204:  .204/30 (4) · .208/29 (8) · .216/29 (8) ·
                                     .224/28 (16) · 172.20.3.0/24 · 4.0/23 · …
  Mayor prefijo libre: 172.20.128.0/17 (32 768)
```

**Lo que enseña:** los tres `/30` seguidos no pierden nada: `704, 708,`
712` son múltiplos de 4, así que el puntero nunca se desvía.

## 3.2 Ejercicio 8 — ¿Cuántas direcciones desperdicia cada plan?

**Enunciado.** Del bloque `192.168.0.0/21` (2048 dir) se necesitan LANs de 300,
200 y 50 hosts más un enlace punto a punto. Compará FLSM y VLSM **midiendo el
desperdicio**, no solo la cantidad de direcciones.

```
  ══ FLSM ══  el mayor pide 301 → h = 9 → /23 para TODAS
     4 × 512 = 2048 = el bloque entero.  Libre: 0
     Usado realmente: 301 + 201 + 51 + 2 = 555
     Desperdicio = 2048 − 555 = 1493   (72,9 % del bloque)

  ══ VLSM ══  301 → /23 (512) · 201 → /24 (256) · 51 → /26 (64) · 2 → /30 (4)
     Total = 836   Libre = 2048 − 836 = 1212
     Desperdicio interno = (510−301)+(254−201)+(62−51)+(2−2) = 209+53+11+0 = 273
     Red + broadcast = 4 redes × 2 = 8      Total no utilizable = 281 (13,7 %)

  ┌──────────────┬───────────────┬──────────────┬──────────────────┐
  │              │ FLSM (/23 x4) │ VLSM         │ Diferencia       │
  ├──────────────┼───────────────┼──────────────┼──────────────────┤
  │ Direccionadas │         2 048 │          836 │  − 1 212         │
  │ Libres       │             0 │        1 212 │  + 1 212         │
  │ Desperdicio  │         1 493 │          281 │  − 81 %          │
  │ Eficiencia   │       27,1 % │       86,3 % │  + 59,2 pp       │
  └──────────────┴───────────────┴──────────────┴──────────────────┘
```

**Conclusión:** el FLSM no desperdicia un 27 % "de direcciones": desperdicia el
**73 %**. Ese es el número que hay que decir, no "usa más direcciones".

## 3.3 Ejercicio 9 — Renumerar para meter un switch (y cuándo NO hace falta)

**Enunciado.** Se reemplaza R2 por un switch, y las subredes 2 y 3 quedan en el
mismo dominio de broadcast. ¿Hay que renumerar?

**Caso A — `192.168.108.0/24` y `192.168.109.0/24`.**

```
  ¿Es un /23?  108 = 01101100,  109 = 01101101 → difieren en **UN bit**
     (00001100 vs 00001101), y un /23 "se come" el último bit del tercer octeto.
     108 es par  ⇒  108/2 = 54 exacto  ⇒  /23 cubre .108.0 – .109.255   ✓
  ⇒ NO HAY QUE RENUMERAR. Solo cambian:
       · la máscara de R1 en esa interfaz:  /24 → /23
       · la máscara de los hosts de las subredes 2 y 3:  /24 → /23
       · el default gateway de esos hosts:  192.168.108.1  (no cambia)
```

**Caso B — `192.168.0.0/24`, `.1.0/24` y `.2.0/24` (del `2010-03 P1b`)**

```
  ¿.0.0/24 + .1.0/24 = un /23? Arrancaría en 192.168.0.0/23 → sí, cubre
  .0.0–.1.255 ✓. PERO .2.0/24 queda en otra subred, así que el switch no puede
  unificar 1 y 2. Para meter las TRES hace falta un /22:
       192.168.0.0/22 cubre .0.0 – .3.255 (1024 dir); 0 es múltiplo de 4 ✓
  ⇒ SÍ hay que renumerar. La solución oficial (mínima cantidad de direcciones
    modificadas) mueve SOLO la subred 1:  192.168.0.0/24 → 192.168.3.0/24, y las
    subredes 2 y 3 quedan en 192.168.0.0/22.
    Tabla de R1:  192.168.3.0/24 → C (eth0)  ·  192.168.0.0/22 → C (eth1)
```

**Lo que hay que decir en el examen:** *"la renumeración es necesaria cuando las
subredes a unificar **no forman un prefijo contiguo y alineado**; si son contiguas
y la cantidad es potencia de 2, alcanza con cambiar la máscara"*, y eso se verifica
mirando cuántos bits las distingue en binario.

## 3.4 Ejercicio 10 — ¿Se puede sumarizar?

**Enunciado.** Del plan del Ejercicio 2 (`172.16.0.0/16`): `0.0/23`, `2.0/24`,
`3.0/25`, `3.128/26`, `3.192/27`. Agrupá las rutas de a dos, de a tres, etc., hasta
cuántas quedan.

```
  Nivel 1:  172.16.3.0/25 + 172.16.3.128/26  = 172.16.3.0/24  ✓ (128+64 = 192,
           contiguo dentro de .3.0–.3.255)
           172.16.3.0/24 + 172.16.3.192/27  = 172.16.3.0/24  ✓ ya dentro
  Nivel 2:  172.16.2.0/24 + 172.16.3.0/24    = 172.16.2.0/23  ✓ (256+256 = 512)
  Nivel 3:  172.16.0.0/23 + 172.16.2.0/23    = 172.16.0.0/21  ✓ (512+512 = 1024)

  RESULTADO: 5 rutas → 1 sola: 172.16.0.0/21
  Chequeo: el plan ocupa .0.0 – .3.255 = 1024 = un /21 exacto. ✓
  Ojo: el /21 ABARCA .4.0 – .7.255, que están LIBRES. Al sumarizar estás
  anunciando también lo que no usás, y eso es correcto: el espacio de una red es
  del router hacia afuera, no "lo que yo uso".
```

**El caso que NO se puede**, para que quede la regla:

```
  172.16.3.128/26 + 172.16.3.192/27  →  64 + 32 = 96, no es potencia de 2.
  Un /25 arrancaría en .128/25 = .128–.255  ✗ incluye .224/27, que es otra red.
  REGLA: la cantidad de direcciones tiene que ser POTENCIA DE 2 y el arranque tiene
  que estar alineado a ese tamaño. Si no, no hay resumen.
```

## 3.5 Ejercicio 11 — El puntero que cambia de paso

**Enunciado.** En `192.168.1.0/24` ya usaste `/25`, `/26`, `/27`, `/30` y `/30`;
el puntero quedó en **232**. Ahora piden, en este orden, un `/29`, un `/31`, un
`/32` y un `/28`. Verificá.

```
  puntero = 192.168.1.232
  /29  inicio = menor múltiplo de 8  ≥ 232 = 232  ✓  → .232/29 (.232–.239)  ptr 240
  /31  inicio = menor múltiplo de 2  ≥ 240 = 240  ✓  → .240/31 (.240–.241)  ptr 242
  /32  inicio = cualquier entero ≥ 242             → .242/32 (.242)         ptr 243
  /28  inicio = menor múltiplo de 16 ≥ 243 = 256  ✗  ¡NO ENTRA!
```

**Acá está la lección:** un `/28` (16 direcciones) **ya no entra**, porque el bloque
libre que queda (`.232`–`.255`, 24 direcciones) no está alineado a 16. Si lo hubieras
pedido **antes** del `/29`:  `/28` arranque en 240 → `.240/28` → puntero 256 = FIN,
y el `/29` + `/31` + `/32` NO HABRÍAN ENTRADO.

**Conclusión práctica:** el **último** bloque del plan es el que peor redondeo
sufre; si vas a necesitar uno grande al final, pedilo primero.

---

# PARTE 4 — CIERRE

## 📌 Resumen

1. Las cinco fórmulas: `2^h − 2 ≥ H` · `2^(32−prefijo)` · `dir/tamaño × tamaño` ·
   `dir + tamaño − 1` · `puntero = menor múltiplo de tamaño ≥ puntero`.
2. Para **n** subredes iguales se roban `log2(n)` bits: 4 subredes en un `/24` →
   **/26** (62 utilizables c/u), no `/27`.
3. `172.16.0.0/16` para 500/250/100/50/25 → `/23 · /24 · /25 · /26 · /27` =
   992 direcciones, libre 64 544, mayor prefijo libre `172.16.128.0/17`.
4. `100.100.100.0/24` para 70+1 y 15+1 → **`/25` + `/27`**; el `/28` NO entra
   (14 utilizables < 16). Libre: 96 = `/26 + /27`.
5. `192.168.2.0/23` con 251 por LAN → `/24` → exactamente **2** subredes, bloque al
   100 %.
6. `147.10.8.0/21` con 123 por LAN → `/25` → **16** subredes; el plan A es mejor
   que el B porque `LAN3 + LAN4` **sumarizan** en un `/24` (2 rutas en vez de 3).
7. Seis routers: el `traceroute` normal va `R2→R6→R5→R1`; si cae R5, pasa a
   `R2→R6→R3→R1`. Si cae R4, no cambia. Las tablas se recalculan, no se borran.
8. **Desperdicio, no "direcciones usadas":** con FLSM, un `/21` para 300+200+50
   pierde el **73 %**; con VLSM, el **13,7 %**.
9. Renumerar **no** hace falta si las subredes a unificar ya forman un prefijo
   contiguo y alineado (`108.0/24` + `109.0/24` = `/23`). Hace falta si no.
10. El **último** bloque del plan es el que peor redondeo sufre: pedí primero el
    más grande.

## ✅ Autoevaluación

Respondé sin mirar. Las respuestas están en `<details>`.

**1.** ¿Por qué 16 direcciones no entran en un `/27` de 32 direcciones?

<details><summary>Respuesta</summary>

Porque `2^4 = 16` es el total **incluyendo** red y broadcast: los utilizables son
`16 − 2 = 14`. El `+2` va **dentro** del `2^h`, así que el prefijo es `/27`
(`2^5 − 2 = 30 ≥ 16`).

</details>

**2.** Cuatro subredes iguales en un `/24`: ¿por qué `/26` y no `/27`?

<details><summary>Respuesta</summary>

Porque el subnetting clásico **roba el mínimo número de bits**: 4 = `2^2`, roba 2
y queda `/26` (62 c/u, 248 en total, `4 × 64 = 256`). `/27` daría **8** subredes de
30: cuatro de sobra. `/25` daría solo 2, insuficiente.

</details>

**3.** `172.16.0.0/16` para 500, 250, 100, 50 y 25 hosts (+1 router cada una):
prefijos, consumo y mayor prefijo libre.

<details><summary>Respuesta</summary>

`501 → /23` · `251 → /24` · `101 → /25` · `51 → /26` · `26 → /27`.
Consumo `512+256+128+64+32 = 992` de 65 536 → libre 64 544. Puntero:
`0.0/23` · `2.0/24` · `3.0/25` · `3.128/26` · `3.192/27`; libre desde `3.224/27` y,
en grande, desde `4.0`. Mayor prefijo libre contiguo: **`172.16.128.0/17`**
(32 768), porque un `/17` dentro de un `/16` ocupa 128 unidades del tercer octeto.

</details>

**4.** `100.100.100.0/24` para 70 puestos + 1 router y 15 servidores + 1 router.
Verificá la solución oficial y decí quécfc остаток queda libre.

<details><summary>Respuesta</summary>

Puestos piden 71 → `2^6 − 2 = 62 < 71` ✗, `2^7 − 2 = 126 ≥ 71` ✓ → **`/25`**.
Servidores piden 16 → `2^4 − 2 = 14 < 16` ✗, `2^5 − 2 = 30 ≥ 16` ✓ → **`/27`**.
Puntero: `100.100.100.0/25` y `100.100.100.128/27`. **Libre: `.160`–`.255` = 96
direcciones**, que se descomponen en `160/26` + `224/27`. La oficial es correcta y
es la única solución posible; lo que suma es observar que ese remanente está
**alineado**, que es el segundo reading de "maximizar para el futuro".

</details>

**5.** Del `/21` `147.10.8.0` con 123 direcciones por LAN: ¿qué prefijo y cuántas
subredes? Dad las dos cuentas.

<details><summary>Respuesta</summary>

`123 + 2 = 125` → `123 + 2 = 125` → `2^6 = 64 < 125` ✗, `2^7 = 128 ≥ 125` ✓ → **`/25`**.
Por tamaño: `2048 / 128 = 16` subredes. Por bits: `11 − 7 = 4` bits → `2^4 = 16`.

</details>

**6.** `192.168.108.0/24` y `192.168.109.0/24`: ¿hay que renumerar para ponerlas
en el mismo dominio de broadcast con un switch?

<details><summary>Respuesta</summary>

**No.** `108 = 01101100` y `109 = 01101101` difieren **en un solo bit**, así que
`192.168.108.0/23` cubre `.108.0`–`.109.255`. Alcanza con cambiar la máscara de R1
y de los hosts a `/23`; el gateway sigue siendo `192.168.108.1`.

</details>

**7.** Del plan del ejercicio 2, ¿cuántas rutas quedan al sumarizar y cuál es la más
agregada posible? ¿Y por qué está bien anunciar direcciones que no usás?

<details><summary>Respuesta</summary>

De 5 a 1: `3.0/25 + 3.128/26` → `3.0/24`; `2.0/24 + 3.0/24` → `2.0/23`;
`0.0/23 + 2.0/23` → **`172.16.0.0/21`**. Se anuncia el prefijo entero aunque
incluya `.4.0`–`.7.255`, que están libres: el espacio de una red es del router
hacia afuera, y lo que se agregue en el futuro entra **sin tocar ninguna tabla**.

</details>

**8.** El puntero quedó en 232 y quedan 24 direcciones libres
(`192.168.1.232`–`.255`). ¿Entran un `/29`, un `/31` y un `/28`? ¿En qué orden?

<details><summary>Respuesta</summary>

En ese orden: `/29` arranca en 232 (múltiplo de 8 ✓), puntero 240; `/31` en 240
(múltiplo de 2 ✓), puntero 242; y el `/28` (16) **ya no entra**: el menor múltiplo
de 16 mayor o igual que 242 es 256, fuera del `/24`. Al revés, el `/28` arranca en
240 y se lleva todo. **El último bloque es el que peor redondeo sufre**: pedí
primero el más grande.

</details>

## 🔗 Referencias

- **`eirc1103` / `sirc1103`** (21-feb-2011) — Problema 2 d: `100.100.100.0/24` para 70 puestos + 15 servidores (Ejercicio 3)
- **`sirc1007`** (27-jul-2010) — P2 a-i: `192.168.2.0/23` con 250 hosts (Ejercicio 4)
- **`sirc0807`** (1-ago-2008) — P2 a-i: `147.10.8.0/21` con 120 hosts por LAN (Ejercicio 5)
- **`sirc0608`** (5-ago-2006) — **Problema 1**: topología de 6 routers (Ejercicio 6) · P4: `200.40.224.0/25` en 18, 11 y 9 hosts
- **`sirc0912`** / **`sirc1003`** — Problema 1 b: renumerar para agregar un switch (Ejercicio 9)
- **Tanenbaum & Wetherall**, *Redes de computadoras* 5ª ed., cap. 5 "La capa de red"
- **RFC 1918** (privadas) 🔍 · **RFC 4632** (CIDR) 🔍 · **RFC 6177** (2011) · **RFC 8200** (2017)
- **Clase anterior:** 28 — VLSM y planes de numeración · **Clase siguiente:** 30 — Tablas de enrutamiento, next hop y ARP