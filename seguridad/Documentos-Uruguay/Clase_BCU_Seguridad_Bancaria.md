# SEGURIDAD BANCARIA EN URUGUAY - BCU

---

## ÍNDICE

1. Marco Regulatorio Bancario Uruguayo
2. Superintendencia de Servicios Financieros
3. Normativa de Seguridad de la Información
4. Requisitos de Ciberseguridad
5. Gestión de Riesgos Tecnológicos
6. Servicios Esenciales y Continuidad
7. Protección de Datos del Cliente
8. Incidentes y Notificaciones
9. Auditoría y Compliance
10. Guía de Implementación
11. Plantillas y Checklist

---

## 1. MARCO REGULATORIO BANCARIO URUGUAYO

### 1.1. Estructura del Sistema Financiero Uruguayo

```
┌─────────────────────────────────────────────────────────────────┐
│              SISTEMA FINANCIERO URUGUAYO                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  BANCO CENTRAL DEL URUGUAY (BCU)                               │
│  │                                                               │
│  ├── Superintendencia de Servicios Financieros                  │
│  │   ├── Regulación de bancos                             │
│  │   ├── Supervisión de seguros                          │
│  │   └── Cooperativas de ahorro y crédito               │
│  │                                                           │
│  ├── Gerencia de Política Monetaria                        │
│  ├── Gerencia de Operaciones                          │
│  └── Gerencia de Riesgos                                  │
│                                                                 │
│  ORGANISMOS RELACIONADOS:                                     │
│  ├── BCU (Banco Central)                                   │
│  ├── AGESIC (Ciberseguridad)                               │
│  ├── URCDP (Protección de datos)                          │
│  └── UIF (Lavado de activos)                               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2. Marco Normativo Principal

```
┌─────────────────────────────────────────────────────────────────┐
│              NORMATIVA DE SEGURIDAD BANCARIA                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  LEYES PRINCIPALES                                             │
│  ├── Ley 16.874 - Ley del Sistema Financiero                  │
│  ├── Ley 18.331 - Protección de Datos Personales             │
│  ├── Ley 19.670 - Modificación de Protección de Datos        │
│  ├── Ley 19.733 - Prevención del Lavado de Activos           │
│  └── Ley 20.075 - Estrategia de Ciberseguridad Nacional      │
│                                                                 │
│  NORMATIVA BCU                                               │
│  ├── Comunicación 2009/199 - Gestión de Riesgos Tecnológicos   │
│  ├── Comunicación 2012/046 - Seguridad de la Información     │
│  ├── Comunicación 2016/045 - Continuidad del Negocio        │
│  ├── Comunicación 2019/012 - Gestión de Incidentes           │
│  └── Circulares de Gobernanza Corporativa                    │
│                                                                 │
│  CIRCULARES Y COMUNICACIONES                                  │
│  ├── SEGCO - Seguridad y Control                            │
│  ├── IT - Tecnología de Información                         │
│  └── SISTEMAS DE PAGO                                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 1.3. Regulaciones Internacionales Aplicables

```
┌─────────────────────────────────────────────────────────────────┐
│         REGULACIONES INTERNACIONALES APLICABLES                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  BASILEA (Basel III/IV)                                      │
│  ├─ Requisitos de capital                                      │
│  ├─ Gestión de riesgos operativos                            │
│  └─ Riesgo tecnológico                                       │
│                                                                 │
│  PCI-DSS (Payment Card Industry)                             │
│  ├─ Seguridad de datos de tarjetas                            │
│  ├─ Si procesa pagos con tarjeta                             │
│  └─ Requisitos obligatorios para adquirientes               │
│                                                                 │
│  RECOMENDACIONES GAFI                                        │
│  ├─ Prevención de lavado de activos                         │
│  ├─ Identificación de clientes (KYC)                        │
│  └─ Registros y conservación de datos                        │
│                                                                 │
│  ISO/IEC 27001                                              │
│  ├─ Sistema de gestión de seguridad                        │
│  └─ No obligatorio pero recomendado                         │
│                                                                 │
│  NIST CYBERSECURITY FRAMEWORK                                │
│  └─ Marco de referencia para gestión de ciberseguridad    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. SUPERINTENDENCIA DE SERVICIOS FINANCIEROS

### 2.1. Funciones de Supervisión

```
┌─────────────────────────────────────────────────────────────────┐
│         FUNCIONES DE SUPERVISIÓN BCU                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  SUPERVISIÓN ON-SITE                                          │
│  ├─ Inspecciones en dependencias del entidad                  │
│  ├─ Verificación de cumplimiento normativo                   │
│  ├─ Evaluación de controles internos                         │
│  └─ Pruebas de penetración (ocasionalmente)                │
│                                                                 │
│  SUPERVISIÓN OFF-SITE                                        │
│  ├─ Análisis de reportes periódicos                          │
│  ├─ Monitoreo de indicadores                                │
│  ├─ Revisión de estados financieros                        │
│  └─ Seguimiento de plan de acción                           │
│                                                                 │
│  SUPERVISIÓN BASADA EN RIESGO                                │
│  ├─ Priorización según riesgo residual                       │
│  ├─ Frecuencia ajustada al perfil de riesgo                 │
│  └─ Enfoque en áreas de mayor riesgo                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2. Requisitos de Reportes

