# 📱 Clase 01: HTML, CSS y Fundamentos del DOM

**Duración:** 4 horas  
**Objetivo:** Dominar HTML5 semántico, CSS3 moderno y entender la estructura del DOM  
**Proyecto:** Estructura de la página de inicio para el sistema de eventos TuFiesta

---

## 📚 Contenido Teórico

### 1. Fundamentos de la Web

#### 1.1 ¿Cómo funciona la Web?

Para entender el desarrollo web, es fundamental comprender cómo funciona la comunicación entre clientes y servidores:

```
┌─────────────────────────────────────────────────────────────────────┐
│                    CÓMO FUNCIONA LA WEB                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   NAVEGADOR (Cliente)                          SERVIDOR              │
│   ┌─────────────────┐                         ┌─────────────────┐   │
│   │ 1. Solicita     │ ─────────────────────► │ Recibe request  │   │
│   │    URL          │    HTTP Request         │ Busca recurso   │   │
│   └─────────────────┘                         └────────┬────────┘   │
│          ▲                                               │           │
│          │                                               ▼           │
│   ┌──────┴──────┐                         ┌─────────────────┐   │
│   │ 6. Renderiza│ ◄────────────────────── │ Devuelve        │   │
│   │   HTML/CSS  │    HTTP Response        │ HTML + CSS + JS │   │
│   └─────────────┘    (200 OK)             └─────────────────┘   │
│                                                                      │
│   Pasos:                                                            │
│   1. Usuario escribe URL en el navegador                           │
│   2. Navegador resuelve DNS (dominio → IP)                         │
│   3. Navegador envía HTTP request al servidor                      │
│   4. Servidor procesa la petición                                  │
│   5. Servidor responde con archivos                                │
│   6. Navegador renderiza y muestra la página                       │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

#### 1.2 Componentes de una Página Web

| Componente | Descripción |
|------------|-------------|
| **HTML** | Estructura y contenido |
| **CSS** | Presentación y diseño |
| **JavaScript** | Interactividad y comportamiento |
| **Imágenes/Media** | Contenido visual |

---

### 2. HTML5 - El Esqueleto de la Web

#### 2.1 ¿Qué es HTML?

**HTML (HyperText Markup Language)** es el lenguaje de marcado estándar para crear páginas web. Define la estructura y el significado del contenido.

**Evolución:**
- **HTML 4.01 (1999)** - Versión anterior
- **XHTML (2000)** - HTML como XML
- **HTML5 (2014)** - Actual, con nuevas etiquetas semánticas

#### 2.2 Estructura Básica de un Documento HTML

```html
<!DOCTYPE html>           <!-- Declara que es HTML5 -->
<html lang="es">          <!-- Idioma del documento -->
<head>
    <!-- Metadatos - información sobre la página -->
    <meta charset="UTF-8">           <!-- Codificación de caracteres -->
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="TuFiesta - Encuentra los mejores eventos">
    <meta name="keywords" content="eventos, entradas, conciertos, teatro">
    <title>TuFiesta - Eventos</title>
    <!-- Recursos externos -->
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <!-- Contenido visible -->
    <header>
        <h1>Bienvenido a TuFiesta</h1>
    </header>
    <main>
        <section>
            <h2>Próximos Eventos</h2>
        </section>
    </main>
    <footer>
        <p>&copy; 2024 TuFiesta</p>
    </footer>
    <!-- Scripts al final para mejor rendimiento -->
    <script src="app.js"></script>
</body>
</html>
```

#### 2.3 Etiquetas Semánticas

Las **etiquetas semánticas** describen el significado del contenido, no solo su apariencia. Esto beneficia al SEO y accesibilidad.

```
┌─────────────────────────────────────────────────────────────────────┐
│                    ETIQUETAS SEMÁNTICAS DE HTML5                    │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   <header>      - Encabezado de página o sección                   │
│   <nav>         - Navegación principal                              │
│   <main>        - Contenido principal                               │
│   <section>     - Sección temática                                  │
│   <article>     - Contenido independiente (ej: evento)             │
│   <aside>       - Contenido relacionado                             │
│   <footer>      - Pie de página                                     │
│   <details>     - Información expandible                            │
│   <summary>     - Resumen de details                               │
│   <figure>      - Contenido ilustrado                               │
│   <figcaption>  - Leyenda de figure                                │
│   <time>        - Representa fecha/hora                            │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

