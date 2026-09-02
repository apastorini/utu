# Clase 12 — Neo4j I: Fundamentos, Cypher y Modelo de Grafos

---

## 1. Marco Teórico

### 1.1 ¿Qué es una Base de Datos de Grafos?

Una base de datos de grafos es un sistema de gestión de datos diseñado para **almacenar, gestionar y consultar relaciones entre datos**. A diferencia de las bases de datos relacionales que organizan datos en tablas, las bases de datos de grafos utilizan un modelo de **nodos** y **relaciones** que se asemeja directamente a la forma en que pensamos sobre conexiones en el mundo real.

Neo4j es la base de datos de grafos más popular del mundo. Es un sistema **ACID** (Atomicidad, Consistencia, Aislamiento, Durabilidad) que almacena datos nativamente como grafos, no en tablas con claves foráneas.

### 1.2 Modelo de Datos: Nodos, Relaciones, Propiedades y Labels

```
                    ┌─────────────┐
                    │   :Persona   │
                    │  ─────────  │
                    │  nombre:    │
                    │  "Juan"     │
                    │  edad: 30   │
                    └──────┬──────┘
                           │
                    [:AMIGO_DE {desde: 2020}]
                           │
                    ┌──────▼──────┐
                    │   :Persona   │
                    │  ─────────  │
                    │  nombre:    │
                    │  "Ana"      │
                    │  edad: 28   │
                    └──────┬──────┘
                           │
                [:TRABAJA_EN {cargo: "Dev"}]
                           │
                    ┌──────▼──────┐
                    │   :Empresa   │
                    │  ─────────  │
                    │  nombre:    │
                    │  "TechCorp" │
                    │  sector:    │
                    │  "Tecnología"│
                    └─────────────┘
```

#### Nodos

Los **nodos** son las entidades基本icas del grafo. Cada nodo representa un objeto o una instancia.

```cypher
// Nodo simple
CREATE (juan:Persona {nombre: "Juan", edad: 30})

// Nodo con múltiples labels
CREATE (ana:Persona:Empleado {nombre: "Ana", edad: 28, cargo: "Dev"})
```

**Características de los nodos:**
- Tienen **labels** (etiquetas) que los categorizan
- Pueden tener **propiedades** (key-value pairs)
- Un nodo puede tener **múltiples labels**
- Los nodos se conectan entre sí mediante relaciones
- Cada nodo tiene un **ID interno** único (pero no se recomienda usarlo)

#### Labels (Etiquetas)

Los labels categorizan los nodos. Son equivalentes a las "tablas" en SQL.

```cypher
// Un nodo puede tener un label
CREATE (p:Persona {nombre: "Luis"})

// Un nodo puede tener múltiples labels
CREATE (m:Persona:Estudiante:Deportista {nombre: "María", edad: 22})

// Los labels se usan para consultar
MATCH (p:Persona) RETURN p
MATCH (e:Empleado) RETURN e
MATCH (p:Persona:Empleado) RETURN p  // Personas que también son empleados
```

#### Relaciones

Las **relaciones** conectan nodos y siempre tienen **dirección** y **tipo**.

```cypher
// Relación simple
CREATE (juan)-[:AMIGO_DE]->(ana)

// Relación con propiedades
CREATE (juan)-[:TRABAJA_EN {desde: 2020, cargo: "Senior Dev"}]->(techcorp)

// Relación en ambas direcciones (crea dos relaciones)
CREATE (juan)-[:CONOCE]->(luis)
CREATE (luis)-[:CONOCE]->(juan)
// O equivalentemente:
CREATE (juan)-[:CONOCE]-(luis)  // Crea relación en ambas direcciones
```

**Características de las relaciones:**
- Siempre tienen **dirección** (de nodo A a nodo B)
- Siempre tienen un **tipo** (ej: :AMIGO_DE, :TRABAJA_EN)
- Pueden tener **propiedades** (key-value pairs)
- Las relaciones son **primera clase** en el grafo (no son Foreign Keys)
- Las consultas por relaciones son **O(1)** en tiempo constante

#### Propiedades

Las **propiedades** son pares key-value que se pueden agregar a nodos y relaciones.

```cypher
// Tipos de propiedades soportados
CREATE (n:Node {
    texto: "Hola",           // String
    entero: 42,              // Integer
    decimal: 3.14,           // Float
    booleano: true,          // Boolean
    fecha: date("2024-01-15"),           // Date
    fecha_hora: datetime(),              // DateTime
    lista: [1, 2, 3],                   // List
    lista_texto: ["a", "b", "c"]        // List of Strings
})

// Propiedades en relaciones
CREATE (a)-[:RELACION {
    peso: 5,
    desde: date("2020-01-01"),
    activa: true
}]->(b)
```

**Restricciones de propiedades:**
- Máximo **512 bytes** por propiedad (valor serializado)
- No se pueden anidar propiedades (no hay objetos anidados)
- Las listas son planas (no listas de listas)
- Los nombres de propiedades son case-sensitive

### 1.3 ¿Cuándo Usar Grafos vs Otras BD?

| Pregunta clave | Grafo | Relacional | Documento | Key-Value |
|---------------|-------|------------|-----------|-----------|
| ¿Tus datos tienen muchas relaciones? | ✅ Sí | ❌ No | ⚠️ Parcial | ❌ No |
| ¿Necesitas traversals profundos? | ✅ Sí | ❌ No | ❌ No | ❌ No |
| ¿Las relaciones cambian frecuentemente? | ✅ Sí | ❌ No | ⚠️ Parcial | ❌ No |
| ¿Necesitas path finding? | ✅ Sí | ⚠️ Complicado | ❌ No | ❌ No |
| ¿Datos mayormente independientes? | ❌ No | ✅ Sí | ✅ Sí | ✅ Sí |
| ¿Consultas simples key-value? | ❌ No | ⚠️ Overkill | ⚠️ Overkill | ✅ Sí |

### 1.4 Casos de Uso

#### Redes Sociales
```
(Usuario)-[:AMIGO_DE]->(Usuario)
(Usuario)-[:ME_GUSTA]->(Publicacion)
(Usuario)-[:COMENTA]->(Publicacion)
(Usuario)-[:SIGUE]->(Usuario)
```

**Consultas típicas:**
- "Amigos de amigos"
- "Personas que conoces y también son amigos de Ana"
- "Comunidad de personas conectadas"
- "Influencers (nodos con más conexiones)"

#### Sistemas de Recomendación
```
(Usuario)-[:COMPRO]->(Producto)
(Producto)-[:CATEGORIZADO_EN]->(Categoria)
(Producto)-[:SIMILAR_A]->(Producto)
(Usuario)-[:VALORO {estrellas: 5}]->(Producto)
```

**Consultas típicas:**
- "Productos que compraste y son similares a este"
- "Usuarios similares a ti también compraron..."
- "Recomendaciones personalizadas"

#### Detección de Fraude
```
(Persona)-[:TIENE_CUENTA]->(Cuenta)
(Cuenta)-[:TRANSACCION_A]->(Cuenta)
(Persona)-[:VIVE_EN]->(Direccion)
(Cuenta)-[:USADA_EN]->(Dispositivo)
```

