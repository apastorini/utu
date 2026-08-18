# PRO-05 · Procedimiento: Notificación de Vulneraciones de Datos Personales

> **Función del MCU 5.0:** Responder (RS.CO — comunicación) · Cumplimiento (CN)
> **ISO/IEC 27001:** A.5.28 (notificación de incidentes) · A.5.34 (datos personales)
> **BCU:** EMG — notificación de incidentes cibernéticos relevantes al supervisor
> **URCDP:** Ley 18.331 art. 12 y Decreto 64/020 — obligación de notificar a la URCDP en **72 horas** las vulneraciones de datos personales que presenten riesgo para los derechos de los titulares
> **Nivel del curso:** 🔴 Dominar

---

## 1. Objetivo y alcance
Definir cuándo y cómo el Banco **notifica las vulneraciones de datos personales** a la URCDP y, cuando corresponda, a los titulares afectados. Aplica a cualquier incidente que comprometa datos personales (clientes, empleados, otros).

## 2. Responsables
- **DPD**: decide y ejecuta la notificación; interlocutor con la URCDP.
- **RSI**: aporta el análisis técnico del incidente.
- **Comité de Incidentes**: aprueba la estrategia de comunicación.
- **Dirección**: aprueba notificaciones a titulares cuando aplica.

## 3. Cuándo notificar a la URCDP (Decreto 64/020 art. 24)
Se notifica cuando la vulneración de datos personales pueda **presentar un riesgo para los derechos y libertades de los titulares**. En caso de duda, se notifica.

**No se notifica** cuando el riesgo para los titulares es improbable (p. ej., datos públicos, cifrados con clave no comprometida y sin otros datos asociados, o sin efecto probable).

## 4. Desarrollo paso a paso
1. El **RSI** confirma el incidente y, junto al **DPD**, determina si involucra datos personales (PRO-04).
2. El **DPD evalúa el riesgo** para los titulares: tipo de datos, volumen, sensibilidad, posibilidad de uso indebido, mitigaciones aplicadas (cifrado, revocación).
3. **Decisión**: si hay riesgo probable → notificar; si no → documentar la justificación de la no notificación.
4. El **DPD prepara la notificación** con:
   - Descripción de la naturaleza de la vulneración.
   - Categorías y número aproximado de titulares y de registros.
   - Categorías de datos comprometidos.
   - Medidas adoptadas y propuestas para mitigar.
   - Contacto del DPD.
5. La **notificación se envía a la URCDP dentro de las 72 horas** de conocido el incidente; si no hay información completa, se envía una notificación preliminar y se completa después.
6. Si el riesgo para los titulares es **alto**, el Banco **comunica a los titulares** de forma clara y gratuita.
7. Se **registra** la notificación, la justificación y la respuesta de la URCDP.
8. Si corresponde reporte al **BCU** (incidente cibernético relevante), el RSI lo coordina en paralelo (PRO-04).

## 5. Plazos clave
| Acción | Plazo |
|---|---|
| Notificación a la URCDP | **72 horas** desde el conocimiento del incidente |
| Comunicación a titulares | Sin dilación, en cuanto se pueda (riesgo alto) |
| Justificación de no notificación | Documentada con el incidente |

## 6. Salidas y registros
- Notificación formal a la URCDP (y su constancia).
- Registro del análisis de riesgo de la vulneración.
- Comunicado a titulares si aplica.
- Coordinación con el reporte al BCU.

## 7. Errores comunes
- No notificar por temor o por falta de claridad (más costoso).
- Notificar tardíamente sin notificación preliminar.
- No documentar la evaluación de riesgo.
- Mezclar los plazos de URCDP (72 h) y de BCU.

## 8. Referencias y evidencia
POL-07 · POL-20 · PRO-04. Alimenta: URCDP-03 (registro de notificaciones), cumplimiento Decreto 64/020.
