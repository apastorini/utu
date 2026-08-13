# Informe de Pentesting - Tarea 2: Red Team

## Taller de Ciberseguridad Orientada al Desarrollo

---

## 1. Portada

| | |
|---|---|
| **Curso** | Taller de Ciberseguridad Orientada al Desarrollo |
| **Tarea** | Tarea 2 - Red Team (Pentesting entre grupos) |
| **Titulo del informe** | Informe de Pruebas de Penetracion |
| **Grupo atacante** | [Completar: Grupo X] |
| **Grupo objetivo** | [Completar: Grupo Y] |
| **Aplicacion analizada** | [Completar: Nombre/URL de la aplicacion] |
| **Fecha de inicio** | [Completar: Clase 39 - Fecha] |
| **Fecha de entrega** | [Completar: Clase 42 - Fecha] |
| **Integrantes** | [Nombre 1], [Nombre 2], [Nombre 3], [Nombre 4] |
| **Profesor** | [Completar nombre] |
| **Version del informe** | 1.0 |

---

## 2. Resumen Ejecutivo

### 2.1. Sintesis del proyecto

Se realizo una evaluacion de seguridad sobre la aplicacion web desarrollada por el [Grupo Y] como parte de la Tarea 1 (Shift Left). Esta evaluacion consistio en un pentesting externo de caja negra parcial, donde se aplicaron tecnicas de reconocimiento, escaneo automatizado, pruebas manuales basadas en OWASP Top 10, explotacion controlada de vulnerabilidades y ataques al sistema operativo subyacente (VM o contenedor Docker).

### 2.2. Hallazgos principales

Durante el periodo de pruebas comprendido entre [Fecha inicio] y [Fecha fin], se identificaron un total de [N] vulnerabilidades distribuidas en las siguientes severidades:

| Severidad | Cantidad |
|-----------|----------|
| Critical | [N] |
| High | [N] |
| Medium | [N] |
| Low | [N] |
| Info | [N] |
| **Total** | **[N]** |

### 2.3. Riesgo general

La aplicacion presenta un nivel de riesgo [Alto / Medio / Bajo]. Se detectaron [N] vulnerabilidades de severidad Critical/High que permiten [describir brevemente el peor impacto posible, ej: acceso no autorizado a la base de datos, ejecucion remota de comandos, suplantacion de usuarios, compromiso del sistema operativo].

### 2.4. Recomendaciones inmediatas

1. Implementar consultas parametrizadas en todos los endpoints con interaccion a base de datos.
2. Reforzar la autenticacion y gestion de sesiones (JWT seguro, rate limiting, password policies).
3. Configurar headers de seguridad HTTP faltantes.
4. Validar y sanitizar toda entrada de usuario en el servidor.
5. Corregir controles de acceso horizontal y vertical (IDOR, Privilege Escalation).
6. Deshabilitar servicios innecesarios expuestos (SSH, FTP, paneles administrativos).
7. Proteger archivos de configuracion con secretos (variables de entorno, .env).

---

## 3. Alcance y Metodologia

### 3.1. Alcance del pentesting

| Item | Descripcion |
|------|-------------|
| **Tipo de prueba** | Pentesting externo de caja negra parcial |
| **URL objetivo** | [Completar URL] |
| **Direccion IP** | [Completar IP] |
| **Puertos** | 80 (HTTP), 443 (HTTPS), [otros identificados] |
| **Tecnologias conocidas** | [Completar: Node.js, Express, MySQL, React, etc.] |
| **Usuario de prueba** | [Completar si se proporcionaron credenciales] |
| **Sistema operativo objetivo** | VM o contenedor Docker del grupo objetivo |
| **Ataques a la API** | Inyeccion SQL, Broken Authentication, IDOR, XSS, Security Misconfiguration, Rate limiting bypass |
| **Ataques al SO/Infraestructura** | Escaneo de puertos, fuerza bruta SSH, FTP anonymous, escalacion de privilegios, container escape, exploracion de BD expuesta, busqueda de secretos |
| **Restricciones** | Ver seccion 3.5 - Reglas de Enfrentamiento |

### 3.2. Metodologia aplicada

La evaluacion siguio el estandar PTES (Penetration Testing Execution Standard) con las siguientes fases:

1. **Reconocimiento (Recon)**: Identificacion de tecnologias, endpoints, puertos y servicios. Escaneo de puertos del host con nmap.
2. **Escaneo automatizado**: Ejecucion de herramientas OWASP ZAP, Nikto, SQLMap, hydra/medusa para fuerza bruta.
3. **Pruebas manuales**: Evaluacion de vulnerabilidades OWASP Top 10 (6+ categorias) y ataques al sistema operativo.
4. **Explotacion**: Desarrollo de PoCs funcionales para cada vulnerabilidad, incluyendo escalacion de privilegios y container escape si aplica.
5. **Documentacion**: Redaccion de hallazgos con CVSS, impacto y mitigaciones.

### 3.3. Herramientas utilizadas

| Herramienta | Version | Proposito |
|-------------|---------|-----------|
| OWASP ZAP | [version] | Escaneo automatizado de vulnerabilidades web |
| Nikto | [version] | Escaneo de servidor web y archivos sensibles |
| SQLMap | [version] | Deteccion y explotacion de inyecciones SQL |
| Nmap | [version] | Escaneo de puertos y servicios |
| Wappalyzer | [version] | Identificacion de tecnologias web |
| WhatWeb | [version] | Fingerprinting de tecnologias web |
| Burp Suite | [version] | Proxy de interceptacion y pruebas manuales |
| curl / wget | [version] | Pruebas HTTP manuales |
| Python 3 | [version] | Desarrollo de scripts de explotacion |
| JWT Tool | [version] | Analisis de tokens JWT |
| Hashcat / John | [version] | Crackeo de hashes (si aplica) |
| Hydra / Medusa | [version] | Fuerza bruta a servicios SSH, FTP, HTTP |
| Gobuster / Dirb | [version] | Fuzzing de directorios y archivos |
| Netcat / nc | [version] | Conexiones manuales a servicios |
| LinPEAS / WinPEAS | [version] | Escalacion de privilegios en Linux/Windows |
| Docker CLI | [version] | Exploracion de contenedores Docker |

### 3.4. Criterios de severidad (CVSS v3.1)

| Rango CVSS | Severidad | Color |
|------------|-----------|-------|
| 9.0 - 10.0 | Critical | Rojo |
| 7.0 - 8.9 | High | Naranja |
| 4.0 - 6.9 | Medium | Amarillo |
| 0.1 - 3.9 | Low | Verde |
| 0.0 | Informational | Azul |

### 3.5. Etica y Reglas de Enfrentamiento (Rules of Engagement)

#### 3.5.1. Horarios de ataque permitidos

Los ataques solo se realizaran durante el horario de clase y en los periodos acordados con el profesor. No se realizaran pruebas fuera de los horarios establecidos ni fuera de las fechas asignadas.

#### 3.5.2. Prohibiciones

- No realizar ataques de Denegacion de Servicio (DoS/DDoS).
- No modificar, eliminar o corromper datos en la aplicacion objetivo.
- No acceder, copiar ni divulgar datos personales de otros estudiantes.
- No instalar backdoors permanentes ni modificar configuraciones del sistema.
- No realizar ataques fuera del alcance definido (solo al sistema del grupo objetivo).

#### 3.5.3. Reglas de interaccion

- El grupo atacante (Red Team) solo interactua con el sistema del grupo objetivo asignado.
- El grupo defensor (Blue Team) no puede modificar la aplicacion ni su infraestructura durante el periodo de ataque.
- Si el Red Team compromete el sistema (obtiene acceso shell, extrae datos, etc.), debe documentar la prueba como PoC y notificar inmediatamente al profesor.
- Toda actividad debe ser registrada y reproducible para fines academicos.

#### 3.5.4. Consecuencias de incumplimiento

El incumplimiento de estas reglas resultara en la descalificacion de la tarea y podra ser informado a las autoridades academicas correspondientes.

---

## 4. Fase 1: Reconocimiento (Recon)

### 4.1. Identificacion de tecnologias

#### Wappalyzer

Se utilizo la extension Wappalyzer y la herramienta WhatWeb para identificar las tecnologias presentes en la aplicacion objetivo.

```bash
whatweb [URL_OBJETIVO]
```

**Resultados:**

| Tecnologia | Version | Categoria |
|------------|---------|-----------|
| [Framework] | [vX.X] | Backend |
| [Base de datos] | [vX.X] | Base de datos |
| [Frontend] | [vX.X] | Frontend |
| [Servidor web] | [vX.X] | Servidor |
| [Lenguaje] | [vX.X] | Lenguaje |
| [Otros] | [vX.X] | - |