```python
# ============================================
# REPORTES A BCU - SEGURIDAD
# ============================================

class ReportesBCU:
    """
    Define los reportes de seguridad requeridos por BCU
    """
    
    REPORTES = {
        "trimestral": {
            "nombre": "Informe de Gestión de Riesgos Tecnológicos",
            "contenido": [
                "Resumen de incidentes de seguridad",
                "Métricas de ciberseguridad",
                "Vulnerabilidades identificadas",
                "Acciones correctivas implementadas",
                "Capacitación del personal",
                "Actualizaciones de seguridad"
            ],
            "plazo": "30 días post trimestre",
            "formato": "Nota formal + Anexo estadístico"
        },
        
        "incidentes_mayores": {
            "nombre": "Notificación de Incidentes Significativos",
            "contenido": [
                "Descripción del incidente",
                "Sistemas afectados",
                "Datos comprometidos (si aplica)",
                "Impacto en operaciones",
                "Acciones de contención",
                "Medidas de prevención"
            ],
            "plazo": "24-48 horas (según severidad)",
            "formato": "Comunicación urgente al BCU"
        },
        
        "anual": {
            "nombre": "Informe Anual de Seguridad",
            "contenido": [
                "Resumen ejecutivo",
                "Evaluación de riesgos",
                "Cumplimiento normativo",
                "Inversiones en seguridad",
                "Auditorías realizadas",
                "Certificaciones obtenidas",
                "Plan de mejoras para siguiente período"
            ],
            "plazo": "90 días post cierre ejercicio",
            "formato": "Memoria anual + Anexos técnicos"
        }
    }
    
    def generar_reporte_trimestral(self, datos):
        """Genera template de reporte trimestral"""
        return {
            "encabezado": {
                "entidad": datos["nombre_entidad"],
                "periodo": datos["periodo"],
                "fecha": datetime.now().isoformat()
            },
            "secciones": self.REPORTES["trimestral"]["contenido"],
            "firma": {
                "responsable_seguridad": "",
                "director_tecnologia": "",
                "director_general": ""
            }
        }
    
    def generar_notificacion_incidente(self, incidente):
        """Genera template de notificación de incidente"""
        return {
            "tipo": "NOTIFICACION_INCIDENTE",
            "entidad": incidente["entidad"],
            "fecha_deteccion": incidente["fecha_deteccion"],
            "fecha_notificacion": datetime.now().isoformat(),
            "severidad": incidente["severidad"],
            "descripcion": incidente["descripcion"],
            "sistemas_afectados": incidente["sistemas"],
            "datos_comprometidos": incidente.get("datos", "Ninguno"),
            "impacto_operacional": incidente["impacto"],
            "acciones_inmediatas": incidente["acciones"],
            "medidas_preventivas": incidente["prevencion"]
        }
```

---

## 3. NORMATIVA DE SEGURIDAD DE LA INFORMACIÓN

### 3.1. Principios de Seguridad Bancaria

```
┌─────────────────────────────────────────────────────────────────┐
│              PRINCIPIOS DE SEGURIDAD BANCARIA                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. CONFIDENCIALIDAD                                          │
│     └─ Proteger información sensible de clientes                │
│     └─ Cifrado de datos en tránsito y reposo                 │
│     └─ Control de acceso basado en necesidad de conocer       │
│                                                                 │
│  2. INTEGRIDAD                                                 │
│     └─ Garantizar exactitud de datos financieros              │
│     └─ Prevenir modificación no autorizada                    │
│     └─ Logs de auditoría inmutables                           │
│                                                                 │
│  3. DISPONIBILIDAD                                            │
│     └─ Alta disponibilidad de sistemas críticos              │
│     └─ Continuidad del negocio documentada                     │
│     └─ Recovery Time Objectives (RTO) definidos               │
│                                                                 │
│  4. AUTENTICIDAD                                              │
│     └─ Verificar identidad de usuarios y sistemas              │
│     └─ Autenticación multifactor (MFA)                        │
│     └─ Firmas digitales para operaciones                      │
│                                                                 │
│  5. NO REPUDIO                                                │
│     └─ Registrar transacciones con evidencia                  │
│     └─ Timestamps confiables                                  │
│     └─ Evidencia de aprobación de operaciones                 │
│                                                                 │
│  6. TRAZABILIDAD                                             │
│     └─ Logs de todas las operaciones                        │
│     └─ Auditoría completa de acceso                           │
│     └─ Retention de registros según regulación               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2. Controles de Seguridad Requeridos

```markdown
# CONTROLES DE SEGURIDAD - BCU
## Basado en normativa de Superintendencia de Servicios Financieros

---

## A. CONTROL DE ACCESO

| Control | Requisito | Evidencia |
|---------|-----------|-----------|
| AC-1 | Políticas de acceso documentadas | Política vigente |
| AC-2 | Gestión de usuarios (creación, modificación, eliminación) | Proceso + logs |
| AC-3 | Control de acceso privilegiado | Inventario cuentas privilegiadas |
| AC-4 | Revisión de accesos trimestral | Actas de revisión |
| AC-5 | Separación de funciones | Matriz de segregación |
| AC-6 | Autenticación multifactor | Configuración + uso |

---

## B. SEGURIDAD DE DATOS

| Control | Requisito | Evidencia |
|---------|-----------|-----------|
| DS-1 | Clasificación de información | Inventario de datos |
| DS-2 | Cifrado en reposo | Configuración cifrado |
| DS-3 | Cifrado en tránsito (TLS 1.2+) | Certificados + configuración |
| DS-4 | Respaldo y recuperación | Políticas + verificación |
| DS-5 | Eliminación segura | Procedimiento documentado |

---

## C. GESTIÓN DE RIESGOS

