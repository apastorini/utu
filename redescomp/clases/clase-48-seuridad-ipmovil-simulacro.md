# Clase 48 — Seguridad aplicada, IP Móvil y Simulacro final

**Bloque:** F (Servicios) · **Semana:** 16 · **Duración estimada:** 150 min
**Correlativa:** Clase 47 (criptografía) · **Cierre del curso**
**Material de referencia:** Tanenbaum cap. 8 y cap. 6 (movilidad) · `ACTUALIZACIONES.md` §10 y §13

---

## 🎯 Al terminar esta clase vas a poder

1. Describir **cómo se aplica** la criptografía: **TLS**, **PGP** e **SSH**, y
   decir qué protección da cada uno.
2. Explicar qué es un **túnel** y una **VPN**, con los **dos modos** (enrutada vs.
  Switched) y el **doble encapsulado**.
3. Distinguir **IDS**, **IPS** y **DPI**, con el criterio de **falso positivo** y de
   **punto deplacede inspección**.
4. Reconocer **cinco ataques típicos** y decir **qué capa** los elimina.
5. Dibujar la arquitectura de **IP Móvil** con los **cuatro componentes** y sus
   **tres modos** de operación, incluida la **ruta triangular**.
6. Resolver un examen completo de 3 horas con cronómetro, por última vez.

> **Prerequisito del examen:** `2011-02 Problema 2` (30 pts — IP Móvil: campos
> MAC/IP por segmento y túnel), `2008-12 P3` (10 pts — arquitectura de IP Móvil),
> `2007-07 P5` (5 pts — funcionamiento de IP Móvil), `2009-07 Problema 1` (30 pts),
> `2008-12 Problema 1` (30 pts — NAT con balanceo de carga), `2008-08 Problema 1`
> (30 pts — tunneling).

---

# PARTE 1 — TEORÍA

## 1.1 TLS: la protección aplicada de un protocolo de aplicación

La clase 47 dio la criptografía. TLS es **la aplicación completa**, y es lo que
justifica toda la clase 47.

```
   ┌─────────────────────────────────────────────────────────────┐
   │                                                             │
   │   SIN TLS                     CON TLS                       │
   │   ─────────                   ────────                      │
   │   El ATM ve                  El ATM ve                     │
   │   "usuario ana               "usuario ana"                 │
   │  / clave: XYZ123"            (todo cifrado)                │
   │                                                             │
   │   → el sniff ve la          → el sniff ve bytes            │
   │     contraseña                 incomprensibles             │
   │   → el MITM modifica        → el MITM rompe el MAC →       │
   │     el monto de la           el cliente lo detecta          │
   │     transferencia                                                │
   └─────────────────────────────────────────────────────────────┘
```

**El handshake de TLS 1.3, mensaje por mensaje** (esto se pregunta):

```
   CLIENTE                                    SERVIDOR
   ───────                                    ────────
   1. ClientHello
      · versión soportada (TLS 1.3)
      · cipher suites  ← ciphers SIMÉTRICOS + hash
      · key_share      ← kp de X25519 o ML-KEM  ← lo trae EN EL MENSAJE 1
      · supported_versions
   ─────────────────────────────────────────────────────▶
                                  2. ServerHello
                                     · elige cipher suite
                                     · ServerHello.key_share ← kp del servidor
                                  3. {EncryptedExtensions}
                                  4. {Certificate}
                                     · kp del servidor (autenticación)
                                  5. {CertificateVerify}
                                     · FIRMA con la clave privada
                                        ★ esto prueba que es quien dice ser
                                  6. {Finished}
                                     · MAC sobre todo el transcript
   ◀────────────────────────────────────────────────────
   7. {Finished}
   ─────────────────────────────────────────────────────▶

   ★ TODO desde (2) en adelante va CIFRADO.
     Los dos Finished exchanged en 1-RTT.
```

**Los cuatro servicios, con el mecanismo exacto que los da:**

| Servicio | Mecanismo en TLS 1.3 |
|---|---|
| **Confidencialidad** | clave de sesión derivada por (EC)DH; cifrado con **AES-256-GCM** o **ChaCha20-Poly1305** |
| **Integridad** | **AEAD**: el tag de autenticación va en cada registro |
| **Autenticación del servidor** | **certificado X.509** + firma del *CertificateVerify* |
| **Autenticación del cliente** | opcional: **certificado cliente** o **SRP** / PSK |
| **Forward secrecy** | **(EC)DH efímero**: las claves de sesión se borran y no se pueden recuperar |

**El concepto que hay que entender: el *forward secrecy*.**

```
   SIN forward secrecy:          CON forward secrecy (PFS):
   ──────────────────────        ──────────────────────────
   El servidor guarda la         El servidor NO guarda la
   clave de sesión.              clave de sesión. Nunca la
   Alguien que roba el           tuvo guardada. Cuando se
   servidor HOY obtiene          termina la conexión, se
   TODO: el tráfico de           borra. Lo único que queda
   AYER descifrado.              es la clave pública (pública).
   ★ "Perfect forward secrecy"   ★ Aunque te entreguen el disco
     significa: aunque te        forense del servidor hoy, no
     entreguen la clave AHORA,    podés descifrar lo de ayer.
     no descifrás lo de AYER.
```

**Y es por eso que el *handshake* de TLS 1.3 es de 1-RTT**: se manda el
`key_share` en el **primer mensaje**, sin esperar el `ServerHello` con
criptografía clásica (RSA). Antes (TLS 1.2 con RSA) eran 2 RTT. Ese es un avance
real y medible.

**Y el puerto que se cambia:** HTTP en 80, **HTTPS en 443**. Y ojo: **443 es
TCP**, no UDP. (El **443/UDP** es **QUIC**, que es otra cosa — clase 9.)

## 1.2 SSH: el mismo esquema, otro uso

```
   CLIENTE ─────────── SERVIDOR
      │                    │
      │── kp_srv ─────────▶│   1. el servidor manda su clave de host
      │                    │      (¡EN CLARO! de eso se encarga DNS/DH)
      │◀─ kp_cli (efímera) ─│   2. el cliente manda su clave efímera
      │                    │
      │  secreto compartido │
      │  + HKDF + las claves de cifrado de sesión  ← derived keys
      │                    │
      │◀═══ CANAL CIFRADO ═══▶│   3. de acá en adelante todo va cifrado
```

**Puntos clave de SSH:**

- **La clave de host es del servidor, pública, y se publica en el DNS** (o en el
  `known_hosts`). Se verifica: si cambia, te avisa.
- **Las claves de sesión son efímeras**: se renegocian por canal o cada hora.
  **Es lo que da el PFS** en SSH.
- **Autenticación del usuario**: por clave pública (ideal), o por contraseña (y
  acá el problema famous: el servidor no recibe la contraseña, sino un valor
  derivado, así que un *sniffer* no la obtiene).
- **Canal de control + canales de sesión**: el canal de control multiplexa varias
  sesiones (port forwarding, SOCKS, agent forwarding). **Es el mismo concepto de
  multiplexación de la clase 16, pero en la capa de aplicación.**
- **Moderno**: por defecto usa **Ed25519** para las claves de host y ECDH para el
  acuerdo (`RFC 8709`, 2020).

> **El "ataque del hombre en el medio" en SSH solo funciona si nadie verifica la
> clave del host.** Y la primera conexión pregunta "¿confiás en esta huella?". Si
> decís que sí sin leer, **perdiste**. Es exactamente el problema de la raíz de
> confianza de la clase 47, pero resuelto a nivel de un solo servidor.

## 1.3 PGP: cifrar correo entre usuarios

PGP (*Pretty Good Privacy*) es el esquema de **seguridad extremo a extremo** para
correo. La diferencia con TLS es **dónde está el protocolo**:

```
   TLS    ──  SEGURIDAD EN EL CAMINO (transport)
            El servidor web la termina: ve todo el tráfico.
            ★ Confiás en el servidor.

   PGP    ──  SEGURIDAD EXTREMO A EXTREMO (aplicación)
            Cifrás el mensaje antes de que salga de tu máquina.
            El servidor de correo TRANSPORTA un texto cifrado.
            ★ El servidor no puede leerlo, aunque lo quiera.
```

**El modelo de claves de PGP** (y el detalle fino que se pregunta):

```
   Cada usuario tiene UNA clave privada y VARIAS claves públicas:

   ┌───────────────────────────────────────────────────────────────┐
   │  Clave MAESTRA (primary key)                                  │
   │    · RSA/ECDSA/EdDSA. Firma. Certifica las subclaves.         │
   │    · Con la que firmás.                                        │
   ├───────────────────────────────────────────────────────────────┤
   │  SUBCLAVE DE CIFRADO                                          │
   │    · RSA o ElGamal (cifrado).                                 │
   │    · Para los que te escriben A VOS.                          │
   ├───────────────────────────────────────────────────────────────┤
   │  SUBCLAVE DE FIRMA                                            │
   │    · DSA/RSA/EdDSA.                                           │
   │    · Para firmar los key ID de las claves de los demás.       │
   └───────────────────────────────────────────────────────────────┘

   ★ La SEPARACIÓN de la clave de firma de la de cifrado es el innovation
     clave: una clave que solo firma NO puede cifrar (y una que solo
     cifra no debería firmar). Es "separación de privilegios".
```

**El proceso de enviar correo con PGP** (ocho pasos):

```
   EMISOR                                RECEPTOR
   ───────                                ───────

   1. Firma:
      H(m) ──► [mi subclave de firma] ──► σ

   2. Cifrado de σ y m:
      [clave pública de Beto (RSA)] ──► (σ ‖ m) cifrado

   3. Agrega metadatos (armored):
      ── BEGIN PGP MESSAGE ──
      m = 65, σ = 2790, kp_emit = 3233
      ── END PGP MESSAGE ──

   4. Envía por SMTP normal. El servidor de correo transporta
      texto ilegible.
                              ◀──── mensaje cifrado ────

   5. Descifra con su clave privada (RSA): recupera (σ ‖ m)

   6. Verifica con la clave pública de Ana (la que trae el
      mensaje, con su key ID): σ^e mod n = H(m)?
      SÍ → "el mensaje es de Ana y está íntegro"
      NO → mensaje alterado o de otro emisor

   7. Extrae la clave pública de Ana del mensaje mismo
      (va firmado con la subclave de firma de Ana).
```

**El problema de la web of trust (*gráfico de confianza*), que se pregunta:**

```
   Cada usuario tiene un key ID. Los usuarios se FIRMAN entre sí
   (el "key signing party"):

       Ana ──firmada por──▶ Beto ──firmada por──▶ Carla
         ▲                                    ▲
         └────────────────────────────────────┘
              Ana y Carla se confían indirectamente

   ★ Problema: ¿qué pasa si Ana firma la clave de Beto pero
     Beto es un atacante? Y la clave "modelo de confianza" de
     PGP: solo son válidas las firmas de claves que están en un
     keyserver confiable.

   ★ RESPUESTA MODERNA (2019+): el modelo de confianza de Web of Trust
     quedó OBSOLETO. Lo que se usa ahora es:
       · la llave pública se verifica FUERA DE BANDA (imprenta, QR,
         Signal Safety Numbers, servidor de correo conocido);
       · o la FIRMATURE por la cadena de CA (PDF/A-3 signatures,
         firma de código de paquete).
```

> **Y ojo con esto en 2026:** PGP (OpenPGP) sigue siendo un estándar, pero por
> problemas históricos de **confianza en el modelo de web of trust** y por el
> asunto **pgp4u/GnuPG** (2023), el mundo de la mensajería pasó a **Signal**
> (protocolo Signal, doble ratchet) o a **Matrix** (MLS). En un examen de 2026,
> si te preguntan sobre cifrado de mensajería, la respuesta moderna es
> **extremo a extremo con identidad fuera de banda**, no "confiá en la firma de
> la clave".

## 1.4 Túneles y VPN

**Túnel** = **encapsular** un paquete dentro de otro para que viaje por una red
que **no lo entiende**. Es una de las 4 técnicas de tunneling (RFC 1701):

```
   ┌─────────────────┐                    ┌─────────────────┐
   │  PAQUETE ORIGINAL│                    │  PAQUETE ORIGINAL│
   │  IP_or: 10.0.0.1│                    │  IP_or: 10.0.0.1│
   │  IP_des: 172.16. │  ◄─ encapsulado ─►│  IP_des: 172.16. │
   │       0.5       │     dos veces      │       0.5       │
   └─────────────────┘                    └─────────────────┘
                    ▲                          ▲
                    │  IP_or: 200.1.1.1      │
                    │  IP_des: 200.1.1.2      │
                    │  ┌────────────────────┐ │
                    │  │  IP_or: 10.0.0.1    │ │
                    │  │  IP_des: 172.16.0.5│ │
                    │  └────────────────────┘ │
                    └──────────────────────────┘
                        PAQUETE COMPLETO CON
                        DOS ENCABEZADOS IP
```

