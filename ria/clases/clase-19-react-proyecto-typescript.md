# 🔷 Clase 19: React con TypeScript - Proyecto Completo

**Duración:** 4 horas  
**Objetivo:** Construir sistema de eventos completo con TypeScript  
**Proyecto:** App full-stack con TypeScript

---

## 📚 Contenido Teórico

### 1. TypeScript en React

#### 1.1 Configuración de Proyecto

```bash
npm create vite@latest mi-proyecto -- --template react-ts
cd mi-proyecto
npm install
```

```json
// tsconfig.json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"]
    }
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

#### 1.2 Tipos Básicos

```tsx
// types/evento.ts
export interface Evento {
    id: number;
    titulo: string;
    descripcion: string;
    fecha: string;
    hora: string;
    ubicacion: string;
    precio: number;
    categoria: Categoria;
    imagen: string;
    capacidad: number;
    entradasDisponibles: number;
    organizador: Usuario;
    creadoEn: string;
    actualizadoEn: string;
}

export type Categoria = 'musica' | 'deportes' | 'tecnologia' | 'arte' | 'otro';

export interface Usuario {
    id: number;
    nombre: string;
    email: string;
    rol: 'usuario' | 'organizador' | 'admin';
    avatar?: string;
}

export interface Entrada {
    id: number;
    eventoId: number;
    usuarioId: number;
    cantidad: number;
    precioTotal: string;
    estado: 'pendiente' | 'confirmada' | 'cancelada';
    purchasedAt: string;
}
```

#### 1.3 Props con TypeScript

```tsx
// types/props.ts
import { Evento, Usuario } from './evento';

export interface EventoCardProps {
    evento: Evento;
    onClick?: (evento: Evento) => void;
    variant?: 'default' | 'compact' | 'featured';
    className?: string;
}

export interface EventoListProps {
    eventos: Evento[];
    cargando?: boolean;
    error?: string | null;
    onEventoClick?: (evento: Evento) => void;
    EmptyComponent?: React.ComponentType;
}

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
    variant?: 'primary' | 'secondary' | 'danger' | 'ghost';
    size?: 'sm' | 'md' | 'lg';
    isLoading?: boolean;
    leftIcon?: React.ReactNode;
    rightIcon?: React.ReactNode;
}

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
    label?: string;
    error?: string;
    helperText?: string;
    leftElement?: React.ReactNode;
    rightElement?: React.ReactNode;
}

export interface ModalProps {
    isOpen: boolean;
    onClose: () => void;
    title?: string;
    children: React.ReactNode;
    size?: 'sm' | 'md' | 'lg' | 'xl';
}
```

---

### 2. Componentes Tipados

#### 2.1 Componente EventoCard

```tsx
// components/EventoCard/EventoCard.tsx
import { Evento, EventoCardProps } from '../../types/props';
import './EventoCard.css';

export default function EventoCard({ 
    evento, 
    onClick, 
    variant = 'default',
    className = '' 
}: EventoCardProps) {
    
    const formatFecha = (fecha: string): string => {
        return new Date(fecha).toLocaleDateString('es-ES', {
            weekday: 'long',
            day: 'numeric',
            month: 'long',
            year: 'numeric'
        });
    };
    
    const handleClick = () => {
        onClick?.(evento);
    };
    
    return (
        <article 
            className={`evento-card evento-card--${variant} ${className}`}
            onClick={handleClick}
            role="article"
            tabIndex={0}
            onKeyDown={(e) => e.key === 'Enter' && handleClick()}
        >
            <div className="evento-card__imagen">
                <img 
                    src={evento.imagen || '/placeholder.jpg'} 
                    alt={evento.titulo}
                    loading="lazy"
                />
                <span className="evento-card__categoria">
                    {evento.categoria}
                </span>
            </div>
            
            <div className="evento-card__contenido">
                <h3 className="evento-card__titulo">
                    {evento.titulo}
                </h3>
                
                <div className="evento-card__meta">
                    <span className="evento-card__fecha">
                        📅 {formatFecha(evento.fecha)}
                    </span>
                    <span className="evento-card__ubicacion">
                        📍 {evento.ubicacion}
                    </span>
                </div>
                
                <div className="evento-card__footer">
                    <span className="evento-card__precio">
                        {evento.precio === 0 
                            ? 'Gratis' 
                            : `$${evento.precio}`
                        }
                    </span>
                    <span className="evento-card__disponibles">
                        {evento.entradasDisponibles} disponibles
                    </span>
                </div>
            </div>
        </article>
    );
}
```

#### 2.2 Hooks Tipados

```tsx
// hooks/useEventos.ts
import { useState, useEffect, useCallback } from 'react';
import { Evento } from '../types/evento';
import { ApiResponse } from '../types/api';

