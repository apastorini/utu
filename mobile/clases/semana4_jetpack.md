# SEMANA 4: Jetpack Compose + Room

## Construyendo MiAppNotas desde cero

En esta clase vas a construir la aplicacion MiAppNotas exactamente como esta en el proyecto real. Todo paso a paso, agregando codigo de a partes, entendiendo cada concepto antes de seguir.

---

## PARTE 0: CONCEPTOS PREVIOS QUE NECESITAS ENTENDER

### 0.1 Que es Kotlin y como funciona

Kotlin es un lenguaje de programacion creado por JetBrains (la misma empresa que hace IntelliJ IDEA, en el que se basa Android Studio).

**Donde corre Kotlin en Android:**

```
Tu codigo Kotlin (.kt)
        |
        v
   Compilador kotlinc
        |
        v
   Bytecode (.class)
        |
        v
   D8/R8 (compilador de Android)
        |
        v
   DEX (Dalvik Executable)
        |
        v
   ART (Android Runtime) en el celular
```

**Ciclo de ejecucion:**

1. Escribes codigo en **Kotlin** (archivos .kt)
2. El compilador lo convierte a **bytecode** (como Java)
3. Android lo convierte a **DEX** (formato que entiende el celular)
4. El celular ejecuta el DEX en **ART** (Android Runtime)

ART es la maquina virtual de Android. Reemplazo a Dalvik en Android 5.0+. Es la que lee tu codigo y lo ejecuta en el procesador del celular.

**Kotlin no usa la JDK para ejecutarse en el celular.** Usa la JDK solo para compilar. El celular usa ART, no la JVM.

### 0.2 La JDK y para que sirve

La JDK (Java Development Kit) es el kit que necesitas para compilar tu app Android.

**Para que la necesitas:**
- Compilar tu codigo Kotlin a bytecode
- Ejecutar Gradle (el sistema de construccion)
- Ejecutar herramientas como D8, R8, aapt2

**NO la necesitas en el celular.** El celular solo necesita el APK compilado.

**Configurar el JDK en Android Studio:**

1. Ve a **File → Settings → Build, Execution, Deployment → Build Tools → Gradle**
2. En **Gradle JDK**, selecciona el que dice algo como:
   - `jbr-17` (JetBrains Runtime 17)
   - `Embedded JDK`
3. Si no aparece ninguno, click en **Download JDK** y elige version 17, vendor JetBrains

**JAVA_HOME:** Es una variable de entorno de Windows que dice donde esta la JDK. Si Gradle falla buscando jlink.exe en una ruta de VS Code, significa que JAVA_HOME esta mal configurado.

Para arreglarlo:
1. Busca "variables de entorno" en Windows
2. En Variables del usuario, busca JAVA_HOME
3. Si apunta a `.vscode`, cambialo a `C:\Program Files\Android\Android Studio\jbr`

### 0.3 Garbage Collector en Android

**Que es:** El Garbage Collector (GC) es un proceso automatico que libera memoria de objetos que ya no se usan.

**En Android:** ART tiene su propio Garbage Collector. No necesitas llamarlo manualmente.

**Como funciona:**
- Cuando creas objetos (`val nota = Nota(...)`), se guardan en memoria heap
- Cuando ningun variable referencia mas ese objeto, el GC lo elimina
- El GC se ejecuta automaticamente cuando necesita memoria

**Que significa para ti:**
- No necesitas liberar memoria manualmente (no hay `free()` como en C)
- Pero si dejas referencias colgadas (como un listener que nunca quitas), eso es un **memory leak**
- Usa `lifecycleScope` y `viewLifecycleOwner` para que las corrutinas y observers se limpien solos

**Tip:** En Android Studio, podes ver el uso de memoria en **View → Tool Windows → Profiler**.

### 0.4 Device Manager (Administrador de Dispositivos)

El Device Manager es donde gestionas los emuladores.

**Como abrirlo:**
- En la barra superior de Android Studio, click en el icono de celular con engranaje
- O: **Tools → Device Manager**

**Crear un emulador:**

1. Click en **Create Device**
2. Elegi un hardware. Recomendados:
   - **Pixel 7** (1080x2400, buena relacion rendimiento/calidad)
   - **Pixel 6** (si tu PC es mas modesta)
3. Elegi una imagen del sistema:
   - **API 34** (Android 14) es buena opcion
   - Si no esta descargada, click en la flecha hacia abajo al lado del nombre
4. Configuraciones importantes:
   - **RAM:** 2048 MB minimo, 4096 recomendado
   - **VM Heap:** 256 MB esta bien
   - **Internal Storage:** 8096 MB
   - **Boot:** Quick Boot (arranca mas rapido)
   - **Graphics:** Hardware - GLES 2.0 (si tenes GPU) o Software (si no)
5. Click **Finish**

**Usar el emulador:**
- En la barra superior, selecciona el emulador en el dropdown
- Click en **Play** (triangulo verde) o Shift + F10

**Atajos utiles del emulador:**
- `Ctrl + F11`: Rotar pantalla
- `Ctrl + M`: Menu
- `Ctrl + Back`: Boton atras

### 0.5 Edit Configurations

**Que es:** Donde configuraste como se ejecuta tu app.

**Como abrirlo:**
- Click en el dropdown donde dice "app" en la barra superior
- **Edit Configurations...**

**Que podes cambiar:**

| Opcion | Para que sirve |
|--------|---------------|
| **Module** | Que modulo se ejecuta (normalmente `app`) |
| **Deployment Target** | En que dispositivo se ejecuta (emulador o celular) |
| **Install Flags** | Flags para `adb install` |
| **Launch Options** | Que Activity se lanza al inicio |

**Configuracion tipica:**
- **Module:** app
- **Deploy:** Default APK
- **Launch:** Default Activity