| Control | Requisito | Evidencia |
|---------|-----------|-----------|
| RM-1 | Evaluación de riesgos anual | Documento de evaluación |
| RM-2 | Plan de tratamiento de riesgos | Documento + seguimiento |
| RM-3 | Monitoreo de riesgos | Reportes periódicos |
| RM-4 | Gestión de vulnerabilidades | Inventario + remediación |

---

## D. RESPUESTA A INCIDENTES

| Control | Requisito | Evidencia |
|---------|-----------|-----------|
| IR-1 | Plan de respuesta documentado | Plan vigente |
| IR-2 | Equipo de respuesta identificado | Nombramiento formal |
| IR-3 | Notificación a BCU | Protocolo documentado |
| IR-4 | Pruebas anuales de incidentes | Registros de pruebas |
| IR-5 | lecciones aprendidas | Documentación post-incidente |

---

## E. CONTINUIDAD DEL NEGOCIO

| Control | Requisito | Evidencia |
|---------|-----------|-----------|
| BC-1 | Plan de Continuidad (BCP) | Documento vigente |
| BC-2 | Plan de Recuperación ante Desastres (DRP) | Documento vigente |
| BC-3 | RTO y RPO definidos | Documentación por sistema |
| BC-4 | Pruebas anuales de DRP | Registros de pruebas |
| BC-5 | Sitio de contingencia | Contrato + pruebas |

---

## F. AUDITORÍA

| Control | Requisito | Evidencia |
|---------|-----------|-----------|
| AU-1 | Auditoría interna de seguridad | Planes y reportes |
| AU-2 | Auditoría externa periódica | Informes |
| AU-3 | Cobertura de auditoría | Matriz de sistemas auditeados |
| AU-4 | Retención de logs | Políticas + almacenamiento |
```

---

## 4. REQUISITOS DE CIBERSEGURIDAD

### 4.1. Clasificación de Sistemas

```
┌─────────────────────────────────────────────────────────────────┐
│              CLASIFICACIÓN DE SISTEMAS BANCARIOS                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  CATEGORÍA CRÍTICA (Tier 1)                                   │
│  ├─ Core Banking (núcleo de negocio)                        │
│  ├─ Sistemas de pagos (SPEG, ACH)                            │
│  ├─ ATM/POS (cajeros y puntos de venta)                     │
│  ├─ Canales digitales (home banking, móvil)                   │
│  └─ Datos de clientes (CRM centralizado)                     │
│                                                                 │
│  REQUISITOS TIER 1:                                           │
│  ├─ Disponibilidad 99.99% (max 52 min downtime/año)         │
│  ├─ RTO ≤ 4 horas                                           │
│  ├─ RPO = 0 (sin pérdida de datos)                          │
│  ├─ Redundancia geográfica obligatoria                       │
│  ├─ Pruebas DRP semestrales                                 │
│  └─ Monitoreo 24/7                                          │
│                                                                 │
│  ─────────────────────────────────────────────────────────────  │
│                                                                 │
│  CATEGORÍA IMPORTANTE (Tier 2)                               │
│  ├─ Gestión de riesgos                                        │
│  ├─ Sistemas de reporting regulatorio                        │
│  ├─ Gestión de cajas y sucursales                           │
│  └─ Sistemas de recursos humanos                             │
│                                                                 │
│  REQUISITOS TIER 2:                                          │
│  ├─ Disponibilidad 99.9% (8.7 horas downtime/año)         │
│  ├─ RTO ≤ 24 horas                                          │
│  ├─ RPO ≤ 4 horas                                           │
│  ├─ Backup diario                                             │
│  └─ Pruebas DRP anuales                                     │
│                                                                 │
│  ─────────────────────────────────────────────────────────────  │
│                                                                 │
│  CATEGORÍA SOPORTE (Tier 3)                                  │
│  ├─ Ofimática                                                │
│  ├─ Correo electrónico                                       │
│  ├─ Intranet                                                 │
│  └─ Desarrollo y pruebas                                     │
│                                                                 │
│  REQUISITOS TIER 3:                                          │
│  ├─ Disponibilidad 99% (3.6 días downtime/año)             │
│  ├─ RTO ≤ 72 horas                                          │
│  ├─ RPO ≤ 24 horas                                          │
│  └─ Pruebas DRP según presupuesto                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 4.2. Métricas de Ciberseguridad

