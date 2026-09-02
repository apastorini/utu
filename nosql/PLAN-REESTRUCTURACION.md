# Plan de Reestructuración — Curso NoSQL

## Objetivo

Reestructurar el curso de 11 clases a **18 clases** donde cada clase sea un **profundización completa** en una tecnología NoSQL, con marco teórico, instalación paso a paso, arquitectura, CRUD, administración, seguridad, backups, replicas y sharding.

## Estructura Actual vs Nueva

### Estructura Actual (11 clases — poco profunda)
```
Clase 01: SQL vs NoSQL (teórico + MongoDB básico)
Clase 02: ACID, CAP (teórico)
Clase 03: Normalización (teórico)
Clase 04: Indexación (teórico)
Clase 05: WAL y Bloom Filters (teórico)
Clase 06: MongoDB avanzado
Clase 07: MongoDB replicación
Clase 08: Sharding
Clase 09: Redis
Clase 10: Cassandra
Clase 11: Neo4j
```

### Nueva Estructura (18 clases — profunda y completa)

```
MÓDULO 0 — Fundamentos (1 clase)
├── Clase 01: Introducción a NoSQL y Categorías

MÓDULO 1 — MongoDB: Base de Datos Documental (4 clases)
├── Clase 02: MongoDB I — Fundamentos, Instalación y CRUD
├── Clase 03: MongoDB II — Consultas Avanzadas y Aggregation
├── Clase 04: MongoDB III — Replicación y Alta Disponibilidad
├── Clase 05: MongoDB IV — Sharding, Administración y Seguridad

MÓDULO 2 — Redis: Almacenamiento Clave-Valor (3 clases)
├── Clase 06: Redis I — Fundamentos, Tipos de Datos y Persistencia
├── Clase 07: Redis II — Caché, Patrones y Pub/Sub
├── Clase 08: Redis III — Replicación, Clustering y Seguridad

MÓDULO 3 — Cassandra: Base de Datos Columnar (3 clases)
├── Clase 09: Cassandra I — Fundamentos, Arquitectura y CQL
├── Clase 10: Cassandra II — Consistencia, Compaction y Escalamiento
├── Clase 11: Cassandra III — Administración, Backups y Seguridad

MÓDULO 4 — Neo4j: Base de Datos de Grafos (3 clases)
├── Clase 12: Neo4j I — Fundamentos, Cypher y Modelo de Grafos
├── Clase 13: Neo4j II — Algoritmos de Grafos y Recomendaciones
├── Clase 14: Neo4j III — Administración, Backups y Seguridad

MÓDULO 5 — ObjectDB: Base de Datos Orientada a Objetos (2 clases)
├── Clase 15: ObjectDB I — Fundamentos, JPA y Modelo de Objetos
├── Clase 16: ObjectDB II — Clustering, Administración y Seguridad

MÓDULO 6 — Integración y Patrones Avanzados (2 clases)
├── Clase 17: Patrones Multi-Base de Datos y Polyglot Persistence
├── Clase 18: Proyecto Final — Sistema Completo Multi-NoSQL
```

## Detalle de Cada Clase

---

### CLASE 01 — Introducción a NoSQL y Categorías

**Marco Teórico:**
- ¿Qué es NoSQL? Origen y evolución
- Las 4 categorías + ObjectDB:
  1. **Documental** (MongoDB, CouchDB, Firestore)
  2. **Clave-Valor** (Redis, DynamoDB, Memcached)
  3. **Columnar** (Cassandra, HBase, ScyllaDB)
  4. **Grafo** (Neo4j, ArangoDB, Neptune)
  5. **Orientado a Objetos** (ObjectDB, db4o, Versant)
- Teorema CAP (Consistencia, Disponibilidad, Tolerancia a Particiones)
- Propiedades ACID vs BASE
- Consistencia fuerte vs eventual
- Cuándo usar cada categoría (tabla comparativa completa)
- Casos de uso reales por categoría

**Instalación General:**
- Docker Desktop (Windows/Linux/macOS)
- Preparación del entorno para todas las BD

**Contenido:**
```markdown
## Estructura de la Clase

1. **Marco Teórico General**
   - Historia de las bases de datos: de jerárquicas a NoSQL
   - El problema de la escalabilidad vertical
   - El movimiento NoSQL (2009+)
   - Polyglot persistence: usar la BD correcta para cada problema

2. **Las 5 Categorías de NoSQL**
   - Tabla comparativa completa
   - Diagrama de decisión: ¿Cuál uso?
   - Ejemplo de uso real de cada una

3. **Teorema CAP (detallado)**
   - Definición formal
   - Diagrama de Venn
   - Clasificación de cada BD
   - Tradeoffs prácticos

4. **ACID vs BASE**
   - Propiedades ACID con ejemplos
   - Modelo BASE (Basically Available, Soft state, Eventual consistency)
   - Cuándo elegir ACID vs BASE

5. **Consistencia en Sistemas Distribuidos**
   - Consistencia fuerte
   - Consistencia eventual
   - Consistencia causal
   - Consistencia de sesión
   - Consistencia monotónica

6. **Instalación del Entorno**
   - Docker Desktop
   - Verificación de Docker
   - Estructura de directorios del curso

7. **Ejercicio Práctico**
   - Levantar una instancia de cada BD con Docker
   - Realizar una operación básica en cada una
   - Comparar tiempos de respuesta
```

---

### CLASE 02 — MongoDB I: Fundamentos, Instalación y CRUD