### 0.6 Profiles (Perfiles de compilacion)

Los profiles son configuraciones de build que definen como se compila tu app.

**Dos profiles principales:**

| Profile | Para que es | Caracteristicas |
|---------|-------------|-----------------|
| **debug** | Desarrollo | Sin ofuscacion, logs habilitados, debug habilitado |
| **release** | Produccion | Ofuscacion con R8, sin logs, optimizada |

**Donde se configuran:** En `app/build.gradle.kts`, dentro de `buildTypes`:

```kotlin
buildTypes {
    release {
        isMinifyEnabled = true        // Activa ofuscacion
        proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro")
    }
    debug {
        isDebuggable = true           // Permite debugging
        applicationIdSuffix = ".debug" // Sufijo para instalar junto a la release
    }
}
```

**Que significa minify:** Ofusca y elimina codigo no usado para hacer el APK mas chico.

### 0.7 Debugging en Android Studio

**Poner un breakpoint:**
1. Click en el margen izquierdo de una linea de codigo (donde estan los numeros de linea)
2. Aparece un punto rojo

**Ejecutar en modo debug:**
- Click en el icono del bicho (bug) en la barra superior
- O: **Run → Debug 'app'**
- O: Shift + F9

**Cuando llega al breakpoint:**
- La ejecucion se pausa
- Podes ver variables en la ventana **Debugger**
- Controles:
  - **Step Over (F8)**: Ejecuta la linea actual y avanza
  - **Step Into (F7)**: Entra dentro de la funcion que se llama
  - **Step Out (Shift + F8)**: Sale de la funcion actual
  - **Resume (F9)**: Continua hasta el proximo breakpoint

**Ver logs:**
- Pestaña **Logcat** en la parte inferior
- Podes filtrar por tag, nivel, o texto
- Niveles: `Log.d()` (debug), `Log.i()` (info), `Log.e()` (error), `Log.w()` (warning)

### 0.8 Mirroring (ver celular en la PC)

**Que es:** Ver la pantalla de tu celular fisico en tu computadora en tiempo real.

**Opcion 1: Android Studio Device Mirroring (recomendado)**

1. Activa **Opciones de desarrollador** en tu celular:
   - Settings → About phone → toca "Build number" 7 veces
2. Activa **USB Debugging**:
   - Settings → Developer options → USB debugging → ON
3. Conecta el celular por USB
4. Acepta el permiso de depuracion en el celular
5. En Android Studio, el celular aparece en el dropdown de dispositivos
6. **Tools → Device Manager → Physical → Start Mirroring** (si tu version lo soporta)

**Opcion 2: scrcpy (gratis, funciona siempre)**

1. Descarga scrcpy: https://github.com/Genymobile/scrcpy
2. Activa USB Debugging en tu celular
3. Conecta por USB
4. Ejecuta `scrcpy` en la terminal
5. Ves tu celular en una ventana en la PC

**Opcion 3: Android Studio Wireless Debugging**

1. En tu celular, activa **Wireless debugging** en Developer options
2. Conecta a la misma red WiFi que tu PC
3. En Android Studio: **Device Manager → Pair using QR code**
4. Escanea el QR con tu celular
5. Ahora podes ejecutar apps sin cable

---

## PARTE 1: CREAR EL PROYECTO

### 1.1 Nuevo Proyecto

1. Abre Android Studio
2. **File → New → New Project**
3. Elige **Empty Activity** (la que tiene el logo de Compose)
4. Configura:

```
Name:           MiAppNotas
Package name:   com.misitioweb.miappnotas
Save location:  (donde quieras)
Language:       Kotlin
Minimum SDK:    API 26
Build Config:   Kotlin DSL
```

5. Click **Finish**
6. Espera a que termine Gradle Sync

### 1.2 Ver que se creo

Cuando termina, tu proyecto tiene esta estructura basica:

```
MiAppNotas/
├── build.gradle.kts              (raiz)
├── settings.gradle.kts
├── gradle/libs.versions.toml     (catalogo de versiones)
└── app/
    ├── build.gradle.kts          (modulo app)
    └── src/main/
        ├── AndroidManifest.xml
        ├── java/com/misitioweb/miappnotas/
        │   └── MainActivity.kt
        └── res/
            └── ... (recursos)
```

**Que hace cada archivo:**

| Archivo | Para que sirve |
|---------|---------------|
| `build.gradle.kts` (raiz) | Plugins que pueden usar los modulos |
| `settings.gradle.kts` | Nombre del proyecto, repositorios |
| `libs.versions.toml` | Todas las versiones centralizadas |
| `app/build.gradle.kts` | Configuracion del modulo app (SDK, dependencias) |
| `AndroidManifest.xml` | Declara activities, permisos, etc |
| `MainActivity.kt` | Tu primera pantalla |

---

## PARTE 2: ENTENDER LA ARQUITECTURA ANTES DE CODIFICAR

Antes de escribir codigo, veamos como vamos a organizar todo.

### 2.1 Que es el patron MVVM

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│    VIEW      │────▶│   VIEWMODEL  │────▶│  REPOSITORY  │────▶│  DATA SOURCE │
│  (Compose)   │     │              │     │              │     │  (Room/Room) │
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
       │                    │                    │
       │   Observa datos    │   Transforma       │   Abstrae el
       │   reactivos        │   para la UI       │   acceso a datos
       └────────────────────┴────────────────────┘
