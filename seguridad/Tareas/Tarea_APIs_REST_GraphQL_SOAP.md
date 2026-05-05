# Tarea: Seguridad en APIs REST, GraphQL y SOAP

---

## Tema 1: A01 - Broken Access Control en APIs REST

**Fecha:** 16/4

### Asignado
- [Equipo a definir]

### Presentación requerida:
- IDOR (Insecure Direct Object Reference) - horizontal y vertical
- Path Traversal / Directory Traversal
- Bypass de restricciones (parámetros modificados, JWT manipulation)
- CORS mal configurado
- Jerarquía de roles y bypass de RBAC

### Demo práctica:
- Usar Juice Shop para encontrar vulnerabilidades de IDOR
- Demo de Path Traversal con DVWA o similar
- Mostrar bypass de controles con Burp Suite o OWASP ZAP

### Entregables:
- Presentación de 40 min
- Demo de explotación en entorno controlado
- Checklist de protección

---

## Tema 2: A02 - Seguridad en APIs GraphQL

**Fecha:** 16/4

### Asignado
- [Equipo a definir]

### Presentación requerida:
- Introspection y exposición de schema completo
- Query Depth Attack (anidamiento infinito)
- Query Complexity / Alias Overloading
- Batch Attacks y bypass de rate limiting
- BOLA en GraphQL (resolvers sin autorización)
- Herramientas específicas: InQL, GraphQL Voyager, Altair

### Demo práctica:
- Exponer schema con introspection en un endpoint vulnerable
- Enviar query de profundidad excesiva para provocar DoS
- Usar InQL para mapear automáticamente un API GraphQL
- Demostrar bypass de rate limit con batch queries

### Entregables:
- Presentación de 40 min
- Demo de explotación en entorno controlado
- Checklist de protección (depth limiter, complexity, batch limit)

---

## Tema 3: A03 - Seguridad en APIs SOAP

**Fecha:** 16/4

### Asignado
- [Equipo a definir]

### Presentación requerida:
- XXE (XML External Entity) - lectura de archivos del servidor
- XML Bomb / Billion Laughs Attack - DoS por expansión exponencial
- WSDL Disclosure público - mapa completo del servicio
- SOAP Action Spoofing - ejecución de operaciones no autorizadas
- XML Signature Wrapping - bypass de autenticación
- WS-Security (Password Digest, firma digital, timestamps)

### Demo práctica:
- Inyectar entidad XXE en un servicio SOAP vulnerable
- Crear XML Bomb y demostrar consumo de memoria
- Usar SoapUI Security para escanear un servicio SOAP
- Mostrar WS-Security correcto vs incorrecto

### Entregables:
- Presentación de 40 min
- Demo de explotación en entorno controlado
- Checklist de protección (XXE prevention, XML limits, WS-Security)

---

## Tema 4: Pipeline CI/CD Seguro para APIs

**Fecha:** 16/4

### Asignado
- [Equipo a definir]

### Presentación requerida:
- SAST: `semgrep scan --config auto` - análisis estático de código
- SCA: `mvn org.owasp:dependency-check-maven:check` - dependencias vulnerables
- Escaneo filesystem: `trivy fs --severity HIGH,CRITICAL C:\Agesic\`
- Bytecode: `mvn spotbugs:spotbugs` - bugs en Java
- SBOM con CycloneDX - inventario de componentes
- DAST: OWASP ZAP para escaneo dinámico de APIs
- Pipeline Jenkins completo con fail-fast

### Demo práctica:
- Ejecutar Semgrep sobre un proyecto con vulnerabilidades intencionales
- Generar SBOM con CycloneDX y analizarlo con Trivy
- Ejecutar pipeline Jenkins y mostrar build fallido por vulnerabilidad crítica
- Mostrar reportes HTML/JSON generados por cada herramienta

### Entregables:
- Presentación de 40 min
- Demo de pipeline CI/CD en entorno controlado
- Checklist de seguridad para integración continua

---

## Herramientas requeridas para todas las demos

| Herramienta | Uso |
|-------------|-----|
| OWASP Juice Shop | App vulnerable para IDOR y BOLA |
| DVWA | Path Traversal y otros ataques web |
| Burp Suite / OWASP ZAP | Proxy y scanner de APIs |
| SoapUI | Testing y security scan de SOAP |
| InQL | Scanner de introspection GraphQL |
| Semgrep | Análisis estático de código |
| Trivy | Escaneo de filesystem e imágenes |
| OWASP Dependency Check | Análisis de dependencias Java |
| SpotBugs | Análisis de bytecode Java |
| Jenkins | Pipeline CI/CD |
| CycloneDX | Generación de SBOM |
