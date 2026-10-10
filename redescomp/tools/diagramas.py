"""
Biblioteca de diagramas SVG para las clases de Redes.

Genera SVG vectorial (sin dependencias) que se incrusta inline en el HTML
del PDF. Ventajas frente a traer imágenes de internet:
  - no hay links rotos ni problemas de licencia
  - el contenido es correcto porque lo escribimos nosotros
  - escala sin perder nitidez al imprimir

Paleta coherente con el PDF:
  AZUL   #0b3d5c   AZUL2 #14507a   CELESTE #7aa7c4   CLARO #eaf2f7
  NARANJA #c8621a   ROJO #b3261e    VERDE #2e7d4f     GRIS #666
"""

AZUL, AZUL2, CELESTE, CLARO = "#0b3d5c", "#14507a", "#7aa7c4", "#eaf2f7"
NARANJA, ROJO, VERDE, GRIS = "#c8621a", "#b3261e", "#2e7d4f", "#666"
FONDO, BORDE = "#ffffff", "#b8cfdb"
TXT, TXTCLARO = "#1a1a1a", "#ffffff"
MONO = "Consolas,'Cascadia Mono',monospace"
SANS = "'Segoe UI','Noto Sans',sans-serif"


# ---------------------------------------------------------------- primitivas

def esc(s: str) -> str:
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def svg(w: int, h: int, cuerpo: str, titulo: str = "") -> str:
    t = (f'<text x="{w/2}" y="24" text-anchor="middle" font-family="{SANS}" '
         f'font-size="15" font-weight="600" fill="{AZUL}">{esc(titulo)}</text>'
         if titulo else "")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="100%" '
            f'viewBox="0 0 {w} {h}" style="max-width:{w}px">'
            f'<rect width="{w}" height="{h}" fill="{FONDO}"/>{t}{cuerpo}</svg>')


def txt(x, y, s, size=12, color=TXT, anchor="start", weight="400", family=MONO):
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{family}" '
            f'font-size="{size}" font-weight="{weight}" fill="{color}">{esc(s)}</text>')


def caja(x, y, w, h, s, fill=CLARO, stroke=BORDE, fs=11, color=TXT, rx=4,
         bold=False, align="middle"):
    tx = x + w / 2 if align == "middle" else x + 6
    anc = "middle" if align == "middle" else "start"
    lines = str(s).split("\n")
    y0 = y + h / 2 - (len(lines) - 1) * (fs + 3) / 2 + fs * 0.35
    body = "".join(
        txt(tx, y0 + i * (fs + 3), ln, fs, color, anc,
            "700" if bold else "400") for i, ln in enumerate(lines))
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="1.2"/>{body}')


def flecha(x1, y1, x2, y2, color=AZUL2, w=1.6, punta=7, etiqueta="", dy=-6):
    a = (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" '
         f'stroke-width="{w}" marker-end="url(#p)"/>')
    t = txt((x1 + x2) / 2, (y1 + y2) / 2 + dy, etiqueta, 10, color, "middle") if etiqueta else ""
    return a + t


def defs():
    return (f'<defs><marker id="p" viewBox="0 0 10 10" refX="9" refY="5" '
            f'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M0,0 L10,5 L0,10 z" fill="{AZUL2}"/></marker>'
            f'<marker id="po" viewBox="0 0 10 10" refX="9" refY="5" '
            f'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M0,0 L10,5 L0,10 z" fill="{NARANJA}"/></marker>'
            f'<marker id="pr" viewBox="0 0 10 10" refX="9" refY="5" '
            f'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M0,0 L10,5 L0,10 z" fill="{ROJO}"/></marker>'
            f'</defs>')


def ar(x1, y1, x2, y2, color=NARANJA, etiqueta=""):
    a = (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" '
         f'stroke-width="1.8" marker-end="url(#po)"/>')
    return a + (txt((x1 + x2) / 2, (y1 + y2) / 2 - 6, etiqueta, 10, color, "middle")
                if etiqueta else "")


# ------------------------------------------------------- 1. pila de capas

def pila_capas():
    """OSI (7) vs TCP/IP (5): dos columnas con las equivalencias."""
    W, H = 780, 560
    CW = 290                      # ancho de cada columna de caja
    XO, XT = 50, 440
    ALTO = 44
    SEP = 52
    osi = ["7  Aplicación", "6  Presentación", "5  Sesión",
           "4  Transporte", "3  Red", "2  Enlace de datos", "1  Física"]
    tcp = ["5  Aplicación", "4  Transporte", "3  Internet", "2  Acceso a red"]
    c = [defs()]
    Y0 = 88
    c.append(txt(XO + CW / 2, 52, "OSI   (7 capas)", 15, AZUL, "middle", "700", SANS))
    c.append(txt(XT + CW / 2, 52, "TCP/IP   (5 capas)", 15, AZUL, "middle", "700", SANS))

    def y_osi(i):                  # i = 0..6
        return Y0 + i * SEP

    # bracket de fusion sobre 7+6+5
    ytop, ybot = y_osi(0), y_osi(2) + ALTO
    c.append(f'<path d="M{XO-14} {ytop} L{XO-14} {ybot}" stroke="{NARANJA}" '
             f'stroke-width="1.8" fill="none"/>')
    c.append(txt(XO - 22, (ytop + ybot) / 2, "se", 10, NARANJA, "middle", "700", SANS))
    c.append(txt(XO - 22, (ytop + ybot) / 2 + 14, "fusionan", 10, NARANJA, "middle", "700", SANS))

    for i, n in enumerate(osi):
        y = y_osi(i)
        fusionable = i <= 2
        col = "#fbe9dd" if fusionable else CLARO
        c.append(caja(XO, y, CW, ALTO, n, col, CELESTE, 12, TXT, 4, i == 0))

    # columna TCP/IP: 1 caja por equivalencia, centrada en el bloque OSI correspondiente
    # Aplicacion(TCP) cubre OSI 7+6+5 -> centro entre la 1 y la 3
    centros = [(y_osi(0) + y_osi(2) + ALTO) / 2,
               y_osi(3) + ALTO / 2,
               y_osi(4) + ALTO / 2,
               y_osi(5) + ALTO / 2 + 14]
    for i, n in enumerate(tcp):
        yy = centros[i] - ALTO / 2
        c.append(caja(XT, yy, CW, ALTO, n, CLARO, CELESTE, 12, TXT, 4, i == 0))
        c.append(ar(XO + CW + 6, centros[i], XT - 6, centros[i]))

    yfin = y_osi(6) + ALTO + 34
    c.append(txt(W / 2, yfin, "En TCP/IP no existen Presentación ni Sesión:", 12, GRIS, "middle"))
    c.append(txt(W / 2, yfin + 20,
                 "el cifrado vive en la capa de Aplicación (TLS) y en la biblioteca.",
                 12, GRIS, "middle"))
    c.append(txt(W / 2, yfin + 46,
                 "Ojo: hay dos criterios de conteo. Tanenbaum cuenta 5 capas porque",
                 11, NARANJA, "middle", "700", SANS))
    c.append(txt(W / 2, yfin + 62,
                 "separa enlace y física; Kurose cuenta 4. La capa 3 es la misma.",
                 11, NARANJA, "middle", "700", SANS))
    return svg(W, H, "".join(c), "Equivalencia entre el modelo OSI y TCP/IP")


# --------------------------------------------------------- 2. encapsulación

def encapsulacion():
    """Byte traveling: 500 B de datos se vuelven 558 B en el medio."""
    W, H = 760, 510
    X, WBOX = 50, 460
    ALTO = 42
    SEP = 54
    c = [defs()]
    capas = [
        ("Aplicación", "500 B  de datos", CLARO, 0),
        ("Transporte", "cabecera TCP", "#d8e8f2", 20),
        ("Internet", "cabecera IP", "#c2dcee", 20),
        ("Enlace", "cabecera Ethernet + FCS", "#aacfe8", 18),
    ]
    Y0 = 76
    c.append(txt(X, Y0 - 12, "Cada capa ENVUELVE a la anterior. Lo naranja es overhead nuevo.",
                 11, GRIS, "start", "700", SANS))
    for i, (nombre, cont, col, extra) in enumerate(capas):
        y = Y0 + i * SEP
        c.append(txt(X, y + 16, nombre, 11, AZUL2, "start", "700", SANS))
        c.append(caja(X + 96, y, 20, ALTO, "+", "#fbe0d0", NARANJA, 13, NARANJA, 3, True))
        if i == 0:
            w_ancho = 360
            c.append(caja(X + 116, y, w_ancho, ALTO, cont, col, CELESTE, 11))
            c.append(txt(X + 116 + w_ancho + 12, y + 17, "500 B", 10, GRIS))
        else:
            w_extra = 100
            w_datos = 360 - w_extra
            c.append(caja(X + 116, y, w_extra, ALTO, f"{extra} B", "#fbe0d0", NARANJA, 11))
            c.append(caja(X + 116 + w_extra, y, w_datos, ALTO, cont, col, CELESTE, 11))
            tot = 500 + extra * (i + 1)
            c.append(txt(X + 116 + 360 + 12, y + 17, f"{tot} B", 10, GRIS))
    yfin = Y0 + 4 * SEP + 12
    c.append(caja(X + 96, yfin, 360 + 20, ALTO, "558 bytes en el medio físico",
                  "#f7d9c8", NARANJA, 12, TXT, 4, True))
    # barra de eficiencia
    yb = yfin + ALTO + 46
    util = 500 / 558
    c.append(txt(X, yb, f"Eficiencia = 500 / 558 = {util*100:.1f}%", 12, VERDE, "start", "700", SANS))
    c.append(f'<rect x="{X}" y="{yb+12}" width="380" height="18" fill="#eee" stroke="{BORDE}"/>')
    c.append(f'<rect x="{X}" y="{yb+12}" width="{380*util:.1f}" height="18" fill="{VERDE}"/>')
    c.append(txt(X + 388, yb + 26, "datos 89,6%", 10, VERDE))
    c.append(txt(X + 388, yb + 42, "overhead 10,4%", 10, NARANJA))
    # nota del receptor
    c.append(txt(X, yb + 82, "El receptor hace lo mismo pero al revés: desempaqueta capa por capa.", 11, GRIS))
    c.append(txt(X, yb + 104, "Con un mensaje de 50 bytes el overhead sería del 54%: "
                              "por eso HTTP agrupa los objetos pequeños.", 11, NARANJA))
    return svg(W, H, "".join(c), "Encapsulación: de 500 bytes a 558")


