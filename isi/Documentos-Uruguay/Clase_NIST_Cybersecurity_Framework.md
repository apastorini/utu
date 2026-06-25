# NIST CYBERSECURITY FRAMEWORK (CSF) - GUÍA COMPLETA

---

## ÍNDICE

1. Introducción al NIST CSF
2. Historia y Evolución
3. Conceptos Fundamentales
4. Las 5 Funciones Core
5. Categorías y Subcategorías
6. Niveles de Implementación (Tiers)
7. Perfiles (Profiles)
8. Implementación Tiers
9. Proceso de Medición
10. Relación con Otros Marcos
11. Guía de Implementación
12. Herramientas y Recursos
13. Ejemplos Prácticos

---

## 1. INTRODUCCIÓN AL NIST CSF

### 1.1. ¿Qué es el NIST Cybersecurity Framework?

```
┌─────────────────────────────────────────────────────────────────┐
│                NIST CYBERSECURITY FRAMEWORK                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  AUTOR: National Institute of Standards and Technology         │
│         (Instituto Nacional de Estándares y Tecnología)        │
│         - EE.UU. Department of Commerce                        │
│                                                                 │
│  PROPÓSITO:                                                    │
│  Proporcionar un marco común para que organizaciones          │
│  puedan entender, gestionar y comunicar riesgos             │
│  de ciberseguridad                                            │
│                                                                 │
│  CARACTERÍSTICAS PRINCIPALES:                                   │
│  ✓ Enfoque basado en riesgos                                 │
│  ✓ Vocabulario común para ciberseguridad                     │
│  ✓ Flexible y escalable                                      │
│  ✓ Orientado a бизнес                                        │
│  ✓ No es mandatorio ni regulatorio por sí solo               │
│  ✓ Adaptable a cualquier organización                        │
│                                                                 │
│  VERSIÓN ACTUAL: 2.0 (2024)                                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2. ¿Por qué fue creado?

```
┌─────────────────────────────────────────────────────────────────┐
│                 ANTECEDENTES DEL NIST CSF                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  2013 - Orden Ejecutiva 13636                                 │
│  └─ Presidente Obama ordena crear marco de ciberseguridad    │
│                                                                 │
│  2014 - NIST CSF versión 1.0                                  │
│  └─ Resultado de colaboración con industria                 │
│  └─ Público y voluntario                                     │
│                                                                 │
│  2017 - NIST CSF versión 1.1                                  │
│  └─ Mejoras basadas en feedback                              │
│  └─ Énfasis en medición y métricas                           │
│                                                                 │
│  2024 - NIST CSF versión 2.0                                  (ACTUAL)│
│  └─ Actualización integral                                   │
│  └─ Nuevos perfiles sectoriales                              │
│  └─ Mayor énfasis en gobernanza                              │
│  └─ Integration con privacy                                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 1.3. Principios Clave

```
┌─────────────────────────────────────────────────────────────────┐
│                 PRINCIPIOS CLAVE DEL NIST CSF                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. ENFOQUE EN NEGOCIOS                                       │
│     └─ Riegos priorizados según impacto en negocio           │
│                                                                 │
│  2. FLEXIBILIDAD                                             │
│     └─ Aplicables a cualquier tipo de organización           │
│     └─ Cualquier tamaño o sector                             │
│                                                                 │
│  3. VOLUNTARIO                                                │
│     └─ No es mandatorio                                       │
│     └─ Cada organización adapta a sus necesidades           │
│                                                                 │
│  4. BASADO EN ESTÁNDARES EXISTENTES                          │
│     └─ No reinventa la rueda                                 │
│     └─ Integra ISO 27001, COBIT, NIST SP 800-53, etc.      │
│                                                                 │
│  5. ENFOQUE EN RIESGOS                                        │
│     └─ Comunicación de riesgos                               │
│     └─ Priorización según impacto                           │
│                                                                 │
│  6. MEJORA CONTINUA                                          │
│     └─ Ciclos de evaluación y mejora                         │
│                                                                 │
│  7. MEDICIÓN Y ACCOUNTABILITY                                │
│     └─ Métricas para evaluar efectividad                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. HISTORIA Y EVOLUCIÓN

### 2.1. Timeline del NIST CSF

```
TIMELINE NIST CYBERSECURITY FRAMEWORK
═══════════════════════════════════════════════════════════════

2013              2014              2017              2024
  │                │                │                │
  ▼                ▼                ▼                ▼
┌──────┐      ┌──────┐      ┌──────┐      ┌──────┐
│ EO   │      │ v1.0 │      │ v1.1 │      │ v2.0 │ (ACTUAL)
│13636 │ ───► │      │ ───► │      │ ───► │      │
└──────┘      └──────┘      └──────┘      └──────┘
                  │                │                │
                  ▼                ▼                ▼
              Lanzamiento      Mejoras           Nueva
              inicial          de contenido    versión
                              + Medición
```

### 2.2. Cambios de v1.1 a v2.0

| Aspecto | v1.1 | v2.0 |
|---------|------|------|
| **Estructura** | 5 funciones, 23 categorías | Igual + más orientación |
| **Perfiles** | Básicos | Más ejemplos sectoriales |
| **Privacidad** | Implícito | Explícito e integrado |
| **Gobernanza** | Mención | Sección dedicada |
| **Medición** | Informativo |Framework de medición unificado |
| **Suministro** | Mínimo | Gestión de cadena de suministro expandida |

---

## 3. CONCEPTOS FUNDAMENTALES

### 3.1. Arquitectura del Marco

```
┌─────────────────────────────────────────────────────────────────┐
│           ARQUITECTURA DEL NIST CYBERSECURITY FRAMEWORK           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│                    ┌─────────────────┐                         │
│                    │   TIER (Nivel) │                         │
│                    │   Implementación│                         │
│                    └────────┬────────┘                         │
│                             │                                   │
│         ┌───────────────────┼───────────────────┐               │
│         │                   │                   │               │
│         ▼                   ▼                   ▼               │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐         │
│  │   FUNCIONES │    │  CATEGORÍAS  │    │SUBCATEGORÍAS│        │
│  │  (5 core)   │───►│   (23)       │───►│  (106)       │       │
│  └─────────────┘    └─────────────┘    └──────┬────────┘       │
│                                                │                 │
│                                                ▼                 │
│                                         ┌─────────────┐        │
│                                         │  PERFILES   │        │
│                                         │(Current/New)│        │
│                                         └─────────────┘        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2. Elementos del Marco

