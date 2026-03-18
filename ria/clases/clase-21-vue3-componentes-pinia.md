# 📦 Clase 21: Vue 3 - Componentes Avanzados y Pinia

**Duración:** 4 horas  
**Objetivo:** Dominar Pinia, composables, y componentes avanzados  
**Proyecto:** Sistema de eventos con estado global

---

## 📚 Contenido Teórico

### 1. Pinia - Gestión de Estado

#### 1.1 Instalación y Configuración

```bash
npm install pinia
```

```javascript
// main.js
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.mount('#app')
```

#### 1.2 Stores con Pinia

```javascript
// stores/eventos.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useEventoStore = defineStore('eventos', () => {
  // State
  const lista = ref([])
  const eventoActual = ref(null)
  const cargando = ref(false)
  const error = ref(null)
  const filtros = ref({
    categoria: 'todas',
    busqueda: ''
  })
  
  // Getters (computed)
  const eventosFiltrados = computed(() => {
    let resultado = [...lista.value]
    
    if (filtros.value.busqueda) {
      const texto = filtros.value.busqueda.toLowerCase()
      resultado = resultado.filter(e => 
        e.titulo.toLowerCase().includes(texto)
      )
    }
    
    if (filtros.value.categoria !== 'todas') {
      resultado = resultado.filter(e => 
        e.categoria === filtros.value.categoria
      )
    }
    
    return resultado
  })
  
  const totalEventos = computed(() => lista.value.length)
  
  // Actions
  async function fetchEventos() {
    try {
      cargando.value = true
      error.value = null
      
      const response = await fetch('/api/eventos')
      if (!response.ok) throw new Error('Error al cargar')
      
      lista.value = await response.json()
    } catch (err) {
      error.value = err.message
    } finally {
      cargando.value = false
    }
  }
  
  async function fetchEventoPorId(id) {
    try {
      cargando.value = true
      
      const response = await fetch(`/api/eventos/${id}`)
      if (!response.ok) throw new Error('No encontrado')
      
      eventoActual.value = await response.json()
    } catch (err) {
      error.value = err.message
    } finally {
      cargando.value = false
    }
  }
  
  async function crearEvento(datos) {
    try {
      cargando.value = true
      
      const response = await fetch('/api/eventos', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(datos)
      })
      
      if (!response.ok) throw new Error('Error al crear')
      
      const nuevo = await response.json()
      lista.value.push(nuevo)
      
      return nuevo
    } catch (err) {
      error.value = err.message
      return null
    } finally {
      cargando.value = false
    }
  }
  
  function setFiltros(nuevosFiltros) {
    filtros.value = { ...filtros.value, ...nuevosFiltros }
  }
  
  function clearEventoActual() {
    eventoActual.value = null
  }
  
  return {
    // State
    lista,
    eventoActual,
    cargando,
    error,
    filtros,
    // Getters
    eventosFiltrados,
    totalEventos,
    // Actions
    fetchEventos,
    fetchEventoPorId,
    crearEvento,
    setFiltros,
    clearEventoActual
  }
})
```

#### 1.3 Usar Store en Componentes

```vue
<script setup>
import { storeToRefs } from 'pinia'
import { useEventoStore } from '../stores/eventos'
import { onMounted } from 'vue'

const store = useEventoStore()

// Desestructurar reactivo - usar storeToRefs para state/getters
const { lista, eventoActual, cargando, error, eventosFiltrados } = storeToRefs(store)

// Actions se llaman directamente
const { fetchEventos, setFiltros } = store

// Lifecycle
onMounted(() => {
  fetchEventos()
})
</script>

<template>
  <div>
    <div v-if="cargando">Cargando...</div>
    <div v-else-if="error">{{ error }}</div>
    <div v-else>
      <div v-for="evento in eventosFiltrados" :key="evento.id">
        {{ evento.titulo }}
      </div>
    </div>
  </div>
</template>
```

---

### 2. Composables

#### 2.1 useLocalStorage

```javascript
// composables/useLocalStorage.js
import { ref, watch } from 'vue'

export function useLocalStorage(key, defaultValue) {
  // Obtener valor inicial
  const valorInicial = localStorage.getItem(key)
  const data = ref(
    valorInicial ? JSON.parse(valorInicial) : defaultValue
  )
  
  // Sincronizar con localStorage
  watch(data, (nuevoValor) => {
    localStorage.setItem(key, JSON.stringify(nuevoValor))
  }, { deep: true })
  
  return data
}
```

