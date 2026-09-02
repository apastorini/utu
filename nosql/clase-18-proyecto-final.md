# Clase 18 — Proyecto Final: Sistema Completo Multi-NoSQL

## Objetivos de Aprendizaje

Al finalizar esta clase y el proyecto, el estudiante sera capaz de:
- Disenar e implementar un sistema completo que integre multiples bases de datos NoSQL
- Aplicar patrones de arquitectura como CQRS, Cache-Aside y Event Sourcing
- Implementar autenticacion JWT, RBAC, rate limiting e input validation
- Configurar monitoreo, health checks y logging estructurado
- Implementar estrategias de backup y restore para cada base de datos
- Realizar pruebas de carga y simular fallos

---

## 1. Diseno del Sistema

### 1.1 Requerimientos Funcionales

| Modulo | Descripcion | Endpoints principales |
|---|---|---|
| **Usuarios** | Registro, login, perfiles | POST /auth/register, POST /auth/login, GET /users/{id} |
| **Productos** | Catalogo CRUD, busqueda | GET /products, POST /products, GET /products/search |
| **Carrito** | Agregar, eliminar, ver carrito | POST /cart/{userId}/add, GET /cart/{userId} |
| **Pedidos** | Crear, confirmar, historial | POST /orders, GET /orders/{id}, GET /orders/user/{id} |
| **Pagos** | Procesar pago, historial | POST /payments, GET /payments/{orderId} |
| **Recomendaciones** | Productos similares, usuarios similares | GET /recommendations/{userId} |
| **Metricas** | Dashboard, clickstream | GET /metrics/dashboard, POST /metrics/event |
| **Inventario** | Stock, reservas | GET /inventory/{productId}, PUT /inventory/{productId} |

### 1.2 Requerimientos No Funcionales

- **Autenticacion JWT** con refresh tokens
- **Rate limiting** por IP y por usuario (sliding window)
- **Cache** para lecturas frecuentes (Cache-Aside pattern)
- **Alta disponibilidad** con replicas en cada BD
- **Seguridad completa**: validacion de inputs, prevencion de inyeccion
- **Monitoreo**: health checks, metricas Prometheus, logging estructurado
- **Backups automatizados** para cada base de datos

### 1.3 Seleccion de BD para Cada Componente

| Componente | BD Seleccionada | Razon |
|---|---|---|
| Usuarios y Productos | MongoDB | Documentos flexibles, busqueda textual |
| Cache y Sesiones | Redis | Velocidad extrema, TTL nativo |
| Carrito de Compras | Redis | Operaciones atomicas, expiracion |
| Recomendaciones | Neo4j | Relaciones complejas, traversals |
| Metricas y Logs | Cassandra | Escritura masiva, time-series |
| Pedidos | MongoDB | Flexibilidad de schema |

### 1.4 Patrones Aplicados

| Patron | Aplicacion | BD involucrada |
|---|---|---|
| **Database per Service** | Cada servicio con su BD | Todas |
| **CQRS** | Lecturas en Redis, escrituras en MongoDB | MongoDB + Redis |
| **Cache-Aside** | Cache de productos frecuentes | Redis |
| **Event Sourcing** | Metricas y auditoria de pedidos | Cassandra |
| **Saga** | Transaccion de pedido (inventario, pago, envio) | MongoDB + Redis |
| **CDC** | MongoDB a Redis para cache | MongoDB + Redis + Kafka |

---

## 2. Arquitectura del Sistema

### 2.1 Diagrama de Componentes

```mermaid
graph TB
    subgraph "Clientes"
        WEB[Web App React/Vue]
        MOB[Mobile App Flutter]
    end

    subgraph "API Layer"
        LB[NGINX Load Balancer]
        AUTH_SVC[Auth Service JWT Tokens]
    end

    subgraph "Business Services"
        USER_SVC[User Service]
        PROD_SVC[Product Service]
        CART_SVC[Cart Service]
        ORDER_SVC[Order Service]
        PAY_SVC[Payment Service]
        RECOM_SVC[Recommendation Service]
        METRIC_SVC[Metrics Service]
    end

    subgraph "Data Layer"
        MONGO[(MongoDB 7.0 Users Products Orders Inventory)]
        REDIS[(Redis 7.2 Sessions Cache Cart Rate Limiting)]
        NEO4J[(Neo4j 5.x Social Graph Recommendations)]
        CASSANDRA[(Cassandra 4.1 Metrics Logs Clickstream)]
    end

    subgraph "Infrastructure"
        KAFKA[Apache Kafka Event Bus]
        PROM[Prometheus Metrics]
        GRAF[Grafana Dashboards]
    end

    WEB --> LB
    MOB --> LB
    LB --> AUTH_SVC
    LB --> PROD_SVC
    LB --> CART_SVC
    LB --> ORDER_SVC
    LB --> PAY_SVC
    LB --> RECOM_SVC
    LB --> METRIC_SVC

    USER_SVC --> MONGO
    PROD_SVC --> MONGO
    PROD_SVC --> REDIS
    CART_SVC --> REDIS
    ORDER_SVC --> MONGO
    PAY_SVC --> MONGO
    PAY_SVC --> REDIS
    RECOM_SVC --> NEO4J
    METRIC_SVC --> CASSANDRA

    ORDER_SVC -->|Publish Events| KAFKA
    KAFKA -->|Consume| METRIC_SVC
    KAFKA -->|Consume| RECOM_SVC
```

### 2.2 Flujo de Datos

```mermaid
sequenceDiagram
    participant C as Cliente
    participant GW as API Gateway
    participant A as Auth Service
    participant P as Product Service
    participant R as Redis Cache
    participant M as MongoDB
    participant CA as Cart Service
    participant O as Order Service

    C->>GW: POST /auth/login
    GW->>A: Verificar credenciales
    A->>M: Buscar usuario
    M-->>A: Usuario
    A->>R: Guardar sesion JWT
    A-->>C: JWT Token

    C->>GW: GET /products?category=laptops
    GW->>P: Buscar productos
    P->>R: GET cache:products:laptops
    alt Cache Hit
        R-->>P: Productos cacheados
    else Cache Miss
        P->>M: FIND productos
        M-->>P: Productos
        P->>R: SET cache TTL 5min
    end
    P-->>C: Lista de productos

    C->>GW: POST /cart/user123/add
    GW->>CA: Agregar al carrito
    CA->>R: HSET carrito:user123
    CA-->>C: Producto agregado

    C->>GW: POST /orders
    GW->>O: Crear pedido
    O->>M: INSERT pedido
    O->>R: Limpiar carrito
    O-->>C: Pedido creado
```

### 2.3 Diagrama de Datos

```mermaid
erDiagram
    USUARIO {
        string _id PK
        string nombre
        string email UK
        string password_hash
        string direccion
        datetime fecha_registro
    }

    PRODUCTO {
        string _id PK
        string nombre
        string descripcion
        double precio
        string categoria
        int stock
        array fotos
        datetime fecha_creacion
    }

    PEDIDO {
        string _id PK
        string usuario_id FK
        array items
        double total
        string estado
        datetime fecha
    }

    USUARIO ||--o{ PEDIDO : "realiza"
    PEDIDO }o--|| PRODUCTO : "contiene"
```

---

## 3. Setup del Proyecto

### 3.1 docker-compose.yml COMPLETO