| Elemento | Descripción | Ejemplo |
|----------|-------------|---------|
| **Función** | Categoría de nivel superior | PROTECT |
| **Categoría** | Grupo de resultados desejados | PR.AC (Access Control) |
| **Subcategoría** | Resultado específico y medible | PR.AC-1: Identities managed |
| **Nivel (Tier)** | Nivel de implementación | Tier 3: Repeatable |
| **Perfil (Profile)** | Estado actual vs objetivo | Banking Profile v2.0 |

---

## 4. LAS 5 FUNCIONES CORE

### 4.1. Vista General

```
┌─────────────────────────────────────────────────────────────────┐
│              LAS 5 FUNCIONES DEL NIST CSF v2.0                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐   │
│  │                                                           │   │
│  │  IDENTIFY (ID)                                           │   │
│  │  "Lo que necesito proteger"                              │   │
│  │                                                           │   │
│  │  • Gestión de activos                                   │   │
│  │  • Gobernanza                                           │   │
│  │  • Evaluación de riesgos                                │   │
│  │  • Estrategia de riesgos                                │   │
│  │  • Gestión de cadena de suministro                      │   │
│  │                                                           │   │
│  └───────────────────────────────────────────────────────────┘   │
│                            │                                     │
│                            ▼                                     │
│  ┌───────────────────────────────────────────────────────────┐   │
│  │                                                           │   │
│  │  PROTECT (PR)                                            │   │
│  │  "Cómo lo protejo"                                       │   │
│  │                                                           │   │
│  │  • Gestión de identidades y acceso                      │   │
│  │  • Concienciación y formación                            │   │
│  │  • Seguridad de datos                                    │   │
│  │  • Plataformas y tecnologías                             │   │
│  │  • Infraestructura resiliente                           │   │
│  │  • Tecnologías de protección                            │   │
│  │                                                           │   │
│  └───────────────────────────────────────────────────────────┘   │
│                            │                                     │
│                            ▼                                     │
│  ┌───────────────────────────────────────────────────────────┐   │
│  │                                                           │   │
│  │  DETECT (DE)                                             │   │
│  │  "Cómo sé que fui atacado"                               │   │
│  │                                                           │   │
│  │  • Anomalías y eventos                                  │   │
│  │  • Continuous monitoring                                │   │
│  │  • Tecnologías de detección                              │   │
│  │                                                           │   │
│  └───────────────────────────────────────────────────────────┘   │
│                            │                                     │
│                            ▼                                     │
│  ┌───────────────────────────────────────────────────────────┐   │
│  │                                                           │   │
│  │  RESPOND (RS)                                            │   │
│  │  "Qué hago cuando fui atacado"                            │   │
│  │                                                           │   │
│  │  • Planificación de respuesta                            │   │
│  │  • Comunicaciones                                        │   │
│  │  • Análisis                                               │   │
│  │  • Mitigación                                            │   │
│  │  • Mejoras                                               │   │
│  │                                                           │   │
│  └───────────────────────────────────────────────────────────┘   │
│                            │                                     │
│                            ▼                                     │
│  ┌───────────────────────────────────────────────────────────┐   │
│  │                                                           │   │
│  │  RECOVER (RC)                                            │   │
│  │  "Cómo restauro las operaciones"                          │   │
│  │                                                           │   │
│  │  • Planificación de recuperación                         │   │
│  │  • Mejoras                                               │   │
│  │  • Comunicaciones                                        │   │
│  │  • Servicios                                             │   │
│  │                                                           │   │
│  └───────────────────────────────────────────────────────────┘   │
│                                                                 │
│  Las funciones operan de forma CÍCLICA e INTEGRADA              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 4.2. Detalle de Cada Función

#### FUNCIÓN 1: IDENTIFY (ID)

```
┌─────────────────────────────────────────────────────────────────┐
│                    FUNCIÓN: IDENTIFY                              │
│                    "Desarrollar comprensión organizacional"        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  PROPÓSITO:                                                    │
│  Ayudar a la organización a comprender y priorizar              │
│  sus activos, negocio, gobernanza y riesgos de ciberseguridad  │
│                                                                 │
│  CATEGORÍAS:                                                  │
│                                                                 │
│  ID.AM - Gestión de Activos (Asset Management)                  │
│  └─ Identificar dispositivos, software, datos y servicios       │
│  └─ Inventarios completos y actualizados                        │
│                                                                 │
│  ID.BE - Gobernanza (Business Environment)                      │
│  └─ Comprender la misión y objetivos                            │
│  └─ Identificar requisitos legales y regulatorios                │
│  └─ Definir roles de ciberseguridad                           │
│                                                                 │
│  ID.GV - Gobernanza (Governance)                                │
│  └─ Políticas y procedimientos de seguridad                    │
│  └─ Oversight de ciberseguridad                                │
│  └─ Cumplimiento regulatorio                                   │
│                                                                 │
│  ID.RA - Evaluación de Riesgos (Risk Assessment)                 │
│  └─ Identificar amenazas                                        │
│  └─ Identificar vulnerabilidades                                │
│  └─ Análisis de impacto y probabilidad                        │
│  └─ Priorización de riesgos                                   │
│                                                                 │
│  ID.RM - Estrategia de Riesgos (Risk Management Strategy)        │
│  └─ Tolerancia al riesgo definida                              │
│  └─ Proceso de gestión de riesgos documentado                  │
│                                                                 │
│  ID.SC - Gestión de Riesgos de Cadena de Suministro (SC)       │
│  └─ Proveedores identificados y evaluados                      │
│  └─ Requisitos de seguridad en contratos                       │
│  └─ Monitoreo de riesgos de terceros                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### FUNCIÓN 2: PROTECT (PR)

