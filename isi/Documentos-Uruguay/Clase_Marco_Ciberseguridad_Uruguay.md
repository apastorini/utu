# MARCO DE CIBERSEGURIDAD URUGUAY - AGESIC

---

## ÍNDICE

1. Introducción al Marco
2. Contexto y Antecedentes
3. Objetivos del Marco
4. Principios Rectores
5. Gobernanza de Ciberseguridad
6. Modelo de Capacidades
7. Funciones del Marco (NIST)
8. Categorías y Subcategorías
9. Niveles de Implementación
10. Perfiles Organizacionales
11. Medición y Evaluación
12. Guía de Implementación
13. Relación con Otros Marcos
14. Recursos y Referencias

---

## 1. INTRODUCCIÓN AL MARCO

### 1.1. ¿Qué es el Marco de Ciberseguridad?

```
┌─────────────────────────────────────────────────────────────────┐
│         MARCO DE CIBERSEGURIDAD DE URUGUAY                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  AUTORIDAD: AGESIC (Agencia de Gobierno Electrónico            │
│              y Sociedad de la Información)                    │
│                                                                 │
│  VERSIÓN ACTUAL: 5.0                                           │
│  PUBLICACIÓN: 2021                                            │
│  ACTUALIZACIÓN: Periodicidad recomendada cada 2 años           │
│                                                                 │
│  BASE: NIST Cybersecurity Framework (CSF) adaptado          │
│  + Contexto uruguayo                                         │
│                                                                 │
│  ALCANCE:                                                    │
│  ├─ Organismos del Estado                                   │
│  ├─ Servicios esenciales                                     │
│  ├─ Infraestructura crítica                                  │
│  └─ Proveedores de servicios informáticos                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2. Propósito del Marco

El Marco de Ciberseguridad de Uruguay tiene como propósito:

```
┌─────────────────────────────────────────────────────────────────┐
│                    PROPÓSITO DEL MARCO                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. PROVEER un lenguaje común para describir                    │
│     la gestión de ciberseguridad                               │
│                                                                 │
│  2. ESTABLECER un conjunto de principios y directrices        │
│     para gestionar riesgos de ciberseguridad                   │
│                                                                 │
│  3. DEFINIR mecanismos para:                                   │
│     ├─ Identificar activos y riesgos                        │
│     ├─ Proteger sistemas e información                      │
│     ├─ Detectar incidentes de seguridad                      │
│     ├─ Responder ante incidentes                             │
│     └─ Recuperar operaciones después de incidentes           │
│                                                                 │
│  4. OFRECER un sistema de medición y evaluación              │
│     del nivel de madurez en ciberseguridad                   │
│                                                                 │
│  5. FACILITAR la comunicación entre:                          │
│     ├─ Áreas técnicas y directivas                         │
│     ├─ Organismos públicos y privados                       │
│     └─ Organismos nacionales e internacionales              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. CONTEXTO Y ANTECEDENTES

### 2.1. Evolución del Marco

```
┌─────────────────────────────────────────────────────────────────┐
│                 HISTORIA DEL MARCO URUGUAYO                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  2013 - VERSIÓN 1.0                                           │
│  └─ Primer marco de ciberseguridad                          │
│  └─ Basado en ISO 27001                                     │
│                                                                 │
│  2015 - VERSIÓN 2.0                                           │
│  └─ Incorporación de NIST CSF                                 │
│  └─ Adaptación al contexto nacional                         │
│                                                                 │
│  2018 - VERSIÓN 3.0                                           │
│  └─ Mejora de perfiles                                       │
│  └─ Incorporación de madurez                                │
│                                                                 │
│  2020 - VERSIÓN 4.0                                           │
│  └─ Actualización tecnológica                                │
│  └─ Integración con servicios de gobierno electrónico        │
│                                                                 │
│  2021 - VERSIÓN 5.0 (Actual)                                  │
│  └─ Alineación con NIST CSF 1.1                              │
│  └─ Nuevos perfiles sectoriales                              │
│  └─ Métricas de evaluación modernizadas                    │
│  └─ Integración con estrategia nacional                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2. Marco Legal Uruguayo

```
┌─────────────────────────────────────────────────────────────────┐
│               MARCO LEGAL RELACIONADO                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  LEYES NACIONALES                                             │
│  ├─ Ley 18.331: Protección de Datos Personales              │
│  ├─ Ley 18.381: Acceso a la Información Pública            │
│  ├─ Ley 19.670: Modificación de Protección de Datos       │
│  ├─ Ley 19.943: Sistema Nacional de Transformación        │
│  │   Pública y laAGESIC                                     │
│  └─ Ley 20.075: Estrategia de Ciberseguridad               │
│                                                                 │
│  AGESIC                                                       │
│  ├─ Agencia de Gobierno Electrónico                         │
│  │   y Sociedad de la Información                           │
│  ├─ Dependencia de la Presidency                          │
│  └─ Rol: Regulación, promoción y coordinación              │
│                                                                 │
│  CERT-UY (hoy parte de AGESIC)                               │
│  └─ Centro de Respuesta a Incidentes                        │
│  └─ Coordinación de incidentes de seguridad                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 2.3. Estrategia Nacional de Ciberseguridad

