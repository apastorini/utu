# INFRA-06 · SAST, DAST, DLP y Prevención de Fuga de Datos

> **Función del MCU 5.0:** Cubrir el dominio de protección de datos y servicios (PR.DS) y la detección de eventos (DE.CM): asegurar el software que el banco desarrolla, probar las aplicaciones en ejecución y evitar que información confidencial salga de la red del Banco sin autorización.
> **ISO/IEC 27001:** Sustenta los controles del Anexo A de seguridad en desarrollo y mantenimiento (A.14.2), pruebas de seguridad (A.14.2.8), y prevención de fuga de información (A.8.2.3 y A.13.1).
> **BCU:** Aporta evidencia técnica para el Reglamento de Normas de Control sobre Riesgo de TIC (RNRCSF), en particular sobre riesgo tecnológico asociado a aplicaciones propias y al manejo de información confidencial de clientes.
> **URCDP:** Protege los datos personales que las aplicaciones del Banco tratan, aplicando medidas técnicas desde el diseño (Decreto 64/020) y evitando que esos datos salgan de la organización sin autorización.
> **Nivel del curso:** 🟢 Descubrir · 🟡 Practicar · 🔴 Dominar

---

## 1. Propósito de este módulo

Un banco no es solo cables, routers y servidores. También es **software**: la banca por internet, la app del celular, el sistema de préstamos, la intranet, los reportes. Y ese software maneja datos personales y secretos bancarios todo el tiempo.

Este módulo responde tres preguntas:

- ¿Cómo nos aseguramos de que el **software que escribimos** no tenga fallas de seguridad antes de llegar a producción?
- ¿Cómo probamos la **aplicación en ejecución** como lo haría un atacante?
- ¿Cómo evitamos que **datos confidenciales se vayan** de la organización (correos, USB, impresora, nube personal)?

> **Analogía:** imagina que el banco es una casa con una puerta nueva. SAST revisa la madera antes de instalarla (busca rajaduras en el material). DAST la golpea una vez instalada (¿se abre con una ganzúa?). Y DLP es el guardia en la salida que revisa qué llevás cuando te vas (¿salió información que no debía?).

---

## 2. Qué significa asegurar el software que el banco desarrolla y usa

Seguridad del software no es una etapa: es un **ciclo**. Desde que se escribe la primera línea de código hasta que la aplicación se retira, hay que preguntarse en cada momento *"¿dónde puede fallar esto?"*.

A esto se le llama **seguridad en el ciclo de vida de desarrollo** (en inglés, *Secure SDLC*). El kit ya lo toca en el documento **PR-07 (Seguridad en el Desarrollo y las Aplicaciones)**. Este módulo te explica la parte técnica de *cómo se prueba*.

Las pruebas de seguridad de aplicaciones se dividen en dos grandes familias:

| Tipo | Qué hace | Cuándo | Se parece a |
|---|---|---|---|
| **SAST** | Lee el código fuente sin ejecutarlo | Durante el desarrollo y en cada integración | El corrector de ortografía del código |
| **DAST** | Prueba la aplicación en ejecución desde afuera | Pre-producción y periódicamente | El atacante que la golpea para ver si cede |

Hay además dos refuerzos: **IAST** (instrumentación que combina lo estático con lo dinámico dentro de la app) y **RASP** (un escudo que vive dentro de la aplicación y responde ante ataques en tiempo real). Los veremos brevemente en la sección 5.

---

## 3. SAST: análisis estático del código fuente

### Qué es

SAST significa **Static Application Security Testing** (prueba estática de seguridad de aplicaciones). Es un programa que **lee el código fuente, sin ejecutarlo**, y busca patrones de código inseguro.

> **Analogía:** es como un arquitecto que revisa los planos de un edificio y dice "este pasillo es demasiado angosto para escapar en caso de incendio", sin necesidad de construirlo primero.

### Cuándo se usa

- En **cada "build"** (cada vez que el equipo compila o integra el código nuevo).
- Integrado en el **CI/CD**: el sistema de integración continua. Si el escaneo encuentra un problema crítico, la entrega se detiene.
- Antes de cada **release** (entrega a producción).

### Ejemplos de herramientas

| Herramienta | Tipo | Nota |
|---|---|---|
| **Semgrep** | Open source | Rápida, fácil de escribir reglas, ideal para empezar |
| **SonarQube** | Comercial/CE | Revisa calidad y seguridad del código; muy usada en equipos grandes |
| **Checkmarx** | Comercial | Escáner SAST de referencia en empresas financieras |
| **Fortify** | Comercial | Suite de seguridad de aplicaciones de amplia adopción |

> **Nota:** en un entorno bancario la herramienta no puede ser "la que me gusta", sino la que la institución autoriza y documenta en **PR-07**. Cualquier herramienta sirve si su uso está definido y sus resultados se gestionan.

