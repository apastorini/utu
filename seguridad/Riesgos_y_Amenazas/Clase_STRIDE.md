# Clase: STRIDE - Metodología de Microsoft para Modelado de Amenazas

## Introducción

STRIDE es una metodología de modelado de amenazas desarrollada por Microsoft que proporciona un enfoque sistemático para identificar vulnerabilidades de seguridad en sistemas de software. El acrónimo representa las seis categorías de amenazas: Spoofing (Suplantación), Tampering (Manipulación), Repudiation (No repudio), Information Disclosure (Divulgación de información), Denial of Service (Denegación de servicio) y Elevation of Privilege (Escalamiento de privilegios).

**Objetivos de aprendizaje:**
1. Comprender el marco STRIDE y sus categorías
2. Aplicar STRIDE al modelado de amenazas de sistemas
3. Identificar contramedidas para cada tipo de amenaza
4. Crear diagramas de flujo de datos para análisis
5. Documentar hallazgos de seguridad

---

## 1. Fundamentos de STRIDE

### 1.1 Origen y propósito

STRIDE fue desarrollado en la década de 1990 por Lorenzo Martignoni y Praerit Garg en Microsoft como parte del proceso de desarrollo de productos seguros. El objetivo era proporcionar un método estructurado para que los desarrolladores identificaran amenazas durante las fases de diseño de software.

### 1.2 El acrónimo

| Letra | Categoría | Definición | Contrapartida de seguridad |
|-------|-----------|------------|---------------------------|
| **S** | Spoofing | Suplantar la identidad de alguien o algo | Autenticación |
| **T** | Tampering | Modificar datos o código sin autorización | Integridad |
| **R** | Repudiation | Negar haber realizado una acción | No repudio |
| **I** | Information Disclosure | Exponer información a personas no autorizadas | Confidencialidad |
| **D** | Denial of Service | Denegar el servicio a usuarios legítimos | Disponibilidad |
| **E** | Elevation of Privilege | Obtener capacidades no autorizadas | Autorización |

### 1.3 Relación con CIA Triad

```
┌─────────────────────────────────────────────────────────────┐
│                    MODELO STRIDE                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│     S ─────────▶ Autenticación ────────▶ Spoofing          │
│     T ─────────▶ Integridad ───────────▶ Tampering         │
│     R ─────────▶ No repudio ───────────▶ Repudiation        │
│     I ─────────▶ Confidencialidad ────▶ Info Disclosure    │
│     D ─────────▶ Disponibilidad ──────▶ Denial of Service │
│     E ─────────▶ Autorización ────────▶ Elevation of Priv│
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. El Proceso de Modelado con STRIDE

### 2.1 Pasos del proceso

```
┌─────────────────────────────────────────────────────────────┐
│           PROCESO DE MODELADO DE AMENAZAS STRIDE            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   1. IDENTIFICAR ACTIVOS        4. IDENTIFICAR AMENAZAS   │
│      ¿Qué estamos protegiendo?     ¿Qué puede salir mal?    │
│                                                             │
│            │                               │                │
│            ▼                               ▼                │
│   2. CREAR DIAGRAMA DFD         5. DOCUMENTAR RIESGOS     │
│      ¿Cómo fluyen los datos?      Registro de hallazgos    │
│                                                             │
│            │                               │                │
│            ▼                               ▼                │
│   3. DIVIDIR EL SISTEMA                                         │
│      ¿Dónde están los límites?                                │
│                                                             │
│                              6. MITIGAR AMENAZAS            │
│                              ¿Qué hacemos al respecto?      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 Paso 1: Identificar activos

**Activos típicos en aplicaciones:**

| Categoría | Ejemplos |
|-----------|----------|
| **Datos de usuario** | Nombres, direcciones, datos financieros |
| **Credenciales** | Contraseñas, tokens, certificados |
| **Datos de negocio** | Transacciones, inventario, precios |
| **Infraestructura** | Llaves de cifrado, configuraciones |
| **Servicio** | Disponibilidad del sistema |

### 2.3 Paso 2: Crear diagrama DFD

**Elementos del DFD:**

