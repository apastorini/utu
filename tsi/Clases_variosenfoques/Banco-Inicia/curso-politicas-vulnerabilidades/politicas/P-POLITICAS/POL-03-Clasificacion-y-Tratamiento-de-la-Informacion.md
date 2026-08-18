# POL-03 · Política de Clasificación y Tratamiento de la Información

> **Función del MCU 5.0:** Identificar (ID.AM — activos; ID.RA — riesgos) · Proteger (PR.DS — datos)
> **ISO/IEC 27001:** A.5.12-A.5.13 (clasificación y etiquetado de información) · A.8.2 (clasificación) · A.5.10 (propiedad de activos)
> **BCU:** EMG — identificación y protección de los activos de información
> **URCDP:** Ley 18.331 art. 9 y 10 — la clasificación es la base de las medidas de seguridad para datos personales
> **Nivel del curso:** 🟡 Practicar

---

### ENCABEZADO
| **Campo** | **Valor** |
|---|---|
| **Código** | POL-03 |
| **Título** | Clasificación y Tratamiento de la Información |
| **Versión** | 1.0 |
| **Estado** | [Borrador / En revisión / Aprobado] |
| **Fecha de aprobación** | [COMPLETAR] |
| **Elaborado por** | RSI + DPD |
| **Revisado por** | Comité de Seguridad · Dueños de activos |
| **Aprobado por** | Comité de Seguridad de la Información |
| **Clasificación** | Uso interno |
| **Próxima revisión** | [Fecha, máx. 1 año] |

### 1. Objetivo
Establecer **cómo se clasifica, etiqueta, almacena, transmite, retiene y destruye** la información del Banco según su sensibilidad, garantizando la protección acorde al riesgo y al valor del activo.

### 2. Alcance
Aplica a toda la información del Banco, en cualquier formato (papel, digital, correo, base de datos, medios removibles, nube) y en todo su ciclo de vida.

### 3. Niveles de clasificación
| Nivel | Definición | Ejemplos |
|---|---|---|
| **PÚBLICO** | Información de acceso público autorizado | Comunicados oficiales, folletos |
| **USO INTERNO** | Para uso interno del Banco, sin datos personales | Políticas, procedimientos internos, organigramas |
| **CONFIDENCIAL** | Acceso restringido; puede contener datos personales | Datos de clientes, informes de riesgo, contratos, estrategia |
| **MUY CONFIDENCIAL** | Acceso muy restringido; riesgo alto si se divulga | Credenciales, claves, datos biométricos, información de auditoría en curso |

### 4. Reglas obligatorias
- **Todo documento y activo de información se clasifica** en su creación (PRO-09).
- La información se **etiqueta** (membrete, metadato, campo) según su nivel.
- El **acceso** a cada nivel se controla (POL-04): los niveles CONFIDENCIAL y MUY CONFIDENCIAL requieren autorización expresa.
- La **transmisión** de información confidencial usa canales cifrados (POL-14) y **no sale del Banco sin autorización**.
- La **retención** sigue el cuadro de plazos del Banco y la normativa (BCU/URCDP); al vencerse, se **destruye de forma segura** (PRO-09).
- Los datos personales se tratan conforme a la **POL-20** (minimización, finalidad, base legal).
- La información **no se degrada de nivel** sin autorización de su dueño.

### 5. Cumplimiento
El tratamiento indebido de información clasificada (especialmente CONFIDENCIAL/MUY CONFIDENCIAL) se investiga como incidente y puede implicar medidas disciplinarias y notificaciones legales (PRO-05).

### 6. Excepciones
Solo por el procedimiento de excepciones (PRO-11), con autorización del dueño del activo y del RSI.

### 7. Revisión
Revisión anual o ante cambios de normativa, de negocio o de estructura.

### Evidencia del kit
| Evidencia | Documento canónico |
|---|---|
| Inventario de activos clasificado | ID-01 |
| Procedimiento de clasificación | PRO-09 |
| Política de datos personales | POL-20, URCDP-01 |
| Registro de destrucción | PRO-09, PR-03 |
