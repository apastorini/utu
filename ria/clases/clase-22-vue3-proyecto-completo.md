# 🚀 Clase 22: Vue 3 - Proyecto Completo

**Duración:** 4 horas  
**Objetivo:** Construir sistema de eventos completo con Vue 3, TypeScript y Pinia  
**Proyecto:** App full-stack de eventos

---

## 📚 Contenido Teórico

### 1. Estructura del Proyecto Full

```
mi-proyecto/
├── public/
├── src/
│   ├── assets/
│   │   └── main.css
│   ├── components/
│   │   ├── common/
│   │   │   ├── AppButton.vue
│   │   │   ├── AppInput.vue
│   │   │   ├── AppModal.vue
│   │   │   └── AppSpinner.vue
│   │   ├── eventos/
│   │   │   ├── EventoCard.vue
│   │   │   ├── EventoList.vue
│   │   │   └── EventoForm.vue
│   │   └── layout/
│   │       ├── AppHeader.vue
│   │       └── AppFooter.vue
│   ├── composables/
│   │   ├── useApi.ts
│   │   ├── useAuth.ts
│   │   └── useLocalStorage.ts
│   ├── router/
│   │   └── index.ts
│   ├── stores/
│   │   ├── eventos.ts
│   │   ├── auth.ts
│   │   └── ui.ts
│   ├── types/
│   │   └── index.ts
│   ├── views/
│   │   ├── HomeView.vue
│   │   ├── EventosView.vue
│   │   ├── EventoDetalleView.vue
│   │   ├── LoginView.vue
│   │   └── AdminView.vue
│   ├── App.vue
│   └── main.ts
├── index.html
├── package.json
├── tsconfig.json
└── vite.config.ts
```

---

### 2. TypeScript en Vue 3

#### 2.1 Tipos Principales

```typescript
// types/index.ts
export interface Evento {
  id: number
  titulo: string
  descripcion: string
  fecha: string
  hora: string
  ubicacion: string
  precio: number
  categoria: Categoria
  imagen: string
  capacidad: number
  entradasDisponibles: number
  organizadorId: number
  creadoEn: string
  actualizadoEn: string
}

export type Categoria = 'musica' | 'deportes' | 'tecnologia' | 'arte' | 'otro'

export interface Usuario {
  id: number
  nombre: string
  email: string
  rol: 'usuario' | 'organizador' | 'admin'
  avatar?: string
}

export interface LoginData {
  email: string
  password: string
}

export interface RegisterData extends LoginData {
  nombre: string
}

export interface ApiResponse<T> {
  items: T[]
  total: number
  page: number
  limit: number
}
```

#### 2.2 Props Tipadas

```vue
<!-- components/eventos/EventoCard.vue -->
<template>
  <article 
    class="evento-card"
    @click="$emit('click', evento)"
  >
    <img :src="evento.imagen" :alt="evento.titulo" />
    <div class="content">
      <h3>{{ evento.titulo }}</h3>
      <p class="fecha">{{ formatFecha(evento.fecha) }}</p>
      <p class="precio">{{ precioFormateado }}</p>
    </div>
  </article>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { Evento } from '../../types'

interface Props {
  evento: Evento
  variant?: 'default' | 'compact' | 'featured'
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'default'
})

defineEmits<{
  click: [evento: Evento]
}>()

const formatFecha = (fecha: string): string => {
  return new Date(fecha).toLocaleDateString('es-ES', {
    day: 'numeric',
    month: 'long'
  })
}

const precioFormateado = computed(() => {
  return props.evento.precio === 0 
    ? 'Gratis' 
    : `$${props.evento.precio}`
})
</script>
```

---

### 3. Pinia con TypeScript

