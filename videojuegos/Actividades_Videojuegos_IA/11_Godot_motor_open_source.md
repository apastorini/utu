# Actividad 11 — Motor open source: Godot

**Duración:** 50 min · **Modalidad:** individual · **Entrega:** repo GitHub público

## 1. Objetivos

- Entender qué es un **motor de videojuegos** y en qué se diferencia de programar todo a mano.
- Instalar **Godot**, un motor open source gratuito.
- Aprender los conceptos de **nodos**, **escenas** y **señales**.
- Hacer un mini-juego: mover un personaje y juntar monedas.

## 2. Marco teórico

Un **motor de videojuegos** (engine) es un programa que ya trae resuelto lo más difícil: dibujado, físicas, colisiones, sonido, manejo de inputs y exportación a distintas plataformas. El creador se concentra en la **lógica y el contenido**.

Ejemplos de motores: Unity, Unreal, Godot, Construct, RPG Maker.

**Godot** es open source, gratis, liviano y con su propio lenguaje de scripts llamado **GDScript** (muy parecido a Python). Sus conceptos básicos:

- **Escena**: un conjunto organizado de nodos que forma un nivel, un personaje o una pieza.
- **Nodo**: la unidad básica (un sprite, un rectángulo de colisión, un sonido, etc.). Los nodos se organizan en árbol (jerarquía padre-hijo).
- **Señal** (signal): un "aviso" que se emite cuando pasa algo (por ejemplo, que un cuerpo entró en un área) y que conectamos a una función para reaccionar.

Un personaje que se mueve es un nodo `CharacterBody2D` (cuerpo que puede chocar y desplazarse) con un `CollisionShape2D` (su forma de colisión). Las monedas son `Area2D` (áreas que detectan cuando otro cuerpo entra).

## 3. Instalación de Godot

