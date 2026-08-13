# Clase 15: VPN, Tuneles, Puentes de Red y Respuesta a Incidentes Empresariales

**Duracion:** 2 horas

---

## Objetivos de Aprendizaje

- Comprender que es una VPN, sus tipos y protocolos, y como se usa en entornos empresariales.
- Configurar tuneles SSH, VPN WireGuard y puentes de red en escenarios reales.
- Identificar los tipos de infecciones empresariales mas comunes, con enfasis en ransomware.
- Aplicar un plan de respuesta a incidentes paso a paso: deteccion, contencion, erradicacion, recuperacion.
- Resolver ejercicios practicos de configuracion de VPN, tuneles, bridges y simulacion de respuesta a incidentes.

---

## Contenido Detallado

### PARTE 1: VPN, TUNELES Y PUENTES DE RED (50 min)

---

### 1. Que es una VPN (Virtual Private Network)?

Una VPN es una tecnologia que permite extender una red privada sobre una red publica, como Internet. Crea un tunel cifrado entre dos puntos, de modo que los datos viajan como si estuvieran en una red local privada, aunque esten cruzando redes no confiables.

**Analogia:** Imagine una autopista publica (Internet) donde todos pueden ver lo que transporta. Una VPN es como un tunel privado dentro de esa autopista: sus datos viajan por el mismo camino fisico, pero dentro del tunel nadie mas puede verlos ni modificarlos.

**Para que sirve:**
- **Teletrabajo:** empleados se conectan a la red corporativa desde sus hogares.
- **Conexion entre sedes:** oficinas en diferentes paises conectadas como si estuvieran en la misma red.
- **Privacidad:** oculta la direccion IP y cifra el trafico ante el ISP y otros observadores.
- **Bypass de censura:** permite acceder a contenido bloqueado geograficamente.

---

### 2. Tipos de VPN

**VPN Site-to-Site (conexion entre oficinas):** Conecta redes enteras entre si. Por ejemplo, la red de la oficina en Madrid con la red de la oficina en Buenos Aires. Los protocolos tipicos son IPsec y MPLS. Los usuarios no notan la VPN: sus equipos ven la otra oficina como si estuviera en la misma red local.

**VPN Remote Access (usuario remoto -> red corporativa):** Un empleado desde su casa o un cafe se conecta a la red de la empresa. Protocolos: OpenVPN, WireGuard, IPsec IKEv2. El usuario debe iniciar la conexion manualmente o mediante un cliente.

**SSL VPN (via navegador, sin cliente):** Se accede a traves del navegador web usando SSL/TLS. No requiere instalar software. Ejemplos: OpenVPN en modo SSL, Cisco AnyConnect. Es util para usuarios que no pueden instalar aplicaciones en sus equipos.

**VPN Movil:** Disenada para dispositivos moviles (smartphones, tablets). Siempre activa, se reconecta automaticamente cuando cambia de red (WiFi a 4G). Usa protocolos optimizados para bajo consumo de bateria.

---

### 3. Protocolos de VPN (comparativa)

| Protocolo | Puertos | Cifrado | Velocidad | Seguridad |
|-----------|---------|---------|-----------|-----------|
| IPsec IKEv2 | UDP 500, 4500 | AES-256 | Alta | Muy alta |
| OpenVPN | UDP 1194 / TCP 443 | AES-256-GCM | Media | Muy alta |
| WireGuard | UDP 51820 | ChaCha20 | Muy alta | Alta |
| PPTP | TCP 1723 | MPPE-128 | Alta | MUY BAJA (no usar) |
| L2TP/IPsec | UDP 1701 | AES-256 | Baja | Alta |

**Explicacion de cada protocolo:**

**IPsec IKEv2:** Es el estandar empresarial. Usa los puertos UDP 500 (IKE) y UDP 4500 (NAT-T). Ofrece cifrado AES-256 y autenticacion mutua mediante certificados o PSK (Pre-Shared Key). Es rapido porque IKEv2 maneja bien los cambios de red (moverse de WiFi a datos moviles sin cortar la VPN). Muy seguro, usado por gobiernos y grandes corporaciones.

**OpenVPN:** Es el mas flexible. Puede correr sobre UDP (puerto 1194) o TCP (puerto 443, que pasa por casi cualquier firewall). Usa OpenSSL para cifrado (AES-256-GCM). Es de codigo abierto y tiene clientes para todas las plataformas. Es mas lento que WireGuard porque tiene mas sobrecarga de procesamiento.

**WireGuard:** Es el mas moderno y rapido. Usa el puerto UDP 51820, cifrado ChaCha20 (mas rapido que AES en CPUs sin aceleracion hardware). Tiene solo 4000 lineas de codigo (vs cientos de miles de OpenVPN), lo que facilita la auditoria de seguridad. Es el recomendado para proyectos nuevos.

**PPTP:** Es el mas antiguo (protocolo de los anos 90). Usa cifrado MPPE-128 que es debil y tiene vulnerabilidades conocidas. NO debe usarse bajo ninguna circunstancia. Aunque es rapido, su seguridad es inaceptable.

**L2TP/IPsec:** Combina L2TP (tunel de capa 2) con IPsec (cifrado). Es seguro pero lento porque encapsula dos veces (doble sobrecarga). Usa UDP 1701.

---

### 4. Tuneles de red (Network Tunneling)

Un tunel de red es una tecnica que encapsula un protocolo de red dentro de otro. Permite que trafico que normalmente estaria bloqueado o seria inseguro viaje a traves de redes restrictivas.

**Tunel SSH:** Redireccion de puertos usando el protocolo SSH. Es la forma mas sencilla de crear un tunel seguro.

**Tunel SSH local** (forward local): el cliente escucha en un puerto local y reenvia el trafico a un destino a traves del servidor SSH.

```
ssh -L 8080:servidor-interno:80 usuario@bastion
```

Explicacion: `-L` indica forward local. `8080` es el puerto local. `servidor-interno:80` es el destino al que se quiere llegar (solo accesible desde el servidor bastion). `usuario@bastion` es el servidor SSH intermedio. Al abrir `http://localhost:8080` en el navegador local, el trafico viaja por SSH hasta el bastion, y desde ahi al servidor interno en el puerto 80.

**Tunel SSH remoto** (forward remoto): el servidor SSH escucha en un puerto y reenvia el trafico al cliente. Sirve para exponer un servicio local a Internet sin abrir puertos en el firewall.

```
ssh -R 8080:localhost:3000 usuario@publico
```

Explicacion: `-R` indica forward remoto. El servidor `publico` escucha en el puerto 8080 y reenvia el trafico al cliente SSH (la maquina local) en el puerto 3000. Util para mostrar un prototipo local a un cliente sin desplegarlo.

**Tunel HTTP/HTTPS:** Usa el metodo CONNECT del protocolo HTTP para establecer tuneles a traves de proxies. Los clientes HTTP envian un comando `CONNECT host:puerto HTTP/1.1` y el proxy establece un tunel TCP. Es como funcionan los proxies HTTPS.

**Tunel DNS:** Es una tecnica de ataque que codifica datos en consultas DNS. Como el trafico DNS suele estar permitido en los firewalls (las empresas necesitan resolver nombres de dominio), un atacante puede exfiltrar datos codificandolos como subdominios. Ejemplo: `base64data.ejemplo.com` - el servidor DNS del atacante registra la consulta y decodifica los datos.

**Tunel ICMP:** Similar al tunel DNS, pero usando paquetes ping (ICMP Echo Request). Los datos se esconden en el campo de datos del paquete ICMP. Es lento pero util cuando solo ping esta permitido.

**ngrok / Cloudflare Tunnel:** Servicios que crean tuneles a Internet sin abrir puertos en el firewall. ngrok expone un servidor local a traves de una URL publica (`https://hash.ngrok.io`). Cloudflare Tunnel (anteriormente Argo Tunnel) hace lo mismo pero integrado con Cloudflare. Muy utiles para desarrollo y demos.

---

### 5. Puentes de red (Network Bridge)

Un bridge (puente de red) es un dispositivo que conecta dos segmentos de red a nivel de capa 2 (nivel de enlace de datos, direcciones MAC). A diferencia de un router (capa 3, IP), un bridge opera con direcciones MAC y no modifica las direcciones IP.

**Diferencia bridge vs router vs switch:**

| Dispositivo | Capa OSI | Unidad de reenvio | Funcion principal |
|-------------|----------|-------------------|-------------------|
| Hub | Capa 1 (fisica) | Bits | Repetir senal a todos los puertos |
| Switch | Capa 2 (enlace) | MAC | Reenviar tramas segun MAC destino |
| Bridge | Capa 2 (enlace) | MAC | Conectar 2 segmentos de red filtrando trafico |
| Router | Capa 3 (red) | IP | Reenviar paquetes segun IP destino |

