# CLASE 4: MAKE (INTEGROMAT) - AUTOMATIZACIÓN AVANZADA

## 📅 Duración: 4 Horas (240 minutos)

---

## 4.1 OBJETIVOS DE APRENDIZAJE

Al finalizar esta clase, los participantes serán capaces de:

1. **Dominar la interfaz de Make (Integromat)** y comprender su arquitectura de escenarios
2. **Diseñar flujos de automatización complejos** utilizando módulos, routers y filtros
3. **Integrar múltiples APIs** para crear soluciones empresariales completas
4. **Manejar errores y excepciones** de manera profesional
5. **Optimizar el rendimiento** de los escenarios para reducir costos

---

## 4.2 CONTENIDOS DETALLADOS

### MÓDULO 1: FUNDAMENTOS DE MAKE (60 minutos)

#### 4.2.1 ¿Qué es Make (Integromat)?

Make (anteriormente conocido como Integromat) es una plataforma de automatización visual que permite conectar más de 1,000 aplicaciones sin necesidad de programar código. A diferencia de Zapier, Make ofrece mayor flexibilidad y capacidades de integración profunda mediante su interfaz visual basada en escenarios.

**Características Distintivas:**

- **Interfaz Visual de Diagramas**: Cada automatización se representa como un escenario visual que puedes diseñar arrastrando y conectando módulos
- **Ejecución Flexible**: Puedes ejecutar escenarios en tiempo real, programar horarios o establecer disparadores basados en eventos
- **Manejo Avanzado de Datos**: Transformaciones, iteraciones y manipulación compleja de datos
- **Costos Competitivos**: Plan gratuito generoso y precios escalables

#### 4.2.2 Arquitectura de Make

Make se organiza en una jerarquía clara que debes comprender para usarlo efectivamente:

```
Make
├── Cuenta (Account)
│   ├── Equipos (Teams)
│   └── Organizaciones (Organizations)
│
├── Espacios de Trabajo (Workspaces)
│   ├── Carpetas (Folders)
│   └── Escenarios (Scenarios)
│
└── Recursos Compartidos
    ├── Conexiones (Connections)
    ├── Webhooks
    └── Variables Globales
```

**Conceptos Clave:**

1. **Módulo**: Cada acción o trigger en Make se llama módulo. Representa una funcionalidad específica de una aplicación.

2. **Escenario**: Un conjunto de módulos conectados que forman una automatización. Es el equivalente a un "Zap" en Zapier.

3. **Operación**: Cada vez que un módulo ejecuta una acción, consume una operación. Las operaciones son la base del cobro en Make.

4. **Ciclo de Ejecución**: Un escenario puede ejecutarse una vez (single run) o múltiples veces en un ciclo de ejecución (batch processing).

```mermaid
graph TD
    A[Make Platform] --> B[Trigger Module]
    B --> C[Action Module 1]
    C --> D[Router]
    D --> E[Action Module 2A]
    D --> F[Action Module 2B]
    E --> G[Action Module 3]
    F --> G
    G --> H[End]
    
    style A fill:#ff6b6b
    style B fill:#ffd93d
    style C fill:#69db7c
    style D fill:#74c0fc
    style E fill:#69db7c
    style F fill:#69db7c
    style G fill:#69db7c
    style H fill:#cc5de8
```

#### 4.2.3 Tipos de Módulos en Make

Make ofrece diferentes categorías de módulos que aprenderás a utilizar:

**1. Módulos de Aplicaciones**
Conectores específicos para servicios como:
- Google Workspace (Sheets, Gmail, Drive)
- Microsoft 365
- Slack, Discord
- CRM (HubSpot, Salesforce, Pipedrive)
- E-commerce (Shopify, WooCommerce)
- Redes Sociales (Instagram, Facebook, LinkedIn)
- Y más de 1,000 aplicaciones

**2. Módulos de Herramientas (Tools)**
Funciones internas de Make:
- **Set Variable**: Guardar valores para usar después
- **Set Multiple Variables**: Guardar múltiples valores
- **Get Variable**: Recuperar valores guardados
- **Text Parser**: Procesar y extraer texto
- **HTML**: Convertir y manipular HTML
- **XML**: Procesar datos XML
- **Date/Time**: Manipular fechas y tiempos
- **Math**: Operaciones matemáticas
- **Basic Operators**: Comparaciones y lógica

