# 3.5 Actividad Completa: Sistema Híbrido de Gestión de Contraseñas

## Objetivo de la Actividad

Implementar un sistema de gestión de contraseñas donde:
- Las contraseñas se almacenan **localmente** en cada usuario
- Un **servidor central** registra eventos y envía notificaciones
- El **administrador** controla qué eventos se notifican
- Cada sistema/servicio tiene su **política de contraseñas** (regex)
- La **master password** rota obligatoriamente
- Cada contraseña tiene su **propio ciclo de rotación**
- La generación automática depende del **ciclo del usuario**
- Todo funciona **sin internet** (red interna)
- Se contempla **teletrabajo** como escenario futuro

---

## Marco Teórico (30 min)

### Conceptos Clave

| Concepto | Definición |
|----------|------------|
| **Vault Local** | Bóveda cifrada en el dispositivo del usuario, nunca sale |
| **Log Central** | Registro de eventos (create/update/delete) en servidor |
| **Política por Sistema** | Reglas de contraseña específicas por servicio (regex) |
| **Rotación Obligatoria** | Cambio forzado de master password cada X días |
| **Rotación por Contraseña** | Cada contraseña tiene su propio tiempo de vida |
| **Generación por Ciclo** | El usuario define cada cuánto generar nuevas contraseñas |
| **Modo Offline** | Funcionamiento completo sin conexión al servidor central |
| **Teletrabajo** | Acceso remoto vía VPN con vault local |

### Flujo General del Sistema

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    FLUJO GENERAL - SISTEMA HÍBRIDO                       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  1. USUARIO ABRE APLICACIÓN LOCAL                                      │
│     │                                                                   │
│     ├── 2. Autenticación: Master Password + 2FA + Biometría          │
│     │                                                                   │
│     ├── 3. Vault local se descifra                                     │
│     │                                                                   │
│     ├── 4. USO DE CONTRASEÑA:                                         │
│     │   ├── Local: acceso inmediato                                    │
│     │   ├── Log: evento enviado al servidor central                   │
│     │   └── Email: notificación si está habilitada                    │
│     │                                                                   │
│     ├── 5. CREACIÓN/MODIFICACIÓN/ELIMINACIÓN:                         │
│     │   ├── Local: cambio aplicado                                     │
│     │   ├── Log: evento registrado en servidor                        │
│     │   └── Email: notificación al usuario                            │
│     │                                                                   │
│     ├── 6. GENERACIÓN AUTOMÁTICA:                                     │
│     │   ├── Según política del sistema (regex)                        │
│     │   ├── Según ciclo del usuario                                   │
│     │   └── Según tiempo de rotación configurado                      │
│     │                                                                   │
│     └── 7. VERIFICACIÓN PERIÓDICA:                                    │
│         ├── ¿Master password vencida? → Forzar cambio                 │
│         ├── ¿Contraseña por vencer? → Notificar                       │
│         └── ¿Contraseña en brecha? → Alertar                          │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Fase 1: Infraestructura (45 min)

### Paso 1: Crear Estructura del Proyecto

```powershell
# Crear directorio del proyecto
mkdir C:\sistema-contrasenas
cd C:\sistema-contrasenas

# Estructura de directorios
mkdir servidor-central
mkdir servidor-central\api
mkdir servidor-central\notificaciones
mkdir servidor-central\logs
mkdir cliente-local
mkdir cliente-local\vaults
mkdir cliente-local\config
mkdir backups
mkdir documentacion
```

### Paso 2: Configurar Servidor Central (API + Logs + Notificaciones)

Crear `servidor-central\docker-compose.yml`:

```yaml
version: '3.8'

services:
  # ============================================
  # API Gateway - Central de Eventos
  # ============================================
  api:
    image: python:3.11-slim
    container_name: central-api
    restart: unless-stopped
    ports:
      - "8443:8443"
    volumes:
      - ./api:/app
      - ./logs:/logs
      - ./config:/config:ro
    environment:
      - DATABASE_URL=postgresql://central:${DB_PASS}@db:5432/central
      - SMTP_HOST=${SMTP_HOST}
      - SMTP_PORT=${SMTP_PORT}
      - SMTP_USER=${SMTP_USER}
      - SMTP_PASS=${SMTP_PASS}
      - JWT_SECRET=${JWT_SECRET}
      - LOG_LEVEL=INFO
    networks:
      - central-net
    depends_on:
      db:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8443/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # ============================================
  # Notificador de Eventos
  # ============================================
  notificador:
    image: python:3.11-slim
    container_name: central-notificador
    restart: unless-stopped
    volumes:
      - ./notificaciones:/app
      - ./logs:/logs
    environment:
      - DATABASE_URL=postgresql://central:${DB_PASS}@db:5432/central
      - SMTP_HOST=${SMTP_HOST}
      - SMTP_PORT=${SMTP_PORT}
      - SMTP_USER=${SMTP_USER}
      - SMTP_PASS=${SMTP_PASS}
      - SMTP_FROM=${SMTP_FROM}
    networks:
      - central-net
    depends_on:
      - api
      - db

  # ============================================
  # PostgreSQL - Base de Datos de Logs
  # ============================================
  db:
    image: postgres:16-alpine
    container_name: central-db
    restart: unless-stopped
    environment:
      POSTGRES_DB: central
      POSTGRES_USER: central
      POSTGRES_PASSWORD: ${DB_PASS}
    volumes:
      - central_data:/var/lib/postgresql/data
    networks:
      - central-net
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U central"]
      interval: 10s
      timeout: 5s
      retries: 5

  # ============================================
  # NGINX - Reverse Proxy
  # ============================================
  nginx:
    image: nginx:alpine
    container_name: central-nginx
    restart: unless-stopped
    ports:
      - "443:443"
      - "80:80"
    volumes:
      - ./config/nginx.conf:/etc/nginx/nginx.conf:ro
    networks:
      - central-net
    depends_on:
      - api

networks:
  central-net:
    driver: bridge

volumes:
  central_data:
```

### Paso 3: Configurar Variables de Entorno

Crear `servidor-central\.env`:

```env
# Base de datos
DB_PASS=C3ntral_S3cur3_DB_2024!

# JWT
JWT_SECRET=jwt_s3cret_k3y_v4ltw4rd3n_bhu_2024

# SMTP (notificaciones)
SMTP_HOST=smtp.bhu.uy
SMTP_PORT=587
SMTP_USER=notificaciones@bhu.uy
SMTP_PASS=smtp_password_aqui
SMTP_FROM=notificaciones@bhu.uy

# Servidor
API_PORT=8443
```

### Paso 4: Script de API Central

Crear `servidor-central\api\app.py`:

