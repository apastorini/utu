# CURSO COMPLETO DE CIBERSEGURIDAD - ÍNDICE GENERAL

---

## 📚 ESTRUCTURA DEL CURSO

Este curso está diseñado para llevarte desde cero hasta un nivel profesional en ciberseguridad, con enfoque práctico y ejemplos ejecutables. El contenido está organizado en 4 niveles de dificultad progresiva.

---

## 🗂️ ORGANIZACIÓN DEL CURSO

```
C:\utu\utu\seguridad\
│
├── Nivel1_Fundamentos/         ← Fundamentos teóricos
├── Nivel2_Entorno/             ← Preparación del laboratorio
├── Clases/                     ← Clases prácticas
├── Temas_Complementarios/      ← Temas adicionales
├── Recursos/                    ← Plantillas y recursos
├── Documentos-Uruguay/         ← Normativa uruguaya (Ley 18.331, BCU, AGESIC, NIST)
├── Seguridad_Bancaria/         ← Documentación bancaria (SGSI, incidentes, mapa riesgos)
├── Riesgos_y_Amenazas/         ← Análisis de riesgos y amenazas (STRIDE, DREAD, ATT&CK)
└── 00_INDICE_CURSO.md         ← Este archivo
```

---

## 📖 CONTENIDO POR NIVEL

### NIVEL 1: FUNDAMENTOS

| Archivo | Descripción |
|---------|-------------|
| `semana_1.md` | Fundamentos de seguridad, CIA, tipos de ataques, GDPR |
| `semana_2.md` | Criptografía, hash, certificados, PKI |
| `Firma_Digital.md` | Firma digital completa: RSA, ECDSA, certificados, no-repudio |
| `Diagramas_Visuales.md` | Diagramas pedagógicos de conceptos |

---

### NIVEL 2: ENTORNO DE TRABAJO

| Archivo | Descripción |
|---------|-------------|
| `semana_3_linux_redes.md` | Linux para pentesting, comandos de red, modelo OSI |
| `semana_3_virtualizacion.md` | Virtualización, VirtualBox, Kali Linux, Docker |
| `semana_4_metodologia.md` | Ciclo de hacking, metodología, frameworks |

---

### CLASES PRÁCTICAS (Carpeta `Clases/`)

| Archivo | Descripción | Orden |
|---------|-------------|-------|
| `clase_01_fuerza_bruta.md` | John the Ripper, Rainbow tables, Hydra, Hashcat | 1 |
| `clase_02_metasploitable.md` | Metasploit Framework, exploits, Metasploitable 2/3 | 2 |
| `clase_03_practica_juice.md` | Laboratorio OWASP Juice Shop (práctica completa) | 3 |
| `clase_04_buffer_overflow.md` | Buffer overflow, stack, shellcoding, exploit dev | 4 |
| `clase_05_escalada_privilegios.md` | Escalada Linux/Windows, GTFOBins, Mimikatz | 5 |

---

## 🇺🇾 DOCUMENTACIÓN URUGUAYA

Carpeta: `Documentos-Uruguay/`

| Archivo | Descripción |
|---------|-------------|
| `Clase_Ley_18331.md` | Ley 18.331 - Protección de Datos Personales Uruguay |
| `Clase_Marco_Ciberseguridad_Uruguay.md` | Marco de Ciberseguridad AGESIC Uruguay v5.0 |
| `Clase_NIST_Cybersecurity_Framework.md` | NIST Cybersecurity Framework v2.0 |
| `Clase_BCU_Seguridad_Bancaria.md` | Seguridad Bancaria - Normativa BCU Uruguay |

> **Nota:** Incluye guías de implementación, plantillas, checklists y código Python de ejemplos.

---

## 🏦 SEGURIDAD BANCARIA

Carpeta: `Seguridad_Bancaria/`

| Archivo | Descripción |
|---------|-------------|
| `Plantilla_SGSI.md` | Sistema de Gestión de Seguridad de la Información - Plantilla integral |
| `Mapa_Riesgos_Bancario.md` | Mapa de riesgos de seguridad bancaria, matriz de probabilidad/impacto |
| `Plantilla_Incidentes_Bancarios.md` | Plantilla para gestión de incidentes de seguridad bancaria |

> **Enfoque:** Normativa BCU, gestión de riesgos en instituciones financieras, planes de continuidad bancaria.

---

## 🎯 RIESGOS Y AMENAZAS

Carpeta: `Riesgos_y_Amenazas/`

### Clases de Metodologías

