# 🎯 Clase 25: Angular - Proyecto Completo

**Duración:** 4 horas  
**Objetivo:** Construir sistema de eventos completo con Angular, TypeScript y Signals  
**Proyecto:** App full-stack de eventos

---

## 📚 Contenido Teórico

### 1. Estructura del Proyecto Full

```
mi-proyecto/
├── src/
│   ├── app/
│   │   ├── core/
│   │   │   ├── guards/
│   │   │   │   └── auth.guard.ts
│   │   │   ├── interceptors/
│   │   │   │   └── auth.interceptor.ts
│   │   │   └── services/
│   │   │       ├── auth.service.ts
│   │   │       └── evento.service.ts
│   │   ├── features/
│   │   │   ├── eventos/
│   │   │   │   ├── components/
│   │   │   │   │   ├── evento-card/
│   │   │   │   │   ├── evento-list/
│   │   │   │   │   └── evento-form/
│   │   │   │   └── pages/
│   │   │   │       ├── eventos-page/
│   │   │   │       └── evento-detalle-page/
│   │   │   └── auth/
│   │   │       ├── login/
│   │   │       └── register/
│   │   ├── shared/
│   │   │   ├── components/
│   │   │   │   ├── header/
│   │   │   │   ├── footer/
│   │   │   │   └── spinner/
│   │   │   └── pipes/
│   │   │       └── truncate.pipe.ts
│   │   ├── app.component.ts
│   │   ├── app.config.ts
│   │   └── app.routes.ts
│   ├── assets/
│   └── styles.scss
├── angular.json
├── package.json
└── tsconfig.json
```

---

### 2. Configuración de App

```typescript
// app.config.ts
import { ApplicationConfig, provideZoneChangeDetection } from '@angular/core';
import { provideRouter, withComponentInputBinding } from '@angular/router';
import { provideHttpClient, withInterceptors } from '@angular/common/http';
import { provideAnimations } from '@angular/platform-browser/animations';
import { routes } from './app.routes';
import { authInterceptor } from './core/interceptors/auth.interceptor';

export const appConfig: ApplicationConfig = {
  providers: [
    provideZoneChangeDetection({ eventCoalescing: true }),
    provideRouter(routes, withComponentInputBinding()),
    provideHttpClient(withInterceptors([authInterceptor])),
    provideAnimations()
  ]
};
```

```typescript
// app.routes.ts
import { Routes } from '@angular/router';
import { authGuard } from './core/guards/auth.guard';

export const routes: Routes = [
  {
    path: '',
    redirectTo: 'eventos',
    pathMatch: 'full'
  },
  {
    path: 'eventos',
    loadChildren: () => import('./features/eventos/eventos.routes')
      .then(m => m.EVENTOS_ROUTES)
  },
  {
    path: 'login',
    loadComponent: () => import('./features/auth/login/login.component')
      .then(m => m.LoginComponent)
  },
  {
    path: 'admin',
    loadChildren: () => import('./features/admin/admin.routes')
      .then(m => m.ADMIN_ROUTES),
    canActivate: [authGuard],
    data: { rol: 'admin' }
  },
  {
    path: '**',
    loadComponent: () => import('./shared/components/not-found/not-found.component')
      .then(m => m.NotFoundComponent)
  }
];
```

---

### 3. Tipos con TypeScript

```typescript
// models/evento.model.ts
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
  organizadorId: number;
  creadoEn: string;
  actualizadoEn: string;
}

export type Categoria = 'musica' | 'deportes' | 'tecnologia' | 'arte' | 'otro';

export interface CreateEventoDto {
  titulo: string;
  descripcion: string;
  fecha: string;
  hora: string;
  ubicacion: string;
  precio: number;
  categoria: Categoria;
  capacidad: number;
  imagen?: string;
}

export interface Usuario {
  id: number;
  nombre: string;
  email: string;
  rol: 'usuario' | 'organizador' | 'admin';
  avatar?: string;
}

export interface LoginResponse {
  usuario: Usuario;
  token: string;
}

export interface PageResponse<T> {
  items: T[];
  total: number;
  page: number;
  limit: number;
}
```

