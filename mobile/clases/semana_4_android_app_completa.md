# SEMANA 4: Mi Primera App de Notas

## Tutorial Paso a Paso - Aplicación Completa

Vas a crear una aplicación completa de notas. En esta clase vas a usar todo lo que aprendiste: Activities, Services, BroadcastReceivers, base de datos Room y sensores. Todo paso a paso, código listo para copiar y probar en el emulador.

---

## CONCEPTOS FUNDAMENTALES ANTES DE EMPEZAR

### ¿Qué es Gradle?

**Gradle** es el sistema de construcción (build) que usa Android Studio. 
- Compila tu código
- Descarga librerías
- Empaqueta la app
- Ejecuta tests

Piensa en Gradle como un "npm" o "maven".

### ¿Qué son los Plugins?

Un **plugin** es una extensión que agrega funcionalidades a Gradle. Son como "plugins de navegador" pero para construir apps.

| Plugin | Para qué sirve |
|--------|----------------|
| `com.android.application` | Compilar apps Android |
| `org.jetbrains.kotlin.android` | Soporte para Kotlin |
| `org.jetbrains.kotlin.plugin.compose` | Compilar UI con Compose (Kotlin 2.0+) |
| `com.google.devtools.ksp` | Generar código automáticamente (reemplaza kapt) |

### ¿Qué es KSP vs KAPT?

**KAPT** (Kotlin Annotation Processing Tool) y **KSP** (Kotlin Symbol Processing) son herramientas que generan código automáticamente durante la compilación.

```
Tu código → KAPT/KSP → Código generado → Compilación final
```

| Característica | KAPT | KSP |
|---------------|------|-----|
| Velocidad | Más lento | Más rápido |
| Compatibilidad | Todas las librerías | Librerías modernas |
| Estado | Mantenido | Recomendado |
| Ejemplo de uso | `kapt("androidx.room:room-compiler:2.6.1")` | `ksp("androidx.room:room-compiler:2.6.1")` |

** Recomendación: Usar KSP porque es más rápido y moderno. **

### ¿Qué es Room?

**Room** es la librería oficial de Android para bases de datos SQLite. Persiste tus datos en el dispositivo.

```
┌─────────────────────────────────────────────────────────────┐
│                      TU APP                                 │
│  ┌─────────────┐     ┌──────────────┐    ┌───────────────┐ │
│  │   UI        │────▶│  Repositorio │────▶│    Room       │ │
│  │  (Compose)  │     │              │     │  (SQLite)     │ │
│  └─────────────┘     └──────────────┘    └───────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

**¿Por qué Room?**
- **Persistencia**: Los datos sobreviven al cierre de la app
- **Fácil**: No escribes SQL, usas funciones Kotlin
- **Seguro**: Validación automática de consultas
- **Reactivo**: Con `Flow` puedes observar cambios en tiempo real

**Alternativas a Room:**

| Alternativa | Tipo | Cuándo usarla |
|-------------|------|---------------|
| **Room** | SQLite ORM | Cuando necesitas base de datos relacional |
| **DataStore** | Key-Value | Configuraciones simples |
| **Firebase Firestore** | Cloud | Cuando necesitas sincronización en la nube |
| **SharedPreferences** | Key-Value | Solo ajustes pequeños |
| **MongoDB Realm** | NoSQL | Cuando necesitas flexibilidad de esquema |

### Archivos de Configuración de Gradle

```
MiAppNotas/
├── build.gradle.kts           ← Configuración raíz (plugins globales)
├── settings.gradle.kts        ← Qué módulos existen, dónde buscar plugins
├── gradle.properties          ← Propiedades de Gradle
└── app/
    └── build.gradle.kts       ← Configuración del módulo app
```

#### 1. gradle/libs.versions.toml (Catálogo de Versiones)

Este archivo define **todas las versiones** de tus dependencias en un solo lugar:

```toml
[versions]
kotlin = "2.1.10"           # Versión de Kotlin
agp = "8.7.3"               # Android Gradle Plugin
room = "2.6.1"              # Room

[libraries]
androidx-core-ktx = { group = "androidx.core", name = "core-ktx", version.ref = "coreKtx" }

[plugins]
kotlin-android = { id = "org.jetbrains.kotlin.android", version.ref = "kotlin" }
```

**Beneficio**: Si cambias la versión en un solo lugar, se actualiza en todo el proyecto.

#### 2. build.gradle.kts (raíz)

Declara los plugins disponibles para **todos** los módulos:

```kotlin
plugins {
    alias(libs.plugins.android.application) apply false  // Solo declarar, no aplicar
    alias(libs.plugins.kotlin.android) apply false
    alias(libs.plugins.kotlin.compose) apply false
    alias(libs.plugins.kotlin.ksp) apply false
}
```

**Nota**: `apply false` significa "declarar pero no usar todavía". Se aplicarán en los módulos que los necesiten.

#### 3. settings.gradle.kts

Define:
- Qué módulos incluye el proyecto
- Dónde buscar plugins (repositorios)
- El nombre del proyecto

```kotlin
pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}

dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
    }
}

rootProject.name = "MiAppNotas"
include(":app")
```

#### 4. app/build.gradle.kts

Aplica los plugins y define las dependencias del módulo:

```kotlin
plugins {
    alias(libs.plugins.android.application)  // Aplica el plugin
    alias(libs.plugins.kotlin.android)
    alias(libs.plugins.kotlin.compose)
    alias(libs.plugins.kotlin.ksp)
}

dependencies {
    implementation(libs.androidx.core.ktx)
    ksp(libs.androidx.room.compiler)  // KSP para generar código Room
}
```

### ¿Qué es un Alias?

Un **alias** es un atajo definido en `libs.versions.toml` que evita repetir la versión:

```toml
# Sin alias (repetitivo)
implementation("org.jetbrains.kotlin:kotlin-android:2.1.10")

# Con alias (limpio)
alias(libs.plugins.kotlin.android)
```

---

## PARTE 1: Crear el Proyecto en Android Studio

### 1.1 Nuevo Proyecto

1. Abre Android Studio
2. Ve a **File → New → New Project**
3. Elige **Empty Activity**
4. Configura el proyecto:

```
Name:                MiAppNotas
Package name:        com.misitioweb.miappnotas
Language:           Kotlin  
Minimum SDK:         API 26 (Android 8.0)
Build Config:        Use Kotlin DSL (build.gradle.kts)
```

5. Click **Finish**
6. Espera a que sincronice Gradle

### 1.2 Agregar Dependencias y Plugins (CONFIGURACIÓN ACTUALIZADA)

> **IMPORTANTE**: Esta configuración usa **Kotlin 2.1.10** con **KSP** (no KAPT). El plugin `org.jetbrains.kotlin.plugin.compose` requiere Kotlin 2.0+.

#### A) Actualizar gradle/libs.versions.toml

Agrega las versiones de Room y KSP:

```toml
[versions]
agp = "8.7.3"
kotlin = "2.1.10"
room = "2.6.1"
ksp = "2.1.10-1.0.28"
# ... otras versiones

[libraries]
# ... otras librerías
androidx-room-runtime = { group = "androidx.room", name = "room-runtime", version.ref = "room" }
androidx-room-ktx = { group = "androidx.room", name = "room-ktx", version.ref = "room" }
androidx-room-compiler = { group = "androidx.room", name = "room-compiler", version.ref = "room" }

[plugins]
android-application = { id = "com.android.application", version.ref = "agp" }
kotlin-android = { id = "org.jetbrains.kotlin.android", version.ref = "kotlin" }
kotlin-compose = { id = "org.jetbrains.kotlin.plugin.compose", version.ref = "kotlin" }
kotlin-ksp = { id = "com.google.devtools.ksp", version.ref = "ksp" }
```

#### B) build.gradle.kts (raíz)

```kotlin
plugins {
    alias(libs.plugins.android.application) apply false
    alias(libs.plugins.kotlin.android) apply false
    alias(libs.plugins.kotlin.compose) apply false
    alias(libs.plugins.kotlin.ksp) apply false
}
```

#### C) app/build.gradle.kts

```kotlin
plugins {
    alias(libs.plugins.android.application)
    alias(libs.plugins.kotlin.android)
    alias(libs.plugins.kotlin.compose)
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
        compose = true
    }
}

dependencies {
    // Compose
    implementation(platform(libs.androidx.compose.bom))
    implementation(libs.androidx.compose.ui)
    implementation(libs.androidx.compose.material3)
    
    // Room con KSP (NO kapt)
    implementation(libs.androidx.room.runtime)
    implementation(libs.androidx.room.ktx)
    ksp(libs.androidx.room.compiler)
    
    // Material
    implementation("com.google.android.material:material:1.11.0")
}
```

Click **Sync Now**.

---

## PARTE 2: La Base de Datos (Room)

### 2.1 La Entidad Nota

Click derecho en la carpeta del paquete:

```
New → Kotlin Class → Class
```

Nombre: **Nota**

Contenido:

```kotlin
package com.misitioweb.miappnotas

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

### 2.2 El DAO

Click derecho:

```
New → Kotlin Class → Interface
```

Nombre: **NotaDao**

Contenido:

```kotlin
package com.misitioweb.miappnotas

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

### 2.3 La Base de Datos

Click derecho:

```
New → Kotlin Class → Class
```

Nombre: **NotaDatabase**

Contenido:

```kotlin
package com.misitioweb.miappnotas

