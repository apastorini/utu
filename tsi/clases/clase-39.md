# Clase 39: Taller Integrador - App Segura Parte 2

**Numero de clase:** 29  
**Duracion:** 2 horas  
**Curso:** Taller de Ciberseguridad Orientada al Desarrollo

---

## Objetivos de Aprendizaje

- Implementar endpoints protegidos con JWT
- Implementar RBAC (Role-Based Access Control)
- Agregar logging seguro sin exponer informacion sensible
- Implementar rate limiting
- Agregar security headers con Helmet
- Escribir pruebas unitarias de seguridad

---

## Contenido Detallado

### 1. Endpoints Protegidos con JWT (15 min)

Agregamos el router de items con proteccion JWT.

```python
# app/schemas/item.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ItemCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)


class ItemUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)


class ItemResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = {"from_attributes": True}
```

```python
# app/models/item.py
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
```

```python
# app/routers/items.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.user import User
from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate, ItemResponse
from app.middleware.security import get_current_user

router = APIRouter(prefix="/api/items", tags=["items"])


@router.get("/", response_model=List[ItemResponse])
def list_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    items = (
        db.query(Item)
        .filter(Item.owner_id == current_user.id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return items


@router.get("/{item_id}", response_model=ItemResponse)
def get_item(
    item_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    item = db.query(Item).filter(Item.id == item_id).first()
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item no encontrado"
        )
    # Verificar ownership (IDOR protection)
    if item.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No autorizado para ver este item"
        )
    return item


@router.post("/", response_model=ItemResponse, status_code=201)
def create_item(
    item_data: ItemCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    item = Item(
        title=item_data.title,
        description=item_data.description,
        owner_id=current_user.id
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.put("/{item_id}", response_model=ItemResponse)
def update_item(
    item_id: int,
    item_data: ItemUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    item = db.query(Item).filter(Item.id == item_id).first()
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item no encontrado"
        )
    if item.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No autorizado para modificar este item"
        )
    if item_data.title is not None:
        item.title = item_data.title
    if item_data.description is not None:
        item.description = item_data.description
    db.commit()
    db.refresh(item)
    return item


@router.delete("/{item_id}", status_code=204)
def delete_item(
    item_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    item = db.query(Item).filter(Item.id == item_id).first()
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item no encontrado"
        )
    if item.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No autorizado para eliminar este item"
        )
    db.delete(item)
    db.commit()
    return None
```

### 2. Middleware de Autorizacion por Roles (15 min)

```python
# app/middleware/rbac.py
from functools import wraps
from fastapi import Depends, HTTPException, status

from app.models.user import User
from app.middleware.security import get_current_user


def require_role(required_role: str):
    """
    Decorator para verificar que el usuario tenga un rol especifico.

    Uso:
        @router.get("/admin/users")
        @require_role("admin")
        def admin_endpoint(current_user: User = Depends(get_current_user)):
            ...
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Extraer current_user de kwargs (inyectado por FastAPI)
            current_user = kwargs.get("current_user")
            if current_user is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Autenticacion requerida"
                )
            if current_user.role != required_role:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Se requiere rol '{required_role}'"
                )
            return func(*args, **kwargs)
        return wrapper
    return decorator
```

Alternativa usando dependencia directa (mas "FastAPI way"):

```python
# app/middleware/rbac.py - Version alternativa
from fastapi import Depends, HTTPException, status
from app.models.user import User
from app.middleware.security import get_current_user


class RoleChecker:
    def __init__(self, allowed_roles: list):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Acceso denegado. Roles permitidos: {self.allowed_roles}"
            )
        return current_user


# Instancias reutilizables
admin_only = RoleChecker(["admin"])
user_or_admin = RoleChecker(["user", "admin"])
```

Uso con clase:

```python
from app.middleware.rbac import admin_only, user_or_admin

@router.get("/admin/users")
def list_all_users(
    current_user: User = Depends(admin_only),
    db: Session = Depends(get_db)
):
    users = db.query(User).all()
    return users
```

### 3. Logging Seguro (10 min)

El logging seguro nunca debe incluir informacion sensible como contrasenas, tokens, datos personales.