**El tunneling es "encapsulation con dos IP":**

| Técnica | Qué hace | Para qué |
|---|---|---|
| **Generic Routing Encapsulation (GRE)** | encapsula **cualquier** protocolo | transparent tunnelling |
| **IP-in-IP** (`RFC 2003`) | solo IP | si sabés que es IP |
| **VXLAN** | **Ethernet sobre IP** (toda la trama MAC) | **overlay en centros de datos** (el moderno) |
| **WireGuard** | cifrado moderno y simple | VPN de 2026 |

### Los dos modos de VPN (esto es lo que se pregunta)

```
   (1) TUNNELING ENRUTADO                          (2) TUNNELING CONMUTADO
      (routing-based / router-to-router)              (switched / Layer 3 switch)

      El router tiene una interfaz        Cada puerto del switch termina un
      "virtual" (tunnel interface):        túnel: todo lo que entra por
      la ruta apunta a esa                un puerto sale por otro con el
      interfaz.                           otro IP de encabezado.

      ┌────────┐  túnel  ┌────────┐     ┌──────┐        ┌──────┐
      │ R1     │═════════│ R2     │     │Switch│        │Switch│
      │ ip_public │      │        │     │ p1   │        │ p2   │
      └───┬────┘         └────┬───┘     └───┬──┘        └──┬──┘
          │                   │             │              │
       Red IP                Red IP       Red A         Red B
      (rutable)             (rutable)   (privada)      (privada)

      Cada paquete:                          Cada paquete:
        encapsulated 2 veces                  encapsulated 2 veces
      Se enruta por la red pública          NO se enruta: se conmuta
      (switch no lo mira)                   (el switch lo reenvía como
                                             cualquier trama)
```

**La diferencia conceptual clave:**

| | Enrutado | Conmutado |
|---|---|---|
| **Información que mira el switch** | **ninguna**: ve el IP externo y reenvía | ve **el Mac destino** y reenvía |
| **Se usa cuando** | las redes son **públicas y ruteables** (Internet) | las redes son **privadas** (no se enrutan por ningún lado) |
| **Mismo protocolo en las dos redes** | casi siempre **diferente** (IPX ↔ IP) | casi siempre **diferente** |
| **Ejemplo típico** | **IPsec en Internet** | **ATM LAN Emulation** (es histórico) |

**Y el doble encapsulado del que habla el Examen 2008-08 Problema 1:**

```
   Un paquete de la LAN A (172.16.1.0/24) para la LAN B (10.1.1.0/24):

   ┌─────────────────────────────────────────────────┐
   │ ENCABEZADO EXTERNO:                             │
   │   IP_or  = 200.1.1.1   (R1, público)          │
   │   IP_des = 200.1.1.2   (R2, público)          │
   ├─────────────────────────────────────────────────┤
   │ ENCABEZADO INTERNO:                             │
   │   IP_or  = 172.16.1.5  (host en A)            │
   │   IP_des = 10.1.1.3    (host en B)            │
   ├─────────────────────────────────────────────────┤
   │   TCP / datos de aplicación                     │
   └─────────────────────────────────────────────────┘

   ★ El switch de la red pública ve SOLO 200.1.1.1 → 200.1.1.2.
     El router R2 ve las dos cabeceras y quita la externa.
```

**Y el VPN real de 2026** es WireGuard o IPsec:

```
   WireGuard  → ~4 000 líneas de código (comparadas con ~500 000 de OpenVPN)
             → criptografía moderna y simple
             → sin negociación de cipher: los peers se preconfiguran

   IPsec      → dos modos:
                 TRANSPORT mode: se cifra SOLO el payload, las cabeceras IP
                                  originales se mantienen visibles
                 TUNNEL mode:   se encapsula el PAQUETE ENTERO (lo de arriba)
```

## 1.5 IDS, IPS y DPI

### Los cuatro componentes

```
   ┌─────────────────────────────────────────────────────────────┐
   │  (1) FUENTES      tráfico de red, logs, eventos del host    │
   │                   (NetFlow, sFLOW, syslog)                   │
   ├─────────────────────────────────────────────────────────────┤
   │  (2) SENSORES     equipos que analizan (NIDS, HIDS)         │
   │                   patrones, firmas, heurísticas              │
   ├─────────────────────────────────────────────────────────────┤
   │  (3) MOTOR DE     compara contra las reglas;               │
   │      ANÁLISIS     correlaciona eventos;                     │
   │                   puntúa (IDS:Score)                        │
   ├─────────────────────────────────────────────────────────────┤
   │  (4) RESPESTA     el operador (IDS) o el equipo             │
   │                   (IPS: bloquea automáticamente)             │
   └─────────────────────────────────────────────────────────────┘
```

### IDS vs. IPS: la diferencia es una línea

```
   IDS  (Intrusion DETECTION System)
   ────────────────────────────────
   Está MIRANDO. Detecta y AVISA.
   El tráfico PASA IGUAL.

   ┌────┐  ──trama sospechosa──▶  [IDS]  ──▶ 🚨 ALERTA al operador
   └────┘                                        │
   └────┘  ──sigue igual──────▶  [destino]     el operador decide

   ★ VENTAJAS:  no interrumpe el tráfico bueno; si el IDS falla,
     solo perdés visibilidad.
   ★ DEBILIDAD: el ataque PASA. Si el operador no mira, no pasa nada.

   IPS  (Intrusion PREVENTION System)
   ───────────────────────────────────
   Está EN el camino. Detecta y BLOQUEA.

   ┌────┐  ──trama sospechosa──▶  [IPS]  ──▶ 🛑 DESCARTADA
   └────┘

   ★ VENTAJAS:  frena el ataque en el momento.
   ★ DEBILIDAD: si el IPS se cuelga y se pone en modo "fail-open",
     pasa TODO. Si se pone en "fail-close", corta el servicio legítimo.
     Es un punto único de falla.
```

> **El compromiso real:** el IPS tiene que estar **en línea** (inline), y eso
> significa que es un **punto único de falla** y un **cuello de botella de
> rendimiento**. El IDS, en cambio, se puede poner en un **puerto espejo**
> (*span port*), que no toca el tráfico: ve una copia. **La respuesta completa al
> examen es esa: IDS en puerto espejo (seguro pero no bloquea), IPS en línea
> (bloquea pero es punto único de falla).**

### Los dos criterios de decisión

| Criterio | Question | Por qué importa |
|---|---|---|
| **¿Punto?** | ¿Dónde está en la red? | NIDS (red), HIDS (host), WIDS (inalámbrico) |
| **¿Cuándo?** | ¿Cómo detecta? | **por firma** (patrón conocido) vs. **por anomalía** (estadística) |

**Y el problema central de todo IDS: el falso positivo.**

```
   ¿FALSO POSITIVO?   = alerta de un ataque que NO hay
   ¿FALSO NEGATIVO?   = un ataque que NO se detecta

   El problema clásico: en un centro de cómputos grande hay
   ~10 000 eventos de seguridad POR DÍA. Si el 95 % son falsos
   positivos, el operador deja de mirar en una semana.

   ★ El refinamiento: el "IDS Score" (eNSP) — puntúa cada evento
     por la probabilidad de ataque y lo ordena por prioridad.
     Así el operador mira los 10 más graves, no los 10 000.
```

**Y los dos estilos de respuesta:**

```
   (a) INTERRUPTIVA  (active response)
       el IPS hace ALGO para frenar el ataque:
         · bloqueo del atacante
         · terminate la sesión TCP
       ★ RIESGO: convertir un ataque en un DoS propio.

   (b) PASIVA        (passive response)
       el IPS solo registra y AVISA; que otro sea el que frene.
       ★ más seguro, pero más lento.
```

### DPI: *Deep Packet Inspection*

```
   IDS/IPS  compara el PAQUETE contra FIRMAS.
             "¿hay un 'EICAR' en esta conexión?"

   DPI     ABRE el paquete, lo DECODIFICA, y lo interpreta
           como si fuera tráfico de aplicación.

           ┌───────────────────────────────────────────┐
           │  Capa 1-4:  IP  TCP/UDP                   │
           │  ┌─────────────────────────────────────┐  │
           │  │ Capa 7:  HTTP GET /index.html        │  │
           │  │  ... el DPI lee la URL, los          │  │
           │  │  headers, incluso el TLS (con las    │  │
           │  │  claves o en un proxy MITM)          │  │
           │  └─────────────────────────────────────┘  │
           └───────────────────────────────────────────┘

   ★ Lo que permite:
     · policy de Application (permitir Facebook, bloquear
       un juego)
     · detección de malware
     · filtrado de spam
     · INSPECCIÓN DE CONTENIDO cifrado  ← acá está el
       problema gigante (clasificados vs. privacidad)
```

> **⚠️ El problema de DPI con cifrado.** Hoy **todo** está cifrado (HTTPS),
> así que un DPI en el medio **no puede leer el contenido**. Para hacerlo:
> 1. **Proxy MITM** con las claves del servidor (que hoy **no se puede** con
>    cifrado de extremo a extremo).
> 2. Instalar la **certificación de una CA propia** en cada dispositivo
>    (esto es lo que hacen losINAfiltered de empresa y las redes de wireless).
> 3. Descifrado en el **endpoint** (instrumentación del navegador).
>
> Es la tensión central de la seguridad de red hoy: **confinarse el tráfico a la
> red ya no es posible sin romper el cifrado de extremo a extremo**. Y por eso
> muchos países (la UE con **ePrivacy**, el Network neutrality) lo han limitado
> con leyes.

## 1.6 Los ataques típicos y qué capa los detiene

Esta tabla es **el resumen más rentable de la clase**: si sabés decir qué capa
corta cada ataque, entendiste seguridad.

```
   ┌─────────────────────┬──────────────────┬─────────────────────────────┐
   │ Ataque              │ Capa donde vive  │ Qué lo detiene              │
   ├─────────────────────┼──────────────────┼─────────────────────────────┤
   │ Sniffing            │ 2 / 3 / 7        │ Cifrado (TLS). Nunca        │
   │                     │                  │ confíes en el cable.       │
   ├─────────────────────┼──────────────────┼─────────────────────────────┤
   │ ARP spoofing        │ 2                │DAI / port security /       │
   │ (ARP poisoning)     │                  │DHCP snooping / VLAN        │
   ├─────────────────────┼──────────────────┼─────────────────────────────┤
   │ IP spoofing         │ 3                │ Ingress filtering (uRPF):  │
   │                     │                  │ el router descarta lo que  │
   │                     │                  │ llega por la interfaz      │
   │                     │                  │ equivocada (BCP 38)        │
   ├─────────────────────┼──────────────────┼─────────────────────────────┤
   │ Mac flooding         │ 2                │ El table flooding: un      │
   │                     │                  │ puerto ve X MACs → se      │
   │                     │                  │ SHUTDOWN y se alerta        │
   ├─────────────────────┼──────────────────┼─────────────────────────────┤
   │ Secuestro DHCP      │ 2                │ DHCP snooping + port        │
   │ (rogue DHCP server) │                  │ security en los puertos de  │
   │                     │                  │ usuario (los puertos no    │
   │                     │                  │ pueden ser servidores)     │
   ├─────────────────────┼──────────────────┼─────────────────────────────┤
   │ Secuestro BGP       │ 3                │ RPKI / ROA: validar que el  │
   │                     │                  │ prefijo está autorizado    │
   │                     │                  │ (ver §Actualización)        │
   ├─────────────────────┼──────────────────┼─────────────────────────────┤
   │ Secuestro DNS       │ 3 / 7            │ DNSSEC: firma la respuesta │
   │                     │                  │ con la clave de la zona     │
   ├─────────────────────┼──────────────────┼─────────────────────────────┤
   │ Rogue CA / MITM TLS │ 7                │ PKI + validación de SAN +  │
   │                     │                  │ CT logs. O sellado         │
   │                     │                  │ (pinning).                 │
   ├─────────────────────┼──────────────────┼─────────────────────────────┤
   │ Ping of Death,      │ 3                │ Filtering de paquetes con   │
   │ Smurf, Teardrop     │                  │ TTL, longitud, flags.      │
   │ DoS                 │                  │ ACLs anti-spoof.           │
   ├─────────────────────┼──────────────────┼─────────────────────────────┤
   │ Secuestro de sesión │ 4 / 7            │ TLS con safe renegotiation; │
   │ (session hijacking) │                  │ HSTS; cookies HttpOnly+     │
   │                     │                  │ Secure.                   │
   ├─────────────────────┼──────────────────┼─────────────────────────────┤
   │ Pharming            │ 7                │ DNSSEC + validación de     │
   │                     │                  │ certificados + HTTPS.       │
   └─────────────────────┴──────────────────┴─────────────────────────────┘
```

