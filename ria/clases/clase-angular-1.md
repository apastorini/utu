Angular no es solo "una librería" como React. Angular es una plataforma completa que te da todas las herramientas (enrutamiento, formularios, peticiones HTTP) listas para usar.

🛑 Paso 0: Los Cimientos
Antes de escribir tu primera línea de código, necesitas preparar tu ambiente. Angular requiere un entorno de ejecución específico.

## Requisitos Técnicos
Node.js: Es el motor que permite ejecutar JavaScript fuera del navegador y gestionar paquetes. Necesitas la versión LTS (Long Term Support).

TypeScript: Angular no usa JavaScript puro por defecto; usa TypeScript. Es como el JavaScript "con superpoderes" que añade tipos de datos para evitar errores.

Angular CLI: Es la herramienta de línea de comandos que hará el trabajo sucio por ti (crear archivos, arrancar el servidor, etc.).

## Instalación
Abre tu terminal y ejecuta este comando para instalar la herramienta principal:
npm install -g @angular/cli

## 🏗️ La Arquitectura: 
Cada pieza es un Componente.

Un componente en Angular siempre se divide en tres partes fundamentales:

El archivo HTML: El esqueleto (la vista).

El archivo CSS: El estilo (la estética).

El archivo TypeScript: El cerebro (la lógica y los datos).

## 🚀  "Hola Mundo"


Crea el proyecto: ng new mi-primer-app
(Dile que sí a todo lo que te pregunte por ahora).

Entra a la carpeta: cd mi-primer-app

Levanta el servidor: ng serve -o

Esto abrirá una pestaña en tu navegador en http://localhost:4200. Verás la página de bienvenida de Angular.


## Anatomía de un Componente
Si abres tu proyecto en un editor (como VS Code), verás muchas carpetas. Buscar src/app. Allí encontrarás el componente principal: AppComponent.

Un componente no es más que una clase de TypeScript decorada con @Component. Dónde el esquema es:

Selector: Es el nombre de la "etiqueta HTML" personalizada (ej: <app-root>).

TemplateUrl: El archivo HTML que este componente controla.

StyleUrls: Los archivos de estilo que solo afectan a este componente.

## 🔗 Data Binding: 
El Data Binding es la forma en que pasamos información desde el código (TypeScript) hacia lo que el usuario ve (HTML). 

1. Interpolación {{ }}
Sirve para mostrar valores del TypeScript en el HTML.

En app.component.ts:

TypeScript
export class AppComponent {
  title = 'Mi curso de Angular';
  usuario = 'Programador Pro';
}
En app.component.html:

HTML
<h1>Bienvenido a {{ title }}</h1>
<p>Hola, {{ usuario }}</p>
2. Property Binding [ ]
Sirve para controlar las propiedades de los elementos HTML (como el src de una imagen o si un botón está desactivado).

En el HTML:

HTML
<button [disabled]="isButtonDisabled">Hacer clic</button>
(Si en el TS defines isButtonDisabled = true;, el botón no se podrá presionar).

##⚡ Event Binding: Escuchando al Usuario ( )
Para que tu app sea interactiva, necesitas reaccionar a lo que hace el usuario. Usamos paréntesis para "escuchar" eventos.

En el HTML:

HTML
<button (click)="saludar()">¡Haz clic aquí!</button>
En el TypeScript:

TypeScript
saludar() {
  alert('¡Hola desde Angular!');
}


## 🛠️ Tu Reto de hoy
 Quiero que hagas lo siguiente:

Borra todo el contenido de app.component.html.

Crea una variable llamada contador que empiece en 0.

Muestra ese contador en el HTML usando Interpolación.

Crea dos botones: uno para sumar 1 y otro para restar 1 usando Event Binding.


## 🕒 Paso 1: Configurar el "Cerebro" (TypeScript)
Abre el archivo src/app/app.component.ts. Vamos a limpiar lo que viene por defecto y definir nuestra lógica.

Copia y pega este código:

TypeScript
import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  standalone: true, // Angular moderno usa componentes standalone
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  // 1. Definimos la variable (propiedad)
  contador: number = 0;

  // 2. Definimos los métodos (funciones)
  incrementar() {
    this.contador++;
  }

  decrementar() {
    if (this.contador > 0) {
      this.contador--;
    }
  }

  resetear() {
    this.contador = 0;
  }
}


