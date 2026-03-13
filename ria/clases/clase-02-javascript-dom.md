# 📱 Clase 02: JavaScript Moderno y Manipulación del DOM

**Duración:** 4 horas  
**Objetivo:** Dominar JavaScript ES6+, eventos y manipulación dinámica del DOM  
**Proyecto:** Funcionalidad interactiva para el sistema de eventos TuFiesta

---

## 📚 Contenido Teórico

### 1. Fundamentos de JavaScript

#### 1.1 ¿Qué es JavaScript?

**JavaScript** es el lenguaje de programación de la web. Permite agregar interactividad a las páginas HTML.

```
┌─────────────────────────────────────────────────────────────────────┐
│                    JAVASCRIPT EN LA WEB                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   NAVEGADOR                                                         │
│   ┌─────────────────────────────────────────────────────────────┐   │
│   │                                                             │   │
│   │   HTML         →   CSS         →   JavaScript             │   │
│   │   (Estructura)    (Estilo)         (Comportamiento)        │   │
│   │                                                             │   │
│   │   •body           •color            •click                │   │
│   │   •div            •font-size        •scroll               │   │
│   │   •p              •display          •form submit          │   │
│   │   •img            •margin           •animaciones          │   │
│   │                                                             │   │
│   │   ┌─────────────────────────────────────────────────────┐ │   │
│   │   │                    JAVASCRIPT                       │ │   │
│   │   │                                                      │ │   │
│   │   │   • DOM Manipulation    - Cambiar HTML/CSS         │ │   │
│   │   │   • Event Handling      - Responder a usuarios      │ │   │
│   │   │   • AJAX/Fetch          - Cargar datos sin recargar │ │   │
│   │   │   • Local Storage       - Guardar datos local       │ │   │
│   │   │   • Canvas/WebGL       - Gráficos                   │ │   │
│   │   │   • APIs Modernas      - Geolocation, etc          │ │   │
│   │   │                                                      │ │   │
│   │   └─────────────────────────────────────────────────────┘ │   │
│   └─────────────────────────────────────────────────────────────┘   │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

#### 1.2 Variables y Tipos de Datos

```javascript
// Tipos de datos primitivos
const nombre = 'Juan';           // String
const edad = 25;                 // Number
const precio = 99.99;           // Number
const activo = true;            // Boolean
const nada = null;              // Null
let indefinido;                 // Undefined
const id = Symbol('id');        // Symbol
const bigNum = 9007199254740991n; // BigInt

// Tipos de datos complejos
const evento = {                // Object
    titulo: 'Concierto',
    precio: 500,
    fecha: '2024-12-15'
};

const eventos = [               // Array
    'Concierto', 
    'Festival', 
    'Teatro'
];

// typeof para verificar tipos
console.log(typeof nombre);     // "string"
console.log(typeof edad);      // "number"
console.log(typeof evento);    // "object"
console.log(typeof eventos);   // "object"
```

---

### 2. ES6+ - Características Modernas

#### 2.1 Variables: const, let y var

```javascript
// const - No se puede reasignar (para valores que no cambian)
const API_URL = 'https://api.tufiesta.uy';
const evento = { titulo: 'Concierto' };
evento.precio = 500;  // ✓ Se puede modificar propiedades
// evento = {};      // ✗ Error: no se puede reasignar

// let - Se puede reasignar (scope de bloque)
let contador = 0;
contador = contador + 1;  // ✓

// var - Scope de función (EVITAR)
var antigua = 'no usar';   // ✗ Problemas con scope

// Ejemplo de scope
if (true) {
    const dentroDeIf = 'solo aquí';
    let letDentroIf = 'también solo aquí';
    var varEnTodo = 'visible en toda la función';
}
// console.log(dentroDeIf);  // Error
// console.log(letDentroIf); // Error
console.log(varEnTodo);     // ✓
```

#### 2.2 Template Literals

```javascript
// Interpolación de strings
const nombre = 'Juan';
const edad = 25;

// Antes
const mensaje = 'Hola, me llamo ' + nombre + ' y tengo ' + edad + ' años';

