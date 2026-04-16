# Clase: DREAD - Metodología de Evaluación de Riesgos de Seguridad

## Introducción

DREAD es un modelo de evaluación de riesgos de seguridad desarrollado por Microsoft que proporciona un marco sistemático para calificar y priorizar vulnerabilidades y amenazas. El acrónimo representa las cinco dimensiones que se evalúan: Damage (Daño), Reproducibility (Reproducibilidad), Exploitability (Explotabilidad), Affected Users (Usuarios afectados) y Discoverability (Detectabilidad).

**Objetivos de aprendizaje:**
1. Comprender el modelo DREAD y sus dimensiones
2. Aplicar DREAD para calificar vulnerabilidades
3. Comparar DREAD con otras metodologías (CVSS, STRIDE)
4. Utilizar DREAD en el contexto de gestión de vulnerabilidades
5. Integrar DREAD con otras metodologías de seguridad

---

## 1. Fundamentos de DREAD

### 1.1 Origen y propósito

DREAD fue desarrollado por Microsoft en la década de 2000 como parte de su proceso de desarrollo de software seguro. Aunque Microsoft ha descontinuado su uso oficial en favor de modelos más estandarizados como CVSS, DREAD sigue siendo una herramienta valiosa por su simplicidad y aplicabilidad práctica en muchos contextos.

### 1.2 El acrónimo

| Letra | Dimensión | Descripción | Pregunta clave |
|-------|-----------|-------------|---------------|
| **D** | Damage | ¿Cuánto daño puede causar? | ¿Qué tan grave es el impacto? |
| **R** | Reproducibility | ¿Qué tan reproducible es? | ¿Qué tan consistente es el ataque? |
| **E** | Exploitability | ¿Qué tan fácil de explotar? | ¿Qué se necesita para explotarlo? |
| **A** | Affected Users | ¿Cuántos usuarios se ven afectados? | ¿Qué proporción de usuarios impacta? |
| **D** | Discoverability | ¿Qué tan fácil de descubrir? | ¿Qué tan fácil es encontrar la vulnerabilidad? |

### 1.3 Relación con otras metodologías

