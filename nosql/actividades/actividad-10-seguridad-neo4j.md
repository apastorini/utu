# Actividad 10 — Seguridad en Neo4j: roles, permisos e inyección Cypher

## Datos generales

- **Duración:** 50 minutos
- **Tipo:** Individual
- **Herramienta de IA:** Libre
- **Requisitos:** Neo4j en Docker (Actividad 9)

## Presupuesto de tiempo

| Paso | Tiempo |
|------|--------|
| Leer el marco teórico | 7 min |
| Cambiar contraseña y crear usuarios | 8 min |
| Asignar roles y probar permisos | 12 min |
| Simular una inyección Cypher | 12 min |
| Sanitización y buenas prácticas | 6 min |
| Verificación y entrega | 5 min |

## Objetivos

1. Conocer el sistema de **roles y permisos** de Neo4j (RBAC).
2. Crear usuarios y asignarles roles con acceso limitado.
3. Comprender qué es una **inyección en Cypher** (Cypher injection) y cómo prevenirla.
4. Simular y explotar una inyección en una consulta de login.

---

## Marco teórico

### Seguridad en Neo4j

Neo4j separa **autenticación** (¿quién sos?) de **autorización** (¿qué podés hacer?):

| Capa | Control |
|------|---------|
| Autenticación | usuarios + contraseñas (o LDAP/SSO en ediciones enterprise) |
| Autorización | **roles** con permisos por tipo de operación y por ámbito |
| Transporte | cifrado TLS (bolt) para no leer credenciales en la red |
| Auditoría | logs de accesos y operaciones |
| Validación | no concatenar entradas del usuario en consultas Cypher |

### Roles nativos de Neo4j

| Rol | Permisos |
|-----|----------|
| `reader` | leer todos los datos |
| `editor` | leer, crear y actualizar datos (no borrar) |
| `publisher` | todo lo de editor + borrar datos |
| `architect` | todo lo de publisher + administrar índices y constraints |
| `admin` | acceso total |

> En producción, cada aplicación usa el **rol mínimo** que necesita. Un dashboard de solo lectura usa `reader`; jamás `admin`.

### Inyección Cypher

Cypher injection es la versión NoSQL de la SQL injection. Si una aplicación arma consultas **concatenando texto** del usuario:

```javascript
// CÓDIGO VULNERABLE
const query = `MATCH (u:Usuario {user: '${user}'}) RETURN u`
```

Un atacante puede inyectar sintaxis y hacer que la consulta devuelva **todos** los usuarios, o borrar datos:

```
' OR 1=1 --
```

**Prevención:** usar **parámetros** (`$param`) — la entrada del usuario va como valor, nunca como código.

```cypher
MATCH (u:Usuario {user: $user}) RETURN u
```

---

## Paso a paso

### Paso 1 — Verificar que Neo4j sigue corriendo

```powershell
docker ps
```