#### curl - Analisis de headers HTTP

```bash
curl -I -v [URL_OBJETIVO]
```

**Headers obtenidos:**

```
HTTP/1.1 200 OK
[header 1]
[header 2]
...
```

**Observaciones:**
- Headers de seguridad presentes: [X-Content-Type-Options, X-Frame-Options, CSP, etc.]
- Headers de seguridad ausentes: [listar faltantes]
- Informacion de version expuesta en headers: [Si/No, detalles]

### 4.2. Escaneo de puertos y servicios (Nmap)

```bash
nmap -sV -sC -p- -T4 [IP_OBJETIVO]
```

**Resultados:**

| Puerto | Estado | Servicio | Version | Notas |
|--------|--------|----------|---------|-------|
| 80/tcp | open | HTTP | [version] | Servidor web sin SSL |
| 443/tcp | open | HTTPS | [version] | Servidor web con SSL |
| 22/tcp | open | SSH | [version] | Acceso SSH (posible ataque de fuerza bruta) |
| 21/tcp | open | FTP | [version] | FTP (posible anonymous access) |
| 3306/tcp | open | MySQL | [version] | Base de datos expuesta |
| 2375/tcp | open | Docker API | [version] | Docker API sin autenticar (container escape) |
| [N]/tcp | open | [servicio] | [version] | [notas] |

### 4.3. Mapeo de endpoints

Se realizo un mapeo manual y automatizado de endpoints de la aplicacion.

```bash
# Crawling basico con curl
curl -s [URL_OBJETIVO]/robots.txt
curl -s [URL_OBJETIVO]/sitemap.xml
```

**robots.txt:**

```
[Contenido del robots.txt si existe]
```

**Sitemap:**

```
[Contenido del sitemap si existe]
```

**Endpoints identificados:**

| Metodo | Endpoint | Parametros | Autenticacion | Descripcion |
|--------|----------|------------|---------------|-------------|
| GET | / | - | No | Pagina principal |
| GET | /api/[recurso] | ?param= | Si/No | Descripcion |
| POST | /api/[recurso] | body JSON | Si | Creacion de recurso |
| PUT | /api/[recurso]/:id | body JSON | Si | Actualizacion |
| DELETE | /api/[recurso]/:id | - | Si | Eliminacion |
| ... | ... | ... | ... | ... |

### 4.4. Analisis de cookies y sesion

```bash
curl -c cookies.txt -b cookies.txt -v [URL_OBJETIVO]/login -d "username=test&password=test"
```

**Observaciones sobre cookies/tokens:**

| Cookie/Token | Atributos | Observaciones |
|-------------|-----------|---------------|
| [Nombre] | HttpOnly, Secure, SameSite | [analisis] |
| JWT | [algoritmo] | [payload analizado] |

---

## 5. Fase 2: Escaneo Automatizado

### 5.1. OWASP ZAP - Full Scan

**Comando ejecutado:**

```
[Completar con el comando o configuracion de ZAP utilizada]
```

**Resumen de alertas:**

| Nivel de riesgo | Cantidad de alertas |
|-----------------|---------------------|
| High | [N] |
| Medium | [N] |
| Low | [N] |
| Informational | [N] |

**Alertas principales:**

| Alerta | URL | Riesgo | Descripcion breve |
|--------|-----|--------|-------------------|
| [Nombre alerta] | [URL] | High/Medium | [Descripcion] |
| [Nombre alerta] | [URL] | High/Medium | [Descripcion] |
| [Nombre alerta] | [URL] | High/Medium | [Descripcion] |

### 5.2. Nikto

```bash
nikto -h [URL_OBJETIVO]
```

**Resultados:**

```
[Salida relevante de Nikto]
```

**Hallazgos principales de Nikto:**

| Item | Descripcion |
|------|-------------|
| [Id hallazgo] | [Descripcion] |
| [Id hallazgo] | [Descripcion] |

### 5.3. SQLMap

```bash
sqlmap -u "[URL_OBJETIVO]/api/endpoint?param=valor" --batch --level=3 --risk=2
```

**Resultados:**