**3. Módulos de Iteración y Arrays**
- **Iterator**: Procesar arrays elemento por elemento
- **Array Aggregator**: Combinar resultados en un array
- **Text Aggregator**: Combinar texto
- **Numeric Aggregator**: Sumas y cálculos

**4. Módulos de Flow Control**
- **Router**: Dirigir datos por diferentes caminos
- **Filter**: Condicionar el flujo
- **Repeater**: Repetir acciones X veces
- **Sleep**: Pausar la ejecución
- **Jump**: Saltar a otro módulo

---

### MÓDULO 2: DISEÑO DE ESCENARIOS AVANZADOS (60 minutos)

#### 4.2.4 El Router: Control de Flujo

El router es uno de los módulos más poderosos de Make. Permite dividir tu flujo en múltiples caminos basados en condiciones.

**Estructura del Router:**

```
[Trigger] --> [Router] --> [Ruta 1: Condition A]
                  --> [Ruta 2: Condition B]
                  --> [Ruta 3: Default/No Match]
```

**Ejemplo Práctico - Clasificación de Leads:**

Imaginemos un escenario que recibe leads de un formulario y los clasifica según su presupuesto:

1. **Trigger**: Webhook recibe datos del formulario
2. **Router**: Evalúa el campo "presupuesto"
3. **Ruta 1**: Si presupuesto > $10,000 → Enviar a equipo Premium
4. **Ruta 2**: Si presupuesto $1,000-$10,000 → Enviar a equipo Estándar
5. **Ruta 3**: Si presupuesto < $1,000 → Enviar a equipo Básico
6. **Ruta 4**: Si no hay presupuesto → Enviar a equipo de Seguimiento

```mermaid
graph LR
    A[Webhook] --> B[Router]
    B -->|Presupuesto > $10k| C[Equipo Premium]
    B -->|Presupuesto $1k-$10k| D[Equipo Estándar]
    B -->|Presupuesto < $1k| E[Equipo Básico]
    B -->|Sin presupuesto| F[Seguimiento]
    
    C --> G[Notificación Slack]
    D --> H[Email Bienvenida]
    E --> I[Agregar a Lista]
    F --> J[Lead Nurturing]
```

#### 4.2.5 Filtros: Condiciones Avanzadas

Los filtros te permiten establecer condiciones que deben cumplirse para que los datos avancen en el flujo.

**Operadores Disponibles:**

| Operador | Descripción | Ejemplo |
|----------|-------------|---------|
| **Equal** | Exactamente igual | email = "test@test.com" |
| **Not Equal** | Diferente | status ≠ "archived" |
| **Contains** | Contiene texto | name contains "Smith" |
| **Not Contains** | No contiene | email not contains "spam" |
| **Starts With** | Comienza con | phone starts with "+1" |
| **Ends With** | Termina con | url ends with ".pdf" |
| **Matches Regex** | Coincide con regex | email matches regex |
| **Is Empty** | Está vacío | notes is empty |
| **Is Not Empty** | No está vacío | notes is not empty |
| **Greater Than** | Mayor que | amount > 1000 |
| **Less Than** | Menor que | priority < 3 |
| **In Array** | Está en array | status in array |
| **Not In Array** | No está en array | role not in array |

**Filtros Avanzados con AND/OR:**

Puedes combinar múltiples condiciones:

```
AND (todas las condiciones deben cumplirse):
  - amount > 1000
  - status = "approved"
  - region = "LATAM"

OR (al menos una debe cumplirse):
  - priority = "high"
  - priority = "urgent"
  - assigned_to = current_user
```

#### 4.2.6 Manejo de Errores

Make proporciona mecanismos robustos para manejar errores:

**1. Configuración de Errores en Módulos:**

Cada módulo tiene una sección "Error Handling" con opciones:
- **Don't include error handling**: No hace nada especial
- **Throw error bubble up**: Lanza el error hacia arriba
- **Ignore**: Ignora el error y continúa
- **Keep module's result**: Mantiene el resultado aunque haya error
- **Custom error handling**: Define qué hacer tú mismo

**2. Directives de Error:**

- **throwError**: Generar un error personalizado
- **sleep**: Pausar antes de reintentar
- **reset**: Reiniciar el flujo

**3. Routers de Error:**

