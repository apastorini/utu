# 5.5 Procedimientos Offline: Acceso Sin Servidor y Teletrabajo

## Visión General

El sistema debe funcionar **sin conexión al servidor central** en escenarios de:
- **Teletrabajo** (sin VPN o VPN caída)
- **Emergencias** (caída del servidor central)
- **Red interna** (acceso a vaults locales sin sync)
- **Desastres** (servidor destruido, reconstrucción desde backups)

---

## Arquitectura Offline-First

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    ARQUITECTURA OFFLINE-FIRST                            │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    SERVIDOR CENTRAL                              │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │   │
│  │  │  API Server  │  │  PostgreSQL  │  │  Notificador │         │   │
│  │  │  (Flask)     │  │  (Primary +  │  │  (Email +    │         │   │
│  │  │              │  │   Replica)   │  │   Webhook)   │         │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘         │   │
│  │                                                                  │   │
│  │  Almacena: Eventos, logs, políticas, configuración              │   │
│  │  NO almacena: Contraseñas (nunca salen del cliente)             │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│                           │                                             │
│              ┌────────────┼────────────┐                               │
│              │            │            │                                │
│         CONECTADO    SEMI-ONLINE   OFFLINE                             │
│         (Sync OK)    (Cola local)  (Sin sync)                          │
│              │            │            │                                │
│              ▼            ▼            ▼                                │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    DISPOSITIVO DE USUARIO                        │   │
│  │                                                                  │   │
│  │  ┌──────────────────────────────────────────────────────────┐   │   │
│  │  │  Vault Local Cifrado (AES-256-GCM)                       │   │   │
│  │  │  - Todas las contraseñas del usuario                     │   │   │
│  │  │  - Metadatos: sistema, rotación, fecha vencimiento       │   │   │
│  │  │  - Políticas cacheadas del servidor                      │   │   │
│  │  │  - Log local de eventos pendientes de sync               │   │   │
│  │  └──────────────────────────────────────────────────────────┘   │   │
│  │                                                                  │   │
│  │  ┌──────────────────────────────────────────────────────────┐   │   │
│  │  │  Cola de Eventos (SQLite local)                          │   │   │
│  │  │  - Eventos generados offline                             │   │   │
│  │  │  - Timestamp + tipo + datos (sin contraseñas)            │   │   │
│  │  │  - Sincronizados cuando hay conexión                     │   │   │
│  │  └──────────────────────────────────────────────────────────┘   │   │
│  │                                                                  │   │
│  │  ┌──────────────────────────────────────────────────────────┐   │   │
│  │  │  Cache de Políticas (TTL: 7 días)                        │   │   │
│  │  │  - Políticas de rotación por sistema                     │   │   │
│  │  │  - Regex de validación                                   │   │   │
│  │  │  - Configuración de notificaciones                       │   │   │
│  │  └──────────────────────────────────────────────────────────┘   │   │
│  │                                                                  │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Estados de Conexión

### 1. CONECTADO (Online)

```
Estado: ✅ Conexión al servidor central activa
Comportamiento:
  - Sync automático cada 5 minutos
  - Notificaciones en tiempo real
  - Políticas actualizadas
  - Eventos enviados inmediatamente
  - Validación de contraseñas contra servidor
```

### 2. SEMI-ONLINE (Cola local)

```
Estado: ⚠️ Conexión intermitente o lenta
Comportamiento:
  - Vault local funciona normalmente
  - Eventos se guardan en cola local
  - Sync cuando la conexión se restablece
  - Notificaciones pendientes se envían en lote
  - Políticas usan cache (última actualización conocida)
```

### 3. OFFLINE (Sin conexión)

```
Estado: 🔴 Sin conexión al servidor
Comportamiento:
  - Vault local funciona completamente
  - Generación y validación de contraseñas
  - Rotación individual funciona
  - Eventos se guardan en cola local
  - Notificaciones pendientes se acumulan
  - Políticas usan cache (puede estar desactualizada)
  - Advertencia: "Modo offline - sync pendiente"
```

