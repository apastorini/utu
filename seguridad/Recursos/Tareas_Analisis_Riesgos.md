# 📋 Tareas de Análisis de Riesgos y Modelado de Amenazas

**Duración de la presentación:** 10-15 minutos por grupo  
**Objetivo:** Aplicar metodologías de análisis de riesgos y threat modeling a escenarios reales  
**Metodologías sugeridas:** STRIDE, DREAD, MITRE ATT&CK, NIST, ISO 27001

Cada grupo debe seleccionar un tema y enviar un correo a apastorini@gmail.com
Con:
Asunto: Tarea 2 ISI 2026
Copia a todos los integrantes
Tres escenarios, ordenados por preferencia.
---

## Escenario 1: Sistema de Banking Digital

**Contexto:**
Una fintech está desarrollando una aplicación móvil de banca que permite a usuarios:
- Consultar saldo y movimientos
- Transferencias entre cuentas
- Pagos de servicios
- Préstamos online
- Inversión en fondos

**Alcance del análisis:**
- App móvil (iOS/Android)
- API Backend (REST)
- Base de datos PostgreSQL
- Integración con pasarela de pagos
- Notificaciones push

**Actividades requeridas:**
1. Identificar y documentar todos los activos críticos
2. Crear diagrama de arquitectura con actores
3. Aplicar STRIDE para identificar amenazas
4. Priorizar amenazas con DREAD
5. Crear matriz de controles de seguridad
6. Documentar riesgos residuales

**Entregables:**
- Documento de análisis de riesgos (formato NIST)
- Diagrama de arquitectura con trust boundaries
- Lista de amenazas priorizadas
- Plan de mitigación

---

## Escenario 2: Plataforma de E-C

Asingado:
Andres Varela, Pablo Morales y Horacio Duarte

**Contexto:**
Una tienda online con las siguientes funcionalidades:
- Catálogo de productos con búsqueda
- Carrito de compras y checkout
- Múltiples métodos de pago
- Panel de administración
- Programa de fidelización
- Chat con clientes

**Alcance del análisis:**
- Frontend React
- Backend Node.js
- Base de datos MongoDB
- Redis para caché
- CDN para assets estáticos
- WebSocket para chat

**Actividades requeridas:**
1. Modelar amenazas con STRIDE
2. Identificar attack surfaces
3. Analizar flujos de datos sensibles
4. Evaluar riesgos de integración con procesadores de pago
5. Documentar amenazas específicas de e-commerce (fraud detection, inventory manipulation)

**Entregables:**
- Diagrama de data flow
- Inventario de amenazas por categoría STRIDE
- Risk assessment report
- Recomendaciones de arquitectura

---

## Escenario 3: Sistema de Salud - Historias Clínicas Electrónicas

Asingado
Bibiana Fariello, Paola Benedictti


**Contexto:**
Un hospital implementa un sistema de HCE con:
- Registro de pacientes
- Notas de evolución médica
- Prescripción de medicamentos
- Resultados de laboratorio
- Imágenes médicas (DICOM)
- Portal para pacientes

**Alcance del análisis:**
- Aplicación web (React)
- API REST + FHIR
- Base de datos MySQL
- PACS para imágenes
- Integración con laboratorio externo

**Actividades requeridas:**
1. Identificar activos de alta criticidad (datos de salud = PHI)
2. Cumplir con consideraciones de HIPAA/GDPR
3. Threat modeling para datos médicos
4. Analizar riesgos de interoperabilidad
5. Evaluar controles de acceso a datos sensibles

**Entregables:**
- Risk assessment conforme a NIST SP 800-66
- Análisis de compliance (HIPAA, GDPR)
- Matriz de controls de seguridad
- Privacy impact assessment

---

## Escenario 4: Plataforma de Educación Online (LMS)
Asingado
Nazarena Valiero, Simon Corvo


**Contexto:**
Una plataforma de e-learning con:
- Cursos en video
- Exámenes y evaluaciones
- Foros de discusión
- Certificados digitales
- Panel de progreso
- Gamificación