**Ejemplo en el proyecto TuFiesta:**

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="TuFiesta - Encuentra y compra entradas para los mejores eventos en Uruguay">
    <title>TuFiesta - Tu Plataforma de Eventos</title>
</head>
<body>
    <!-- Encabezado principal -->
    <header role="banner">
        <nav role="navigation" aria-label="Navegación principal">
            <a href="/" class="logo">🎉 TuFiesta</a>
            <ul>
                <li><a href="/eventos">Eventos</a></li>
                <li><a href="/categorias">Categorías</a></li>
                <li><a href="/login">Iniciar Sesión</a></li>
            </ul>
        </nav>
    </header>

    <!-- Contenido principal -->
    <main role="main">
        <!-- Sección Hero -->
        <section id="hero" aria-labelledby="hero-title">
            <h1 id="hero-title">Descubre Eventos Increíbles</h1>
            <p>Encuentra los mejores eventos cerca de ti</p>
        </section>

        <!-- Lista de eventos destacados -->
        <section id="eventos-destacados" aria-labelledby="destacados-title">
            <h2 id="destacados-title">Eventos Destacados</h2>
            
            <!-- Cada evento es un article independiente -->
            <article class="evento-card" aria-labelledby="evento-1-titulo">
                <img src="/img/concierto.jpg" alt="Concierto de Rock">
                <h3 id="evento-1-titulo">Concierto de Rock</h3>
                <p><time datetime="2024-12-15">15 de Diciembre, 2024</time></p>
                <p>Estadio Centenario</p>
                <span class="precio">$1.500</span>
                <button>Comprar Entrada</button>
            </article>
            
            <article class="evento-card" aria-labelledby="evento-2-titulo">
                <img src="/img/festival.jpg" alt="Festival de Jazz">
                <h3 id="evento-2-titulo">Festival de Jazz</h3>
                <p><time datetime="2024-12-20">20 de Diciembre, 2024</time></p>
                <p>Teatro Solís</p>
                <span class="precio">$800</span>
                <button>Comprar Entrada</button>
            </article>
        </section>
        
        <!-- Barra lateral con eventos relacionados -->
        <aside role="complementary" aria-label="Próximos eventos">
            <h3>Próximamente</h3>
            <ul>
                <li>Tech Conference 2024</li>
                <li>Stand Up Comedy Night</li>
                <li>Festival de Arte</li>
            </ul>
        </aside>
    </main>

    <!-- Pie de página -->
    <footer role="contentinfo">
        <p>&copy; 2024 TuFiesta. Todos los derechos reservados.</p>
        <address>contacto@tufiesta.uy</address>
    </footer>
</body>
</html>
```

#### 2.4 Accesibilidad en HTML (WCAG Basics)

La accesibilidad web ensures que personas con discapacidades puedan usar la web.

```
┌─────────────────────────────────────────────────────────────────────┐
│                    ATRIBUTOS DE ACCESIBILIDAD                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Atributos esenciales:                                              │
│  ───────────────────                                                │
│  • lang="es"          - Idioma del contenido                       │
│  • alt="descripción"  - Texto alternativo para imágenes             │
│  • title="tooltip"    - Información adicional                       │
│  • aria-label         - Etiqueta para lectores de pantalla         │
│  • role               - Rol semántico del elemento                 │
│  • aria-labelledby    - Vincula a elemento que describe            │
│  • aria-describedby   - Vincula a descripción                      │
│  • tabindex           - Orden de navegación por teclado             │
│  • disabled           - Deshabilita elemento                        │
│  • required           - Campo obligatorio                           │
│                                                                      │
│  Ejemplos:                                                          │
│  <img src="concierto.jpg" alt="Concierto de Rock en el Estadio">    │
│  <button aria-label="Cerrar menú">✕</button>                       │
│  <input type="email" aria-describedby="email-help" required>        │
│  <p id="email-help">Ingresa tu email profesional</p>              │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

### 3. CSS3 - El Estilo de la Web

#### 3.1 ¿Qué es CSS?

**CSS (Cascading Style Sheets)** controla la presentación visual: colores, fuentes, espaciado, diseño, y más.