---

## Procedimiento: Teletrabajo

### Escenario A: VPN + Vault Local (Recomendado)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    TELETRABAJO: VPN + VAULT LOCAL                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  EMPLEADO EN CASA                                                      │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  1. Conectar VPN (WireGuard/OpenVPN)                           │   │
│  │     → Accede a red interna de la empresa                        │   │
│  │                                                                  │   │
│  │  2. Abrir App de Gestión de Contraseñas                        │   │
│  │     → Vault local se carga en memoria                           │   │
│  │     → Sync con servidor central (si hay conexión)               │   │
│  │                                                                  │   │
│  │  3. Usar contraseñas normalmente                               │   │
│  │     → Copiar al portapapeles (se limpia en 30 seg)             │   │
│  │     → Autofill en navegador (plugin)                            │   │
│  │                                                                  │   │
│  │  4. Generar/rotar contraseñas según necesidad                   │   │
│  │     → Valida contra políticas cacheadas                         │   │
│  │     → Notifica al servidor (si hay conexión VPN)                │   │
│  │                                                                  │   │
│  │  5. Desconectar VPN al finalizar jornada                       │   │
│  │     → Vault local sigue accesible (solo lectura)               │   │
│  │     → No se pueden generar/rotar (sin sync)                    │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Escenario B: Sin VPN (Offline Total)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    TELETRABAJO: SIN VPN (OFFLINE)                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  EMPLEADO EN CASA (sin VPN)                                            │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  1. Abrir App de Gestión de Contraseñas                        │   │
│  │     → Vault local se carga en memoria                           │   │
│  │     → Modo offline activado automáticamente                     │   │
│  │     → Aviso: "Sin conexión - sync pendiente"                    │   │
│  │                                                                  │   │
│  │  2. Usar contraseñas existentes normalmente                     │   │
│  │     → Copiar al portapapeles (se limpia en 30 seg)             │   │
│  │     → Autofill en navegador (plugin)                            │   │
│  │                                                                  │   │
│  │  3. Generar contraseñas (si es necesario)                       │   │
│  │     → Usa políticas cacheadas (puede estar desactualizada)     │   │
│  │     → Evento se guarda en cola local                            │   │
│  │     → Se sync cuando haya conexión                              │   │
│  │                                                                  │   │
│  │  4. Rotar contraseñas (si es necesario)                         │   │
│  │     → Actualiza vault local                                     │   │
│  │     → Evento se guarda en cola local                            │   │
│  │     → Se sync cuando haya conexión                              │   │
│  │                                                                  │   │
│  │  5. Al volver a la oficina o conectar VPN                      │   │
│  │     → Sync automático de eventos pendientes                     │   │
│  │     → Actualización de políticas desde servidor                  │   │
│  │     → Envío de notificaciones pendientes                        │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Procedimiento Paso a Paso: Teletrabajo con VPN

