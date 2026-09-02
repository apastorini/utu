# 4.4 Arquitecturas Comparadas: Opciones para BHU

## Visión General

Se presentan **4 opciones arquitectónicas** para el sistema de gestión de contraseñas, cada una con sus ventajas y desventajas. Se incluye una recomendación específica para un escenario bancario.

---

## Opción A: Vaultwarden Extendido (Custom Hooks)

### Descripción

Usar Vaultwarden como backend principal, extendido con hooks personalizados para logging, notificaciones y políticas.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    OPCIÓN A: VAULTWARDEN EXTENDIDO                       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  DISPOSITIVOS DE USUARIOS                                               │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                            │
│  │ Extensión │  │ Desktop  │  │  Móvil   │                            │
│  │ Navegador │  │   App    │  │   App    │                            │
│  └─────┬────┘  └─────┬────┘  └─────┬────┘                            │
│        │             │             │                                    │
│        └─────────────┼─────────────┘                                   │
│                      │                                                  │
│              Sync E2E (Vaultwarden)                                    │
│                      │                                                  │
│  SERVIDOR CENTRAL                                                       │
│  ┌──────────────────┴──────────────────┐                               │
│  │         Vaultwarden Server          │                               │
│  │  ┌───────────────────────────────┐  │                               │
│  │  │  Custom Hooks (Plugin Python) │  │                               │
│  │  │  - Logging de eventos         │  │                               │
│  │  │  - Notificaciones email       │  │                               │
│  │  │  - Validación de políticas    │  │                               │
│  │  └───────────────────────────────┘  │                               │
│  │  ┌──────────────┐  ┌─────────────┐ │                               │
│  │  │  PostgreSQL  │  │   Redis     │ │                               │
│  │  └──────────────┘  └─────────────┘ │                               │
│  └─────────────────────────────────────┘                               │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Ventajas

| # | Ventaja | Descripción |
|---|---------|-------------|
| 1 | **Reutiliza infraestructura** | Vaultwarden ya está probado y funciona |
| 2 | **Costo $0** | Sin licencias, sin desarrollo desde cero |
| 3 | **Clientes existentes** | Extensión, desktop, móvil ya funcionan |
| 4 | **Comunidad activa** | Soporte community, actualizaciones frecuentes |
| 5 | **Despliegue rápido** | Docker compose, listo en horas |

### Desventajas

| # | Desventaja | Descripción |
|---|------------|-------------|
| 1 | **Personalización limitada** | Hooks son básicos, no se puede cambiar el core |
| 2 | **Políticas por sistema** | No soporta regex personalizadas nativamente |
| 3 | **Rotación por contraseña** | No tiene soporte nativo de rotación individual |
| 4 | **Modo offline** | Vaultwarden requiere sync con servidor |
| 5 | **Sin control de notificaciones** | Configuración básica, no granular por admin |
| 6 | **Dependencia del proyecto** | Si Vaultwarden cambia, se rompen los hooks |

### Complejidad de Implementación

| Componente | Esfuerzo | Tiempo |
|------------|----------|--------|
| Instalación base | Bajo | 2 horas |
| Custom hooks | Medio | 1-2 semanas |
| Políticas por sistema | Alto | 2-3 semanas |
| Rotación por contraseña | Alto | 2-3 semanas |
| **Total** | **Medio-Alto** | **4-8 semanas** |

### ¿Cuándo Usar?

- Empresas pequeñas (<50 usuarios)
- Sin requisitos de compliance estrictos
- Presupuesto limitado
- Necesidad rápida de implementación

---

## Opción B: KeePassXC + Servidor API Custom

### Descripción

