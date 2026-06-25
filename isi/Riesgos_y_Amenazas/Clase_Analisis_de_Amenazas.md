# Clase: Análisis de Amenazas de Ciberseguridad

## Introducción

El análisis de amenazas es el proceso de identificar, comprender y caracterizar los agentes amenazantes, sus motivaciones, capacidades y métodos de ataque. A diferencia del análisis de riesgos (que evalúa probabilidad e impacto), el análisis de amenazas se centra específicamente en el adversario: quién quiere hacerle daño a la organización y cómo podría hacerlo.

**Objetivos de aprendizaje:**
1. Comprender la diferencia entre amenaza, vulnerabilidad y riesgo
2. Identificar y categorizar actores de amenazas
3. Analizar motivaciones y capacidades de atacantes
4. Estudiar patrones de ataque comunes
5. Aplicar inteligencia de amenazas (Threat Intelligence)
6. Construir perfiles de amenazas para la organización

---

## 1. Conceptos Fundamentales

### 1.1 Diferenciación clave

| Concepto | Definición | Ejemplo |
|----------|------------|---------|
| **Amenaza** | Actor, evento o circunstancia que puede causar daño | Ransomware, empleado insatisfecho, tormenta |
| **Vulnerabilidad** | Debilidad que puede ser explotada | Software sin parches, contraseña débil |
| **Riesgo** | Probabilidad de que una amenaza aproveche una vulnerabilidad | "Alta probabilidad de breach por ransomware" |
| **Impacto** | Consecuencia si se materializa el riesgo | Pérdida de datos, interrupción de servicios |

```
        Amenaza ──explotación──▶ Vulnerabilidad
                                         │
                                         ▼
                                      Riesgo
                                         │
                                         ▼
                                      Impacto
```

### 1.2 Tipos de amenazas

**Por intención:**
- **Amenazas intencionales:** Ataques deliberados con propósito específico
- **Amenazas accidentales:** Errores, negligencia, desastres naturales

**Por origen:**
- **Amenazas internas:** Empleados, contratistas, socios de negocio
- **Amenazas externas:** Hackers, cibercriminales, estados-nación, competidores

**Por motivación:**
- **Económicas:** Cibercriminales, fraude
- **Espionaje:** Competidores, estados-nación
- **Ideológicas:** Hacktivistas, terroristas
- **Personales:** Venganza, prestigio

### 1.3 El ciclo de vida del ataque (Kill Chain)

Desarrollado por Lockheed Martin, describe las fases de un ataque:

```
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│RECON    │───▶│WEAPONIZE│───▶│DELIVER  │───▶│EXPLOIT  │───▶│INSTALL  │
│Reconocim│    │Crear    │    │Transmit │    │Ejecutar │    │Establecer│
│         │    │payload  │    │arma     │    │código   │    │persistencia│
└─────────┘    └─────────┘    └─────────┘    └─────────┘    └─────────┘
                                                                │
                                                                ▼
┌─────────┐    ┌─────────┐    ┌─────────┐              ┌─────────┐
│ACTIONS  │◀───│COMMAND  │◀───│CONTROL  │◀───────────── │EXFIL    │
│Objetivos│    │Controlar│    │Canal de │              │Exfiltrar│
│alcanzad.│    │sistema  │    │comandos │              │datos    │
└─────────┘    └─────────┘    └─────────┘              └─────────┘
```

**Defensas por fase:**
| Fase | Detección | Prevención |
|------|-----------|------------|
| Reconocimiento | SIEM, monitoreo DNS | LIMITAR información pública |
| Weaponize | Sandbox de email | WAF, validación de inputs |
| Delivery | Filtros de correo, gateway | SEGURIDAD del email |
| Exploitation | EDR, HIDS | PARCHES, hardening |
| Installation | EDR, análisis de comportamiento | WHITELISTING de aplicaciones |
| Command & Control | IDS/IPS, monitoreo de red | SEGMENTACIÓN, DNS filtering |
| Actions on Objectives | DLP, UEBA | MONITOREO de datos |

---

## 2. Actores de Amenazas

### 2.1 Taxonomía de actores

| Actor | Descripción | Amenaza para bancos |
|-------|-------------|--------------------|
| **Script Kiddies** | Atacantes novatos usando herramientas prefabricadas | Baja, ataques oportunistas |
| **Cibercriminales** | Organizaciones motivadas por lucro | Alta, fraude y ransomware |
| **Hacktivistas** | Activistas con motivaciones ideológicas | Media, desfiguración y doxing |
| **Estados-nación (APT)** | Grupos respaldados por gobiernos | Muy alta, espionaje |
| **Insiders** | Empleados o exempleados con acceso | Alta, robar o sabotear |
| **Terroristas** | Motivados por causar miedo | Media, propaganda |
| **Competidores** | Empresas que buscan ventaja desleal | Media, espionaje industrial |