```
PASO 1: PREPARACIÓN (Antes de salir de la oficina)
─────────────────────────────────────────────────
□ Verificar que el vault local esté actualizado
  → Abrir app → Sync manual → Confirmar "Última sincronización: hace X minutos"
□ Verificar que la VPN funcione
  → Conectar VPN de prueba → Acceder a recurso interno
□ Verificar que las extensiones de navegador estén instaladas
  → Chrome: Extensiones → Gestor de Contraseñas → Habilitada
□ Copiar procedimiento de emergencia a dispositivo offline
  → Guardar en USB: procedimiento-offline.pdf
□ Verificar que la política de master password no vence pronto
  → Si vence en <7 días, rotar antes de salir

PASO 2: EN CASA (Con VPN)
─────────────────────────
□ Conectar VPN
  → Abrir cliente VPN → Conectar → Verificar IP interna
□ Abrir app de gestión de contraseñas
  → Vault local se carga automáticamente
  → Verificar: "Conectado al servidor" (verde)
□ Usar contraseñas normalmente
  → Copiar/pegar o autofill
□ Si necesitas generar nueva contraseña
  → Seleccionar sistema → Generar → Valida contra política
  → Sync inmediato con servidor
□ Al finalizar jornada
  → Sync manual → Desconectar VPN

PASO 3: SIN VPN (Emergencia)
────────────────────────────
□ Abrir app de gestión de contraseñas
  → Modo offline activado automáticamente
  → Aviso: "⚠️ Modo offline - sync pendiente"
□ Usar contraseñas existentes
  → Copiar/pegar o autofill
  → Funciona normalmente
□ Si necesitas generar/rotar
  → Usa políticas cacheadas
  → Evento en cola local
□ Al volver a tener conexión
  → Sync automático
  → Verificar que eventos se enviaron

PASO 4: AL VOLVER A LA OFICINA
──────────────────────────────
□ Conectar a red interna (WiFi o cable)
□ Abrir app de gestión de contraseñas
  → Sync automático de eventos pendientes
  → Actualización de políticas
  → Verificar: "Última sincronización: hace X minutos"
□ Revisar notificaciones pendientes
  → Algunas podrían haber llegado con retraso
□ Verificar que no hay alertas de seguridad
  → Revisar dashboard de administración
```

---

## Procedimiento: Emergencia - Servidor Central Caído

### Escenario: El servidor central no responde

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    EMERGENCIA: SERVIDOR CENTRAL CAÍDO                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  SÍNTOMAS:                                                             │
│  - App muestra "Error de conexión"                                     │
│  - Sync falla con timeout                                              │
│  - Notificaciones no se envían                                         │
│  - Dashboard no carga                                                  │
│                                                                         │
│  IMPACTO:                                                              │
│  - Vault local: ✅ Funciona normalmente                                │
│  - Generación:  ✅ Funciona (políticas cacheadas)                      │
│  - Rotación:    ✅ Funciona (eventos en cola)                          │
│  - Logs:        ⚠️ Pendientes de sync                                  │
│  - Notif email: ❌ No se envían (servidor SMTP caído)                  │
│  - Auditoría:   ⚠️ Logs locales se acumulan                            │
│                                                                         │
│  PROCEDIMIENTO:                                                        │
│  1. Verificar que es problema del servidor (no de tu red)             │
│  2. Notificar a TI/seguridad                                          │
│  3. Continuar trabajando con vault local                               │
│  4. NO generar contraseñas nuevas (políticas pueden estar viejas)     │
│  5. Usar contraseñas existentes solamente                             │
│  6. Cuando servidor vuelva, sync automático                           │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Checklist de Emergencia

