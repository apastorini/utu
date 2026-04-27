# ⚙️ Clase 06: JavaScript - Web Workers, Streams y Parallelism


**Objetivo:** Dominar transferencia de datos sin almacenamiento, streams y paralelismo en JavaScript  
**Fecha:** 27-4-2026

---

## 📚 PARTE 1: Fundamentos de Protocolos de Red

### 1.1 ¿Qué es un Protocolo de Red?

Un **protocolo de red** es un conjunto de reglas y convenciones que permiten la comunicación entre dispositivos electrónicos a través de una red. Es como un idioma que dos computadoras usan para entenderse.

**¿Por Qué Surge?**
En los años 70s, cada fabricante (IBM, DEC, HP) usaba protocolos propietarios. Una IBM no podía comunicarse con una DEC. Para estandarizar, se creó TCP/IP en 1983 como estándar de ARPANET.

**¿Para Qué Diferentes Protocolos?**
No existe un protocolo "perfecto". Cada uno se diseña para resolver problemas específicos:
- **FTP** → Transferencia de archivos
- **SMTP** → Email
- **HTTP** → Web
- **DNS** → Nombres de dominio

---

### 1.2 TCP vs UDP: Los Dos Pilares

#### TCP (Transmission Control Protocol)

**¿Qué es?**
TCP es un protocolo **orientado a conexión** que garantiza la entrega ordenada y sin errores de datos entre dos dispositivos.

**¿Cómo Funciona?**
```
1. Handshake de tres vías:
   - Cliente → SYN
   - Servidor → SYN-ACK
   - Cliente → ACK
   
2. Los datos se numeran y confirman uno por uno

3. Si un paquete se pierde, se detecta y se reenvía automáticamente

4. Cierre ordenado de la conexión
```

**¿Por Qué Surge?**
Los protocolos anteriores a TCP no garantizaban que los datos llegaran correctamente. TCP resolvió el problema de la fiabilidad en redes.

**¿Para Qué Serving?**
- Navegación web (HTTP/HTTPS)
- Correo electrónico (SMTP, IMAP)
- Transferencia de archivos (FTP, SFTP)
- Cuando la integridad de datos es crítica

#### UDP (User Datagram Protocol)

**¿Qué es?**
UDP es un protocolo **sin conexión** que envía datos sin garantía de entrega ni orden.

**¿Cómo Funciona?**
```
1. Sin handshake - enviar directamente
2. Sin números de secuencia
3. Sin confirmación de entrega
4. Si se pierde un paquete, no se reenvía automáticamente
```

**¿Por Qué Existe?**
TCP tiene overhead: más bytes por paquete, reintentos, esperas. UDP es mucho más rápido cuando la velocidad prima sobre la perfección.

**¿Para Qué Serving?**
- Streaming de video/audio en vivo
- Gaming online
- DNS queries (muy rápidas)
- Videollamadas (VoIP)
- Cuando perder algunos paquetes es aceptable

---

### 1.3 Evolución de HTTP

#### HTTP/1.0 (1991)

**Características:**
- Cada request requiere nueva conexión TCP
- Sin estado entre requests
- Headers simples en texto plano

**Limitación:** Cada request = una nueva conexión = latencia alta

#### HTTP/1.1 (1999)

**Nuevas características:**
- **Keep-Alive**: reuse conexiones TCP
- **Pipelining**: varios requests sin esperar respuesta
- **Hosting virtual**: múltiples sitios en un servidor

**¿Por Qué Surge?**
HTTP/1.0 era muy lento. Cada archivo requería una conexión nueva.

**Limitación:** Los responses deben venir en orden (head-of-line blocking)

#### HTTP/2 (2015)

**Nuevas características:**
- **Multiplexing**: múltiples requests en una conexión
- **Server Push**: el servidor envía recursos proactivamente
- **Header Compression** (HPACK)
- **Binary frames**: más eficiente que texto

**¿Por Qué Surge?**
HTTP/1.1 aún tenía limitaciones. Cargar una página con 100 recursos = 100 requests o pocas conexiones paralelas.

**¿Para Qué Serving?**
- Aplicaciones web modernas
- APIs con muchas llamadas

#### HTTP/3 / QUIC (2022)

**¿Qué es QUIC?**
QUIC es un nuevo protocolo construido sobre UDP que combina seguridad TLS con velocidad UDP.