// Ahora (template literals)
const mensaje = `Hola, me llamo ${nombre} y tengo ${edad} años`;

// Expresiones complejas
const evento = { titulo: 'Concierto', precio: 500 };
const mensaje = `El evento "${evento.titulo}" cuesta $${evento.precio * 1.22} con IVA`;

// Multilínea
const html = `
    <div class="evento">
        <h3>${evento.titulo}</h3>
        <p>Precio: $${evento.precio}</p>
    </div>
`;
```

#### 2.3 Destructuring

```javascript
// Destructuring de objetos
const evento = {
    id: 1,
    titulo: 'Concierto de Rock',
    precio: 500,
    categoria: 'musica',
    fecha: '2024-12-15'
};

// Extracción de propiedades
const { id, titulo } = evento;
console.log(titulo);  // "Concierto de Rock"

// Renombrar
const { precio: precioFinal } = evento;
console.log(precioFinal);  // 500

// Valores por defecto
const { capacidad = 100 } = evento;
console.log(capacidad);  // 100

// Destructuring de arrays
const colores = ['rojo', 'verde', 'azul'];
const [primero, segundo] = colores;
console.log(primero);  // "rojo"

// Ignorar elementos
const [, , tercer] = colores;
console.log(tercer);  // "azul"

// Rest operator
const [head, ...tail] = [1, 2, 3, 4, 5];
console.log(head);  // 1
console.log(tail);  // [2, 3, 4, 5]
```

#### 2.4 Arrow Functions

```javascript
// Función tradicional
function sumar(a, b) {
    return a + b;
}

// Arrow function
const sumar = (a, b) => a + b;

// Con cuerpo
const saludar = (nombre) => {
    const mensaje = `Hola, ${nombre}!`;
    return mensaje;
};

// Parámetros
const sinParametros = () => 'Hola';
const unParametro = x => x * 2;
const dosParametros = (x, y) => x + y;

// Diferencia con 'this'
// Función tradicional tiene su propio 'this'
function Evento() {
    this.titulo = 'Concierto';
    setTimeout(function() {
        console.log(this.titulo);  // undefined
    }, 1000);
}

// Arrow function NO tiene su propio 'this'
function EventoArrow() {
    this.titulo = 'Concierto';
    setTimeout(() => {
        console.log(this.titulo);  // "Concierto"
    }, 1000);
}
```

#### 2.5 Métodos de Arrays

```javascript
const eventos = [
    { id: 1, titulo: 'Concierto Rock', precio: 500, categoria: 'musica', fecha: '2024-12-15' },
    { id: 2, titulo: 'Festival Jazz', precio: 800, categoria: 'musica', fecha: '2024-12-20' },
    { id: 3, titulo: 'Tech Conference', precio: 2500, categoria: 'tecnologia', fecha: '2025-01-10' },
    { id: 4, titulo: 'Stand Up Comedy', precio: 350, categoria: 'comedia', fecha: '2024-12-28' },
    { id: 5, titulo: 'Festival Arte', precio: 600, categoria: 'arte', fecha: '2025-01-05' }
];

// map - Transformar cada elemento
const titulos = eventos.map(e => e.titulo);
// ["Concierto Rock", "Festival Jazz", "Tech Conference", "Stand Up Comedy", "Festival Arte"]

const conIVA = eventos.map(e => ({
    ...e,
    precioConIVA: e.precio * 1.22
}));

// filter - Filtrar elementos
const eventosMusicales = eventos.filter(e => e.categoria === 'musica');
const eventosBaratos = eventos.filter(e => e.precio < 600);

// find - Encontrar primer elemento
const eventoEncontrado = eventos.find(e => e.id === 3);
// { id: 3, titulo: 'Tech Conference', ... }

// findIndex - Índice del elemento
const indice = eventos.findIndex(e => e.id === 3);
// 2

// some - ¿Alguno cumple condición?
const hayMusica = eventos.some(e => e.categoria === 'musica');
// true

// every - ¿Todos cumplen?
const todosBaratos = eventos.every(e => e.precio < 3000);
// true

// reduce - Acumular valores
const precioTotal = eventos.reduce((sum, e) => sum + e.precio, 0);
// 4750

