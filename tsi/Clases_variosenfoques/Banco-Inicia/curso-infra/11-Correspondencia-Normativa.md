# INFRA-11 · Correspondencia Normativa y Cómo Llenar los Documentos

> **Función del MCU 5.0:** Vincular cada tema técnico de infraestructura con los dominios y funciones del Marco de Ciberseguridad de Uruguay (Agesic), para que la evidencia técnica demuestre cumplimiento de la estructura nacional.
> **ISO/IEC 27001:** Enlaza los controles del Anexo A con la documentación del SGSI del Banco: inventario de activos (A.8.1), control de acceso (A.9), seguridad de redes (A.13) y gestión de vulnerabilidades (A.12.6).
> **BCU:** Traduce la infraestructura en evidencia auditable ante el BCU: informes del RSI (GV-06), hallazgos de auditorías (BCU-05) y la Estrategia de Monitoreo y Gestión del Riesgo de TIC (EMG).
> **URCDP:** Documenta las medidas técnicas que protegen datos personales según la Ley 18.331, su modificativa Ley 19.670 y el Decreto 64/020: Documento de Seguridad (URCDP-01), notificaciones (URCDP-02) e inscripción de bases (URCDP-04).
> **Decreto 66/025:** Traduce la infraestructura en evidencia para la Dirección de Seguridad de la Información de Agesic y el CERTuy: RSI designado (art. 10.c), notificación de incidentes (art. 10.g), trazabilidad de logs ≥12 meses (art. 11.a) y auditorías según el MCU con resumen ejecutivo en 30 días y plan de acción en 60 (arts. 16–17). Detalle completo en INFRA-14.
> **Nivel del curso:** 🟢 Descubrir · 🟡 Practicar · 🔴 Dominar

---

## 1. Propósito de este módulo

Todos los módulos anteriores te enseñaron **qué es la red y cómo protegerla**. Este módulo te enseña la parte que en la vida real nadie te perdona que falte: **demostrarlo por escrito**.

Cuando llega un auditor del BCU, un oficial de la URCDP o el personal de Agesic, no pide que le expliques la red: pide **documentos y evidencia**. Este módulo te da el puente entre:

- Lo que hiciste en el laboratorio (INFRA-09 e INFRA-10).
- Lo que dice la norma (MCU 5.0, ISO/IEC 27001, BCU, URCDP).
- Lo que exige cada plantilla del kit (ID-01, URCDP-01, PR-06, etc.).
- La evidencia que demuestra que lo hiciste de verdad.

La idea central es simple: **si la red se protege pero no está documentada, ante la norma es como si no estuviera protegida.**

---

## 2. Tabla maestra de correspondencia normativa

Esta tabla cubre los temas principales de infraestructura de red. Para cada tema indica la norma que lo exige, la plantilla del kit donde se registra, qué escribir y qué evidencia acompaña.

