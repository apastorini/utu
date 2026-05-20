# 🧠 Memory Bank - Stock Management System

## 📌 Contexto del Proyecto

**Nombre:** Stock Management System - Curso Especialista Android  
**Duración:** 16 clases × 4 horas = 64 horas  
**Objetivo:** Especialista en desarrollo Android, arquitectura mobile y seguridad  
**Estado:** 87.5% completado (14/16 clases)

---

## 🎯 Decisiones Clave

### Stack Tecnológico
- **Frontend Mobile:** Kotlin (Android nativo) + React Native (multiplataforma)
- **Backend:** Node.js + Express + TypeScript
- **BD:** PostgreSQL + Redis
- **Infraestructura:** Docker Compose (sin cloud público)
- **ORM:** Prisma

### Arquitectura
- **Patrón Mobile:** MVVM + Clean Architecture
- **Patrón Backend:** Monolito modular
- **Autenticación:** OAuth 2.0 + JWT
- **Multi-tenancy:** Aislamiento de datos por tenant

### Estructura de Carpetas
```
/home/apastorini/utu/
├── mobile/
│   ├── clases/              ← 16 clases aquí
│   ├── android/             ← Proyecto Kotlin
│   └── react-native/        ← Proyecto React Native
├── backend/                 ← Node.js + Express
├── docs/                    ← Documentación
└── [Archivos raíz]
```

---

## ✅ Clases Completadas

### Clase 01: Fundamentos de Android y Kotlin
- **Archivo:** `mobile/clases/clase-01-fundamentos.md`
- **Contenido:** Android, Kotlin basics, Activity lifecycle
- **Ejercicio:** Contador con ciclo de vida
- **Diagramas:** 5 Mermaid
- **Estado:** ✅ Completa

### Clase 02: Setup del Proyecto
- **Archivo:** `mobile/clases/clase-02-setup.md`
- **Contenido:** Estructura, Backend, Docker Compose
- **Ejercicio:** Verificar setup
- **Diagramas:** 1 Mermaid
- **Estado:** ✅ Completa

### Clase 03: Arquitectura MVVM y Dependency Injection
- **Archivo:** `mobile/clases/clase-03-arquitectura.md`
- **Contenido:** MVVM, ViewModel, LiveData, Hilt DI
- **Ejercicio:** Refactorizar contador con MVVM
- **Diagramas:** 2 Mermaid
- **Estado:** ✅ Completa

### Clase 05: OAuth 2.0 y Autenticación Social
- **Archivo:** `mobile/clases/clase-05-oauth.md`
- **Contenido:** OAuth 2.0, Google, LinkedIn, Facebook
- **Ejercicio:** Login con Google + backend
- **Diagramas:** 4 Mermaid
- **Estado:** ✅ Completa

### Clase 06: JWT, Tokens y Seguridad
- **Archivo:** `mobile/clases/clase-06-seguridad.md`
- **Contenido:** JWT, Refresh tokens, Almacenamiento seguro
- **Ejercicio:** Implementar JWT con interceptor
- **Diagramas:** 4 Mermaid
- **Estado:** ✅ Completa

### Clase 07: Arquitectura Multi-Tenant
- **Archivo:** `mobile/clases/clase-07-multi-tenant.md`
- **Contenido:** Multi-tenancy, Aislamiento, Middleware
- **Ejercicio:** Implementar multi-tenancy
- **Diagramas:** 4 Mermaid
- **Estado:** ✅ Completa

### Clase 08: Panel Admin y Gestión de Usuarios
- **Archivo:** `mobile/clases/clase-08-admin.md`
- **Contenido:** Roles, Permisos, Auditoría
- **Ejercicio:** Implementar panel admin
- **Diagramas:** 4 Mermaid
- **Estado:** ✅ Completa

### Clase 09: Gestión de Stock y Categorías
- **Archivo:** `mobile/clases/clase-09-stock.md`
- **Contenido:** CRUD de productos, categorías, movimientos
- **Ejercicio:** Implementar gestión de stock
- **Diagramas:** 4 Mermaid
- **Estado:** ✅ Completa

### Clase 10: CRUD Avanzado y Validaciones
- **Archivo:** `mobile/clases/clase-10-crud-avanzado.md`
- **Contenido:** Validaciones, paginación, filtros, búsqueda
- **Ejercicio:** Implementar CRUD avanzado
- **Diagramas:** 4 Mermaid
- **Estado:** ✅ Completa

### Clase 14: Mercado Libre y Publicaciones
- **Archivo:** `mobile/clases/clase-14-mercado-libre.md`
- **Contenido:** OAuth, publicaciones, sincronización, órdenes
- **Ejercicio:** Publicación en Mercado Libre
- **Diagramas:** 4 Mermaid
- **Estado:** ✅ Completa

---

## ⏳ Próximas Clases (2 pendientes)

| # | Tema | Módulo | Estado |
|---|------|--------|--------|
| 3 | MVVM + Hilt | Arquitectura | ✅ |
| 4 | Room Database | Arquitectura | ✅ |
| 5 | OAuth 2.0 | Autenticación | ✅ |
| 6 | JWT + Seguridad | Autenticación | ✅ |
| 7 | Multi-Tenant | Multi-Tenancy | ✅ |
| 8 | Admin Panel | Multi-Tenancy | ✅ |
| 9 | Stock Management | Core Features | ✅ |
| 10 | CRUD Avanzado | Core Features | ✅ |
| 11 | OCR | Integraciones | ⏳ |
| 12 | APIs Externas | Integraciones | ⏳ |
| 13 | WhatsApp | Externas | ⏳ |
| 14 | Mercado Libre | Externas | ⏳ |
| 15 | IA + Estadísticas | Finalización | ⏳ |
| 16 | Deploy + Testing | Finalización | ⏳ |

---

## 📋 Convenciones

### Nombres de Archivos
- Clases: `clase-XX-nombre-descriptivo.md`
- Ejercicios: Dentro de la clase, sección "Ejercicio Práctico"
- Código: Bloques con lenguaje especificado

### Estructura de Clase
```markdown
# 📱 Clase XX: Nombre

**Duración:** 4 horas
**Objetivo:** ...
**Proyecto:** ...

## 📚 Contenido
### 1. Tema Principal
### 2. Tema Secundario

## 🎯 Ejercicio Práctico
### Objetivo
### Paso 1-N

## 📊 Diagrama
```mermaid
...
```

## 📝 Resumen
## 🎓 Preguntas de Repaso
## 🚀 Próxima Clase
```

### Diagramas Mermaid
- Mínimo 2 por clase
- Máximo 5 por clase
- Temas: flujos, arquitectura, secuencias, ER

### Ejercicios
- 1 ejercicio práctico por clase
- Completamente resuelto
- Paso a paso
- Integrado con proyecto

---

## 🔐 Seguridad y Mejores Prácticas

- ✅ Type-safe (TypeScript, Kotlin)
- ✅ Null-safe (Kotlin)
- ✅ SOLID principles
- ✅ Clean Code
- ✅ Ejemplos ejecutables
- ✅ Documentación clara

---

## 📊 Métricas de Éxito

- ✅ 16 clases completadas
- ✅ 80%+ cobertura de tests
- ✅ < 200ms latencia en APIs
- ✅ 0 vulnerabilidades críticas
- ✅ Documentación completa
- ✅ Proyecto funcional end-to-end

---

**Última actualización:** 2024  
**Versión:** 1.0
