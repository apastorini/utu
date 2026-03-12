# 🚀 Clase 02: Setup del Proyecto y Estructura Base

**Duración:** 4 horas  
**Objetivo:** Crear estructura completa del proyecto (Android, React Native, Backend)  
**Proyecto:** Proyecto base funcionando con Docker

---

## 📚 Contenido

### 1. Estructura General del Proyecto

```
stock-management-system/
├── backend/                    # Node.js + Express
│   ├── src/
│   │   ├── auth/
│   │   ├── users/
│   │   ├── tenants/
│   │   ├── stock/
│   │   ├── shared/
│   │   └── index.ts
│   ├── package.json
│   ├── tsconfig.json
│   ├── Dockerfile
│   └── .env.example
│
├── mobile-android/             # Kotlin + Android
│   ├── app/
│   │   ├── src/
│   │   │   ├── main/
│   │   │   ├── test/
│   │   │   └── androidTest/
│   │   └── build.gradle.kts
│   ├── build.gradle.kts
│   └── settings.gradle.kts
│
├── mobile-react-native/        # React Native
│   ├── src/
│   ├── package.json
│   └── app.json
│
├── docker-compose.yml
├── INDICE.md
├── REQUERIMIENTOS.md
├── ARQUITECTURA.md
└── STATUS.md
```

---

### 2. Setup del Backend (Node.js + Express)

#### Paso 1: Inicializar Proyecto

```bash
mkdir -p stock-management-system/backend
cd stock-management-system/backend
npm init -y
```

#### Paso 2: Instalar Dependencias

```bash
npm install express cors dotenv bcryptjs jsonwebtoken prisma @prisma/client
npm install -D typescript @types/express @types/node ts-node nodemon
```

#### Paso 3: Configurar TypeScript (tsconfig.json)

```json
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
    "resolveJsonModule": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

#### Paso 4: Package.json

```json
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
```

#### Paso 5: Archivo Principal (src/index.ts)

```typescript
import express, { Express, Request, Response } from 'express';
import cors from 'cors';
import dotenv from 'dotenv';

dotenv.config();

const app: Express = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());

// Health check
app.get('/health', (req: Request, res: Response) => {
  res.json({ status: 'OK', timestamp: new Date() });
});

// Rutas base
app.get('/api/v1', (req: Request, res: Response) => {
  res.json({ message: 'Stock Management API v1' });
});

// Error handling
app.use((err: any, req: Request, res: Response) => {
  console.error(err);
  res.status(500).json({ error: 'Internal Server Error' });
});

app.listen(PORT, () => {
  console.log(`✅ Backend corriendo en http://localhost:${PORT}`);
});
```

#### Paso 6: Variables de Entorno (.env)

```env
PORT=3000
DATABASE_URL="postgresql://user:password@postgres:5432/stock_db"
JWT_SECRET="tu-secreto-super-seguro-cambiar-en-produccion"
JWT_EXPIRY="15m"
REFRESH_TOKEN_EXPIRY="7d"
NODE_ENV="development"
```

---

### 3. Setup de Android (Kotlin)

#### Paso 1: Crear Proyecto en Android Studio

```
File → New → New Project
- Template: Empty Activity
- Name: StockApp
- Package: com.example.stockapp
- Language: Kotlin
- Min SDK: API 26 (Android 8.0)
```

#### Paso 2: Configurar build.gradle.kts (Project)

```kotlin
plugins {
    id("com.android.application") version "8.1.0" apply false
    id("com.android.library") version "8.1.0" apply false
    id("org.jetbrains.kotlin.android") version "1.9.0" apply false
}
```

#### Paso 3: Configurar build.gradle.kts (App)

```kotlin
plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}

android {
    namespace = "com.example.stockapp"
    compileSdk = 34

    defaultConfig {
        applicationId = "com.example.stockapp"
        minSdk = 26
        targetSdk = 34
        versionCode = 1
        versionName = "1.0.0"
    }

    buildTypes {
        release {
            isMinifyEnabled = false
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    kotlinOptions {
        jvmTarget = "17"
    }

    buildFeatures {
        viewBinding = true
    }
}

dependencies {
    // AndroidX
    implementation("androidx.appcompat:appcompat:1.6.1")
    implementation("androidx.constraintlayout:constraintlayout:2.1.4")
    implementation("androidx.lifecycle:lifecycle-runtime-ktx:2.6.1")
    
    // Material Design
    implementation("com.google.android.material:material:1.9.0")
    
    // Networking
    implementation("com.squareup.okhttp3:okhttp:4.11.0")
    implementation("com.squareup.retrofit2:retrofit:2.9.0")
    implementation("com.squareup.retrofit2:converter-gson:2.9.0")
    
    // JSON
    implementation("com.google.code.gson:gson:2.10.1")
    
    // Testing
    testImplementation("junit:junit:4.13.2")
    androidTestImplementation("androidx.test.espresso:espresso-core:3.5.1")
}
```

#### Paso 4: AndroidManifest.xml

```xml
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.example.stockapp">

    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.CAMERA" />

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:theme="@style/Theme.StockApp">

        <activity
            android:name=".MainActivity"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>

    </application>

</manifest>
```

#### Paso 5: MainActivity.kt

```kotlin
package com.example.stockapp

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import com.example.stockapp.databinding.ActivityMainBinding

class MainActivity : AppCompatActivity() {
    
    private lateinit var binding: ActivityMainBinding
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)
        
        binding.textView.text = "Stock Management System"
    }
}
```

#### Paso 6: activity_main.xml

```xml
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:gravity="center"
    android:padding="16dp">

    <TextView
        android:id="@+id/textView"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Stock Management System"
        android:textSize="24sp"
        android:textStyle="bold" />

