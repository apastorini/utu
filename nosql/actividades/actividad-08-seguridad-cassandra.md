# Actividad 8 — Seguridad en Cassandra y consultas avanzadas

## Datos generales

- **Duración:** 50 minutos
- **Tipo:** Individual
- **Herramienta de IA:** Libre
- **Requisitos:** Cassandra en Docker (Actividad 7)

## Presupuesto de tiempo

| Paso | Tiempo |
|------|--------|
| Leer el marco teórico | 7 min |
| Levantar Cassandra con autenticación | 10 min |
| Crear roles y permisos (GRANT) | 12 min |
| Probar la autorización por tabla | 8 min |
| Consultas avanzadas CQL | 8 min |
| Verificación y entrega | 5 min |

## Objetivos

1. Activar **autenticación** (`PasswordAuthenticator`) en Cassandra.
2. Crear **roles** y asignar permisos por tabla con `GRANT`/`REVOKE`.
3. Comprobar que un rol limitado **no puede** consultar tablas que no le corresponden.
4. Escribir consultas CQL avanzadas: `IN`, `COUNT`, rangos y funciones.

---

## Marco teórico

### Autenticación y autorización en Cassandra

Por defecto, Cassandra acepta cualquier conexión **sin pedir credenciales**. Se activa con dos archivos de configuración:

| Archivo | Propiedad | Control |
|---------|-----------|---------|
| `cassandra.yaml` | `authenticator: PasswordAuthenticator` | ¿Quién sos? (autenticación) |
| `cassandra.yaml` | `authorizer: CassandraAuthorizer` | ¿Qué podés hacer? (autorización) |

### Roles y permisos

- **Rol (role):** identidad con contraseña y opciones (puede ser `SUPERUSER` o no).
- **Permiso:** lo que un rol puede hacer sobre un objeto (`SELECT`, `INSERT`, `UPDATE`, `DELETE`, `CREATE`, `ALTER`…).
- **GRANT** otorga permiso; **REVOKE** lo quita.
- Los permisos se asignan por **keyspace**, **tabla** o función.

```
GRANT SELECT ON TABLE monitoreo.metricas_servidor TO rol_lector;
```

### Usuario por defecto

Con `PasswordAuthenticator` activado, solo existe el usuario `cassandra` / `cassandra` (SUPERUSER). Lo primero es **cambiarlo**.

### Consultas avanzadas que vamos a ver

- `WHERE ... IN (...)` → varias particiones a la vez.
- `COUNT(*)` → contar (pesado en producción, sirve para prácticas).
- Rango con clustering key → cortar por tiempo.
- `dateOf()` / `toTimestamp()` → manejo de fechas.

---

## Paso a paso

### Paso 1 — Crear la configuración con autenticación

Creá la carpeta `C:\curso-nosql\cassandra-segura` y un `cassandra.yaml` con **solo los cambios** respecto al default:

```yaml
authenticator: PasswordAuthenticator
authorizer: CassandraAuthorizer
```

### Paso 2 — Levantar Cassandra con esa configuración

```powershell
docker rm -f cassandra-clase

docker run -d --name cassandra-clase \
  -p 9042:9042 \
  -v ${PWD}/cassandra-segura:/etc/cassandra \
  cassandra:5
```

> Cassandra 5 lee `cassandra.yaml` desde `/etc/cassandra`. El montaje sobreescribe el archivo original con el tuyo. Esperá 30-60 s hasta que arranque.

### Paso 3 — Conectar como usuario por defecto

```powershell
docker exec -it cassandra-clase cqlsh -u cassandra -p cassandra
```

### Paso 4 — Cambiar la contraseña del SUPERUSER

```sql
ALTER ROLE cassandra WITH PASSWORD = 'Cassandra-Ahora-Segura';
```

> Proba salir y entrar con la nueva contraseña: `cqlsh -u cassandra -p Cassandra-Ahora-Segura`.

### Paso 5 — Crear los objetos base

```sql
CREATE KEYSPACE app_meteorologia
  WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};

USE app_meteorologia;

CREATE TABLE estaciones (
    estacion text,
    fecha timestamp,
    temp double,
    humedad int,
    PRIMARY KEY (estacion, fecha)
);

INSERT INTO estaciones (estacion, fecha, temp, humedad)
VALUES ('cerro', '2026-08-01 08:00:00', 12.5, 70);
INSERT INTO estaciones (estacion, fecha, temp, humedad)
VALUES ('cerro', '2026-08-01 09:00:00', 14.0, 66);
INSERT INTO estaciones (estacion, fecha, temp, humedad)
VALUES ('cerro', '2026-08-01 10:00:00', 16.5, 60);
INSERT INTO estaciones (estacion, fecha, temp, humedad)
VALUES ('prado', '2026-08-01 08:00:00', 11.0, 75);
INSERT INTO estaciones (estacion, fecha, temp, humedad)
VALUES ('prado', '2026-08-01 10:00:00', 15.0, 62);
```

