# Clase 17 — Patrones Multi-Base de Datos y Polyglot Persistence

## Objetivos de Aprendizaje

Al finalizar esta clase, el estudiante será capaz de:
- Diseñar arquitecturas que integren múltiples bases de datos
- Implementar patrones como CQRS, Event Sourcing, Saga y Change Data Capture
- Seleccionar la base de datos correcta para cada problema
- Integrar Docker Compose con múltiples bases de datos NoSQL
- Desarrollar código que sincronice datos entre diferentes sistemas de persistencia
- Evaluar compensaciones de rendimiento, consistencia y complejidad

---

## 1. Marco Teórico

### 1.1 Polyglot Persistence: Concepto y Filosofía

**Polyglot Persistence** (Persistencia Multilingüe) es una estrategia arquitectónica que consiste en utilizar **múltiples bases de datos** dentro de un mismo sistema, seleccionando la herramienta más adecuada para cada tipo de datos y operación.

> "No hay una base de datos que sirva para todo. La mejor base de datos es la que se adapta al problema específico que estás resolviendo."

#### ¿Por qué usar múltiples bases de datos?

Cada base de datos fue diseñada con fortalezas específicas:

| Base de Datos | Fortaleza Principal | Caso de Uso Ideal |
|---|---|---|
| **MongoDB** | Documentos flexibles, alto write throughput | Catálogos, contenido, logs |
| **Redis** | Velocidad extrema, estructuras de datos | Caché, sesiones, rate limiting |
| **Cassandra** | Escritura masiva, disponibilidad | Métricas IoT, time-series |
| **Neo4j** | Relaciones complejas, traversals | Redes sociales, recomendaciones |
| **ObjectDB** | Persistencia nativa de objetos Java | Aplicaciones Java enterprise |
| **PostgreSQL** | Transacciones ACID complejas | Pagos, inventario crítico |
| **Elasticsearch** | Búsqueda full-text, analytics | Búsqueda de productos, logs |

#### La Base de Datos Correcta para Cada Problemo

```mermaid
graph TB
    START[¿Qué tipo de datos necesitas?] --> Q1{¿Son documentos\nflexibles?}
    Q1 -->|Sí| MONGO[MongoDB<br/>Documentos JSON/BSON]
    Q1 -->|No| Q2{¿Necesitas\nvelocidad extrema?}
    Q2 -->|Sí| REDIS[Redis<br/>Key-Value In-Memory]
    Q2 -->|No| Q3{¿Tienes relaciones\ncomplejas?}
    Q3 -->|Sí| NEO[Neo4j<br/>Base de Grafos]
    Q3 -->|No| Q4{¿Escribes masivamente\nen series de tiempo?}
    Q4 -->|Sí| CASS[Cassandra<br/>Wide-Column Store]
    Q4 -->|No| Q5{¿Tu app es Java\ny quieres simplicidad?}
    Q5 -->|Sí| OBJ[ObjectDB<br/>Orientada a Objetos]
    Q5 -->|No| Q6{¿Necesitas búsquedas\ntextuales complejas?}
    Q6 -->|SÍ| ES[Elasticsearch<br/>Motor de Búsqueda]
    Q6 -->|No| PG[PostgreSQL<br/>RDBMS Relacional]
```

#### Diagrama de Decisión Completo

```mermaid
flowchart TD
    A[Solicitud del Usuario] --> B{¿Qué operación?}
    B -->|Lectura frecuente| C{¿Datos estáticos?}
    C -->|Sí| D[Redis Cache]
    C -->|No| E[BD Transaccional]
    B -->|Escritura masiva| F{¿Requiere orden temporal?}
    F -->|Sí| G[Cassandra]
    F -->|No| H[MongoDB]
    B -->|Búsqueda| I[Elasticsearch]
    B -->|Relaciones| J[Neo4j]
    B -->|Transacciones ACID| K[PostgreSQL/MySQL]

    D --> L[API Response]
    E --> L
    G --> L
    H --> L
    I --> L
    J --> L
    K --> L

    L --> M[Cliente]
```

---

## 2. Patrones de Integración

### 2.1 Database per Service

Cada microservicio posee su propia base de datos, completamente aislada de los demás.

**Ventajas:**
- Desacoplamiento completo entre servicios
- Cada servicio puede usar la BD que mejor se adapte
- Escalamiento independiente
- Despliegue independiente

**Desventajas:**
- Consistencia distribuida (no hay transacciones atómicas entre BD)
- Complejidad en queries cruzadas
- Gestión de múltiples esquemas

**Ejemplo:**

```mermaid
graph LR
    subgraph "Servicio de Usuarios"
        US[User Service]
        USDB[(MongoDB<br/>usuarios)]
    end

    subgraph "Servicio de Productos"
        PS[Product Service]
        PSDB[(PostgreSQL<br/>productos)]
    end

    subgraph "Servicio de Sesiones"
        SS[Session Service]
        SSDB[(Redis<br/>sesiones)]
    end

    subgraph "Servicio de Recomendaciones"
        RS[Recommendation Service]
        RSDB[(Neo4j<br/>grafo social)]
    end

    US --> USDB
    PS --> PSDB
    SS --> SSDB
    RS --> RSDB

    API[API Gateway] --> US
    API --> PS
    API --> SS
    API --> RS
```

### 2.2 Shared Database

Múltiples servicios comparten una misma base de datos.

```mermaid
graph LR
    S1[Servicio A] --> BD[(Base de Datos<br/>Compartida)]
    S2[Servicio B] --> BD
    S3[Servicio C] --> BD
```

**Ventajas:** Transacciones atómicas, simplicidad
**Desventajas:** Acoplamiento, difícil escalar independientemente

### 2.3 API Composition

Consultar múltiples APIs y combinar los resultados en la aplicación.

```java
// API Composition Pattern
@RestController
@RequestMapping("/api/vista-completa")
public class ApiCompositionController {

    @Autowired private WebClient webClient;

    @GetMapping("/pedido/{id}")
    public ResponseEntity<VistaCompletaPedido> getVistaCompleta(
            @PathVariable Long id) {

        // Consultar múltiples servicios en paralelo
        Mono<Pedido> pedidoMono = webClient.get()
            .uri("http://pedido-service/pedidos/{id}", id)
            .retrieve()
            .bodyToMono(Pedido.class);

        Mono<Usuario> usuarioMono = webClient.get()
            .uri("http://usuario-service/usuarios/{pedido.usuarioId}")
            .retrieve()
            .bodyToMono(Usuario.class);

        Mono<List<Producto>> productosMono = webClient.get()
            .uri("http://producto-service/productos/pedido/{id}", id)
            .retrieve()
            .bodyToFlux(Producto.class)
            .collectList();

        // Combinar resultados
        return Mono.zip(pedidoMono, usuarioMono, productosMono)
            .map(tuple -> new VistaCompletaPedido(
                tuple.getT1(),  // Pedido
                tuple.getT2(),  // Usuario
                tuple.getT3()   // Productos
            ))
            .map(ResponseEntity::ok)
            .defaultIfEmpty(ResponseEntity.notFound().build())
            .block();
    }
}
```