```
┌─────────────────────────────────────────────────────────────────┐
│                    FUNCIÓN: PROTECT                               │
│                    "Desarrollar e implementar safeguards"         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  PROPÓSITO:                                                    │
│  Desarrollar e implementar safeguards apropiados                 │
│  para garantizar la entrega de servicios críticos                 │
│                                                                 │
│  CATEGORÍAS:                                                  │
│                                                                 │
│  PR.AC - Gestión de Identidades y Acceso (Identity & Access)     │
│  └─ Políticas de acceso                                       │
│  └─ Gestión de identidades                                     │
│  └─ Control de acceso (físico y lógico)                       │
│  └─ Autenticación robusta (MFA)                                │
│  └─ Cuentas privilegiadas                                     │
│                                                                 │
│  PR.AT - Concienciación y Formación (Awareness & Training)       │
│  └─ Personal consciente de ciberseguridad                       │
│  └─ Roles privilegiados entrenados                            │
│  └─ Simulaciones de phishing                                   │
│                                                                 │
│  PR.DS - Seguridad de Datos (Data Security)                    │
│  └─ Clasificación de información                               │
│  └─ Protección en tránsito y en reposo                       │
│  └─ Gestión del ciclo de vida de datos                        │
│  └─ Eliminación segura                                         │
│                                                                 │
│  PR.IP - Tecnología de Protección (Information Protection)       │
│  └─ Configuraciones seguras de sistemas                       │
│  └─ Gestión de vulnerabilidades                                │
│  └─ Mantenimiento de equipos                                  │
│                                                                 │
│  PR.PS - Mantenimiento (Platform Security)                      │
│  └─ Infraestructura resiliente                                 │
│  └─ Recuperación ante desastres                               │
│                                                                 │
│  PR.PT - Tecnologías de Protección (Protective Technology)       │
│  └─ Logs y monitoreo                                          │
│  └─ Firewalls, IDS/IPS                                        │
│  └─ Canales de comunicación seguros                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### FUNCIÓN 3: DETECT (DE)

```
┌─────────────────────────────────────────────────────────────────┐
│                    FUNCIÓN: DETECT                                │
│                    "Identificar ocurrencia de eventos"            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  PROPÓSITO:                                                    │
│  Desarrollar e implementar actividades de detección              │
│  para identificar la ocurrencia de eventos de seguridad          │
│                                                                 │
│  CATEGORÍAS:                                                  │
│                                                                 │
│  DE.AE - Anomalías y Eventos (Anomalies and Events)             │
│  └─ Eventos de red baselines                                   │
│  └─ Detección de anomalías                                     │
│  └─ Correlación de eventos                                     │
│  └─ Investigación de eventos                                   │
│                                                                 │
│  DE.CM - Monitoreo Continuo (Continuous Monitoring)              │
│  └─ Sistemas monitoreados                                       │
│  └─ Técnicas de detección activas                              │
│  └─ Líneas base definidas y monitoreadas                      │
│                                                                 │
│  DE.CT - Tecnologías de Detección (Detection Processes)          │
│  └─ Procedimientos de detección documentados                    │
│  └─ Tecnologías de detección probadas                          │
│  └─ Automatización de detección                               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### FUNCIÓN 4: RESPOND (RS)

```
┌─────────────────────────────────────────────────────────────────┐
│                    FUNCIÓN: RESPOND                              │
│                    "Tomar acciones sobre incidentes"              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  PROPÓSITO:                                                    │
│  Desarrollar e implementar actividades de respuesta             │
│  para tomar acciones respecto a incidentes detectados           │
│                                                                 │
│  CATEGORÍAS:                                                  │
│                                                                 │
│  RS.RP - Planificación de Respuesta (Response Planning)         │
│  └─ Plan de respuesta documentado y actualizado                │
│  └─ Roles y responsabilidades definidos                        │
│                                                                 │
│  RS.CO - Comunicaciones (Communications)                        │
│  └─ Notificaciones internas                                    │
│  └─ Información compartida con externos                        │
│  └─ Preservación de evidencia                                 │
│                                                                 │
│  RS.AN - Análisis (Analysis)                                    │
│  └─ Análisis forense                                         │
│  └─ Determinación de impacto                                  │
│  └─ Identificación de causa raíz                              │
│                                                                 │
│  RS.MI - Mitigación (Mitigation)                                │
│  └─ Incidentes contenidos                                     │
│  └─ Mitigaciones implementadas                                │
│  └─ Lecciones aprendidas documentadas                         │
│                                                                 │
│  RS.IM - Mejoras (Improvements)                                 │
│  └─ Lecciones incorporadas al plan de respuesta                │
│  └─ Procesos de mejora continua                               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### FUNCIÓN 5: RECOVER (RC)

```
┌─────────────────────────────────────────────────────────────────┐
│                    FUNCIÓN: RECOVER                              │
│                    "Mantener y restaurar capacidades"            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  PROPÓSITO:                                                    │
│  Desarrollar e implementar actividades para                     │
│  mantener planes de resiliencia y restaurar                    │
│  capacidades afectadas                                          │
│                                                                 │
│  CATEGORÍAS:                                                  │
│                                                                 │
│  RC.RP - Planificación de Recuperación (Recovery Planning)      │
│  └─ Plan de recuperación documentado                           │
│  └─ Roles de recuperación definidos                          │
│  └─ Recursos identificados y disponibles                      │
│                                                                 │
│  RC.IM - Mejoras (Improvements)                                 │
│  └─ Estrategias de recuperación mejoradas                      │
│  └─ Lecciones aprendidas incorporadas                        │
│                                                                 │
│  RC.CO - Comunicaciones (Communications)                         │
│  └─ Organismos internos notificados                           │
│  └─ Partes interesadas actualizadas                           │
│  └─ Gestión de reputación                                     │
│                                                                 │
│  RC.SR - Servicios (Recovery Services)                          │
│  └─ Sistemas restaurados                                      │
│  └─ Servicios críticos operando                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 5. CATEGORÍAS Y SUBCATEGORÍAS

### 5.1. Lista Completa de Categorías

```
NIST CSF v2.0 - 5 Funciones, 22 Categorías, 106+ Subcategorías
═══════════════════════════════════════════════════════════════════

FUNCIÓN IDENTIFY (ID)
├── ID.AM - Gestión de Activos (6 subcategorías)
├── ID.BE - Contexto de Negocio (3 subcategorías)
├── ID.GV - Gobernanza (4 subcategorías)
├── ID.RA - Evaluación de Riesgos (5 subcategorías)
├── ID.RM - Estrategia de Riesgos (3 subcategorías)
└── ID.SC - Gestión de Riesgos de Suministro (5 subcategorías)

FUNCIÓN PROTECT (PR)
├── PR.AA - Gestión de Identidades y Acceso (8 subcategorías)
├── PR.AT - Concienciación y Formación (4 subcategorías)
├── PR.DS - Seguridad de Datos (7 subcategorías)
├── PR.PS - Seguridad de Plataformas (4 subcategorías)
├── PR.PT - Tecnologías de Protección (5 subcategorías)
└── PR.IR - Preparación (3 subcategorías)

FUNCIÓN DETECT (DE)
├── DE.AE - Anomalías y Eventos (5 subcategorías)
├── DE.CM - Monitoreo Continuo (7 subcategorías)
└── DE.CT - Procesos de Detección (4 subcategorías)

FUNCIÓN RESPOND (RS)
├── RS.MA - Planificación de Respuesta (3 subcategorías)
├── RS.CO - Comunicaciones (4 subcategorías)
├── RS.AN - Análisis (5 subcategorías)
├── RS.MI - Mitigación (3 subcategorías)
└── RS.IM - Mejoras (2 subcategorías)

FUNCIÓN RECOVER (RC)
├── RC.RP - Planificación de Recuperación (3 subcategorías)
├── RC.CO - Comunicaciones (3 subcategorías)
├── RC.IM - Mejoras (2 subcategorías)
└── RC.SR - Servicios (3 subcategorías)
```

