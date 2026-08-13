# Actividad 13 — Indexación y rendimiento en MongoDB

## Datos generales

- **Duración:** 50 minutos
- **Tipo:** Individual
- **Herramienta de IA:** Libre
- **Requisitos:** MongoDB en Docker (Actividad 2)

## Presupuesto de tiempo

| Paso | Tiempo |
|------|--------|
| Leer el marco teórico | 7 min |
| Cargar datos masivos | 8 min |
| Consulta sin índice + explain | 8 min |
| Crear índice + comparar | 8 min |
| Índices compuestos | 8 min |
| Índice TTL | 6 min |
| Verificación y entrega | 5 min |

## Objetivos

1. Comprender qué es un **índice** y por qué acelera las consultas.
2. Medir el rendimiento con `explain()`.
3. Crear índices **simples, compuestos** y de **TTL**.
4. Evaluar el costo de los índices (escrituras, memoria).

---

## Marco teórico

### ¿Qué es un índice?

Un índice es una estructura auxiliar (MongoDB usa **B-tree**) que ordena un subconjunto de campos para encontrar rápido. Analogía: el índice alfabético de un libro. Buscar "Zebra" con índice es instantáneo; sin índice hay que leer todo el libro.

```
Consulta: find({ precio: { $gt: 100 } })

Sin índice  → COLLSCAN: revisa documento por documento (O(n))
Con índice  → IXSCAN: usa el árbol ordenado por precio (O(log n))
```

### Consecuencias

- **Beneficio:** lecturas mucho más rápidas.
- **Costo:** cada índice ocupa memoria y **ralentiza las escrituras** (hay que mantenerlo actualizado).
- **Regla:** índice para las consultas que se hacen de verdad, no "un índice por campo".

### Tipos de índices que vamos a usar

| Tipo | Comando | Uso |
|------|---------|-----|
| Simple | `createIndex({ campo: 1 })` | búsquedas por un campo |
| Compuesto | `createIndex({ a: 1, b: -1 })` | consultas que filtran por varios campos |
| TTL | `createIndex({ fecha: 1 }, { expireAfterSeconds: N })` | borrar documentos automáticamente tras N segundos |
| Texto | `createIndex({ campo: "text" })` | búsqueda full-text |

### Cómo leer `explain()`

```javascript
db.coleccion.find(...).explain("executionStats")
```

Campos clave:

- `executionStats.nReturned` → cuántos devolvió.
- `executionStats.totalDocsExamined` → cuántos revisó (debería ser ~nReturned con índice).
- `executionStats.executionTimeMillis` → tiempo.
- `winningPlan.stage` → `COLLSCAN` (malo) o `IXSCAN` (bueno).

---

## Paso a paso

### Paso 1 — Levantar MongoDB y cargar datos

```powershell
docker start mongo-clase
docker exec -it mongo-clase mongosh
```

```javascript
use rendimiento

// Cargamos 50.000 productos
const categorias = ["tecnologia", "hogar", "libros", "ropa", "juguetes"];
const productos = [];
for (let i = 0; i < 50000; i++) {
    productos.push({
        nombre: "Producto-" + i,
        precio: Math.round(Math.random() * 900 + 100),
        categoria: categorias[Math.floor(Math.random() * categorias.length)],
        stock: Math.floor(Math.random() * 100),
        fecha_ingreso: new Date(2026, 0, 1 + Math.floor(Math.random() * 200))
    });
}
db.productos.insertMany(productos);
db.productos.countDocuments();
```

### Paso 2 — Consulta sin índice

```javascript
db.productos.find({ precio: { $gte: 800 } }).explain("executionStats")
```

Mirá:

- `winningPlan.stage` → `COLLSCAN`
- `totalDocsExamined` → ~50000 (revisó todo)
- `executionTimeMillis` → registralo.

### Paso 3 — Crear el índice y volver a medir

```javascript
db.productos.createIndex({ precio: 1 })

db.productos.find({ precio: { $gte: 800 } }).explain("executionStats")
```

Mirá ahora:

- `winningPlan.stage` → `IXSCAN`
- `totalDocsExamined` → igual a `nReturned` (solo los que cumplen)
- `executionTimeMillis` → mucho menor.

Anotá la diferencia de tiempo.

### Paso 4 — Índice compuesto

Consulta por categoría + precio:

```javascript
// Sin índice
db.productos.find({ categoria: "libros", precio: { $gte: 500 } }).explain("executionStats")

// Índice compuesto (categoría primero, después precio)
db.productos.createIndex({ categoria: 1, precio: 1 })

// Con índice compuesto
db.productos.find({ categoria: "libros", precio: { $gte: 500 } }).explain("executionStats")
```

> **El orden importa:** el índice `{categoria:1, precio:1}` sirve para filtrar primero por categoría y luego por precio. El índice inverso `{precio:1, categoria:1}` **no** serviría para esta consulta.

### Paso 5 — Índice TTL (datos que se autoborran)

Ideal para sesiones, tokens y logs con fecha de vencimiento:

```javascript
// Colección de sesiones que vencen a los 60 segundos
db.sesiones.insertMany([
    { token: "abc-1", usuario: "Ana", creada: new Date() },
    { token: "abc-2", usuario: "Bruno", creada: new Date() }
]);

db.sesiones.createIndex({ creada: 1 }, { expireAfterSeconds: 60 });

// En un minuto la colección queda vacía sola
db.sesiones.countDocuments();
```

> Mongo revisa los índices TTL aproximadamente **cada 60 segundos**. No esperes el borrado inmediato.

### Paso 6 — Ver los índices de la colección

```javascript
db.productos.getIndexes()
```

Notarás que `_id` tiene índice automático (clave primaria).

### Paso 7 — Borrar un índice que no se usa

```javascript
db.productos.dropIndex({ precio: 1 })
db.productos.getIndexes()
```

> Mantener índices que no se usan es desperdicio de memoria y de velocidad de escritura.

### Paso 8 — Índice de texto (bonus)

```javascript
db.productos.createIndex({ nombre: "text" })

db.productos.find({ $text: { $search: "Producto-123" } }).limit(5)
```

### Paso 9 — Preguntar a la IA

```
¿Por qué un índice ayuda en lecturas pero perjudica las escrituras?
¿Cuándo conviene un índice compuesto y cuál es el orden correcto de sus campos?
¿Qué es un COLLSCAN y por qué es señal de un problema de diseño?
```

## Verificación de resultados

- [ ] El `explain()` sin índice muestra `COLLSCAN` y ~50000 documentos examinados.
- [ ] Con índice muestra `IXSCAN` y examina solo los que devuelve.
- [ ] El índice compuesto acelera la consulta por categoría+precio.
- [ ] La colección `sesiones` se vacía sola tras ~1-2 minutos.
- [ ] `getIndexes()` muestra los índices creados.

## Criterios de evaluación

| Criterio | Puntos |
|----------|--------|
| Datos cargados (50000) | 10 |
| Medición sin índice (COLLSCAN) | 20 |
| Índice simple y comparación | 25 |
| Índice compuesto y orden de campos | 20 |
| Índice TTL y texto | 25 |

## Entregable

- Archivo `indices-mongodb.md` con: capturas de `explain()` **antes y después**, la tabla de tiempos, y los índices creados.
- Respuesta de la IA sobre el orden de los campos en índices compuestos.

## Para pensar

Los índices mejoran las lecturas de un solo nodo. En la Actividad 14 vas a ver **replicación** (varias copias del dato) y en la 15 **sharding** (partir los datos en varios nodos).