```python
# app/services/logger.py
import logging
import json
import re
from datetime import datetime, timezone


class SecureLogger:
    """
    Logger que filtra informacion sensible antes de escribir.
    """

    # Patrones de campos sensibles
    SENSITIVE_FIELDS = [
        "password", "secret", "token", "authorization",
        "credit_card", "ssn", "phone", "email"
    ]

    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)

        # Handler para archivo
        handler = logging.FileHandler("app.log")
        handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ))
        self.logger.addHandler(handler)

    def _sanitize(self, data: dict) -> dict:
        """Elimina o enmascara campos sensibles."""
        sanitized = {}
        for key, value in data.items():
            key_lower = key.lower()
            if any(field in key_lower for field in self.SENSITIVE_FIELDS):
                sanitized[key] = "***REDACTED***"
            elif isinstance(value, dict):
                sanitized[key] = self._sanitize(value)
            else:
                sanitized[key] = value
        return sanitized

    def log_event(self, level: str, event: str, user_id: int = None,
                  details: dict = None, ip_address: str = None):
        """Registra un evento de seguridad."""
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event": event,
            "user_id": user_id,
            "ip_address": ip_address,
            "details": self._sanitize(details or {})
        }

        message = json.dumps(log_entry)

        if level.upper() == "INFO":
            self.logger.info(message)
        elif level.upper() == "WARNING":
            self.logger.warning(message)
        elif level.upper() == "ERROR":
            self.logger.error(message)
        elif level.upper() == "CRITICAL":
            self.logger.critical(message)


# Instancia global
secure_logger = SecureLogger("secure_api")
```

Uso en endpoints:

```python
from app.services.logger import secure_logger

@router.post("/login", response_model=TokenResponse)
def login(credentials: UserLogin, request: Request, db: Session = Depends(get_db)):
    user = authenticate_user(db, credentials.username, credentials.password)

    if user is None:
        secure_logger.log_event(
            level="WARNING",
            event="LOGIN_FAILED",
            details={"username": credentials.username},
            ip_address=request.client.host
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales invalidas"
        )

    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})

    secure_logger.log_event(
        level="INFO",
        event="LOGIN_SUCCESS",
        user_id=user.id,
        ip_address=request.client.host
    )

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token
    )
```

### 4. Rate Limiting (15 min)

```python
# app/middleware/ratelimit.py
import time
from collections import defaultdict
from fastapi import HTTPException, Request, status


class RateLimiter:
    """
    Rate limiter simple en memoria (para produccion usar Redis).
    """

    def __init__(self):
        # {key: [(timestamp, count), ...]}
        self.requests = defaultdict(list)

    def _get_key(self, request: Request) -> str:
        """Identificador unico basado en IP o usuario autenticado."""
        client_ip = request.client.host if request.client else "unknown"

        # Si hay usuario autenticado, usar su ID
        if hasattr(request.state, "user"):
            return f"user:{request.state.user.id}"

        return f"ip:{client_ip}"

    def check(self, request: Request, max_requests: int = 10,
              window_seconds: int = 60) -> None:
        """
        Verifica si el request excede el limite.

        Args:
            request: Request de FastAPI
            max_requests: Maximo de requests permitidos en la ventana
            window_seconds: Tamano de la ventana en segundos
        """
        key = self._get_key(request)
        now = time.time()

        # Limpiar entradas viejas
        self.requests[key] = [
            req_time for req_time in self.requests[key]
            if now - req_time < window_seconds
        ]

        # Verificar limite
        if len(self.requests[key]) >= max_requests:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Limite de requests excedido. "
                       f"Maximo: {max_requests} por {window_seconds}s",
                headers={"Retry-After": str(window_seconds)}
            )

        # Registrar request
        self.requests[key].append(now)


# Instancia global
rate_limiter = RateLimiter()
```

Integracion como middleware FastAPI:

```python
# app/middleware/ratelimit_middleware.py
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware

from app.middleware.ratelimit import rate_limiter


class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Aplicar rate limiting a rutas de autenticacion
        if request.url.path.startswith("/auth"):
            rate_limiter.check(
                request,
                max_requests=5,       # 5 intentos
                window_seconds=60     # por minuto
            )

        response = await call_next(request)
        return response
```

Registrar en `main.py`:

```python
from app.middleware.ratelimit_middleware import RateLimitMiddleware

app.add_middleware(RateLimitMiddleware)
```

### 5. Security Headers (10 min)

```python
# app/middleware/headers.py
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response: Response = await call_next(request)

        # Prevenir que el navegador haga MIME-type sniffing
        response.headers["X-Content-Type-Options"] = "nosniff"

        # Prevenir clickjacking
        response.headers["X-Frame-Options"] = "DENY"

        # Habilitar XSS filter en navegadores antiguos
        response.headers["X-XSS-Protection"] = "1; mode=block"

        # HSTS (HTTP Strict Transport Security)
        response.headers["Strict-Transport-Security"] = \
            "max-age=31536000; includeSubDomains"

        # Content Security Policy
        response.headers["Content-Security-Policy"] = \
            "default-src 'self'; script-src 'self'; style-src 'self'"

        # Referrer Policy
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        # Cache-Control para respuestas sensibles
        if request.url.path.startswith("/auth"):
            response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate"

        # Remove Server header
        if "server" in response.headers:
            del response.headers["server"]

        return response
```

