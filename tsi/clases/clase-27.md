# Clase 27: Validacion de Entradas y Salidas

**Numero de clase:** 17
**Duracion:** 2 horas

## Objetivos de Aprendizaje

- Comprender por que toda entrada de usuario debe considerarse maliciosa
- Diferenciar entre whitelist y blacklist para validacion
- Distinguir entre sanitizacion y validacion
- Implementar output encoding para prevenir XSS
- Aplicar tecnicas de validacion para tipos numericos, emails, URLs y fechas

## Contenido Detallado

### 1. Por que Validar Entradas

El principio fundamental: "Todos los datos son maliciosos hasta que se demuestre lo contrario". Toda entrada que ingresa a un sistema desde una fuente externa (usuario, API, archivo, base de datos) puede contener datos disenados para comprometer el sistema.

**Vectores de ataque por falta de validacion:**
- Inyeccion SQL
- Cross-Site Scripting (XSS)
- Command Injection
- Path Traversal
- Buffer Overflows
- Inyeccion de LDAP/XML

### 2. Tipos de Validacion

**Whitelist (Lista Blanca):** Permitir solo lo que se sabe que es valido. Mas seguro porque asume que todo es invalido por defecto.
- Ejemplo: `^[a-zA-Z0-9]{3,20}$`

**Blacklist (Lista Negra):** Bloquear lo que se sabe que es malicioso. Menos seguro porque siempre hay vectores no contemplados.
- Ejemplo: Bloquear `<script>`, `' OR 1=1--`

**Tipos de validacion:**
- **Tipo:** Asegurar que el dato es del tipo esperado (int, float, bool)
- **Longitud:** Minimo y maximo de caracteres
- **Formato:** Expresiones regulares, patrones especificos
- **Rango:** Valores minimos y maximos permitidos

### 3. Sanitizacion vs. Validacion

| Aspecto | Validacion | Sanitizacion |
|---------|-----------|--------------|
| Accion | Rechazar dato invalido | Limpiar/modificar dato |
| Seguridad | Mayor (rechazo total) | Menor (puede omitir algo) |
| Uso tipico | Input de formularios | Output para HTML/URL |
| Ejemplo | Rechazar email sin @ | Escapar < por &lt; |

### 4. Output Encoding

Tecnica para evitar que datos generados por el usuario sean interpretados como codigo por el navegador.

**Tipos de encoding:**
- **HTML Encoding:** Convierte `<` en `&lt;`, `>` en `&gt;`, `&` en `&amp;`, `"` en `&quot;`
- **URL Encoding:** Convierte caracteres especiales a `%XX` (ej: espacio a `%20`)
- **JavaScript Encoding:** Escapa caracteres para contextos JavaScript
- **CSS Encoding:** Para valores insertados en CSS

### 5. Frameworks y Librerias

- **OWASP ESAPI:** Enterprise Security API, libreria de referencia
- **validator.js:** Validacion de strings del lado JavaScript
- **Java Bean Validation:** Anotaciones como `@NotNull`, `@Size`, `@Pattern`
- **Pydantic:** Validacion de modelos en Python
- **marshmallow:** Deserializacion y validacion en Python

### 6. Casos Especificos de Validacion

**Inputs numericos:**
```python
def validar_edad(valor):
    try:
        edad = int(valor)
        if edad < 0 or edad > 150:
            return False, "Edad fuera de rango"
        return True, edad
    except (ValueError, TypeError):
        return False, "Debe ser un numero entero"
```

**Emails:**
```python
import re

def validar_email(email):
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(patron, email) and len(email) <= 254:
        return True, email.lower()
    return False, "Email invalido"
```

**URLs:**
```python
from urllib.parse import urlparse

def validar_url(url):
    try:
        parsed = urlparse(url)
        if parsed.scheme not in ('http', 'https'):
            return False, "Solo HTTP/HTTPS permitidos"
        if not parsed.netloc:
            return False, "URL sin dominio"
        return True, url
    except Exception:
        return False, "URL malformada"
```

**Fechas:**
```python
from datetime import datetime

def validar_fecha(texto, formato='%Y-%m-%d'):
    try:
        fecha = datetime.strptime(texto, formato)
        return True, fecha
    except ValueError:
        return False, "Formato de fecha invalido (use YYYY-MM-DD)"
```

## Ejercicio 1: App Flask con Validacion Completa (Whitelist)