> **Lo importante:** **ningún mecanismo de capa 2 o 3 es una frontera de
> seguridad**. Todos son **defensas en profundidad**. La única defensa que
> **realmente** impide el MITM y el eavesdropping es la **criptografía de la
> capa de aplicación** (TLS), porque no depende de que el atacante esté en tu red.

## 1.7 IP Móvil

### El problema

```
   El nodo MÓVIL (MN) tiene una DIRECCIÓN PERMANENTE (home address = IP fija),
   que pertenece a su RED LOCAL (home network).

   Cuando se va a otra red (foreign network), cambia de IP.
   PERO sus interlocutores (CN = correspondent node) siguen hablando con la
   HOME ADDRESS.

   El problema: los paquetes para la HOME ADDRESS van a la HOME NETWORK, y no
   llegan al MN. El MN no recibe nada. Se rompe la conexión TCP.

   ★ La identidad del MN es su HOME ADDRESS. Y la identidad viaja con él
     en todos los sistemas. ¿Cómo se hace para que siga funcionando?
```

### Los cuatro componentes (esto es EXACTAMENTE la respuesta al Examen 2008-12 P3)

```
   ┌──────────────────────────────────────────────────────────────┐
   │                                                              │
   │   MN ──────── Home Network ──────── Home Agent             │
   │  (nodo      (red local del         (el router de la         │
   │   móvil)     nodo móvil)            RED LOCAL, que           │
   │                │                  "actúa como proxy"        │
   │                │                       │                     │
   │                │                   se REGISTRA              │
   │                │                   cuando llega              │
   │                                                              │
   │   MN ──────── Foreign Network ──── Foreign Agent            │
   │                  │                   (el router de la         │
   │                  │                    RED VISITADA)           │
   │                                      │                       │
   │                                      │ recibe el registro     │
   │                                      │ y avisa al HOME AGENT   │
   │                                      ▼                       │
   │                                   COA (Care-Of Address)      │
   │                                   = la IP que tiene el MN   │
   │                                     en la red foránea        │
   │                                                              │
   │   CN ───────── Correspondent Node                            │
   │   (con el que el MN se comunica, p.ej. un servidor web)      │
   │                                                              │
   └──────────────────────────────────────────────────────────────┘
```

**La tabla de roles que hay que saber de memoria:**

| Componente | Qué es | Rol |
|---|---|---|
| **MN** (*Mobile Node*) | el host que se mueve | tiene dos direcciones: **permanente** (la de casa) y **care-of** (la temporal) |
| **HA** (*Home Agent*) | el router de la **red local** | hace de **proxy** del MN: guarda su ubicación y **reenvía** los paquetes que llegan a la home address |
| **FA** (*Foreign Agent*) | el router de la **red foránea** | recibe el **registro** del MN y le **notifica** al HA |
| **CN** (*Correspondent Node*) | el otro extremo (servidor, peer) | habla con la home address del MN |

**Y las dos direcciones del MN:**

```
   HOME ADDRESS (permanente):  172.16.0.5   ← siempre la misma
                                    ↕
                          SON DISTINTAS
                                    ↕
   CARE-OF ADDRESS (temporal):  172.172.0.17  ← cambia con cada red
```

### Los tres modos de operación

```
   (1) MODO SIMPLE (sin foreign agent)
   ──────────────────────────────────
   El MNOBTIENE care-of address por DHPCS o SLAAC, y se REGISTRA
   DIRECTAMENTE con el HA.

   El MN ──REGISTRATION──▶ HA      "estoy en 172.172.0.17, TTL = 300 s"

   ┌──────────┐                     ┌──────────┐
   │   MN     │──── registro ──────▶│   HA     │
   │ home:     │                     │          │
   │ 172.16.0.5│                     │ guarda:  │
   │ care-of:  │◀── binding ack ───│ MN@      │
   │ 172.172.  │                     │ COA      │
   │   0.17    │                     └──────────┘

   ★ El MN se mete solo en la foreign network.

   (2) MODO CON FOREIGN AGENT  ← el del Examen 2011-02
   ─────────────────────────────────────────────
   El MN NO puede obtener una dirección: la pide al FA,
   que le ASIGNA la care-of address.

   ┌──────────┐                     ┌──────────┐
   │   MN     │──── registro ──────▶│   FA     │
   │          │◀─ COA = 172.172.0.17│          │
   └────┬─────┘                     └────┬─────┘
        │                                │
        │                                │ "el MN está acá, en 172.172.0.17"
        │                                ▼
        │                           ┌──────────┐
        └──────────────────────────▶│   HA     │
              (el paquete del MN      │          │
               pasa por el FA y        │ crea el │
               llega al HA)           │ TÚNEL   │
                                    └──────────┘

   ★ El MN queda "dentro" del FA: usa la red interna del FA.

   (3) MODO CORRESPONDENT  (CN actualizado)
   ─────────────────────────────────────
   Se le AVISA al CN cuál es la care-of address del MN, para que el
   CN mande directo al MN y no pase por el HA. Se evita el túnel.

   ★ Es la forma más eficiente pero la más compleja de implementar.
```

**Los dos mensajes que hay que saber:**

| Mensaje | Quién → Quién | Contenido |
|---|---|---|
| **Binding Update** | MN → HA (o MN → FA → HA) | "mi care-of address es X, con TTL de 300 s" |
| **Binding Acknowledgement** | HA → MN | "recibí tu registro, vigente hasta las 15:34" |

### La ruta triangular — el problema conceptual central

Acá está **el 90 % de los puntos** de los problemas de IP Móvil.

```
   ESCENARIO: MN está en la foreign network. El CN (servidor)
   está en la INTERNET (ni en la home ni en la foreign).

   ¿Cómo llega un paquete del CN al MN?

   ── RUTA TRIANGULAR (lo que hace IP Móvil) ──

        CN                HA              FA              MN
        │                 │               │               │
        │──paquete────────▶│               │               │
        │  (destino:      │               │               │
        │   HOME ADDRESS  │               │               │
        │   del MN)       │               │               │
        │                 │──TÚNEL────────▶│               │
        │                 │  (destino:     │               │
        │                 │   CARE-OF ADDR)│               │
        │                 │               │──paquete──────▶│
        │                 │               │               │
        │◀────────paquete──────────────────│──paquete──────│
        │                 │               │               │

   ★ Los paquetes HACEN UN TRIÁNGULO: CN → HA → FA → MN, y de vuelta.
     El HA desvía el tráfico al túnel.

   ── ¿POR QUÉ ES NECESARIA? ──
   Porque el CN no sabe la care-of address del MN.
   Los paquetes del CN van a la HOME ADDRESS, y el HA es el
   único que sabe dónde está el MN ahora.

   ── EL PROBLEMA: "routing triangular"  ──
   El tráfico va y vuelve por la red INTERNA del operador.
   Hay trTransit link entre HA y FA. Y el CN está en Internet.

   ★ El problema es que el tráfico de ida y el de vuelta PUEDEN
     tomar caminos DISTINTOS → ASIMETRÍA. Eso rompe algunos
     protocolos y confunde a los middleboxes.
```

> **La solución que da el Examen 2011-02** (y es lo que hay que escribir):
> *implementar un **túnel** entre el HA y el FA, **de forma escalable**: no
> modificando los routers intermedios (que sería no escalable) sino
> **encapsulando** los paquetes que el HA le manda al FA. O sea, cuando el HA
> reenvía al COA, en vez de mandar el paquete pelado, le pone **un encabezado IP
> extra** con origen `IP_HA` y destino `IP_FA`. Así:*
>
> - *El paquete del CN al MN viaja: `[IP_or:CN, IP_des:HOME_MN]` → HA lo envuelve: `[IP_or:HA, IP_des:FA][IP_or:CN, IP_des:HOME_MN]` → FA lo desenvuelve y lo entrega al MN.*
> - *El paquete del MN al CN viaja **directo**: `[IP_or:COA_MN, IP_des:CN]`. No pasa por el HA.*
>
> *Escalable porque requiere **solo configurar los dos routers extremos** (HA y
> FA), sin tocar los intermedios. Y sin túnel, el paquete del MN al CN
> haría el mismo camino dos veces, y el TTL lo descartaría.*

### ⚠️ Actualización a 2026 — por qué esto no se desplegó

Esta es una de las piezas de **reencuadre** más importantes del curso.

```
   Mobile IPv4  (RFC 5944, 2010) ─┐
   Mobile IPv6  (RFC 6275, 2011) ─┴─→ SIGUEN EN STANDARDS TRACK. NO SON OBSOLETOS.
                                    ╰─→ PERO NO SE DESPLEGARON.

   ¿POR QUÉ NO?
   1. COMPLEJIDAD: requiere modificar el MN, el HA y el CN. Cada operador
      tendría que soporte todo el stack. IPv6 va aún más lejos con la migración.
   2. MIDDLEBOXES: NAT, firewalls y load balancers en el camino rompen el
      túnel porque "no entienden" la hipótesis del túnel.
   3. CGN: en el mundo real hay CGNAT (Carrier-Grade NAT). El HA no puede
      ver al CN porque ambos están detrás de NAT.
   4. ROAMING ENTRE TECNOLOGÍAS: pasar de 4G a 5G a WiFi a 5G rompe la
      dirección. IP Móvil asume una red, no una tecnología.

   ── ¿QUÉ SE USA EN 2026 EN SU LUGAR? ──
   · VPN  (WireGuard, IPsec): simple, funciona, oculta todo.
   · CGN + IPv6: la dirección ya no importa tanto.
   · QUIC connection migration (RFC 9000 §9): la industria resolvió la
     movilidad EN LA CAPA DE TRANSPORTE, no en la capa 3.

   ★ EL CAMBIO DE PARADIGMA: el Connection ID (RFC 9000 §5.1) hace que
     la identidad de la conexión DEJE DE SER LA IP. Eso habilita:
       (a) migración de conexión (cambiás de WiFi a 5G sin cortar)
       (b) NAT rebinding sin romper (el NAT cambia el puerto, QUIC no se rompe)
       (c) balanceo en servidores (varios servidores, un Connection ID)
```

> **Para el examen:** si te piden IP Móvil, **respondé como en 2011** (el modelo
> con HA, FA, COA, ruta triangular es lo que se evalúa), **PERO agregá una línea
> al final** diciendo que en la práctica se reemplazó por VPN + QUIC migration,
> y **por qué**. Esa última línea es la que te distingue.

---

# PARTE 2 — PRÁCTICA RESUELTA

## 2.1 Ejercicio 1 — El túnel doble del Examen 2008-08

**Datos.** Una empresa tiene dos sedes: LAN A = `172.16.1.0/24`, LAN B =
`10.1.1.0/24`. Los routers R1 (200.1.1.1) y R2 (200.1.1.2) están unidos por
Internet. Un host `H_A` (`172.16.1.5`) manda a `H_B` (`10.1.1.3`).

**Resolución — los dos encabezados, en cada punto del camino:**

```
   ═══ EN LA LAN A ═══
   ┌───────────────────────────────────────────────────────────┐
   │ ENCABEZADO INTERNO (el del paquete original):              │
   │   IP_or  = 172.16.1.5    IP_des = 10.1.1.3              │
   │   MAC_or = MAC(H_A)       MAC_des = MAC(R1)               │
   │   Protocolo = TCP, puerto 80                              │
   └───────────────────────────────────────────────────────────┘

   R1 lo encapsula:
   ┌───────────────────────────────────────────────────────────┐
   │ ENCABEZADO EXTERNO (el del túnel):                        │
   │   IP_or  = 200.1.1.1     IP_des = 200.1.1.2              │
   │   Protocolo = 47 (GRE)                                    │
   ├───────────────────────────────────────────────────────────┤
   │ ENCABEZADO INTERNO (el del paquete original):              │
   │   IP_or  = 172.16.1.5    IP_des = 10.1.1.3              │
   │   MAC_or = MAC(R1)        MAC_des = <next-hop en Internet>│
   └───────────────────────────────────────────────────────────┘

   ═══ EN INTERNET ═══
   Los routers de Internet MIRAN SOLO el encabezado externo:
   200.1.1.1 → 200.1.1.2. No saben ni les importa qué hay adentro.

   ═══ EN LA LAN B ═══
   R2 desenvuelve, quita el externo, y reencola:
   ┌───────────────────────────────────────────────────────────┐
   │ ENCABEZADO INTERNO:                                        │
   │   IP_or  = 172.16.1.5    IP_des = 10.1.1.3              │
   │   MAC_or = MAC(R2)        MAC_des = MAC(H_B)              │
   └───────────────────────────────────────────────────────────┘
```

