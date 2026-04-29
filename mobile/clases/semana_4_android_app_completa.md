# SEMANA 4: Mi Primera App de Notas — XML/Views → Jetpack Compose

## Tutorial Completo: Dos Enfoques, Una App

En esta clase vas a construir la misma aplicacion de notas **dos veces**: primero con el enfoque clasico **XML/Views** y luego con **Jetpack Compose**. Veras las diferencias lado a lado, entenderas por que Google migró a Compose, y tendras el codigo completo de ambos enfoques.

Tambien aprenderas a configurar el JDK, crear emuladores, debugear, y usar todos los componentes de Android (Activity, Service, BroadcastReceiver, ContentProvider, Fragment). Al final, integraremos Google Maps y Google Calendar **sin necesidad de API keys**.

---

## CONCEPTOS FUNDAMENTALES ANTES DE EMPEZAR

### ¿Que es Gradle?

**Gradle** es el sistema de construccion (build) que usa Android Studio.
- Compila tu codigo
- Descarga librerias
- Empaqueta la app
- Ejecuta tests

Piensa en Gradle como un "npm" o "maven" pero para Android.

### ¿Que son los Plugins?

Un **plugin** es una extension que agrega funcionalidades a Gradle.

| Plugin | Para que sirve |
|--------|----------------|
| `com.android.application` | Compilar apps Android |
| `org.jetbrains.kotlin.android` | Soporte para Kotlin |
| `org.jetbrains.kotlin.plugin.compose` | Compilar UI con Compose (Kotlin 2.0+) |
| `com.google.devtools.ksp` | Generar codigo automaticamente |

### ¿Que es KSP vs KAPT?

**KAPT** y **KSP** generan codigo automaticamente durante la compilacion (Room los necesita).

| Caracteristica | KAPT | KSP |
|---------------|------|-----|
| Velocidad | Mas lento | Mas rapido |
| Estado | Mantenimiento | Recomendado |

**Recomendacion: Usar KSP.**

### ¿Que es Room?

**Room** es la libreria oficial de Android para bases de datos SQLite.

```
┌─────────────────────────────────────────────────────────────┐
│                      TU APP                                 │
│  ┌─────────────┐     ┌──────────────┐    ┌───────────────┐ │
│  │   UI        │────▶│  Repositorio │────▶│    Room       │ │
│  │ (XML/Views) │     │              │     │  (SQLite)     │ │
│  └─────────────┘     └──────────────┘    └───────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

**Alternativas a Room:**

| Alternativa | Tipo | Cuando usarla |
|-------------|------|---------------|
| **Room** | SQLite ORM | Base de datos relacional |
| **DataStore** | Key-Value | Configuraciones simples |
| **Firebase Firestore** | Cloud | Sincronizacion en la nube |
| **SharedPreferences** | Key-Value | Solo ajustes pequenos |

### Archivos de Configuracion de Gradle

```
MiAppNotas/
├── build.gradle.kts           ← Configuracion raiz (plugins globales)
├── settings.gradle.kts        ← Que modulos existen
├── gradle.properties          ← Propiedades de Gradle
└── app/
    └── build.gradle.kts       ← Configuracion del modulo app
```

#### gradle/libs.versions.toml (Catalogo de Versiones)

Define todas las versiones en un solo lugar:

```toml
[versions]
kotlin = "2.1.10"
agp = "8.7.3"
room = "2.6.1"
ksp = "2.1.10-1.0.28"

[libraries]
androidx-room-runtime = { group = "androidx.room", name = "room-runtime", version.ref = "room" }
androidx-room-ktx = { group = "androidx.room", name = "room-ktx", version.ref = "room" }
androidx-room-compiler = { group = "androidx.room", name = "room-compiler", version.ref = "room" }

