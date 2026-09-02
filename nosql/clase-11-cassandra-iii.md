# Clase 11 — Cassandra III: Administración, Backups y Seguridad

---

## 1. Administración de Cassandra

### 1.1 nodetool COMPLETO

`nodetool` es la herramienta principal para administrar un nodo de Cassandra. Se ejecuta localmente en cada nodo del cluster.

#### nodetool status

Muestra el estado general del cluster: qué nodos están activos, su carga, y distribución de datos.

```bash
nodetool status
```

```
Datacenter: DC1
===============
Status=Up/Down
|/ State=Normal/Leaving/Joining/Moving
--
Address    Load       Tokens  Owns (effective)  Host ID                           Rack
10.0.0.1   256.12 GiB  256     33.3%             a1b2c3d4-e5f6-7890-abcd-ef1234567890  rack1
10.0.0.2   248.87 GiB  256     33.3%             b2c3d4e5-f6a7-8901-bcde-f12345678901  rack1
10.0.0.3   252.45 GiB  256     33.4%             c3d4e5f6-a7b8-9012-cdef-123456789012  rack1
```

**Campos explicados:**

| Campo | Descripción |
|-------|-------------|
| **Address** | IP del nodo |
| **Load** | Cantidad de datos almacenados en el nodo |
| **Tokens** | Número de tokens virtuales |
| **Owns (effective)** | Porcentaje de datos que posee este nodo |
| **Host ID** | Identificador único del nodo |
| **Rack** | Rack físico/lógico donde está el nodo |

**Estados posibles:**

| State | Descripción |
|-------|-------------|
| **Normal** | Nodo operativo normal |
| **Leaving** | Nodo abandonando el cluster (decommission) |
| **Joining** | Nodo uniéndose al cluster (bootstrap) |
| **Moving** | Nodo moviendo sus rangos de tokens |

**Status Up/Down:**
- **Up**: Nodo respondiendo a gossip
- **Down**: Nodo no responde (puede estar caído o con problemas de red)

#### nodetool info

Información detallada del nodo actual:

```bash
nodetool info
```

```
ID                     : a1b2c3d4-e5f6-7890-abcd-ef1234567890
Gossip active          : true
Native Transport active: true
Load                   : 256.12 GiB
Tokens                 : 256
Data Center            : DC1
Rack                   : rack1
Partitioner            : org.apache.cassandra.dht.Murmur3Partitioner
Released Version       : 4.1.0
Native Transport Address: 10.0.0.1
Listen Address         : 10.0.0.1
Entropy                : 0.9987
Uptime (seconds)       : 864000
Heap Memory (MB)       : 4096.00 / 8192.00
Off Heap Memory (MB)   : 128.00
Data Center            : DC1
Rack                   : rack1
Exceptions             : 0
Key Cache              : size 1024, capacity 1024, hit count 50000, size 0
Row Cache              : size 0, capacity 0, hit count 0
Counter Cache          : size 0, capacity 0
```

**Campos importantes:**

| Campo | Descripción |
|-------|-------------|
| **Gossip active** | Si el protocolo gossip está activo |
| **Native Transport active** | Si CQL native transport está activo |
| **Load** | Datos almacenados |
| **Heap Memory** | Uso de heap JVM (usado / máximo) |
| **Off Heap Memory** | Memoria fuera del heap (memtables off-heap) |
| **Key Cache** | Cache de partition keys |
| **Row Cache** | Cache de filas completas |
| **Uptime** | Tiempo activo del nodo |

#### nodetool compactionstats

Muestra el estado actual de compaction:

```bash
nodetool compactionstats
```

```
pending tasks: 2
  compaction id:     abc-123-def-456
  keyspace:          mi_keyspace
  table:             usuarios
  bytes total:       1073741824
  bytes compacted:   536870912
  progress:          50.0%
  SSTables to compact: 8
  Compaction type:   SizeTieredCompactionStrategy
  Cell count per sstable:
    abc123-...-def456  2500000
    ghi789-...-jkl012  2400000
```

**Uso para monitoreo:**
```bash
# Monitorear en tiempo real
watch -n 5 nodetool compactionstats

# En scripts de monitoreo
nodetool compactionstats | grep "pending tasks" | awk '{print $3}'
```

#### nodetool tpstats (Thread Pool Stats)

Estadísticas de los pools de hilos:

```bash
nodetool tpstats
```

```
Pool Name                    Active  Pending  Completed  Blocked  All time blocked
---------------------------------------------------------------------------
Alternate ilead               0       0        150        0        0
Anti-Entropy stage            0       0        12         0        0
CompactionExecutor            2       0        856        0        12
Counter mutation stage        0       0        45         0        0
GossipStage                   0       0        1200       0        0
MemtableFlushWriter           1       0        234        0        0
MemtablePostFlush             0       0        156        0        0
MemtableReclaimMemory         0       0        123        0        0
Misc                           0       0        78         0        0
Mutation stage                0       0        4567       0        0
Read repair                    0       0        89         0        0
Replication on flush           0       0        234        0        0
RequestProcessor               0       1        8901       0        0
Response qualifier             0       0        7654       0        0
stage                         0       0        3456       0        0
hintedhandoff                  0       0        0          0        0
internal                       0       0        1234       0        0
memtable permissions flush     0       0        45         0        0
native-transport-0             2       0        89012      0        0
pending ranges                 0       0        12         0        0
readstage                      0       0        34567      0        0
rollback                      0       0        23         0        0
streaming st                   0       0        89         0        0
sync-Replicated                 0       0        456        0        0
```

**Campos clave:**

| Campo | Descripción |
|-------|-------------|
| **Active** | Hilos activos ahora mismo |
| **Pending** | Operaciones esperando un hilo |
| **Completed** | Total de operaciones completadas |
| **Blocked** | Hilos bloqueados esperando |
| **All time blocked** | Total de bloqueos históricos |

> **ALERTA**: Si `Pending` > 0 consistentemente o `Blocked` > 0, hay un cuello de botella.

#### nodetool cfstats (Column Family Stats)

Estadísticas detalladas de una tabla:

```bash
nodetool cfstats mi_keyspace.usuarios
```

```
Table: usuarios
Keyspace: mi_keyspace
Read Count: 123456
Read Latency: 2.345 ms
Write Count: 89012
Write Latency: 1.234 ms
Pending Flushes: 0
SSTables in each level:
  [0]: 0
  [1]: 4
  [2]: 2
  [3]: 1
Space used (live): 1073741824
Space used (total): 1288490188
Space used by snapshots: 0
Space used by tombstones: 1048576

Compacted partition minimum bytes: 128
Compacted partition maximum bytes: 65536
Compacted partition mean bytes: 2048

Number of keys (estimate): 1000000
MemTable cell count: 25000
MemTable data size: 2097152
MemTable off heap data size: 0
MemTable switch count: 12
Local read count: 123456
Local read latency: 2.345 ms
Local write count: 89012
Local write latency: 1.234 ms

Bloom filter false positives: 234
Bloom filter false ratio: 0.0012
Bloom filter space used: 1048576

Tombstone scanned rows: 1234
Tombstone limit: 100000
Tombstone warn threshold: 10000
```

**Métricas importantes:**