| Parametro | Tecnica | Inyectable | Tipo de DB | Payload |
|-----------|---------|------------|------------|---------|
| [param] | [Error/Boolean/Time/Union] | Si/No | [MySQL/PostgreSQL/etc.] | [payload] |
| [param] | [Error/Boolean/Time/Union] | Si/No | [MySQL/PostgreSQL/etc.] | [payload] |

**Datos extraidos (si aplica):**

```
[Tablas, columnas o datos obtenidos durante la prueba controlada]
```

---

## 6. Fase 3: Pruebas Manuales (OWASP Top 10)

---

### Hallazgo 1: [Titulo de la vulnerabilidad]

- **ID**: OWASP [codigo] - [Nombre]; CWE-[numero]
- **Severidad**: [CRITICAL / HIGH / MEDIUM / LOW] (CVSS: [X.X])
- **Endpoint**: [Metodo] [URL/endpoint]
- **Categoria OWASP**: [Categoria correspondiente]

#### Descripcion

[Descripcion detallada de la vulnerabilidad: como se manifiesta, que componente esta afectado, que causa raiz la genera]

#### PoC (Proof of Concept)

**Paso 1:** [Descripcion del paso]

```bash
[Comando exacto utilizado]
```

**Paso 2:** [Descripcion del paso]

```
[Request HTTP raw si aplica]
```

**Paso 3:** [Descripcion del paso]

```
[Respuesta obtenida]
```

**Script de explotacion (si aplica):**

```python
# [nombre_script].py
# Descripcion: [que hace este script]
# Uso: python [script].py [argumentos]

import requests
import sys

def exploit(url, payload):
    # [Codigo del PoC]
    pass

if __name__ == "__main__":
    # [Ejemplo de uso]
    pass
```

#### Impacto

- **Confidencialidad**: [Alto/Medio/Bajo - descripcion]
- **Integridad**: [Alto/Medio/Bajo - descripcion]
- **Disponibilidad**: [Alto/Medio/Bajo - descripcion]
- **Impacto en el negocio**: [Que puede lograr un atacante]

#### Mitigacion

**Solucion recomendada:**

```[lenguaje]
[Codigo o configuracion especifica para mitigar la vulnerabilidad]
```

**Acciones adicionales:**
- [Accion correctiva 1]
- [Accion correctiva 2]

---

### Hallazgo 2: [Titulo de la vulnerabilidad]

- **ID**: OWASP [codigo] - [Nombre]; CWE-[numero]
- **Severidad**: [CRITICAL / HIGH / MEDIUM / LOW] (CVSS: [X.X])
- **Endpoint**: [Metodo] [URL/endpoint]

#### Descripcion

[Descripcion detallada]

#### PoC

```bash
[Comando exacto]
```

```
[Request/Response]
```

#### Impacto

[Descripcion del impacto]

#### Mitigacion

```[lenguaje]
[Codigo de mitigacion]
```

---

### Hallazgo 3: [Titulo de la vulnerabilidad]

- **ID**: OWASP [codigo] - [Nombre]; CWE-[numero]
- **Severidad**: [CRITICAL / HIGH / MEDIUM / LOW] (CVSS: [X.X])
- **Endpoint**: [Metodo] [URL/endpoint]

#### Descripcion

[Descripcion detallada]

#### PoC

```bash
[Comando exacto]
```

```
[Request/Response]
```

#### Impacto

[Descripcion del impacto]

#### Mitigacion

```[lenguaje]
[Codigo de mitigacion]
```

---

### Hallazgo 4: [Titulo de la vulnerabilidad]

- **ID**: OWASP [codigo] - [Nombre]; CWE-[numero]
- **Severidad**: [CRITICAL / HIGH / MEDIUM / LOW] (CVSS: [X.X])
- **Endpoint**: [Metodo] [URL/endpoint]

#### Descripcion

[Descripcion detallada]

#### PoC

```bash
[Comando exacto]
```

```
[Request/Response]
```

#### Impacto

[Descripcion del impacto]

#### Mitigacion

```[lenguaje]
[Codigo de mitigacion]
```

---

### Hallazgo 5: [Titulo de la vulnerabilidad]

- **ID**: OWASP [codigo] - [Nombre]; CWE-[numero]
- **Severidad**: [CRITICAL / HIGH / MEDIUM / LOW] (CVSS: [X.X])
- **Endpoint**: [Metodo] [URL/endpoint]

#### Descripcion

[Descripcion detallada]

