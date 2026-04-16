# Clase: Análisis de Riesgos de Seguridad de la Información

## Introducción

El análisis de riesgos es el proceso sistemático de identificar, evaluar y priorizar los riesgos que pueden afectar la confidencialidad, integridad y disponibilidad de los activos de información de una organización. Esta clase proporciona una guía completa sobre cómo conducir análisis de riesgos efectivos, desde la identificación hasta la implementación de controles.

**Objetivos de aprendizaje:**
1. Comprender los conceptos fundamentales de gestión de riesgos
2. Aplicar metodologías de análisis de riesgos (cuantitativas y cualitativas)
3. Identificar amenazas y vulnerabilidades relevantes
4. Calcular y priorizar riesgos
5. Seleccionar y diseñar controles apropiados
6. Documentar el proceso y mantenerlo actualizado

---

## 1. Fundamentos de Gestión de Riesgos

### 1.1 ¿Qué es un riesgo?

Un **riesgo** es la posibilidad de que una amenaza aproveche una vulnerabilidad para causar daño a un activo. Se expresa típicamente como:

```
Riesgo = Probabilidad × Impacto
```

**Componentes del riesgo:**

| Componente | Descripción | Ejemplo |
|------------|-------------|---------|
| **Amenaza** | Evento potencial que puede causar daño | Ransomware, terremoto, empleado insatisfecho |
| **Vulnerabilidad** | Debilidad que puede ser explotada | Sistema sin parches, contraseña débil |
| **Activo** | Recurso que tiene valor para la organización | Base de datos de clientes, servidor web |
| **Impacto** | Consecuencia si el riesgo se materializa | Pérdida financiera, daño reputacional |

### 1.2 Marco normativo y mejores prácticas

| Marco | Descripción | Uso principal |
|-------|-------------|---------------|
| **ISO 31000** | Gestión del riesgo - Directrices | Enfoque general de gestión de riesgos |
| **ISO 27005** | Gestión de riesgos en seguridad de la información | Enfoque específico para InfoSec |
| **NIST SP 800-30** | Guide for Conducting Risk Assessments | Metodología del gobierno de EE.UU. |
| **NIST CSF** | Cybersecurity Framework | Marco de ciberseguridad |
| **COSO ERM** | Enterprise Risk Management | Gestión integral de riesgos empresariales |
| **MAGERIT** | Metodología de análisis y gestión de riesgos de TI | Metodología española/MER |

### 1.3 Tipos de análisis de riesgos

| Tipo | Descripción | Ventajas | Desventajas |
|------|-------------|----------|-------------|
| **Cualitativo** | Usa descripciones verbales y escalas | Rápido, fácil de entender | Subjetivo, menos preciso |
| **Cuantitativo** | Usa valores numéricos | Preciso, facilita comparación | Requiere datos, más complejo |
| **Híbrido** | Combina ambos enfoques | Balance entre precisión y practicidad | Puede requerir más recursos |

---

## 2. Proceso de Análisis de Riesgos

### 2.1 Fases del proceso

