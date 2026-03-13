# 📱 Clase 09: Microservicios Síncronos

**Duración:** 4 horas  
**Objetivo:** Diseñar e implementar arquitectura de microservicios con comunicación síncrona  
**Proyecto:** Sistema de eventos distribuido con múltiples servicios

---

## 📚 Contenido Teórico

### 1. Fundamentos de Arquitectura de Microservicios

#### 1.1 ¿Qué son los Microservicios?

Los **microservicios** son un estilo arquitectónico que estructura una aplicación como un conjunto de servicios pequeños, autónomos y desplegables de forma independiente. Cada servicio:

- **Tiene su propia base de datos** (o esquema)
- **Se desarrolla de forma independiente** por equipos pequeños
- **Se despliega de forma autónoma** sin afectar otros servicios
- **Se comunica a través de APIs bien definidas**
- **Es propietario de su lógica de negocio**

#### 1.2 Diferencia entre Monolito y Microservicios

**Arquitectura Monolítica:**
```
┌─────────────────────────────────────────────────────┐
│                  APLICACIÓN MONOLITO                │
│  ┌─────────────────────────────────────────────┐   │
│  │              INTERFAZ DE USUARIO             │   │
│  └─────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────┐   │
│  │              LÓGICA DE NEGOCIO              │   │
│  │  • Módulo de Usuarios                       │   │
│  │  • Módulo de Eventos                        │   │
│  │  • Módulo de Reservas                       │   │
│  │  • Módulo de Pagos                          │   │
│  └─────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────┐   │
│  │              BASE DE DATOS                  │   │
│  │  • Tablas: usuarios, eventos, reservas...   │   │
│  └─────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘

PROS:                         CONTRAS:
✅ Simple de desarrollar       ❌ Acoplamiento fuerte
✅ Simple de probar             ❌ Difícil de escalar
✅ Despliegue simple            ❌ Un fallo afecta todo
✅ Alta velocidad inicial       ❌ Technology lock-in
```

**Arquitectura de Microservicios:**
```
                    ┌─────────────────┐
                    │   API GATEWAY   │
                    └────────┬────────┘
                             │
         ┌───────────────────┼───────────────────┐
         │                   │                   │
         ▼                   ▼                   ▼
┌────────────────┐  ┌────────────────┐  ┌────────────────┐
│   SERVICIO    │  │   SERVICIO    │  │   SERVICIO    │
│   USUARIOS    │  │   EVENTOS     │  │   RESERVAS    │
│               │  │               │  │               │
│  ┌─────────┐  │  │  ┌─────────┐  │  │  ┌─────────┐  │
│  │  Lógica │  │  │  │  Lógica │  │  │  │  Lógica │  │
│  └─────────┘  │  │  └─────────┘  │  │  └─────────┘  │
│  ┌─────────┐  │  │  ┌─────────┐  │  │  ┌─────────┐  │
│  │    DB   │  │  │  │    DB   │  │  │  │    DB   │  │
│  │ usuarios│  │  │  │ eventos │  │  │  │reservas │  │
│  └─────────┘  │  │  └─────────┘  │  │  └─────────┘  │
└───────┬───────┘  └───────┬───────┘  └───────┬───────┘
        │                   │                   │
        └───────────────────┼───────────────────┘
                            │
                    ┌───────▼────────┐
                    │   SERVICE       │
                    │   REGISTRY      │
                    └────────────────┘
```

**PROS:**                              **CONTRAS:**
✅ Escalabilidad independiente         ❌ Complejidad operacional
✅ Despliegue independiente            ❌ Latencia de red
✅ Tecnología heterogénea              ❌ Consistencia distribuida
✅ Equipos autónomos                   ❌ Debugging difícil
✅ Alta disponibilidad                 ❌ Duplicación de datos

#### 1.3 Cuándo Usar Microservicios

| Situación | Recomendación |
|-----------|---------------|
| Equipo pequeño (< 5 desarrolladores) | Monolito |
| Startup buscando time-to-market | Monolito primero |
| Aplicación simple con 1-2 dominios | Monolito |
| Equipo mediano-grande (10+ devs) | Microservicios |
| Múltiños dominios de negocio | Microservicios |
| Necesidad de escalar independiente | Microservicios |
| Requieren tecnología diferente | Microservicios |

---

