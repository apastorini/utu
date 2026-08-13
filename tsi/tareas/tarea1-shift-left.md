# Tarea 1 - Shift Left: Seguridad en Desarrollo

**Curso:** Taller de Ciberseguridad Orientada al Desarrollo  
**Tipo:** Trabajo grupal (2 personas)  
**Entrega:** Clase 37 | **Presentacion:** Clases 42-43

---

## 1. Objetivo

Desarrollar una API REST funcional aplicando principios de seguridad **Shift Left**: las practicas de seguridad deben integrarse desde el inicio del ciclo de desarrollo, no al final. El proyecto incluye codificacion segura, pipeline CI/CD con gates de seguridad, despliegue en VM o contenedor Docker, y documentacion de las decisiones adoptadas.

El grupo **Blue Team** desarrolla y despliega la aplicacion. El grupo **Red Team** (asignado por el profesor) realizara pruebas de penetracion sobre la API y la infraestructura desplegada. Por ello, el Blue Team debe exponer deliberadamente ciertas vulnerabilidades controladas con fines educativos.

---

## 2. Escenarios disponibles

Cada grupo recibe UN escenario asignado por el profesor. Todos los grupos tienen los mismos requisitos funcionales y de seguridad, pero adaptados al escenario recibido.

| #  | Escenario | Recurso principal |
|----|-----------|-------------------|
| 1  | Plataforma de E-commerce | Productos con carrito de compras |
| 2  | Sistema de Gestion Hospitalaria | Turnos medicos e historias clinicas |
| 3  | Red Social de Microblogging | Posts, likes, follows |
| 4  | Sistema Bancario Online | Transferencias y gestion de cuentas |
| 5  | Plataforma de E-learning | Cursos, inscripciones y evaluaciones |
| 6  | Sistema de Reservas de Vuelos | Busqueda y reserva de vuelos |
| 7  | Plataforma de Streaming | Catalogo de videos y suscripciones |
| 8  | Sistema de Comercio P2P | Compra-venta entre usuarios con reputacion |

---

## 3. Requisitos funcionales

Desarrollar una API REST utilizando el framework/lenguaje de preferencia (Flask, FastAPI, Express.js, Django REST, etc.).

1. **Registro de usuario** con email y contraseña.
2. **Login** con JWT (access token + refresh token).
3. **CRUD completo** del recurso principal del escenario (crear, leer, actualizar, eliminar).
4. **Perfil de usuario** con datos personales (nombre, email, etc.). El usuario solo puede ver/editar su propio perfil.
5. **Busqueda y filtro** del recurso principal (por nombre, categoria, fecha, etc.).
6. **Roles**: al menos dos roles -- `admin` (gestion global) y `user` (operaciones sobre sus propios recursos).

---

## 4. Requisitos de seguridad (Shift Left)

Cada item debe estar implementado y documentado en el informe.

### 4.1 Validacion de entradas (10 pts)

- Usar **whitelist** (lista blanca) en todos los endpoints: definir que campos y formatos se aceptan, rechazar todo lo demas.
- Sanitizar entradas para eliminar caracteres peligrosos (etiquetas HTML, caracteres de escape, etc.).
- Validar tipos de datos, longitudes maximas y minimas, y rangos.
- No confiar unicamente en validacion del frontend; toda validacion debe replicarse en el backend.

### 4.2 Autenticacion y autorizacion (15 pts)

- Almacenar contraseñas con **bcrypt** o **argon2** (nunca en texto plano, nunca con hash debil como MD5/SHA1).
- JWT con **expiracion** (access token corto: 15-30 min; refresh token largo: 7-30 dias).
- Endpoint para renovar access token usando refresh token (con rotacion).
- **RBAC** (Role-Based Access Control) via middleware: `admin` puede todo; `user` solo sobre recursos propios.
- Proteger contra **IDOR** (Insecure Direct Object Reference): verificar que el usuario autenticado es el propietario del recurso antes de cualquier operacion.

### 4.3 Prevencion de inyecciones (10 pts)

- Usar **ORM** o **prepared statements / parametrized queries** en todas las consultas a la base de datos.
- Prohibida la concatenacion de strings para construir queries SQL.
- Si se usa SQL nativo, emplear siempre parametros posicionales o nominales ($1, $2 o :name).

### 4.4 Security Headers y Rate Limiting (10 pts)

