# RC-02 · Plan de Recuperación ante Desastres (DRP) del Banco

> ⚠️ **Alerta:** este documento menciona **nombres propios del organigrama del Banco** (personas y cargos, abril 2026). Antes de usar el documento, verificá la vigencia de esos nombres contra el organigrama actual.
> **Función del MCU 5.0:** Recuperar (RC.RP — Planificación de la recuperación)
> **ISO/IEC 27001:** A.8.13 (Respaldo de la información)
> **BCU:** **RNRCSF art. 492 (resguardo de datos)** · Estándares Mínimos de Gestión — Continuidad
> **URCDP:** Ley 18.331 art. 10 · Decreto 64/020
> **Nivel del curso:** 🔴 Dominar

## 1. Qué es y por qué existe
El **Plan de Recuperación ante Desastres (DRP)** define cómo el Banco recupera sus **sistemas y datos** cuando un evento de gran escala los destruye o los inutiliza: un incendio o inundación del centro de cómputos, un ciberataque destructivo (ransomware que cifra todo), un corte mayor de energía o un fallo catastrófico del proveedor. Complementa al BCP (RC-01): el BCP dice cómo sigue el negocio; el DRP dice cómo se reconstruyen las plataformas.
La normativa es exigente. El **art. 492 de la RNRCSF** (BCU) obliga a mantener resguardos de datos que **no se afecten por el mismo evento** que afecta a los sistemas de producción, a custodiar las **claves de desencriptación** de los resguardos en forma independiente, y a **probar anualmente** la recuperación e integridad de **la totalidad** de los datos resguardados. No basta con tener respaldos: hay que demostrar que se pueden restaurar.
El DRP define el **sitio alternativo de recuperación**, el orden de restauración de los sistemas según su criticidad, los RTO/RPO por sistema, los roles que ejecutan la recuperación y el ciclo de pruebas y simulacros que garantiza que el plan funciona.
## 2. Marco de referencia
| **Norma** | **Referencia** | **Qué exige** |
|---|---|---|
| **MCU 5.0 (Agesic)** | RC.RP | Recuperación dentro de las tolerancias (perfil Avanzado: ≤ 24 h) |
| **ISO/IEC 27001:2022** | A.8.13 | Respaldo de la información conforme a los requisitos acordados |
| **BCU** | **RNRCSF art. 492** · EMG · Continuidad | Resguardos no afectados por el mismo evento; claves independientes; **prueba anual de recuperación e integridad de la totalidad** |
| **URCDP** | Ley 18.331 art. 10 | Disponibilidad y recuperación de los datos personales |

## 3. Cómo completar esta plantilla (guía de llenado)
1. **Definí qué es un desastre** con el RSI y la División TI: umbrales de interrupción (ej. > X horas o > Y sistemas críticos) y criterios de declaración.
2. **Definí el sitio alternativo** con la División TI: sitio propio, nube o contrato con tercero; verificá que cumpla el art. 492 (no afectado por el mismo evento).
3. **Documentá el orden de recuperación** con los Jefes de Producción y Sistemas (Ing. Daniel Herrera, Lic. Cristian Palo) según criticidad (core, pagos, banca, sucursales).
4. **Validá el resguardo de claves** con el RSI y Legal: claves de desencriptación custodiadas en lugar independiente y con acceso controlado.
5. **Programá las pruebas anuales** de recuperación e integridad de la totalidad de los datos, con informe de resultados.
6. Consultá al **Oficial de Cumplimiento** y al **Jefe de Riesgos No Financieros** (Cra. Melissa Moraes) para alinear con los requisitos BCU y el apetito de riesgo.
## 4. Plantilla del documento

### ENCABEZADO
| **Campo** | **Valor** |
|---|---|
| **Código** | RC-02 |
| **Título** | Plan de Recuperación ante Desastres (DRP) |
| **Versión** | 1.0 |
| **Estado** | [Borrador / En revisión / Aprobado] |
| **Fecha de aprobación** | [COMPLETAR] |
| **Elaborado por** | RSI |
| **Revisado por** | Gerente División TI · Comité de Seguridad |
| **Aprobado por** | Directorio |
| **Clasificación** | Confidencial |
| **Próxima revisión** | [Fecha, máx. 1 año] |

### 1. Objetivo
Recuperar los sistemas y datos del Banco ante un desastre, dentro de los RTO/RPO aprobados, cumpliendo el art. 492 de la RNRCSF y garantizando la integridad de la información restaurada.
### 2. Definición de desastre
Se declara desastre cuando [COMPLETAR: la interrupción supera X horas de los sistemas críticos, el centro de cómputos queda inutilizado, o la decisión la toma el Comité de Crisis]. La declaración la formaliza el Comité y activa este plan junto con RC-01.
### 3. Sitio alternativo de recuperación
| **Ítem** | **Valor** |
|---|---|
| Ubicación | [COMPLETAR: sitio propio / nube / tercero] |
| Distancia del sitio primario | [COMPLETAR: asegura que no se afecte por el mismo evento] |
| Capacidad | [COMPLETAR: sistemas críticos, volumen de datos] |
| Conectividad | [COMPLETAR: enlaces y redundancia] |
| Equipo de recuperación | [COMPLETAR: integrantes, plazos de llegada] |