# ------------------------------------------------------------- 3. topología

def topologia_natsubredes():
    """Red privada con dos subredes detras de un router NAT, saliendo a Internet."""
    W, H = 820, 400
    c = [defs()]

    def subred(x, y, w, h, nombre):
        return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" '
                f'fill="#f5f9fc" stroke="{CELESTE}" stroke-width="1.5" '
                f'stroke-dasharray="6 4"/>' +
                txt(x + 12, y + 22, nombre, 11, AZUL2, "start", "700", SANS))

    YLAN, HLAN = 150, 180
    c.append(subred(30, YLAN, 300, HLAN, "LAN 1   192.168.1.0/24"))
    c.append(subred(490, YLAN, 300, HLAN, "LAN 2   192.168.2.0/24"))
    # hosts de LAN 1
    c.append(caja(60, YLAN + 44, 120, 42, "192.168.1.25\nMAC_H", CLARO, BORDE, 10))
    c.append(caja(60, YLAN + 108, 120, 42, "192.168.1.40\nservidor", CLARO, BORDE, 10))
    # hosts de LAN 2
    c.append(caja(580, YLAN + 44, 120, 42, "192.168.2.25", CLARO, BORDE, 10))
    c.append(caja(580, YLAN + 108, 120, 42, "192.168.2.40", CLARO, BORDE, 10))
    # router
    XR = 375
    c.append(caja(XR, YLAN + 62, 76, 60, "R1\nNAT", "#f7d9c8", NARANJA, 13, TXT, 6, True))
    c.append(ar(190, YLAN + 92, XR - 6, YLAN + 78, AZUL2))
    c.append(ar(XR + 76 + 6, YLAN + 78, 570, YLAN + 92, AZUL2))
    c.append(txt(XR + 38, YLAN + 56, "192.168.1.1", 9, NARANJA, "middle", "700"))
    c.append(txt(XR + 38, YLAN + 138, "192.168.2.1", 9, NARANJA, "middle", "700"))
    # Internet
    c.append(f'<ellipse cx="415" cy="70" rx="190" ry="32" fill="#e9f4ed" '
             f'stroke="{VERDE}" stroke-width="1.6"/>')
    c.append(txt(415, 66, "Internet", 13, VERDE, "middle", "700", SANS))
    c.append(txt(415, 86, "servidor web  219.41.31.21", 10, VERDE, "middle"))
    c.append(f'<line x1="415" y1="102" x2="415" y2="{YLAN+56}" stroke="{VERDE}" stroke-width="2.4"/>')
    c.append(txt(425, YLAN + 44, "IP publica de R1:  220.10.10.30", 10, VERDE, "start", "700", SANS))
    # tabla NAT al costado
    c.append(txt(30, YLAN + HLAN + 34, "Tabla NAT de R1:", 11, AZUL, "start", "700", SANS))
    filas = ["(192.168.1.25 : 51000)  ->  (220.10.10.30 : 40001)",
             "(192.168.1.25 : 51002)  ->  (220.10.10.30 : 40002)",
             "(192.168.1.40 : 33333)  ->  (220.10.10.30 : 40003)"]
    for k, f in enumerate(filas):
        c.append(txt(30, YLAN + HLAN + 54 + k * 18, f, 10, TXT, "start"))
    c.append(txt(30, YLAN + HLAN + 118, "Al salir R1 cambia la IP origen y el puerto origen.",
                 10, GRIS))
    c.append(txt(30, YLAN + HLAN + 136, "Al volver busca la entrada y cambia destino IP y puerto.",
                 10, GRIS))
    return svg(W, H, "".join(c), "Red privada con dos subredes detras de un NAT")


def topologia_empresa():
    """Casa central y dos sucursales sobre un bloque publico, con VLSM."""
    W, H = 820, 430
    c = [defs()]

    def sede(x, y, nombre, sub, col=CELESTE):
        return (f'<rect x="{x}" y="{y}" width="210" height="86" rx="8" fill="#f5f9fc" '
                f'stroke="{col}" stroke-width="1.5" stroke-dasharray="6 4"/>' +
                txt(x + 12, y + 22, nombre, 11, AZUL2, "start", "700", SANS) +
                txt(x + 12, y + 44, sub, 10, TXT, "start") +
                txt(x + 12, y + 62, "enlace: /30", 9, GRIS, "start"))
    c.append(sede(30, 100, "Casa central", "LAN1  192.168.1.0/26"))
    c.append(sede(30, 236, "LAN2  (70 puestos)", "192.168.1.128/25"))
    c.append(sede(580, 100, "Sucursal Colonia", "LAN3  192.168.3.0/26"))
    c.append(sede(580, 236, "Sucursal Maldonado", "LAN4  192.168.4.0/26"))
    # routers
    for x, y, n in [(280, 88, "R1"), (280, 224, "R1b"), (480, 88, "R2"), (480, 224, "R3")]:
        c.append(caja(x, y, 72, 50, n, "#f7d9c8", NARANJA, 12, TXT, 6, True))
    c.append(ar(240, 130, 278, 114))
    c.append(ar(240, 266, 278, 242))
    c.append(ar(354, 114, 478, 114, VERDE))
    c.append(ar(354, 258, 478, 258, VERDE))
    # ISP
    c.append(f'<rect x="330" y="150" width="180" height="50" rx="8" fill="#eef4f8" '
             f'stroke="{BORDE}"/>')
    c.append(txt(420, 172, "ISP", 11, AZUL2, "middle", "700", SANS))
    c.append(txt(420, 190, "100.100.100.0/24", 10, GRIS, "middle", "700", SANS))
    c.append(txt(30, 46, "Plan de numeracion con bloque publico del ISP", 14, AZUL,
                 "start", "700", SANS))
    c.append(txt(30, 348, "Cada LAN pide el prefijo MAS PEQUENO que la abarque:", 10,
                 AZUL2, "start", "700", SANS))
    c.append(txt(30, 368, "LAN2 con 70 puestos necesita 71 direcciones -> /25 (128).",
                 10, GRIS))
    c.append(txt(30, 386, "Las otras, con 63 hosts, necesitan 65 -> /26 (64).", 10, GRIS))
    c.append(txt(30, 408, "Los bloques se asignan de mayor a menor, alineados. Asi se "
                          "deja libre lo que masTamano queda.", 10, NARANJA))
    return svg(W, H, "".join(c), "Plan de numeracion de una empresa con sucursales")


# ------------------------------------------------------------ 4. secuencias

def _secuencia(participantes, nombre_col, filas, titulo, alto_fila=34):
    """Diagrama de secuencia. filas = [(de, a, etiqueta, estilo)] con estilo n/r/v."""
    n = len(participantes)
    # separacion proporcional: se reserva el ancho del texto de etiqueta
    MARGEN, ANCHO_CJA = 34, 200
    SEP_COL = 250
    if n > 3:
        SEP_COL = 268
    xs = [MARGEN + ANCHO_CJA / 2 + i * SEP_COL for i in range(n)]
    W = MARGEN * 2 + ANCHO_CJA + (n - 1) * SEP_COL
    H = 86 + len(filas) * alto_fila + 20
    c = [defs()]
    for x, nm in zip(xs, participantes):
        c.append(caja(x - ANCHO_CJA / 2, 38, ANCHO_CJA, 36, nm, CLARO, CELESTE, 11, TXT, 5, True))
        c.append(f'<line x1="{x}" y1="74" x2="{x}" y2="{H-16}" stroke="{CELESTE}" '
                 f'stroke-width="1.2" stroke-dasharray="4 3"/>')
    for i, (de, a, etiqueta, estilo) in enumerate(filas):
        y = 100 + i * alto_fila
        x1, x2 = xs[de], xs[a]
        col = {"n": AZUL2, "r": ROJO, "v": VERDE}.get(estilo, AZUL2)
        mk = {"n": "p", "r": "pr", "v": "po"}.get(estilo, "p")
        c.append(f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{col}" '
                 f'stroke-width="1.8" marker-end="url(#{mk})"/>')
        c.append(txt((x1 + x2) / 2, y - 7, etiqueta.replace("|", "  ·  "), 10, col, "middle"))
    return svg(W, H, "".join(c), titulo), W, H