### 5.2. Subcategorías Detalladas (Extracto)

```python
# ============================================
# SUBCATEGORÍAS DEL NIST CSF v2.0
# ============================================

SUBCATEGORIAS = {
    # ============================================
    # IDENTIFY - Gestión de Activos (ID.AM)
    # ============================================
    "ID.AM-01": {
        "descripcion": "Inventario de dispositivos físicos",
        "nivel_base": 1,
        "ejemplos": [
            "Servidores, workstations, laptops",
            "Dispositivos de red (routers, switches)",
            "Dispositivos IoT"
        ]
    },
    "ID.AM-02": {
        "descripcion": "Inventario de plataformas y aplicaciones de software",
        "nivel_base": 1,
        "ejemplos": [
            "Sistemas operativos",
            "Aplicaciones de negocio",
            "Bases de datos"
        ]
    },
    "ID.AM-03": {
        "descripcion": "Inventario de datos de la organización",
        "nivel_base": 2,
        "ejemplos": [
            "Clasificación de datos",
            "Ubicación de datos sensibles",
            "Propietarios de datos"
        ]
    },
    "ID.AM-04": {
        "descripcion": "Inventario de servicios externos",
        "nivel_base": 2,
        "ejemplos": [
            "Servicios cloud (SaaS, PaaS, IaaS)",
            "Servicios de terceros"
        ]
    },
    "ID.AM-05": {
        "descripcion": "Mapeo de dependencias de activos a necesidades de negocio",
        "nivel_base": 3,
        "ejemplos": [
            "Activos críticos identificados",
            "Impacto de pérdida de activos"
        ]
    },
    "ID.AM-06": {
        "descripcion": "Inventario de personas con acceso a activos",
        "nivel_base": 2,
        "ejemplos": [
            "Lista de personas con acceso privilegiado",
            "Access reviews periódicos"
        ]
    },
    
    # ============================================
    # PROTECT - Gestión de Acceso (PR.AA)
    # ============================================
    "PR.AA-01": {
        "descripcion": "Políticas de identidad y acceso",
        "nivel_base": 1,
        "ejemplos": [
            "Política de contraseñas",
            "Política de acceso",
            "Procedimientos de aprovisionamiento"
        ]
    },
    "PR.AA-02": {
        "descripcion": "Gestión de identidades",
        "nivel_base": 1,
        "ejemplos": [
            "Creación de usuarios",
            "Revisión de accesos",
            "Desactivación de cuentas"
        ]
    },
    "PR.AA-03": {
        "descripcion": "Control de acceso basado en roles (RBAC)",
        "nivel_base": 2,
        "ejemplos": [
            "Roles definidos",
            "Principio de menor privilegio",
            "Separación de funciones"
        ]
    },
    "PR.AA-04": {
        "descripcion": "Autenticación robusta",
        "nivel_base": 2,
        "ejemplos": [
            "MFA implementado",
            "Autenticación biométrica",
            "FIDO2/WebAuthn"
        ]
    },
    "PR.AA-05": {
        "descripcion": "Gestión de cuentas privilegiadas",
        "nivel_base": 3,
        "ejemplos": [
            "Vault de contraseñas",
            "Acceso privilegiado bajo solicitud",
            "Auditoría de accesos privilegiados"
        ]
    },
    "PR.AA-06": {
        "descripcion": "Control de acceso físico",
        "nivel_base": 1,
        "ejemplos": [
            "Badges de acceso",
            "Cámaras de seguridad",
            "Controles de área restringida"
        ]
    },
    
    # ============================================
    # PROTECT - Seguridad de Datos (PR.DS)
    # ============================================
    "PR.DS-01": {
        "descripcion": "Datos en reposo protegidos",
        "nivel_base": 1,
        "ejemplos": [
            "Cifrado de discos (BitLocker, LUKS)",
            "Cifrado de bases de datos"
        ]
    },
    "PR.DS-02": {
        "descripcion": "Datos en tránsito protegidos",
        "nivel_base": 1,
        "ejemplos": [
            "TLS 1.2/1.3",
            "VPN para acceso remoto",
            "Certificados válidos"
        ]
    },
    "PR.DS-05": {
        "descripcion": "Protección contra fuga de datos (DLP)",
        "nivel_base": 3,
        "ejemplos": [
            "DLP endpoint",
            "DLP red",
            "Clasificación automática"
        ]
    },
    "PR.DS-06": {
        "descripcion": "Integridad de datos",
        "nivel_base": 2,
        "ejemplos": [
            "Checksums",
            "Hashes de integridad",
            "Firmas digitales"
        ]
    },
    
    # ============================================
    # DETECT - Monitoreo Continuo (DE.CM)
    # ============================================
    "DE.CM-01": {
        "descripcion": "Red monitoreada",
        "nivel_base": 1,
        "ejemplos": [
            "Logs de firewall",
            "IDS/IPS activo",
            "NetFlow análisis"
        ]
    },
    "DE.CM-04": {
        "descripcion": "Malware detectado",
        "nivel_base": 2,
        "ejemplos": [
            "Antivirus/EDR",
            "Sandboxing",
            "YARA rules"
        ]
    },
    "DE.CM-07": {
        "descripcion": "Monitoreo de integridad de archivos",
        "nivel_base": 3,
        "ejemplos": [
            "AIDE",
            "Tripwire",
            "osquery"
        ]
    },
    
    # ============================================
    # RESPOND - Planificación (RS.MA)
    # ============================================
    "RS.MA-01": {
        "descripcion": "Plan de respuesta a incidentes",
        "nivel_base": 1,
        "ejemplos": [
            "Documento de respuesta",
            "Playbooks de incidentes",
            "Contacto de emergencia"
        ]
    },
    "RS.MA-02": {
        "descripcion": "Equipo de respuesta a incidentes",
        "nivel_base": 2,
        "ejemplos": [
            "CSIRT definido",
            "Roles de respuesta",
            "Contactos escalamiento"
        ]
    },
}

def evaluar_subcategoria(subcategoria, respuestas):
    """
    Evalúa el nivel de cumplimiento de una subcategoría
    
    Returns:
        dict con puntuación (0-100) y nivel
    """
    # Promedio de respuestas
    promedio = sum(respuestas) / len(respuestas)
    
    # Mapear a puntuación
    # 0 = No implementado (0%)
    # 1 = Parcialmente (25%)
    # 2 = Implementado parcialmente (50%)
    # 3 = Mayormente implementado (75%)
    # 4 = Completamente implementado (100%)
    
    puntuacion = promedio * 25
    
    # Determinar nivel
    if puntuacion < 25:
        nivel = 1
    elif puntuacion < 50:
        nivel = 2
    elif puntuacion < 75:
        nivel = 3
    else:
        nivel = 4
    
    return {
        "subcategoria": subcategoria,
        "puntuacion": puntuacion,
        "nivel": nivel,
        "descripcion_nivel": {
            1: "No implementado o parcialmente",
            2: "Implementado parcialmente",
            3: "Mayormente implementado",
            4: "Completamente implementado y medido"
        }[nivel]
    }
```

