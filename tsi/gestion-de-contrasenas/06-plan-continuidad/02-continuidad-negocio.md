# 6.2 Plan de Continuidad de Negocio (BCP)

## Definición

El **Plan de Continuidad de Negocio (BCP)** es un conjunto de procedimientos que garantizan que los servicios críticos de la organización (incluyendo la gestión de contraseñas) continúen operando durante y después de un desastre o interrupción.

## Alcance del BCP para Gestión de Contraseñas

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    BCP - GESTIÓN DE CONTRASEÑAS                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  SERVICIOS CRÍTICOS A PROTEGER:                                        │
│  ├── Acceso a contraseñas de todos los empleados                       │
│  ├── Compartición de credenciales entre departamentos                  │
│  ├── Autenticación de usuarios en sistemas críticos                    │
│  ├── API keys de servicios esenciales                                  │
│  └── Credenciales de administración de infraestructura                 │
│                                                                         │
│  ESCENARIOS A CONSIDERAR:                                              │
│  ├── 1. Servidor central caído (Vaultwarden)                          │
│  ├── 2. Pérdida total del servidor                                    │
│  ├── 3. Corrupción de base de datos                                   │
│  ├── 4. Ataque cibernético (ransomware, DDoS)                         │
│  ├── 5. Desastre natural (incendio, inundación)                       │
│  ├── 6. Pérdida de dispositivos de usuarios                           │
│  └── 7. Olvido de master password a nivel masivo                      │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Objetivos del BCP

### Métricas Clave

| Métrica | Definición | Objetivo BHU |
|---------|------------|--------------|
| **RTO** (Recovery Time Objective) | Tiempo máximo de inactividad aceptable | 4 horas |
| **RPO** (Recovery Point Objective) | Máxima pérdida de datos aceptable | 15 minutos |
| **MTPD** (Maximum Tolerable Period of Disruption) | Tiempo máximo antes de impacto grave | 24 horas |
| **MBCO** (Minimum Business Continuity Objective) | Nivel mínimo de servicio requerido | 80% de usuarios |

### Niveles de Servicio

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    NIVELES DE SERVICIO                                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  NIVEL 1: OPERACIÓN NORMAL (100%)                                     │
│  ├── Todos los servicios disponibles                                  │
│  ├── Sync automática funcionando                                      │
│  ├── Notificaciones activas                                           │
│  ├── Backup automático ejecutándose                                   │
│  └── Monitoreo completo                                               │
│                                                                         │
│  NIVEL 2: DEGRADADO (80%)                                             │
│  ├── Vault local funciona (sin sync)                                  │
│  ├── Compartición no disponible                                       │
│  ├── Notificaciones retrasadas                                       │
│  ├── Backup manual requerido                                          │
│  └── Monitoreo básico                                                 │
│                                                                         │
│  NIVEL 3: MÍNIMO (50%)                                                │
│  ├── Solo vault local (sin servidor)                                  │
│  ├── Sin sincronización                                               │
│  ├── Sin notificaciones                                               │
│  ├── Backup manual urgente                                            │
│  └── Sin monitoreo                                                    │
│                                                                         │
│  NIVEL 4: EMERGENCIA (20%)                                            │
│  ├── Usuarios acceden a vaults locales individuales                   │
│  ├── Compartición manual por otros medios                             │
│  ├── Sin backup automático                                            │
│  └── Recuperación manual                                              │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Estrategias de Continuidad

### Estrategia 1: Vault Local como Primer Nivel

