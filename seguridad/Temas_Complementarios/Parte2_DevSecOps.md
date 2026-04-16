# CURSO COMPLETO DE CIBERSEGURIDAD - PARTE 3

## MÓDULO 5: HERRAMIENTAS AVANZADAS Y DEVSECOPS

### 5.1 Trivy - Escaneo de Vulnerabilidades en Contenedores

**Definición:** Escáner de seguridad para contenedores, imágenes, sistemas de archivos y repositorios Git.

#### Instalación

```bash
# Ubuntu/Debian
sudo apt-get install wget apt-transport-https gnupg lsb-release
wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | sudo apt-key add -
echo "deb https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main" | sudo tee -a /etc/apt/sources.list.d/trivy.list
sudo apt-get update
sudo apt-get install trivy

# macOS
brew install trivy

# Docker
docker pull aquasec/trivy
```

#### Ejemplos Prácticos

```bash
# Escanear imagen de Docker
trivy image nginx:latest

# Escanear solo vulnerabilidades CRITICAL y HIGH
trivy image --severity CRITICAL,HIGH nginx:latest

# Escanear imagen local
docker build -t mi-app:latest .
trivy image mi-app:latest

# Escanear sistema de archivos
trivy fs /ruta/al/proyecto

# Escanear repositorio Git remoto
trivy repo https://github.com/usuario/proyecto

# Generar reporte en JSON
trivy image --format json --output reporte.json nginx:latest

# Generar reporte en HTML
trivy image --format template --template "@contrib/html.tpl" \
  --output reporte.html nginx:latest
```

---

### 5.2 LABORATORIO COMPLETO: Jenkins con Docker y Trivy

Este laboratorio te enseñará a configurar un pipeline CI/CD seguro con escaneo automático de vulnerabilidades.

#### Paso 1: Preparar el entorno

```bash
# Crear directorio del proyecto
mkdir jenkins-security-lab
cd jenkins-security-lab

# Crear red Docker
docker network create jenkins-network
```

#### Paso 2: Crear aplicación de ejemplo

```bash
# Crear Dockerfile vulnerable
cat > Dockerfile << 'EOF'
# Imagen base antigua (vulnerable)
FROM node:14.17.0

WORKDIR /app

# Copiar archivos
COPY package.json .
COPY app.js .

# Instalar dependencias
RUN npm install

EXPOSE 3000

CMD ["node", "app.js"]
EOF

# Crear aplicación Node.js simple
cat > app.js << 'EOF'
const express = require('express');
const app = express();

app.get('/', (req, res) => {
  res.send('¡Hola desde la aplicación vulnerable!');
});

app.listen(3000, () => {
  console.log('Servidor corriendo en puerto 3000');
});
EOF

# Crear package.json con dependencias vulnerables
cat > package.json << 'EOF'
{
  "name": "app-vulnerable",
  "version": "1.0.0",
  "dependencies": {
    "express": "4.17.1"
  }
}
EOF
```

#### Paso 3: Levantar Jenkins con Docker

```bash
# Crear volumen para persistencia
docker volume create jenkins-data

# Levantar Jenkins
docker run -d \
  --name jenkins \
  --network jenkins-network \
  -p 8080:8080 \
  -p 50000:50000 \
  -v jenkins-data:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  jenkins/jenkins:lts

# Esperar a que Jenkins inicie (30-60 segundos)
sleep 60

# Obtener contraseña inicial
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

#### Paso 4: Configurar Jenkins

1. Abrir navegador en `http://localhost:8080`
2. Ingresar contraseña inicial
3. Instalar plugins sugeridos
4. Crear usuario admin

#### Paso 5: Instalar Trivy en Jenkins

```bash
# Entrar al contenedor de Jenkins
docker exec -it -u root jenkins bash

# Instalar Trivy dentro de Jenkins
apt-get update
apt-get install -y wget apt-transport-https gnupg lsb-release
wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | apt-key add -
echo "deb https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main" | tee -a /etc/apt/sources.list.d/trivy.list
apt-get update
apt-get install -y trivy

# Instalar Docker CLI
apt-get install -y docker.io

# Salir del contenedor
exit
```

