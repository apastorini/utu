# Estructura de Carpetas del SGSI del Banco

> **Código:** EST-CARPETAS-001 · **Versión:** 1.0
> **Objetivo:** definir **dónde vive cada documento y evidencia** del SGSI, quién puede verlo/editar y cómo se controlan las versiones. Es la "memoria" del sistema.

---

## 1. Principios

1. **Un solo lugar de verdad** (repositorio oficial, ej. SharePoint/Drive del Banco o carpeta en red con control de acceso).
2. **Control de acceso por clasificación**: los documentos del SGSI se clasifican (ver ID-ASS-02) y solo acceden quienes deben.
3. **Versión y aprobación controladas**: cada documento tiene código, versión, estado y responsable.
4. **Evidencias separadas de plantillas**: la plantilla (documento en blanco) no se mezcla con la evidencia (documento lleno y aprobado).
5. **Retención**: guardar al menos el ciclo de revisión vigente + la versión anterior; los registros de incidentes y auditorías se conservan según normativa.

## 2. Árbol de carpetas del repositorio SGSI

```
SGSI-Banco/
├── 00-GOBERNANZA/
│   ├── 01-Politicas/            ← GV-01, GV-02, GV-03, GV-04, GV-05, GV-06
│   ├── 02-Actas-Comite/         ← actas de reuniones del Comité (evidencia)
│   ├── 03-Resoluciones/         ← designación RSI, DPD, aprobaciones
│   └── 04-Matriz-Normativa/     ← matriz de correspondencia (MCU/ISO/BCU/URCDP)
├── 01-IDENTIFICACION/
│   ├── 01-Inventario-Activos/   ← ID-01 (por proceso), mapas de red, diagramas
│   ├── 02-Clasificacion/        ← ID-ASS-02
│   ├── 03-Riesgos/              ← ID-02 metodología, ID-03 registro, ID-04 plan, SoA
│   └── 04-Perfil-Ciberseguridad/← ID-05 diagnóstico y objetivo
├── 02-PROTECCION/
│   ├── 01-Accesos/              ← PR-01 y registros de revisión de accesos
│   ├── 02-Datos/                ← PR-03 cifrado, clasificación, backups lógicos
│   ├── 03-Fisica/               ← PR-04, planos, registros de ingreso
│   ├── 04-Respaldo/             ← PR-05, resultados de pruebas de restauración
│   ├── 05-Vulnerabilidades/     ← PR-06, reportes de escaneo
│   ├── 06-Desarrollo/           ← PR-07 SDLC, revisiones de código
│   ├── 07-Terceros/             ← PR-08, GV-05, contratos con cláusulas de seguridad
│   └── 08-Personas/             ← PR-02 capacitación, acuerdos de confidencialidad
├── 03-DETECCION/
│   ├── 01-Monitoreo-Logs/       ← DE-01, arquitectura SIEM
│   ├── 02-Anomalias/            ← DE-02, alertas y casos investigados
│   └── 03-Pruebas/              ← DE-03 pentest, reportes y plan de remediación
├── 04-RESPUESTA/
│   ├── 01-Plan-Incidentes/      ← RS-01 y versiones
│   ├── 02-Notificaciones/       ← RS-02, URCDP-02, constancias de envío
│   ├── 03-Forense/              ← RS-03, preservación de evidencia
│   └── 04-Incidentes-Registro/  ← registro de incidentes (números, estados, informes)
├── 05-RECUPERACION/
│   ├── 01-BCP/                  ← RC-01 (BIA, BCP)
│   ├── 02-DRP/                  ← RC-02 (DRP, resguardo art. 492)
│   ├── 03-Crisis/               ← RC-03 comunicación
│   └── 04-Pruebas/              ← informes de simulacros y pruebas
├── 06-CUMPLIMIENTO/
│   ├── 01-URCDP/                ← URCDP-01…06, inscripciones, EIPD, ARCO
│   ├── 02-BCU/                  ← BCU-01…06, reportes y comunicaciones al BCU
│   └── 03-AUDITORIAS/           ← BCU-05, informes de auditoría interna/externa
├── 07-MEJORA/
│   ├── 01-Indicadores/          ← P-MET-01 y datos mensuales
│   ├── 02-Revision-Direccion/   ← GV-06 informes
│   ├── 03-No-Conformidades/     ← hallazgos y acciones correctivas
│   └── 04-Lecciones/            ← RC-04
├── 08-TEMPLATES/                ← copias originales de las plantillas (este kit)
└── 09-ARCHIVO/                  ← versiones anteriores, documentos obsoletos
```

> **Tip:** cada carpeta `0X-` del repositorio corresponde a una **función del MCU 5.0** (Gobernar, Identificar, Proteger, Detectar, Responder, Recuperar) + Cumplimiento y Mejora. Así el vínculo entre documento y marco es directo.

## 3. Nomenclatura de archivos

Formato recomendado para cada archivo:

```
[CÓDIGO]_[Nombre sin acentos ni espacios]_[VXX.X]_[ESTADO].md/docx
```

Ejemplos:
- `GV-01_Politica-Seguridad-Info_V1.0_Aprobado.docx`
- `ID-03_Registro-Riesgos_V1.2_En-Revision.xlsx`
- `RC-01_BCP_V1.0_Borrador.docx`

Estados: `Borrador`, `En-Revision`, `Aprobado`, `Obsoleto`.

## 4. Control de cambios (tabla por documento)

| Código | Título | Versión | Fecha | Estado | Aprobador |
|---|---|---|---|---|---|
| GV-01 | Política de Seguridad de la Información | 1.0 | | Aprobado | Directorio |
| ID-03 | Registro de Riesgos | 1.2 | | En revisión | RSI |
| ... | | | | | |

## 5. Accesos por rol (matriz mínima)

| Carpeta | RSI | DPD | Div. TI | Comité | Directorio | Auditoría |
|---|---|---|---|---|---|---|
| 00-GOBERNANZA | R | R | - | R | R | R |
| 01-IDENTIFICACION | R | C | C | R | I | R |
| 02-PROTECCION | R | C | R | I | I | R |
| 03-DETECCION | R | I | R | I | I | R |
| 04-RESPUESTA | R | R | R | R | C | R |
| 05-RECUPERACION | R | I | R | R | C | R |
| 06-CUMPLIMIENTO | R | R | I | R | I | R |
| 07-MEJORA | R | I | I | R | R | R |

**R** = Lectura/Escritura (propietario) · **C** = Consulta · **I** = Informado (solo lectura) · `-` = sin acceso.

## 6. Copias de seguridad del repositorio

El propio repositorio del SGSI es un **activo crítico**: debe incluirse en las copias de respaldo (PR-05) y su restauración debe probarse, porque sin él no se puede demostrar cumplimiento.

## 7. Revisión de esta estructura

Esta estructura se revisa: (a) al final de cada fase del plan, (b) cuando se agrega un documento nuevo, (c) anualmente.
