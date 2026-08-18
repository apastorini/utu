# ID-02 · Metodología de Análisis y Evaluación de Riesgos del Banco

> ⚠️ **Alerta:** este documento menciona **nombres propios del organigrama del Banco** (personas y cargos, abril 2026). Antes de usar el documento, verificá la vigencia de esos nombres contra el organigrama actual.
> **Función del MCU 5.0:** Identificar (ID.RA — Evaluación de riesgos) · Gobernar (GV.RM — Estrategia de gestión de riesgos)
> **ISO/IEC 27001:** Cláusula 6.1 (Planificación del tratamiento de riesgos) · ISO/IEC 27005 (guía de gestión de riesgos)
> **BCU:** Circular 2227 (gestión del riesgo operacional) · EMG · Marco de Riesgos
> **URCDP:** Ley 18.331 art. 10 · Decreto 64/020 art. 6.f (Evaluación de Impacto de Protección de Datos)
> **Nivel del curso:** 🟡 Practicar · 🔴 Aplicar

## 1. Qué es y por qué existe
La **Metodología de Análisis y Evaluación de Riesgos** es el documento que define **cómo el Banco mide sus riesgos de seguridad de la información**. Establece las reglas del juego: qué escalas usar, cómo se combina probabilidad e impacto, qué significa cada nivel de riesgo y qué nivel es aceptable. Es el "juego de reglas" que luego se aplica en ID-03.
Sin una metodología única, cada área mediría distinto y no se podrían comparar riesgos ni priorizar inversiones. El BCU, vía Circular 2227, exige gestionar el riesgo operacional de forma estructurada; Agesic pide un proceso de evaluación de riesgos documentado (ID.RA); y la URCDP exige medidas de seguridad "adecuadas al riesgo" de las bases con datos personales. La metodología es la evidencia de que existe **un proceso**, no decisiones aisladas.
Esta metodología usa un **enfoque cualitativo** (escalas de probabilidad e impacto de 1 a 5 y matriz de riesgo de 5×5), recomendado para empezar porque es entendible por la dirección, auditable y suficiente para un banco del tamaño del Banco. Puede complementarse con análisis cuantitativo (pérdida esperada en pesos) para los riesgos más altos.
## 2. Marco de referencia
| **Marco** | **Referencia** | **Qué exige aplicable al Banco** |
|---|---|---|
| **MCU 5.0 (Agesic)** | ID.RA (identificar, evaluar, priorizar riesgos); GV.RM (apetito de riesgo) | Evaluación de riesgos documentada, repetible y con criterios de priorización |
| **ISO/IEC 27001** | Cláusula 6.1, 8.2; ISO/IEC 27005 | Metodología definida, criterios de aceptación y tratamiento documentados |
| **BCU** | Circular 2227; EMG · Marco de Riesgos | Gestión del riesgo operacional con identificación, medición y control |
| **URCDP** | Ley 18.331 art. 10; D. 64/020 | Medidas proporcionales al riesgo; base de la Evaluación de Impacto de Protección de Datos |

## 3. Cómo completar esta plantilla (guía de llenado)
1. **Confirmá el apetito de riesgo** con la Gerencia General y el Área de Riesgos: qué nivel de riesgo acepta el banco sin tratamiento adicional. Documentalo en el punto 5.
2. **Adoptá las escalas** del punto 3 (probabilidad e impacto de 1 a 5) y la matriz de calor del punto 4. No las modifiques sin aprobación del Comité.
3. **Definí los criterios de impacto** específicos del Banco: reputacional (prensa), regulatorio (BCU/URCDP), financiero (pérdida en pesos), operacional (horas de indisponibilidad) y legal.
4. **Calibrá** los niveles con un taller: que distintas áreas entiendan igual qué es "impacto 4" o "probabilidad 3". La calibración evita que un área sobrestime todo.
5. **Definí los roles** del proceso (punto 6): quién identifica riesgos, quién los evalúa, quién decide el tratamiento.
6. **Fijá la frecuencia** de re-evaluación: al menos anual, y cada vez que cambie algo relevante (nuevo sistema, nueva norma, incidente mayor).
7. **Consultá en el Banco:** Área Riesgos — Jefe de Departamento Riesgos No Financieros (Melissa Moraes) para calibrar con el riesgo operacional existente; División TI (Bernardo Ureta) por el riesgo tecnológico; y el Comité de Seguridad de la Información para aprobar la metodología.
## 4. Plantilla del documento