Puedes redirigir errores a rutas específicas:

```
[Module] --> [Error Handler Router]
                  --> [Ruta 1: Notificar al equipo]
                  --> [Ruta 2: Reintentar automáticamente]
                  --> [Ruta 3: Registrar en log y continuar]
```

```mermaid
flowchart TD
    A[Module] --> B{Success?}
    B -->|Yes| C[Continue Flow]
    B -->|No| D[Error Handler]
    
    D --> E{Retry Count < 3?}
    E -->|Yes| F[Wait 5 min]
    E -->|No| G[Notify Team]
    F --> A
    
    G --> H[Log Error]
    H --> I[Alternative Action]
    
    style A fill:#69db7c
    style B fill:#ffd93d
    style D fill:#ff6b6b
    style G fill:#ff6b6b
    style I fill:#74c0fc
```

---

### MÓDULO 3: INTEGRACIÓN CON APIS (60 minutos)

#### 4.2.7 HTTP Module: Conectando con Cualquier API

El módulo HTTP te permite conectarte a cualquier API pública o privada que use protocolo HTTP. Esto abre un mundo de posibilidades más allá de los conectores predefinidos.

**Casos de Uso del Módulo HTTP:**

- Conectar con APIs internas de la empresa
- Usar APIs de servicios sin conector nativo
- Integrar con sistemas legacy
- Conectar con APIs gubernamentales

**Configuración del Módulo HTTP:**

```
URL: https://api.ejemplo.com/v1/recurso
Method: GET / POST / PUT / DELETE / PATCH
Headers:
  - Authorization: Bearer {{token}}
  - Content-Type: application/json
Body:
  - {"campo1": "valor1", "campo2": "valor2"}
Query String:
  - param1: valor1
  - param2: valor2
```

**Ejemplo: Conectar con API de Clima:**

1. **Módulo HTTP**:
   - URL: `https://api.openweathermap.org/data/2.5/weather`
   - Method: GET
   - Query String: `lat={{lat}}&lon={{lon}}&appid={{apiKey}}&units=metric`

2. **Output**:
   - Temperatura actual
   - Humedad
   - Descripción del clima

3. **Siguiente paso**:
   - Enviar notificación con el clima

#### 4.2.8 Autenticación en APIs

Las APIs pueden requerir diferentes tipos de autenticación:

**1. API Key (Basic)**

```
Headers:
  X-API-Key: tu_api_key_aqui
```

**2. Bearer Token (OAuth)**

```
Headers:
  Authorization: Bearer tu_bearer_token_aqui
```

**3. Basic Auth**

```
Headers:
  Authorization: Basic {{base64(username:password)}}
```

**4. OAuth 2.0**

Make tiene integraciones preconfiguradas para OAuth. Solo necesitas:
- Client ID
- Client Secret
- Authorization URL
- Token URL

**5. Custom Headers**

Algunas APIs usanHeaders personalizadas:
```
Headers:
  X-Auth-Token: tu_token
  X-Company-ID: tu_compania
```

#### 4.2.9 Webhooks: Integración en Tiempo Real

Los webhooks son fundamentales para automatizaciones en tiempo real. Son notificaciones automáticas que una aplicación envía a otra cuando ocurre un evento.

**Tipos de Webhooks en Make:**

**1. Webhook como Trigger (Receiving):**
- Make genera una URL única
- Cuando esa URL recibe una petición, se activa el escenario

**2. Webhook como Action (Sending):**
- El escenario envía datos a una URL externa
- Útil para notify otros sistemas

**Configuración de Webhook Receiver:**

```
1. Agregar módulo "Webhook" → "Custom Webhook"
2. Make genera URL: https://hook.make.com/abc123
3. Configurar en la otra aplicación (ej: Shopify,Typeform)
4. Probar conexión
```

**Ejemplo: Webhook de Stripe:**

1. **Trigger**: Webhook de Stripe → "Payment Succeeded"
2. **Procesar datos**: Extraer información del cliente y transacción
3. **Actualizar CRM**: Agregar/actualizar cliente en HubSpot
4. **Enviar email**: Confirmación de pago al cliente
5. **Notificar en Slack**: Alertas de ventas exitosas