</LinearLayout>
```

---

### 4. Docker Compose

Crear `docker-compose.yml` en la raíz del proyecto:

```yaml
version: '3.8'

services:
  # PostgreSQL Database
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

  # Redis Cache
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

  # Backend API
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

  # Nginx Reverse Proxy
  nginx:
    image: nginx:alpine
    container_name: stock_nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - backend

volumes:
  postgres_data:

networks:
  default:
    name: stock_network
```

#### Dockerfile para Backend

```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 3000

CMD ["npm", "run", "dev"]
```

#### nginx.conf

```nginx
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
```

---

### 5. Ejecutar el Proyecto

#### Opción 1: Con Docker Compose

```bash
# Iniciar todos los servicios
docker-compose up -d

# Ver logs
docker-compose logs -f backend

# Detener
docker-compose down

# Acceso
# Backend: http://localhost:3000
# Nginx: http://localhost:80
```

#### Opción 2: Backend Local

```bash
cd backend
npm install
npm run dev

# Acceso: http://localhost:3000
```

#### Opción 3: Android Studio

```bash
# Abrir proyecto
File → Open → mobile-android

# Ejecutar
Run → Run 'app'
```

---

## 📊 Diagrama: Arquitectura del Proyecto

```mermaid
graph TB
    subgraph "Cliente"
        ANDROID["Android<br/>Kotlin"]
        RN["React Native<br/>iOS/Android"]
    end
    
    subgraph "Infraestructura"
        NGINX["Nginx<br/>Reverse Proxy"]
    end
    
    subgraph "Backend"
        EXPRESS["Express.js<br/>Node.js"]
    end
    
    subgraph "Datos"
        PG["PostgreSQL<br/>Base de Datos"]
        REDIS["Redis<br/>Cache"]
    end
    
    ANDROID --> NGINX
    RN --> NGINX
    NGINX --> EXPRESS
    EXPRESS --> PG
    EXPRESS --> REDIS
```

---

## 🔧 Estructura de Carpetas del Backend

```
backend/
├── src/
│   ├── auth/
│   │   ├── auth.controller.ts
│   │   ├── auth.service.ts
│   │   └── auth.routes.ts
│   ├── users/
│   │   ├── users.controller.ts
│   │   ├── users.service.ts
│   │   └── users.routes.ts
│   ├── tenants/
│   │   ├── tenants.controller.ts
│   │   ├── tenants.service.ts
│   │   └── tenants.routes.ts
│   ├── stock/
│   │   ├── stock.controller.ts
│   │   ├── stock.service.ts
│   │   └── stock.routes.ts
│   ├── shared/
│   │   ├── middleware/
│   │   │   ├── auth.middleware.ts
│   │   │   └── error.middleware.ts
│   │   ├── utils/
│   │   │   ├── jwt.util.ts
│   │   │   └── hash.util.ts
│   │   └── types/
│   │       └── index.ts
│   └── index.ts
├── prisma/
│   └── schema.prisma
├── package.json
├── tsconfig.json
├── Dockerfile
└── .env
```

---

## 🎯 Ejercicio: Verificar Setup

### Paso 1: Verificar Backend

```bash
curl http://localhost:3000/health
# Respuesta esperada: {"status":"OK","timestamp":"2024-01-01T..."}
```

### Paso 2: Verificar Base de Datos

```bash
docker exec -it stock_postgres psql -U stockuser -d stock_db -c "\dt"
```

### Paso 3: Verificar Redis

```bash
docker exec -it stock_redis redis-cli ping
# Respuesta: PONG
```

### Paso 4: Verificar Android

```bash
# En Android Studio
# Build → Make Project
# Run → Run 'app'
```

---

## 📝 Checklist de Setup

- ✅ Estructura de carpetas creada
- ✅ Backend Node.js configurado
- ✅ Android Studio proyecto creado
- ✅ Docker Compose configurado
- ✅ PostgreSQL corriendo
- ✅ Redis corriendo
- ✅ Backend accesible en localhost:3000
- ✅ Nginx funcionando
- ✅ Android emulador funcionando

---

## 🚀 Próxima Clase

Clase 03: Arquitectura MVVM - Implementaremos ViewModel, LiveData y Dependency Injection en Android.

---

**Última actualización:** 2024  
**Tiempo estimado:** 4 horas