**Lo que muestra este ejercicio:** la **dirección MAC cambia en CADA salto**
(porque es de capa 2), pero la **dirección IP origen/destino interna NO cambia
nunca** durante todo el túnel. El túnel **no es NAT**: no traduce, solo
encapsula.

## 2.2 Ejercicio 2 — Calcular qué capa corta cada ataque

**Enunciado.** Una red corporativa tiene: switches gestionables, un router de
borde con ACLs, un firewall con IPS, DNS interno, y HTTPS obligatorio por
política. ¿Qué ataques quedan contenidos y por qué?

**Resolución — la tabla de decisión:**

| Ataque | ¿Lo corta? | Por qué |
|---|---|---|
| **Sniffing** | ✅ | HTTPS obligatorio: todo el tráfico útil va cifrado. El cable es público. |
| **ARP poisoning** | ✅ | port security en los puertos de acceso +DAI: si una MAC aparece en dos puertos, se bloquea el puerto. |
| **Rogue DHCP** | ✅ | DHCP snooping: solo los puertos "confiables" (los de los uplinks) pueden ser servidores DHCP. |
| **IP spoofing** | ✅ | ACL anti-spoof en el borde + uRPF: `permit ip 172.16.0.0 0.0.0.255 any` en la interfaz interna. |
| **Secuestro BGP** | ✅ | RPKI: se valida el ROA del prefijo antes de aceptarlo. |
| **Secuestro DNS** | ✅ | DNS interno + DNSSEC hacia afuera + validación de SAN en HTTPS: si el DNS devuelve una IP de otro, el certificado no matchea y el navegador aborta. |
| **Rogue CA / MITM TLS** | ✅ | HTTPS obligatorio + **no instalar CAs** + CT logs. ★ Si el admin de la empresa instala una CA propia, eso es un backdoor. |
| **Ping of Death** | ✅ | el borde filtra paquetes con longitud o flags inválidos. |
| **Denegación de servicio (volumen)** | ❌ | **NINGÚN firewall lo detiene.** Si alguien te manda 100 Gbps, no hay defensa local. Se necesita upstream (anti-DDoS,anycast). |

> **La fila que hay que subrayar:** *la última. Un firewall **no** detiene un
> ataque de denegación de servicio por volumen, porque para hacerlo tendría que
> ser más rápido que el atacante. Eso se resuelve **aguas arriba**, en el
> proveedor de tránsito, con scrubbing o anycast. **Un IDS/IPS es una defensa de
> escritorio, no una defensa de infraestructura.***

## 2.3 Ejercicio 3 — Por qué un hash no da confidencialidad (demostración)

**Enunciado.** Beto tiene un hash de una contraseña. ¿Qué puede hacer un atacante?

**Resolución:**

```
   Sistema:   H(password) = SHA-256(password), almacenado.
   ─────────────────────────────────────────────────────────────
   SI el atacante tiene SOLO el hash:
     → PUEDE probar contraseñas contra el hash (ataque de
       diccionario). PEOR que con texto plano, porque
       no puede recuperar la original, pero SÍ puede
       verificar si una candidata es correcta.

   SI el atacante tiene el hash Y la contraseña:
     → el hash NO le dice cuál es la contraseña. Pero puede
       USAR EL HASH como si fuera la contraseña:
         · muchos sistemas comparan el hash del hash
           (el login hash H(password); si H' == H'
           comparando hashes, sirve);
         · sistemas con HASH COMO TOKEn: mandás el hash
           como contraseña y entrás.
       ★ Esto se llama "pass-the-hash".

   SI la contraseña es corta o común:
     → el atacante la saca en segundos (GPU: 10^10/s con SHA-256).

   ── LO QUE LO SOLUCIONA ──
   · SALT (salt): un valor aleatorio por usuario, concatenado
     antes del hash. H(password || salt). Hace que dos
     contraseñas iguales den hashes distintos.
   · KDF LENTO: bcrypt / scrypt / Argon2. 100 000× más lento
     que SHA-256. Una GPU que hace 10^10 SHA-256/s hace
     10^5 bcrypt/s: la diferencia ES la defensa.
```

> **Este ejercicio conecta con el WPA2 de la clase 43:** WPA2 con PSK suffers
> justamente del problema del (2): la contraseña se **deriva** y se puede atacar
> por **diccionario offline**. Y WPA3 con **SAE** resuelve **precisamente** eso:
> el protocolo de Dragonfly hace que **no se pueda verificar una contraseña
> candidata offline** a partir del handshake capturado. Es el mismo problema,
> resuelto con un protocolo en lugar de una KDF más lenta.

---

# PARTE 3 — PROBLEMAS DE EXAMEN DE FING

## 3.1 ⭐ Examen 2011-02, Problema 2 (30 puntos) — IP Móvil

> **Fuente:** Examen `sirc1102`, 3 de febrero de 2011.
> **Link:** https://www.fing.edu.uy/inco/cursos/redescomp/examenes/sirc1102.pdf

### Enunciado (resumen del original)

*Se tiene un nodo móvil (MN) que se mueve entre WLAN1+LAN1 y WLAN2+LAN2. El CN
está en LAN3. Se pide: (a) los campos MAC/IP de cada segmento cuando el paquete va
del MN al CN; (b) lo mismo cuando va del CN al MN, en cada modo de operación; y
(c) qué pasa con los campos IP según el modo.*

### Resolución — parte a) y b) en tabla

**Caso A: MN en WLAN1/LAN1, todo en su home network.**

```
   MN ──[WLAN1]── AP ──[LAN1]── R1 ──[LAN3]── CN
   (MN es      (bridging)        (rutea)
    local)
```

| Segmento | MAC origen | MAC destino | IP origen | IP destino |
|---|---|---|---|---|
| **WLAN1** | **MAC1** (MN) | **MAC4** (AP) | 172.172.0.17 | 203.203.203.3 |
| **LAN1** | **MAC1** (MN) | **MAC2** (R1) | 172.172.0.17 | 203.203.203.3 |
| **LAN3** | **MAC8** (R1) | **MAC9** (CN) | 172.172.0.17 | 203.203.203.3 |

**Lo que muestra la tabla:** la **IP origen/destino no cambia en ningún salto**
(es un paquete normal, MN y CN están "directamente visibles"). Lo único que cambia
es la **MAC**, en cada router (es de capa 2). En WLAN1 la MAC destino es la del
**AP** (porque la trama es **inalámbrica** y el primer salto es el AP). En LAN1 es
la de **R1**.

**Caso B: MN en WLAN2/LAN2, con foreign agent.**

| Segmento | MAC origen | MAC destino | IP origen | IP destino |
|---|---|---|---|---|
| **WLAN2** | MAC1 (MN) | **MAC7** (FA) | 172.172.0.17 | 203.203.203.3 |
| **LAN2** | MAC1 (MN) | MAC5 (router) | 172.172.0.17 | 203.203.203.3 |
| **LAN3** | MAC8 (R) | MAC9 (CN) | 172.172.0.17 | 203.203.203.3 |

**Ojo con la MAC destino del primer tramo:** es la del **foreign agent**, porque el
MN entra a la red foránea a través del FA. Y el CN **nunca** cambia su IP destino:
sigue siendo la **home address** del MN, porque el MN "se hace pasar" por estar en
casa.

### Resolución — parte c) y ii) el túnel

**El problema (que el enunciado pide resolver)**: cuando el MN está en la foreign
network y el CN quiere mandarle un paquete, lo manda a la **home address**. Ese
paquete viaja por Internet hasta el **HA**. El HA ve que el MN está registrado con
COA = `172.172.0.17`, así que debería reenviarlo ahí.

**El problema:** si el HA lo reenvía **sin túnel**, el paquete sale por la red
pública con destino `172.172.0.17` (una IP **privada**). Los routers de Internet
**no pueden rutear una IP privada** y **descartan** el paquete. O peor: el **next
hop** lo devuelve, y el paquete vuelve al HA: **un loop**, hasta que se descarta
por TTL.

**La solución: el túnel HA → FA.**

```
   El HA, en vez de mandar el paquete pelado al COA, lo ENCAPSULA:

   ┌──────────────────────────────────────────────────────┐
   │ ENCABEZADO DEL TÚNEL:                               │
   │   IP_or  = 111.1.1.1   (dirección PÚBLICA del HA)  │
   │   IP_des = 222.1.1.1   (dirección PÚBLICA del FA)  │
   ├──────────────────────────────────────────────────────┤
   │ ENCABEZADO INTERIOR (el paquete del CN):             │
   │   IP_or  = 203.203.203.3   (el CN)                  │
   │   IP_des = 172.172.0.17    (home address del MN)    │
   └──────────────────────────────────────────────────────┘

   ★ Ahora los routers de Internet PUEDEN rutear: 111.1.1.1 → 222.1.1.1
     son dos IPs públicas.
   ★ El FA desenvuelve y le entrega al MN (que está en su LAN interna).
```

**Y lo que dice la solución oficial sobre por qué el túnel no es "escalable":**

> *"…y es posible y escalable pues **sólo requiere la configuración de dos
> routers**."*

**El razonamiento completo:**

- Si en vez de túnel se quisiera "arreglar" el problema con **rutas estáticas** en
  todos los routers intermedios, haría falta configurar **cada router de la red
  del operador**, uno por uno. Eso es **NO escalable**: con 500 MN hay que
  mantener 500 rutas en cada router, y cada vez que un MN se mueve hay que
  actualizar todas.
- Con el **túnel**, el problema se resuelve en **los dos extremos** (HA y FA). Los
  routers intermedios no necesitan saber NADA: solo reenvían según su tabla, y la
  tabla dice "de 111.1.1.1 a 222.1.1.1, siguiente salto…". Eso ya existe porque es
  una conexión común entre dos puntos.

**Y los casos de la parte c), en tabla:**

```
   ┌──────────────┬──────────────────────────┬──────────────────────────┐
   │              │ MN → CN                  │ CN → MN                  │
   ├──────────────┼──────────────────────────┼──────────────────────────┤
   │ Caso A       │ IP_or = 172.172.0.17     │ IP_or = 203.203.203.3   │
   │ (en home)    │ IP_des = 203.203.203.3  │ IP_des = 172.172.0.17    │
   │              │ (normal, sin túnel)      │ (normal, sin túnel)      │
   ├──────────────┼──────────────────────────┼──────────────────────────┤
   │ Caso B       │ IP_or = 172.172.0.17     │ 1er tramo:               │
   │ (en foreign, │ IP_des = 203.203.203.3  │   IP_or = 203.203.203.3  │
   │  route       │ (sale directo a         │   IP_des = 172.172.0.17  │
   │  triangular)│  Internet, NO pasa por HA)│   (va al HA)             │
   │              │                          │ 2do tramo (túnel):       │
   │              │                          │   IP_or = 111.1.1.1 (HA) │
   │              │                          │   IP_des = 222.1.1.1 (FA)│
   │              │                          │   encapsula: CN → MN     │
   └──────────────┴──────────────────────────┴──────────────────────────┘
```

> **El detalle conceptual que hay que decir explícitamente:** el paquete **MN → CN**
> en el caso B **no pasa por el HA**. Sale directo del MN a Internet con destino
> el CN. Esto se llama **ruta triangular**: CN → HA → FA → MN (ida) y MN → CN
> directo (vuelta). **La asimetría es el problema**: el mismo paquete de ida y
> vuelta puede tomar caminos distintos, lo cual rompe la idea de "extremo a
> extremo". **Por eso existe el modo "correspondent"**: notificarle al CN la COA
> para que los dos caminos sean directos.

## 3.2 Examen 2008-12, Pregunta 3 (10 puntos) — arquitectura de IP Móvil