```python
#!/usr/bin/env python3
"""
Servidor Central de Eventos - Sistema de Contraseñas BHU
Registra eventos de vaults locales y envía notificaciones
"""

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from datetime import datetime, timedelta
import hashlib
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import logging

app = Flask(__name__)

# Configuración
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

db = SQLAlchemy(app)
jwt = JWTManager(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("central-api")

# ============================================
# MODELOS DE BASE DE DATOS
# ============================================

class EventLog(db.Model):
    """Log de eventos de vaults locales"""
    __tablename__ = 'event_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(255), nullable=False, index=True)
    event_type = db.Column(db.String(50), nullable=False, index=True)
    # event_type: password_created, password_updated, password_deleted,
    #             password_used, master_password_changed, vault_unlocked,
    #             2fa_enabled, 2fa_disabled, device_added
    resource_name = db.Column(db.String(255))
    resource_type = db.Column(db.String(50))  # password, api_key, note, etc.
    collection = db.Column(db.String(255))
    ip_address = db.Column(db.String(45))
    device_info = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    metadata_json = db.Column(db.Text)  # JSON adicional
    email_sent = db.Column(db.Boolean, default=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_email': self.user_email,
            'event_type': self.event_type,
            'resource_name': self.resource_name,
            'resource_type': self.resource_type,
            'collection': self.collection,
            'ip_address': self.ip_address,
            'device_info': self.device_info,
            'timestamp': self.timestamp.isoformat(),
            'email_sent': self.email_sent
        }


class NotificationConfig(db.Model):
    """Configuración de notificaciones por usuario (admin controla)"""
    __tablename__ = 'notification_configs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(255), nullable=False)
    event_type = db.Column(db.String(50), nullable=False)
    email_enabled = db.Column(db.Boolean, default=True)
    webhook_enabled = db.Column(db.Boolean, default=False)
    webhook_url = db.Column(db.String(500))
    
    # Configuración global (admin)
    is_global = db.Column(db.Boolean, default=False)
    admin_email = db.Column(db.String(255))


class PasswordPolicy(db.Model):
    """Política de contraseñas por sistema/servicio"""
    __tablename__ = 'password_policies'
    
    id = db.Column(db.Integer, primary_key=True)
    system_name = db.Column(db.String(255), nullable=False, unique=True)
    description = db.Column(db.Text)
    min_length = db.Column(db.Integer, default=16)
    max_length = db.Column(db.Integer, default=128)
    require_uppercase = db.Column(db.Boolean, default=True)
    require_lowercase = db.Column(db.Boolean, default=True)
    require_numbers = db.Column(db.Boolean, default=True)
    require_symbols = db.Column(db.Boolean, default=True)
    custom_regex = db.Column(db.String(500))  # Expresión regular personalizada
    rotation_days = db.Column(db.Integer, default=90)
    max_age_days = db.Column(db.Integer)  # Sin límite si es None
    allow_reuse = db.Column(db.Boolean, default=False)
    check_hibp = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class MasterPasswordPolicy(db.Model):
    """Política de master password"""
    __tablename__ = 'master_password_policies'
    
    id = db.Column(db.Integer, primary_key=True)
    min_length = db.Column(db.Integer, default=20)
    require_uppercase = db.Column(db.Boolean, default=True)
    require_lowercase = db.Column(db.Boolean, default=True)
    require_numbers = db.Column(db.Boolean, default=True)
    require_symbols = db.Column(db.Boolean, default=True)
    rotation_days = db.Column(db.Integer, default=180)
    max_age_days = db.Column(db.Integer, default=365)
    prevent_reuse_count = db.Column(db.Integer, default=10)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class User(db.Model):
    """Usuarios registrados"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    name = db.Column(db.String(255))
    department = db.Column(db.String(100))
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    last_master_password_change = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# ============================================
# ENDPOINTS DE LA API
# ============================================

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()})


@app.route('/api/v1/events', methods=['POST'])
@jwt_required()
def log_event():
    """Registrar evento desde vault local"""
    data = request.json
    user_email = get_jwt_identity()
    
    event = EventLog(
        user_email=user_email,
        event_type=data.get('event_type'),
        resource_name=data.get('resource_name'),
        resource_type=data.get('resource_type'),
        collection=data.get('collection'),
        ip_address=request.remote_addr,
        device_info=data.get('device_info'),
        metadata_json=json.dumps(data.get('metadata', {}))
    )
    
    db.session.add(event)
    db.session.commit()
    
    logger.info(f"Event logged: {event.event_type} for {user_email}")
    
    # Verificar si se debe enviar notificación
    should_notify = check_notification_config(user_email, event.event_type)
    if should_notify:
        send_notification(event)
    
    return jsonify({'status': 'logged', 'event_id': event.id}), 201


@app.route('/api/v1/events', methods=['GET'])
@jwt_required()
def get_events():
    """Obtener eventos del usuario o todos (admin)"""
    user_email = get_jwt_identity()
    user = User.query.filter_by(email=user_email).first()
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)
    
    query = EventLog.query
    
    if not user or not user.is_admin:
        query = query.filter_by(user_email=user_email)
    
    # Filtros opcionales
    event_type = request.args.get('event_type')
    if event_type:
        query = query.filter_by(event_type=event_type)
    
    start_date = request.args.get('start_date')
    if start_date:
        query = query.filter(EventLog.timestamp >= start_date)
    
    events = query.order_by(EventLog.timestamp.desc()).paginate(
        page=page, per_page=per_page
    )
    
    return jsonify({
        'events': [e.to_dict() for e in events.items],
        'total': events.total,
        'pages': events.pages,
        'current_page': events.page
    })


@app.route('/api/v1/policies', methods=['GET'])
@jwt_required()
def get_policies():
    """Obtener todas las políticas de contraseñas"""
    policies = PasswordPolicy.query.all()
    return jsonify([{
        'id': p.id,
        'system_name': p.system_name,
        'description': p.description,
        'min_length': p.min_length,
        'max_length': p.max_length,
        'require_uppercase': p.require_uppercase,
        'require_lowercase': p.require_lowercase,
        'require_numbers': p.require_numbers,
        'require_symbols': p.require_symbols,
        'custom_regex': p.custom_regex,
        'rotation_days': p.rotation_days,
        'max_age_days': p.max_age_days,
        'allow_reuse': p.allow_reuse,
        'check_hibp': p.check_hibp
    } for p in policies])


@app.route('/api/v1/policies', methods=['POST'])
@jwt_required()
def create_policy():
    """Crear nueva política de contraseñas (admin)"""
    data = request.json
    
    policy = PasswordPolicy(
        system_name=data['system_name'],
        description=data.get('description'),
        min_length=data.get('min_length', 16),
        max_length=data.get('max_length', 128),
        require_uppercase=data.get('require_uppercase', True),
        require_lowercase=data.get('require_lowercase', True),
        require_numbers=data.get('require_numbers', True),
        require_symbols=data.get('require_symbols', True),
        custom_regex=data.get('custom_regex'),
        rotation_days=data.get('rotation_days', 90),
        max_age_days=data.get('max_age_days'),
        allow_reuse=data.get('allow_reuse', False),
        check_hibp=data.get('check_hibp', True)
    )
    
    db.session.add(policy)
    db.session.commit()
    
    return jsonify({'status': 'created', 'policy_id': policy.id}), 201


@app.route('/api/v1/policies/<int:policy_id>', methods=['PUT'])
@jwt_required()
def update_policy(policy_id):
    """Actualizar política de contraseñas (admin)"""
    policy = PasswordPolicy.query.get_or_404(policy_id)
    data = request.json
    
    for key in ['system_name', 'description', 'min_length', 'max_length',
                'require_uppercase', 'require_lowercase', 'require_numbers',
                'require_symbols', 'custom_regex', 'rotation_days',
                'max_age_days', 'allow_reuse', 'check_hibp']:
        if key in data:
            setattr(policy, key, data[key])
    
    db.session.commit()
    
    return jsonify({'status': 'updated'})


@app.route('/api/v1/policies/<int:policy_id>', methods=['DELETE'])
@jwt_required()
def delete_policy(policy_id):
    """Eliminar política de contraseñas (admin)"""
    policy = PasswordPolicy.query.get_or_404(policy_id)
    db.session.delete(policy)
    db.session.commit()
    
    return jsonify({'status': 'deleted'})


@app.route('/api/v1/master-password-policy', methods=['GET'])
@jwt_required()
def get_master_password_policy():
    """Obtener política de master password"""
    policy = MasterPasswordPolicy.query.first()
    if not policy:
        policy = MasterPasswordPolicy()
        db.session.add(policy)
        db.session.commit()
    
    return jsonify({
        'min_length': policy.min_length,
        'require_uppercase': policy.require_uppercase,
        'require_lowercase': policy.require_lowercase,
        'require_numbers': policy.require_numbers,
        'require_symbols': policy.require_symbols,
        'rotation_days': policy.rotation_days,
        'max_age_days': policy.max_age_days,
        'prevent_reuse_count': policy.prevent_reuse_count
    })


@app.route('/api/v1/master-password-policy', methods=['PUT'])
@jwt_required()
def update_master_password_policy():
    """Actualizar política de master password (admin)"""
    policy = MasterPasswordPolicy.query.first()
    if not policy:
        policy = MasterPasswordPolicy()
        db.session.add(policy)
    
    data = request.json
    for key in ['min_length', 'require_uppercase', 'require_lowercase',
                'require_numbers', 'require_symbols', 'rotation_days',
                'max_age_days', 'prevent_reuse_count']:
        if key in data:
            setattr(policy, key, data[key])
    
    db.session.commit()
    
    return jsonify({'status': 'updated'})


@app.route('/api/v1/notification-config', methods=['GET'])
@jwt_required()
def get_notification_config():
    """Obtener configuración de notificaciones"""
    user_email = get_jwt_identity()
    configs = NotificationConfig.query.filter_by(user_email=user_email).all()
    
    # También obtener configuración global
    global_configs = NotificationConfig.query.filter_by(is_global=True).all()
    
    return jsonify({
        'user_configs': [{
            'event_type': c.event_type,
            'email_enabled': c.email_enabled,
            'webhook_enabled': c.webhook_enabled,
            'webhook_url': c.webhook_url
        } for c in configs],
        'global_configs': [{
            'event_type': c.event_type,
            'email_enabled': c.email_enabled,
            'admin_email': c.admin_email
        } for c in global_configs]
    })


@app.route('/api/v1/notification-config', methods=['POST'])
@jwt_required()
def update_notification_config():
    """Actualizar configuración de notificaciones (admin)"""
    data = request.json
    
    # Actualizar o crear configuración
    config = NotificationConfig.query.filter_by(
        user_email=data['user_email'],
        event_type=data['event_type'],
        is_global=data.get('is_global', False)
    ).first()
    
    if not config:
        config = NotificationConfig(
            user_email=data['user_email'],
            event_type=data['event_type'],
            is_global=data.get('is_global', False)
        )
        db.session.add(config)
    
    config.email_enabled = data.get('email_enabled', True)
    config.webhook_enabled = data.get('webhook_enabled', False)
    config.webhook_url = data.get('webhook_url')
    config.admin_email = data.get('admin_email')
    
    db.session.commit()
    
    return jsonify({'status': 'updated'})


@app.route('/api/v1/users', methods=['GET'])
@jwt_required()
def get_users():
    """Obtener lista de usuarios"""
    users = User.query.all()
    return jsonify([{
        'id': u.id,
        'email': u.email,
        'name': u.name,
        'department': u.department,
        'is_admin': u.is_admin,
        'is_active': u.is_active,
        'last_master_password_change': u.last_master_password_change.isoformat() if u.last_master_password_change else None
    } for u in users])


@app.route('/api/v1/users', methods=['POST'])
@jwt_required()
def create_user():
    """Registrar nuevo usuario"""
    data = request.json
    
    user = User(
        email=data['email'],
        name=data.get('name'),
        department=data.get('department'),
        is_admin=data.get('is_admin', False)
    )
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'status': 'created', 'user_id': user.id}), 201


@app.route('/api/v1/users/<int:user_id>/master-password-changed', methods=['POST'])
@jwt_required()
def record_master_password_change(user_id):
    """Registrar cambio de master password"""
    user = User.query.get_or_404(user_id)
    user.last_master_password_change = datetime.utcnow()
    db.session.commit()
    
    return jsonify({'status': 'recorded'})


# ============================================
# FUNCIONES AUXILIARES
# ============================================

def check_notification_config(user_email, event_type):
    """Verificar si se debe enviar notificación para este evento"""
    # Buscar configuración específica del usuario
    config = NotificationConfig.query.filter_by(
        user_email=user_email,
        event_type=event_type,
        is_global=False
    ).first()
    
    if config:
        return config.email_enabled
    
    # Buscar configuración global
    global_config = NotificationConfig.query.filter_by(
        event_type=event_type,
        is_global=True
    ).first()
    
    if global_config:
        return global_config.email_enabled
    
    # Default: notificar eventos críticos
    critical_events = [
        'master_password_changed', '2fa_disabled', 
        'vault_exported', 'device_added'
    ]
    return event_type in critical_events


def send_notification(event):
    """Enviar notificación por email"""
    try:
        smtp_host = os.environ.get('SMTP_HOST')
        smtp_port = int(os.environ.get('SMTP_PORT', 587))
        smtp_user = os.environ.get('SMTP_USER')
        smtp_pass = os.environ.get('SMTP_PASS')
        smtp_from = os.environ.get('SMTP_FROM')
        
        # Construir mensaje según tipo de evento
        subject, body = build_notification(event)
        
        msg = MIMEMultipart()
        msg['From'] = f"BHU Vaultwarden <{smtp_from}>"
        msg['To'] = event.user_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html', 'utf-8'))
        
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.send_message(msg)
        server.quit()
        
        # Marcar como enviado
        event.email_sent = True
        db.session.commit()
        
        logger.info(f"Notification sent: {event.event_type} to {event.user_email}")
        
    except Exception as e:
        logger.error(f"Error sending notification: {e}")


def build_notification(event):
    """Construir asunto y cuerpo del email según tipo de evento"""
    templates = {
        'password_created': {
            'subject': f'Contraseña creada: {event.resource_name}',
            'body': f'''
            <h2>Nueva contraseña creada</h2>
            <p><strong>Recurso:</strong> {event.resource_name}</p>
            <p><strong>Tipo:</strong> {event.resource_type}</p>
            <p><strong>Colección:</strong> {event.collection}</p>
            <p><strong>Fecha:</strong> {event.timestamp}</p>
            <p><strong>IP:</strong> {event.ip_address}</p>
            <p><strong>Dispositivo:</strong> {event.device_info}</p>
            <hr>
            <p><em>Si no creaste esta contraseña, contacta a IT inmediatamente.</em></p>
            '''
        },
        'password_updated': {
            'subject': f'Contraseña modificada: {event.resource_name}',
            'body': f'''
            <h2>Contraseña modificada</h2>
            <p><strong>Recurso:</strong> {event.resource_name}</p>
            <p><strong>Fecha:</strong> {event.timestamp}</p>
            <p><strong>IP:</strong> {event.ip_address}</p>
            <p><strong>Dispositivo:</strong> {event.device_info}</p>
            <hr>
            <p><em>Si no realizaste este cambio, contacta a IT inmediatamente.</em></p>
            '''
        },
        'password_deleted': {
            'subject': f'Contraseña eliminada: {event.resource_name}',
            'body': f'''
            <h2>Contraseña eliminada</h2>
            <p><strong>Recurso:</strong> {event.resource_name}</p>
            <p><strong>Fecha:</strong> {event.timestamp}</p>
            <p><strong>IP:</strong> {event.ip_address}</p>
            <hr>
            <p><em>Si no eliminaste esta contraseña, contacta a IT inmediatamente.</em></p>
            '''
        },
        'password_used': {
            'subject': f'Contraseña utilizada: {event.resource_name}',
            'body': f'''
            <h2>Contraseña utilizada</h2>
            <p><strong>Recurso:</strong> {event.resource_name}</p>
            <p><strong>Fecha:</strong> {event.timestamp}</p>
            <p><strong>IP:</strong> {event.ip_address}</p>
            <p><strong>Dispositivo:</strong> {event.device_info}</p>
            <hr>
            <p><em>Si no utilizaste esta contraseña, verifica la seguridad de tu cuenta.</em></p>
            '''
        },
        'master_password_changed': {
            'subject': 'ALERTA: Master Password cambiada',
            'body': f'''
            <h2 style="color: red;">ALERTA: Master Password cambiada</h2>
            <p><strong>Fecha:</strong> {event.timestamp}</p>
            <p><strong>IP:</strong> {event.ip_address}</p>
            <p><strong>Dispositivo:</strong> {event.device_info}</p>
            <hr>
            <p><strong>Si no realizaste este cambio, contacta a IT INMEDIATAMENTE.</strong></p>
            '''
        },
        '2fa_disabled': {
            'subject': 'ALERTA CRÍTICO: 2FA deshabilitado',
            'body': f'''
            <h2 style="color: red;">ALERTA CRÍTICO: 2FA deshabilitado</h2>
            <p><strong>Fecha:</strong> {event.timestamp}</p>
            <p><strong>IP:</strong> {event.ip_address}</p>
            <hr>
            <p><strong style="color: red;">ACCIÓN INMEDIATA REQUERIDA: 
            Contacta a IT y re-habilita 2FA.</strong></p>
            '''
        },
        'device_added': {
            'subject': 'Nuevo dispositivo registrado',
            'body': f'''
            <h2>Nuevo dispositivo registrado en tu vault</h2>
            <p><strong>Dispositivo:</strong> {event.device_info}</p>
            <p><strong>Fecha:</strong> {event.timestamp}</p>
            <p><strong>IP:</strong> {event.ip_address}</p>
            <hr>
            <p><em>Si no reconoces este dispositivo, contacta a IT.</em></p>
            '''
        }
    }
    
    template = templates.get(event.event_type, {
        'subject': f'Evento de seguridad: {event.event_type}',
        'body': f'<p>Evento: {event.event_type}</p><p>Fecha: {event.timestamp}</p>'
    })
    
    return template['subject'], template['body']


# ============================================
# INICIALIZACIÓN
# ============================================

with app.app_context():
    db.create_all()
    
    # Crear política de master password por defecto si no existe
    if not MasterPasswordPolicy.query.first():
        default_policy = MasterPasswordPolicy()
        db.session.add(default_policy)
        db.session.commit()
        logger.info("Default master password policy created")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8443, debug=False)
```