- Implementar los siguientes headers HTTP en todas las respuestas:
  - `Strict-Transport-Security` (HSTS)
  - `Content-Security-Policy` (CSP)
  - `X-Frame-Options` (DENY o SAMEORIGIN)
  - `X-Content-Type-Options` (nosniff)
- **Rate limiting** en endpoints criticos: login, registro, creacion/actualizacion de recursos.
  - Ejemplo: 5 intentos de login por minuto por IP, 30 requests por minuto por usuario en endpoints generales.
  - Respuesta con `429 Too Many Requests` y header `Retry-After`.

### 4.5 Manejo seguro de errores y logging (10 pts)

- **Errores genericos** al cliente: nunca exponer detalles internos (stack traces, nombres de tablas, versiones de librerias).
- **Logging estructurado** en formato JSON con nivel apropiado (INFO, WARN, ERROR).
- Los logs **no deben incluir** datos sensibles: contraseñas, tokens, datos biometricos, tarjetas de credito.
- Registrar: timestamp, nivel, mensaje, endpoint, usuario (anonimizado si aplica), ID de correlacion.

### 4.6 Secrets Management (5 pts)

- No hardcodear secretos (claves JWT, credenciales de DB, API keys).
- Usar **variables de entorno** (archivo `.env` excluido del repositorio via `.gitignore`).
- Proveer un archivo `.env.example` con valores placeholder.
- En pipeline CI/CD, usar **secrets del repositorio** (Jenkins credentials / GitHub Secrets / GitLab CI Variables).

### 4.7 Cifrado de datos sensibles en reposo (opcional segun escenario)

- Si el escenario maneja datos especialmente sensibles (historias clinicas, datos bancarios, documentos de identidad), cifrar con **AES-256-GCM** antes de almacenar.
- La clave de cifrado debe obtenerse de variable de entorno, nunca hardcodeada.

---

## 5. Requisitos del pipeline CI/CD (30 pts)

Crear un pipeline automatizado en **Jenkins** (obligatorio). El Jenkinsfile debe estar incluido en el repositorio raiz. Se permite complementar con GitHub Actions solo como alternativa adicional, pero el pipeline principal debe ser en Jenkins.

### 5.1 Etapas del pipeline

El Jenkinsfile debe incluir las siguientes etapas (stages) en orden:

1. **Checkout**: clonar el repositorio desde GitHub/GitLab.
2. **Linting**: analisis de estilo y buenas practicas (flake8 / ESLint / pylint).
3. **Tests unitarios**: ejecutar suite de tests (pytest / jest / unittest) y validar que todos pasan.
4. **SAST (Static Application Security Testing)**: escaneo de vulnerabilidades en codigo fuente (Bandit para Python, Semgrep, SonarQube, o similar).
5. **SCA (Software Composition Analysis)**: escaneo de dependencias (pip-audit / Safety para Python, Snyk, OWASP Dependency-Check).
6. **Build Docker**: construir imagen Docker siguiendo buenas practicas de seguridad (imagen base minima, no ejecutar como root, multi-stage build).
7. **Trivy scan**: escaneo de vulnerabilidades en la imagen Docker con Trivy.
8. **Deploy**: publicar la imagen en un registro (Docker Hub, GitHub Container Registry) o desplegar en el entorno destino.

### 5.2 Quality Gate

El pipeline debe **fallar** si se encuentran vulnerabilidades CRITICAS o HIGH en SAST, SCA o Trivy.

### 5.3 Estructura del Jenkinsfile

Incluir un archivo `Jenkinsfile` en la raiz del repositorio con la siguiente estructura:

```groovy
pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'myapp:latest'
        DOCKER_REGISTRY = 'docker.io'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Lint') {
            steps {
                sh 'pip install flake8 && flake8 .'
            }
        }

        stage('Test') {
            steps {
                sh 'pip install -r requirements.txt && pytest'
            }
        }

        stage('SAST - Bandit') {
            steps {
                sh 'pip install bandit && bandit -r . -f json -o bandit-report.json'
            }
            post {
                always {
                    archiveArtifacts artifacts: 'bandit-report.json'
                }
            }
        }

        stage('SCA - Safety/pip-audit') {
            steps {
                sh 'pip install pip-audit && pip-audit'
            }
        }

        stage('Build Docker') {
            steps {
                sh 'docker build -t $DOCKER_IMAGE .'
            }
        }

        stage('Trivy Scan') {
            steps {
                sh 'trivy image --severity CRITICAL,HIGH --exit-code 1 $DOCKER_IMAGE'
            }
        }

        stage('Deploy') {
            steps {
                sh 'docker push $DOCKER_IMAGE'
            }
        }
    }

    post {
        failure {
            emailext(
                to: "${env.CHANGE_AUTHOR_EMAIL}",
                subject: "Pipeline fallo - ${env.JOB_NAME} - ${env.BUILD_NUMBER}",
                body: "El pipeline ha fallado. Revisar: ${env.BUILD_URL}"
            )
        }
    }
}
```