```
┌─────────────────────────────────────────────────────────────────┐
│         ESTRATEGIA NACIONAL DE CIBERSEGURIDAD                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  PILARES:                                                      │
│                                                                 │
│  1. FORTALECIMIENTO INSTITUCIONAL                              │
│     ├─ Fortalecer capacidades de AGESIC                      │
│     ├─ Crear gobernanza de ciberseguridad                    │
│     └─ Coordinar esfuerzos entre organismos                  │
│                                                                 │
│  2. PROTECCIÓN DE INFRAESTRUCTURA CRÍTICA                     │
│     ├─ Identificar infraestructura crítica                    │
│     ├─ Establecer requisitos de seguridad                   │
│     └─ Promover inversiones en protección                   │
│                                                                 │
│  3. DESARROLLO DE CAPACIDADES                                  │
│     ├─ Formación de profesionales                            │
│     ├─ Investigación y desarrollo                           │
│     └─ Concienciación ciudadana                             │
│                                                                 │
│  4. COOPERACIÓN INTERNACIONAL                                 │
│     ├─ Participación en organismos internacionales           │
│     ├─ Intercambio de información                         │
│     └─ Asistencia técnica                                   │
│                                                                 │
│  5. MARCO NORMATIVO                                          │
│     └─ Desarrollo de normativa específica                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. OBJETIVOS DEL MARCO

### 3.1. Objetivos Estratégicos

```
┌─────────────────────────────────────────────────────────────────┐
│                 OBJETIVOS ESTRATÉGICOS                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  OBJETIVO GENERAL:                                             │
│  Establecer un marco de referencia para la gestión             │
│  de ciberseguridad en el Estado uruguayo, Promoviendo           │
│  la resiliencia cibernética y la confianza digital            │
│                                                                 │
│  ─────────────────────────────────────────────────────────────  │
│                                                                 │
│  OBJETIVOS ESPECÍFICOS:                                       │
│                                                                 │
│  OE1: Disponer de un lenguaje Común                          │
│       └─ Vocabulario estandarizado para ciberseguridad         │
│                                                                 │
│  OE2: Facilitar la gestión de riesgos                        │
│       └─ Metodología para identificar, analizar y tratar       │
│         riesgos de ciberseguridad                               │
│                                                                 │
│  OE3: Mejorar la coordinación interinstitucional              │
│       └─ Mecanismos de cooperación entre organismos           │
│                                                                 │
│  OE4: Promover la mejora continua                             │
│       └─ Sistema de medición de madurez                       │
│         y seguimiento de mejoras                               │
│                                                                 │
│  OE5: Facilitar el cumplimiento normativo                    │
│       └─ Alineación con estándares internacionales            │
│         y normativa nacional                                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2. Destinatarios del Marco

| Destinatario | Uso del Marco |
|--------------|---------------|
| **Autoridades** | Tomar decisiones informadas sobre inversión en ciberseguridad |
| **Gestores de TI** | Planificar y ejecutar programas de ciberseguridad |
| **Equipos técnicos** | Implementar controles y medir su efectividad |
| **Auditores** | Evaluar el nivel de madurez y conformance |
| **Proveedores** | Entender requisitos de sus clientes públicos |
| **Ciudadanos** | Conocer el nivel de protección esperado |

---

## 4. PRINCIPIOS RECTORES

### 4.1. Principios Fundamentales