### Paso 5: Script de Notificaciones

Crear `servidor-central\notificaciones\notificador.py`:

```python
#!/usr/bin/env python3
"""
Servicio de Notificaciones - Procesa eventos y envía emails
"""

import time
import smtplib
import json
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import os
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("notificador")

# Configuración
CHECK_INTERVAL = 60  # Segundos entre verificaciones
SMTP_HOST = os.environ.get('SMTP_HOST')
SMTP_PORT = int(os.environ.get('SMTP_PORT', 587))
SMTP_USER = os.environ.get('SMTP_USER')
SMTP_PASS = os.environ.get('SMTP_PASS')
SMTP_FROM = os.environ.get('SMTP_FROM')
API_URL = "http://api:8443"


def check_pending_notifications():
    """Verificar eventos pendientes de notificación"""
    try:
        # Obtener eventos de las últimas 24 horas sin email enviado
        response = requests.get(
            f"{API_URL}/api/v1/events",
            params={'per_page': 100},
            headers={'Authorization': f'Bearer {get_system_token()}'}
        )
        
        if response.status_code == 200:
            events = response.json().get('events', [])
            pending = [e for e in events if not e.get('email_sent')]
            
            for event in pending:
                process_event(event)
                
    except Exception as e:
        logger.error(f"Error checking notifications: {e}")


def process_event(event):
    """Procesar un evento y enviar notificación si corresponde"""
    logger.info(f"Processing event: {event['event_type']} for {event['user_email']}")
    
    # Verificar configuración de notificación
    if should_notify(event['user_email'], event['event_type']):
        send_email_notification(event)
        mark_as_notified(event['id'])


def should_notify(user_email, event_type):
    """Verificar si se debe notificar para este evento"""
    # Eventos siempre notificados (críticos)
    always_notify = [
        'master_password_changed',
        '2fa_disabled',
        'vault_exported',
        'device_added'
    ]
    
    if event_type in always_notify:
        return True
    
    # Para otros eventos, verificar configuración
    # (por defecto, notificar todos los cambios)
    return True


def send_email_notification(event):
    """Enviar notificación por email"""
    try:
        subject, body = build_email(event)
        
        msg = MIMEMultipart()
        msg['From'] = f"BHU Vaultwarden <{SMTP_FROM}>"
        msg['To'] = event['user_email']
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html', 'utf-8'))
        
        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)
        server.quit()
        
        logger.info(f"Email sent: {event['event_type']} to {event['user_email']}")
        
    except Exception as e:
        logger.error(f"Error sending email: {e}")


def build_email(event):
    """Construir email de notificación"""
    templates = {
        'password_created': (
            f"Contraseña creada: {event.get('resource_name', 'N/A')}",
            f"<h2>Nueva contraseña creada</h2>"
            f"<p>Recurso: {event.get('resource_name', 'N/A')}</p>"
            f"<p>Fecha: {event.get('timestamp', 'N/A')}</p>"
            f"<p>IP: {event.get('ip_address', 'N/A')}</p>"
        ),
        'password_updated': (
            f"Contraseña modificada: {event.get('resource_name', 'N/A')}",
            f"<h2>Contraseña modificada</h2>"
            f"<p>Recurso: {event.get('resource_name', 'N/A')}</p>"
            f"<p>Fecha: {event.get('timestamp', 'N/A')}</p>"
        ),
        'password_deleted': (
            f"Contraseña eliminada: {event.get('resource_name', 'N/A')}",
            f"<h2>Contraseña eliminada</h2>"
            f"<p>Recurso: {event.get('resource_name', 'N/A')}</p>"
            f"<p>Fecha: {event.get('timestamp', 'N/A')}</p>"
        ),
        'password_used': (
            f"Contraseña utilizada: {event.get('resource_name', 'N/A')}",
            f"<h2>Contraseña utilizada</h2>"
            f"<p>Recurso: {event.get('resource_name', 'N/A')}</p>"
            f"<p>Fecha: {event.get('timestamp', 'N/A')}</p>"
        ),
    }
    
    return templates.get(event['event_type'], (
        f"Evento: {event['event_type']}",
        f"<p>Evento: {event['event_type']}</p>"
    ))


def mark_as_notified(event_id):
    """Marcar evento como notificado"""
    try:
        requests.put(
            f"{API_URL}/api/v1/events/{event_id}/notified",
            headers={'Authorization': f'Bearer {get_system_token()}'}
        )
    except Exception as e:
        logger.error(f"Error marking event as notified: {e}")


def get_system_token():
    """Obtener token del sistema (service account)"""
    # En producción, usar JWT o API key del sistema
    return os.environ.get('SYSTEM_TOKEN', 'system_token_placeholder')


if __name__ == '__main__':
    logger.info("Notificador iniciado")
    while True:
        check_pending_notifications()
        time.sleep(CHECK_INTERVAL)
```

