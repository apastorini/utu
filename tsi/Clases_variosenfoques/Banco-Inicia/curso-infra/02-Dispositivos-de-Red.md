# INFRA-02 · Dispositivos de Red

> **Función del MCU 5.0:** Este módulo explica cada dispositivo de red que encontrará el RSI en el relevamiento de infraestructura: switches, routers, firewalls, APs, IDS/IPS, balanceadores, concentradores VPN y sistemas de monitoreo.
> **ISO/IEC 27001:** Los controles del Anexo A (gestión de activos, control de accesos, gestión de vulnerabilidades, registro de eventos) se aplican directamente sobre estos dispositivos.
> **BCU:** La gestión de riesgos tecnológicos exige inventariar, parchear y controlar el acceso a los dispositivos de red; un dispositivo olvidado es un riesgo invisible.
> **URCDP:** El inventario de sistemas del Documento de Seguridad URCDP-01 debe listar los dispositivos, su firmware y su responsable.
> **Nivel del curso:** 🟢 Descubrir · 🟡 Practicar · 🔴 Dominar

---

## 1. El switch: el cartero del edificio

Un **switch** conecta los equipos de una misma red (o subred) y entrega los datos a quien corresponde. Es el **cartero del edificio**: recibe un paquete y lo lleva al departamento exacto.

- Trabaja en la **capa 2** (enlace): usa las direcciones MAC (identificadores físicos únicos de cada tarjeta de red), no las IPs.
- Tiene varios **puertos** (RJ45 o fibra) donde se enchufan las computadoras, impresoras y cámaras.
- Puede soportar **VLANs**: en un mismo switch conviven varios "barrios" lógicos sin que el tráfico se cruce.
- Los switches **administrables** permiten configurar VLANs, calidad de servicio y puertos de acceso (una MAC por puerto), y generan **logs** de conexiones.

### Diferencia con el hub

El **hub** era el dispositivo antiguo que repetía cada dato a todos los puertos (el cartero que gritaba la carta para que la oiga todo el edificio). El switch es inteligente y entrega solo al destinatario. En el Banco ya no deberían existir hubs: todo es conmutado.

### Errores comunes

- ☐ Switches sin segmentar: todo el mundo en la misma VLAN (se rompe el aislamiento).
- ☐ Dejar puertos libres sin proteger: cualquiera puede enchufar un cable y entrar a la red (control de puertos).
- ☐ Credenciales de administración por defecto (`admin/admin`).
- ☐ Firmware desactualizado sin parches (PR-06).

---

## 2. El router: el policía de tránsito

Un **router** conecta redes entre sí. Es el **policía de tránsito** que decide por qué camino se manda cada auto (paquete) para llegar a otra ciudad (otra subred o red).

- Trabaja en la **capa 3** (red): usa las direcciones IP.
- Mantiene una **tabla de rutas**: sabe qué caminos existen y cuál es el mejor para cada destino.
- En una oficina, el router suele ser también el **gateway** (la salida del barrio) que vimos en INFRA-01.
- Une la LAN de la sucursal con la WAN que llega a Casa Central.

### Errores comunes

- ☐ Rutas estáticas mal escritas: el tráfico "da vueltas" o se pierde.
- ☐ Puertos administrativos (web, SSH) expuestos a Internet.
- ☐ No documentar la tabla de rutas en el inventario.

---

## 3. El firewall: el guardia de seguridad

El **firewall** es el **guardia de seguridad del edificio**: decide quién entra, quién sale y qué puede llevar. Es el primer control de la frontera de la red. (El detalle profundo de reglas y configuración se ve en **INFRA-03**; aquí vemos el primer contacto.)

- Trabaja en base a **reglas allow/deny** (permitir/denegar): se define qué origen, qué destino y qué puerto está autorizado.
- Puede ser **hardware** (un aparato dedicado, común en Casa Central) o **software** (un programa instalado en un servidor o en la propia computadora).
- Separa zonas: Internet, DMZ (servidores públicos), red interna. Cada zona tiene reglas distintas.
- Registra **logs**: cada conexión permitida o bloqueada queda anotada (insumo para DE-01).