// Filtrar + Map (chain)
const titulosBaratos = eventos
    .filter(e => e.precio < 600)
    .map(e => e.titulo);
// ["Concierto Rock", "Stand Up Comedy", "Festival Arte"]
```

#### 2.6 Spread y Rest Operators

```javascript
// Spread - Expandir
const arr1 = [1, 2, 3];
const arr2 = [...arr1, 4, 5];
// [1, 2, 3, 4, 5]

const obj1 = { a: 1, b: 2 };
const obj2 = { ...obj1, c: 3, d: 4 };
// { a: 1, b: 2, c: 3, d: 4 }

// Clonar objetos
const eventoOriginal = { titulo: 'Concierto', precio: 500 };
const eventoClonado = { ...eventoOriginal };

// Combinar objetos
const base = { titulo: 'Evento', fecha: '2024-12-15' };
const completo = { ...base, precio: 500, ubicacion: 'Montevideo' };

// Rest - Recolectar
function sumar(...numeros) {
    return numeros.reduce((a, b) => a + b, 0);
}
sumar(1, 2, 3, 4);  // 10

const [primero, segundo, ...resto] = [1, 2, 3, 4, 5];
// primero=1, segundo=2, resto=[3, 4, 5]
```

#### 2.7 Optional Chaining y Nullish

```javascript
const evento = {
    titulo: 'Concierto',
    precio: 500,
    ubicacion: null
};

// Optional chaining (?.)
const ciudad = evento.ubicacion?.ciudad;  // undefined (no error)
const provincia = evento.ubicacion?.direccion?.provincia;  // undefined

// Nullish coalescing (??)
const precio = evento.precio ?? 0;  // 500
const capacidad = evento.capacidad ?? 100;  // 100 (porque capacidad no existe)
const ubicacion = evento.ubicacion ?? 'No especificada';  // "No especificada"

// Equivalent a || pero con diferencia:
// "" o 0 son "falsy" con || pero "valid" con ??
const valor1 = '' ?? 'default';   // ""
const valor2 = '' || 'default';   // "default"

const valor3 = 0 ?? 'default';    // 0
const valor4 = 0 || 'default';    // "default"
```

---

### 3. Programación Orientada a Objetos

#### 3.1 Clases

```javascript
// Definir una clase
class Evento {
    // Constructor
    constructor(titulo, precio, fecha) {
        this.titulo = titulo;
        this.precio = precio;
        this.fecha = fecha;
        this.id = Date.now();
        this.compradores = [];
    }
    
    // Método
    obtenerDetalles() {
        return `${this.titulo} - $${this.precio} - ${this.fecha}`;
    }
    
    // Método con cálculo
    obtenerPrecioConIVA() {
        return this.precio * 1.22;
    }
    
    // Getter
    get estaLleno() {
        return this.compradores.length >= this.capacidad;
    }
    
    // Setter
    set capacidad(valor) {
        if (valor > 0) {
            this._capacidad = valor;
        }
    }
    
    // Método estático (no necesita instancia)
    static crearDemo() {
        return new Evento('Evento Demo', 0, new Date().toISOString());
    }
}

// Herencia
class EventoMusical extends Evento {
    constructor(titulo, precio, fecha, artista) {
        super(titulo, precio, fecha);  // Llamar al padre
        this.artista = artista;
        this.tipo = 'musical';
    }
    
    // Override de método
    obtenerDetalles() {
        return `${super.obtenerDetalles()} - Artista: ${this.artista}`;
    }
}

// Usar las clases
const evento1 = new Evento('Concierto', 500, '2024-12-15');
console.log(evento1.obtenerDetalles());

const rock = new EventoMusical('Rock Fest', 800, '2024-12-20', 'Metallica');
console.log(rock.obtenerDetalles());
```

---

### 4. El DOM - Manipulación con JavaScript

#### 4.1 Seleccionar Elementos

```javascript
// Seleccionar un elemento
const header = document.getElementById('header');
const primerEvento = document.querySelector('.evento-card');
const boton = document.querySelector('button.primary');