**Consultas típicas:**
- "Cuentas que comparten el mismo dispositivo"
- "Patrones de transacciones sospechosas"
- "Grupos de personas conectadas por direcciones"

#### Knowledge Graphs
```
(Concepto)-[:ES_UN_TIPO_DE]->(Concepto)
(Concepto)-[:TIENE_ATRIBUTO]->(Atributo)
(Documento)-[:MENCIONA]->(Concepto)
(Persona)-[:AUTOR_DE]->(Documento)
```

### 1.5 Comparación con SQL: JOINs vs Traversals

```sql
-- SQL: Consulta de amigos de amigos
-- Necesita múltiples JOINs (O(n*m) en el peor caso)
SELECT DISTINCT u3.nombre
FROM usuarios u1
JOIN amistades a1 ON u1.id = a1.usuario_id
JOIN amistades a2 ON a1.amigo_id = a2.usuario_id
JOIN usuarios u3 ON a2.amigo_id = u3.id
WHERE u1.nombre = 'Juan'
  AND u3.nombre != 'Juan';
```

```cypher
// Neo4j: Misma consulta como traversal (O(1) por relación)
MATCH (juan:Persona {nombre: 'Juan'})-[:AMIGO_DE]->()-[:AMIGO_DE]->(fof:Persona)
WHERE fof.nombre <> 'Juan'
RETURN DISTINCT fof.nombre
```

**Rendimiento comparativo:**

| Profundidad | SQL (JOINs) | Neo4j (Traversal) |
|-------------|-------------|-------------------|
| 2 niveles | ~100ms | ~2ms |
| 3 niveles | ~1000ms | ~5ms |
| 4 niveles | ~10000ms | ~10ms |
| 5 niveles | ~100000ms | ~15ms |

> **Con Neo4j, la profundidad de la consulta NO afecta significativamente el rendimiento**. En SQL, cada nivel de JOIN multiplica el tiempo de ejecución.

### 1.6 Propiedades del Grafo

| Propiedad | Definición | Ejemplo |
|-----------|-----------|---------|
| **Densidad** | Relaciones existentes / relaciones posibles | Grafo denso: muchos amigos. Grafo sparse: pocos amigos |
| **Grado de nodo** | Número de relaciones de un nodo | Juan tiene grado 5 (5 amigos) |
| **Grado promedio** | Grado total / número de nodos | En red social promedio: 150 amigos |
| **Camino (Path)** | Secuencia de nodos y relaciones conectados | Juan → Ana → Pedro |
| **Camino más corto** | Path con menos aristas entre dos nodos | Juan → Luis (3 saltos) |
| **Componente conectada** | Subgrafo donde todos los nodos están conectados | Amigos de Facebook |
| **Ciclo** | Path que empieza y termina en el mismo nodo | Juan → Ana → Luis → Juan |
| **Subgrafo** | Conjunto de nodos y relaciones dentro del grafo | "Mis amigos" es un subgrafo |

---

## 2. Instalación

### 2.1 Docker (Recomendado para desarrollo)

```bash
# Neo4j Community (gratis)
docker run -d \
  --name neo4j \
  -p 7474:7474 \
  -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/mi_password_segura \
  -e NEO4J_PLUGINS='["apoc"]' \
  -v neo4j_data:/data \
  -v neo4j_logs:/logs \
  neo4j:5

# Neo4j Enterprise (licencia comercial)
docker run -d \
  --name neo4j-enterprise \
  -p 7474:7474 \
  -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/mi_password_segura \
  neo4j:5-enterprise
```

**Puertos:**

| Puerto | Protocolo | Uso |
|--------|-----------|-----|
| **7474** | HTTP | Neo4j Browser (interfaz web) |
| **7687** | Bolt | Conexiones de cliente (cypher-shell, drivers) |

**Variables de entorno importantes:**

| Variable | Descripción |
|----------|-------------|
| `NEO4J_AUTH` | Usuario/contraseña (default: neo4j/neo4j) |
| `NEO4J_PLUGINS` | Plugins a instalar (APOC, GDS, etc.) |
| `NEO4J_apoc_import_file_enabled` | Habilitar importación de archivos |
| `NEO4J_dbms_memory_heap_initial__size` | Heap inicial |
| `NEO4J_dbms_memory_heap_max__size` | Heap máximo |
| `NEO4J_dbms_memory_pagecache_size` | Tamaño del page cache |

### 2.2 Ubuntu/Debian

```bash
# Agregar repositorio de Neo4j
wget -O - https://debian.neo4j.com/neotechnology.gpg.key | sudo gpg --dearmor -o /usr/share/keyrings/neo4j-keyring.gpg

echo "deb [signed-by=/usr/share/keyrings/neo4j-keyring.gpg] https://debian.neo4j.com stable latest" | sudo tee /etc/apt/sources.list.d/neo4j.list

# Actualizar e instalar
sudo apt update
sudo apt install neo4j

# Iniciar servicio
sudo systemctl start neo4j
sudo systemctl enable neo4j

# Estado del servicio
sudo systemctl status neo4j
```

### 2.3 Windows

```bash
# Opción 1: Neo4j Desktop (GUI)
# Descargar desde https://neo4j.com/download/
# Ejecutar instalador y crear un DBMS local

# Opción 2: Chocolatey
choco install neo4j

# Opción 3: Scoop
scoop bucket add neo4j https://github.com/neo4j/scoop-neo4j.git
scoop install neo4j
```

### 2.4 Verificación

```bash
# Verificar instalación con cypher-shell
cypher-shell -u neo4j -p mi_password_segura

# Consulta de prueba
MATCH (n) RETURN count(n);

# Verificar versión
CALL dbms.components() YIELD name, versions
RETURN name, versions;
```

**Salida esperada:**
```
+--------------------------+-----------+
| name                     | versions  |
+--------------------------+-----------+
| "Neo4j Kernel"           | ["5.x.x"] |
| "Community Edition"      | ["5.x.x"] |
+--------------------------+-----------+
```

**Acceder a Neo4j Browser:**
```
http://localhost:7474
```

### 2.5 Neo4j Desktop vs Community vs Enterprise

| Característica | Desktop | Community | Enterprise |
|---------------|---------|-----------|------------|
| **Precio** | Gratis | Gratis | Comercial |
| **Uso** | Desarrollo local | Servidor | Producción |
| **Clustering** | No | No | Sí (Causal Clustering) |
| **Backup** | Manual | Manual | Automático |
| **Monitorización** | Básica | Básica | Avanzada |
| **Security** | Básica | Básica | RBAC, LDAP, SSL |
| **Multi-tenancy** | No | No | Sí |
| **Soporte** | Comunidad | Comunidad | Profesional |

---

## 3. Neo4j Browser

### 3.1 Interfaz Web

Neo4j Browser es la interfaz web incluida con Neo4j. Accede a: `http://localhost:7474`