### 2. Principios de Diseño

#### 2.1 Principios Fundamentales (The Twelve-Factor App)

1. **Codebase:** Una base de código, múltiples despliegues
2. **Dependencies:** Dependencias explícitas y aisladas
3. **Config:** Configuración en el entorno
4. **Backing Services:** Tratar servicios externos como recursos
5. **Build, Release, Run:** Separar stages de build y ejecución
6. **Processes:** Ejecutar como procesos stateless
7. **Port Binding:** Exportar servicios vía puerto
8. **Concurrency:** Escalar por procesos
9. **Disposability:** Arranque y apagado rápido
10. **Dev/Prod Parity:** Entornos lo más similares posibles
11. **Logs:** Tratar logs como stream de eventos
12. **Admin Processes:** Tareas admin en procesos iguales

#### 2.2 Principios de Microservicios

**Diseño Dirigido por Dominio (DDD):**

```
┌─────────────────────────────────────────────────────────┐
│                    DOMINIO: EVENTOS                     │
│  ┌─────────────────────────────────────────────────┐   │
│  │                 BOUNDED CONTEXT                │   │
│  │                                                  │   │
│  │   Entities:        Value Objects:              │   │
│  │   • Evento          • Fecha                     │   │
│  │   • Reserva         • Precio                    │   │
│  │   • Usuario         • Ubicación                 │   │
│  │                                                  │   │
│  │   Aggregates:       Domain Services:            │   │
│  │   • EventoAggregate • ReservaService            │   │
│  │                                                  │   │
│  │   Repositories:     Domain Events:              │   │
│  │   • EventoRepo      • EventoCreado              │   │
│  │   • ReservaRepo     • ReservaConfirmada         │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

**Cada microservicio = Bounded Context**

- **Usuario Service:** Gestión de usuarios, auth, perfiles
- **Evento Service:** CRUD de eventos, búsqueda, categorías
- **Reserva Service:** Reservas, disponibilidad, confirmaciones
- **Pago Service:** Procesamiento de pagos, reembolsos
- **Notificación Service:** Emails, SMS, push notifications

#### 2.3 Patrones de Comunicación

**Comunicación Síncrona (Request-Response):**
```
CLIENTE → REST/gRPC → SERVICIO → RESPUESTA
```
- Ventaja: Simple, fácil de entender
- Desventaja: Acoplamiento temporal, latencia

**Comunicación Asíncrona (Message Queue):**
```
CLIENTE → MESSAGE BROKER → SERVICIO → RESPUESTA
         (Kafka, RabbitMQ)      ↓
                            PROCESAR
```
- Ventaja: Desacoplamiento, resiliencia
- Desventaja: Complejidad, consistencia eventual

---

### 3. API Gateway

#### 3.1 ¿Qué es un API Gateway?

El **API Gateway** es el punto de entrada único a la arquitectura de microservicios. Es como un "portero" que:
- Recibe todas las peticiones de los clientes
- Las rutea al servicio correcto
- Implementa seguridad (auth, rate limiting)
- Agrega logging y monitoreo
- Maneja errores de forma centralizada

#### 3.2 Funciones del API Gateway

| Función | Descripción |
|---------|-------------|
| **Enrutamiento** | Dirigir requests al servicio apropiado |
| **Autenticación** | Validar tokens JWT, API keys |
| **Autorización** | Verificar permisos de acceso |
| **Rate Limiting** | Limitar requests por cliente |
| **Cacheo** | Cachear respuestas frecuentes |
| **Transformación** | Convertir protocolos (HTTP → gRPC) |
| **Logging** | Registrar todas las requests |
| **Circuit Breaker** | Manejar fallos gracefully |

#### 3.3 Tipos de API Gateway

**Centralizado (Un solo gateway):**
```
Internet → [API Gateway] → MS1, MS2, MS3
```

**BFF (Backend for Frontend):**
```
         → [BFF Mobile]   → MS1, MS2
Internet → [BFF Web]     → MS1, MS3
         → [BFF Desktop]  → MS1, MS2, MS3
```

---

### 4. Service Discovery

#### 4.1 El Problema

En microservicios, las instancias cambian constantemente:
- Escalado automático (más/menos instancias)
- Despliegues (nuevas versiones)
- Fallos (recuperación automática)

¿Cómo saber a qué IP/ruta llamar?

#### 4.2 Service Registry

El **Service Registry** es una base de datos de servicios disponibles.

```javascript
// service-registry/index.js
class ServiceRegistry {
    constructor() {
        this.services = new Map();
    }
    