### ENCABEZADO
| **Campo** | **Valor** |
|---|---|
| **Código** | ID-02 |
| **Título** | Metodología de Análisis y Evaluación de Riesgos |
| **Versión** | 1.0 |
| **Estado** | [Borrador / En revisión / Aprobado] |
| **Fecha de aprobación** | [COMPLETAR] |
| **Elaborado por** | RSI con el Área de Riesgos |
| **Revisado por** | Comité de Seguridad de la Información |
| **Aprobado por** | Gerencia General |
| **Clasificación** | Uso interno |
| **Próxima revisión** | [Fecha, máx. 1 año] |

### 1. Objetivo
Establecer el método único y repetible para identificar, analizar y evaluar los riesgos de seguridad de la información del Banco, permitiendo compararlos, priorizarlos y decidir su tratamiento con criterios objetivos.
### 2. Alcance
Aplica a todos los activos del inventario (ID-01) dentro del alcance del SGSI, a los procesos críticos y a los servicios de terceros. Incluye los riesgos sobre datos personales de los clientes.
### 3. Escalas de evaluación
**Escala de probabilidad (qué tan posible es que ocurra):**
| **Nivel** | **Valor** | **Descripción** |
|---|---|---|
| Muy baja | 1 | Extremadamente improbable; no se conoce caso en el sector |
| Baja | 2 | Poco probable; se requiere una combinación de fallas |
| Media | 3 | Posible; existen antecedentes o condiciones favorables |
| Alta | 4 | Probable; las condiciones actuales lo facilitan |
| Muy alta | 5 | Casi seguro; ya ocurrió o las condiciones son evidentes |

**Escala de impacto (qué tan grave es si ocurre):**
| **Nivel** | **Valor** | **Impacto financiero** | **Indisponibilidad** | **Impacto reputacional/regulatorio** |
|---|---|---|---|---|
| Insignificante | 1 | Menor a [COMPLETAR: USD 5.000] | Hasta 1 hora | Sin repercusión relevante |
| Menor | 2 | [COMPLETAR: USD 5.000 a 50.000] | Hasta 4 horas | Queja aislada; nota interna del supervisor |
| Moderado | 3 | [COMPLETAR: USD 50.000 a 500.000] | Hasta 12 horas | Reclamos de clientes; requerimiento BCU/URCDP |
| Mayor | 4 | [COMPLETAR: USD 500.000 a 2.000.000] | Hasta 24 horas | Cobertura de prensa; sanción o plan de acción del supervisor |
| Catastrófico | 5 | Más de [COMPLETAR: USD 2.000.000] | Más de 24 horas | Pérdida de confianza; sanción grave o intervención |

### 4. Matriz de riesgo (matriz de calor 5×5)
Riesgo = Probabilidad × Impacto. La celda determina el nivel: verde = bajo, amarillo = medio, naranja = alto, rojo = crítico.
| **Probabilidad \ Impacto** | **1 Insignificante** | **2 Menor** | **3 Moderado** | **4 Mayor** | **5 Catastrófico** |
|---|---|---|---|---|---|
| **5 Muy alta** | 5 (Medio) | 10 (Alto) | 15 (Alto) | 20 (Crítico) | 25 (Crítico) |
| **4 Alta** | 4 (Medio) | 8 (Alto) | 12 (Alto) | 16 (Crítico) | 20 (Crítico) |
| **3 Media** | 3 (Bajo) | 6 (Medio) | 9 (Alto) | 12 (Alto) | 15 (Crítico) |
| **2 Baja** | 2 (Bajo) | 4 (Medio) | 6 (Medio) | 8 (Alto) | 10 (Alto) |
| **1 Muy baja** | 1 (Bajo) | 2 (Bajo) | 3 (Bajo) | 4 (Medio) | 5 (Medio) |