**Tipos de selectores:**
```css
/* Elemento */
p { color: blue; }

/* Clase */
.evento-card { border: 1px solid #ddd; }

/* ID */
#header { background: white; }

/* Atributo */
input[type="email"] { border: 1px solid blue; }

/* Descendiente */
nav a { text-decoration: none; }

/* Hijo */
ul > li { display: inline; }

/* Pseudo-clase */
a:hover { color: red; }
a:active { color: orange; }
input:focus { border-color: blue; }

/* Pseudo-elemento */
p::first-line { font-weight: bold; }
```

#### 3.2 Modelo de Caja (Box Model)

```
┌─────────────────────────────────────────────────────────────────────┐
│                        BOX MODEL                                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   ┌───────────────────────────────────────────────────────┐        │
│   │                    MARGIN (externo)                    │        │
│   │  ┌─────────────────────────────────────────────────┐   │        │
│   │  │                  BORDER                          │   │        │
│   │  │  ┌─────────────────────────────────────────┐    │   │        │
│   │  │  │              PADDING                     │    │   │        │
│   │  │  │  ┌───────────────────────────────┐      │    │   │        │
│   │  │  │  │                               │      │    │   │        │
│   │  │  │  │         CONTENT               │      │    │   │        │
│   │  │  │  │      (ancho x alto)           │      │    │   │        │
│   │  │  │  │                               │      │    │   │        │
│   │  │  │  └───────────────────────────────┘      │    │   │        │
│   │  │  └─────────────────────────────────────────┘    │   │        │
│   │  └─────────────────────────────────────────────────┘   │        │
│   └───────────────────────────────────────────────────────────┘        │
│                                                                      │
│   Ancho total = width + padding + border + margin                   │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

**Importante:** En CSS moderno, usamos `box-sizing: border-box` para incluir padding y border en el width.

```css
/* Reset moderno */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}
```

#### 3.3 Flexbox - Diseño Flexible

Flexbox es un módulo de diseño unidimensional para distribuir espacio entre items.

```
┌─────────────────────────────────────────────────────────────────────┐
│                         FLEXBOX                                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   CONTAINER (display: flex)                                         │
│   ────────────────────────                                          │
│   justify-content:                                                  │
│   ┌───┐   ┌───┐   ┌───┐   ┌───┐                                    │
│   │ A │   │ B │   │ C │   │ D │   flex-start (default)            │
│   └───┘   └───┘   └───┘   └───┘                                    │
│                                                                      │
│   ┌───┐   ┌───┐   ┌───┐   ┌───┐                                    │
│   │ A │   │ B │   │ C │   │ D │   center                          │
│   └───┘   └───┘   └───┘   └───┘                                    │
│                                                                      │
│   ┌───┐   ┌───┐   ┌───┐   ┌───┐                                    │
│   │ A │   │ B │   │ C │   │ D │   space-between                   │
│   └───┘   └───┘   └───┘   └───┘                                    │
│                                                                      │
│   ┌───┐   ┌───┐   ┌───┐   ┌───┐                                    │
│   │ A │   │ B │   │ C │   │ D │   space-around                    │
│   └───┘   └───┘   └───┘   └───┘                                    │
│                                                                      │
│   align-items:                                                      │
│   ┌─────────┐                                                       │
│   │    A    │   flex-start                                        │
│   ├─────────┤                                                       │
│   │  B  │ C │   center                                            │
│   ├─────────┤                                                       │
│   │    D    │   flex-end                                          │
│   └─────────┘                                                       │
│                                                                      │
│   flex-direction:                                                   │
│   row (default)     │    column                                     │
│   ┌┬┬┬┐            │    ┌┐                                        │
│   ├┼┼┼┤            │    ├┤                                        │
│   ├┼┼┼┤            │    ├┤                                        │
│   └┴┴┴┘            │    └┤                                        │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

**Ejemplo - Layout de tarjetas de eventos:**

```css
/* Contenedor de eventos */
.eventos-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    justify-content: center;
    padding: 20px;
}

/* Tarjeta de evento */
.evento-card {
    display: flex;
    flex-direction: column;
    width: 300px;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease;
}

.evento-card:hover {
    transform: translateY(-5px);
}

.evento-card img {
    width: 100%;
    height: 200px;
    object-fit: cover;
}

.evento-card .contenido {
    padding: 16px;
    flex: 1;
    display: flex;
    flex-direction: column;
}

.evento-card .precio {
    margin-top: auto;
    font-size: 1.25rem;
    font-weight: bold;
    color: #6366f1;
}
```

