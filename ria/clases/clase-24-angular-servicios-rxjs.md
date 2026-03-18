# ⚡ Clase 24: Angular - Servicios, RxJS y Estado

**Duración:** 4 horas  
**Objetivo:** Dominar RxJS, signals y gestión de estado en Angular  
**Proyecto:** Sistema de eventos reactivo

---

## 📚 Contenido Teórico

### 1. RxJS en Angular

#### 1.1 Observables Básico

```typescript
import { Observable, of, throwError, from, interval, timer } from 'rxjs';
import { map, filter, reduce, catchError, tap } from 'rxjs/operators';

// Observable simple
const obs$ = new Observable(observer => {
  observer.next(1);
  observer.next(2);
  observer.next(3);
  observer.complete();
});

obs$.subscribe(val => console.log(val));

// of - crear observable de valores
of(1, 2, 3).subscribe();

// from - de array o promise
from([1, 2, 3]).subscribe();
from(Promise.resolve('dato')).subscribe();

// map
of(1, 2, 3).pipe(
  map(x => x * 2)
).subscribe();

// filter
of(1, 2, 3, 4, 5).pipe(
  filter(x => x > 2)
).subscribe();

// pipe con múltiples operadores
of(1, 2, 3, 4, 5).pipe(
  filter(x => x % 2 === 0),
  map(x => x * 10)
).subscribe();
```

#### 1.2 Operadores de Creación

```typescript
import { interval, timer, fromEvent, ajax, EMPTY } from 'rxjs';
import { map, take, takeUntil, switchMap, mergeMap } from 'rxjs/operators';

// interval - emite cada X milisegundos
interval(1000).pipe(
  take(5)
).subscribe();

// timer -delay inicial
timer(1000, 1000).pipe(
  take(5)
).subscribe();

// fromEvent - de evento del DOM
const button = document.querySelector('button');
fromEvent(button!, 'click').subscribe();

// ajax - HTTP requests
ajax.getJSON('/api/eventos').subscribe();

// EMPTY - observable vacío
EMPTY.subscribe(); // completa inmediatamente

// throwError - error
throwError(() => new Error('Error')).subscribe({
  error: err => console.log(err)
});
```

#### 1.3 Operadores de Transformación

```typescript
import { of, from } from 'rxjs';
import { map, mergeMap, switchMap, exhaustMap, flatMap } from 'rxjs/operators';

// map
of(1, 2, 3).pipe(
  map(x => ({ valor: x, doble: x * 2 }))
).subscribe();

// mergeMap - ejecuta observable interno, aplanar
of(1, 2, 3).pipe(
  mergeMap(x => of(x * 2))
).subscribe();

// switchMap - cancela observable anterior
fromEvent(document, 'click').pipe(
  switchMap(() => interval(1000))
).subscribe();

// exhaustMap - ignora hasta que complete
fromEvent(document, 'click').pipe(
  exhaustMap(() => of(1, 2, 3))
).subscribe();

// flatten arrays
from([1, 2, 3]).pipe(
  map(x => [x, x * 2]),
  mergeMap(x => from(x))
).subscribe();
```

#### 1.4 Operadores de Filtrado

```typescript
import { interval, of } from 'rxjs';
import { filter, take, debounceTime, distinctUntilChanged, takeUntil, skip } from 'rxjs/operators';

// filter
of(1, 2, 3, 4, 5).pipe(
  filter(x => x > 2)
).subscribe();

// take - primeros N
interval(1000).pipe(
  take(5)
).subscribe();

// skip - omitir primeros N
of(1, 2, 3, 4, 5).pipe(
  skip(2)
).subscribe();

// takeUntil - completar cuando otro observable emite
interval(1000).pipe(
  takeUntil(timer(5000))
).subscribe();

// debounceTime - esperar silencios
fromEvent(document, 'input').pipe(
  debounceTime(300)
).subscribe();

// distinctUntilChanged - solo cambios
of(1, 1, 2, 2, 3).pipe(
  distinctUntilChanged()
).subscribe();
```

---

### 2. HTTP con RxJS

