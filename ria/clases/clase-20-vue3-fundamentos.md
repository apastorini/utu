# 💚 Clase 20: Vue 3 - Fundamentos

**Duración:** 4 horas  
**Objetivo:** Dominar Vue 3, Composition API y componentes básicos  
**Proyecto:** Sistema de eventos con Vue 3

---

## 📚 Contenido Teórico

### 1. Fundamentos de Vue 3

#### 1.1 Instalación y Setup

```bash
# Con Vite (recomendado)
npm create vue@latest mi-proyecto
cd mi-proyecto
npm install

# O con Vue CLI
npm install -g @vue/cli
vue create mi-proyecto
```

```bash
# Estructura del proyecto
mi-proyecto/
├── public/
├── src/
│   ├── assets/
│   ├── components/
│   ├── views/
│   ├── router/
│   ├── stores/
│   ├── App.vue
│   └── main.js
├── index.html
├── package.json
└── vite.config.js
```

#### 1.2 Vue 3 - Options API vs Composition API

**Options API (clásico):**
```vue
<!-- components/Saludo.vue -->
<template>
  <div class="saludo">
    <h1>Hola, {{ nombre }}!</h1>
    <p>Tienes {{ edad }} años</p>
    <button @click="incrementar">+</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      nombre: 'Juan',
      edad: 25
    }
  },
  methods: {
    incrementar() {
      this.edad++
    }
  },
  computed: {
    mensaje() {
      return `Hola ${this.nombre}, tienes ${this.edad} años`
    }
  }
}
</script>

<style scoped>
.saludo {
  text-align: center;
}
button {
  padding: 8px 16px;
  cursor: pointer;
}
</style>
```

**Composition API (moderno):**
```vue
<!-- components/Saludo.vue -->
<template>
  <div class="saludo">
    <h1>Hola, {{ nombre }}!</h1>
    <p>Tienes {{ edad }} años</p>
    <button @click="incrementar">+</button>
    <p>{{ mensaje }}</p>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const nombre = ref('Juan')
const edad = ref(25)

const incrementar = () => {
  edad.value++
}

const mensaje = computed(() => {
  return `Hola ${nombre.value}, tienes ${edad.value} años`
})
</script>

<style scoped>
.saludo {
  text-align: center;
}
button {
  padding: 8px 16px;
  cursor: pointer;
}
</style>
```

---

### 2. Reactividad con Composition API

#### 2.1 ref y reactive

```vue
<script setup>
import { ref, reactive } from 'vue'

// ref - para tipos primitivos y objetos
const count = ref(0)
const usuario = ref({ nombre: 'Juan', edad: 25 })

// Modificar valor
count.value++
usuario.value.nombre = 'Pedro'

// reactive - solo para objetos
const estado = reactive({
  cargando: false,
  error: null,
  datos: []
})

// Modificar (sin .value)
estado.cargando = true
</script>
```

#### 2.2 Computed y Watch

```vue
<script setup>
import { ref, computed, watch } from 'vue'

const precio = ref(100)
const descuento = ref(0)

// Computed - valor derivado
const precioFinal = computed(() => {
  return precio.value - (precio.value * descuento.value / 100)
})

// Watch - observar cambios
watch(precio, (nuevo, anterior) => {
  console.log(`Precio cambió de ${anterior} a ${nuevo}`)
})

// Watch con deep
const usuario = ref({ perfil: { edad: 25 } })
watch(usuario, (nuevo) => {
  console.log('Usuario cambió:', nuevo)
}, { deep: true })

// WatchEffect - se ejecuta inmediatamente
import { watchEffect } from 'vue'
watchEffect(() => {
  console.log('Precio:', precio.value)
})
</script>
```

#### 2.3 Lifecycle Hooks

```vue
<script setup>
import { 
  onMounted, 
  onUpdated, 
  onUnmounted,
  onBeforeMount,
  onBeforeUpdate,
  onBeforeUnmount
} from 'vue'

// Equivalentes a Options API
// beforeCreate/setup -> ya no necesario
// created/setup -> script setup se ejecuta en este momento

onBeforeMount(() => {
  console.log('Antes de montar')
})

onMounted(() => {
  console.log('Componente montado')
  // Ideal para fetch inicial
  fetchData()
})

onBeforeUpdate(() => {
  console.log('Antes de actualizar')
})

onUpdated(() => {
  console.log('Componente actualizado')
})

onBeforeUnmount(() => {
  console.log('Antes de desmontar')
  // Cleanup
})

onUnmounted(() => {
  console.log('Componente desmontado')
})
</script>
```