#### Paso 6: Crear Pipeline de Jenkins

En Jenkins, crear nuevo item → Pipeline → Pegar este código:

```groovy
pipeline {
    agent any
    
    environment {
        IMAGE_NAME = 'app-vulnerable'
        IMAGE_TAG = 'latest'
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo 'Clonando código...'
                // En producción: git clone del repositorio
                sh 'echo "Código descargado"'
            }
        }
        
        stage('Build Docker Image') {
            steps {
                echo 'Construyendo imagen Docker...'
                script {
                    sh """
                        docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
                    """
                }
            }
        }
        
        stage('Security Scan - Trivy') {
            steps {
                echo 'Escaneando vulnerabilidades con Trivy...'
                script {
                    sh """
                        trivy image --severity HIGH,CRITICAL \
                          --format json \
                          --output trivy-report.json \
                          ${IMAGE_NAME}:${IMAGE_TAG}
                        
                        # Mostrar resumen
                        trivy image --severity HIGH,CRITICAL ${IMAGE_NAME}:${IMAGE_TAG}
                    """
                }
            }
        }
        
        stage('Quality Gate') {
            steps {
                echo 'Verificando umbral de seguridad...'
                script {
                    def trivyReport = readJSON file: 'trivy-report.json'
                    def criticalCount = 0
                    def highCount = 0
                    
                    trivyReport.Results.each { result ->
                        result.Vulnerabilities.each { vuln ->
                            if (vuln.Severity == 'CRITICAL') {
                                criticalCount++
                            } else if (vuln.Severity == 'HIGH') {
                                highCount++
                            }
                        }
                    }
                    
                    echo "Vulnerabilidades CRITICAL: ${criticalCount}"
                    echo "Vulnerabilidades HIGH: ${highCount}"
                    
                    // Fallar si hay vulnerabilidades críticas
                    if (criticalCount > 0) {
                        error("Build fallido: Se encontraron ${criticalCount} vulnerabilidades CRITICAL")
                    }
                    
                    // Advertir si hay muchas HIGH
                    if (highCount > 10) {
                        unstable("Build inestable: Se encontraron ${highCount} vulnerabilidades HIGH")
                    }
                }
            }
        }
        
        stage('Deploy') {
            when {
                expression { currentBuild.result == null || currentBuild.result == 'SUCCESS' }
            }
            steps {
                echo 'Desplegando aplicación...'
                sh """
                    docker stop app-vulnerable || true
                    docker rm app-vulnerable || true
                    docker run -d --name app-vulnerable -p 3000:3000 ${IMAGE_NAME}:${IMAGE_TAG}
                """
            }
        }
    }
    
    post {
        always {
            echo 'Limpiando workspace...'
            archiveArtifacts artifacts: 'trivy-report.json', allowEmptyArchive: true
        }
        success {
            echo '✓ Pipeline completado exitosamente'
        }
        failure {
            echo '✗ Pipeline falló - revisar vulnerabilidades'
        }
    }
}
```

#### Paso 7: Ejecutar el Pipeline

1. Guardar el pipeline
2. Hacer clic en "Build Now"
3. Ver consola de salida

**Resultado esperado:** El build fallará debido a vulnerabilidades críticas en la imagen base antigua.

#### Paso 8: Remediar vulnerabilidades

```bash
# Actualizar Dockerfile con imagen más reciente
cat > Dockerfile << 'EOF'
# Imagen base actualizada
FROM node:18-alpine

WORKDIR /app

# Copiar archivos
COPY package.json .
COPY app.js .

# Instalar dependencias
RUN npm install

# Usuario no privilegiado
RUN addgroup -g 1001 -S nodejs && adduser -S nodejs -u 1001
USER nodejs

EXPOSE 3000

CMD ["node", "app.js"]
EOF

# Actualizar dependencias
cat > package.json << 'EOF'
{
  "name": "app-segura",
  "version": "1.0.0",
  "dependencies": {
    "express": "^4.18.2"
  }
}
EOF
```

#### Paso 9: Ejecutar nuevamente

Hacer clic en "Build Now" → Ahora debería pasar el quality gate.

