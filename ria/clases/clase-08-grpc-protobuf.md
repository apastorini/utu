# 📱 Clase 08: gRPC y Protocol Buffers

**Duración:** 4 horas  
**Objetivo:** Dominar la comunicación entre servicios con gRPC y Protocol Buffers  
**Proyecto:** Sistema de eventos con microservicios gRPC

---

## 📚 Contenido Teórico

### 1. Fundamentos de gRPC

#### 1.1 ¿Qué es gRPC?

**gRPC (Google Remote Procedure Call)** es un framework de comunicación entre servicios desarrollado por Google en 2015 y liberado como código abierto. Permite que un programa cliente ejecute funciones en un programa servidor located en otra máquina, como si fuera una llamada local.

**Características fundamentales:**

| Característica | Descripción |
|----------------|-------------|
| **Alto rendimiento** | Hasta 10x más rápido que REST gracias a HTTP/2 |
| **Tipado fuerte** | Contratos definidos que comparten cliente y servidor |
| **Streaming** | Soporte para streams bidireccionales |
| **Generación de código** | Código cliente/servidor automáticocross-language |
| **Multilenguaje** | Soporta 11+ lenguajes de programación |

#### 1.2 ¿Por qué usar gRPC en lugar de REST?

**REST usa HTTP/1.1:**
- Cada request requiere una nueva conexión TCP (overhead)
- No soporte nativo para multiplexing
- Formato JSON texto-espeso (más bytes)
- No hay contrato automático entre servicios

**gRPC usa HTTP/2:**
- Conexiones persistentes (reutiliza conexiones)
- Multiplexing: múltiples requests en una sola conexión
- Binary framing (más eficiente que texto)
- Server push: el servidor puede enviar datos sin esperar request
- Header compression con HPACK

```
HTTP/1.1 (REST):          HTTP/2 (gRPC):
┌─────┐                   ┌─────────────────┐
│ req │ ──────────────►   │ Request 1       │
└─────┘                   │ Request 2       │
┌─────┐                   │ Request 3       │
│ req │ ──────────────►   │ (en paralelo)   │
└─────┘                   └─────────────────┘
```

#### 1.3 Tipos de comunicación en gRPC

**Unary (Unario):** El cliente envía una solicitud y recibe una respuesta.
```protobuf
rpc GetUsuario(UsuarioRequest) returns (Usuario);
```
Similar a una llamada REST GET normal.

**Server Streaming:** El cliente envía una solicitud, el servidor devuelve un stream de mensajes.
```protobuf
rpc GetNotificaciones(UsuarioRequest) returns (stream Notificacion);
```
Útil para: feeds en tiempo real, logs, actualizaciones.

**Client Streaming:** El cliente envía un stream de mensajes, el servidor responde con un mensaje.
```protobuf
rpc SubirArchivos(stream Fragmento) returns (UploadResult);
```
Útil para: uploads grandes, procesamiento por lotes.

**Bidirectional Streaming:** Ambos envíen streams de forma independiente.
```protobuf
rpc Chat(stream Mensaje) returns (stream Mensaje);
```
Útil para: chat en tiempo real, colaboración.

---

### 2. Protocol Buffers (ProtoBuf)

#### 2.1 ¿Qué son Protocol Buffers?

Protocol Buffers es un mecanismo de serialización (convertir objetos a bytes) desarrollado por Google. Es como JSON pero más eficiente, rápido y con tipado fuerte.

**Ventajas sobre JSON:**

| Aspecto | JSON | Protocol Buffers |
|---------|------|------------------|
| Tamaño | Grande (texto) | Pequeño (binario) |
| Velocidad | Lento (parseo texto) | Rápido (binario) |
| Tipado | Dinámico | Estático/fuerte |
| Schema | No tiene | Obligatorio |
| Legibilidad | Humano readable | No (binario) |

#### 2.2 Sintaxis de Protocol Buffers