```
┌─────────────────────────────────────────────────────────────────────────┐
│  ESTRATEGIA: OFFLINE-FIRST                                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  VENTAJA: El vault local funciona SIEMPRE, sin importar el servidor   │
│                                                                         │
│  IMPLEMENTACIÓN:                                                        │
│  ├── Cada dispositivo tiene vault local cifrado                       │
│  ├── Sync es opcional, no requerida                                   │
│  ├── Contraseñas siempre accesibles                                   │
│  └── Sin punto único de fallo                                         │
│                                                                         │
│  FLUJO DE EMERGENCIA:                                                  │
│  1. Servidor central cae                                              │
│  2. Usuarios siguen usando vaults locales                             │
│  3. Sync se reanuda cuando servidor vuelve                           │
│  4. Conflictos se resuelven (última escritura gana)                  │
│                                                                         │
│  LIMITACIÓN:                                                           │
│  ├── No hay compartición durante la emergencia                        │
│  ├── No hay notificaciones                                            │
│  └── No hay backup automático                                         │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Estrategia 2: Backup Distribuido

```
┌─────────────────────────────────────────────────────────────────────────┐
│  ESTRATEGIA: BACKUP 3-2-1                                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  REGLA 3-2-1:                                                          │
│  ├── 3 copias de los datos                                            │
│  ├── 2 medios diferentes                                              │
│  └── 1 copia off-site                                                 │
│                                                                         │
│  DISTRIBUCIÓN PARA BHU:                                                │
│                                                                         │
│  Copia 1: Servidor local (Primary)                                    │
│  ├── PostgreSQL en el servidor Vaultwarden                            │
│  ├── Almacenamiento: disco local del servidor                         │
│  └── Actualización: en tiempo real                                     │
│                                                                         │
│  Copia 2: Servidor de backup (Local)                                  │
│  ├── Réplica de PostgreSQL                                            │
│  ├── Almacenamiento: NAS/SAN de la empresa                           │
│  └── Actualización: cada 15 minutos                                   │
│                                                                         │
│  Copia 3: Backup off-site                                             │
│  ├── Exportación cifrada de vaults                                    │
│  ├── Almacenamiento: cloud (S3, Backblaze) o USB en otra ubicación   │
│  └── Actualización: diaria                                            │
│                                                                         │
│  Copia 4 (Emergencia): USB cifrado en caja fuerte                    │
│  ├── Vault exportado y cifrado                                        │
│  ├── Actualización: mensual                                           │
│  └── Acceso: solo con 2 autorizaciones                               │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Estrategia 3: High Availability (HA)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  ESTRATEGIA: HIGH AVAILABILITY                                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ARQUITECTURA HA:                                                       │
│                                                                         │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐               │
│  │ Vaultwarden │    │ Vaultwarden │    │ Vaultwarden │               │
│  │    (1)      │    │    (2)      │    │    (3)      │               │
│  └──────┬──────┘    └──────┬──────┘    └──────┬──────┘               │
│         │                  │                  │                        │
│         └──────────────────┼──────────────────┘                       │
│                            │                                          │
│                     ┌──────┴──────┐                                   │
│                     │   NGINX     │                                   │
│                     │ Load Balance│                                   │
│                     └──────┬──────┘                                   │
│                            │                                          │
│         ┌──────────────────┼──────────────────┐                       │
│         │                  │                  │                        │
│  ┌──────┴──────┐    ┌──────┴──────┐    ┌──────┴──────┐               │
│  │ PostgreSQL  │    │ PostgreSQL  │    │   Redis     │               │
│  │  Primary    │───►│  Replica    │    │   Cache     │               │
│  └─────────────┘    └─────────────┘    └─────────────┘               │
│                                                                         │
│  BENEFICIOS:                                                            │
│  ├── Si un Vaultwarden falla, los otros toman el cargo               │
│  ├── PostgreSQL con réplica: failover automático                     │
│  ├── Redis: cache de sesiones compartido                             │
│  └── Sin punto único de fallo                                        │
│                                                                         │
│  IMPLEMENTACIÓN:                                                        │
│  ├── Docker Swarm o Kubernetes                                        │
│  ├── PostgreSQL con Patroni (auto-failover)                          │
│  ├── NGINX con health checks                                          │
│  └── Storage compartido (NFS/S3)                                      │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Procedimientos de Emergencia

### Escenario 1: Servidor Caído