#### PoC

```bash
[Comando exacto]
```

```
[Request/Response]
```

#### Impacto

[Descripcion del impacto]

#### Mitigacion

```[lenguaje]
[Codigo de mitigacion]
```

---

### Hallazgo 6: [Titulo de la vulnerabilidad]

- **ID**: OWASP [codigo] - [Nombre]; CWE-[numero]
- **Severidad**: [CRITICAL / HIGH / MEDIUM / LOW] (CVSS: [X.X])
- **Endpoint**: [Metodo] [URL/endpoint]

#### Descripcion

[Descripcion detallada]

#### PoC

```bash
[Comando exacto]
```

```
[Request/Response]
```

#### Impacto

[Descripcion del impacto]

#### Mitigacion

```[lenguaje]
[Codigo de mitigacion]
```

---

### Hallazgo 7: [Titulo de la vulnerabilidad] (opcional / adicional)

- **ID**: OWASP [codigo] - [Nombre]; CWE-[numero]
- **Severidad**: [CRITICAL / HIGH / MEDIUM / LOW] (CVSS: [X.X])
- **Endpoint**: [Metodo] [URL/endpoint]

#### Descripcion

[Descripcion detallada]

#### PoC

```bash
[Comando exacto]
```

```
[Request/Response]
```

#### Impacto

[Descripcion del impacto]

#### Mitigacion

```[lenguaje]
[Codigo de mitigacion]
```

---

### Hallazgo 8: [Titulo de la vulnerabilidad] (opcional / adicional)

- **ID**: OWASP [codigo] - [Nombre]; CWE-[numero]
- **Severidad**: [CRITICAL / HIGH / MEDIUM / LOW] (CVSS: [X.X])
- **Endpoint**: [Metodo] [URL/endpoint]

#### Descripcion

[Descripcion detallada]

#### PoC

```bash
[Comando exacto]
```

```
[Request/Response]
```

#### Impacto

[Descripcion del impacto]

#### Mitigacion

```[lenguaje]
[Codigo de mitigacion]
```

---

## 7. Ataques al Sistema Operativo / Infraestructura

### 7.1. Escaneo de puertos del host

Se realizo un escaneo completo de puertos sobre la IP de la VM/contenedor Docker para identificar servicios expuestos.

```bash
nmap -sS -sV -O -p- [IP_OBJETIVO]
```

**Resultados:**

| Puerto | Servicio | Version | Estado |
|--------|----------|---------|--------|
| [puerto] | [servicio] | [version] | open |
| [puerto] | [servicio] | [version] | open |
| [puerto] | [servicio] | [version] | open |

**Sistema operativo detectado:** [Linux/Windows, distribucion/version]

### 7.2. Fuerza bruta a SSH

Se intento acceso por fuerza bruta al servicio SSH utilizando Hydra/Medusa con diccionarios de credenciales comunes.

```bash
hydra -l [usuario] -P [diccionario.txt] ssh://[IP_OBJETIVO]
```

**Resultados:**

| Usuario | Password | Acceso concedido |
|---------|----------|-----------------|
| [usuario] | [password] | Si/No |

### 7.3. FTP anonymous access

Se probo el acceso anonimo al servicio FTP.

```bash
ftp [IP_OBJETIVO]
# User: anonymous
# Password: anonymous
```

**Resultados:**

| Acceso anonimo | Archivos encontrados | Contenido sensible |
|----------------|---------------------|-------------------|
| Si/No | [lista de archivos] | [Si/No - descripcion] |

### 7.4. Escalacion de privilegios

Una vez obtenido acceso a la shell, se realizo una busqueda de vectores de escalacion de privilegios.

```bash
# Ver usuarios y grupos
cat /etc/passwd
cat /etc/shadow

# Ver permisos sudo
sudo -l

# Buscar binarios SUID
find / -perm -4000 2>/dev/null

# Ejecutar LinPEAS
./linpeas.sh
```

**Resultados:**

| Vector | Encontrado | Descripcion |
|--------|-----------|-------------|
| SUID bins | Si/No | [binarios encontrados] |
| Sudo misconfig | Si/No | [comandos sudo permitidos] |
| Crontab | Si/No | [tareas programadas] |
| Kernel exploit | Si/No | [version de kernel] |

### 7.5. Container escape (si aplica)

Se evaluo la posibilidad de escapar del contenedor Docker al host subyacente.

