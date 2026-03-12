# CURSO COMPLETO DE CIBERSEGURIDAD - ÍNDICE GENERAL

## 📚 Estructura del Curso

Este curso está diseñado para llevarte desde cero hasta un nivel profesional en ciberseguridad, con enfoque práctico y ejemplos ejecutables.

---

## 📖 CONTENIDO POR ARCHIVO

### **Parte 1: Fundamentos** (`Curso_Ciberseguridad_Parte1.md`)

#### MÓDULO 1: Fundamentos de la Seguridad Informática
- 1.1 Motivación y estadísticas
- 1.2 Tríada CIA (Confidencialidad, Integridad, Disponibilidad)
  - Ejemplos de código en Python
  - Casos prácticos reales
- 1.3 Tipos de Ataques Comunes
  - Phishing (tipos y ejemplos)
  - Malware (virus, ransomware, troyanos)
  - DDoS (volumétricos, de protocolo, de aplicación)
  - SQL Injection (con código vulnerable y seguro)
  - XSS (Cross-Site Scripting)
- 1.4 Privacidad y Protección de Datos
  - Ley 18.331 (Uruguay)
  - GDPR (Europa)
  - Derechos ARCO
  - Ejemplo de RAT (Registro de Actividades de Tratamiento)

#### MÓDULO 2: Áreas de Aplicación
- 2.1 Dominios de Ciberseguridad
  - Seguridad de Red (firewalls, IDS/IPS, VPN)
  - Seguridad de Aplicaciones (SDLC, SAST, DAST)
  - Seguridad en la Nube (IaaS, PaaS, SaaS)

---

### **Parte 2: Criptografía** (`Curso_Ciberseguridad_Parte2.md`)

#### MÓDULO 3: Criptografía
- 3.1 Conceptos Fundamentales
- 3.2 Criptografía Simétrica (AES)
  - Ejemplos en Python
  - Ejemplos en PowerShell
- 3.3 Criptografía Asimétrica (RSA)
  - Generación de claves
  - Cifrado y descifrado
- 3.4 Funciones Hash
  - SHA-256, bcrypt, Argon2
  - Verificación de integridad
  - Almacenamiento seguro de contraseñas
- 3.5 Firma Digital
  - Proceso completo con ejemplos
- 3.6 Certificados Digitales y PKI
  - Generar certificados SSL/TLS
  - Configurar HTTPS en Nginx
- 3.7 Protocolos de Encriptación
  - TLS/SSL
  - SSH (configuración segura)
  - VPN (WireGuard)
- 3.8 Computación Cuántica y Criptografía Post-Cuántica

#### MÓDULO 4: Herramientas de Seguridad
- 4.1 Nmap (escaneo de redes)
- 4.2 Wireshark / tcpdump (análisis de tráfico)

---

### **Parte 3: DevSecOps** (`Curso_Ciberseguridad_Parte3.md`)

#### MÓDULO 5: Herramientas Avanzadas y DevSecOps
- 5.1 Trivy (escaneo de vulnerabilidades)
- 5.2 **LABORATORIO COMPLETO: Jenkins + Docker + Trivy**
  - Instalación paso a paso
  - Creación de pipeline CI/CD
  - Escaneo automático de seguridad
  - Quality gates
- 5.3 SonarQube (análisis estático)
  - Código Java vulnerable y corregido
- 5.4 OWASP ZAP (pruebas dinámicas)
  - Aplicación vulnerable en Flask
- 5.5 Metasploit (framework de explotación)
- 5.6 Burp Suite (proxy de interceptación)

#### MÓDULO 6: Seguridad en Bases de Datos
- 6.1 PostgreSQL
  - Configuración segura
  - Cifrado de datos sensibles (pgcrypto)
  - Control de acceso granular (RBAC)
  - Row Level Security (RLS)
- 6.2 MongoDB
  - Autenticación
  - Cifrado de campos en Node.js
  - Roles personalizados
- 6.3 Cumplimiento y Compliance
  - Implementación técnica de GDPR
  - Derecho al olvido
  - Portabilidad de datos

---

### **Parte 4: Certificados Digitales** (`Curso_Ciberseguridad_Parte4_Certificados.md`)

#### MÓDULO 7: Certificados Digitales, KeyStores y TrustStores
- 7.1 Fundamentos de Certificados Digitales
  - Estructura X.509 (con diagrama visual)
  - Atributos (CN, O, OU, L, ST, C)
  - Extensiones (SAN, Key Usage, etc.)
- 7.2 Cadena de Confianza (Chain of Trust)
  - Root CA, Intermediate CA, End-Entity
  - Diagrama de verificación
- 7.3 **KeyStore vs TrustStore**
  - Diferencias conceptuales
  - Contenido de cada uno
  - Diagramas comparativos
- 7.4 Tipos de Certificados
  - DV, OV, EV
  - SSL/TLS, Client, Code Signing, S/MIME
  - Wildcard, Multi-Domain (SAN)