### 2.4 CQRS (Command Query Responsibility Segregation)

Separar las operaciones de **escritura** (commands) de las de **lectura** (queries), usando bases de datos optimizadas para cada caso.

```mermaid
graph TB
    subgraph "Escritura (Commands)"
        CMD[Command Handler]
        WRITEDB[(MongoDB<br/>Write-Optimized)]
    end

    subgraph "Lectura (Queries)"
        QRY[Query Handler]
        READDB[(Redis<br/>Read-Optimized)]
    end

    subgraph "Sincronización"
        EVT[Event Bus<br/>Kafka/RabbitMQ]
    end

    CLIENT[Client] -->|Write| CMD
    CLIENT -->|Read| QRY
    CMD --> WRITEDB
    CMD -->|Publish Event| EVT
    EVT -->|Subscribe| READDB
    QRY --> READDB
```

```java
// CQRS Implementation

// --- COMMAND SIDE ---
@Service
public class PedidoCommandService {

    @Autowired private PedidoWriteRepository writeRepo;
    @Autowired private ApplicationEventPublisher eventPublisher;

    @Transactional
    public PedidoId crearPedido(CrearPedidoCommand cmd) {
        Pedido pedido = Pedido.crear(
            cmd.getUsuarioId(),
            cmd.getItems(),
            cmd.getDireccionEnvio()
        );

        // Guardar en MongoDB (optimizado para escritura)
        writeRepo.save(pedido);

        // Publicar evento
        eventPublisher.publishEvent(new PedidoCreadoEvent(
            pedido.getId(),
            pedido.getUsuarioId(),
            pedido.getTotal(),
            LocalDateTime.now()
        ));

        return pedido.getId();
    }

    @Transactional
    public void confirmarPedido(ConfirmarPedidoCommand cmd) {
        Pedido pedido = writeRepo.findById(cmd.getPedidoId())
            .orElseThrow(() -> new PedidoNotFoundException(cmd.getPedidoId()));

        pedido.confirmar();
        writeRepo.save(pedido);

        eventPublisher.publishEvent(new PedidoConfirmadoEvent(
            pedido.getId(),
            LocalDateTime.now()
        ));
    }
}

// --- QUERY SIDE ---
@Service
public class PedidoQueryService {

    @Autowired private PedidoCacheRepository cacheRepo;
    @Autowired private RedisTemplate<String, Object> redis;

    public PedidoVista getPedido(PedidoId id) {
        // Primero intentar caché
        PedidoVista cached = cacheRepo.findById(id.toString());
        if (cached != null) return cached;

        // Si no está en caché, consultar MongoDB
        Pedido pedido = writeRepo.findById(id);
        PedidoVista vista = PedidoVista.from(pedido);

        // Guardar en caché
        cacheRepo.save(vista);
        return vista;
    }

    public List<PedidoVista> getPedidosPorUsuario(UsuarioId userId) {
        return cacheRepo.findByUsuarioId(userId.toString());
    }
}

// --- EVENT HANDLER (sincronización) ---
@Component
public class PedidoEventHandler {

    @Autowired private PedidoCacheRepository cacheRepo;

    @EventListener
    public void onPedidoCreado(PedidoCreadoEvent event) {
        PedidoVista vista = new PedidoVista();
        vista.setId(event.getPedidoId().toString());
        vista.setUsuarioId(event.getUsuarioId().toString());
        vista.setTotal(event.getTotal());
        vista.setEstado("CREADO");
        vista.setFechaCreacion(event.getTimestamp());

        cacheRepo.save(vista);
    }

    @EventListener
    public void onPedidoConfirmado(PedidoConfirmadoEvent event) {
        PedidoVista vista = cacheRepo.findById(event.getPedidoId().toString());
        if (vista != null) {
            vista.setEstado("CONFIRMADO");
            vista.setFechaConfirmacion(event.getTimestamp());
            cacheRepo.save(vista);
        }
    }
}
```

### 2.5 Event Sourcing

Almacenar **eventos inmutables** en lugar de estados. Cada cambio se registra como un evento, y el estado actual se reconstructa reproduciendo los eventos.

```mermaid
graph LR
    subgraph "Event Store (Cassandra)"
        E1[Evento 1<br/>PedidoCreado<br/>2026-01-15 10:00]
        E2[Evento 2<br/>ItemAgregado<br/>2026-01-15 10:01]
        E3[Evento 3<br/>PagoRecibido<br/>2026-01-15 10:05]
        E4[Evento 4<br/>EnvioProgramado<br/>2026-01-15 10:10]
    end

    E1 --> E2 --> E3 --> E4

    subgraph "State Reconstruction"
        REPLAY[Replay de Eventos]
        STATE[Estado Actual<br/>Pedido #12345<br/>Estado: Enviado]
    end

    E4 --> REPLAY --> STATE
```