---

### 3. Templates en Vue

#### 3.1 Directivas Fundamentales

```vue
<template>
  <!-- v-if / v-else / v-else-if -->
  <div v-if="usuario.rol === 'admin'">
    Panel de Admin
  </div>
  <div v-else-if="usuario.rol === 'organizador'">
    Panel de Organizador
  </div>
  <div v-else>
    Panel de Usuario
  </div>
  
  <!-- v-show - alterna display:none -->
  <div v-show="mostrar">Visible</div>
  
  <!-- v-for con key -->
  <ul>
    <li 
      v-for="evento in eventos" 
      :key="evento.id"
    >
      {{ evento.titulo }}
    </li>
  </ul>
  
  <!-- v-for con índice -->
  <li v-for="(evento, index) in eventos" :key="index">
    {{ index + 1 }}. {{ evento.titulo }}
  </li>
  
  <!-- v-for con objeto -->
  <div v-for="(valor, clave) in objeto" :key="clave">
    {{ clave }}: {{ valor }}
  </div>
  
  <!-- v-bind : shorthand -->
  <img :src="imagen" :alt="titulo" :class="{ activo: esActivo }" />
  
  <!-- v-on @ shorthand -->
  <button @click="handleClick" @mouseenter="onHover">
    Click
  </button>
  
  <!-- v-model -->
  <input v-model="busqueda" />
  <textarea v-model="descripcion"></textarea>
  <select v-model="categoria">
    <option value="">Seleccionar</option>
  </select>
  <input type="checkbox" v-model="aceptado" />
  <input type="radio" v-model="opcion" value="a" />
  
  <!-- v-text y v-html -->
  <span v-text="mensaje"></span>
  <span v-html="htmlContent"></span>
</template>

<script setup>
import { ref } from 'vue'

const usuario = ref({ rol: 'usuario' })
const mostrar = ref(true)
const eventos = ref([
  { id: 1, titulo: 'Concierto' },
  { id: 2, titulo: 'Festival' }
])
const objeto = ref({ nombre: 'Juan', edad: 25 })
const imagen = ref('/img.jpg')
const titulo = ref('Imagen')
const esActivo = ref(true)
const busqueda = ref('')
const descripcion = ref('')
const categoria = ref('')
const aceptado = ref(false)
const opcion = ref('')
const mensaje = ref('Hola')
const htmlContent = ref('<strong>Negrita</strong>')

const handleClick = () => console.log('Click')
const onHover = () => console.log('Hover')
</script>
```

#### 3.2 Eventos y Métodos

```vue
<template>
  <!-- Eventos con modificadores -->
  <form @submit.prevent="enviarFormulario">
    <input @keyup.enter="buscar" />
    <button @click.stop="handleClick">Click (sin propagación)</button>
    <a href="#" @click.prevent>Link sin navegación</button>
  </form>
  
  <!-- Event object -->
  <button @click="handleEvent">Con evento</button>
  <button @click="(e) => handleCustom(e, 'data')">Con datos</button>
  
  <!-- Eventos personalizados -->
  <Hijo @mi-evento="handlePadre" />
</template>

<script setup>
const enviarFormulario = () => {
  console.log('Formulario enviado')
}

const buscar = () => {
  console.log('Buscando...')
}

const handleClick = (e) => {
  console.log('Click:', e)
}

const handleEvent = (e) => {
  console.log('Target:', e.target)
  console.log('Type:', e.type)
}

const handleCustom = (e, data) => {
  console.log('Data:', data)
}

const handlePadre = (dato) => {
  console.log('Evento del hijo:', dato)
}
</script>
```

---

### 4. Componentes en Vue 3

#### 4.1 Props y Emits