```
┌─────────────────────────────────────────────────────────────┐
│          COMPLEMENTARIEDAD DE MARCOS DE AMENAZAS            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   ┌─────────────┐                                          │
│   │   STRIDE    │── Identifica QUÉ amenazas existen        │
│   │  (Modelo)   │                                         │
│   └──────┬──────┘                                          │
│          │                                                  │
│          ▼                                                  │
│   ┌─────────────┐                                          │
│   │ Identified  │── Lista de amenazas/vulnerabilidades      │
│   │  Threat     │                                         │
│   └──────┬──────┘                                          │
│          │                                                  │
│          ▼                                                  │
│   ┌─────────────┐                                          │
│   │   DREAD     │── Califica CADA amenaza (priorización)  │
│   │  (Rating)   │                                         │
│   └──────┬──────┘                                          │
│          │                                                  │
│          ▼                                                  │
│   ┌─────────────┐                                          │
│   │ Risk Matrix │── Priorización de mitigaciones            │
│   │             │                                         │
│   └─────────────┘                                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Escalas de Calificación DREAD

### 2.1 Escala de Damage (Daño potencial)

| Score | Nivel | Descripción | Ejemplos |
|-------|-------|-------------|----------|
| 10 | Crítico | Destrucción completa del sistema | RCE con domain admin, data destruction |
| 9 | Muy alto | Toda la base de datos comprometida | SQL injectionfull data breach |
| 7 | Alto | Pérdida significativa de datos | Acceso a transacciones financieras |
| 6 | Medio | Pérdida parcial de funcionalidad | Modify de algunos datos |
| 4 | Bajo | Pérdida mínima | Acceso a información de bajo valor |
| 3 | Muy bajo | Sin impacto técnico significativo | Información trivial expuesta |
| 0 | Ninguno | Sin impacto |什么都没有发生 |

### 2.2 Escala de Reproducibility (Reproducibilidad)

| Score | Nivel | Descripción | Condiciones |
|-------|-------|-------------|-------------|
| 10 | Perfecta | Siempre reproducible | Sin condiciones especiales |
| 9 | Muy alta | Generalmente reproducible | Condiciones comunes |
| 7 | Alta | Reproducible la mayoría de veces | Condiciones específicas |
| 5 | Media | Inconsistente | Depende de timing o configuración |
| 3 | Baja | Difícil de reproducir | Solo bajo condiciones específicas |
| 1 | Muy baja | Teórica | Requiere condiciones casi imposibles |
| 0 | N/A | No aplicable | No reproducible |

### 2.3 Escala de Exploitability (Explotabilidad)

| Score | Nivel | Descripción | Requisitos |
|-------|-------|-------------|-----------|
| 10 | Alta | Herramienta disponible, trivial | Solo conocimiento básico |
| 9 | Muy alta | Código de exploit público | Herramienta fácilmente disponible |
| 7 | Alta | Código de exploit requiere adaptación | Conocimiento moderado necesario |
| 5 | Media | Explotación requiere habilidades | Experto necesita adaptar |
| 3 | Baja | Exploración teórica difícil | Habilidades avanzadas necesarias |
| 1 | Muy baja | No práctico explotarlo | Requiere investigación extensa |
| 0 | N/A | No explotable | No hay vector de ataque |

### 2.4 Escala de Affected Users (Usuarios afectados)

| Score | Nivel | Descripción | Porcentaje |
|-------|-------|-------------|-----------|
| 10 | Todos | Todos los usuarios afectados | 100% |
| 9 | Muchos | Significativo porcentaje | > 50% |
| 7 | Algunos | Grupo específico pero grande | > 25% |
| 5 | Pocos | Grupo pequeño específico | > 10% |
| 3 | Muy pocos | Usuarios individuales | < 10% |
| 1 | Ninguno | No afecta usuarios | 0% |
| 0 | N/A | No aplicable | N/A |

### 2.5 Escala de Discoverability (Detectabilidad)

| Score | Nivel | Descripción | Acceso |
|-------|-------|-------------|-------|
| 10 | Muy fácil | Visible en documentation/público | Todos pueden encontrarlo |
| 9 | Fácil | Fácil de descubrir | Con acceso básico |
| 7 | Moderada | Puede ser descubierto por usuarios avanzados | Con técnicas simples |
| 5 | Difícil | Descubrimiento difícil | Requiere investigación |
| 3 | Muy difícil | Descubrimiento muy improbable | Solo con código fuente |
| 1 | Casi imposible | Teórica | Requiere acceso privilegiado |
| 0 | N/A | No descubrible | No hay evidencia de exploit |

---

## 3. Cálculo del Score DREAD

### 3.1 Fórmula

```
DREAD Score = (Damage + Reproducibility + Exploitability + Affected Users + Discoverability) / 5
```

**Rango posible:** 0 a 10

### 3.2 Clasificación de severidad

| Rango | Nivel | Color | Acciones |
|-------|-------|-------|----------|
| 9.0 - 10.0 | Crítico | Rojo | Remediation inmediata |
| 7.0 - 8.9 | Alto | Naranja | Remediation urgente |
| 5.0 - 6.9 | Medio | Amarillo | Remediation en siguiente sprint |
| 3.0 - 4.9 | Bajo | Verde claro | Remediation programada |
| 0.0 - 2.9 | Informativo | Verde | Documentar, monitorear |

### 3.3 Ejemplo de cálculo

**Vulnerabilidad: SQL Injection en login**

| Dimensión | Score | Justificación |
|-----------|-------|---------------|
| Damage | 9 | Acceso potencial a toda la base de datos |
| Reproducibility | 9 | Siempre reproducible con payloads estándar |
| Exploitability | 8 | Herramientas automáticas disponibles |
| Affected Users | 7 | Todos los usuarios que usan el login |
| Discoverability | 6 | Requiere conocimiento de pentesting |
| **Total** | **7.8** | **ALTO - Remediation urgente** |

---

## 4. Aplicación Práctica de DREAD

### 4.1 Caso: Evaluación de vulnerabilidades en portal bancario

**Vulnerabilidad 1: Stored XSS en campo nombre**

| Dimensión | Score | Justificación |
|-----------|-------|---------------|
| Damage | 7 | Robo de cookies, session hijacking |
| Reproducibility | 10 | Siempre se ejecuta para todos los usuarios |
| Exploitability | 7 | Requiere conocimiento de XSS |
| Affected Users | 8 | Todos los usuarios que ven el perfil |
| Discoverability | 7 | Encontrable con scanners estándar |
| **Total** | **7.8** | **ALTO** |

**Vulnerabilidad 2: Information disclosure en headers**

| Dimensión | Score | Justificación |
|-----------|-------|---------------|
| Damage | 3 | Revela versiones de software |
| Reproducibility | 10 | Siempre visible en requests |
| Exploitability | 2 | Requiere encadenar con otras vulnerabilidades |
| Affected Users | 1 | Solo visible para atacantes técnicos |
| Discoverability | 5 | Scripts kiddies no lo notan fácilmente |
| **Total** | **4.2** | **BAJO** |

**Vulnerabilidad 3: CSRF en cambio de email**

| Dimensión | Score | Justificación |
|-----------|-------|---------------|
| Damage | 6 | Cambio no autorizado de email crítico |
| Reproducibility | 8 | Consistentemente reproducible |
| Exploitability | 6 | Requiere crafting de request malicioso |
| Affected Users | 5 | Solo el usuario víctima |
| Discoverability | 7 | Tokens anti-CSRF detectan la ausencia |
| **Total** | **6.4** | **MEDIO** |

### 4.2 Comparación de vulnerabilidades

| ID | Vulnerabilidad | D | R | E | A | D | Total | Prioridad |
|----|----------------|---|---|---|---|---|-------|----------|
| V1 | Stored XSS | 7 | 10 | 7 | 8 | 7 | 7.8 | 1ro |
| V3 | CSRF | 6 | 8 | 6 | 5 | 7 | 6.4 | 2do |
| V2 | Info disclosure | 3 | 10 | 2 | 1 | 5 | 4.2 | 3ro |

### 4.3 Matriz de priorización

```
┌─────────────────────────────────────────────────────────────┐
│                 MATRIZ DE PRIORIZACIÓN DREAD               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   DAMAGE                                                    │
│     ▲                                                       │
│   10│                                                       │
│    9│                                                       │
│    8│                                    [XSS - V1]         │
│    7│                                                       │
│    6│                          [CSRF - V3]                 │
│    5│                                                       │
│    4│                                                       │
│    3│                  [Info Disc - V2]                     │
│    2│                                                       │
│    1│                                                       │
│    0└────────────────────────────────────────────────►     │
│       0   1   2   3   4   5   6   7   8   9   10          │
│                       EXPLOITABILITY                        │
│                                                             │
│   Leyenda:                                                  │
│   [ ] = Vulnerabilidad V1 (Prioridad 1)                    │
│   [ ] = Vulnerabilidad V3 (Prioridad 2)                    │
│   [ ] = Vulnerabilidad V2 (Prioridad 3)                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. DREAD vs. Otras Metodologías