```mermaid
sequenceDiagram
    participant Customer
    participant Stripe
    participant Make
    participant CRM
    participant Email
    participant Slack
    
    Customer->>Stripe: Realiza pago
    Stripe->>Make: Webhook: Payment Succeeded
    Make->>CRM: Actualizar cliente
    Make->>Email: Enviar confirmación
    Make->>Slack: Notificar equipo
    
    Note over Stripe,Slack: Todo esto ocurre en segundos
```

---

### MÓDULO 4: PATRONES DE DISEÑO AVANZADOS (45 minutos)

#### 4.2.10 Patrón: Manejo de Colecciones

Cuando trabajas con arrays o colecciones de datos, necesitas procesarlos eficientemente:

**1. Iterator: Procesar Elemento por Elemento**

```
[Get Records] --> [Iterator] --> [Process Each] --> [Output]
```

El iterator convierte cada elemento de un array en una ejecución separada del flujo.

**2. Array Aggregator: Recopilar Resultados**

```
[Process 1] --> [Array Aggregator]
[Process 2] --> [Array Aggregator]
[Process 3] --> [Array Aggregator]

Array Aggregator --> [Final Output]
```

**3. Combinar Iterator + Aggregator:**

Este es un patrón muy común:
1. Obtienes una lista de elementos (array)
2. Procesas cada uno con Iterator
3. Recopilas resultados con Array Aggregator

```mermaid
graph TD
    A[Get Orders Array] --> B[Iterator]
    B --> C[For Each Order]
    C --> D[Get Customer Details]
    D --> E[Get Product Details]
    E --> F[Calculate Total]
    F --> G[Array Aggregator]
    G --> H[Generate Report]
    
    style A fill:#ffd93d
    style B fill:#74c0fc
    style G fill:#69db7c
    style H fill:#cc5de8
```

#### 4.2.11 Patrón: Reintentos con Backoff

Cuando una API falla temporalmente, quieres reintentar automáticamente:

**Lógica de Backoff Exponential:**
- Primer intento: Inmediato
- Segundo intento: 1 minuto después
- Tercer intento: 5 minutos después
- Cuarto intento: 30 minutos después

**Implementación en Make:**

```
1. Module with Error Handler → "Throw error bubble up"
2. Router after module
3. Filter: {{if(contains(error.message, "429"); true; false)}}
4. Sleep: 60 seconds
5. Jump back to original module
```

#### 4.2.12 Patrón: Rate Limiting

Muchas APIs tienen límites de cuántas peticiones puedes hacer por segundo o minuto. Maneja esto correctamente:

**Estrategia 1: Sleep entre llamadas**

```
[Module 1] --> [Sleep: 200ms] --> [Module 2] --> [Sleep: 200ms] --> [Module 3]
```

**Estrategia 2: Procesamiento por lotes**

```
1. Get all items
2. Use Iterator with Batch (ej: 10 items)
3. Process batch
4. Sleep between batches
```

---

### MÓDULO 5: OPTIMIZACIÓN Y MEJORES PRÁCTICAS (15 minutos)

#### 4.2.13 Optimización de Operaciones

Cada módulo ejecuta una "operación". Reducir operaciones te ahorra dinero:

**Tips de Optimización:**

1. **Combina Transformaciones**: Usa el módulo "Map" en lugar de múltiples módulos de texto

2. **Limita Datos**: Configura filtros temprano para no procesar datos innecesarios

3. **Desactiva Escenarios que No Usas**: Los escenarios activados consumen operaciones aunque no procesen nada

4. **Usa Webhooks en lugar de Polling**: Los webhooks son más eficientes que revisar periódicamente

5. **Agrupa Operaciones en Batch**: En lugar de procesar 100 elementos uno por uno, agrúpalos

#### 4.2.14 Estructura de Escenarios

**Organización Recomendada:**

```
Carpeta: CLIENTES
├── Escenario: 01-Nuevo-Cliente-Welcome
├── Escenario: 02-Actualizar-CRM
├── Escenario: 03-Notificaciones-Slack
└── Escenario: 04-Seguimiento-Post-Venta
```

**命名ación Consistente:**
- Usa prefijos numéricos para orden
- Nombres descriptivos
- Incluir trigger en nombre

---

## 4.3 DIAGRAMAS EN MERMAID

### Diagrama 1: Arquitectura de un Escenario Complejo

