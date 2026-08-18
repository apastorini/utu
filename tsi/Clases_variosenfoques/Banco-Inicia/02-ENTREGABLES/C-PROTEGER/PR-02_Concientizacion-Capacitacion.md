# PR-02 · Programa de Concientización y Capacitación en Seguridad del Banco

> ⚠️ **Alerta:** este documento menciona **nombres propios del organigrama del Banco** (personas y cargos, abril 2026). Antes de usar el documento, verificá la vigencia de esos nombres contra el organigrama actual.
> **Función del MCU 5.0:** Proteger (PR.AT — Concientización y capacitación)
> **ISO/IEC 27001:** A.6.3 (Concientización, educación y formación sobre seguridad de la información)
> **BCU:** Estándares Mínimos de Gestión — Gobierno; Circular 2227 (riesgo operativo)
> **URCDP:** Ley 18.331 art. 29 (capacitar al personal que trata datos personales) · Decreto 64/020
> **Nivel del curso:** 🟢 Descubrir · 🟡 Practicar

## 1. Qué es y por qué existe
Las personas son, a la vez, el eslabón más débil y la primera línea de defensa de la ciberseguridad. La gran mayoría de los incidentes que afectan a bancos uruguayos y del mundo comienza con un correo de **phishing**, una contraseña débil, un dispositivo extraviado o un funcionario que comparte información sin verificar a quién. Ninguna tecnología de protección reemplaza a un funcionario que sabe qué hacer (y qué no hacer) antes de que ocurra el incidente.
Esta política establece el **programa permanente** de concientización y capacitación del Banco: quiénes deben capacitarse, sobre qué temas, con qué frecuencia, con qué metodologías y —lo más importante— cómo se mide si la capacitación **cambió el comportamiento**. La URCDP exige expresamente (art. 29 de la Ley 18.331) que los responsables de bases de datos capaciten a su personal; el BCU espera ver evidencia de que la función de seguridad forma a la organización.
En el Banco, la capacitación debe llegar a todos los perfiles: cajeros y oficiales de crédito en sucursal (que tratan datos personales a diario), analistas de crédito, personal del sistema de pagos, administradores de sistemas y gerentes. Cada grupo necesita un contenido y un nivel de profundidad acordes a su exposición al riesgo.
## 2. Marco de referencia
| **Referencia** | **Requisito aplicable** |
|---|---|
| **MCU 5.0 (Agesic)** | PR.AT — concientización y capacitación del personal y terceros según sus funciones; medición de la eficacia |
| **ISO/IEC 27001:2022** | A.6.3 concientización, educación y formación; A.6.2 condiciones de contratación (competencias) |
| **BCU** | EMG · Gobierno (la función de seguridad forma a la organización); Circular 2227 (riesgo operativo) |
| **URCDP** | Ley 18.331 art. 29 (capacitación del personal que trata datos personales); Decreto 64/020 |

## 3. Cómo completar esta plantilla (guía de llenado)
1. **Completá el encabezado** (código, versión, fecha). La aprueba el Comité de Seguridad de la Información.
2. **Coordiná con División Capital Humano** (Jefe de Desarrollo de RRHH, Ing. Cecilia Cabrera): ellos poseen la plataforma de e-learning y los registros de asistencia del personal.
3. **Definí el plan anual de capacitación** con el RSI y el DPD (los contenidos de datos personales los revisa el DPD).
4. **Personalizá los apartados [COMPLETAR]** con los temas, frecuencias y metas concretas del año.
5. **Establecé los indicadores de eficacia** (porcentaje de aprobación, tasa de caída en simulacros de phishing) y definí quién los reporta (RSI al Comité, semestral).
6. **Aprobá, registrá en el control de cambios** y publicá en `02-ENTREGABLES/C-PROTEGER`. Revisá anualmente o ante incidentes de factor humano relevantes.
## 4. Plantilla del documento

### ENCABEZADO
| **Campo** | **Valor** |
|---|---|
| **Código** | PR-02 |
| **Título** | Programa de Concientización y Capacitación en Seguridad |
| **Versión** | 1.0 |
| **Estado** | [Borrador / En revisión / Aprobado] |
| **Fecha de aprobación** | [COMPLETAR] |
| **Elaborado por** | RSI |
| **Revisado por** | DPD · Div. Capital Humano · Comité de Seguridad |
| **Aprobado por** | Comité de Seguridad de la Información |
| **Clasificación** | Uso interno |
| **Próxima revisión** | [Fecha, máx. 1 año] |