| Elemento | Representación | Descripción |
|----------|---------------|-------------|
| **Proceso** | Círculo | Código en ejecución |
| **Flujo de datos** | Flecha | Movimiento de datos |
| **Almacén de datos** | Líneas paralelas | Archivos, BD, queues |
| **Interactor** | Cuadrado | Usuarios, sistemas externos |
| **Confianza** | Línea punteada | Límite de confianza |

**Ejemplo: Sistema de banca online**

```
┌──────────┐                              ┌──────────┐
│ USUARIO  │                              │ SISTEMA  │
│ WEB      │                              │ BCU/     │
│          │                              │ SWIFT    │
└────┬─────┘                              └────┬─────┘
     │                                         │
     │ HTTPS                                  │ SOAP/REST
     │                                        │
     ▼                                        ▼
┌─────────────────────────────────────────────────────────┐
│                     DMZ                                │
│  ┌─────────────┐    ┌─────────────┐                   │
│  │ WEB SERVER  │───▶│  LOAD       │                   │
│  │             │    │  BALANCER    │                   │
│  └─────────────┘    └─────────────┘                   │
└─────────────────────────────────────────────────────────┘
                     │
                     │ Intern
                     ▼
┌─────────────────────────────────────────────────────────┐
│                   RED INTERNA                            │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐ │
│  │ APP SERVER  │───▶│  DATABASE   │    │  MESSAGE    │ │
│  │             │    │  CLUSTER    │    │  QUEUE      │ │
│  └─────────────┘    └─────────────┘    └─────────────┘ │
└─────────────────────────────────────────────────────────┘
```

---

## 3. Análisis Detallado por Categoría STRIDE

### 3.1 S - Spoofing (Suplantación)

**Definición:** Impersonificar a alguien o algo legítimo para obtener acceso no autorizado.

**Ejemplos:**
- Credenciales robadas de un usuario legítimo
- Spoofing de IP o DNS para redirigir tráfico
- Certificados SSL falsos
- Suplantación de un servidor de aplicaciones

**Contramedidas:**

| Contramedida | Implementación |
|--------------|---------------|
| Autenticación fuerte | MFA, certificados cliente |
| Sesiones seguras | Tokens con tiempo de expiración |
| Certificados digitales | PKI, TLS mutuo |
| Logging de autenticación | Registro de intentos y éxitos |

**Preguntas para identificar spoofing:**
- ¿Cómo se autentica un usuario?
- ¿Se pueden falsificar las credenciales?
- ¿Hay protección contra credential stuffing?
- ¿Se valida la identidad de servicios externos?

### 3.2 T - Tampering (Manipulación)

**Definición:** Modificar datos, archivos o código sin autorización.

**Ejemplos:**
- Modificación de transacciones financieras
- Inyección de código SQL
- Alteración de archivos de configuración
- Modificación de logs para ocultar actividad

**Contramedidas:**

| Contramedida | Implementación |
|--------------|---------------|
| Integridad de datos | Hashing, firmas digitales |
| Validación de entrada | Sanitización de inputs |
| Control de versiones | Auditoría de cambios |
| Inmutabilidad | WORM storage para logs |

**Preguntas para identificar tampering:**
- ¿Quién puede modificar los datos?
- ¿Hay validación de integridad?
- ¿Se auditan los cambios?
- ¿Cómo se protege contra SQL injection?

### 3.3 R - Repudiation (No repudio)

**Definición:** Capacidad de negar haber realizado una acción que realmente se realizó.

**Ejemplos:**
- Usuario niega haber enviado una transacción
- Administrador niega haber modificado configuraciones
- Sistema否认 haber enviado un mensaje

**Contramedidas:**

| Contramedida | Implementación |
|--------------|---------------|
| Logging inmutable | Registro con hash chain |
| Firmas digitales | Non-repudiation de mensajes |
| Timestamps confiables | NTP sincronizado, TSA |
| Segregación de duties | Múltiples aprobaciones |

**Preguntas para identificar repudiation:**
- ¿Se registran todas las acciones importantes?
- ¿Son los logs a prueba de manipulación?
- ¿Hay firm digitales de transacciones?
- ¿Se puede probar quién hizo qué y cuándo?

### 3.4 I - Information Disclosure (Divulgación de información)

**Definición:** Exponer información confidencial a personas no autorizadas.

