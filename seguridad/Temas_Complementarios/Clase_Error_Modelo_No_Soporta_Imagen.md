# Clase: Errores de Input Multimodal en IA - "Cannot Read Image"

## Entendiendo las limitaciones de entrada en modelos de lenguaje

---

**Versión:** 1.0  
**Fecha:** Abril 2026  
**Proyecto:** Curso de Ciberseguridad - Temas Complementarios

---

## Tabla de Contenidos

1. Introducción al Error
2. ¿Por qué ocurre este error?
3. Modelos de Texto vs Modelos Multimodales
4. Anatomía del Error
5. Cómo manejarlo como Desarrollador
6. Cómo manejarlo como Usuario
7. Workarounds y Soluciones
8. El Futuro de la IA Multimodal
9. Resumen

---

## 1. Introducción al Error

El error:

```
ERROR: Cannot read "image.png" (this model does not support image input).
Inform the user.
```

Es un mensaje común en sistemas de IA y herramientas CLI cuando un usuario intenta procesar un archivo de imagen pero el modelo activo **solo acepta texto**.

### ¿Qué significa?

| Parte del mensaje | Significado |
|-------------------|-------------|
| `Cannot read "image.png"` | El sistema intentó abrir un archivo PNG |
| `this model does not support image input` | El modelo actual no tiene capacidad visual |
| `Inform the user` | Instrucción interna para notificar al usuario |

---

## 2. ¿Por qué ocurre este error?

### 2.1 El modelo es "text-only"

Los LLM tradicionales (como las primeras versiones de GPT, LLaMA, etc.) fueron entrenados exclusivamente con **texto**. No saben interpretar píxeles.

```
┌─────────────────────────────────────────────────────────┐
│                  MODELO TEXT-ONLY                       │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Entrada: TEXTO → Modelo → Salida: TEXTO                │
│                                                         │
│  NO puede recibir:                                      │
│  ❌ Imágenes (PNG, JPG, GIF)                            │
│  ❌ Audio (MP3, WAV)                                    │
│  ❌ Video (MP4, AVI)                                    │
│  ❌ Archivos binarios                                   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 2.2 El pipeline no tiene conversor

Incluso si el modelo soportara imágenes, el **pipeline de entrada** debe estar configurado para convertirlas a un formato que el modelo entienda.

```
Pipeline correcto:
  Imagen → Encoder Visual → Tokens visuales → Modelo → Respuesta

Pipeline que falla:
  Imagen → ??? → Modelo text-only → ERROR
```

### 2.3 Causas comunes

| Causa | Descripción |
|-------|-------------|
| Modelo incorrecto | Usando un modelo text-only cuando se necesita visión |
| Configuración | La herramienta no está configurada para multimodal |
| Formato no soportado | El modelo soporta imágenes pero no ese formato específico |
| Límite de tamaño | La imagen excede el tamaño máximo permitido |
| Bug en la herramienta | Error en el código que maneja inputs |

---

## 3. Modelos de Texto vs Modelos Multimodales

### 3.1 Modelos Text-Only

Solo procesan y generan texto.

| Modelo | Desarrollador | Tipo |
|--------|---------------|------|
| GPT-3 | OpenAI | Text-only |
| LLaMA 2 (base) | Meta | Text-only |
| Claude 2 (early) | Anthropic | Text-only |
| Mistral 7B | Mistral AI | Text-only |
| BERT | Google | Text-only |

### 3.2 Modelos Multimodales

Pueden procesar texto + imágenes (y a veces audio/video).

| Modelo | Desarrollador | Modalidades |
|--------|---------------|-------------|
| GPT-4o | OpenAI | Texto + Imagen + Audio |
| GPT-4V | OpenAI | Texto + Imagen |
| Claude 3.5 Sonnet | Anthropic | Texto + Imagen |
| Gemini 1.5 Pro | Google | Texto + Imagen + Audio + Video |
| LLaVA | Open/Comunidad | Texto + Imagen |
| Qwen2-VL | Alibaba | Texto + Imagen + Video |

### 3.3 Comparación visual

```
┌──────────────────────────────────────────────────────────┐
│              MODELOS DE IA - EVOLUCIÓN                   │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  GPT-3 (2020)                                            │
│  ┌────────────┐                                          │
│  │   TEXTO    │ ──▶  Modelo ──▶  TEXTO                   │
│  └────────────┘                                          │
│                                                          │
│  GPT-4V (2023)                                           │
│  ┌────────────┐    ┌────────────┐                        │
│  │   TEXTO    │ ──▶│            │                        │
│  └────────────┘    │  Modelo    │ ──▶  TEXTO             │
│  ┌────────────┐    │ Multimodal │                        │
│  │  IMÁGENES  │ ──▶│            │                        │
│  └────────────┘    └────────────┘                        │
│                                                          │
│  GPT-4o (2024)                                           │
│  ┌────────────┐    ┌────────────┐                        │
│  │   TEXTO    │ ──▶│            │                        │
│  └────────────┘    │            │                        │
│  ┌────────────┐    │  Modelo    │ ──▶  TEXTO + AUDIO    │
│  │  IMÁGENES  │ ──▶│            │                        │
│  └────────────┘    │            │                        │
│  ┌────────────┐    │            │                        │
│  │   AUDIO    │ ──▶│            │                        │
│  └────────────┘    └────────────┘                        │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