```bash
# Verificar montaje de docker.sock
ls -la /var/run/docker.sock

# Ver capacidades del contenedor
cat /proc/1/status | grep Cap

# Intentar listar contenedores desde dentro
docker ps

# Montar disco del host (si --privileged)
fdisk -l
mount /dev/sda1 /mnt
```

**Resultados:**

| Vector | Encontrado | Descripcion |
|--------|-----------|-------------|
| docker.sock montado | Si/No | [ruta] |
| Privileged mode | Si/No | - |
| Capabilities peligrosas | Si/No | [SYS_ADMIN, NET_ADMIN, etc.] |
| Escape exitoso | Si/No | [detalles] |

### 7.6. Base de datos expuesta

Se intento acceder a la base de datos directamente si el puerto estaba expuesto.

```bash
# Conexion a MySQL
mysql -h [IP_OBJETIVO] -u root -p

# Conexion a PostgreSQL
psql -h [IP_OBJETIVO] -U postgres
```

**Resultados:**

| Motor | Puerto | Acceso sin password | Bases de datos encontradas |
|-------|--------|--------------------|---------------------------|
| [MySQL/PostgreSQL] | [puerto] | Si/No | [listado] |

### 7.7. Secretos en archivos de configuracion

Se buscaron archivos de configuracion con credenciales o secretos en el sistema.

```bash
# Buscar archivos .env
find / -name ".env" 2>/dev/null

# Buscar archivos de configuracion
find / -name "config*" -o -name "*.conf" 2>/dev/null

# Revisar variables de entorno
env
```

**Resultados:**

| Archivo | Ruta | Secretos encontrados |
|---------|------|---------------------|
| .env | [ruta] | [credenciales/tokens expuestos] |
| config.js | [ruta] | [credenciales expuestas] |

### 7.8. Procesos y servicios corriendo

Se revisaron los procesos y servicios activos en el sistema.

```bash
# Listar procesos
ps aux

# Ver puertos en escucha
netstat -tulpn

# Ver servicios activos
systemctl list-units --type=service --state=running
```

**Resultados:**

| Proceso/Servicio | PID | Puerto | Usuario | Descripcion |
|-----------------|-----|--------|---------|-------------|
| [nombre] | [PID] | [puerto] | [usuario] | [descripcion] |

---

## 8. Categorias OWASP Top 10 evaluadas

