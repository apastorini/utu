# 📱 Clase 13: Proyecto - Setup, Frontend y Backend

**Duración:** 4 horas  
**Objetivo:** Configurar el proyecto completo del sistema de eventos  
**Proyecto:** Sistema de eventos tipo tufiesta.uy

---

## 📚 Contenido Teórico

### 1. Arquitectura Full-Stack

#### 1.1 Conceptos de Arquitectura

```
┌─────────────────────────────────────────────────────────────────┐
│                    ARQUITECTURA FULL-STACK                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   FRONTEND (Client)              BACKEND (Server)                │
│   ┌─────────────────┐           ┌─────────────────┐             │
│   │ React/Vue/     │   HTTP    │ Node/Python/    │             │
│   │ Angular        │ ─────────►│ Java/Go         │             │
│   └─────────────────┘  JSON    └────────┬────────┘             │
│                                         │                       │
│                                         ▼                       │
│                                   ┌─────────────┐               │
│                                   │   API REST  │               │
│                                   │   o GraphQL │               │
│                                   └──────┬──────┘               │
│                                          │                       │
│                         ┌────────────────┼────────────────┐     │
│                         ▼                ▼                ▼     │
│                   ┌──────────┐    ┌──────────┐    ┌──────────┐ │
│                   │  MongoDB │    │   Redis  │    │  MySQL   │ │
│                   │ (Document)│    │  (Cache) │    │(Relacion)│ │
│                   └──────────┘    └──────────┘    └──────────┘ │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

#### 1.2 API RESTful

| Método | Descripción | Ejemplo |
|--------|-------------|---------|
| **GET** | Obtener recursos | GET /eventos |
| **POST** | Crear recursos | POST /eventos |
| **PUT** | Actualizar completo | PUT /eventos/1 |
| **PATCH** | Actualizar parcial | PATCH /eventos/1 |
| **DELETE** | Eliminar recurso | DELETE /eventos/1 |

#### 1.3 Códigos de Estado HTTP

| Código | Significado |
|--------|-------------|
| 200 | OK - Éxito |
| 201 | Created - Recurso creado |
| 400 | Bad Request - Datos inválidos |
| 401 | Unauthorized - No autenticado |
| 403 | Forbidden - No autorizado |
| 404 | Not Found - No existe |
| 500 | Internal Server Error |


---

## 💻 Contenido Práctico

### 2. Configuración del Backend

```bash
mkdir server && cd server
npm init -y
npm install express mongoose dotenv cors helmet winston joi jsonwebtoken bcryptjs express-validator
npm install -D nodemon
```

```javascript
// server/src/models/Evento.js
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
        min: 0,
        default: 0
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

eventoSchema.virtual('disponibles').get(function() {
    return this.capacidad - this.vendidos;
});

eventoSchema.index({ titulo: 'text', descripcion: 'text' });

module.exports = mongoose.model('Evento', eventoSchema);
```

### 3. Configuración del Frontend

```bash
npm create vite@latest client -- --template react
cd client
npm install react-router-dom axios
```

```javascript
// client/src/api/client.js
import axios from 'axios';

const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL || '/api',
    timeout: 10000
});

api.interceptors.request.use(config => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

api.interceptors.response.use(
    response => response,
    error => {
        if (error.response?.status === 401) {
            localStorage.removeItem('token');
            window.location.href = '/login';
        }
        return Promise.reject(error);
    }
);

export const eventoApi = {
    listar: (params) => api.get('/eventos', { params }),
    obtener: (id) => api.get(`/eventos/${id}`),
    crear: (data) => api.post('/eventos', data),
    actualizar: (id, data) => api.put(`/eventos/${id}`, data),
    eliminar: (id) => api.delete(`/eventos/${id}`)
};

export default api;
```

---

## 📚 Ejercicios

1. Crear estructura de directorios
2. Configurar Express con MongoDB
3. Crear modelos de datos
4. Implementar API REST
5. Configurar React con Vite

---

## 📚 Recursos

- [Express.js](https://expressjs.com/)
- [Mongoose](https://mongoosejs.com/)
- [Vite](https://vitejs.dev/)