    // Registrar servicio
    register(serviceName, url, metadata = {}) {
        if (!this.services.has(serviceName)) {
            this.services.set(serviceName, {
                instances: [],
                metadata: {}
            });
        }
        
        this.services.get(serviceName).instances.push({
            url,
            metadata,
            status: 'healthy',
            registeredAt: Date.now()
        });
        
        console.log(`✅ Servicio registrado: ${serviceName} -> ${url}`);
    }
    
    // Desregistrar servicio
    deregister(serviceName, url) {
        const service = this.services.get(serviceName);
        if (service) {
            service.instances = service.instances.filter(i => i.url !== url);
            console.log(`❌ Servicio desregistrado: ${serviceName} -> ${url}`);
        }
    }
    
    // Obtener instancia saludable
    getService(serviceName) {
        const service = this.services.get(serviceName);
        
        if (!service || service.instances.length === 0) {
            throw new Error(`Servicio no disponible: ${serviceName}`);
        }
        
        // Round-robin simple
        const instance = service.instances[Math.floor(Math.random() * service.instances.length)];
        
        if (instance.status !== 'healthy') {
            throw new Error(`Servicio no saludable: ${serviceName}`);
        }
        
        return instance;
    }
    
    // Health check
    markUnhealthy(serviceName, url) {
        const service = this.services.get(serviceName);
        if (service) {
            const instance = service.instances.find(i => i.url === url);
            if (instance) {
                instance.status = 'unhealthy';
            }
        }
    }
}

module.exports = new ServiceRegistry();
```

#### 4.3 Patrón Circuit Breaker

El **Circuit Breaker** previene fallos en cascada.

```
ESTADOS DEL CIRCUIT BREAKER:

CLOSED (Cerrado) - Normal
┌────────────────────────────────┐
│  Request → Servicio → Response │
│  (Todo funciona bien)          │
└────────────────────────────────┘
   │ Fallos > threshold
   ▼
   
OPEN (Abierto) - Fallando
┌────────────────────────────────┐
│  Request → [CORTOCIRCUITO]     │
│  (Fallos inmediatos)          │
└────────────────────────────────┘
   │ Timeout
   ▼
   
HALF-OPEN (Semi-abierto)
┌────────────────────────────────┐
│  Request → [Prueba]            │
│  (Test de recuperación)       │
└────────────────────────────────┘
```

---

### 5. Comunicación entre Servicios

#### 5.1 Tipos de Comunicación

**1. Punto a Punto (Síncrona):**
```
Servicio A → REST/gRPC → Servicio B
```

**2. Mediator (Orquestación):**
```
         ┌──────────────┐
         │   ORQUESTA   │
         └──────┬───────┘
                │
    ┌───────────┼───────────┐
    ▼           ▼           ▼
  MS-1       MS-2        MS-3
```

**3. Choreography (Coreografía):**
```
  MS-1 ──evento──► MS-2 ──evento──► MS-3
    │                         ▲
    └─────────────────────────┘
        (sin orchestrator)
```

#### 5.2 Manejo de Errores

**Retry Pattern (Reintentos):**
```javascript
async function callWithRetry(fn, maxRetries = 3) {
    for (let i = 0; i < maxRetries; i++) {
        try {
            return await fn();
        } catch (error) {
            if (i === maxRetries - 1) throw error;
            await delay(Math.pow(2, i) * 1000); // Exponential backoff
        }
    }
}
```

**Fallback Pattern:**
```javascript
async function getUserData(userId) {
    try {
        // Intentar con servicio principal
        return await usuarioService.getUser(userId);
    } catch (error) {
        // Fallback a cache
        const cached = await cache.get(`user:${userId}`);
        if (cached) return cached;
        
        // Fallback a datos por defecto
        return { id: userId, nombre: 'Usuario', premium: false };
    }
}
```

---

## 💻 Contenido Práctico

### 6. Implementación

#### 6.1 Estructura de Proyecto

```
microservicios/
├── docker-compose.yml
├── nginx/
│   └── nginx.conf
├── api-gateway/
│   ├── Dockerfile
│   ├── package.json
│   └── src/
│       └── index.js
├── usuario-service/
│   ├── Dockerfile
│   ├── package.json
│   └── src/
│       ├── config/
│       ├── controllers/
│       ├── models/
│       ├── routes/
│       ├── services/
│       ├── middleware/
│       └── index.js
├── evento-service/
├── reserva-service/
└── service-registry/
```

#### 6.2 API Gateway

```javascript
// api-gateway/src/index.js
const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');
const cors = require('cors');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');

