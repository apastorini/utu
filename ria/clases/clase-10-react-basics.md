# 📱 Clase 10: React Basics - Componentes y JSX

**Duración:** 4 horas  
**Objetivo:** Dominar los fundamentos de React, componentes y JSX  
**Proyecto:** Frontend del sistema de eventos con React

---

## 📚 Contenido Teórico

### 1. Fundamentos de React

#### 1.1 ¿Qué es React?

**React** es una biblioteca JavaScript de código abierto desarrollada por Facebook (Meta) para construir interfaces de usuario interactivas. Fue lanzada en 2013 y se ha convertido en la biblioteca más popular para el desarrollo frontend.

**Características fundamentales:**

| Característica | Descripción |
|----------------|-------------|
| **Componentes** | Bloques de construcción reutilizables |
| **Virtual DOM** | Representación en memoria del DOM real |
| **JSX** | Sintaxis que combina JavaScript con HTML |
| **Unidirectional Data Flow** | Datos fluyen en una sola dirección |
| **Inmutabilidad** | Los datos no se mutan, se crean nuevos |
| **Declarativo** | Describes el resultado, no el proceso |

#### 1.2 ¿Por qué React?

**Arquitectura tradicional (DOM Real):**
```
Usuario hace click → Evento → Manipulación directa del DOM → Re-render completo
                                 ↓
                           Alto costo computacional
```

**Arquitectura React (Virtual DOM):**
```
Usuario hace click → Evento → Actualizar Virtual DOM → Calcular diferencia →
                            → Aplicar solo cambios necesarios → Re-render optimizado
```

#### 1.3 Conceptos Clave

**Componente:** Una función o clase que recibe props y retorna elementos React.

```jsx
// Componente funcional (moderno)
function Saludo({ nombre }) {
    return <h1>Hola, {nombre}!</h1>;
}

// Componente de clase (legacy)
class Saludo extends React.Component {
    render() {
        return <h1>Hola, {this.props.nombre}!</h1>;
    }
}
```

**Props:** Datos que se pasan de padre a hijo (readonly).

**Estado (State):** Datos internos del componente que pueden cambiar.

**Elemento:** Objeto ligero que representa un nodo en el Virtual DOM.

**JSX:** Extensión de sintaxis que permite escribir HTML en JavaScript.

---

### 2. JSX en Profundidad

#### 2.1 ¿Qué es JSX?

JSX (JavaScript XML) es una extensión de sintaxis que permite escribir marcado (HTML-like) dentro de JavaScript. NO es HTML, es una forma de escribir elementos React.

```jsx
// JSX
const elemento = <h1 className="titulo">Hola Mundo</h1>;

// Equivalente en JavaScript puro
const elemento = React.createElement(
    'h1',
    { className: 'titulo' },
    'Hola Mundo'
);
```

#### 2.2 Reglas de JSX

**Regla 1: Toda etiqueta debe cerrarse**
```jsx
// Incorrecto
<input type="text">
<br>

// Correcto
<input type="text" />
<br />
```

**Regla 2: Usar className en lugar de class**
```jsx
// Incorrecto
<div class="contenedor">Contenido</div>

// Correcto
<div className="contenedor">Contenido</div>
```

**Regla 3: camelCase para atributos**
```jsx
// Incorrecto
<button onclick={handleClick} tabindex="0">Click</button>

// Correcto
<button onClick={handleClick} tabIndex="0">Click</button>
```

**Regla 4: Solo un elemento raíz**
```jsx
// Incorrecto
return (
    <h1>Título</h1>
    <p>Párrafo</p>
);

// Correcto - usar Fragment
return (
    <>
        <h1>Título</h1>
        <p>Párrafo</p>
    </>
);

// O usar un contenedor
return (
    <div>
        <h1>Título</h1>
        <p>Párrafo</p>
    </div>
);
```

#### 2.3 Expresiones en JSX

