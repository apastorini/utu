# PRO-10 · Procedimiento: Desarrollo Seguro de Software y Código con IA

> **Función del MCU 5.0:** Proteger (PR.IP — ciclo de vida seguro) · Gobernar (GV.OR)
> **ISO/IEC 27001:** A.8.24-A.8.31 (seguridad en el desarrollo y ciclo de vida) · A.8.28 (código seguro)
> **BCU:** EMG / RNRCSF — el desarrollo de software de producción debe cumplir estándares de seguridad
> **URCDP:** Ley 18.331 art. 10 — el software que trata datos personales debe ser seguro por diseño
> **Nivel del curso:** 🔴 Dominar (ampliado con el curso `curso-ia-segura`)

---

## 1. Objetivo y alcance
Garantizar que el **software desarrollado, modificado o adquirido** por el Banco cumpla requisitos de seguridad desde el diseño hasta la producción, incluyendo el **código asistido o generado por IA** (POL-17). Aplica al desarrollo interno, integraciones y proveedores.

## 2. Responsables
- **Desarrollo (Div. TI / DevOps)**: implementa los controles.
- **RSI**: define requisitos, revisa y aprueba la entrada a producción.
- **Dueños del negocio**: validan requisitos funcionales y de seguridad.
- **DPD**: revisa los tratamientos de datos personales en la solución (POL-20).

## 3. Requisitos de seguridad en el ciclo de vida
| Fase | Controles |
|---|---|
| **Diseño** | Modelado de amenazas; requisitos de seguridad; revisión de datos personales (privacidad por diseño) |
| **Desarrollo** | Guías de codificación segura; análisis estático (SAST); análisis de dependencias (SCA); código generado por IA revisado (POL-17, AISEC-11) |
| **Pruebas** | Pruebas de seguridad (DAST), revisión manual, pruebas de datos no reales (anonimizados) |
| **Pre-producción** | Escaneo de vulnerabilidades, gestión de secretos, revisión del RSI |
| **Producción** | Configuración segura (PRO-03), monitoreo (POL-06), versionado |
| **Retiro** | Borrado seguro de datos (PRO-09) |

## 4. Reglas obligatorias
- **No se utilizan datos reales de clientes** en entornos de desarrollo ni pruebas: se usan datos sintéticos o anonimizados.
- **Secretos y credenciales** no se incluyen en el código ni en repositorios; se gestionan con bóveda de secretos.
- Todo cambio pasa por **control de versiones, revisión y revisión de seguridad** antes de producción (POL-15).
- **Código generado por IA**: se revisa manualmente y se escanea (SAST) como cualquier código; el desarrollador responde por su contenido (POL-17, AISEC-11/AISEC-12).
- Las **librerías** se mantienen actualizadas y sin vulnerabilidades conocidas (PRO-06).
- Las aplicaciones web cumplen **OWASP ASVS** y controles de framework (autenticación, autorización, validación, codificación de salida).
- El software adquirido pasa la **evaluación de seguridad del proveedor** (POL-11, PRO-13).

## 5. Desarrollo paso a paso (flujo básico)
1. El **dueño** solicita el desarrollo con requisitos funcionales y de seguridad.
2. **RSI/Arquitectura** revisa el diseño y el modelado de amenazas.
3. **Desarrollo** codifica con las guías seguras (y con herramientas de IA solo aprobadas — POL-17).
4. El equipo ejecuta **SAST, SCA y pruebas de seguridad**; corrige los hallazgos.
5. **Revisión de código** (pares) y aprobación del **RSI** para pasar a pruebas.
6. **QA** prueba con datos anonimizados; **RSI** realiza pruebas de seguridad finales.
7. **Publicación** con control de versiones y despliegue supervisado.
8. Registro de la **decisión de aprobación** de entrada a producción.

## 6. Salidas y registros
- Requisitos y diseño de seguridad.
- Resultados de SAST/DAST/SCA y su remediación.
- Registro de aprobación de entrada a producción.
- Inventario de aplicaciones y versiones.

## 7. Errores comunes
- Publicar con vulnerabilidades conocidas "por urgencia".
- Datos de producción en pruebas.
- Código de IA sin revisar ni escanear.
- Secretos en repositorios.

## 8. Referencias y evidencia
POL-15 · POL-17 · POL-19 · PRO-06 · PRO-13. Alimenta: PR-03, curso AISEC-11/AISEC-12.