```protobuf
// Versión del lenguaje
syntax = "proto3";

// Paquete (namespace)
package evento;

// Definición de mensajes
message Evento {
    string id = 1;           // Campo 1
    string titulo = 2;       // Campo 2
    string descripcion = 3;  // Campo 3
    string fecha = 4;
    string ubicacion = 5;
    double precio = 6;
    int32 capacidad = 7;
    string categoria = 8;
    bool activo = 9;
}

// Tipos de datos disponibles:
message TiposDemo {
    // Números
    int32    entero = 1;    // Entero de 32 bits
    int64    largo = 2;     // Entero de 64 bits
    float    flotante = 3;  // Número decimal
    double   doble = 4;     // Número decimal doble
    
    // Strings y bytes
    string   texto = 5;     // Cadena de texto UTF-8
    bytes    datos = 6;     // Datos binarios
    
    // Booleanos
    bool     activo = 7;    // true/false
    
    // Enumeraciones
    Estado   estado = 8;   // Valores predefinidos
    
    // Tipos anidados
    SubMessage sub = 9;     // Message dentro de message
    
    // Mapas
    map<string, string> etiquetas = 10;
    
    // Oneof (uno de varios tipos)
    oneof tipo_conexion {
        string ip = 11;
        string hostname = 12;
    }
}

// Enumeración
enum Estado {
    ESTADO_DESCONOCIDO = 0;
    ACTIVO = 1;
    INACTIVO = 2;
    ELIMINADO = 3;
}

// Message anidado
message SubMessage {
    string nombre = 1;
}
```

#### 2.3 Field Numbers (Números de Campo)

Cada campo tiene un **número único** que lo identifica. Estos números son:
- **Permanentes:** No cambiar nunca en producción
- **Únicos:** No puede haber dos campos con el mismo número
- **1-15:** Usar para campos frecuentes (ocupan 1 byte)
- **16-2047:** Usar para campos menos frecuentes (ocupan 2 bytes)

```protobuf
// Malo: cambiar números en producción
message Evento {
    string id = 1;
    string titulo = 2;  // Si cambias a "titulo = 5", rompe compatibilidad
}

// Bueno: campos frecuentes primero
message Evento {
    string id = 1;           // Frecuente (1 byte)
    string titulo = 2;       // Frecuente (1 byte)
    repeated string tags = 15;   // Menos frecuente (2 bytes)
}
```

#### 2.4 Reglas de los campos

```protobuf
message Evento {
    // optional: campo opcional (implícito en proto3)
    optional string titulo = 1;
    
    // repeated: campo que puede tener múltiples valores (array)
    repeated string fotos = 2;
    
    // map: par clave-valor
    map<string, int32> precios = 3;
}
```

---

### 3. Servicios gRPC

#### 3.1 Definición de Servicios

Un **servicio** en gRPC define los métodos remotos disponibles:

```protobuf
// Servicio de eventos
service EventoService {
    // Unary: request → response
    rpc CrearEvento (CrearEventoRequest) returns (Evento);
    rpc ObtenerEvento (ObtenerEventoRequest) returns (Evento);
    rpc ActualizarEvento (ActualizarEventoRequest) returns (Evento);
    rpc EliminarEvento (EliminarEventoRequest) returns (EliminarEventoResponse);
    
    // Server streaming
    rpc ListarEventos (ListarEventosRequest) returns (stream Evento);
    
    // Client streaming
    rpc ProcesarReservas (stream ReservaRequest) returns (ProcesoResponse);
    
    // Bidirectional streaming
    rpc ChatSoporte (stream Mensaje) returns (stream Mensaje);
}
```

#### 3.2 Keys del Message Request/Response

```protobuf
// Request para crear evento
message CrearEventoRequest {
    string titulo = 1;
    string descripcion = 2;
    string fecha = 3;
    string ubicacion = 4;
    double precio = 5;
    int32 capacidad = 6;
    string categoria = 7;
    string imagen = 8;
}

// Response de evento
message Evento {
    string id = 1;
    string titulo = 2;
    string descripcion = 3;
    string fecha = 4;
    string ubicacion = 5;
    double precio = 6;
    int32 capacidad = 7;
    int32 vendidos = 8;
    string categoria = 9;
    bool activo = 10;
    string created_at = 11;
    string updated_at = 12;
}

// Response con paginación
message ListaEventosResponse {
    repeated Evento eventos = 1;
    int32 total = 2;
    int32 pagina = 3;
    int32 total_paginas = 4;
}
```

---

## 💻 Contenido Práctico

### 4. Implementación en Node.js

