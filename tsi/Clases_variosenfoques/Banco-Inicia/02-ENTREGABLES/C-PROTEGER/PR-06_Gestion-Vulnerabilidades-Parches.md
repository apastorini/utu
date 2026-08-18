# PR-06 · Gestión de Vulnerabilidades y Parches del Banco
> **Función del MCU 5.0:** Proteger (PR.PS — Seguridad de plataformas) · Detectar (DE.CM — Monitoreo continuo)
> **ISO/IEC 27001:** A.8.8 (Gestión de vulnerabilidades técnicas) · A.8.9 (Gestión de configuraciones)
> **BCU:** Estándares Mínimos de Gestión — Riesgo tecnológico; Circular 2280 (sistema de pagos)
> **URCDP:** Ley 18.331 art. 10 (medidas de seguridad)
> **Nivel del curso:** 🟡 Practicar · 🔴 Dominar

## 1. Qué es y por qué existe
Una vulnerabilidad sin parchear es una puerta abierta: los atacantes escanean internet en busca de sistemas bancarios con fallas conocidas y las explotan en horas. La gestión de vulnerabilidades y parches es el proceso que **descubre, clasifica, prioriza, corrige y verifica** las debilidades técnicas antes de que sean aprovechadas. Agesic recomienda en su guía de gestión de vulnerabilidades **escaneos periódicos mensuales** y plazos de corrección según criticidad.
Esta política define cómo el Banco mantiene al día el **inventario de activos** (base imprescindible del proceso), cómo se **escanea** la infraestructura y las aplicaciones, cómo se **prioriza** cada hallazgo (con el estándar CVSS y el contexto del banco), qué **ventanas de parcheo** se respetan según criticidad, cómo se gestionan las **excepciones** con mitigaciones compensatorias y cómo se **valida** que el parche no haya roto la operación.
En el Banco, los activos más críticos —core bancario, sistema de pagos y Banco En Línea— son también los que más cuidado requieren: un parche mal aplicado puede interrumpir el servicio tanto como la vulnerabilidad que se intenta corregir. Por eso esta política distingue entre los equipos de borde e infraestructura (parcheo ágil) y los sistemas centrales (parcheo planificado con ventana de mantenimiento y prueba).
## 2. Marco de referencia
| **Referencia** | **Requisito aplicable** |
|---|---|
| **MCU 5.0 (Agesic)** | PR.PS — seguridad de plataformas (configuración y mantenimiento); DE.CM — monitoreo continuo |
| **ISO/IEC 27001:2022** | A.8.8 gestión de vulnerabilidades técnicas; A.8.9 gestión de configuraciones |
| **BCU** | EMG · Riesgo tecnológico; Circular 2280 (seguridad del sistema de pagos) |
| **URCDP** | Ley 18.331 art. 10 (medidas de seguridad técnicas) |
| **Agesic** | Guía para la gestión de vulnerabilidades (escaneo mensual recomendado) |

## 3. Cómo completar esta plantilla (guía de llenado)
1. **Completá el encabezado** (código, versión, fecha). La aprueba el Comité de Seguridad de la Información.
2. **Verificá con la Div. TI** que el inventario de activos (ID-01) esté actualizado: sin inventario no hay escaneo confiable.
3. **Definí con Producción y Soporte** la herramienta de escaneo, la frecuencia (mensual) y las ventanas de mantenimiento por sistema.
4. **Personalizá los apartados [COMPLETAR]** con CVSS, plazos de parcheo y responsables reales.
5. **Coordiná el proceso de excepciones** con el Jefe de Riesgos No Financieros (aceptación formal del riesgo residual).
6. **Aprobá, registrá en el control de cambios** y publicá en `02-ENTREGABLES/C-PROTEGER`. Revisá anualmente.
## 4. Plantilla del documento

### ENCABEZADO
| **Campo** | **Valor** |
|---|---|
| **Código** | PR-06 |
| **Título** | Gestión de Vulnerabilidades y Parches |
| **Versión** | 1.0 |
| **Estado** | [Borrador / En revisión / Aprobado] |
| **Fecha de aprobación** | [COMPLETAR] |
| **Elaborado por** | RSI |
| **Revisado por** | Div. TI · Depto. Producción · Comité de Seguridad |
| **Aprobado por** | Comité de Seguridad de la Información |
| **Clasificación** | Uso interno |
| **Próxima revisión** | [Fecha, máx. 1 año] |