**Ejemplos:**
- Breach de base de datos de clientes
- Interceptación de comunicaciones (MITM)
- Archivos de configuración expuestos
- Mensajes de error demasiado detallados

**Contramedidas:**

| Contramedida | Implementación |
|--------------|---------------|
| Cifrado | TLS, cifrado en BD, tokenización |
| Control de acceso | RBAC, mínimo privilegio |
| Minimización de datos | No almacenar datos innecesarios |
| Manejo de errores | Mensajes genéricos al usuario |

**Preguntas para identificar information disclosure:**
- ¿Qué datos sensibles existen?
- ¿Cómo se protege la confidencialidad?
- ¿Hay datos innecesarios en logs o respuestas?
- ¿Están cifradas las comunicaciones?

### 3.5 D - Denial of Service (Denegación de servicio)

**Definición:** Impedir que usuarios legítimos accedan a un servicio.

**Ejemplos:**
- Ataque DDoS a servidores web
- Consumo excesivo de recursos
- Inundación de base de datos
- Eliminación de datos críticos

**Contramedidas:**

| Contramedida | Implementación |
|--------------|---------------|
| Redundancia | Balanceo de carga, failover |
| Rate limiting | Control de tráfico entrante |
| Throttling | Límites de consumo de recursos |
| DDoS protection | CDN, servicios anti-DDoS |

**Preguntas para identificar DoS:**
- ¿Qué servicios son críticos?
- ¿Qué pasa si el servicio no está disponible?
- ¿Hay protección contra DDoS?
- ¿Hay límites de recursos?

### 3.6 E - Elevation of Privilege (Escalamiento de privilegios)

**Definición:** Obtener permisos mayores de los que originalmente se tenían.

**Ejemplos:**
- Usuario normal ejecuta código como admin
- SQL injection para ejecutar comandos
- Buffer overflow para shell remoto
- Abuso de configuraciones privilegiadas

**Contramedidas:**

| Contramedida | Implementación |
|--------------|---------------|
| Principio de mínimo privilegio | RBAC, just-in-time access |
| Sandboxing | Aislamiento de procesos |
| Input validation | Prevenir inyección |
| Hardening | Reducir superficie de ataque |

**Preguntas para identificar elevation of privilege:**
- ¿Qué privilegios tiene cada rol?
- ¿Se pueden escalar privilegios?
- ¿Hay validación de permisos en cada operación?
- ¿Se ejecutan procesos con más privilegios de los necesarios?

---

## 4. Matriz STRIDE para Activos Comunes

### 4.1 Matriz resumen

| Elemento | S | T | R | I | D | E |
|----------|---|---|---|---|---|---|
| **Servidor Web** | ✓ | ✓ | | ✓ | ✓ | ✓ |
| **Base de datos** | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| **API REST** | ✓ | ✓ | | ✓ | ✓ | ✓ |
| **Archivo local** | ✓ | ✓ | ✓ | ✓ | | ✓ |
| **Cola de mensajes** | ✓ | ✓ | | ✓ | ✓ | ✓ |
| **Cliente/browser** | ✓ | ✓ | | ✓ | | ✓ |
| **Sistema de archivos** | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| **Red entre procesos** | ✓ | ✓ | | ✓ | ✓ | ✓ |

### 4.2 Amenazas específicas por tipo de aplicación

**Para aplicaciones web:**

| Amenaza STRIDE | Vulnerabilidad típica |
|---------------|----------------------|
| Spoofing | Sesiones no cifradas, XSS para robar cookies |
| Tampering | XSS, CSRF, SQL injection |
| Repudiation | Falta de logs de auditoría |
| Information Disclosure | Configuración expuesta, path traversal |
| Denial of Service | Slow HTTP headers, floods |
| Elevation of Privilege | IDOR, broken access control |

**Para APIs REST:**

| Amenaza STRIDE | Vulnerabilidad típica |
|---------------|----------------------|
| Spoofing | Falta de autenticación, tokens inseguros |
| Tampering | Falta de firma de requests |
| Repudiation | No se firman las llamadas |
| Information Disclosure | Rate limiting, datos excesivos |
| Denial of Service | Sin throttling, payloads grandes |
| Elevation of Privilege | Broken Object Level Authorization |

---

## 5. Herramientas para Modelado STRIDE

