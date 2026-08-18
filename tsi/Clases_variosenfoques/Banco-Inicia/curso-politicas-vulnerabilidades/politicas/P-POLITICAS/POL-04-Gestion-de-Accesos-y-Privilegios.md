# POL-04 · Política de Gestión de Accesos y Privilegios

> **Función del MCU 5.0:** Proteger (PR.AC — identidad y control de acceso)
> **ISO/IEC 27001:** A.5.15 (control de acceso) · A.8.2-A.8.6 (gestión de cuentas, privilegios, revisión) · A.5.18 (menor privilegio)
> **BCU:** EMG — gestión de accesos es uno de los riesgos de TIC más frecuentemente auditados
> **URCDP:** Ley 18.331 — los accesos a datos personales deben ser mínimos y trazables (PD.5)
> **Nivel del curso:** 🟡 Practicar → 🔴 Dominar

---

### ENCABEZADO
| **Campo** | **Valor** |
|---|---|
| **Código** | POL-04 |
| **Título** | Gestión de Accesos y Privilegios |
| **Versión** | 1.0 |
| **Estado** | [Borrador / En revisión / Aprobado] |
| **Fecha de aprobación** | [COMPLETAR] |
| **Elaborado por** | RSI + Div. TI |
| **Revisado por** | Comité de Seguridad · RRHH |
| **Aprobado por** | Comité de Seguridad de la Información |
| **Clasificación** | Uso interno |
| **Próxima revisión** | [Fecha, máx. 1 año] |

### 1. Objetivo
Garantizar que **cada usuario acceda solo a lo que necesita para su función** (menor privilegio), que las cuentas se creen, modifiquen y eliminen de forma controlada, y que el acceso sea trazable.

### 2. Alcance
Aplica a todas las cuentas de usuario, cuentas de servicio, cuentas administrativas, sistemas, aplicaciones, bases de datos, redes y accesos físicos del Banco.

### 3. Reglas obligatorias
- **Identificación única:** cada persona tiene su cuenta personal; están prohibidas las cuentas compartidas (salvo autorización excepcional con registro).
- **Menor privilegio:** los permisos se otorgan al mínimo necesario para la función.
- **Cuentas administrativas:** se usan solo para tareas administrativas; se crean con nombre específico, no se comparten y sus acciones se registran (POL-13).
- **Autenticación fuerte:** se exige contraseña robusta (POL-14) y **MFA** para accesos administrativos, remotos y aplicaciones sensibles.
- **Altas y bajas:** el acceso se otorga tras la solicitud aprobada (PRO-01) y se **revoca de inmediato** en la baja de personal (PRO-08).
- **Revisión periódica:** los accesos y privilegios se revisan al menos **cada 6 meses** (PRO-02); los privilegios administrativos, cada 3 meses.
- **Segregación de funciones:** quien autoriza no ejecuta y quien audita no autoriza (para procesos críticos: pagos, cambios, accesos).
- **Registro:** toda concesión, modificación y revocación de acceso queda registrada (PCS-04).

### 4. Cumplimiento
Los accesos no autorizados o las cuentas sin revisar se tratan como hallazgos de seguridad. El uso indebido de cuentas se investiga (PCS-03) y puede dar lugar a medidas disciplinarias.

### 5. Excepciones
Las excepciones (cuentas compartidas, privilegios temporales) se solicitan por PRO-11 y se aprueban con plazo de caducidad y registro.

### 6. Revisión
Revisión anual de la política; revisión semestral de accesos; revisión trimestral de privilegios administrativos.

### Evidencia del kit
| Evidencia | Documento canónico |
|---|---|
| Solicitudes de acceso aprobadas | PR-01 |
| Revisión periódica de accesos | PR-01, PRO-02 |
| Registro de altas/bajas | PRO-01, PRO-08 |
| Bitácora de cuentas administrativas | DE-01, POL-13 |
| Excepciones y caducidades | GV-06, PRO-11 |