**Marco Teórico:**
- ¿Qué es MongoDB? Filosofía y diseño
- Modelo de datos: documentos BSON, colecciones, bases de datos
- Arquitectura: WiredTiger engine, almacenamiento en disco
- Comparación con bases relacionales

**Instalación Paso a Paso:**
- Windows: MSI, configuración del servicio
- Linux (Ubuntu/Debian): repositorio oficial
- macOS: Homebrew
- Docker: multiplataforma
- Archivo de configuración mongod.conf (explicado línea por línea)

**Arquitectura Detallada:**
```markdown
## Componentes de MongoDB

1. **mongod** — Servidor principal
   - Gestiona memoria, disco, red
   - Motor WiredTiger (B-Tree)
   - Journaling para durabilidad

2. **mongosh** — Shell interactivo

3. **MongoDB Compass** — GUI

4. **Drivers** — Python, Java, Node.js, etc.

## WiredTiger Engine
- Almacenamiento en documentos BSON
- Compresión (snappy, zlib)
- Checkpointing cada 60 segundos
- Journal (WAL) para recuperación

## Modelo de Datos
- Documento = JSON/BSON (max 16MB)
- Colección = grupo de documentos (similar a tabla)
- Base de datos = grupo de colecciones
```

**CRUD Completo:**
```markdown
## Operaciones CRUD

### Crear (Insert)
- insertOne()
- insertMany()
- bulkWrite()
- insert con validación de esquema

### Leer (Read)
- find() con filtros
- Operadores: $eq, $ne, $gt, $gte, $lt, $lte, $in, $nin
- Operadores lógicos: $and, $or, $not, $nor
- Proyección de campos
- sort(), limit(), skip()
- Contar y agrupar

### Actualizar (Update)
- updateOne(), updateMany()
- Operadores: $set, $unset, $inc, $mul, $rename
- Operadores de array: $push, $pull, $addToSet, $each
- Upsert
- replaceOne()

### Eliminar (Delete)
- deleteOne(), deleteMany()
- findOneAndDelete()
- Bulk write operations

### Aggregation Pipeline (introducción)
- $match, $group, $sort, $limit, $skip
- $project, $addFields
- $unwind
```

**Seguridad:**
```markdown
## Seguridad Básica

1. **Autenticación**
   - Crear usuario admin
   - Crear usuario de aplicación
   - Roles: read, readWrite, dbAdmin, userAdmin, root

2. **Autorización**
   - RBAC (Role-Based Access Control)
   - Roles predefinidos vs personalizados

3. **Red**
   - bindIp: solo escuchar en interfaces específicas
   - Puerto configurable
   - SSL/TLS para conexiones

4. **Cifrado**
   - Cifrado en reposo (encryption at rest)
   - Cifrado en tránsito (encryption in transit)
```

---

### CLASE 03 — MongoDB II: Consultas Avanzadas y Aggregation

**Marco Teórico:**
- Pipeline de agregación: concepto y flujo
- Etapas del pipeline y su orden
- Optimización de consultas
- Patrones de modelado avanzados

**Contenido:**
```markdown
## Aggregation Pipeline (Profundización)

1. **Etapas principales**
   - $match (filtrar — usar primero para reducir datos)
   - $group (agregar: $sum, $avg, $min, $max, $push, $addToSet)
   - $sort (ordenar)
   - $project (proyectar/renombrar campos)
   - $unwind (descomponer arrays)
   - $lookup (JOIN con otra colección)
   - $addFields (agregar campos calculados)
   - $out / $merge (guardar resultado)
   - $facet (múltiples pipelines en paralelo)
   - $bucket / $bucketAuto (agrupar por rangos)
   - $sample (muestreo aleatorio)
   - $graphLookup (búsqueda recursiva en grafos)

2. **Ejemplos completos**
   - Análisis de ventas por región y período
   - Top N productos por categoría
   - Estadísticas de usuario con $facet
   - Búsqueda recursiva de categorías con $graphLookup

3. **Optimización de Pipeline**
   - Regla: $match primero
   - Usar índices en $match y $sort
   - Evitar $unwind innecesario
   - Usar $limit antes de etapas costosas
   - explain("executionStats") para análisis

## Patrones de Modelado

1. **Patrón Bucket**
   - Agrupar datos por tiempo
   - Ejemplo: métricas por hora

2. **Patrón Polimórfico**
   - Documentos de diferentes estructuras en una colección
   - Campo "tipo" para diferenciar

3. **Patrón Schema Versioning**
   - Versionar esquemas para migraciones

4. **Patrón Extended Reference**
   - Embeber datos frecuentemente leídos
   - Referenciar datos que cambian poco

5. **Patrón Computed**
   - Pre-calcular valores derivados
```

---

### CLASE 04 — MongoDB III: Replicación y Alta Disponibilidad

**Marco Teórico:**
- ¿Qué es la replicación? ¿Por qué?
- Replica Sets: arquitectura primario-secundario
- Oplog: registro de operaciones
- Electores: elección de primario
- Consistencia en réplicas

**Instalación de Replica Set:**
- Configuración manual (3 nodos en localhost)
- Configuración con Docker Compose
- Inicialización y verificación