```java
// Event Sourcing Implementation

// --- Eventos ---
public interface DomainEvent {
    String getAggregateId();
    LocalDateTime getTimestamp();
    String getEventType();
}

@Value
public class PedidoCreadoEvent implements DomainEvent {
    String aggregateId;
    String usuarioId;
    List<ItemPedidoDTO> items;
    String direccionEnvio;
    LocalDateTime timestamp = LocalDateTime.now();
    String eventType = "PEDIDO_CREADO";
}

@Value
public class ItemAgregadoEvent implements DomainEvent {
    String aggregateId;
    String productoId;
    int cantidad;
    BigDecimal precioUnitario;
    LocalDateTime timestamp = LocalDateTime.now();
    String eventType = "ITEM_AGREGADO";
}

@Value
public class PagoRecibidoEvent implements DomainEvent {
    String aggregateId;
    BigDecimal monto;
    String metodoPago;
    LocalDateTime timestamp = LocalDateTime.now();
    String eventType = "PAGO_RECIBIDO";
}

@Value
public class EnvioProgramadoEvent implements DomainEvent {
    String aggregateId;
    String direccionEnvio;
    String carrier;
    LocalDateTime timestamp = LocalDateTime.now();
    String eventType = "ENVIO_PROGRAMADO";
}

// --- Aggregate (reconstruido desde eventos) ---
public class PedidoAggregate {

    private String id;
    private String usuarioId;
    private PedidoEstado estado;
    private List<ItemPedido> items;
    private BigDecimal total;
    private String direccionEnvio;
    private List<DomainEvent> uncommittedEvents = new ArrayList<>();

    // Reconstruir desde eventos
    public static PedidoAggregate fromEvents(List<DomainEvent> events) {
        PedidoAggregate pedido = new PedidoAggregate();
        for (DomainEvent event : events) {
            pedido.apply(event);
        }
        return pedido;
    }

    // Aplicar evento al estado
    public void apply(DomainEvent event) {
        if (event instanceof PedidoCreadoEvent e) {
            this.id = e.getAggregateId();
            this.usuarioId = e.getUsuarioId();
            this.items = new ArrayList<>();
            this.direccionEnvio = e.getDireccionEnvio();
            this.estado = PedidoEstado.CREADO;
        }
        else if (event instanceof ItemAgregadoEvent e) {
            this.items.add(new ItemPedido(
                e.getProductoId(), e.getCantidad(), e.getPrecioUnitario()
            ));
            recalcularTotal();
        }
        else if (event instanceof PagoRecibidoEvent e) {
            this.estado = PedidoEstado.PAGADO;
        }
        else if (event instanceof EnvioProgramadoEvent e) {
            this.direccionEnvio = e.getDireccionEnvio();
            this.estado = PedidoEstado.ENVIADO;
        }
    }

    // Comandos que generan eventos
    public void agregarItem(String productoId, int cantidad, BigDecimal precio) {
        ItemAgregadoEvent event = new ItemAgregadoEvent(
            this.id, productoId, cantidad, precio
        );
        this.apply(event);
        this.uncommittedEvents.add(event);
    }

    public void confirmarPago(BigDecimal monto, String metodo) {
        PagoRecibidoEvent event = new PagoRecibidoEvent(
            this.id, monto, metodo
        );
        this.apply(event);
        this.uncommittedEvents.add(event);
    }
}

// --- Event Store (Cassandra) ---
@Service
public class CassandraEventStore {

    @Autowired private CqlTemplate cqlTemplate;

    public void saveEvents(String aggregateId, List<DomainEvent> events) {
        for (DomainEvent event : events) {
            String insertEvent = "INSERT INTO event_store " +
                "(aggregate_id, event_type, timestamp, event_data) " +
                "VALUES (?, ?, ?, ?)";

            cqlTemplate.execute(insertEvent,
                aggregateId,
                event.getEventType(),
                event.getTimestamp(),
                toJson(event)
            );
        }
    }

    public List<DomainEvent> getEvents(String aggregateId) {
        String query = "SELECT * FROM event_store " +
            "WHERE aggregate_id = ? ORDER BY timestamp ASC";

        return cqlTemplate.query(query, (rs, rowNum) -> {
            String eventType = rs.getString("event_type");
            String jsonData = rs.getString("event_data");
            return deserializeEvent(eventType, jsonData);
        }, aggregateId);
    }

    // Replay: reconstruir aggregate desde eventos
    public PedidoAggregate loadPedido(String pedidoId) {
        List<DomainEvent> events = getEvents(pedidoId);
        return PedidoAggregate.fromEvents(events);
    }
}
```

### 2.6 Saga Pattern

Gestionar transacciones distribuidas sin Two-Phase Commit, usando una secuencia de pasos con transacciones compensatorias en caso de fallo.

#### Choreography-based Saga

```mermaid
sequenceDiagram
    participant C as Cliente
    participant P as Pedido Service
    participant I as Inventario Service
    participant PA as Pago Service
    participant E as Envío Service

    C->>P: Crear Pedido
    P->>P: Guardar pedido (MongoDB)
    P-->>I: Evento: PedidoCreado
    I->>I: Reservar stock
    I-->>PA: Evento: StockReservado
    PA->>PA: Cobrar (PostgreSQL)
    PA-->>E: Evento: PagoAceptado
    E->>E: Programar envío
    E-->>P: Evento: EnvioProgramado
    P->>P: Marcar como enviado
    P-->>C: Notificación: Pedido enviado
```

```java
// Choreography-based Saga

// --- Pedido Service ---
@Service
public class PedidoSagaService {

    @EventListener
    public void onStockReservado(StockReservadoEvent event) {
        // Intentar cobrar
        Pedido pedido = pedidoRepo.findById(event.getPedidoId());

        try {
            PagoRequest request = new PagoRequest(
                pedido.getId(),
                pedido.getTotal(),
                pedido.getMetodoPago()
            );
            pagoService.cobrar(request);

        } catch (PagoFallidoException e) {
            // Transacción compensatoria: liberar stock
            eventPublisher.publishEvent(new StockLiberarEvent(
                event.getPedidoId(),
                event.getItems()
            ));

            pedido.rechazar("Pago fallido");
            pedidoRepo.save(pedido);
        }
    }

    @EventListener
    public void onStockReservaFallida(StockReservaFallidaEvent event) {
        Pedido pedido = pedidoRepo.findById(event.getPedidoId());
        pedido.rechazar("Sin stock suficiente");
        pedidoRepo.save(pedido);
    }
}

// --- Inventario Service ---
@Service
public class InventarioSagaService {

    @EventListener
    public void onPedidoCreado(PedidoCreadoEvent event) {
        try {
            for (ItemPedidoDTO item : event.getItems()) {
                inventarioRepo.reservar(item.getProductoId(), item.getCantidad());
            }

            eventPublisher.publishEvent(new StockReservadoEvent(
                event.getPedidoId(), event.getItems()
            ));

        } catch (StockInsuficienteException e) {
            eventPublisher.publishEvent(new StockReservaFallidaEvent(
                event.getPedidoId(),
                e.getProductoId(),
                e.getCantidadDisponible()
            ));
        }
    }

    @EventListener
    public void onStockLiberar(StockLiberarEvent event) {
        // Compensación: devolver stock
        for (ItemPedidoDTO item : event.getItems()) {
            inventarioRepo.liberar(item.getProductoId(), item.getCantidad());
        }
    }
}
```

#### Orchestration-based Saga

```mermaid
sequenceDiagram
    participant O as Saga Orchestrator
    participant P as Pedido Service
    participant I as Inventario Service
    participant PA as Pago Service
    participant E as Envío Service

    O->>P: 1. Crear Pedido
    P-->>OK: Pedido creado
    O->>I: 2. Reservar Stock
    I-->>OK: Stock reservado
    O->>PA: 3. Cobrar
    PA-->>OK: Pago aceptado
    O->>E: 4. Programar Envío
    E-->>OK: Envío programado
    O->>P: 5. Confirmar Pedido
```