```mermaid
flowchart TB
    subgraph TRIGGER[Trigger]
        A[Webhook] --> B[Parse JSON]
    end
    
    subgraph PROCESS[Procesamiento]
        B --> C[Router: Type Check]
        C -->|Type A| D[Filter: Validar]
        D --> E[HTTP: API Call]
        E --> F[Parse Response]
        C -->|Type B| G[Iterator]
        G --> H[Loop Item]
        H --> I[Transform Data]
    end
    
    subgraph OUTPUT[Salida]
        F --> J[Aggregator]
        I --> J
        J --> K[HTTP: Webhook to Next System]
        K --> L[Slack Notification]
    end
    
    subgraph ERROR[Error Handling]
        E -.-> M[Error Handler]
        I -.-> M
        M --> N[Log Error]
        N --> O[Alert Team]
    end
    
    style TRIGGER fill:#e7c6ff
    style PROCESS fill:#c1ffc1
    style OUTPUT fill:#bde0fe
    style ERROR fill:#ffd6ff
```

### Diagrama 2: Flujo de Autenticación OAuth

```mermaid
sequenceDiagram
    participant User
    participant App
    participant Make
    participant API
    
    User->>App: Clic "Conectar"
    App->>Make: Redirect con Client ID
    Make->>User: Mostrar OAuth Screen
    User->>Make: Autorizar acceso
    Make->>API: Request Token
    API->>Make: Return Access Token
    Make->>App: Redirect con Success
    Note over Make: Guardar Token
    
    App->>Make: Request con datos
    Make->>API: API Call con Bearer Token
    API->>Make: Response datos
    Make->>App: Return datos
    
    Note over User: Conexión establecida
```

### Diagrama 3: Patrón de Manejo de Errores

```mermaid
flowchart TD
    A[Start] --> B[Execute Module]
    B --> C{Success?}
    
    C -->|Yes| D[Continue]
    C -->|No| E{Retry Count < 3?}
    
    E -->|Yes| F[Wait Exponential Backoff]
    F --> B
    
    E -->|No| G[Error Router]
    
    G --> H{Rate Limit?}
    H -->|Yes| I[Wait 60 sec]
    I --> B
    
    H -->|No| J{Auth Error?}
    J -->|Yes| K[Refresh Token]
    K --> L[Retry Once]
    L --> B
    
    J -->|No| M[Log Error]
    M --> N[Notify Channel]
    N --> O[Fallback Action]
    
    style C fill:#69db7c
    style E fill:#ffd93d
    style G fill:#ff6b6b
    style N fill:#ff6b6b
```

---

## 4.4 REFERENCIAS EXTERNAS

1. **Documentación Oficial de Make**
   - URL: https://www.make.com/en/help/introduction
   - Relevancia: Guía completa de todas las funcionalidades

2. **Make Academy**
   - URL: https://www.make.com/academy
   - Relevancia: Cursos gratuitos en video

3. **Make Community**
   - URL: https://community.make.com
   - Relevancia: Foros de soporte y ejemplos

4. **Make Blog - Best Practices**
   - URL: https://www.make.com/blog
   - Relevancia: Tips y casos de uso

5. **API OpenWeatherMap Documentación**
   - URL: https://openweathermap.org/api
   - Relevancia: Ejemplo de API para prácticas

6. **Stripe API Documentation**
   - URL: https://stripe.com/docs/development
   - Relevancia: API de pagos para ejemplos

---

## 4.5 EJERCICIOS PRÁCTICOS RESUELTOS Y EXPLICADOS

### Ejercicio 1: Crear Escenario de Notificaciones de Leads

**ESCENARIO:** Tienes un formulario en Typeform que captura leads. Cuando alguien completa el formulario, quieres:
1. Guardar los datos en Google Sheets
2. Clasificar el lead según presupuesto
3. Notificar al equipo correcto en Slack

**PASO 1: Configurar el Trigger**

1. Ve a Make y crea nuevo escenario
2. Busca "Typeform" en módulos
3. Selecciona "Watch Form Responses"
4. Conecta tu cuenta de Typeform
5. Selecciona el formulario de leads
6. Configura el Trigger: "Instant"

**PASO 2: Configurar Google Sheets**

1. Agrega módulo: Google Sheets "Add Row"
2. Conecta tu cuenta de Google
3. Configura:
   - Spreadsheet: "Leads Database"
   - Sheet: "Responses"
   - Row: Items del formulario (name, email, phone, budget)

