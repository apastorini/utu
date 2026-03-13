# 📋 Tareas de Vulnerabilidades OWASP - Presentaciones

**Duración de cada presentación:** 40 minutos  
**Objetivo:** Profundizar en cada vulnerabilidad OWASP, mostrando variantes, explotación, detección y protección  
**Herramienta sugerida:** OWASP Juice Shop para prácticas

---

## Tarea 1: A01 - Broken Access Control (Variantes y Defensa en Profundidad)

**Presentación requerida:**
- IDOR (Insecure Direct Object Reference) - horizontal y vertical
- Path Traversal / Directory Traversal
- Bypass de restricciones (parámetros modificados, JWT manipulation)
- CORS mal configurado
- JC (Jerarquía de roles) y bypass deRBAC

**Demo práctica:**
- Usar Juice Shop para encontrar vulnerabilidades de IDOR
- Demo de Path Traversal con DVWA o similar
- Mostrar bypass de controles con Burp Suite

**Entregables:**
- Presentación de 40 min
- Demo de explotación en entorno controlado
- Checklist de protección

---

## Tarea 2: A02 - Cryptographic Failures (Criptografía Aplicada)

**Presentación requerida:**
- Contraseñas sin hash (MD5, SHA1 vulnerabilities)
- Claves hardcodeadas y en repositorios
- Datos sensibles en texto plano en BD
- TLS/SSL mal configurado (versiones outdated)
- Algoritmos débiles (RC4, 3DES, etc.)

**Demo práctica:**
- Crackear hashes con John the Ripper / Hashcat
- Demonstrar слабость de algoritmos MD5/SHA1
- Configurar SSL correctamente con test de SSL Labs

**Entregables:**
- Presentación de 40 min
- Demo de cracking de contraseñas
- Guía de configuración criptográfica segura

---

## Tarea 3: A03 - Injection (SQL, NoSQL, Command, LDAP, XML)

**Presentación requerida:**
- SQL Injection (In-band, Blind, Out-of-band, Second-order)
- NoSQL Injection
- Command Injection
- LDAP Injection
- XPath/XML Injection
- ORM Injection

**Demo práctica:**
- SQLmap en Juice Shop o DVWA
- Command injection en WebGoat
- NoSQL injection con MongoDB

**Entregables:**
- Presentación de 40 min
- Demostración de explotación con herramientas
- Código seguro con prepared statements

---

## Tarea 4: A04 - Insecure Design (Diseño de Seguridad)

**Presentación requerida:**
- Falta de rate limiting
- Ausencia de threat modeling
- Business logic vulnerabilities
- Race conditions
- Authentication bypass por lógica de aplicación
- Captcha bypass

**Demo práctica:**
- Demonstrar falta de rate limiting
- Explotar race conditions en aplicaciones
- Bypass de lógica de negocio

**Entregables:**
- Presentación de 40 min
- Diagramas de threat modeling
- Checklist de secure design

---

## Tarea 5: A05 - Security Misconfiguration (Hardening Completo)

**Presentación requerida:**
- Headers de seguridad faltantes (CSP, X-Frame-Options, etc.)
- Debug mode en producción
- Mensajes de error verbose
- CORS permisivo
- Default credentials
- Servicios innecesarios expuestos

**Demo práctica:**
- Escaneo con Nikto, Nmap
- Verificar headers con curl/Burp
- Hardening de servidor (Nginx/Apache)

**Entregables:**
- Presentación de 40 min
- Script de hardening automatizado
- Checklist de configuración segura

---

## Tarea 6: A06 - Vulnerable and Outdated Components (Gestión de Dependencias)

**Presentación requerida:**
- Libraries y frameworks desactualizados
- Dependencias con vulnerabilidades conocidas (Log4j, Spring4Shell)
- Componentes sin soporte
- Registry poisoning
- Typo-squatting en packages

**Demo práctica:**
- npm audit / pip safety
- OWASP Dependency-Check
- Encontrar vulnerabilidades en proyecto real

**Entregables:**
- Presentación de 40 min
- Integración de Dependabot en repositorio
- Política de gestión de dependencias

---

## Tarea 7: A07 - Identification and Authentication Failures (Auth Security)

**Presentación requerida:**
- Credential stuffing
- Session fixation/hijacking
- Weak password policies
- Session expiration failures
- MFA bypass techniques
- OAuth/OpenID vulnerabilities

**Demo práctica:**
- Hydra para credential stuffing
- Session hijacking con Burp Suite
- Testing de MFA