---

### 4. Guards e Interceptores

```typescript
// core/guards/auth.guard.ts
import { inject } from '@angular/core';
import { Router, CanActivateFn } from '@angular/router';
import { AuthService } from '../services/auth.service';

export const authGuard: CanActivateFn = (route, state) => {
  const authService = inject(AuthService);
  const router = inject(Router);
  
  if (!authService.isAuthenticated()) {
    router.navigate(['/login'], { 
      queryParams: { redirect: state.url } 
    });
    return false;
  }
  
  const requiredRol = route.data['rol'] as string | undefined;
  
  if (requiredRol && authService.usuario()?.rol !== requiredRol) {
    router.navigate(['/']);
    return false;
  }
  
  return true;
};
```

```typescript
// core/interceptors/auth.interceptor.ts
import { HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { AuthService } from '../services/auth.service';

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const authService = inject(AuthService);
  const token = authService.token();
  
  if (token) {
    req = req.clone({
      setHeaders: {
        Authorization: `Bearer ${token}`
      }
    });
  }
  
  return next(req);
};
```

---

### 5. Servicios con Signals

```typescript
// core/services/auth.service.ts
import { Injectable, inject, signal, computed } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { tap, catchError, of, Observable } from 'rxjs';
import { Usuario, LoginResponse } from '../../models/evento.model';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private http = inject(HttpClient);
  private router = inject(Router);
  private apiUrl = '/api/auth';
  
  // State signals
  private _usuario = signal<Usuario | null>(null);
  private _token = signal<string | null>(null);
  
  // Readonly
  readonly usuario = this._usuario.asReadonly();
  readonly token = this._token.asReadonly();
  
  readonly isAuthenticated = computed(() => !!this._token());
  readonly isAdmin = computed(() => this._usuario()?.rol === 'admin');
  readonly isOrganizador = computed(() => 
    this._usuario()?.rol === 'organizador' || this.isAdmin()
  );
  
  constructor() {
    // Restore from localStorage
    const token = localStorage.getItem('token');
    const usuario = localStorage.getItem('usuario');
    
    if (token && usuario) {
      this._token.set(token);
      this._usuario.set(JSON.parse(usuario));
    }
  }
  
  login(email: string, password: string): Observable<boolean> {
    return this.http.post<LoginResponse>(`${this.apiUrl}/login`, { email, password })
      .pipe(
        tap(response => {
          this._token.set(response.token);
          this._usuario.set(response.usuario);
          localStorage.setItem('token', response.token);
          localStorage.setItem('usuario', JSON.stringify(response.usuario));
        }),
        map(() => true),
        catchError(() => of(false))
      );
  }
  
  logout(): void {
    this._token.set(null);
    this._usuario.set(null);
    localStorage.removeItem('token');
    localStorage.removeItem('usuario');
    this.router.navigate(['/login']);
  }
  
  register(data: { nombre: string; email: string; password: string }): Observable<boolean> {
    return this.http.post<LoginResponse>(`${this.apiUrl}/register`, data)
      .pipe(
        tap(response => {
          this._token.set(response.token);
          this._usuario.set(response.usuario);
          localStorage.setItem('token', response.token);
          localStorage.setItem('usuario', JSON.stringify(response.usuario));
        }),
        map(() => true),
        catchError(() => of(false))
      );
  }
}
```