```yaml
version: '3.8'

services:
  # ===== MongoDB =====
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
      - ./scripts/init_mongo.js:/docker-entrypoint-initdb.d/init_mongo.js
    networks:
      - app-network
    healthcheck:
      test: echo 'db.runCommand("ping").ok' | mongosh -u admin -p admin123 --authenticationDatabase admin --quiet
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  # ===== Redis =====
  redis:
    image: redis:7.2-alpine
    container_name: redis
    ports:
      - "6379:6379"
    command: >
      redis-server
      --requirepass admin123
      --maxmemory 256mb
      --maxmemory-policy allkeys-lru
      --appendonly yes
      --appendfsync everysec
    volumes:
      - redis_data:/data
    networks:
      - app-network
    healthcheck:
      test: ["CMD", "redis-cli", "-a", "admin123", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  # ===== Neo4j =====
  neo4j:
    image: neo4j:5.14-community
    container_name: neo4j
    ports:
      - "7474:7474"
      - "7687:7687"
    environment:
      NEO4J_AUTH: neo4j/admin123
      NEO4J_PLUGINS: '["apoc"]'
      NEO4J_server_memory_heap_initial__size: 256m
      NEO4J_server_memory_heap_max__size: 512m
    volumes:
      - neo4j_data:/data
      - ./scripts/init_neo4j.cypher:/var/lib/neo4j/init/init_neo4j.cypher
    networks:
      - app-network
    healthcheck:
      test: ["CMD", "neo4j", "status"]
      interval: 15s
      timeout: 10s
      retries: 5
    restart: unless-stopped

  # ===== Cassandra =====
  cassandra:
    image: cassandra:4.1
    container_name: cassandra
    ports:
      - "9042:9042"
    environment:
      CASSANDRA_CLUSTER_NAME: "TiendaCluster"
      CASSANDRA_DC: "dc1"
      CASSANDRA_RACK: "rack1"
      CASSANDRA_ENDPOINT_SNITCH: SimpleSnitch
    volumes:
      - cassandra_data:/var/lib/cassandra
    networks:
      - app-network
    healthcheck:
      test: ["CMD-SHELL", "cqlsh -e 'DESCRIBE KEYSPACES;'"]
      interval: 30s
      timeout: 10s
      retries: 10
    restart: unless-stopped

  # ===== API Service =====
  api:
    build:
      context: ./api
      dockerfile: Dockerfile
    container_name: api-service
    ports:
      - "8000:8000"
    environment:
      MONGO_URI: mongodb://admin:admin123@mongodb:27017/tienda?authSource=admin
      REDIS_HOST: redis
      REDIS_PORT: 6379
      REDIS_PASSWORD: admin123
      NEO4J_URI: bolt://neo4j:7687
      NEO4J_USER: neo4j
      NEO4J_PASSWORD: admin123
      CASSANDRA_HOST: cassandra
      JWT_SECRET: mi-secreto-super-seguro-cambiar-en-produccion
      JWT_EXPIRY: 3600
      REFRESH_TOKEN_EXPIRY: 604800
    volumes:
      - ./api:/app
    networks:
      - app-network
    depends_on:
      mongodb:
        condition: service_healthy
      redis:
        condition: service_healthy
      neo4j:
        condition: service_healthy
      cassandra:
        condition: service_healthy
    restart: unless-stopped

  # ===== Prometheus =====
  prometheus:
    image: prom/prometheus:v2.47.0
    container_name: prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./config/prometheus.yml:/etc/prometheus/prometheus.yml
    networks:
      - app-network
    restart: unless-stopped

  # ===== Grafana =====
  grafana:
    image: grafana/grafana:10.1.0
    container_name: grafana
    ports:
      - "3000:3000"
    environment:
      GF_SECURITY_ADMIN_PASSWORD: admin123
    volumes:
      - grafana_data:/var/lib/grafana
    networks:
      - app-network
    depends_on:
      - prometheus
    restart: unless-stopped

volumes:
  mongodb_data:
  redis_data:
  neo4j_data:
  cassandra_data:
  grafana_data:

networks:
  app-network:
    driver: bridge
```

### 3.2 Inicializacion de Cada BD

#### MongoDB: Crear usuario admin, usuario app, esquemas e indices

```javascript
// scripts/init_mongo.js
db = db.getSiblingDB('tienda');

// Crear usuario de aplicacion
db.createUser({
    user: "appuser",
    pwd: "app123",
    roles: [{ role: "readWrite", db: "tienda" }]
});

// Crear colecciones con validacion
db.createCollection("usuarios", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["nombre", "email", "password_hash"],
            properties: {
                nombre: { bsonType: "string", description: "Nombre del usuario" },
                email: { bsonType: "string", description: "Email unico" },
                password_hash: { bsonType: "string" },
                direccion: {
                    bsonType: "object",
                    properties: {
                        calle: { bsonType: "string" },
                        ciudad: { bsonType: "string" },
                        pais: { bsonType: "string" },
                        codigo_postal: { bsonType: "string" }
                    }
                },
                activo: { bsonType: "bool" }
            }
        }
    }
});

db.createCollection("productos", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["nombre", "precio", "categoria"],
            properties: {
                nombre: { bsonType: "string" },
                descripcion: { bsonType: "string" },
                precio: { bsonType: "double", minimum: 0 },
                categoria: { bsonType: "string" },
                stock: { bsonType: "int", minimum: 0 },
                fotos: { bsonType: "array", items: { bsonType: "string" } },
                especificaciones: { bsonType: "object" }
            }
        }
    }
});

db.createCollection("pedidos", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["usuario_id", "items", "total", "estado"],
            properties: {
                usuario_id: { bsonType: "string" },
                items: { bsonType: "array" },
                total: { bsonType: "double", minimum: 0 },
                estado: {
                    bsonType: "string",
                    enum: ["CREADO", "CONFIRMADO", "ENVIADO", "ENTREGADO", "CANCELADO"]
                }
            }
        }
    }
});

// Indices
db.usuarios.createIndex({ "email": 1 }, { unique: true });
db.usuarios.createIndex({ "nombre": "text" });
db.productos.createIndex({ "nombre": "text", "descripcion": "text" });
db.productos.createIndex({ "categoria": 1, "precio": 1 });
db.productos.createIndex({ "precio": 1 });
db.pedidos.createIndex({ "usuario_id": 1, "fecha": -1 });
db.pedidos.createIndex({ "estado": 1 });

print("MongoDB inicializado correctamente");
```

#### Redis: Configurar ACL

```bash
#!/bin/bash
# scripts/init_redis.sh
echo "Configurando Redis ACL..."

docker exec redis redis-cli -a admin123 ACL SETUSER appuser on ">app123" "+@read" "+@write" "-@dangerous"
docker exec redis redis-cli -a admin123 ACL SETUSER readonly on ">lectura" "+@read" "-@write" "-@dangerous"
docker exec redis redis-cli -a admin123 ACL SAVE

echo "Redis ACL configurado:"
docker exec redis redis-cli -a admin123 ACL LIST
```

#### Neo4j: Crear usuario, roles, constraints y datos

```cypher
// scripts/init_neo4j.cypher
// Crear usuario de aplicacion
CREATE USER appuser SET PASSWORD 'app123';
GRANT READ TO appuser;

// Constraints
CREATE CONSTRAINT usuario_id IF NOT EXISTS FOR (u:Usuario) REQUIRE u.id IS UNIQUE;
CREATE CONSTRAINT producto_id IF NOT EXISTS FOR (p:Producto) REQUIRE p.id IS UNIQUE;
CREATE CONSTRAINT categoria_nombre IF NOT EXISTS FOR (c:Categoria) REQUIRE c.nombre IS UNIQUE;

// Indices
CREATE INDEX producto_nombre IF NOT EXISTS FOR (p:Producto) ON (p.nombre);
CREATE INDEX producto_precio IF NOT EXISTS FOR (p:Producto) ON (p.precio);

// Datos iniciales
CREATE (u1:Usuario {id: "u1", nombre: "Juan Perez", email: "juan@ejemplo.com"});
CREATE (u2:Usuario {id: "u2", nombre: "Maria Garcia", email: "maria@ejemplo.com"});
CREATE (u3:Usuario {id: "u3", nombre: "Carlos Lopez", email: "carlos@ejemplo.com"});

CREATE (cat1:Categoria {nombre: "Laptops"});
CREATE (cat2:Categoria {nombre: "Accesorios"});
CREATE (cat3:Categoria {nombre: "Audio"});

CREATE (p1:Producto {id: "p1", nombre: "Laptop HP Pavilion", precio: 899.99});
CREATE (p2:Producto {id: "p2", nombre: "Mouse Logitech MX", precio: 79.99});
CREATE (p3:Producto {id: "p3", nombre: "Teclado Mecanico RGB", precio: 129.99});
CREATE (p4:Producto {id: "p4", nombre: "Auriculares Sony WH", precio: 299.99});
CREATE (p5:Producto {id: "p5", nombre: "Laptop Dell XPS", precio: 1299.99});
CREATE (p6:Producto {id: "p6", nombre: "Webcam HD Logitech", precio: 69.99});

CREATE (p1)-[:PERTENECE_A]->(cat1);
CREATE (p2)-[:PERTENECE_A]->(cat2);
CREATE (p3)-[:PERTENECE_A]->(cat2);
CREATE (p4)-[:PERTENECE_A]->(cat3);
CREATE (p5)-[:PERTENECE_A]->(cat1);
CREATE (p6)-[:PERTENECE_A]->(cat2);

// Relaciones de compra
CREATE (u1)-[:COMPRO {fecha: date('2026-01-10'), cantidad: 1}]->(p1);
CREATE (u1)-[:COMPRO {fecha: date('2026-01-10'), cantidad: 1}]->(p2);
CREATE (u1)-[:COMPRO {fecha: date('2026-01-12'), cantidad: 1}]->(p4);
CREATE (u2)-[:COMPRO {fecha: date('2026-01-11'), cantidad: 1}]->(p1);
CREATE (u2)-[:COMPRO {fecha: date('2026-01-11'), cantidad: 1}]->(p3);
CREATE (u3)-[:COMPRO {fecha: date('2026-01-13'), cantidad: 1}]->(p2);
CREATE (u3)-[:COMPRO {fecha: date('2026-01-13'), cantidad: 1}]->(p5);
CREATE (u3)-[:COMPRO {fecha: date('2026-01-15'), cantidad: 1}]->(p4);

// Relaciones sociales
CREATE (u1)-[:SIGUE]->(u2);
CREATE (u1)-[:SIGUE]->(u3);
CREATE (u2)-[:SIGUE]->(u1);

// Similaridad de usuarios (basada en compras)
CREATE (u1)-[:SIMILAR_A {score: 0.85}]->(u2);
CREATE (u2)-[:SIMILAR_A {score: 0.85}]->(u1);
CREATE (u1)-[:SIMILAR_A {score: 0.70}]->(u3);
```

