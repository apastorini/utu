# Actividad 7 — Cassandra: base columnar y consultas CQL

## Datos generales

- **Duración:** 50 minutos
- **Tipo:** Individual
- **Herramienta de IA:** Libre
- **Requisitos:** Docker funcionando (necesitás ~2 GB de RAM libre)

## Presupuesto de tiempo

| Paso | Tiempo |
|------|--------|
| Leer el marco teórico | 7 min |
| Levantar Cassandra con Docker | 8 min |
| Crear keyspace y tablas | 10 min |
| Insertar datos | 8 min |
| Consultas CQL (time-series) | 12 min |
| Verificación y entrega | 5 min |

## Objetivos

1. Comprender el modelo de datos **columnar** y su optimización para escrituras.
2. Diferenciar **partition key** de **clustering key**.
3. Escribir CQL: `CREATE KEYSPACE`, `CREATE TABLE`, `INSERT`, `SELECT`.
4. Modelar un caso de datos de **series de tiempo** (métricas de servidores).

---

## Marco teórico

### ¿Qué es Cassandra?

Apache Cassandra es una base NoSQL **columnar distribuida**, open source, diseñada para escribir enormes volúmenes de datos sin perder disponibilidad. Es usada por Netflix, Spotify, Uber, Instagram, etc.

### Modelo lógico vs físico

- **Lógicamente** se ven tablas con columnas (similar a SQL).
- **Físicamente**, los datos de la misma **partición** se guardan juntos, ordenados por la **clave de clustering**.

### Los 3 conceptos clave de CQL

| Concepto | Ejemplo | Función |
|----------|---------|---------|
| **Partition key** | `servidor_id` | decide en qué nodo vive el dato |
| **Clustering key** | `fecha` | ordena los datos dentro de la partición |
| **Primary key** | `(servidor_id, fecha)` | es la unión de ambos |

```
PRIMARY KEY (partition_key, clustering_key1, clustering_key2, ...)
```

### Regla de oro del modelado Cassandra

> **"El modelado se hace al revés que en SQL":** primero pensás las consultas que vas a hacer, y después diseñás las tablas para servir **esas consultas específicas**. Una consulta por tabla, o tablas denormalizadas a propósito.

### Partición

Todos los datos con la misma `partition key` se guardan juntos (en un nodo). Eso hace las consultas por partición **muy rápidas**, pero te obliga a elegir bien la clave:

- **Muy pocas particiones** → todo cae en un nodo (desbalance).
- **Partition key que cambia poco** (ej. país) → escalamiento pobre.

---

## Paso a paso

### Paso 1 — Levantar Cassandra

```powershell
docker run -d --name cassandra-clase \
  -p 9042:9042 \
  cassandra:5
```

Cassandra tarda un poco en arrancar (30-60 s). Verificá:

```powershell
docker ps
```

### Paso 2 — Entrar a la consola CQL

```powershell
docker exec -it cassandra-clase cqlsh
```

Deberías ver `cqlsh>`. Probá:

```sql
SELECT release_version FROM system.local;
```

### Paso 3 — Crear el keyspace

Un keyspace agrupa tablas (equivalente aproximado a una base de datos).

```sql
CREATE KEYSPACE monitoreo
  WITH replication = {
    'class': 'SimpleStrategy',
    'replication_factor': 1
  };
```

> `SimpleStrategy` es solo para pruebas con un nodo. En producción se usa `NetworkTopologyStrategy`.

### Paso 4 — Crear una tabla de series de tiempo

```sql
USE monitoreo;

CREATE TABLE metricas_servidor (
    servidor_id uuid,
    fecha timestamp,
    cpu double,
    memoria double,
    disco double,
    PRIMARY KEY (servidor_id, fecha)
) WITH CLUSTERING ORDER BY (fecha DESC);
```

- `servidor_id` es la **partition key**.
- `fecha` es la **clustering key** (ordena descendente: lo más nuevo primero).

### Paso 5 — Ver las tablas del keyspace

```sql
DESCRIBE KEYSPACES;
DESCRIBE TABLE metricas_servidor;
```

### Paso 6 — Insertar datos

```sql
INSERT INTO metricas_servidor (servidor_id, fecha, cpu, memoria, disco)
VALUES (uuid(), toTimestamp(now()), 42.5, 61.0, 78.2);

INSERT INTO metricas_servidor (servidor_id, fecha, cpu, memoria, disco)
VALUES (uuid(), toTimestamp(now()), 55.0, 63.4, 79.0);

INSERT INTO metricas_servidor (servidor_id, fecha, cpu, memoria, disco)
VALUES (uuid(), toTimestamp(now()), 38.1, 58.2, 77.5);
```