```

**View (Compose):** Solo muestra datos y reacciona a clicks. No tiene logica de negocio.

**ViewModel:** Guarda el estado de la pantalla. Sobrevive rotaciones de pantalla. Le dice al repositorio que hacer.

**Repository:** Es el intermediario. La UI no sabe si los datos vienen de Room, de una API, o de SharedPreferences.

**Data Source (Room):** La base de datos real en el celular.

### 2.2 Que es DAO

**DAO = Data Access Object.** Es un patron de disenio que encapsula todo el acceso a datos.

**Por que existe:** Para que el resto de tu app no tenga que escribir SQL. El DAO traduce funciones de Kotlin a consultas SQL.

```
Tu codigo llama a:     notaDao.insertar(nota)
                                |
                                v
Room genera SQL:        INSERT INTO notas (titulo, contenido) VALUES (?, ?)
```

**Sin DAO:** Tendrias que escribir SQL a mano en toda tu app.

**Con DAO:** Solo llamas funciones de Kotlin.

### 2.3 Que es Repository

Es una capa mas de abstraccion. El ViewModel no habla directo con el DAO, habla con el Repository.

**Por que?** Para poder cambiar la fuente de datos sin cambiar el ViewModel.

```
Hoy:     ViewModel → Repository → Room (base de datos local)

Maniana: ViewModel → Repository → API REST (internet)
         (el ViewModel no cambia!)
```

### 2.4 Conceptos de Kotlin que vas a ver

#### `suspend`

Una funcion `suspend` puede pausar su ejecucion sin bloquear el hilo.

```kotlin
// Funcion normal: bloquea el hilo hasta terminar
fun obtenerDatos(): String {
    Thread.sleep(2000)  // Congela la UI 2 segundos!
    return "datos"
}

// Funcion suspend: puede esperar sin bloquear
suspend fun obtenerDatos(): String {
    delay(2000)  // Pausa la corrutina, la UI sigue respondiendo
    return "datos"
}
```

**Regla:** Solo podes llamar a `suspend` desde otra `suspend` o desde una corrutina (`lifecycleScope.launch {}`).

#### `@Volatile`

Es una anotacion que dice "esta variable puede ser leida por varios hilos al mismo tiempo".

```kotlin
companion object {
    @Volatile
    private var INSTANCIA: NotaDatabase? = null
```

**Por que se usa aca:** Para que cuando dos hilos quieran crear la base de datos al mismo tiempo, no creen dos instancias diferentes. `@Volatile` asegura que todos los hilos ven el mismo valor.

#### `by lazy`

Crea el valor solo la primera vez que se usa.

```kotlin
val repositorio by lazy { NotaRepositorio(database.notaDao()) }
```

**Cuando se ejecuta?** Recien cuando escribis `repositorio.algo()` por primera vez. Si nunca lo usas, nunca se crea.

#### `Flow` y `StateFlow`

**Flow** es un stream de datos. En vez de pedir datos una vez, te "suscribis" y recibis actualizaciones.

```kotlin
// Flow: emite datos en el tiempo
fun obtenerTodas(): Flow<List<Nota>>
```

**StateFlow** es un Flow que siempre tiene un valor actual y notifica cuando cambia.

```kotlin
// StateFlow: como LiveData pero de Kotlin
val notas: StateFlow<List<Nota>>
```

#### `collectAsState()`

Es como observar un Flow desde Compose. Cuando el Flow emite un valor nuevo, Compose redibuja la pantalla.

```kotlin
val notas by viewModel.notas.collectAsState()
// Cuando notas cambia, la pantalla se redibuja automaticamente
```

---

## PARTE 3: AGREGAR DEPENDENCIAS

### 3.1 Abrir el catalogo de versiones

En Android Studio, abre:

```
Gradle Scripts → gradle/libs.versions.toml
```

Este archivo centraliza todas las versiones.

### 3.2 Agregar Room

Busca la seccion `[versions]` y agrega:

```toml
[versions]
# ... lo que ya hay ...
room = "2.6.1"
ksp = "2.1.10-1.0.28"
```

En `[libraries]`, agrega:

```toml
[libraries]
# ... lo que ya hay ...
androidx-room-runtime = { group = "androidx.room", name = "room-runtime", version.ref = "room" }
androidx-room-ktx = { group = "androidx.room", name = "room-ktx", version.ref = "room" }
androidx-room-compiler = { group = "androidx.room", name = "room-compiler", version.ref = "room" }
```

En `[plugins]`, agrega:

```toml
[plugins]
# ... lo que ya hay ...
kotlin-ksp = { id = "com.google.devtools.ksp", version.ref = "ksp" }
```

### 3.3 Agregar plugins al build.gradle.kts de la raiz

Abre el archivo `build.gradle.kts` (el de la raiz, no el de app):

```kotlin
plugins {
    alias(libs.plugins.android.application) apply false
    alias(libs.plugins.kotlin.android) apply false
    alias(libs.plugins.kotlin.compose) apply false
    alias(libs.plugins.kotlin.ksp) apply false
}
```

### 3.4 Aplicar plugins en app/build.gradle.kts

Abre `app/build.gradle.kts`. En los plugins, agrega KSP:

```kotlin
plugins {
    alias(libs.plugins.android.application)
    alias(libs.plugins.kotlin.android)
    alias(libs.plugins.kotlin.compose)
    alias(libs.plugins.kotlin.ksp)
}
```

En `dependencies`, agrega Room:

```kotlin
dependencies {
    // ... lo que ya hay ...
    
    implementation(libs.androidx.room.runtime)
    implementation(libs.androidx.room.ktx)
    ksp(libs.androidx.room.compiler)
}
```

### 3.5 Sync

Click en **Sync Now** (barra superior).

Si termina sin errores, estas listo para empezar a crear archivos.

---

## PARTE 4: CREAR LA ENTIDAD NOTA

### 4.1 Crear el paquete de datos

Primero, vamos a organizar el codigo por capas.

En el panel izquierdo (Project), navega a:

```
app → src → main → java → com.misitioweb.miappnotas
```

Click derecho sobre `com.misitioweb.miappnotas`:

```
New → Package
```

Escribi: **data**

Click derecho sobre `data`:

```
New → Package
```

Escribi: **local**

Ahora tenes: `com.misitioweb.miappnotas.data.local`

### 4.2 Crear la clase Nota

Click derecho sobre el paquete `local`:

```
New → Kotlin Class/File → Class
```

Nombre: **Nota**

Android Studio crea el archivo. Reemplaza todo el contenido con:

```kotlin
package com.misitioweb.miappnotas.data.local

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "notas")
data class Nota(
    @PrimaryKey(autoGenerate = true)
    val id: Long = 0,
    val titulo: String,
    val contenido: String,
    val fechaCreacion: Long = System.currentTimeMillis(),
    val esImportante: Boolean = false
)
```

### 4.3 Que significa cada cosa

**`@Entity(tableName = "notas")`:** Le dice a Room "esta clase es una tabla en la base de datos, y la tabla se llama notas".

**`@PrimaryKey(autoGenerate = true)`:** Este campo es la clave primaria. `autoGenerate` significa que Room genera el ID automaticamente.

**`data class`:** Es una clase especial de Kotlin que genera automaticamente `equals()`, `hashCode()`, `toString()` y `copy()`. Perfecta para modelos de datos.

**`val id: Long = 0`:** El ID es 0 por defecto. Cuando Room lo inserta, lo cambia por el valor real generado.

**`val fechaCreacion: Long = System.currentTimeMillis()`:** La fecha se pone automaticamente al crear el objeto. Es un timestamp en milisegundos.

### 4.4 Probar que compila

Click en **Build → Make Project** (o Ctrl + F9).

Si dice "Build successful", la entidad esta bien.

---

## PARTE 5: CREAR EL DAO

### 5.1 Crear la interfaz

En el mismo paquete `data.local`:

```
New → Kotlin Class/File → Interface
```

Nombre: **NotaDao**

Reemplaza el contenido:

```kotlin
package com.misitioweb.miappnotas.data.local