const app = express();

// Configuración de servicios
const SERVICES = {
    usuarios: process.env.USUARIO_SERVICE_URL || 'http://localhost:3001',
    eventos: process.env.EVENTO_SERVICE_URL || 'http://localhost:3002',
    reservas: process.env.RESERVA_SERVICE_URL || 'http://localhost:3003',
    pagos: process.env.PAGO_SERVICE_URL || 'http://localhost:3004',
    notificaciones: process.env.NOTIFICACION_SERVICE_URL || 'http://localhost:3005'
};

// Middleware de seguridad
app.use(helmet());
app.use(cors({
    origin: process.env.CORS_ORIGIN || '*'
}));

// Rate limiting
const limiter = rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutos
    max: 100 // máximo 100 requests por IP
});
app.use(limiter);

// Logging
app.use((req, res, next) => {
    console.log(`📝 ${req.method} ${req.path} - ${new Date().toISOString()}`);
    next();
});

// Rutas del API Gateway
app.use('/api/usuarios', createProxyMiddleware({
    target: SERVICES.usuarios,
    changeOrigin: true,
    pathRewrite: { '^/api/usuarios': '' },
    onError: (err, req, res) => {
        res.status(503).json({ error: 'Servicio no disponible' });
    },
    onProxyReq: (proxyReq, req) => {
        proxyReq.setHeader('X-Request-Id', req.id);
    }
}));

app.use('/api/eventos', createProxyMiddleware({
    target: SERVICES.eventos,
    changeOrigin: true,
    pathRewrite: { '^/api/eventos': '' }
}));

app.use('/api/reservas', createProxyMiddleware({
    target: SERVICES.reservas,
    changeOrigin: true,
    pathRewrite: { '^/api/reservas': '' }
}));

app.use('/api/pagos', createProxyMiddleware({
    target: SERVICES.pagos,
    changeOrigin: true,
    pathRewrite: { '^/api/pagos': '' }
}));

app.use('/api/notificaciones', createProxyMiddleware({
    target: SERVICES.notificaciones,
    changeOrigin: true,
    pathRewrite: { '^/api/notificaciones': '' }
}));

// Health check
app.get('/health', (req, res) => {
    res.json({
        status: 'ok',
        timestamp: new Date().toISOString(),
        services: Object.keys(SERVICES)
    });
});

app.get('/api/healthy', (req, res) => {
    res.json({ status: 'healthy' });
});

// Manejo de errores
app.use((err, req, res, next) => {
    console.error('❌ Error en Gateway:', err);
    res.status(500).json({
        error: 'Error interno del gateway',
        message: process.env.NODE_ENV === 'development' ? err.message : undefined
    });
});

// 404
app.use((req, res) => {
    res.status(404).json({ error: 'Endpoint no encontrado' });
});

const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
    console.log(`🚀 API Gateway corriendo en puerto ${PORT}`);
    console.log(`📡 Servicios disponibles:`, Object.keys(SERVICES));
});
```

#### 6.3 Servicio de Eventos con Comunicación

```javascript
// evento-service/src/services/eventoService.js
const axios = require('axios');

class EventoService {
    constructor() {
        this.usuarioServiceUrl = process.env.USUARIO_SERVICE_URL || 'http://localhost:3001';
        this.reservaServiceUrl = process.env.RESERVA_SERVICE_URL || 'http://localhost:3003';
        this.notificacionServiceUrl = process.env.NOTIFICACION_SERVICE_URL || 'http://localhost:3005';
    }
    