```
┌─────────────────────────────────────────────────────────┐
│ Neo4j Browser                                     ─ □ × │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────────────────────────────────────────┐   │
│  │ $ MATCH (n) RETURN n LIMIT 25                    │   │
│  │                                                  │   │
│  └──────────────────────────────────────────────────┘   │
│                                                         │
│  [▶ Ejecutar]  [Limpiar]  [ historial]  [ configurar] │
│                                                         │
│  ┌─────────────┬──────────────┬───────────────────┐    │
│  │  Graph      │  Table       │  Text             │    │
│  ├─────────────┼──────────────┼───────────────────┤    │
│  │  🟢🔴🔵    │  id | name   │  {name: "Juan"}   │    │
│  │  ●───●      │  1 | Juan    │  {name: "Ana"}    │    │
│  │  │   │      │  2 | Ana     │                    │    │
│  │  ●───●      │  3 | Luis    │                    │    │
│  └─────────────┴──────────────┴───────────────────┘    │
│                                                         │
│  ┌──────────────────────────────────────────────────┐   │
│  │ Information │ Node Labels │ Relationship Types   │   │
│  │ Nodes: 5    │ Persona: 3   │ AMIGO_DE: 4         │   │
│  │ Rels: 4     │ Empresa: 2   │ TRABAJA_EN: 2       │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

### 3.2 Crear Nodos Visualmente

1. Haz clic derecho en el canvas
2. Selecciona "Add node"
3. Selecciona el label (ej: `:Persona`)
4. Agrega propiedades
5. Arrastra desde el nodo para crear relaciones

### 3.3 Ejecutar Cypher

Escribe consultas Cypher en la barra de comandos y haz clic en "▶ Ejecutar" o presiona `Ctrl+Enter`.

### 3.4 Visualizar Grafos

- **Modo Graph**: Visualización gráfica del grafo
- **Modo Table**: Resultados en tabla
- **Modo Text**: Resultados en texto
- **Modo Code**: Resultado como JSON/Cypher

### 3.5 Guías y Referencias

Neo4j Browser incluye guías integradas:
- **:play intro** - Introducción a Neo4j
- **:play cypher** - Tutorial de Cypher
- **:play northwind** - Ejemplo con datos de Northwind
- **:help** - Comandos de ayuda

---

## 4. Modelo de Datos (Detallado)

### 4.1 Diagrama del Modelo de Datos

```mermaid
classDiagram
    class Persona {
        UUID id
        String nombre
        String email
        Integer edad
        String ciudad
    }

    class Empresa {
        UUID id
        String nombre
        String sector
        Integer empleados
    }

    class Producto {
        UUID id
        String nombre
        Float precio
        String categoria
    }

    class Categoria {
        UUID id
        String nombre
        String descripcion
    }

    class Publicacion {
        UUID id
        String contenido
        DateTime fecha
    }

    Persona "0..*" --> "0.." Empresa : TRABAJA_EN
    Persona "0..*" --> "0.." Persona : AMIGO_DE
    Persona "0..*" --> "0.." Producto : COMPRO
    Persona "0..*" --> "0..* Publicacion : PUBLICO
    Persona "0..*" --> "0..* Publicacion : ME_GUSTA
    Producto "0..*" --> "0..1" Categoria : PERTENECE_A
    Producto "0..*" --> "0..* Producto : SIMILAR_A
```

### 4.2 Ejemplo Completo: Modelo de Red Social

```cypher
// ============ CREAR NODOS ============

// Personas
CREATE (juan:Persona {nombre: "Juan García", email: "juan@mail.com", edad: 30, ciudad: "Madrid"})
CREATE (ana:Persona {nombre: "Ana López", email: "ana@mail.com", edad: 28, ciudad: "Barcelona"})
CREATE (pedro:Persona {nombre: "Pedro Martínez", email: "pedro@mail.com", edad: 35, ciudad: "Madrid"})
CREATE (maria:Persona {nombre: "María Rodríguez", email: "maria@mail.com", edad: 26, ciudad: "Valencia"})
CREATE (luis:Persona {nombre: "Luis Sánchez", email: "luis@mail.com", edad: 32, ciudad: "Sevilla"})
CREATE (carmen:Persona {nombre: "Carmen Fernández", email: "carmen@mail.com", edad: 29, ciudad: "Bilbao"})
CREATE (diego:Persona {nombre: "Diego Hernández", email: "diego@mail.com", edad: 31, ciudad: "Málaga"})
CREATE (laura:Persona {nombre: "Laura Moreno", email: "laura@mail.com", edad: 27, ciudad: "Zaragoza"})
CREATE (pablo:Persona {nombre: "Pablo Jiménez", email: "pablo@mail.com", edad: 33, ciudad: "Madrid"})
CREATE (sofia:Persona {nombre: "Sofía Ruiz", email: "sofia@mail.com", edad: 25, ciudad: "Barcelona"})

// Empresas
CREATE (techcorp:Empresa {nombre: "TechCorp", sector: "Tecnología", empleados: 500})
CREATE (banco:Empresa {nombre: "BancoCentral", sector: "Finanzas", empleados: 1000})
CREATE (startup:Empresa {nombre: "StartupLab", sector: "Innovación", empleados: 50})

// ============ CREAR RELACIONES ============

// Amistades
CREATE (juan)-[:AMIGO_DE {desde: date("2018-01-15")}]->(ana)
CREATE (juan)-[:AMIGO_DE {desde: date("2019-03-20")}]->(pedro)
CREATE (juan)-[:AMIGO_DE {desde: date("2020-06-10")}]->(maria)
CREATE (ana)-[:AMIGO_DE {desde: date("2018-05-25")}]->(luis)
CREATE (ana)-[:AMIGO_DE {desde: date("2019-11-30")}]->(carmen)
CREATE (pedro)-[:AMIGO_DE {desde: date("2020-01-05")}]->(diego)
CREATE (maria)-[:AMIGO_DE {desde: date("2021-02-14")}]->(laura)
CREATE (maria)-[:AMIGO_DE {desde: date("2020-08-20")}]->(pablo)
CREATE (luis)-[:AMIGO_DE {desde: date("2019-07-04")}]->(sofia)
CREATE (carmen)-[:AMIGO_DE {desde: date("2020-12-25")}]->(pablo)
CREATE (diego)-[:AMIGO_DE {desde: date("2021-03-10")}]->(laura)
CREATE (pablo)-[:AMIGO_DE {desde: date("2018-09-15")}]->(sofia)
CREATE (laura)-[:AMIGO_DE {desde: date("2020-04-01")}]->(diego)

// Trabajos
CREATE (juan)-[:TRABAJA_EN {cargo: "Senior Dev", desde: 2019}]->(techcorp)
CREATE (ana)-[:TRABAJA_EN {cargo: "Product Manager", desde: 2020}]->(techcorp)
CREATE (pedro)-[:TRABAJA_EN {cargo: "Analista", desde: 2018}]->(banco)
CREATE (maria)-[:TRABAJA_EN {cargo: "CEO", desde: 2021}]->(startup)
CREATE (luis)-[:TRABAJA_EN {cargo: "DevOps", desde: 2020}]->(startup)
CREATE (carmen)-[:TRABAJA_EN {cargo: "Data Scientist", desde: 2019}]->(techcorp)

// ============ CONSULTAS BÁSICAS ============

// Ver todos los nodos
MATCH (n) RETURN n LIMIT 25;

// Ver todas las relaciones
MATCH ()-[r]->() RETURN r LIMIT 25;