```java
// Saga Orchestrator
@Service
public class PedidoSagaOrchestrator {

    @Autowired private PedidoService pedidoService;
    @Autowired private InventarioService inventarioService;
    @Autowired private PagoService pagoService;
    @Autowired private EnvioService envioService;

    @Transactional
    public void ejecutarSaga(CrearPedidoCommand cmd) {
        String sagaId = UUID.randomUUID().toString();
        PedidoAggregate pedido = null;

        try {
            // Paso 1: Crear pedido
            pedido = pedidoService.crear(cmd);
            log.info("Saga {} - Paso 1: Pedido creado: {}", sagaId, pedido.getId());

            // Paso 2: Reservar stock
            inventarioService.reservarStock(pedido.getId(), pedido.getItems());
            log.info("Saga {} - Paso 2: Stock reservado", sagaId);

            // Paso 3: Cobrar
            pagoService.cobrar(pedido.getId(), pedido.getTotal(),
                pedido.getMetodoPago());
            log.info("Saga {} - Paso 3: Pago procesado", sagaId);

            // Paso 4: Programar envío
            envioService.programarEnvio(pedido.getId(),
                pedido.getDireccionEnvio());
            log.info("Saga {} - Paso 4: Envío programado", sagaId);

            // Paso 5: Confirmar pedido
            pedidoService.confirmar(pedido.getId());
            log.info("Saga {} - Saga completada exitosamente", sagaId);

        } catch (Exception e) {
            log.error("Saga {} - Error: {}. Iniciando compensación",
                sagaId, e.getMessage());

            // Transacciones compensatorias (en orden inverso)
            if (pedido != null) {
                tryCompensarEnvio(pedido.getId());
                tryCompensarPago(pedido.getId());
                tryCompensarStock(pedido.getId());
                tryCompensarPedido(pedido.getId());
            }

            throw new SagaFailedException(sagaId, e);
        }
    }

    private void tryCompensarEnvio(String pedidoId) {
        try {
            envioService.cancelarEnvio(pedidoId);
            log.info("Compensación: Envío cancelado");
        } catch (Exception e) {
            log.error("Compensación envío fallida: {}", e.getMessage());
        }
    }

    private void tryCompensarPago(String pedidoId) {
        try {
            pagoService.revertirPago(pedidoId);
            log.info("Compensación: Pago revertido");
        } catch (Exception e) {
            log.error("Compensación pago fallida: {}", e.getMessage());
        }
    }

    private void tryCompensarStock(String pedidoId) {
        try {
            inventarioService.liberarStock(pedidoId);
            log.info("Compensación: Stock liberado");
        } catch (Exception e) {
            log.error("Compensación stock fallida: {}", e.getMessage());
        }
    }

    private void tryCompensarPedido(String pedidoId) {
        try {
            pedidoService.cancelar(pedidoId);
            log.info("Compensación: Pedido cancelado");
        } catch (Exception e) {
            log.error("Compensación pedido fallida: {}", e.getMessage());
        }
    }
}
```

### 2.7 Two-Phase Commit (2PC)

```mermaid
sequenceDiagram
    participant C as Coordinator
    participant A as Participant A
    participant B as Participant B

    Note over C: Phase 1: Prepare
    C->>A: PREPARE
    C->>B: PREPARE
    A-->>C: VOTE YES
    B-->>C: VOTE YES

    Note over C: Phase 2: Commit
    C->>A: GLOBAL COMMIT
    C->>B: GLOBAL COMMIT
    A-->>C: ACK
    B-->>C: ACK
    Note over C: Transacción completada
```

**Ventajas:** Consistencia fuerte (ACID distribuido)
**Desventajas:** Blocking, punto único de fallo, latencia alta

---

## 3. Change Data Capture (CDC)

### 3.1 Concepto

CDC detecta cambios en la base de datos (inserts, updates, deletes) y los propaga a otros sistemas en tiempo real.

```mermaid
graph LR
    subgraph "Source DB"
        DB[(MongoDB<br/>PostgreSQL<br/>MySQL)]
    end

    subgraph "CDC Engine"
        CDC[Debezium]
    end

    subgraph "Message Broker"
        KAFKA[Apache Kafka]
    end

    subgraph "Sinks"
        S1[Redis Cache]
        S2[Elasticsearch]
        S3[Data Warehouse]
    end

    DB -->|Change Events| CDC
    CDC -->|Publish| KAFKA
    KAFKA -->|Consume| S1
    KAFKA -->|Consume| S2
    KAFKA -->|Consume| S3
```

### 3.2 Debezium

```yaml
# docker-compose.yml con Debezium
version: '3.8'
services:
  # MongoDB
  mongodb:
    image: mongo:7.0
    ports:
      - "27017:27017"
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: admin123
    volumes:
      - mongodb_data:/data/db

  # Kafka
  zookeeper:
    image: confluentinc/cp-zookeeper:7.5.0
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181

  kafka:
    image: confluentinc/cp-kafka:7.5.0
    depends_on:
      - zookeeper
    ports:
      - "9092:9092"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:29092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1

  # Debezium MongoDB Connector
  connect:
    image: quay.io/debezium/connect:2.4
    depends_on:
      - kafka
      - mongodb
    ports:
      - "8083:8083"
    environment:
      BOOTSTRAP_SERVERS: kafka:29092
      GROUP_ID: debezium-connect
      CONFIG_STORAGE_TOPIC: connect-configs
      OFFSET_STORAGE_TOPIC: connect-offsets

  # Debezium MongoDB Connector Configuration
  register-connector:
    image: curlimages/curl
    depends_on:
      - connect
    command: >
      sh -c "
      sleep 30 &&
      curl -X POST http://connect:8083/connectors -H 'Content-Type: application/json' -d '{
        \"name\": \"mongo-products-connector\",
        \"config\": {
          \"connector.class\": \"io.debezium.connector.mongodb.MongoDbConnector\",
          \"mongodb.connection.mode\": \"replica_set\",
          \"mongodb.connection.hosts\": \"mongodb:27017\",
          \"mongodb.user\": \"admin\",
          \"mongodb.password\": \"admin123\",
          \"topic.prefix\": \"mongo\",
          \"database.include.list\": \"tienda\",
          \"collection.include.list\": \"tienda.productos\",
          \"snapshot.mode\": \"initial\"
        }
      }'
      "

volumes:
  mongodb_data:
```

### 3.3 MongoDB Change Streams

```java
// MongoDB Change Streams — Sincronizar MongoDB → Redis
import com.mongodb.client.*;
import com.mongodb.client.model.Aggregates;
import org.bson.Document;

public class MongoToRedisSync {

    public static void main(String[] args) {
        MongoClient mongoClient = MongoClients.create(
            "mongodb://admin:admin123@localhost:27017/?authSource=admin"
        );

        MongoDatabase db = mongoClient.getDatabase("tienda");
        MongoCollection<Document> productos = db.getCollection("productos");

        // Redis connection
        JedisPool jedisPool = new JedisPool("localhost", 6379);

        // Watch for changes
        List<Bson> pipeline = Arrays.asList(
            Aggregates.match(Filters.in("operationType",
                "insert", "update", "replace", "delete"))
        );

        ChangeStreamIterable<Document> changeStream = productos.watch(pipeline)
            .fullDocument(FullDocument.UPDATE_LOOKUP)
            .resumeAfter(getLastResumeToken());

        changeStream.forEach(event -> {
            String operationType = event.getOperationType().getValue();
            String documentKey = event.getDocumentKey().get("_id").toString();

            System.out.println("Change detected: " + operationType +
                " on document: " + documentKey);

            try (Jedis jedis = jedisPool.getResource()) {
                switch (operationType) {
                    case "insert":
                    case "update":
                    case "replace":
                        Document doc = event.getFullDocument();
                        jedis.set(
                            "producto:" + documentKey,
                            doc.toJson()
                        );
                        jedis.expire("producto:" + documentKey, 3600);
                        System.out.println("  → Redis: producto cacheado");
                        break;

                    case "delete":
                        jedis.del("producto:" + documentKey);
                        System.out.println("  → Redis: producto eliminado del caché");
                        break;
                }

                // Guardar resume token
                jedis.set("mongo:resume_token",
                    toJson(event.getResumeToken()));
            }
        });
    }

    private static Document getLastResumeToken() {
        try (Jedis jedis = new Jedis("localhost", 6379)) {
            String token = jedis.get("mongo:resume_token");
            if (token != null) {
                return Document.parse(token);
            }
        }
        return null;
    }
}
```