---

## Fase 2: Cliente Local (30 min)

### Paso 6: Configurar Vault Local con Políticas

Crear `cliente-local\config\policies.json`:

```json
{
  "master_password": {
    "min_length": 20,
    "require_uppercase": true,
    "require_lowercase": true,
    "require_numbers": true,
    "require_symbols": true,
    "rotation_days": 180,
    "max_age_days": 365,
    "prevent_reuse_count": 10
  },
  "default_password": {
    "min_length": 16,
    "max_length": 128,
    "require_uppercase": true,
    "require_lowercase": true,
    "require_numbers": true,
    "require_symbols": true,
    "rotation_days": 90,
    "check_hibp": true
  },
  "systems": {
    "linux_server": {
      "name": "Linux Servers",
      "min_length": 24,
      "require_uppercase": true,
      "require_lowercase": true,
      "require_numbers": true,
      "require_symbols": true,
      "custom_regex": "^(?=.*[A-Z])(?=.*[a-z])(?=.*\\d)(?=.*[@$!%*?&#])[A-Za-z\\d@$!%*?&#]{24,}$",
      "rotation_days": 60,
      "description": "Credenciales de acceso a servidores Linux"
    },
    "windows_ad": {
      "name": "Windows/Active Directory",
      "min_length": 16,
      "require_uppercase": true,
      "require_lowercase": true,
      "require_numbers": true,
      "require_symbols": true,
      "rotation_days": 90,
      "description": "Credenciales de dominio Windows"
    },
    "database": {
      "name": "Bases de Datos",
      "min_length": 32,
      "require_uppercase": true,
      "require_lowercase": true,
      "require_numbers": true,
      "require_symbols": true,
      "custom_regex": "^(?=.*[A-Z])(?=.*[a-z])(?=.*\\d)(?=.*[^A-Za-z0-9]).{32,}$",
      "rotation_days": 30,
      "description": "Credenciales de bases de datos (MySQL, PostgreSQL, MongoDB)"
    },
    "api_keys": {
      "name": "API Keys y Tokens",
      "min_length": 32,
      "require_uppercase": true,
      "require_lowercase": true,
      "require_numbers": true,
      "require_symbols": false,
      "rotation_days": 90,
      "description": "API keys de servicios externos"
    },
    "web_services": {
      "name": "Servicios Web",
      "min_length": 16,
      "require_uppercase": true,
      "require_lowercase": true,
      "require_numbers": true,
      "require_symbols": true,
      "rotation_days": 90,
      "description": "Credenciales de paneles web, CMS, etc."
    },
    "email": {
      "name": "Cuentas de Email",
      "min_length": 16,
      "require_uppercase": true,
      "require_lowercase": true,
      "require_numbers": true,
      "require_symbols": true,
      "rotation_days": 180,
      "description": "Cuentas de correo electrónico"
    },
    "wifi": {
      "name": "Redes WiFi",
      "min_length": 20,
      "require_uppercase": true,
      "require_lowercase": true,
      "require_numbers": true,
      "require_symbols": true,
      "rotation_days": 180,
      "description": "Contraseñas de redes WiFi"
    },
    "vpn": {
      "name": "VPN",
      "min_length": 24,
      "require_uppercase": true,
      "require_lowercase": true,
      "require_numbers": true,
      "require_symbols": true,
      "rotation_days": 90,
      "description": "Credenciales de acceso VPN"
    },
    "cloud_services": {
      "name": "Servicios Cloud",
      "min_length": 24,
      "require_uppercase": true,
      "require_lowercase": true,
      "require_numbers": true,
      "require_symbols": true,
      "rotation_days": 60,
      "description": "AWS, Azure, GCP, etc."
    },
    "personal": {
      "name": "Uso Personal",
      "min_length": 12,
      "require_uppercase": true,
      "require_lowercase": true,
      "require_numbers": true,
      "require_symbols": false,
      "rotation_days": 180,
      "description": "Cuentas personales (redes sociales, etc.)"
    }
  },
  "notifications": {
    "password_created": {
      "email_enabled": true,
      "webhook_enabled": false
    },
    "password_updated": {
      "email_enabled": true,
      "webhook_enabled": false
    },
    "password_deleted": {
      "email_enabled": true,
      "webhook_enabled": false
    },
    "password_used": {
      "email_enabled": true,
      "webhook_enabled": false
    },
    "master_password_changed": {
      "email_enabled": true,
      "webhook_enabled": false
    },
    "2fa_disabled": {
      "email_enabled": true,
      "webhook_enabled": false
    },
    "device_added": {
      "email_enabled": true,
      "webhook_enabled": false
    }
  }
}
```