**Contenido:**
```markdown
## Replica Sets

1. **Arquitectura**
   - Primario: recibe escrituras
   - Secundario: replica datos, puede servir lecturas
   - Arbiter: vota pero no almacena datos

2. **Oplog (Operations Log)**
   - Colección especial local.oplog.rs
   - Registro de todas las escrituras
   - Los secundarios leen y aplican el oplog
   - Tamaño configurable (oplogSizeMB)

3. **Elección de Primario**
   - Necesita mayoría absoluta (>50%)
   - El nodo con oplog más reciente tiene prioridad
   - Configuración de prioridades
   - Step down manual

4. **Read Preferences**
   - primary (default)
   - primaryPreferred
   - secondary
   - secondaryPreferred
   - nearest

5. **Write Concern**
   - w: 1 (default — solo primario)
   - w: "majority" (mayoría de nodos)
   - w: 0 (fire and forget)
   - j: true (esperar journal)

6. **Read Concern**
   - local (default)
   - majority (datos confirmados por mayoría)
   - linearizable (consistencia total)
   - available (más rápido, menos consistente)

## Simulación de Fallos

1. Matar el primario
2. Observar elección del nuevo primario
3. Medir tiempo de failover
4. Reincorporar nodo caído
5. Verificar sincronización del oplog

## Backups en MongoDB

1. **mongodump** — backup lógico
2. **mongorestore** — restauración
3. **File System Snapshots** — backup físico
4. **Atlas Backup** (mencionar)
5. **Automatización con scripts**
```

---

### CLASE 05 — MongoDB IV: Sharding, Administración y Seguridad

**Marco Teórico:**
- ¿Qué es el sharding? ¿Por qué?
- Particionamiento vs sharding
- Consistent Hashing (teoría completa)
- Arquitectura de cluster shardado
- Mongos, Config Servers, Shard Servers

**Instalación de Cluster Shardado:**
- Docker Compose completo
- Inicialización paso a paso
- Verificación de distribución

**Contenido:**
```markdown
## Sharding en MongoDB

1. **Arquitectura**
   - mongos (router)
   - Config Servers (metadatos)
   - Shard Servers (datos — cada uno es un replica set)

2. **Clave de Shard**
   - Ranged Sharding
   - Hashed Sharding
   - Tagged Sharding
   - Elegir la clave correcta

3. **Balancing**
   - Migración automática de chunks
   - Configurar ventana de balancing
   - Monitorear migraciones

4. **Consistent Hashing**
   - Problema del hashing simple
   - Anillo de hash
   - Implementación en Python
   - Simulación de agregar/quitar nodos

## Administración de MongoDB

1. **Monitoreo**
   - db.serverStatus()
   - db.stats()
   - mongostat
   - mongotop
   - MongoDB Atlas (mencionar)

2. **Mantenimiento**
   - Compactación de colecciones
   - Reindexación
   - Limpieza de datos antiguos
   - Rotación de logs

3. **Performance Tuning**
   - Análisis de explain()
   - Índices: creación, análisis, eliminación
   - Profiler de consultas
   - Optimización de aggregation pipeline

## Seguridad Completa de MongoDB

1. **Autenticación y Autorización**
   - SCRAM-SHA-256
   - LDAP (enterprise)
   - X.509 certificates
   - Roles personalizados

2. **Cifrado**
   - Encryption at rest (WiredTiger)
   - Encryption in transit (SSL/TLS)
   - Client-Side Field Level Encryption

3. **Red**
   - bindIp restriction
   - Firewall rules
   - VPN para acceso

4. **Auditoría**
   - Audit log
   - Eventos de seguridad

5. **Hardening**
   - Deshabilitar script engine
   - Restringir commandos peligrosos
   - NoSQL injection prevention

6. **Backup Security**
   - Cifrar backups
   - Almacenamiento seguro
   - Restauración verificada
```

---

### CLASE 06 — Redis I: Fundamentos, Tipos de Datos y Persistencia

**Marco Teórico:**
- ¿Qué es Redis? Origen y filosofía
- Modelo de datos clave-valor
- Arquitectura single-threaded + I/O multiplexing
- Memoria vs disco: ¿por qué es tan rápido?
- Persistencia: RDB vs AOF

**Instalación:**
- Windows (WSL2 recomendado)
- Linux (Ubuntu/Debian)
- macOS (Homebrew)
- Docker

**Contenido:**
```markdown
## Arquitectura de Redis

1. **Single-Threaded Model**
   - Un hilo para comandos
   - I/O multiplexing (epoll/kqueue)
   - Sin overhead de concurrencia

2. **Memoria**
   - Todos los datos en RAM
   - Estructuras de datos optimizadas
   - O(1) para la mayoría de operaciones

3. **Persistencia**
   - RDB (snapshots)
   - AOF (Append Only File)
   - Híbrido (RDB + AOF)

## Tipos de Datos Completos

1. **Strings**
   - SET, GET, MSET, MGET
   - INCR, DECR, INCRBY
   - SETEX, PSETEX, SETNX
   - APPEND, STRLEN
   - GETRANGE, SETRANGE

2. **Hashes**
   - HSET, HGET, HMSET, HMGET
   - HGETALL, HKEYS, HVALS
   - HINCRBY, HDEL
   - HEXISTS

3. **Lists**
   - LPUSH, RPUSH, LPOP, RPOP
   - LRANGE, LLEN, LINDEX
   - LINSERT, LSET
   - BLPOP, BRPOP (blocking)
   - LREM

4. **Sets**
   - SADD, SREM, SMEMBERS
   - SINTER, SUNION, SDIFF
   - SRANDMEMBER, SPOP
   - SCARD, SISMEMBER

5. **Sorted Sets**
   - ZADD, ZREM, ZRANGE, ZREVRANGE
   - ZRANGEBYSCORE, ZREVRANGEBYSCORE
   - ZRANK, ZREVRANK
   - ZSCORE, ZINCRBY
   - ZCARD, ZCOUNT

6. **Bitmaps**
   - SETBIT, GETBIT
   - BITCOUNT, BITOP

7. **HyperLogLog**
   - PFADD, PFCOUNT, PFMERGE

8. **Streams (Redis 5+)**
   - XADD, XRANGE, XREAD
   - Consumer Groups
   - XACK, XPENDING

## Persistencia Detallada

1. **RDB**
   - Snapshot periódico
   - fork() para no bloquear
   - Ventajas: backup rápido, restore rápido
   - Desventajas: pérdida de datos entre snapshots

2. **AOF**
   - Cada escritura se registra
   - appendfsync: always, everysec, no
   - Reescritura automática del AOF
   - Ventajas: mejor durabilidad
   - Desventajas: archivo más grande, restore más lento

3. **Híbrido**
   - RDB + AOF (Redis 4+)
   - Mejor de ambos mundos
```

