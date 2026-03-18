# ⚛️ Clase 17: React Hooks Avanzados

**Duración:** 4 horas  
**Objetivo:** Dominar hooks avanzados, custom hooks y patrones de rendimiento  
**Proyecto:** Sistema de eventos con hooks personalizados

---

## 📚 Contenido Teórico

### 1. Hooks Fundamentales Revisados

#### 1.1 useState con Funciones

```jsx
import { useState } from 'react';

function Contador() {
    const [count, setCount] = useState(0);
    
    // Forma correcta: función cuando el nuevo estado depende del anterior
    const incrementar = () => {
        setCount(prevCount => prevCount + 1);
    };
    
    // Equivalente a: setCount(count + 1)
    // Pero seguro con múltiples actualizaciones
    
    return (
        <div>
            <p>Count: {count}</p>
            <button onClick={incrementar}>+</button>
            <button onClick={() => setCount(c => c - 1)}>-</button>
        </div>
    );
}
```

#### 1.2 useEffect y Ciclo de Vida

```jsx
import { useState, useEffect } from 'react';

function EventoDetalle({ eventoId }) {
    const [evento, setEvento] = useState(null);
    const [cargando, setCargando] = useState(true);
    const [error, setError] = useState(null);
    
    // useEffect se ejecuta después de cada render
    useEffect(() => {
        console.log('Componente montado o actualizado');
        
        // Cleanup function - se ejecuta antes del próximo effect
        // y cuando el componente se desmonta
        return () => {
            console.log('Cleanup antes del próximo effect o unmount');
        };
    }); // Sin dependencias = se ejecuta en cada render
    
    // useEffect con array vacío = solo una vez (montaje)
    useEffect(() => {
        console.log('Solo una vez - montaje');
        
        return () => {
            console.log('Solo una vez - desmontaje');
        };
    }, []); // []
    
    // useEffect con dependencias = se ejecuta cuando cambian
    useEffect(() => {
        if (eventoId) {
            fetchEvento(eventoId);
        }
    }, [eventoId]); // [eventoId]
    
    // Fetch con cleanup para evitar memory leaks
    useEffect(() => {
        const controller = new AbortController();
        
        async function fetchData() {
            try {
                setCargando(true);
                const response = await fetch(`/api/eventos/${eventoId}`, {
                    signal: controller.signal
                });
                const data = await response.json();
                setEvento(data);
            } catch (err) {
                if (err.name !== 'AbortError') {
                    setError(err.message);
                }
            } finally {
                setCargando(false);
            }
        }
        
        fetchData();
        
        return () => controller.abort(); // Cleanup
    }, [eventoId]);
    
    if (cargando) return <Spinner />;
    if (error) return <Error mensaje={error} />;
    if (!evento) return null;
    
    return <div>{evento.titulo}</div>;
}
```

---

### 2. Hooks de Rendimiento

#### 2.1 useMemo - Memoización de Valores

```jsx
import { useMemo } from 'react';

function EventoList({ eventos, filtro, sortBy }) {
    // Solo se recalcula cuando cambian eventos, filtro o sortBy
    const eventosProcesados = useMemo(() => {
        console.log('Calculando eventos filtrados...');
        
        let resultado = [...eventos];
        
        // Filtrar
        if (filtro) {
            resultado = resultado.filter(e => 
                e.titulo.toLowerCase().includes(filtro.toLowerCase())
            );
        }
        
        // Ordenar
        resultado.sort((a, b) => {
            if (sortBy === 'fecha') {
                return new Date(a.fecha) - new Date(b.fecha);
            }
            return a.precio - b.precio;
        });
        
        return resultado;
    }, [eventos, filtro, sortBy]);
    
    return (
        <ul>
            {eventosProcesados.map(e => (
                <li key={e.id}>{e.titulo}</li>
            ))}
        </ul>
    );
}
```

#### 2.2 useCallback - Memoización de Funciones