interface UseEventosOptions {
    categoria?: string;
    search?: string;
    page?: number;
    limit?: number;
}

interface UseEventosReturn {
    eventos: Evento[];
    cargando: boolean;
    error: string | null;
    total: number;
    pagina: number;
    totalPaginas: number;
    refetch: () => void;
}

export function useEventos(options: UseEventosOptions = {}): UseEventosReturn {
    const { categoria, search, page = 1, limit = 10 } = options;
    
    const [eventos, setEventos] = useState<Evento[]>([]);
    const [cargando, setCargando] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [total, setTotal] = useState(0);
    const [pagina, setPagina] = useState(page);
    
    const fetchEventos = useCallback(async () => {
        try {
            setCargando(true);
            setError(null);
            
            const params = new URLSearchParams();
            if (categoria && categoria !== 'todas') params.set('categoria', categoria);
            if (search) params.set('q', search);
            params.set('page', page.toString());
            params.set('limit', limit.toString());
            
            const response = await fetch(`/api/eventos?${params}`);
            
            if (!response.ok) {
                throw new Error('Error al cargar eventos');
            }
            
            const data: ApiResponse<Evento[]> = await response.json();
            
            setEventos(data.items);
            setTotal(data.total);
            setPagina(data.page);
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Error desconocido');
        } finally {
            setCargando(false);
        }
    }, [categoria, search, page, limit]);
    
    useEffect(() => {
        fetchEventos();
    }, [fetchEventos]);
    
    return {
        eventos,
        cargando,
        error,
        total,
        pagina,
        totalPaginas: Math.ceil(total / limit),
        refetch: fetchEventos
    };
}

// hooks/useForm.ts
import { useState, useCallback } from 'react';

interface FormState<T> {
    values: T;
    errors: Partial<Record<keyof T, string>>;
    touched: Partial<Record<keyof T, boolean>>;
    isSubmitting: boolean;
}

interface UseFormOptions<T> {
    initialValues: T;
    validate: (values: T) => Partial<Record<keyof T, string>>;
    onSubmit: (values: T) => Promise<void>;
}

export function useForm<T extends Record<string, unknown>>({
    initialValues,
    validate,
    onSubmit
}: UseFormOptions<T>) {
    const [state, setState] = useState<FormState<T>>({
        values: initialValues,
        errors: {},
        touched: {},
        isSubmitting: false
    });
    
    const handleChange = useCallback((
        field: keyof T,
        value: unknown
    ) => {
        setState(prev => ({
            ...prev,
            values: { ...prev.values, [field]: value }
        }));
    }, []);
    
    const handleBlur = useCallback((field: keyof T) => {
        setState(prev => ({
            ...prev,
            touched: { ...prev.touched, [field]: true }
        }));
    }, []);
    
    const handleSubmit = useCallback(async (e: React.FormEvent) => {
        e.preventDefault();
        
        const errors = validate(state.values);
        
        setState(prev => ({
            ...prev,
            errors,
            touched: Object.keys(state.values).reduce(
                (acc, key) => ({ ...acc, [key]: true }),
                {}
            ) as Partial<Record<keyof T, boolean>>
        }));
        
        if (Object.keys(errors).length > 0) {
            return;
        }
        
        setState(prev => ({ ...prev, isSubmitting: true }));
        
        try {
            await onSubmit(state.values);
        } finally {
            setState(prev => ({ ...prev, isSubmitting: false }));
        }
    }, [state.values, validate, onSubmit]);
    
    const reset = useCallback(() => {
        setState({
            values: initialValues,
            errors: {},
            touched: {},
            isSubmitting: false
        });
    }, [initialValues]);
    
    return {
        values: state.values,
        errors: state.errors,
        touched: state.touched,
        isSubmitting: state.isSubmitting,
        handleChange,
        handleBlur,
        handleSubmit,
        reset,
        setValues: (values: T) => setState(prev => ({ ...prev, values }))
    };
}
```

---

### 3. Context Tipado

```tsx
// context/AuthContext.tsx
import { createContext, useContext, useState, useCallback, ReactNode } from 'react';
import { Usuario } from '../types/evento';