Un bridge conecta dos redes como si fueran una sola. Los dispositivos en ambos lados del bridge ven todos los dispositivos como si estuvieran en la misma red local.

**Bridge en Linux:** Se puede crear un bridge con `brctl` (deprecado) o con `ip link`:

```bash
# Crear un bridge
ip link add name br0 type bridge

# Agregar interfaces al bridge
ip link set eth0 master br0
ip link set eth1 master br0

# Activar el bridge
ip link set br0 up
```

**Bridge en Docker:** Cuando se crea una red bridge personalizada, Docker crea un bridge virtual en el host. Los contenedores conectados a esa red pueden comunicarse por nombre de contenedor.

```bash
# Crear red bridge personalizada
docker network create --driver bridge mi-red

# Conectar contenedores a la misma red
docker run --network=mi-red --name contenedor1 nginx
docker run --network=mi-red --name contenedor2 alpine ping contenedor1
```

**Bridge en VirtualBox:** El modo "Red Adaptador Puente" (Bridged Adapter) conecta la maquina virtual directamente a la red fisica del host. La VM obtiene una IP del mismo rango que la LAN fisica (por DHCP del router de la red), como si fuera un dispositivo mas conectado al mismo switch.

**Escenario real:** Un laboratorio de pruebas donde se tienen varias VMs en modo bridge. Todas las VMs obtienen IPs de la red corporativa y pueden comunicarse con los equipos reales. Esto permite simular una red real sin necesidad de equipos fisicos adicionales.

---

### 6. Escenarios reales de uso

**VPN Site-to-Site - sucursal bancaria conectada a matriz via IPsec:**
Un banco con 50 sucursales. Cada sucursal tiene un router con IPsec configurado hacia el router central de la matriz. Todo el trafico entre sucursales esta cifrado. Los empleados de cualquier sucursal pueden acceder a la base de datos central como si estuvieran en la misma red.

**VPN Remote Access - empleados conectandose desde casa con WireGuard:**
Una empresa de 200 empleados implementa WireGuard. Cada empleado tiene un archivo de configuracion con una clave privada unica. Al conectarse, obtienen una IP interna (10.0.0.x) y pueden acceder a recursos corporativos (servidores de archivos, intranet, ERP) como si estuvieran en la oficina.

**Bridge para laboratorios - VMs en bridge mode para simular red real:**
Un equipo de seguridad crea 5 VMs en VirtualBox con modo bridge. Una VM es un servidor Linux con servicios web y base de datos. Otra VM es un cliente Windows. Otra es un Kali Linux para pruebas de penetracion. Todas estan en la misma red que el host, lo que permite probar ataques y defensas en un entorno controlado pero realista.

**SSH Tunnel para administracion remota - acceso a base de datos en red interna:**
Un administrador necesita conectarse a una base de datos PostgreSQL que solo escucha en la red interna (no tiene IP publica). El administrador tiene acceso SSH a un servidor bastion. Usa:

```bash
ssh -L 5432:bd-interna:5432 admin@bastion.empresa.com
```

Ahora el administrador puede conectar su pgAdmin local a `localhost:5432` y el trafico viaja cifrado por SSH hasta el bastion, que lo reenvia a la base de datos interna.

---

### PARTE 2: INFECCIONES EMPRESARIALES Y RESPUESTA A INCIDENTES (70 min)

---

### 7. Tipos de infecciones empresariales comunes

**Ransomware:** Malware que cifra los archivos de la victima y exige un rescate (generalmente en criptomonedas) para descifrarlos. Ejemplos historicos: WannaCry (2017), REvil (2019-2021), LockBit (2021-2023), BlackCat/ALPHV (2022-2024). Es la amenaza mas costosa para las empresas.

**Phishing / Spear Phishing:** Correo electronico enganoso que suplanta a una entidad confiable (banco, proveedor, CEO) para robar credenciales o instalar malware. El spear phishing es una version dirigida: el atacante investiga a la victima y personaliza el mensaje.

**Business Email Compromise (BEC):** Suplantacion de ejecutivos de alto nivel (CEO, CFO) para ordenar transferencias bancarias fraudulentas. No requiere malware, solo ingenieria social. Segun el FBI, ha generado perdidas por mas de 50 mil millones de dolares.

**Malware / Trojan:** Software malicioso que se hace pasar por legitimo. Ejemplos: Emotet (botnet bancario), QakBot (trojan de acceso inicial). Una vez instalado, puede robar datos, descargar mas malware, o dar acceso remoto al atacante.

**RAT (Remote Access Trojan):** Tipo de trojan que permite el control remoto del equipo infectado. Ejemplos: DarkComet, njRAT, Gh0st RAT. El atacante puede ver la pantalla, grabar teclas, encender la camara, transferir archivos.

**Keyloggers / Stealers:** Malware especializado en robar credenciales. Los keyloggers registran las teclas presionadas. Los stealers (como RedLine, Raccoon, Vidar) roban contrasenas almacenadas en navegadores, cookies, archivos de carteras de criptomonedas.

**Supply Chain Attack:** Compromiso de proveedores de software o servicios para infectar a los clientes finales. Ejemplos: SolarWinds (2020, 18,000 clientes afectados, incluido el gobierno de EE.UU.), Kaseya (2021, ataque ransomware a traves de un proveedor de IT), Log4j (2021, vulnerabilidad en una libreria Java usada por millones de aplicaciones).

**Web Shell:** Script malicioso (PHP, ASP, JSP) subido a un servidor web que permite ejecutar comandos remotos. Ejemplo: `shell.php` con una linea como `<?php system($_GET['cmd']); ?>`. El atacante accede via `http://servidor/shell.php?cmd=whoami`.

---

### 8. Ransomware - Analisis detallado

**Que es ransomware?** Es un tipo de malware que cifra los archivos de la victima usando criptografia fuerte (generalmente AES-256 para cifrado simetrico y RSA-4096 para proteger la clave simetrica). Luego exige un pago (rescate) a cambio de la clave de descifrado.

**Como infecta:**
- **Phishing:** El vector mas comun. El usuario recibe un correo con un archivo adjunto malicioso (macro de Office, PDF con exploit, JS en zip).
- **RDP expuesto:** Atacantes escanean Internet en busca de puertos 3389 abiertos y prueban credenciales por fuerza bruta.
- **Vulnerabilidades en software:** Explotacion de fallos en aplicaciones sin parchear (VPNs, servidores web, sistemas de email).
- **Drive-by download:** El usuario visita un sitio web comprometido que descarga e instala el malware automaticamente.

**Ciclo de vida de un ataque ransomware:**

1. **Acceso inicial:** El atacante obtiene acceso al primer equipo. Puede ser por phishing (el empleado ejecuta la macro), RDP brute force, o explotacion de una vulnerabilidad.

2. **Establecimiento:** El malware descarga una segunda etapa desde un servidor C2 (Command & Control). Esta etapa puede desactivar el antivirus/EDR, establecer persistencia (tareas programadas, servicios, registry Run keys).

3. **Movimiento lateral:** El atacante se propaga por la red usando herramientas legitimas del sistema como PsExec (`psexec \\equipo -s cmd`), WMI (`wmic /node:equipo process call create "cmd.exe"`), SMB, RDP. El objetivo es llegar al mayor numero de equipos posibles, especialmente servidores de archivos y bases de datos.

4. **Exfiltracion:** Antes de cifrar, el atacante roba datos sensibles. Esto permite la doble extorsion: "paga o publicamos tus datos". Los datos se comprimen y se envian a servidores controlados por el atacante.

5. **Cifrado:** Se ejecuta el ransomware en masa. Los archivos se cifran y se renombran (ej: `documento.pdf` -> `documento.pdf.lockbit`). Se dejan notas de rescate en cada carpeta.

6. **Extorsion:** Aparece la nota de rescate con instrucciones para pagar (generalmente en Bitcoin o Monero), un plazo (ej: 72 horas) y la amenaza de filtrar los datos si no se paga.

**Familias famosas:**

**WannaCry (2017):** Exploto la vulnerabilidad EternalBlue (MS17-010) en el protocolo SMB de Windows. En pocas horas afecto mas de 200,000 sistemas en 150 paises. El NHS britanico, Telefonica, FedEx y Renault fueron algunas de las victimas mas conocidas. Se detuvo cuando un investigador registro un dominio "kill switch" que el malware consultaba.

**NotPetya (2017):** Aparecio pocas semanas despues de WannaCry. Disfrazado de ransomware, en realidad era un wiper: destruia los datos de forma irreversible incluso si se pagaba el rescate. Fue un ataque dirigido a Ucrania (se disfrazo de actualizacion del software contable M.E.Doc). Causo perdidas globales estimadas en 10 mil millones de dolares.