[plugins]
android-application = { id = "com.android.application", version.ref = "agp" }
kotlin-android = { id = "org.jetbrains.kotlin.android", version.ref = "kotlin" }
kotlin-ksp = { id = "com.google.devtools.ksp", version.ref = "ksp" }
```

**Beneficio**: Cambias la version en un solo lugar y se actualiza en todo el proyecto.

#### build.gradle.kts (raiz)

```kotlin
plugins {
    alias(libs.plugins.android.application) apply false
    alias(libs.plugins.kotlin.android) apply false
    alias(libs.plugins.kotlin.ksp) apply false
}
```

`apply false` = "declarar pero no usar todavia".

#### settings.gradle.kts

```kotlin
pluginManagement {
    repositories { google(); mavenCentral(); gradlePluginPortal() }
}
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories { google(); mavenCentral() }
}
rootProject.name = "MiAppNotas"
include(":app")
```

---

## PARTE 0: CONFIGURAR JDK, EMULADORES Y HERRAMIENTAS

### 0.1 La JDK y para que sirve

La **JDK** (Java Development Kit) es el kit que necesitas para compilar tu app Android.

**Para que la necesitas:**
- Compilar tu codigo Kotlin a bytecode
- Ejecutar Gradle
- Ejecutar herramientas como D8, R8, aapt2

**NO la necesitas en el celular.** El celular solo necesita el APK compilado.

**Configurar el JDK en Android Studio:**

1. Ve a **File → Settings → Build, Execution, Deployment → Build Tools → Gradle**
2. En **Gradle JDK**, selecciona:
   - `jbr-21` (JetBrains Runtime 21) o `Embedded JDK`
3. Si no aparece, click en **Download JDK** y elige version 21, vendor JetBrains

**JAVA_HOME:** Variable de entorno de Windows que dice donde esta la JDK. Si Gradle falla buscando `jlink.exe` en una ruta de VS Code, significa que `JAVA_HOME` esta mal configurado.

Para arreglarlo, abre PowerShell:
```powershell
[System.Environment]::SetEnvironmentVariable("JAVA_HOME", "C:\Program Files\Android\Android Studio\jbr", "User")
```

### 0.2 Kotlin: Donde corre tu codigo

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

**Kotlin NO usa la JDK para ejecutarse en el celular.** Usa la JDK solo para compilar. El celular usa **ART** (Android Runtime).

### 0.3 Garbage Collector en Android

El **Garbage Collector** (GC) libera memoria de objetos que ya no se usan automaticamente.

**En Android:** ART tiene su propio GC. No necesitas llamarlo manualmente.

**Como funciona:**
- Creas objetos (`val nota = Nota(...)`), se guardan en memoria heap
- Cuando ninguna variable referencia ese objeto, el GC lo elimina
- El GC se ejecuta automaticamente cuando necesita memoria

**Que significa para ti:**
- No necesitas liberar memoria manualmente
- Si dejas referencias colgadas (listener que nunca quitas), es un **memory leak**
- Usa `lifecycleScope` para que las corrutinas se limpien solas

### 0.4 Device Manager (Crear Emuladores)

El Device Manager es donde gestionas los emuladores.

**Como abrirlo:**
- Barra superior de Android Studio → icono de celular con engranaje
- O: **Tools → Device Manager**

**Crear un emulador paso a paso:**

1. Click en **Create Device**
2. Elegi hardware. Recomendados:
   - **Pixel 7** (1080x2400, buen rendimiento)
   - **Pixel 6** (si tu PC es mas modesta)
   - **Nexus 5X** (si tu PC tiene poca RAM)
3. Elegi una imagen del sistema:
   - **API 34** (Android 14) es buena opcion
   - Si no esta descargada, click en la flecha ↓ al lado del nombre
4. Configuraciones importantes:
   - **RAM:** 2048 MB minimo, 4096 recomendado
   - **VM Heap:** 256 MB
   - **Internal Storage:** 8096 MB
   - **Boot:** Quick Boot (arranca mas rapido)
   - **Graphics:** Hardware - GLES 2.0 (si tenes GPU) o Software (si no)
5. Click **Finish**

**Emular en diferentes dispositivos:**

Para probar como se ve tu app en distintos tamanios de pantalla, crea varios emuladores:

| Dispositivo | Tamanio | DPI | Uso |
|-------------|---------|-----|-----|
| Pixel 7 | 6.3" | 416 | Telefono estandar |
| Pixel Fold | 7.6" | 420 | Plegable |
| Pixel Tablet | 11" | 276 | Tablet |
| Nexus 10 | 10.1" | 320 | Tablet grande |

**Atajos utiles del emulador:**
- `Ctrl + F11`: Rotar pantalla
- `Ctrl + M`: Menu
- `Ctrl + Back`: Boton atras
- Barra lateral del emulador: Simular ubicacion GPS, batera, red, etc.

### 0.5 Edit Configurations

Donde configuras como se ejecuta tu app.

**Como abrirlo:**
- Click en el dropdown donde dice "app" en la barra superior
- **Edit Configurations...**

**Opciones:**

| Opcion | Para que sirve |
|--------|---------------|
| **Module** | Que modulo se ejecuta (normalmente `app`) |
| **Deployment Target** | En que dispositivo se ejecuta |
| **Launch Options** | Que Activity se lanza al inicio |

### 0.6 Profiles (Perfiles de compilacion)

| Profile | Para que es | Caracteristicas |
|---------|-------------|-----------------|
| **debug** | Desarrollo | Sin ofuscacion, logs habilitados |
| **release** | Produccion | Ofuscacion con R8, sin logs, optimizada |

Se configuran en `app/build.gradle.kts`:

```kotlin
buildTypes {
    release {
        isMinifyEnabled = true
        proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro")
    }
    debug {
        isDebuggable = true
    }
}
```

### 0.7 Debugging en Android Studio

**Poner un breakpoint:**
1. Click en el margen izquierdo de una linea de codigo
2. Aparece un punto rojo

**Ejecutar en modo debug:**
- Click en el icono del bicho (bug) en la barra superior
- O: **Shift + F9**

**Controles cuando llega al breakpoint:**

| Accion | Atajo | Que hace |
|--------|-------|----------|
| Step Over | F8 | Ejecuta la linea actual y avanza |
| Step Into | F7 | Entra dentro de la funcion |
| Step Out | Shift + F8 | Sale de la funcion actual |
| Resume | F9 | Continua hasta el proximo breakpoint |

**Ver logs:** Pestaña **Logcat** en la parte inferior. Niveles: `Log.d()`, `Log.i()`, `Log.e()`, `Log.w()`

### 0.8 Mirroring (ver celular en la PC)

**Opcion 1: Android Studio Device Mirroring**

1. Activa **Opciones de desarrollador**: Settings → About phone → toca "Build number" 7 veces
2. Activa **USB Debugging**: Settings → Developer options → USB debugging → ON
3. Conecta el celular por USB
4. Acepta el permiso en el celular
5. En Android Studio, el celular aparece en el dropdown

**Opcion 2: scrcpy (gratis, recomendado)**

1. Descarga scrcpy: https://github.com/Genymobile/scrcpy
2. Activa USB Debugging
3. Conecta por USB
4. Ejecuta `scrcpy` en la terminal

**Opcion 3: Wireless Debugging**

1. Activa **Wireless debugging** en Developer options
2. Misma red WiFi que tu PC
3. **Device Manager → Pair using QR code**

---

## PARTE 1: CREAR EL PROYECTO

### 1.1 Nuevo Proyecto

1. Abre Android Studio
2. **File → New → New Project**
3. Aqui viene la primera decision importante:

**Opcion A — Empty Views Activity (XML):**
- Elige **"Empty Views Activity"**
- Usa layouts XML y Views tradicionales

**Opcion B — Empty Activity (Compose):**
- Elige **"Empty Activity"** (la que tiene el logo de Compose)
- Usa Jetpack Compose

**Para esta clase, empezamos con Opcion A (XML).** Luego haremos la version Compose.

4. Configura:

```
Name:           MiAppNotas
Package name:   com.misitioweb.miappnotas
Language:       Kotlin
Minimum SDK:    API 26 (Android 8.0)
Build Config:   Kotlin DSL (build.gradle.kts)
```

5. Click **Finish**
6. Espera a que termine Gradle Sync

### 1.2 Ver que se creo

**Enfoque XML/Views:**
```
MiAppNotas/
├── build.gradle.kts
├── settings.gradle.kts
├── gradle/libs.versions.toml
└── app/
    ├── build.gradle.kts
    └── src/main/
        ├── AndroidManifest.xml
        ├── java/com/misitioweb/miappnotas/
        │   └── MainActivity.kt
        └── res/
            ├── layout/
            │   └── activity_main.xml     ← AQUI VA LA UI
            └── ... (valores, drawable, etc)
```

**Enfoque Compose:**
```
MiAppNotas/
├── build.gradle.kts
├── settings.gradle.kts
├── gradle/libs.versions.toml
└── app/
    ├── build.gradle.kts
    └── src/main/
        ├── AndroidManifest.xml
        ├── java/com/misitioweb/miappnotas/
        │   ├── MainActivity.kt
        │   └── ui/theme/
        │       ├── Color.kt
        │       ├── Theme.kt
        │       └── Type.kt
        └── res/
            └── ... (sin layout XML)
```

**Diferencia clave:** En XML los archivos de UI estan en `res/layout/`. En Compose, la UI se escribe directamente en Kotlin.

---

## PARTE 2: XML/Views VS JETPACK COMPOSE — LA GRAN DIFERENCIA

### 2.1 ¿Cual es la diferencia fundamental?

**XML/Views (enfoque clasico):**
```
UI = archivos XML separados + codigo Kotlin que los manipula

activity_main.xml                    MainActivity.kt
┌─────────────────┐                  ┌───────────────────────┐
│ <TextView       │   findViewById   │ val tv =              │
│   id="@+id/tv"  │ ◀────────────── │   findViewById(...)   │
│   text="Hola"   │                  │ tv.text = "Nuevo"     │
│ />              │                  │                       │
└─────────────────┘                  └───────────────────────┘
  DESCRIBE la UI                     MODIFICA la UI
```

**Jetpack Compose (enfoque moderno):**
```
UI = solo codigo Kotlin declarativo

MainActivity.kt
┌──────────────────────────────────────────┐
│ @Composable                              │
│ fun Pantalla() {                         │
│     Text("Hola")  ← Se redibuja solo     │
│ }                                        │
│                                          │
│ DESCRIBE + MODIFICA en el mismo lugar    │
└──────────────────────────────────────────┘
```

### 2.2 Comparacion lado a lado

| Aspecto | XML/Views | Jetpack Compose |
|---------|-----------|-----------------|
| **Donde se escribe la UI** | Archivos XML en `res/layout/` | Funciones `@Composable` en Kotlin |
| **Como se referencia un elemento** | `findViewById(R.id.miVista)` | Estado (`var texto by mutableStateOf("")`) |
| **Como se actualiza la UI** | `miTextView.text = "nuevo"` manualmente | Cambias el estado y Compose redibuja solo |
| **Listas** | `RecyclerView` + `Adapter` + `ViewHolder` (3 clases) | `LazyColumn` (1 bloque de codigo) |
| **Animaciones** | XML animators o codigo imperativo | Modificadores declarativos |
| **Preview en vivo** | Design tab en XML | `@Preview` composable + Interactive Preview |
| **Curva de aprendizaje** | Mas facile de entender al inicio | Requiere pensar de forma declarativa |
| **Boilerplate** | Mucho codigo repetitivo | Menos codigo, mas expresivo |
| **Estado** | Lo manejas manualmente | Estado es la fuente de verdad |

### 2.3 Ejemplo concreto: Un contador

**XML/Views:**
```kotlin
// activity_main.xml
<Button id="@+id/btn" text="Clicks: 0" />

