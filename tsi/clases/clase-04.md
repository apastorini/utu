# Clase 4: Modelado de Amenazas (Threat Modeling)

**Duracion:** 2 horas

---

## Objetivos de Aprendizaje

1. Comprender que es el modelado de amenazas y sus objetivos
2. Dominar la metodologia STRIDE para clasificar y analizar amenazas
3. Crear e interpretar Diagramas de Flujo de Datos (DFD)
4. Identificar amenazas en una aplicacion y proponer mitigaciones

---

## Contenido Detallado

### 1. Que es Threat Modeling?

El modelado de amenazas es un proceso estructurado para identificar, cuantificar y priorizar amenazas de seguridad en un sistema. No es una actividad unica, sino que se integra en el ciclo de desarrollo.

**Objetivos:**
- Identificar amenazas ANTES de que se materialicen
- Disenar controles de seguridad efectivos
- Priorizar esfuerzos de seguridad basados en riesgo
- Documentar el perfil de riesgo del sistema
- Cumplir con requisitos regulatorios

**Beneficios:**
- Reduce costos al encontrar problemas en diseno
- Mejora la comunicacion entre equipos (dev, ops, security)
- Proporciona documentacion de decisiones de seguridad
- Identifica suposiciones de seguridad incorrectas

```
Proceso de Threat Modeling
+------------------+    +------------------+    +------------------+
| 1. DEFINIR       |--->| 2. DESCOMPONER   |--->| 3. IDENTIFICAR   |
|    ALCANCE       |    |    LA APP        |    |    AMENAZAS      |
+------------------+    +------------------+    +------------------+
                                                         |
                                                         v
+------------------+    +------------------+    +------------------+
| 5. VALIDAR Y     |<---| 4. DOCUMENTAR    |<---|    MITIGACIONES  |
|    ACTUALIZAR    |    |    AMENAZAS      |    |                  |
+------------------+    +------------------+    +------------------+
```

### 2. Metodologia STRIDE

Desarrollada por Microsoft, STRIDE es un acronimo que clasifica amenazas en 6 categorias.

| Letra | Amenaza | Definicion | Ejemplo |
|-------|---------|-----------|---------|
| **S** | Spoofing | Suplantacion de identidad | Falsificar un token JWT |
| **T** | Tampering | Manipulacion de datos | Modificar una peticion HTTP en transito |
| **R** | Repudiation | Negacion de una accion | Un usuario niega haber realizado una transferencia |
| **I** | Information Disclosure | Exposicion de informacion | Leer la BD por inyeccion SQL |
| **D** | Denial of Service | Denegacion de servicio | Saturar un endpoint con peticiones |
| **E** | Elevation of Privilege | Escalada de privilegios | Usuario normal obtiene acceso admin |

#### Spoofing (Suplantacion)
- **Afecta a:** Autenticacion
- **Pregunta clave:** ?Como puede alguien hacerse pasar por otra entidad?
- **Mitigaciones:** Autenticacion fuerte (MFA), certificados, verificar origen

#### Tampering (Manipulacion)
- **Afecta a:** Integridad
- **Pregunta clave:** ?Como puede alguien modificar datos sin autorizacion?
- **Mitigaciones:** Firmas digitales, hashing, checksums, integridad de mensajes

#### Repudiation (No Repudio)
- **Afecta a:** No repudio (trazabilidad)
- **Pregunta clave:** ?Como puede alguien negar haber realizado una accion?
- **Mitigaciones:** Logs de auditoria, firmas digitales, registros inmutables

#### Information Disclosure (Divulgacion de Informacion)
- **Afecta a:** Confidencialidad
- **Pregunta clave:** ?Como puede alguien acceder a informacion que no deberia?
- **Mitigaciones:** Cifrado, control de acceso, minimizar datos expuestos

#### Denial of Service (Denegacion de Servicio)
- **Afecta a:** Disponibilidad
- **Pregunta clave:** ?Como puede alguien impedir que el sistema funcione?
- **Mitigaciones:** Rate limiting, balanceo de carga, auto-scaling, WAF

