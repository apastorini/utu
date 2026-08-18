# PRO-09 · Procedimiento: Clasificación, Custodia, Retención y Destrucción de la Información

> **Función del MCU 5.0:** Gobernar (GV.OR — activos) · Proteger (PR.DS — gestión de datos)
> **ISO/IEC 27001:** A.5.9-A.5.13 (gestión de activos, clasificación, etiquetado) · A.8.2 (clasificación) · A.8.10 (borrado seguro) · A.8.11 (ocultamiento)
> **BCU:** EMG — gobierno de la información y retención según normativa
> **URCDP:** Ley 18.331 art. 9 y 20 (conservación) y Decreto 414/009 — retención limitada y destrucción segura de datos personales
> **Nivel del curso:** 🟡 Practicar

---

## 1. Objetivo y alcance
Definir cómo se **clasifica, etiqueta, custodia, conserva y destruye** la información, en cualquier formato (papel, electrónico, multimedia, modelos de IA). Aplica a todas las áreas del Banco.

## 2. Clasificación (según POL-13)
| Clase | Ejemplos | Tratamiento |
|---|---|---|
| **Público** | Comunicados oficiales, informes anuales | Sin restricción |
| **Uso interno** | Procedimientos, organigramas, actas | Solo personal del Banco |
| **Confidencial** | Datos de clientes, estrategias, resultados, información financiera interna | Autorización y cifrado |
| **Muy confidencial** | Credenciales, claves de sistema, datos biométricos, información de fusiones | Mínimo acceso + cifrado + vigilancia |

## 3. Etiquetado y custodia
- Los documentos se **etiquetan** según su clase (membrete, pie de página, metadatos).
- La custodia sigue la regla del **menor privilegio**: solo accede quien lo necesita para su función (POL-04).
- Los sistemas permiten restringir el acceso por clase (ACL, clasificación de documentos).

## 4. Retención
| Tipo de información | Plazo de retención (referencia) |
|---|---|
| Datos de clientes (operaciones, cuentas) | Según normativa BCU y Código de Comercio (p. ej., 10 años para operaciones financieras) |
| Datos personales de empleados | Mientras dure la relación y el plazo legal laboral |
| Correos y documentos administrativos | Según política de archivo [COMPLETAR] |
| Registros de seguridad (logs, accesos) | [COMPLETAR: 6 meses-1 año] |
| Datos con finalidad cumplida | **Eliminar** o **anonimizar** |
- El plazo se aplica desde el cierre del trámite; se revisa el inventario de forma periódica.

## 5. Destrucción segura
- **Papel (confidencial o mayor)**: trituradora de seguridad (nivel ≥ [COMPLETAR: P-4]) o empresa certificada con certificado de destrucción.
- **Electrónico**: borrado seguro (sobrescritura/DOD) o **destrucción física** del disco para MUY CONFIDENCIALES (POL-14).
- **Dispositivos**: el retiro de equipos incluye borrado o destrucción según su contenido (PRO-03).
- **Nube/IA**: se eliminan los datos y se pide la eliminación certificada al proveedor (POL-19); se verifica el cumplimiento.

## 6. Desarrollo paso a paso
1. El **dueño del activo** clasifica la información en el inventario (POL-03).
2. El **sistema o el área** aplica el etiquetado y las restricciones de acceso.
3. Al vencer la retención, el **dueño** revisa y decide: **destruir** o **conservar** con justificación.
4. **Div. TI** ejecuta la destrucción electrónica y la registra (certificado).
5. La destrucción de datos personales se registra como evidencia (POL-20).

## 7. Salidas y registros
- Inventario de activos clasificados (ID-01).
- Certificados de destrucción.
- Registro de retención y revisiones.

## 8. Errores comunes
- Clasificar "por defecto" sin criterio (todo Uso interno).
- No aplicar retención (guardar todo para siempre).
- Descartar papel sin triturar.
- Reciclar equipos sin borrado seguro.

## 9. Referencias y evidencia
POL-03 · POL-13 · POL-14 · POL-20. Alimenta: ID-01, URCDP-01, auditorías.
