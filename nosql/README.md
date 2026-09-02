# Curso: Bases de Datos NoSQL — 18 Clases

## Objetivo

Dominar los conceptos fundamentales, arquitecturas y herramientas de bases de datos NoSQL, con un enfoque práctico en **administración, seguridad, backups, replicación y sharding** para formar profesionales capaces de administrar bases de datos en producción.

## Filosofía del Curso

Cada clase es un **profundización completa** en una tecnología NoSQL, incluyendo:
1. **Marco teórico** — conceptos, historia, fundamentos
2. **Instalación paso a paso** — Windows, Linux y Docker
3. **Arquitectura detallada** — componentes, flujos, diagramas
4. **CRUD y consultas** — ejemplos prácticos con filtros
5. **Administración** — monitoreo, mantenimiento, performance tuning
6. **Replicación y alta disponibilidad** — configuración, failover
7. **Sharding/escalamiento** — distribución de datos
8. **Backups y restore** — estrategias, automatización
9. **Seguridad completa** — auth, cifrado, auditoría, hardening
10. **Ejercicio práctico** — paso a paso verificable

## Estructura del Curso

### Módulo 0 — Fundamentos (1 clase)

| Clase | Archivo | Tema | Tecnología |
|-------|---------|------|------------|
| 1 | `clase-01-introduccion-nosql.md` | Introducción a NoSQL y Categorías | General (todas) |

### Módulo 1 — MongoDB: Base de Datos Documental (4 clases)

| Clase | Archivo | Tema | Enfoque |
|-------|---------|------|---------|
| 2 | `clase-02-mongodb-i.md` | MongoDB I: Fundamentos, Instalación y CRUD | CRUD completo, configuración |
| 3 | `clase-03-mongodb-ii.md` | MongoDB II: Consultas Avanzadas y Aggregation | Pipeline de agregación |
| 4 | `clase-04-mongodb-iii.md` | MongoDB III: Replicación y Alta Disponibilidad | Replica Sets, Oplog, Failover |
| 5 | `clase-05-mongodb-iv.md` | MongoDB IV: Sharding, Administración y Seguridad | Cluster shardado, admin completo |

### Módulo 2 — Redis: Almacenamiento Clave-Valor (3 clases)

| Clase | Archivo | Tema | Enfoque |
|-------|---------|------|---------|
| 6 | `clase-06-redis-i.md` | Redis I: Fundamentos, Tipos de Datos y Persistencia | 8 tipos de datos, RDB/AOF |
| 7 | `clase-07-redis-ii.md` | Redis II: Caché, Patrones y Pub/Sub | Cache-aside, Streams, Rate Limiting |
| 8 | `clase-08-redis-iii.md` | Redis III: Replicación, Clustering y Seguridad | Sentinel, Cluster, ACL |

### Módulo 3 — Cassandra: Base de Datos Columnar (3 clases)

| Clase | Archivo | Tema | Enfoque |
|-------|---------|------|---------|
| 9 | `clase-09-cassandra-i.md` | Cassandra I: Fundamentos, Arquitectura y CQL | LSM Tree, Peer-to-Peer, CQL |
| 10 | `clase-10-cassandra-ii.md` | Cassandra II: Consistencia, Compaction y Escalamiento | QUORUM, STCS/LCS/TWCS |
| 11 | `clase-11-cassandra-iii.md` | Cassandra III: Administración, Backups y Seguridad | nodetool, snapshots, auth |

### Módulo 4 — Neo4j: Base de Datos de Grafos (3 clases)

| Clase | Archivo | Tema | Enfoque |
|-------|---------|------|---------|
| 12 | `clase-12-neo4j-i.md` | Neo4j I: Fundamentos, Cypher y Modelo de Grafos | Cypher completo, modelo de grafos |
| 13 | `clase-13-neo4j-ii.md` | Neo4j II: Algoritmos de Grafos y Recomendaciones | PageRank, Louvain, Similitud |
| 14 | `clase-14-neo4j-iii.md` | Neo4j III: Administración, Backups y Seguridad | GDS, SSL, roles, auditoría |

### Módulo 5 — ObjectDB: Base de Datos Orientada a Objetos (2 clases)

| Clase | Archivo | Tema | Enfoque |
|-------|---------|------|---------|
| 15 | `clase-15-objectdb-i.md` | ObjectDB I: Fundamentos, JPA y Modelo de Objetos | JPA, entities, herencia, JPQL |
| 16 | `clase-16-objectdb-ii.md` | ObjectDB II: Clustering, Administración y Seguridad | Server mode, backup, SSL |

### Módulo 6 — Integración y Patrones Avanzados (2 clases)

| Clase | Archivo | Tema | Enfoque |
|-------|---------|------|---------|
| 17 | `clase-17-patrones-multi-bd.md` | Patrones Multi-Base de Datos y Polyglot Persistence | CQRS, Event Sourcing, CDC, Saga |
| 18 | `clase-18-proyecto-final.md` | Proyecto Final: Sistema Completo Multi-NoSQL | E-commerce con 5 bases de datos |