---

## 4. Casos de Uso Multi-BD

### 4.1 E-commerce

```mermaid
graph TB
    subgraph "Frontend"
        WEB[Web App]
        MOB[Mobile App]
    end

    subgraph "API Gateway"
        GW[API Gateway<br/>Kong/NGINX]
    end

    subgraph "Microservicios"
        US[Usuario Service<br/>Python]
        PS[Producto Service<br/>Java]
        CS[Carrito Service<br/>Node.js]
        OS[Orden Service<br/>Java]
        RS[Recomendaciones<br/>Python]
        AS[Analytics Service<br/>Go]
    end

    subgraph "Bases de Datos"
        USDB[(MongoDB<br/>Usuarios<br/>& Perfiles)]
        PSDW[(PostgreSQL<br/>Productos<br/>& Inventario)]
        CSRD[(Redis<br/>Carrito &<br/>Sesiones)]
        OSDB[(MongoDB<br/>Pedidos)]
        RSNEO[(Neo4j<br/>Grafo de<br/>Recomendaciones)]
        ASCAS[(Cassandra<br/>Métricas &<br/>Clickstream)]
    end

    subgraph "Event Bus"
        KAFKA[Apache Kafka]
    end

    WEB --> GW
    MOB --> GW
    GW --> US
    GW --> PS
    GW --> CS
    GW --> OS
    GW --> RS
    GW --> AS

    US --> USDB
    PS --> PSDW
    CS --> CSRD
    OS --> OSDB
    RS --> RSNEO
    AS --> ASCAS

    OS -->|Publish Events| KAFKA
    KAFKA -->|Consume| RS
    KAFKA -->|Consume| AS
    KAFKA -->|CDC| CSRD
```

#### Código de Integración (Python)

```python
# multi_db_ecommerce.py — Integración multi-DB para e-commerce
import pymongo
import redis
from neo4j import GraphDatabase
from cassandra.cluster import Cluster
from datetime import datetime
import json

class EcommerceMultiDB:
    """Integración de múltiples bases de datos para e-commerce"""

    def __init__(self):
        # MongoDB — Usuarios y Pedidos
        self.mongo_client = pymongo.MongoClient(
            "mongodb://admin:admin123@localhost:27017/?authSource=admin"
        )
        self.mongo_usuarios = self.mongo_client["tienda"]["usuarios"]
        self.mongo_pedidos = self.mongo_client["tienda"]["pedidos"]

        # PostgreSQL — Productos (usando psycopg2)
        # import psycopg2
        # self.pg_conn = psycopg2.connect(
        #     host="localhost", database="tienda",
        #     user="admin", password="admin123"
        # )

        # Redis — Caché y Sesiones
        self.redis_client = redis.Redis(
            host="localhost", port=6379, db=0,
            decode_responses=True
        )

        # Neo4j — Recomendaciones
        self.neo4j_driver = GraphDatabase.driver(
            "bolt://localhost:7687",
            auth=("neo4j", "admin123")
        )

        # Cassandra — Métricas y Clickstream
        self.cassandra_cluster = Cluster(
            ["127.0.0.1"], protocol_version=4
        )
        self.cassandra_session = self.cassandra_cluster.connect("tienda")

    def crear_usuario(self, usuario_data):
        """Crear usuario en MongoDB + caché en Redis"""
        result = self.mongo_usuarios.insert_one(usuario_data)
        user_id = str(result.inserted_id)

        # Caché en Redis
        self.redis_client.setex(
            f"usuario:{user_id}",
            3600,
            json.dumps(usuario_data, default=str)
        )

        self.registrar_metrica("crear_usuario", user_id)
        return user_id

    def buscar_producto(self, query):
        """Buscar producto con caché Redis"""
        cache_key = f"search:{hash(query)}"

        # Intentar caché
        cached = self.redis_client.get(cache_key)
        if cached:
            self.registrar_metrica("buscar_producto_cache_hit", query)
            return json.loads(cached)

        # No hay caché: buscar en PostgreSQL (simulado como MongoDB)
        resultados = list(self.mongo_usuarios.find(
            {"nombre": {"$regex": query, "$options": "i"}},
            {"_id": 1, "nombre": 1}
        ))

        # Guardar en caché 5 minutos
        self.redis_client.setex(cache_key, 300, json.dumps(
            resultados, default=str
        ))

        self.registrar_metrica("buscar_producto_cache_miss", query)
        return resultados

    def agregar_al_carrito(self, user_id, producto_id, cantidad):
        """Carrito de compras en Redis (Hash + TTL)"""
        carrito_key = f"carrito:{user_id}"

        # Usar Hash de Redis para el carrito
        self.redis_client.hset(
            carrito_key,
            producto_id,
            json.dumps({
                "producto_id": producto_id,
                "cantidad": cantidad,
                "agregado_en": datetime.now().isoformat()
            })
        )
        # TTL de 24 horas
        self.redis_client.expire(carrito_key, 86400)

        self.registrar_metrica("agregar_carrito", user_id)

    def obtener_carrito(self, user_id):
        """Obtener carrito desde Redis"""
        carrito_key = f"carrito:{user_id}"
        items = self.redis_client.hgetall(carrito_key)

        return {
            k: json.loads(v) for k, v in items.items()
        }

    def crear_pedido(self, user_id, items):
        """Crear pedido en MongoDB + eventos"""
        pedido = {
            "usuario_id": user_id,
            "items": items,
            "estado": "CREADO",
            "fecha": datetime.now(),
            "total": sum(
                item.get("precio", 0) * item.get("cantidad", 1)
                for item in items
            )
        }

        result = self.mongo_pedidos.insert_one(pedido)
        pedido_id = str(result.inserted_id)

        # Limpiar carrito
        self.redis_client.delete(f"carrito:{user_id}")

        # Registrar métricas
        self.registrar_metrica("crear_pedido", pedido_id)
        for item in items:
            self.registrar_metrica(
                "item_pedido",
                f"{pedido_id}:{item.get('producto_id')}"
            )

        return pedido_id

    def obtener_recomendaciones(self, user_id, limit=5):
        """Obtener recomendaciones desde Neo4j"""
        query = """
        MATCH (u:Usuario {id: $user_id})-[:COMPRO]->(p:Producto)
              -[:CATEGORIA]->(c:Categoria)
              <-[:CATEGORIA]-(recomendado:Producto)
        WHERE NOT (u)-[:COMPRO]->(recomendado)
        RETURN recomendado.nombre AS nombre,
               recomendado.id AS id,
               COUNT(*) AS relevancia
        ORDER BY relevancia DESC
        LIMIT $limit
        """

        with self.neo4j_driver.session() as session:
            result = session.run(query,
                user_id=user_id, limit=limit
            )
            return [dict(record) for record in result]

    def registrar_metrica(self, evento, detalle):
        """Registrar métrica en Cassandra"""
        query = """
        INSERT INTO metricas (evento, timestamp, detalle, ttl_value)
        VALUES (?, ?, ?, 2592000)
        """
        self.cassandra_session.execute(query, (
            evento, datetime.now(), detalle
        ))

    def obtener_metricas(self, evento, horas=24):
        """Consultar métricas desde Cassandra"""
        from datetime import timedelta
        desde = datetime.now() - timedelta(hours=horas)

        query = """
        SELECT * FROM metricas
        WHERE evento = ? AND timestamp > ?
        ORDER BY timestamp DESC
        """
        rows = self.cassandra_session.execute(query, (evento, desde))
        return list(rows)

    def close(self):
        """Cerrar todas las conexiones"""
        self.mongo_client.close()
        self.redis_client.close()
        self.neo4j_driver.close()
        self.cassandra_cluster.shutdown()


# === USO ===
if __name__ == "__main__":
    db = EcommerceMultiDB()

    # Crear usuario
    user_id = db.crear_usuario({
        "nombre": "Juan Pérez",
        "email": "juan@ejemplo.com",
        "direccion": "Calle Principal 123"
    })
    print(f"Usuario creado: {user_id}")

    # Agregar al carrito
    db.agregar_al_carrito(user_id, "prod_001", 2)
    db.agregar_al_carrito(user_id, "prod_002", 1)

    # Obtener carrito
    carrito = db.obtener_carrito(user_id)
    print(f"Carrito: {carrito}")

    # Crear pedido
    pedido_id = db.crear_pedido(user_id, [
        {"producto_id": "prod_001", "nombre": "Laptop", "precio": 999.99, "cantidad": 2},
        {"producto_id": "prod_002", "nombre": "Mouse", "precio": 29.99, "cantidad": 1}
    ])
    print(f"Pedido creado: {pedido_id}")

    # Obtener recomendaciones
    recomendaciones = db.obtener_recomendaciones(user_id)
    print(f"Recomendaciones: {recomendaciones}")

    # Ver métricas
    metricas = db.obtener_metricas("crear_pedido", horas=1)
    print(f"Métricas de pedidos: {len(metricas)} registros")

    db.close()
```