---

### CLASE 07 — Redis II: Caché, Patrones y Pub/Sub

**Marco Teórico:**
- Patrones de caché: Cache-Aside, Write-Through, Write-Behind
- Evicción: LRU, LFU, TTL
- Materialized Views con Redis
- Pub/Sub y Message Brokers

**Contenido:**
```markdown
## Patrones de Caché

1. **Cache-Aside (Lazy Loading)**
   - Flujo completo con diagrama
   - Código en Python
   - Cuando usar

2. **Write-Through**
   - Flujo completo
   - Código en Python
   - Ventajas/desventajas

3. **Write-Behind (Write-Back)**
   - Cola de escrituras
   - Batch processing
   - Código en Python

## Evicción y TTL

1. **Políticas de evicción**
   - allkeys-lru
   - volatile-lru
   - allkeys-lfu
   - volatile-lfu
   - allkeys-random
   - volatile-ttl
   - noeviction

2. **TTL en práctica**
   - EXPIRE, PEXPIRE
   - TTL, PTTL
   - PERSIST (quitar TTL)
   - SET con EX/PX

## Materialized Views con Redis

1. **Concepto**
   - Precomputed results
   - Actualización en tiempo real
   - Lecturas O(1)

2. **Implementación**
   - Dashboard de ventas
   - Top productos
   - Contadores en tiempo real

## Pub/Sub

1. **Redis Pub/Sub**
   - SUBSCRIBE, PUBLISH
   - PATTERNS (suscripción por patrón)
   - Limitaciones (no persiste mensajes)

2. **Redis Streams (mejor alternativa)**
   - Consumer Groups
   - Persistencia de mensajes
   - XACK para confirmar procesamiento

## Casos de Uso

1. **Session Store**
2. **Rate Limiting**
3. **Leaderboards**
4. **Real-time Analytics**
5. **Message Queue**
6. **Distributed Lock**
```

---

### CLASE 08 — Redis III: Replicación, Clustering y Seguridad

**Marco Teórico:**
- Replicación maestro-esclavo
- Redis Cluster: sharding automático
- Sentinel: alta disponibilidad

**Instalación de Cluster:**
- Redis Cluster con Docker
- Configuración de 6 nodos (3 maestros + 3 esclavos)

**Contenido:**
```markdown
## Replicación en Redis

1. **Master-Slave**
   - Configuración
   - Replicación asíncrona
   - Partial Resynchronization

2. **Redis Sentinel**
   - Monitoreo automático
   - Failover automático
   - Configuración de 3 sentinels

3. **Redis Cluster**
   - 16384 slots
   - Distribución automática
   - Migración de slots

## Administración de Redis

1. **Monitoreo**
   - INFO command
   - redis-cli --latency
   - MEMORY USAGE
   - SLOWLOG

2. **Mantenimiento**
   - MEMORY DOCTOR
   - MEMORY PURGE
   - BGSAVE
   - LASTSAVE

3. **Performance Tuning**
   - Pipeline (multiplexing)
   - Lua scripts
   - Large key detection
   - Hot key detection

## Seguridad de Redis

1. **Autenticación**
   - requirepass (legacy)
   - ACL (Redis 6+)
   - Users y passwords
   - Comandos por usuario

2. **Red**
   - bind configuration
   - protected-mode
   - TLS/SSL

3. **Comandos peligrosos**
   - DESHABILITAR: FLUSHALL, FLUSHDB
   - RENAME-COMMAND
   - Prohibir CONFIG SET

4. **Cifrado**
   - TLS para conexiones
   - Cifrado en reposo (enterprise)

5. **Backups**
   - RDB snapshot
   - AOF backup
   - Script de backup automatizado

## Clustering Completo

1. **Crear cluster con docker-compose**
2. **Agregar/quitar nodos**
3. **Balancear slots**
4. **Simular fallos**
5. **Recuperación de datos**
```

---

### CLASE 09 — Cassandra I: Fundamentos, Arquitectura y CQL

**Marco Teórico:**
- ¿Qué es Cassandra? Origen (Facebook 2008)
- Arquitectura Peer-to-Peer (sin master)
- Modelo de datos: keyspace, tabla, partition key, clustering key
- LSM Tree: memtable, SSTable, commit log
- Distribución de datos con tokens

**Instalación:**
- Java 11+ (requisito)
- Ubuntu/Debian
- Docker
- Windows (manual o Docker)