Crear una aplicacion Flask con 5 endpoints vulnerables y agregar validacion completa usando whitelist.

```python
# app.py - Version completa con validacion
from flask import Flask, request, jsonify
import re
from datetime import datetime
from urllib.parse import urlparse

app = Flask(__name__)

# ============================================================
# FUNCIONES DE VALIDACION (Whitelist)
# ============================================================

def validar_nombre(nombre):
    """Solo letras, espacios, guiones y puntos, entre 2 y 50 caracteres."""
    if not nombre or not isinstance(nombre, str):
        return False, "Nombre requerido"
    nombre = nombre.strip()
    if len(nombre) < 2 or len(nombre) > 50:
        return False, "Nombre debe tener entre 2 y 50 caracteres"
    if not re.match(r'^[a-zA-Z][a-zA-Z\s.\'-]{1,48}[a-zA-Z.]$', nombre):
        return False, "Nombre contiene caracteres no permitidos"
    return True, nombre


def validar_edad(edad):
    """Entero entre 0 y 150."""
    try:
        valor = int(edad)
        if valor < 0 or valor > 150:
            return False, "Edad debe estar entre 0 y 150"
        return True, valor
    except (ValueError, TypeError):
        return False, "Edad debe ser un numero entero"


def validar_email(email):
    """Formato email estandar, longitud maxima 254."""
    if not email or not isinstance(email, str):
        return False, "Email requerido"
    email = email.strip().lower()
    if len(email) > 254:
        return False, "Email demasiado largo"
    patron = r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$'
    if not re.match(patron, email):
        return False, "Formato de email invalido"
    return True, email


def validar_url(url):
    """Solo HTTP/HTTPS, dominio requerido."""
    if not url or not isinstance(url, str):
        return False, "URL requerida"
    url = url.strip()
    try:
        parsed = urlparse(url)
        if parsed.scheme not in ('http', 'https'):
            return False, "Solo URLs HTTP/HTTPS permitidas"
        if not parsed.netloc:
            return False, "URL debe incluir un dominio valido"
        return True, url
    except Exception:
        return False, "URL malformada"


def validar_fecha(texto):
    """Formato YYYY-MM-DD, fecha real."""
    if not texto or not isinstance(texto, str):
        return False, "Fecha requerida"
    texto = texto.strip()
    patron = r'^\d{4}-\d{2}-\d{2}$'
    if not re.match(patron, texto):
        return False, "Formato debe ser YYYY-MM-DD"
    try:
        datetime.strptime(texto, '%Y-%m-%d')
        return True, texto
    except ValueError:
        return False, "Fecha no valida (ej: mes entre 01-12, dia entre 01-31)"


def validar_comentario(comentario):
    """Texto plano, sin HTML, max 500 caracteres."""
    if not comentario or not isinstance(comentario, str):
        return False, "Comentario requerido"
    comentario = comentario.strip()
    if len(comentario) > 500:
        return False, "Comentario demasiado largo (max 500 caracteres)"
    if len(comentario) < 1:
        return False, "Comentario no puede estar vacio"
    # Bloquear tags HTML evidentes
    if re.search(r'<[^>]+>', comentario):
        return False, "No se permiten tags HTML"
    return True, comentario


# ============================================================
# ENDPOINTS
# ============================================================

@app.route('/usuario', methods=['POST'])
def crear_usuario():
    """Registro de usuario con nombre, edad y email."""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'JSON requerido'}), 400

    errores = {}

    valido, resultado = validar_nombre(data.get('nombre', ''))
    if not valido:
        errores['nombre'] = resultado

    valido, resultado = validar_edad(data.get('edad', ''))
    if not valido:
        errores['edad'] = resultado

    valido, resultado = validar_email(data.get('email', ''))
    if not valido:
        errores['email'] = resultado

    if errores:
        return jsonify({'error': 'Datos invalidos', 'detalles': errores}), 400

    return jsonify({
        'mensaje': 'Usuario creado exitosamente',
        'usuario': {
            'nombre': resultado[1] if isinstance(resultado, tuple) else None,
            'email': resultado
        }
    }), 201


@app.route('/comentario', methods=['POST'])
def crear_comentario():
    """Endpoint que acepta comentarios y los devuelve escapados."""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'JSON requerido'}), 400

    valido, resultado = validar_comentario(data.get('comentario', ''))
    if not valido:
        return jsonify({'error': resultado}), 400

    from html import escape
    comentario_seguro = escape(resultado)

    return jsonify({
        'mensaje': 'Comentario recibido',
        'comentario': comentario_seguro
    }), 201


@app.route('/enlace', methods=['POST'])
def crear_enlace():
    """Valida y almacena una URL."""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'JSON requerido'}), 400

    valido, resultado = validar_url(data.get('url', ''))
    if not valido:
        return jsonify({'error': resultado}), 400

    return jsonify({
        'mensaje': 'URL valida',
        'url': resultado
    }), 201


@app.route('/evento', methods=['POST'])
def crear_evento():
    """Valida nombre del evento y fecha."""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'JSON requerido'}), 400

    errores = {}

    valido, resultado = validar_nombre(data.get('nombre_evento', ''))
    if not valido:
        errores['nombre_evento'] = resultado

    valido, resultado = validar_fecha(data.get('fecha', ''))
    if not valido:
        errores['fecha'] = resultado

    if errores:
        return jsonify({'error': 'Datos invalidos', 'detalles': errores}), 400

    return jsonify({
        'mensaje': 'Evento creado',
        'evento': {
            'nombre': data.get('nombre_evento'),
            'fecha': data.get('fecha')
        }
    }), 201


@app.route('/buscar', methods=['GET'])
def buscar():
    """Busqueda con parametro de consulta validado."""
    query = request.args.get('q', '')
    if not query or len(query.strip()) == 0:
        return jsonify({'error': 'Parametro de busqueda requerido'}), 400
    if len(query) > 100:
        return jsonify({'error': 'Busqueda demasiado larga (max 100 caracteres)'}), 400
    if re.search(r'[<>\'";]', query):
        return jsonify({'error': 'Caracteres no permitidos en la busqueda'}), 400

    from html import escape
    query_segura = escape(query.strip())

    return jsonify({
        'resultados': [],
        'query': query_segura
    })


if __name__ == '__main__':
    app.run(debug=False)
```

