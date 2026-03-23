🧪 Lección 10: Pipes (Transformación de Datos)
Angular trae varios de fábrica que te ahorran horas de programar formatos de fecha, moneda o texto.

Paso 1: Preparar los datos en el Componente
Vamos a añadir una fecha y un precio a nuestro componente de inicio. Abre src/app/componentes/inicio/inicio.component.ts.

Copia y pega este código (añade estas variables):

TypeScript
export class InicioComponent {
  hoy = new Date(); // Fecha actual
  precioTotal = 1550.75; // Un número decimal
  textoLargo = 'angular es el framework más potente para empresas';
  porcentaje = 0.856;
}
Paso 2: Usar los Pipes en el HTML
La sintaxis es el símbolo de la barra vertical |. Abre src/app/componentes/inicio/inicio.component.html.

Copia y pega este bloque para ver la magia:

HTML
<div style="padding: 20px; font-family: sans-serif; line-height: 1.8;">
  <h2>Transformación con Pipes 🧪</h2>

  <p><strong>Original:</strong> {{ textoLargo }}</p>
  <p><strong>Mayúsculas:</strong> {{ textoLargo | uppercase }}</p>
  <p><strong>Título:</strong> {{ textoLargo | titlecase }}</p>

  <hr>

  <p><strong>Fecha bruta:</strong> {{ hoy }}</p>
  <p><strong>Fecha bonita:</strong> {{ hoy | date:'fullDate' }}</p>
  <p><strong>Solo hora:</strong> {{ hoy | date:'shortTime' }}</p>
  <p><strong>Personalizado:</strong> {{ hoy | date:'dd/MM/yyyy' }}</p>

  <hr>

  <p><strong>Precio:</strong> {{ precioTotal | currency:'USD' }}</p>
  <p><strong>Precio (EUR):</strong> {{ precioTotal | currency:'EUR':'symbol':'1.2-2' }}</p>
  <p><strong>Progreso:</strong> {{ porcentaje | percent }}</p>

  <hr>

  <p><strong>Datos crudos:</strong></p>
  <pre>{{ {nombre: 'Angular', version: 18} | json }}</pre>
</div>
🧐 ¿Por qué usar Pipes? (Detalle Pro)
Internacionalización: El currency detecta automáticamente dónde poner la coma o el punto según el idioma del navegador.

Rendimiento: Angular es muy inteligente; si el dato no cambia, el Pipe no se vuelve a ejecutar.

Encadenamiento: ¡Puedes usar varios a la vez!

Ejemplo: {{ hoy | date:'fullDate' | uppercase }}

🏗️ Bonus: Crea tu propio Pipe (Custom Pipe)
A veces necesitas algo muy específico, como un Pipe que acorte un texto si es muy largo.

Generar: ng generate pipe pipes/acortar

Lógica (acortar.pipe.ts):

TypeScript
transform(value: string, limite: number = 10): string {
  return value.length > limite ? value.substring(0, limite) + '...' : value;
}
Uso: {{ 'Este es un texto muy largo' | acortar:5 }} -> Resultado: Este ...

✅ Verificación
Mira tu navegador. Verás cómo la fecha que antes era un texto ilegible ahora dice algo como "Saturday, March 21, 2026", y los precios tienen su símbolo de moneda correspondiente.



🏗️ El Proyecto Final: CryptoTracker Pro
Paso 1: Generar la estructura
Cierra tu terminal actual y ejecuta estos comandos uno por uno:

ng generate service services/crypto

ng generate component componentes/lista-crypto

ng generate component componentes/detalle-crypto

Paso 2: El Servicio de Datos (HTTP + RxJS)
Usaremos una API real para traer precios de criptomonedas.
Abre src/app/services/crypto.service.ts:

TypeScript
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class CryptoService {
  // API pública de CoinGecko
  private url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=10&page=1';

  constructor(private http: HttpClient) {}

  getCoins(): Observable<any[]> {
    return this.http.get<any[]>(this.url);
  }

  getCoinById(id: string): Observable<any> {
    return this.http.get<any>(`https://api.coingecko.com/api/v3/coins/${id}`);
  }
}
Paso 3: Configurar las Rutas
Abre src/app/app.routes.ts y configura el camino:

TypeScript
import { Routes } from '@angular/router';
import { ListaCryptoComponent } from './componentes/lista-crypto/lista-crypto.component';
import { DetalleCryptoComponent } from './componentes/detalle-crypto/detalle-crypto.component';

export const routes: Routes = [
  { path: 'mercado', component: ListaCryptoComponent },
  { path: 'moneda/:id', component: DetalleCryptoComponent },
  { path: '', redirectTo: '/mercado', pathMatch: 'full' }
];
Paso 4: La Lista de Monedas (Componente Principal)
Abre src/app/componentes/lista-crypto/lista-crypto.component.ts:

TypeScript
import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { CryptoService } from '../../services/crypto.service';

@Component({
  selector: 'app-lista-crypto',
  standalone: true,
  imports: [CommonModule, RouterLink],
  template: `
    <div style="padding: 20px;">
      <h2>📈 Mercado Crypto (Top 10)</h2>
      <table border="1" style="width: 100%; border-collapse: collapse; text-align: left;">
        <thead style="background: #f4f4f4;">
          <tr>
            <th>Moneda</th>
            <th>Precio Actual</th>
            <th>Cambio 24h</th>
            <th>Acción</th>
          </tr>
        </thead>
        <tbody>
          <tr *ngFor="let c of cryptos">
            <td><img [src]="c.image" width="20"> {{ c.name }} ({{ c.symbol | uppercase }})</td>
            <td>{{ c.current_price | currency:'USD' }}</td>
            <td [style.color]="c.price_change_percentage_24h > 0 ? 'green' : 'red'">
              {{ c.price_change_percentage_24h | number:'1.1-2' }}%
            </td>
            <td><button [routerLink]="['/moneda', c.id]">Ver Detalles</button></td>
          </tr>
        </tbody>
      </table>
    </div>
  `
})
export class ListaCryptoComponent implements OnInit {
  cryptos: any[] = [];
  constructor(private cryptoService: CryptoService) {}

  ngOnInit() {
    this.cryptoService.getCoins().subscribe(data => this.cryptos = data);
  }
}
Paso 5: El Detalle de la Moneda (Ciclo de Vida)
Abre src/app/componentes/detalle-crypto/detalle-crypto.component.ts:

TypeScript
import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { CryptoService } from '../../services/crypto.service';

