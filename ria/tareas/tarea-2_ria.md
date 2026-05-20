# 📋 Tarea 2: Desarrollar aplicación RIA#

**Duración de la presentación:** 10-15 minutos por grupo  
**Objetivo:** Desarrollar una aplicación RIA

---

## 📧 Proceso de Inscripción#

Cada grupo debe seleccionar un sitio RIA a desarrollar y enviar un correo a **apastorini@gmail.com**

**Asunto:** Tarea 2 RIA 2026  
**Copia a:** todos los integrantes  
**Contenido:** Elegir una de los escenarios propuestos para implementar un sitio RIA utilziando angular, vue o react. .

---


**Criterio de evaluación:** Si el trabajo cumple con los requisitos de entrega, se aprueba la tarea. En caso contrario, el grupo tendrá la posibilidad de una nueva instancia en junio.

---

## 📂 Estructura Git Recomendada #

Todo el material generado debe almacenarse en un repositorio Git **público**. Se sugiere la siguiente estructura de carpetas:pdf     # Normativas descargadas
```



---

## Uso de Inteligencia Artificial #

Si el grupo decide utilizar herramientas de IA (Copilot, ChatGPT, Claude, Cursor, etc.), **debe cumplir con los siguientes requisitos**:

### 1. Registro de Prompts#
Todos los prompts utilizados deben almacenarse en la carpeta `prompts/` del repositorio.
- Formato sugerido: `01-descripcion.txt` o `01-descripcion.md`
- Deben incluir: fecha, herramienta utilizada y el texto exacto del prompt.

### 2. Memory Bank (Enfoque Sugerido)#
Para dar contexto a la IA y obtener mejores resultados, el grupo debe crear un archivo `prompts/00-memory-bank.md`. Este archivo le indica a la IA qué archivos son necesarios para entender el proyecto.

**Ejemplo de `00-memory-bank.md`:**
```markdown
# Memory Bank - Contexto para IA#

## Archivos de contexto necesarios:



### 3. Declaración de Herramientas#
En el `README.md` del repositorio, incluir una sección:
```markdown
## Herramientas de IA utilizadas#
- ChatGPT (GPT-4o) - Para generación de borrador de amenazas STRIDE
- Cursor - Asistencia en redacción de controles NIST
```

---

## 📋 Tarea 2: Desarrollo de Aplicaciones con APIs Públicas#

**Fecha de Presentación:** Lunes 1 de Junio  
**Modalidad:** Grupal #

---

## 🎯 Objetivo#

Desarrollar 1 aplicaciones que consuman APIs públicas externas, siguiendo el ciclo completo de desarrollo: diseño → desarrollo → tests → documentación → demo. Pueden elegir una de las siguientes opcioens de app.

**Restricciones Clave:**
- ❌ No backend complejo / lógica de negocio propia
- ❌ No bases de datos propias#
- ✅ Llamar APIs públicas gratuitas#
- ✅ Si hay problemas de CORS → usar herramientas de bypass (cors-anywhere, etc.)#
- ✅ Navegación de páginas obligatoria#
- ✅ Usar Vue 3, React o Angular (libertad del grupo)#
- ✅ Usar Bootstrap o Material Design#

---

## 📱 10 Escenarios / Aplicaciones Propuestas#

Cada grupo elige UNO y puede enriquecerlo con su propia impronta cumpliendo con las exigencias.

