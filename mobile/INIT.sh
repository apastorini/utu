#!/bin/bash

# Script de Inicialización - Stock Management System
# Este script configura todo el proyecto desde cero

set -e

echo "🚀 Inicializando Stock Management System..."

# Crear estructura de carpetas
echo "📁 Creando estructura de carpetas..."
mkdir -p stock-management-system/{backend,mobile-android,mobile-react-native}
cd stock-management-system

# Backend
echo "⚙️  Configurando Backend..."
cd backend

# package.json
cat > package.json << 'EOF'
{
  "name": "stock-backend",
  "version": "1.0.0",
  "description": "Backend para Stock Management System",
  "main": "dist/index.js",
  "scripts": {
    "dev": "ts-node src/index.ts",
    "build": "tsc",
    "start": "node dist/index.js",
    "prisma:generate": "prisma generate",
    "prisma:migrate": "prisma migrate dev",
    "prisma:studio": "prisma studio"
  },
  "dependencies": {
    "express": "^4.18.2",
    "cors": "^2.8.5",
    "dotenv": "^16.3.1",
    "bcryptjs": "^2.4.3",
    "jsonwebtoken": "^9.1.0",
    "prisma": "^5.3.1",
    "@prisma/client": "^5.3.1"
  },
  "devDependencies": {
    "typescript": "^5.2.2",
    "@types/express": "^4.17.20",
    "@types/node": "^20.5.9",
    "@types/bcryptjs": "^2.4.2",
    "@types/jsonwebtoken": "^9.0.4",
    "ts-node": "^10.9.1",
    "nodemon": "^3.0.1"
  }
}
EOF

# tsconfig.json
cat > tsconfig.json << 'EOF'
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "commonjs",
    "lib": ["ES2020"],
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
EOF

# .env
cat > .env << 'EOF'
PORT=3000
DATABASE_URL="postgresql://stockuser:stockpass123@postgres:5432/stock_db"
REDIS_URL="redis://redis:6379"
JWT_SECRET="dev-secret-key-change-in-production"
JWT_EXPIRY="15m"
REFRESH_TOKEN_EXPIRY="7d"
NODE_ENV="development"
EOF

# Crear carpeta src
mkdir -p src

# src/index.ts
cat > src/index.ts << 'EOF'
import express, { Express, Request, Response } from 'express';
import cors from 'cors';
import dotenv from 'dotenv';

dotenv.config();

const app: Express = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());

app.get('/health', (req: Request, res: Response) => {
  res.json({ status: 'OK', timestamp: new Date() });
});

app.get('/api/v1', (req: Request, res: Response) => {
  res.json({ message: 'Stock Management API v1' });
});

app.listen(PORT, () => {
  console.log(`✅ Backend corriendo en http://localhost:${PORT}`);
});
EOF

# Dockerfile
cat > Dockerfile << 'EOF'
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 3000
CMD ["npm", "run", "dev"]
EOF

cd ..

# Docker Compose
echo "🐳 Configurando Docker Compose..."
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    container_name: stock_postgres
    environment:
      POSTGRES_USER: stockuser
      POSTGRES_PASSWORD: stockpass123
      POSTGRES_DB: stock_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U stockuser"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    container_name: stock_redis
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: stock_backend
    environment:
      NODE_ENV: development
      PORT: 3000
      DATABASE_URL: "postgresql://stockuser:stockpass123@postgres:5432/stock_db"
      REDIS_URL: "redis://redis:6379"
      JWT_SECRET: "dev-secret-key-change-in-production"
    ports:
      - "3000:3000"
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    volumes:
      - ./backend/src:/app/src
    command: npm run dev

volumes:
  postgres_data:

networks:
  default:
    name: stock_network
EOF

# nginx.conf
cat > nginx.conf << 'EOF'
events {
    worker_connections 1024;
}

http {
    upstream backend {
        server backend:3000;
    }

    server {
        listen 80;
        server_name localhost;

        location / {
            proxy_pass http://backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
EOF

# README
cat > README.md << 'EOF'
# Stock Management System

Sistema de gestión de stock multi-tenant con autenticación OAuth.

## Inicio Rápido

### Con Docker Compose
```bash
docker-compose up -d
```

### Backend Local
```bash
cd backend
npm install
npm run dev
```

## Acceso

- Backend: http://localhost:3000
- Health: http://localhost:3000/health
- PostgreSQL: localhost:5432
- Redis: localhost:6379

## Documentación

- [Índice](./INDICE.md)
- [Requerimientos](./REQUERIMIENTOS.md)
- [Arquitectura](./ARQUITECTURA.md)
- [Status](./STATUS.md)
EOF

echo "✅ Proyecto inicializado exitosamente!"
echo ""
echo "📝 Próximos pasos:"
echo "1. cd stock-management-system"
echo "2. docker-compose up -d"
echo "3. Accede a http://localhost:3000/health"
echo ""
echo "🎓 Documentación disponible en INDICE.md"
