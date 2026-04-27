# 📱 Clase 03: Bootstrap y Material Design - Responsive

**Duración:** 4 horas  
**Objetivo:** Crear interfaces profesionales con Bootstrap 5 y Material Design  
**Proyecto:** Interfaz completa y responsiva para TuFiesta

---

## 📚 Contenido Teórico

### 1. Fundamentos de Diseño Responsive

#### 1.1 ¿Qué es el Diseño Responsive?

El **diseño responsive** crea sitios web que se adaptan a cualquier tamaño de pantalla (móvil, tablet, desktop).

```
┌─────────────────────────────────────────────────────────────────────┐
│                    DISEÑO RESPONSIVE                                  │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   MOBILE FIRST vs DESKTOP FIRST                                     │
│   ───────────────────────────                                      │
│                                                                      │
│   Mobile First: Empezar desde móvil, escalar a desktop            │
│   Desktop First: Empezar desde desktop, adaptar a móvil            │
│                                                                      │
│   ┌─────────┐  ┌─────────────┐  ┌───────────────────┐             │
│   │ Mobile  │  │   Tablet    │  │     Desktop       │             │
│   │ < 768px │  │  768-1024px │  │     > 1024px      │             │
│   └─────────┘  └─────────────┘  └───────────────────┘             │
│   ┌───┐       ┌───┬───┐       ┌───┬───┬───┐                     │
│   │ A │       │ A │ B │       │ A │ B │ C │                     │
│   └───┘       └───┴───┘       └───┴───┴───┘                     │
│                                                                      │
│   Breakpoints comunes:                                               │
│   • 576px  - Teléfonos pequeños                                     │
│   • 768px  - Teléfonos / Tablets                                    │
│   • 992px  - Tablets grandes / Laptops                             │
│   • 1200px - Desktops                                              │
│   • 1400px - Pantallas grandes                                      │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

#### 1.2 Viewport Meta Tag

```html
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```

Este tag es **esencial** para que el diseño responsive funcione en dispositivos móviles.

---

### 2. Bootstrap 5

#### 2.1 ¿Qué es Bootstrap?

**Bootstrap** es el framework CSS más popular para crear interfaces responsive y mobile-first.
https://getbootstrap.com/
https://getbootstrap.com/docs/4.1/getting-started/introduction/
```
┌─────────────────────────────────────────────────────────────────────┐
│                    BOOTSTRAP 5 - CARACTERÍSTICAS                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   ✓ Mobile First                                                    │
│   ✓ Grid System flexible                                            │
│   ✓ Componentes listos para usar                                   │
│   ✓ Personalizable con variables SCSS                               │
│   ✓ Sin jQuery (vanilla JS)                                        │
│   ✓ Soporte para Dark Mode                                          │
│   ✓ RTL support                                                     │
│   ✓ Documentación extensa                                          │
│                                                                      │
│   CDN:                                                              │
│   <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/      │
│   dist/css/bootstrap.min.css" rel="stylesheet">                    │
│   <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/     │
│   dist/js/bootstrap.bundle.min.js"></script>                        │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

#### 2.2 Sistema de Grid

El grid de Bootstrap tiene 12 columnas:

```css
/* Funcionamiento del grid */
.container        /* Ancho fijo con márgenes */
.container-fluid  /* Ancho completo */

.row             /* Fila con flexbox */

.col             /* Columna automática */
.col-1 a col-12 /* Columnas de tamaño fijo */
.col-sm-*        /* Small: ≥576px */
.col-md-*        /* Medium: ≥768px */
.col-lg-*        /* Large: ≥992px */
.col-xl-*        /* X-Large: ≥1200px */
.col-xxl-*       /* XX-Large: ≥1400px */

/* Ejemplo: 3 columnas en desktop, 2 en tablet, 1 en móvil */
<div class="row">
    <div class="col-12 col-md-6 col-lg-4">Columna 1</div>
    <div class="col-12 col-md-6 col-lg-4">Columna 2</div>
    <div class="col-12 col-md-6 col-lg-4">Columna 3</div>
</div>
```