@Component({
  selector: 'app-detalle-crypto',
  standalone: true,
  imports: [CommonModule, RouterLink],
  template: `
    <div *ngIf="moneda" style="padding: 20px; border: 2px solid #333; border-radius: 10px; margin: 20px;">
      <button routerLink="/mercado">⬅ Volver al Mercado</button>
      <h1>{{ moneda.name }} <small>({{ moneda.symbol | uppercase }})</small></h1>
      <p>{{ moneda.description.en | slice:0:300 }}...</p>
      <div style="background: #eee; padding: 15px;">
        <h3>Precio: {{ moneda.market_data.current_price.usd | currency:'USD' }}</h3>
        <p>Ranking de Mercado: #{{ moneda.market_cap_rank }}</p>
      </div>
    </div>
  `
})
export class DetalleCryptoComponent implements OnInit, OnDestroy {
  moneda: any;

  constructor(private route: ActivatedRoute, private cryptoService: CryptoService) {}

  ngOnInit() {
    const id = this.route.snapshot.paramMap.get('id');
    if (id) {
      this.cryptoService.getCoinById(id).subscribe(res => this.moneda = res);
    }
  }

  ngOnDestroy() {
    console.log('Saliendo del detalle de la moneda...');
  }
}
🧐 ¿Qué hemos logrado aquí?
Integración Total: El servicio pide datos reales a una API externa.

Transformación: Usamos currency, uppercase, number y slice (Pipes) para que los datos crudos se vean profesionales.

Navegación: Pasamos el ID de la moneda de la tabla al componente de detalle.

Estado: Usamos *ngIf para esperar a que la API responda antes de intentar dibujar el detalle (evitando errores de "undefined").

✅ Verificación Final
Ve a /mercado. Deberías ver la tabla con los precios reales de Bitcoin, Ethereum, etc.

Haz clic en "Ver Detalles" de cualquiera.

Observa cómo cambia la URL y se carga la descripción de la moneda.

¡Felicidades! Has pasado de no saber nada a construir una SPA (Single Page Application) funcional conectada a una API real.


Nivel 2: Formularios Reactivos.

En el nivel anterior usamos [(ngModel)] (Formularios Template-Driven), que es genial para cosas rápidas. Pero para un Login Profesional o un registro complejo, los expertos usan Reactive Forms. ¿Por qué? Porque te dan el control total de la validación, son más fáciles de testear y son mucho más robustos.

🛡️ Lección 11: Formularios Reactivos y Validaciones
Vamos a construir un formulario de Inicio de Sesión que valide que el email sea correcto y que la contraseña tenga una longitud mínima.

Paso 1: Importar ReactiveFormsModule
Abre src/app/app.component.ts (o el componente donde vayas a trabajar) y añade el módulo necesario.

TypeScript
import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormGroup, FormControl, Validators } from '@angular/forms'; // <-- 1. Importar herramientas

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule], // <-- 2. Registrar aquí
  templateUrl: './app.component.html'
})
export class AppComponent {
  // Aquí definiremos el formulario en el siguiente paso
}
Paso 2: Definir la estructura del Formulario (TS)
En los formularios reactivos, tú creas el objeto del formulario en el código TypeScript y luego lo "vinculas" al HTML.

Copia esto dentro de tu clase AppComponent:

TypeScript
export class AppComponent {
  // Definimos el grupo de controles
  loginForm = new FormGroup({
    // FormControl(valor_inicial, [validaciones])
    email: new FormControl('', [Validators.required, Validators.email]),
    password: new FormControl('', [Validators.required, Validators.minLength(6)])
  });

  enviarDatos() {
    if (this.loginForm.valid) {
      console.log('Datos del formulario:', this.loginForm.value);
      alert('¡Login exitoso! (Mira la consola)');
    } else {
      alert('El formulario contiene errores. Por favor, revísalo.');
    }
  }

  // Helper para detectar errores en el HTML más fácil
  get f() { return this.loginForm.controls; }
}
Paso 3: Vincular con el HTML
Abre tu app.component.html. Aquí usamos formGroup para conectar el objeto y formControlName para cada campo.

Copia y pega este código:

HTML
<div style="max-width: 300px; margin: 50px auto; padding: 20px; border: 1px solid #ccc; border-radius: 8px; font-family: Arial;">
  <h2 style="text-align: center;">Login Pro</h2>

  <form [formGroup]="loginForm" (ngSubmit)="enviarDatos()">
    
    <div style="margin-bottom: 15px;">
      <label>Email:</label><br>
      <input type="email" formControlName="email" style="width: 100%; padding: 8px;">
      
      <small *ngIf="f.email.touched && f.email.errors?.['required']" style="color: red;">El email es obligatorio.</small>
      <small *ngIf="f.email.touched && f.email.errors?.['email']" style="color: red;">Formato de email inválido.</small>
    </div>

    <div style="margin-bottom: 15px;">
      <label>Contraseña:</label><br>
      <input type="password" formControlName="password" style="width: 100%; padding: 8px;">
      
      <small *ngIf="f.password.touched && f.password.errors?.['minlength']" style="color: red;">Mínimo 6 caracteres.</small>
    </div>

    <button type="submit" [disabled]="loginForm.invalid" 
            style="width: 100%; padding: 10px; background-color: #007bff; color: white; border: none; cursor: pointer;">
      Entrar
    </button>

  </form>

  <p style="font-size: 0.8em; margin-top: 10px;">Estado del Form: {{ loginForm.status }}</p>
</div>
🧐 ¿Por qué esto es mejor? (Explicación técnica)
Sincronización: El objeto loginForm en el TS es la "fuente de la verdad". Si cambias un valor ahí, el HTML cambia; si el usuario escribe, el objeto se actualiza.

Validadores (Validators): Angular ya trae funciones para casi todo (email, requeridos, patrones de texto, números máximos).

Estado Detallado: Cada campo tiene propiedades como:

touched: ¿El usuario hizo clic y salió del campo? (Ideal para no mostrar errores antes de tiempo).

dirty: ¿El usuario ha escrito algo?

valid: ¿Pasa todas las reglas?

✅ Verificación
Intenta darle al botón sin escribir nada. Verás que no puedes (está desactivado).

Escribe un email mal formado (sin el @). Verás que aparece el error.

Escribe una contraseña de 3 letras. Verás el error de longitud.

Cuando todo esté correcto, el botón se activará y podrás ver los datos en la consola.


🛠️ Lección 12: Validaciones Personalizadas (Custom Validators)
Vamos a crear una función que prohíba palabras específicas en nuestro formulario de registro.

Paso 1: Crear la función de validación (TS)
Abre tu app.component.ts. Fuera de la clase (o como un método estático), vamos a definir nuestra regla.

Copia y pega este código antes de tu @Component:

TypeScript
import { AbstractControl, ValidationErrors, ValidatorFn } from '@angular/forms';

// Esta función devuelve otra función que Angular usará para validar
export function prohibidoNombre(nombreProhibido: string): ValidatorFn {
  return (control: AbstractControl): ValidationErrors | null => {
    // Si el valor del input incluye la palabra prohibida...
    const esProhibido = control.value.toLowerCase().includes(nombreProhibido.toLowerCase());
    
    // Si es prohibido, devolvemos un objeto con el error. Si no, devolvemos null.
    return esProhibido ? { 'nombreInvalido': { value: control.value } } : null;
  };
}
Paso 2: Aplicar el validador al Formulario
Ahora vamos a añadir un campo "username" a nuestro FormGroup y le aplicaremos nuestra nueva regla.

Actualiza el loginForm en tu app.component.ts:

TypeScript
export class AppComponent {
  loginForm = new FormGroup({
    // Aplicamos nuestro validador personalizado 'prohibidoNombre'
    username: new FormControl('', [
      Validators.required, 
      prohibidoNombre('admin'), // 🚩 No dejamos que se llame admin
      prohibidoNombre('root')   // 🚩 Ni tampoco root
    ]),
    email: new FormControl('', [Validators.required, Validators.email]),
    password: new FormControl('', [Validators.required, Validators.minLength(6)])
  });

  get f() { return this.loginForm.controls; }
}
Paso 3: Mostrar el error específico en el HTML
Abre app.component.html y añade el nuevo campo de texto con su mensaje de error personalizado.

Copia y añade esto antes del campo email:

HTML
<div style="margin-bottom: 15px;">
  <label>Nombre de Usuario:</label><br>
  <input type="text" formControlName="username" style="width: 100%; padding: 8px;">
  
  <small *ngIf="f.username.touched && f.username.errors?.['nombreInvalido']" style="color: darkorange;">
    ⚠️ El nombre "{{ f.username.errors?.['nombreInvalido'].value }}" no está permitido por seguridad.
  </small>
</div>
🧐 ¿Cómo funciona por dentro?
AbstractControl: Es el objeto que representa el input. Tiene el valor, el estado y los errores.

ValidationErrors | null: Es el contrato de Angular. Si todo está bien, devuelve null. Si hay error, devuelve un objeto (ej: { 'miError': true }).

Flexibilidad: Puedes crear validadores que comparen dos campos (como "Confirmar contraseña") o incluso validadores Asíncronos (que consultan a una base de datos si un email ya existe mientras el usuario escribe).

✅ Verificación del Reto
Escribe "Juan" en el nombre de usuario. Verás que no hay error.

Escribe "Administrador" o "admin".

Verás cómo aparece instantáneamente el mensaje naranja avisando que ese nombre no está permitido.


📮 Lección 13: Enviando datos al Servidor (HTTP POST)
Vamos a simular el registro de un nuevo usuario usando la API de prueba.

Paso 1: Actualizar el Servicio (crypto.service.ts)
Añadiremos un método para enviar el formulario. Abre src/app/services/crypto.service.ts (o el servicio que estés usando).

Copia y pega este método:

TypeScript
// ... imports anteriores
import { HttpClient } from '@angular/common/http';

@Injectable({ providedIn: 'root' })
export class CryptoService {
  private apiPostUrl = 'https://jsonplaceholder.typicode.com/posts';

  constructor(private http: HttpClient) {}

  // Usamos POST para enviar un objeto al servidor
  registrarUsuario(datosUsuario: any): Observable<any> {
    // http.post(url, cuerpo_del_mensaje)
    return this.http.post(this.apiPostUrl, datosUsuario);
  }
}
Paso 2: Conectar el Formulario con el Servicio (app.component.ts)
Ahora, en el método enviarDatos(), llamaremos al servicio en lugar de solo mostrar un console.log.

Actualiza tu clase en app.component.ts:

TypeScript
export class AppComponent {
  // ... tu loginForm y validadores anteriores ...

  constructor(private cryptoService: CryptoService) {}

  enviarDatos() {
    if (this.loginForm.valid) {
      const datosParaEnviar = this.loginForm.value;
      console.log('Enviando a la nube...', datosParaEnviar);

      // Llamamos al método POST del servicio
      this.cryptoService.registrarUsuario(datosParaEnviar).subscribe({
        next: (respuesta) => {
          console.log('✅ Servidor respondió con éxito:', respuesta);
          alert('¡Usuario registrado! ID asignado: ' + respuesta.id);
          this.loginForm.reset(); // Limpiamos el formulario tras el éxito
        },
        error: (err) => {
          console.error('❌ Error en el servidor:', err);
          alert('Hubo un fallo en la conexión.');
        }
      });
    }
  }
}
🧐 ¿Qué está pasando en el cable?
Cuando haces un POST, Angular convierte automáticamente tu objeto de TypeScript en un JSON y le añade los encabezados necesarios (Content-Type: application/json).

Request (Petición): Envías los datos (email, password, etc.).

Processing (Procesamiento): El servidor recibe el JSON, lo guarda en la base de datos y genera un ID.

Response (Respuesta): El servidor te devuelve el objeto creado (a veces con un mensaje de "201 Created").

🛠️ Detalle Pro: Manejo de Estados de Carga
Para que tu app se vea profesional, el botón debería decir "Enviando..." mientras la API responde.

En tu TS:

TypeScript
cargando: boolean = false;

enviarDatos() {
  this.cargando = true; // Empieza la carga
  this.cryptoService.registrarUsuario(this.loginForm.value).subscribe({
    next: (res) => {
       this.cargando = false; // Termina la carga
       // ... resto del código
    }
  });
}
En tu HTML:

HTML
<button type="submit" [disabled]="loginForm.invalid || cargando">
  {{ cargando ? 'Procesando...' : 'Registrar Usuario' }}
</button>
✅ Verificación
Completa el formulario correctamente (sin nombres prohibidos y con email real).

Haz clic en el botón.

Abre la Consola (F12). Verás un objeto que contiene tus datos más un id: 101 (que es el que asigna la API de prueba).


El Nivel 3 trata sobre la optimización y la seguridad. Una aplicación profesional no solo debe funcionar, debe ser rápida y segura.

Hoy empezamos con la revolución más grande de los últimos años en Angular: Signals.

🚦 Lección 14: Angular Signals (El futuro de la Reactividad)
Hasta ahora, cuando cambiabas una variable, Angular tenía que revisar "todo el árbol de componentes" para ver qué había cambiado. Con las Signals, Angular sabe exactamente qué pedacito de HTML debe actualizarse, lo que hace que la app vuele.

