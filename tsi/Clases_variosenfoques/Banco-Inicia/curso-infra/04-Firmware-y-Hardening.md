# INFRA-04 · Firmware y Hardening

> **Función del MCU 5.0:** Endurecer la configuración de los dispositivos y mantener su firmware actualizado para reducir vulnerabilidades.
> **ISO/IEC 27001:** Anexo A.8.8 Gestión de vulnerabilidades técnicas; A.8.9 Gestión de configuración.
> **BCU:** BCU-04 (gestión de vulnerabilidades y actualizaciones) — proceso técnico de parches.
> **URCDP:** URCDP-01 — medidas de seguridad técnicas apropiadas al riesgo.
> **Nivel del curso:** 🟢 Descubrir · 🟡 Practicar · 🔴 Dominar

---

## 1. Introducción: el "software escondido" de los dispositivos

Imaginá que en el banco cada dispositivo es como un empleado:

- La computadora tiene un **programa** para hacer su trabajo (el sistema operativo y las aplicaciones).
- Pero también tiene una "instrucción grabada en su memoria interna" que le dice cómo encender, cómo hablar con sus piezas, cómo arrancar. Esa instrucción es el **firmware**.

El firmware vive dentro de casi todo lo que tiene un chip:

- Routers y switches (los que conectan la red).
- Firewalls (el guardia de INFRA-03).
- Puntos de acceso WiFi (los que reparten la señal).
- NAS y discos de almacenamiento.
- Impresoras y multifunción.
- El **BIOS/UEFI** de cada computadora (lo que arranca antes que el sistema operativo).

> **Analogía rápida:** el sistema operativo es la persona que trabaja en la oficina; el firmware es su **memoria de cómo ser humano**, grabada desde el nacimiento. Si esa memoria tiene un defecto, la persona puede ser manipulada antes de empezar el día.

Este archivo te enseña por qué el firmware importa tanto, cómo se gestionan los parches, y qué es el **hardening** (endurecer la configuración). Todo con nivel de principiante absoluto.

---

## 2. ¿Qué es el firmware y en qué se diferencia?

### 2.1 Definición

El **firmware** es un software de bajo nivel, almacenado en una memoria especial (no en el disco de siempre), que controla cómo funciona un dispositivo. Es la "capa de arranque y de control de hardware".

### 2.2 Firmware vs sistema operativo vs aplicación

| Capa | Qué es | Ejemplo | Quién lo actualiza |
|---|---|---|---|
| **Firmware** | Controla el hardware directamente | BIOS/UEFI de una PC, sistema del router | El fabricante del dispositivo |
| **Sistema operativo** | Base de programas donde corren las aplicaciones | Windows, Linux | Microsoft, Red Hat, etc. |
| **Aplicación** | Programa que hace una tarea concreta | Navegador, sistema de gestión bancaria | El proveedor de la aplicación |

El firmware está **más cerca del hardware**: si el firmware de un router es vulnerable, la red entera puede estar en riesgo, aunque el sistema operativo de los servidores esté impecable.

### 2.3 ¿Por qué es objetivo de atacantes?

- El firmware se actualiza menos que el sistema operativo: los equipos "se instalan y se olvidan".
- Al estar "escondido", pocos lo revisan.
- Un firmware comprometido puede esconder un atacante dentro del dispositivo (se llama **persistencia**): sobrevive a reinicios y a reinstalaciones del sistema operativo.
- Es como si el ladrón se escondiera dentro de las paredes del edificio: nadie lo ve, pero controla las puertas.

> **Dato importante:** las vulnerabilidades de firmware aparecen en listas públicas (CVE). Cuando un fabricante anuncia una, hay una carrera: el banco debe aplicar el parche **antes** de que los atacantes lo exploten.

---

## 3. ¿Por qué importa la gestión del firmware?

### 3.1 Parches y su ciclo

Un **parche** es una actualización del fabricante que corrige fallas de seguridad o errores. El ciclo de vida de un parche:

1. El fabricante publica la corrección.
2. El banco la prueba (en laboratorio, no en producción).
3. Se planifica una **ventana de cambio** (horario donde el servicio se puede interrumpir un rato).
4. Se aplica el parche.
5. Se verifica que todo siga funcionando.
6. Se registra todo.

### 3.2 Ciclo de soporte y fin de vida (EOL)

Todo equipo tiene una fecha límite:

- **Soporte activo:** el fabricante publica parches con normalidad.
- **Fin de soporte / EOL (End of Life):** ya no se publican parches. Los equipos EOL son **imanes de atacantes**: las vulnerabilidades se conocen y nunca se corrigen.

> **Regla de oro:** un dispositivo sin soporte no se puede mantener seguro. Se debe reemplazar o, como mínimo, aislarlo de la red y registrar el riesgo (enlaza con ID-02/ID-03).

### 3.3 Actualizaciones seguras

Las actualizaciones deben:

- Descargarse solo de sitios oficiales del fabricante (o del repositorio interno del banco).
- Verificarse con la **firma digital** (comprobar que el archivo es auténtico).
- Aplicarse en horarios planificados, con respaldo previo de la configuración.

---

## 4. Proceso de gestión de parches de infraestructura

Un proceso simple y ordenado (enlaza con **PR-06** de gestión de cambios):

| Paso | Acción | Responsable |
|---|---|---|
| 1 | Mantener el **inventario de versiones** de firmware de todos los dispositivos | Infraestructura |
| 2 | **Suscribirse a avisos de seguridad** del fabricante (bulletins, CVE) | Infraestructura |
| 3 | Evaluar si el parche aplica a nuestro equipamiento y con qué urgencia | Infraestructura |
| 4 | **Probar en laboratorio** (entorno de prueba) | Infraestructura |
| 5 | Solicitar la **ventana de cambio** (PR-06) | Infraestructura |
| 6 | **Aplicar** el parche con respaldo de configuración | Infraestructura |
| 7 | **Verificar** funcionamiento y comportamiento | Infraestructura |
| 8 | **Registrar** fecha, versión y resultado | Infraestructura |

> **Nota del curso:** 🟡 Practicar — el participante debe saber describir este proceso y llenar el registro de la sección 10. No hace falta ejecutar parches reales.

---

## 5. Hardening: ¿qué es?

El **hardening** (endurecimiento) es ajustar la configuración de un dispositivo para que tenga **solo lo que necesita** y nada más. Se aplica a servidores, firewalls, routers, switches, impresoras, y también a computadoras.

### 5.1 Tres principios del hardening

1. **Mínimo servicio:** desactivar todo lo que no se usa (cuantos menos servicios, menos puertas para los atacantes).
2. **Mínimo privilegio:** cada cuenta y programa tiene solo los permisos imprescindibles.
3. **Seguro por defecto:** la configuración segura debe ser la inicial, no un "después lo ajustamos".

> **Analogía:** el hardening es la "lista de seguridad" del banco: se cierran ventanas que no se usan, se cambian las cerraduras de fábrica, se quitan carteles que dicen dónde está la caja fuerte. El dispositivo "recién salido de fábrica" es seguro solo en apariencia: suele venir con contraseñas por defecto y servicios abiertos.

### 5.2 Guías para el hardening

- **CIS Benchmarks:** listas de recomendaciones técnicas por tipo de producto (Windows, Linux, routers, firewalls). Son el estándar mundial y se usan como base para un **baseline** (configuración de referencia).
- **Guías del fabricante:** cada fabricante publica su "hardening guide" con lo recomendado para su equipo.
- **Políticas internas del Banco:** el banco adapta las guías a su realidad y a la normativa local.

> **Baseline de configuración:** es la "fotografía" de la configuración segura aprobada. Sirve para verificar que un dispositivo está bien configurado y para detectar cambios no autorizados.

---

## 6. Checklist de hardening por tipo de dispositivo

**Credenciales y acceso:**

- ☐ Cambiar todas las **contraseñas por defecto** de fábrica.
- ☐ Crear cuentas de administración **separadas** de las de uso diario.
- ☐ Restringir el **acceso administrativo por IP** (solo desde la red de administración).
- ☐ Usar **autenticación de dos factores (2FA)** para administrar los equipos.
- ☐ Configurar **administración fuera de banda**: una red física separada solo para gestionar equipos (no por la red de producción ni por WiFi).

**Servicios:**

- ☐ Desactivar **telnet** (va sin cifrar) y usar **SSH** (cifrado).
- ☐ Desactivar **SNMP v1/v2c** (sin cifrado) o usarlo solo en redes internas de monitoreo con comunidad fuerte.
- ☐ Desactivar **HTTP** de administración y usar **HTTPS**.
- ☐ Cerrar servicios y puertos que no se necesitan.

**Red y tiempo:**

- ☐ Usar cifrado WiFi **WPA3** (o mínimo WPA2-Enterprise).
- ☐ Configurar **NTP** (reloj sincronizado) para que los logs tengan horas correctas.
- ☐ Separar redes WiFi de empleados y de visitas.

**Registro y respaldo:**

- ☐ Enviar los logs a un **log centralizado** (enlaza con DE-01).
- ☐ Hacer **respaldo cifrado de las configuraciones** de los dispositivos.

---

## 7. Gestión de credenciales de dispositivos

Las credenciales de los equipos de red (routers, switches, firewalls, impresoras) son llaves muy valiosas. Se gestionan como en una bóveda:

- **Bóveda de secretos:** un gestor de contraseñas centralizado donde se guardan las credenciales de administración (nadie las tiene escritas en un papel ni en la memoria).
- **Rotación:** se cambian las contraseñas periódicamente y cuando alguien deja el equipo.
- **Cuentas separadas:** la cuenta de administración del equipo no se comparte con cuentas personales, y cada administrador tiene la suya (así se sabe quién hizo qué, enlaza con **PR-01**).

