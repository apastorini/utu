# 📱 Clase 12: Rutas, Navegación y Layouts

**Duración:** 4 horas  
**Objetivo:** Implementar navegación con React Router y crear layouts reutilizables  
**Proyecto:** Sistema de rutas completo para la aplicación de eventos

---

## 📚 Contenido Teórico

### 1. Fundamentos de Routing en SPA

#### 1.1 ¿Qué es el Routing?

En una **Single Page Application (SPA)**, el routing permite cambiar la URL y el contenido sin recargar la página.

**SPA tradicional vs Multi Page:**
```
Traditional (Multi Page):
Request → Server → HTML Response → Page Reload

SPA (Single Page):
Request → JS Loads → Virtual DOM Update → No Reload
```

**Routing en SPA:**
```
URL: /eventos
  ↓
Router detecta cambio
  ↓
Carga componente EventoList
  ↓
Actualiza Virtual DOM
  ↓
URL cambia a /eventos/:id
  ↓
Carga componente EventoDetail
```

#### 1.2 React Router

React Router es la librería estándar para routing en React.

| Componente | Descripción |
|------------|-------------|
| **BrowserRouter** | Envuelve la app, usa HTML5 History API |
| **Routes** | Contenedor para todas las rutas |
| **Route** | Define una ruta específica |
| **Link** | Crea enlaces (no recargan) |
| **useNavigate** | Navegación programática |
| **useParams** | Lee parámetros de URL |
| **useLocation** | Información de la ruta actual |

---

### 2. Configuración de Rutas

#### 2.1 BrowserRouter

```jsx
// main.jsx
import { BrowserRouter } from 'react-router-dom';
import App from './App';

ReactDOM.createRoot(document.getElementById('root')).render(
    <React.StrictMode>
        <BrowserRouter>
            <App />
        </BrowserRouter>
    </React.StrictMode>
);
```

#### 2.2 Rutas Básicas

```jsx
// App.jsx
import { Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import EventoList from './pages/EventoList';
import EventoDetail from './pages/EventoDetail';
import Login from './pages/Login';
import NotFound from './pages/NotFound';

function App() {
    return (
        <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/eventos" element={<EventoList />} />
            <Route path="/eventos/:id" element={<EventoDetail />} />
            <Route path="/login" element={<Login />} />
            <Route path="*" element={<NotFound />} />
        </Routes>
    );
}
```

#### 2.3 Rutas con Parámetros

```jsx
// /eventos/:id - Parámetro dinámico
function EventoDetail() {
    const { id } = useParams();
    // id = "123" si URL es /eventos/123
    
    return <div>Evento ID: {id}</div>;
}

// /eventos/:categoria/:fecha - Múltiples parámetros
function FiltrarEventos() {
    const { categoria, fecha } = useParams();
    // /eventos/musica/2024-03
    // categoria = "musica"
    // fecha = "2024-03"
}
```

---

### 3. Navegación Programática

#### 3.1 useNavigate

```jsx
import { useNavigate } from 'react-router-dom';

function EventoCard({ evento }) {
    const navigate = useNavigate();
    
    const handleClick = () => {
        navigate(`/eventos/${evento.id}`);
    };
    
    const handleEditar = (e) => {
        e.stopPropagation();
        navigate(`/eventos/${evento.id}/editar`);
    };
    
    return (
        <div onClick={handleClick}>
            <h3>{evento.titulo}</h3>
            <button onClick={handleEditar}>Editar</button>
        </div>
    );
}
```

#### 3.2 Navegación con Estado

```jsx
function ResultadoBusqueda() {
    const navigate = useNavigate();
    
    const irAEvento = (evento) => {
        navigate('/eventos/' + evento.id, {
            state: { desde: 'busqueda', busqueda: 'rock' }
        });
    };
}

// Leer el estado
function EventoDetail() {
    const location = useLocation();
    const desde = location.state?.desde;
    
    return (
        <div>
            <p>Viniste desde: {desde}</p>
        </div>
    );
}
```

---

### 4. Rutas Anidadas y Layouts

#### 4.1 Outlet - Rutas Anidadas

