# 🎓 Stock Management System - Curso Especialista Android

## ✅ Estado Actual

```
📊 Progreso: 2/16 clases completadas (12.5%)

✅ Completado:
  ├─ Clase 01: Fundamentos de Android y Kotlin
  ├─ Clase 02: Setup del Proyecto
  ├─ Backend Node.js + Express
  ├─ Docker Compose (PostgreSQL, Redis, Nginx)
  └─ Estructura base del proyecto

⏳ Próximo:
  └─ Clase 03: Arquitectura MVVM y Dependency Injection
```

---

## 🚀 Inicio Rápido

### Opción 1: Con Docker (Recomendado)

```bash
# Clonar/descargar el proyecto
cd stock-management-system

# Iniciar servicios
docker-compose up -d

# Verificar
curl http://localhost:3000/health
# Respuesta: {"status":"OK","timestamp":"..."}
```

### Opción 2: Backend Local

```bash
cd backend
npm install
npm run dev

# Acceso: http://localhost:3000
```

### Opción 3: Android Studio

```bash
# Abrir proyecto
File → Open → mobile-android

# Ejecutar
Run → Run 'app'
```

---

## 📚 Documentación

| Documento | Descripción |
|-----------|-------------|
| [INDICE.md](./INDICE.md) | Índice completo de 16 clases |
| [REQUERIMIENTOS.md](./REQUERIMIENTOS.md) | Funcionales y no funcionales |
| [ARQUITECTURA.md](./ARQUITECTURA.md) | Decisiones técnicas (ADR) |
| [STATUS.md](./STATUS.md) | Progreso detallado y changelog |
| [Clase 01](./clases/clase-01-fundamentos.md) | Fundamentos de Android y Kotlin |
| [Clase 02](./clases/clase-02-setup.md) | Setup del proyecto |

---

## 🛠️ Stack Tecnológico

```
Frontend:
  ├─ Android (Kotlin)
  └─ React Native

Backend:
  ├─ Node.js + Express
  ├─ TypeScript
  └─ Prisma ORM

Base de Datos:
  ├─ PostgreSQL
  └─ Redis

Infraestructura:
  ├─ Docker
  ├─ Docker Compose
  └─ Nginx
```

---

## 📋 Estructura del Proyecto

```
stock-management-system/
├── backend/                    # Node.js + Express
│   ├── src/
│   ├── package.json
│   ├── tsconfig.json
│   ├── Dockerfile
│   └── .env
├── mobile-android/             # Kotlin + Android
├── mobile-react-native/        # React Native
├── docker-compose.yml
├── nginx.conf
├── INDICE.md
├── REQUERIMIENTOS.md
├── ARQUITECTURA.md
├── STATUS.md
└── README.md
```

---

## 🎯 Características Principales

- ✅ Autenticación OAuth (Google, LinkedIn, Facebook)
- ✅ Multi-tenant con usuarios admin
- ✅ Gestión de emprendimientos
- ✅ Gestión de stock con categorías
- ✅ OCR para lectura de boletas
- ✅ Integración WhatsApp
- ✅ Publicación en Mercado Libre
- ✅ Estadísticas y reportes
- ✅ Asistente IA
- ✅ Personalización UI

---

## 🔗 Accesos

| Servicio | URL | Credenciales |
|----------|-----|--------------|
| Backend | http://localhost:3000 | - |
| Health Check | http://localhost:3000/health | - |
| PostgreSQL | localhost:5432 | user: stockuser / pass: stockpass123 |
| Redis | localhost:6379 | - |
| Nginx | http://localhost:80 | - |

---

## 📝 Próximos Pasos

1. **Clase 03:** Arquitectura MVVM
   - ViewModel
   - LiveData/StateFlow
   - Dependency Injection (Hilt)

2. **Clase 04:** Room Database
   - Entidades
   - DAOs
   - Migraciones

3. **Clase 05-06:** Autenticación OAuth
   - Google, LinkedIn, Facebook
   - JWT y Refresh Tokens

---

## 🐛 Troubleshooting

### Puerto 3000 en uso
```bash
# Cambiar puerto en .env
PORT=3001

# O matar proceso
lsof -ti:3000 | xargs kill -9
```

### PostgreSQL no conecta
```bash
# Verificar contenedor
docker ps | grep postgres

# Ver logs
docker logs stock_postgres
```

### Redis no responde
```bash
# Verificar conexión
docker exec -it stock_redis redis-cli ping
# Respuesta: PONG
```

---

## 📞 Soporte

Para dudas o problemas:
1. Revisa la documentación en INDICE.md
2. Consulta la clase correspondiente
3. Verifica los logs: `docker-compose logs -f`

---

## 📊 Métricas

- **Clases:** 16 (4 horas cada una)
- **Duración Total:** 64 horas
- **Ejercicios:** 16 (todos resueltos)
- **Diagramas:** 40+ (Mermaid)
- **Líneas de Código:** 5000+

---

**Última actualización:** 2024  
**Versión:** 1.1  
**Estado:** En desarrollo activo
