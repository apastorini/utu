# Clase 02 — MongoDB I: Fundamentos, Instalacion y CRUD

> **Duracion estimada:** 5 horas  
> **Nivel:** Introductorio a Intermedio  
> **Requisitos previos:** Clase 01 completada, Docker instalado  
> **Objetivo:** Dominar la instalacion, configuracion, arquitectura y operaciones CRUD completas de MongoDB

---

## Indice

1. [Marco Teorico](#1-marco-teorico)
2. [Instalacion Paso a Paso](#2-instalacion-paso-a-paso)
3. [Arquitectura Detallada](#3-arquitectura-detallada)
4. [Conexion y Primeros Pasos](#4-conexion-y-primeros-pasos)
5. [CRUD Completo](#5-crud-completo)
6. [Seguridad Basica](#6-seguridad-basica)
7. [Ejercicio Practico](#7-ejercicio-practico)

---

## 1. Marco Teorico

### 1.1 Que es MongoDB? Filosofia y Diseno

MongoDB fue creado por **Dwight Merriman, Eliot Horowitz y Michael Dirolf** en 2007
bajo la empresa **10gen** (renombrada a MongoDB Inc. en 2013).
Fue liberado como open source en 2009 con la mision de construir una base de datos
que los desarrolladores amarian usar.

**Filosofia de diseno de MongoDB:**

```mermaid
graph TB
    subgraph "Filosofia MongoDB"
        D[Desarrollador primero]
        D --> F[Flexibilidad del esquema]
        D --> P[Performance alta]
        D --> S[Escalabilidad horizontal]
        D --> R[Developer Experience]

        F --> F1[Documentos JSON/BSON]
        F --> F2[Esquema dinamico]
        F --> F3[Embedding vs Referencing]

        P --> P1[WiredTiger Engine]
        P --> P2[Indices avanzados]
        P --> P3[Lock a nivel documento]

        S --> S1[Sharding automatico]
        S --> S2[Replicas]
        S --> S3[Multi-datacenter]

        R --> R1[Shell interactivo]
        R --> R2[Drivers en 12+ lenguajes]
        R --> R3[Compass GUI]
        R --> R4[Atlas cloud managed]
    end

    style D fill:#47a248,color:#fff
```

**Linea temporal de MongoDB:**

| Version | Ano | Caracteristicas principales |
|---------|-----|----------------------------|
| 1.0 | 2009 | Primera version estable |
| 2.0 | 2011 | Embedded documents, Indexes |
| 2.6 | 2014 | Aggregation framework mejorado |
| 3.0 | 2015 | WiredTiger engine (default), compresion |
| 3.2 | 2015 | Document validation, BI connector |
| 3.4 | 2016 | $lookup, read concern majority |
| 4.0 | 2018 | **Transacciones multi-document** |
| 4.2 | 2019 | Transacciones distribuidas |
| 5.0 | 2021 | Time series collections, Window functions |
| 6.0 | 2022 | Change streams mejorados, Encryption at rest |
| 7.0 | 2023 | Resharding, Versioned API, Range deletions |
| 8.0 | 2024 | 32x mas rapido en escrituras, Vector search GA |

### 1.2 Modelo de Datos: Documentos BSON, Colecciones, Bases de Datos

**Jerarquia de organizacion:**

```mermaid
graph TB
    subgraph "MongoDB Server - mongod"
        subgraph "Base de Datos: tienda"
            subgraph "Coleccion: productos"
                D1["Documento 1: _id, nombre, precio"]
                D2["Documento 2: _id, nombre, categorias"]
                D3["Documento 3: _id, nombre, specs"]
            end
            subgraph "Coleccion: clientes"
                D4["Documento 1: _id, nombre, email"]
                D5["Documento 2: _id, nombre, historial"]
            end
            subgraph "Coleccion: pedidos"
                D6["Documento 1: _id, cliente_id, items, total"]
                D7["Documento 2: _id, cliente_id, items, total"]
            end
        end
        subgraph "Base de Datos: admin"
            SA[Usuarios del sistema]
        end
        subgraph "Base de Datos: local"
            SL[Replication logs]
        end
    end
```

**Un documento es un par clave-valor donde:**
- Las claves son strings (UTF-8)
- Los valores pueden ser cualquier tipo de dato BSON
- Cada documento tiene un campo `_id` unico (ObjectId por defecto)
- No hay esquema fijo: documentos en la misma coleccion pueden tener campos diferentes

```javascript
// Ejemplo de documentos en una coleccion "productos"
// Documento 1: Laptop (estructura completa)
{
    "_id": ObjectId("64a7b3c9e1234567890abcde"),
    "nombre": "Laptop Pro X1",
    "marca": "TechBrand",
    "precio": 1299.99,
    "moneda": "USD",
    "stock": 25,
    "disponible": true,
    "especificaciones": {
        "procesador": "Intel Core i7-13700H",
        "ram_gb": 16,
        "almacenamiento": {
            "tipo": "NVMe SSD",
            "capacidad_gb": 512
        },
        "pantalla": {
            "pulgadas": 15.6,
            "resolucion": "2560x1440",
            "tipo_panel": "IPS",
            "frecuencia_hz": 165
        }
    },
    "categorias": ["laptops", "gaming", "profesional"],
    "etiquetas": ["oferta-verano", "nuevo-2024"],
    "opiniones": [
        {
            "usuario": "ana_tech",
            "rating": 5,
            "comentario": "Excelente rendimiento para programacion",
            "fecha": ISODate("2024-03-20T10:30:00Z")
        },
        {
            "usuario": "carlos_dev",
            "rating": 4,
            "comentario": "Buena pantalla, bateria mejorable",
            "fecha": ISODate("2024-04-15T14:20:00Z")
        }
    ],
    "fecha_creacion": ISODate("2024-03-15T00:00:00Z"),
    "fecha_actualizacion": ISODate("2024-08-01T12:00:00Z")
}

// Documento 2: Auriculares (estructura diferente)
{
    "_id": ObjectId("64a7b3c9e1234567890abcdf"),
    "nombre": "Auriculares Bluetooth Pro",
    "marca": "SoundMax",
    "precio": 79.99,
    "moneda": "USD",
    "stock": 150,
    "disponible": true,
    "categorias": ["audio", "bluetooth"],
    "fecha_creacion": ISODate("2024-06-01T00:00:00Z")
    // NOTA: este documento NO tiene especificaciones ni opiniones
    // Y esta perfecto! MongoDB no requiere campos iguales
}
```

### 1.3 BSON vs JSON (Diferencias Detalladas)

BSON (Binary JSON) es el formato de serializacion binario que MongoDB usa internamente.
JSON es el formato de representacion que los desarrolladores ven.

```mermaid
graph LR
    subgraph "JSON"
        J1[Texto plano]
        J2[Tipos: string, number, boolean, null, object, array]
        J3[Legible por humanos]
    end

    subgraph "BSON"
        B1[Formato binario]
        B2[Tipos: ObjectId, Date, Int32, Int64, Decimal128, Binary]
        B3[Parsing eficiente]
    end

    J1 -->|Serializar| B1
    B1 -->|Deserializar| J1
```

**Comparacion detallada:**

| Caracteristica | JSON | BSON |
|---------------|------|------|
| Formato | Texto (UTF-8) | Binario |
| Tipos de datos | 6 tipos | 12+ tipos |
| Date support | No (solo string) | Si BSON Date (64-bit ms) |
| Integer types | Solo number (float64) | Int32, Int64, Double |
| Decimal precision | No (float issues) | Si Decimal128 (128-bit) |
| Binary data | No | Si BinData type |
| ObjectId | No (solo string) | Si 12-byte nativo |
| Regex | No | Si BSON Regex |
| Tamano tipico | Mas grande (texto) | Mas compacto (binario) |
| Parsing | Mas lento | Mas rapido |

**Tipos BSON disponibles en MongoDB:**

```javascript
{
    "nombre": "Laptop Pro",                       // String
    "precio": 1299.99,                             // Double (number)
    "stock": NumberInt(25),                        // Int32
    "ventas_totales": NumberLong(1500000),         // Int64
    "impuesto": NumberDecimal("0.21"),             // Decimal128
    "disponible": true,                            // Boolean
    "descuento": null,                             // Null
    "fecha_lanzamiento": ISODate("2024-03-15"),   // Date
    "ts": Timestamp(1, 1693420800),               // Timestamp
    "_id": ObjectId("64a7b3c9e1234567890abcde"),  // ObjectId
    "categorias": ["laptops", "gaming"],           // Array
    "specs": {"ram": "16GB", "cpu": "i7"},        // Embedded Document
    "imagen": BinData(0, "SGVsbG8gV29ybGQ="),    // Binary Data
    "filtro": /laptop/i,                           // Regular Expression
    "min": MinKey(),                               // Min Key
    "max": MaxKey()                                // Max Key
}
```

**Limites de MongoDB:**

| Limite | Valor |
|--------|-------|
| Tamano maximo de documento | **16 MB** (BSON) |
| Profundidad maxima de nesting | **100 niveles** |
| Tamano maximo de clave | **255 bytes** |
| Tamano maximo de coleccion | Ilimitado |
| Tamano maximo de base de datos | Ilimitado |
| Indices por coleccion | **64** (default, configurable hasta 128) |

### 1.4 Motor WiredTiger: B-Tree, Compresion, Journaling

WiredTiger es el motor de almacenamiento default desde MongoDB 3.2.

```mermaid
graph TB
    subgraph "WiredTiger Storage Engine"
        APP[Aplicacion MongoDB]
        APP --> CACHE[Cache WiredTiger<br/>RAM 50% - 1GB]
        APP --> OPLOG[Oplog<br/>Replicacion]
        CACHE --> BTR[B-Tree Index<br/>en memoria]
        CACHE --> DOCS[Documents<br/>Working Set]
        BTR --> DISK[Disco Data Files<br/>snappy/zlib/zstd]
        DOCS --> DISK
        DISK --> JOURNAL[Journal WAL<br/>cada 100ms o 2MB]
        JOURNAL --> CHECKPOINT[Checkpoint<br/>cada 60 segundos]
    end

    style CACHE fill:#47a248,color:#fff
    style JOURNAL fill:#ff9800,color:#fff
    style CHECKPOINT fill:#2196f3,color:#fff
```

**Caracteristicas clave de WiredTiger:**

1. **Document-level locking:** Permite que multiples operaciones de escritura
   se ejecuten concurrentemente en documentos diferentes de la misma coleccion.
   Antes de WiredTiger (con MMAPv1), el bloqueo era a nivel de pagina o coleccion.

2. **Checkpoints:** Cada 60 segundos (o cuando se alcanza 2GB de datos en journal),
   WiredTiger escribe un checkpoint consistente con los datos en disco.

3. **Journal (Write-Ahead Logging):** Registra todas las escrituras antes de
   aplicarlas a los archivos de datos. Si el servidor falla, el journal permite
   recuperar los datos desde el ultimo checkpoint.

4. **Compresion:**
   - **snappy:** Compresion por defecto. Rapida, buena relacion compresion/velocidad.
   - **zlib:** Mayor compresion pero mas lenta. Usada para datos archivados.
   - **zstd:** Mezcla de ambos, disponible desde MongoDB 4.2.

```javascript
// Configurar compresion por coleccion
db.createCollection("logs", {
    storageEngine: {
        wiredTiger: {
            configString: "block_compressor=zstd"
        }
    }
});

// Ver compresion actual
db.adminCommand({ parameter: "wiredTigerCompressor" });
```

### 1.5 Comparacion Detallada con Bases Relacionales

| Caracteristica | MongoDB | MySQL/PostgreSQL |
|---------------|---------|------------------|
| **Modelo de datos** | Documentos (JSON/BSON) | Filas y columnas (tablas) |
| **Esquema** | Flexible (schema-on-read) | Rigido (schema-on-write) |
| **Lenguaje de consulta** | MQL | SQL estandar |
| **Relaciones** | Embedding o $lookup | JOIN nativo |
| **Escalabilidad** | Horizontal (sharding) | Vertical (principalmente) |
| **Transacciones** | Multi-document (desde 4.0) | Multi-table (nativo) |
| **Indices** | B-Tree, Hash, Geo, Text, TTL | B-Tree, Hash, GIN, GiST |
| **Motor** | WiredTiger | InnoDB, MyISAM, etc. |
| **Atomicidad** | A nivel de operacion | A nivel de transaccion |
| **Normalizacion** | Desnormalizacion (embedding) | Normalizacion (3NF) |
| **Tamano max doc** | 16 MB | 1 TB (PostgreSQL TOAST) |

---

## 2. Instalacion Paso a Paso

### 2.1 Windows: Instalacion con MSI Installer

**Paso 1: Descargar el instalador**

```powershell
# Descargar MongoDB Community Server 7.0 para Windows
# Ir a: https://www.mongodb.com/try/download/community
# Seleccionar: Version 7.0.x, OS: Windows, Package: MSI

# O descargar con PowerShell:
Invoke-WebRequest -Uri "https://fastdl.mongodb.org/windows/mongodb-windows-x86_64-7.0.x-signed.msi" -OutFile "$env:TEMP\mongodb-installer.msi"
```

**Paso 2: Ejecutar el instalador**

```powershell
Start-Process msiexec.exe -Wait -ArgumentList "/i $env:TEMP\mongodb-installer.msi /l*v $env:TEMP\mongodb-install.log"
```

En el asistente de instalacion:
1. **Welcome** - Next
2. **License Agreement** - Accept - Next
3. **Choose Setup Type:** Complete (recomendado)
4. **Service Configuration:** "Install MongoDB as a Service", Service Name: MongoDB
5. **Install Compass:** "Install MongoDB Compass" (recomendado)
6. **Ready to Install** - Install - Finish

**Paso 3: Configurar directorios**

```powershell
# Crear directorios de trabajo
New-Item -ItemType Directory -Force -Path "C:\data\db"
New-Item -ItemType Directory -Force -Path "C:\data\log"

# MongoDB se instalo en:
# C:\Program Files\MongoDB\Server\7.0\
# ├── bin\
# │   ├── mongod.exe        (servidor)
# │   ├── mongos.exe        (router de sharding)
# │   ├── mongosh.exe       (shell moderno)
# │   └── mongo.exe         (shell legacy)
# ├── conf\
# │   └── mongod.conf       (archivo de configuracion)
# └── logs\
```

**Paso 4: Configurar el servicio de Windows**

```powershell
# Verificar que MongoDB se instalo como servicio
Get-Service -Name "MongoDB"

# Si no se instalo como servicio, crearlo manualmente:
& "C:\Program Files\MongoDB\Server\7.0\bin\mongod.exe" `
    --dbpath "C:\data\db" `
    --logpath "C:\data\log\mongod.log" `
    --install `
    --serviceName "MongoDB"

# Iniciar el servicio
net start MongoDB

# Verificar que esta corriendo
Get-Service -Name "MongoDB" | Format-Table Name, Status
# Name    Status
# ----    ------
# MongoDB Running
```

**Paso 5: Verificar la instalacion**

```powershell
# Verificar version de mongod
& "C:\Program Files\MongoDB\Server\7.0\bin\mongod.exe" --version
# db version: v7.0.x

# Conectar con mongosh
& "C:\Program Files\MongoDB\Server\7.0\bin\mongosh.exe"
# test> db.version()
# '7.0.x'
# test> db.runCommand({ ping: 1 })
# { ok: 1 }
# test> exit
```

### 2.2 Linux Ubuntu/Debian: Instalacion con apt

**Paso 1: Importar la clave GPG**

```bash
curl -fsSL https://www.mongodb.org/static/pgp/server-7.0.asc | \
   sudo gpg -o /usr/share/keyrings/mongodb-server-7.0.gpg \
   --dearmor
```

**Paso 2: Agregar el repositorio**

```bash
# Para Ubuntu 22.04 (Jammy)
echo "deb [ signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | \
   sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list

# Para Ubuntu 24.04 (Noble), cambiar "jammy" por "noble"
# Para Debian 12 (Bookworm):
# echo "deb [ signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] https://repo.mongodb.org/apt/debian bookworm/mongodb-org/7.0 main" | \
#    sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list
```

**Paso 3: Actualizar e instalar**

```bash
sudo apt update
sudo apt install -y mongodb-org

# Esto instala:
# - mongodb-org-server    (mongod)
# - mongodb-org-mongos    (mongos)
# - mongodb-org-shell     (mongosh)
# - mongodb-org-tools     (mongodump, mongoexport, etc.)
```

**Paso 4: Configurar el servicio**

```bash
sudo mkdir -p /var/lib/mongo
sudo mkdir -p /var/log/mongodb
sudo chown -R mongodb:mongodb /var/lib/mongo
sudo chown -R mongodb:mongodb /var/log/mongodb

# Crear archivo de configuracion
sudo tee /etc/mongod.conf << 'EOF'
storage:
  dbPath: /var/lib/mongo
  journal:
    enabled: true
  wiredTiger:
    engineConfig:
      cacheSizeGB: 1
    collectionConfig:
      blockCompressor: snappy

systemLog:
  destination: file
  path: /var/log/mongodb/mongod.log
  logAppend: true
  logRotate: reopen

net:
  port: 27017
  bindIp: 127.0.0.1

processManagement:
  timeZoneInfo: /usr/share/zoneinfo
EOF

# Iniciar y habilitar el servicio
sudo systemctl start mongod
sudo systemctl enable mongod

# Verificar estado
sudo systemctl status mongod
# mongod.service - MongoDB Database Server
#      Active: active (running) since ...
#      Main PID: 12345 (mongod)
```

**Paso 5: Verificar**

```bash
mongod --version
# db version v7.0.x

mongosh
# test> db.version()
# '7.0.x'
# test> db.runCommand({ ping: 1 })
# { ok: 1 }
# test> exit
```

### 2.3 macOS: Homebrew

```bash
brew tap mongodb/brew
brew install mongodb-community@7.0
brew services start mongodb-community@7.0
mongosh --eval "db.version()"
```

### 2.4 Docker: Multiplataforma con Volumenes

```bash
# Linux/macOS
docker run -d \
  --name mongodb \
  -p 27017:27017 \
  -e MONGO_INITDB_ROOT_USERNAME=admin \
  -e MONGO_INITDB_ROOT_PASSWORD=admin123 \
  -v mongodb-data:/data/db \
  -v mongodb-config:/data/configdb \
  mongo:7.0

# Windows (PowerShell)
docker run -d `
  --name mongodb `
  -p 27017:27017 `
  -e MONGO_INITDB_ROOT_USERNAME=admin `
  -e MONGO_INITDB_ROOT_PASSWORD=admin123 `
  -v mongodb-data:/data/db `
  -v mongodb-config:/data/configdb `
  mongo:7.0
```

**Con docker-compose (recomendado para desarrollo):**

```yaml
version: '3.8'

services:
  mongodb:
    image: mongo:7.0
    container_name: mongodb
    ports:
      - "27017:27017"
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: admin123
      MONGO_INITDB_DATABASE: tienda
    volumes:
      - mongodb-data:/data/db
      - mongodb-config:/data/configdb
    command: --auth
    healthcheck:
      test: >
        mongosh -u admin -p admin123 --authenticationDatabase admin
        --eval "db.adminCommand('ping')" --quiet
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  mongodb-data:
  mongodb-config:
```

```bash
# Levantar
docker compose up -d

# Verificar
docker compose ps

# Conectar
docker exec -it mongodb mongosh -u admin -p admin123 --authenticationDatabase admin
```

### 2.5 Archivo mongod.conf COMPLETO Explicado Linea por Linea

```yaml
# ============================================================
# Archivo de configuracion: mongod.conf
# Linux: /etc/mongod.conf
# Windows: C:\Program Files\MongoDB\Server\7.0\bin\mongod.cfg
# ============================================================

# ----------------------------------------------------------
# STORAGE: Configuracion del motor de almacenamiento
# ----------------------------------------------------------
storage:
  # Directorio donde MongoDB almacena los datos
  dbPath: /var/lib/mongo

  # Habilitar journal para crash recovery
  journal:
    enabled: true

  # Motor de almacenamiento (default: wiredTiger)
  engine: wiredTiger

  # Configuracion de WiredTiger
  wiredTiger:
    engineConfig:
      # Tamano de cache en GB
      # Regla general: 50% de RAM menos 1GB menos tamano de indexes
      # Ejemplo: 16GB RAM -> (16 / 2) - 1 = 7GB
      cacheSizeGB: 7

      # Compresion de journal
      journalCompressor: snappy

      # Directorio para indices
      directoryForIndexes: false

    collectionConfig:
      # Compresion por defecto para colecciones
      # snappy: rapida (default)
      # zlib: mayor compresion, mas lenta
      # zstd: balance (desde MongoDB 4.2)
      blockCompressor: snappy

    indexConfig:
      prefixCompression: true

# ----------------------------------------------------------
# SYSTEMLOG: Configuracion de logs
# ----------------------------------------------------------
systemLog:
  destination: file
  path: /var/log/mongodb/mongod.log
  logAppend: true
  verbosity: 0
  logRotate: reopen
  component:
    accessControl:
      verbosity: 0
    command:
      verbosity: 0
    control:
      verbosity: 0
    storage:
      verbosity: 0
    write:
      verbosity: 0

# ----------------------------------------------------------
# NET: Configuracion de red
# ----------------------------------------------------------
net:
  port: 27017
  # 127.0.0.1 = solo localhost (seguro)
  # 0.0.0.0 = todas las interfaces (NO recomendado en produccion)
  # 192.168.1.100 = una IP especifica
  bindIp: 127.0.0.1
  maxIncomingConnections: 65536
  compression:
    compressors: snappy,zstd,zlib

  # TLS/SSL (recomendado en produccion)
  # tls:
  #   mode: requireTLS
  #   certificateKeyFile: /etc/ssl/mongo.pem
  #   CAFile: /etc/ssl/ca.pem

# ----------------------------------------------------------
# SECURITY: Configuracion de seguridad
# ----------------------------------------------------------
security:
  authorization: enabled
  # enableEncryption: true
  # encryptionKeyFile: /var/lib/mongo/keyfile

# ----------------------------------------------------------
# PROCESS MANAGEMENT: Gestion de procesos
# ----------------------------------------------------------
processManagement:
  timeZoneInfo: /usr/share/zoneinfo

# ----------------------------------------------------------
# OPERATION PROFILING: Analisis de consultas
# ----------------------------------------------------------
operationProfiling:
  mode: slowOp
  slowOpThresholdMs: 100
  slowOpSampleRate: 1.0

# ----------------------------------------------------------
# REPLICATION (opcional)
# ----------------------------------------------------------
# replication:
#   replSetName: rs0
#   oplogSizeMB: 2048

# ----------------------------------------------------------
# SHARDING (opcional)
# ----------------------------------------------------------
# sharding:
#   clusterRole: shardsvr
```

### 2.6 Verificacion de Instalacion

```bash
echo "=== Verificacion MongoDB ==="

# 1. Verificar que mongod esta corriendo
pgrep mongod && echo "mongod: CORRIENDO" || echo "mongod: DETENIDO"

# 2. Verificar version
mongod --version 2>/dev/null | head -1

# 3. Verificar puerto
netstat -tlnp 2>/dev/null | grep 27017 || ss -tlnp | grep 27017

# 4. Conectar y verificar
mongosh --eval "
  db.version();
  db.runCommand({ ping: 1 });
  db.serverStatus().host;
  db.serverStatus().mem;
" --quiet

# 5. Verificar base de datos admin
mongosh admin --eval "
  db.getUsers();
" --quiet
```

---

## 3. Arquitectura Detallada

### 3.1 Componentes de MongoDB

```mermaid
graph TB
    subgraph "Cliente"
        APP1[Aplicacion Node.js]
        APP2[Aplicacion Python]
        APP3[Aplicacion Java]
        CLI[mongosh CLI]
        GUI[MongoDB Compass]
    end

    subgraph "MongoDB Server - mongod"
        CONN[Capa de Conexiones<br/>Wire Protocol]
        QUERY[Query Engine<br/>Parser + Optimizer]
        WRITE[Write Engine<br/>BulkWrite]

        subgraph "Storage Engine: WiredTiger"
            CACHE[Cache WiredTiger<br/>Working Set]
            INDEX[B-Tree Indices]
            DOCS[Document Store]
            JOURNAL[Journal WAL]
        end

        OPLOG[Oplog<br/>Replication Log]
    end

    APP1 --> CONN
    APP2 --> CONN
    APP3 --> CONN
    CLI --> CONN
    GUI --> CONN
    CONN --> QUERY
    CONN --> WRITE
    QUERY --> CACHE
    WRITE --> CACHE
    CACHE --> INDEX
    CACHE --> DOCS
    CACHE --> JOURNAL
    WRITE --> OPLOG

    style CACHE fill:#47a248,color:#fff
    style JOURNAL fill:#ff9800,color:#fff
```

**mongod:** El daemon principal. Procesa peticiones del cliente, ejecuta consultas,
gestiona almacenamiento, y maneja replicacion.

**mongosh:** Shell interactivo moderno (reemplaza a mongo legacy). Soporta JavaScript,
autocompletado, formateo de salida.

**MongoDB Compass:** GUI grafica para explorar datos, crear indices, analizar
rendimiento de consultas.

**Drivers:** Bibliotecas para conectar desde Node.js, Python (PyMongo), Java, C#, Go, Rust, Ruby, PHP.

### 3.2 WiredTiger Engine (Detallado)

```mermaid
graph LR
    subgraph "Flujo de una escritura"
        W1["1. Cliente envia escritura"] --> W2["2. WiredTiger escribe en cache"]
        W2 --> W3["3. Se registra en journal WAL"]
        W3 --> W4["4. Se confirma al cliente"]
        W4 --> W5["5. Async: flush a disco en checkpoint"]
    end

    subgraph "Flujo de una lectura"
        R1["1. Cliente envia lectura"] --> R2["2. WiredTiger busca en cache"]
        R2 --> R3{"En cache?"}
        R3 -->|Si| R4["Retorna datos desde RAM"]
        R3 -->|No| R5["Carga desde disco a cache"]
        R5 --> R4
    end

    style W3 fill:#ff9800,color:#fff
    style R4 fill:#47a248,color:#fff
```

**Document-level locking:**

```
Operacion 1: UPDATE productos SET precio = 999 WHERE _id = "abc"
Operacion 2: UPDATE productos SET stock = 50 WHERE _id = "xyz"

Con WiredTiger (document-level lock):
  Op 1: bloquea SOLO documento abc
  Op 2: bloquea SOLO documento xyz
  => Ambas se ejecutan EN PARALELO

Con MMAPv1 (collection-level lock):
  Op 1: bloquea TODA la coleccion productos
  Op 2: ESPERA a que termine op 1
  => Secuencial, mucho mas lento
```

### 3.3 Modelo de Datos en Profundidad

**Documentos completos con todos los tipos BSON:**

```javascript
{
    "_id": ObjectId("507f1f77bcf86cd799439011"),
    "nombre": "Laptop Pro X1",
    "precio": NumberDecimal("1299.99"),
    "stock": NumberInt(25),
    "ventas_totales": NumberLong(1500000),
    "disponible": true,
    "descuento": null,
    "fecha": ISODate("2024-08-15T10:30:00Z"),
    "tags": ["gaming", "portatil"],
    "direccion": {
        "calle": "Av. Principal 123",
        "ciudad": "Madrid",
        "coordenadas": { "lat": 40.4168, "lng": -3.7038 }
    },
    "avatar": BinData(0, "aHR0cHM6Ly9..."),
    "busqueda": /laptop.*pro/i,
    "validador": function() { return this.stock > 0; }
}
```

**Tipos BSON completos:**

| Tipo BSON | Numero | Alias | Descripcion |
|-----------|--------|-------|-------------|
| Double | 1 | number | Float 64-bit |
| String | 2 | string | UTF-8 |
| Object | 3 | object | Documento embebido |
| Array | 4 | array | Arreglo |
| Binary | 5 | BinData | Datos binarios |
| ObjectId | 7 | ObjectId | 12-byte unico |
| Boolean | 8 | boolean | true/false |
| Date | 9 | Date | Fecha en ms |
| Null | 10 | null | Null |
| Regex | 11 | RegExp | Expresion regular |
| Code | 13 | Code | Codigo JavaScript |
| Int32 | 16 | Int32 | Entero 32-bit |
| Timestamp | 17 | Timestamp | Internal |
| Long | 18 | Long | Entero 64-bit |
| Decimal | 19 | Decimal128 | 128-bit decimal |
| MinKey | 255 | MinKey | Comparador min |
| MaxKey | 127 | MaxKey | Comparador max |

---

## 4. Conexion y Primeros Pasos

### 4.1 mongosh: Opciones de Conexion

```bash
# Conexion basica
mongosh

# Conexion con URI
mongosh "mongodb://localhost:27017"

# Conexion con autenticacion
mongosh "mongodb://admin:admin123@localhost:27017/admin"

# Conexion a base de datos especifica
mongosh "mongodb://localhost:27017/tienda"

# Conexion con replicas
mongosh "mongodb://user:pass@replica1:27017,replica2:27017,replica3:27017/?replicaSet=rs0"

# Opciones utiles
mongosh --quiet          # Sin banner inicial
mongosh --eval "db.version()"  # Ejecutar comando directo
mongosh --nodb           # Sin conectarse a ninguna base
```

### 4.2 Con Autenticacion y Sin Autenticacion

```javascript
// SIN autenticacion (solo para desarrollo local)
mongosh
// test> db.version()

// CON autenticacion
mongosh -u admin -p admin123 --authenticationDatabase admin
// Primary> use tienda
// tienda> db.collection.find()

// Verificar usuario actual
db.runCommand({ connectionStatus: 1 })
// {
//   authInfo: {
//     authenticatedUsers: [{ user: "admin", db: "admin" }]
//   },
//   ok: 1
// }
```

### 4.3 Crear Base de Datos y Colecciones

```javascript
// MongoDB crea la BD y coleccion implicitamente al insertar datos
use tienda

// Crear coleccion explicitamente
db.createCollection("productos")

// Ver colecciones
show collections

// Ver bases de datos
show dbs

// Ver detalles de la coleccion
db.productos.stats()
```

### 4.4 db.createCollection() con Opciones

```javascript
// Capped collection: tamano fijo, util para logs y metrics
db.createCollection("eventos_log", {
    capped: true,
    size: 10485760,    // 10 MB maximo total
    max: 50000         // 50,000 documentos maximo
});

// Con validacion de esquema
db.createCollection("usuarios", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["nombre", "email"],
            properties: {
                nombre: {
                    bsonType: "string",
                    description: "Nombre completo del usuario"
                },
                email: {
                    bsonType: "string",
                    pattern: "^.+@.+$",
                    description: "Email valido"
                },
                edad: {
                    bsonType: "int",
                    minimum: 0,
                    maximum: 150
                }
            }
        }
    },
    validationLevel: "moderate",
    validationAction: "error"
});
```

---

## 5. CRUD Completo

### 5.1 CREATE (Crear)

**insertOne():**

```javascript
use tienda;

// Insertar un solo documento
db.productos.insertOne({
    nombre: "Laptop Pro X1",
    marca: "TechBrand",
    precio: 1299.99,
    moneda: "USD",
    stock: 25,
    disponible: true,
    especificaciones: {
        procesador: "Intel Core i7-13700H",
        ram_gb: 16,
        almacenamiento: "512GB NVMe SSD"
    },
    categorias: ["laptops", "gaming", "profesional"],
    fecha_creacion: new Date()
});

// Resultado esperado:
// {
//   acknowledged: true,
//   insertedId: ObjectId("64a7b3c9e1234567890abcde")
// }

// Con _id especificado
db.productos.insertOne({
    _id: "prod_001",
    nombre: "Mouse Gamer RGB",
    precio: 49.99,
    stock: 100
});
// { acknowledged: true, insertedId: "prod_001" }
```

**insertMany():**

```javascript
// Insertar multiples documentos
db.productos.insertMany([
    {
        nombre: "Auriculares Bluetooth Pro",
        marca: "SoundMax",
        precio: 79.99,
        stock: 150,
        categorias: ["audio", "bluetooth"]
    },
    {
        nombre: "Tablet Air 10",
        marca: "TechBrand",
        precio: 599.99,
        stock: 40,
        categorias: ["tablets"]
    },
    {
        nombre: "Teclado Mecanico",
        marca: "KeyMaster",
        precio: 129.99,
        stock: 75,
        categorias: ["perifericos", "gaming"]
    },
    {
        nombre: "Monitor UltraWide 34",
        marca: "ViewPro",
        precio: 899.99,
        stock: 20,
        categorias: ["monitores"]
    },
    {
        nombre: "Webcam HD 1080p",
        marca: "ViewPro",
        precio: 89.99,
        stock: 200,
        categorias: ["perifericos"]
    },
    {
        nombre: "SSD Externo 1TB",
        marca: "StorageMax",
        precio: 119.99,
        stock: 60,
        categorias: ["almacenamiento"]
    },
    {
        nombre: "Cargador USB-C 100W",
        marca: "PowerTech",
        precio: 45.99,
        stock: 300,
        categorias: ["accesorios"]
    },
    {
        nombre: "Funda Laptop 15 pulgadas",
        marca: "CasePro",
        precio: 34.99,
        stock: 0,
        categorias: ["accesorios"]
    },
    {
        nombre: "Hub USB-C 7 puertos",
        marca: "PowerTech",
        precio: 59.99,
        stock: 45,
        categorias: ["accesorios", "perifericos"]
    },
    {
        nombre: "Parlante Bluetooth Portatil",
        marca: "SoundMax",
        precio: 69.99,
        stock: 80,
        categorias: ["audio", "portatil"]
    }
]);

// Resultado esperado:
// {
//   acknowledged: true,
//   insertedCount: 10,
//   insertedIds: {
//     0: ObjectId("..."),  1: ObjectId("..."),
//     ...
//     9: ObjectId("...")
//   }
// }
```

**bulkWrite():**

```javascript
// Operaciones mixtas en un solo comando
db.productos.bulkWrite([
    {
        insertOne: {
            document: {
                nombre: "Cable HDMI 4K 2m",
                precio: 12.99,
                stock: 500
            }
        }
    },
    {
        updateOne: {
            filter: { nombre: "Laptop Pro X1" },
            update: { $set: { stock: 24 } }
        }
    },
    {
        deleteOne: {
            filter: { nombre: "Funda Laptop 15 pulgadas" }
        }
    },
    {
        updateOne: {
            filter: { nombre: "Cable USB-C" },
            update: { $set: { nombre: "Cable USB-C", precio: 9.99, stock: 100 } },
            upsert: true
        }
    }
], { ordered: false });

// Resultado:
// {
//   acknowledged: true,
//   insertedCount: 1,
//   matchedCount: 1,
//   modifiedCount: 1,
//   deletedCount: 1,
//   upsertedCount: 1,
//   upsertedIds: { 3: ObjectId("...") }
// }
```

**Errores comunes:**

```javascript
// Error: duplicate key (_id duplicado)
db.productos.insertOne({ _id: "prod_001", nombre: "Duplicado" });
// MongoServerError: E11000 duplicate key error collection:
// tienda.productos index: _id_ dup key: { _id: "prod_001" }

// Error: validation failure
db.usuarios.insertOne({ nombre: "Ana" });
// MongoServerError: Document failed validation
// Requerido: "email" no esta presente

// Solucion: catch errors
try {
    db.productos.insertOne({ _id: "prod_001", nombre: "Duplicado" });
} catch (e) {
    if (e.code === 11000) {
        print("Documento duplicado, ignorando...");
    } else {
        throw e;
    }
}
```

### 5.2 READ (Leer)

**Operadores de comparacion:**

```javascript
// $eq: igual (operador por defecto)
db.productos.find({ precio: 1299.99 });
db.productos.find({ precio: { $eq: 1299.99 } });

// $ne: no igual
db.productos.find({ marca: { $ne: "TechBrand" } });

// $gt: mayor que
db.productos.find({ precio: { $gt: 500 } });

// $gte: mayor o igual que
db.productos.find({ precio: { $gte: 500 } });

// $lt: menor que
db.productos.find({ precio: { $lt: 100 } });

// $lte: menor o igual que
db.productos.find({ precio: { $lte: 50 } });

// $in: en la lista
db.productos.find({ marca: { $in: ["TechBrand", "SoundMax"] } });

// $nin: no en la lista
db.productos.find({ marca: { $nin: ["TechBrand"] } });

// $exists: campo existe/no existe
db.productos.find({ especificaciones: { $exists: true } });
db.productos.find({ especificaciones: { $exists: false } });

// $type: tipo del campo
db.productos.find({ precio: { $type: "double" } });
db.productos.find({ stock: { $type: "int" } });

// $regex: expresion regular
db.productos.find({ nombre: { $regex: /pro/i } });
db.productos.find({ nombre: { $regex: /^Laptop/ } });
db.productos.find({ nombre: { $regex: /bluetooth$/, $options: "i" } });

// $mod: modulo
db.productos.find({ stock: { $mod: [10, 0] } });  // stock divisible por 10

// Rangos: productos entre 100 y 500
db.productos.find({ precio: { $gte: 100, $lte: 500 } });

// Productos con stock > 0 Y precio < 200
db.productos.find({
    $and: [
        { stock: { $gt: 0 } },
        { precio: { $lt: 200 } }
    ]
});
```

**Operadores logicos:**

```javascript
// $and: ambas condiciones deben cumplirse
db.productos.find({
    $and: [
        { stock: { $gt: 0 } },
        { precio: { $lt: 100 } }
    ]
});

// $or: al menos una condicion
db.productos.find({
    $or: [
        { marca: "TechBrand" },
        { marca: "SoundMax" }
    ]
});

// $not: niega la condicion
db.productos.find({
    precio: { $not: { $gt: 500 } }
});

// $nor: ninguna condicion
db.productos.find({
    $nor: [
        { marca: "TechBrand" },
        { stock: { $gt: 100 } }
    ]
});
```

**Proyeccion de campos:**

```javascript
// Incluir solo campos especificos
db.productos.find({}, { nombre: 1, precio: 1 });
// { _id: ObjectId("..."), nombre: "Laptop Pro X1", precio: 1299.99 }

// Excluir campos
db.productos.find({}, { especificaciones: 0, fecha_creacion: 0 });

// Sin _id
db.productos.find({}, { _id: 0, nombre: 1, precio: 1 });

// Campos anidados
db.productos.find(
    { nombre: "Laptop Pro X1" },
    { "especificaciones.procesador": 1, "especificaciones.ram_gb": 1 }
);
```

**sort(), limit(), skip():**

```javascript
// Ascendente (1) o descendente (-1)
db.productos.find().sort({ precio: 1 });       // menor a mayor precio
db.productos.find().sort({ precio: -1 });      // mayor a menor precio
db.productos.find().sort({ precio: 1, nombre: 1 });

// Limitar resultados
db.productos.find().limit(5);

// Saltar (skip) - paginacion
db.productos.find().skip(5).limit(5);  // pagina 2

// ADVERTENCIA: skip grande es ineficiente
// skip(10000).limit(10) es muy lento
// Alternativa: cursor-based pagination
db.productos.find({ _id: { $gt: lastSeenId } }).limit(10);

// Combinar: top 3 productos mas caros
db.productos.find()
    .sort({ precio: -1 })
    .limit(3)
    .projection({ nombre: 1, precio: 1, _id: 0 });
// [
//   { nombre: "Laptop Pro X1", precio: 1299.99 },
//   { nombre: "Monitor UltraWide 34", precio: 899.99 },
//   { nombre: "Tablet Air 10", precio: 599.99 }
// ]
```

**countDocuments(), estimatedDocumentCount(), findOne():**

```javascript
// Contar documentos con filtro (preciso)
db.productos.countDocuments();
// 11

db.productos.countDocuments({ stock: { $gt: 0 } });
// 10

db.productos.countDocuments({ categorias: "gaming" });
// 2

// Estimado rapido (usa metadata del indice)
db.productos.estimatedDocumentCount();
// 11

// findOne: retorna un solo documento
db.productos.findOne({ nombre: "Laptop Pro X1" });
// { _id: ObjectId("..."), nombre: "Laptop Pro X1", ... }

db.productos.findOne(
    { precio: { $gt: 500 } },
    { nombre: 1, precio: 1 }
);
// { _id: ObjectId("..."), nombre: "Laptop Pro X1", precio: 1299.99 }
```

### 5.3 UPDATE (Actualizar)

**Operadores basicos:**

```javascript
// $set: establecer valor de campo
db.productos.updateOne(
    { nombre: "Laptop Pro X1" },
    { $set: { precio: 1199.99, stock: 30 } }
);
// { matchedCount: 1, modifiedCount: 1 }

// $unset: eliminar campo
db.productos.updateOne(
    { nombre: "Laptop Pro X1" },
    { $unset: { moneda: "" } }
);

// $inc: incrementar
db.productos.updateOne(
    { nombre: "Mouse Gamer RGB" },
    { $inc: { stock: -5 } }  // reducir stock en 5
);
db.productos.updateOne(
    { nombre: "Monitor UltraWide 34" },
    { $inc: { precio: 50 } }  // subir precio 50
);

// $mul: multiplicar
db.productos.updateOne(
    { nombre: "Monitor UltraWide 34" },
    { $mul: { precio: 1.10 } }  // subir precio 10%
);

// $min: actualizar solo si el nuevo valor es menor
db.productos.updateOne(
    { nombre: "Laptop Pro X1" },
    { $min: { precio: 1099.99 } }
);

// $max: actualizar solo si el nuevo valor es mayor
db.productos.updateOne(
    { nombre: "Laptop Pro X1" },
    { $max: { precio: 1399.99 } }
);

// $rename: renombrar campo
db.productos.updateMany(
    {},
    { $rename: { "fecha_creacion": "createdAt" } }
);

// $currentDate: establecer a la fecha actual
db.productos.updateOne(
    { nombre: "Laptop Pro X1" },
    { $currentDate: { updatedAt: true } }
);
```

**Operadores de array:**

```javascript
// $push: agregar elemento al array
db.productos.updateOne(
    { nombre: "Laptop Pro X1" },
    { $push: { etiquetas: "oferta-otono" } }
);

// $push con $each: agregar multiples elementos
db.productos.updateOne(
    { nombre: "Laptop Pro X1" },
    { $push: { etiquetas: { $each: ["nuevo-2024", "bestseller"] } } }
);

// $push con $slice: mantener solo los ultimos N elementos
db.productos.updateOne(
    { nombre: "Laptop Pro X1" },
    { $push: {
        etiquetas: {
            $each: ["tag1", "tag2", "tag3"],
            $slice: -5
        }
    }}
);

// $push con $sort: ordenar despues de insertar
db.productos.updateOne(
    { nombre: "Laptop Pro X1" },
    { $push: {
        opiniones: {
            $each: [{ usuario: "nuevo", rating: 5 }],
            $sort: { rating: -1 }
        }
    }}
);

// $push con $position: insertar en posicion especifica
db.productos.updateOne(
    { nombre: "Laptop Pro X1" },
    { $push: {
        etiquetas: {
            $each: ["urgente"],
            $position: 0
        }
    }}
);

// $pull: eliminar elementos que cumplen condicion
db.productos.updateOne(
    { nombre: "Laptop Pro X1" },
    { $pull: { etiquetas: "tag1" } }
);

// $pull con query
db.productos.updateOne(
    { nombre: "Laptop Pro X1" },
    { $pull: { opiniones: { rating: { $lt: 3 } } } }
);

// $addToSet: agregar solo si no existe
db.productos.updateOne(
    { nombre: "Laptop Pro X1" },
    { $addToSet: { categorias: "gaming" } }  // ya existe, no cambia nada
);
db.productos.updateOne(
    { nombre: "Laptop Pro X1" },
    { $addToSet: { categorias: "nueva-cat" } }  // se agrega
);

// $pop: eliminar primer o ultimo elemento
db.productos.updateOne(
    { nombre: "Laptop Pro X1" },
    { $pop: { etiquetas: 1 } }   // ultimo elemento
);
db.productos.updateOne(
    { nombre: "Laptop Pro X1" },
    { $pop: { etiquetas: -1 } }  // primer elemento
);
```

**Upsert:**

```javascript
// upsert: si existe actualiza, si no existe crea
db.productos.updateOne(
    { nombre: "Cable DisplayPort" },
    {
        $set: {
            nombre: "Cable DisplayPort",
            precio: 19.99,
            stock: 200,
            categorias: ["cables"]
        }
    },
    { upsert: true }
);
// Si no existia, crea el documento
// Resultado:
// {
//   acknowledged: true,
//   matchedCount: 0,
//   modifiedCount: 0,
//   upsertedId: ObjectId("...")
// }
```

**findOneAndUpdate(), findOneAndReplace(), findOneAndDelete():**

```javascript
// findOneAndUpdate: actualiza y retorna el documento
db.productos.findOneAndUpdate(
    { nombre: "Laptop Pro X1" },
    { $inc: { stock: -1 } },
    { returnDocument: "after" }
);

// findOneAndReplace: reemplaza todo el documento
db.productos.findOneAndReplace(
    { nombre: "Mouse Gamer RGB" },
    {
        nombre: "Mouse Gamer RGB v2",
        precio: 59.99,
        stock: 80,
        categorias: ["perifericos", "gaming"],
        nueva_version: true
    },
    { returnDocument: "after" }
);

// findOneAndDelete: elimina y retorna el documento
db.productos.findOneAndDelete(
    { stock: 0 }
);
```

### 5.4 DELETE (Eliminar)

```javascript
// deleteOne: elimina el primer documento que coincida
db.productos.deleteOne({ nombre: "Cable DisplayPort" });
// { acknowledged: true, deletedCount: 1 }

// deleteMany: elimina todos los documentos que coincidan
db.productos.deleteMany({ stock: { $lte: 0 } });
// { acknowledged: true, deletedCount: 1 }

// deleteMany: eliminar todos los documentos
db.productos.deleteMany({});
// { acknowledged: true, deletedCount: N }

// drop: eliminar toda la coleccion (incluye indices, mucho mas rapido)
db.productos.drop();
// true
```

---

## 6. Seguridad Basica

### 6.1 Autenticacion

**Crear usuario admin en base admin:**

```javascript
use admin

// Crear usuario root
db.createUser({
    user: "admin",
    pwd: "admin123!",
    roles: [
        { role: "userAdminAnyDatabase", db: "admin" },
        { role: "readWriteAnyDatabase", db: "admin" },
        { role: "clusterAdmin", db: "admin" }
    ]
});

// Reiniciar mongod con --auth o security.authorization: enabled
// Conectar con autenticacion
mongosh -u admin -p "admin123!" --authenticationDatabase admin
```

**Crear usuario de aplicacion:**

```javascript
use admin;

// Usuario solo de lectura para la BD tienda
db.createUser({
    user: "lector_tienda",
    pwd: "lector123!",
    roles: [
        { role: "read", db: "tienda" }
    ]
});

// Usuario de lectura/escritura para la BD tienda
db.createUser({
    user: "app_tienda",
    pwd: "app123!",
    roles: [
        { role: "readWrite", db: "tienda" }
    ]
});

// Verificar usuarios
db.getUsers();

// Probar credenciales
db.auth("app_tienda", "app123!");
// 1 = exitoso

// Cambiar contrasena
db.changeUserPassword("app_tienda", "nuevaContrasena123!");

// Eliminar usuario
db.dropUser("lector_tienda");
```

**Roles predefinidos:**

| Rol | Base | Descripcion |
|-----|------|-------------|
| read | Cualquier BD | Solo lectura |
| readWrite | Cualquier BD | Lectura y escritura |
| dbAdmin | Cualquier BD | Administracion de BD |
| userAdmin | Cualquier BD | Crear/eliminar usuarios |
| clusterAdmin | admin | Administracion de cluster |
| dbOwner | Cualquier BD | readWrite + dbAdmin + userAdmin |
| root | admin | Todos los privilegios |
| readAnyDatabase | admin | Lectura en todas las BDs |
| readWriteAnyDatabase | admin | Lectura/escritura en todas las BDs |

### 6.2 Autorizacion (RBAC)

```javascript
// Ver todos los roles disponibles
db.getRoles({ showBuiltinRoles: true });

// Crear rol personalizado
db.createRole({
    role: "ventasRead",
    privileges: [
        {
            resource: { db: "tienda", collection: "productos" },
            actions: ["find"]
        },
        {
            resource: { db: "tienda", collection: "pedidos" },
            actions: ["find", "insert", "update"]
        }
    ],
    roles: []
});

// Asignar rol a usuario
db.createUser({
    user: "vendedor",
    pwd: "vendedor123!",
    roles: [{ role: "ventasRead", db: "admin" }]
});

// Verificar permisos
db.getUser("vendedor", { showPrivileges: true });
```

### 6.3 Red

```yaml
# En mongod.conf
net:
  # Solo escuchar en localhost (desarrollo)
  bindIp: 127.0.0.1

  # Produccion: IP del servidor + localhost
  # bindIp: 127.0.0.1,192.168.1.100

  # NEVER en produccion:
  # bindIp: 0.0.0.0

  port: 27017

  # SSL/TLS para conexiones cifradas
  # tls:
  #   mode: requireTLS
  #   certificateKeyFile: /etc/ssl/mongo.pem
  #   CAFile: /etc/ssl/ca.pem
```

```bash
# Verificar que MongoDB solo escucha en localhost
netstat -tlnp | grep 27017
# tcp  127.0.0.1:27017  0.0.0.0:*  LISTEN  PID/mongod
```

### 6.4 NoSQL Injection

**Ejemplo de ataque:**

```javascript
// Una API web recibe un JSON del usuario:
// { "usuario": "admin", "password": "abc" }

// El atacante envia:
// { "usuario": {"$gt": ""}, "password": {"$gt": ""}

// Si el backend NO valida el tipo, MongoDB ejecuta:
db.usuarios.find({
    usuario: { $gt: "" },
    password: { $gt: "" }
});
// Retorna TODOS los usuarios
```

**Prevencion:**

```javascript
// Node.js / Express: sanitizar la entrada
function sanitizeInput(input) {
    if (typeof input === 'object' && input !== null) {
        for (const key in input) {
            if (typeof input[key] === 'object' && input[key] !== null) {
                if (key.startsWith('$')) {
                    delete input[key];
                } else {
                    sanitizeInput(input[key]);
                }
            }
        }
    }
    return input;
}

// Usar $eq en vez de comparaciones directas
// MAL (vulnerable):
db.usuarios.find({ usuario: userInput });

// BIEN (seguro):
db.usuarios.find({ usuario: { $eq: userInput } });

// Validacion de esquema
db.createCollection("usuarios", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["usuario", "password"],
            properties: {
                usuario: { bsonType: "string" },
                password: { bsonType: "string" }
            }
        }
    }
});
```

---

## 7. Ejercicio Practico

### Ejercicio 1: Crear la base de datos tienda

```javascript
use tienda;

// Crear coleccion productos con validacion
db.createCollection("productos", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["nombre", "precio", "stock"],
            properties: {
                nombre: { bsonType: "string" },
                precio: { bsonType: "double" },
                stock: { bsonType: "int" },
                categorias: { bsonType: "array" }
            }
        }
    }
});

