# Clase 14: Jenkins - Instalacion, Configuracion y Pipelines de CI/CD con Seguridad

**Duracion:** 2 horas

---

## Objetivos de Aprendizaje

- Comprender que es Jenkins y su arquitectura (Master + Agentes).
- Instalar y configurar Jenkins usando Docker.
- Crear pipelines declarativos (Jenkinsfile) para automatizar CI/CD.
- Incorporar gates de seguridad (SAST, SCA, escaneo de contenedores) dentro del pipeline.
- Configurar integracion con GitHub/GitLab mediante webhooks.
- Aplicar hardening basico a la instancia de Jenkins.
- Resolver ejercicios practicos con pipelines seguros.

---

## Contenido Detallado

### 1. Que es Jenkins?

Jenkins es un servidor de automatizacion open-source escrito en Java. Es la herramienta mas utilizada en la industria para implementar pipelines de Integracion Continua (CI) y Entrega Continua (CD).

**Usos principales:**
- **Integracion Continua (CI):** compilar, testear y analizar el codigo en cada push al repositorio.
- **Entrega Continua (CD):** desplegar automaticamente en entornos de desarrollo, staging o produccion.

**Arquitectura:**
- **Jenkins Master:** nodo central que gestiona los pipelines, la interfaz web y la programacion de tareas.
- **Agentes (Nodes):** maquinas (fisicas, virtuales o contenedores) que ejecutan los jobs. El master puede delegar trabajo a los agentes para escalar horizontalmente.

**Ecosistema de Plugins:**
Jenkins tiene mas de 1800 plugins que extienden su funcionalidad: integracion con Git, Docker, Kubernetes, SonarQube, AWS, Azure, etc.

---

### 2. Instalacion de Jenkins (paso a paso)

#### Opcion 1: Instalacion nativa en Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install -y openjdk-17-jre

curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io.key | sudo tee /usr/share/keyrings/jenkins-keyring.asc > /dev/null
echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] https://pkg.jenkins.io/debian-stable binary/ | sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null

sudo apt update
sudo apt install -y jenkins

sudo systemctl start jenkins
sudo systemctl enable jenkins
```

#### Opcion 2: Jenkins con Docker (recomendada para el curso)

```bash
docker run -d --name jenkins \
  -p 8080:8080 -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  jenkins/jenkins:lts-jdk17
```

**Explicacion de parametros:**
- `-p 8080:8080`: expone el puerto web de Jenkins.
- `-p 50000:50000`: puerto para conexion de agentes (JNLP).
- `-v jenkins_home:/var/jenkins_home`: volumen persistente para configuracion.
- `-v /var/run/docker.sock:/var/run/docker.sock`: permite a Jenkins ejecutar Docker dentro del contenedor (Docker-in-Docker).

#### Obtener la contrasena inicial

```bash
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

#### Acceder a la interfaz web
Abrir `http://localhost:8080` en el navegador, pegar la contrasena inicial y seguir el asistente:
1. Instalar plugins sugeridos.
2. Crear usuario administrador.
3. Configurar la URL de Jenkins.

---

### 3. Configuracion inicial de Jenkins

#### Plugins recomendados

Estos plugins son esenciales para un pipeline de CI/CD con seguridad:

| Plugin | Proposito |
|--------|-----------|
| Git | Integracion con repositorios Git |
| Pipeline | Creacion de pipelines como codigo |
| Blue Ocean | Interfaz grafica moderna |
| Docker Pipeline | Construir y publicar imagenes Docker |
| HTML Publisher | Publicar reportes HTML (Bandit, etc.) |
| JUnit | Publicar reportes de tests |
| SonarQube Scanner | Analisis estatico de codigo (SAST) |
| OWASP Dependency-Check | Analisis de dependencias (SCA) |

**Instalacion:** Manage Jenkins -> Plugins -> Available Plugins -> buscar e instalar.

#### Configurar herramientas

1. Ir a Manage Jenkins -> Tools.
2. Agregar:
   - **JDK:** instalacion automatica (Adoptium JDK 17).
   - **Git:** ruta del binario (usar `which git`).
   - **Maven:** instalacion automatica (Maven 3.9).

#### Credenciales

1. Ir a Manage Jenkins -> Credentials -> System -> Global credentials (unrestricted).
2. Agregar:
   - **GitHub token:** tipo "Secret text" con un token personal de GitHub.
   - **SSH key:** para acceso a repositorios privados.
   - **Docker Hub credentials:** tipo "Username with password".

Las credenciales se referencian en el Jenkinsfile usando el ID asignado:

```groovy
withCredentials([string(credentialsId: 'github-token', variable: 'TOKEN')]) {
    sh "curl -H 'Authorization: token $TOKEN' ..."
}
```

---

### 4. Concepto de Pipeline en Jenkins

Un pipeline es una secuencia automatizada de pasos (stages) que llevan el codigo desde el repositorio hasta produccion. Jenkins permite definir pipelines como codigo mediante un archivo llamado **Jenkinsfile**.

