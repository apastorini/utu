# Plantilla: Documento de Presentación de Vulnerabilidad OWASP

```
================================================================================
                    INFORME DE VULNERABILIDAD OWASP
================================================================================

================================================================================
SECCIÓN 1: INFORMACIÓN GENERAL
================================================================================

Título de la Vulnerabilidad:
OWASP Code: [A01-A10]
Severidad: [Crítica|Alta|media|Baja]
CVSS Score: [0.0-10.0]
Fecha de Descubrimiento: [DD/MM/AAAA]
Fecha de Reporte: [DD/MM/AAAA]
Investigador: [Nombre del grupo]

================================================================================
SECCIÓN 2: DESCRIPCIÓN TÉCNICA
================================================================================

2.1 Descripción de la Vulnerabilidad
----------------------------------------
[Descripción clara y técnica de qué es la vulnerabilidad]

2.2 Variantes Cubiertas
----------------------------------------
- Variante 1: [Nombre y descripción]
- Variante 2: [Nombre y descripción]
- [Agregar más variantes según corresponda]

2.3 CWE Relacionados
----------------------------------------
- CWE-XXX: [Nombre]
- CWE-XXX: [Nombre]

2.4 Impacto de Negocio
----------------------------------------
[Impacto potencial en el negocio si es explotada]

================================================================================
SECCIÓN 3: ANÁLISIS TÉCNICO
================================================================================

3.1 Código Vulnerable (Ejemplo)
----------------------------------------
```
[Lenguaje de programación]
# Código vulnerable aquí
# Marcar líneas vulnerables con comentarios
```

3.2 Análisis del Ataque
----------------------------------------
[Paso a paso cómo explotar la vulnerabilidad]

3.3 Variantes de Ataque
----------------------------------------
3.3.1 Variante 1
   [Descripción y ejemplo de payloads]

3.3.2 Variante 2
   [Descripción y ejemplo de payloads]

================================================================================
SECCIÓN 4: DEMOSTRACIÓN PRÁCTICA (LAB)
================================================================================

4.1 Entorno de Prueba
----------------------------------------
Herramientas utilizadas:
- [Herramienta 1]: [Versión] - [Propósito]
- [Herramienta 2]: [Versión] - [Propósito]

Entorno: [DVWA|Juice Shop|WebGoat|Propio]

4.2 Pasos de Reproducción
----------------------------------------
Paso 1: [Descripción]
Paso 2: [Descripción]
[Continuar con todos los pasos]

4.3 Evidencia de Explotación
----------------------------------------
[Capturas de pantalla, logs, output de herramientas]

4.4 Output/Resultado
----------------------------------------
```
[Output de la herramienta o resultado observado]
```

================================================================================
SECCIÓN 5: DETECCIÓN
================================================================================

5.1 Cómo Detectar la Vulnerabilidad
----------------------------------------
[Métodos manuales y automáticos]

5.2 Herramientas de Detección
----------------------------------------
| Herramienta | Tipo | Comando/Uso |
|-------------|------|-------------|
| [Nombre] | [Automático/Manual] | [Comando] |

5.3 Signos de Compromiso (IOCs)
----------------------------------------
[Indicadores de que la vulnerabilidad fue explotada]

================================================================================
SECCIÓN 6: MEDIDAS DE PROTECCIÓN
================================================================================

6.1 Controles de Prevención
----------------------------------------
[Cómo evitar que la vulnerabilidad exista]

6.2 Código Seguro (Ejemplo)
----------------------------------------
```
[Lenguaje de programación]
# Código seguro con mitigaciones
# Explicar cada control implementado
```

6.3 Controles de Detección
----------------------------------------
[Cómo detectar si está siendo explotada]

6.4 Controles de Corrección
----------------------------------------
[Pasos para remediar si ya está presente]

================================================================================
SECCIÓN 7: RECURSOS ADICIONALES
================================================================================

7.1 Referencias
----------------------------------------
- OWASP: [URL]
- CWE: [URL]
- CVE relacionado: [URL si aplica]
- Documentación oficial: [URL]

7.2 Herramientas Relacionadas
----------------------------------------
[Lista de herramientas adicionales para estudio]

7.3 Lecturas Recomendadas
----------------------------------------
[Artículos, papers, libros]

================================================================================
SECCIÓN 8: CHECKLIST DE VERIFICACIÓN
================================================================================

[ ] Código usa prepared statements / parameterized queries
[ ] Validación de entrada en servidor
[ ] Principio de mínimo privilegio aplicado
[ ] Headers de seguridad configurados
[ ] Logging de intentos sospechosos
[ ] [Agregar más items específicos]

================================================================================
ANEXO: PRESENTACIÓN
================================================================================

8.1 Slides Outline
----------------------------------------
- Slide 1: Título y objetivos (2 min)
- Slide 2: ¿Qué es esta vulnerabilidad? (5 min)
- Slide 3: Variantes identificadas (8 min)
- Slide 4: Demo práctica - Detección (7 min)
- Slide 5: Demo práctica - Explotación (8 min)
- Slide 6: Cómo protegerse (8 min)
- Slide 7: Q&A (2 min)

8.2 Tiempo Total: 40 minutos

================================================================================
                                 FIN DEL DOCUMENTO
================================================================================
```

---

## Ejemplo Completado (Fragmento)

```
================================================================================
                    INFORME DE VULNERABILIDAD OWASP
================================================================================

================================================================================
SECCIÓN 1: INFORMACIÓN GENERAL
================================================================================

Título de la Vulnerabilidad: Broken Access Control - IDOR
OWASP Code: A01-2021
Severidad: Alta
CVSS Score: 7.5
Fecha de Descubrimiento: 13/03/2026
Fecha de Reporte: 13/03/2026
Investigador: Grupo 1 - Seguridad App

================================================================================
SECCIÓN 2: DESCRIPCIÓN TÉCNICA
================================================================================

2.1 Descripción de la Vulnerabilidad
----------------------------------------
Insecure Direct Object Reference (IDOR) ocurre cuando una aplicación expõe 
referencias directas a objetos internos (IDs deBase de datos, nombres de 
archivos) sin verificar la autorización del usuario. Un atacante puede 
manipular estas referencias para acceder a datos de otros usuarios.

2.2 Variantes Cubiertas
----------------------------------------
- IDOR Horizontal: Acceder a recursos del mismo nivel de privilegio
- IDOR Vertical: Acceder a recursos de mayor privilegio
- Path Traversal: Manipulación de rutas de archivos
- Parameter Manipulation: Modificación de parámetros de solicitud
```

---

## Plantilla de Slides (40 min)

| Slide | Contenido | Tiempo |
|-------|-----------|--------|
| 1 | Título,OWASP Code, Integrantes | 2 min |
| 2 | ¿Qué es? - Definición y contexto | 3 min |
| 3-4 | Variantes técnicas | 8 min |
| 5-6 | Demo: Cómo detectar (herramientas) | 7 min |
| 7-9 | Demo: Cómo explotar (payloads) | 10 min |
| 10-12 | Mitigaciones y código seguro | 8 min |
| 13 | Checklist y recursos | 1 min |
| 14 | Q&A | 1 min |