---

### 5.3 SonarQube - Análisis de Código Estático

#### Levantar SonarQube con Docker

```bash
# Crear red
docker network create sonar-network

# Levantar PostgreSQL
docker run -d \
  --name sonarqube-db \
  --network sonar-network \
  -e POSTGRES_USER=sonar \
  -e POSTGRES_PASSWORD=sonar \
  -e POSTGRES_DB=sonarqube \
  postgres:13

# Levantar SonarQube
docker run -d \
  --name sonarqube \
  --network sonar-network \
  -p 9000:9000 \
  -e SONAR_JDBC_URL=jdbc:postgresql://sonarqube-db:5432/sonarqube \
  -e SONAR_JDBC_USERNAME=sonar \
  -e SONAR_JDBC_PASSWORD=sonar \
  sonarqube:community

# Esperar inicio (2-3 minutos)
# Acceder a http://localhost:9000
# Usuario: admin / Contraseña: admin
```

#### Analizar proyecto Java

```bash
# Crear proyecto Java vulnerable
mkdir java-vulnerable-app
cd java-vulnerable-app

# Crear código vulnerable
cat > VulnerableApp.java << 'EOF'
import java.sql.*;
import java.util.Scanner;

public class VulnerableApp {
    // Contraseña hardcodeada (VULNERABILIDAD)
    private static final String DB_PASSWORD = "admin123";
    
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Ingrese usuario: ");
        String usuario = scanner.nextLine();
        
        try {
            Connection conn = DriverManager.getConnection(
                "jdbc:mysql://localhost:3306/db", 
                "root", 
                DB_PASSWORD
            );
            
            // SQL Injection (VULNERABILIDAD)
            String query = "SELECT * FROM usuarios WHERE nombre='" + usuario + "'";
            Statement stmt = conn.createStatement();
            ResultSet rs = stmt.executeQuery(query);
            
            while (rs.next()) {
                System.out.println("Usuario encontrado: " + rs.getString("nombre"));
            }
            
            // Recurso no cerrado (VULNERABILIDAD)
            // conn.close();
            
        } catch (SQLException e) {
            // Información sensible en logs (VULNERABILIDAD)
            System.out.println("Error de BD: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
EOF

# Compilar
javac VulnerableApp.java

# Analizar con SonarQube Scanner
docker run --rm \
  --network sonar-network \
  -v $(pwd):/usr/src \
  sonarsource/sonar-scanner-cli \
  -Dsonar.projectKey=java-vulnerable \
  -Dsonar.sources=. \
  -Dsonar.host.url=http://sonarqube:9000 \
  -Dsonar.login=admin \
  -Dsonar.password=admin
```

#### Código Java corregido

```java
import java.sql.*;
import java.util.Scanner;
import java.util.Properties;
import java.io.FileInputStream;

public class SecureApp {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Ingrese usuario: ");
        String usuario = scanner.nextLine();
        
        // Leer configuración de archivo externo
        Properties props = new Properties();
        try (FileInputStream fis = new FileInputStream("config.properties")) {
            props.load(fis);
        } catch (Exception e) {
            System.err.println("Error cargando configuración");
            return;
        }
        
        // Usar try-with-resources para cerrar automáticamente
        try (Connection conn = DriverManager.getConnection(
                props.getProperty("db.url"),
                props.getProperty("db.user"),
                props.getProperty("db.password")
        )) {
            
            // Usar PreparedStatement para prevenir SQL Injection
            String query = "SELECT * FROM usuarios WHERE nombre = ?";
            try (PreparedStatement pstmt = conn.prepareStatement(query)) {
                pstmt.setString(1, usuario);
                
                try (ResultSet rs = pstmt.executeQuery()) {
                    while (rs.next()) {
                        System.out.println("Usuario encontrado: " + rs.getString("nombre"));
                    }
                }
            }
            
        } catch (SQLException e) {
            // Log genérico sin información sensible
            System.err.println("Error de base de datos");
            // En producción: usar logger apropiado
        }
    }
}
```

---

### 5.4 OWASP ZAP - Pruebas de Seguridad Dinámicas