```
╔══════════════════════════════════════════════════════════════╗
║  CHECKLIST: SERVIDOR CENTRAL CAÍDO                           ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  FASE 1: DIAGNÓSTICO (0-15 min)                             ║
║  □ Ping al servidor central                                 ║
║  □ Verificar DNS                                            ║
║  □ Verificar firewall                                       ║
║  □ Consultar a otros usuarios (¿les funciona?)              ║
║  □ Verificar status del servidor (si tienes acceso)         ║
║                                                              ║
║  FASE 2: CONTENCIÓN (15-30 min)                             ║
║  □ Notificar a administrador de sistemas                    ║
║  □ Notificar a jefe de seguridad                            ║
║  □ Documentar hora de inicio del incidente                  ║
║  □ Activar modo offline en todas las apps                    ║
║                                                              ║
║  FASE 3: CONTINUIDAD (30 min - restoration)                 ║
║  □ Usar vaults locales (solo lectura)                       ║
║  □ NO generar contraseñas nuevas (políticas desactualizadas)║
║  □ NO rotar contraseñas (eventos no se sync)                ║
║  □ Usar contraseñas existentes solamente                    ║
║  □ Documentar cada uso de contraseña en papel               ║
║                                                              ║
║  FASE 4: RESTAURACIÓN                                       ║
║  □ Verificar que servidor está arriba                       ║
║  □ Sync manual de eventos pendientes                        ║
║  □ Verificar que políticas se actualizaron                  ║
║  □ Revisar logs de seguridad                                ║
║  □ Generar reporte del incidente                            ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

---

## Procedimiento: Emergencia - Contraseña Olvidada (Master)

### Escenario: El usuario olvidó su master password

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    EMERGENCIA: MASTER PASSWORD OLVIDADA                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  IMPACTO:                                                              │
│  - Vault local: ❌ INACCESIBLE                                         │
│  - Todas las contraseñas: ❌ PERDIDAS (localmente)                     │
│  - Servidor central: ⚠️ Logs disponibles, pero no vault                │
│                                                                         │
│  OPCIONES:                                                             │
│                                                                         │
│  OPCIÓN 1: Restaurar desde backup                                     │
│  ├── Requisito: Tener backup reciente del vault                        │
│  ├── Proceso: Restaurar vault → Crear nuevo master password            │
│  └── Riesgo: Pierde cambios desde el último backup                     │
│                                                                         │
│  OPCIÓN 2: Usar cuenta de recuperación (break-glass)                  │
│  ├── Requisito: Tener break-glass account configurada                  │
│  ├── Proceso: Acceder con break-glass → Resetear master password       │
│  └── Riesgo: Requiere aprobación de 2 admins                           │
│                                                                         │
│  OPCIÓN 3: Contactar a administrador                                   │
│  ├── Requisito: Admin tiene acceso a break-glass                       │
│  ├── Proceso: Admin verifica identidad → Resetea cuenta                │
│  └── Riesgo: Tiempo de espera, puede ser horas                         │
│                                                                         │
│  OPCIÓN 4: Recuperación desde envelope físico                          │
│  ├── Requisito: Tener envelope en caja de seguridad                    │
│  ├── Proceso: Abrir envelope → Usar master password de emergencia      │
│  └── Riesgo: Solo funciona si el envelope está actualizado             │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Procedimiento Paso a Paso

```
PASO 1: INTENTAR RECORDAR (0-5 min)
──────────────────────────────────
□ Revisar gestor de contraseñas del navegador
  → ¿Guardaste el master password ahí?
□ Revisar notas físicas
  → ¿Lo escribiste en algún lado?
□ Revisar gestor de contraseñas del teléfono
  → ¿Lo sincronizaste con el móvil?
□ Intentar variaciones comunes
  → ¿Lo cambiaste recientemente?

PASO 2: RESTAURAR DESDE BACKUP (5-30 min)
──────────────────────────────────────────
□ Localizar backup más reciente
  → USB: Ver fecha del archivo .kdbx o .encrypted
  → Servidor: Ver logs de backup
□ Verificar que el backup no esté corrupto
  → Intentar abrir con master password anterior
□ Restaurar vault
  → Copiar backup a ubicación original
  → Abrir con master password del backup
□ Crear nuevo master password
  → Cumplir política de complejidad
  → Rotar master password inmediatamente
□ Verificar que todas las contraseñas estén presentes
  → Contar entradas vs. número esperado
□ Registrar evento en servidor central
  → "Master password reset desde backup"

PASO 3: USAR BREAK-GLASS (Si no hay backup)
─────────────────────────────────────────────
□ Contactar a administrador de sistemas
  → Línea de emergencia: XXX-XXXX
  → Verificar identidad (3 preguntas de seguridad)
□ Admin accede a break-glass account
  → Usa credenciales de emergencia del envelope
  → Verifica que no hay actividad sospechosa
□ Admin resetea la cuenta del usuario
  → Desactiva master password actual
  → Genera临时 master password
  → Notifica al usuario por canal seguro
□ Usuario accede y crea nuevo master password
  → Cumplir política de complejidad
  → Verificar que vault esté intacto
□ Admin registra evento
  → "Master password reset via break-glass"
  → "Usuario: XXX, Admin: YYY, Hora: ZZZ"