**Nuevas características:**
- **0-RTT**: conexión instantánea
- **No head-of-line blocking**
- Mejor manejo de pérdida de paquetes
- Funciona en móviles

**¿Por Qué Surge?**
TCP tiene problemas en redes móviles. QUIC fue diseñado específicamente para resolver esto.

---

### 1.4 Protocolos de Aplicación Modernos

#### WebSockets (2011)

**¿Qué es?**
WebSockets es un protocolo que permite comunicación **bidireccional full-duplex** entre cliente y servidor sobre una única conexión TCP.

**¿Por Qué Surge?**
HTTP es request-response: el cliente siempre inicia la comunicación. Para chat, gaming, o apps en tiempo real, necesitamos que el servidor inicie mensajes.

**¿Para Qué Serving?**
- Chat en tiempo real
- Juegos multiplayer
--notificaciones en vivo
- Colaboración en documentos

#### gRPC (2015)

**¿Qué es?**
gRPC es un framework de Remote Procedure Call (RPC) que usa **Protocol Buffers** para codificar datos de manera binaria y eficiente.

**¿Por Qué Surge?**
REST usa JSON que es texto y verboso. Para microservicios donde la velocidad importa, JSON añade overhead significativo.

**¿Para Qué Serving?**
- Microservicios internos
- APIs de alto rendimiento
- Comunicación entre servicios

```protobuf
// Ejemplo de Protocol Buffers
syntax = "proto3";

message Evento {
    int32 id = 1;
    string titulo = 2;
    double precio = 3;
}

service EventoService {
    rpc ObtenerEvento (EventoRequest) returns (Evento);
    rpc StreamEventos (Empty) returns (stream Evento);
}
```

#### Server-Sent Events (SSE)

**¿Qué es?**
SSE permite que un servidor envíe actualizaciones a un cliente a través de una conexión HTTP estándar.

**¿Por Qué Surge?**
WebSockets bidireccionales son complejos. Para casos donde solo el servidor necesita enviar datos, SSE es más simple.

**¿Para Qué Serving?**
- Notificaciones
- Actualizaciones de precios en tiempo real
- monitoring de sistemas

#### WebRTC (2011)

**¿Qué es?**
WebRTC (Web Real-Time Communication) permite comunicación **P2P directa** entre navegadores sin pasar por un servidor.

**¿Por Qué Surge?**
Para videollamadas, si todo pasara por servidor, el costo en servidor sería enorme. P2P reduce costos drásticamente.

**¿Para Qué Serving?**
- Videollamadas
- Transferencia de archivos P2P
- Gaming P2P
- Voz sobre IP

**Comparativa:**

| Protocolo | Bidireccional | Tipo | Cuando Usar |
|----------|---------------|------|-------------|
| HTTP/REST | No | Request/Response | APIs CRUD |
| WebSockets | Sí | Stream | Chat, Games |
| gRPC | Método | RPC | Microservicios |
| SSE | No | Push | Updates |
| WebRTC | P2P | Direct | VoIP, archivos |

---

## 📚 PARTE 2: Streams - Fundamentos Teóricos

### 2.1 ¿Qué es un Stream?

Un **stream** es una secuencia de datos que se transmite progresivamente, pedazo por pedazo, en lugar de esperar a tener todos los datos disponibles.

**¿Por Qué Surge?**
En aplicaciones antiguas, primero descargabas todo el archivo a memoria, luego procesabas. Si el archivo era huge (GBs), el programa colapsaba. Stream permite procesar mientras llegan los datos.

**¿Para Qué Serving?**
- Procesar archivos huge sin memory overflow
- Procesamiento en tiempo real (video, audio)
- Transferencia de datos eficiente
- Backpressure natural

### 2.2 Concepto de Stream Pipeline

Un stream típicamente tiene tres partes:

```
┌───────────────────────────────────────────────────────────────────┐
│                  STREAM PIPELINE                         │
├──────────────────────────────────────��────────────────────────────┤
│                                                           │
│   ┌──────────┐    ┌──────────────┐    ┌──────────┐            │
│   │PRODUCER │ ──►│  TRANSFORM  │ ──►│CONSUMER │            │
│   │(Source) │    │  (Process)  │    │ (Sink)   │            │
│   └──────────┘    └──────────────┘    └──────────┘            │
│        │                                       │                │
│        ▼                                       ▼                │
│   Datos raw                                Datos                  │
│   fluyendo                                procesados             │
│                                                           │
│   EJEMPLO:                                                │
│   Producer: Archivo en disco                               │
│   Transform: Compresión ZIP                              │
│   Consumer: Guardar archivo comprimido                    │
└───────────────────────────────────────────────────────────────────┘
```