**REvil / Sodinokibi (2019-2021):** Ransomware-as-a-Service (RaaS): los desarrolladores alquilaban el malware a afiliados que realizaban los ataques. Famoso por pedir rescates millonarios (el mayor fue de 70 millones de dolares a Kaseya). El grupo fue desmantelado por autoridades rusas en 2022.

**LockBit (2021-2023):** El grupo de ransomware mas activo del mundo. Su caracteristica principal es la velocidad de cifrado (usa cifrado multihilo). Ademas, automatiza la filtracion de datos y tiene un portal de negociacion con las victimas. LockBit 3.0 introdujo el primer "bug bounty" para ransomware.

**BlackCat / ALPHV (2022-2024):** Escrito en Rust, lo que lo hace multiplataforma (Windows y Linux). Fue el primer ransomware en atacar maquinas Linux y entornos VMware ESXi. Usa cifrado ChaCha20 (rapido) y RSA-OAEP para proteger la clave.

---

### 9. Como detectar un ransomware (indicadores de compromiso)

**Senales tempranas (antes del cifrado):**

- **Procesos anomalos:** `powershell.exe` ejecutando scripts con `-EncodedCommand`, `-ExecutionPolicy Bypass`, o descargando archivos con `Invoke-WebRequest` o `Invoke-Expression`.
- **Conexiones de red a IPs sospechosas:** El equipo se conecta a IPs en rangos poco comunes (ej: 45.33.32.156, 185.220.101.x) o a dominios recien registrados.
- **Archivos .exe en carpetas temporales:** Ejecutables en `%TEMP%`, `%APPDATA%`, `%LOCALAPPDATA%` que no deberian estar ahi.
- **Desactivacion de antivirus/EDR:** Intentos de detener servicios de seguridad (`net stop WinDefend`, `sc stop SentinelService`).
- **Escaneo de red interno:** El equipo comprometido empieza a escanear la red local en busca de otros equipos (puertos 445, 3389, 139).
- **Creacion de tareas programadas:** `schtasks /create` con nombres generados aleatoriamente para establecer persistencia.

**Senales durante el ataque (cifrado en progreso):**

- **Archivos cambiando de extension:** Los archivos aparecen con nuevas extensiones como `.encrypted`, `.lockbit`, `.enc`, `.xyz`, `.crypted`.
- **Notas de rescate:** Aparecen archivos `README.txt`, `HOW_TO_DECRYPT.txt`, `RECOVERY.txt`, etc., en multiples directorios.
- **Alto consumo de I/O en discos:** El monitor de recursos muestra actividad de lectura/escritura al 100% en discos, especialmente en unidades de red.
- **Alertas de integridad de archivos (FIM):** Sistemas de monitoreo de integridad detectan cambios masivos en archivos.
- **Cambio de fondos de pantalla:** Algunas variantes cambian el fondo de pantalla por la nota de rescate.

**Herramientas de deteccion:**

- **EDR (Endpoint Detection & Response):** CrowdStrike Falcon, SentinelOne, Microsoft Defender for Endpoint. Detectan comportamientos anomalos en tiempo real.
- **SIEM:** Wazuh (open-source), Splunk, ELK Stack. Correlacionan logs de multiples fuentes para identificar patrones de ataque.
- **Sysmon + Event Logs:** Sysmon registra creacion de procesos, conexiones de red, cambios en el sistema de archivos. Los logs se envian a un SIEM para analisis.
- **YARA rules:** Reglas para detectar patrones de malware en archivos y memoria.

**Ejemplo de YARA rule para detectar ransomware:**

```
rule Ransomware_Note {
    strings:
        $note1 = "Your files have been encrypted" nocase
        $note2 = "Bitcoin" nocase
        $note3 = "Decrypt" nocase
    condition:
        all of them
}
```

Esta regla detecta archivos que contengan las tres frases, lo que es indicativo de una nota de rescate.

---

### 10. Plan de respuesta a incidentes (IR) - Paso a paso

**Paso 1: Preparacion (antes del ataque)**

La preparacion es la fase mas importante porque cuando ocurre el incidente no hay tiempo para planificar.

- Tener un plan de respuesta a incidentes documentado y aprobado por la direccion.
- Backups offline siguiendo la regla 3-2-1: 3 copias de los datos, en 2 medios diferentes, 1 copia fuera de linea (sin conexion a la red).
- EDR/SIEM implementado, configurado y monitoreado 24/7.
- Lista de contactos de emergencia: equipo de respuesta a incidentes, legal, recursos humanos, comunicaciones, direccion.
- Playbooks para los tipos de incidentes mas probables (ransomware, phishing, BEC, fuga de datos).
- Acuerdos de nivel de servicio (SLA) con proveedores de respuesta a incidentes.

**Paso 2: Identificacion / Deteccion**

- Confirmar que es un incidente real (no un falso positivo).
- Determinar el alcance: cuantos equipos afectados, que datos estan comprometidos, cual es el vector de entrada.
- Ejecutar el playbook de ransomware.
- Recopilar evidencia: capturas de pantalla, logs, imagenes de memoria (si es posible).

**Comandos iniciales en equipo sospechoso:**

```powershell
# Ver conexiones de red activas
netstat -anob | findstr ESTABLISHED

# Ver procesos con nombre sospechoso
Get-Process | Where-Object {$_.ProcessName -like "*encrypt*" -or $_.ProcessName -like "*ransom*"}

# Ver extensiones de archivos modificadas recientemente
Get-ChildItem -Path C:\ -Recurse -Filter *.encrypted -ErrorAction SilentlyContinue

# Ver tareas programadas sospechosas
schtasks /query /fo LIST /v
```

**Paso 3: Contencion**

El objetivo es evitar que el ataque se propague y limitar el dano.

- AISLAR el equipo infectado: desconectar el cable de red, deshabilitar WiFi, desconectar Bluetooth.
- Apagar switches de puertos afectados si el ransomware se propaga via SMB.
- Bloquear las IPs de C2 en el firewall perimetral y en los proxies.
- Cambiar contrasenas de cuentas comprometidas (especialmente administradores de dominio).
- Deshabilitar cuentas de servicio sospechosas.
- Deshabilitar brechas de seguridad (RDP expuesto, VPN sin MFA, etc.).
- **NO apagar el equipo:** Si se apaga, se pierde la evidencia en memoria (procesos, conexiones activas, claves de cifrado en RAM).
- **NO pagar el rescate:** No garantiza la recuperacion de los datos y financia futuros ataques.

**Paso 4: Erradicacion**

- Identificar el vector de entrada y cerrarlo definitivamente.
- Eliminar el malware de los equipos afectados (usando herramientas EDR o formateo).
- Parchear la vulnerabilidad que permitio el acceso inicial.
- Reinstalar sistemas comprometidos desde cero (recomendado sobre limpiar).
- Rotar TODAS las credenciales: contrasenas de dominio, servicios, aplicaciones, VPN, WiFi.
- Revocar y regenerar certificados y tokens comprometidos.

**Paso 5: Recuperacion**

- Restaurar desde backups limpios (verificar primero que los backups NO estan infectados).
- Probar la integridad de los datos restaurados (no solo que existan, sino que funcionen).
- Implementar controles adicionales para prevenir recurrencia:
  - MFA obligatorio en todos los accesos remotos.
  - Segmentacion de red (los servidores de archivos no deben estar en la misma red que los usuarios).
  - Deshabilitar macros de Office por politicas de grupo.
  - Bloquear ejecucion de scripts en %TEMP% y %APPDATA% con AppLocker o WDAC.
- Monitorear intensivamente durante las primeras semanas post-recuperacion.

**Paso 6: Lecciones Aprendidas**

- Reunion post-mortem con todas las partes involucradas (TI, seguridad, direccion, usuarios afectados).
- Actualizar el plan de respuesta a incidentes con lo aprendido.
- Mejorar controles de seguridad basado en las brechas identificadas.
- Capacitar a empleados (especialmente sobre phishing).
- Reportar a autoridades si aplica (INCIBE, Policía Cibernetica, etc.).
- Compartir indicadores de compromiso (IOCs) con la comunidad (MISP, VirusTotal).

---

### 11. Escenario real simulado - Ransomware LockBit

**Contexto:** PYME de 50 empleados. El departamento de contabilidad recibe un correo con una factura falsa de un proveedor conocido.

**El ataque paso a paso:**

1. **El empleado** hace clic en el enlace "Descargar Factura" que descarga un archivo Excel con una macro maliciosa.
2. **La macro** ejecuta un comando PowerShell oculto que descarga el binario de LockBit desde un servidor C2 en la nube (ej: `185.234.72.18:8080`).
3. **LockBit** se ejecuta, desactiva Windows Defender usando `Set-MpPreference -DisableRealtimeMonitoring $true`, y establece persistencia via tarea programada.
4. **Movimiento lateral:** LockBit escanea la red local (rango 192.168.1.0/24), encuentra el servidor de archivos (192.168.1.10) con SMB abierto, y usa credenciales robadas de la sesion del usuario para conectarse y ejecutar el ransomware en el servidor.
5. **Cifrado:** LockBit cifra 500GB de datos compartidos: documentos de Office, PDFs, bases de datos Access, archivos de diseno, backups de la NAS.
6. **Nota de rescate:** En cada carpeta aparece `README-LOCKBIT.txt` con instrucciones de pago: 5 BTC (~350,000 USD al momento del ataque).

