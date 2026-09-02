# 6.4 Gestión de Emergencias: Master Password Olvidada y Break-Glass

## Escenarios de Emergencia

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    ESCENARIOS DE EMERGENCIA                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ESCENARIO 1: Usuario olvidó master password (Común)                   │
│  ├── Frecuencia: Media (1-2 veces por trimestre)                       │
│  ├── Impacto: Individual                                               │
│  ├── Recuperación: Backup cifrado del usuario                         │
│  └── Tiempo: 30 min - 2 horas                                         │
│                                                                         │
│  ESCENARIO 2: Admin olvidó master password (Serio)                     │
│  ├── Frecuencia: Baja (1 vez al año)                                   │
│  ├── Impacto: Organización                                            │
│  ├── Recuperación: Break-glass account                                │
│  └── Tiempo: 1-4 horas                                                │
│                                                                         │
│  ESCENARIO 3: Todos los usuarios pierden acceso (Crítico)             │
│  ├── Frecuencia: Muy baja (desastre)                                  │
│  ├── Impacto: Total                                                    │
│  ├── Recuperación: Restauración completa desde backup                 │
│  └── Tiempo: 4-24 horas                                               │
│                                                                         │
│  ESCENARIO 4: Compromiso de cuenta admin (Crítico)                    │
│  ├── Frecuencia: Baja                                                 │
│  ├── Impacto: Seguridad de todos los usuarios                         │
│  ├── Recuperación: Revocación + rotación masiva                       │
│  └── Tiempo: 1-8 horas                                                │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Escenario 1: Usuario Olvidó Master Password

### Procedimiento

```
┌─────────────────────────────────────────────────────────────────────────┐
│  PROCEDIMIENTO: MASTER PASSWORD OLVIDADA - USUARIO                      │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  PASO 1: VERIFICACIÓN DE IDENTIDAD (5 min)                            │
│  ├── El usuario contacta a IT Helpdesk                               │
│  ├── IT verifica identidad con 2 factores:                           │
│  │   ├── Pregunta de seguridad personal                              │
│  │   ├── Código enviado al email corporativo                         │
│  │   └── Llamada telefónica a número registrado                      │
│  ├── Documentar solicitud en ticket                                  │
│  └── Asignar número de ticket                                        │
│                                                                         │
│  PASO 2: BUSCAR BACKUP DEL USUARIO (10 min)                          │
│  ├── Verificar si el usuario tiene backup cifrado                    │
│  ├── Ubicaciones a revisar:                                          │
│  │   ├── USB personal del usuario (si tiene)                         │
│  │   ├── Cloud personal cifrado (Google Drive, Dropbox)              │
│  │   ├── Backup institucional en TI                                  │
│  │   └── Caja fuerte (si es usuario ejecutivo)                       │
│  ├── Si NO tiene backup: proceder al Paso 4                         │
│  └── Si SÍ tiene backup: proceder al Paso 3                         │
│                                                                         │
│  PASO 3: RECUPERACIÓN DESDE BACKUP (30 min)                          │
│  ├── Solicitar al usuario que traiga su backup cifrado               │
│  ├── Verificar que el backup es válido (integridad)                  │
│  ├── Descifrar backup con contraseña del backup                      │
│  │   (Esta contraseña es DIFERENTE a la master password)             │
│  ├── Crear nueva master password para el usuario                     │
│  │   (Veterana: ≥20 caracteres, generar aleatoria)                   │
│  ├── Importar backup con nueva master password                       │
│  ├── Verificar que todas las contraseñas están presentes             │
│  ├── Habilitar 2FA nuevamente                                        │
│  ├── Documentar en ticket                                            │
│  └── Capacitar usuario: importancia del backup                       │
│                                                                         │
│  PASO 4: SIN BACKUP - RECUPERACIÓN MANUAL (2-8 horas)                │
│  ├── ⚠️ Las contraseñas del vault del usuario ESTÁN PERDIDAS        │
│  ├── Crear nueva master password para el usuario                     │
│  ├── El usuario debe recrear manualmente todas sus contraseñas       │
│  ├── Ayudar al usuario a identificar sistemas importantes            │
│  │   ├── Email corporativo                                           │
│  │   ├── Redes sociales corporativas                                 │
│  │   ├── Herramientas de trabajo                                     │
│  │   ├── Servicios de terceros                                       │
│  │   └── APIs y tokens                                               │
│  ├── Para cada sistema:                                              │
│  │   ├── Usar función "Olvidé mi contraseña" del sistema            │
│  │   ├── O contactar administrador del sistema                       │
│  │   └── Generar nueva contraseña con el gestor                     │
│  ├── Documentar en ticket                                            │
│  └── Lección: recordar importancia del backup                        │
│                                                                         │
│  COSTO ESTIMADO:                                                       │
│  ├── Con backup: 30 min de IT + 15 min del usuario                  │
│  ├── Sin backup: 4-8 horas de IT + tiempo del usuario               │
│  └── Prevención: Capacitar sobre backup obligatorio                  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Formulario de Solicitud de Recuperación

```markdown
# SOLICITUD DE RECUPERACIÓN DE MASTER PASSWORD
# Ticket #: [NÚMERO]
# Fecha: [FECHA]