    // Validar que el organizador existe y tiene permisos
    async validarOrganizador(organizadorId, token) {
        try {
            const response = await axios.get(
                `${this.usuarioServiceUrl}/usuarios/${organizadorId}`,
                {
                    headers: { Authorization: `Bearer ${token}` },
                    timeout: 5000
                }
            );
            
            const usuario = response.data.data;
            
            // Verificar rol de organizador o admin
            if (!['organizador', 'admin'].includes(usuario.rol)) {
                throw new Error('No tienes permisos para crear eventos');
            }
            
            return usuario;
            
        } catch (error) {
            if (error.response?.status === 404) {
                throw new Error('Usuario no encontrado');
            }
            if (error.code === 'ECONNABORTED') {
                throw new Error('Servicio de usuarios no disponible');
            }
            throw error;
        }
    }
    
    // Crear evento con validaciones
    async crearEvento(datos, token) {
        // 1. Validar organizador
        await this.validarOrganizador(datos.organizadorId, token);
        
        // 2. Crear el evento en la base de datos
        const evento = await this.eventoRepository.crear(datos);
        
        // 3. Enviar notificación asíncronamente
        this.enviarNotificacion(
            datos.organizadorId,
            'EVENTO_CREADO',
            `Tu evento "${evento.titulo}" ha sido publicado`
        ).catch(err => console.warn('Notificación fallida:', err.message));
        
        return evento;
    }
    
    // Obtener evento con información de reservas
    async getEventoConReservas(eventoId) {
        const evento = await this.eventoRepository.obtenerPorId(eventoId);
        
        if (!evento) {
            throw new Error('Evento no encontrado');
        }
        
        // Obtener reservas del servicio de reservas
        let reservas = [];
        try {
            const response = await axios.get(
                `${this.reservaServiceUrl}/reservas/evento/${eventoId}`,
                { timeout: 3000 }
            );
            reservas = response.data.data;
        } catch (error) {
            console.warn('No se pudieron obtener las reservas:', error.message);
        }
        
        return {
            ...evento.toObject(),
            reservas,
            totalVendidos: reservas.reduce((sum, r) => sum + r.cantidad, 0)
        };
    }
    
    // Cancelar evento y todas sus reservas
    async cancelarEvento(eventoId, motivo, token) {
        const evento = await this.eventoRepository.obtenerPorId(eventoId);
        
        if (!evento) {
            throw new Error('Evento no encontrado');
        }
        
        // Obtener reservas
        let reservas = [];
        try {
            const response = await axios.get(
                `${this.reservaServiceUrl}/reservas/evento/${eventoId}`,
                { timeout: 3000 }
            );
            reservas = response.data.data;
        } catch (error) {
            console.warn('Error al obtener reservas:', error.message);
        }
        
        // Cancelar cada reserva
        for (const reserva of reservas) {
            try {
                await axios.post(
                    `${this.reservaServiceUrl}/reservas/${reserva.id}/cancelar`,
                    { motivo: `Evento cancelado: ${motivo}` },
                    { timeout: 2000 }
                );
                console.log(`✅ Reserva ${reserva.id} cancelada`);
            } catch (error) {
                console.warn(`Error al cancelar reserva ${reserva.id}:`, error.message);
            }
        }
        
        // Marcar evento como cancelado
        const eventoActualizado = await this.eventoRepository.actualizar(eventoId, {
            activo: false,
            motivoCancelacion: motivo,
            canceladoAt: new Date()
        });
        
        // Notificar al organizador
        this.enviarNotificacion(
            evento.organizadorId,
            'EVENTO_CANCELADO',
            `Tu evento "${evento.titulo}" ha sido cancelado`
        );
        
        return eventoActualizado;
    }
    
    // Enviar notificación (async, no bloquea)
    async enviarNotificacion(usuarioId, tipo, mensaje) {
        try {
            await axios.post(
                `${this.notificacionServiceUrl}/notificaciones`,
                {
                    usuarioId,
                    tipo,
                    titulo: tipo.replace('_', ' '),
                    mensaje,
                    canal: ['email', 'push']
                },
                { timeout: 2000 }
            );
        } catch (error) {
            console.warn('Error enviando notificación:', error.message);
        }
    }
}

module.exports = EventoService;
```

#### 6.4 Circuit Breaker Implementation

```javascript
// utils/circuitBreaker.js
class CircuitBreaker {
    constructor(options = {}) {
        this.timeout = options.timeout || 5000;        // Timeout de la llamada
        this.threshold = options.threshold || 5;       // Fallos para abrir
        this.resetTimeout = options.resetTimeout || 30000; // Tiempo para reintentar
        this.failures = 0;
        this.lastFailureTime = null;
        this.state = 'CLOSED'; // CLOSED, OPEN, HALF_OPEN
    }
    
