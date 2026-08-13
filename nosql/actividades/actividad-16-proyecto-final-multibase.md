# Actividad 16 — Proyecto final: API segura multi-base (MongoDB + Redis + Neo4j)

## Datos generales

- **Duración:** 50 minutos
- **Tipo:** Individual o parejas
- **Herramienta de IA:** Libre (idealmente OpenCode en modo Build)
- **Requisitos:** Node.js LTS instalado, Docker funcionando

## Presupuesto de tiempo

| Paso | Tiempo |
|------|--------|
| Leer el marco teórico | 7 min |
| Levantar las 3 bases y el proyecto | 10 min |
| Escribir la API (paso 4-8) | 20 min |
| Probar con curl/PowerShell | 8 min |
| Verificación y reflexión de seguridad | 5 min |

## Objetivos

1. Integrar **MongoDB, Redis y Neo4j** en una sola aplicación.
2. Implementar **autenticación JWT** con sesiones revocables en Redis.
3. Aplicar **buenas prácticas de seguridad** vistas en el curso.
4. Entregar el proyecto integrador de la asignatura.

---

## Marco teórico

### El stack del proyecto

| Capa | Tecnología | Responsabilidad |
|------|------------|-----------------|
| API | Node.js + Express | recibe peticiones, orquesta las bases |
| Documental | MongoDB | usuarios y catálogo de productos |
| Clave-valor | Redis | sesiones (con TTL) para poder "cerrar sesión" |
| Grafos | Neo4j | recomendaciones cruzando compras |
| Autenticación | JWT + bcrypt | tokens firmados y contraseñas hasheadas |

### Por qué JWT + Redis

- **JWT:** un token firmado que la app valida sin consultar una base. Ideal para APIs.
- **El problema:** los JWT **no se pueden revocar** (valen hasta vencer).
- **La solución:** guardamos el token en Redis con `EX` (expiración). El middleware de auth revisa que el token esté en Redis → si se hace logout, se borra y el token muere de inmediato.

```
login ──► emite JWT ──► guarda "sesion:id" en Redis (TTL 1h)
petición ──► verifica JWT (firma) + verifica sesión en Redis
logout ──► borra la clave de Redis ──► el token queda inútil
```

### Checklist de seguridad que aplicás acá

- [x] Contraseñas **hasheadas** con bcrypt (nunca en texto plano).
- [x] JWT con **expiración** y clave secreta en `.env`.
- [x] Sesiones **revocables** en Redis con TTL.
- [x] Consultas con **parámetros** (sin concatenación → sin inyección).
- [x] Sin secretos en el código (todo en `.env`, ignorado por git).
- [x] Mínimo privilegio: cada base con su propio usuario.

---

## Paso a paso

### Paso 1 — Levantar las bases (compose reducido)

Creá `C:\curso-nosql\proyecto-final\docker-compose.yml`:

```yaml
services:
  mongodb:
    image: mongo:7
    container_name: pf-mongo
    ports: ["27017:27017"]
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: ClaveMongoProyecto
    volumes: [pf-mongo:/data/db]

  redis:
    image: redis:7
    container_name: pf-redis
    command: redis-server --requirepass ClaveRedisProyecto
    ports: ["6379:6379"]
    volumes: [pf-redis:/data]

  neo4j:
    image: neo4j:5-community
    container_name: pf-neo4j
    environment:
      NEO4J_AUTH: neo4j/ClaveNeo4jProyecto
    ports: ["7474:7474", "7687:7687"]
    volumes: [pf-neo4j:/data]

volumes:
  pf-mongo:
  pf-redis:
  pf-neo4j:
```

```powershell
docker compose up -d
```

### Paso 2 — Crear el proyecto Node.js

```powershell
npm init -y
npm install express mongodb redis neo4j-driver jsonwebtoken bcryptjs dotenv
```

Creá el archivo `.env`:

```env
MONGO_URL=mongodb://admin:ClaveMongoProyecto@localhost:27017
REDIS_URL=redis://:ClaveRedisProyecto@localhost:6379
NEO4J_URL=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASS=ClaveNeo4jProyecto
JWT_SECRET=una-clave-secreta-muy-larga-y-aleatoria-2026
```

Y `.gitignore` con: `node_modules` y `.env`.

### Paso 3 — Cargar datos de prueba

**MongoDB (catálogo):**

