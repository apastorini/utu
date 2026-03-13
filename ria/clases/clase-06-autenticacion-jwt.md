# 📱 Clase 06: Autenticación, JWT y Seguridad

**Duración:** 4 horas  
**Objetivo:** Implementar autenticación con JWT, hash de contraseñas y seguridad  
**Proyecto:** Sistema de autenticación para el sistema de eventos TuFiesta

---

## 📚 Contenido Teórico

### 1. Fundamentos de Autenticación

#### 1.1 Autenticación vs Autorización

```
┌─────────────────────────────────────────────────────────────────────┐
│              AUTENTICACIÓN vs AUTORIZACIÓN                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   AUTENTICACIÓN (WHO ARE YOU?)                                      │
│   ──────────────────────────────────                                │
│   Verifica la identidad del usuario                                 │
│   • Login con email/password                                        │
│   • Login con redes sociales                                        │
│   • Biometría                                                       │
│   • Tokens                                                           │
│                                                                      │
│   EJEMPLO: "Yo soy Juan, mi ID es juan@email.com"                 │
│                                                                      │
│   ─────────────────────────────────────────────────────────────────│
│                                                                      │
│   AUTORIZACIÓN (WHAT CAN YOU DO?)                                   │
│   ──────────────────────────────────                                │
│   Verifica los permisos del usuario                                 │
│   • Roles (admin, usuario, organizador)                           │
│   • Permisos específicos                                            │
│   • Acceso a recursos                                               │
│                                                                      │
│   EJEMPLO: "Juan puede comprar entradas, Admin puede eliminar eventos"
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

#### 1.2 Métodos de Autenticación

| Método | Descripción | Usos |
|--------|-------------|------|
| **Basic Auth** | Email:password codificado | APIs simples |
| **Session** | Cookies de sesión | Apps tradicionales |
| **JWT** | Tokens firmados | SPAs, APIs |
| **OAuth** | Terceros (Google, Facebook) | Login social |
| **API Keys** | Claves de acceso | APIs públicas |

---

### 2. JWT - JSON Web Tokens

#### 2.1 ¿Qué es JWT?

**JWT** es un estándar para crear tokens de acceso que permiten compartir claims (información) de forma segura.

```
┌─────────────────────────────────────────────────────────────────────┐
│                      JWT - ESTRUCTURA                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   ┌──────────────┬──────────────┬──────────────────────┐         │
│   │   HEADER     │   PAYLOAD    │     SIGNATURE        │         │
│   │  (Algoritmo) │   (Datos)    │   (Verificación)    │         │
│   └──────────────┴──────────────┴──────────────────────┘         │
│                                                                      │
│   header.payload.signature                                         │
│   xxxxyyyyzzz.aaaabbbbcccc.dddddeeeeeffff                         │
│                                                                      │
│   EJEMPLO:                                                          │
│   ────────                                                          │
│   HEADER: { "alg": "HS256", "typ": "JWT" }                        │
│   PAYLOAD: { "sub": "123", "name": "Juan", "admin": true }       │
│   SIGNATURE: HMACSHA256(base64UrlEncode(header) + "." +           │
│                    base64UrlEncode(payload), secret)               │
│                                                                      │
│   USOS COMUNES:                                                     │
│   ───────────                                                      │
│   • Access Token ( corto plazo, 15min-1h )                        │
│   • Refresh Token ( largo plazo, días/semanas )                   │
│   • Email verification                                              │
│   • Password reset                                                   │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

### 3. Implementación

```javascript
// models/Usuario.js
const mongoose = require('mongoose');
const bcrypt = require('bcryptjs');

const usuarioSchema = new mongoose.Schema({
    nombre: { type: String, required: true },
    email: { type: String, required: true, unique: true, lowercase: true },
    password: { type: String, required: true, minlength: 6 },
    rol: { type: String, enum: ['usuario', 'organizador', 'admin'], default: 'usuario' }
});

// Hash password antes de guardar
usuarioSchema.pre('save', async function(next) {
    if (!this.isModified('password')) return next();
    this.password = await bcrypt.hash(this.password, 12);
    next();
});

// Comparar passwords
usuarioSchema.methods.compararPassword = async function(passwordIngresado) {
    return await bcrypt.compare(passwordIngresado, this.password);
};

module.exports = mongoose.model('Usuario', usuarioSchema);
```

```javascript
// middleware/auth.js
const jwt = require('jsonwebtoken');

const autenticar = (req, res, next) => {
    const token = req.header('Authorization')?.replace('Bearer ', '');
    
    if (!token) {
        return res.status(401).json({ error: 'Acceso denegado' });
    }
    
    try {
        const decoded = jwt.verify(token, process.env.JWT_SECRET);
        req.usuario = decoded;
        next();
    } catch (error) {
        res.status(401).json({ error: 'Token inválido' });
    }
};

module.exports = autenticar;
```

---

## 📚 Ejercicios

1. Implementar registro y login
2. Generar y validar JWT
3. Proteger rutas
4. Agregar roles

---

## 📚 Recursos

- [JWT.io](https://jwt.io/)
- [bcrypt](https://www.npmjs.com/package/bcryptjs)