### Paso 6 — Crear roles con permisos

```sql
-- Rol de solo lectura sobre todo el keyspace
CREATE ROLE lector_meteo WITH LOGIN = true AND PASSWORD = 'LectorMeteo123';
GRANT SELECT ON KEYSPACE app_meteorologia TO lector_meteo;

-- Rol de escritura SOLO sobre la tabla estaciones
CREATE ROLE escritor_cerro WITH LOGIN = true AND PASSWORD = 'EscritorCerro123';
GRANT SELECT ON TABLE app_meteorologia.estaciones TO escritor_cerro;
GRANT INSERT ON TABLE app_meteorologia.estaciones TO escritor_cerro;

-- Rol administrador (sin SUPERUSER)
CREATE ROLE admin_meteo WITH LOGIN = true AND PASSWORD = 'AdminMeteo123';
GRANT ALL ON KEYSPACE app_meteorologia TO admin_meteo;
```

### Paso 7 — Probar el rol limitado

Salí y conectate como `escritor_cerro`:

```powershell
docker exec -it cassandra-clase cqlsh -u escritor_cerro -p EscritorCerro123
```

```sql
-- Puede insertar en su tabla
INSERT INTO app_meteorologia.estaciones (estacion, fecha, temp, humedad)
VALUES ('cerro', '2026-08-01 11:00:00', 18.0, 58);

SELECT * FROM app_meteorologia.estaciones WHERE estacion = 'cerro';
```

Ahora intentá **crear** algo (no tiene permiso):

```sql
CREATE KEYSPACE hack WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};
-- → debería dar error Unauthorized: Permission denied
```

E intentá insertar en otra tabla:

```sql
CREATE TABLE app_meteorologia.otra (id int PRIMARY KEY);
-- → Unauthorized
```

### Paso 8 — Revocar un permiso

Con `cassandra` (SUPERUSER):

```sql
REVOKE INSERT ON TABLE app_meteorologia.estaciones FROM escritor_cerro;
```

Probá de nuevo insertar como `escritor_cerro` → ahora debe fallar.

### Paso 9 — Consultas avanzadas CQL

Con `cassandra`:

```sql
USE app_meteorologia;

-- Varias particiones a la vez
SELECT * FROM estaciones WHERE estacion IN ('cerro', 'prado');

-- Rango de tiempo dentro de una partición
SELECT * FROM estaciones
WHERE estacion = 'cerro' AND fecha >= '2026-08-01 09:00:00';

-- Contar (práctica; en producción es caro)
SELECT COUNT(*) FROM estaciones;

-- Todos los datos de la partición 'cerro' ordenados
SELECT estacion, temp, humedad FROM estaciones WHERE estacion = 'cerro';
```

### Paso 10 — Ver los roles creados

```sql
LIST ROLES;
LIST ROLES OF cassandra;
```

### Paso 11 — Preguntar a la IA

```
¿Por qué Cassandra usa roles con GRANT y no los usuarios directos de MongoDB?
¿Cuál es la diferencia entre un rol SUPERUSER y admin_meteo con GRANT ALL sobre un keyspace?
¿Qué pasa si un cluster tiene la autenticación desactivada y se expone a internet?
```

## Verificación de resultados

- [ ] Conectar sin usuario ya no es posible (o da error de autenticación).
- [ ] `escritor_cerro` inserta en `estaciones` pero no puede crear keyspaces.
- [ ] Tras `REVOKE`, el insert del paso 8 falla.
- [ ] `SELECT ... IN ('cerro','prado')` devuelve ambas particiones.
- [ ] `LIST ROLES` muestra los roles creados.

## Criterios de evaluación

| Criterio | Puntos |
|----------|--------|
| Cassandra con autenticación y autorización activadas | 20 |
| Cambio de contraseña del SUPERUSER | 10 |
| Roles y GRANT correctos | 25 |
| Prueba del rol limitado + REVOKE | 20 |
| Consultas avanzadas CQL | 25 |

## Entregable

- Archivo `cassandra-seguridad.cql` con roles, permisos y las capturas de errores `Unauthorized`.
- Respuesta de la IA sobre la diferencia de modelos de seguridad entre Cassandra y MongoDB.

## Para pensar

En la Actividad 10 vas a ver seguridad en **Neo4j** (base de grafos): otra forma de autorización (built-in vs LDAP) y además las **inyecciones en Cypher**. Antes, en la Actividad 9 aprendés a consultar grafos.
