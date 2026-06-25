# Clase 41: Presentacion de Proyectos - Parte 1

**Numero de clase:** 31  
**Duracion:** 2 horas  
**Curso:** Taller de Ciberseguridad Orientada al Desarrollo

---

## Objetivos de Aprendizaje

- Presentar y defender proyectos de seguridad ante la clase
- Evaluar proyectos utilizando una rubrica formal
- Proporcionar y recibir feedback constructivo
- Demostrar comprension de conceptos de DevSecOps

---

## Contenido Detallado

### 1. Estructura de la Sesion (15 min)

**Organizacion del tiempo (2 horas):**
- 10 min: Introduccion y recordatorio de criterios
- 5 min por presentacion (x 10 grupos = 50 min)
- 3 min de preguntas por presentacion (x 10 = 30 min)
- 15 min: Feedback general y cierre

**Material necesario:**
- Proyector o pantalla compartida
- Rubrica de evaluacion impresa o digital para cada estudiante
- Cronometro visible para todos
- Acceso al repositorio de cada grupo

### 2. Criterios de Evaluacion - Proyecto Shift Left (5 min)

| Criterio | Peso | Excelente (4) | Bueno (3) | Suficiente (2) | Insuficiente (1) |
|----------|------|---------------|-----------|----------------|-------------------|
| Codigo seguro | 25% | Sin vulnerabilidades, mejores practicas | Vulnerabilidades menores | Vulnerabilidades moderadas | Vulnerabilidades criticas |
| Pipeline CI/CD | 25% | Pipeline completo con SAST, SCA, gates | Pipeline con SAST o SCA | Pipeline basico sin seguridad | Sin pipeline |
| Documentacion | 15% | Completa, clara, con instrucciones | Adecuada | Incompleta | Ausente |
| Defensas implementadas | 20% | Validacion, JWT, RBAC, rate limiting | 3 de 4 defensas | 2 de 4 defensas | 1 o menos defensas |
| Presentacion | 15% | Clara, demostracion en vivo, responde preguntas | Buena exposicion | Presentacion basica | Sin preparacion |

### 3. Rubrica de Evaluacion Detallada (10 min)

**Rubrica para evaluacion por pares:**

```
RUBRICA DE EVALUACION - PROYECTO SHIFT LEFT
============================================

Grupo evaluado: _______________
Evaluador: ____________________

1. CODIGO SEGURO (25 puntos)
   - Uso de consultas parametrizadas (0-5): ___
   - Validacion de entrada (0-5): ___
   - Manejo seguro de contrasenas (0-5): ___
   - Control de acceso/autorizacion (0-5): ___
   - Logging seguro (0-5): ___
   Total: ___/25

2. PIPELINE CI/CD (25 puntos)
   - Pipeline implementado y funcional (0-7): ___
   - SAST integrado (Bandit, Semgrep, etc.) (0-6): ___
   - SCA integrado (pip-audit, npm audit, etc.) (0-6): ___
   - Quality gates con fail criteria (0-6): ___
   Total: ___/25

3. DOCUMENTACION (15 puntos)
   - README con instrucciones claras (0-5): ___
   - Archivo .env.example y configuracion (0-5): ___
   - Explicacion de decisiones de seguridad (0-5): ___
   Total: ___/15

4. DEFENSAS IMPLEMENTADAS (20 puntos)
   - Autenticacion JWT (0-5): ___
   - Hashing de contrasenas (0-5): ___
   - Rate limiting (0-5): ___
   - Security headers (0-5): ___
   Total: ___/20

5. PRESENTACION (15 puntos)
   - Claridad y organizacion (0-5): ___
   - Demostracion en vivo (0-5): ___
   - Respuesta a preguntas (0-5): ___
   Total: ___/15

PUNTAJE TOTAL: ___/100

COMENTARIOS:
_________________________________________
_________________________________________
```

### 4. Guia para la Presentacion (10 min)

**Estructura recomendada (5 min):**

1. **Introduccion (30 seg):** Nombre del proyecto, integrantes, tecnologias utilizadas
2. **Demo de la app (1 min):** Mostrar que la aplicacion funciona
3. **Defensas de seguridad (1.5 min):** Mostrar implementacion de JWT, validacion, RBAC
4. **Pipeline CI/CD (1 min):** Mostrar el workflow de GitHub Actions funcionando
5. **Lecciones aprendidas (30 seg):** Que aprendieron, que harian diferente
6. **Preguntas (restante):** Responder preguntas del profesor y companeros

**Consejos para la presentacion:**
- Tener la demo preparada y funcionando localmente
- Tener el pipeline ya ejecutado (o ejecutar un commit en vivo)
- Mostrar tanto los casos de exito como los fallos del pipeline
- Si algo falla en vivo, explicar que esperaban y por que fallo
- Responder honestamente si no saben algo

### 5. Preguntas Tecnicas para la Ronda (10 min)

Banco de preguntas que el profesor puede hacer:

1. "Por que eligieron esa herramienta SAST y no otra?"
2. "Como manejarian un falso positivo de Bandit en el pipeline?"
3. "Que pasaria si un atacante obtiene el JWT de un usuario?"
4. "Como escalarian esta solucion a microservicios?"
5. "Que mejoras de seguridad agregarian si tuvieran mas tiempo?"
6. "Como protegen las claves de API en el pipeline de CI/CD?"
7. "Que pasaria si la base de datos se compromete? Las contrasenas estan seguras?"
8. "Como implementarian logging sin exponer datos personales?"
9. "Que ocurre si el rate limiter falla? Como se recupera?"
10. "Como verificarian que el contenedor desplegado es el mismo que se construyo?"

