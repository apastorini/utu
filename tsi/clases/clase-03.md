# Clase 3: Ciclo de Vida del Desarrollo Seguro (SSDLC)

**Duracion:** 2 horas

---

## Objetivos de Aprendizaje

1. Comprender las diferencias entre modelos de desarrollo tradicionales y el SSDLC
2. Conocer las fases del SSDLC y los controles de seguridad aplicables en cada una
3. Familiarizarse con los marcos de trabajo: Microsoft SDL, NIST SSDF, OWASP SAMM
4. Aplicar el SSDLC a un caso de estudio real

---

## Contenido Detallado

### 1. Modelos Tradicionales vs. Seguros

#### Waterfall (Cascada)
- Fases secuenciales: Requisitos -> Diseno -> Implementacion -> Pruebas -> Despliegue -> Mantenimiento
- La seguridad solo se prueba al final
- Corregir vulnerabilidades tarde es muy costoso

#### Agile
- Ciclos iterativos cortos (sprints)
- La seguridad suele relegarse por presion de entregar rapido
- Sin practicas especificas de seguridad, se acumula "deuda de seguridad"

#### SSDLC (Secure Software Development Life Cycle)
- Integra seguridad en CADA fase del ciclo de vida
- No es un modelo nuevo, es una adaptacion de cualquier modelo existente
- Reduce costos y riesgos al encontrar vulnerabilidades temprano

```
Comparativa de Costos de Correccion
+--------------------------------------------------+
| Fase         | Costo Relativo de Correccion       |
|--------------+------------------------------------|
| Requisitos   | 1x                                |
| Diseno       | 6x                                |
| Codificacion | 15x                               |
| Pruebas      | 30x                               |
| Produccion   | 100x                              |
+--------------------------------------------------+
(Fuente: NIST, IBM System Sciences Institute)
```

### 2. Fases del SSDLC

```
+--------+    +--------+    +--------+    +--------+    +--------+    +--------+
|REQUISI- |--->| DISENO |--->| CODIFI- |--->|PRUEBAS |--->|DESPLIE-|--->| MANTE-  |
|TOS DE   |    | SEGURO |    | CACION  |    | DE     |    | GUE    |    | NIMIENTO|
|SEGURIDAD|    |        |    | SEGURA  |    |SEGURIDAD|   | SEGURO |    |         |
+--------+    +--------+    +--------+    +--------+    +--------+    +--------+
    |             |             |             |             |             |
    v             v             v             v             v             v
*Analisis    *Threat    *Estandares *SAST      *Config.    *Monitoreo
de riesgos   Modeling   de codigo   DAST        segura      continuo
*Regulacio-  *Principios*Peer review*Pruebas de *Hardening  *Gestion de
nes (GDPR,   de diseno  *Analisis   penetracion *Seguridad  parches
PCI DSS)     seguro     de depend.  *Fuzzing     en el CI/CD *Respuesta a
*Req. de     *Minimo    *Validacion *SCA         *Secret     incidentes
negocio      privilegio  de entradas             scanning
```

#### Fase 1: Requisitos de Seguridad
- Identificar requisitos regulatorios (GDPR, PCI DSS, HIPAA, SOX)
- Definir requisitos funcionales de seguridad (autenticacion, autorizacion, cifrado)
- Analisis de riesgos inicial
- Definir criterios de aceptacion de seguridad

#### Fase 2: Diseno Seguro
- Modelado de amenazas (Threat Modeling) - se ve en la Clase 4
- Principios de diseno seguro:
  - **Defense in depth:** multiples capas de seguridad
  - **Least privilege:** minimos privilegios necesarios
  - **Fail secure:** ante fallo, el sistema debe cerrar acceso, no abrirlo
  - **Separation of duties:** separar responsabilidades criticas
  - **Secure by default:** configuracion segura por defecto
- Revisar arquitectura y diagramas de flujo de datos

#### Fase 3: Codificacion Segura
- Usar estandares de codificacion segura (CERT, OWASP ASVS)
- Implementar validacion de entradas y salidas
- Codigo limpio, sin secretos hardcodeados
- Revision por pares (peer review) con checklist de seguridad
- Analisis estatico de codigo (SAST) integrado en IDE o CI

#### Fase 4: Pruebas de Seguridad
- SAST (Static Application Security Testing): SonarQube, Fortify, Checkmarx
- DAST (Dynamic Application Security Testing): OWASP ZAP, Burp Suite
- SCA (Software Composition Analysis): OWASP Dependency Check, Snyk
- Pruebas de penetracion manuales
- Fuzzing: envio de entradas aleatorias o malformadas