#### Cassandra: Crear keyspace, tablas y usuarios

```cql
-- scripts/init_cassandra.cql
-- Keyspace con replicacion
CREATE KEYSPACE IF NOT EXISTS tienda
WITH replication = {
    'class': 'SimpleStrategy',
    'replication_factor': 3
};

USE tienda;

-- Tabla de metricas (time-series)
CREATE TABLE IF NOT EXISTS metricas (
    metric_name text,
    timestamp timestamp,
    value text,
    source text,
    PRIMARY KEY (metric_name, timestamp)
) WITH CLUSTERING ORDER BY (timestamp DESC)
  AND default_time_to_live = 7776000;

-- Tabla de clickstream
CREATE TABLE IF NOT EXISTS clickstream (
    session_id text,
    timestamp timestamp,
    user_id text,
    event_type text,
    page text,
    details text,
    PRIMARY KEY (session_id, timestamp)
) WITH CLUSTERING ORDER BY (timestamp DESC)
  AND default_time_to_live = 2592000;

-- Tabla de audit log
CREATE TABLE IF NOT EXISTS audit_log (
    entity_type text,
    timestamp timestamp,
    entity_id text,
    action text,
    user_id text,
    old_values text,
    new_values text,
    PRIMARY KEY (entity_type, timestamp)
) WITH CLUSTERING ORDER BY (timestamp DESC);

-- Tabla de historial de pedidos (por usuario)
CREATE TABLE IF NOT EXISTS historial_pedidos (
    usuario_id text,
    fecha timestamp,
    pedido_id text,
    total decimal,
    estado text,
    items text,
    PRIMARY KEY (usuario_id, fecha)
) WITH CLUSTERING ORDER BY (fecha DESC);

-- Usuario de aplicacion
CREATE ROLE IF NOT EXISTS appuser WITH PASSWORD = 'app123' AND LOGIN = true;
GRANT ALL ON KEYSPACE tienda TO appuser;

-- Usuario de solo lectura
CREATE ROLE IF NOT EXISTS readonly_user WITH PASSWORD = 'lectura' AND LOGIN = true;
GRANT SELECT ON KEYSPACE tienda TO readonly_user;
```

---

## 4. Implementacion del Backend

### 4.1 Estructura del Proyecto

```
api/
  Dockerfile
  requirements.txt
  main.py                    # FastAPI app
  config.py                  # Configuration
  auth/
    __init__.py
    jwt_handler.py           # JWT creation and verification
    middleware.py            # Auth middleware
    rbac.py                  # Role-based access control
  services/
    __init__.py
    user_service.py          # MongoDB users
    product_service.py       # MongoDB + Redis cache
    cart_service.py          # Redis cart
    order_service.py         # MongoDB orders
    recommendation_service.py # Neo4j recommendations
    metrics_service.py       # Cassandra metrics
    inventory_service.py     # MongoDB inventory
  models/
    __init__.py
    schemas.py               # Pydantic models
  middleware/
    __init__.py
    rate_limiter.py          # Redis rate limiting
    security.py              # Input validation
  utils/
    __init__.py
    database.py              # DB connections
```

### 4.2 Configuracion y Dependencias

```python
# config.py
import os

class Settings:
    MONGO_URI: str = os.getenv("MONGO_URI",
        "mongodb://admin:admin123@localhost:27017/tienda?authSource=admin")
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_PASSWORD: str = os.getenv("REDIS_PASSWORD", "admin123")
    NEO4J_URI: str = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    NEO4J_USER: str = os.getenv("NEO4J_USER", "neo4j")
    NEO4J_PASSWORD: str = os.getenv("NEO4J_PASSWORD", "admin123")
    CASSANDRA_HOST: str = os.getenv("CASSANDRA_HOST", "127.0.0.1")
    JWT_SECRET: str = os.getenv("JWT_SECRET", "mi-secreto-super-seguro")
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRY: int = int(os.getenv("JWT_EXPIRY", "3600"))
    REFRESH_TOKEN_EXPIRY: int = int(os.getenv("REFRESH_TOKEN_EXPIRY", "604800"))
    CACHE_TTL: int = 300
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW: int = 60

settings = Settings()
```

```
# requirements.txt
fastapi==0.104.1
uvicorn==0.24.0
pymongo==4.6.1
redis==5.0.1
neo4j==5.14.0
cassandra-driver==3.29.0
passlib==1.7.4
python-jose[cryptography]==3.3.0
bcrypt==4.1.2
pydantic==2.5.3
prometheus-client==0.19.0
prometheus-fastapi-instrumentator==6.1.0
httpx==0.25.2
```

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

### 4.3 Database Connections

```python
# utils/database.py
from pymongo import MongoClient
from redis import Redis
from neo4j import GraphDatabase
from cassandra.cluster import Cluster
from config import settings

class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True

        # MongoDB
        self.mongo_client = MongoClient(settings.MONGO_URI)
        self.mongo_db = self.mongo_client["tienda"]

        # Redis
        self.redis_client = Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            password=settings.REDIS_PASSWORD,
            decode_responses=True,
            socket_connect_timeout=5,
            retry_on_timeout=True
        )

        # Neo4j
        self.neo4j_driver = GraphDatabase.driver(
            settings.NEO4J_URI,
            auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
        )

        # Cassandra
        self.cassandra_cluster = Cluster(
            [settings.CASSANDRA_HOST],
            protocol_version=4
        )
        self.cassandra_session = self.cassandra_cluster.connect("tienda")

    @property
    def usuarios(self):
        return self.mongo_db["usuarios"]

    @property
    def productos(self):
        return self.mongo_db["productos"]

    @property
    def pedidos(self):
        return self.mongo_db["pedidos"]

    def close(self):
        self.mongo_client.close()
        self.redis_client.close()
        self.neo4j_driver.close()
        self.cassandra_cluster.shutdown()

db = Database()
```

### 4.4 MongoDB Service — CRUD de Productos

```python
# services/product_service.py
from bson import ObjectId
from typing import Optional, List
from models.schemas import ProductoCreate, ProductoResponse
from utils.database import db
from config import settings
import json

class ProductService:

    def __init__(self):
        self.collection = db.productos
        self.cache = db.redis_client
        self.cache_ttl = settings.CACHE_TTL

    def crear_producto(self, producto: ProductoCreate) -> ProductoResponse:
        data = producto.model_dump()
        result = self.collection.insert_one(data)
        data["_id"] = str(result.inserted_id)

        # Invalidar cache de listados
        keys = self.cache.keys("products:*")
        if keys:
            self.cache.delete(*keys)

        return ProductoResponse(**data)

    def obtener_producto(self, producto_id: str) -> Optional[ProductoResponse]:
        cache_key = f"product:{producto_id}"
        cached = self.cache.get(cache_key)

        if cached:
            return ProductoResponse(**json.loads(cached))

        doc = self.collection.find_one({"_id": ObjectId(producto_id)})
        if doc:
            doc["_id"] = str(doc["_id"])
            self.cache.setex(cache_key, self.cache_ttl, json.dumps(doc, default=str))
            return ProductoResponse(**doc)
        return None

    def listar_productos(self, categoria: Optional[str] = None,
                         skip: int = 0, limit: int = 20) -> List[ProductoResponse]:
        cache_key = f"products:{categoria}:{skip}:{limit}"
        cached = self.cache.get(cache_key)

        if cached:
            return [ProductoResponse(**p) for p in json.loads(cached)]

        query = {"activo": True}
        if categoria:
            query["categoria"] = categoria

        docs = list(self.collection.find(query).skip(skip).limit(limit))
        for doc in docs:
            doc["_id"] = str(doc["_id"])

        self.cache.setex(cache_key, self.cache_ttl, json.dumps(docs, default=str))
        return [ProductoResponse(**d) for d in docs]

    def buscar_productos(self, texto: str) -> List[ProductoResponse]:
        cache_key = f"search:{hash(texto)}"
        cached = self.cache.get(cache_key)

        if cached:
            return [ProductoResponse(**p) for p in json.loads(cached)]

        docs = list(self.collection.find(
            {"$text": {"$search": texto}},
            {"score": {"$meta": "textScore"}}
        ).sort([("score", {"$meta": "textScore"})]).limit(20))

        for doc in docs:
            doc["_id"] = str(doc["_id"])

        self.cache.setex(cache_key, 60, json.dumps(docs, default=str))
        return [ProductoResponse(**d) for d in docs]

    def actualizar_producto(self, producto_id: str,
                            updates: dict) -> Optional[ProductoResponse]:
        result = self.collection.update_one(
            {"_id": ObjectId(producto_id)},
            {"$set": updates}
        )

        if result.modified_count > 0:
            # Invalidar cache
            self.cache.delete(f"product:{producto_id}")
            keys = self.cache.keys("products:*")
            if keys:
                self.cache.delete(*keys)
            return self.obtener_producto(producto_id)
        return None

    def eliminar_producto(self, producto_id: str) -> bool:
        result = self.collection.update_one(
            {"_id": ObjectId(producto_id)},
            {"$set": {"activo": False}}
        )

        if result.modified_count > 0:
            self.cache.delete(f"product:{producto_id}")
            keys = self.cache.keys("products:*")
            if keys:
                self.cache.delete(*keys)
            return True
        return False

    def reducir_stock(self, producto_id: str, cantidad: int) -> bool:
        result = self.collection.update_one(
            {"_id": ObjectId(producto_id), "stock": {"$gte": cantidad}},
            {"$inc": {"stock": -cantidad}}
        )
        if result.modified_count > 0:
            self.cache.delete(f"product:{producto_id}")
            return True
        return False
```