```
┌─────────────────────────────────────────────────────────────────┐
│                 PRINCIPIOS RECTORES DEL MARCO                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. PROPORCIONALIDAD                                           │
│     └─ Las medidas deben ser proporcionales al riesgo          │
│     └─ Evitar sobre-regulación o sub-protección             │
│                                                                 │
│  2. RESPONSABILIDAD COMPARTIDA                               │
│     └─ Todos los actores tienen responsabilidad              │
│     └─ Coordinación y cooperación                            │
│                                                                 │
│  3. ENFOQUE BASADO EN RIESGOS                                │
│     └─ Priorización según criticidad de activos               │
│     └─ Recursos hacia mayores riesgos                        │
│                                                                 │
│  4. DEFENSA EN PROFUNDIDAD                                   │
│     └─ Múltiples capas de protección                        │
│     └─ Si falla una capa, las otras responden               │
│                                                                 │
│  5. MEJORA CONTINUA                                          │
│     └─ El panorama de amenazas evoluciona constantemente      │
│     └─ Necesidad de adaptación y actualización              │
│                                                                 │
│  6. TRANSPARENCIA                                             │
│     └─ Procesos y decisiones documentados                    │
│     └─ Información accesible a interesados legítimos         │
│                                                                 │
│  7. PRIVACIDAD POR DISEÑO                                    │
│     └─ Protección de datos personales desde el inicio         │
│                                                                 │
│  8. COMPATIBILIDAD                                            │
│     └─ Alineación con marcos internacionales                  │
│     └─ Facilitar intercambio y cooperación                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 5. GOBERNANZA DE CIBERSEGURIDAD

### 5.1. Estructura de Gobernanza

```
┌─────────────────────────────────────────────────────────────────┐
│              ESTRUCTURA DE GOBERNANZA URUGUAY                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│                    NIVEL POLÍTICO                              │
│                    ─────────────────                          │
│         Comité Interministerial de Ciberseguridad              │
│                    └─ Ministers de:                          │
│                       ├─ Interior                            │
│                       ├─ Defensa                             │
│                       ├─ Economía                            │
│                       └─ Innovación                         │
│                                                                 │
│                         │                                      │
│                         ▼                                      │
│                    NIVEL ESTRATÉGICO                         │
│                    ─────────────────                         │
│                      AGESIC                                   │
│                    └─ Dirección de Ciberseguridad              │
│                    └─ CERT-UY                                 │
│                    └─ Unidades de Seguridad de la              │
│                       Información (USI)                      │
│                                                                 │
│                         │                                      │
│                         ▼                                      │
│                    NIVEL OPERATIVO                            │
│                    ────────────────                            │
│              Organismos del Estado                             │
│              └─ Equipos técnicos de TI                        │
│              └─ Enlaces de seguridad                        │
│              └─ Operadores de sistemas críticos              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 5.2. Roles y Responsabilidades

| Rol | Descripción | Responsabilidades |
|-----|-------------|-----------------|
| **AGESIC** | Agencia rectora | Regulación, guías, coordinación, asistencia |
| **CERT-UY** | Equipo de respuesta | Coordinación de incidentes, alertas |
| **USI** | Unidad de Seguridad | Gestión de seguridad en cada organismo |
| **Enlace de Seguridad** | Punto de contacto | Coordinación con CERT-UY |
| **CISO/Director de Seguridad** | Líder técnico | Estrategia, gestión de riesgos |

### 5.3. Modelo de Madurez de Gobernanza

```
┌─────────────────────────────────────────────────────────────────┐
│                 NIVELES DE MADUREZ - GOBERNANZA                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Nivel 1: INICIAL                                              │
│  └─ No existe gobernanza formalizada                          │
│  └─ Decisiones ad-hoc                                        │
│                                                                 │
│  Nivel 2: EN DESARROLLO                                        │
│  └─ Se identifican roles básicos                              │
│  └─ Políticas incipientes                                    │
│                                                                 │
│  Nivel 3: DEFINIDO                                             │
│  └─ Gobernanza documentada                                   │
│  └─ Roles y responsabilidades claras                        │
│  └─ Enlaces de seguridad designados                         │
│                                                                 │
│  Nivel 4: GESTIONADO                                           │
│  └─ Métricas de desempeño                                    │
│  └─ Revisiones periódicas                                    │
│  └─ Mejora basada en resultados                              │
│                                                                 │
│  Nivel 5: OPTIMIZADO                                           │
│  └─ Mejora continua                                        │
│  └─ Benchmarking con otros organismos                        │
│  └─ Contribución a políticas nacionales                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 6. MODELO DE CAPACIDADES

### 6.1. Las 5 Funciones Core (Basadas en NIST CSF)

```
┌─────────────────────────────────────────────────────────────────┐
│              LAS 5 FUNCIONES DEL MARCO                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐                                               │
│  │  IDENTIFY   │  Comprender la organización                   │
│  │  (Identificar)│  y su contexto de ciberseguridad            │
│  └──────┬──────┘                                               │
│         │                                                      │
│         ▼                                                      │
│  ┌─────────────┐                                               │
│  │  PROTECT    │  Implementar safeguards                       │
│  │  (Proteger) │  para proteger activos                       │
│  └──────┬──────┘                                               │
│         │                                                      │
│         ▼                                                      │
│  ┌─────────────┐                                               │
│  │   DETECT    │  Identificar ocurrencia                      │
│  │  (Detectar) │  de eventos de seguridad                     │
│  └──────┬──────┘                                               │
│         │                                                      │
│         ▼                                                      │
│  ┌─────────────┐                                               │
│  │  RESPOND    │  Tomar acciones sobre                       │
│  │  (Responder)│  incidentes detectados                       │
│  └──────┬──────┘                                               │
│         │                                                      │
│         ▼                                                      │
│  ┌─────────────┐                                               │
│  │   RECOVER   │  Restaurar capacidades                      │
│  │ (Recuperar) │  afectadas por incidentes                     │
│  └─────────────┘                                               │
│                                                                 │
│  Las 5 funciones operan de forma cíclica e integrada          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 6.2. Desglose de Funciones

#### FUNCIÓN 1: IDENTIFY (Identificar)

