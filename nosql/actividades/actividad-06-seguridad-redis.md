# Actividad 6 — Seguridad en Redis: contraseñas, ACLs y hardening

## Datos generales

- **Duración:** 50 minutos
- **Tipo:** Individual
- **Herramienta de IA:** Libre
- **Requisitos:** Redis en Docker (Actividad 5)

## Presupuesto de tiempo

| Paso | Tiempo |
|------|--------|
| Leer el marco teórico | 7 min |
| Levantar Redis con requirepass | 8 min |
| Conectar y autenticarse | 8 min |
| ACLs: usuarios con permisos | 12 min |
| Renombrar y bloquear comandos | 8 min |
| Verificación y entrega | 7 min |

## Objetivos

1. Conocer por qué Redis es un objetivo frecuente de ataques reales.
2. Proteger Redis con `requirepass` y `protected-mode`.
3. Crear **usuarios ACL** con permisos limitados.
4. **Renombrar/bloquear comandos peligrosos** (`FLUSHALL`, `CONFIG`, `EVAL`, `KEYS`).
5. Restringir el acceso por red.

---

## Marco teórico

### ¿Por qué es tan atacado Redis?

Redis nació **sin autenticación** y con comandos muy poderosos. Durante años, miles de servidores quedaron expuestos en internet por:

- Ejecutarse en el puerto 6379 **sin contraseña**.
- `protected-mode` desactivado o enlaces a todas las interfaces (`bind 0.0.0.0`).

Los ataques típicos:

| Ataque | Cómo lo hace | Daño |
|--------|--------------|------|
| Criptominería | Escribe claves con un cron / `redis-cli` vía `CONFIG SET dir` | Usa tu CPU, instala malware |
| Borrado total | `FLUSHALL` | Pierde todos los datos |
| Ransomware | Guarda una nota de rescate en claves | Extorsión |
| Malware | `EVAL` / scripts Lua maliciosos | Toma control del servidor |

> El famoso `redis-rogue-server` explota servidores sin contraseña para **subir un shell**. Nunca expongas Redis a internet.

### Defensas en capas

1. `requirepass` → contraseña para todo cliente.
2. `protected-mode yes` → solo responde a localhost si no hay contraseña.
3. `bind 127.0.0.1` → escuchar solo en la interfaz local.
4. **ACLs** → cada aplicación con su usuario y permisos.
5. **Renombrar/bloquear comandos peligrosos** → evitar `CONFIG`, `FLUSHALL`, `EVAL`, `KEYS`.
6. **No ejecutar como root** y correr en contenedor aislado (no publicar el puerto si no hace falta).

---

## Paso a paso

### Paso 1 — Crear un archivo de configuración seguro

Creá una carpeta de trabajo `C:\curso-nosql\redis-seguro` y adentro un archivo `redis.conf`:

```conf
# Escuchar solo en la interfaz local del contenedor
bind 127.0.0.1

# Exigir contraseña a todos los clientes
requirepass Clave-Redis-Muy-Segura-2026

# Modo protegido por si falta contraseña
protected-mode yes

# Renombrar (inutilizar) comandos peligrosos
rename-command FLUSHALL ""
rename-command FLUSHDB ""
rename-command CONFIG ""
rename-command EVAL ""
rename-command EVALSHA ""
rename-command KEYS ""
```

> Con `rename-command X ""` el comando queda **deshabilitado por completo**. En un entorno real podrías renombrarlo a algo secreto en vez de vaciarlo.

### Paso 2 — Levantar Redis con esa configuración

Desde `C:\curso-nosql\redis-seguro`:

```powershell
docker rm -f redis-clase

docker run -d --name redis-clase \
  -p 6379:6379 \
  -v ${PWD}:/etc/redis \
  redis:7 redis-server /etc/redis/redis.conf
```

- `-v ${PWD}:/etc/redis` monta tu carpeta con el archivo `.conf`.
- El último argumento ejecuta Redis con tu configuración.

### Paso 3 — Conectar sin contraseña (debe fallar)

```powershell
docker exec -it redis-clase redis-cli
```

Probá:

```bash
PING
```

Deberías ver `NOAUTH Authentication required`. Eso ya es una victoria de seguridad.

### Paso 4 — Conectar autenticado

Salí y reconectá pasando la contraseña:

```powershell
docker exec -it redis-clase redis-cli -a "Clave-Redis-Muy-Segura-2026"
```

O usá `AUTH`:

```bash
AUTH Clave-Redis-Muy-Segura-2026
PING
# → PONG
```

### Paso 5 — Confirmar que los comandos peligrosos están muertos

```bash
FLUSHALL
# → ERR unknown command
CONFIG GET save
# → ERR unknown command
KEYS *
# → ERR unknown command
```

Los comandos que antes eran un peligro ahora **ni siquiera existen**.

### Paso 6 — Crear usuarios ACL con permisos

Los ACL de Redis permiten definir qué comandos y claves puede usar cada usuario.

```bash
# Usuario de solo lectura (puede leer todo, no escribir)
ACL SETUSER lector on >Lector123 ~* +@read

# Usuario de caché (puede leer/escribir en claves que empiecen con "cache:")
ACL SETUSER cache_app on >CacheApp456 ~cache:* +@read +@write -@dangerous

# Usuario administrador (el actual "default" tiene acceso total)
ACL GETUSER default
```

Explicación:

- `on` → usuario activo.
- `>clave` → define la contraseña.
- `~*` → patrón de claves permitidas (`~cache:*` limita a esas).
- `+@read` → permite la categoría de comandos de lectura.
- `-@dangerous` → prohíbe comandos marcados peligrosos.
- `+@write` → permite comandos de escritura.

### Paso 7 — Conectarse como el usuario "cache_app"

```powershell
docker exec -it redis-clase redis-cli -a CacheApp456
```

```bash
# Puede escribir en su patrón de claves
SET cache:perfil:1 "{}"

# Pero no puede tocar claves fuera de su patrón
SET usuario:1 "{}"
# → NOPERM this user has no permissions to access one of the keys used as arguments

# Y no puede usar comandos peligrosos aunque existieran
CONFIG GET save
# → NOPERM
```

### Paso 8 — Listar los usuarios creados

Con el `default`:

```powershell
docker exec -it redis-clase redis-cli -a "Clave-Redis-Muy-Segura-2026"
```

```bash
ACL LIST
ACL USERS
```

### Paso 9 — Simular el escenario "sin seguridad"

Para que veas la diferencia, levantá un Redis temporal **sin protección** y comprobá que `CONFIG SET` funciona (lo que permite el ataque de criptominería):

```powershell
docker run -d --name redis-inseguro -p 6380:6379 redis:7
docker exec -it redis-inseguro redis-cli
```

```bash
CONFIG GET dir          # muestra el directorio
SET nota "te secuestre tus datos"   # ransomware simulado
FLUSHALL
```

```powershell
docker rm -f redis-inseguro
```

### Paso 10 — Preguntar a la IA

```
¿Qué diferencia hay entre requirepass y las ACL de Redis 7? ¿Cuál es más segura?
¿Qué comandos de Redis están marcados como @dangerous y por qué?
¿Cómo quedaría un redis.conf de producción para una app web real?
```

## Verificación de resultados

- [ ] `PING` sin contraseña devuelve `NOAUTH`.
- [ ] Con la contraseña, `PING` devuelve `PONG`.
- [ ] `FLUSHALL`, `CONFIG`, `KEYS` devuelven `unknown command`.
- [ ] El usuario ACL `cache_app` no puede tocar claves fuera de `cache:*`.
- [ ] El Redis inseguro (temporal) permite `CONFIG SET` y fue eliminado al final.

## Criterios de evaluación

| Criterio | Puntos |
|----------|--------|
| redis.conf con requirepass y protected-mode | 20 |
| Renombrado de comandos peligrosos verificado | 25 |
| Usuarios ACL con permisos limitados | 25 |
| Prueba de que el usuario ACL no sale de su patrón | 20 |
| Reflexión sobre el ataque simulado | 10 |

## Entregable

- Archivo `redis-seguro.md` con: el `redis.conf` usado, salidas de `ACL LIST` y capturas de los errores `NOAUTH` / `NOPERM` / `unknown command`.
- Respuesta de la IA sobre la comparación `requirepass` vs ACL.

## Para pensar

En la Actividad 8 vas a ver la seguridad en **Cassandra**, que maneja la autorización de otra forma (GRANT de permisos por tabla). La Actividad 12 une todo con `docker compose` y secretos.