interface AuthState {
    usuario: Usuario | null;
    token: string | null;
    isAuthenticated: boolean;
}

interface AuthContextValue extends AuthState {
    login: (email: string, password: string) => Promise<boolean>;
    logout: () => void;
    register: (data: RegisterData) => Promise<boolean>;
}

interface RegisterData {
    nombre: string;
    email: string;
    password: string;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
    const [state, setState] = useState<AuthState>(() => {
        const token = localStorage.getItem('token');
        const usuario = localStorage.getItem('usuario');
        
        return {
            token,
            usuario: usuario ? JSON.parse(usuario) : null,
            isAuthenticated: !!token
        };
    });
    
    const login = useCallback(async (email: string, password: string) => {
        try {
            const response = await fetch('/api/auth/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password })
            });
            
            if (!response.ok) return false;
            
            const data = await response.json();
            
            localStorage.setItem('token', data.token);
            localStorage.setItem('usuario', JSON.stringify(data.usuario));
            
            setState({
                token: data.token,
                usuario: data.usuario,
                isAuthenticated: true
            });
            
            return true;
        } catch {
            return false;
        }
    }, []);
    
    const logout = useCallback(() => {
        localStorage.removeItem('token');
        localStorage.removeItem('usuario');
        
        setState({
            token: null,
            usuario: null,
            isAuthenticated: false
        });
    }, []);
    
    const register = useCallback(async (data: RegisterData) => {
        try {
            const response = await fetch('/api/auth/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            
            return response.ok;
        } catch {
            return false;
        }
    }, []);
    
    return (
        <AuthContext.Provider value={{
            ...state,
            login,
            logout,
            register
        }}>
            {children}
        </AuthContext.Provider>
    );
}

export function useAuth(): AuthContextValue {
    const context = useContext(AuthContext);
    
    if (!context) {
        throw new Error('useAuth debe usarse dentro de AuthProvider');
    }
    
    return context;
}
```

---

### 4. Redux Toolkit con TypeScript

```tsx
// store/slices/eventoSlice.ts
import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { Evento } from '../../types/evento';

interface EventoState {
    lista: Evento[];
    eventoActual: Evento | null;
    cargando: boolean;
    error: string | null;
    filtros: {
        categoria: string;
        busqueda: string;
        pagina: number;
    };
}

const initialState: EventoState = {
    lista: [],
    eventoActual: null,
    cargando: false,
    error: null,
    filtros: {
        categoria: 'todas',
        busqueda: '',
        pagina: 1
    }
};

export const fetchEventos = createAsyncThunk(
    'eventos/fetchEventos',
    async (filtros: { categoria?: string; busqueda?: string; pagina?: number }) => {
        const params = new URLSearchParams();
        if (filtros.categoria && filtros.categoria !== 'todas') {
            params.set('categoria', filtros.categoria);
        }
        if (filtros.busqueda) {
            params.set('q', filtros.busqueda);
        }
        params.set('page', (filtros.pagina || 1).toString());
        
        const response = await fetch(`/api/eventos?${params}`);
        
        if (!response.ok) {
            throw new Error('Error al cargar eventos');
        }
        
        return response.json();
    }
);

export const fetchEventoPorId = createAsyncThunk(
    'eventos/fetchEventoPorId',
    async (id: number) => {
        const response = await fetch(`/api/eventos/${id}`);
        
        if (!response.ok) {
            throw new Error('Evento no encontrado');
        }
        
        return response.json();
    }
);

const eventoSlice = createSlice({
    name: 'eventos',
    initialState,
    reducers: {
        setFiltros: (state, action: PayloadAction<Partial<EventoState['filtros']>>) => {
            state.filtros = { ...state.filtros, ...action.payload };
        },
        setEventoActual: (state, action: PayloadAction<Evento | null>) => {
            state.eventoActual = action.payload;
        },
        clearError: (state) => {
            state.error = null;
        }
    },
    extraReducers: (builder) => {
        builder
            .addCase(fetchEventos.pending, (state) => {
                state.cargando = true;
                state.error = null;
            })
            .addCase(fetchEventos.fulfilled, (state, action) => {
                state.cargando = false;
                state.lista = action.payload.items;
            })
            .addCase(fetchEventos.rejected, (state, action) => {
                state.cargando = false;
                state.error = action.error.message || 'Error';
            })
            .addCase(fetchEventoPorId.fulfilled, (state, action) => {
                state.eventoActual = action.payload;
            });
    }
});

