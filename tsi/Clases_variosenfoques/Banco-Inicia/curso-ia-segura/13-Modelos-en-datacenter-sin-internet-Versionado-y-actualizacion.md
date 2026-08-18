# AISEC-13 · Modelos en datacenter sin internet: versionado, catálogo y actualización

> **Función del MCU 5.0:** La gestión de modelos es gestión de activos (ID.AM) y de cambios (PR.IP): cada modelo es un activo que se inventaría, versiona, actualiza, prueba y retira, dejando evidencia.
> **ISO/IEC 27001:** Gestión de activos (A.5.9), gestión de cambios (A.8.32), gestión de vulnerabilidades (A.8.8) y protección contra códigos maliciosos (A.8.7). Un modelo sin control de versiones es un activo sin control.
> **BCU:** El datacenter y sus componentes (incluidos los modelos de IA) deben estar documentados en los EMG y el RNRCSF con su ciclo de vida y versiones.
> **URCDP:** Un modelo desactualizado o de origen no verificado puede procesar datos con comportamientos no controlados: la trazabilidad de versiones es parte de la seguridad (PD.5).
> **Decreto 66/025:** El CERTuy espera que la institución sepa qué hay desplegado y qué versiones corre, para poder responder ante vulnerabilidades publicadas de modelos.
> **Nivel del curso:** 🔴 Dominar

---

## 1. El escenario: un datacenter sin salida a internet

El Banco decide que sus modelos de IA corran en **datacenters locales sin salida a internet**: los datos jamás salen, pero tampoco se puede "bajar un modelo nuevo con un clic". Eso genera tres preguntas prácticas:

1. **¿Cómo hago para versionar y mantener los modelos que ya tengo?**
2. **¿Cómo cargo modelos nuevos o más actualizados si no hay internet?**
3. **¿Cómo sé que el modelo que cargo es legítimo y no fue manipulado?**

Este módulo responde esas tres preguntas con un **modelo de gestión de modelos (model registry)**.

> Analogía: pensar en los modelos como si fueran **medicamentos**. No se compran en cualquier lado, tienen lote (versión), fecha de vencimiento (actualización), se verifican antes de usarse (hash/firma), se prueban en un grupo chico (entorno de prueba) y se registra quién los administró y a qué pacientes (trazabilidad).

---

## 2. La pieza central: el Registro de Modelos (Model Registry)

Un **Registro de Modelos** es el inventario central donde cada modelo queda documentado. Es la misma lógica que el inventario de activos del SGSI, pero para modelos de IA.

### Campos mínimos por modelo registrado

| Campo | Qué registra | Ejemplo |
|---|---|---|
| **ID del modelo** | Identificador único | `llama-3.1-8b-instruct` |
| **Versión** | Versión semántica del modelo | `3.1.2` |
| **Proveedor/origen** | De dónde viene | `Meta (Hugging Face oficial)` |
| **Fecha de alta** | Cuándo entró al Banco | `2026-02-10` |
| **SHA-256** | Huella digital del archivo | `a3f9...` |
| **Licencia** | Términos de uso | `Llama 3.1 Community License` |
| **Tamaño** | Peso en GB | `4.9 GB` |
| **Formato** | Formato del archivo | `GGUF`, `FP16`, `AWQ` |
| **Estado** | `aprobado` / `prueba` / `retirado` | `aprobado` |
| **Aprobado por** | Quién autorizó el uso | RSI + TI |
| **Fecha de próxima revisión** | Caducidad del modelo | `2026-08-10` |
| **Riesgo asociado** | Vulnerabilidades conocidas | `ninguna conocida` |

### Dónde vive el registro

El registro es un **documento controlado** (puede ser una planilla, una base o una carpeta versionada). El kit lo trabaja como la plantilla `GV-02` (inventario) adaptada a modelos. **Cada modelo desplegado en Ollama/vLLM debe tener su fila en el registro.**

---

## 3. Cómo se versiona un modelo (ciclo de vida)

### 3.1 Etapas del ciclo de vida

| Etapa | Qué pasa | Quién |
|---|---|---|
| **Propuesta** | TI pide incorporar/actualizar un modelo justificando la necesidad | TI |
| **Evaluación** | Se evalúa riesgo, licencia, origen y necesidad (¿realmente hace falta?) | RSI + TI |
| **Descarga verificada** | Se obtiene el archivo por un canal controlado y se verifica su integridad | TI |
| **Prueba** | Se carga en el entorno de prueba, se ejecutan pruebas de sanidad y de seguridad | TI + RSI |
| **Aprobación** | El RSI aprueba la promoción a producción | RSI |
| **Producción** | Se despliega en Ollama/vLLM, se registra y se monitorea | TI |
| **Revisión** | Se revisa periódicamente (nueva versión, vulnerabilidades, obsolescencia) | RSI |
| **Retiro** | Se desactiva el modelo viejo, se archiva su registro y se documenta el motivo | RSI + TI |