**Alcance del análisis:**
- Frontend Vue.js
- Backend Python/Django
- PostgreSQL
- CDN para video
- Integración con API de certificates

**Actividades requeridas:**
1. Threat modeling del flujo de certificación
2. Analizar riesgos de cheating en exámenes
3. Evaluar protección de contenido intelectual
4. Identificar amenazas en interacción social (foros)
5. Assessment de privacidad de datos de menores (COPPA)

**Entregables:**
- Documento de análisis de amenazas
- Evaluación de privacidad
- Controles para integridad académica
- Guía de compliance

---

## Escenario 5: IoT - Sistema de Domótica Smart 

Asingado
Renzo Rampoldi , Felipe Queirolo

**Contexto:**
Sistema de automatización del hogar:
- Control de iluminación
- Termostato inteligente
- cerraduras electrónicas
- Cámaras de seguridad
- Asistentes de voz
- Sensores de movimiento/temperatura

**Alcance del análisis:**
- IoT devices (various protocols)
- Hub central
- Aplicación móvil
- Cloud backend
- Integraciones con Alexa/Google Home

**Actividades requeridas:**
1. Mapear superficie de ataque IoT
2. Analizar protocolos (Zigbee, Z-Wave, WiFi)
3. Threat modeling de dispositivos críticos (cerraduras)
4. Evaluar riesgos de integración con asistentes
5. Analizar amenazas de firmware

**Entregables:**
- Inventario de activos IoT
- Análisis de amenazas por dispositivo
- Evaluación de riesgos de comunicaciones
- Recomendaciones de seguridad IoT

---

## Escenario 6: Sistema de Recursos Humanos (HRIS)

Asingado
Luis Andrada, Leonardo Gimenez

**Contexto:**
Plataforma de gestión de RRHH:
- Nóminas y liquidaciones
- Gestión de beneficios
- Evaluaciones de desempeño
- Portal de empleados
- Onboarding digital
- Generación de contratos

**Alcance del análisis:**
- Aplicación web
- Backend Java/Spring
- Integración con sistemas de nómina
- Base de datos Oracle
- Firma digital de documentos

**Actividades requeridas:**
1. Identificar datos de alta sensibilidad (salarios, beneficios)
2. Threat modeling con STRIDE
3. Analizar riesgos de insider threats
4. Evaluar controles de acceso basados en roles
5. Assessment de continuidad de negocio

**Entregables:**
- Risk register
- Análisis de amenazas internas
- Controles de acceso documentados
- Plan de continuidad

---

## Escenario 7: API Gateway para Microservicios

**Contexto:**
Arquitectura de microservicios con:
- API Gateway central
- Autenticación/Authorization (OAuth2, JWT)
- Service Mesh
- Logging centralizado
- Circuit breakers
- Rate limiting

**Alcance del análisis:**
- Kong/AWS API Gateway
- Kubernetes cluster
- Multiple microservices (inventory, orders, users)
- Service-to-service communication (mTLS)
- Redis/Message queue

**Actividades requeridas:**
1. Modelar amenazas de arquitectura de microservicios
2. Analizar riesgos de API Gateway
3. Evaluar comunicación entre servicios
4. Threat modeling de service mesh
5. Analizar riesgos de configuración de Kubernetes

**Entregables:**
- Arquitectura de seguridad documentada
- Amenazas por componente
- Controles de seguridad en gateway
- Kubernetes security assessment

---

## Escenario 8: Sistema de Votación Electrónica
Asingado
Francisco Ancheta
Damazo Tor
Diego Koci


**Contexto:**
Plataforma de votación digital para elecciones organizacionales:
- Registro de votantes
- Autenticación de identidad
- Emisión de voto (anonimato)
- Escrutinio automático
- Resultados en tiempo real
- Auditoría completa

**Alcance del análisis:**
- Aplicación web/móvil
- Backend con cifrado homomórfico
- Blockchain para audit trail
- Sistema de encriptación de votos