---

## 6. NIVELES DE IMPLEMENTACIÓN (TIERS)

### 6.1. Los 4 Tiers

```
┌─────────────────────────────────────────────────────────────────┐
│                    IMPLEMENTATION TIERS                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  TIER 1: PARTIAL (Parcial)                                    │
│  ══════════════════════════                                    │
│                                                                 │
│  • Procesos: Ad-hoc, reactivos                                │
│  • Org: No formalized                 ┌──────────────────┐   │
│  • Risk Mgmt: No existe proceso         │   PARTIAL        │   │
│  • Resources: Sin recursos dedicados    │                   │   │
│  • Integration: No hay                     │                   │   │
│                                         └───┬──────────────┘   │
│                                             │                    │
│  TIER 2: RISK INFORMED (Informado por Riesgos)                │
│  ════════════════════════════════════════                       │
│                                                                 │
│  • Procesos: Aprobados por dirección                         │
│  • Org: Roles definidos pero no siempre                   ┌────┴───┐
│  • Risk Mgmt: Políticas existen pero no integradas           │  RISK   │
│  • Resources: Algunos recursos dedicados                      │INFORMED│
│  • Integration: Limitada                                        │        │
│                                                              └─┬──────┘
│                                                                  │
│  TIER 3: REPEATABLE (Repetible)                              │
│  ════════════════════════════════════                         │
│                                                                 │
│  • Procesos: Documentados y aprobados                       ┌───┴─────┐
│  • Org: Roles y responsabilidades claras                     │REPEATABLE│
│  • Risk Mgmt: Proceso formalizado                             │         │
│  • Resources: Personal dedicado                              │         │
│  • Integration: Con otras funciones de organización       └─┬───────┘
│                                                                 │
│                                                                  │
│  TIER 4: ADAPTIVE (Adaptativo)                               │
│  ═══════════════════════════════════                          │
│                                                                 │
│  • Procesos: Mejora continua basada en métricas            ┌──┴───────┐
│  • Org: Cultura de ciberseguridad arraigada                 │ ADAPTIVE │
│  • Risk Mgmt: Optimizado                                     │         │
│  • Resources: Optimizados                                    │         │
│  • Integration: Completa integración                      └──────────┘
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 6.2. Características Detalladas por Tier

```python
TIERS = {
    1: {
        "nombre": "Partial",
        "descripcion": "Procesos ad-hoc, no existe gestión formal de ciberseguridad",
        "caracteristicas": {
            "Procesos": [
                "No existe política formal",
                "Respuesta reactiva a incidentes",
                "No hay procesos documentados"
            ],
            "Gobernanza": [
                "Roles no definidos",
                "Sin supervisión de seguridad"
            ],
            "Gestión de Riesgos": [
                "No existe proceso de gestión de riesgos",
                "Riesgos identificados informalmente"
            ],
            "Recursos": [
                "Sin recursos dedicados",
                "IT hace todo"
            ],
            "Integración": [
                "No hay integración",
                "Seguridad aislada"
            ]
        },
        "objetivo": "Avanzar a Tier 2",
        "prioridad": "Formalizar procesos básicos"
    },
    2: {
        "nombre": "Risk Informed",
        "descripcion": "Gestión de riesgos existe pero no integrada completamente",
        "caracteristicas": {
            "Procesos": [
                "Políticas aprobadas",
                "Procesos informales",
                "Algunas métricas"
            ],
            "Gobernanza": [
                "Roles definidos informalmente",
                "DPO/Responsable de seguridad existe"
            ],
            "Gestión de Riesgos": [
                "Evaluación de riesgos periódica",
                "No integrada con decisiones de negocio"
            ],
            "Recursos": [
                "Algunos recursos dedicados",
                "Consultores externos"
            ],
            "Integración": [
                "Comunicación con negocio",
                "No integrada en todos los procesos"
            ]
        },
        "objetivo": "Avanzar a Tier 3",
        "prioridad": "Integrar seguridad en procesos de negocio"
    },
    3: {
        "nombre": "Repeatable",
        "descripcion": "Procesos documentados y repetibles, integrados con el negocio",
        "caracteristicas": {
            "Procesos": [
                "Políticas y procedimientos documentados",
                "Aprobados por la dirección",
                "Consistentemente implementados"
            ],
            "Gobernanza": [
                "CISO o equivalente",
                "Comité de seguridad",
                "Reportes regulares"
            ],
            "Gestión de Riesgos": [
                "Proceso formalizado",
                "Integrado con planificación",
                "Tolerancia al riesgo definida"
            ],
            "Recursos": [
                "Equipo de seguridad dedicado",
                "Presupuesto dedicado"
            ],
            "Integración": [
                "Integrado en ciclo de vida de desarrollo",
                "Seguridad en todas las fases"
            ]
        },
        "objetivo": "Avanzar a Tier 4",
        "prioridad": "Automatizar y optimizar"
    },
    4: {
        "nombre": "Adaptive",
        "descripcion": "Mejora continua basada en datos y预测analytics",
        "caracteristicas": {
            "Procesos": [
                "Mejora continua basada en métricas",
                "Procesos optimizados",
                "Automatización avanzada"
            ],
            "Gobernanza": [
                "Cultura de seguridad arraigada",
                "Seguridad como ventaja competitiva"
            ],
            "Gestión de Riesgos": [
                "Proactiva y predictiva",
                "Threat intelligence integrada"
            ],
            "Recursos": [
                "Equipo maduro y especializados",
                "Innovación en seguridad"
            ],
            "Integración": [
                "Totalmente integrado",
                "DevSecOps mature"
            ]
        },
        "objetivo": "Mantener y mejorar",
        "prioridad": "Innovación y liderazgo"
    }
}
```

---

## 7. PERFILES (PROFILES)

### 7.1. ¿Qué es un Perfil?

```
┌─────────────────────────────────────────────────────────────────┐
│                    NIST CSF PROFILES                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  PERFIL = Estado actual + Estado objetivo                       │
│           de ciberseguridad de una organización                  │
│                                                                 │
│  COMPONENTES:                                                  │
│                                                                 │
│  Current Profile (Estado Actual)                               │
│  └─ Dónde está la organización hoy                           │
│  └─ Evaluado mediante subcategorías                           │
│  └─ Puntuación actual                                         │
│                                                                 │
│  Target Profile (Estado Objetivo)                              │
│  └─ Dónde quiere estar la organización                       │
│  └─ Definido por requerimientos de negocio                   │
│  └─ Considerando recursos disponibles                        │
│                                                                 │
│  GAP = Current - Target                                       │
│  └─ Brecha a cerrar                                          │
│  └─ Priorizada por riesgo                                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 7.2. Ejemplo de Perfil