```python
class MetricasCiberseguridadBCU:
    """
    Métricas requeridas por normativa BCU
    """
    
    METRICAS = {
        # ============================================
        # GESTIÓN DE ACCESOS
        # ============================================
        "usuarios_totales": {
            "descripcion": "Total de usuarios activos",
            "frecuencia": "mensual",
            "formato": "número"
        },
        "usuarios_privilegiados": {
            "descripcion": "Usuarios con acceso privilegiado",
            "frecuencia": "mensual",
            "formato": "número + % del total"
        },
        "revision_accesos": {
            "descripcion": "Cumplimiento de revisión trimestral",
            "frecuencia": "trimestral",
            "formato": "Sí/No + evidencia"
        },
        
        # ============================================
        # INCIDENTES
        # ============================================
        "incidentes_totales": {
            "descripcion": "Total incidentes de seguridad",
            "frecuencia": "mensual",
            "formato": "número"
        },
        "incidentes_criticos": {
            "descripcion": "Incidentes de severidad crítica",
            "frecuencia": "inmediato + mensual",
            "formato": "número + detalle"
        },
        "tiempo_promedio_deteccion": {
            "descripcion": "MTTD - Mean Time to Detect",
            "frecuencia": "trimestral",
            "formato": "horas"
        },
        "tiempo_promedio_respuesta": {
            "descripcion": "MTTR - Mean Time to Respond",
            "frecuencia": "trimestral",
            "formato": "horas"
        },
        "tiempo_promedio_recuperacion": {
            "descripcion": "MTTR - Mean Time to Recover",
            "frecuencia": "trimestral",
            "formato": "horas"
        },
        
        # ============================================
        # VULNERABILIDADES
        # ============================================
        "vulnerabilidades_criticas_abiertas": {
            "descripcion": "Vulnerabilidades críticas sin remediar",
            "frecuencia": "mensual",
            "formato": "número",
            "umbral": "0 en > 24 horas"
        },
        "vulnerabilidades_altas_abiertas": {
            "descripcion": "Vulnerabilidades altas sin remediar",
            "frecuencia": "mensual",
            "formato": "número",
            "umbral": "< 5 en > 7 días"
        },
        "tiempo_remediacion_criticas": {
            "descripcion": "Tiempo promedio de remediación críticas",
            "frecuencia": "trimestral",
            "formato": "días",
            "umbral": "< 7 días"
        },
        
        # ============================================
        # DISPONIBILIDAD
        # ============================================
        "uptime_critico": {
            "descripcion": "Disponibilidad sistemas críticos",
            "frecuencia": "mensual",
            "formato": "porcentaje",
            "umbral": "> 99.99%"
        },
        "uptime_importante": {
            "descripcion": "Disponibilidad sistemas importantes",
            "frecuencia": "mensual",
            "formato": "porcentaje",
            "umbral": "> 99.9%"
        },
        "incidentes_disponibilidad": {
            "descripcion": "Incidentes que afectan disponibilidad",
            "frecuencia": "mensual",
            "formato": "número"
        },
        
        # ============================================
        # CAPACITACIÓN
        # ============================================
        "personal_capacitado": {
            "descripcion": "% personal capacitado en ciberseguridad",
            "frecuencia": "trimestral",
            "formato": "porcentaje",
            "umbral": "> 90%"
        },
        "simulaciones_phishing": {
            "descripcion": "Tasa de click en simulaciones phishing",
            "frecuencia": "trimestral",
            "formato": "porcentaje",
            "umbral": "< 5%"
        },
        
        # ============================================
        # AUDITORÍA
        # ============================================
        "hallazgos_pendientes": {
            "descripcion": "Hallazgos de auditoría pendientes",
            "frecuencia": "mensual",
            "formato": "número + severidad"
        },
        "pruebas_penetracion": {
            "descripcion": "Ejecución de pruebas de penetración",
            "frecuencia": "anual",
            "formato": "Sí/No + informe"
        }
    }
    
    def generar_dashboard(self):
        """Genera template de dashboard mensual"""
        return {
            "entidad": "",
            "periodo": "",
            "fecha": datetime.now().isoformat(),
            "metricas": {k: {"valor": "", "cumplimiento": ""} 
                         for k in self.METRICAS.keys()}
        }
```

---

## 5. GESTIÓN DE RIESGOS TECNOLÓGICOS

### 5.1. Marco de Gestión de Riesgos

```
┌─────────────────────────────────────────────────────────────────┐
│              GESTIÓN DE RIESGOS TECNOLÓGICOS                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  METODOLOGÍA DE EVALUACIÓN                                     │
│  ─────────────────────────                                     │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              EVALUACIÓN DE RIESGOS                     │   │
│  │                                                         │   │
│  │   PROBABILIDAD × IMPACTO = NIVEL DE RIESGO           │   │
│  │                                                         │   │
│  │   Probabilidad: 1-5                                    │   │
│  │   Impacto: 1-5                                         │   │
│  │                                                         │   │
│  │   ===============================                    │   │
│  │   1-8: Bajo (Aceptable)                              │   │
│  │   9-14: Medio (Mitigar)                              │   │
│  │   15-25: Alto (Requerir tratamiento)                  │   │
│  │                                                         │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  TIPOS DE RIESGOS                                              │
│  ───────────────                                                │
│  ├─ Riesgo Operativo (fallas tecnológicas, errores humanos)  │
│  ├─ Riesgo de Ciberseguridad (ataques, malware, ransomware) │
│  ├─ Riesgo de Incumplimiento (no comply with regulations)  │
│  ├─ Riesgo de Reputación (publicidad negativa)           │
│  ├─ Riesgo de Continuidad (interrupción de servicios)     │
│  └─ Riesgo de Terceros (proveedores, outsourcing)        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 5.2. Matriz de Riesgos

```python
class MatrizRiesgosBCU:
    """
    Matriz de riesgos tecnológicos según BCU
    """
    
    # Escala de probabilidad
    PROBABILIDAD = {
        1: "Muy baja (evento improbable)",
        2: "Baja (poco probable)",
        3: "Media (posible)",
        4: "Alta (probable)",
        5: "Muy alta (casi seguro)"
    }
    
    # Escala de impacto
    IMPACTO = {
        1: "Muy bajo (reporte menor)",
        2: "Bajo (impacto local, menor)",
        3: "Medio (impacto en área, manejable)",
        4: "Alto (impacto significativo en negocio)",
        5: "Muy alto (crítico, podría cerrar operaciones)"
    }
    
    # Matriz combinada
    MATRIZ = {
        # Probabilidad x Impacto
        (1, 1): {"nivel": "Bajo", "color": "verde"},
        (1, 2): {"nivel": "Bajo", "color": "verde"},
        (1, 3): {"nivel": "Bajo", "color": "verde"},
        (1, 4): {"nivel": "Medio", "color": "amarillo"},
        (1, 5): {"nivel": "Medio", "color": "amarillo"},
        
        (2, 1): {"nivel": "Bajo", "color": "verde"},
        (2, 2): {"nivel": "Bajo", "color": "verde"},
        (2, 3): {"nivel": "Medio", "color": "amarillo"},
        (2, 4): {"nivel": "Medio", "color": "amarillo"},
        (2, 5): {"nivel": "Alto", "color": "naranja"},
        
        (3, 1): {"nivel": "Bajo", "color": "verde"},
        (3, 2): {"nivel": "Medio", "color": "amarillo"},
        (3, 3): {"nivel": "Medio", "color": "amarillo"},
        (3, 4): {"nivel": "Alto", "color": "naranja"},
        (3, 5): {"nivel": "Alto", "color": "rojo"},
        
        (4, 1): {"nivel": "Medio", "color": "amarillo"},
        (4, 2): {"nivel": "Medio", "color": "amarillo"},
        (4, 3): {"nivel": "Alto", "color": "naranja"},
        (4, 4): {"nivel": "Alto", "color": "rojo"},
        (4, 5): {"nivel": "Crítico", "color": "rojo"},
        
        (5, 1): {"nivel": "Medio", "color": "amarillo"},
        (5, 2): {"nivel": "Alto", "color": "naranja"},
        (5, 3): {"nivel": "Alto", "color": "naranja"},
        (5, 4): {"nivel": "Crítico", "color": "rojo"},
        (5, 5): {"nivel": "Crítico", "color": "rojo"}
    }
    
    def evaluar_riesgo(self, probabilidad, impacto):
        """Evalúa el nivel de riesgo"""
        return self.MATRIZ.get((probabilidad, impacto))
    
    def generar_plan_tratamiento(self, riesgo):
        """Genera plan de tratamiento según nivel"""
        planes = {
            "Bajo": "Aceptar con monitoreo",
            "Medio": "Mitigar con controles compensatorios",
            "Alto": "Mitigar urgentemente + plan de contingencia",
            "Crítico": "Escalar a directorio + tratamiento inmediato"
        }
        return planes.get(riesgo["nivel"])