#### Pipeline como Codigo (Pipeline as Code)

Ventajas:
- Versionado junto con el codigo fuente.
- Reutilizable entre proyectos.
- Auditable (cada cambio queda registrado en Git).

#### Declarative Pipeline vs Scripted Pipeline

| Caracteristica | Declarative | Scripted |
|----------------|-------------|----------|
| Sintaxis | Simple, estructurada | Flexible, basada en Groovy |
| Curva de aprendizaje | Baja | Media-alta |
| Validacion | Built-in | Manual |
| Uso recomendado | Proyectos nuevos | Casos complejos |

**Declarative Pipeline (recomendado):**

```groovy
pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/user/repo.git'
            }
        }
        stage('Build') {
            steps {
                sh 'mvn compile'
            }
        }
        stage('Test') {
            steps {
                sh 'mvn test'
            }
        }
        stage('Deploy') {
            steps {
                sh 'mvn deploy'
            }
        }
    }
}
```

**Explicacion de secciones:**
- `pipeline`: bloque raiz de todo pipeline declarativo.
- `agent`: define donde se ejecuta (any, none, docker, label).
- `stages`: contenedor de etapas, se ejecutan en orden.
- `stage`: etapa individual con nombre descriptivo.
- `steps`: pasos concretos dentro de cada etapa.
- `post`: bloque opcional que se ejecuta al final (always, success, failure).

---

### 5. Pipeline con Gates de Seguridad

Los **gates de seguridad** son puntos de control dentro del pipeline que verifican que el codigo cumple con requisitos minimos de seguridad antes de continuar. Si un gate falla, el pipeline se detiene y no se despliega.

#### Stage SAST (Static Application Security Testing)

Analiza el codigo fuente en busqueda de vulnerabilidades sin ejecutarlo.

```groovy
stage('SAST - Bandit') {
    steps {
        sh 'bandit -r app/ -f json -o bandit-report.json'
    }
    post {
        always {
            publishHTML(target: [
                reportName: 'Bandit Report',
                reportDir: '.',
                reportFiles: 'bandit-report.json'
            ])
        }
        failure {
            error "SAST encontro vulnerabilidades criticas. Pipeline detenido."
        }
    }
}
```

#### Stage SCA (Software Composition Analysis)

Analiza las dependencias del proyecto en busca de vulnerabilidades conocidas.

```groovy
stage('SCA - OWASP Dependency-Check') {
    steps {
        sh 'dependency-check --scan . -o dependency-check-report.html'
    }
    post {
        always {
            publishHTML(target: [
                reportName: 'Dependency Check',
                reportDir: '.',
                reportFiles: 'dependency-check-report.html'
            ])
        }
    }
}
```

#### Stage Container Scan

Escanea la imagen Docker en busca de vulnerabilidades en las capas del sistema operativo y paquetes.

```groovy
stage('Container Scan - Trivy') {
    steps {
        sh 'trivy image --severity=CRITICAL --exit-code 1 myapp:latest'
    }
}
```

El parametro `--exit-code 1` hace que Trivy retorne codigo de error si encuentra vulnerabilidades, lo que causa que el stage falle.

#### Stage Quality Gate

Unifica todos los umbrales de seguridad y decide si el pipeline continua.

```groovy
stage('Quality Gate') {
    steps {
        script {
            def banditReport = readJSON file: 'bandit-report.json'
            def highCount = banditReport.results.count { it.issue_severity == 'HIGH' }
            if (highCount > 0) {
                error "Quality Gate fallo: $highCount vulnerabilidades HIGH encontradas"
            }
        }
    }
}
```

---

### 6. Jenkinsfile Completo con Seguridad

```groovy
pipeline {
    agent any

    tools {
        maven 'Maven-3.9'
        jdk 'JDK-17'
    }

    environment {
        DOCKER_IMAGE = 'myapp:latest'
        DOCKER_HUB_REPO = 'dockerhubuser/myapp'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/student/myapp.git'
            }
        }

        stage('Lint') {
            steps {
                sh 'flake8 . --max-line-length=120'
            }
        }

        stage('Unit Tests') {
            steps {
                sh 'python -m pytest tests/ --junitxml=report.xml'
            }
            post {
                always {
                    junit 'report.xml'
                }
            }
        }

        stage('SAST - Bandit') {
            steps {
                sh 'bandit -r src/ -f json -o bandit-report.json'
            }
            post {
                always {
                    publishHTML(target: [
                        reportName: 'Bandit SAST',
                        reportDir: '.',
                        reportFiles: 'bandit-report.json'
                    ])
                }
                failure {
                    error 'SAST encontro vulnerabilidades criticas. Pipeline detenido.'
                }
            }
        }

        stage('SCA - Safety') {
            steps {
                sh 'safety check -r requirements.txt --json > safety-report.json'
            }
            post {
                failure {
                    error 'Se encontraron dependencias con vulnerabilidades criticas'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $DOCKER_IMAGE .'
            }
        }

        stage('Container Scan - Trivy') {
            steps {
                sh 'trivy image --severity=CRITICAL --exit-code 1 $DOCKER_IMAGE'
            }
        }

        stage('Deploy to Dev') {
            steps {
                sh 'docker-compose -f docker-compose.dev.yml up -d'
            }
        }
    }

    post {
        always {
            cleanWs()
        }
        success {
            echo 'Pipeline completado exitosamente con todos los gates de seguridad'
        }
        failure {
            echo 'Pipeline fallo - revisar reportes de seguridad'
        }
    }
}
```

