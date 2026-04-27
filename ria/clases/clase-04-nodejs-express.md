# 📱 Clase 04: Node.js, Express y Primeras APIs REST

**Duración:** 4 horas  
**Objetivo:** Crear servidor backend con Node.js y Express, implementar APIs REST  
**Proyecto:** API REST para el sistema de eventos 

---

## 📚 Contenido Teórico

### 1. Fundamentos de Node.js

#### 1.1 ¿Qué es Node.js?

**Node.js** es un runtime de JavaScript basado en el motor V8 de Chrome que permite ejecutar JavaScript en el servidor.

```
┌─────────────────────────────────────────────────────────────────────┐
│                    NODE.JS - VISIÓN GENERAL                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   CARACTERÍSTICAS PRINCIPALES:                                       │
│   ─────────────────────────                                          │
│   • JavaScript en el servidor                                        │
│   • Non-blocking I/O (E/S no bloqueante)                           │
│   • Event Loop (manejo de operaciones asíncronas)                  │
│   • NPM (Node Package Manager) - Mayor ecosistema de librerías       │
│   • Mismo lenguaje en frontend y backend                            │
│                                                                      │
│   ARQUITECTURA:                                                      │
│   ┌──────────────────────────────────────────────┐                  │
│   │                    V8                         │                  │
│   │   ┌────────────────────────────────────┐    │                  │
│   │   │     JavaScript Code                 │    │                  │
│   │   │     ↓ Compilador                    │    │                  │
│   │   │     ↓                                │    │                  │
│   │   │     Machine Code                    │    │                  │
│   │   └────────────────────────────────────┘    │                  │
│   └──────────────────────────────────────────────┘                  │
│   │                      │                        │                  │
│   │    ┌────────────────┴─────────────────┐     │                  │
│   │    │         LIBUV (Event Loop)        │     │                  │
│   │    │  ┌──────────────────────────┐     │     │                  │
│   │    │  │ Non-blocking Operations  │     │     │                  │
│   │    │  │ • File System           │     │     │                  │
│   │    │  │ • Network (HTTP)        │     │     │                  │
│   │    │  │ • Database              │     │     │                  │
│   │    │  │ • Timers                │     │     │                  │
│   │    │  └──────────────────────────┘     │     │                  │
│   │    └───────────────────────────────────┘     │                  │
│   └──────────────────────────────────────────────┘                  │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

#### 1.2 Blocking vs Non-Blocking

```javascript
// BLOQUEANTE (Síncrono)
// El código espera a que termine la operación
const datos = fs.readFileSync('archivo.txt');
console.log(datos);
// ↓ Código siguiente espera

// NO BLOQUEANTE (Asíncrono)
// El código continúa mientras la operación está en progreso
fs.readFile('archivo.txt', (err, datos) => {
    console.log(datos);
});
console.log('Esto se ejecuta ANTES de leer el archivo');
```

---

### 2. Express.js

#### 2.1 ¿Qué es Express?

**Express** es el framework web más popular de Node.js para crear aplicaciones y APIs.

```
┌─────────────────────────────────────────────────────────────────────┐
│                         EXPRESS.JS                                    │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   CARACTERÍSTICAS:                                                   │
│   ─────────────                                                    │
│   • Minimalista y flexible                                          │
│   • Routing poderoso                                               │
│   • Middleware extensible                                          │
│   • Soporte para templates engines                                 │
│   • Facilita REST APIs                                            │
│                                                                      │
│   CONCEPTOS CLAVE:                                                  │
│   ────────────────                                                  │
│   • App (instancia de Express)                                    │
│   • Request (req) - datos del cliente                             │
│   • Response (res) - respuesta del servidor                       │
│   • Middleware - funciones intermedias                            │
│   • Router - manejo de rutas                                     │
│                                                                      │
│   REQUEST → MIDDLEWARE → ROUTE → RESPONSE                          │
│   ═══════   ═════════   ══════   ═════════                        │
│                                                                      │
│   ┌─────────┐   ┌──────────┐   ┌──────────┐   ┌─────────┐        │
│   │ Request │──►│ Logger  │──►│ Auth    │──►│ Route   │──►Resp │
│   └─────────┘   └──────────┘   └──────────┘   └─────────┘        │
│                    ↓                                                 │
│               (next())                                              │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

#### 2.2 Estructura de una Aplicación Express

```javascript
const express = require('express');
const app = express();

// Middleware
app.use(express.json());  // Parsear JSON
app.use(express.urlencoded({ extended: true }));
app.use(cors());

// Rutas
app.get('/', (req, res) => {
    res.send('¡Hola mundo!');
});

app.get('/api/eventos', (req, res) => {
    res.json({ eventos: [] });
});

app.post('/api/eventos', (req, res) => {
    const nuevoEvento = req.body;
    res.status(201).json(nuevoEvento);
});

// Iniciar servidor
app.listen(3000, () => {
    console.log('Servidor en puerto 3000');
});
```

---

### 3. APIs RESTful

#### 3.1 ¿Qué es REST?

**REST (REpresentational State Transfer)** es un estilo arquitectónico para diseñar servicios web.