```jsx
const nombre = 'Juan';
const edad = 25;

function getSaludo() {
    return '¡Hola!';
}

const elemento = (
    <div>
        {/* Comentarios en JSX */}
        <h1>{nombre}</h1>
        <p>Tengo {edad} años</p>
        <p>{getSaludo()}</p>
        <p>{5 + 3}</p>
        <p>{edad >= 18 ? 'Adulto' : 'Menor'}</p>
    </div>
);
```

#### 2.4 Eventos en JSX

```jsx
function Boton() {
    const handleClick = (e) => {
        console.log('Click:', e.target);
        console.log('Tipo:', e.type);
    };
    
    return (
        <button 
            onClick={handleClick}
            onMouseEnter={() => console.log('Mouse enter')}
            onMouseLeave={() => console.log('Mouse leave')}
        >
            Click me
        </button>
    );
}
```

---

### 3. Componentes en Profundidad

#### 3.1 Componentes Funcionales vs Clases

**Componente Funcional (Recomendado):**
```jsx
function EventoCard({ titulo, fecha, precio, imagen, onClick }) {
    const formatFecha = (fecha) => {
        return new Date(fecha).toLocaleDateString('es-ES', {
            day: 'numeric',
            month: 'long',
            year: 'numeric'
        });
    };
    
    return (
        <article className="evento-card" onClick={onClick}>
            <img src={imagen} alt={titulo} className="evento-imagen" />
            <div className="evento-info">
                <h3>{titulo}</h3>
                <time dateTime={fecha}>{formatFecha(fecha)}</time>
                <span className="precio">${precio}</span>
            </div>
        </article>
    );
}
```

**Componente de Clase (Legacy):**
```jsx
class EventoCard extends React.Component {
    formatFecha(fecha) {
        return new Date(fecha).toLocaleDateString('es-ES', {
            day: 'numeric',
            month: 'long',
            year: 'numeric'
        });
    }
    
    render() {
        const { titulo, fecha, precio, imagen, onClick } = this.props;
        
        return (
            <article className="evento-card" onClick={onClick}>
                <img src={imagen} alt={titulo} className="evento-imagen" />
                <div className="evento-info">
                    <h3>{titulo}</h3>
                    <time dateTime={fecha}>{this.formatFecha(fecha)}</time>
                    <span className="precio">${precio}</span>
                </div>
            </article>
        );
    }
}
```

#### 3.2 Props - Propiedades

Las **props** son la forma de pasar datos de un componente padre a un componente hijo.

```jsx
// Definir tipos con PropTypes (runtime validation)
import PropTypes from 'prop-types';

function UsuarioCard({ nombre, email, rol = 'usuario', estado }) {
    return (
        <div className={`usuario-card estado-${estado}`}>
            <h3>{nombre}</h3>
            <p>{email}</p>
            <span className="badge">{rol}</span>
        </div>
    );
}

UsuarioCard.propTypes = {
    nombre: PropTypes.string.isRequired,
    email: PropTypes.string.isRequired,
    rol: PropTypes.oneOf(['usuario', 'organizador', 'admin']),
    estado: PropTypes.oneOf(['activo', 'inactivo', 'pendiente'])
};

UsuarioCard.defaultProps = {
    rol: 'usuario',
    estado: 'pendiente'
};
```

**Con TypeScript:**
```typescript
interface UsuarioCardProps {
    nombre: string;
    email: string;
    rol?: 'usuario' | 'organizador' | 'admin';
    estado?: 'activo' | 'inactivo' | 'pendiente';
}

function UsuarioCard({ nombre, email, rol = 'usuario', estado = 'pendiente' }: UsuarioCardProps) {
    return (
        <div className={`usuario-card estado-${estado}`}>
            <h3>{nombre}</h3>
            <p>{email}</p>
            <span className="badge">{rol}</span>
        </div>
    );
}
```

#### 3.3 Children - Hijos

