# 📱 Clase 14: Proyecto - Integración y Testing

**Duración:** 4 horas  
**Objetivo:** Integrar frontend con backend y escribir tests  
**Proyecto:** Sistema de eventos completo con pruebas

---

## 📚 Contenido Teórico

### 1. Fundamentos de Testing

#### 1.1 ¿Por qué hacer tests?

| Beneficio | Descripción |
|-----------|-------------|
| **Calidad** | Menos bugs en producción |
| **Confianza** | Refactorización segura |
| **Documentación** | Tests son documentación viva |
| **Regresión** | Detecta bugs automáticamente |
| **Tiempo** | Ahorra tiempo a largo plazo |

#### 1.2 Tipos de Tests

```
┌─────────────────────────────────────────────────────────────┐
│                    TIPOS DE TESTING                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  UNIT TESTS              INTEGRATION TESTS    E2E TESTS    │
│  ┌───────────┐           ┌───────────┐       ┌───────────┐ │
│  │  Función  │           │ Múltiples │       │  App      │ │
│  │  específica│◄────────►│ módulos   │◄─────►│ completa  │ │
│  └───────────┘           └───────────┘       └───────────┘ │
│       ▲                        ▲                  ▲        │
│       │                        │                  │        │
│  Rápido                  Moderado               Lento       │
│  (< 10ms)                (< 1s)                (> 10s)    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

#### 1.3 TDD (Test Driven Development)

```
1. Escribir test que falla
2. Implementar código mínimo
3. Refactorizar
4. Repetir
```

---

## 💻 Contenido Práctico

### 2. Testing con Jest - Backend

```bash
npm install --save-dev jest supertest mongodb-memory-server
```

```javascript
// server/tests/evento.test.js
const request = require('supertest');
const app = require('../src/index');
const Evento = require('../src/models/Evento');

describe('Eventos API', () => {
    let token;
    
    beforeEach(async () => {
        // Setup: crear usuario y obtener token
    });
    
    describe('GET /api/eventos', () => {
        it('debería listar eventos', async () => {
            const res = await request(app).get('/api/eventos');
            
            expect(res.status).toBe(200);
            expect(res.body.success).toBe(true);
        });
        
        it('debería filtrar por categoría', async () => {
            const res = await request(app).get('/api/eventos?categoria=musica');
            
            expect(res.status).toBe(200);
            expect(res.body.data[0].categoria).toBe('musica');
        });
    });
    
    describe('POST /api/eventos', () => {
        it('debería crear un evento', async () => {
            const eventoData = {
                titulo: 'Nuevo Evento',
                descripcion: 'Descripción',
                fecha: '2024-12-31',
                ubicacion: 'Montevideo',
                precio: 50,
                capacidad: 100,
                categoria: 'musica'
            };
            
            const res = await request(app)
                .post('/api/eventos')
                .set('Authorization', `Bearer ${token}`)
                .send(eventoData);
            
            expect(res.status).toBe(201);
            expect(res.body.data.titulo).toBe(eventoData.titulo);
        });
    });
});
```

### 3. Testing con React Testing Library

```bash
npm install --save-dev @testing-library/react @testing-library/jest-dom vitest
```

```jsx
// client/src/components/__tests__/EventoCard.test.jsx
import { render, screen, fireEvent } from '@testing-library/react';
import EventoCard from '../EventoCard';

const mockEvento = {
    id: '1',
    titulo: 'Concierto de Rock',
    fecha: '2024-03-15',
    precio: 50,
    categoria: 'musica'
};

describe('EventoCard', () => {
    it('debería renderizar el título', () => {
        render(<EventoCard evento={mockEvento} />);
        
        expect(screen.getByText('Concierto de Rock')).toBeInTheDocument();
    });
    
    it('debería renderizar el precio', () => {
        render(<EventoCard evento={mockEvento} />);
        
        expect(screen.getByText('$50')).toBeInTheDocument();
    });
    
    it('debería llamar onClick al hacer click', () => {
        const handleClick = jest.fn();
        
        render(<EventoCard evento={mockEvento} onClick={handleClick} />);
        
        fireEvent.click(screen.getByText('Concierto de Rock'));
        
        expect(handleClick).toHaveBeenCalled();
    });
});
```

---

## 📚 Ejercicios

1. Tests unitarios para modelos
2. Tests de controladores
3. Tests de integración
4. Tests de componentes React

---

## 📚 Recursos

- [Jest](https://jestjs.io/)
- [React Testing Library](https://testing-library.com/react)
