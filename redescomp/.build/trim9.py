import pathlib, sys
sys.stdout.reconfigure(encoding="utf-8")
p = pathlib.Path("clases/clase-09-http-detallado.md")
t = p.read_text(encoding="utf-8")
before = len(t)

R = []

# --- 2.1: paso 4, reemplazar el bloque de mensaje por prosa
R.append(("""*Paso 4 — Segundo pedido (09:45): el `max-age` venció, hay que revalidar.*

```
GET /notas/2026.pdf HTTP/1.1
Host: www.fing.edu.uy
User-Agent: Mozilla/5.0 (X11; Linux x86_64)
If-None-Match: "5d9b21-30d40-6518a1f0"
If-Modified-Since: Mon, 05 Oct 2026 09:14:07 GMT
Accept: application/pdf
Connection: keep-alive

```
""", """*Paso 4 — Segundo pedido (09:45): el `max-age` venció, hay que revalidar.* El
mensaje es **idéntico al del paso 1** más las dos cabeceras condicionales:

```
If-None-Match: "5d9b21-30d40-6518a1f0"
If-Modified-Since: Mon, 05 Oct 2026 09:14:07 GMT
```
"""))

# --- 2.1: paso 6, reemplazar el bloque de mensaje por prosa
R.append(("""*Paso 6 — Tercer pedido (10:00): ahora sí, y el archivo cambió.*

```
HTTP/1.1 200 OK
Date: Tue, 06 Oct 2026 10:00:00 GMT
Server: nginx/1.26.1
Last-Modified: Tue, 06 Oct 2026 09:50:11 GMT
ETag: "5d9b21-31234-6518a9c8"
Cache-Control: max-age=1800
Accept-Ranges: bytes
Content-Type: application/pdf
Content-Length: 201344
Connection: keep-alive

%PDF-1.7 ... 201.344 bytes ... %%EOF
```
""", """*Paso 6 — Tercer pedido (10:00): ahora sí, y el archivo cambió.* La respuesta es
un `200` completo **idéntico al del paso 2** salvo tres campos: `Last-Modified`
pasa a `Tue, 06 Oct 2026 09:50:11 GMT`, el `ETag` pasa a `"5d9b21-31234-6518a9c8"`
y `Content-Length` pasa a `201344`.
"""))

# --- autoevaluación 1
R.append(("""**No.** `POST` es el único método común que **no es ni seguro ni idempotente**: si el servidor procesó el cobro y lo que se perdió fue la respuesta, un reintento automático **cobra dos veces**.

La propiedad que lo salva es la **idempotencia**: si el método fuera idempotente, reintentarlo *n* veces tendría el mismo efecto que una y el cliente podría reintentar solo. Por eso los clientes HTTP reales, ante un `POST` ambiguo, o preguntan al usuario, o mandan una **idempotency key** que el servidor usa para deduplicar.""",
"""**No.** `POST` es el único método común que **no es ni seguro ni idempotente**: si el servidor procesó el cobro y lo que se perdió fue la respuesta, un reintento automático **cobra dos veces**. La propiedad que lo salva es la **idempotencia**: si el método fuera idempotente, reintentarlo *n* veces tendría el mismo efecto que una. Por eso los clientes reales, ante un `POST` ambiguo, preguntan al usuario o mandan una **idempotency key** para deduplicar."""))

# --- autoevaluación 2
R.append(("""- **`no-cache`**: el recurso **se guarda**, pero **nunca se sirve sin revalidarlo**. Declaración explícita de intención.
- **`max-age=0`**: el recurso **se guarda**, pero su frescura es de **cero segundos**, así que hay que revalidarlo siempre. Logra lo mismo que `no-cache` **por aritmética**, no por declaración.
- **`no-store`**: el recurso **no se guarda en ninguna caché**. Es la única que garantiza que el dato no queda en reposo.

Los dos primeros sirven para **revalidar barato**: con un `ETag` presente, la revalidación cuesta 180 bytes (un `304`) en lugar de 200 000. `no-store` es para datos que no deben quedar en disco.""",
"""- **`no-cache`**: el recurso **se guarda**, pero **nunca se sirve sin revalidarlo**. Declaración explícita de intención.
- **`max-age=0`**: el recurso **se guarda**, pero su frescura es de **cero segundos**. Logra lo mismo que `no-cache` **por aritmética**, no por declaración.
- **`no-store`**: el recurso **no se guarda en ninguna caché**. Es la única que garantiza que el dato no queda en reposo.

Los dos primeros sirven para **revalidar barato**: con un `ETag`, la revalidación cuesta 180 bytes (un `304`) en lugar de 200 000. `no-store` es para datos que no deben quedar en disco."""))

