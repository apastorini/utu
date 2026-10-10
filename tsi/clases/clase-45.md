# Clase 45: Auditoria de la Red Casera WiFi - Descubrimiento, Versiones y Analisis de Comunicaciones

**Numero de clase:** 34  
**Duracion:** 2 horas  
**Curso:** Seguridad de la Informacion

---

## Objetivos de Aprendizaje

- Comprender la arquitectura de una red casera WiFi y los estandares 802.11 (WiFi 4/5/6/7)
- Distinguir los algoritmos de cifrado y autenticacion WiFi (WEP, WPA, WPA2, WPA3) y por que cada uno es seguro o no
- Detectar la version de firmware del router y de los dispositivos conectados, y como buscar vulnerabilidades publicadas
- Descubrir todos los dispositivos de la red con tres enfoques: Windows, Kali Linux y aplicacion movil (Fing, WiFi Analyzer, Termux + nmap y PCAPdroid)
- Capturar y analizar comunicaciones con Wireshark, entendiendo que se puede y que no se puede ver (y por que)
- Aplicar tecnicas de intrusion en un entorno propio y controlado para entender la defensa
- Elaborar un informe de hallazgos con recomendaciones de endurecimiento

---

## Aviso Legal y Etico - Leer Antes de Practicar

Todas las practicas de esta clase se realizan **exclusivamente sobre la red WiFi propia o con autorizacion escrita del dueno**. Escanear, interceptar o intentar acceder a redes ajenas sin permiso es ilegal en Uruguay: la **Ley 20.327** (prevencion y represion de la ciberdelincuencia, 2024) tipifica el **acceso ilicito a datos informaticos** (Art. 297 BIS) y la **interceptacion ilicita** (Art. 297 TER) con 6 a 24 meses de prision, y la **Ley 18.331** protege los datos personales; en la mayoria de los paises rigen normas equivalentes. El objetivo es entender como se defiende una red, no como se ataca a terceros.

En clase se usara la **red WiFi del aula / del docente**, o en su defecto un punto de acceso propio configurado para la practica.

---

## Organizacion de la Sesion (2 horas)

| Actividad | Duracion |
|-----------|----------|
| Teoria: red casera, estandares WiFi y algoritmos de cifrado | 30 min |
| Practica A: Windows (descubrimiento y versiones) | 25 min |
| Practica B: Kali Linux en VM (escaneo, firmware, comunicaciones) | 35 min |
| Practica C: aplicacion movil (en paralelo con B, incluye Termux/PCAPdroid) | 20 min |
| Glosario, preguntas y cierre | 10 min |

---

## Contenido Detallado

### 1. Anatomia de una Red Casera (8 min)

```
   INTERNET
      |
   [ CABLE / FIBRA ]
      |
 +---------+        +--------------------------+
 |  MODEM  |<------>|  ROUTER / ONT WiFi       |
 +---------+        |  - WAN (llega del ISP)   |
                    |  - LAN (192.168.1.0/24)  |
                    |  - DHCP: asigna IPs       |
                    |  - DNS: resuelve nombres  |
                    |  - NAT: traduce IPs       |
                    |  - WiFi: 2.4 GHz / 5 GHz |
                    +--------------------------+
                       |        |         |
                    [PC]     [Celular]  [TV]
```

| Componente | Que es | Por que importa |
|------------|--------|-----------------|
| **Modem** | Traduce la senal del ISP (cable/fibra) a datos digitales | Si se filtra la clave WiFi desde el ISP, da igual el router |
| **Router** | Enruta paquetes entre la red local e Internet | Es el "cerebro" y el principal objetivo: quien lo controla, controla la red |
| **WAN / LAN** | WAN = lado de Internet, LAN = lado de la casa | Las practicas solo se hacen sobre la LAN propia |
| **DHCP** | Asigna IPs automaticamente a los dispositivos | Su tabla de concesiones es la **lista mas rapida de dispositivos** de la red |
| **DNS** | Traduce nombres a IPs (ej. google.com -> 142.250.x.x) | Un DNS mal configurado redirige tus consultas a un atacante |
| **NAT** | Oculta la red interna tras una unica IP publica | Por defecto bloquea conexiones entrantes: es la primera barrera |
| **MAC** | Direccion fisica unica de cada adaptador de red | Identifica el fabricante (OUI) pero **se puede falsificar** |
| **Direccion IP privada** | Rango 192.168.x.x, 10.x.x.x (no routeable en Internet) | Delata la topologia interna |

**Y el modem? Por que no lo ves en tu casa (caso Uruguay / Antel)**

El **modem** (modulador-demodulador) es la pieza que convierte la senal del medio de transporte (par de cobre telefonico, cable coaxial u optica) en Ethernet digital. En un diagrama ideal son dos equipos separados, pero **en la mayoria de los hogares esta adentro de la misma caja que hace de router y WiFi**, y por eso "no lo ves":

| Situacion | Que hardware hay | Donde esta el modem |
|-----------|------------------|---------------------|
| **Fibra optica (Antel FTTH)** | Una **ONT** (unidad de terminacion optica) con WiFi integrado | La ONT hace de modem optico + router. Antel la describe como "comunmente llamada modem o router" y puede operar en **modo puente** o **router WiFi** |
| **ADSL (linea telefonica)** | Modem-router Wifi de Antel | El modem ADSL esta integrado en esa misma caja; al pasar a fibra ese equipo lo retira el tecnico |
| **Cable (DOCSIS)** | Modem-router del proveedor | Integrado, salvo que el proveedor lo entregue aparte en modo puente |
| **Router propio (ej. uno comprado)** | Equipo del ISP (ONT/modem) **+** tu router | El modem sigue estando: es el equipo del proveedor, adelante del tuyo |

**Como comprobarlo en 30 segundos (practica de la Practica A):**

```powershell
# 1) IP de tu PC y su gateway (el gateway es la "puerta" hacia el ISP)
ipconfig | findstr /i "IPv4 Default Gateway"

# 2) Tu IP publica vista desde dentro (Windows: ir a un sitio tipo ifconfig.me
#    o usar PowerShell)
(Invoke-WebRequest -Uri "https://ifconfig.me" -UseBasicParsing).Content

# 3) Comparar: si la IP publica NO es la de tu equipo, hay al menos un
#    NAT adelante -> equipo del proveedor y/o CGNAT
```

- **IP privada en la WAN** (`192.168.x.x`, `10.x.x.x`) -> hay un equipo del ISP (ONT/modem en modo router) delante de ti: **doble NAT**.
- **`100.64.x.x`** -> estas tras un **CGNAT** (NAT compartido por el proveedor), que tambien impide recibir conexiones entrantes.
- **IP publica real en tu PC** -> el equipo del ISP esta en **modo puente** y tu router es el unico NAT: la configuracion mas limpia.

**Por que importa en seguridad:** con **doble NAT** algunas defensas del router propio quedan inutilizadas (port forwarding, DMZ, UPnP se resuelven en el equipo del ISP y no en el tuyo), y el equipo del proveedor es uno mas que hay que mantener actualizado. Si puedes, poner la ONT en **puente** y dejar el enrutamiento a cargo de tu router. *(Si el proveedor no lo permite, al menos desactiva el WiFi de la ONT para no tener dos redes y usa solo la de tu router.)*

### 2. Estandares WiFi 802.11 - Versiones y Velocidades (6 min)

El IEEE define WiFi bajo la norma **802.11**. Cada revision tiene letra, y el mercado las rebautizo con numeros (WiFi 4, WiFi 5, ...):

| Estandar | Nombre comercial | Frecuencia | Velocidad teorica max | Anio |
|----------|------------------|------------|----------------------|------|
| 802.11b | WiFi 1 | 2.4 GHz | 11 Mbps | 1999 |
| 802.11a | WiFi 2 | 5 GHz | 54 Mbps | 1999 |
| 802.11g | WiFi 3 | 2.4 GHz | 54 Mbps | 2003 |
| 802.11n | **WiFi 4** | 2.4 / 5 GHz | 600 Mbps | 2009 |
| 802.11ac | **WiFi 5** | 5 GHz | 6.9 Gbps | 2013 |
| 802.11ax | **WiFi 6 / 6E** | 2.4 / 5 / 6 GHz | 9.6 Gbps | 2020 |
| 802.11be | **WiFi 7** | 2.4 / 5 / 6 GHz | 46 Gbps | 2024 |