### Paso 7: Script de Cliente Local

Crear `cliente-local\vault_client.py`:

```python
#!/usr/bin/env python3
"""
Cliente Local - Gestión de Vault con Conexión al Servidor Central
"""

import json
import os
import hashlib
import base64
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import requests
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("vault-client")

# Configuración
VAULT_DIR = os.path.expanduser("~/.vault-local")
CONFIG_FILE = os.path.join(VAULT_DIR, "config", "policies.json")
VAULT_FILE = os.path.join(VAULT_DIR, "vault.enc")
SERVER_URL = "https://central.bhu.uy:8443"
LOG_FILE = os.path.join(VAULT_DIR, "logs", "local.log")

class VaultClient:
    def __init__(self):
        self.ensure_directories()
        self.load_config()
        self.vault_data = {}
        self.master_password = None
        self.fernet = None
        
    def ensure_directories(self):
        """Crear directorios necesarios"""
        dirs = [
            VAULT_DIR,
            os.path.join(VAULT_DIR, "config"),
            os.path.join(VAULT_DIR, "logs"),
            os.path.join(VAULT_DIR, "backups")
        ]
        for d in dirs:
            os.makedirs(d, exist_ok=True)
    
    def load_config(self):
        """Cargar políticas de contraseñas"""
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = self.get_default_config()
            self.save_config()
    
    def get_default_config(self):
        """Configuración por defecto"""
        return {
            "master_password": {
                "min_length": 20,
                "rotation_days": 180,
                "max_age_days": 365
            },
            "systems": {},
            "notifications": {}
        }
    
    def save_config(self):
        """Guardar configuración"""
        with open(CONFIG_FILE, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def unlock(self, master_password):
        """Descifrar vault con master password"""
        self.master_password = master_password
        
        # Derivar clave de cifrado
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b'vault-salt-bhu-2024',  # En producción, usar salt único
            iterations=480000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
        self.fernet = Fernet(key)
        
        # Cargar vault si existe
        if os.path.exists(VAULT_FILE):
            self.load_vault()
        
        # Registrar evento
        self.log_event('vault_unlocked')
        
        logger.info("Vault descifrado exitosamente")
        return True
    
    def load_vault(self):
        """Cargar vault cifrado"""
        with open(VAULT_FILE, 'rb') as f:
            encrypted_data = f.read()
        
        try:
            decrypted_data = self.fernet.decrypt(encrypted_data)
            self.vault_data = json.loads(decrypted_data)
        except Exception as e:
            logger.error(f"Error descifrando vault: {e}")
            raise
    
    def save_vault(self):
        """Guardar vault cifrado"""
        if not self.fernet:
            raise Exception("Vault no está descifrado")
        
        data = json.dumps(self.vault_data, indent=2).encode()
        encrypted_data = self.fernet.encrypt(data)
        
        with open(VAULT_FILE, 'wb') as f:
            f.write(encrypted_data)
    
    def add_credential(self, system_type, name, username, password, url=None, notes=None):
        """Agregar nueva credencial"""
        # Verificar política del sistema
        policy = self.config.get('systems', {}).get(system_type, self.config.get('default_password', {}))
        
        # Validar contraseña contra política
        if not self.validate_password(password, policy):
            raise ValueError(f"La contraseña no cumple la política de {system_type}")
        
        # Crear entrada
        credential = {
            'id': hashlib.md5(f"{system_type}:{name}:{datetime.now().isoformat()}".encode()).hexdigest(),
            'system_type': system_type,
            'name': name,
            'username': username,
            'password': password,
            'url': url,
            'notes': notes,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'last_used': None,
            'rotation_days': policy.get('rotation_days', 90),
            'next_rotation': (datetime.now() + timedelta(days=policy.get('rotation_days', 90))).isoformat()
        }
        
        # Guardar en vault local
        if system_type not in self.vault_data:
            self.vault_data[system_type] = []
        
        self.vault_data[system_type].append(credential)
        self.save_vault()
        
        # Log local
        self.log_event('password_created', {
            'resource_name': name,
            'resource_type': system_type,
            'collection': system_type
        })
        
        # Enviar a servidor central
        self.send_event_to_server('password_created', {
            'resource_name': name,
            'resource_type': system_type,
            'collection': system_type
        })
        
        logger.info(f"Credencial agregada: {name} ({system_type})")
        return credential
    
    def update_credential(self, credential_id, **kwargs):
        """Actualizar credencial existente"""
        for system_type, credentials in self.vault_data.items():
            for i, cred in enumerate(credentials):
                if cred['id'] == credential_id:
                    # Actualizar campos
                    for key, value in kwargs.items():
                        if key in ['username', 'password', 'url', 'notes']:
                            cred[key] = value
                    
                    cred['updated_at'] = datetime.now().isoformat()
                    
                    # Recalcular próxima rotación si cambió la contraseña
                    if 'password' in kwargs:
                        policy = self.config.get('systems', {}).get(system_type, {})
                        cred['next_rotation'] = (
                            datetime.now() + timedelta(days=policy.get('rotation_days', 90))
                        ).isoformat()
                    
                    self.save_vault()
                    
                    # Log
                    self.log_event('password_updated', {
                        'resource_name': cred['name'],
                        'resource_type': system_type
                    })
                    
                    # Enviar a servidor
                    self.send_event_to_server('password_updated', {
                        'resource_name': cred['name'],
                        'resource_type': system_type
                    })
                    
                    logger.info(f"Credencial actualizada: {cred['name']}")
                    return cred
        
        raise ValueError(f"Credencial no encontrada: {credential_id}")
    
    def delete_credential(self, credential_id):
        """Eliminar credencial"""
        for system_type, credentials in self.vault_data.items():
            for i, cred in enumerate(credentials):
                if cred['id'] == credential_id:
                    # Log antes de eliminar
                    self.log_event('password_deleted', {
                        'resource_name': cred['name'],
                        'resource_type': system_type
                    })
                    
                    # Enviar a servidor
                    self.send_event_to_server('password_deleted', {
                        'resource_name': cred['name'],
                        'resource_type': system_type
                    })
                    
                    # Eliminar
                    del self.vault_data[system_type][i]
                    self.save_vault()
                    
                    logger.info(f"Credencial eliminada: {cred['name']}")
                    return True
        
        raise ValueError(f"Credencial no encontrada: {credential_id}")
    
    def use_credential(self, credential_id):
        """Registrar uso de credencial"""
        for system_type, credentials in self.vault_data.items():
            for cred in credentials:
                if cred['id'] == credential_id:
                    cred['last_used'] = datetime.now().isoformat()
                    self.save_vault()
                    
                    # Log
                    self.log_event('password_used', {
                        'resource_name': cred['name'],
                        'resource_type': system_type
                    })
                    
                    # Enviar a servidor
                    self.send_event_to_server('password_used', {
                        'resource_name': cred['name'],
                        'resource_type': system_type
                    })
                    
                    logger.info(f"Credencial utilizada: {cred['name']}")
                    return cred
        
        raise ValueError(f"Credencial no encontrada: {credential_id}")
    
    def generate_password(self, system_type, length=None):
        """Generar contraseña según política del sistema"""
        import secrets
        import string
        
        policy = self.config.get('systems', {}).get(system_type, self.config.get('default_password', {}))
        
        if length is None:
            length = policy.get('min_length', 16)
        
        # Construir alfabeto según política
        chars = ""
        if policy.get('require_lowercase', True):
            chars += string.ascii_lowercase
        if policy.get('require_uppercase', True):
            chars += string.ascii_uppercase
        if policy.get('require_numbers', True):
            chars += string.digits
        if policy.get('require_symbols', True):
            chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        # Generar contraseña
        while True:
            password = ''.join(secrets.choice(chars) for _ in range(length))
            
            # Verificar que cumple requisitos mínimos
            if (not policy.get('require_lowercase') or any(c.islower() for c in password) and
                not policy.get('require_uppercase') or any(c.isupper() for c in password) and
                not policy.get('require_numbers') or any(c.isdigit() for c in password) and
                not policy.get('require_symbols') or any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)):
                break
        
        logger.info(f"Contraseña generada para {system_type} ({length} caracteres)")
        return password
    
    def validate_password(self, password, policy):
        """Validar contraseña contra política"""
        if len(password) < policy.get('min_length', 16):
            return False
        
        if policy.get('require_uppercase') and not any(c.isupper() for c in password):
            return False
        
        if policy.get('require_lowercase') and not any(c.islower() for c in password):
            return False
        
        if policy.get('require_numbers') and not any(c.isdigit() for c in password):
            return False
        
        if policy.get('require_symbols') and not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            return False
        
        # Verificar regex personalizada si existe
        if policy.get('custom_regex'):
            import re
            if not re.match(policy['custom_regex'], password):
                return False
        
        return True
    
    def check_rotation_needed(self):
        """Verificar si hay contraseñas que necesitan rotación"""
        needs_rotation = []
        now = datetime.now()
        
        for system_type, credentials in self.vault_data.items():
            for cred in credentials:
                if cred.get('next_rotation'):
                    next_rotation = datetime.fromisoformat(cred['next_rotation'])
                    if now >= next_rotation:
                        needs_rotation.append({
                            'credential': cred,
                            'system_type': system_type,
                            'overdue_days': (now - next_rotation).days
                        })
        
        return needs_rotation
    
    def log_event(self, event_type, metadata=None):
        """Registrar evento en log local"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'event_type': event_type,
            'metadata': metadata or {}
        }
        
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        
        with open(LOG_FILE, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
    
    def send_event_to_server(self, event_type, metadata=None):
        """Enviar evento al servidor central"""
        try:
            # Enviar con retry
            for attempt in range(3):
                try:
                    response = requests.post(
                        f"{SERVER_URL}/api/v1/events",
                        json={
                            'event_type': event_type,
                            'device_info': self.get_device_info(),
                            **(metadata or {})
                        },
                        headers={'Authorization': f'Bearer {self.get_auth_token()}'},
                        timeout=10,
                        verify=True
                    )
                    
                    if response.status_code == 201:
                        logger.info(f"Evento enviado al servidor: {event_type}")
                        return True
                        
                except requests.exceptions.ConnectionError:
                    logger.warning(f"Servidor no disponible (intento {attempt + 1}/3)")
                    time.sleep(2 ** attempt)
            
            # Si no pudo enviar, guardar para enviar después
            self.queue_event(event_type, metadata)
            return False
            
        except Exception as e:
            logger.error(f"Error enviando evento: {e}")
            self.queue_event(event_type, metadata)
            return False
    
    def queue_event(self, event_type, metadata):
        """Cola de eventos para enviar cuando haya conexión"""
        queue_file = os.path.join(VAULT_DIR, "logs", "pending_events.json")
        
        events = []
        if os.path.exists(queue_file):
            with open(queue_file, 'r') as f:
                events = json.load(f)
        
        events.append({
            'event_type': event_type,
            'timestamp': datetime.now().isoformat(),
            'metadata': metadata or {}
        })
        
        with open(queue_file, 'w') as f:
            json.dump(events, f, indent=2)
    
    def sync_pending_events(self):
        """Sincronizar eventos pendientes con el servidor"""
        queue_file = os.path.join(VAULT_DIR, "logs", "pending_events.json")
        
        if not os.path.exists(queue_file):
            return
        
        with open(queue_file, 'r') as f:
            events = json.load(f)
        
        if not events:
            return
        
        sent_count = 0
        for event in events[:]:
            try:
                response = requests.post(
                    f"{SERVER_URL}/api/v1/events",
                    json=event,
                    headers={'Authorization': f'Bearer {self.get_auth_token()}'},
                    timeout=10
                )
                
                if response.status_code == 201:
                    events.remove(event)
                    sent_count += 1
                    
            except Exception:
                break
        
        # Guardar eventos restantes
        with open(queue_file, 'w') as f:
            json.dump(events, f, indent=2)
        
        logger.info(f"Sincronizados {sent_count} eventos pendientes")
    
    def get_device_info(self):
        """Obtener información del dispositivo"""
        import platform
        return {
            'os': platform.system(),
            'hostname': platform.node(),
            'python_version': platform.python_version()
        }
    
    def get_auth_token(self):
        """Obtener token de autenticación"""
        # En producción, usar JWT real
        return os.environ.get('VAULT_AUTH_TOKEN', 'default_token')
    
    def backup_vault(self):
        """Crear backup del vault"""
        backup_dir = os.path.join(VAULT_DIR, "backups")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(backup_dir, f"vault_backup_{timestamp}.enc")
        
        if os.path.exists(VAULT_FILE):
            import shutil
            shutil.copy2(VAULT_FILE, backup_file)
            logger.info(f"Backup creado: {backup_file}")
            return backup_file
        
        return None


# ============================================
# INTERFAZ DE LÍNEA DE COMANDOS
# ============================================

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Cliente Local de Vault')
    subparsers = parser.add_subparsers(dest='command', help='Comandos disponibles')
    
    # unlock
    unlock_parser = subparsers.add_parser('unlock', help='Descifrar vault')
    unlock_parser.add_argument('--master-password', required=True, help='Master password')
    
    # add
    add_parser = subparsers.add_parser('add', help='Agregar credencial')
    add_parser.add_argument('--system', required=True, help='Tipo de sistema')
    add_parser.add_argument('--name', required=True, help='Nombre')
    add_parser.add_argument('--username', required=True, help='Usuario')
    add_parser.add_argument('--password', help='Contraseña (se genera si no se especifica)')
    add_parser.add_argument('--url', help='URL')
    add_parser.add_argument('--notes', help='Notas')
    
    # generate
    gen_parser = subparsers.add_parser('generate', help='Generar contraseña')
    gen_parser.add_argument('--system', required=True, help='Tipo de sistema')
    gen_parser.add_argument('--length', type=int, help='Longitud')
    
    # check-rotation
    subparsers.add_parser('check-rotation', help='Verificar rotación pendiente')
    
    # list
    subparsers.add_parser('list', help='Listar credenciales')
    
    # sync
    subparsers.add_parser('sync', help='Sincronizar con servidor')
    
    # backup
    subparsers.add_parser('backup', help='Crear backup')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    client = VaultClient()
    
    if args.command == 'unlock':
        client.unlock(args.master_password)
        print("Vault descifrado exitosamente")
        
    elif args.command == 'generate':
        password = client.generate_password(args.system, args.length)
        print(f"Contraseña generada: {password}")
        
    elif args.command == 'add':
        if not args.password:
            args.password = client.generate_password(args.system)
            print(f"Contraseña generada: {args.password}")
        
        cred = client.add_credential(
            args.system, args.name, args.username, 
            args.password, args.url, args.notes
        )
        print(f"Credencial agregada: {cred['name']}")
        
    elif args.command == 'check-rotation':
        needs_rotation = client.check_rotation_needed()
        if needs_rotation:
            print("Credenciales que necesitan rotación:")
            for item in needs_rotation:
                print(f"  - {item['credential']['name']} ({item['system_type']}) - {item['overdue_days']} días atrasada")
        else:
            print("No hay rotaciones pendientes")
            
    elif args.command == 'list':
        for system_type, credentials in client.vault_data.items():
            print(f"\n{system_type}:")
            for cred in credentials:
                print(f"  - {cred['name']}: {cred['username']}")
                
    elif args.command == 'sync':
        client.sync_pending_events()
        print("Sincronización completada")
        
    elif args.command == 'backup':
        backup_file = client.backup_vault()
        if backup_file:
            print(f"Backup creado: {backup_file}")


if __name__ == '__main__':
    main()
```