### Qué encuentra

- **Inyección SQL:** el programa arma una consulta a la base con datos del usuario sin sanitizarlos.
- **XSS (cross-site scripting):** el programa muestra texto del usuario sin escapar, permitiendo que inyecte scripts.
- **Secretos en el código:** contraseñas, claves API o tokens escritos "a mano" dentro del archivo fuente.
- **Uso de funciones inseguras**, falta de validación de entradas, deserialización peligrosa, etc.

### Límites

- No ve el comportamiento **en ejecución**: puede no detectar problemas de configuración o de integración con otros sistemas.
- Genera **falsos positivos**: marca como problema algo que en la práctica no lo es. Hay que revisar y descartar con criterio.
- Depende de la **cobertura del lenguaje y de las reglas** configuradas: solo encuentra lo que sus reglas saben buscar.

---

## 4. DAST: análisis dinámico de la aplicación en ejecución

### Qué es

DAST significa **Dynamic Application Security Testing** (prueba dinámica de seguridad de aplicaciones). Ejecuta la aplicación **como si fuera un atacante externo**: le manda solicitudes reales (por HTTP, por ejemplo) y analiza las respuestas buscando vulnerabilidades expuestas.

> **Analogía:** SAST revisa los planos; DAST manda a alguien a tocar la puerta del edificio terminado, probar las ventanas y ver si alguna cede.

### Cuándo se usa

- En **pre-producción**, antes de que el cambio llegue al ambiente real.
- En **forma periódica** (al menos una vez al año) sobre las aplicaciones críticas.
- Cuando hay **cambios grandes**: nueva funcionalidad, nuevo componente, nueva versión.

### Ejemplos de herramientas

| Herramienta | Tipo | Nota |
|---|---|---|
| **OWASP ZAP** | Open source | Gratuita y muy usada; ideal para equipos que empiezan |
| **Burp Suite** | Comercial | La favorita de quienes hacen pruebas manuales y automatizadas |
| **Acunetix** | Comercial | Escáner web con gestión de hallazgos |

### Qué encuentra

- **Vulnerabilidades expuestas**: inyecciones que SAST no vio porque se producen por la interacción de varios componentes.
- **Errores de configuración** del servidor o de la aplicación (por ejemplo, una página de error que muestra el stack trace completo).
- **Cabeceras HTTP inseguras**, autenticación débil, endpoints expuestos sin control de acceso, cifrado débil en tránsito.
- Fallas que **solo aparecen cuando los módulos se ejecutan juntos**.

### Límites

- Necesita que la aplicación esté **corriendo** y con datos de prueba representativos.
- Puede **alterar la base de datos** (los escaneos envían datos raros). Por eso se ejecuta en ambientes de prueba, no en producción real.
- No ve el código que no se puede alcanzar desde afuera; hay fallas que solo se descubren revisando el código.

---

## 5. IAST y RASP (en breve)

Son dos tecnologías complementarias que conviene conocer aunque su implementación sea posterior:

| Tecnología | Qué hace | Diferencia clave |
|---|---|---|
| **IAST** | Se instala *dentro* de la aplicación y combina la vista del código con las solicitudes reales | Ve el código que sí se ejecuta: menos falsos positivos |
| **RASP** | Vive *dentro* de la aplicación en producción y **responde** ante ataques (bloquea, alerta) | No detecta: defiende en el momento del ataque |

> En el Banco, IAST y RASP son refuerzos opcionales de **PR-07**. La base obligatoria es SAST + DAST + pentest manual (documento **DE-03**).

---

## 6. OWASP Top 10: el resumen que todos deberían conocer

**OWASP** es una fundación mundial de seguridad de aplicaciones. Publica una lista, actualizada cada pocos años, con las **10 familias de fallas más comunes y peligrosas** en aplicaciones web. Es el "ranking de riesgos" del desarrollo.

| # | Categoría | Ejemplo simple |
|---|---|---|
| 1 | **Broken Access Control** (control de acceso roto) | Un usuario normal puede ver la pantalla de administrador solo cambiando la URL |
| 2 | **Cryptographic Failures** (fallas criptográficas) | Contraseñas guardadas en texto plano en la base |
| 3 | **Injection** (inyección) | Escribir `'; DROP TABLE clientes; --` en el campo de búsqueda y que la base lo ejecute |
| 4 | **Insecure Design** (diseño inseguro) | Un formulario de recuperación de contraseña que nunca bloquea intentos |
| 5 | **Security Misconfiguration** (mala configuración) | El servidor responde con mensajes de error que revelan versiones internas |
| 6 | **Vulnerable and Outdated Components** (componentes desactualizados) | La app usa una librería vieja con vulnerabilidades conocidas |
| 7 | **Identification and Authentication Failures** (fallas de identificación y autenticación) | Permitir adivinar contraseñas sin límite de intentos |
| 8 | **Software and Data Integrity Failures** (fallas de integridad) | Un paquete actualizado se instala sin verificar que provenga de la fuente oficial |
| 9 | **Security Logging and Monitoring Failures** (fallas de registro y monitoreo) | Los ataques pasan desapercibidos porque no hay registros ni alertas |
| 10 | **Server-Side Request Forgery (SSRF)** | La app consulta una URL interna que el usuario le indica, y así el atacante "viaja" por la red interna |