### 2.3 Tipos de Streams

#### Readable Stream (Flujo de Lectura)
Emite datos que pueden ser leídos.

**Ejemplo:** Leer un archivo de 10GB chunk por chunk

#### Writable Stream (Flujo de Escritura)
Recibe datos para escribir.

**Ejemplo:** Escribir respuestas HTTP chunk por chunk

#### Transform Stream (Flujo de Transformación)
Procesa datos en el medio del pipeline.

**Ejemplo:** Comprimir, encriptar, parser JSON

#### Duplex Stream (Flujo Doble)
Permite lectura y escritura.

**Ejemplo:** Conexión WebSocket

---

### 2.4 Backpressure: El Problema del Consumidor Lento

**¿Qué es?**
Ocurre cuando el consumidor no puede procesar tan rápido como el Producer genera datos. Sin control, la memoria se satura.

**¿Cómo se Resuelve?**
El consumidor indica al Producer que reduzca la velocidad.

```javascript
// Sin backpressure (peligroso)
const producer = getInfiniteData();
const consumer = slowProcessor();
while (true) {
    const data = await producer.read();
    await consumer.process(data);  // Acumula en memoria si es lento
}

// Con backpressure (seguro)
const reader = stream.getReader();
while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    await consumer.process(value);
    // Si consumer no puede más, reader.read() espera naturalmente
}
```

---

### 2.5 Streams en JavaScript

#### Stream API Nativa del Navegador

```javascript
// READABLE STREAM - Fuente de datos
const readable = new ReadableStream({
    start(controller) {
        // Inicializar el stream
        controller.enqueue('chunk 1');
        controller.enqueue('chunk 2');
        controller.enqueue('chunk 3');
        controller.close(); // Terminar stream
    },
    pull(controller) {
        // Llamado cuando el buffer necesita más datos
    },
    cancel(reason) {
        // Cleanup si se cancela
    }
});

// LEER DEL STREAM
const reader = readable.getReader();
while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    console.log('Leído:', value);
}

// WRITABLE STREAM - Destino
const writable = new WritableStream({
    write(chunk) {
        console.log('Escribiendo:', chunk);
    },
    close() {
        console.log('Stream cerrado');
    },
    abort(reason) {
        console.error('Error:', reason);
    }
});

// ESCRIBIR AL STREAM
const writer = writable.getWriter();
await writer.write('Hola');
await writer.write('Mundo');
await writer.close();

// TRANSFORM STREAM - Transformación
const uppercase = new TransformStream({
    transform(chunk, controller) {
        controller.enqueue(chunk.toUpperCase());
    }
});

// PIPE CHAIN - Encadenar streams
const fileStream = file.stream();
const textStream = fileStream.pipeThrough(new TextDecoderStream());
const lines = textStream.pipeThrough(new TransformStream(lineSplitter));
lines.pipeTo(writableStream);
```

---

### 2.6 Streams en Java (Reactor/Project Reactor)

**¿Qué es Project Reactor?**
Reactor es una biblioteca reactiva para Java que implementa Streams asíncronos. Es la base de Spring WebFlux.

**¿Por Qué Surge?**
Los streams síncronos de Java bloquean el thread. Reactor permite procesamiento no-bloqueante, ideal para sistemas de alta concurrencia.

**¿Para Qué Serving?**
- Aplicaciones Spring WebFlux
- Microservicios reactivos
- Procesamiento asíncrono de alto rendimiento

```java
import reactor.core.publisher.*;

// FLUX: 0 a N elementos (similar a Observable o Stream)
Flux<Integer> numeros = Flux.just(1, 2, 3, 4, 5);

// Transformar
Flux<Integer> duplicados = numeros
    .map(n -> n * 2)
    .filter(n -> n > 5);

// De archivo
Flux<String> lineas = Flux.using(
    () -> Files.lines(Paths.get("archivo.txt")),
    Flux::from,
    Stream::close
);

// PROCESSAMIENTO PARALELO
Flux<Integer> paralelo = numeros
    .parallel(4)
    .runOn(Schedulers.parallel())
    .map(n -> procesamientoPesado(n))
    .sequential();

// MONO: 0 a 1 elemento
Mono<Evento> evento = Mono.fromCallable(() -> buscarEvento(1))
    .subscribeOn(Schedulers.boundedElastic());
```

