# Actividad 2 — Primeros pasos con MongoDB: CRUD y consultas

## Datos generales

- **Duración:** 50 minutos
- **Tipo:** Individual
- **Herramienta de IA:** Libre (OpenCode, ChatGPT, Claude, Gemini, Copilot… la que prefieras)
- **Requisitos:** Docker funcionando (Actividad 1)

## Presupuesto de tiempo

| Paso | Tiempo |
|------|--------|
| Leer el marco teórico | 5 min |
| Levantar MongoDB con Docker | 5 min |
| Insertar documentos | 10 min |
| Consultar documentos | 15 min |
| Actualizar y eliminar | 10 min |
| Verificación y entrega | 5 min |

## Objetivos

1. Levantar MongoDB en un contenedor Docker.
2. Entender el modelo de datos por **documentos**.
3. Ejecutar operaciones **CRUD** (Create, Read, Update, Delete) con `mongosh`.
4. Consultar documentos con filtros, operadores y proyecciones.

---

## Marco teórico

### ¿Qué es MongoDB?

MongoDB es una base de datos **NoSQL documental** open source. Los datos se guardan como **documentos BSON** (formato binario derivado de JSON). Un documento es un objeto con pares clave-valor, que admite anidamiento y arreglos.

### Estructura de niveles

```
Base de datos (database)
   └── Colección (collection)   ← equivalente aproximado a una tabla
          └── Documento         ← equivalente aproximado a una fila
```

### Ventajas del modelo documental

- **Esquema flexible:** cada documento puede tener campos distintos.
- **Anidamiento:** los datos que se leen juntos se guardan juntos (desnormalización).
- **Sin JOINs:** el dato relacionado va dentro del mismo documento.

### Operadores de comparación

| Operador | Significado | Ejemplo |
|----------|-------------|---------|
| `$gt` | mayor que | `{ precio: { $gt: 100 } }` |
| `$gte` | mayor o igual | `{ edad: { $gte: 18 } }` |
| `$lt` | menor que | `{ stock: { $lt: 5 } }` |
| `$in` | está dentro de un arreglo | `{ categoria: { $in: ["a","b"] } }` |
| `$regex` | búsqueda por patrón | `{ nombre: { $regex: "^Mar" } }` |

---

## Paso a paso

### Paso 1 — Levantar MongoDB en Docker

Ejecutá en la terminal:

```powershell
docker run -d --name mongo-clase \
  -p 27017:27017 \
  -v mongo-clase-data:/data/db \
  mongo:7
```

- `-d` ejecuta el contenedor en segundo plano.
- `-p 27017:27017` publica el puerto 27017 en tu PC.
- `-v ...:/data/db` guarda los datos en un volumen (persisten entre reinicios).
- `mongo:7` es la imagen oficial.

Verificá que esté corriendo:

```powershell
docker ps
```

### Paso 2 — Entrar a la consola de MongoDB

```powershell
docker exec -it mongo-clase mongosh
```

Deberías ver el prompt `test>`.

### Paso 3 — Crear base de datos y colección

```javascript
// Cambiás de base de datos (se crea al guardar el primer dato)
use biblioteca

// Los documentos se ven "bonitos"
db.libros.find().pretty()

// Creás la colección explícitamente (opcional, se crea sola al insertar)
db.createCollection("libros")
show collections
```

### Paso 4 — Insertar documentos

Insertá un solo documento:

```javascript
db.libros.insertOne({
    titulo: "Cien años de soledad",
    autor: "Gabriel García Márquez",
    anio: 1967,
    precio: 450,
    categorias: ["Literatura", "Realismo mágico"],
    editorial: { nombre: "Sudamericana", pais: "Argentina" },
    disponible: true
})
```

Insertá varios documentos:

```javascript
db.libros.insertMany([
    { titulo: "Dune", autor: "Frank Herbert", anio: 1965, precio: 520, categorias: ["Ciencia ficción"], editorial: { nombre: "Ace Books", pais: "EEUU" }, disponible: true },
    { titulo: "1984", autor: "George Orwell", anio: 1949, precio: 380, categorias: ["Distopía", "Ciencia ficción"], editorial: { nombre: "Secker", pais: "Inglaterra" }, disponible: false },
    { titulo: "Fahrenheit 451", autor: "Ray Bradbury", anio: 1953, precio: 410, categorias: ["Distopía", "Ciencia ficción"], editorial: { nombre: "Ballantine", pais: "EEUU" }, disponible: true },
    { titulo: "El principito", autor: "Antoine de Saint-Exupéry", anio: 1943, precio: 250, categorias: ["Infantil", "Fábula"], editorial: { nombre: "Reynal", pais: "Francia" }, disponible: true }
])
```