---

## 4. Anatomía del Error

### 4.1 Desglose técnico

```python
# Pseudocódigo de cómo se genera este error

def procesar_input(archivo, modelo):
    """Intenta procesar un archivo con un modelo."""
    
    # Determinar tipo de archivo
    tipo = detectar_tipo(archivo)
    # tipo podría ser: "image", "text", "pdf", etc.
    
    # Verificar capacidades del modelo
    capacidades = modelo.get_capacidades()
    # capacidades podría ser: ["text"] o ["text", "image", "audio"]
    
    # Validar compatibilidad
    if tipo == "image" and "image" not in capacidades:
        # ❌ Aquí se genera el error
        raise ErrorIncompatible(
            f'Cannot read "{archivo.nombre}" '
            f'(this model does not support image input). '
            f'Inform the user.'
        )
    
    # Si es compatible, continuar procesamiento
    return modelo.procesar(archivo)
```

### 4.2 Dónde aparece

| Contexto | Ejemplo |
|----------|---------|
| **CLI tools** | opencode, claude-cli, herramientas de terminal |
| **APIs** | OpenAI API, Anthropic API con modelo incorrecto |
| **Chatbots** | Interfaces web con modelo text-only |
| **SDKs** | LangChain, LlamaIndex con configuración errónea |
| **Agentes AI** | Agentes que reciben archivos no soportados |

### 4.3 Variantes del error

```
# Variantes comunes que puedes encontrar:

"Error: Image input is not supported by this model"

"Unsupported input type: image/png"

"This model only accepts text. Please provide text input only."

"Model 'llama-3-8b' does not support vision. Use a vision-capable model."

"Input validation failed: image data provided but model is text-only"
```

---

## 5. Cómo manejarlo como Desarrollador

### 5.1 Validar antes de enviar

```python
# Python - Validar capacidades antes de procesar

import os
from PIL import Image

def es_imagen(ruta):
    """Verifica si un archivo es una imagen."""
    extensiones_imagen = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp'}
    _, ext = os.path.splitext(ruta.lower())
    return ext in extensiones_imagen

def modelo_soporta_imagen(nombre_modelo):
    """Verifica si el modelo soporta imágenes."""
    modelos_vision = {
        'gpt-4o', 'gpt-4-turbo', 'gpt-4-vision-preview',
        'claude-3-opus', 'claude-3-sonnet', 'claude-3-haiku',
        'gemini-pro-vision', 'llava-1.6'
    }
    return nombre_modelo.lower() in modelos_vision

def procesar_archivo(ruta, modelo):
    """Procesa un archivo de forma segura."""
    
    # Paso 1: Detectar tipo
    if es_imagen(ruta):
        if not modelo_soporta_imagen(modelo):
            print(f"ERROR: Cannot read '{ruta}' (this model does not support image input).")
            print("Sugerencia: Usa un modelo con capacidad de visión como GPT-4o o Claude 3.")
            return None
    
    # Paso 2: Procesar normalmente
    print(f"Procesando {ruta} con {modelo}...")
    # ... lógica de procesamiento ...
```

### 5.2 Extraer texto de imágenes como workaround