### 2.2 Perfiles detallados de actores

#### 2.2.1 Cibercriminales (APT-C2)

**Perfil típico:**
- Estructura organizada con roles especializados
- Operaciones motivadas por beneficio económico
- Uso de malware comercial y custom
- Orientados a fraude financiero, ransomware, cryptojacking

**Indicadores de actividad:**
```
TTPs observados:
- spearfishing con payloads maliciosos
- uso de herramientas legítimas (LOLBAS)
- movimiento lateral con Cobalt Strike
- exfiltración vía C2 modificado
```

**Ejemplos知名的:**
- FIN7/Carbanak: Especializada en retail y restaurantes, adaptada a banca
- TA505: ransomware as a service, herramientas modulares
- Wizard Spider: Conti/Trickbot, enfoque en hospitales y banca

#### 2.2.2 Estados-nación (APT)

**Perfil típico:**
- Recursos ilimitados, paciencia operativa
- Objetivos: espionaje, sabotage, destrucción
- Herramientas sofisticadas, zero-days propios
- Persistencia profunda, difícil de detectar

**Grupos conocidos:**
| Grupo | País atribuido | Objetivo | Banca? |
|-------|---------------|----------|--------|
| APT41 | China | Espionaje, cybercrime | Sí |
| Lazarus | Corea del Norte | Finanzas, destabilización | Sí |
| Sandworm | Rusia | Destrucción, infraestructura crítica | Sí |
| Cozy Bear | Rusia | Espionaje gubernamental | Indirecto |
| Fancy Bear | Rusia | Militar, política | Indirecto |

#### 2.2.3 Insiders

**Tipos de insiders maliciosos:**

| Tipo | Perfil | Señales de alerta |
|------|--------|-------------------|
| **Vengativo** | Empleado satisfecho, recientes cambios | Acceso fuera de horario, búsqueda de datos sensibles |
| **Financieramente motivado** | Deudas, estilo de vida | Transferencias inusual, intentos de elevación |
| **Espía corporativo** | Nuevos empleados, consultoría | Acceso a proyectos sensibles, contacto con competidores |
| **Activista** | Ideología marcada | Acceso a información sensible, filtración |

---

## 3. Análisis de Motivaciones

### 3.1 Matriz motivaciones vs. objetivos

| Motivación | Objetivo primario | Objetivos secundarios | Métodos típicos |
|------------|------------------|----------------------|-----------------|
| **Dinero** | Robo directo, fraude | Ransomware, cryptojacking | Phishing, malware financiero |
| **Espionaje** | Información valiosa | Acceso sostenido | APT, watering hole |
| **Sabotaje** | Dañar operaciones | Destrucción de datos | Ransomware destructivo, wiper |
| **Hacktivismo** | Difundir mensaje | Causar vergüenza | DDoS, doxing, defacement |
| **Venganza** | Dañar a la organización | Satisfacción personal | Sabotaje, filtración |
| **Prestigio** | Fama, reputación | Probar habilidades | Desafíos públicos, leak |

### 3.2 Perfil de amenaza por sector

**Para el sector bancario uruguayo:**

| Actor | Relevancia | Probabilidad | Impacto potencial |
|-------|------------|--------------|-------------------|
| Cibercriminales (LATAM) | Muy alta | Alta | Alto |
| Ransomware operators | Alta | Alta | Muy alto |
| APT financiada por estados | Media | Baja | Crítico |
| Insiders | Alta | Media | Alto |
| Hacktivistas locales | Baja | Baja | Bajo |
| Competidores locales | Media | Media | Medio |

---

## 4. Metodologías de Análisis de Amenazas

### 4.1 Fuentes de inteligencia de amenazas

**Fuentes abiertas (OSINT):**
| Fuente | Contenido |
|--------|----------|
| MITRE ATT&CK | Base de conocimientos de TTPs |
| CISA Alerts | Alertas de vulnerabilidades y amenazas |
| ISACs sectoriales | Inteligencia específica por industria |
| Shodan/Censys | Dispositivos expuestos en internet |
| VirusTotal | hashes, URLs, IPs maliciosas |
| AbuseIPDB | IPs reportadas por abuse |
| Twitter/X #ThreatIntel | Inteligencia en tiempo real |
| Blogs de seguridad | Análisis de investigadores |

