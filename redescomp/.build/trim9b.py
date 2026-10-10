import pathlib, sys
sys.stdout.reconfigure(encoding="utf-8")
p = pathlib.Path("clases/clase-09-http-detallado.md")
t = p.read_text(encoding="utf-8")
before = len(t)

INI = "### a) y b) — Resolución"
FIN = "## 3.2 Examen 2009-07, Problema 2"

i = t.index(INI)
j = t.index(FIN)

nuevo = """### a) y b) — Resolución

La tabla oficial es correcta y es la respuesta del apartado a). Lo que hay que
agregar son las **capas que la oficial abstrae**: el paso 1 vale **1 RTT de TCP** (2
con HTTPS), el paso 4 es un `FIN` que no cuesta RTT pero deja un `TIME-WAIT` de 2×MSL
en el cliente, y el paso 3 debería llevar `Cache-Control` + `ETag` + `Last-Modified`,
que es lo que hace que la **segunda** carga de la misma página sea un `304` en lugar
de 11 descargas.

**Respuesta redactada, lista para copiar en el examen:**

> **a)** En HTTP **no persistente**, por cada objeto (el HTML y cada una de las 10
> imágenes) el cliente ejecuta **cuatro pasos**: (1) establece una conexión TCP con el
> servidor, (2) envía un request pidiendo el objeto, (3) el servidor envía un
> response con el contenido del objeto, (4) el servidor cierra la conexión. El
> primer objeto es la página HTML; al recibirla y parsearla, el cliente descubre las
> 10 imágenes referenciadas y repite los pasos 1–4 **una vez por cada imagen**. En
> total son **11 objetos × 4 pasos = 44 pasos**, con **11 conexiones TCP distintas** y
> **22 RTT** (2 RTT por objeto: 1 de handshake TCP + 1 de request/response). Si el
> sitio usa HTTPS, a cada uno de esos RTT se le suma 1 RTT de TLS: **33 RTT**.
>
> **b)** En HTTP **persistente** se establece **una sola** conexión TCP y por ella se
> piden los 11 objetos uno tras otro: **1 RTT** de handshake + **11 RTT** de
> request/response = **12 RTT**, contra los 22 del no persistente. La mejora es real
> cuando el navegador trabaja **secuencialmente**, porque se eliminan los
> `N − 1 = 10` handshakes. **Pero no siempre mejora:** si el navegador abre
> conexiones **en paralelo** (que es lo que hacen los reales) y los objetos vienen de
> **varios servidores**, los handshakes pasan todos al mismo tiempo: el no persistente
> baja a **4 RTT** y el persistente queda en **4 RTT**, o sea, la ventaja
> **desaparece**.

**Lo que esta clase 9 agrega: la misma pregunta, versión por versión.**

```
   ═══ El mismo caso, en HTTP/2 ═══
   1 conexión TCP (11 streams simultáneos)        1 RTT
   GET HTML + 10 GETs en paralelo                 1 RTT
   ───────────────────────────────────────────────────
   Total:                                           2 RTT
   Contra los 22 RTT del no persistente y los 12 del persistente.
   La pérdida de un stream frena SOLO a ese stream.

   ═══ El mismo caso, en HTTP/3 ═══
   1 conexión QUIC (con TLS integrado)            1 RTT
   GET HTML + 10 GETs en paralelo                 1 RTT
   ───────────────────────────────────────────────────
   Total:                                           2 RTT
   Pero el handshake es 1 RTT en vez de 2 (TCP + TLS), y la pérdida de un
   stream no frena a los otros: en HTTP/1.1 una sola pérdida de paquete en
   una imagen congelaba la página entera durante 1 RTO.

   ═══ Y con HTTPS, que es el caso real ═══
   HTTP/1.1 no persistente + HTTPS:  11 × (1 TCP + 1 TLS + 1 HTTP) = 33 RTT
   HTTP/1.1 persistente  + HTTPS:     1 + 1 + 11                     = 13 RTT
   HTTP/2              + TLS:         1 + 1                          =  2 RTT
   HTTP/3              + QUIC:        1                              =  1 RTT
```

*Interpretación:* el objetivo de HTTP/2 y HTTP/3 **es exactamente este problema de
examen**. Los dos nacen para matar el número de viajes que el enunciado cuenta, y la
lección es que **el problema no se resolvió cambiando la forma de pedir**: se resolvió
cambiando la forma de **transportar** varias peticiones a la vez.

> **Nota contra la oficial:** la oficial dice «puede resultar más performante», que
> es la respuesta honesta y matizada, y agrega el mejor argumento del apartado b):
> **«si el servidor nos limita por IP»**, o sea que el navegador no puede paralelizar
> porque el servidor impone un límite por IP. Yo repito ese argumento y agrego las
> tres precisiones que la oficial omite: el costo en RTT del paso 1, el `TIME-WAIT`
> del paso 4 y el `ETag`/`Cache-Control` del paso 3.

---

"""

t = t[:i] + nuevo + t[j:]
p.write_text(t, encoding="utf-8", newline="\n")
print("antes:", before, "ahora:", len(t), "ahorro:", before - len(t))