### Cómo lo cubren SAST y DAST

| Categoría OWASP | SAST | DAST |
|---|---|---|
| Inyección (3) | ✓ Detecta en el código | ✓ La prueba enviando datos maliciosos |
| Fallas criptográficas (2) | ✓ Detecta almacenamiento inseguro | Parcial (según lo que exponga) |
| Control de acceso roto (1) | Parcial | ✓ La prueba roles y rutas |
| Mala configuración (5) | Parcial | ✓ La ve desde afuera |
| Componentes desactualizados (6) | ✓ Con reglas de dependencias | Parcial |
| Diseño inseguro (4) | No | Parcial |
| SSRF (10) | Parcial | ✓ La prueba con URLs internas |
| Registro y monitoreo (9) | No | No (se verifica aparte, en DE-01) |

> **Punto clave:** ninguna herramienta cubre todo. Por eso el proceso recomendado combina **varias técnicas**, como dice la sección siguiente.

---

## 7. Proceso recomendado

No se trata de hacerlo todo todo el tiempo, sino de hacer **lo correcto en el momento correcto**. Este es el proceso base del kit:

| Fase | Herramienta / técnica | Frecuencia | Responsable |
|---|---|---|---|
| Cada integración de código (CI/CD) | **SAST** automatizado | En cada build | Desarrolladores + DevOps |
| Antes de cada release | **SAST** final + **DAST** sobre pre-producción | En cada release | Equipo de desarrollo + seguridad |
| Periódico | **DAST** sobre aplicaciones críticas | Al menos anual | Seguridad de aplicaciones |
| Periódico | **Pentest manual** (documento DE-03) | Al menos anual o por exigencia BCU | Equipo externo autorizado |
| Continuo | Revisión de **componentes y dependencias** (SCA) | En cada build + mensual | Desarrolladores |
| Continuo | **DLP** sobre canales de salida | 24×7 | Área de seguridad / TI |

> **Analogía:** SAST es el control de calidad en la fábrica, DAST es la prueba del producto ya armado, y el pentest es el inspector externo que llega sin avisar.

---

## 8. DLP: prevención de fuga de datos

### Qué es

DLP significa **Data Loss Prevention** (prevención de pérdida de datos). Es un conjunto de controles cuyo trabajo es **impedir que información confidencial salga de la organización por canales no autorizados** — o al menos detectarlo y registrarlo.

> **Analogía:** en una fábrica con materiales secretos, el DLP es el guardia en la salida que revisa qué lleva cada empleado en el bolso. No prohíbe salir: revisa que lo que sale sea lo que puede salir.

### Los tres modos del DLP

| Modo | Dónde mira | Ejemplo |
|---|---|---|
| **Red** (*network*) | El tráfico de salida de la red | Un correo con números de tarjeta que sale a un dominio personal |
| **Endpoint** | El equipo del usuario | Copiar un archivo a un USB, imprimir, captura de pantalla |
| **Almacenamiento** | Los datos en reposo | Descubrir un archivo de datos personales guardado sin cifrar en un disco compartido |

### Qué hace en la práctica

- **Bloquea**: no deja que el correo salga si contiene un número de cédula en masa.
- **Avisa**: alerta al área de seguridad para que analice el caso.
- **Registra**: deja evidencia del intento (quién, qué, cuándo, hacia dónde).
- **Descubre**: encuentra datos sensibles donde no deberían estar.

---

## 9. Fuga de datos: vías típicas y cómo prevenirlas

La fuga no siempre es un ciberataque. Muchas veces es un descuido. Estas son las vías más frecuentes:

| Vía de fuga | Ejemplo | Cómo se previene |
|---|---|---|
| **Correo electrónico** | Enviar una planilla con datos personales a un correo externo | DLP de correo + reglas de envío + clasificación |
| **USB / dispositivos removibles** | Copiar datos a un pendrive | Bloqueo o control de USB + cifrado + registro |
| **Impresora** | Imprimir una nómina y olvidarla en la bandeja | Impresión segura con PIN + DLP de impresión |
| **Nube personal** | Subir un archivo a una cuenta personal | Bloqueo de nubes no autorizadas + DLP de red |
| **Capturas de pantalla** | Fotografiar la pantalla con el celular | Watermarking + política + concientización |
| **Exfiltración por red** | Enviar datos a un servidor externo (malware o filtrado) | DLP de red + EDR (INFRA-05) + reglas de salida |