> **Texto del examen:** *Muestre e identifique en un diagrama topológico los
> componentes principales de la arquitectura IP Móvil, indicando el rol de cada
> uno de ellos.*

### Resolución — el diagrama que hay que dibujar (10 puntos, ~2 por elemento)

**El diagrama completo, que es lo que hay que hacer en el papel:**

```
                       ═══ INTERNET ═══
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
   ┌────┴─────┐         ┌─────┴────┐          ┌────┴────┐
   │  HOME    │         │          │          │    CN   │
   │  NETWORK │         │  (nodos  │          │ (corres-│
   │          │         │  en trán- │          │ pondent)│
   │ ┌──────┐ │         │   sito)   │          │  Node   │
   │ │  HA  │ │         │          │          │ 203.203.│
   │ │      │─┼─────────┤          │          │ 203.3   │
   │ └──────┘ │         │          │          └─────────┘
   │ ┌──────┐ │         │          │
   │ │  MN  │ │         │          │     ┌─────────────────┐
   │ │      │─┼─┐       │          │     │ FOREIGN NETWORK │
   │ └──────┘ │ │       │          │     │ ┌──────────┐   │
   └──────────┘ │       │          │     │ │    FA    │   │
      ▲        │       │          │     │ └────┬─────┘   │
      │        │       │          │     │ ┌────┴─────┐   │
   home addr   │       │          │     │ │    MN    │   │
  172.16.0.5  │       │          │     │ │ (care-of │   │
   (permanente)│       │          │     │ │  address)│   │
               │       │          │     │ └──────────┘   │
               │       │          │     │ 172.172.0.17   │
               └───────┼──────────┼─────┘  (temporal)    │
                       │          │           │
                    (ruta        │      registro del MN
                     triangular)  │           │
                                    └───────────┘
```

**La tabla de roles (5 elementos × 2 puntos):**

| Componente | Rol | En una frase |
|---|---|---|
| **MN** (*Mobile Node*) | el nodo que se mueve | tiene una **dirección permanente** (home) y una **temporal** (care-of). Se **registra** ante el HA y migra su dirección actual. |
| **HA** (*Home Agent*) | el router de la **red local** del MN | hace de **proxy**: recibe los paquetes destinados a la home address del MN y los **desvía** a través del túnel hacia el COA. |
| **FA** (*Foreign Agent*) | el router de la **red foránea** | **recibe** el registro del MN, le **asigna** (o le presta) la **care-of address**, y **notifica** al HA. |
| **CN** (*Correspondent Node*) | el otro extremo de la comunicación | habla con la **home address** del MN; en el modo "correspondent" se le **notifica** el COA para que el camino sea directo. |
| **Túnel** | el camino entre HA y FA | encapsula el tráfico del CN para que llegue al MN a través de la red del operador, **sin modificar los routers intermedios**. |

**Y los puntos que la cátedra suele agregar** (suman):

1. **El MN tiene DOS direcciones y eso es lo esencial**: la **permanente**
   (home address, asignada por la home network, no cambia nunca) y la
   **temporal** (care-of address, cambia cada vez que el MN cambia de red). La
   home address es la que "usa" el CN; el COA es la que "ve" la red.
2. **El binding tiene un TTL** (típicamente 300 s). El MN lo renueva
   periódicamente. Si no renueva, el HA **deja de desviar** y el MN tiene que
   re-registrarse. **Es lo mismo que el lease de DHCP**, aplicado a la
   mobilidade.
3. **Los tres modos** (simple, con foreign agent, correspondent) y que el
   "correspondent" es el único que elimina la ruta triangular pero es el más
   complejo.

## 3.3 Examen 2007-07, Pregunta 5 (5 puntos) — funcionamiento de IP Móvil

**Resolución.** Es la versión corta de §3.2, en cinco puntos:

1. El MN **sale** de su red local con su home address y **no se registra**
   con nadie todavía: simplemente se mueve.
2. Cuando llega a una red foránea, **obtiene una care-of address** (por DHCP, por
   SLAAC en IPv6, o del foreign agent si lo hay).
3. El MN **manda un Binding Update al HA**: "mi care-of address es X, con TTL de
   300 s". Si hay un FA en el medio, el Update pasa por él.
4. El HA **recibe, registra y acusa** (Binding Acknowledgement). **Desde este
   momento**, el HA sabe dónde está el MN.
5. Cuando llega un paquete del CN con destino = home address del MN, el HA lo
   intercepta (está en su red local), lo **encapsula en un túnel hacia el FA**
   (con destino = COA), y el FA lo entrega al MN.

> **Tope para 5 puntos:** los 5 pasos, con los nombres de los mensajes
> (Binding Update, Binding Ack, COA, home address) y quién se registra con quién.

---

# PARTE 4 — CIERRE DEL CURSO

## 📌 Resumen del Bloque F y del curso entero en 10 líneas

1. **TLS** = cifrado + integridad + autenticación + **forward secrecy**, con
   handshake de **1 RTT** en TLS 1.3. **443/TCP**. Cifra con **clave de sesión
   (EC)DH**, autentica con el **certificado**.
2. **SSH** = el mismo esquema con **PFS por claves efímeras**, **Ed25519** por
   defecto, y canal de control **multiplexado**.
3. **PGP** = cifrado **extremo a extremo** con **clave maestra separada** de la de
   cifrado; clave pública **verificada fuera de banda**.
4. **Túnel** = encapsular con **dos IP**, así el paquete cruza una red que no lo
   entiende. **Enrutado** (routers de Internet miran solo la IP externa) vs.
   **conmutado** (el switch mira MACs).
5. **IDS** avisa (en puerto espejo, no interrumpe); **IPS** bloquea (en línea, es
   punto único de falla). **DPI** abre y decodifica, y con cifrado requiere MITM
   o CA instalada.
6. **Ningún mecanismo de capa 2/3 es frontera de seguridad** — la única defensa
   real contra MITM es la **criptografía de la capa 7**.
7. **IP Móvil**: MN, HA, FA, CN; home address + care-of address; el HA hace de
   **proxy** y desvía por un **tunnel** hacia el FA; **ruta triangular** es el
   problema central y el túnel lo resuelve **sin tocar los routers intermedios**.
8. En 2026, **IP Móvil no se desplegó**: lo reemplazaron **VPN + QUIC migration**
   + el **Connection ID**, que saca la identidad de la IP.
9. **Punto de corte por capa**: capa 2 → port security/DAI/DHCP snooping;
   capa 3 → ACL/uRPF/RPKI; capa 7 → **TLS** (la única real).
10. **La idea que cierra el curso**: cada capa resuelve un problema y crea otro;
    la seguridad de una red es la **suma de las defensas**, y la única que no se
    puede rodear es la que **no depende de la red**: la criptografía de extremo a
    extremo.

## 🔑 Mapa final del curso — dónde está cada cosa

```
   ┌────────────────────────────────────────────────────────────┐
   │ BLOQUE A — Fundamentos (1-7)                               │
   │   qué es una red · OSI/TCP-IP · encapsulación ·           │
   │   store-and-forward · retardo · Nyquist-Shannon            │
   ├────────────────────────────────────────────────────────────┤
   │ BLOQUE B — Aplicación (8-15)                               │
   │   HTTP/1.1 · DNS · correo · sockets · DHCP                 │
   ├────────────────────────────────────────────────────────────┤
   │ BLOQUE C — Transporte (16-23)                              │
   │   UDP · TCP cabecera · handshake · confiabilidad ·        │
   │   flujo vs. congestión · ECN                              │
   ├────────────────────────────────────────────────────────────┤
   │ BLOQUE D — Red (24-37)                                     │
   │   forwarding/routing · datagramas vs. VC · IPv4 ·          │
   │   subnetting · VLSM · tablas/ARP · NAT/PAT ·              │
   │   distance-vector · link-state/OSPF · BGP · MTU · IPv6    │
   ├────────────────────────────────────────────────────────────┤
   │ BLOQUE E — Enlace (38-43)                                  │
   │   framing · errores (detección/corrección/ARQ) ·           │
   │   acceso al medio · switch/VLAN/STP · WiFi 802.11          │
   ├────────────────────────────────────────────────────────────┤
   │ BLOQUE F — Servicios (44-48)                               │
   │   multimedia/RTP · QoS/MPLS · SNMP/NETCONF ·               │
   │   criptografía · seguridad aplicada + IP Móvil              │
   └────────────────────────────────────────────────────────────┘

   Y LAS CONEXIONES QUE HAY QUE TENER PRESENTES:

   · TCP  ──────→  congestion → bufferbloat → QOS (clase 45)
   · ARP  ──────→  switch → VLAN → STP → wireless (38-43)
   · subnetting ─→  VLSM → planes de numeración → BGP (26-34)
   · DNS   ─────→  caché → seguridad (DNSSEC) → Internet (10-13, 47)
   · sockets ───→  servidor/cliente → DHCP → HTTP → correo (14-15)
   · hash  ─────→  firma → PKI → TLS → SSH/PGP (47-48)
   · mobility ──→  QUIC → connection ID → NAT rebinding (48)
```

---

## 📝 SIMULACRO FINAL — Examen completo

> **Instrucciones del examen real:** 3 horas · sin material · individual ·
> **puntaje mínimo de aprobación: 60/100** · **obligatorio responder
> correctamente al menos 15 puntos en las preguntas teóricas**.
> **5 preguntas teóricas (~40 pts) + 2 problemas prácticos (30 pts c/u).**

### Preguntas teóricas

**Teórica 1 (10 puntos).** Un usuario en una red con WiFi abre el navegador y
escribe `https://www.ejemplo.com`. Describa, en orden, **todos** los pasos desde
que aprieta Enter: qué protocolos participan, qué se resuelve primero, qué
cifrado se establece, y qué pasa si alguno de ellos falla. Sea específico sobre
los **mensajes** de cada protocolo.

**Teórica 2 (10 puntos).** Describa cómo se **enruta** un paquete entre dos redes
distintas: (a) el papel de forwarding y enrutamiento, (b) por qué la tabla ARP es
necesaria en cada salto, (c) qué pasa si la tabla ARP no tiene la entrada
destino, y (d) qué diferencia hay entre enrutamiento **distance-vector** y
**link-state**.

**Teórica 3 (8 puntos).** Explique cómo se implementa la **confiabilidad** en la
capa de transporte, y por qué **no se puede implementar igual** en la capa de
enlace en una red de paquetes arbitraria. Mencione los mecanismos concretos de TCP.

**Teórica 4 (8 puntos).** Explique qué es una **función de hash**, qué servicios de
seguridad aporta, y por qué **una firma digital necesita combinar** un hash con un
cifrado **asimétrico** (y no puede usar solo un hash, ni solo un MAC).

**Teórica 5 (4 puntos).** Mencione **cuatro ataques** típicos a redes de
computadoras y, para cada uno, indique **en qué capa** se produce y **qué mecanismo
de defensa** lo mitiga.

### Problemas prácticos

**Problema 1 (30 puntos).** Una red está compuesta por **tres subredes**
interconectadas por los routers **R1** y **R2**, tal como se muestra en la figura:

```
     Subred A (clase C)          Subred B (clase C)        Subred C (clase C)
   ┌──────────────────┐      ┌──────────────────┐      ┌──────────────────┐
   │  H_C    R1       │      │  R1       R2     │      │  R2       H_F     │
   │ .3  ── .1        │══════│ .2 ────── .1     │══════│ .2 ────── .4      │
   │      (R1: .1/.2) │      │                  │      │                  │
   └──────────────────┘      └──────────────────┘      └──────────────────┘
```

Las tres subredes son clase C. Los routers R1 y R2 tienen **dos interfaces** cada
uno (una por subred). El enrutamiento es **estático**. Las direcciones MAC se
indican en la tabla del enunciado original.

Se pide:

a) Para la topología:
   i) Las **tablas de enrutamiento** de R1 y R2 que dan conectividad extremo a
   extremo.
   ii) Las **tablas de enrutamiento de los hosts**.
   iii) El **intercambio de tramas** para mandar un paquete de H_C a H_F,
   indicando `{MAC_or, MAC_des, IP_or, IP_des, protocolo, tipo}` en **cada** salto,
   **suponiendo las tablas ARP vacías**.

b) Se reemplaza el **R2 por un switch** que une las subredes B y C, sin cambiar
   las direcciones IP.
   i) La nueva tabla de enrutamiento de R1, **justificando** las modificaciones.
   ii) Las nuevas tablas de los hosts. Qué cambios de configuración hacen falta.
   iii) **Comparar** la nueva topología con la original: ventajas y desventajas.

