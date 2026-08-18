# PRO-04 · Procedimiento: Respuesta ante Incidentes de Seguridad

> **Función del MCU 5.0:** Responder (RS.RP — respuesta) · Recuperar (RC.RP — recuperación)
> **ISO/IEC 27001:** A.5.24-A.5.28 (gestión de incidentes)
> **BCU:** EMG / RNRCSF — gestión de incidentes cibernéticos con reporte al supervisor
> **URCDP:** Ley 18.331 art. 12 y Decreto 64/020 — notificación de vulneraciones de datos personales en 72 h
> **Nivel del curso:** 🔴 Dominar

---

## 1. Objetivo y alcance
Detectar, contener, erradicar y recuperar los incidentes de seguridad con rapidez y trazabilidad, minimizando el impacto. Aplica a todo incidente que afecte la confidencialidad, integridad o disponibilidad de la información y los sistemas del Banco, incluido el entorno de IA.

## 2. Responsables
- **Todo el personal**: reporta al detectar o sospechar un incidente.
- **Mesa de Ayuda**: primer punto de contacto y registro.
- **RSI (CERT interno)**: investiga, contiene y gestiona.
- **Comité de Incidentes**: decisiones de comunicación y escalamiento.
- **DPD**: evalúa y ejecuta la notificación a la URCDP si hay datos personales.

## 3. Entradas
- Reporte inicial (teléfono, correo, ticket, alerta de monitoreo).
- Evidencia inicial (correos, capturas, logs, muestras).
- Procedimiento de monitoreo (POL-06).

## 4. Clasificación de incidentes
| Nivel | Ejemplo | Respuesta |
|---|---|---|
| **Leve** | Correo phishing no abierto, alerta falsa | Registro y cierre |
| **Moderado** | Equipo infectado, cuenta comprometida | Contención y análisis |
| **Grave** | Ransomware, fuga de datos, acceso no autorizado a sistemas críticos | Respuesta completa, escalamiento a Dirección y BCU |
| **Crítico** | Indisponibilidad de servicios esenciales, impacto a clientes | Crisis + comunicación externa |

## 5. Desarrollo paso a paso (fases)

### 5.1 Detección y reporte (RS.RP)
1. Cualquier persona reporta el incidente al **RSI/Mesa de Ayuda** con: qué pasó, cuándo, dónde y qué evidencia hay.
2. El RSI registra el incidente en el **registro de incidentes** (RS-01) y asigna un nivel.
3. Se **preserva la evidencia** (no apagar el equipo, no borrar logs).

### 5.2 Contención (RS.RP)
4. Se **aísla** lo afectado: desconexión de red, bloqueo de cuentas, revocación de accesos, bloqueo de dominios de correo malicioso.
5. Se notifica a los responsables de sistemas afectados.

### 5.3 Erradicación y análisis
6. Se elimina la causa raíz (malware, acceso, configuración).
7. El RSI analiza logs, correos y evidencia para determinar **alcance y causa raíz**.
8. Si hay **datos personales** involucrados, se evalúa el riesgo para los titulares con el DPD.

### 5.4 Notificación y comunicación
9. **A la URCDP**: si la vulneración presenta riesgo para los derechos de los titulares, se notifica en **72 horas** (Decreto 64/020) con el contenido definido en PRO-05.
10. **Al BCU**: incidentes cibernéticos relevantes se reportan según el RNRCSF y la normativa vigente.
11. **Interna**: comunicación a Dirección y Comité según la gravedad.

### 5.5 Recuperación (RC.RP)
12. Se restaura con **respaldos limpios** (POL-08), verificando que no queden rastros.
13. Se valida el funcionamiento y se vigila por recaídas.

### 5.6 Lecciones aprendidas
14. Se documenta el incidente: línea de tiempo, causa raíz, acciones y lecciones.
15. Se definen **planes de acción** (mejoras de controles) con responsable y fecha.
16. Se comunica la lección al personal (POL-09, PRO-12).

## 6. Salidas y registros
- Registro de incidente completo (RS-01).
- Informe de incidente (causa raíz, impacto, lecciones).
- Notificación a URCDP/BCU si corresponde.
- Plan de acción de mejoras.

## 7. Errores comunes
- No reportar por temor o por "resolver rápido".
- Apagar equipos y perder evidencia.
- Comunicar sin confirmar datos.
- No aprender de los incidentes previos.

## 8. Referencias
POL-07 (Plan de respuesta) · POL-06 (Monitoreo) · PRO-05 (Notificación) · POL-05 (Malware) · PCS-05.

## 9. Evidencia
Registro de incidentes, informes, notificaciones. Alimenta: RS-01, ID-02, cumplimiento BCU y URCDP.
