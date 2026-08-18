# AISEC-02 · Marco normativo uruguayo de IA y datos personales

> **Función del MCU 5.0:** Este módulo aterriza los requisitos de cumplimiento (CN) y protección de datos personales (PD) del Marco de Ciberseguridad de Agesic 5.0 sobre el uso de IA: PD.1 (legalidad), PD.2 (veracidad/calidad), PD.4 (consentimiento), PD.5 (seguridad de datos), PD.7 (responsabilidad proactiva) y CN.1 (cumplimiento normativo).
> **ISO/IEC 27001:** Cumplimiento legal y contractual (A.5.31/A.5.34) y protección de datos personales en entornos de cómputo (A.5.35). Referencia de gobernanza específica: ISO/IEC 42001 (Sistema de Gestión de la IA).
> **BCU:** El uso de IA que trata datos de clientes entra en el alcance del RNRCSF y de los EMG: debe estar documentado, autorizado y con evidencia.
> **URCDP:** Es la autoridad de control. Ley 18.331, Decreto 414/009, Decreto 64/020, Ley 19.670 y Decreto 66/025 rigen el tratamiento de datos personales, incluyendo el que hagan las herramientas de IA.
> **Nivel del curso:** 🟡 Practicar

---

## 1. ¿Por qué la ley importa para usar un chatbot?

Pensemos en el siguiente escenario: un funcionario quiere escribir un correo a un cliente moroso. Para "ganar tiempo", copia el nombre, la cédula, el saldo y la situación del cliente en una herramienta de IA gratuita de internet, y le pide: "redactá un correo firme de cobro".

Ese acto, en apariencia inofensivo, es un **tratamiento de datos personales sin base legal ni técnica adecuada**. Le pasamos a un tercero sin contrato, sin registro, sin garantías de seguridad y sin el consentimiento del titular (que, para morosidad de crédito, la ley además exige expreso). Si el cliente se entera o si se fuga ese dato, el Banco queda expuesto a:

- Una **sanción de la URCDP** (multa de hasta 500.000 UI, Ley 18.331 art. 39).
- Un **incidente reportable en 72 horas** (Decreto 64/020).
- Una **observación del BCU** en la supervisión de riesgo operacional/TIC.
- Un daño reputacional difícil de medir.

Esa es la razón de fondo del curso: **la ley no persigue usar IA; persigue tratar datos sin control.**

---

## 2. El mapa normativo uruguayo (lo mínimo que hay que conocer)

| Norma | Qué regula para nosotros |
|---|---|
| **Ley 18.331** (Ley de Protección de Datos Personales) | Principios del tratamiento: legalidad, calidad, finalidad, seguridad (arts. 9 y 10). Consentimiento del titular. Deber de confidencialidad (art. 27). Sanciones (art. 39). |
| **Decreto 414/009** | Reglamenta la Ley 18.331: consentimiento informado, previo, expreso y revocable; categorías especiales de datos (salud, etc.). |
| **Decreto 64/020** | Régimen de **vulneraciones de seguridad** de datos personales: incidentes se notifican a la **URCDP en 72 horas** cuando haya riesgo para los derechos de los titulares. |
| **Ley 19.670** | Fortalece la protección: **responsabilidad proactiva** (privacy by design) y el **Delegado de Protección de Datos (DPD)** en entidades públicas y grandes tratamientos. |
| **Ley 20.212** | Ley de Presupuesto: su **artículo 74** manda al Poder Ejecutivo definir la **Estrategia Nacional de Inteligencia Artificial y Datos** (áreas, etapas y financiación). Refleja el interés del Estado uruguayo en IA con gobernanza. |
| **Decreto 66/025** | Reglamenta el marco de ciberseguridad: RSI institucional, notificación de incidentes al **CERTuy**, gestión de riesgos de seguridad de la información. Aplica al uso de IA si trata datos institucionales. |
| **MCU 5.0 (Agesic)** | Marco de Ciberseguridad del Uruguay: funciones GV, ID, PR, DE, RS, RC y dominios transversales **CN (Cumplimiento normativo y revisiones)** y **PD (Protección de datos personales)**. |
| **ISO/IEC 27001 y 42001** | Referencias internacionales voluntarias: la 27001 para el SGSI y la 42001 para gobernanza de sistemas de IA. No son ley uruguaya, pero sirven de guía de mejores prácticas. |

> **Importante:** Uruguay todavía **no tiene una ley específica de IA**. La regulación vigente se construye con las leyes de datos personales (18.331 y 19.670), el Decreto 64/020, el Decreto 66/025 y el marco de gobernanza que impulsa Agesic. Por eso, el **principio rector es la protección de datos personales**, aunque la herramienta sea un "chatbot".

---

## 3. Lo que el MCU 5.0 exige que revisemos (PD y CN)

El MCU 5.0 de Agesic tiene **72 requisitos**. Los que más tocan la IA son:

| Requisito | Qué significa para el uso de IA |
|---|---|
| **CN.1** Cumplir requisitos normativos | La institución debe conocer y cumplir todas las normas que aplican a sus tratamientos de datos, incluidos los que haga la IA. |
| **PD.1** Legalidad | Todo tratamiento de datos con IA debe tener base legal (consentimiento, ley, contrato). Pegar datos en una web anónima **no tiene base legal**. |
| **PD.2** Veracidad y calidad | Los datos deben ser exactos y actualizados. La IA que inventa (alucinación) no puede ser la única fuente de un dato de cliente. |
| **PD.3** Finalidad | Los datos se usan solo para la finalidad declarada. Una IA de "resúmenes generales" no habilita a procesar datos de clientes. |
| **PD.4** Consentimiento informado | Para datos sensibles y morosidad el consentimiento debe ser **expreso, informado, previo y revocable** (Decreto 414/009). Un correo de cobranza generado con datos sin esa base es un riesgo. |
| **PD.5** Seguridad de los datos | El tratamiento debe implementar medidas técnicas y organizativas (cifrado, control de acceso, registro). Implica que la herramienta de IA usada debe ser **auditable y autorizada**. |
| **PD.6** Reserva | Deber de confidencialidad de quienes tratan datos. La IA externa sin contrato rompe la reserva. |
| **PD.7** Responsabilidad proactiva | Privacy by design: se evalúa el impacto (EIPD) antes de usar una herramienta de IA con datos personales. |
| **PD.8** Derechos de los titulares | Los clientes pueden pedir información, acceso, rectificación, supresión, etc. Si la IA "guardó" datos en una nube externa, el Banco **no puede responder** a esos derechos → incumplimiento directo. |

> **Resumen ejecutivo:** usar IA con datos de clientes solo está bien si la herramienta **está autorizada, tiene base legal, respeta finalidad, permite ejercer derechos, y deja registros**. Eso es exactamente lo que las herramientas oficiales del Banco ofrecen y las cuentas personales no.

---

## 4. Los tres escenarios y su veredicto normativo

| Escenario | ¿Es válido? | Por qué |
|---|---|---|
| Usar el **asistente oficial del Banco** (servidor propio o nube con contrato y garantías) para redactar correos sin datos personales identificables | ✅ Sí | Herramienta autorizada, auditable, sin salida de datos. |
| Usar el asistente oficial con un **borrador anonimizado** (sin nombres, cédulas ni saldos) | ✅ Sí (con revisión humana) | Minimización de datos: principio del art. 9 Ley 18.331. |
| Pegar **cédula, saldo y deuda** de un cliente en **ChatGPT/Claude/Gemini personal** de internet | ❌ No | Fuga de datos personales, sin base legal, sin contrato, sin posibilidad de responder a los derechos del titular (PD.1, PD.5, PD.6, PD.8). |

---

## 5. Qué significa "responsabilidad proactiva" en la práctica (Ley 19.670)

La Ley 19.670 no espera a que ocurra el incidente: exige que el Banco **piense antes**. En términos prácticos para la IA:

1. **Inventariar** qué herramientas de IA se usan (oficiales y las que aparezcan "por la ventana").
2. **Evaluar el impacto** (EIPD) antes de habilitar un uso nuevo con datos personales (PD.7).
3. **Tener un Delegado de Protección de Datos (DPD)** designado y notificado a la URCDP.
4. **Registrar los tratamientos** en el Registro de Bases de Datos (Ley 18.331 art. 22).
5. **Documentar las decisiones**: quién autorizó, con qué base, qué herramienta, qué datos.
6. **Capacitar** al personal: este curso es parte de esa obligación.

---

## 6. El checklist normativo mínimo para usar IA en el Banco

- [ ] La herramienta está **autorizada por escrito** (política de uso aceptable / registro de herramientas aprobadas).
- [ ] Existe **base legal** para los datos que se procesan (consentimiento, contrato o ley).
- [ ] Los datos ingresados respetan la **finalidad** declarada del tratamiento.
- [ ] Se aplica **minimización**: solo los datos estrictamente necesarios, idealmente anonimizados.
- [ ] La herramienta **no envía datos a terceros sin contrato** ni los usa para entrenar modelos.
- [ ] Hay **registros/logs** de uso para auditoría (quién, qué, cuándo, qué datos).
- [ ] Todo resultado tiene **revisión humana** antes de usarse.
- [ ] Se puede responder a un pedido de un titular (acceso, rectificación, supresión) aunque el dato haya pasado por la IA.
- [ ] Si hay una fuga, se puede **notificar a la URCDP en 72 horas** (Decreto 64/020) porque sabemos qué herramienta y qué datos fueron.

---

## 7. Conclusión del módulo

- La ley no prohíbe la IA: prohíbe **tratar datos sin control**.
- Las herramientas oficiales del Banco existen, entre otras cosas, para que **cumplir la ley no le cueste nada al funcionario**.
- Cada vez que un funcionario usa una herramienta personal con datos del Banco, genera un **incumplimiento PD.1/PD.5/PD.6/PD.8** del MCU 5.0 y una posible sanción de la URCDP.
- La **minimización** es el mejor aliado: sin dato personal, no hay problema legal.

> **Ejercicio:** Mire su jornada laboral y liste tres tareas en las que usaría IA. Para cada una, responda: ¿qué datos necesito realmente? ¿Puedo hacerlo sin nombres ni números de clientes? Ese ejercicio es la práctica diaria del principio de minimización.