```typescript
import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, retry, shareReplay, finalize } from 'rxjs/operators';

@Injectable({ providedIn: 'root' })
export class EventoService {
  private http = inject(HttpClient);
  private apiUrl = '/api/eventos';
  
  // GET con parámetros
  getEventos(params?: {
    categoria?: string;
    busqueda?: string;
    page?: number;
    limit?: number;
  }): Observable<any[]> {
    let httpParams = new HttpParams();
    
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          httpParams = httpParams.set(key, value.toString());
        }
      });
    }
    
    return this.http.get<any[]>(this.apiUrl, { params: httpParams }).pipe(
      retry(2), // reintentar 2 veces
      catchError(error => {
        console.error('Error:', error);
        return throwError(() => error);
      }),
      shareReplay(1) // cachear última emisión
    );
  }
  
  // POST
  crearEvento(data: any): Observable<any> {
    return this.http.post(this.apiUrl, data).pipe(
      catchError(error => throwError(() => error))
    );
  }
  
  // PUT
  actualizarEvento(id: number, data: any): Observable<any> {
    return this.http.put(`${this.apiUrl}/${id}`, data);
  }
  
  // DELETE
  eliminarEvento(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${id}`);
  }
  
  // POST con progress
  subirArchivo(file: File): Observable<any> {
    const formData = new FormData();
    formData.append('file', file);
    
    return this.http.post('/api/upload', formData, {
      reportProgress: true
    });
  }
}
```

---

### 3. Signals (Angular 16+)

#### 3.1 Signals Básico

```typescript
import { Component, signal, computed, effect } from '@angular/core';

@Component({
  selector: 'app-contador',
  template: `
    <p>Count: {{ count() }}</p>
    <p>Doble: {{ doble() }}</p>
    <button (click)="incrementar()">+</button>
    <button (click)="resetear()">Reset</button>
  `
})
export class ContadorComponent {
  // Signal - valor reactivo
  count = signal(0);
  
  // Computed - derivado
  doble = computed(() => this.count() * 2);
  
  constructor() {
    // Effect - efecto secundarios
    effect(() => {
      console.log('Count cambió:', this.count());
    });
  }
  
  incrementar(): void {
    this.count.update(c => c + 1);
  }
  
  resetear(): void {
    this.count.set(0);
  }
}
```

#### 3.2 Signals con Servicios

```typescript
// services/carrito.service.ts
import { Injectable, signal, computed } from '@angular/core';

interface CarritoItem {
  id: number;
  nombre: string;
  precio: number;
  cantidad: number;
}

@Injectable({ providedIn: 'root' })
export class CarritoService {
  // State como signals
  private _items = signal<CarritoItem[]>([]);
  
  // Getters públicos
  readonly items = this._items.asReadonly();
  
  readonly total = computed(() => 
    this._items().reduce((sum, item) => sum + item.precio * item.cantidad, 0)
  );
  
  readonly cantidad = computed(() => 
    this._items().reduce((sum, item) => sum + item.cantidad, 0)
  );
  
  agregar(item: CarritoItem): void {
    this._items.update(items => {
      const existente = items.find(i => i.id === item.id);
      if (existente) {
        return items.map(i => 
          i.id === item.id 
            ? { ...i, cantidad: i.cantidad + 1 }
            : i
        );
      }
      return [...items, { ...item, cantidad: 1 }];
    });
  }
  
  quitar(id: number): void {
    this._items.update(items => items.filter(i => i.id !== id));
  }
  