# --- autoevaluación 5
R.append(("""Porque **reduce la distancia física entre el cliente y el servidor que le responde**, y el RTT es proporcional a esa distancia más los saltos y el procesamiento de cada router.

El tiempo de carga de una página es esencialmente `número de viajes × RTT`. Si un cliente en Montevideo espera 120 ms a un servidor en Virginia y 3 ms a un nodo del CDN en Montevideo, el mismo contenido se entrega **40 veces más rápido**, sin cambiar un solo byte. Y el segundo beneficio es la **descarga del origen**: si el 95 % de los pedidos lo responde el nodo del CDN, el origen sobrevive a un pico de tráfico o a un ataque.""",
"""Porque **reduce la distancia física entre el cliente y el servidor que le responde**, y el RTT es proporcional a esa distancia más los saltos. El tiempo de carga de una página es esencialmente `número de viajes × RTT`: un cliente en Montevideo que espera 120 ms a un servidor en Virginia y 3 ms a un nodo del CDN en Montevideo recibe el mismo contenido **40 veces más rápido**, sin cambiar un byte. El segundo beneficio es la **descarga del origen**: si el 95 % de los pedidos lo responde el nodo del CDN, el origen sobrevive a un pico o a un ataque."""))

# --- autoevaluación 6
R.append(("""**Gana:**
- **Latencia:** 1 RTT en vez de 2 (el handshake QUIC incluye el de TLS 1.3).
- **Sin head-of-line blocking entre streams:** la pérdida de un stream no frena a los otros, porque la recuperación es por stream y no por conexión.
- **Migración de conexión:** el `Connection ID` sobrevive al cambio de IP y de puerto, lo que arregla el *NAT rebinding* que rompe a TCP.

**Pierde:**
- **CPU por paquete:** todo va cifrado con AEAD, incluso el tráfico que no necesita confidencialidad.
- **Compatibilidad:** cualquier *middlebox* que no entienda QUIC o que filtre UDP/443 rompe la conexión.
- **Despliegue:** 21 % del tráfico, contra 50 % de HTTP/2.""",
"""**Gana:** **latencia** (1 RTT en vez de 2, porque el handshake QUIC incluye el de TLS 1.3), **sin head-of-line blocking entre streams** (la recuperación es por stream y no por conexión) y **migración de conexión** (el `Connection ID` sobrevive al cambio de IP y de puerto, lo que arregla el *NAT rebinding* que rompe a TCP).

**Pierde:** **CPU por paquete** (todo va cifrado con AEAD, incluso lo que no necesita confidencialidad), **compatibilidad** (cualquier *middlebox* que no entienda QUIC o que filtre UDP/443 rompe la conexión) y **despliegue** (21 % del tráfico, contra 50 % de HTTP/2)."""))

# --- autoevaluación 7
R.append(("""Depende de **a qué nivel** se pregunte.

- **A nivel de conexión: SÍ.** En HTTP/1.1 cada objeto va en su propia conexión TCP; si un paquete se pierde, se frena esa conexión entera. HTTP/2 pone todos los streams en **una sola** conexión, así que el número de conexiones (y por lo tanto el de puntos donde una pérdida puede frenar al tráfico que te importa) baja de 5 a 1.
- **Entre streams: NO.** Cada stream se numera, pero **TCP es un flujo ordenado**: si se pierde el segmento del stream 5, el receptor no puede entregar el 6 ni el 7 **de ningún stream**, porque la conexión los tiene en orden.
- **HTTP/3: SÍ en los dos niveles**, porque ya no hay conexión TCP debajo: QUIC numera y recupera **por stream**, así que el stream 5 se pierde y el 6 se entrega igual.""",
"""Depende de **a qué nivel** se pregunte. **A nivel de conexión: SÍ**, porque HTTP/2 baja de 5 conexiones TCP a una sola, así que hay un solo punto donde una pérdida puede frenar al tráfico que te importa. **Entre streams: NO**, porque **TCP es un flujo ordenado**: si se pierde el segmento del stream 5, el receptor no puede entregar el 6 ni el 7 **de ningún stream**. **HTTP/3: SÍ en los dos niveles**, porque ya no hay conexión TCP debajo: QUIC numera y recupera **por stream**."""))

