# Informe Técnico: Estrategia Integral de Seguridad Mobile y SDLC

**Preparado para:** Gestión de Arquitectura y Seguridad  
**Objetivo:** Blindar el ecosistema mobile y asegurar la cadena de suministro de software  
**Extensión:** Resumen técnico ejecutivo

---

## I. Arquitectura de Red y Exposición Mobile

### API Discovery (Configuración Dinámica)

**Qué hacer:** La app no debe contener URLs hardcodeadas. Al iniciar, consulta un único endpoint de discovery que devuelve el mapa de rutas activas.

**Por qué:** Permite rotar infraestructura (cambios de IP en F5, migraciones cloud) sin actualizar la app en las tiendas. Elimina el riesgo de URLs quemadas en el código.

### Patrón BFF (Backend for Frontend)

**Qué hacer:** Interponer una capa BFF entre la app y los microservicios internos. La app solo conoce UNA URL (la del BFF expuesta en el F5).

**Por qué:** Oculta la topología interna de red. El BFF agrega datos, aplica políticas de seguridad y centraliza la autenticación. Sin BFF, cada microservicio queda expuesto como superficie de ataque individual.

### F5 / API Gateway + SSL Pinning

**Qué hacer:** El F5 (o API Manager) gestiona la terminación TLS. En la app se configura SSL Pinning: la app valida que el hash de la clave pública del certificado recibido coincida con un hash pre-almacenado. Si no coincide, aborta la conexión.

**Por qué:** Es la única defensa real contra Man-in-the-Middle (MitM) en redes Wi-Fi públicas. Sin pinning, un atacante con un proxy (Burp, mitmproxy) puede interceptar todo el tráfico.

---

## II. Identidad y Protección de Tokens (OAuth 2.1)

### PKCE (Proof Key for Code Exchange)

**Qué hacer:** En el flujo OAuth mobile, la app genera un `code_verifier` aleatorio por cada login, envía su hash (`code_challenge`) al solicitar el código de autorización, y presenta el `code_verifier` original al canjearlo por tokens.

**Por qué:** Sin PKCE, cualquier app maliciosa en el dispositivo que intercepte el authorization code puede canjearlo por un token de acceso. PKCE ata criptográficamente el code a la app que lo solicitó.

### DPoP (Demonstrating Proof-of-Possession)

**Qué hacer:** Al obtener el token de acceso, la app genera un par de claves asimétricas (almacenadas en Secure Enclave / TrustZone). Cada request al backend se firma con la clave privada; el servidor verifica con la clave pública.

**Por qué:** Los tokens bearer tradicionales funcionan como "efectivo": quien los tiene, los usa. Si un atacante roba el token del almacenamiento del teléfono, DPoP lo vuelve inútil en otra máquina porque no tiene la clave privada para firmar.

### Flujo Completo

```
App → Discovery (obtiene URL del BFF)
     → Login con PKCE (obtiene token + par de claves DPoP)
     → Cada API call: token + DPoP proof firmado
     → BFF verifica DPoP, valida token, reenvía al microservicio
```

---

## III. Integridad y Anti-Tampering (Mobile)

### App Attestation

**Qué hacer:** Implementar Play Integrity (Android) y App Attest (iOS). El backend recibe un token de atestación y valida que la app no esté modificada, no corra en emulador y el dispositivo no esté rooteado. Rechazar peticiones si la atestación falla.

**Por qué:** Sin atestación, un atacante puede decompilar la app, quitar el SSL Pinning, y re-empaquetarla para interceptar tráfico o automatizar ataques.

### Ofuscación con Capa Nativa (NDK)

**Qué hacer:** Mover lógica sensible (validación de firmas, URLs de discovery, generación de code_verifier) a librerías C/C++ vía NDK. Usar R8/ProGuard (o DexGuard) para ofuscar el bytecode Java/Kotlin.

**Por qué:** Las herramientas de decompilación estándar (JADX, apktool) leen bytecode Java con facilidad. El código nativo (C/C++) requiere ingeniería inversa con Ghidra/IDA Pro, elevando significativamente el costo del ataque.

---

## IV. Gobierno de Desarrollo y SDLC

### Gestión de Artefactos (Nexus / Artifactory)

**Qué hacer:** Configurar Nexus (o Artifactory) como proxy forzado para npm, pip, maven. Los desarrolladores NO pueden consumir librerías directo de internet; todo pasa por el repositorio interno. Configurar políticas de bloqueo de CVEs críticos.

