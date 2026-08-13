# Actividad 14 — Replicación y alta disponibilidad en MongoDB

## Datos generales

- **Duración:** 50 minutos
- **Tipo:** Individual (o parejas)
- **Herramienta de IA:** Libre
- **Requisitos:** Docker funcionando

## Presupuesto de tiempo

| Paso | Tiempo |
|------|--------|
| Leer el marco teórico | 7 min |
| Crear la red y los 3 nodos | 8 min |
| Iniciar el replica set | 8 min |
| Escribir/leer y ver el oplog | 8 min |
| Simular falla de nodo (failover) | 10 min |
| Verificación y entrega | 9 min |

## Objetivos

1. Comprender qué es un **replica set** y la relación **primario/secundarios**.
2. Montar un cluster de 3 nodos MongoDB con Docker.
3. Verificar la **replicación** de datos (oplog) y el **failover**.
4. Entender la **consistencia eventual** entre réplicas.

---

## Marco teórico

### ¿Qué es la replicación?

La replicación mantiene **copias idénticas** de los datos en varios nodos. Si un nodo muere, otro sigue sirviendo: eso es **alta disponibilidad (HA)**.

### Replica set (MongoDB)

```
          ┌────────────┐
          │  PRIMARIO  │  ← único que acepta escrituras
          └─────┬──────┘
     oplog      │ replicación
   ┌────────────┼────────────┐
   ▼            ▼            ▼
┌──────┐    ┌──────┐    ┌──────┐
│ SEC  │    │ SEC  │    │ SEC  │  ← sirven lecturas
└──────┘    └──────┘    └──────┘
```

- **Primario (primary):** único nodo que acepta escrituras.
- **Secundarios (secondary):** copian los datos del primario y sirven lecturas.
- **OpLog:** "Write-Ahead Log" que registra cada operación; los secundarios lo replican en orden.
- **Elección (election):** si el primario cae, los secundarios **eligen** un nuevo primario automáticamente.
- **Votación:** con 3 nodos, hacen falta **mayoría** (2) para elegir. Por eso los replica sets suelen tener **cantidad impar** de miembros.

### Niveles de consistencia

- En el primario: lectura **consistente** (acabás de escribir, lo leés).
- En un secundario: puede haber **eventual consistency** (el dato recién escrito todavía no llegó).
- `readPreference` decide dónde leer: `primary`, `secondary`, `nearest`, etc.

> **Regla:** las lecturas de datos críticos (saldo, sesión) van al primario. Las lecturas pesadas no críticas (reportes) pueden ir a secundarios.

---

## Paso a paso

### Paso 1 — Crear la red y los 3 nodos

```powershell
docker network create mongo-repl

docker run -d --name mongo1 --network mongo-repl -p 27017:27017 mongo:7 --replSet rs0
docker run -d --name mongo2 --network mongo-repl -p 27018:27017 mongo:7 --replSet rs0
docker run -d --name mongo3 --network mongo-repl -p 27019:27017 mongo:7 --replSet rs0
```

- `--network mongo-repl`: los nodos se ven entre sí por nombre.
- `--replSet rs0`: los marca como parte del replica set "rs0".
- Puertos distintos para poder entrar a cada uno desde tu PC.

Esperá unos segundos y verificá que los 3 estén vivos:

```powershell
docker ps
```

### Paso 2 — Iniciar el replica set

Entrá al nodo 1:

```powershell
docker exec -it mongo1 mongosh
```

Inicializá el cluster indicando los 3 miembros (hosts = nombres de contenedor en la red Docker):

```javascript
rs.initiate({
    _id: "rs0",
    members: [
        { _id: 0, host: "mongo1:27017" },
        { _id: 1, host: "mongo2:27017" },
        { _id: 2, host: "mongo3:27017" }
    ]
})
```

### Paso 3 — Ver el estado

```javascript
rs.status()
```

Mirá:

- `myState` del nodo → `1` (PRIMARY).
- Cada miembro con su `health` y `stateStr`.

Esperá a que los 3 estén `PRIMARY`/`SECONDARY` sanos:

```javascript
rs.status().members.forEach(m => print(m.name, m.stateStr, "health:", m.health))
```