#### 2.3 Componentes Principales

**Navbar:**
```html
<nav class="navbar navbar-expand-lg navbar-dark bg-primary">
    <div class="container-fluid">
        <a class="navbar-brand" href="#">TuFiesta</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" 
                data-bs-target="#navbarNav">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav ms-auto">
                <li class="nav-item">
                    <a class="nav-link active" href="#">Inicio</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="#">Eventos</a>
                </li>
                <li class="nav-item dropdown">
                    <a class="nav-link dropdown-toggle" href="#" 
                       data-bs-toggle="dropdown">Categorías</a>
                    <ul class="dropdown-menu">
                        <li><a class="dropdown-item" href="#">Música</a></li>
                        <li><a class="dropdown-item" href="#">Tecnología</a></li>
                        <li><hr class="dropdown-divider"></li>
                        <li><a class="dropdown-item" href="#">Ver todas</a></li>
                    </ul>
                </li>
            </ul>
        </div>
    </div>
</nav>
```

**Cards:**
```html
<div class="card" style="width: 18rem;">
    <img src="..." class="card-img-top" alt="...">
    <div class="card-body">
        <h5 class="card-title">Concierto de Rock</h5>
        <p class="card-text">Descripción del evento...</p>
        <a href="#" class="btn btn-primary">Comprar</a>
    </div>
</div>
```

**Botones:**
```html
<button class="btn btn-primary">Primary</button>
<button class="btn btn-secondary">Secondary</button>
<button class="btn btn-success">Success</button>
<button class="btn btn-danger">Danger</button>
<button class="btn btn-warning">Warning</button>
<button class="btn btn-info">Info</button>
<button class="btn btn-light">Light</button>
<button class="btn btn-dark">Dark</button>
<button class="btn btn-outline-primary">Outline</button>
```

**Formularios:**
```html
<form>
    <div class="mb-3">
        <label for="email" class="form-label">Email</label>
        <input type="email" class="form-control" id="email" 
               placeholder="nombre@ejemplo.com">
        <div class="form-text">No compartiremos tu email.</div>
    </div>
    <div class="mb-3">
        <label for="password" class="form-label">Contraseña</label>
        <input type="password" class="form-control" id="password">
    </div>
    <div class="mb-3 form-check">
        <input type="checkbox" class="form-check-input" id="recordar">
        <label class="form-check-label" for="recordar">Recordarme</label>
    </div>
    <button type="submit" class="btn btn-primary">Enviar</button>
</form>
```

El concepto de responsividad en Bootstrap es lo que suele costar más al principio. Para entenderlo, no hay que pensar en "tamaños de pantalla", sino en "puntos de quiebre" (Breakpoints).Aquí tienes la guía definitiva paso a paso para dominar el Grid de Bootstrap 5.


📐 1. Teoría de los Breakpoints: El "Cerebro" de BootstrapBootstrap divide la pantalla en 12 columnas invisibles. La resolución se detecta mediante Breakpoints. Un breakpoint es simplemente un ancho de pantalla (en píxeles) donde el diseño "salta" a una nueva configuración.SiglaNombreResolución (Ancho)Dispositivo comúnxsExtra Small< 576pxMóviles verticalessmSmall≥ 576pxMóviles horizontalesmdMedium≥ 768pxTabletslgLarge≥ 992pxLaptops / DesktopsxlX-Large≥ 1200pxMonitores grandesxxlXX-Large≥ 1400pxMonitores Ultra-wideLa Regla de Oro: "Mobile First"Bootstrap funciona de forma ascendente. Si tú escribes col-md-6, significa:"Desde el tamaño Medium en adelante, ocupa 6 columnas".¿Y en tamaños más pequeños (xs)? Ocupará el 100% (12 columnas) por defecto.