    async execute(fn) {
        // Verificar si el circuit breaker está abierto
        if (this.state === 'OPEN') {
            if (Date.now() - this.lastFailureTime >= this.resetTimeout) {
                console.log('🔄 Circuit Breaker: HALF_OPEN (probando...)');
                this.state = 'HALF_OPEN';
            } else {
                throw new Error('Circuit breaker OPEN - servicio no disponible');
            }
        }
        
        try {
            // Ejecutar con timeout
            const result = await Promise.race([
                fn(),
                new Promise((_, reject) =>
                    setTimeout(() => reject(new Error('Timeout')), this.timeout)
                )
            ]);
            
            // Éxito - cerrar el circuit breaker
            this.onSuccess();
            return result;
            
        } catch (error) {
            // Fallo - abrir el circuit breaker
            this.onFailure();
            throw error;
        }
    }
    
    onSuccess() {
        this.failures = 0;
        if (this.state !== 'CLOSED') {
            console.log('✅ Circuit Breaker: CERRADO (recuperado)');
        }
        this.state = 'CLOSED';
    }
    
    onFailure() {
        this.failures++;
        this.lastFailureTime = Date.now();
        
        if (this.failures >= this.threshold) {
            console.log('❌ Circuit Breaker: ABIERTO (demasiados fallos)');
            this.state = 'OPEN';
        }
    }
    
    getState() {
        return {
            state: this.state,
            failures: this.failures,
            lastFailure: this.lastFailureTime,
            nextRetry: this.state === 'OPEN' 
                ? new Date(this.lastFailureTime + this.resetTimeout).toISOString()
                : null
        };
    }
}

// Uso
const usuarioBreaker = new CircuitBreaker({
    timeout: 5000,
    threshold: 3,
    resetTimeout: 30000
});

async function getUsuario(usuarioId) {
    return usuarioBreaker.execute(async () => {
        const response = await axios.get(`${USUARIO_SERVICE}/usuarios/${usuarioId}`);
        return response.data;
    });
}