```
┌─────────────────────────────────────────────────────────────────┐
│                    PROCESO DE ANÁLISIS DE RIESGOS               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐ │
│   │   1.    │───▶│   2.    │───▶│   3.    │───▶│   4.    │ │
│   │ Context │    │   ID    │    │ Analiz. │    │  Eval.   │ │
│   │   o     │    │  riesgo │    │  riesgo  │    │  riesgo  │ │
│   └──────────┘    └──────────┘    └──────────┘    └──────────┘ │
│                                                                 │
│        ┌──────────┐    ┌──────────┐    ┌──────────┐           │
│   ◀───│   6.    │◀───│   5.    │◀───│   4b.   │           │
│        │ Monit.  │    │ Tratar  │    │ Prioriz.│           │
│        │  y rev. │    │ riesgo  │    │         │           │
│        └──────────┘    └──────────┘    └──────────┘           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 Fase 1: Establecimiento del contexto

**Contexto organizacional:**
- Misión, visión y objetivos estratégicos
- Estructura organizacional
- Políticas y regulaciones aplicables
- Partes interesadas y sus expectativas
- Criterios de aceptación del riesgo

**Contexto técnico:**
- Inventario de activos de información
- Arquitectura de sistemas
- Proveedores y servicios tercerizados
- Flujos de información
- Tecnologías utilizadas

### 2.3 Fase 2: Identificación de riesgos

**Técnicas de identificación:**

1. **Análisis de escenarios:** Imaginar situaciones hipotéticas
2. **Lluvia de ideas (Brainstorming):** Sesiones con expertos
3. **Delphi:** Consulta anónima a expertos
4. ** checklists:** Listas predefinidas de riesgos comunes
5. **Análisis de causa raíz:** Identificar causas profundas
6. **Análisis de tendencias:** Revisión de incidentes pasados
7. **Threat modeling:** Modelado sistemático de amenazas

**Categorización de riesgos:**

| Categoría | Ejemplos |
|-----------|----------|
| **Estratégicos** | Cambios regulatorios, competencia, mercado |
| **Operativos** | Error humano, falla de sistemas, fraude |
| **Financieros** | Pérdida de ingresos, sobrecostes, fraude |
| **Cumplimiento** | Sanciones, litigios, multas |
| **Tecnológicos** | Ciberseguridad, obsolescencia, dependencia |
| **Reputacionales** | Publicidad negativa, pérdida de confianza |

---

## 3. Metodología de Análisis Cualitativo

### 3.1 Escala de probabilidad

| Nivel | Valor | Descripción | Frecuencia orientativa |
|-------|-------|-------------|----------------------|
| Muy Baja | 1 | Improbable que ocurra | < 1% de probabilidad |
| Baja | 2 | Poco probable pero posible | 1-20% |
| Media | 3 | Podría ocurrir | 21-50% |
| Alta | 4 | Probable | 51-80% |
| Muy Alta | 5 | Casi seguro | > 80% |

### 3.2 Escala de impacto

| Nivel | Valor | Descripción | Criterios |
|-------|-------|-------------|----------|
| Muy Bajo | 1 | Impacto insignificante | Sin efecto perceptible |
| Bajo | 2 | Impacto menor | Afectación local, manejable internamente |
| Medio | 3 | Impacto significativo | Afectación departamental, requiere gestión |
| Alto | 4 | Impacto grave | Afectación organizacional, comunicación externa |
| Muy Alto | 5 | Impacto catastrófico | Crisis organizacional, posible cierre |

### 3.3 Matriz de valoración

```
         IMPACTO
         1     2     3     4     5
Prob  ┌─────┬─────┬─────┬─────┬─────┐
  5   │  5  │ 10  │ 15  │ 20  │ 25  │  ■ Rojo: Crítico (15-25)
      ├─────┼─────┼─────┼─────┼─────┤    - Acciones inmediatas
  4   │  4  │  8  │ 12  │ 16  │ 20  │  🟠 Naranja: Alto (10-14)
      ├─────┼─────┼─────┼─────┼─────┤    - Acciones urgentes
  3   │  3  │  6  │  9  │ 12  │ 15  │  🟡 Amarillo: Medio (5-9)
      ├─────┼─────┼─────┼─────┼─────┤    - Planificar mitigación
  2   │  2  │  4  │  6  │  8  │ 10  │  🟢 Verde: Bajo (1-4)
      ├─────┼─────┼─────┼─────┼─────┤    - Monitorear
  1   │  1  │  2  │  3  │  4  │  5  │
      └─────┴─────┴─────┴─────┴─────┘
