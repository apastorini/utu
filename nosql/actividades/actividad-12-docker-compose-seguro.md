# Actividad 12 — Docker Compose multi-base con credenciales seguras

## Datos generales

- **Duración:** 50 minutos
- **Tipo:** Individual (o parejas)
- **Herramienta de IA:** Libre
- **Requisitos:** Docker Desktop con **Docker Compose** (se instala junto con Docker Desktop)

## Presupuesto de tiempo

| Paso | Tiempo |
|------|--------|
| Leer el marco teórico | 7 min |
| Crear la estructura y el archivo .env | 8 min |
| Escribir el docker-compose.yml | 15 min |
| Levantar y probar todo | 12 min |
| Verificación y entrega | 8 min |

## Objetivos

1. Levantar **varias bases NoSQL juntas** con un solo archivo `docker-compose.yml`.
2. Aislar servicios con **redes** de Docker.
3. Guardar credenciales en un archivo `.env` (nunca en el código).
4. Aplicar el patrón de **secretos** y contraseñas seguras desde el arranque.

---

## Marco teórico

### ¿Qué es Docker Compose?

Docker Compose describe **varios contenedores** en un solo archivo YAML. Un comando (`docker compose up -d`) levanta todo. Cada servicio (MongoDB, Redis, Cassandra, Neo4j) se define con su imagen, puertos, volúmenes, variables de entorno y red.

### Bloques de un compose

| Bloque | Función |
|--------|---------|
| `services:` | lista de contenedores |
| `image:` | imagen a usar |
| `container_name:` | nombre del contenedor |
| `ports:` | mapeo puerto-host:puerto-contenedor |
| `volumes:` | persistencia (o montajes de config) |
| `environment:` | variables de entorno (usuario, contraseñas…) |
| `networks:` | red(es) a las que pertenece |
| `restart:` | política de reinicio |

### Seguridad con variables de entorno

Nunca se escriben contraseñas en el `docker-compose.yml` (quedarían en el repositorio). La buena práctica:

```
.dockerignore y .env  →  credenciales fuera del archivo principal
.gitignore  →  .env no se sube nunca a Git
```

- `.env` define las variables (leído automáticamente por Compose).
- En el `docker-compose.yml` se referencia con `${VARIABLE}`.

### Redes aisladas

En un entorno real, los servicios **internos** (bases) no exponen puertos a internet: solo la app los alcanza dentro de la red Docker. Acá publicamos puertos **solo** para que vos puedas probar desde tu PC. En producción se quitan los `ports`.

---

## Paso a paso

### Paso 1 — Crear la estructura de carpetas

Creá la carpeta `C:\curso-nosql\compose-seguro` y adentro estas subcarpetas:

```
compose-seguro/
├── docker-compose.yml
├── .env
├── .gitignore
└── mongodb/
    └── mongod-init.js
```

### Paso 2 — Crear el archivo `.env` (secretos)

Adentro de `compose-seguro` creá `.env`:

```env
MONGO_USER=admin
MONGO_PASSWORD=SuperClaveMongo2026
REDIS_PASSWORD=SuperClaveRedis2026
CASSANDRA_PASSWORD=SuperClaveCassandra2026
NEO4J_PASSWORD=SuperClaveNeo4j2026
```

### Paso 3 — Crear `.gitignore` (para que los secretos no se suban)

```gitignore
.env
```

### Paso 4 — Crear el script de inicialización de MongoDB

En `mongodb/mongod-init.js`:

```javascript
db = db.getSiblingDB("admin");
db.createUser({
    user: "admin",
    pwd: process.env.MONGO_USER ? "x" : "x", // se reemplaza por variable real en compose
    roles: [{ role: "root", db: "admin" }]
});
```

> En la práctica, las credenciales de Mongo se pasan por **variables de entorno** de la imagen (`MONGO_INITDB_ROOT_USERNAME/PASSWORD`), sin scripts. El script sirve para ver el patrón de init de Docker.

### Paso 5 — Escribir el `docker-compose.yml`