**Contenido:**
```markdown
## Arquitectura Cassandra

1. **Peer-to-Peer Ring**
   - Sin nodo maestro
   - Todos los nodos son iguales
   - Gossip protocol para comunicación

2. **Componentes**
   - Ring: distribución de tokens
   - Token: posición en el ring (0 a 2^127-1)
   - Gossip: protocolo de comunicación
   - Snitch: topology awareness
   - Replication Factor (RF)

3. **Write Path**
   - Commit Log (WAL)
   - Memtable (memoria)
   - Flush → SSTable (disco)
   - Compaction (merge de SSTables)

4. **Read Path**
   - Bloom Filter (¿está en esta SSTable?)
   - Partition Index
   - Compression Summary
   - Partition Data

## Modelo de Datos CQL

1. **Keyspace**
   - SimpleStrategy
   - NetworkTopologyStrategy
   - Replication Factor

2. **Tablas**
   - Partition Key
   - Clustering Key
   - CLUSTERING ORDER BY

3. **Tipos de datos**
   - Text, Int, Bigint, UUID, Timestamp
   - List, Set, Map
   - UDT (User Defined Types)

## CQL (Cassandra Query Language)

1. **DDL**
   - CREATE KEYSPACE
   - CREATE TABLE
   - CREATE INDEX
   - ALTER TABLE
   - DROP TABLE

2. **DML**
   - INSERT INTO
   - UPDATE
   - DELETE
   - SELECT

3. **Consultas**
   - WHERE con partition key (siempre requerida)
   - Filtros por clustering key
   - ORDER BY
   - LIMIT
   - ALLOW FILTERING (cuidado)

4. ** BATCH**
   - LOGGED BATCH
   - UNLOGGED BATCH
   - COUNTER BATCH

5. **Pagination**
   - paging state
   - Token-based pagination
```

---

### CLASE 10 — Cassandra II: Consistencia, Compaction y Escalamiento

**Marco Teórico:**
- Niveles de consistencia (ONE, QUORUM, ALL, LOCAL_QUORUM)
- Fórmula R + W > N
- Compaction Strategies
- Quorum Consensus
- Multi-datacenter

**Contenido:**
```markdown
## Niveles de Consistencia

1. **Configuración**
   - CONSISTENCY ONE
   - CONSISTENCY QUORUM
   - CONSISTENCY ALL
   - CONSISTENCY LOCAL_QUORUM
   - CONSISTENCY EACH_QUORUM

2. **Fórmula R + W > N**
   - Ejemplos con RF = 3
   - Ejemplos con RF = 5
   - Tradeoffs

3. **Lightweight Transactions (LWT)**
   - IF NOT EXISTS
   - IF EXISTS
   - Paxos protocol

## Compaction

1. **SizeTieredCompactionStrategy (STCS)**
   - Default
   - Agrupa SSTables de tamaño similar
   - Mejor para write-heavy

2. **LeveledCompactionStrategy (LCS)**
   - SSTables en niveles
   - Mejor para read-heavy
   - Más I/O en writes

3. **TimeWindowCompactionStrategy (TWCS)**
   - Ideal para time-series
   - Agrupa por ventanas de tiempo

4. **Choosing Strategy**
   - Tabla de decisión
   - Workloads típicos

## Escalamiento Horizontal

1. **Agregar nodos al cluster**
   - Bootstrap
   - Rebalanceo de tokens
   - Streaming de datos

2. **Quitar nodos**
   - Decommission
   - Cleanup

3. **Multi-Datacenter**
   - NetworkTopologyStrategy
   - Replicación cross-DC
   - Consistencia cross-DC

4. **Sharding en Cassandra**
   - Partition key design
   - Hot partition prevention
   - Data modeling for distribution

## Compaction en la Práctica

1. **Monitorear compaction**
   - nodetool compactionstats
   - nodetool tpstats

2. **Forzar compaction**
   - nodetool compact

3. **Detener compaction**
   - nodetool stop
```

---

### CLASE 11 — Cassandra III: Administración, Backups y Seguridad

**Marco Teórico:**
- Administración de clusters
- Monitoreo y alertas
- Estrategias de backup
- Seguridad completa

**Instalación de Cluster 3 Nodos:**
- Docker Compose completo
- Verificación del cluster

**Contenido:**
```markdown
## Administración de Cassandra

1. **nodetool**
   - status
   - info
   - compactionstats
   - tpstats
   - cfstats
   - repair
   - cleanup
   - compact
   - flush
   - drain

2. **Monitoreo**
   - Métricas JMX
   - Prometheus + Grafana
   - Alarmas y alertas

3. **Mantenimiento**
   - Repair periódico
   - Cleanup después de quitar nodos
   - Flush para forzar escritura a disco
   - Scrub para reparar SSTables corruptos

4. **Performance Tuning**
   - Batch size limits
   - Consistency level tuning
   - Compression (LZ4, Snappy)
   - Caching (key, row, counter)

## Backups en Cassandra

1. **Snapshot-based backups**
   - nodetool snapshot
   - Copiar archivos de snapshot
   - Automatización con scripts

2. **Backup Strategy**
   - Full backup + incrementales
   - Retención de backups
   - Almacenamiento off-site

3. **Restore**
   - nodetool refresh
   - Copiar snapshot al directorio de datos
   - Verificación post-restore

4. **Herramientas**
   - Medusa (Netflix backup tool)
   - CSGTool (restore)

## Seguridad de Cassandra

1. **Autenticación**
   - PasswordAuthenticator
   - AllowAllAuthenticator (inseguro)
   - Crear usuarios y roles

2. **Autorización**
   - CassandraAuthorizer
   - GRANT, REVOKE
   - Permisos por keyspace y tabla

3. **Cifrado**
   - Encryption in transit (SSL/TLS)
   - Encryption at rest
   - Transparent Data Encryption (TDE)

4. **Red**
   - Firewall rules
   - Bind interfaces
   - JMX security

5. **Auditoría**
   - Audit logging
   - Custom audit provider

6. **Backups Seguros**
   - Cifrar snapshots
   - Acceso restringido
   - Verificación de integridad
```