```
┌─────────────────────────────────────────────────────────────────┐
│              FUNCIÓN: IDENTIFY - IDENTIFICAR                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  PROPÓSITO: Desarrollar comprensión organizacional               │
│  de sistemas, activos, datos y capacidades de ciberseguridad   │
│                                                                 │
│  CATEGORÍAS:                                                  │
│                                                                 │
│  ID.AM - Gestión de Activos                                     │
│  ├─ Identificar dispositivos y sistemas                       │
│  ├─ Identificar software y aplicaciones                       │
│  ├─ Identificar información almacenada                       │
│  └─ Identificar personas, roles y responsabilidades          │
│                                                                 │
│  ID.BE - Gobernanza                                           │
│  ├─ Políticas de ciberseguridad establecidas                  │
│  ├─ Roles y responsabilidades definidos                       │
│  ├─ Legal y regulatorio identificado                         │
│  └─ Estrategia de riesgos definida                          │
│                                                                 │
│  ID.RA - Evaluación de Riesgos                                 │
│  ├─ Identificación de amenazas                               │
│  ├─ Identificación de vulnerabilidades                      │
│  ├─ Impacto y probabilidad determinados                      │
│  └─ Riesgos priorizados                                      │
│                                                                 │
│  ID.RM - Estrategia de Gestión de Riesgos                      │
│  ├─ Riesgos tratados según estrategia                        │
│  ├─ Roles de gestión de riesgos establecidos                 │
│  └─ Proceso de gestión de riesgos documentado               │
│                                                                 │
│  ID.SC - Gestión de Riesgos de la Cadena de Suministro         │
│  ├─ Proveedores identificados                               │
│  ├─ Proveedores evaluados                                  │
│  └─ Contratos incluyen requisitos de seguridad               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### FUNCIÓN 2: PROTECT (Proteger)

```
┌─────────────────────────────────────────────────────────────────┐
│              FUNCIÓN: PROTECT - PROTEGER                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  PROPÓSITO: Desarrollar e implementar safeguards              │
│  apropiados para garantizar entrega de servicios               │
│                                                                 │
│  CATEGORÍAS:                                                  │
│                                                                 │
│  PR.AC - Gestión de Identidades y Acceso                       │
│  ├─ Identidades gestionadas                                  │
│  ├─ Acceso físico y lógico controlado                        │
│  ├─ Roles y privilegios definidos                           │
│  ├─ Autenticación multifactor implementada                  │
│  └─ Cuentas privilegiadas gestionadas                      │
│                                                                 │
│  PR.AT - Concienciación y Formación                            │
│  ├─ Personal entrenado en ciberseguridad                     │
│  ├─ Roles privilegiados entrenados                          │
│  └─ Phishing simulations realizadas                        │
│                                                                 │
│  PR.DS - Seguridad de Datos                                    │
│  ├─ Datos clasificados                                      │
│  ├─ Datos protegidos en tránsito y en reposo               │
│  ├─ Gestión del ciclo de vida de datos                     │
│  └─ Datos eliminados de forma segura                       │
│                                                                 │
│  PR.IP - Tecnología de Protección                              │
│  ├─ Configuraciones de seguridad implementadas             │
│  ├─ Gestión de vulnerabilidades                             │
│  ├─ Tecnologías de protección instaladas                    │
│  └─ Mantenimiento de sistemas documentado                  │
│                                                                 │
│  PR.MA - Mantenimiento                                           │
│  └─ Componentes reparados y mantenidos                       │
│                                                                 │
│  PR.PT - Protección de Tecnologías                             │
│  ├─ Logging y monitoreo configurados                        │
│  ├─ Protecciones de red implementadas                      │
│  └─ Canales de comunicación seguros                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### FUNCIÓN 3: DETECT (Detectar)

```
┌─────────────────────────────────────────────────────────────────┐
│              FUNCIÓN: DETECT - DETECTAR                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  PROPÓSITO: Desarrollar e implementar actividades               │
│  para identificar ocurrencia de eventos de seguridad            │
│                                                                 │
│  CATEGORÍAS:                                                  │
│                                                                 │
│  DE.CM - Anomalías y Eventos                                   │
│  ├─ Eventos de red monitoreados                              │
│  ├─ Uso de aplicaciones monitoreado                          │
│  ├─ Potenciales incidentes identificados                      │
│  └─ Eventos son investigados                                  │
│                                                                 │
│  DE.CP - Monitoreo Continuo                                   │
│  ├─ Sistemas monitoreados de forma continua                  │
│  ├─ Técnicas de detección implementadas                      │
│  └─ Líneas base establecidas                                 │
│                                                                 │
│  DE.AE - Tecnologías de Detección                             │
│  ├─ IDS/IPS implementados                                    │
│  ├─ Antivirus/EDR activos                                   │
│  └─ SIEM configurado                                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### FUNCIÓN 4: RESPOND (Responder)

```
┌─────────────────────────────────────────────────────────────────┐
│              FUNCIÓN: RESPOND - RESPONDER                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  PROPÓSITO: Desarrollar e implementar actividades               │
│  para tomar acciones respecto a incidentes detectados          │
│                                                                 │
│  CATEGORÍAS:                                                  │
│                                                                 │
│  RS.RP - Planificación de Respuesta                              │
│  ├─ Plan de respuesta documentado                             │
│  └─ Roles y responsabilidades definidos                      │
│                                                                 │
│  RS.CO - Comunicaciones                                         │
│  ├─ Notificaciones internas realizadas                        │
│  ├─ Información compartida con externos                      │
│  └─ Información preservada para análisis                      │
│                                                                 │
│  RS.AN - Análisis                                                │
│  ├─ Análisis forense realizado                               │
│  ├─ Impacto determinado                                      │
│  └─ Causa raíz identificada                                 │
│                                                                 │
│  RS.MI - Mitigación                                             │
│  ├─ Incidentes contenidos                                   │
│  ├─ Mitigaciones implementadas                              │
│  └─ Lecciones aprendidas documentadas                       │
│                                                                 │
│  RS.IM - Mejoras                                                │
│  └─ Lecciones incorporadas a planes de respuesta            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### FUNCIÓN 5: RECOVER (Recuperar)