// Crear coleccion clientes
db.createCollection("clientes");

// Crear coleccion pedidos
db.createCollection("pedidos");
```

### Ejercicio 2: Insertar 10 productos con diferentes estructuras

```javascript
db.productos.insertMany([
    { nombre: "Laptop Gamer", precio: 1599.99, stock: 15, categorias: ["laptops", "gaming"], specs: { cpu: "i9", ram: 32 } },
    { nombre: "Mouse inalambrico", precio: 29.99, stock: 200, categorias: ["perifericos"] },
    { nombre: "Monitor 4K", precio: 799.99, stock: 25, categorias: ["monitores"], specs: { pulgadas: 27 } },
    { nombre: "Teclado bluetooth", precio: 69.99, stock: 0, categorias: ["perifericos"] },
    { nombre: "SSD 1TB NVMe", precio: 109.99, stock: 80, categorias: ["almacenamiento"] },
    { nombre: "Webcam 4K", precio: 149.99, stock: 45, categorias: ["perifericos", "streaming"] },
    { nombre: "Auriculares gaming", precio: 199.99, stock: 60, categorias: ["audio", "gaming"] },
    { nombre: "Cable HDMI 2.1", precio: 14.99, stock: 300, categorias: ["accesorios"] },
    { nombre: "Hub USB-C", precio: 49.99, stock: 120, categorias: ["accesorios"] },
    { nombre: "Alfombrilla XL", precio: 24.99, stock: 90, categorias: ["accesorios", "gaming"] }
]);
```

### Ejercicio 3: Realizar 10 consultas

```javascript
// 1. Todos los productos
db.productos.find();