**Fuentes comerciales:**
- Feeds de threat intelligence (Recorded Future, Mandiant, CrowdStrike)
- Suscripciones a ISAC financieras
- Reportes de vendors de seguridad
- Información compartida por peers (ISACs)

### 4.2 Framework de análisis

**Metodología de 5 pasos:**

```
┌────────────────────────────────────────────────────────────┐
│                 ANÁLISIS DE AMENAZAS                       │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  1. IDENTIFICAR ──▶ 2. CARACTERIZAR ──▶ 3. EVALUAR        │
│     ¿Quién nos amenaza?     ¿Cómo operan?      ¿Qué riesgo?│
│                                                            │
│  4. PRIORIZAR ───▶ 5. MONITOREAR                          │
│     ¿Dónde actuar?        ¿Cambió algo?                    │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### 4.3 Análisis de indicadores de amenaza (IOCs)

**Tipos de IOCs:**

| Tipo | Ejemplo | Uso en detección |
|------|---------|-----------------|
| **IP address** | 192.168.1.100 | Firewall, SIEM |
| **Domain** | malicioso.com | DNS filtering, proxy |
| **Hash de archivo** | SHA256:abc123... | Antivirus, EDR |
| **URL** | hxxp://mal[.]com/payload.exe | Gateway web |
| **Mutex** | Global\MalwareMutex | Análisis de memoria |
| **Patters de comportamiento** | PowerShell obfuscado | EDR, анализ поведения |

---

## 5. Threat Modeling para la Organización

### 5.1 Preguntas clave para threat modeling

1. **¿Qué estamos protegiendo?** → Inventario de activos críticos
2. **¿Contra quién nos protegemos?** → Perfil de actores de amenaza
3. **¿Cómo podrían atacarnos?** → Vectores de ataque probables
4. **¿Qué pasa si nos atacan?** → Análisis de impacto
5. **¿Cómo lo sabemos si nos atacan?** → Capacidades de detección

### 5.2 Diagrama de flujo de datos (DFD)

```
┌─────────────┐                    ┌─────────────┐
│   USUARIO   │                    │  ENTORNO    │
│  EXTERNO    │                    │   EXTERNO   │
└──────┬──────┘                    └──────┬──────┘
       │                                 │
       │    ┌─────────────────────┐      │
       └────┤     INTERNET        ├──────┘
            │  (DMZ - Firewall)   │
            └──────────┬──────────┘
                       │
       ┌───────────────┼───────────────┐
       │               │               │
       ▼               ▼               ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│ SERVIDOR    │ │ SERVIDOR    │ │ SERVIDOR    │
│ WEB         │ │ APLICACIONES│ │ API         │
└──────┬──────┘ └──────┬──────┘ └──────┬──────┘
       │               │               │
       │    ┌──────────┴──────────┐   │
       │    │    RED INTERNA      │   │
       │    │  (Segmentos VLAN)   │   │
       │    └──────────┬──────────┘   │
       │               │               │
       │    ┌──────────┴──────────┐    │
       │    │   BASE DE DATOS    │    │
       │    │   (Datos críticos) │    │
       │    └────────────────────┘    │
       └─────────────────────────────┘