import androidx.room.*
import kotlinx.coroutines.flow.Flow

@Dao
interface NotaDao {
    
    @Query("SELECT * FROM notas ORDER BY fechaCreacion DESC")
    fun obtenerTodas(): Flow<List<Nota>>
    
    @Query("SELECT * FROM notas WHERE id = :id")
    suspend fun obtenerPorId(id: Long): Nota?
    
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertar(nota: Nota): Long
    
    @Update
    suspend fun actualizar(nota: Nota)
    
    @Delete
    suspend fun eliminar(nota: Nota)
}
```

### 5.2 Que significa cada cosa

**`@Dao`:** Le dice a Room "esta interfaz define operaciones con la base de datos". Room genera la implementacion automaticamente.

**`interface`:** No tiene cuerpo. Room genera el codigo que implementa estas funciones.

**`@Query("SELECT ...")`:** Es una consulta SQL que vos escribis. Room la valida en tiempo de compilacion.

**`:id` en la query:** Es un parametro. Se reemplaza con el valor del argumento `id`.

**`Flow<List<Nota>>`:** Retorna un Flow que emite una lista cada vez que la base de datos cambia. La UI se actualiza sola.

**`suspend`:** Estas operaciones pueden tardar (especialmente si hay muchos datos). `suspend` permite ejecutarlas sin congelar la UI.

**`@Insert(onConflict = OnConflictStrategy.REPLACE)`:** Si ya existe una nota con el mismo ID, la reemplaza en vez de dar error.

**`@Update` y `@Delete`:** Room genera el SQL automaticamente basandose en la entidad.

### 5.3 Compilar

**Build → Make Project**. Si funciona, segui.

---

## PARTE 6: CREAR LA BASE DE DATOS

### 6.1 Crear la clase

En `data.local`:

```
New → Kotlin Class/File → Class
```

Nombre: **NotaDatabase**

```kotlin
package com.misitioweb.miappnotas.data.local

import android.content.Context
import androidx.room.Database
import androidx.room.Room
import androidx.room.RoomDatabase

@Database(entities = [Nota::class], version = 1, exportSchema = false)
abstract class NotaDatabase : RoomDatabase() {
    
    abstract fun notaDao(): NotaDao
    
    companion object {
        @Volatile
        private var INSTANCIA: NotaDatabase? = null
        
        fun obtener(context: Context): NotaDatabase {
            return INSTANCIA ?: synchronized(this) {
                val base = Room.databaseBuilder(
                    context.applicationContext,
                    NotaDatabase::class.java,
                    "notas_db"
                ).build()
                INSTANCIA = base
                base
            }
        }
    }
}
```

### 6.2 Que significa cada cosa

**`@Database(entities = [Nota::class], version = 1)`:** Esta base de datos tiene una entidad (Nota) y es la version 1. Cuando cambies la estructura, subis la version.

**`abstract class`:** No se puede instanciar directamente. Room genera la implementacion.

**`abstract fun notaDao(): NotaDao`:** Room genera automaticamente el DAO. Esta funcion lo retorna.

**`@Volatile private var INSTANCIA`:** Pattern Singleton thread-safe. `@Volatile` asegura que todos los hilos ven el mismo valor. Si dos hilos llaman a `obtener()` al mismo tiempo, no crean dos bases de datos.

**`synchronized(this)`:** Solo un hilo puede ejecutar este bloque a la vez. Es la segunda capa de proteccion.

**`Room.databaseBuilder(...)`:** Construye la base de datos.

- `context.applicationContext`: El contexto de la aplicacion (no de una Activity)
- `NotaDatabase::class.java`: La clase de la base de datos
- `"notas_db"`: El nombre del archivo SQLite en el celular

### 6.3 Compilar

**Build → Make Project**.

---

## PARTE 7: CREAR EL REPOSITORIO

### 7.1 Crear el paquete

Click derecho sobre `data`:

```
New → Package
```

Nombre: **repository**

### 7.2 Crear la clase

En `data.repository`:

```
New → Kotlin Class/File → Class
```

Nombre: **NotaRepositorio**

```kotlin
package com.misitioweb.miappnotas.data.repository