**Interpretación:** los riesgos en zonas **roja** (≥ 15) y **naranja** (≥ 8) requieren tratamiento prioritario (ID-04). Los **verdes** (≤ 4) pueden aceptarse documentadamente si están dentro del apetito.
### 5. Apetito y criterios de aceptación de riesgo
- **Apetito de riesgo del Banco:** [COMPLETAR: ej. no aceptar riesgos críticos en activos que soportan pagos o datos personales; nivel máximo aceptable sin tratamiento: medio (amarillo)].
- **Criterio de aceptación:** un riesgo puede aceptarse solo si el propietario del activo lo firma, el RSI lo evalúa y queda registrado con fecha de revisión. Los riesgos que afecten el sistema de pagos o datos personales sensibles **nunca** se aceptan en nivel alto o superior.
### 6. Roles en el proceso de gestión de riesgos
| **Rol** | **Responsabilidad** |
|---|---|
| **Propietario del activo** | Identifica riesgos de su activo, aporta datos y firma el tratamiento |
| **RSI** | Coordina la evaluación, consolida el registro de riesgos y controla el plan |
| **Área de Riesgos (RNF)** | Valida la calibración, los criterios y el alineamiento con el riesgo operacional |
| **División TI** | Aporta la información técnica de amenazas y vulnerabilidades |
| **Comité de Seguridad** | Decide el tratamiento de los riesgos altos y críticos |
| **Gerencia General / Directorio** | Aprueba el apetito de riesgo y el plan de tratamiento |

### 7. Frecuencia de re-evaluación
El análisis se re-ejecuta [COMPLETAR: anualmente, y de forma extraordinaria ante: incorporación de un sistema mayor, cambio en el perfil de riesgo, incidente relevante, nuevo requerimiento normativo o auditoría].
### 8. Control de cambios
| **Versión** | **Fecha** | **Cambio** | **Elaboró** | **Aprobó** |
|---|---|---|---|---|
| 0.1 | [COMPLETAR] | Versión inicial | RSI | — |
| 1.0 | [COMPLETAR] | Aprobación de la metodología | RSI | Gerencia General |

## 5. Ejemplo aplicado al Banco (modelo de referencia)
Ejemplo de cómo quedaría calibrado el impacto para el Banco (adaptá los montos y horarios a la realidad del banco).
**Impacto financiero (ejemplo):** 1: menor a USD 5.000 · 2: hasta USD 50.000 · 3: hasta USD 500.000 · 4: hasta USD 2.000.000 · 5: más de USD 2.000.000 (incluye multas, gastos de respuesta y pérdida de operación).
**Indisponibilidad (ejemplo, alineada al perfil Avanzado del MCU 5.0):** el Banco tolera como máximo 24 horas de indisponibilidad de servicios críticos. Por eso una caída de más de 24 horas del core se califica de impacto 5, y de hasta 12 horas, impacto 3.
**Apetito (ejemplo):** el Comité declara apetito "moderado" para sistemas internos, y apetito "bajo" (no aceptar niveles alto/crítico) para todo lo que toque el sistema de pagos, el ahorro de los clientes y los datos personales. Todo riesgo crítico se reporta al Directorio en el informe semestral del RSI (GV-06).
**Uso de la matriz (ejemplo):** un riesgo con probabilidad 3 (media) e impacto 4 (mayor) da 12 → **Alto** → entra en el plan de tratamiento (ID-04) con responsable y plazo. Un riesgo con probabilidad 1 e impacto 3 da 3 → **Bajo** → puede aceptarse por el propietario del activo.

**Documentos relacionados:** ID-01 (Inventario de activos) · ID-03 (Análisis de riesgos) · ID-04 (Plan de tratamiento) · BCU-02 (Marco de gestión de riesgos) · URCDP-05 (EIPD) · GV-06 (Informe del RSI).