#### 3.4 CSS Grid - Diseño en Dos Dimensiones

CSS Grid es ideal para layouts complejos.

```
┌─────────────────────────────────────────────────────────────────────┐
│                           CSS GRID                                    │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   grid-template-columns: repeat(3, 1fr)                             │
│   ┌─────────┬─────────┬─────────┐                                   │
│   │    A    │    B    │    C    │                                   │
│   ├─────────┼─────────┼─────────┤                                   │
│   │    D    │    E    │    F    │                                   │
│   ├─────────┼─────────┼─────────┤                                   │
│   │    G    │    H    │    I    │                                   │
│   └─────────┴─────────┴─────────┘                                   │
│                                                                      │
│   Ejemplo de layout típico:                                         │
│   ┌─────────────────────────────────────────┐                       │
│   │ HEADER (span 3)                        │                       │
│   ├─────────────┬───────────────────────────┤                       │
│   │ SIDEBAR     │    MAIN CONTENT           │                       │
│   │ (span 1)    │    (span 2)              │                       │
│   ├─────────────┼───────────────────────────┤                       │
│   │ FOOTER (span 3)                        │                       │
│   └─────────────────────────────────────────┘                       │
│                                                                      │
│   Código:                                                           │
│   .container {                                                      │
│       display: grid;                                                │
│       grid-template-columns: 250px 1fr;                             │
│       grid-template-rows: auto 1fr auto;                            │
│       min-height: 100vh;                                           │
│   }                                                                 │
│                                                                      │
│   .header { grid-column: 1 / -1; }                                 │
│   .sidebar { }                                                     │
│   .main { }                                                        │
│   .footer { grid-column: 1 / -1; }                                │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

**Grid para el proyecto TuFiesta:**

```css
/* Layout principal con Grid */
.page-layout {
    display: grid;
    grid-template-columns: 1fr 300px;  /* Contenido + Sidebar */
    grid-template-areas:
        "header header"
        "main aside"
        "footer footer";
    gap: 30px;
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

.page-layout header { grid-area: header; }
.page-layout main { grid-area: main; }
.page-layout aside { grid-area: aside; }
.page-layout footer { grid-area: footer; }

/* Grid de eventos */
.eventos-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 24px;
}

/* Responsive: una columna en móvil */
@media (max-width: 768px) {
    .page-layout {
        grid-template-columns: 1fr;
        grid-template-areas:
            "header"
            "main"
            "aside"
            "footer";
    }
}
```

#### 3.5 Variables CSS

Las variables CSS permiten reutilizar valores en todo el documento.

```css
:root {
    /* Colores */
    --color-primary: #6366f1;
    --color-secondary: #ec4899;
    --color-success: #10b981;
    --color-error: #ef4444;
    --color-warning: #f59e0b;
    
    /* Colores del tema */
    --color-bg: #ffffff;
    --color-text: #1f2937;
    --color-text-muted: #6b7280;
    --color-border: #e5e7eb;
    
    /* Espaciado */
    --spacing-xs: 0.25rem;
    --spacing-sm: 0.5rem;
    --spacing-md: 1rem;
    --spacing-lg: 1.5rem;
    --spacing-xl: 2rem;
    
    /* Bordes */
    --border-radius: 8px;
    --border-radius-lg: 12px;
    
    /* Sombras */
    --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
    --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1);
    --shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.1);
    
    /* Transiciones */
    --transition-fast: 150ms ease;
    --transition-normal: 300ms ease;
}

/* Usar variables */
.button {
    background-color: var(--color-primary);
    border-radius: var(--border-radius);
    transition: background-color var(--transition-fast);
}