```typescript
// features/eventos/services/evento.store.ts
import { Injectable, inject, signal, computed } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, tap, catchError, of, map } from 'rxjs';
import { Evento, CreateEventoDto, Categoria } from '../../../models/evento.model';

export interface Filtros {
  categoria: Categoria | 'todas';
  busqueda: string;
  ordenarPor: 'fecha' | 'precio' | 'titulo';
}

@Injectable({ providedIn: 'root' })
export class EventoStore {
  private http = inject(HttpClient);
  private apiUrl = '/api/eventos';
  
  // State
  private _eventos = signal<Evento[]>([]);
  private _eventoActual = signal<Evento | null>(null);
  private _cargando = signal(false);
  private _error = signal<string | null>(null);
  private _filtros = signal<Filtros>({
    categoria: 'todas',
    busqueda: '',
    ordenarPor: 'fecha'
  });
  
  // Readonly
  readonly eventos = this._eventos.asReadonly();
  readonly eventoActual = this._eventoActual.asReadonly();
  readonly cargando = this._cargando.asReadonly();
  readonly error = this._error.asReadonly();
  readonly filtros = this._filtros.asReadonly();
  
  // Computed
  readonly eventosFiltrados = computed(() => {
    let resultado = [...this._eventos()];
    const filtros = this._filtros();
    
    if (filtros.busqueda) {
      const texto = filtros.busqueda.toLowerCase();
      resultado = resultado.filter(e => 
        e.titulo.toLowerCase().includes(texto) ||
        e.descripcion?.toLowerCase().includes(texto)
      );
    }
    
    if (filtros.categoria !== 'todas') {
      resultado = resultado.filter(e => e.categoria === filtros.categoria);
    }
    
    resultado.sort((a, b) => {
      switch (filtros.ordenarPor) {
        case 'fecha':
          return new Date(a.fecha).getTime() - new Date(b.fecha).getTime();
        case 'precio':
          return a.precio - b.precio;
        case 'titulo':
          return a.titulo.localeCompare(b.titulo);
        default:
          return 0;
      }
    });
    
    return resultado;
  });
  
  readonly categorias = computed(() => {
    const cats = new Set(this._eventos().map(e => e.categoria));
    return ['todas', ...Array.from(cats)];
  });
  
  // Actions
  setFiltros(filtros: Partial<Filtros>): void {
    this._filtros.update(f => ({ ...f, ...filtros }));
  }
  
  fetchEventos(): void {
    this._cargando.set(true);
    this._error.set(null);
    
    this.http.get<Evento[]>(this.apiUrl).pipe(
      tap(eventos => {
        this._eventos.set(eventos);
        this._cargando.set(false);
      }),
      catchError(error => {
        this._error.set(error.message);
        this._cargando.set(false);
        return of([]);
      })
    ).subscribe();
  }
  
  fetchEventoPorId(id: number): void {
    this._cargando.set(true);
    this._error.set(null);
    
    this.http.get<Evento>(`${this.apiUrl}/${id}`).pipe(
      tap(evento => {
        this._eventoActual.set(evento);
        this._cargando.set(false);
      }),
      catchError(error => {
        this._error.set(error.message);
        this._cargando.set(false);
        return of(null);
      })
    ).subscribe();
  }
  
  crearEvento(evento: CreateEventoDto): Observable<Evento | null> {
    this._cargando.set(true);
    
    return this.http.post<Evento>(this.apiUrl, evento).pipe(
      tap(nuevo => {
        this._eventos.update(e => [...e, nuevo]);
        this._cargando.set(false);
      }),
      map(evento => {
        this._cargando.set(false);
        return evento;
      }),
      catchError(error => {
        this._error.set(error.message);
        this._cargando.set(false);
        return of(null);
      })
    );
  }
  
  eliminarEvento(id: number): Observable<boolean> {
    return this.http.delete<void>(`${this.apiUrl}/${id}`).pipe(
      tap(() => {
        this._eventos.update(e => e.filter(evt => evt.id !== id));
      }),
      map(() => true),
      catchError(error => {
        this._error.set(error.message);
        return of(false);
      })
    );
  }
  
  clearEventoActual(): void {
    this._eventoActual.set(null);
  }
}
```

---

## 💻 Contenido Práctico

### 6. Componentes del Proyecto

