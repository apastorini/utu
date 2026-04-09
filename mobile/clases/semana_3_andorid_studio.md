# SETUP ANDROID STUDIO

## PARTE 1: INSTALACIÓN

### 1.1 Descarga

Abre tu navegador y ve a:

```
https://developer.android.com/studio
```

Click en el botón grande que dice "Download Android Studio". Acepta los términos si te los pide. El archivo pesa alrededor de 1GB, así que tarda dependiendo de tu conexión.

### 1.2 Instalación en Windows

Busca el archivo descargado (normalmente en Descargas) y haz doble click.

```
android-studio-2024.x.x.x.exe
```

1. Pantalla de bienvenida: Click "Next"
2. Elige dónde instalar: Por defecto está bien, pero si tienes SSD ponlo ahí. Click "Next"
3. Configuración de componentes:
   - ☑ Android Studio
   - ☑ Android Virtual Device (esto es el simulador, importante)
   - ☑ Android SDK
   - ☑ Android SDK Platform-tools
4. Click "Install"
5. Espera a que termine. Puede tardar 10-20 minutos.
6. Click "Finish"

### 1.3 Primera Configuración

Al abrir Android Studio por primera vez aparece un asistente:

1. **Import Settings**: Elige "Do not import settings" (es tu primera instalación)
2. **Setup Wizard**: Elige "Standard" (configuración recomendada)
3. **Theme**: Elige el que prefieras, claro u oscuro
4. **SDK Components**: Descargará lo necesario. Acepta la licencia y espera.
5. **Download Components**: Esperar a que termine de bajar todo.
6. **Setup Complete**: Click "Finish"

Si ves la pantalla principal de Android Studio, la instalación fue bien.

### 1.4 Instalación en Mac

1. Abre el archivo DMG descargado
2. Arrastra "Android Studio" a la carpeta Aplicaciones
3. Ábrelo desde Aplicaciones
4. Sigue los mismos pasos del asistente que en Windows

### 1.5 Verificar Instalación

Ve a:

```
Tools → SDK Manager
```

En la pestaña "SDK Platforms" deberías ver algo como:

```
☑ Android 14 (API 34)
☑ Android 13 (API 33)
☐ Android 12 (API 31)
```

Si no hay nada marcado, marca Android 14 y click "Apply".

---

## PARTE 2: CREAR EL PROYECTO

### 2.1 Nuevo Proyecto

Desde Android Studio:

```
File → New → New Project
```

Aparece una ventana con plantillas. Elige **"Empty Activity"** (la primera opción). Es la más limpia para aprender.

Click en "Next".

### 2.2 Configurar el Proyecto

Rellena así:

```
Name:                MiPrimeraApp
Package name:        com.misitioweb.miprimeraapp
Save location:       (déjalo por defecto)
Language:            Kotlin
Minimum SDK:         API 26 (Android 8.0)
Build configuration:  Kotlin DSL
```

**Explicación rápida de cada campo:**

- **Name**: El nombre que ve el usuario en el celular
- **Package name**: Identificador único de tu app. Sigue el formato "com.tudominio.nombreapp". No puede haber dos apps con el mismo package name en Google Play.
- **Language**: Kotlin es el lenguaje oficial actual de Android
- **Minimum SDK**: La versión mínima de Android que soportará tu app. API 26 cubre más del 90% de dispositivos.

Click "Finish".

### 2.3 Esperar la Sincronización

En la esquina inferior derecha aparece una barra de progreso que dice "Gradle Sync". Gradle es el sistema que compila tu proyecto. No toques nada hasta que termine.

Esto puede tardar entre 2 y 10 minutos la primera vez. Si marca error, normalmente es por falta de conexión o porque algo se descargó mal. En ese caso, ve a:

```
File → Invalidate Caches → Invalidate and Restart
```

---

## PARTE 3: CONOCER EL PROYECTO

### 3.1 Ver la Estructura

En el panel izquierdo (Project), cambia la vista:

```
Project: (dropdown) → Project Files
```

Ahora ves la estructura real de carpetas.