import com.misitioweb.miappnotas.data.local.Nota
import com.misitioweb.miappnotas.data.local.NotaDao
import kotlinx.coroutines.flow.Flow

class NotaRepositorio(private val notaDao: NotaDao) {
    
    val todasLasNotas: Flow<List<Nota>> = notaDao.obtenerTodas()
    
    suspend fun obtenerPorId(id: Long): Nota? = notaDao.obtenerPorId(id)
    
    suspend fun insertar(nota: Nota): Long = notaDao.insertar(nota)
    
    suspend fun actualizar(nota: Nota) = notaDao.actualizar(nota)
    
    suspend fun eliminar(nota: Nota) = notaDao.eliminar(nota)
}
```

### 7.3 Que significa cada cosa

**`class NotaRepositorio(private val notaDao: NotaDao)`:** El repositorio recibe el DAO en el constructor. Esto se llama **inyeccion de dependencias** (manual en este caso).

**`val todasLasNotas: Flow<List<Nota>>`:** Expone el Flow del DAO. El ViewModel lo observa.

**`suspend fun obtenerPorId...`:** Delega directamente al DAO. Podrias agregar logica extra aca (como cachear, o combinar con una API) sin que el ViewModel se entere.

### 7.4 Compilar

**Build → Make Project**.

---

## PARTE 8: CREAR EL VIEWMODEL

### 8.1 Crear el paquete UI

Click derecho sobre `com.misitioweb.miappnotas`:

```
New → Package
```

Nombre: **ui**

### 8.2 Crear el ViewModel

En el paquete `ui`:

```
New → Kotlin Class/File → Class
```

Nombre: **NotaViewModel**

```kotlin
package com.misitioweb.miappnotas.ui

import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.viewModelScope
import com.misitioweb.miappnotas.data.local.Nota
import com.misitioweb.miappnotas.data.repository.NotaRepositorio
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch

class NotaViewModel(
    private val repositorio: NotaRepositorio
) : ViewModel() {
```

### 8.3 Agregar el Flow de notas

Dentro de la clase, despues del constructor:

```kotlin
    val notas: StateFlow<List<Nota>> = repositorio.todasLasNotas
        .stateIn(
            scope = viewModelScope,
            started = SharingStarted.WhileSubscribed(5000),
            initialValue = emptyList()
        )
```

**Que hace esto:**

- `repositorio.todasLasNotas` es un `Flow`
- `stateIn()` lo convierte en `StateFlow` (siempre tiene un valor)
- `viewModelScope`: La corrutina vive mientras viva el ViewModel
- `SharingStarted.WhileSubscribed(5000)`: Mientras la UI este observando, mantiene la conexion activa. Si deja de observar por 5 segundos, se desconecta para ahorrar recursos
- `initialValue = emptyList()`: Mientras carga, muestra lista vacia

### 8.4 Agregar el estado del editor

```kotlin
    private val _notaSeleccionada = MutableStateFlow<Nota?>(null)
    val notaSeleccionada: StateFlow<Nota?> = _notaSeleccionada.asStateFlow()

    private val _mostrarEditor = MutableStateFlow(false)
    val mostrarEditor: StateFlow<Boolean> = _mostrarEditor.asStateFlow()
```

**Que es MutableStateFlow:** Un Flow que podes modificar. El `_` adelante es convencion de Kotlin: el privado es mutable, el publico es solo lectura (`asStateFlow()`).

### 8.5 Agregar las funciones

```kotlin
    fun seleccionarNota(nota: Nota?) {
        _notaSeleccionada.value = nota
        _mostrarEditor.value = nota != null
    }

    fun nuevaNota() {
        _notaSeleccionada.value = null
        _mostrarEditor.value = true
    }

    fun guardarNota(nota: Nota) {
        viewModelScope.launch {
            if (nota.id == 0L) {
                repositorio.insertar(nota)
            } else {
                repositorio.actualizar(nota)
            }
            cerrarEditor()
        }
    }

    fun eliminarNota(nota: Nota) {
        viewModelScope.launch {
            repositorio.eliminar(nota)
            cerrarEditor()
        }
    }

    fun cerrarEditor() {
        _notaSeleccionada.value = null
        _mostrarEditor.value = false
    }
```

**Que hace `viewModelScope.launch`:** Inicia una corrutina en el ambito del ViewModel. Si el ViewModel se destruye, la corrutina se cancela automaticamente.

### 8.6 Agregar el Factory

El ViewModel necesita el repositorio. Como no usamos Hilt (inyeccion de dependencias automatica), creamos un Factory:

```kotlin
    class Factory(private val repositorio: NotaRepositorio) : ViewModelProvider.Factory {
        @Suppress("UNCHECKED_CAST")
        override fun <T : ViewModel> create(modelClass: Class<T>): T {
            if (modelClass.isAssignableFrom(NotaViewModel::class.java)) {
                return NotaViewModel(repositorio) as T
            }
            throw IllegalArgumentException("Unknown ViewModel class")
        }
    }
}
```

**Que es ViewModelProvider.Factory:** Es una interfaz que dice "yo se como crear este ViewModel". Se usa cuando el ViewModel necesita parametros en el constructor.

### 8.7 Compilar

**Build → Make Project**.

---

## PARTE 9: CREAR LAS PANTALLAS DE COMPOSE

### 9.1 Crear el paquete de screens

En `ui`:

```
New → Package
```

Nombre: **screens**

### 9.2 Crear ListaNotasScreen

En `ui.screens`:

```
New → Kotlin Class/File → Kotlin File
```

Nombre: **ListaNotasScreen**

```kotlin
package com.misitioweb.miappnotas.ui.screens

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.FloatingActionButton
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import com.misitioweb.miappnotas.data.local.Nota
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ListaNotasScreen(
    notas: List<Nota>,
    onNotaClick: (Nota) -> Unit,
    onAgregarClick: () -> Unit,
    onEliminarClick: (Nota) -> Unit
) {
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Mis Notas") },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = MaterialTheme.colorScheme.primary,
                    titleContentColor = MaterialTheme.colorScheme.onPrimary
                )
            )
        },
        floatingActionButton = {
            FloatingActionButton(
                onClick = onAgregarClick,
                containerColor = MaterialTheme.colorScheme.primary
            ) {
                Icon(Icons.Default.Add, contentDescription = "Agregar nota")
            }
        }
    ) { paddingValues ->
        if (notas.isEmpty()) {
            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(paddingValues),
                contentAlignment = Alignment.Center
            ) {
                Text(
                    text = "No hay notas. Toca + para agregar una.",
                    style = MaterialTheme.typography.bodyLarge,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
        } else {
            LazyColumn(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(paddingValues),
                contentPadding = PaddingValues(16.dp),
                verticalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                items(notas, key = { it.id }) { nota ->
                    NotaItem(
                        nota = nota,
                        onClick = { onNotaClick(nota) },
                        onEliminarClick = { onEliminarClick(nota) }
                    )
                }
            }
        }
    }
}
```

### 9.3 Que es cada cosa en Compose

**`@Composable`:** Es una anotacion que dice "esta funcion dibuja UI". Solo se puede llamar desde otra funcion `@Composable`.

**`Scaffold`:** Es una estructura base de Material Design. Tiene slots para:
- `topBar`: La barra de arriba
- `floatingActionButton`: El boton flotante
- El contenido va en el lambda `{ paddingValues -> ... }`

**`LazyColumn`:** Es el equivalente a RecyclerView en Compose. Solo renderiza los items visibles.

**`items(notas, key = { it.id })`:** Recorre la lista. El `key` ayuda a Compose a saber que item cambio.

### 9.4 Agregar el item de nota

Al final del mismo archivo `ListaNotasScreen.kt`, agrega:

```kotlin
@Composable
fun NotaItem(
    nota: Nota,
    onClick: () -> Unit,
    onEliminarClick: () -> Unit
) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .clickable(onClick = onClick),
        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp),
        colors = CardDefaults.cardColors(
            containerColor = if (nota.esImportante) {
                MaterialTheme.colorScheme.errorContainer
            } else {
                MaterialTheme.colorScheme.surface
            }
        )
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp)
        ) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    text = nota.titulo,
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.Bold,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis,
                    modifier = Modifier.weight(1f)
                )
                IconButton(onClick = onEliminarClick) {
                    Icon(
                        Icons.Default.Delete,
                        contentDescription = "Eliminar",
                        tint = MaterialTheme.colorScheme.error
                    )
                }
            }
            
            Spacer(modifier = Modifier.height(4.dp))
            
            Text(
                text = nota.contenido,
                style = MaterialTheme.typography.bodyMedium,
                maxLines = 2,
                overflow = TextOverflow.Ellipsis,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
            
            Spacer(modifier = Modifier.height(8.dp))
            
            val fechaFormat = SimpleDateFormat("dd/MM/yyyy HH:mm", Locale.getDefault())
            Text(
                text = fechaFormat.format(Date(nota.fechaCreacion)),
                style = MaterialTheme.typography.labelSmall,
                color = MaterialTheme.colorScheme.outline
            )
        }
    }
}
```

**Que hace:** Muestra cada nota en una tarjeta con titulo, contenido, fecha y boton de eliminar.

**`modifier`:** Es como se estila cada elemento en Compose. Encadenas modificadores para cambiar tamanio, padding, color, etc.

**`Card`:** Un contenedor con bordes redondeados y sombra.

**`clickable(onClick = ...)`:** Hace que cualquier elemento responda a clicks.

### 9.5 Compilar

**Build → Make Project**.

---

## PARTE 10: CREAR LA PANTALLA DE EDITAR

### 10.1 Crear el archivo

En `ui.screens`:

```
New → Kotlin Class/File → Kotlin File
```

Nombre: **EditarNotaScreen**

```kotlin
package com.misitioweb.miappnotas.ui.screens

