# 📱 Clase 16: Accesibilidad, i18n, Deploy y Optimización

**Duración:** 4 horas  
**Objetivo:** Completar el sistema con accesibilidad, multiidioma, deployment y optimización  
**Proyecto:** Sistema de eventos listo para producción

---

## 📚 Contenido Teórico

### 1. Accesibilidad (WCAG 2.1)

#### 1.1 ¿Qué es WCAG?

Las Pautas de Accesibilidad para el Contenido Web (WCAG) definen cómo hacer el contenido web más accesible para personas con discapacidades.

**Principios WCAG:**

| Principio | Descripción |
|-----------|-------------|
| **Perceptible** | Información presentable de maneras que los usuarios puedan percibir |
| **Operable** | Componentes de interfaz usable |
| **Comprensible** | Información y operación comprensible |
| **Robusto** | Contenido suficiente para intérpretes diversos |

**Niveles de Conformidad:**
- **A** - Nivel básico
- **AA** - Nivel intermedio (requisito legal Uruguay)
- **AAA** - Nivel más alto

#### 1.2 Técnicas de Accesibilidad

```jsx
// Formularios accesibles
<form>
    <label htmlFor="email">Email:</label>
    <input
        id="email"
        name="email"
        type="email"
        aria-describedby="email-error"
        aria-invalid={error ? 'true' : 'false'}
        required
    />
    {error && (
        <span id="email-error" role="alert" className="error">
            {error}
        </span>
    )}
</form>

// Navegación por teclado
<button 
    onClick={handleAction}
    onKeyDown={(e) => e.key === 'Enter' && handleAction()}
>
    Acción
</button>

// Skip link
<a href="#main" className="skip-link">
    Saltar al contenido
</a>
```

---

### 2. Internacionalización (i18n)

#### 2.1 Conceptos

La **internacionalización (i18n)** es el proceso de diseñar software para que pueda adaptarse a diferentes idiomas y regiones sin cambios de código.

```
┌─────────────────────────────────────────────────────────────┐
│                    i18n vs l10n                             │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   i18n (internationalization):                              │
│   Preparar el código para soportar múltiples idiomas       │
│   - Extrar textos a archivos                                │
│   - Usar variables en lugar de strings hardcodeadas        │
│   - Formatear fechas/números según locale                  │
│                                                              │
│   l10n (localization):                                      │
│   Adaptar a un idioma/región específico                     │
│   - Traducir textos                                         │
│   - Ajustar formatos                                        │
│   - Contenido específico                                    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

#### 2.2 Implementación con i18next

```javascript
// i18n/index.js
import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import es from './locales/es.json';
import en from './locales/en.json';

i18n
    .use(initReactI18next)
    .init({
        resources: {
            es: { translation: es },
            en: { translation: en }
        },
        lng: localStorage.getItem('idioma') || 'es',
        fallbackLng: 'es',
        interpolation: { escapeValue: false }
    });

export default i18n;
```

---

### 3. Optimización de Performance

#### 3.1 Métricas Core Web Vitals

| Métrica | Objetivo | Descripción |
|---------|----------|-------------|
| **LCP** | < 2.5s | Largest Contentful Paint |
| **FID** | < 100ms | First Input Delay |
| **CLS** | < 0.1 | Cumulative Layout Shift |

#### 3.2 Técnicas de Optimización

```jsx
// Code splitting
const EventoDetail = lazy(() => import('./pages/EventoDetail'));

// Memoización
const EventoCardMemo = React.memo(function EventoCard({ evento }) {
    return <Card>{evento.titulo}</Card>;
});

// Optimización de imágenes
<img 
    src={imagen} 
    loading="lazy"
    srcSet={`${imagen} 1x, ${imagen2x} 2x`}
    alt={titulo}
/>
```

---

### 4. Deployment

```yaml
# GitHub Actions
name: Deploy

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: npm ci
      - run: npm test

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: docker-compose build

  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to server
        uses: appleboy/ssh-action@v0.1.0
        with:
          host: ${{ secrets.HOST }}
          script: |
            cd /opt/tufiesta
            docker-compose up -d
```

---

## 📚 Ejercicios

1. Agregar labels y roles ARIA
2. Implementar i18n con español/inglés
3. Optimizar con lazy loading
4. Configurar CI/CD

---

## 📚 Recursos

- [WCAG 2.1](https://www.w3.org/WAI/WCAG21/quickref/)
- [i18next](https://www.i18next.com/)
- [Web Vitals](https://web.dev/vitals/)
