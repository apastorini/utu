# 📱 Clase 11: Hooks, Estados y Efectos

**Duración:** 4 horas  
**Objetivo:** Dominar useState, useEffect y crear hooks personalizados  
**Proyecto:** Gestión de estado en el sistema de eventos

---

## 📚 Contenido Teórico

### 1. Fundamentos del Estado en React

#### 1.1 ¿Qué es el Estado?

El **estado** son datos que cambian a lo largo del tiempo en un componente. Cuando el estado cambia, React vuelve a renderizar el componente para reflejar esos cambios en la UI.

**Diferencia entre Props y State:**

| Props | State |
|-------|-------|
| Se pasan desde el padre | Se define dentro del componente |
| Solo lectura | Mutable (con setState) |
| Configuran el componente | Controlan el comportamiento |
| Inmutables | Cambian con el tiempo |

#### 1.2 El Ciclo de Vida del Componente

```
┌─────────────────────────────────────────────────────────────────┐
│                    CICLO DE VIDA                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────┐     ┌──────────┐     ┌─────────────┐               │
│  │ MOUNT    │────►│ UPDATE   │────►│ UNMOUNT     │               │
│  │ (montaje)│     │ (actualiz)│     │ (desmontaje)│               │
│  └──────────┘     └──────────┘     └─────────────┘               │
│       │                │                  │                       │
│       ▼                ▼                  ▼                       │
│  • Constructor    • setState          • Cleanup                  │
│  • useEffect[]    • useEffect[deps]   • componentWillUnmount     │
│  • render         • render            • useEffect return         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

### 2. useState - Gestión de Estado

#### 2.1 useState Básico

```jsx
import { useState } from 'react';

function Contador() {
    // Desestructuración: [valorActual, funcionQueActualiza]
    const [contador, setContador] = useState(0);
    
    return (
        <div>
            <p>Contador: {contador}</p>
            <button onClick={() => setContador(contador + 1)}>
                Incrementar
            </button>
        </div>
    );
}
```

#### 2.2 Estado con Objetos

```jsx
function Formulario() {
    const [datos, setDatos] = useState({
        nombre: '',
        email: '',
        telefono: '',
        direccion: ''
    });
    
    // Forma correcta: usar función callback si el nuevo 
    // estado depende del anterior
    const handleChange = (e) => {
        const { name, value } = e.target;
        
        setDatos(prev => ({
            ...prev,
            [name]: value  // Computed property name
        }));
    };
    
    return (
        <form>
            <input
                name="nombre"
                value={datos.nombre}
                onChange={handleChange}
            />
            <input
                name="email"
                value={datos.email}
                onChange={handleChange}
            />
            <input
                name="telefono"
                value={datos.telefono}
                onChange={handleChange}
            />
        </form>
    );
}
```

#### 2.3 Estado Inicial Funcional

```jsx
// Malo: la función se ejecuta en cada render
const [state, setState] = useState(calcularExpensiveInitialState());

// Bueno: la función solo se ejecuta en el primer render
const [state, setState] = useState(() => calcularExpensiveInitialState());
```

---

### 3. useEffect - Efectos Secundarios

#### 3.1 ¿Qué son los Efectos?

Los **efectos secundarios** son operaciones que ocurren fuera del renderizado:
- Fetch de datos
- Suscripciones a WebSockets
- Timers (setTimeout, setInterval)
- Manipulación del DOM
- Logging

#### 3.2 useEffect con Dependencias

```jsx
import { useState, useEffect } from 'react';