// Ver el grafo completo (peligroso en grafos grandes)
MATCH (n)-[r]->(m) RETURN n, r, m;
```

---

## 5. Cypher: Lenguaje de Consulta (MUY Detallado)

### 5.1 Creación (CREATE y MERGE)

#### CREATE: Crear nodos y relaciones

```cypher
// Nodo simple
CREATE (n:Persona {nombre: "Nuevo Usuario", edad: 25})

// Múltiples nodos de una vez
CREATE
  (a:Persona {nombre: "Alice", edad: 30}),
  (b:Persona {nombre: "Bob", edad: 25}),
  (c:Empresa {nombre: "MiEmpresa", sector: "Tech"}),
  (a)-[:TRABAJA_EN {desde: 2020}]->(c),
  (a)-[:AMIGO_DE {desde: 2019}]->(b)

// Nodo con múltiples labels
CREATE (p:Persona:Empleado:Gerente {
  nombre: "Carlos",
  edad: 40,
  email: "carlos@empresa.com"
})
```

#### MERGE: Crear si no existe

```cypher
// Crear nodo solo si no existe (basado en propiedades de Match)
MERGE (p:Persona {email: "nuevo@mail.com"})
ON CREATE SET p.creado = datetime(), p.nombre = "Nuevo"
ON MATCH SET p.ultimo_acceso = datetime()

// Crear relación solo si no existe
MERGE (a:Persona {email: "a@mail.com"})
MERGE (b:Persona {email: "b@mail.com"})
MERGE (a)-[:AMIGO_DE]->(b)

// MERGE con relación con propiedades
MERGE (a:Persona {email: "a@mail.com"})
MERGE (b:Persona {email: "b@mail.com"})
MERGE (a)-[r:AMIGO_DE]->(b)
ON CREATE SET r.desde = date()
ON MATCH SET r.ultima_interaccion = datetime()
```

> **REGLA DE ORO**: Usa `MERGE` cuando no estés seguro si el nodo/relación ya existe. Usa `CREATE` cuando estás seguro de que es nuevo.

### 5.2 Lectura (MATCH ... RETURN)

#### Consultas básicas

```cypher
// Todos los nodos de un label
MATCH (p:Persona) RETURN p;

// Todas las propiedades
MATCH (p:Persona) RETURN p.nombre, p.edad, p.email;

// Primeros 10 resultados
MATCH (p:Persona) RETURN p.nombre, p.edad LIMIT 10;

// Sin duplicados
MATCH (p:Persona) RETURN DISTINCT p.ciudad;

// Ordenar por edad
MATCH (p:Persona) RETURN p.nombre, p.edad ORDER BY p.edad DESC;

// Paginación
MATCH (p:Persona) RETURN p.nombre, p.edad ORDER BY p.edad SKIP 10 LIMIT 5;
```

#### WHERE: Filtrado

```cypher
// Operadores de comparación
MATCH (p:Persona) WHERE p.edad > 30 RETURN p.nombre;
MATCH (p:Persona) WHERE p.edad >= 28 AND p.edad <= 35 RETURN p.nombre;
MATCH (p:Persona) WHERE p.ciudad = "Madrid" RETURN p.nombre;
MATCH (p:Persona) WHERE p.ciudad <> "Madrid" RETURN p.nombre;

// CONTAINS, STARTS WITH, ENDS WITH
MATCH (p:Persona) WHERE p.nombre CONTAINS "an" RETURN p.nombre;
MATCH (p:Persona) WHERE p.nombre STARTS WITH "J" RETURN p.nombre;
MATCH (p:Persona) WHERE p.email ENDS WITH "@mail.com" RETURN p.nombre;

// IN (lista de valores)
MATCH (p:Persona) WHERE p.ciudad IN ["Madrid", "Barcelona"] RETURN p.nombre;

// IS NULL / IS NOT NULL
MATCH (p:Persona) WHERE p.telefono IS NOT NULL RETURN p.nombre;
MATCH (p:Persona) WHERE p.email IS NULL RETURN p.nombre;

// Funciones de texto
MATCH (p:Persona) WHERE toLower(p.nombre) CONTAINS "juan" RETURN p.nombre;
MATCH (p:Persona) WHERE size(p.nombre) > 10 RETURN p.nombre;
MATCH (p:Persona) WHERE length(p.email) > 15 RETURN p.nombre;

// Funciones de nodo
MATCH (p:Persona) WHERE 'Empleado' IN labels(p) RETURN p.nombre;
MATCH (p:Persona) WHERE exists(p.email) RETURN p.nombre;

// Combinar condiciones
MATCH (p:Persona)
WHERE (p.edad > 25 AND p.ciudad = "Madrid")
   OR (p.edad > 30 AND p.ciudad = "Barcelona")
RETURN p.nombre, p.edad, p.ciudad;
```

#### Patrones de Ruta

```cypher
// Ruta básica: amigos directos
MATCH (juan:Persona {nombre: "Juan"})-[:AMIGO_DE]->(amigo:Persona)
RETURN amigo.nombre;

// Ruta con filtro en la relación
MATCH (juan:Persona {nombre: "Juan"})-[r:AMIGO_DE]->(amigo:Persona)
WHERE r.desde > date("2019-01-01")
RETURN amigo.nombre, r.desde;

// Ruta variable: amigos de amigos (hasta 3 saltos)
MATCH (juan:Persona {nombre: "Juan"})-[:AMIGO_DE*1..3]->(fof:Persona)
WHERE fof.nombre <> "Juan"
RETURN DISTINCT fof.nombre, fof.ciudad;

// Ruta inversa: quién es amigo de Juan
MATCH (otro:Persona)-[:AMIGO_DE]->(juan:Persona {nombre: "Juan"})
RETURN otro.nombre;

// Ruta con intermediarios
MATCH path = (juan:Persona {nombre: "Juan"})-[:AMIGO_DE*]->(destino:Persona {nombre: "Sofía"})
RETURN path, length(path) AS saltos;

// Path más corto (BFS - Breadth First Search)
MATCH path = shortestPath(
  (juan:Persona {nombre: "Juan"})-[:AMIGO_DE*]-(destino:Persona {nombre: "Sofía"})
)
RETURN path, length(path) AS distancia;

// Todos los caminos más cortos
MATCH path = allShortestPaths(
  (juan:Persona {nombre: "Juan"})-[:AMIGO_DE*]-(destino:Persona {nombre: "Sofía"})
)
RETURN path, length(path) AS distancia;

// Extraer nodos y relaciones del path
MATCH path = (juan:Persona {nombre: "Juan"})-[:AMIGO_DE*2]->(destino:Persona)
RETURN nodes(path) AS nodos_en_camino,
       relationships(path) AS relaciones_en_camino,
       length(path) AS profundidad;
```

#### WITH: Encadenar Operaciones

`WITH` pasa resultados de una cláusula a la siguiente, permitiendo encadenar operaciones.

```cypher
// Filtrar después de una agregación
MATCH (p:Persona)-[:AMIGO_DE]->(amigo:Persona)
WITH p, count(amigo) AS num_amigos
WHERE num_amigos > 2
RETURN p.nombre, num_amigos
ORDER BY num_amigos DESC;

// Pasar datos entre cláusulas
MATCH (juan:Persona {nombre: "Juan"})-[:AMIGO_DE]->(amigo:Persona)
WITH amigo
MATCH (amigo)-[:TRABAJA_EN]->(empresa:Empresa)
RETURN amigo.nombre, empresa.nombre;