```
┌─────────────────────────────────────────────────────────────────────────┐
│  PROCEDIMIENTO: SERVIDOR CAÍDO                                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  DETECCIÓN (Tiempo: 0-5 min):                                         │
│  ├── Health check falla                                               │
│  ├── Usuarios reportan que no pueden sincronizar                      │
│  ├── Monitoreo genera alerta                                          │
│  └── Alerta: "Vaultwarden no responde"                               │
│                                                                         │
│  CONTENCIÓN (Tiempo: 5-30 min):                                       │
│  ├── Verificar si es caída total o parcial                           │
│  ├── Comunicar a usuarios: "Servidor temporalmente inaccesible"      │
│  ├── Indicar: "Sus vaults locales siguen funcionando"                │
│  ├── Solicitar: "No cierren la extensión del navegador"              │
│  └── Escalar a IT si no se resuelve en 15 min                       │
│                                                                         │
│  RECUPERACIÓN (Tiempo: 30 min - 4 horas):                             │
│  ├── Diagnosticar causa de la caída                                  │
│  ├── Si es hardware: activar réplica/failover                        │
│  ├── Si es software: reiniciar/actualizar                            │
│  ├── Si es red: verificar conectividad                               │
│  ├── Restaurar desde backup si es necesario                          │
│  └── Verificar funcionamiento completo                               │
│                                                                         │
│  POST-INCIDENTE:                                                       │
│  ├── Documentar causa raíz                                           │
│  ├── Actualizar procedimientos si es necesario                        │
│  ├── Comunicar resolución a usuarios                                 │
│  └── Programar revisión de preventivos                               │
│                                                                         │
│  IMPACTO ESPERADO:                                                     │
│  ├── Vault local: ✅ Funciona (sin sync)                             │
│  ├── Compartición: ❌ No disponible                                  │
│  ├── Notificaciones: ❌ No disponibles                               │
│  └── Usuarios afectados: Todos (pero pueden trabajar)               │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Escenario 2: Pérdida Total del Servidor

```
┌─────────────────────────────────────────────────────────────────────────┐
│  PROCEDIMIENTO: PÉRDIDA TOTAL DEL SERVIDOR                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  DETECCIÓN (Tiempo: 0-5 min):                                         │
│  ├── Servidor no responde                                             │
│  ├── No hay posibilidad de recuperación inmediata                     │
│  └── Alerta: "Servidor destruido/inaccesible"                        │
│                                                                         │
│  CONTENCIÓN (Tiempo: 5-30 min):                                       │
│  ├── Comunicar a usuarios: "Servidor temporalmente fuera de servicio" │
│  ├── Indicar: "Sus vaults locales siguen funcionando"                │
│  ├── Activar plan de recuperación                                    │
│  └── Contactar proveedor de infraestructura                          │
│                                                                         │
│  RECUPERACIÓN (Tiempo: 2-24 horas):                                   │
│  ├── Provisionar nuevo servidor                                       │
│  ├── Restaurar desde backup off-site                                 │
│  │   ├── 1. Descargar backup cifrado                                │
│  │   ├── 2. Descifrar con clave de emergencia                       │
│  │   ├── 3. Restaurar PostgreSQL                                     │
│  │   ├── 4. Restaurar configuración                                  │
│  │   └── 5. Verificar integridad                                    │
│  ├── Configurar nuevo servidor                                       │
│  ├── Verificar que usuarios pueden sincronizar                       │
│  └── Comunicar resolución                                            │
│                                                                         │
│  VERIFICACIÓN POST-RECUPERACIÓN:                                       │
│  ├── Todos los usuarios pueden hacer login                            │
│  ├── Sincronización funciona correctamente                           │
│  ├── Notificaciones reanudadas                                        │
│  ├── Backups automáticos reanudados                                  │
│  └── Auditoría de integridad                                         │
│                                                                         │
│  IMPACTO ESPERADO:                                                     │
│  ├── Vault local: ✅ Funciona (sin sync)                             │
│  ├── Compartición: ❌ No disponible hasta recuperación               │
│  ├── Notificaciones: ❌ No disponibles hasta recuperación            │
│  └── Datos: ✅ Recuperables desde backup                             │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Escenario 3: Ataque Ransomware

