# Plan de Gestión de Incidentes de Seguridad Bancaria

## Instrucciones de Uso

Este documento es una plantilla para el registro y gestión de incidentes de seguridad de la información en instituciones bancarias uruguayas. Debe ser completado por el equipo de respuesta a incidentes (CSIRT) cuando ocurra cualquier incidente de seguridad.

**Tiempo máximo de llenado inicial:** 30 minutos desde la detección del incidente.

---

## 1. Identificación del Incidente

### 1.1 Datos Generales

| Campo | Valor |
|-------|-------|
| **ID del Incidente** | INC-[AAAA]-[0000] |
| **Fecha de detección** | DD/MM/AAAA HH:MM |
| **Fecha de inicio estimada** | DD/MM/AAAA HH:MM (o "Desconocida") |
| **Fecha de reporte** | DD/MM/AAAA HH:MM |
| **Hora local** | UTC-3 |
| **Detectado por** | [Nombre / Sistema / Herramienta] |
| **Clasificación inicial** | [ ] Confirmado / [ ] Sospechoso |

### 1.2 Clasificación del Incidente

Marque la categoría principal y todas las secundarias aplicables:

**Categoría principal:**
- [ ] Malware (incluye ransomware)
- [ ] Phishing/Ingeniería social
- [ ] Acceso no autorizado
- [ ] Divulgación de datos
- [ ] Denegación de servicio
- [ ] Fraude
- [ ] Uso inapropiado de recursos
- [ ] Compromiso de aplicación
- [ ] Vulnerabilidad explotada
- [ ] Incidente físico
- [ ] Otro: _______________

**Categorías secundarias:**
- [ ] Compromiso de credenciales
- [ ] Exfiltración de datos
- [ ] Modificación no autorizada
- [ ] Destrucción de datos
- [ ] Interrupción de servicio
- [ ] Acceso interno no autorizado
- [ ] Amenaza interna

### 1.3 Nivel de Severidad

| Nivel | Descripción | Tiempo de respuesta objetivo |
|-------|-------------|------------------------------|
| [ ] **Crítico (P1)** | Compromiso de sistemas core, breach masivo, ransomware generalizado | Inmediato (< 15 min) |
| [ ] **Alto (P2)** | Compromiso significativo, breach parcial, fraude confirmado | < 1 hora |
| [ ] **Medio (P3)** | Incidente contenido, compromiso limitado | < 4 horas |
| [ ] **Bajo (P4)** | Intento detectado y bloqueado, alerta sin impacto | < 24 horas |

**Justificación de severidad:**
> [Explique brevemente por qué se asignó este nivel]

---

## 2. Descripción del Incidente

### 2.1 Resumen Ejecutivo

*Descripción de máximo 3 oraciones: qué ocurrió, cuándo, y cuál es el impacto estimado.*

> 

> 

> 

### 2.2 Detalle Completo

*Descripción cronológica detallada de los eventos:*

**Línea de tiempo de eventos:**

| Hora | Evento | Fuente de información | Evidencia |
|------|--------|----------------------|-----------|
| HH:MM | | | |
| | | | |
| | | | |
| | | | |
| | | | |
| | | | |

### 2.3 Sistemas y Activos Afectados

| ID Asset | Nombre del sistema | Criticidad | Tipo de compromiso | # Usuarios afectados |
|----------|--------------------|------------|--------------------|--------------------|
| | | [ ] Alta [ ] Media [ ] Baja | | |
| | | [ ] Alta [ ] Media [ ] Baja | | |
| | | [ ] Alta [ ] Media [ ] Baja | | |
| | | [ ] Alta [ ] Media [ ] Baja | | |

### 2.4 Datos Comprometidos (si aplica)

| Tipo de dato | Volumen estimado | Sensibilidad | Datos personales? |
|--------------|-----------------|--------------|-------------------|
| [ ] Datos personales (clientes) | | [ ] Alta [ ] Media [ ] Baja | [ ] Sí [ ] No |
| [ ] Datos financieros | | [ ] Alta [ ] Media [ ] Baja | [ ] Sí [ ] No |
| [ ] Credenciales | | [ ] Alta [ ] Media [ ] Baja | [ ] Sí [ ] No |
| [ ] Información confidencial | | [ ] Alta [ ] Media [ ] Baja | [ ] Sí [ ] No |
| [ ] Datos de tarjetas (PAN) | | | [ ] Sí [ ] No |
| [ ] Otro: _______________ | | [ ] Alta [ ] Media [ ] Baja | [ ] Sí [ ] No |

**Cantidad total de registros afectados:** _______________
**Cantidad de clientes afectados:** _______________

---

## 3. Investigación

### 3.1 Hipótesis Inicial

*¿Qué cree que ocurrió y cómo fue posible?*

> 

> 

### 3.2 Hallazgos de Investigación