| Métrica | Descripción | Valor Ideal |
|---------|-------------|-------------|
| **Read Latency** | Latencia promedio de lectura | < 10ms |
| **Write Latency** | Latencia promedio de escritura | < 5ms |
| **SSTables per level** | SSTables por nivel de compaction | 0 en L0 |
| **Bloom filter false ratio** | Falsos positivos del Bloom Filter | < 0.01 |
| **Tombstone scanned rows** | Filas escaneadas por tombstones | < 1000 |
| **Pending Flushes** | Flushes pendientes | 0 |

#### nodetool repair

Reparación anti-entropy:

```bash
# Repair completo de un keyspace
nodetool repair mi_keyspace

# Repair con opciones
nodetool repair -pr mi_keyspace  # Primary range only (más rápido)
nodetool repair --full mi_keyspace  # Reparación completa

# Repair de una tabla específica
nodetool repair mi_keyspace usuarios

# Repair con parallelism
nodetool repair -par parallel mi_keyspace  # Paralelo (default)
nodetool repair -par dclocal mi_keyspace  # Local DC only
nodetool repair -par sequential mi_keyspace  # Secuencial
```

**Opciones importantes de repair:**

| Opción | Descripción |
|--------|-------------|
| `-pr` | Solo primary range (más rápido) |
| `--full` | Reparación completa (no incremental) |
| `-par parallel` | Repair paralelo (default) |
| `-par dclocal` | Solo local DC |
| `-st / -et` | Start/End token range |

#### nodetool cleanup

Elimina datos que ya no pertenecen a este nodo después de quitar nodos:

```bash
# Cleanup de todo el cluster
nodetool cleanup

# Cleanup de un keyspace específico
nodetool cleanup mi_keyspace

# Cleanup de una tabla específica
nodetool cleanup mi_keyspace usuarios
```

> **IMPORTANTE**: Ejecutar cleanup **después** de decommission o remove para liberar espacio.

#### nodetool compact

Forzar compaction manual:

```bash
# Compaction de toda la tabla
nodetool compact mi_keyspace usuarios

# Compaction de un keyspace completo
nodetool compact mi_keyspace

# Forzar compaction con tamaño específico
nodetool compact -st <start_token> -et <end_token> mi_keyspace usuarios
```

> **PRECAUCIÓN**: No forzar compaction en producción sin necesidad. La compaction automática es generalmente suficiente.

#### nodetool flush

Forzar flush de Memtable a SSTable:

```bash
# Flush de todo el nodo
nodetool flush

# Flush de un keyspace
nodetool flush mi_keyspace

# Flush de una tabla específica
nodetool flush mi_keyspace usuarios
```

**Cuándo usar flush:**
- Antes de hacer backup (asegurar que los datos estén en disco)
- Antes de un restart del nodo
- Antes de upgrade de Cassandra

#### nodetool drain

Detiene todas las escrituras entrantes y espera a que se completen las existentes:

```bash
nodetool drain
```

**Flujo del drain:**
```
1. Detiene接收 nuevas escrituras CQL
2. Cierra el native transport (CQL client connections)
3. Espera a que se completen todas las operaciones pendientes
4. Hace flush de todos los memtables a disco
5. Nodo listo para shutdown seguro
```

> **IMPORTANTE**: Siempre ejecutar `nodetool drain` antes de `nodetool stop` o `systemctl stop cassandra`.

#### nodetool snapshot

Crear snapshot (backup) de datos:

```bash
# Snapshot de un keyspace
nodetool snapshot mi_keyspace

# Snapshot con nombre personalizado
nodetool snapshot -t backup_2024_01_15 mi_keyspace

# Snapshot de una tabla específica
nodetool snapshot -t backup_tabla mi_keyspace usuarios

# Snapshot de todas las tablas
nodetool snapshot -t full_backup
```

**Directorio del snapshot:**
```
/var/lib/cassandra/data/<keyspace>/<table>-<uuid>/snapshots/<snapshot_name>/
```

#### nodetool listsnapshots

Listar todos los snapshots existentes:

```bash
nodetool listsnapshots
```

```
Snapshot name  Keyspace name  Column family name  True size  Size on disk
backup_2024_01_15  mi_keyspace  usuarios           256.12 MiB  128.06 MiB
backup_2024_01_14  mi_keyspace  usuarios           248.00 MiB  124.00 MiB
full_backup         mi_keyspace  (all)              512.00 MiB  256.00 MiB
```

#### nodetool clearsnapshot

Eliminar snapshots:

```bash
# Eliminar un snapshot específico
nodetool clearsnapshot -t backup_2024_01_15 mi_keyspace

# Eliminar todos los snapshots de un keyspace
nodetool clearsnapshot mi_keyspace

# Eliminar todos los snapshots del nodo
nodetool clearsnapshot
```

#### nodetool disablegossip / enablegossip

Controlar el protocolo gossip:

```bash
# Deshabilitar gossip (el nodo aparecerá como Down para otros)
nodetool disablegossip

# Habilitar gossip
nodetool enablegossip
```

> **USO**: Principalmente para mantenimiento o debugging. Nunca deshabilitar gossip en producción sin planificación.

#### nodetool disablebinary / enablebinary

Controlar el native transport (CQL):

```bash
# Deshabilitar CQL connections
nodetool disablebinary

# Habilitar CQL connections
nodetool enablebinary
```

#### nodetool decommission

Retirar un nodo del cluster:

```bash
# Verificar estado primero
nodetool status

# Decommissar el nodo
# IMPORTANTE: Solo ejecutar en el nodo que se va a retirar
nodetool decommission
```

**Proceso de decommission:**
```
1. El nodo deja de recibir nuevas lecturas/escrituras
2. Migra todas sus particiones a otros nodos
3. Se retira del gossip ring
4. El nodo se apaga automáticamente
5. Los demás nodos redistribuyen los datos
```

#### nodetool assassinate (Debug)

Fuerza la eliminación de un nodo del cluster (uso de emergencia):

```bash
# SOLO cuando el nodo está permanently Down
# y no se puede hacer decommission
nodetool assassinate 10.0.0.3
```

> **PELIGRO**: `assassinate` puede causar pérdida de datos si el nodo tiene datos únicos. Usar solo como último recurso.

### 1.2 Monitoreo

#### Métricas JMX (Puerto 7199)

Cassandra expone métricas vía JMX en el puerto 7199:

```yaml
# cassandra.yaml
jmx_port: 7199
```

**Métricas JMX principales:**

| MBean | Descripción |
|-------|-------------|
| `org.apache.cassandra.metrics:type=ClientRequest` | Latencia y throughput de client requests |
| `org.apache.cassandra.metrics:type=Storage` | Operaciones de storage |
| `org.apache.cassandra.metrics:type=ThreadPools` | Estados de thread pools |
| `org.apache.cassandra.metrics:type=Compaction` | Progreso de compaction |
| `org.apache.cassandra.metrics:type=Caches` | Hit rates de caches |
| `org.apache.cassandra.metrics:type=Net` | Métricas de red |

**Acceso con jmxterm:**
```bash
# Conectar a JMX
java -jar jmxterm.jar -l localhost:7199

# Listar MBeans
> domain org.apache.cassandra.metrics
> get -b org.apache.cassandra.metrics:type=Storage,scope=Read,name=Latency
```

