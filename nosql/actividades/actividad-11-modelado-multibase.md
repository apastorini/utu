# Actividad 11 — Modelado multi-base: e-commerce con MongoDB, Redis y Neo4j

## Datos generales

- **Duración:** 50 minutos
- **Tipo:** Individual (o parejas)
- **Herramienta de IA:** Libre
- **Requisitos:** Docker funcionando

## Presupuesto de tiempo

| Paso | Tiempo |
|------|--------|
| Leer el marco teórico | 7 min |
| Levantar las 3 bases | 6 min |
| MongoDB: catálogo y pedidos | 12 min |
| Redis: caché y sesión | 10 min |
| Neo4j: recomendaciones | 10 min |
| Verificación y entrega | 5 min |

## Objetivos

1. Aplicar **polyglot persistence**: usar la base adecuada para cada necesidad.
2. Modelar el mismo sistema (e-commerce) en **MongoDB, Redis y Neo4j**.
3. Escribir consultas en las tres bases y comparar el enfoque.
4. Justificar cada elección de tecnología con argumentos técnicos.

---

## Marco teórico

### ¿Qué es polyglot persistence?

"Poliglota" = que habla muchos idiomas. En vez de meter todo en una sola base, usás **la mejor herramienta para cada parte** del sistema:

| Necesidad del e-commerce | Base elegida | Por qué |
|--------------------------|--------------|---------|
| Catálogo de productos con estructura flexible | MongoDB | documentos con categorías y specs variables |
| Pedidos con ítems embebidos | MongoDB | se leen juntos, sin JOINs |
| Carrito y sesión de usuario (muy rápidos) | Redis | clave-valor en memoria, TTL |
| Contadores y "más vistos" | Redis | INCR a velocidad RAM |
| Recomendaciones "personas como vos compraron…" | Neo4j | recorridos de relaciones |
| Detección de fraude en compras | Neo4j | patrones de conexión |

> La clave de un arquitecto de datos no es "saber una base", sino **decidir cuál usar para cada caso**.

### Analogía de responsabilidades

- **MongoDB** guarda el "qué" (los datos del catálogo y los pedidos).
- **Redis** guarda el "cuánto" y "qué tan rápido" (sesiones, cachés, contadores).
- **Neo4j** guarda el "cómo se conecta" (gustos, amigos, compras relacionadas).

---

## Paso a paso

### Paso 1 — Levantar las 3 bases

```powershell
docker rm -f mongo-clase redis-clase neo4j-clase 2>$null

docker run -d --name mongo-clase -p 27017:27017 mongo:7
docker run -d --name redis-clase -p 6379:6379 redis:7
docker run -d --name neo4j-clase -p 7474:7474 -p 7687:7687 -e NEO4J_AUTH=neo4j/Neo4j123 neo4j:5-community
```

### Paso 2 — MongoDB: catálogo de productos

```powershell
docker exec -it mongo-clase mongosh
```

```javascript
use ecommerce

db.productos.insertMany([
    { sku: "TEC-001", nombre: "Teclado mecánico", precio: 80, categorias: ["tecnología", "periféricos"], stock: 40, specs: { layout: "ES", switches: "rojos" } },
    { sku: "TEC-002", nombre: "Mouse inalámbrico", precio: 35, categorias: ["tecnología", "periféricos"], stock: 120, specs: { dpi: 16000 } },
    { sku: "MON-001", nombre: "Monitor 27\"", precio: 350, categorias: ["tecnología", "monitores"], stock: 15, specs: { resolucion: "2560x1440" } },
    { sku: "LIB-001", nombre: "Dune", precio: 25, categorias: ["libros", "ficción"], stock: 80, specs: { paginas: 412 } },
    { sku: "LIB-002", nombre: "1984", precio: 20, categorias: ["libros", "distopía"], stock: 60, specs: { paginas: 328 } }
])

// Catálogo de productos de tecnología con stock bajo
db.productos.find(
    { categorias: "tecnología", stock: { $lt: 50 } },
    { nombre: 1, stock: 1, _id: 0 }
)
```

Pedido con ítems embebidos:

```javascript
db.pedidos.insertOne({
    numero: 1001,
    cliente: "Ana",
    fecha: new Date(),
    total: 115,
    items: [
        { sku: "TEC-001", cantidad: 1, precio: 80 },
        { sku: "TEC-002", cantidad: 1, precio: 35 }
    ]
})

db.pedidos.find({ numero: 1001 }).pretty()
```

