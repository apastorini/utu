# 📋 Requerimientos - Stock Management System

## 1. Requerimientos Funcionales (RF)

### 1.1 Autenticación y Autorización

**RF-001: Autenticación OAuth Social**
- El sistema debe permitir login con Google, LinkedIn y Facebook
- Cada proveedor OAuth debe mapear datos del usuario (email, nombre, foto)
- Primer login crea automáticamente cuenta de usuario
- Tokens OAuth se almacenan de forma segura

**RF-002: Gestión de Sesiones**
- JWT con access token (15 min) y refresh token (7 días)
- Logout invalida tokens en servidor
- Refresh automático de tokens en cliente

**RF-003: Roles y Permisos**
- Rol ADMIN: acceso total a todos los datos
- Rol USER: acceso solo a sus datos
- Rol VIEWER: solo lectura de datos asignados

### 1.2 Gestión de Usuarios

**RF-004: Perfil de Usuario**
- Cada usuario tiene: email, nombre, foto, teléfono, país
- Puede editar su perfil
- Puede cambiar contraseña
- Puede desactivar cuenta

**RF-005: Panel Admin**
- Admin ve lista de todos los usuarios
- Admin puede ver datos de cualquier usuario
- Admin puede desactivar/activar usuarios
- Admin puede cambiar roles
- Auditoría de acciones admin

### 1.3 Multi-Tenancy

**RF-006: Tenants**
- Cada usuario tiene un tenant (espacio aislado)
- Datos de un tenant no son visibles para otros
- Admin puede ver todos los tenants

**RF-007: Emprendimientos**
- Cada usuario puede crear múltiples emprendimientos
- Cada emprendimiento tiene: nombre, descripción, logo, RUT/CUIT
- Cada emprendimiento tiene su propio stock
- Personalización UI por emprendimiento

### 1.4 Gestión de Stock

**RF-008: Categorías de Stock**
- Usuario crea categorías personalizadas
- Categorías pueden tener subcategorías
- Cada categoría tiene: nombre, descripción, ícono

**RF-009: Productos/Items**
- Crear, leer, actualizar, eliminar items
- Cada item tiene: código, nombre, descripción, precio, cantidad, categoría
- Historial de cambios de cantidad
- Alertas de stock bajo

**RF-010: Movimientos de Stock**
- Registrar entrada de stock
- Registrar salida de stock
- Cada movimiento tiene: fecha, cantidad, tipo, motivo, usuario
- Trazabilidad completa

### 1.5 OCR y Lectura de Boletas

**RF-011: Captura de Boletas**
- Usuario toma foto de boleta/factura
- Sistema extrae datos (fecha, proveedor, items, total)
- Datos se pre-cargan en formulario de entrada
- Usuario confirma o edita antes de guardar

**RF-012: Reconocimiento de Items**
- OCR identifica items conocidos
- Sugiere categorías basado en histórico
- Permite crear nuevos items desde boleta

### 1.6 Gestión de Proveedores

**RF-013: Registro de Proveedores**
- Crear, editar, eliminar proveedores
- Datos: nombre, teléfono, email, dirección, RUT/CUIT
- Historial de compras

**RF-014: Comunicación WhatsApp**
- Enviar mensajes a proveedores vía WhatsApp
- Recibir confirmaciones de pedidos
- Historial de conversaciones

### 1.7 Publicación en Mercado Libre

**RF-015: Integración Mercado Libre**
- Conectar cuenta de Mercado Libre
- Publicar items desde stock
- Sincronizar stock con Mercado Libre
- Ver ventas realizadas

### 1.8 Estadísticas y Reportes

**RF-016: Dashboard**
- Resumen de stock total
- Movimientos últimos 30 días
- Items más vendidos
- Proveedores principales

**RF-017: Reportes**
- Reporte de stock por categoría
- Reporte de movimientos (entrada/salida)
- Reporte de ventas
- Exportar a PDF/Excel

### 1.9 IA e Inteligencia

**RF-018: Asistente IA**
- Chatbot para consultas sobre stock
- Recomendaciones de reorden
- Análisis de tendencias
- Predicción de demanda

