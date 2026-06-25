# CURSO COMPLETO DE CIBERSEGURIDAD - PARTE 4

## MÓDULO 7: CERTIFICADOS DIGITALES, KEYSTORES Y TRUSTSTORES

### 7.1 Fundamentos de Certificados Digitales

#### 7.1.1 ¿Qué es un Certificado Digital?

**Definición:** Documento electrónico que vincula una clave pública con la identidad de su propietario, firmado por una Autoridad Certificadora (CA).

**Analogía:** Es como un pasaporte digital que prueba tu identidad en internet.

```
┌─────────────────────────────────────────────────────────┐
│           CERTIFICADO DIGITAL X.509                     │
├─────────────────────────────────────────────────────────┤
│ Versión: 3                                              │
│ Número de Serie: 4A:3F:2E:1D:9C:8B:7A:6F               │
│                                                         │
│ EMISOR (CA):                                            │
│   CN = DigiCert Global Root CA                         │
│   O = DigiCert Inc                                      │
│   C = US                                                │
│                                                         │
│ SUJETO (Propietario):                                   │
│   CN = www.ejemplo.com                                  │
│   O = Empresa Ejemplo S.A.                             │
│   L = Montevideo                                        │
│   C = UY                                                │
│                                                         │
│ Validez:                                                │
│   Desde: 2024-01-01 00:00:00 UTC                       │
│   Hasta: 2025-01-01 23:59:59 UTC                       │
│                                                         │
│ CLAVE PÚBLICA (RSA 2048 bits):                         │
│   30 82 01 0a 02 82 01 01 00 c4 5e 9f...              │
│                                                         │
│ Extensiones:                                            │
│   - Subject Alternative Names (SAN)                     │
│     * www.ejemplo.com                                   │
│     * ejemplo.com                                       │
│     * *.ejemplo.com                                     │
│   - Key Usage: Digital Signature, Key Encipherment     │
│   - Extended Key Usage: TLS Web Server Authentication  │
│                                                         │
│ FIRMA DIGITAL (SHA256-RSA):                             │
│   8f 3a 2b 1c 9d 4e 5f 6a 7b 8c...                    │
└─────────────────────────────────────────────────────────┘
```

#### 7.1.2 Componentes de un Certificado X.509

**Atributos principales:**

1. **Subject (Sujeto):** Identidad del propietario
   - CN (Common Name): Nombre del dominio o persona
   - O (Organization): Organización
   - OU (Organizational Unit): Departamento
   - L (Locality): Ciudad
   - ST (State): Estado/Provincia
   - C (Country): País (código ISO de 2 letras)

2. **Issuer (Emisor):** Identidad de la CA que firmó el certificado

3. **Serial Number:** Número único asignado por la CA

4. **Validity Period:** Período de validez (Not Before / Not After)

5. **Public Key:** Clave pública del propietario

6. **Signature Algorithm:** Algoritmo usado para firmar (ej: SHA256-RSA)

7. **Extensions (Extensiones):**
   - **Subject Alternative Name (SAN):** Dominios adicionales
   - **Key Usage:** Propósitos de la clave (firma, cifrado, etc.)
   - **Extended Key Usage:** Usos específicos (TLS server, email, code signing)
   - **Basic Constraints:** Si es CA o certificado final
   - **Authority Key Identifier:** Identifica la clave de la CA
   - **Subject Key Identifier:** Identifica la clave del sujeto
   - **CRL Distribution Points:** Dónde verificar revocaciones

---

### 7.2 Cadena de Confianza (Chain of Trust)

```
┌──────────────────────────────────────────────────────────┐
│                    ROOT CA                               │
│         (DigiCert Global Root CA)                        │
│                                                          │
│  • Autofirmado                                           │
│  • Válido por 20-30 años                                 │
│  • Incluido en navegadores/SO                            │
│  • Clave privada en HSM ultra-seguro                     │
└────────────────┬─────────────────────────────────────────┘
                 │ Firma
                 ▼
┌──────────────────────────────────────────────────────────┐
│              INTERMEDIATE CA                             │
│         (DigiCert TLS RSA SHA256 2020 CA1)              │
│                                                          │
│  • Firmado por Root CA                                   │
│  • Válido por 5-10 años                                  │
│  • Usado para firmar certificados finales               │
│  • Si se compromete, solo se revoca este nivel          │
└────────────────┬─────────────────────────────────────────┘
                 │ Firma
                 ▼
┌──────────────────────────────────────────────────────────┐
│              END-ENTITY CERTIFICATE                      │
│              (www.ejemplo.com)                           │
│                                                          │
│  • Firmado por Intermediate CA                           │
│  • Válido por 1 año (máximo 398 días desde 2020)        │
│  • Usado por el servidor web                             │
│  • Contiene clave pública del servidor                   │
└──────────────────────────────────────────────────────────┘
```

