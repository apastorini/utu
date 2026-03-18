# 🧭 Clase 18: React Routing y Estado Global

**Duración:** 4 horas  
**Objetivo:** Dominar React Router y gestión de estado con Redux Toolkit  
**Proyecto:** Sistema de eventos con navegación y estado global

---

## 📚 Contenido Teórico

### 1. React Router v6

#### 1.1 Configuración Básica

```bash
npm install react-router-dom
```

```jsx
// main.jsx
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import App from './App';
import './index.css';

createRoot(document.getElementById('root')).render(
    <StrictMode>
        <BrowserRouter>
            <App />
        </BrowserRouter>
    </StrictMode>
);
```

```jsx
// App.jsx
import { Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Eventos from './pages/Eventos';
import EventoDetalle from './pages/EventoDetalle';
import Login from './pages/Login';
import Register from './pages/Register';
import Perfil from './pages/Perfil';
import Admin from './pages/Admin';
import NotFound from './pages/NotFound';
import Layout from './components/Layout';

function App() {
    return (
        <Routes>
            <Route path="/" element={<Layout />}>
                <Route index element={<Home />} />
                <Route path="eventos" element={<Eventos />} />
                <Route path="eventos/:id" element={<EventoDetalle />} />
                <Route path="perfil" element={<Perfil />} />
                <Route path="admin" element={<Admin />} />
            </Route>
            
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            
            <Route path="*" element={<NotFound />} />
        </Routes>
    );
}

export default App;
```

#### 1.2 Layout con Outlet

```jsx
// components/Layout.jsx
import { Outlet, Link } from 'react-router-dom';

function Layout() {
    return (
        <div className="layout">
            <header>
                <nav>
                    <Link to="/">Inicio</Link>
                    <Link to="/eventos">Eventos</Link>
                    <Link to="/perfil">Perfil</Link>
                </nav>
            </header>
            
            <main>
                {/* Outlet renderiza la ruta hijo actual */}
                <Outlet />
            </main>
            
            <footer>
                <p>&copy; 2024 Mi App</p>
            </footer>
        </div>
    );
}

export default Layout;
```

---

### 2. Navegación Programática

#### 2.1 useNavigate

```jsx
import { useNavigate } from 'react-router-dom';

function LoginForm() {
    const navigate = useNavigate();
    
    const handleSubmit = async (e) => {
        e.preventDefault();
        
        const success = await login();
        
        if (success) {
            // Navegar a página anterior o home
            navigate('/', { replace: true });
            // O navegar a una ruta específica
            // navigate('/perfil');
        }
    };
    
    return <form onSubmit={handleSubmit}>...</form>;
}
```

#### 2.2 Parámetros de Ruta

```jsx
// Route: /eventos/:id
import { useParams, useNavigate } from 'react-router-dom';

function EventoDetalle() {
    const { id } = useParams();
    const navigate = useNavigate();
    
    // El ID viene como string
    const eventoId = parseInt(id);
    
    return (
        <div>
            <button onClick={() => navigate('/eventos')}>
                Volver a Eventos
            </button>
            <h1>Evento #{id}</h1>
        </div>
    );
}
```

#### 2.3 useLocation y query params

```jsx
import { useLocation, useSearchParams } from 'react-router-dom';

function Eventos() {
    const location = useLocation();
    const [searchParams, setSearchParams] = useSearchParams();
    
    const categoria = searchParams.get('categoria');
    const pagina = searchParams.get('pagina') || 1;
    
    const cambiarCategoria = (cat) => {
        setSearchParams({ categoria: cat, pagina: '1' });
    };
    
    return (
        <div>
            <p>Path: {location.pathname}</p>
            <p>Categoría: {categoria}</p>
            <button onClick={() => cambiarCategoria('musica')}>
                Música
            </button>
        </div>
    );
}
```

---

### 3. Rutas Anidadas y Protected Routes

#### 3.1 Rutas Anidadas

```jsx
function App() {
    return (
        <Routes>
            <Route path="/admin" element={<AdminLayout />}>
                <Route index element={<AdminDashboard />} />
                <Route path="usuarios" element={<AdminUsuarios />} />
                <Route path="eventos" element={<AdminEventos />} />
                <Route path="configuracion" element={<AdminConfig />} />
            </Route>
        </Routes>
    );
}

// AdminLayout.jsx
import { Outlet } from 'react-router-dom';

function AdminLayout() {
    return (
        <div className="admin-layout">
            <aside>
                <nav>
                    <Link to="/admin">Dashboard</Link>
                    <Link to="/admin/usuarios">Usuarios</Link>
                    <Link to="/admin/eventos">Eventos</Link>
                </nav>
            </aside>
            <main>
                <Outlet />
            </main>
        </div>
    );
}
```