1. Andá a https://godotengine.org/download
2. Descargá la versión **Godot 4** (estándar, .NET es para programar en C#).
3. Descomprimí el archivo (no necesita instalación, se ejecuta el `.exe`).
4. En Windows, Godot corre con el **Direct3D** o **OpenGL**; si abrís y se ve mal, probá abrir con "Compatibility".

```powershell
# Verificá que el archivo bajó y ejecutalo
Get-ChildItem Descargas -Filter "Godot*"
```

> Si preferís un motor web (sin instalar): podés probar alternativas como PICO-8, o usar este curso con **Pyxel**, pero en esta clase vamos con Godot porque es el estándar open source.

## 4. Paso a paso

### 4.1 Creá el proyecto

1. Abrí Godot → **New Project**.
2. Nombre: `monedas_godot`. Carpeta: dentro de `mis-videojuegos/clase_11_godot/`.
3. **Editor**: elegí el modo **3D**... no, elegí **2D** (es un juego en 2D).
4. Create.

### 4.2 Creá la escena del jugador

1. En el panel *Scene* (arriba a la izquierda) → **+** → agregá un nodo raíz `CharacterBody2D`. Nombralo `Jugador`.
2. Clic derecho en `Jugador` → **Add Child Node** → `Sprite2D` (esto mostrará una imagen; sin imagen usa un ícono por defecto).
3. Agregá otro hijo → `CollisionShape2D` → en la propiedad `Shape` → *New RectangleShape2D* (tamaño aprox. 32x32).
4. Clic derecho en `Jugador` → **Attach Script** → Create (se abre el editor de GDScript). Pegá este código:

```gdscript
extends CharacterBody2D

@export var velocidad := 300.0
var monedas := 0

func _physics_process(delta: float) -> void:
	# Input.get_axis devuelve -1 (izquierda), 0 o +1 (derecha)
	var direccion := Input.get_axis("ui_left", "ui_right")
	velocity.x = direccion * velocidad
	move_and_slide()

	# mover también en vertical con arriba/abajo
	var vertical := Input.get_axis("ui_up", "ui_down")
	velocity.y = vertical * velocidad
	move_and_slide()
```

> `Input.get_axis` usa las acciones predefinidas `ui_left`, `ui_right`, etc., que ya existen en Godot.

### 4.3 Creá la escena de la moneda

1. **Scene** → + → nodo raíz `Area2D`, nombralo `Moneda`.
2. Agregale un hijo `Sprite2D` y otro `CollisionShape2D` (círculo, radio ~12).
3. En el `CollisionShape2D`, marcá el área: el nodo raíz `Area2D` ya tiene en *Inspector* una sección *Monitoring*; dejá el **monitoring = On** (viene así).
4. Clic derecho en `Moneda` → **Attach Script** → este código:

```gdscript
extends Area2D

# Señal: cuando un cuerpo entra en el área
func _on_body_entered(body: Node2D) -> void:
	if body.name == "Jugador":
		body.monedas += 1
		print("Monedas: ", body.monedas)
		queue_free()   # destruir la moneda
```

5. Volvé a la escena del jugador y en el `Jugador` (nodo raíz), en *Node > Signals*, conectá `body_entered`... no: la conexión va en la moneda. Asegurate de tener el script de la moneda pegado; luego en el editor, **Scene > Run** va a necesitar la escena principal.

### 4.4 Armá el nivel

1. **Project > Project Settings > Main Scene**: elegí una escena para el nivel.
2. Creá una nueva escena con nodo raíz `Node2D` llamada `Nivel`.
3. Arrastrá la escena `Moneda.tscn` varias veces dentro de `Nivel` (instancias) y ubicalas en distintos lugares.
4. Arrastrá `Jugador.tscn` como hijo de `Nivel`.
5. Ejecutá con **F5** o el botón Play. Movete con las flechas y juntá monedas (la consola imprime el contador).

## 5. Actividad de cierre (para el commit)

1. Agregá **más monedas** (5 o 6 instancias) en posiciones distintas.
2. Hacé que al juntar 3 monedas se muestre `"Ganaste"` en pantalla (podés usar el nodo `Label` y una variable, o imprimir en consola).
3. Guardá el proyecto en git (Godot genera una carpeta `.godot/` que NO hay que subir). Creá un `.gitignore`:

```gitignore
.godot/
```

4. Commit y push:

```powershell
git add .
git commit -m "Clase 11: Godot - personaje que junta monedas"
git push
```

## 6. Usando IA en esta clase (prompts sugeridos)

> **Prompt 1:** "¿Cuál es la diferencia entre `CharacterBody2D` y `Area2D` en Godot 4? ¿Cuándo uso cada uno?"
>
> **Prompt 2:** "Mi personaje no se mueve. Este es mi script y la estructura de nodos: [describí lo que hiciste]. ¿Qué falta?"
>
> **Prompt 3:** "¿Cómo agrego una cámara que siga al jugador (`Camera2D`)? Mostrame los pasos exactos."
>
> **Prompt 4:** "¿Cómo exporto mi juego de Godot a Windows (.exe) y a web (HTML) paso a paso?"

## 7. Desafíos para seguir practicando

- **Exportar** el juego a Windows y a la web (Export > Add Preset).
- Convertirlo en **plataformas**: usar `is_on_floor()` y un salto con `Input.is_action_just_pressed("ui_accept")`.
- Añadir un **Timer** para limitar el tiempo de juego.
- Sonidos con `AudioStreamPlayer`.
- Publicar la versión web del juego en GitHub Pages (actividad 16).

## 8. Rúbrica de evaluación

| Criterio | Logrado | En proceso | No logrado |
|---|---|---|---|
| Instaló y abrió Godot | Corre el editor | Instaló con ayuda | No |
| Entiende nodos/escenas | Explica y arma | Arma guiado | No |
| Personaje se mueve | Correcto | Parcial | No |
| Juntar monedas | Funciona con señal | Con fallas | No |