**Proceso de verificación:**

```
Cliente (Navegador)
    │
    │ 1. Recibe certificado del servidor
    ▼
┌─────────────────────────────┐
│ Certificado: www.ejemplo.com│
└─────────────────────────────┘
    │
    │ 2. Verifica firma con clave pública de Intermediate CA
    ▼
┌─────────────────────────────┐
│ Intermediate CA             │
└─────────────────────────────┘
    │
    │ 3. Verifica firma con clave pública de Root CA
    ▼
┌─────────────────────────────┐
│ Root CA (en TrustStore)     │
└─────────────────────────────┘
    │
    │ 4. Root CA es confiable → Toda la cadena es válida
    ▼
  ✓ CONEXIÓN SEGURA
```

---

### 7.3 KeyStore vs TrustStore

#### 7.3.1 KeyStore (Almacén de Claves)

**Definición:** Archivo que contiene claves privadas y sus certificados asociados.

**Contenido:**
- Clave privada del servidor/aplicación
- Certificado del servidor
- Cadena de certificados (intermediate + root)

**Uso:** El servidor usa el KeyStore para presentar su identidad a los clientes.

```
┌─────────────────────────────────────────────────────────┐
│                    KEYSTORE.JKS                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Alias: "servidor-web"                                  │
│  ├─ Clave Privada (protegida con password)             │
│  │    • RSA 2048 bits                                   │
│  │    • NUNCA se comparte                               │
│  │                                                      │
│  └─ Cadena de Certificados:                             │
│       ├─ [0] Certificado del servidor (www.ejemplo.com) │
│       ├─ [1] Intermediate CA                            │
│       └─ [2] Root CA                                    │
│                                                         │
│  Alias: "cliente-api"                                   │
│  ├─ Clave Privada                                       │
│  └─ Certificado de cliente                              │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

#### 7.3.2 TrustStore (Almacén de Confianza)

**Definición:** Archivo que contiene certificados de CAs en las que confiamos.

**Contenido:**
- Certificados de Root CAs
- Certificados de Intermediate CAs
- Solo claves públicas (NO claves privadas)

**Uso:** El cliente usa el TrustStore para verificar certificados de servidores.

```
┌─────────────────────────────────────────────────────────┐
│                   TRUSTSTORE.JKS                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Alias: "digicert-root-ca"                              │
│  └─ Certificado Root CA (solo clave pública)            │
│                                                         │
│  Alias: "lets-encrypt-root"                             │
│  └─ Certificado Root CA                                 │
│                                                         │
│  Alias: "empresa-interna-ca"                            │
│  └─ Certificado CA corporativa                          │
│                                                         │
│  Alias: "servidor-partner"                              │
│  └─ Certificado de servidor externo confiable           │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

#### 7.3.3 Comparación Visual

```
SERVIDOR                                    CLIENTE
┌──────────────┐                           ┌──────────────┐
│  KEYSTORE    │                           │  TRUSTSTORE  │
│              │                           │              │
│ • Mi clave   │                           │ • CAs        │
│   privada    │                           │   confiables │
│              │                           │              │
│ • Mi         │    ──────────────────>    │ • Verifica   │
│   certificado│    Presenta identidad     │   identidad  │
│              │                           │              │
└──────────────┘                           └──────────────┘
     "Quién soy"                               "En quién confío"
```

---

### 7.4 Tipos de Certificados

#### 7.4.1 Según Validación

