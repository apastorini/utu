# Curso: Bases de Datos NoSQL — 12 Clases

## Objetivo

Dominar los conceptos fundamentales, arquitecturas y herramientas de bases de datos NoSQL, integrando los 20 temas clave de system design interviews.

## Estructura

| Clase | Tema | Tecnología |
|-------|------|------------|
| 1 | SQL vs NoSQL y tipos de BD NoSQL | MongoDB |
| 2 | ACID, CAP Theorem y Consistencia | MongoDB, PostgreSQL, Cassandra |
| 3 | Normalización vs Desnormalización | MongoDB, PostgreSQL |
| 4 | Indexación: B-Tree vs LSM Tree | MongoDB, Redis |
| 5 | WAL y Bloom Filters | PostgreSQL, Redis |
| 6 | MongoDB: Modelado y consultas avanzadas | MongoDB |
| 7 | MongoDB: Replicación y alta disponibilidad | MongoDB |
| 8 | Sharding, particionamiento y consistent hashing | MongoDB, Python |
| 9 | Redis: Caché y clave-valor | Redis |
| 10 | Cassandra: Base de datos columnar distribuida | Cassandra |
| 11 | Neo4j: Bases de datos de grafos | Neo4j |
| 12 | Transacciones distribuidas y patrones avanzados | MongoDB, Debezium, Kafka |

## Módulos

- **Módulo 1 — Fundamentos:** Clases 1-3
- **Módulo 2 — Motores de almacenamiento e indexación:** Clases 4-5
- **Módulo 3 — MongoDB en profundidad:** Clases 6-7
- **Módulo 4 — Escalamiento horizontal:** Clases 8-9
- **Módulo 5 — Columnares y grafos:** Clases 10-11
- **Módulo 6 — Transacciones distribuidas:** Clase 12

## Escenarios Multi-Base de Datos

El curso integra escenarios que combinan múltiples bases de datos:

| Clase | Escenario multi-BD |
|-------|--------------------|
| 2 | Comparación SQL vs NoSQL vs Columnar en el mismo caso de uso |
| 3 | Modelar e-commerce en SQL + NoSQL simultáneamente |
| 8 | Sharding en MongoDB + caching en Redis |
| 9 | Redis como caché frente a MongoDB/PostgreSQL |
| 10 | Cassandra + Redis para métricas en tiempo real |
| 11 | Neo4j + MongoDB para recomendaciones con perfiles |
| 12 | MongoDB + Kafka + Debezium + Redis para sistema de pagos |

## Tareas del Curso

- **Tarea 1 — Exposición Grupal:** `tarea-1-exposiciones.md`
- **Tarea 2 — Diseño de Sistemas NoSQL:** `tarea-2-diseno-sistemas.md`

## Mapeo de Temas de System Design

Los 20 temas de system design están cubiertos en las clases:

1. SQL vs NoSQL → Clase 1
2. ACID → Clase 2
3. Normalización → Clase 3
4. Database Indexing → Clase 4
5. Replication Strategies → Clase 7
6. Read Replicas → Clase 7
7. Database Caching → Clase 9
8. CAP Theorem → Clase 2
9. Sharding & Partitioning → Clase 8
10. Isolation Levels → Clase 10
11. Materialized Views → Clase 9
12. Consistent Hashing → Clase 8
13. Eventual Consistency → Clase 2
14. B-Tree vs LSM Tree → Clases 4, 10
15. Write-Ahead Log → Clase 5
16. Bloom Filters → Clase 5
17. Quorum Consensus → Clase 10
18. Change Data Capture → Clase 12
19. Two-Phase Commit → Clase 12
20. Saga Pattern → Clase 12