# Ejemplo de uso
matriz = MatrizRiesgosBCU()

# Riesgo: Ataque ransomware
resultado = matriz.evaluar_riesgo(probabilidad=4, impacto=5)
print(f"Riesgo ransomware: {resultado['nivel']} ({resultado['color']})")
# Salida: Riesgo ransomware: Crítico (rojo)

# Plan de tratamiento
tratamiento = matriz.generar_plan_tratamiento(resultado)
print(f"Tratamiento: {tratamiento}")
# Salida: Tratamiento: Escalar a directorio + tratamiento inmediato
```

---

## 6. CONTINUIDAD DEL NEGOCIO

### 6.1. Requisitos de Continuidad

```
┌─────────────────────────────────────────────────────────────────┐
│              CONTINUIDAD DEL NEGOCIO BANCARIO                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  DOCUMENTACIÓN REQUERIDA                                        │
│  ───────────────────────────                                   │
│                                                                 │
│  PLAN DE CONTINUIDAD DEL NEGOCIO (BCP)                          │
│  ├─ Alcance y objetivos                                       │
│  ├─ Análisis de impacto en el negocio (BIA)                   │
│  ├─ Roles y responsabilidades                                 │
│  ├─ Procedimientos de activación                              │
│  ├─ Comunicación y notificaciones                             │
│  └─ Pruebas y mantenimiento                                  │
│                                                                 │
│  PLAN DE RECUPERACIÓN ante Desastres (DRP)                      │
│  ├─ Sistemas críticos priorizados                              │
│  ├─ RTO y RPO definidos por sistema                           │
│  ├─ Procedimientos de recuperación                            │
│  ├─ Sitio alternativo                                        │
│  └─ Arreglos con proveedores                                 │
│                                                                 │
│  ANÁLISIS DE IMPACTO (BIA)                                      │
│  ├─ Procesos de negocio críticos                              │
│  ├─ Tiempo máximo tolerable de interrupción (MTPD)            │
│  ├─ Recursos necesarios para recuperación                     │
│  └─ Dependencias identificadas                                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 6.2. Tiempos de Recuperación