**Análisis de logs:**
- [ ] SIEM revisado: _______________
- [ ] Logs de firewall: [ ] Sí [ ] No [ ] Parcial
- [ ] Logs de aplicaciones: [ ] Sí [ ] No [ ] Parcial
- [ ] Logs de endpoints: [ ] Sí [ ] No [ ] Parcial
- [ ] Logs de Active Directory: [ ] Sí [ ] No [ ] Parcial

**Evidencia recopilada:**

| # | Tipo de evidencia | Ubicación/Referencia | Cadena de custodia |
|---|-------------------|---------------------|-------------------|
| 1 | | | [ ] Sí [ ] No |
| 2 | | | [ ] Sí [ ] No |
| 3 | | | [ ] Sí [ ] No |
| 4 | | | [ ] Sí [ ] No |

**IOCs (Indicadores de Compromiso) identificados:**

| IOC | Tipo | Valor |
|-----|------|-------|
| 1 | IP | |
| 2 | Dominio | |
| 3 | Hash de archivo | |
| 4 | URL | |
| 5 | Email | |

### 3.3 Análisis de Causa Raíz

*Describa la causa raíz del incidente:*

> 

> 

**Causa raíz identificada:**
- [ ] Vulnerabilidad no parcheada
- [ ] Error de configuración
- [ ] Error humano
- [ ] Acción maliciosa interna
- [ ] Acción maliciosa externa
- [ ] Falla de proceso
- [ ] Proveedor tercerizado
- [ ] Otro: _______________

---

## 4. Contención

### 4.1 Acciones de Contención Inmediatas

| # | Acción | Responsable | Hora de ejecución | Completada? |
|---|--------|-------------|------------------|-------------|
| 1 | | | HH:MM | [ ] Sí [ ] No |
| 2 | | | HH:MM | [ ] Sí [ ] No |
| 3 | | | HH:MM | [ ] Sí [ ] No |
| 4 | | | HH:MM | [ ] Sí [ ] No |

### 4.2 Acciones de Contención a Largo Plazo

| # | Acción | Responsable | Fecha objetivo | Estado |
|---|--------|-------------|---------------|--------|
| 1 | | | DD/MM | [ ] Pendiente [ ] En curso [ ] Completada |
| 2 | | | DD/MM | [ ] Pendiente [ ] En curso [ ] Completada |
| 3 | | | DD/MM | [ ] Pendiente [ ] En curso [ ] Completada |

---

## 5. Remediación y Recuperación

### 5.1 Plan de Remediación

| # | Acción correctiva | Prioridad | Responsable | Fecha objetivo | Estado |
|---|-------------------|-----------|-------------|---------------|--------|
| 1 | Parcheo de vulnerabilidad | | | | [ ] |
| 2 | Reinicio/reconstrucción de sistemas | | | | [ ] |
| 3 | Reset de credenciales comprometidas | | | | [ ] |
| 4 | Actualización de reglas de seguridad | | | | [ ] |
| 5 | Revisión de permisos y accesos | | | | [ ] |
| 6 | Implementación de nuevo control | | | | [ ] |
| 7 | Capacitación adicional | | | | [ ] |
| 8 | Otro: _______________ | | | | [ ] |

### 5.2 Recuperación de Sistemas

| Sistema | Acción de recuperación | Fecha inicio | Fecha completada | Validado por |
|---------|------------------------|--------------|-----------------|--------------|
| | | | | |
| | | | | |
| | | | | |

**¿Se recuperaron todos los datos?**
- [ ] Sí, integridad verificada
- [ ] Parcialmente (especificar en observaciones)
- [ ] No aplica (sin pérdida de datos)

**Observaciones de recuperación:**
> 

---

## 6. Notificaciones

### 6.1 Notificaciones Internas

| Destinatario | Método | Fecha/Hora | Completada? |
|--------------|--------|------------|-------------|
| CISO | | | [ ] Sí [ ] No |
| Director de Tecnología | | | [ ] Sí [ ] No |
| Gerencia General | | | [ ] Sí [ ] No |
| Legal/Asesoría Legal | | | [ ] Sí [ ] No |
| Área de Cumplimiento | | | [ ] Sí [ ] No |
| Comunicaciones/RRPP | | | [ ] Sí [ ] No |
| Recursos Humanos (si interno) | | | [ ] Sí [ ] No |
| Comité de Crisis | | | [ ] Sí [ ] No |

### 6.2 Notificaciones Regulatorias

| Entidad | Requerido? | Plazo legal | Fecha límite | Estado |
|---------|-----------|-------------|--------------|--------|
| BCU | [ ] Sí [ ] No | 24 horas* | | [ ] Notificado [ ] Pendiente [ ] No aplica |
| AGESIC (CERTuy) | [ ] Sí [ ] No | 72 horas | | [ ] Notificado [ ] Pendiente [ ] No aplica |
| URCDP (protección datos) | [ ] Sí [ ] No | 72 horas | | [ ] Notificado [ ] Pendiente [ ] No aplica |

*Consulte la normativa vigente para plazos exactos según el tipo de incidente.

### 6.3 Notificaciones a Terceros