```

### 5.3 Vectores de ataque relevantes para banca

| Vector | Descripción | Probabilidad | Controles |
|--------|-------------|--------------|-----------|
| Phishing/Spear phishing | Correos dirigidos a empleados | Muy alta | MFA, capacitación, filtro |
| Credenciales robadas | Brute force, credential stuffing | Alta | MFA, lockout, monitoring |
| Vulnerabilidades web | SQLi, XSS, SSRF | Alta | WAF, SDLC seguro |
| Cadena de suministro | Software de terceros comprometido | Media | Evaluación, firmas verific |
| Movimiento lateral | desde endpoints comprometidos | Alta | Segmentación, EDR |
| Explotación de VPN | Vulnerabilidades en acceso remoto | Alta | Parches, MFA, monitoring |
| Ataques a API | Abuso de APIs expuestas | Alta | Rate limiting, auth |
| Ingenieria social | Llamadas, pretextos | Alta | Capacitación, verificación |

---

## 6. Técnicas, Tácticas y Procedimientos (TTPs)

### 6.1 Mapeo a MITRE ATT&CK

**Tácticas (fases del ataque):**

| Táctica | Descripción | Ejemplos |
|---------|-------------|----------|
| **Reconnaissance** | Recopilar información | OSINT, escaneo, phishing |
| **Resource Development** | Preparar recursos | Comprar malware, crear infraestructura |
| **Initial Access** | Entrar a la red | Phishing, exploit, credenciales |
| **Execution** | Ejecutar código | Malicioso, legítimo |
| **Persistence** | Mantener acceso | Backdoors, cuentas nuevas |
| **Privilege Escalation** | Elevar privilegios | Exploits, configuraciones |
| **Defense Evasion** | Evitar detección | Ofuscación, deshabilitar controles |
| **Credential Access** | Robar credenciales | Keylogging, harvesting |
| **Discovery** | Explorar la red | Enumeración, reconocimiento |
| **Lateral Movement** | Moverse por la red | Pass-the-hash, RDP |
| **Collection** | Recopilar datos | Captura de pantalla, archivos |
| **Command and Control** | Comunicar con C2 | DNS Tunneling, HTTPS |
| **Exfiltration** | Extraer datos | FTP, cloud storage |
| **Impact** | Dañar/destruir | Ransomware, wipers |

### 6.2 TTPs comunes en ataques a instituciones financieras

**Top 10 TTPs observados en banca (resumen):**

1. **T1566 - Phishing** ( Spear phishing targeting executives)
2. **T1078 - Valid Accounts** (Credenciales válidas para acceso)
3. **T1059 - Command and Scripting Interpreter** (PowerShell, cmd)
4. **T1021 - Remote Services** (RDP, SSH, VNC)
5. **T1484 - Domain Trust Modification** (Movement to AD)
6. **T1005 - Data from Local System** (File collection)
7. **T1041 - Exfiltration Over C2 Channel** (C2 exfil)
8. **T1486 - Data Encrypted for Impact** (Ransomware)
9. **T1053 - Scheduled Task/Job** (Persistence)
10. **T1562 - Impair Defenses** (Disable security tools)

---

## 7. Inteligencia de Amenazas Práctica

### 7.1 Fuentes específicas para Uruguay

| Fuente | URL/Contacto | Tipo |
|--------|--------------|------|
| **CERTuy (AGESIC)** | cert@agesic.gub.uy | Nacional, incidentes |
| **Centro Cibernético Policial** | Ministerio del Interior | Policial |
| **Bcu - Supervisión** | Normativa de seguridad | Regulatorio |
| **ASBA** | Asociación de Bancos Privados | Sectorial |
| **FIRST** | feeds FIRST.org | feeds de TF-CSIRT |

### 7.2 Configuración de monitoreo de amenazas

**YARA rules para detección:**

```yara
rule Banking_Trojan_Generic {
    meta:
        description = "Detects common banking trojan patterns"
        author = "Security Team"
        date = "2024-01"
    strings:
        $s1 = "inject.dll" ascii
        $s2 = "hook32.dll" ascii
        $s3 = "keylog" ascii nocase
    condition:
        2 of them
}
```

**Queries de búsqueda en Shodan:**

```
org:"Banco Central"
port:443 ssl:"banking"
vuln:CVE-2024-*
```

### 7.3 Integración con SIEM

**Reglas de correlación sugeridas:**

| Regla | Condición | Severidad |
|-------|-----------|-----------|
| Login anomalous | 5+ intentos fallidos desde diferentes IPs en 10 min | Medium |
| PowerShell suspicious | PowerShell con downloadstring o invoke-expression | High |
| Data exfiltration | > 500MB upload a dominio no whitelisted | Critical |
| Lateral movement | Cuenta de servicio accede a estaciones | High |

---

## 8. Construcción de Perfil de Amenazas

### 8.1 Metodología

```
┌────────────────────────────────────────────────────────────┐
│              CONSTRUCCIÓN DE PERFIL DE AMENAZAS            │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  Paso 1: Inventario de activos críticos                    │
│           → ¿Qué tiene valor para nosotros?                 │
│                                                            │
│  Paso 2: Mapeo de actores relevantes                       │
│           → ¿Quién nos quiere atacar?                      │
│                                                            │
│  Paso 3: Análisis de motivaciones                          │
│           → ¿Por qué nos atacarían?                       │
│                                                            │
│  Paso 4: Identificación de TTPs                            │
│           → ¿Cómo nos atacarían?                          │
│                                                            │
│  Paso 5: Evaluación de capacidades                         │
│           → ¿Tienen la capacidad de hacerlo?               │
│                                                            │
│  Paso 6: Determinación de probabilidad                     │
│           → ¿Qué tan probable es que nos ataquen?          │
│                                                            │
│  Paso 7: Priorización de defensas                          │
│           → ¿Dónde concentrar recursos?                    │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### 8.2 Plantilla de perfil de amenaza