**Explicacion de cada stage:**

| Stage | Funcion | Importancia |
|-------|---------|-------------|
| Checkout | Trae el codigo del repositorio | Base de todo el pipeline |
| Lint | Verifica estilo de codigo | Previene errores y mejora mantenibilidad |
| Unit Tests | Ejecuta pruebas unitarias | Garantiza que el codigo funciona correctamente |
| SAST - Bandit | Busca vulnerabilidades en el codigo fuente | Detecta inyecciones, hardcodeo de secrets, etc. |
| SCA - Safety | Busca vulnerabilidades en dependencias | Evita librerias con CVEs conocidos |
| Build Docker Image | Construye la imagen del contenedor | Prepara el artefacto para deploy |
| Container Scan | Escanea la imagen con Trivy | Detecta vulnerabilidades en paquetes del SO |
| Deploy to Dev | Despliega en entorno de desarrollo | Entrega continua automatizada |

---

### 7. Blue Ocean

Blue Ocean es una interfaz grafica moderna para Jenkins que simplifica la visualizacion de pipelines.

**Instalacion:** Manage Jenkins -> Plugins -> buscar "Blue Ocean" -> instalar.

**Caracteristicas:**
- Visualizacion grafica de pipelines (cada stage se ve como un bloque de colores).
- Logs en tiempo real por stage.
- Diagnostico visual: los stages en rojo indican fallo, en verde exito.
- Editor visual de pipelines (arrastrar y soltar).
- Integracion con GitHub y GitLab para Pull Request checks.

**Uso:** una vez instalado, hacer clic en "Open Blue Ocean" en el menu lateral de Jenkins.

---

### 8. Integracion con GitHub/GitLab

#### Webhooks

Los webhooks permiten que Jenkins se ejecute automaticamente cuando ocurre un evento en el repositorio (push, pull request).

**Configuracion en GitHub:**
1. Repositorio -> Settings -> Webhooks -> Add webhook.
2. Payload URL: `http://jenkins:8080/github-webhook/`.
3. Content type: `application/json`.
4. Events: "Just the push event" (o seleccionar eventos especificos).

**Configuracion en Jenkins:**
1. Instalar plugin "GitHub Integration".
2. Configure el job como "GitHub project" y pegue la URL del repositorio.
3. En Build Triggers, marcar "GitHub hook trigger for GITScm polling".

#### Multibranch Pipeline

Detecta automaticamente las ramas del repositorio y crea un pipeline para cada una.

**Configuracion:**
1. New Item -> Multibranch Pipeline.
2. Branch Sources: agregar Git y pegar la URL del repositorio.
3. Scan credentials: agregar credenciales si es privado.
4. Build Configuration: por defecto usa el Jenkinsfile en la raiz.

**Ventajas:**
- Pipeline automatico para cada branch.
- Los Pull Requests aparecen como pipelines separados.
- Se puede configurar comportamiento especifico por branch.

---

### 9. Hardening de Jenkins

#### Usar HTTPS

Configurar un proxy reverso con nginx + Let's Encrypt para servir Jenkins por HTTPS:

```nginx
server {
    listen 443 ssl;
    server_name jenkins.midominio.com;

    ssl_certificate /etc/letsencrypt/live/jenkins.midominio.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/jenkins.midominio.com/privkey.pem;

    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

#### Control de Acceso

- Usar "Matrix-based security" en Manage Jenkins -> Configure Global Security.
- Asignar permisos minimos por rol (admin, developer, viewer).
- Integrar con LDAP o GitHub OAuth para autenticacion centralizada.

#### Agentes Efimeros

Usar contenedores Docker como agentes para que cada job se ejecute en un entorno limpio y desechable:

```groovy
pipeline {
    agent {
        docker {
            image 'python:3.11'
            args '-v /var/run/docker.sock:/var/run/docker.sock'
        }
    }
    stages {
        stage('Test') {
            steps {
                sh 'python --version'
            }
        }
    }
}
```

#### Buenas Practicas

| Practica | Descripcion |
|----------|-------------|
| Actualizar Jenkins y plugins | Aplicar parches de seguridad regularmente |
| No hardcodear credenciales | Usar el sistema de Credentials de Jenkins |
| Auditar logs | Revisar logs de acceso periodicamente |
| Backup de jenkins_home | Respaldar configuracion y plugins |
| Usar agentes separados | Aislar el master de los jobs |
| Restringir plugins | Solo instalar plugins necesarios |

---

### 10. Ejercicio 1 - Instalar Jenkins con Docker

**Enunciado:**
Instalar Jenkins usando Docker, configurar los plugins iniciales y crear el primer usuario administrador.

**Solucion paso a paso:**

Paso 1: Crear un volumen persistente y ejecutar el contenedor.

```bash
docker volume create jenkins_home