```jsx
function Modal({ children, titulo, abierto, onClose }) {
    if (!abierto) return null;
    
    return (
        <div className="modal-overlay" onClick={onClose}>
            <div className="modal-content" onClick={e => e.stopPropagation()}>
                <div className="modal-header">
                    <h2>{titulo}</h2>
                    <button onClick={onClose} aria-label="Cerrar">✕</button>
                </div>
                <div className="modal-body">
                    {children}
                </div>
                <div className="modal-footer">
                    <slot name="footer" />
                </div>
            </div>
        </div>
    );
}

// Uso
<Modal titulo="Confirmar" abierto={true} onClose={cerrar}>
    <p>¿Estás seguro?</p>
    <div slot="footer">
        <button>Confirmar</button>
        <button>Cancelar</button>
    </div>
</Modal>
```

---

### 4. Estilos en React

#### 4.1 CSS Modules

```css
/* Button.module.css */
.button {
    padding: 10px 20px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 16px;
    transition: background-color 0.2s;
}

.primary {
    background-color: #007bff;
    color: white;
}

.primary:hover {
    background-color: #0056b3;
}

.secondary {
    background-color: #6c757d;
    color: white;
}

.disabled {
    opacity: 0.5;
    cursor: not-allowed;
}
```

```jsx
/* Button.jsx */
import styles from './Button.module.css';

function Button({ children, variant = 'primary', disabled, onClick }) {
    const className = [
        styles.button,
        styles[variant],
        disabled && styles.disabled
    ].filter(Boolean).join(' ');
    
    return (
        <button 
            className={className}
            disabled={disabled}
            onClick={onClick}
        >
            {children}
        </button>
    );
}
```

#### 4.2 Styled Components

```bash
npm install styled-components
```

```jsx
import styled from 'styled-components';

const Card = styled.div`
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    padding: 16px;
    transition: transform 0.2s;
    
    &:hover {
        transform: translateY(-4px);
    }
`;

const Titulo = styled.h2`
    color: #333;
    font-size: 1.5rem;
    margin-bottom: 8px;
`;

const Precio = styled.span`
    color: ${props => props.$destacado ? '#e74c3c' : '#333'};
    font-weight: bold;
    font-size: 1.25rem;
`;

function EventoCard({ evento }) {
    return (
        <Card>
            <Titulo>{evento.titulo}</Titulo>
            <Precio $destacado={evento.precio > 100}>
                ${evento.precio}
            </Precio>
        </Card>
    );
}
```

---

## 💻 Contenido Práctico

### 5. Estructura del Proyecto

```
mi-app/
├── public/
│   ├── index.html
│   ├── manifest.json
│   └── favicon.ico
├── src/
│   ├── components/          # Componentes reutilizables
│   │   ├── common/
│   │   │   ├── Button.jsx
│   │   │   ├── Modal.jsx
│   │   │   └── Input.jsx
│   │   ├── eventos/
│   │   │   ├── EventoCard.jsx
│   │   │   ├── EventoList.jsx
│   │   │   └── EventoForm.jsx
│   │   └── layout/
│   │       ├── Header.jsx
│   │       ├── Footer.jsx
│   │       └── Layout.jsx
│   ├── pages/               # Páginas/componentes de ruta
│   │   ├── Home.jsx
│   │   ├── Eventos.jsx
│   │   ├── DetalleEvento.jsx
│   │   └── 404.jsx
│   ├── hooks/               # Hooks personalizados
│   ├── context/             # Contextos
│   ├── services/            # APIs
│   ├── styles/              # Estilos globales
│   ├── utils/               # Utilidades
│   ├── App.jsx
│   ├── main.jsx
│   └── index.css
├── package.json
├── vite.config.js
└── README.md
```

### 6. Implementación del Proyecto

