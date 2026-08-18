# INFRA-07 · Auditoría de la Infraestructura Actual

> **Función del MCU 5.0:** Apoyar la función de identificación y gestión de activos (ID.AM), la protección (PR) y la mejora continua, al verificar sistemáticamente que la infraestructura de red instalada esté documentada, configurada de forma segura y alineada al marco nacional.
> **ISO/IEC 27001:** Sustenta el requisito de auditorías internas (A.9.3), la revisión de la seguridad de la red (A.13), el inventario de activos (A.8) y la mejora del SGSI a partir de los hallazgos.
> **BCU:** Da insumos directos para el informe del RSI (GV-06), las auditorías internas (BCU-05) y la Estrategia de Monitoreo y Gestión del Riesgo de TIC (EMG), verificando que lo documentado coincida con lo instalado.
> **URCDP:** Verifica que el Documento de Seguridad (URCDP-01) refleje la infraestructura real que trata datos personales, con las medidas físicas y lógicas declaradas funcionando en la práctica.
> **Nivel del curso:** 🟢 Descubrir · 🟡 Practicar · 🔴 Dominar

---

## 1. Propósito de este módulo

Hay una frase que toda auditoría demuestra una y otra vez: **lo que está documentado no siempre es lo que está instalado**. Puede haber un router que no figura en el inventario, un firewall con una regla vieja que abre todo, o una impresora con contraseña de fábrica conectada a la red.

La auditoría de infraestructura es la **revisión sistemática** de lo que realmente existe, cómo está configurado, y si cumple con las normas del banco (MCU 5.0, BCU, URCDP).

> **Analogía:** es el control médico anual de la red: se miden todos los signos vitales, se busca lo que no debería estar, y al final se entrega un diagnóstico con tratamiento.

### Auditoría interna vs. revisión del RSI

| Aspecto | Auditoría interna (BCU-05) | Revisión del RSI |
|---|---|---|
| Quién la hace | Auditoría interna del Banco o un externo autorizado | El Responsable de Seguridad de la Información y su equipo |
| Objetivo | Verificar cumplimiento y dar una opinión independiente | Verificar el estado operativo y mejorar controles |
| Frecuencia | Periódica, según el plan del SGSI | Periódica y a demanda (cambios, incidentes) |
| Documento del kit | BCU-05 (informe de auditoría) | GV-06 (informe del RSI) |

> Ambas se apoyan en **las mismas técnicas**. Este módulo te enseña los pasos; el informe final se completa con BCU-05.

---

## 2. Orden de trabajo: los 11 pasos

La auditoría se hace **en orden**, para que cada paso sirva de base al siguiente. Cada paso tiene su checklist (☐) y su evidencia.

### Paso 1 · Inventario real de dispositivos y sistemas

Contrastar lo que **existe** con lo que figura en el inventario (**ID-01**). Se revisan routers, switches, firewalls, puntos de acceso (AP), servidores, endpoints (PC y notebooks) e IoT (impresoras, videocámaras, control de accesos).

- ☐ Listé todos los dispositivos conectados a la red (no solo los que recuerdo).
- ☐ Contrasté cada dispositivo con el inventario ID-01.
- ☐ Registré dispositivos no inventariados (los "fantasmas").
- ☐ Revisé que los equipos retirados no sigan conectados.

> **Evidencia:** export del inventario (con MAC y IP por dispositivo) + captura del descubrimiento de red + lista de discrepancias.

### Paso 2 · Mapa de red y segmentación

Verificar que la red está dividida como dicen los diagramas (documento **GV-02**): VLANs, zonas, DMZ.

- ☐ Confirmé que el diagrama de red coincide con la realidad.
- ☐ Verifiqué que la **DMZ está aislada** (el tráfico entre la DMZ y el interior pasa por el firewall, no hay conexión directa).
- ☐ Revisé que los dispositivos estén en la VLAN/zona que les corresponde.
- ☐ Comprobé que no haya segmentos olvidados ni "puentes" sin control.

> **Evidencia:** diagrama actualizado + tabla de VLANs/zona + captura de interfaces y etiquetas.

### Paso 3 · Configuración de seguridad (hardening)

Revisar que cada dispositivo esté configurado de forma endurecida (baseline de **INFRA-04**).

- ☐ No hay **credenciales por defecto** (admin/admin, 1234, etc.).
- ☐ No hay **servicios innecesarios** habilitados (telnet, SNMP v1, HTTP, FTP).
- ☐ Los protocolos de administración son seguros: **SSH** (no telnet), **HTTPS** (no HTTP), **SNMP v3** (o v2 con comunidad restringida).
- ☐ Las redes Wi-Fi usan cifrado fuerte (**WPA3** o, en su defecto, WPA2 con contraseña fuerte).
- ☐ Las versiones de sistema operativo y firmware cumplen el baseline.