```typescript
// stores/eventos.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Evento, Categoria } from '../types'

interface Filtros {
  categoria: Categoria | 'todas'
  busqueda: string
  ordenarPor: 'fecha' | 'precio' | 'titulo'
}

export const useEventoStore = defineStore('eventos', () => {
  // State
  const eventos = ref<Evento[]>([])
  const eventoActual = ref<Evento | null>(null)
  const cargando = ref(false)
  const error = ref<string | null>(null)
  
  const filtros = ref<Filtros>({
    categoria: 'todas',
    busqueda: '',
    ordenarPor: 'fecha'
  })
  
  // Getters
  const eventosFiltrados = computed<Evento[]>(() => {
    let resultado = [...eventos.value]
    
    if (filtros.value.busqueda) {
      const texto = filtros.value.busqueda.toLowerCase()
      resultado = resultado.filter(e => 
        e.titulo.toLowerCase().includes(texto) ||
        e.descripcion?.toLowerCase().includes(texto)
      )
    }
    
    if (filtros.value.categoria !== 'todas') {
      resultado = resultado.filter(e => 
        e.categoria === filtros.value.categoria
      )
    }
    
    resultado.sort((a, b) => {
      switch (filtros.value.ordenarPor) {
        case 'fecha':
          return new Date(a.fecha).getTime() - new Date(b.fecha).getTime()
        case 'precio':
          return a.precio - b.precio
        case 'titulo':
          return a.titulo.localeCompare(b.titulo)
        default:
          return 0
      }
    })
    
    return resultado
  })
  
  const categorias = computed<string[]>(() => {
    const cats = new Set(eventos.value.map(e => e.categoria))
    return ['todas', ...Array.from(cats)]
  })
  
  // Actions
  async function fetchEventos(): Promise<void> {
    try {
      cargando.value = true
      error.value = null
      
      const response = await fetch('/api/eventos')
      if (!response.ok) throw new Error('Error al cargar')
      
      eventos.value = await response.json()
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Error desconocido'
    } finally {
      cargando.value = false
    }
  }
  
  async function fetchEventoPorId(id: number): Promise<Evento | null> {
    try {
      cargando.value = true
      error.value = null
      
      const response = await fetch(`/api/eventos/${id}`)
      if (!response.ok) throw new Error('No encontrado')
      
      eventoActual.value = await response.json()
      return eventoActual.value
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Error'
      return null
    } finally {
      cargando.value = false
    }
  }
  
  async function crearEvento(datos: Omit<Evento, 'id' | 'creadoEn' | 'actualizadoEn'>): Promise<Evento | null> {
    try {
      cargando.value = true
      
      const response = await fetch('/api/eventos', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(datos)
      })
      
      if (!response.ok) throw new Error('Error al crear')
      
      const nuevo: Evento = await response.json()
      eventos.value.push(nuevo)
      
      return nuevo
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Error'
      return null
    } finally {
      cargando.value = false
    }
  }
  
  function setFiltros(nuevos: Partial<Filtros>): void {
    filtros.value = { ...filtros.value, ...nuevos }
  }
  
  return {
    // State
    eventos,
    eventoActual,
    cargando,
    error,
    filtros,
    // Getters
    eventosFiltrados,
    categorias,
    // Actions
    fetchEventos,
    fetchEventoPorId,
    crearEvento,
    setFiltros
  }
})
```

---

### 4. Router con TypeScript

```typescript
// router/index.ts
import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import type { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'home',
    component: () => import('../views/HomeView.vue')
  },
  {
    path: '/eventos',
    name: 'eventos',
    component: () => import('../views/EventosView.vue')
  },
  {
    path: '/eventos/:id',
    name: 'evento-detalle',
    component: () => import('../views/EventoDetalleView.vue'),
    props: true
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('../views/LoginView.vue')
  },
  {
    path: '/admin',
    name: 'admin',
    component: () => import('../views/AdminView.vue'),
    meta: { requiresAuth: true, rol: 'admin' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ 
      name: 'login', 
      query: { redirect: to.fullPath } 
    })
  } else if (to.meta.rol && authStore.usuario?.rol !== to.meta.rol) {
    next({ name: 'home' })
  } else {
    next()
  }
})

export default router
```

---

## 💻 Contenido Práctico

### 5. Ejercicio Resuelto: Sistema Completo

