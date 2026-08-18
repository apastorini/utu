# INFRA-13 · Guía de Relevamiento: Qué Preguntar y Qué Pedir como RSI

> **Función del MCU 5.0:** Identificar (ID.AM Inventario, ID.RA Evaluación de riesgos) y Gobernar (GV.RR Roles, GV.RM Estrategia de riesgo). Este módulo es la herramienta práctica que el RSI usa para "poner sobre la mesa" la infraestructura real del banco.
> **ISO/IEC 27001:** Apoya la cláusula 4 (contexto y alcance), 6.1 (evaluación de riesgos) y el Anexo A (evidencia de controles); también el requisito de comunicación (cláusula 7.4).
> **BCU:** El relevamiento alimenta los entregables EMG: gobierno y política de riesgo tecnológico (BCU-01), marco de riesgos (BCU-02), función de seguridad (BCU-03) y función de gestión de TI (BCU-04).
> **URCDP:** Lo que se releva permite completar el Documento de Seguridad (URCDP-01) con medidas físicas y lógicas reales.
> **Decreto 66/025:** El relevamiento es el primer paso para demostrar cumplimiento: sin saber qué se tiene, no se puede rendir cuentas al CERTuy ni a la Dirección de Seguridad de la Información de Agesic (arts. 10 y 11).
> **Nivel del curso:** 🔴 Dominar

---

## 1. Por qué este módulo: el RSI no adivina, pregunta

El RSI no es un técnico que configura firewall, pero sí es la persona que **debe saber exactamente qué firewall hay, dónde está, qué reglas tiene y quién lo administra**. Ese conocimiento no se adivina: se releva.

> **Analogía:** si contrataras a un director de seguridad para un edificio, no le pedirías que instale cámaras; le pedirías que te diga cuántas cámaras hay, cuáles funcionan, quién ve las imágenes y cuánto se guardan. Eso es exactamente lo que hace este módulo.

Este módulo es un **banco de preguntas y pedidos de evidencia**, organizado por tema y por interlocutor. El resultado del relevamiento alimenta: el inventario (ID-01), el análisis de riesgos (ID-02/03), el plan de tratamiento (ID-04), el Documento de Seguridad (URCDP-01) y los informes al BCU (BCU-01 a BCU-04).

---

## 2. Las reglas del buen relevamiento

Antes de las preguntas, tres reglas que separan a un RSI que entiende de uno que "hace ruido":

1. **Pedí evidencia, no promesas.** Si te dicen "el firewall está bien configurado", pedí el **export de reglas**. Si te dicen "hacemos backups", pedí el **log de una restauración exitosa**. La promesa sin evidencia no sirve.
2. **Una cosa a la vez, con fecha y responsable.** Cada pedido se hace por escrito, con un plazo y un responsable. El seguimiento es tan importante como el pedido.
3. **Priorizá por riesgo, no por comodidad.** Lo primero que se releva es lo crítico: sistemas que manejan dinero y datos personales, accesos administrativos, conectividad a Internet.

### El pedido formal

Cada pedido debe tener: qué se pide, para qué sirve (norma que lo exige), formato aceptado, plazo y responsable. Ejemplo de encabezado:

| Campo | Ejemplo |
|---|---|
| Pedido N.º | RELEV-001 |
| Tema | Configuración del firewall perimetral |
| Qué se pide | Export de reglas vigentes (archivo) + diagrama de zonas |
| Para qué | Inventario ID-01 · Análisis de riesgos ID-03 · Documento de Seguridad URCDP-01 |
| Formato | PDF o TXT; nombre de archivo con fecha |
| Plazo | 10 días hábiles |
| Responsable | Jefatura de Infraestructura |

---

## 3. Preguntas por tema de infraestructura

Para cada tema, las preguntas "de calle" y "de fondo" que hace el RSI.

### 3.1 Firewalls y perímetro

| Pregunta | Qué revela la respuesta |
|---|---|
| ¿Cuántos firewalls hay? ¿De qué marca y modelo? ¿Dónde están físicamente? | Inventario y criticidad |
| ¿Quién administra cada firewall? ¿Hay más de un administrador? | Separación de funciones (PR-01) |
| ¿Cada cuánto se revisan las reglas? ¿Hay reglas obsoletas o sin propietario? | Higiene de reglas (INFRA-03) |
| ¿El firewall permite tráfico saliente libre a Internet? | Riesgo de exfiltración |
| ¿Hay regla que permita acceso remoto directo a la red interna? | Superficie de ataque |
| ¿El administrador ingresa por consola o por red? ¿Con qué autenticación? | Acceso administrativo |

**Evidencia a pedir:** export de reglas (`pfctl -sr` o equivalente), diagrama de zonas, acta de última revisión de reglas, captura de la política de administración (MFA).

### 3.2 Segmentación, VLAN y DMZ