**Preguntas para el analisis:** Que haria paso a paso? Como detectaria? Como conteneria? Como recuperaria?

**SOLUCION - Plan de respuesta detallado (10 pasos):**

**Paso 1: Confirmar el incidente**
- El equipo de TI recibe alertas de EDR: "Desactivacion de antivirus en equipo PC-CONTABILIDAD-05" y "Conexiones a IP sospechosa 185.234.72.18".
- Usuarios reportan que no pueden abrir archivos en la unidad compartida Z:.
- Confirmar revisando: los archivos tienen extension `.lockbit` y hay `README-LOCKBIT.txt` en las carpetas.

**Paso 2: Activar el equipo de respuesta a incidentes**
- Convocar al equipo IR: TI, seguridad, legal, direccion.
- Notificar a la direccion: "Tenemos un incidente de ransomware en curso".
- Iniciar el playbook de ransomware.

**Paso 3: Contencion inmediata**
- Desconectar el cable de red del equipo PC-CONTABILIDAD-05 (aislarlo fisicamente).
- Apagar el puerto del switch al que esta conectado el servidor de archivos (para evitar que el cifrado continue).
- Bloquear en el firewall la IP 185.234.72.18 y el puerto 8080.
- Deshabilitar temporalmente el acceso SMB (puerto 445) desde la VLAN de usuarios a la VLAN de servidores.
- Cambiar la contrasena del usuario de contabilidad.

**Paso 4: Evaluar el dano**
- Determinar alcance: servidor de archivos afectado, PC de contabilidad afectado, ?mas equipos?
- Revisar logs de red: ?hubo conexiones salientes a otros C2? ?Se intento acceder a bases de datos?
- Verificar si hay exfiltracion de datos (logs de DNS, proxy, firewall).
- Estimar volumen de datos cifrados y criticidad.

**Paso 5: Preservar evidencia**
- Hacer imagen forense del disco del PC de contabilidad (si es posible).
- Capturar la memoria RAM del equipo (antes de apagarlo).
- Registrar los indicadores de compromiso: IP del C2, hash del binario, nombres de archivos de rescate, extension de archivos cifrados.
- Tomar capturas de pantalla de la nota de rescate, alertas del EDR, logs.

**Paso 6: Erradicacion**
- Determinar vector de entrada: correo de phishing con factura falsa.
- Bloquear el remitente del correo en el servidor de correo.
- Enviar comunicado a todos los empleados: "No abrir correos de X proveedor, no ejecutar archivos adjuntos sin verificar".
- Reinstalar el PC de contabilidad desde cero.
- Restaurar el servidor de archivos desde backup (despues de verificar que los backups no estan cifrados).

**Paso 7: Recuperacion de datos**
- Verificar que los backups estan limpios: revisar que no tengan archivos `.lockbit` ni `README-LOCKBIT.txt`.
- Restaurar los datos del servidor de archivos desde el backup mas reciente anterior al ataque.
- Probar que los datos restaurados son accesibles y estan completos.
- Implementar medidas temporales: los archivos restaurados se montan en una VLAN separada, solo accesible por usuarios autorizados.

**Paso 8: Mejora de controles**
- Bloquear macros de Office por GPO: solo macros firmadas por la empresa.
- Implementar AppLocker para bloquear ejecucion desde %TEMP% y %APPDATA%.
- Configurar reglas de reduccion de superficie de ataque (ASR) en Defender: bloquear ejecucion de scripts de Office que llamen a procesos hijo.
- Activar MFA para todos los accesos remotos.
- Segmentar red: crear VLAN separada para servidores de archivos con reglas de firewall restrictivas.

**Paso 9: Monitoreo post-incidente**
- Los equipos restaurados se monitorean intensivamente durante 2 semanas.
- Alertas de EDR configuradas para cualquier intento de desactivacion.
- Revision diaria de logs de firewall, proxy y DNS.
- Pruebas de recuperacion semanales.

**Paso 10: Lecciones aprendidas**
- Reunion post-mortem: ?Por que el empleado hizo clic? ?Por que las macros estaban habilitadas? ?Por que el servidor de archivos era accesible desde cualquier equipo?
- Actualizar politicas de seguridad: backups 3-2-1, prohibicion de macros, segmentacion de red.
- Capacitar a empleados trimestralmente sobre phishing.
- Reportar el incidente a las autoridades (INCIBE en Espana).

---

### 12. Otros escenarios de infeccion

**BEC (Business Email Compromise):**

- Un empleado de finanzas recibe un correo del "CEO" pidiendo una transferencia urgente de 50,000 EUR a un nuevo proveedor.
- El correo parece legitimo: mismo tono, mismo formato, pero el dominio es `empresa-urgente.com` en vez de `empresa.com`.
- Deteccion: verificar la direccion de remitente completa, no solo el nombre mostrado. Llamar al CEO por telefono para confirmar.
- Respuesta: contactar al banco inmediatamente para detener la transferencia (ventana de 24-48 horas). Reportar a las autoridades. Enviar alerta a toda la empresa.

**Web Shell en servidor web:**

- Un atacante encuentra una vulnerabilidad de subida de archivos en un formulario web y sube `shell.php`.
- Desde la web shell, ejecuta comandos: `whoami`, `ls -la /etc/`, `cat /etc/passwd`, explora la base de datos.
- Deteccion: archivos .php inusuales en carpetas de subida de archivos (uploads/, images/, tmp/). Alertas de WAF detectando parametros como `cmd=`, `exec=`, `system=`.
- Respuesta: eliminar el archivo malicioso inmediatamente. Parchear la vulnerabilidad de subida. Revisar logs del servidor web para determinar el alcance. Rotar credenciales de la base de datos.

**Fuerza bruta a RDP:**

- Un servidor con RDP abierto a Internet (puerto 3389) recibe miles de intentos de login desde IPs rusas, chinas y de Europa del Este.
- Deteccion: Event ID 4625 (login fallido) masivo en Windows Security Log. Alertas de fail2ban o similar. Picos de trafico en el puerto 3389.
- Respuesta: cambiar el puerto RDP (ej: de 3389 a 13389). Configurar VPN obligatoria para acceso remoto (RDP solo accesible desde la red interna). Activar MFA para cuentas con acceso administrativo. Configurar Account Lockout (bloquear cuenta tras N intentos fallidos).

**Data exfiltration via DNS:**

- Un empleado malicioso codifica datos de clientes como subdominios y los envia a un dominio que controla: `base64encodeddata.malicioso.com`.
- Deteccion: consultas DNS a dominios con nombres largos y aleatorios, volumen anomalo de consultas DNS desde un mismo equipo, dominios recien registrados.
- Respuesta: implementar solucion DLP (Data Loss Prevention) que monitoree el contenido de las consultas DNS. Bloquear consultas a dominios no autorizados o sospechosos. Investigar al empleado.

---

### PARTE 3: EJERCICIOS PRACTICOS

---

### 13. Ejercicio 1 - Configurar VPN WireGuard (paso a paso)

**Enunciado:** Instalar y configurar WireGuard en un servidor Linux (Ubuntu) y un cliente Windows. Probar conectividad haciendo ping a traves de la VPN.

**Solucion paso a paso:**

**Paso 1: Instalar WireGuard en el servidor (Linux)**

```bash
# Actualizar paquetes e instalar WireGuard
sudo apt update
sudo apt install -y wireguard

# Generar par de claves para el servidor
cd /etc/wireguard
umask 077  # Solo root puede leer las claves
wg genkey | tee server-private.key | wg pubkey > server-public.key

# Ver las claves generadas
cat server-private.key  # Guardar esta clave
cat server-public.key   # Compartir con los clientes
```

**Paso 2: Configurar el servidor WireGuard**

Crear el archivo `/etc/wireguard/wg0.conf`:

```ini
[Interface]
Address = 10.0.0.1/24
ListenPort = 51820
PrivateKey = <contenido-de-server-private.key>

# Reglas de firewall para NAT
PostUp = iptables -A FORWARD -i wg0 -j ACCEPT
PostUp = iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
PostDown = iptables -D FORWARD -i wg0 -j ACCEPT
PostDown = iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE

[Peer]
# Cliente Windows
PublicKey = <public-key-del-cliente>
AllowedIPs = 10.0.0.2/32
```

**Paso 3: Iniciar el servidor WireGuard**