**Problema 2 (30 puntos).** Se desea implementar un **protocolo de
transferencia de datos confiable** en una red donde **todos los nodos son
alcanzables por broadcast**, con estas características:

- Debe poder transferir datos **simultáneamente** de un computador a todos los demás.
- En cada momento, la capa de aplicación debe haber recibido los datos de los
  **mismos `n` paquetes**, pudiendo diferir solo en los del paquete `n+1`
  (**entrega ordenada**).
- Debe recuperarse de fallos de transmisión y eliminar duplicados.
- **No** tendrá control de congestión.
- **No** tendrá control de flujo.

Primitivas disponibles: `rdt_send(datos)`, `udt_send_broadcast(pkt)`,
`rdt_rcv(pkt)`, `deliver_data(datos)`.

Se pide:

a) Diseñe el protocolo: qué campos lleva el **encabezado** de cada paquete y por
   qué (**justifique cada uno**).

b) Implemente el procedimiento de **emisión** del emisor y de **recepción** del
   receptor, en pseudocódigo.

c) Explique cómo se garantiza la **entrega ordenada** y la **eliminación de
   duplicados** en cada caso: **pérdida de un ACK**, **duplicado de un paquete de
   datos**, y **pérdida del propio paquete de datos**.

### Cronómetro sugerido

| Momento | Minutos | Qué hacer |
|---|---|---|
| 0:00 – 0:10 | 10 | leer TODO, elegir qué problemas hacer, decidir si hacés los 2 |
| 0:10 – 0:55 | 45 | **las 5 teóricas** (8-10 min cada una) |
| 0:55 – 1:55 | 60 | **Problema 1** |
| 1:55 – 2:55 | 60 | **Problema 2** |
| 2:55 – 3:00 | 5 | releer, corregir, completar cotas |

> **Recordá:** el mínimo es **60/100** **Y ≥15 pts en las teóricas**. Si te quedás
> sin tiempo para los problemas, todavía aprobás: **no abandones las teóricas**.

<details>
<summary><b>✅ RESPUESTAS DEL SIMULACRO FINAL</b></summary>

#### Teórica 1 (10 pts)

| # | Paso | Detalle | RTT |
|---|---|---|---|
| 1 | **DHCP** | si no tiene IP: DORA (4 mensajes, broadcast, UDP 68→67) | 4 × RTT |
| 2 | **DNS** | el resolver pregunta por `www.ejemplo.com` tipo A. El stub resolver consulta **iterativamente** al recursivo, que consulta a root → TLD → autoritativo | 0 a 4 |
| 3 | **ARP** | el host resuelve la MAC del gateway (para salir a Internet). ARP es **broadcast** en la LAN local | 1 |
| 4 | **TCP** | 3-way handshake con el servidor en el **443** | 1 |
| 5 | **TLS 1.3** | ClientHello (con key_share) → ServerHello + Certificate + CertificateVerify + Finished → Finished. **1 RTT** total | 1 |
| 6 | **HTTP GET** | `GET / HTTP/1.1` por el canal cifrado | — |
| 7 | **render** | el navegador pide CSS/JS/imágenes, cada uno por el mismo canal (o abre nuevos) | varios |

**Si algo falla:**

- **DHCP falla** → el host se autoconfigura en `169.254/16`, **no puede salir** de la LAN y no navega.
- **DNS falla** → error de navegación; si es un timeout **no** se cachea, y si es NXDOMAIN **sí** (con TTL negativo).
- **ARP falla** → no hay conexión local; timeout.
- **TCP falla** → si el puerto está cerrado, **RST** (conexión **refusada**, rápida); si hay un firewall que descarta, **timeout** (lento). Es una distinción clave.
- **TLS falla** → si el **certificado no valida** (cadena rota, SAN distinto, vencido), el navegador **aborta**: es la defensa contra el MITM.
- **404** → el servidor respondió, no tiene el objeto. **No es un fallo de red.**

> **Tope para 10:** los 7 pasos en orden, con los mensajes nombrados (DORA, 3-way, 1-RTT de TLS 1.3), y la distinción entre **conexión rechazada (RST)** y **timeout**.

#### Teórica 2 (10 pts)

**(a) Forwarding vs. enrutamiento.** El **enrutamiento** es el **proceso** (en un
router, algoritmo como RIP/OSPF/BGP) que **decide** la tabla: qué destino va por
qué interfaz. El **forwarding** es la **acción** de, paquete por paquete, **buscar
el prefijo más largo** en esa tabla y moverlo de la interfaz de entrada a la de
salida. El enrutamiento **genera** la tabla; el forwarding la **usa**.

**(b) Por qué ARP en cada salto.** El paquete IP **solo cambia la MAC**; la IP
origen/destino **no cambia** de punta a punta (salvo NAT o encapsulación). Pero en
**cada tramo de red local**, el paquete va dentro de una **trama** que necesita
**MAC destino** (la del siguiente salto). Y esa MAC hay que **resolverla con ARP**.
Por eso hay un ARP **por salto**: en la red local A, en la B, en la C.

**(c) Si la tabla ARP no tiene la entrada.** ARP **envía un broadcast**
("¿quién tiene esta IP?") y **espera**. Si nadie responde en unos segundos, se da
por **no alcanzado** (ARP **no reintenta** indefinidamente) y se genera un error.
Ojo: ARP **no tiene reintentos ni ACK** — es de la familia UDP en ese sentido.

**(d) Distance-vector vs. link-state.**

| | **Distance-vector** | **Link-state** |
|---|---|---|
| Qué manda | el **vector de distancias** a sus vecinos | el **estado completo del grafo** (LSDB) a **todos** |
| Cómo calcula | Bellman-Ford: `D(x,v) = min_u [ D(u,v) + c(u,x) ]` | **Dijkstra** sobre su propia LSDB |
| Cuántos таблиas | **una por nodo**, con los vectores de los vecinos | **una LSDB completa por nodo** |
| Sabe la topología | **no**: solo lo que le dicen sus vecinos | **sí**: la tiene todos |
| Convergencia | **lenta**: "count to infinity", muy lento | **rápida** |
| Si algo se rompe | puede generar **bucles** hasta que converja | recalcula rápido, **topología consistente** |
| Escala | **no** (RIP ≤15 saltos) | **sí** (OSPF, IS-IS en backbone) |

> **Tope para 10:** (a) la distinción proceso/acción y la tabla de forwarding; (b)
> la IP no cambia pero la MAC sí, por eso ARP por salto; (c) el broadcast y que
> **ARP no reintenta**; (d) la tabla con al menos 4 filas y el "count to infinity"
> como ejemplo de por qué DV no escala.

#### Teórica 3 (8 pts)

**Los mecanismos concretos de TCP** (nombres, que es lo que suma):

1. **Número de secuencia** (32 bits) y **ACK** (ACK cumulativo: "espero el byte
   `n`). Detecta **pérdida y desorden**.
2. **Suma de verificación** (checksum) de **todo** el segmento (cabecera + datos).
   Detecta **corrupción**.
3. **Retransmisión por **timeout** (RTO, derivado de RTT y su varianza) y
   por **3 ACKs duplicados** (**fast retransmit**, que dispara al recibir 4 ACKs
   para el mismo byte).
4. **Ventana deslizante** y **control de flujo** (ancho de banda receptor → el
   receptor avisa su ventana en cada ACK, TCP usa el campo `window`).
5. **Control de congestión** (slow start, AIMD, fast recovery) — es control de
   congestión, no de flujo: el emisor, no el receptor.

**Por qué no se puede en la capa de enlace** (esta es la parte conceptual, y es
exactamente lo que pregunta el `2009-12 P2`):

1. **En la capa de enlace solo se conhece al vecino inmediato.** No hay
   información de la red completa. En capa de enlace, "reliable" significa "este
   **enlace** no pierde tramas", **no** "el camino completo no pierde".
2. **Los buffers de los routers son finitos y no son del emisor.** El campo
   `WindowScale` de TCP lo negocia el **receptor final**. En la capa de enlace, el
   router **no tiene** un campo para decirte "mis buffers están llenos".
3. **El reintento extremo a extremo en capa de enlace es imposible si la ruta
   cambia** (un router puede reenviar por otro camino, con **TTL** y loops). El
   *acknowledgment* de enlace solo cubre **un salto**.
4. **Los enlaces de la red pública no ofrecen servicio confiable**: un enlace
   celular o satelital pierde tramas legítimamente, y el router de la mitad del
   camino **no va a retransmitir** porque eso es trabajo del origen.

> **Tope para 8:** los mecanismos nombrados (seq, ACK, checksum, timeout y
> fast-retransmit, ventana deslizante), y las razones de por qué **enlace ≠
> transporte** (solo vecino, sin control de flujo extremo a extremo, buffers ajenos,
> ruta cambiante).

#### Teórica 4 (8 pts)

**Hash** = función que mapea un mensaje de cualquier tamaño a una salida de
tamaño fijo, con: determinismo, unidireccionalidad, **resistencia a colisiones**,
y **avalancha**. Ejemplo: **SHA-256**.

**Servicios que aporta: SOLO integridad.** Detecta que el mensaje cambió
(porque el hash cambió), y nada más:
- **No confidencialidad**: el hash no oculta nada.
- **No autenticidad**: cualquiera puede calcularlo, no lleva clave.
- **No no repudio**: igual, cualquiera puede hashear cualquier mensaje.

**Por qué la firma necesita hash + asimétrico:**

- **Un hash solo no firma**: cualquiera calcula `H(m)` y lo pega al mensaje.
  No prueba quién lo hizo.
- **Un cifrado simétrico (MAC) tampoco**: para verificar, el receptor necesita la
  clave compartida; si la tiene, **también puede firmar**. **Verificar y firmar
  serían la misma operación** → **no hay no-repudio**.

**La firma digital** (RSA-PSS / ECDSA / Ed25519):

```
   Firmar:    σ = Sign(misma_clave_privada, H(m))     ← firma el HASH
   Verificar: 1) ¿σ valida con kp? (autenticidad)
              2) ¿H(m) recibido == el H(m) firmado?    (integridad)
              3) Solo el dueño de la clave privada puede firmar
                 → no repudio
   ★ Y NO cifra: el mensaje va en claro con la firma al lado.
```

Se firma el **hash** y no el mensaje por **eficiencia** (el hash es de 32 bytes,
sea cual sea el tamaño del mensaje), por **longitud fija** de la firma, y por
**no filtrar** el tamaño del secreto.

> **Tope para 8:** la definición con las 4 propiedades, el "solo integridad" con las
> 3 razones, y la firma como hash + clave privada, con el "no cifra" explícito.

#### Teórica 5 (4 pts)

| Ataque | Capa | Defensa |
|---|---|---|
| **Sniffing / eavesdropping** | 2/3/7 | **Cifrado (TLS/HTTPS)** — la única real; nunca confíes en el cable |
| **ARP poisoning / spoofing** | 2 | **port security + DAI + DHCP snooping + VLAN** |
| **IP spoofing** | 3 | **ACL anti-spoof + uRPF (BCP 38)** en el borde |
| **Secuestro BGP** | 3 | **RPKI / ROA** (validar que el prefijo esté autorizado) |

Se pueden mencionar también: **MAC flooding** (port security), **rogue CA /
MITM TLS** (validación de cadena + SAN + CT logs), **secuestro DNS** (DNSSEC),
**pharming** (DNSSEC + HTTPS).

> **Tope para 4:** 4 ataques, cada uno con capa y defensa. Añadir la frase clave:
> *la única defensa que **no depende de la red** es la criptografía de la capa de
> aplicación; todo lo demás es defensa en profundidad.*

#### Problema 1 (30 pts)

**(a-i) Tablas de enrutamiento de R1 y R2** (con la figura del enunciado):

**R1** (interfaz A = .1 en subred A, interfaz B = .2 en subred B):

| Red destino | Next-hop | Interfaz |
|---|---|---|
| Subred A (directa) | — | A (.1) |
| Subred B (directa) | — | B (.2) |
| **Subred C** | **R2 (.1 en B)** | **B (.2)** |

**R2** (interfaz B = .1 en subred B, interfaz C = .2 en subred C):

| Red destino | Next-hop | Interfaz |
|---|---|---|
| Subred B (directa) | — | B (.1) |
| Subred C (directa) | — | C (.2) |
| **Subred A** | **R1 (.2 en B)** | **B (.1)** |