### Paso 3 — Redis: sesión de usuario y carrito

```powershell
docker exec -it redis-clase redis-cli
```

```bash
# Sesión (con expiración)
SET sesion:ana "{\"cliente\":\"Ana\",\"id\":1}" EX 60

# Carrito (hash: producto → cantidad)
HSET carrito:ana TEC-001 1
HSET carrito:ana LIB-001 2
HGETALL carrito:ana

# Contador de visitas al catálogo
INCR contador:visitas
INCR contador:visitas

# Productos más vistos (sorted set)
ZINCRBY ranking:productos 1 TEC-001
ZINCRBY ranking:productos 3 MON-001
ZREVRANGE ranking:productos 0 -1 WITHSCORES
```

### Paso 4 — Neo4j: recomendaciones

```powershell
docker exec -it neo4j-clase cypher-shell -u neo4j -p Neo4j123
```

```cypher
// Quienes compraron también compraron (relación de pedido)
CREATE (ana:Cliente {nombre: "Ana"})
CREATE (bruno:Cliente {nombre: "Bruno"})
CREATE (p1:Producto {sku: "TEC-001", nombre: "Teclado"})
CREATE (p2:Producto {sku: "TEC-002", nombre: "Mouse"})
CREATE (p3:Producto {sku: "MON-001", nombre: "Monitor"})
CREATE (ana)-[:COMPRO]->(p1)
CREATE (ana)-[:COMPRO]->(p2)
CREATE (bruno)-[:COMPRO]->(p1)
CREATE (bruno)-[:COMPRO]->(p3);
```

Recomendación: "productos que compraron otros clientes que compraron lo mismo que Ana":

```cypher
MATCH (ana:Cliente {nombre: "Ana"})-[:COMPRO]->(producto)<-[:COMPRO]-(otro:Cliente)
WHERE otro <> ana
MATCH (otro)-[:COMPRO]->(otro_producto)
WHERE NOT EXISTS((ana)-[:COMPRO]->(otro_producto))
RETURN DISTINCT otro.nombre AS recomendado_a_partir_de, otro_producto.nombre AS producto;
```

Resultado esperado: "a partir de Bruno → Monitor".

### Paso 5 — Integrar: simular el flujo completo

**Paso 5.1 —** El cliente entra: la sesión se lee de Redis.

```bash
GET sesion:ana
```

**Paso 5.2 —** Consulta el catálogo en MongoDB (con caché de Redis en la práctica real).

```powershell
docker exec -it mongo-clase mongosh ecommerce --quiet --eval 'db.productos.find({}, {nombre:1,_id:0}).toArray()'
```

**Paso 5.3 —** El sistema de recomendaciones consulta Neo4j.

```cypher
MATCH (ana:Cliente {nombre: "Ana"})-[:COMPRO]->(producto)<-[:COMPRO]-(:Cliente)-[:COMPRO]->(rec)
WHERE NOT EXISTS((ana)-[:COMPRO]->(rec))
RETURN rec.nombre AS sugerencia;
```

### Paso 6 — Preguntar a la IA

```
¿Qué problemas de consistencia aparecen si el stock vive en MongoDB pero el carrito en Redis?
¿Cuándo convendría guardar el carrito en Redis con TTL y cuándo en MongoDB?
¿Cómo sincronizarías Neo4j con MongoDB cuando un cliente hace una compra?
```

## Verificación de resultados

- [ ] Las 3 bases responden en sus puertos.
- [ ] MongoDB devuelve el catálogo filtrado y el pedido 1001.
- [ ] Redis muestra el carrito de Ana y el ranking de productos.
- [ ] Neo4j recomienda el Monitor a partir del Teclado compartido.
- [ ] Podés explicar **por qué** elegiste cada base para cada dato.

## Criterios de evaluación

| Criterio | Puntos |
|----------|--------|
| Las 3 bases levantadas | 15 |
| MongoDB modelado y consultas | 25 |
| Redis sesión/carrito/ranking | 25 |
| Neo4j recomendación | 25 |
| Justificación de cada tecnología | 10 |

## Entregable

- Archivo `multi-base-ecommerce.md` con: los comandos de cada base, el resultado de las consultas y una tabla "necesidad → base → por qué".
- Respuesta de la IA sobre la consistencia carrito/stock.

## Seguridad (adelanto)

En la Actividad 12 vas a montar las 3 bases con **`docker compose`**, redes aisladas, volúmenes y **secretos** para las credenciales. Adiós a las bases sin contraseña.