```jsx
// src/App.jsx - Componente principal
import { useState } from 'react';
import Header from './components/layout/Header';
import Footer from './components/layout/Footer';
import EventoList from './pages/EventoList';
import EventoDetail from './pages/EventoDetail';
import EventoForm from './pages/EventoForm';
import NotFound from './pages/NotFound';
import './App.css';

function App() {
    const [paginaActual, setPaginaActual] = useState('inicio');
    const [eventoSeleccionado, setEventoSeleccionado] = useState(null);
    
    const renderPagina = () => {
        switch (paginaActual) {
            case 'inicio':
                return <EventoList />;
            case 'detalle':
                return <EventoDetail evento={eventoSeleccionado} />;
            case 'crear':
                return <EventoForm onGuardar={() => setPaginaActual('inicio')} />;
            default:
                return <NotFound />;
        }
    };
    
    return (
        <div className="app">
            <Header 
                onNavigate={setPaginaActual} 
                paginaActual={paginaActual}
            />
            <main className="app-main">
                {renderPagina()}
            </main>
            <Footer />
        </div>
    );
}

export default App;
```

```jsx
// src/components/eventos/EventoCard.jsx
import './EventoCard.css';

function EventoCard({ evento, onClick }) {
    const formatFecha = (fecha) => {
        const date = new Date(fecha);
        return date.toLocaleDateString('es-ES', { 
            day: 'numeric', 
            month: 'long',
            year: 'numeric'
        });
    };
    
    return (
        <article 
            className="evento-card" 
            onClick={() => onClick?.(evento)}
            role="article"
        >
            <div className="evento-card-imagen">
                <img 
                    src={evento.imagen || '/placeholder.jpg'} 
                    alt={evento.titulo} 
                />
                <span className="evento-card-categoria">
                    {evento.categoria}
                </span>
            </div>
            <div className="evento-card-contenido">
                <h3 className="evento-card-titulo">{evento.titulo}</h3>
                <p className="evento-card-fecha">
                    📅 {formatFecha(evento.fecha)}
                </p>
                <p className="evento-card-ubicacion">
                    📍 {evento.ubicacion}
                </p>
                <div className="evento-card-footer">
                    <span className="evento-card-precio">
                        ${evento.precio}
                    </span>
                    <button className="evento-card-boton">
                        Ver Detalles
                    </button>
                </div>
            </div>
        </article>
    );
}

export default EventoCard;
```

```jsx
// src/pages/EventoList.jsx
import { useState, useEffect } from 'react';
import EventoCard from '../components/eventos/EventoCard';
import './EventoList.css';

const EVENTOS_MOCK = [
    { 
        id: 1, 
        titulo: 'Concierto de Rock', 
        fecha: '2024-03-15', 
        precio: 50, 
        imagen: '/rock.jpg', 
        categoria: 'musica',
        ubicacion: 'Estadio Centenario'
    },
    { 
        id: 2, 
        titulo: 'Festival de Jazz', 
        fecha: '2024-03-20', 
        precio: 35, 
        imagen: '/jazz.jpg', 
        categoria: 'musica',
        ubicacion: 'Teatro Solís'
    },
    { 
        id: 3, 
        titulo: 'Tech Conference', 
        fecha: '2024-04-01', 
        precio: 100, 
        imagen: '/tech.jpg', 
        categoria: 'tecnologia',
        ubicacion: 'Punta del Este'
    },
    { 
        id: 4, 
        titulo: 'Stand Up Comedy', 
        fecha: '2024-03-25', 
        precio: 25, 
        imagen: '/comedy.jpg', 
        categoria: 'entretenimiento',
        ubicacion: 'La Casa de la Comedy'
    },
];

function EventoList() {
    const [eventos, setEventos] = useState([]);
    const [filtro, setFiltro] = useState('');
    const [categoria, setCategoria] = useState('todas');
    const [cargando, setCargando] = useState(true);
    
    useEffect(() => {
        // Simulación de carga de datos
        const timer = setTimeout(() => {
            setEventos(EVENTOS_MOCK);
            setCargando(false);
        }, 500);
        
        return () => clearTimeout(timer);
    }, []);
    
    const eventosFiltrados = eventos.filter(evento => {
        const coincideFiltro = evento.titulo
            .toLowerCase()
            .includes(filtro.toLowerCase());
        const coincideCategoria = categoria === 'todas' || 
            evento.categoria === categoria;
        return coincideFiltro && coincideCategoria;
    });
    
    if (cargando) {
        return <div className="loading">Cargando eventos...</div>;
    }
    
    return (
        <div className="evento-list">
            <div className="evento-list-header">
                <h1>Explora Eventos</h1>
            </div>
            
            <div className="evento-list-filtros">
                <input
                    type="text"
                    placeholder="Buscar eventos..."
                    value={filtro}
                    onChange={e => setFiltro(e.target.value)}
                    className="busqueda-input"
                    aria-label="Buscar eventos"
                />
                <select 
                    value={categoria} 
                    onChange={e => setCategoria(e.target.value)}
                    className="categoria-select"
                    aria-label="Filtrar por categoría"
                >
                    <option value="todas">Todas las categorías</option>
                    <option value="musica">Música</option>
                    <option value="tecnologia">Tecnología</option>
                    <option value="entretenimiento">Entretenimiento</option>
                </select>
            </div>
            
            <div className="evento-list-grid">
                {eventosFiltrados.map(evento => (
                    <EventoCard 
                        key={evento.id} 
                        evento={evento}
                    />
                ))}
            </div>
            
            {eventosFiltrados.length === 0 && (
                <p className="no-eventos">
                    No se encontraron eventos
                </p>
            )}
        </div>
    );
}

export default EventoList;
```