Usar KeePassXC como vault local, con un servidor API custom que registra eventos y envía notificaciones.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    OPCIÓN B: KEEPASSXC + API CUSTOM                      │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  DISPOSITIVOS DE USUARIOS                                               │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                            │
│  │ KeePassXC│  │ KeePassXC│  │ KeePass  │                            │
│  │ Desktop  │  │ Browser  │  │  Móvil   │                            │
│  │          │  │ Plugin   │  │ (3rd pat)│                            │
│  └─────┬────┘  └─────┬────┘  └─────┬────┘                            │
│        │             │             │                                    │
│        │  vault.kdbx │             │                                    │
│        │  (local)    │             │                                    │
│        │             │             │                                    │
│  SERVIDOR CENTRAL                                                       │
│  ┌──────────────────┴──────────────────┐                               │
│  │      API Server Custom (Python)     │                               │
│  │  ┌───────────────────────────────┐  │                               │
│  │  │  - Recepción de eventos       │  │                               │
│  │  │  - Logging a PostgreSQL       │  │                               │
│  │  │  - Notificaciones email       │  │                               │
│  │  │  - Políticas configurables    │  │                               │
│  │  └───────────────────────────────┘  │                               │
│  │  ┌──────────────┐  ┌─────────────┐ │                               │
│  │  │  PostgreSQL  │  │  SMTP       │ │                               │
│  │  └──────────────┘  └─────────────┘ │                               │
│  └─────────────────────────────────────┘                               │
│                                                                         │
│  PLUGIN KEEPASSXC (Custom)                                             │
│  ┌─────────────────────────────────────┐                               │
│  │  - Hook de eventos (create/update)  │                               │
│  │  - Envío a API server               │                               │
│  │  - Verificación de políticas        │                               │
│  │  - Generación según regex           │                               │
│  └─────────────────────────────────────┘                               │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Ventajas

| # | Ventaja | Descripción |
|---|---------|-------------|
| 1 | **100% local por diseño** | vault.kdbx nunca sale del dispositivo |
| 2 | **KeePassXC es maduro** | 10+ años de desarrollo, muy estable |
| 3 | **Personalización total** | API server se puede diseñar a medida |
| 4 | **Políticas completas** | Regex, rotación, todo configurable |
| 5 | **Sin dependencia de proveedor** | Todo open source y local |
| 6 | **Modo offline nativo** | KeePassXC funciona sin servidor |

### Desventajas

| # | Desventaja | Descripción |
|---|------------|-------------|
| 1 | **Sin clientes móviles nativos** | KeePass para móvil es limitado |
| 2 | **Plugin custom requerido** | Hay que desarrollar el plugin de eventos |
| 3 | **Sin autofill automático** | Requiere copy-paste manual |
| 4 | **Experiencia de usuario** | Menos pulida que Vaultwarden |
| 5 | **Compartición limitada** | KeePass no tiene colecciones compartidas |

### Complejidad de Implementación

| Componente | Esfuerzo | Tiempo |
|------------|----------|--------|
| KeePassXC instalación | Bajo | 1 hora |
| API Server custom | Medio | 2-3 semanas |
| Plugin KeePassXC | Alto | 3-4 semanas |
| Integración completa | Medio | 1-2 semanas |
| **Total** | **Alto** | **6-10 semanas** |

### ¿Cuándo Usar?

- Equipos técnicos (desarrolladores, sysadmins)
- Requisito estricto de vault local
- Sin necesidad de móvil
- Personalización total requerida

---

## Opción C: Custom Solution (Recomendada para Banco)

### Descripción

Aplicación nativa (Electron/native) con vault local cifrado + servidor central de logs/notificaciones. Totalmente personalizable.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    OPCIÓN C: CUSTOM SOLUTION                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  DISPOSITIVOS DE USUARIOS                                               │
│  ┌─────────────────────────────────────────────────────────────┐       │
│  │  App Nativa (Electron / .NET / Rust)                        │       │
│  │  ┌───────────────────────────────────────────────────────┐  │       │
│  │  │  Vault Local Cifrado (AES-256-GCM)                   │  │       │
│  │  │  - Contraseñas del usuario                           │  │       │
│  │  │  - Políticas de rotación por contraseña              │  │       │
│  │  │  - Generación según regex del sistema                │  │       │
│  │  │  - Log local de eventos                              │  │       │
│  │  └───────────────────────────────────────────────────────┘  │       │
│  │  ┌───────────────────────────────────────────────────────┐  │       │
│  │  │  Autenticación Multi-Factor                          │  │       │
│  │  │  - Master Password + 2FA (TOTP/WebAuthn) + Biometría │  │       │
│  │  │  - Timeout configurable                              │  │       │
│  │  │  - Bloqueo automático                                │  │       │
│  │  └───────────────────────────────────────────────────────┘  │       │
│  │  ┌───────────────────────────────────────────────────────┐  │       │
│  │  │  Extensión Navegador (no guardan credenciales)       │  │       │
│  │  │  - Autofill desde vault local                        │  │       │
│  │  │  - Nunca almacenan en el navegador                   │  │       │
│  │  └───────────────────────────────────────────────────────┘  │       │
│  └─────────────────────────────────────────────────────────────┘       │
│                         │                                               │
│                    Eventos (TCP/HTTP)                                   │
│                         │                                               │
│  SERVIDOR CENTRAL                                                       │
│  ┌─────────────────────┴────────────────────┐                         │
│  │  API Gateway + Event Processor           │                         │
│  │  ┌─────────────────────────────────────┐ │                         │
│  │  │  - Recepción y logging de eventos   │ │                         │
│  │  │  - Validación de políticas          │ │                         │
│  │  │  - Distribución de notificaciones   │ │                         │
│  │  │  - Control de rotación              │ │                         │
│  │  │  - Dashboard de administración      │ │                         │
│  │  └─────────────────────────────────────┘ │                         │
│  │  ┌──────────────┐  ┌───────────────┐    │                         │
│  │  │  PostgreSQL  │  │  Notificador  │    │                         │
│  │  │  (Primary +  │  │  (Email +     │    │                         │
│  │  │   Replica)   │  │   Webhook)    │    │                         │
│  │  └──────────────┘  └───────────────┘    │                         │
│  └───────────────────────────────────────────┘                         │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Ventajas