| # | Aplicación | API Pública Sugerida | Descripción Detallada |
|---|-------------------|-------------------|----------------|
| 1 | **Buscador de Películas** | [TMDB API](https://www.themoviedb.org/documentation/api) | **Búsqueda por título**, filtrar por género/año, ver detalles (sinopsis, reparto, rating), ver tráilers. Debe permitir navegar entre películas y ver ficha completa. Libre: 1000 requests/día |
| 2 | **Clima en Tiempo Real** | [OpenWeatherMap](https://openweathermap.org/api) | **Búsqueda por ciudad**, clima actual (temp, humedad, viento), pronóstico 5 días con iconos animados. Debe mostrar mapa de precipitaciones y permitir cambiar entre °C/°F. Libre: 1000 calls/día |
| 3 | **Buscador de Recetas** | [TheMealDB](https://www.themealdb.com/api.php) | **Búsqueda por ingrediente**, filtrar por categoría (vegana, postres) y área geográfica. Ver ingredientes, instrucciones paso a paso y video. Debe permitir guardar favoritos en localStorage. Libre |
| 4 | **Noticias por Categoría** | [NewsAPI](https://newsapi.org/) | **Headlines por país** (US, AR, UY, etc.), filtrar por tópico (tech, sports, health). Ver noticia completa, compartir enlace, buscar por palabra clave. Debe mostrar fecha y fuente. Libre: 100 calls/día |
| 5 | **Conversor de Monedas** | [ExchangeRate-API](https://www.exchangerate-api.com/) | **Conversión en tiempo real** entre +150 monedas. Historial de tasas (gráfico últimos 30 días), conversión múltiple simultánea. Debe validar inputs y mostrar símbolos de moneda. Libre: 1500 requests/mes |
| 6 | **Buscador de Libros** | [OpenLibrary](https://openlibrary.org/developers/api) | **Búsqueda por título/autor/ISBN**, ver detalles (sinopsis, páginas, editorial), ver reseñas y calificaciones. Debe permitir filtrar por año y guardar lecturas pendientes. Libre |
| 7 | **Pokédex Interactivo** | [PokeAPI](https://pokeapi.co/) | **Fichas completas de Pokémon**, buscar por nombre/número, filtrar por tipo (fuego, agua, etc.). Ver estadísticas, habilidades, cadena de evolución y sprites animados. Libre, sin límites |
| 8 | **Rastreador de Vuelos** | [AviationStack](https://aviationstack.com/) | **Búsqueda por número de vuelo**, ver estado en vivo (salida, llegada, retrasos), ruta en mapa. Filtrar por aerolínea y ver info de aeropuertos (terminal, puerta). Libre: 500 calls/mes |
| 9 | **Buscador de Usuarios GitHub** | [GitHub API](https://docs.github.com/en/rest) | **Buscar usuarios/devs**, ver perfil (avatar, bio, ubicación), listar repositorios con estrellas y forks. Ver actividad reciente (commits, PRs) y lenguajes usados. Libre: 60 calls/hora |
| 10 | **Dog Finder (Mascotas)** | [Dog CEO API](https://dog.ceo.org/) | **Búsqueda por raza**, ver fotos aleatorias de perros, filtrar por tamaño (pequeño, grande). Ver temperamento, esperanza de vida y peso. Debe permitir "me gusta" y galería personal. Libre |

---

## 🛠️ Ciclo de Desarrollo #

### Paso 1: Diseño de Mockups (Entregable al Docente)#
**Herramientas Gratuitas Sugeridas:**
- [Figma](https://www.figma.com/) (mejor opción, colaborativo)#
- [Excalidraw](https://excalidraw.com/) (simple, rápido)#
- [Penpot](https://penpot.app/) (open source)#
- [Draw.io](https://app.diagrams.net/) (para diagramas)#

**Lo que deben entregar:**
1. Mockup de la UI (móvil y desktop)#
2. Diagrama de componentes#
3. Flujo de navegación (user flow)#
4. Aplicación implementada

```
┌─────────────────────────────────┐
│         DIAGRAMA DE COMPONENTES (Ejemplo)            │
├─────────────────────────────────┤
│                                                 │
│   App                                          │
│   ├── Navbar                                   │
│   ├── HomePage                                 │
│   │   ├── SearchBar                            │
│   │   └── ResultsList                         │
│   │       └── ResultCard                       │
│   ├── DetailPage                               │
│   └── AboutPage                               │
│                                                 │
└─────────────────────────────────┘
```

### Paso 2: Configuración del Entorno#
```bash
# Para React#
npx create-react-app mi-app#
# o con Vite#
npm create vite@latest mi-app -- --template react#

# Para Vue 3#
npm create vue@latest mi-app#

# Para Angular#
ng new mi-app --routing --style=scss#
```

### Paso 3: Desarrollo con Navegación#
**Obligatorio:** Mínimo 3 páginas/rutas diferentes.

**Ejemplo (React Router):**
```jsx
<Routes>
  <Route path="/" element={<Home />} />
  <Route path="/detalle/:id" element={<Detalle />} />
  <Route path="/acerca" element={<Acerca />} />
</Routes>
```

**Ejemplo de llamada a API (con fallback):**
```javascript
// Si hay problemas de CORS#
const API_URL = 'https://cors-anywhere.herokuapp.com/https://api.ejemplo.com/data';#

// O usar proxy local#
const response = await fetch(API_URL);#
const data = await response.json();#
```

### Paso 4: Testing (Herramientas Gratuitas)#

#### Tests Unitarios:#
- **React:** Jest + React Testing Library#
- **Vue:** Vitest + Vue Test Utils#
- **Angular:** Jasmine + Karma (viene por defecto)#

```bash
# React/Vue#
npm install --save-dev jest @testing-library/react#

# Ejecutar#
npm test#
```

```javascript
// Ejemplo de test unitario#
test('renderiza resultados de búsqueda', () => {
  render(<SearchResults results={mockData} />);
  expect(screen.getByText('Película 1')).toBeInTheDocument();
});
```

#### Tests de Integración:#
```bash
# Cypress (gratuito)#
npm install cypress --save-dev#

# Playwright (gratuito, de Microsoft)#
npm init playwright@latest#
```

```javascript
// Ejemplo Cypress#
it('navega a detalle de película', () => {
  cy.visit('/');
  cy.get('[data-cy=search]').type('Avengers');
  cy.get('[data-cy=result-1]').click();
  cy.url().should('include', '/detalle/123');
});
```

#### Tests de Performance:#
- **Lighthouse** (Chrome DevTools - gratuito)#
- **WebPageTest** (https://www.webpagetest.org/)#

### Paso 5: Dockerización (Obligatorio)#

**Crear Dockerfile:**
```dockerfile
# Para React/Vue (producción)#
FROM node:18-alpine as build#
WORKDIR /app#
COPY package*.json ./#
RUN npm install#
COPY . .#
RUN npm run build#

FROM nginx:alpine#
COPY --from=build /app/dist /usr/share/nginx/html#
EXPOSE 80#
CMD ["nginx", "-g", "daemon off;"]#
```

**Crear docker-compose.yml:**
```yaml
version: '3.8'#
services:#
  web:#
    build: .#
    ports:#
      - "8080:80"#
    environment:#
      - NODE_ENV=production#
```

```bash
# Construir y ejecutar#
docker-compose up --build#

# Verificar contenedor#
docker ps#
```

### Paso 6: Subir a Git (Obligatorio)#
```bash
git init#
git add .#
git commit -m "Initial commit with mockups and structure"#
git branch -M main#
git remote add origin https://github.com/usuario/repo.git#
git push -u origin main#

# README.md obligatorio con:#
# - Descripción#
# - Cómo ejecutar#
# - APIs usadas#
# - Herramientas usadas#
# - Comandos Docker#
```

### Paso 7: Video Demo (30 segundos)#
**Herramientas:**
- OBS Studio (gratuito)#
- Zoom/Meet (grabar pantalla)#
- Peek (Linux)#
- Xbox Game Bar (Windows)#

**Qué mostrar:**
1. Navegación entre páginas#
2. Búsqueda funcionando#
3. Llamada a API funcionando#
4. Detalle de un elemento#

### Paso 8: Presentación PPT#
**Contenido mínimo:**
1. Portada (nombre app, integrantes)#
2. Mockups de UI#
3. Diagrama de componentes#
4. APIs usadas (con enlaces)#
5. Tests realizados (capturas)#
6. Enlaces: GitHub repo + Demo video#
7. Conclusiones#

---

## 🔄 Alternativas si la API Falla#

| API Principal | Alternativa 1 | Alternativa 2 |
|--------------|---------------|---------------|
| TMDB | [OMDb API](http://www.omdbapi.com/) | [Watchmode](https://www.watchmode.com/) |
| OpenWeather | [WeatherAPI](https://www.weatherapi.com/) | [AccuWeather](https://developer.accuweather.com/) |
| TheMealDB | [Spoonacular](https://spoonacular.com/food-api) | [Edamam](https://www.edamam.com/) |
| NewsAPI | [CurrentsAPI](https://currentsapi.services/) | [GNews](https://gnews.io/) |
| ExchangeRate | [Frankfurter](https://api.frankfurter.io/) | [CurrencyAPI](https://currencyapi.net/) |

**Nota:** Si una API no funciona → buscar alternativa y documentar en README.md.

---

## 📦 Entregables (Checklist)#

- [ ] **Mockups** (Figma/Excalidraw) → Entregar al docente primer monitoreo#
- [ ] **Código fuente** en GitHub con README.md completo#
- [ ] **Tests unitarios** pasando (captura de pantalla)#
- [ ] **Tests de integración** pasando (captura)#
- [ ] **Reporte de Performance** (Lighthouse score)#
- [ ] **Video de 30 segundos** (enlace en README)#
- [ ] **PPT de presentación** (7 diapositivas mínimo)#

---

## 📊 Criterios de Evaluación#

| Criterio | Puntaje |
|----------|---------|
| Mockups de UI (entrega inicial) | 15 pts |
| Navegación funcional (3+ rutas) | 20 pts |
| Consumo de API pública | 25 pts |
| Tests (unitarios + integración) | 20 pts |
| Performance (Lighthouse > 80) | 10 pts |
| Documentación (README + PPT) | 10 pts |
| **Total** | **100 pts** |

---

## 🚀 Comandos Rápidos para el Lab#

```bash
# 1. Crear proyecto (Vue 3 ejemplo)#
npm create vue@latest mi-app-lab2#
cd mi-app-lab2#
npm install#
npm run dev#

# 2. Instalar router#
npm install vue-router@4#

# 3. Instalar testing#
npm install --save-dev vitest @vue/test-utils#

# 4. Subir a GitHub#
git init#
git add .#
git commit -m "feat: initial setup with router"#
git branch -M main#
git remote add origin https://github.com/usuario/mi-app-lab2.git#
git push -u origin main#
```

---

## 🧪 Ejemplos de Pruebas con JMeter#

### Crear Test Plan (test-plan.jmx):#
```xml
<?xml version="1.0" encoding="UTF-8"?>
<jmeterTestPlan version="1.2" properties="5.0">
  <TestPlan guiclass="TestPlanGui" testname="API Test">
    <elementProp name="TestPlan.user_defined_variables">
      <Arguments>
        <Argument name="API_URL" value="https://api.ejemplo.com/data"/>
      </Arguments>
    </elementProp>
    <ThreadGroup guiclass="ThreadGroupGui" testname="Grupo de Hilos">
      <elementProp name="ThreadGroup.arguments">
        <Arguments>
          <Argument name="ThreadGroup.num_threads" value="10"/>
          <Argument name="ThreadGroup.ramp_time" value="5"/>
          <Argument name="ThreadGroup.duration" value="60"/>
        </Arguments>
      </elementProp>
    </ThreadGroup>
    <HTTPSamplerProxy guiclass="HttpTestSampleGui" testname="GET API">
      <elementProp name="HTTPSampler.arguments">
        <Arguments>
          <Argument name="API_URL" value="${API_URL}"/>
        </Arguments>
      </elementProp>
    </HTTPSamplerProxy>
  </TestPlan>
</jmeterTestPlan>
```

**Ejecutar JMeter:**
```bash
# GUI mode (para crear test plan)#
jmeter#

# Non-GUI mode (para ejecutar pruebas)#
jmeter -n -t test-plan.jmx -l results.jtl -e -o report#
```

---

## 🎨 Estructura del Proyecto (Sugerida)#

```
mi-grupo-lab2/
├── public/
│   └── index.html#
├── src/
│   ├── assets/
│   ├── components/
│   │   ├── Navbar.vue#
│   │   ├── SearchBar.vue#
│   │   └── ResultCard.vue#
│   ├── views/
│   │   ├── Home.vue#
│   │   ├── Detail.vue#
│   │   └── About.vue#
│   ├── router/
│   │   └── index.js#
│   ├── services/
│   │   └── api.js#
│   ├── App.vue#
│   └── main.js#
├── tests/
│   ├── unit/
│   │   └── SearchBar.spec.js#
│   └── integration/
│       └── navigation.spec.js#
├── docker/
│   ├── Dockerfile#
│   └── nginx.conf#
├── docker-compose.yml#
├── README.md#
├── package.json#
└── vite.config.js#
```

---

**¡Listo para presentar el lunes 1 de junio!** Imprenta o comparte la pantalla con este documento.
