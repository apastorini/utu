# POL-09 · Política de Seguridad Física y del Entorno

> **Función del MCU 5.0:** Proteger (PR.PT — protección del entorno físico)
> **ISO/IEC 27001:** A.7.1-A.7.14 (seguridad física y ambiental) · A.7.10 (prevención de robo) · A.7.12 (seguridad de cableado)
> **BCU:** EMG — control de acceso físico y protección de centros de datos
> **URCDP:** Ley 18.331 art. 10 — las medidas físicas protegen los datos personales en soporte físico y digital
> **Nivel del curso:** 🟢 Descubrir → 🟡 Practicar

---

### ENCABEZADO
| **Campo** | **Valor** |
|---|---|
| **Código** | POL-09 |
| **Título** | Seguridad Física y del Entorno |
| **Versión** | 1.0 |
| **Estado** | [Borrador / En revisión / Aprobado] |
| **Fecha de aprobación** | [COMPLETAR] |
| **Elaborado por** | Seguridad Física + RSI |
| **Revisado por** | Comité de Seguridad · Facilities |
| **Aprobado por** | Dirección General |
| **Clasificación** | Uso interno |
| **Próxima revisión** | [Fecha, máx. 1 año] |

### 1. Objetivo
Proteger los **edificios, salas, equipos, centros de datos y medios físicos** del Banco contra accesos no autorizados, daños, robo e incidentes ambientales (incendio, inundación, corte eléctrico).

### 2. Alcance
Aplica a todas las sedes, salas de servidores, salas técnicas, sucursales, áreas administrativas, equipos portátiles y medios físicos de almacenamiento.

### 3. Reglas obligatorias
- **Control de acceso físico**: puertas con tarjeta/biometría; acceso por zonas según función (menor privilegio físico).
- **Zonas sensibles** (datacenter, sala de comunicaciones): acceso restringido, registro de visitas y acompañamiento.
- **Visitas y contratistas**: registro de ingreso/egreso, identificación visible y acompañamiento en zonas sensibles.
- **Seguridad ambiental**: extinción de incendios, detección de agua, control de temperatura/humedad, energía redundante (UPS/grupo electrógeno) en datacenter.
- **Equipos móviles**: se aseguran (cable de seguridad) en áreas de atención al público; nunca se dejan desatendidos (POL-18).
- **Medios físicos** (discos, cintas, impresiones): almacenamiento bajo llave y **destrucción segura** al vencerse (PRO-09).
- **Cableado y planta**: acceso protegido; los puertos de red sin uso se deshabilitan o se controlan (POL-12).
- **Escritorio y pantalla limpia**: sin información confidencial a la vista (POL-18).
- Los incidentes físicos se reportan por el canal de incidentes (POL-07/PRO-04).

### 4. Responsabilidades
- **Seguridad Física**: operación de controles físicos, videovigilancia, rondas.
- **Facilities**: mantenimiento ambiental y estructural.
- **RSI**: coordina la seguridad física con la lógica en zonas sensibles.
- **Todo el personal**: porta credencial, no permite colados (social engineering), reporta anomalías.

### 5. Cumplimiento y revisión
Las violaciones de acceso físico se investigan como incidentes. Revisión anual de la política y auditorías periódicas de acceso físico.

### Evidencia del kit
| Evidencia | Documento canónico |
|---|---|
| Registro de visitas y accesos | PR-04 |
| Registro de acceso al datacenter | PR-04, PR-03 |
| Inventario de activos físicos | ID-01 |
| Controles ambientales | BCU-01 |
| Procedimiento de destrucción | PRO-09 |