Paso 1: Definir una Signal (TS)
Abre src/app/app.component.ts. Vamos a transformar nuestro antiguo contador en una versión ultra-eficiente con Signals.

Copia y pega este código:

TypeScript
import { Component, signal, computed, effect } from '@angular/core'; // <-- Importar herramientas de Signals

@Component({
  selector: 'app-root',
  standalone: true,
  template: `
    <div style="padding: 20px; border: 2px solid #5c2d91; border-radius: 10px;">
      <h1>Signals: Reactividad Pro ⚡</h1>
      
      <p>Contador: <strong>{{ contador() }}</strong></p>
      <p>Doble del contador: <strong>{{ dobleContador() }}</strong></p>

      <button (click)="incrementar()">Incrementar</button>
      <button (click)="resetear()">Resetear</button>

      <div *ngIf="contador() > 10" style="color: green;">
        ¡Has superado las 10 unidades!
      </div>
    </div>
  `
})
export class AppComponent {
  // 1. Definimos la Signal (valor inicial 0)
  contador = signal(0);

  // 2. Signal Computada (se actualiza sola cuando 'contador' cambia)
  dobleContador = computed(() => this.contador() * 2);

  constructor() {
    // 3. Effect: Se ejecuta cada vez que las señales involucradas cambian
    // Ideal para guardar en LocalStorage o analíticas
    effect(() => {
      console.log(`El contador ahora vale: ${this.contador()}`);
    });
  }

  incrementar() {
    // Para actualizar una Signal usamos .update() o .set()
    this.contador.update(valor => valor + 1);
  }

  resetear() {
    this.contador.set(0);
  }
}
🧐 ¿Por qué usar Signals en lugar de variables normales?
Precisión Quirúrgica: Angular ya no tiene que adivinar qué cambió. La Signal le avisa directamente al elemento del DOM.

Valores Computados (computed): Son valores que dependen de otros. Si el contador no cambia, el "dobleContador" no se vuelve a calcular, ahorrando procesador.

Sintaxis Limpia: Fíjate que en el HTML ahora llamamos a la variable como una función: {{ contador() }}. Esto le indica a Angular que debe estar atento a ese valor específico.

🏗️ Paso 2: Signals con Listas (Objetos)
Las Signals no son solo para números. Mira cómo manejarías una lista de tareas:

TypeScript
listaTareas = signal([{ id: 1, nombre: 'Aprender Signals' }]);

agregarTarea(nuevoNombre: string) {
  this.listaTareas.update(tareas => [
    ...tareas, 
    { id: Date.now(), nombre: nuevoNombre }
  ]);
}
✅ Verificación
Abre tu consola del navegador.

Haz clic en el botón Incrementar.

Verás cómo el mensaje del effect aparece instantáneamente y el "Doble" se actualiza sin que tú hagas nada manual.

Un Guard (Guardián) es una pieza de código que se ejecuta antes de que el usuario entre en una ruta.

Imagina que tienes una página de /admin. No quieres que cualquier persona que escriba la URL pueda entrar. El Guard intercepta la navegación, revisa si el usuario tiene permiso (o si está logueado) y decide: "Pasa" o "Te redirijo al Login".

🛡️ Lección 15: Functional Route Guards (canActivate)
En el Angular moderno, los Guards son funciones simples y muy potentes.

Paso 1: Crear el Servicio de Autenticación (Simulado)
Primero necesitamos a alguien que nos diga si el usuario está logueado o no.
Abre src/app/services/auth.service.ts (o créalo):

TypeScript
import { Injectable, signal } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class AuthService {
  // Usamos una Signal para que toda la app sepa el estado de sesión al instante
  isLoggedIn = signal(false);

  login() {
    this.isLoggedIn.set(true);
  }

  logout() {
    this.isLoggedIn.set(false);
  }

  estaAutenticado(): boolean {
    return this.isLoggedIn();
  }
}
Paso 2: Crear el Guardián (auth.guard.ts)
No necesitas un comando especial, es solo una función. Crea un archivo en src/app/guards/auth.guard.ts:

TypeScript
import { inject } from '@angular/core';
import { Router, CanActivateFn } from '@angular/router';
import { AuthService } from '../services/auth.service';

export const authGuard: CanActivateFn = (route, state) => {
  const authService = inject(AuthService); // Inyectamos el servicio
  const router = inject(Router);           // Inyectamos el router para redirigir

  if (authService.estaAutenticado()) {
    console.log('✅ Acceso permitido por el Guard');
    return true; // El usuario puede pasar
  } else {
    console.warn('🚫 Acceso denegado. Redirigiendo...');
    return router.parseUrl('/login'); // Bloqueamos y mandamos al login
  }
};
Paso 3: Aplicar el Guard a las Rutas
Ahora le decimos al Router qué rutas deben estar protegidas por este "portero".
Abre src/app/app.routes.ts:

TypeScript
import { Routes } from '@angular/router';
import { authGuard } from './guards/auth.guard'; // Importar el guard
import { ListaCryptoComponent } from './componentes/lista-crypto/lista-crypto.component';
import { LoginComponent } from './componentes/login/login.component'; // (Imagina que existe)

export const routes: Routes = [
  { path: 'login', component: LoginComponent },
  { 
    path: 'mercado', 
    component: ListaCryptoComponent,
    canActivate: [authGuard] // 🛡️ ¡Aquí está la magia! Solo entran si el guard da el OK
  },
  { path: '', redirectTo: '/mercado', pathMatch: 'full' }
];
🧐 ¿Por qué esto es vital? (Detalle Pro)
Seguridad en el Cliente: Evitas que el usuario vea componentes sensibles sin permiso.

Experiencia de Usuario: Puedes redirigir automáticamente a la página de pago si intentan entrar a contenido Premium sin suscripción.

Múltiples Guards: Puedes poner varios en una sola ruta. Ejemplo: canActivate: [authGuard, adminGuard, pagoAlDiaGuard].

✅ Prueba de Fuego
Intenta entrar a localhost:4200/mercado.

Como isLoggedIn empieza en false, el Guard te debería expulsar automáticamente hacia /login.

Si creas un botón que llame a authService.login(), verás que ahora sí te deja entrar.


El Lazy Loading (Carga Perezosa) es lo que separa una aplicación "de juguete" de una Enterprise Application.

Imagina que tu app tiene 50 páginas. Sin Lazy Loading, cuando el usuario entra a la "Home", el navegador descarga el código de las 50 páginas de golpe. Con Lazy Loading, solo descarga la "Home". Si el usuario nunca entra a "Administración", ese código jamás se descarga, ahorrando datos y tiempo.