// MainActivity.kt
var contador = 0
val btn = findViewById<Button>(R.id.btn)
btn.setOnClickListener {
    contador++
    btn.text = "Clicks: $contador"  // Actualizacion MANUAL
}
```

**Compose:**
```kotlin
@Composable
fun Contador() {
    var contador by remember { mutableStateOf(0) }
    Button(onClick = { contador++ }) {
        Text("Clicks: $contador")  // Se redibuja SOLO
    }
}
```

**En XML:** Tienes que buscar la vista, y actualizarla manualmente cada vez que cambian los datos.

**En Compose:** Declaras el estado, y cada vez que cambia, la UI se redibuja automaticamente.

### 2.4 ¿Por que Google migro a Compose?

1. **Menos codigo:** Un RecyclerView necesita 3 clases. Un LazyColumn necesita 1 bloque.
2. **Menos bugs:** No hay `NullPointerException` por `findViewById` que devuelve null.
3. **State-driven:** La UI siempre refleja el estado actual. No hay inconsistencias.
4. **Reusable:** Los Composables son funciones, se reusan facilmente.
5. **Preview interactivo:** Ves los cambios en tiempo real sin compilar.

### 2.5 ¿Debo aprender XML si existe Compose?

**Si.** Porque:
- Muchos proyectos legacy usan XML
- Algunas librerias todavia requieren Views
- Entender ambos enfoques te hace mejor desarrollador
- La transicion de XML a Compose es gradual (puedes mezclar ambos)

---

## PARTE 3: AGREGAR DEPENDENCIAS (ENFOQUE XML)

### 3.1 Actualizar gradle/libs.versions.toml

```toml
[versions]
agp = "8.7.3"
kotlin = "2.1.10"
room = "2.6.1"
ksp = "2.1.10-1.0.28"
material = "1.11.0"

[libraries]
androidx-core-ktx = { group = "androidx.core", name = "core-ktx", version = "1.12.0" }
androidx-appcompat = { group = "androidx.appcompat", name = "appcompat", version = "1.6.1" }
androidx-recyclerview = { group = "androidx.recyclerview", name = "recyclerview", version = "1.3.2" }
androidx-room-runtime = { group = "androidx.room", name = "room-runtime", version.ref = "room" }
androidx-room-ktx = { group = "androidx.room", name = "room-ktx", version.ref = "room" }
androidx-room-compiler = { group = "androidx.room", name = "room-compiler", version.ref = "room" }
material = { group = "com.google.android.material", name = "material", version.ref = "material" }

[plugins]
android-application = { id = "com.android.application", version.ref = "agp" }
kotlin-android = { id = "org.jetbrains.kotlin.android", version.ref = "kotlin" }
kotlin-ksp = { id = "com.google.devtools.ksp", version.ref = "ksp" }
```

### 3.2 app/build.gradle.kts

```kotlin
plugins {
    alias(libs.plugins.android.application)
    alias(libs.plugins.kotlin.android)
    alias(libs.plugins.kotlin.ksp)
}

android {
    namespace = "com.misitioweb.miappnotas"
    compileSdk = 35

    defaultConfig {
        applicationId = "com.misitioweb.miappnotas"
        minSdk = 26
        targetSdk = 35
        versionCode = 1
        versionName = "1.0"
    }

    buildFeatures {
        viewBinding = true  // IMPORTANTE para XML/Views
    }
}

dependencies {
    implementation(libs.androidx.core.ktx)
    implementation(libs.androidx.appcompat)
    implementation(libs.androidx.recyclerview)
    implementation(libs.material)

    // Room
    implementation(libs.androidx.room.runtime)
    implementation(libs.androidx.room.ktx)
    ksp(libs.androidx.room.compiler)
}
```

### 3.3 Click en **Sync Now**

Si termina sin errores, estas listo.

---

## PARTE 4: LA BASE DE DATOS (ROOM) — IGUAL EN AMBOS ENFOQUES

### 4.1 Crear paquetes de organizacion

```
app → src → main → java → com.misitioweb.miappnotas
```

Click derecho sobre el paquete:

```
New → Package → data → New → Package → local
```

Ahora tenes: `com.misitioweb.miappnotas.data.local`

### 4.2 La Entidad Nota

Click derecho sobre `data.local`:

```
New → Kotlin Class/File → Class
```

Nombre: **Nota**

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

**Que significa cada cosa:**

| Anotacion | Para que |
|-----------|----------|
| `@Entity(tableName = "notas")` | Esta clase es una tabla llamada "notas" |
| `@PrimaryKey(autoGenerate = true)` | El ID se genera automaticamente |
| `data class` | Clase especial de Kotlin que genera `equals()`, `hashCode()`, `toString()` y `copy()` automaticamente |

### 4.3 El DAO

En `data.local`:

```
New → Kotlin Class/File → Interface
```

Nombre: **NotaDao**

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

**Conceptos clave:**

- `@Dao`: Room genera la implementacion automaticamente
- `Flow<List<Nota>>`: Stream reactivo. Cada vez que la BD cambia, emite una nueva lista
- `suspend`: Puede pausar sin bloquear el hilo principal
- `:id` en la query: Parametro que se reemplaza con el argumento

### 4.4 La Base de Datos

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

**Patron Singleton thread-safe:**

```
@Volatile → Todos los hilos ven el mismo valor
     +
synchronized(this) → Solo un hilo ejecuta el bloque a la vez
     =
Una sola instancia de la base de datos, sin importar cuantos hilos la pidan
```

### 4.5 El Repositorio

Click derecho sobre `data`:

```
New → Package → repository
```

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

**Inyeccion de dependencias manual:** El repositorio recibe el DAO en el constructor.

### 4.6 Compilar

**Build → Make Project** (Ctrl + F9). Si dice "Build successful", segui.

---

## PARTE 5: ENFOQUE XML/VIEWS — LA UI

### 5.1 Layout Principal

Abre `res/layout/activity_main.xml` y reemplaza todo:

```xml
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout
    xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:padding="8dp">

    <TextView
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="Mis Notas"
        android:textSize="24sp"
        android:textStyle="bold"
        android:padding="8dp"
        android:gravity="center" />

    <androidx.recyclerview.widget.RecyclerView
        android:id="@+id/recyclerNotas"
        android:layout_width="match_parent"
        android:layout_height="0dp"
        android:layout_weight="1" />

    <Button
        android:id="@+id/btnSensor"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_margin="4dp"
        android:text="Probar Sensores" />

    <Button
        android:id="@+id/btnRecordar"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_margin="4dp"
        android:text="Iniciar Recordatorio" />

</LinearLayout>
```

**Elementos clave:**

| Elemento | Para que |
|----------|----------|
| `LinearLayout` | Contenedor que organiza hijos en una fila o columna |
| `android:orientation="vertical"` | Los hijos van uno debajo del otro |
| `android:layout_weight="1"` | El RecyclerView ocupa todo el espacio disponible |
| `android:id="@+id/..."` | Identificador unico para encontrar la vista con `findViewById` |

### 5.2 Layout de Cada Nota

Click derecho en `res/layout`:

```
New → Layout Resource File
```

Nombre: **item_nota**

```xml
<?xml version="1.0" encoding="utf-8"?>
<com.google.android.material.card.MaterialCardView
    xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:layout_marginBottom="8dp"
    app:cardCornerRadius="8dp"
    app:cardElevation="2dp">

    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="vertical"
        android:padding="12dp">

        <TextView
            android:id="@+id/tvTitulo"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:text="Titulo"
            android:textSize="16sp"
            android:textStyle="bold" />

        <TextView
            android:id="@+id/tvContenido"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:layout_marginTop="4dp"
            android:maxLines="2"
            android:text="Contenido..." />

        <TextView
            android:id="@+id/tvFecha"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:layout_marginTop="4dp"
            android:textSize="10sp"
            android:textColor="#888888" />

    </LinearLayout>
</com.google.android.material.card.MaterialCardView>
```

### 5.3 El Adaptador (RecyclerView.Adapter)

Click derecho en el paquete `com.misitioweb.miappnotas`:

```
New → Kotlin Class/File → Class
```

Nombre: **NotaAdaptador**

```kotlin
package com.misitioweb.miappnotas

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.DiffUtil
import androidx.recyclerview.widget.ListAdapter
import androidx.recyclerview.widget.RecyclerView