```
MiPrimeraApp/
├── app/                          ← Tu aplicación
│   ├── src/
│   │   ├── main/                 ← Código principal
│   │   │   ├── java/             ← Código Kotlin
│   │   │   │   └── com/misitioweb/miprimeraapp/
│   │   │   │       └── MainActivity.kt
│   │   │   ├── res/              ← Recursos (layouts, imágenes, textos)
│   │   │   │   ├── layout/
│   │   │   │   │   └── activity_main.xml
│   │   │   │   ├── values/
│   │   │   │   │   └── strings.xml
│   │   │   │   └── drawable/
│   │   │   └── AndroidManifest.xml
│   │   └── build.gradle.kts      ← Configuración de compilación
│   └── build.gradle.kts
├── build.gradle.kts              ← Configuración global
├── settings.gradle.kts
└── gradle/
```

### 3.2 Los Archivos Importantes

**MainActivity.kt** - Es el código de tu pantalla principal:

```kotlin
package com.misitioweb.miprimeraapp

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
    }
}
```

**activity_main.xml** - Es el diseño visual de tu pantalla:

```xml
<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout 
    xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:layout_width="match_parent"
    android:layout_height="match_parent">

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Hello World!"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

</androidx.constraintlayout.widget.ConstraintLayout>
```

**AndroidManifest.xml** - Declara qué tiene tu app:

```xml
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.MiPrimeraApp">
        
        <activity
            android:name=".MainActivity"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
        
    </application>

</manifest>
```

---

## PARTE 4: Repaso CICLO DE VIDA

### 4.1 Qué es el Ciclo de Vida

Cuando abres una app, el sistema operativo la va guiando por diferentes estados. Cada estado tiene métodos que tú puedes sobrescribir para ejecutar código en el momento justo.

Imagina que abres WhatsApp, oprimes el botón de Home (vas a otra app), y vuelves a WhatsApp. ¿Qué pasó internamente?

```
Tocas WhatsApp       → La app se "crea"
WhatsApp aparece      → La app se "inicia" y "resume"
Vas a otra app        → La app se "pausa" y se "detiene"
Vuelves a WhatsApp    → La app se "reinicia"
Cierras WhatsApp      → La app se "destruye"
```

### 4.2 Los Estados y Métodos

| Estado | Método que se llama | Qué pasa |
|--------|-------------------|---------|
| Creación | `onCreate()` | La pantalla se crea por primera vez. Solo ocurre una vez. |
| Visible | `onStart()` | La pantalla empieza a ser visible |
| Activa | `onResume()` | La pantalla está lista para que el usuario interactúe |
| Pierde foco | `onPause()` | Algo overlaid la pantalla (llamada, notificación) |
| Invisible | `onStop()` | La pantalla ya no se ve |
| Reinicia | `onRestart()` | Vuelve a ser visible después de estar oculta |
| Destruida | `onDestroy()` | La pantalla se cierra definitivamente |

### 4.3 El Flujo Real

```
onCreate()
    │
    ▼
onStart()
    │
    ▼
onResume()
    │
    ├──→ (usuario interactúa)
    │
    ├──→ onPause() ─→ onStop()
    │                      │
    │                      ├──→ onRestart()
    │                      │         │
    │                      │    onStart()
    │                      │         │
    │                      └──→ onDestroy()
    │
onPause() ← cuando otra app aparece
onStop()
```

### 4.4 Código Completo con el Ciclo de Vida

Abre `MainActivity.kt` y reemplaza todo el contenido con esto:

```kotlin
package com.misitioweb.miprimeraapp

import android.os.Bundle
import android.util.Log
import androidx.appcompat.app.AppCompatActivity

class MainActivity : AppCompatActivity() {

    // Tag para identificar tus logs en Logcat
    private val TAG = "MainActivity"

    // Se llama UNA SOLA VEZ cuando se crea la Activity
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        
        Log.d(TAG, ">>> onCreate: La activity se creó")
    }

    // Se llama cuando la activity se vuelve visible
    override fun onStart() {
        super.onStart()
        Log.d(TAG, ">>> onStart: La activity es visible")
    }

    // Se llama cuando la activity está en primer plano y lista para interactuar
    override fun onResume() {
        super.onResume()
        Log.d(TAG, ">>> onResume: La activity está activa")
    }

    // Se llama cuando la activity pierde el foco (aparece otra cosa encima)
    override fun onPause() {
        super.onPause()
        Log.d(TAG, ">>> onPause: La activity perdió el foco")
    }

    // Se llama cuando la activity deja de estar visible
    override fun onStop() {
        super.onStop()
        Log.d(TAG, ">>> onStop: La activity no es visible")
    }

    // Se llama solo si la activity se va a destruir y volver a crear
    override fun onRestart() {
        super.onRestart()
        Log.d(TAG, ">>> onRestart: La activity va a reiniciarse")
    }

    // Se llama cuando la activity se destruye
    override fun onDestroy() {
        super.onDestroy()
        Log.d(TAG, ">>> onDestroy: La activity se destruyó")
    }
}
```

