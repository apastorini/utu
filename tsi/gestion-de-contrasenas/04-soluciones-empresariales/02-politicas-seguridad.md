# 4.2 Políticas de Seguridad para Contraseñas

## Política de Contraseñas BHU

### 1. Alcance

Esta política aplica a todos los empleados, contratistas y usuarios con acceso a sistemas de BHU.

### 2. Definiciones

| Término | Definición |
|---------|------------|
| **Contraseña Maestra** | Clave principal que desbloquea el vault de contraseñas del usuario |
| **Contraseña de Sistema** | Clave para acceder a sistemas, servicios o aplicaciones |
| **API Key** | Token de autenticación para acceso programático |
| **Vault** | Bóveda cifrada donde se almacenan contraseñas y secretos |
| **2FA** | Autenticación de dos factores |
| **MFA** | Autenticación multi-factor |

### 3. Requisitos de Contraseñas

#### 3.1 Contraseña Maestra (Vaultwarden)

| Requisito | Valor | Justificación |
|-----------|-------|---------------|
| Longitud mínima | 20 caracteres | Entropía ≥80 bits |
| Complejidad | Mayúsculas + minúsculas + números + símbolos | Resistencia a diccionario |
| Rotación | No obligatoria (pero recomendada cada 180 días) | Contraseña fuerte no necesita rotación frecuente |
| Reutilización | Prohibida | Evitar credential stuffing |
| Historial | No reutilizar las últimas 10 | Prevenir rotación a contraseñas anteriores |
| Verificación HIBP | Obligatoria al crear/cambiar | Evitar contraseñas comprometidas |

#### 3.2 Contraseñas de Sistema

| Requisito | Valor | Justificación |
|-----------|-------|---------------|
| Longitud mínima | 16 caracteres | Resistencia a fuerza bruta |
| Complejidad | ≥3 tipos de caracteres | Entropía adecuada |
| Rotación | 90 días (sistemas críticos) | Reducir ventana de exposición |
| | 180 días (sistemas estándar) | |
| Reutilización | Prohibida | |
| Historial | No reutilizar las últimas 12 | |

#### 3.3 Contraseñas de Administrador/Privilegiados

| Requisito | Valor | Justificación |
|-----------|-------|---------------|
| Longitud mínima | 24 caracteres | Mayor exposición |
| Complejidad | Todos los tipos de caracteres | |
| Rotación | 60 días | Mayor riesgo |
| Reutilización | Prohibida | |
| 2FA | Obligatorio (hardware key preferida) | Múltiples factores |
| Sesiones | Timeout 15 minutos inactividad | Reducir ventana |
| IP restriction | Solo desde IPs corporativas | Reducir superficie |

#### 3.4 API Keys y Tokens

| Requisito | Valor | Justificación |
|-----------|-------|---------------|
| Almacenamiento | Vaultwarden o HashiCorp Vault | Nunca en código fuente |
| Rotación | 90 días | Reducir exposición |
| Permisos | Mínimos necesarios (least privilege) | Reducir impacto |
| Monitoreo | Logging de uso obligatorio | Detección de anomalías |
| Revocación | Procedimiento documentado | Responder a incidentes |

### 4. Autenticación Multi-Factor (MFA)

#### 4.1 Requisitos por Tipo de Usuario

| Tipo de Usuario | MFA Obligatorio | Métodos Permitidos |
|-----------------|-----------------|-------------------|
| **Usuarios estándar** | Sí | TOTP, WebAuthn, App móvil |
| **Administradores** | Sí | WebAuthn (hardware key) + TOTP |
| **Service accounts** | Sí | API key + IP whitelist |
| **Cuentas de emergencia** | Sí | Hardware key + PIN |

#### 4.2 Métodos de MFA

| Método | Seguridad | Recomendado para |
|--------|-----------|------------------|
| **WebAuthn/FIDO2** | ⭐⭐⭐⭐⭐ | Admin, Usuarios críticos |
| **TOTP** | ⭐⭐⭐⭐ | Todos los usuarios |
| **App móvil (push)** | ⭐⭐⭐ | Usuarios estándar |
| **SMS** | ⭐⭐ | ❌ No recomendado |
| **Email** | ⭐ | ❌ No recomendado |

### 5. Políticas de Compartición

#### 5.1 Compartición Dentro de la Organización

| Escenario | Permitido | Procedimiento |
|-----------|-----------|---------------|
| Misma colección | Sí | Automático |
| Otra colección (mismo depto) | Sí | Aprobación de manager |
| Otro departamento | Sí | Aprobación de admin |
| Externo a BHU | ❌ No | Prohibido |

#### 5.2 Compartición con Externos

```
PROHIBIDO compartir:
❌ Contraseñas de sistemas BHU
❌ API keys de servicios corporativos
❌ Credenciales de administración
❌ Contraseñas de WiFi corporativa
❌ Credenciales de bases de datos

PERMITIDO compartir (con aprobación):
✅ Acceso temporal a herramientas específicas
✅ Credenciales de prueba (no producción)
✅ Información pública (no sensible)
```