**Pruebas de los endpoints:**
```bash
# Prueba 1: Usuario valido
curl -X POST http://localhost:5000/usuario -H "Content-Type: application/json" -d "{\"nombre\": \"Juan Perez\", \"edad\": 30, \"email\": \"juan@example.com\"}"

# Prueba 2: Usuario con datos invalidos
curl -X POST http://localhost:5000/usuario -H "Content-Type: application/json" -d "{\"nombre\": \"<script>alert(1)</script>\", \"edad\": -5, \"email\": \"invalido\"}"

# Prueba 3: Comentario con XSS
curl -X POST http://localhost:5000/comentario -H "Content-Type: application/json" -d "{\"comentario\": \"<script>document.cookie</script>\"}"

# Prueba 4: URL valida e invalida
curl -X POST http://localhost:5000/enlace -H "Content-Type: application/json" -d "{\"url\": \"https://google.com\"}"
curl -X POST http://localhost:5000/enlace -H "Content-Type: application/json" -d "{\"url\": \"javascript:alert(1)\"}"

# Prueba 5: Evento con fecha
curl -X POST http://localhost:5000/evento -H "Content-Type: application/json" -d "{\"nombre_evento\": \"Conferencia Seguridad\", \"fecha\": \"2025-12-31\"}"
```

## Ejercicio 2: Output Encoding para Prevenir XSS en App de Comentarios

Aplicacion Flask para comentarios que muestra como el output encoding evita XSS.