---

### CLASE 12 — Neo4j I: Fundamentos, Cypher y Modelo de Grafos

**Marco Teórico:**
- ¿Qué es una base de datos de grafos?
- Modelo de datos: nodos, relaciones, propiedades, labels
- ¿Cuándo usar grafos vs otras BD?
- Casos de uso: redes sociales, recomendaciones, fraude,知识图谱
- Comparación con SQL (JOINs vs traversals)

**Instalación:**
- Docker
- Ubuntu/Debian
- Windows (Neo4j Desktop)
- Neo4j Browser (interfaz web)

**Contenido:**
```markdown
## Modelo de Grafos

1. **Elementos**
   - Nodos (entidades)
   - Relaciones (conexiones dirigidas)
   - Propiedades (key-value)
   - Labels (categorías)

2. **Propiedades del Grafo**
   - Densidad de conexiones
   - Grado de nodos
   - Caminos
   - Subgrafos

## Cypher: Lenguaje de Consulta

1. **Creación**
   - CREATE (nodos y relaciones)
   - MERGE (crear si no existe)
   - ON CREATE SET / ON MATCH SET

2. **Lectura**
   - MATCH ... RETURN
   - WHERE (filtros)
   - ORDER BY, SKIP, LIMIT
   - DISTINCT
   - WITH (encadenar operaciones)

3. **Patrones de Ruta**
   - Ruta básica: (a)-[:REL]->(b)
   - Ruta variable: -[:REL*1..3]->
   - shortestPath()
   - allShortestPaths()

4. **Filtrado y Agregación**
   - WHERE con operadores
   - Contar: count(), count(DISTINCT ...)
   - Colecciones: collect(), unwind()
   - Matemáticas: avg(), sum(), min(), max()

5. **Actualización**
   - SET (propiedades)
   - REMOVE (propiedades/labels)
   - DELETE (nodos/relaciones)
   - DETACH DELETE

6. **Índices y Constraints**
   - CREATE INDEX
   - CREATE CONSTRAINT
   - FULLTEXT INDEX
   - SHOW INDEXES / CONSTRAINTS
```

---

### CLASE 13 — Neo4j II: Algoritmos de Grafos y Recomendaciones

**Marco Teórico:**
- Algoritmos de grafos: PageRank, Shortest Path, Community Detection
- Graph Data Science Library
- Modelado para recomendaciones
- Similitud de nodos

**Contenido:**
```markdown
## Algoritmos de Grafos

1. **Centrality**
   - PageRank
   - Betweenness Centrality
   - Degree Centrality
   - Closeness Centrality

2. **Pathfinding**
   - Shortest Path (Dijkstra)
   - All Shortest Paths
   - Single Source Shortest Path

3. **Community Detection**
   - Louvain
   - Label Propagation
   - Weakly Connected Components

4. **Similarity**
   - Node Similarity (Jaccard)
   - Cosine Similarity

## Graph Data Science (GDS)

1. **Projecting Graphs**
   - GDS graph project
   - Memoria vs disco

2. **Running Algorithms**
   - Stream mode
   - Stats mode
   - Write mode

3. **Machine Learning on Graphs**
   - Node Classification
   - Link Prediction

## Casos de Uso

1. **Sistema de Recomendaciones**
   - "Usuarios que compraron X también compraron Y"
   - Recomendación basada en categorías
   - Similitud de usuarios

2. **Detección de Fraude**
   - Anillos de fraude
   - Caminos sospechosos

3. **Análisis de Redes Sociales**
   - Comunidades
   - Influencers
   - Caminos más cortos

4. **Knowledge Graphs**
   - Modelado de conocimiento
   - Consultas semánticas
```

---

### CLASE 14 — Neo4j III: Administración, Backups y Seguridad

**Contenido:**
```markdown
## Administración de Neo4j

1. **Monitoreo**
   - dbms.listQueries()
   - dbms.queryJmx()
   - Métricas de rendimiento
   - Neo4j Ops Manager (mencionar)

2. **Mantenimiento**
   - Consistency checks
   - Index management
   - Constraint management
   - Store migration

3. **Performance Tuning**
   - Memory configuration
   - Page cache
   - Query tuning with EXPLAIN/PROFILE
   - Index usage optimization

## Backups de Neo4j

1. **neo4j-admin backup**
   - Full backup
   - Incremental backup
   - Consistent backup (offline)

2. **Online Backup**
   - Backup con base de datos activa
   - Consistencia punto-en-tiempo

3. **Restore**
   - neo4j-admin restore
   - Verificación post-restore

4. **Automatización**
   - Scripts de backup
   - Cron jobs
   - Almacenamiento seguro

## Seguridad de Neo4j

1. **Autenticación**
   - Native auth
   - LDAP
   - OIDC (OpenID Connect)
   - SAML

2. **Autorización**
   - Roles predefinidos
   - Custom roles
   - PERMITTED GRAPHS
   - Read/Write/Admin

3. **Cifrado**
   - SSL/TLS certificates
   - Connector configuration
   - Trust stores

4. **Auditoría**
   - Security log
   - Query logging
   - Custom log providers

5. **Inyección Cypher**
   - Prevención
   - Parámetros en consultas
   - Validación de entrada

6. **Hardening**
   - Disable inter-bolt connector
   - Disable foreign script engines
   - Restrict UDFs
```

---

### CLASE 15 — ObjectDB I: Fundamentos, JPA y Modelo de Objetos