export const { setFiltros, setEventoActual, clearError } = eventoSlice.actions;
export default eventoSlice.reducer;
```

---

## 💻 Contenido Práctico

### 5. Ejercicio Resuelto: Formulario Tipado

```tsx
// types/forms.ts
export interface EventoFormData {
    titulo: string;
    descripcion: string;
    fecha: string;
    hora: string;
    ubicacion: string;
    precio: number;
    categoria: string;
    capacidad: number;
    imagen: string;
}

export interface LoginFormData {
    email: string;
    password: string;
}

export interface RegisterFormData {
    nombre: string;
    email: string;
    password: string;
    confirmPassword: string;
}

// validation.ts
import { EventoFormData, LoginFormData, RegisterFormData } from '../types/forms';

export const validateEvento = (values: EventoFormData) => {
    const errors: Partial<Record<keyof EventoFormData, string>> = {};
    
    if (!values.titulo.trim()) {
        errors.titulo = 'El título es requerido';
    } else if (values.titulo.length < 5) {
        errors.titulo = 'El título debe tener al menos 5 caracteres';
    }
    
    if (!values.descripcion.trim()) {
        errors.descripcion = 'La descripción es requerida';
    } else if (values.descripcion.length < 20) {
        errors.descripcion = 'La descripción debe tener al menos 20 caracteres';
    }
    
    if (!values.fecha) {
        errors.fecha = 'La fecha es requerida';
    } else if (new Date(values.fecha) < new Date()) {
        errors.fecha = 'La fecha debe ser futura';
    }
    
    if (!values.ubicacion.trim()) {
        errors.ubicacion = 'La ubicación es requerida';
    }
    
    if (values.precio < 0) {
        errors.precio = 'El precio no puede ser negativo';
    }
    
    if (values.capacidad < 1) {
        errors.capacidad = 'La capacidad mínima es 1';
    }
    
    return errors;
};

export const validateLogin = (values: LoginFormData) => {
    const errors: Partial<Record<keyof LoginFormData, string>> = {};
    
    if (!values.email) {
        errors.email = 'El email es requerido';
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(values.email)) {
        errors.email = 'Email inválido';
    }
    
    if (!values.password) {
        errors.password = 'La contraseña es requerida';
    } else if (values.password.length < 6) {
        errors.password = 'Mínimo 6 caracteres';
    }
    
    return errors;
};
```

```tsx
// pages/EventoForm/EventoForm.tsx
import { useForm } from '../../hooks/useForm';
import { EventoFormData, validateEvento } from '../../types/forms';
import Input from '../../components/Input';
import Button from '../../components/Button';
import './EventoForm.css';

const initialValues: EventoFormData = {
    titulo: '',
    descripcion: '',
    fecha: '',
    hora: '',
    ubicacion: '',
    precio: 0,
    categoria: '',
    capacidad: 100,
    imagen: ''
};