| Archivo | Descripción |
|---------|-------------|
| `Clase_Analisis_de_Riesgos.md` | Metodología completa de análisis de riesgos (ISO 27005, NIST SP 800-30) |
| `Clase_Analisis_de_Amenazas.md` | Taxonomía de amenazas, actores, ciclo de ataque (Kill Chain) |
| `Clase_STRIDE.md` | Metodología Microsoft para modelado de amenazas, DFDs, contramedidas |
| `Clase_DREAD.md` | Sistema de calificación de vulnerabilidades, cálculo de scores |
| `Clase_MITRE_ATTCK.md` | Framework ATT&CK, tácticas, técnicas, Navigator, Purple Team |

### Templates

Carpeta: `Riesgos_y_Amenazas/Templates/`

| Archivo | Descripción |
|---------|-------------|
| `Plantilla_Mapa_Riesgos.md` | Plantilla genérica para mapa de riesgos organizacional |
| `Plantilla_Registro_Amenazas.md` | Registro de amenazas con mapeo a ATT&CK |

> **Metodologías cubiertas:** STRIDE, DREAD, MITRE ATT&CK, ISO 31000, NIST CSF

---

## 📚 TEMAS COMPLEMENTARIOS

Carpeta: `Temas_Complementarios/`

| Archivo | Descripción |
|---------|-------------|
| `Parte2_DevSecOps.md` | Trivy, SonarQube, OWASP ZAP, Jenkins |
| `Parte3_Certificados.md` | Certificados digitales, KeyStore, TrustStore, PKI |
| `Parte4_OWASP_Top10.md` | OWASP Top 10 2021, código vulnerable y seguro |
| `Parte5_APIs.md` | OWASP API Security Top 10, OAuth 2.0 |
| `Parte6_Kubernetes.md` | Seguridad en Kubernetes, RBAC, Network Policies |
| `Parte7_IngenieriaSocial.md` | Phishing, Ingeniería social, Gophish |
| `Parte8_IncidentResponse.md` | Respuesta a incidentes, NIST, forense digital |
| `Parte9_Compliance.md` | ISO 27001, PCI-DSS, SOC 2, GDPR |
| `Parte10_Roles.md` | Roles en ciberseguridad, profesiones |
| `Clase_Seguridad_Nginx_FastAPI.md` | Seguridad en Nginx y FastAPI |

---

## 🛠️ RECURSOS

Carpeta: `Recursos/`

### Plantillas
| Archivo | Descripción |
|---------|-------------|
| `Plantilla_Analisis_Riesgos.md` | Plantilla para análisis de riesgos |
| `Plantilla_Vulnerabilidad_OWASP.md` | Plantilla para documentar vulnerabilidades |
| `Tareas_Analisis_Riesgos.md` | Ejercicios de análisis de riesgos |
| `Tareas_Vulnerabilidades_OWASP.md` | Ejercicios OWASP |
| `Plantilla_Informe_Pentesting.md` | Template profesional de informe de pentesting (NIST SP 800-115) |

### Herramientas y códigos
| Carpeta | Descripción |
|---------|-------------|
| `Clase2_Codigos/` | Códigos de ejemplo de criptografía (AES, RSA) |
| `VirtualBox/` | Recursos de VirtualBox |
| `metasploitable3-workspace/` | Workspace de Metasploitable 3 |
| `material_externo/` | Material adicional |

---

## 🎓 RUTA DE APRENDIZAJE RECOMENDADA

### Nivel 1: Fundamentos (Semanas 1-2)
```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  1. semana_1.md          → Fundamentos de ciberseguridad        │
│     - Tríada CIA                                               │
│     - Tipos de ataques (Phishing, Malware, DDoS, etc.)         │
│     - Privacidad y protección de datos (GDPR, Ley 18.331)      │
│                                                                 │
│  2. semana_2.md          → Criptografía básica                  │
│     - Criptografía simétrica y asimétrica                      │
│     - Funciones hash                                            │
│     - Certificados digitales                                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Nivel 2: Preparación del Entorno (Semanas 3-4)
```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  3. semana_3_linux_redes.md   → Linux y redes para pentesting  │
│     - Comandos de Linux                                               │
│     - Modelo OSI y TCP/IP                                       │
│     - Puertos y servicios                                       │
│     - Nmap básico                                               │
│                                                                 │
│  4. semana_3_virtualizacion.md → Virtualización               │
│     - VirtualBox                                                │
│     - Instalación de Kali Linux                                 │
│     - Docker y contenedores                                    │
│                                                                 │
│  5. semana_4_metodologia.md   → Metodología                   │
│     - Ciclo de hacking (6 fases)                               │
│     - Frameworks de pentesting                                  │
│     - Documentación y reportes                                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Nivel 3: Explotación (Semanas 5-10)
```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  6. clase_01_fuerza_bruta.md    → Ataques de contraseña (1)  │
│     - John the Ripper                                              │
│     - Rainbow tables, Hydra, Hashcat                             │
│                                                                 │
│  7. clase_02_metasploitable.md   → Explotación con Metasploit (2)│
│     - Metasploit Framework                                       │
│     - Metasploitable 2 y 3                                      │
│     - Exploits públicos                                          │
│                                                                 │
│  8. clase_03_practica_juice.md   → Laboratorio OWASP Juice (3)│
│     - OWASP Top 10 práctico                                     │
│     - SQL Injection, XSS, BOLA                                  │
│                                                                 │
│  9. clase_04_buffer_overflow.md  → Buffer Overflow (4)       │
│     - Memoria x86/x64                                           │
│     - Stack overflow, Shellcoding                                │
│     - Bypass protecciones (ASLR, NX, PIE)                       │
│                                                                 │
│  10. clase_05_escalada_privilegios.md → Escalada de privs (5)│
│     - Escalada en Linux (SUID, sudo, kernel exploits)           │
│     - Escalada en Windows (servicios, DLL hijacking)            │
│     - Pass-the-Hash, GTFOBins, LOLBAS                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Nivel 4: Explotación Avanzada (Semanas 9-12)
```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  9. clase_06_buffer_overflow.md  → Buffer Overflow            │
│     - Memoria x86/x64                                           │
│     - Stack overflow                                            │
│     - Shellcoding                                               │
│     - Bypass de protecciones (ASLR, NX, PIE)                    │
│                                                                 │
│  10. clase_07_escalada_privilegios.md → Escalada de privilegios│
│     - Escalada en Linux (SUID, sudo, kernel exploits)           │
│     - Escalada en Windows (servicios, DLL hijacking)            │
│     - Pass-the-Hash                                             │
│     - GTFOBins, LOLBAS                                           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📊 ESTADÍSTICAS DEL CURSO