## 🎨 Paso 2: 
Ahora abre src/app/app.component.html. Borra todo lo que haya (probablemente el código de bienvenida de Angular) y pega esto:

HTML
<div style="text-align: center; margin-top: 50px; font-family: sans-serif;">
  <h1>Mi Primer Contador en Angular</h1>

  <h2 [style.color]="contador > 10 ? 'green' : 'black'">
    Valor actual: {{ contador }}
  </h2>

  <hr />

  <button (click)="incrementar()" style="padding: 10px 20px; cursor: pointer;">
    Sumar +1
  </button>

  <button (click)="decrementar()" style="padding: 10px 20px; cursor: pointer; margin-left: 10px;">
    Restar -1
  </button>

  <br><br>

  <button (click)="resetear()" style="background-color: #ff4d4d; color: white; border: none; padding: 5px 15px; border-radius: 5px; cursor: pointer;">
    Resetear contador
  </button>

  <p *ngIf="contador === 0">El contador está en el inicio.</p>
</div>


## 🧐 ¿Qué acabamos de hacer? 
Tipado de datos: En el TS pusimos contador: number = 0. TypeScript nos asegura que nadie intente meter un texto ahí por accidente.

this.contador: Dentro de la clase, siempre usamos this para referirnos a las variables que definimos arriba.

Directiva de seguridad: En el método decrementar, añadí un if para que no baje de cero (a menos que tú quieras números negativos).

Estilo dinámico: En el HTML puse [style.color]. Eso es Property Binding. Si el contador pasa de 10, el número se pondrá verde automáticamente.

✅ Verificación
Si tu terminal sigue ejecutando ng serve, guarda los archivos y ve al navegador. Deberías ver tus botones funcionando y el número actualizándose al instante sin recargar la página.


🛠️ Lección 2: Listas y Condicionales (*ngFor y *ngIf)
Imagina que queremos crear una lista de tareas (To-Do List). Vamos a construirla paso a paso.

Paso 1: Definir los datos en el TS
Abre src/app/app.component.ts. Vamos a crear un arreglo de objetos. Borra lo anterior y pega esto:

TypeScript
import { Component } from '@angular/core';
import { CommonModule } from '@angular/common'; // IMPORTANTE: Necesario para usar directivas

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule], // Debes agregar CommonModule aquí para que funcionen *ngIf y *ngFor
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  // Creamos una lista de objetos
  tareas = [
    { id: 1, nombre: 'Aprender Angular', completada: true },
    { id: 2, nombre: 'Instalar el CLI', completada: true },
    { id: 3, nombre: 'Dominar las directivas', completada: false },
    { id: 4, nombre: 'Hacer un deploy', completada: false }
  ];

  // Variable para mostrar/ocultar la lista
  mostrarLista: boolean = true;

  toggleLista() {
    this.mostrarLista = !this.mostrarLista;
  }
}
Paso 2: Mostrar la lista en HTML
Abre src/app/app.component.html. Vamos a usar *ngFor para repetir elementos y *ngIf para decidir si se ven.

Copia y pega este código:

HTML
<div style="padding: 20px; font-family: Arial, sans-serif;">
  <h2>Mis Tareas Pendientes</h2>

  <button (click)="toggleLista()">
    {{ mostrarLista ? 'Ocultar Lista' : 'Mostrar Lista' }}
  </button>

  <hr>

  <div *ngIf="mostrarLista; else mensajeOculto">
    
    <ul>
      <li *ngFor="let t of tareas" style="margin-bottom: 10px;">
        
        <strong [style.color]="t.completada ? 'green' : 'red'">
          {{ t.nombre }}
        </strong>

        <span *ngIf="t.completada"> ✅ (Terminada)</span>
        <span *ngIf="!t.completada"> ⏳ (En proceso)</span>
        
      </li>
    </ul>

  </div>

  <ng-template #mensajeOculto>
    <p style="color: gray; font-style: italic;">La lista está oculta por el usuario.</p>
  </ng-template>

</div>
🧐 ¿Qué acaba de pasar aquí? 
*ngFor="let t of tareas": Angular toma el elemento <li> y lo clona tantas veces como objetos haya en tu arreglo tareas. La t representa a cada tarea individual en cada vuelta del ciclo.