export default function EventoForm() {
    const {
        values,
        errors,
        touched,
        isSubmitting,
        handleChange,
        handleBlur,
        handleSubmit
    } = useForm<EventoFormData>({
        initialValues,
        validate: validateEvento,
        onSubmit: async (data) => {
            const response = await fetch('/api/eventos', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            
            if (!response.ok) {
                throw new Error('Error al crear evento');
            }
            
            // Redirigir o mostrar éxito
        }
    });
    
    return (
        <form onSubmit={handleSubmit} className="evento-form">
            <Input
                name="titulo"
                label="Título"
                value={values.titulo}
                onChange={(e) => handleChange('titulo', e.target.value)}
                onBlur={() => handleBlur('titulo')}
                error={touched.titulo ? errors.titulo : undefined}
                required
            />
            
            <div className="form-group">
                <label>Descripción</label>
                <textarea
                    name="descripcion"
                    value={values.descripcion}
                    onChange={(e) => handleChange('descripcion', e.target.value)}
                    onBlur={() => handleBlur('descripcion')}
                    rows={4}
                />
                {touched.descripcion && errors.descripcion && (
                    <span className="error">{errors.descripcion}</span>
                )}
            </div>
            
            <div className="form-row">
                <Input
                    name="fecha"
                    type="date"
                    label="Fecha"
                    value={values.fecha}
                    onChange={(e) => handleChange('fecha', e.target.value)}
                    onBlur={() => handleBlur('fecha')}
                    error={touched.fecha ? errors.fecha : undefined}
                    required
                />
                
                <Input
                    name="hora"
                    type="time"
                    label="Hora"
                    value={values.hora}
                    onChange={(e) => handleChange('hora', e.target.value)}
                    onBlur={() => handleBlur('hora')}
                    required
                />
            </div>
            
            <Input
                name="ubicacion"
                label="Ubicación"
                value={values.ubicacion}
                onChange={(e) => handleChange('ubicacion', e.target.value)}
                onBlur={() => handleBlur('ubicacion')}
                error={touched.ubicacion ? errors.ubicacion : undefined}
                required
            />
            
            <div className="form-row">
                <Input
                    name="precio"
                    type="number"
                    label="Precio"
                    value={values.precio}
                    onChange={(e) => handleChange('precio', Number(e.target.value))}
                    error={touched.precio ? errors.precio : undefined}
                    min={0}
                />
                
                <Input
                    name="capacidad"
                    type="number"
                    label="Capacidad"
                    value={values.capacidad}
                    onChange={(e) => handleChange('capacidad', Number(e.target.value))}
                    error={touched.capacidad ? errors.capacidad : undefined}
                    min={1}
                />
            </div>
            
            <div className="form-group">
                <label>Categoría</label>
                <select
                    name="categoria"
                    value={values.categoria}
                    onChange={(e) => handleChange('categoria', e.target.value)}
                >
                    <option value="">Seleccionar...</option>
                    <option value="musica">Música</option>
                    <option value="deportes">Deportes</option>
                    <option value="tecnologia">Tecnología</option>
                </select>
            </div>
            
            <Button type="submit" isLoading={isSubmitting}>
                Crear Evento
            </Button>
        </form>
    );
}
```

---

## 🛠️ Ejercicios Prácticos

### Ejercicio 1: Tipar Componente Modal
- Crear Modal con tipos props正确

### Ejercicio 2: Tipar Custom Hook useDebounce
- Generics para el tipo de valor

### Ejercicio 3: Tipar slice de Redux
- Estado, acciones y selectors con TypeScript

### Ejercicio 4: Formulario de Registro
- Validación completa con tipos

---

## 🚀 Proyecto de la Clase

### Sistema de Eventos Completo con TypeScript

```tsx
// main.tsx
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { Provider } from 'react-redux';
import { BrowserRouter } from 'react-router-dom';
import { store } from './store';
import App from './App';
import './index.css';

createRoot(document.getElementById('root')!).render(
    <StrictMode>
        <Provider store={store}>
            <BrowserRouter>
                <App />
            </BrowserRouter>
        </Provider>
    </StrictMode>
);
```

```tsx
// App.tsx
import { Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from './context/AuthContext';
import Layout from './components/Layout';
import Home from './pages/Home';
import Eventos from './pages/Eventos';
import EventoDetalle from './pages/EventoDetalle';
import EventoForm from './pages/EventoForm';
import Login from './pages/Login';
import Perfil from './pages/Perfil';
import AdminDashboard from './pages/admin/Dashboard';
import NotFound from './pages/NotFound';

function ProtectedRoute({ children, roles }: { children: React.ReactNode; roles?: string[] }) {
    const { isAuthenticated, usuario } = useAuth();
    
    if (!isAuthenticated) {
        return <Navigate to="/login" replace />;
    }
    
    if (roles && usuario && !roles.includes(usuario.rol)) {
        return <Navigate to="/" replace />;
    }
    
    return <>{children}</>;
}

export default function App() {
    return (
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
                
                <Route path="perfil" element={
                    <ProtectedRoute>
                        <Perfil />
                    </ProtectedRoute>
                } />
                
                <Route path="admin" element={
                    <ProtectedRoute roles={['admin']}>
                        <AdminDashboard />
                    </ProtectedRoute>
                } />
            </Route>
            
            <Route path="*" element={<NotFound />} />
        </Routes>
    );
}
```

### Entregables

1. **Proyecto configurado** con TypeScript y Vite
2. **Tipos completos** para modelos, props y forms
3. **Hooks tipados** con Generics
4. **Context con tipos** estrictos
5. **Redux con TypeScript** completo

---

## 📚 Recursos Adicionales

- [TypeScript React Handbook](https://react.dev/learn/typescript)
- [Redux Toolkit TypeScript Guide](https://redux-toolkit.js.org/usage/usage-with-typescript)
- [Vite with TypeScript](https://vitejs.dev/guide/#type-support)