#### Elevation of Privilege (Escalada de Privilegios)
- **Afecta a:** Autorizacion
- **Pregunta clave:** ?Como puede un usuario obtener permisos que no le corresponden?
- **Mitigaciones:** Validacion de autorizacion en cada endpoint, RBAC, minimo privilegio

### 3. Diagramas de Flujo de Datos (DFD)

Un DFD representa graficamente como fluyen los datos a traves del sistema.

**Elementos de un DFD:**

```
SIMBOLOS DE DFD (Notacion De Marco)
+----------+     Datos en transito
| Proceso  |<---~~~~~~~~~~~~~~~---> Datos en reposo
+----------+
     ^
     |      --->  Flujo de datos
     v
+----------+    +--------+
| Entidad  |    |Almacen |
| Externa  |    |Datos   |
| (usuario)|    |(BD)    |
+----------+    +--------+

+.. .. .. ..+
. Limite de .
. Confianza .
+.. .. .. ..+
```

**Reglas del DFD:**
- Cada elemento tiene un nombre unico
- Los flujos de datos tienen direccion (flechas)
- Los procesos transforman datos de entrada en salida
- Las entidades externas estan fuera del sistema
- Los almacenes de datos guardan datos persistidos

### 4. Proceso Completo

#### Paso 1: Definir Alcance
- Que sistema estamos analizando?
- Cuales son los limites del sistema?
- Que asunciones hacemos?
- Cual es el peor caso que debemos considerar?

#### Paso 2: Descomponer la Aplicacion
- Crear DFD de la aplicacion
- Identificar todas las entradas de datos
- Identificar almacenes de datos
- Marcar limites de confianza

#### Paso 3: Identificar Amenazas
- Aplicar STRIDE a cada elemento del DFD
- Usar herramientas como Microsoft Threat Modeling Tool
- Preguntar: "Que puede pasar aqui?"

#### Paso 4: Documentar Amenazas
- Para cada amenaza: descripcion, categoria STRIDE, impacto, probabilidad
- Priorizar por riesgo (Alto/Medio/Bajo)

#### Paso 5: Mitigar
- Proponer controles para cada amenaza
- Decidir: mitigar, transferir, aceptar, evitar

### 5. Herramientas

| Herramienta | Tipo | Caracteristicas |
|------------|------|----------------|
| **Microsoft Threat Modeling Tool** | Gratuita, Windows | DFD automatico, plantillas STRIDE, genera reportes |
| **OWASP Threat Dragon** | Open source, web/desktop | Multiplataforma, DFD, almacena en JSON |
| **OWASP Cornucopia** | Web, juego | Basado en cartas para brainstorming |
| **STRIDE-per-element** | Metodologia | Aplicar STRIDE a cada elemento del DFD |
| **Threatspec** | Open source | Threat modeling como codigo (archivos de configuracion) |

---

## Ejercicio: Modelado de Amenazas de una App de Login

**Escenario:** Tienes una aplicacion web simple de login. El usuario ingresa usuario y contrasena, el frontend (React) envia los datos por HTTPS al backend (Flask), que consulta una BD de usuarios y devuelve un token JWT si las credenciales son correctas. Este token se usa para acceder a rutas protegidas.

### 1. Crear el DFD

```
+--------------+                    +--------------+                    +----------+
|  Usuario     |<--- HTTPS/TLS --->|  Frontend    |<--- HTTPS/TLS --->|  Backend  |
|  (Navegador) |                   |  React SPA   |                    |  Flask    |
+--------------+                   +--------------+                    +----------+
                                                                             |
                                                                             v
                                                                       +----------+
                                                                       |    BD    |
                                                                       | Postgres |
                                                                       +----------+
+.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..+
.                          LIMITE DE CONFIANZA                                    .
.  Todo lo que esta dentro de este cuadro es controlado por la organizacion       .
+.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..+
```

### 2. Aplicar STRIDE a cada elemento

Analizaremos cada elemento del DFD y aplicaremos las 6 categorias STRIDE.