### 6. Respaldo y Recuperación

#### 6.1 Backup Obligatorio

| Tipo de Backup | Frecuencia | Retención | Ubicación |
|----------------|------------|-----------|-----------|
| Vault personal (usuario) | Cada 90 días | Indefinido | USB cifrado + Cloud |
| Vaultwarden server | Diario | 30 días | Storage local + off-site |
| Base de datos PostgreSQL | Cada 15 minutos | 7 días | Storage local |
| Configuración | Semanal | 90 días | Git privado |
| Certificados TLS | Al renovar | 2 años | Vault fisico |

#### 6.2 Procedimiento de Emergencia

```
SI UN USUARIO PIERDE MASTER PASSWORD:

1. Verificar identidad (2 factores presenciales)
2. Buscar backup cifrado del usuario
3. Si existe backup:
   a. Admin aprueba importación
   b. Usuario importa con nueva master password
   c. Documentar incidente
4. Si NO existe backup:
   a. Contraseña PERDIDA permanentemente
   b. Reset manual en cada sistema
   c. Documentar como incidente de seguridad
   d. Lección: backup es obligatorio
```

### 7. Auditoría y Monitoreo

#### 7.1 Eventos a Registrar

| Evento | Prioridad | Retención |
|--------|-----------|-----------|
| Login exitoso | Media | 90 días |
| Login fallido | Alta | 1 año |
| Cambio de contraseña | Alta | 1 año |
| Compartición de contraseña | Media | 90 días |
| 2FA habilitado/deshabilitado | Crítica | 2 años |
| Exportación de vault | Crítica | 2 años |
| Nuevo dispositivo | Alta | 1 año |
| Cambio de permisos | Alta | 1 año |
| Eliminación de cuenta | Crítica | 3 años |

#### 7.2 Alertas Automáticas

| Alerta | Umbral | Acción |
|--------|--------|--------|
| 5+ login fallidos en 5 min | Inmediato | Email a admin + usuario |
| Login desde IP desconocida | Inmediato | Email a usuario |
| 2FA deshabilitado | Inmediato | Email a admin + CEO |
| Exportación de vault | Inmediato | Email a admin |
| API key con permisos excesivos | Al crear | Notificación a admin |
| Contraseña en brecha HIBP | Diario | Email a usuario |

### 8. Incidentes de Seguridad

#### 8.1 Clasificación de Incidentes

| Nivel | Descripción | Ejemplo | Respuesta |
|-------|-------------|---------|-----------|
| **P1 - Crítico** | Brecha de datos masiva | Servidor comprometido | Inmediato, 24/7 |
| **P2 - Alto** | Acceso no autorizado | Admin account compromised | < 1 hora |
| **P3 - Medio** | Uso sospechoso | Login desde ubicación inusual | < 4 horas |
| **Bajo** | Evento menor | Contraseña en brecha conocida | < 24 horas |

#### 8.2 Procedimiento de Respuesta

```
1. DETECCIÓN
   ├── Monitoreo automático (SIEM)
   ├── Reporte de usuario
   └── Auditoría periódica

2. CONTENCIÓN
   ├── Revocar sesiones activas
   ├── Bloquear cuenta afectada
   ├── Cambiar credenciales comprometidas
   └── Aislar sistemas afectados

3. ERadicación
   ├── Eliminar acceso del atacante
   ├── Patch de vulnerabilidad explotada
   └── Verificar integridad de sistemas

4. RECUPERACIÓN
   ├── Restaurar desde backup limpio
   ├── Re-habilitar cuentas legítimas
   └── Verificar funcionamiento

5. LECCIONES APRENDIDAS
   ├── Documentar incidente
   ├── Actualizar políticas
   ├── Capacitar usuarios afectados
   └── Mejorar controles
```

### 9. Cumplimiento Normativo

| Norma | Requisito | Implementación |
|-------|-----------|----------------|
| **PCI-DSS 8.3** | Contraseñas ≥12, rotación 90 días | Vaultwarden + política |
| **PCI-DSS 8.4** | MFA para admin | WebAuthn obligatorio |
| **GDPR Art. 32** | Cifrado de datos | E2E + at rest |
| **GDPR Art. 17** | Derecho de eliminación | Export/delete vault |
| **ISO 27001 A.9** | Gestión de accesos | Roles + least privilege |
| **SOC 2 CC6.1** | Controles lógicos | MFA + audit logging |

### 10. Sanciones

| Violación | Sanción |
|-----------|---------|
| Compartir master password |amonestación + capacitación |
| No usar 2FA |amonestación + bloqueo hasta habilitar |
| Guardar contraseñas en texto plano |amonestación + capacitación |
| Compartir credenciales por email |amonestación + revisión de acceso |
| Crear cuenta de servicio no autorizada |suspensión + revisión |
| Compromiso de seguridad por negligencia |suspensión + investigación |

---

> **Actividad**: Adapta esta política al contexto de tu empresa o institución. Identifica 3 requisitos que podrías implementar inmediatamente y justifica por qué son importantes.
