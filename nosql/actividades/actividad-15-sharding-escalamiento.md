# Actividad 15 — Sharding y escalamiento horizontal en MongoDB

## Datos generales

- **Duración:** 50 minutos
- **Tipo:** Individual (o parejas)
- **Herramienta de IA:** Libre
- **Requisitos:** Docker funcionando (~4 GB de RAM libres)

## Presupuesto de tiempo

| Paso | Tiempo |
|------|--------|
| Leer el marco teórico | 8 min |
| Escribir el docker-compose (6 servicios) | 12 min |
| Inicializar config servers y shards | 10 min |
| Conectar el mongos y activar sharding | 8 min |
| Insertar datos y ver la distribución | 7 min |
| Verificación y entrega | 5 min |

## Objetivos

1. Comprender **sharding**: partir los datos en varios nodos para escalar horizontalmente.
2. Levantar un cluster shardeado: **config servers, shards y mongos**.
3. Elegir y activar una **shard key**.
4. Verificar cómo se distribuyen los **chunks** entre los shards.

---

## Marco teórico

### ¿Qué es sharding?

La replicación (Actividad 14) da **copias** de los datos; pero todos los datos siguen estando en un solo cluster. Cuando un dataset es enorme, ningún disco alcanza: hay que **partir** los datos en varios nodos. Eso es **sharding** (particionamiento horizontal).

### Piezas del cluster

```
                    ┌────────────────────────────┐
   la app consulta  │          mongos           │  ← router (balanceador)
   ─────────────────►  (sabe qué shard tiene qué) │
                    └──────┬─────────────┬──────┘
                           │             │
              config servers│             │
              (metadatos)  │             │
                    ┌──────▼──┐     ┌─────▼────┐
                    │  shard 1 │     │  shard 2 │
                    │ (replica)│     │ (replica)│
                    └──────────┘     └──────────┘
```

| Pieza | Función |
|-------|---------|
| **mongos** | router: recibe las consultas y las reparte a los shards |
| **config servers** | guardan los metadatos (qué chunks viven en qué shard) |
| **shards** | guardan los datos; cada shard es normalmente un replica set |

### Shard key y chunks

- **Shard key:** el campo por el que se parten los datos (ej. `_id`, `cliente_id`).
- Los datos se agrupan en **chunks** según rangos de la shard key.
- El mongos usa los metadatos de los config servers para saber **qué chunk buscar en qué shard**.
- Con shard key **hashed**, los valores se distribuyen uniformemente (no hay "puntos calientes").

### Escalamiento

- **Escalado vertical:** una máquina más grande. Tiene límite físico.
- **Escalado horizontal (sharding):** agrego más shards y los datos se reparten. Sin límite práctico.

> **Consistent hashing** (tema de system design) es la idea de fondo: el mapeo dato→nodo se distribuye para minimizar el movimiento de datos al agregar nodos.

---

## Paso a paso

### Paso 1 — Crear la carpeta y el archivo de composición

Creá `C:\curso-nosql\sharding` y adentro `docker-compose.yml`:

```yaml
services:
  configsvr1:
    image: mongo:7
    container_name: configsvr1
    command: mongod --configsvr --replSet cfgrs --port 27019 --bind_ip_all
    ports: ["27019:27019"]
    networks: [mongo-shard]

  configsvr2:
    image: mongo:7
    container_name: configsvr2
    command: mongod --configsvr --replSet cfgrs --port 27019 --bind_ip_all
    networks: [mongo-shard]

  configsvr3:
    image: mongo:7
    container_name: configsvr3
    command: mongod --configsvr --replSet cfgrs --port 27019 --bind_ip_all
    networks: [mongo-shard]

  shard1:
    image: mongo:7
    container_name: shard1
    command: mongod --shardsvr --replSet shard1rs --port 27018 --bind_ip_all
    ports: ["27018:27018"]
    networks: [mongo-shard]

  shard2:
    image: mongo:7
    container_name: shard2
    command: mongod --shardsvr --replSet shard2rs --port 27018 --bind_ip_all
    ports: ["27017:27018"]
    networks: [mongo-shard]

  mongos:
    image: mongo:7
    container_name: mongos
    command: mongos --configdb cfgrs/configsvr1:27019,configsvr2:27019,configsvr3:27019 --port 27000 --bind_ip_all
    ports: ["27000:27000"]
    depends_on: [configsvr1, configsvr2, configsvr3, shard1, shard2]
    networks: [mongo-shard]

networks:
  mongo-shard:
```

> Fijate que los **config servers** forman un replica set (`cfgrs`) con 3 nodos, cada **shard** también es un replica set (acá simplificados a 1 nodo) y el **mongos** es el router que la app ve.