| Tema de infraestructura | Norma | Plantilla del kit | Qué escribir | Evidencia |
|---|---|---|---|---|
| Inventario y mapa de red | MCU ID.AM; URCDP-01 (inventario de bases) | ID-01, GV-02 | Lista de activos de red con atributos (tipo, IP, zona, firmware, responsable) | Diagrama de red + export de configuración |
| Segmentación, zonas y DMZ | MCU PR.PS / PR.AA; BCU EMG | INFRA-03, GV-02, ID-01 | Zonas definidas, reglas de tráfico entre zonas, justificación de cada zona | Reglas de firewall exportadas + diagrama de zonas |
| Firewall y reglas | MCU PR.PS; BCU-01 / BCU-03 | INFRA-03 | Reglas aplicadas, revisión periódica, propietario de cada regla | Export de reglas (`pfctl -sr`) + acta de revisión |
| Firmware y parches | MCU PR.PS | PR-06, INFRA-04 | Inventario de versiones de firmware y parches, fechas, responsables | Reporte de parches y actualizaciones aplicadas |
| Antivirus / EDR | MCU PR.PS; BCU-03 | INFRA-05, BCU-03 | Cobertura de antivirus/EDR por equipo, estado de detección | Reporte de cobertura del antivirus/EDR |
| SAST / DAST | MCU PR.DS | PR-07, DE-03, URCDP-05 | Escaneos de seguridad de aplicaciones (estático y dinámico) | Reportes de escaneo con fechas y hallazgos |
| DLP y fuga de datos | MCU PR.DS | PR-03, URCDP-01 | Controles de prevención de fuga, canales monitoreados, políticas | Reporte DLP + políticas firmadas |
| Logs y SIEM | MCU DE.CM; Decreto 66/025 art. 11.a (trazabilidad ≥12 meses) | DE-01, DE-02, BCU-04 | Fuentes de logs cubiertas, retención (≥12 meses), correlación | Cobertura de logs (tabla fuente/estado) + reporte de retención |
| Monitoreo y alertas | MCU DE.CM / DE.AE; BCU EMG (Estrategia de Monitoreo) | DE-01, DE-02, INFRA-12 | Casos de uso, umbrales, líneas de base, SLAs de triage | Catálogo de reglas + reporte mensual de monitoreo |
| Datos personales en la infra | Ley 18.331, Decreto 64/020 | URCDP-01 (medidas físicas/lógicas), URCDP-04 (inscripción) | Medidas que protegen las bases de datos personales, personal autorizado, encargados | Documento de Seguridad firmado + constancia de inscripción |
| Vulneraciones | Ley 19.670 art. 38; Decreto 66/025 art. 10.g (CERTuy) | URCDP-02, RS-02 | Registro de incidentes, plazos de notificación (24 h contención, 72 h URCDP, CERTuy según procedimiento) | Registro de incidentes + notificaciones enviadas |
| RSI y gobierno de la seguridad | Decreto 66/025 art. 10.c; BCU EMG | GV-03, GV-06 | RSI designado por escrito, equipo, informe a Dirección | Designación firmada + informes del RSI |
| Auditoría según MCU | Decreto 66/025 arts. 16–17 | BCU-05, ID-05 | Auditorías por lineamientos del MCU; resumen ejecutivo en 30 días y plan de acción en 60 | Informe de auditoría + resumen ejecutivo a Agesic + plan de acción |
| Riesgos | MCU ID.RA / GV.RM | ID-02, ID-03, ID-04 | Identificación, valoración y plan de tratamiento de riesgos | Planillas de riesgo + plan de tratamiento |
| Continuidad | MCU RC.RP | RC-01, RC-02, BCU-06 | Estrategia de respaldo, BCP/DRP y pruebas | Documentos BCP/DRP + actas de prueba |

---

## 3. Cómo llenar URCDP-01 (Documento de Seguridad de Datos Personales)

Este es el documento más importante de la cartera H-URCDP. La infraestructura de red aparece en casi todas sus secciones. Estas son las que se completan con la información de este curso:

### 3.1 Inventario de bases de datos y sistemas

| Sección del documento | Qué escribir | De dónde sale |
|---|---|---|
| Inventario de bases de datos | Cada base que contiene datos personales: nombre, finalidad, ubicación (servidor, red, zona) | ID-01 y el laboratorio (INFRA-10) |
| Inventario de sistemas | Aplicaciones y servicios que procesan datos personales, y en qué red viven | ID-01 |
| Titularidad y encargados | Quién responde por cada base y quién la procesa (encargados de tratamiento) | GV-01, contrato de encargados |

### 3.2 Medidas físicas

Describí el entorno donde viven los servidores:

- **Racks y sala de servidores:** ubicación, puertas, quién tiene llave, registro de entrada.
- **Cableado:** bandejas, canaletas, identificadores de cable, protección contra incendios.
- **Videovigilancia:** cámaras que cubren el acceso a la sala y a los racks.
- **Energía y climatización:** SAI, generador, control de temperatura.
- **Aislamiento del laboratorio:** si el banco tiene un laboratorio de pruebas, registrar que está separado de producción (INFRA-09).

### 3.3 Medidas lógicas

Las más técnicas y las que este curso te permite documentar con evidencia:

| Medida lógica | Qué escribir | Evidencia que acompaña |
|---|---|---|
| Firewall perimetral | Modelo, ubicación, reglas principales | Export de reglas (INFRA-10) |
| Segmentación y DMZ | Zonas definidas y qué vive en cada una | Diagrama (GV-02, INFRA-03) |
| Control de acceso | Quién accede a cada red o sistema, por qué medio | Listas de acceso (ID-01) |
| Cifrado | Datos cifrados en tránsito (TLS/VPN) y en reposo | Configuración de VPN/TLS (INFRA-07) |
| Antivirus/EDR | Cobertura y actualización | Reporte de cobertura (INFRA-05) |
| Registros (logs) | Qué se registra y cuánto se conserva | Cobertura de logs (DE-01) |
| Gestión de parches | Frecuencia y responsables | Reporte PR-06 |

### 3.4 Personal autorizado y encargados

- Lista de roles con acceso a la infraestructura (administradores de red, DBA, soporte).
- Quiénes son los encargados externos (proveedores de nube, mantenimiento) y qué datos pueden ver.
- Firmas y fechas de autorización.

> **Regla práctica:** no escribas "se cuenta con firewall" así nomás. Escribí marca, modelo, dónde está, qué reglas tiene y adjuntá la evidencia. Un documento genérico no sirve ante una inspección.

---

## 4. Cómo llenar ID-01 (Inventario de Activos)

ID-01 es el inventario general de activos, y la red aporta su parte: routers, switches, firewalls, servidores, puntos de acceso y el propio cableado. Cada activo de red se registra con estos atributos:

| Atributo | Qué significa | Ejemplo (del laboratorio) |
|---|---|---|
| Identificador | Código único del activo | `FW-001` |
| Tipo de activo | Función que cumple | Firewall |
| Marca / modelo | Fabricante y modelo | pfSense CE 2.7 |
| Dirección IP / MAC | Identificación en la red | 10.10.10.254 / 08:00:27:... |
| VLAN / zona | Segmento lógico donde vive | LAN (zona interna) |
| Sistema operativo / firmware | Versión instalada | FreeBSD 14 |
| Versión / parche | Nivel de actualización | 2.7.2 (ago 2026) |
| Responsable | Quién lo administra | Área de Infraestructura |
| Criticidad | Impacto si se pierde (Alta/Media/Baja) | Alta |
| Evidencia | Dónde está la prueba de que existe | Diagrama INFRA-03, export de reglas |

Ejemplo de fila completa:

| Identificador | Tipo | Marca/Modelo | IP | VLAN/Zona | SO/Firmware | Versión | Responsable | Criticidad |
|---|---|---|---|---|---|---|---|---|
| FW-001 | Firewall | pfSense CE | 10.10.10.254 | LAN interna | FreeBSD | 2.7.2 | Infraestructura | Alta |
| SW-001 | Switch de acceso | Cisco Catalyst | 10.10.10.2 | LAN interna | IOS | 15.2 | Infraestructura | Alta |
| SRV-001 | Servidor de datos | Dell PowerEdge | 10.10.10.20 | LAN interna | Ubuntu Server | 24.04 | DBA | Alta |
| WEB-001 | Servidor web | VM VirtualBox | 10.10.20.10 | DMZ | Debian | 12 | Infraestructura | Media |

> **Regla práctica:** todo activo que tenga IP, o que esté conectado a la red, va al inventario. Lo que no está inventariado, ante un auditor no existe.

---

## 5. Cómo llenar PR-06 / ID-04 (gestión de vulnerabilidades)

La gestión de vulnerabilidades de la infraestructura se documenta en dos lugares que trabajan juntos:

- **ID-04 (Análisis de riesgo detallado):** identifica las vulnerabilidades de cada activo.
- **PR-06 (Plan de parches y actualizaciones):** planifica y registra la corrección.

### 5.1 El ciclo de gestión

1. **Identificar:** escaneos (Nmap, Nessus/OpenVAS) y avisos de fabricantes. Resultado: lista de vulnerabilidades.
2. **Valorar:** se clasifican por severidad (Crítica, Alta, Media, Baja) con base en la CVSS.
3. **Tratar:** se aplica el parche, se mitiga con otra medida o se acepta el riesgo.
4. **Registrar:** se deja todo anotado y con responsable.
5. **Revisar:** se repite el ciclo con frecuencia definida.