```python
# comentarios_xss.py - App con y sin proteccion XSS
from flask import Flask, request, render_template_string, escape
import html

app = Flask(__name__)

# Simulacion de base de datos
comentarios_db = []


@app.route('/')
def index():
    return '''
    <h1>App de Comentarios</h1>
    <form action="/comentar" method="POST">
        <input type="text" name="usuario" placeholder="Tu nombre" required>
        <textarea name="comentario" placeholder="Tu comentario" required></textarea>
        <button type="submit">Enviar</button>
    </form>
    <hr>
    <h2>Comentarios</h2>
    <a href="/comentarios/sin-proteger">Ver SIN proteccion (peligroso)</a><br>
    <a href="/comentarios/protegido">Ver CON proteccion (seguro)</a>
    '''


@app.route('/comentar', methods=['POST'])
def comentar():
    usuario = request.form.get('usuario', '').strip()
    comentario = request.form.get('comentario', '').strip()

    if not usuario or not comentario:
        return "Todos los campos son requeridos", 400
    if len(usuario) > 50 or len(comentario) > 500:
        return "Texto demasiado largo", 400

    comentarios_db.append({
        'usuario': usuario,
        'comentario': comentario
    })
    return "Comentario agregado. <a href='/'>Volver</a>"


@app.route('/comentarios/sin-proteger')
def comentarios_sin_proteger():
    """Vulnerable a XSS - NO USAR EN PRODUCCION"""
    items = ''
    for c in comentarios_db:
        items += f'<div><strong>{c["usuario"]}:</strong> {c["comentario"]}</div><hr>'

    return render_template_string(f'''
    <h1>Comentarios (SIN proteccion XSS)</h1>
    <p>ADVERTENCIA: Esta vista es vulnerable a XSS</p>
    {items}
    <a href="/">Volver</a>
    ''')


@app.route('/comentarios/protegido')
def comentarios_protegido():
    """Seguro contra XSS - usa html.escape"""
    items = ''
    for c in comentarios_db:
        usuario_seguro = html.escape(c['usuario'])
        comentario_seguro = html.escape(c['comentario'])
        items += f'<div><strong>{usuario_seguro}:</strong> {comentario_seguro}</div><hr>'

    return f'''
    <h1>Comentarios (CON proteccion XSS)</h1>
    {items}
    <a href="/">Volver</a>
    '''


@app.route('/comentarios/jinja-protegido')
def comentarios_jinja_protegido():
    """Usando Jinja2 que escapa por defecto (mas seguro aun)"""
    return render_template_string('''
    <h1>Comentarios (Protegido por Jinja2)</h1>
    {% for c in comentarios %}
        <div><strong>{{ c.usuario }}:</strong> {{ c.comentario }}</div><hr>
    {% endfor %}
    <a href="/">Volver</a>
    ''', comentarios=comentarios_db)


if __name__ == '__main__':
    app.run(debug=True)
```

**Prueba de XSS:**
```bash
# Probar con
curl -X POST http://localhost:5000/comentar -d "usuario=<script>alert('XSS')</script>&comentario=<img src=x onerror=alert('XSS')>"

# Luego visitar
# http://localhost:5000/comentarios/sin-proteger  -> EJECUTA el script
# http://localhost:5000/comentarios/protegido     -> MUESTRA el codigo escapado
```

## Ejercicio 3: Validaciones Robustas para Formulario de Registro