### 1. Objetivo
Detectar, priorizar, corregir y verificar las **vulnerabilidades técnicas** de los sistemas del Banco dentro de plazos acordes a su riesgo, minimizando la ventana de exposición a ataques sin afectar la disponibilidad de los servicios.
### 2. Alcance
Aplica a [COMPLETAR: todos los activos tecnológicos del Banco —servidores, estaciones de trabajo, equipos de red, bases de datos, sistemas operativos, aplicaciones del core, Banco En Línea, sistema de pagos—] incluyendo los sistemas administrados o alojados por terceros que procesen información del banco.
### 3. Base: inventario de activos actualizado
- El proceso parte del **inventario de activos** (ID-01), actualizado al menos trimestralmente o ante cambios significativos.
- Se incluyen: IP, sistema operativo, versión, propietario y criticidad del activo.
- Los activos fuera de soporte (EOL/EOS) se identifican y se les aplica **mitigación compensatoria** o plan de retiro.
### 4. Escaneo periódico
- **Escaneo de vulnerabilidades mensual** (recomendación de Agesic) sobre toda la red interna y los perímetros [COMPLETAR: herramienta de escaneo, p. ej. herramientas open source como OpenVAS o soluciones comerciales].
- **Escaneos específicos** tras: cambios mayores, instalación de servicios expuestos y ante avisos de vulnerabilidades activas (CVE con explotación en curso).
- Las credenciales de escaneo se gestionan como cuentas privilegiadas (PR-01).
### 5. Clasificación y priorización
| **Criticidad (CVSS)** | **Plazo de parcheo** | **Observaciones** |
|---|---|---|
| **Crítico (≥ 9.0)** | [COMPLETAR: 48–72 h] | Incluye mitigación inmediata mientras se corrige |
| **Alto (7.0–8.9)** | [COMPLETAR: 2 semanas] | Planificar en la ventana de mantenimiento |
| **Medio (4.0–6.9)** | [COMPLETAR: 1 mes] | Parcheo en el ciclo regular |
| **Bajo (< 4.0)** | [COMPLETAR: 3 meses] | Acumular al ciclo trimestral |

- La prioridad se ajusta por **contexto**: exposición a internet, presencia de datos personales o de pago, y existencia de exploit público.
### 6. Ventanas de parcheo y aplicación
- **Equipos de borde y estaciones:** parcheo inmediato según plazo.
- **Sistemas centrales (core, pagos):** parcheo en **ventana de mantenimiento planificada**, con prueba previa en ambiente de homologación.
- Los parches se prueban en ambiente de prueba antes de producción (salvo vulnerabilidad crítica con riesgo mayor que el del cambio).
- **Validación posterior:** verificar que el servicio quedó operativo, los controles activos y que la vulnerabilidad ya no figura en el escaneo.
### 7. Gestión de excepciones
- Si no es posible parchear en plazo, se registra una **excepción** con: activo, vulnerabilidad, motivo, mitigación compensatoria, responsable y **fecha de vencimiento**.
- Las excepciones de activos críticos se aprueban por el **Comité de Seguridad**; el resto, por el RSI con el dueño del activo.
- Las excepciones se revisan al menos trimestralmente.
### 8. Reporte
El RSI reporta trimestralmente al Comité: número de vulnerabilidades por criticidad, cumplimiento de plazos, excepciones vigentes y tendencia. El informe queda disponible para auditorías del BCU y de Agesic.
### 9. Responsabilidades
| **Rol** | **Responsabilidad** |
|---|---|
| **Div. TI (Producción/Sistemas)** | Ejecutar escaneos y parcheo; mantener el inventario |
| **Dueños de activos** | Aprobar parcheo en sistemas de su área; aceptar riesgos |
| **RSI** | Coordinar el proceso, analizar resultados, excepciones y reporte |
| **Jefe de Riesgos No Financieros** | Aceptar formalmente el riesgo residual de excepciones |
| **Comité de Seguridad** | Aprobar plazos, excepciones críticas y plan anual |

### 10. Control de cambios
| **Versión** | **Fecha** | **Cambio** | **Elaboró** | **Aprobó** |
|---|---|---|---|---|
| 0.1 | [COMPLETAR] | Versión inicial (borrador) | RSI | — |
| 1.0 | [COMPLETAR] | Aprobación del Comité | RSI | Comité |

## 5. Ejemplo aplicado al Banco (modelo de referencia)
Ejemplo ilustrativo de cómo quedaría el apartado 4 completado. Adaptá al contenido institucional real del Banco.
**Escaneo (ejemplo):**
- El Banco ejecuta un **escaneo mensual** sobre toda la red con su herramienta de escaneo; en enero de 2026 detectó 3 vulnerabilidades críticas en un equipo perimetral de conexión con el sistema de pagos. Dos se parchearon en **48 h**; la tercera requirió excepción de 15 días (por compatibilidad con el middleware) con **mitigación compensatoria**: regla de firewall restrictiva y monitoreo intensificado de ese equipo.
**Ventana de mantenimiento (ejemplo):**
- Los parches de seguridad del **core bancario** se aplican en la ventana mensual de mantenimiento (domingos de 02:00 a 05:00), tras validación en el ambiente de homologación. En el ciclo de marzo se aplicaron los parches de alta prioridad sin afectar la operación y la validación posterior confirmó el servicio activo a las 05:30.
**Ciclo de mejora (ejemplo):**
- Al detectar que el 20 % de las estaciones de sucursal tenía parches pendientes por baja conectividad, se habilitó la descarga de parches por el canal de replicación local y el cumplimiento subió de 80 % a 97 % en dos meses. El resultado se reportó al Comité junto con la tendencia trimestral.

**Documentos relacionados:** ID-01 (Inventario de Activos), PR-01 (Control de Acceso), PR-03 (Seguridad de Datos), DE-01 (Monitoreo), DE-03 (Pruebas de Seguridad), RS-01 (Incidentes), PR-07 (Desarrollo Seguro).