```python
class TiemposRecuperacion:
    """
    Define tiempos de recuperación requeridos por BCU
    """
    
    # Clasificación de sistemas y RTO/RPO
    CLASIFICACION = {
        "critico": {
            "descripcion": "Sistemas que procesan transacciones financieras",
            "ejemplos": [
                "Core Banking",
                "Sistemas de pagos (ACH, SPEG)",
                "ATM/POS",
                "Home Banking"
            ],
            "rto": "4 horas",  # Recovery Time Objective
            "rpo": "0 horas",  # Recovery Point Objective
            "disponibilidad": "99.99%",
            "pruebas": "semestrales"
        },
        "importante": {
            "descripcion": "Sistemas de soporte al negocio",
            "ejemplos": [
                "Gestión de riesgos",
                "Reporting regulatorio",
                "Gestión desucursales"
            ],
            "rto": "24 horas",
            "rpo": "4 horas",
            "disponibilidad": "99.9%",
            "pruebas": "anuales"
        },
        "soporte": {
            "descripcion": "Sistemas administrativos",
            "ejemplos": [
                "Correo electrónico",
                "Ofimática",
                "Intranet"
            ],
            "rto": "72 horas",
            "rpo": "24 horas",
            "disponibilidad": "99%",
            "pruebas": "bianuales"
        }
    }
    
    def generar_tabla_rto_rpo(self):
        """Genera tabla de RTO/RPO por sistema"""
        tabla = []
        for nivel, config in self.CLASIFICACION.items():
            tabla.append({
                "nivel": nivel.upper(),
                "descripcion": config["descripcion"],
                "rto": config["rto"],
                "rpo": config["rpo"],
                "disponibilidad": config["disponibilidad"],
                "pruebas": config["pruebas"]
            })
        return tabla
    
    def verificar_cumplimiento(self, sistema):
        """Verifica si un sistema cumple con RTO/RPO"""
        nivel = sistema["nivel"]
        config = self.CLASIFICACION[nivel]
        
        return {
            "sistema": sistema["nombre"],
            "nivel": nivel,
            "rto_requerido": config["rto"],
            "rto_actual": sistema["rto_actual"],
            "cumple_rto": self.comparar_tiempo(
                sistema["rto_actual"], 
                config["rto"]
            ),
            "rpo_requerido": config["rpo"],
            "rpo_actual": sistema["rpo_actual"],
            "cumple_rpo": self.comparar_tiempo(
                sistema["rpo_actual"], 
                config["rpo"]
            )
        }
    
    def comparar_tiempo(self, actual, requerido):
        """Compara tiempos de recuperación"""
        # Simplificado - en producción usar conversión a horas
        return actual <= requerido


# Ejemplo de uso
tiempos = TiemposRecuperacion()

# Mostrar requisitos
tabla = tiempos.generar_tabla_rto_rpo()
print("\nREQUISITOS DE RTO/RPO - BCU")
print("=" * 80)
for item in tabla:
    print(f"\n{item['nivel']}: {item['descripcion']}")
    print(f"  RTO: {item['rto']} | RPO: {item['rpo']} | Disponibilidad: {item['disponibilidad']}")
```

---

## 7. PROTECCIÓN DE DATOS DEL CLIENTE

### 7.1. Datos Personales en Banca

```
┌─────────────────────────────────────────────────────────────────┐
│              DATOS PERSONALES EN EL SECTOR BANCARIO                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  DATOS IDENTIFICADORES                                          │
│  ├─ Nombre completo                                            │
│  ├─ Cédula de identidad                                       │
│  ├─ Fecha y lugar de nacimiento                               │
│  ├─ Estado civil                                              │
│  └─ Fotografía                                                │
│                                                                 │
│  DATOS DE CONTACTO                                             │
│  ├─ Dirección                                                 │
│  ├─ Teléfono                                                  │
│  ├─ Email                                                     │
│  └─ Redes sociales (si aplica)                                │
│                                                                 │
│  DATOS FINANCIEROS (sensibles)                                 │
│  ├─ Cuentas bancarias                                         │
│  ├─ Saldos y movimientos                                      │
│  ├─ Historial crediticio                                      │
│  ├─ Bienes y propiedades                                      │
│  ├─ Ingresos y egresos                                        │
│  └─ Préstamos y deudas                                        │
│                                                                 │
│  DATOS DE TRANSPARENCIA FISCAL                                 │
│  ├─ País de residencia fiscal                                  │
│  ├─ TIN/NIF extranjero                                        │
│  └─ Actividades económicas                                    │
│                                                                 │
│  DATOS DE COMPORTAMIENTO                                       │
│  ├─ Hábitos de consumo                                        │
│  ├─ Preferencias de canales                                   │
│  └─ Análisis de scoring                                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 7.2. Implementación de Controles

```python
class ProteccionDatosBancarios:
    """
    Controles de protección de datos según BCU y Ley 18.331
    """
    
    def __init__(self):
        self.controles_requeridos = {
            # Confidencialidad
            "CIFRADO_ENCEST": {
                "descripcion": "Cifrado de datos sensibles en reposo",
                "tecnologia": ["AES-256", "TDE"],
                "alcance": ["Bases de datos", "Archivos"],
                "evidencia": "Configuración + keys management"
            },
            "CIFRADO_TRANSITO": {
                "descripcion": "Cifrado de datos en tránsito",
                "tecnologia": ["TLS 1.2+", "SSH"],
                "alcance": ["APIs", "Web", "Email"],
                "evidencia": "Certificados + configuración"
            },
            
            # Control de acceso
            "RBAC": {
                "descripcion": "Control de acceso basado en roles",
                "implementacion": "Matriz de permisos por rol",
                "evidencia": "Documentación + pruebas"
            },
            "MFA": {
                "descripcion": "Autenticación multifactor",
                "alcance": ["Acceso a sistemas internos", "Canales digitales"],
                "evidencia": "Configuración + logs de uso"
            },
            
            # Registro y auditoría
            "AUDITORIA": {
                "descripcion": "Logs de auditoría",
                "elementos": [
                    "Usuario",
                    "Fecha/hora",
                    "Acción",
                    "Recurso",
                    "Resultado"
                ],
                "retention": "5 años mínimo",
                "evidencia": "Logs + análisis de acceso"
            },
            
            # Tokenización
            "TOKENIZACION": {
                "descripcion": "Tokenización de datos de tarjetas",
                "estandar": "PCI-DSS",
                "evidencia": "Implementación + certificaciones"
            }
        }
    
    def generar_checklist(self):
        """Genera checklist de cumplimiento"""
        return {
            control: {
                "estado": "Pendiente",
                "evidencia": "",
                "fecha_implementacion": None,
                "responsable": ""
            }
            for control in self.controles_requeridos.keys()
        }