> **Error común:** la misma contraseña para todos los routers, anotada en una hoja dentro de la sala de servidores. Eso es como dejar la llave de la bóveda bajo el felpudo.

---

## 8. Firmware de los endpoints (computadoras)

Además de los dispositivos de red, las computadoras tienen su propio firmware y arranque que proteger:

- **BIOS/UEFI:** el programa que arranca la computadora. Hay que mantenerlo actualizado y **protegerlo con contraseña** para que nadie arranque desde un USB ajeno.
- **Secure Boot:** función que solo deja arrancar sistemas operativos firmados (auténticos). Se activa y así se impide que un programa malicioso "se disfrace" de sistema operativo.
- **Cifrado de disco:** **BitLocker** (Windows) o **VeraCrypt** (software libre) cifran el disco completo. Si roban la notebook, no pueden leer los datos (enlaza con **PR-03** de protección de datos).

> **Analogía:** el Secure Boot es el portero que exige credencial antes de abrir el banco; el cifrado de disco es la caja fuerte con llave donde se guarda todo aunque se lleven la caja.

---

## 9. Errores comunes

1. **Firmware desactualizado por miedo a cambios:** no se aplican parches porque "pueden romper algo". El riesgo de no parchear suele ser mucho mayor. Se prueba en laboratorio y se planifica.
2. **Credenciales por defecto:** dispositivos con usuario/contraseña de fábrica (admin/admin). Es el primer intento de cualquier atacante.
3. **Administración por WiFi:** gestionar equipos críticos desde una red WiFi compartida, donde cualquiera podría capturar el tráfico.
4. **Backups de configuración sin cifrar:** guardar las configuraciones (con sus secretos) en un archivo plano sin protección.
5. **Ignorar el fin de vida:** mantener en producción equipos EOL sin registrar el riesgo.
6. **Sin baseline:** no tener una configuración de referencia, por lo que no se detecta cuándo un dispositivo se desvía de lo seguro.

---

## 10. Relación con el kit y evidencias

### 10.1 Tabla de inventario de firmware

Este registro es la evidencia central de INFRA-04:

| Dispositivo | Modelo | Versión de firmware | Última actualización | Proveedor | Fin de soporte |
|---|---|---|---|---|---|
| Router sucursal Centro | Fabricante X R-200 | v3.4.2 | 2026-07-10 | Fabricante X | 2029-01-01 |
| Switch piso 1 | Fabricante Y SW-48 | v2.1.0 | 2026-06-20 | Fabricante Y | 2028-06-01 |
| Firewall principal | Fabricante Z FW-1000 | v8.0.1 | 2026-07-15 | Fabricante Z | 2029-09-01 |
| Punto de acceso WiFi | Fabricante W AP-6 | v1.9.0 | 2026-05-30 | Fabricante W | 2027-12-01 |

### 10.2 Cómo presentar un reporte de gestión de parches

Un buen reporte incluye:

- Fecha del informe y período que cubre.
- Total de dispositivos y porcentaje parcheado.
- Lista de parches críticos pendientes y su fecha límite.
- Equipos en fin de soporte y plan de reemplazo.
- Resultado de las pruebas de laboratorio.
- Firmas de quien aplica y quien autoriza (PR-06).

### 10.3 Cómo presentar un baseline de configuración

- Nombre del dispositivo/tipo y versión.
- Parámetros obligatorios (servicios desactivados, protocolos permitidos, forma de acceso).
- Check de verificación con fecha y resultado.
- Registro de cambios al baseline.

### 10.4 Documentos que alimenta

| Documento | Aporte |
|---|---|
| **ID-01 (inventario)** | La tabla de firmware es parte del inventario de activos |
| **PR-01 (acceso)** | Credenciales, 2FA y administración restringida |
| **PR-03 (datos)** | Cifrado de disco y de respaldos de configuración |
| **PR-06 (cambios)** | Ventanas de cambio y registro de parches |
| **DE-01 (logs)** | Logs centralizados con NTP |
| **BCU-04** | Proceso de gestión de vulnerabilidades y actualizaciones |
| **URCDP-01** | Medidas técnicas de seguridad de los dispositivos |

> **Tip de evidencias:** guardar capturas de pantalla con la versión de firmware y la fecha de actualización, el reporte de parches, y el baseline aprobado. Marcar los documentos como "Uso interno".

---

## 11. Actividades de práctica

**Checklist:**

- ☐ Armar la tabla de inventario de firmware con 5 dispositivos reales del banco.
- ☐ Identificar qué dispositivos están en fin de soporte y cuándo vencerá cada uno.
- ☐ Escribir un reporte de gestión de parches de un mes.
- ☐ Redactar un baseline mínimo para un firewall (servicios, protocolos, acceso).
- ☐ Listar las contraseñas por defecto que hay que cambiar en un router nuevo.
- ☐ Marcar en un mapa qué equipos tienen administración fuera de banda.

---

**Documentos relacionados:** ID-01, PR-01, PR-03, PR-06, DE-01, BCU-04, URCDP-01, MATRIZ-001.