## Datos del Solicitante
- Nombre completo: _______________
- Departamento: _______________
- Email corporativo: _______________
- Teléfono: _______________
- Supervisor: _______________

## Verificación de Identidad
- [ ] Pregunta de seguridad respondida correctamente
- [ ] Código de verificación enviado a email corporativo
- [ ] Código de verificación verificado
- [ ] Llamada telefónica de verificación completada

## Tipo de Solicitud
- [ ] Olvido de master password
- [ ] Cuenta bloqueada por intentos fallidos
- [ ] Sospecha de compromiso de cuenta
- [ ] Otro: _______________

## Información de Backup
- [ ] Usuario tiene backup personal
  - Ubicación: _______________
  - ¿Puede traerlo? Sí / No
- [ ] Backup institucional disponible
  - Última fecha de backup: _______________
- [ ] No tiene backup (proceder a recuperación manual)

## Aprobación
- Solicitante: _______________ Fecha: _______________
- IT Helpdesk: _______________ Fecha: _______________
- Supervisor: _______________ Fecha: _______________
```

## Escenario 2: Break-Glass Account

### Concepto

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    BREAK-GLASS ACCOUNT                                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ¿QUÉ ES?                                                             │
│  Una cuenta de emergencia que permite recuperar acceso cuando          │
│  todas las cuentas normales están comprometidas o inaccesibles.       │
│                                                                         │
│  ¿CUÁNDO SE USA?                                                      │
│  ├── Admin principal no puede acceder (master pass perdida)           │
│  ├── Cuenta admin comprometida por atacante                           │
│  ├── Desastre que destruye servidor                                   │
│  └── Emergencia de seguridad que requiere acceso inmediato           │
│                                                                         │
│  ¿QUIÉN CONTROLA?                                                     │
│  ├── 2 personas designadas (CTO + CEO)                               │
│  ├── Ambas deben estar presentes (protocolo de 2 personas)           │
│  ├── Documento en sobre sellado en caja fuerte                      │
│  └── Copia digital cifrada en USB en otra ubicación                 │
│                                                                         │
│  RESTRICCIONES:                                                        │
│  ├── Cuenta limitada a emergencias específicas                       │
│  ├── Logging completo de cada uso                                    │
│  ├── Notificación inmediata a todo el equipo directivo              │
│  ├── Requiere justificación escrita                                  │
│  └── Revisión post-incidente obligatoria (48 horas)                 │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Contenido del Sobre Break-Glass

```
╔══════════════════════════════════════════════════════════════════════════╗
║              CREDENCIALES DE EMERGENCIA - BHU VAULTWARDEN                ║
║              ⚠️ SOLO PARA USO EN EMERGENCIAS DOCUMENTADAS ⚠️            ║
╠══════════════════════════════════════════════════════════════════════════╣
║                                                                          ║
║  CUENTA DE EMERGENCIA:                                                   ║
║  Email: breakglass-emergency@bhu.uy                                     ║
║  Master Password: Xk9#mP$vL2nQ!wR7tY4jB8uH3sF6gD5                     ║
║                                                                          ║
║  ADMIN TOKEN:                                                            ║
║  eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.Emergency.Token.Here            ║
║                                                                          ║
║  PANEL ADMIN:                                                            ║
║  URL: https://vaultwarden.bhu.uy/admin                                 ║
║  Token: [Admin Token anterior]                                          ║
║                                                                          ║
║  ─────────────────────────────────────────────────────────────────────   ║
║                                                                          ║
║  PROCEDIMIENTO DE USO:                                                   ║
║                                                                          ║
║  1. Verificar que es una emergencia válida:                             ║
║     ├── Admin principal no puede acceder                                ║
║     ├── Cuenta admin comprometida                                      ║
║     └── Emergencia de seguridad documentada                            ║
║                                                                          ║
║  2. Verificar presencia de 2 personas autorizadas:                     ║
║     ├── CEO: [Nombre] - Tel: [Número]                                  ║
║     └── CTO: [Nombre] - Tel: [Número]                                  ║
║                                                                          ║
║  3. Abrir sobre (verificar sellos intactos):                           ║
║     ├── Fecha de sellado: _______________                              ║
║     ├── Firmas en reverso: _______________                             ║
║     └── Si sellos rotos → NO USAR, investigar                         ║
║                                                                          ║
║  4. Seguir procedimiento según emergencia:                             ║
║     │                                                                   ║
║     ├── Si admin no puede acceder:                                     ║
║     │   a. Ir a https://vaultwarden.bhu.uy/admin                      ║
║     │   b. Ingresar Admin Token                                        ║
║     │   c. Ir a Users → Seleccionar usuario                           ║
║     │   d. Click "Reset Master Password"                              ║
║     │   e. Crear nueva master password                                 ║
║     │   f. Comunicar nueva contraseña al usuario                      ║
║     │                                                                   ║
║     ├── Si cuenta comprometida:                                        ║
║     │   a. Ir a Admin Panel                                            ║
║     │   b. Revocar todas las sesiones activas                         ║
║     │   c. Cambiar master password del usuario                        ║
║     │   d. Habilitar 2FA obligatorio                                  ║
║     │   e. Verificar logs de actividad sospechosa                     ║
║     │   f. Notificar a usuario                                        ║
║     │                                                                   ║
║     └── Si desastre total:                                             ║
║         a. Provisionar nuevo servidor                                  ║
║         b. Restaurar desde backup off-site                            ║
║         c. Seguir procedimiento de DRP                                ║
║         d. Verificar integridad                                       ║
║                                                                          ║
║  5. Documentar cada paso en el acta de emergencia                     ║
║                                                                          ║
║  6. Después de la emergencia:                                          ║
║     ├── Cambiar TODAS las credenciales comprometidas                  ║
║     ├── Re-sellar sobre con nuevas credenciales                       ║
║     ├── Devolver a caja fuerte                                        ║
║     └── Programar revisión post-incidente (48 horas)                  ║
║                                                                          ║
║  ─────────────────────────────────────────────────────────────────────   ║
║                                                                          ║
║  PERSONAS AUTORIZADAS:                                                   ║
║  ├── CEO: [Nombre] - [Email] - [Teléfono]                            ║
║  ├── CTO: [Nombre] - [Email] - [Teléfono]                            ║
║  └── IT Admin: [Nombre] - [Email] - [Teléfono]                       ║
║                                                                          ║
║  CÓDIGO DE VERIFICACIÓN: [Código de 6 dígitos para verificar]          ║
║                                                                          ║
║  FECHA DE ÚLTIMA ACTUALIZACIÓN: [FECHA]                                ║
║  PRÓXIMA REVISIÓN REQUERIDA: [FECHA + 90 días]                         ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝
```

### Acta de Uso de Break-Glass

```markdown
# ACTA DE USO DE BREAK-GLASS ACCOUNT
# Ticket #: [NÚMERO]
# Fecha: [FECHA] [HORA]

