# RC-01 · Plan de Continuidad del Negocio (BCP) del Banco
> **Función del MCU 5.0:** Recuperar (RC.RP — Planificación de la recuperación)
> **ISO/IEC 27001:** A.5.29 (Continuidad de la seguridad de la información) · A.5.30 (Tecnologías para la continuidad)
> **BCU:** Estándares Mínimos de Gestión — Continuidad · Circular 2227
> **URCDP:** Ley 18.331 art. 10 (disponibilidad y seguridad de datos)
> **Nivel del curso:** 🟡 Practicar · 🔴 Dominar

## 1. Qué es y por qué existe
El **Plan de Continuidad del Negocio (BCP)** garantiza que los procesos esenciales del Banco sigan operando, aunque sea en forma reducida, cuando ocurre una interrupción: un incendio en el centro de cómputos, un ciberataque, una pandemia, una falla de un proveedor o una catástrofe natural. Mientras el DRP (RC-02) se ocupa de recuperar los sistemas, el BCP se ocupa del **negocio**: que los clientes puedan seguir pagando cuotas, cobrando ahorros y gestionando sus créditos.
Para el BCU, la continuidad es un estándar mínimo de gestión: la entidad debe identificar sus procesos críticos, medir el impacto de su interrupción y tener estrategias probadas de recuperación. Para el MCU 5.0 (RC.RP) el Banco debe tener planes de recuperación alineados con la tolerancia a la indisponibilidad definida (perfil Avanzado: no más de 24 horas corridas para servicios críticos).
El BCP se construye sobre un **análisis de impacto al negocio (BIA)**: qué procesos son críticos, cuánta pérdida produce cada hora de interrupción y cuánto se puede tardar en recuperarlos (RTO) sin perder datos más allá de lo aceptable (RPO). Sin BIA no hay BCP: solo una lista de buenas intenciones.
## 2. Marco de referencia
| **Norma** | **Referencia** | **Qué exige** |
|---|---|---|
| **MCU 5.0 (Agesic)** | RC.RP | Planificación de la recuperación según la criticidad y la tolerancia definida |
| **ISO/IEC 27001:2022** | A.5.29 / A.5.30 | Planificación de la continuidad de la seguridad de la información |
| **BCU** | EMG · Continuidad · Circular 2227 | Procesos críticos, estrategias de continuidad y pruebas |
| **URCDP** | Ley 18.331 art. 10 | Disponibilidad de los datos personales y del servicio al titular |

## 3. Cómo completar esta plantilla (guía de llenado)
1. **Hacé el BIA con cada dueño de proceso:** junto a los gerentes de las Áreas Comercial, Operaciones y TI, y Financiera, identificá procesos críticos, dependencias y tolerancias (RTO/RPO).
2. **Definí la organización de crisis** con la Gerencia General: Comité de Crisis, integrantes, suplentes y decisiones delegadas.
3. **Determiná las estrategias de continuidad** con la División TI y Operaciones: trabajo alternativo, sede alterna, proveedores de respaldo, acuerdos con terceros.
4. **Definí los procedimientos de recuperación por proceso** con los dueños: pasos, responsables y recursos necesarios.
5. **Programá las pruebas** con el RSI y el Comité: simulacros por proceso al menos anuales, con reporte de resultados.
6. Consultá al **RSI** (Riesgos No Financieros) para alinear el BCP con la gestión de riesgos y con el **Oficial de Cumplimiento** para los procesos de pago regulados.
## 4. Plantilla del documento

### ENCABEZADO
| **Campo** | **Valor** |
|---|---|
| **Código** | RC-01 |
| **Título** | Plan de Continuidad del Negocio (BCP) |
| **Versión** | 1.0 |
| **Estado** | [Borrador / En revisión / Aprobado] |
| **Fecha de aprobación** | [COMPLETAR] |
| **Elaborado por** | RSI |
| **Revisado por** | Comité de Crisis · Comité de Seguridad de la Información |
| **Aprobado por** | Directorio |
| **Clasificación** | Uso interno |
| **Próxima revisión** | [Fecha, máx. 1 año] |