// Límite de resultados por grupo
MATCH (p:Persona)-[:AMIGO_DE]->(amigo:Persona)
WITH p, collect(amigo.nombre) AS amigos
WHERE size(amigos) > 2
RETURN p.nombre, amigos
LIMIT 5;
```

#### OPTIONAL MATCH

```cypher
// LEFT JOIN de Cypher: incluir resultados aunque no haya match
MATCH (p:Persona)
OPTIONAL MATCH (p)-[:TRABAJA_EN]->(e:Empresa)
RETURN p.nombre, e.nombre AS empresa;
// Si p no tiene relación TRABAJA_EN, empresa será NULL

// Múltiples OPTIONAL MATCH
MATCH (p:Persona)
OPTIONAL MATCH (p)-[:AMIGO_DE]->(amigo:Persona)
OPTIONAL MATCH (p)-[:TRABAJA_EN]->(empresa:Empresa)
RETURN p.nombre, collect(DISTINCT amigo.nombre) AS amigos, empresa.nombre AS empresa;
```

#### UNWIND

```cypher
// Expandir una lista en filas
UNWIND [1, 2, 3, 4, 5] AS numero
RETURN numero;

// Crear múltiples nodos desde una lista
UNWIND [
  {nombre: "Alice", edad: 30},
  {nombre: "Bob", edad: 25},
  {nombre: "Charlie", edad: 35}
] AS datos
CREATE (p:Persona {nombre: datos.nombre, edad: datos.edad})
RETURN p;

// Convertir cadena a lista y expandir
MATCH (p:Persona)
WITH p, split(p.nombre, " ") AS palabras
UNWIND palabras AS palabra
RETURN p.nombre, palabra;
```

### 5.3 Filtrado y Agregación

```cypher
// count() - Contar nodos
MATCH (p:Persona) RETURN count(p);
MATCH (p:Persona) RETURN count(p) AS total_personas;

// count(DISTINCT ...) - Contar únicos
MATCH (p:Persona)-[:AMIGO_DE]->(amigo:Persona)
RETURN p.nombre, count(DISTINCT amigo) AS amigos_unicos;

// collect() - Recoger en lista
MATCH (p:Persona)-[:AMIGO_DE]->(amigo:Persona)
RETURN p.nombre, collect(amigo.nombre) AS lista_amigos;

// collect(DISTINCT ...) - Sin duplicados
MATCH (p:Persona)-[:TRABAJA_EN]->(e:Empresa)
RETURN e.nombre, collect(DISTINCT p.nombre) AS empleados;

// Funciones de agregación
MATCH (p:Persona) RETURN avg(p.edad) AS edad_promedio;
MATCH (p:Persona) RETURN min(p.edad) AS menor, max(p.edad) AS mayor;
MATCH (p:Persona) RETURN sum(p.edad) AS suma_edades;

// CASE WHEN
MATCH (p:Persona)
RETURN p.nombre,
  CASE
    WHEN p.edad < 25 THEN "Joven"
    WHEN p.edad < 35 THEN "Adulto"
    ELSE "Mayor"
  END AS categoria;

// Porcentaje
MATCH (p:Persona)
WITH p, CASE
  WHEN p.edad < 25 THEN "Joven"
  WHEN p.edad < 35 THEN "Adulto"
  ELSE "Mayor"
END AS categoria
RETURN categoria, count(p) AS cantidad,
       round(100.0 * count(p) / (SELECT count(*) FROM Persona), 2) AS porcentaje;
```

### 5.4 Actualización (SET, REMOVE, DELETE)

#### SET: Actualizar propiedades y labels

```cypher
// Actualizar una propiedad
MATCH (p:Persona {nombre: "Juan García"})
SET p.edad = 31;

// Actualizar múltiples propiedades
MATCH (p:Persona {nombre: "Juan García"})
SET p.edad = 31, p.ciudad = "Barcelona", p.actualizado = datetime();

// Agregar label a nodo existente
MATCH (p:Persona {nombre: "Juan García"})
SET p:Empleado:Gerente;

// Copiar propiedades de un nodo a otro
MATCH (source:Persona {nombre: "Juan García"})
MATCH (target:Persona {nombre: "Ana López"})
SET target = source;

// Incrementar propiedad
MATCH (p:Persona {nombre: "Juan García"})
SET p.edad = p.edad + 1;
```

#### REMOVE: Eliminar propiedades y labels

```cypher
// Eliminar una propiedad
MATCH (p:Persona {nombre: "Juan García"})
REMOVE p.telefono;

// Eliminar un label
MATCH (p:Persona {nombre: "Juan García"})
REMOVE p:Gerente;

// Eliminar múltiples propiedades
MATCH (p:Persona {nombre: "Juan García"})
REMOVE p.temp_field1, p.temp_field2;
```

#### DELETE: Eliminar nodos y relaciones

```cypher
// Eliminar una relación específica
MATCH (a:Persona {nombre: "Juan García"})-[r:AMIGO_DE]->(b:Persona {nombre: "Ana López"})
DELETE r;

// Eliminar un nodo (solo si no tiene relaciones)
MATCH (p:Persona {nombre: "Temporal"})
DELETE p;
// Error si tiene relaciones: "Cannot delete node because it still has relationships"

// DETACH DELETE: Eliminar nodo y todas sus relaciones
MATCH (p:Persona {nombre: "Temporal"})
DETACH DELETE p;

// Eliminar todos los nodos y relaciones (PELIGROSO)
MATCH (n) DETACH DELETE n;

// Eliminar con condición
MATCH (p:Persona)
WHERE p.edad < 18
DETACH DELETE p;

// Crear y eliminar en la misma consulta
MATCH (p:Persona {nombre: "Juan García"})
CREATE (n:Copia {nombre: p.nombre, email: p.email})
DELETE p
RETURN n;
```

### 5.5 Ejemplo Completo: Red Social

```cypher
// ============ FASE 1: CREAR GRAFO ============

// Crear 10 usuarios
UNWIND [
  {nombre: "Juan García", edad: 30, ciudad: "Madrid", email: "juan@mail.com"},
  {nombre: "Ana López", edad: 28, ciudad: "Barcelona", email: "ana@mail.com"},
  {nombre: "Pedro Martínez", edad: 35, ciudad: "Madrid", email: "pedro@mail.com"},
  {nombre: "María Rodríguez", edad: 26, ciudad: "Valencia", email: "maria@mail.com"},
  {nombre: "Luis Sánchez", edad: 32, ciudad: "Sevilla", email: "luis@mail.com"},
  {nombre: "Carmen Fernández", edad: 29, ciudad: "Bilbao", email: "carmen@mail.com"},
  {nombre: "Diego Hernández", edad: 31, ciudad: "Málaga", email: "diego@mail.com"},
  {nombre: "Laura Moreno", edad: 27, ciudad: "Zaragoza", email: "laura@mail.com"},
  {nombre: "Pablo Jiménez", edad: 33, ciudad: "Madrid", email: "pablo@mail.com"},
  {nombre: "Sofía Ruiz", edad: 25, ciudad: "Barcelona", email: "sofia@mail.com"}
] AS datos
CREATE (p:Persona {
  nombre: datos.nombre,
  edad: datos.edad,
  ciudad: datos.ciudad,
  email: datos.email,
  creado: datetime()
});