### 5.2 Tabla de ejemplo del plan de tratamiento

| Vulnerabilidad | Activo | Severidad | Plazo | Responsable | Estado |
|---|---|---|---|---|---|
| CVE-2026-XXXX en FreeBSD | FW-001 | Crítica | 72 h | Infraestructura | ☑ Corregido (fecha) |
| CVE-2026-YYYY en Ubuntu | SRV-001 | Alta | 7 días | DBA | ☐ En proceso |
| Puerto 22 abierto en DMZ | WEB-001 | Media | 30 días | Infraestructura | ☐ Pendiente |
| Firmware desactualizado de switch | SW-001 | Baja | 90 días | Infraestructura | ☐ Programado |

> **Regla práctica:** el plan de tratamiento nunca queda vacío. Cada vulnerabilidad tiene severidad, plazo y responsable. El estado se actualiza con fecha, y la evidencia (reporte de escaneo, acta de parche) se adjunta.

---

## 6. Cómo usar MATRIZ-001 (Matriz de Correspondencia Normativa)

La matriz es la herramienta que demuestra cumplimiento de un vistazo. Funciona como una tabla grande con tres columnas:

1. **Control o requisito normativo** (ejemplo: MCU PR.PS, ISO/IEC 27001 A.13, Decreto 64/020 art. X).
2. **Documento o plantilla del kit que lo evidencia** (ejemplo: INFRA-03, ID-01, URCDP-01).
3. **Evidencia específica y estado** (ejemplo: export de reglas `pfctl -sr`, fecha, vigencia).

### Cómo mantenerla al día

- Marcá la columna "estado": 🟢 Cumplido · 🟡 En proceso · 🔴 Pendiente.
- Cada fila con evidencia lleva fecha de última verificación.
- Ante un cambio de red (una zona nueva, un firewall nuevo), la fila correspondiente se actualiza el mismo día.
- La matriz se revisa al menos una vez al año junto con los módulos INFRA-01 a INFRA-10.

> **Regla práctica:** no pongas "Cumplido" sin evidencia. Si la evidencia caducó (por ejemplo, un reporte de parches de hace dos años), el estado pasa a "Pendiente de actualización".

---

## 7. Qué evidencia presentar según el interlocutor

No todos los organismos piden lo mismo. Cada uno mira un ángulo distinto:

### Ante el BCU

- Informe del Responsable de Seguridad de la Información (**GV-06**).
- Resultados de auditorías internas de seguridad (**BCU-05**).
- Estrategia de Monitoreo y Gestión del Riesgo de TIC (**EMG**) y su implementación.
- Evidencia de controles de continuidad (**RC-01, RC-02, BCU-06**).
- Foco: riesgo de las TIC para las operaciones del banco.

### Ante Agesic

- Perfil de ciberseguridad institucional (**ID-05**) con los niveles alcanzados por función del MCU.
- Evidencia de cada función: inventario (ID.AM), protección (PR), detección (DE), respuesta (RS), recuperación (RC).
- Designación del RSI (**GV-03**) y notificaciones al CERTuy (**RS-02**) — Decreto 66/025 arts. 10.c y 10.g.
- Trazabilidad de eventos ≥12 meses (**DE-01**, INFRA-12) — Decreto 66/025 art. 11.a.
- Resumen ejecutivo de auditoría en 30 días y plan de acción en 60 (**BCU-05**, ID-05) — Decreto 66/025 arts. 16–17.
- Foco: alineación con el Marco de Ciberseguridad de Uruguay 5.0 y cumplimiento del Decreto 66/025.

### Ante la URCDP

- Documento de Seguridad de Datos Personales (**URCDP-01**) firmado y vigente.
- Notificaciones de vulneraciones (**URCDP-02**) si corresponden.
- Registro de bases de datos inscritas (**URCDP-04**).
- Evaluaciones de impacto (**URCDP-05**) si aplican.
- Foco: protección de los datos personales y los derechos de sus titulares.

> **Regla práctica:** antes de una auditoría, armá un paquete por interlocutor usando MATRIZ-001 como índice. No entregues la carpeta completa: cada organismo recibe lo suyo.

