# 🔶 Clase 23: Angular - Fundamentos

**Duración:** 4 horas  
**Objetivo:** Dominar Angular, componentes, módulos y TypeScript  
**Proyecto:** Sistema de eventos con Angular

---

## 📚 Contenido Teórico

### 1. Fundamentos de Angular

#### 1.1 Instalación y Setup

```bash
# Instalar Angular CLI globalmente
npm install -g @angular/cli

# Crear nuevo proyecto
ng new mi-proyecto
cd mi-proyecto

# O con opciones específicas
ng new mi-proyecto --routing --style=scss --strict --skip-git
```

```bash
# Estructura del proyecto
mi-proyecto/
├── src/
│   ├── app/
│   │   ├── components/
│   │   ├── services/
│   │   ├── models/
│   │   ├── app.component.ts
│   │   ├── app.component.html
│   │   ├── app.component.css
│   │   ├── app.config.ts
│   │   └── app.routes.ts
│   ├── assets/
│   ├── styles.scss
│   ├── index.html
│   └── main.ts
├── angular.json
├── package.json
└── tsconfig.json
```

#### 1.2 Componentes

```typescript
// src/app/components/evento-card/evento-card.component.ts
import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';

interface Evento {
  id: number;
  titulo: string;
  descripcion: string;
  fecha: string;
  precio: number;
  imagen: string;
}

@Component({
  selector: 'app-evento-card',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './evento-card.component.html',
  styleUrls: ['./evento-card.component.css']
})
export class EventoCardComponent {
  @Input() evento!: Evento;
  @Input() variant: 'default' | 'compact' | 'featured' = 'default';
  @Output() clicked = new EventEmitter<Evento>();
  
  formatFecha(fecha: string): string {
    return new Date(fecha).toLocaleDateString('es-ES', {
      day: 'numeric',
      month: 'long'
    });
  }
  
  onClick(): void {
    this.clicked.emit(this.evento);
  }
}
```

```html
<!-- src/app/components/evento-card/evento-card.component.html -->
<article 
  class="evento-card" 
  [class]="variant"
  (click)="onClick()"
>
  <div class="imagen">
    <img [src]="evento.imagen" [alt]="evento.titulo" />
  </div>
  <div class="contenido">
    <h3>{{ evento.titulo }}</h3>
    <p class="fecha">{{ formatFecha(evento.fecha) }}</p>
    <p class="precio">{{ evento.precio === 0 ? 'Gratis' : '$' + evento.precio }}</p>
  </div>
</article>
```

```css
/* src/app/components/evento-card/evento-card.component.css */
.evento-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.2s;
}

.evento-card:hover {
  transform: translateY(-4px);
}

.evento-card img {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.contenido {
  padding: 16px;
}

.fecha {
  color: #666;
}

.precio {
  font-weight: bold;
  font-size: 1.2rem;
}
```

#### 1.3 Uso del Componente

```typescript
// src/app/app.component.ts
import { Component } from '@angular/core';
import { EventoCardComponent } from './components/evento-card/evento-card.component';

interface Evento {
  id: number;
  titulo: string;
  descripcion: string;
  fecha: string;
  precio: number;
  imagen: string;
}

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [EventoCardComponent],
  template: `
    <h1>Eventos</h1>
    <div class="grid">
      <app-evento-card
        *ngFor="let evento of eventos"
        [evento]="evento"
        [variant]="'default'"
        (clicked)="onEventoClick($event)"
      />
    </div>
  `
})
export class AppComponent {
  eventos: Evento[] = [
    {
      id: 1,
      titulo: 'Concierto de Rock',
      descripcion: 'Gran show',
      fecha: '2024-03-15',
      precio: 50,
      imagen: '/rock.jpg'
    },
    {
      id: 2,
      titulo: 'Festival de Jazz',
      descripcion: 'Noche de jazz',
      fecha: '2024-03-20',
      precio: 35,
      imagen: '/jazz.jpg'
    }
  ];
  
  onEventoClick(evento: Evento): void {
    console.log('Click:', evento);
  }
}
```

