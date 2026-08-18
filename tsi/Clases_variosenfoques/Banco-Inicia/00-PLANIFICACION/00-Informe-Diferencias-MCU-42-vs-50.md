# Informe de diferencias: MCU 4.2 vs MCU 5.0

> **Objetivo:** explicar qué cambió entre el **Marco de Ciberseguridad 4.2** y el **5.0** de Agesic, para que el equipo entienda por qué el kit del Banco está construido sobre el 5.0 y qué implica no migrar referencias viejas (4.2) en documentos, listas de verificación o matrices.

---

## 1. Ficha de cada versión

| Aspecto | MCU 4.2 | MCU 5.0 |
|---|---|---|
| **Publicación** | 28/12/2022 (Marco de Referencia) | Versión 5.0 – Agosto 2025 |
| **Base internacional** | NIST CSF **1.1** | NIST CSF **2.0** |
| **Funciones** | **5**: Identificar (ID), Proteger (PR), Detectar (DE), Responder (RE), Recuperar (RC) | **6**: Gobernar (GV), Identificar (ID), Proteger (PR), Detectar (DE), Responder (RS), Recuperar (RC) |
| **Categorías** | 22 (basadas en CSF 1.1) | 22 (basadas en CSF 2.0), reorganizadas |
| **Requisitos** | Definidos por subcategoría, asociados a ISO 27001:2013, COBIT 5, CIS CSC, NIST 800-53 rev.4 | **72 requisitos** con prioridad por perfil |
| **Prioridades** | **P1 / P2 / P3 / N/A** (corto, medio, largo plazo; 1-2-3 años) | **Alta / Media / Baja** (por impacto y línea de base) |
| **Perfiles** | Básico (B), Estándar (E), Avanzado (A) | Básico, Estándar, Avanzado + **perfiles comunitarios** por sector |
| **Madurez** | Modelo de madurez 0-4 | Modelo de madurez **vinculado a controles** en cada nivel (más objetivo) |
| **Alcance normativo** | Documento orientativo | Reforzado por **Decreto 66/025** (obligatoriedad, RSI, notificación al CERTuy, trazabilidad ≥ 12 meses) |
| **Apartados sectoriales** | No | Sí: **salud** y **sistema de pagos** (le aplica al Banco) |

---

## 2. Lo más importante: nace la función "Gobernar" (GV)

En el 4.2 la **gobernanza** era una categoría dentro de Identificar (`ID.GO`). En el 5.0 pasa a ser una **función completa al tope del ciclo** (`GV`), con 6 categorías propias.

```
MCU 4.2 (5 funciones)              MCU 5.0 (6 funciones)
                                   GV (Gobernar)  ← NUEVA, 6 categorías
ID ── Identificar                  ID (Identificar)
PR ── Proteger                     PR (Proteger)
DE ── Detectar                     DE (Detectar)
RE ── Responder                    RS (Responder)
RC ── Recuperar                    RC (Recuperar)
```

Esto refleja un cambio de paradigma: la ciberseguridad deja de ser un tema técnico de "Identificar/Proteger" y pasa a ser **responsabilidad de la dirección** (política, roles, supervisión, cadena de suministro).

---

## 3. Cambio de códigos por función (mapeo 4.2 → 5.0)

> Regla práctica: si un documento cita códigos tipo `RE.xx` o `ID.GO`, es de la **versión 4.2**. Los códigos del 5.0 usan `GV.*`, `RS.*` y los códigos CSF 2.0 (`ID.AM`, `PR.AA`, `DE.CM`, etc.).

### Gobernar (nueva)
| MCU 5.0 | Origen en 4.2 |
|---|---|
| GV.OC · Contexto organizativo | ID.AN (Ambiente del negocio) + contexto |
| GV.RM · Estrategia de gestión de riesgos | ID.GR (Estrategia) |
| GV.RR · Roles y responsabilidades | ID.GO (Gobernanza) |
| GV.PO · Política | ID.GO |
| GV.OV · Supervisión | ID.GO |
| GV.SC · Cadena de suministro | ID.CS |

### Identificar
| MCU 5.0 | MCU 4.2 |
|---|---|
| ID.AM · Gestión de activos | ID.GA |
| ID.RA · Evaluación de riesgos | ID.ER |
| ID.IM · Mejora (NUEVA) | — (dispersa en RE.ME / RC.ME) |