**1. Domain Validated (DV)**
- Validación: Solo propiedad del dominio
- Tiempo: Minutos
- Costo: Gratis (Let's Encrypt) o bajo
- Uso: Blogs, sitios personales
- Indicador: Candado verde

**2. Organization Validated (OV)**
- Validación: Dominio + existencia legal de la organización
- Tiempo: 1-3 días
- Costo: Medio
- Uso: Empresas, e-commerce
- Indicador: Candado + nombre de organización

**3. Extended Validation (EV)**
- Validación: Dominio + verificación exhaustiva de la empresa
- Tiempo: 1-2 semanas
- Costo: Alto
- Uso: Bancos, grandes corporaciones
- Indicador: Barra verde con nombre de empresa (navegadores antiguos)

#### 7.4.2 Según Uso

**1. SSL/TLS Server Certificate**
- Uso: HTTPS en servidores web
- Key Usage: Digital Signature, Key Encipherment
- Extended Key Usage: TLS Web Server Authentication

**2. Client Certificate**
- Uso: Autenticación de usuarios/dispositivos
- Key Usage: Digital Signature
- Extended Key Usage: TLS Web Client Authentication

**3. Code Signing Certificate**
- Uso: Firmar software/aplicaciones
- Key Usage: Digital Signature
- Extended Key Usage: Code Signing

**4. Email Certificate (S/MIME)**
- Uso: Cifrar y firmar emails
- Key Usage: Digital Signature, Key Encipherment
- Extended Key Usage: Email Protection

**5. Wildcard Certificate**
- Uso: Múltiples subdominios
- CN: *.ejemplo.com
- Cubre: www.ejemplo.com, api.ejemplo.com, mail.ejemplo.com

**6. Multi-Domain (SAN) Certificate**
- Uso: Múltiples dominios diferentes
- SAN: ejemplo.com, ejemplo.net, otro-dominio.com

---

### 7.5 Certificados Autofirmados

#### 7.5.1 ¿Qué es un Certificado Autofirmado?

**Definición:** Certificado firmado por la misma entidad que lo emite, sin intervención de una CA externa.

```
┌──────────────────────────────────────────────────────────┐
│         CERTIFICADO AUTOFIRMADO                          │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  Emisor:    CN=localhost, O=Mi Empresa                   │
│  Sujeto:    CN=localhost, O=Mi Empresa                   │
│             ▲                ▲                           │
│             └────────────────┘                           │
│              SON IGUALES                                 │
│                                                          │
│  • No hay cadena de confianza                            │
│  • No está en TrustStore de navegadores                  │
│  • Genera advertencia de seguridad                       │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

#### 7.5.2 Cuándo Usar Certificados Autofirmados

**✓ Casos válidos:**
- Desarrollo local
- Entornos de testing
- Redes internas corporativas (con CA interna)
- Comunicación entre microservicios internos
- Laboratorios de aprendizaje

**✗ NO usar en:**
- Sitios web públicos
- Producción
- Aplicaciones móviles públicas
- APIs públicas

#### 7.5.3 Crear Certificado Autofirmado

```bash
# Generar clave privada y certificado autofirmado en un paso
openssl req -x509 -newkey rsa:2048 -nodes \
  -keyout servidor.key \
  -out servidor.crt \
  -days 365 \
  -subj "/C=UY/ST=Montevideo/L=Montevideo/O=Mi Empresa/CN=localhost"

# Ver contenido del certificado
openssl x509 -in servidor.crt -text -noout

# Verificar que es autofirmado (Issuer == Subject)
openssl x509 -in servidor.crt -noout -issuer -subject
```

#### 7.5.4 Cómo lo Maneja el Navegador

**Flujo de validación:**

```
1. Navegador recibe certificado autofirmado
   │
   ▼
2. Busca el emisor en TrustStore
   │
   ▼
3. NO ENCUENTRA (no es una CA conocida)
   │
   ▼
4. ADVERTENCIA DE SEGURIDAD
   │
   ├─ Chrome: "Tu conexión no es privada"
   ├─ Firefox: "Advertencia: Riesgo potencial de seguridad"
   └─ Edge: "Tu conexión no es privada"
   │
   ▼
5. Usuario puede:
   ├─ Volver atrás (recomendado)
   └─ Continuar de todos modos (bajo su riesgo)
```

**Pantalla de advertencia:**

```
┌────────────────────────────────────────────────────────┐
│  ⚠️  Tu conexión no es privada                         │
├────────────────────────────────────────────────────────┤
│                                                        │
│  Es posible que los atacantes estén intentando        │
│  robar tu información de localhost (por ejemplo,      │
│  contraseñas, mensajes o tarjetas de crédito).        │
│                                                        │
│  NET::ERR_CERT_AUTHORITY_INVALID                       │
│                                                        │
│  Este servidor no pudo probar que es localhost;       │
│  el certificado de seguridad es autofirmado.          │
│                                                        │
│  [Volver a la seguridad]  [Avanzado]                  │
│                                                        │
└────────────────────────────────────────────────────────┘
```

#### 7.5.5 Agregar Certificado Autofirmado al TrustStore

**En el navegador (Chrome/Edge):**

```bash
# Linux
1. Abrir Chrome → Configuración → Privacidad y seguridad
2. Seguridad → Administrar certificados
3. Autoridades → Importar
4. Seleccionar servidor.crt
5. Marcar "Confiar en este certificado para identificar sitios web"

# Windows
certutil -addstore -user "Root" servidor.crt

# macOS
sudo security add-trusted-cert -d -r trustRoot -k /Library/Keychains/System.keychain servidor.crt
```

**En Java (aplicación):**

```bash
# Importar al TrustStore de Java
keytool -import -alias mi-servidor-local \
  -file servidor.crt \
  -keystore $JAVA_HOME/lib/security/cacerts \
  -storepass changeit
```

---

### 7.6 Trabajar con KeyStores en Java

#### 7.6.1 Crear KeyStore

```bash
# Generar par de claves y certificado autofirmado en KeyStore
keytool -genkeypair \
  -alias servidor-web \
  -keyalg RSA \
  -keysize 2048 \
  -validity 365 \
  -keystore keystore.jks \
  -storepass password123 \
  -keypass password123 \
  -dname "CN=localhost, OU=IT, O=Mi Empresa, L=Montevideo, ST=Montevideo, C=UY"

# Listar contenido del KeyStore
keytool -list -v -keystore keystore.jks -storepass password123

# Exportar certificado público
keytool -export -alias servidor-web \
  -file servidor.crt \
  -keystore keystore.jks \
  -storepass password123
```

#### 7.6.2 Crear TrustStore

```bash
# Crear TrustStore e importar certificado de CA
keytool -import -alias ca-confiable \
  -file ca-cert.crt \
  -keystore truststore.jks \
  -storepass password123

# Importar múltiples CAs
keytool -import -alias digicert-root \
  -file digicert-root.crt \
  -keystore truststore.jks \
  -storepass password123

# Listar certificados confiables
keytool -list -keystore truststore.jks -storepass password123
```

#### 7.6.3 Usar KeyStore y TrustStore en Aplicación Java

```java
import javax.net.ssl.*;
import java.io.FileInputStream;
import java.security.KeyStore;

public class SSLConfiguracion {
    
    public static void configurarSSL() throws Exception {
        // Cargar KeyStore (identidad del servidor)
        KeyStore keyStore = KeyStore.getInstance("JKS");
        try (FileInputStream fis = new FileInputStream("keystore.jks")) {
            keyStore.load(fis, "password123".toCharArray());
        }
        
        // Configurar KeyManagerFactory
        KeyManagerFactory kmf = KeyManagerFactory.getInstance(
            KeyManagerFactory.getDefaultAlgorithm()
        );
        kmf.init(keyStore, "password123".toCharArray());
        
        // Cargar TrustStore (CAs confiables)
        KeyStore trustStore = KeyStore.getInstance("JKS");
        try (FileInputStream fis = new FileInputStream("truststore.jks")) {
            trustStore.load(fis, "password123".toCharArray());
        }
        
        // Configurar TrustManagerFactory
        TrustManagerFactory tmf = TrustManagerFactory.getInstance(
            TrustManagerFactory.getDefaultAlgorithm()
        );
        tmf.init(trustStore);
        
        // Crear SSLContext
        SSLContext sslContext = SSLContext.getInstance("TLS");
        sslContext.init(
            kmf.getKeyManagers(),
            tmf.getTrustManagers(),
            null
        );
        
        // Establecer como contexto por defecto
        SSLContext.setDefault(sslContext);
        
        System.out.println("SSL configurado correctamente");
    }
    
    public static void main(String[] args) {
        try {
            configurarSSL();
            
            // Ahora todas las conexiones HTTPS usarán esta configuración
            // Ejemplo: HttpsURLConnection, RestTemplate, etc.
            
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

#### 7.6.4 Configurar en Spring Boot

```yaml
# application.yml
server:
  port: 8443
  ssl:
    enabled: true
    key-store: classpath:keystore.jks
    key-store-password: password123
    key-store-type: JKS
    key-alias: servidor-web
    
# Para cliente HTTPS
rest:
  ssl:
    trust-store: classpath:truststore.jks
    trust-store-password: password123
    trust-store-type: JKS
```

```java
// Configuración programática
@Configuration
public class SSLConfig {
    
    @Bean
    public RestTemplate restTemplate() throws Exception {
        // Cargar TrustStore
        KeyStore trustStore = KeyStore.getInstance("JKS");
        try (InputStream is = getClass().getResourceAsStream("/truststore.jks")) {
            trustStore.load(is, "password123".toCharArray());
        }
        
        SSLContext sslContext = SSLContextBuilder
            .create()
            .loadTrustMaterial(trustStore, null)
            .build();
        
        SSLConnectionSocketFactory socketFactory = 
            new SSLConnectionSocketFactory(sslContext);
        
        HttpClient httpClient = HttpClients.custom()
            .setSSLSocketFactory(socketFactory)
            .build();
        
        HttpComponentsClientHttpRequestFactory factory = 
            new HttpComponentsClientHttpRequestFactory(httpClient);
        
        return new RestTemplate(factory);
    }
}
```

---

### 7.7 Let's Encrypt - Certificados Gratuitos

#### 7.7.1 ¿Qué es Let's Encrypt?

**Definición:** CA gratuita y automatizada que emite certificados DV válidos por 90 días.

**Ventajas:**
- Completamente gratuito
- Automatización con ACME protocol
- Renovación automática
- Confiable (incluido en todos los navegadores)

#### 7.7.2 Obtener Certificado con Certbot

```bash
# Instalar Certbot
sudo apt install certbot python3-certbot-nginx

# Obtener certificado para Nginx
sudo certbot --nginx -d ejemplo.com -d www.ejemplo.com

# Obtener certificado standalone (sin servidor web)
sudo certbot certonly --standalone -d ejemplo.com

# Renovar certificados (automático con cron)
sudo certbot renew

# Verificar renovación automática
sudo certbot renew --dry-run
```

#### 7.7.3 Configuración Nginx con Let's Encrypt

```nginx
server {
    listen 80;
    server_name ejemplo.com www.ejemplo.com;
    
    # Redirigir HTTP a HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name ejemplo.com www.ejemplo.com;
    
    # Certificados de Let's Encrypt
    ssl_certificate /etc/letsencrypt/live/ejemplo.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/ejemplo.com/privkey.pem;
    
    # Configuración SSL segura
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    
    # HSTS (HTTP Strict Transport Security)
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    
    location / {
        root /var/www/html;
        index index.html;
    }
}
```

---

### 7.8 Laboratorio Completo: HTTPS con Certificados

#### Escenario: Servidor web con certificado autofirmado

```bash
# 1. Generar clave privada
openssl genrsa -out servidor.key 2048

# 2. Crear CSR (Certificate Signing Request)
openssl req -new -key servidor.key -out servidor.csr \
  -subj "/C=UY/ST=Montevideo/L=Montevideo/O=Lab Seguridad/CN=localhost"

# 3. Autofirmar certificado
openssl x509 -req -days 365 -in servidor.csr \
  -signkey servidor.key -out servidor.crt

# 4. Crear servidor HTTPS en Python
cat > servidor_https.py << 'EOF'
import http.server
import ssl

# Configurar servidor HTTP
server_address = ('localhost', 4443)
httpd = http.server.HTTPServer(server_address, http.server.SimpleHTTPRequestHandler)

# Configurar SSL
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain('servidor.crt', 'servidor.key')

httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

print("Servidor HTTPS corriendo en https://localhost:4443")
httpd.serve_forever()
EOF

# 5. Ejecutar servidor
python3 servidor_https.py

# 6. Probar con curl (ignorando verificación)
curl -k https://localhost:4443

# 7. Probar con curl (verificando certificado - fallará)
curl https://localhost:4443
# Error: SSL certificate problem: self signed certificate

# 8. Agregar certificado al TrustStore de curl
curl --cacert servidor.crt https://localhost:4443
```