### Paso 2 — Levantar el cluster

```powershell
docker compose up -d
docker ps
```

Esperá 10-20 s a que todos estén "healthy"/"running" (6 contenedores).

### Paso 3 — Inicializar los replica sets

**Config servers:**

```powershell
docker exec configsvr1 mongosh --port 27019 --eval "rs.initiate({_id:'cfgrs', configsvr:true, members:[{_id:0,host:'configsvr1:27019'},{_id:1,host:'configsvr2:27019'},{_id:2,host:'configsvr3:27019'}]})"
```

**Shard 1:**

```powershell
docker exec shard1 mongosh --port 27018 --eval "rs.initiate({_id:'shard1rs', members:[{_id:0,host:'shard1:27018'}]})"
```

**Shard 2:**

```powershell
docker exec shard2 mongosh --port 27018 --eval "rs.initiate({_id:'shard2rs', members:[{_id:0,host:'shard2:27018'}]})"
```

### Paso 4 — Agregar los shards al mongos

```powershell
docker exec mongos mongosh --port 27000 --eval "sh.addShard('shard1rs/shard1:27018')"
docker exec mongos mongosh --port 27000 --eval "sh.addShard('shard2rs/shard2:27018')"
```

Verificá el estado:

```powershell
docker exec mongos mongosh --port 27000 --eval "sh.status()"
```

Deberías ver 2 shards: `shard1rs` y `shard2rs`.

### Paso 5 — Activar sharding y elegir la shard key

```powershell
docker exec mongos mongosh --port 27000 --eval "sh.enableSharding('tienda')"
```

Ahora shardeá la colección `ventas` por `_id` con **hashed** (distribución uniforme):

```powershell
docker exec mongos mongosh --port 27000 --eval "sh.shardCollection('tienda.ventas', { _id: 'hashed' })"
```

### Paso 6 — Insertar datos y ver la distribución

```powershell
docker exec -it mongos mongosh --port 27000
```

```javascript
use tienda

// 20.000 ventas
const docs = [];
for (let i = 0; i < 20000; i++) {
    docs.push({ id: i, cliente: "cliente-" + (i % 100), total: Math.round(Math.random() * 500) });
}
db.ventas.insertMany(docs);
db.ventas.countDocuments();

// ¿Cómo se repartieron los datos?
db.ventas.getShardDistribution()
```

`getShardDistribution()` muestra **cuántos documentos y qué porcentaje** vive en cada shard. Idealmente ~50% / 50%.

### Paso 7 — El mongos enruta las consultas

```javascript
// Consulta normal: el mongos decide dónde buscarla
db.ventas.find({ id: 15000 }).pretty();

// Consulta con "targeted read": va directo al shard correcto
db.ventas.find({ _id: ObjectId("...") });
```

El mongos oculta el cluster: la app **no sabe** que hay 2 shards.

### Paso 8 — Ver los chunks

```javascript
sh.status()
```

Mirá la sección de `tienda.ventas`: los **chunks** y a qué shard pertenece cada uno.

### Paso 9 — Preguntar a la IA

```
¿Qué pasa si elijo una mala shard key? (por ejemplo, una con pocos valores distintos)
¿Cuál es la diferencia entre particionar por rango y por hash?
¿Cómo se relaciona el sharding con el teorema CAP y la consistencia?
```

## Verificación de resultados

- [ ] `sh.status()` muestra 2 shards (`shard1rs`, `shard2rs`).
- [ ] `db.ventas.getShardDistribution()` reparte los 20000 documentos entre los 2 shards.
- [ ] Los datos están balanceados (≈50% en cada shard).
- [ ] El mongos responde consultas normales sin errores.
- [ ] Podés explicar el rol de cada pieza (config servers, mongos, shards).

## Criterios de evaluación

| Criterio | Puntos |
|----------|--------|
| docker-compose con 6 servicios | 25 |
| Inicialización de replica sets (config + shards) | 20 |
| sh.addShard y sh.status correctos | 20 |
| shardCollection con hash | 15 |
| Distribución verificada + explicación | 20 |

## Entregable

- Archivo `sharding.md` con: `sh.status()` inicial y final, la salida de `getShardDistribution()` y una captura de la inserción.
- Respuesta de la IA sobre las malas shard keys.

## Para pensar

Con **replicación** (14) tenés copias y con **sharding** (15) tenés particiones. En el proyecto final (Actividad 16) vas a construir una API que usa MongoDB + Redis + Neo4j de forma segura, aplicando índices, replicación y el stack de la Actividad 12.