```python
class PerfilNIST:
    """
    Representa un perfil del NIST CSF
    """
    
    def __init__(self, nombre, organizacion):
        self.nombre = nombre
        self.organizacion = organizacion
        self.current_profile = {}  # Estado actual
        self.target_profile = {}   # Estado objetivo
        self.fecha = datetime.now()
    
    def evaluar_current(self, subcategorias):
        """
        Evalúa el estado actual de la organización
        """
        for sub in subcategorias:
            self.current_profile[sub["id"]] = {
                "descripcion": sub["descripcion"],
                "nivel": sub.get("nivel_actual", 1),
                "evidencia": sub.get("evidencia", ""),
                "缺口": sub.get("缺口", [])
            }
    
    def definir_target(self, subcategorias):
        """
        Define el estado objetivo
        """
        for sub in subcategorias:
            self.target_profile[sub["id"]] = {
                "nivel_deseado": sub.get("nivel_deseado", 3),
                "fecha_objetivo": sub.get("fecha", None)
            }
    
    def calcular_gap(self):
        """
        Calcula la brecha entre estado actual y objetivo
        """
        gaps = []
        
        for sub_id in self.current_profile:
            if sub_id in self.target_profile:
                current = self.current_profile[sub_id]["nivel"]
                target = self.target_profile[sub_id]["nivel_deseado"]
                
                if current < target:
                    gaps.append({
                        "subcategoria": sub_id,
                        "current": current,
                        "target": target,
                        "缺口": target - current,
                        "descripcion": self.current_profile[sub_id]["descripcion"]
                    })
        
        # Ordenar por prioridad (mayor gap primero)
        return sorted(gaps, key=lambda x: x["缺口"], reverse=True)
    
    def generar_plan_accion(self):
        """
        Genera plan de acción para cerrar gaps
        """
        gaps = self.calcular_gap()
        plan = []
        
        for i, gap in enumerate(gaps, 1):
            plan.append({
                "n": i,
                "subcategoria": gap["subcategoria"],
                "descripcion": gap["descripcion"],
                "gap": gap["缺口"],
                "acciones": self.sugerir_acciones(gap),
                "recursos_requeridos": self.estimar_recursos(gap),
                "fecha_limite": self.calcular_fecha(gap)
            })
        
        return plan
    
    def sugerir_acciones(self, gap):
        """Sugiere acciones para cerrar gap"""
        # Ejemplo simplificado
        if gap["缺口"] >= 2:
            return [
                "Contratar recursos especializados",
                "Implementar tecnología",
                "Capacitar personal"
            ]
        else:
            return [
                "Mejorar documentación",
                "Completar implementación",
                "Verificar efectividad"
            ]
    
    def estimar_recursos(self, gap):
        """Estima recursos necesarios"""
        # Simplificado
        return {
            "horas": gap["缺口"] * 40,
            "presupuesto": gap["缺口"] * 10000,
            "personas": gap["缺口"]
        }
    
    def calcular_fecha(self, gap):
        """Calcula fecha límite para cerrar gap"""
        meses = gap["缺口"] * 3  # 3 meses por nivel
        return datetime.now() + timedelta(days=meses * 30)


# ============================================
# EJEMPLO DE USO
# ============================================

perfil = PerfilNIST(
    nombre="Perfil Banco XYZ v2.0",
    organizacion="Banco XYZ Uruguay"
)

# Evaluar estado actual
perfil.evaluar_current([
    {
        "id": "ID.AM-01",
        "descripcion": "Inventario de dispositivos",
        "nivel_actual": 3,
        "evidencia": "Inventario actualizado en CMDB"
    },
    {
        "id": "ID.AM-02",
        "descripcion": "Inventario de software",
        "nivel_actual": 2,
        "evidencia": "Inventario parcial"
    },
    {
        "id": "PR.AA-04",
        "descripcion": "Autenticación robusta",
        "nivel_actual": 2,
        "evidencia": "MFA solo en sistemas críticos"
    }
])

# Definir estado objetivo
perfil.definir_target([
    {"id": "ID.AM-01", "nivel_deseado": 4},
    {"id": "ID.AM-02", "nivel_deseado": 4},
    {"id": "PR.AA-04", "nivel_deseado": 4}
])

# Generar informe
print("=" * 60)
print(f"PERFIL: {perfil.nombre}")
print("=" * 60)
print("\nGAPS PRIORIZADOS:\n")

for gap in perfil.calcular_gap():
    print(f"  {gap['subcategoria']}: {gap['current']} → {gap['target']} (gap: {gap['缺口']})")
    print(f"    {gap['descripcion']}\n")
```

