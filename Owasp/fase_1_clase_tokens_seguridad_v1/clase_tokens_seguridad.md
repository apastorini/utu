# Tokens de identidad, de Basic al DPoP — Clase completa

**Guion + explicación + laboratorio de seguridad de APIs**
Versión 2.0 · Foco: seguridad ofensiva *autorizada* y defensa · Incluye el caso ID Uruguay.
Aborda la seguridad de APIs desde **todos los enfoques**: qué se mira, cómo se defiende y para quién.

---

## Índice

0. [Cómo usar esta clase y reglas de ética/legal](#0-cómo-usar-esta-clase-y-reglas-de-éticolegal)
1. [El mapa completo: todos los enfoques para abordar la seguridad de APIs](#1-el-mapa-completo-todos-los-enfoques-para-abordar-la-seguridad-de-apis)
2. [Taxonomía de las APIs: qué estamos protegiendo exactamente](#2-taxonomía-de-las-apis-qué-estamos-protegiendo-exactamente)
3. [Módulos técnicos (M1–M11): de Basic al DPoP](#3-módulos-técnicos)
4. [La seguridad de API más allá del token: el cuerpo completo, dominio por dominio](#4-la-seguridad-de-api-más-allá-del-token-el-cuerpo-completo-dominio-por-dominio)
   - Identidad · Autenticación · Autorización · Gateway · Control de consumo · Validación · Transporte · Exposición de datos · Inventario · Observabilidad · Cadena de suministro · Resiliencia · Negocio · Threat modeling · Zero Trust · Criptografía · Gobierno · Cumplimiento · Privacidad · Anti-patrones
5. [Entorno de laboratorio seguro](#5-entorno-de-laboratorio-seguro)
6. [Glosario de atajos](#6-glosario-de-atajos)
7. [Plantilla de reporte responsable](#7-plantilla-de-reporte-responsable)
8. [Bibliografía](#8-bibliografía)

## 0. Cómo usar esta clase y reglas de ética/legal

### Cómo está armada
Cada tecnología (Basic → DPoP) se explica con la misma estructura:

1. **Idea** — qué problema resuelve y cuándo nació (primera aparición).
2. **Guion para explicar** — lo que decís en la charla / clase (texto hablado).
3. **Ejemplo que puedo hacer** — algo concreto, reproducible, sin riesgo.
4. **Vulnerabilidades y cómo comprobarlas** — el "modo seguridad": qué puede fallar y cómo se verifica **en un entorno propio o autorizado**.
5. **Defensa** — qué control mitiga ese fallo y con qué norma se referencia.

**Pero la clase no termina en los tokens.** El documento se amplió para cubrir la seguridad de una API **completa**:
- La **Sección 1** presenta *todos* los enfoques posibles para hablar de seguridad de APIs (30 lentes, agrupados en qué se mira, cómo se defiende y para quién).
- La **Sección 2** es una **taxonomía**: qué tipos de API existen (REST, GraphQL, gRPC, eventos, webhooks…) y qué riesgo trae cada uno.
- La **Sección 3** son los **módulos técnicos de tokens** (M1–M11), de Basic al DPoP.
- La **Sección 4** recorre, **dominio por dominio**, todo lo demás que hay que asegurar (autorización, gateway, rate limiting, validación, transporte, inventario, observabilidad, cadena de suministro, cumplimiento, privacidad, anti-patrones…).

### Reglas de ética y legal (leé esto antes de cualquier prueba)

> **Regla de oro:** probá vulnerabilidades únicamente contra (a) sistemas que vos construiste, (b) laboratorios diseñados para ser vulnerables, o (c) sistemas para los que tenés **autorización por escrito** y un alcance definido.
>
> Probar autenticación, robar/reutilizar tokens o manipular identificadores de objetos en sistemas de terceros **sin autorización** es acceso no autorizado y es delito, aunque "sólo sea mirar" o aunque el token lo hayas copiado de tu propio navegador.

Buenas prácticas mínimas:
- **Tu cuenta, tu sesión, tu cliente:** observar tu propio token en tu propio navegador es legítimo; reutilizarlo contra otros recursos o cuentas, no.
- **Alcance escrito:** si vas a probar algo que no es tuyo, pedí permiso y guardá el correo/RFC de autorización.
- **No exfiltrás datos:** si encontrás algo, demostrá el acceso con el mínimo dato necesario (p. ej. tu propio ID), nunca volcás la base.
- **Divulgación responsable:** reportá al dueño del sistema o a su CERT. En Uruguay: **CERTuy (AGESIC)** — https://www.gub.uy/centro-nacional-respuesta-incidentes-seguridad-informatica/
- **Laboratorios recomendados:** OWASP crAPI, DVGA, OWASP Juice Shop, VAmPI, PortSwigger Web Security Academy (labs de JWT y OAuth).

*Herramientas de la clase:* `curl`, navegador con DevTools, Burp Suite Community / ZAP, `jwt_tool`, `PyJWT` (Python), `docker`, `gitleaks`/`ggshield`.

---

## 1. El mapa completo: todos los enfoques para abordar la seguridad de APIs

No existe **una** forma de mirar la seguridad de una API. Existen muchas, y cada una ilumina algo distinto y esconde el resto. Esta sección es deliberadamente exhaustiva: primero el catálogo completo de enfoques —agrupados en tres familias según si miran *qué*, *cómo* o *para quién*—, y al final una tabla comparativa y una recomendación de combinación.

**Las tres preguntas que ordenan todo:**
- **Familia A — qué se mira:** el objeto de estudio (arquitectura, actores, datos, estilos, ciclo de vida).
- **Familia B — cómo se defiende:** los mecanismos (autorización, criptografía, tráfico, validación, observabilidad, secretos).
- **Familia C — para quién y por qué:** el contexto (riesgos, gobierno, cumplimiento, privacidad, negocio, madurez).

---

### Familia A — Enfoques según QUÉ se mira

**1.1 Enfoque por capas de arquitectura.**
- *Pregunta central:* ¿en qué capa vive el control y en qué capa vive el atacante?
- *Qué mira:* cliente → red → gateway → autenticación → autorización → lógica de negocio → datos.
- *Cuándo usarlo:* charlas mixtas y diseño; es el más didáctico.
- *Si lo omito:* creo que "arreglé la autenticación" equivale a "arreglé la API".

**1.2 Enfoque por actor: persona, sistema y delegación.**
- *Pregunta central:* ¿quién invoca la API y en nombre de quién?
- *Qué mira:* humano (browser/app), máquina (M2M), y el caso híbrido de un servicio actuando por una persona.
- *Cuándo usarlo:* MFA, identidades no humanas, delegación (OAuth), consentimiento.
- *Si lo omito:* aplico el modelo de la persona a la máquina (pedir "MFA" a un microservicio) o dejo credenciales eternas en CI.

**1.3 Enfoque por ciclo de vida de la credencial.**
- *Pregunta central:* ¿en qué eslabón se puede robar, reutilizar o perpetuar este token?
- *Qué mira:* emisión → transporte → almacenamiento → uso → renovación → revocación → expiración.
- *Cuándo usarlo:* es el enfoque de esta clase; permite hablar de access, refresh e ID token y sus relaciones.
- *Si lo omito:* hablo solo de firma y olvido rotación y revocación, donde ocurren la mayoría de los incidentes.

**1.4 Enfoque por ciclo de vida del software (shift-left).**
- *Pregunta central:* ¿en qué fase del desarrollo se introduce y se detecta el riesgo?
- *Qué mira:* diseño → desarrollo → build/CI → test → despliegue → runtime → retiro/decomisión.
- *Cuándo usarlo:* para mover la seguridad a la izquierda y justificar automatización.
- *Si lo omito:* la seguridad queda como un pentest al final, cuando ya es caro corregir.

**1.5 Enfoque por superficie de ataque.**
- *Pregunta central:* ¿desde dónde me atacan y con qué activo?
- *Qué mira:* cliente (token en JS/localStorage) · red (TLS, proxies) · backend (validación de claims) · cadena de suministro (CI, dependencias) · negocio (abuso de flujos).
- *Cuándo usarlo:* para no subestimar las fugas "aburridas pero reales".
- *Si lo omito:* ignoro que la mayoría de los secretos filtrados son de máquinas, no de personas.

**1.6 Enfoque por dato y contrato.**
- *Pregunta central:* ¿qué datos cruzan la API y qué promete el contrato?
- *Qué mira:* esquema (OpenAPI/AsyncAPI/protobuf/SDL), validación de tipos, campos sensibles, versionado, compatibilidad, contract testing.
- *Cuándo usarlo:* equipos con diseño API-first y catálogo de servicios.
- *Si lo omito:* el contrato y la implementación divergen, y aparecen campos no documentados y "shadow fields".

**1.7 Enfoque por estilo de API.**
- *Pregunta central:* ¿cómo cambian los riesgos según el paradigma (REST, GraphQL, gRPC, SOAP, WebSocket, webhooks)?
- *Qué mira:* cada estilo tiene su clase de riesgo: sobre-fetch y query depth en GraphQL; métodos y enums por defecto en gRPC; XML y firma en SOAP; canales persistentes y autorización por mensaje en WebSocket; SSRF y firmas de webhook.
- *Cuándo usarlo:* cuando la organización usa más de un estilo (casi siempre).
- *Si lo omito:* aplico recetas de REST a GraphQL o a eventos y dejo huecos.
- *Ver detalle:* Sección 2, "Taxonomía de las APIs".

**1.8 Enfoque por protocolo y transporte.**
- *Pregunta central:* ¿qué garantiza (y qué no) el canal?
- *Qué mira:* HTTP/1.1, HTTP/2, HTTP/3/QUIC, TLS, mTLS, cabeceras, CORS, HSTS, PN.
- *Cuándo usarlo:* cuando hay mTLS, service mesh, proxies que terminan TLS o clientes legacy.
- *Si lo omito:* asumo cifrado extremo a extremo donde hay terminación en un proxy.

**1.9 Enfoque por tipo de consumidor.**
- *Pregunta central:* ¿la API es para mi propio front, para un partner, para el público o para uso interno?
- *Qué mira:* first-party (SPA/móvil), interno (servicio a servicio), partner (contratos bilaterales), público/open (sin relación previa), marketplace de terceros.
- *Cuándo usarlo:* para elegir el esquema de identidad y el nivel de confianza correcto.
- *Si lo omito:* trato igual a un socio contractual y a un cliente anónimo de Internet.

**1.10 Enfoque por modelo de despliegue.**
- *Pregunta central:* ¿dónde corre la API y qué cambia en cada modelo?
- *Qué mira:* monolito, microservicios, serverless/funciones, edge, contenedores, service mesh, on-prem, nube, híbrido/multi-nube.
- *Cuándo usarlo:* arquitecturas distribuidas y migraciones a la nube.
- *Si lo omito:* aplico supuestos de red plana a un entorno con malla, sidecars y tráfico este-oeste.

**1.11 Enfoque por tipo de identidad (humana vs. no humana).**
- *Pregunta central:* ¿cuántas identidades de máquina tengo frente a las humanas?
- *Qué mira:* NHIs (service accounts, CI tokens, workloads, dispositivos), su ciclo de vida y su rotación.
- *Cuándo usarlo:* cuando el grueso del tráfico es M2M (la mayoría de las APIs).
- *Si lo omito:* las NHIs quedan sin dueño ni rotación, y son las que más se filtran.

---

### Familia B — Enfoques según CÓMO se defiende

**1.12 Enfoque por paradigma de confianza.**
- *Pregunta central:* ¿confío en *quién sos* (identidad) o en *qué tenés* (posesión/capability)?
- *Qué mira:* ACL vs. capabilities, perimetral vs. Zero Trust, identidad vs. posesión.
- *Cuándo usarlo:* para dar profundidad y justificar DPoP/mTLS.
- *Si lo omito:* no entiendo por qué "robar el token" es un ataque completo.

**1.13 Enfoque por modelo de autorización.**
- *Pregunta central:* ¿cómo se decide si esta identidad puede hacer esta acción sobre este objeto?
- *Qué mira:* RBAC, ABAC, ReBAC, PBAC, policy-as-code (p. ej. OPA), autorización a nivel de objeto y de función.
- *Cuándo usarlo:* siempre que haya objetos por usuario (casi siempre).
- *Si lo omito:* la autenticación funciona y la autorización no; ahí vive BOLA.

**1.14 Enfoque criptográfico y de gestión de claves.**
- *Pregunta central:* ¿qué firma, qué cifra y quién custodia las claves?
- *Qué mira:* JOSE (JWS/JWE/JWK/JWA), PKI, mTLS, KMS/HSM, rotación de claves, criptografía poscuántica.
- *Cuándo usarlo:* diseño de confianza técnica y cumplimiento.
- *Si lo omito:* claves de larga vida, algoritmos débiles y firmas mal validadas.

**1.15 Enfoque por control de tráfico.**
- *Pregunta central:* ¿qué límites y políticas aplico al caudal?
- *Qué mira:* gateway, rate limiting, cuotas, throttling, concurrencia, bot management, geo/IP policy.
- *Cuándo usarlo:* abuso, scraping, fuerza bruta, protección de disponibilidad.
- *Si lo omito:* una API costosa se convierte en un vector de denegación de servicio barato.

**1.16 Enfoque por validación y saneamiento.**
- *Pregunta central:* ¿confío en la entrada? (correcto: no).
- *Qué mira:* inyección (SQL/NoSQL/comandos), SSRF, XXE, deserialización insegura, mass assignment, plantillas, type confusion.
- *Cuándo usarlo:* revisión de código y pruebas ofensivas.
- *Si lo omito:* el token es impecable y la API es inyectable.

**1.17 Enfoque por observabilidad y respuesta.**
- *Pregunta central:* ¿cómo sé que algo pasa, y qué hago cuando pasa?
- *Qué mira:* logs, trazas, métricas, SIEM, detección de anomalías, revocación, respuesta a incidentes.
- *Cuándo usarlo:* operación y seguridad conjuntas.
- *Si lo omito:* un token robado se usa durante semanas sin que nadie lo note.

**1.18 Enfoque por secretos, identidad de máquina y cadena de suministro.**
- *Pregunta central:* ¿dónde viven los secretos y quién los controla?
- *Qué mira:* secret managers, rotación, escaneo de repos/CI, SBOM/SCA, seguridad del pipeline, terceros.
- *Cuándo usarlo:* cuando hay CI/CD y dependencias externas (siempre).
- *Si lo omito:* los secretos terminan en un repo público y las dependencias introducen el próximo Codecov.

---

### Familia C — Enfoques según PARA QUIÉN y POR QUÉ

**1.19 Enfoque por OWASP API Security Top 10.**
- *Pregunta central:* ¿cuál de los diez riesgos tengo hoy y cómo lo pruebo?
- *Qué mira:* BOLA, Broken Authentication, BOPLA, consumo sin límites, BFLA, flujos de negocio, SSRF, misconfiguración, inventario, consumo inseguro.
- *Cuándo usarlo:* auditoría práctica y priorización.
- *Si lo omito:* me quedo en la teoría de tokens sin cubrir autorización, negocio ni configuración.

**1.20 Enfoque por framework de threat modeling.**
- *Pregunta central:* ¿qué puede salir mal en este diseño, sistemáticamente?
- *Qué mira:* STRIDE, LINDDUN (privacidad), PASTA, DREAD, árboles de ataque, diagramas de flujo de datos.
- *Cuándo usarlo:* antes de escribir código; en revisiones de diseño.
- *Si lo omito:* resuelvo síntomas y no causas, y repito los mismos errores en cada API.

**1.21 Enfoque por audiencia.**
- *Pregunta central:* ¿a quién le hablo y qué le importa?
- *Qué mira:* devs (cómo lo implemento), arquitectos (cómo lo diseño), seguridad (cómo lo rompo/defiendo), management (cuánto cuesta).
- *Cuándo usarlo:* cualquier charla o documento; define el nivel de detalle.
- *Si lo omito:* pierdo al público por exceso o por defecto de profundidad.

**1.22 Enfoque por cumplimiento y regulatorio.**
- *Pregunta central:* ¿qué me exige la norma y cómo se traduce en controles?
- *Qué mira:* ISO 27001, PCI DSS, NIST, y en Uruguay el marco de AGESIC, la Ley 18.331 y el Decreto 66/025 (con obligación de reporte a CERTuy).
- *Cuándo usarlo:* gobierno, empresas reguladas, sector financiero y salud.
- *Si lo omito:* no puedo traducir "cumplir" en controles concretos de token y de API.

**1.23 Enfoque por privacidad y protección de datos.**
- *Pregunta central:* ¿qué datos personales cruzan la API y con qué base legal?
- *Qué mira:* minimización, PII, consentimiento, retención, residencia, derecho de acceso y supresión.
- *Cuándo usarlo:* cuando hay datos de personas (siempre).
- *Si lo omito:* una API segura puede seguir siendo ilegal por tratar datos de más.

**1.24 Enfoque por modelo de negocio y abuso económico.**
- *Pregunta central:* ¿qué gana un atacante con esta API, más allá de robar datos?
- *Qué mira:* scraping, escalping, abuso de cupones, creación masiva de cuentas, fraude, reventa de datos y de capacidad.
- *Cuándo usarlo:* productos con valor transaccional o de datos.
- *Si lo omito:* protejo la confidencialidad y me comen por el bolsillo con abuso de lógica.

**1.25 Enfoque por madurez y gobierno.**
- *Pregunta central:* ¿en qué nivel estoy y hacia dónde voy?
- *Qué mira:* OWASP SAMM, modelos de madurez, catálogo de APIs, dueño por API, métricas, capacitación, centro de excelencia.
- *Cuándo usarlo:* programas de seguridad y planes a mediano plazo.
- *Si lo omito:* hago acciones sueltas sin un camino de mejora.

**1.26 Enfoque por economía del atacante (modelo de amenaza).**
- *Pregunta central:* ¿cuánto le cuesta al atacante y cuánto me cuesta a mí defenderme?
- *Qué mira:* costo de obtención de credenciales, valor del objetivo, superficie automatizable, ROI del ataque.
- *Cuándo usarlo:* priorizar defensas con mejor relación costo/beneficio.
- *Si lo omito:* invierto donde no duele y dejo abierto lo barato de explotar.

**1.27 Enfoque histórico/evolutivo.**
- *Pregunta central:* ¿por qué cada tecnología nació, qué resolvió y qué dejó abierto?
- *Qué mira:* Basic/Digest → cookies → API keys → OAuth 1.0 → bearer → JWT → OIDC/PKCE → mTLS/DPoP.
- *Cuándo usarlo:* enseñanza de fundamentos y decisiones de arquitectura.
- *Si lo omito:* repito modas sin entender los términos de intercambio.

**1.28 Enfoque académico/formal.**
- *Pregunta central:* ¿qué principios de diseño se están violando?
- *Qué mira:* principios de Saltzer & Schroeder (mínimo privilegio, separación de privilegios, mediación completa, diseño abierto), capabilities, *confused deputy*, *trust boundaries*.
- *Cuándo usarlo:* para dar rigor y citar fuentes primarias.
- *Si lo omito:* discuto herramientas sin principios, y las herramientas cambian; los principios no.

**1.29 Enfoque por resiliencia y disponibilidad.**
- *Pregunta central:* ¿qué pasa cuando algo falla o me saturan?
- *Qué mira:* DoS/DDoS, consumo de recursos, backpressure, circuit breakers, degradación elegante, continuidad.
- *Cuándo usarlo:* APIs críticas y de alto tráfico.
- *Si lo omito:* la seguridad se enfoca en confidencialidad y olvida la disponibilidad como parte de la tríada CIA.

**1.30 Enfoque por anti-patrones.**
- *Pregunta central:* ¿qué errores concretos se repiten en la industria?
- *Qué mira:* catálogo de malas prácticas (token en URL, secreto hardcodeado, autorización solo en el front, `alg` del token, paginación sin límites…).
- *Cuándo usarlo:* como checklist rápido de revisión y para capacitación.
- *Si lo omito:* repito los mismos errores con distinto nombre.

---

### Tabla comparativa de enfoques

| Familia | Enfoque | Pregunta central | Mejor para | Si lo omito… |
|---|---|---|---|---|
| A | Capas de arquitectura | ¿Dónde vive el control? | Arquitectos | Confundo authn con authz |
| A | Actor (persona/sistema/delegación) | ¿Quién invoca? | MFA y M2M | Aplico mal la MFA |
| A | Ciclo de vida de la credencial | ¿En qué eslabón falla? | Charla integral de tokens | Olvido rotar y revocar |
| A | Ciclo de vida del software | ¿En qué fase se detecta? | Shift-left | Seguridad tardía y cara |
| A | Superficie de ataque | ¿Desde dónde atacan? | Cubrir fugas reales | Ignoro CI y repos |
| A | Dato y contrato | ¿Qué promete el contrato? | API-first | Aparecen shadow fields |
| A | Estilo de API | ¿Cómo cambian los riesgos? | Organizaciones multiestilo | Recetas de REST mal aplicadas |
| A | Protocolo y transporte | ¿Qué garantiza el canal? | mTLS, mesh, proxies | Asumo cifrado extremo |
| A | Tipo de consumidor | ¿Para quién es la API? | Elegir identidad y confianza | Trato igual a socio y anónimo |
| A | Modelo de despliegue | ¿Dónde corre? | Distribuido y nube | Supuestos de red plana |
| A | Identidad humana vs. no humana | ¿Cuántas NHIs tengo? | M2M y CI | NHIs sin dueño ni rotación |
| B | Paradigma de confianza | ¿Identidad o posesión? | Profundidad conceptual | No entiendo el riesgo bearer |
| B | Modelo de autorización | ¿Puede hacer esto sobre esto? | Objetos por usuario | Dejo BOLA abierto |
| B | Criptografía y claves | ¿Quién firma y custodia? | Confianza técnica | Claves eternas y débiles |
| B | Control de tráfico | ¿Qué límites aplico? | Abuso y disponibilidad | DoS barato y scraping |
| B | Validación y saneamiento | ¿Confío en la entrada? | Código y pentest | API inyectable |
| B | Observabilidad y respuesta | ¿Cómo lo detecto y actúo? | Operación y SOC | Token robado invisible |
| B | Secretos y cadena de suministro | ¿Dónde viven los secretos? | CI/CD y terceros | Próximo Codecov |
| C | OWASP API Top 10 | ¿Qué riesgo tengo? | Auditoría y priorización | Teoría sin práctica |
| C | Threat modeling | ¿Qué puede salir mal? | Diseño | Síntomas, no causas |
| C | Audiencia | ¿A quién hablo? | Cualquier comunicación | Pierdo al público |
| C | Cumplimiento | ¿Qué me exigen? | Gobierno y regulado | Norma sin control |
| C | Privacidad | ¿Qué datos trato? | PII | Seguro pero ilegal |
| C | Negocio y abuso | ¿Qué gana el atacante? | Productos transaccionales | Me comen el margen |
| C | Madurez y gobierno | ¿Hacia dónde voy? | Programa de seguridad | Acciones sueltas |
| C | Economía del atacante | ¿Cuánto le cuesta? | Priorizar defensas | Invierto donde no duele |
| C | Histórico/evolutivo | ¿Por qué nació? | Fundamentos | Repito modas |
| C | Académico/formal | ¿Qué principio se viola? | Rigor y citas | Herramienta sin principio |
| C | Resiliencia | ¿Qué pasa si falla? | APIs críticas | Olvido disponibilidad |
| C | Anti-patrones | ¿Qué errores se repiten? | Capacitación y revisión | Mismos errores |

### Recomendación de combinación

Para **una charla o un programa completo** conviene una combinación, no un solo lente:

1. **Enfoque histórico/evolutivo + ciclo de vida de la credencial** para el hilo narrativo (por qué estamos donde estamos).
2. **Enfoque por actor + por modelo de autorización** para el corazón técnico (persona vs. sistema; objeto vs. función).
3. **Enfoque por OWASP API Top 10 + por estilo de API** como atlas de vulnerabilidades y de superficies.
4. **Enfoque por threat modeling + por ciclo de vida del software** para el "cómo se trabaja".
5. **Enfoque por cumplimiento, privacidad y negocio** para el "por qué le importa a la organización".

Esa mezcla es, exactamente, la estructura del resto de este documento: los enfoques son el mapa; las secciones siguientes son el territorio.

## 2. Taxonomía de las APIs: qué estamos protegiendo exactamente

Antes de los tokens conviene saber **de qué estamos hablando** cuando decimos "API". No todas se parecen, y cada familia trae su propia clase de riesgo. Esta sección clasifica las APIs por cinco ejes: estilo, consumidor, despliegue, contrato y tipo de dato. Sirve como índice mental para elegir qué mirar en cada caso.

### 2.1 Por estilo o paradigma

| Estilo | Cómo funciona | Fortalezas | Riesgos característicos |
|---|---|---|---|
| **REST** | Recursos sobre HTTP, verbos, representaciones JSON | Simple, cacheable, ubicuo | BOLA/BFLA, over-fetching, versionado laxo, IDOR por IDs predecibles |
| **GraphQL** | Un endpoint, el cliente pide la forma | Eficiencia de datos, tipado fuerte | Consultas profundas/costosas, *introspection* expuesta, BOLA por resolver, sobre-exposición de campos |
| **gRPC / Protobuf** | RPC binario sobre HTTP/2 | Rendimiento, contrato estricto | Reflexión expuesta, métodos no previstos, falta de inspección por proxies/WAF |
| **SOAP / XML** | Mensajes XML con WSDL | Contrato formal, WS-Security | XXE, WS-Security mal configurado, *entity expansion*, complejidad |
| **WebSocket** | Canal bidireccional persistente | Tiempo real | Autenticación solo al abrir el canal; autorización por mensaje; cross-site hijacking |
| **Webhooks / callbacks** | El proveedor llama a tu URL | Integración push | SSRF, falta de firma (HMAC), replay, URLs no validadas |
| **Event-driven / async** | Colas y tópicos (Kafka, AMQP, SNS/SQS) | Desacople y escala | Autorización por tópico, *event injection*, secretos de broker, datos en claro en el bus |
| **Serverless functions** | Endpoints efímeros (functions) | Escala y costo variable | Configuración por defecto, IAM de la función, inyección de eventos, *cold start* como vector de abuso |

**Regla práctica:** las recetas de REST (validar ID, verbo, rol) **no** se trasladan automáticamente a GraphQL, eventos o WebSocket. Cada estilo exige su propio modelo de autorización.

### 2.2 Por tipo de consumidor

- **First-party:** tus propios front-ends (SPA, móvil). El reto es proteger el artefacto en un cliente que el usuario controla.
- **Interno (servicio a servicio):** tráfico este-oeste. El reto es la identidad de workload y el mínimo privilegio.
- **Partner / B2B:** relación contractual con otra organización. El reto es la federación, la auditoría y el alcance acordado.
- **Público / open API:** sin relación previa con el consumidor. El reto es el abuso, el scraping y la ausencia de contexto de confianza.
- **Marketplace de terceros:** aplicaciones de otros sobre tus datos. El reto es el consentimiento, el alcance y la revocación granular.

### 2.3 Por modelo de despliegue

- **Monolito:** un solo proceso; la seguridad es más simple de razonar y de auditar.
- **Microservicios:** muchos servicios; la autorización debe ser **consistente** en todos, y el tráfico interno también se protege.
- **Serverless:** piezas efímeras; la configuración y los permisos por función son el punto crítico.
- **Edge / CDN:** la ejecución cerca del usuario; cuidado con dónde termina TLS y dónde viven los secretos.
- **Service mesh:** sidecars con mTLS e identidad de workload; cambia dónde se aplican las políticas.
- **On-prem / nube / híbrido / multi-nube:** cambian el perímetro, la residencia de datos y el modelo de identidad.

### 2.4 Por contrato y versionado

- **OpenAPI / Swagger:** contrato de REST; base para validación, documentación y pruebas.
- **AsyncAPI:** el equivalente para eventos y mensajes.
- **GraphQL SDL / protobuf / WSDL:** contratos de sus estilos.
- **Versionado:** en la URL (`/v1`), en cabecera o por *media type*. El riesgo real es el **inventario**: versiones viejas, beta y de prueba que siguen vivas y sin protección (Api9 de OWASP).

### 2.5 Por tipo de dato y dominio

- **PII / datos personales:** sujetos a privacidad y base legal.
- **Financiero:** PCI DSS si hay datos de tarjeta.
- **Salud:** marcos específicos según jurisdicción.
- **Gobierno / identidad ciudadana:** alto impacto; en Uruguay, ID Uruguay y el marco de AGESIC.

> **Cómo se conecta con el resto del documento:** la Sección 1 dice *con qué lente miro*; esta Sección 2 dice *qué estoy mirando*; la Sección 3 (módulos M1–M11) entra en el mundo de los **tokens**; y la Sección 4 recorre, **dominio por dominio**, todo lo demás que hay que asegurar en una API.

## 3. Módulos técnicos

> En cada módulo: **Idea · Guion · Ejemplo práctico · Vulnerabilidades y cómo comprobarlas · Defensa.**
> Recordá: las comprobaciones ofensivas van **sólo** contra laboratorios o entornos autorizados.

---

## M1 — HTTP Basic / Digest (1999)

### Idea
Autenticación HTTP clásica: el cliente manda credenciales (Basic: `usuario:contraseña` en Base64) en **cada** petición. **Primera aparición: RFC 2617, junio de 1999**; Digest añade un hash y un `nonce`; **RFC 7616 (agosto de 2015)** moderniza Digest con SHA-256 y reemplaza a la 2617.

### Guion para explicar
"Basic es como darle a alguien la llave de tu casa para que entre a revisar una habitación: le das la llave, no un permiso para esa habitación. Viaja en cada request, y si mirás el valor, no está cifrado: está codificado. Base64 no es seguridad; es transporte tolerante a caracteres."

### Ejemplo que puedo hacer
```bash
# Endpoint público de práctica (no es un sistema de terceros real)
curl -v -u usuario:clave https://httpbin.org/basic-auth/usuario/clave

# Mirar la cabecera
curl -s -u usuario:clave https://httpbin.org/basic-auth/usuario/clave -D -
```
En el navegador: DevTools → Network → cualquier request con `Authorization: Basic ...` → copiá el valor y decodificalo:
```bash
echo -n "dXN1YXJpbzpjbGF2ZQ==" | base64 -d
```

### Vulnerabilidades y cómo comprobarlas (en tu entorno)
| Vulnerabilidad | Cómo se comprueba (autorizado) |
|---|---|
| Credenciales reutilizadas por request | Interceptá una request con un proxy (Burp/ZAP) en **tu** app y reenviala: sigue autenticando todo el tiempo |
| No hay "logout" real | Guardá la cabecera y usala de nuevo tras "cerrar sesión" en tu app: si sigue funcionando, no hay revocación |
| Base64 ≠ cifrado | Decodificá la cabecera (comando de arriba) |
| Fuerza bruta | En tu app, medí si hay rate-limit/lockout enviando N intentos de tu propio usuario de prueba |
| Credenciales en logs/URLs | Buscá en tus propios logs si aparece el header; en APIs de prueba, probá una URL con user:pass |

### Defensa
TLS obligatorio, migrar a tokens/OIDC, rate-limit y lockout, nunca loguear credenciales, nunca usar Basic en URLs.

---

## M2 — Cookies y sesiones (1996)

### Idea
El servidor guarda el estado y el navegador repite un **identificador de sesión** en una cookie. **Primera aparición: especificación de cookies de Netscape, 1996; RFC 2109 (1998); RFC 6265 (abril de 2011)** es la vigente.

### Guion para explicar
"La sesión en servidor es segura para la web tradicional y mala para APIs: el estado no escala, no delega y no cruza clientes. Pero trae dos problemas clásicos que seguimos viendo: robo de cookie por XSS y CSRF."

### Ejemplo que puedo hacer
- En tu app: login → DevTools → Application → Cookies → observá `HttpOnly`, `Secure`, `SameSite`.
- Con `curl` (tu app): `curl -c cookies.txt -d 'user=...&pass=...' https://TU-APP/login` y luego `curl -b cookies.txt https://TU-APP/perfil`.

### Vulnerabilidades y cómo comprobarlas
| Vulnerabilidad | Cómo se comprueba (autorizado/lab) |
|---|---|
| Cookie sin `HttpOnly` → XSS la lee | En un lab (PortSwigger XSS / Juice Shop) inyectá `document.cookie` y verificá que la sesión es accesible |
| Sin `SameSite` → CSRF | Lab de CSRF de PortSwigger: formulario que dispara una acción autenticada |
| Session fixation | En tu app: fijá vos el valor de la cookie antes del login y verificá si el servidor la respeta |
| Sesión no se invalida al logout | Reutilizá la cookie vieja tras logout: si sirve, no hay revocación |
| Falta de rotación de sesión | Compará el ID de sesión antes y después del login (debería cambiar) |

### Defensa
`HttpOnly` + `Secure` + `SameSite`, rotar el ID en el login, invalidar en el servidor al logout, tiempo de inactividad, tokens CSRF.

---

## M3 — API keys (mediados de los 2000)

### Idea
No tienen RFC: son práctica de industria, popularizadas con la nube (**access keys de AWS, 2006**). Identifican a un sistema, **no autentican a una persona**, y por defecto **no expiran**.

### Guion para explicar
"La API key es el bearer token más usado y menos cuidado del mundo. Es un identificador estático que se mete en un archivo, en una variable de entorno o —peor— en el JavaScript de un frontend, donde cualquiera lo lee. Identifica, no autentica."

### Ejemplo que puedo hacer
```bash
curl -H "X-API-Key: TU_CLAVE_DE_PRUEBA" https://httpbin.org/headers
```
Para mostrar extracción: en **tu propia** web/app, DevTools → Network → buscá `api_key`, `apikey`, `token` en las requests del cliente.

Escaneo de **tus propios** repos (no de terceros):
```bash
# gitleaks o ggshield sobre tu repo
gitleaks detect --source . -v
```

### Vulnerabilidades y cómo comprobarlas
| Vulnerabilidad | Cómo se comprueba |
|---|---|
| Clave hardcodeada en el cliente | DevTools/descompilar tu app; buscá el secreto en el bundle |
| Clave en el repositorio | `gitleaks`, `ggshield`, `trufflehog` sobre tu repo/CI |
| Sin expiración ni rotación | Verificá que la clave sigue funcionando después de meses (tu entorno) |
| Sin scope ni límites | Usá la clave "de solo lectura" para intentar una operación de escritura en tu API |
| Sin rate limit | Enviá N requests a tu endpoint con la misma key y medí 429/423 |

### Defensa
Rotación, revocación, scope, IP allowlist, rate limit, secret manager, detección en CI (secret scanning). Dato para citar: **28,65 M de secretos nuevos en commits públicos de GitHub en 2025 (+34 %)** — [GitGuardian, State of Secrets Sprawl 2026](https://blog.gitguardian.com/the-state-of-secrets-sprawl-2026/).

---

## M4 — OAuth 1.0 (firma HMAC) (2007 / 2010)

### Idea
Antes del bearer, OAuth **firmaba cada request** con HMAC-SHA1 y un secreto compartido. **Especificación comunitaria, diciembre de 2007; RFC 5849, abril de 2010.** El token no se puede copiar y reusar: la firma está atada al método, la URL y los parámetros. Es el ancestro conceptual de DPoP.

### Guion para explicar
"OAuth 1.0 era la antítesis del bearer: nada de mandar un string reutilizable, cada request se firmaba. Más seguro en teoría, carísimo en la práctica: canonicalizar parámetros, secretos compartidos por cada par de servicios, y una pesadilla en móviles. El mundo eligió simplicidad y nació el bearer."

### Ejemplo que puedo hacer
Construir la firma conceptualmente en Python (sin llamar a nadie):
```python
import hmac, hashlib, base64, urllib.parse
method = "GET"
url = "https://api.ejemplo.com/recurso"
params = {"oauth_consumer_key": "key", "oauth_nonce": "abc123", "oauth_timestamp": "1700000000"}
base = "&".join([method, urllib.parse.quote(url, safe=""),
                 urllib.parse.quote("&".join(f"{k}={params[k]}" for k in sorted(params)), safe="")])
signature = base64.b64encode(hmac.new(b"secreto", base.encode(), hashlib.sha1).digest())
print("oauth_signature =", urllib.parse.quote(signature))
```
Mostrá que cambiar **un solo parámetro** invalida la firma: eso es lo que el bearer no tiene.

### Vulnerabilidades y cómo comprobarlas
| Vulnerabilidad | Cómo se comprueba (lab propio) |
|---|---|
| Errores de canonicalización | Alterá el orden/encoding de parámetros y observá si la firma valida o no |
| Secreto compartido filtrado | Si el secreto se filtra, se pueden firmar requests: probá en tu implementación de práctica |
| Sin anti-replay (nonce/timestamp) | Reenviá la misma request firmada dos veces contra tu lab: ¿la acepta? |
| Complejidad de implementación | Compará líneas de código vs. un flujo bearer |

### Defensa
Nonce + timestamp anti-replay, secretos por par, TLS. Hoy: migrar a DPoP en vez de reimplementar OAuth 1.0.

---

## M5 — Bearer token (OAuth 2.0) (2012)

### Idea
OAuth 2.0 separa autorización de autenticación y entrega al cliente un **access token**: un string con alcance y vida. **RFC 6749, octubre de 2012**; su uso bearer, **RFC 6750, octubre de 2012**. La regla: **quien tiene el token, lo usa.** La propia norma lo admite en **RFC 6749 §10.3**: *"This specification does not provide any methods for the resource server to ensure that an access token presented to it by a given client was issued to that client by the authorization server."*

### Guion para explicar
"El bearer ganó por simplicidad: un string en una cabecera, sin firmar cada request, sin secretos compartidos. El precio está escrito en la norma: el servidor de recursos no puede saber si quien presenta el token es a quien se le emitió. Ese es el corazón de esta clase."

### Ejemplo que puedo hacer
```bash
# Con TU token (de tu cuenta / tu entorno)
curl -H "Authorization: Bearer TU_TOKEN" https://httpbin.org/bearer

# Inspeccionar la forma de la cabecera en DevTools de TU app
# Network -> Request Headers -> Authorization: Bearer eyJ...
```
**Demostración de reutilización (sólo tu cuenta, tu entorno):** copiá tu token a un `curl` en otra terminal —atelada al mismo host de tu app— y comprobá que el servidor lo acepta sin más. Eso *es* el punto de la charla; no lo hagas contra terceros.

### Vulnerabilidades y cómo comprobarlas
| Vulnerabilidad | Cómo se comprueba (tu entorno) |
|---|---|
| Replay: el token no está atado al cliente | Copiá el token y usalo desde otro cliente (curl) contra tu API |
| Token en URL/query | Buscá tokens en logs, en el header `Referer` o en el historial (tu app) |
| Vida demasiado larga | Decodificá `exp` (JWT) o medí cuánto sigue vivo un token opaco |
| Sin revocación | Probá tu token después de "cerrar sesión": si sigue válido, no hay revocación (RFC 7009) |
| Sobre-privilegio | Pedí un token con scope amplio en tu client y usá un endpoint fuera del scope mínimo |
| Transporte inseguro | Verificá que tu API sólo acepta HTTPS y rechaza el token por HTTP |

### Defensa
Vida corta, `aud` estricto, scope mínimo, revocación (RFC 7009) e introspección (RFC 7662), nunca en query (**RFC 9700, enero 2025** lo prohíbe), y sender-constrained (M9).

---

## M6 — JWT (2010 / 2015)

### Idea
**JWT (JSON Web Token)**: `header.payload.signature`, base64url. **Primer borrador: 28 de diciembre de 2010; RFC 7519, mayo de 2015** (familia JOSE: JWS 7515, JWE 7516, JWK 7517, JWA 7518). El payload **no está cifrado**: está firmado. El header trae `alg` y `kid`.

### Guion para explicar
"Un JWT es como una credencial plastificada: firmada, no sellada. Cualquiera lee el contenido. Y guarda una trampa: el header dice con qué algoritmo se firmó; si el validador le hace caso al token en lugar de a su configuración, el atacante elige el algoritmo. De ahí salen `alg: none`, la confusión RS256→HS256 y la inyección de `kid`."

### Ejemplo que puedo hacer
Generá y decodificá tu propio JWT (nada de terceros):
```python
# pip install pyjwt
import jwt
token = jwt.encode({"sub": "123", "scope": "read", "iss": "https://mi-lab"}, "secreto", algorithm="HS256")
print(token)
print(jwt.decode(token, "secreto", algorithms=["HS256"]))
```
Decodificá el payload **sin verificar** para ver que base64 no oculta nada:
```bash
python -c "import base64,sys; p=sys.argv[1].split('.')[1]; print(base64.urlsafe_b64decode(p+'='*(-len(p)%4)).decode())" eyJ...
```

### Vulnerabilidades y cómo comprobarlas (en laboratorio propio)

**Montá un lab minúsculo** (Flask) que acepte JWT, para probar los clásicos sin tocar a nadie:

```python
# lab_jwt.py  ->  flask run  (sólo local)
from flask import Flask, request, jsonify
import jwt
app = Flask(__name__)
@app.route("/perfil")
def perfil():
    tok = request.headers.get("Authorization", "").replace("Bearer ", "")
    try:
        # ATAJO VULNERABLE A PROPÓSITO: confía en el alg del token y usa la clave como secreto
        data = jwt.decode(tok, "secreto", algorithms=None, options={"verify_signature": True})
        return jsonify(data)
    except Exception as e:
        return str(e), 401
```

| Ataque | Cómo se comprueba (contra EL LAB de arriba) |
|---|---|
| `alg: none` | Generá un token con `{"alg":"none"}` y sin firma; si el servidor lo acepta, es vulnerable |
| Confusión RS256→HS256 | Si el server verifica con clave pública, intentá firmar con HS256 usando esa clave pública como secreto |
| `kid` injection | Enviá `kid` apuntando a un archivo/ruta conocida; observá si cambia la clave usada |
| Secreto débil (HS256) | Crackeá **tu propio** token con `hashcat`/`jwt_tool` y un diccionario: `jwt_tool eyJ... -C -d rockyou.txt` |
| Sin `exp` / `aud` | Generá un token sin expiración o con otra `aud` y probá si el endpoint lo acepta |
| Firma no verificada | Cambiá un byte del payload sin refirmar; si pasa, no verifica firma |

Con `jwt_tool` (todo contra tu lab):
```bash
git clone https://github.com/ticarpi/jwt_tool
python3 jwt_tool.py eyJ... -M at      # prueba alg none
python3 jwt_tool.py eyJ... -C -d wordlist.txt   # crackea el secreto
```

### Defensa
`alg` **desde la configuración del validador**, nunca del token; verificar `iss`, `aud`, `exp`, `nbf`; claves fuertes; rotación de claves (`kid` correcto); validar contra JWKS; y **RFC 8725 (febrero 2020)** + [OWASP JWT Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html).

---

## M7 — OIDC, authorization code, PKCE e ID token (2014)

### Idea
**OpenID Connect Core 1.0**, final aprobado el **26 de febrero de 2014**, es la capa de identidad sobre OAuth 2.0. Flujo *authorization code*: **RFC 6749 §4.1 (2012)**, código de un solo uso (si se reutiliza, la norma exige denegar y revocar, §4.1.2). **PKCE: RFC 7636, agosto de 2015.** El **ID token** es un JWT que dice *quién* es la persona y *cómo* se autenticó (`auth_time`, `amr`, `acr`) y **no sirve para acceder a recursos**.

### Guion para explicar
"El authorization code es el cupón de un solo uso que cambia un artefacto público —lo que viaja por el navegador— por uno privado. PKCE le agrega un candado: aunque te roben el código, no lo podés canjear sin el verificador. Y el ID token es el DNI que te muestran en la puerta, no el pase que te ponen en la muñeca para entrar al recinto."

### Ejemplo que puedo hacer (flujo, sin llamar a sistemas de terceros)
Con tu propio lab (Keycloak local, o el proyecto de práctica):
```
1) /authorize?response_type=code&client_id=lab&redirect_uri=http://localhost/cb
   &scope=openid&state=RANDOM&code_challenge=...&code_challenge_method=S256
2) el usuario (vos) se autentica en el lab
3) /cb?code=XXXX&state=RANDOM
4) POST /token  code=XXXX + code_verifier=...  -> access_token, id_token, refresh_token
```
Decodificá el **id_token** localmente y mirá `iss`, `aud`, `auth_time`, `amr`, `nonce`.

### Vulnerabilidades y cómo comprobarlas
| Vulnerabilidad | Cómo se comprueba (lab propio / tu integración) |
|---|---|
| Sin PKCE → código interceptable | Repetí el flujo **de tu lab** sin `code_challenge` e intentá canjear el código con otro cliente |
| `redirect_uri` laxa | En tu lab, probá un `redirect_uri` no registrado (p. ej. un subpath o dominio parecido) |
| Falta de `state` → CSRF | Iniciá el login y manipulá/eliminá el `state`: ¿acepta la respuesta? |
| Falta de `nonce` → replay del ID token | Reutilizá un ID token viejo en tu cliente y verificá si valida `nonce`/`auth_time` |
| *Mix-up attack* | En lab con dos IdP, cruzá respuestas entre proveedores |
| ID token usado como access token | Probá mandar el ID token al endpoint de recursos de tu lab: debe rechazarse |
| Rate-limit en login | Enviá N intentos de tu usuario de práctica y medí bloqueo |

### Defensa
PKCE obligatorio (lo exige **RFC 9700**), `redirect_uri` exacta, `state` y `nonce`, validar `iss`/`aud`/`exp`/`nonce` en el RP, no usar el ID token como access token.

---

## M8 — Refresh token (2012)

### Idea
Token de vida larga que **sólo** se usa contra el endpoint de token para obtener nuevos access tokens. **RFC 6749 §§1.5 y 6 (octubre de 2012)**; rotación sugerida en **§10.4**; **RFC 9700 (enero de 2025)** la exige para clientes públicos. Revocación: **RFC 7009, octubre de 2013**.

### Guion para explicar
"El access token es el boleto de la función; el refresh token es la acreditación que te deja pedir uno nuevo sin volver a la taquilla. La rotación convierte al refresh en un artefacto de un solo uso: si un atacante lo usa, el legítimo lo delata."

### Ejemplo que puedo hacer
En tu lab: guardá el refresh token, pedí un access token nuevo y observá si el refresh **cambia** (rotación) y si el viejo queda **inválido** (detección de reuso).

### Vulnerabilidades y cómo comprobarlas
| Vulnerabilidad | Cómo se comprueba (lab/tu integración) |
|---|---|
| Sin rotación | Reutilizá el mismo refresh token dos veces: si ambas funcionan, no hay rotación |
| Sin detección de reuso | Usá el refresh viejo después de rotar: si sigue vivo, no hay detección |
| Vida infinita | Verificá si hay `exp` o política de caducidad absoluta |
| Almacenamiento inseguro | En tu app, buscá el refresh en `localStorage`/almacenamiento sin cifrar del cliente |
| Refresh usado contra la API de recursos | Mandá el refresh a un endpoint de recursos de tu lab: debe rechazarse |

### Defensa
Rotación + detección de reuso, vida absoluta, binding al cliente, almacenamiento seguro, revocación en logout/cambio de contraseña.

---

## M9 — mTLS y DPoP (sender-constrained) (2020 / 2023)

### Idea
Atar el token a su portador. **mTLS + token atado a certificado: RFC 8705, febrero de 2020.** **DPoP: RFC 9449, octubre de 2023.** Con DPoP, el cliente firma cada request con su clave privada; el token sólo sirve presentado con esa prueba.

### Guion para explicar
"Si el problema del bearer es que cualquiera que lo tenga lo usa, la solución es exigir algo más que la posesión. mTLS ata el token al certificado; DPoP ata el token a una clave privada que el cliente prueba en cada request. Es la idea de OAuth 1.0, pero bien integrada. RFC 9700 (2025) ya los recomienda."

### Ejemplo que puedo hacer
DPoP — construí una prueba **conceptual** con Python (sin servidor real):
```python
# La prueba DPoP es un JWT firmado por el CLIENTE con su clave privada
# Header típico: {"typ":"dpop+jwt","alg":"ES256","jwk":{...}}
# Claims: jti (único), htm (método), htu (URL), iat
# El servidor rechaza si htm/htu no coinciden con el request, o si el jti se repite
```
Para una prueba real y segura, levantá **Keycloak en Docker** (soporta DPoP) y hacé el flujo contra tu propio Keycloak.

### Vulnerabilidades y cómo comprobarlas
| Vulnerabilidad | Cómo se comprueba (lab propio) |
|---|---|
| DPoP sin validar `htm`/`htu` | Cambiá el método o la URL del request manteniendo la prueba: ¿lo acepta? |
| Replay de la prueba (`jti`) | Reenviá la misma prueba dos veces: debe rechazarse |
| `ath` ausente | Presentá el access token sin atar la prueba al token (`ath` = hash del access token) |
| Nonce de servidor ignorado | Si el server exige nonce, probá sin él |
| mTLS mal configurado | En tu lab, probá presentar un token atado a un certificado **sin** el certificado: debe fallar |

### Defensa
Validar `htm`, `htu`, `jti` (anti-replay), `ath`, `alg` permitido; rotación de claves; y **RFC 9449 / RFC 8705**.

---

## M10 — OWASP API Security Top 10 (laboratorio)

Éste es el "atlas" para elegir qué probar. Cada ítem con su forma de comprobarlo **en un lab** ([OWASP API Security Top 10 – 2023](https://owasp.org/API-Security/editions/2023/en/0x11-t10/)).

| # | Riesgo | Cómo se comprueba (lab) | Herramienta |
|---|---|---|---|
| API1 | **BOLA** — Broken Object Level Authorization | Con **tu** token, cambiá el ID del objeto por otro del lab (`/api/pedidos/1234` → `5678`) y mirá si devuelve datos ajenos | Burp/Postman + ffuf |
| API2 | **Broken Authentication** | Login sin rate-limit, JWT sin validar, credenciales por defecto | jwt_tool, Burp Intruder |
| API3 | **BOPLA / Mass Assignment** | Mandá campos extra (`"rol":"admin"`, `"saldo":999`) y observá si se aplican | Postman |
| API4 | **Unrestricted Resource Consumption** | Paginación gigante, búsquedas costosas; medí CPU/latencia en tu lab | ab, k6 |
| API5 | **BFLA** — Broken Function Level Authorization | Con usuario normal, llamá endpoints de admin (`/admin/...`) | Postman |
| API6 | **Sensitive Business Flows** | Repetí un flujo (cupón, reintento de pago) más veces de las permitidas | script propio |
| API7 | **SSRF** | Endpoint que recibe una URL: apuntalo a `http://localhost`/metadatos en tu lab | Burp Collaborator |
| API8 | **Misconfiguration** | CORS `*`, errores verbosos, métodos no documentados, TLS débil | nuclei, ZAP |
| API9 | **Improper Inventory** | Versiones viejas (`/v1`, `/beta`, `/swagger`) expuestas | ffuf, gobuster |
| API10 | **Unsafe Consumption** | Confiar en datos de terceros (respuesta de otro servicio) sin validar | manual |

**Laboratorios oficiales/diseñados para romper:** [OWASP crAPI](https://owasp.org/projects/crapi), DVGA, [OWASP Juice Shop](https://owasp.org/www-project-juice-shop/), VAmPI, y los labs de [PortSwigger Web Security Academy](https://portswigger.net/web-security) (JWT, OAuth, BOLA).

---

## M11 — Caso ID Uruguay (laboratorio ético)

### Qué es
**ID Uruguay** es el proveedor de identidad del Estado uruguayo, gestionado por **AGESIC**. Se integra vía **OpenID Connect** y su documentación técnica muestra el *token endpoint* `/oidc/v1/token` con **`token_type` = "Bearer"**, un **ID token** en formato **JWT**, y llamadas a *UserInfo* con `Authorization: Bearer`.

- Documentación oficial: https://www.gub.uy/agencia-gobierno-electronico-sociedad-informacion-conocimiento/comunicacion/publicaciones/documentacion-tecnica-id-uruguay/documentacion-tecnica-id-uruguay/id-0
- Guía "Desarrollo seguro" (AGESIC): https://www.gub.uy/agencia-gobierno-electronico-sociedad-informacion-conocimiento/sites/agencia-gobierno-electronico-sociedad-informacion-conocimiento/files/Desarrollo%20seguro.pdf

### La línea ética, explícita
- **Vos podés** ejecutar el flujo completo **con tu propia cuenta** y **tu propio cliente de desarrollo** (o el de tu organización, con autorización interna). Eso incluye observar tus tokens, decodificar tu ID token y verificar la configuración de *tu* integración.
- **Vos NO podés** (sin autorización escrita de AGESIC): probar `redirect_uri` de otros clientes, atacar al IdP, automatizar intentos, intentar acceder a datos de otras personas, ni "probar qué pasa si cambio el token".
- Si querés evaluar el IdP en sí: coordiná con **AGESIC** y canalizá por **CERTuy** (`https://www.gub.uy/centro-nacional-respuesta-incidentes-seguridad-informatica/`).

### Verificación defensiva de tu integración (permitida y útil)

| Control | Cómo verificarlo en TU cliente | Resultado esperado | Referencia |
|---|---|---|---|
| **PKCE obligatorio** | Revisá tu `authorization` request: `code_challenge` + `code_challenge_method=S256` | Presente y verificado | RFC 7636 / RFC 9700 |
| **`redirect_uri` exacta** | Confirmá que registrás la URI exacta (sin comodines) y que tu app la valida | Coincidencia exacta | RFC 9700 |
| **`state` y `nonce`** | Verificá que tu app genera y valida ambos | Presentes, aleatorios, de un solo uso | OIDC Core |
| **Validación del ID token** | Tu código debe validar `iss`, `aud`, `exp`, `nonce` y la firma contra JWKS | Todo validado | OIDC Core |
| **ID token no se usa como access token** | Buscá en tu código si el ID token se envía a APIs | Nunca | OIDC Core |
| **Vida del access token** | Decodificá tu access token (si es JWT) y mirá `exp` | Corta y acorde al riesgo | RFC 9068 |
| **Rotación de refresh token** | Pedí dos veces seguidas: ¿el refresh cambia y el viejo se invalida? | Rotación + detección de reuso | RFC 9700 |
| **Revocación / logout** | Cerrá sesión y probá si tu token/refresh ya no sirve | Invalidado | RFC 7009 |
| **Transporte** | Verificá TLS y que no se acepten tokens por HTTP ni en query | Sólo HTTPS + header | RFC 9700 |
| **Almacenamiento en tu cliente** | ¿Dónde guarda tu app el token? (memoria/cookie `HttpOnly` mejor que `localStorage`) | Sin acceso por JS | OWASP |

### Guion de la demostración en clase (sin riesgo)
1. Mostrá la **documentación oficial** de ID Uruguay: `token_type: Bearer` e ID token JWT. *(Cero pruebas a nadie.)*
2. En **tu propio** login con tu cuenta, abrí DevTools → Network y mostrá la respuesta del *token endpoint* y la cabecera `Authorization: Bearer` **enmascarando el token**.
3. Decodificá **tu** ID token en https://jwt.io (es cliente: no viaja a ningún servidor) y leé `iss`, `aud`, `exp`, `auth_time`, `amr`.
4. Cerrá sesión y explicá por qué ese cierre debe invalidar los artefactos.
5. Frase: *"No tocamos ningún sistema ajeno: miramos un billete al portador en nuestra propia billetera."*

---

## 4. La seguridad de API más allá del token: el cuerpo completo, dominio por dominio

Las secciones anteriores cubren **tokens** (Sección 3, módulos M1–M11). Pero una API segura se construye en **todos** los dominios del sistema. Esta sección recorre, uno por uno, cada dominio de seguridad de API, con: qué protege, controles, fallas típicas, cómo se prueba y qué decía ya la bibliografía. Es el complemento que hace que la clase sea completa: el token es una puerta, no el edificio.

> Recordatorio ético: cualquier prueba ofensiva va contra laboratorios o entornos autorizados (ver Sección 0 y la Sección 5 de laboratorio).

### 4.1 Identidad: humana, no humana y delegada

**Qué protege:** saber *quién* o *qué* actúa, antes de decidir *qué puede hacer*.

- **Identidad humana:** personas frente a un proveedor de identidad (OIDC), con sesión, MFA y claims (`sub`, `acr`, `amr`, `auth_time`).
- **Identidad no humana (NHI):** service accounts, workloads, jobs de CI, dispositivos IoT. Su ciclo de vida —nacer, rotar, morir— es donde más falla la industria.
- **Identidad delegada:** un servicio actuando en nombre de una persona (OAuth), con consentimiento, alcance y revocación.

**Controles:** federación de identidad, identidad de workload (p. ej. SPIFFE/SPIRE), credenciales efímeras (STS), rotación automática, mínimo privilegio, inventario y dueño por identidad.

**Fallas típicas:** cuentas compartidas, usuarios genéricos (`admin`, `service`), credenciales de máquina sin expiración, secretos en repos y CI.

**Cómo se prueba (lab/autorizado):** inventariar NHIs; verificar que cada credencial expira y rota; buscar secretos en **tus** repos con `gitleaks`/`gghshield`.

**Fuentes:** NIST SP 800-63-4 (2025); SPIFFE (CNCF, 2017-); GitGuardian, *State of Secrets Sprawl 2026*.

### 4.2 Autenticación: patrones y su evolución

**Qué protege:** comprobar la identidad declarada.

- **Factores:** conocimiento (contraseña), posesión (dispositivo, clave), inherencia (biometría). MFA = dos de tipos distintos.
- **Passwordless y passkeys:** WebAuthn (W3C, 2019) resiste phishing por diseño; alineado con NIST SP 800-63-4 (2025).
- **Entre servicios:** client credentials (RFC 6749 §4.4), `private_key_jwt` (RFC 7523), mTLS (RFC 8705).
- **APIs:** bearer (RFC 6750), y su evolución sender-constrained: DPoP (RFC 9449).

**Fallas típicas:** MFA por SMS, sin rate limit, sin step-up para operaciones sensibles, tokens de vida larga, `alg` tomado del token.

**Cómo se prueba:** N intentos contra **tu** login y medir bloqueo; intentar `alg:none` y confusión HS/RS contra tu lab (ver Sección 5 / Módulo M6).

**Fuentes:** OWASP API2:2023 *Broken Authentication*; NIST SP 800-63-4 (2025).

### 4.3 Autorización: el corazón (donde vive BOLA)

**Qué protege:** decidir si *esta* identidad puede hacer *esta* acción sobre *este* objeto.

- **Modelos:** RBAC (roles), ABAC (atributos), ReBAC (relaciones), PBAC (políticas). En la práctica se combinan.
- **Niveles:** a nivel de **función** (¿puede llamar `/admin`?) y a nivel de **objeto** (¿puede ver el pedido 5678?).
- **Policy as code:** motores como OPA/Rego o Cedar para centralizar y versionar la política.
- **Mediación completa:** toda decisión pasa por un punto de control; nada de "el front ya oculta el botón".

**Fallas típicas (las tres de OWASP API):**
- **BOLA (Api1):** token válido + objeto ajeno. La nº 1 de la lista; ~40 % de los ataques a APIs la involucran.
- **BFLA (Api5):** llamar funciones para las que no hay permiso.
- **BOPLA (Api3) / mass assignment:** controlar propiedades que no deberías (`rol`, `saldo`).

**Cómo se prueba (lab):** con **tu** token, cambiar el ID del objeto; con usuario normal, llamar endpoints de admin; enviar campos extra.

**Fuentes:** OWASP API Security Top 10 (2023); principios de Saltzer & Schroeder (1975); *confused deputy* (Norm Hardy, 1988).

### 4.4 Gateway, API management, service mesh y WAF

**Qué protege:** el punto de entrada y el tránsito entre servicios.

- **API Gateway:** enrutamiento, autenticación, cuotas, transformación, observabilidad en un punto común.
- **API management:** catálogo, versiones, portales, claves, planes, analítica.
- **Service mesh:** mTLS, identidad de workload y políticas entre servicios (este-oeste).
- **WAF:** filtrado de ataques conocidos; complementa, no reemplaza, la validación en la app.

**Fallas típicas:** rutas no documentadas que evitan el gateway, políticas solo en el borde y no en el interior, WAF como única defensa, configuración por defecto.

**Cómo se prueba:** buscar rutas alternativas (`/v1`, `/internal`, `/swagger`, IP directa del servicio) que evadan el gateway; medir si las cuotas se aplican de forma consistente.

**Fuentes:** OWASP API8:2023 *Security Misconfiguration*; Zero Trust (NIST SP 800-207).

### 4.5 Control de consumo y anti-abuso

**Qué protege:** disponibilidad, costo y equidad del servicio.

- **Rate limiting** (por IP, token, usuario, API key), **cuotas** por plan, **throttling**, límites de **concurrencia**.
- **Bot management:** distinguir automatización legítima de abusiva.
- **Límites específicos:** tamaño de request, profundidad de GraphQL, costo de consultas, paginación máxima.

**Fallas típicas:** ausencia de `429`/`Retry-After`, límites solo por IP (trivial de rotar), GraphQL sin límite de profundidad, endpoints costosos sin cuota.

**Cómo se prueba (lab):** enviar N requests y medir si hay `429`; en tu lab GraphQL, enviar una consulta anidada profunda.

**Fuentes:** OWASP API4:2023 *Unrestricted Resource Consumption*.

### 4.6 Validación de entrada e inyección

**Qué protege:** que la entrada no cambie el significado de lo que hace el sistema.

- **Inyección:** SQL, NoSQL, comandos del sistema, LDAP, plantillas (SSTI).
- **SSRF:** el servidor es inducido a pedir una URL interna (metadatos cloud, `localhost`).
- **XXE:** entidades externas XML (SOAP, parsers XML).
- **Deserialización insegura:** objetos que al reconstruirse ejecutan código o cambian estado.
- **Mass assignment:** ver 4.3.
- **Defensa:** validación por lista blanca, tipado estricto, parametrización, deserialización sin código, allowlist de dominios salientes.

**Cómo se prueba (lab):** crAPI/DVGA/Juice Shop; Burp Collaborator para SSRF; PortSwigger labs.

**Fuentes:** OWASP API7:2023 *SSRF*; OWASP Top 10 (2021).

### 4.7 Transporte y red

**Qué protege:** confidencialidad, integridad y autenticidad del canal.

- **TLS** obligatorio; **mTLS** para autenticación mutua; **HSTS**; cifrados modernos; deshabilitar versiones viejas.
- **HTTP/2 y HTTP/3 (QUIC)** cambian supuestos de proxies e inspección.
- **CORS** bien acotado (no `*` con credenciales); **cabeceras de seguridad**.
- **Pinning** en clientes móviles (con sus propios riesgos de operación).

**Fallas típicas:** protocolos obsoletos, terminación TLS en un punto no confiable, CORS permisivo, tokens viajando por HTTP, certificados sin rotación.

**Cómo se prueba:** escanear cifrados (testssl.sh) contra **tu** endpoint; revisar CORS con un origen propio.

**Fuentes:** RFC 9700 (2025); OWASP API8:2023.

### 4.8 Exposición de datos, errores e información

**Qué protege:** no entregar más de lo necesario, ni señalar de más.

- **Data minimization:** devolver solo los campos que el consumidor necesita.
- **Errores:** mensajes verbosos que revelan stack, rutas, versiones o existencia de recursos.
- **Sobre-exposición:** `debug`, *introspection*, endpoints de estado (health, metrics) abiertos.
- **Logs:** nunca registrar tokens, contraseñas ni PII sin protección.

**Cómo se prueba:** provocar errores y leer la respuesta; pedir un recurso inexistente y ver si el error filtra.

**Fuentes:** OWASP API3:2023 *BOPLA*; OWASP API8:2023.

### 4.9 Inventario, versionado y ciclo de vida

**Qué protege:** saber qué APIs existes y cuáles siguen vivas.

- **Descubrimiento y catálogo:** toda API con dueño, propósito y clasificación.
- **Versionado y deprecación:** plan explícito para retirar versiones viejas.
- **Shadow / zombie APIs:** olvidadas, sin mantenimiento, sin protección.

**Fallas típicas:** `/v1` y `/beta` expuestas, documentación pública de endpoints internos, servicios retirados pero accesibles.

**Cómo se prueba:** fuzzing de rutas y versiones contra **tu** entorno; revisar el catálogo.

**Fuentes:** OWASP API9:2023 *Improper Inventory Management*.

### 4.10 Observabilidad, detección y respuesta

**Qué protege:** que puedas ver y reaccionar.

- **Logging** estructurado (sin secretos) y **trazas** distribuidas.
- **SIEM** y detección de anomalías: token usado desde dos geografías, picos de error, enumeración de IDs.
- **Revocación** (RFC 7009) e **introspección** (RFC 7662).
- **Respuesta a incidentes:** playbooks para "token filtrado", "credencial de CI expuesta", "abuso masivo".

**Fallas típicas:** no saber qué tokens están vivos; no poder revocar un refresh; no detectar reuso.

**Cómo se prueba:** simular el robo de **tu** token y verificar si el sistema lo detecta o lo revoca.

**Fuentes:** RFC 7009 (2013); RFC 7662 (2015); NIST SP 800-61 (respuesta a incidentes).

### 4.11 Cadena de suministro y CI/CD

**Qué protege:** que el software y sus dependencias no introduzcan el próximo incidente.

- **Secretos en el pipeline:** escaneo de repos y de CI (`gitleaks`, `ggshield`, `trufflehog`), *secret managers*, rotación.
- **Dependencias:** SBOM, análisis de composición (SCA), fijado de versiones, revisión de mantenedores.
- **Pipeline hardening:** permisos mínimos del runner, aislamiento, *builds* reproducibles, firma de artefactos (SLSA).
- **Consumo de terceros:** no confiar en respuestas de servicios externos sin validar (Api10 de OWASP).

**Fallas típicas:** tokens de CI con permisos amplios, acciones de terceros sin pin de commit, dependencias abandonadas.

**Cómo se prueba:** correr un escáner de secretos en **tu** repo; revisar permisos del `GITHUB_TOKEN` en tu pipeline.

**Fuentes:** OWASP API10:2023 *Unsafe Consumption of APIs*; caso Codecov (2021); SLSA.

### 4.12 Disponibilidad y resiliencia

**Qué protege:** la "A" de la tríada CIA.

- **Resistencia a DoS/DDoS:** límites, *shaping*, absorción en el borde.
- **Backpressure y circuit breakers:** evitar fallos en cascada.
- **Degradación elegante:** responder con lo esencial cuando una dependencia falla.
- **Continuidad:** planes de recuperación, *failover*, pruebas.

**Fallas típicas:** endpoints costosos sin cuota, falta de timeouts, dependencias sin aislamiento.

**Fuentes:** OWASP API4:2023; NIST SP 800-160 (ingeniería de sistemas resilientes).

### 4.13 Lógica de negocio, fraude y abuso

**Qué protege:** que la API se use para lo que fue diseñada.

- **Abusos frecuentes:** scraping, escalping de stock, cupones repetidos, creación masiva de cuentas, *referral fraud*, abuso de reembolsos.
- **Detección:** límites por *flujo* (no solo por request), reglas de negocio, correlación entre identidades y patrones.

**Fallas típicas:** el ataque es una secuencia de llamadas válidas en orden indebido o en exceso.

**Cómo se prueba (lab):** repetir un flujo legítimo más veces de las previstas y observar si el sistema lo frena.

**Fuentes:** OWASP API6:2023 *Unrestricted Access to Sensitive Business Flows*.

### 4.14 Diseño seguro y threat modeling

**Qué protege:** resolver el riesgo **antes** de codificar.

- **Metodologías:** STRIDE (amenazas), LINDDUN (privacidad), PASTA (riesgo), DREAD (priorización), árboles de ataque.
- **Insumos:** diagramas de flujo de datos, límites de confianza, activos, actores.
- **Salida:** amenazas priorizadas con controles y dueños.

**Fallas típicas:** hacer threat modeling una vez y archivarlo; no involucrar a producto.

**Fuentes:** Microsoft STRIDE; OWASP Threat Modeling; NIST SP 800-154.

### 4.15 Zero Trust aplicado a APIs

**Qué protege:** elimina la confianza implícita del perímetro.

- **Principios:** verificar explícitamente, mínimo privilegio, asumir la brecha.
- **En APIs:** cada request se evalúa por identidad y contexto; el tráfico interno también se autentica (mesh/mTLS); políticas por recurso, no por red.
- **En identidad:** sesiones y tokens con vida corta, reevaluación continua, step-up.

**Fuentes:** NIST SP 800-207 (Zero Trust Architecture).

### 4.16 Criptografía y gestión de claves

**Qué protege:** la confianza técnica (firma, cifrado, identidad).

- **JOSE:** JWS (firma), JWE (cifrado), JWK (claves), JWA (algoritmos).
- **PKI y mTLS:** certificados, cadenas, revocación (CRL/OCSP), rotación.
- **Custodia de claves:** KMS/HSM, separación de funciones, rotación, y **preparación poscuántica** (migración a algoritmos resistentes).
- **Errores a evitar:** algoritmos obsoletos, claves compartidas, `alg` desde el token (RFC 8725).

**Fuentes:** RFC 7515–7518 (2015); RFC 8725 (2020); NIST PQC (2024).

### 4.17 Gobierno, madurez y cultura

**Qué protege:** que la seguridad sea **sostenible** y no dependa de héroes.

- **Propiedad:** cada API con dueño, con SLA y con canal de reporte.
- **Madurez:** OWASP SAMM, modelos de madurez de seguridad de API, métricas.
- **Centro de excelencia:** estándares, plantillas, revisión de diseño, capacitación.
- **Diseño como código:** *policy as code*, *infrastructure as code*, pruebas de seguridad en el pipeline.

**Fuentes:** OWASP SAMM; NIST CSF 2.0 (2024).

### 4.18 Cumplimiento y normativa (con Uruguay)

**Qué protege:** que el sistema cumpla lo que la ley y el estándar exigen.

- **Estándares:** ISO/IEC 27001, PCI DSS, NIST, OWASP.
- **Uruguay:**
  - **AGESIC** conduce la estrategia de gobierno digital y ciberseguridad.
  - **Ley 18.331 (2008)** de Protección de Datos Personales y su **Unidad Reguladora (URCDP)**.
  - **Decreto 66/025** de ciberseguridad: obligaciones para organismos y prestadores, incluida la **gestión de incidentes y el reporte a CERTuy**.
  - **CERTuy** (AGESIC): canal oficial de reporte de incidentes — https://www.gub.uy/centro-nacional-respuesta-incidentes-seguridad-informatica/
  - **ID Uruguay**: proveedor de identidad del Estado (OpenID Connect, `token_type: Bearer`), documentación técnica en gub.uy.
- **Traducción a controles:** inventario, gestión de accesos, rotación de secretos, registro de eventos, respuesta a incidentes, divulgación responsable.

### 4.19 Privacidad y protección de datos

**Qué protege:** a las personas cuyos datos tratan las APIs.

- **Principios:** minimización, finalidad, proporcionalidad, retención limitada, residencia, consentimiento.
- **Diseño:** privacidad desde el diseño y por defecto (LINDDUN); *pseudonimización*; cifrado.
- **Derechos:** acceso, rectificación, supresión.
- **En APIs:** no devolver PII de más, no loguearla, no exponerla en errores, y permitir el borrado efectivo (fin del mito "el token es anónimo").

**Fuentes:** Ley 18.331 (Uruguay); URCDP; LINDDUN.

### 4.20 Catálogo de anti-patrones (checklist de lo que NO hacer)

| Anti-patrón | Por qué duele | Qué hacer en su lugar |
|---|---|---|
| Token en la URL/query | Queda en logs, `Referer`, historial, CDN | Cabecera `Authorization` (RFC 9700) |
| Secreto hardcodeado en el cliente | Cualquiera lo extrae del bundle/app | Backend-for-frontend; no confiar en el cliente |
| Autorización solo en el front | El front no es un control | Autorizar en el servidor, a nivel de objeto |
| `alg` tomado del token | `alg:none`, confusión HS/RS | Algoritmo desde la configuración (RFC 8725) |
| JWT de larga vida sin revocación | No se puede cortar | Vida corta + rotación/introspección |
| Refresh token enviado a la API | Confusión de roles | Solo contra el endpoint de token |
| ID token usado como access token | Token para la app, no para el recurso | Access token para la API |
| Firma no verificada | Cualquiera forja tokens | Verificar firma siempre |
| Sin validación de `aud`/`iss` | Token robado de otra app sirve | Validar emisor y audiencia |
| Rate limit solo por IP | Trivial de rotar | Limitar por identidad y por recurso |
| Paginación sin tope | Consumo ilimitado | Límites máximos y cuotas |
| Errores verbosos | Filtran rutas y versiones | Mensajes genéricos al cliente |
| CORS `*` con credenciales | Cualquier sitio llama | Orígenes explícitos |
| mTLS terminado en proxy sin reenvío de identidad | Se pierde la identidad del cliente | Propagar la identidad verificada |
| Cuentas de servicio compartidas | No hay trazabilidad | Identidades únicas y de vida corta |
| API keys eternas | Sin rotación ni revocación | Rotación, revocación, allowlist |
| `introspection`/`debug` abiertos | Fuga de información | Cerrar en producción |
| Versionado incontrolado | Shadow/zombie APIs | Catálogo y deprecación |
| Confiar en datos de terceros | Inyección por cadena de suministro | Validar toda entrada externa (Api10) |
| Logs con tokens o PII | Fuga por observabilidad | Redacción y minimización |

### 4.21 Fuentes ampliadas de esta sección

- **OWASP:** [API Security Top 10 (2023)](https://owasp.org/API-Security/editions/2023/en/0x11-t10/) · [WSTG](https://owasp.org/www-project-web-security-testing-guide/) · [SAMM](https://owasp.org/www-project-samm/) · [Cheat Sheets](https://cheatsheetseries.owasp.org/)
- **NIST:** [SP 800-63-4 (2025)](https://pages.nist.gov/800-63-4/) · [SP 800-207 Zero Trust](https://csrc.nist.gov/pubs/sp/800/207/final) · [SP 800-61 (IR)](https://csrc.nist.gov/pubs/sp/800/61/r2/final) · [Cybersecurity Framework 2.0](https://www.nist.gov/cyberframework)
- **IETF:** RFC 6749 · 6750 · 7515–7519 · 7523 · 7636 · 7662 · 7009 · 8176 · 8252 · 8705 · 8725 · 9068 · 9449 · 9700
- **Uruguay:** [CERTuy](https://www.gub.uy/centro-nacional-respuesta-incidentes-seguridad-informatica/) · [AGESIC](https://www.gub.uy/agencia-gobierno-electronico-sociedad-informacion-conocimiento/) · [Ley 18.331 — URCDP](https://www.gub.uy/unidad-reguladora-control-datos-personales/) · Documentación técnica de [ID Uruguay](https://www.gub.uy/agencia-gobierno-electronico-sociedad-informacion-conocimiento/comunicacion/publicaciones/documentacion-tecnica-id-uruguay/documentacion-tecnica-id-uruguay/id-0)
- **Laboratorios:** [OWASP crAPI](https://owasp.org/projects/crapi) · [Juice Shop](https://owasp.org/www-project-juice-shop/) · [PortSwigger Academy](https://portswigger.net/web-security) · DVGA

## 5. Entorno de laboratorio seguro

Levantá todo con Docker, sin tocar producción de nadie.

```bash
# OWASP crAPI (API intencionalmente vulnerable, con BOLA, JWT, etc.)
docker compose --file https://raw.githubusercontent.com/OWASP/crAPI/develop/deploy/docker/docker-compose.yml up -d

# DVGA (Damn Vulnerable GraphQL Application)
git clone https://github.com/dolevf/Damn-Vulnerable-GraphQL-Application && cd Damn-Vulnerable-GraphQL-Application
docker build -t dvga . && docker run -d -p 5013:5013 dvga

# Keycloak (OIDC/OAuth real para practicar PKCE, refresh, DPoP)
docker run -d -p 8080:8080 -e KEYCLOAK_ADMIN=admin -e KEYCLOAK_ADMIN_PASSWORD=admin quay.io/keycloak/keycloak:latest start-dev

# Juice Shop (web + API)
docker run -d -p 3000:3000 bkimminich/juice-shop
```

Herramientas: Burp Suite Community o ZAP, `jwt_tool`, `ffuf`/`gobuster`, `nuclei`, `gitleaks`/`ggshield`, Postman/Insomnia, `k6`/`ab`.

---

## 6. Glosario de atajos

| Término | Significado |
|---|---|
| **BOLA / IDOR** | Presentar token válido para acceder a objetos de otro (Api1 OWASP). |
| **BOPLA** | Mass assignment / controlar propiedades que no deberías (Api3). |
| **BFLA** | Llamar funciones para las que no tenés permiso (Api5). |
| **Replay** | Reutilizar un artefacto capturado (token, prueba) sin cambios. |
| **Sender-constrained** | Token que exige prueba de posesión (mTLS, DPoP). |
| **PKCE** | Candado del authorization code para clientes públicos (RFC 7636). |
| **`alg: none` / confusión de alg** | Clases de ataque sobre JWT al confiar en el header del token. |
| **AiTM** | Adversary-in-the-Middle: phishing que roba la sesión ya autenticada. |
| **Infostealer / pass-the-cookie** | Malware que roba cookies/tokens del navegador. |
| **MFA fatigue (T1621)** | Bombardeo de pushes hasta obtener aprobación. |
| **NHI** | Identidad no humana (servicio, CI, device). |
| **JWKS** | Conjunto de claves públicas para validar JWTs. |
| **Diff channel** | *Front channel* (navegador) vs *back channel* (servidor a servidor). |

---

### Ampliación del glosario (enfoques, dominios y normativa)

| Término | Significado |
|---|---|
| **API Gateway** | Componente de entrada que enruta, autentica, aplica cuotas y observa el tráfico. |
| **Rate limiting / cuota / throttling** | Límites de caudal por identidad, IP o recurso; base del control de abuso (Api4). |
| **IAM** | Identity and Access Management: administración de identidades y sus permisos. |
| **RBAC / ABAC / ReBAC / PBAC** | Modelos de autorización por roles / atributos / relaciones / políticas. |
| **Policy as code** | Política de autorización versionada y ejecutada por un motor (p. ej. OPA/Rego, Cedar). |
| **NHI** | Non-Human Identity: identidad de servicio, workload, CI o dispositivo. |
| **SPIFFE/SPIRE** | Estándar y proyecto (CNCF) de identidad de workload con rotación automática. |
| **Zero Trust** | Modelo de "verificar siempre, mínimo privilegio, asumir la brecha" (NIST SP 800-207). |
| **SSRF** | Server-Side Request Forgery: inducir al servidor a pedir una URL interna (Api7). |
| **XXE** | XML External Entity: entidades externas en parsers XML. |
| **Deserialización insegura** | Reconstruir objetos a partir de datos no confiables y ejecutar efectos. |
| **Mass assignment (BOPLA)** | El cliente controla propiedades que no debería (Api3). |
| **Shadow / zombie API** | API olvidada o sin mantenimiento, expuesta sin control (Api9). |
| **SBOM / SCA** | Inventario de componentes de software y análisis de dependencias. |
| **Threat modeling / STRIDE / LINDDUN** | Metodologías para anticipar amenazas (seguridad / privacidad). |
| **OWASP SAMM** | Modelo de madurez de seguridad de software. |
| **WAF** | Web Application Firewall: filtrado de ataques conocidos en el borde. |
| **Service mesh** | Malla de servicios con mTLS e identidad de workload (tráfico este-oeste). |
| **JOSE (JWS/JWE/JWK/JWA)** | Familia de firma, cifrado, claves y algoritmos para tokens (RFC 7515–7518). |
| **PKI / KMS / HSM** | Infraestructura de clave pública / gestión de claves / módulo de hardware. |
| **CORS / HSTS** | Política de orígenes cruzados / forzado de HTTPS en el navegador. |
| **Capability / confused deputy** | Facultad de acceso por posesión; problema del "delegado confundido" (Hardy, 1988). |
| **BOLA / BFLA** | Autorización rota a nivel de objeto (Api1) / de función (Api5). |
| **PCI DSS** | Estándar de la industria de tarjetas de pago. |
| **Ley 18.331 (Uruguay)** | Protección de Datos Personales; regula la URCDP. |
| **Decreto 66/025 (Uruguay)** | Obligaciones de ciberseguridad, incluida la gestión de incidentes y el reporte a CERTuy. |
| **CERTuy** | Centro Nacional de Respuesta a Incidentes de Seguridad Informática (AGESIC). |
| **AGESIC** | Agencia de Gobierno Electrónico y Sociedad de la Información y del Conocimiento (Uruguay). |

---

## 7. Plantilla de reporte responsable

```
Asunto: [Divulgación Responsable] Posible <vulnerabilidad> en <sistema>

1. Resumen (2-3 líneas)
2. Impacto estimado (qué datos/acciones compromete)
3. Alcance probado (cuenta propia / cliente de prueba; qué NO se tocó)
4. Pasos de reproducción (mínimos, sin datos de terceros)
5. Evidencia (capturas enmascaradas, timestamps)
6. Recomendación de mitigación
7. Declaración: no se accedió a datos de terceros ni se alteró información
8. Contacto y disponibilidad para coordinar
```

En Uruguay, canal oficial: **CERTuy (AGESIC)** — https://www.gub.uy/centro-nacional-respuesta-incidentes-seguridad-informatica/

---

## 8. Bibliografía

**Normas IETF:** [RFC 2617](https://www.rfc-editor.org/rfc/rfc2617) · [RFC 7616](https://www.rfc-editor.org/rfc/rfc7616) · [RFC 6265](https://www.rfc-editor.org/rfc/rfc6265) · [RFC 5849](https://www.rfc-editor.org/rfc/rfc5849) · [RFC 6749](https://www.rfc-editor.org/rfc/rfc6749) · [RFC 6750](https://www.rfc-editor.org/rfc/rfc6750) · [RFC 6819](https://www.rfc-editor.org/rfc/rfc6819) · [RFC 7009](https://www.rfc-editor.org/rfc/rfc7009) · [RFC 7519](https://www.rfc-editor.org/rfc/rfc7519) · [RFC 7636](https://www.rfc-editor.org/rfc/rfc7636) · [RFC 7662](https://www.rfc-editor.org/rfc/rfc7662) · [RFC 8176](https://www.rfc-editor.org/rfc/rfc8176) · [RFC 8252](https://www.rfc-editor.org/rfc/rfc8252) · [RFC 8705](https://www.rfc-editor.org/rfc/rfc8705) · [RFC 8725](https://www.rfc-editor.org/rfc/rfc8725) · [RFC 9068](https://www.rfc-editor.org/rfc/rfc9068) · [RFC 9449](https://www.rfc-editor.org/rfc/rfc9449) · [RFC 9700](https://www.rfc-editor.org/rfc/rfc9700)

**Identidad y gobierno:** [OpenID Connect Core 1.0](https://openid.net/specs/openid-connect-core-1_0.html) · [NIST SP 800-63-4 (jul 2025)](https://pages.nist.gov/800-63-4/) · [Marco de Ciberseguridad de Uruguay (AGESIC)](https://www.gub.uy/centro-nacional-respuesta-incidentes-seguridad-informatica/tematica/gestion-ciberseguridad)

**OWASP y labs:** [API Security Top 10 2023](https://owasp.org/API-Security/editions/2023/en/0x11-t10/) · [JWT Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html) · [WSTG](https://owasp.org/www-project-web-security-testing-guide/) · [crAPI](https://owasp.org/projects/crapi) · [Juice Shop](https://owasp.org/www-project-juice-shop/) · [PortSwigger Academy](https://portswigger.net/web-security)

**Casos reales:** [Meta "View As" 2018](https://about.fb.com/news/2018/09/security-update/) · [Cloudflare/Okta 2023](https://blog.cloudflare.com/how-cloudflare-mitigated-yet-another-okta-compromise/) · [Okta 2022 (sin impacto en Cloudflare)](https://blog.cloudflare.com/cloudflare-investigation-of-the-january-2022-okta-compromise/) · [Codecov 2021](https://about.codecov.io/security-update/) · [GitGuardian Secrets Sprawl 2026](https://blog.gitguardian.com/the-state-of-secrets-sprawl-2026/) · [Uber 2022 (UpGuard)](https://www.upguard.com/blog/what-caused-the-uber-data-breach)

**Uruguay / ID Uruguay:** [Documentación técnica ID Uruguay (gub.uy)](https://www.gub.uy/agencia-gobierno-electronico-sociedad-informacion-conocimiento/comunicacion/publicaciones/documentacion-tecnica-id-uruguay/documentacion-tecnica-id-uruguay/id-0) · [Desarrollo seguro (AGESIC, PDF)](https://www.gub.uy/agencia-gobierno-electronico-sociedad-informacion-conocimiento/sites/agencia-gobierno-electronico-sociedad-informacion-conocimiento/files/Desarrollo%20seguro.pdf) · [CERTuy](https://www.gub.uy/centro-nacional-respuesta-incidentes-seguridad-informatica/)
