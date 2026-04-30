# 📋 Tareas de Análisis de Riesgos y Modelado de Amenazas

**Duración de la presentación:** 10-15 minutos por grupo  
**Objetivo:** Aplicar metodologías de análisis de riesgos y threat modeling a escenarios reales. Fomentar la propuesta de trabajo de los estudiantes y el intercambio con el docente.
**Metodologías sugeridas:** STRIDE, DREAD, MITRE ATT&CK, NIST, ISO 27001

Cada grupo debe seleccionar un tema y enviar un correo a apastorini@gmail.com
Con:
Asunto: Tarea 2 ISI 2026
Copia a todos los integrantes
Tres escenarios, ordenados por preferencia.
---

## Escenario 1: Sistema de Banking Digital

Asignado
Mauro Mascheroni 
Ximena Gonzalez

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

Ignacio González 
Mathias Pessaj
Sebastián Di Loreto

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

## Criterios de evaluación según escenario

1. **Identificación de activos** (15%): Todos los activos críticos documentados
2. **Diagrama de arquitectura** (15%): Claro, con trust boundaries
3. **Aplicación de metodología** (20%): STRIDE/DREAD correctamente usado
4. **Profundidad del análisis** (20%): Amenazas realistas y completas
5. **Plan de mitigación** (20%): Controles viables y priorizados
6. **Calidad de documentación** (10%): Claro y ordenado


---

## Repositorio de Documentación Técnica 

### 1. Gestión de Riesgos y Activos 
Documentación para el inventario de activos y la matriz de riesgos según normativas locales e internacionales.