// 2. Productos con precio > 100
db.productos.find({ precio: { $gt: 100 } });

// 3. Productos con stock = 0
db.productos.find({ stock: 0 });

// 4. Productos de la categoria "gaming"
db.productos.find({ categorias: "gaming" });

// 5. Productos de "perifericos" con precio < 100
db.productos.find({ $and: [{ categorias: "perifericos" }, { precio: { $lt: 100 } }] });

// 6. Top 3 mas caros
db.productos.find().sort({ precio: -1 }).limit(3).project({ nombre: 1, precio: 1, _id: 0 });

// 7. Productos sin campo specs
db.productos.find({ specs: { $exists: false } });

// 8. Productos cuyo nombre contiene "gaming"
db.productos.find({ nombre: { $regex: /gaming/i } });

// 9. Productos con precio entre 50 y 200
db.productos.find({ precio: { $gte: 50, $lte: 200 } });

// 10. Contar productos con stock > 50
db.productos.countDocuments({ stock: { $gt: 50 } });
```

### Ejercicio 4: Actualizar y eliminar

```javascript
// 1. Subir precio 10% a todos los productos de gaming
db.productos.updateMany(
    { categorias: "gaming" },
    { $mul: { precio: 1.10 } }
);

// 2. Agregar tag "nuevo" a productos sin specs
db.productos.updateMany(
    { specs: { $exists: false } },
    { $push: { tags: "nuevo" } }
);