**Por qué:** Previene ataques de Dependency Confusion (librería maliciosa con mismo nombre que una interna) y garantiza que las versiones de librerías sean inmutables y auditables.

### SCA en el Pipeline (Trivy / Dependency-Check)

**Qué hacer:** Integrar Trivy o OWASP Dependency-Check en el `.gitlab-ci.yml` o Jenkinsfile. Escanear dependencias en cada commit. Fallar el build (`Build Break`) solo ante vulnerabilidades CRITICAL o HIGH. Reportar MEDIUM/LOW como advertencias.

```bash
# Ejemplo: escaneo en pipeline
trivy fs --severity HIGH,CRITICAL --fail-on-severity CRITICAL .
mvn org.owasp:dependency-check-maven:check -DfailBuildOnCVSS=7
```

**Por qué:** Las dependencias de terceros representan ~80% del código en una app moderna. Log4Shell (CVE-2021-44228) demostró que sin SCA, saber si estás afectado puede llevar días; con SCA son minutos.

### SAST (SonarQube)

**Qué hacer:** Ejecutar SonarQube en el pipeline para analizar el código propio (no dependencias). Configurar Quality Gate que exija 0 vulnerabilidades, 0 bugs y coverage > 80%.

**Por qué:** Complementa al SCA: mientras Dependency-Check mira las librerías de terceros, SonarQube encuentra errores de seguridad en el código que escriben tus desarrolladores.

### SBOM (Software Bill of Materials)

**Qué hacer:** Generar automáticamente un SBOM en formato CycloneDX al finalizar el build. Almacenarlo como artefacto del pipeline.

```bash
mvn org.cyclonedx:cyclonedx-maven-plugin:makeAggregateBom
trivy fs --format cyclonedx -o sbom.json .
```

**Por qué:** Cuando se descubre una nueva vulnerabilidad (ej. Log4Shell 2.0), el SBOM te dice en minutos si estás afectado, sin tener que revisar cada repositorio manualmente.

---

## V. Resumen de la Pila Tecnológica

| Capa | Componente | Tecnología | Propósito |
|------|-----------|------------|-----------|
| **Red** | Gateway | F5 BIG-IP / API Manager | Terminación TLS, exposición del BFF |
| **Arquitectura** | BFF | Backend for Frontend | Ocultar topología interna, agregar seguridad |
| **Mobile** | Discovery | Remote Config / API propia | URLs dinámicas sin hardcodeo |
| **Mobile** | SSL Pinning | Cliente (app) + F5 | Mitigación de MitM |
| **Mobile** | Ofuscación | R8/ProGuard + NDK (C/C++) | Elevar costo de ingeniería inversa |
| **Identidad** | Auth | OAuth 2.1 + PKCE | Protección del authorization code |
| **Identidad** | Token Binding | DPoP | Token atado al dispositivo |
| **Integridad** | Atestación | Play Integrity + App Attest | Validación de dispositivo y app |
| **Artefactos** | Proxy | Sonatype Nexus | Gobierno de dependencias |
| **SCA** | Escaneo | Trivy / OWASP Dependency-Check | Detectar CVEs en librerías |
| **SAST** | Calidad | SonarQube | Detectar bugs en código propio |
| **SBOM** | Inventario | CycloneDX | Auditoría de componentes |

---

## VI. Conclusiones y Recomendaciones Prioritarias

1. **Corto plazo (1-2 semanas):** Implementar PKCE en todos los flujos OAuth mobile. Configurar Nexus como proxy forzado para npm/pip/maven. Agregar Trivy al pipeline con fail en CRITICAL.

2. **Mediano plazo (1-2 meses):** Implementar BFF para todas las apps mobile. Agregar SSL Pinning en cliente. Configurar SonarQube y SBOM automático en el pipeline.

3. **Largo plazo (3-6 meses):** Migrar a DPoP. Implementar App Attestation (Play Integrity + App Attest). Mover lógica sensible a capa NDK. Evaluar madurez con pruebas de penetración.

La combinación de **BFF + Discovery** da agilidad operativa; **PKCE + DPoP** asegura identidad; **App Attest + SSL Pinning** garantiza integridad del cliente; **Nexus + Trivy + SonarQube + SBOM** cierra la cadena de suministro. Sin estas capas, el ecosistema mobile depende de buenas intenciones en lugar de controles verificables.

---

*Documento consolidado - Mayo 2026*