class NotaAdaptador(
    private val alClickar: (Nota) -> Unit
) : ListAdapter<Nota, NotaAdaptador.NotaViewHolder>(NotaDiff()) {

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): NotaViewHolder {
        val vista = LayoutInflater.from(parent.context)
            .inflate(R.layout.item_nota, parent, false)
        return NotaViewHolder(vista)
    }

    override fun onBindViewHolder(holder: NotaViewHolder, position: Int) {
        holder.bind(getItem(position))
    }

    inner class NotaViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        private val tvTitulo: TextView = itemView.findViewById(R.id.tvTitulo)
        private val tvContenido: TextView = itemView.findViewById(R.id.tvContenido)
        private val tvFecha: TextView = itemView.findViewById(R.id.tvFecha)

        init {
            itemView.setOnClickListener {
                val posicion = bindingAdapterPosition
                if (posicion != RecyclerView.NO_POSITION) {
                    alClickar(getItem(posicion))
                }
            }
        }

        fun bind(nota: Nota) {
            tvTitulo.text = nota.titulo
            tvContenido.text = nota.contenido
            val fecha = java.text.SimpleDateFormat("dd/MM/yyyy HH:mm", java.util.Locale.getDefault())
            tvFecha.text = fecha.format(java.util.Date(nota.fechaCreacion))
        }
    }

    class NotaDiff : DiffUtil.ItemCallback<Nota>() {
        override fun areItemsTheSame(oldItem: Nota, newItem: Nota) = oldItem.id == newItem.id
        override fun areContentsTheSame(oldItem: Nota, newItem: Nota) = oldItem == newItem
    }
}
```

**Como funciona RecyclerView:**

```
┌──────────────────────────────────────────────────────────────┐
│  RecyclerView                                                │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  Adapter (NotaAdaptador)                               │  │
│  │  ┌──────────────────────────────────────────────────┐  │  │
│  │  │  ViewHolder 1 → item_nota.xml → Nota 1           │  │  │
│  │  │  ViewHolder 2 → item_nota.xml → Nota 2           │  │  │
│  │  │  ViewHolder 3 → item_nota.xml → Nota 3           │  │  │
│  │  │  ... (solo los visibles en pantalla)              │  │  │
│  │  └──────────────────────────────────────────────────┘  │  │
│  └────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

**ViewHolder:** Reutiliza las vistas. En vez de crear un nuevo item_nota.xml cada vez, recicla los que salieron de pantalla.

**DiffUtil:** Compara la lista vieja con la nueva y solo actualiza los items que cambiaron. Mas eficiente que `notifyDataSetChanged()`.

### 5.4 MainActivity (XML/Views)

Abre `MainActivity.kt`:

```kotlin
package com.misitioweb.miappnotas

import android.content.Intent
import android.os.Bundle
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.lifecycleScope
import androidx.recyclerview.widget.LinearLayoutManager
import com.misitioweb.miappnotas.databinding.ActivityMainBinding
import kotlinx.coroutines.flow.collectLatest
import kotlinx.coroutines.launch

class MainActivity : AppCompatActivity() {

    private lateinit var binding: ActivityMainBinding
    private lateinit var adapter: NotaAdaptador
    private lateinit var repositorio: NotaRepositorio

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        // ViewBinding: genera clases automaticas para cada layout XML
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        val database = NotaDatabase.obtener(applicationContext)
        repositorio = NotaRepositorio(database.notaDao())

        setupRecyclerView()
        setupBotones()
        observarNotas()
    }

    private fun setupRecyclerView() {
        adapter = NotaAdaptador { nota ->
            val intent = Intent(this, EditarNotaActivity::class.java)
            intent.putExtra("nota_id", nota.id)
            startActivity(intent)
        }

        binding.recyclerNotas.apply {
            layoutManager = LinearLayoutManager(this@MainActivity)
            adapter = this@MainActivity.adapter
        }
    }

    private fun setupBotones() {
        binding.btnSensor.setOnClickListener {
            startActivity(Intent(this, SensorActivity::class.java))
        }

        binding.btnRecordar.setOnClickListener {
            startService(Intent(this, RecordatorioService::class.java))
            Toast.makeText(this, "Recordatorio iniciado", Toast.LENGTH_SHORT).show()
        }
    }

    private fun observarNotas() {
        lifecycleScope.launch {
            repositorio.todasLasNotas.collectLatest { notas ->
                adapter.submitList(notas)
            }
        }
    }
}
```

**ViewBinding:** En vez de usar `findViewById<TextView>(R.id.tvTitulo)`, ViewBinding genera una clase `ActivityMainBinding` con todas las vistas tipadas. Si el XML cambia, el binding se actualiza en compilacion.

**`lifecycleScope.launch`:** Inicia una corrutina ligada al ciclo de vida de la Activity. Si la Activity se destruye, la corrutina se cancela automaticamente.

### 5.5 Habilitar ViewBinding

Si no funciona `ActivityMainBinding`, agrega en `app/build.gradle.kts`:

```kotlin
android {
    ...
    buildFeatures {
        viewBinding = true
    }
}
```

Y sincroniza.

---

## PARTE 6: EDITAR NOTA ACTIVITY (XML/Views)

### 6.1 Crear la Activity

Click derecho en el paquete:

```
New → Activity → Empty Views Activity
```

Nombre: **EditarNotaActivity**

### 6.2 El Layout

Abre `activity_editar_nota.xml`:

```xml
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout
    xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:padding="16dp">

    <TextView
        android:id="@+id/tvTituloPantalla"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="Nueva Nota"
        android:textSize="24sp"
        android:textStyle="bold"
        android:layout_marginBottom="16dp" />

    <com.google.android.material.textfield.TextInputLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:hint="Titulo"
        style="@style/Widget.MaterialComponents.TextInputLayout.OutlinedBox">

        <com.google.android.material.textfield.TextInputEditText
            android:id="@+id/etTitulo"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:inputType="textCapSentences" />

    </com.google.android.material.textfield.TextInputLayout>

    <com.google.android.material.textfield.TextInputLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_marginTop="16dp"
        android:hint="Contenido"
        style="@style/Widget.MaterialComponents.TextInputLayout.OutlinedBox">

        <com.google.android.material.textfield.TextInputEditText
            android:id="@+id/etContenido"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:inputType="textMultiLine|textCapSentences"
            android:minLines="5"
            android:gravity="top" />

    </com.google.android.material.textfield.TextInputLayout>

    <CheckBox
        android:id="@+id/cbImportante"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="16dp"
        android:text="Nota importante" />

    <Button
        android:id="@+id/btnGuardar"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_marginTop="24dp"
        android:text="Guardar" />

    <Button
        android:id="@+id/btnEliminar"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_marginTop="8dp"
        android:text="Eliminar"
        android:visibility="gone"
        android:textColor="#FF0000" />

</LinearLayout>
```

### 6.3 El Codigo

Abre `EditarNotaActivity.kt`:

```kotlin
package com.misitioweb.miappnotas

import android.os.Bundle
import android.view.View
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.lifecycleScope
import com.misitioweb.miappnotas.databinding.ActivityEditarNotaBinding
import kotlinx.coroutines.launch

class EditarNotaActivity : AppCompatActivity() {

    private lateinit var binding: ActivityEditarNotaBinding
    private lateinit var repositorio: NotaRepositorio
    private var notaId: Long = 0

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityEditarNotaBinding.inflate(layoutInflater)
        setContentView(binding.root)

        val database = NotaDatabase.obtener(applicationContext)
        repositorio = NotaRepositorio(database.notaDao())

        notaId = intent.getLongExtra("nota_id", 0)

        if (notaId > 0) {
            binding.tvTituloPantalla.text = "Editar Nota"
            binding.btnEliminar.visibility = View.VISIBLE
            cargarNota()
        }

        setupBotones()
    }

    private fun setupBotones() {
        binding.btnGuardar.setOnClickListener { guardar() }
        binding.btnEliminar.setOnClickListener { eliminar() }
    }

    private fun cargarNota() {
        lifecycleScope.launch {
            val nota = repositorio.obtenerPorId(notaId)
            if (nota != null) {
                binding.etTitulo.setText(nota.titulo)
                binding.etContenido.setText(nota.contenido)
                binding.cbImportante.isChecked = nota.esImportante
            }
        }
    }

    private fun guardar() {
        val titulo = binding.etTitulo.text.toString().trim()
        val contenido = binding.etContenido.text.toString().trim()

        if (titulo.isEmpty()) {
            binding.etTitulo.error = "El titulo es obligatorio"
            return
        }

        lifecycleScope.launch {
            val nota = Nota(
                id = if (notaId > 0) notaId else 0,
                titulo = titulo,
                contenido = contenido,
                esImportante = binding.cbImportante.isChecked
            )

            if (notaId > 0) {
                repositorio.actualizar(nota)
                Toast.makeText(this@EditarNotaActivity, "Nota actualizada", Toast.LENGTH_SHORT).show()
            } else {
                repositorio.insertar(nota)
                Toast.makeText(this@EditarNotaActivity, "Nota creada", Toast.LENGTH_SHORT).show()
            }
            finish()
        }
    }

    private fun eliminar() {
        lifecycleScope.launch {
            val nota = repositorio.obtenerPorId(notaId)
            if (nota != null) {
                repositorio.eliminar(nota)
                Toast.makeText(this@EditarNotaActivity, "Eliminada", Toast.LENGTH_SHORT).show()
                finish()
            }
        }
    }
}
```