```
┌─────────────────────────────────────────────────────────────────┐
│              FUNCIÓN: RECOVER - RECUPERAR                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  PROPÓSITO: Desarrollar e implementar actividades               │
│  para mantener planes de resiliencia y restaurar capacidades     │
│                                                                 │
│  CATEGORÍAS:                                                  │
│                                                                 │
│  RC.RP - Planificación de Recuperación                          │
│  ├─ Plan de continuidad documentado                           │
│  ├─ Roles de recuperación definidos                          │
│  └─ Recursos identificados                                  │
│                                                                 │
│  RC.IM - Mejoras                                               │
│  ├─ Estrategias de recuperación mejoradas                    │
│  └─ Lecciones incorporadas                                   │
│                                                                 │
│  RC.CO - Comunicaciones                                         │
│  ├─ Organismos internos notificados                          │
│  ├─ Partes interesadas externas notificadas                    │
│  └─ Reputación protegida                                     │
│                                                                 │
│  RC.RS - Servicios de Recuperación                              │
│  ├─ Sistemas restaurados                                   │
│  └─ Servicios críticos en operación                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 7. NIVELES DE IMPLEMENTACIÓN (MADUREZ)

### 7.1. Niveles de Madurez

```
┌─────────────────────────────────────────────────────────────────┐
│              NIVELES DE MADUREZ DEL MARCO                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  NIVEL 1: PARCIAL                                               │
│  ─────────────                                                  │
│  • Conciencia de riesgos existe pero no formalizada           │
│  • Procesos ad-hoc                                              │
│  • Implementación puntual de controles                        │
│  • Sin medición de efectividad                                 │
│                                                                 │
│  NIVEL 2: INFORMACIÓN RIESGOS                                  │
│  ──────────────────────────                                    │
│  • Riesgos identificados                                        │
│  • Políticas de seguridad establecidas                        │
│  • Controles básicos implementados                            │
│  • Priorización basada en riesgos                             │
│                                                                 │
│  NIVEL 3: REPETIBLE                                            │
│  ─────────────                                                 │
│  • Procesos documentados y repetibles                        │
│  • Roles y responsabilidades definidos                        │
│  • Controles implementados consistentemente                   │
│  • Medición básica de efectividad                             │
│                                                                 │
│  NIVEL 4: GESTIONADO                                           │
│  ────────────────                                              │
│  • Procesos medidos y monitoreados                           │
│  • Mejora basada en métricas                                 │
│  • Automatización de controles                               │
│  • Benchmarking interno                                       │
│                                                                 │
│  NIVEL 5: OPTIMIZADO                                           │
│  ──────────────                                                │
│  • Mejora continua basada en mejores prácticas                │
│  • Automatización avanzada                                   │
│  • Contribución a la comunidad                              │
│  • Innovación en ciberseguridad                               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 7.2. Evaluación de Madurez