function UserProfile({ userId }) {
    const [usuario, setUsuario] = useState(null);
    const [cargando, setCargando] = useState(true);
    const [error, setError] = useState(null);
    
    // useEffect: se ejecuta cuando userId cambia
    useEffect(() => {
        async function fetchUsuario() {
            try {
                setCargando(true);
                setError(null);
                
                const response = await fetch(`/api/usuarios/${userId}`);
                
                if (!response.ok) {
                    throw new Error('Error al cargar usuario');
                }
                
                const data = await response.json();
                setUsuario(data);
            } catch (err) {
                setError(err.message);
            } finally {
                setCargando(false);
            }
        }
        
        fetchUsuario();
    }, [userId]); // ← Dependencia: solo se ejecuta cuando userId cambia
    
    if (cargando) return <div>Cargando...</div>;
    if (error) return <div>Error: {error}</div>;
    if (!usuario) return null;
    
    return <div>{usuario.nombre}</div>;
}
```

#### 3.3 Casos de Uso Comunes

**1. Fetch de datos con cleanup:**
```jsx
function useFetch(url) {
    const [datos, setDatos] = useState(null);
    const [cargando, setCargando] = useState(true);
    const [error, setError] = useState(null);
    
    useEffect(() => {
        const controller = new AbortController();
        
        async function fetchData() {
            try {
                setCargando(true);
                const response = await fetch(url, {
                    signal: controller.signal
                });
                
                if (!response.ok) {
                    throw new Error('Error en la petición');
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
        
        // Cleanup: cancelar petición al desmontar
        return () => controller.abort();
    }, [url]);
    
    return { datos, cargando, error };
}
```

**2. WebSocket:**
```jsx
function useWebSocket(url) {
    const [mensajes, setMensajes] = useState([]);
    const [conectado, setConectado] = useState(false);
    
    useEffect(() => {
        const ws = new WebSocket(url);
        
        ws.onopen = () => setConectado(true);
        
        ws.onmessage = (event) => {
            const mensaje = JSON.parse(event.data);
            setMensajes(prev => [...prev, mensaje]);
        };
        
        ws.onclose = () => setConectado(false);
        
        // Cleanup: cerrar conexión
        return () => ws.close();
    }, [url]);
    
    return { mensajes, conectado };
}
```

**3. Intervalos:**
```jsx
function Timer() {
    const [segundos, setSegundos] = useState(0);
    
    useEffect(() => {
        const interval = setInterval(() => {
            setSegundos(s => s + 1);
        }, 1000);
        
        // Cleanup: limpiar intervalo
        return () => clearInterval(interval);
    }, []); // Array vacío = solo al montar
    
    return <div>Tiempo: {segundos}s</div>;
}
```

---

### 4. Hooks Personalizados (Custom Hooks)

#### 4.1 ¿Qué son?

Los **custom hooks** son funciones que reutilizan lógica con estado. Su nombre debe empezar con "use".

```jsx
// useLocalStorage.js
import { useState, useEffect } from 'react';

function useLocalStorage(clave, valorInicial) {
    // Obtener valor inicial
    const [valor, setValor] = useState(() => {
        try {
            const item = localStorage.getItem(clave);
            return item ? JSON.parse(item) : valorInicial;
        } catch (error) {
            console.error('Error leyendo localStorage:', error);
            return valorInicial;
        }
    });
    
    // Guardar cuando cambie el valor
    useEffect(() => {
        try {
            localStorage.setItem(clave, JSON.stringify(valor));
        } catch (error) {
            console.error('Error guardando en localStorage:', error);
        }
    }, [clave, valor]);
    
    return [valor, setValor];
}

// Uso
function Preferencias() {
    const [tema, setTema] = useLocalStorage('tema', 'claro');
    const [idioma, setIdioma] = useLocalStorage('idioma', 'es');
    
    return (
        <div>
            <button onClick={() => setTema(tema === 'claro' ? 'oscuro' : 'claro')}>
                Tema: {tema}
            </button>
        </div>
    );
}
```

#### 4.2 useFetch Personalizado

```jsx
// useFetch.js
import { useState, useEffect, useRef } from 'react';

function useFetch(url, opciones = {}) {
    const [datos, setDatos] = useState(null);
    const [cargando, setCargando] = useState(true);
    const [error, setError] = useState(null);
    const abortControllerRef = useRef(null);
    
    useEffect(() => {
        const fetchData = async () => {
            // Cancelar petición anterior
            if (abortControllerRef.current) {
                abortControllerRef.current.abort();
            }
            
            abortControllerRef.current = new AbortController();
            
            try {
                setCargando(true);
                setError(null);
                
                const response = await fetch(url, {
                    ...opciones,
                    signal: abortControllerRef.current.signal
                });
                
                if (!response.ok) {
                    throw new Error(`Error: ${response.status}`);
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
        };
        
        fetchData();
        
        // Cleanup
        return () => {
            if (abortControllerRef.current) {
                abortControllerRef.current.abort();
            }
        };
    }, [url]);
    
    return { datos, cargando, error };
}

// Uso
function ListaEventos() {
    const { datos: eventos, cargando, error } = useFetch('/api/eventos');
    
    if (cargando) return <div>Cargando...</div>;
    if (error) return <div>Error: {error}</div>;
    
    return (
        <ul>
            {eventos.map(e => <li key={e.id}>{e.titulo}</li>)}
        </ul>
    );
}
```

---

### 5. useRef y useContext

#### 5.1 useRef

```jsx
// Referencia a elementos del DOM
function FormularioConFocus() {
    const inputRef = useRef(null);
    
    useEffect(() => {
        inputRef.current.focus();
    }, []);
    
    return <input ref={inputRef} />;
}

// Mutable sin re-render
function ContadorConRef() {
    const [contador, setContador] = useState(0);
    const renderCount = useRef(0);
    
    useEffect(() => {
        renderCount.current++;
    });
    
    return (
        <div>
            <p>Contador: {contador}</p>
            <p>Renderizados: {renderCount.current}</p>
            <button onClick={() => setContador(c => c + 1)}>
                Incrementar
            </button>
        </div>
    );
}
```

#### 5.2 useContext

```jsx
// AuthContext.js
import { createContext, useContext, useState, useEffect } from 'react';

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
        
        const data = await response.json();
        setUsuario(data.usuario);
        setToken(data.token);
        localStorage.setItem('token', data.token);
    };
    
    const logout = () => {
        setUsuario(null);
        setToken(null);
        localStorage.removeItem('token');
    };
    
    return (
        <AuthContext.Provider value={{ usuario, token, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
}

export function useAuth() {
    return useContext(AuthContext);
}

// Uso
function BotonLogout() {
    const { logout } = useAuth();
    return <button onClick={logout}>Cerrar Sesión</button>;
}

function InfoUsuario() {
    const { usuario } = useAuth();
    
    if (!usuario) return <p>No has iniciado sesión</p>;
    
    return <p>Hola, {usuario.nombre}</p>;
}
```

---

## 💻 Contenido Práctico

### Implementación del Proyecto

```jsx
// src/context/EventoContext.jsx
import { createContext, useContext, useState, useEffect, useCallback } from 'react';

const EventoContext = createContext(null);

export function EventoProvider({ children }) {
    const [eventos, setEventos] = useState([]);
    const [eventoActual, setEventoActual] = useState(null);
    const [cargando, setCargando] = useState(true);
    const [error, setError] = useState(null);
    const [filtros, setFiltros] = useState({
        categoria: 'todas',
        buscar: '',
        fechaDesde: '',
        fechaHasta: ''
    });
    
    const cargarEventos = useCallback(async () => {
        setCargando(true);
        setError(null);
        
        try {
            const response = await fetch('/api/eventos');
            
            if (!response.ok) {
                throw new Error('Error al cargar eventos');
            }
            
            const data = await response.json();
            setEventos(data);
        } catch (err) {
            setError(err.message);
            // Cargar datos de ejemplo si falla
            setEventos(EVENTOS_EJEMPLO);
        } finally {
            setCargando(false);
        }
    }, []);
    
    useEffect(() => {
        cargarEventos();
    }, [cargarEventos]);
    
    const crearEvento = async (datos) => {
        const response = await fetch('/api/eventos', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(datos)
        });
        
        if (!response.ok) {
            throw new Error('Error al crear evento');
        }
        
        const nuevoEvento = await response.json();
        setEventos(prev => [...prev, nuevoEvento]);
        
        return nuevoEvento;
    };
    
    const actualizarEvento = async (id, datos) => {
        const response = await fetch(`/api/eventos/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(datos)
        });
        
        const eventoActualizado = await response.json();
        setEventos(prev => 
            prev.map(e => e.id === id ? eventoActualizado : e)
        );
        
        return eventoActualizado;
    };
    
    const eliminarEvento = async (id) => {
        await fetch(`/api/eventos/${id}`, { method: 'DELETE' });
        setEventos(prev => prev.filter(e => e.id !== id));
    };
    
    const eventosFiltrados = eventos.filter(evento => {
        const coincideBuscar = evento.titulo
            .toLowerCase()
            .includes(filtros.buscar.toLowerCase());
        
        const coincideCategoria = filtros.categoria === 'todas' ||
            evento.categoria === filtros.categoria;
        
        return coincideBuscar && coincideCategoria;
    });
    
    const value = {
        eventos: eventosFiltrados,
        eventoActual,
        cargando,
        error,
        filtros,
        setFiltros,
        setEventoActual,
        crearEvento,
        actualizarEvento,
        eliminarEvento,
        recargar: cargarEventos
    };
    
    return (
        <EventoContext.Provider value={value}>
            {children}
        </EventoContext.Provider>
    );
}

export function useEventos() {
    const context = useContext(EventoContext);
    if (!context) {
        throw new Error('useEventos debe usarse dentro de EventoProvider');
    }
    return context;
}

const EVENTOS_EJEMPLO = [
    { id: '1', titulo: 'Concierto de Rock', fecha: '2024-03-15', precio: 50, categoria: 'musica', ubicacion: 'Estadio' },
    { id: '2', titulo: 'Festival de Jazz', fecha: '2024-03-20', precio: 35, categoria: 'musica', ubicacion: 'Teatro Solís' },
    { id: '3', titulo: 'Tech Conference', fecha: '2024-04-01', precio: 100, categoria: 'tecnologia', ubicacion: 'Punta del Este' },
];
```

---

## 🛠️ Ejercicios Prácticos

### Ejercicio 1: Formulario con Validación
- useState para cada campo
- Validar antes de enviar
- Mostrar errores al usuario

### Ejercicio 2: Fetch con useEffect
- Cargar eventos desde API
- Estados de carga y error
- Cleanup al desmontar

### Ejercicio 3: Custom Hooks
- useEventos: gestión de API
- useCarrito: compras
- useAuth: autenticación

### Ejercicio 4: Context
- Contexto de tema (claro/oscuro)
- Contexto de idioma
- Consumir en componentes

---

## 📚 Recursos Adicionales

- [Hooks API Reference](https://react.dev/reference/react)
- [useState](https://react.dev/reference/react/useState)
- [useEffect](https://react.dev/reference/react/useEffect)
- [Building Custom Hooks](https://react.dev/learn/reusing-logic-with-hooks)