**PASO 3: Configurar Clasificación con Router**

1. Agrega módulo "Router" después de Sheets
2. Crea 3 rutas con filtros:

**Ruta 1 - Premium:**
```
Filter:
{{9. ¿Cuál es tu presupuesto?}} > 10000
```

**Ruta 2 - Estándar:**
```
Filter:
{{9. ¿Cuál es tu presupuesto?}} > 1000
AND
{{9. ¿Cuál es tu presupuesto?}} <= 10000
```

**Ruta 3 - Básico:**
```
Filter:
{{9. ¿Cuál es tu presupuesto?}} <= 1000
```

**PASO 4: Notificaciones en Slack**

1. En cada ruta, agrega módulo Slack "Send Message"
2. Configura el mensaje apropiado para cada nivel:
   - Premium: Notifica a @equipo-premium
   - Estándar: Notifica a @equipo-estandar
   - Básico: Notifica a @equipo-basico

**PASO 5: Guardar y Activar**

1. Pon nombre al escenario: "Lead Routing - Typeform to Slack"
2. Guarda el escenario
3. Activa el escenario (toggle azul)

---

### Ejercicio 2: Sincronización de Inventario

**ESCENARIO:** Tienes productos en Shopify y también en WooCommerce. Necesitas que el inventario se sincronice automáticamente cuando hay una venta en cualquiera de las plataformas.

**Arquitectura de la Solución:**

```mermaid
flowchart LR
    subgraph SHOPIFY[Shopify]
        A[Nueva Orden]
    end
    
    subgraph MAKE[Make Scenario]
        B[Webhook: Shopify]
        C[HTTP: Get Stock WooCommerce]
        D[Calculate: New Stock]
        E[HTTP: Update WooCommerce]
    end
    
    subgraph WOOCOMMERCE[WooCommerce]
        F[Inventario Actualizado]
    end
    
    A --> B
    B --> C
    C --> D
    D --> E
    E --> F
```

**PASO 1: Webhook de Shopify**

1. Crea webhook en Shopify: Order Created
2. URL del webhook: Genera en Make
3. Configura el trigger en Make

**PASO 2: Extraer Productos de la Orden**

1. Usa el módulo "Iterator" para procesar cada línea de la orden
2. Extrae: SKU del producto, cantidad comprada

**PASO 3: Consultar WooCommerce**

1. Usa módulo HTTP para consultar API de WooCommerce
2. Endpoint: `GET /wp-json/wc/v3/products`
3. Filtro: `?sku={sku}`
4. Respuesta: Stock actual en WooCommerce

**PASO 4: Calcular Nuevo Stock**

```
Nuevo Stock = Stock Actual (WooCommerce) - Cantidad Vendida (Shopify)
```

**PASO 5: Actualizar WooCommerce**

1. Usa módulo HTTP
2. Endpoint: `POST /wp-json/wc/v3/products/{id}`
3. Body: `{ "manage_stock": true, "stock_quantity": {{nuevo_stock}} }`

---

### Ejercicio 3: Pipeline de Procesamiento de Emails

**ESCENARIO:** Procesar emails entrantes y clasificarlos, responder automáticamente según el tipo.

**PASO 1: Configurar Gmail Trigger**

1. Módulo Gmail "Watch Emails"
2. Filtro: `subject:("Soporte" OR "Ventas" OR "General")`
3. Label: "To Process"

**PASO 2: Parser de Contenido**

1. Extraer: Remitente, asunto, cuerpo
2. Usar "Text Parser" para limpiar HTML
3. Usar "AI" (OpenAI) para clasificar el email

**PASO 3: Clasificación con AI**

1. Módulo HTTP hacia OpenAI API
2. Prompt: "Clasifica este email en una categoría: Soporte, Ventas, General, Urgente"
3. Input: El cuerpo del email

**PASO 4: Router con Filtros**

- Ruta Urgente: Notificación inmediata + atender primero
- Ruta Soporte: Agregar a cola de tickets
- Ruta Ventas: Agregar a CRM + asignar a vendedor
- Ruta General: Archivar + responder automáticamente

**PASO 5: Respuesta Automática**

1. Módulo Gmail "Send Email"
2. Template de respuesta según clasificación
3. Firma personalizada

---