```python
# Usar OCR para convertir imagen a texto

import pytesseract
from PIL import Image

def extraer_texto_de_imagen(ruta_imagen):
    """Extrae texto de una imagen usando OCR."""
    # pytesseract → Wrapper de Tesseract OCR
    # Image.open → Abre la imagen con Pillow
    imagen = Image.open(ruta_imagen)
    
    # image_to_string → Convierte imagen a texto
    texto = pytesseract.image_to_string(imagen)
    
    return texto

# Uso:
# 1. Usuario sube imagen
# 2. Extraemos texto con OCR
# 3. Enviamos el texto al modelo text-only
texto = extraer_texto_de_imagen("captura.png")
resultado = modelo_texto.procesar(texto)
```

### 5.3 Cambiar modelo dinámicamente

```python
# Seleccionar modelo según tipo de input

def seleccionar_modelo(tipo_input):
    """Elige el modelo correcto según el tipo de input."""
    
    if tipo_input == "texto":
        return "llama-3-70b"  # Modelo text-only (más barato)
    elif tipo_input == "imagen":
        return "gpt-4o"       # Modelo multimodal
    elif tipo_input == "audio":
        return "whisper-large" # Modelo de audio
    elif tipo_input == "video":
        return "gemini-1.5-pro" # Soporta video
    else:
        raise ValueError(f"Tipo de input no soportado: {tipo_input}")
```

### 5.4 En aplicaciones web

```javascript
// JavaScript - Validar antes de enviar al API

async function enviarArchivoAlModelo(file, modelo) {
    const modelosConVision = [
        'gpt-4o', 'gpt-4-turbo', 'claude-3-opus', 
        'claude-3-sonnet', 'gemini-pro-vision'
    ];
    
    const esImagen = file.type.startsWith('image/');
    
    if (esImagen && !modelosConVision.includes(modelo)) {
        // Mostrar error al usuario
        mostrarError(
            `No se puede procesar "${file.name}". ` +
            `El modelo "${modelo}" no soporta imágenes. ` +
            `Por favor, selecciona un modelo con capacidad de visión.`
        );
        return;
    }
    
    // Continuar con el envío normal
    await procesarInput(file, modelo);
}
```

---

## 6. Cómo manejarlo como Usuario

### 6.1 Opción 1: Cambiar de modelo

Si tu herramienta lo permite, selecciona un modelo con capacidad de visión:

| Si usas... | Cambia a... |
|------------|-------------|
| GPT-3.5 / GPT-4 base | GPT-4o o GPT-4 Turbo |
| Claude 2 | Claude 3.5 Sonnet |
| LLaMA base | LLaVA o Qwen2-VL |
| Gemini Flash | Gemini Pro (con visión) |

### 6.2 Opción 2: Describir la imagen

Si no puedes cambiar de modelo, **describe** la imagen en texto:

```
❌ Subir: captura_error.png

✅ Describir:
"La imagen muestra un error de consola que dice:
'Connection refused on port 5432'.
El sistema es Ubuntu 22.04 con PostgreSQL."
```

### 6.3 Opción 3: Usar OCR primero

Extrae el texto de la imagen y envíalo como texto:

```bash
# En Linux
tesseract imagen.png texto_extraido
cat texto_extraido.txt | tu_herramienta_ia

# En macOS (con comando integrado)
shortcuts run "Extract Text from Image" --input imagen.png

# En Windows (PowerShell con API de Windows)
# Usar Windows.Media.Ocr
```

### 6.4 Opción 4: Herramientas online

Usa herramientas gratuitas para extraer texto de imágenes:

| Herramienta | URL | Uso |
|-------------|-----|-----|
| OnlineOCR | onlineocr.net | Extraer texto de imágenes |
| New OCR | newocr.com | OCR gratuito |
| Google Lens | lens.google.com | Extraer texto con el móvil |
| Copyfish | copyfish.xyz | Extensión de navegador |

---

## 7. Workarounds y Soluciones

### 7.1 Convertir imagen a descripción con API

```python
# Usar un modelo vision para describir la imagen
# y luego enviar la descripción al modelo text-only

import openai

def imagen_a_descripcion(ruta_imagen):
    """Convierte imagen a descripción de texto."""
    
    # Usar GPT-4V para describir la imagen
    with open(ruta_imagen, "rb") as f:
        respuesta = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Describe esta imagen en detalle."},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64.b64encode(f.read()).decode()}"
                            }
                        }
                    ]
                }
            ]
        )
    
    return respuesta.choices[0].message.content

# Flujo:
# 1. Imagen → GPT-4o → Descripción en texto
# 2. Descripción → Modelo text-only → Respuesta final
descripcion = imagen_a_descripcion("captura.png")
respuesta = modelo_texto.procesar(descripcion)
```