| Pregunta | Qué revela la respuesta |
|---|---|
| ¿La red interna está dividida en zonas? ¿Cuáles? | Segmentación (INFRA-03) |
| ¿Los servidores de Internet (web, correo) están en una DMZ? | Arquitectura segura |
| ¿El tráfico entre cajas/sucursales y el core está restringido? | Contención de ataques |
| ¿Hay un laboratorio de pruebas separado de producción? | Aislamiento (INFRA-09) |
| ¿WiFi de invitados separado de la red corporativa? | Perímetro lógico |

**Evidencia a pedir:** diagrama de red con zonas y VLAN, lista de redes VLAN con sus funciones, captura de reglas interzona.

### 3.3 Switches, routers y cableado

| Pregunta | Qué revela la respuesta |
|---|---|
| ¿Qué switches y routers hay? ¿Marca, modelo y versión de firmware? | Inventario (ID-01) |
| ¿Hay switch con puertos libres accesibles? | Riesgo de conexión no autorizada |
| ¿Se controlan los puertos de red (802.1X / MAC filtering)? | Control de acceso a la red |
| ¿Los equipos de red tienen contraseña por defecto? | Hardening (INFRA-04) |
| ¿El cableado de la sala de servidores está identificado y ordenado? | Seguridad física (PR-04) |

**Evidencia a pedir:** inventario de dispositivos con firmware, captura de configuración de seguridad de puertos, planilla de revisión de contraseñas.

### 3.4 Monitoreo, logs y SIEM

| Pregunta | Qué revela la respuesta |
|---|---|
| ¿Los logs están centralizados o dispersos? | Madurez del monitoreo (INFRA-12) |
| ¿Cuánto tiempo se conservan los logs? | Cumplimiento (≥12 meses, Decreto 66/025) |
| ¿Hay reglas de alerta? ¿Quién las investiga? | SOC/equipo de respuesta |
| ¿Hay registro de accesos a sistemas críticos? | Trazabilidad (URCDP-01) |
| ¿Las cámaras de seguridad y los accesos físicos registran eventos? | Monitoreo físico |

**Evidencia a pedir:** lista de fuentes de logs conectadas, reporte de retención, ejemplo de una alerta y su tratamiento, captura del SIEM.

### 3.5 Antivirus, EDR y parches

| Pregunta | Qué revela la respuesta |
|---|---|
| ¿Qué antivirus/EDR hay? ¿Cubre el 100% de los equipos? | Cobertura (INFRA-05) |
| ¿Cómo se gestionan los parches de servidores y de firmware? | PR-06 |
| ¿Cuál es el tiempo máximo para aplicar un parche crítico? | SLAs de parcheo |
| ¿Hay equipos sin soporte del fabricante (EOL)? | Riesgo técnico (ID-03) |
| ¿El antivirus detecta malware y se reporta? | Detección (DE-02) |

**Evidencia a pedir:** reporte de cobertura del antivirus/EDR, reporte de parches de los últimos 3 meses, inventario de equipos EOL.

### 3.6 Aplicaciones y desarrollo

| Pregunta | Qué revela la respuesta |
|---|---|
| ¿Qué aplicaciones críticas hay y en qué red viven? | Inventario de sistemas |
| ¿Se hacen análisis SAST/DAST? ¿Con qué frecuencia? | Desarrollo seguro (INFRA-06) |
| ¿El código se versiona y revisa antes de pasar a producción? | SDLC (PR-07) |
| ¿Hay aplicaciones sin documentar o "de las que nadie se acuerda"? | Sistemas sombra (shadow IT) |
| ¿Cómo se controla el acceso de los desarrolladores a producción? | Separación de ambientes |

**Evidencia a pedir:** inventario de aplicaciones, reportes de escaneo SAST/DAST recientes, política de acceso a producción.

### 3.7 Acceso remoto y VPN

| Pregunta | Qué revela la respuesta |
|---|---|
| ¿Qué solución de VPN se usa? ¿Quién puede conectarse? | Acceso remoto (INFRA-02) |
| ¿El acceso remoto usa autenticación de doble factor? | PR-01 |
| ¿Las conexiones VPN se registran y auditan? | Trazabilidad |
| ¿Los contratistas y terceros entran por el mismo canal que los funcionarios? | Riesgo de terceros (PR-08) |

**Evidencia a pedir:** configuración de VPN, política de acceso remoto firmada, listado de usuarios VPN activos.

### 3.8 Respaldo y continuidad

| Pregunta | Qué revela la respuesta |
|---|---|
| ¿Qué sistemas se respaldan? ¿Cada cuánto? | PR-05 |
| ¿Se probó alguna vez la restauración? ¿Cuándo? | Disponibilidad (RC-01/02) |
| ¿Hay copias fuera del sitio? | Resistencia a desastres |
| ¿Las copias se protegen contra ransomware (inmutables/offline)? | Defensa contra ransomware |