### 4.5 Ver los Logs

1. En Android Studio, abajo, haz click en la pestaña **"Logcat"**
2. En el buscador escribe: `MainActivity`
3. Ejecuta la app (Shift + F10)
4. Verás los mensajes apareciendo en orden

---

## PARTE 5: CREAR MÁS ACTIVITIES

### 5.1 Para qué sirven varias Activities

Una app tiene varias pantallas. WhatsApp tiene pantalla de chats, pantalla de chat individual, pantalla de configuración. Cada una es una Activity diferente.

### 5.2 Crear una Segunda Activity

1. En el panel izquierdo, ve a:
   ```
   app → src → main → java → com.misitioweb.miprimeraapp
   ```
2. Click derecho en esa carpeta:
   ```
   New → Activity → Empty Activity
   ```
3. Configura:
   ```
   Activity Name:    SegundaActivity
   Layout Name:      activity_segunda
   ```
4. Click "Finish"

Se crearon dos archivos nuevos:
- `SegundaActivity.kt` en la carpeta java
- `activity_segunda.xml` en `res/layout`

### 5.3 Diseñar la Segunda Pantalla

Abre `activity_segunda.xml` y reemplaza con:

```xml
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout
    xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:gravity="center"
    android:padding="24dp"
    android:background="#F5F5F5">

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Esta es la Segunda Pantalla"
        android:textSize="22sp"
        android:textStyle="bold"
        android:textColor="#333333" />

    <Button
        android:id="@+id/btnVolver"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Volver"
        android:layout_marginTop="24dp" />

</LinearLayout>
```

### 5.4 Programar la Segunda Activity

Abre `SegundaActivity.kt`:

```kotlin
package com.misitioweb.miprimeraapp

import android.os.Bundle
import android.util.Log
import androidx.appcompat.app.AppCompatActivity

class SegundaActivity : AppCompatActivity() {

    private val TAG = "SegundaActivity"

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_segunda)
        
        Log.d(TAG, ">>> onCreate: SegundaActivity creada")
    }

    override fun onStart() {
        super.onStart()
        Log.d(TAG, ">>> onStart")
    }

    override fun onResume() {
        super.onResume()
        Log.d(TAG, ">>> onResume")
    }

    override fun onPause() {
        super.onPause()
        Log.d(TAG, ">>> onPause")
    }

    override fun onStop() {
        super.onStop()
        Log.d(TAG, ">>> onStop")
    }

    override fun onDestroy() {
        super.onDestroy()
        Log.d(TAG, ">>> onDestroy")
    }
}
```

### 5.5 Declarar en el Manifest

Abre `AndroidManifest.xml`. Toda Activity debe estar declarada:

```xml
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.MiPrimeraApp">
        
        <!-- Primera Activity (LAUNCHER) -->
        <activity
            android:name=".MainActivity"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
        
        <!-- Segunda Activity -->
        <activity
            android:name=".SegundaActivity"
            android:exported="false" />
        
    </application>

</manifest>
```

### 5.6 Navegar de una Activity a Otra

Regresa a `MainActivity.kt` y actualiza el código:

```kotlin
package com.misitioweb.miprimeraapp

import android.content.Intent
import android.os.Bundle
import android.util.Log
import android.widget.Button
import androidx.appcompat.app.AppCompatActivity

class MainActivity : AppCompatActivity() {

    private val TAG = "MainActivity"

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        
        Log.d(TAG, ">>> onCreate")
        
        // Encontrar el botón por su ID
        val btnIrASegunda = findViewById<Button>(R.id.btnIrASegunda)
        
        // Configurar el click
        btnIrASegunda.setOnClickListener {
            // Crear el intent para ir a la segunda activity
            val intent = Intent(this, SegundaActivity::class.java)
            
            // También puedes enviar datos
            intent.putExtra("nombre_usuario", "Juan")
            intent.putExtra("edad_usuario", 28)
            
            // Iniciar la activity
            startActivity(intent)
        }
    }

    override fun onStart() {
        super.onStart()
        Log.d(TAG, ">>> onStart")
    }

    override fun onResume() {
        super.onResume()
        Log.d(TAG, ">>> onResume")
    }

    override fun onPause() {
        super.onPause()
        Log.d(TAG, ">>> onPause")
    }

    override fun onStop() {
        super.onStop()
        Log.d(TAG, ">>> onStop")
    }

    override fun onDestroy() {
        super.onDestroy()
        Log.d(TAG, ">>> onDestroy")
    }
}
```

