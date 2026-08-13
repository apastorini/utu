# Actividad 9 — Neo4j: bases de datos de grafos y consultas Cypher

## Datos generales

- **Duración:** 50 minutos
- **Tipo:** Individual
- **Herramienta de IA:** Libre
- **Requisitos:** Docker funcionando (necesitás ~2 GB de RAM libre)

## Presupuesto de tiempo

| Paso | Tiempo |
|------|--------|
| Leer el marco teórico | 7 min |
| Levantar Neo4j con Docker | 8 min |
| Crear nodos y relaciones | 12 min |
| Consultas MATCH | 10 min |
| Recorridos y recomendaciones | 8 min |
| Verificación y entrega | 5 min |

## Objetivos

1. Comprender el modelo de datos de **grafos**: nodos, relaciones, propiedades y etiquetas.
2. Escribir consultas **Cypher**: `CREATE`, `MATCH`, `WHERE`, `RETURN`.
3. Modelar una red social simple y hacer **recorridos** de relaciones.
4. Resolver un caso de **recomendaciones** con consultas de grafos.

---

## Marco teórico

### ¿Qué es una base de datos de grafos?

En vez de tablas, los datos se modelan como **nodos** conectados por **relaciones**. Es la base más natural para datos con muchas conexiones (redes sociales, fraude, rutas, recomendaciones).

```
(persona:A) -[:AMIGO]-> (persona:B)
```

### Elementos del modelo

| Elemento | Significado | Ejemplo |
|----------|-------------|---------|
| **Nodo** | una entidad | `(:Persona {nombre: "Ana"})` |
| **Etiqueta (label)** | tipo del nodo | `Persona`, `Producto`, `Compra` |
| **Propiedad** | dato del nodo/relación | `{edad: 30}` |
| **Relación** | conexión con dirección | `-[:AMIGO {desde: 2020}]->` |
| **Tipo de relación** | tipo de la conexión | `AMIGO`, `COMPRO`, `TRABAJA_EN` |

### ¿Cuándo un grafo gana?

- **Recorridos de varios saltos:** "amigos de amigos", "¿hay un camino entre A y B?".
- **Detección de fraude:** encontrar estructuras sospechosas (ej. una persona conectada a muchas tarjetas).
- **Recomendaciones:** "personas como tú también compraron…".

> Con SQL o MongoDB, "amigos de amigos" requiere JOINs o múltiples consultas; en un grafo es una sola consulta de profundidad.

### Sintaxis Cypher básica

```cypher
// Nodo
(:Persona {nombre: "Ana"})

// Relación con dirección
(ana:Persona)-[:AMIGO]->(bruno:Persona)

// Patrón completo
MATCH (ana:Persona {nombre: "Ana"})-[:AMIGO]->(amigo)
RETURN amigo.nombre
```

- `MATCH` encuentra el patrón.
- `WHERE` filtra.
- `RETURN` devuelve resultados (puede proyectar propiedades).
- Variables como `ana`, `amigo` reutilizan los nodos dentro de la consulta.

---

## Paso a paso

### Paso 1 — Levantar Neo4j

```powershell
docker run -d --name neo4j-clase \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/Neo4j123 \
  neo4j:5-community
```

- `7474` es la interfaz web (Browser). `7687` es el protocolo Bolt.
- `NEO4J_AUTH=neo4j/Neo4j123` define usuario y contraseña iniciales.

Esperá a que arranque (15-40 s):

```powershell
docker ps
```

### Paso 2 — Elegir cómo ejecutar Cypher

Dos opciones:

**Opción A — Web Browser:** entrá a http://localhost:7474 , usuario `neo4j`, contraseña `Neo4j123`.

**Opción B — Terminal:** ejecutá consultas con `cypher-shell`:

```powershell
docker exec -it neo4j-clase cypher-shell -u neo4j -p Neo4j123
```

Se abre el prompt `neo4j@neo4j>`. Usá la que te resulte más cómoda.

### Paso 3 — Crear nodos y relaciones

```cypher
CREATE (ana:Persona {nombre: "Ana", ciudad: "Montevideo"})
CREATE (bruno:Persona {nombre: "Bruno", ciudad: "Montevideo"})
CREATE (carla:Persona {nombre: "Carla", ciudad: "Salto"})
CREATE (diego:Persona {nombre: "Diego", ciudad: "Paysandú"});
```

Creá las relaciones de amistad:

```cypher
MATCH (ana:Persona {nombre: "Ana"}), (bruno:Persona {nombre: "Bruno"})
CREATE (ana)-[:AMIGO {desde: 2020}]->(bruno);

MATCH (ana:Persona {nombre: "Ana"}), (carla:Persona {nombre: "Carla"})
CREATE (ana)-[:AMIGO {desde: 2021}]->(carla);

MATCH (bruno:Persona {nombre: "Bruno"}), (diego:Persona {nombre: "Diego"})
CREATE (bruno)-[:AMIGO {desde: 2019}]->(diego);

MATCH (carla:Persona {nombre: "Carla"}), (diego:Persona {nombre: "Diego"})
CREATE (carla)-[:AMIGO {desde: 2022}]->(diego);
```