#### 3.2 Rutas Protegidas

```jsx
// components/ProtectedRoute.jsx
import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

function ProtectedRoute({ children, roles = [] }) {
    const { usuario, isAuthenticated } = useAuth();
    const location = useLocation();
    
    if (!isAuthenticated) {
        // Redirigir al login, guardando la ubicación actual
        return <Navigate to="/login" state={{ from: location }} replace />;
    }
    
    // Verificar roles si se especificaron
    if (roles.length > 0 && !roles.includes(usuario?.rol)) {
        return <Navigate to="/" replace />;
    }
    
    return children;
}

// Uso en App.jsx
function App() {
    return (
        <Routes>
            <Route path="/admin" element={
                <ProtectedRoute roles={['admin']}>
                    <AdminLayout />
                </ProtectedRoute>
            }>
                <Route index element={<AdminDashboard />} />
            </Route>
        </Routes>
    );
}
```

---

### 4. Lazy Loading de Rutas

```jsx
import { Suspense, lazy } from 'react';
import { Routes, Route } from 'react-router-dom';
import Spinner from './components/Spinner';

// Lazy loading - código dividido
const Home = lazy(() => import('./pages/Home'));
const Eventos = lazy(() => import('./pages/Eventos'));
const EventoDetalle = lazy(() => import('./pages/EventoDetalle'));
const Admin = lazy(() => import('./pages/Admin'));

function App() {
    return (
        <Suspense fallback={<Spinner />}>
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/eventos" element={<Eventos />} />
                <Route path="/eventos/:id" element={<EventoDetalle />} />
                <Route path="/admin" element={<Admin />} />
            </Routes>
        </Suspense>
    );
}
```

---

### 5. Redux Toolkit

#### 5.1 Instalación y Configuración

```bash
npm install @reduxjs/toolkit react-redux
```

```jsx
// store/index.js
import { configureStore } from '@reduxjs/toolkit';
import eventoReducer from './slices/eventoSlice';
import usuarioReducer from './slices/usuarioSlice';
import uiReducer from './slices/uiSlice';

export const store = configureStore({
    reducer: {
        eventos: eventoReducer,
        usuario: usuarioReducer,
        ui: uiReducer
    },
    middleware: (getDefaultMiddleware) =>
        getDefaultMiddleware({
            serializableCheck: false
        })
});

export default store;
```

#### 5.2 Slices

```jsx
// store/slices/eventoSlice.js
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';

// Async Thunk para fetching
export const fetchEventos = createAsyncThunk(
    'eventos/fetchEventos',
    async (_, { rejectWithValue }) => {
        try {
            const response = await fetch('/api/eventos');
            if (!response.ok) throw new Error('Error al cargar');
            return await response.json();
        } catch (error) {
            return rejectWithValue(error.message);
        }
    }
);

export const crearEvento = createAsyncThunk(
    'eventos/crearEvento',
    async (evento, { rejectWithValue }) => {
        try {
            const response = await fetch('/api/eventos', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(evento)
            });
            if (!response.ok) throw new Error('Error al crear');
            return await response.json();
        } catch (error) {
            return rejectWithValue(error.message);
        }
    }
);

const eventoSlice = createSlice({
    name: 'eventos',
    initialState: {
        lista: [],
        eventoActual: null,
        cargando: false,
        error: null,
        filtros: {
            categoria: 'todas',
            busqueda: ''
        }
    },
    reducers: {
        setEventoActual: (state, action) => {
            state.eventoActual = action.payload;
        },
        setFiltros: (state, action) => {
            state.filtros = { ...state.filtros, ...action.payload };
        },
        clearError: (state) => {
            state.error = null;
        }
    },
    extraReducers: (builder) => {
        builder
            // Fetch eventos
            .addCase(fetchEventos.pending, (state) => {
                state.cargando = true;
                state.error = null;
            })
            .addCase(fetchEventos.fulfilled, (state, action) => {
                state.cargando = false;
                state.lista = action.payload;
            })
            .addCase(fetchEventos.rejected, (state, action) => {
                state.cargando = false;
                state.error = action.payload;
            })
            // Crear evento
            .addCase(crearEvento.fulfilled, (state, action) => {
                state.lista.push(action.payload);
            });
    }
});

export const { setEventoActual, setFiltros, clearError } = eventoSlice.actions;
export default eventoSlice.reducer;
```

#### 5.3 Selectors