### 5.7 Actualizar el Layout de MainActivity

Abre `activity_main.xml`:

```xml
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout
    xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:gravity="center"
    android:padding="24dp">

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Pantalla Principal"
        android:textSize="28sp"
        android:textStyle="bold"
        android:textColor="#2196F3" />

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Presiona el botón para ir a la segunda pantalla"
        android:textSize="16sp"
        android:layout_marginTop="16dp"
        android:layout_marginBottom="32dp" />

    <Button
        android:id="@+id/btnIrASegunda"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Ir a Segunda Pantalla" />

</LinearLayout>
```

### 5.8 Recibir Datos en la Segunda Activity

Abre `SegundaActivity.kt` y recibe los datos:

```kotlin
package com.misitioweb.miprimeraapp

import android.os.Bundle
import android.util.Log
import android.widget.Button
import androidx.appcompat.app.AppCompatActivity

class SegundaActivity : AppCompatActivity() {

    private val TAG = "SegundaActivity"

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_segunda)
        
        Log.d(TAG, ">>> onCreate")
        
        // Recibir datos
        val nombre = intent.getStringExtra("nombre_usuario")
        val edad = intent.getIntExtra("edad_usuario", 0)
        
        Log.d(TAG, "Datos recibidos: nombre=$nombre, edad=$edad")
        
        // Botón para volver
        val btnVolver = findViewById<Button>(R.id.btnVolver)
        btnVolver.setOnClickListener {
            finish() // Cierra esta activity y vuelve a la anterior
        }
    }

    override fun onStart() {
        super.onStart()
        Log.d(TAG, ">>> onStart")
    }

    override fun onResume() {
        super.onResume()
        Log.d(TAG, ">>> onResume")
    }

    override fun onPause() {
        super.onPause()
        Log.d(TAG, ">>> onPause")
    }

    override fun onStop() {
        super.onStop()
        Log.d(TAG, ">>> onStop")
    }

    override fun onDestroy() {
        super.onDestroy()
        Log.d(TAG, ">>> onDestroy")
    }
}
```

---

## PARTE 6: CREAR UN FRAGMENT

### 6.1 Qué es un Fragment

Un Fragment es como un "pedazo de Activity". Te permite tener varias secciones dentro de una misma pantalla. Es útil para apps que funcionan tanto en celulares como en tablets, o cuando quieres tener navegación dentro de una misma Activity.

### 6.2 Crear un Fragment

1. Click derecho en la carpeta del paquete:
   ```
   New → Fragment → Empty Fragment
   ```
2. Configure:
   ```
   Fragment Name:    MiFragment
   Layout Name:      fragment_mi
   ☑ Include fragment factory methods
   ☑ Include interface callbacks
   ```
3. Click "Finish"

### 6.3 El Código del Fragment

Abre `MiFragment.kt`:

```kotlin
package com.misitioweb.miprimeraapp

import android.os.Bundle
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.fragment.app.Fragment

class MiFragment : Fragment() {

    private val TAG = "MiFragment"

    // Se llama para crear la vista del fragment
    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        Log.d(TAG, ">>> onCreateView")
        return inflater.inflate(R.layout.fragment_mi, container, false)
    }

    // Se llama después de que la vista fue creada
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        Log.d(TAG, ">>> onViewCreated")
        
        // Encontrar elementos de la vista
        val tvSaludo = view.findViewById<TextView>(R.id.tvSaludo)
        tvSaludo.text = "Hola desde el Fragment"
    }

    override fun onStart() {
        super.onStart()
        Log.d(TAG, ">>> onStart")
    }

    override fun onResume() {
        super.onResume()
        Log.d(TAG, ">>> onResume")
    }

    override fun onPause() {
        super.onPause()
        Log.d(TAG, ">>> onPause")
    }

    override fun onStop() {
        super.onStop()
        Log.d(TAG, ">>> onStop")
    }

    override fun onDestroyView() {
        super.onDestroyView()
        Log.d(TAG, ">>> onDestroyView")
    }
}
```