---

## Fase 3: Actividad Paso a Paso para Estudiantes (60 min)

### Paso 8: Configurar el Sistema Completo

```powershell
# 1. Levantar servidor central
cd C:\sistema-contrasenas\servidor-central
docker compose up -d

# 2. Verificar que funciona
curl https://localhost/health

# 3. Crear usuario de prueba
curl -X POST https://localhost/api/v1/users \
  -H "Content-Type: application/json" \
  -d '{"email":"test@bhu.uy","name":"Usuario de Prueba","department":"TI"}'

# 4. Crear política para Linux servers
curl -X POST https://localhost/api/v1/policies \
  -H "Content-Type: application/json" \
  -d '{
    "system_name": "linux_server",
    "description": "Credenciales de servidores Linux",
    "min_length": 24,
    "custom_regex": "^(?=.*[A-Z])(?=.*[a-z])(?=.*\\d)(?=.*[@$!%*?&#]).{24,}$",
    "rotation_days": 60
  }'
```

### Paso 9: Usar el Cliente Local

```powershell
# 1. Ir al directorio del cliente
cd C:\sistema-contrasenas\cliente-local

# 2. Generar contraseña para Linux server
python vault_client.py generate --system linux_server --length 32

# 3. Agregar credencial
python vault_client.py add \
  --system linux_server \
  --name "Server Principal" \
  --username "root" \
  --url "192.168.1.10"

# 4. Listar credenciales
python vault_client.py list

# 5. Verificar rotación pendiente
python vault_client.py check-rotation

# 6. Sincronizar con servidor
python vault_client.py sync

# 7. Crear backup
python vault_client.py backup
```