## Resumen por Tecnología

| Tecnología | Categoría | Clases | Contenido Principal |
|------------|-----------|--------|---------------------|
| MongoDB | Documental | 2, 3, 4, 5 | CRUD, Aggregation, Replicación, Sharding, Admin |
| Redis | Clave-Valor | 6, 7, 8 | Tipos de datos, Caché, Streams, Cluster, ACL |
| Cassandra | Columnar | 9, 10, 11 | CQL, Consistencia, Compaction, Backups, Auth |
| Neo4j | Grafo | 12, 13, 14 | Cypher, Algoritmos, GDS, Roles, SSL |
| ObjectDB | Orientado a Objetos | 15, 16 | JPA, Herencia, Clustering, Backup |

## Contenido de Administración y Seguridad por Clase

| Clase | Admin | Backups | Replicación | Sharding | Seguridad |
|-------|-------|---------|-------------|----------|-----------|
| 1 | — | — | — | — | Introducción |
| 2 | Config | — | — | — | Auth básica, NoSQL injection |
| 3 | Explain, Profiler | — | — | — | — |
| 4 | Monitoreo | mongodump | Replica Set | — | Write/Read Concern |
| 5 | nodetool | Scripts | — | Cluster shardado | Completa |
| 6 | — | RDB/AOF | — | — | Básica |
| 7 | — | — | — | — | Rate Limiting |
| 8 | INFO, SLOWLOG | Scripts | Master-Slave | Cluster (16384 slots) | ACL, TLS |
| 9 | nodetool | — | — | — | Básica |
| 10 | Compaction | — | Multi-DC | Horizontal | QUORUM |
| 11 | nodetool completo | Snapshots | — | — | SSL, Auth completa |
| 12 | Browser, Cypher | — | — | — | Constraints |
| 13 | GDS | — | — | — | — |
| 14 | Monitoreo | neo4j-admin | — | — | SSL, Roles, Auditoría |
| 15 | Explorer | Online/Offline | — | — | — |
| 16 | JMX, Logging | Automatizado | Master-Slave | — | SSL, Auth completa |
| 17 | — | — | — | — | Patrones de seguridad |
| 18 | Monitoreo completo | Estrategia completa | Configurada | Configurado | JWT + RBAC + Rate Limit |

## Escenarios Multi-Base de Datos

| Clase | Escenario multi-BD |
|-------|--------------------|
| 1 | Comparación de todas las 5 categorías |
| 4 | MongoDB + Redis para caché de replicados |
| 5 | MongoDB shardado + Redis cache |
| 8 | Redis como caché frente a MongoDB/PostgreSQL |
| 10 | Cassandra + Redis para métricas en tiempo real |
| 13 | Neo4j + MongoDB para recomendaciones con perfiles |
| 15 | ObjectDB + MongoDB para persistencia Java |
| 17 | Patrones de integración multi-BD |
| 18 | Sistema e-commerce completo con 5 bases de datos |

## Actividades Prácticas

Las actividades están en la carpeta `actividades/` y corresponden a la estructura de 16 actividades de 50 minutos cada una.

| # | Actividad | Base / Tema | Seguridad |
|---|-----------|-------------|-----------|
| 1 | [Instalación de herramientas y Normalización](actividades/actividad-01-instalacion-y-normalizacion.md) | Normalización + OpenCode + Docker | — |
| 2 | [MongoDB: CRUD y primeras consultas](actividades/actividad-02-mongodb-crud.md) | MongoDB | — |
| 3 | [MongoDB: Aggregation Framework](actividades/actividad-03-mongodb-aggregation.md) | MongoDB | — |
| 4 | [Seguridad en MongoDB](actividades/actividad-04-seguridad-mongodb.md) | MongoDB | Auth, RBAC, NoSQL injection |
| 5 | [Redis: clave-valor y caché](actividades/actividad-05-redis-clave-valor.md) | Redis | — |
| 6 | [Seguridad en Redis](actividades/actividad-06-seguridad-redis.md) | Redis | requirepass, ACL, hardening |
| 7 | [Cassandra: CQL y series de tiempo](actividades/actividad-07-cassandra-cql.md) | Cassandra | — |
| 8 | [Seguridad en Cassandra](actividades/actividad-08-seguridad-cassandra.md) | Cassandra | Auth, roles, GRANT |
| 9 | [Neo4j: grafos y Cypher](actividades/actividad-09-neo4j-cypher.md) | Neo4j | — |
| 10 | [Seguridad en Neo4j](actividades/actividad-10-seguridad-neo4j.md) | Neo4j | Roles, inyección Cypher |
| 11 | [Modelado multi-base: e-commerce](actividades/actividad-11-modelado-multibase.md) | MongoDB + Redis + Neo4j | — |
| 12 | [Docker Compose multi-base seguro](actividades/actividad-12-docker-compose-seguro.md) | 4 bases juntas | secretos, .env, redes |
| 13 | [Indexación y rendimiento](actividades/actividad-13-indexacion-rendimiento.md) | MongoDB | índices, TTL |
| 14 | [Replicación y alta disponibilidad](actividades/actividad-14-replicacion-alta-disponibilidad.md) | MongoDB | replica set, failover |
| 15 | [Sharding y escalamiento horizontal](actividades/actividad-15-sharding-escalamiento.md) | MongoDB | shard key, chunks |
| 16 | [Proyecto final: API segura multi-base](actividades/actividad-16-proyecto-final-multibase.md) | Node.js + MongoDB + Redis + Neo4j | JWT, bcrypt, sesiones |