```bash
# Activar el forwarding de IP
sudo sysctl -w net.ipv4.ip_forward=1
echo "net.ipv4.ip_forward=1" | sudo tee -a /etc/sysctl.conf

# Iniciar la interfaz WireGuard
sudo systemctl enable wg-quick@wg0
sudo systemctl start wg-quick@wg0

# Verificar el estado
sudo wg show
```

**Paso 4: Configurar el cliente Windows**

Descargar WireGuard desde https://www.wireguard.com/install/ e instalarlo.

Generar claves desde la interfaz o con comandos:

```powershell
# En PowerShell como administrador
cd C:\Program Files\WireGuard
.\wg.exe genkey | tee client-private.key | .\wg.exe pubkey > client-public.key

# Ver las claves
type client-private.key
type client-public.key
```

Crear un nuevo tunel en WireGuard con esta configuracion:

```ini
[Interface]
PrivateKey = <contenido-de-client-private.key>
Address = 10.0.0.2/24
DNS = 8.8.8.8

[Peer]
PublicKey = <public-key-del-servidor>
Endpoint = <IP-publica-del-servidor>:51820
AllowedIPs = 10.0.0.0/24, 192.168.1.0/24
PersistentKeepalive = 25
```

**Paso 5: Agregar el cliente al servidor**

Editar `/etc/wireguard/wg0.conf` en el servidor y agregar el peer (si no se agrego antes):

```ini
[Peer]
PublicKey = <public-key-del-cliente>
AllowedIPs = 10.0.0.2/32
```

Luego recargar la configuracion:

```bash
sudo wg addconf wg0 <(wg-quick strip wg0)
# O reiniciar el servicio
sudo systemctl restart wg-quick@wg0
```

**Paso 6: Probar conectividad**

```bash
# Desde el cliente, hacer ping al servidor VPN
ping 10.0.0.1

# Desde el servidor, hacer ping al cliente
ping 10.0.0.2

# Verificar el estado de la conexion
sudo wg show
```

La salida de `wg show` debe mostrar algo como:

```
interface: wg0
  public key: <server-public-key>
  private key: (hidden)
  listening port: 51820

peer: <client-public-key>
  endpoint: <IP-cliente>:12345
  allowed ips: 10.0.0.2/32
  latest handshake: 5 seconds ago
  transfer: 1.23 KiB received, 4.56 KiB sent
```

---

### 14. Ejercicio 2 - Simular un ataque de ransomware (en laboratorio controlado)

**Enunciado:** Crear una VM aislada, ejecutar un script Python que simule un ataque de ransomware (cifrado de archivos, creacion de nota), y practicar la deteccion y contencion.

**Solucion:**

**Paso 1: Crear el script Python de simulacion**

Crear el archivo `simular_ransomware.py` (ejecutar SOLO en laboratorio aislado):

```python
#!/usr/bin/env python3
"""
SIMULACION DE RANSOMWARE - SOLO USAR EN LABORATORIO AISLADO
Este script simula un ataque de ransomware con fines educativos.
No cifra realmente, solo cambia extensiones y crea notas de rescate.
"""

import os
import time
import shutil
from pathlib import Path

DIRECTORIO_BLANCO = "C:\\Laboratorio_Ransomware"
EXTENSION_CIFRADO = ".encrypted"
NOMBRE_NOTA = "README_RESCATE.txt"

def simular_cifrado():
    print(f"[+] Creando directorio de laboratorio en {DIRECTORIO_BLANCO}")
    os.makedirs(DIRECTORIO_BLANCO, exist_ok=True)

    # Crear archivos de prueba
    archivos = [
        ("documento_importante.txt", "Este es un documento importante de la empresa."),
        ("informe_financiero.xlsx", "Datos financieros del Q1 2025..."),
        ("base_clientes.csv", "nombre,email,telefono"),
        ("presentacion_ventas.pptx", "Diapositivas de ventas..."),
        ("backup_base_datos.sql", "CREATE TABLE usuarios..."),
    ]

    for nombre, contenido in archivos:
        ruta = os.path.join(DIRECTORIO_BLANCO, nombre)
        with open(ruta, "w") as f:
            f.write(contenido)
        print(f"    [+] Creado: {nombre}")

    print(f"\n[+] Simulando cifrado de {len(archivos)} archivos...")
    time.sleep(1)

    # Renombrar archivos (simular cifrado)
    for nombre, _ in archivos:
        original = os.path.join(DIRECTORIO_BLANCO, nombre)
        cifrado = original + EXTENSION_CIFRADO
        shutil.move(original, cifrado)
        print(f"    [!] Archivo cifrado: {nombre} -> {nombre}{EXTENSION_CIFRADO}")
        time.sleep(0.3)

    # Crear nota de rescate
    nota = f"""
================================================================
  ATENCION: Sus archivos han sido CIFRADOS
================================================================

Todos sus documentos, bases de datos y archivos importantes
han sido cifrados con AES-256.

Para recuperar sus datos, debe pagar un rescate de 0.5 BTC
a la siguiente direccion de Bitcoin:

  bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh

Instrucciones:
1. Compre 0.5 BTC en un exchange.
2. Envie los Bitcoins a la direccion indicada.
3. Envie un correo a rescate@recuperacion-datos.com con su ID.
4. Recibira la clave de descifrado en 24-48 horas.

NO intente descifrar los archivos usted mismo.
NO contacte a la policia.
Cualquier intento de recuperacion sin nuestra clave
resultara en la destruccion permanente de sus datos.

Tu ID unico: SIM-{hash(str(time.time()))[:8].upper()}
================================================================
"""
    ruta_nota = os.path.join(DIRECTORIO_BLANCO, NOMBRE_NOTA)
    with open(ruta_nota, "w") as f:
        f.write(nota)

    print(f"\n[+] Nota de rescate creada: {NOMBRE_NOTA}")
    print(f"\n[+] Simulacion completada. {len(archivos)} archivos 'cifrados'.")

    # Mostrar resumen
    print(f"\n[+] Resumen de archivos en {DIRECTORIO_BLANCO}:")
    for archivo in Path(DIRECTORIO_BLANCO).iterdir():
        print(f"    {'[CIFRADO]' if archivo.suffix == EXTENSION_CIFRADO else '[NOTA]'}   {archivo.name}")

if __name__ == "__main__":
    print("""
    ================================================
    SIMULACION DE RANSOMWARE - SOLO LABORATORIO
    ================================================
    """)
    simular_cifrado()
```

**Paso 2: Ejecutar la simulacion**

```powershell
# Crear y ejecutar en una VM aislada (Windows Sandbox o VM)
python simular_ransomware.py
```

**Paso 3: Detectar la simulacion**

Usar Sysmon y Process Monitor para detectar la actividad:

```powershell
# Ver procesos sospechosos (simular rename masivo)
Get-Process | Where-Object {$_.ProcessName -like "*python*"}

# Ver cambios de extension de archivos
Get-ChildItem -Path C:\Laboratorio_Ransomware -Recurse -Filter *.encrypted

# Ver conexiones de red (ninguna en este caso, pero practicar)
netstat -anob | findstr ESTABLISHED

# Ver eventos de Sysmon (ID 11 = FileCreate, ID 23 = FileDelete)
Get-WinEvent -FilterHashtable @{LogName='Microsoft-Windows-Sysmon/Operational'; ID=11,23} | Select-Object TimeCreated, Message -First 10
```

**Paso 4: Contener la simulacion**

```powershell
# SIMULAR contencion:
# 1. Aislar el equipo (en simulacion, detener el proceso)
Stop-Process -Name python -Force

# 2. Verificar que no hay mas procesos sospechosos
Get-Process | Where-Object {$_.CPU -gt 50 -and $_.StartTime -gt (Get-Date).AddMinutes(-10)}

# 3. Bloquear IPs (si hubiera C2 real, no aplica en simulacion)
# New-NetFirewallRule -DisplayName "Bloquear C2" -Direction Outbound -RemoteAddress 185.234.72.18 -Action Block

# 4. Tomar nota de los IOCs
Write-Host "Indicadores de Compromiso (IOCs):" -ForegroundColor Yellow
Write-Host "  Extension de archivos: .encrypted"
Write-Host "  Nombre de nota: README_RESCATE.txt"
Write-Host "  Proceso: python.exe (simulacion)"
```

---

### 15. Ejercicio 3 - Crear playbook de respuesta a ransomware

**Enunciado:** Escribir un playbook paso a paso para respuesta a ransomware, con comandos especificos para cada fase.

**Solucion - Playbook de 20 pasos:**