- 7.5 **Certificados Autofirmados**
  - Qué son y cuándo usarlos
  - Cómo los maneja el navegador
  - Crear certificado autofirmado
  - Agregar al TrustStore
- 7.6 Trabajar con KeyStores en Java
  - Crear KeyStore con keytool
  - Crear TrustStore
  - Usar en aplicación Java
  - Configurar en Spring Boot
- 7.7 Let's Encrypt
  - Obtener certificado con Certbot
  - Configuración Nginx
- 7.8 Laboratorio Completo: HTTPS con Certificados
  - Servidor HTTPS en Python
  - Pruebas con curl

---

### **Parte 5: OWASP Top 10** (`Curso_Ciberseguridad_Parte5_OWASP.md`)

#### MÓDULO 8: OWASP Top 10 y Seguridad de Aplicaciones Web
- 8.1 OWASP Top 10 (2021) - Visión General
- 8.2 **A01 - Broken Access Control**
  - Código vulnerable y seguro
  - Diagrama de ataque
- 8.3 **A02 - Cryptographic Failures**
  - Contraseñas en texto plano vs bcrypt
  - Claves hardcodeadas vs variables de entorno
- 8.4 **A03 - Injection**
  - SQL Injection (análisis profundo)
  - Tipos: In-band, Blind, Out-of-band
  - Prevención completa
  - Laboratorio con sqlmap
- 8.5 **A04 - Insecure Design**
  - Rate limiting con Flask-Limiter
  - Threat Modeling con STRIDE
- 8.6 **A05 - Security Misconfiguration**
  - Configuración segura de Flask
  - Headers de seguridad
  - Checklist de hardening Nginx
- 8.7 **A06 - Vulnerable and Outdated Components**
  - Gestión de dependencias (pip, npm, maven)
  - Dependabot
- 8.8 **A10 - Server-Side Request Forgery (SSRF)**
  - Código vulnerable y seguro
  - Validación de URLs

#### MÓDULO 9: Pentesting y Ethical Hacking
- 9.1 Metodología de Pentesting (6 fases)
- 9.2 Herramientas Esenciales (Kali Linux)
- 9.3 Laboratorio: Pentesting Completo

---

### **Diagramas Visuales** (`Diagramas_Visuales.md`)

Contiene 10 diagramas pedagógicos en ASCII art:

1. **Defensa en Profundidad** (7 capas de seguridad)
2. **Flujo de Autenticación con JWT** (paso a paso)
3. **Ataque Man-in-the-Middle** (HTTP vs HTTPS)
4. **Arquitectura de Microservicios Segura**
5. **Ciclo de Vida de Incidente de Seguridad** (NIST)
6. **Modelo Zero Trust** (vs modelo tradicional)
7. **Pipeline CI/CD Seguro** (DevSecOps completo)
8. **Criptografía Simétrica vs Asimétrica** (comparación visual)
9. **Ataque de Fuerza Bruta** (complejidad de contraseñas)
10. **Anatomía de un Ataque de Phishing** (email + página falsa)

---

## 🎯 CÓMO USAR ESTE CURSO

### Para Estudiantes

1. **Lectura secuencial:** Comienza por la Parte 1 y avanza en orden
2. **Práctica obligatoria:** Ejecuta TODOS los ejemplos de código
3. **Laboratorios:** Dedica tiempo extra a los laboratorios completos
4. **Diagramas:** Usa los diagramas visuales para entender conceptos

### Para Docentes

1. **Módulos independientes:** Cada módulo puede enseñarse por separado
2. **Ejemplos adaptables:** Modifica los ejemplos según tu contexto
3. **Evaluaciones:** Usa los laboratorios como trabajos prácticos
4. **Diagramas:** Proyecta los diagramas en clase

### Para Profesionales

1. **Referencia rápida:** Busca el tema específico en el índice
2. **Actualización:** Revisa las partes de DevSecOps y OWASP
3. **Implementación:** Adapta los ejemplos a tu stack tecnológico

---

## 🛠️ REQUISITOS TÉCNICOS

### Software Necesario

```bash
# Sistema Operativo
- Linux (Ubuntu 22.04 recomendado)
- Windows 10/11 con WSL2
- macOS

# Lenguajes
- Python 3.8+
- Java 11+
- Node.js 16+

# Herramientas
- Docker y Docker Compose
- Git
- OpenSSL
- curl / wget

# Editores
- VS Code (recomendado)
- IntelliJ IDEA
- PyCharm
```

### Instalación Rápida (Ubuntu)

```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar herramientas básicas
sudo apt install -y \
  python3 python3-pip \
  openjdk-11-jdk \
  nodejs npm \
  docker.io docker-compose \
  git curl wget \
  nmap wireshark \
  openssl

# Instalar bibliotecas Python
pip3 install \
  cryptography \
  bcrypt \
  flask \
  flask-limiter \
  flask-cors \
  flask-talisman \
  psycopg2-binary \
  sqlalchemy \
  requests

# Agregar usuario a grupo docker
sudo usermod -aG docker $USER

# Reiniciar sesión para aplicar cambios
```

