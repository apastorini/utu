# VPOL-11 · Data Backup Policy

> **Función del MCU 5.0:** Recuperar (RC.RP — ejecutar planes de recuperación) · Proteger (PR.DS — respaldo)
> **ISO/IEC 27001:** A.8.13 (respaldos de la información) · A.8.14 (redundancia) · A.12.3
> **BCU:** EMG y RNRCSF — continuidad del negocio y recuperación de datos críticos
> **URCDP:** Ley 18.331 art. 10 — pérdida o destrucción de datos personales como vulneración notificable
> **Nivel del curso:** 🟡 Practicar

---

### ENCABEZADO
| **Campo** | **Valor** |
|---|---|
| **Código** | VPOL-11 |
| **Título** | Data Backup |
| **Versión** | 1.0 |
| **Estado** | [Borrador / En revisión / Aprobado] |
| **Fecha de aprobación** | [COMPLETAR] |
| **Elaborado por** | Div. TI (Respaldos) + RSI |
| **Revisado por** | Jefe de Producción · BCU (continuidad) |
| **Aprobado por** | Comité de Seguridad de la Información |
| **Clasificación** | Uso interno |
| **Próxima revisión** | [Fecha, máx. 1 año] |

### 1. Objetivo
Garantizar que la información crítica del Banco esté **respaldada, protegida y recuperable** dentro de los objetivos de tiempo (RTO) y de pérdida de datos (RPO) definidos, ante fallos, desastres, ataques (incluido ransomware) o errores humanos.

### 2. Alcance
Aplica a todas las plataformas, bases de datos, aplicaciones, archivos compartidos, correo, configuraciones de red/seguridad y, cuando corresponda, a los datos críticos de los sistemas en nube (ver VPOL-10).

### 3. Clasificación de datos y niveles de respaldo
| Nivel | Tipo de dato | Frecuencia de respaldo | RPO | RTO |
|---|---|---|---|---|
| **Crítico** | Core bancario, sistema de pagos, Banco En Línea, base de clientes | [COMPLETAR: p. ej. continuo / horario] | [COMPLETAR: p. ej. 15 min] | [COMPLETAR: p. ej. 4 h] |
| **Alto** | Aplicaciones de negocio, archivos de áreas | Diario | 24 h | [COMPLETAR] |
| **Medio** | Documentación interna | Semanal | 7 días | [COMPLETAR] |
| **Bajo** | Información pública | Mensual | 30 días | [COMPLETAR] |

### 4. Reglas de respaldo
- Estrategia **3-2-1** (mínimo): 3 copias, en 2 medios/soportes distintos, 1 copia **off-site** (fuera del CPD principal).
- Los respaldos se **cifran** (PR-03) y las copias off-site se protegen contra acceso no autorizado.
- **Inmutabilidad/anti-ransomware** para copias críticas: retención que impida la alteración o borrado por un atacante.
- **Prueba de restauración periódica**: [COMPLETAR: p. ej. mensual para críticos, trimestral para el resto], documentada.
- Monitoreo diario del éxito de los respaldos y **alerta ante fallas** (SIEM/DE-01).
- Los respaldos que contengan **datos personales** se gestionan bajo la Ley 18.331 (acceso, retención y eliminación).

### 5. Responsabilidades
- **Div. TI (Respaldos):** ejecuta, monitorea y prueba.
- **RSI:** valida el cumplimiento y el cifrado de las copias.
- **Comité de Continuidad (RC):** revisa RTO/RPO y los ejercicios de recuperación.
- **DPD:** supervisa los respaldos que contienen datos personales.

### 6. Incumplimiento y revisión
Toda falla de respaldo no resuelta se informa como **incidente de continuidad**. Revisión anual o ante cambios de infraestructura.

### Evidencia del kit
| Evidencia | Documento canónico |
|---|---|
| Logs de respaldo y pruebas de restauración | PR-05, RC-02 |
| Objetivos RTO/RPO definidos | BCU-02 (continuidad) |
| Cifrado de copias | PR-03 |
| Ejercicios de recuperación | RC-02 |