---

### 2. Directivas

#### 2.1 *ngIf, *ngFor, *ngSwitch

```html
<!-- ngIf -->
<div *ngIf="cargando">Cargando...</div>
<div *ngIf="error as err">Error: {{ err }}</div>
<div *ngIf="eventos.length > 0; else noEventos">
  Hay eventos
</div>
<ng-template #noEventos>
  No hay eventos
</ng-template>

<!-- ngFor -->
<li *ngFor="let evento of eventos; index as i; even as esPar">
  {{ i + 1 }}. {{ evento.titulo }}
  <span *ngIf="esPar">(par)</span>
</li>

<li *ngFor="let evento of eventos; trackBy: trackById">
  {{ evento.titulo }}
</li>

<!-- ngSwitch -->
<div [ngSwitch]="categoria">
  <div *ngSwitchCase="'musica'">Música</div>
  <div *ngSwitchCase="'deportes'">Deportes</div>
  <div *ngSwitchCase="'tecnologia'">Tecnología</div>
  <div *ngSwitchDefault>Otro</div>
</div>
```

```typescript
// trackBy function
trackById(index: number, item: any): number {
  return item.id;
}
```

#### 2.2 Directivas de Atributo

```html
<!-- ngClass -->
<div [ngClass]="{
  'activo': isActive,
  'destacado': isFeatured,
  'disabled': isDisabled
}">
  Contenido
</div>

<!-- ngStyle -->
<div [ngStyle]="{
  'color': color,
  'font-size.px': fontSize,
  'display': 'block'
}">
  Contenido
</div>

<!-- ngModel (requiere FormsModule) -->
<input [(ngModel)]="busqueda" />
```

---

### 3. Pipes

```html
<!-- Pipes integrados -->
<p>{{ fecha | date:'longDate' }}</p>
<!-- 15 de marzo de 2024 -->

<p>{{ precio | currency:'USD' }}</p>
<!-- $50.00 -->

<p>{{ evento.titulo | uppercase }}</p>

<p>{{ nombre | slice:0:10 }}</p>

<p>{{ evento | json }}</p>

<!-- Pipe con parámetros -->
<p>{{ texto | truncate:100:'...' }}</p>

<!-- Pipes encadenados -->
<p>{{ fecha | date:'short' | uppercase }}</p>
```

```typescript
// Custom pipe
import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'truncate'
})
export class TruncatePipe implements PipeTransform {
  transform(value: string, limit: number, trail: string = '...'): string {
    if (!value) return '';
    return value.length > limit 
      ? value.substring(0, limit) + trail 
      : value;
  }
}
```

---

### 4. Servicios e Inyección de Dependencias

#### 4.1 Crear Servicio

```typescript
// src/app/services/evento.service.ts
import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, BehaviorSubject, asyncScheduler } from 'rxjs';
import { tap, catchError, shareReplay } from 'rxjs/operators';

export interface Evento {
  id: number;
  titulo: string;
  descripcion: string;
  fecha: string;
  hora: string;
  ubicacion: string;
  precio: number;
  categoria: string;
  imagen: string;
  capacidad: number;
  entradasDisponibles: number;
}

@Injectable({
  providedIn: 'root'
})
export class EventoService {
  private http = inject(HttpClient);
  private apiUrl = '/api/eventos';
  
  private eventosCache$ = new BehaviorSubject<Evento[]>([]);
  
  getEventos(): Observable<Evento[]> {
    return this.eventosCache$.asObservable();
  }
  
  fetchEventos(): Observable<Evento[]> {
    return this.http.get<Evento[]>(this.apiUrl).pipe(
      tap(eventos => this.eventosCache$.next(eventos)),
      shareReplay(1),
      catchError(error => {
        console.error('Error:', error);
        throw error;
      })
    );
  }
  
  getEventoPorId(id: number): Observable<Evento> {
    return this.http.get<Evento>(`${this.apiUrl}/${id}`);
  }
  
  crearEvento(evento: Partial<Evento>): Observable<Evento> {
    return this.http.post<Evento>(this.apiUrl, evento).pipe(
      tap(nuevo => {
        const actuales = this.eventosCache$.getValue();
        this.eventosCache$.next([...actuales, nuevo]);
      })
    );
  }
  
  eliminarEvento(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${id}`).pipe(
      tap(() => {
        const actuales = this.eventosCache$.getValue();
        this.eventosCache$.next(actuales.filter(e => e.id !== id));
      })
    );
  }
}
```

---

### 5. Formularios

#### 5.1 Template-driven

```typescript
// component.ts
import { Component } from '@angular/core';
import { NgForm } from '@angular/forms';

