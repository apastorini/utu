# Checklist de Seguridad - Gestión de Contraseñas

## Uso diario

| # | Verificación | Estado | Responsable | Fecha |
|---|-------------|--------|-------------|-------|
| 1 | Login con master password fuerte | ☐ | Cada usuario | |
| 2 | 2FA habilitado y funcionando | ☐ | Cada usuario | |
| 3 | No compartir master password | ☐ | Cada usuario | |
| 4 | Usar autofill del navegador | ☐ | Cada usuario | |
| 5 | Verificar URL antes de login (anti-phishing) | ☐ | Cada usuario | |
| 6 | No guardar contraseñas en texto plano | ☐ | Cada usuario | |
| 7 | Cerrar sesión en dispositivos compartidos | ☐ | Cada usuario | |

## Semanal

| # | Verificación | Estado | Responsable | Fecha |
|---|-------------|--------|-------------|-------|
| 1 | Revisar notificaciones de seguridad | ☐ | IT Admin | |
| 2 | Verificar logins fallidos inusuales | ☐ | IT Admin | |
| 3 | Comprobar sincronización funciona | ☐ | Cada usuario | |
| 4 | Verificar HIBP (contraseñas en brechas) | ☐ | IT Admin | |
| 5 | Revisar compartición de contraseñas | ☐ | IT Admin | |

## Mensual

| # | Verificación | Estado | Responsable | Fecha |
|---|-------------|--------|-------------|-------|
| 1 | Ejecutar backup manual de vault personal | ☐ | Cada usuario | |
| 2 | Verificar backup del servidor | ☐ | IT Admin | |
| 3 | Revisar permisos de usuarios | ☐ | IT Admin | |
| 4 | Actualizar vault con cambios recientes | ☐ | Cada usuario | |
| 5 | Verificar rotación de API keys próximas | ☐ | IT Admin | |
| 6 | Ejecutar drill de restauración (simulación) | ☐ | IT Admin | |

## Trimestral

| # | Verificación | Estado | Responsable | Fecha |
|---|-------------|--------|-------------|-------|
| 1 | Auditoría completa de permisos | ☐ | CTO | |
| 2 | Rotar API keys (90 días) | ☐ | DevOps | |
| 3 | Actualizar wordlist de verificación HIBP | ☐ | IT Admin | |
| 4 | Revisar y actualizar documentación | ☐ | IT Admin | |
| 5 | Capacitación de usuarios nuevos | ☐ | IT Admin | |
| 6 | Verificar integridad de backups | ☐ | IT Admin | |
| 7 | Revisar certificados TLS | ☐ | IT Admin | |
| 8 | Actualizar break-glass credentials | ☐ | CTO | |

## Anual

| # | Verificación | Estado | Responsable | Fecha |
|---|-------------|--------|-------------|-------|
| 1 | Revisión completa de política de contraseñas | ☐ | CTO + CEO | |
| 2 | Auditoría externa de seguridad | ☐ | Externo | |
| 3 | Actualizar BCP y DRP | ☐ | IT Admin | |
| 4 | Renovar certificados TLS | ☐ | IT Admin | |
| 5 | Revisar cumpliance normativo | ☐ | Legal + IT | |
| 6 | Evaluación de herramientas alternativas | ☐ | CTO | |
| 7 | Actualizar capacitación obligatoria | ☐ | RRHH + IT | |
| 8 | Test completo de recuperación | ☐ | IT Admin | |

## Verificación de Seguridad del Servidor

| # | Verificación | Estado | Última Verificación | Próxima |
|---|-------------|--------|---------------------|---------|
| 1 | Vaultwarden actualizado | ☐ | | |
| 2 | PostgreSQL actualizado | ☐ | | |
| 3 | NGINX actualizado | ☐ | | |
| 4 | Docker actualizado | ☐ | | |
| 5 | SO actualizado (patches) | ☐ | | |
| 6 | Firewall configurado | ☐ | | |
| 7 | TLS 1.3 habilitado | ☐ | | |
| 8 | Rate limiting activo | ☐ | | |
| 9 | Health checks funcionando | ☐ | | |
| 10 | Backup automático verificado | ☐ | | |
| 11 | Logs centralizados activos | ☐ | | |
| 12 | Monitoreo de recursos activo | ☐ | | |

## Verificación de Seguridad de Usuarios

| # | Usuario | 2FA | Vault Backup | Master Pass ≥20 | Última Verificación |
|---|---------|-----|--------------|-----------------|---------------------|
| 1 | admin@bhu.uy | ☐ | ☐ | ☐ | |
| 2 | juan.perez@bhu.uy | ☐ | ☐ | ☐ | |
| 3 | maria.garcia@bhu.uy | ☐ | ☐ | ☐ | |
| 4 | carlos.lopez@bhu.uy | ☐ | ☐ | ☐ | |
| 5 | [agregar más] | ☐ | ☐ | ☐ | |

---

## Firma de Verificación

| Rol | Nombre | Verificación | Fecha |
|-----|--------|-------------|-------|
| IT Admin | | ☐ Checklist completo | |
| CTO | | ☐ Revisión aprobada | |

---

> **Frecuencia**: Este checklist debe completarse según la frecuencia indicada (diario/semanal/mensual/trimestral/anual). Mantener registros de al menos los últimos 12 meses.