**Lo clave:** cada router tiene **3 entradas**: las 2 redes directas y la **1 ruta
estática** hacia la red que queda "al otro lado". Es el **mínimo** para
conectividad extremo a extremo.

**(a-ii) Tablas de los hosts** (por ejemplo, H_C en la subred C):

| Red destino | Next-hop | Interfaz |
|---|---|---|
| Subred C (directa) | — | eth0 |
| Subred B | **R2 (.2 en C)** | eth0 |
| **Subred A** | **R2 (.2 en C)** | eth0 |

**Y H_A en A:**

| Red destino | Next-hop |
|---|---|
| Subred A | directa |
| Subred B | **R1 (.1 en A)** |
| **Subred C** | **R1 (.1 en A)** |

> **El host NUNCA pone "siguiente salto" que no sea de su propia red**: pone el
> **gateway por defecto**. Los hosts no rutean; delegan.

**(a-iii) El intercambio de tramas de H_C a H_F** (ARP vacío). Supongamos que
subred C = `192.168.3.0/24`, H_C = `.3`, R2 en C = `.2`, R2 en B = `.1`, R1 en B
= `.2`, R1 en A = `.1`, subred A = `192.168.1.0/24`, H_F = `.4`.

**Paso 0 — ARP de H_C para conocer la MAC de R2 (.2 en C):**

```
   MAC_or  = MAC(H_C)
   MAC_des = FF:FF:FF:FF:FF:FF     (broadcast)
   Tipo    = ARP Request: "¿quién tiene 192.168.3.2? Decime tu MAC."
   ┌──────────────────────────────────────────────────┐
   │  IP_or  = 192.168.3.3        (H_C)               │
   │  IP_des = 192.168.3.2        (¿quién?)           │
   └──────────────────────────────────────────────────┘

   R2 responde (unicast):
   MAC_or = MAC(R2_c)   MAC_des = MAC(H_C)
   ┌──────────────────────────────────────────────────┐
   │  IP_or = 192.168.3.2     IP_des = 192.168.3.3   │
   │  MAC solicitada = MAC(H_C)                        │
   └──────────────────────────────────────────────────┘
```

**Trama 1 — H_C → R2 (el paquete entra en la red):**

```
   MAC_or = MAC(H_C)      MAC_des = MAC(R2_c)         ← MAC del gateway
   ┌──────────────────────────────────────────────────┐
   │  IP_or  = 192.168.3.3    IP_des = 192.168.1.4   │  ← IP destino = FINAL
   │  TTL = 64 (H_C lo inicializa)                    │
   └──────────────────────────────────────────────────┘
```

**ARP en R2 para conocer R1 (.2 en B):** R2 hace ARP **en la subred B** por
`192.168.2.2` (la interfaz de R1 en B). R1 responde.

**Trama 2 — R2 → R1:**

```
   MAC_or = MAC(R2_b)      MAC_des = MAC(R1_b)
   ┌──────────────────────────────────────────────────┐
   │  IP_or  = 192.168.3.3    IP_des = 192.168.1.4   │  ← ¡IGUAL!
   │  TTL = 63    ← R2 decrementa                     │
   └──────────────────────────────────────────────────┘
```

**ARP en R1 para conocer H_F (.4 en A):** R1 hace ARP **en la subred A** por
`192.168.1.4`. H_F responde.

**Trama 3 — R1 → H_F:**

```
   MAC_or = MAC(R1_a)      MAC_des = MAC(H_F)
   ┌──────────────────────────────────────────────────┐
   │  IP_or  = 192.168.3.3    IP_des = 192.168.1.4   │  ← ¡IGUAL!
   │  TTL = 62    ← R1 decrementa                     │
   └──────────────────────────────────────────────────┘
```

**Las tres observaciones que hay que escribir** (son los puntos):

1. **La IP origen y destino NO cambian** en ningún salto (H_C a H_F): eso es
   **extremo a extremo**, sin NAT.
2. **La MAC cambia en CADA salto**, porque la trama es de capa 2 y cada tramo es
   un enlace distinto.
3. **El TTL se decrementa** en cada router. Si en 64 saltos no llegara, se
   descarta (y el emisor recibe un **ICMP Time Exceeded**).

**(b-i) R2 → switch.** Si se reemplaza R2 por un switch, las subredes B y C quedan
**en el mismo dominio de broadcast** (el del switch). Ahora **R1 solo tiene que
conocer a los hosts de B y C**, no la subred B "a través de R2".

Nueva tabla de **R1**:

| Red destino | Next-hop | Interfaz |
|---|---|---|
| Subred A (directa) | — | A |
| **Subred B y C (juntas)** | — | **B, directa** |

> **La justificación clave:** al ser un switch, las subredes B y C comparten el
> mismo segmento. Por eso R1 tiene una sola ruta directa hacia **ambas**, y no
> necesita next-hop. La ruta "estática" a la subred C **desaparece**, porque ahora
> es **directa** desde R1.

**(b-ii) Tablas de los hosts.** H_C ahora tiene **gateway = el switch (que no
rutea)**, no R2. Lo que corresponde es poner el **gateway por defecto = la interfaz
de R1 en B**, para salir a otras redes, y para llegar a H_F (misma subred) **no
necesita gateway**: resuelve por ARP directo.

**(b-iii) Ventajas y desventajas de la nueva topología:**

| | Original (R2 rutea) | Nueva (switch) |
|---|---|---|
| **Aislamiento de fallos** | R2 caído = **toda** la red B-C se cae | Switch caído = **toda**, igual (pero el switch es más barato) |
| **Dominio de broadcast** | 2 dominios separados | **1 solo** → más broadcasts, más carga |
| **Cantidad de subtredes** | **Conserva el aislamiento** (una subred por red lógica) | **Pierde el aislamiento** (una sola red lógica) |
| **Seguridad** | Better: separa redes lógicas | Peor: todo está en el mismo dominio |
| **Tráfico** | 2 saltos para ir de B a C (B→R2→C) | **1 salto** (más eficiente) |
| **Costo** | R2 es un router (caro) | Un switch (barato) |

> **Tope para 30:** (a) las 3 tablas con next-hop e interfaz; (b-iii) la
> comparación con al menos 4 filas. La observación de que **el switch no es una
> frontera de seguridad y no aísla dominios de broadcast** es la que más suma.

#### Problema 2 (30 pts)

**(a) Encabezado del paquete de datos** (justificando cada campo):

```
   ┌──────────────┬──────────────┬──────────────┬──────────────┬───────────┐
   │  seq  (n)    │  ack  (m)    │   flags      │   datos      │  CRC      │
   │  # de seq.   │  # confirmado│  (datos?)    │  (payload)   │  (cifrado)│
   └──────────────┴──────────────┴──────────────┴──────────────┴───────────┘
```

| Campo | Función | Por qué |
|---|---|---|
| **`seq`** (número de secuencia) | identifica **qué** paquete es | para **detectar pérdida** y **desorden** |
| **`ack`** (número de ACK) | dice "**recibí hasta acá**" (cumulativo) | para **confirmar** y para **detectar pérdida** |
| **`flags`** | marca **tipo** de mensaje: `DATA`, `ACK`, `NAK` | para distinguir qué hacer con el mensaje |
| **`datos`** | la carga útil | el contenido |
| **`CRC`** | detección de **errores de transmisión** | el broadcast no garantiza integridad |

**Y el mensaje de ACK**, que va **separado** (o piggybacked, si es_full duplex):

```
   ┌──────────────┬──────────────┬───────────┐
   │  ack  (m)    │  flags=ACK   │   CRC     │
   │ "llegué a m" │              │           │
   └──────────────┴──────────────┴───────────┘
```

**(b) Emisor:**

```pseudocode
procedure emitir(datos)
{
    seq = 0
    pending = vacía

    while (hay datos que enviar)
    {
        paquete = construir(seq, 0, DATA, datos)
        pending.agregar(paquete)
        udt_send_broadcast(paquete)

        esperar_ack_o_timeout()

        while (not pendiente.ack_recibido)
        {
            retransmitir el paquete más viejo de pending
            esperar_ack_o_timeout()
        }
        seq++
    }
}

procedure al_recibir_ack(m)
{
    // ack cumulativo: elimina TODOS los pendientes hasta m
    pending.eliminar_hasta(m)
}
```

**Receptor:**

```pseudocode
procedure recibir()
{
    esperado = 0
    buffer = vacío

    while (true)
    {
        pkt = rdt_rcv(buffer)

        if (pkt == NULL)      // timeout: reintentar leer
            continue

        if (CRC(pkt) == ERROR)
        {
            udt_send_broadcast(construir(esperado, 0, NAK))
            continue
        }

        if (pkt.flag == DATA)
        {
            if (pkt.seq < esperado)
            {
                // DUPLICADO: ya lo tengo. re-confirmo.
                udt_send_broadcast(construir(pkt.seq, 0, ACK))
            }
            else if (pkt.seq == esperado)
            {
                // EN ORDEN: lo entrego
                deliver_data(pkt.datos)
                esperado++
                // confirmo
                udt_send_broadcast(construir(esperado, 0, ACK))
            }
            else
            {
                // FALTA ALGO: pkt.seq > esperado → hay un hueco
                // pido que me reenvíen desde `esperado`
                udt_send_broadcast(construir(esperado, 0, NAK))
                // NO lo entrego todavía: para mantener el orden
            }
        }
    }
}
```

**Lo que hay que justificar (esto es lo que da los 30 puntos):**

- **El `ack` es CUMULATIVO** (no individual): si recibo `ack(m)`, recibo **todo
  hasta `m`**. Así se evita un ACK por cada paquete, y es exactamente lo que hace
  TCP.
- **El emisor guarda `pending`** (los enviados sin confirmar) para poder
  **retransmitir** los que se perdieron.
- **El receptor usa `esperado`** para **entregar en orden**: si recibe `seq > esperado`,
  **no lo entrega** (entregaría fuera de orden) y manda un **NAK** pidiendo el
  que falta.

**(c) Los tres casos:**

**Caso 1 — Se pierde un ACK.** El emisor **no lo sabe** (no hay confirmación de
llegada del ACK). Después del **timeout**, retransmite el paquete. El receptor lo
recibe con `seq < esperado` → lo detecta como **duplicado**, **NO lo vuelve a
entregar**, y **re-confirma** con un ACK. **Se pierde eficiencia, no corrección.**

**Caso 2 — Se duplica un paquete de datos.** El receptor ve `pkt.seq < esperado` →
sabe que ya lo entregó → **lo descarta** y **re-confirma**. La **eliminación de
duplicados** la da el número de secuencia (`esperado`): todo lo que tenga `seq <
esperado` ya salió.

**Caso 3 — Se pierde el propio paquete de datos.** El receptor ve que falta un
número (si recibe el `n+1` antes que el `n`, detecta el hueco) → manda un **NAK
por `esperado`**, y el emisor (que tiene `esperado` en `pending`) lo retransmite.
Si el emisor ya no tiene nada en `pending` (porque el ACK anterior cubrió ese paquete), espera el
**timeout** y reenvía. **Y si no hay NAK, el próximo paquete que llegue con hueco
también dispara un NAK.**

> **Tope para 30:** (a) el encabezado con 5 campos justificados, (b) los dos
> procedimientos en pseudocódigo con el `ack` cumulativo y `pending`, (c) los 3
> casos con qué pasa en emisor y receptor. La clave de cada caso: pérdida de ACK →
> timeout + duplicado descartado; duplicado → `seq < esperado`, no se entrega;
> pérdida de datos → hueco detectado → NAK.

</details>

## ✅ Autoevaluación

Respondé sin mirar. Las respuestas están en `<details>`.

**1.** ¿Qué clave cifra los datos en TLS 1.3? ¿Y para qué sirve la clave que va
en el certificado?

<details><summary>Respuesta</summary>

**La clave de sesión simétrica**, acordada por **(EC)DHE** (X25519 en la práctica)
derivada con HKDF, es la que cifra los datos de aplicación. **Nunca se transmite**:
los dos la calculan a partir del secreto compartido.

**La clave pública del certificado no cifra los datos**: se usa para **autenticar
al servidor**. El servidor firma con su privada, el cliente verifica con la pública
del certificado, y eso descarta el *man-in-the-middle*.

En TLS 1.2 la clave del certificado tenía **dos** usos: autenticar **y** cifrar el
*pre-master secret*. En **TLS 1.3 el transporte de clave con RSA fue eliminado**
(`RFC 8446`): todo el secreto se negocia con (EC)DHE.

</details>

**2.** ¿Por qué un IDS y un IPS son decisiones distintas y no se pueden
sustituir?