```python
# registro_validador.py - Validaciones completas para registro de usuario
import re
from datetime import datetime


class ValidadorRegistro:
    """
    Validador robusto para formulario de registro de usuarios.
    Aplica principio de whitelist: solo lo que coincida con patrones
    conocidos es aceptado.
    """

    @staticmethod
    def validar_nombre_usuario(usuario):
        """
        - Solo letras minusculas, numeros, guion bajo
        - Entre 3 y 20 caracteres
        - Debe comenzar con letra
        """
        if not usuario or not isinstance(usuario, str):
            return False, "Nombre de usuario requerido"
        usuario = usuario.strip()
        if len(usuario) < 3 or len(usuario) > 20:
            return False, "Nombre de usuario debe tener entre 3 y 20 caracteres"
        if not re.match(r'^[a-zA-Z][a-zA-Z0-9_]{2,19}$', usuario):
            return False, "Debe comenzar con letra y solo contener letras, numeros y guion bajo"
        return True, usuario

    @staticmethod
    def validar_contrasena(contrasena):
        """
        - Minimo 8 caracteres, maximo 128
        - Al menos 1 mayuscula, 1 minuscula, 1 numero, 1 caracter especial
        - No espacios en blanco
        """
        if not contrasena or not isinstance(contrasena, str):
            return False, "Contrasena requerida"
        if len(contrasena) < 8 or len(contrasena) > 128:
            return False, "Contrasena debe tener entre 8 y 128 caracteres"
        if ' ' in contrasena:
            return False, "Contrasena no puede contener espacios"
        if not re.search(r'[A-Z]', contrasena):
            return False, "Debe contener al menos una mayuscula"
        if not re.search(r'[a-z]', contrasena):
            return False, "Debe contener al menos una minuscula"
        if not re.search(r'[0-9]', contrasena):
            return False, "Debe contener al menos un numero"
        if not re.search(r'[!@#$%^&*(),.?":{}|<>_\-+=\[\]\\;/]', contrasena):
            return False, "Debe contener al menos un caracter especial"
        return True, contrasena

    @staticmethod
    def validar_email(email):
        """RFC 5321 simplificado + verificacion DNS opcional."""
        if not email or not isinstance(email, str):
            return False, "Email requerido"
        email = email.strip().lower()
        if len(email) > 254:
            return False, "Email demasiado largo (max 254 caracteres)"
        if len(email) < 5:
            return False, "Email demasiado corto"
        patron = r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$'
        if not re.match(patron, email):
            return False, "Formato de email invalido"
        local, dominio = email.rsplit('@', 1)
        if len(local) > 64:
            return False, "Parte local del email demasiado larga"
        if dominio.startswith('.') or dominio.endswith('.'):
            return False, "Dominio no puede comenzar o terminar con punto"
        if '..' in dominio:
            return False, "Dominio no puede tener puntos consecutivos"
        return True, email

    @staticmethod
    def validar_telefono(telefono):
        """
        - Solo digitos, +, -, y espacios
        - Entre 7 y 15 digitos
        - Opcional: codigo de pais con +
        """
        if not telefono or not isinstance(telefono, str):
            return False, "Telefono requerido"
        telefono = telefono.strip()
        if not re.match(r'^\+?[\d\s\-]{7,20}$', telefono):
            return False, "Formato de telefono invalido"
        solo_digitos = re.sub(r'[\s\-]', '', telefono)
        if len(solo_digitos) < 7 or len(solo_digitos) > 15:
            return False, "Numero de digitos invalido (7-15 digitos)"
        return True, telefono

    @staticmethod
    def validar_edad(edad):
        """Entero entre 13 y 120."""
        try:
            valor = int(edad)
            if valor < 13:
                return False, "Debes tener al menos 13 anos para registrarte"
            if valor > 120:
                return False, "Edad maxima permitida: 120 anos"
            return True, valor
        except (ValueError, TypeError):
            return False, "Edad debe ser un numero entero"

    @staticmethod
    def validar_codigo_postal(cp, pais='MX'):
        """Valida codigo postal segun pais."""
        if not cp or not isinstance(cp, str):
            return False, "Codigo postal requerido"
        cp = cp.strip()
        patrones = {
            'MX': r'^\d{5}$',
            'US': r'^\d{5}(-\d{4})?$',
            'ES': r'^\d{5}$',
            'AR': r'^\d{4}$',
            'CL': r'^\d{7}$',
        }
        patron = patrones.get(pais.upper())
        if not patron:
            return False, f"Pais {pais} no soportado"
        if not re.match(patron, cp):
            return False, f"Formato de codigo postal invalido para {pais}"
        return True, cp

    @staticmethod
    def validar_terminos(aceptado):
        """Debe ser True explicitamente."""
        if aceptado is not True:
            return False, "Debes aceptar los terminos y condiciones"
        return True, aceptado

    @classmethod
    def validar_registro_completo(cls, datos):
        """
        Valida todos los campos de un registro.
        datos: dict con keys: usuario, contrasena, email, telefono, edad, cp, pais, terminos
        Returns: (valido: bool, errores: dict, datos_limpios: dict)
        """
        errores = {}
        limpios = {}

        # Nombre de usuario
        valido, msg = cls.validar_nombre_usuario(datos.get('usuario'))
        if valido:
            limpios['usuario'] = msg
        else:
            errores['usuario'] = msg

        # Contrasena
        valido, msg = cls.validar_contrasena(datos.get('contrasena'))
        if valido:
            limpios['contrasena'] = msg
        else:
            errores['contrasena'] = msg

        # Email
        valido, msg = cls.validar_email(datos.get('email'))
        if valido:
            limpios['email'] = msg
        else:
            errores['email'] = msg

        # Telefono
        valido, msg = cls.validar_telefono(datos.get('telefono', ''))
        if valido:
            limpios['telefono'] = msg
        else:
            errores['telefono'] = msg

        # Edad
        valido, msg = cls.validar_edad(datos.get('edad'))
        if valido:
            limpios['edad'] = msg
        else:
            errores['edad'] = msg

        # Codigo postal
        valido, msg = cls.validar_codigo_postal(
            datos.get('codigo_postal', ''),
            datos.get('pais', 'MX')
        )
        if valido:
            limpios['codigo_postal'] = msg
        else:
            errores['codigo_postal'] = msg

        # Terminos
        valido, msg = cls.validar_terminos(datos.get('terminos'))
        if valido:
            limpios['terminos'] = True
        else:
            errores['terminos'] = msg

        if errores:
            return False, errores, limpios
        return True, {}, limpios


# ============================================================
# EJEMPLO DE USO
# ============================================================
if __name__ == '__main__':
    datos_validos = {
        'usuario': 'juan123',
        'contrasena': 'Passw0rd!Segura',
        'email': 'juan@example.com',
        'telefono': '+52 55 1234 5678',
        'edad': '25',
        'codigo_postal': '06600',
        'pais': 'MX',
        'terminos': True
    }

    valido, errores, limpios = ValidadorRegistro.validar_registro_completo(datos_validos)
    print("Registro valido:", valido)
    if not valido:
        print("Errores:", errores)
    else:
        print("Datos limpios:", limpios)

    datos_invalidos = {
        'usuario': '<script>',
        'contrasena': 'short',
        'email': 'no-email',
        'telefono': 'abc',
        'edad': '-1',
        'codigo_postal': '123',
        'pais': 'MX',
        'terminos': False
    }

    valido, errores, limpios = ValidadorRegistro.validar_registro_completo(datos_invalidos)
    print("\nRegistro valido:", valido)
    if not valido:
        print("Errores:", errores)
```

