# POL-14 · Política de Criptografía y Gestión de Claves

> **Función del MCU 5.0:** Proteger (PR.DS — protección de datos; PR.AC — acceso)
> **ISO/IEC 27001:** A.8.24 (criptografía) · A.8.23 (transferencia segura) · A.5.30-A.5.31 (requisitos y cumplimiento)
> **BCU:** EMG / RNRCSF — protección del sistema de pagos y de datos sensibles mediante cifrado
> **URCDP:** Ley 18.331 art. 10 — el cifrado es una medida técnica de seguridad esperada para datos personales
> **Nivel del curso:** 🔴 Dominar

---

### ENCABEZADO
| **Campo** | **Valor** |
|---|---|
| **Código** | POL-14 |
| **Título** | Criptografía y Gestión de Claves |
| **Versión** | 1.0 |
| **Estado** | [Borrador / En revisión / Aprobado] |
| **Fecha de aprobación** | [COMPLETAR] |
| **Elaborado por** | RSI + Div. TI |
| **Revisado por** | Comité de Seguridad |
| **Aprobado por** | Comité de Seguridad de la Información |
| **Clasificación** | Confidencial |
| **Próxima revisión** | [Fecha, máx. 1 año] |

### 1. Objetivo
Definir los **algoritmos, usos y gestión de claves** de cifrado del Banco, garantizando la confidencialidad e integridad de la información en tránsito y en reposo, con controles sobre el ciclo de vida de las claves.

### 2. Alcance
Aplica a datos en tránsito (redes, correo, VPN, web) y en reposo (discos, bases de datos, respaldos, medios removibles, dispositivos móviles), y a las claves, certificados y secretos que los protegen.

### 3. Usos obligatorios del cifrado
| Caso | Cifrado requerido |
|---|---|
| Comunicaciones (web, correo, VPN, API) | TLS 1.2+ (recomendado 1.3) |
| Datos personales y de clientes en reposo | Cifrado en base de datos / almacenamiento |
| Respaldos (POL-08) | Cifrado en tránsito y en reposo |
| Equipos móviles y portátiles | Cifrado de disco completo |
| Medios removibles | Cifrado del contenido |
| Transmisión a terceros | Cifrado + canal autorizado (POL-11) |

### 4. Gestión de claves y secretos
- Las claves se generan con **algoritmos y longitudes aprobadas** [COMPLETAR: AES-256, RSA-2048+/ECC-256] y se almacenan en **módulos de seguridad o gestores de secretos** (HSM/vault), no en archivos planos ni en el código.
- **Ciclo de vida**: generación, distribución, almacenamiento, uso, rotación, revocación y destrucción, todo registrado.
- **Rotación**: [COMPLETAR: anual; inmediata ante sospecha de compromiso].
- **Certificados**: monitoreo de vencimiento y renovación automática/planificada.
- **Secretos en código**: prohibido; se detecta con escaneo de secretos (Gitleaks) en el SDLC (POL-15).
- **Copias de claves**: se respaldan de forma segura para no perder acceso a los datos cifrados.

### 5. Responsabilidades
- **Div. TI**: implementa y opera el cifrado y los gestores de claves.
- **RSI**: aprueba algoritmos, vigila vencimientos y gestiona incidentes de claves.
- **Desarrollo**: aplica las prácticas de cifrado en el SDLC.

### 6. Cumplimiento y revisión
Las claves expuestas o algoritmos débiles se tratan como incidentes (POL-07). Revisión anual de la política y del catálogo de algoritmos.

### Evidencia del kit
| Evidencia | Documento canónico |
|---|---|
| Catálogo de algoritmos y claves | PR-03, BCU-03 |
| Registro de rotación de claves | PR-03 |
| Escaneo de secretos | POL-15, Actividad 10 |
| Configuración TLS | POL-12, Actividad 26 |
| Gestor de secretos | PR-03 |