⚡ Lección 16: Lazy Loading (Carga bajo demanda)
En Angular moderno, esto se hace directamente en el archivo de rutas de una forma muy elegante.

Paso 1: Cambiar la forma de importar componentes
Abre src/app/app.routes.ts. En lugar de importar los componentes arriba del todo con import { ... }, vamos a cargarlos dinámicamente.

Sustituye tu archivo de rutas por este modelo Pro:

TypeScript
import { Routes } from '@angular/router';
import { authGuard } from './guards/auth.guard';

export const routes: Routes = [
  { 
    path: 'inicio', 
    // 🚀 Aquí está el Lazy Loading: el componente solo se importa cuando entras a la ruta
    loadComponent: () => import('./componentes/inicio/inicio.component')
      .then(m => m.InicioComponent) 
  },
  { 
    path: 'mercado', 
    canActivate: [authGuard],
    loadComponent: () => import('./componentes/lista-crypto/lista-crypto.component')
      .then(m => m.ListaCryptoComponent)
  },
  { 
    path: 'configuracion', 
    loadComponent: () => import('./componentes/config/config.component')
      .then(m => m.ConfigComponent)
  },
  { path: '', redirectTo: '/inicio', pathMatch: 'full' }
];
Paso 2: ¿Cómo verificar que funciona? (El truco del desarrollador)
Abre tu aplicación en el navegador.

Presiona F12 y ve a la pestaña Network (Red).

Filtra por JS.

Recarga la página en /inicio. Verás que se cargan unos pocos archivos.

Ahora, haz clic en el botón para ir a /mercado.

¡Magia! Verás que en ese preciso instante aparece un nuevo archivo .js en la lista. Ese es el código de la página de mercado cargándose justo a tiempo.

🧐 Beneficios del Lazy Loading (Detalle Pro)
Lighthouse Score: Tu puntuación de Google subirá al cielo porque el "Initial Bundle Size" será minúsculo.

Modularidad: Te obliga a tener componentes bien separados.

Ancho de Banda: Los usuarios en móviles con internet lento te lo agradecerán profundamente.

🏗️ Nivel 4: El Toque Final de Diseño (Angular Material)
Para que tu app no parezca de 1995, los profesionales usamos librerías de componentes pre-diseñados. La más famosa es Angular Material (creada por Google).

Tu última misión técnica de hoy:
Instala Angular Material en tu proyecto con este comando en la terminal:
ng add @angular/material

(Elige un tema de color, dile que sí a la tipografía y a las animaciones).

✅ Verificación
Una vez instalado, ¿quieres que te enseñe a usar un Mat-Table (una tabla profesional con buscador y paginación) o prefieres que veamos Interceptors para añadir el token de seguridad a todas tus llamadas a la API automáticamente?


En el mundo empresarial, las tablas son el pan de cada día. Pero nadie quiere una tabla de HTML básica; queremos una que tenga paginación, ordenamiento y un buscador que funcione en tiempo real.

Para esto, Angular Material nos da el componente MatTable. Es un poco más complejo de configurar que una tabla normal, pero el resultado es 100% profesional.

📊 Lección 17: Tablas Profesionales con Angular Material
Vamos a transformar nuestra lista de Criptomonedas en una tabla de alto nivel.

Paso 1: Importar los módulos necesarios
Abre src/app/componentes/lista-crypto/lista-crypto.component.ts. Necesitamos importar varios componentes de Material.

TypeScript
import { Component, OnInit, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatTableModule, MatTableDataSource } from '@angular/material/table'; // Tabla
import { MatPaginatorModule, MatPaginator } from '@angular/material/paginator'; // Paginación
import { MatSortModule, MatSort } from '@angular/material/sort'; // Ordenamiento
import { MatInputModule } from '@angular/material/input'; // Buscador
import { MatFormFieldModule } from '@angular/material/form-field';
import { CryptoService } from '../../services/crypto.service';

@Component({
  selector: 'app-lista-crypto',
  standalone: true,
  imports: [
    CommonModule, 
    MatTableModule, 
    MatPaginatorModule, 
    MatSortModule, 
    MatInputModule, 
    MatFormFieldModule
  ],
  templateUrl: './lista-crypto.component.html'
})
export class ListaCryptoComponent implements OnInit {
  // 1. Definimos las columnas que queremos mostrar
  columnasVisibles: string[] = ['image', 'name', 'symbol', 'price'];
  
  // 2. Fuente de datos especial de Material
  dataSource = new MatTableDataSource<any>([]);

  // 3. Referencias a los componentes de la vista
  @ViewChild(MatPaginator) paginator!: MatPaginator;
  @ViewChild(MatSort) sort!: MatSort;

  constructor(private cryptoService: CryptoService) {}

  ngOnInit() {
    this.cryptoService.getCoins().subscribe(data => {
      this.dataSource.data = data;
      this.dataSource.paginator = this.paginator;
      this.dataSource.sort = this.sort;
    });
  }

  // 4. Función para el buscador
  aplicarFiltro(event: Event) {
    const filtro = (event.target as HTMLInputElement).value;
    this.dataSource.filter = filtro.trim().toLowerCase();
  }
}
Paso 2: El HTML de la Tabla Pro
Abre src/app/componentes/lista-crypto/lista-crypto.component.html. Aquí es donde ocurre la magia de las directivas de Material.

HTML
<div style="padding: 20px;">
  
  <mat-form-field appearance="outline" style="width: 100%;">
    <mat-label>Buscar moneda...</mat-label>
    <input matInput (keyup)="aplicarFiltro($event)" placeholder="Ej. Bitcoin">
  </mat-form-field>

  <div class="mat-elevation-z8">
    <table mat-table [dataSource]="dataSource" matSort>

      <ng-container matColumnDef="image">
        <th mat-header-cell *matHeaderCellDef> Icono </th>
        <td mat-cell *matCellDef="let element"> 
          <img [src]="element.image" width="30"> 
        </td>
      </ng-container>

      <ng-container matColumnDef="name">
        <th mat-header-cell *matHeaderCellDef mat-sort-header> Nombre </th>
        <td mat-cell *matCellDef="let element"> {{element.name}} </td>
      </ng-container>

      <ng-container matColumnDef="symbol">
        <th mat-header-cell *matHeaderCellDef> Símbolo </th>
        <td mat-cell *matCellDef="let element"> {{element.symbol | uppercase}} </td>
      </ng-container>

      <ng-container matColumnDef="price">
        <th mat-header-cell *matHeaderCellDef mat-sort-header> Precio </th>
        <td mat-cell *matCellDef="let element"> {{element.current_price | currency}} </td>
      </ng-container>

      <tr mat-header-row *matHeaderRowDef="columnasVisibles"></tr>
      <tr mat-row *matRowDef="let row; columns: columnasVisibles;"></tr>
    </table>

    <mat-paginator [pageSizeOptions]="[5, 10, 20]" showFirstLastButtons></mat-paginator>
  </div>