```python
class EvaluadorMadurez:
    """
    Evalúa el nivel de madurez según Marco de Ciberseguridad Uruguay
    """
    
    NIVELES = {
        1: "Parcial",
        2: "Información de Riesgos",
        3: "Repetible",
        4: "Gestionado",
        5: "Optimizado"
    }
    
    def evaluar_subcategoria(self, respuestas):
        """
        Evalúa una subcategoría específica
        
        Args:
            respuestas: dict con respuestas a preguntas
        
        Returns:
            dict con puntuación y nivel
        """
        # Puntuación: 0-100
        puntuacion = sum(respuestas.values()) / len(respuestas) * 100
        
        # Determinar nivel
        if puntuacion < 20:
            nivel = 1
        elif puntuacion < 40:
            nivel = 2
        elif puntuacion < 60:
            nivel = 3
        elif puntuacion < 80:
            nivel = 4
        else:
            nivel = 5
        
        return {
            "puntuacion": puntuacion,
            "nivel": nivel,
            "descripcion": self.NIVELES[nivel]
        }
    
    def evaluar_funcion(self, subcategorias):
        """
        Evalúa una función completa (ID, PR, DE, RS, RC)
        """
        puntuaciones = []
        for sub in subcategorias:
            result = self.evaluar_subcategoria(sub["respuestas"])
            puntuaciones.append(result["puntuacion"])
        
        return {
            "funcion": subcategorias[0]["funcion"],
            "puntuacion_promedio": sum(puntuaciones) / len(puntuaciones),
            "nivel_promedio": self.nivel_desde_puntuacion(
                sum(puntuaciones) / len(puntuaciones)
            )
        }
    
    def nivel_desde_puntuacion(self, puntuacion):
        """Convierte puntuación a nivel"""
        if puntuacion < 20: return 1
        elif puntuacion < 40: return 2
        elif puntuacion < 60: return 3
        elif puntuacion < 80: return 4
        else: return 5


# Ejemplo de evaluación
evaluador = EvaluadorMadurez()

# Evaluar función IDENTIFY
resultado = evaluador.evaluar_funcion([
    {
        "funcion": "ID.AM",
        "respuestas": {
            "inventario_dispositivos": 4,
            "inventario_software": 3,
            "clasificacion_datos": 2,
            "mapeo_dependencias": 3
        }
    },
    {
        "funcion": "ID.RA",
        "respuestas": {
            "analisis_amenazas": 3,
            "analisis_vulnerabilidades": 4,
            "evaluacion_impacto": 2,
            "matriz_riesgos": 3
        }
    }
])

print(f"Función: {resultado['funcion']}")
print(f"Puntuación: {resultado['puntuacion_promedio']:.1f}%")
print(f"Nivel: {resultado['nivel_promedio']} ({evaluador.NIVELES[resultado['nivel_promedio']]})")
```

---

## 8. PERFILES ORGANIZACIONALES

### 8.1. Tipos de Perfiles

```
┌─────────────────────────────────────────────────────────────────┐
│                 PERFILES ORGANIZACIONALES                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  PERFIL BÁSICO (Todos los organismos)                          │
│  ─────────────────────────────────────                          │
│  Requisitos mínimos para cualquier organismo público           │
│  └─ Políticas básicas de seguridad                            │
│  └─ Gestión de identidades básica                            │
│  └─ Respuesta a incidentes básica                            │
│                                                                 │
│  PERFIL ESTÁNDAR (Organismos con sistemas intermedios)          │
│  ─────────────────────────────────────────────────             │
│  Requisitos para organismos con sistemas que procesan          │
│  información sensible                                          │
│  └─ Gestión de riesgos formalizada                           │
│  └─ Controles técnicos completos                             │
│  └─ Monitoreo continuo                                      │
│                                                                 │
│  PERFIL ALTO (Organismos críticos)                              │
│  ──────────────────────────                                    │
│  Para organismos que manejan infraestructura crítica           │
│  o información altamente sensible                             │
│  └─ Modelo de madurez nivel 4+                             │
│  └─ Capacidades avanzadas de detección                        │
│  └─ Ejercicios de simulación                                │
│                                                                 │
│  PERFILES SECTORIALES                                           │
│  ───────────────────                                           │
│  └─ Salud                                                    │
│  └─ Educación                                                 │
│  └─ Finanzas (BCU)                                          │
│  └─ Seguridad                                               │
│  └─ Servicios esenciales                                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 8.2. Implementación de Perfiles

```python
class PerfilOrganizacional:
    """
    Define el perfil de ciberseguridad de un organismo
    """
    
    PERFILES = {
        "basico": {
            "nivel_minimo": 2,
            "controles_obligatorios": [
                "ID.AM-1", "ID.AM-2",  # Inventario de activos
                "PR.AC-1", "PR.AC-3",  # Control de acceso
                "PR.IP-1",             # Políticas documentadas
                "DE.CM-1",             # Monitoreo básico
                "RS.RP-1"              # Plan de respuesta
            ],
            "documentacion_minima": [
                "Política de seguridad",
                "Inventario de activos",
                "Plan de respuesta a incidentes"
            ]
        },
        "estandar": {
            "nivel_minimo": 3,
            "controles_obligatorios": [
                # Todos del perfil básico +
                "ID.RA-1", "ID.RA-2",  # Gestión de riesgos
                "PR.DS-1", "PR.DS-2",  # Seguridad de datos
                "PR.AT-1", "PR.AT-2",  # Concienciación
                "DE.CM-3", "DE.CM-4",  # Monitoreo continuo
                "RS.CO-1", "RS.AN-1"   # Respuesta a incidentes
            ],
            "documentacion_minima": [
                # Todo del perfil básico +
                "Evaluación de riesgos",
                "Plan de continuidad",
                "Procedimientos operativos"
            ]
        },
        "alto": {
            "nivel_minimo": 4,
            "controles_obligatorios": [
                # Todos del perfil estándar +
                "ID.SC-1", "ID.SC-2",    # Gestión cadena suministro
                "PR.MA-1", "PR.MA-2",      # Mantenimiento
                "DE.AE-1", "DE.AE-2",     # Detección avanzada
                "RS.MI-1", "RS.IM-1",     # Mitigación y mejora
                "RC.RP-1", "RC.CO-1"      # Recuperación
            ],
            "documentacion_minima": [
                # Todo del perfil estándar +
                "Análisis de impacto de negocio",
                "Estrategia de recuperación",
                "Ejercicios de simulación documentados"
            ]
        }
    }
    
    def __init__(self, tipo_perfil):
        self.tipo = tipo_perfil
        self.config = self.PERFILES[tipo_perfil]
    
    def generar_checklist(self):
        """Genera checklist de cumplimiento"""
        checklist = []
        
        for control in self.config["controles_obligatorios"]:
            checklist.append({
                "control": control,
                "obligatorio": True,
                "nivel_requerido": self.config["nivel_minimo"],
                "evidencia_requerida": self.obtener_evidencia(control)
            })
        
        return checklist
    
    def obtener_evidencia(self, control):
        """Define evidencia requerida para cada control"""
        evidencias = {
            "ID.AM-1": "Inventario actualizado de dispositivos",
            "ID.AM-2": "Inventario de software aprobado",
            "ID.RA-1": "Documento de identificación de amenazas",
            "PR.AC-1": "Política de control de acceso",
            "PR.DS-1": "Clasificación de datos documentada",
            "DE.CM-1": "Logs de actividad de sistemas"
        }
        return evidencias.get(control, "Evidencia documental")