  vaciar(): void {
    this._items.set([]);
  }
}
```

```typescript
// Usar en componente
@Component({
  selector: 'app-carrito',
  template: `
    <p>Items: {{ carrito.cantidad() }}</p>
    <p>Total: ${{ carrito.total() }}</p>
    <ul>
      <li *ngFor="let item of carrito.items()">
        {{ item.nombre }} - {{ item.cantidad }}
        <button (click)="carrito.quitar(item.id)">X</button>
      </li>
    </ul>
  `
})
export class CarritoComponent {
  constructor(public carrito: CarritoService) {}
}
```

---

### 4. Estado Global con Services

```typescript
// services/ui.service.ts
import { Injectable, signal } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class UiService {
  // UI state
  private _sidebarAbierto = signal(true);
  readonly sidebarAbierto = this._sidebarAbierto.asReadonly();
  
  private _tema = signal<'claro' | 'oscuro'>('claro');
  readonly tema = this._tema.asReadonly();
  
  private _cargando = signal(false);
  readonly cargando = this._cargando.asReadonly();
  
  toggleSidebar(): void {
    this._sidebarAbierto.update(v => !v);
  }
  
  toggleTema(): void {
    this._tema.update(t => t === 'claro' ? 'oscuro' : 'claro');
  }
  
  setCargando(value: boolean): void {
    this._cargando.set(value);
  }
}
```

---

### 5. RxJS en Componentes

#### 5.1 Subscripciones y Cleanup

```typescript
import { Component, OnInit, OnDestroy, inject } from '@angular/core';
import { Subject, takeUntil, Subscription } from 'rxjs';
import { EventoService } from '../services/evento.service';

@Component({
  selector: 'app-eventos',
  template: `
    <div *ngFor="let e of eventos$ | async">{{ e.titulo }}</div>
  `
})
export class EventosComponent implements OnInit, OnDestroy {
  private eventoService = inject(EventoService);
  private destroy$ = new Subject<void>();
  
  // Observable directo
  eventos$ = this.eventoService.getEventos();
  