### 4.5 Redis Service — Carrito de Compras, Sesion, Rate Limiting

```python
# services/cart_service.py
from typing import Optional, Dict
import json
from utils.database import db
from datetime import datetime

class CartService:

    CART_TTL = 86400  # 24 horas

    def __init__(self):
        self.redis = db.redis_client

    def agregar_item(self, user_id: str, producto_id: str,
                     cantidad: int, precio: float, nombre: str) -> Dict:
        cart_key = f"cart:{user_id}"
        item_key = f"item:{producto_id}"

        item_data = json.dumps({
            "producto_id": producto_id,
            "nombre": nombre,
            "cantidad": cantidad,
            "precio_unitario": precio,
            "subtotal": precio * cantidad,
            "agregado_en": datetime.now().isoformat()
        })

        self.redis.hset(cart_key, item_key, item_data)
        self.redis.expire(cart_key, self.CART_TTL)

        return self.obtener_carrito(user_id)

    def obtener_carrito(self, user_id: str) -> Dict:
        cart_key = f"cart:{user_id}"
        items_raw = self.redis.hgetall(cart_key)

        items = []
        total = 0.0
        for key, value in items_raw.items():
            item = json.loads(value)
            items.append(item)
            total += item["subtotal"]

        return {
            "user_id": user_id,
            "items": items,
            "total_items": len(items),
            "total": round(total, 2),
            "ttl": self.redis.ttl(cart_key)
        }

    def actualizar_cantidad(self, user_id: str, producto_id: str,
                            nueva_cantidad: int) -> Optional[Dict]:
        cart_key = f"cart:{user_id}"
        item_key = f"item:{producto_id}"

        existing = self.redis.hget(cart_key, item_key)
        if not existing:
            return None

        item = json.loads(existing)
        item["cantidad"] = nueva_cantidad
        item["subtotal"] = item["precio_unitario"] * nueva_cantidad
        item["modificado_en"] = datetime.now().isoformat()

        self.redis.hset(cart_key, item_key, json.dumps(item))
        return self.obtener_carrito(user_id)

    def eliminar_item(self, user_id: str, producto_id: str) -> Dict:
        cart_key = f"cart:{user_id}"
        item_key = f"item:{producto_id}"
        self.redis.hdel(cart_key, item_key)
        return self.obtener_carrito(user_id)

    def vaciar_carrito(self, user_id: str) -> None:
        self.redis.delete(f"cart:{user_id}")

    def carrito_existe(self, user_id: str) -> bool:
        return self.redis.exists(f"cart:{user_id}") > 0
```

```python
# services/user_service.py
from bson import ObjectId
from typing import Optional
from passlib.context import CryptContext
from models.schemas import UserCreate, UserResponse
from utils.database import db
from config import settings
import json

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:

    def __init__(self):
        self.collection = db.usuarios
        self.cache = db.redis_client

    def crear_usuario(self, user: UserCreate) -> UserResponse:
        existing = self.collection.find_one({"email": user.email})
        if existing:
            raise ValueError("El email ya esta registrado")

        user_data = user.model_dump()
        user_data["password_hash"] = pwd_context.hash(user.password)
        del user_data["password"]
        user_data["activo"] = True

        result = self.collection.insert_one(user_data)
        user_data["_id"] = str(result.inserted_id)

        return UserResponse(
            id=user_data["_id"],
            nombre=user_data["nombre"],
            email=user_data["email"]
        )

    def autenticar(self, email: str, password: str) -> Optional[dict]:
        doc = self.collection.find_one({"email": email})
        if doc and pwd_context.verify(password, doc["password_hash"]):
            doc["_id"] = str(doc["_id"])
            return doc
        return None

    def obtener_usuario(self, user_id: str) -> Optional[UserResponse]:
        cache_key = f"user:{user_id}"
        cached = self.cache.get(cache_key)

        if cached:
            data = json.loads(cached)
            return UserResponse(**data)

        doc = self.collection.find_one({"_id": ObjectId(user_id)})
        if doc:
            doc["_id"] = str(doc["_id"])
            safe_data = {k: v for k, v in doc.items() if k != "password_hash"}
            self.cache.setex(cache_key, 300, json.dumps(safe_data, default=str))
            return UserResponse(
                id=doc["_id"],
                nombre=doc["nombre"],
                email=doc["email"]
            )
        return None
```

### 4.6 Neo4j Service — Recomendaciones

```python
# services/recommendation_service.py
from typing import List, Dict
from utils.database import db

class RecommendationService:

    def __init__(self):
        self.driver = db.neo4j_driver

    def obtener_recomendaciones(self, user_id: str, limit: int = 5) -> List[Dict]:
        query = """
        MATCH (u:Usuario {id: $user_id})-[:COMPRO]->(p:Producto)
              -[:PERTENECE_A]->(c:Categoria)
              <-[:PERTENECE_A]-(recomendado:Producto)
        WHERE NOT (u)-[:COMPRO]->(recomendado)
          AND recomendado.precio > 0
        RETURN recomendado.id AS id,
               recomendado.nombre AS nombre,
               recomendado.precio AS precio,
               COUNT(*) AS relevancia
        ORDER BY relevancia DESC
        LIMIT $limit
        """

        with self.driver.session() as session:
            result = session.run(query, user_id=user_id, limit=limit)
            return [dict(record) for record in result]

    def usuarios_similares(self, user_id: str, limit: int = 5) -> List[Dict]:
        query = """
        MATCH (u:Usuario {id: $user_id})-[:SIGUE|SIMILAR_A]-(similar:Usuario)
        WHERE similar.id <> $user_id
        RETURN similar.id AS id,
               similar.nombre AS nombre,
               similar.email AS email
        LIMIT $limit
        """

        with self.driver.session() as session:
            result = session.run(query, user_id=user_id, limit=limit)
            return [dict(record) for record in result]

    def productos_comprados_juntos(self, producto_id: str,
                                    limit: int = 5) -> List[Dict]:
        query = """
        MATCH (p:Producto {id: $producto_id})<-[:COMPRO]-(u:Usuario)
              -[:COMPRO]->(otro:Producto)
        WHERE otro.id <> $producto_id
        RETURN otro.id AS id,
               otro.nombre AS nombre,
               otro.precio AS precio,
               COUNT(DISTINCT u) AS frecuencia
        ORDER BY frecuencia DESC
        LIMIT $limit
        """

        with self.driver.session() as session:
            result = session.run(query, producto_id=producto_id, limit=limit)
            return [dict(record) for record in result]

    def registrar_compra(self, user_id: str, pedido_id: str,
                         items: List[Dict]) -> None:
        query = """
        MATCH (u:Usuario {id: $user_id})
        UNWIND $items AS item
        MATCH (p:Producto {id: item.producto_id})
        CREATE (u)-[:COMPRO {
            pedido_id: $pedido_id,
            fecha: datetime(),
            cantidad: item.cantidad
        }]->(p)
        """

        with self.driver.session() as session:
            session.run(query,
                user_id=user_id,
                pedido_id=pedido_id,
                items=items
            )
```

### 4.7 Cassandra Service — Metricas