*ngIf="mostrarLista": Si la variable es false, Angular no solo "esconde" el HTML con CSS, sino que lo elimina físicamente del DOM, lo que ahorra memoria.

else mensajeOculto: Es la forma elegante de Angular de decir: "Si no se cumple la condición, muestra este otro bloque de código que etiqueté con #mensajeOculto".

CommonModule: En las versiones más nuevas de Angular (Angular 17+), si usas componentes "Standalone", tienes que avisarle al componente que vas a usar estas herramientas básicas importando el CommonModule.

✅ Verificación
Guarda los cambios. Ahora deberías ver una lista de tareas con colores (verde si está completada, rojo si no) y un botón que hace aparecer y desaparecer toda la sección.


## Lección 3: Formularios y [(ngModel)]
Vamos a añadir la capacidad de agregar nuevas tareas a nuestra lista anterior.

Paso 1: Importar FormsModule
Para que Angular entienda el "Two-Way Binding", necesitamos un módulo especial. Abre src/app/app.component.ts y actualiza la sección de imports.

Copia y pega este bloque de código (sustituyendo el anterior):

TypeScript
import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms'; // <-- 1. IMPORTANTE: Agregamos esto

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule], // <-- 2. Lo declaramos aquí
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  tareas = [
    { id: 1, nombre: 'Aprender Angular', completada: true },
    { id: 2, nombre: 'Dominar las directivas', completada: false }
  ];

  // Variable que estará "atada" al cuadro de texto (input)
  nuevaTareaNombre: string = '';

  // Método para añadir la tarea al arreglo
  agregarTarea() {
    if (this.nuevaTareaNombre.trim() !== '') {
      const nueva = {
        id: this.tareas.length + 1,
        nombre: this.nuevaTareaNombre,
        completada: false
      };
      
      this.tareas.push(nueva); // Añadimos al array
      this.nuevaTareaNombre = ''; // Limpiamos el input
    }
  }

  // Método para borrar una tarea (extra para practicar)
  eliminarTarea(id: number) {
    this.tareas = this.tareas.filter(t => t.id !== id);
  }
}
Paso 2: El HTML con [(ngModel)]
Abre src/app/app.component.html. Vamos a añadir un campo de entrada y un botón arriba de nuestra lista.

Copia y pega este código:

HTML
<div style="padding: 20px; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; max-width: 400px;">
  <h2>Mi Lista de Tareas Pro</h2>

  <div style="margin-bottom: 20px; background: #f4f4f4; padding: 15px; border-radius: 8px;">
    <label>Nueva Tarea:</label><br>
    
    <input 
      [(ngModel)]="nuevaTareaNombre" 
      placeholder="Ej. Comprar leche..."
      style="padding: 8px; width: 70%;"
    >
    
    <button (click)="agregarTarea()" style="padding: 8px; margin-left: 5px; background-color: #007bff; color: white; border: none; cursor: pointer;">
      Añadir
    </button>
    
    <p style="font-size: 0.8em; color: gray;">Escribiendo: {{ nuevaTareaNombre }}</p>
  </div>

  <hr>

  <ul style="list-style: none; padding: 0;">
    <li *ngFor="let t of tareas" style="display: flex; justify-content: space-between; margin-bottom: 10px; border-bottom: 1px solid #eee; padding-bottom: 5px;">
      
      <span [style.textDecoration]="t.completada ? 'line-through' : 'none'">
        <input type="checkbox" [(ngModel)]="t.completada"> {{ t.nombre }}
      </span>

      <button (click)="eliminarTarea(t.id)" style="background: none; border: none; color: red; cursor: pointer;">
        ❌
      </button>

    </li>
  </ul>

  <p *ngIf="tareas.length === 0" style="color: orange;">¡Felicidades! No tienes tareas pendientes.</p>
</div>
🧐 ¿Cómo funciona ? 
[(ngModel)]: Se le llama coloquialmente "Banana in a box" (la banana () dentro de la caja []).

[] significa que el dato va del Código al HTML.

() significa que el dato va del HTML al Código (cuando el usuario escribe).

Juntos hacen que ambos estén siempre sincronizados.

push(): Al ser un arreglo de JavaScript normal, cuando añadimos un objeto, Angular detecta el cambio y redibuja automáticamente el *ngFor. No tienes que hacer nada más.