**Actividades requeridas:**
1. Análisis de amenazas específico para sistemas de votación
2. Modelar requisitos de seguridad (integridad, anonimalidad, verificabilidad)
3. Threat modeling con enfoque en manipulación de resultados
4. Evaluar riesgos de coerción/voto coercion
5. Análisis de privacidad del votante

**Entregables:**
- Documento de requisitos de seguridad
- Análisis de amenazas específicas
- Matriz de controles de integridad
- Evaluación de anonimalidad

---

## Escenario 9: Plataforma drides (Ridesharing)

**Contexto:**
Aplicación tipo Uber con:
- Geolocalización en tiempo real
- Matching conductor-pasajero
- Sistema de pagos integrado
- Ratings y reviews
- Chat in-app
- Historia de viajes

**Alcance del análisis:**
- App móvil (iOS/Android)
- Backend Node.js
- PostgreSQL + Redis
- Google Maps API
- Stripe/pagos

**Actividades requeridas:**
1. Threat modeling de datos de ubicación
2. Analizar riesgos de privacidad GPS
3. Evaluar seguridad de pagos
4. Assessment de comunicación en tiempo real
5. Análisis de fraude en transacciones

**Entregables:**
- Privacy impact assessment (ubicación)
- Análisis de amenazas de geolocalización
- Controles de seguridad en pagos
- Evaluación de fraude

---

## Escenario 10: Industrial Control System (SCADA/ICS)

**Contexto:**
Sistema de control industrial para planta manufacturera:
- Control de procesos productivos
- Monitoring de sensores
- Control de PLCs
- Alertas y alarmas
- Reporting de producción
- Integración con ERP

**Alcance del análisis:**
- SCADA/HMI
- PLCs (Siemens, Allen Bradley)
- Red industrial (PROFINET, EtherNet/IP)
- Historian server
- Integración con corporate network

**Actividades requeridas:**
1. Análisis de amenazas a entornos OT/ICS
2. Identificar activos críticos de planta
3. Modelar amenazas con enfoque IT/OT
4. Evaluar riesgos de acceso remoto
5. Assessment de segmentación de red

**Entregables:**
- Risk assessment OT
- Inventario de activos ICS
- Análisis de amenazas IT/OT
- Plan de segmentación
- Controles de acceso remoto

---

## Metodologías a Utilizar

| Metodología | Uso | Herramientas |
|-------------|-----|---------------|
| **STRIDE** | Categorización de amenazas | Microsoft TMT, OWASP Threat Dragon |
| **DREAD** | Priorización de riesgos | Plantilla propia |
| **MITRE ATT&CK** | Tactics y techniques | MITRE ATT&CK Navigator |
| **NIST SP 800-30** | Análisis de riesgos | Plantillas NIST |
| **ISO 27001** | Gestión de riesgos | Frameworks ISO |
| **PASTA** | Proceso de threat modeling | Metodología complementaria |

---

## Herramientas Recomendadas

| Herramienta | Tipo | Descripción |
|-------------|------|-------------|
| **OWASP Threat Dragon** | Diagramación | Código abierto para threat modeling |
| **Microsoft TMT** | Desktop app | Threat Modeling Tool |
| **draw.io** | Diagramación | Diagramas de arquitectura |
| **MITRE ATT&CK Navigator** | Visualización | Mapeo de amenazas |
| **Risk Radar** | Gestión | Risk register |
| ** OWASP Risk Rating Framework** | Metodología | Plantilla de riesgos |

---

## Criterios de Evaluación por Escenario

1. **Identificación de activos** (15%): Todos los activos críticos documentados
2. **Diagrama de arquitectura** (15%): Claro, con trust boundaries
3. **Aplicación de metodología** (20%): STRIDE/DREAD correctamente usado
4. **Profundidad del análisis** (20%): Amenazas realistas y completas
5. **Plan de mitigación** (20%): Controles viables y priorizados
6. **Calidad de documentación** (10%): Claro y profesional