```jsx
// store/selectors/eventoSelectors.js
import { createSelector } from '@reduxjs/toolkit';

// Selector básico
export const selectEventos = (state) => state.eventos.lista;
export const selectCargando = (state) => state.eventos.cargando;
export const selectError = (state) => state.eventos.error;

// Selector memoizado
export const selectEventosFiltrados = createSelector(
    [selectEventos, (state) => state.eventos.filtros],
    (eventos, filtros) => {
        let resultado = [...eventos];
        
        if (filtros.busqueda) {
            const texto = filtros.busqueda.toLowerCase();
            resultado = resultado.filter(e => 
                e.titulo.toLowerCase().includes(texto)
            );
        }
        
        if (filtros.categoria !== 'todas') {
            resultado = resultado.filter(e => e.categoria === filtros.categoria);
        }
        
        return resultado;
    }
);

// Selector con parámetro
export const selectEventoPorId = (id) => createSelector(
    [selectEventos],
    (eventos) => eventos.find(e => e.id === parseInt(id))
);
```

---

### 6. Uso de Redux en Componentes

#### 6.1 useSelector y useDispatch

```jsx
import { useSelector, useDispatch } from 'react-redux';
import { fetchEventos, setFiltros } from '../store/slices/eventoSlice';
import { selectEventosFiltrados, selectCargando, selectError } from '../store/selectors/eventoSelectors';

function EventoList() {
    const dispatch = useDispatch();
    const eventos = useSelector(selectEventosFiltrados);
    const cargando = useSelector(selectCargando);
    const error = useSelector(selectError);
    
    useEffect(() => {
        dispatch(fetchEventos());
    }, [dispatch]);
    
    const handleFiltroChange = (filtros) => {
        dispatch(setFiltros(filtros));
    };
    
    if (cargando) return <Spinner />;
    if (error) return <Error message={error} />;
    
    return (
        <div>
            {eventos.map(evento => (
                <EventoCard key={evento.id} evento={evento} />
            ))}
        </div>
    );
}
```

---

## 💻 Contenido Práctico

### 7. Estructura del Proyecto

```
src/
├── store/
│   ├── index.js
│   ├── slices/
│   │   ├── eventoSlice.js
│   │   ├── usuarioSlice.js
│   │   └── uiSlice.js
│   └── selectors/
│       ├── eventoSelectors.js
│       └── usuarioSelectors.js
├── pages/
│   ├── Home.jsx
│   ├── Eventos.jsx
│   ├── EventoDetalle.jsx
│   ├── Login.jsx
│   ├── Register.jsx
│   ├── Perfil.jsx
│   ├── Admin/
│   │   ├── AdminLayout.jsx
│   │   ├── Dashboard.jsx
│   │   └── Usuarios.jsx
│   └── NotFound.jsx
├── components/
│   ├── Layout.jsx
│   ├── ProtectedRoute.jsx
│   └── ...
```

### 8. Ejercicio Resuelto: Sistema de Eventos con Routing y Redux

```jsx
// pages/Eventos.jsx - Página completa
import { useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { Link } from 'react-router-dom';
import { fetchEventos, setFiltros } from '../store/slices/eventoSlice';
import { selectEventosFiltrados, selectCargando, selectError } from '../store/selectors/eventoSelectors';
import EventoCard from '../components/EventoCard';
import Spinner from '../components/Spinner';

function Eventos() {
    const dispatch = useDispatch();
    const eventos = useSelector(selectEventosFiltrados);
    const cargando = useSelector(selectCargando);
    const error = useSelector(selectError);
    const filtros = useSelector(state => state.eventos.filtros);
    
    useEffect(() => {
        dispatch(fetchEventos());
    }, [dispatch]);
    
    const handleFiltroChange = (key, value) => {
        dispatch(setFiltros({ [key]: value }));
    };
    
    if (cargando) return <Spinner />;
    if (error) return <div className="error">Error: {error}</div>;
    
    return (
        <div className="eventos-page">
            <header className="eventos-header">
                <h1>Todos los Eventos</h1>
                <Link to="/eventos/nuevo" className="btn btn-primary">
                    Crear Evento
                </Link>
            </header>
            
            <div className="filtros">
                <input
                    type="text"
                    placeholder="Buscar eventos..."
                    value={filtros.busqueda}
                    onChange={e => handleFiltroChange('busqueda', e.target.value)}
                    className="input-busqueda"
                />
                
                <select
                    value={filtros.categoria}
                    onChange={e => handleFiltroChange('categoria', e.target.value)}
                >
                    <option value="todas">Todas las categorías</option>
                    <option value="musica">Música</option>
                    <option value="deportes">Deportes</option>
                    <option value="tecnologia">Tecnología</option>
                </select>
            </div>
            
            <div className="eventos-grid">
                {eventos.map(evento => (
                    <Link 
                        to={`/eventos/${evento.id}`} 
                        key={evento.id}
                        className="evento-link"
                    >
                        <EventoCard evento={evento} />
                    </Link>
                ))}
            </div>
            
            {eventos.length === 0 && (
                <p className="no-resultados">
                    No se encontraron eventos
                </p>
            )}
        </div>
    );
}

export default Eventos;
```