---

## 8. PROCESO DE MEDICIÓN

### 8.1. Framework de Medición

```
┌─────────────────────────────────────────────────────────────────┐
│                 NIST CSF MEASUREMENT FRAMEWORK                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  MÉTRICAS = Subcategorías + Niveles de Cumplimiento             │
│                                                                 │
│  ESCALA DE EVALUACIÓN:                                          │
│                                                                 │
│  0 = No implementado (0%)                                      │
│  1 = Parcialmente implementado (1-33%)                          │
│  2 = Mayormente implementado (34-66%)                          │
│  3 = Completamente implementado (67-100%)                       │
│  N/A = No aplica                                               │
│                                                                 │
│  ─────────────────────────────────────────────────────────────  │
│                                                                 │
│  MÉTRICAS RECOMENDADAS POR FUNCIÓN:                             │
│                                                                 │
│  IDENTIFY:                                                      │
│  • % de activos inventariados                                    │
│  • Frecuencia de actualización del inventario                   │
│  • N° de riesgos evaluados por trimestre                       │
│                                                                 │
│  PROTECT:                                                       │
│  • % de usuarios con MFA activo                                 │
│  • % de datos clasificados                                     │
│  • N° de empleados treinados                                   │
│                                                                 │
│  DETECT:                                                        │
│  • Tiempo promedio de detección (MTTD)                         │
│  • N° de alertas investigadas                                   │
│  • % de cobertura de monitoreo                                  │
│                                                                 │
│  RESPOND:                                                      │
│  • Tiempo promedio de respuesta (MTTR)                         │
│  • N° de incidentes por severidad                             │
│  • % de playbooks ejecutados exitosamente                      │
│                                                                 │
│  RECOVER:                                                      │
│  • Tiempo de recuperación (RTO)                                │
│  • N° de ejercicios de recuperación realizados                │
│  • % de sistemas críticos con backup verificable                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 8.2. Dashboard de Métricas

```python
class DashboardNIST:
    """
    Dashboard de métricas NIST CSF
    """
    
    def __init__(self, organizacion):
        self.organizacion = organizacion
        self.metrica = {}
    
    def agregar_metrica(self, funcion, categoria, metrica):
        """Agrega una métrica al dashboard"""
        key = f"{funcion}.{categoria}"
        self.metrica[key] = metrica
    
    def calcular_puntuacion_funcion(self, funcion):
        """Calcula puntuación promedio de una función"""
        metricas_funcion = [
            v for k, v in self.metrica.items() 
            if k.startswith(funcion)
        ]
        if not metricas_funcion:
            return None
        
        return sum(m["valor"] for m in metricas_funcion) / len(metricas_funcion)
    
    def generar_reporte(self):
        """Genera reporte completo"""
        funciones = ["ID", "PR", "DE", "RS", "RC"]
        
        reporte = {
            "organizacion": self.organizacion,
            "fecha": datetime.now().isoformat(),
            "funciones": {},
            "puntuacion_total": 0
        }
        
        for fn in funciones:
            puntuacion = self.calcular_puntuacion_funcion(fn)
            if puntuacion:
                reporte["funciones"][fn] = {
                    "puntuacion": round(puntuacion, 2),
                    "nivel": self.nivel_desde_puntuacion(puntuacion),
                    "estado": self.estado_desde_puntuacion(puntuacion)
                }
                reporte["puntuacion_total"] += puntuacion
        
        reporte["puntuacion_total"] /= len(reporte["funciones"])
        
        return reporte
    
    def nivel_desde_puntuacion(self, puntuacion):
        if puntuacion < 25: return 1
        elif puntuacion < 50: return 2
        elif puntuacion < 75: return 3
        else: return 4
    
    def estado_desde_puntuacion(self, puntuacion):
        if puntuacion < 25: return "Crítico"
        elif puntuacion < 50: return "Bajo"
        elif puntuacion < 75: return "Aceptable"
        else: return "Óptimo"


# Uso del dashboard
dashboard = DashboardNIST("Mi Organización")

dashboard.agregar_metrica("ID", "AM-01", {"nombre": "Inventario", "valor": 75})
dashboard.agregar_metrica("PR", "AA-04", {"nombre": "MFA", "valor": 60})
dashboard.agregar_metrica("DE", "CM-01", {"nombre": "Monitoreo", "valor": 45})
dashboard.agregar_metrica("RS", "MA-01", {"nombre": "Plan RI", "valor": 80})
dashboard.agregar_metrica("RC", "RP-01", {"nombre": "BCP", "valor": 55})

reporte = dashboard.generar_reporte()

print(f"""
╔════════════════════════════════════════════════════╗
║     REPORTE NIST CSF - {reporte['organizacion']}
╠════════════════════════════════════════════════════╣
║  Fecha: {reporte['fecha']}
╠════════════════════════════════════════════════════╣
║  FUNCIÓN        │ PUNTUACIÓN │ NIVEL │ ESTADO     ║
╠════════════════════════════════════════════════════╣
║  IDENTIFY       │   {reporte['funciones']['ID']['puntuacion']:5.1f}%  │   {reporte['funciones']['ID']['nivel']}    │ {reporte['funciones']['ID']['estado']:9s}  ║
║  PROTECT        │   {reporte['funciones']['PR']['puntuacion']:5.1f}%  │   {reporte['funciones']['PR']['nivel']}    │ {reporte['funciones']['PR']['estado']:9s}  ║
║  DETECT         │   {reporte['funciones']['DE']['puntuacion']:5.1f}%  │   {reporte['funciones']['DE']['nivel']}    │ {reporte['funciones']['DE']['estado']:9s}  ║
║  RESPOND        │   {reporte['funciones']['RS']['puntuacion']:5.1f}%  │   {reporte['funciones']['RS']['nivel']}    │ {reporte['funciones']['RS']['estado']:9s}  ║
║  RECOVER        │   {reporte['funciones']['RC']['puntuacion']:5.1f}%  │   {reporte['funciones']['RC']['nivel']}    │ {reporte['funciones']['RC']['estado']:9s}  ║
╠════════════════════════════════════════════════════╣
║  PROMEDIO TOTAL │   {reporte['puntuacion_total']:5.1f}%  │       │              ║
╚════════════════════════════════════════════════════╝
""")
```

---

## 9. RELACIÓN CON OTROS MARCOS

### 9.1. Mapeo con ISO 27001

```
┌─────────────────────────────────────────────────────────────────┐
│              MAPEO NIST CSF ↔ ISO/IEC 27001:2022                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  NIST CSF                    ISO 27001:2022                     │
│  ─────────                   ─────────────────                   │
│                                                                 │
│  IDENTIFY                    Clause 4-6                        │
│  ├─ ID.AM-1,2,3           → A.5.1, A.8.1                     │
│  ├─ ID.BE                   → A.5.1                          │
│  ├─ ID.GV                   → Clause 5,6                     │
│  └─ ID.RA, RM              → Clause 6.1,6.1.2                 │
│                                                                 │
│  PROTECT                     Clause 8                          │
│  ├─ PR.AA                   → A.5.15, A.5.17, A.8.2         │
│  ├─ PR.AT                   → A.6.3                          │
│  ├─ PR.DS                   → A.8.3, A.8.4, A.8.5, A.8.6   │
│  ├─ PR.PS                   → A.8.9, A.8.19, A.8.20          │
│  └─ PR.PT                   → A.8.22, A.8.24                 │
│                                                                 │
│  DETECT                      Clause 8                          │
│  ├─ DE.AE                   → A.8.16                         │
│  └─ DE.CM                   → A.8.17                          │
│                                                                 │
│  RESPOND                     Clause 8                          │
│  └─ RS.*                    → A.5.26, A.8.17                  │
│                                                                 │
│  RECOVER                     Clause 8                          │
│  └─ RC.*                    → A.5.29, A.8.17                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 9.2. Mapeo con NIST SP 800-53