```jsx
import { useState, useCallback } from 'react';

function ParentComponent() {
    const [count, setCount] = useState(0);
    
    // Sin useCallback - nueva referencia en cada render
    const handleClick1 = () => {
        console.log('Click');
    };
    
    // Con useCallback - misma referencia salvo que cambie dependencia
    const handleClick2 = useCallback(() => {
        console.log('Click');
    }, []); // []
    
    // Con dependencias
    const handleClickWithCount = useCallback((id) => {
        console.log('Click en:', id, 'Count:', count);
    }, [count]); // Se recrea cuando cambia count
    
    return (
        <div>
            <ChildComponent onClick={handleClick2} />
            <ChildComponent onClick={handleClickWithCount} />
        </div>
    );
}
```

**Cuándo usar useCallback:**
- Pasando callbacks a componentes memoizados
- Dependencias de otros hooks
- Funciones en contexto de valor

---

### 3. useRef - Referencias Mutable

#### 3.1 Acceso a Elementos del DOM

```jsx
import { useRef, useEffect } from 'react';

function EnfocarInput() {
    const inputRef = useRef(null);
    
    useEffect(() => {
        // Enfocar input al montar
        inputRef.current?.focus();
    }, []);
    
    const handleClick = () => {
        inputRef.current?.focus();
    };
    
    return (
        <div>
            <input ref={inputRef} type="text" />
            <button onClick={handleClick}>Enfocar</button>
        </div>
    );
}
```

#### 3.2 Persistencia de Valores sin Re-render

```jsx
import { useState, useRef, useEffect } from 'react';

function ContadorConHistorial() {
    const [count, setCount] = useState(0);
    const historialRef = useRef([]); // No causa re-render
    
    useEffect(() => {
        historialRef.current.push(count);
        console.log('Historial:', historialRef.current);
    }, [count]);
    
    const incrementar = () => setCount(c => c + 1);
    
    return (
        <div>
            <p>Count: {count}</p>
            <p>Historial的长度: {historialRef.current.length}</p>
            <button onClick={incrementar}>+</button>
        </div>
    );
}
```

---

### 4. Custom Hooks

#### 4.1 useLocalStorage

```jsx
// hooks/useLocalStorage.js
import { useState, useEffect } from 'react';

function useLocalStorage(key, valorInicial) {
    // Leer valor inicial del localStorage
    const [valor, setValor] = useState(() => {
        try {
            const item = localStorage.getItem(key);
            return item ? JSON.parse(item) : valorInicial;
        } catch (error) {
            console.error(`Error reading localStorage key "${key}":`, error);
            return valorInicial;
        }
    });
    
    // Actualizar localStorage cuando cambia el valor
    useEffect(() => {
        try {
            localStorage.setItem(key, JSON.stringify(valor));
        } catch (error) {
            console.error(`Error setting localStorage key "${key}":`, error);
        }
    }, [key, valor]);
    
    return [valor, setValor];
}

export default useLocalStorage;
```

**Uso:**
```jsx
function ConfiguracionUsuario() {
    const [tema, setTema] = useLocalStorage('tema', 'claro');
    const [idioma, setIdioma] = useLocalStorage('idioma', 'es');
    
    return (
        <div>
            <select value={tema} onChange={e => setTema(e.target.value)}>
                <option value="claro">Claro</option>
                <option value="oscuro">Oscuro</option>
            </select>
        </div>
    );
}
```

#### 4.2 useFetch - Custom Hook para Datos