PASO 4: RECUPERACIÓN DESDE ENVELOPE (Último recurso)
─────────────────────────────────────────────────────
□ Localizar envelope de emergencia
  → Caja de seguridad en oficina principal
  → Solo personal autorizado tiene acceso
□ Abrir envelope con 2 testigos
  → Testigo 1: Gerente de área
  → Testigo 2: Jefe de seguridad
□ Usar master password de emergencia
  → Ingresar en app de gestión de contraseñas
  → Acceder a vault
□ Crear nuevo master password
  → Cumplir política de complejidad
  → Cambiar master password de emergencia
□ Registrar evento
  → "Master password reset desde envelope"
  → "Testigos: XXX, YYY"
□ Actualizar envelope con nuevo master password
  → Generar nuevo master password de emergencia
  → Re-sellar envelope
```

---

## Procedimiento: Emergencia - Acceso desde Dispositivo Nueva

### Escenario: El usuario necesita acceder desde un dispositivo nuevo

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    EMERGENCIA: DISPOSITIVO NUEVO                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ESCENARIO:                                                            │
│  - Usuario tiene laptop nueva                                          │
│  - Laptop vieja se dañó/perdió                                        │
│  - Necesita acceso urgente a contraseñas                               │
│                                                                         │
│  REQUISITOS:                                                           │
│  - Master password del usuario                                         │
│  - Dispositivo de 2FA (o backup codes)                                 │
│  - Conexión a red interna (o VPN)                                      │
│  - Backup del vault (si vault local no existe en dispositivo nuevo)    │
│                                                                         │
│  PROCEDIMIENTO:                                                        │
│  1. Instalar app de gestión de contraseñas                            │
│  2. Restaurar vault desde backup (si aplica)                           │
│  3. Ingresar master password                                           │
│  4. Completar 2FA (TOTP o WebAuthn)                                    │
│  5. Verificar biometría (si aplica)                                    │
│  6. Sync con servidor central                                          │
│  7. Verificar que todas las contraseñas están presentes                │
│  8. Registrar evento: "Acceso desde dispositivo nuevo"                 │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Cola de Eventos Offline

### Estructura del Evento

```json
{
  "event_id": "uuid-v4",
  "timestamp": "2026-08-26T14:30:00Z",
  "type": "password_generated",
  "data": {
    "system_id": "linux-ssh",
    "entry_id": "entry-uuid",
    "created_at": "2026-08-26",
    "expires_at": "2026-11-24",
    "rotation_days": 90
  },
  "user_id": "user-uuid",
  "device_id": "device-uuid",
  "synced": false,
  "synced_at": null,
  "retry_count": 0
}
```

### Sincronización de Cola

```
USUARIO reconecta a la red
                    │
                    ▼
┌──────────────────────────────────────────────┐
│  1. Detectar conexión al servidor            │
│     (heartbeat cada 30 segundos)             │
└──────────────────────────────────────────────┘
                    │
                    ▼
┌──────────────────────────────────────────────┐
│  2. Leer eventos pendientes de SQLite        │
│     (synced = false)                         │
└──────────────────────────────────────────────┘
                    │
                    ▼
┌──────────────────────────────────────────────┐
│  3. Enviar eventos al servidor               │
│     (POST /api/v1/events/batch)              │
│     - Lote de hasta 100 eventos              │
│     - Reintentar si falla (max 3 veces)      │
└──────────────────────────────────────────────┘
                    │
                    ▼
┌──────────────────────────────────────────────┐
│  4. Marcar eventos como sincronizados        │
│     (synced = true, synced_at = now)         │
└──────────────────────────────────────────────┘
                    │
                    ▼
┌──────────────────────────────────────────────┐
│  5. Actualizar políticas desde servidor      │
│     (GET /api/v1/policies)                   │
│     - Actualizar cache local                 │
│     - Aplicar nuevas políticas               │
└──────────────────────────────────────────────┘
                    │
                    ▼