### 6.4 Declarar en el Manifest

En `AndroidManifest.xml`, dentro de `<application>`:

```xml
<activity
    android:name=".EditarNotaActivity"
    android:exported="false" />
```

---

## PARTE 7: SERVICE — RECORDATORIO EN SEGUNDO PLANO

### 7.1 Crear el Service

Click derecho:

```
New → Service → Service
```

Nombre: **RecordatorioService**

```kotlin
package com.misitioweb.miappnotas

import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.app.Service
import android.content.Intent
import android.os.IBinder
import androidx.core.app.NotificationCompat

class RecordatorioService : Service() {

    private var hilo: Thread? = null
    private var corriendo = false

    override fun onCreate() {
        super.onCreate()
        crearCanal()
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        corriendo = true

        hilo = Thread {
            var contador = 0
            while (corriendo && contador < 30) {
                try {
                    if (contador == 10) {
                        mostrarNotificacion()
                    }
                    Thread.sleep(1000)
                    contador++
                } catch (e: InterruptedException) {
                    break
                }
            }
            stopSelf()
        }
        hilo?.start()

        return START_STICKY
    }

    override fun onBind(intent: Intent?) = null

    override fun onDestroy() {
        super.onDestroy()
        corriendo = false
        hilo?.interrupt()
    }

    private fun crearCanal() {
        val canal = NotificationChannel(
            CANAL_ID, "Recordatorio", NotificationManager.IMPORTANCE_DEFAULT
        )
        canal.description = "Recordatorio de notas"
        getSystemService(NotificationManager::class.java).createNotificationChannel(canal)
    }

    private fun mostrarNotificacion() {
        val intent = Intent(this, MainActivity::class.java)
        val pendingIntent = PendingIntent.getActivity(
            this, 0, intent, PendingIntent.FLAG_IMMUTABLE
        )

        val notificacion = NotificationCompat.Builder(this, CANAL_ID)
            .setSmallIcon(android.R.drawable.ic_menu_agenda)
            .setContentTitle("Recordatorio")
            .setContentText("Revisa tus notas")
            .setContentIntent(pendingIntent)
            .setAutoCancel(true)
            .build()

        getSystemService(NotificationManager::class.java).notify(NOTIF_ID, notificacion)
    }

    companion object {
        const val CANAL_ID = "recordatorio_canal"
        const val NOTIF_ID = 1
    }
}
```

### 7.2 Declarar en el Manifest

```xml
<service
    android:name=".RecordatorioService"
    android:enabled="true"
    android:exported="false" />
```

### 7.3 Como funciona un Service

```
MainActivity                  RecordatorioService
     │                               │
     │  startService(Intent)         │
     │──────────────────────────────▶│
     │                               │ onCreate() → crea canal notificacion
     │                               │ onStartCommand() → inicia hilo
     │                               │   hilo: cuenta 30 segundos
     │                               │   segundo 10: muestra notificacion
     │                               │   segundo 30: stopSelf()
     │                               │
     │                               │ onDestroy() → limpia
```

**START_STICKY:** Si el sistema mata el Service, lo reinicia automaticamente (con `intent` null).

---

## PARTE 8: BroadcastReceiver — ESCUCHAR EVENTOS DEL SISTEMA

### 8.1 Crear el Receiver

Click derecho:

```
New → Other → Broadcast Receiver
```

Nombre: **EventoReceiver**

```kotlin
package com.misitioweb.miappnotas

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.widget.Toast

class EventoReceiver : BroadcastReceiver() {

    override fun onReceive(context: Context?, intent: Intent?) {
        when (intent?.action) {
            Intent.ACTION_BOOT_COMPLETED -> {
                Toast.makeText(context, "App lista tras reinicio", Toast.LENGTH_SHORT).show()
            }
            Intent.ACTION_BATTERY_LOW -> {
                Toast.makeText(context, "Bateria baja!", Toast.LENGTH_LONG).show()
            }
        }
    }
}
```

### 8.2 Declarar en el Manifest

```xml
<receiver
    android:name=".EventoReceiver"
    android:enabled="true"
    android:exported="false">
    <intent-filter>
        <action android:name="android.intent.action.BOOT_COMPLETED" />
        <action android:name="android.intent.action.BATTERY_LOW" />
    </intent-filter>
</receiver>

<uses-permission android:name="android.permission.RECEIVE_BOOT_COMPLETED" />
```

### 8.3 Como funciona un BroadcastReceiver

```
Sistema Android                  EventoReceiver
       │                               │
       │  BOOT_COMPLETED               │
       │  (celular encendio)           │
       │──────────────────────────────▶│
       │                               │ onReceive() → muestra Toast
       │
       │  BATTERY_LOW                  │
       │  (bateria < 15%)              │
       │──────────────────────────────▶│
       │                               │ onReceive() → muestra Toast
```

---

## PARTE 9: SENSORES — ACELEROMETRO

### 9.1 Crear Activity

Click derecho:

```
New → Activity → Empty Views Activity
```

Nombre: **SensorActivity**

### 9.2 Layout

Abre `activity_sensor.xml`:

```xml
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout
    xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:gravity="center"
    android:padding="24dp"
    android:background="#E8F5E9">

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Prueba de Sensores"
        android:textSize="24sp"
        android:textStyle="bold" />

    <TextView
        android:id="@+id/tvValores"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="32dp"
        android:text="X: 0 | Y: 0 | Z: 0"
        android:textSize="18sp"
        android:fontFamily="monospace" />

    <ImageView
        android:id="@+id/ivIcono"
        android:layout_width="100dp"
        android:layout_height="100dp"
        android:layout_marginTop="32dp"
        android:src="@android:drawable/ic_menu_compass" />

</LinearLayout>
```

### 9.3 Codigo

```kotlin
package com.misitioweb.miappnotas

import android.content.Context
import android.hardware.Sensor
import android.hardware.SensorEvent
import android.hardware.SensorEventListener
import android.hardware.SensorManager
import android.os.Bundle
import android.widget.ImageView
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity

class SensorActivity : AppCompatActivity(), SensorEventListener {

    private lateinit var sm: SensorManager
    private var acelerometro: Sensor? = null

    private lateinit var tvValores: TextView
    private lateinit var ivIcono: ImageView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_sensor)

        tvValores = findViewById(R.id.tvValores)
        ivIcono = findViewById(R.id.ivIcono)

        sm = getSystemService(Context.SENSOR_SERVICE) as SensorManager
        acelerometro = sm.getDefaultSensor(Sensor.TYPE_ACCELEROMETER)
    }

    override fun onResume() {
        super.onResume()
        acelerometro?.let {
            sm.registerListener(this, it, SensorManager.SENSOR_DELAY_NORMAL)
        }
    }

    override fun onPause() {
        super.onPause()
        sm.unregisterListener(this)
    }

    override fun onSensorChanged(event: SensorEvent?) {
        event?.let {
            if (it.sensor.type == Sensor.TYPE_ACCELEROMETER) {
                val x = it.values[0]
                val y = it.values[1]
                val z = it.values[2]

                tvValores.text = "X: %.1f  Y: %.1f  Z: %.1f".format(x, y, z)

                ivIcono.rotation = when {
                    x > 5 -> 90f
                    x < -5 -> -90f
                    else -> 0f
                }
            }
        }
    }

    override fun onAccuracyChanged(sensor: Sensor?, accuracy: Int) {}
}
```