### Paso 4 — Consultas básicas

```cypher
// Todos los nodos
MATCH (n) RETURN n;

// Personas de Montevideo
MATCH (p:Persona)
WHERE p.ciudad = "Montevideo"
RETURN p.nombre, p.ciudad;

// Ordenar por nombre
MATCH (p:Persona)
RETURN p.nombre
ORDER BY p.nombre;

// Contar
MATCH (p:Persona)
RETURN count(p) AS total_personas;
```

### Paso 5 — Recorridos de un salto

```cypher
// Amigos de Ana
MATCH (ana:Persona {nombre: "Ana"})-[:AMIGO]->(amigo)
RETURN amigo.nombre;

// Con detalles de la relación
MATCH (ana:Persona {nombre: "Ana"})-[r:AMIGO]->(amigo)
RETURN amigo.nombre, r.desde;
```

### Paso 6 — Recorridos de varios saltos (el poder del grafo)

Amigos de amigos de Ana:

```cypher
MATCH (ana:Persona {nombre: "Ana"})-[:AMIGO]->()-[:AMIGO]->(amigo_de_amigo)
WHERE amigo_de_amigo <> ana
RETURN DISTINCT amigo_de_amigo.nombre;
```

¿Está Carla conectada con Diego en 2 saltos?

```cypher
MATCH (carla:Persona {nombre: "Carla"})-[r*1..2]->(diego:Persona {nombre: "Diego"})
RETURN length(r) AS saltos;
```

### Paso 7 — Caso de recomendaciones: películas

```cypher
// Personas que gustaron de películas
MATCH (ana:Persona {nombre: "Ana"})
CREATE (ana)-[:GUSTA_DE]->(:Pelicula {titulo: "Dune"})
WITH ana
MATCH (bruno:Persona {nombre: "Bruno"})
CREATE (bruno)-[:GUSTA_DE]->(:Pelicula {titulo: "Dune"})
CREATE (bruno)-[:GUSTA_DE]->(:Pelicula {titulo: "Blade Runner"})
CREATE (carla:Persona {nombre: "Carla"})
CREATE (carla)-[:GUSTA_DE]->(:Pelicula {titulo: "Inception"})
CREATE (carla)-[:GUSTA_DE]->(:Pelicula {titulo: "Blade Runner"});
```

Recomendación simple: "películas que gustaron a amigos de Ana, que Ana no vio":

```cypher
MATCH (ana:Persona {nombre: "Ana"})-[:AMIGO]->(amigo)-[:GUSTA_DE]->(pelicula)
WHERE NOT EXISTS((ana)-[:GUSTA_DE]->(pelicula))
RETURN DISTINCT pelicula.titulo AS recomendacion;
```

### Paso 8 — Detección de estructura (fraude)

```cypher
// Simulación: una persona compra con muchas tarjetas → patrón sospechoso
CREATE (sospechosa:Persona {nombre: "Eva"})
CREATE (tarjeta1:Tarjeta {numero: "4001"})
CREATE (tarjeta2:Tarjeta {numero: "4002"})
CREATE (tarjeta3:Tarjeta {numero: "4003"})
CREATE (sospechosa)-[:USO]->(tarjeta1)
CREATE (sospechosa)-[:USO]->(tarjeta2)
CREATE (sospechosa)-[:USO]->(tarjeta3);

// Personas que usan más de 2 tarjetas distintas (posible fraude)
MATCH (p:Persona)-[:USO]->(t:Tarjeta)
WITH p, count(t) AS tarjetas
WHERE tarjetas > 2
RETURN p.nombre, tarjetas;
```

### Paso 9 — Preguntar a la IA

```
¿En qué casos conviene Neo4j frente a MongoDB? ¿Y al revés?
Mostrame cómo calcular el camino más corto entre dos personas con Cypher.
¿Qué significa el operador *1..2 (variable-length relationship)? Dámelo con un ejemplo.
```

## Verificación de resultados

- [ ] El paso 5 devuelve Bruno y Carla como amigos de Ana.
- [ ] El paso 6 (amigos de amigos) devuelve a Diego.
- [ ] La recomendación del paso 7 sugiere "Blade Runner" (a Bruno le gusta y Carla también).
- [ ] El paso 8 detecta a Eva con 3 tarjetas.
- [ ] Podés ver el grafo visualmente en el Browser de Neo4j.

## Criterios de evaluación

| Criterio | Puntos |
|----------|--------|
| Contenedor Neo4j levantado | 10 |
| Nodos y relaciones creados | 25 |
| Consultas MATCH + WHERE | 25 |
| Recorrido de varios saltos | 20 |
| Caso recomendaciones/fraude | 20 |

## Entregable

- Archivo `neo4j-cypher.cypher` con todos los comandos y resultados.
- Captura del grafo en el Browser de Neo4j.
- Respuesta de la IA sobre cuándo usar grafos vs documentos.

## Seguridad (adelanto)

Neo4j también tiene roles y permisos, y es vulnerable a **inyecciones en Cypher**. En la Actividad 10 vas a protegerlo y a explotar una inyección simulada en un login.