#### Instalación y uso básico

```bash
# Levantar ZAP en Docker
docker run -u zap -p 8090:8090 \
  -v $(pwd):/zap/wrk/:rw \
  owasp/zap2docker-stable zap-webswing.sh

# Acceder a http://localhost:8090

# Escaneo desde línea de comandos
docker run --rm -t owasp/zap2docker-stable \
  zap-baseline.py -t https://ejemplo.com -r reporte.html
```

#### Crear aplicación web vulnerable para pruebas

```python
# app_vulnerable.py
from flask import Flask, request, render_template_string

app = Flask(__name__)

# Almacenamiento en memoria (no usar en producción)
usuarios = {'admin': 'admin123'}

@app.route('/')
def home():
    return '''
    <h1>Aplicación Vulnerable</h1>
    <a href="/login">Login</a><br>
    <a href="/search">Buscar</a>
    '''

# VULNERABILIDAD: SQL Injection simulada
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        password = request.form['password']
        
        # Simulación de SQL Injection
        query = f"SELECT * FROM usuarios WHERE usuario='{usuario}' AND password='{password}'"
        
        if usuario in usuarios and usuarios[usuario] == password:
            return f"<h2>Bienvenido {usuario}</h2>"
        elif "' OR '1'='1" in usuario:
            return "<h2>¡SQL Injection detectada! Acceso concedido</h2>"
        else:
            return "<h2>Credenciales inválidas</h2>"
    
    return '''
    <form method="post">
        Usuario: <input name="usuario"><br>
        Password: <input name="password" type="password"><br>
        <input type="submit" value="Login">
    </form>
    '''

# VULNERABILIDAD: XSS Reflejado
@app.route('/search')
def search():
    query = request.args.get('q', '')
    # No se escapa el HTML - vulnerable a XSS
    return render_template_string(f'''
    <h1>Resultados de búsqueda</h1>
    <p>Buscaste: {query}</p>
    <form>
        <input name="q" value="{query}">
        <input type="submit" value="Buscar">
    </form>
    ''')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

#### Ejecutar y escanear

```bash
# Instalar Flask
pip install flask

# Ejecutar aplicación
python app_vulnerable.py

# En otra terminal, escanear con ZAP
docker run --rm --network host owasp/zap2docker-stable \
  zap-full-scan.py -t http://localhost:5000 -r reporte_zap.html
```

---

### 5.5 Metasploit - Framework de Explotación

#### Instalación

```bash
# Ubuntu/Debian
curl https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb > msfinstall
chmod 755 msfinstall
./msfinstall

# Docker
docker pull metasploitframework/metasploit-framework
```

#### Laboratorio: Explotar vulnerabilidad conocida

```bash
# Levantar máquina vulnerable (Metasploitable2)
docker run -d --name metasploitable vulnerables/metasploit-vulnerable-apps

# Obtener IP del contenedor
docker inspect metasploitable | grep IPAddress

# Iniciar Metasploit
msfconsole

# Dentro de msfconsole:
# Buscar exploit para vsftpd (servicio FTP vulnerable)
msf6 > search vsftpd

# Usar exploit
msf6 > use exploit/unix/ftp/vsftpd_234_backdoor

# Configurar target
msf6 exploit(vsftpd_234_backdoor) > set RHOSTS 172.17.0.2

# Ejecutar exploit
msf6 exploit(vsftpd_234_backdoor) > exploit

# Si es exitoso, obtendrás shell en la máquina vulnerable
```

---

### 5.6 Burp Suite - Proxy de Interceptación

#### Configuración básica

1. Descargar Burp Suite Community de portswigger.net
2. Ejecutar: `java -jar burpsuite_community.jar`
3. Configurar navegador para usar proxy 127.0.0.1:8080
4. Instalar certificado CA de Burp en el navegador

#### Laboratorio: Interceptar y modificar peticiones

```bash
# Levantar aplicación de prueba
python app_vulnerable.py