---

### 2.7 Streams en Python (asyncio)

**¿Qué es asyncio?**
asyncio es una biblioteca de Python para escribir código concurrente usando async/await. Es la base de frameworks como aiohttp.

**¿Por Qué Surge?**
Python tradicional es single-threaded. asyncio permite manejar miles de conexiones simultáneas sin crear un thread por cada una.

**¿Para Qué Serving?**
- Servidores web de alto rendimiento (aiohttp, FastAPI)
- scrapersweb
- APIs asíncronas

```python
import asyncio

# SERVER DE STREAMS
async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    print(f"Conexión desde {addr}")
    
    while True:
        data = await reader.read(1024)
        if not data:
            break
        
        response = process(data)
        writer.write(response)
        await writer.drain()
    
    writer.close()

async def main():
    server = await asyncio.start_server(
        handle_client, 'localhost', 8888
    )
    async with server:
        await server.serve_forever()

asyncio.run(main())

# AIOFILES - STREAMS DE ARCHIVOS
import aiofiles

async def procesar_archivo():
    async with aiofiles.open('input.txt', 'r') as f:
        async for linea in f:
            await proceso(linea.strip())
```

### 2.8 Comparación de Streams

| Característica | JS | Java (Reactor) | Python (asyncio) |
|--------------|-----|----------------|-----------------|
| **Tipo** | Async | Sync/Async | Async |
| **Backpressure** | .cancel() | request(N) | .drain() |
| **Transform** | TransformStream | .map() | async gen |
| **Parallel** | Worker | .parallel() | gather() |
| **Error handling** | try/catch | .error() | try/except |
| **Buffered** | yes | yes | partial |
| **Memory** | Streams API | Schedulers | buffer config |

---

## 📚 PARTE 3: Transferencia SIN Almacenamiento

### 3.1 Escenario: Transferencia P2P Directa

**¿Qué es?**
Transferencia peer-to-peer (P2P) directa significa que los datos van directamente de un usuario a otro sin pasar por un servidor de almacenamiento.

**¿Por Qué Surge?**
Los servidores de almacenamiento tienen problemas:
- Costo de almacenamiento en la nube
- Privacy: terceros tienen acceso
- Velocidad depende del servidor

**¿Para Qué Serving?**
- Compartir archivos grandes sin costo de almacenamiento
- Privacidad extrema (nunca toca servidor)
- Transferencia en tiempo real

```
┌────────────────────────────────────────────────────────────────────┐
│     TRANSFERENCIA P2P DIRECTA SÍN ALMACENAMIENTO           │
├────────────────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐                │
│  │ Usuario │    │         │    │ Usuario │                │
│  │    A   │───►│  P2P   │◄───│    B   │                │
│  └─────────┘    │ Direct  │    └─────────┘                │
│       ▲         │         │         ▼                        │
│       │        (sin servidor de archivos)                      │
│       │         │         │                                │
│  Archivo       WebRTC         Archivo                          │
│  origen       DataChannel   destino                         │
│                                                         │
│  VENTAJAS:                                             │
│  ✓ Privacidad: archivo nunca toca servidor               │
│  ✓ Velocidad: transferencia directa P2P             │
│  ✓ Costo: sin almacenamiento en la nube                  │
│  ✓ Privacidad: encryptado P2P                              │
│                                                         │
│  DESVENTAJAS:                                        │
│  ✗ Ambos usuarios deben estar online                 │
│  ✗ Se necesita servidor de señalización            │
│  ✗ Limitado por bandwidth de conexión directa         │
└────────────────────────────────────────────────────────────────────┘
```

---

### 3.2 WebRTC DataChannel

**¿Qué es?**
RTCDataChannel es una API que permite transferir datos arbitrarios entre peers directamente.

**¿Por Qué Surge?**
WebRTC originalmente solo soportaba audio/video. DataChannel permite datos arbitrary P2P.