### Proteger
| MCU 5.0 | MCU 4.2 |
|---|---|
| PR.AA · Identidad, autenticación y control de acceso | PR.CA |
| PR.AT · Concientización y capacitación | PR.CF |
| PR.DS · Seguridad de datos | PR.SD |
| PR.PS · Seguridad de plataformas (NUEVA) | PR.PI + PR.TP (reorganizadas) |
| PR.IR · Resiliencia de la infraestructura (NUEVA) | PR.MA (mantenimiento) + PR.PI |

### Detectar
| MCU 5.0 | MCU 4.2 |
|---|---|
| DE.CM · Monitoreo continuo | DE.MC |
| DE.AE · Análisis de eventos adversos | DE.AE (se mantiene) |
| — | DE.PD (Procesos de detección) → absorbida en DE.CM / DE.AE |

### Responder
| MCU 5.0 | MCU 4.2 |
|---|---|
| RS.MA · Gestión de incidentes | RE.PR (Planificación de respuesta) |
| RS.AN · Análisis de incidentes | RE.AN |
| RS.CO · Notificación y comunicación | RE.CO |
| RS.MI · Mitigación | RE.MI |
| — | RE.ME (Mejoras) → migra a ID.IM |

### Recuperar
| MCU 5.0 | MCU 4.2 |
|---|---|
| RC.RP · Ejecución del plan de recuperación | RC.PR |
| RC.CO · Comunicación de la recuperación | RC.CO |
| — | RC.ME (Mejoras) → migra a ID.IM |

---

## 4. Cambios en prioridades y perfiles

| Concepto | MCU 4.2 | MCU 5.0 |
|---|---|---|
| Escala de prioridad | P1 (≤1 año), P2 (1-2 años), P3 (2-3 años), N/A | Alta, Media, Baja |
| Base de la prioridad | Plazo de implementación | Criticidad: línea de base, primera línea de defensa, resiliencia |
| Perfiles | B / E / A | B / E / A + perfiles comunitarios (plantillas por sector con línea base verde y metas a 3 años) |
| Madurez | 5 niveles (0-4) | 5 niveles **ligados a cumplimiento de controles específicos** (más auditable) |

---

## 5. Requisitos: del "por subcategoría" al "72 requisitos"

- **4.2:** los requisitos se listaban asociados a cada subcategoría (ej. `GA.1 Identificar formalmente los activos...`), derivados de ISO 27001:2013, COBIT 5, CIS CSC y NIST 800-53 rev.4.
- **5.0:** Agesic define **72 requisitos** explícitos. Un mismo requisito puede mencionarse en más de una subcategoría. La Guía de implementación y la Guía de auditoría se actualizaron a esta versión.

> **Impacto para el Banco:** el kit usa los códigos del 5.0 (`GV.OV`, `ID.AM`, `PR.AA`, `DE.CM`, `RS.MA`, `RC.RP`, etc.). Cualquier checklist, matriz o documento que cite `ID.GO`, `PR.CA`, `RE.PR`, `DE.MC`, `RC.PR` proviene de la versión 4.2 y debe migrarse.

---

## 6. Consecuencias normativas (por qué importa migrar)

1. **Decreto 66/025** refuerza la adopción del MCU, la designación del RSI, la notificación de incidentes al CERTuy y la trazabilidad mínima de 12 meses. La obligatoriedad ya no es solo para organismos públicos.
2. El **Banco** opera el **sistema de pagos** → le aplican los apartados sectoriales del 5.0 y debe aspirar a **perfil Avanzado** (indisponibilidad máx. 24 h).
3. Los **perfiles comunitarios** del 5.0 dan línea base concreta para el sector financiero; conviene usarlos como insumo de `ID-05_Perfil-Ciberseguridad.md`.
4. Al **auditar**, Agesic lo hará con la **lista de verificación del 5.0** (modelo de madurez ligado a controles). Seguir referenciando 4.2 genera brechas de evidencia.

---

## 7. Referencias oficiales

- MCU 4.2 (Marco de Referencia, 28/12/2022): https://www.gub.uy/agencia-gobierno-electronico-sociedad-informacion-conocimiento/comunicacion/publicaciones/marco-ciberseguridad-42
- MCU 5.0 (Versión 5.0 – Agosto 2025): https://www.gub.uy/agencia-gobierno-electronico-sociedad-informacion-conocimiento/comunicacion/publicaciones/marco-ciberseguridad-50
- Guía de implementación del MCU 5.0 y lista de verificación (sitio de Agesic).
- Documento interno: `01-CURSO-RSI/02-Marco-Ciberseguridad-50-Agesic.md` y `00-Matriz-Correspondencia-Normativa.md` (ya alineados al 5.0).