// Seleccionar múltiples elementos
const todosEventos = document.querySelectorAll('.evento-card');
const botones = document.querySelectorAll('button');

// Iterar sobre elementos
todosEventos.forEach((evento, indice) => {
    console.log(`Evento ${indice + 1}:`, evento.textContent);
});

// Seleccionar父/hijo
const contenido = header.querySelector('.contenido');
const padre = header.parentElement;
const hijos = header.children;
```

#### 4.2 Modificar Contenido

```javascript
const evento = document.querySelector('.evento-card');

// Texto (solo texto, sin HTML)
evento.textContent = 'Nuevo título';

// HTML (interpreta etiquetas)
evento.innerHTML = '<h3>Nuevo título</h3><p>Descripción</p>';

// Atributos
evento.setAttribute('data-id', '123');
evento.getAttribute('data-id');
evento.removeAttribute('data-id');

// Clases
evento.classList.add('destacado');
evento.classList.remove('oculto');
evento.classList.toggle('activo');
evento.classList.contains('destacado');  // true/false

// Estilos
evento.style.color = 'blue';
evento.style.backgroundColor = '#f0f0f0';
evento.style.display = 'none';
```

#### 4.3 Crear y Eliminar Elementos

```javascript
// Crear elemento
const nuevoEvento = document.createElement('article');
nuevoEvento.className = 'evento-card';
nuevoEvento.innerHTML = `
    <h3>Nuevo Evento</h3>
    <p class="precio">$500</p>
`;

// Agregar al DOM
const grid = document.querySelector('.eventos-grid');
grid.appendChild(nuevoEvento);

// Insertar en posición específica
grid.insertBefore(nuevoEvento, grid.firstChild);

// Clonar
const eventoClonado = evento.cloneNode(true);  // true = deep clone

// Eliminar
nuevoEvento.remove();
// o
grid.removeChild(nuevoEvento);
```

#### 4.4 Eventos

```javascript
// Event Listener
const boton = document.querySelector('.btn-comprar');

// Agregar listener
boton.addEventListener('click', function(event) {
    console.log('Clicked!', event.target);
    console.log('Datos del evento:', event.currentTarget.dataset);
});

// Arrow function
boton.addEventListener('click', (e) => {
    e.preventDefault();  // Prevenir comportamiento por defecto
    console.log('Comprando...');
});

// Eventos comunes
element.addEventListener('click');        // Click
element.addEventListener('mouseenter');   // Mouse entra
element.addEventListener('mouseleave');  // Mouse sale
element.addEventListener('input');       // Input cambia
element.addEventListener('submit');      // Form submit
element.addEventListener('keydown');     // Tecla presionada

// Event delegation (delegación de eventos)
// En lugar de agregar listener a cada hijo, agregar al padre
const grid = document.querySelector('.eventos-grid');

grid.addEventListener('click', (e) => {
    const card = e.target.closest('.evento-card');
    if (card) {
        console.log('Click en:', card.dataset.id);
    }
});

// Remover listener
function handleClick() {
    console.log('Click');
}
boton.addEventListener('click', handleClick);
boton.removeEventListener('click', handleClick);
```

---

### 5. Proyecto: Funcionalidad de Eventos

```javascript
// app.js - JavaScript para TuFiesta

// Datos de ejemplo
const eventos = [
    { id: 1, titulo: 'Concierto de Rock', precio: 500, categoria: 'musica', imagen: 'rock.jpg', fecha: '15 Dic', ubicacion: 'Estadio Centenario' },
    { id: 2, titulo: 'Festival de Jazz', precio: 800, categoria: 'musica', imagen: 'jazz.jpg', fecha: '20 Dic', ubicacion: 'Teatro Solís' },
    { id: 3, titulo: 'Tech Conference', precio: 2500, categoria: 'tecnologia', imagen: 'tech.jpg', fecha: '10 Ene', ubicacion: 'Punta del Este' },
    { id: 4, titulo: 'Stand Up Comedy', precio: 350, categoria: 'comedia', imagen: 'comedy.jpg', fecha: '28 Dic', ubicacion: 'La Casa de la Comedy' }
];

// Estado de la aplicación
let filtros = {
    buscar: '',
    categoria: 'todas'
};