```yaml
# ============================================
# PLAYBOOK DE RESPUESTA A RANSOMWARE
# ============================================
# Version: 1.0
# Aplica a: Entorno Windows con Active Directory
# ============================================

# FASE 1: DETECCION Y NOTIFICACION (Pasos 1-5)

PASO 1: Recibir alerta
  Fuentes: EDR, SIEM, usuario reporta archivos no abren
  Accion: Confirmar sintomas
  Comandos:
    Get-ChildItem -Path \\servidor\compartido -Recurse -Filter *.lockbit
    Get-ChildItem -Path C:\ -Recurse -Filter *README*.txt -ErrorAction SilentlyContinue

PASO 2: Activar equipo de respuesta
  Accion: Notificar a IR, TI, legal, direccion
  Canal: Teams/Slack canal #incidentes + llamada telefonica
  Mensaje: "INCIDENTE ACTIVO - Ransomware detectado en [EQUIPO]"

PASO 3: Recolectar evidencia inicial
  Comandos:
    # Capturar procesos en ejecucion
    Get-Process | Export-Csv C:\evidencia\procesos.csv
    # Capturar conexiones de red
    netstat -anob > C:\evidencia\conexiones.txt
    # Capturar tareas programadas
    schtasks /query /fo CSV > C:\evidencia\tareas.csv
    # Capturar servicios
    Get-Service | Export-Csv C:\evidencia\servicios.csv

PASO 4: Determinar alcance
  Accion: Verificar que equipos estan afectados
  Comandos:
    # Buscar archivos cifrados en toda la red
    Get-ChildItem -Path \\* -Recurse -Filter *.lockbit -ErrorAction SilentlyContinue
    # Verificar conexiones activas al C2 desde firewalls
    # (revisar logs de firewall/proxy para IPs sospechosas)

PASO 5: Documentar todo
  Accion: Registrar hora de deteccion, equipos afectados, IOCs
  Herramienta: Ticket de incidente (ServiceNow, Jira, o documento compartido)

# FASE 2: CONTENCION (Pasos 6-10)

PASO 6: Aislar equipos infectados
  Accion: Desconectar cable de red del equipo
  Comando fisico: Desconectar RJ45
  O comando de red:
    # Deshabilitar adaptador de red
    Disable-NetAdapter -Name "Ethernet" -Confirm:$false

PASO 7: Bloquear C2 en firewall
  Accion: Agregar regla de bloqueo para IPs y dominios del C2
  Comandos:
    New-NetFirewallRule -DisplayName "BLOCK C2 RANSOMWARE" `
      -Direction Outbound -RemoteAddress 185.234.72.18 -Action Block
    # Si hay proxy, bloquear dominio en proxy

PASO 8: Detener propagacion
  Accion: Bloquear SMB entre VLANs
  Comandos:
    # Bloquear puerto 445 en firewall de servidores
    New-NetFirewallRule -DisplayName "BLOCK SMB RANSOMWARE" `
      -Direction Inbound -LocalPort 445 -Action Block -Profile Any

PASO 9: Deshabilitar cuentas comprometidas
  Accion: Cambiar contrasenas y forzar cierre de sesion
  Comandos:
    # Forzar cambio de contrasena en proximo inicio
    Set-ADUser -Identity usuario_afectado -ChangePasswordAtLogon $true
    # Revocar sesiones activas
    Get-ADUser -Identity usuario_afectado | Revoke-ADAuthentication

PASO 10: Preservar evidencia (NO APAGAR)
  Accion: NO apagar el equipo afectado
  Accion: Hacer imagen de disco si es posible
  Comando:
    # Si se necesita apagar, capturar memoria primero
    # (requiere herramientas forenses como FTK Imager o DumpIt)

# FASE 3: ERRADICACION (Pasos 11-14)

PASO 11: Identificar vector de entrada
  Accion: Revisar logs para determinar como entro el atacante
  Fuentes: Logs de correo, logs de RDP, logs de VPN, logs de web
  Ejemplo:
    # Buscar correos con adjuntos maliciosos
    Search-Mailbox -Identity usuario_afectado -SearchQuery "attachment:*.docm OR attachment:*.xlsm"

PASO 12: Cerrar vector de entrada
  Accion: Parchear vulnerabilidad o bloquear metodo de entrada
  Ejemplos:
    - Bloquear macros de Office por GPO
    - Deshabilitar RDP expuesto
    - Parchear VPN vulnerable

PASO 13: Eliminar malware
  Accion: Reinstalar sistemas afectados desde cero
  Comando:
    # Formatear y reinstalar (no confiar en limpieza)
    # Usar MDT, SCCM, o imagen gold

PASO 14: Rotar todas las credenciales
  Accion: Cambiar contrasenas de dominio, servicios, aplicaciones
  Comandos:
    # Resetear contrasena de administrador de dominio
    $pass = ConvertTo-SecureString "NuevaPassSegura!2025" -AsPlainText -Force
    Set-ADAccountPassword -Identity "Administrador" -NewPassword $pass -Reset

# FASE 4: RECUPERACION (Pasos 15-17)

PASO 15: Verificar backups
  Accion: Confirmar que los backups NO estan infectados
  Comandos:
    # Buscar archivos cifrados en backups
    Get-ChildItem -Path \\backup-server\share -Recurse -Filter *.lockbit
    # Restaurar desde backup mas reciente y limpio

PASO 16: Restaurar datos
  Accion: Restaurar desde backup limpio
  Comando:
    # Ejemplo con robocopy
    robocopy \\backup-server\restore\ C:\datos\ /E /R:2 /W:5

PASO 17: Verificar integridad
  Accion: Probar que los datos restaurados funcionan
  Comandos:
    # Verificar que no hay archivos cifrados
    Get-ChildItem -Path C:\datos -Recurse -Filter *.lockbit | Measure-Object
    # Verificar que los archivos criticos existen
    Test-Path "C:\datos\base_datos\clientes.db"

# FASE 5: LECCIONES APRENDIDAS (Pasos 18-20)

PASO 18: Reunion post-mortem
  Accion: Reunir a todas las partes para analizar el incidente
  Preguntas clave:
    - Que fallo? Que permitio el acceso inicial?
    - Que funciono bien? Que contencion fue efectiva?
    - Que se podria haber hecho mejor?

PASO 19: Actualizar controles
  Accion: Implementar mejoras basadas en las lecciones aprendidas
  Ejemplos:
    - Activar MFA en todos los accesos remotos
    - Segmentar red (VLANs separadas para usuarios y servidores)
    - Implementar backup 3-2-1 con copia offline
    - Deshabilitar macros de Office por GPO

PASO 20: Reportar y capacitar
  Accion: Reportar a autoridades si aplica
  Accion: Capacitar a empleados sobre phishing
  Recursos:
    - INCIBE (Espana): https://www.incibe.es/
    - CCN-CERT: https://www.ccn-cert.cni.es/
    - Simulacion de phishing para empleados
```

---

### 16. Ejercicio 4 - Analisis de un caso real (estudio)

**Enunciado:** Dada la descripcion del ataque SolarWinds, analizar el vector de entrada, movimiento lateral, impacto y lecciones aprendidas.

**Contexto:** SolarWinds es una empresa que desarrolla Orion, una plataforma de monitoreo de redes utilizada por mas de 30,000 organizaciones, incluyendo agencias gubernamentales de EE.UU. y Fortune 500.

**El ataque:**

En diciembre de 2020 se descubrio que atacantes (atribuido a APT29/Cozy Bear, grupo ruso) habian comprometido el pipeline de compilacion de SolarWinds. Insertaron codigo malicioso en las actualizaciones de Orion (versiones 2019.4 a 2020.2.1) que se distribuyeron a los clientes como actualizaciones legitimas, firmadas digitalmente. El backdoor, llamado SUNBURST, permanecia inactivo por 14 dias para evitar deteccion, luego se comunicaba con C2 mediante trafico HTTP camuflado.

**SOLUCION - Analisis completo:**

**Vector de entrada:**
- Los atacantes comprometieron el servidor de compilacion (build server) de SolarWinds.
- Insertaron codigo malicioso en el codigo fuente de Orion antes de la compilacion.
- El backdoor se compilo junto con el producto legitimo y se firmo con el certificado digital de SolarWinds.
- Los clientes descargaron la actualidad infectada desde el sitio oficial de SolarWinds (ataque a la cadena de suministro).

**Tecnica usada:** Supply Chain Attack (A08: Software and Data Integrity Failures del OWASP Top 10). Los atacantes no atacaron directamente a los clientes finales, sino al proveedor de software.

**Movimiento lateral:**
- Una vez instalado en la red de la victima, SUNBURST esperaba 14 dias antes de activarse (para evitar deteccion en sandboxes).
- Se comunicaba con C2 usando dominios como `appsync-api.eu-west-1.avsvmcloud.com`, camuflado como trafico legitimo de API.
- Los atacantes usaban credenciales robadas y movimientos laterales para llegar a sistemas de alto valor.
- En el caso de Microsoft, los atacantes accedieron al codigo fuente de algunos productos (Azure, Exchange, Teams).