### 9.4 Declarar en el Manifest

```xml
<activity
    android:name=".SensorActivity"
    android:exported="false" />
```

**Importante:** En el emulador, podes simular el acelerometro desde la barra lateral del emulador → "Extended controls" → "Sensors".

---

## PARTE 10: FRAGMENT — UI REUTILIZABLE

### 10.1 ¿Que es un Fragment?

Un **Fragment** es una porcion reutilizable de UI dentro de una Activity. Piensa en ello como un "mini-Activity" que vive dentro de otro Activity.

### 10.2 Crear un Fragment de detalle

Click derecho:

```
New → Fragment → Fragment (Blank)
```

Nombre: **NotaDetailFragment**

```kotlin
package com.misitioweb.miappnotas

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.fragment.app.Fragment

class NotaDetailFragment : Fragment() {

    private var notaId: Long = 0

    companion object {
        fun newInstance(notaId: Long): NotaDetailFragment {
            val fragment = NotaDetailFragment()
            val args = Bundle()
            args.putLong("nota_id", notaId)
            fragment.arguments = args
            return fragment
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        arguments?.let {
            notaId = it.getLong("nota_id")
        }
    }

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        return inflater.inflate(R.layout.fragment_nota_detail, container, false)
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        val tvDetalle = view.findViewById<TextView>(R.id.tvDetalle)
        tvDetalle.text = "Mostrando detalle de nota ID: $notaId"
    }
}
```

### 10.3 Layout del Fragment

`res/layout/fragment_nota_detail.xml`:

```xml
<?xml version="1.0" encoding="utf-8"?>
<FrameLayout
    xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:background="#E3F2FD"
    android:padding="24dp">

    <TextView
        android:id="@+id/tvDetalle"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="Detalle de nota"
        android:textSize="18sp"
        android:gravity="center" />

</FrameLayout>
```

### 10.4 ¿Por que usar Fragments?

- **Pantallas con tabs:** Cada tab es un Fragment
- **Tablets:** Master-detail (lista a la izquierda, detalle a la derecha)
- **Navegacion:** Bottom Navigation cambia Fragments
- **Reutilizacion:** El mismo Fragment en diferentes Activities

**En Compose:** Los Fragments se reemplazan por navegacion entre Composables. No necesitas Fragments.

---

## PARTE 11: CONTENTPROVIDER — COMPARTIR DATOS

### 11.1 ¿Que es un ContentProvider?

Un **ContentProvider** permite compartir datos entre aplicaciones. El sistema Android los usa para contactos, calendario, fotos, etc.

### 11.2 Ejemplo: Leer contactos del sistema

No necesitas crear tu propio ContentProvider para esta app. Pero si necesitas **usar** uno existente. Aqui un ejemplo de como leer contactos:

```kotlin
package com.misitioweb.miappnotas

import android.Manifest
import android.content.pm.PackageManager
import android.os.Bundle
import android.provider.ContactsContract
import android.widget.ArrayAdapter
import android.widget.ListView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat

class ContactosActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val listView = ListView(this)
        setContentView(listView)

        if (ContextCompat.checkSelfPermission(this, Manifest.permission.READ_CONTACTS)
            != PackageManager.PERMISSION_GRANTED
        ) {
            ActivityCompat.requestPermissions(
                this,
                arrayOf(Manifest.permission.READ_CONTACTS),
                1
            )
        } else {
            cargarContactos(listView)
        }
    }

    private fun cargarContactos(listView: ListView) {
        val contactos = mutableListOf<String>()

        // ContentResolver es como accedemos a ContentProviders
        val cursor = contentResolver.query(
            ContactsContract.CommonDataKinds.Phone.CONTENT_URI,
            null, null, null, null
        )

        cursor?.use {
            val nombreIdx = it.getColumnIndexOrThrow(ContactsContract.CommonDataKinds.Phone.DISPLAY_NAME)
            val telefonoIdx = it.getColumnIndexOrThrow(ContactsContract.CommonDataKinds.Phone.NUMBER)

            while (it.moveToNext()) {
                val nombre = it.getString(nombreIdx)
                val telefono = it.getString(telefonoIdx)
                contactos.add("$nombre - $telefono")
            }
        }

        listView.adapter = ArrayAdapter(this, android.R.layout.simple_list_item_1, contactos)
    }

    override fun onRequestPermissionsResult(
        requestCode: Int, permissions: Array<out String>, grantResults: IntArray
    ) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        if (requestCode == 1 && grantResults.isNotEmpty() && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
            cargarContactos(findViewById<ListView>(android.R.id.content))
        } else {
            Toast.makeText(this, "Permiso denegado", Toast.LENGTH_SHORT).show()
        }
    }
}
```

### 11.3 Declarar en el Manifest

```xml
<activity android:name=".ContactosActivity" android:exported="false" />
<uses-permission android:name="android.permission.READ_CONTACTS" />
```

---

## PARTE 12: INTEGRACION GOOGLE MAPS Y CALENDAR (SIN API KEY)

### 12.1 ¿Por que no necesitamos API key?

Usamos **Intents** para abrir apps externas. No necesitamos API keys porque:
- **Google Maps:** Usamos intents con URI `geo:` o `google.navigation:`
- **Google Calendar:** Usamos intents con `Intent.ACTION_INSERT` al calendario del sistema

La app delega el trabajo a la app de Google instalada en el celular.

### 12.2 Agregar permisos de Internet

En `AndroidManifest.xml`, antes de `<application>`:

```xml
<uses-permission android:name="android.permission.INTERNET" />
```

### 12.3 Abrir Google Maps con una ubicacion

Agrega una funcion en `EditarNotaActivity.kt`:

```kotlin
private fun abrirMapa() {
    val ubicacion = binding.etContenido.text.toString().trim()
    if (ubicacion.isEmpty()) {
        Toast.makeText(this, "Escribe una ubicacion en el contenido primero", Toast.LENGTH_SHORT).show()
        return
    }

    // Opcion 1: Busqueda por nombre
    val uri = Uri.parse("geo:0,0?q=${Uri.encode(ubicacion)}")
    val intent = Intent(Intent.ACTION_VIEW, uri)
    intent.setPackage("com.google.android.apps.maps")

    if (intent.resolveActivity(packageManager) != null) {
        startActivity(intent)
    } else {
        // Si no tiene Google Maps, abre en el navegador
        val webIntent = Intent(Intent.ACTION_VIEW,
            Uri.parse("https://www.google.com/maps/search/?api=1&query=${Uri.encode(ubicacion)}")
        )
        startActivity(webIntent)
    }
}
```

### 12.4 Abrir Google Maps con coordenadas especificas

```kotlin
private fun abrirMapaConCoordenadas(lat: Double, lng: Double) {
    val uri = Uri.parse("geo:$lat,$lng?q=$lat,$lng(Mi Nota)")
    val intent = Intent(Intent.ACTION_VIEW, uri)
    intent.setPackage("com.google.android.apps.maps")

    if (intent.resolveActivity(packageManager) != null) {
        startActivity(intent)
    }
}
```

### 12.5 Agregar evento a Google Calendar

```kotlin
private fun agregarACalendario() {
    val titulo = binding.etTitulo.text.toString().trim()
    if (titulo.isEmpty()) {
        Toast.makeText(this, "Escribe un titulo primero", Toast.LENGTH_SHORT).show()
        return
    }

    val calendarioIntent = Intent(Intent.ACTION_INSERT).apply {
        data = android.provider.CalendarContract.Events.CONTENT_URI
        putExtra(android.provider.CalendarContract.Events.TITLE, titulo)
        putExtra(android.provider.CalendarContract.Events.DESCRIPTION,
            binding.etContenido.text.toString().trim())
        putExtra(android.provider.CalendarContract.EXTRA_EVENT_BEGIN_TIME,
            System.currentTimeMillis())
        putExtra(android.provider.CalendarContract.EXTRA_EVENT_END_TIME,
            System.currentTimeMillis() + 3600000) // 1 hora despues
    }

    if (calendarioIntent.resolveActivity(packageManager) != null) {
        startActivity(calendarioIntent)
    } else {
        Toast.makeText(this, "No se encontro app de calendario", Toast.LENGTH_SHORT).show()
    }
}
```