</div>
🧐 ¿Qué acabamos de construir? (Detalle Pro)
MatTableDataSource: Es un motor inteligente. No necesitas programar el filtro manualmente; él busca en todas las propiedades del objeto por ti.

mat-sort-header: Al añadir esta directiva a una cabecera, Angular Material habilita automáticamente las flechas para ordenar (A-Z, Mayor-Menor).

@ViewChild: Es la forma en que el TypeScript "agarra" el componente del HTML para decirle: "Oye Paginador, tú vas a controlar esta fuente de datos".

mat-elevation-z8: Es una clase de CSS que viene con Material para darle esa sombra suave y aspecto de "tarjeta" profesional.

✅ Verificación
Escribe en el buscador. Verás cómo la tabla se filtra en tiempo real.

Haz clic en la cabecera "Precio". Verás cómo se ordena de mayor a menor.

Cambia el tamaño de página en el paginador de abajo.

Los Interceptors.

Imagina que tu aplicación tiene 50 llamadas a una API protegida. En cada una, tendrías que añadir manualmente el Token de Sesión (JWT) en las cabeceras. Es aburrido y propenso a errores.

Un Interceptor es como un "peaje" por el que pasan todas las peticiones HTTP. Él se encarga de inyectar el token automáticamente en cada viaje, sin que tú tengas que escribirlo 50 veces.

🛡️ Lección 18: Interceptores HTTP (Seguridad Centralizada)
En Angular 17+ (standalone), los interceptores son funciones ultra-ligeras.

Paso 1: Crear la función del Interceptor
Crea un archivo en src/app/interceptors/auth.interceptor.ts:

TypeScript
import { HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { AuthService } from '../services/auth.service';

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const authService = inject(AuthService);
  const token = 'MI_TOKEN_JWT_SECRET_123'; // Aquí lo pedirías al authService

  console.log('🛰️ Interceptor: Inyectando seguridad a la petición:', req.url);

  // Clonamos la petición original y le añadimos el Header de Authorization
  const authReq = req.clone({
    setHeaders: {
      Authorization: `Bearer ${token}`
    }
  });

  // Enviamos la petición modificada al siguiente paso
  return next(authReq);
};
Paso 2: Registrar el Interceptor en la App
Para que Angular use este "peaje", debemos avisarle en la configuración global. Abre src/app/app.config.ts.

Copia y pega este ajuste en tus providers:

TypeScript
import { ApplicationConfig } from '@angular/core';
import { provideHttpClient, withInterceptors } from '@angular/common/http'; // <-- Importar withInterceptors
import { authInterceptor } from './interceptors/auth.interceptor'; // <-- Importar tu función