**Impacto:**
- 18,000 organizaciones descargaron la actualizacion infectada (aunque se cree que solo unos cientos fueron atacados activamente).
- Victimas incluyeron: gobierno de EE.UU. (Tesoro, Departamento de Estado, DHS, NIH, Pentagono), Microsoft, FireEye, Cisco, Intel, NVIDIA, VMware.
- FireEye (empresa de ciberseguridad) fue quien descubrio el ataque y lo hizo publico.
- Costo estimado: mas de 100 mil millones de dolares en respuesta y remediacion global.
- El ataque estuvo activo por 8-14 meses antes de ser descubierto.

**Lecciones aprendidas:**

1. **Confianza zero en la cadena de suministro:** No confiar automaticamente en actualizaciones de software, incluso si estan firmadas digitalmente. Verificar integridad mediante hash checksums y monitorear comportamiento post-instalacion.

2. **Seguridad del pipeline de CI/CD:** Proteger el servidor de compilacion con controles de acceso estrictos, MFA, auditoria, y segmentacion de red. Cualquier compromiso del pipeline afecta a todos los clientes.

3. **Deteccion de comportamiento, no solo de firmas:** SUNBURST uso codigo firmado y legitimo, por lo que los antivirus tradicionales no lo detectaron. Las soluciones EDR que basan deteccion en comportamiento (conexiones sospechosas, procesos inusuales) tienen mejor chance.

4. **Monitoreo de trafico DNS/HTTP saliente:** El backdoor usaba dominios que imitaban servicios cloud legitimos. Monitorear y analizar consultas DNS y trafico HTTP ayuda a detectar C2.

5. **Segmentacion de red:** Una vez dentro, los atacantes se movieron lateralmente. La segmentacion de red limita el movimiento lateral y reduce el impacto.

6. **Respuesta a incidentes sin informacion completa:** Durante meses no se supo el alcance real del ataque. Las organizaciones tuvieron que asumir que estaban comprometidas y actuar en consecuencia.

**Timeline del ataque:**

```
Sep 2019: Atacantes comprometen el build server de SolarWinds
Mar 2020: Primera version infectada de Orion distribuida
Jun 2020: FireEye (victima) recibe actualizacion infectada
Nov 2020: FireEye descubre la anomalia durante una investigacion interna
Dic 2020: FireEye revela publicamente el ataque
Ene 2021: Varias agencias de EE.UU. confirman compromiso
Abr 2021: SolarWinds publica actualizacion limpia
```

---

### 17. Ejercicio 5 - Configurar tunel SSH para acceso remoto seguro

**Enunciado:** Un cliente necesita acceder a una base de datos PostgreSQL en un servidor interno. Solo tiene acceso SSH al servidor bastion. Configurar un tunel SSH local y verificar la conexion.

**Escenario:**
- Cliente local: Windows/Linux con psql o pgAdmin.
- Servidor bastion: `bastion.empresa.com`, usuario `admin`, IP publica 203.0.113.10.
- Servidor BD interno: `bd-interna`, IP 10.0.1.50, PostgreSQL en puerto 5432.
- El servidor BD solo escucha en la red interna (10.0.1.0/24), no tiene IP publica.

**Solucion:**

**Paso 1: Verificar conectividad SSH al bastion**

```bash
# Probar que podemos conectarnos al bastion
ssh admin@bastion.empresa.com
```

Si la conexion falla, verificar: credenciales, clave SSH, que el puerto 22 esta abierto.

**Paso 2: Crear el tunel SSH local**

```bash
ssh -L 5432:10.0.1.50:5432 admin@bastion.empresa.com
```

Explicacion del comando:
- `-L`: indica que es un forward local (local port forwarding).
- `5432`: es el puerto en la maquina local donde escuchara el tunel.
- `10.0.1.50:5432`: es el destino final. Desde el bastion, el trafico se reenvia a la IP interna 10.0.1.50 puerto 5432.
- `admin@bastion.empresa.com`: es el servidor SSH intermedio.

El comando se queda ejecutandose en primer plano. Para mantenerlo en segundo plano:

```bash
ssh -L 5432:10.0.1.50:5432 -N -f admin@bastion.empresa.com
```

- `-N`: no ejecuta comando remoto, solo establece el tunel.
- `-f`: ejecuta en segundo plano (background).

**Paso 3: Verificar que el tunel esta funcionando**

```bash
# Verificar que el puerto local esta escuchando
netstat -an | findstr 5432
# Deberia mostrar: TCP 127.0.0.1:5432  LISTENING

# En Linux/macOS:
lsof -i :5432
```

**Paso 4: Conectarse a PostgreSQL a traves del tunel**

```bash
# Usando psql (cliente de linea de comandos de PostgreSQL)
psql -h localhost -p 5432 -U usuario_bd -d nombre_bd

# Cuando pida contrasena, ingresar la de PostgreSQL (no la SSH)
```

**Paso 5: Alternativa con pgAdmin (interfaz grafica)**

1. Abrir pgAdmin.
2. Crear nueva conexion (Add New Server).
3. En la pestana Connection:
   - Host name/address: `localhost`
   - Port: `5432`
   - Maintenance database: `nombre_bd`
   - Username: `usuario_bd`
4. Hacer clic en Save.

La conexion se realiza a traves del tunel SSH.

**Paso 6: Verificar la seguridad del tunel**

```bash
# Verificar que el trafico viaja cifrado (no se puede interceptar)
# En una terminal separada, mientras el tunel esta activo:
ssh -v -L 5432:10.0.1.50:5432 admin@bastion.empresa.com
# La salida verbose muestra: "Local forwarding listening on 127.0.0.1 port 5432"
```

**Paso 7: Cerrar el tunel**

```bash
# Encontrar el proceso SSH en segundo plano
Get-Process ssh  # Windows
# o
ps aux | grep ssh  # Linux/macOS

# Terminar el proceso
kill <PID>
# O si esta en primer plano: Ctrl+C
```

**Extension: Tunel SSH con configuracion persistente**

Para no tener que escribir el comando cada vez, agregar al archivo `~/.ssh/config`:

```
Host bastion
    HostName bastion.empresa.com
    User admin
    IdentityFile ~/.ssh/id_rsa

Host bd-tunel
    HostName bastion.empresa.com
    User admin
    IdentityFile ~/.ssh/id_rsa
    LocalForward 5432 10.0.1.50:5432
```

Luego conectar con:

```bash
ssh bd-tunel
```

---

### 18. Ejercicio 6 - Bridge network en Docker

**Enunciado:** Crear 2 contenedores en una red bridge personalizada, configurar comunicacion entre ellos por nombre de contenedor, probar conectividad, y luego aislar un contenedor en su propia red sin acceso externo.

**Solucion:**

**Paso 1: Crear la red bridge personalizada**

```bash
# Crear una red bridge personalizada
docker network create --driver bridge mi-red

# Verificar que se creo
docker network ls
```

**Paso 2: Crear dos contenedores conectados a la misma red**

```bash
# Contenedor 1: servidor web
docker run -d --name web-server --network mi-red nginx:alpine

# Contenedor 2: cliente para hacer pruebas
docker run -it --name cliente --network mi-red alpine sh
```

**Paso 3: Probar comunicacion por nombre de contenedor**

Dentro del contenedor `cliente` (que se abrio en modo interactivo):

```sh
# Hacer ping al contenedor web-server por nombre
ping web-server

# Probar conexion HTTP
wget -O- http://web-server:80

# Salida esperada:
# Connecting to web-server (web-server)...
# 200 OK
# <html>... (pagina de bienvenida de nginx)
```

La magia de Docker bridge personalizada: los contenedores pueden resolverse por nombre porque Docker tiene un DNS interno.

**Paso 4: Salir del contenedor y verificar desde el host**

```sh
# Dentro del contenedor alpine, salir
exit
```

```bash
# Desde el host, los contenedores no son accesibles por nombre
ping web-server  # NO funcionara (el DNS de Docker solo funciona dentro de la red)

# Para acceder al web-server desde el host, necesitamos publicar puertos
docker run -d --name web-server-published -p 8080:80 nginx:alpine
curl http://localhost:8080  # Funciona
```

**Paso 5: Aislar un contenedor en su propia red sin acceso externo**

```bash
# Crear una red interna (sin acceso a Internet)
docker network create --internal red-aislada

# Crear contenedor en la red aislada
docker run -d --name contenedor-aislado --network red-aislada alpine sleep 3600

# Ejecutar comando en el contenedor aislado
docker exec contenedor-aislado ping 8.8.8.8
# Esto fallara: la red es interna, no tiene salida a Internet
```

**Paso 6: Verificar el aislamiento de red**

```bash
# Ejecutar ping a Google desde el contenedor aislado (debe fallar)
docker exec contenedor-aislado ping 8.8.8.8

# Ejecutar ping a Google desde un contenedor normal (debe funcionar)
docker exec cliente ping 8.8.8.8
```

**Paso 7: Conectar un contenedor a multiples redes**