### 5.1 Comparación con CVSS

| Aspecto | DREAD | CVSS |
|---------|-------|------|
| **Origen** | Microsoft | NIST/FIRST |
| **Complejidad** | Simple (5 dims) | Compleja (3 grupos, 7 métricas) |
| **Flexibilidad** | Menos estructurado | Muy estructurado |
| **Uso actual** | Algunos usan internamente | Estándar de facto |
| **Output** | Score 0-10 | Vector + Score |
| **Base vectorial** | No | Sí (CVSS-BTV) |

### 5.2 Cuándo usar DREAD vs. CVSS

| Situación | Metodología recomendada |
|-----------|------------------------|
| Análisis rápido de vulnerabilidades | DREAD |
| Reportes formales de vulnerabilidades | CVSS v3.1 |
| Priorización en desarrollo agile | DREAD |
| Cumplimiento regulatorio | CVSS |
| Comparación con industry peers | CVSS |
| Decision-making interno | DREAD |

### 5.3 Híbrido: DREAD + CVSS

```
┌─────────────────────────────────────────────────────────────┐
│              ENFOQUE HÍBRIDO RECOMENDADO                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   1. Identificar vulnerabilidad (STRIDE, pentest, SAST)   │
│                    │                                        │
│                    ▼                                        │
│   2. Calificar con CVSS para reporte formal                │
│      - CVSS:3.1 Vector:AV:N/AC:L/PR:N/UI:N/S:U/C:H...    │
│                    │                                        │
│                    ▼                                        │
│   3. Calificar con DREAD para priorización interna        │
│      - D:7 R:8 E:7 A:6 D:5 = 6.6 (Medio)                │
│                    │                                        │
│                    ▼                                        │
│   4. Ajustar priorización según contexto organizacional   │
│      - Si es Critical Asset: aumentar prioridad           │
│      - Si hay amenaza activa: aumentar prioridad         │
│                    │                                        │
│                    ▼                                        │
│   5. Decisión de remediation                               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 6. Adaptaciones de DREAD

### 6.1 DREAD score ajustado para ambiente bancario

| Dimensión | Consideraciones bancarias |
|-----------|--------------------------|
| **Damage** | Incluir impacto regulatorio, multas BCU, pérdida de license |
| **Reproducibility** | Considerar季節性 (Black Friday, fin de mes) |
| **Exploitability** | Incluir disponibilidad de exploits en underground |
| **Affected Users** | Considerar usuarios B2B (empresas) además de retail |
| **Discoverability** | Incluir exposure a internet, scanners Shodan |

### 6.2 DREAD modified (DREAD++)

Algunas organizaciones agregan dimensiones adicionales:

| Dimensión adicional | Descripción |
|--------------------|-------------|
| **Compliance** | Impacto regulatorio (GDPR, BCU, PCI-DSS) |
| **Business Impact** | Impacto en continuidad de negocio |
| **Recovery** | Tiempo y costo de recuperación |

---

## 7. Taller Práctico

### 7.1 Ejercicio: Evaluar vulnerabilidades

**Contexto:** Portal de banca empresarial con las siguientes vulnerabilidades identificadas:

1. Remote Code Execution via file upload
2. Missing function level access control (IDOR)
3. Unencrypted database backup stored on cloud
4. Weak password policy (min 6 caracteres)
5. JWT algorithm confusion vulnerability

**Tarea:** Calificar cada vulnerabilidad con DREAD y priorizarlas.

### 7.2 Solución sugerida

**Vulnerabilidad 1: RCE via file upload**

| Dimensión | Score | Justificación |
|-----------|-------|---------------|
| Damage | 10 | Compromiso total del servidor |
| Reproducibility | 9 | Siempre reproducible |
| Exploitability | 8 | Herramientas públicas disponibles |
| Affected Users | 7 | Potencialmente todos los clientes |
| Discoverability | 6 | Encontrable con fuzzing |
| **Total** | **8.0** | **ALTO** |

**Vulnerabilidad 2: IDOR**

| Dimensión | Score | Justificación |
|-----------|-------|---------------|
| Damage | 6 | Acceso a datos de otros usuarios |
| Reproducibility | 9 | Siempre reproducible |
| Exploitability | 8 | Fácil de manipular IDs |
| Affected Users | 5 | Solo usuarios específicos |
| Discoverability | 7 | Encontrable fácilmente |
| **Total** | **7.0** | **ALTO** |

**Vulnerabilidad 3: Unencrypted backup**

| Dimensión | Score | Justificación |
|-----------|-------|---------------|
| Damage | 9 | Todos los datos potencialmente expuestos |
| Reproducibility | 7 | Requiere acceso al bucket S3 |
| Exploitability | 5 | Depende de permisos mal configurados |
| Affected Users | 10 | Todos los usuarios |
| Discoverability | 8 | Shodan puede encontrar buckets abiertos |
| **Total** | **7.8** | **ALTO** |

**Vulnerabilidad 4: Weak password policy**

| Dimensión | Score | Justificación |
|-----------|-------|---------------|
| Damage | 7 | Cuenta comprometida |
| Reproducibility | 10 | Siempre reproducible |
| Exploitability | 9 | Ataques de fuerza bruta efectivos |
| Affected Users | 7 | Muchos usuarios con contraseñas débiles |
| Discoverability | 8 | Conocido y explotable |
| **Total** | **8.2** | **CRÍTICO** |

**Vulnerabilidad 5: JWT algorithm confusion**

| Dimensión | Score | Justificación |
|-----------|-------|---------------|
| Damage | 8 | Suplantación de identidad |
| Reproducibility | 7 | Requiere condiciones específicas |
| Exploitability | 6 | Conocimiento de cryptografía necesario |
| Affected Users | 7 | Todos los usuarios del sistema |
| Discoverability | 4 | No detectable sin código fuente |
| **Total** | **6.4** | **MEDIO** |

### 7.3 Priorización final

| Prioridad | Vulnerabilidad | DREAD Score | Remediation |
|-----------|---------------|-------------|-------------|
| 1 | Weak password policy | 8.2 | Cambiar política a 12+ chars, MFA |
| 2 | RCE via file upload | 8.0 | Validar uploads, aislar storage |
| 3 | Unencrypted backup | 7.8 | Cifrar backups, IAM policies |
| 4 | IDOR | 7.0 | Implementar authorization checks |
| 5 | JWT confusion | 6.4 | Hardcode algorithm, update library |

---

## 8. Plantilla de Documentación DREAD

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
INFORME DE EVALUACIÓN DREAD
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PROYECTO/SISTEMA: [Nombre]
FECHA: [Fecha]
ELABORADO POR: [Nombre]
VERSIÓN: [Versión]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
VULNERABILIDADES EVALUADAS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

| ID | Descripción | D | R | E | A | D | Score | Nivel | Remediation | SLA |
|----|-------------|---|---|---|---|---|-------|-------|-------------|-----|
| 01 | | | | | | | | | | |
| 02 | | | | | | | | | | |
| 03 | | | | | | | | | | |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RESUMEN EJECUTIVO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Total vulnerabilidades evaluadas: [X]
Críticas: [X]
Altas: [X]
Medias: [X]
Bajas: [X]

Vulnerabilidades por remediar en 24h:
Vulnerabilidades por remediar en 1 semana:
Vulnerabilidades por remediar en 1 mes:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
APROBACIONES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CISO: ____________________ Fecha: ____/____/______
Gerente de Desarrollo: ____________________ Fecha: ____/____/______

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 9. Limitaciones y Mejores Prácticas

### 9.1 Limitaciones de DREAD

1. **Subjetividad:** Las calificaciones pueden variar entre evaluadores
2. **No considera contexto temporal:** Vulnerabilidades pueden volverse más o menos críticas
3. **No estándar:** No hay un estándar oficial widely accepted
4. **Simplificación excesiva:** Reduce complejidad a números

### 9.2 Mejores prácticas

| Práctica | Recomendación |
|----------|---------------|
| **Consistencia** | Usar definiciones claras y ejemplos para cada nivel |
| **Calibración** | Hacer sesiones de calibración entre evaluadores |
| **Documentación** | Justificar siempre cada calificación |
| **Revisión** | Peer review de calificaciones DREAD |
| **Contexto** | Ajustar según criticidad del activo |
| **Actualización** | Re-evaluar periódicamente, especialmente post-remediation |

### 9.3 Matriz de calibración

| Para alcanzar consistencia | Acción |
|---------------------------|--------|
| Crear ejemplos de referencia | Documentar 2-3 casos por nivel |
| Sesiones de calibración | Discutir calificaciones en equipo |
| Dual evaluation | Cada vuln. evaluada por 2 personas |
| Archivo de decisiones pasadas | Mantener registro de justificaciones |

---

## Resumen

DREAD es una herramienta útil para:

1. **Priorizar** vulnerabilidades de forma sistemática
2. **Comunicar** riesgo a stakeholders no técnicos
3. **Comparar** diferentes vulnerabilidades objetivamente
4. **Complementar** análisis de amenazas (STRIDE)
5. **Decidir** dónde invertir recursos de remediation

Aunque tiene limitaciones, cuando se usa consistentemente y con documentación adecuada, DREAD proporciona un marco práctico para la gestión de vulnerabilidades.

---

**Material complementario:**
- Plantilla de evaluación DREAD (en carpeta Templates)
- Tabla de calibración de ejemplo
- Ejercicios adicionales con diferentes escenarios

**Referencias:**
- Microsoft Security Development Lifecycle (SDL)
- OWASP Risk Rating Methodology
- NIST SP 800-30