```typescript
// features/eventos/pages/eventos-list/eventos-list.component.ts
import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { EventoStore } from '../../services/evento.store';
import { EventoCardComponent } from '../../components/evento-card/evento-card.component';
import { Filtros } from '../../models/evento.model';

@Component({
  selector: 'app-eventos-list',
  standalone: true,
  imports: [CommonModule, RouterModule, FormsModule, EventoCardComponent],
  template: `
    <div class="eventos-page">
      <header class="header">
        <h1>Todos los Eventos</h1>
        <a *ngIf="auth.isOrganizador()" routerLink="/eventos/nuevo" class="btn btn-primary">
          Crear Evento
        </a>
      </header>
      
      <div class="filtros">
        <input
          type="text"
          placeholder="Buscar eventos..."
          [ngModel]="store.filtros().busqueda"
          (ngModelChange)="onBusquedaChange($event)"
          class="input-buscar"
        />
        
        <select
          [ngModel]="store.filtros().categoria"
          (ngModelChange)="onCategoriaChange($event)"
        >
          <option *ngFor="let cat of store.categorias()" [value]="cat">
            {{ cat === 'todas' ? 'Todas las categorías' : cat }}
          </option>
        </select>
        
        <select
          [ngModel]="store.filtros().ordenarPor"
          (ngModelChange)="onOrdenChange($event)"
        >
          <option value="fecha">Por Fecha</option>
          <option value="precio">Por Precio</option>
          <option value="titulo">Por Título</option>
        </select>
      </div>
      
      <div *ngIf="store.cargando()" class="loading">
        <app-spinner />
      </div>
      
      <div *ngIf="store.error() as error" class="error">
        {{ error }}
      </div>
      
      <div *ngIf="!store.cargando()" class="eventos-grid">
        <app-evento-card
          *ngFor="let evento of store.eventosFiltrados()"
          [evento]="evento"
          [routerLink]="['/eventos', evento.id]"
        />
      </div>
      
      <p *ngIf="!store.cargando() && store.eventosFiltrados().length === 0" class="no-resultados">
        No se encontraron eventos
      </p>
    </div>
  `,
  styles: [`
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
    
    .loading, .error, .no-resultados {
      text-align: center;
      padding: 40px;
    }
  `]
})
export class EventosListComponent implements OnInit {
  store = inject(EventoStore);
  auth = inject(AuthService); // necesitas inyectar
  
  ngOnInit(): void {
    this.store.fetchEventos();
  }
  
  onBusquedaChange(value: string): void {
    this.store.setFiltros({ busqueda: value });
  }
  
  onCategoriaChange(value: string): void {
    this.store.setFiltros({ categoria: value as any });
  }
  
  onOrdenChange(value: string): void {
    this.store.setFiltros({ ordenarPor: value as any });
  }
}
```

