# Clase 1 — SQL vs NoSQL y Tipos de Bases de Datos NoSQL

## 1. Modelos Relacionales vs No Relacionales

### Modelo Relacional (SQL)

- Datos organizados en tablas con filas y columnas
- Esquema fijo y rígido
- Relaciones mediante claves foráneas
- Lenguaje SQL estandarizado
- Ejemplos: PostgreSQL, MySQL, Oracle, SQL Server

```sql
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT NOW()
);

CREATE TABLE pedidos (
    id SERIAL PRIMARY KEY,
    usuario_id INT REFERENCES usuarios(id),
    total DECIMAL(10,2),
    estado VARCHAR(20)
);
```

### Modelo NoSQL

- Sin esquema fijo (schema-less) o esquema flexible
- Diferentes modelos de datos según el caso de uso
- Escalabilidad horizontal nativa
- Ejemplos: MongoDB, Redis, Cassandra, Neo4j

### Cuándo usar cada modelo

| Criterio | SQL | NoSQL |
|----------|-----|-------|
| Datos estructurados y estables | Sí | No |
| Transacciones complejas multi-tabla | Sí | Limitado |
| Esquema cambiante | No | Sí |
| Escalamiento horizontal | Complejo | Nativo |
| Grandes volúmenes de datos no estructurados | No | Sí |
| Consultas ad-hoc complejas | Sí | Limitado |

```mermaid
graph TD
    A[¿Necesitas base de datos?] --> B{¿Datos estructurados y estables?}
    B -->|Sí| C{¿Transacciones complejas?}
    B -->|No| D[NoSQL]
    C -->|Sí| E[SQL]
    C -->|No| F{¿Escalamiento horizontal crítico?}
    F -->|Sí| D
    F -->|No| E
    D --> G{¿Tipo de datos?}
    G -->|Documentos| H[MongoDB]
    G -->|Clave-Valor| I[Redis]
    G -->|Columnas| J[Cassandra]
    G -->|Grafos| K[Neo4j]
```

## 2. Tipos de Bases de Datos NoSQL

### 2.1 Documentales

- Almacenan datos como documentos (JSON/BSON)
- Cada documento tiene estructura propia
- Ideales para contenido, catálogos, perfiles

**Ejemplo en MongoDB:**

```json
{
    "_id": ObjectId("64f1a2b3c4d5e6f7a8b9c0d1"),
    "nombre": "María López",
    "email": "maria@ejemplo.com",
    "edad": 28,
    "direcciones": [
        { "tipo": "casa", "calle": "Av. Corrientes 1234", "ciudad": "Buenos Aires" },
        { "tipo": "trabajo", "calle": "San Martín 567", "ciudad": "Córdoba" }
    ],
    "intereses": ["programación", "música", "viajes"]
}
```

### 2.2 Clave-Valor

- Diccionario distribuido
- Máxima velocidad de lectura/escritura
- Ideales para caché, sesiones, contadores

**Ejemplo en Redis:**

```
SET usuario:1001 '{"nombre": "Juan", "email": "juan@ejemplo.com"}'
GET usuario:1001
SET contador:visitas 1542
INCR contador:visitas
```

### 2.3 Columnas

- Datos organizados por columnas, no filas
- Optimizadas para escrituras masivas
- Ideales para time-series, IoT, analytics

**Ejemplo en Cassandra:**

```sql
CREATE TABLE metricas_servidor (
    servidor_id UUID,
    fecha TIMESTAMP,
    cpu double,
    memoria double,
    disco double,
    PRIMARY KEY (servidor_id, fecha)
) WITH CLUSTERING ORDER BY (fecha DESC);
```

### 2.4 Grafos

- Nodos, relaciones y propiedades
- Optimizadas para recorridos de relaciones
- Ideales para redes sociales, recomendaciones, detección de fraude

**Ejemplo en Neo4j (Cypher):**

```cypher
CREATE (juan:Persona {nombre: "Juan", edad: 30})
CREATE (maria:Persona {nombre: "María", edad: 28})
CREATE (juan)-[:AMIGO_DE {desde: 2020}]->(maria)
CREATE (juan)-[:TRABAJA_EN]->(:Empresa {nombre: "TechCorp"})
```