### Errores comunes

- ☐ Regla "permitir todo" para "agilizar" la operación: es dejar la puerta abierta.
- ☐ Firewall sin administrador definido ni revisión periódica de reglas.
- ☐ Olvidar que el firewall también controla la salida (egreso), no solo la entrada.

---

## 4. Punto de acceso inalámbrico (AP) y controlador

Un **punto de acceso (AP)** da **WiFi**: permite que celulares, notebooks y tablets se conecten sin cables. Es el **puente inalámbrico** hacia la red cableada.

- Emite una o más **SSID** (nombres de la red WiFi, ejemplo: `Banco-Empleados`, `Banco-Invitados`).
- Usa **WPA2 o WPA3** para cifrar el tráfico (jamás WiFi abierta o WEP, que están rotos).
- Con **redes de invitados** separadas por VLAN: los visitantes navegan pero no tocan la red interna.
- El **controlador** (físico o virtual) administra muchos APs a la vez: configuración centralizada, actualización de firmware y monitoreo.

### Errores comunes

- ☐ WiFi abierta o con clave por defecto de fábrica.
- ☐ Invitados y empleados en la misma red.
- ☐ APs viejos que solo soportan WEP/WPA, sin parches.
- ☐ APs ubicados de forma que la señal salga a la calle sin control.

---

## 5. Módem / ONT / router del proveedor

El **módem** o **ONT** (para fibra óptica) es el equipo que **termina la conexión del ISP** (proveedor de Internet). Es el **límite con el proveedor**: hasta ahí llega el control del banco, de ahí hacia fuera el control es del ISP.

- En casa, el "router del proveedor" combina módem + router + AP en un solo aparato.
- En una empresa como el Banco, este equipo queda normalmente **detrás del firewall** del banco: el equipo del proveedor entrega la línea y el firewall del banco la controla.
- Es importante saber qué equipo es de quién (del ISP o del banco) para saber de quién es la responsabilidad de parchearlo (PR-06).

### Errores comunes

- ☐ Dejar credenciales del proveedor por defecto en el equipo del ISP.
- ☐ No saber quién administra ese equipo (falta de responsables en el inventario).

---

## 6. IDS / IPS: los detectores y preventores

El **IDS** (Sistema de Detección de Intrusos) **detecta** actividad sospechosa y **alerta**. El **IPS** (Sistema de Prevención de Intrusos) detecta y además **bloquea** en el acto.

| Aspecto | IDS | IPS |
|---------|-----|-----|
| Acción | Observa y avisa (detección pasiva) | Bloquea (prevención activa) |
| Ubicación típica | En paralelo (copia del tráfico) | En serie (en el camino del tráfico) |
| Analogía | El guardia que anota sospechosos y llama por radio | El guardia que corta el paso directamente |

Se colocan en los puntos importantes (borde de Internet, entre zonas) y sus alertas alimentan el sistema de monitoreo (DE-01).

### Errores comunes

- ☐ Un IPS mal configurado bloquea tráfico legítimo (falsos positivos que cortan la operación).
- ☐ Un IDS cuyas alertas nadie revisa: detecta pero no sirve para nada.

---

## 7. Balanceador de carga

El **balanceador de carga** reparte el tráfico entre varios servidores para que ninguno se sature. Es el **recepcionista** que manda a los clientes a la ventanilla menos ocupada.

- Sirve para **alta disponibilidad**: si un servidor falla, el balanceador redirige a los demás sin que el usuario note la caída.
- Se usa sobre todo para los servicios expuestos (Banco En Línea) y para servidores de aplicaciones internas.
- Deja **logs** de quién pidió qué y a qué servidor se le asignó.

### Errores comunes

- ☐ Balanceador sin verificación de salud de los servidores (manda tráfico a un servidor caído).
- ☐ No documentar qué aplicaciones están detrás de cada balanceador.

---

## 8. Concentrador VPN y túneles VPN

