# POL-20 · Política de Protección de Datos Personales

> **Función del MCU 5.0:** Cumplimiento normativo (CN) · Protección de datos personales (PD.1 … PD.8) — dominio transversal completo
> **ISO/IEC 27001:** A.5.34 (protección de datos personales) · A.5.35 (revisión) · A.5.31-A.5.32 (requisitos legales)
> **BCU:** EMG — gobierno de la información y protección de los datos de clientes
> **URCDP:** Ley 18.331, Decreto 414/009, Decreto 64/020, Ley 19.670 — marco central de protección de datos personales en Uruguay
> **Nivel del curso:** 🔴 Dominar

---

### ENCABEZADO
| **Campo** | **Valor** |
|---|---|
| **Código** | POL-20 |
| **Título** | Protección de Datos Personales |
| **Versión** | 1.0 |
| **Estado** | [Borrador / En revisión / Aprobado] |
| **Fecha de aprobación** | [COMPLETAR] |
| **Elaborado por** | DPD + RSI |
| **Revisado por** | Comité de Seguridad · Comité de Datos · Legales |
| **Aprobado por** | Dirección General |
| **Clasificación** | Confidencial |
| **Próxima revisión** | [Fecha, máx. 1 año] |

### 1. Objetivo
Garantizar que todo **tratamiento de datos personales** realizado por el Banco respete la **Ley 18.331** y su reglamentación, y los requisitos **PD.1-PD.8** del MCU 5.0, protegiendo los derechos de los titulares.

### 2. Alcance
Aplica a todo dato personal tratado por el Banco: clientes, empleados, proveedores, visitantes y terceros, en cualquier formato y por cualquier medio (sistemas, papel, correo, nube, IA, terceros).

### 3. Principios del tratamiento (Ley 18.331 art. 9 y MCU 5.0 PD)
| Principio | Requisito PD | Qué implica |
|---|---|---|
| **Legalidad** | PD.1 | Toda base de datos se ampara en una base legal (consentimiento, ley, contrato) |
| **Veracidad / calidad** | PD.2 | Los datos son exactos, completos y actualizados |
| **Finalidad** | PD.3 | Los datos se usan solo para la finalidad declarada |
| **Consentimiento** | PD.4 | Previo, expreso, informado y revocable (Decreto 414/009); refuerzo para datos sensibles |
| **Seguridad** | PD.5 | Medidas técnicas y organizativas; notificación de vulneraciones en 72 h (Decreto 64/020) |
| **Reserva** | PD.6 | Confidencialidad de quienes tratan datos |
| **Responsabilidad proactiva** | PD.7 | EIPD y privacidad por diseño (Ley 19.670) |
| **Derechos del titular** | PD.8 | Información, acceso, rectificación, inclusión, supresión, impugnación; respuesta en plazos legales |

### 4. Reglas obligatorias
- **Registro de bases de datos**: se mantiene el registro de tratamientos (Ley 18.331 art. 22) y se inscribe ante la URCDP cuando corresponde.
- **Consentimiento**: se obtiene, se documenta y se puede revocar; para datos sensibles el tratamiento es restringido (Decreto 414/009).
- **Minimización**: se recoge solo lo necesario; en pruebas y en IA se usa **anonimización** (POL-17, curso AISEC-06).
- **Derechos (ARCO)**: el Banco responde los pedidos en los plazos legales (5 días hábiles según el Decreto 414/009, según el caso) con procedimiento definido (PRO-09/PCS-08).
- **Seguridad**: los datos se protegen con los controles de todas las políticas del kit (accesos, cifrado, respaldos, monitoreo).
- **Incidentes**: toda vulneración se notifica a la URCDP en **72 horas** cuando haya riesgo para los titulares (PRO-05).
- **Terceros**: los encargados de tratamiento firman acuerdo y cumplen las garantías (POL-11).
- **Transferencias internacionales**: se verifican las condiciones legales antes de enviar datos al exterior (POL-19, nube).
- **IA**: las herramientas que tratan datos personales se rigen por la POL-17 y el curso AISEC.

### 5. Responsabilidades
- **DPD**: supervisa el cumplimiento, atiende a la URCDP, impulsa EIPD.
- **RSI**: implementa los controles de seguridad.
- **Dueños de bases**: aseguran la calidad y finalidad de sus tratamientos.
- **Todo el personal**: cumple los principios y reporta incidentes.

### 6. Cumplimiento y revisión
El incumplimiento expone al Banco a sanciones de la URCDP (Ley 18.331 art. 39). Revisión anual de la política y del inventario de tratamientos; EIPD ante nuevos usos.

### Evidencia del kit
| Evidencia | Documento canónico |
|---|---|
| Inventario de bases y tratamientos | URCDP-01 |
| Registro ante la URCDP | URCDP-02 |
| Procedimiento de derechos ARCO | PRO-09 |
| Procedimiento de notificación | PRO-05 |
| EIPD | URCDP-04 |
| Acuerdos de encargado de tratamiento | POL-11 |
