# POL-16 · Política de Dispositivos Móviles, Medios Removibles y Trabajo Remoto

> **Función del MCU 5.0:** Proteger (PR.AC — acceso; PR.DS — datos)
> **ISO/IEC 27001:** A.8.1-A.8.2 (dispositivos de usuario) · A.8.3 (política de dispositivos) · A.6.7 (trabajo remoto)
> **BCU:** EMG — protección de datos fuera de las instalaciones y en medios móviles
> **URCDP:** Ley 18.331 art. 10 — los datos personales fuera de la sede requieren medidas reforzadas
> **Nivel del curso:** 🟡 Practicar

---

### ENCABEZADO
| **Campo** | **Valor** |
|---|---|
| **Código** | POL-16 |
| **Título** | Dispositivos Móviles, Medios Removibles y Trabajo Remoto |
| **Versión** | 1.0 |
| **Estado** | [Borrador / En revisión / Aprobado] |
| **Fecha de aprobación** | [COMPLETAR] |
| **Elaborado por** | Div. TI + RSI |
| **Revisado por** | Comité de Seguridad · RRHH |
| **Aprobado por** | Comité de Seguridad de la Información |
| **Clasificación** | Uso interno |
| **Próxima revisión** | [Fecha, máx. 1 año] |

### 1. Objetivo
Proteger la información del Banco en **dispositivos móviles, medios removibles y en la modalidad de trabajo remoto**, controlando su uso, cifrado y destrucción.

### 2. Alcance
Aplica a portátiles, celulares corporativos, tablets, memorias USB, discos externos, tarjetas y a todo acceso remoto (VPN, escritorio remoto, nube).

### 3. Reglas obligatorias
- **Dispositivos corporativos**: solo equipos autorizados, con cifrado de disco (POL-14), antivirus/EDR, parches y bloqueo de pantalla.
- **BYOD**: solo se permite si está autorizado por la Div. TI; los datos del Banco se manejan en contenedores gestionados o vía acceso remoto, sin copiarlos al dispositivo personal.
- **Medios removibles**: prohibido el uso de memorias USB personales para datos CONFIDENCIALES; los medios corporativos se cifran, se inventarían y se destruyen de forma segura al retiro (PRO-09).
- **Trabajo remoto**: solo por VPN corporativa con MFA; el equipo debe estar actualizado y bloqueado; no se trabaja en lugares públicos con información visible (POL-18).
- **Pérdida o robo**: se reporta de inmediato (PRO-04) para aplicar borrado remoto y revocación.
- Está prohibido **almacenar datos de clientes en dispositivos personales**.
- Las conexiones Wi-Fi públicas **no** se usan para información confidencial sin VPN.

### 4. Responsabilidades
- **Div. TI**: gestión de dispositivos (MDM), cifrado y parches.
- **RSI**: define reglas y gestiona incidentes de dispositivos.
- **Usuario**: custodia el equipo y reporta pérdidas.

### 5. Cumplimiento y revisión
La pérdida de un dispositivo sin reportar o con datos personales se investiga y puede ser vulneración notificable (PRO-05). Revisión anual de la política.

### Evidencia del kit
| Evidencia | Documento canónico |
|---|---|
| Inventario de dispositivos | ID-01, PR-03 |
| Configuración MDM y cifrado | PR-03 |
| Registro de incidentes de dispositivos | RS-01 |
| Registro de medios removibles | PRO-09, PR-03 |
| Política de trabajo remoto | PR-08 |