🏗️ 2. Anatomía de una Fila (The Row)Para que el grid funcione, siempre debes seguir esta jerarquía:.container: El colchón exterior (centra el contenido)..row: El contenedor de columnas (usa Flexbox)..col-*: Los hijos directos donde va el contenido.


💡 3. Ejemplos Prácticos paso a paso. Vamos a ver cómo se ve el mismo código en diferentes dispositivos.Ejemplo A: El "Espejo" (Mitad y Mitad)Queremos 2 columnas que se pongan una debajo de otra en móvil, pero una al lado de la otra en Tablet.HTML<div class="container">
  <div class="row">
    <div class="col-12 col-md-6 bg-primary text-white"> Columna A </div>
    <div class="col-12 col-md-6 bg-success text-white"> Columna B </div>
  </div>
</div>


En móvil (<768px): Verás dos bloques largos (12/12).En Tablet (>=768px): Verás dos bloques de 50% de ancho (6/12 + 6/12).Ejemplo B: El Complejo (Cambio en 3 niveles)Este es el ejemplo más real. Queremos:Móvil: 1 columna (toda la pantalla).Tablet: 2 columnas.Desktop: 4 columnas.HTML<div class="row">
  <div class="col-12 col-md-6 col-lg-3"> Elemento 1 </div>
  <div class="col-12 col-md-6 col-lg-3"> Elemento 2 </div>
  <div class="col-12 col-md-6 col-lg-3"> Elemento 3 </div>
  <div class="col-12 col-md-6 col-lg-3"> Elemento 4 </div>
</div>


¿Cómo lo interpreta Bootstrap?¿Pantalla > 992px (lg)? Ok, leo col-lg-3. Como 12 / 3 = 4, entran 4 columnas exactas.¿Pantalla entre 768px y 991px (md)? Ignoro el lg y leo col-md-6. Como 12 / 6 = 2, se ven 2 filas con 2 columnas cada una.¿Pantalla < 768px? Ignoro todo y leo col-12. Se ve 1 columna por fila.Ejemplo C: Columnas con "Offset" (Espacios vacíos)A veces quieres centrar una columna pero que no ocupe todo el ancho.HTML<div class="row">
  <div class="col-md-6 offset-md-3 bg-warning">
    Estoy centrado en Desktop
  </div>
</div>


🛠️ 4. ¿Cómo probarlo tú mismo? No necesitas 5 dispositivos físicos para probar esto. Sigue estos pasos:Abre tu archivo HTML con Bootstrap en Chrome.Presiona F12 (Herramientas de Desarrollador).Haz clic en el icono de "Dispositivos" (un icono de un móvil y una tablet arriba a la izquierda de la consola).

Arriba verás una barra de píxeles. Arrastra el borde de la pantalla lentamente:Verás cómo al pasar los 768px o los 992px, tus columnas "saltan" .


📝 Resumen de Clases Útiles:g-* (Gutter): Para cambiar el espacio entre columnas (ej: g-3).align-items-center: Para centrar columnas verticalmente dentro de una fila.justify-content-center: Para centrar columnas horizontalmente si sobran espacios de las 12 disponibles.


🔍 1. La anatomía de la clase (El secreto está en el medio)Una clase de Bootstrap se divide en tres partes:col - [breakpoint] - [número]col: Le dice al navegador "esto es una columna".[breakpoint]: Le dice "CUÁNDO" debe aplicarse (sm, md, lg...).[número]: Le dice "CUÁNTO" espacio ocupar (del 1 al 12).


🚦 2. ¿Por qué se ve distinto? (La Cascada)Imagina que el navegador es un inspector que mide el ancho de la pantalla cada milisegundo. Supongamos que tienes esta clase:class="col-12 col-md-6 col-lg-3"Si la pantalla mide...El navegador dice...Resultado visual400px (Móvil)"Es menor a 768px, ignoro md y lg. Solo veo col-12".1 columna (toda la pantalla)800px (Tablet)" Ya pasamos los 768px. Activo col-md-6".2 columnas (6 + 6 = 12)1200px (PC)"Superamos los 992px. Activo col-lg-3".4 columnas (3+3+3+3 = 12)