### 3.2 Versionado semántico

Los modelos se versionan como software: `MAJOR.MINOR.PATCH`.

- **MAJOR**: cambio grande (nueva familia, arquitectura distinta).
- **MINOR**: mejora del mismo modelo (nueva revisión con más datos).
- **PATCH**: corrección de un problema puntual.

**Regla:** nunca se "pisa" un modelo en producción. La versión vieja se queda registrada hasta su retiro. Si la nueva falla, se puede **volver atrás (rollback)** en minutos porque la anterior sigue guardada.

### 3.3 El modelo viejo no se borra: se retira

Retirar ≠ borrar. El retiro es un **proceso con registro**: se desactiva, se archiva el artefacto (si el espacio lo permite), se documenta por qué se retiró y se guarda la evidencia (pruebas, fechas). Si hubiera un incidente, poder volver a la versión anterior es parte de la respuesta (RS).

---

## 4. Cómo se actualiza sin internet (ingesta de modelos)

El problema central: si el datacenter no tiene salida a internet, **¿de dónde sale el archivo del modelo nuevo?**

Hay **tres mecanismos válidos**, ordenados de más seguro a más práctico:

### Opción A · Aislamiento total con zona de tránsito (la más segura)

1. Existe una **única estación de trabajo de tránsito** (sin conexión a la red del Banco, con su propio antivirus actualizado) con acceso puntual a internet o a la fuente del modelo.
2. El archivo del modelo se descarga **ahí**, no en el datacenter.
3. Se calcula el **SHA-256** y se compara contra el valor publicado por el proveedor oficial (dos personas verifican).
4. Se copia al datacenter por **medio físico controlado** (disco/USB exclusivo del proceso, cifrado, numerado y registrado) o por **red administrativa aislada**.
5. Se verifica el hash **una vez dentro** del datacenter antes de instalarlo.

### Opción B · Zona desmilitarizada (DMZ) de actualización

1. El datacenter abre **una única conexión controlada** a un servidor espejo autorizado (proxy/registry interno de la nube o del proveedor).
2. Solo esa conexión puede bajar modelos; el resto del tráfico sigue bloqueado.
3. La bajada se registra en logs (quién, cuándo, qué archivo, hash).
4. El archivo pasa por el mismo control de hash y pruebas antes de producción.

### Opción C · Entrega física del proveedor

1. El proveedor envía el modelo en un medio físico verificado (si el contrato lo permite).
2. Se verifican la firma digital y el hash en la estación de tránsito.
3. Mismo flujo de copia y pruebas que en la Opción A.

> **En todas las opciones aplica la misma regla: el modelo solo entra si el hash coincide, viene de fuente oficial, está probado y está aprobado por el RSI.**

---

## 5. Verificación de integridad y origen (lo que nunca se salta)

### 5.1 Hash (integridad)

Un **hash SHA-256** es la "huella digital" del archivo del modelo. Si alguien modifica aunque sea un byte, el hash cambia por completo.

```powershell
# Calcular el hash del modelo descargado (Windows)
Get-FileHash .\modelo.gguf -Algorithm SHA256

# En Linux
sha256sum modelo.gguf
```

El resultado debe coincidir con el valor **publicado por el proveedor oficial**. Si no coincide: **no se instala, se descarta y se investiga**.

### 5.2 Firma digital (origen)

Además del hash, muchos modelos vienen **firmados digitalmente** por el proveedor. Verificar la firma confirma que el archivo viene realmente de quien dice venir (no es un suplantador que publicó un archivo falso). La verificación se hace con la clave pública del proveedor.

### 5.3 Checklist de ingesta de un modelo

- [ ] ¿La necesidad está justificada y aprobada?
- [ ] ¿La fuente es la oficial del proveedor?
- [ ] ¿El SHA-256 coincide con el publicado?
- [ ] ¿La licencia permite el uso en el Banco?
- [ ] ¿Se verificó la firma digital?
- ¿El modelo pasó las pruebas en el entorno de prueba?
- [ ] ¿El RSI aprobó la promoción?
- [ ] ¿Quedó registrado en el Registro de Modelos?

---

## 6. Pruebas antes de promocionar un modelo

Un modelo nuevo no se despliega directo. Se ejecuta una **batería de pruebas de sanidad y seguridad**:

| Prueba | Qué detecta | Ejemplo |
|---|---|---|
| **Sanidad básica** | Que responde correctamente a preguntas simples | "¿Cuánto es 7×8?" → "56" |
| **Calidad de respuesta** | Mejora o regresión frente al modelo anterior | Comparar resúmenes sobre el mismo texto |
| **Alucinación** | Inventos sobre temas del Banco | Preguntar sobre la política PD-01 sin RAG y ver si inventa |
| **Prompt injection** | Que un texto malicioso no lo secuestra | Ver módulo AISEC-05 |
| **Sesgo** | Respuestas discriminatorias | Preguntas sobre perfiles de clientes |
| **Lenguaje de salida** | Español correcto y tono institucional | Redactar un correo de prueba |
| **Rendimiento** | Velocidad y consumo de hardware | Medir latencia en vLLM |

Resultado de cada prueba → se registra en la **bitácora del modelo**. Solo con el visto bueno del RSI el modelo pasa a producción.

---

## 7. Actualización planificada vs. actualización urgente

| Tipo | Disparador | Proceso |
|---|---|---|
| **Planificada** | Nueva versión del proveedor, calendario semestral/anual | Ingesta completa por el flujo normal (sección 4), pruebas, aprobación, despliegue, retiro del anterior |
| **Urgente** | **Vulnerabilidad publicada** del modelo o del software (Ollama/vLLM) | Proceso acelerado: se evalúa el riesgo, se aplica el parche/modelo nuevo o se **desactiva temporalmente** el modelo afectado (contención) hasta resolver |

### Cómo saber si un modelo tiene vulnerabilidades (sin internet en el datacenter)

1. La **zona de tránsito o DMZ** consulta periódicamente los avisos del proveedor y de CERTuy.
2. El RSI recibe un **resumen mensual de avisos de vulnerabilidad de modelos**.
3. Si hay una vulnerabilidad crítica: se aplica el flujo urgente.

---

## 8. Hardware y almacenamiento (datos prácticos)

| Aspecto | Recomendación |
|---|---|
| GPU | Los modelos grandes necesitan GPUs con mucha VRAM; verificar la memoria mínima del modelo antes de comprar |
| Almacenamiento | Reservar espacio para la **versión actual + la anterior** (rollback) + la de prueba |
| Red interna | Copiar modelos grandes por red de alta velocidad entre la estación de tránsito y el datacenter |
| Copias de seguridad | El archivo del modelo aprobado forma parte del respaldo (plantilla de backup del kit) |
| Actualización de software | Ollama, vLLM y el resto del stack se actualizan con el mismo flujo de ingesta controlada |

---

## 9. Evidencias que deja la gestión de modelos

| Evidencia | Qué demuestra | Requisito |
|---|---|---|
| Registro de Modelos (inventario con versiones y hashes) | Control de activos | A.5.9, GV-02, ID.AM |
| Reporte de verificación de hash/firma | Integridad del artefacto | A.8.8, PR.DS |
| Bitácora de pruebas del modelo | Validación antes de producción | PR.IP, A.8.32 |
| Registro de aprobación del RSI | Gobierno del cambio | GV, CN.1 |
| Registro de retiro de versiones viejas | Ciclo de vida completo | A.5.9, A.8.32 |
| Avisos de vulnerabilidad revisados | Gestión de vulnerabilidades | A.8.8, Decreto 66/025 |

---

## 10. Conclusión del módulo

- En un datacenter sin internet, los modelos se gestionan con un **Registro de Modelos**: inventario, versiones, hashes, licencias, estado y aprobaciones.
- La **ingesta sin internet** se resuelve con **zona de tránsito** (descarga controlada + verificación) o **DMZ de actualización**; nunca abriendo el datacenter a internet.
- **Todo modelo se verifica** (hash + firma), **se prueba** (sanidad, alucinación, inyección, sesgo) y **se aprueba** antes de producción.
- **Nada se pisa**: el modelo anterior queda disponible hasta el retiro formal, permitiendo volver atrás.
- Las **actualizaciones urgentes** (vulnerabilidades) tienen su propio flujo acelerado, incluida la contención (apagar el modelo afectado).
- Toda esta gestión **queda documentada**: es evidencia para Agesic, BCU y URCDP.

> **Ejercicio (TI/RSI):** Arme el Registro de Modelos de su institución con una fila por cada modelo desplegado (versión, hash, licencia, estado, aprobado por). Luego simule la ingesta de una "nueva versión": use cualquier archivo de prueba, calcule su SHA-256, documente las 3 verificaciones y complete la bitácora de pruebas. Ese registro es la evidencia del módulo.