**Perfil: [Nombre del Actor]**

| Campo | Descripción |
|-------|-------------|
| **Nombre del actor** | |
| **Origen/Atribución** | |
| **Motivación principal** | |
| **Motivaciones secundarias** | |
| **Historia de ataques** | |
| **Capacidades técnicas** | Alta / Media / Baja |
| **Recursos** | Alto / Medio / Bajo |
| **Sofisticación** | Alta / Media / Baja |
| **Objetivos típicos** | |
| **Métodos preferidos** | |
| **TTPs conocidos** | |
| **Indicadores de presencia** | |
| **Probabilidad de ataque** | Muy alta / Alta / Media / Baja |
| **Nivel de amenaza** | Crítico / Alto / Medio / Bajo |

---

## 9. Caso de Estudio: Amenaza Ransomware en Banca

### 9.1 Escenario

Una institución bancaria mediana en Uruguay ha identificado que los grupos de ransomware Conti y LockBit tienen historial de ataques al sector financiero LATAM.

### 9.2 Análisis de actor

| Aspecto | Análisis |
|---------|----------|
| **Actor** | LockBit 3.0 (RaaS) |
| **Motivación** | Beneficio económico directo |
| **Capacidad** | Muy alta (herramientas profesionales) |
| **Reputación** | Exige rescates altos, publica datos |
| **Historial LATAM** | Múltiples ataques a empresas mexicanas y brasileñas |

### 9.3 TTPs probables de LockBit

| Fase | TTP esperado | Contramedida |
|------|-------------|-------------|
| Acceso inicial | Phishing, exploit RDP, compras de acceso | MFA, parches, EDR |
| Movimiento lateral | Cobalt Strike, SMB, RDP | Segmentación, monitoring |
| Persistencia | Lööpy, scheduled tasks | Revisión de persistencia |
| Exfiltración | MEGASync, Rclone | DLP, monitoreo de egress |
| Cifrado | BitLocker custom, VSS delete | Backups inmutables, offline |

### 9.4 Plan de acción

| Prioridad | Acción | Responsable | Plazo |
|-----------|--------|-------------|-------|
| 1 | Implementar MFA en todos los accesos privilegiados | Seguridad | 30 días |
| 2 | Configurar backup inmutable (WORM) | Infraestructura | 15 días |
| 3 | Segmentar red kritische systems | Redes | 45 días |
| 4 | Desplegar EDR en todos los endpoints | Seguridad | 30 días |
| 5 | Crear plan de respuesta a ransomware | CISO | 7 días |
| 6 | Simular ataque de ransomware (purple team) | SOC | 60 días |

---

## 10. Taller Práctico

### 10.1 Ejercicio: Crear perfil de amenaza para su organización

**Tarea:** Desarrolle un perfil de amenazas para una empresa del sector X (elige el sector).

**Pasos:**
1. Identificar 3-5 actores de amenaza relevantes
2. Para cada actor, completar:
   - Motivación
   - Capacidad
   - TTPs probables
3. Mapear los TTPs a MITRE ATT&CK
4. Identificar controles actuales para cada TTP
5. Proponer mejoras en controles

### 10.2 Plantilla de entrega

```
EMPRESA: [Nombre虚构 o real]
SECTOR: [Sector]
FECHA: [Fecha]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PERFIL DE AMENAZA #1: [Nombre del actor]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Motivación: 
Capacidad: 
Objetivos:
TTPs probables:
Controles actuales:
Brechas identificadas:
Recomendaciones:

[Repetir para cada actor]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RESUMEN EJECUTIVO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Top 3 amenazas:
Top 3 controles a mejorar:
Recursos necesarios:
```

---

## Resumen

El análisis de amenazas es fundamental para una postura de seguridad efectiva porque permite:

1. **Priorizar** defensas según el perfil real de amenazas
2. **Anticipar** técnicas de ataque antes de que ocurran
3. **Detectar** indicadores específicos de compromiso
4. **Responder** de forma más efectiva conheciendo al adversario
5. **Invertir** recursos donde realmente importan

La amenaza evoluciona constantemente: grupos cambian TTPs, surgen nuevos actores, aparecen nuevas vulnerabilidades. El análisis de amenazas debe ser un proceso continuo, no un ejercicio puntual.

---

**Próxima clase:** STRIDE - Metodología de Microsoft para Modelado de Amenazas

**Material complementario:**
- MITRE ATT&CK Navigator (attack.mitre.org)
- MITRE D3FEND (d3fend.mitre.org)
- Plantilla de Perfil de Amenazas
- Repositorio de IOCs del sector financiero