🎨 3. Comparativa visual de nombresMira la diferencia sutil en los nombres y cómo cambia el diseño:Caso 1: Diseño Fijo (No cambia nunca)HTML<div class="col-6">Contenido</div>
Nombre: No tiene "apellido" (md, lg).Efecto: Siempre ocupará el 50% de la pantalla, ya sea en un reloj inteligente o en un cine. No es responsivo.Caso 2: Diseño Adaptable (El "Salto")HTML<div class="col-12 col-md-6">Contenido</div>
Nombre: Tiene el "apellido" md.Efecto:En pantallas pequeñas se ve gigante (12).En pantallas medianas "salta" a la mitad (6).

📐 4. El sistema de las 12 columnas (Matemática simple)Bootstrap siempre suma 12. Para saber cuántas cosas verás en una fila, divide 12 entre tu número:col-md-12 $\rightarrow 12 / 12 = \mathbf{1}$ elemento por fila.col-md-6  $\rightarrow 12 / 6 = \mathbf{2}$ elementos por fila.col-md-4  $\rightarrow 12 / 4 = \mathbf{3}$ elementos por fila.col-md-3  $\rightarrow 12 / 3 = \mathbf{4}$ elementos por fila.🛠️ Hagamos el ejercicio de la GaleríaPara que tus alumnos lo entiendan, pídeles que creen una galería de fotos que se comporte así:Móvil: 1 foto por fila (para verla bien grande).Tablet: 2 fotos por fila.PC: 3 fotos por fila.El código que deben escribir:HTML<div class="container">
  <div class="row">
    <div class="col-12 col-md-6 col-lg-4 border p-3"> Foto 1 </div>
    <div class="col-12 col-md-6 col-lg-4 border p-3"> Foto 2 </div>
    <div class="col-12 col-md-6 col-lg-4 border p-3"> Foto 3 </div>
  </div>
</div>


🛠️ Ejercicio: Construcción de una Galería de Carteleras
Objetivo
Crear una página que muestre 3 tarjetas de eventos. El diseño debe adaptarse automáticamente:

Móvil: 1 tarjeta por fila (ocupa las 12 columnas).

Tablet: 2 tarjetas por fila (ocupa 6 columnas cada una).

Desktop: 3 tarjetas por fila (ocupa 4 columnas cada una).

Paso 1: Estructura Base (HTML)
Primero, prepara el documento e incluye Bootstrap 5 mediante el CDN en el <head>.

HTML
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Ejercicio de Grid Bootstrap</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-5">
        <h2 class="text-center mb-4">Próximos Eventos</h2>
        <div class="row g-4" id="contenedor-eventos">
            </div>
    </div>
</body>
</html>


Paso 2: Crear las Columnas Responsivas
Dentro del <div class="row">, añade tres bloques div. Para lograr el cambio de diseño según la resolución, usa los nombres de clase con los "apellidos" de resolución (md para tablet y lg para desktop).

El código para cada columna:

HTML
<div class="col-12 col-md-6 col-lg-4">
    </div>
Paso 3: Agregar el Contenido (Bootstrap Cards)
Inserta una tarjeta dentro de cada columna. Utiliza las clases card, card-body y btn.

Código completo de una tarjeta:

HTML
<div class="col-12 col-md-6 col-lg-4">
    <div class="card h-100">
        <div class="card-body">
            <h5 class="card-title">Concierto de Rock</h5>
            <p class="card-text">Fecha: 25 de Octubre</p>
            <p class="text-muted">Ubicación: Estadio Central</p>
            <button class="btn btn-primary w-100">Ver Detalles</button>
        </div>
    </div>
</div>
Paso 4: Prueba de Resolución
Para verificar que las clases funcionan, los estudiantes deben realizar lo siguiente:

Abrir el archivo en el navegador Chrome.

Presionar F12 para abrir las herramientas de desarrollo.

Activar el modo dispositivo (icono de móvil/tablet).