# Uso
perfil = PerfilOrganizacional("estandar")
checklist = perfil.generar_checklist()

print("CHECKLIST DE CUMPLIMIENTO")
print("=" * 60)
print(f"Perfil: {perfil.tipo.upper()}")
print(f"Nivel mínimo requerido: {perfil.config['nivel_minimo']}")
print("=" * 60)

for item in checklist:
    print(f"Control: {item['control']}")
    print(f"  Evidencia: {item['evidencia_requerida']}")
    print()
```

---

## 9. RELACIÓN CON OTROS MARCOS

### 9.1. Alineación con Estándares Internacionales

```
┌─────────────────────────────────────────────────────────────────┐
│              ALINEACIÓN CON OTROS MARCOS                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  NIST CYBERSECURITY FRAMEWORK                                  │
│  └─ Base del Marco Uruguayo                                 │
│  └─ Adaptación al contexto nacional                          │
│                                                                 │
│  ISO/IEC 27001:2022                                           │
│  └─ Anexo A mapeado a funciones y categorías               │
│  └─ Permite certificación dual                              │
│                                                                 │
│  NIST SP 800-53                                               │
│  └─ Controles detallados como referencia                     │
│  └─ Mapeo a subcategorías                                   │
│                                                                 │
│  COBIT 2019                                                   │
│  └─ Alineación con objetivos de TI                          │
│  └─ Governanza y gestión integrada                          │
│                                                                 │
│  CIS CONTROLS v8                                             │
│  └─ Controles prioritizados para implementación              │
│  └─ Mapeo a categorías del marco                           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 9.2. Tabla de Mapeo Simplificada

| Función Uruguay | NIST CSF | ISO 27001 Anexo A | CIS Controls |
|-----------------|----------|-------------------|--------------|
| **IDENTIFY** | ID | A.5, A.6, A.8 | IG-1, IG-2 |
| **PROTECT** | PR | A.7, A.8, A.9, A.10, A.11, A.12, A.13, A.14, A.15, A.16, A.18 | |
| **DETECT** | DE | A.12, A.16, A.18 | |
| **RESPOND** | RS | A.16, A.17 | |
| **RECOVER** | RC | A.17, A.18 | |

---

## 10. GUÍA DE IMPLEMENTACIÓN

### 10.1. Pasos para Implementar

```
┌─────────────────────────────────────────────────────────────────┐
│              GUÍA DE IMPLEMENTACIÓN DEL MARCO                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  PASO 1: PREPARACIÓN ORGANIZACIONAL                            │
│  ─────────────────────────────────                             │
│  □ Obtener patrocinio de la dirección                         │
│  □ Definir alcance del proceso                                │
│  □ Identificar equipo de trabajo                              │
│  □ Establecer cronograma                                      │
│                                                                 │
│  PASO 2: EVALUACIÓN ACTUAL                                    │
│  ─────────────────────────                                     │
│  □ Completar evaluación de madurez actual                     │
│  □ Documentar controles implementados                         │
│  □ Identificar gaps vs perfil objetivo                        │
│  □ Priorizar berdasarkan riesgo y factibilidad               │
│                                                                 │
│  PASO 3: DISEÑO DE MEJORA                                    │
│  ─────────────────────                                         │
│  □ Definir perfil objetivo                                    │
│  □ Seleccionar controles a implementar                       │
│  □ Diseñar plan de implementación                             │
│  □ Asignar recursos y responsables                            │
│                                                                 │
│  PASO 4: IMPLEMENTACIÓN                                       │
│  ─────────────────                                             │
│  □ Implementar controles seleccionados                       │
│  □ Documentar evidencia de implementación                     │
│  □ Capacitar personal                                       │
│  □ Ejecutar pruebas de efectividad                           │
│                                                                 │
│  PASO 5: MONITOREO Y MEJORA                                   │
│  ─────────────────────────                                     │
│  □ Medir efectividad de controles                           │
│  □ Realizar auditorías internas                               │
│  □ Identificar nuevas mejoras                                │
│  □ Actualizar evaluación de madurez                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 10.2. Template de Evaluación

```markdown
# EVALUACIÓN DE MADUREZ - MARCO DE CIBERSEGURIDAD URUGUAY