Checkbox dinámico: Fíjate que en el checkbox también usamos [(ngModel)]="t.completada". Si marcas el cuadro, la propiedad completada del objeto cambia a true automáticamente.

✅ Verificación
Guarda todo. Ahora en tu navegador deberías poder:

Escribir en el cuadro (verás como el texto de abajo cambia al mismo tiempo).

Hacer clic en "Añadir" y ver cómo aparece en la lista de abajo.

Marcar tareas como completadas (se tacharán solas).

Borrar tareas con la "X".


## Lección 4: Componentes Padre e Hijo (@Input y @Output)
Imagina que el AppComponent es el Jefe (Padre) y vamos a crear un componente llamado TareaComponent que es el Empleado (Hijo).

Paso 1: Crear el nuevo componente
En tu terminal (dentro de la carpeta del proyecto), escribe:
ng generate component tarea
(Esto creará una carpeta llamada tarea con sus 4 archivos).

Paso 2: Configurar al "Hijo" (tarea.component.ts)
El hijo necesita dos cosas: recibir una tarea (@Input) y avisar al padre cuando alguien quiera borrarla (@Output).

Abre src/app/tarea/tarea.component.ts y pega esto:

TypeScript
import { Component, Input, Output, EventEmitter } from '@angular/common';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-tarea', // Esta es la etiqueta que usaremos en el HTML del padre
  standalone: true,
  imports: [CommonModule],
  templateUrl: './tarea.component.html'
})
export class TareaComponent {
  // @Input permite que el padre nos envíe datos
  @Input() infoTarea: any;

  // @Output permite enviar mensajes (eventos) al padre
  @Output() borrarEvento = new EventEmitter<number>();

  notificarBorrado() {
    // Emitimos el ID de la tarea hacia arriba
    this.borrarEvento.emit(this.infoTarea.id);
  }
}
Paso 3: El HTML del "Hijo" (tarea.component.html)
Abre src/app/tarea/tarea.component.html y pega esto:

HTML
<div style="border: 1px solid #ddd; padding: 10px; margin: 5px; border-radius: 5px; display: flex; justify-content: space-between; background-color: #fff;">
  
  <span>
    <strong [style.textDecoration]="infoTarea.completada ? 'line-through' : 'none'">
      {{ infoTarea.nombre }}
    </strong>
  </span>

  <button (click)="notificarBorrado()" style="color: red; border: none; background: none; cursor: pointer;">
    Eliminar Componente
  </button>
</div>
Paso 4: Conectar al "Padre" (app.component.ts)
Ahora debemos decirle al padre que use este nuevo componente. Abre src/app/app.component.ts.

Importa el TareaComponent.

Agrégalo a la lista de imports.

TypeScript
import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { TareaComponent } from './tarea/tarea.component'; // <-- 1. Importar

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule, TareaComponent], // <-- 2. Registrar
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  tareas = [
    { id: 1, nombre: 'Aprender Input/Output', completada: false },
    { id: 2, nombre: 'Componentes Standalone', completada: true }
  ];

  eliminarTareaPadre(id: number) {
    this.tareas = this.tareas.filter(t => t.id !== id);
  }
}
Paso 5: El HTML del "Padre" (app.component.html)
Finalmente, usa la etiqueta del hijo dentro del *ngFor. Borra la lista anterior y pon esto:

HTML
<div style="padding: 20px;">
  <h1>Gestor de Proyectos</h1>
  
  <app-tarea 
    *ngFor="let t of tareas" 
    [infoTarea]="t"
    (borrarEvento)="eliminarTareaPadre($event)">
  </app-tarea>

</div>
🧐 ¿Por qué hicimos esto? 
Si mañana quieres que las tareas tengan fotos, fechas o prioridades, solo editas un archivo (tarea.component.html) y todos los lugares donde se use se actualizarán. El AppComponent ahora está más limpio porque no le importa cómo se dibuja una tarea, solo le importa la lista de datos.

## Lección 5: Servicios y RxJS Básico
Paso 1: Crear el Servicio
En tu terminal, ejecuta:
ng generate service tarea
(Esto creará tarea.service.ts en tu carpeta src/app).

Paso 2: Programar la "Central de Datos" (tarea.service.ts)
Abre el archivo y vamos a centralizar la lista de tareas allí.