**Uso:**
```vue
<script setup>
import { useLocalStorage } from '../composables/useLocalStorage'

const tema = useLocalStorage('tema', 'claro')
const usuario = useLocalStorage('usuario', { nombre: '', email: '' })
</script>

<template>
  <select v-model="tema">
    <option value="claro">Claro</option>
    <option value="oscuro">Oscuro</option>
  </select>
</template>
```

#### 2.2 useFetch

```javascript
// composables/useFetch.js
import { ref } from 'vue'

export function useFetch(url, options = {}) {
  const datos = ref(null)
  const cargando = ref(true)
  const error = ref(null)
  
  async function fetchData() {
    try {
      cargando.value = true
      error.value = null
      
      const response = await fetch(url, options)
      if (!response.ok) throw new Error(`HTTP ${response.status}`)
      
      datos.value = await response.json()
    } catch (err) {
      error.value = err.message
    } finally {
      cargando.value = false
    }
  }
  
  // Ejecutar inmediatamente
  fetchData()
  
  // Retornar
  return {
    datos,
    cargando,
    error,
    refetch: fetchData
  }
}
```

**Uso:**
```vue
<script setup>
import { computed } from 'vue'
import { useFetch } from '../composables/useFetch'

const { datos, cargando, error, refetch } = useFetch('/api/eventos')
const eventos = computed(() => datos.value || [])
</script>

<template>
  <div v-if="cargando">Cargando...</div>
  <div v-else-if="error">{{ error }}</div>
  <div v-else>
    <div v-for="e in eventos" :key="e.id">{{ e.titulo }}</div>
  </div>
  <button @click="refetch">Actualizar</button>
</template>
```

#### 2.3 useDebounce

```javascript
// composables/useDebounce.js
import { ref, watch } from 'vue'

export function useDebounce(valor, delay = 500) {
  const valorDebounced = ref(valor)
  let timeout = null
  
  watch(valor, (nuevo) => {
    clearTimeout(timeout)
    timeout = setTimeout(() => {
      valorDebounced.value = nuevo
    }, delay)
  })
  
  return valorDebounced
}
```

#### 2.4 useAuth (Store como Composable)

```javascript
// stores/auth.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const usuario = ref(null)
  const token = ref(localStorage.getItem('token'))
  
  const isAuthenticated = computed(() => !!token.value)
  
  async function login(email, password) {
    const response = await fetch('/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    })
    
    if (!response.ok) return false
    
    const data = await response.json()
    token.value = data.token
    usuario.value = data.usuario
    
    localStorage.setItem('token', data.token)
    
    return true
  }
  
  function logout() {
    token.value = null
    usuario.value = null
    localStorage.removeItem('token')
  }
  
  return {
    usuario,
    token,
    isAuthenticated,
    login,
    logout
  }
})
```

---

### 3. Componentes Avanzados

#### 3.1 Provide/Inject

```vue
<!-- components/Parent.vue -->
<template>
  <div class="parent">
    <slot />
  </div>
</template>

<script setup>
import { provide, ref } from 'vue'

const theme = ref('claro')
const cambiarTema = (nuevo) => {
  theme.value = nuevo
}

// Provide para descendientes
provide('theme', theme)
provide('cambiarTema', cambiarTema)
</script>
```

```vue
<!-- components/Child.vue -->
<script setup>
import { inject } from 'vue'

const theme = inject('theme')
const cambiarTema = inject('cambiarTema')
</script>

<template>
  <div :class="`tema-${theme}`">
    <button @click="cambiarTema('oscuro')">Oscuro</button>
  </div>
</template>
```

#### 3.2 Dynamic Components

```vue
<template>
  <!-- component dinámico -->
  <component :is="componenteActual" />
  
  <!-- O con objeto -->
  <component :is="componentes[variante]" />
</template>

<script setup>
import { ref, computed } from 'vue'
import CardSimple from './CardSimple.vue'
import CardFeatured from './CardFeatured.vue'
import CardCompact from './CardCompact.vue'

const variante = ref('simple')

const componentes = {
  simple: CardSimple,
  featured: CardFeatured,
  compact: CardCompact
}

const componenteActual = computed(() => componentes[variante.value])
</script>
```