```jsx
// hooks/useFetch.js
import { useState, useEffect } from 'react';

function useFetch(url, opciones = {}) {
    const [datos, setDatos] = useState(null);
    const [cargando, setCargando] = useState(true);
    const [error, setError] = useState(null);
    
    useEffect(() => {
        const controller = new AbortController();
        
        async function fetchData() {
            try {
                setCargando(true);
                setError(null);
                
                const response = await fetch(url, {
                    ...opciones,
                    signal: controller.signal
                });
                
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}`);
                }
                
                const data = await response.json();
                setDatos(data);
            } catch (err) {
                if (err.name !== 'AbortError') {
                    setError(err.message);
                }
            } finally {
                setCargando(false);
            }
        }
        
        fetchData();
        
        return () => controller.abort();
    }, [url, opciones.method, opciones.body]);
    
    // Función para re-fetch manual
    const refetch = () => {
        setCargando(true);
        setError(null);
        // Volver a ejecutar el efecto
    };
    
    return { datos, cargando, error, refetch };
}

export default useFetch;
```

**Uso:**
```jsx
function ListaEventos() {
    const { datos, cargando, error } = useFetch('/api/eventos');
    
    if (cargando) return <Spinner />;
    if (error) return <Error mensaje={error} />;
    
    return (
        <ul>
            {datos.map(evento => (
                <li key={evento.id}>{evento.titulo}</li>
            ))}
        </ul>
    );
}
```

#### 4.3 useDebounce

```jsx
// hooks/useDebounce.js
import { useState, useEffect } from 'react';

function useDebounce(valor, delay = 500) {
    const [valorDebounced, setValorDebounced] = useState(valor);
    
    useEffect(() => {
        const timer = setTimeout(() => {
            setValorDebounced(valor);
        }, delay);
        
        return () => clearTimeout(timer);
    }, [valor, delay]);
    
    return valorDebounced;
}

export default useDebounce;
```

**Uso con búsqueda:**
```jsx
function BuscadorEventos() {
    const [busqueda, setBusqueda] = useState('');
    const busquedaDebounced = useDebounce(busqueda, 300);
    
    const { datos } = useFetch(
        busquedaDebounced 
            ? `/api/eventos?q=${busquedaDebounced}`
            : '/api/eventos'
    );
    
    return (
        <input 
            value={busqueda}
            onChange={e => setBusqueda(e.target.value)}
            placeholder="Buscar eventos..."
        />
    );
}
```

#### 4.4 useToggle

```jsx
// hooks/useToggle.js
import { useState, useCallback } from 'react';

function useToggle(valorInicial = false) {
    const [valor, setValor] = useState(valorInicial);
    
    const toggle = useCallback(() => {
        setValor(v => !v);
    }, []);
    
    const setTrue = useCallback(() => setValor(true), []);
    const setFalse = useCallback(() => setValor(false), []);
    
    return [valor, toggle, setTrue, setFalse];
}

export default useToggle;
```

---

### 5. useContext - Estado Global

#### 5.1 Crear Contexto

```jsx
// context/AuthContext.jsx
import { createContext, useContext, useState } from 'react';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
    const [usuario, setUsuario] = useState(null);
    const [token, setToken] = useState(null);
    
    const login = async (email, password) => {
        const response = await fetch('/api/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });
        
        if (response.ok) {
            const data = await response.json();
            setUsuario(data.usuario);
            setToken(data.token);
            return true;
        }
        return false;
    };
    
    const logout = () => {
        setUsuario(null);
        setToken(null);
    };
    
    const valor = {
        usuario,
        token,
        login,
        logout,
        isAuthenticated: !!token
    };
    
    return (
        <AuthContext.Provider value={valor}>
            {children}
        </AuthContext.Provider>
    );
}

export function useAuth() {
    const contexto = useContext(AuthContext);
    if (!contexto) {
        throw new Error('useAuth debe usarse dentro de AuthProvider');
    }
    return contexto;
}
```

#### 5.2 Usar Contexto

```jsx
// components/Header.jsx
import { useAuth } from '../context/AuthContext';