import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.Check
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.misitioweb.miappnotas.data.local.Nota

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun EditarNotaScreen(
    nota: Nota?,
    onGuardar: (Nota) -> Unit,
    onEliminar: (Nota) -> Unit,
    onVolver: () -> Unit
) {
```

### 10.2 Agregar el estado

Despues de la declaracion de la funcion, agrega:

```kotlin
    var titulo by remember { mutableStateOf(nota?.titulo ?: "") }
    var contenido by remember { mutableStateOf(nota?.contenido ?: "") }
    var esImportante by remember { mutableStateOf(nota?.esImportante ?: false) }
    
    val esEdicion = nota != null
```

**Que es `remember`:** En Compose, cada vez que se redibuja la pantalla, las variables locales se resetean. `remember` le dice a Compose "guarda este valor entre redibujos".

**`mutableStateOf`:** Crea un estado que, cuando cambia, redibuja la pantalla.

**`by` delegation:** Permite usar `titulo = "nuevo"` en vez de `titulo.value = "nuevo"`.

### 10.3 Agregar LaunchedEffect

```kotlin
    LaunchedEffect(nota) {
        nota?.let {
            titulo = it.titulo
            contenido = it.contenido
            esImportante = it.esImportante
        }
    }
```

**Que es `LaunchedEffect`:** Es un bloque de codigo que se ejecuta cuando cambian sus llaves (`nota`). Se usa para efectos secundarios (como inicializar estado cuando llegan datos nuevos).

### 10.4 Agregar el Scaffold

```kotlin
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text(if (esEdicion) "Editar Nota" else "Nueva Nota") },
                navigationIcon = {
                    IconButton(onClick = onVolver) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Volver")
                    }
                },
                actions = {
                    if (esEdicion) {
                        IconButton(onClick = { nota?.let { onEliminar(it) } }) {
                            Icon(
                                Icons.Default.Delete,
                                contentDescription = "Eliminar",
                                tint = MaterialTheme.colorScheme.error
                            )
                        }
                    }
                    IconButton(
                        onClick = {
                            if (titulo.isNotBlank()) {
                                val nuevaNota = Nota(
                                    id = nota?.id ?: 0,
                                    titulo = titulo.trim(),
                                    contenido = contenido.trim(),
                                    fechaCreacion = nota?.fechaCreacion ?: System.currentTimeMillis(),
                                    esImportante = esImportante
                                )
                                onGuardar(nuevaNota)
                            }
                        }
                    ) {
                        Icon(Icons.Default.Check, contentDescription = "Guardar")
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = MaterialTheme.colorScheme.primary,
                    titleContentColor = MaterialTheme.colorScheme.onPrimary,
                    navigationIconContentColor = MaterialTheme.colorScheme.onPrimary,
                    actionIconContentColor = MaterialTheme.colorScheme.onPrimary
                )
            )
        }
    ) { paddingValues ->
```

### 10.5 Agregar el contenido

```kotlin
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
                .padding(16.dp)
        ) {
            OutlinedTextField(
                value = titulo,
                onValueChange = { titulo = it },
                label = { Text("Titulo") },
                placeholder = { Text("Ingresa el titulo") },
                modifier = Modifier.fillMaxWidth(),
                singleLine = true,
                isError = titulo.isBlank()
            )
            
            Spacer(modifier = Modifier.height(16.dp))
            
            OutlinedTextField(
                value = contenido,
                onValueChange = { contenido = it },
                label = { Text("Contenido") },
                placeholder = { Text("Escribe tu nota...") },
                modifier = Modifier
                    .fillMaxWidth()
                    .weight(1f),
                minLines = 5
            )
            
            Spacer(modifier = Modifier.height(16.dp))
            
            androidx.compose.foundation.layout.Row(
                modifier = Modifier.fillMaxWidth(),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    text = "Nota importante",
                    style = MaterialTheme.typography.bodyLarge,
                    modifier = Modifier.weight(1f)
                )
                androidx.compose.material3.Switch(
                    checked = esImportante,
                    onCheckedChange = { esImportante = it }
                )
            }
        }
    }
}
```

### 10.6 Compilar

**Build → Make Project**.

---

## PARTE 11: MODIFICAR MainActivity

### 11.1 Abrir MainActivity

Abre `MainActivity.kt`. Tiene codigo por defecto de Compose. Vamos a reemplazarlo.

### 11.2 Reemplazar el contenido

Borra todo y pega:

```kotlin
package com.misitioweb.miappnotas

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.lifecycle.viewmodel.compose.viewModel
import com.misitioweb.miappnotas.data.local.NotaDatabase
import com.misitioweb.miappnotas.data.repository.NotaRepositorio
import com.misitioweb.miappnotas.ui.NotaViewModel
import com.misitioweb.miappnotas.ui.screens.EditarNotaScreen
import com.misitioweb.miappnotas.ui.screens.ListaNotasScreen
import com.misitioweb.miappnotas.ui.theme.MiAppNotasTheme

class MainActivity : ComponentActivity() {

    private lateinit var repositorio: NotaRepositorio

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val database = NotaDatabase.obtener(applicationContext)
        repositorio = NotaRepositorio(database.notaDao())