```

---

## 8. INCIDENTES Y NOTIFICACIONES

### 8.1. Clasificación de Incidentes

```
┌─────────────────────────────────────────────────────────────────┐
│              CLASIFICACIÓN DE INCIDENTES - BCU                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  SEVERIDAD CRÍTICA (Notificación inmediata)                     │
│  ├─ Brecha de datos de clientes                               │
│  ├─ Compromiso de sistemas de pagos                           │
│  ├─ Ransomware que afecta operaciones                        │
│  ├─ Fraude masivo                                            │
│  └─ Falla de sistemas críticos > 4 horas                     │
│                                                                 │
│  Tiempo de notificación: 24 horas                             │
│  Canal: Comunicación directa a Superintendencia                │
│                                                                 │
│  ─────────────────────────────────────────────────────────────  │
│                                                                 │
│  SEVERIDAD ALTA (Notificación en 48 horas)                    │
│  ├─ Intento de acceso no autorizado                          │
│  ├─ Malware detectado en sistemas                             │
│  ├─ Falla de redundancia                                    │
│  ├─ Compromiso de credenciales privilegiadas                 │
│  └─ Incidente en sistemas de terceros críticos                 │
│                                                                 │
│  Tiempo de notificación: 48 horas                             │
│  Canal: Reporte formal                                       │
│                                                                 │
│  ─────────────────────────────────────────────────────────────  │
│                                                                 │
│  SEVERIDAD MEDIA (Notificación mensual)                       │
│  ├─ Violación de políticas internas                          │
│  ├─ Incidentes menores de disponibilidad                     │
│  ├─ Alertas de seguridad no materializadas                   │
│  └─ Fallas de controles                                      │
│                                                                 │
│  Tiempo de notificación: Reporte mensual                      │
│  Canal: Reporte trimestral                                  │
│                                                                 │
│  ─────────────────────────────────────────────────────────────  │
│                                                                 │
│  SEVERIDAD BAJA (Registro interno)                            │
│  ├─ Eventos de log sospechosos                               │
│  ├─ Violaciones menores de seguridad                         │
│  └─ Mejores prácticas identificadas                          │
│                                                                 │
│  Registro: Interno + métricas                                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 8.2. Template de Notificación

```markdown
# NOTIFICACIÓN DE INCIDENTE DE SEGURIDAD
## Banco/Institución: [NOMBRE]
## Fecha de Notificación: [FECHA]

---

## 1. IDENTIFICACIÓN DEL INCIDENTE

| Campo | Descripción |
|-------|-------------|
| ID Incidente | [Código interno] |
| Fecha de Detección | [Fecha] |
| Fecha de Inicio (estimada) | [Fecha] |
| Severidad | [Crítica/Alta/Media/Baja] |
| Categoría | [Tipo de incidente] |

---

## 2. DESCRIPCIÓN DEL INCIDENTE

[Descripción detallada del incidente]

---

## 3. SISTEMAS Y DATOS AFECTADOS

### Sistemas Afectados
| Sistema | Criticidad | Impacto |
|---------|------------|---------|
| | | |

### Datos Comprometidos (si aplica)
| Tipo de Dato | Cantidad Estimada | Propietarios |
|--------------|------------------|--------------|
| | | |

---

## 4. IMPACTO

| Aspecto | Descripción | Magnitud |
|---------|-------------|----------|
| Operacional | | |
| Financiero | | |
| Reputacional | | |
| Legal | | |

---

## 5. ACCIONES DE CONTENCIÓN

[Pasos tomados para contener el incidente]

---

## 6. MEDIDAS DE RECUPERACIÓN

[Acciones para restaurar sistemas]

---

## 7. PREVENCIÓN DE RECURRENCIA

[Medidas para evitar que ocurra nuevamente]

---

## 8. CONTACTOS

| Rol | Nombre | Teléfono | Email |
|-----|--------|----------|-------|
| Responsable Seguridad | | | |
| CTO/CIO | | | |
| DPO | | | |
| CEO | | | |

---

## 9. ANEXOS

- [ ] Logs relevantes
- [ ] Evidencia forense
- [ ] Cronología del incidente
- [ ] Impacto cuantificado
```

---

## 9. AUDITORÍA Y COMPLIANCE

### 9.1. Marco de Auditoría

```
┌─────────────────────────────────────────────────────────────────┐
│              AUDITORÍA DE SEGURIDAD BANCARIA                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  AUDITORÍA INTERNA                                             │
│  ├─ Evaluación anual de controles de seguridad                │
│  ├─ Pruebas de penetración                                   │
│  ├─ Revisión de configuraciones                              │
│  ├─ Auditoría de acceso y privilegiados                      │
│  └─ Verificación de continuidad                               │
│                                                                 │
│  AUDITORÍA EXTERNA                                             │
│  ├─ Revisión anual por firma de auditoría                    │
│  ├─ Certificación ISO 27001 (recomendada)                   │
│  ├─ Evaluación PCI-DSS (si procesa tarjetas)                │
│  └─ Auditoría de terceros críticos                           │
│                                                                 │
│  FRECUENCIA DE EVALUACIONES                                   │
│  ├─ Continuous monitoring (monitoreo continuo)                │
│  ├─ Revisiones trimestrales de métricas                      │
│  ├─ Auditoría anual de seguridad                             │
│  └─ Pruebas de penetración anuales                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 9.2. Checklist de Compliance BCU

```markdown
# CHECKLIST DE COMPLIANCE - SEGURIDAD BCU

## GOBERNANZA
- [ ] Políticas de seguridad aprobadas por directorio
- [ ] CISO o responsable de seguridad identificado
- [ ] Comité de seguridad funcionando
- [ ] Presupuesto de seguridad asignado
- [ ] Plan de capacitación ejecutado

