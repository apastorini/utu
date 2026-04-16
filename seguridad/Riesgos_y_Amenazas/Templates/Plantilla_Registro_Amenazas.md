# PLANTILLA: Registro de Amenazas de Ciberseguridad

## Instrucciones de Uso

Esta plantilla proporciona un formato estructurado para documentar las amenazas de ciberseguridad identificadas en la organización. Complete cada sección según las indicaciones y mantenga el registro actualizado.

---

## 1. Información General

| Campo | Valor |
|-------|-------|
| **Organización** | [Nombre de la empresa] |
| **Versión del documento** | [X.X] |
| **Fecha de elaboración** | DD/MM/AAAA |
| **Última actualización** | DD/MM/AAAA |
| **Elaborado por** | [Nombre(s)] |
| **Clasificación** | [Confidencial/Interno/Público] |

---

## 2. Taxonomía de Amenazas

### 2.1 Categorización por origen

| Código | Categoría | Descripción | Ejemplos |
|--------|-----------|-------------|----------|
| AMZ-NAT | Naturales | Eventos físicos naturales | Terremotos, inundaciones |
| AMZ-TEC | Técnicas | Fallas de tecnología | Fallas de hardware, software |
| AMZ-ACC | Accidentales | Acciones no intencionales | Error humano, negligencia |
| AMZ-INT | Internas intencionales | Actores internos maliciosos | Empleados, contratistas |
| AMZ-EXT | Externas intencionales | Actores externos maliciosos | Hackers, cibercriminales, APT |
| AMZ-ORG | Organizacionales | Cambios internos | Reestructuración, cambio de proveedor |

### 2.2 Categorización por motivación

| Código | Motivación | Descripción |
|--------|------------|-------------|
| MOT-FIN | Financiera | Beneficio económico directo |
| MOT-ESP | Espionaje | Robo de información |
| MOT-SAB | Sabotaje | Dañar operaciones |
| MOT-IDE | Ideológica | Causa política o social |
| MOT-VEN | Venganza | Desquite personal |
| MOT-PRE | Prestigio | Fama, reputación |
| MOT-DES | Destrucción | Daño sin beneficio directo |

### 2.3 Actores de amenaza conocidos

| Actor | Tipo | Motivación | Capacidad | Region/Industria | Observaciones |
|-------|------|------------|-----------|------------------|---------------|
| | | | Alta/Media/Baja | | |
| | | | Alta/Media/Baja | | |
| | | | Alta/Media/Baja | | |
| | | | Alta/Media/Baja | | |

---

## 3. Registro de Amenazas

### 3.1 Formato de entrada

| Campo | Descripción |
|-------|-------------|
| **ID** | Código único (AMZ-XXX) |
| **Fecha de identificación** | DD/MM/AAAA |
| **Fuente** | Dónde se identificó (threat intel, auditoría, incidente) |
| **Categoría** | Código de categoría de origen |
| **Motivación** | Código de motivación |
| **Descripción** | Descripción detallada de la amenaza |
| **Activo(s) vulnerable(s)** | Sistemas o datos que podrían verse afectados |
| **Vector de ataque** | Cómo se materializaría la amenaza |
| **Probabilidad** | Valoración (1-5) |
| **Impacto potencial** | Valoración (1-5) |
| **Nivel de riesgo** | Calculado |
| **TTPs asociados** | Técnicas MITRE ATT&CK relacionadas |
| **IOCs conocidos** | Indicadores de compromiso |
| **Controles actuales** | Medidas existentes |
| **Gaps identificados** | Deficiencias en controles |
| **Acciones recomendadas** | Mejoras sugeridas |
| **Responsable** | Persona a cargo del seguimiento |
| **Estado** | Activo/Mitigado/En monitoreo/Cerrado |
| **Última revisión** | DD/MM/AAAA |

### 3.2 Entradas del registro

---

## AMZ-001

| Campo | Valor |
|-------|-------|
| **Nombre de la amenaza** | [Nombre descriptivo] |
| **Fecha de identificación** | DD/MM/AAAA |
| **Fuente** | [Fuente de identificación] |
| **Categoría** | [Código de categoría] |
| **Motivación** | [Código de motivación] |
| **Descripción** | [Descripción detallada] |

**Activos vulnerables:**
- [ ] Activo 1
- [ ] Activo 2

**Vector de ataque:**
> 

**Valoración:**
| Criterio | Valor |
|----------|-------|
| Probabilidad | 1-5 |
| Impacto | 1-5 |
| Nivel de riesgo | |

**Mapeo ATT&CK:**
| Technique ID | Technique Name | Aplicabilidad |
|--------------|----------------|---------------|
| | | Alta/Media/Baja |

**IOCs:**
| Tipo | Valor |
|------|-------|
| IP | |
| Dominio | |
| Hash | |
| Otro | |

**Controles actuales:**
> 

**Gaps identificados:**
> 

**Acciones recomendadas:**
| # | Acción | Prioridad | Responsable | Fecha objetivo |
|---|--------|-----------|-------------|----------------|
| 1 | | Alta/Media/Baja | | |

**Estado:** [ ] Activo [ ] Mitigado [ ] En monitoreo [ ] Cerrado
**Responsable:**
**Última revisión:** DD/MM/AAAA

---

## AMZ-002

*(Repetir estructura para cada amenaza)*

---

## AMZ-003

---

## AMZ-004

---

## AMZ-005

---

## 4. Análisis de Tendencias

### 4.1 Amenazas emergentes

*Documente amenazas nuevas o en evolución que podrían afectar a la organización:*