#### Prometheus + Grafana

**cassandra-exporter para Prometheus:**

```yaml
# docker-compose.yml para monitoring stack
version: '3.8'
services:
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml

  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin

  cassandra-exporter:
    image: promjmx/jmx_prometheus_javaagent
    ports:
      - "8080:8080"
    volumes:
      - ./config.yml:/config.yml
    command: ["-javaagent:/opt/jmx_prometheus_javaagent.jar=8080:/config.yml"]
```

**prometheus.yml:**
```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'cassandra'
    static_configs:
      - targets: ['cassandra:8080']
    metrics_path: '/metrics'
```

**cassandra-exporter config.yml:**
```yaml
rules:
  # Latencia de lectura
  - pattern: "org.apache.cassandra.metrics<type=(ClientRequest), scope=(Read), name=(Latency)><>(\\w+)"
    name: "cassandra_read_latency_$4"
    help: "Cassandra read latency"
    type: GAUGE

  # Latencia de escritura
  - pattern: "org.apache.cassandra.metrics<type=(ClientRequest), scope=(Write), name=(Latency)><>(\\w+)"
    name: "cassandra_write_latency_$4"
    help: "Cassandra write latency"
    type: GAUGE

  # Pending tasks
  - pattern: "org.apache.cassandra.metrics<type=(ThreadPools), scope=(.*), name=(PendingTasks)><>(\\w+)"
    name: "cassandra_thread_pool_pending_$2"
    help: "Cassandra thread pool pending tasks"
    type: GAUGE

  # Compaction pending
  - pattern: "org.apache.cassandra.metrics<type=(Compaction), name=(PendingTasks)><>(\\w+)"
    name: "cassandra_compaction_pending_$2"
    help: "Cassandra compaction pending tasks"
    type: GAUGE
```

**Grafana Dashboard IDs para Cassandra:**
- Dashboard principal: `12062`
- Compaction monitoring: `13968`
- Performance: `12497`

#### Alarmas y Alertas

**Prometheus alert rules:**
```yaml
groups:
  - name: cassandra-alerts
    rules:
      - alert: CassandraNodeDown
        expr: cassandra_up == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Nodo Cassandra caído"

      - alert: CassandraHighReadLatency
        expr: cassandra_read_latency_mean > 0.01
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Latencia de lectura alta: {{ $value }}s"

      - alert: CassandraCompactionPending
        expr: cassandra_compaction_pending_tasks > 10
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "Compaction pendiente: {{ $value }} tareas"

      - alert: CassandraHighHeapUsage
        expr: cassandra_heap_memory_used_bytes / cassandra_heap_memory_max_bytes > 0.85
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Heap usage alto: {{ $value | humanizePercentage }}"
```

#### Métricas Importantes a Monitorear

| Categoría | Métrica | Umbral Crítico |
|-----------|---------|---------------|
| **Latencia** | Read Latency (p99) | > 50ms |
| **Latencia** | Write Latency (p99) | > 25ms |
| **Throughput** | Read operations/sec | Monitorear tendencia |
| **Throughput** | Write operations/sec | Monitorear tendencia |
| **Compaction** | Pending tasks | > 20 |
| **Compaction** | Compaction throughput | < 64MB/s |
| **Memoria** | Heap usage | > 85% |
| **Memoria** | Off-heap usage | > 90% |
| **Thread Pools** | Pending tasks | > 0 por más de 5 min |
| **Thread Pools** | Blocked tasks | > 0 |
| **Disco** | Disk usage | > 75% |
| **Red** | Dropped messages | > 0 |
| **Gossip** | Suspended gossip | > 0 |

---

## 2. Mantenimiento

### 2.1 Repair Periódico

El repair es la operación de mantenimiento más crítica en Cassandra.

#### ¿Por qué es necesario?

Cassandra usa **anti-entropy repair** para sincronizar datos entre nodos. Sin repair regular:
- Los datos pueden quedarse inconsistentes entre nodos
- Los **tombstones** pueden "resucitar" después de `gc_grace_seconds`
- Los fallos de replicación no se detectan

```
gc_grace_seconds = 864000 (10 días por defecto)

Si no haces repair en 10 días:
  Nodo A: DELETE FROM tabla WHERE id = 1 (ts=100)
  Nodo B: Nunca recibió el DELETE
  Después de gc_grace: el tombstone se purga de Nodo A
  Resultado: Nodo B todavía tiene el dato → "resurrección"
```

#### Tipos de Repair

| Tipo | Descripción | Cuándo usar |
|------|-------------|-------------|
| **Incremental** | Repara solo datos nuevos desde último repair | Repair regular (default) |
| **Full** | Repara todos los datos completamente | Primer repair o después de problemas |
| **Sequential** | Repara una partición a la vez | Menos resource-intensive |
| **Parallel** | Repara múltiples particiones en paralelo | Más rápido, más recursos |
| **DC-Local** | Solo repara dentro del datacenter local | Multi-DC, baja latencia cross-DC |

#### Mejores Prácticas de Repair

```bash
# 1. Ejecutar repair cada 7-10 días (menos que gc_grace_seconds)
# Programar en crontab
0 2 * * 0 /usr/bin/nodetool repair --full mi_keyspace >> /var/log/cassandra/repair.log 2>&1

# 2. Repair por keyspace
for keyspace in $(nodetool describecluster | grep -oP 'Keyspaces: \K.*' | tr ',' '\n'); do
    nodetool repair $keyspace
done

# 3. Usar -pr para repair más rápido (primary range only)
nodetool repair -pr mi_keyspace

# 4. Monitorear repair
nodetool netstats  # Ver progreso de streaming
```

### 2.2 Cleanup Después de Quitar Nodos

```bash
# Después de decommission, ejecutar cleanup en todos los nodos restantes
nodetool cleanup

# Cleanup específico
nodetool cleanup mi_keyspace

# Cleanup de una tabla
nodetool cleanup mi_keyspace usuarios

# Cleanup puede tomar tiempo con tablas grandes
# Monitorear con:
watch -n 10 nodetool compactionstats
```

### 2.3 Flush para Forzar Escritura a Disco

```bash
# Forzar flush de todos los memtables
nodetool flush

# Flush específico
nodetool flush mi_keyspace usuarios

# Flush antes de backup (CRÍTICO)
nodetool flush && nodetool snapshot -t backup_$(date +%Y%m%d) mi_keyspace
```

### 2.4 Scrub para Reparar SSTables Corruptos

```bash
# Scrub una tabla (reorganiza y repara SSTables)
nodetool scrub mi_keyspace usuarios

# Scrub con opciones
nodetool scrub -v mi_keyspace usuarios  # Verbose
nodetool scrub -r mi_keyspace usuarios  # Reconstruct
nodetool scrub --skip-corrupted mi_keyspace usuarios  # Saltar corruptos
```

> **NOTA**: Scrub es destructivo (crea nuevos SSTables y elimina los viejos). Hacer backup primero.

### 2.5 Upgrade SSTables

```bash
# Actualizar SSTables a formato de versión actual
nodetool upgradetables mi_keyspace usuarios

# Upgrade todas las tablas
nodetool upgradetables

# Verificar formato actual
ls -la /var/lib/cassandra/data/mi_keyspace/usuarios-*/nb-1-big-Data.db
```