        enableEdgeToEdge()
        setContent {
            MiAppNotasTheme {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    val viewModel: NotaViewModel = viewModel(
                        factory = NotaViewModel.Factory(repositorio)
                    )

                    val notas by viewModel.notas.collectAsState()
                    val notaSeleccionada by viewModel.notaSeleccionada.collectAsState()
                    val mostrarEditor by viewModel.mostrarEditor.collectAsState()

                    if (mostrarEditor) {
                        EditarNotaScreen(
                            nota = notaSeleccionada,
                            onGuardar = { viewModel.guardarNota(it) },
                            onEliminar = { viewModel.eliminarNota(it) },
                            onVolver = { viewModel.cerrarEditor() }
                        )
                    } else {
                        ListaNotasScreen(
                            notas = notas,
                            onNotaClick = { viewModel.seleccionarNota(it) },
                            onAgregarClick = { viewModel.nuevaNota() },
                            onEliminarClick = { viewModel.eliminarNota(it) }
                        )
                    }
                }
            }
        }
    }
}
```

### 11.3 Que hace cada parte

**`ComponentActivity`:** La Activity base para apps que usan Compose. No hereda de `AppCompatActivity`.

**`enableEdgeToEdge()`:** Hace que la app use toda la pantalla, incluyendo el area de la barra de estado.

**`setContent { ... }`:** El punto de entrada de Compose. Todo lo que va adentro es UI de Compose.

**`MiAppNotasTheme { ... }`:** Aplica los colores y tipografia del tema.

**`viewModel(factory = ...)`:** Crea o reutiliza el ViewModel. Usa el Factory que definimos para pasarle el repositorio.

**`collectAsState()`:** Observa el StateFlow. Cuando cambia, Compose redibuja.

**El `if (mostrarEditor)`:** Decide que pantalla mostrar. No hay Navigation component, solo condicionales. Simple.

### 11.4 Compilar

**Build → Make Project**.

---

## PARTE 12: COMPONENTES QUE NO USAMOS EN ESTE PROYECTO

### 12.1 Service

Un **Service** es un componente que corre en segundo plano, sin interfaz.

**Cuando se usa:**
- Reproducir musica
- Descargar archivos grandes
- Sincronizar datos periodicamente
- Notificaciones que persisten

**En este proyecto:** No lo usamos porque la app es simple. No necesita hacer nada en segundo plano.

**Ejemplo de como seria:**

```kotlin
class SyncService : Service() {
    
    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        // Hacer trabajo en segundo plano
        return START_NOT_STICKY
    }
    
    override fun onBind(intent: Intent?): IBinder? = null
}
```

**Tipos de Service:**

| Tipo | Cuando usarlo |
|------|---------------|
| **Started** | Se inicia con `startService()`, corre hasta que se detiene |
| **Bound** | Se vincula con `bindService()`, corre mientras hay clientes |
| **Foreground** | Tiene una notificacion visible, no lo mata el sistema facil |

### 12.2 BroadcastReceiver

Escucha eventos del sistema o de otras apps.

**Cuando se usa:**
- Detectar cuando el celular se enciende
- Detectar cambio de conexion de red
- Detectar bateria baja

**En este proyecto:** No lo usamos.

**Ejemplo:**

```kotlin
class NetworkReceiver : BroadcastReceiver() {
    override fun onReceive(context: Context?, intent: Intent?) {
        // Reaccionar al evento
    }
}
```

### 12.3 ContentProvider

Comparte datos entre aplicaciones.

**Cuando se usa:**
- Acceder a contactos del sistema
- Compartir archivos entre apps

**En este proyecto:** No lo usamos.

### 12.4 Fragment

Una porcion reutilizable de UI dentro de una Activity.

**Cuando se usa:**
- Pantallas con tabs
- Tablets con master-detail
- Navegacion con Bottom Navigation

**En este proyecto:** No lo usamos porque Compose reemplaza la necesidad de Fragments. Toda la UI se compone con Composables.

---

## PARTE 13: ESTRUCTURA FINAL DEL PROYECTO

```
MiAppNotas/
├── build.gradle.kts
├── settings.gradle.kts
├── gradle/
│   └── libs.versions.toml
└── app/
    ├── build.gradle.kts
    └── src/main/
        ├── AndroidManifest.xml
        ├── java/com/misitioweb/miappnotas/
        │   ├── MainActivity.kt
        │   ├── data/
        │   │   ├── local/
        │   │   │   ├── Nota.kt              (Entidad Room)
        │   │   │   ├── NotaDao.kt           (Data Access Object)
        │   │   │   └── NotaDatabase.kt      (Base de datos)
        │   │   └── repository/
        │   │       └── NotaRepositorio.kt   (Repository)
        │   └── ui/
        │       ├── NotaViewModel.kt         (ViewModel)
        │       ├── screens/
        │       │   ├── ListaNotasScreen.kt  (Pantalla lista)
        │       │   └── EditarNotaScreen.kt  (Pantalla editor)
        │       └── theme/
        │           ├── Color.kt
        │           ├── Theme.kt
        │           └── Type.kt
        └── res/
            └── ... (iconos, strings, etc)
```

---

## PARTE 14: EJECUTAR Y PROBAR

### 14.1 En el emulador

1. Selecciona el emulador en el dropdown
2. Click en **Play** (Shift + F10)
3. Espera a que se instale

### 14.2 Que probar

- **Crear nota:** Click en el boton +
- **Editar nota:** Click en una nota existente
- **Eliminar:** Click en el icono de basura
- **Importante:** Activa el switch y nota como cambia el color de la tarjeta

### 14.3 Debugging

1. Pon un breakpoint en `guardarNota()` del ViewModel
2. Ejecuta en modo debug (Shift + F9)
3. Crea una nota
4. Cuando llegue al breakpoint, inspecciona las variables

### 14.4 Ver logs

Abre **Logcat** en la parte inferior de Android Studio.

---

## PARTE 15: RESUMEN DE CONCEPTOS

### Patrones de diseno usados

| Patron | Donde se usa | Para que |
|--------|--------------|----------|
| **MVVM** | Toda la arquitectura | Separar UI de logica |
| **Repository** | `NotaRepositorio` | Abstraer fuente de datos |
| **DAO** | `NotaDao` | Encapsular acceso a BD |
| **Singleton** | `NotaDatabase` | Una sola instancia de BD |
| **Factory** | `NotaViewModel.Factory` | Crear ViewModel con parametros |

### Palabras clave de Kotlin

| Concepto | Para que sirve |
|----------|---------------|
| `suspend` | Funcion que puede pausarse sin bloquear el hilo |
| `@Volatile` | Variable visible por todos los hilos inmediatamente |
| `by lazy` | Inicializacion diferida (solo cuando se usa) |
| `Flow` | Stream de datos reactivo |
| `StateFlow` | Flow con valor actual y notificaciones de cambio |
| `collectAsState()` | Observar Flow desde Compose |
| `viewModelScope` | Corrutina ligada al ciclo de vida del ViewModel |
| `remember` | Guardar estado entre recomposiciones en Compose |
| `mutableStateOf` | Estado mutable que dispara recomposicion |
| `LaunchedEffect` | Ejecutar efecto cuando cambian las llaves |

### Componentes de Android

| Componente | Usado? | Para que |
|------------|--------|----------|
| Activity | SI | Punto de entrada |
| Compose | SI | UI declarativa |
| ViewModel | SI | Estado de la pantalla |
| Room | SI | Base de datos local |
| Service | NO | Segundo plano |
| BroadcastReceiver | NO | Eventos del sistema |
| ContentProvider | NO | Compartir datos |
| Fragment | NO | UI reutilizable |