```vue
<!-- views/EventosView.vue -->
<template>
  <div class="eventos-view">
    <header class="header">
      <h1>Todos los Eventos</h1>
      <router-link 
        v-if="authStore.isAuthenticated" 
        to="/eventos/nuevo"
        class="btn btn-primary"
      >
        Crear Evento
      </router-link>
    </header>
    
    <div class="filtros">
      <input
        v-model="filtros.busqueda"
        type="text"
        placeholder="Buscar eventos..."
        class="input-buscar"
      />
      
      <select v-model="filtros.categoria">
        <option 
          v-for="cat in store.categorias" 
          :key="cat" 
          :value="cat"
        >
          {{ cat === 'todas' ? 'Todas las categorías' : cat }}
        </option>
      </select>
      
      <select v-model="filtros.ordenarPor">
        <option value="fecha">Por Fecha</option>
        <option value="precio">Por Precio</option>
        <option value="titulo">Por Título</option>
      </select>
    </div>
    
    <AppSpinner v-if="store.cargando" />
    
    <div v-else-if="store.error" class="error">
      {{ store.error }}
    </div>
    
    <div v-else class="eventos-grid">
      <EventoCard
        v-for="evento in store.eventosFiltrados"
        :key="evento.id"
        :evento="evento"
        @click="verDetalle"
      />
    </div>
    
    <p 
      v-if="!store.cargando && store.eventosFiltrados.length === 0"
      class="no-resultados"
    >
      No se encontraron eventos
    </p>
  </div>
</template>

<script setup lang="ts">
import { reactive, watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'
import { useEventoStore } from '../stores/eventos'
import { useAuthStore } from '../stores/auth'
import EventoCard from '../components/eventos/EventoCard.vue'
import AppSpinner from '../components/common/AppSpinner.vue'
import type { Evento } from '../types'

const router = useRouter()
const store = useEventoStore()
const authStore = useAuthStore()

const { filtros } = storeToRefs(store)

const verDetalle = (evento: Evento) => {
  router.push(`/eventos/${evento.id}`)
}

// Sincronizar filtros con store
watch(filtros, (nuevos) => {
  store.setFiltros(nuevos)
}, { deep: true })

onMounted(() => {
  store.fetchEventos()
})
</script>

<style scoped>
.eventos-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.filtros {
  display: flex;
  gap: 12px;
  margin-bottom: 24px;
  flex-wrap: wrap;
}

.input-buscar {
  flex: 1;
  min-width: 200px;
  padding: 10px 14px;
  border: 1px solid #ddd;
  border-radius: 6px;
}

.eventos-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

.error, .no-resultados {
  text-align: center;
  padding: 40px;
  color: #666;
}
</style>
```

```vue
<!-- views/EventoDetalleView.vue -->
<template>
  <div class="detalle-view">
    <button @click="router.back()" class="btn-volver">
      ← Volver
    </button>
    
    <AppSpinner v-if="store.cargando" />
    
    <div v-else-if="store.error" class="error">
      {{ store.error }}
    </div>
    
    <article v-else-if="evento" class="evento-detalle">
      <div class="imagen">
        <img :src="evento.imagen" :alt="evento.titulo" />
      </div>
      
      <div class="contenido">
        <span class="categoria">{{ evento.categoria }}</span>
        <h1>{{ evento.titulo }}</h1>
        
        <div class="meta">
          <p>📅 {{ formatFecha(evento.fecha) }}</p>
          <p>🕐 {{ evento.hora }}</p>
          <p>📍 {{ evento.ubicacion }}</p>
        </div>
        
        <p class="descripcion">{{ evento.descripcion }}</p>
        
        <div class="precio">
          <span class="valor">{{ precio }}</span>
          <span class="disponibles">
            {{ evento.entradasDisponibles }} entradas disponibles
          </span>
        </div>
        
        <button 
          class="btn btn-primary btn-comprar"
          :disabled="evento.entradasDisponibles === 0"
          @click="comprar"
        >
          {{ evento.entradasDisponibles === 0 ? 'Agotado' : 'Comprar Entrada' }}
        </button>
      </div>
    </article>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useEventoStore } from '../stores/eventos'
import { useCarritoStore } from '../stores/carrito'
import AppSpinner from '../components/common/AppSpinner.vue'

const route = useRoute()
const router = useRouter()
const eventoStore = useEventoStore()
const carritoStore = useCarritoStore()

const evento = computed(() => eventoStore.eventoActual)

const formatFecha = (fecha: string): string => {
  return new Date(fecha).toLocaleDateString('es-ES', {
    weekday: 'long',
    day: 'numeric',
    month: 'long',
    year: 'numeric'
  })
}

const precio = computed(() => {
  if (!evento.value) return ''
  return evento.value.precio === 0 
    ? 'Gratis' 
    : `$${evento.value.precio}`
})

const comprar = () => {
  if (evento.value) {
    carritoStore.agregar(evento.value)
    router.push('/carrito')
  }
}

onMounted(async () => {
  const id = parseInt(route.params.id as string)
  await eventoStore.fetchEventoPorId(id)
})

onUnmounted(() => {
  eventoStore.eventoActual = null
})
</script>

<style scoped>
.detalle-view {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
}

.btn-volver {
  background: none;
  border: none;
  color: #666;
  cursor: pointer;
  padding: 8px 0;
  margin-bottom: 20px;
}

.evento-detalle {
  display: grid;
  gap: 24px;
}

@media (min-width: 768px) {
  .evento-detalle {
    grid-template-columns: 1fr 1fr;
  }
}

.imagen img {
  width: 100%;
  border-radius: 12px;
}

.categoria {
  text-transform: uppercase;
  font-size: 12px;
  color: #666;
  letter-spacing: 1px;
}

h1 {
  margin: 8px 0 16px;
}

.meta p {
  margin: 8px 0;
  color: #555;
}

.descripcion {
  margin: 20px 0;
  line-height: 1.6;
}

.precio {
  margin: 24px 0;
}

.precio .valor {
  font-size: 28px;
  font-weight: bold;
  display: block;
}

.precio .disponibles {
  color: #666;
}

.btn-comprar {
  width: 100%;
  padding: 14px;
  font-size: 16px;
}
</style>
```