```mermaid
graph LR
    subgraph "Documentales"
        D1[MongoDB]
        D2[CouchDB]
        D3[Firebase Firestore]
    end
    subgraph "Clave-Valor"
        KV1[Redis]
        KV2[DynamoDB]
        KV3[Memcached]
    end
    subgraph "Columnas"
        C1[Cassandra]
        C2[HBase]
        C3[ScyllaDB]
    end
    subgraph "Grafos"
        G1[Neo4j]
        G2[ArangoDB]
        G3[Amazon Neptune]
    end
```

## 3. Instalación y Configuración de MongoDB

### 3.1 Instalación en Windows

1. Descargar MongoDB Community Server desde https://www.mongodb.com/try/download/community
2. Ejecutar el instalador y seleccionar "Complete"
3. Instalar MongoDB Compass (GUI)
4. Verificar instalación:

```bash
mongod --version
```

5. Iniciar el servicio:

```bash
net start MongoDB
```

### 3.2 Instalación en Linux (Ubuntu)

```bash
# Importar clave pública
curl -fsSL https://www.mongodb.org/static/pgp/server-7.0.asc | sudo gpg --dearmor -o /usr/share/keyrings/mongodb-server-7.0.gpg

# Agregar repositorio
echo "deb [signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg] http://repo.mongodb.org/apt/ubuntu $(lsb_release -cs)/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list

# Instalar
sudo apt update
sudo apt install -y mongodb-org

# Iniciar servicio
sudo systemctl start mongod
sudo systemctl enable mongod

# Verificar estado
sudo systemctl status mongod
```

### 3.3 Instalación en macOS

```bash
# Con Homebrew
brew tap mongodb/brew
brew install mongodb-community@7.0
brew services start mongodb-community@7.0

# Verificar
mongosh --eval "db.runCommand({ping: 1})"
```

### 3.4 Instalación con Docker (Multiplataforma)

```bash
docker run -d \
  --name mongodb \
  -p 27017:27017 \
  -v mongo-data:/data/db \
  -e MONGO_INITDB_ROOT_USERNAME=admin \
  -e MONGO_INITDB_ROOT_PASSWORD=secreto123 \
  mongo:7.0
```

## 4. Configuración de MongoDB

### 4.1 Archivo de configuración: `mongod.conf`

```yaml
storage:
  dbPath: /var/lib/mongodb
  journal:
    enabled: true

systemLog:
  destination: file
  path: /var/log/mongodb/mongod.log
  logAppend: true

net:
  port: 27017
  bindIp: 127.0.0.1

security:
  authorization: enabled
```

### 4.2 Crear usuario administrador

```bash
mongosh
```

```javascript
use admin
db.createUser({
    user: "admin",
    pwd: "secreto123",
    roles: [{ role: "root", db: "admin" }]
})
```

### 4.3 Crear usuario de aplicación

```javascript
use curso_nosql
db.createUser({
    user: "app_user",
    pwd: "app_password",
    roles: [
        { role: "readWrite", db: "curso_nosql" }
    ]
})
```

## 5. Primeros Pasos con MongoDB

### 5.1 Conectar a MongoDB

```bash
# Sin autenticación
mongosh

# Con autenticación
mongosh "mongodb://app_user:app_password@localhost:27017/curso_nosql"
```

### 5.2 Crear base de datos y colección

```javascript
// Crear/usar base de datos
use curso_nosql

// Crear colección (se crea automáticamente al insertar)
db.createCollection("usuarios")

// Ver colecciones
show collections
```

### 5.3 Insertar documentos