### 2.6 Compactación Manual

```bash
# Forzar compaction (usar con precaución)
nodetool compact mi_keyspace usuarios

# Verificar progreso
nodetool compactionstats

# Ver tamaño de SSTables después
ls -lh /var/lib/cassandra/data/mi_keyspace/usuarios-*/nb-*-Data.db
```

---

## 3. Performance Tuning

### 3.1 Batch Size Limits

**REGLA DE ORO**: Nunca usar batches de más de **5KB**.

```sql
-- MAL (batch demasiado grande)
BEGIN BATCH
  INSERT INTO tabla (id, val) VALUES (1, 'a');
  INSERT INTO tabla (id, val) VALUES (2, 'b');
  -- ... miles de inserts
  INSERT INTO tabla (id, val) VALUES (10000, 'z');
APPLY BATCH;

-- BIEN (batch pequeño para operaciones atómicas)
BEGIN BATCH
  INSERT INTO cuentas (id, saldo) VALUES ('origen', 500);
  INSERT INTO cuentas (id, saldo) VALUES ('destino', 1500);
APPLY BATCH;

-- BIEN (usar un-loop para inserts masivos)
UNWIND [
  {id: uuid(), val: 'a'},
  {id: uuid(), val: 'b'},
  {id: uuid(), val: 'c'}
] AS row
CREATE (n:Node {id: row.id, val: row.val});
```

**¿Por qué?**
- Los batches en Cassandra son diferentes a SQL batches
- Un batch grande bloquea el coordinador
- Causa latencia y puede causar timeout

### 3.2 Compression

```yaml
# cassandra.yaml
compression:
  sstable_compression: LZ4Compressor  # Default, buen balance
  # sstable_compression: SnappyCompressor  # Rápido, menor ratio
  # sstable_compression: ZstdCompressor  # Mejor ratio, más CPU
```

| Algoritmo | Ratio | CPU | Latencia | Uso Recomendado |
|-----------|-------|-----|----------|-----------------|
| **LZ4** | Bueno | Bajo | Baja | Default, general |
| **Snappy** | Moderado | Muy Bajo | Muy Baja | Write-heavy |
| **Zstd** | Excelente | Medio | Media | Read-heavy, ahorro de disco |
| **None** | N/A | N/A | Muy Baja | Debugging (no recomendado) |

```sql
-- Configurar compresión en tabla
CREATE TABLE usuarios (
    id UUID PRIMARY KEY,
    nombre TEXT,
    email TEXT
) WITH compression = {
    'sstable_compression': 'ZstdCompressor',
    'chunk_length_in_kb': 16
};
```

### 3.3 Caching

#### Key Cache
Almacena partition keys → SSTable offsets. Reduce I/O para lookups.

```yaml
# cassandra.yaml
key_cache_size_in_mb: 5  # 5% del heap (default)
key_cache_save_period: 14400  # Segundos (4 horas)
key_cache_keys_to_save: 100  # por tabla
```

#### Row Cache
Almacena filas completas en memoria. **Generalmente NO recomendado.**

```yaml
# cassandra.yaml
row_cache_size_in_mb: 0  # Default: deshabilitado
```

> **NO usar row cache** excepto para datos completamente estáticos (tablas de referencia). Cada escritura invalida el row cache.

#### Counter Cache
Para tablas de contadores.

```yaml
# cassandra.yaml
counter_cache_size_in_mb: 5
```

### 3.4 Memtable Settings

```yaml
# cassandra.yaml
memtable_allocation_type: offheap_objects  # Mejor para GC
memtable_heap_space_in_mb: 2048
memtable_offheap_space_in_mb: 2048
memtable_cleanup_threshold: 0.11
```

### 3.5 Concurrent Reads/Writes

```yaml
# cassandra.yaml
concurrent_reads: 32  # 16 * número de discos
concurrent_writes: 32  # 8 * número de cores
concurrent_counter_writes: 32
concurrent_materialized_view_writes: 32
```

### 3.6 Heap Sizing (jvm.options)

```bash
# conf/jvm.options
-Xms8G    # Heap mínimo: 8GB
-Xmx8G    # Heap máximo: 8GB (mismo valor para evitar resizing)
```

**Reglas de tamaño de heap:**
- Máximo **8GB** para heap (más causa long GC pauses)
- Usar **off-heap** para memtables
- Dejar al menos **4GB** libre para OS page cache
- Si el nodo tiene 32GB RAM: 8GB heap + 4GB OS + 20GB page cache

### 3.7 GC Tuning (G1GC)

```bash
# conf/jvm.options (Cassandra 4.0+)
-XX:+UseG1GC
-XX:G1RSetUpdatingPauseTimePercent=5
-XX:MaxGCPauseMillis=300
-XX:InitiatingHeapOccupancyPercent=70
-XX:G1HeapRegionSize=16m
-XX:G1NewSizePercent=8
-XX:G1MaxNewSizePercent=12
```

**Monitoreo de GC:**
```bash
# Habilitar GC logging
-XX:+PrintGCDetails
-XX:+PrintGCDateStamps
-Xloggc:/var/log/cassandra/gc.log
```

---

## 4. Backups en Cassandra

### 4.1 Snapshot-Based Backups

Los backups en Cassandra se basan en **snapshots** del filesystem.

#### Crear Snapshot

```bash
# Snapshot de un keyspace completo
nodetool snapshot -t backup_2024_01_15 mi_keyspace

# Output:
# Snapshot directory: backup_2024_01_15
# /var/lib/cassandra/data/mi_keyspace/usuarios-uuid/snapshots/backup_2024_01_15/
# /var/lib/cassandra/data/mi_keyspace/productos-uuid/snapshots/backup_2024_01_15/
```

#### Estructura de Directorios del Snapshot

```
/var/lib/cassandra/data/
├── mi_keyspace/
│   ├── usuarios-<uuid>/
│   │   ├── snapshots/
│   │   │   └── backup_2024_01_15/
│   │   │       ├── nb-1-big-Data.db    # Datos SSTable
│   │   │       ├── nb-1-big-Index.db   # Partition index
│   │   │       ├── nb-1-big-Filter.db  # Bloom filter
│   │   │       ├── nb-1-big-CompressionInfo.db  # Compression info
│   │   │       ├── nb-1-big-Statistics.db  # Estadísticas
│   │   │       └── manifest.json
│   │   ├── nb-1-big-Data.db  # SSTable actual
│   │   └── ...
│   └── productos-<uuid>/
│       └── snapshots/
│           └── backup_2024_01_15/
│               └── ...
└── system/
    └── ...
```

#### Copiar Snapshot a Ubicación Segura

```bash
# Copiar a almacenamiento externo
SNAPSHOT_DIR="/var/lib/cassandra/data/mi_keyspace/usuarios-<uuid>/snapshots/backup_2024_01_15"
REMOTE_DIR="/backup/cassandra/2024/01/15"

# Copiar a servidor remoto
rsync -avz $SNAPSHOT_DIR/ user@backup-server:$REMOTE_DIR/

# Copiar a S3
aws s3 cp $SNAPSHOT_DIR/ s3://my-cassandra-backups/2024/01/15/mi_keyspace/usuarios/

# Copiar a GCS
gsutil -m cp -r $SNAPSHOT_DIR/ gs://my-cassandra-backups/2024/01/15/

# Copiar a Azure Blob
azcopy copy $SNAPSHOT_DIR/ https://myaccount.blob.core.windows.net/backups/2024/01/15/
```