Una **VPN** crea un **túnel cifrado** entre dos puntos a través de una red pública. Es como una **tubería blindada**: aunque pase por territorio ajeno, nadie puede leer lo que viaja dentro.

- **VPN cliente-site:** un empleado desde su casa se conecta a la red del banco (el concentrador VPN de Casa Central autoriza y cifra).
- **VPN site-to-site:** dos sedes del banco se conectan entre sí por un túnel permanente (Casa Central con cada sucursal).
- El **concentrador VPN** es el punto donde terminan todos los túneles; aplica autenticación (usuario, token, certificado) y controla qué puede tocar cada conexión.

### Errores comunes

- ☐ Túneles VPN sin cifrado o con cifrado débil.
- ☐ Cuentas VPN compartidas entre varios empleados.
- ☐ No cerrar las sesiones VPN inactivas.

---

## 9. Servidor proxy y filtrado de contenido

Un **proxy** es un intermediario: los equipos le piden a él que traiga las páginas en su lugar. Es el **mensajero** que sale a la calle en representación de la oficina.

- Centraliza la salida a Internet: el banco solo expone la IP del proxy, no la de cada empleado.
- Permite **filtrado de contenido**: se puede bloquear sitios no autorizados o categorías de riesgo.
- Complementa al firewall (filtra a nivel de aplicación/sitio, no solo de IP/puerto).

### Errores comunes

- ☐ Empleados que eluden el proxy (salida directa) sin control.
- ☐ Proxy con listas de bloqueo desactualizadas.

---

## 10. Sistema de monitoreo y SIEM

Un **SIEM** (Sistema de Gestión de Eventos e Información de Seguridad) **recolecta y correlaciona** los logs de todos los dispositivos: firewalls, switches, routers, servidores, VPN. Es el **central telefónico del guardia**: recibe todos los llamados, los cruza y detecta patrones anormales.

- Se conecta a los dispositivos mediante protocolos de registro (syslog) y les pide eventos.
- Detecta cosas como: muchos intentos de acceso a un mismo servidor, o una VPN conectada a horas extrañas.
- **DE-01** (registro de eventos) depende de que los dispositivos envíen sus logs al SIEM; si un dispositivo no está conectado, "no existe" para el monitoreo.

### Errores comunes

- ☐ Dispositivos que no envían logs al SIEM (cobertura incompleta).
- ☐ Alertas que nadie atiende (saturación y ruido).
- ☐ Relojes de los dispositivos desincronizados: los eventos no se correlacionan por fecha/hora.

---

## 11. Tabla resumen: dispositivo, capa y evidencia

| Dispositivo | Capa | Para qué sirve | Evidencia que deja |
|-------------|------|----------------|--------------------|
| Switch | 2 | Conectar equipos, segmentar VLANs | Logs de conexión, configs de VLAN |
| Router | 3 | Unir redes, elegir rutas | Tablas de rutas, logs de tráfico |
| Firewall | 3/4 | Permitir/denegar tráfico | Logs de conexiones permitidas y bloqueadas |
| AP / controlador | 2 | WiFi segura, SSID, invitados | Logs de asociación WiFi |
| Módem / ONT | 1 | Límite con el ISP | Logs del proveedor (externo) |
| IDS / IPS | 3/4 | Detectar y bloquear intrusos | Alertas, eventos de bloqueo |
| Balanceador | 4/7 | Repartir tráfico, alta disponibilidad | Logs de balanceo, health checks |
| Concentrador VPN | 3/4 | Túneles cifrados remotos | Logs de conexión/desconexión VPN |
| Proxy | 7 | Intermediario y filtrado | Logs de navegación |
| SIEM | Todas | Correlacionar eventos | Base de eventos central |

---

## 12. Perfil típico de la infraestructura del Banco (ejemplo a adaptar)

Este es un ejemplo orientativo de cómo se ven las redes de un banco. Cada sucursal es diferente; el RSI debe adaptarlo a la realidad relevada.

