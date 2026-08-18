# PCS-08 · Proceso de Protección de Datos Personales

> **Función del MCU 5.0:** Cumplimiento normativo (CN) · Protección de datos personales (PD.1…PD.8)
> **ISO/IEC 27001:** A.5.34 (protección de datos personales) · A.5.35 (revisión independiente) · A.5.31-A.5.32 (requisitos legales)
> **BCU:** EMG — gobierno de la información y protección de los datos de clientes
> **URCDP:** Ley 18.331, Decreto 414/009, Decreto 64/020, Ley 19.670 — marco central
> **Nivel del curso:** 🔴 Dominar
> **Ejecuta:** POL-20 (y POL-17 para IA)

---

## 1. Objetivo y alcance
Garantizar que todo **tratamiento de datos personales** cumpla los principios de la Ley 18.331 y los requisitos PD.1-PD.8 del MCU 5.0, protegiendo los derechos de los titulares. Aplica a clientes, empleados, proveedores, visitantes y terceros, en cualquier soporte y medio (incluida la IA).

## 2. Entradas
- Inventario de bases de datos y tratamientos (URCDP-01).
- Solicitudes de derechos (ARCO) de los titulares.
- Nuevas iniciativas que traten datos (proyectos, sistemas, IA, proveedores).
- Incidentes que comprometan datos personales (PCS-03).

## 3. Actividades numeradas

**3.1 — Registrar los tratamientos de datos.**
- **Responsable:** DPD con dueños de bases.
- **Pasos:** (a) mantener el inventario de bases de datos y tratamientos, (b) verificar la base legal de cada tratamiento (consentimiento, ley, contrato), (c) inscribir ante la URCDP lo que corresponda.
- **Salida:** Inventario y registro URCDP actualizados.
- **Plazo:** Al crear cada tratamiento y revisión anual.

**3.2 — Verificar principios y minimización.**
- **Responsable:** DPD con dueños de bases.
- **Pasos:** (a) revisar finalidad, exactitud y necesidad de cada dato recogido, (b) aplicar minimización y anonimización en pruebas/IA (POL-17), (c) corregir desvíos.
- **Salida:** Tratamientos alineados a los principios.
- **Plazo:** En la revisión anual y en cada nuevo tratamiento.

**3.3 — Gestionar el consentimiento.**
- **Responsable:** DPD + áreas de negocio.
- **Pasos:** (a) recoger el consentimiento previo, expreso e informado, (b) documentar y permitir la revocación, (c) aplicar las restricciones para datos sensibles (Decreto 414/009).
- **Salida:** Registro de consentimientos y revocaciones.
- **Plazo:** Al captar datos y al recibir revocaciones.

**3.4 — Atender los derechos de los titulares (ARCO).**
- **Responsable:** DPD (oficina de atención al titular).
- **Pasos:** (a) recibir y registrar la solicitud, (b) verificar la identidad, (c) responder dentro del plazo legal (acceso, rectificación, inclusión, supresión, impugnación), (d) registrar la respuesta.
- **Salida:** Respuesta al titular dentro del plazo.
- **Plazo:** Plazos legales (Decreto 414/009); registro de cada solicitud.

**3.5 — Evaluar el impacto (EIPD).**
- **Responsable:** DPD con RSI.
- **Pasos:** (a) identificar tratamientos de alto riesgo (masivos, sensibles, IA, transferencias), (b) realizar la EIPD antes del inicio (Ley 19.670), (c) definir medidas y aprobar.
- **Salida:** EIPD documentada y aprobada (URCDP-04).
- **Plazo:** Antes de iniciar tratamientos de alto riesgo.

**3.6 — Gestionar incidentes y notificaciones.**
- **Responsable:** DPD con RSI.
- **Pasos:** (a) participar en la evaluación del incidente (PCS-03), (b) decidir y ejecutar la notificación a la URCDP en 72 h (PRO-05), (c) comunicar a los titulares si hay alto riesgo, (d) registrar.
- **Salida:** Notificaciones emitidas y registradas.
- **Plazo:** 72 h desde el conocimiento.

**3.7 — Supervisar proveedores y transferencias.**
- **Responsable:** DPD.
- **Pasos:** (a) revisar acuerdos de encargado de tratamiento (PCS-07), (b) verificar las transferencias internacionales (POL-19), (c) exigir garantías.
- **Salida:** Acuerdos y transferencias revisados.
- **Plazo:** En cada contratación y revisión anual.

## 4. Salidas
- Inventario de tratamientos y registro URCDP.
- Registro de consentimientos y respuestas ARCO.
- EIPD realizadas.
- Notificaciones de vulneraciones registradas.

## 5. Responsables del proceso
| Rol | Función |
|---|---|
| **DPD** | Coordina el proceso, interlocutor con URCDP |
| **RSI** | Implementa los controles de seguridad |
| **Dueños de bases** | Mantienen la calidad y finalidad de sus datos |
| **Áreas de negocio** | Captan consentimiento y atienden titulares |
| **Comité de Datos** | Supervisa el programa de privacidad |

## 6. Indicadores (KPIs)
- % de tratamientos con base legal verificada (meta 100%).
- % de solicitudes ARCO respondidas dentro del plazo (meta 100%).
- % de EIPD obligatorias realizadas antes del inicio (meta 100%).
- Nº de notificaciones a la URCDP y su plazo de cumplimiento.

## 7. Registros que deja
- Inventario de tratamientos y registro URCDP.
- Solicitudes ARCO y respuestas.
- EIPD y notificaciones.

## 8. Referencias
POL-20 · POL-17 · PRO-05 · PRO-09 · PCS-03 · PCS-07.

## 9. Evidencia en el kit
URCDP-01 (inventario) · URCDP-02 (registro) · URCDP-03 (notificaciones) · URCDP-04 (EIPD) · URCDP-05 (encargados).
