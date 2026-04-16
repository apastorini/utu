# PLANTILLA: Mapa de Riesgos de Seguridad

## Instrucciones de Uso

Esta plantilla proporciona un formato estructurado para documentar el mapa de riesgos de seguridad de la información de una organización. Complete cada sección según las indicaciones.

---

## 1. Información General

| Campo | Valor |
|-------|-------|
| **Organización** | [Nombre de la empresa] |
| **Departamento/Área** | [Área responsable] |
| **Versión del documento** | [X.X] |
| **Fecha de elaboración** | DD/MM/AAAA |
| **Fecha de última actualización** | DD/MM/AAAA |
| **Próxima revisión programada** | DD/MM/AAAA |
| **Elaborado por** | [Nombre(s)] |
| **Revisado por** | [Nombre(s)] |
| **Aprobado por** | [Nombre(s) y cargo] |

---

## 2. Alcance y Contexto

### 2.1 Alcance del análisis

*Describa qué activos, sistemas, procesos y ubicaciones están incluidos en este mapa de riesgos:*

> 

> 

### 2.2 Contexto organizacional

*Misión, visión y objetivos estratégicos relevantes para seguridad:*

> 

### 2.3 Factores contextuales

| Factor | Descripción |
|--------|-------------|
| **Regulatorios** | Normativas aplicables (BCU, BCU, etc.) |
| **Sector** | Industria y características del sector |
| **Geográfico** | Ubicación(es) y consideraciones regionales |
| **Tecnológico** | stack tecnológico principal |
| **Tercerizados** | Proveedores y servicios externalizados |

---

## 3. Taxonomía de Riesgos

### 3.1 Categorías de riesgos definidas

| Código | Categoría | Definición operativa |
|--------|-----------|---------------------|
| R-CIA | Confidencialidad, Integridad, Disponibilidad | Riesgos técnicos de seguridad |
| R-OPE | Operativos | Errores, fallas de procesos |
| R-FRA | Fraude | Actividades fraudulentas |
| R-COMP | Cumplimiento | Incumplimiento normativo |
| R-FIS | Físicos | Acceso físico, desastres |
| R-REP | Reputacionales | Daño a imagen y marca |

### 3.2 Subcategorías específicas

*Agregue subcategorías según las necesidades de su organización:*

| Código | Subcategoría | Pertenece a |
|--------|-------------|-------------|
| | | |
| | | |
| | | |
| | | |
| | | |

---

## 4. Escala de Valoración

### 4.1 Escala de Probabilidad

| Nivel | Valor | Descripción | Criterios |
|-------|-------|-------------|----------|
| Muy Baja | 1 | Improbable | < 5% probabilidad anual |
| Baja | 2 | Poco probable | 5-20% probabilidad anual |
| Media | 3 | Posible | 20-50% probabilidad anual |
| Alta | 4 | Probable | 50-80% probabilidad anual |
| Muy Alta | 5 | Casi seguro | > 80% probabilidad anual |

### 4.2 Escala de Impacto

| Nivel | Valor | Descripción | Impacto financiero estimado |
|-------|-------|-------------|---------------------------|
| Muy Bajo | 1 | Insignificante | < USD [X] |
| Bajo | 2 | Menor | USD [X] - [Y] |
| Medio | 3 | Significativo | USD [Y] - [Z] |
| Alto | 4 | Grave | USD [Z] - [W] |
| Muy Alto | 5 | Catastrófico | > USD [W] |

### 4.3 Matriz de valoración (predefinida)

```
         IMPACTO
         1     2     3     4     5
Prob  ┌─────┬─────┬─────┬─────┬─────┐
  5   │  5  │ 10  │ 15  │ 20  │ 25  │
      ├─────┼─────┼─────┼─────┼─────┤
  4   │  4  │  8  │ 12  │ 16  │ 20  │
      ├─────┼─────┼─────┼─────┼─────┤
  3   │  3  │  6  │  9  │ 12  │ 15  │
      ├─────┼─────┼─────┼─────┼─────┤
  2   │  2  │  4  │  6  │  8  │ 10  │
      ├─────┼─────┼─────┼─────┼─────┤
  1   │  1  │  2  │  3  │  4  │  5  │
      └─────┴─────┴─────┴─────┴─────┘
```

### 4.4 Clasificación de riesgos

| Rango | Nivel | Color | Acciones |
|-------|-------|-------|----------|
| 1-4 | Bajo | Verde | Monitoreo |
| 5-9 | Medio | Amarillo | Planificar mitigación |
| 10-14 | Alto | Naranja | Mitigación urgente |
| 15-25 | Crítico | Rojo | Acción inmediata |

---

## 5. Inventario de Activos

### 5.1 Categorización de activos

| Categoría | Descripción | Criticidad típica |
|-----------|-------------|------------------|
| **Datos** | Bases de datos, archivos, información |
| **Aplicaciones** | Software, sistemas, APIs |
| **Infraestructura** | Servidores, redes, cloud |
| **Procesos** | Procedimientos operativos críticos |
| **Personas** | Personal clave, conocimiento |
| **Reputación** | Marca, imagen, relaciones |

### 5.2 Inventario simplificado