import android.content.Context
import androidx.room.Database
import androidx.room.Room
import androidx.room.RoomDatabase

@Database(entities = [Nota::class], version = 1)
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

### 2.4 El Repositorio

Click derecho:

```
New → Kotlin Class → Class
```

Nombre: **NotaRepositorio**

Contenido:

```kotlin
package com.misitioweb.miappnotas

import kotlinx.coroutines.flow.Flow

class NotaRepositorio(private val notaDao: NotaDao) {
    
    val todasLasNotas: Flow<List<Nota>> = notaDao.obtenerTodas()
    
    suspend fun obtenerPorId(id: Long): Nota? = notaDao.obtenerPorId(id)
    
    suspend fun insertar(nota: Nota): Long = notaDao.insertar(nota)
    
    suspend fun actualizar(nota: Nota) = notaDao.actualizar(nota)
    
    suspend fun eliminar(nota: Nota) = notaDao.eliminar(nota)
}
```

---

## PARTE 3: La Application

### 3.1 MiApplicacion

Click derecho:

```
New → Kotlin Class → Class
```

Nombre: **MiApplicacion**

Contenido:

```kotlin
package com.misitioweb.miappnotas

import android.app.Application

class MiApplicacion : Application() {
    
    val database by lazy { NotaDatabase.obtener(this) }
    val repositorio by lazy { NotaRepositorio(database.notaDao()) }
}
```

### 3.2 Actualizar AndroidManifest.xml

Abre AndroidManifest.xml y cambia la etiqueta application:

```xml
<application
    android:name=".MiApplicacion"
    android:allowBackup="true"
    android:icon="@mipmap/ic_launcher"
    android:label="@string/app_name"
    android:roundIcon="@mipmap/ic_launcher_round"
    android:supportsRtl="true"
    android:theme="@style/Theme.MiAppNotas">
    
    <activity
        android:name=".MainActivity"
        android:exported="true">
        <intent-filter>
            <action android:name="android.intent.action.MAIN" />
            <category android:name="android.intent.category.LAUNCHER" />
        </intent-filter>
    </activity>
    
</application>
```

---

## PARTE 4: MainActivity - Lista de Notas

### 4.1 El Layout

Abre activity_main.xml y reemplaza todo:

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

    <com.google.android.material.floatingactionbutton.FloatingActionButton
        android:id="@+id/fabAgregar"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_gravity="bottom|end"
        android:layout_margin="16dp"
        android:src="@android:drawable/ic_input_add" />

</LinearLayout>
```

### 4.2 Diseño de Cada Nota

Click derecho en res/layout:

```
New → Layout Resource File
```

Nombre: **item_nota**

Contenido:

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
            android:text="Título"
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

### 4.3 El Adaptador

Click derecho:

```
New → Kotlin Class → Class
```

Nombre: **NotaAdaptador**

Contenido:

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

### 4.4 MainActivity

Abre MainActivity.kt y reemplaza todo:

```kotlin
package com.misitioweb.miappnotas

import android.content.Intent
import android.os.Bundle
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
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)
        
        val app = application as MiApplicacion
        repositorio = app.repositorio
        
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
        binding.fabAgregar.setOnClickListener {
            startActivity(Intent(this, EditarNotaActivity::class.java))
        }
        
        binding.btnSensor.setOnClickListener {
            startActivity(Intent(this, SensorActivity::class.java))
        }
        
        binding.btnRecordar.setOnClickListener {
            startService(Intent(this, RecordatorioService::class.java))
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

---

## PARTE 5: Editar Nota Activity

### 5.1 Crear la Activity

Click derecho en el paquete:

```
New → Activity → Empty Activity
```

Nombre: **EditarNotaActivity**

Click Finish.

### 5.2 El Layout

Abre activity_editar_nota.xml y reemplaza:

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
        android:hint="Título"
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

### 5.3 El Código

Abre EditarNotaActivity.kt:

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
        
        val app = application as MiApplicacion
        repositorio = app.repositorio
        
        notaId = intent.getLongExtra("nota_id", 0)
        
        setupBotones()
        
        if (notaId > 0) {
            cargarNota()
        }
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
                binding.btnEliminar.visibility = View.VISIBLE
            }
        }
    }
    
    private fun guardar() {
        val titulo = binding.etTitulo.text.toString().trim()
        val contenido = binding.etContenido.text.toString().trim()
        
        if (titulo.isEmpty()) {
            binding.etTitulo.error = "El título es obligatorio"
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
            } else {
                repositorio.insertar(nota)
            }
            
            Toast.makeText(this@EditarNotaActivity, "Guardado", Toast.LENGTH_SHORT).show()
            finish()
        }
    }
    
    private fun eliminar() {
        lifecycleScope.launch {
            val nota = repositorio.obtenerPorId(notaId)
            if (nota != null) {
                repositorio.eliminar(nota)
                Toast.makeText(this@EditarNotaActivity, "Eliminado", Toast.LENGTH_SHORT).show()
                finish()
            }
        }
    }
}
```

### 5.4 Declarar en el Manifest

En AndroidManifest.xml, dentro de application:

```xml
<activity
    android:name=".EditarNotaActivity"
    android:exported="false" />