**¿Para Qué Serving?**
- Transferencia de archivos
- Chat P2P
- Gaming P2P
- Compartir cualquier dato

```javascript
// CREAR DATACHANNEL
const pc = new RTCPeerConnection(config);
const dataChannel = pc.createDataChannel("archivos");

dataChannel.onopen = () => console.log("Canal abierto");
dataChannel.onmessage = (event) => console.log("Recibido:", event.data);

// ENVIAR DATOS
const file = document.querySelector('input[type="file"]').files[0];
dataChannel.send(file); // Automatically chunks large data

// RECIBIR DATOS
dataChannel.binaryType = "arraybuffer";
dataChannel.onmessage = (event) => {
    const data = event.data;
    // procesar chunk
};
```

---

### 3.3 Sistema de Transfer con Chunked Upload

**¿Qué es?**
Subir archivos en chunks pequeños, procesando cada chunk inmediatamente sin almacenar el archivo completo.

**¿Por Qué Surge?**
Si subimos un archivo de 1GB, esperar a que termine para procesarlo es ineficiente. Procesando chunk por chunk es más rápido.

**¿Para Qué Serving?**
- Procesamiento de video
- Validación progresiva
- Compresión en tiempo real
- Detección de malware

```javascript
// CHUNKED UPLOAD SERVER (Node.js)
app.post('/upload/:session/:chunk', async (req, res) => {
    const { session, chunk } = req.params;
    const chunkData = req.body;
    
    // Procesar inmediatamente sin esperar a que termine upload
    await processChunk(chunkData, chunk, session);
    
    res.json({ success: true, chunk: parseInt(chunk), processed: true });
});

async function processChunk(chunkData, chunkIndex, sessionId) {
    // Validar, comprimir, escanear...
    return { processed: true };
}
```

---

## 📚 PARTE 4: Web Workers - Fundamentos

### 4.1 ¿Qué es un Web Worker?

Un **Web Worker** es un script JavaScript que se ejecuta en un thread separado en segundo plano, independiente del thread principal del navegador.

**¿Por Qué Surge?**
JavaScript en el navegador es single-threaded. Si haces cálculos pesados, la UI se congela. Workers permiten procesamiento paralelo sin congelar la UI.

**¿Para Qué Serving?**
- Cálculos pesados
- Procesamiento de imágenes/video
- Parseo de grandes archivos JSON
- Paralelización de tareas

---

### 4.2 Tipos de Workers

#### Dedicated Worker
Un worker dedicado funciona solo con el script que lo creó.

```javascript
// main.js
const worker = new Worker('worker.js');

// worker.js
self.onmessage = function(event) {
    const result = heavyComputation(event.data);
    self.postMessage(result);
};
```

#### Shared Worker
Un worker compartido entre múltiples páginas del mismo origen.

```javascript
// main.js - todas las páginas comparten
const worker = new SharedWorker('shared.js');

// shared.js
const connections = [];
self.onconnect = (e) => {
    connections.push(e.ports[0]);
};
self.onmessage = (e) => {
    // Broadcast a todas las conexiones
    connections.forEach(port => port.postMessage(e.data));
};
```

#### Service Worker
Un worker que actúa como proxy de red, permitiendo features offline.

```javascript
// service-worker.js
self.addEventListener('fetch', (event) => {
    event.respondWith(
        caches.match(event.request)
            .then(response => response || fetch(event.request))
    );
});
```

---

### 4.3 Comunicación: postMessage

```javascript
// ENVIAR DESDE MAIN A WORKER
const worker = new Worker('worker.js');

worker.postMessage({ data: [1, 2, 3] });

worker.onmessage = function(event) {
    console.log('Resultado:', event.data);
};

// ENVIAR DESDE WORKER A MAIN
// worker.js
self.onmessage = function(event) {
    const data = event.data;
    const result = process(data);
    self.postMessage(result);
};
```

---

### 4.4 MessageChannel

**¿Qué es?**
MessageChannel crea un canal de comunicación bidireccional entre contextos.

**¿Por Qué Surge?**
postMessage envía mensajes a un worker específico. MessageChannel permite que el worker responda por un canal dedicado.