```powershell
docker exec -it pf-mongo mongosh "mongodb://admin:ClaveMongoProyecto@localhost:27017/appsegura" --eval "db.productos.insertMany([{nombre:'Teclado',precio:80},{nombre:'Mouse',precio:35},{nombre:'Monitor',precio:350},{nombre:'Dune',precio:25}])"
```

**Neo4j (relaciones de compra):**

```powershell
docker exec -it pf-neo4j cypher-shell -u neo4j -p ClaveNeo4jProyecto
```

```cypher
CREATE (a:Cliente {nombre:"ana"})-[:COMPRO]->(:Producto {nombre:"Teclado"})
CREATE (a)-[:COMPRO]->(:Producto {nombre:"Mouse"})
CREATE (:Cliente {nombre:"bruno"})-[:COMPRO]->(:Producto {nombre:"Teclado"})
CREATE (:Cliente {nombre:"bruno"})-[:COMPRO]->(:Producto {nombre:"Monitor"});
```

> Si el usuario "ana" va a registrarse en la API, el `nombre` debe coincidir con el que uses en `/registro` y `/login`.

### Paso 4 — Crear `app.js` (la API completa)

```javascript
require('dotenv').config();
const express = require('express');
const jwt = require('jsonwebtoken');
const bcrypt = require('bcryptjs');
const { MongoClient } = require('mongodb');
const { createClient } = require('redis');
const neo4j = require('neo4j-driver');

const app = express();
app.use(express.json());

const mongo = new MongoClient(process.env.MONGO_URL);
const redis = createClient({ url: process.env.REDIS_URL });
const neo = neo4j.driver(process.env.NEO4J_URL,
    neo4j.auth.basic(process.env.NEO4J_USER, process.env.NEO4J_PASS));

(async () => {
    await mongo.connect();
    await redis.connect();
    console.log('MongoDB y Redis conectados');
})();

const db = mongo.db('appsegura');

// Middleware: valida JWT y que la sesión siga viva en Redis
async function auth(req, res, next) {
    const token = (req.headers.authorization || '').replace('Bearer ', '');
    try {
        const payload = jwt.verify(token, process.env.JWT_SECRET);
        const viva = await redis.get(`sesion:${payload.sub}`);
        if (!viva) return res.status(401).json({ error: 'sesion expirada' });
        req.user = payload;
        next();
    } catch (e) {
        res.status(401).json({ error: 'token invalido' });
    }
}

// Registro: hash de la contraseña
app.post('/registro', async (req, res) => {
    const { usuario, clave } = req.body;
    if (!usuario || !clave) return res.status(400).json({ error: 'faltan datos' });
    const hash = await bcrypt.hash(clave, 10);
    await db.usuarios.insertOne({ usuario, hash });
    res.json({ ok: true });
});

// Login: valida, emite JWT y crea sesión en Redis (TTL 1h)
app.post('/login', async (req, res) => {
    const { usuario, clave } = req.body;
    const user = await db.usuarios.findOne({ usuario });
    if (!user || !(await bcrypt.compare(clave, user.hash)))
        return res.status(401).json({ error: 'credenciales invalidas' });
    const token = jwt.sign({ sub: user._id.toString(), usuario },
        process.env.JWT_SECRET, { expiresIn: '1h' });
    await redis.set(`sesion:${user._id}`, token, { EX: 3600 });
    res.json({ token });
});

// Logout: revoca la sesión de inmediato
app.post('/logout', auth, async (req, res) => {
    await redis.del(`sesion:${req.user.sub}`);
    res.json({ ok: true });
});

// Catálogo desde MongoDB (filtro con Number(), sin inyección)
app.get('/productos', auth, async (req, res) => {
    const precioMin = Number(req.query.precioMin) || 0;
    const productos = await db.productos
        .find({ precio: { $gte: precioMin } })
        .limit(20).toArray();
    res.json(productos);
});

// Recomendaciones desde Neo4j (consulta con parámetro $nombre)
app.get('/recomendaciones', auth, async (req, res) => {
    const session = neo.session();
    try {
        const result = await session.run(
            `MATCH (a:Cliente {nombre: $nombre})-[:COMPRO]->(p)
             <-[:COMPRO]-(:Cliente)-[:COMPRO]->(rec)
             WHERE NOT EXISTS((a)-[:COMPRO]->(rec))
             RETURN DISTINCT rec.nombre AS sugerencia LIMIT 5`,
            { nombre: req.user.usuario }
        );
        res.json(result.records.map(r => r.get('sugerencia')));
    } finally {
        session.close();
    }
});

app.listen(3000, () => console.log('API corriendo en http://localhost:3000'));
```