@Component({
  selector: 'app-evento-form',
  template: `
    <form #form="ngForm" (ngSubmit)="onSubmit(form)">
      <div>
        <label>Título</label>
        <input 
          type="text" 
          name="titulo" 
          [(ngModel)]="evento.titulo"
          required
          minlength="5"
          #tituloInput="ngModel"
        />
        <div *ngIf="tituloInput.invalid && tituloInput.touched">
          Título requerido (mín 5 caracteres)
        </div>
      </div>
      
      <div>
        <label>Precio</label>
        <input 
          type="number" 
          name="precio" 
          [(ngModel)]="evento.precio"
          min="0"
        />
      </div>
      
      <div>
        <label>Categoría</label>
        <select name="categoria" [(ngModel)]="evento.categoria">
          <option value="musica">Música</option>
          <option value="deportes">Deportes</option>
          <option value="tecnologia">Tecnología</option>
        </select>
      </div>
      
      <button type="submit" [disabled]="form.invalid">
        Guardar
      </button>
    </form>
  `
})
export class EventoFormComponent {
  evento = {
    titulo: '',
    precio: 0,
    categoria: 'musica'
  };
  
  onSubmit(form: NgForm): void {
    if (form.valid) {
      console.log('Datos:', this.evento);
    }
  }
}
```

#### 5.2 Reactive Forms

```typescript
import { Component, inject } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-evento-form',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  template: `
    <form [formGroup]="form" (ngSubmit)="onSubmit()">
      <div>
        <label>Título</label>
        <input formControlName="titulo" />
        <div *ngIf="form.get('titulo')?.invalid && form.get('titulo')?.touched">
          <small *ngIf="form.get('titulo')?.errors?.['required']">
            Título requerido
          </small>
          <small *ngIf="form.get('titulo')?.errors?.['minlength']">
            Mínimo 5 caracteres
          </small>
        </div>
      </div>
      
      <div>
        <label>Email</label>
        <input formControlName="email" type="email" />
      </div>
      
      <div formGroupName="direccion">
        <label>Calle</label>
        <input formControlName="calle" />
      </div>
      
      <button type="submit" [disabled]="form.invalid">
        Guardar
      </button>
    </form>
  `
})
export class EventoFormComponent {
  private fb = inject(FormBuilder);
  
  form = this.fb.group({
    titulo: ['', [Validators.required, Validators.minLength(5)]],
    descripcion: [''],
    precio: [0, [Validators.min(0)]],
    email: ['', [Validators.required, Validators.email]],
    categoria: ['musica'],
    direccion: this.fb.group({
      calle: [''],
      ciudad: ['']
    })
  });
  
  onSubmit(): void {
    if (this.form.valid) {
      console.log('Form value:', this.form.value);
    }
  }
}
```

---

## 💻 Contenido Práctico

### 6. Ejercicio Resuelto: Lista de Eventos