### 5.4 Instrucciones para instalar Jenkins (via Docker)

Incluir en el README los pasos para:

1. Ejecutar Jenkins en Docker:
   ```bash
   docker run -d --name jenkins \
     -p 8080:8080 -p 50000:50000 \
     -v jenkins_home:/var/jenkins_home \
     -v /var/run/docker.sock:/var/run/docker.sock \
     jenkins/jenkins:lts
   ```
2. Obtener la contraseña inicial: `docker logs jenkins`.
3. Instalar los plugins necesarios: Docker Pipeline, Blue Ocean, Credentials Binding, Email Extension.
4. Configurar credenciales en Jenkins (GitHub token, Docker Hub credentials) via "Manage Jenkins > Credentials".
5. Crear un Pipeline job que apunte al repositorio y al Jenkinsfile.

---

## 6. Despliegue obligatorio en VM o Docker (10 pts)

La API debe desplegarse y ser accesible desde la red para que el Red Team pueda realizar las pruebas de penetracion.

### 6.1 Opciones de despliegue

- **Maquina virtual**: VirtualBox con Alpine Linux o Ubuntu Server. Configurar red en modo "Bridge" o "NAT con reenvio de puertos" para que sea accesible desde la red del laboratorio.
- **Contenedor Docker**: Ejecutar la aplicacion en un contenedor con puertos expuestos y accesible desde la red del host.

### 6.2 Requisitos del despliegue

- Compartir la direccion IP y puerto con el profesor para que el Red Team pueda atacar.
- El contenedor o VM debe mantenerse operativo durante el periodo de pruebas.
- Documentar en el README las instrucciones detalladas paso a paso para:
  - Descargar y compilar el proyecto.
  - Ejecutar la aplicacion en Docker (`docker build` y `docker run` con puertos expuestos).
  - Acceder a la API (todos los endpoints documentados en una tabla).
  - Acceder al sistema operativo subyacente si logran escalar privilegios (VM o contenedor).

### 6.3 Usuario de prueba deliberadamente vulnerable

Crear un usuario de prueba con credenciales debiles para que el Red Team tenga un punto de entrada conocido. Ejemplo:

- **Usuario**: `admin`
- **Contraseña**: `admin123`

Documentar este usuario en el README como "usuario de prueba para propositos educativos".

---

## 7. VM expuesta con proposito educativo (5 pts)

El grupo Blue Team debe exponer deliberadamente algunos servicios inseguros PARA PROPOSITO EDUCATIVO del ejercicio Red Team. Esto permite al Red Team practicar tanto pentesting web (API) como pentesting de sistema operativo.

### 7.1 Servicios inseguros sugeridos

- Puerto SSH abierto con autenticacion por contraseña (no solo llaves).
- Servicio FTP anonimo o con credenciales debiles.
- Panel de administracion en una ruta predecible (ej: `/admin`) con contraseña debil.
- Puerto de base de datos expuesto (ej: PostgreSQL en 5432) con credenciales por defecto.
- Endpoint de depuracion (debug) habilitado en produccion.

### 7.2 Documentacion requerida

En el README o en una seccion del informe, documentar:

- Que vulnerabilidades fueron dejadas INTENCIONALMENTE.
- Cuales vulnerabilidades fueron mitigadas (y como).
- Cual es el alcance de cada vulnerabilidad intencional (que puede hacer el atacante si la explota).
- Cuales servicios estan protegidos y no deben ser atacados (limites del ejercicio).

---

## 8. Entregables

1. **Repositorio Git** (GitHub o GitLab) con codigo fuente completo.
2. **README.md** que incluya:
   - Instrucciones de instalacion y ejecucion (incluyendo Docker y Jenkins).
   - Descripcion del escenario.
   - Decisiones de seguridad tomadas y justificacion.
   - Variables de entorno necesarias (`.env.example`).
   - Explicacion del pipeline CI/CD (Jenkins).
   - Instrucciones detalladas para el Red Team (despliegue, endpoints, usuario vulnerable).
   - Documentacion de vulnerabilidades intencionales y mitigadas.
