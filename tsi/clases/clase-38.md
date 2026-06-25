# Clase 38: Taller Integrador - App Segura Parte 1

**Numero de clase:** 28  
**Duracion:** 2 horas  
**Curso:** Taller de Ciberseguridad Orientada al Desarrollo

---

## Objetivos de Aprendizaje

- Desarrollar una API REST segura desde cero con FastAPI
- Implementar autenticacion con JWT y refresh tokens
- Almacenar contrasenas de forma segura con bcrypt
- Aplicar input validation y parametrized queries
- Estructurar un proyecto con separacion de responsabilidades

---

## Contenido Detallado

### 1. Estructura del Proyecto (10 min)

Creamos la siguiente estructura de carpetas para la aplicacion segura:

```
secure-api/
├── app/
│   ├── __init__.py
│   ├── main.py              # Punto de entrada de la aplicacion
│   ├── config.py            # Configuracion (variables de entorno)
│   ├── database.py          # Conexion a base de datos
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py          # Modelo de usuario
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── user.py          # Pydantic schemas (validacion)
│   ├── routers/
│   │   ├── __init__.py
│   │   └── auth.py          # Endpoints de autenticacion
│   ├── services/
│   │   ├── __init__.py
│   │   └── auth_service.py  # Logica de autenticacion
│   └── middleware/
│       ├── __init__.py
│       └── security.py      # Middleware de seguridad
├── requirements.txt
└── .env                     # Variables de entorno (nunca subir a git)
```

### 2. Configuracion y Dependencias (10 min)

```txt
# requirements.txt
fastapi==0.109.0
uvicorn[standard]==0.27.0
sqlalchemy==2.0.25
pydantic[email-validator]==2.5.3
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
python-dotenv==1.0.0
alembic==1.13.1
```

```python
# app/config.py
import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    PROJECT_NAME: str = "Secure API"
    VERSION: str = "1.0.0"

    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./secure_api.db"
    )

    # JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Bcrypt
    BCRYPT_ROUNDS: int = 12

    # CORS
    ALLOWED_ORIGINS: list = ["http://localhost:3000"]

    def __init__(self):
        if not self.SECRET_KEY:
            raise ValueError(
                "SECRET_KEY no configurada. "
                "Establezca la variable de entorno SECRET_KEY."
            )


settings = Settings()
```

### 3. Base de Datos y Modelo de Usuario (15 min)

```python
# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False}  # Solo para SQLite
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

```python
# app/models/user.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), default="user")  # "user" o "admin"
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
```

### 4. Schemas de Validacion con Pydantic (10 min)

```python
# app/schemas/user.py
from pydantic import BaseModel, EmailStr, Field, field_validator
import re


class UserRegister(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8, max_length=128)

    @field_validator("username")
    @classmethod
    def validate_username(cls, v):
        if not re.match(r"^[a-zA-Z0-9_]+$", v):
            raise ValueError(
                "Username solo permite letras, numeros y guion bajo"
            )
        return v

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if not re.search(r"[A-Z]", v):
            raise ValueError("La contrasena debe tener al menos una mayuscula")
        if not re.search(r"[a-z]", v):
            raise ValueError("La contrasena debe tener al menos una minuscula")
        if not re.search(r"\d", v):
            raise ValueError("La contrasena debe tener al menos un numero")
        return v


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    role: str
    is_active: bool

    model_config = {"from_attributes": True}


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
```

### 5. Servicio de Autenticacion (15 min)

```python
# app/services/auth_service.py
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.config import settings
from app.models.user import User
from app.schemas.user import UserRegister

# Contexto de hashing con bcrypt
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=settings.BCRYPT_ROUNDS
)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError:
        return None


def register_user(db: Session, user_data: UserRegister) -> User:
    # Verificar si el usuario o email ya existe
    existing = db.query(User).filter(
        (User.username == user_data.username) |
        (User.email == user_data.email)
    ).first()

    if existing:
        if existing.username == user_data.username:
            raise ValueError("El nombre de usuario ya esta registrado")
        raise ValueError("El email ya esta registrado")

    # Crear nuevo usuario
    user = User(
        email=user_data.email,
        username=user_data.username,
        password_hash=hash_password(user_data.password),
        role="user"
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, username: str, password: str) -> User:
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    if not user.is_active:
        return None
    return user
```

### 6. Middleware de Seguridad (10 min)

```python
# app/middleware/security.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.services.auth_service import decode_token

security_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
    db: Session = Depends(get_db)
) -> User:
    token = credentials.credentials
    payload = decode_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tipo de token incorrecto",
        )

    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalido: sin identificador de usuario",
        )

    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo",
        )

    return user