---

## 📊 PROGRESIÓN SUGERIDA

### Nivel Principiante (Semanas 1-4)
- ✅ Parte 1: Fundamentos completos
- ✅ Parte 2: Criptografía básica (hasta 3.5)
- ✅ Diagramas 1-3

### Nivel Intermedio (Semanas 5-8)
- ✅ Parte 2: Criptografía avanzada (3.6-3.8)
- ✅ Parte 3: Herramientas (hasta 5.4)
- ✅ Parte 4: Certificados completo
- ✅ Diagramas 4-7

### Nivel Avanzado (Semanas 9-12)
- ✅ Parte 3: DevSecOps completo
- ✅ Parte 5: OWASP Top 10 completo
- ✅ Módulo 9: Pentesting
- ✅ Diagramas 8-10
- ✅ Proyecto final integrador

---

## 🎓 PROYECTO FINAL SUGERIDO

**Título:** Sistema de E-commerce Seguro

**Requisitos:**
1. Aplicación web con autenticación (JWT + MFA)
2. Base de datos con cifrado de datos sensibles
3. HTTPS con certificado (Let's Encrypt o autofirmado)
4. Pipeline CI/CD con escaneo de seguridad (Trivy + SonarQube)
5. Protección contra OWASP Top 10
6. Documentación de arquitectura de seguridad
7. Plan de respuesta a incidentes

**Entregables:**
- Código fuente en GitHub
- Dockerfile y docker-compose.yml
- Pipeline de Jenkins/GitLab CI
- Reporte de seguridad (vulnerabilidades encontradas y mitigadas)
- Presentación de 20 minutos

---

## 📚 BIBLIOGRAFÍA COMPLEMENTARIA

### Libros
1. **W. Stallings, L. Brown** - "Computer Security: Principles and Practice" (4th Edition, 2018)
2. **OWASP** - "OWASP Testing Guide v4.2"
3. **NIST** - "Cybersecurity Framework"

### Recursos Online
- [OWASP.org](https://owasp.org) - Proyectos y documentación
- [CERTuy](https://www.gub.uy/centro-nacional-respuesta-incidentes-seguridad-informatica/) - Materiales didácticos Uruguay
- [HackTheBox](https://www.hackthebox.com) - Laboratorios prácticos
- [TryHackMe](https://tryhackme.com) - Aprendizaje guiado
- [PortSwigger Web Security Academy](https://portswigger.net/web-security) - Tutoriales interactivos

### Certificaciones Recomendadas
- **CompTIA Security+** (Fundamentos)
- **CEH (Certified Ethical Hacker)** (Pentesting)
- **CISSP** (Gestión de seguridad)
- **OSCP** (Pentesting avanzado)
- **AWS/Azure Security Specialty** (Cloud)

---

## 🤝 CONTRIBUCIONES

Este curso es un material educativo en constante evolución. Se aceptan:
- Correcciones de errores
- Nuevos ejemplos prácticos
- Traducciones
- Mejoras en diagramas
- Casos de estudio locales (Uruguay)

---

## ⚖️ NOTA LEGAL Y ÉTICA

**IMPORTANTE:** Todo el contenido de este curso debe usarse exclusivamente con fines educativos y en entornos controlados (laboratorios propios, máquinas virtuales, plataformas autorizadas).

**Está PROHIBIDO:**
- Realizar ataques a sistemas sin autorización explícita
- Usar las técnicas aprendidas para actividades ilegales
- Acceder a datos personales sin consentimiento
- Distribuir malware o herramientas de ataque

**Recuerda:** La ciberseguridad ética implica:
- Obtener permisos por escrito antes de cualquier prueba
- Respetar la privacidad y confidencialidad
- Reportar vulnerabilidades de forma responsable
- Cumplir con las leyes locales e internacionales

---

## 📞 SOPORTE Y COMUNIDAD

Para dudas, consultas o reportar errores:
- Crear issue en el repositorio
- Contactar al instructor
- Unirse a comunidades de ciberseguridad en Uruguay:
  - OWASP Uruguay Chapter
  - CERTuy
  - Meetups de seguridad informática

---

## 🏆 RECONOCIMIENTOS

Este curso fue desarrollado con aportes de:
- Comunidad OWASP
- CERTuy (AGESIC)
- Experiencias de profesionales de la industria
- Feedback de estudiantes de tecnólogo en ciberseguridad

---

**Versión:** 1.0  
**Última actualización:** 2024  
**Licencia:** Creative Commons BY-NC-SA 4.0  

---

## 🚀 ¡COMIENZA TU VIAJE EN CIBERSEGURIDAD!

La seguridad informática no es solo una carrera, es una responsabilidad. Cada línea de código que escribas, cada sistema que configures, puede proteger o exponer a miles de personas.

**"Con gran poder viene gran responsabilidad"** - Úsalo sabiamente.

¡Éxitos en tu aprendizaje! 🔐

