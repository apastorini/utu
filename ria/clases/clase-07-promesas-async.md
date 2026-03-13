# 📱 Clase 07: Promesas, Async/Await y Callbacks

**Duración:** 4 horas  
**Objetivo:** Dominar la programación asincrónica en JavaScript  
**Proyecto:** Sistema de gestión de eventos asincrónico

---

## 📚 Contenido Teórico

### 1. Fundamentos de Programación Asincrónica

#### 1.1 ¿Qué es la Programación Asincrónica?

La programación asincrónica permite que tu código no bloquee la ejecución mientras espera operaciones lentas.

```
┌─────────────────────────────────────────────────────────────────────┐
│               SINCRÓNICO vs ASINCRÓNICO                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   SINCRÓNICO (BLOQUEANTE)                                           │
│   ─────────────────────────                                          │
│   ┌─────────────────────────────────────────────────────────────┐   │
│   │ console.log('1. Inicio');                                  │   │
│   │ const datos = leerArchivoSync('datos.json');  ← BLOQUEA   │   │
│   │ console.log('2. Datos:', datos);                          │   │
│   │ console.log('3. Fin');                                    │   │
│   └─────────────────────────────────────────────────────────────┘   │
│   Tiempo: [----leer archivo----][mostrar datos]                   │
│                                                                      │
│   ──────────────────────────────────────────────────────────────── │
│                                                                      │
│   ASINCRÓNICO (NO BLOQUEANTE)                                       │
│   ──────────────────────────────                                     │
│   ┌─────────────────────────────────────────────────────────────┐   │
│   │ console.log('1. Inicio');                                  │   │
│   │ leerArchivoAsync((err, datos) => {               ← NO    │   │
│   │     console.log('2. Datos:', datos);             │ BLOQUEA│   │
│   │ });                                                        │   │
│   │ console.log('3. Fin');         ← Se ejecuta INMEDIATO    │   │
│   └─────────────────────────────────────────────────────────────┘   │
│   Tiempo: [leer archivo en paralelo] [mostrar datos]               │
│   └──────────────────────────────────────────────┘                  │
│   La línea 3 se ejecuta ANTES de que termine la lectura           │
│                                                                      │
│   CASOS DE USO:                                                     │
│   ────────────                                                     │
│   • Solicitudes HTTP (fetch, axios)                                │
│   • Lectura/escritura de archivos                                  │
│   • Consultas a bases de datos                                     │
│   • Temporizadores (setTimeout, setInterval)                       │
│   • WebSockets                                                     │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

### 2. Callbacks

#### 2.1 ¿Qué son los Callbacks?

Un **callback** es una función que se pasa como argumento a otra función y se ejecuta después de que termine una operación.

```javascript
// Estructura de callback
function operacionAsincrona(parametros, callback) {
    // Hacer algo...
    if (error) {
        callback(error, null);
    } else {
        callback(null, resultado);
    }
}

// Usar callback
operacionAsincrona(datos, (error, resultado) => {
    if (error) {
        console.error('Error:', error);
    } else {
        console.log('Resultado:', resultado);
    }
});
```

#### 2.2 Callback Hell

El "Callback Hell" ocurre cuando hay muchos callbacks anidados:

```javascript
// MALO - Callback Hell
getDatosUsuario(id, (err, usuario) => {
    if (err) { handleError(err); return; }
    
    getEventosUsuario(usuario.id, (err, eventos) => {
        if (err) { handleError(err); return; }
        
        getReservasUsuario(usuario.id, (err, reservas) => {
            if (err) { handleError(err); return; }
            
            // Mucho más anidado...
        });
    });
});

// SOLUCIÓN: Promesas o async/await
```

---

### 3. Promesas

#### 3.1 ¿Qué son las Promesas?

Una **Promise** representa un valor que puede estar disponible ahora, en el futuro, o nunca.

```
┌─────────────────────────────────────────────────────────────────────┐
│                      ESTADOS DE UNA PROMESA                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   ┌─────────────┐                                                   │
│   │  PENDING    │                                                   │
│   │ (Pendiente) │                                                   │
│   └──────┬──────┘                                                   │
│          │ fulfilled                                                │
│          ▼                                                         │
│   ┌─────────────┐                                                   │
│   │  FULFILLED  │                                                   │
│   │ (Resuelta)  │ ────► .then()                                    │
│   └─────────────┘                                                   │
│          │ rejected                                                 │
│          ▼                                                         │
│   ┌─────────────┐                                                   │
│   │  REJECTED   │                                                   │
│   │ (Rechazada) │ ────► .catch()                                  │
│   └─────────────┘                                                   │
│                                                                      │
│   CREAR UNA PROMESA:                                                │
│   ─────────────────                                                 │
│   const miPromesa = new Promise((resolve, reject) => {            │
│       // Hacer algo asíncrono                                      │
│       if (exitoso) {                                               │
│           resolve(resultado);                                      │
│       } else {                                                     │
│           reject(new Error('Error!'));                             │
│       }                                                             │
│   });                                                              │
│                                                                      │
│   USAR UNA PROMESA:                                                 │
│   ───────────────                                                  │
│   miPromesa                                                        │
│       .then(resultado => console.log(resultado))                   │
│       .catch(error => console.error(error));                      │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

#### 3.2 Métodos de Promesas

```javascript
// .then() - Ejecutar cuando se resuelve
fetch('/api/eventos')
    .then(response => response.json())
    .then(data => console.log(data));

// .catch() - Manejar errores
fetch('/api/eventos')
    .then(response => response.json())
    .catch(error => console.error(error));

// .finally() - Siempre se ejecuta
fetch('/api/eventos')
    .then(data => console.log(data))
    .catch(error => console.error(error))
    .finally(() => console.log('Completado'));

// Promise.all() - Ejecutar en paralelo
Promise.all([
    fetch('/api/usuarios').then(r => r.json()),
    fetch('/api/eventos').then(r => r.json()),
    fetch('/api/reservas').then(r => r.json())
]).then(([usuarios, eventos, reservas]) => {
    // Todos listos
});

// Promise.race() - Primera en resolverse
Promise.race([
    fetch('/api/fast'),
    new Promise((_, reject) => setTimeout(reject, 3000))
]).then(result => console.log(result));
```

---

### 4. Async/Await

#### 4.1 Sintaxis Cleaner

**Async/Await** es syntactic sugar sobre promesas que hace el código más legible.

```javascript
// CON PROMESAS
function obtenerEventos() {
    fetch('/api/eventos')
        .then(response => response.json())
        .then(data => {
            console.log(data);
        })
        .catch(error => {
            console.error(error);
        });
}

// CON ASYNC/AWAIT
async function obtenerEventos() {
    try {
        const response = await fetch('/api/eventos');
        const data = await response.json();
        console.log(data);
    } catch (error) {
        console.error(error);
    }
}

// FUNCIÓN ASYNC
async function crearEvento(datos) {
    // 'await' pausa hasta que la promesa se resuelva
    const response = await fetch('/api/eventos', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(datos)
    });
    
    if (!response.ok) {
        throw new Error('Error al crear evento');
    }
    
    return await response.json();
}
```

---

## 📚 Ejercicios

1. Convertir callbacks a promesas
2. Implementar funciones async/await
3. Manejo de errores
4. Ejecutar operaciones en paralelo

---

## 📚 Recursos

- [MDN - Async](https://developer.mozilla.org/es/docs/Web/JavaScript/Reference/Statements/async_function)
- [Promise](https://developer.mozilla.org/es/docs/Web/JavaScript/Reference/Global_Objects/Promise)