#### 4.1 Estructura del Proyecto

```
proyecto-grpc/
├── proto/
│   └── evento.proto
├── server/
│   ├── index.js
│   └── package.json
├── client/
│   ├── index.js
│   └── package.json
└── generated/
    └── (archivos generados)
```

#### 4.2 Instalación de Dependencias

```bash
# En server y client
npm install grpc @grpc/proto-loader

# Opcional: para proto3 conLong strings como String
npm install protobufjs
```

#### 4.3 Generar Código desde Proto

```bash
# Generar código JavaScript
npx proto-loader-gen-types --protoDir=./proto --outDir=./generated evento.proto

# O usar grpc-tools
npm install -D grpc-tools
npx grpc_tools_node_protoc --js_out=generate_accessors:./generated --grpc_out=./generated -I./proto evento.proto
```

#### 4.4 Servidor gRPC

```javascript
// server/index.js
const grpc = require('grpc');
const protoLoader = require('@grpc/proto-loader');
const path = require('path');

// Cargar el archivo .proto
const PROTO_PATH = path.join(__dirname, '../proto/evento.proto');

const packageDefinition = protoLoader.loadSync(PROTO_PATH, {
    keepCase: false,
    longs: String,
    enums: String,
    defaults: true,
    oneofs: true
});

// Cargar el paquete
const eventoProto = grpc.loadPackageDefinition(packageDefinition);

// Base de datos en memoria
const eventos = new Map();

// Implementación del servicio
const eventoService = {
    // UNARY - Crear evento
    crearEvento: (call, callback) => {
        const id = Date.now().toString();
        const evento = {
            id,
            titulo: call.request.titulo,
            descripcion: call.request.descripcion,
            fecha: call.request.fecha,
            ubicacion: call.request.ubicacion,
            precio: call.request.precio,
            capacidad: call.request.capacidad,
            categoria: call.request.categoria,
            vendidos: 0,
            activo: true,
            createdAt: new Date().toISOString(),
            updatedAt: new Date().toISOString()
        };
        
        eventos.set(id, evento);
        console.log(`✅ Evento creado: ${evento.titulo}`);
        
        callback(null, evento);
    },
    
    // UNARY - Obtener evento por ID
    obtenerEvento: (call, callback) => {
        const evento = eventos.get(call.request.id);
        
        if (!evento) {
            callback({
                code: grpc.status.NOT_FOUND,
                message: 'Evento no encontrado'
            });
            return;
        }
        
        callback(null, evento);
    },
    
    // UNARY - Actualizar evento
    actualizarEvento: (call, callback) => {
        const { id, ...datos } = call.request;
        
        if (!eventos.has(id)) {
            callback({
                code: grpc.status.NOT_FOUND,
                message: 'Evento no encontrado'
            });
            return;
        }
        
        const eventoActualizado = {
            ...eventos.get(id),
            ...datos,
            updatedAt: new Date().toISOString()
        };
        
        eventos.set(id, eventoActualizado);
        console.log(`✅ Evento actualizado: ${id}`);
        
        callback(null, eventoActualizado);
    },
    
    // UNARY - Eliminar evento
    eliminarEvento: (call, callback) => {
        const { id } = call.request;
        
        if (!eventos.has(id)) {
            callback({
                code: grpc.status.NOT_FOUND,
                message: 'Evento no encontrado'
            });
            return;
        }
        
        eventos.delete(id);
        console.log(`✅ Evento eliminado: ${id}`);
        
        callback(null, { success: true, message: 'Evento eliminado' });
    },
    
    // SERVER STREAMING - Listar eventos
    listarEventos: (call, callback) => {
        const { pagina, limite, categoria } = call.request;
        
        let lista = Array.from(eventos.values());
        
        // Filtrar por categoría si se especifica
        if (categoria && categoria !== '') {
            lista = lista.filter(e => e.categoria === categoria);
        }
        
        const skip = ((pagina || 1) - 1) * (limite || 10);
        const eventosPagina = lista.slice(skip, skip + (limite || 10));
        
        // Enviar cada evento como stream
        eventosPagina.forEach(evento => {
            call.write(evento);
        });
        
        call.end();
        
        // Responder con metadatos de paginación
        callback(null, {
            total: lista.length,
            pagina: pagina || 1
        });
    },
    
    // CLIENT STREAMING - Procesar reservas
    procesarReservas: (call, callback) => {
        let totalMonto = 0;
        let cantidad = 0;
        
        call.on('data', (reserva) => {
            totalMonto += reserva.cantidad * reserva.precioUnitario;
            cantidad += reserva.cantidad;
            console.log(`📝 Reserva procesada: ${reserva.eventoId}`);
        });
        
        call.on('end', () => {
            callback(null, {
                totalProcesado: totalMonto,
                cantidadProcesada: cantidad,
                estado: 'completado'
            });
        });
    },
    
    // BIDIRECTIONAL STREAMING - Chat
    chat: (call) => {
        call.on('data', (mensaje) => {
            const respuesta = {
                id: Date.now().toString(),
                texto: `Eco: ${mensaje.texto}`,
                timestamp: new Date().toISOString(),
                remitente: 'servidor'
            };
            
            call.write(respuesta);
        });
        
        call.on('end', () => {
            call.end();
        });
    }
};

// Crear el servidor
const server = new grpc.Server();

// Agregar el servicio
server.addService(eventoProto.evento.EventoService.service, eventoService);

// Iniciar el servidor
const PORT = '0.0.0.0:50051';

server.bind(PORT, grpc.ServerCredentials.createInsecure());

server.start();

console.log(`🚀 Servidor gRPC corriendo en ${PORT}`);
console.log(`📡 Esperando conexiones...`);
```

