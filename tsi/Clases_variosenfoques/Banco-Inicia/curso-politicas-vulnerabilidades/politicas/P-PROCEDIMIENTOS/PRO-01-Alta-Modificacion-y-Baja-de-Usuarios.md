# PRO-01 · Procedimiento: Alta, Modificación y Baja de Usuarios

> **Función del MCU 5.0:** Proteger (PR.AC — gestión de identidades y accesos)
> **ISO/IEC 27001:** A.8.2 (asignación de derechos de acceso) · A.8.4 (alta de cuentas) · A.8.5 (retiro)
> **BCU:** EMG — gestión de accesos como control de riesgo de TIC
> **URCDP:** Ley 18.331 art. 10 — trazabilidad de quién accede a datos personales
> **Nivel del curso:** 🔴 Dominar

---

## 1. Objetivo y alcance
Estandarizar la creación, modificación y eliminación de cuentas de usuario en los sistemas del Banco, garantizando autorización previa y trazabilidad. Aplica a todo el personal, contratistas y proveedores.

## 2. Responsables
- **Solicitante** (jefe de área): inicia la solicitud.
- **Div. TI (Administración de cuentas)**: ejecuta el alta/modificación/baja.
- **RSI**: revisa y audita; aprueba cuentas privilegiadas.
- **RRHH**: informa ingresos y egresos (PRO-08).

## 3. Entradas
- Solicitud de acceso aprobada (formulario/ticket).
- Documento de identificación del solicitante.
- Perfil de rol (qué sistemas y permisos).
- Datos de ingreso/egreso de RRHH.

## 4. Desarrollo paso a paso

### 4.1 Alta de usuario
1. El **jefe de área** envía la solicitud con: nombre, cargo, sistemas necesarios y nivel de acceso.
2. **RRHH** confirma el ingreso del colaborador.
3. **Div. TI** verifica que la solicitud esté completa y aprobada.
4. **Div. TI** crea la cuenta en el dominio/sistemas con el **mínimo privilegio** según el rol.
5. **Div. TI** entrega credenciales iniciales y activa MFA (si aplica).
6. **RSI** verifica que los permisos coincidan con la solicitud y registra.
7. **Registrar**: fecha, usuario, sistemas, permisos, quién aprobó.

### 4.2 Modificación de accesos
1. El **jefe de área** solicita el cambio de rol/permisos (promoción, cambio de función).
2. **Div. TI** revoca o agrega accesos según la nueva función.
3. **RSI** revisa los cambios de privilegios (especialmente administrativos).
4. **Registrar** la modificación con fecha y motivo.

### 4.3 Baja de usuario
1. **RRHH** notifica el egreso (dimisión, despido, cese de contrato) con antelación y confidencialidad.
2. **Div. TI revoca todos los accesos de inmediato** (dominio, correo, sistemas, VPN, aplicaciones, nube).
3. **Div. TI** deshabilita la cuenta (no se elimina de inmediato: se conserva para auditoría).
4. **Seguridad Física** revoca tarjetas de acceso físico.
5. **RSI** verifica que no queden accesos activos y registra la baja (PRO-08).

## 5. Salidas y registros
- Ticket de solicitud de acceso.
- Registro de cuentas creadas/modificadas/bajas.
- Bitácora de verificación del RSI.
- Notificación de baja (PRO-08).

## 6. Errores comunes a evitar
- Otorgar acceso sin solicitud aprobada.
- Otorgar más privilegios de los necesarios.
- No revocar accesos en la baja (causa frecuente de incidentes).
- Compartir cuentas para "agilizar" el trabajo.

## 7. Referencias
- POL-04 (Gestión de Accesos y Privilegios) · PCS-04 (Proceso de accesos) · POL-10 · PRO-08.

## 8. Evidencia
Solicitudes aprobadas, registro de altas/bajas, verificación del RSI. Alimenta: PR-01, GV-02, auditorías de accesos.