```jsx
import { Outlet } from 'react-router-dom';

function Layout() {
    return (
        <div className="layout">
            <Header />
            <main>
                <Outlet />  {/* Aquí se renderiza la ruta hijo */}
            </main>
            <Footer />
        </div>
    );
}

function AuthLayout() {
    return (
        <div className="auth-layout">
            <div className="sidebar">
                <h1>TuFiesta</h1>
            </div>
            <div className="content">
                <Outlet />
            </div>
        </div>
    );
}
```

#### 4.2 Definir Rutas Anidadas

```jsx
function App() {
    return (
        <Routes>
            {/* Rutas con Layout público */}
            <Route element={<Layout />}>
                <Route path="/" element={<Home />} />
                <Route path="/eventos" element={<EventoList />} />
                <Route path="/eventos/:id" element={<EventoDetail />} />
            </Route>
            
            {/* Rutas con Layout de auth */}
            <Route element={<AuthLayout />}>
                <Route path="/login" element={<Login />} />
                <Route path="/register" element={<Register />} />
            </Route>
            
            {/* Rutas de admin */}
            <Route path="/admin" element={<AdminLayout />}>
                <Route index element={<Dashboard />} />
                <Route path="eventos" element={<AdminEventos />} />
                <Route path="usuarios" element={<AdminUsuarios />} />
            </Route>
        </Routes>
    );
}
```

---

### 5. Rutas Protegidas

#### 5.1 ProtectedRoute

```jsx
function ProtectedRoute({ children, requireAuth = true, rol }) {
    const { usuario, cargando } = useAuth();
    const location = useLocation();
    
    if (cargando) {
        return <div>Cargando...</div>;
    }
    
    if (requireAuth && !usuario) {
        return <Navigate to="/login" state={{ from: location }} replace />;
    }
    
    if (rol && usuario?.rol !== rol) {
        return <Navigate to="/" replace />;
    }
    
    return children;
}

// Uso
function App() {
    return (
        <Routes>
            <Route path="/perfil" element={
                <ProtectedRoute>
                    <Perfil />
                </ProtectedRoute>
            } />
            
            <Route path="/admin" element={
                <ProtectedRoute rol="admin">
                    <AdminPanel />
                </ProtectedRoute>
            } />
        </Routes>
    );
}
```

---

## 💻 Contenido Práctico

```jsx
// src/App.jsx
import { Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import ProtectedRoute from './components/ProtectedRoute';
import Loading from './components/Loading';

// Lazy loading
import { lazy, Suspense } from 'react';

const Home = lazy(() => import('./pages/Home'));
const EventoList = lazy(() => import('./pages/EventoList'));
const EventoDetail = lazy(() => import('./pages/EventoDetail'));
const CrearEvento = lazy(() => import('./pages/CrearEvento'));
const Login = lazy(() => import('./pages/Login'));
const Perfil = lazy(() => import('./pages/Perfil'));
const AdminDashboard = lazy(() => import('./pages/admin/Dashboard'));

function App() {
    return (
        <Suspense fallback={<Loading />}>
            <Routes>
                {/* Rutas públicas */}
                <Route element={<Layout />}>
                    <Route path="/" element={<Home />} />
                    <Route path="/eventos" element={<EventoList />} />
                    <Route path="/eventos/:id" element={<EventoDetail />} />
                </Route>
                
                {/* Rutas de autenticación */}
                <Route path="/login" element={<Login />} />
                
                {/* Rutas protegidas */}
                <Route element={<ProtectedRoute />}>
                    <Route element={<Layout />}>
                        <Route path="/eventos/nuevo" element={<CrearEvento />} />
                        <Route path="/perfil" element={<Perfil />} />
                    </Route>
                </Route>
                
                {/* Admin */}
                <Route 
                    path="/admin" 
                    element={
                        <ProtectedRoute rol="admin">
                            <AdminDashboard />
                        </ProtectedRoute>
                    } 
                />
                
                {/* 404 */}
                <Route path="*" element={<NotFound />} />
            </Routes>
        </Suspense>
    );
}
```

---

## 🛠️ Ejercicios

1. Configurar React Router con lazy loading
2. Crear rutas dinámicas /eventos/:id
3. Implementar rutas protegidas
4. Crear layouts anidados

---

## 📚 Recursos

- [React Router Docs](https://reactrouter.com/)
- [Routing](https://react.dev/learn/routing)
