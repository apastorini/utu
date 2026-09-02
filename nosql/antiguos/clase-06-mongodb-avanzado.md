# Clase 6 — MongoDB: Modelado y Consultas Avanzadas

## 1. Instalación Completa de MongoDB Community Server

### Windows

1. Descargar desde https://www.mongodb.com/try/download/community
2. Seleccionar versión 7.0+, plataforma Windows, formato `.msi`
3. Ejecutar instalador → "Complete" installation
4. Instalar MongoDB Compass (opcional)
5. Verificar:

```bash
mongod --version
mongosh --version
```

### Ubuntu/Debian

```bash
curl -fsSL https://www.mongodb.org/static/pgp/server-7.0.asc | sudo gpg --dearmor -o /usr/share/keyrings/mongodb-server-7.0.gpg

echo "deb [signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg] http://repo.mongodb.org/apt/ubuntu $(lsb_release -cs)/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list

sudo apt update
sudo apt install -y mongodb-org

sudo systemctl start mongod
sudo systemctl enable mongod
sudo systemctl status mongod
```

### Docker (cualquier OS)

```bash
docker run -d \
  --name mongodb-clase6 \
  -p 27017:27017 \
  -v $(pwd)/mongo-data:/data/db \
  mongo:7.0
```

## 2. Configuración de mongod.conf

```yaml
# /etc/mongod.conf (Linux) o C:\Program Files\MongoDB\Server\7.0\bin\mongod.cfg (Windows)

storage:
  dbPath: /var/lib/mongodb
  journal:
    enabled: true
  wiredTiger:
    engineConfig:
      cacheSizeGB: 2

systemLog:
  destination: file
  path: /var/log/mongodb/mongod.log
  logAppend: true
  logRotate: rename

net:
  port: 27017
  bindIp: 127.0.0.1

security:
  authorization: enabled

processManagement:
  timeZoneInfo: /usr/share/zoneinfo
```

## 3. Autenticación

```bash
# Conectar sin auth
mongosh

# Crear admin
use admin
db.createUser({
    user: "admin",
    pwd: "admin123",
    roles: [{ role: "root", db: "admin" }]
})

# Crear usuario de app
use red_social
db.createUser({
    user: "app_user",
    pwd: "app123",
    roles: [{ role: "readWrite", db: "red_social" }]
})

# Reconectar con auth
mongosh "mongodb://app_user:app123@localhost:27017/red_social"
```

## 4. CRUD Avanzado

### 4.1 Update con Operadores

```javascript
// $set, $unset, $inc, $mul, $rename, $min, $max, $currentDate
db.usuarios.updateOne(
    { _id: ObjectId("...") },
    {
        $set: { nombre: "Nuevo Nombre" },
        $inc: { visitas: 1 },
        $currentDate: { ultima_actualizacion: true }
    }
)

// $push, $pull, $addToSet (arrays)
db.usuarios.updateOne(
    { _id: ObjectId("...") },
    {
        $push: { posts: { titulo: "Nuevo post", fecha: new Date() } },
        $addToSet: { tags: "mongodb" },  // solo si no existe
        $pull: { tags: "obsolete" }      // eliminar valor
    }
)

// $push con $each, $slice, $sort
db.usuarios.updateOne(
    { _id: ObjectId("...") },
    {
        $push: {
            actividad: {
                $each: [
                    { accion: "login", fecha: new Date("2024-01-01") },
                    { accion: "post", fecha: new Date("2024-01-02") }
                ],
                $slice: -10,   // mantener últimos 10
                $sort: { fecha: -1 }
            }
        }
    }
)
```

### 4.2 Upsert

```javascript
// Insertar si no existe, actualizar si existe
db.usuarios.updateOne(
    { email: "nuevo@ejemplo.com" },
    { $set: { nombre: "Nuevo Usuario", edad: 25 } },
    { upsert: true }
)
```

### 4.3 Bulk Write

```javascript
db.usuarios.bulkWrite([
    { insertOne: { document: { nombre: "A", edad: 20 } } },
    { updateOne: { filter: { nombre: "B" }, update: { $inc: { edad: 1 } } } },
    { deleteOne: { filter: { nombre: "C" } } },
    { replaceOne: { filter: { nombre: "D" }, replacement: { nombre: "E", edad: 30 } } }
])
```

## 5. Pipeline de Agregación

### 5.1 Etapas Principales

| Etapa | Función |
|-------|---------|
| `$match` | Filtrar documentos |
| `$group` | Agrupar y aplicar funciones de agregación |
| `$sort` | Ordenar |
| `$limit` / `$skip` | Limitar / saltar resultados |
| `$project` | Proyectar/renombrar campos |
| `$unwind` | Descomponer arrays |
| `$lookup` | JOIN con otra colección |
| `$addFields` | Agregar campos calculados |
| `$out` | Guardar resultado en nueva colección |
| `$merge` | Mergear resultado en colección existente |

### 5.2 Ejemplos de Agregación