### 4.2 Backup Strategy

```
Estrategia de Retención:
┌─────────────────────────────────────────────────────┐
│ Tipo         │ Frecuencia │ Retención │ Almacenamiento │
├──────────────┼────────────┼───────────┼───────────────│
│ Full Backup  │ Diario     │ 7 días    │ Disco local    │
│ Incremental  │ Cada hora  │ 24 horas  │ Disco local    │
│ Semanal      │ Domingo    │ 4 semanas │ S3/GCS        │
│ Mensual      │ 1er día    │ 12 meses  │ Glacier/Cold   │
└─────────────────────────────────────────────────────┘
```

### 4.3 Restore

#### Paso 1: Copiar Snapshot al Directorio de Datos

```bash
# En cada nodo del cluster
SNAPSHOT_PATH="/backup/cassandra/2024/01/15/mi_keyspace/usuarios"
DATA_PATH="/var/lib/cassandra/data/mi_keyspace/usuarios-<uuid>"

# Copiar archivos del snapshot
cp $SNAPSHOT_PATH/* $DATA_PATH/
```

#### Paso 2: Refrescar la Tabla

```bash
# Cassandra detecta los nuevos archivos
nodetool refresh mi_keyspace usuarios

# Verificar
nodetool cfstats mi_keyspace.usuarios
# Read Count should show data is accessible
```

#### Paso 3: Verificación Post-Restore

```sql
-- Verificar datos restaurados
SELECT COUNT(*) FROM mi_keyspace.usuarios;
SELECT * FROM mi_keyspace.usuarios LIMIT 10;

-- Verificar integridad
SELECT COUNT(*) FROM mi_keyspace.usuarios WHERE id IN (
    SELECT id FROM mi_keyspace.usuarios
);
```

### 4.4 Automatización con Scripts

#### Script de Backup Completo

```bash
#!/bin/bash
# backup_cassandra.sh
# Backup automatizado de Cassandra

set -e

# Configuración
KEYSPACES=("mi_keyspace" "otro_keyspace")
SNAPSHOT_NAME="backup_$(date +%Y%m%d_%H%M%S)"
REMOTE_BACKUP_DIR="/backup/cassandra"
CASSANDRA_HOST=$(hostname -I | awk '{print $1}')
LOG_FILE="/var/log/cassandra/backup.log"
RETENTION_DAYS=7

# Función de logging
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a $LOG_FILE
}

# Verificar que nodetool está disponible
if ! command -v nodetool &> /dev/null; then
    log "ERROR: nodetool no encontrado"
    exit 1
fi

# Flush antes del snapshot
log "Iniciando flush..."
nodetool flush
log "Flush completado"

# Crear snapshot para cada keyspace
for KEYSPACE in "${KEYSPACES[@]}"; do
    log "Creando snapshot para $KEYSPACE..."
    nodetool snapshot -t $SNAPSHOT_NAME $KEYSPACE
    log "Snapshot $SNAPSHOT_NAME creado para $KEYSPACE"
done

# Copiar snapshots a directorio remoto
for KEYSPACE in "${KEYSPACES[@]}"; do
    SNAPSHOT_BASE="/var/lib/cassandra/data/$KEYSPACE"
    for TABLE_DIR in $SNAPSHOT_BASE/*/snapshots/$SNAPSHOT_NAME; do
        if [ -d "$TABLE_DIR" ]; then
            TABLE_NAME=$(basename $(dirname $(dirname $TABLE_DIR)))
            DEST_DIR="$REMOTE_BACKUP_DIR/$SNAPSHOT_NAME/$KEYSPACE/$TABLE_NAME"
            mkdir -p $DEST_DIR
            cp -r $TABLE_DIR/* $DEST_DIR/
            log "Copiado $KEYSPACE/$TABLE_NAME a $DEST_DIR"
        fi
    done
done

# Backup a almacenamiento remoto (S3/GCS)
if command -v aws &> /dev/null; then
    log "Subiendo a S3..."
    aws s3 cp $REMOTE_BACKUP_DIR/$SNAPSHOT_NAME/ s3://my-cassandra-backups/$SNAPSHOT_NAME/ --recursive
    log "Upload a S3 completado"
fi

# Limpiar snapshots antiguos en Cassandra
log "Limpiando snapshots antiguos..."
for KEYSPACE in "${KEYSPACES[@]}"; do
    nodetool clearsnapshot -t $SNAPSHOT_NAME $KEYSPACE
done

# Limpiar backups antiguos
find $REMOTE_BACKUP_DIR -maxdepth 1 -type d -mtime +$RETENTION_DAYS -exec rm -rf {} \;
log "Limpieza completada"

log "Backup completado exitosamente: $SNAPSHOT_NAME"
```

#### Script de Restore

```bash
#!/bin/bash
# restore_cassandra.sh
# Restore de Cassandra desde snapshot

set -e

# Configuración
SNAPSHOT_NAME=$1
KEYSPACE=$2
TABLE=$3
CASSANDRA_DATA="/var/lib/cassandra/data"

if [ -z "$SNAPSHOT_NAME" ] || [ -z "$KEYSPACE" ] || [ -z "$TABLE" ]; then
    echo "Uso: $0 <snapshot_name> <keyspace> <table>"
    exit 1
fi

LOG_FILE="/var/log/cassandra/restore.log"
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a $LOG_FILE
}

# Verificar que el snapshot existe
SNAPSHOT_DIR="$CASSANDRA_DATA/$KEYSPACE/$TABLE"*/snapshots/$SNAPSHOT_NAME
if [ ! -d "$SNAPSHOT_DIR" ]; then
    log "ERROR: Snapshot no encontrado: $SNAPSHOT_DIR"
    exit 1
fi

# Obtener directorio de datos actual
TABLE_DIR=$(dirname $(dirname $SNAPSHOT_DIR))

# Copiar archivos del snapshot al directorio de datos
log "Copiando archivos del snapshot..."
for file in $SNAPSHOT_DIR/*; do
    if [ -f "$file" ]; then
        cp "$file" "$TABLE_DIR/"
        log "Copiado: $(basename $file)"
    fi
done

# Refrescar la tabla
log "Refrescando tabla..."
nodetool refresh $KEYSPACE $TABLE

# Verificar
log "Verificando datos restaurados..."
ROW_COUNT=$(cqlsh -e "SELECT COUNT(*) FROM $KEYSPACE.$TABLE;" | tail -1)
log "Filas restauradas: $ROW_COUNT"

log "Restore completado exitosamente"
```

#### Cron Job para Backups Automáticos

```bash
# crontab -e
# Backup diario a las 2:00 AM
0 2 * * * /opt/cassandra/scripts/backup_cassandra.sh >> /var/log/cassandra/backup_cron.log 2>&1

# Restore automático de testing (lunes a las 3:00 AM)
0 3 * * 1 /opt/cassandra/scripts/restore_cassandra.sh backup_$(date -d "yesterday" +%Y%m%d) mi_keyspace usuarios >> /var/log/cassandra/restore_cron.log 2>&1
```