> Ojo: con `uuid()` cada fila tiene una partición distinta. Para el próximo paso, guardá **un mismo servidor** usando el mismo `uuid()` fijo:

```sql
-- Insertamos 3 lecturas del MISMO servidor (misma partition key)
INSERT INTO metricas_servidor (servidor_id, fecha, cpu, memoria, disco)
VALUES (11111111-1111-1111-1111-111111111111, '2026-08-01 10:00:00', 41.0, 60.0, 75.0);

INSERT INTO metricas_servidor (servidor_id, fecha, cpu, memoria, disco)
VALUES (11111111-1111-1111-1111-111111111111, '2026-08-01 10:05:00', 47.0, 62.0, 76.0);

INSERT INTO metricas_servidor (servidor_id, fecha, cpu, memoria, disco)
VALUES (11111111-1111-1111-1111-111111111111, '2026-08-01 10:10:00', 88.0, 75.0, 81.0);

-- Otro servidor distinto
INSERT INTO metricas_servidor (servidor_id, fecha, cpu, memoria, disco)
VALUES (22222222-2222-2222-2222-222222222222, '2026-08-01 10:00:00', 20.0, 40.0, 50.0);
```

### Paso 7 — Consultar por partición (rápido)

```sql
SELECT * FROM metricas_servidor
WHERE servidor_id = 11111111-1111-1111-1111-111111111111;
```

Los datos vienen **ordenados por fecha descendente** gracias al clustering.

### Paso 8 — Rango de tiempo dentro de la partición

```sql
SELECT * FROM metricas_servidor
WHERE servidor_id = 11111111-1111-1111-1111-111111111111
  AND fecha >= '2026-08-01 10:05:00';
```

### Paso 9 — Ver por qué NO se puede consultar de otra forma

Intentá filtrar solo por fecha (sin partition key):

```sql
SELECT * FROM metricas_servidor WHERE fecha = '2026-08-01 10:00:00';
```

CQL te da un error: necesita la partition key (o `ALLOW FILTERING`). Ese error **es una feature**: obliga a diseñar tablas pensando en las consultas.

### Paso 10 — Agregar datos de ejemplo de "ventas diarias" y agregar

```sql
CREATE TABLE ventas_diarias (
    pais text,
    fecha date,
    total double,
    PRIMARY KEY (pais, fecha)
);

INSERT INTO ventas_diarias (pais, fecha, total) VALUES ('UY', '2026-08-10', 1200.50);
INSERT INTO ventas_diarias (pais, fecha, total) VALUES ('UY', '2026-08-11', 980.00);
INSERT INTO ventas_diarias (pais, fecha, total) VALUES ('AR', '2026-08-10', 3400.00);

SELECT * FROM ventas_diarias;
```

### Paso 11 — Preguntar a la IA

```
¿Cuál es la diferencia entre partition key y clustering key en Cassandra? Mostrame un ejemplo.
¿Qué es ALLOW FILTERING y por qué es peligroso para el rendimiento?
¿Cómo modelaría Cassandra las métricas de 1000 servidores en tiempo real?
```

## Verificación de resultados

- [ ] El keyspace `monitoreo` existe y `DESCRIBE TABLE` muestra la estructura.
- [ ] La consulta del paso 7 devuelve las 3 lecturas del servidor `1111...` ordenadas por fecha descendente.
- [ ] La consulta del paso 9 da error de CQL (sin partition key).
- [ ] `SELECT * FROM ventas_diarias;` funciona (toda la tabla es "una consulta de partición por cada pais").

## Criterios de evaluación

| Criterio | Puntos |
|----------|--------|
| Contenedor Cassandra levantado | 10 |
| Keyspace + tabla con clave correcta | 25 |
| Inserciones correctas | 20 |
| Consultas por partición y rango | 25 |
| Error del paso 9 explicado | 20 |

## Entregable

- Archivo `cassandra-cql.cql` con todos los comandos y sus resultados.
- Respuesta de la IA sobre la diferencia partition vs clustering key.

## Seguridad (adelanto)

Cassandra viene con autenticación **desactivada** por defecto. En la próxima actividad la vas a activar, crear usuarios con roles (SUPERUSER, lector, escritor) y ver cómo Cassandra autoriza por **tabla** con `GRANT`.
