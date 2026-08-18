# VPOL-02 · Cómo se redacta una política de seguridad

> **Función del MCU 5.0:** Gobernar (GV.OR — marco de gestión, políticas) · Proteger (PR.AC — gestión de identidades y accesos)
> **ISO/IEC 27001:** A.5.1 (políticas para la seguridad de la información) · A.5.2 (revisión)
> **BCU:** EMG — gobierno y cultura de seguridad; las políticas son la base de la gestión de riesgos
> **URCDP:** Ley 18.331 art. 10 (medidas de seguridad) — las políticas documentan esas medidas
> **Nivel del curso:** 🟡 Practicar → 🔴 Dominar

---

## 1. ¿Qué es una política?

Una **política de seguridad** es un documento de alto nivel, aprobado por la dirección, que expresa **qué** debe cumplirse. No explica el detalle de **cómo** (eso es el proceso/procedimiento): fija las reglas, los responsables y las consecuencias de incumplimiento.

- Decimos **qué** → la política.
- Decimos **cómo, cuándo y quién** → el proceso/procedimiento.
- Comprobamos que **se cumple y se evidencia** → el control.

## 2. Estructura estándar de una política

Toda política del kit (y de las plantillas ISACA) sigue esta estructura:

| Sección | Qué va | Pregunta que responde |
|---|---|---|
| Encabezado | Código, versión, estado, fecha, aprobadores | ¿Qué documento es? |
| Objetivo | Propósito de la política | ¿Para qué existe? |
| Alcance | A quién/a qué aplica (y qué queda fuera) | ¿A quién alcanza? |
| Marco de referencia | Normas: Agesic, BCU, URCDP, ISO 27001 | ¿De dónde surge? |
| Roles y responsabilidades | Quién decide, quién ejecuta, quién audita | ¿Quién responde? |
| Reglas / disposiciones | Las reglas concretas (numeradas) | ¿Qué se debe hacer? |
| Cumplimiento | Consecuencias del incumplimiento | ¿Qué pasa si no? |
| Excepciones | Cómo se pide y se aprueba una desviación | ¿Se puede salir de la regla? |
| Revisión | Periodicidad de actualización | ¿Cuándo se revisa? |

## 3. Reglas de oro para escribir bien

1. **Un párrafo de objetivo corto y verificable.** Si no se puede auditar, no sirve.
2. **Alcance explícito**: "Aplica a todo el personal del Banco, proveedores y contratistas".
3. **Verbos en presente**: "El usuario debe", "El RSI aprueba". Nada de "se debería".
4. **Cada regla con responsable y sanción/control asociado.**
5. **Evitar jerga**: si un auditor o un nuevo empleado no la entiende, está mal escrita.
6. **Usar el [COMPLETAR]** para los datos del Banco: así la plantilla se reutiliza.

## 4. Ejemplo de regla bien redactada

❌ "Se recomienda que las contraseñas sean suficientemente seguras y que eventualmente se cambien periódicamente."

✅ "**PR-01-R7.** Las contraseñas de cuentas de usuario deben tener mínimo 12 caracteres e incluir 3 de 4 clases de caracteres. Se exige rotación anual obligatoria (o inmediata ante sospecha de compromiso). El Administrador de Sistemas verifica el cumplimiento con la política de contraseñas del dominio y reporta las excepciones al RSI cada mes."

## 5. Frecuencia de revisión

- Las políticas se revisan **al menos anualmente** o ante cambios significativos (nueva norma, incidente, cambio de negocio).
- Toda revisión se registra en el **control de cambios** del SGSI (GV-06).
- La aprobación final corresponde al **Comité de Seguridad de la Información**.

## 6. Relación con el kit

- Las políticas aprobadas se publican en `02-ENTREGABLES/` (GV-01, PR-01…PR-08, RS-01, etc.).
- Cada plantilla ISACA (VPOL-06…VPOL-20) ya está redactada con esta estructura: solo completá los `[COMPLETAR]`.
- La actividad DOCX 44 del curso RSI practica la redacción completa.

> **Recuerde:** la política es el *qué*. Un SGSI con 15 políticas perfectas pero cero procesos que las ejecuten es papel mojado.