La prevención no es una sola herramienta: es la suma de **DLP + clasificación de la información (PR-03) + minimización + cifrado + políticas claras + concientización (PR-02)**.

> **Regla de oro:** si un dato **no debe salir**, debe estar **clasificado** como confidencial y **controlado por herramienta**, no solo "por buena voluntad".

---

## 10. Clasificación de la información: la base de todo

El DLP solo sabe qué bloquear si antes sabemos **qué es cada dato**. Por eso el kit pide clasificar la información (documento **PR-03**) y registrarlo en el Documento de Seguridad (**URCDP-01**).

| Nivel | Ejemplo | ¿Puede salir? |
|---|---|---|
| **Pública** | Brochures, datos de contacto institucionales | Sí, libremente |
| **Uso interno** | Procedimientos, organigramas | Solo con autorización |
| **Confidencial** | Datos personales, nóminas, resultados | No, salvo caso autorizado |
| **Secretos bancarios** | Información de clientes, credenciales | Nunca sin autorización formal |

> **Dato personal:** según la ley uruguaya (Ley 18.331 y Decreto 64/020), el dato personal **no debe salir del tratamiento sin autorización**. Aunque el receptor sea una empresa del mismo grupo, la salida requiere justificación y registro.

---

## 11. Controles complementarios

El DLP no trabaja solo. Se apoya en toda la "caja de herramientas" del kit:

| Control | Documento del kit | Para qué sirve |
|---|---|---|
| **Cifrado** de datos en reposo y en tránsito | PR-03 | Si el dato se escapa, no se puede leer |
| **Gestión de accesos** (mínimo privilegio) | PR-01 | Menos gente puede llegar a los datos confidenciales |
| **Copias de seguridad** seguras | PR-05 | Recuperarse de un incidente sin pagar rescate |
| **Correo con DLP** | INFRA-06 (este) | Filtra envíos hacia afuera |
| **Bloqueo de USB** | Política del SGSI | Cierra el canal físico |
| **Watermarking** (marcas de agua) | Política del SGSI | Si hay captura, se sabe de qué equipo salió |
| **Informes de exfiltración** | INFRA-06 (este) | Miden intentos y permiten mejorar |

---

## 12. Evidencias a conservar

Para demostrar ante BCU, Agesic y URCDP que los controles existen y funcionan, guarda:

- ☐ **Reporte SAST** del build con fecha, herramienta, proyecto y estado de los hallazgos.
- ☐ **Reporte DAST** con fecha, alcance, ambiente y **puntuación CVSS** de cada hallazgo.
- ☐ **Plan de remediación**: qué se encontró, quién lo corrige y para cuándo.
- ☐ **Reporte DLP**: eventos bloqueados, revisados y resueltos (mensual).
- ☐ **Registro de permisos de dispositivos removibles**: quién tiene autorización y por qué.

> El detalle de cómo armar y presentar estas evidencias está en el módulo **INFRA-08 (Evidencias a Presentar)**.

---

## 13. Relación con el kit

| Documento | Cómo se conecta |
|---|---|
| **PR-07** | Define el proceso de seguridad en el desarrollo; este módulo da la técnica |
| **DE-03** | Pentest manual y respuesta: complemento del DAST automatizado |
| **URCDP-01** | Documento de Seguridad: clasificación y medidas que protegen datos personales |
| **URCDP-05** | Evaluación de Impacto (EIPD) cuando el tratamiento es de alto riesgo |
| **BCU (RNRCSF)** | Riesgo tecnológico de las aplicaciones y de la información confidencial |
| **ID-04** | Inventario de riesgos: los hallazgos SAST/DAST alimentan la matriz de riesgo |
| **PR-03** | Clasificación, cifrado y minimización: base del DLP |
| **PR-02** | Concientización: las personas son la primera y última línea contra la fuga |

> **Checklist del lector**
> - ☐ Puedo explicar la diferencia entre SAST y DAST con una analogía.
> - ☐ Conozco las herramientas que el Banco autoriza para cada prueba.
> - ☐ Sé qué es el OWASP Top 10 y por qué ninguna herramienta lo cubre solo.
> - ☐ Identifico las vías de fuga y qué control corresponde a cada una.
> - ☐ Supe qué evidencias debo conservar para el SGSI.

---

**Documentos relacionados:** ID-04, PR-01, PR-02, PR-03, PR-05, PR-07, DE-03, BCU-02, URCDP-01, URCDP-05, MATRIZ-001.