# En Burp Suite:
# 1. Ir a Proxy → Intercept → Intercept is on
# 2. En navegador, ir a http://localhost:5000/login
# 3. Ingresar credenciales y enviar
# 4. En Burp, verás la petición interceptada
# 5. Modificar parámetros (ej: cambiar precio de producto)
# 6. Forward para enviar petición modificada
```

---

## MÓDULO 6: SEGURIDAD EN BASES DE DATOS

### 6.1 PostgreSQL - Configuración Segura

#### Instalación y hardening

```bash
# Instalar PostgreSQL
sudo apt install postgresql postgresql-contrib

# Configurar autenticación (/etc/postgresql/14/main/pg_hba.conf)
sudo nano /etc/postgresql/14/main/pg_hba.conf

# Cambiar de 'trust' a 'md5' o 'scram-sha-256'
# local   all   all   scram-sha-256
# host    all   all   127.0.0.1/32   scram-sha-256

# Configurar PostgreSQL (/etc/postgresql/14/main/postgresql.conf)
sudo nano /etc/postgresql/14/main/postgresql.conf

# Configuraciones de seguridad:
listen_addresses = 'localhost'  # Solo conexiones locales
ssl = on  # Habilitar SSL
password_encryption = scram-sha-256  # Cifrado fuerte
log_connections = on  # Auditoría
log_disconnections = on
log_statement = 'all'  # Registrar todas las consultas

# Reiniciar servicio
sudo systemctl restart postgresql
```

#### Cifrado de datos sensibles

```sql
-- Instalar extensión pgcrypto
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Crear tabla con datos sensibles
CREATE TABLE pacientes (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    ci_cifrado BYTEA,  -- Cédula cifrada
    diagnostico_cifrado BYTEA  -- Diagnóstico cifrado
);

-- Insertar datos cifrados
INSERT INTO pacientes (nombre, ci_cifrado, diagnostico_cifrado)
VALUES (
    'Juan Pérez',
    pgp_sym_encrypt('12345678', 'clave_maestra_segura'),
    pgp_sym_encrypt('Diabetes tipo 2', 'clave_maestra_segura')
);

-- Consultar datos descifrados (solo con clave correcta)
SELECT 
    nombre,
    pgp_sym_decrypt(ci_cifrado, 'clave_maestra_segura') AS ci,
    pgp_sym_decrypt(diagnostico_cifrado, 'clave_maestra_segura') AS diagnostico
FROM pacientes;

-- Cifrado a nivel de columna con clave diferente por registro
CREATE TABLE usuarios_sensibles (
    id SERIAL PRIMARY KEY,
    email VARCHAR(100),
    tarjeta_credito_cifrada BYTEA,
    clave_individual VARCHAR(64)  -- Hash de clave única por usuario
);
```

#### Control de acceso granular (RBAC)

```sql
-- Crear roles
CREATE ROLE medico;
CREATE ROLE enfermero;
CREATE ROLE administrativo;

-- Permisos para médico (acceso completo)
GRANT SELECT, INSERT, UPDATE ON pacientes TO medico;

-- Permisos para enfermero (solo lectura y actualización)
GRANT SELECT, UPDATE ON pacientes TO enfermero;

-- Permisos para administrativo (solo datos no sensibles)
CREATE VIEW pacientes_publico AS
SELECT id, nombre FROM pacientes;

GRANT SELECT ON pacientes_publico TO administrativo;

-- Crear usuarios y asignar roles
CREATE USER dr_garcia WITH PASSWORD 'password_seguro';
GRANT medico TO dr_garcia;

-- Row Level Security (RLS)
ALTER TABLE pacientes ENABLE ROW LEVEL SECURITY;

-- Política: cada médico solo ve sus pacientes
CREATE POLICY medico_ve_sus_pacientes ON pacientes
    FOR SELECT
    TO medico
    USING (medico_asignado = current_user);
```

---

### 6.2 MongoDB - Seguridad NoSQL

#### Configuración segura

```bash
# Instalar MongoDB
sudo apt install mongodb

# Habilitar autenticación (/etc/mongod.conf)
security:
  authorization: enabled

# Reiniciar
sudo systemctl restart mongod

# Crear usuario administrador
mongosh
use admin
db.createUser({
  user: "admin",
  pwd: "password_seguro",
  roles: [ { role: "userAdminAnyDatabase", db: "admin" } ]
})