## GESTIÓN DE RIESGOS
- [ ] Evaluación de riesgos tecnológicos anual
- [ ] Matriz de riesgos documentada
- [ ] Planes de tratamiento implementados
- [ ] Monitoreo de riesgos continuo

## CONTROL DE ACCESO
- [ ] Políticas de acceso documentadas
- [ ] Gestión de identidades implementada
- [ ] MFA en sistemas críticos
- [ ] Revisión trimestral de accesos
- [ ] Cuentas privilegiadas gestionadas

## SEGURIDAD DE DATOS
- [ ] Clasificación de información
- [ ] Cifrado en reposo
- [ ] Cifrado en tránsito
- [ ] Gestión de claves
- [ ] Backup verificado

## CONTINUIDAD
- [ ] BCP documentado y aprobado
- [ ] DRP documentado
- [ ] Sitio alternativo configurado
- [ ] Pruebas de DRP ejecutadas
- [ ] RTO/RPO documentados por sistema

## INCIDENTES
- [ ] Plan de respuesta documentado
- [ ] Equipo de respuesta identificado
- [ ] Protocolo de notificación a BCU
- [ ] Pruebas de respuesta a incidentes
- [ ] Registro de incidentes mantenido

## AUDITORÍA
- [ ] Auditoría interna de seguridad
- [ ] Hallazgos remediados
- [ ] Certificaciones vigentes
- [ ] Cumplimiento PCI-DSS (si aplica)
```

---

## 10. GUÍA DE IMPLEMENTACIÓN

### 10.1. Plan de Acción

```
┌─────────────────────────────────────────────────────────────────┐
│              PLAN DE IMPLEMENTACIÓN - BCU                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  FASE 1: FUNDAMENTOS (Meses 1-3)                              │
│  ───────────────────────────────                               │
│  □ Designar responsable de seguridad (CISO)                  │
│  □ Aprobar políticas de seguridad                              │
│  □ Crear comité de seguridad                                   │
│  □ Definir estructura de gobernanza                            │
│  □ Establecer presupuesto                                     │
│                                                                 │
│  FASE 2: EVALUACIÓN (Meses 4-6)                             │
│  ──────────────────────────                                   │
│  □ Evaluación de riesgos tecnológicos                           │
│  □ Inventario de activos y sistemas                           │
│  □ Evaluación de controles actuales                             │
│  □ Gap analysis vs requisitos BCU                              │
│  □ Priorización de acciones                                   │
│                                                                 │
│  FASE 3: FORTALECIMIENTO (Meses 7-12)                      │
│  ───────────────────────────────────                          │
│  □ Implementar controles críticos                              │
│  □ Mejorar gestión de identidades                             │
│  □ Implementar MFA                                          │
│  □ Fortalecer monitoreo                                      │
│  □ Actualizar BCP y DRP                                      │
│                                                                 │
│  FASE 4: MADUREZ (Año 2+)                                   │
│  ──────────────────────                                       │
│  □ Mejorar continuo basado en métricas                       │
│  □ Buscar certificaciones (ISO 27001)                        │
│  □ Optimizar procesos                                        │
│  □ Integrar seguridad en desarrollo                          │
│  □ Participación en ejercicios sectoriales                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 11. PLANTILLAS Y CHECKLIST

### 11.1. Reporte Trimestral BCU

```python
class ReporteTrimestralBCU:
    """
    Genera template de reporte trimestral para BCU
    """
    
    def __init__(self, entidad, periodo):
        self.entidad = entidad
        self.periodo = periodo
        self.secciones = []
    
    def agregar_seccion(self, titulo, contenido):
        self.secciones.append({"titulo": titulo, "contenido": contenido})
    
    def generar_template(self):
        return {
            "encabezado": {
                "entidad": self.entidad,
                "periodo": self.periodo,
                "fecha": datetime.now().isoformat(),
                "elaborado_por": "",
                "aprobado_por": ""
            },
            "secciones": [
                {
                    "titulo": "1. GESTIÓN DE RIESGOS",
                    "contenido": {
                        "evaluacion_riesgos": "",
                        "incidentes_significativos": [],
                        "vulnerabilidades_criticas": [],
                        "acciones_correctivas": []
                    }
                },
                {
                    "titulo": "2. CONTROL DE ACCESO",
                    "contenido": {
                        "usuarios_privilegiados": "",
                        "revision_accesos": "",
                        "incidentes_acceso": []
                    }
                },
                {
                    "titulo": "3. SEGURIDAD DE DATOS",
                    "contenido": {
                        "incidentes_datos": [],
                        "cumplimiento_18331": "",
                        "medidas_implementadas": []
                    }
                },
                {
                    "titulo": "4. CONTINUIDAD",
                    "contenido": {
                        "pruebas_bcp": "",
                        "pruebas_drp": "",
                        "incidentes_disponibilidad": []
                    }
                },
                {
                    "titulo": "5. CAPACITACIÓN",
                    "contenido": {
                        "capacitaciones_realizadas": [],
                        "metricas_phishing": "",
                        "personal_capacitado": ""
                    }
                },
                {
                    "titulo": "6. AUDITORÍA",
                    "contenido": {
                        "hallazgos_pendientes": [],
                        "acciones_remediacion": [],
                        "proxima_auditoria": ""
                    }
                }
            ],
            "firma_responsable_seguridad": "",
            "firma_director_tecnologia": "",
            "firma_director_general": ""
        }
```

---

**Documento:** Seguridad Bancaria - BCU Uruguay  
**Versión:** 1.0  
**Última actualización:** 2026  
**Referencia:** Superintendencia de Servicios Financieros - BCU