```javascript
// MAIN THREAD
const channel = new MessageChannel();
const port1 = channel.port1;
const port2 = channel.port2;

port1.onmessage = (e) => console.log('Desde worker:', e.data);
port1.start();

// Enviar port2 al worker
const worker = new Worker('worker.js');
worker.postMessage(null, [port2]);

// worker.js
self.onmessage = function(event) {
    const port = event.ports[0];
    port.onmessage = (e) => {
        port.postMessage({ ack: true });
    };
    port.start();
};
```

---

### 4.5 Transferable Objects

**¿Qué es?**
Un transferable object es un objeto cuyo ownership se transfiere entre contexts, no se copia (mucho más rápido).

**¿Por Qué Surge?**
Enviar datos grandes por postMessage copia los datos, lo cual toma tiempo. Transfer ownership es instantáneo.

**¿Para Qué Serving?**
- Arrays grandes
- Buffers de imágenes
- Cualquier dato >1MB

```javascript
// SIN TRANSFERABLE (copia ~10ms por MB)
const array = new Uint8Array(10 * 1024 * 1024); // 10MB
worker.postMessage({ data: array }); // Copia 10ms

// CON TRANSFERABLE (casi instantáneo)
const buffer = array.buffer;
worker.postMessage({ data: buffer }, [buffer]);
// Después de transfer, buffer.byteLength === 0
```

---

## 📚 PARTE 5: SharedArrayBuffer y Atomics

### 5.1 ¿Qué es SharedArrayBuffer?

SharedArrayBuffer es un ArrayBuffer que puede ser compartido entre multiple workers y el main thread.

**¿Por Qué Surge?**
postMessage tiene overhead de copia. Shared memory permite acceso directo a datos compartidos sin copiar.

**¿Para Qué Serving?**
- Contadores concurrentes
- Estado compartido entre workers
- Sincronización de datos

**Precaución:**
Requiere Cross-Origin Isolation:
```http
Cross-Origin-Opener-Policy: same-origin
Cross-Origin-Embedder-Policy: require-corp
```

---

### 5.2 Atomics

**¿Qué son Atomics?**
Atomics es un objeto que proporciona operaciones atómicas para SharedArrayBuffer.

**¿Por Qué Surge?**
Sin operaciones atómicas, múltiples workers escribiendo al mismo tiempo = datos corruptos (race conditions).

**¿Para Qué Serving?**
- Crear mutexes
- Contadores thread-safe
- Sincronización entre workers

```javascript
const sharedBuffer = new SharedArrayBuffer(1024);
const sharedArray = new Int32Array(sharedBuffer);

// ESCRITURA ATÓMICA
Atomics.store(sharedArray, 0, 42);
const value = Atomics.load(sharedArray, 0);

// OPERACIONES ATÓMICAS
Atomics.add(sharedArray, 0, 1);    // += 1
Atomics.sub(sharedArray, 0, 1);    // -= 1
Atomics.and(sharedArray, 0, 0b1111); // bitwise AND
Atomics.or(sharedArray, 0, 0b1111);  // bitwise OR
Atomics.xor(sharedArray, 0, 0b1111); // bitwise XOR

// COMPARE-AND-SWAP (solo cambia si valor es igual)
const old = Atomics.compareExchange(sharedArray, 0, 42, 100);
```

---

### 5.3 Synchronization

```javascript
// ESPERAR HASTA QUE UN VALOR CAMBIE
const ready = new Int32Array(new SharedArrayBuffer(400));

// En un worker
Atomics.wait(ready, 0, 0); // Espera hasta que ready[0] != 0

// En otro worker o main
Atomics.store(ready, 0, 1);
Atomics.notify(ready, 0, 1); // Despertar wait()

// CON TIMEOUT
try {
    Atomics.wait(ready, 0, 0); // Espera infinita
} catch {
    Atomics.wait(ready, 0, 0, 1000); // Timeout 1s
}
```

---

### 5.4 Race Conditions

**¿Qué es?**
Una race condition ocurre cuando múltiples threads acceden a datos compartidos y el resultado depende del orden de ejecución.

**Problema:**
```javascript
// Sin coordinación - RACE CONDITION
let counter = 0;

// Worker 1: counter++
let temp1 = counter;
counter = temp1 + 1;

// Worker 2: counter++ (más lento)
let temp2 = counter;
counter = temp2 + 1;

// Resultado: counter = 1 (debería ser 2!)
```