**RF-019: Automatización**
- Alertas automáticas de stock bajo
- Sugerencias de compra
- Notificaciones de cambios importantes

---

## 2. Requerimientos No Funcionales (RNF)

### 2.1 Rendimiento

**RNF-001: Velocidad de Respuesta**
- APIs responden en < 200ms (p95)
- Carga de pantallas en < 1s
- Sincronización de datos en < 5s

**RNF-002: Escalabilidad**
- Sistema soporta 10,000+ usuarios concurrentes
- Base de datos optimizada con índices
- Caché Redis para datos frecuentes

### 2.2 Seguridad

**RNF-003: Encriptación**
- HTTPS/TLS en todas las comunicaciones
- Contraseñas hasheadas con bcrypt
- Tokens JWT firmados
- Datos sensibles encriptados en BD

**RNF-004: Autenticación**
- OAuth 2.0 con PKCE
- 2FA opcional
- Rate limiting en login (5 intentos/15 min)

**RNF-005: Autorización**
- Control de acceso basado en roles (RBAC)
- Validación de permisos en cada endpoint
- Auditoría de acciones sensibles

**RNF-006: Protección de Datos**
- GDPR compliant
- Derecho al olvido implementado
- Exportación de datos del usuario

### 2.3 Disponibilidad

**RNF-007: Uptime**
- 99.5% de disponibilidad
- Backups diarios
- Recuperación ante fallos en < 1 hora

**RNF-008: Sincronización Offline**
- App funciona sin conexión
- Sincroniza cuando hay conexión
- Conflictos resueltos automáticamente

### 2.4 Compatibilidad

**RNF-009: Plataformas**
- Android 8.0+ (API 26+)
- iOS 13+ (React Native)
- Navegadores modernos (Chrome, Firefox, Safari)

**RNF-010: Dispositivos**
- Funciona en teléfonos y tablets
- Responsive design
- Optimizado para pantallas pequeñas

### 2.5 Mantenibilidad

**RNF-011: Código**
- Arquitectura limpia (MVVM, Clean Architecture)
- Cobertura de tests > 80%
- Documentación completa

**RNF-012: Deployment**
- Docker para reproducibilidad
- CI/CD automatizado
- Versionado semántico

### 2.6 Usabilidad

**RNF-013: UX**
- Interfaz intuitiva
- Accesibilidad WCAG 2.1 AA
- Soporte para múltiples idiomas

**RNF-014: Documentación**
- API documentada con OpenAPI/Swagger
- Guías de usuario
- Tutoriales en video

---

## 3. Restricciones Técnicas

- **Sin servicios cloud públicos** (AWS, GCP, Azure)
- **Infraestructura local** con Docker/Kubernetes
- **Base de datos:** PostgreSQL
- **Backend:** Node.js + Express
- **Mobile:** React Native + Kotlin
- **Software gratuito** (open source)

---

## 4. Casos de Uso Principales

### Caso 1: Nuevo Usuario
```
1. Usuario accede a app
2. Selecciona "Login con Google"
3. Se autentica en Google
4. Sistema crea cuenta automáticamente
5. Usuario crea su primer emprendimiento
6. Accede al dashboard
```

### Caso 2: Registrar Stock desde Boleta
```
1. Usuario toma foto de boleta
2. OCR extrae datos
3. Sistema sugiere items y categorías
4. Usuario confirma o edita
5. Stock se actualiza automáticamente
6. Se registra movimiento de entrada
```

### Caso 3: Admin Revisa Usuarios
```
1. Admin accede a panel
2. Ve lista de todos los usuarios
3. Selecciona un usuario
4. Ve todos sus datos y emprendimientos
5. Puede cambiar rol o desactivar
6. Se registra auditoría
```

---

## 5. Métricas de Éxito

- ✅ 100% de funcionalidades implementadas
- ✅ 80%+ cobertura de tests
- ✅ < 200ms latencia en APIs
- ✅ 0 vulnerabilidades críticas
- ✅ Documentación completa
- ✅ Proyecto funcional end-to-end

