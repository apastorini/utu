# VPOL-19 · User Access Management Policy

> **Función del MCU 5.0:** Proteger (PR.AC — gestión de identidades, credenciales y acceso)
> **ISO/IEC 27001:** A.5.15/5.16/5.17/5.18 (control de accesos: políticas, gestión, autenticación, derechos) · A.8.5/8.6 (autenticación segura)
> **BCU:** EMG — control de accesos, segregación de funciones, cuentas privilegiadas
> **URCDP:** Ley 18.331 — el acceso a datos personales solo para fines determinados y autorizados
> **Nivel del curso:** 🟡 Practicar

---

### ENCABEZADO
| **Campo** | **Valor** |
|---|---|
| **Código** | VPOL-19 |
| **Título** | User Access Management |
| **Versión** | 1.0 |
| **Estado** | [Borrador / En revisión / Aprobado] |
| **Fecha de aprobación** | [COMPLETAR] |
| **Elaborado por** | RSI + Div. TI |
| **Revisado por** | Jefes de área · DPD |
| **Aprobado por** | Comité de Seguridad de la Información |
| **Clasificación** | Uso interno |
| **Próxima revisión** | [Fecha, máx. 1 año] |

### 1. Objetivo
Definir cómo se **crean, cambian, autorizan, revocan y auditan** los accesos lógicos del Banco, garantizando el **mínimo privilegio**, la **segregación de funciones** y la **trazabilidad**, protegiendo especialmente las cuentas privilegiadas.

### 2. Alcance
Aplica a todos los usuarios (personal, contratistas, proveedores, sistemas) y a todos los sistemas: dominio, core, Banco En Línea, bases de datos, red, nube, SIEM, y cuentas de servicio.

### 3. Ciclo de vida del acceso
1. **Solicitud** de acceso por el jefe del área, justificada según el puesto.
2. **Autorización** según la matriz de accesos ([COMPLETAR: perfiles predefinidos por rol]).
3. **Alta** por la Div. TI con **MFA** cuando corresponda.
4. **Cambio** de rol: se ajustan los accesos al nuevo cargo.
5. **Revisión periódica** de accesos: [COMPLETAR: semestral] con validación de cada jefe.
6. **Baja inmediata** ante egreso o cambio de funciones (VPOL-16).

### 4. Mínimo privilegio y segregación
- Cada usuario tiene **solo los accesos necesarios** para su función.
- **Segregación de funciones** obligatoria: quien solicita/aprueba/ejecuta no es el mismo (p. ej. quien autoriza una transferencia no la ejecuta; quien administra no audita).
- Acceso a **datos personales** de clientes: solo por necesidad, con registro de consulta (VPOL-14).

### 5. Cuentas privilegiadas y de servicio
- **Cuentas de administrador:** únicas por persona, con MFA, sin uso compartido; prohibido el uso diario con cuenta admin (se usa cuenta normal + elevación puntual).
- Las acciones privilegiadas se **registran y revisan** mensualmente (VPOL-14).
- **Cuentas de servicio** (sistemas ↔ sistemas): secretos en gestor de credenciales (no en el código), con rotación [COMPLETAR: trimestral] y revisión de vigencia.

### 6. Autenticación y credenciales
- **MFA obligatoria** para: acceso remoto, cuentas privilegiadas, Banco En Línea, nube y sistemas críticos.
- Política de contraseñas: [COMPLETAR: mínimo 12 caracteres, 3 de 4 clases, sin reutilización de últimas 5, rotación anual o ante sospecha] (conforme actividad 28 / PR-01).
- Prohibido compartir credenciales; cada acceso se identifica individualmente.
- **Bloqueo** de cuenta tras [COMPLETAR: 5] intentos fallidos y bloqueo por inactividad [COMPLETAR: 5] minutos.

### 7. Revisión y auditoría
- Revisión de accesos **semestral** con evidencia (acta por área).
- La **Auditoría Interna** evalúa periódicamente la gestión de accesos y los accesos privilegiados.
- Los accesos no justificados se **revocan** y se reporta el desvío al Comité.

### 8. Cumplimiento y excepciones
El acceso no autorizado o compartido se trata como **incidente** (y posible denuncia, Ley 19.223). Excepciones con aprobación del RSI y plazo definido.

### Evidencia del kit
| Evidencia | Documento canónico |
|---|---|
| Matriz de accesos y perfiles | PR-01 |
| Revisión de accesos semestral | PR-01 / EV-04 |
| Gestor de credenciales y rotación | PR-01 |
| Registro de accesos privilegiados | PR-01 / DE-01 |