// Crear relaciones de amistad
MATCH (juan:Persona {nombre: "Juan García"})
MATCH (ana:Persona {nombre: "Ana López"})
MATCH (pedro:Persona {nombre: "Pedro Martínez"})
MATCH (maria:Persona {nombre: "María Rodríguez"})
MATCH (luis:Persona {nombre: "Luis Sánchez"})
MATCH (carmen:Persona {nombre: "Carmen Fernández"})
MATCH (diego:Persona {nombre: "Diego Hernández"})
MATCH (laura:Persona {nombre: "Laura Moreno"})
MATCH (pablo:Persona {nombre: "Pablo Jiménez"})
MATCH (sofia:Persona {nombre: "Sofía Ruiz"})
CREATE
  (juan)-[:AMIGO_DE {desde: date("2018-01-15")}]->(ana),
  (juan)-[:AMIGO_DE {desde: date("2019-03-20")}]->(pedro),
  (juan)-[:AMIGO_DE {desde: date("2020-06-10")}]->(maria),
  (ana)-[:AMIGO_DE {desde: date("2018-05-25")}]->(luis),
  (ana)-[:AMIGO_DE {desde: date("2019-11-30")}]->(carmen),
  (pedro)-[:AMIGO_DE {desde: date("2020-01-05")}]->(diego),
  (maria)-[:AMIGO_DE {desde: date("2021-02-14")}]->(laura),
  (maria)-[:AMIGO_DE {desde: date("2020-08-20")}]->(pablo),
  (luis)-[:AMIGO_DE {desde: date("2019-07-04")}]->(sofia),
  (carmen)-[:AMIGO_DE {desde: date("2020-12-25")}]->(pablo),
  (diego)-[:AMIGO_DE {desde: date("2021-03-10")}]->(laura),
  (pablo)-[:AMIGO_DE {desde: date("2018-09-15")}]->(sofia),
  (laura)-[:AMIGO_DE {desde: date("2020-04-01")}]->(diego);

// ============ FASE 2: CONSULTAS ============

// 1. Amigos directos de Juan
MATCH (juan:Persona {nombre: "Juan García"})-[:AMIGO_DE]->(amigo:Persona)
RETURN amigo.nombre, amigo.ciudad, amigo.edad
ORDER BY amigo.nombre;

// Resultado esperado:
// ┌─────────────────────┬─────────────┬──────────┐
// │ amigo.nombre        │ amigo.ciudad│ amigo.edad│
// ├─────────────────────┼─────────────┼──────────┤
// │ "Ana López"         │ "Barcelona" │ 28       │
// │ "María Rodríguez"   │ "Valencia"  │ 26       │
// │ "Pedro Martínez"    │ "Madrid"    │ 35       │
// └─────────────────────┴─────────────┴──────────┘

// 2. Amigos de amigos (2 saltos)
MATCH (juan:Persona {nombre: "Juan García"})-[:AMIGO_DE*2]->(fof:Persona)
WHERE fof.nombre <> "Juan García"
RETURN DISTINCT fof.nombre, fof.ciudad;

// 3. Mutual friends: personas que son amigos de ambos Juan y Ana
MATCH (juan:Persona {nombre: "Juan García"})-[:AMIGO_DE]->(mutual:Persona)<-[:AMIGO_DE]-(ana:Persona {nombre: "Ana López"})
WHERE mutual <> juan AND mutual <> ana
RETURN mutual.nombre;

// 4. Path más corto entre Juan y Sofía
MATCH path = shortestPath(
  (juan:Persona {nombre: "Juan García"})-[:AMIGO_DE*]-(sofia:Persona {nombre: "Sofía Ruiz"})
)
RETURN path, length(path) AS saltos,
       [n IN nodes(path) | n.nombre] AS nombres_en_camino;

// 5. Personas con más amigos
MATCH (p:Persona)-[:AMIGO_DE]-(amigo:Persona)
RETURN p.nombre, count(DISTINCT amigo) AS num_amigos
ORDER BY num_amigos DESC
LIMIT 5;

// Resultado esperado:
// ┌─────────────────────┬────────────┐
// │ p.nombre            │ num_amigos │
// ├─────────────────────┼────────────┤
// │ "Juan García"       │ 3          │
// │ "Ana López"         │ 3          │
// │ "María Rodríguez"   │ 3          │
// │ "Pedro Martínez"    │ 2          │
// │ "Luis Sánchez"      │ 2          │
// └─────────────────────┴────────────┘

// 6. Ciudad con más personas
MATCH (p:Persona)
RETURN p.ciudad, count(p) AS personas
ORDER BY personas DESC;

// 7. Red de Juan: todos los nodos alcanzables
MATCH (juan:Persona {nombre: "Juan García"})-[:AMIGO_DE*1..5]->(conectado:Persona)
RETURN DISTINCT conectado.nombre, conectado.ciudad;

// 8. Personas aisladas (sin amigos)
MATCH (p:Persona)
WHERE NOT (p)-[:AMIGO_DE]-()
RETURN p.nombre, p.ciudad;
```

---

## 6. Índices y Constraints

### 6.1 CREATE INDEX

Los índices mejoran el rendimiento de las consultas WHERE y MATCH.

```cypher
// Índice en una propiedad
CREATE INDEX FOR (p:Persona) ON (p.email);

// Índice compuesto (múltiples propiedades)
CREATE INDEX FOR (p:Persona) ON (p.ciudad, p.edad);

// Índice para búsqueda de texto completo
CREATE FULLTEXT INDEX persona_nombre_email FOR (p:Persona) ON EACH [p.nombre, p.email];

// Verificar índices existentes
SHOW INDEXES;

// Usar índice en consulta
MATCH (p:Persona {email: "juan@mail.com"}) RETURN p.nombre;
// La consulta anterior usa el índice automáticamente
```

### 6.2 CREATE CONSTRAINT

```cypher
// Constraint de unicidad (también crea índice)
CREATE CONSTRAINT constraint_email_unique
FOR (p:Persona)
REQUIRE p.email IS UNIQUE;

// Constraint de existencia
CREATE CONSTRAINT constraint_nombre_exists
FOR (p:Persona)
REQUIRE p.nombre IS NOT NULL;

// Constraint de tipo (Enterprise Edition)
CREATE CONSTRAINT constraint_edad_range
FOR (p:Persona)
REQUIRE p.edad IS INTEGER
IS ALSO >= 0
IS ALSO <= 150;

// Verificar constraints
SHOW CONSTRAINTS;

// Ejemplo de uso
CREATE (p:Persona {email: "juan@mail.com", nombre: "Juan"});
CREATE (p:Persona {email: "juan@mail.com", nombre: "Otro Juan"});
// Error:违反 unique constraint
```

### 6.3 DROP INDEX / DROP CONSTRAINT

```cypher
// Eliminar índice por nombre
DROP INDEX persona_email;

// Eliminar constraint por nombre
DROP CONSTRAINT constraint_email_unique;

