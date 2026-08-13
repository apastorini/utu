# Actividades — Bases de Datos NoSQL

16 actividades prácticas de **50 minutos** cada una. Todo el material es **open source y 100 % local** (sin nube). En cada actividad hay **marco teórico** y **paso a paso** para que el estudiante trabaje de forma autónoma usando una herramienta de IA (se recomienda **OpenCode**, y la Actividad 1 explica cómo instalarla).

## Cómo usar este material

1. Cada estudiante lee el **marco teórico** (5-8 min) y después sigue los pasos.
2. Todo se ejecuta en la PC del estudiante con **Docker** (las bases corren en contenedores).
3. La IA se usa para resolver dudas, generar explicaciones y verificar resultados. La Actividad 1 muestra cómo instalar **OpenCode**; el resto deja libre la elección de la herramienta (OpenCode, ChatGPT, Claude, Gemini, Copilot, etc.).

## Requisitos previos

- **Docker Desktop** (se instala en la Actividad 1).
- **Node.js LTS** (necesario para OpenCode y para el proyecto final).
- Windows 10/11 (o Linux/macOS con los equivalentes indicados).

## Índice de actividades

| # | Actividad | Base / Tema | Seguridad |
|---|-----------|-------------|-----------|
| 1 | [Instalación de herramientas y Normalización](actividad-01-instalacion-y-normalizacion.md) | Normalización 1FN-3FN + OpenCode + Docker | — |
| 2 | [MongoDB: CRUD y primeras consultas](actividad-02-mongodb-crud.md) | MongoDB (documental) | — |
| 3 | [MongoDB: Aggregation Framework](actividad-03-mongodb-aggregation.md) | MongoDB | — |
| 4 | [Seguridad en MongoDB](actividad-04-seguridad-mongodb.md) | MongoDB | Auth, RBAC, NoSQL injection |
| 5 | [Redis: clave-valor y caché](actividad-05-redis-clave-valor.md) | Redis (clave-valor) | — |
| 6 | [Seguridad en Redis](actividad-06-seguridad-redis.md) | Redis | requirepass, ACL, hardening |
| 7 | [Cassandra: CQL y series de tiempo](actividad-07-cassandra-cql.md) | Cassandra (columnar) | — |
| 8 | [Seguridad en Cassandra](actividad-08-seguridad-cassandra.md) | Cassandra | Auth, roles, GRANT |
| 9 | [Neo4j: grafos y Cypher](actividad-09-neo4j-cypher.md) | Neo4j (grafos) | — |
| 10 | [Seguridad en Neo4j](actividad-10-seguridad-neo4j.md) | Neo4j | Roles, inyección Cypher |
| 11 | [Modelado multi-base: e-commerce](actividad-11-modelado-multibase.md) | MongoDB + Redis + Neo4j | — |
| 12 | [Docker Compose multi-base seguro](actividad-12-docker-compose-seguro.md) | 4 bases juntas | secretos, .env, redes |
| 13 | [Indexación y rendimiento](actividad-13-indexacion-rendimiento.md) | MongoDB | índices, TTL |
| 14 | [Replicación y alta disponibilidad](actividad-14-replicacion-alta-disponibilidad.md) | MongoDB | replica set, failover |
| 15 | [Sharding y escalamiento horizontal](actividad-15-sharding-escalamiento.md) | MongoDB | shard key, chunks |
| 16 | [Proyecto final: API segura multi-base](actividad-16-proyecto-final-multibase.md) | Node.js + MongoDB + Redis + Neo4j | JWT, bcrypt, sesiones |

## Estructura pedagógica

- **Módulo 0 — Herramientas y fundamentos (Actividad 1):** normalización, instalación de OpenCode y Docker.
- **Módulo 1 — MongoDB (Actividades 2-4):** CRUD, aggregation y seguridad.
- **Módulo 2 — Redis (Actividades 5-6):** clave-valor, caché y hardening.
- **Módulo 3 — Cassandra (Actividades 7-8):** columnar, CQL y autorización.
- **Módulo 4 — Neo4j (Actividades 9-10):** grafos, Cypher y seguridad.
- **Módulo 5 — Integración (Actividades 11-12):** polyglot persistence y Docker Compose seguro.
- **Módulo 6 — Escalamiento (Actividades 13-15):** índices, replicación y sharding.
- **Módulo 7 — Proyecto final (Actividad 16):** API segura multi-base.

## Estructura de cada actividad

```
# Título
## Datos generales     → duración, tipo, herramienta de IA, requisitos
## Presupuesto de tiempo
## Objetivos
## Marco teórico        → 5-8 min de lectura
## Paso a paso          → comandos y consultas numerados
## Verificación de resultados
## Criterios de evaluación
## Entregable
```

## Notas al docente

- Las actividades 4, 6, 8 y 10 son las de **seguridad** (una por cada tipo de base NoSQL).
- Las actividades 11, 12 y 16 trabajan **varias bases a la vez** (polyglot persistence).
- Las actividades 14 y 15 requieren más RAM (3-4 GB); conviene no hacerlas en paralelo con otras.
- Cada actividad entrega un **archivo** (`.js`, `.cql`, `.cypher`, `.md`) que sirve como evidencia de evaluación.
