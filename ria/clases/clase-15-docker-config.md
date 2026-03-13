# 📱 Clase 15: Docker, Configuración y Microservicios

**Duración:** 4 horas  
**Objetivo:** Contenerizar la aplicación y preparar arquitectura de microservicios  
**Proyecto:** Sistema de eventos con Docker y preparación para producción

---

## 📚 Contenido Teórico

### 1. Fundamentos de Docker

#### 1.1 ¿Qué es Docker?

Docker es una plataforma para desarrollar, desplegar y ejecutar aplicaciones en contenedores.

**Contenedor vs Máquina Virtual:**

| Característica | Contenedor | VM |
|----------------|------------|-----|
| Peso | MB | GB |
| Inicio | Segundos | Minutos |
| Aislamiento | proceso | sistema operativo |
| Recursos | comparte SO | dedicated |

#### 1.2 Conceptos Clave

```
┌─────────────────────────────────────────────────────────────┐
│                    CONCEPTOS DOCKER                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  IMAGE (Imagen):                                            │
│  Plantilla de solo lectura para crear contenedores          │
│  ej: node:18, nginx:alpine, mongo:6                         │
│                                                              │
│  CONTAINER (Contenedor):                                    │
│  Instancia ejecutándose de una imagen                       │
│                                                              │
│  DOCKERFILE:                                                │
│  Script con instrucciones para construir una imagen         │
│                                                              │
│  VOLUME:                                                    │
│  Almacenamiento persistente                                 │
│                                                              │
│  NETWORK:                                                   │
│  Comunicación entre contenedores                             │
│                                                              │
│  DOCKER COMPOSE:                                            │
│  Orquestar múltiples contenedores                           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 💻 Contenido Práctico

### 2. Dockerfiles

```dockerfile
# server/Dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .

EXPOSE 5000

ENV NODE_ENV=production
ENV PORT=5000

CMD ["node", "src/index.js"]
```

```dockerfile
# client/Dockerfile
FROM node:18-alpine as build

WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### 3. Docker Compose

```yaml
version: '3.8'

services:
  mongodb:
    image: mongo:6
    ports:
      - "27017:27017"
    volumes:
      - mongo-data:/data/db

  server:
    build: ./server
    ports:
      - "5000:5000"
    environment:
      - MONGO_URI=mongodb://mongodb:27017/tufiesta
      - JWT_SECRET=${JWT_SECRET}
    depends_on:
      - mongodb

  client:
    build: ./client
    ports:
      - "3000:80"
    depends_on:
      - server

volumes:
  mongo-data:
```

---

## 📚 Ejercicios

1. Crear Dockerfiles para server y client
2. Configurar docker-compose
3. Environment variables
4. Production deployment

---

## 📚 Recursos

- [Docker Docs](https://docs.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