### 12.6 Agregar botones en el layout de edicion

En `activity_editar_nota.xml`, agrega antes del cierre del LinearLayout:

```xml
    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_marginTop="16dp"
        android:orientation="horizontal">

        <Button
            android:id="@+id/btnMapa"
            android:layout_width="0dp"
            android:layout_height="wrap_content"
            android:layout_weight="1"
            android:layout_marginEnd="4dp"
            android:text="📍 Mapa"
            style="@style/Widget.MaterialComponents.Button.OutlinedButton" />

        <Button
            android:id="@+id/btnCalendario"
            android:layout_width="0dp"
            android:layout_height="wrap_content"
            android:layout_weight="1"
            android:layout_marginStart="4dp"
            android:text="📅 Calendario"
            style="@style/Widget.MaterialComponents.Button.OutlinedButton" />

    </LinearLayout>
```

### 12.7 Conectar los botones en EditarNotaActivity

En `setupBotones()`, agrega:

```kotlin
private fun setupBotones() {
    binding.btnGuardar.setOnClickListener { guardar() }
    binding.btnEliminar.setOnClickListener { eliminar() }
    binding.btnMapa.setOnClickListener { abrirMapa() }
    binding.btnCalendario.setOnClickListener { agregarACalendario() }
}
```

### 12.8 Como funcionan los Intents

```
Tu App                          Google Maps
  │                                 │
  │  Intent.ACTION_VIEW             │
  │  uri = "geo:0,0?q=Buenos Aires" │
  │────────────────────────────────▶│
  │                                 │ Abre el mapa con la busqueda
  │                                 │
Tu App                          Google Calendar
  │                                 │
  │  Intent.ACTION_INSERT           │
  │  CalendarContract.Events        │
  │────────────────────────────────▶│
  │                                 │ Abre formulario de nuevo evento
  │                                 │ con titulo y descripcion prellenados
```

**`resolveActivity()`:** Verifica que haya una app instalada que pueda manejar el Intent. Si no, puedes mostrar un mensaje o abrir en el navegador.

---

## PARTE 13: AndroidManifest.xml COMPLETO

```xml
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools">

    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.RECEIVE_BOOT_COMPLETED" />
    <uses-permission android:name="android.permission.READ_CONTACTS" />

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.MaterialComponents.DayNight.DarkActionBar">

        <activity
            android:name=".MainActivity"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>

        <activity
            android:name=".EditarNotaActivity"
            android:exported="false" />

        <activity
            android:name=".SensorActivity"
            android:exported="false" />

        <activity
            android:name=".ContactosActivity"
            android:exported="false" />

        <service
            android:name=".RecordatorioService"
            android:enabled="true"
            android:exported="false" />

        <receiver
            android:name=".EventoReceiver"
            android:enabled="true"
            android:exported="false">
            <intent-filter>
                <action android:name="android.intent.action.BOOT_COMPLETED" />
                <action android:name="android.intent.action.BATTERY_LOW" />
            </intent-filter>
        </receiver>

    </application>
</manifest>
```

---

## PARTE 14: DIAGRAMA DE ARQUITECTURA COMPLETA

### 14.1 Arquitectura de la App XML/Views

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         PRESENTACION (UI)                               │
│                                                                         │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────────┐  │
│  │   MainActivity   │  │ EditarNotaAct.   │  │   SensorActivity     │  │
│  │                  │  │                  │  │                      │  │
│  │  activity_main   │  │ activity_editar  │  │  activity_sensor     │  │
│  │  .xml            │  │ _nota.xml         │  │  .xml                │  │
│  │                  │  │                  │  │                      │  │
│  │  RecyclerView    │  │ TextInputLayout  │  │  SensorManager       │  │
│  │  NotaAdaptador   │  │ CheckBox         │  │  SensorEventListener │  │
│  └────────┬─────────┘  └────────┬─────────┘  └──────────────────────┘  │
│           │                     │                                       │
│           │  Intent             │  Intent                               │
│           ├─────────────────────▶│                                       │
│           │                     │                                       │
│           │                     │  ┌──────────────────────┐             │
│           │                     │  │ ContactosActivity    │             │
│           │                     │  │  (ContentProvider)   │             │
│           │                     │  └──────────────────────┘             │
│           │                     │                                       │
│           │                     │  ┌──────────────────────┐             │
│           │                     └─▶│ NotaDetailFragment   │             │
│           │                        │  (UI reutilizable)   │             │
│           │                        └──────────────────────┘             │
└───────────┼─────────────────────────────────────────────────────────────┘
            │
            │  llama directamente
            ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         DATOS                                           │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    NotaRepositorio                               │   │
│  │  (intermediario entre UI y base de datos)                        │   │
│  └──────────────────────────┬──────────────────────────────────────┘   │
│                             │                                           │
│                             ▼                                           │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                       NotaDao                                    │   │
│  │  (Data Access Object - traduce Kotlin a SQL)                     │   │
│  │                                                                  │   │
│  │  obtenerTodas() → Flow<List<Nota>>                               │   │
│  │  insertar(nota) → suspend                                        │   │
│  │  actualizar(nota) → suspend                                      │   │
│  │  eliminar(nota) → suspend                                        │   │
│  └──────────────────────────┬──────────────────────────────────────┘   │
│                             │                                           │
│                             ▼                                           │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    NotaDatabase                                  │   │
│  │  (Room - SQLite en el dispositivo)                               │   │
│  │                                                                  │   │
│  │  Singleton thread-safe (@Volatile + synchronized)                │   │
│  └─────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                    COMPONENTES EN SEGUNDO PLANO                         │
│                                                                         │
│  ┌──────────────────────┐    ┌──────────────────────┐                  │
│  │ RecordatorioService  │    │   EventoReceiver     │                  │
│  │                      │    │                      │                  │
│  │ Corre en background  │    │ Escucha eventos del  │                  │
│  │ Muestra notificacion │    │ sistema (boot, bat.) │                  │
│  │ despues de 10 seg    │    │                      │                  │
│  └──────────────────────┘    └──────────────────────┘                  │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                    INTEGRACIONES EXTERNAS (Intents)                     │
│                                                                         │
│  ┌──────────────────────┐    ┌──────────────────────┐                  │
│  │   Google Maps        │    │  Google Calendar     │                  │
│  │   (ACTION_VIEW)      │    │  (ACTION_INSERT)     │                  │
│  │   uri: geo:0,0?q=... │    │  Events.CONTENT_URI  │                  │
│  └──────────────────────┘    └──────────────────────┘                  │
└─────────────────────────────────────────────────────────────────────────┘
```

### 14.2 Flujo de datos completo

```
Usuario toca "Crear nota" (MainActivity)
         │
         ▼
Intent → EditarNotaActivity
         │
         ▼
Usuario escribe titulo + contenido
         │
         ▼
Toca "Guardar" → guardar()
         │
         ▼
