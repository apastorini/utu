# Actividad 1 — Instalación de herramientas y Normalización de datos

## Datos generales

- **Duración:** 50 minutos
- **Tipo:** Individual
- **Herramienta de IA:** OpenCode (en esta actividad aprendés a instalarla)
- **Requisitos:** Windows 10/11 con acceso de administrador (o Linux/macOS)

## Presupuesto de tiempo

| Paso | Tiempo |
|------|--------|
| Leer el marco teórico | 5 min |
| Instalar Node.js + OpenCode | 15 min |
| Instalar Docker Desktop | 10 min |
| Ejercicio de normalización con la IA | 15 min |
| Verificación y entrega | 5 min |

## Objetivos

1. Instalar el agente de IA **OpenCode** en tu computadora.
2. Instalar **Docker** para levantar bases de datos NoSQL en clases posteriores.
3. Comprender la **normalización de bases de datos relacionales** (1FN, 2FN, 3FN).
4. Usar la IA por primera vez para resolver un ejercicio de modelado.

---

## Marco teórico

### ¿Por qué normalizar antes de pasar a NoSQL?

Una base de datos relacional (SQL) organiza los datos en **tablas** con filas y columnas. Para evitar **redundancia** (datos repetidos) y **anomalías** (errores al insertar, actualizar o borrar), los modelos se "normalizan". Las formas normales más usadas son:

**1FN — Primera Forma Normal:**
- Cada celda contiene un único valor (atómico).
- No hay grupos repetidos ni listas dentro de una celda.

**2FN — Segunda Forma Normal:**
- Cumple 1FN.
- Cada columna no clave depende de la **clave completa**, no de una parte.

**3FN — Tercera Forma Normal:**
- Cumple 2FN.
- No hay dependencias transitivas: una columna no puede depender de otra columna que no sea la clave.

> Ejemplo clásico de anomalía: guardar `(producto, categoría, precio_categoría)`. Si cambia la categoría, hay que cambiar el precio en todas las filas. Eso se resuelve separando en una tabla `categorías`.

### ¿Por qué NoSQL "desnormaliza"?

Las bases NoSQL **sacrifican** deliberadamente la normalización para ganar velocidad y escalabilidad: los datos se agrupan en **documentos, claves-valor, columnas o grafos** tal como se leen. Entender bien la normalización te ayuda a decidir **cuándo** desnormalizar.

> **Regla práctica:** primero modelás la normalización mentalmente; después decidís cómo agrupar los documentos en NoSQL.

### ¿Qué es OpenCode?

OpenCode es un **agente de programación con IA** open source que se ejecuta en la terminal. Entiende proyectos completos, crea archivos, ejecuta comandos y responde preguntas. Es la herramienta que vas a usar durante todo el curso para resolver consultas, generar datos de prueba y verificar comandos de bases de datos.

---

## Paso a paso

### Parte A — Instalar OpenCode

**Paso 1.** Verificá que tengas **Node.js** instalado. Abrí una terminal (PowerShell) y escribí:

```powershell
node --version
npm --version
```

Si da error, descargá Node.js LTS desde https://nodejs.org y volvé a abrir la terminal.

**Paso 2.** Instalá OpenCode de forma global:

```powershell
npm install -g opencode-ai
```

**Paso 3.** Verificá que quedó instalado:

```powershell
opencode --version
```

> **Si usás Linux/macOS**, el instalador oficial es `curl -fsSL https://opencode.ai/install | bash`. En Windows también funciona `choco install opencode` o `scoop install opencode`.

**Paso 4.** Probá la interfaz. Entrá en una carpeta de trabajo (por ejemplo `C:\curso-nosql`) y ejecutá:

```powershell
opencode
```

**Paso 5.** Configurá un proveedor de IA. Dentro de OpenCode ejecutá:

```
/connect
```

Ahí podés elegir un proveedor y pegar tu API key. Si no tenés, consultá con tu docente cómo obtener una. Con `Esc` salís de la interfaz.

### Parte B — Instalar Docker Desktop

Docker permite ejecutar bases de datos NoSQL (MongoDB, Redis, Cassandra, Neo4j) en contenedores aislados, sin instalar nada directamente en tu PC.

**Paso 6.** Descargá **Docker Desktop** desde https://www.docker.com/products/docker-desktop/ e instalalo.

**Paso 7.** Abrí Docker Desktop, esperá a que el motor arranque y verificá en la terminal:

```powershell
docker version
docker compose version
```

> Si Docker Desktop pide WSL 2, aceptá e instalalo; es gratis y open source. Esta es la única vez que instalás Docker: en todas las actividades siguientes lo único que vas a hacer es levantar contenedores.

**Paso 8.** Probá que Docker funciona con el clásico "hola mundo":

```powershell
docker run --rm hello-world
```

### Parte C — Ejercicio de normalización con la IA

**Paso 9.** Creá un archivo de texto con el problema a resolver. Dentro de OpenCode escribí un mensaje como este:

```
Tenés la siguiente tabla desnormalizada de una biblioteca:

| libro_id | titulo    | autor        | categoria      | socios                  |
|----------|-----------|--------------|----------------|-------------------------|
| 1        | Cien años | G. Márquez   | Literatura     | Ana, Luis               |
| 2        | Dune      | F. Herbert   | Ciencia ficción| Ana                     |
| 1        | Cien años | G. Márquez   | Literatura     | Pedro                   |

1) Normalizala a 1FN, 2FN y 3FN mostrando cada paso.
2) Mostrá las tablas finales en forma de esquema.
3) Explicá qué anomalías de actualización eliminaste.
```

**Paso 10.** Leé la respuesta de la IA. Pedile que te lo **explique de nuevo en tus propias palabras** si algo no quedó claro:

```
Explicame la 3FN con un ejemplo distinto, sin repetir lo anterior.
```

**Paso 11.** Guardá la solución que te dio la IA en un archivo `normalizacion.md` dentro de tu carpeta de trabajo. Para eso pedile a OpenCode:

```
Guardá la solución final del ejercicio de normalización en el archivo normalizacion.md
```

## Verificación de resultados

- [ ] `opencode --version` muestra una versión.
- [ ] `docker run --rm hello-world` imprime el mensaje de Docker.
- [ ] Tenés el archivo `normalizacion.md` con las tablas en 3FN.
- [ ] Podés explicar con tus palabras qué anomalía elimina la 3FN.

## Criterios de evaluación

| Criterio | Puntos |
|----------|--------|
| OpenCode instalado y funcionando | 25 |
| Docker instalado y verificado | 25 |
| Normalización a 3FN correcta (archivo entregado) | 30 |
| Explicación propia de las anomalías eliminadas | 20 |

## Entregable

- Archivo `normalizacion.md` con el ejercicio resuelto.
- Captura de pantalla de `opencode --version` y `docker version`.

---

## Actividades futuras

En las próximas actividades ya **no** vas a instalar herramientas: vas a levantar bases de datos con Docker y consultarlas paso a paso. Podés usar **OpenCode o cualquier otra herramienta de IA** que prefieras (ChatGPT, Claude, Gemini, GitHub Copilot, etc.). La idea del curso es que vos la elijas y la aproveches para aprender más rápido.
