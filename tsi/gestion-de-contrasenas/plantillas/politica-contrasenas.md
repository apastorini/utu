# Plantilla: Política de Contraseñas para Empresa

## [NOMBRE DE LA EMPRESA] - Política de Contraseñas

**Versión**: 1.0
**Fecha de aprobación**: [FECHA]
**Próxima revisión**: [FECHA + 12 meses]
**Responsable**: [Nombre del CTO/Security Officer]

---

### 1. Objetivo

Establecer los requisitos y procedimientos para la gestión segura de contraseñas en [NOMBRE DE LA EMPRESA], protegiendo los activos de información de la organización y sus clientes.

### 2. Alcance

Esta política aplica a:
- Todos los empleados permanentes y temporales
- Contratistas y consultores externos
- Proveedores con acceso a sistemas de la empresa
- Cualquier persona con credenciales de acceso a sistemas de [NOMBRE DE LA EMPRESA]

### 3. Definiciones

| Término | Definición |
|---------|------------|
| **Contraseña Maestra** | Clave principal que desbloquea el gestor de contraseñas del usuario |
| **Contraseña de Sistema** | Clave para acceder a sistemas, servicios o aplicaciones |
| **API Key** | Token de autenticación para acceso programático |
| **Vault** | Bóveda cifrada donde se almacenan contraseñas y secretos |
| **2FA** | Autenticación de dos factores |
| **MFA** | Autenticación multi-factor |
| **Gestor** | Aplicación Vaultwarden para gestión de contraseñas |

### 4. Requisitos de Contraseñas

#### 4.1 Contraseña Maestra (Vaultwarden)

| Requisito | Valor |
|-----------|-------|
| Longitud mínima | 20 caracteres |
| Complejidad | ≥3 tipos de caracteres (mayúsculas, minúsculas, números, símbolos) |
| Reutilización | Prohibida (no reutilizar las últimas 10) |
| Verificación HIBP | Obligatoria al crear/cambiar |
| Rotación | Recomendada cada 180 días |

#### 4.2 Contraseñas de Sistema

| Requisito | Valor |
|-----------|-------|
| Longitud mínima | 16 caracteres |
| Complejidad | ≥3 tipos de caracteres |
| Rotación (sistemas críticos) | 90 días |
| Rotación (sistemas estándar) | 180 días |
| Reutilización | Prohibida (no reutilizar las últimas 12) |

#### 4.3 Contraseñas de Administrador

| Requisito | Valor |
|-----------|-------|
| Longitud mínima | 24 caracteres |
| Complejidad | Todos los tipos de caracteres |
| Rotación | 60 días |
| 2FA | Obligatorio (hardware key preferida) |
| Timeout de sesión | 15 minutos |

### 5. Autenticación Multi-Factor (MFA)

| Tipo de Usuario | MFA Obligatorio | Métodos Permitidos |
|-----------------|-----------------|-------------------|
| Usuarios estándar | Sí | TOTP, WebAuthn |
| Administradores | Sí | WebAuthn + TOTP |
| Service accounts | Sí | API key + IP whitelist |

### 6. Compartición de Contraseñas

| Escenario | Permitido |
|-----------|-----------|
| Misma colección | Sí |
| Otra colección (mismo depto) | Sí (aprobación manager) |
| Otro departamento | Sí (aprobación admin) |
| Externo a la empresa | **Prohibido** |

### 7. Respaldo y Recuperación

| Elemento | Frecuencia | Responsable |
|----------|------------|-------------|
| Vault personal (usuario) | Cada 90 días | Cada usuario |
| Vaultwarden server | Diario | IT |
| PostgreSQL | Cada 15 minutos | IT (automático) |
| Configuración | Semanal | IT |

### 8. Incidentes de Seguridad

| Nivel | Descripción | Tiempo de Respuesta |
|-------|-------------|---------------------|
| P1 - Crítico | Brecha de datos masiva | Inmediato, 24/7 |
| P2 - Alto | Acceso no autorizado | < 1 hora |
| P3 - Medio | Uso sospechoso | < 4 horas |
| Bajo | Evento menor | < 24 horas |

### 9. Sanciones

| Violación | Sanción |
|-----------|---------|
| Compartir master password | Amonestación + capacitación |
| No usar 2FA | Bloqueo hasta habilitar |
| Guardar contraseñas en texto plano | Amonestación + revisión |
| Compartir credenciales por email | Amonestación + revisión de acceso |

### 10. Cumplimiento Normativo

| Norma | Requisito | Implementación |
|-------|-----------|----------------|
| PCI-DSS 8.3 | Contraseñas ≥12, rotación 90 días | Gestor + política |
| PCI-DSS 8.4 | MFA para admin | WebAuthn obligatorio |
| GDPR Art. 32 | Cifrado de datos | E2E + at rest |

### 11. Aprobación

| Rol | Nombre | Firma | Fecha |
|-----|--------|-------|-------|
| CEO | | | |
| CTO | | | |
| Security Officer | | | |

---

> **Nota**: Esta política debe ser revisada anualmente o cuando haya cambios significativos en la infraestructura o regulaciones aplicables.