module.exports = CircuitBreaker;
```

---

## 🛠️ Ejercicios Prácticos

### Ejercicio 1: Crear Microservicio de Usuarios

**Pasos:**
1. Crear estructura de proyecto
2. Implementar modelo de usuario
3. Crear CRUD completo
4. Agregar autenticación JWT
5. Escribir tests

### Ejercicio 2: Conectar Servicios

**Pasos:**
1. Crear evento-service
2. Consumir usuario-service
3. Implementar Circuit Breaker
4. Manejar errores de forma apropiada
5. Agregar logging

### Ejercicio 3: API Gateway

**Pasos:**
1. Implementar API Gateway con Express
2. Configurar proxy a cada servicio
3. Agregar rate limiting
4. Implementar health checks
5. Agregar logging centralizado

---

## 🚀 Proyecto de la Clase

### Arquitectura Completa de Microservicios

```
tufiesta-microservices/
├── docker-compose.yml
├── Makefile
├── README.md
│
├── api-gateway/
│   ├── Dockerfile
│   ├── package.json
│   └── src/
│       └── index.js          # Gateway principal
│
├── services/
│   ├── usuario-service/
│   │   ├── Dockerfile
│   │   ├── package.json
│   │   └── src/
│   │       ├── config/       # Configuración
│   │       ├── controllers/  # Controladores
│   │       ├── models/       # Modelos Mongoose
│   │       ├── routes/       # Rutas
│   │       ├── services/     # Lógica de negocio
│   │       ├── middleware/   # Auth, validation
│   │       └── index.js      # Entry point
│   │
│   ├── evento-service/
│   │   ├── Dockerfile
│   │   ├── package.json
│   │   └── src/
│   │       ├── config/
│   │       ├── controllers/
│   │       ├── models/
│   │       ├── routes/
│   │       ├── services/
│   │       ├── middleware/
│   │       └── index.js
│   │
│   ├── reserva-service/
│   │   ├── Dockerfile
│   │   ├── package.json
│   │   └── src/
│   │       ├── config/
│   │       ├── controllers/
│   │       ├── models/
│   │       ├── routes/
│   │       ├── services/
│   │       ├── middleware/
│   │       └── index.js
│   │
│   ├── pago-service/
│   │   ├── Dockerfile
│   │   ├── package.json
│   │   └── src/
│   │       └── index.js
│   │
│   └── notificacion-service/
│       ├── Dockerfile
│       ├── package.json
│       └── src/
│           └── index.js
│
└── scripts/
    ├── deploy.sh
    └── test.sh
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  # API Gateway - Punto de entrada
  api-gateway:
    build: ./api-gateway
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - USUARIO_SERVICE_URL=http://usuario-service:3001
      - EVENTO_SERVICE_URL=http://evento-service:3002
      - RESERVA_SERVICE_URL=http://reserva-service:3003
      - PAGO_SERVICE_URL=http://pago-service:3004
      - NOTIFICACION_SERVICE_URL=http://notificacion-service:3005
    depends_on:
      - usuario-service
      - evento-service
      - reserva-service
    networks:
      - tufiesta-network
    restart: unless-stopped

  # MongoDB
  mongodb:
    image: mongo:6
    ports:
      - "27017:27017"
    volumes:
      - mongo-data:/data/db
    networks:
      - tufiesta-network

  # Redis
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    networks:
      - tufiesta-network

  # Microservicio de Usuarios
  usuario-service:
    build: ./services/usuario-service
    ports:
      - "3001:3001"
    environment:
      - PORT=3001
      - MONGO_URI=mongodb://mongodb:27017/usuarios
      - JWT_SECRET=${JWT_SECRET}
      - JWT_EXPIRES_IN=7d
    depends_on:
      - mongodb
    networks:
      - tufiesta-network
    restart: unless-stopped

  # Microservicio de Eventos
  evento-service:
    build: ./services/evento-service
    ports:
      - "3002:3002"
    environment:
      - PORT=3002
      - MONGO_URI=mongodb://mongodb:27017/eventos
      - USUARIO_SERVICE_URL=http://usuario-service:3001
      - RESERVA_SERVICE_URL=http://reserva-service:3003
      - NOTIFICACION_SERVICE_URL=http://notificacion-service:3005
    depends_on:
      - mongodb
      - usuario-service
    networks:
      - tufiesta-network
    restart: unless-stopped

  # Microservicio de Reservas
  reserva-service:
    build: ./services/reserva-service
    ports:
      - "3003:3003"
    environment:
      - PORT=3003
      - MONGO_URI=mongodb://mongodb:27017/reservas
      - EVENTO_SERVICE_URL=http://evento-service:3002
      - USUARIO_SERVICE_URL=http://usuario-service:3001
      - PAGO_SERVICE_URL=http://pago-service:3004
    depends_on:
      - mongodb
      - evento-service
      - usuario-service
    networks:
      - tufiesta-network
    restart: unless-stopped

  # Microservicio de Pagos
  pago-service:
    build: ./services/pago-service
    ports:
      - "3004:3004"
    environment:
      - PORT=3004
      - STRIPE_SECRET_KEY=${STRIPE_SECRET_KEY}
    networks:
      - tufiesta-network
    restart: unless-stopped

  # Microservicio de Notificaciones
  notificacion-service:
    build: ./services/notificacion-service
    ports:
      - "3005:3005"
    environment:
      - PORT=3005
      - SMTP_HOST=${SMTP_HOST}
      - SMTP_PORT=${SMTP_PORT}
      - SMTP_USER=${SMTP_USER}
      - SMTP_PASS=${SMTP_PASS}
    networks:
      - tufiesta-network
    restart: unless-stopped

volumes:
  mongo-data:

networks:
  tufiesta-network:
    driver: bridge
```

### Entregables

1. **API Gateway** funcionando con enrutamiento
2. **3+ microservicios** implementados (usuarios, eventos, reservas)
3. **Comunicación síncrona** entre servicios
4. **Circuit Breaker** implementado
5. **Docker Compose** configurado
6. **Documentación** de la arquitectura

---

## 📚 Recursos Adicionales

- [Microservices.io - Patrones](https://microservices.io/)
- [Building Microservices - Sam Newman](https://www.oreilly.com/library/view/building-microservices-2nd/9781492034018/)
- [The Twelve-Factor App](https://12factor.net/)
- [gRPC Documentation](https://grpc.io/docs/)