.button:hover {
    background-color: var(--color-secondary);
}
```

---

### 4. El DOM - Modelo de Objetos del Documento

#### 4.1 ¿Qué es el DOM?

El **DOM (Document Object Model)** es una representación en memoria de la estructura HTML que permite a JavaScript manipular la página.

```
┌─────────────────────────────────────────────────────────────────────┐
│                         DOM TREE                                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│                        document                                      │
│                           │                                          │
│                    ┌──────┴──────┐                                  │
│                    ▼             ▼                                   │
│                  html         (otros nodos)                         │
│                   │                                                │
│           ┌───────┴───────┐                                         │
│           ▼               ▼                                         │
│        head             body                                         │
│    ┌────┴────┐      ┌────┴────┐                                    │
│    ▼         ▼      ▼         ▼                                     │
│  title     meta    header    main    aside    footer                │
│   │         │       │        │       │        │                    │
│   │         │       │       ┌─┴──┐   │        │                    │
│   │         │       │       ▼    ▼   ▼        │                    │
│  texto   atributos  nav   section section  p                      │
│                                  │       │                          │
│                                  ▼       ▼                          │
│                              article  ul                           │
│                                │       │                           │
│                                ▼       ▼                           │
│                               h2       li                          │
│                                                                      │
│   NODOS del DOM:                                                    │
│   • Element nodes (<div>, <p>, <span>)                             │
│   • Text nodes (contenido de texto)                                │
│   • Attribute nodes (class, id, src)                               │
│   • Comment nodes (<!-- comentario -->)                            │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

#### 4.2 Relación entre HTML, CSS y JavaScript

```
┌─────────────────────────────────────────────────────────────────────┐
│              RELACIÓN HTML + CSS + JavaScript                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   HTML (Estructura)                                                │
│   ─────────────────                                                 │
│   <div id="evento-1" class="card">                                │
│       <h3>Concierto</h3>                                          │
│       <p class="precio">$500</p>                                   │
│   </div>                                                           │
│                                                                      │
│   CSS (Estilo)                                                      │
│   ───────────                                                      │
│   .card { border: 1px solid #ddd; padding: 16px; }               │
│   .precio { color: blue; font-weight: bold; }                    │
│                                                                      │
│   JavaScript (Comportamiento)                                      │
│   ─────────────────────────                                         │
│   const card = document.getElementById('evento-1');                │
│   card.addEventListener('click', () => alert('Comprar!'));        │
│                                                                      │
│   Resultado: Elemento estilado con interactividad                   │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 💻 Contenido Práctico

### 5. Implementación del Proyecto - Clase 01

```html
<!-- index.html - Estructura completa del proyecto TuFiesta -->
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="TuFiesta - Encuentra los mejores eventos en Uruguay">
    <title>TuFiesta - Tu Plataforma de Eventos</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <!-- Header -->
    <header class="site-header">
        <div class="container">
            <a href="/" class="logo">🎉 TuFiesta</a>
            <nav class="main-nav" aria-label="Navegación principal">
                <ul>
                    <li><a href="/">Inicio</a></li>
                    <li><a href="/eventos">Eventos</a></li>
                    <li><a href="/categorias">Categorías</a></li>
                </ul>
            </nav>
            <div class="auth-buttons">
                <a href="/login" class="btn btn-outline">Iniciar Sesión</a>
                <a href="/register" class="btn btn-primary">Registrarse</a>
            </div>
        </div>
    </header>

    <!-- Main -->
    <main>
        <!-- Hero Section -->
        <section class="hero">
            <div class="container">
                <h1>Descubre Eventos Increíbles</h1>
                <p>Encuentra y compra entradas para los mejores eventos cerca de ti</p>
                <form class="search-box" role="search">
                    <input type="search" placeholder="Buscar eventos..." aria-label="Buscar eventos">
                    <button type="submit">Buscar</button>
                </form>
            </div>
        </section>

        <!-- Eventos Section -->
        <section class="eventos-section">
            <div class="container">
                <h2>Próximos Eventos</h2>
                
                <div class="eventos-grid">
                    <!-- Evento 1 -->
                    <article class="evento-card">
                        <div class="evento-imagen">
                            <img src="/images/concierto.jpg" alt="Concierto de Rock">
                            <span class="categoria-badge">Música</span>
                        </div>
                        <div class="evento-contenido">
                            <h3>Concierto de Rock</h3>
                            <p class="evento-fecha">
                                <time datetime="2024-12-15">15 de Diciembre, 2024</time>
                            </p>
                            <p class="evento-ubicacion">📍 Estadio Centenario, Montevideo</p>
                            <div class="evento-footer">
                                <span class="precio">$1.500</span>
                                <button class="btn btn-primary">Comprar</button>
                            </div>
                        </div>
                    </article>

                    <!-- Evento 2 -->
                    <article class="evento-card">
                        <div class="evento-imagen">
                            <img src="/images/festival.jpg" alt="Festival de Jazz">
                            <span class="categoria-badge">Música</span>
                        </div>
                        <div class="evento-contenido">
                            <h3>Festival de Jazz</h3>
                            <p class="evento-fecha">
                                <time datetime="2024-12-20">20 de Diciembre, 2024</time>
                            </p>
                            <p class="evento-ubicacion">📍 Teatro Solís, Montevideo</p>
                            <div class="evento-footer">
                                <span class="precio">$800</span>
                                <button class="btn btn-primary">Comprar</button>
                            </div>
                        </div>
                    </article>

                    <!-- Evento 3 -->
                    <article class="evento-card">
                        <div class="evento-imagen">
                            <img src="/images/tech.jpg" alt="Tech Conference">
                            <span class="categoria-badge">Tecnología</span>
                        </div>
                        <div class="evento-contenido">
                            <h3>Tech Conference 2024</h3>
                            <p class="evento-fecha">
                                <time datetime="2025-01-10">10 de Enero, 2025</time>
                            </p>
                            <p class="evento-ubicacion">📍 Punta del Este Convention</p>
                            <div class="evento-footer">
                                <span class="precio">$2.500</span>
                                <button class="btn btn-primary">Comprar</button>
                            </div>
                        </div>
                    </article>

                    <!-- Evento 4 -->
                    <article class="evento-card">
                        <div class="evento-imagen">
                            <img src="/images/comedy.jpg" alt="Stand Up Comedy">
                            <span class="categoria-badge">Comedia</span>
                        </div>
                        <div class="evento-contenido">
                            <h3>Stand Up Comedy Night</h3>
                            <p class="evento-fecha">
                                <time datetime="2024-12-28">28 de Diciembre, 2024</time>
                            </p>
                            <p class="evento-ubicacion">📍 La Casa de la Comedy</p>
                            <div class="evento-footer">
                                <span class="precio">$350</span>
                                <button class="btn btn-primary">Comprar</button>
                            </div>
                        </div>
                    </article>
                </div>
            </div>
        </section>
    </main>

    <!-- Footer -->
    <footer class="site-footer">
        <div class="container">
            <p>&copy; 2024 TuFiesta. Todos los derechos reservados.</p>
            <nav aria-label="Navegación del pie">
                <a href="/terminos">Términos</a>
                <a href="/privacidad">Privacidad</a>
                <a href="/contacto">Contacto</a>
            </nav>
            <address>contacto@tufiesta.uy</address>
        </div>
    </footer>

    <script src="app.js"></script>