Copia y pega este código:

TypeScript
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root' // Esto hace que el servicio esté disponible en toda la app
})
export class TareaService {
  // Centralizamos los datos aquí
  private listaTareas = [
    { id: 1, nombre: 'Aprender Servicios', completada: false },
    { id: 2, nombre: 'Entender la Inyección', completada: false }
  ];

  constructor() { }

  // Método para obtener tareas
  getTareas() {
    return this.listaTareas;
  }

  // Método para agregar
  agregarTarea(nombre: string) {
    const nueva = { id: Date.now(), nombre, completada: false };
    this.listaTareas.push(nueva);
  }

  // Método para eliminar
  eliminarTarea(id: number) {
    this.listaTareas = this.listaTareas.filter(t => t.id !== id);
    return this.listaTareas; // Retornamos la lista actualizada
  }
}
Paso 3: "Inyectar" el servicio en el Padre (app.component.ts)
Ahora el AppComponent ya no creará los datos, se los pedirá al TareaService.

Actualiza tu app.component.ts así:

TypeScript
import { Component, OnInit } from '@angular/core'; // Importamos OnInit
import { CommonModule } from '@angular/common';
import { TareaComponent } from './tarea/tarea.component';
import { TareaService } from './tarea.service'; // 1. Importar el servicio

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, TareaComponent],
  templateUrl: './app.component.html'
})
export class AppComponent implements OnInit {
  misTareas: any[] = [];

  // 2. Inyectar el servicio en el constructor
  constructor(private tareaService: TareaService) {}

  // 3. OnInit se ejecuta cuando el componente "nace"
  ngOnInit() {
    this.misTareas = this.tareaService.getTareas();
  }

  borrarDesdePadre(id: number) {
    this.misTareas = this.tareaService.eliminarTarea(id);
  }
}
🧐 ¿Qué es la Inyección de Dependencias?
Imagina que un componente es un Coche.

Sin Inyección: El coche tiene que fabricar su propio motor (el componente crea sus datos).

Con Inyección: El coche pide un motor a una fábrica externa (el Servicio) y se lo "instalan" en el constructor.

Ventajas de este método:
Compartir datos: Si creas un componente EstadisticasComponent, solo tienes que inyectar el mismo TareaService y tendrá acceso a las mismas tareas.

Orden: La lógica de "cómo se borra" o "cómo se guarda" está en el servicio, no ensuciando el HTML/CSS del componente.

Persistencia: Es el lugar ideal para añadir código que guarde en el localStorage o llame a una API de internet.

✅ Tu siguiente paso
Guarda los archivos. El funcionamiento visual será el mismo, pero ahora tu arquitectura es profesional. Los datos viven en una capa separada.


## 🌍 Lección 6: Peticiones HTTP y Observables
Vamos a usar una API de prueba gratuita llamada JSONPlaceholder para traer tareas reales de internet.

Paso 1: Configurar el Proveedor HTTP
En las versiones modernas de Angular (17+), el cliente HTTP se configura en el archivo src/app/app.config.ts.

Abre src/app/app.config.ts y añade provideHttpClient():

TypeScript
import { ApplicationConfig } from '@angular/core';
import { provideRouter } from '@angular/router';
import { provideHttpClient } from '@angular/common/http'; // <-- 1. Importar

import { routes } from './app.routes';

export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(routes),
    provideHttpClient() // <-- 2. Registrar
  ]
};
Paso 2: Actualizar el Servicio (tarea.service.ts)
Ahora el servicio no usará un arreglo fijo, sino que irá a buscarlo a la web.

Copia y pega este código en src/app/tarea.service.ts:

TypeScript
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http'; // Importar el cliente
import { Observable } from 'rxjs'; // Importar Observable

@Component({
  // ...
})
export class TareaService {
  private apiUrl = 'https://jsonplaceholder.typicode.com/todos?_limit=5';

  constructor(private http: HttpClient) { }

  // Este método devuelve un "paquete que se abrirá después" (Observable)
  getTareasRemotas(): Observable<any[]> {
    return this.http.get<any[]>(this.apiUrl);
  }
}
Paso 3: Consumir los datos en el Componente (app.component.ts)
Aquí es donde ocurre la suscripción. Si no te suscribes, la petición nunca se dispara.