function Header() {
    const { usuario, logout, isAuthenticated } = useAuth();
    
    return (
        <header>
            <h1>Mi App</h1>
            {isAuthenticated ? (
                <div>
                    <span>Hola, {usuario.nombre}</span>
                    <button onClick={logout}>Cerrar Sesión</button>
                </div>
            ) : (
                <a href="/login">Iniciar Sesión</a>
            )}
        </header>
    );
}
```

---

## 💻 Contenido Práctico

### 6. Estructura de Hooks

```
src/
├── hooks/
│   ├── useLocalStorage.js
│   ├── useFetch.js
│   ├── useDebounce.js
│   ├── useToggle.js
│   ├── useAuth.js        #导出 useAuth
│   └── index.js          #exportar todos
├── context/
│   ├── AuthContext.jsx
│   └── ThemeContext.jsx
├── components/
└── pages/
```

### 7. Ejercicio Resuelto: Lista de Eventos con Hooks

```jsx
// hooks/useEventos.js
import { useState, useEffect, useCallback } from 'react';

const EVENTOS_API = '/api/eventos';

export function useEventos() {
    const [eventos, setEventos] = useState([]);
    const [cargando, setCargando] = useState(true);
    const [error, setError] = useState(null);
    
    const fetchEventos = useCallback(async () => {
        try {
            setCargando(true);
            const response = await fetch(EVENTOS_API);
            if (!response.ok) throw new Error('Error al cargar');
            const data = await response.json();
            setEventos(data);
        } catch (err) {
            setError(err.message);
        } finally {
            setCargando(false);
        }
    }, []);
    
    useEffect(() => {
        fetchEventos();
    }, [fetchEventos]);
    
    const agregarEvento = useCallback(async (nuevoEvento) => {
        const response = await fetch(EVENTOS_API, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(nuevoEvento)
        });
        
        if (response.ok) {
            const evento = await response.json();
            setEventos(prev => [...prev, evento]);
            return evento;
        }
        return null;
    }, []);
    
    const eliminarEvento = useCallback(async (id) => {
        const response = await fetch(`${EVENTOS_API}/${id}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            setEventos(prev => prev.filter(e => e.id !== id));
            return true;
        }
        return false;
    }, []);
    
    return {
        eventos,
        cargando,
        error,
        refetch: fetchEventos,
        agregarEvento,
        eliminarEvento
    };
}

// hooks/useFiltroEventos.js
import { useState, useMemo } from 'react';

export function useFiltroEventos(eventos) {
    const [filtroTexto, setFiltroTexto] = useState('');
    const [filtroCategoria, setFiltroCategoria] = useState('todas');
    const [sortBy, setSortBy] = useState('fecha');
    
    const eventosFiltrados = useMemo(() => {
        let resultado = [...eventos];
        
        // Filtrar por texto
        if (filtroTexto) {
            const texto = filtroTexto.toLowerCase();
            resultado = resultado.filter(e => 
                e.titulo.toLowerCase().includes(texto) ||
                e.descripcion?.toLowerCase().includes(texto)
            );
        }
        
        // Filtrar por categoría
        if (filtroCategoria !== 'todas') {
            resultado = resultado.filter(e => e.categoria === filtroCategoria);
        }
        
        // Ordenar
        resultado.sort((a, b) => {
            switch (sortBy) {
                case 'fecha':
                    return new Date(a.fecha) - new Date(b.fecha);
                case 'precio':
                    return a.precio - b.precio;
                case 'titulo':
                    return a.titulo.localeCompare(b.titulo);
                default:
                    return 0;
            }
        });
        
        return resultado;
    }, [eventos, filtroTexto, filtroCategoria, sortBy]);
    
    return {
        filtroTexto,
        setFiltroTexto,
        filtroCategoria,
        setFiltroCategoria,
        sortBy,
        setSortBy,
        eventosFiltrados
    };
}

// Componente principal
function EventoList() {
    const { eventos, cargando, error, agregarEvento, eliminarEvento } = useEventos();
    const {
        filtroTexto,
        setFiltroTexto,
        filtroCategoria,
        setFiltroCategoria,
        sortBy,
        setSortBy,
        eventosFiltrados
    } = useFiltroEventos(eventos);
    
    if (cargando) return <div className="loading">Cargando...</div>;
    if (error) return <div className="error">Error: {error}</div>;
    
    return (
        <div className="evento-list">
            <div className="filtros">
                <input
                    value={filtroTexto}
                    onChange={e => setFiltroTexto(e.target.value)}
                    placeholder="Buscar..."
                />
                <select 
                    value={filtroCategoria} 
                    onChange={e => setFiltroCategoria(e.target.value)}
                >
                    <option value="todas">Todas</option>
                    <option value="musica">Música</option>
                    <option value="deportes">Deportes</option>
                </select>
                <select value={sortBy} onChange={e => setSortBy(e.target.value)}>
                    <option value="fecha">Fecha</option>
                    <option value="precio">Precio</option>
                    <option value="titulo">Título</option>
                </select>
            </div>
            
            <div className="eventos-grid">
                {eventosFiltrados.map(evento => (
                    <EventoCard 
                        key={evento.id} 
                        evento={evento}
                        onEliminar={() => eliminarEvento(evento.id)}
                    />
                ))}
            </div>
        </div>
    );
}
```

---

## 🛠️ Ejercicios Prácticos

### Ejercicio 1: Custom Hook usePagination
- Crear hook que maneje paginación
- Retornar: páginaActual, totalPaginas, siguiente, anterior, irAPagina

### Ejercicio 2: Custom Hook useForm
- Manejar estado de formulario
- Validar campos
- Retornar valores y handlers

### Ejercicio 3: useIntersectionObserver
- Detectar cuando un elemento es visible
- Usar para lazy loading de imágenes

### Ejercicio 4: Context con Múltiples Valores
- Crear ThemeContext para tema claro/oscuro
- Consumir en múltiples componentes

---

## 🚀 Proyecto de la Clase

### Sistema de Eventos con Hooks Avanzados

```jsx
// App.jsx - Usando todos los hooks
import { useState, useCallback } from 'react';
import { AuthProvider } from './context/AuthContext';
import { ThemeProvider } from './context/ThemeContext';
import { useEventos } from './hooks/useEventos';
import { useFiltroEventos } from './hooks/useFiltroEventos';
import useLocalStorage from './hooks/useLocalStorage';
import EventoList from './pages/EventoList';
import EventoForm from './pages/EventoForm';
import Header from './components/Header';

function App() {
    const { eventos, cargando, agregarEvento } = useEventos();
    const filtros = useFiltroEventos(eventos);
    const [mostrarFormulario, setMostrarFormulario] = useState(false);
    
    const handleCrearEvento = async (datos) => {
        const nuevo = await agregarEvento(datos);
        if (nuevo) {
            setMostrarFormulario(false);
        }
    };
    
    return (
        <AuthProvider>
            <ThemeProvider>
                <div className="app">
                    <Header />
                    <main>
                        <button onClick={() => setMostrarFormulario(true)}>
                            Crear Evento
                        </button>
                        
                        {mostrarFormulario && (
                            <Modal onClose={() => setMostrarFormulario(false)}>
                                <EventoForm onSubmit={handleCrearEvento} />
                            </Modal>
                        )}
                        
                        <EventoList {...filtros} />
                    </main>
                </div>
            </ThemeProvider>
        </AuthProvider>
    );
}

export default App;
```

### Entregables

1. **Custom hooks** funcionales (useFetch, useLocalStorage, useDebounce)
2. **Context** para autenticación y tema
3. **Componentes** usando los hooks
4. **Filtros y ordenamiento** optimizados con useMemo

---

## 📚 Recursos Adicionales

- [React Hooks API Reference](https://react.dev/reference/react)
- [Building Reusable Custom Hooks](https://react.dev/learn/reusing-logic-with-custom-hooks)
- [useEffect Ultimate Guide](https://overreacted.io/a-complete-guide-to-useeffect/)