```python
# services/metrics_service.py
from datetime import datetime, timedelta
from typing import List, Dict
from utils.database import db
import json

class MetricsService:

    def __init__(self):
        self.session = db.cassandra_session

    def registrar_evento(self, metric_name: str, value: str,
                         source: str = "api") -> None:
        query = """
        INSERT INTO metricas (metric_name, timestamp, value, source)
        VALUES (?, ?, ?, ?)
        """
        self.session.execute(query, (metric_name, datetime.now(), value, source))

    def registrar_clickstream(self, session_id: str, user_id: str,
                               event_type: str, page: str,
                               details: str = "") -> None:
        query = """
        INSERT INTO clickstream
        (session_id, timestamp, user_id, event_type, page, details)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        self.session.execute(query, (
            session_id, datetime.now(), user_id,
            event_type, page, details
        ))

    def registrar_audit(self, entity_type: str, entity_id: str,
                        action: str, user_id: str,
                        old_values: str = "", new_values: str = "") -> None:
        query = """
        INSERT INTO audit_log
        (entity_type, timestamp, entity_id, action, user_id,
         old_values, new_values)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        self.session.execute(query, (
            entity_type, datetime.now(), entity_id,
            action, user_id, old_values, new_values
        ))

    def obtener_metricas(self, metric_name: str,
                          horas: int = 24) -> List[Dict]:
        desde = datetime.now() - timedelta(hours=horas)
        query = """
        SELECT timestamp, value, source FROM metricas
        WHERE metric_name = ? AND timestamp > ?
        ORDER BY timestamp DESC
        """
        rows = self.session.execute(query, (metric_name, desde))
        return [{"timestamp": str(r.timestamp), "value": r.value,
                 "source": r.source} for r in rows]

    def obtener_historial_pedidos(self, user_id: str,
                                   limit: int = 50) -> List[Dict]:
        query = """
        SELECT fecha, pedido_id, total, estado
        FROM historial_pedidos
        WHERE usuario_id = ?
        LIMIT ?
        """
        rows = self.session.execute(query, (user_id, limit))
        return [{"fecha": str(r.fecha), "pedido_id": r.pedido_id,
                 "total": float(r.total), "estado": r.estado}
                for r in rows]

    def dashboard_metricas(self) -> Dict:
        now = datetime.now()
        ultima_hora = now - timedelta(hours=1)
        hoy = now.replace(hour=0, minute=0, second=0, microsecond=0)

        queries = {
            "pedidos_hoy": """
                SELECT COUNT(*) as total FROM historial_pedidos
                WHERE usuario_id = 'counter' AND fecha > ?
                ALLOW FILTERING
            """,
            "eventos_hora": """
                SELECT COUNT(*) as total FROM metricas
                WHERE metric_name = 'api_request' AND timestamp > ?
            """
        }

        result = {}
        for name, query in queries.items():
            rows = self.session.execute(query, [ultima_hora if "hora" in name else hoy])
            row = rows.one()
            result[name] = row.total if row else 0

        return result
```

### 4.8 Order Service — Crear Pedido

```python
# services/order_service.py
from bson import ObjectId
from typing import Optional, List
from datetime import datetime
from models.schemas import OrderCreate, OrderResponse
from utils.database import db
from services.cart_service import CartService
from services.product_service import ProductService
from services.metrics_service import MetricsService
from services.recommendation_service import RecommendationService
import json

class OrderService:

    def __init__(self):
        self.collection = db.pedidos
        self.cache = db.redis_client
        self.cart_service = CartService()
        self.product_service = ProductService()
        self.metrics_service = MetricsService()
        self.recommendation_service = RecommendationService()

    def crear_pedido(self, user_id: str, order: OrderCreate) -> OrderResponse:
        # Obtener carrito
        carrito = self.cart_service.obtener_carrito(user_id)
        if not carrito["items"]:
            raise ValueError("El carrito esta vacio")

        # Verificar stock
        for item in carrito["items"]:
            producto = self.product_service.obtener_producto(item["producto_id"])
            if not producto or producto.stock < item["cantidad"]:
                raise ValueError(
                    f"Stock insuficiente para {item.get('nombre', 'producto')}"
                )

        # Crear pedido
        pedido_data = {
            "usuario_id": user_id,
            "items": carrito["items"],
            "total": carrito["total"],
            "estado": "CREADO",
            "direccion_envio": order.direccion_envio,
            "metodo_pago": order.metodo_pago,
            "fecha": datetime.now(),
            "fecha_actualizacion": datetime.now()
        }

        result = self.collection.insert_one(pedido_data)
        pedido_id = str(result.inserted_id)

        # Reducir stock
        for item in carrito["items"]:
            self.product_service.reducir_stock(
                item["producto_id"], item["cantidad"]
            )

        # Registrar en Cassandra (historial)
        self._registrar_historial_cassandra(user_id, pedido_id, pedido_data)

        # Registrar metrica
        self.metrics_service.registrar_evento(
            "pedido_creado",
            json.dumps({"pedido_id": pedido_id, "total": carrito["total"]})
        )

        # Registrar compra en Neo4j
        items_neo4j = [
            {"producto_id": item["producto_id"], "cantidad": item["cantidad"]}
            for item in carrito["items"]
        ]
        self.recommendation_service.registrar_compra(
            user_id, pedido_id, items_neo4j
        )

        # Vaciar carrito
        self.cart_service.vaciar_carrito(user_id)

        pedido_data["_id"] = pedido_id
        return OrderResponse(**pedido_data)

    def obtener_pedido(self, pedido_id: str) -> Optional[OrderResponse]:
        cache_key = f"order:{pedido_id}"
        cached = self.cache.get(cache_key)

        if cached:
            return OrderResponse(**json.loads(cached))

        doc = self.collection.find_one({"_id": ObjectId(pedido_id)})
        if doc:
            doc["_id"] = str(doc["_id"])
            self.cache.setex(cache_key, 300, json.dumps(doc, default=str))
            return OrderResponse(**doc)
        return None

    def pedidos_usuario(self, user_id: str) -> List[OrderResponse]:
        docs = list(self.collection.find(
            {"usuario_id": user_id}
        ).sort("fecha", -1).limit(50))

        for doc in docs:
            doc["_id"] = str(doc["_id"])

        return [OrderResponse(**d) for d in docs]

    def _registrar_historial_cassandra(self, user_id: str,
                                        pedido_id: str, data: dict) -> None:
        query = """
        INSERT INTO historial_pedidos
        (usuario_id, fecha, pedido_id, total, estado, items)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        db.cassandra_session.execute(query, (
            user_id, data["fecha"], pedido_id,
            data["total"], data["estado"],
            json.dumps(data["items"], default=str)
        ))
```

### 4.9 JWT Authentication

```python
# auth/jwt_handler.py
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import HTTPException, status
from config import settings

def create_access_token(user_id: str, email: str, role: str = "user") -> str:
    expire = datetime.utcnow() + timedelta(seconds=settings.JWT_EXPIRY)
    payload = {
        "sub": user_id,
        "email": email,
        "role": role,
        "type": "access",
        "exp": expire,
        "iat": datetime.utcnow()
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

def create_refresh_token(user_id: str) -> str:
    expire = datetime.utcnow() + timedelta(seconds=settings.REFRESH_TOKEN_EXPIRY)
    payload = {
        "sub": user_id,
        "type": "refresh",
        "exp": expire,
        "iat": datetime.utcnow()
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalido o expirado"
        )
```

```python
# auth/middleware.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from auth.jwt_handler import verify_token

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    token = credentials.credentials
    payload = verify_token(token)

    if payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tipo de token invalido"
        )

    return payload

async def require_admin(user: dict = Depends(get_current_user)) -> dict:
    if user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requieren permisos de administrador"
        )
    return user
```

```python
# auth/rbac.py
from enum import Enum

class Role(Enum):
    ADMIN = "admin"
    USER = "user"
    VENDOR = "vendor"

PERMISSIONS = {
    Role.ADMIN: {
        "users:read", "users:write", "users:delete",
        "products:read", "products:write", "products:delete",
        "orders:read", "orders:write", "orders:cancel",
        "payments:read", "payments:write",
        "metrics:read", "metrics:write",
        "inventory:read", "inventory:write",
        "admin:all"
    },
    Role.USER: {
        "users:read:own", "users:write:own",
        "products:read",
        "orders:read:own", "orders:write",
        "payments:read:own",
        "inventory:read"
    },
    Role.VENDOR: {
        "products:read", "products:write:own",
        "orders:read:own",
        "inventory:read", "inventory:write:own",
        "metrics:read:own"
    }
}

def has_permission(role: str, permission: str) -> bool:
    user_role = Role(role) if role in [r.value for r in Role] else Role.USER
    return permission in PERMISSIONS.get(user_role, set())
```

### 4.10 Rate Limiting

```python
# middleware/rate_limiter.py
from fastapi import Request, HTTPException, status
from utils.database import db
from datetime import datetime
import time

class RateLimiter:

    def __init__(self):
        self.redis = db.redis_client

    def is_allowed(self, key: str, max_requests: int = 100,
                   window_seconds: int = 60) -> bool:
        now = time.time()
        window_start = now - window_seconds

        pipe = self.redis.pipeline()
        pipe.zremrangebyscore(key, 0, window_start)
        pipe.zadd(key, {str(now): now})
        pipe.zcard(key)
        pipe.expire(key, window_seconds)
        results = pipe.execute()

        request_count = results[2]
        return request_count <= max_requests

    def check_rate_limit(self, request: Request,
                         max_requests: int = 100) -> None:
        # Rate limit por IP
        client_ip = request.client.host
        ip_key = f"ratelimit:ip:{client_ip}"

        if not self.is_allowed(ip_key, max_requests):
            retry_after = self._get_retry_after(ip_key)
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Demasiadas solicitudes. Intenta de nuevo.",
                headers={"Retry-After": str(retry_after)}
            )

    def check_user_rate_limit(self, user_id: str,
                               max_requests: int = 200) -> None:
        user_key = f"ratelimit:user:{user_id}"

        if not self.is_allowed(user_key, max_requests):
            retry_after = self._get_retry_after(user_key)
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Limite de solicitudes excedido.",
                headers={"Retry-After": str(retry_after)}
            )

    def _get_retry_after(self, key: str) -> int:
        ttl = self.redis.ttl(key)
        return max(ttl, 1)

rate_limiter = RateLimiter()
```