```vue
<!-- components/EventoCard.vue -->
<template>
  <article class="evento-card" @click="$emit('click', evento)">
    <img :src="imagen" :alt="evento.titulo" />
    <h3>{{ evento.titulo }}</h3>
    <p>{{ formatoFecha(evento.fecha) }}</p>
    <span>${{ evento.precio }}</span>
  </article>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  evento: {
    type: Object,
    required: true
  },
  variant: {
    type: String,
    default: 'default',
    validator: (v) => ['default', 'compact', 'featured'].includes(v)
  }
})

// Define emits
const emit = defineEmits(['click', 'eliminar'])

const imagen = computed(() => props.evento.imagen || '/placeholder.jpg')

const formatoFecha = (fecha) => {
  return new Date(fecha).toLocaleDateString('es-ES', {
    day: 'numeric',
    month: 'long'
  })
}
</script>

<style scoped>
.evento-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 16px;
  cursor: pointer;
  transition: transform 0.2s;
}
.evento-card:hover {
  transform: translateY(-4px);
}
</style>
```

**Usar componente:**
```vue
<template>
  <EventoCard 
    :evento="eventoData"
    variant="featured"
    @click="seleccionarEvento"
    @eliminar="confirmarEliminar"
  />
</template>

<script setup>
import { ref } from 'vue'
import EventoCard from './components/EventoCard.vue'

const eventoData = ref({
  id: 1,
  titulo: 'Concierto de Rock',
  fecha: '2024-03-15',
  precio: 50,
  imagen: '/rock.jpg'
})

const seleccionarEvento = (evento) => {
  console.log('Seleccionado:', evento)
}

const confirmarEliminar = () => {
  console.log('Eliminar')
}
</script>
```

#### 4.2 Slots

```vue
<!-- components/Modal.vue -->
<template>
  <Teleport to="body">
    <div v-if="abierto" class="modal-overlay" @click.self="$emit('close')">
      <div class="modal" :class="`modal--${size}`">
        <header class="modal-header">
          <h2>{{ titulo }}</h2>
          <button @click="$emit('close')">✕</button>
        </header>
        
        <div class="modal-body">
          <!-- Slot por defecto -->
          <slot />
        </div>
        
        <footer class="modal-footer">
          <!-- Slots con nombre -->
          <slot name="footer">
            <button @click="$emit('close')">Cerrar</button>
          </slot>
        </footer>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
defineProps({
  abierto: Boolean,
  titulo: String,
  size: {
    type: String,
    default: 'md'
  }
})

defineEmits(['close'])
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
}
.modal {
  background: white;
  border-radius: 8px;
  max-width: 90vw;
}
.modal--sm { width: 300px; }
.modal--md { width: 500px; }
.modal--lg { width: 800px; }
</style>
```

**Usar:**
```vue
<Modal :abierto="mostrarModal" titulo="Confirmar" @close="mostrarModal = false">
  <p>¿Estás seguro de continuar?</p>
  
  <template #footer>
    <button @click="confirmar">Confirmar</button>
    <button @click="mostrarModal = false">Cancelar</button>
  </template>
</Modal>
```

---

## 💻 Contenido Práctico

### 5. Estructura del Proyecto

```
src/
├── assets/
│   └── main.css
├── components/
│   ├── common/
│   │   ├── Button.vue
│   │   ├── Input.vue
│   │   ├── Modal.vue
│   │   └── Spinner.vue
│   ├── eventos/
│   │   ├── EventoCard.vue
│   │   ├── EventoList.vue
│   │   └── EventoForm.vue
│   └── layout/
│       ├── Header.vue
│       ├── Footer.vue
│       └── Layout.vue
├── views/
│   ├── Home.vue
│   ├── Eventos.vue
│   ├── EventoDetalle.vue
│   └── Login.vue
├── stores/
│   ├── eventos.js
│   └── usuario.js
├── router/
│   └── index.js
├── App.vue
└── main.js
```

### 6. Ejercicio Resuelto: Lista de Eventos

