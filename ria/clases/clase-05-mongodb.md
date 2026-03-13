# 📱 Clase 05: MongoDB y Modelos de Datos

**Duración:** 4 horas  
**Objetivo:** Integrar MongoDB para persistencia de datos, crear modelos con Mongoose  
**Proyecto:** Base de datos para el sistema de eventos TuFiesta

---

## 📚 Contenido Teórico

### 1. Fundamentos de MongoDB

#### 1.1 ¿Qué es MongoDB?

**MongoDB** es una base de datos NoSQL orientada a documentos, flexible y escalable.

```
┌─────────────────────────────────────────────────────────────────────┐
│                    MONGODB vs BASES DE DATOS RELACIONALES             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   SQL (MySQL, PostgreSQL)         │  MongoDB                       │
│   ────────────────────────────────  │  ──────────                    │
│   Tablas                           │  Colecciones                   │
│   Filas/Registros                  │  Documentos (JSON/BSON)       │
│   Columnas                         │  Campos                        │
│   JOINs                            │  Embed/References              │
│   SCHEMA FIJO                      │  SCHEMA FLEXIBLE               │
│                                                                      │
│   Ejemplo:                         │  Ejemplo:                      │
│   ┌─────────────────────┐         │  {                             │
│   │ eventos             │         │    "titulo": "Concierto",     │
│   ├───────┬─────────────┤         │    "precio": 500,             │
│   │ id    │ titulo     │         │    "categoria": "musica",      │
│   │ 1     │ Concierto  │         │    "fecha": "2024-12-15"      │
│   │ 2     │ Teatro     │         │  }                             │
│   └───────┴─────────────┘         │                                │
│                                                                      │
│   RELACIONES:                      │  RELACIONES:                  │
│   FOREIGN KEYS                     │  EMBEDDED / REFERENCES        │
│                                                                      │
│   eventouser                    │  evento {                       │
│   ┌─────────┬─────────┐           │    "titulo": "...",           │
│   │ evento_id│ user_id │           │    "organizador": {           │
│   └─────────┴─────────┘           │      "nombre": "Juan",         │
│                                  │      "email": "juan@..."       │
│                                  │    }                            │
│                                  │  }                              │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

#### 1.2 Operaciones CRUD

```javascript
// Insertar documentos
db.eventos.insertOne({ titulo: "Concierto", precio: 500 })
db.eventos.insertMany([
    { titulo: "Teatro", precio: 300 },
    { titulo: "Cine", precio: 200 }
])

// Leer documentos
db.eventos.find()                      // Todos
db.eventos.findOne({ _id: 1 })         // Uno
db.eventos.find({ categoria: "musica" }) // Con filtro

// Actualizar
db.eventos.updateOne(
    { _id: 1 },
    { $set: { precio: 600 } }
)
db.eventos.updateMany(
    { categoria: "musica" },
    { $inc: { precio: 100 } }
)

// Eliminar
db.eventos.deleteOne({ _id: 1 })
db.eventos.deleteMany({ activo: false })
```

---

### 2. Mongoose - ODM

#### 2.1 ¿Qué es Mongoose?

**Mongoose** proporciona una capa de modelado de objetos (ODM) para MongoDB y Node.js.

```
┌─────────────────────────────────────────────────────────────────────┐
│                         MONGOOSE                                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   CARACTERÍSTICAS:                                                   │
│   ─────────────                                                    │
│   • Schema definition (estructura de documentos)                    │
│   • Model creation (constructores para colecciones)                 │
│   • Validation (validación de datos)                               │
│   • Middleware (hooks del ciclo de vida)                          │
│   • Queries (métodos de consulta)                                  │
│   • Population (relaciones entre documentos)                      │
│                                                                      │
│   FLUJO DE TRABAJO:                                                 │
│   ────────────────                                                  │
│   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐          │
│   │   Schema    │───►│   Model     │───►│  Document   │          │
│   │  (Definir)   │    │ (Constructor)│    │ (Instancia) │          │
│   └─────────────┘    └─────────────┘    └─────────────┘          │
│                                                                      │
│   const eventoSchema = new mongoose.Schema({...});                  │
│   const Evento = mongoose.model('Evento', eventoSchema);          │
│   const evento = new Evento({ titulo: 'Concierto' });              │
│   evento.save();                                                   │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

### 3. Modelos del Proyecto

```javascript
// models/Evento.js
const mongoose = require('mongoose');

const eventoSchema = new mongoose.Schema({
    titulo: {
        type: String,
        required: [true, 'El título es requerido'],
        trim: true,
        maxlength: [100, 'Máximo 100 caracteres']
    },
    descripcion: {
        type: String,
        required: true,
        maxlength: 2000
    },
    fecha: {
        type: Date,
        required: true
    },
    ubicacion: {
        type: String,
        required: true
    },
    precio: {
        type: Number,
        required: true,
        min: 0
    },
    capacidad: {
        type: Number,
        required: true,
        min: 1
    },
    vendidos: {
        type: Number,
        default: 0
    },
    categoria: {
        type: String,
        enum: ['musica', 'tecnologia', 'deportes', 'arte', 'otro'],
        default: 'otro'
    },
    imagen: String,
    organizador: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'Usuario',
        required: true
    },
    activo: {
        type: Boolean,
        default: true
    }
}, {
    timestamps: true,
    toJSON: { virtuals: true },
    toObject: { virtuals: true }
});

// Virtual - campo calculado
eventoSchema.virtual('disponibles').get(function() {
    return this.capacidad - this.vendidos;
});

// Índice para búsqueda de texto
eventoSchema.index({ titulo: 'text', descripcion: 'text' });

module.exports = mongoose.model('Evento', eventoSchema);
```

---

## 📚 Ejercicios

1. Conectar MongoDB con Mongoose
2. Crear modelos Evento y Usuario
3. Implementar CRUD completo
4. Agregar validaciones

---

## 📚 Recursos

- [MongoDB](https://www.mongodb.com/)
- [Mongoose](https://mongoosejs.com/)