#### 4.5 Cliente gRPC

```javascript
// client/index.js
const grpc = require('grpc');
const protoLoader = require('@grpc/proto-loader');
const readline = require('readline');

const PROTO_PATH = __dirname + '/../proto/evento.proto';

const packageDefinition = protoLoader.loadSync(PROTO_PATH, {
    keepCase: false,
    longs: String,
    enums: String,
    defaults: true,
    oneofs: true
});

const eventoProto = grpc.loadPackageDefinition(packageDefinition);

// Crear cliente
const client = new eventoProto.evento.EventoService(
    'localhost:50051',
    grpc.credentials.createInsecure()
);

class EventoClient {
    // UNARY - Crear evento
    async crearEvento(datos) {
        return new Promise((resolve, reject) => {
            client.crearEvento(datos, (error, response) => {
                if (error) {
                    reject(error);
                    return;
                }
                resolve(response);
            });
        });
    }
    
    // UNARY - Obtener evento
    async obtenerEvento(id) {
        return new Promise((resolve, reject) => {
            client.obtenerEvento({ id }, (error, response) => {
                if (error) {
                    reject(error);
                    return;
                }
                resolve(response);
            });
        });
    }
    
    // UNARY - Actualizar evento
    async actualizarEvento(id, datos) {
        return new Promise((resolve, reject) => {
            client.actualizarEvento({ id, ...datos }, (error, response) => {
                if (error) {
                    reject(error);
                    return;
                }
                resolve(response);
            });
        });
    }
    
    // UNARY - Eliminar evento
    async eliminarEvento(id) {
        return new Promise((resolve, reject) => {
            client.eliminarEvento({ id }, (error, response) => {
                if (error) {
                    reject(error);
                    return;
                }
                resolve(response);
            });
        });
    }
    
    // SERVER STREAMING - Listar eventos
    listarEventos(pagina = 1, limite = 10, categoria = '') {
        const stream = client.listarEventos({ pagina, limite, categoria });
        
        return new Promise((resolve, reject) => {
            const eventos = [];
            
            stream.on('data', (evento) => {
                eventos.push(evento);
                console.log(`📄 Evento: ${evento.titulo} - $${evento.precio}`);
            });
            
            stream.on('error', reject);
            
            stream.on('end', () => {
                resolve(eventos);
            });
        });
    }
    
    // CLIENT STREAMING - Procesar reservas
    async procesarReservas(reservas) {
        const stream = client.procesarReservas((error, response) => {
            if (error) {
                console.error('Error:', error);
                return;
            }
            console.log(`✅ Total procesado: $${response.totalProcesado}`);
            console.log(`📊 Cantidad: ${response.cantidadProcesada}`);
        });
        
        reservas.forEach(reserva => {
            stream.write(reserva);
        });
        
        stream.end();
    }
    
    // BIDIRECTIONAL STREAMING - Chat
    chat() {
        const stream = client.chat();
        
        stream.on('data', (mensaje) => {
            console.log(`💬 ${mensaje.remitente}: ${mensaje.texto}`);
        });
        
        // Enviar mensajes
        const rl = readline.createInterface({
            input: process.stdin,
            output: process.stdout
        });
        
        const ask = () => {
            rl.question('Tu mensaje: ', (texto) => {
                if (texto.toLowerCase() === 'salir') {
                    stream.end();
                    rl.close();
                    return;
                }
                
                stream.write({
                    texto,
                    timestamp: new Date().toISOString()
                });
                
                ask();
            });
        };
        
        ask();
    }
}

// Uso del cliente
async function main() {
    const cliente = new EventoClient();
    
    console.log('=== Ejemplo gRPC ===\n');
    
    // 1. Crear evento
    console.log('1️⃣ Creando evento...');
    const nuevoEvento = await cliente.crearEvento({
        titulo: 'Concierto de Rock',
        descripcion: 'El mejor concierto del año',
        fecha: '2024-12-31',
        ubicacion: 'Estadio Centenario',
        precio: 1500,
        capacidad: 50000,
        categoria: 'musica'
    });
    console.log('✅ Evento creado:', nuevoEvento.id);
    
    // 2. Obtener evento
    console.log('\n2️⃣ Obteniendo evento...');
    const evento = await cliente.obtenerEvento(nuevoEvento.id);
    console.log('📄 Evento:', evento.titulo);
    
    // 3. Listar eventos (streaming)
    console.log('\n3️⃣ Listando eventos...');
    await cliente.listarEventos(1, 10, 'musica');
    
    // 4. Actualizar evento
    console.log('\n4️⃣ Actualizando evento...');
    await cliente.actualizarEvento(nuevoEvento.id, {
        precio: 1800,
        capacidad: 45000
    });
    console.log('✅ Evento actualizado');
    
    // 5. Eliminar evento
    console.log('\n5️⃣ Eliminando evento...');
    await cliente.eliminarEvento(nuevoEvento.id);
    console.log('✅ Evento eliminado');
    
    // 6. Client streaming
    console.log('\n6️⃣ Procesando reservas (streaming)...');
    await cliente.procesarReservas([
        { eventoId: '1', cantidad: 2, precioUnitario: 100 },
        { eventoId: '1', cantidad: 3, precioUnitario: 100 },
        { eventoId: '2', cantidad: 1, precioUnitario: 200 }
    ]);
    
    console.log('\n✅ Ejemplo completado');
}

main().catch(console.error);
```