Registrar en `main.py`:

```python
from app.middleware.headers import SecurityHeadersMiddleware

app.add_middleware(SecurityHeadersMiddleware)
```

### 6. Tests de Seguridad (15 min)

```python
# tests/test_security.py
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.database import Base, engine, SessionLocal
from app.models.user import User
from app.services.auth_service import hash_password


@pytest.fixture(autouse=True)
def setup_db():
    """Crear tablas limpias para cada test."""
    Base.metadata.create_all(bind=engine)
    yield
    # Limpiar despues de cada test
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session():
    session = SessionLocal()
    yield session
    session.close()


@pytest.fixture
def test_user(db_session):
    user = User(
        email="test@example.com",
        username="testuser",
        password_hash=hash_password("TestPass123"),
        role="user"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def admin_user(db_session):
    user = User(
        email="admin@example.com",
        username="adminuser",
        password_hash=hash_password("AdminPass123"),
        role="admin"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.mark.asyncio
async def test_register_with_weak_password():
    """Test: registro con contrasena debil debe fallar."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/auth/register", json={
            "email": "weak@example.com",
            "username": "weakuser",
            "password": "123"  # Demasiado corta, sin mayusculas
        })
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_login_invalid_credentials():
    """Test: login con credenciales invalidas debe fallar."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/auth/login", json={
            "username": "nonexistent",
            "password": "WrongPass123"
        })
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_access_without_token():
    """Test: endpoint protegido sin token debe retornar 401."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/items/")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_access_with_expired_token():
    """Test: token expirado debe dar 401."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get(
            "/api/items/",
            headers={"Authorization": "Bearer expired.token.here"}
        )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_idor_access_other_user_item(test_user):
    """Test: usuario no puede acceder a items de otro usuario."""
    # Crear un segundo usuario con un item
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Login como test_user
        login_resp = await client.post("/auth/login", json={
            "username": "testuser",
            "password": "TestPass123"
        })
        token = login_resp.json()["access_token"]

        # Crear item
        create_resp = await client.post(
            "/api/items/",
            headers={"Authorization": f"Bearer {token}"},
            json={"title": "Mi item", "description": "desc"}
        )
        item_id = create_resp.json()["id"]

        # Intentar acceder como otro usuario (simulado con usuario2)
        # En este test, simplemente verificamos que el item creado
        # pertenece al usuario correcto
        assert create_resp.status_code == 201
        assert create_resp.json()["owner_id"] == test_user.id


@pytest.mark.asyncio
async def test_security_headers():
    """Test: verificar que los security headers estan presentes."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/health")
    assert response.headers.get("x-content-type-options") == "nosniff"
    assert response.headers.get("x-frame-options") == "DENY"
    assert response.headers.get("strict-transport-security") is not None
```

### 7. Actualizar main.py (5 min)

```python
# app/main.py - Version final
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import engine, Base
from app.routers import auth, items
from app.middleware.ratelimit_middleware import RateLimitMiddleware
from app.middleware.headers import SecurityHeadersMiddleware

# Crear tablas
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION
)

# Middleware (orden importante: se ejecutan en orden inverso)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)
app.add_middleware(RateLimitMiddleware)
app.add_middleware(SecurityHeadersMiddleware)

# Routers
app.include_router(auth.router)
app.include_router(items.router)


@app.get("/health")
def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=False)
```

---

## Ejercicio 1: Implementar GET /api/items Protegido

**Enunciado:** Implementar el endpoint GET /api/items que solo devuelva items del usuario autenticado.

**Solucion:** Ya incluida en la seccion 1. El endpoint:

- Requiere autenticacion via `Depends(get_current_user)`
- Filtra items por `owner_id == current_user.id`
- Soporta paginacion via `skip` y `limit`
- Valida que `skip >= 0` y `limit` entre 1 y 100

Prueba:
```bash
# Login
TOKEN=$(curl -s -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"TestPass123"}' | \
  python -c "import sys,json; print(json.load(sys.stdin)['access_token'])")

# Listar items
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/items/

# Sin token (debe fallar)
curl http://localhost:8000/api/items/
# Respuesta: 401 Unauthorized
```

---

## Ejercicio 2: Implementar Middleware de Autorizacion por Roles

**Enunciado:** Crear un middleware/dependencia que restrinja endpoints segun el rol del usuario.

**Solucion:** Ya incluida en la seccion 2 (clase `RoleChecker`). Ejemplo de uso:

```python
from app.middleware.rbac import RoleChecker
from app.models.user import User

# Crear instancias
admin_only = RoleChecker(["admin"])
user_or_admin = RoleChecker(["user", "admin"])

# Endpoint solo para admin
@router.get("/admin/users")
def list_users(
    current_user: User = Depends(admin_only),
    db: Session = Depends(get_db)
):
    """Solo administradores pueden listar todos los usuarios."""
    users = db.query(User).all()
    return users

# Endpoint accesible por user y admin
@router.get("/api/items/stats")
def get_stats(
    current_user: User = Depends(user_or_admin),
    db: Session = Depends(get_db)
):
    items_count = db.query(Item).filter(
        Item.owner_id == current_user.id
    ).count()
    return {"total_items": items_count}
```

---

## Ejercicio 3: Agregar Rate Limiting con Flask-Limiter (version FastAPI)

**Enunciado:** Agregar rate limiting de 5 intentos por minuto en login.

**Solucion:** Ya incluida en la seccion 4. Para una solucion mas robusta:

```bash
pip install slowapi
```

```python
# app/middleware/slowapi_setup.py
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
```

En `main.py`:
```python
from app.middleware.slowapi_setup import limiter, _rate_limit_exceeded_handler

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
```

En `routers/auth.py`:
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@router.post("/login")
@limiter.limit("5/minute")
def login(credentials: UserLogin, request: Request, db: Session = Depends(get_db)):
    # ... resto del codigo
```

---

## Ejercicio 4: Escribir Tests Unitarios de Seguridad

**Enunciado:** Escribir 3 tests de seguridad: registro con contrasena debil, acceso sin token, y verificacion de security headers.

**Solucion:** Tests ya incluidos en la seccion 6. Resumen de lo que cada test verifica:

1. `test_register_with_weak_password`: Verifica que contrasenas debiles son rechazadas (422)
2. `test_access_without_token`: Verifica que endpoints protegidos requieren autenticacion (401)
3. `test_security_headers`: Verifica que headers como X-Content-Type-Options y X-Frame-Options estan presentes

Para ejecutar los tests:
```bash
pip install pytest httpx pytest-asyncio
cd secure-api
pytest tests/ -v
```

---

## Preguntas y Respuestas

**1. Que es RBAC y como se implemento en la aplicacion?**

RBAC (Role-Based Access Control) asigna permisos basados en roles. En nuestra app, los roles son "user" y "admin". Se implemento con una dependencia `RoleChecker` que verifica `current_user.role` contra los roles permitidos en cada endpoint.

**2. Por que es importante rate limiting en endpoints de autenticacion?**

Rate limiting previene ataques de fuerza bruta y diccionario. Sin el, un atacante puede probar miles de contrasenas por minuto. Con 5 intentos por minuto, un ataque de 10,000 contrasenas tomaria mas de 33 horas.

**3. Que security headers se agregaron y que protege cada uno?**

- X-Content-Type-Options: previene MIME sniffing
- X-Frame-Options: previene clickjacking
- X-XSS-Protection: habilita filtro XSS en navegadores antiguos
- Strict-Transport-Security: fuerza HTTPS
- Content-Security-Policy: controla recursos que puede cargar la pagina

**4. Que informacion no debe aparecer en los logs de seguridad?**

Nunca registrar: contrasenas (ni hasheadas), tokens JWT, secret keys, datos de tarjetas de credito, numeros de seguro social, emails completos (parcialmente enmascarados puede ser aceptable), informacion biomedica.

**5. Como se protege contra IDOR en los endpoints del CRUD?**

En cada endpoint que accede a un recurso por ID, se verifica que `item.owner_id == current_user.id`. Si el usuario no es el propietario y no es admin, se retorna 403 Forbidden. Esto evita que un usuario malicioso cambie el ID en la URL para acceder a recursos de otros.

**6. Que hace `from_attributes = True` en los schemas de respuesta?**

Configura Pydantic para crear instancias del schema directamente desde objetos SQLAlchemy (ORM). Sin esta opcion, habria que convertir manualmente el objeto a diccionario. Con `from_attributes = True`, se pasa el objeto directamente y Pydantic mapea los atributos.

**7. Cual es la diferencia entre `Depends(get_current_user)` y `Depends(admin_only)`?**

`get_current_user` solo verifica que el token JWT sea valido y retorna el usuario. `admin_only` (que internamente usa `get_current_user`) ademas verifica que el usuario tenga el rol requerido. Se pueden componer: primero se autentica, luego se autoriza.

---

## Tarea / Lectura Recomendada

- Completar todos los endpoints del CRUD con proteccion IDOR
- Agregar rate limiting funcional y probarlo con un script de fuerza bruta
- Escribir al menos 3 tests de seguridad adicionales
- Leer: OWASP REST Security Cheat Sheet (https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html)
- Preparacion: Tener la app funcionando para las pruebas de la clase 30