> **Evidencia:** checklist de hardening completado + salida de comandos de configuración + capturas de consolas.

### Paso 4 · Gestión de parches y firmware

- ☐ Tengo el inventario de versiones de firmware y sistemas (PR-06).
- ☐ No hay equipos con **fin de soporte** sin un plan aprobado.
- ☐ Las actualizaciones críticas se aplicaron dentro de los plazos definidos.
- ☐ Hay responsable y registro de cada actualización.

> **Evidencia:** reporte de parches con fechas + acta o registro de actualizaciones.

### Paso 5 · Firewall y reglas

- ☐ Las reglas siguen **mínimo privilegio** (solo lo necesario).
- ☐ No hay **reglas obsoletas** (para servicios que ya no existen).
- ☐ No hay reglas tipo "permitir todo" sin justificación.
- ☐ Los **logs del firewall están activos** y llegan al SIEM (DE-01).
- ☐ Se revisan las **reglas de salida** (no solo las de entrada).

> **Evidencia:** export de reglas + acta de revisión de reglas con fecha y responsable.

### Paso 6 · Controles de acceso administrativo

- ☐ Sé **quién administra qué** (matriz de accesos, PR-01).
- ☐ No hay **cuentas compartidas** sin justificación y control.
- ☐ El acceso administrativo tiene **2FA** (segundo factor).
- ☐ Las altas y bajas de personal se reflejan en los accesos.

> **Evidencia:** matriz de accesos + registro de 2FA + listado de cuentas administrativas.

### Paso 7 · Monitoreo y logs

- ☐ Las fuentes de logs cubiertas son las definidas en DE-01.
- ☐ El **SIEM** recibe y correlaciona eventos (DE-02).
- ☐ La **retención** de logs cumple la política (y las exigencias BCU/URCDP).
- ☐ Los relojes de los equipos están sincronizados (**NTP**).
- ☐ Hay **alertas** configuradas y se revisan periódicamente.

> **Evidencia:** tabla de cobertura de fuentes + captura del SIEM + prueba de alerta.

### Paso 8 · Respaldos y recuperación

- ☐ Los **datos** están respaldados (PR-05).
- ☐ Las **configuraciones de dispositivos** están respaldadas (poder reconstruir un router o firewall).
- ☐ Se hicieron **pruebas de restauración** (RC-02) y están documentadas.
- ☐ Los respaldos están protegidos (cifrado, acceso restringido, copia fuera de sitio).

> **Evidencia:** registro de respaldos + acta de prueba de restauración con resultado.

### Paso 9 · Protección de extremos