```yaml
services:
  mongodb:
    image: mongo:7
    container_name: db-mongodb
    ports:
      - "27017:27017"
    environment:
      MONGO_INITDB_ROOT_USERNAME: ${MONGO_USER}
      MONGO_INITDB_ROOT_PASSWORD: ${MONGO_PASSWORD}
    volumes:
      - mongo-vol:/data/db
    networks:
      - datos
    restart: unless-stopped

  redis:
    image: redis:7
    container_name: db-redis
    command: redis-server --requirepass ${REDIS_PASSWORD}
    ports:
      - "6379:6379"
    volumes:
      - redis-vol:/data
    networks:
      - datos
    restart: unless-stopped

  cassandra:
    image: cassandra:5
    container_name: db-cassandra
    environment:
      CASSANDRA_PASSWORD: ${CASSANDRA_PASSWORD}
    ports:
      - "9042:9042"
    volumes:
      - cassandra-vol:/var/lib/cassandra
    networks:
      - datos
    restart: unless-stopped

  neo4j:
    image: neo4j:5-community
    container_name: db-neo4j
    environment:
      NEO4J_AUTH: neo4j/${NEO4J_PASSWORD}
      NEO4J_PLUGINS: '["apoc"]'
    ports:
      - "7474:7474"
      - "7687:7687"
    volumes:
      - neo4j-vol:/data
    networks:
      - datos
    restart: unless-stopped

networks:
  datos:

volumes:
  mongo-vol:
  redis-vol:
  cassandra-vol:
  neo4j-vol:
```

> Notá que en ningún lado aparece una contraseña en texto plano: todo viene de `.env`.

### Paso 6 — Levantar todo

Desde la carpeta `compose-seguro`:

```powershell
docker compose up -d
```

Verificá los contenedores:

```powershell
docker compose ps
docker ps
```

### Paso 7 — Probar cada base con sus credenciales

**MongoDB:**

```powershell
docker exec -it db-mongodb mongosh "mongodb://admin:SuperClaveMongo2026@localhost:27017/admin" --eval "db.runCommand({ping:1})"
```

**Redis:**

```powershell
docker exec -it db-redis redis-cli -a "SuperClaveRedis2026" PING
```

**Neo4j:** entrá a http://localhost:7474 con `neo4j` / `SuperClaveNeo4j2026`.

**Cassandra:** entrá y creá el SUPERUSER:

```powershell
docker exec -it db-cassandra cqlsh -u cassandra -p cassandra
```

```sql
ALTER ROLE cassandra WITH PASSWORD = 'SuperClaveCassandra2026';
```

### Paso 8 — Verificar que sin contraseña no entra nadie

```powershell
docker exec -it db-redis redis-cli PING
# → NOAUTH
docker exec -it db-mongodb mongosh --eval "db.runCommand({ping:1})"
# → error de autenticación
```

### Paso 9 — Apagar todo con un comando

```powershell
docker compose down
```

Los volúmenes quedan: los datos persisten. Para borrar también los datos (cuidado):

```powershell
docker compose down -v
```

### Paso 10 — Preguntar a la IA

```
¿Qué diferencia hay entre env_file y environment en docker compose? ¿Cuándo usar cada uno?
¿Qué es Docker secrets y cómo se usaría para no exponer contraseñas ni en el .env?
¿Por qué en producción las bases no publican ports al host? ¿Cómo se conectaría la app a ellas?
```

## Verificación de resultados

- [ ] `docker compose ps` muestra 4 contenedores corriendo.
- [ ] Cada base responde **con** su credencial de `.env`.
- [ ] Sin credenciales, MongoDB y Redis rechazan la conexión.
- [ ] `docker compose down` apaga todo y `down -v` borra los datos.

## Criterios de evaluación

| Criterio | Puntos |
|----------|--------|
| Estructura de carpetas y `.env` correctos | 20 |
| `docker-compose.yml` con 4 servicios | 30 |
| Credenciales desde `.env` (ninguna en texto plano) | 20 |
| Pruebas de conexión autenticada | 20 |
| Reflexión sobre red y producción | 10 |

## Entregable

- Carpeta `compose-seguro` completa (sin `.env` si la vas a compartir; documentá las variables requeridas en un `README.md`).
- Captura de `docker compose ps` y de una prueba autenticada por base.

## Para pensar

Tenés el stack completo corriendo. En las próximas actividades vas a optimizarlo: **índices** (13), **replicación** (14), **sharding** (15) y un **proyecto final** que une todo (16).