---

## 8. Frecuencia de revisión y actualización

La documentación se revisa de forma periódica y también ante cambios significativos. Esta tabla define la frecuencia base:

| Documento | Revisión periódica | Actualización inmediata ante |
|---|---|---|
| ID-01 (Inventario de activos) | Trimestral | Alta o baja de cualquier activo de red |
| ID-02 / ID-03 / ID-04 (Riesgos) | Anual | Nuevo riesgo o incidente significativo |
| PR-06 (Parches) | Mensual | Cada nueva versión de firmware crítico |
| DE-01 / DE-02 (Logs) | Trimestral | Cambio de cobertura de registros |
| URCDP-01 (Documento de Seguridad) | Anual | Cambio en las bases, medidas o encargados |
| URCDP-04 (Inscripción de bases) | Anual | Nueva base de datos o nueva finalidad |
| INFRA-03 (Segmentación) | Anual | Cambio de zonas, firewall o reglas |
| MATRIZ-001 | Anual | Cualquier cambio normativo (MCU, BCU, Decreto 64/020, Decreto 66/025) |

> **Regla práctica:** "revisión" no es leer de memoria: es abrir el documento, compararlo con la realidad y firmar con fecha que se revisó. La firma y la fecha son la diferencia entre un documento vivo y un PDF viejo.

---

## 9. Errores comunes al llenar la documentación

| Error | Por qué es peligroso | Cómo evitarlo |
|---|---|---|
| Llenar documentos genéricos sin la infra real | Un auditor lo detecta a los dos minutos | Escribir marca, modelo, IP y zona reales de cada cosa |
| No actualizar tras cambios de red | La documentación deja de reflejar la realidad | Regla de oro: el día del cambio, se actualiza el documento |
| Evidencias sin fecha | No tienen valor probatorio | Todo archivo con fecha en el nombre y en el contenido |
| Documentos firmados sin control de cambios | No se sabe qué cambió ni cuándo | Tabla de versiones: versión, fecha, autor, descripción del cambio |
| Copiar y pegar reglas de otra institución | No responde a la realidad del Banco | Cada regla se escribe para una zona real y se justifica |
| Guardar evidencia suelta sin índice | No se encuentra cuando se pide | Expediente ordenado con índice y referencia a MATRIZ-001 |

---

## 10. Cierre del módulo

Con este módulo cierras el curso de infraestructura de red. Ya sabés armar una red, protegerla, simularla, probarla y —lo más importante— **demostrarlo por escrito** ante URCDP, BCU y Agesic. La infraestructura ya no es solo cables y configuraciones: es evidencia viva de que el Banco cumple la norma.

### Checklist del módulo

- ☐ Identifiqué qué tema de infraestructura corresponde a cada norma (incluido el Decreto 66/025).
- ☐ Completé URCDP-01 con medidas físicas y lógicas reales y evidencia.
- ☐ Registré los activos de red en ID-01 con todos sus atributos.
- ☐ Armé el plan de tratamiento de vulnerabilidades en PR-06 / ID-04.
- ☐ Mantengo MATRIZ-001 actualizada con estado y fecha.
- ☐ Sé qué evidencia preparar para cada interlocutor (BCU, Agesic, URCDP, CERTuy).
- ☐ Definí frecuencias de revisión y control de cambios de cada documento.

---

**Documentos relacionados:** GV-01, GV-02, GV-03, GV-04, GV-06, ID-01, ID-02, ID-03, ID-04, ID-05, PR-01, PR-02, PR-03, PR-04, PR-05, PR-06, PR-07, PR-08, DE-01, DE-02, DE-03, RS-01, RS-02, RS-03, RC-01, RC-02, RC-03, RC-04, BCU-01, BCU-02, BCU-03, BCU-04, BCU-05, BCU-06, URCDP-01, URCDP-02, URCDP-03, URCDP-04, URCDP-05, URCDP-06, MATRIZ-001 · Referencias internas: INFRA-01, INFRA-02, INFRA-03, INFRA-04, INFRA-05, INFRA-06, INFRA-07, INFRA-08, INFRA-09, INFRA-10, INFRA-12, INFRA-13, INFRA-14
