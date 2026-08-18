# AISEC-09 · Gobierno y auditoría del uso de IA

> **Función del MCU 5.0:** Este módulo vincula el uso de IA con el dominio Gobernar (GV) y los transversales CN (cumplimiento) y PD (protección de datos): política, roles, evaluación de impacto, registro de tratamientos y auditoría.
> **ISO/IEC 27001:** Liderazgo y compromiso (A.5.1), roles y responsabilidades (A.5.2-A.5.3), cumplimiento (A.5.31-A.5.34). Referencia: ISO/IEC 42001 para gobernanza de IA.
> **BCU:** El gobierno de la IA forma parte del gobierno de la información que exigen los EMG y el RNRCSF.
> **URCDP:** Responsabilidad proactiva (Ley 19.670): EIPD, registro de bases, DPD, y capacidad de responder ante titulares y ante la autoridad.
> **Nivel del curso:** 🔴 Dominar

---

## 1. Gobierno de la IA: quién decide qué

| Rol | Responsabilidad |
|---|---|
| **Dirección / Alta gerencia** | Aprueba la política de IA, asigna recursos y sanciona el marco de uso |
| **RSI** | Custodia el riesgo: autoriza herramientas, revisa incidentes, mantiene evidencia |
| **DPD (Delegado de Protección de Datos)** | Evalúa la legalidad de los tratamientos con IA y los EIPD |
| **TI** | Despliega, configura y mantiene las herramientas (AISEC-08) |
| **Usuarios** | Usan la herramienta oficial, respetan las reglas (AISEC-06/07) |
| **Auditoría interna** | Verifica el cumplimiento del marco |

---

## 2. La política de uso aceptable de IA

El Banco debe tener una **política de uso aceptable de IA** aprobada (plantilla base: `templates-ISACA\02-AI-Acceptable-Use`). Contenido mínimo:

1. **Alcance**: herramientas oficiales autorizadas (BigPickle, OpenCode, etc.).
2. **Prohibiciones**: cuentas personales, datos de clientes, extensiones no autorizadas.
3. **Clasificación de datos**: qué datos entran y cuáles no (módulo 06).
4. **Revisión humana**: obligatoria sobre todo resultado.
5. **Incidentes**: qué hacer ante fuga, sospecha o hallazgo.
6. **Consecuencias**: incumplimientos y medidas.
7. **Vigencia y revisión**: fecha de revisión anual.

> **Nota para el RSI:** completar la plantilla ISACA-02 con el caso Banco, firmarla y comunicarla a los 300 funcionarios es evidencia directa de gobierno (GV-01/GV-02) y de concienciación (A.6.3).

---

## 3. Evaluación de impacto (EIPD) y registro de tratamientos

### Cuándo se necesita un EIPD (PD.7, Ley 19.670)

Cuando el uso de IA involucra **datos personales** (aunque sean anonimizados parcialmente) o datos sensibles. El EIPD documenta:

- Qué datos se tratan y con qué base legal.
- Qué herramienta se usa y dónde se procesa.
- Qué riesgos existen para los titulares (fuga, acceso indebido, sesgo).
- Qué medidas de mitigación se implementan.
- Quién aprueba y con qué vigencia.

### Registro de bases de datos (Ley 18.331 art. 22)

Si un uso de IA con datos personales configura una base de datos, debe estar **registrada ante la URCDP** (o justificar su inscripción en el registro institucional). La herramienta local (BigPickle/Ollama) que procesa documentos internos con datos debe estar reflejada en el Documento de Seguridad.

---

## 4. La auditoría del uso de IA: cómo se hace

### Qué auditar

| Área | Qué revisar |
|---|---|
| Inventario | ¿Qué herramientas de IA existen y están todas autorizadas? |
| Política | ¿Está aprobada, vigente y comunicada? |
| Datos | ¿Qué datos ingresan a las herramientas? ¿Se respeta la clasificación? |
| Accesos | ¿Quién tiene acceso y con qué permiso? ¿Roles coherentes? |
| Logs | ¿Existen registros de uso? ¿Se revisan? |
| RAG | ¿Qué documentos están indexados? ¿Están clasificados y vigentes? |
| Incidentes | ¿Hubo hallazgos? ¿Se investigaron y documentaron? |
| Capacitación | ¿El personal fue capacitado y firmó la política? |

### Cómo se presenta la evidencia

Siguiendo el formato de evidencia del kit (MATRIZ-002, EV-01 a EV-05): para cada requisito (PD.x, CN.x, EMG, ISO 27001) se indica **evidencia / cómo presentarla / área responsable / rol / justificación**.

---

## 5. Matriz de evidencia del uso de IA (ejemplo)

| Requisito | Evidencia | Cómo presentarla | Área responsable |
|---|---|---|---|
| PD.1 Legalidad | EIPD aprobado y base legal documentada | Documento firmado por RSI y DPD | Cumplimiento |
| PD.5 Seguridad | Configuración DLP + logs + bloqueo de dominios | Capturas de configuración y reportes | TI |
| PD.6 Reserva | Contratos con proveedores (si hay nube) | Contratos firmados | Compras |
| PD.7 Proactividad | EIPD + política aprobada | Política firmada | RSI |
| CN.1 Cumplimiento | Matriz de correspondencia de IA | MATRIZ (este kit) | RSI |
| A.6.3 Concienciación | Registro de capacitación de 300 funcionarios | Planillas firmadas | RRHH |
| A.8.12 DLP | Reglas DLP activas y reporte de bloqueos | Reportes de DLP | TI |
| RS-02 Incidentes | Registro de incidentes de IA | Reportes y cierre | RSI |

---

## 6. Indicadores de gobierno (para reportar a dirección)

| Indicador | Qué mide |
|---|---|
| % de herramientas de IA autorizadas | Control del inventario |
| Nº de accesos bloqueados a IA externa (DLP) | Eficacia del control de fuga |
| Nº de hallazgos de shadow IA | Riesgo residual |
| % de personal capacitado | Concienciación |
| Tiempo de respuesta a incidentes de IA | Capacidad de respuesta |
| % de respuestas con revisión humana registrada | Adhesión al proceso |

---

## 7. El ciclo de mejora continua (PDCA aplicado a la IA)

1. **Planificar**: política, EIPD, inventario, capacitación.
2. **Hacer**: desplegar herramientas, aplicar reglas, capacitar.
3. **Verificar**: monitorear logs, revisar DLP, auditar, medir indicadores.
4. **Actuar**: corregir hallazgos, retirar herramientas no autorizadas, actualizar política.

---

## 8. Conclusión del módulo

- El gobierno de la IA se sostiene en **política, roles, EIPD, registro de tratamientos y auditoría**.
- La **evidencia** (política firmada, logs, DLP, capacitación, incidentes) es lo que responden ante URCDP, BCU y Agesic.
- El ciclo **planificar-hacer-verificar-actuar** garantiza que la IA se use bien y se siga usando bien.
- Sin gobierno, la IA es un riesgo; con gobierno, es una ventaja operativa controlada.

> **Ejercicio (RSI):** Use la plantilla `templates-ISACA\02-AI-Acceptable-Use` y redacte la política de IA del Banco Ficticio. Luego arme la matriz de evidencia (tabla del punto 5) con las áreas responsables de su institución.