docker run -d --name jenkins \
  -p 8080:8080 -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  jenkins/jenkins:lts-jdk17
```

Paso 2: Obtener la contrasena inicial.

```bash
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

Paso 3: Acceder a `http://localhost:8080`, pegar la contrasena.

Paso 4: En el asistente, seleccionar "Install suggested plugins". Esperar a que se complete la instalacion.

Paso 5: Crear el usuario administrador:
- Username: `admin`
- Password: `Admin123!` (usar una contrasena segura en produccion)
- Full name: `Administrador`
- E-mail: `admin@example.com`

Paso 6: Configurar la URL de Jenkins (http://localhost:8080) y hacer clic en "Save and Finish".

Paso 7: Instalar plugins adicionales:
1. Manage Jenkins -> Plugins -> Available Plugins.
2. Buscar e instalar: Blue Ocean, Docker Pipeline, HTML Publisher, OWASP Dependency-Check.

Paso 8: Verificar la instalacion.
```bash
docker ps --filter name=jenkins
curl -I http://localhost:8080
```

---

### 11. Ejercicio 2 - Crear Pipeline Simple

**Enunciado:**
Crear un Jenkinsfile para una aplicacion Python Flask que realice:
1. Checkout del repositorio.
2. Instalar dependencias (pip install).
3. Ejecutar tests (pytest).
4. Ejecutar linting (flake8).
5. Ejecutar SAST (bandit).
6. Ejecutar SCA (safety).
7. Construir imagen Docker.
8. Escanear imagen con Trivy (fallar si hay CRITICAL).
9. Subir imagen a Docker Hub.

**Solucion:**

Crear el archivo `Jenkinsfile` en la raiz del proyecto:

```groovy
pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'my-flask-app:latest'
        DOCKER_HUB_REPO = 'dockerhubuser/my-flask-app'
        DOCKER_TAG = "${BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/student/flask-app.git', branch: 'main'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'python -m venv venv'
                sh '. venv/bin/activate && pip install -r requirements.txt'
            }
        }

        stage('Lint - Flake8') {
            steps {
                sh '. venv/bin/activate && flake8 . --max-line-length=120 --exclude=venv'
            }
        }

        stage('Unit Tests - Pytest') {
            steps {
                sh '. venv/bin/activate && python -m pytest tests/ --junitxml=report.xml'
            }
            post {
                always {
                    junit 'report.xml'
                }
            }
        }

        stage('SAST - Bandit') {
            steps {
                sh '. venv/bin/activate && bandit -r src/ -f json -o bandit-report.json'
            }
            post {
                always {
                    archiveArtifacts artifacts: 'bandit-report.json'
                }
                failure {
                    error 'SAST: Se encontraron vulnerabilidades en el codigo'
                }
            }
        }

        stage('SCA - Safety') {
            steps {
                sh '. venv/bin/activate && safety check -r requirements.txt --json > safety-report.json'
            }
            post {
                failure {
                    error 'SCA: Se encontraron dependencias con vulnerabilidades conocidas'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $DOCKER_IMAGE .'
            }
        }

        stage('Container Scan - Trivy') {
            steps {
                sh 'trivy image --severity=CRITICAL --exit-code 1 $DOCKER_IMAGE'
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'docker-hub-credentials',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh """
                        echo \$DOCKER_PASS | docker login -u \$DOCKER_USER --password-stdin
                        docker tag \$DOCKER_IMAGE \$DOCKER_HUB_REPO:\$DOCKER_TAG
                        docker tag \$DOCKER_IMAGE \$DOCKER_HUB_REPO:latest
                        docker push \$DOCKER_HUB_REPO:\$DOCKER_TAG
                        docker push \$DOCKER_HUB_REPO:latest
                    """
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
        success {
            echo 'Pipeline ejecutado exitosamente. Imagen publicada en Docker Hub.'
        }
        failure {
            echo 'Pipeline fallo. Revisar los reportes de seguridad.'
        }
    }
}
```

**Crear el job en Jenkins:**
1. New Item -> Pipeline.
2. Nombre: `flask-app-secure-pipeline`.
3. Pipeline definition: "Pipeline script from SCM".
4. SCM: Git, pegar la URL del repositorio.
5. Script Path: `Jenkinsfile`.
6. Guardar y ejecutar.

---

### 12. Ejercicio 3 - Pipeline con Quality Gates

**Enunciado:**
Modificar el Jenkinsfile anterior para que:
- Falle si Bandit encuentra vulnerabilidades HIGH o CRITICAL.
- Falle si Safety encuentra cualquier vulnerabilidad.
- Falle si Trivy encuentra CRITICAL en la imagen.
- Envie notificacion por email en caso de fallo.

**Solucion:**

```groovy
pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'my-flask-app:latest'
        DOCKER_HUB_REPO = 'dockerhubuser/my-flask-app'
        DOCKER_TAG = "${BUILD_NUMBER}"
        RECIPIENT_EMAIL = 'equipo-seguridad@example.com'
    }

    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/student/flask-app.git', branch: 'main'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'python -m venv venv'
                sh '. venv/bin/activate && pip install -r requirements.txt'
            }
        }

        stage('Lint') {
            steps {
                sh '. venv/bin/activate && flake8 . --max-line-length=120 --exclude=venv'
            }
        }

        stage('Unit Tests') {
            steps {
                sh '. venv/bin/activate && python -m pytest tests/ --junitxml=report.xml'
            }
            post {
                always {
                    junit 'report.xml'
                }
            }
        }

        stage('SAST - Bandit') {
            steps {
                script {
                    sh '. venv/bin/activate && bandit -r src/ -f json -o bandit-report.json'

                    def report = readJSON file: 'bandit-report.json'
                    def highCriticalIssues = report.results.findAll { result ->
                        result.issue_severity in ['HIGH', 'CRITICAL']
                    }

                    if (highCriticalIssues.size() > 0) {
                        echo "Vulnerabilidades HIGH/CRITICAL encontradas: ${highCriticalIssues.size()}"
                        for (issue in highCriticalIssues) {
                            echo "  - ${issue.filename}:${issue.line_number} - ${issue.issue_text}"
                        }
                        error "Quality Gate fallo: ${highCriticalIssues.size()} vulnerabilidades HIGH/CRITICAL en SAST"
                    } else {
                        echo "SAST: Sin vulnerabilidades HIGH o CRITICAL. Continuando..."
                    }
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: 'bandit-report.json'
                }
            }
        }

        stage('SCA - Safety') {
            steps {
                script {
                    sh '. venv/bin/activate && safety check -r requirements.txt --json > safety-report.json'

                    def report = readJSON file: 'safety-report.json'
                    if (report.size() > 0) {
                        echo "Vulnerabilidades encontradas en dependencias: ${report.size()}"
                        error "Quality Gate fallo: ${report.size()} vulnerabilidades en dependencias"
                    } else {
                        echo "SCA: Sin vulnerabilidades en dependencias. Continuando..."
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $DOCKER_IMAGE .'
            }
        }

        stage('Container Scan - Trivy') {
            steps {
                script {
                    try {
                        sh 'trivy image --severity=CRITICAL --exit-code 1 $DOCKER_IMAGE'
                    } catch (Exception e) {
                        error "Quality Gate fallo: Trivy encontro vulnerabilidades CRITICAL en la imagen"
                    }
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'docker-hub-credentials',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh """
                        echo \$DOCKER_PASS | docker login -u \$DOCKER_USER --password-stdin
                        docker tag \$DOCKER_IMAGE \$DOCKER_HUB_REPO:\$DOCKER_TAG
                        docker tag \$DOCKER_IMAGE \$DOCKER_HUB_REPO:latest
                        docker push \$DOCKER_HUB_REPO:\$DOCKER_TAG
                        docker push \$DOCKER_HUB_REPO:latest
                    """
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
        success {
            echo 'Pipeline completado exitosamente con todos los quality gates superados.'
        }
        failure {
            script {
                echo 'Pipeline fallo. Enviando notificacion por email...'

                def subject = "[Jenkins] Pipeline ${env.JOB_NAME} #${env.BUILD_NUMBER} FALLO"
                def body = """
                    <h2>Pipeline Fallo - Quality Gate no Superado</h2>
                    <p><strong>Job:</strong> ${env.JOB_NAME}</p>
                    <p><strong>Build:</strong> #${env.BUILD_NUMBER}</p>
                    <p><strong>URL:</strong> ${env.BUILD_URL}</p>
                    <p><strong>Estado:</strong> ${currentBuild.currentResult}</p>
                    <p>Revisar los reportes de seguridad adjuntos al build.</p>
                """

                mail(
                    to: env.RECIPIENT_EMAIL,
                    subject: subject,
                    body: body,
                    mimeType: 'text/html'
                )
            }
        }
    }
}
```

---

### 13. Ejercicio 4 - Multibranch Pipeline

**Enunciado:**
Configurar un Multibranch Pipeline en Jenkins que escanee el repositorio y cree pipelines para cada branch con PR checks.

**Solucion:**

#### Configuracion en Jenkins UI

1. En el panel de Jenkins, hacer clic en **New Item**.
2. Ingresar nombre: `flask-app-multibranch`.
3. Seleccionar **Multibranch Pipeline**.
4. Hacer clic en **OK**.

**Configurar Branch Sources:**
1. En "Branch Sources", hacer clic en "Add source" y seleccionar "Git".
2. Project Repository: `https://github.com/student/flask-app.git`.
3. Credentials: agregar credencial si el repositorio es privado.

**Configurar Scan:**
1. "Scan Multibranch Pipeline Triggers": marcar "Periodically if not otherwise run".
2. Intervalo: `1 minute`.
3. "Discover branches": "All branches".
4. "Discover pull requests from origin": "Merging the pull request with the current target branch revision".

**Build Configuration:**
1. "Mode": "by Jenkinsfile".
2. "Script Path": `Jenkinsfile`.

#### Jenkinsfile con soporte para branches y PRs

```groovy
pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "flask-app:${BRANCH_NAME}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'python -m venv venv'
                sh '. venv/bin/activate && pip install -r requirements.txt'
            }
        }

        stage('Lint') {
            when {
                expression { env.BRANCH_NAME == 'main' }
            }
            steps {
                sh '. venv/bin/activate && flake8 . --max-line-length=120 --exclude=venv'
            }
        }

        stage('Unit Tests') {
            steps {
                sh '. venv/bin/activate && python -m pytest tests/ --junitxml=report.xml'
            }
            post {
                always {
                    junit 'report.xml'
                }
            }
        }

        stage('SAST - Bandit') {
            when {
                expression { env.BRANCH_NAME == 'main' }
            }
            steps {
                sh '. venv/bin/activate && bandit -r src/ -f json -o bandit-report.json'
            }
            post {
                always {
                    archiveArtifacts artifacts: 'bandit-report.json'
                }
            }
        }

        stage('Build Docker Image') {
            when {
                expression { env.BRANCH_NAME == 'main' }
            }
            steps {
                sh 'docker build -t $DOCKER_IMAGE .'
            }
        }

        stage('Deploy to Dev') {
            when {
                branch 'main'
            }
            steps {
                sh 'docker-compose -f docker-compose.dev.yml up -d'
            }
        }

        stage('PR Comment') {
            when {
                changeRequest()
            }
            steps {
                echo "Pull Request #${CHANGE_ID} - Analisis completado"
                sh "echo 'Tests y analisis completados para PR #${CHANGE_ID}'"
            }
        }
    }

    post {
        always {
            cleanWs()
        }
        failure {
            script {
                if (env.CHANGE_ID) {
                    echo "PR #${CHANGE_ID} fallo - revisar detalles"
                }
            }
        }
    }
}
```

**Funcionamiento:**
- Cada branch en el repositorio crea automaticamente un pipeline.
- Los Pull Requests son detectados y se ejecuta el pipeline correspondiente.
- Los stages de linting, SAST y deploy solo se ejecutan en `main` usando `when`.
- El stage `PR Comment` se ejecuta solo cuando es un Pull Request (`changeRequest()`).

---

### 14. Ejercicio 5 - Pipeline Desplegando con docker-compose

**Enunciado:**
Pipeline completo que:
- Construya la app.
- Ejecute tests y analisis de seguridad.
- Construya imagen Docker.
- Despliegue con docker-compose en servidor dev (via SSH).

**Solucion:**

#### Jenkinsfile

```groovy
pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'myapp:latest'
        DEV_SERVER = 'dev-admin@192.168.1.100'
        SSH_KEY = 'ssh-key-dev-server'
    }

    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/student/myapp.git', branch: 'main'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'python -m venv venv'
                sh '. venv/bin/activate && pip install -r requirements.txt'
            }
        }

        stage('Lint') {
            steps {
                sh '. venv/bin/activate && flake8 . --max-line-length=120 --exclude=venv'
            }
        }

        stage('Tests') {
            steps {
                sh '. venv/bin/activate && python -m pytest tests/ --junitxml=report.xml'
            }
            post {
                always {
                    junit 'report.xml'
                }
            }
        }

        stage('SAST - Bandit') {
            steps {
                sh '. venv/bin/activate && bandit -r src/ -f json -o bandit-report.json'
            }
            post {
                always {
                    archiveArtifacts artifacts: 'bandit-report.json'
                }
            }
        }

        stage('SCA - Safety') {
            steps {
                sh '. venv/bin/activate && safety check -r requirements.txt --json > safety-report.json'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $DOCKER_IMAGE .'
            }
        }

        stage('Container Scan - Trivy') {
            steps {
                sh 'trivy image --severity=CRITICAL --exit-code 1 $DOCKER_IMAGE'
            }
        }

        stage('Deploy via SSH') {
            steps {
                script {
                    sh """
                        docker save \$DOCKER_IMAGE | gzip > myapp.tar.gz
                    """

                    withCredentials([sshUserPrivateKey(
                        credentialsId: SSH_KEY,
                        keyFileVariable: 'SSH_KEY_FILE',
                        usernameVariable: 'SSH_USER'
                    )]) {
                        sh """
                            scp -i \$SSH_KEY_FILE -o StrictHostKeyChecking=no \
                                docker-compose.dev.yml \
                                myapp.tar.gz \
                                $DEV_SERVER:/opt/myapp/

                            ssh -i \$SSH_KEY_FILE -o StrictHostKeyChecking=no \
                                $DEV_SERVER \
                                'cd /opt/myapp && \
                                 gunzip -c myapp.tar.gz | docker load && \
                                 docker-compose -f docker-compose.dev.yml up -d'
                        """
                    }

                    sh 'rm myapp.tar.gz'
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
        success {
            echo 'Despliegue completado exitosamente en servidor de desarrollo.'
        }
        failure {
            echo 'El despliegue fallo. Revisar logs y reportes de seguridad.'
        }
    }
}
```

#### Archivo docker-compose.dev.yml

```yaml
version: '3.8'

services:
  app:
    image: myapp:latest
    container_name: myapp-dev
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=development
      - DATABASE_URL=postgresql://user:pass@db:5432/myapp
    depends_on:
      - db
    restart: unless-stopped

  db:
    image: postgres:15-alpine
    container_name: myapp-db-dev
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=myapp
    volumes:
      - pgdata:/var/lib/postgresql/data
    restart: unless-stopped

volumes:
  pgdata:
```

#### Script de deploy alternativo (deploy.sh)

```bash
#!/bin/bash
# deploy.sh - Script para desplegar en servidor remoto
# Uso: ./deploy.sh <imagen> <servidor> <archivo_compose>

set -euo pipefail

IMAGE="${1:-myapp:latest}"
SERVER="${2:-dev-admin@192.168.1.100}"
COMPOSE_FILE="${3:-docker-compose.dev.yml}"
SSH_KEY="${SSH_KEY:-/opt/jenkins/.ssh/id_rsa}"

echo "=== Iniciando despliegue ==="

echo "Comprimiendo imagen Docker..."
docker save "$IMAGE" | gzip > /tmp/myapp-deploy.tar.gz

echo "Transfiriendo archivos al servidor..."
scp -i "$SSH_KEY" -o StrictHostKeyChecking=no \
    "$COMPOSE_FILE" \
    /tmp/myapp-deploy.tar.gz \
    "$SERVER:/opt/myapp/"

echo "Desplegando en servidor remoto..."
ssh -i "$SSH_KEY" -o StrictHostKeyChecking=no \
    "$SERVER" \
    "cd /opt/myapp && \
     gunzip -c myapp-deploy.tar.gz | docker load && \
     docker-compose -f $COMPOSE_FILE up -d && \
     rm myapp-deploy.tar.gz && \
     echo 'Despliegue completado'"

echo "Limpiando archivos temporales..."
rm /tmp/myapp-deploy.tar.gz

echo "=== Despliegue exitoso ==="
```

---

### 15. Preguntas y Respuestas

**P1: Que es un Jenkinsfile?**

Es un archivo de texto ubicado en la raiz del repositorio que define un pipeline de Jenkins como codigo (Pipeline as Code). Escrito en Groovy, describe las etapas, pasos y condiciones del proceso de CI/CD. Al estar versionado junto con el codigo fuente, permite auditoria, reutilizacion y colaboracion.

---

**P2: Cual es la diferencia entre Declarative Pipeline y Scripted Pipeline?**

El Declarative Pipeline usa una sintaxis estructurada y predecible (bloques `pipeline`, `stages`, `stage`, `steps`) que es mas facil de leer y escribir, ideal para la mayoria de los casos. El Scripted Pipeline usa Groovy puro, lo que permite mayor flexibilidad y control, pero es mas complejo y propenso a errores. Se recomienda Declarative para proyectos nuevos.

---

**P3: Como se integra Jenkins con GitHub?**

Mediante webhooks. En GitHub se configura un webhook que apunta a la URL de Jenkins (`http://jenkins:8080/github-webhook/`). Cuando ocurre un push o pull request, GitHub envia una notificacion a Jenkins, que automaticamente dispara el pipeline correspondiente. Tambien se puede usar el plugin "GitHub Branch Source" para Multibranch Pipelines que escanean el repositorio periodicamente.

---

**P4: Para que sirve Blue Ocean?**

Blue Ocean es una interfaz grafica moderna para Jenkins que facilita la visualizacion de pipelines. Muestra cada stage como un bloque de colores (verde = exito, rojo = fallo), permite ver logs en tiempo real por stage, incluye un editor visual de pipelines y se integra con GitHub/GitLab para mostrar el estado de los Pull Requests directamente.

---

**P5: Como se manejan las credenciales en Jenkins?**

Jenkins cuenta con un sistema de Credentials Manager (Manage Jenkins -> Credentials) que almacena de forma segura tokens, claves SSH, usuarios y contrasenas. Las credenciales se referencian en los Jenkinsfiles mediante IDs unicos usando `withCredentials` o `credentials()`. Nunca se deben hardcodear credenciales en el Jenkinsfile ni en scripts.

```groovy
withCredentials([string(credentialsId: 'github-token', variable: 'TOKEN')]) {
    sh "curl -H 'Authorization: token $TOKEN' https://api.github.com/user"
}
```

---

**P6: Que es un quality gate en CI/CD?**

Un quality gate es un punto de control dentro del pipeline que verifica que el codigo cumple con umbrales minimos de calidad y seguridad. Si no se supera el quality gate, el pipeline se detiene y no se despliega. Ejemplos: numero maximo de vulnerabilidades SAST, cobertura de tests minima, ausencia de dependencias con CVEs criticos, etc. Los quality gates aseguran que solo codigo seguro y de calidad llegue a produccion.

---

**P7: Como se ejecuta un stage condicional (solo en main branch, solo en PR)?**

Usando el bloque `when` dentro del stage:

**Solo en main branch:**
```groovy
stage('Deploy') {
    when {
        branch 'main'
    }
    steps {
        sh 'deploy.sh'
    }
}
```

**Solo en Pull Request:**
```groovy
stage('PR Check') {
    when {
        changeRequest()
    }
    steps {
        echo "Ejecutando checks para PR #${CHANGE_ID}"
    }
}
```

**Condicion compuesta:**
```groovy
stage('Full Security Scan') {
    when {
        allOf {
            branch 'main'
            not { triggeredBy 'TimerTrigger' }
        }
    }
    steps {
        sh 'full-security-scan.sh'
    }
}
```

---

**P8: Que diferencia hay entre agent any y agent none en un pipeline declarativo?**

`agent any` ejecuta el pipeline en cualquier agente disponible, sin restricciones. `agent none` se aplica a nivel del pipeline raiz y requiere que cada stage defina su propio agent, lo que permite usar diferentes entornos para diferentes etapas (por ejemplo, un contenedor Python para tests y un contenedor Java para compilacion).

```groovy
pipeline {
    agent none
    stages {
        stage('Build') {
            agent { docker 'maven:3.9' }
            steps {
                sh 'mvn compile'
            }
        }
        stage('Test') {
            agent { docker 'python:3.11' }
            steps {
                sh 'python -m pytest'
            }
        }
    }
}
```

---

**P9: Como se publican reportes HTML en Jenkins?**

Usando el plugin HTML Publisher. En el bloque `post` del stage, se llama a `publishHTML` especificando el nombre del reporte, el directorio y el archivo:

```groovy
post {
    always {
        publishHTML(target: [
            reportName: 'Bandit Report',
            reportDir: '.',
            reportFiles: 'bandit-report.json'
        ])
    }
}
```

Los reportes quedan accesibles desde la pagina del build en Jenkins.

---

**P10: Que es un Multibranch Pipeline y que ventajas tiene?**

Es un tipo de proyecto en Jenkins que detecta automaticamente las ramas de un repositorio y crea un pipeline para cada una. Ventajas:
- No requiere crear un job por cada branch.
- Los Pull Requests se detectan y ejecutan automaticamente.
- Cada branch tiene su propio historial de builds.
- Se puede configurar comportamiento diferente por branch usando `when { branch '...' }`.
- Facilita la integracion con estrategias GitFlow o trunk-based development.

---

## Tarea Recomendada

1. **Instalar Jenkins con Docker** siguiendo los pasos del Ejercicio 1. Configurar al menos 5 plugins de seguridad.

2. **Crear un pipeline para un proyecto propio** (puede ser un fork de un proyecto open-source simple) que incluya:
   - Linting (flake8 para Python, ESLint para JS, etc.).
   - Tests automatizados.
   - Un stage SAST (Bandit para Python, ESLint security para JS, etc.).
   - Un stage SCA (Safety para Python, npm audit para JS, etc.).
   - Un quality gate que detenga el pipeline si se superan los umbrales definidos.

3. **Configurar un webhook de GitHub** para que el pipeline se ejecute automaticamente al hacer push a la rama main.

4. **Agregar un stage de despliegue** que suba una imagen Docker a Docker Hub (usando credenciales de Jenkins, no hardcodeadas).

5. **Leer la documentacion oficial** sobre hardening de Jenkins en:
   - https://www.jenkins.io/doc/book/security/
   - https://www.jenkins.io/doc/administration/security/

6. **Crear un script de hardening** automatizado que ejecute las siguientes acciones:
   - Forzar HTTPS.
   - Deshabilitar usuarios anonimos.
   - Configurar tiempo de sesion maximo.
   - Activar logs de auditoria.

**Entrega:** Jenkinsfile completo del pipeline creado, captura de pantalla del pipeline ejecutado exitosamente en Blue Ocean, y un breve informe (200-300 palabras) explicando las medidas de seguridad implementadas en cada stage.