```javascript
db.usuarios.insertMany([
    { nombre: "Ana", edad: 28, ciudad: "Buenos Aires", salario: 50000, depto: "IT" },
    { nombre: "Carlos", edad: 35, ciudad: "Córdoba", salario: 60000, depto: "IT" },
    { nombre: "María", edad: 30, ciudad: "Buenos Aires", salario: 55000, depto: "RRHH" },
    { nombre: "Pedro", edad: 42, ciudad: "Rosario", salario: 70000, depto: "IT" },
    { nombre: "Laura", edad: 25, ciudad: "Buenos Aires", salario: 45000, depto: "RRHH" }
])

// Salario promedio por departamento
db.usuarios.aggregate([
    { $group: {
        _id: "$depto",
        salario_promedio: { $avg: "$salario" },
        salario_max: { $max: "$salario" },
        empleados: { $sum: 1 }
    }},
    { $sort: { salario_promedio: -1 } }
])

// Top ciudades por cantidad de empleados
db.usuarios.aggregate([
    { $group: { _id: "$ciudad", total: { $sum: 1 } } },
    { $sort: { total: -1 } },
    { $limit: 3 }
])

// Proyección con campos calculados
db.usuarios.aggregate([
    { $match: { edad: { $gte: 30 } } },
    { $project: {
        nombre: 1,
        edad: 1,
        salario_mensual: { $divide: ["$salario", 12] },
        _id: 0
    }}
])
```

### 5.3 $lookup (JOIN)

```javascript
// Colección: pedidos
db.pedidos.insertMany([
    { usuario_id: ObjectId("64f1...01"), producto: "Laptop", monto: 999.99 },
    { usuario_id: ObjectId("64f1...02"), producto: "Mouse", monto: 25.50 },
    { usuario_id: ObjectId("64f1...01"), producto: "Teclado", monto: 75.00 }
])

// JOIN: usuario + sus pedidos
db.usuarios.aggregate([
    { $lookup: {
        from: "pedidos",
        localField: "_id",
        foreignField: "usuario_id",
        as: "mis_pedidos"
    }},
    { $unwind: { path: "$mis_pedidos", preserveNullAndEmptyArrays: true } },
    { $project: {
        nombre: 1,
        producto: "$mis_pedidos.producto",
        monto: "$mis_pedidos.monto"
    }}
])
```

### 5.4 $unwind

```javascript
db.usuarios.aggregate([
    { $unwind: "$intereses" },
    { $group: { _id: "$intereses", count: { $sum: 1 } } },
    { $sort: { count: -1 } }
])
// → ["JavaScript": 5, "Python": 3, ...]
```

### 5.5 Pipeline Complejo

```javascript
// Usuarios IT de Buenos Aires con sus pedidos
db.usuarios.aggregate([
    { $match: { depto: "IT", ciudad: "Buenos Aires" } },
    { $lookup: {
        from: "pedidos",
        localField: "_id",
        foreignField: "usuario_id",
        as: "pedidos"
    }},
    { $addFields: {
        total_gastado: { $sum: "$pedidos.monto" },
        cantidad_pedidos: { $size: "$pedidos" }
    }},
    { $project: {
        nombre: 1,
        depto: 1,
        total_gastado: 1,
        cantidad_pedidos: 1
    }},
    { $sort: { total_gastado: -1 } }
])
```

## 6. Patrones de Modelado Avanzados

### Patrón Bucket

```javascript
// Métricas de servidor agrupadas por hora
db.metricas.insertMany([
    {
        servidor: "srv-001",
        fecha: new Date("2024-01-15"),
        hora: 14,
        datos: [
            { minuto: 0, cpu: 45.2, mem: 62.1 },
            { minuto: 5, cpu: 46.8, mem: 62.3 },
            { minuto: 10, cpu: 44.5, mem: 61.9 }
        ]
    }
])
```

### Patrón Polimórfico

```javascript
db.notificaciones.insertMany([
    { tipo: "email", destinatario: "user@ejemplo.com", asunto: "Bienvenida", cuerpo: "..." },
    { tipo: "sms", destinatario: "+54911...", mensaje: "Tu código: 1234" },
    { tipo: "push", dispositivo_id: "device-xyz", titulo: "Nuevo mensaje", cuerpo: "..." }
])
```

## 7. Ejercicio Práctico: Modelar Red Social

### Estructura

```javascript
// Colección: usuarios
db.usuarios.insertOne({
    nombre: "Carlos",
    username: "carlos_g",
    email: "carlos@red.com",
    seguidores: [ObjectId("..."), ObjectId("...")],
    siguiendo: [ObjectId("...")],
    posts_count: 0
})

// Colección: posts
db.posts.insertOne({
    usuario_id: ObjectId("..."),
    usuario_nombre: "Carlos",
    contenido: "Primer post!",
    tipo: "texto",
    likes: [],
    comentarios: [
        { usuario_id: ObjectId("..."), usuario_nombre: "Ana", texto: "Genial!", fecha: new Date() }
    ],
    fecha: new Date()
})

// Colección: relaciones (para grafos simples)
db.relaciones.insertMany([
    { seguidor: ObjectId("..."), seguido: ObjectId("..."), fecha: new Date() }
])
```

### Consultas

```javascript
// Feed de un usuario (posts de quienes sigue)
db.posts.aggregate([
    { $match: { usuario_id: { $in: usuario.siguiendo } } },
    { $sort: { fecha: -1 } },
    { $limit: 20 }
])

// Posts con más likes
db.posts.aggregate([
    { $addFields: { likes_count: { $size: "$likes" } } },
    { $sort: { likes_count: -1 } },
    { $limit: 10 }
])
```