Cambiar el ancho de la ventana manualmente:

Al reducir a menos de 768px, las tarjetas deben apilarse una sobre otra.

Entre 768px y 991px, deben aparecer dos por fila.

Al superar los 992px, deben aparecer las tres en la misma línea.

📝 Guía de Clases Utilizadas
qué significa cada parte del nombre de la clase en este ejercicio:

container: Centra el contenido y añade márgenes laterales.

row: Activa el sistema de filas basado en Flexbox.

g-4: (Gutter) Añade una separación de nivel 4 entre las columnas para que no se peguen.

col-12: Orden para pantallas de menos de 768px (ocupa todo el ancho).

col-md-6: Orden para tablets (ocupa la mitad, entran 2).

col-lg-4: Orden para computadoras (ocupa un tercio, entran 3).

h-100: Hace que todas las tarjetas tengan la misma altura, aunque el texto sea diferente.
---

### 3. Material Design

#### 3.1 ¿Qué es Material Design?

**Material Design** es el lenguaje de diseño de Google, caracterizado por superficies, sombras y movimiento.

https://m3.material.io/

```
┌─────────────────────────────────────────────────────────────────────┐
│               MATERIAL DESIGN - PRINCIPIOS                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   1. SURFACES (Superficies)                                        │
│      - Todo es una superficie con elevación                         │
│      - Sombras indican profundidad                                  │
│                                                                      │
│   2. MOTION (Movimiento)                                            │
│      - Animaciones significativas                                   │
│      - Transiciones fluidas                                         │
│                                                                      │
│   3. ICONOGRAPHY (Iconografía)                                      │
│      - Íconos consistente                                           │
│      - Sistema de grid                                              │
│                                                                      │
│   4. COLOR                                                          │
│      - Paleta primaria, secundaria, error                            │
│      - Tonos para jerarquía                                         │
│                                                                      │
│   5. TYPOGRAPHY                                                     │
│      - Escala de tipografía                                         │
│      - Roboto como fuente principal                                  │
│                                                                      │
│   Material Icons:                                                    │
│   <link href="https://fonts.googleapis.com/icon?family=Material+Icons"  │
│   rel="stylesheet">                                                │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

#### 3.2 Material CSS (Alternativa ligera)

```html
<!-- Material Icons -->
<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">

<!-- Material CSS (lightweight alternative a Angular Material) -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/material-components-web@latest/dist/material-components-web.min.css">
```

#### 3.3 Componentes Material

**Buttons:**
```html
<button class="mdc-button mdc-button--raised">
    <span class="mdc-button__label">Aceptar</span>
</button>

<button class="mdc-button mdc-button--outlined">
    <span class="mdc-button__label">Cancelar</span>
</button>

<button class="mdc-button mdc-button--text">
    <span class="mdc-button__label">Más info</span>
</button>
```

**Cards:**
```html
<div class="mdc-card">
    <div class="mdc-card__media" style="background-image: url(...)"></div>
    <div class="mdc-card__content">
        <h2 class="mdc-typography--headline6">Concierto</h2>
        <p class="mdc-typography--body2">Descripción...</p>
    </div>
    <div class="mdc-card__actions">
        <button class="mdc-button mdc-card__action">Ver más</button>
        <button class="mdc-button mdc-card__action">Comprar</button>
    </div>