## Preguntas y Respuestas

**P1: Cual es la diferencia fundamental entre whitelist y blacklist?**
R: Whitelist (lista blanca) permite solo lo que se sabe que es valido y rechaza todo lo demas, mientras que blacklist (lista negra) bloquea solo lo que se sabe que es malicioso. Whitelist es mas seguro porque no depende de conocer todos los vectores de ataque posibles.

**P2: Que es output encoding y que tipos principales existen?**
R: Output encoding es la tecnica de convertir caracteres especiales en sus equivalentes seguros para evitar que sean interpretados como codigo. Los tipos principales son: HTML encoding (convierte < en &lt;), URL encoding (convierte caracteres a %XX), JavaScript encoding (escapa strings para JS) y CSS encoding.

**P3: Por que se dice que "todos los datos son maliciosos hasta que se demuestre lo contrario"?**
R: Es el principio fundamental de seguridad de entradas. Dato que proviene de una fuente externa (usuario, API, archivo) puede contener diseno malicioso como inyecciones SQL, XSS o command injection. Asumir que todo es malicioso obliga a implementar validacion rigurosa en cada punto de entrada.

**P4: Cual es la diferencia entre sanitizacion y validacion?**
R: Validacion rechaza el dato si no cumple con los criterios establecidos. Sanitizacion modifica el dato para hacerlo seguro (ej: eliminar caracteres peligrosos). Validacion es mas segura porque no confia en que la sanitizacion cubra todos los casos.

**P5: Como se debe validar una direccion de email correctamente?**
R: Verificar formato con expresion regular (local@dominio.tld), longitud maxima de 254 caracteres total (RFC 5321), parte local maxima 64 caracteres, dominio no debe comenzar/terminar con punto ni tener puntos consecutivos. Convertir a minusculas para normalizar.

**P6: Que es OWASP ESAPI y para que sirve?**
R: ESAPI (Enterprise Security API) es una libreria de OWASP que proporciona metodos de seguridad estandarizados para validacion de entradas, output encoding, control de acceso y criptografia. Ayuda a los desarrolladores a implementar controles de seguridad sin tener que escribirlos desde cero.

**P7: Por que no es suficiente escapar solo < y > para prevenir XSS?**
R: Porque XSS puede ocurrir en diferentes contextos: atributos HTML (hay que escapar comillas), eventos (onerror, onload), URLs (javascript:), CSS (expression()), y contextos JavaScript. Cada contexto requiere su tipo especifico de encoding.

## Tarea / Lectura Recomendada

1. **OWASP Input Validation Cheat Sheet:**
   https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html

2. **OWASP XSS Prevention Cheat Sheet:**
   https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html

3. **OWASP ESAPI Documentation:**
   https://owasp.org/www-project-enterprise-security-api/

4. **Tarea practica:** Crear un validador de CSV que rechace archivos con inyeccion de formulas de Excel (=, +, -, @ al inicio de celdas).

5. **Tarea practica:** Implementar un middleware Flask que valide automaticamente todos los parametros de request usando expresiones regulares configuradas por endpoint.