### 4.2 Red Social

```mermaid
graph TB
    subgraph "Bases de Datos"
        MONGO[(MongoDB<br/>Perfiles & Posts)]
        REDIS[(Redis<br/>Feed en Tiempo Real)]
        NEO4J[(Neo4j<br/>Relaciones Sociales)]
        CASS[(Cassandra<br/>Métricas & Notificaciones)]
    end

    US[User Service] --> MONGO
    FEED[Feed Service] --> REDIS
    SOCIAL[Social Graph Service] --> NEO4J
    NOTIF[Notification Service] --> CASS

    CDC[Debezium CDC] -->|Change Streams| KAFKA[Kafka]
    KAFKA -->|Sync| REDIS
    KAFKA -->|Analytics| CASS
```

### 4.3 Sistema de Pagos

```mermaid
graph TB
    subgraph "Pago Service"
        API[API REST]
        SAGA[Saga Orchestrator]
    end

    subgraph "Bases de Datos"
        MONGO[(MongoDB<br/>Transacciones)]
        REDIS[(Redis<br/>Idempotency Keys<br/>& Rate Limiting)]
        KAFKA[Apache Kafka<br/>Eventos de Pago]
    end

    API --> SAGA
    SAGA --> MONGO
    SAGA --> REDIS
    SAGA -->|Publish| KAFKA

    subgraph "Sagas"
        PAY[Pago Saga]
    end

    SAGA --> PAY
```

```java
// Idempotency key con Redis
@Service
public class PagoService {

    @Autowired private RedisTemplate<String, String> redis;
    @Autowired private PagoRepository pagoRepo;

    public PagoResponse procesarPago(PagoRequest request) {
        String idempotencyKey = request.getIdempotencyKey();

        // Verificar si ya se procesó esta petición
        String existing = redis.opsForValue().get(
            "idempotency:" + idempotencyKey
        );
        if (existing != null) {
            return PagoResponse.alreadyProcessed(existing);
        }

        // Rate limiting por usuario
        String rateKey = "rate:user:" + request.getUserId();
        Long requests = redis.opsForValue().increment(rateKey);
        redis.expire(rateKey, 60); // 1 minuto

        if (requests > 10) { // Max 10 pagos por minuto
            throw new RateLimitExceededException(
                "Demasiadas solicitudes de pago"
            );
        }

        // Procesar pago
        Pago pago = pagoRepo.save(new Pago(request));

        // Guardar idempotency key
        redis.opsForValue().set(
            "idempotency:" + idempotencyKey,
            pago.getId(),
            86400 // 24 horas
        );

        return PagoResponse.success(pago);
    }
}
```

### 4.4 IoT / Monitoreo

```mermaid
graph TB
    subgraph "IoT Devices"
        D1[Sensor Temperature]
        D2[Sensor Humidity]
        D3[GPS Tracker]
    end

    subgraph "Ingestion"
        MQTT[MQTT Broker]
    end

    subgraph "Processing"
        Flink[Apache Flink]
    end

    subgraph "Storage"
        CASS[(Cassandra<br/>Time-Series<br/>Métricas)]
        REDIS[(Redis<br/>Últimos Valores<br/>TTL Automático)]
        MONGO[(MongoDB<br/>Config Dispositivos)]
        NEO4J[(Neo4j<br/>Dependencias<br/>Dispositivos)]
    end

    D1 --> MQTT
    D2 --> MQTT
    D3 --> MQTT
    MQTT --> Flink
    Flink --> CASS
    Flink --> REDIS
    Flink --> MONGO
    Flink --> NEO4J
```

```python
# IoT Multi-DB Integration
from cassandra.cluster import Cluster
import redis
import pymongo

class IoTMultiDB:

    def __init__(self):
        self.cassandra = Cluster(["127.0.0.1"])
        self.cass_session = self.cassandra.connect("iot")
        self.redis_client = redis.Redis(host="localhost", port=6379)
        self.mongo_client = pymongo.MongoClient("localhost:27017")
        self.mongo_config = self.mongo_client["iot"]["dispositivos"]

    def ingest_metric(self, device_id, metric_type, value):
        """Ingerir métrica: Cassandra (time-series) + Redis (último valor)"""

        # Cassandra: almacenar time-series con TTL de 30 días
        self.cass_session.execute(
            """INSERT INTO metricas
               (device_id, metric_type, timestamp, value)
               VALUES (?, ?, toTimestamp(now()), ?)
               USING TTL 2592000""",
            (device_id, metric_type, value)
        )

        # Redis: último valor con TTL de 1 hora
        self.redis_client.setex(
            f"device:{device_id}:{metric_type}",
            3600,
            json.dumps({
                "value": value,
                "timestamp": datetime.now().isoformat()
            })
        )

    def get_latest(self, device_id, metric_type):
        """Obtener último valor (Redis first, fallback Cassandra)"""
        cached = self.redis_client.get(
            f"device:{device_id}:{metric_type}"
        )
        if cached:
            return json.loads(cached)

        # Fallback to Cassandra
        rows = self.cass_session.execute(
            """SELECT value, timestamp FROM metricas
               WHERE device_id = ? AND metric_type = ?
               LIMIT 1""",
            (device_id, metric_type)
        )
        row = rows.one()
        return {"value": row.value, "timestamp": str(row.timestamp)}

    def get_device_config(self, device_id):
        """Obtener configuración del dispositivo desde MongoDB"""
        return self.mongo_config.find_one({"device_id": device_id})

    def get_device_dependencies(self, device_id):
        """Obtener dependencias desde Neo4j"""
        with self.neo4j_driver.session() as session:
            result = session.run(
                """MATCH (d:Device {id: $id})-[:DEPENDS_ON]->(dep)
                   RETURN dep.id, dep.nombre""",
                id=device_id
            )
            return [dict(r) for r in result]
```