Si no está, levantalo igual que en la Actividad 9. Después entrá al Browser (http://localhost:7474) o usá `cypher-shell`.

### Paso 2 — Cambiar la contraseña del admin

En el Browser, el primer comando:

```cypher
ALTER CURRENT USER SET PASSWORD FROM 'Neo4j123' TO 'NuevaClaveSegura2026';
```

> Con `cypher-shell`, primero entra con la vieja (`-p Neo4j123`) y ejecutá el mismo comando.

### Paso 3 — Crear datos de ejemplo

```cypher
CREATE (ana:Usuario {user: "ana", clave: "hash-anonimizado"})
CREATE (bruno:Usuario {user: "bruno", clave: "hash-anonimizado"})
CREATE (dato1:DatoSensible {valor: "archivo-1-confidencial"})
CREATE (ana)-[:ACCEDE]->(dato1);
```

### Paso 4 — Crear usuarios con roles

Los usuarios se crean con `CREATE USER` (solo `admin` puede):

```cypher
CREATE USER lector SET PASSWORD 'Lector123' SET STATUS ACTIVE;
CREATE USER editor_app SET PASSWORD 'EditorApp123' SET STATUS ACTIVE;
```

> Las contraseñas en `cypher-shell` pueden requerir comillas simples si tienen caracteres especiales. Se admiten letras, números y `._-`.

### Paso 5 — Asignar roles

```cypher
GRANT ROLE reader TO lector;
GRANT ROLE editor TO editor_app;
SHOW ROLES;
SHOW USERS;
```

### Paso 6 — Probar los permisos

Salí y entrá como `lector` (en el Browser te deslogueás; con cypher-shell):

```powershell
docker exec -it neo4j-clase cypher-shell -u lector -p Lector123
```

```cypher
// Puede leer
MATCH (n) RETURN n;

// No puede crear
CREATE (:Usuario {user: "hack"});
// → Debe fallar por permisos
```

Ahora entrá como `editor_app` y probá crear:

```powershell
docker exec -it neo4j-clase cypher-shell -u editor_app -p EditorApp123
```

```cypher
// Puede crear nodos
CREATE (:Usuario {user: "nuevo"});
MATCH (n) RETURN n;
```

### Paso 7 — Ver los permisos exactos de un rol

Con el admin:

```cypher
SHOW ROLE editor PRIVILEGES;
SHOW ROLE reader PRIVILEGES;
```

### Paso 8 — Simular una inyección Cypher (login vulnerable)

Vamos a entender el ataque. Creá la colección de usuarios (ya la tenés). Imaginá una app que arma así la consulta:

```javascript
// CÓDIGO VULNERABLE (solo para entender el ataque)
const query = `MATCH (u:Usuario {user: '${user}', clave: '${clave}'}) RETURN u`
```

**Ataque 1 — autenticación sin conocer la clave.** Si el atacante escribe como `user`:

```
'}) RETURN u//
```

La consulta concatenada queda así (equivalente a lo que ejecuta la app vulnerable):

```cypher
MATCH (u:Usuario {user: ''}) RETURN u//', clave: '...'}) RETURN u
```

En la práctica, el atacante busca que la consulta devuelva un nodo **sin validar la clave**. Simulámoslo con una consulta equivalente que cualquier atacante probaría:

```cypher
// Lo que la app vulnerable ejecutaría con una inyección:
MATCH (u:Usuario)
WHERE u.user = 'ana' OR 1 = 1
RETURN u;
```

Esto devuelve **todos** los usuarios. El `OR 1 = 1` hace que el filtro sea siempre verdadero.

**Ataque 2 — borrado masivo.** Una variante famosa intenta ejecutar un `DETACH DELETE`:

```cypher
// Lo que un atacante intentaría inyectar:
MATCH (u:Usuario {user: 'ana'})
DETACH DELETE u;
// → si la app no valida y ejecuta varias consultas, borra los nodos
```

> No borres los datos reales: corré esta consulta **solo** si querés re-crear los nodos después con el paso 3.

### Paso 9 — La solución: parámetros

La app segura usa parámetros; la entrada del usuario **nunca** se concatena:

```cypher
// Versión segura con parámetro $user
MATCH (u:Usuario {user: $user}) RETURN u;
```

```javascript
// En el código de la app (ejemplo conceptual):
// session.run('MATCH (u:Usuario {user: $user}) RETURN u', { user: userInput })
```

Con parámetros, si el usuario escribe `' OR 1=1 --`, Neo4j lo trata como **texto literal** para buscar, no como código. No hay inyección posible.

### Paso 10 — Preguntar a la IA

```
¿Cuál es la diferencia entre los roles reader, editor y publisher de Neo4j?
¿Cómo haría una API Node.js para ejecutar una consulta Cypher con parámetros y sin inyección?
¿Qué es una constraint de unicidad en Neo4j y cómo evita usuarios duplicados? (CREATE CONSTRAINT)
```

## Verificación de resultados

- [ ] Cambiaste la contraseña del usuario `neo4j`.
- [ ] `lector` puede leer pero no crear nodos.
- [ ] `editor_app` puede crear nodos.
- [ ] `SHOW ROLE reader PRIVILEGES` muestra permisos de solo lectura.
- [ ] Entendés y reproducís la simulación de inyección con `OR 1 = 1`.

## Criterios de evaluación

| Criterio | Puntos |
|----------|--------|
| Usuarios y roles creados | 25 |
| Prueba de permisos (lector vs editor) | 20 |
| Simulación de inyección Cypher | 25 |
| Solución con parámetros explicada | 20 |
| Preguntas a la IA respondidas | 10 |

## Entregable

- Archivo `neo4j-seguridad.cypher` con usuarios, roles, la simulación de inyección y la versión con parámetros.
- Captura del error de permisos de `lector`.
- Respuesta de la IA sobre constraints de unicidad.

## Para pensar

Ya recorriste seguridad en MongoDB, Redis, Cassandra y Neo4j. En la Actividad 12 vas a juntar **varias bases** en un solo `docker-compose.yml` con secretos. Antes, en la Actividad 11, modelás un mismo caso de uso real (e-commerce) en las tres bases.