export const appConfig: ApplicationConfig = {
  providers: [
    // ... otros providers como provideRouter ...
    provideHttpClient(
      withInterceptors([authInterceptor]) // 🛡️ Activamos el interceptor aquí
    )
  ]
};
🧐 ¿Por qué esto es Nivel Senior?
DRY (Don't Repeat Yourself): Centralizas la seguridad. Si el token cambia de formato, solo editas un archivo.

Manejo de Errores Global: También puedes usar interceptores para detectar si el servidor devuelve un error 401 (No autorizado) y redirigir al usuario al Login automáticamente.

Logs de Auditoría: Puedes medir cuánto tarda cada petición HTTP en completarse desde un solo lugar.

🏁 ¡Felicidades, Graduado! 🎓
Has recorrido el camino completo desde el "Hola Mundo" hasta las arquitecturas profesionales. Repasemos tu arsenal:

Básico: Componentes, Data Binding, Directivas e Inputs/Outputs.

Intermedio: Servicios, HTTP (GET/POST), Routing y Pipes.

Avanzado: Signals, Guards, Lazy Loading, Angular Material e Interceptors.


🏛️ Bloque 1: Arquitectura y Rendimiento
1. ¿Cómo optimizarías el "Initial Bundle Size" de una aplicación Enterprise con +200 componentes?
Respuesta de Arquitecto: No basta con decir "Lazy Loading". Un arquitecto mencionaría:

Lazy Loading de Rutas: Dividir la app en feature-chunks.

Deferrable Views (@defer): La joya de Angular 17. Permite cargar componentes (como pesadas gráficas o mapas) solo cuando entran en el viewport o bajo ciertas condiciones.

Análisis de Bundle: Usar source-map-explorer para identificar librerías pesadas (como Moment.js) y reemplazarlas por alternativas tree-shakable (como date-fns).

Standalone Components: Para eliminar el overhead de los NgModules y permitir un mejor tree-shaking del compilador.

2. Diferencia entre ChangeDetectionStrategy.Default y OnPush. ¿Cuándo usarías cada uno?
Respuesta: Por defecto, Angular revisa todo el árbol si algo cambia (sucio).

OnPush le dice a Angular: "Solo revisa este componente si su @Input cambia de referencia o si un Observable emite un valor con el pipe async".

Decisión de Arquitecto: Implementaría una política de OnPush por defecto en toda la organización para aplicaciones de alta densidad de datos (dashboards), ya que reduce drásticamente los ciclos de renderizado.

🚦 Bloque 2: Reactividad y Estado
3. Signals vs RxJS: ¿Las Signals reemplazan a RxJS?
Respuesta: No. Son herramientas complementarias.

Signals: Son para el Estado Síncrono y la renderización (la vista). Son excelentes para valores que la UI necesita leer ahora mismo.

RxJS: Es para el Estado Asíncrono y flujos de eventos complejos (WebSockets, streams de datos, race conditions con switchMap).

Arquitectura: Usaría RxJS en los servicios para la lógica de datos y transformaría esos Observables a Signals con toSignal() para consumirlos de forma limpia en los componentes.

4. ¿Qué estrategia de Gestión de Estado elegirías: NGRX (Redux), Signals o Servicios con BehaviorSubject?
Respuesta: Depende de la complejidad:

Servicios con Signals/BehaviorSubject: Para apps medianas. Fácil de mantener y poco "boilerplate".

NGRX/NGXS: Para apps masivas con estados muy complejos, donde la trazabilidad (Redux DevTools) y la inmutabilidad estricta son vitales para evitar bugs entre múltiples equipos de desarrollo.

🛡️ Bloque 3: Patrones y Estándares
5. ¿Qué es la "Inyección de Dependencias" (DI) jerárquica y cómo la usarías para proveer diferentes versiones de un servicio?
Respuesta: Angular tiene un sistema de inyectores en árbol.

Si provees un servicio en app.config (root), es una instancia única (Singleton).

Si lo provees a nivel de Componente, cada instancia del componente recibe una instancia nueva del servicio.

Uso real: Útil para crear "Sandboxes" donde un componente hijo necesita una configuración del servicio distinta a la del resto de la app.

6. ¿Cómo manejarías la seguridad JWT en una arquitectura Micro-frontend con Angular?
Respuesta: 1.  Interceptors: Para adjuntar el token automáticamente.
2.  HttpOnly Cookies: Mencionaría que, por seguridad, es preferible a LocalStorage para evitar ataques XSS.
3.  Route Guards: Para control de acceso granular basado en Roles (RBAC).
4.  Refresh Tokens: Implementaría lógica en el Interceptor para detectar el error 401, renovar el token en segundo plano y re-intentar la petición fallida sin que el usuario lo note.

🚀 Pregunta de Bonus (El "Killer"):
"Si tienes una fuga de memoria (Memory Leak) en una app de Angular, ¿dónde buscarías primero?"

Respuesta: Buscaría suscripciones de RxJS que no se han cerrado con unsubscribe() o el operador takeUntil(), especialmente en componentes que se destruyen y recrean mucho. También revisaría setInterval o addEventListener manuales que no se limpian en el ngOnDestroy.


Entrar en el mundo de los Micro-frontends (MFE) con Angular es pasar al siguiente nivel de arquitectura. Es la solución para empresas masivas (como bancos o e-commerce) donde tienes 50+ desarrolladores y no quieres que un error en el "Carrito de Compras" tire abajo toda la aplicación de "Seguros".

La estrategia estándar hoy en día es usar Module Federation (introducido en Webpack 5 y ahora soportado por herramientas como Esbuild).

🏗️ Arquitectura de Micro-frontends en Angular
Un sistema de MFE se divide en dos roles principales:

El Shell (Anfitrión): Es el marco de la aplicación. Contiene el menú, el login y decide qué micro-app cargar según la URL.

Los Remotes (Micro-apps): Son aplicaciones independientes (ej: Pagos, Perfil, Catálogo). Se pueden desplegar por separado, en fechas distintas y por equipos distintos.

🛠️ Guía de Implementación (Paso a Paso)
Para implementar esto de forma profesional, solemos usar la librería @angular-architects/module-federation.

1. Preparar los proyectos
Imagina que tienes un espacio de trabajo con una app "Shell" y una app "Dashboard".

Bash
# Instalamos la utilidad de federación
ng add @angular-architects/module-federation --project shell --port 4200
ng add @angular-architects/module-federation --project dashboard --port 4201
2. Configurar el Remote (Dashboard)
El "Remote" debe decidir qué piezas quiere exponer al mundo. Esto se hace en el archivo webpack.config.js (o en la configuración de federación que genera el comando anterior).

JavaScript
// dashboard/webpack.config.js
const { shareAll, withModuleFederationPlugin } = require('@angular-architects/module-federation/webpack');

module.exports = withModuleFederationPlugin({
  name: 'dashboard',
  exposes: {
    // Exponemos un componente o un set de rutas completo
    './Module': './src/app/dashboard/dashboard.module.ts',
  },
  shared: {
    ...shareAll({ singleton: true, strictVersion: true, requiredVersion: 'auto' }),
  },
});
Nota: El atributo singleton: true es vital para que toda la app use la misma instancia de Angular y de RxJS.

3. Configurar el Shell (Anfitrión)
El Shell debe saber dónde vive el Dashboard. En el archivo de rutas del Shell, cargamos el componente de forma remota:

TypeScript
// shell/src/app/app.routes.ts
import { loadRemoteModule } from '@angular-architects/module-federation';

export const routes: Routes = [
  {
    path: 'dashboard',
    loadChildren: () =>
      loadRemoteModule({
        type: 'module',
        remoteEntry: 'http://localhost:4201/remoteEntry.js', // URL del micro-frontend
        exposedModule: './Module'
      })
      .then(m => m.DashboardModule)
  }
];
🧐 Desafíos de Arquitecto (Lo que te preguntarán)
Como arquitecto, debes tener respuesta para estos 3 problemas críticos:

A. Comunicación entre Micro-frontends
¿Cómo se hablan entre ellos?

Mala práctica: No acoples las apps con servicios compartidos (esto rompe la independencia).

Buena práctica: Usa un Bus de Eventos (CustomEvents del navegador) o el LocalStorage. El Shell puede pasar datos a través de props o parámetros de URL, pero las micro-apps deben ser lo más "agnósticas" posible.

B. Gestión de dependencias (Versioning)
Si el Shell usa Angular 17 y el Remote usa Angular 18, podrías tener problemas.

Estrategia: Forzar versiones singleton en el config de Webpack. Si las versiones son incompatibles, Angular puede descargar ambas (encapsulamiento), pero esto aumenta el peso de la carga.

C. Diseño y Estilos
¿Cómo evitas que el CSS de una app rompa la otra?

Usa Shadow DOM en los componentes o prefijos de CSS únicos (ej: .mfe-dashboard-button). Lo ideal es tener una Librería de Componentes (Design System) compartida como un paquete de NPM privado.

🚀 La "Pregunta de Oro" del Reclutador:
"¿Por qué usarías Micro-frontends en lugar de una Monolito bien estructurado?"

Respuesta de Arquitecto: "No los usaría por rendimiento técnico (porque el overhead es mayor), sino por escalabilidad organizacional. Los uso cuando el equipo es tan grande que el despliegue se convierte en un cuello de botella. Si un equipo puede desplegar su parte sin esperar al resto, ganamos agilidad de negocio."

🔗 Estrategias de Comunicación en Micro-frontends
1. Comunicación mediante la URL (La más limpia)
Es la forma más robusta. Si el Shell necesita decirle al Remote de "Pagos" qué factura cargar, lo hace a través de parámetros de ruta.

Ventaja: Si el usuario refresca la página, el Remote sigue teniendo la información.

Uso: http://mi-app.com/pagos/detalle/5521

2. Custom Events del Navegador (Event Bus)
Como cada micro-app vive en el mismo DOM, podemos usar los eventos nativos de JavaScript. Es ideal para acciones "de fuego y olvido" (ej: "El usuario cerró sesión").

En el Shell (Emisor):

TypeScript
const evento = new CustomEvent('usuario-deslogueado', { detail: { timestamp: Date.now() } });
window.dispatchEvent(evento);
En el Remote (Receptor):

TypeScript
@HostListener('window:usuario-deslogueado', ['$event'])
onLogout(event: any) {
  this.miServicioLocal.limpiarCache();
}
3. Librería de Estado Compartida (Estrategia Pro)
Si realmente necesitas compartir objetos complejos (como el perfil del usuario), creas una librería de Angular aparte (usando Nx Monorepo o un paquete NPM).

🛠️ Implementación de Estado Compartido con Nx
Si usas Nx, puedes crear una librería llamada shared-auth-state que contenga un servicio con Signals.

Shared Library: Contiene el AuthService con una Signal de usuario.

Shell: Inyecta el servicio y hace user.set(datos).

Remote: Inyecta el mismo servicio (gracias a singleton: true en Module Federation) y lee user().

⚠️ Advertencia de Arquitecto: Si un Remote puede modificar el estado del Shell sin control, tendrás bugs imposibles de rastrear. Regla de oro: El Shell es el dueño del estado global; los Remotes son consumidores.

🔥 Pregunta Crítica de Entrevista: Versionado de Dependencias
"¿Qué haces si el Shell usa Angular 18 pero un equipo de un Remote se queda atrás en Angular 17?"

Respuesta de Arquitecto:

Versiones Compartidas (Shared): En el webpack.config, configuramos las dependencias como singleton: true. Si las versiones son compatibles (mismo major), Webpack cargará solo una.

Versiones estrictas: Si son incompatibles y ponemos strictVersion: true, la app fallará al cargar. Esto es preferible a tener errores extraños en tiempo de ejecución.

Encapsulamiento: Si el equipo del Remote no puede actualizar, dejamos de compartir Angular y cada uno carga su propia versión. Esto aumenta el peso de la app (+2MB de JS), pero permite la independencia total.

✅ Resumen para tu entrevista de Arquitecto:
Para triunfar, debes mencionar estos 4 pilares:

Independencia de Despliegue: Cada MFE tiene su propio pipeline de CI/CD.

Singletons: Solo una instancia de Angular/RxJS en memoria.

Shell Agnosticism: El Shell no debe saber cómo funcionan los Remotes por dentro.

Error Handling: Si un Remote falla (404 o error JS), el Shell debe mostrar un "Fallback" elegante y no morir por completo.

Un arquitecto de Angular no ve los errores como "un problema en la consola", sino como un flujo de datos que debe ser capturado, procesado y reportado sin que el usuario pierda la confianza en la aplicación.

En una arquitectura de Micro-frontends (MFE), el manejo de errores es crítico: si un Remote falla, no debe "contagiar" al Shell ni al resto de los Remotes.

🛡️ Estrategia de Gestión de Errores Globales
1. El ErrorHandler Global (Nivel de Aplicación)
Angular provee una clase base llamada ErrorHandler. Por defecto, solo hace un console.error. Un arquitecto la sobrescribe para centralizar el reporte (por ejemplo, enviando el error a Sentry o Azure Application Insights).

Paso 1: Crear el Global Handler

TypeScript
import { ErrorHandler, Injectable } from '@angular/core';

@Injectable()
export class GlobalErrorHandler implements ErrorHandler {
  handleError(error: any): void {
    const chunkFailedMessage = /Loading chunk [\d]+ failed/;

    if (chunkFailedMessage.test(error.message)) {
      // Error típico de MFE: Un remote no está disponible
      console.error('Fallo crítico: No se pudo cargar un módulo remoto.');
      // Aquí podrías forzar una recarga o mostrar un mensaje amigable
    }

    // Reportar a un servicio externo (Sentry, LogRocket, etc.)
    console.error('Error capturado por el Arquitecto:', error);
  }
}
Paso 2: Registrarlo en el Shell (app.config.ts)

TypeScript
providers: [
  { provide: ErrorHandler, useClass: GlobalErrorHandler }
]
2. Error Boundaries en Micro-frontends (El "Aislamiento")
En MFE, el mayor riesgo es que loadRemoteModule falle (porque el servidor del Remote se cayó). Si no manejas esto, el Router de Angular lanzará una excepción y la pantalla quedará en blanco.

Estrategia de Carga Segura:
En lugar de cargar el módulo directamente en las rutas, usa un bloque try/catch o el operador catchError en el loadChildren.

TypeScript
// shell/src/app/app.routes.ts
{
  path: 'pagos',
  loadChildren: () => loadRemoteModule({
    type: 'module',
    remoteEntry: 'http://mfe-pagos.com/remoteEntry.js',
    exposedModule: './Module'
  }).catch(err => {
    console.error('MFE Pagos no disponible', err);
    // Retornamos un componente de "Fallback" o Error interno
    return import('./componentes/error-mfe/error-mfe.component').then(m => m.ErrorMfeComponent);
  })
}
3. Interceptores para Errores HTTP (Nivel de Red)
El Interceptor es el lugar ideal para manejar errores globales de API, como el famoso 401 (No autorizado) o el 500 (Error de servidor).

TypeScript
export const errorInterceptor: HttpInterceptorFn = (req, next) => {
  const router = inject(Router);
  const toast = inject(ToastService); // Un servicio de notificaciones

  return next(req).pipe(
    catchError((error: HttpErrorResponse) => {
      if (error.status === 401) {
        // Token expirado: Redirigir al login
        router.navigate(['/login']);
      } else if (error.status === 503) {
        // Servidor en mantenimiento
        toast.show('El servidor está temporalmente fuera de servicio');
      }
      return throwError(() => error);
    })
  );
};
🧐 Preguntas de Arquitecto para la Entrevista
Q1: "¿Cómo evitarías que un bucle infinito en un Remote bloquee el hilo principal del Shell?"
Respuesta: En JavaScript, al compartir el mismo hilo (Main Thread), es difícil evitar el bloqueo total si el código es síncrono. Sin embargo, como arquitecto recomendaría:

Uso de Web Workers para procesos pesados.

Implementar monitoreo de performance (User Timing API) para detectar qué MFE está consumiendo más tiempo de CPU y "matar" su carga si es necesario.

Q2: "¿Qué es el 'Graceful Degradation' en el contexto de Micro-frontends?"
Respuesta: Es la capacidad de la app de seguir funcionando aunque falten piezas. Si el micro-frontend de "Recomendaciones" falla, el Shell debe simplemente ocultar esa sección o mostrar un banner estático, pero permitir que el usuario siga comprando.

Q3: "¿Cómo manejarías el versionado de errores?"
Respuesta: Añadiría metadatos a cada error (AppID, Version, UserID, Environment). En una arquitectura MFE, es vital saber qué versión de qué micro-app lanzó el error para que el equipo responsable pueda actuar rápido.