```
┌─────────────────────────────────────────────────────────────────────┐
│                    REST API - PRINCIPIOS                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   RECURSOS (Sustantivos - plural):                                  │
│   ───────────────────────────                                      │
│   ✓ /eventos                                                        │
│   ✓ /usuarios                                                      │
│   ✗ /getEventos (usar GET /eventos)                               │
│   ✗ /evento/1 (usar /eventos/1)                                    │
│                                                                      │
│   MÉTODOS HTTP:                                                      │
│   ────────────                                                      │
│   GET    → Obtener recursos                                         │
│   POST   → Crear nuevos recursos                                    │
│   PUT    → Reemplazar completamente                                │
│   PATCH  → Actualizar parcialmente                                  │
│   DELETE → Eliminar recursos                                        │
│                                                                      │
│   CÓDIGOS DE ESTADO:                                                 │
│   ─────────────                                                     │
│   200 OK                    - Éxito                                 │
│   201 Created               - Recurso creado                        │
│   204 No Content            - Éxito sin respuesta                   │
│   400 Bad Request           - Datos inválidos                        │
│   401 Unauthorized          - No autenticado                          │
│   403 Forbidden             - No autorizado                          │
│   404 Not Found            - Recurso no existe                      │
│   500 Internal Server Error - Error del servidor                     │
│                                                                      │
│   ENDPOINTS PARA EVENTOS:                                            │
│   ────────────────────                                              │
│   GET    /api/eventos          - Listar todos                       │
│   GET    /api/eventos/:id     - Obtener uno                        │
│   POST   /api/eventos         - Crear nuevo                         │
│   PUT    /api/eventos/:id     - Actualizar (completo)              │
│   PATCH  /api/eventos/:id     - Actualizar (parcial)              │
│   DELETE /api/eventos/:id     - Eliminar                            │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

### 4. Implementación del Proyecto

#### 4.1 Estructura del Proyecto

```
tufiesta-api/
├── src/
│   ├── controllers/    # Lógica de las rutas
│   ├── routes/         # Definición de rutas
│   ├── models/         # Modelos de datos
│   ├── middleware/     # Funciones intermedias
│   ├── config/         # Configuración
│   └── index.js        # Entry point
├── package.json
└── .env
```

#### 4.2 Código del Servidor

```javascript
// src/index.js
require('dotenv').config();
const express = require('express');
const cors = require('cors');
const helmet = require('helmet');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware global
app.use(helmet());           // Seguridad
app.use(cors());             // CORS
app.use(express.json());     // Parsear JSON
app.use(express.urlencoded({ extended: true }));

// Rutas
app.use('/api/eventos', require('./routes/eventos'));
app.use('/api/usuarios', require('./routes/usuarios'));

// Health check
app.get('/health', (req, res) => {
    res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// 404 handler
app.use((req, res) => {
    res.status(404).json({ error: 'Endpoint no encontrado' });
});

// Error handler
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).json({ error: 'Error interno del servidor' });
});

app.listen(PORT, () => {
    console.log(`🚀 Servidor corriendo en http://localhost:${PORT}`);
});
```

```javascript
// src/routes/eventos.js
const express = require('express');
const router = express.Router();

// Base de datos en memoria
let eventos = [
    { id: 1, titulo: 'Concierto de Rock', precio: 1500, fecha: '2024-12-15', categoria: 'musica' },
    { id: 2, titulo: 'Tech Conference', precio: 2500, fecha: '2025-01-10', categoria: 'tecnologia' },
    { id: 3, titulo: 'Stand Up Comedy', precio: 350, fecha: '2024-12-28', categoria: 'comedia' }
];

// GET /api/eventos - Listar todos
router.get('/', (req, res) => {
    const { categoria, buscar } = req.query;
    
    let resultado = [...eventos];
    
    if (categoria && categoria !== 'todas') {
        resultado = resultado.filter(e => e.categoria === categoria);
    }
    
    if (buscar) {
        resultado = resultado.filter(e => 
            e.titulo.toLowerCase().includes(buscar.toLowerCase())
        );
    }
    
    res.json({
        success: true,
        data: resultado,
        total: resultado.length
    });
});

// GET /api/eventos/:id - Obtener uno
router.get('/:id', (req, res) => {
    const evento = eventos.find(e => e.id === parseInt(req.params.id));
    
    if (!evento) {
        return res.status(404).json({
            success: false,
            error: 'Evento no encontrado'
        });
    }
    
    res.json({ success: true, data: evento });
});

// POST /api/eventos - Crear
router.post('/', (req, res) => {
    const { titulo, precio, fecha, categoria } = req.body;
    
    if (!titulo || !precio || !fecha) {
        return res.status(400).json({
            success: false,
            error: 'Faltan datos requeridos'
        });
    }
    
    const nuevoEvento = {
        id: Date.now(),
        titulo,
        precio,
        fecha,
        categoria: categoria || 'otro',
        createdAt: new Date().toISOString()
    };
    
    eventos.push(nuevoEvento);
    
    res.status(201).json({
        success: true,
        data: nuevoEvento
    });
});

// PUT /api/eventos/:id - Actualizar
router.put('/:id', (req, res) => {
    const index = eventos.findIndex(e => e.id === parseInt(req.params.id));
    
    if (index === -1) {
        return res.status(404).json({
            success: false,
            error: 'Evento no encontrado'
        });
    }
    
    eventos[index] = { ...eventos[index], ...req.body };
    
    res.json({
        success: true,
        data: eventos[index]
    });
});

// DELETE /api/eventos/:id - Eliminar
router.delete('/:id', (req, res) => {
    const index = eventos.findIndex(e => e.id === parseInt(req.params.id));
    
    if (index === -1) {
        return res.status(404).json({
            success: false,
            error: 'Evento no encontrado'
        });
    }
    
    eventos.splice(index, 1);
    
    res.json({
        success: true,
        message: 'Evento eliminado'
    });
});

module.exports = router;
```

---

## 📚 Ejercicios

1. Crear servidor Express básico
2. Implementar CRUD de eventos
3. Agregar filtros y paginación
4. Conectar con frontend

---

## 📚 Recursos

- [Express.js](https://expressjs.com/)
- [Node.js](https://nodejs.org/)
- [REST API Tutorial](https://restfulapi.net/)