</div>
```

---

### 4. Proyecto: TuFiesta con Bootstrap

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TuFiesta - Eventos</title>
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Bootstrap Icons -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css">
    <style>
        :root {
            --primary: #6366f1;
            --secondary: #ec4899;
        }
        .hero {
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            padding: 80px 0;
        }
        .event-card {
            transition: transform 0.3s;
        }
        .event-card:hover {
            transform: translateY(-5px);
        }
    </style>
</head>
<body>
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark sticky-top">
        <div class="container">
            <a class="navbar-brand" href="#">
                <i class="bi bi-calendar-event"></i> TuFiesta
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" 
                    data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item"><a class="nav-link active" href="#">Inicio</a></li>
                    <li class="nav-item"><a class="nav-link" href="#eventos">Eventos</a></li>
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="#" data-bs-toggle="dropdown">
                            Categorías
                        </a>
                        <ul class="dropdown-menu">
                            <li><a class="dropdown-item" href="#">Música</a></li>
                            <li><a class="dropdown-item" href="#">Tecnología</a></li>
                            <li><a class="dropdown-item" href="#">Deportes</a></li>
                        </ul>
                    </li>
                    <li class="nav-item"><a class="nav-link" href="#">Contacto</a></li>
                </ul>
                <form class="d-flex ms-3">
                    <input class="form-control me-2" type="search" placeholder="Buscar...">
                    <button class="btn btn-outline-light" type="submit">
                        <i class="bi bi-search"></i>
                    </button>
                </form>
            </div>
        </div>
    </nav>

    <!-- Hero Section -->
    <section class="hero text-white text-center">
        <div class="container">
            <h1 class="display-4 fw-bold">Descubre Eventos Increíbles</h1>
            <p class="lead mb-4">Encuentra y compra entradas para los mejores eventos</p>
            <div class="row justify-content-center">
                <div class="col-md-8">
                    <div class="input-group input-group-lg">
                        <span class="input-group-text bg-white border-0">
                            <i class="bi bi-search"></i>
                        </span>
                        <input type="text" class="form-control border-0" 
                               placeholder="¿Qué evento buscas?">
                        <button class="btn btn-light" type="button">Buscar</button>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Filtros -->
    <section class="py-4 bg-light">
        <div class="container">
            <div class="row align-items-center">
                <div class="col-md-3">
                    <h5 class="mb-0">Filtrar por:</h5>
                </div>
                <div class="col-md-9">
                    <div class="btn-group" role="group">
                        <button type="button" class="btn btn-outline-primary active">Todos</button>
                        <button type="button" class="btn btn-outline-primary">Música</button>
                        <button type="button" class="btn btn-outline-primary">Tecnología</button>
                        <button type="button" class="btn btn-outline-primary">Deportes</button>
                        <button type="button" class="btn btn-outline-primary">Arte</button>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Eventos Grid -->
    <section id="eventos" class="py-5">
        <div class="container">
            <h2 class="mb-4">Próximos Eventos</h2>
            <div class="row g-4">
                <!-- Evento 1 -->
                <div class="col-12 col-md-6 col-lg-4 col-xl-3">
                    <div class="card h-100 event-card shadow-sm">
                        <img src="https://picsum.photos/400/250" class="card-img-top" alt="Evento">
                        <div class="card-body">
                            <span class="badge bg-primary mb-2">Música</span>
                            <h5 class="card-title">Concierto de Rock</h5>
                            <p class="card-text text-muted small">
                                <i class="bi bi-calendar"></i> 15 Dic 2024<br>
                                <i class="bi bi-geo-alt"></i> Estadio Centenario
                            </p>
                        </div>
                        <div class="card-footer bg-white border-top-0">
                            <div class="d-flex justify-content-between align-items-center">
                                <span class="h5 text-primary mb-0">$1.500</span>
                                <button class="btn btn-primary btn-sm">Comprar</button>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Evento 2 -->
                <div class="col-12 col-md-6 col-lg-4 col-xl-3">
                    <div class="card h-100 event-card shadow-sm">
                        <img src="https://picsum.photos/401/250" class="card-img-top" alt="Evento">
                        <div class="card-body">
                            <span class="badge bg-success mb-2">Tecnología</span>
                            <h5 class="card-title">Tech Conference</h5>
                            <p class="card-text text-muted small">
                                <i class="bi bi-calendar"></i> 10 Ene 2025<br>
                                <i class="bi bi-geo-alt"></i> Punta del Este
                            </p>
                        </div>
                        <div class="card-footer bg-white border-top-0">
                            <div class="d-flex justify-content-between align-items-center">
                                <span class="h5 text-primary mb-0">$2.500</span>
                                <button class="btn btn-primary btn-sm">Comprar</button>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Evento 3 -->
                <div class="col-12 col-md-6 col-lg-4 col-xl-3">
                    <div class="card h-100 event-card shadow-sm">
                        <img src="https://picsum.photos/402/250" class="card-img-top" alt="Evento">
                        <div class="card-body">
                            <span class="badge bg-warning text-dark mb-2">Comedia</span>
                            <h5 class="card-title">Stand Up Night</h5>
                            <p class="card-text text-muted small">
                                <i class="bi bi-calendar"></i> 28 Dic 2024<br>
                                <i class="bi bi-geo-alt"></i> La Casa de la Comedy
                            </p>
                        </div>
                        <div class="card-footer bg-white border-top-0">
                            <div class="d-flex justify-content-between align-items-center">
                                <span class="h5 text-primary mb-0">$350</span>
                                <button class="btn btn-primary btn-sm">Comprar</button>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Evento 4 -->
                <div class="col-12 col-md-6 col-lg-4 col-xl-3">
                    <div class="card h-100 event-card shadow-sm">
                        <img src="https://picsum.photos/403/250" class="card-img-top" alt="Evento">
                        <div class="card-body">
                            <span class="badge bg-info mb-2">Arte</span>
                            <h5 class="card-title">Festival de Arte</h5>
                            <p class="card-text text-muted small">
                                <i class="bi bi-calendar"></i> 5 Ene 2025<br>
                                <i class="bi bi-geo-alt"></i> Centro Cultural
                            </p>
                        </div>
                        <div class="card-footer bg-white border-top-0">
                            <div class="d-flex justify-content-between align-items-center">
                                <span class="h5 text-primary mb-0">$600</span>
                                <button class="btn btn-primary btn-sm">Comprar</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Paginación -->
            <nav class="mt-5" aria-label="Paginación">
                <ul class="pagination justify-content-center">
                    <li class="page-item disabled">
                        <a class="page-link" href="#">Anterior</a>
                    </li>
                    <li class="page-item active"><a class="page-link" href="#">1</a></li>
                    <li class="page-item"><a class="page-link" href="#">2</a></li>
                    <li class="page-item"><a class="page-link" href="#">3</a></li>
                    <li class="page-item">
                        <a class="page-link" href="#">Siguiente</a>
                    </li>
                </ul>
            </nav>
        </div>
    </section>

    <!-- Footer -->
    <footer class="bg-dark text-white py-4">
        <div class="container">
            <div class="row">
                <div class="col-md-4">
                    <h5>TuFiesta</h5>
                    <p class="text-muted">Tu plataforma de eventos favorita</p>
                </div>
                <div class="col-md-4">
                    <h5>Enlaces</h5>
                    <ul class="list-unstyled">
                        <li><a href="#" class="text-muted text-decoration-none">Sobre nosotros</a></li>
                        <li><a href="#" class="text-muted text-decoration-none">Términos</a></li>
                        <li><a href="#" class="text-muted text-decoration-none">Privacidad</a></li>
                    </ul>
                </div>
                <div class="col-md-4">
                    <h5>Contacto</h5>
                    <p class="text-muted">
                        <i class="bi bi-envelope"></i> contacto@tufiesta.uy<br>
                        <i class="bi bi-phone"></i> +598 1234 5678
                    </p>
                </div>
            </div>
            <hr>
            <p class="text-center text-muted mb-0">&copy; 2024 TuFiesta</p>
        </div>
    </footer>

    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

---

## 🛠️ Ejercicios Prácticos

1. Crear layout completo con Bootstrap
2. Implementar navbar responsive
3. Crear grid de eventos con filtros
4. Agregar modales de compra

---

## 📚 Recursos

- [Bootstrap 5 Docs](https://getbootstrap.com/docs/5.3/)
- [Material Design](https://material.io/)
- [Bootstrap Icons](https://icons.getbootstrap.com/)