```

### 7. Router de Autenticacion (15 min)

```python
# app/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user import (
    UserRegister,
    UserLogin,
    UserResponse,
    TokenResponse
)
from app.services.auth_service import (
    register_user,
    authenticate_user,
    create_access_token,
    create_refresh_token,
    decode_token
)
from app.middleware.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse, status_code=201)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    try:
        user = register_user(db, user_data)
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )


@router.post("/login", response_model=TokenResponse)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, credentials.username, credentials.password)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales invalidas",
        )

    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token
    )


@router.post("/refresh", response_model=TokenResponse)
def refresh(refresh_token: str, db: Session = Depends(get_db)):
    payload = decode_token(refresh_token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token invalido o expirado",
        )

    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tipo de token incorrecto",
        )

    user_id = payload.get("sub")
    user = db.query(User).filter(User.id == int(user_id)).first()

    if user is None or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado o inactivo",
        )

    new_access_token = create_access_token({"sub": str(user.id)})
    new_refresh_token = create_refresh_token({"sub": str(user.id)})

    return TokenResponse(
        access_token=new_access_token,
        refresh_token=new_refresh_token
    )


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
```

### 8. Punto de Entrada Principal (5 min)

```python
# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine, Base
from app.routers import auth

# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION
)

# CORS seguro
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

# Incluir routers
app.include_router(auth.router)


@app.get("/health")
def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=False)
```

### 9. Archivo .env (5 min)

```env
# .env - NUNCA subir al repositorio
SECRET_KEY=generate-random-64-char-key-here-abcdef1234567890abcdef1234567890
DATABASE_URL=sqlite:///./secure_api.db
```

Generar clave segura con Python:
```python
import secrets
print(secrets.token_hex(32))
```

---

## Ejercicio 1: Crear Proyecto Flask/FastAPI con Estructura Segura

**Enunciado:** Crear la estructura de carpetas completa del proyecto con FastAPI, incluyendo todos los archivos de inicializacion.

**Solucion:**

```
secure-api/
├── app/
│   ├── __init__.py          # from app.main import app
│   ├── main.py              # Punto de entrada
│   ├── config.py            # Configuracion segura
│   ├── database.py          # Conexion BD
│   ├── models/
│   │   ├── __init__.py      # from app.models.user import User
│   │   └── user.py          # Modelo SQLAlchemy
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── user.py          # Pydantic validacion
│   ├── routers/
│   │   ├── __init__.py
│   │   └── auth.py          # Endpoints auth
│   ├── services/
│   │   ├── __init__.py
│   │   └── auth_service.py  # Logica de negocio
│   └── middleware/
│       ├── __init__.py
│       └── security.py      # JWT validation
├── requirements.txt
├── .env.example             # Template sin valores reales
└── .gitignore               # Incluir .env, *.db, __pycache__
```

Recomendacion: Cada `__init__.py` debe exponer las clases/funciones principales:

```python
# app/__init__.py
from app.main import app

# app/models/__init__.py
from app.models.user import User

# app/schemas/__init__.py
from app.schemas.user import UserRegister, UserLogin, UserResponse, TokenResponse

# app/routers/__init__.py
from app.routers.auth import router as auth_router

# app/services/__init__.py
from app.services.auth_service import (
    hash_password, verify_password,
    create_access_token, create_refresh_token,
    decode_token, register_user, authenticate_user
)

# app/middleware/__init__.py
from app.middleware.security import get_current_user
```

---

## Ejercicio 2: Implementar Modelo de Usuario con Contrasena Hasheada

**Enunciado:** Implementar el modelo de usuario SQLAlchemy y la funcion de hashing con bcrypt.

**Solucion:** Ya incluida en las secciones 3 y 5 de la clase. Puntos clave:

- La columna `password_hash` almacena el hash, nunca la contrasena en texto plano
- Se usa `passlib` con `bcrypt` y `bcrypt__rounds=12` (12 rondas de salting)
- La funcion `hash_password()` retorna el hash
- `verify_password()` compara la contrasena ingresada contra el hash
- El hash de bcrypt incluye el salt automaticamente (formato: `$2b$12$...`)

Verificar que funciona:

```python
# test_hash.py
from app.services.auth_service import hash_password, verify_password

password = "MiPassword123!"
hashed = hash_password(password)
print(f"Hash: {hashed}")
# Output: $2b$12$abc123... (60 caracteres)