def sec_arp():
    s, _, _ = _secuencia(
        ["Host H\n(ARP vacia)", "Router R1", "Servidor Web"],
        None,
        [(0, 1, "ARP Request -> broadcast\n¿MAC de 192.168.1.1?", "n"),
         (1, 0, "ARP Reply -> unicast\nMAC1 = 192.168.1.1", "v"),
         (0, 1, "Trama: MAC2 -> MAC1\nIP 192.168.1.25 -> 219.41.31.21", "n"),
         (1, 2, "Sale a Internet: MAC destino = MAC del ISP", "n")],
        "Secuencia ARP completa (Examen 2011-03, apartado b.i)", alto_fila=40)
    return s


def sec_dns():
    s, _, _ = _secuencia(
        ["PC", "Servidor\nlocal", "Root", "TLD .edu", "Autoritativo"],
        None,
        [(0, 1, "consulta A\npruebaexamen.edu", "n"),
         (1, 2, "¿quien es\nel .edu?", "n"),
         (2, 1, "IP del TLD .edu\nsolo una referencia", "v"),
         (1, 3, "¿cual es el\nautoritativo?", "n"),
         (3, 1, "IP del autoritativo\nreferencia", "v"),
         (1, 4, "consulta A\npruebaexamen.edu", "n"),
         (4, 1, "IP de pruebaexamen.edu\ncon TTL", "v"),
         (1, 0, "IP de pruebaexamen.edu\nla cachea antes de responder", "v")],
        "Resolucion DNS iterativa sin cache (Examen 2010-07 P3)", alto_fila=38)
    return s


def sec_handshake():
    s, _, _ = _secuencia(
        ["Cliente  :49200", "Servidor  :80"],
        None,
        [(0, 1, "1)  SYN         seq = 2000", "n"),
         (1, 0, "2)  SYN + ACK   seq = 5000   ack = 2001", "v"),
         (0, 1, "3)  ACK         seq = 2001   ack = 5001", "n"),
         (0, 1, "    datos       seq = 2001   ack = 5001", "n"),
         (1, 0, "    ACK         seq = 5001   ack = 2001+d", "v"),
         (0, 1, "4)  FIN         seq = 2001+d", "n"),
         (1, 0, "    FIN + ACK   seq = 5001+d   ack = ...", "v"),
         (0, 1, "    ACK         ack = ...", "n")],
        "Three-way handshake y cierre de 4 vias (Examen 2006-12 P4)", alto_fila=32)
    return s


# ------------------------------------------------------ 5. gráfico de cwnd

def grafico_cwnd():
    """Evolución de cwnd: slow start (x2), congestion avoidance (+1) y perdidas."""
    W, H = 740, 440
    x0, y0, pw, ph = 90, 330, 560, 250
    VMAX, STEP = 16, 34
    c = [defs()]

    def px(r):
        return x0 + r * STEP

    def py(v):
        return y0 - (v / VMAX) * ph
    c.append(f'<rect x="{x0}" y="{y0-ph}" width="{pw}" height="{ph}" fill="#fcfdfe" '
             f'stroke="{BORDE}"/>')
    for v in range(0, VMAX + 1, 4):
        c.append(f'<line x1="{x0}" y1="{py(v)}" x2="{x0+pw}" y2="{py(v)}" stroke="#eef2f4"/>')
        c.append(txt(x0 - 10, py(v) + 4, str(v), 10, GRIS, "end"))
    c.append(f'<line x1="{x0}" y1="{y0}" x2="{x0+pw}" y2="{y0}" stroke="{GRIS}" stroke-width="1.5"/>')
    c.append(f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y0-ph}" stroke="{GRIS}" stroke-width="1.5"/>')
    for r in range(0, 17):
        c.append(txt(px(r), y0 + 18, str(r), 10, GRIS, "middle"))
    c.append(txt(x0 - 46, y0 - ph / 2 - 4, "cwnd", 12, AZUL, "middle", "700", SANS))
    c.append(txt(x0 - 46, y0 - ph / 2 + 12, "(MSS)", 10, GRIS, "middle"))
    c.append(txt(x0 + pw / 2, y0 + 40, "RTT", 12, AZUL, "middle", "700", SANS))
    c.append(f'<line x1="{x0}" y1="{py(8)}" x2="{x0+pw}" y2="{py(8)}" '
             f'stroke="{NARANJA}" stroke-width="1.5" stroke-dasharray="7 5"/>')
    c.append(txt(x0 + pw - 6, py(8) - 8, "ssthresh = 8 MSS", 10, NARANJA, "end", "700", SANS))
    ss = [(0, 1), (1, 2), (2, 4), (3, 8)]
    c.append('<polyline points="' + " ".join(f"{px(a)},{py(b)}" for a, b in ss) +
             f'" fill="none" stroke="{ROJO}" stroke-width="2.8"/>')
    for a, b in ss:
        c.append(f'<circle cx="{px(a)}" cy="{py(b)}" r="4" fill="{ROJO}"/>')
        c.append(txt(px(a) + 9, py(b) - 6, str(b), 10, ROJO, "start", "700"))
    c.append(txt(px(0) + 4, py(0.85), "slow start:  cwnd += MSS por ACK  →  duplica cada RTT",
                 10, ROJO, "start", "700", SANS))
    ca = [(3, 8), (4, 9), (5, 10), (6, 11), (7, 12), (8, 13)]
    c.append('<polyline points="' + " ".join(f"{px(a)},{py(b)}" for a, b in ca) +
             f'" fill="none" stroke="{VERDE}" stroke-width="2.8"/>')
    c.append(txt(px(5.5), py(13) - 14, "congestion avoidance:  +1 MSS por RTT",
                 10, VERDE, "middle", "700", SANS))
    c.append(ar(px(3), py(8), px(3), py(4), ROJO))
    c.append(txt(px(3) + 9, py(6.6), "3 ACK duplicados  →  fast retransmit", 10, ROJO,
                 "start", "700", SANS))
    c.append(txt(px(3) + 9, py(6.6) + 15, "Tahoe: 1 MSS      Reno: 4 MSS  ( = cwnd/2 )",
                 9, ROJO))
    c.append('<polyline points="' + " ".join(f"{px(a)},{py(b)}" for a, b in
             [(3, 4), (4, 5), (5, 6), (6, 7)]) + f'" fill="none" stroke="#e0913c" '
             f'stroke-width="2.2" stroke-dasharray="5 3"/>')
    c.append(ar(px(6), py(7), px(6), py(1), ROJO))
    c.append(txt(px(6) + 9, py(4.8), "timeout  →  Tahoe y Reno van los dos a 1 MSS",
                 10, ROJO, "start", "700", SANS))
    yleg = y0 + 62
    c.append(txt(x0, yleg, "Tahoe vuelve a 1 MSS ante cualquier perdida.", 10, GRIS))
    c.append(txt(x0, yleg + 17, "Reno solo cae a cwnd/2 con 3 ACK duplicados; ante un "
                                "timeout cae igual que Tahoe.", 10, GRIS))
    return svg(W, H, "".join(c), "Evolucion de la ventana de congestion")


# ------------------------------------------------------- 6. eficiencia ALOHA