```
Internet ──> Firewall borde (Casa Central) ──> DMZ (Banco En Línea, web, correo)
                       │
                       ├──> LAN Casa Central (empleados) con VLANs por área
                       ├──> Concentrador VPN (empleados remotos)
                       └──> WAN ──> Firewall sucursal ──> Switch sucursal ──> PCs y cajeros
```

Características típicas:
- **Casa Central:** firewall de borde, DMZ con los servidores públicos, LAN segmentada por VLANs, SIEM central.
- **Sucursales:** router/firewall de acceso, uno o más switches, APs para WiFi de empleados, cámaras en VLAN aparte.
- **Cajeros y puntos de venta:** segmento propio, aislado del resto de la red de la sucursal.

---

## 13. Errores comunes en dispositivos (resumen)

- ☐ Switches sin segmentar en VLANs.
- ☐ Credenciales de administración por defecto.
- ☐ Dispositivos sin parches de firmware (PR-06).
- ☐ WiFi abierta o con seguridad vieja.
- ☐ Puertos administrativos (SSH/web) expuestos a Internet.
- ☐ Dispositivos sin logs enviados al SIEM.
- ☐ Equipos sin responsable asignado en el inventario.

---

## 14. Relación con el kit Banco-Inicia

| Documento | Cómo ayuda este módulo |
|-----------|------------------------|
| ID-01 (Inventario de Activos) | Registrar cada dispositivo como activo con IP, VLAN, firmware y responsable |
| PR-01 (Acceso y Administración) | Definir quién puede entrar a cada dispositivo y con qué método |
| PR-06 (Parches y Vulnerabilidades) | Programar el parcheo de firmware de switches, routers, firewalls, APs |
| PR-04 (Seguridad Física) | Saber dónde están los racks y armarios que contienen estos equipos |
| DE-01 / DE-02 (Logs y Detección) | Asegurar que todos los dispositivos envíen logs al SIEM |
| URCDP-01 | Alimentar el inventario de sistemas del Documento de Seguridad |
| MATRIZ-001 | Asociar cada dispositivo a las aplicaciones que soporta |

### Mini-tabla de ejemplo: inventario de dispositivos (para ID-01)

| Tipo | Marca/Modelo | IP | VLAN | Firmware | Responsable |
|------|--------------|-----|------|----------|-------------|
| Firewall | FortiGate 100F | 10.0.0.1 | n/a | v7.2.5 | Analista de Red |
| Switch núcleo | Cisco Catalyst 9300 | 10.0.1.1 | nativa/100 | IOS-XE 17.9 | Analista de Red |
| Switch sucursal | Cisco Catalyst 2960 | 10.20.1.1 | 200 | IOS 15.2 | Técnico Sucursal |
| AP | Aruba AP-515 | 10.0.5.10 | 300 | 8.10 | Analista de Red |
| Concentrador VPN | FortiGate VPN SSL | 10.0.0.2 | n/a | v7.2.5 | Analista de Seguridad |
| Balanceador | F5 BIG-IP | 10.0.2.1 | 400 | 17.1 | Administrador de Apps |

> La mini-tabla es un ejemplo: rellénela el RSI con los datos reales de cada sucursal.

---

## 15. Glosario rápido

| Término | Significado simple |
|---------|--------------------|
| Switch | Cartero del edificio: entrega a cada puerto |
| Router | Policía de tránsito: une redes y elige rutas |
| Firewall | Guardia de seguridad: permite o deniega |
| AP | Puente WiFi hacia la red cableada |
| SSID | Nombre de la red WiFi |
| IDS/IPS | Detecta / detecta y bloquea intrusos |
| Balanceador | Recepcionista: reparte carga entre servidores |
| VPN | Tubería cifrada a través de redes ajenas |
| Proxy | Mensajero que navega en nombre de la oficina |
| SIEM | Central telefónico que cruza todos los logs |
| Firmware | Software interno del dispositivo |

---

**Documentos relacionados:** GV-01, GV-02, ID-01, PR-01, PR-04, PR-06, DE-01, DE-02, URCDP-01, MATRIZ-001