## Emergencia Reportada
- Tipo: [Olvido master pass / Cuenta comprometida / Desastre]
- Descripción: _______________
- Solicitante: _______________

## Personas Autorizadas Presentes
1. Nombre: _______________ Cargo: _______________
   Firma: _______________ Hora llegada: _______________

2. Nombre: _______________ Cargo: _______________
   Firma: _______________ Hora llegada: _______________

## Verificación de Sobre
- [ ] Sobre localizado en caja fuerte
- [ ] Sellos intactos verificados
- [ ] Código de verificación confirmado: _______________

## Acciones Realizadas
1. [Hora] _______________ Acción: _______________
2. [Hora] _______________ Acción: _______________
3. [Hora] _______________ Acción: _______________
...

## Resultado
- [ ] Acceso restaurado exitosamente
- [ ] Cuenta comprometida aislada
- [ ] Desastre mitigado
- [ ] Otro: _______________

## Próximos Pasos
1. _______________
2. _______________
3. _______________

## Cierre
- Hora de cierre: _______________
- Persona que cierra: _______________
- Próxima revisión: _______________

## Firmas
CEO: _______________ Fecha: _______________
CTO: _______________ Fecha: _______________
```

## Escenario 3: Compromiso de Cuenta Admin

### Procedimiento de Respuesta

```
┌─────────────────────────────────────────────────────────────────────────┐
│  PROCEDIMIENTO: COMPROMISO DE CUENTA ADMIN                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  FASE 1: DETECCIÓN (Inmediato)                                        │
│  ├── Señales de compromiso:                                           │
│  │   ├── Login desde IP/location inusual                             │
│  │   ├── Cambios no autorizados en permisos                          │
│  │   ├── Exportación de datos sospechosa                             │
│  │   ├── 2FA deshabilitado                                           │
│  │   └── Actividad fuera de horario laboral                          │
│  ├── Acción inmediata:                                                │
│  │   ├── Revocar sesión activa del admin                             │
│  │   ├── Bloquear cuenta temporalmente                               │
│  │   └── Notificar a CTO y CEO                                       │
│                                                                         │
│  FASE 2: CONTENCIÓN (5-30 min)                                       │
│  ├── Cambiar master password de la cuenta admin                       │
│  ├── Revocar TODOS los tokens API activos                            │
│  ├── Verificar 2FA sigue habilitado                                  │
│  ├── Revisar logs de actividad reciente                              │
│  │   ├── ¿Qué acciones realizó el admin comprometido?               │
│  │   ├── ¿Qué usuarios/colecciones afectó?                          │
│  │   └── ¿Hubo exportación de datos?                                │
│  ├── Verificar que no hay otros admins comprometidos                 │
│  └── Activar break-glass si es necesario                            │
│                                                                         │
│  FASE 3: ERRADICACIÓN (30 min - 2 horas)                             │
│  ├── Cambiar master password de TODOS los usuarios afectados         │
│  ├── Regenerar API keys comprometidas                                │
│  ├── Verificar integridad de vaults                                  │
│  ├── Revisar permisos de todos los usuarios                          │
│  ├── Verificar que no hay backdoors creadas                          │
│  └── Actualizar break-glass credentials                              │
│                                                                         │
│  FASE 4: RECUPERACIÓN (2-8 horas)                                    │
│  ├── Restaurar desde backup ANTERIOR al compromiso                   │
│  │   (si se detectó daño en datos)                                   │
│  ├── Verificar que todos los usuarios pueden acceder                 │
│  ├── Re-habilitar 2FA obligatorio                                    │
│  ├── Monitoreo intensivo por 72 horas                                │
│  └── Comunicar a usuarios afectados                                  │
│                                                                         │
│  FASE 5: POST-INCIDENTE (48 horas)                                   │
│  ├── Reunión de revisión con equipo directivo                        │
│  ├── Documentar causa raíz                                           │
│  ├── Implementar medidas preventivas                                 │
│  │   ├── IP whitelist para admin                                      │
│  │   ├── Monitoreo de actividad admin                                │
│  │   ├── Requiere 2 aprobaciones para cambios críticos               │
│  │   └── Auditoría semanal de permisos                               │
│  └── Actualizar plan de incidente                                    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Prevención: Capacitación Obligatoria