#### 3.3 Teleport

```vue
<template>
  <button @click="abrirModal">Abrir</button>
  
  <Teleport to="body">
    <div v-if="mostrar" class="modal-overlay">
      <div class="modal">
        <slot />
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { ref } from 'vue'

const mostrar = ref(false)

const abrirModal = () => {
  mostrar.value = true
}
</script>
```

---

### 4. Vue Router con Pinia

#### 4.1 Router con Guards

```javascript
// router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import Dashboard from '../views/Dashboard.vue'

const routes = [
  { path: '/', component: Home },
  { path: '/login', component: Login },
  { 
    path: '/dashboard', 
    component: Dashboard,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Guard global
router.beforeEach((to, from, next) => {
  const auth = useAuthStore()
  
  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    next({ path: '/login', query: { redirect: to.fullPath } })
  } else {
    next()
  }
})

export default router
```

#### 4.2 Rutas Anidadas

```javascript
// router/index.js
{
  path: '/admin',
  component: AdminLayout,
  meta: { requiresAuth: true, rol: 'admin' },
  children: [
    { path: '', component: AdminDashboard },
    { path: 'usuarios', component: AdminUsuarios },
    { path: 'eventos', component: AdminEventos }
  ]
}
```

```vue
<!-- views/AdminLayout.vue -->
<template>
  <div class="admin-layout">
    <aside>
      <nav>
        <router-link to="/admin">Dashboard</router-link>
        <router-link to="/admin/usuarios">Usuarios</router-link>
        <router-link to="/admin/eventos">Eventos</router-link>
      </nav>
    </aside>
    <main>
      <router-view />
    </main>
  </div>
</template>
```

---

## 💻 Contenido Práctico

### 5. Ejercicio Resuelto: Store de Eventos

```javascript
// stores/eventoStore.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useEventoStore = defineStore('eventos', () => {
  // State
  const eventos = ref([])
  const cargando = ref(false)
  const error = ref(null)
  
  const filtros = ref({
    texto: '',
    categoria: 'todas',
    ordenarPor: 'fecha'
  })
  
  // Getters
  const eventosFiltrados = computed(() => {
    let resultado = [...eventos.value]
    
    // Filtrar por texto
    if (filtros.value.texto) {
      const t = filtros.value.texto.toLowerCase()
      resultado = resultado.filter(e => 
        e.titulo.toLowerCase().includes(t) ||
        e.descripcion?.toLowerCase().includes(t)
      )
    }
    
    // Filtrar por categoría
    if (filtros.value.categoria !== 'todas') {
      resultado = resultado.filter(e => 
        e.categoria === filtros.value.categoria
      )
    }
    
    // Ordenar
    resultado.sort((a, b) => {
      switch (filtros.value.ordenarPor) {
        case 'fecha':
          return new Date(a.fecha) - new Date(b.fecha)
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
  
  const categorias = computed(() => {
    const cats = new Set(eventos.value.map(e => e.categoria))
    return ['todas', ...Array.from(cats)]
  })
  
  const total = computed(() => eventos.value.length)
  
  // Actions
  async function fetchEventos() {
    try {
      cargando.value = true
      error.value = null
      
      const res = await fetch('/api/eventos')
      if (!res.ok) throw new Error('Error al cargar')
      
      eventos.value = await res.json()
    } catch (e) {
      error.value = e.message
    } finally {
      cargando.value = false
    }
  }
  
  async function crearEvento(datos) {
    try {
      cargando.value = true
      
      const res = await fetch('/api/eventos', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(datos)
      })
      
      if (!res.ok) throw new Error('Error al crear')
      
      const nuevo = await res.json()
      eventos.value.push(nuevo)
      
      return nuevo
    } catch (e) {
      error.value = e.message
      return null
    } finally {
      cargando.value = false
    }
  }
  
  async function eliminarEvento(id) {
    try {
      const res = await fetch(`/api/eventos/${id}`, {
        method: 'DELETE'
      })
      
      if (!res.ok) throw new Error('Error al eliminar')
      
      eventos.value = eventos.value.filter(e => e.id !== id)
      
      return true
    } catch (e) {
      error.value = e.message
      return false
    }
  }
  
  function setFiltros(filtrosNuevos) {
    filtros.value = { ...filtros.value, ...filtrosNuevos }
  }
  
  function resetFiltros() {
    filtros.value = {
      texto: '',
      categoria: 'todas',
      ordenarPor: 'fecha'
    }
  }
  
  return {
    // State
    eventos,
    cargando,
    error,
    filtros,
    // Getters
    eventosFiltrados,
    categorias,
    total,
    // Actions
    fetchEventos,
    crearEvento,
    eliminarEvento,
    setFiltros,
    resetFiltros
  }
})
```