### 4.11 API Principal

```python
# main.py
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from models.schemas import (
    UserCreate, UserResponse, UserLogin, TokenResponse,
    ProductoCreate, ProductoResponse,
    CartItemAdd, CartResponse,
    OrderCreate, OrderResponse,
    MetricEvent
)
from services.user_service import UserService
from services.product_service import ProductService
from services.cart_service import CartService
from services.order_service import OrderService
from services.recommendation_service import RecommendationService
from services.metrics_service import MetricsService
from auth.jwt_handler import create_access_token, create_refresh_token, verify_token
from auth.middleware import get_current_user, require_admin
from middleware.rate_limiter import rate_limiter
from utils.database import db
from config import settings
import uuid

app = FastAPI(
    title="Multi-NoSQL E-commerce API",
    description="Sistema completo con MongoDB, Redis, Neo4j y Cassandra",
    version="1.0.0"
)

# Prometheus metrics
Instrumentator().instrument(app).expose(app)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Services
user_service = UserService()
product_service = ProductService()
cart_service = CartService()
order_service = OrderService()
recommendation_service = RecommendationService()
metrics_service = MetricsService()

@app.on_event("startup")
async def startup():
    pass

@app.on_event("shutdown")
async def shutdown():
    db.close()

# ===== AUTH ENDPOINTS =====

@app.post("/auth/register", response_model=UserResponse)
async def register(user: UserCreate):
    try:
        return user_service.crear_usuario(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/auth/login", response_model=TokenResponse)
async def login(credentials: UserLogin):
    user = user_service.autenticar(credentials.email, credentials.password)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    access_token = create_access_token(
        user["_id"], user["email"],
        user.get("role", "user")
    )
    refresh_token = create_refresh_token(user["_id"])

    metrics_service.registrar_evento("login", user["_id"])

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )

@app.post("/auth/refresh")
async def refresh_token(refresh_token: str):
    payload = verify_token(refresh_token)
    if payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Token invalido")

    new_access = create_access_token(
        payload["sub"], payload.get("email", ""), payload.get("role", "user")
    )
    return {"access_token": new_access, "token_type": "bearer"}

# ===== USER ENDPOINTS =====

@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: str,
                   user: dict = Depends(get_current_user)):
    rate_limiter.check_rate_limit_by_user(user["sub"])

    result = user_service.obtener_usuario(user_id)
    if not result:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return result

# ===== PRODUCT ENDPOINTS =====

@app.get("/products", response_model=list)
async def list_products(categoria: str = None,
                        skip: int = 0, limit: int = 20):
    return product_service.listar_productos(categoria, skip, limit)

@app.get("/products/search", response_model=list)
async def search_products(q: str):
    return product_service.buscar_productos(q)

@app.get("/products/{product_id}", response_model=ProductoResponse)
async def get_product(product_id: str):
    result = product_service.obtener_producto(product_id)
    if not result:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return result

@app.post("/products", response_model=ProductoResponse)
async def create_product(product: ProductoCreate,
                         user: dict = Depends(require_admin)):
    return product_service.crear_producto(product)

@app.put("/products/{product_id}", response_model=ProductoResponse)
async def update_product(product_id: str, updates: dict,
                         user: dict = Depends(require_admin)):
    result = product_service.actualizar_producto(product_id, updates)
    if not result:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return result

@app.delete("/products/{product_id}")
async def delete_product(product_id: str,
                         user: dict = Depends(require_admin)):
    if product_service.eliminar_producto(product_id):
        return {"message": "Producto eliminado"}
    raise HTTPException(status_code=404, detail="Producto no encontrado")

# ===== CART ENDPOINTS =====

@app.get("/cart/{user_id}", response_model=CartResponse)
async def get_cart(user_id: str,
                   user: dict = Depends(get_current_user)):
    return cart_service.obtener_carrito(user_id)

@app.post("/cart/{user_id}/add")
async def add_to_cart(user_id: str, item: CartItemAdd,
                      user: dict = Depends(get_current_user)):
    product = product_service.obtener_producto(item.producto_id)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    return cart_service.agregar_item(
        user_id, item.producto_id,
        item.cantidad, product.precio, product.nombre
    )

@app.delete("/cart/{user_id}/item/{product_id}")
async def remove_from_cart(user_id: str, product_id: str,
                           user: dict = Depends(get_current_user)):
    return cart_service.eliminar_item(user_id, product_id)

# ===== ORDER ENDPOINTS =====

@app.post("/orders", response_model=OrderResponse)
async def create_order(order: OrderCreate,
                       user: dict = Depends(get_current_user)):
    try:
        return order_service.crear_pedido(user["sub"], order)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/orders/{order_id}", response_model=OrderResponse)
async def get_order(order_id: str,
                    user: dict = Depends(get_current_user)):
    result = order_service.obtener_pedido(order_id)
    if not result:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return result

@app.get("/orders/user/{user_id}", response_model=list)
async def get_user_orders(user_id: str,
                          user: dict = Depends(get_current_user)):
    return order_service.pedidos_usuario(user_id)

# ===== RECOMMENDATION ENDPOINTS =====

@app.get("/recommendations/{user_id}")
async def get_recommendations(user_id: str, limit: int = 5):
    return recommendation_service.obtener_recomendaciones(user_id, limit)

@app.get("/recommendations/{user_id}/similar-users")
async def get_similar_users(user_id: str, limit: int = 5):
    return recommendation_service.usuarios_similares(user_id, limit)

@app.get("/recommendations/product/{product_id}/bought-together")
async def get_bought_together(product_id: str, limit: int = 5):
    return recommendation_service.productos_comprados_juntos(product_id, limit)

# ===== METRICS ENDPOINTS =====

@app.post("/metrics/event")
async def track_event(event: MetricEvent):
    metrics_service.registrar_evento(
        event.event_name, event.value, event.source
    )
    return {"message": "Evento registrado"}

@app.get("/metrics/{metric_name}")
async def get_metrics(metric_name: str, horas: int = 24):
    return metrics_service.obtener_metricas(metric_name, horas)

@app.get("/metrics/dashboard")
async def get_dashboard():
    return metrics_service.dashboard_metricas()

# ===== HEALTH CHECK =====

@app.get("/health")
async def health_check():
    health = {"status": "ok", "services": {}}

    # MongoDB
    try:
        db.mongo_client.admin.command("ping")
        health["services"]["mongodb"] = "ok"
    except Exception:
        health["services"]["mongodb"] = "error"
        health["status"] = "degraded"

    # Redis
    try:
        db.redis_client.ping()
        health["services"]["redis"] = "ok"
    except Exception:
        health["services"]["redis"] = "error"
        health["status"] = "degraded"

    # Neo4j
    try:
        with db.neo4j_driver.session() as session:
            session.run("RETURN 1")
        health["services"]["neo4j"] = "ok"
    except Exception:
        health["services"]["neo4j"] = "error"
        health["status"] = "degraded"

    # Cassandra
    try:
        db.cassandra_session.execute("SELECT now() FROM system.local")
        health["services"]["cassandra"] = "ok"
    except Exception:
        health["services"]["cassandra"] = "error"
        health["status"] = "degraded"

    return health
```

### 4.12 Pydantic Schemas

```python
# models/schemas.py
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

class UserCreate(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    nombre: str
    email: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class ProductoCreate(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=200)
    descripcion: Optional[str] = None
    precio: float = Field(..., gt=0)
    categoria: str
    stock: int = Field(default=0, ge=0)
    fotos: List[str] = []
    especificaciones: Optional[dict] = None

class ProductoResponse(BaseModel):
    id: str
    nombre: str
    descripcion: Optional[str] = None
    precio: float
    categoria: str
    stock: int = 0
    fotos: List[str] = []
    especificaciones: Optional[dict] = None

class CartItemAdd(BaseModel):
    producto_id: str
    cantidad: int = Field(..., gt=0, le=100)

class CartItem(BaseModel):
    producto_id: str
    nombre: str
    cantidad: int
    precio_unitario: float
    subtotal: float

class CartResponse(BaseModel):
    user_id: str
    items: List[CartItem]
    total_items: int
    total: float
    ttl: int

class OrderCreate(BaseModel):
    direccion_envio: dict
    metodo_pago: str = Field(..., pattern="^(tarjeta|paypal|transferencia)$")

class OrderResponse(BaseModel):
    id: str
    usuario_id: str
    items: List[dict]
    total: float
    estado: str
    fecha: Optional[str] = None

class MetricEvent(BaseModel):
    event_name: str
    value: str
    source: str = "api"
```