**Por que importa en seguridad:**
- **WiFi 4 (802.11n) y anteriores no soportan WPA3.** Si tu equipo solo hace 802.11n, estara condenado a WPA2.
- **WiFi 5/6/6E/7** si soportan WPA3, PMF (Protected Management Frames) y cifrado mas fuerte.
- **2.4 GHz** viaja mas lejos y atraviesa paredes, pero tiene solo **3 canales no solapados (1, 6, 11)** y mucha interferencia (microondas, Bluetooth). **5 GHz** tiene muchos mas canales y menos interferencia, pero menos alcance.
- Un **dispositivo viejo conectado a la red degrada la seguridad de TODA la red**: si el router acepta WPA2 por compatibilidad, todo el trafico baja al nivel WPA2.

### 3. Algoritmos de Cifrado y Autenticacion WiFi (8 min)

Este es el nucleo de la seguridad inalambrica. Cada "version" de seguridad WiFi combina **autenticacion** (como te identificas) + **cifrado** (como se protege el trafico):

| Seguridad | Autenticacion | Cifrado | Estado | Por que |
|-----------|---------------|---------|--------|---------|
| **WEP** (1999) | Clave estatica | **RC4** de 40/104 bits | **ROTO** - prohibido | Requiere solo ~40.000 paquetes para recuperar la clave. Se descifra en minutos con aircrack |
| **WPA** (2003) | PSK + **TKIP** (Michael MIC) | RC4 corregido | **ROTO** - legado | TKIP tenia un fallo estructural; es WEP con parches |
| **WPA2-Personal** (2004) | PSK + 4-way handshake | **AES-CCMP (128 bits)** | **VALIDO** | El estandar actual. Seguro si la clave es larga y aleatoria |
| **WPA2-Enterprise** | 802.1X (RADIUS) | AES-CCMP | **VALIDO** | Cada usuario tiene credencial propia. Para empresas |
| **WPA3-Personal** (2018) | **SAE** (Dragonfly) | **AES-GCMP 256** | **RECOMENDADO** | Protege la clave incluso si se captura el handshake |

**Conceptos clave y su por que:**

| Concepto | Que es | Por que importa |
|----------|--------|-----------------|
| **PSK** (Pre-Shared Key) | La clave WiFi que escribes en cada dispositivo | Es el unico secreto: si es debil, todo se cae |
| **PMK** | Clave maestra derivada del PSK con PBKDF2 (4096 iteraciones) | Frena la fuerza bruta: cada intento cuesta CPU |
| **Handshake de 4 vias** | Intercambio de 4 mensajes al conectar un cliente | Prueba que ambos saben el PSK **sin enviarlo** y negocia claves de sesion |
| **PTK / GTK** | Claves de sesion para ese cliente / para el grupo | Se renuevan; no se puede descifrar trafico viejo con una clave nueva |
| **PMKID** | Hash del PMK con la MAC del punto de acceso | **Vulnerabilidad:** se captura con 1 solo paquete, sin cliente conectado |
| **TKIP** | Protocolo de cifrado viejo (predecesor de AES) | Tiene fallos estructurales; hoy solo existe por compatibilidad |
| **AES-CCMP / GCMP** | Cifrado simetrico moderno (AES) | Estan auditados y no tienen ataques practicos conocidos |
| **WPS** (WiFi Protected Setup) | Conexion por PIN de 8 digitos o boton | **ROTO:** el PIN se fuerza en horas. **Debe desactivarse siempre** |
| **KRACK** (CVE-2017-13077) | Reenvio de mensajes del handshake de 4 vias | Muestra por que hay que parchear el firmware del router |
| **PMF / 802.11w** | Protege las tramas de gestion del WiFi | Detiene ataques de desautenticacion masivos. Requerido en WPA3 |
| **PMF desactivada** | Cualquiera puede mandar tramas "desconectate" | Un atacante desconecta usuarios repetidamente (ataque DoS) |

**Jerarquia de fortaleza de la clave WiFi:**

```
DEBIL (se fuerza en minutos)          FUERTE (inviable)
"12345678"  ->  rockyou.txt           "k7#mQ2$vLp9@Zr4x"  ->  10^30 combinaciones
"password"  ->  listas de 14M         Frase de 5 palabras aleatorias
"clave2026" ->  diccionarios          Combinar: 3 palabras + simbolos + digitos
```

**Regla practica:** una clave de **16+ caracteres con mayusculas, minusculas, digitos y simbolos** hace inviable el ataque de diccionario, incluso capturando el handshake completo. El algoritmo (AES) no es el eslabon debil: **la clave humana lo es**.

### 4. Como Funciona un Ataque de Diccionario a WPA2 (4 min - solo teoria)

Se explica para **entender la defensa**, no para aplicarlo en redes ajenas:

```
1. ESCUCHA PASIVA
   El atacante captura el handshake de 4 vias de un cliente al conectarse
        (aireplay-ng -0 fuerza la desconexion para forzar un handshake nuevo)

2. DERIVACION DE CLAVES (PBKDF2)
   El handshake NO contiene la clave. Contiene: PSK + MAC AP + MAC cliente + nonces
   -> se deriva el PMK con PBKDF2 (4096 iteraciones, lento a proposito)

3. PRUEBA DE CADA CANDIDATO
   Aircrack-ng prueba cada palabra del diccionario:
     candidato "12345678" -> PBKDF2 -> PMK -> comparar con el PMK del handshake
     Si coincide: "KEY FOUND!"
   14 millones de palabras (rockyou) en una GPU toman segundos

4. POR QUE FUNCIONA SOBRE CLAVES DEBILES
   La verificacion es OFFLINE: no hay bloqueo, no hay log, no se alerta a nadie.
   El atacante puede probar millones de veces sin ruido en la red.
```

**Defensas (y por que funcionan):**

| Defensa | Mecanismo |
|---------|-----------|
| Clave de 16+ caracteres | El diccionario no la contiene y el espacio de busqueda es inviable |
| **WPA3-SAE** | Sustituye el 4-way handshake por el intercambio Dragonfly: el handshake **no contiene material para atacar offline** (resistencia a diccionario) |
| Desactivar WPS | Corta el vector de PIN |
| PMF / 802.11w | Impide forzar el handshake desconectando usuarios |
| Aislar clientes (AP isolation) | Evita que un vecino comprometido ataque a otros |
| Actualizar firmware | Parchea KRACK y vulnerabilidades del handshake |

### 5. Firmware: Version, Actualizaciones y Vulnerabilidades (4 min)

**Que es el firmware?** El sistema operativo embebido del router, camara, TV o PLC. Es el software que corre en el dispositivo IoT.

**Por que es critico:**
- El firmware viejo tiene vulnerabilidades publicadas con exploits funcionando (CVE)
- Los routers con firmware desactualizado son el blanco #1 de botnets como **Mirai**
- Muchos fabricantes dejan de actualizar modelos a los 2-3 anos
- **Credenciales por defecto:** `admin/admin`, `admin/1234`, `admin/` son frecuentes y equivalentes a no tener clave

**Como se detecta la version (las 3 formas, ver Practicas):**

| Fuente | Que revela |
|--------|------------|
| Etiqueta fisica del router (abajo/atras) | Modelo, MAC, a veces version HW y clave WiFi default |
| Panel web del router (`http://192.168.1.1`) | **Firmware version**, uptime, interfaces, clientes |
| Escaneo con Nmap (`-sV`) | Version del servidor web embebido, banners |
| UPnP/SSDP (`gssdp-discover`, `upnpc`) | Modelo, fabricante, version de software de cada IoT |
| ARP + OUI | Fabricante a partir de los primeros 6 caracteres de la MAC |
| App movil (Fing, Router Scan) | Fabricante, modelo y a veces firmware |

