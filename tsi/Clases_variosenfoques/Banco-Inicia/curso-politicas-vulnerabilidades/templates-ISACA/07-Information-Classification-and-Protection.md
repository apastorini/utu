# VPOL-12 · Information Classification and Protection Policy

> **Función del MCU 5.0:** Identificar (ID.RA — inventario y clasificación) · Proteger (PR.DS — tratamiento de datos)
> **ISO/IEC 27001:** A.5.9 (inventario de activos) · A.5.10/5.12/5.13 (clasificación, etiquetado, tratamiento)
> **BCU:** EMG — identificación de activos y su criticidad para el negocio
> **URCDP:** Ley 18.331 — los datos personales son un activo con protección reforzada
> **Nivel del curso:** 🟡 Practicar

---

### ENCABEZADO
| **Campo** | **Valor** |
|---|---|
| **Código** | VPOL-12 |
| **Título** | Information Classification and Protection |
| **Versión** | 1.0 |
| **Estado** | [Borrador / En revisión / Aprobado] |
| **Fecha de aprobación** | [COMPLETAR] |
| **Elaborado por** | RSI |
| **Revisado por** | DPD · Comité de Seguridad |
| **Aprobado por** | Comité de Seguridad de la Información |
| **Clasificación** | Uso interno |
| **Próxima revisión** | [Fecha, máx. 1 año] |

### 1. Objetivo
Establecer un **esquema de clasificación de la información** del Banco y definir el **nivel de protección** que corresponde a cada categoría, de modo que cada activo se trate según su valor y sensibilidad.

### 2. Alcance
Aplica a toda la información del Banco en cualquier formato: digital (bases de datos, archivos, correos, mensajes, código) y físico (documentos impresos). Aplica también a la información de clientes y terceros bajo custodia del Banco.

### 3. Niveles de clasificación
| Nivel | Etiqueta | Ejemplo | Protección mínima |
|---|---|---|---|
| 1 | **Público** | Información de prensa, publicidad | Sin restricciones |
| 2 | **Uso interno** | Manuales, organigramas, políticas aprobadas | Acceso solo al personal; no divulgación externa |
| 3 | **Confidencial** | Datos de clientes, información comercial, financiera no pública | Acceso por necesidad; cifrado; mínimo privilegio |
| 4 | **Muy confidencial / Secreto** | Claves, credenciales, datos de seguridad, fusiones, datos biométricos | Acceso restringido a lista corta; cifrado reforzado; auditoría de accesos |

### 4. Reglas de clasificación y etiquetado
- El **propietario del activo** (dueño de negocio) clasifica la información al crearla o recibirla.
- Etiquetado en documentos: encabezado/pie con la etiqueta; en correos: asunto y firma.
- **Datos personales** siempre son como mínimo **Confidencial (nivel 3)**, sin perjuicio de las reglas especiales de la Ley 18.331.
- Se re-clasifica (rebaja o sube) según la vigencia, el ciclo de vida o nuevos riesgos; la **eliminación** segura se rige por la tabla de retención.

### 5. Protección según el nivel
- **Almacenamiento:** cifrado en reposo para niveles 3 y 4.
- **Transmisión:** TLS/cifrado en tránsito para niveles 3 y 4; prohibido enviar nivel 4 por correo sin cifrado adicional.
- **Acceso:** mínimo privilegio y revisión periódica (VPOL-19); **nivel 4 con doble autorización y registro**.
- **Medios extraíbles:** pendrives con datos confidenciales **cifrados** (VPOL-17).
- **Impresión:** solo impresoras autorizadas; retiro inmediato (VPOL-09).
- **Nube e IA:** los niveles 3 y 4 **no** se cargan en servicios externos no autorizados (VPOL-10, VPOL-07).

### 6. Responsabilidades
- **Propietarios de activos:** clasifican y revisan.
- **RSI:** mantiene el esquema y resuelve dudas de clasificación.
- **DPD:** garantiza el tratamiento de los datos personales según la ley.
- **Auditoría:** verifica etiquetado y tratamiento.

### 7. Cumplimiento y excepciones
Clasificar mal (en particular **tratar datos confidenciales como públicos**) se investiga como incidente de fuga potencial. Revisión anual.

### Evidencia del kit
| Evidencia | Documento canónico |
|---|---|
| Inventario de activos con clasificación | ID-01 |
| Esquema de cifrado por nivel | PR-03 |
| Tratamiento de datos personales | URCDP-01 |
| Matriz de clasificación | ID-01 / GV-03 |