def grafico_aloha():
    """Curvas de carga vs. rendimiento para ALOHA y Slotted-ALOHA."""
    import math
    W, H = 760, 380
    x0, y0, pw, ph = 84, 300, 600, 230
    ESC = 1.9
    c = [defs()]
    c.append(f'<rect x="{x0}" y="{y0-ph}" width="{pw}" height="{ph}" fill="#fcfdfe" '
             f'stroke="{BORDE}"/>')
    for v in (0.2, 0.4, 0.6):
        c.append(f'<line x1="{x0}" y1="{y0-v*ph*ESC}" x2="{x0+pw}" '
                 f'y2="{y0-v*ph*ESC}" stroke="#eef2f4"/>')
        c.append(txt(x0 - 8, y0 - v * ph * ESC + 4, f"{v:.1f}".replace(".", ","),
                     10, GRIS, "end"))
    c.append(f'<line x1="{x0}" y1="{y0}" x2="{x0+pw}" y2="{y0}" stroke="{GRIS}" stroke-width="1.5"/>')
    c.append(f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y0-ph}" stroke="{GRIS}" stroke-width="1.5"/>')
    c.append(txt(x0 - 8, y0 + 4, "0", 10, GRIS, "end"))
    c.append(txt(x0, y0 + 18, "0", 10, GRIS, "middle"))
    for g in (0.25, 0.5, 0.75):
        c.append(txt(x0 + g * pw, y0 + 18, f"{g:.2f}".replace(".", ","), 10, GRIS, "middle"))
    c.append(txt(x0 + pw, y0 + 18, "1,0", 10, GRIS, "middle"))
    c.append(txt(x0 + pw / 2, y0 + 42, "carga G (intentos por ranura)", 11, AZUL,
                 "middle", "700", SANS))
    c.append(txt(x0 - 48, y0 - ph / 2 - 8, "rendimiento", 11, AZUL, "middle", "700", SANS))
    c.append(txt(x0 - 48, y0 - ph / 2 + 8, "S", 10, GRIS, "middle"))

    def curva(f, color, upto=0.95, n=140):
        pts = []
        for k in range(n + 1):
            g = upto * k / n
            s = f(g)
            pts.append(f"{x0+g*pw},{y0-s*ph*ESC}")
        return f'<polyline points="{" ".join(pts)}" fill="none" stroke="{color}" stroke-width="2.6"/>'
    c.append(curva(lambda g: g * math.exp(-2 * g), ROJO))
    c.append(curva(lambda g: g * math.exp(-g), AZUL2))
    c.append(f'<circle cx="{x0+0.5*pw}" cy="{y0-0.184*ph*ESC}" r="4.5" fill="{ROJO}"/>')
    c.append(txt(x0 + 0.5 * pw - 12, y0 - 0.184 * ph * ESC - 9, "max = 1/(2e) = 0,184",
                 10, ROJO, "end", "700", SANS))
    c.append(f'<circle cx="{x0+0.368*pw}" cy="{y0-0.368*ph*ESC}" r="4.5" fill="{AZUL2}"/>')
    c.append(txt(x0 + 0.368 * pw + 10, y0 - 0.368 * ph * ESC - 9, "max = 1/e = 0,368",
                 10, AZUL2, "start", "700", SANS))
    c.append(txt(x0 + 10, y0 - ph + 20, "ALOHA puro      S = G · e^(-2G)", 11, ROJO,
                 "start", "700", SANS))
    c.append(txt(x0 + 10, y0 - ph + 40, "Slotted ALOHA   S = G · e^(-G)", 11, AZUL2,
                 "start", "700", SANS))
    c.append(txt(x0, y0 + 68, "Slotted dobla el maximo porque la ventana vulnerable pasa "
                              "de 2T a T.", 10, GRIS))
    c.append(txt(x0, y0 + 86, "Aunque ninguno supera el 37 %, es el techo teorico: por eso "
                              "Ethernet conmutada no usa ALOHA.", 10, GRIS))
    return svg(W, H, "".join(c), "Rendimiento de ALOHA y Slotted-ALOHA")


# --------------------------------------------------- 7. AND de una máscara

def diagrama_subnet():
    """Dirección AND máscara, con el resultado en binario columna a columna."""
    W, H = 780, 400
    c = [defs()]
    ip = "192.168.10.55"
    mstr = "255.255.255.192"
    c.append(txt(40, 44, "IP", 12, AZUL, "start", "700", SANS))
    c.append(txt(400, 44, "Mascara  (/26)", 12, AZUL, "start", "700", SANS))
    c.append(txt(600, 44, "AND = resultado", 12, AZUL, "start", "700", SANS))

    def b8(s):
        return format(int(s), "08b")

    ipb = [b8(x) for x in ip.split(".")]
    msk = [b8(x) for x in mstr.split(".")]
    y = 62
    for j in range(4):
        c.append(txt(40, y + 14, ipb[j], 13, TXT))
        c.append(txt(400, y + 14, msk[j], 13, TXT))
        r = int(ipb[j], 2) & int(msk[j], 2)
        c.append(txt(600, y + 14, format(r, "08b"), 13, VERDE, "start", "700"))
        c.append(f'<line x1="36" y1="{y+24}" x2="756" y2="{y+24}" stroke="#eef2f4"/>')
        y += 32
    c.append(txt(40, y + 26, f"{ip}  AND  {mstr}  =  192.168.10.64", 13, AZUL,
                 "start", "700", SANS))
    y += 58
    # izquierda: que se obtiene
    c.append(txt(40, y, "Lo que resulta de ese AND:", 11, GRIS, "start", "700", SANS))
    filas = [("direccion de red", "192.168.10.64", NARANJA),
             ("primer host", "192.168.10.65", VERDE),
             ("ultimo host", "192.168.10.126", VERDE),
             ("broadcast", "192.168.10.127", ROJO),
             ("hostables", "62", AZUL)]
    yfila = y + 20
    for nombre, val, col in filas:
        c.append(caja(40, yfila, 190, 26, nombre, "#f7f9fa", BORDE, 10, GRIS, 3, False, "start"))
        c.append(txt(242, yfila + 18, val, 11, col, "start", "700"))
        yfila += 29
    # derecha: por que /26
    c.append(txt(400, y, "El prefijo /26 significa:", 11, GRIS, "start", "700", SANS))
    for k, s in enumerate(["26 bits de red + 6 bits de host",
                           "2^6 = 64 direcciones en la subred",
                           "64 - 2 = 62 hostables"]):
        c.append(txt(400, y + 22 + k * 20, s, 11, NARANJA if k == 2 else TXT))
    c.append(txt(400, y + 96, "El AND pone en 0 todos los bits", 11, GRIS))
    c.append(txt(400, y + 112, "de host: por eso el resultado es", 11, GRIS))
    c.append(txt(400, y + 128, "la direccion de RED, no una de host.", 11, GRIS))
    return svg(W, H, "".join(c), "Como se aplica una mascara de subred, bit a bit")


# ---------------------------------------------------- 8. cabeceras de campos

def cabecera_tcp():
    W, H = 760, 330
    c = [defs()]
    campos = [
        ("Source Port", 16), ("Destination Port", 16),
        ("Sequence Number", 32),
        ("Acknowledgment Number", 32),
        ("Data Offset", 4), ("Res", 3), ("Flags", 9), ("Window Size", 16),
        ("Checksum", 16), ("Urgent Pointer", 16),
        ("Options (variables)", 160),
    ]
    COLS = 32
    ANCHO = 700 / COLS
    x0, y = 40, 70
    fila = 0
    usado = 0
    for nombre, bits in campos:
        if usado + bits > COLS:
            y += 34
            fila += 1
            usado = 0
        w = bits * ANCHO
        es4 = bits == 4
        col = "#f7d9c8" if es4 else (CLARO if fila % 2 == 0 else "#dceaf3")
        c.append(caja(x0 + usado * ANCHO, y, w, 30, nombre, col, CELESTE, 9.5,
                      TXT, 3, False))
        c.append(txt(x0 + usado * ANCHO + w / 2, y + 44, f"{bits}", 9, GRIS, "middle"))
        usado += bits
    c.append(txt(x0, 52, "bit 0", 10, GRIS))
    for i in range(COLS + 1):
        if i % 4 == 0:
            c.append(txt(x0 + i * ANCHO, 52, str(i), 9, GRIS, "middle"))
    c.append(txt(40, y + 86, "Cabecera minima: 5 filas de 32 bits = 20 bytes. "
                             "Con opciones puede llegar a 60 bytes.", 11, GRIS))
    c.append(txt(40, y + 116, "Los ACKs son de BYTES, no de segmentos:", 11, NARANJA,
                 "start", "700", SANS))
    c.append(txt(40, y + 136, "si seq = 1100 y mandas 20 bytes, el ACK siguiente es 1120.",
                 11, NARANJA))
    return svg(W, H, "".join(c), "Cabecera TCP, campo por campo")