### 4.5 Herramientas Externas

#### Medusa (Netflix Backup Tool)

```bash
# Instalar Medusa
pip install cassandra-medusa

# Configurar medusa.ini
cat > /etc/cassandra/medusa.ini << EOF
[storage]
storage_provider = s3
bucket_name = my-cassandra-backups
prefix = cassandra-backups
region = us-east-1

[cassandra]
root = /var/lib/cassandra
config_file = /etc/cassandra/cassandra.yaml
data_directories = /var/lib/cassandra/data
commitlog_directory = /var/lib/cassandra/commitlog
saved_caches_directory = /var/lib/cassandra/saved_caches

[ssh]
username = cassandra
key_file = /home/cassandra/.ssh/id_rsa

[checks]
heat = 1

[logging]
level = INFO
EOF

# Crear backup
medusa backup --backup-name backup_2024_01_15

# Listar backups
medusa list-backups

# Restore
medusa restore --backup-name backup_2024_01_15

# Restore específico
medusa restore-node --backup-name backup_2024_01_15 --host cassandra-node-1
```

### 4.6 Backups Cifrados con GPG

```bash
# Cifrar backup antes de subir a almacenamiento remoto
BACKUP_DIR="/backup/cassandra/backup_2024_01_15"

# Cifrar directorio completo
tar -czf - $BACKUP_DIR | gpg --symmetric --cipher-algo AES256 -o backup_2024_01_15.tar.gz.gpg

# Subir a S3 cifrado
aws s3 cp backup_2024_01_15.tar.gz.gpg s3://my-cassandra-backups/encrypted/

# Para restaurar: descifrar
gpg --decrypt backup_2024_01_15.tar.gz.gpg | tar -xzf -

# Programar en cron
0 2 * * * tar -czf - /backup/cassandra/latest | gpg --symmetric --cipher-algo AES256 --passphrase-file /root/.gpg_passphrase -o /backup/cassandra/encrypted/backup_$(date +\%Y\%m\%d).tar.gz.gpg
```

---

## 5. Seguridad de Cassandra

### 5.1 Autenticación

#### AllowAllAuthenticator (Default - INSEGURO)

```yaml
# cassandra.yaml
authenticator: AllowAllAuthenticator
```

Este modo permite **cualquier conexión sin autenticación**. Solo para desarrollo local.

#### PasswordAuthenticator

```yaml
# cassandra.yaml
authenticator: PasswordAuthenticator
```

**Requiere:**
1. Cambiar en cassandra.yaml
2. Reiniciar el nodo
3. Primera conexión con usuario default: `cassandra` / `cassandra`
4. Cambiar contraseña del usuario default
5. Crear nuevos usuarios

```sql
-- Conectar con credenciales default
cqlsh -u cassandra -p cassandra

-- Cambiar contraseña del usuario cassandra
ALTER ROLE cassandra WITH PASSWORD 'nueva_contraseña_segura_123!';

-- Crear nuevo usuario
CREATE ROLE usuario_app WITH PASSWORD 'app_password_456!' AND LOGIN = true;

-- Crear usuario con SuperUser
CREATE ROLE admin WITH PASSWORD 'admin_password_789!' AND LOGIN = true AND SUPERUSER = true;

-- Verificar roles
SELECT role, super, data_center, password_hash FROM system_auth.roles;
```

### 5.2 Autorización

#### CassandraAuthorizer

```yaml
# cassandra.yaml
authorizer: CassandraAuthorizer
```

```sql
-- Conceder permisos a nivel de keyspace
GRANT ALL ON KEYSPACE mi_keyspace TO usuario_app;

-- Conceder permisos de lectura
GRANT SELECT ON KEYSPACE mi_keyspace TO usuario_readonly;

-- Conceder permisos de escritura
GRANT INSERT, UPDATE ON KEYSPACE mi_keyspace TO usuario_write;

-- Conceder permisos a nivel de tabla
GRANT SELECT ON TABLE mi_keyspace.usuarios TO usuario_readonly;

-- Conceder permisos a nivel de columna
GRANT SELECT (nombre, email) ON TABLE mi_keyspace.usuarios TO usuario_limitado;

-- Revocar permisos
REVOKE ALL ON KEYSPACE mi_keyspace FROM usuario_app;

-- Ver permisos de un usuario
SHOW GRANTS FOR usuario_app;

-- Ver quién tiene permiso sobre un recurso
SELECT * FROM system_auth.role_permissions WHERE resource = 'keyspace mi_keyspace';
```

**Tabla de permisos:**

| Permiso | Descripción |
|---------|-------------|
| **CREATE** | Crear keyspace/tabla |
| **ALTER** | Modificar estructura |
| **DROP** | Eliminar keyspace/tabla |
| **SELECT** | Leer datos |
| **INSERT** | Insertar datos |
| **UPDATE** | Actualizar datos |
| **DELETE** | Eliminar datos |
| **TRUNCATE** | Vaciar tabla |
| **ALL** | Todos los permisos |
| **AUTHORIZE** | Conceder/revocar permisos |

### 5.3 Cifrado

#### Encryption in Transit (SSL/TLS)

**Generar certificados:**

```bash
# Generar CA (Certificate Authority)
openssl genrsa -out ca.key 4096
openssl req -new -x509 -days 365 -key ca.key -out ca.crt \
    -subj "/C=US/ST=State/L=City/O=Org/CN=Cassandra CA"

# Generar certificado del servidor
openssl genrsa -out node.key 2048
openssl req -new -key node.key -out node.csr \
    -subj "/C=US/ST=State/L=City/O=Org/CN=cassandra-node1"
openssl x509 -req -days 365 -in node.csr -CA ca.crt -CAkey ca.key \
    -CAcreateserial -out node.crt

# Generar keystore y truststore para Java
keytool -import -alias cassandra-ca -file ca.crt -keystore truststore.jks \
    -storepass truststore_password -noprompt

keytool -import -alias node -file node.crt -key node.key \
    -keystore keystore.jks -storepass keystore_password
```

**Configurar en cassandra.yaml:**

```yaml
# Inter-nodo encryption (entre nodos del cluster)
server_encryption_options:
    internode_encryption: all
    keystore: /etc/cassandra/keystore.jks
    keystore_password: keystore_password
    truststore: /etc/cassandra/truststore.jks
    truststore_password: truststore_password
    client_auth: optional  # or required

# Client encryption (entre cliente y Cassandra)
client_encryption_options:
    enabled: true
    keystore: /etc/cassandra/keystore.jks
    keystore_password: keystore_password
    truststore: /etc/cassandra/truststore.jks
    truststore_password: truststore_password
    client_auth: optional  # or required para mutual TLS
    protocol: TLSv1.2
    algorithm: SunX509
```

**Conectar con SSL:**

```bash
# cqlsh con SSL
cqlsh --ssl -u usuario -p password

# Con archivos de certificado
CQLSH_NO_BUNDLED_CERTS=true SSL_CERTFILE=ca.crt cqlsh --ssl
```

#### Encryption at Rest