Actualiza tu src/app/app.component.ts así:

TypeScript
import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TareaComponent } from './tarea/tarea.component';
import { TareaService } from './tarea.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, TareaComponent],
  template: `
    <div style="padding: 20px;">
      <h1>Tareas desde la API</h1>
      
      <p *ngIf="misTareas.length === 0">Cargando datos del servidor...</p>

      <app-tarea 
        *ngFor="let t of misTareas" 
        [infoTarea]="t">
      </app-tarea>
    </div>
  `
})
export class AppComponent implements OnInit {
  misTareas: any[] = [];

  constructor(private tareaService: TareaService) {}

  ngOnInit() {
    // Nos "suscribimos" al flujo de datos
    this.tareaService.getTareasRemotas().subscribe({
      next: (datos) => {
        this.misTareas = datos; // Cuando llegan los datos, los guardamos
        console.log('Datos recibidos:', datos);
      },
      error: (err) => {
        console.error('¡Ups! Algo salió mal', err);
      }
    });
  }
}
🧐 ¿Qué acaba de pasar? 
HttpClient: Es el servicio oficial de Angular para hacer GET, POST, PUT y DELETE.

Observable: A diferencia de una Promesa de JavaScript (que solo ocurre una vez), un Observable puede emitir datos varias veces y se puede cancelar. Es el estándar de Angular.

.subscribe(): Es el gatillo. Hasta que no llamas a subscribe, Angular no hace la petición HTTP para ahorrar recursos.

Tipado Dinámico: Fíjate que en el HTML usamos [infoTarea]="t". Como la API devuelve objetos con title y completed, tendrás que ajustar tu tarea.component.html para que use {{ infoTarea.title }} en lugar de nombre.

✅ Verificación
Guarda todo y mira tu navegador. Deberías ver cómo, tras medio segundo de carga, aparecen 5 tareas que vienen directamente de los servidores de JSONPlaceholder.


El Router no recarga la página (como haría un sitio web antiguo), sino que intercambia los componentes en pantalla de forma instantánea.

##🗺️ Lección 7: Enrutamiento (Routing)
Vamos a crear dos "páginas": una para la Lista de Tareas y otra para un Contacto (o cualquier otra sección).

Paso 1: Crear los componentes de las "páginas"
Genera dos componentes nuevos en tu terminal:

ng generate component componentes/inicio

ng generate component componentes/contacto

Paso 2: Configurar las Rutas (app.routes.ts)
Abre el archivo src/app/app.routes.ts. Aquí es donde definimos qué URL corresponde a qué componente.

Copia y pega este código:

TypeScript
import { Routes } from '@angular/router';
import { InicioComponent } from './componentes/inicio/inicio.component';
import { ContactoComponent } from './componentes/contacto/contacto.component';

export const routes: Routes = [
  { path: 'inicio', component: InicioComponent },
  { path: 'contacto', component: ContactoComponent },
  { path: '', redirectTo: '/inicio', pathMatch: 'full' }, // Ruta por defecto
  { path: '**', redirectTo: '/inicio' } // Si el usuario escribe cualquier cosa mal
];
Paso 3: Habilitar el "Espacio de Navegación" (app.component.html)
Ahora, en el AppComponent, debemos quitar la lógica de las tareas y poner un "agujero" donde se cargarán las rutas. También añadiremos un menú de navegación.

Actualiza src/app/app.component.html con esto:

HTML
<nav style="padding: 20px; background: #333; color: white;">
  <a routerLink="/inicio" routerLinkActive="activo" style="color: white; margin-right: 15px;">Inicio</a>
  <a routerLink="/contacto" routerLinkActive="activo" style="color: white;">Contacto</a>
</nav>

<div style="padding: 20px; border: 2px solid #eee; margin-top: 10px;">
  <router-outlet></router-outlet>
</div>

<style>
  .activo { font-weight: bold; text-decoration: underline; color: #00ff00 !important; }
</style>
Paso 4: Asegurar las Importaciones (app.component.ts)
Para que las etiquetas <router-outlet> y routerLink funcionen, el componente padre debe conocerlas.

Asegúrate de que tu src/app/app.component.ts se vea así:

TypeScript
import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet, RouterLink, RouterLinkActive } from '@angular/router'; // <-- Importar estas 3

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, RouterOutlet, RouterLink, RouterLinkActive], // <-- Agregarlas aquí
  templateUrl: './app.component.html'
})
export class AppComponent {
  // El padre queda muy limpio, solo gestiona la estructura general
}
🧐 ¿Qué acabamos de aprender? 
<router-outlet>: Es un marcador de posición. Angular lo ve y dice: "Ok, lo que sea que toque mostrar según la URL, lo pondré justo aquí".