// Eliminar índice de texto completo
DROP INDEX persona_nombre_email;
```

### 6.4 Impacto en Rendimiento

| Consulta | Sin Índice | Con Índice |
|----------|-----------|------------|
| `MATCH (p:Persona {email: "x"})` | Full scan O(n) | Index lookup O(log n) |
| `MATCH (p:Persona) WHERE p.edad > 30` | Full scan O(n) | Index scan O(log n + m) |
| `MATCH (p:Persona)-[:AMIGO_DE]->()` | Full scan O(n) | Relationship traversal O(1) |

---

## 7. Ejercicio Práctico

### Ejercicio 1: Instalar Neo4j con Docker

```bash
# Ejecutar Neo4j con APOC plugin
docker run -d \
  --name neo4j-curso \
  -p 7474:7474 \
  -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/curso123 \
  -e NEO4J_PLUGINS='["apoc"]' \
  -e NEO4J_apoc_import_file_enabled=true \
  -v neo4j_data:/data \
  -v neo4j_logs:/logs \
  neo4j:5

# Esperar a que esté listo (~30 segundos)
# Acceder a http://localhost:7474
# Login: neo4j / curso123

# Conectar con cypher-shell
cypher-shell -u neo4j -p curso123
```

### Ejercicio 2: Crear Grafo de Red Social (20 usuarios, 30 relaciones)

```cypher
// Crear 20 usuarios
UNWIND [
  {nombre: "Juan García", edad: 30, ciudad: "Madrid"},
  {nombre: "Ana López", edad: 28, ciudad: "Barcelona"},
  {nombre: "Pedro Martínez", edad: 35, ciudad: "Madrid"},
  {nombre: "María Rodríguez", edad: 26, ciudad: "Valencia"},
  {nombre: "Luis Sánchez", edad: 32, ciudad: "Sevilla"},
  {nombre: "Carmen Fernández", edad: 29, ciudad: "Bilbao"},
  {nombre: "Diego Hernández", edad: 31, ciudad: "Málaga"},
  {nombre: "Laura Moreno", edad: 27, ciudad: "Zaragoza"},
  {nombre: "Pablo Jiménez", edad: 33, ciudad: "Madrid"},
  {nombre: "Sofía Ruiz", edad: 25, ciudad: "Barcelona"},
  {nombre: "Carlos Díaz", edad: 40, ciudad: "Madrid"},
  {nombre: "Elena Vargas", edad: 24, ciudad: "Valencia"},
  {nombre: "Miguel Torres", edad: 36, ciudad: "Sevilla"},
  {nombre: "Isabel Ramos", edad: 29, ciudad: "Bilbao"},
  {nombre: "Andrés Morales", edad: 38, ciudad: "Málaga"},
  {nombre: "Nuria Castro", edad: 26, ciudad: "Zaragoza"},
  {nombre: "Roberto Silva", edad: 34, ciudad: "Madrid"},
  {nombre: "Lucía Herrera", edad: 27, ciudad: "Barcelona"},
  {nombre: "Fernando Reyes", edad: 41, ciudad: "Valencia"},
  {nombre: "Marta Ortiz", edad: 23, ciudad: "Sevilla"}
] AS datos
CREATE (p:Persona {
  nombre: datos.nombre,
  edad: datos.edad,
  ciudad: datos.ciudad,
  email: toLower(replace(datos.nombre, ' ', '.')) + '@mail.com'
});

// Crear 30 relaciones de amistad
MATCH (usuarios:Persona)
WITH collect(usuarios) AS lista_usuarios
UNWIND range(0, 29) AS i
WITH lista_usuarios,
     toInteger(rand() * size(lista_usuarios)) AS idx1,
     toInteger(rand() * size(lista_usuarios)) AS idx2
WITH lista_usuarios[idx1] AS u1, lista_usuarios[idx2] AS u2
WHERE u1 <> u2
MERGE (u1)-[r:AMIGO_DE {desde: date() + duration({days: toInteger(rand() * 1000)})}]->(u2)
RETURN count(r) AS relaciones_creadas;

// Verificar el grafo
MATCH (p:Persona) RETURN count(p) AS total_usuarios;
MATCH ()-[r:AMIGO_DE]->() RETURN count(r) AS total_amistades;
```

### Ejercicio 3: Consultar Amigos, Amigos de Amigos, Mutual Friends

```cypher
// 1. Amigos directos de Juan
MATCH (juan:Persona {nombre: "Juan García"})-[:AMIGO_DE]->(amigo)
RETURN amigo.nombre, amigo.ciudad
ORDER BY amigo.nombre;

// 2. Amigos de amigos (2 saltos)
MATCH (juan:Persona {nombre: "Juan García"})-[:AMIGO_DE*2]->(fof)
WHERE fof <> juan
RETURN DISTINCT fof.nombre, fof.ciudad;

// 3. Amigos de amigos de amigos (3 saltos)
MATCH (juan:Persona {nombre: "Juan García"})-[:AMIGO_DE*3]->(conectado)
WHERE conectado <> juan
RETURN DISTINCT conectado.nombre, conectado.ciudad;

// 4. Mutual friends entre Juan y Ana
MATCH (juan:Persona {nombre: "Juan García"})-[:AMIGO_DE]->(mutual)<-[:AMIGO_DE]-(ana:Persona {nombre: "Ana López"})
WHERE mutual <> juan AND mutual <> ana
RETURN mutual.nombre AS amigo_en_comun;

// 5. Conteo de amigos de amigos
MATCH (juan:Persona {nombre: "Juan García"})-[:AMIGO_DE*2]->(fof)
WHERE fof <> juan
RETURN fof.nombre, count(*) AS veces_conectado
ORDER BY veces_conectado DESC;
```

### Ejercicio 4: Crear Grafo de Productos + Compras

```cypher
// Crear categorías
CREATE (tecnologia:Categoria {nombre: "Tecnología"})
CREATE (libros:Categoria {nombre: "Libros"})
CREATE (ropa:Categoria {nombre: "Ropa"})
CREATE (deportes:Categoria {nombre: "Deportes"});

// Crear productos
UNWIND [
  {nombre: "Laptop HP", precio: 899.99, cat: "Tecnología"},
  {nombre: "iPhone 15", precio: 1199.99, cat: "Tecnología"},
  {nombre: "Auriculares Sony", precio: 299.99, cat: "Tecnología"},
  {nombre: "El Principito", precio: 12.99, cat: "Libros"},
  {nombre: "Cien Años de Soledad", precio: 15.99, cat: "Libros"},
  {nombre: "Camiseta Nike", precio: 35.00, cat: "Ropa"},
  {nombre: "Jeans Levi's", precio: 89.99, cat: "Ropa"},
  {nombre: "Balón Adidas", precio: 29.99, cat: "Deportes"},
  {nombre: "Raqueta Wilson", precio: 149.99, cat: "Deportes"},
  {nombre: "Tablet Samsung", precio: 449.99, cat: "Tecnología"}
] AS datos
CREATE (prod:Producto {nombre: datos.nombre, precio: datos.precio})
WITH prod, datos.cat AS cat_nombre
MATCH (c:Categoria {nombre: cat_nombre})
CREATE (prod)-[:PERTENECE_A]->(c);