### Temario de Capacitación

```
┌─────────────────────────────────────────────────────────────────────────┐
│  CAPACITACIÓN: GESTIÓN SEGURA DE CONTRASEÑAS                            │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  MÓDULO 1: Fundamentos (1 hora)                                       │
│  ├── ¿Qué es un gestor de contraseñas?                              │
│  ├── ¿Por qué es importante?                                         │
│  ├── Cifrado E2E y zero-knowledge                                    │
│  └── Tipos de amenazas                                               │
│                                                                         │
│  MÓDULO 2: Uso Diario (1 hora)                                       │
│  ├── Login y desbloqueo                                              │
│  ├── Guardar y usar contraseñas                                      │
│  ├── Generar contraseñas seguras                                     │
│  ├── Compartir contraseñas                                           │
│  └── Verificación HIBP                                               │
│                                                                         │
│  MÓDULO 3: Seguridad (1 hora)                                        │
│  ├── Configurar 2FA/TOTP                                             │
│  ├── Configurar WebAuthn/FIDO2                                       │
│  ├── Biometría y PIN local                                           │
│  ├── Backup obligatorio                                              │
│  └── Phishing y cómo detectarlo                                      │
│                                                                         │
│  MÓDULO 4: Emergencias (30 min)                                      │
│  ├── ¿Qué hacer si olvido mi master password?                       │
│  ├── ¿Qué hacer si mi dispositivo se pierde/roba?                   │
│  ├── Procedimiento de recuperación                                   │
│  └── Contactar IT Helpdesk                                           │
│                                                                         │
│  MÓDULO 5: Práctica (30 min)                                         │
│  ├── Ejercicio práctico: crear vault                                 │
│  ├── Ejercicio práctico: guardar y usar contraseña                   │
│  ├── Ejercicio práctico: configurar 2FA                              │
│  └── Ejercicio práctico: backup y recuperación                       │
│                                                                         │
│  EVALUACIÓN:                                                           │
│  ├── Quiz de 10 preguntas (mínimo 80% para aprobar)                 │
│  └── Ejercicio práctico supervisado                                  │
│                                                                         │
│  CERTIFICADO:                                                          │
│  ├── Válido por 1 año                                                │
│  ├── Renovación: reciclaje anual de 30 min                           │
│  └── Requerido para acceso a sistemas críticos                       │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Resumen de Procedimientos

| Escenario | Tiempo Respuesta | Quién Actúa | Documentación |
|-----------|-----------------|-------------|---------------|
| Master pass olvidada (usuario) | 30 min - 2 hrs | IT Helpdesk | Ticket |
| Master pass olvidada (admin) | 1-4 hrs | CTO + CEO | Acta break-glass |
| Compromiso cuenta admin | 1-8 hrs | IT + Directivos | Incident report |
| Desastre total | 4-24 hrs | IT + todos | DRP completo |

---

> **Actividad final del curso**: Simula un escenario de emergencia (master password olvidada) con un compañero. Ejecuta el procedimiento completo y documenta cada paso. Evalúa: ¿el procedimiento funcionó? ¿Qué mejoras propondrías?