### 1. Objetivo
Asegurar la continuidad de los procesos esenciales del Banco ante interrupciones, dentro de los tiempos de recuperación (RTO/RPO) aprobados, minimizando pérdidas y protegiendo a clientes, funcionarios y la confianza pública.
### 2. Alcance
Aplica a [COMPLETAR: procesos críticos del Banco: crédito hipotecario, captación de ahorro, sistema de pagos, atención al cliente, gestión financiera y administración]. Cubre instalaciones, sistemas, personas y proveedores.
### 3. Análisis de impacto al negocio (BIA)
| **Proceso crítico** | **Dueño** | **RTO** | **RPO** | **Impacto por hora de interrupción** |
|---|---|---|---|---|
| **Sistema de pagos** | Dpto. Sistema de Pagos | [COMPLETAR: 4 h] | [COMPLETAR] | [COMPLETAR] |
| **Crédito hipotecario (cobranza de cuotas)** | Área Comercial | [COMPLETAR: 8 h] | [COMPLETAR] | [COMPLETAR] |
| **Ahorro / captación** | Área Comercial | [COMPLETAR: 8 h] | [COMPLETAR] | [COMPLETAR] |
| **Atención al cliente (sucursales y canales)** | Dpto. Canales de Atención | [COMPLETAR: 4 h] | [COMPLETAR] | [COMPLETAR] |
| **Finanzas y mercado de capitales** | Div. Finanzas y Mercado | [COMPLETAR: 24 h] | [COMPLETAR] | [COMPLETAR] |

### 4. Organización de crisis
| **Rol** | **Integrante sugerido** | **Función** |
|---|---|---|
| **Comité de Crisis** | Gerente General + gerentes de área | Decide la activación, prioridades y recursos |
| **Coordinador de continuidad** | RSI | Conduce la ejecución del plan |
| **Coordinador de recuperación TI** | Gerente Div. TI | Recuperación de sistemas (con RC-02) |
| **Coordinador de logística** | Dpto. Servicios Generales | Sede alterna, transporte, suministros |
| **Comunicaciones** | [COMPLETAR] | Comunicados internos y externos (RC-03) |
| **DPD / Legal** | DPD + Servicios Jurídicos | Obligaciones legales y datos personales |

### 5. Estrategias de continuidad
[COMPLETAR: sede alterna de trabajo, teletrabajo, redundancia de proveedores de telecomunicaciones, contrato con proveedor de cómputo en la nube/respaldo, personal clave con roles cruzados, y acuerdos de niveles de servicio con terceros críticos].
### 6. Activación del plan
El plan se activa cuando [COMPLETAR: criterios: interrupción que supera X horas de un proceso crítico, decisión del Comité de Crisis]. La activación se registra y comunica según la matriz de RC-03.
### 7. Procedimientos de recuperación por proceso
Para cada proceso crítico del BIA se documenta: pasos de recuperación, responsables, recursos y sistemas requeridos, y el punto de recuperación (RPO) desde el cual se restaura la información. [COMPLETAR: insertar los procedimientos por proceso: crédito, ahorro, pagos, atención al cliente].
### 8. Pruebas del plan
Se realizan simulacros [COMPLETAR: al menos anuales y ante cambios mayores], con un informe de resultados (RC-04) que incluya: procesos probados, desvíos frente a RTO/RPO y acciones de mejora.
### 9. Control de cambios
| **Versión** | **Fecha** | **Cambio** | **Elaboró** | **Aprobó** |
|---|---|---|---|---|
| 0.1 | [COMPLETAR] | Versión inicial (borrador) | RSI | — |
| 1.0 | [COMPLETAR] | Aprobación del Directorio | RSI | Directorio |

## 5. Ejemplo aplicado al Banco (modelo de referencia)
Ejemplo ilustrativo. Adaptá a la operación real del Banco.
**BIA (ejemplo):**
- **Sistema de pagos:** RTO de 4 h, RPO de 15 minutos; es el proceso con mayor impacto regulatorio (Circular 2280): cada hora caída afecta a clientes y contrapartes del sistema de pagos uruguayo.
- **Cobranza de cuotas hipotecarias:** RTO de 8 h en días de cobranza; RPO de 1 día. Se priorizan los días de vencimiento.
- **Banco En Línea:** RTO de 4 h en horario hábil; RPO de 5 minutos para transacciones, dado el riesgo de fraude.
- **Sucursales:** RTO de 24 h para operación reducida (retiro de ahorros y pagos) con procedimiento manual autorizado.
**Estrategias (ejemplo):**
- Sede alterna de operación contratada/identificada a [COMPLETAR] km del edificio central, con estaciones, telefonía y conexiones probadas.
- Procedimientos manuales de contingencia para el cobro de cuotas en sucursales (recibo manual con cierre en línea posterior).
- Proveedor de telecomunicaciones con doble ruta y enlace de respaldo del centro de cómputos.
- Roles cruzados: dos personas entrenadas por proceso crítico.
**Prueba (ejemplo):** simulacro anual de interrupción del sistema de pagos: se operó 2 horas en modo contingencia con datos de RPO de 15 minutos; el desvío fue de 40 minutos por una falla de documentación, corregido en RC-04 y re-probado en el tercer trimestre.

**Documentos relacionados:**
- RC-02 (DRP) · RC-03 (Comunicación de Crisis) · RC-04 (Lecciones Aprendidas)
- RS-01 (Respuesta a Incidentes) · PR-05 (Respaldo)
- BCU-06 (Plan de Contingencia y Continuidad)