**Entregables:**
- Presentación de 40 min
- Policy de contraseñas segura
- Configuración de MFA

---

## Tarea 8: A08 - Software and Data Integrity Failures (Supply Chain Security)

**Presentación requerida:**
- Deserialización insegura
- CI/CD pipeline attacks
- Insecure dependencies (typosquatting)
- Code injection en pipelines
- Marshalling/Unmarshalling vulnerabilities
- Deserialization gadgets (Java, Python)

**Demo práctica:**
- Explotar deserialización en Java/Python
- Demo de compromiso de pipeline CI/CD
- Verificar integridad de dependencias

**Entregables:**
- Presentación de 40 min
- Análisis de riesgos de supply chain
- Pipeline seguro documentado

---

## Tarea 9: A09 - Security Logging and Monitoring Failures (Blue Team)

**Presentación requerida:**
- Falta de logging
- Logs sin auditoría
- No detectar ataques en progreso
- Retention policy insuficiente
- Log injection
- OWASP ZAP / SIEM integration

**Demo práctica:**
- Configurar logging en aplicación vulnerable
- Detectar ataques con logs
- Integration con ELK Stack o similar

**Entregables:**
- Presentación de 40 min
- Configuración de logging seguro
- Dashboard de detección

---

## Tarea 10: A10 - Server-Side Request Forgery (SSRF) (Red Team)

**Presentación requerida:**
- SSRF básico y avanzado
- Bypass de filtros (DNS rebinding, URL parsing)
- Cloud metadata exploitation (AWS, GCP, Azure)
- Internal port scanning via SSRF
- Blind SSRF

**Demo práctica:**
- Explotar SSRF en Juice Shop
- Extraer metadata de AWS/GCP
- Bypass de filtros comunes

**Entregables:**
- Presentación de 40 min
- Laboratorio de SSRF
-Guía de mitigación

---

## Distribución Sugerida

| Grupo | Vulnerabilidad |OWASP Code |
|-------|----------------|------------|
| Grupo 1 | Broken Access Control | A01 |
| Grupo 2 | Cryptographic Failures | A02 |
| Grupo 3 | Injection (SQL, NoSQL, CMD) | A03 |
| Grupo 4 | Insecure Design | A04 |
| Grupo 5 | Security Misconfiguration | A05 |
| Grupo 6 | Vulnerable Components | A06 |
| Grupo 7 | Identification/Auth Failures | A07 |
| Grupo 8 | Software/Data Integrity | A08 |
| Grupo 9 | Logging/Monitoring | A09 |
| Grupo 10 | SSRF | A10 |

---

## Criterios de Evaluación por Presentación

1. **Profundidad técnica** (20%): Conocimiento de variantes y técnicas
2. **Demo práctica** (30%): Demostración funcional con herramientas
3. **Protección y mitigación** (20%): Controles efectivos
4. **Calidad de presentación** (15%): Claridad y organización
5. **Recursos adicionales** (15%): Lab, guías, herramientas

---

## Herramientas Recomendadas para Laboratorio

| Herramienta | Tipo | Uso Principal |
|-------------|------|---------------|
| OWASP Juice Shop | VM/Docker | Laboratorio web vulnerable |
| DVWA | PHP | SQLi, XSS, CSRF |
| WebGoat | Java | Lecciones de seguridad |
| Metasploitable | Linux | Vulnerabilidades múltiples |
| Burp Suite | Proxy | Testing manual |
| SQLmap | Automatizado | SQL Injection |
| Nmap | Escaneo | Puertos y servicios |
| Nikto | Web scan | Vulnerabilidades web |
| John the Ripper | Password cracking | Hashes |
| OWASP ZAP | Proxy | Scanner automático |

---

## Conexión con el Curso

| Presentación | Tema relacionado del curso |
|--------------|---------------------------|
| A01 - Broken Access Control | Parte 5 - OWASP |
| A02 - Cryptographic Failures | Parte 4 - Certificados |
| A03 - Injection | Parte 5 - SQL Injection |
| A04 - Insecure Design | Parte 5 - Threat Modeling |
| A05 - Security Misconfiguration | Parte 5 - Hardening |
| A06 - Vulnerable Components | Parte 5 - Dependencias |
| A07 - Auth Failures | Parte 3 - Autenticación |
| A08 - Integrity Failures | Parte 6 - APIs |
| A09 - Logging | Parte 9 - Incident Response |
| A10 - SSRF | Parte 6 - APIs