---

## 🛠️ Ejercicios Prácticos

### Ejercicio 1: Componentes Básicos
- Crear Header con navegación
- Crear Footer con información
- Crear EventoCard con todos los detalles
- Crear Layout que envuelva el contenido

### Ejercicio 2: Componente Modal
- Crear Modal reutilizable
- Implementar estado abierto/cerrado
- Agregar overlay y cierre con ESC

### Ejercicio 3: Lista de Eventos
- Crear array de eventos de ejemplo
- Renderizar con .map()
- Implementar filtros por categoría

### Ejercicio 4: Formulario
- Crear formulario de evento
- Manejar cambios de inputs
- Validar datos básicos

---

## 🚀 Proyecto de la Clase

### Sistema de Eventos Completo en React

```jsx
// App.jsx - Estructura completa
import { useState, useEffect } from 'react';
import Header from './components/Header';
import Footer from './Footer';
import EventoList from './pages/EventoList';
import EventoDetail from './pages/EventoDetail';
import EventoForm from './pages/EventoForm';
import Login from './pages/Login';
import './App.css';

function App() {
    const [paginaActual, setPaginaActual] = useState('inicio');
    const [eventoSeleccionado, setEventoSeleccionado] = useState(null);
    const [usuario, setUsuario] = useState(null);
    
    const navigateTo = (pagina, evento = null) => {
        setPaginaActual(pagina);
        setEventoSeleccionado(evento);
    };
    
    const renderPagina = () => {
        switch (paginaActual) {
            case 'inicio':
                return <EventoList onSelect={navigateTo} />;
            case 'detalle':
                return <EventoDetail evento={eventoSeleccionado} />;
            case 'crear':
                return <EventoForm onSave={() => navigateTo('inicio')} />;
            case 'login':
                return <Login onLogin={setUsuario} />;
            default:
                return <div>404 - Página no encontrada</div>;
        }
    };
    
    return (
        <div className="app">
            <Header 
                onNavigate={navigateTo}
                usuario={usuario}
            />
            <main className="main-content">
                {renderPagina()}
            </main>
            <Footer />
        </div>
    );
}

export default App;
```

### Entregables

1. **App.jsx** con navegación funcional
2. **EventoList** con filtros y renderizado de lista
3. **EventoCard** con estilos y datos
4. **Modal** reutilizable
5. **Formulario** de creación de eventos
6. Estilos CSS aplicados

---

## 📚 Recursos Adicionales

- [Documentación oficial de React](https://react.dev/)
- [JSX Reference](https://react.dev/reference/react)
- [Components and Props](https://react.dev/learn/components-and-props)
- [Thinking in React](https://react.dev/learn/thinking-in-react)