assert verify_password(password, hashed) == True
assert verify_password("WrongPassword", hashed) == False
print("Hashing funciona correctamente")
```

---

## Ejercicio 3: Implementar Endpoint POST /auth/register con Validacion

**Enunciado:** Implementar el endpoint de registro con validacion estricta de email, username y contrasena.

**Solucion:** Ya incluida en las secciones 4, 5 y 7. Resumen de validaciones:

1. **Email:** Validado con `EmailStr` de Pydantic (formato email valido)
2. **Username:** Longitud 3-50 caracteres, solo alfanumerico + guion bajo, validado con regex
3. **Password:** Longitud 8-128 caracteres, debe tener mayuscula, minuscula y numero
4. **Duplicados:** Se verifica que username y email no existan en BD
5. **Hash:** La contrasena se hashea con bcrypt antes de almacenar
6. **Respuesta:** Nunca devuelve el hash en la respuesta (UserResponse no incluye password_hash)

Ejemplo de request/response:

```bash
# Registro exitoso
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "usuario1",
    "password": "MiPassword123"
  }'

# Respuesta:
# {
#   "id": 1,
#   "email": "user@example.com",
#   "username": "usuario1",
#   "role": "user",
#   "is_active": true
# }

# Registro con error de validacion
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "email-invalido",
    "username": "us",
    "password": "123"
  }'

# Respuesta: 422 Unprocessable Entity con detalles de validacion
```

---

## Ejercicio 4: Implementar Endpoint POST /auth/login con JWT

**Enunciado:** Implementar login que retorne access_token y refresh_token JWT.

**Solucion:** Ya incluida en las secciones 5 y 7. Flujo completo:

1. Recibe username y password
2. Busca usuario en BD por username
3. Verifica contrasena con bcrypt
4. Verifica que el usuario este activo
5. Genera access_token (30 min de validez) y refresh_token (7 dias)
6. Retorna ambos tokens

Tokens JWT contienen:
```json
{
  "sub": "1",        // ID del usuario
  "exp": 1700000000, // Fecha de expiracion
  "type": "access",  // o "refresh"
  "iat": 1700000000  // Fecha de emision
}
```

Ejemplo de login:

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "usuario1",
    "password": "MiPassword123"
  }'

# Respuesta:
# {
#   "access_token": "eyJhbGciOiJIUzI1NiIs...",
#   "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
#   "token_type": "bearer"
# }
```

---

## Preguntas y Respuestas

**1. Por que se usa bcrypt en vez de SHA256 para almacenar contrasenas?**

SHA256 es un hash rapido, disenado para verificacion de integridad. Un atacante puede calcular millones de SHA256 por segundo. Bcrypt es un hash lento por diseno (adaptive hash), incluye salt automatico y permite ajustar el factor de costo. Hace que ataques de fuerza bruta sean impracticables.

**2. Que informacion contiene un JWT y como se protege?**

Un JWT contiene un header (algoritmo), payload (datos como sub, exp, type) y signature. El payload NO debe contener informacion sensible como contrasenas. La firma protege contra manipulacion: si alguien modifica el payload, la firma no valida.

**3. Por que es importante validar los datos de entrada con Pydantic?**

Pydantic valida automaticamente tipos, formatos, longitudes y restricciones personalizadas. Previene que datos maliciosos o malformados lleguen a la base de datos. Reduce el riesgo de injection, buffer overflow y otros ataques basados en entrada no validada.

**4. Que diferencia hay entre access_token y refresh_token?**

El access_token tiene corta duracion (minutos u horas) y se usa para autenticar requests. El refresh_token tiene larga duracion (dias) y solo se usa para obtener nuevos access_tokens sin pedir credenciales nuevamente. Esto limita el dano si un access_token es robado.

**5. Por que se configura CORS con origenes especificos?**

CORS (Cross-Origin Resource Sharing) controla que origenes pueden acceder a la API. Si se configura como `*` (todos los origenes), cualquier sitio web malicioso puede hacer requests desde el navegador del usuario. Restringir a origenes conocidos previene ataques CSRF.

**6. Que es el modelo `from_attributes = True` en Pydantic?**

Permite crear instancias del schema desde objetos SQLAlchemy (ORM). Sin esta configuracion, Pydantic solo acepta diccionarios. Con `from_attributes = True`, se puede pasar directamente un objeto `User` y Pydantic mapea los atributos del modelo a los campos del schema.

**7. Como se genera una SECRET_KEY segura para JWT?**

Usando `secrets.token_hex(32)` de Python que genera 64 caracteres hexadecimales criptograficamente aleatorios. No debe estar hardcodeada en el codigo fuente, sino en variables de entorno o un archivo .env excluido del repositorio.

---

## Tarea / Lectura Recomendada

- Completar la implementacion de la API hasta el login funcionando
- Leer: FastAPI Security Documentation (https://fastapi.tiangolo.com/tutorial/security/)
- Leer: JWT.io para entender la estructura de tokens (https://jwt.io/)
- Investigar: OWASP ASVS (Application Security Verification Standard) nivel 1 y 2
- Preparacion: Traer la API funcionando para la clase 29