```jsx
// pages/EventoDetalle.jsx
import { useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useSelector, useDispatch } from 'react-redux';
import { fetchEventoPorId, setEventoActual } from '../store/slices/eventoSlice';

function EventoDetalle() {
    const { id } = useParams();
    const navigate = useNavigate();
    const dispatch = useDispatch();
    const { eventoActual, cargando, error } = useSelector(state => state.eventos);
    
    useEffect(() => {
        dispatch(fetchEventoPorId(id));
        
        return () => {
            dispatch(setEventoActual(null));
        };
    }, [dispatch, id]);
    
    if (cargando) return <Spinner />;
    if (error) return <div className="error">{error}</div>;
    if (!eventoActual) return <div>No encontrado</div>;
    
    return (
        <div className="evento-detalle">
            <button onClick={() => navigate(-1)} className="btn-volver">
                ← Volver
            </button>
            
            <div className="evento-imagen">
                <img src={eventoActual.imagen} alt={eventoActual.titulo} />
            </div>
            
            <h1>{eventoActual.titulo}</h1>
            <p className="fecha">{eventoActual.fecha}</p>
            <p className="ubicacion">{eventoActual.ubicacion}</p>
            <p className="descripcion">{eventoActual.descripcion}</p>
            <p className="precio">${eventoActual.precio}</p>
            
            <button 
                onClick={() => navigate(`/eventos/${id}/comprar`)}
                className="btn btn-primary"
            >
                Comprar Entrada
            </button>
        </div>
    );
}

export default EventoDetalle;
```

---

## 🛠️ Ejercicios Prácticos

### Ejercicio 1: Rutas con Parámetros
- Crear ruta `/eventos/:categoria`
- Filtrar automáticamente por categoría

### Ejercicio 2: Breadcrumbs
- Crear componente que muestre navegación basada en ruta actual

### Ejercicio 3: Redux con Múltiples Slices
- Crear slice para autenticación
- Crear slice para UI (loading, modals)

### Ejercicio 4: Infinite Scroll
- Implementar paginación infinita con Redux

---

## 🚀 Proyecto de la Clase

### Sistema de Eventos con Routing y Redux

```jsx
// App.jsx - Configuración completa
import { Provider } from 'react-redux';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import store from './store';
import Layout from './components/Layout';
import Home from './pages/Home';
import Eventos from './pages/Eventos';
import EventoDetalle from './pages/EventoDetalle';
import EventoForm from './pages/EventoForm';
import Login from './pages/Login';
import Register from './pages/Register';
import Perfil from './pages/Perfil';
import AdminLayout from './pages/admin/AdminLayout';
import Dashboard from './pages/admin/Dashboard';
import ProtectedRoute from './components/ProtectedRoute';

function App() {
    return (
        <Provider store={store}>
            <BrowserRouter>
                <Routes>
                    <Route path="/" element={<Layout />}>
                        <Route index element={<Home />} />
                        <Route path="eventos" element={<Eventos />} />
                        <Route path="eventos/:id" element={<EventoDetalle />} />
                        <Route path="eventos/nuevo" element={
                            <ProtectedRoute>
                                <EventoForm />
                            </ProtectedRoute>
                        } />
                        <Route path="login" element={<Login />} />
                        <Route path="register" element={<Register />} />
                        <Route path="perfil" element={
                            <ProtectedRoute>
                                <Perfil />
                            </ProtectedRoute>
                        } />
                    </Route>
                    
                    <Route path="/admin" element={
                        <ProtectedRoute roles={['admin']}>
                            <AdminLayout />
                        </ProtectedRoute>
                    }>
                        <Route index element={<Dashboard />} />
                    </Route>
                    
                    <Route path="*" element={<NotFound />} />
                </Routes>
            </BrowserRouter>
        </Provider>
    );
}

export default App;
```

### Entregables

1. **Sistema de rutas** completo con layout
2. **Rutas protegidas** por autenticación y roles
3. **Estado global** con Redux Toolkit
4. **Async thunks** para API calls
5. **Selectores memoizados** para optimización

---

## 📚 Recursos Adicionales

- [React Router v6 Docs](https://reactrouter.com/)
- [Redux Toolkit Docs](https://redux-toolkit.js.org/)
- [Redux with React](https://react-redux.js.org/)