### Paso 10: Verificar en el Servidor Central

```powershell
# 1. Ver logs de eventos
curl https://localhost/api/v1/events \
  -H "Authorization: Bearer system_token"

# 2. Ver políticas configuradas
curl https://localhost/api/v1/policies

# 3. Verificar que se enviaron notificaciones
# (Revisar logs del contenedor notificador)
docker logs central-notificador
```

### Paso 11: Probar Rotación

```powershell
# 1. Verificar master password vencida
# (Simular cambiando la fecha en la DB)
docker exec central-db psql -U central -c "
  UPDATE users 
  SET last_master_password_change = '2023-01-01' 
  WHERE email = 'test@bhu.uy'
"

# 2. El sistema debería alertar que necesita cambio
python vault_client.py check-rotation

# 3. Cambiar master password
# (En producción, esto sería un proceso guiado)
```

### Paso 12: Probar Sin Conexión

```powershell
# 1. Detener servidor central
docker compose stop

# 2. Verificar que el cliente local sigue funcionando
python vault_client.py list

# 3. Agregar credencial (se guardará localmente)
python vault_client.py add \
  --system api_keys \
  --name "API Test" \
  --username "test_key"

# 4. Verificar que hay eventos pendientes
type ~\.vault-local\logs\pending_events.json

# 5. Reactivar servidor
docker compose start

# 6. Sincronizar eventos pendientes
python vault_client.py sync
```