3. **Jenkinsfile** completo en la raiz del repositorio.
4. **Pipeline CI/CD** configurado y funcionando (verde en el ultimo build de Jenkins).
5. **Despliegue funcional** en VM o Docker, accesible desde la red.
6. **Informe de seguridad** (formato PDF o MD) siguiendo el template estandar provisto en este documento, que incluya:
   - Diagrama de threat modeling usando metodologia STRIDE.
   - Vulnerabilidades identificadas durante el desarrollo y como se mitigaron.
   - Justificacion de cada decision de seguridad implementada.
   - Resultados de SAST, SCA y Trivy (capturas de pantalla o tablas con hallazgos).
   - Analisis de riesgos residuales.
7. **Video demo** (maximo 5 minutos) mostrando:
   - Funcionalidad basica de la API (registro, login, CRUD).
   - Ejecucion del pipeline CI/CD en Jenkins y sus etapas.
   - Resultados de las herramientas de seguridad.
   - Despliegue en VM o Docker funcionando.

---

## 9. Rubrica de evaluacion

| Criterio | Detalle | Puntos |
|----------|---------|--------|
| Validacion de entradas | Whitelist en todos los endpoints, sanitizacion, validacion de tipos y longitudes | 10 |
| Autenticacion y autorizacion | bcrypt/argon2, JWT con expiracion, refresh tokens, RBAC, proteccion contra IDOR | 15 |
| Prevencion de inyecciones | ORM o prepared statements, sin concatenacion de strings en queries | 10 |
| Security headers y rate limiting | HSTS, CSP, X-Frame-Options, X-Content-Type-Options, rate limiting en login y endpoints criticos | 10 |
| Manejo seguro de errores y logging | Errores genericos al cliente, logs JSON sin datos sensibles, niveles adecuados | 10 |
| Secrets management | Variables de entorno, .env.example, sin secretos hardcodeados | 5 |
| Pipeline CI/CD con gates de seguridad | Lint, tests, SAST, SCA, quality gate que falla en criticas/high, Docker seguro | 20 |
| Jenkinsfile completo y funcional | Jenkinsfile con todas las etapas (Checkout, Lint, Test, SAST, SCA, Build Docker, Trivy, Deploy) | 10 |
| Despliegue en VM/Docker funcional | API desplegada y accesible desde la red, IP/puerto compartido con el profesor | 10 |
| README con instrucciones para Red Team | Instrucciones detalladas para descargar, ejecutar, acceder a la API y al sistema operativo | 5 |
| Vulnerabilidades intencionales documentadas | Servicios inseguros expuestos y documentados, tabla de vulnerabilidades intencionales vs mitigadas | 5 |
| Template de informe completado | Informe siguiendo el template estandar con todas las secciones requeridas | 10 |
| Informe de seguridad | Threat modeling STRIDE, vulnerabilidades identificadas/mitigadas, justificacion, resultados SAST/SCA | 10 |
| README y documentacion | Instalacion, escenario, decisiones de seguridad, .env.example, pipeline, despliegue | 5 |
| Video demo | 5 min mostrando funcionalidad + pipeline + resultados de seguridad + despliegue | 5 |
| **Total** | | **140** |

---

## 10. Fechas importantes

- **Clase 37**: Entrega del repositorio (push a GitHub/GitLab, tag o commit final).
- **Clases 41-42**: Presentacion en clase (10-15 min por grupo, incluyendo demo del pipeline, despliegue y discusion de seguridad).

---

## 11. Recomendaciones y buenas practicas

- Usar un linter desde el primer commit; no dejar la deuda tecnica para el final.
- Escribir tests unitarios para los endpoints criticos (login, registro, CRUD).
- Ejecutar SAST y SCA localmente antes de hacer push para evitar sorpresas en el pipeline.
- La imagen Docker debe ser escaneada (Trivy, Docker Scout) como paso adicional en el pipeline.
- No subir el archivo `.env` ni `__pycache__/`, `node_modules/`, `.venv/` al repositorio.
- Documentar en el README las decisiones de seguridad: por que se eligio bcrypt sobre argon2, por que tal header CSP, etc.
- Para el threat modeling, considerar activos, actores, limites de confianza y flujos de datos. Incluir un diagrama (Draw.io, Lucidchart, Mermaid).
- Probar el despliegue en un entorno limpio (VM limpia o contenedor desde cero) para asegurarse de que las instrucciones del README son correctas.
- Coordinar con el Red Team asignado para definir ventana de pruebas y reglas de engagement.