| # | Categoria OWASP | Evaluada | Hallazgo encontrado |
|---|-----------------|----------|---------------------|
| A01 | Broken Access Control | [Si/No] | [Hallazgo #] |
| A02 | Cryptographic Failures | [Si/No] | [Hallazgo #] |
| A03 | Injection | [Si/No] | [Hallazgo #] |
| A04 | Insecure Design | [Si/No] | [Hallazgo #] |
| A05 | Security Misconfiguration | [Si/No] | [Hallazgo #] |
| A06 | Vulnerable and Outdated Components | [Si/No] | [Hallazgo #] |
| A07 | Identification and Auth Failures | [Si/No] | [Hallazgo #] |
| A08 | Software and Data Integrity Failures | [Si/No] | [Hallazgo #] |
| A09 | Security Logging and Monitoring Failures | [Si/No] | [Hallazgo #] |
| A10 | Server-Side Request Forgery (SSRF) | [Si/No] | [Hallazgo #] |

**Total de categorias evaluadas:** [N] de 10 (minimo requerido: 6)

---

## 9. Estadisticas

### 9.1. Distribucion por severidad

| Severidad | Cantidad | Porcentaje |
|-----------|----------|------------|
| Critical | [N] | [X]% |
| High | [N] | [X]% |
| Medium | [N] | [X]% |
| Low | [N] | [X]% |
| Info | [N] | [X]% |
| **Total** | **[N]** | **100%** |

### 9.2. Distribucion por categoria OWASP

| Categoria | Cantidad de hallazgos |
|-----------|----------------------|
| A01 - Broken Access Control | [N] |
| A02 - Cryptographic Failures | [N] |
| A03 - Injection | [N] |
| A04 - Insecure Design | [N] |
| A05 - Security Misconfiguration | [N] |
| A06 - Vulnerable Components | [N] |
| A07 - Identification & Auth Failures | [N] |
| A08 - Integrity Failures | [N] |
| A09 - Logging & Monitoring Failures | [N] |
| A10 - SSRF | [N] |

### 9.3. Distribucion por tipo de endpoint

| Tipo de endpoint | Hallazgos |
|-----------------|-----------|
| GET (lectura) | [N] |
| POST (creacion) | [N] |
| PUT/PATCH (actualizacion) | [N] |
| DELETE (eliminacion) | [N] |

### 9.4. Topologia de riesgo

```
Critical  [X%]  ########
High      [X%]  ######
Medium    [X%]  ####
Low       [X%]  ##
Info      [X%]  #
```

---

## 10. Conclusiones

### 10.1. Resumen general

La aplicacion desarrollada por el [Grupo Y] presenta [fortalezas/debilidades] en materia de seguridad. Se identificaron [N] vulnerabilidades, de las cuales [N] son de severidad Critical o High, lo que representa un riesgo [aceptable/moderado/alto] para el negocio. Adicionalmente, se evaluaron [N] vectores de ataque al sistema operativo, de los cuales [N] resultaron exitosos.

### 10.2. Aspectos positivos

- [Aspecto de seguridad que el grupo objetivo implemento correctamente]
- [Otro aspecto positivo]
- [Otro aspecto positivo]

### 10.3. Areas de mejora

- [Area critica que requiere atencion inmediata]
- [Area que requiere mejora a mediano plazo]
- [Area de mejora continua]

### 10.4. Lecciones aprendidas

**Como equipo atacante (Red Team):**
- [Que aprendio el grupo durante el proceso de pentesting]
- [Tecnica o herramienta que resulto especialmente util]
- [Dificultad encontrada y como se supero]

**Recomendaciones para el grupo objetivo (Blue Team/Desarrollo):**
- [Recomendacion general 1]
- [Recomendacion general 2]
- [Recomendacion general 3]

### 10.5. Prioridad de remediacion

| Prioridad | Accion | Hallazgos | Plazo sugerido |
|-----------|--------|-----------|----------------|
| Inmediata | Corregir vulnerabilidades Critical | #[N], #[N] | 24-48 horas |
| Corto plazo | Corregir vulnerabilidades High | #[N], #[N] | 1 semana |
| Mediano plazo | Corregir vulnerabilidades Medium | #[N], #[N] | 2-4 semanas |
| Largo plazo | Corregir vulnerabilidades Low/Info | #[N], #[N] | Proximo sprint |

---

## 11. Anexos

### Anexo A: Scripts de explotacion

Los scripts se encuentran en el directorio `pocs/` del repositorio del grupo.

| Nombre del script | Descripcion | Lenguaje |
|-------------------|-------------|----------|
| `[script1].py` | [Descripcion] | Python 3 |
| `[script2].py` | [Descripcion] | Python 3 |
| `[script3].sh` | [Descripcion] | Bash |
| `[script4].py` | [Descripcion] | Python 3 |

### Anexo B: Requests HTTP raw

Los archivos de requests HTTP se encuentran en `pocs/requests/`.

| Archivo | Endpoint | Descripcion |
|---------|----------|-------------|
| `[request1].txt` | [Endpoint] | [Descripcion] |
| `[request2].txt` | [Endpoint] | [Descripcion] |
| `[request3].txt` | [Endpoint] | [Descripcion] |

### Anexo C: Payloads utilizados

Los payloads se documentan en `pocs/payloads/`.

| Archivo | Tipo | Descripcion |
|---------|------|-------------|
| `[payloads1].txt` | SQLi | Payloads de inyeccion SQL probados |
| `[payloads2].txt` | XSS | Payloads de Cross-Site Scripting probados |
| `[payloads3].txt` | [Otro] | [Descripcion] |

### Anexo D: Salidas completas de herramientas

| Herramienta | Archivo de salida |
|-------------|-------------------|
| Nmap | `outputs/nmap_scan.txt` |
| Nikto | `outputs/nikto_scan.txt` |
| OWASP ZAP | `outputs/zap_report.html` |
| SQLMap | `outputs/sqlmap_results.txt` |
| WhatWeb | `outputs/whatweb.txt` |
| Hydra | `outputs/hydra_ssh.txt` |
| LinPEAS | `outputs/linpeas.txt` |

### Anexo E: Checklist de cumplimiento

| Requisito | Cumple | Puntaje |
|-----------|--------|---------|
| Reconocimiento completo (nmap, whatweb, endpoints) | [Si/No] | - |
| Escaneo automatizado (ZAP, Nikto, SQLMap) | [Si/No] | - |
| Pruebas manuales (6+ categorias OWASP) | [Si/No] | - |
| PoCs funcionales y reproducibles | [Si/No] | - |
| Informe profesional (CVSS, impacto, mitigaciones) | [Si/No] | - |
| Presentacion con demo en vivo (2+ ataques) | [Si/No] | - |
| Scripts/herramientas documentados | [Si/No] | - |
| Conclusiones y lecciones aprendidas | [Si/No] | - |
| **Ataques al sistema operativo (fuerza bruta SSH, escalacion, container escape)** | **[Si/No]** | **15 puntos** |
| **Template de informe completado correctamente** | **[Si/No]** | **10 puntos** |
| **Rules of Engagement cumplidas** | **[Si/No]** | **5 puntos** |

---

---

# INFORME DE PENTESTING - TAREA RED TEAM

## Grupo Atacante: [Nombres]
## Grupo Objetivo: [Nombres]
## Aplicacion: [Escenario]
## Fecha: [Fecha de entrega]

---

## 1. RESUMEN EJECUTIVO
[2-3 parrafos: alcance, metodologia, hallazgos criticos, recomendaciones principales]
[Incluir tabla con total de vulnerabilidades por severidad]

## 2. ALCANCE Y METODOLOGIA
### 2.1 Alcance
- Direccion IP objetivo: [IP:Puerto]
- Sistema operativo: [detectado]
- Aplicacion: [URLs, endpoints]
### 2.2 Metodologia
- Estandar: PTES (Penetration Testing Execution Standard)
- CVSS v3.1 para puntuacion de vulnerabilidades
### 2.3 Herramientas utilizadas
[Tabla: Herramienta, Version, Uso]

## 3. RECONOCIMIENTO
### 3.1 Informacion general del objetivo
| Elemento | Resultado |
|----------|-----------|
| IP | |
| Puertos abiertos | |
| SO detectado | |
| Servicios | |
| Tecnologias web | |
### 3.2 Comandos utilizados
```
nmap -sS -sV -O -p- [IP]
whatweb [URL]
...
```
### 3.3 Resultados

## 4. VULNERABILIDADES ENCONTRADAS

### [H-01] [Nombre de la vulnerabilidad] - [Severidad: CRITICAL/HIGH/MEDIUM/LOW]
- **OWASP ID**: [ej: A1: Injection]
- **CWE**: [ej: CWE-89]
- **CVSS**: [ej: 9.8]
- **Endpoint**: [Ruta]
- **Descripcion**: [Explicacion detallada]
- **PoC** (Proof of Concept):
  ```
  [Comando, codigo o request utilizado]
  ```
- **Impacto**: [Que puede lograr un atacante]
- **Recomendacion**: [Como mitigarlo]
- **Referencia**: [OWASP Cheat Sheet, enlace]

[Repetir para cada vulnerabilidad encontrada]

## 5. ATAQUES AL SISTEMA OPERATIVO
### 5.1 Escaneo de puertos
### 5.2 Fuerza bruta SSH/FTP
### 5.3 Escalacion de privilegios
### 5.4 Container escape (si aplica)
### 5.5 Secretos expuestos

## 6. ESTADISTICAS
| Severidad | Cantidad | Porcentaje |
|-----------|----------|------------|
| Critical | | |
| High | | |
| Medium | | |
| Low | | |
| **Total** | | |

## 7. CONCLUSIONES Y RECOMENDACIONES
### 7.1 Hallazgos criticos a mitigar
### 7.2 Recomendaciones generales
### 7.3 Lecciones aprendidas

---

## ANEXOS
### A. Scripts utilizados
### B. Requests HTTP
### C. Payloads
### D. Salidas de herramientas
### E. Checklist OWASP Top 10 evaluado

---

## 12. Registro de cambios

| Version | Fecha | Cambios realizados | Autor |
|---------|-------|--------------------|-------|
| 1.0 | [Fecha] | Version inicial del informe | [Nombre] |

---

*Documento generado como parte de la Tarea 2 - Red Team del curso Taller de Ciberseguridad Orientada al Desarrollo.*
*Prohibida su distribucion fuera del ambito academico sin autorizacion del profesor.*