## Mapeo de Temas de System Design (20 temas)

Los 20 temas de system design están cubiertos en las clases:

| # | Tema | Clase(s) |
|---|------|----------|
| 1 | SQL vs NoSQL | Clase 1 |
| 2 | ACID | Clase 1 |
| 3 | Normalización | Clase 1 (conceptos) |
| 4 | Database Indexing | Clases 2, 3, 6, 9 |
| 5 | Replication Strategies | Clases 4, 8, 10, 11 |
| 6 | Read Replicas | Clase 4 |
| 7 | Database Caching | Clases 7, 8 |
| 8 | CAP Theorem | Clase 1 |
| 9 | Sharding & Partitioning | Clases 5, 8, 10 |
| 10 | Isolation Levels | Clases 1, 10 |
| 11 | Materialized Views | Clase 7 |
| 12 | Consistent Hashing | Clase 5 |
| 13 | Eventual Consistency | Clase 1 |
| 14 | B-Tree vs LSM Tree | Clases 2, 6, 9 |
| 15 | Write-Ahead Log | Clases 2, 6, 9 |
| 16 | Bloom Filters | Clases 6, 9 |
| 17 | Quorum Consensus | Clase 10 |
| 18 | Change Data Capture | Clase 17 |
| 19 | Two-Phase Commit | Clase 17 |
| 20 | Saga Pattern | Clase 17 |

## Estructura de Archivos

```
nosql/
├── README.md                              ← Este archivo
├── PLAN-REESTRUCTURACION.md               ← Plan de la reestructuración
├── clase-01-introduccion-nosql.md         ← NUEVO
├── clase-02-mongodb-i.md                  ← NUEVO
├── clase-03-mongodb-ii.md                 ← NUEVO
├── clase-04-mongodb-iii.md                ← NUEVO
├── clase-05-mongodb-iv.md                 ← NUEVO
├── clase-06-redis-i.md                    ← NUEVO
├── clase-07-redis-ii.md                   ← NUEVO
├── clase-08-redis-iii.md                  ← NUEVO
├── clase-09-cassandra-i.md                ← NUEVO
├── clase-10-cassandra-ii.md               ← NUEVO
├── clase-11-cassandra-iii.md              ← NUEVO
├── clase-12-neo4j-i.md                    ← NUEVO
├── clase-13-neo4j-ii.md                   ← NUEVO
├── clase-14-neo4j-iii.md                  ← NUEVO
├── clase-15-objectdb-i.md                 ← NUEVO
├── clase-16-objectdb-ii.md                ← NUEVO
├── clase-17-patrones-multi-bd.md          ← NUEVO
├── clase-18-proyecto-final.md             ← NUEVO
├── actividades/                           ← Actividades prácticas
│   ├── README.md
│   ├── actividad-01-instalacion-y-normalizacion.md
│   ├── actividad-02-mongodb-crud.md
│   ├── ... (16 actividades)
│   └── docx/
└── [archivos antiguos]                    ← Pueden eliminarse
    ├── clase-01-sql-vs-nosql.md
    ├── clase-02-acid-cap-consistencia.md
    ├── clase-03-normalizacion.md
    ├── clase-04-indexacion.md
    ├── clase-05-wal-bloom-filters.md
    ├── clase-06-mongodb-avanzado.md
    ├── clase-07-mongodb-replicacion.md
    ├── clase-08-sharding.md
    ├── clase-09-redis.md
    ├── clase-10-cassandra.md
    └── clase-11-neo4j.md
```

## Requisitos

- **Docker Desktop** (se instala en la Actividad 1)
- **Node.js LTS** (necesario para OpenCode)
- **Java 17+** (para ObjectDB y Cassandra)
- **Python 3.x** (para ejemplos de integración)
- Windows 10/11 (o Linux/macOS)

## Notas al Docente

- Cada clase tiene **~600-1000+ líneas** de contenido comprehensivo
- Los diagramas Mermaid se renderizan en GitHub, VS Code, y la mayoría de editores markdown
- Las clases 4, 5, 8, 11, 14, 16 tienen **secciones completas de seguridad**
- La Clase 18 es un **proyecto final integrador** que usa las 5 bases de datos
- Los archivos antiguos (clase-01-sql-vs-nosql.md, etc.) pueden eliminarse después de verificar que el nuevo contenido los cubre