```
┌─────────────────────────────────────────────────────────────────────────┐
│  PROCEDIMIENTO: ATAQUE RANSOMWARE                                       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  DETECCIÓN:                                                             │
│  ├── Archivos cifrados en servidor                                    │
│  ├── Mensaje de ransom aparece                                        │
│  ├── Vaultwarden no funciona                                          │
│  └── Alerta de seguridad                                              │
│                                                                         │
│  CONTENCIÓN INMEDIATA:                                                 │
│  ├── ❌ NO PAGAR EL RESCATE                                          │
│  ├── Desconectar servidor de la red                                   │
│  ├── Preservar evidencia forense                                     │
│  ├── Notificar a autoridades                                         │
│  └── Activar plan de incidente                                       │
│                                                                         │
│  RECUPERACIÓN:                                                         │
│  ├── Restaurar desde backup ANTERIOR al ataque                       │
│  │   (verificar que el backup no está comprometido)                   │
│  ├── Provisionar nuevo servidor limpio                                │
│  ├── Restaurar vaults desde backup                                   │
│  ├── Cambiar todas las credenciales comprometidas                    │
│  └── Verificar integridad de sistemas                                │
│                                                                         │
│  VERIFICACIÓN:                                                         │
│  ├── Los vaults locales de usuarios NO están comprometidos           │
│  │   (están cifrados E2E)                                             │
│  ├── Solo el servidor fue afectado                                    │
│  ├── Usuarios pueden seguir usando vaults locales                    │
│  └── Sincronización se reanuda después de recuperación               │
│                                                                         │
│  LECCIONES:                                                             │
│  ├── Implementar backup offline (no accesible por ransomware)        │
│  ├── Segmentación de red                                              │
│  ├── Monitoreo de anomalías                                          │
│  └── Capacitación de usuarios                                        │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Matriz de Riesgos y Mitigaciones

| Riesgo | Probabilidad | Impacto | Mitigación | Plan de Respuesta |
|--------|-------------|---------|------------|-------------------|
| Servidor caído | Media | Alto | HA + backup | Failover + restauración |
| Pérdida total servidor | Baja | Crítico | Backup off-site | Recuperación desde backup |
| Corrupción DB | Media | Alto | Réplica + backup | Restaurar réplica |
| Ransomware | Baja | Crítico | Backup offline | Restaurar + aislar |
| Desastre natural | Baja | Crítico | Backup geográfico | DRP completo |
| Pérdida dispositivo | Media | Medio | Vault local + backup | Revocar + restaurar |
| Master pass olvidada | Media | Alto | Backup cifrado | Recuperación de emergencia |
| Compromiso admin | Baja | Crítico | 2FA + monitoreo | Revocar + investigar |

## Comunicación de Emergencia

### Plantilla de Comunicación

```
ASUNTO: [URGENTE] Interrupción del servicio de contraseñas - BHU

FECHA: [Fecha]
HORA: [Hora]
IMPACTO: [Descripción del impacto]
USUARIOS AFECTADOS: [Todos/Departamento específico]

ESTADO ACTUAL:
├── Servidor central: [Caído/Funcionando parcialmente]
├── Vaults locales: [Funcionando/No disponibles]
├── Sincronización: [No disponible/Funcionando]
└── Compartición: [No disponible/Funcionando]

ACCIONES EN CURSO:
1. [Acción 1]
2. [Acción 2]
3. [Acción 3]

INSTRUCCIONES PARA USUARIOS:
├── [Instrucción 1]
├── [Instrucción 2]
└── [Instrucción 3]

PRÓXIMA ACTUALIZACIÓN: [Fecha/Hora]
CONTACTO: [Nombre] - [Email] - [Teléfono]

---
Este mensaje es parte del Plan de Continuidad de Negocio de BHU.
```

---

> **Actividad**: Crea un BCP para una empresa de tu elección. Define: RTO, RPO, escenarios a cubrir, estrategias de mitigación, y procedimientos de recuperación para al menos 3 escenarios.