```vue
<!-- views/Eventos.vue -->
<template>
  <div class="eventos-page">
    <header class="header">
      <h1>Todos los Eventos</h1>
      <router-link to="/eventos/nuevo" class="btn btn-primary">
        Crear Evento
      </router-link>
    </header>
    
    <div class="filtros">
      <input
        v-model="filtroTexto"
        type="text"
        placeholder="Buscar eventos..."
        class="input-busqueda"
      />
      
      <select v-model="categoriaSeleccionada">
        <option value="todas">Todas las categorías</option>
        <option value="musica">Música</option>
        <option value="deportes">Deportes</option>
        <option value="tecnologia">Tecnología</option>
      </select>
    </div>
    
    <div v-if="cargando" class="loading">
      <Spinner />
    </div>
    
    <div v-else-if="error" class="error">
      {{ error }}
    </div>
    
    <div v-else class="eventos-grid">
      <EventoCard
        v-for="evento in eventosFiltrados"
        :key="evento.id"
        :evento="evento"
        @click="verDetalle(evento)"
      />
    </div>
    
    <p v-if="!cargando && eventosFiltrados.length === 0" class="no-resultados">
      No se encontraron eventos
    </p>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import EventoCard from '../components/eventos/EventoCard.vue'
import Spinner from '../components/common/Spinner.vue'

const router = useRouter()

const eventos = ref([])
const cargando = ref(true)
const error = ref(null)
const filtroTexto = ref('')
const categoriaSeleccionada = ref('todas')

const fetchEventos = async () => {
  try {
    cargando.value = true
    const response = await fetch('/api/eventos')
    if (!response.ok) throw new Error('Error al cargar')
    eventos.value = await response.json()
  } catch (err) {
    error.value = err.message
  } finally {
    cargando.value = false
  }
}

const eventosFiltrados = computed(() => {
  let resultado = [...eventos.value]
  
  if (filtroTexto.value) {
    const texto = filtroTexto.value.toLowerCase()
    resultado = resultado.filter(e => 
      e.titulo.toLowerCase().includes(texto)
    )
  }
  
  if (categoriaSeleccionada.value !== 'todas') {
    resultado = resultado.filter(e => 
      e.categoria === categoriaSeleccionada.value
    )
  }
  
  return resultado
})

const verDetalle = (evento) => {
  router.push(`/eventos/${evento.id}`)
}

onMounted(() => {
  fetchEventos()
})
</script>

<style scoped>
.eventos-page {
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
  gap: 10px;
  margin-bottom: 20px;
}

.input-busqueda {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.eventos-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

.loading, .error, .no-resultados {
  text-align: center;
  padding: 40px;
}
</style>
```

---

## 🛠️ Ejercicios Prácticos

### Ejercicio 1: Componente Contador
- Crear contador con opciones API y comparar

### Ejercicio 2: Formulario de Login
- v-model con validación básica
- Mostrar/ocultar contraseña

### Ejercicio 3: Componente con Slots
- Crear Card con header, body y footer opcionales

### Ejercicio 4: Lista Filtrable
- Array de objetos con filtros computados

---

## 🚀 Proyecto de la Clase

### Sistema de Eventos con Vue 3

```vue
<!-- App.vue -->
<template>
  <div id="app">
    <header class="app-header">
      <nav>
        <router-link to="/">Inicio</router-link>
        <router-link to="/eventos">Eventos</router-link>
        <router-link to="/login">Login</router-link>
      </nav>
    </header>
    
    <main class="app-main">
      <router-view />
    </main>
    
    <footer class="app-footer">
      <p>&copy; 2024 Mi App de Eventos</p>
    </footer>
  </div>
</template>

<script setup>
// Composition API
</script>

<style>
#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.app-header {
  background: #333;
  color: white;
  padding: 1rem;
}

.app-header nav {
  display: flex;
  gap: 1rem;
}

.app-header a {
  color: white;
  text-decoration: none;
}

.app-header a.router-link-active {
  font-weight: bold;
}

.app-main {
  flex: 1;
}

.app-footer {
  background: #f5f5f5;
  padding: 1rem;
  text-align: center;
}
</style>
```

```javascript
// main.js
import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'

// Importar vistas
import Home from './views/Home.vue'
import Eventos from './views/Eventos.vue'
import EventoDetalle from './views/EventoDetalle.vue'

// Configurar rutas
const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: Home },
    { path: '/eventos', component: Eventos },
    { path: '/eventos/:id', component: EventoDetalle }
  ]
})

// Crear y montar app
const app = createApp(App)
app.use(router)
app.mount('#app')
```

### Entregables

1. **Proyecto Vue 3** configurado con Vite
2. **Componentes** con Composition API
3. **Props y emits** entre componentes
4. **Slots** para contenido reutilizable
5. **Directivas** y eventos

---

## 📚 Recursos Adicionales

- [Vue 3 Docs](https://vuejs.org/)
- [Composition API](https://vuejs.org/api/composition-api.html)
- [Vue Router](https://router.vuejs.org/)