### 7.2 Convertir imagen a base64 (para APIs que lo soportan)

```python
import base64
import json

def imagen_a_base64(ruta):
    """Convierte imagen a string base64."""
    with open(ruta, "rb") as f:
        # encode → Convierte bytes a base64
        # decode → Convierte bytes a string UTF-8
        return base64.b64encode(f.read()).decode('utf-8')

# Uso con APIs que soportan imágenes en base64:
payload = {
    "model": "gpt-4o",
    "messages": [{
        "role": "user",
        "content": [
            {"type": "text", "text": "¿Qué ves en esta imagen?"},
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/png;base64,{imagen_a_base64('foto.png')}"
                }
            }
        ]
    }]
}
```

### 7.3 Pipeline automático de fallback

```python
def procesar_con_fallback(archivo, modelo_principal, modelo_fallback):
    """Intenta procesar con el modelo principal, fallback si no soporta."""
    
    try:
        # Intentar con modelo principal
        return modelo_principal.procesar(archivo)
    except ErrorIncompatible as e:
        print(f"Modelo principal no soporta este formato: {e}")
        print(f"Intentando con modelo fallback: {modelo_fallback.nombre}")
        
        # Si es imagen y el fallback es text-only, usar OCR
        if es_imagen(archivo) and not modelo_fallback.soporta_imagen:
            texto = extraer_texto_de_imagen(archivo)
            return modelo_fallback.procesar(texto)
        
        # Si el fallback sí soporta imágenes, enviar directo
        return modelo_fallback.procesar(archivo)
```

---

## 8. El Futuro de la IA Multimodal

### 8.1 Tendencia actual

```
2020: Solo texto
  ↓
2023: Texto + Imagen
  ↓
2024: Texto + Imagen + Audio
  ↓
2025: Texto + Imagen + Audio + Video + 3D
  ↓
2026: Todas las modalidades nativamente
```

### 8.2 Modelos "omni"

Los nuevos modelos tienden a ser **nativamente multimodales**:

| Modelo | Año | Modalidades |
|--------|-----|-------------|
| GPT-4o | 2024 | Texto, imagen, audio |
| Gemini 2.0 | 2024 | Texto, imagen, audio, video |
| Claude 3.5 | 2024 | Texto, imagen |
| LLaMA 3.2 Vision | 2024 | Texto, imagen |
| Qwen2.5-VL | 2025 | Texto, imagen, video |

### 8.3 ¿Desaparecerá este error?

Con el tiempo, **sí**. A medida que los modelos se vuelvan nativamente multimodales por defecto, el error "does not support image input" será cada vez menos común.

Sin embargo, seguirá existiendo para:
- Modelos especializados text-only (más baratos, más rápidos)
- Formatos no soportados (ej: un modelo de imagen que no soporta video)
- Herramientas con modelos antiguos
- Entornos con restricciones de recursos

---

## 9. Resumen

### 9.1 Puntos clave

| Concepto | Descripción |
|----------|-------------|
| El error | Ocurre al enviar imágenes a un modelo text-only |
| La causa | El modelo no fue entrenado para procesar píxeles |
| La solución | Usar modelo multimodal o convertir imagen a texto |
| El futuro | Los modelos tienden a ser multimodales nativos |

### 9.2 Checklist de resolución

| Paso | Acción |
|------|--------|
| 1 | Verificar si el modelo soporta imágenes |
| 2 | Si no, cambiar a modelo multimodal |
| 3 | Si no es posible, usar OCR para extraer texto |
| 4 | Describir la imagen manualmente en texto |
| 5 | Usar pipeline: imagen → descripción → modelo text-only |

### 9.3 Recursos

| Recurso | URL/Info |
|---------|----------|
| Tesseract OCR | https://github.com/tesseract-ocr/tesseract |
| OpenAI Vision API | https://platform.openai.com/docs/guides/vision |
| Anthropic Vision | https://docs.anthropic.com/en/docs/build-with-claude/vision |
| Google Vision API | https://cloud.google.com/vision |
| EasyOCR | https://github.com/JaidedAI/EasyOCR |

---

*Documento creado con fines educativos. Parte del curso de ciberseguridad.*
