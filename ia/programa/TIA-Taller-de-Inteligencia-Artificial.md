# Programa de
# Taller de Inteligencia Artificial (TIA)

---

## 1. NOMBRE DE LA UNIDAD CURRICULAR

Taller de Inteligencia Artificial (TIA)

---

## 2. CRÉDITOS

8 créditos

---

## 3. OBJETIVOS DE LA UNIDAD CURRICULAR

- Construir infraestructuras industriales de agentes inteligentes con persistencia de memoria a largo plazo, capaces de mantener estado y contexto a través de múltiples sesiones de interacción.
- Desplegar sistemas multi-agente escalables mediante plataformas de contenerización y orquestación de contenedores, aplicando patrones de arquitecturas distribuidas.
- Optimizar modelos de lenguaje de tamaño reducido (SLMs) mediante técnicas de ajuste fino para tareas empresariales específicas, comprendiendo los principios de eficiencia computacional.
- Implementar sistemas de observabilidad (Agent-Ops) que permitan el trazado de decisiones, la detección de anomalías y la aplicación de mecanismos de control (kill-switches semánticos) en sistemas autónomos.
- Diseñar arquitecturas de escalamiento horizontal para enjambres de agentes, integrando patrones de tolerancia a fallos, balanceo de carga y recuperación ante desastres.

---

## 4. METODOLOGÍA DE ENSEÑANZA

**Participación de los Estudiantes:**

- **Demostraciones Prácticas:** El instructor realizará demostraciones en el laboratorio de despliegue de sistemas multi-agente, estrategias de persistencia de estado, configuración de observabilidad y técnicas de ajuste fino de modelos, durante las horas de clase.
- **Presentaciones Técnicas (Parcial 1):** Los estudiantes realizarán presentaciones técnicas grupales de 25 minutos sobre una arquitectura de orquestación de agentes persistentes, incluyendo diagramas de flujo, estrategias de memoria y planes de contingencia.
- **Proyecto Final (Evaluación Final):** Defensa de una infraestructura "organización autónoma" completa, desplegable y escalable, que integre agentes con sistemas externos, con monitoreo, mecanismos de control y documentación completa de la arquitectura.

---

## 5. TEMARIO

| Semanas | Unidad | Contenidos |
|---|---|---|
| 1-4 | **Workflows Agénticos Industriales** | Arquitecturas de agentes industriales. Diferencias con sistemas conversacionales. Gestión de estados y transiciones. Persistencia de estado. Patrones de diseño para agentes con memoria. |
| 5-8 | **Integración con Sistemas Externos** | Conexión con sistemas empresariales (ERP, CRM). Patrones de adaptación y capas de abstracción. Mensajería asíncrona y colas. Patrones de transacciones distribuidas (Saga). |
| 9-12 | **Agent-Ops y Observabilidad** | Trazado de decisiones y pensamientos. Métricas y monitoreo de agentes. Mecanismos de control y seguridad (circuit breakers, kill-switches). Alertas y procedimientos de respuesta. |
| 13-16 | **Escalamiento y Optimización** | Contenerización de agentes. Orquestación de contenedores y auto-escalado. Modelos de lenguaje pequeños (SLMs): selección, ajuste fino y despliegue. Infraestructura como código. |

---

## 6. BIBLIOGRAFÍA

### 6.1 Básica

- Sutton, R., Barto, A. (2018). *Reinforcement Learning: An Introduction*. 2nd Edition. MIT Press.
- Wooldridge, M. (2009). *An Introduction to MultiAgent Systems*. 2nd Edition. Wiley.

### 6.2 Complementaria

- Hu, E. et al. (2021). "LoRA: Low-Rank Adaptation of Large Language Models". Disponible en: https://arxiv.org/abs/2106.09685
- Microsoft. *Azure Well-Architected Framework*. Disponible en: https://learn.microsoft.com/es-es/azure/well-architected/
- Microsoft Learn. *Formación para ingenieros de IA*. Disponible en: https://learn.microsoft.com/es-es/training/career-paths/ai-engineer
- OWASP Foundation. (Última versión). *OWASP Top 10 for LLM Applications*. Disponible en: https://owasp.org/www-project-top-10-for-llm-applications/
- Burns, T. et al. (2024). "The Shift from Models to Compound AI Systems". Disponible en: https://bair.berkeley.edu/blog/2024/02/18/compound-ai-systems/

---

## 7. CONOCIMIENTOS PREVIOS EXIGIDOS Y RECOMENDADOS

### 7.1 Conocimientos Previos Exigidos

Se requieren conocimientos de Introducción a la IA para Desarrolladores (o equivalente), programación avanzada y sistemas operativos.

### 7.2 Conocimientos Previos Recomendados

Conocimientos básicos de bases de datos, redes de computadoras y arquitecturas distribuidas.

No incluye la información de previaturas. Las unidades curriculares previas serán definidas por cada carrera que tome la unidad curricular y serán incluidas en el anexo B.

---

## ANEXO A

### Para todas las Carreras

Esta primera parte del anexo incluye aspectos complementarios que son generales de la unidad curricular.

---

### A1) INSTITUTO

Comisión Nacional de Carrera del Tecnólogo en Informática (UTU-UTEC-UDELAR)

---

### A2) CRONOGRAMA TENTATIVO

| Semana | Actividad |
|---|---|
| 1 | Arquitecturas de agentes industriales. Estados y transiciones |
| 2 | Persistencia de estado. Almacenes en memoria |
| 3 | Gestión de memoria: semántica, episódica, procedural |
| 4 | Tolerancia a fallos y máquinas de estado |
| 5 | Integración con sistemas empresariales (ERP/CRM) |
| 6 | Patrones de adaptación y capas de abstracción |
| 7 | Mensajería asíncrona. Patrón Saga |
| 8 | **Parcial 1** - Presentaciones técnicas |
| 9 | Trazado de decisiones. Observabilidad |
| 10 | Métricas y monitoreo de agentes |
| 11 | Circuit breakers y kill-switches semánticos |
| 12 | Alertas y procedimientos de respuesta |
| 13 | Contenerización de agentes |
| 14 | Orquestación y auto-escalado |
| 15 | **Evaluación Final** - Proyecto integrador |
| 16 | Cierre, tendencias y lecciones aprendidas |

---

### A3) MODALIDAD DEL CURSO Y PROCEDIMIENTO DE EVALUACIÓN

**Aprobación del Curso:** Obtener un promedio ponderado mínimo de 60% en el total de las instancias de evaluación. La presentación técnica grupal es obligatoria para aprobar el curso.

| Instancia | Descripción | Peso |
|---|---|---|
| Parcial 1 (Semana 8) | Presentación técnica grupal (25 min) de una arquitectura de orquestación de agentes persistentes | 40% |
| Evaluación Final (Semana 15) | Defensa de una infraestructura "organización autónoma" desplegable y escalable | 40% |
| Participación | Asistencia y entrega de trabajos prácticos de laboratorio | 20% |

### A4) CALIDAD DE LIBRE

Esta asignatura no adhiere a la resolución del consejo sobre la condición de libre.

### A5) CUPOS DE LA UNIDAD CURRICULAR

No tiene cupo

---

## ANEXO B

### Para la carrera Tecnólogo en Informática

---

### B1) ÁREA DE FORMACIÓN

Sistemas Inteligentes Avanzados

### B2) UNIDADES CURRICULARES PREVIAS

Introducción a la IA para Desarrolladores (Curso Aprobado).
Sistemas Operativos (Curso Aprobado).