### Paso 4 — Escribir en el primario

```javascript
// En mongo1 (primario)
db.ventas.insertOne({ id: 1, cliente: "Ana", total: 150 })
db.ventas.find().pretty()
```

### Paso 5 — Comprobar que el dato llegó a los secundarios

Salí de mongosh y conectá directo al nodo 2:

```powershell
docker exec -it mongo2 mongosh --eval "rs.slaveOk(); db.ventas.find().toArray()"
```

> `rs.slaveOk()` (o `setSecondaryOk()`) permite leer desde un secundario. El dato debería estar ahí porque el oplog ya lo replicó.

### Paso 6 — Ver el oplog (el registro de replicación)

```javascript
// En el primario
db.getSiblingDB("local").oplog.rs.find().sort({ $natural: -1 }).limit(3).forEach(o => printjson(o))
```

El oplog guarda `ts` (timestamp), `op` (`i`=insert, `u`=update, `d`=delete) y `o` (el documento).

### Paso 7 — Probar lecturas en secundario (consistencia eventual)

```powershell
docker exec -it mongo2 mongosh
```

```javascript
db.setSecondaryOk()
db.ventas.find().pretty()
```

### Paso 8 — Simular una falla (failover)

Desde una **nueva terminal**, apagá el primario a la fuerza (simula un crash):

```powershell
docker kill mongo1
```

Esperá ~10-30 s y consultá el estado desde mongo2:

```powershell
docker exec -it mongo2 mongosh --eval "rs.status().members.forEach(m => print(m.name, m.stateStr))"
```

Uno de los secundarios (mongo2 o mongo3) debe haber pasado a **PRIMARY** automáticamente (elección).

Probá que el cluster sigue escribiendo (ahora el primario es otro):

```powershell
docker exec -it mongo2 mongosh --eval "db.ventas.insertOne({ id: 2, cliente: 'Bruno', total: 90 })"
```

### Paso 9 — Volver a levantar el nodo caído

```powershell
docker start mongo1
```

Esperá unos segundos y verificá que vuelve como **SECONDARY** y se **resincroniza** con el nuevo primario:

```powershell
docker exec -it mongo2 mongosh --eval "rs.status().members.forEach(m => print(m.name, m.stateStr))"
```

```powershell
docker exec -it mongo1 mongosh --eval "db.setSecondaryOk(); db.ventas.find().toArray()"
```

El nodo recuperado debería tener las ventas 1 y 2 (se puso al día con el oplog).

### Paso 10 — Preguntar a la IA

```
¿Por qué un replica set necesita mayoría y por eso suele tener cantidad impar de nodos?
¿Qué diferencia hay entre replica set y sharding? ¿Sirven para lo mismo?
¿Qué pasa con las escrituras si quiero tener 2 primarios? ¿Es posible y a qué costo?
```

## Verificación de resultados

- [ ] `rs.status()` muestra 1 PRIMARY y 2 SECONDARY sanos.
- [ ] El dato insertado en el primario aparece en el secundario.
- [ ] El oplog muestra la operación `i`.
- [ ] Tras matar `mongo1`, otro nodo pasa a PRIMARY y el cluster sigue escribiendo.
- [ ] Al volver, `mongo1` se resincroniza como SECONDARY.

## Criterios de evaluación

| Criterio | Puntos |
|----------|--------|
| Red + 3 nodos levantados | 20 |
| Replica set inicializado correctamente | 20 |
| Replicación verificada (dato en secundarios) | 20 |
| Failover simulado y explicado | 25 |
| Recuperación del nodo caído | 15 |

## Entregable

- Archivo `replica-set.md` con: salida de `rs.status()` inicial, la del oplog, y la salida **antes y después** del failover.
- Explicación propia (5 líneas) de por qué el cluster no se quedó sin primario.
- Respuesta de la IA sobre mayoría y cantidad impar de nodos.

## Para pensar

La replicación da **copias**, pero todas viven en un solo cluster. En la Actividad 15 vas a ver **sharding**: partir los datos en varios nodos para escalar horizontalmente, con `mongos` como punto de entrada.