**Marco Teórico:**
- ¿Qué es ObjectDB?
- BD orientada a objetos vs relacional vs NoSQL
- JPA (Java Persistence API) y Hibernate
- Modelo de datos: clases, objetos, herencia
- Cuando usar ObjectDB vs MongoDB vs PostgreSQL

**Instalación:**
- Java 17+ (JDK)
- Maven/Gradle
- ObjectDB Embedded (JAR)
- ObjectDB Server
- Windows y Linux

**Contenido:**
```markdown
## Fundamentos de ObjectDB

1. **¿Qué es una BD Orientada a Objetos?**
   - Modelo relacional vs modelo de objetos
   - Impedancia de impedancia (object-relational impedance mismatch)
   - ObjectDB: BD OODBMS nativa para Java

2. **Arquitectura**
   - Embedded mode (en la aplicación)
   - Client-Server mode (servidor dedicado)
   - Storage: archivos .odb
   - Motor: Enhanced Persistence

3. **JPA (Java Persistence API)**
   - Estándar para persistencia en Java
   - Entity classes
   - Annotations: @Entity, @Id, @OneToMany, etc.
   - EntityManagerFactory
   - EntityManager
   - Transactions

## Modelo de Datos

1. **Entities**
   - @Entity, @Id, @GeneratedValue
   - @Table, @Column
   - @Temporal, @Enumerated

2. **Relaciones**
   - @OneToOne
   - @OneToMany / @ManyToOne
   - @ManyToMany
   - Cascade types
   - Fetch types (LAZY, EAGER)

3. **Herencia**
   - SINGLE_TABLE
   - JOINED
   - TABLE_PER_CLASS

4. **Embeddables**
   - @Embeddable
   - @Embedded

## JPA Query Language (JPQL)

1. **Queries básicas**
   - SELECT ... FROM ... WHERE
   - Named parameters
   - Positional parameters

2. **Relationships queries**
   - JOIN FETCH
   - LEFT JOIN
   - Subqueries

3. **Aggregation**
   - COUNT, AVG, SUM, MIN, MAX
   - GROUP BY, HAVING

4. **Native Queries**
   - @Query annotation
   - Custom SQL

## Ejemplo Completo

```java
// Entity
@Entity
public class Producto {
    @Id @GeneratedValue
    private Long id;
    private String nombre;
    private double precio;
    
    @ManyToOne
    private Categoria categoria;
    
    @OneToMany(cascade = CascadeType.ALL)
    private List<Resena> resenas;
}

// Repository
@Repository
public interface ProductoRepository 
    extends JpaRepository<Producto, Long> {
    
    List<Producto> findByPrecioBetween(double min, double max);
    
    @Query("SELECT p FROM Producto p WHERE p.categoria.nombre = :cat")
    List<Producto> findByCategoria(@Param("cat") String cat);
}
```
```

---

### CLASE 16 — ObjectDB II: Clustering, Administración y Seguridad

**Contenido:**
```markdown
## Clustering en ObjectDB

1. **Server Mode**
   - Configuración del servidor
   - Conexión remota
   - Connection pooling

2. **Replication**
   - Master-Slave replication
   - Sincronización

3. **Backup y Restore**
   - Online backup (sin parar el servidor)
   - Offline backup
   - Automatización

## Administración

1. **Monitoreo**
   - ObjectDB Explorer
   - Métricas JMX
   - Logs de transacciones

2. **Mantenimiento**
   - Defragmentación
   - Compactación
   - Integrity checks

3. **Performance Tuning**
   - Query optimization
   - Index creation
   - Cache configuration
   - Batch operations

## Seguridad

1. **Autenticación**
   - User authentication
   - Password policies

2. **Autorización**
   - Permissions by database
   - Read/Write/Admin roles

3. **Cifrado**
   - SSL/TLS connections
   - Encryption at rest

4. **Auditoría**
   - Transaction logging
   - Access logs

## ObjectDB vs Otras BD

| Característica | ObjectDB | MongoDB | PostgreSQL |
|---------------|----------|---------|------------|
| Modelo | Objetos | Documentos | Tablas |
| Lenguaje | JPA/JPQL | MQL | SQL |
| Herencia | Nativa | Embebido | Tablas separadas |
| Relaciones | Nativa | $lookup/referencia | JOINs |
| Performance | Muy alta | Alta | Media-Alta |
| Uso ideal | Java apps | Web/mobile | General |
```

---

### CLASE 17 — Patrones Multi-Base de Datos y Polyglot Persistence

**Contenido:**
```markdown
## Polyglot Persistence

1. **Concepto**
   - Usar la BD correcta para cada problema
   - Ejemplo: MongoDB + Redis + Neo4j + Cassandra

2. **Patrones de Integración**
   - Database per Service
   - Shared Database
   - CQRS (Command Query Responsibility Segregation)
   - Event Sourcing
   - Saga Pattern
   - Two-Phase Commit

3. **Change Data Capture (CDC)**
   - Debezium
   - Kafka Connect
   - MongoDB Change Streams

## Casos de Uso Multi-BD

1. **E-commerce**
   - MongoDB: catálogo de productos
   - Redis: caché y sesiones
   - Cassandra: historial de pedidos
   - Neo4j: recomendaciones

2. **Red Social**
   - MongoDB: perfiles y posts
   - Redis: feed en tiempo real
   - Neo4j: relaciones sociales
   - Cassandra: métricas

3. **Sistema de Pagos**
   - MongoDB: transacciones
   - Redis: idempotencia
   - Kafka: eventos
   - Debezium: CDC

4. **IoT/Monitoreo**
   - Cassandra: métricas de tiempo real
   - Redis: últimos valores
   - MongoDB: configuración de dispositivos
   - Neo4j: relaciones entre dispositivos

## Event Sourcing

1. **Concepto**
   - Almacenar eventos, no estados
   - Replay de eventos
   - Audit trail

2. **Implementación**
   - Event store
   - Projections
   - Snapshots

## CQRS

1. **Command side**
2. **Query side**
3. **Sincronización entre lados**
```