```

### 3.4 Ejemplo práctico de análisis cualitativo

| ID | Activo | Amenaza | Vulnerabilidad | Prob | Imp | Valor | Nivel |
|----|--------|---------|-----------------|------|-----|-------|-------|
| R-001 | Base de datos clientes | Ransomware | Parches desactualizados | 3 | 5 | 15 | Crítico |
| R-002 | Servidor web | SQL Injection | Falta validación input | 4 | 4 | 16 | Crítico |
| R-003 | Portales digitales | Phishing | Sin MFA | 4 | 3 | 12 | Alto |
| R-004 | Emails | Spear phishing | Capacitación insuficiente | 4 | 3 | 12 | Alto |
| R-005 | Workstations | Malware | Sin EDR | 3 | 3 | 9 | Medio |

---

## 4. Metodología de Análisis Cuantitativo

### 4.1 Conceptos fundamentales

**Pérdida Esperada Anual (ALE - Annual Loss Expectancy):**

```
ALE = SLE × ARO
```

Donde:
- **SLE** (Single Loss Expectancy): Pérdida por evento individual
- **ARO** (Annualized Rate of Occurrence): Frecuencia anual de ocurrencia

**Cálculo de SLE:**

```
SLE = Valor del activo × Factor de exposición
```

### 4.2 Ejemplo de cálculo cuantitativo

| Parámetro | Valor | Ejemplo |
|------------|-------|---------|
| Valor del activo | $500,000 | Costo de reconstrucción/repetición |
| Probabilidad anual (ARO) | 0.2 | 1 vez cada 5 años |
| Factor de exposición | 50% | Solo el 50% de los datos |
| **SLE** | $250,000 | Valor × Exposición |
| **ALE** | $50,000 | SLE × ARO |

### 4.3 Tabla de cuantificación

| Nivel de riesgo | Valor monetario ALE | Acciones recomendadas |
|-----------------|--------------------|-----------------------|
| Crítico | > $500,000 | Mitigación inmediata, inversión obligatoria |
| Alto | $100,000 - $500,000 | Plan de mitigación urgente |
| Medio | $10,000 - $100,000 | Evaluar costo-beneficio de controles |
| Bajo | < $10,000 | Aceptación o transferencia (seguros) |

---

## 5. Identificación de Amenazas y Vulnerabilidades

### 5.1 Taxonomía de amenazas

**Origen de las amenazas:**

| Categoría | Ejemplos | Probabilidad relativa |
|-----------|----------|----------------------|
| **Natural** | Terremotos, inundaciones, tormentas | Variable según ubicación |
| **Técnica** | Falla de hardware, software, comunicaciones | Alta |
| **Humana accidental** | Error humano, negligencia | Muy alta |
| **Humana intencional (interna)** | Empleado insatisfecho,间谍 | Media |
| **Humana intencional (externa)** | Hackers, cibercriminales, APT | Alta |
| **Organizacional** | Cambio de proveedor, reestructuración | Media |

### 5.2 Fuentes de amenazas comunes

| Fuente | Motivación | Capacidades típicas |
|--------|------------|---------------------|
| **Script kiddies** | Entretenimiento, reputación | Básica |
| **Cibercriminales** | Beneficio económico | Media-Alta |
| **Hacktivistas** | Ideología política | Media |
| **Estados-nación (APT)** | Espionaje, sabotaje | Muy alta |
| **Insiders** | Venganza, beneficio personal | Variable |
| **Terroristas** | Causar miedo, propaganda | Variable |
| **Competidores** | Ventaja comercial | Media |

### 5.3 Categorías de vulnerabilidades

| Categoría | Ejemplos | Detección |
|-----------|----------|-----------|
| **Físicas** | Puertas sin control, cables expuestos | Auditoría física |
| **De software** | Bugs, configuraciones inseguras | Escaneo, pentesting |
| **De red** | Puertos abiertos, protocolos inseguros | Análisis de tráfico |
| **De proceso** | Falta de procedimientos, segregación | Revisión de procesos |
| **Humanas** | Falta de capacitación, negligencia | Auditoría, simulacros |
| **De diseño** | Arquitectura deficiente | Revisión de diseño |

### 5.4 Checklist de vulnerabilidades comunes

- [ ] Sistemas operativos sin parches actualizados
- [ ] Contraseñas débiles o por defecto
- [ ] Falta de autenticación multifactor
- [ ] Configuraciones por defecto
- [ ] Servicios innecesarios activos
- [ ] Permisos excesivos
- [ ] Falta de cifrado en datos sensibles
- [ ] Backups no probados
- [ ] Registro y monitoreo insuficientes
- [ ] Falta de segmentación de red
- [ ] Proveedores sin evaluación de seguridad
- [ ] Personal sin capacitación

---

## 6. Evaluación y Priorización de Riesgos

### 6.1 Criterios de priorización

| Criterio | Descripción | Peso sugerido |
|----------|-------------|--------------|
| Magnitud del impacto | Severidad de las consecuencias | 40% |
| Probabilidad de ocurrencia | Likelihood de que ocurra | 30% |
| Velocidad de aparición | Tiempo para materializarse | 10% |
| Persistencia | Duración del impacto | 10% |
| Detectabilidad | Qué tan fácil es identificarlo | 10% |

### 6.2 Priorización usando MoSCoW

| Categoría | Descripción | Porcentaje objetivo |
|-----------|-------------|--------------------|
| **Must have** (Crítico) | Requerido obligatoriamente | 60% del esfuerzo |
| **Should have** (Alto) | Altamente deseable | 20% del esfuerzo |
| **Could have** (Medio) | Deseable si hay recursos | 15% del esfuerzo |
| **Won't have** (Bajo) | Excluido en esta iteración | 5% del esfuerzo |

### 6.3 Matriz de priorización

| | Impacto ALTO | Impacto MEDIO | Impacto BAJO |
|---|---|---|---|
| **Probabilidad ALTA** | 1. Inmediato | 2. Corto plazo | 3. Medio plazo |
| **Probabilidad MEDIA** | 4. Corto plazo | 5. Medio plazo | 6. Monitorear |
| **Probabilidad BAJA** | 7. Medio plazo | 8. Monitorear | 9. Aceptar |

---

## 7. Tratamiento de Riesgos

### 7.1 Opciones de tratamiento

| Opción | Descripción | Cuándo usar |
|--------|-------------|-------------|
| **Mitigar** | Reducir probabilidad e/o impacto | Cuando el riesgo es inaceptable |
| **Transferir** | Trasladar a terceros (seguros, outsourcing) | Cuando no se puede mitigar económicamente |
| **Aceptar** | Asumir el riesgo deliberadamente | Cuando el costo > beneficio |
| **Evitar** | Eliminar la actividad que genera riesgo | Cuando es posible y viable |
| **Ignorar** | No tomar acción (NO recomendado) | Solo en riesgos muy bajos |

### 7.2 Selección de controles

**Controles preventivos:**
- Evitan que ocurra el incidente
- Ejemplos: Firewall, autenticación, cifrado, formación

**Controles detectives:**
- Detectan que está ocurriendo
- Ejemplos: SIEM, logs, IDS, antivirus

**Controles correctivos:**
- Reducen el impacto después de ocurrido
- Ejemplos: Backup, DRP, procedimientos de respuesta

### 7.3 Costo-beneficio de controles

```
Justificación del control:
Beneficio = ALE (sin control) - ALE (con control) - Costo del control