```bash
# Opción 1: Cifrado a nivel de SO (LUKS en Linux)
# Crear volumen cifrado
cryptsetup luksFormat /dev/sdb
cryptsetup luksOpen /dev/sdb cassandra_encrypted
mkfs.ext4 /dev/mapper/cassandra_encrypted
mount /dev/mapper/cassandra_encrypted /var/lib/cassandra

# Opción 2: Cassandra Enterprise - Transparent Data Encryption (TDE)
# Solo disponible en versión Enterprise de DataStax
```

### 5.4 Seguridad de Red

#### Firewall Rules

```bash
# UFW (Ubuntu)
# Puertos de Cassandra
ufw allow from 10.0.0.0/24 to any port 9042  # CQL native
ufw allow from 10.0.0.0/24 to any port 7000  # Inter-node (cluster)
ufw allow from 10.0.0.0/24 to any port 7001  # Inter-node SSL
ufw allow from 10.0.0.0/24 to any port 7199  # JMX (restringir)
ufw deny 7199  # Bloquear JMX desde fuera

# iptables
iptables -A INPUT -p tcp --dport 9042 -s 10.0.0.0/24 -j ACCEPT
iptables -A INPUT -p tcp --dport 7000 -s 10.0.0.0/24 -j ACCEPT
iptables -A INPUT -p tcp --dport 7199 -j DROP
```

#### JMX Security

```yaml
# cassandra-env.sh
LOCAL_JMX=yes  # Solo escuchar en localhost

# Si se necesita JMX remoto:
# Habilitar autenticación JMX
-Dcom.sun.management.jmxremote.authenticate=true
-Dcom.sun.management.jmxremote.password.file=/etc/cassandra/jmxremote.password
-Dcom.sun.management.jmxremote.access.file=/etc/cassandra/jmxremote.access

# Habilitar SSL para JMX
-Dcom.sun.management.jmxremote.ssl=true
-Dcom.sun.management.jmxremote.ssl.need.client.auth=true
```

**Archivos de configuración JMX:**

```
# jmxremote.password
cassandraadmin strongpassword123!

# jmxremote.access
cassandraadmin readwrite
monitor readonly
```

### 5.5 Auditoría

#### Audit Logging

```yaml
# cassandra.yaml (Cassandra 4.0+)
audit_logging_options:
    enabled: true
    logger: FileAuditLogger  # o CassandraAuditLogger
    archive_dir: /var/log/cassandra/audit/
    log_dir: /var/log/cassandra/audit/
    block: false  # Si true, bloquea operaciones no autorizadas
    predicates: [DROP, MODIFY, CREATE, GRANT]  # Qué eventos auditar
    excluded_keyspaces: [system, system_auth]
```

**Formato de log de auditoría:**
```
2024-01-15 10:30:00 | EXECUTE | cassandra | /10.0.0.1 | SELECT * FROM mi_keyspace.usuarios WHERE id = ?
2024-01-15 10:30:01 | MODIFY | usuario_app | /10.0.0.2 | INSERT INTO mi_keyspace.usuarios ...
2024-01-15 10:30:02 | ERROR | usuario_bad | /10.0.0.99 | GRANT ALL ON KEYSPACE system TO baduser
```

### 5.6 Hardening

#### Deshabilitar JMX Remoto

```bash
# cassandra-env.sh
LOCAL_JMX=yes

# Si LOCAL_JMX=yes, JMX solo escucha en 127.0.0.1
# No se puede acceder desde fuera del nodo
```

#### Non-root User

```bash
# Cassandra NO debe correr como root
# Crear usuario dedicado
useradd -r -m -d /var/lib/cassandra -s /bin/bash cassandra
chown -R cassandra:cassandra /var/lib/cassandra
chown -R cassandra:cassandra /etc/cassandra
chown -R cassandra:cassandra /var/log/cassandra

# Iniciar como usuario cassandra
su - cassandra -c "cassandra -R"
```

#### Proteger Archivos de Configuración

```bash
# Permisos de cassandra.yaml
chmod 600 /etc/cassandra/cassandra.yaml
chown cassandra:cassandra /etc/cassandra/cassandra.yaml

# Permisos de keystores
chmod 600 /etc/cassandra/keystore.jks
chmod 600 /etc/cassandra/truststore.jks
chown cassandra:cassandra /etc/cassandra/*.jks
```

---

## 6. Ejercicio Práctico

### Ejercicio 1: Configurar Cluster de 3 Nodos con Docker

```bash
# Crear docker-compose.yml
cat > docker-compose.yml << 'EOF'
version: '3.8'
services:
  cassandra1:
    image: cassandra:4.1
    container_name: cass1
    ports:
      - "9041:9042"
      - "7191:7199"
    environment:
      - CASSANDRA_CLUSTER_NAME=MiCluster
      - CASSANDRA_DC=DC1
      - CASSANDRA_RACK=rack1
      - CASSANDRA_ENDPOINT_SNITCH=GossipingPropertyFileSnitch
      - CASSANDRA_NUM_TOKENS=256
    volumes:
      - cassandra1_data:/var/lib/cassandra
    networks:
      - cass-net

  cassandra2:
    image: cassandra:4.1
    container_name: cass2
    ports:
      - "9042:9042"
    environment:
      - CASSANDRA_CLUSTER_NAME=MiCluster
      - CASSANDRA_DC=DC1
      - CASSANDRA_RACK=rack1
      - CASSANDRA_ENDPOINT_SNITCH=GossipingPropertyFileSnitch
      - CASSANDRA_NUM_TOKENS=256
      - CASSANDRA_SEEDS=cass1
    depends_on:
      - cassandra1
    volumes:
      - cassandra2_data:/var/lib/cassandra
    networks:
      - cass-net

  cassandra3:
    image: cassandra:4.1
    container_name: cass3
    ports:
      - "9043:9042"
    environment:
      - CASSANDRA_CLUSTER_NAME=MiCluster
      - CASSANDRA_DC=DC1
      - CASSANDRA_RACK=rack1
      - CASSANDRA_ENDPOINT_SNITCH=GossipingPropertyFileSnitch
      - CASSANDRA_NUM_TOKENS=256
      - CASSANDRA_SEEDS=cass1
    depends_on:
      - cassandra1
    volumes:
      - cassandra3_data:/var/lib/cassandra
    networks:
      - cass-net

volumes:
  cassandra1_data:
  cassandra2_data:
  cassandra3_data:

networks:
  cass-net:
    driver: bridge
EOF

# Iniciar cluster
docker-compose up -d

# Esperar a que esté listo (~60 segundos)
docker exec -it cass1 nodetool status
```

### Ejercicio 2: Configurar PasswordAuthenticator

```bash
# Modificar cassandra.yaml en cada nodo
# Para Docker:
docker exec -it cass1 bash -c "
  sed -i 's/authenticator: AllowAllAuthenticator/authenticator: PasswordAuthenticator/' /etc/cassandra/cassandra.yaml
"
docker exec -it cass2 bash -c "
  sed -i 's/authenticator: AllowAllAuthenticator/authenticator: PasswordAuthenticator/' /etc/cassandra/cassandra.yaml
"
docker exec -it cass3 bash -c "
  sed -i 's/authenticator: AllowAllAuthenticator/authenticator: PasswordAuthenticator/' /etc/cassandra/cassandra.yaml
"

# Reiniciar nodos uno por uno
docker restart cass1
sleep 30
docker restart cass2
sleep 30
docker restart cass3
sleep 30

# Conectar con credenciales default
docker exec -it cass1 cqlsh -u cassandra -p cassandra
```