### 4. Recuperación de resguardos de datos (art. 492 RNRCSF)
- Los resguardos de datos se conservan en soportes que **no se afecten por el mismo evento** que afecta a los sistemas de producción [COMPLETAR: sitio/medios].
- Las **claves de desencriptación** se custodian en forma **independiente** y bajo control del [COMPLETAR: RSI + un segundo custodio], con acceso registrado.
- Se realizan **pruebas anuales de recuperación e integridad de la totalidad** de los datos resguardados, con informe firmado [COMPLETAR: por el RSI y la División TI].
### 5. Orden de recuperación de sistemas
| **Orden** | **Sistema** | **RTO** | **RPO** | **Responsable** |
|---|---|---|---|---|
| 1 | [COMPLETAR: Core bancario / base de datos principal] | [COMPLETAR: 8 h] | [COMPLETAR: 15 min] | Div. TI |
| 2 | [COMPLETAR: Sistema de pagos] | [COMPLETAR: 4 h] | [COMPLETAR] | Dpto. Sistema de Pagos |
| 3 | [COMPLETAR: Banco En Línea / banca móvil] | [COMPLETAR: 12 h] | [COMPLETAR] | Div. TI |
| 4 | [COMPLETAR: Canales de sucursal] | [COMPLETAR: 24 h] | [COMPLETAR] | Div. TI |
| 5 | [COMPLETAR: Sistemas administrativos] | [COMPLETAR: 72 h] | [COMPLETAR] | Div. TI |

### 6. Roles de recuperación
| **Rol** | **Titular sugerido** | **Función** |
|---|---|---|
| **Coordinador de recuperación** | Gerente Div. TI | Conduce la ejecución técnica del DRP |
| **Coordinador de continuidad** | RSI | Articula con el BCP (RC-01) y el Comité |
| **Administrador de resguardos** | Dpto. Producción | Monta y verifica los resguardos y su integridad |
| **Administrador de base de datos** | Dpto. Sistemas | Restaura las bases y valida la integridad |
| **Custodio de claves** | RSI + segundo custodio | Provee las claves de desencriptación |
| **Legal / Comunicaciones** | Según RC-03 | Obligaciones legales y comunicación de la crisis |

### 7. Procedimiento de recuperación
7. Declaración de desastre por el Comité de Crisis.
8. Activación del sitio alternativo y del equipo de recuperación.
9. Restauración de los resguardos en el orden definido; desencriptación con las claves custodiadas.
10. Verificación de integridad de la totalidad de los datos (hashes, conteos, conciliaciones).
11. Puesta en producción y verificación funcional por los dueños de proceso (BIA de RC-01).
12. Vuelta al sitio primario cuando esté disponible y se autorice.
### 8. Pruebas y simulacros
[COMPLETAR: prueba anual de recuperación de la totalidad de los datos conforme al art. 492; simulacros parciales por sistema al menos semestrales; y prueba del sitio alternativo]. Cada prueba genera informe con desvíos y plan de acción (RC-04).
### 9. Control de cambios
| **Versión** | **Fecha** | **Cambio** | **Elaboró** | **Aprobó** |
|---|---|---|---|---|
| 0.1 | [COMPLETAR] | Versión inicial (borrador) | RSI | — |
| 1.0 | [COMPLETAR] | Aprobación del Directorio | RSI | Directorio |

## 5. Ejemplo aplicado al Banco (modelo de referencia)
Ejemplo ilustrativo. Adaptá a la operación real del Banco.
**Caso: ransomware que cifra el core (ejemplo):**
- El [fecha] un ataque de ransomware cifra los servidores del core y las bases de clientes. El Comité de Crisis declara desastre y activa el DRP.
- **Sitio alternativo:** se activa el entorno de recuperación en la nube contratada, con réplicas del último resguardo íntegro (RPO objetivo de 15 minutos).
- **Resguardos (art. 492):** los resguardos estaban en bóveda del proveedor de respaldo, no afectada por el ataque; las claves de desencriptación fueron provistas por el custodio independiente (RSI + segundo custodio).
- **Orden de recuperación:** se restauró primero el core y la base de clientes (8 h), luego el sistema de pagos (4 h adicionales), luego Banco En Línea. La verificación de integridad se hizo con conteos y hashes comparados contra el inventario.
- **Prueba anual:** el resultado se comparó con la última prueba anual de recuperación de la totalidad (realizada en el [mes]), que permitió completar la restauración sin improvisar pasos.
- **Resultado:** servicio de banca restablecido en 16 h (dentro del RTO de 24 h del perfil Avanzado del MCU 5.0); informe de lecciones aprendidas en RC-04.

**Documentos relacionados:**
- RC-01 (BCP) · RC-03 (Comunicación de Crisis) · RC-04 (Lecciones Aprendidas)
- PR-05 (Respaldo y Recuperación) · RS-01 (Respuesta a Incidentes)
- BCU-06 (Contingencia y Continuidad) · URCDP-01 (Documento de Seguridad)
