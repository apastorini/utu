# CURSO COMPLETO DE CIBERSEGURIDAD - PARTE 6

## MÓDULO 10: SEGURIDAD EN APIs REST

### 10.1 Fundamentos de APIs REST

```
┌────────────────────────────────────────────────────────────┐
│              ARQUITECTURA API REST                         │
└────────────────────────────────────────────────────────────┘

Cliente (App móvil, Web, IoT)
    │
    │ HTTP Request
    │ GET /api/usuarios/123
    │ Authorization: Bearer eyJhbGc...
    ▼
┌─────────────────────────────────────────────────────────┐
│  API GATEWAY                                            │
│  • Rate Limiting                                        │
│  • Autenticación                                        │
│  • Logging                                              │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│  BACKEND API                                            │
│  • Lógica de negocio                                    │
│  • Validación                                           │
│  • Autorización                                         │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│  BASE DE DATOS                                          │
└─────────────────────────────────────────────────────────┘
```

### 10.2 OWASP API Security Top 10

**API1: Broken Object Level Authorization (BOLA)**

```python
# ❌ VULNERABLE
@app.route('/api/pedidos/<int:pedido_id>')
def obtener_pedido(pedido_id):
    pedido = Pedido.query.get(pedido_id)
    return jsonify(pedido.to_dict())

# ✅ SEGURO
@app.route('/api/pedidos/<int:pedido_id>')
@requiere_autenticacion
def obtener_pedido(pedido_id):
    pedido = Pedido.query.filter_by(
        id=pedido_id,
        usuario_id=g.usuario_id
    ).first_or_404()
    return jsonify(pedido.to_dict())
```

### 10.3 OAuth 2.0 Flow

```
Usuario → Cliente → Auth Server → Resource Server
   │         │           │              │
   │ Login   │           │              │
   │────────>│ Redirect  │              │
   │         │──────────>│              │
   │         │           │ Code         │
   │         │<──────────│              │
   │         │ Exchange  │              │
   │         │──────────>│              │
   │         │ Token     │              │
   │         │<──────────│              │
   │         │ Request + Token          │
   │         │─────────────────────────>│
   │         │           │ Data         │
   │         │<─────────────────────────│
```

### 10.4 Rate Limiting con Redis

```python
from flask_limiter import Limiter
from redis import Redis

limiter = Limiter(
    app=app,
    storage_uri="redis://localhost:6379"
)

@app.route('/api/buscar')
@limiter.limit("100 per hour")
def buscar():
    return jsonify(resultados)
```