### 1. Objetivo
Desarrollar y mantener las **competencias de seguridad de la información** de todos los funcionarios del Banco y de los terceros que presten servicios en sus instalaciones, y medir el impacto de la formación en el comportamiento real.
### 2. Alcance
Aplica a [COMPLETAR: todos los funcionarios del Banco, incluidos gerentes y dirección; contratistas, pasantes y proveedores con acceso a sistemas o información del banco; funcionarios nuevos desde su ingreso]. Incluye las modalidades presencial, virtual y los simulacros.
### 3. Público objetivo y frecuencia mínima
| **Público** | **Contenido mínimo** | **Frecuencia mínima** |
|---|---|---|
| **Todos los funcionarios** | Phishing, contraseñas, datos personales, dispositivos, reporte de incidentes | Anual (obligatorio) + refuerzos |
| **Personal que trata datos personales** (sucursales, crédito, cobranzas) | URCDP, secreto bancario, derechos ARCO, manejo de datos | Anual + refuerzo específico |
| **Personal de TI y del sistema de pagos** | Seguridad en sistemas, parches, gestión de accesos, monitoreo | Semestral |
| **Gerentes y jefes** | Gobierno de la seguridad, riesgos, rol de liderazgo | Anual |
| **Terceros y contratistas** | Reglas de la política PR-01 y confidencialidad | Al ingreso y anual |

### 4. Temas del programa
a) **Ingeniería social y phishing:** cómo reconocer correos, enlaces y llamadas fraudulentas.
b) **Contraseñas y autenticación:** buenas prácticas, MFA, uso individual de credenciales.
c) **Datos personales:** principio de confidencialidad, secreto bancario, base legal, derechos del titular.
d) **Dispositivos y estaciones de trabajo:** escritorio limpio, bloqueo de pantalla, equipos móviles, memorias USB.
e) **Incidentes:** qué reportar, a quién y cuándo (RS-01).
f) **Teletrabajo y acceso remoto:** VPN, lugares de trabajo, dispositivos personales.
### 5. Metodologías
- **Curso e-learning** obligatorio anual con evaluación final (aprobación mínima [COMPLETAR: 80%]).
- **Inducción de seguridad** para nuevos ingresos (antes del alta de accesos).
- **Simulacros de phishing** periódicos (cada [COMPLETAR: 3 meses]) sobre cuentas institucionales.
- **Charlas y talleres** presenciales por área y campañas de comunicación interna.
- **Comunicados y afiches** en sucursales y en la intranet.
### 6. Medición de eficacia
| **Indicador** | **Meta sugerida** | **Frecuencia de reporte** |
|---|---|---|
| % de funcionarios que completan la capacitación anual | [COMPLETAR: ≥ 95%] | Trimestral |
| Tasa de caída en simulacros de phishing | [COMPLETAR: < 10%] | Trimestral |
| % de aprobación del curso | [COMPLETAR: ≥ 80%] | Anual |
| Horas de capacitación por persona | [COMPLETAR] | Anual |
| Tiempo de reporte de phishing (correos reenviados al RSI) | [COMPLETAR] | Trimestral |

### 7. Responsabilidades
| **Rol** | **Responsabilidad** |
|---|---|
| **RSI** | Diseñar, coordinar, ejecutar simulacros y reportar indicadores al Comité |
| **Div. Capital Humano** | Plataforma, registro de asistencia, inducción, coordinación de horarios |
| **DPD** | Contenidos de protección de datos personales |
| **Jefes de departamento** | Garantizar la asistencia de sus equipos y el refuerzo local |
| **Comité de Seguridad** | Aprobar el plan anual y evaluar los resultados |

### 8. Control de cambios
| **Versión** | **Fecha** | **Cambio** | **Elaboró** | **Aprobó** |
|---|---|---|---|---|
| 0.1 | [COMPLETAR] | Versión inicial (borrador) | RSI | — |
| 1.0 | [COMPLETAR] | Aprobación del Comité | RSI | Comité |

## 5. Ejemplo aplicado al Banco (modelo de referencia)
Ejemplo ilustrativo de cómo quedaría el apartado 4 completado. Adaptá al contenido institucional real del Banco.
**Plan anual (ejemplo):**
- **Febrero:** inducción de nuevos ingresos (Banco En Línea, sucursales y Div. TI) con módulo de seguridad de 2 horas y acuse de la Política de Seguridad.
- **Marzo–noviembre:** cuatro campañas de **simulacro de phishing** con plantillas que imitan comunicaciones internas del Banco ("cambio de política", "nómina", "notificación de correo"). En la primera campaña cayó el 14 % de los funcionarios; tras refuerzos específicos a sucursales, la última campaña bajó al 6 %.
- **Junio:** curso e-learning anual obligatorio "Seguridad de la Información y Protección de Datos" (90 minutos), con módulo específico de secreto bancario para el personal de sucursales y del sistema de pagos.
- **Setiembre:** taller presencial para Div. TI sobre gestión segura de accesos y parches, coordinado con PR-06.
- **Diciembre:** informe del RSI al Comité con indicadores: 97 % de cobertura, 6 % de caída en phishing, 88 % de aprobación. Se aprobó profundizar el módulo de datos personales para 2027 por solicitud del DPD.
**Medición de eficacia (ejemplo):**
- Los funcionarios que cayeron en dos simulacros consecutivos reciben **capacitación remedial obligatoria** antes del próximo ciclo.
- Los resultados por área se comparten con los jefes de departamento (sin individualizar) para focalizar refuerzos en sucursales con mayor tasa de caída.

**Documentos relacionados:** GV-01 (Política de Seguridad), GV-03 (Roles y Comité), PR-01 (Control de Acceso), RS-01 (Incidentes), URCDP-01 (Documento de Seguridad de Datos), PR-08 (Terceros).