---

## 🛠️ Ejercicios Prácticos

### Ejercicio 1: Implementar servicio gRPC básico

**Objetivo:** Crear un servicio completo de gestión de eventos

```protobuf
// proto/evento.proto - Define el archivo proto con:
syntax = "proto3";

package evento;

service EventoService {
    rpc CrearEvento (CrearEventoRequest) returns (Evento);
    rpc ObtenerEvento (ObtenerEventoRequest) returns (Evento);
    rpc ActualizarEvento (ActualizarEventoRequest) returns (Evento);
    rpc EliminarEvento (EliminarEventoRequest) returns (EliminarEventoResponse);
    rpc ListarEventos (ListarEventosRequest) returns (stream Evento);
    rpc BuscarEventos (BuscarEventosRequest) returns (ListaEventos);
}

message Evento { ... }
message CrearEventoRequest { ... }
message ObtenerEventoRequest { ... }
message ActualizarEventoRequest { ... }
message EliminarEventoRequest { ... }
message EliminarEventoResponse { ... }
message ListarEventosRequest { ... }
message BuscarEventosRequest { ... }
message ListaEventos { ... }
```

### Ejercicio 2: Streaming de eventos

Implementar streaming bidireccional para:
- Notificaciones en tiempo real a clientes subscritos
- Chat de soporte entre usuarios y administradores

### Ejercicio 3: gRPC + REST

Crear servidor que exponga ambos protocolos:
- REST para clientes web tradicionales
- gRPC para comunicación entre microservicios

---

## 🚀 Proyecto de la Clase

