# POL-05 · Política de Gestión de Vulnerabilidades

> **Función del MCU 5.0:** Proteger (PR.PS — seguridad de plataformas) · Detectar (DE.CM — monitoreo) · Responder (RS)
> **ISO/IEC 27001:** A.8.8 (gestión de vulnerabilidades técnicas) · A.8.9 (gestión de configuraciones) · A.8.7 (protección contra malware)
> **BCU:** EMG y RNRCSF — corrección oportuna de vulnerabilidades como control de riesgo tecnológico
> **URCDP:** Ley 18.331 art. 10 — vulnerabilidades sin corregir pueden derivar en vulneraciones de datos personales (Decreto 64/020)
> **Nivel del curso:** 🔴 Dominar

---

### ENCABEZADO
| **Campo** | **Valor** |
|---|---|
| **Código** | POL-05 |
| **Título** | Gestión de Vulnerabilidades |
| **Versión** | 1.0 |
| **Estado** | [Borrador / En revisión / Aprobado] |
| **Fecha de aprobación** | [COMPLETAR] |
| **Elaborado por** | RSI + Operaciones de Seguridad |
| **Revisado por** | Div. TI · Producción · Comité de Seguridad |
| **Aprobado por** | Comité de Seguridad de la Información |
| **Clasificación** | Confidencial |
| **Próxima revisión** | [Fecha, máx. 1 año] |

### 1. Objetivo
Establecer el proceso continuo para **descubrir, evaluar, priorizar, corregir y verificar** las vulnerabilidades de los sistemas del Banco, reduciendo la ventana de exposición (ver PCS-02 y PRO-03).

### 2. Alcance
Aplica a todos los activos tecnológicos: servidores, estaciones, equipos de red, bases de datos, aplicaciones (incluidas las públicas), código fuente, contenedores, dependencias, dispositivos móviles y servicios en nube.

### 3. Base: inventario de activos
- El proceso parte del **inventario de activos actualizado** (ID-01) con IP/FQDN, sistema, versión, propietario y criticidad.
- Los activos **fuera de soporte (EOL/EOS)** se identifican y reciben mitigación compensatoria o plan de retiro.

### 4. Escaneo y evaluación
- **Escaneo periódico**: mensual de la red interna y perímetros, con herramienta [COMPLETAR: OpenVAS/comercial].
- **Escaneos específicos** tras: cambios mayores, nueva exposición, avisos de CVE con explotación activa.
- **Aplicaciones web**: pruebas de seguridad (DAST/OWASP ZAP) de las aplicaciones públicas y Banco En Línea, con el WAF en modo monitoreo→bloqueo.
- **Código y contenedores**: análisis estático (SAST), escaneo de imágenes (Trivy) y de dependencias (pip-audit) dentro del SDLC (POL-15).
- **Credenciales expuestas**: escaneo de secretos en repositorios (Gitleaks) y verificación de correos filtrados (HIBP).

### 5. Clasificación y priorización
| Criticidad (CVSS + contexto) | Plazo de corrección | Observaciones |
|---|---|---|
| **Crítico (≥ 9.0 o explotación activa)** | [COMPLETAR: 48–72 h] | Mitigación inmediata mientras se corrige |
| **Alto (7.0–8.9)** | [COMPLETAR: 2 semanas] | En ventana de mantenimiento |
| **Medio (4.0–6.9)** | [COMPLETAR: 1 mes] | Ciclo regular |
| **Bajo (< 4.0)** | [COMPLETAR: 3 meses] | Ciclo trimestral |

La prioridad se ajusta por **contexto**: exposición a internet, datos personales/pago, exploit público.

### 6. Corrección y verificación
- Aplicación de parches según POL-06 (cambios); los críticos pueden ser **emergencias** (PRO-03).
- Prueba previa en homologación para sistemas centrales.
- **Verificación**: escaneo puntual que confirme que la vulnerabilidad desapareció + validación de servicio operativo.
- **Excepciones** (no corregir): aceptación formal del riesgo residual por el Jefe de Riesgos/Comité, con mitigación compensatoria y plazo de revisión (PRO-11).

### 7. Métricas (KPIs)
| Indicador | Fórmula |
|---|---|
| % activos escaneados | Escaneados ÷ inventario |
| % vulnerabilidades corregidas a tiempo | Corregidas en plazo ÷ detectadas |
| Tiempo medio de corrección (MTTR) | Σ días de corrección ÷ n |
| Vulnerabilidades críticas abiertas | Conteo actual |
| % excepciones | Excepciones ÷ hallazgos |

### 8. Responsabilidades
- **Operaciones de Seguridad**: ejecuta escaneos, verifica y reporta.
- **Div. TI / Producción**: aplica parches y pruebas.
- **RSI**: prioriza, gestiona excepciones y reporta al Comité.
- **Comité de Seguridad**: revisa resultados y decide excepciones mayores.

### 9. Cumplimiento y revisión
Los desvíos de plazos se reportan al Comité con plan de recuperación. Revisión anual de la política (o ante cambios del proceso).

### Evidencia del kit
| Evidencia | Documento canónico |
|---|---|
| Escaneos y reportes | DE-01 |
| Registro de corrección y verificación | PRO-03, EV-03 |
| Métricas del tablero | EV-05, Actividad 43 |
| Proceso de gestión | PCS-02 |
| Excepciones aprobadas | PRO-11, GV-03 |