### Paso 5 — Consultar documentos (Read)

Todas las consultas devuelven un **cursor**. Podés mostrar los resultados con `forEach(printjson)` o `.pretty()`.

```javascript
// Todos los libros
db.libros.find().pretty()

// Con filtro simple
db.libros.find({ disponible: true }).pretty()

// Con operador de comparación
db.libros.find({ precio: { $gt: 400 } }).pretty()

// Con operador lógico (AND implícito)
db.libros.find({ disponible: true, precio: { $gte: 400 } }).pretty()

// Búsqueda dentro de arreglos
db.libros.find({ categorias: "Ciencia ficción" }).pretty()

// Búsqueda por campo anidado (notación con punto)
db.libros.find({ "editorial.pais": "EEUU" }).pretty()

// Búsqueda por patrón (regex)
db.libros.find({ titulo: { $regex: "^(Cien|El)" } }).pretty()
```

### Paso 6 — Proyecciones (elegir qué campos mostrar)

```javascript
// Solo titulo y precio, sin _id
db.libros.find({}, { titulo: 1, precio: 1, _id: 0 }).pretty()
```

### Paso 7 — Contar y ordenar

```javascript
// Cantidad de documentos que cumplen el filtro
db.libros.countDocuments({ disponible: true })

// Ordenar por precio descendente
db.libros.find().sort({ precio: -1 }).pretty()

// Limitar resultados
db.libros.find().sort({ precio: -1 }).limit(3).pretty()
```

### Paso 8 — Actualizar (Update)

```javascript
// Actualizar un solo documento
db.libros.updateOne(
    { titulo: "Dune" },
    { $set: { precio: 599 } }
)

// Agregar un elemento a un arreglo
db.libros.updateOne(
    { titulo: "1984" },
    { $push: { categorias: "Clásico" } }
)

// Actualizar varios documentos a la vez
db.libros.updateMany(
    { disponible: false },
    { $set: { disponible: true } }
)
```

### Paso 9 — Eliminar (Delete)

```javascript
// Eliminar un documento
db.libros.deleteOne({ titulo: "El principito" })

// Eliminar todos los que cumplan el filtro
db.libros.deleteMany({ anio: { $lt: 1950 } })

// Ver cuántos quedaron
db.libros.countDocuments()
```

### Paso 10 — Pedir ayuda a la IA

Usá tu herramienta de IA para profundizar. Ejemplos de preguntas:

```
En MongoDB, ¿cuál es la diferencia entre updateOne y replaceOne? Mostrame un ejemplo.
¿Cómo puedo buscar libros cuyo editorial.pais sea "EEUU" y con más de una categoría?
¿Qué es un cursor y por qué find() no devuelve directamente los documentos?
```

## Verificación de resultados

- [ ] `docker exec -it mongo-clase mongosh` entra sin errores.
- [ ] Insertaste al menos 5 libros y 1 quedó con documento anidado `editorial`.
- [ ] Hiciste consultas con `$gt`, `$in`, `$regex` y búsqueda en arreglo.
- [ ] `countDocuments()` devuelve la cantidad esperada.

## Criterios de evaluación

| Criterio | Puntos |
|----------|--------|
| Contenedor MongoDB levantado | 15 |
| Inserción de documentos (individual y masiva) | 25 |
| Consultas con filtros, operadores y proyección | 30 |
| Actualizaciones y eliminaciones correctas | 20 |
| Uso de la IA para resolver una duda (captura) | 10 |

## Entregable

- Archivo `crud-mongodb.js` con los comandos ejecutados y el resultado de cada consulta (pedíselo a la IA para generarlo a partir de tu historial).
- Captura de la terminal mostrando al menos 3 consultas.

## Consejos de seguridad para próximas clases

En esta clase el contenedor quedó **sin contraseña** (solo para pruebas). En la Actividad 4 vas a habilitar autenticación, crear usuarios con roles y proteger el servicio. No uses bases sin contraseña para datos reales.