# Conectar con autenticación
mongosh -u admin -p password_seguro --authenticationDatabase admin
```

#### Cifrado de campos sensibles

```javascript
// Conectar a MongoDB
const { MongoClient } = require('mongodb');
const crypto = require('crypto');

// Función de cifrado
function cifrar(texto, clave) {
    const iv = crypto.randomBytes(16);
    const cipher = crypto.createCipheriv('aes-256-cbc', Buffer.from(clave), iv);
    let cifrado = cipher.update(texto, 'utf8', 'hex');
    cifrado += cipher.final('hex');
    return iv.toString('hex') + ':' + cifrado;
}

// Función de descifrado
function descifrar(textoCifrado, clave) {
    const partes = textoCifrado.split(':');
    const iv = Buffer.from(partes[0], 'hex');
    const cifrado = partes[1];
    const decipher = crypto.createDecipheriv('aes-256-cbc', Buffer.from(clave), iv);
    let descifrado = decipher.update(cifrado, 'hex', 'utf8');
    descifrado += decipher.final('utf8');
    return descifrado;
}

// Usar en aplicación
const claveMaestra = crypto.randomBytes(32); // Guardar en variable de entorno

async function insertarPaciente() {
    const client = new MongoClient('mongodb://localhost:27017');
    await client.connect();
    const db = client.db('hospital');
    
    await db.collection('pacientes').insertOne({
        nombre: 'María González',
        ci: cifrar('87654321', claveMaestra),
        diagnostico: cifrar('Hipertensión', claveMaestra),
        fecha_ingreso: new Date()
    });
    
    await client.close();
}

async function consultarPaciente() {
    const client = new MongoClient('mongodb://localhost:27017');
    await client.connect();
    const db = client.db('hospital');
    
    const paciente = await db.collection('pacientes').findOne({ nombre: 'María González' });
    
    console.log('CI:', descifrar(paciente.ci, claveMaestra));
    console.log('Diagnóstico:', descifrar(paciente.diagnostico, claveMaestra));
    
    await client.close();
}
```

#### Control de acceso en MongoDB

```javascript
// Crear roles personalizados
use hospital

db.createRole({
  role: "medicoRole",
  privileges: [
    {
      resource: { db: "hospital", collection: "pacientes" },
      actions: [ "find", "insert", "update" ]
    }
  ],
  roles: []
})

db.createRole({
  role: "enfermeroRole",
  privileges: [
    {
      resource: { db: "hospital", collection: "pacientes" },
      actions: [ "find", "update" ]
    }
  ],
  roles: []
})

// Crear usuarios con roles
db.createUser({
  user: "dr_martinez",
  pwd: "password_seguro",
  roles: [ { role: "medicoRole", db: "hospital" } ]
})
```

---

### 6.3 Cumplimiento y Compliance

#### GDPR - Implementación técnica

```sql
-- PostgreSQL: Tabla de consentimientos
CREATE TABLE consentimientos (
    id SERIAL PRIMARY KEY,
    usuario_id INT REFERENCES usuarios(id),
    finalidad VARCHAR(100),  -- 'marketing', 'analytics', etc.
    consentimiento_otorgado BOOLEAN,
    fecha_consentimiento TIMESTAMP,
    ip_origen INET,
    version_politica VARCHAR(10)
);

-- Registrar consentimiento
INSERT INTO consentimientos (usuario_id, finalidad, consentimiento_otorgado, fecha_consentimiento, ip_origen, version_politica)
VALUES (123, 'marketing', true, NOW(), '192.168.1.100', 'v2.1');

-- Derecho al olvido (anonimización)
UPDATE usuarios
SET 
    nombre = 'Usuario Anonimizado',
    email = CONCAT('anonimo_', id, '@deleted.com'),
    telefono = NULL,
    direccion = NULL,
    fecha_nacimiento = NULL
WHERE id = 123;

-- Portabilidad de datos (exportar en JSON)
SELECT json_agg(row_to_json(t))
FROM (
    SELECT * FROM usuarios WHERE id = 123
) t;
```

