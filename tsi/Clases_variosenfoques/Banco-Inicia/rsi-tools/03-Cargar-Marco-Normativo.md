# TOOLS-03 · Cargar el Marco Normativo (MCU 5.0, BCU, URCDP, Decreto 66/025)

> **Función del MCU 5.0:** Gobernar (GV): organizar el marco normativo que obliga al Banco y dejarlo disponible para todo el SGSI.
> **ISO/IEC 27001:** El contexto de la organización (cláusulas 4.1–4.2) y la determinación de requisitos legales (cláusula 6.1.3, A.5.34–A.5.36) exigen conocer y documentar las obligaciones.
> **BCU / URCDP / Decreto 66/025:** Todo el curso necesita las normas cargadas para correlacionar evidencia.
> **Nivel del curso:** 🟡 Practicar

---

## 1. Por qué "cargar" las normas primero

Antes de instalar herramientas, el RSI debe tener el **marco normativo** accesible y ordenado. Las herramientas producen evidencia; las normas dicen **qué evidencia se necesita**. Si no tenés las normas cargadas, no sabés qué demostrar.

Este módulo crea la **estructura documental del laboratorio** y descarga los documentos oficiales desde las fuentes de referencia (sitios oficiales del Estado uruguayo).

---

## 2. Crear la estructura de carpetas del repositorio normativo

Creá esta estructura dentro de tu repositorio documental del SGSI (o en tu disco de laboratorio):

```
Repositorio-SGSI\
├── 00-NORMATIVA\
│   ├── 01-Agesic-MCU5.0\
│   ├── 02-BCU-EMG\
│   ├── 03-URCDP-ProtDatos\
│   ├── 04-Decreto-66-025\
│   ├── 05-ISO-27001\
│   └── 06-Otros (Circular 2227, etc.)\
├── 01-POLITICAS\
├── 02-ACTIVOS\
├── 03-RIESGOS\
├── 04-EVIDENCIA\
└── 05-INCIDENTES\
```

En PowerShell/terminal de Windows:

```powershell
$base = "C:\Repositorio-SGSI"
@("00-NORMATIVA\01-Agesic-MCU5.0","00-NORMATIVA\02-BCU-EMG","00-NORMATIVA\03-URCDP-ProtDatos","00-NORMATIVA\04-Decreto-66-025","00-NORMATIVA\05-ISO-27001","00-NORMATIVA\06-Otros","01-POLITICAS","02-ACTIVOS","03-RIESGOS","04-EVIDENCIA","05-INCIDENTES") | ForEach-Object { New-Item -ItemType Directory -Path (Join-Path $base $_) -Force }
```

---

## 3. Descargar las normas desde las fuentes oficiales

> ⚠️ Usá siempre **sitios oficiales** del Estado (gub.uy, bcu.gub.uy, urcdp.gub.uy, impo.com.uy, iso.org). El kit `README.md` tiene los enlaces en la sección 7.

| Norma | Qué buscar | Carpeta destino |
|---|---|---|
| MCU 5.0 + guía de implementación | Sitio de Agesic → "Marco de Ciberseguridad 5.0" → descargar PDF y guía | `01-Agesic-MCU5.0` |
| Guía EMG (Estándares Mínimos de Gestión) | Sitio del BCU → "Estándares Mínimos de Gestión – Seguridad de la Información" | `02-BCU-EMG` |
| RNRCSF art. 492 (riesgo TIC) | Sitio del BCU → normativa sobre riesgo de TIC | `02-BCU-EMG` |
| Circular 2227 (riesgo operacional) | Sitio del BCU → normativa | `06-Otros` |
| Ley 18.331 y Ley 19.670 | IMPO (impo.com.uy) | `03-URCDP-ProtDatos` |
| Decreto 64/020 | IMPO (reglamento de la Ley 19.670) | `03-URCDP-ProtDatos` |
| Decreto 66/025 | IMPO (reglamenta cometidos de Agesic en seguridad) | `04-Decreto-66-025` |
| ISO/IEC 27001:2022 | Si el Banco la tiene licenciada (no piratear) | `05-ISO-27001` |
| Guías SGSI Agesic (planillas xlsx) | Sitio de Agesic → guías del MCU | `01-Agesic-MCU5.0` |

---

## 4. Nombrar cada documento con un código

Para poder citar las normas en las plantillas del kit, guardá cada PDF con un nombre tipo:

- `MCU-50_2025.pdf`
- `BCU-EMG_SeguridadInformacion.pdf`
- `Ley-18331_ProtDatos.pdf`
- `Ley-19670_Vulneraciones.pdf`
- `Decreto-64020_Reglamento-L19670.pdf`
- `Decreto-66025_Agesic-Seguridad.pdf`
- `Circular-2227_RiesgoOperacional.pdf`

> Este código es el que después vas a citar en las plantillas (por ejemplo, en la MATRIZ-001 y en las URCDP).

---

## 5. Cruzar las normas con las plantillas (MATRIZ-001)

El kit tiene la matriz en `00-PLANIFICACION/00-Matriz-Correspondencia-Normativa.md`. Tu tarea:

1. Abrí la matriz y verificá que lista cada norma con su función MCU 5.0 y sus plantillas.
2. Marcá con "descargada" cada norma que cargaste en el repositorio.
3. Cuando una herramienta produzca evidencia, vas a poder anotar "evidencia de la norma X, carpeta 04-EVIDENCIA".

---

## 6. Herramienta recomendada para el repositorio

- **Obsidian** (open source, gratuito para uso personal) o **Joplin**: para enlazar notas entre normas, plantillas y evidencias.
- **LibreOffice** (open source): para abrir/editar las planillas de Agesic y de riesgos sin depender de Microsoft.

Instalación en Windows:

```powershell
winget install Obsidian.Obsidian
winget install TheDocumentFoundation.LibreOffice
```

---

## 7. Cómo volcarlo a las plantillas del kit

- **GV-01 (Política)**: citá en la política el marco normativo que obliga al Banco.
- **GV-02 (Alcance)**: el alcance del SGSI se define sabiendo qué normas aplican.
- **MATRIZ-001**: la matriz de correspondencia se completa con el repositorio descargado.

---

## 8. Lista de verificación del módulo

- ☐ Creé la estructura `Repositorio-SGSI\`.
- ☐ Descargué MCU 5.0 y su guía desde el sitio de Agesic.
- ☐ Descargué la Guía EMG del BCU y el RNRCSF art. 492.
- ☐ Descargué Ley 18.331, Ley 19.670 y Decreto 64/020 desde IMPO.
- ☐ Descargué el Decreto 66/025 desde IMPO.
- ☐ Cada PDF tiene un nombre con código.
- ☐ La MATRIZ-001 está marcada con las normas descargadas.

---

**Documentos relacionados:** GV-01, GV-02, MATRIZ-001, HERRAM-001