---

## 5. Integración Práctica con Docker Compose

```yaml
# docker-compose.yml — Multi-database environment
version: '3.8'

services:
  # MongoDB
  mongodb:
    image: mongo:7.0
    container_name: mongodb
    ports:
      - "27017:27017"
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: admin123
    volumes:
      - mongodb_data:/data/db
    healthcheck:
      test: echo 'db.runCommand("ping").ok' | mongosh -u admin -p admin123 --authenticationDatabase admin
      interval: 10s
      timeout: 5s
      retries: 5

  # Redis
  redis:
    image: redis:7.2-alpine
    container_name: redis
    ports:
      - "6379:6379"
    command: redis-server --requirepass admin123 --maxmemory 256mb --maxmemory-policy allkeys-lru
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "-a", "admin123", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Neo4j
  neo4j:
    image: neo4j:5.14-community
    container_name: neo4j
    ports:
      - "7474:7474"
      - "7687:7687"
    environment:
      NEO4J_AUTH: neo4j/admin123
      NEO4J_PLUGINS: '["apoc"]'
    volumes:
      - neo4j_data:/data
    healthcheck:
      test: ["CMD", "neo4j", "status"]
      interval: 10s
      timeout: 10s
      retries: 5

  # Cassandra
  cassandra:
    image: cassandra:4.1
    container_name: cassandra
    ports:
      - "9042:9042"
    environment:
      CASSANDRA_CLUSTER_NAME: "TiendaCluster"
      CASSANDRA_DC: "dc1"
    volumes:
      - cassandra_data:/var/lib/cassandra
    healthcheck:
      test: ["CMD-SHELL", "cqlsh -e 'DESCRIBE KEYSPACES;'"]
      interval: 30s
      timeout: 10s
      retries: 5

  # API Service
  api:
    build: ./api
    container_name: api-service
    ports:
      - "8000:8000"
    environment:
      MONGO_URI: mongodb://admin:admin123@mongodb:27017/tienda?authSource=admin
      REDIS_URI: redis://:admin123@redis:6379
      NEO4J_URI: bolt://neo4j:7687
      NEO4J_USER: neo4j
      NEO4J_PASSWORD: admin123
      CASSANDRA_HOST: cassandra
    depends_on:
      mongodb:
        condition: service_healthy
      redis:
        condition: service_healthy
      neo4j:
        condition: service_healthy
      cassandra:
        condition: service_healthy

volumes:
  mongodb_data:
  redis_data:
  neo4j_data:
  cassandra_data:
```

### Inicialización de Cada BD

#### MongoDB: Crear usuario admin y app

```javascript
// init_mongo.js
db = db.getSiblingDB('tienda');

// Crear usuario de aplicación
db.createUser({
    user: "appuser",
    pwd: "app123",
    roles: [
        { role: "readWrite", db: "tienda" }
    ]
});

// Crear colecciones
db.createCollection("usuarios", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["nombre", "email"],
            properties: {
                nombre: { bsonType: "string" },
                email: { bsonType: "string" },
                edad: { bsonType: "int" }
            }
        }
    }
});

db.createCollection("productos");
db.createCollection("pedidos");

// Índices
db.usuarios.createIndex({ "email": 1 }, { unique: true });
db.productos.createIndex({ "nombre": "text", "descripcion": "text" });
db.pedidos.createIndex({ "usuario_id": 1, "fecha": -1 });

print("MongoDB inicializado correctamente");
```

#### Redis: Configurar ACL

```bash
# init_redis.sh — Configurar Redis ACL
redis-cli -a admin123 ACL SETUSER appuser on >app123 +@read +@write -@dangerous
redis-cli -a admin123 ACL SETUSER readonly on >lectura +@read -@write -@dangerous

# Verificar usuarios
redis-cli -a admin123 ACL LIST

# Guardar configuración ACL
redis-cli -a admin123 ACL SAVE
```

#### Neo4j: Crear usuario y datos iniciales

```cypher
// init_neo4j.cypher
// Crear usuario de aplicación
CREATE USER appuser SET PASSWORD 'app123'
GRANT READ TO appuser;

// Crear constrains e índices
CREATE CONSTRAINT usuario_id IF NOT EXISTS
FOR (u:Usuario) REQUIRE u.id IS UNIQUE;

CREATE CONSTRAINT producto_id IF NOT EXISTS
FOR (p:Producto) REQUIRE p.id IS UNIQUE;

CREATE INDEX producto_nombre IF NOT EXISTS
FOR (p:Producto) ON (p.nombre);

// Datos de ejemplo
CREATE (u1:Usuario {id: "u1", nombre: "Juan", email: "juan@ejemplo.com"})
CREATE (u2:Usuario {id: "u2", nombre: "María", email: "maria@ejemplo.com"})
CREATE (p1:Producto {id: "p1", nombre: "Laptop HP", precio: 999.99})
CREATE (p2:Producto {id: "p2", nombre: "Mouse Logitech", precio: 29.99})
CREATE (c1:Categoria {nombre: "Electrónica"})

CREATE (p1)-[:PERTENECE_A]->(c1)
CREATE (p2)-[:PERTENECE_A]->(c1)
CREATE (u1)-[:COMPRO {fecha: datetime(), cantidad: 1}]->(p1)
CREATE (u1)-[:COMPRO {fecha: datetime(), cantidad: 2}]->(p2)
CREATE (u2)-[:COMPRO {fecha: datetime(), cantidad: 1}]->(p2)
CREATE (u1)-[:SIMILAR_A {score: 0.85}]->(u2);
```

#### Cassandra: Crear keyspace, tablas y usuarios