| Amenaza | Descripción | Relevancia | Probabilidad | Observaciones |
|---------|-------------|------------|--------------|---------------|
| | | Alta/Media/Baja | 1-5 | |
| | | Alta/Media/Baja | 1-5 | |
| | | Alta/Media/Baja | 1-5 | |

### 4.2 Tendencias sectoriales

*Amenazas específicas del sector [banca/finanzas/salud/etc.]:*

> 

---

## 5. Mapeo a MITRE ATT&CK

### 5.1 Técnicas más relevantes para la organización

| Technique ID | Technique Name | Táctica | Amenazas asociadas | Controles implementados |
|--------------|----------------|---------|---------------------|-------------------------|
| | | | AMZ-XXX | [ ] Sí [ ] No |
| | | | | |
| | | | | |
| | | | | |
| | | | | |

### 5.2 Cobertura de controles por táctica

| Táctica | # Técnicas relevantes | # Técnicas con control | Cobertura % |
|---------|----------------------|----------------------|-------------|
| Reconnaissance | | | |
| Resource Development | | | |
| Initial Access | | | |
| Execution | | | |
| Persistence | | | |
| Privilege Escalation | | | |
| Defense Evasion | | | |
| Credential Access | | | |
| Discovery | | | |
| Lateral Movement | | | |
| Collection | | | |
| Command and Control | | | |
| Exfiltration | | | |
| Impact | | | |

---

## 6. Fuentes de Inteligencia

### 6.1 Fuentes de amenaza

| Fuente | Tipo | Frecuencia | Responsable | last consulted |
|--------|------|------------|-------------|----------------|
| CERTuy/AGESIC | Nacional | Ad-hoc | | DD/MM/AAAA |
| ISAC [sector] | Sectorial | Mensual | | DD/MM/AAAA |
| CISA/NCSC | Internacional | Ad-hoc | | DD/MM/AAAA |
| Proveedor de TI [nombre] | Comercial | Semanal | | DD/MM/AAAA |
| [Otra fuente] | | | | |

### 6.2 Integración con feeds

| Feed | Contenido | Plataforma de consumo | Frecuencia |
|------|-----------|----------------------|------------|
| | | | |
| | | | |
| | | | |

---

## 7. Alertas y Notificaciones

### 7.1 Alertas activas

| ID Alerta | Fuente | Fecha | Amenaza relacionada | Estado | Acciones tomadas |
|-----------|--------|-------|-------------------|--------|------------------|
| | | DD/MM/AAAA | AMZ-XXX | Nueva/En análisis/Cerrada | |
| | | DD/MM/AAAA | AMZ-XXX | Nueva/En análisis/Cerrada | |
| | | DD/MM/AAAA | AMZ-XXX | Nueva/En análisis/Cerrada | |

### 7.2 Protocolo de escalamiento

| Nivel | Criterio | Destinatario | Tiempo de respuesta |
|-------|----------|--------------|---------------------|
| 1 | KRI en amarillo | Equipo Seguridad | 24 horas |
| 2 | KRI en rojo | CISO | 4 horas |
| 3 | Incidente confirmado | Gerencia General | 1 hora |
| 4 | Crisis | Comité de Crisis + Directorio | Inmediato |

---

## 8. Evaluaciones Periódicas

### 8.1 Checklist de revisión

| # | Actividad | Frecuencia | Última fecha | Estado |
|---|-----------|------------|--------------|--------|
| 1 | Revisión de Threat Intel feeds | [Frecuencia] | DD/MM/AAAA | [ ] Completada |
| 2 | Actualización de registro de amenazas | [Frecuencia] | DD/MM/AAAA | [ ] Completada |
| 3 | Revisión de IOCs | [Frecuencia] | DD/MM/AAAA | [ ] Completada |
| 4 | Evaluación de nuevos actores | [Frecuencia] | DD/MM/AAAA | [ ] Completada |
| 5 | Prueba de controles | [Frecuencia] | DD/MM/AAAA | [ ] Completada |
| 6 | Actualización de mapeo ATT&CK | [Frecuencia] | DD/MM/AAAA | [ ] Completada |
| 7 | Revisión con Comité de Riesgos | [Frecuencia] | DD/MM/AAAA | [ ] Completada |

### 8.2 Próximas actividades

| Actividad | Fecha programada | Responsable |
|-----------|-----------------|-------------|
| | DD/MM/AAAA | |
| | DD/MM/AAAA | |
| | DD/MM/AAAA | |

---

## 9. Aprobaciones

| Rol | Nombre | Fecha | Firma |
|-----|--------|-------|-------|
| Elaborado por | | | |
| Revisado por (CISO) | | | |
| Aprobado por (Gerencia) | | | |

---

## Historial de Cambios

| Versión | Fecha | Descripción del cambio | Autor |
|---------|-------|------------------------|-------|
| 1.0 | DD/MM/AAAA | Creación inicial | |
| | | | |
| | | | |

---

## Anexo: Glosario de Términos

| Término | Definición |
|---------|------------|
| **IOC** | Indicator of Compromise - Indicador de compromiso |
| **TTP** | Tactics, Techniques, and Procedures |
| **APT** | Advanced Persistent Threat - Amenaza persistente avanzada |
| **Threat Intel** | Inteligencia de amenazas - Información sobre actores de amenaza |
| **OSINT** | Open Source Intelligence - Inteligencia de fuentes abiertas |
| **MITRE ATT&CK** | Framework de conocimiento de tácticas y técnicas de ataque |
| **Diamond Model** | Modelo para análisis de amenazas basado en 4 elementos |
| **Kill Chain** | Fases de un ataque (ej. Lockheed Martin) |

---

**Nota:** Mantenga este registro actualizado y revíselo periódicamente. Integre la información con otras herramientas de seguridad (SIEM, SOAR, EDR) cuando sea posible.