Si Beneficio > 0: El control está justificado económicamente
```

| Nivel de riesgo | Control recomendado | Inversión máxima (% de ALE) |
|-----------------|--------------------|----------------------------|
| Crítico | Múltiples controles robustos | 80-100% del ALE |
| Alto | Controles sustanciales | 50-80% del ALE |
| Medio | Controles básicos | 20-50% del ALE |
| Bajo | Controles mínimos o monitoreo | < 20% del ALE |

---

## 8. Documentación del Análisis de Riesgos

### 8.1 Contenido del informe de riesgos

1. **Resumen ejecutivo** - Conclusiones clave para la dirección
2. **Alcance y metodología** - Qué se analizó y cómo
3. **Inventario de activos** - Activos incluidos en el análisis
4. **Identificación de amenazas** - Amenazas relevantes
5. **Evaluación de vulnerabilidades** - Debilidades identificadas
6. **Matriz de riesgos** - Valoración de cada riesgo
7. **Planes de tratamiento** - Controles propuestos
8. **Recomendaciones** - Priorizadas según criticidad
9. **Anexos** - Evidencia, cálculos detallados

### 8.2 Registro de riesgos

| Campo | Descripción |
|-------|-------------|
| ID | Identificador único |
| Fecha de creación | Cuándo se identificó |
| Activo relacionado | Activo(s) afectado(s) |
| Amenaza | Descripción de la amenaza |
| Vulnerabilidad | Debilidad explotable |
| Probabilidad | Valoración (1-5 o cuantitativa) |
| Impacto | Valoración (1-5 o cuantitativa) |
| Valor del riesgo | Resultado del cálculo |
| Nivel de riesgo | Clasificación (Bajo/Medio/Alto/Crítico) |
| Controles actuales | Medidas existentes |
| Controles propuestos | Mejoras recomendadas |
| Responsable | Persona a cargo |
| Fecha de revisión | Próxima evaluación |

---

## 9. Mantenimiento y Mejora Continua

### 9.1 Frecuencia de revisión

| Tipo de revisión | Frecuencia | Triggerevents |
|------------------|------------|---------------|
| Revisión completa | Anual | Fin de año fiscal |
| Revisión de riesgos críticos | Trimestral | Cambio de trimestre |
| Revisión de riesgos altos | Mensual | — |
| Revisión ante cambios | Ad-hoc | Nuevos sistemas, mergers, incidentes |

### 9.2 Indicadores de efectividad

| KRI | Descripción | Objetivo |
|-----|-------------|----------|
| Reducción de riesgo residual | % de riesgos en nivel aceptable | > 90% |
| Implementación de controles | % de controles implementados a tiempo | > 95% |
| Nuevas vulnerabilidades | # de vulnerabilidades críticas nuevas | < 5/mes |
| Tiempo de remediación | Días promedio en cerrar vulnerabilidades | < 30 días |

---

## 10. Taller Práctico

### 10.1 Ejercicio: Análisis de riesgo de un portal web

**Contexto:** Una empresa bancaria tiene un portal de banca online que maneja datos de 100,000 clientes.

**Activos identificados:**
- Servidor web (valor: $50,000)
- Base de datos de clientes (valor: $500,000)
- Certificados SSL (valor: $5,000)
- Reputación (valor: $1,000,000)

**Tarea:** Realizar un análisis de riesgos cualitativo identificando al menos 5 riesgos.

### 10.2 Solución sugerida

| ID | Activo | Amenaza | Vulnerabilidad | Prob | Imp | Valor | Nivel |
|----|--------|---------|----------------|------|-----|-------|-------|
| 1 | DB clientes | Breach de datos | Falta cifrado | 2 | 5 | 10 | Alto |
| 2 | Servidor web | DDoS | Sin anti-DDoS | 3 | 3 | 9 | Medio |
| 3 | Servidor web | SQL Injection | Input no validado | 3 | 4 | 12 | Alto |
| 4 | Certificados | Expiración | Sin alerta | 3 | 2 | 6 | Medio |
| 5 | Reputación | Publicidad negativa | Sin plan de crisis | 2 | 4 | 8 | Medio |

---

## Resumen

El análisis de riesgos es un proceso continuo y iterativo que permite a las organizaciones:
- **Conocer** sus activos y su valor
- **Entender** las amenazas y vulnerabilidades
- **Cuantificar** los riesgos de forma sistemática
- **Decidir** qué riesgos mitigar, transferir o aceptar
- **Actuar** implementando controles apropiados
- **Mejorar** continuamente mediante revisión y ajustes

La clave del éxito está en adaptar la metodología a las necesidades de la organización, involucrar a las partes interesadas correctas, y mantener el proceso vivo y actualizado.

---

**Material complementario:**
- Plantilla de Análisis de Riesgos (en carpeta Templates)
- Caso de estudio: Análisis de riesgos en infraestructura bancaria
- Referencias: ISO 27005, NIST SP 800-30, MAGERIT