┌──────────────────────────────────────────────┐
│  6. Enviar notificaciones pendientes         │
│     (el servidor las procesa)                │
└──────────────────────────────────────────────┘
```

---

## Cache de Políticas

### Estructura del Cache

```json
{
  "policies": {
    "linux-ssh": {
      "policy": { ... },
      "cached_at": "2026-08-26T10:00:00Z",
      "ttl_hours": 168
    },
    "windows-ad": {
      "policy": { ... },
      "cached_at": "2026-08-26T10:00:00Z",
      "ttl_hours": 168
    }
  },
  "master_password_policy": {
    "policy": { ... },
    "cached_at": "2026-08-26T10:00:00Z",
    "ttl_hours": 168
  },
  "last_sync": "2026-08-26T10:00:00Z",
  "sync_status": "ok"
}
```

### Validación del Cache

```python
def get_policy(system_id: str) -> dict:
    """Obtiene política, usando cache si offline."""
    cache = load_policy_cache()

    if system_id in cache['policies']:
        cached = cache['policies'][system_id]
        cached_at = datetime.fromisoformat(cached['cached_at'])
        ttl = timedelta(hours=cached['ttl_hours'])

        if datetime.now() - cached_at < ttl:
            # Cache válido
            return cached['policy']
        else:
            # Cache expirado, intentar sync
            try:
                policy = fetch_policy_from_server(system_id)
                update_cache(system_id, policy)
                return policy
            except ConnectionError:
                # Offline, usar cache expirado con advertencia
                log_warning(f"Usando política cacheada expirada: {system_id}")
                return cached['policy']

    # No hay cache, intentar sync
    try:
        policy = fetch_policy_from_server(system_id)
        update_cache(system_id, policy)
        return policy
    except ConnectionError:
        # Offline, política por defecto
        return get_default_policy()
```

---

## Procedimiento: Sync Después de Reconexión

```
╔══════════════════════════════════════════════════════════════╗
║  PROCEDIMIENTO: SYNC DESPUÉS DE RECONEXIÓN                   ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  PRE-REQUISITOS:                                            ║
║  - Conexión a red interna estable                           ║
║  - Servidor central operativo                               ║
║  - Vault local accesible                                    ║
║                                                              ║
║  PASOS:                                                     ║
║                                                              ║
║  1. Verificar conexión                                      ║
║     □ Ping al servidor: ping central.bhu.local              ║
║     □ Verificar VPN (si teletrabajo): status vpn            ║
║     □ Si no hay conexión, esperar y reintentar              ║
║                                                              ║
║  2. Abrir app de gestión de contraseñas                     ║
║     □ Detecta conexión automáticamente                      ║
║     □ Inicia sync de eventos pendientes                      ║
║     □ Muestra progreso: "Sincronizando X eventos..."        ║
║                                                              ║
║  3. Verificar sync completado                               ║
║     □ "Última sincronización: hace X minutos"               ║
║     □ "Eventos pendientes: 0"                               ║
║     □ "Políticas actualizadas: Sí"                          ║
║                                                              ║
║  4. Verificar notificaciones                                ║
║     □ Revisar bandeja de email                              ║
║     □ Algunas notificaciones pueden llegar con retraso      ║
║     □ Si faltan, contactar a TI                             ║
║                                                              ║
║  5. Verificar integridad                                    ║
║     □ Contar entradas en vault                              ║
║     □ Comparar con número esperado                          ║
║     □ Si hay diferencias, contactar a TI                    ║
║                                                              ║
║  6. Documentar                                              ║
║     □ Registrar hora de sync en bitácora                    ║
║     □ Anotar si hubo problemas                              ║
║     □ Reportar a supervisor si aplica                        ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

---

## Procedimiento: Trabajo en Sitio del Cliente