routerLink: Es el sustituto de href. Si usas href, la app se reinicia y pierdes tus variables. Con routerLink, Angular solo cambia el trozo de HTML necesario.

routerLinkActive: Es una maravilla. Le añade una clase CSS (en este caso .activo) al enlace solo cuando estás en esa página. Ideal para menús.

Rutas Comodín (**): Siempre ponla al final. Si el usuario intenta entrar a /perfil-que-no-existe, lo mandamos a inicio automáticamente.

✅ Verificación
Guarda todo. Ahora en tu navegador deberías ver una barra de navegación negra.

Haz clic en "Inicio" y verás el contenido de InicioComponent.

Haz clic en "Contacto" y verás el contenido de ContactoComponent.

¡Fíjate que la página nunca parpadea ni muestra el círculo de carga! Eso es una SPA (Single Page Application).



## 🔍 Lección 8: Parámetros de Ruta (ActivatedRoute)
Paso 1: Crear el componente de Detalle
En tu terminal:
ng generate component componentes/tarea-detalle

Paso 2: Configurar la ruta dinámica (app.routes.ts)
Necesitamos decirle al Router que después de detalle/ vendrá un número o texto variable. Usamos los dos puntos (:).

Actualiza src/app/app.routes.ts:

TypeScript
import { Routes } from '@angular/router';
import { InicioComponent } from './componentes/inicio/inicio.component';
import { TareaDetalleComponent } from './componentes/tarea-detalle/tarea-detalle.component'; // <-- Importar

export const routes: Routes = [
  { path: 'inicio', component: InicioComponent },
  { path: 'detalle/:id', component: TareaDetalleComponent }, // <-- :id es la variable
  { path: '', redirectTo: '/inicio', pathMatch: 'full' }
];
Paso 3: Leer el parámetro en el componente (tarea-detalle.component.ts)
Para saber qué ID puso el usuario en la URL, inyectamos un servicio especial llamado ActivatedRoute.

Copia y pega este código en src/app/componentes/tarea-detalle/tarea-detalle.component.ts:

TypeScript
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router'; // <-- 1. Importar el "lector" de rutas

@Component({
  selector: 'app-tarea-detalle',
  standalone: true,
  template: `
    <div style="padding: 20px; border: 1px solid blue; border-radius: 10px;">
      <h2>Detalle de la Tarea</h2>
      <p style="font-size: 1.2em;">Has solicitado ver la tarea con <strong>ID: {{ idTarea }}</strong></p>
      
      <button routerLink="/inicio" style="margin-top: 10px;">Volver al listado</button>
    </div>
  `
})
export class TareaDetalleComponent implements OnInit {
  idTarea: string | null = '';

  // 2. Inyectamos el servicio ActivatedRoute
  constructor(private route: ActivatedRoute) {}

  ngOnInit() {
    // 3. Capturamos el parámetro 'id' que definimos en las rutas
    this.idTarea = this.route.snapshot.paramMap.get('id');
  }
}
Nota: No olvides importar RouterLink en el decorador @Component si el botón de volver no funciona.

Paso 4: Crear el enlace dinámico (inicio.component.html)
Ahora, en tu lista de tareas (que debería estar en el componente de Inicio), vamos a poner un botón que nos lleve al detalle de cada una.

En el HTML donde tengas tu *ngFor de tareas, añade esto:

HTML
<div *ngFor="let t of tareas" style="margin-bottom: 10px; padding: 5px; background: #f9f9f9;">
  <span>{{ t.title }}</span>
  
  <button [routerLink]="['/detalle', t.id]" style="margin-left: 10px; cursor: pointer;">
    Ver más...
  </button>
</div>
🧐 ¿Qué acaba de pasar?
El Comodín :id: Al poner dos puntos en la ruta, Angular acepta cualquier cosa en esa posición (/detalle/1, /detalle/abc, etc.).