| Métrica | Valor |
|---------|-------|
| **Niveles** | 4 completos |
| **Clases prácticas** | 5 (clase_01 a clase_05) |
| **Clases de metodología** | 5 (Riesgos, Amenazas, STRIDE, DREAD, ATT&CK) |
| **Documentación uruguaya** | 4 (Ley 18.331, AGESIC, NIST, BCU) |
| **Documentación bancaria** | 3 (SGSI, Mapa Riesgos, Incidentes) |
| **Plantillas** | 4+ |
| **Temas complementarios** | 9 |
| **Ejemplos de código** | 200+ |
| **Herramientas** | 40+ |
| **Laboratorios** | 10+ |
| **Tiempo estimado** | 12-16 semanas |

---

## 🛠️ REQUISITOS TÉCNICOS

### Software Necesario

```bash
# Sistema Operativo
- Linux (Ubuntu 22.04 recomendado)
- Windows 10/11 con WSL2
- macOS

# Virtualización
- VirtualBox 7.0+
- Docker y Docker Compose

# Herramientas de Pentesting
- Kali Linux 2024+
- Metasploitable 2 y 3
- OWASP Juice Shop

# Editores y lenguajes
- VS Code
- Python 3.8+
- Java 11+
```

---

## 📚 BIBLIOGRAFÍA COMPLEMENTARIA

### Libros
1. **W. Stallings, L. Brown** - "Computer Security: Principles and Practice"
2. **OWASP** - "OWASP Testing Guide v4.2"
3. **Jon Erickson** - "Hacking: The Art of Exploitation"
4. **Georgia Weidman** - "Penetration Testing"

### Plataformas de Práctica
- [HackTheBox](https://www.hackthebox.com)
- [TryHackMe](https://tryhackme.com)
- [PortSwigger Academy](https://portswigger.net/web-security)
- [VulnHub](https://www.vulnhub.com)

### Certificaciones
- **CompTIA Security+** - Fundamentos
- **CEH** - Hacking ético
- **OSCP** - Pentesting avanzado
- **CISSP** - Gestión de seguridad

---

## ⚖️ NOTA LEGAL Y ÉTICA

**IMPORTANTE:** Todo el contenido de este curso debe usarse exclusivamente con fines educativos y en entornos controlados.

**Está PROHIBIDO:**
- Realizar ataques a sistemas sin autorización explícita
- Usar técnicas para actividades ilegales
- Acceder a datos personales sin consentimiento

**Recuerda:** La ciberseguridad ética implica obtener permisos por escrito antes de cualquier prueba.

---

## 📞 RECURSOS ADICIONALES

- [OWASP.org](https://owasp.org) - Proyectos y documentación
- [CERTuy](https://www.gub.uy/centro-nacional-respuesta-incidentes-seguridad-informatica/) - Uruguay
- [HackTricks](https://book.hacktricks.xyz/) - Técnicas de pentesting
- [GTFOBins](https://gtfobins.github.io/) - Binarios Unix explotables
- [LOLBAS](https://lolbas-project.github.io/) - Binarios Windows explotables

---

**Versión:** 4.0  
**Última actualización:** 16/04/2026  
**Licencia:** Creative Commons BY-NC-SA 4.0