- ☐ El antivirus/**EDR** (INFRA-05) cubre todos los endpoints.
- ☐ No hay equipos con protección **excluida o deshabilitada** sin justificación.
- ☐ Las alertas de detección se respondieron en tiempo.

> **Evidencia:** reporte de cobertura del antivirus/EDR + listado de exclusiones aprobadas.

### Paso 10 · Seguridad física de la infraestructura

- ☐ Los **racks y salas** tienen control de acceso (quién entra y quién no).
- ☐ El **cableado** está identificado y protegido.
- ☐ Las salas tienen **UPS** y condiciones ambientales adecuadas (PR-04).
- ☐ No hay puntos de red abiertos en zonas públicas.

> **Evidencia:** planillas de control de acceso a salas + fotos (si la política lo permite) + registro de mantenimiento.

### Paso 11 · Documentación de datos personales

- ☐ El **Documento de Seguridad (URCDP-01)** refleja la infraestructura real.
- ☐ Las bases de datos personales están ubicadas donde dice el documento.
- ☐ Las medidas físicas y lógicas declaradas **existen en la práctica**.
- ☐ Los encargados de tratamiento y accesos registrados coinciden con la realidad.

> **Evidencia:** copia vigente de URCDP-01 + acta de la verificación + discrepancias corregidas.

---

## 3. Métodos de recolección de evidencias

Para completar cada paso se usan varios métodos, según el tipo de verificación:

| Método | Qué es | Ejemplo |
|---|---|---|
| **Entrevistas** | Preguntar a los responsables | "¿Quién revisa las reglas del firewall?" |
| **Revisión documental** | Leer documentos y políticas | Verificar que PR-06 exista y esté vigente |
| **Revisión de configuraciones** | Inspeccionar la config real | Leer la configuración del switch |
| **Escaneo pasivo** | Observar la red sin alterarla | Ver qué responde cada equipo (no invasivo) |
| **Escaneo activo** | Enviar solicitudes a los equipos | Nmap para descubrir puertos y servicios — **solo con autorización** |
| **Revisión de consolas** | Mirar los paneles de gestión | Cobertura del antivirus, SIEM, firewall |

> **Regla crítica:** el **escaneo activo se hace con autorización escrita y en una ventana definida**. Escanear sin permiso es en sí mismo un incidente de seguridad. Ver documento **DE-01 / DE-03**.

---

## 4. Tabla resumen de la auditoría

| Paso | Qué revisar | Herramienta sugerida | Evidencia | Documento del kit |
|---|---|---|---|---|
| 1 | Inventario real | Descubrimiento de red, consolas | Export inventario + IP/MAC | ID-01, GV-02 |
| 2 | Mapa y segmentación | Diagramas, consola de VLAN | Diagrama + tabla de zonas | GV-02, INFRA-03 |
| 3 | Hardening | Checklist + config | Checklist + capturas | INFRA-04 |
| 4 | Parches y firmware | Consola de gestión de parches | Reporte de parches | PR-06 |
| 5 | Firewall y reglas | Export de reglas | Export + acta de revisión | INFRA-03 |
| 6 | Accesos administrativos | Matriz + consola | Matriz + registro 2FA | PR-01 |
| 7 | Logs y SIEM | Consola SIEM | Cobertura + captura alertas | DE-01, DE-02 |
| 8 | Respaldos | Consola de backup | Registro + acta de restauración | PR-05, RC-02 |
| 9 | Protección extremos | Consola antivirus/EDR | Reporte de cobertura | INFRA-05 |
| 10 | Seguridad física | Recorrido + planillas | Planillas + registro | PR-04 |
| 11 | Datos personales | Contraste URCDP-01 vs real | Acta + discrepancias | URCDP-01 |

---

## 5. Resultado: el informe de auditoría

Al terminar se redacta el informe (base: **BCU-05**). Su estructura mínima:

1. **Alcance y fecha** de la auditoría.
2. **Metodología y herramientas** usadas.
3. **Hallazgos** clasificados por severidad.
4. **Riesgos asociados** (alimentan el inventario de riesgos, ID-02/03/04).
5. **Recomendaciones** y **plan de acción** con plazos y responsables.

### Modelo de hallazgo

| Campo | Ejemplo |
|---|---|
| **Descripción** | La impresora del 3er piso usa la contraseña de fábrica |
| **Evidencia** | Captura de la consola de la impresora |
| **Normativa vulnerada** | MCU PR.AA; BCU RNRCSF; URCDP-01 |
| **Severidad** | Alta |
| **Recomendación** | Cambiar credencial, incluirla en el inventario y en el proceso de alta |
| **Plazo** | 7 días / Responsable: administrador de red |

> Cada hallazgo se clasifica en **crítico / alto / medio / bajo**. Los críticos y altos se comunican de inmediato al RSI y se registran en el inventario de riesgos (ID-04) con plan de tratamiento.

---

## 6. Errores comunes al auditar

- ✗ **Auditar sin autorización o sin ventana definida:** puede generar incidentes y daños en producción.
- ✗ **No contrastar con el inventario:** se describen "equipos conocidos" y se pierden los fantasma.
- ✗ **No conservar evidencia:** un hallazgo sin captura es una opinión, no una prueba.
- ✗ **Mezclar hallazgos con opiniones:** el informe debe distinguir "hecho verificado" de "sugerencia".
- ✗ **No dar seguimiento:** una auditoría sin plan de acción y sin seguimiento no mejora nada.
- ✗ **Solo mirar la parte lógica y olvidar la física**, o al revés.

---

## 7. Relación con el kit

| Documento | Cómo se conecta |
|---|---|
| **BCU-05** | Informe de auditoría interna: formato de salida de este módulo |
| **GV-06** | Informe del RSI: la auditoría es insumo de sus conclusiones |
| **ID-01 a ID-04** | Inventario de activos y riesgos: se contrastan y actualizan con los hallazgos |
| **URCDP-01** | Verifica que el Documento de Seguridad refleje la infraestructura real |
| **PR-06** | Gestión de parches y vulnerabilidades: se audita en el paso 4 |
| **DE-01 / DE-02** | Cobertura de logs y SIEM: se audita en el paso 7 |

> **Checklist del lector**
> - ☐ Puedo explicar la diferencia entre auditoría interna y revisión del RSI.
> - ☐ Conozco los 11 pasos y la evidencia de cada uno.
> - ☐ Sé que el escaneo activo requiere autorización y ventana.
> - ☐ Puedo redactar un hallazgo con severidad, recomendación y plazo.
> - ☐ Sé qué errores comunes evitar al auditar.

---

**Documentos relacionados:** GV-06, ID-01, ID-02, ID-03, ID-04, PR-04, PR-05, PR-06, DE-01, DE-02, RC-02, BCU-05, URCDP-01, MATRIZ-001.