---

## 12. Ejemplo de threat modeling con STRIDE

| Tipo de amenaza | Descripcion | Mitigacion |
|-----------------|-------------|------------|
| Spoofing | Suplantacion de identidad via JWT robado | Refresh token rotation, expiracion corta, HTTPS |
| Tampering | Modificacion de datos en transito | HTTPS, HMAC en JWT, validacion de integridad |
| Repudiation | Usuario niega haber realizado una accion | Logging estructurado con ID de correlacion y timestamp |
| Information Disclosure | Exposicion de datos sensibles en respuestas | Errores genericos, cifrado AES-256-GCM en reposo |
| Denial of Service | Ataque de fuerza bruta en login | Rate limiting, account lockout temporal |
| Elevation of Privilege | Usuario user accede a recurso de admin | RBAC middleware, verificacion de pertenencia (IDOR check) |

---

## 13. Stack tecnologico sugerido (a confirmar con el profesor)

| Lenguaje | Framework | ORM | Testing | SAST | SCA |
|----------|-----------|-----|---------|------|-----|
| Python | Flask / FastAPI | SQLAlchemy / Peewee | pytest | Bandit | pip-audit / Safety |
| Python | Django REST | Django ORM | pytest | Bandit | pip-audit / Safety |
| Node.js | Express.js | Prisma / Sequelize | Jest | ESLint + eslint-plugin-security | Snyk / npm audit |
| Java | Spring Boot | Hibernate | JUnit | SpotBugs / SonarQube | OWASP Dependency-Check |
| Go | Gin / Chi | GORM | go test | gosec | nancy |

**Nota:** Se permite cualquier lenguaje y framework, siempre que se cumplan los requisitos de seguridad. Consultar con el profesor si hay dudas sobre la eleccion.

---

## 14. Template de informe estandar

El informe debe entregarse en formato PDF o MD completando el siguiente template. Cada seccion debe estar debidamente desarrollada; no se aceptan respuestas de una linea.

```
# INFORME DE DESARROLLO SEGURO - TAREA SHIFT LEFT

## Grupo: [Nombres]
## Escenario: [Escenario asignado]
## Fecha: [Fecha de entrega]

---

## 1. RESUMEN EJECUTIVO
[2-3 parrafos describiendo la aplicacion, decisiones de seguridad principales, y resultados del pipeline]

## 2. ARQUITECTURA DE LA APLICACION
### 2.1 Diagrama de arquitectura
[Diagrama en ASCII o imagen]
### 2.2 Stack tecnologico
[Lenguaje, framework, base de datos, librerias principales]
### 2.3 Endpoints de la API
[Tabla: Metodo, Ruta, Descripcion, Autenticacion, Autorizacion]

## 3. DECISIONES DE SEGURIDAD
### 3.1 Autenticacion y autorizacion
### 3.2 Validacion de entradas
### 3.3 Manejo de errores
### 3.4 Proteccion de datos sensibles
### 3.5 Secrets management

## 4. THREAT MODELING (STRIDE)
| Tipo | Amenaza | Componente | Mitigacion |
|------|---------|------------|------------|
| Spoofing | | | |
| Tampering | | | |
| Repudiation | | | |
| Info Disclosure | | | |
| DoS | | | |
| Elevation of Privilege | | | |

## 5. RESULTADOS DEL PIPELINE CI/CD (JENKINS)
### 5.1 Jenkinsfile
[Codigo completo del Jenkinsfile]
### 5.2 Resultados SAST
[Tabla con hallazgos de Bandit/FindSecBugs]
### 5.3 Resultados SCA
[Tabla con dependencias vulnerables]
### 5.4 Resultados Trivy
[Tabla con vulnerabilidades de la imagen Docker]
### 5.5 Quality Gates
[Explicacion de que hace fallar el pipeline]

## 6. DESPLIEGUE
### 6.1 Instrucciones para Red Team
### 6.2 Vulnerabilidades intencionales
[Tabla con vulnerabilidades dejadas a proposito para el ejercicio]

## 7. VULNERABILIDADES MITIGADAS VS NO MITIGADAS
| Vulnerabilidad | Mitigada? | Tecnica usada |
|----------------|-----------|---------------|
| SQL Injection | Si | Consultas parametrizadas |
| XSS | Si | Output encoding |
| ... | | |

## 8. LECCIONES APRENDIDAS
[3-5 lecciones]
```