### Escenario: Empleado visita sucursal o cliente

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    TRABAJO EN SITIO DEL CLIENTE                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  PREPARACIÓN (Antes de salir):                                         │
│  □ Sync manual del vault local                                         │
│  □ Verificar que todas las contraseñas necesarias están en el vault    │
│  □ Copiar contraseñas críticas a vault offline (si aplica)            │
│  □ Llevar dispositivo con 2FA (celular con authenticator)             │
│  □ Llevar envelope de emergencia (si es visita crítica)               │
│  □ Verificar que la política de rotación no vence durante la visita   │
│                                                                         │
│  EN EL SITIO:                                                          │
│  □ Usar vault local (sin conexión a servidor)                          │
│  □ Generar contraseñas según políticas cacheadas                       │
│  □ Documentar cada contraseña generada en papel seguro                 │
│  □ NO dejar contraseñas en papel en el sitio del cliente             │
│  □ Al salir, destruir papel con contraseñas                            │
│                                                                         │
│  AL VOLVER:                                                            │
│  □ Sync manual del vault                                               │
│  □ Verificar que eventos se sincronizaron                              │
│  □ Revisar notificaciones pendientes                                   │
│  □ Reportar cualquier incidencia                                       │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Procedimiento: Dispositivo Robado o Perdido

### Escenario: El laptop del usuario fue robado

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    EMERGENCIA: DISPOSITIVO ROBADO                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  IMPACTO INMEDIATO:                                                    │
│  - Vault local: ⚠️ Cifrado pero accesible si conocen master password  │
│  - Contraseñas: ⚠️ Potencialmente comprometidas                        │
│  - 2FA: ✅ Seguro (en otro dispositivo)                                │
│  - Master password: ⚠️ Comprometido si estaba escrito                  │
│                                                                         │
│  PROCEDIMIENTO INMEDIATO (0-30 min):                                   │
│  1. Reportar a TI/seguridad inmediatamente                             │
│  2. Cambiar master password desde otro dispositivo                      │
│  3. Revocar tokens 2FA y regenerar                                     │
│  4. Revocar todas las contraseñas del vault robado                     │
│  5. Activar wipe remoto (si soportado)                                 │
│  6. Cambiar contraseñas de sistemas críticos                           │
│  7. Documentar incidente                                               │
│                                                                         │
│  PROCEDIMIENTO POSTERIOR (1-7 días):                                   │
│  1. Restaurar vault desde backup                                       │
│  2. Generar nuevas contraseñas para todos los sistemas                 │
│  3. Auditar logs para detectar acceso no autorizado                    │
│  4. Actualizar políticas de seguridad                                  │
│  5. Revisar y actualizar envelope de emergencia                        │
│  6. Capacitar al usuario sobre seguridad de dispositivos               │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Checklist de Seguridad Post-Robo

```
╔══════════════════════════════════════════════════════════════╗
║  CHECKLIST: DISPOSITIVO ROBADO                               ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  INMEDIATO (0-30 min):                                      ║
║  □ Reportar a TI (ticket #XXXX)                             ║
║  □ Cambiar master password desde otro dispositivo            ║
║  □ Revocar tokens 2FA                                       ║
║  □ Activar wipe remoto                                      ║
║  □ Cambiar contraseña de email corporativo                  ║
║                                                              ║
║  PRIMERAS HORAS (30 min - 4 horas):                         ║
║  □ Cambiar contraseñas de sistemas críticos:                ║
║    □ Core banking                                          ║
║    □ VPN                                                    ║
║    □ SSH servers                                            ║
║    □ Cloud (AWS/Azure/GCP)                                  ║
║    □ Email                                                  ║
║  □ Revocar certificados digitales                          ║
║  □ Notificar a supervisor                                  ║
║                                                              ║
║  PRIMER DÍA (4-24 horas):                                   ║
║  □ Cambiar contraseñas de todos los sistemas                ║
║  □ Auditar logs de acceso                                  ║
║  □ Verificar que no hay accesos sospechosos                ║
║  □ Restaurar vault desde backup                            ║
║  □ Documentar incidente completo                           ║
║                                                              ║
║  SIGUIENTES 7 DÍAS:                                         ║
║  □ Monitorear actividad inusual                            ║
║  □ Revisar y actualizar envelope de emergencia             ║
║  □ Capacitación sobre seguridad de dispositivos            ║
║  □ Actualizar políticas si es necesario                    ║
║  □ Revisar si se necesita reporte formal                   ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

---

## Script de Sync Automático

### PowerShell: Sync de Eventos Pendientes

```powershell
# sync-events.ps1
# Ejecutar al reconectar a la red