| Destinatario | Razón | Método | Fecha/Hora | Completada? |
|--------------|-------|--------|------------|-------------|
| Proveedores afectados | | | | [ ] Sí [ ] No |
| Clientes afectados | | | | [ ] Sí [ ] No |
| Autoridades policiales | [ ] Sí [ ] No | | | [ ] Sí [ ] No |
| Aseguradoras | [ ] Sí [ ] No | | | [ ] Sí [ ] No |

---

## 7. Impacto y Costos

### 7.1 Evaluación de Impacto

| Tipo de impacto | Estimación |
|-----------------|------------|
| Impacto financiero directo | USD _______________ |
| Pérdida de ingresos por indisponibilidad | USD _______________ |
| Costos de investigación y respuesta | USD _______________ |
| Costos legales y regulatorios | USD _______________ |
| Costos de remediación tecnológica | USD _______________ |
| Impacto reputacional (estimado) | [ ] Bajo [ ] Medio [ ] Alto [ ] Muy alto |
| **Total estimado** | **USD _______________** |

### 7.2 Impacto Operativo

| Métrica | Valor |
|---------|-------|
| Tiempo total de indisponibilidad | _______________ horas |
| Número de transacciones afectadas | _______________ |
| Número de cuentas afectadas | _______________ |
| Sistemas fuera de servicio | _______________ |

---

## 8. Lecciones Aprendidas

### 8.1 ¿Qué funcionó bien?

> 

> 

### 8.2 ¿Qué podría mejorarse?

> 

> 

### 8.3 Recomendaciones para Prevenir Incidentes Similares

| # | Recomendación | Prioridad | Responsable | Fecha objetivo |
|---|----------------|-----------|-------------|---------------|
| 1 | | [ ] Alta [ ] Media [ ] Baja | | |
| 2 | | [ ] Alta [ ] Media [ ] Baja | | |
| 3 | | [ ] Alta [ ] Media [ ] Baja | | |

### 8.4 Actualización de Documentación

| Documento | Cambio recomendado | Estado |
|-----------|-------------------|--------|
| Procedimientos de seguridad | | [ ] Actualizado [ ] Pendiente |
| Controles técnicos | | [ ] Actualizado [ ] Pendiente |
| Plan de capacitación | | [ ] Actualizado [ ] Pendiente |
| Inventario de activos | | [ ] Actualizado [ ] Pendiente |

---

## 9. Cierre del Incidente

### 9.1 Validación Final

| Verificación | Estado |
|--------------|--------|
| Contención confirmada | [ ] Sí [ ] No |
| Sistemas restaurados | [ ] Sí [ ] No |
| Amenaza eradicated | [ ] Sí [ ] No |
| Vulnerabilidades remediadas | [ ] Sí [ ] No |
| Monitoreo intensificado en curso | [ ] Sí [ ] No |
| Notificaciones completadas | [ ] Sí [ ] No |

### 9.2 Cierre Formal

| Campo | Valor |
|-------|-------|
| **Fecha de cierre** | DD/MM/AAAA |
| **Duración total del incidente** | _______________ días |
| **Estado final** | [ ] Resuelto [ ] Contenido [ ] Cerrado por inactividad |
| **Resuelto por** | |
| **Aprobado por (CISO)** | |
| **Aprobado por (Gerencia)** | |

### 9.3 Clasificación Final

| Campo | Valor |
|-------|-------|
| ¿Fue un breach de datos personales? | [ ] Sí [ ] No |
| ¿Hubo fraude confirmado? | [ ] Sí [ ] No |
| ¿Se requirió escalamiento regulatorio? | [ ] Sí [ ] No |
| **Categoría final:** | |

---

## 10. Anexos

### 10.1 Lista de Evidencias

| # | Descripción | Formato | Custodio | Ubicación |
|---|-------------|---------|----------|-----------|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |

### 10.2 Línea de Tiempo Consolidada

*Grafique la línea de tiempo final del incidente:*

```
[Línea de tiempo]
```

### 10.3 Contactos de Respuesta

| Rol | Nombre | Teléfono | Email | 24/7? |
|-----|--------|----------|-------|-------|
| Líder de respuesta | | | | [ ] Sí [ ] No |
| CISO | | | | [ ] Sí [ ] No |
| Forense externo | | | | [ ] Sí [ ] No |
| Legal | | | | [ ] Sí [ ] No |
| Comunicaciones | | | | [ ] Sí [ ] No |

---

**Documento preparado por:** _________________________
**Cargo:** _________________________
**Fecha:** _________________________

**Aprobado por:** _________________________
**Cargo:** _________________________
**Fecha:** _________________________

---

## Checklist de Cierre de Incidente

- [ ] Formulario completo
- [ ] Todas las evidencias documentadas
- [ ] Cadena de custodia intacta
- [ ] Notificaciones internas completadas
- [ ] Notificaciones regulatorias según aplique
- [ ] Plan de remediación documentado
- [ ] Lecciones aprendidas registradas
- [ ] Aprobaciones firmadas
- [ ] Archivo en repositorio seguro
- [ ] Referencia en registro maestro de incidentes