---

### 6. Store de Carrito

```typescript
// stores/carrito.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Evento } from '../types'

export const useCarritoStore = defineStore('carrito', () => {
  const items = ref<Array<{ evento: Evento; cantidad: number }>>([])
  
  const total = computed(() => {
    return items.value.reduce((sum, item) => {
      return sum + (item.evento.precio * item.cantidad)
    }, 0)
  })
  
  const cantidadItems = computed(() => {
    return items.value.reduce((sum, item) => sum + item.cantidad, 0)
  })
  
  function agregar(evento: Evento): void {
    const existente = items.value.find(i => i.evento.id === evento.id)
    
    if (existente) {
      if (evento.entradasDisponibles > existente.cantidad) {
        existente.cantidad++
      }
    } else {
      items.value.push({ evento, cantidad: 1 })
    }
  }
  
  function quitar(eventoId: number): void {
    const index = items.value.findIndex(i => i.evento.id === eventoId)
    if (index !== -1) {
      items.value.splice(index, 1)
    }
  }
  
  function actualizarCantidad(eventoId: number, cantidad: number): void {
    const item = items.value.find(i => i.evento.id === eventoId)
    if (item && cantidad > 0) {
      item.cantidad = Math.min(cantidad, item.evento.entradasDisponibles)
    }
  }
  
  function vaciar(): void {
    items.value = []
  }
  
  return {
    items,
    total,
    cantidadItems,
    agregar,
    quitar,
    actualizarCantidad,
    vaciar
  }
})
```

---

## 🛠️ Ejercicios Prácticos

### Ejercicio 1: Formulario Tipado
- Tipos para form data
- Validación con TypeScript

### Ejercicio 2: Admin Dashboard
- CRUD completo de eventos

### Ejercicio 3: Sistema de Login
- Registro, login, logout

### Ejercicio 4: Carrito de Compras
- Agregar, quitar, total

---

## 🚀 Proyecto de la Clase

### App Completa con Vue 3 + TS

```typescript
// main.ts
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import './assets/main.css'

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')
```

```vue
<!-- App.vue -->
<template>
  <div id="app">
    <AppHeader />
    
    <main>
      <router-view />
    </main>
    
    <AppFooter />
    
    <Teleport to="body">
      <AppModal 
        :show="showModal" 
        @close="showModal = false"
      >
        <template #header>
          <h2>Modal</h2>
        </template>
        Contenido
      </AppModal>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import AppHeader from './components/layout/AppHeader.vue'
import AppFooter from './components/layout/AppFooter.vue'
import AppModal from './components/common/AppModal.vue'

const showModal = ref(false)
</script>
```

### Entregables

1. **Proyecto completo** con TypeScript
2. **Stores tipados** con Pinia
3. **Router** con guards
4. **Vistas completas** del sistema
5. **Carrito de compras** funcional

---

## 📚 Recursos Adicionales

- [Vue 3 + TypeScript](https://vuejs.org/guide/typescript/overview.html)
- [Pinia + TypeScript](https://pinia.vuejs.org/cookbook/options-api.html)
- [Vue Router + TypeScript](https://router.vuejs.org/guide/advanced/meta.html)
