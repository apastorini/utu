# PCS-04 · Proceso de Gestión de Accesos e Identidades

> **Función del MCU 5.0:** Proteger (PR.AC — identidades, credenciales y acceso)
> **ISO/IEC 27001:** A.8.2-A.8.6 (asignación, gestión y revisión de accesos) · A.5.15-A.5.18 (control de acceso)
> **BCU:** EMG — gestión formal de identidades y accesos como control crítico
> **URCDP:** Ley 18.331 art. 10 — trazabilidad de quién accede a datos personales
> **Nivel del curso:** 🔴 Dominar
> **Ejecuta:** POL-04 (y PRO-01 / PRO-02 / PRO-08 como apoyo)

---

## 1. Objetivo y alcance
Gestionar el **ciclo de vida de las identidades y accesos** de todos los usuarios (personal, terceros, servicios) garantizando autorización previa, mínimo privilegio y revisión periódica. Aplica a todos los sistemas, aplicaciones, nube y bases de datos.

## 2. Entradas
- Solicitudes de acceso aprobadas por los jefes de área.
- Avisos de ingreso/egreso/cambio de función (RRHH — PRO-08).
- Listados de cuentas y privilegios por sistema.
- Registro de roles y perfiles por función.

## 3. Actividades numeradas

**3.1 — Alta de identidad y acceso.**
- **Responsable:** Div. TI; aprobación del jefe de área.
- **Pasos:** (a) verificar la solicitud aprobada y el perfil de rol, (b) crear la cuenta con mínimo privilegio, (c) entregar credenciales y activar MFA, (d) registrar.
- **Salida:** Cuenta creada y registrada (PRO-01).
- **Plazo:** 24-48 h desde la solicitud completa.

**3.2 — Cambio de función o de privilegios.**
- **Responsable:** Div. TI con aprobación.
- **Pasos:** (a) ajustar permisos según la nueva función, (b) revocar lo que ya no corresponde, (c) registrar el motivo.
- **Salida:** Permisos alineados a la función.
- **Plazo:** 24-72 h.

**3.3 — Baja de accesos.**
- **Responsable:** Div. TI; disparado por RRHH.
- **Pasos:** (a) revocar todos los accesos el mismo día del egreso, (b) deshabilitar la cuenta conservando la trazabilidad, (c) revocar accesos físicos, (d) verificar que no queden accesos activos.
- **Salida:** Baja ejecutada y verificada (PRO-01, PRO-08).
- **Plazo:** El mismo día; verificación en 48 h.

**3.4 — Revisión periódica de accesos.**
- **Responsable:** RSI con dueños de sistemas.
- **Pasos:** (a) exportar listados de cuentas y privilegios, (b) validar contra el personal vigente y la función, (c) marcar revocaciones/modificaciones, (d) ejecutarlas y registrar (PRO-02).
- **Salida:** Acta de revisión y accesos ajustados.
- **Plazo:** Estándar cada 6 meses; privilegiados cada 3 meses.

**3.5 — Cuentas privilegiadas y de servicio.**
- **Responsable:** RSI.
- **Pasos:** (a) inventariar cuentas privilegiadas y de servicio, (b) aplicar controles reforzados (gestor de contraseñas, MFA, revisión extra), (c) monitorear su uso.
- **Salida:** Inventario de cuentas privilegiadas controlado.
- **Plazo:** Inventario trimestral; control continuo.

**3.6 — Detección y corrección de desvíos.**
- **Responsable:** RSI.
- **Pasos:** (a) revisar accesos inactivos y excesos detectados (monitoreo, auditoría), (b) corregir y documentar, (c) informar al Comité cuando sea relevante.
- **Salida:** Correcciones registradas.
- **Plazo:** Según hallazgo.

## 4. Salidas
- Solicitudes aprobadas y registros de altas/bajas.
- Actas de revisión de accesos.
- Inventario de cuentas privilegiadas y de servicio.
- Reportes de desvíos corregidos.

## 5. Responsables del proceso
| Rol | Función |
|---|---|
| **Jefes de área** | Aprueban solicitudes y validan accesos |
| **RRHH** | Informa ingresos, cambios y egresos |
| **Div. TI** | Ejecuta altas, bajas, modificaciones y revisión técnica |
| **RSI** | Coordina la revisión, controla privilegios y audita |
| **Dueños de sistemas** | Validan accesos de sus sistemas |

## 6. Indicadores (KPIs)
- % de bajas ejecutadas el mismo día (meta 100%).
- % de accesos revisados en el plazo (meta ≥ 90%).
- Nº de cuentas inactivas/privilegios excesivos detectados y corregidos.
- % de cuentas privilegiadas con MFA (meta 100%).

## 7. Registros que deja
- Tickets de altas/bajas/modificaciones.
- Actas de revisión con firmas.
- Inventario de cuentas privilegiadas.

## 8. Referencias
POL-04 · PRO-01 · PRO-02 · PRO-08 · PCS-09 (monitoreo de accesos).

## 9. Evidencia en el kit
PR-01 (política de accesos) · GV-02 (registro de personal) · auditorías de accesos.