$ServerUrl = "https://central.bhu.local:5000"
$VaultPath = "$env:USERPROFILE\.vaultwarden\events.db"
$LogFile = "$env:USERPROFILE\.vaultwarden\sync.log"

function Write-Log {
    param([string]$Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "$timestamp - $Message" | Out-File -FilePath $LogFile -Append
}

function Test-ServerConnection {
    try {
        $response = Invoke-WebRequest -Uri "$ServerUrl/health" -TimeoutSec 5
        return $response.StatusCode -eq 200
    } catch {
        return $false
    }
}

function Get-PendingEvents {
    # Leer eventos pendientes de SQLite
    # (Implementación específica del vault)
    $events = @()
    # TODO: Leer de SQLite
    return $events
}

function Sync-Events {
    param([array]$Events)

    $batch = $Events | Select-Object -First 100
    $json = $batch | ConvertTo-Json

    try {
        $response = Invoke-WebRequest `
            -Uri "$ServerUrl/api/v1/events/batch" `
            -Method POST `
            -Body $json `
            -ContentType "application/json" `
            -TimeoutSec 30

        if ($response.StatusCode -eq 200) {
            Write-Log "Sync exitoso: $($batch.Count) eventos enviados"
            return $true
        }
    } catch {
        Write-Log "Error en sync: $($_.Exception.Message)"
        return $false
    }
}

# Main
Write-Log "Iniciando sync de eventos..."

if (-not (Test-ServerConnection)) {
    Write-Log "Servidor no disponible. Sync pospuesto."
    exit 0
}

$pending = Get-PendingEvents
Write-Log "Eventos pendientes: $($pending.Count)"

if ($pending.Count -gt 0) {
    $success = Sync-Events -Events $pending
    if ($success) {
        Write-Log "Sync completado exitosamente"
    } else {
        Write-Log "Sync falló. Reintentar más tarde."
    }
} else {
    Write-Log "No hay eventos pendientes"
}

# Actualizar políticas
try {
    $policies = Invoke-WebRequest -Uri "$ServerUrl/api/v1/policies" -TimeoutSec 10
    $policies.Content | Out-File "$env:USERPROFILE\.vaultwarden\policies-cache.json"
    Write-Log "Políticas actualizadas"
} catch {
    Write-Log "Error actualizando políticas: $($_.Exception.Message)"
}

Write-Log "Sync completado"
```

---

## Resumen de Procedimientos Offline

| Escenario | Vault Local | Generación | Rotación | Logs | Notificaciones |
|-----------|------------|------------|----------|------|----------------|
| **Online** | ✅ | ✅ | ✅ | ✅ Real-time | ✅ Email |
| **Offline** | ✅ | ✅ (cache) | ✅ (local) | ✅ Cola | ⚠️ Pendiente |
| **Servidor caído** | ✅ | ✅ (cache) | ✅ (local) | ✅ Cola | ❌ No envía |
| **Sin VPN** | ✅ | ✅ (cache) | ✅ (local) | ✅ Cola | ⚠️ Pendiente |
| **Dispositivo nuevo** | ✅ (restore) | ✅ | ✅ | ✅ | ✅ |
| **Dispositivo robado** | ⚠️ Cifrado | ⚠️ Revocar | ⚠️ Revocar | ✅ | ⚠️ Urgente |

---

> **Actividad**: Simula un escenario de teletrabajo sin VPN. Genera contraseñas offline, documenta los eventos en una cola local, y luego sincroniza cuando "vuelva la conexión". Evalúa qué funciona y qué se pierde.