</body>
</html>
```

```css
/* styles.css - Estilos completos */

/* Variables */
:root {
    --color-primary: #6366f1;
    --color-primary-dark: #4f46e5;
    --color-secondary: #ec4899;
    --color-success: #10b981;
    --color-bg: #ffffff;
    --color-bg-secondary: #f9fafb;
    --color-text: #1f2937;
    --color-text-muted: #6b7280;
    --color-border: #e5e7eb;
    --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
    --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1);
    --radius: 8px;
    --radius-lg: 12px;
    --transition: 0.3s ease;
}

/* Reset */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    color: var(--color-text);
    line-height: 1.6;
    background-color: var(--color-bg);
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}

/* Header */
.site-header {
    background: white;
    box-shadow: var(--shadow-sm);
    position: sticky;
    top: 0;
    z-index: 100;
}

.site-header .container {
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 70px;
}

.logo {
    font-size: 1.5rem;
    font-weight: bold;
    text-decoration: none;
    color: var(--color-primary);
}

.main-nav ul {
    display: flex;
    list-style: none;
    gap: 30px;
}

.main-nav a {
    text-decoration: none;
    color: var(--color-text);
    font-weight: 500;
    transition: color var(--transition);
}

.main-nav a:hover {
    color: var(--color-primary);
}

.auth-buttons {
    display: flex;
    gap: 10px;
}

/* Buttons */
.btn {
    padding: 10px 20px;
    border-radius: var(--radius);
    text-decoration: none;
    font-weight: 500;
    cursor: pointer;
    border: none;
    transition: all var(--transition);
}

.btn-primary {
    background: var(--color-primary);
    color: white;
}

.btn-primary:hover {
    background: var(--color-primary-dark);
}

.btn-outline {
    border: 2px solid var(--color-primary);
    color: var(--color-primary);
}

.btn-outline:hover {
    background: var(--color-primary);
    color: white;
}

/* Hero */
.hero {
    background: linear-gradient(135deg, var(--color-primary), var(--color-secondary));
    color: white;
    padding: 80px 0;
    text-align: center;
}