#### Fase 5: Despliegue Seguro
- Hardening del servidor: eliminar servicios innecesarios, configurar firewalls
- Gestor de secretos (HashiCorp Vault, AWS Secrets Manager)
- CI/CD con gates de seguridad: si falla SAST, no pasa a produccion
- Firmado de artefactos
- Container scanning (Docker image scanning)

#### Fase 6: Mantenimiento
- Monitoreo continuo de seguridad (SIEM, IDS/IPS)
- Gestion de parches y actualizaciones
- Plan de respuesta a incidentes
- Revision periodica de vulnerabilidades
- Retiro seguro de datos y sistemas

### 3. Marcos de Trabajo

#### Microsoft SDL (Security Development Lifecycle)
- Creado por Microsoft en 2004
- 13 fases que integran seguridad en todo el ciclo
- Incluye training obligatorio, threat modeling, herramientas de analisis
- Caso de exito: reduccion del 70% de vulnerabilidades en productos Microsoft

#### NIST SSDF (Secure Software Development Framework) - SP 800-218
- Marco del gobierno de EE.UU.
- 4 categorias principales:
  - **Prepare the Organization** (PO): definir roles, responsabilidades, estandares
  - **Protect the Software** (PS): proteger componentes, codigo, integridad
  - **Produce Well-Secured Software** (PW): requisitos, diseno, codificacion, pruebas seguras
  - **Respond to Vulnerabilities** (RV): recibir reportes, analizar, parchear

#### OWASP SAMM (Software Assurance Maturity Model)
- Modelo de madurez para medir y mejorar practicas de seguridad
- 5 funciones de negocio: Governance, Design, Implementation, Verification, Operations
- Cada funcion tiene 3 practicas de seguridad con niveles 0-3
- Permite crear una hoja de ruta personalizada

```
OWASP SAMM - Funciones y Practicas
+------------------+----------------------------+
| Funcion           | Practicas de Seguridad    |
+------------------+----------------------------+
| Governance        | Estrategia y Metricas,    |
|                   | Politicas y Cumplimiento, |
|                   | Educacion y Guia          |
+------------------+----------------------------+
| Design            | Evaluacion de Amenazas,   |
|                   | Requisitos de Seguridad,  |
|                   | Arquitectura Segura       |
+------------------+----------------------------+
| Implementation    | Gestion de Dependencias,  |
|                   | Provision Segura,         |
|                   | Errores y Manejo de       |
|                   | Excepciones               |
+------------------+----------------------------+
| Verification      | Evaluacion de            |
|                   | Vulnerabilidades,         |
|                   | Revisiones de Codigo,     |
|                   | Pruebas de Seguridad      |
+------------------+----------------------------+
| Operations        | Gestion de Incidentes,   |
|                   | Gestion de Ambiente,     |
|                   | Gestion Operacional      |
+------------------+----------------------------+
```

---

## Ejercicio 1: Aplicar SSDLC a una App de Compras Online

**Caso de Estudio:** Una startup quiere desarrollar una aplicacion web de compras online. Los usuarios pueden registrarse, buscar productos, anadirlos al carrito y pagar con tarjeta de credito. La aplicacion maneja datos personales (nombre, email, direccion) y datos de pago.

Para cada fase del SSDLC, determine:

1. **Requisitos de Seguridad:** Que requisitos de seguridad debe cumplir esta aplicacion?
2. **Diseno Seguro:** Que principios de diseno seguro debe aplicar?
3. **Codificacion Segura:** Que practicas debe seguir el equipo de desarrollo?
4. **Pruebas de Seguridad:** Que tipo de pruebas debe realizar?
5. **Despliegue Seguro:** Que medidas debe tomar al lanzar la aplicacion?
6. **Mantenimiento:** Que actividades continuas debe realizar?

### Solucion

#### Fase 1: Requisitos de Seguridad
- **PCI DSS:** Obligatorio si maneja tarjetas de credito
- **GDPR:** Si tiene clientes en Europa, debe cumplir con proteccion de datos
- **Autenticacion segura:** Login con MFA, politicas de contrasenas fuertes
- **Cifrado en transito:** TLS 1.2+ en todas las comunicaciones
- **Cifrado en reposo:** Datos de pago cifrados en BD
- **No almacenar CVV:** PCI DSS prohibe almacenar codigos de seguridad
- **Logging seguro:** Logs de auditoria sin datos sensibles
- **Limite de intentos de login:** Bloqueo tras N intentos fallidos