### 6.4 El Layout del Fragment

Abre `fragment_mi.xml`:

```xml
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout
    xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:orientation="vertical"
    android:padding="16dp"
    android:background="#E3F2FD">

    <TextView
        android:id="@+id/tvSaludo"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Fragment aquí"
        android:textSize="18sp"
        android:textColor="#1565C0" />

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Este es un fragment dentro de la activity"
        android:textSize="14sp"
        android:layout_marginTop="8dp" />

</LinearLayout>
```

### 6.5 Usar el Fragment en una Activity

Crea una Activity que contenga el Fragment. Primero crea una Activity llamada `ActivityConFragment`:

```
New → Activity → Empty Activity → ActivityConFragment
```

Abre `activity_con_fragment.xml`:

```xml
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout
    xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:padding="16dp">

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Activity con Fragment"
        android:textSize="24sp"
        android:textStyle="bold"
        android:layout_marginBottom="16dp" />

    <!-- Aquí se cargará el fragment dinámicamente -->
    <FrameLayout
        android:id="@+id/contenedorFragment"
        android:layout_width="match_parent"
        android:layout_height="200dp"
        android:background="#EEEEEE" />

</LinearLayout>
```

Abre `ActivityConFragment.kt`:

```kotlin
package com.misitioweb.miprimeraapp

import android.os.Bundle
import android.util.Log
import androidx.appcompat.app.AppCompatActivity
import androidx.fragment.app.commit
import com.misitioweb.miprimeraapp.databinding.ActivityConFragmentBinding

class ActivityConFragment : AppCompatActivity() {

    private val TAG = "ActivityConFragment"
    private lateinit var binding: ActivityConFragmentBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityConFragmentBinding.inflate(layoutInflater)
        setContentView(binding.root)
        
        Log.d(TAG, ">>> onCreate")
        
        // Solo agregar el fragment si es la primera vez
        if (savedInstanceState == null) {
            supportFragmentManager.commit {
                replace(R.id.contenedorFragment, MiFragment())
            }
        }
    }

    override fun onStart() {
        super.onStart()
        Log.d(TAG, ">>> onStart")
    }

    override fun onResume() {
        super.onResume()
        Log.d(TAG, ">>> onResume")
    }

    override fun onPause() {
        super.onPause()
        Log.d(TAG, ">>> onPause")
    }

    override fun onStop() {
        super.onStop()
        Log.d(TAG, ">>> onStop")
    }

    override fun onDestroy() {
        super.onDestroy()
        Log.d(TAG, ">>> onDestroy")
    }
}
```

No olvides declararlo en el Manifest.

---

## PARTE 7: CREAR UN SERVICE

### 7.1 Qué es un Service

Un Service es un componente que corre en segundo plano, sin interfaz visual. Sirve para tareas que necesitan seguir ejecutándose aunque el usuario no esté mirando la app. Por ejemplo: reproducir música, descargar archivos, sincronizar datos.

### 7.2 Crear el Service

```
New → Service → Service
```

Configure:
```
Service Name:    MiServicio
☐ IntentService (para tareas asíncronas)
```

### 7.3 El Código del Service

Abre `MiServicio.kt`:

```kotlin
package com.misitioweb.miprimeraapp

import android.app.Service
import android.content.Intent
import android.os.IBinder
import android.util.Log

class MiServicio : Service() {

    private val TAG = "MiServicio"
    private var hiloTrabajo: Thread? = null
    private var estaCorriendo = false

    // Se llama cuando el service se crea
    override fun onCreate() {
        super.onCreate()
        Log.d(TAG, ">>> onCreate: Service creado")
    }

    // Se llama cada vez que se inicia el service
    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        Log.d(TAG, ">>> onStartCommand: startId=$startId")
        
        estaCorriendo = true
        
        // Crear un hilo para el trabajo en segundo plano
        hiloTrabajo = Thread {
            var contador = 0
            while (estaCorriendo && contador < 20) {
                try {
                    Log.d(TAG, "Servicio ejecutándose... contador=$contador")
                    Thread.sleep(1000)
                    contador++
                } catch (e: InterruptedException) {
                    Log.e(TAG, "Error en el hilo: ${e.message}")
                    Thread.currentThread().interrupt()
                }
            }
            Log.d(TAG, "Trabajo del servicio terminado")
            
            // Detener el servicio manualmente
            stopSelf()
        }
        hiloTrabajo?.start()
        
        // START_STICKY: si el sistema mata el service, lo recrea
        return START_STICKY
    }

    // Se llama cuando se hace bind al service (para comunicación)
    override fun onBind(intent: Intent?): IBinder? {
        Log.d(TAG, ">>> onBind")
        return null
    }

    // Se llama cuando el último cliente se desvincula
    override fun onUnbind(intent: Intent?): Boolean {
        Log.d(TAG, ">>> onUnbind")
        return super.onUnbind(intent)
    }

    // Se llama cuando el service se destruye
    override fun onDestroy() {
        super.onDestroy()
        estaCorriendo = false
        hiloTrabajo?.interrupt()
        Log.d(TAG, ">>> onDestroy: Service destruido")
    }
}
```

### 7.4 Declarar el Service en el Manifest

```xml
<manifest ...>

    <application
        ...>
        
        <activity android:name=".MainActivity" ... />
        <activity android:name=".SegundaActivity" ... />
        <activity android:name=".ActivityConFragment" ... />
        
        <!-- Declarar el Service -->
        <service
            android:name=".MiServicio"
            android:enabled="true"
            android:exported="false" />
        
    </application>

</manifest>
```

### 7.5 Iniciar el Service desde una Activity

Crea una Activity nueva llamada `ActivityServiceTest`.

```xml
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout
    xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:gravity="center"
    android:padding="24dp">

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Prueba de Service"
        android:textSize="24sp"
        android:textStyle="bold"
        android:layout_marginBottom="32dp" />

    <Button
        android:id="@+id/btnIniciarServicio"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Iniciar Servicio"
        android:layout_marginBottom="16dp" />

    <Button
        android:id="@+id/btnDetenerServicio"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Detener Servicio" />

</LinearLayout>
```

```kotlin
package com.misitioweb.miprimeraapp

import android.content.Intent
import android.os.Bundle
import android.util.Log
import android.widget.Button
import androidx.appcompat.app.AppCompatActivity
import com.misitioweb.miprimeraapp.databinding.ActivityServiceTestBinding

class ActivityServiceTest : AppCompatActivity() {

    private val TAG = "ServiceTest"
    private lateinit var binding: ActivityServiceTestBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityServiceTestBinding.inflate(layoutInflater)
        setContentView(binding.root)
        
        Log.d(TAG, ">>> onCreate")
        
        binding.btnIniciarServicio.setOnClickListener {
            Log.d(TAG, "Iniciando servicio...")
            val intent = Intent(this, MiServicio::class.java)
            startService(intent)
        }
        
        binding.btnDetenerServicio.setOnClickListener {
            Log.d(TAG, "Deteniendo servicio...")
            val intent = Intent(this, MiServicio::class.java)
            stopService(intent)
        }
    }

    override fun onStart() {
        super.onStart()
        Log.d(TAG, ">>> onStart")
    }

    override fun onResume() {
        super.onResume()
        Log.d(TAG, ">>> onResume")
    }

    override fun onPause() {
        super.onPause()
        Log.d(TAG, ">>> onPause")
    }

    override fun onStop() {
        super.onStop()
        Log.d(TAG, ">>> onStop")
    }

    override fun onDestroy() {
        super.onDestroy()
        Log.d(TAG, ">>> onDestroy")
    }
}
```

---

## PARTE 8: CREAR UN BROADCAST RECEIVER

### 8.1 Qué es un Broadcast Receiver

Es un componente que escucha eventos del sistema o de otras apps. Por ejemplo: cuando el celular se enciende, cuando llega un SMS, cuando cambia la conexión a internet.

### 8.2 Crear el Broadcast Receiver

```
New → Other → Broadcast Receiver
```

Configure:
```
Name:            MiReceiver
☐ Exported       (si otras apps deben poder enviarte eventos)
☐ Enabled
```

### 8.3 El Código del Receiver

Abre `MiReceiver.kt`:

```kotlin
package com.misitioweb.miprimeraapp

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.util.Log

class MiReceiver : BroadcastReceiver() {

    private val TAG = "MiReceiver"

    override fun onReceive(context: Context?, intent: Intent?) {
        Log.d(TAG, ">>> onReceive: Evento recibido")
        Log.d(TAG, "Action: ${intent?.action}")
        Log.d(TAG, "Data: ${intent?.data}")
        
        // Verificar qué acción llegó
        when (intent?.action) {
            Intent.ACTION_BOOT_COMPLETED -> {
                Log.d(TAG, "El celular acabou de iniciar!")
            }
            "com.misitioweb.EVENTO_PERSONAL" -> {
                val mensaje = intent.getStringExtra("mensaje")
                Log.d(TAG, "Mensaje personal: $mensaje")
            }
        }
    }
}
```

### 8.4 Declarar en el Manifest

```xml
<manifest ...>

    <application ...>
        
        ...
        
        <!-- Declarar el Receiver -->
        <receiver
            android:name=".MiReceiver"
            android:enabled="true"
            android:exported="false">
            
            <intent-filter>
                <!-- Escuchar cuando el celular inicia -->
                <action android:name="android.intent.action.BOOT_COMPLETED" />
                
                <!-- Escuchar eventos personalizados -->
                <action android:name="com.misitioweb.EVENTO_PERSONAL" />
            </intent-filter>
            
        </receiver>
        
    </application>

</manifest>
```

### 8.5 Enviar un Broadcast desde una Activity

```kotlin
// En cualquier Activity
val intent = Intent("com.misitioweb.EVENTO_PERSONAL")
intent.putExtra("mensaje", "Hola desde la Activity!")
sendBroadcast(intent)
```

---

## PARTE 9: EL EMULADOR (AVD)

### 9.1 Qué es un AVD

AVD significa Android Virtual Device. Es basically un celular virtual que corre en tu computadora. Te permite probar apps sin necesidad de un celular real.

### 9.2 Crear un Emulador

1. Ve a:
   ```
   Tools → Device Manager
   ```
2. Click en el botón **"Create Device"**
3. Selecciona un dispositivo. Elige **"Pixel 7"** o **"Pixel 6"** (son los más estándar). Click "Next".
4. Selecciona la imagen del sistema. Busca **"API 34"** con ABI **x86_64**. Si no está descargada, dale click al botón de descarga (la flecha hacia abajo) y espera.
5. Click "Next"
6. Configura el nombre si quieres. Leave the rest por defecto.
7. Click "Finish"

La descarga puede tardar 10-20 minutos y ocupa aproximadamente 3GB.

### 9.3 Ejecutar la App en el Emulador

1. En la barra superior de Android Studio, verás un dropdown que dice algo como "app". Ahí mismo selecciona el emulador que creaste.
2. Presiona el botón verde de **Play** (▶️) o Shift + F10.
3. Esperar. La primera vez que arrancas el emulador tarda entre 3 y 10 minutos.
4. Cuando esté corriendo, verás el emulador con la app instalada.

### 9.4 Controles del Emulador

```
En el emulador:
├── Botón Home (casa)          → Va a la pantalla principal
├── Botón Back (flecha)        → Retrocede
├── Botón Recientes (cuadrado) → Muestra apps abiertas
├── Botón Power                → Bloquear/pantalla apagada
└── Rotar                      → Cambiar orientación
```

### 9.5 Si el Emulador es Lento

Si el emulador va muy lento en tu computadora:

1. **Minimizar** el emulador cuando no lo uses
2. Reducir la **animación del sistema**:
   - En el emulador, ve a Settings → System → Developer options → Window animation scale → 0.5x
3. Usar **Quick Boot** en lugar de Cold Boot:
   - En Device Manager → Edit Device → Boot: Quick Boot
4. Si tienes procesador AMD en Windows, asegúrate de tener **Hyper-V** activado.

---

## PARTE 10: EJECUTAR EN CELULAR REAL

### 10.1 Configurar el Celular

En tu celular Android:

1. Ve a **Configuración → Acerca del teléfono**
2. Busca **"Número de compilación"**
3. Tócalo **7 veces** hasta que diga "Ahora eres desarrollador"
4. Ve a **Configuración → Sistema → Opciones de desarrollador**
5. Activa **"Depuración USB"**
6. (Opcional) Activa **"Instalar por USB"**