```typescript
// features/eventos/pages/evento-detalle/evento-detalle.component.ts
import { Component, OnInit, OnDestroy, inject, input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { EventoStore } from '../../services/evento.store';
import { CarritoService } from '../../../carrito/services/carrito.service';

@Component({
  selector: 'app-evento-detalle',
  standalone: true,
  imports: [CommonModule, RouterModule],
  template: `
    <div class="detalle-page">
      <button routerLink="/eventos" class="btn-volver">
        ← Volver a Eventos
      </button>
      
      <div *ngIf="store.cargando()" class="loading">
        <app-spinner />
      </div>
      
      <div *ngIf="store.error() as error" class="error">
        {{ error }}
      </div>
      
      <article *ngIf="evento()" class="evento-detalle">
        <div class="imagen">
          <img [src]="evento()!.imagen" [alt]="evento()!.titulo" />
        </div>
        
        <div class="contenido">
          <span class="categoria">{{ evento()!.categoria }}</span>
          <h1>{{ evento()!.titulo }}</h1>
          
          <div class="meta">
            <p>📅 {{ evento()!.fecha | date:'fullDate' }}</p>
            <p>🕐 {{ evento()!.hora }}</p>
            <p>📍 {{ evento()!.ubicacion }}</p>
          </div>
          
          <p class="descripcion">{{ evento()!.descripcion }}</p>
          
          <div class="precio">
            <span class="valor">
              {{ evento()!.precio === 0 ? 'Gratis' : '$' + evento()!.precio }}
            </span>
            <span class="disponibles">
              {{ evento()!.entradasDisponibles }} entradas disponibles
            </span>
          </div>
          
          <button 
            class="btn btn-primary btn-comprar"
            [disabled]="evento()!.entradasDisponibles === 0"
            (click)="comprar()"
          >
            {{ evento()!.entradasDisponibles === 0 ? 'Agotado' : 'Comprar Entrada' }}
          </button>
        </div>
      </article>
    </div>
  `,
  styles: [`
    .detalle-page {
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
    
    .btn-comprar {
      width: 100%;
      padding: 14px;
      font-size: 16px;
    }
  `]
})
export class EventoDetalleComponent implements OnInit, OnDestroy {
  store = inject(EventoStore);
  private carrito = inject(CarritoService);
  
  // Route input binding (Angular 16+)
  id = input<number>();
  
  evento = this.store.eventoActual;
  
  ngOnInit(): void {
    const id = this.id();
    if (id) {
      this.store.fetchEventoPorId(id);
    }
  }
  
  ngOnDestroy(): void {
    this.store.clearEventoActual();
  }
  
  comprar(): void {
    const evt = this.evento();
    if (evt) {
      this.carrito.agregar(evt);
    }
  }
}
```

---

### 7. Routing de Eventos

```typescript
// features/eventos/eventos.routes.ts
import { Routes } from '@angular/router';

export const EVENTOS_ROUTES: Routes = [
  {
    path: '',
    loadComponent: () => import('./pages/eventos-list/eventos-list.component')
      .then(m => m.EventosListComponent)
  },
  {
    path: ':id',
    loadComponent: () => import('./pages/evento-detalle/evento-detalle.component')
      .then(m => m.EventoDetalleComponent)
  },
  {
    path: 'nuevo',
    loadComponent: () => import('./pages/evento-form/evento-form.component')
      .then(m => m.EventoFormComponent),
    // canActivate: [authGuard] // descomenta para proteger
  }
];
```

---

## 🛠️ Ejercicios Prácticos

### Ejercicio 1: Login/Register
- Formularios reactivos
- Auth service con signals

### Ejercicio 2: Admin Dashboard
- CRUD completo de eventos

### Ejercicio 3: Carrito de Compras
- Agregar, quitar, calcular total

### Ejercicio 4: Protected Routes
- Guards por rol

---

## 🚀 Proyecto de la Clase

### App Completa con Angular

```typescript
// main.ts
import { bootstrapApplication } from '@angular/platform-browser';
import { AppComponent } from './app/app.component';
import { appConfig } from './app/app.config';

bootstrapApplication(AppComponent, appConfig)
  .catch(err => console.error(err));
```

```typescript
// app.component.ts
import { Component } from '@angular/core';
import { RouterOutlet, RouterModule } from '@angular/router';
import { HeaderComponent } from './shared/components/header/header.component';
import { FooterComponent } from './shared/components/footer/footer.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, RouterModule, HeaderComponent, FooterComponent],
  template: `
    <app-header />
    <main>
      <router-outlet />
    </main>
    <app-footer />
  `,
  styles: [`
    :host {
      display: flex;
      flex-direction: column;
      min-height: 100vh;
    }
    
    main {
      flex: 1;
    }
  `]
})
export class AppComponent {}
```

### Entregables

1. **Proyecto completo** con Angular 17+
2. **Servicios con Signals**
3. **Routing** con guards
4. **HTTP** con interceptores
5. ** CRUD** de eventos
6. **Carrito de compras**

---

## 📚 Recursos Adicionales

- [Angular Standalone](https://angular.io/guide/standalone-components)
- [Angular Signals](https://angular.io/guide/signals)
- [Angular Router](https://angular.io/guide/router)