```cql
-- init_cassandra.cql
-- Keyspace
CREATE KEYSPACE IF NOT EXISTS tienda
WITH replication = {
    'class': 'SimpleStrategy',
    'replication_factor': 3
};

USE tienda;

-- Tabla de métricas (time-series)
CREATE TABLE IF NOT EXISTS metricas (
    evento text,
    timestamp timestamp,
    detalle text,
    PRIMARY KEY (evento, timestamp)
) WITH CLUSTERING ORDER BY (timestamp DESC)
  AND default_time_to_live = 2592000;

-- Tabla de historial de pedidos
CREATE TABLE IF NOT EXISTS historial_pedidos (
    usuario_id text,
    pedido_id text,
    fecha timestamp,
    total decimal,
    estado text,
    PRIMARY KEY (usuario_id, fecha)
) WITH CLUSTERING ORDER BY (fecha DESC);

-- Tabla de clickstream
CREATE TABLE IF NOT EXISTS clickstream (
    session_id text,
    timestamp timestamp,
    page text,
    action text,
    PRIMARY KEY (session_id, timestamp)
) WITH CLUSTERING ORDER BY (timestamp DESC);

-- Usuario de aplicación
CREATE ROLE IF NOT EXISTS appuser WITH PASSWORD = 'app123'
  AND LOGIN = true;
GRANT ALL ON KEYSPACE tienda TO appuser;

-- Usuario de solo lectura
CREATE ROLE IF NOT EXISTS readonly WITH PASSWORD = 'lectura'
  AND LOGIN = true;
GRANT SELECT ON KEYSPACE tienda TO readonly;

SELECT * FROM system_auth.roles WHERE role = 'appuser';
```

---

## 6. Ejercicio Práctico

### Ejercicio: Arquitectura Multi-BD Completa

**Objetivo:** Diseñar e implementar un sistema multi-base de datos para una plataforma de e-commerce.

**Requisitos:**
- Docker y Docker Compose instalados
- Python 3.8+ o Java 11+
- Conexión a internet

**Paso 1: Crear el docker-compose.yml**

Copiar el docker-compose.yml de la sección 5.

**Paso 2: Inicializar las bases de datos**

```bash
# Levantar solo las bases de datos
docker-compose up -d mongodb redis neo4j cassandra

# Esperar a que estén listas
docker-compose ps  # Verificar health checks

# Inicializar MongoDB
docker exec -i mongodb mongosh -u admin -p admin123 --authenticationDatabase admin < scripts/init_mongo.js

# Inicializar Redis
docker exec redis redis-cli -a admin123 ACL SETUSER appuser on >app123 +@read +@write

# Inicializar Neo4j
docker exec -i neo4j cypher-shell -u neo4j -p admin123 < scripts/init_neo4j.cypher

# Inicializar Cassandra
docker exec -i cassandra cqlsh < scripts/init_cassandra.cql
```

**Paso 3: Implementar la integración en Python**

Crear `multi_db.py` con la clase `EcommerceMultiDB` mostrada en la sección 4.1.

**Paso 4: Crear API REST**

```python
# api.py
from fastapi import FastAPI, HTTPException
from multi_db import EcommerceMultiDB
from pydantic import BaseModel

app = FastAPI(title="E-commerce Multi-DB API")
db = EcommerceMultiDB()

class UsuarioCreate(BaseModel):
    nombre: str
    email: str

class CarritoItem(BaseModel):
    producto_id: str
    cantidad: int

@app.post("/usuarios")
async def crear_usuario(usuario: UsuarioCreate):
    user_id = db.crear_usuario(usuario.dict())
    return {"id": user_id, "message": "Usuario creado"}

@app.get("/usuarios/{user_id}/recomendaciones")
async def get_recomendaciones(user_id: str):
    recs = db.obtener_recomendaciones(user_id)
    return {"recomendaciones": recs}

@app.post("/carrito/{user_id}/agregar")
async def agregar_al_carrito(user_id: str, item: CarritoItem):
    db.agregar_al_carrito(user_id, item.producto_id, item.cantidad)
    return {"message": "Agregado al carrito"}

@app.get("/carrito/{user_id}")
async def get_carrito(user_id: str):
    return db.obtener_carrito(user_id)

@app.get("/metricas/{evento}")
async def get_metricas(evento: str, horas: int = 24):
    return {"metricas": db.obtener_metricas(evento, horas)}

@app.on_event("shutdown")
async def shutdown():
    db.close()
```

**Paso 5: Verificar cada base de datos**

```bash
# Verificar MongoDB
docker exec mongodb mongosh -u admin -p admin123 --authenticationDatabase admin \
    --eval "db.usuarios.find().toArray()" tienda

# Verificar Redis
docker exec redis redis-cli -a admin123 KEYS "*"

# Verificar Neo4j
docker exec neo4j cypher-shell -u neo4j -p admin123 \
    "MATCH (n) RETURN labels(n), count(n)"

# Verificar Cassandra
docker exec cassandra cqlsh -e "SELECT * FROM tienda.metricas LIMIT 10;"
```

**Paso 6: Medir rendimiento**

```python
# benchmark.py
import time
from multi_db import EcommerceMultiDB

db = EcommerceMultiDB()

# Benchmark MongoDB
start = time.time()
for i in range(1000):
    db.crear_usuario({"nombre": f"User{i}", "email": f"user{i}@test.com"})
mongo_time = time.time() - start

# Benchmark Redis
start = time.time()
for i in range(10000):
    db.redis_client.setex(f"test:{i}", 60, f"value{i}")
redis_time = time.time() - start

# Benchmark Cassandra
start = time.time()
for i in range(10000):
    db.registrar_metrica("benchmark_test", f"item_{i}")
cassandra_time = time.time() - start

print(f"MongoDB (1K inserts): {mongo_time:.2f}s")
print(f"Redis (10K sets): {redis_time:.2f}s")
print(f"Cassandra (10K inserts): {cassandra_time:.2f}s")
```

**Entregable esperado:**

1. docker-compose.yml con las 4 bases de datos y API
2. Scripts de inicialización para cada BD
3. Código Python integrando las 4 bases de datos
4. API REST funcional
5. Benchmark de rendimiento documentado
6. Diagrama de arquitectura personalizado
7. Análisis: ¿por qué cada BD para cada caso de uso?

---

## Resumen de la Clase

| Patrón | Descripción | Cuándo usar |
|---|---|---|
| **Database per Service** | Cada microservicio con su propia BD | Microservicios, independencia |
| **CQRS** | Separar lecturas de escrituras | Alta concurrencia, optimización |
| **Event Sourcing** | Almacenar eventos, no estados | Auditoría, debugging, temporal |
| **Saga** | Transacciones distribuidas sin 2PC | Flujos multi-servicio |
| **CDC** | Propagar cambios en tiempo real | Sincronización entre BD |
| **API Composition** | Combinar datos de múltiples APIs | Consultas cruzadas simples |

---

## Tarea

1. Diseñar arquitectura multi-BD para un sistema de red social
2. Crear docker-compose con MongoDB, Redis, Neo4j y Cassandra
3. Implementar CDC con Debezium entre MongoDB y Redis
4. Implementar CQRS para el servicio de lecturas
5. Implementar Event Sourcing para pedidos
6. Documentar compensaciones de cada decisión de diseño
7. Presentar benchmark comparativo de las 4 BD
