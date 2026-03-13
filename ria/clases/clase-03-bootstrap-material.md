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

---

### 3. Material Design

#### 3.1 ¿Qué es Material Design?

**Material Design** es el lenguaje de diseño de Google, caracterizado por superficies, sombras y movimiento.

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