snapshot.paramMap: Es como una "foto" de la URL en el momento exacto en que el componente se cargó. De ahí extraemos el valor de id.

[routerLink]="['/ruta', variable]": Cuando el link es dinámico, lo pasamos como un arreglo. El primer elemento es la ruta fija y el segundo es el valor que queremos inyectar.

✅ Verificación
Ve a tu lista de tareas.

Haz clic en "Ver más..." de la primera tarea (ID 1).

Deberías ver cómo la URL cambia a http://localhost:4200/detalle/1 y el componente te muestra ese mismo número en pantalla.


La importancia de entender el Ciclo de Vida (Lifecycle Hooks) .Un componente de Angular no aparece y desaparece por arte de magia; tiene un "nacimiento", un "crecimiento" (cambios de datos) y un "fin" (cuando navegas a otra ruta). Angular nos da funciones especiales para ejecutar código en esos momentos exactos.


## ⏳ Lección 9: El Ciclo de Vida del Componente
Imagina que tu componente es un actor de teatro:Constructor: El actor se pone el vestuario (se crea la clase).

ngOnInit: El actor sale al escenario (el HTML ya está listo).

ngOnChanges: El actor recibe una nueva instrucción del director (cambia un @Input).

ngOnDestroy: El actor se retira al camerino (el componente se elimina).

Paso 1: Implementar los Hooks (tarea-detalle.component.ts)Vamos a usar el componente de detalle para ver esto en acción. Abre src/app/componentes/tarea-detalle/tarea-detalle.component.ts.Copia y pega este código:TypeScriptimport { Component, OnInit, OnDestroy, OnChanges, SimpleChanges, Input } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-tarea-detalle',
  standalone: true,
  template: `
    <div style="padding: 20px; background: #e3f2fd;">
      <h2>Ciclo de Vida en Acción</h2>
      <p>ID Detectado: <strong>{{ idTarea }}</strong></p>
      <button routerLink="/inicio">Cerrar y destruir componente</button>
    </div>
  `
})
export class TareaDetalleComponent implements OnInit, OnDestroy {
  idTarea: string | null = '';
  intervalo: any;

  constructor(private route: ActivatedRoute) {
    console.log('1. CONSTRUCTOR: Clase creada, pero el HTML aún no existe.');
  }

  ngOnInit() {
    console.log('2. ngOnInit: ¡El componente ya está en pantalla!');
    this.idTarea = this.route.snapshot.paramMap.get('id');

    // Ejemplo: Creamos un contador que corre en segundo plano
    this.intervalo = setInterval(() => {
      console.log('El componente sigue vivo...');
    }, 2000);
  }

  ngOnDestroy() {
    console.log('3. ngOnDestroy: El usuario se fue. Limpiando recursos...');
    // ¡IMPORTANTE! Si no limpiamos el intervalo, seguirá corriendo para siempre
    // consumiendo memoria (Memory Leak).
    clearInterval(this.intervalo);
  }
}


Paso 2: Entender por qué es importante ngOnDestroyMira el código de arriba. Si el usuario entra y sale de la página 10 veces y no usáramos clearInterval, tendrías 10 contadores corriendo al mismo tiempo en la memoria del navegador. Tu app se volvería lenta.
🧐 Los 3 Hooks más usados 
Hook: Cuándo ocurrePara qué se usangOnInitJusto después del constructor.Llamar a APIs, inicializar variables, suscripciones.ngOnChangesCada vez que un @Input cambia.
Reaccionar si el Padre le envía un dato nuevo al Hijo.
ngOnDestroy Justo antes de que el componente muera.Cancelar suscripciones, limpiar Timers, cerrar WebSockets.

🛠️ F12 o Clic derecho -> Inspeccionar -> pestaña Console).Navega a la página de "Detalle". Verás los mensajes de Constructor y ngOnInit.Verás que cada 2 segundos sale el mensaje "El componente sigue vivo...".Haz clic en el botón para volver a "Inicio".Verás el mensaje de ngOnDestroy y, lo más importante, el contador se detendrá.


En Angular, un Pipe (tubería) es una herramienta que toma un dato y lo transforma visualmente sin cambiar el valor original en tu código TypeScript. Imagina que tienes un precio de 100.5. El Pipe lo convertirá en $100.50 para el usuario, pero para tu lógica seguirá siendo un número.