**Como buscar vulnerabilidades del firmware:**
1. Identificar **fabricante + modelo + version exacta**
2. Buscar en **NVD** (https://nvd.nist.gov) `TP-Link WR841N firmware`
3. Buscar en **CVE Details** y **Exploit-DB**
4. Consultar **routerdefaultpasswords.com** para credenciales default
5. Revisar la pagina del fabricante para ver si hay firmware mas nuevo

**Checklist de endurecimiento del router (entregable de la clase):**

| Control | Estado |
|---------|--------|
| Firmware actualizado a la ultima version | ☐ |
| Clave WiFi WPA3 o WPA2 con AES (nunca WEP/WPA-TKIP) | ☐ |
| Clave WiFi de 16+ caracteres, aleatoria | ☐ |
| WPS desactivado | ☐ |
| Clave de administracion distinta a `admin/admin` | ☐ |
| Gestion remota (WAN) desactivada | ☐ |
| UPnP desactivado si no se necesita | ☐ |
| SSID sin datos personales (no "CasaDeJuanPerez") | ☐ |
| Red de invitados separada (guest network) | ☐ |
| DHCP con rango acotado y firewall activo | ☐ |

---

## Practica A: Desde Windows (25 min) - Sin Instalar Nada

**Objetivo:** descubrir la red, ver estandares WiFi y detectar versiones usando solo herramientas nativas.

**Paso 1: Ver la informacion de la conexion WiFi actual**

```powershell
netsh wlan show interfaces
```

**Salida esperada (campos relevantes):**

```
SSID                   : UTU-ALUMNOS
Estado                 : conectado
Modo de red            : infraestructura
Tipo de radio          : 802.11ac
Frecuencia             : 5 GHz
Autenticacion          : WPA2-Personal
Cifrado                : CCMP
BSSID                  : a4:2b:b0:11:22:33
Canal                  : 44
Senal                  : 78%
```

**Que interpretar:**
- `Tipo de radio 802.11ac` = **WiFi 5** -> soporta WPA3 si el router tambien lo hace
- `Autenticacion WPA2-Personal` = clave compartida (PSK)
- `Cifrado CCMP` = AES, correcto (si dijera "TKIP" o "WEP" hay que cambiar el router)
- `BSSID` = MAC del punto de acceso, sirve para cruzar con el escaneo posterior
- `Senal 78%` -> senal debil obliga a reintentos: la seguridad degrada con mala senal

**Paso 2: Version exacta del adaptador WiFi y sus capacidades**

```powershell
netsh wlan show drivers
```

Buscar las lineas:

```
Servicio de autoconfiguracion inalambrica : soportado
Tipo de proveedor          : Intel
Version de driver          : 22.240.0.6
Tipos de radio admitidos   : 802.11n 802.11ac 802.11ax
Autenticacion y cifrado soportados : WPA2-PSK, WPA3-SAE
PMF (marcos protegidos)    : Soportado
```

**Por que:** aqui ves **que soporta tu tarjeta**. Si `Tipos de radio admitidos` solo llega a `802.11n`, tu equipo no podra usar WiFi 6 ni WPA3 aunque el router si. La seguridad de la red es la del eslabon mas viejo.

Tambien, version del driver (para buscar CVEs del fabricante):

```powershell
Get-CimInstance Win32_PnPSignedDriver |
  Where-Object DeviceName -match "Wi-?Fi|Wireless|802.11" |
  Select-Object DeviceName, DriverVersion, DriverDate | Format-List
```

**Paso 3: Ver todas las redes visibles y su seguridad**

```powershell
netsh wlan show networks mode=bssid
```

**Salida esperada:**

```
SSID 1 : UTU-ALUMNOS
    Tipo de red             : Infraestructura
    Autenticacion           : WPA2-Personal
    Cifrado                 : CCMP
    Canal                    : 44
    Senal                    : 78%
    Radio                    : 802.11ac

SSID 2 : Vecino_2.4G
    Autenticacion           : WPA2-Personal
    Cifrado                 : TKIP      <-- inseguro, deberia ser CCMP
```

**Por que:** muestra la **postura de seguridad de toda la cuadra**. Detectas redes abiertas (`Abierta`/`Ninguna`), WEP (roto) o TKIP (deprecado). Es la forma mas rapida de auditar el entorno sin tocar nada.

**Paso 4: Descubrir los dispositivos de la red**

```powershell
# a) Ver la configuracion IP
ipconfig /all | findstr /i "IPv4 Subnet Gateway DHCP DNS"

# b) Ver vecinos ya conocidos
arp -a

# c) Hacer un barrido de la subred (ajustar 192.168.1.0 a tu red)
$red = "192.168.1"
1..254 | ForEach-Object {
  $ip = "$red.$_"
  if (Test-Connection -ComputerName $ip -Count 1 -Quiet -ErrorAction SilentlyContinue) {
    $ip
  }
} | Tee-Object -Variable activos

# d) Volver a leer la tabla ARP ahora que hay mas equipos
arp -a
```

**Por que:** el barrido con `Test-Connection` (ping) fuerza a cada equipo a responder, y la tabla **ARP** guarda sus IPs con sus MAC. Los 6 primeros octetos de la MAC son el **OUI** (registro IEEE) -> se buscan en https://standards-oui.ieee.org/ y te dan el fabricante (ej. `a4:2b:b0` = Apple, `28:d0:cb` = Huawei). Asi identificas "quien es" cada IP.

**Si algo se cae durante el barrido (guia de problemas):**

El barrido solo envia **254 ping ICMP de a uno por vez**: no puede apagar el WiFi ni ocultar el SSID de nadie. Aun asi, si la red propia desaparece:

1. `netsh wlan show networks` -> la red propia figura? Si no figura, **el punto de acceso dejo de emitir**.
2. Mirar el router: LED de power y LED WLAN. Los equipos Antel traen **boton WLAN/WIFI** (atras o al costado): un golpe accidental lo apaga.
3. Si el router no responde: **desconectarlo 10 segundos** y reconectar; tarda 60-90 seg en volver. Mientras tanto Windows puede conectarse solo a **otra red guardada** (pasa seguido: te quedas "con internet" pero en la red equivocada).
4. Verificar desde el celular si la red propia se ve desde otro equipo (descarta la placa WiFi de la PC).
5. Cuando vuelva: `netsh wlan connect name=<tu-SSID>` y `netsh wlan show interfaces` para confirmar. **No** borrar el perfil salvo que se quiera volver a escribir la clave.
6. **Hallazgo valido para el informe:** si la red cae de forma repetida al hacer el barrido, el equipo no resiste carga o su proteccion anti-DoS esta mal implementada: registrar fecha/hora y reproduccion.

**4b: Detectar el modem / equipo del ISP delante de ti (doble NAT o CGNAT)**

```powershell
# IP local y gateway (la "puerta" hacia el proveedor)
ipconfig | findstr /i "IPv4 Default Gateway"

# IP publica vista desde tu equipo
(Invoke-WebRequest -Uri "https://ifconfig.me" -UseBasicParsing).Content
```

**Como se interpreta:** si la IP publica **coincide** con la de tu equipo, no hay NAT adelante (el equipo del ISP esta en puente). Si **no coincide**, hay un NAT entre tu PC y Internet: fijate si la WAN de tu router es `192.168.x.x` (equipo del ISP en modo router -> doble NAT) o `100.64.x.x` (CGNAT del proveedor). Ver detalle en el bloque "Y el modem?" de la seccion 1.

**Paso 5: Historial y version de firmware del router**

```powershell
netsh wlan show wlanreport
```

Esto genera un reporte HTML en:
`C:\ProgramData\Microsoft\Windows\WLANReport\wlan-report-latest.html`

Abrirlo en el navegador. Contiene: eventos de conexion/desconexion, autenticaciones fallidas, cambios de red, version de la tarjeta y del driver.

Para el **firmware del router**, abrir el panel de administracion:
1. Ver el Gateway con `ipconfig` (ej. `192.168.1.1`)
2. Abrir `http://192.168.1.1` en el navegador
3. Login (etiqueta del equipo o credenciales default -> ver checklist)
4. Buscar **System Information / Diagnostics / Firmware Version**

**Por que:** es la unica fuente oficial de la version exacta. Si no hay actualizaciones en la pagina del fabricante para tu modelo, **el router es EOL (fin de vida)** y hay que reemplazarlo.

**Paso 6: Capturar y ver las propias comunicaciones con Wireshark**

1. Instalar Wireshark: https://www.wireshark.org/download.html
2. Elegir la interfaz **Wi-Fi** y dar a Capture (la de mayor trafico)
3. Aplicar filtros:

| Filtro | Que muestra |
|--------|-------------|
| `dns` | Todas las consultas de nombres: que sitios visitan los dispositivos |
| `http` | Peticiones en claro (se ven las URLs, logins, cookies) |
| `tls.handshake.type == 1` | Solo el SNI del TLS: que dominio se pide, aunque este cifrado |
| `ip.addr == 192.168.1.1` | Todo el trafico hacia/desde el router |
| `wlan.fc.type_subtype == 0x0c` | Tramas de desautenticacion (posible ataque). En Windows casi nunca aparecen: capturar tramas de gestion exige modo monitor, que solo esta en la Practica B |
| `arp` | Resoluciones IP->MAC (posible ARP spoofing) |

**Ejemplo practico en vivo:** abrir `http://neverssl.com` y ver en Wireshark la peticion completa con la URL y los headers. Luego abrir `https://ejemplo.com` y comprobar que **solo se ve la IP y el nombre del dominio (SNI), pero no el contenido**.

**Por que:** esta es la leccion central. **HTTPS cifra el contenido pero no el trafico de metadatos.** Un vecino con modo monitor puede ver a que dominios te conectas, cuando y cuanto trafico genera, pero no el texto. Por eso se despliega **DoH/DoT** (DNS over HTTPS/TLS) y **VPNs**: para proteger tambien los metadatos.

**Paso 7: Informe de configuracion actual (entregable)**

Exportar la postura de seguridad:

```powershell
$out = "$env:USERPROFILE\Desktop\auditoria-wifi"
New-Item -ItemType Directory $out -Force | Out-Null
netsh wlan show interfaces   | Out-File "$out\conexion-actual.txt"
netsh wlan show networks     | Out-File "$out\redes-visibles.txt"
netsh wlan show drivers      | Out-File "$out\adaptador.txt"
ipconfig /all                | Out-File "$out\ipconfig.txt"
arp -a                       | Out-File "$out\arp.txt"
netsh wlan show wlanreport   | Out-File "$out\reporte-ruta.txt"
Get-Content "$out\reporte-ruta.txt" | Select-String "wlan-report"
notepad "$out\redes-visibles.txt"
```

---

## Practica B: Desde Kali Linux en VM (35 min)

**Objetivo:** escaneo profundo, fingerprinting de firmware y captura/analisis de comunicaciones.

**Pre-requisito - configurar la VM:**

1. En VirtualBox: VM > Configurar > **Red > Conectar en: Adaptador puente (Bridged)**  
   **Por que:** con NAT la VM queda atras de una capa de traduccion y **no ve los demas equipos de la red casera**. Con puente obtiene IP propia en la LAN y puede escanear de igual a igual.
2. Iniciar Kali y verificar conectividad:

```bash
ip a
ping -c 3 192.168.1.1
```

> **Nota sobre el modo monitor:** la tarjeta WiFi virtual de la VM **NO** soporta modo monitor ni desautenticacion. Para la parte de captura WiFi hacen falta dos cosas: (a) una **USB WiFi compatible** (Atheros AR9271, Alfa AWUS036ACH) conectada a la PC y (b) en VirtualBox: **Dispositivos > USB > marcar la interfaz WiFi** para que la VM la tome. Sin eso, las practicas de red cableada (nmap, Wireshark en eth0) funcionan igual.

**Paso 1: Descubrimiento de dispositivos de la red**

```bash
# a) Descubrimiento por ping sweep + tabla ARP
sudo apt install -y nmap
nmap -sn 192.168.1.0/24

# b) Escaneo ARP explicito (mas confiable que ICMP en LAN)
nmap -sn -PR 192.168.1.0/24

# c) Identificar fabricante por OUI
for ip in $(nmap -sn -PR 192.168.1.0/24 | grep -oP '(?<=Nmap scan report for )\d+\.\d+\.\d+\.\d+'); do
  mac=$(arp -n $ip | grep -oP '([0-9a-f]{2}:){5}[0-9a-f]{2}')
  echo "$ip -> $mac"
done
```

**Por que `-sn -PR`:** en una red local la mayoria de equipos **no responde a ping** (firewall de Windows), pero **todos responden a ARP** al ser una capa 2. Es el descubrimiento mas fiable en LAN. Con `-sn` no se abren puertos: solo se descubre (mas rapido y menos ruidoso).

**Paso 2: Deteccion de versiones y servicios (fingerprinting)**

```bash
# Versiones de SO y servicios de todos los equipos
sudo nmap -sV -O 192.168.1.0/24 -oN escaneo-versiones.txt

# Del router: que version de servidor web embebido corre
sudo nmap -sV -p 80,443,8080,23 --script=http-headers,http-title 192.168.1.1

# Banners de servicios
sudo nmap -sV --version-all -p- 192.168.1.1
```

**Salida esperada (orientativa):**

```
PORT    STATE SERVICE VERSION
80/tcp  open  http    GoAhead httpd  (firmware 1.0.0 build 2019)
443/tcp open  ssl/http GoAhead httpd
23/tcp  open  telnet  BusyBox telnetd  <-- peligroso: telnet abierto
```

**Por que:** `-sV` lanza probes y **compara la respuesta con una base de datos de firmas** para deducir el software y su version exacta. Esa version se busca despues en NVD/Exploit-DB. Un `telnetd` o un servidor web de 2019 en un router es una **bandera roja**: probablemente con CVEs publicados.

**Paso 3: Version de firmware de los dispositivos IoT por UPnP/SSDP**

```bash
sudo apt install -y gssdp-tools miniupnpc

# Descubrir dispositivos UPnP en la red
gssdp-discover --timeout=5

# Alternativa con netcat (M-SEARCH por UDP: SSDP viaja en UDP 1900, no en TCP,
# por eso no sirve un curl comun aqui)
printf 'M-SEARCH * HTTP/1.1\r\nHOST: 239.255.255.250:1900\r\nMAN: "ssdp:discover"\r\nMX: 3\r\nST: ssdp:all\r\n\r\n' \
  | nc -u -w 3 239.255.255.250 1900 > respuestas.txt
cat respuestas.txt

# Obtener el descripcion.xml (modelo, fabricante, version)
curl -s http://192.168.1.1:5000/rootDesc.xml | grep -iE "modelName|softwareVersion|UDN"
```

**Salida esperada (orientativa):**

```
LOCATION: http://192.168.1.10:5000/rootDesc.xml
ST: urn:schemas-upnp-org:device:InternetGatewayDevice:1

<modelName>Android TV</modelName>
<softwareVersion>1.4.5</softwareVersion>
<UDN>uuid:xxxxxxxx-xxxx-...</UDN>
```

**Por que:** UPnP anuncia automaticamente en la LAN el **modelo y la version de software** de smart TVs, camaras, consolas y PLCs. Es informacion valiosa para el atacante... y para el auditor, que asi puede cruzarla con CVE. **Defensa:** desactivar UPnP si no se necesita (ver checklist).

**Paso 4: Captura de comunicaciones con Wireshark (cableada)**

```bash
# Listar interfaces
ip a

# Capturar con tshark (CLI) o wireshark (GUI)
sudo tshark -i eth0 -w captura-red.pcap -c 2000

# Analizar despues
tshark -r captura-red.pcap -Y "dns" -T fields -e ip.dst -e dns.qry.name | head -30
tshark -r captura-red.pcap -Y "http.request.method == POST" -V | head -60
```

**Filtros utiles en la GUI (`wireshark captura-red.pcap`):**

| Filtro | Utilidad |
|--------|----------|
| `dns.qry.name` | Todos los dominios resueltos (perfil de navegacion) |
| `http.request.uri` | URLs completas en claro |
| `http contains "password"` | Busqueda de credenciales en claro |
| `tls.handshake.extensions_server_name` | Dominios visitados via HTTPS (SNI) |
| `arp && arp.opcode == 2` | Respuestas ARP -> posible ARP spoofing |
| `icmp` | Pings: posible descubrimiento o tunelizacion |

**Paso 5 (avanzado): Analisis WiFi con modo monitor**

*Requiere USB WiFi compatible y autorizacion sobre la red propia.*

```bash
sudo apt install -y aircrack-ng

# Verificar que la tarjeta soporta modo monitor
sudo airmon-ng

# Matar procesos que interfieren y activar modo monitor
sudo airmon-ng check kill
sudo airmon-ng start wlan0      # crea wlan0mon

# 1) Escanear: ver APs, canales, cifrado y clientes
sudo airodump-ng wlan0mon

# 2) Capturar SOLO de tu red (BSSID y canal del paso anterior)
sudo airodump-ng -c 6 --bssid AA:BB:CC:DD:EE:FF -w captura wlan0mon

# 3) (sobre tu propio AP con clientes de prueba) forzar handshake
sudo aireplay-ng -0 5 -a AA:BB:CC:DD:EE:FF wlan0mon

# 4) Probar el diccionario rockyou contra TU captura
sudo aircrack-ng -w /usr/share/wordlists/rockyou.txt captura-01.cap
```

**Como interpretar la salida de `airodump-ng`:**

```
BSSID              CH  CURVE  ENC      CIPHER  AUTH    ESSID
AA:BB:CC:DD:EE:FF  6   54e    WPA2     CCMP    PSK     UTU-ALUMNOS   <-- seguro
11:22:33:44:55:66  1   54e    WPA      TKIP    PSK     Vecino        <-- inseguro
99:88:77:66:55:44  11  54e    WEP      WEP     OPN     Abierta       <-- roto
```

**Por que es pedagogico:** el alumno ve **en vivo** la diferencia entre WEP, WPA-TKIP y WPA2-CCMP, y comprueba con `aircrack` que una clave debil cae mientras una fuerte no. Entiende asi, de forma practica, que **la debilidad no esta en AES sino en la clave**.

**Si no hay USB WiFi compatible:** limitarse a las practicas de red cableada (Pasos 1-4). Son las que se aplican en auditorias reales de red casera.

**Paso 6: Buscar vulnerabilidades del firmware detectado**

```bash
searchsploit TP-Link WR841N
searchsploit GoAhead httpd

# Consulta rapida a NVD
curl -s "https://services.nvd.nist.gov/rest/json/cves/2.0?keywordSearch=GoAhead%20httpd" \
  | python3 -c "import sys,json; d=json.load(sys.stdin); [print(v['cve']['id'], v['cve']['descriptions'][0]['value'][:100]) for v in d['vulnerabilities'][:5]]"
```

**Por que:** conectar el hallazgo tecnico (`GoAhead httpd 1.0.0`) con la base de datos de vulnerabilidades es lo que transforma un escaneo en una **auditoria**. Sin ese paso, solo tienes puertos abiertos sin contexto de riesgo.

**Paso 7: ARP spoofing - demostracion defensiva (solo red propia)**

```bash
# Detectar si alguien en tu red hace ARP spoofing
sudo apt install -y arping
arping -c 3 192.168.1.1        # verifica que la MAC del gateway no cambie

# Verificar en Wireshark el filtro:
# arp.opcode == 2 && eth.src != <mac_real_router>
```

**Por que se explica:** si un atacante en la LAN envia respuestas ARP falsas ("yo soy 192.168.1.1"), el trafico de la victima pasa por su equipo (**Man-in-the-Middle**). **Defensas:** ARP estatico, cambio de MAC, 802.1X, red segmentada y cifrado de extremo a extremo (HTTPS) que hace inutil el trafico interceptado.

---

## Practica C: Desde una Aplicacion Movil (20 min)

**Objetivo:** hacer lo mismo con el celular, entendiendo que cada plataforma tiene limitaciones distintas. Se puede hacer **en paralelo** con la Practica B.

**Requisito:** conectar el telefono a la **misma red WiFi** de la practica (o usar los datos moviles para escanear, aunque asi solo veras el celular).

**Paso 1: Fing - descubrimiento de dispositivos (Android/iOS)**

1. Instalar **Fing** (gratuita) desde Play Store / App Store
2. Abrirla y dar permiso de ubicacion (necesario para leer la red WiFi)
3. Esperar el escaneo automatico

**Salida esperada:**

```
192.168.1.1   Router       TP-Link    A4:2B:B0:...   Gateway
192.168.1.23  iPhone       Apple      A4:83:E7:...   Mi celular
192.168.1.44  Unknown      Espressif  28:60:46:...   <-- dispositivo IoT
192.168.1.51  Smart TV     Samsung    5C:CB:99:...   Activo hace 5 min
```

**Que aporta Fing que Windows no:**
- Identifica **modelo y fabricante** por OUI automaticamente (sin buscar en IEEE)
- Historial de dispositivos: avisa cuando aparece uno **nuevo en la red** (deteccion de intrusos)
- Escaneo de puertos basicos del objetivo
- Test de velocidad y calidad del WiFi

**Por que es una buena herramienta para el usuario final:** hace en 10 segundos lo que en Windows tomaba 5 comandos. Su limite: no detecta firmware, no hace fingerprinting de servicios ni captura de trafico.

**Paso 2: WiFi Analyzer - canales, estandares y senal (Android)**

1. Instalar **WiFi Analyzer** (de farproc, open source) o **Ampere Wifi Analyzer**
2. Conceder permisos de ubicacion
3. Ver la pestana **Canales** / **Vista grafica**

**Que mirar:**

| Indicador | Que significa | Accion |
|-----------|---------------|--------|
| Senal en dBm | -30 a -60 = excelente; -70 = limite; -80 = inestable | Acercar el router o agregar repetidor/malla |
| Canal congesto | Muchas redes en el canal 6 | Cambiar a canal 1 o 11 (2.4 GHz) |
| Banda | 2.4 GHz vs 5 GHz | Usar 5 GHz cerca, 2.4 GHz lejos |
| Estandar reportado | "11n", "11ac", "11ax" | Confirma WiFi 4/5/6 real, no el del rotulo |

**Por que:** el **canal es el recurso compartido**. En 2.4 GHz solo hay 3 canales sin solaparse (1, 6, 11) y en barrios densos todos usan el 6: eso genera colisiones y reintentos, baja el rendimiento y, sobre todo, **las tramas de gestion viajan en claro y se capturan mas facil** en un entorno saturado.

**Paso 3: Router Scan / acceso al panel web desde el celular**

1. Abrir el navegador y acceder a `http://192.168.1.1` (o `192.168.0.1`, `10.0.0.1`)
2. Login con credenciales de la etiqueta o las que se cambiaron
3. Navegar a **System / Firmware / Status**

**Por que desde el celular tambien:** el panel web es un servicio HTTP interno, no depende del SO. La misma autenticacion, el mismo firmware, la misma pantalla. Es la forma mas directa de obtener la **version exacta** en cualquier dispositivo.

**Paso 4: Ingenieria social inversa - verificar credenciales default**

Con el modelo del router (etiqueta o panel), buscar en:
- `https://routerdefaultpasswords.com/`
- `https://www.routerpasswords.com/`

**Solo sobre tu propio router**, para comprobar si sigue con `admin/admin`. Si es asi, cambiarla es **prioridad 1** del checklist.

**Paso 5: Herramientas de seguridad en Android (Termux + PCAPdroid)**

Apps como Fing resuelven el inventario, pero **si se puede instalar un entorno de escaneo real en el celular**, sin root y sin pagar nada. Se prueba lo mismo que en las otras plataformas, con limites que despues se explican.

**5a. Termux: terminal de Linux en Android (escaneo de red)**

1. Instalar **Termux** desde **F-Droid** (la version de Play Store esta desactualizada): https://f-droid.org/packages/com.termux/
2. Actualizar e instalar herramientas:

```bash
pkg update && pkg upgrade -y
pkg install nmap netcat-openbsd curl iputils -y

# a) El celular como parte de la red: SSID y BSSID al que esta conectado
ip addr show wlan0

# b) Descubrir la misma red casera que en las otras practicas
nmap -sn 192.168.1.0/24

# c) Version de servicios del router (mismo objetivo que en Kali)
nmap -sT -p 80,443,23,8080 192.168.1.1

# d) Cabeceras del panel del router
curl -sI http://192.168.1.1 | head -15
```

**Por que `-sT` y no `-sS`:** el escaneo SYN (`-sS`) necesita privilegios sobre el socket crudo y **Android no los da a una app comun**; `-sT` abre y cierra la conexion de forma normal. Da el mismo resultado de puertos abiertos, solo que es mas ruidoso.

**5b. PCAPdroid: capturar trafico sin root (equivalente del Wireshark movil)**

1. Instalar **PCAPdroid** (open source, F-Droid o Play Store): https://f-droid.org/packages/com.emanuelef.remote_capture/
2. Aceptar el permiso (crea una **VPN local**: no sale a Internet, todo se procesa en el equipo)
3. Elegir en *dump mode* **PCAP file** y dar **Start**
4. Navegar un rato, **Stop**, y buscar el archivo en `Download/PCAPdroid/`
5. Pasarlo a la PC (`adb`, carpeta compartida o correo a uno mismo) y abrirlo en **Wireshark**: los filtros de la Practica A (`dns`, `http.request`, `tls.handshake.extensions_server_name`) funcionan igual

**Por que funciona sin root:** Android exige que todo trafico pase por una **VPN local** (API `VpnService`) para que una app pueda verlo. Eso tiene dos limites importantes: (1) **solo ve el trafico saliente del propio celular**, nunca el de los demas dispositivos de la red (eso exige modo monitor, que es cosa de Kali); (2) en modo no-root **solo se capturan conexiones iniciadas por el telefono**, no las entrantes.

**5c. Si se quiere todo el arsenal: Kali NetHunter**

**Kali NetHunter** es Kali Linux corriendo en Android: la version **Rootless** corre en Termux con un chroot de Kali (trabaja sin root, mismo alcance que los puntos anteriores); la version **rooted** da ademas captura en **modo monitor** y ataques de capa 8, pero exige un dispositivo compatible con root y/o un adaptador WiFi USB con chip soportado (Alfa Atheros/Realtek) conectado por OTG. Es el mismo limite de siempre: **el chip WiFi del telefono esta disenado para modo managed**.

**Que se puede probar igual en las 3 plataformas y que no:** el cuadro comparativo completo (Windows / Kali / Android) esta en el Paso 6.

**Paso 6: Limitaciones del celular (por que no reemplaza a Kali)**

| Capacidad | Windows | Kali Linux | Celular |
|-----------|---------|------------|---------|
| Ver la red y estandares | ✅ `netsh` | ✅ `iw`, `nmcli` | ✅ Fing / WiFi Analyzer |
| Descubrir dispositivos | ✅ ping + arp | ✅ nmap completo | ⚠️ Fing, o `nmap` con Termux |
| Version de firmware | ✅ panel web | ✅ nmap -sV + UPnP | ⚠️ panel web + `nmap -sT` (sin banner completo) |
| Escaneo de puertos profundo | ⚠️ con nmap instalado | ✅ nativo | ⚠️ con Termux + `nmap -sT` |
| Captura de paquetes | ✅ Wireshark | ✅ Wireshark / tshark | ⚠️ PCAPdroid (solo el trafico propio) |
| Terminal de Linux | ⚠️ WSL opcional | ✅ | ⚠️ Termux (sin privilegios) |
| Modo monitor WiFi | ❌ | ⚠️ con USB WiFi | ❌ (requiere root + chip compatible) |
| Analisis de firmware/CVE | ⚠️ manual | ✅ searchsploit / NVD API | ⚠️ NVD con `curl` (sin searchsploit) |
| Movilidad / rapidez | ❌ | ❌ | ✅ escaneo en 10 seg |

**Por que estas diferencias:** Windows y Kali corren en un SO completo con acceso directo a la tarjeta de red. El celular tiene un **sandbox**: Android restringe el acceso de bajo nivel a las apps (a partir de Android 10 ni siquiera se puede leer el MAC real), y lo unico que se abre es por la via de la **VPN local** que usan Termux y PCAPdroid. Eso alcanza para escaneo y para capturar **el propio** trafico, pero no para ver la red completa: para eso sigue haciendo falta Kali. iOS es aun mas cerrado: no permite ni Termux ni captura de trafico sin jailbreak. **La app o Termux son ideales para el diagnostico rapido; Kali para el analisis profundo.**

---

## Ejercicio Integrador: Informe de Auditoria de la Red Casera

**Enunciado:** Consolidar las 3 practicas en un informe de 2-3 paginas con esta estructura:

```
INFORME DE AUDITORIA WiFi - [Fecha] - [Nombre del auditor]

1. INVENTARIO DE DISPOSITIVOS
   IP | MAC | Fabricante (OUI) | Modelo | Version SO/Firmware | Fuente (Windows/Kali/App)

2. POSTURA DE SEGURIDAD WiFi
   - Estandar: WiFi 4/5/6 (evidencia: netsh wlan show drivers)
   - Cifrado actual: WPA2-CCMP (evidencia: netsh wlan show interfaces)
   - Cifrado recomendado: WPA3-SAE
   - Estado WPS: Habilitado -> RIESGO ALTO

3. VULNERABILIDADES DETECTADAS
   Hallazgo | CVE (si aplica) | Severidad | Evidencia | Impacto
   Ej: Firmware 1.0.0 (2019) con CVE-2017-XXXX | Alta | searchsploit | RCE remota

4. COMUNICACIONES OBSERVADAS
   - Dominios visitados visibles via SNI (ejemplos)
   - Trafico en claro detectado (HTTP, DNS sin DoH)
   - Dispositivos que no deberian estar en la red

5. CHECKLIST DE ENDURECIMIENTO (10 controles de la clase)

6. RECOMENDACIONES PRIORIZADAS (maximo 5, con esfuerzo/impacto)
```

**Solucion paso a paso:**

1. Juntar las salidas de las 3 practicas: `arp-a.txt` y capturas de `netsh` (Windows), `escaneo-versiones.txt` y `respuestas.txt` (Kali), y los pantallazos de Fing/WiFi Analyzer mas las salidas de Termux (`nmap -sn`) y el `.pcap` de PCAPdroid (celular).
2. Construir el inventario (seccion 1) cruzando por IP y MAC: lo que un medio no vio (por ejemplo el fabricante en Windows) lo completa otro (nmap -O o Fing), y en la ultima columna se anota de donde salio cada dato.
3. Completar la postura WiFi (seccion 2) citando el comando exacto que la prueba (`netsh wlan show interfaces` para el cifrado, `netsh wlan show drivers` para el estandar y el estado de WPS).
4. Poblar la tabla de vulnerabilidades (seccion 3) uniendo el hallazgo de firmware con la busqueda en searchsploit/NVD; si no hay CVE, igualmente se documenta el riesgo de tener un firmware de 2019.
5. Exportar de Wireshark la lista de dominios por SNI (`tls.handshake.extensions_server_name`) y buscar trafico en claro con `http.request.method` y `dns` (seccion 4).
6. Marcar en la checklist los 10 controles como cumplidos o no, con la evidencia de cada uno (seccion 5).
7. Ordenar las recomendaciones por esfuerzo/impacto (seccion 6) y verificar que cada hallazgo tenga al menos una recomendacion asociada.
8. Revisar que el informe declare el ambito (red propia o autorizada) y evite afirmar "hay un intruso" sin evidencia.

**Criterios de evaluacion:**

| Criterio | Peso |
|----------|------|
| Evidencia tecnica comprobable (capturas, salidas, hash) | 30% |
| Uso correcto de las 3 plataformas (o justificacion de su ausencia) | 25% |
| Analisis de firmware + cruce con CVE | 20% |
| Claridad del informe y recomendaciones accionables | 15% |
| Cumplimiento del marco legal y etico declarado | 10% |

---

## Glosario

| Termino | Definicion | Por que importa |
|---------|------------|-----------------|
| **SSID** | Nombre visible de la red WiFi | No es seguridad: se puede ocultar, pero se filtra en los beacons |
| **BSSID** | MAC del punto de acceso | Identifica el AP fisico concreto que te da servicio |
| **Beacon** | Trama que anuncia "aqui estoy" cada 100ms | Cualquiera la escucha: revela SSID y capacidades |
| **WEP** | Cifrado de 1999 con RC4 de 40/104 bits | Roto: se descifra en minutos con ~40.000 paquetes |
| **WPA** | WPA con TKIP, transicion de WEP | Deprecado: TKIP tiene fallos estructurales |
| **WPA2** | Autenticacion PSK + cifrado AES-CCMP | El estandar actual; seguro con clave fuerte |
| **WPA3** | Autenticacion SAE + AES-GCMP 256 | Resiste ataques offline de diccionario |
| **PSK** | La clave WiFi precompartida | El unico secreto del modo personal |
| **4-way handshake** | Intercambio de 4 mensajes al asociar | Prueba el conocimiento del PSK sin revelarlo |
| **PMKID** | Primer mensaje del handshake con hash del PMK | Permite ataque con 1 paquete, sin cliente |
| **AES** | Algoritmo de cifrado simetrico moderno | Estandar de la industria; sin ataques practicos |
| **RC4** | Cifrado de flujo antiguo | Roto para WEP y debil para TKIP |
| **TKIP** | Protocolo de cifrado predecesor de AES | Sustituto temporal de WEP, hoy obsoleto |
| **CCMP / GCMP** | Modos de operacion basados en AES | Protegen integridad + confidencialidad |
| **WPS** | Conexion por PIN o boton | El PIN de 8 digitos se fuerza en horas -> desactivar |
| **KRACK** | CVE-2017-13077: reenvio del handshake | Exige parchear el firmware del router |
| **PMF (802.11w)** | Protege tramas de gestion | Detiene desconexiones forzadas |
| **OUI** | Primeros 3 octetos de la MAC (registro IEEE) | Identifica el fabricante del dispositivo |
| **MAC address** | Direccion fisica de la interfaz | Identifica pero **se falsifica**; no es confiable |
| **ARP** | Mapeo IP -> MAC en la LAN | Base del descubrimiento y del ARP spoofing |
| **ARP spoofing** | Enviar ARP falsos para interceptar trafico | MitM en LAN; se defiende con HTTPS y 802.1X |
| **DHCP** | Asignacion automatica de IPs | Su tabla es el inventario mas rapido de la red |
| **DNS** | Resolucion de nombres a IPs | Las consultas en claro revelan toda la navegacion |
| **DoH / DoT** | DNS sobre HTTPS / TLS | Cifra las consultas DNS: nadie ve que dominios visitas |
| **NAT** | Traduccion de IP privada a publica | Oculta la LAN; no sustituye a un firewall |
| **Modem** | Traduce la senal del medio (cobre, coaxial, optica) a Ethernet | Suele venir integrado en el equipo del proveedor: por eso "no lo ves" |
| **ONT** | Modem optico de fibra con router/WiFi integrado | Es el equipo del ISP en FTTH; ponerlo en modo puente evita doble NAT |
| **CGNAT** | NAT compartido del proveedor (rango 100.64.x.x) | Impide conexiones entrantes; hay que pedir IP publica si se necesita |
| **Doble NAT** | Dos routers traduciendo en cascada | Rompe port forwarding, DMZ y UPnP; busca que la WAN sea publica |
| **Gateway** | IP del router en la LAN | El primer salto hacia Internet y el foco del spoofing |
| **Nmap** | Escanner de redes y servicios | Estandar para inventario y fingerprinting |
| **`-sV`** | Deteccion de versiones de servicios | Convierte puertos abiertos en software+version identificable |
| **`-sn`** | Escaneo solo de hosts (sin puertos) | Descubrimiento rapido y poco ruidoso |
| **Wireshark** | Analizador de paquetes grafico | Permite ver "dentro" de la red y demostrar cifrado |
| **tshark** | Wireshark en linea de comandos | Ideal para scripts y capturas en servidores |
| **Termux** | Terminal de Linux en Android (sin root) | Permite `nmap`, `curl` y scripts desde el celular |
| **PCAPdroid** | Captura de trafico en Android via VPN local | Equivalente movil de Wireshark: solo el trafico del propio equipo |
| **Kali NetHunter** | Kali Linux instalado en Android | Acercara el arsenal de Kali al celular; modo monitor solo con hardware compatible |
| **Modo monitor** | Captura TODAS las tramas de un canal | Unica forma de ver el WiFi ajeno (requiere hardware compatible) |
| **Modo managed** | Solo el trafico propio | Lo normal en Windows/Android/iOS |
| **SNI** | Campo del TLS con el dominio visitado | El contenido esta cifrado, pero el destino se ve |
| **Man-in-the-Middle** | Atacante entre dos partes que se comunican | En WiFi: ARP spoofing o evil twin |
| **Evil twin** | AP falso con el mismo SSID | Los dispositivos se conectan solos -> defensa: PMF, WPA3, ver ESSID |
| **Firmware** | SO embebido del dispositivo | Si esta viejo, tiene CVEs publicados y explotables |
| **CVE** | Identificador unico de vulnerabilidad | El puente entre "version detectada" y "riesgo real" |
| **NVD** | Base de datos nacional de CVEs | Fuente oficial para buscar vulnerabilidades |
| **EOL (End of Life)** | Producto sin soporte/actualizaciones | Si el fabricante no parchea, hay que reemplazarlo |
| **IoT** | Dispositivos conectados (TV, camara, PLC) | Suelen ser el eslabon mas debil de la red |
| **UPnP/SSDP** | Autoanuncio de servicios en la LAN | Filtra modelo y version de cada dispositivo |
| **802.1X** | Autenticacion por puerto con RADIUS | Aislamiento por usuario: ideal para redes con visitas |
| **SSID broadcast** | Anuncio del nombre de red | Desactivarlo no da seguridad: el SSID se filtra igual |
| **Riesgo** | Probabilidad de que una amenaza explote una vulnerabilidad | No todo hallazgo es igual: se prioriza por impacto |

---

## Preguntas y Respuestas

**1. Por que se puede ver el nombre del sitio web que visito si HTTPS esta cifrado?**

Porque el primer mensaje del TLS (**Client Hello**) incluye el **SNI** (Server Name Indication), que indica el dominio solicitado, y ese campo viaja en claro para que el servidor sepa que certificado presentar. Ademas la **IP de destino** es visible siempre. El contenido (URL, formularios, respuestas) si esta cifrado. Por eso existen **ECH (Encrypted Client Hello)** y **DoH**: para cerrar tambien esos metadatos.

**2. Si cambio el SSID a uno raro, estoy mas segura?**

No. El SSID es un nombre, no una clave. Se envia en cada beacon en claro y un atacante lo ignora por completo. Peor aun: cambiarlo por uno similar a otro router (ej. `FBI-Surveillance-Van`) puede romper compatibilidad con dispositivos viejos. Lo que protege es la **clave WPA3/WPA2 y el firmware actualizado**.

**3. Que diferencia practica hay entre hacerlo en Windows, en Kali y en el celular?**

Windows da lo basico nativamente (`netsh`, `ipconfig`, `arp`) y permite instalar Wireshark: suficiente para un inventario y una auditoria ligera. Kali ofrece el arsenal completo: fingerprinting (`nmap -sV`), UPnP, modo monitor, aircrack, searchsploit y API de CVE. El celular es rapido y portable (Fing resuelve el inventario en 10 segundos) pero esta **aislado por el sandbox del SO**: no captura trafico ni escanea puertos. La combinacion de las 3 cubre desde el usuario final hasta el auditor.

**4. Mi router es de 2017 y no recibe actualizaciones. Que hago?**

Primero confirmarlo: buscar el modelo en la pagina del fabricante y en NVD. Si no hay firmware desde hace 2+ anos, el dispositivo esta **EOL** y cualquier CVE nuevo sera eterno. Acciones: (1) desactivar todo lo que se pueda (UPnP, gestion remota, WPS), (2) segmentar la red con una VLAN/guest para los IoT, (3) planificar el reemplazo. Un router es el perimetro de la casa: no es un gasto opcional.

**5. Puede alguien ver mis contrasenas con Wireshark?**

Solo si viajan en claro (HTTP, FTP, telnet, DNS). Con **HTTPS/TLS** el contenido esta cifrado con AES: Wireshark muestra bytes ilegibles. El riesgo real cuando todo esta cifrado son (a) los **metadatos** (que dominios visitas, cuando, cuanto trafico) y (b) los **dispositivos legacy** que aun hablan en claro (IoT baratos, impresoras). Por eso la auditoria revisa ambos: cifrado del trafico y version del firmware.

**6. Por que el ataque de diccionario a WPA2 no es un fallo de AES?**

Porque AES no se rompe: el atacante no descifra nada. Captura el handshake (que no contiene la clave, sino datos para derivar el PMK con 4096 iteraciones de PBKDF2) y **fuerza el PSK offline**, probando candidatos uno a uno. Es una carrera de CPU: un diccionario de 14 millones de palabras cae en segundos, una clave de 16 caracteres aleatorios no cae en la edad del universo. **La solucion es la longitud y aleatoriedad de la clave (y WPA3-SAE), no cambiar de algoritmo.**

**7. Desactive el broadcast del SSID. Sirve de algo?**

Casi nada. Oculta el nombre en los beacons, pero el SSID sigue viajando en claro cuando un cliente **se conecta o se reconecta**, asi que un atacante con modo monitor lo captura ademas de ver las MAC del AP y del cliente. Ademas suele causar problemas de compatibilidad. Es un control de "puerta cerrada con ventana abierta": solo disuade al vecino curioso, no a un atacante.

**8. Un dispositivo aparece en mi red y no se quien es. Que hago?**

1. Identificar la MAC en Fing/nmap y buscar el OUI en IEEE para saber el fabricante  
2. Cruzar con el DHCP del router (Host Name suele revelar el equipo)  
3. Si no se reconoce: cambiar la clave WiFi (lo desconecta a todos), subir a WPA3, y revisar que no sea un vecino conectado con la clave filtrada o un dispositivo propio con otro nombre  
4. Medida preventiva: habilitar **AP isolation** y red de invitados para los visitantes/IoT

**9. Todos tienen modem? Yo tengo el equipo de Antel y no veo ningun modem.**

No hay un equipo "modem" aparte porque **esta integrado en la caja del proveedor**. En fibra, lo que recibe la optica es la **ONT** (unidad de terminacion optica) y trae adentro el modem optico, el router y el WiFi: Antel la describe como "comunamente llamada modem o router" y puede operar en modo puente o router WiFi. En ADSL pasaba igual con el modem-router. Se comprueba en 30 segundos: comparar tu IP publica con la de tu equipo; si no coinciden, hay un NAT adelante (equipo del ISP y/o CGNAT). Eso es lo que se revisa en el bloque "Y el modem?" de la seccion 1 y en el Paso 1 de la Practica A.

**10. Puedo instalar herramientas de seguridad en un celular Android y probar lo mismo?**

Si, en parte. **Termux** (instalado desde F-Droid) da una terminal de Linux sin root y permite `nmap -sn` y `nmap -sT` contra la red propia, mas `curl` para revisar cabeceras del router. **PCAPdroid** (open source) captura el trafico del propio celular sin root usando una VPN local y exporta un `.pcap` que se abre en Wireshark con los mismos filtros de la Practica A. Lo que **no** se puede sin root es modo monitor, `aircrack`/`aireplay`, escaneos SYN/UDP ni ver el trafico de los demas dispositivos: ahi hace falta **Kali NetHunter** con root y un adaptador WiFi USB compatible, o directamente Kali en la VM (Practica B). En iOS ni siquiera hay Termux: todo queda en apps de inventario.

**11. Corri el barrido de la subred y me desaparecio mi red WiFi. La rompi?**

No: el barrido solo manda ping ICMP, no tiene forma de apagar el WiFi ni de ocultar el SSID. Lo que suele pasar es que **el router se reinicio o se colgo**, o que se apago el **boton WLAN** del equipo; mientras tanto **Windows se reconecta solo a otra red guardada**, y la PC aparenta seguir con internet en la red equivocada. Se revisa con `netsh wlan show networks` (si la propia no figura, el AP dejo de emitir), mirando los LED y el boton WLAN del router, y de ultima reiniciandolo. El caso inverso tambien vale: si la red cae **de forma repetida** al hacer el barrido, el hallazgo es del router (no resiste carga) y se documenta en el informe.

---

## Tarea / Lectura Recomendada

1. **Practicar:** Ejecutar la Practica A completa en Windows y entregar la carpeta `auditoria-wifi` del escritorio con las 5 salidas.
2. **Practicar:** Repetir el inventario con Kali (`nmap -sn -PR` + `nmap -sV`) y comparar los resultados con los de Windows y con Fing: cuantos dispositivos detecta cada plataforma y por que difieren.
3. **Auditoria:** Completar el checklist de endurecimiento de la seccion 5 en el router propio (con foto del panel antes/despues de cada cambio).
4. **Analisis:** Capturar 5 minutos de trafico con Wireshark y listar 5 dominios visibles via SNI + 1 trafico HTTP en claro si existe.
5. **Desde el celular:** Instalar Termux (F-Droid) y ejecutar `nmap -sn 192.168.1.0/24` y `nmap -sT -p 80,443 192.168.1.1`; luego instalar PCAPdroid, capturar 2 minutos y abrir el `.pcap` en Wireshark de la PC. Comparar cuantos equipos detecta el celular contra los de Windows y de Kali.
6. **Detectar el modem:** averiguar si en casa hay doble NAT o CGNAT (IP publica vs IP del equipo) y anotar si la ONT/router del proveedor esta en modo puente o router.
7. **Leer:** Wi-Fi Alliance - *WPA3 Specification*: https://www.wi-fi.org/discover-wi-fi/security
8. **Leer:** NVD - buscar el firmware de tu router: https://nvd.nist.gov/
9. **Leer:** OWASP - *Internet of Things Cheat Sheet*: https://owasp.org/www-project-internet-of-things/
10. **Ver:** Demo de KRACK (https://www.krackattacks.com/) - por que parchear el firmware del router es obligatorio.
11. **Investigar:** Diferencia entre WPA3-Personal (SAE) y OWE (Enhanced Open) para redes publicas, y porque el WiFi de un hotel deberia usar OWE y no WPA2 con clave compartida.
12. **Reflexionar:** Escribir un parrafo explicando por que "la seguridad de la red casera es la de su eslabon mas debil" usando un dispositivo IoT concreto como ejemplo.