### 6. Feedback Constructivo (10 min)

**Metodo de feedback: "2 estrellas y 1 deseo"**
- 2 aspectos positivos (estrellas)
- 1 area de mejora con sugerencia concreta (deseo)

**Ejemplos de feedback constructivo:**

Positivo:
- "Me gusto que implementaron rate limiting con Redis en vez de memoria"
- "La documentacion del pipeline es clara y facil de seguir"
- "Buena decision usar multi-stage build para reducir tamano de imagen"

Constructivo:
- "Podrian mejorar la validacion de entrada agregando expresiones regulares mas estrictas"
- "Sugiero agregar un healthcheck al contenedor de la BD"
- "El .env no deberia estar en el repositorio aunque sea de ejemplo sin valores reales"

---

## Ejercicio: Evaluar usando la Rubrica

**Enunciado:** Los grupos que no estan presentando deben evaluar a sus companeros usando la rubrica proporcionada. Cada estudiante evalua al menos 2 presentaciones y entrega las rubricas completadas al final de la clase.

**Solucion - Rubrica de ejemplo completada:**

```
RUBRICA DE EVALUACION - EJEMPLO COMPLETADO
============================================

Grupo evaluado: Los DevSecOps
Evaluador: Estudiante X

1. CODIGO SEGURO (25 puntos)
   - Uso de consultas parametrizadas (0-5): 5
   - Validacion de entrada (0-5): 5
   - Manejo seguro de contrasenas (0-5): 4
   - Control de acceso/autorizacion (0-5): 4
   - Logging seguro (0-5): 3
   Total: 21/25

2. PIPELINE CI/CD (25 puntos)
   - Pipeline implementado y funcional (0-7): 7
   - SAST integrado (0-6): 6
   - SCA integrado (0-6): 6
   - Quality gates con fail criteria (0-6): 5
   Total: 24/25

3. DOCUMENTACION (15 puntos)
   - README con instrucciones claras (0-5): 5
   - Archivo .env.example y configuracion (0-5): 4
   - Explicacion de decisiones de seguridad (0-5): 4
   Total: 13/15

4. DEFENSAS IMPLEMENTADAS (20 puntos)
   - Autenticacion JWT (0-5): 5
   - Hashing de contrasenas (0-5): 5
   - Rate limiting (0-5): 4
   - Security headers (0-5): 4
   Total: 18/20

5. PRESENTACION (15 puntos)
   - Claridad y organizacion (0-5): 4
   - Demostracion en vivo (0-5): 5
   - Respuesta a preguntas (0-5): 4
   Total: 13/15

PUNTAJE TOTAL: 89/100

COMENTARIOS:
Excelente trabajo en el pipeline CI/CD con Bandit y pip-audit. La
demostracion en vivo fue clara y mostraron tanto exito como fallo.
Sugerencia: agregar logging seguro usando la libreria 'structlog'
para evitar exponer datos sensibles en los logs.
```

---

## Preguntas y Respuestas

**1. Que peso tiene cada criterio en la evaluacion del proyecto?**

Codigo seguro (25%), Pipeline CI/CD (25%), Defensas implementadas (20%), Documentacion (15%), Presentacion (15%).

**2. Que debe incluir la documentacion del proyecto?**

README con instrucciones de instalacion y ejecucion, archivo .env.example, explicacion de las decisiones de seguridad tomadas, y ejemplo de uso de los endpoints.

**3. Como se evalua el pipeline CI/CD?**

Se evalua que este implementado y funcional (7 pts), que incluya SAST (6 pts), SCA (6 pts), y quality gates con criterios de fallo (6 pts).

**4. Que tipo de preguntas tecnicas se esperan en la ronda?**

Preguntas sobre justificacion de herramientas, manejo de falsos positivos, escalabilidad, proteccion de secretos, logging seguro, y recuperacion ante fallos.

**5. Cual es el formato de feedback recomendado?**

"2 estrellas y 1 deseo": dos aspectos positivos y un area de mejora con sugerencia concreta. Esto asegura feedback balanceado y constructivo.

**6. Que ocurre si un grupo no tiene el pipeline funcionando en la presentacion?**

Se evalua sobre lo que se presenta. Si el pipeline no funciona, la puntuacion en ese criterio sera baja o cero. Se recomienda tener una grabacion o capturas de pantalla como respaldo.

**7. Como se maneja el tiempo de presentacion?**

Cada grupo tiene exactamente 5 minutos mas 3 de preguntas. Se usa un cronometro visible. A los 4 minutos se avisa. A los 5 minutos se corta y se pasa a preguntas.

---

## Tarea / Lectura Recomendada

- Completar las rubricas de evaluacion de los grupos que presentaron
- Preparar la presentacion del ataque Red Team para la clase 32 (grupos que presentan en la segunda sesion)
- Leer: Recursos de OWASP para seguir aprendiendo despues del curso
- Reflexionar: Que aprendiste en el curso? Que aplicaras en tu trabajo diario?