| ID Activo | Nombre | Categoría | Criticidad | Ubicación | Responsable |
|-----------|--------|-----------|-----------|-----------|-------------|
| A-001 | | | Alta/Media/Baja | | |
| A-002 | | | Alta/Media/Baja | | |
| A-003 | | | Alta/Media/Baja | | |
| A-004 | | | Alta/Media/Baja | | |
| A-005 | | | Alta/Media/Baja | | |

---

## 6. Registro de Riesgos

### 6.1 Formato de registro

| Campo | Descripción |
|-------|-------------|
| **ID** | Código único (R-XXX) |
| **Fecha de identificación** | DD/MM/AAAA |
| **Activo(s) afectado(s)** | ID(s) del activo |
| **Categoría** | Código de categoría |
| **Descripción** | Descripción detallada del riesgo |
| **Causa/Origen** | Qué origina el riesgo |
| **Probabilidad** | Valor 1-5 |
| **Impacto** | Valor 1-5 |
| **Valor del riesgo** | Probabilidad × Impacto |
| **Nivel** | Bajo/Medio/Alto/Crítico |
| **Controles actuales** | Medidas existentes |
| **Tratamiento propuesto** | Mitigar/Transferir/Aceptar/Evitar |
| **Responsable** | Persona a cargo |
| **Fecha objetivo de tratamiento** | DD/MM/AAAA |
| **Riesgo residual** | Valor después de controles |
| **Estado** | Activo/Mitigado/Cerrado |

### 6.2 Riesgos identificados

| ID | Activo | Categoría | Descripción | Prob | Imp | Valor | Nivel | Tratamiento | Estado |
|----|--------|-----------|-------------|------|-----|-------|-------|------------|--------|
| R-001 | | | | | | | | | |
| R-002 | | | | | | | | | |
| R-003 | | | | | | | | | |
| R-004 | | | | | | | | | |
| R-005 | | | | | | | | | |
| R-006 | | | | | | | | | |
| R-007 | | | | | | | | | |
| R-008 | | | | | | | | | |
| R-009 | | | | | | | | | |
| R-010 | | | | | | | | | |

---

## 7. Mapa de Calor Visual

### 7.1 Representación del mapa

*Copie o dibuje su matriz de riesgos:*

```
┌─────────────────────────────────────────────────────────────┐
│                         MAPA DE CALOR                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   IMPACTO                                                   │
│     ▲                                                       │
│   5 │                                                       │
│     │                                                       │
│   4 │                                                       │
│     │                                                       │
│   3 │                                                       │
│     │                                                       │
│   2 │                                                       │
│     │                                                       │
│   1 │                                                       │
│     └────────────────────────────────────────────────►     │
│       1   2   3   4   5                                      │
│                      PROBABILIDAD                           │
│                                                             │
│   [Escriba el ID de cada riesgo en su posición]            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 7.2 Leyenda

| Color | Nivel | Cantidad | % del total |
|-------|-------|----------|------------|
| 🟢 Verde | Bajo | | |
| 🟡 Amarillo | Medio | | |
| 🟠 Naranja | Alto | | |
| 🔴 Rojo | Crítico | | |

---

## 8. Plan de Tratamiento de Riesgos

### 8.1 Controles propuestos

| ID Riesgo | Control propuesto | Tipo | Prioridad | Responsable | Fecha objetivo | Presupuesto estimado |
|-----------|-------------------|------|-----------|-------------|-----------------|---------------------|
| | | Preventivo/Detectivo/Correctivo | Alta/Media/Baja | | | |
| | | | | | | |
| | | | | | | |
| | | | | | | |
| | | | | | | |

### 8.2 Cronograma de implementación

| Trimestre | Acciones principales | Riesgos abordados |
|-----------|---------------------|------------------|
| Q1 20XX | | |
| Q2 20XX | | |
| Q3 20XX | | |
| Q4 20XX | | |

---

## 9. Indicadores y Monitoreo

### 9.1 Key Risk Indicators (KRI)

| KRI | Descripción | Fórmula | Frecuencia | Umbral verde | Umbral amarillo | Umbral rojo |
|-----|-------------|---------|------------|--------------|-----------------|-------------|
| KRI-01 | | | | | | |
| KRI-02 | | | | | | |
| KRI-03 | | | | | | |

### 9.2 Frecuencia de revisión

| Tipo de revisión | Frecuencia | Participantes | Entregable |
|------------------|------------|---------------|------------|
| Monitoreo operativo | [Frecuencia] | Equipo seguridad | Reporte |
| Revisión táctica | [Frecuencia] | CISO + Gerencia | Matriz actualizada |
| Revisión estratégica | [Frecuencia] | Comité de Riesgos | Informe al Directorio |

---

## 10. Aprobaciones

| Rol | Nombre | Fecha | Firma |
|-----|--------|-------|-------|
| Elaborado por | | | |
| Revisado por (CISO) | | | |
| Aprobado por (Gerencia) | | | |
| Aprobado por (Directorio) | | | |

---

## Historial de Cambios

| Versión | Fecha | Descripción del cambio | Autor |
|---------|-------|------------------------|-------|
| 1.0 | DD/MM/AAAA | Creación inicial | |
| | | | |
| | | | |

---

**Nota:** Personalice esta plantilla según las necesidades específicas de su organización, regulaciones aplicables y estándares de referencia (ISO 27001, NIST CSF, etc.).