#### Fase 2: Diseno Seguro
- **Defense in depth:** WAF + firewall + validacion en app + BD segura
- **Least privilege:** Usuarios solo ven sus propios datos; roles separados (admin, cliente)
- **Seguridad en APIs:** Rate limiting, autenticacion por token, validacion de esquemas
- **Separacion de datos:** Datos de pago en BD separada o tokenizados via pasarela de pago
- **Diagrama de flujo de datos (DFD):** Identificar flujos de datos sensibles
- **Fallos seguros:** Si falla validacion de pago, no procesar orden parcial

#### Fase 3: Codificacion Segura
- **Validacion de entrada:** Sanitizar todos los inputs (busqueda, formularios, APIs)
- **Consultas parametrizadas:** Para prevenir inyeccion SQL
- **XSS prevention:** Escapar output, usar Content-Security-Policy, HttpOnly cookies
- **CSRF tokens:** Para formularios y acciones de estado
- **Hashing de contrasenas:** bcrypt/Argon2, nunca almacenar texto plano
- **Manejo de sesiones:** Tokens JWT seguros, tiempo de expiracion, refresh tokens
- **Logging sin datos sensibles:** No loguear contrasenas, tokens, CVV
- **Revision de dependencias:** Usar npm audit, pip-audit, OWASP Dependency Check

#### Fase 4: Pruebas de Seguridad
- **SAST (estatico):** SonarQube o ESLint security plugin en CI
- **DAST (dinamico):** OWASP ZAP contra entorno de staging
- **SCA (composicion):** Snyk o GitHub Dependabot para dependencias
- **Pruebas de penetracion:** Contratar ethical hacker antes del lanzamiento
- **Pruebas de autenticacion:** Probar bypass de login, fuerza bruta, session hijacking
- **Pruebas de pago:** Intentar manipular montos, estados de orden, reembolsos
- **Fuzzing:** Envio de datos malformados en APIs

#### Fase 5: Despliegue Seguro
- **HTTPS obligatorio:** Certificados TLS de Let's Encrypt, redirect HTTP->HTTPS
- **Headers de seguridad:** HSTS, X-Frame-Options, X-Content-Type-Options, CSP
- **Firewall:** Restringir puertos y orígenes IP
- **WAF:** ModSecurity o AWS WAF para proteccion adicional
- **Secretos en vault:** No hardcodear claves de API ni credenciales de BD
- **Minimo privilegio en servidor:** Usuarios no root, permisos minimos
- **Seguridad del contenedor:** Escaneo de imagenes Docker, no ejecutar como root
- **CI/CD con gates:** Si SAST o SCA encuentran criticos, no deployar

#### Fase 6: Mantenimiento
- **Monitoreo 24/7:** Alertas de intrusion, anomalias en trafico y patrones de pago
- **Gestion de parches:** Aplicar parches de seguridad en < 48h para criticos
- **Rotacion de secretos:** Cambiar claves de API y certificados periodicamente
- **Backups cifrados:** Diarios, con prueba de restauracion mensual
- **Plan de respuesta a incidentes:** Roles definidos, procedimientos documentados
- **Auditoria trimestral:** Revisar logs, accesos, configuraciones
- **Bug bounty program:** Programa de recompensas para investigadores externos

---

## Ejercicio 2: Crear Checklist de Seguridad para cada Fase del SSDLC

Crear un checklist practico (minimo 5 items por fase) que un desarrollador pueda usar diariamente.

### Solucion: Checklist SSDLC

#### Requisitos
- [ ] Se identificaron requisitos regulatorios aplicables (GDPR, PCI DSS, HIPAA)?
- [ ] Se definio el nivel de autenticacion requerido para cada funcionalidad?
- [ ] Se documentaron los datos sensibles que manejara el sistema?
- [ ] Se establecieron criterios de aceptacion de seguridad?
- [ ] Se realizo un analisis de riesgos inicial?

#### Diseno
- [ ] Se realizo threat modeling (STRIDE) sobre la arquitectura?
- [ ] Se aplico el principio de minimo privilegio en el diseno de roles?
- [ ] Se definio el cifrado para datos en transito y en reposo?
- [ ] Los errores del sistema no revelan informacion sensible?
- [ ] Se diseno la separacion de datos sensibles (pago, personales)?

#### Codificacion
- [ ] Se usan consultas parametrizadas para todas las operaciones de BD?
- [ ] Las contrasenas se almacenan con bcrypt/Argon2?
- [ ] Las entradas del usuario se validan y sanitizan?
- [ ] No hay secretos (claves, tokens) hardcodeados en el codigo?
- [ ] Se manejan excepciones sin exponer informacion tecnica?