<details><summary>Respuesta</summary>

Porque **están en puntos distintos de la red y resuelven problemas distintos**.

El **IDS** va en un **puerto espejo** (*span port*): ve una **copia** del tráfico,
no lo toca. **No puede bloquear nada**, pero **tampoco puede romper nada**: si el
IDS falla o se cuelga, lo único que se pierde es visibilidad. Su salida es una
**alerta** a un operador.

El **IPS** va **en línea** (*inline*): es parte del camino. **Puede bloquear**, y por
eso es mucho más eficaz contra un ataque en curso. Pero es un **punto único de
fallo**: si se cuelga, o el tráfico pasa (*fail-open*, menos seguro) o se corta todo
(*fail-close*, se cae el servicio legítimo). Y es un **cuello de botella de
rendimiento**, porque tiene que analizar **todo** el tráfico.

La respuesta completa: **se usan los dos, en paralelo** — IDS para visibilidad y
para el análisis forense posterior, IPS para la defensa en tiempo real.

</details>

**3.** ¿Por qué el túnel de IP Móvil es escalable y las rutas estáticas en los
routers intermedios no?

<details><summary>Respuesta</summary>

Porque **el túnel se resuelve en los dos extremos**.

El problema: el HA tiene que hacer llegar un paquete al MN, cuya **care-of address**
(`172.172.0.17`) es una **IP privada**. Los routers de Internet **no rutean IPs
privadas**: la descartan o la devuelven al remitente, generando un **loop** hasta
que el TTL lo mate.

**Rutas estáticas**: para arreglarlo habría que **programar cada router de la red
del operador** para que sepa que "de la red del MN a la IP privada hay que seguir
por esta interfaz". Con 500 MNs, son 500 rutas **por router**, y cada vez que un MN
se mueve hay que **actualizar todos los routers**. Eso es **inmantenible**.

**Túnel**: el HA le pone **un encabezado IP extra** al paquete, con origen = la IP
**pública** del HA y destino = la IP **pública** del FA. Ahora los routers de
Internet rutean normal: solo ven "de 111.1.1.1 a 222.1.1.1", que ya es una ruta
que existe. El FA quita el encabezado externo y entrega el original al MN.

Se configura **una vez** en el HA y **una vez** en el FA. Los routers intermedios
**no se tocan**. Eso es escalable.

</details>

**4.** ¿Qué es el *forward secrecy* y por qué en TLS se logra con (EC)DHE y no con
RSA?

<details><summary>Respuesta</summary>

**Forward secrecy** significa que **el secreto de la sesión no se puede recuperar
después**, aunque alguien se quede con el material del servidor **hoy**.

**Cómo se logra en TLS 1.3:** las claves de sesión se derivan de un **intercambio
(EC)DHE efímero**. Cada sesión usa claves públicas **nuevas**, que se descartan al
terminar. El servidor **nunca guarda** el secreto compartido. Por eso, si te
entregan el disco forense del servidor **ahora**, **no podés descifrar** lo que se
habló **ayer**: las claves privadas nunca existieron juntas dos veces.

**Por qué no con RSA:** en el TLS antiguo, el *pre-master secret* venía cifrado con
la clave pública del servidor y **quedaba guardada en el servidor** para poder
descifrar las sesiones. Si te AGREDA el servidor, tenías las claves y podías
descifrar **todo el histórico**. RSA **no da forward secrecy** por sí solo.

La misma regla aplica a Diffie-Hellman: **estático no da FS** (ataque Logjam),
**efímero sí**.

</details>

**5.** ¿Qué diferencia hay entre sniffing y ARP poisoning en términos de capa y
de defensa?

<details><summary>Respuesta</summary>

**Sniffing** es un ataque **pasivo**: te ponés a escuchar. No modifica nada, no
genera tráfico, y es **indetectable** para la víctima. Vive en **capa 2/3** (el
medio compartido) o **capa 7** (el protocolo). La única defensa real es el
**cifrado de la capa de aplicación (TLS)**: si todo está cifrado, el sniffing ve
bytes incomprensibles.

**ARP poisoning** es un ataque **activo de capa 2**: el atacante manda tramas ARP
falsas para **modificar la tabla ARP** de la víctima y así lograr que envíe el
tráfico a él en lugar de al gateway real. Se resuelve con **port security**
(limitar cuántas MACs por puerto), **DAI** (validar las tablas ARP), y
**segmentación en VLANs**.

**La diferencia clave:** el sniffing se rompe **con cifrado** (capa 7); el ARP
poisoning se rompe **con control de acceso a la capa 2**. **Son defensas
completamente distintas**, y esa es la respuesta que hay que dar.

</details>

**6.** ¿Por qué la IP Móvil (MIPv4/MIPv6) no se desplegó, si sigue en Standards
Track?

<details><summary>Respuesta</summary>

Porque **técnicamente funciona pero operacionalmente es inviable**. Las cuatro
razones:

1. **Complejidad**: requiere que **el MN, el HA y el CN** soporten todo el stack de
   movilidad. Y por la **asimetría** de la ruta triangular, o el CN tiene que
   soportarlo o el tráfico pasa por el túnel en el HA.
2. **Middleboxes**: NAT, firewalls y load balancers en el camino **rompen el
   túnel**, porque no entienden la hipótesis del encapsulado. Y en el mundo real
   **todo el mundo tiene CGNAT**.
3. **CGN**: el Carrier-Grade NAT del operador implica que el HA **no puede ver** al
   CN (los dos están detrás de NAT). El mecanismo entero asume visibilidad
   extremo a extremo, que **no existe** en Internet hoy.
4. **Roaming entre tecnologías**: pasar de 4G a 5G a WiFi **cambia la dirección**.
   IP Móvil asume que el MN se mueve **dentro de la misma red** gestionada por el
   mismo operador, que ya no es el caso.

**Y qué se usa en su lugar:** **VPN** (WireGuard, IPsec), que es simple y funciona;
**CGN** e IPv6, que hacen que la dirección importe menos; y sobre todo **QUIC
connection migration** (`RFC 9000` §9), que resolvió la movilidad **en la capa de
transporte**: el **Connection ID** hace que **la identidad de la conexión deje de
ser la IP**, y eso habilita migración, NAT rebinding sin romper, y balanceo.

> **La respuesta de examen:** el modelo con HA, FA, COA y ruta triangular es lo que
> se evalúa, **pero** hay que agregar una línea diciendo que no se desplegó y por
> qué. Esa última línea es la que te distingue.

</details>

**7.** ¿Qué es DPI y por qué tiene un problema estructural hoy?

<details><summary>Respuesta</summary>

**DPI** (*Deep Packet Inspection*) es un mecanismo que **abre el paquete, decodifica
sus capas y lo interpreta como si fuera tráfico de aplicación**: lee la URL de un
HTTP, los headers, o incluso descifra el TLS. Sirve para aplicar **política por
aplicación** (permitir el trabajo, bloquear un juego), detectar malware y filtrar
spam.

**El problema estructural:** hoy **prácticamente todo** el tráfico está cifrado
(HTTPS). Un DPI en el medio **no puede leer el contenido** — es criptográficamente
imposible sin la clave. Para hacerlo tiene solo tres caminos:

1. **Proxy MITM** con las claves del servidor: **imposible** con cifrado de extremo
   a extremo.
2. **Instalar una CA corporativa** en cada dispositivo: **técnicamente funciona**,
   pero es **instalar una puerta trasera** en cada máquina, y viola la privacidad.
3. **Descifrar en el endpoint** (instrumentación del navegador o del SO): solo
   funciona si controlás el equipo.

Y hay una tercera capa: si la **app** usa cifrado de extremo a extremo (Signal,
WhatsApp), el cifrado ocurre **dentro** de la app y **nadie en la red** — ni el
administrador, ni el gobierno — puede leerlo. **Por eso hay leyes** (la
*ePrivacy* de la UE) que **limitan** el uso del DPI para inspección de contenido.

</details>

**8.** Un switch tiene *port security* y una MAC puede aprenderse solo una vez.
¿Qué pasa si un atacante hace flooding de MACs?

<details><summary>Respuesta</summary>

Se llama **MAC flooding** (o **CAM table overflow**), y el ataque tiene dos fases:

1. **Llenar la tabla.** La tabla CAM del switch tiene un **tamaño finito** (por
   ejemplo, 8 000 entradas). El atacante manda tramas con **MACs de origen
   aleatorias** hasta llenarla.
2. **Forzar al switch a actuar como un hub.** Cuando la tabla está llena, el switch
   **no puede aprender** la MAC destino, y por eso **reenvía la trama por TODOS los
   puertos** (como un hub). A partir de ahí, el atacante **ve todo el tráfico** de
   la VLAN.

**Las defensas:**

- **Port security** con límite de MACs por puerto: al superar el límite, el puerto
  entra en `shutdown` o `restrict` y **se genera un aviso**.
- **Dynamic ARP Inspection (DAI)**: valida los paquetes ARP contra el **DHCP
  snooping binding database**, y descarta los ARP con IP-MAC inconsistentes.
- **DHCP snooping**: solo los puertos "confiables" (los uplinks) pueden actuar como
  servidores DHCP; así se corta el *rogue DHCP*.
- **VLAN**: separar los puertos de usuarios de los de gestión y de los de
  servidores.

**Y el detalle importante:** el ataque **sí** es posible porque el switch no tiene
"puertos seguros" **por defecto**. Por eso el 802.1X + port security + DHCP snooping
+ DAI se ven **siempre juntos** en cualquier red empresarial bien armada.

</details>


## 🔗 Referencias

- **Examen `sirc1102`** — Problema 2 completo (30 pts: IP Móvil, campos por segmento, túnel)
- **Examen `sirc0812`** — Pregunta 3 (10 pts: arquitectura de IP Móvil) y **Problema 1** (30 pts: NAT con balanceo de carga)
- **Examen `sirc0707`** — Pregunta 5 (5 pts: funcionamiento de IP Móvil)
- **Examen `sirc0907`** — Problema 1 (30 pts: ruteo sobre una malla a nivel de enlace)
- **Examen `sirc0912`** — Pregunta 2 (10 pts: confiabilidad en transporte vs. enlace)
- **Examen `sirc0902`** — Problema 1 (9 pts: TLS)
- **Examen `sirc1002`** — Pregunta 4 (8 pts: firma digital)
- **Tanenbaum & Wetherall**, *Redes de computadoras* 5ª ed., cap. 8 (seguridad) y cap. 6 (movilidad)
- **`RFC 4303`** — IPsec · **`RFC 6347`** — VXLAN · **`RFC 2890`** — encapsulación IP · **`RFC 5944`** — Mobile IPv4 · **`RFC 6275`** — Mobile IPv6 · **`RFC 6084`** — DNS-Based Discovery
- **`ACTUALIZACIONES.md` §10** — el reencuadre de IP Móvil · **§13** — anclas de confianza por ámbito
- **`PLAN-48-CLASES.md`** — el plan completo de las 48 clases

---

## 🎓 Cierre del curso

Has llegado al final de las **48 clases**. Este es el mapa de lo que viste:

- **Bloque A** (1-7): los conceptos que todo lo demás asume — qué es una red, capas,
  encapsulación, y por qué el retardo es el problema central.
- **Bloque B** (8-15): las aplicaciones — cómo se ve una red desde arriba (HTTP,
  DNS, correo, sockets, DHCP).
- **Bloque C** (16-23): el transporte — UDP y TCP, y toda la maquinaria de
  confiabilidad y congestión.
- **Bloque D** (24-37): la red — direccionamiento, forwarding, enrutamiento, y los
  protocolos que lo hacen posible.
- **Bloque E** (38-43): el enlace — tramas, errores, acceso al medio, switch y
  WiFi.
- **Bloque F** (44-48): los servicios — multimedia, calidad, gestión y seguridad.

**Y la idea que atraviesa el curso entero:** cada capa resuelve un problema de la capa de
abajo y crea uno nuevo. El **store-and-forward** crea el retardo; el **retardo** crea
la necesidad de **control de congestión**; la **congestión** crea la necesidad de
**QoS**; el **cableado** de abajo crea la necesidad de **cifrado** de arriba. **Una
red es una cadena de compromisos, y entender de dónde viene cada uno es entender
la red.**

Mucha suerte en el examen. Acordate de una cosa: **3 horas, 60 puntos, y 15 en
teoría son obligatorios.** Las teóricas valen 40 de 100: si las hacés bien, tenés
la mitad del examen asegurado.