def cabecera_ipv4():
    W, H = 740, 340
    c = [defs()]
    campos = [("Version", 4), ("IHL", 4), ("Type of Service", 8), ("Total Length", 16),
              ("Identification", 16), ("Flags", 3), ("Fragment Offset", 13),
              ("Time to Live", 8), ("Protocol", 8), ("Header Checksum", 16),
              ("Source IP Address", 32), ("Destination IP Address", 32),
              ("Options (variables)", 128)]
    COLS, ANCHO = 32, 700 / 32
    x0, y, usado = 40, 70, 0
    for nombre, bits in campos:
        if usado + bits > COLS:
            y += 34
            usado = 0
        w = bits * ANCHO
        frag = nombre in ("Flags", "Fragment Offset")
        col = "#f7d9c8" if frag else (CLARO if (y // 34) % 2 == 0 else "#dceaf3")
        c.append(caja(x0 + usado * ANCHO, y, w, 30, nombre, col,
                      NARANJA if frag else CELESTE, 9.5, TXT, 3, False))
        c.append(txt(x0 + usado * ANCHO + w / 2, y + 44, f"{bits}", 9, GRIS, "middle"))
        usado += bits
    c.append(txt(40, y + 74, "En naranja: los tres campos que hacen posible la "
                             "fragmentación. El bit DF es el 2.º de Flags.", 11, GRIS))
    c.append(txt(40, y + 96, "IHL = 5 significa cabecera de 20 bytes sin opciones.", 11, TXT))
    return svg(W, H, "".join(c), "Cabecera IPv4, campo por campo")


def cabecera_ipv6():
    W, H = 740, 280
    c = [defs()]
    campos = [("Version", 4), ("Traffic Class", 8), ("Flow Label", 20),
              ("Payload Length", 16), ("Next Header", 8), ("Hop Limit", 8),
              ("Source Address", 128), ("Destination Address", 128)]
    COLS, ANCHO = 32, 700 / 32
    x0, y, usado = 40, 70, 0
    for nombre, bits in campos:
        if usado + bits > COLS:
            y += 34
            usado = 0
        w = bits * ANCHO
        col = CLARO if (y // 34) % 2 == 0 else "#dceaf3"
        c.append(caja(x0 + usado * ANCHO, y, w, 30, nombre, col, CELESTE, 9.5, TXT, 3))
        usado += bits
    c.append(txt(40, 56, "cabecera fija de 40 bytes (5 filas), sin opciones", 10, GRIS))
    c.append(txt(40, y + 70, "Desaparecen frente a IPv4: el checksum de cabecera, "
                             "el IHL y el Fragment Offset.", 11, GRIS))
    c.append(txt(40, y + 92, "Aparece: el Flow Label de 20 bits, que identifica un "
                             "flujo sin mirar el 5-tupla.", 11, VERDE))
    c.append(txt(40, y + 114, "El Payload Length excluye las cabeceras de extensión.", 11, NARANJA))
    return svg(W, H, "".join(c), "Cabecera IPv6, campo por campo")


# ---------------------------------------------------------- 9. Dijkstra

def grafico_dijkstra():
    """Grafo con Dijkstra: nodos definitivos (S) y tentativos (T)."""
    W, H = 700, 380
    pos = {"u": (350, 60), "v": (170, 170), "w": (530, 170),
           "x": (100, 300), "y": (350, 300), "z": (600, 300)}
    aristas = [("u", "v", 1), ("u", "w", 4), ("v", "x", 2), ("v", "y", 5),
               ("w", "y", 1), ("w", "z", 3), ("x", "y", 1), ("y", "z", 2)]
    c = [defs()]
    definitivos = {"u", "v", "x", "y"}
    for a, b, w_ in aristas:
        x1, y1 = pos[a]
        x2, y2 = pos[b]
        col = VERDE if (a in definitivos and b in definitivos) else "#b9c6cf"
        c.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" '
                 f'stroke-width="{2.4 if col == VERDE else 1.4}"/>')
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        c.append(caja(mx - 13, my - 11, 26, 22, str(w_), "#ffffff", BORDE, 10, TXT, 11))
    dist = {"u": 0, "v": 1, "x": 3, "y": 5, "w": 4, "z": 7}
    for n, (x, y) in pos.items():
        col = VERDE if n in definitivos else "#f7d9c8"
        c.append(f'<circle cx="{x}" cy="{y}" r="21" fill="{col}" '
                 f'stroke="{VERDE if n in definitivos else NARANJA}" stroke-width="2.2"/>')
        c.append(txt(x, y + 5, n, 13, TXT, "middle", "700", SANS))
        c.append(txt(x, y + 36, f"d={dist[n]}", 10, GRIS, "middle"))
    c.append(f'<circle cx="60" cy="34" r="8" fill="{VERDE}"/>')
    c.append(txt(74, 38, "definitivo (S)", 10, GRIS))
    c.append(f'<circle cx="180" cy="34" r="8" fill="#f7d9c8" stroke="{NARANJA}"/>')
    c.append(txt(194, 38, "tentativo (T)", 10, GRIS))
    c.append(txt(350, 365, "Dijkstra termina cuando S = todos los nodos.", 10, GRIS, "middle"))
    return svg(W, H, "".join(c), "Dijkstra: S (definitivos) y T (tentativos)")


# ------------------------------------------------------ 10. CRC y polinomios

def crc_polinomio():
    """Division polinomica larga en GF(2), con los XOR explicitos."""
    W, H = 700, 400
    FS = 15
    c = [defs()]

    def bits(s):
        return list(s)

    def fila(y, s, col, x0=90, peso=700):
        x = x0
        for b in bits(s):
            c.append(caja(x, y, peso / len(s), 24, b, "#ffffff",
                          col if b == "1" else BORDE, 11,
                          col if b == "1" else "#bbb", 2, b == "1"))
            x += peso / len(s)

    def regla(y, x1, x2, col):
        c.append(f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{col}" stroke-width="1.6"/>')

    c.append(txt(40, 40, "Dividendo:  D(x)·x^r + R(x)", 13, TXT, "start", "700", SANS))
    c.append(txt(40, 66, "Divisor:     G(x)   =  1101", 13, AZUL2, "start", "700", SANS))
    c.append(txt(40, 92, "Resto R(x):  lo que sobra, y es el CRC que se envia", 13,
                 NARANJA, "start", "700", SANS))
    # fila 1: dividendo completo
    c.append(txt(46, 140, "1101011 1011001", 12, GRIS, "start", "700"))
    fila(112, "11010111011", TXT)
    regla(140, 88, 372, TXT)
    # divisor alineado
    fila(150, "1101", AZUL2)
    c.append(txt(660, 165, "G(x) = x^3 + x^2 + 1", 10, AZUL2, "end", "700", SANS))
    # resto parcial
    c.append(txt(46, 202, "0100", 12, ROJO, "start", "700"))
    fila(178, "0100", ROJO)
    regla(206, 88, 222, ROJO)
    # siguiente parcial
    c.append(txt(46, 246, "0011", 12, ROJO, "start", "700"))
    fila(222, "0011", ROJO)
    regla(250, 88, 158, ROJO)
    # XOR final -> resto
    c.append(txt(46, 292, "0011", 12, NARANJA, "start", "700"))
    fila(268, "0011", NARANJA)
    c.append(f'<line x1="88" y1="298" x2="214" y2="298" stroke="{NARANJA}" stroke-width="1.8"/>')
    c.append(caja(214, 300, 62, 26, "0011", "#fbe0d0", NARANJA, 12, NARANJA, 3, True))
    c.append(txt(286, 319, "= el CRC (4 bits)", 11, NARANJA, "start", "700", SANS))
    c.append(txt(40, 352, "En GF(2) sumar es XOR y multiplicar es AND. Por eso la "
                          "resta de la division es un XOR.", 10, GRIS))
    c.append(txt(40, 372, "Se divide D(x)·x^r entre G(x) y se manda el resto pegado "
                          "al mensaje original.", 10, GRIS))
    return svg(W, H, "".join(c), "Division polinomica para calcular el CRC")


# ---------------------------------------------------- 11. leaky / token

def cubetas():
    """Leaky bucket y token bucket lado a lado."""
    W, H = 760, 330
    c = [defs()]

    def cubeta(x, y, nivel, etiqueta, col, nota):
        c.append(f'<rect x="{x}" y="{y}" width="160" height="160" rx="6" fill="#fff" '
                 f'stroke="{AZUL2}" stroke-width="2"/>')
        c.append(f'<rect x="{x+3}" y="{y+160-nivel}" width="154" height="{nivel-3}" '
                 f'fill="{col}" opacity="0.55"/>')
        c.append(f'<line x1="{x+3}" y1="{y+160-nivel}" x2="{x+157}" y2="{y+160-nivel}" '
                 f'stroke="{col}" stroke-width="2.4"/>')
        c.append(txt(x + 80, y + 186, etiqueta, 12, AZUL, "middle", "700", SANS))
        c.append(txt(x + 80, y + 204, nota, 9, GRIS, "middle"))
    c.append(txt(30, 40, "La misma salida (una linea fina a la derecha) sale de dos "
                         "mecanismos distintos:", 11, GRIS, "start", "700", SANS))
    cubeta(50, 64, 70, "leaky bucket", "#9fc6e0", "nivel = liquido acumulado")
    cubeta(270, 64, 40, "token bucket", "#9fd8b0", "nivel = tokens disponibles")
    # salida
    for x in (218, 438):
        c.append(ar(x, 144, x, 144, AZUL2))
        c.append(f'<line x1="{x}" y1="74" x2="{x}" y2="214" stroke="{AZUL2}" stroke-width="2"/>')
        c.append(txt(x + 8, 148, "salida a la\\ntasa r", 9, AZUL2, "start", "700", SANS))
    # entrada
    c.append(ar(130, 14, 130, 58, NARANJA))
    c.append(txt(140, 34, "entrada", 9, NARANJA, "start", "700", SANS))
    c.append(ar(350, 14, 350, 58, NARANJA))
    c.append(txt(360, 34, "tokens a\\nritmo r", 9, NARANJA, "start", "700", SANS))
    c.append(ar(130, 14, 350, 14, NARANJA))
    # tabla comparativa
    c.append(txt(500, 74, "leaky bucket", 12, AZUL, "start", "700", SANS))
    for i, t in enumerate(["· salida SIEMPRE a la tasa r",
                           "· si esta llena, descarta el paquete",
                           "· NO permite rafagas",
                           "· introduce latencia por la cola"]):
        c.append(txt(500, 96 + i * 19, t, 10, TXT))
    c.append(txt(500, 196, "token bucket", 12, AZUL, "start", "700", SANS))
    for i, t in enumerate(["· sale a la tasa r, pero puede",
                           "  BURSTAR hasta b tokens",
                           "· los tokens se generan a ritmo r",
                           "  y se consumen al enviar",
                           "· SI permite rafagas"]):
        c.append(txt(500, 218 + i * 19, t, 10, TXT))
    c.append(txt(30, 300, "Parametros comunes:  b = capacidad (tamanio de la cubeta / "
                          "cantidad maxima de tokens)", 10, AZUL2, "start", "700", SANS))
    c.append(txt(30, 318, "                             r = tasa de salida o de generacion de tokens",
                 10, AZUL2, "start", "700", SANS))
    return svg(W, H, "".join(c), "Leaky bucket frente a token bucket")


# ----------------------------------------------------------- 12. MPLS

def mpls_hop():
    """El mismo paquete a traves de 3 saltos MPLS, cambiando solo la etiqueta."""
    W, H = 800, 330
    c = [defs()]
    NW, NGAP, SEP = 150, 55, 0
    nodos = [("LER ingreso", "red de cliente", NARANJA),
             ("LSR 1", "nucleo", AZUL2),
             ("LSR 2", "nucleo", AZUL2),
             ("LER egreso", "red destino", NARANJA)]
    x0 = 40
    xs = []
    for i2, (rol, sub, col) in enumerate(nodos):
        x = x0 + i2 * (NW + NGAP)
        xs.append(x)
        c.append(caja(x, 48, NW, 52, f"{rol}\n{sub}", "#f7d9c8" if col == NARANJA else CLARO,
                      col, 10, TXT, 6, True))
        if i2 < len(nodos) - 1:
            c.append(ar(x + NW + 4, 74, x + NW + NGAP - 4, 74))
    # la etiqueta que lleva el paquete en cada tramo
    yp = 160
    tramos = [("IP 8.8.8.8\nsin etiqueta", CLARO, BORDE, "1. el ingreso decide el camino"),
              ("Lbl 100 · 12000", "#dceaf3", CELESTE, "2. solo cambia la etiqueta"),
              ("Lbl 104 · 12000", "#dceaf3", CELESTE, "3. sigue cambiando"),
              ("IP 8.8.8.8\nsin etiqueta", CLARO, BORDE, "4. el egreso saca la etiqueta")]
    for i2, (s, fill, st, nota) in enumerate(tramos):
        x = xs[i2]
        c.append(txt(x, yp - 8, nota, 9, NARANJA if i2 in (0, 3) else AZUL2, "start", "700", SANS))
        c.append(caja(x, yp, NW, 44, s, fill, st, 9, TXT, 4, False))
        if i2 < len(tramos) - 1:
            c.append(ar(x + NW + 4, yp + 22, x + NW + NGAP - 4, yp + 22, NARANJA))
    c.append(txt(x0, 250, "El LSR nunca mira la direccion IP: por eso es rapido.",
                 10, GRIS))
    c.append(txt(x0, 268, "Ese es el trade-off: velocidad a cambio de que el nucleo no",
                 10, GRIS))
    c.append(txt(x0, 286, "puede aplicar ningun filtro de seguridad por IP.", 10, GRIS))
    return svg(W, H, "".join(c), "Un LSP de MPLS saltando por el nucleo")


# ------------------------------------------------------- 13. CSMA/CD

def csma_cd():
    """Linea de tiempo de una colision en CSMA/CD con backoff exponencial."""
    W, H = 780, 360
    c = [defs()]
    TL0 = 70
    c.append(txt(TL0, 40, "tiempo ->", 11, GRIS, "start", "700", SANS))
    # lifeline de A y de B
    for nombre, x in [("A", 110), ("B", 330)]:
        c.append(caja(x - 42, 54, 84, 30, nombre, CLARO, CELESTE, 12, TXT, 5, True))
        c.append(f'<line x1="{x}" y1="84" x2="{x}" y2="272" stroke="{CELESTE}" '
                 f'stroke-width="1.3" stroke-dasharray="4 3"/>')
    # trama de A y de B
    c.append(caja(110, 112, 230, 26, "trama de A", CLARO, AZUL2, 10))
    c.append(caja(150, 146, 90, 26, "trama de B", "#f7d9c8", NARANJA, 10))
    c.append(txt(110, 106, "A empieza primero (sensing OK)", 9, GRIS))
    # momento de la colision
    xc = 240
    c.append(f'<line x1="{xc}" y1="92" x2="{xc}" y2="186" stroke="{ROJO}" '
             f'stroke-width="2" stroke-dasharray="4 3"/>')
    c.append(txt(xc + 7, 186, "COLISIÓN", 10, ROJO, "start", "700", SANS))
    c.append(caja(110, 200, 300, 26, "jamming  ·  ambos se detienen", "#fbe0e0",
                  ROJO, 10))
    c.append(txt(110, 196, "se emite la secuencia de jammed (32/64 bits)", 9, GRIS))
    # ventanas de backoff, alineadas bajo el instante de la colision
    intentos = [(110, 80, "intento 1", "r en [0,1]"),
                (270, 130, "intento 2", "r en [0,3]"),
                (480, 250, "intento 3", "r en [0,7]")]
    for x, w, et, rng in intentos:
        c.append(caja(x, 250, w, 26, rng, CLARO, CELESTE, 10))
        c.append(txt(x + w / 2, 244, et, 9, GRIS, "middle"))
    # el que gana
    c.append(ar(270, 250, 195, 250, VERDE))
    c.append(txt(70, 292, "backoff exponencial:  r en [0, 2^k - 1],  k = numero de intento",
                 10, AZUL2, "start", "700", SANS))
    c.append(txt(70, 310, "el menor r gana y transmite; si vuelve a chocar, dobla el rango.",
                 10, VERDE))
    return svg(W, H, "".join(c), "CSMA/CD: colision y backoff exponencial")


def csma_ca():
    """RTS/CTS resuelve la estacion oculta; C se calla por el NAV."""
    W, H = 780, 380
    c = [defs()]
    nodos = [("A", 110), ("B", 390), ("C (oculta)", 660)]
    for nombre, x in nodos:
        c.append(caja(x - 55, 44, 110, 32, nombre, CLARO, CELESTE, 12, TXT, 5, True))
        c.append(f'<line x1="{x}" y1="76" x2="{x}" y2="300" stroke="{CELESTE}" '
                 f'stroke-width="1.3" stroke-dasharray="4 3"/>')
    filas = [("RTS de A", 110, 390, NARANJA),
             ("CTS de B", 390, 660, VERDE),
             ("trama de A", 110, 390, AZUL2),
             ("ACK de B", 390, 110, ROJO)]
    y = 104
    for etiqueta, x1, x2, col in filas:
        c.append(ar(x1, y, x2, y, col))
        c.append(txt((x1 + x2) / 2, y - 7, etiqueta, 10, col, "middle", "700", SANS))
        y += 34
    # por que C se calla
    c.append(txt(70, 216, "asi se resuelve la estacion oculta:", 10, VERDE, "start", "700", SANS))
    c.append(caja(70, 226, 640, 74,
                  "C no oye el RTS de A (no esta a su alcance), pero SI oye el CTS de B:"
                  " se actualiza su NAV y espera sin transmitir.",
                  "#eef7f0", VERDE, 11, TXT, 5, False))
    c.append(f'<line x1="660" y1="300" x2="660" y2="300" stroke="{VERDE}" stroke-width="1.6"/>')
    c.append(txt(60, 338, "En radio no se puede usar CSMA/CD: la antena es half-duplex, "
                          "la potencia propia enmascera a los demas", 10, GRIS))
    c.append(txt(60, 354, "y no se puede transmitir y escuchar a la vez. Por eso WiFi no "
                          "detecta colisiones: las EVITA.", 10, GRIS))
    c.append(txt(60, 374, "Mecanismos: RTS/CTS, NAK, ACK por trama (no acumulado), "
                          "espera aleatoria y EDCA con 4 colas.", 10, NARANJA,
                 "start", "700", SANS))
    return svg(W, H, "".join(c), "CSMA/CA con RTS/CTS y estacion oculta")


# ------------------------------------------------------- 14. NAT

def nat_tabla():
    """Tabla NAT con traduccion de puertos (PAT): 3 sesiones simultaneas."""
    W, H = 760, 350
    c = [defs()]
    CW = 236
    xs = [24, 268, 512]
    cab = ["IP privada : puerto", "IP publica : puerto", "estado"]
    for x, t2 in zip(xs, cab):
        c.append(caja(x, 46, CW, 30, t2, AZUL, AZUL, 11, TXTCLARO, 4, True))
    filas = [["192.168.1.25 : 51000", "220.10.10.30 : 40001", "activa"],
             ["192.168.1.25 : 51002", "220.10.10.30 : 40002", "activa"],
             ["192.168.1.40 : 33333", "220.10.10.30 : 40003", "activa"],
             ["192.168.1.77 : 8080", "220.10.10.30 : 40004", "timeout 300 s"]]
    y = 82
    for i2, f in enumerate(filas):
        bg = CLARO if i2 % 2 == 0 else "#f7f9fa"
        for x, v in zip(xs, f):
            c.append(caja(x, y, CW, 30, v, bg, BORDE, 10, TXT, 3))
        y += 33
    c.append(txt(24, y + 34, "La clave de la tabla es (IP privada, puerto privado). El puerto "
                             "es lo que permite", 10, GRIS))
    c.append(txt(24, y + 50, "multiplexar many-to-one: 3 sesiones, 1 sola IP publica.",
                 10, GRIS))
    c.append(txt(24, y + 76, "Al volver un paquete se busca (IP publica, puerto publico) y "
                             "se traducen", 10, GRIS))
    c.append(txt(24, y + 92, "la IP destino y el puerto destino.", 10, GRIS))
    c.append(txt(24, y + 118, "Ese es el motivo por el que NAT rompe el aislamiento "
                              "de capas:", 10, NARANJA, "start", "700", SANS))
    c.append(txt(24, y + 134, "el router tiene que entender TCP/UDP para funcionar.",
                 10, NARANJA))
    return svg(W, H, "".join(c), "Tabla NAT con traduccion de puertos (PAT)")


def voip_buffer():
    """Jitter buffer: tiempos de llegada frente a reproduccion regular."""
    W, H = 720, 380
    x0, y0, PH, ESC = 90, 110, 210, 1.2
    c = [defs()]
    c.append(f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y0+PH}" stroke="{GRIS}"/>')
    c.append(f'<line x1="{x0}" y1="{y0+PH}" x2="{x0+520}" y2="{y0+PH}" stroke="{GRIS}"/>')
    llegadas = [0, 60, 90, 150, 185, 230, 300, 330, 400]
    gen = [0, 40, 80, 120, 160, 200, 240, 280, 320]
    for tl, g in zip(llegadas, gen):
        yy = y0 + PH - tl * ESC
        xx = x0 + g * ESC
        c.append(f'<line x1="{xx}" y1="{y0+PH}" x2="{xx}" y2="{yy}" stroke="#f2dbd3" '
                 f'stroke-width="1"/>')
        c.append(f'<circle cx="{xx}" cy="{yy}" r="4.5" fill="{ROJO}"/>')
        c.append(txt(xx + 8, yy + 4, str(tl), 9, ROJO))
    c.append(txt(x0 - 8, y0 + PH + 4, "0", 10, GRIS, "end"))
    c.append(txt(x0 - 8, y0 + 4, "400 ms", 10, GRIS, "end"))
    c.append(txt(x0 - 8, y0 + PH / 2, "llegada", 9, GRIS, "end"))
    c.append(txt(x0 + 528, y0 + PH + 4, "ti", 10, VERDE, "end"))
    c.append(txt(x0 + 260, y0 + PH + 26, "tiempo de generacion", 10, GRIS, "middle"))
    pmax = max(llegadas) - min(gen)
    yb = y0 + PH - pmax * ESC
    c.append(f'<line x1="{x0}" y1="{yb}" x2="{x0+520}" y2="{yb}" stroke="{VERDE}" '
             f'stroke-width="1.6" stroke-dasharray="6 4"/>')
    c.append(txt(x0 + 16, yb - 9, f"p = {pmax} ms  =  retardo del ULTIMO  -  retardo del primero",
                 10, VERDE, "start", "700", SANS))
    c.append(txt(x0 + 16, y0 + 20, "cada punto es un datagrama: se genera cada 40 ms",
                 10, GRIS))
    c.append(txt(x0 + 16, y0 + 38, "(columna) pero llega cuando puede (fila).", 10, GRIS))
    c.append(txt(x0 + 16, y0 + 66, "El receptor DEBERIA emitirlos a ritmo constante, no "
                                   "cuando llegan.", 10, GRIS))
    c.append(txt(x0 + 16, y0 + 82, "Por eso los mete en un buffer y los reproduce en t_i + p.",
                 10, GRIS))
    c.append(txt(x0 + 16, y0 + PH - 24, "Sin buffer, el oyente oye un corte cada vez que un "
                                        "datagrama tarda mas que el anterior.",
                 10, NARANJA, "start", "700", SANS))
    return svg(W, H, "".join(c), "Buffer de jitter: por que p es el maximo, no el promedio")


def tuneles():
    W, H = 760, 330
    c = [defs()]
    c.append(txt(30, 36, "Que envuelve a que:", 11, GRIS, "start", "700", SANS))
    Y = 56
    capas = [("Host A   192.168.1.25", 30, 120, CLARO, BORDE),
             ("paquete original:  192.168.1.25  ->  10.0.0.7", 30, 620, "#dceaf3", CELESTE),
             ("cabecera IPsec (nueva)", 96, 554, "#fbe0d0", NARANJA),
             ("cabecera IP exterior:  200.10.10.1  ->  200.10.10.2", 162, 488, "#f7d9c8", NARANJA)]
    for s, x, w, fill, st in capas:
        c.append(caja(x, Y, w, 30, s, fill, st, 10, TXT, 3, False))
        Y += 32
    c.append(caja(620, 56, 110, 90, "Host B\\n10.0.0.7", CLARO, BORDE, 10))
    c.append(txt(385, 196, "Cada capa de overlay AUMENTA el tamano del paquete y "
                           "RESTA MTU disponible.", 10, NARANJA, "middle", "700", SANS))
    c.append(txt(385, 216, "Por eso hace falta clamp MSS en el borde de las redes con jumbo frames.", 10, GRIS, "middle"))
    c.append(txt(385, 244, "Y rompe el aislamiento de capas: el router exterior tiene "
                           "que ENENDER IPsec", 10, GRIS, "middle"))
    c.append(txt(385, 262, "para forwarding, cuando su unico trabajo deberia ser mirar la "
                           "IP de destino.", 10, GRIS, "middle"))
    c.append(txt(385, 292, "Tipos: site-to-site (always on) y remoto (el usuario inicia).",
                 10, AZUL2, "middle", "700", SANS))
    return svg(W, H, "".join(c), "Un tunel y por que complica el MTU")


# ------------------------------------------------------- 16. pila de capa 7

def pila_http():
    """Del clic a la primera respuesta: DNS, TCP, TLS y HTTP."""
    W, H = 720, 400
    c = [defs()]
    pasos = [("DNS", "resolver www.ejemplo.com -> 93.184.216.34", VERDE, "1 RTT"),
             ("TCP", "handshake de 3 vias contra el puerto 80", AZUL2, "1 RTT"),
             ("TLS", "handshake, certificado, claves de sesion", NARANJA, "2 RTT"),
             ("HTTP", "GET /index.html  ->  200 OK", ROJO, "1 RTT")]
    y = 56
    for nombre, det, col, rtt in pasos:
        c.append(caja(40, y, 110, 42, nombre, col, col, 13, TXTCLARO, 5, True))
        c.append(caja(166, y, 330, 42, det, "#f7f9fa", BORDE, 11, TXT, 4))
        c.append(caja(512, y, 110, 42, rtt, "#fff", col, 11, col, 4, True))
        y += 56
    c.append(caja(40, y, 110, 42, "luego", "#eef2f5", GRIS, 12, GRIS, 5, True))
    c.append(caja(166, y, 456, 42,
                  "una conexion TCP por objeto en HTTP/1.1, o multiplexada en h2/h3",
                  "#f7f9fa", BORDE, 11, TXT, 4))
    y += 62
    c.append(caja(40, y, 582, 44,
                  "En total: ~5 RTT antes de recibir el primer byte de la pagina.",
                  "#e9f4ed", VERDE, 12, TXT, 5, True))
    c.append(txt(40, y + 66, "Por eso importan la cache, las cookies de sesion y la "
                             "conexion persistente:", 10, GRIS))
    c.append(txt(40, y + 84, "cada RTT ahorrado se siente en el tiempo de carga.", 10, GRIS))
    return svg(W, H, "".join(c), "Del clic a la primera respuesta")


# ------------------------------------------------------- 17. SNMP / gestión

def modelo_snmp():
    W, H = 780, 350
    c = [defs()]
    c.append(caja(290, 46, 200, 48, "Gestor / NMS", "#f7d9c8", NARANJA, 13, TXT, 6, True))
    agentes = [(50, "Router 1"), (310, "Switch 2"), (570, "Servidor 3")]
    for x, n in agentes:
        c.append(caja(x, 200, 160, 44, n, CLARO, CELESTE, 11, TXT, 5, True))
        c.append(caja(x, 248, 160, 30, "agente", "#dceaf3", CELESTE, 10, GRIS, 4))
    # traps (arriba): el agente avisa sin que le pregunten
    c.append(f'<line x1="130" y1="104" x2="130" y2="146" stroke="{VERDE}" stroke-width="1.8"/>')
    c.append(f'<line x1="650" y1="104" x2="650" y2="146" stroke="{VERDE}" stroke-width="1.8"/>')
    c.append(f'<line x1="130" y1="146" x2="650" y2="146" stroke="{VERDE}" stroke-width="1.8"/>')
    c.append(ar(130, 146, 390, 96))
    c.append(txt(30, 168, "traps (push):  no solicitadas. El agente avisa cuando quiere.",
                 10, VERDE, "start", "700", SANS))
    c.append(txt(30, 184, "Problema: no podes confiar en que lleguen, y no sabes quien esta caido.",
                 9, VERDE))
    # polling (abajo): el gestor va preguntando uno por uno
    ybus = 296
    for x in (130, 390, 650):
        c.append(f'<line x1="{x}" y1="278" x2="{x}" y2="{ybus}" stroke="{AZUL2}" stroke-width="1.8"/>')
    c.append(ar(650, ybus, 130, 278))
    c.append(txt(30, ybus + 14, "polling (pull):  GET / GETNEXT / GETBULK.", 10, AZUL2,
                 "start", "700", SANS))
    c.append(txt(30, ybus + 30, "El gestor pregunta dispositivo por dispositivo: con muchos, "
                                "se demora.", 9, AZUL2))
    c.append(txt(390, 24, "El agente vive en el dispositivo gestionado y la MIB es el esquema "
                          "de los datos (OIDs jerarquicos).", 10, GRIS, "middle"))
    return svg(W, H, "".join(c), "Modelo de gestion: gestor, agentes y MIB")


# ------------------------------------------------------------ 21. indice

def ipv6_modelos():
    """Unicast, multicast y anycast en IPv6, y por que anycast no es un tipo."""
    W, H = 780, 340
    c = [defs()]
    CW, GAP = 210, 45
    cols = [("Unicast", "un emisor -> un receptor", "2001:db8::1", AZUL2, 1),
            ("Multicast", "ff00::/8 con jerarquia de ambito", "ff02::1:ff00:1", VERDE, 1),
            ("Anycast", "varios nodos con la MISMA IP", "2001:db8::1", NARANJA, 3)]
    for k, (nombre, det, ej, col, nn) in enumerate(cols):
        x = 34 + k * (CW + GAP)
        c.append(caja(x, 48, CW, 34, nombre, col, col, 12, TXTCLARO, 5, True))
        c.append(txt(x + CW / 2, 104, det, 10, TXT, "middle"))
        c.append(caja(x + 15, 118, CW - 30, 30, ej, CLARO, BORDE, 10))
        # nodos
        yb = 205
        for j2 in range(nn):
            cx = x + CW / 2 + (j2 - (nn - 1) / 2) * 52
            c.append(f'<circle cx="{cx}" cy="{yb}" r="17" fill="#fff" stroke="{col}" '
                     f'stroke-width="2.2"/>')
        c.append(ar(x + CW / 2, 152, x + CW / 2, yb - 22, col))
        if k == 2:
            c.append(txt(x + CW / 2, yb + 40, "el router elige el mas cercano", 9,
                         NARANJA, "middle", "700", SANS))
    c.append(txt(W / 2, 296, "anycast NO es un tipo de direccion: es un SERVICIO que se le "
                             "da a un grupo de nodos.", 11, ROJO, "middle", "700", SANS))
    c.append(txt(W / 2, 314, "Es lo que usan los root servers de DNS y los resolvers "
                             "publicos (1.1.1.1, 8.8.8.8).", 10, GRIS, "middle"))
    return svg(W, H, "".join(c), "Unicast, multicast y anycast en IPv6")


def los_tres_servicios():
    """Los tres servicios de seguridad y la diferencia fina entre integridad y no repudio."""
    W, H = 780, 356
    c = [defs()]
    filas = [("Confidencialidad", "solo el emisor y el receptor entienden el mensaje",
              "cifrado simetrico o asimetrico", AZUL2),
             ("Integridad", "el mensaje no fue alterado en transito",
              "hash / HMAC / AEAD", VERDE),
             ("No repudio", "el emisor no puede negar haberlo enviado",
              "firma digital + identidad vinculable", NARANJA)]
    y = 40
    for nombre, defi, como, col in filas:
        c.append(caja(34, y, 196, 48, nombre, col, col, 12, TXTCLARO, 5, True))
        c.append(txt(248, y + 19, defi, 11, TXT))
        c.append(txt(248, y + 39, "se logra con: " + como, 10, GRIS))
        y += 62
    c.append(f'<rect x="34" y="{y+14}" width="712" height="70" rx="6" fill="#fdf3ec" '
             f'stroke="{NARANJA}"/>')
    c.append(txt(50, y + 40, "La diferencia fina entre integridad y no repudio NO es el "
                             "algoritmo.", 11, NARANJA, "start", "700", SANS))
    c.append(txt(50, y + 62, "Es QUIEN controla la clave privada: si la tiene solo Alicia, "
                             "Alicia no puede negar.", 11, NARANJA))
    c.append(txt(34, y + 106, "Y los tres se resuelven juntos en TLS, no por separado.",
                 11, AZUL, "start", "700", SANS))
    c.append(txt(34, y + 126, "Sumalos: autenticacion (soy quien digo ser) y control de acceso.",
                 10, GRIS))
    return svg(W, H, "".join(c), "Los tres servicios de seguridad")


def handshake_tls():
    """Handshake de TLS 1.3 en un RTT."""
    W, H = 740, 260
    c = [defs()]
    pasos = [("1 RTT extra", "ClientHello: versiones, cipher suites, key share"),
             ("1 RTT", "ServerHello + Certificate + Finished"),
             ("0 RTT", "ya se pueden mandar datos de aplicacion")]
    y = 46
    for nombre, det in pasos:
        c.append(caja(34, y, 150, 42, nombre, AZUL, AZUL, 11, TXTCLARO, 5, True))
        c.append(txt(200, y + 26, det, 11, TXT))
        y += 58
    c.append(txt(34, y + 24, "TLS 1.3 cambio: solo AEAD, sin compresion, sin renegociacion, "
                             "y forward secrecy obligatorio.", 10, GRIS))
    c.append(txt(34, y + 42, "El certificado sigue siendo X.509: lo que cambio fue el "
                             "intercambio de claves.", 10, GRIS))
    return svg(W, H, "".join(c), "Handshake de TLS 1.3 en un RTT")


def indice_modulo():
    """Los 6 bloques del curso."""
    W, H = 760, 330
    c = [defs()]
    filas = [("A · Fundamentos", "1-7", "redes, capas, retardo, Nyquist/Shannon", AZUL2),
             ("B · Aplicacion", "8-15", "HTTP, DNS, correo, sockets, DHCP", VERDE),
             ("C · Transporte", "16-23", "UDP, TCP, control de congestion", NARANJA),
             ("D · Red", "24-37", "IPv4, subnetting, ruteo, BGP, IPv6", ROJO),
             ("E · Enlace", "38-43", "framing, CRC, ARQ, acceso, 802.11", CELESTE),
             ("F · Servicios", "44-48", "multimedia, QoS, SNMP, seguridad", VERDE)]
    y = 48
    for nombre, rango, cont, col in filas:
        c.append(caja(34, y, 190, 38, nombre, col, col, 11, TXTCLARO, 4, True))
        c.append(txt(244, y + 24, rango, 11, TXT, "start", "700", SANS))
        c.append(txt(300, y + 24, cont, 10, GRIS))
        y += 45
    return svg(W, H, "".join(c), "Los 6 bloques del curso")


# ------------------------------------------------------------- registro

DIAGRAMAS = {
    "pila-capas": pila_capas,
    "encapsulacion": encapsulacion,
    "topologia-nat": topologia_natsubredes,
    "topologia-empresa": topologia_empresa,
    "sec-arp": sec_arp,
    "sec-dns": sec_dns,
    "sec-handshake": sec_handshake,
    "grafico-cwnd": grafico_cwnd,
    "grafico-aloha": grafico_aloha,
    "subnet-and": diagrama_subnet,
    "cabecera-tcp": cabecera_tcp,
    "cabecera-ipv4": cabecera_ipv4,
    "cabecera-ipv6": cabecera_ipv6,
    "dijkstra": grafico_dijkstra,
    "crc-polinomio": crc_polinomio,
    "cubetas": cubetas,
    "mpls-hop": mpls_hop,
    "csma-cd": csma_cd,
    "csma-ca": csma_ca,
    "nat-tabla": nat_tabla,
    "tuneles": tuneles,
    "pila-http": pila_http,
    "modelo-snmp": modelo_snmp,
    "voip-buffer": voip_buffer,
    "ipv6-modelos": ipv6_modelos,
    "los-3-servicios": los_tres_servicios,
    "handshake-tls": handshake_tls,
    "indice-modulos": indice_modulo,
}


if __name__ == "__main__":
    import pathlib
    out = pathlib.Path(__file__).resolve().parent.parent / ".build" / "diagramas"
    out.mkdir(parents=True, exist_ok=True)
    for nombre, fn in DIAGRAMAS.items():
        (out / f"{nombre}.svg").write_text(fn(), encoding="utf-8")
        print(f"{nombre:22} ok")