```

---

## PARTE 6: Service - Recordatorio

### 6.1 Crear el Service

Click derecho:

```
New → Service → Service
```

Nombre: **RecordatorioService**

Contenido:

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
-corriendo = false
        hilo?.interrupt()
    }
    
    private fun crearCanal() {
        val canal = NotificationChannel(CANAL_ID, "Recordatorio", NotificationManager.IMPORTANCE_DEFAULT)
        canal.description = "Recordatorio de notas"
        getSystemService(NotificationManager::class.java).createNotificationChannel(canal)
    }
    
    private fun mostrarNotificacion() {
        val intent = Intent(this, MainActivity::class.java)
        val pendingIntent = PendingIntent.getActivity(this, 0, intent, PendingIntent.FLAG_IMMUTABLE)
        
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

### 6.2 Declarar

En AndroidManifest.xml:

```xml
<service
    android:name=".RecordatorioService"
    android:enabled="true"
    android:exported="false" />
```

---

## PARTE 7: BroadcastReceiver

### 7.1 Crear el Receiver

Click derecho:

```
New → Other → Broadcast Receiver
```

Nombre: **EventoReceiver**

Contenido:

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
                Toast.makeText(context, "App lista", Toast.LENGTH_SHORT).show()
            }
            Intent.ACTION_BATTERY_LOW -> {
                Toast.makeText(context, "Batería baja", Toast.LENGTH_LONG).show()
            }
        }
    }
}
```

### 7.2 Declarar

En AndroidManifest.xml:

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

---

## PARTE 8: Sensores

### 8.1 Crear Activity

Click derecho:

```
New → Activity → Empty Activity
```

Nombre: **SensorActivity**

### 8.2 Layout

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

### 8.3 Código

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
        acelerometro?.let { sm.registerListener(this, it, SensorManager.SENSOR_DELAY_NORMAL) }
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

### 8.4 Declarar

En AndroidManifest.xml:

```xml
<activity
    android:name=".SensorActivity"
    android:exported="false" />
```

---

## PARTE 9: Ejecutar en el Emulador

### 9.1 Ejecutar

1. Selecciona el emulador en la barra superior
2. Presiona Shift + F10 o el botón Play verde
3. Espera a que se instale

### 9.2 Qué Probar

- Crear nota: Click en el botón (+) de abajo
- Editar nota: Click en una nota de la lista
- Eliminar: En edición, click en Eliminar
- Recordatorio: Click en "Iniciar Recordatorio", espera 10 segundos
- Sensores: Click en "Probar Sensores", mueves el emulador

### 9.3 Ver Logs

Abre la pestaña Logcat en Android Studio para ver los mensajes del sistema.

---

## Estructura Final

```
MiAppNotas/
├── app/src/main/
│   ├── java/com/misitioweb/miappnotas/
│   │   ├── Nota.kt
│   │   ├── NotaDao.kt
│   │   ├── NotaDatabase.kt
│   │   ├── NotaRepositorio.kt
│   │   ├── NotaAdaptador.kt
│   │   ├── MiApplicacion.kt
│   │   ├── MainActivity.kt
│   │   ├── EditarNotaActivity.kt
│   │   ├── SensorActivity.kt
│   │   ├── RecordatorioService.kt
│   │   └── EventoReceiver.kt
│   ├── res/layout/
│   │   ├── activity_main.xml
│   │   ├── activity_editar_nota.xml
│   │   ├── activity_sensor.xml
│   │   └── item_nota.xml
│   └── AndroidManifest.xml
```

---

## Resumen

### Componentes Usados

| Tipo | Nombre | Para qué |
|------|--------|----------|
| Activity | MainActivity | Lista de notas |
| Activity | EditarNotaActivity | Crear/editar nota |
| Activity | SensorActivity | Probar acelerómetro |
| Service | RecordatorioService | Notificación en segundo plano |
| BroadcastReceiver | EventoReceiver | Escuchar eventos del sistema |
| Room | Nota, NotaDao, NotaDatabase | Base de datos |
| Adaptador | NotaAdaptador | Lista visual |
| Application | MiApplicacion | Instancia global |

### Funciona en el Emulador

| Función | Funciona? |
|---------|------------|
| Crear/editar notas | ✅ |
| Base de datos | ✅ |
| Lista RecyclerView | ✅ |
| Service | ✅ |
| Notificación | ✅ |
| Sensores | ⚠️ |
| Eventos | ✅ |