### Paso 5 — Probar la API

```powershell
node app.js
```

En **otra terminal**, probá el flujo completo:

```powershell
# 1. Registrar un usuario
Invoke-RestMethod -Method Post -Uri http://localhost:3000/registro -ContentType "application/json" -Body '{"usuario":"ana","clave":"MiClave123"}'

# 2. Login → guardate el token
$login = Invoke-RestMethod -Method Post -Uri http://localhost:3000/login -ContentType "application/json" -Body '{"usuario":"ana","clave":"MiClave123"}'
$token = $login.token

# 3. Consultar productos (autenticado)
Invoke-RestMethod -Method Get -Uri http://localhost:3000/productos -Headers @{ Authorization = "Bearer $token" }

# 4. Productos con filtro
Invoke-RestMethod -Method Get -Uri "http://localhost:3000/productos?precioMin=50" -Headers @{ Authorization = "Bearer $token" }

# 5. Recomendaciones desde Neo4j
Invoke-RestMethod -Method Get -Uri http://localhost:3000/recomendaciones -Headers @{ Authorization = "Bearer $token" }

# 6. Logout y verificá que el token queda inútil
Invoke-RestMethod -Method Post -Uri http://localhost:3000/logout -Headers @{ Authorization = "Bearer $token" }
Invoke-RestMethod -Method Get -Uri http://localhost:3000/productos -Headers @{ Authorization = "Bearer $token" }
# → debe dar 401 sesion expirada
```

> En Linux/macOS usá `curl -X POST ... -H "Content-Type: application/json" -d '{"usuario":"ana","clave":"MiClave123"}'` con la misma lógica.

### Paso 6 — Verificar la seguridad "por las malas"

```powershell
# Sin token → 401
Invoke-RestMethod -Method Get -Uri http://localhost:3000/productos

# Token inventado → 401
Invoke-RestMethod -Method Get -Uri http://localhost:3000/productos -Headers @{ Authorization = "Bearer abc123" }
```

### Paso 7 — Usar la IA para mejorar

Pedile a tu herramienta de IA:

```
Agregá validación para que /registro rechace usuarios duplicados.
¿Cómo agrego un rate limiter para evitar fuerza bruta en /login?
¿Cómo cambio getShardDistribution por una consulta que muestre los 3 productos más caros?
```

### Paso 8 — Reflexión de seguridad (entrega)

Escribí en `reflexion-seguridad.md`:

1. ¿Por qué las contraseñas van hasheadas y nunca en texto plano?
2. ¿Qué pasaría si el `.env` se subiera a GitHub? ¿Qué riesgo concreto hay?
3. ¿Cómo evita esta API las inyecciones (NoSQL y Cypher)?
4. ¿Qué mejora de seguridad le harías si fuera un sistema real?

## Verificación de resultados

- [ ] `node app.js` inicia y dice "MongoDB y Redis conectados".
- [ ] El registro y login devuelven un token.
- [ ] `/productos` y `/recomendaciones` responden con el token.
- [ ] Después de `/logout` el mismo token devuelve `401 sesion expirada`.
- [ ] Sin token, todo devuelve `401`.

## Criterios de evaluación

| Criterio | Puntos |
|----------|--------|
| Compose multi-base funcionando | 15 |
| API completa (registro, login, logout, productos, recomendaciones) | 35 |
| Flujo JWT + sesión Redis (logout revoca) | 20 |
| Seguridad: hash, .env, parámetros, 401 | 20 |
| Reflexión de seguridad entregada | 10 |

## Entregable

- Proyecto `proyecto-final/` con: `app.js`, `docker-compose.yml`, `.env` (sin subir a git), `.gitignore` y `reflexion-seguridad.md`.
- Captura de los 3 endpoints funcionando (con token).

---

## Cierre del curso

En estas 16 actividades recorriste: normalización y herramientas (1), MongoDB (2-4), Redis (5-6), Cassandra (7-8), Neo4j (9-10), modelado multi-base (11), despliegue seguro con Docker Compose (12), índices (13), replicación (14), sharding (15) y un proyecto integrador seguro (16). Tenés un stack NoSQL completo, open source y 100 % local, listo para usar en tus propios proyectos.