---

## 5. Seguridad del Sistema

### 5.1 JWT Authentication Flow

```mermaid
sequenceDiagram
    participant C as Cliente
    participant API as API
    participant R as Redis
    participant M as MongoDB

    C->>API: POST /auth/login {email, password}
    API->>M: Buscar usuario por email
    M-->>API: Usuario con password_hash
    API->>API: Verificar password con bcrypt
    API->>API: Generar JWT access_token
    API->>API: Generar JWT refresh_token
    API->>R: Guardar refresh_token con TTL
    API-->>C: {access_token, refresh_token}

    C->>API: GET /products (con Authorization: Bearer token)
    API->>API: Verificar JWT signature
    API->>API: Verificar expiry
    API->>API: Extraer user_id y role
    API->>API: Verificar permisos (RBAC)
    API-->>C: Lista de productos
```

### 5.2 RBAC — Roles y Permisos

```mermaid
graph TB
    subgraph "Roles"
        ADMIN[Admin]
        USER[User]
        VENDOR[Vendor]
    end

    subgraph "Permisos"
        P1[users:read]
        P2[users:write]
        P3[users:delete]
        P4[products:read]
        P5[products:write]
        P6[products:delete]
        P7[orders:read]
        P8[orders:write]
        P9[metrics:read]
        P10[inventory:write]
    end

    ADMIN --> P1
    ADMIN --> P2
    ADMIN --> P3
    ADMIN --> P4
    ADMIN --> P5
    ADMIN --> P6
    ADMIN --> P7
    ADMIN --> P8
    ADMIN --> P9
    ADMIN --> P10

    USER --> P1
    USER --> P4
    USER --> P7
    USER --> P8

    VENDOR --> P4
    VENDOR --> P5
    VENDOR --> P7
    VENDOR --> P9
    VENDOR --> P10
```

### 5.3 Input Validation — Prevencion de Inyeccion

```python
# middleware/security.py
import re
from fastapi import HTTPException

class InputSanitizer:

    NOSQL_INJECTION_PATTERNS = [
        r'\$where',
        r'\$regex',
        r'\$gt',
        r'\$lt',
        r'\$ne',
        r'\$in',
        r'\$nin',
        r'\$exists',
        r'\$and',
        r'\$or',
        r'\$not',
        r'\$nor',
        r'function\s*\(',
        r'eval\s*\(',
    ]

    CYPHER_INJECTION_PATTERNS = [
        r'CREATE\s+',
        r'DELETE\s+',
        r'MATCH\s+.*\bDETACH\b',
        r'DROP\s+',
        r'CALL\s+apoc',
        r'LOAD\s+CSV',
    ]

    @staticmethod
    def sanitize_string(value: str) -> str:
        if not isinstance(value, str):
            return value

        # Remove potential NoSQL injection characters
        value = re.sub(r'[{}]', '', value)
        value = re.sub(r'\$', '', value)

        # Basic XSS prevention
        value = value.replace('<', '&lt;').replace('>', '&gt;')
        value = value.replace('"', '&quot;')

        return value.strip()

    @staticmethod
    def validate_object(data: dict) -> dict:
        if not isinstance(data, dict):
            return data

        sanitized = {}
        for key, value in data.items():
            key = InputSanitizer.sanitize_string(str(key))

            if isinstance(value, str):
                # Check for NoSQL injection
                for pattern in InputSanitizer.NOSQL_INJECTION_PATTERNS:
                    if re.search(pattern, value, re.IGNORECASE):
                        raise HTTPException(
                            status_code=400,
                            detail="Entrada no valida detectada"
                        )
                value = InputSanitizer.sanitize_string(value)
            elif isinstance(value, dict):
                value = InputSanitizer.validate_object(value)
            elif isinstance(value, list):
                value = [
                    InputSanitizer.validate_object(item)
                    if isinstance(item, dict)
                    else InputSanitizer.sanitize_string(str(item))
                    if isinstance(item, str)
                    else item
                    for item in value
                ]

            sanitized[key] = value

        return sanitized

    @staticmethod
    def validate_cypher_input(value: str) -> str:
        for pattern in InputSanitizer.CYPHER_INJECTION_PATTERNS:
            if re.search(pattern, value, re.IGNORECASE):
                raise HTTPException(
                    status_code=400,
                    detail="Entrada no valida para consulta"
                )
        return value
```

### 5.4 CORS Configuration

```python
# En main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "https://mi-tienda.com",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["Authorization", "Content-Type"],
    expose_headers=["X-Total-Count", "Retry-After"],
    max_age=600,
)
```

---

## 6. Monitoreo y Observabilidad

### 6.1 Health Checks

```mermaid
graph TB
    subgraph "Health Check Endpoints"
        HC[/health<br/>GET]
    end

    subgraph "Checks"
        HC --> M1{MongoDB OK?}
        HC --> M2{Redis OK?}
        HC --> M3{Neo4j OK?}
        HC --> M4{Cassandra OK?}
    end

    M1 -->|OK| S1[status: ok]
    M1 -->|ERROR| S2[status: degraded]
    M2 -->|OK| S1
    M2 -->|ERROR| S2
    M3 -->|OK| S1
    M3 -->|ERROR| S2
    M4 -->|OK| S1
    M4 -->|ERROR| S2
```

### 6.2 Prometheus Configuration

```yaml
# config/prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'api-service'
    static_configs:
      - targets: ['api:8000']
    metrics_path: '/metrics'

  - job_name: 'redis'
    static_configs:
      - targets: ['redis:6379']

  - job_name: 'mongodb'
    static_configs:
      - targets: ['mongodb:27017']

  - job_name: 'neo4j'
    static_configs:
      - targets: ['neo4j:7474']

  - job_name: 'cassandra'
    static_configs:
      - targets: ['cassandra:9042']
```

### 6.3 Metricas por Endpoint

| Endpoint | Metrica | Tipo |
|---|---|---|
| /products | requests_total | Counter |
| /products | request_duration_seconds | Histogram |
| /orders | orders_created_total | Counter |
| /orders | order_value | Summary |
| /cart | cart_operations_total | Counter |
| /auth | login_attempts_total | Counter |
| /auth | login_failures_total | Counter |

---

## 7. Estrategia de Backup

### 7.1 Script de Backup Completo

```bash
#!/bin/bash
# scripts/backup_all.sh — Backup completo de todas las BD

BACKUP_DIR="/backups"
DATE=$(date +%Y%m%d_%H%M%S)
LOG_FILE="$BACKUP_DIR/backup_$DATE.log"
RETENTION_DAYS=30

mkdir -p "$BACKUP_DIR"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "=== Inicio de Backup Completo ==="

# ===== MongoDB =====
log "Backup MongoDB..."
docker exec mongodb mongodump \
    -u admin -p admin123 --authenticationDatabase admin \
    --db tienda \
    --out /tmp/backup_$DATE
docker cp mongodb:/tmp/backup_$DATE "$BACKUP_DIR/mongodb_$DATE"
log "MongoDB backup completado"

# ===== Redis =====
log "Backup Redis..."
docker exec redis redis-cli -a admin123 BGSAVE
sleep 5
docker cp redis:/data/dump.rdb "$BACKUP_DIR/redis_$DATE.rdb"
log "Redis backup completado"

# ===== Neo4j =====
log "Backup Neo4j..."
docker exec neo4j neo4j-admin database dump neo4j \
    --to-path=/tmp/neo4j_backup_$DATE
docker cp neo4j:/tmp/neo4j_backup_$DATE "$BACKUP_DIR/neo4j_$DATE"
log "Neo4j backup completado"

# ===== Cassandra =====
log "Backup Cassandra..."
docker exec cassandra nodetool snapshot -t backup_$DATE tienda
docker cp cassandra:/var/lib/cassandra/data/tienda/backup_$DATE \
    "$BACKUP_DIR/cassandra_$DATE"
log "Cassandra backup completado"

# ===== Limpiar backups antiguos =====
log "Limpiando backups antiguos (>$RETENTION_DAYS dias)..."
find "$BACKUP_DIR" -maxdepth 1 -name "*_$(date +%Y%m%d)*" -mtime +$RETENTION_DAYS -exec rm -rf {} +
find "$BACKUP_DIR" -maxdepth 1 -type f -mtime +$RETENTION_DAYS -delete

# ===== Verificar integridad =====
log "Verificando integridad de backups..."
TOTAL_SIZE=$(du -sh "$BACKUP_DIR" | awk '{print $1}')
BACKUP_COUNT=$(find "$BACKUP_DIR" -name "*$DATE*" | wc -l)
log "Total backups creados: $BACKUP_COUNT"
log "Tamano total: $TOTAL_SIZE"

log "=== Backup Completo Finalizado ==="
```