**Solución con Atomics:**
```javascript
// Con mutex usando Atomics
const lock = new Int32Array(new SharedArrayBuffer(400));

function incrementaSeguro() {
    // Adquirir lock (spin lock)
    while (Atomics.compareExchange(lock, 0, 0, 1) !== 0) {
        // Esperar
    }
    
    // Sección crítica
    counter++;
    
    // Liberar lock
    Atomics.store(lock, 0, 0);
}
```

---

## 📚 PARTE 6: Casos de Uso Reales

### 6.1 Procesamiento de Imágenes

```javascript
// WORKER: Aplicar filtro a imagen
self.onmessage = function(event) {
    const { imageData, filter } = event.data;
    const data = imageData.data;
    
    for (let i = 0; i < data.length; i += 4) {
        const r = data[i], g = data[i+1], b = data[i+2];
        
        switch(filter) {
            case 'grayscale':
                const avg = (r + g + b) / 3;
                data[i] = data[i+1] = data[i+2] = avg;
                break;
            case 'sepia':
                data[i] = Math.min(255, r * 0.393 + g * 0.769 + b * 0.189);
                data[i+1] = Math.min(255, r * 0.349 + g * 0.686 + b * 0.168);
                data[i+2] = Math.min(255, r * 0.272 + g * 0.534 + b * 0.131);
                break;
        }
    }
    
    // Devolver con transferable
    self.postMessage({ imageData }, [imageData.data.buffer]);
};

// MAIN: Usar worker
async function applyFilter(imageData, filter) {
    const worker = new Worker('image-worker.js');
    const buffer = imageData.data.buffer.slice(0); // Transferible
    
    return new Promise(resolve => {
        worker.onmessage = (e) => resolve(e.data.imageData);
        worker.postMessage({ imageData, filter }, [buffer]);
    });
}
```

### 6.2 Word Counter Paralelo

```javascript
// WORKER
self.onmessage = function(event) {
    const { text } = event.data;
    const words = text.toLowerCase().split(/\s+/);
    const counts = {};
    
    for (const word of words) {
        const clean = word.replace(/[^a-z]/g, '');
        if (clean) {
            counts[clean] = (counts[clean] || 0) + 1;
        }
    }
    
    self.postMessage(counts);
};

// MAIN: Paralelizar
async function parallelCount(text, numWorkers = 4) {
    const chunkSize = Math.ceil(text.length / numWorkers);
    
    // Crear workers
    const workers = [];
    for (let i = 0; i < numWorkers; i++) {
        const start = i * chunkSize;
        const end = Math.min(start + chunkSize, text.length);
        const chunk = text.substring(start, end);
        
        const worker = new Worker('counter.js');
        worker.postMessage({ text: chunk });
        
        workers.push(new Promise(resolve => {
            worker.onmessage = (e) => resolve(e.data);
        }));
    }
    
    // Combinar resultados
    const results = await Promise.all(workers);
    const merged = {};
    for (const result of results) {
        for (const [word, count] of Object.entries(result)) {
            merged[word] = (merged[word] || 0) + count;
        }
    }
    
    return merged;
}
```

---

## 📚 PARTE 7: Ejercicios Prácticos

### Ejercicio 1: Chat P2P
- Objetivo: Crear chat sin servidor中间
- Pistas: RTCPeerConnection, RTCDataChannel

### Ejercicio 2: Image Processor
- Objetivo: Procesar imagen con múltiples workers
- Pistas: Dividir imagen en regiones

### Ejercicio 3: File Uploader Resumable
- Objetivo: Upload que se puede reanudar
- Pistas: Chunked upload + checkpoint

### Ejercicio 4: Shared Counter
- Objetivo: Contador thread-safe
- Pistas: SharedArrayBuffer + Atomics

---

## ✅ Checklist de la Clase

- [ ] TCP/UDP fundamentos y cuándo usar cada uno
- [ ] Evolución de HTTP (1.0 → 1.1 → 2 → 3)
- [ ] gRPC, WebSockets, SSE, WebRTC
- [ ] Streams: producer → transform → consumer
- [ ] Streams en JavaScript, Java, Python
- [ ] Backpressure
- [ ] Transferencia P2P sin almacenamiento
- [ ] Web Workers: postMessage, MessageChannel
- [ ] Transferable objects
- [ ] SharedArrayBuffer y Atomics
- [ ] Race conditions y cómo prevenirlas
- [ ] Casos de uso reales