### 10.2 Conectar el Celular

1. Conecta el celular a la computadora con el cable USB
2. En el celular puede aparecer un mensaje: "Permitir depuración USB". Toca **"Permitir"**
3. En Android Studio, debería aparecer tu celular en la lista de dispositivos

### 10.3 Si No Aparece el Celular

En Windows a veces faltan drivers. Instálalos:

```
https://developer.android.com/studio/run/win-usb
```

En Mac o Linux normalmente funciona directo.

Para verificar que la computadora detecta el celular:

```bash
# Abrir terminal y escribir:
adb devices

# Debería mostrar algo como:
# List of devices attached
# XXXXXXXX    device
```

Si dice "unauthorized", revisa el celular (debe pedir permiso de depuración).

---

## PARTE 11: ESTRUCTURA FINAL DEL PROYECTO

Tu proyecto debería verse así:

```
MiPrimeraApp/
│
├── app/
│   │
│   ├── src/
│   │   │
│   │   ├── main/
│   │   │   │
│   │   │   ├── java/
│   │   │   │   └── com/
│   │   │   │       └── misitioweb/
│   │   │   │           └── miprimeraapp/
│   │   │   │               │
│   │   │   │               ├── MainActivity.kt
│   │   │   │               ├── SegundaActivity.kt
│   │   │   │               ├── ActivityConFragment.kt
│   │   │   │               ├── ActivityServiceTest.kt
│   │   │   │               ├── MiFragment.kt
│   │   │   │               ├── MiServicio.kt
│   │   │   │               └── MiReceiver.kt
│   │   │   │
│   │   │   ├── res/
│   │   │   │   │
│   │   │   │   ├── layout/
│   │   │   │   │   ├── activity_main.xml
│   │   │   │   │   ├── activity_segunda.xml
│   │   │   │   │   ├── activity_con_fragment.xml
│   │   │   │   │   ├── activity_service_test.xml
│   │   │   │   │   └── fragment_mi.xml
│   │   │   │   │
│   │   │   │   ├── values/
│   │   │   │   │   ├── strings.xml
│   │   │   │   │   ├── colors.xml
│   │   │   │   │   └── themes.xml
│   │   │   │   │
│   │   │   │   └── drawable/
│   │   │   │       └── (imágenes e iconos)
│   │   │   │
│   │   │   └── AndroidManifest.xml
│   │   │
│   │   ├── test/
│   │   └── androidTest/
│   │
│   ├── build.gradle.kts
│   └── proguard-rules.pro
│
├── build.gradle.kts
├── settings.gradle.kts
├── gradle.properties
├── gradlew
├── gradlew.bat
└── gradle/
    └── wrapper/
```

---

## PARTE 12: RESUMEN DE LO QUE APRENDISTE

### Componentes que conoces ahora

| Componente | Para qué sirve | Método principal |
|------------|---------------|------------------|
| **Activity** | Una pantalla de la app | `onCreate()`, `onStart()`, `onResume()` |
| **Fragment** | Una sección dentro de una Activity | `onCreateView()`, `onResume()` |
| **Service** | Tareas en segundo plano | `onCreate()`, `onStartCommand()` |
| **BroadcastReceiver** | Escuchar eventos del sistema | `onReceive()` |

### Ciclo de vida 

```
Creación:      onCreate() → onStart() → onResume()
Destrucción:   onPause() → onStop() → onDestroy()
```

### Flujo de navegación

```
MainActivity
    │
    ├── (click botón) ─→ startActivity(Intent) ─→ SegundaActivity
    │                                                      │
    │                              (finish()) ←─────────────┘
    │
    └── (otro botón) ─→ MiServicio.startService()
```

---

## COSAS QUE PUEDES HACER AHORA

1. Crear un proyecto desde cero en Android Studio
2. Entender y usar el ciclo de vida de Activities y Fragments
3. Crear múltiples Activities y navegar entre ellas
4. Pasar datos entre Activities con Intent extras
5. Crear y usar Fragments dentro de Activities
6. Crear y ejecutar Services en segundo plano
7. Crear BroadcastReceivers para escuchar eventos del sistema
8. Configurar y ejecutar apps en el emulador
9. Ejecutar apps en un celular real

---