```javascript
// Insertar un documento
db.usuarios.insertOne({
    nombre: "Carlos García",
    email: "carlos@ejemplo.com",
    edad: 35,
    activo: true,
    intereses: ["JavaScript", "Python", "Docker"],
    direccion: {
        calle: "Av. 9 de Julio 1000",
        ciudad: "Buenos Aires",
        cp: "C1043"
    },
    fecha_registro: new Date()
})

// Insertar múltiples documentos
db.usuarios.insertMany([
    {
        nombre: "Ana Martínez",
        email: "ana@ejemplo.com",
        edad: 28,
        activo: true,
        intereses: ["MongoDB", "Node.js"],
        direccion: { calle: "Calle 500", ciudad: "La Plata", cp: "1900" },
        fecha_registro: new Date()
    },
    {
        nombre: "Pedro Rodríguez",
        email: "pedro@ejemplo.com",
        edad: 42,
        activo: false,
        intereses: ["Java", "Spring", "PostgreSQL"],
        direccion: { calle: "San Martín 200", ciudad: "Córdoba", cp: "5000" },
        fecha_registro: new Date()
    }
])
```

### 5.4 Consultar documentos

```javascript
// Obtener todos
db.usuarios.find()

// Con filtro
db.usuarios.find({ edad: { $gte: 30 } })

// Con proyección (solo ciertos campos)
db.usuarios.find({}, { nombre: 1, email: 1, _id: 0 })

// Buscar por campo embebido
db.usuarios.find({ "direccion.ciudad": "Buenos Aires" })

// Buscar en arrays
db.usuarios.find({ intereses: "Python" })

// Operadores lógicos
db.usuarios.find({
    $and: [
        { edad: { $gte: 25 } },
        { activo: true }
    ]
})
```

### 5.5 Actualizar documentos

```javascript
// Actualizar uno
db.usuarios.updateOne(
    { email: "carlos@ejemplo.com" },
    { $set: { edad: 36 } }
)

// Actualizar varios
db.usuarios.updateMany(
    { activo: false },
    { $set: { activo: true } }
)

// Agregar elemento a array
db.usuarios.updateOne(
    { email: "ana@ejemplo.com" },
    { $push: { intereses: "Redis" } }
)
```

### 5.6 Eliminar documentos

```javascript
// Eliminar uno
db.usuarios.deleteOne({ email: "pedro@ejemplo.com" })

// Eliminar varios
db.usuarios.deleteMany({ activo: false })
```

## 6. Comparación Práctica: SQL vs NoSQL en un Caso Real

### Esquema de usuarios + pedidos

**SQL (PostgreSQL):**

```sql
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    email VARCHAR(150)
);

CREATE TABLE pedidos (
    id SERIAL PRIMARY KEY,
    usuario_id INT REFERENCES usuarios(id),
    producto VARCHAR(100),
    cantidad INT,
    precio DECIMAL(10,2),
    fecha TIMESTAMP
);

-- Consulta con JOIN
SELECT u.nombre, p.producto, p.precio
FROM usuarios u
JOIN pedidos p ON u.id = p.usuario_id
WHERE u.email = 'carlos@ejemplo.com';
```

**NoSQL (MongoDB):**

```javascript
// Documentos embebidos (denormalización)
db.usuarios.insertOne({
    nombre: "Carlos García",
    email: "carlos@ejemplo.com",
    pedidos: [
        { producto: "Laptop", cantidad: 1, precio: 999.99, fecha: new Date() },
        { producto: "Mouse", cantidad: 2, precio: 25.50, fecha: new Date() }
    ]
})

// Consulta directa, sin JOIN
db.usuarios.findOne(
    { email: "carlos@ejemplo.com" },
    { pedidos: 1, _id: 0 }
)
```

```mermaid
graph LR
    A[Consulta] --> B{¿Necesitas JOINs?}
    B -->|Sí, pocos documentos| C[SQL con JOIN]
    B -->|No, datos embebidos| D[NoSQL con documentos]
    B -->|Sí, datos distribuidos| E{¿Frecuencia?}
    E -->|Alta| F[NoSQL con referencias + $lookup]
    E -->|Baja| C
```

## 7. Ejercicio Práctico

Crear una base de datos `tienda` con las colecciones:

1. `productos`: nombre, categoría, precio, stock, tags (array), especificaciones (documento embebido)
2. `clientes`: nombre, email, dirección, historial_compras (array embebido)
3. Insertar al menos 10 productos y 5 clientes
4. Consultar productos con precio mayor a $500
5. Buscar clientes de una ciudad específica
6. Actualizar stock de un producto
7. Agregar una compra al historial de un cliente