| # | Ventaja | Descripción |
|---|---------|-------------|
| 1 | **Control total** | Cada aspecto es personalizable |
| 2 | **Vault 100% local** | Nunca sale del dispositivo |
| 3 | **Políticas completas** | Regex, rotación individual, todo configurable |
| 4 | **Autenticación completa** | Master + 2FA + Biometría |
| 5 | **Notificaciones granulares** | Admin controla cada evento |
| 6 | **Modo offline** | Funciona sin servidor central |
| 7 | **Cumpliance completo** | Logs, auditoría, rotación |
| 8 | **Browser plugins seguros** | No guardan credenciales en navegador |
| 9 | **Sin internet requerido** | Todo funciona en red interna |
| 10 | **Teletrabajo soportado** | Vault local + sync por VPN |

### Desventajas

| # | Desventaja | Descripción |
|---|------------|-------------|
| 1 | **Desarrollo desde cero** | Requiere equipo de desarrollo |
| 2 | **Costo inicial alto** | 3-6 meses de desarrollo |
| 3 | **Mantenimiento propio** | Actualizaciones, bugs, soporte |
| 4 | **Testing extensivo** | Seguridad requiere auditing |
| 5 | **Documentación** | Requiere docs completos |

### Complejidad de Implementación

| Componente | Esfuerzo | Tiempo |
|------------|----------|--------|
| App local (vault + auth) | Muy alto | 4-6 semanas |
| Extensión navegador | Alto | 2-3 semanas |
| API server + logs | Alto | 3-4 semanas |
| Notificador | Medio | 1-2 semanas |
| Dashboard admin | Alto | 2-3 semanas |
| Testing y auditoría | Muy alto | 4-6 semanas |
| **Total** | **Muy alto** | **16-24 semanas** |

### ¿Cuándo Usar?

- Bancos e instituciones financieras
- Cumpliance PCI-DSS/SOX requerido
- Sin acceso a internet
- Requisitos de alta disponibilidad
- Teletrabajo contemplado

---

## Opción D: Solución Comercial Adaptada

### Descripción

Usar 1Password Business o Bitwarden Enterprise con personalizaciones y auto-hosting.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    OPCIÓN D: SOLUCIÓN COMERCIAL                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  DISPOSITIVOS DE USUARIOS                                               │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                            │
│  │ Extensión │  │ Desktop  │  │  Móvil   │                            │
│  │ 1Password │  │ 1Password│  │ 1Password│                            │
│  └─────┬────┘  └─────┬────┘  └─────┬────┘                            │
│        └─────────────┼─────────────┘                                   │
│                      │                                                  │
│  SERVIDOR CENTRAL                                                       │
│  ┌──────────────────┴──────────────────┐                               │
│  │    1Password Enterprise Server      │                               │
│  │  (Self-hosted o Cloud)              │                               │
│  │  - Todos los features incluidos     │                               │
│  │  - Soporte 24/7                     │                               │
│  │  - Actualizaciones automáticas      │                               │
│  └─────────────────────────────────────┘                               │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Ventajas

| # | Ventaja | Descripción |
|---|---------|-------------|
| 1 | **Producto probado** | Miles de empresas lo usan |
| 2 | **Soporte 24/7** | Ayuda inmediata cuando hay problemas |
| 3 | **Actualizaciones** | Security patches automáticos |
| 4 | **Experiencia de usuario** | La mejor UX del mercado |
| 5 | **Cumpliance** | SOC 2, GDPR, etc. |