#### Pruebas
- [ ] Se ejecuto SAST en el codigo fuente?
- [ ] Se ejecutaron pruebas DAST contra la aplicacion en staging?
- [ ] Se revisaron las dependencias con SCA?
- [ ] Se probaron escenarios de autenticacion (login fallido, fuerza bruta)?
- [ ] Se verifico que no hay endpoints sin autenticacion?

#### Despliegue
- [ ] HTTPS esta configurado y redirige desde HTTP?
- [ ] Los headers de seguridad estan presentes (HSTS, CSP, X-Frame-Options)?
- [ ] Los secretos se cargan desde un vault o variables de entorno?
- [ ] El servidor/sistema esta hardening (puertos cerrados, servicios minimos)?
- [ ] Las imagenes Docker estan escaneadas y sin vulnerabilidades criticas?

#### Mantenimiento
- [ ] Hay monitoreo de seguridad activo con alertas?
- [ ] Los parches de seguridad se aplican en menos de 48h para criticos?
- [ ] Los backups se prueban mensualmente?
- [ ] El plan de respuesta a incidentes esta documentado y actualizado?
- [ ] Se realizan revisiones periodicas de acceso y permisos?

---

## Preguntas y Respuestas

### Pregunta 1
**Cual es la principal diferencia entre el desarrollo tradicional y el SSDLC?**

**Respuesta:** La principal diferencia es el momento en que se integra la seguridad. En el desarrollo tradicional (Waterfall, Agile sin seguridad), la seguridad se evalua al final, justo antes o despues del despliegue. En el SSDLC, la seguridad se integra en cada fase desde los requisitos hasta el mantenimiento. Esto permite detectar y corregir vulnerabilidades temprano, reduciendo costos y riesgos significativamente.

### Pregunta 2
**Que significa "fail secure" y de un ejemplo?**

**Respuesta:** "Fail secure" significa que cuando un sistema falla, debe hacerlo de manera que mantenga la seguridad (denegando acceso) en lugar de permitir acceso no autorizado. Ejemplo: si un servidor de autenticacion falla, el sistema debe denegar todos los accesos (fail closed) en lugar de permitirlos (fail open). En un sistema de control de acceso fisico, si la cerradura electronica falla, debe permanecer cerrada, no abierta.

### Pregunta 3
**Para que sirve OWASP SAMM? En que se diferencia de un checklist de seguridad?**

**Respuesta:** OWASP SAMM (Software Assurance Maturity Model) es un modelo de madurez que permite evaluar el estado actual de las practicas de seguridad de una organizacion y crear una hoja de ruta de mejora. A diferencia de un checklist (que es binario: cumple/no cumple), SAMM define niveles de madurez (0-3) para cada practica, permitiendo mejoras graduales y medibles. Es un marco estrategico, no tactico.

### Pregunta 4
**Que es un "gate" de seguridad en CI/CD? De un ejemplo.**

**Respuesta:** Un gate de seguridad en CI/CD es un punto en el pipeline donde se evalua automaticamente una condicion de seguridad. Si no se cumple, el pipeline se detiene y no se despliega. Ejemplo: en el pipeline de CI, despues de compilar, se ejecuta SAST (analisis estatico). Si se encuentra una vulnerabilidad de severidad "critica" o "alta", el pipeline falla y el equipo de desarrollo debe corregirla antes de que el codigo pase a produccion.

### Pregunta 5
**Por que es importante hacer threat modeling en la fase de diseno y no despues?**

**Respuesta:** El threat modeling en la fase de diseno permite identificar amenazas antes de escribir codigo. Si se descubre una amenaza arquitectonica (ej: diseno que permite fuga de datos entre inquilinos) despues de implementar, corregirla puede requerir reescribir grandes porciones del sistema. Encontrar problemas de diseno cuando solo existen diagramas es mucho mas barato que cuando ya hay miles de lineas de codigo. Ademas, el threat modeling guia las decisiones de diseno hacia opciones inherentemente mas seguras.

---

## Tarea / Lectura Recomendada

1. **Leer:** Microsoft SDL - https://www.microsoft.com/en-us/securityengineering/sdl/
2. **Leer:** NIST SSDF SP 800-218 - https://csrc.nist.gov/publications/detail/sp/800-218/final
3. **Leer:** OWASP SAMM - https://owaspsamm.org/
4. **Practicar:** Aplicar el checklist de SSDLC a un proyecto propio o de ejemplo
5. **Profundizar:** Leer "Secure Software Development Lifecycle" de OWASP - https://owasp.org/www-project-secure-software-development-lifecycle/