# --- autoevaluación 8
R.append(("""**No es un problema técnico: es un problema de despliegue.** HTTP/3 gana en latencia, en aislamiento de pérdida y en movilidad. Lo que lo frena es que:

1. **El cambio es gradual y la Web es heterogénea.** HTTP/2 solo cambiaba la capa de aplicación sobre un TCP ya desplegado: bastaba actualizar el servidor web. HTTP/3 cambia el transporte y necesita cliente **y** servidor.
2. **Casi todo el tráfico sigue necesitando TCP.** DNS clásico, SSH, servidores de correo, juegos sin migrar. QUIC no reemplaza a TCP: convive con él.
3. **Los *middleboxes* son el cuello de botella.** Cualquier firewall que no entienda QUIC rompe HTTP/3. Se despliega a la velocidad a la que se reemplazan firewalls.
4. **HTTP/2 ya había capturado la mitad.** Con un 50 % del tráfico, no se justifica migrar el resto por una mejora que casi nadie percibe.""",
"""**No es un problema técnico: es un problema de despliegue.** HTTP/3 gana en latencia, en aislamiento de pérdida y en movilidad. Lo que lo frena es que (1) el cambio es gradual y la Web es heterogénea: HTTP/2 solo cambiaba la capa de aplicación sobre un TCP ya desplegado, HTTP/3 cambia el transporte y necesita cliente **y** servidor; (2) casi todo el tráfico sigue necesitando TCP, porque QUIC no lo reemplaza: convive con él; (3) los *middleboxes* son el cuello de botella: cualquier firewall que no entienda QUIC rompe HTTP/3, y se despliega a la velocidad a la que se reemplazan firewalls; y (4) HTTP/2 ya había capturado la mitad del tráfico."""))

# --- 1.1: acortar la columna Notas de CONNECT y PATCH
R.append(("| **CONNECT** | Abre un **túnel TCP** | no | `200` | Seguro e idempotente. Base de los proxies y de HTTPS. |",
          "| **CONNECT** | Abre un **túnel TCP** | no | `200` | Seguro e idempotente. Base de los proxies y de HTTPS. |"))

# --- 3.3: condensar
R.append(("""**La idea común, que es la que hay que saber decir:** cuando **el delimitador vive
dentro del mismo canal que los datos** (no hay longitud explícita), hace falta
**escapar** el delimitador en el emisor y **desescapar** en el receptor. Es el mismo
problema que el **byte stuffing** del PPP (`2003-03 P3`) y que el **bit stuffing** de
Ethernet. **Tres protocolos, tres objetos distintos de relleno: el punto en POP3 y
SMTP, el byte de escape en PPP, el bit en Ethernet.** La razón es siempre la misma:
**ninguno de esos caracteres puede aparecer legítimamente donde se lo proscribe.**""",
"""**La idea común, que es la que hay que saber decir:** cuando **el delimitador vive dentro del mismo canal que los datos** (no hay longitud explícita), hace falta **escapar** el delimitador en el emisor y **desescapar** en el receptor. Es el mismo problema que el **byte stuffing** del PPP (`2003-03 P3`) y el **bit stuffing** de Ethernet. **Tres protocolos, tres objetos de relleno distintos: el punto en POP3 y SMTP, el byte de escape en PPP, el bit en Ethernet.** La razón es siempre la misma: **ninguno de esos caracteres puede aparecer legítimamente donde se lo proscribe.**"""))

for old, new in R:
    if old not in t:
        print("NO ENCONTRADO:", old[:70].replace("\n", " "))
    t = t.replace(old, new, 1)

p.write_text(t, encoding="utf-8", newline="\n")
print("antes:", before, "ahora:", len(t), "ahorro:", before - len(t))