```sql
-- Cambiar contraseña del usuario cassandra
ALTER ROLE cassandra WITH PASSWORD 'MiContraseñaSegura123!';

-- Crear usuario de aplicación
CREATE ROLE app_usuario WITH PASSWORD 'AppPass456!' AND LOGIN = true;

-- Crear usuario de solo lectura
CREATE ROLE solo_lectura WITH PASSWORD 'ReadOnly789!' AND LOGIN = true;
```

### Ejercicio 3: Crear Usuarios con Diferentes Permisos

```sql
-- Conectar como cassandra
cqlsh -u cassandra -p 'MiContraseñaSegura123!'

-- Crear keyspace de prueba
CREATE KEYSPACE empresa WITH replication = {
    'class': 'SimpleStrategy',
    'replication_factor': 3
};

-- Crear tablas
CREATE TABLE empresa.empleados (
    id UUID PRIMARY KEY,
    nombre TEXT,
    departamento TEXT,
    salario DECIMAL
);

CREATE TABLE empresa.rrhh (
    id UUID PRIMARY KEY,
    empleado_id UUID,
    evaluacion TEXT,
    fecha DATE
);

-- Conceder permisos
-- app_usuario puede leer y escribir empleados
GRANT SELECT, INSERT, UPDATE ON TABLE empresa.empleados TO app_usuario;

-- solo_lectura solo puede leer
GRANT SELECT ON KEYSPACE empresa TO solo_lectura;

-- Crear usuario admin
CREATE ROLE admin_db WITH PASSWORD 'AdminPass!' AND LOGIN = true AND SUPERUSER = true;

-- Verificar permisos
SHOW GRANTS FOR app_usuario;
SHOW GRANTS FOR solo_lectura;

-- Probar permisos
-- Como solo_lectura (debería funcionar):
cqlsh -u solo_lectura -p 'ReadOnly789!'
SELECT * FROM empresa.empleados;  -- Funciona

-- Como app_usuario (debería funcionar):
cqlsh -u app_usuario -p 'AppPass456!'
INSERT INTO empresa.empleados (id, nombre, departamento, salario)
VALUES (uuid(), 'Juan', 'IT', 50000);  -- Funciona

-- Como solo_lectura (debería fallar):
cqlsh -u solo_lectura -p 'ReadOnly789!'
INSERT INTO empresa.empleados (id, nombre) VALUES (uuid(), 'Test');  -- Falla
```

### Ejercicio 4: Realizar Backup con nodetool snapshot

```bash
# 1. Flush para asegurar que los datos estén en disco
docker exec -it cass1 nodetool flush empresa

# 2. Crear snapshot
docker exec -it cass1 nodetool snapshot -t backup_ejercicio empresa

# 3. Verificar snapshot
docker exec -it cass1 nodetool listsnapshots

# 4. Ver archivos del snapshot
docker exec -it cass1 ls -la /var/lib/cassandra/data/empresa/empleados-*/snapshots/backup_ejercicio/

# 5. Copiar snapshot fuera del contenedor
docker cp cass1:/var/lib/cassandra/data/empresa/ /tmp/backup_empresa/
ls -la /tmp/backup_empresa/
```

### Ejercicio 5: Restaurar Backup

```bash
# 1. Eliminar datos (simular pérdida)
docker exec -it cass1 cqlsh -u cassandra -p 'MiContraseñaSegura123!' -e "
  TRUNCATE empresa.empleados;
"

# 2. Verificar que está vacía
docker exec -it cass1 cqlsh -u cassandra -p 'MiContraseñaSegura123!' -e "
  SELECT COUNT(*) FROM empresa.empleados;
"

# 3. Restaurar: copiar snapshot de vuelta al directorio de datos
docker exec -it cass1 bash -c "
  TABLE_DIR=\$(ls -d /var/lib/cassandra/data/empresa/empleados-*)
  SNAPSHOT_DIR=\$TABLE_DIR/snapshots/backup_ejercicio
  cp \$SNAPSHOT_DIR/* \$TABLE_DIR/
"

# 4. Refrescar
docker exec -it cass1 nodetool refresh empresa empleados

# 5. Verificar restauración
docker exec -it cass1 cqlsh -u cassandra -p 'MiContraseñaSegura123!' -e "
  SELECT COUNT(*) FROM empresa.empleados;
"
```

### Ejercicio 6: Script de Backup Automatizado

```bash
# Crear script
cat > /tmp/cassandra_backup.sh << 'SCRIPT'
#!/bin/bash
set -e

SNAPSHOT_NAME="auto_$(date +%Y%m%d_%H%M%S)"
CONTAINER="cass1"
KEYSPACE="empresa"
BACKUP_HOST_DIR="/tmp/cassandra_backups/$SNAPSHOT_NAME"

echo "$(date): Iniciando backup $SNAPSHOT_NAME"

# Flush
docker exec $CONTAINER nodetool flush $KEYSPACE

# Snapshot
docker exec $CONTAINER nodetool snapshot -t $SNAPSHOT_NAME $KEYSPACE

# Copiar fuera del contenedor
mkdir -p $BACKUP_HOST_DIR
docker cp $CONTAINER:/var/lib/cassandra/data/$KEYSPACE/ $BACKUP_HOST_DIR/

# Listar snapshots
docker exec $CONTAINER nodetool listsnapshots

# Limpiar snapshot local
docker exec $CONTAINER nodetool clearsnapshot -t $SNAPSHOT_NAME $KEYSPACE

echo "$(date): Backup completado: $BACKUP_HOST_DIR"
du -sh $BACKUP_HOST_DIR
SCRIPT

chmod +x /tmp/cassandra_backup.sh
/tmp/cassandra_backup.sh
```

### Ejercicio 7: Verificar Seguridad

```bash
# Verificar que JMX no está expuesto externamente
docker exec -it cass1 bash -c "netstat -tlnp | grep 7199"
# Debería mostrar solo 127.0.0.1:7199

# Verificar que CQL requiere autenticación
docker exec -it cass1 cqlsh  # Sin credenciales - debería fallar

# Verificar certificados SSL (si están configurados)
docker exec -it cass1 ls -la /etc/cassandra/*.jks

# Verificar permisos de archivos
docker exec -it cass1 ls -la /etc/cassandra/cassandra.yaml
# Debería mostrar permisos restrictivos

# Verificar usuario del proceso
docker exec -it cass1 ps aux | grep cassandra
# No debería mostrar root
```

---

## Resumen de la Clase 11

| Tema | Puntos Clave |
|------|-------------|
| **nodetool** | Herramienta principal de administración |
| **Mantenimiento** | Repair cada 7-10 días, cleanup después de cambios |
| **Performance** | Batches < 5KB, G1GC, off-heap memtables |
| **Backups** | Snapshots + copia externa + automatización |
| **Seguridad** | PasswordAuthenticator + CassandraAuthorizer + SSL |
| **Hardening** | Non-root, JMX local, firewall |

---

*Próxima clase: Neo4j I — Fundamentos, Cypher y Modelo de Grafos*