### 7.2 Política de Retencion

| BD | Frecuencia | Retencion | Metodo |
|---|---|---|---|
| MongoDB | Diario | 30 dias | mongodump |
| Redis | Cada 6 horas | 7 dias | BGSAVE + AOF |
| Neo4j | Diario | 30 dias | neo4j-admin dump |
| Cassandra | Semanal | 90 dias | nodetool snapshot |

### 7.3 Cron Jobs

```bash
# Backup diario a las 2:00 AM
0 2 * * * /opt/scripts/backup_all.sh >> /var/log/backup.log 2>&1

# Backup Redis cada 6 horas
0 */6 * * * /opt/scripts/backup_redis.sh >> /var/log/backup.log 2>&1

# Limpieza de logs antiguos (primer domingo de cada mes)
0 4 * * 0 find /var/log -name "*.log" -mtime +90 -delete
```

---

## 8. Despliegue y Pruebas

### 8.1 Docker Compose Up

```bash
# Clonar e iniciar
git clone https://github.com/tienda-multi-nosql.git
cd tienda-multi-nosql

# Inicializar bases de datos
docker-compose up -d mongodb redis neo4j cassandra
sleep 60

# Ejecutar scripts de inicializacion
docker exec -i mongodb mongosh -u admin -p admin123 --authenticationDatabase admin tienda < scripts/init_mongo.js
bash scripts/init_redis.sh
docker exec -i neo4j cypher-shell -u neo4j -p admin123 < scripts/init_neo4j.cypher
docker exec -i cassandra cqlsh < scripts/init_cassandra.cql

# Iniciar API
docker-compose up -d api

# Verificar health
curl http://localhost:8000/health
```

**Salida esperada:**

```json
{
    "status": "ok",
    "services": {
        "mongodb": "ok",
        "redis": "ok",
        "neo4j": "ok",
        "cassandra": "ok"
    }
}
```

### 8.2 Pruebas de Carga

```bash
# Instalar wrk
# Ubuntu: sudo apt install wrk
# Mac: brew install wrk

# Test de carga en productos (lectura con cache)
wrk -t4 -c100 -d30s --latency \
    http://localhost:8000/products

# Test de carga en login
wrk -t4 -c50 -d30s --latency \
    -s scripts/login_bench.lua \
    http://localhost:8000/auth/login

# Apache Bench
ab -n 10000 -c 100 http://localhost:8000/products
```

**Script Lua para wrk (login benchmark):**

```lua
-- scripts/login_bench.lua
wrk.method = "POST"
wrk.headers["Content-Type"] = "application/json"

counter = 0

function request()
    counter = counter + 1
    local body = string.format(
        '{"email":"user%d@test.com","password":"testpass123"}',
        counter % 1000
    )
    return wrk.format(nil, "/auth/login", nil, body)
end
```

**Resultados esperados:**

```
=== Benchmark: GET /products ===
Running 30s test @ http://localhost:8000/products
  4 threads and 100 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    12.34ms    5.67ms  45.23ms   68.42%
    Req/Sec     2.12k    156.34    2.45k     72.00%
  Latency Distribution
     50%   10.12ms
     75%   14.56ms
     90%   20.34ms
     99%   35.67ms
  252,456 requests in 30.01s, 52.34MB read
Requests/sec:   8,412.34
Transfer/sec:      1.74MB

=== Benchmark: POST /auth/login ===
Running 30s test @ http://localhost:8000/auth/login
  4 threads and 50 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    25.67ms   12.34ms  89.45ms   62.34%
    Req/Sec    0.49k     45.67    0.65k     65.00%
  58,234 requests in 30.01s, 12.45MB read
Requests/sec:   1,940.56
Transfer/sec:    421.67KB
```

### 8.3 Simular Fallos y Recuperacion

```bash
# Simular caida de MongoDB
docker stop mongodb
sleep 5
curl http://localhost:8000/health
# -> {"status": "degraded", "services": {"mongodb": "error", ...}}

# Verificar que Redis sigue respondiendo
curl http://localhost:8000/cart/user123
# -> Respuesta normal (Redis no depende de MongoDB)

# Verificar que Neo4j sigue respondiendo
curl http://localhost:8000/recommendations/u1
# -> Respuesta normal

# Recuperar MongoDB
docker start mongodb
sleep 30
curl http://localhost:8000/health
# -> {"status": "ok", "services": {"mongodb": "ok", ...}}
```

---

## 9. Criterios de Evaluacion del Proyecto

### 9.1 Distribucion de Puntos

| Categoria | Porcentaje | Descripcion |
|---|---|---|
| **Funcionalidad** | 40% | Todos los endpoints funcionan, CRUD completo, autenticacion JWT |
| **Arquitectura** | 20% | Uso correcto de cada BD, patrones de diseno, separacion de responsabilidades |
| **Seguridad** | 20% | JWT + RBAC, rate limiting, input validation, prevencion de inyeccion |
| **Administracion** | 10% | Backups configurados, monitoreo activo, scripts de mantenimiento |
| **Documentacion** | 10% | README completo, diagrama de arquitectura, instrucciones de setup |

### 9.2 Checklist de Funcionalidad (40%)

- [ ] Registro de usuario con hash de password
- [ ] Login con JWT access y refresh tokens
- [ ] CRUD de productos (admin puede crear/editar/eliminar, usuario solo leer)
- [ ] Busqueda de productos con cache en Redis
- [ ] Carrito de compras en Redis con TTL
- [ ] Creacion de pedido que reduce stock
- [ ] Historial de pedidos del usuario
- [ ] Recomendaciones basadas en grafo (Neo4j)
- [ ] Metricas de uso (Cassandra)
- [ ] Health check de todas las bases de datos

### 9.3 Checklist de Arquitectura (20%)

- [ ] MongoDB para usuarios, productos y pedidos
- [ ] Redis para cache, sesiones y carrito
- [ ] Neo4j para recomendaciones y relaciones
- [ ] Cassandra para metricas y logs temporales
- [ ] Patron Database per Service implementado
- [ ] Patron CQRS o Cache-Aside para lecturas
- [ ] Patron Event Sourcing o CDC para sincronizacion
- [ ] Docker Compose con todas las bases de datos

### 9.4 Checklist de Seguridad (20%)

- [ ] JWT con expiracion configurable
- [ ] Refresh tokens
- [ ] RBAC con al menos 3 roles (admin, user, vendor)
- [ ] Rate limiting por IP
- [ ] Rate limiting por usuario
- [ ] Input validation en todos los endpoints
- [ ] Prevencion de NoSQL injection
- [ ] Prevencion de Cypher injection
- [ ] CORS configurado correctamente
- [ ] Passwords hasheados con bcrypt

### 9.5 Checklist de Administracion (10%)

- [ ] Backup automatizado de MongoDB
- [ ] Backup automatizado de Redis
- [ ] Backup automatizado de Neo4j
- [ ] Backup automatizado de Cassandra
- [ ] Prometheus con metricas del API
- [ ] Grafana con dashboard (al menos 3 paneles)
- [ ] Politica de retencion de backups
- [ ] Script de restore probado

### 9.6 Checklist de Documentacion (10%)

- [ ] README con instrucciones de setup
- [ ] Diagrama de arquitectura (mermaid)
- [ ] Diagrama de datos (ER)
- [ ] Lista de endpoints (API docs)
- [ ] Justificacion de BD por componente
- [ ] Benchmark de rendimiento documentado
- [ ] Instrucciones de pruebas de carga

---

## Resumen del Proyecto

| Componente | Tecnologia | Justificacion |
|---|---|---|
| **Usuarios/Productos/Pedidos** | MongoDB | Documentos flexibles, busqueda textual |
| **Cache/Sesiones/Carrito** | Redis | Velocidad extrema, TTL nativo |
| **Recomendaciones** | Neo4j | Relaciones complejas, traversals de grafo |
| **Metricas/Logs** | Cassandra | Escritura masiva, time-series con TTL |
| **Autenticacion** | JWT + Redis | Stateless, tokens en cache |
| **Monitoreo** | Prometheus + Grafana | Estandar de la industria |
| **Orquestacion** | Docker Compose | Despliegue completo local |

---

## Tarea Final

1. Clonar o crear el proyecto con la estructura documentada
2. Implementar todos los endpoints listados
3. Configurar todas las bases de datos con datos iniciales
4. Implementar autenticacion JWT completa con RBAC
5. Implementar rate limiting por IP y por usuario
6. Implementar input validation contra inyecciones
7. Configurar health checks para cada base de datos
8. Configurar Prometheus y Grafana
9. Crear script de backup completo
10. Ejecutar pruebas de carga y documentar resultados
11. Presentar demo en vivo del sistema funcionando
12. Documentar todo en README con diagramas