```vue
<!-- views/Eventos.vue -->
<template>
  <div class="eventos">
    <h1>Eventos</h1>
    
    <div class="filtros">
      <input
        v-model="filtros.texto"
        placeholder="Buscar..."
        @input="actualizarFiltros"
      />
      
      <select v-model="filtros.categoria" @change="actualizarFiltros">
        <option 
          v-for="cat in store.categorias" 
          :key="cat" 
          :value="cat"
        >
          {{ cat === 'todas' ? 'Todas' : cat }}
        </option>
      </select>
      
      <select v-model="filtros.ordenarPor" @change="actualizarFiltros">
        <option value="fecha">Fecha</option>
        <option value="precio">Precio</option>
        <option value="titulo">Título</option>
      </select>
    </div>
    
    <div v-if="store.cargando">Cargando...</div>
    <div v-else-if="store.error">{{ store.error }}</div>
    
    <div v-else class="grid">
      <div 
        v-for="evento in store.eventosFiltrados" 
        :key="evento.id"
        class="card"
      >
        <h3>{{ evento.titulo }}</h3>
        <p>{{ evento.fecha }}</p>
        <p>${{ evento.precio }}</p>
        <button @click="eliminar(evento.id)">Eliminar</button>
      </div>
    </div>
    
    <p v-if="!store.cargando && store.eventosFiltrados.length === 0">
      No hay eventos
    </p>
  </div>
</template>

<script setup>
import { reactive, onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { useEventoStore } from '../stores/eventoStore'

const store = useEventoStore()
const { filtros } = storeToRefs(store)

const actualizarFiltros = () => {
  store.setFiltros(filtros.value)
}

const eliminar = async (id) => {
  if (confirm('¿Eliminar?')) {
    await store.eliminarEvento(id)
  }
}

onMounted(() => {
  store.fetchEventos()
})
</script>
```

---

## 🛠️ Ejercicios Prácticos

### Ejercicio 1: Store de Carrito
- Agregar, quitar, calcular total

### Ejercicio 2: Composables usePagination
- Página actual, siguiente, anterior

### Ejercicio 3: Auth con Pinia
- Login, logout, persistencia

### Ejercicio 4: Router con Meta
- Rutas protegidas por rol

---

## 🚀 Proyecto de la Clase

### Sistema con Pinia y Composables

```javascript
// stores/index.js
import { createPinia } from 'pinia'

export const pinia = createPinia()

// Exportar stores
export * from './eventos'
export * from './auth'
export * from './carrito'
```

```javascript
// composables/index.js
export * from './useLocalStorage'
export * from './useFetch'
export * from './useDebounce'
export * from './useApi'
```

```vue
<!-- views/EventoDetalle.vue -->
<template>
  <div v-if="store.cargando">Cargando...</div>
  <div v-else-if="store.error">{{ store.error }}</div>
  <div v-else-if="evento">
    <h1>{{ evento.titulo }}</h1>
    <p>{{ evento.descripcion }}</p>
    <button @click="agregarAlCarrito(evento)">
      Agregar al Carrito
    </button>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useEventoStore } from '../stores/eventos'
import { useCarritoStore } from '../stores/carrito'

const route = useRoute()
const eventoStore = useEventoStore()
const carritoStore = useCarritoStore()

const evento = computed(() => eventoStore.eventoActual)

const agregarAlCarrito = (evt) => {
  carritoStore.agregar(evt)
}

onMounted(() => {
  eventoStore.fetchEventoPorId(route.params.id)
})
</script>
```

### Entregables

1. **Stores de Pinia** completos
2. **Composables** reutilizables
3. **Vue Router** con guards
4. **Provide/Inject** entre componentes

---

## 📚 Recursos Adicionales

- [Pinia Docs](https://pinia.vuejs.org/)
- [Vue Composables](https://vuejs.org/guide/reusability/composables.html)
- [Vue Router](https://router.vuejs.org/)