```
┌─────────────────────────────────────────────────────────────────┐
│         NIST CSF ↔ NIST SP 800-53 Rev 5 (Controls)              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  NIST CSF Control        NIST SP 800-53 Controls                │
│  ─────────────────       ────────────────────                  │
│                                                                 │
│  ID.AM-1                 AC-2, CM-8                           │
│  ID.RA-1                 RA-3, RA-5                           │
│  PR.AA-1                 AC-1, AC-2                           │
│  PR.AA-4                 AC-3, AC-4                           │
│  PR.DS-1                 SC-28, SC-8                          │
│  PR.DS-2                 SC-8                                 │
│  DE.AE-1                 SI-4                                  │
│  RS.MA-1                 IR-1, IR-2, IR-4                     │
│  RC.RP-1                 IR-7, CP-2, CP-7                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 10. GUÍA DE IMPLEMENTACIÓN

### 10.1. Pasos de Implementación

```
┌─────────────────────────────────────────────────────────────────┐
│                 GUÍA DE IMPLEMENTACIÓN DEL NIST CSF               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  PASO 1: PREPARACIÓN                                           │
│  ─────────────────                                             │
│  □ Obtener compromiso de la dirección                          │
│  □ Definir alcance                                             │
│  □ Establecer equipo de trabajo                                 │
│  □ Seleccionar perfil base                                     │
│                                                                 │
│  PASO 2: EVALUACIÓN ACTUAL (Current Profile)                    │
│  ────────────────────────────────────────────                   │
│  □ Revisar cada subcategoría                                   │
│  □ Evaluar estado actual (0-3)                                 │
│  □ Documentar evidencia                                        │
│  □ Identificar gaps                                            │
│                                                                 │
│  PASO 3: DEFINIR ESTADO OBJETIVO (Target Profile)              │
│  ──────────────────────────────────────────────────             │
│  □ Definir niveles objetivo por subcategoría                   │
│  □ Considerar recursos disponibles                            │
│  □ Priorizar basado en riesgo y factibilidad                   │
│                                                                 │
│  PASO 4: ANÁLISIS DE BRECHAS                                   │
│  ──────────────────────────                                     │
│  □ Calcular gaps                                              │
│  □ Priorizar acciones                                          │
│  □ Estimar recursos necesarios                                 │
│                                                                 │
│  PASO 5: PLAN DE ACCIÓN                                        │
│  ───────────────────                                           │
│  □ Definir controles a implementar                            │
│  □ Asignar responsables                                       │
│  □ Establecer cronograma                                      │
│  □ Definir métricas de éxito                                   │
│                                                                 │
│  PASO 6: IMPLEMENTACIÓN                                        │
│  ──────────────────                                            │
│  □ Implementar controles                                      │
│  □ Documentar evidencia                                        │
│  □ Capacitar personal                                          │
│                                                                 │
│  PASO 7: MONITOREO Y MEJORA                                    │
│  ──────────────────────────                                     │
│  □ Medir efectividad                                          │
│  □ Comparar con Target Profile                                │
│  □ Actualizar Current Profile                                │
│  □ Mejorar continuamente                                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 11. RECURSOS Y HERRAMIENTAS

### 11.1. Herramientas Oficiales NIST

| Herramienta | Descripción | Link |
|-------------|-------------|------|
| **NIST CSFREF** | Referencia del framework | nist.gov/cyberframework |
| **CSF Tool** | Herramienta de evaluación | Pagina NIST |
| **Informative References** | Mapeo a otros estándares | NIST GitHub |
| **FAQ** | Preguntas frecuentes | nist.gov/cyberframework |

### 11.2. Recursos Adicionales

```
╔═══════════════════════════════════════════════════════════════════╗
║                    RECURSOS NIST CSF                             ║
╠═══════════════════════════════════════════════════════════════════╣
║                                                                   ║
║  DOCUMENTACIÓN:                                                   ║
║  • NIST CSF 2.0 (documento oficial)                             ║
║  • Quick Start Guide                                            ║
║  • Roadmap                                                     ║
║  • Informative References Summary                               ║
║                                                                   ║
║  PERFILES SECTORIALES:                                           ║
║  • Manufacturing                                                ║
║  • Healthcare                                                   ║
║  • Small Business                                              ║
║  • Enterprise                                                    ║
║                                                                   ║
║  HERRAMIENTAS:                                                   ║
║  • NIST CSF Excel Template                                     ║
║  • Community resources                                          ║
║  • Case studies                                                 ║
║                                                                   ║
║  FORMACIÓN:                                                      ║
║  • NIST CSF 101 (video)                                        ║
║  • Podcast series                                             ║
║  • Webinars                                                    ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
```

---

**Documento:** NIST Cybersecurity Framework (CSF)  
**Versión:** 2.0  
**Última actualización:** 2024  
**Referencia:** https://csrc.nist.gov/publications/detail/white-paper/3/ea92cdf2-4e39-4275-9560-edfe547a62f9/final