| Elemento | S | T | R | I | D | E |
|----------|---|---|---|---|---|---|
| Usuario | X |   | X |   |   |   |
| Frontend (React) | X | X |   | X |   | X |
| Conexion Front-Back |   | X |   | X |   |   |
| Backend (Flask) | X | X | X | X | X | X |
| BD Postgres |   | X | X | X | X | X |

### 3. Amenazas Identificadas y Mitigaciones

#### Amenaza S1 - Spoofing contra el Frontend
**Descripcion:** Un atacante crea un sitio web identico al legitimo (phishing) para robar credenciales.
**Categoria:** Spoofing
**Mitigacion:** Usar certificados TLS validos, HSTS, educar usuarios, verificar origen con CORS.

#### Amenaza T1 - Tampering en la comunicacion Front-Back
**Descripcion:** Un atacante intercepta y modifica la peticion login (MITM).
**Categoria:** Tampering
**Mitigacion:** HTTPS obligatorio con TLS 1.2+, certificate pinning, HSTS.

#### Amenaza R1 - Repudiation de login
**Descripcion:** Un usuario niega haber iniciado sesion o realizado una accion.
**Categoria:** Repudiation
**Mitigacion:** Logs de auditoria inmutables con timestamp, IP, User-Agent. Almacenar hash de la sesion.

#### Amenaza I1 - Information Disclosure en BD
**Descripcion:** Atacante obtiene acceso a la BD y lee contrasenas, emails, tokens.
**Categoria:** Information Disclosure
**Mitigacion:** Cifrado en reposo, contrasenas con bcrypt, minimizar datos almacenados, cifrado de columnas sensibles.

#### Amenaza D1 - DoS contra el endpoint de login
**Descripcion:** Atacante satura el endpoint /login con peticiones masivas.
**Categoria:** Denial of Service
**Mitigacion:** Rate limiting (limitar request por IP/minuto), CAPTCHA despues de N intentos, WAF, auto-scaling.

#### Amenaza E1 - Elevation of Privilege via JWT
**Descripcion:** Usuario modifica el token JWT para escalar privilegios (cambiar role de "user" a "admin").
**Categoria:** Elevation of Privilege
**Mitigacion:** Firmar JWT con clave secreta fuerte (HS256) o RSA (RS256), verificar firma en cada request, incluir claims de autorizacion en el token.

#### Amenaza S2 - Spoofing en Backend
**Descripcion:** Un atacante hace spoofing del backend para interceptar credenciales.
**Categoria:** Spoofing
**Mitigacion:** Certificados TLS del lado del servidor, validacion de certificado por parte del frontend.

#### Amenaza T2 - Tampering en BD
**Descripcion:** Atacante modifica registros de usuarios directamente en BD.
**Categoria:** Tampering
**Mitigacion:** Control de acceso a BD, minimo privilegio para la conexion de la app, trigger de auditoria, backups regulares.

#### Amenaza I2 - Information Disclosure en Respuestas
**Descripcion:** El backend devuelve demasiada informacion en la respuesta (ej: "Usuario no existe" vs "Contrasena incorrecta").
**Categoria:** Information Disclosure
**Mitigacion:** Mensajes de error genericos ("Credenciales invalidas"), no revelar que campo es incorrecto.

#### Amenaza D2 - DoS contra BD
**Descripcion:** Consultas lentas o mal disenadas saturan la BD.
**Categoria:** Denial of Service
**Mitigacion:** Indices en tablas, query optimization, connection pooling, timeout en consultas, limites de resultados.

### 4. Priorizacion de Riesgos

| Amenaza | Impacto | Probabilidad | Riesgo |
|---------|---------|-------------|--------|
| I1 - Disclosure de BD | Alto | Media | **Critico** |
| E1 - Escalada via JWT | Alto | Alta | **Critico** |
| T2 - Tampering en BD | Alto | Baja | **Alto** |
| S1 - Spoofing Frontend | Alto | Alta | **Critico** |
| D1 - DoS login | Medio | Alta | **Alto** |
| I2 - Info disclosure msgs | Bajo | Alta | **Medio** |
| R1 - Repudiation | Medio | Media | **Medio** |
| D2 - DoS BD | Alto | Baja | **Medio** |