  ngOnInit(): void {
    // Con takeUntil
    this.eventoService.getEventos().pipe(
      takeUntil(this.destroy$)
    ).subscribe(datos => {
      // hacer algo
    });
  }
  
  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }
}
```

#### 5.2 Async Pipe

```typescript
@Component({
  selector: 'app-eventos',
  template: `
    <!-- async pipe subscribe/unsubscribe automáticamente -->
    <div *ngIf="eventos$ | async as eventos; else loading">
      <div *ngFor="let e of eventos">{{ e.titulo }}</div>
    </div>
    
    <ng-template #loading>
      <p>Cargando...</p>
    </ng-template>
    
    <!-- Error handling -->
    <div *ngIf="eventos$ | async as datos; else loading">
      {{ datos | json }}
    </div>
    
    <ng-container *ngIf="eventos$ | async as datos; else loading">
      <app-evento-card *ngFor="let e of datos" [evento]="e" />
    </ng-container>
  `
})
export class EventosComponent {
  eventos$ = this.eventoService.getEventos();
}
```

---

## 💻 Contenido Práctico

### 6. Ejercicio Resuelto: EventoStore con Signals y RxJS

```typescript
// services/evento.store.ts
import { Injectable, inject, signal, computed, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { toObservable, toSignal } from '@angular/core/rxjs-interop';
import { Observable, catchError, of, tap, BehaviorSubject } from 'rxjs';

export interface Evento {
  id: number;
  titulo: string;
  descripcion: string;
  fecha: string;
  precio: number;
  categoria: string;
  imagen: string;
}

export interface Filtros {
  categoria: string;
  busqueda: string;
  ordenarPor: string;
}

@Injectable({ providedIn: 'root' })
export class EventoStore {
  private http = inject(HttpClient);
  private apiUrl = '/api/eventos';
  
  // State signals
  private _eventos = signal<Evento[]>([]);
  private _cargando = signal(false);
  private _error = signal<string | null>(null);
  private _filtros = signal<Filtros>({
    categoria: 'todas',
    busqueda: '',
    ordenarPor: 'fecha'
  });
  
  // Readonly signals
  readonly eventos = this._eventos.asReadonly();
  readonly cargando = this._cargando.asReadonly();
  readonly error = this._error.asReadonly();
  readonly filtros = this._filtros.asReadonly();
  
  // Computed signals
  readonly eventosFiltrados = computed(() => {
    let resultado = [...this._eventos()];
    const filtros = this._filtros();
    
    if (filtros.busqueda) {
      const texto = filtros.busqueda.toLowerCase();
      resultado = resultado.filter(e => 
        e.titulo.toLowerCase().includes(texto)
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
      catchError(error => {
        this._error.set(error.message);
        return of([]);
      })
    ).subscribe(eventos => {
      this._eventos.set(eventos);
      this._cargando.set(false);
    });
  }
  
  fetchEventoPorId(id: number): Observable<Evento | undefined> {
    return this.http.get<Evento>(`${this.apiUrl}/${id}`).pipe(
      tap(evento => this._eventos.update(e => [...e, evento])),
      catchError(error => {
        this._error.set(error.message);
        return of(undefined);
      })
    );
  }
  
  crearEvento(evento: Partial<Evento>): Observable<Evento | null> {
    this._cargando.set(true);
    
    return this.http.post<Evento>(this.apiUrl, evento).pipe(
      tap(nuevo => {
        this._eventos.update(e => [...e, nuevo]);
        this._cargando.set(false);
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
}
```

```typescript
// Componente usando el store
@Component({
  selector: 'app-eventos',
  standalone: true,
  imports: [CommonModule, EventoCardComponent, NgFor, NgIf],
  template: `
    <div class="filtros">
      <input
        [value]="store.filtros().busqueda"
        (input)="onBusqueda($event)"
        placeholder="Buscar..."
      />
      
      <select 
        [value]="store.filtros().categoria"
        (change)="onCategoria($event)"
      >
        <option 
          *ngFor="let cat of store.categorias()" 
          [value]="cat"
        >
          {{ cat === 'todas' ? 'Todas' : cat }}
        </option>
      </select>
    </div>
    
    <div *ngIf="store.cargando()">Cargando...</div>
    
    <div *ngIf="store.error() as error" class="error">
      {{ error }}
    </div>
    
    <app-evento-card
      *ngFor="let evento of store.eventosFiltrados()"
      [evento]="evento"
    />
    
    <p *ngIf="store.eventosFiltrados().length === 0">
      No hay eventos
    </p>
  `
})
export class EventosComponent {
  store = inject(EventoStore);
  
  constructor() {
    this.store.fetchEventos();
  }
  
  onBusqueda(event: Event): void {
    const value = (event.target as HTMLInputElement).value;
    this.store.setFiltros({ busqueda: value });
  }
  
  onCategoria(event: Event): void {
    const value = (event.target as HTMLSelectElement).value;
    this.store.setFiltros({ categoria: value });
  }
}
```

---

## 🛠️ Ejercicios Prácticos

### Ejercicio 1: RxJS Operators
- map, filter, reduce con pipe

### Ejercicio 2: HTTP con RxJS
- CRUD completo con operadores

### Ejercicio 3: Signals
- Convertir service a signals

### Ejercicio 4: Async Pipe
- Eliminar subscripciones manuales

---

## 🚀 Proyecto de la Clase

### Estado con Signals y RxJS

```typescript
// stores/auth.store.ts
import { Injectable, inject, signal, computed } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { tap } from 'rxjs/operators';

@Injectable({ providedIn: 'root' })
export class AuthStore {
  private http = inject(HttpClient);
  
  // State
  private _usuario = signal<any>(null);
  private _token = signal<string | null>(null);
  
  // Getters
  readonly usuario = this._usuario.asReadonly();
  readonly token = this._token.asReadonly();
  readonly isAuthenticated = computed(() => !!this._token());
  readonly isAdmin = computed(() => this._usuario()?.rol === 'admin');
  
  login(email: string, password: string): any {
    return this.http.post<any>('/api/auth/login', { email, password }).pipe(
      tap(response => {
        this._token.set(response.token);
        this._usuario.set(response.usuario);
      })
    );
  }
  
  logout(): void {
    this._token.set(null);
    this._usuario.set(null);
  }
}
```

### Entregables

1. **RxJS operators** completos
2. **HTTP service** con manejo de errores
3. **Signals** para estado
4. **Store** con signals y computed
5. **Async pipe** en templates

---

## 📚 Recursos Adicionales

- [RxJS Docs](https://rxjs.dev/)
- [Angular Signals](https://angular.io/guide/signals)
- [HttpClient](https://angular.io/guide/http)