### Desventajas

| # | Desventaja | Descripción |
|---|------------|-------------|
| 1 | **Costo alto** | $6-8/user/mes = $2,160-3,456/año para 30 usuarios |
| 2 | **Sin personalización** | No se puede cambiar el core |
| 3 | **Sin vault local** | Requiere sync con servidor |
| 4 | **Dependencia del proveedor** | Si cambian precios o política |
| 5 | **Sin control total** | Datos en sus servidores (si cloud) |

### Costo para 30 Usuarios

| Concepto | 1Password Business | Bitwarden Enterprise |
|----------|--------------------|--------------------|
| Costo mensual | $237 | $180 |
| Costo anual | $2,844 | $2,160 |
| 3 años | $8,532 | $6,480 |

### ¿Cuándo Usar?

- Sin restricción de presupuesto
- Sin requisitos de vault local
- Empresa no bancaria
- Sin necesidad de personalización

---

## Tabla Comparativa Final

| Criterio | Opción A | Opción B | Opción C | Opción D |
|----------|----------|----------|----------|----------|
| **Vault local** | ❌ | ✅ | ✅ | ❌ |
| **Políticas por sistema** | ⚠️ Limitado | ✅ | ✅ | ⚠️ Limitado |
| **Rotación por contraseña** | ❌ | ✅ | ✅ | ⚠️ Limitado |
| **Generación por regex** | ❌ | ✅ | ✅ | ⚠️ Limitado |
| **Notificaciones granulares** | ⚠️ Básico | ✅ | ✅ | ✅ |
| **2FA + Biometría** | ✅ | ⚠️ Limitado | ✅ | ✅ |
| **Modo offline** | ⚠️ Limitado | ✅ | ✅ | ⚠️ Limitado |
| **Sin internet** | ❌ | ✅ | ✅ | ❌ |
| **Teletrabajo** | ⚠️ VPN | ✅ Local | ✅ Local | ⚠️ VPN |
| **Costo** | $0 | $0 | $0 + dev | $2,160+/año |
| **Tiempo impl.** | 4-8 sem | 6-10 sem | 16-24 sem | 1-2 sem |
| **Cumpliance** | ⚠️ | ⚠️ | ✅ | ✅ |
| **Soporte** | Community | Ninguno | Interno | 24/7 |

---

## 🏦 Recomendación para Banco: Opción C

### Justificación

| Requisito del Banco | Opción C lo cumple |
|---------------------|-------------------|
| **Sin internet** | ✅ Todo funciona en red interna |
| **Vault local** | ✅ Contraseñas nunca salen del dispositivo |
| **Cumpliance PCI-DSS** | ✅ Logs completos, rotación configurable |
| **Alta disponibilidad** | ✅ PostgreSQL cluster + app stateless |
| **Políticas por sistema** | ✅ Regex configurables por admin |
| **Rotación individual** | ✅ Cada contraseña tiene su ciclo |
| **Notificaciones** | ✅ Admin controla qué se notifica |
| **2FA + Biometría** | ✅ WebAuthn + TOTP + Windows Hello |
| **Teletrabajo** | ✅ Vault local + sync por VPN |
| **Sin credenciales en navegador** | ✅ Plugin propio, no guarda nada |

### Plan de Implementación para Banco

```
FASE 1: Fundamentos (4 semanas)
├── Diseño de arquitectura
├── Vault local cifrado
├── Autenticación multi-factor
└── API server básico

FASE 2: Funcionalidad (4 semanas)
├── Políticas por sistema (regex)
├── Rotación por contraseña
├── Generación automática
└── Notificaciones email

FASE 3: Seguridad (4 semanas)
├── Hardening de servidor
├── Auditoría de seguridad
├── Penetration testing
└── Cumpliance check

FASE 4: Despliegue (4 semanas)
├── Piloto con 10 usuarios
├── Rollout gradual
├── Capacitación
└── Soporte post-lanzamiento

TOTAL: 16 semanas (4 meses)
```

### Alternativa Rápida (Si el tiempo apremia)

Si se necesita algo inmediato mientras se desarrolla la Opción C:

**Fase puente: Opción A (Vaultwarden Extendido)**
- Implementar en 1-2 semanas
- Cubre necesidades básicas
- Migrar a Opción C cuando esté lista

---

> **Actividad**: Evalúa las 4 opciones según los criterios de tu empresa/institución. Justifica cuál elegirías y por qué.