---

### CLASE 18 — Proyecto Final: Sistema Completo Multi-NoSQL

**Contenido:**
```markdown
## Diseño del Sistema

1. **Requerimientos**
   - API REST para e-commerce
   - Soporte para múltiples bases de datos
   - Autenticación JWT
   - Caché con Redis
   - Recomendaciones con Neo4j
   - Métricas con Cassandra
   - Catálogo con MongoDB
   - Usuarios con ObjectDB

2. **Arquitectura**
   - Diagrama de componentes
   - Flujo de datos
   - Patrones de integración

## Implementación

1. **Setup del Proyecto**
   - Docker Compose multi-bd
   - Configuración de cada BD
   - Seguridad completa

2. **API REST**
   - CRUD de productos (MongoDB)
   - Caché de productos (Redis)
   - Sesiones de usuario (Redis)
   - Recomendaciones (Neo4j)
   - Métricas de访问 (Cassandra)
   - Persistencia de objetos (ObjectDB)

3. **Seguridad**
   - JWT authentication
   - RBAC
   - Rate limiting
   - Input validation
   - NoSQL injection prevention

4. **Monitoreo**
   - Health checks
   - Métricas por BD
   - Alertas

## Evaluación

1. **Criterios**
   - Funcionalidad completa
   - Seguridad implementada
   - Performance aceptable
   - Documentación

2. **Entregable**
   - Código fuente
   - Docker Compose funcional
   - Documentación
   - Demo en vivo
```

---

## Resumen de Cambios por Archivo

| Archivo Actual | Nuevo Archivo | Cambio Principal |
|---------------|---------------|------------------|
| `clase-01-sql-vs-nosql.md` | `clase-01-introduccion-nosql.md` | Expandido con teoría completa |
| `clase-02-acid-cap-consistencia.md` | Integado en Clase 01 | Teoría integrada |
| `clase-03-normalizacion.md` | Integado en Clases 02-03 | Patrones de modelado |
| `clase-04-indexacion.md` | Integado en Clases 02-05 | Índices por tecnología |
| `clase-05-wal-bloom-filters.md` | Integado en Clases 06,09 | Persistencia por tecnología |
| `clase-06-mongodb-avanzado.md` | `clase-02-mongodb-i.md` + `clase-03-mongodb-ii.md` | Dividido y expandido |
| `clase-07-mongodb-replicacion.md` | `clase-04-mongodb-iii.md` | Expandido con admin |
| `clase-08-sharding.md` | `clase-05-mongodb-iv.md` | Integrado con admin completo |
| `clase-09-redis.md` | `clase-06-redis-i.md` + `clase-07-redis-ii.md` + `clase-08-redis-iii.md` | Dividido en 3 |
| `clase-10-cassandra.md` | `clase-09-cassandra-i.md` + `clase-10-cassandra-ii.md` + `clase-11-cassandra-iii.md` | Dividido en 3 |
| `clase-11-neo4j.md` | `clase-12-neo4j-i.md` + `clase-13-neo4j-ii.md` + `clase-14-neo4j-iii.md` | Dividido en 3 |
| — | `clase-15-objectdb-i.md` | **NUEVO** |
| — | `clase-16-objectdb-ii.md` | **NUEVO** |
| — | `clase-17-patrones-multi-bd.md` | **NUEVO** |
| — | `clase-18-proyecto-final.md` | **NUEVO** |

## Estructura de Cada Clase (Template)

Cada clase seguirá esta estructura:

```markdown
# Clase XX — Título

## 1. Marco Teórico
- ¿Qué es?
- Origen y evolución
- Modelo de datos
- Arquitectura (diagrama)
- Casos de uso
- Comparación con otras BD

## 2. Instalación
### Windows (paso a paso)
### Linux (paso a paso)
### Docker (multiplataforma)
### Verificación de instalación

## 3. Arquitectura Detallada
- Componentes principales
- Flujo de escritura/lectura
- Almacenamiento en disco
- Gestión de memoria

## 4. CRUD y Operaciones
### Crear
### Leer (con filtros)
### Actualizar
### Eliminar
### Operaciones avanzadas

## 5. Consultas Avanzadas
- Aggregation/Query language
- Índices
- Optimización
- Patrones de modelado

## 6. Administración
- Monitoreo
- Mantenimiento
- Performance tuning
- Resolución de problemas

## 7. Replicación y Alta Disponibilidad
- Configuración
- Failover
- Read/Write concerns
- Simulación de fallos

## 8. Sharding/Escalamiento (si aplica)
- Distribución de datos
- Consistent hashing
- Balanceo

## 9. Backups y Restore
- Estrategias
- Automatización
- Verificación

## 10. Seguridad
- Autenticación
- Autorización
- Cifrado
- Auditar
- Hardening
- Prevención de inyección

## 11. Ejercicio Práctico
- Paso a paso
- Verificación
```

## Próximos Pasos

1. Crear cada archivo de clase siguiendo el template
2. Migrar contenido existente relevante
3. Agregar teoría faltante
4. Agregar secciones de administración y seguridad
5. Agregar ejemplos de instalación completos
6. Actualizar README.md del curso
7. Actualizar actividades para alinear con nuevas clases