**Evidencia a pedir:** log de una restauración exitosa, política de respaldo, acta de la última prueba de restauración.

---

## 4. Preguntas por interlocutor

Cada área responde mejor a preguntas en su idioma. La tabla muestra a quién preguntarle qué:

| Interlocutor | Mejor preguntarle sobre | Por qué |
|---|---|---|
| Jefatura de Infraestructura | Red, servidores, firewalls, backups | Es quien administra los dispositivos |
| Área de Seguridad de la Información | Controles, incidentes, políticas | Es la segunda línea de defensa |
| Área de Desarrollo / TI Apps | Ciclo de vida del software, SAST/DAST | Riesgo en aplicaciones |
| Oficial de Cumplimiento / Riesgo | Normas BCU y de datos, sanciones | Marco regulatorio |
| Usuario de negocio (caja, sucursal) | Cómo usa la red y qué necesita | Disponibilidad percibida |
| Proveedores y terceros | Qué acceden, qué datos ven | Riesgo de cadena de suministro (GV-05) |
| Auditoría Interna | Hallazgos previos, evidencias exigidas | Continuidad de la mejora (BCU-05) |

---

## 5. Priorización del relevamiento: por qué orden preguntar

No todo es igual de urgente. El orden recomendado, de mayor a menor urgencia:

| Prioridad | Tema | Por qué primero |
|---|---|---|
| 1 | Sistemas que mueven dinero y datos personales | Impacto máximo (BCU + URCDP) |
| 2 | Acceso administrativo y cuentas privilegiadas | Es lo primero que ataca un intruso |
| 3 | Perímetro (firewall, VPN, Internet) | Puerta de entrada |
| 4 | Monitoreo y logs | Sin esto no hay detección |
| 5 | Parches y antivirus | Defensas básicas |
| 6 | Aplicaciones y desarrollo | Riesgo por código |
| 7 | Respaldo y continuidad | Para recuperarse |

---

## 6. El entregable del relevamiento: la ficha por tema

Cada tema relevado termina en una **ficha de infraestructura** que alimenta a las plantillas del kit. Ejemplo de ficha:

| Campo | Contenido |
|---|---|
| Tema | Firewall perimetral |
| Estado encontrado | pfSense 2.7.2, 1.200 reglas, 40% sin propietario, sin MFA de administración |
| Brecha vs. norma | PR-01 (acceso administrativo), INFRA-03 (higiene de reglas) |
| Riesgo asociado | Alto: regla obsoleta permite acceso a la DMZ |
| Acción a tomar | Revisión de reglas con Infraestructura; habilitar MFA |
| Plazo / responsable | 30 días · Jefatura de Infraestructura |
| Evidencia | Export de reglas RELEV-001 |

Las fichas llenas alimentan: ID-01 (inventario), ID-03 (riesgos), ID-04 (plan de tratamiento), URCDP-01 (Documento de Seguridad) y GV-06 (informe del RSI).

---

## 7. Checklist del RSI después del relevamiento

- ☐ Pedí evidencia de cada tema, no promesas.
- ☐ Los pedidos quedaron por escrito con plazo y responsable.
- ☐ Relevé lo crítico primero (dinero, datos personales, accesos).
- ☐ Completé las fichas de infraestructura de los temas principales.
- ☐ Cargué los activos de red en ID-01 con todos sus atributos.
- ☐ Las brechas encontradas alimentan el análisis de riesgos (ID-03).
- ☐ El plan de tratamiento (ID-04) tiene acciones, plazos y responsables.
- ☐ El Documento de Seguridad (URCDP-01) refleja medidas reales, no genéricas.

---

## 8. Cierre del módulo

El RSI no adivina: **pregunta y pide evidencia**. Con las preguntas de este módulo podés diagnosticar la infraestructura del Banco en pocas semanas, priorizada por riesgo, y convertir ese diagnóstico en inventario, riesgos, plan de tratamiento e informes. El siguiente módulo (INFRA-14) te dice qué de todo esto es **obligatorio por decreto** ante Agesic y el CERTuy.

### Checklist del módulo

- ☐ Usé las preguntas por tema (firewalls, segmentación, switches, monitoreo, EDR, apps, VPN, backups).
- ☐ Pregunté a cada interlocutor en su idioma.
- ☐ Priorizé el relevamiento por riesgo.
- ☐ Armé fichas de infraestructura y las conecté a las plantillas del kit.

---

**Documentos relacionados:** GV-01, GV-02, GV-03, GV-05, GV-06, ID-01, ID-02, ID-03, ID-04, PR-01, PR-04, PR-05, PR-06, PR-07, PR-08, DE-01, DE-02, RC-01, RC-02, BCU-01, BCU-02, BCU-03, BCU-04, BCU-05, URCDP-01, URCDP-05 · Referencias internas: INFRA-01 a INFRA-12, INFRA-14
