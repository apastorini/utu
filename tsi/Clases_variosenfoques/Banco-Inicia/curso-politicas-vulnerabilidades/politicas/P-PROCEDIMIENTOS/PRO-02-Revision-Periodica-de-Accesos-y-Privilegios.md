# PRO-02 · Procedimiento: Revisión Periódica de Accesos y Privilegios

> **Función del MCU 5.0:** Proteger (PR.AC — revisión de accesos)
> **ISO/IEC 27001:** A.8.6 (revisión de derechos de acceso) · A.8.4 (retiro de accesos)
> **BCU:** EMG — revisión periódica de accesos esperada por el supervisor
> **URCDP:** Ley 18.331 art. 10 — los accesos a datos personales deben revisarse
> **Nivel del curso:** 🔴 Dominar

---

## 1. Objetivo y alcance
Verificar periódicamente que los accesos y privilegios de cada usuario corresponden a su función actual, revocando los obsoletos y corrigiendo los excesos. Aplica a todas las cuentas y sistemas.

## 2. Responsables
- **Dueños de sistemas**: validan los accesos de su sistema.
- **Div. TI**: emite los listados y ejecuta las revocaciones.
- **RSI**: coordina, consolida y reporta resultados.

## 3. Entradas
- Listados de cuentas y privilegios por sistema (exportación del dominio, apps, nube, bases).
- Registro de altas/bajas del período.
- Listado de personal vigente (RRHH).

## 4. Desarrollo paso a paso
1. **Div. TI exporta** el listado de cuentas activas, privilegios y último acceso por sistema.
2. **RSI prepara** el paquete por área (usuarios del área y sus accesos).
3. **El dueño de cada área/sistema revisa** y marca: mantiene / modifica / revoca, con justificación.
4. **Div. TI revoca o modifica** los accesos marcados, dentro de [COMPLETAR: 5 días hábiles].
5. **Cuentas inactivas** (sin uso [COMPLETAR: 60-90 días]) se deshabilitan.
6. **Cuentas privilegiadas**: la revisión incluye una validación adicional del RSI (quién tiene permisos de administrador y por qué).
7. **RSI consolida** los resultados, calcula métricas (accesos revocados, excesos encontrados) y reporta al Comité.
8. **Registrar**: fecha de revisión, participantes, hallazgos y acciones.

## 5. Frecuencia
- Accesos estándar: **cada 6 meses**.
- Cuentas privilegiadas/administrativas: **cada 3 meses**.
- Extraordinaria: tras cambios de estructura, egresos masivos o incidentes.

## 6. Salidas y registros
- Acta de revisión con firmas de los dueños.
- Listado de accesos revocados/modificados.
- Reporte de métricas al Comité.

## 7. Errores comunes
- Revisar "contra el papel" sin validar el sistema.
- No revisar cuentas de servicio ni integraciones.
- Dejar pasar privilegios administrativos sobrantes.

## 8. Referencias y evidencia
POL-04 · PCS-04 · PRO-01. Alimenta: PR-01, auditorías, hallazgos de BCU.