// Crear relaciones de compra
MATCH (juan:Persona {nombre: "Juan García"})
MATCH (ana:Persona {nombre: "Ana López"})
MATCH (pedro:Persona {nombre: "Pedro Martínez"})
MATCH (lapHP:Producto {nombre: "Laptop HP"})
MATCH (iphone:Producto {nombre: "iPhone 15"})
MATCH (auriculares:Producto {nombre: "Auriculares Sony"})
MATCH (principito:Producto {nombre: "El Principito"})
MATCH (cien:Producto {nombre: "Cien Años de Soledad"})
MATCH (camiseta:Producto {nombre: "Camiseta Nike"})
MATCH (jeans:Producto {nombre: "Jeans Levi's"})
MATCH (balon:Producto {nombre: "Balón Adidas"})
MATCH (raqueta:Producto {nombre: "Raqueta Wilson"})
MATCH (tablet:Producto {nombre: "Tablet Samsung"})
CREATE
  (juan)-[:COMPRO {fecha: date("2024-01-15"), cantidad: 1}]->(lapHP),
  (juan)-[:COMPRO {fecha: date("2024-02-20"), cantidad: 1}]->(auriculares),
  (juan)-[:COMPRO {fecha: date("2024-03-10"), cantidad: 2}]->(principito),
  (ana)-[:COMPRO {fecha: date("2024-01-20"), cantidad: 1}]->(iphone),
  (ana)-[:COMPRO {fecha: date("2024-02-15"), cantidad: 1}]->(camiseta),
  (ana)-[:COMPRO {fecha: date("2024-03-05"), cantidad: 1}]->(balon),
  (pedro)-[:COMPRO {fecha: date("2024-01-25"), cantidad: 1}]->(tablet),
  (pedro)-[:COMPRO {fecha: date("2024-02-10"), cantidad: 1}]->(cien),
  (pedro)-[:COMPRO {fecha: date("2024-03-01"), cantidad: 1}]->(raqueta);

// ============ CONSULTAS ============

// Productos más populares (más compras)
MATCH (p:Producto)<-[:COMPRO]-(comprador:Persona)
RETURN p.nombre, p.precio, count(comprador) AS num_compras
ORDER BY num_compras DESC;

// Qué compró cada usuario
MATCH (u:Persona)-[c:COMPRO]->(p:Producto)
RETURN u.nombre, collect(p.nombre) AS productos_comprados;

// Usuarios que compraron tecnología
MATCH (u:Persona)-[:COMPRO]->(p:Producto)-[:PERTENECE_A]->(c:Categoria {nombre: "Tecnología"})
RETURN u.nombre, collect(p.nombre) AS tecnologia_comprada;

// Productos en la misma categoría que algo que compró Juan
MATCH (juan:Persona {nombre: "Juan García"})-[:COMPRO]->(p:Producto)-[:PERTENECE_A]->(c:Categoria)
MATCH (otro:Producto)-[:PERTENECE_A]->(c)
WHERE NOT (juan)-[:COMPRO]->(otro)
RETURN otro.nombre, otro.precio, c.nombre AS categoria
ORDER BY c.nombre;
```

### Ejercicio 5: Path Más Corto entre Dos Usuarios

```cypher
// Path más corto entre Juan y Sofía
MATCH path = shortestPath(
  (juan:Persona {nombre: "Juan García"})-[:AMIGO_DE*]-(sofia:Persona {nombre: "Sofía Ruiz"})
)
RETURN
  [n IN nodes(path) | n.nombre] AS camino,
  length(path) AS saltos,
  [r IN relationships(path) | r.desde] AS fechas_amistad;

// Todos los paths de longitud <= 4 entre Juan y Sofía
MATCH path = (juan:Persona {nombre: "Juan García"})-[:AMIGO_DE*1..4]-(sofia:Persona {nombre: "Sofía Ruiz"})
WHERE length(path) <= 4
RETURN
  [n IN nodes(path) | n.nombre] AS camino,
  length(path) AS saltos
ORDER BY saltos;

// Distancia promedio entre todos los pares de usuarios
MATCH (p1:Persona), (p2:Persona)
WHERE p1 <> p2
OPTIONAL MATCH path = shortestPath((p1)-[:AMIGO_DE*]-(p2))
RETURN avg(length(path)) AS distancia_promedio;

// El par de usuarios más alejado
MATCH (p1:Persona), (p2:Persona)
WHERE p1 <> p2
OPTIONAL MATCH path = shortestPath((p1)-[:AMIGO_DE*]-(p2))
RETURN p1.nombre, p2.nombre, length(path) AS distancia
ORDER BY distancia DESC
LIMIT 5;
```

### Ejercicio 6: Crear Índices y Constraints

```cypher
// Crear índice de unicidad en email
CREATE CONSTRAINT constraint_email
FOR (p:Persona)
REQUIRE p.email IS UNIQUE;

// Crear índice en nombre para búsquedas rápidas
CREATE INDEX index_nombre
FOR (p:Persona)
ON (p.nombre);

// Crear índice en ciudad
CREATE INDEX index_ciudad
FOR (p:Persona)
ON (p.ciudad);

// Crear índice de texto completo
CREATE FULLTEXT INDEX fulltext_nombre
FOR (p:Persona)
ON EACH [p.nombre];

// Crear índice en precio de productos
CREATE INDEX index_precio
FOR (p:Producto)
ON (p.precio);

// Ver todos los índices
SHOW INDEXES;

// Ver todos los constraints
SHOW CONSTRAINTS;
```

### Ejercicio 7: Medir Rendimiento con y Sin Índices

```cypher
// Sin índice en nombre (full scan)
// Primero eliminar el índice temporalmente
DROP INDEX index_nombre;

// Medir tiempo de búsqueda (usar PROFILE o EXPLAIN)
PROFILE MATCH (p:Persona {nombre: "Juan García"}) RETURN p;
// Ejecutar varias veces y observar "db hits" en el plan de ejecución

// Recrear índice
CREATE INDEX index_nombre FOR (p:Persona) ON (p.nombre);

// Medir de nuevo
PROFILE MATCH (p:Persona {nombre: "Juan García"}) RETURN p;
// Ahora debería mostrar "db hits: 1" en lugar de escanear todos los nodos

// Comparar con EXPLAIN (solo muestra plan, no ejecuta)
EXPLAIN MATCH (p:Persona {nombre: "Juan García"}) RETURN p;

// Con índice: verás "NodeIndexSeek"
// Sin índice: verás "AllNodesScan"

// Búsqueda de texto completo (requiere FULLTEXT INDEX)
CALL db.index.fulltext.queryNodes("fulltext_nombre", "Juan") YIELD node, score
RETURN node.nombre, score
ORDER BY score DESC;
```

---

## Resumen de la Clase 12

| Tema | Puntos Clave |
|------|-------------|
| **Modelo de Grafo** | Nodos + Relaciones + Propiedades + Labels |
| **Cypher** | CREATE, MATCH, WHERE, RETURN, MERGE, SET, DELETE |
| **Rutas** | shortestPath, allShortestPaths, variable length paths |
| **Agregación** | count, collect, avg, sum, CASE WHEN |
| **WITH** | Encadenar operaciones, pasar datos entre cláusulas |
| **Índices** | CREATE INDEX para búsquedas frecuentes |
| **Constraints** | UNIQUE, IS NOT NULL para integridad de datos |

---

*Próxima clase: Neo4j II — Avanzado, Algoritmos y Rendimiento*