## INFORMACIÓN DEL ORGANISMO

| Campo | Valor |
|-------|-------|
| Nombre | |
| Sigla | |
| Fecha evaluación | |
| Evaluador | |
| Versión marco | 5.0 |

---

## RESULTADOS POR FUNCIÓN

### IDENTIFY (Identificar)

| Subcategoría | Respuesta | Evidencia | Nivel | Observaciones |
|--------------|-----------|-----------|-------|---------------|
| ID.AM-1 | 0-5 | | | |
| ID.AM-2 | 0-5 | | | |
| ID.BE-1 | 0-5 | | | |
| ... | | | | |

**Puntuación función:** ___%

### PROTECT (Proteger)

[Tabla similar]

### DETECT (Detectar)

[Tabla similar]

### RESPOND (Responder)

[Tabla similar]

### RECOVER (Recuperar)

[Tabla similar]

---

## RESUMEN DE EVALUACIÓN

| Función | Puntuación | Nivel Actual | Nivel Objetivo | Gap |
|---------|------------|--------------|----------------|-----|
| IDENTIFY | | | | |
| PROTECT | | | | |
| DETECT | | | | |
| RESPOND | | | | |
| RECOVER | | | | |
| **PROMEDIO** | | | | |

---

## PLAN DE ACCIÓN

| N° | Control | Prioridad | Responsable | Fecha | Estado |
|----|---------|-----------|--------------|-------|--------|
| 1 | | Alta/Media/Baja | | | |
| 2 | | | | | |
```

---

## 11. RECURSOS Y REFERENCIAS

### 11.1. Documentos Oficiales

| Recurso | Descripción | Link |
|---------|-------------|------|
| Marco v5.0 | Documento oficial del marco | Portal AGESIC |
| Guía de Implementación | Instrucciones de uso | Portal AGESIC |
| Plantillas | Herramientas de evaluación | Portal AGESIC |
| Casos de Uso | Ejemplos sectoriales | Portal AGESIC |

### 11.2. Contactos

| Organismo | Contacto |
|-----------|----------|
| **AGESIC** | agesic@agesic.gub.uy |
| **CERT-UY** | cert-uy@agesic.gub.uy |
| **Portal** | www.agesic.gub.uy |

---

## 12. RELACIÓN CON NIST CSF

### 12.1. Mapeo Completo de Funciones y Categorías

| Función | Descripción | Categorías |
|---------|-------------|------------|
| **ID** | Identificar | AM, BE, GV, RA, RM, SC |
| **PR** | Proteger | AC, AT, DS, IP, MA, PT |
| **DE** | Detectar | AE, CM |
| **RS** | Responder | RP, CO, AN, MI, IM |
| **RC** | Recuperar | RP, IM, CO, RS |

### 12.2. Subcategorías Detalladas (Extracto)

```
ID.AM: Gestión de Activos
├─ ID.AM-1: Inventario de dispositivos
├─ ID.AM-2: Inventario de software
├─ ID.AM-3: Inventario de información
├─ ID.AM-4: Dependencias externas
├─ ID.AM-5: Amenazas externas mapeadas
└─ ID.AM-6: Roles y responsabilidades

ID.RA: Evaluación de Riesgos
├─ ID.RA-1: Identificación de amenazas
├─ ID.RA-2: Identificación de vulnerabilidades
├─ ID.RA-3: Análisis de impacto
├─ ID.RA-4: Análisis de probabilidad
├─ ID.RA-5: Determinación de riesgo
└─ ID.RA-6: Respuesta a riesgos

PR.AC: Gestión de Acceso
├─ PR.AC-1: Políticas de acceso
├─ PR.AC-2: Gestión de identidades
├─ PR.AC-3: Control de acceso físico
├─ PR.AC-4: Control de acceso lógico
├─ PR.AC-5: Autenticación robusta
└─ PR.AC-6: Cuentas privilegiadas
```

---

**Documento:** Marco de Ciberseguridad de Uruguay - AGESIC  
**Versión:** 5.0  
**Última actualización:** 2026