```typescript
// src/app/pages/eventos/eventos.component.ts
import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { EventoService, Evento } from '../../services/evento.service';
import { EventoCardComponent } from '../../components/evento-card/evento-card.component';

@Component({
  selector: 'app-eventos',
  standalone: true,
  imports: [CommonModule, RouterModule, EventoCardComponent],
  template: `
    <div class="eventos-page">
      <header>
        <h1>Todos los Eventos</h1>
        <a routerLink="/eventos/nuevo" class="btn btn-primary">
          Crear Evento
        </a>
      </header>
      
      <div class="filtros">
        <input
          type="text"
          placeholder="Buscar..."
          [(ngModel)]="filtroTexto"
          (ngModelChange)="filtrar()"
        />
        
        <select [(ngModel)]="filtroCategoria" (ngModelChange)="filtrar()">
          <option value="todas">Todas</option>
          <option value="musica">Música</option>
          <option value="deportes">Deportes</option>
          <option value="tecnologia">Tecnología</option>
        </select>
      </div>
      
      <div *ngIf="cargando" class="loading">Cargando...</div>
      
      <div *ngIf="error" class="error">{{ error }}</div>
      
      <div class="grid" *ngIf="!cargando && !error">
        <app-evento-card
          *ngFor="let evento of eventosFiltrados"
          [evento]="evento"
          (clicked)="verDetalle($event)"
        />
      </div>
      
      <p *ngIf="!cargando && eventosFiltrados.length === 0">
        No se encontraron eventos
      </p>
    </div>
  `
})
export class EventosComponent implements OnInit {
  private eventoService = inject(EventoService);
  
  eventos: Evento[] = [];
  eventosFiltrados: Evento[] = [];
  cargando = true;
  error = '';
  
  filtroTexto = '';
  filtroCategoria = 'todas';
  
  ngOnInit(): void {
    this.cargarEventos();
  }
  
  cargarEventos(): void {
    this.eventoService.fetchEventos().subscribe({
      next: (eventos) => {
        this.eventos = eventos;
        this.eventosFiltrados = eventos;
        this.cargando = false;
      },
      error: (err) => {
        this.error = err.message;
        this.cargando = false;
      }
    });
  }
  
  filtrar(): void {
    let resultado = [...this.eventos];
    
    if (this.filtroTexto) {
      const texto = this.filtroTexto.toLowerCase();
      resultado = resultado.filter(e => 
        e.titulo.toLowerCase().includes(texto)
      );
    }
    
    if (this.filtroCategoria !== 'todas') {
      resultado = resultado.filter(e => 
        e.categoria === this.filtroCategoria
      );
    }
    
    this.eventosFiltrados = resultado;
  }
  
  verDetalle(evento: Evento): void {
    console.log('Ver detalle:', evento);
  }
}
```

---

## 🛠️ Ejercicios Prácticos

### Ejercicio 1: Componente Contador
- Input, Output, EventEmitter

### Ejercicio 2: Formulario Reactive
- Validaciones, grupos

### Ejercicio 3: Pipe Personalizado
- Transformar datos

### Ejercicio 4: Servicio con HTTP
- CRUD completo

---

## 🚀 Proyecto de la Clase

### Sistema de Eventos con Angular

```typescript
// app.config.ts
import { ApplicationConfig } from '@angular/core';
import { provideRouter } from '@angular/router';
import { provideHttpClient } from '@angular/common/http';
import { routes } from './app.routes';

export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(routes),
    provideHttpClient()
  ]
};
```

```typescript
// app.routes.ts
import { Routes } from '@angular/router';

export const routes: Routes = [
  { path: '', redirectTo: 'eventos', pathMatch: 'full' },
  { 
    path: 'eventos', 
    loadComponent: () => import('./pages/eventos/eventos.component')
      .then(m => m.EventosComponent)
  },
  { 
    path: 'eventos/:id', 
    loadComponent: () => import('./pages/evento-detalle/evento-detalle.component')
      .then(m => m.EventoDetalleComponent)
  }
];
```

### Entregables

1. **Proyecto Angular** configurado
2. **Componentes** con standalone
3. **Servicios** con HTTP
4. **Formularios** reactivos
5. **Pipes** personalizados

---

## 📚 Recursos Adicionales

- [Angular Docs](https://angular.io/)
- [Angular Components](https://angular.io/guide/component-overview)
- [Angular Services](https://angular.io/guide/services)