## 4.6 TECNOLOGÍAS ESPECÍFICAS

### Herramientas Cubiertas en Esta Clase

| Herramienta | Función | Costo | Link |
|-------------|---------|-------|------|
| **Make (Integromat)** | Automatización visual | Gratis-$299+ | make.com |
| **Google Sheets** | Base de datos | Gratis | sheets.google.com |
| **Slack** | Notificaciones | Gratis | slack.com |
| **Gmail** | Email | Gratis | gmail.com |
| **HTTP Module** | Conexión API | Incluido | make.com |
| **Webhooks** | Triggers tiempo real | Incluido | make.com |

---

## 4.7 ACTIVIDADES DE LABORATORIO

### Laboratorio 1: Tu Primer Escenario Completo

**Objetivo:** Crear un escenario que integre al menos 3 aplicaciones.

**Instrucciones:**

1. **Elige 3 aplicaciones** que uses en tu negocio (ej: Typeform + Sheets + Slack)

2. **Diseña el flujo:**
   - ¿Qué activa el escenario?
   - ¿Qué datos procesa?
   - ¿Qué acción finalize?

3. **Construye en Make:**
   - Configura el trigger
   - Agrega módulos de procesamiento
   - Configura acciones finales

4. **Prueba el escenario:**
   - Activa el escenario
   - Ejecuta el trigger manualmente
   - Verifica que todo funcione

**Entregable:** screenshot del escenario funcionando + descripción del flujo

---

### Laboratorio 2: Manejo de Errores

**Objetivo:** Implementar manejo de errores robusto.

**Instrucciones:**

1. **Toma el laboratorio 1** y agrega manejo de errores

2. **Agrega Routers de Error:**
   - ¿Qué debe pasar si el trigger falla?
   - ¿Qué debe pasar si una API no responde?

3. **Configura Notificaciones:**
   - Cuando haya un error, notifica en Slack
   - Incluye información de debug

4. **Prueba el Error Handler:**
   - Genera un error a propósito
   - Verifica que la notificación funcione

---

### Laboratorio 3: Optimización de Escenarios

**Objetivo:** Reducir operaciones y mejorar rendimiento.

**Instrucciones:**

1. **Analiza un escenario existente** (del Laboratorio 1 o 2)

2. **Identifica oportunidades de optimización:**
   - ¿Hay módulos que puedes combinar?
   - ¿Estás procesando datos innecesarios?
   - ¿Hay filtros que puedes agregar temprano?

3. **Implementa mejoras:**
   - Aplica los cambios
   - Mide la diferencia en operaciones

4. **Documenta:**
   - ¿Cuántas operaciones ahorraste?
   - ¿Mejora el rendimiento?

---

## 4.8 RESUMEN DE PUNTOS CLAVE

### Conceptos Fundamentales

1. **Make es una plataforma de automatización visual** que permite conectar aplicaciones sin código, ofreciendo mayor flexibilidad que alternativas como Zapier.

2. **Los escenarios se construyen con módulos** que se conectan visualmente. Cada módulo representa una acción o trigger específico.

3. **El Router es fundamental** para flujos complejos, permitiendo enviar datos por diferentes caminos según condiciones.

4. **Los filtros permiten establecer condiciones** que deben cumplirse para que los datos avancen en el flujo.

5. **El manejo de errores es crítico** para automatizaciones robustas. Make ofrece múltiples opciones para manejar fallos.

6. **El módulo HTTP abre infinitas posibilidades** al permitir conectar con cualquier API que use HTTP.

7. **Los Webhooks permiten integraciones en tiempo real** sin necesidad de polling o verificaciones periódicas.

### Herramientas Aprendidas

- Make (Integromat): Interfaz, escenarios, módulos
- Google Sheets: Integración básica
- Slack: Notificaciones
- Gmail: Procesamiento de emails
- Módulo HTTP: APIs externas

### Próximos Pasos

- [ ] Completar Laboratorios 1, 2 y 3
- [ ] Explorar la biblioteca de templates de Make
- [ ] Integrar al menos 3 aplicaciones de tu negocio
- [ ] Implementar manejo de errores en todos tus escenarios

---

**FIN DE LA CLASE 4**

*En la Clase 5, aprenderemos a integrar capacidades de IA en tus flujos No-Code usando OpenAI, Stable Diffusion y más.*
