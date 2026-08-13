# Actividad 16 — Proyecto final y publicación

**Duración:** 50 min (presentación y cierre) · **Modalidad:** individual · **Entrega:** juego completo en GitHub público

## 1. Objetivos

- Planificar un juego completo con un **GDD mínimo** (documento de diseño).
- Elegir un juego de los vistos y **mejorarlo** con al menos 3 features nuevas.
- Escribir un **README** profesional para el repositorio.
- **Publicar** el juego (GitHub Pages para juegos web) para que cualquiera juegue.
- Presentarlo a la clase.

## 2. Marco teórico

Un juego no termina cuando "funciona". El proceso profesional es:

1. **Diseño (GDD):** escribir qué es el juego, cómo se juega, controles, puntaje, niveles.
2. **Prototipo:** versión mínima que se puede jugar.
3. **Iteración:** jugar, corregir, mejorar (balance, diversión, dificultad).
4. **Documentación:** README, instrucciones, capturas.
5. **Publicación:** subir a internet para que otros jueguen.
6. **Feedback y versión nueva.**

**GDD (Game Design Document)**: documento de 1 a 2 páginas que describe el juego. Tenerlo por escrito ayuda a no perderse y a que otros entiendan tu proyecto. Usá la plantilla que está en la carpeta de materiales (`GDD Plantilla de Documentación.docx`) o la versión mínima de la sección 4.1.

**GitHub Pages**: servicio gratuito de GitHub que publica sitios web estáticos. Si tu juego es un archivo HTML (actividad 7), podés publicarlo en segundos. Si es Pygame o Godot, publicás el código + instrucciones, o exportás Godot a web (HTML).

## 3. Paso a paso

### 3.1 Elegí y planificá tu juego (10 min)

Elegí uno de los juegos del curso y mejoralo. Algunas ideas:

- **Nibbles:** agregá niveles, paredes, modo difícil.
- **Arkanoid:** power-ups, 3 niveles, ladrillos especiales.
- **Batalla naval:** IA más inteligente, sonido, pantalla de victoria bonita.
- **Aventura gráfica:** más escenas, imágenes, música.
- O un juego nuevo combinando ideas (por ejemplo "El mono contra invasores").

### 3.2 Escribí el GDD mínimo (en el README)

### 3.3 Implementá (30 min)

Trabajá en una carpeta nueva `proyecto_final/`. Un orden que funciona:

1. Asegurate de que el juego base funcione.
2. Agregá **una** feature a la vez y probá cada una.
3. Cada feature = un commit con mensaje claro.

### 3.4 Publicá en GitHub Pages (si tu juego es web)

```powershell
# En el repo, creá la carpeta para el sitio y poné tu juego adentro
mkdir proyecto_final/sitio
# copiá tu juego.html como proyecto_final/sitio/index.html
git add .
git commit -m "Clase 16: juego final listo para publicar"
git push
```

1. En GitHub: **Settings** → **Pages** → *Source*: **Deploy from a branch** → rama `main`, carpeta `/proyecto_final/sitio` → Save.
2. Esperá 1 o 2 minutos y entrá a `https://tuusuario.github.io/mis-videojuegos/proyecto_final/sitio/`.

> Para juegos Pygame: publicá el repositorio (ya es público) y poné en el README cómo ejecutarlo. Para Godot: usá *Export → Web* y subí la carpeta generada igual que un sitio web.

## 4. Actividad de cierre: README y presentación

### 4.1 README profesional

```markdown
# [Nombre del juego]

![Captura](captura.png)

Mini-juego hecho en [Pygame / JavaScript / Godot] como proyecto final del
curso "Desarrollo de Videojuegos con IA".

## Cómo se juega
[Descripción de 2 o 3 líneas]

## Controles
- Flechas: mover
- ESPACIO: disparar / saltar

## Cómo ejecutar
python juego.py   (o abrí el HTML en el navegador)

## Créditos
- Código: [tu nombre]
- Asistencia de IA: [nombre del asistente] para generar/ depurar
- Sprites/Sonidos: [fuente, si usaste]

## Versiones
- v1.0: juego base
- v1.1: + power-ups
```

### 4.2 Presentación (2-3 minutos por estudiante)

Contá: qué juego hiciste, qué features agregaste, qué aprendiste y **qué le pediste a la IA**. Mostrá un fragmento del código que te haya costado.

## 5. Usando IA en esta clase (prompts sugeridos)

> **Prompt 1 (ideas):** "Tengo mi Nibbles funcionando. Darme 5 ideas de features que lo hagan más divertido, ordenadas de fácil a difícil."
>
> **Prompt 2 (priorizar):** "Decime cuál de estas features elegir para un proyecto de 1 hora y por qué: [lista de ideas]."
>
> **Prompt 3 (mejorar README):** "Revisá mi README y decime qué le falta para que otro estudiante pueda ejecutar el juego sin ayuda."
>
> **Prompt 4 (balance):** "¿Mi juego es demasiado fácil? Decime qué valores de velocidad/gravedad/puntaje cambiar y por qué."
>
> **Prompt 5 (revisión final):** "Hacé una revisión final de mi código: errores, código repetido, y 3 mejoras de rendimiento."

## 6. Rúbrica de evaluación final

| Criterio | Logrado (10-9) | En proceso (8-6) | No logrado (5-0) |
|---|---|---|---|
| GDD / planificación | GDD completo en README | README parcial | Sin plan |
| Features nuevas | 3+ implementadas | 1-2 | Ninguna |
| Calidad del código | Funciona y es legible | Funciona a medias | No funciona |
| Publicación | Web publicada (o instrucciones claras) | Solo repo | Sin repo |
| Presentación | Explica y muestra código | Cuenta sin mostrar | No presenta |
| Uso de IA | La usó y explica qué pidió | La usó poco | No la usó |

## 7. Para seguir después del curso

- Publicá todos tus juegos web en GitHub Pages y armá un **índice con links**.
- Probá **Godot 4** con un proyecto propio más grande.
- Sumate a una **game jam** (hackathon de juegos de 48 h) para practicar en equipo.
- Seguí usando IA, pero con el método de esta clase: especificar, generar, probar, iterar.