// 3. Reducir stock en 1 para el producto mas barato
db.productos.find().sort({ precio: 1 }).limit(1).forEach(
    doc => db.productos.updateOne({ _id: doc._id }, { $inc: { stock: -1 } })
);

// 4. Eliminar productos sin stock
db.productos.deleteMany({ stock: 0 });

// 5. Verificar cambios
db.productos.find().sort({ precio: -1 });
```

### Ejercicio 5: Crear usuario de aplicacion

```javascript
use admin;

db.createUser({
    user: "app_tienda",
    pwd: "app123!",
    roles: [
        { role: "readWrite", db: "tienda" }
    ]
});

// Verificar
db.getUser("app_tienda");

// Probar conexion
mongosh -u app_tienda -p "app123!" --authenticationDatabase admin
use tienda;
db.productos.countDocuments();  // Debe funcionar
db.productos.insertOne({ nombre: "test", precio: 1 });  // Debe funcionar
use admin;
db.getUsers();  // No debe funcionar (sin permisos en admin)
```

---

## Resumen de la Clase

```mermaid
mindmap
  root((MongoDB I))
    Marco Teorico
      10gen 2009
      BSON vs JSON
      WiredTiger Engine
      Document-level locking
    Instalacion
      Windows MSI
      Linux apt
      Docker
      mongod.conf
    Modelo de Datos
      Documento max 16MB
      Colecciones
      Tipos BSON 12+
      Indices
    CRUD
      insertOne / insertMany
      find + operadores
      updateOne / updateMany
      deleteOne / deleteMany
    Seguridad
      Autenticacion
      RBAC roles
      bindIp
      NoSQL Injection
```

---

> **Proxima clase:** Clase 03 — MongoDB II: Consultas Avanzadas y Aggregation Pipeline

---

*Curso NoSQL — Clase 02 de 3 — MongoDB I: Fundamentos, Instalacion y CRUD*