### 5. Plan de Accion Priorizado

1. **Semana 1:** Implementar bcrypt para contrasenas, firmar JWT con RS256, verificar firma en cada request
2. **Semana 2:** Configurar HTTPS/HSTS, certificados validos, rate limiting en login
3. **Semana 3:** Implementar logs de auditoria inmutables, mensajes de error genericos
4. **Semana 4:** Hardening de BD, minimo privilegio, cifrado en reposo, backups

---

## Preguntas y Respuestas

### Pregunta 1
**Cual es la diferencia entre una amenaza y un riesgo en threat modeling?**

**Respuesta:** Una amenaza es un evento potencial que puede causar dano (ej: "un atacante puede inyectar SQL"). El riesgo es la combinacion de la probabilidad de que ocurra la amenaza y el impacto que tendria. En threat modeling primero identificamos amenazas (cualitativamente, con STRIDE) y luego evaluamos el riesgo (cuantitativa o cualitativamente) para priorizar mitigaciones. Una amenaza con baja probabilidad y bajo impacto puede aceptarse; una con alta probabilidad y alto impacto debe mitigarse.

### Pregunta 2
**Que es un limite de confianza en un DFD y por que es importante?**

**Respuesta:** Un limite de confianza (trust boundary) es una linea imaginaria que separa areas con diferentes niveles de confianza o control. Por ejemplo, el limite entre Internet y la red interna, o entre el frontend y el backend. Es importante porque los flujos de datos que cruzan un limite de confianza son puntos donde se deben aplicar controles de seguridad (cifrado, autenticacion, validacion). Cada vez que un dato cruza un limite, hay una oportunidad para un ataque.

### Pregunta 3
**En STRIDE, las amenazas Repudiation son las menos consideradas. Por que son importantes?**

**Respuesta:** Las amenazas de repudiation son importantes porque sin la capacidad de probar que una accion ocurrio, no se pueden: (1) investigar incidentes de seguridad (no hay evidencia), (2) cumplir con requisitos legales y regulatorios (SOX, GDPR requieren trazabilidad), (3) responsabilizar a usuarios maliciosos internos, (4) defender a usuarios legitimos cuyas cuentas fueron comprometidas. En un sistema financiero, la falta de no repudio permitiria a un atacante transferir dinero y negar haberlo hecho.

### Pregunta 4
**Como se relaciona el threat modeling con el SSDLC?**

**Respuesta:** El threat modeling es una actividad clave de la fase de **Diseno Seguro** del SSDLC. Sin embargo, no debe realizarse una sola vez: debe actualizarse cuando cambia la arquitectura, se anaden nuevas funcionalidades o se descubren nuevas amenazas. Idealmente, el threat modeling se realiza: (1) inicialmente en la fase de diseno, (2) cada vez que se anade una funcionalidad importante, (3) cuando se descubre una nueva clase de vulnerabilidad (ej: Log4j), y (4) anual como revision general.

### Pregunta 5
**Que herramienta de threat modeling recomienda para un equipo pequeno con presupuesto limitado?**

**Respuesta:** Para un equipo pequeno sin presupuesto, recomiendo **OWASP Threat Dragon** porque: es gratuita y open source, funciona en Windows/Linux/Mac, soporta DFD graficos, exporta a JSON, y permite colaboracion. Alternativamente, se puede usar una aproximacion "lightweight": una planilla de calculo con columnas para cada categoria STRIDE, los elementos del sistema, y las mitigaciones. La herramienta no es tan importante como el proceso y las preguntas correctas.

---

## Tarea / Lectura Recomendada

1. **Leer:** OWASP Threat Modeling Cheat Sheet - https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html
2. **Descargar:** Microsoft Threat Modeling Tool (gratuita) y practicar con ejemplos
3. **Leer:** "Threat Modeling: Designing for Security" de Adam Shostack (capitulos 1-4)
4. **Practicar:** Crear un DFD y aplicar STRIDE para una aplicacion de chat simple
5. **Profundizar:** Leer el whitepaper de STRIDE de Microsoft - "The STRIDE Threat Model"