```bash
# Crear una segunda red
docker network create otra-red

# Conectar el contenedor web-server a ambas redes
docker network connect otra-red web-server

# Verificar las redes del contenedor
docker inspect web-server --format='{{json .NetworkSettings.Networks}}'
```

**Paso 8: Limpiar los recursos**

```bash
# Detener y eliminar contenedores
docker rm -f web-server cliente web-server-published contenedor-aislado

# Eliminar redes
docker network rm mi-red red-aislada otra-red
```

**Explicacion de conceptos:**

- **Red bridge por defecto:** Cuando no se especifica `--network`, Docker usa la red `bridge` por defecto. Los contenedores se comunican por IP pero NO por nombre de contenedor.
- **Red bridge personalizada:** Creada con `docker network create --driver bridge`. Los contenedores se comunican por nombre de contenedor (DNS automatico). Es la forma recomendada.
- **Red interna (`--internal`):** Los contenedores no tienen acceso al exterior (no pueden hacer peticiones a Internet). Solo se comunican entre ellos y con el host.
- **Multiples redes:** Un contenedor puede estar en varias redes simultaneamente, actuando como bridge entre ellas.

---

### 19. Preguntas y Respuestas

**P1: Cual es la diferencia entre VPN Site-to-Site y Remote Access?**

**Respuesta:** La VPN Site-to-Site conecta redes enteras entre si (oficina central con sucursal), no requiere intervencion del usuario, y todo el trafico entre las redes viaja cifrado. La VPN Remote Access conecta un usuario individual a la red corporativa desde una ubicacion remota, requiere un cliente VPN en el equipo del usuario, y solo el trafico del usuario va cifrado. Site-to-Site usa tipicamente IPsec o MPLS; Remote Access usa OpenVPN, WireGuard o IPsec IKEv2.

---

**P2: Que protocolo VPN es mas rapido y por que?**

**Respuesta:** WireGuard es el mas rapido por varias razones: (1) usa cifrado ChaCha20 que es mas eficiente que AES en CPUs sin aceleracion hardware, (2) tiene solo ~4,000 lineas de codigo (menos sobrecarga de procesamiento), (3) opera en el kernel de Linux (modo kernel, no espacio de usuario como OpenVPN), (4) maneja mejor la reconexion en cambios de red. En pruebas comparativas, WireGuard suele ser 2-3 veces mas rapido que OpenVPN y ligeramente mas rapido que IPsec.

---

**P3: Que es un tunel SSH inverso y para que sirve?**

**Respuesta:** Un tunel SSH inverso (remote forward) se crea con `ssh -R`. Hace que el servidor SSH escuche en un puerto y reenvie el trafico al cliente SSH. Sirve para exponer un servicio local (como un servidor web en desarrollo) a Internet sin abrir puertos en el firewall. Por ejemplo, un desarrollador puede compartir su servidor local en el puerto 3000 con un cliente usando: `ssh -R 8080:localhost:3000 usuario@servidor-publico`. El cliente accede a `http://servidor-publico:8080` y ve el servidor local del desarrollador.

---

**P4: Para que sirve el modo bridge en VirtualBox?**

**Respuesta:** El modo bridge en VirtualBox conecta la maquina virtual directamente a la red fisica del host. La VM obtiene una direccion IP del mismo rango que la LAN fisica (por DHCP del router de la red), como si fuera un dispositivo mas conectado al mismo switch. Esto permite que la VM sea accesible desde otros equipos de la red (y viceversa), lo que es util para laboratorios, simulaciones de redes reales, servidores de pruebas, y tests de conectividad. A diferencia del modo NAT (donde la VM esta detras de un router virtual), en modo bridge la VM es parte de la red real.

---

**P5: Cuales son las 3 senales tempranas de ransomware?**

**Respuesta:** Las 3 senales tempranas mas importantes son: (1) Procesos anomalos como PowerShell ejecutando scripts con `-EncodedCommand` o `Invoke-WebRequest` para descargar archivos; (2) Conexiones de red a IPs sospechosas o dominios recien registrados (posibles C2); (3) Intentos de desactivacion de antivirus/EDR, como comandos `net stop WinDefend` o `Set-MpPreference -DisableRealtimeMonitoring`. Otras senales incluyen archivos .exe en carpetas temporales y escaneo de red interno.

---

**P6: Por que NO se debe pagar el rescate en un ataque ransomware?**

**Respuesta:** Por varias razones: (1) No garantiza la recuperacion de datos: aproximadamente el 30% de las victimas que pagan no recuperan todos sus datos, y algunos atacantes simplemente desaparecen. (2) Financia el crimen: cada rescate pagado financia el desarrollo de nuevo malware y futuros ataques. (3) La victima queda marcada como "pagadora" y puede ser atacada nuevamente. (4) Es ilegal en algunas jurisdicciones (pagar a criminales puede violar leyes de financiacion al terrorismo). (5) Existe la alternativa de restaurar desde backups, que es mas confiable a largo plazo.

---

**P7: Que es el movimiento lateral en un ciberataque?**

**Respuesta:** El movimiento lateral es la fase del ataque en la que el atacante, habiendo comprometido un primer equipo, se propaga a otros sistemas dentro de la misma red. Tecnicas comunes: (1) PsExec para ejecutar comandos en equipos remotos, (2) WMI para ejecutar procesos, (3) RDP para acceso remoto, (4) SMB para copiar malware a recursos compartidos, (5) Pass-the-Hash para autenticarse sin conocer la contrasena, (6) Kerberos ticket attacks (Golden Ticket, Silver Ticket). El objetivo es llegar a sistemas de alto valor como controladores de dominio, servidores de bases de datos o servidores de backups.

---

**P8: Cual es la diferencia entre BEC y phishing tradicional?**

**Respuesta:** La diferencia principal es el objetivo y la sofisticacion. El phishing tradicional es masivo: se envian miles de correos genericos a usuarios aleatorios, suplantando bancos o servicios populares, buscando robar credenciales o instalar malware. El BEC (Business Email Compromise) es dirigido: el atacante investiga a la empresa, identifica al CEO, CFO o alguien con autoridad para transferencias, y suplanta a esa persona especifica en un correo personalizado. El BEC no siempre usa malware, se basa en ingenieria social pura. Mientras el phishing tradicional busca muchas victimas (cantidad), el BEC busca una victima de alto valor con una transaccion grande (calidad).

---

**P9: Que es la regla 3-2-1 de backups?**

**Respuesta:** Es una estrategia de respaldo de datos que indica: 3 copias de los datos (1 copia primaria + 2 backups), almacenadas en 2 tipos de medios diferentes (ej: un backup en disco local y otro en cinta o nube), con 1 copia fuera de linea (offline, desconectada de la red). La copia fuera de linea es crucial contra ransomware porque el ransomware no puede cifrar lo que no puede alcanzar. Ejemplo practico: los datos originales estan en el servidor (copia 1), un backup diario en un NAS local (copia 2, medio 1), un backup semanal en cinta guardada en caja fuerte (copia 3, medio 2, fuera de linea).

---

### Tarea Recomendada

1. **Configurar WireGuard** entre dos maquinas (pueden ser VMs en VirtualBox en modo bridge). Probar conectividad haciendo ping y transfiriendo archivos via SCP a traves de la VPN. Documentar los pasos y la configuracion.

2. **Crear un tunel SSH** para acceder a un servicio interno (puede ser una base de datos MySQL o PostgreSQL en Docker). Verificar la conexion usando un cliente local (MySQL Workbench, pgAdmin, DBeaver). Probar tambien el tunel SSH inverso para exponer un servicio local.

3. **Simular un ataque de ransomware** usando el script Python del Ejercicio 2 en una VM aislada. Practicar la deteccion (Sysmon, Process Monitor, netstat) y la contencion (aislar el equipo, detener procesos, bloquear IPs). Escribir un informe de 1 pagina documentando los IOCs encontrados.

4. **Crear un playbook de respuesta a incidentes** para ransomware adaptado a una PYME (50 empleados). Incluir: contactos de emergencia, pasos de deteccion, contencion, erradicacion, recuperacion. Personalizar los comandos para el entorno (Windows con Active Directory).

5. **Configurar una red bridge en Docker** con 3 contenedores (frontend web, API, base de datos) en redes separadas. El frontend solo debe comunicarse con la API, y la API solo con la base de datos. La base de datos no debe tener acceso a Internet.

6. **Investigar un caso real de ransomware** (LockBit, BlackCat, REvil, o WannaCry). Escribir un analisis de 2 paginas incluyendo: vector de entrada, movimiento lateral, dano causado, rescate pedido, y lecciones aprendidas.

7. **Leer el NIST SP 800-61 Rev. 2** (Computer Security Incident Handling Guide) y resumir las 4 fases del ciclo de vida de respuesta a incidentes segun NIST.