### Sistema de Eventos con gRPC

```protobuf
// proto/evento.proto - Definición completa del proyecto
syntax = "proto3";

package evento;

// ============================================
// SERVICIOS
// ============================================

service EventoService {
    // CRUD Básico
    rpc CrearEvento (CrearEventoRequest) returns (Evento);
    rpc ObtenerEvento (ObtenerEventoRequest) returns (Evento);
    rpc ActualizarEvento (ActualizarEventoRequest) returns (Evento);
    rpc EliminarEvento (EliminarEventoRequest) returns (EliminarEventoResponse);
    
    // Consultas
    rpc ListarEventos (ListarEventosRequest) returns (ListaEventos);
    rpc BuscarEventos (BuscarEventosRequest) returns (ListaEventos);
    rpc GetEventosPorCategoria (CategoriaRequest) returns (stream Evento);
    
    // Disponibilidad
    rpc VerificarDisponibilidad (DisponibilidadRequest) returns (DisponibilidadResponse);
}

// ============================================
// MENSAJES - EVENTOS
// ============================================

message Evento {
    string id = 1;
    string titulo = 2;
    string descripcion = 3;
    string fecha = 4;
    string fecha_fin = 5;
    string ubicacion = 6;
    double precio = 7;
    int32 capacidad = 8;
    int32 vendidos = 9;
    string categoria = 10;
    string imagen = 11;
    bool activo = 12;
    string organizador_id = 13;
    string created_at = 14;
    string updated_at = 15;
}

message CrearEventoRequest {
    string titulo = 1;
    string descripcion = 2;
    string fecha = 3;
    string fecha_fin = 4;
    string ubicacion = 5;
    double precio = 6;
    int32 capacidad = 7;
    string categoria = 8;
    string imagen = 9;
    string organizador_id = 10;
}

message ActualizarEventoRequest {
    string id = 1;
    string titulo = 2;
    string descripcion = 3;
    string fecha = 4;
    string fecha_fin = 5;
    string ubicacion = 6;
    double precio = 7;
    int32 capacidad = 8;
    string categoria = 9;
    string imagen = 10;
    bool activo = 11;
}

message ObtenerEventoRequest {
    string id = 1;
}

message EliminarEventoRequest {
    string id = 1;
}

message EliminarEventoResponse {
    bool success = 1;
    string message = 2;
}

// ============================================
// MENSAJES - CONSULTAS
// ============================================

message ListarEventosRequest {
    int32 pagina = 1;
    int32 limite = 2;
    string ordenar_por = 3;  // fecha, precio, titulo
    bool ascendente = 4;
    string categoria = 5;
}

message BuscarEventosRequest {
    string query = 1;
    string categoria = 2;
    string fecha_desde = 3;
    string fecha_hasta = 4;
    double precio_min = 5;
    double precio_max = 6;
}

message CategoriaRequest {
    string categoria = 1;
}

message ListaEventos {
    repeated Evento eventos = 1;
    int32 total = 2;
    int32 pagina = 3;
    int32 total_paginas = 4;
}

// ============================================
// MENSAJES - DISPONIBILIDAD
// ============================================

message DisponibilidadRequest {
    string evento_id = 1;
    int32 cantidad = 2;
}

message DisponibilidadResponse {
    bool disponible = 1;
    int32 disponibles = 2;
    string mensaje = 3;
}
```

### Archivos Entregables

1. **evento.proto** - Definición del servicio y mensajes
2. **server/index.js** - Servidor gRPC con todas las operaciones
3. **client/eventoClient.js** - Cliente reutilizable
4. **tests/evento.test.js** - Tests básicos

### Comandos para ejecutar

```bash
# Iniciar servidor
node server/index.js

# Probar con cliente
node client/index.js

# Listar servicios
grpcurl -plaintext localhost:50051 list

# Ver método
grpcurl -plaintext localhost:50051 describe evento.EventoService
```

---

## 📚 Recursos Adicionales

- [Documentación oficial gRPC](https://grpc.io/docs/)
- [Guía de Protocol Buffers](https://developers.google.com/protocol-buffers)
- [gRPC en Node.js](https://grpc.io/docs/languages/node/)
- [Best practices](https://cloud.google.com/apis/design)