*   **Agesic - Metodología de Gestión de Riesgos (MGR):** [https://www.gub.uy/agencia-gobierno-electronico-sociedad-informacion-conocimiento/comunicacion/publicaciones/metodologia-gestion-riesgos-v20](https://www.gub.uy/agencia-gobierno-electronico-sociedad-informacion-conocimiento/comunicacion/publicaciones/metodologia-gestion-riesgos-v20)
    *   *Nota:* En la sección "Descargas" de ese link están las planillas Excel para la Matriz de Riesgos.
*   **NIST SP 800-30 Rev. 1 (PDF):** [https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-30r1.pdf](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-30r1.pdf)
*   **NIST SP 800-53 Rev. 5 (Controles):** [https://csrc.nist.gov/pubs/sp/800/53/r5/final](https://csrc.nist.gov/pubs/sp/800/53/r5/final)

### 2. Modelado de Amenazas (STRIDE / DREAD)
Herramientas para identificar y categorizar amenazas en los flujos de datos.

*   **Microsoft Threat Modeling Tool (Download):** [https://aka.ms/threatmodelingtool](https://aka.ms/threatmodelingtool)
*   **OWASP Threat Dragon (App):** [https://threatdragon.org/](https://threatdragon.org/)
*   **MITRE ATT&CK Navigator:** [https://mitre-attack.github.io/attack-navigator/](https://mitre-attack.github.io/attack-navigator/)

### 3. Privacidad y Arquitectura
Recursos para cumplimiento de HIPAA/PHI (Escenario 3) y diseño de diagramas.

*   **Agesic - Guía de Evaluación de Impacto (Protección de Datos):** [https://www.gub.uy/unidad-reguladora-control-datos-personales/comunicacion/publicaciones/guia-evaluacion-impacto-proteccion-datos-personales](https://www.gub.uy/unidad-reguladora-control-datos-personales/comunicacion/publicaciones/guia-evaluacion-impacto-proteccion-datos-personales)
*   **NIST SP 800-66 (HIPAA/Salud):** [https://csrc.nist.gov/pubs/sp/800/66/r2/final](https://csrc.nist.gov/pubs/sp/800/66/r2/final)
*   **Plantilla de Arquitectura de Seguridad (SABSA/ISO):** [https://www.pro-academic.co.uk/wp-content/uploads/2018/11/Security-Architecture-Document-SAD-Template.docx](https://www.pro-academic.co.uk/wp-content/uploads/2018/11/Security-Architecture-Document-SAD-Template.docx)

---

##  Trust Boundaries y Flujos de Datos

En el contexto de esta tarea, un diagrama de arquitectura no es meramente funcional, sino que debe servir como base para el análisis de seguridad. La clave está en la identificación de los **Trust Boundaries** (Fronteras de Confianza).

### Implementación Técnica de Fronteras
Una frontera de confianza ocurre en cualquier punto donde el nivel de confianza de los datos cambia. En la práctica, esto implica:

1.  **Segmentación por Interfaz:** Cada vez que un dato pasa de una red externa (Internet) a una red interna (VLAN de Aplicación), debe haber una frontera de confianza. Esto es crítico para identificar amenazas de **Spoofing** y **Information Disclosure**.
2.  **Aislamiento de Persistencia:** Las bases de datos nunca deben estar en la misma zona que el servidor web. Dibujar una frontera entre el Backend y la DB permite justificar controles como el cifrado en reposo y el uso de cuentas de servicio con privilegios mínimos.
3.  **Actores y Roles:** El diagrama debe diferenciar claramente el acceso de un "Usuario Final" frente a un "Administrador". Cada uno tiene una frontera de confianza distinta hacia el sistema.

Al presentar el análisis, el error común es listar amenazas genéricas. Para evitarlo, vincula cada amenaza de tu lista STRIDE con una frontera específica del diagrama. Por ejemplo: *"Amenaza T1 (Tampering) en la frontera entre App Móvil y API Gateway: Mitigada mediante validación de firmas JWT y mTLS"*.

---

## 1. Identificación de Activos Críticos
**Procedimiento:**
Elabora un inventario tabulado de todos los elementos con valor para el negocio. Debes dividirlos en:
*   **Activos de Información:** Bases de datos de clientes, saldos, historias clínicas.
*   **Activos de Software:** Microservicios, código de la App, lógica de negocio.
*   **Activos de Infraestructura:** Servidores cloud, bases de datos PostgreSQL/MongoDB.

**Por qué:**
Establece el alcance de la protección. Sin un inventario, el análisis de riesgos es incompleto porque no se conoce qué se está intentando proteger ni qué impacto tendría su pérdida.

**Estructura del Template:**
| ID | Activo | Tipo | C (Confidencialidad) | I (Integridad) | A (Disponibilidad) | Criticidad |
|----|--------|------|----------------------|----------------|-------------------|------------|
| A1 | DB Usuarios | Datos | Alta | Alta | Media | Crítica |

**Cómo llenarlo:** Asigna valores (Baja/Media/Alta) según el daño que causaría la filtración (C), la alteración (I) o la caída (A) del activo.

---

## 2. Diagrama de Arquitectura y Trust Boundaries
**Procedimiento:**
Dibuja los componentes del sistema y traza líneas de flujo de datos. Sobre este dibujo, añade perímetros de seguridad:
1.  **Zona Externa:** Todo lo que no controlas (Internet).
2.  **Zona Perimetral:** El punto de entrada (API Gateway/WAF).
3.  **Zona Interna:** Servidores de aplicación y bases de datos.
4.  **Trust Boundaries:** Líneas que marcan el paso entre estas zonas.

**Por qué:**
Las vulnerabilidades suelen concentrarse en los puntos donde los datos cruzan de una zona con poco control a una zona protegida. Visualizar estas fronteras permite identificar dónde aplicar validaciones.

---

## 3. Identificación de Amenazas (STRIDE)
**Procedimiento:**
Analiza cada flujo que atraviesa una frontera de confianza usando las categorías STRIDE:
*   **Spoofing:** ¿Puede alguien hacerse pasar por un usuario o servicio?
*   **Tampering:** ¿Se pueden modificar los datos en tránsito o en la base de datos?
*   **Repudiation:** ¿Puede un usuario negar que realizó una transferencia o pago?
*   **Information Disclosure:** ¿Hay datos sensibles expuestos en logs o mensajes de error?
*   **Denial of Service:** ¿Se puede saturar el backend para dejarlo inoperativo?
*   **Elevation of Privilege:** ¿Puede un usuario normal acceder a funciones de administrador?

**Por qué:**
Asegura que el análisis sea sistemático y no dependa únicamente de la intuición del analista, cubriendo vectores de ataque lógicos y técnicos.

---

## 4. Priorización de Amenazas (DREAD)
**Procedimiento:**
Evalúa cada amenaza detectada asignando un puntaje del 1 al 10 en:
*   **Damage:** Qué tan grave es el daño.
*   **Reproducibility:** Qué tan fácil es repetir el ataque.
*   **Exploitability:** Qué tanto esfuerzo técnico requiere el ataque.
*   **Affected Users:** A cuántos usuarios impacta.
*   **Discoverability:** Qué tan fácil es encontrar la vulnerabilidad.

**Por qué:**
Permite gestionar los recursos de forma eficiente, enfocando el trabajo en las amenazas que representan un riesgo real y alto para la organización.

---

## 5. Matriz de Controles de Seguridad
**Procedimiento:**
Por cada amenaza de alta prioridad, define una contramedida específica.

**Estructura del Template:**
| ID Amenaza | Descripción STRIDE | Control Propuesto | Estándar Referencia |
|------------|--------------------|-------------------|---------------------|
| T1 | Modificación de saldos en tránsito | Implementación de TLS 1.3 y firmas digitales | ISO 27001 A.10.1 |

**Cómo llenarlo:** En la columna "Control Propuesto", describe la solución técnica (ej. Hashing para integridad, MFA para autenticación).

---

## 6. Documento de Análisis de Riesgos (NIST SP 800-30)
**Procedimiento:**
Este es el entregable final que consolida los pasos anteriores en un informe formal.

**Estructura del Template:**
1.  **Introducción:** Alcance del sistema analizado.
2.  **Identificación de Riesgos:** Listado de amenazas (STRIDE) y activos asociados.
3.  **Análisis de Impacto y Probabilidad:** Resultados de la evaluación DREAD.
4.  **Recomendaciones de Mitigación:** La matriz de controles.
5.  **Riesgo Residual:** Evaluación del nivel de riesgo que permanece tras aplicar las soluciones.

**Cómo llenarlo:**
*   **Riesgo Inherente:** Es el riesgo inicial (Impacto x Probabilidad).
*   **Riesgo Residual:** Debes justificar por qué el control sugerido baja el puntaje inicial a un nivel aceptable para la empresa.

**Por qué:**
Es el estándar internacional para comunicar hallazgos técnicos a la dirección de la empresa de manera que puedan tomar decisiones informadas sobre la inversión en seguridad.