// Inicializar
document.addEventListener('DOMContentLoaded', () => {
    renderizarEventos(eventos);
    configurarFiltros();
    configurarBusqueda();
});

// Renderizar eventos
function renderizarEventos(listaEventos) {
    const grid = document.getElementById('eventos-grid');
    
    if (listaEventos.length === 0) {
        grid.innerHTML = '<p class="no-eventos">No se encontraron eventos</p>';
        return;
    }
    
    grid.innerHTML = listaEventos.map(evento => crearHTMLEvento(evento)).join('');
    
    // Agregar event listeners a los botones
    grid.querySelectorAll('.btn-comprar').forEach(boton => {
        boton.addEventListener('click', manejarCompra);
    });
}

// Crear HTML de una tarjeta
function crearHTMLEvento(evento) {
    return `
        <article class="evento-card" data-id="${evento.id}">
            <div class="evento-imagen">
                <img src="/images/${evento.imagen}" alt="${evento.titulo}">
                <span class="categoria-badge">${evento.categoria}</span>
            </div>
            <div class="evento-contenido">
                <h3>${evento.titulo}</h3>
                <p class="evento-fecha">📅 ${evento.fecha}</p>
                <p class="evento-ubicacion">📍 ${evento.ubicacion}</p>
                <div class="evento-footer">
                    <span class="precio">$${evento.precio}</span>
                    <button class="btn btn-primary btn-comprar" data-id="${evento.id}">
                        Comprar
                    </button>
                </div>
            </div>
        </article>
    `;
}

// Manejar compra
function manejarCompra(e) {
    const boton = e.target;
    const eventoId = boton.dataset.id;
    const evento = eventos.find(ev => ev.id === parseInt(eventoId));
    
    if (evento) {
        alert(`¡Excelente! Has seleccionado: ${evento.titulo}\nPrecio: $${evento.precio}`);
    }
}

// Configurar filtros de categoría
function configurarFiltros() {
    const select = document.getElementById('filtro-categoria');
    
    select.addEventListener('change', (e) => {
        filtros.categoria = e.target.value;
        filtrarEventos();
    });
}

// Configurar búsqueda
function configurarBusqueda() {
    const input = document.getElementById('buscar');
    
    input.addEventListener('input', (e) => {
        filtros.buscar = e.target.value.toLowerCase();
        filtrarEventos();
    });
}

// Filtrar eventos
function filtrarEventos() {
    const eventosFiltrados = eventos.filter(evento => {
        const coincideBuscar = evento.titulo.toLowerCase().includes(filtros.buscar);
        const coincideCategoria = filtros.categoria === 'todas' || 
            evento.categoria === filtros.categoria;
        return coincideBuscar && coincideCategoria;
    });
    
    renderizarEventos(eventosFiltrados);
}

// Ejemplo: agregar evento dinámicamente
function agregarEvento(nuevoEvento) {
    eventos.push(nuevoEvento);
    renderizarEventos(eventos);
}

// Ejemplo: filtrar por precio
function filtrarPorPrecio(precioMax) {
    const eventosFiltrados = eventos.filter(e => e.precio <= precioMax);
    renderizarEventos(eventosFiltrados);
}
```

---

## 🛠️ Ejercicios Prácticos

### Ejercicio 1: Manipulación del DOM
- Crear función que agregue nuevos eventos al grid
- Implementar eliminación de eventos
- Actualizar precio dinámicamente

### Ejercicio 2: Eventos
- Agregar evento click a cada tarjeta
- Implementar tooltip al hover
- Crear modal de confirmación

### Ejercicio 3: Filtros
- Filtrar por categoría
- Filtrar por rango de precio
- Ordenar por fecha/precio

### Ejercicio 4: Carrito de compras
- Agregar eventos al carrito
- Calcular total
- Persistir en localStorage

---

## 📚 Recursos

- [MDN JavaScript](https://developer.mozilla.org/es/docs/Web/JavaScript)
- [ES6 Features](https://es6-features.org/)
- [DOM Manipulation](https://developer.mozilla.org/es/docs/Web/API/Document_Object_Model)