.hero h1 {
    font-size: 3rem;
    margin-bottom: 20px;
}

.hero p {
    font-size: 1.25rem;
    margin-bottom: 30px;
    opacity: 0.9;
}

/* Search Box */
.search-box {
    display: flex;
    max-width: 500px;
    margin: 0 auto;
    background: white;
    border-radius: var(--radius-lg);
    overflow: hidden;
}

.search-box input {
    flex: 1;
    padding: 15px 20px;
    border: none;
    outline: none;
    font-size: 1rem;
}

.search-box button {
    padding: 15px 30px;
    background: var(--color-primary);
    color: white;
    border: none;
    cursor: pointer;
}

/* Eventos Section */
.eventos-section {
    padding: 60px 0;
    background: var(--color-bg-secondary);
}

.eventos-section h2 {
    text-align: center;
    margin-bottom: 40px;
    font-size: 2rem;
}

/* Eventos Grid */
.eventos-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 30px;
}

/* Evento Card */
.evento-card {
    background: white;
    border-radius: var(--radius-lg);
    overflow: hidden;
    box-shadow: var(--shadow-md);
    transition: transform var(--transition), box-shadow var(--transition);
}

.evento-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
}

.evento-imagen {
    position: relative;
    height: 200px;
    overflow: hidden;
}

.evento-imagen img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.categoria-badge {
    position: absolute;
    top: 10px;
    right: 10px;
    background: var(--color-primary);
    color: white;
    padding: 5px 12px;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 500;
}

.evento-contenido {
    padding: 20px;
}

.evento-contenido h3 {
    margin-bottom: 10px;
    font-size: 1.25rem;
}

.evento-fecha, .evento-ubicacion {
    color: var(--color-text-muted);
    font-size: 0.9rem;
    margin-bottom: 5px;
}

.evento-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 15px;
    padding-top: 15px;
    border-top: 1px solid var(--color-border);
}

.precio {
    font-size: 1.25rem;
    font-weight: bold;
    color: var(--color-primary);
}

/* Footer */
.site-footer {
    background: var(--color-text);
    color: white;
    padding: 40px 0;
    text-align: center;
}

.site-footer a {
    color: white;
    margin: 0 10px;
    text-decoration: none;
}

.site-footer address {
    margin-top: 20px;
    font-style: normal;
    color: var(--color-text-muted);
}

/* Responsive */
@media (max-width: 768px) {
    .site-header .container {
        flex-direction: column;
        height: auto;
        padding: 15px;
        gap: 15px;
    }
    
    .main-nav ul {
        gap: 15px;
        font-size: 0.9rem;
    }
    
    .hero h1 {
        font-size: 2rem;
    }
    
    .eventos-grid {
        grid-template-columns: 1fr;
    }
}
```

---

## 🛠️ Ejercicios Prácticos

### Ejercicio 1: Crear estructura HTML semántica
Crear la página de inicio de TuFiesta con:
- Header con navegación
- Section Hero
- Grid de eventos
- Footer

### Ejercicio 2: Estilizar con Flexbox
Usar Flexbox para:
- Alinear elementos del header
- Centrar contenido del hero
- Distribuir contenido de las tarjetas

### Ejercicio 3: Grid responsive
Implementar grid que:
- Muestre 3 columnas en desktop
- Muestre 2 columnas en tablet
- Muestre 1 columna en móvil

### Ejercicio 4: Variables CSS
Crear sistema de temas con variables CSS para:
- Colores primarios y secundarios
- Espaciado consistente
- Bordes y sombras

---

## 🚀 Proyecto de la Clase

**Entregables:**
1. Archivo `index.html` con estructura semántica completa
2. Archivo `styles.css` con diseño responsive
3. Al menos 4 tarjetas de eventos
4. Header y footer estilizados
5. Formulario de búsqueda

---

## 📚 Recursos Adicionales

- [MDN - HTML](https://developer.mozilla.org/es/docs/Web/HTML)
- [MDN - CSS](https://developer.mozilla.org/es/docs/Web/CSS)
- [CSS-Tricks - Flexbox](https://css-tricks.com/snippets/css/a-guide-to-flexbox/)
- [CSS-Tricks - Grid](https://css-tricks.com/snippets/css/complete-guide-grid/)
- [Web Accessibility Initiative](https://www.w3.org/WAI/)