lifecycleScope.launch {
    Nota(titulo, contenido)
    repositorio.insertar(nota)
         │
         ▼
    NotaDao.insertar(nota)  [suspend]
         │
         ▼
    Room genera SQL: INSERT INTO notas (...)
         │
         ▼
    SQLite guarda en notas_db
         │
         ▼
    Flow<List<Nota>> emite nueva lista
         │
         ▼
    repositorio.todasLasNotas recibe update
         │
         ▼
    adapter.submitList(notas)
         │
         ▼
    RecyclerView actualiza la lista
         │
         ▼
    Usuario ve la nueva nota
}
```

---

## PARTE 15: RESUMEN DE TODOS LOS COMPONENTES ANDROID

### 15.1 Los 4 componentes principales de Android

| Componente | Para que | Usado en esta clase? | Ejemplo |
|------------|----------|----------------------|---------|
| **Activity** | Una pantalla con UI | SI | MainActivity, EditarNotaActivity, SensorActivity |
| **Service** | Trabajo en segundo plano sin UI | SI | RecordatorioService |
| **BroadcastReceiver** | Escuchar eventos del sistema | SI | EventoReceiver |
| **ContentProvider** | Compartir datos entre apps | SI | ContactosActivity (usa el del sistema) |

### 15.2 Componentes adicionales

| Componente | Para que | Usado? |
|------------|----------|--------|
| **Fragment** | UI reutilizable dentro de un Activity | SI | NotaDetailFragment |
| **Intent** | Comunicacion entre componentes/apps | SI | Navegacion, Maps, Calendar |
| **ViewModel** | Estado que sobrevive rotaciones | NO en XML, SI en Compose |
| **RecyclerView** | Listas eficientes | SI | Lista de notas |
| **Room** | Base de datos SQLite | SI | Notas persistentes |
| **Notification** | Alertas fuera de la app | SI | RecordatorioService |
| **SensorManager** | Acceder a sensores del dispositivo | SI | Acelerometro |

### 15.3 Ciclo de vida de una Activity

```
                    onCreate()
                       │
                       ▼
                    onStart()
                       │
                       ▼
                    onResume()  ← La Activity es visible e interactiva
                       │
              ┌────────┴────────┐
              ▼                 ▼
         onPause()          onStop()
              │                 │
              ▼                 ▼
         onResume()         onRestart()
         (vuelve)              │
                               ▼
                            onStart()
                               │
                               ▼
                            onResume()

                    onStop()
                       │
                       ▼
                   onDestroy()  ← La Activity se destruye
```

---

## PARTE 16: COMPARACION FINAL — XML/Views vs COMPOSE

### 16.1 Lo que cambia

| Aspecto | XML/Views | Jetpack Compose |
|---------|-----------|-----------------|
| **UI** | Archivos XML separados | Funciones `@Composable` |
| **Referenciar vistas** | `findViewById` / ViewBinding | Estado (`mutableStateOf`) |
| **Actualizar UI** | Manual (`tv.text = ...`) | Automatico (cambia estado) |
| **Listas** | RecyclerView + Adapter (3 clases) | LazyColumn (1 bloque) |
| **Navegacion** | Intents entre Activities | Navegacion condicional o NavHost |
| **Estado** | Lo manejas tu | Estado es la fuente de verdad |
| **Preview** | Design tab | `@Preview` + Interactive Preview |
| **ViewMode** | No se usa generalmente | SI, con `collectAsState()` |

### 16.2 Cuando usar cada uno

**Usa XML/Views si:**
- Mantenes un proyecto existente
- Tu equipo no conoce Compose
- Necesitas una libreria que solo soporta Views
- Quieres entender la base historica de Android

**Usa Compose si:**
- Proyecto nuevo
- Quieres menos codigo y menos bugs
- Tu equipo esta dispuesto a aprender
- Quieres la direccion que Google recomienda

### 16.3 Puedes mezclar ambos

```kotlin
// En un layout XML puedes incluir Compose:
<androidx.compose.ui.platform.ComposeView
    android:id="@+id/compose_view"
    android:layout_width="match_parent"
    android:layout_height="wrap_content" />

// En tu Activity:
findViewById<ComposeView>(R.id.compose_view).setContent {
    MiComposable()
}
```

---

## PARTE 17: ESTRUCTURA FINAL DEL PROYECTO

```
MiAppNotas/
├── build.gradle.kts
├── settings.gradle.kts
├── gradle/libs.versions.toml
└── app/
    ├── build.gradle.kts
    └── src/main/
        ├── AndroidManifest.xml
        ├── java/com/misitioweb/miappnotas/
        │   ├── MainActivity.kt              (Lista de notas)
        │   ├── EditarNotaActivity.kt        (Crear/editar nota + Maps/Calendar)
        │   ├── SensorActivity.kt            (Acelerometro)
        │   ├── ContactosActivity.kt         (ContentProvider)
        │   ├── NotaAdaptador.kt             (RecyclerView Adapter)
        │   ├── NotaDetailFragment.kt        (Fragment reutilizable)
        │   ├── RecordatorioService.kt       (Service en background)
        │   ├── EventoReceiver.kt            (BroadcastReceiver)
        │   ├── data/
        │   │   ├── local/
        │   │   │   ├── Nota.kt              (Entidad Room)
        │   │   │   ├── NotaDao.kt           (DAO)
        │   │   │   └── NotaDatabase.kt      (Singleton BD)
        │   │   └── repository/
        │   │       └── NotaRepositorio.kt   (Repository)
        │   └── ui/ (para version Compose)
        │       ├── NotaViewModel.kt
        │       └── screens/
        │           ├── ListaNotasScreen.kt
        │           └── EditarNotaScreen.kt
        └── res/
            ├── layout/
            │   ├── activity_main.xml
            │   ├── activity_editar_nota.xml
            │   ├── activity_sensor.xml
            │   ├── item_nota.xml
            │   └── fragment_nota_detail.xml
            └── values/
                ├── strings.xml
                └── themes.xml
```

---

## PARTE 18: EJECUTAR Y PROBAR

### 18.1 En el emulador

1. Selecciona el emulador en el dropdown
2. Click en **Play** (Shift + F10)
3. Espera a que se instale

### 18.2 Que probar

| Funcion | Como probarla |
|---------|---------------|
| Crear nota | Click en FAB (+) |
| Editar nota | Click en una nota de la lista |
| Eliminar nota | Boton "Eliminar" en edicion |
| Recordatorio | Boton "Iniciar Recordatorio", espera 10 seg |
| Sensores | Boton "Probar Sensores", simula en el emulador |
| Google Maps | En edicion, escribe una ubicacion y toca "Mapa" |
| Google Calendar | En edicion, toca "Calendario" |

### 18.3 Debugging

1. Pon un breakpoint en `guardar()` de EditarNotaActivity
2. Ejecuta en modo debug (Shift + F9)
3. Crea una nota
4. Inspecciona las variables en el panel Debugger

### 18.4 Ver logs

Abre **Logcat** en la parte inferior. Filtra por tu paquete `com.misitioweb.miappnotas`.

---

## RESUMEN DE PATRONES Y CONCEPTOS

### Patrones de disenio

| Patron | Donde | Para que |
|--------|-------|----------|
| **Repository** | NotaRepositorio | Abstraer acceso a datos |
| **DAO** | NotaDao | Encapsular queries SQL |
| **Singleton** | NotaDatabase | Una sola instancia de BD |
| **Adapter** | NotaAdaptador | Conectar datos con RecyclerView |
| **ViewHolder** | NotaViewHolder | Reutilizar vistas en la lista |
| **Observer** | Flow/collectLatest | Reaccionar a cambios de datos |
| **Factory** | ViewModel.Factory (Compose) | Crear ViewModel con parametros |

### Keywords de Kotlin

| Concepto | Para que |
|----------|----------|
| `suspend` | Funcion que puede pausar sin bloquear el hilo |
| `@Volatile` | Variable visible por todos los hilos |
| `by lazy` | Inicializacion diferida |
| `Flow` | Stream de datos reactivo |
| `StateFlow` | Flow con valor actual |
| `lifecycleScope` | Corrutina ligada al ciclo de vida |
| `collectLatest` | Recibe el valor mas reciente de un Flow |

### Componentes de Android usados

| Componente | Clase | Para que |
|------------|-------|----------|
| Activity | MainActivity | Lista de notas |
| Activity | EditarNotaActivity | Crear/editar nota + integraciones |
| Activity | SensorActivity | Acelerometro |
| Activity | ContactosActivity | Leer contactos (ContentProvider) |
| Service | RecordatorioService | Notificacion en background |
| BroadcastReceiver | EventoReceiver | Boot completed, bateria baja |
| Fragment | NotaDetailFragment | UI reutilizable |
| ContentProvider | ContactsContract | Leer contactos del sistema |
| Intent | Varios | Navegacion, Maps, Calendar |