### 5.1 Herramientas disponibles

| Herramienta | Tipo | Pros | Contras |
|-------------|------|------|---------|
| **Microsoft Threat Modeling Tool** | Desktop (gratuita) | Integrada con STRIDE, gratuita | Descontinuada en 2024 |
| **OWASP Threat Dragon** | Web (gratuita) | Open source, colaborativa | Menos completa |
| **IriusRisk** | Comercial | Completa, integraciones | Costosa |
| **CAIRIS** | Open source | Muy completa | Curva de aprendizaje |
| **draw.io + plantillas** | General | Flexible, fácil | Manual |

### 5.2 Ejemplo con Microsoft Threat Modeling Tool

```
┌─────────────────────────────────────────────────────────────┐
│           DIAGRAMA DE AMENAZAS - SISTEMA DE PAGOS           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│                    ┌─────────────┐                         │
│                    │  INTERNET   │                         │
│                    │   (T1)      │                         │
│                    └──────┬──────┘                         │
│                           │                                 │
│         ┌─────────────────┼─────────────────┐               │
│         │                 │                 │               │
│         ▼                 ▼                 ▼               │
│   ┌──────────┐     ┌──────────┐     ┌──────────┐         │
│   │ BROWSER  │     │ PARTNER  │     │ MOBILE   │         │
│   │ (T2)     │     │ SYSTEM   │     │ APP (T2) │         │
│   └────┬─────┘     └────┬─────┘     └────┬─────┘         │
│        │                │                │                 │
│        │ HTTPS          │ SOAP/REST      │ HTTPS          │
│        │ (T3)           │ (T3)           │ (T3)           │
│        │                │                │                 │
│        └────────────────┼────────────────┘               │
│                         │                                 │
│                         ▼                                 │
│                  ┌─────────────┐                         │
│                  │  API GATEWAY │                         │
│                  │   (T4)       │                         │
│                  └──────┬──────┘                         │
│                         │                                 │
│              ┌──────────┴──────────┐                     │
│              │                     │                       │
│              ▼                     ▼                       │
│        ┌──────────┐          ┌──────────┐                │
│        │ PAYMENT  │          │ CORE     │                │
│        │ SERVICE  │          │ BANKING  │                │
│        │ (T5)     │          │ (T6)     │                │
│        └──────────┘          └──────────┘                │
│                                                             │
│  T1 = Internet boundary                                    │
│  T2 = User boundary                                        │
│  T3 = TLS encrypted channel                                │
│  T4 = API Gateway boundary                                 │
│  T5 = Payment service boundary                             │
│  T6 = Core banking boundary                                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 6. Taller Práctico: Análisis STRIDE

### 6.1 Escenario

Sistema de transferencias bancarias entre usuarios:

**Componentes:**
1. Aplicación móvil del banco
2. API Backend de transferencias
3. Base de datos de transacciones
4. Integración con clearing local
5. Cola de mensajes asíncronos

### 6.2 Análisis STRIDE para el escenario

**Flujo: Usuario inicia transferencia**

```
Usuario → App Móvil → API → Validación → BD (transacción) → Cola → Clearing
```

**Análisis de amenazas:**

| ID | Flujo/Elemento | STRIDE | Amenaza | Contramedida |
|----|----------------|--------|---------|-------------|
| 01 | App → API | S | Suplantar identidad de usuario | MFA, OAuth2 |
| 02 | App → API | T | Modificar monto en tránsito | HTTPS + firma request |
| 03 | App → API | I | Interceptar credenciales | TLS 1.3, certificate pinning |
| 04 | API → BD | T | SQL injection | Prepared statements, WAF |
| 05 | API → BD | E | Elevación por IDOR | Validación ownership |
| 06 | API → Cola | D | DoS llenando cola | Rate limiting, quotas |
| 07 | BD | R | Negar transacción | Logging inmutable, receipts |
| 08 | Cola → Clearing | I | Exposición de datos sensibles | Tokenización, cifrado |
| 09 | Cola → Clearing | R | Partes niegan envío/recepción | ACK firmados |
| 10 | Clearing | D | Fail de sistema externo | Circuit breaker, retry |

### 6.3 Plantilla de documentación

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DOCUMENTO DE MODELADO STRIDE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SISTEMA: [Nombre del sistema]
FECHA: [Fecha]
VERSIÓN: [Versión]
ELABORADO POR: [Nombre]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DIAGRAMA DE FLUJO DE DATOS
[Incluir diagrama DFD aquí]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ANÁLISIS DE AMENAZAS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Elemento: [Nombre]
Tipo: [Proceso/Flujo/Store/Interactor]

| ID | STRIDE | Amenaza | Impacto | Probabilidad | Risk | Contramedida | Estado |
|----|--------|---------|---------|--------------|------|--------------|--------|
| | | | | | | | |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RESUMEN DE RIESGOS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Alto:
Medio:
Bajo:

ACCIONES PENDIENTES:
| # | Acción | Responsable | Fecha objetivo |
|---|--------|-------------|----------------|
| | | | |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7. Mejores Prácticas

### 7.1 Cuándo realizar el análisis

| Fase del desarrollo | Recomendación |
|-------------------|---------------|
| Conceptualización | ✓ Análisis inicial, arquitectura |
| Diseño | ✓ Análisis detallado, antes de codificar |
| Implementación | ✗ Demasiado tarde, costos altos |
| Pruebas | △ Análisis limitado, encontrar gaps |
| Producción | △ Mantener actualizado ante cambios |

### 7.2 Frecuencia de revisión

- **Anualmente:** Revisión completa del modelo
- **Ante cambios significativos:** Nuevos features, integraciones
- **Post-incidente:** Después de un breach, revisar el modelo

### 7.3 Errores comunes

1. No involucrar a los desarrolladores
2. Modelar solo la arquitectura "ideal"
3. Ignorar amenazas de denegación de servicio
4. No documentar las contramedidas
5. Tratarlo como ejercicio puntual, no continuo

---

## 8. Integración con el SDLC

### 8.1 Flujo de integración

```
┌─────────────────────────────────────────────────────────────┐
│          INTEGRACIÓN STRIDE EN EL SDLC                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐   │
│  │  REQUISITOS │───▶│    DISEÑO   │───▶│   CODIGO    │   │
│  │             │    │             │    │             │   │
│  │ -Reqs seg.  │    │ -Threat     │    │ -Seg coding │   │
│  │ -Arquitect. │    │   modeling  │    │ -SAST       │   │
│  │ -Modelo     │    │ -STRIDE     │    │ -Reviews    │   │
│  │   DFD       │    │ -Mitigac.   │    │             │   │
│  └─────────────┘    └──────┬──────┘    └──────┬──────┘   │
│                             │                     │         │
│                             ▼                     ▼         │
│                      ┌─────────────┐    ┌─────────────┐   │
│                      │   PRUEBAS   │◀───│   BUILD      │   │
│                      │             │    │             │   │
│                      │ -DAST       │    │ -SCA        │   │
│                      │ -Pen test   │    │ -Security   │   │
│                      │ -Threat     │    │   testing   │   │
│                      │   model     │    │             │   │
│                      │   update   │    │             │   │
│                      └──────┬──────┘    └─────────────┘   │
│                             │                              │
│                             ▼                              │
│                      ┌─────────────┐                       │
│                      │ DEPLOYMENT  │                       │
│                      │             │                       │
│                      │ -Hardening  │                       │
│                      │ -Secrets    │                       │
│                      │   mgmt      │                       │
│                      │ -Monitoring │                       │
│                      └─────────────┘                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Resumen

STRIDE es una metodología valiosa porque:

1. **Estructura** el análisis de amenazas de forma sistemática
2. **Cubre** las 6 categorías fundamentales de seguridad
3. **Conecta** cada amenaza con su contramedida
4. **Integra** bien con el desarrollo de software
5. **Es flexible** y adaptable a diferentes sistemas

El análisis STRIDE debe realizarse temprano en el diseño y actualizarse con cada cambio significativo en la arquitectura.

---

**Material complementario:**
- Plantilla de análisis STRIDE (en carpeta Templates)
- Guía de Microsoft Threat Modeling Tool
- OWASP Threat Modeling Cheat Sheet
- Ejercicios adicionales con diferentes arquitecturas

**Próxima clase:** DREAD - Metodología de Evaluación de Riesgos