---

## Fase 4: Verificación Final (15 min)

### Checklist de Verificación

| # | Verificación | Estado |
|---|-------------|--------|
| 1 | Vault local se descifra con master password | ☐ |
| 2 | 2FA funciona (TOTP) | ☐ |
| 3 | Biometría funciona (Windows Hello) | ☐ |
| 4 | Credenciales se guardan localmente | ☐ |
| 5 | Eventos se registran en servidor central | ☐ |
| 6 | Notificaciones se envían por email | ☐ |
| 7 | Políticas por sistema funcionan | ☐ |
| 8 | Generación automática respeta políticas | ☐ |
| 9 | Rotación de master password funciona | ☐ |
| 10 | Rotación por contraseña funciona | ☐ |
| 11 | Sistema funciona sin servidor central | ☐ |
| 12 | Sincronización después de reconexión funciona | ☐ |
| 13 | Backup y restauración funcionan | ☐ |
| 14 | Admin puede configurar notificaciones | ☐ |
| 15 | Logs de auditoría están completos | ☐ |

---

## Fase 5: Análisis y Mejoras (20 min)

### Preguntas de Reflexión

1. ¿Qué pasaría si el servidor central queda destruido?
2. ¿Cómo se maneja el teletrabajo con vaults locales?
3. ¿Qué pasa si un usuario pierde su dispositivo?
4. ¿Cómo se compara con una solución comercial?
5. ¿Qué mejoras implementarías para un banco?

### Documentación de Entrega

Crear `entrega-actividad/`:
- `01-configuracion/` - Archivos de configuración
- `02-scripts/` - Scripts utilizados
- `03-evidencias/` - Capturas de pantalla
- `04-analisis/` - Análisis de fortalezas/debilidades
- `05-mejoras/` - Propuestas de mejora
- `README.md` - Índice

---

> **Tiempo total: 2.5 horas**
>
> **Nota**: Esta actividad demuestra un sistema completo de gestión de contraseñas híbrido, con énfasis en seguridad, disponibilidad y cumplimiento normativo.
