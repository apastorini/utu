# -*- coding: utf-8 -*-
"""
Presentación fase_3 — Bearer token: del riesgo al sender-constrained
Basada en la estructura de Gemini: 3 actos, 25 minutos, sin adjetivos.
Cada slide tiene guion en notas del ponente.
"""
import os
import sys

from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR, MSO_AUTO_SIZE
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, "Slides template - OWASP UY.pptx")
IMGDIR = os.path.join(HERE, "img_deck")
PPTX_OUT = os.path.join(HERE, "presentacion_owasp_uy_fase3.pptx")
PDF_OUT = os.path.join(HERE, "presentacion_owasp_uy_fase3.pdf")

NAVY = RGBColor(0x1B, 0x27, 0x38)
BLUE = RGBColor(0x74, 0xAA, 0xDC)
GRAY = RGBColor(0x7A, 0x7A, 0x7A)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT = RGBColor(0xEA, 0xF2, 0xFB)

BODY = (571550, 1524000, 8250900, 4167300)
EYEBROW = (452438, 205000, 7600000, 260000)
FOOT = (452438, 5830000, 8600000, 240000)
PAGE = (11000000, 5830000, 900000, 240000)

TOTAL = 20


def get_ph(slide, idx):
    for ph in slide.placeholders:
        if ph.placeholder_format.idx == idx:
            return ph
    return None


def drop_ph(slide, idx):
    ph = get_ph(slide, idx)
    if ph is not None:
        ph._element.getparent().remove(ph._element)


def delete_slide(prs, index):
    sldIdLst = prs.slides._sldIdLst
    sldId = list(sldIdLst)[index]
    rId = sldId.get(
        "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"
    )
    prs.part.drop_rel(rId)
    sldIdLst.remove(sldId)


def set_title(slide, text):
    ph = get_ph(slide, 1)
    tf = ph.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    size = min(32.0, max(20.0, 1230.0 / max(len(text), 1)))
    for r in p.runs:
        r.font.name = "Lato"
        r.font.size = Pt(size)
        r.font.bold = True
        r.font.color.rgb = NAVY
    return ph


def add_eyebrow(slide, text):
    left, top, width, height = EYEBROW
    box = slide.shapes.add_textbox(left, top, width, height)
    p = box.text_frame.paragraphs[0]
    r = p.add_run()
    r.text = text.upper()
    r.font.name = "Lato"
    r.font.size = Pt(12.5)
    r.font.bold = True
    r.font.color.rgb = RGBColor(0x2E, 0x6D, 0xA4)


def fill_bullets(slide, bullets):
    ph = get_ph(slide, 2)
    tf = ph.text_frame
    tf.word_wrap = True
    tf.auto_size = MSO_AUTO_SIZE.NONE
    n = len(bullets)
    size = 24 if n <= 3 else 22 if n == 4 else 20 if n == 5 else 18
    for i, item in enumerate(bullets):
        lead, rest = item if isinstance(item, tuple) else (None, item)
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        for r in list(p.runs):
            r._r.getparent().remove(r._r)
        p.space_after = Pt(4)
        p.line_spacing = 1.02
        for text, bold in ((lead, True), (rest, False)):
            if not text:
                continue
            r = p.add_run()
            r.text = text
            r.font.name = "Lato"
            r.font.size = Pt(size)
            r.font.bold = bold
            r.font.color.rgb = NAVY
    return ph


def add_picture_fit(slide, path):
    l, t, w, h = BODY
    iw, ih = Image.open(path).size
    sc = min(w / iw, h / ih)
    nw, nh = int(iw * sc), int(ih * sc)
    slide.shapes.add_picture(path, l + (w - nw) // 2, t + (h - nh) // 2, nw, nh)


def _cell(cell, text, size, bold, color, fill):
    cell.fill.solid()
    cell.fill.fore_color.rgb = fill
    cell.vertical_anchor = MSO_ANCHOR.MIDDLE
    cell.margin_left = Emu(80000)
    cell.margin_right = Emu(60000)
    cell.margin_top = Emu(20000)
    cell.margin_bottom = Emu(20000)
    tf = cell.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    r = p.add_run()
    r.text = text
    r.font.name = "Lato"
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.color.rgb = color


def add_table(slide, headers, rows, ratios, size=13):
    l, t, w, h = BODY
    t = t + 200000
    h = h - 400000
    ncols = len(headers)
    gf = slide.shapes.add_table(len(rows) + 1, ncols, l, t, w, h)
    table = gf.table
    table.first_row = True
    table.horz_banding = False
    total = sum(ratios)
    for j, ratio in enumerate(ratios):
        table.columns[j].width = Emu(int(w * ratio / total))
    for j, htext in enumerate(headers):
        _cell(table.cell(0, j), htext, size, True, WHITE, NAVY)
    for i, row in enumerate(rows, start=1):
        fill = WHITE if i % 2 else LIGHT
        for j, val in enumerate(row):
            _cell(table.cell(i, j), val, size, j == 0, NAVY, fill)
    return table


def add_footer(slide, source, page):
    left, top, width, height = FOOT
    box = slide.shapes.add_textbox(left, top, width, height)
    r = box.text_frame.paragraphs[0].add_run()
    r.text = "Fuente: " + source
    r.font.size = Pt(9)
    r.font.name = "Lato"
    r.font.color.rgb = GRAY

    left, top, width, height = PAGE
    box = slide.shapes.add_textbox(left, top, width, height)
    p = box.text_frame.paragraphs[0]
    p.alignment = PP_ALIGN.RIGHT
    r = p.add_run()
    r.text = "%d / %d" % (page, TOTAL)
    r.font.size = Pt(9)
    r.font.name = "Lato"
    r.font.color.rgb = GRAY


def add_notes(slide, text):
    slide.notes_slide.notes_text_frame.text = text


def new_content(prs, spec, page):
    slide = prs.slides.add_slide(prs.slide_layouts[3])
    set_title(slide, SHORT.get(spec["title"], spec["title"]))
    if spec.get("eyebrow"):
        add_eyebrow(slide, spec["eyebrow"])
    if spec.get("figure"):
        drop_ph(slide, 2)
        add_picture_fit(slide, os.path.join(IMGDIR, spec["figure"]))
    elif spec.get("table"):
        drop_ph(slide, 2)
        headers, rows, ratios = spec["table"]
        add_table(slide, headers, rows, ratios, size=spec.get("tsize", 13))
    else:
        fill_bullets(slide, spec["bullets"])
    add_footer(slide, spec["source"], page)
    add_notes(slide, spec["notes"])
    return slide


def new_cover(prs, spec):
    slide = prs.slides.add_slide(prs.slide_layouts[2])
    t0 = get_ph(slide, 0)
    t0.left, t0.top, t0.width, t0.height = (
        Emu(773900), Emu(1200000), Emu(10900000), Emu(2400000))
    t0.text_frame.word_wrap = True
    p = t0.text_frame.paragraphs[0]
    p.text = spec["title"]
    for r in p.runs:
        r.font.name = "Lato"
        r.font.size = Pt(48)
        r.font.bold = True
        r.font.color.rgb = NAVY
    t2 = get_ph(slide, 2)
    t2.left, t2.top, t2.width, t2.height = (
        Emu(773900), Emu(3720000), Emu(10900000), Emu(1200000))
    t2.text_frame.word_wrap = True
    p2 = t2.text_frame.paragraphs[0]
    p2.text = spec["subtitle"]
    for r in p2.runs:
        r.font.name = "Lato"
        r.font.size = Pt(30)
        r.font.bold = True
        r.font.italic = False
        r.font.color.rgb = RGBColor(0x2E, 0x6D, 0xA4)
    drop_ph(slide, 1)
    add_notes(slide, spec["notes"])
    return slide


# ------------------------------------------------------------------ guiones
G = {
    "cover": "Buenas tardes. 25 minutos, tres actos. El título juega con «al infinito y más allá»: el token bearer es el billete que nunca muere y el «más allá» es lo que viene después. Sin rodeos: por qué un Authorization: Bearer en el header ya no alcanza y qué hacemos al respecto.",
    "acto1": "Planteo del conflicto. El token bearer es un billete al portador: quien lo tiene, lo usa. Si se filtra por XSS, logs o almacenamiento inseguro, el atacante entra sin importar desde dónde llame. El RFC 6749 sección 10.3 lo admite: el servidor de recursos no puede confirmar que el token se emitió a quien lo presenta.",
    "robo": "El robo del token no es teórico. Facebook 2018: la función «Ver como» generó 50 millones de access tokens robables. Starbucks 2019: claves API expuestas en GitHub. En ambos casos el token se usó sin restricciones porque no estaba atado a nada.",
    "que_no_cubre": "Qué no cubre el bearer. No cifra el payload (JWT es base64). No autoriza por sí solo: la autorización es otro capítulo. No previene replay. No protege contra XSS. No verifica el dispositivo. No es MFA. El token solo responde una pregunta: ¿es válido? Nada más.",
    "linea_tiempo": "La línea de tiempo. Pasado: Basic Auth y cookies con estado en el servidor. Presente: OAuth 2.0, JWT sin estado, bearer como estándar. Más allá: mTLS y DPoP, donde el token queda atado al cliente que lo solicitó.",
    "acto2": "Acto II: seguridad dinámica. La autenticación no es un interruptor de encendido/apagado. Es un flujo continuo: el usuario entra con contraseña, pero para operaciones sensibles la API debe exigir más. Ahí entra MFA Step-Up.",
    "paso_arriba": "MFA Step-Up: el mecanismo. RFC 9470. La API evalúa la transacción: es sensible, el token dice autenticación simple. Responde 401 con WWW-Authenticate y acr_values. El frontend redirige al IdP. El usuario pasa segundo factor. Nuevo token con acr actualizado. Reintento exitoso.",
    "que_pide": "Qué pide el Step-Up en el token. acr (Authentication Context Class Reference) y amr (Authentication Methods References) son los claims the dicen cómo se autenticó el usuario. Si acr dice contraseña simple y la operación exige MFA, el token no sirve. No es el token: es el contexto de autenticación dentro del token.",
    "m2m": "Máquina a máquina: sin humano para factorizar. Cuando la invocador es un microservicio o un job de CI, no hay segundo factor que mostrar. El equivalente es mTLS con certificados X.509 o firmado de peticiones con claves asimétricas (Private Key JWT).",
    "acto3": "Acto III: el ecosistema mobile. Las apps móviles están en manos del atacante. Pueden modificar el APK, desactivar SSL pinning, extraer secretars. El cliente «Frankenstein» simula ser la app legítima y llama a la API directly.",
    "pkce": "PKCE: el candado del código. RFC 7636. El cliente genera un code_verifier, envía su hash como code_challenge, y prueba el verifier al canjear el código. Si un atacante intercepta el código, no lo puede canjear sin el verifier. Hoy es obligatorio en clientes públicos.",
    "attestation": "App Attestation: la prueba de integridad. Play Integrity API en Android, DeviceCheck en iOS. El servidor de attestation verifica que el binario no fue modificado y emite un token de attestation. La API lo verifica antes de procesar solicitudes sensibles.",
    "acto3_final": "Acto III: el clímax mobile. App Attestation verifica la integridad del binario. PKCE protege el código de autorización. DPoP ata el token a una clave privada del dispositivo. Las tres capas juntas: el cliente Frankenstein se queda fuera.",
    "dpop_vs_mtls": "DPoP contra mTLS. mTLS opera en capa 4: certificado X.509 en el handshake TLS, token atado al certificado vía claim cnf. Robo de token inútil sin el certificado. Gestión de PKI compleja.",
    "dpop": "DPoP: la prueba en capa 7. El cliente genera un par de claves dinámicamente. El token se ata a la clave pública. Cada request incluye un JWT firmado con la clave privada en un header DPoP. Sin PKI, sin certificados de red, funciona a través de proxies y WAFs.",
    "tabla_dpop": "DPoP contra mtls: la comparación. mTLS: capa 4, certificado X.509, ideal para M2M y microservicios, gestión de PKI compleja. DPoP: capa 7, JWT en header, ideal para SPAs y móviles, sin PKI pero con sobrecarga computacional.",
    "arquitectura": "Arquitectura: el token vive en el ecosistema. TLS protege en tránsito pero no contra XSS ni logs. Gateway valida firma, expiración y aud. Zero Trust: cada microservicio autoriza según su lógica de negocio.",
    "canal_seguro": "Canal seguro y gateway: sus límites. TLS no protege contra robo en el cliente. El gateway es la primera línea: throttling, WAF, validación de firma. El error común: el gateway valida y los microservicios confían ciegamente. Zero Trust: propagar claims y autorizar en cada capa.",
    "caso_uruguay": "El caso uruguayo. ID Uruguay usa OIDC con bearer tokens. Cualquier integración con tokens de larga vida sin rotación es un riesgo. Cualquier SPA con token en localStorage es un riesgo. Las mitigaciones de esta charla aplican igual: DPoP, PKCE, Step-Up.",
    "takeaways": "Tres acciones para mañana. Primero: auditar la vida de los tokens de acceso y refresh. Segundo: revisar dónde se almacenan los tokens en clientes públicos. Tercero: identificar operaciones sensibles y planificar Step-Up. El token bearer es el presente. El sender-constrained es el siguiente paso.",
    "cierre": "El token se acaba. El riesgo no. Autenticar es la puerta. Autorizar es la cerradura. La seguridad no está en el string: está en el sistema. Gracias."}


COVER = {
    "type": "cover",
    "title": "Bearer Token: del riesgo al sender-constrained",
    "subtitle": "25 minutos, tres actos",
    "notes": G["cover"],
}

DECK = [
    {"eyebrow": "Acto I", "title": "El conflicto: el billete al portador",
     "bullets": [
        ("Posesión = autorización: ", "el token se presenta y se acepta."),
        ("No se verifica el dispositivo ", "ni el cliente que lo usa."),
        ("Si se filtra: ", "quien lo tiene, lo usa."),
     ],
     "source": "RFC 6749, Bearer Token Usage (octubre 2012).", "notes": G["acto1"]},

    {"eyebrow": "Acto I", "title": "El robo del token: casos documentados",
     "bullets": [
        ("Facebook (2018): ", "50 millones de tokens robados vía «Ver como»."),
        ("Starbucks (2019): ", "claves API expuestas en GitHub."),
        ("En ambos: ", "el token se usó sin restricciones."),
     ],
     "source": "Meta Security Report (2018); HackerOne (2019).", "notes": G["robo"]},

    {"eyebrow": "Acto I", "title": "Qué no cubre el bearer token",
     "bullets": [
        ("No cifra: ", "JWT es base64, no cifrado."),
        ("No autoriza: ", "es otro capítulo."),
        ("No previene replay: ", "interceptado = reutilizado."),
        ("No verifica dispositivo ", "ni cliente."),
        ("No es MFA: ", "la autenticación ya pasó."),
     ],
     "source": "RFC 6749 §10.3 (2012).", "notes": G["que_no_cubre"]},

    {"eyebrow": "Línea de tiempo", "title": "De Basic Auth al sender-constrained",
     "figure": "d_family.png",
     "source": "RFC 2617 (1999); RFC 6749 (2012); RFC 8705 (2020); RFC 9449 (2023).", "notes": G["linea_tiempo"]},

    {"eyebrow": "Acto II", "title": "Seguridad dinámica: MFA Step-Up",
     "bullets": [
        ("La autenticación no es binaria: ", "es un flujo continuo."),
        ("Operaciones sensibles: ", "exigen re-autenticación."),
        ("Mecanismo: ", "RFC 9470, Step-Up Authentication Challenge."),
     ],
     "source": "RFC 9470 (2023); NIST SP 800-63-4 (2025).", "notes": G["acto2"]},

    {"eyebrow": "Acto II", "title": "Step-Up: el flujo 401 y reintento",
     "bullets": [
        ("1. La API evalúa: ", "transacción sensible, acr insuficiente."),
        ("2. Responde 401: ", "WWW-Authenticate con acr_values."),
        ("3. El frontend redirige al IdP ", "para segundo factor."),
        ("4. Nuevo token con acr actualizado. ", "Reintento exitoso."),
     ],
     "source": "RFC 9470 (2023).", "notes": G["paso_arriba"]},

    {"eyebrow": "Acto II", "title": "Los claims acr y amr",
     "bullets": [
        ("acr: ", "Authentication Context Class Reference."),
        ("amr: ", "Authentication Methods References."),
        ("Dicen cómo se autenticó, ", "no solo quién."),
     ],
     "source": "RFC 8176 (2017); OIDC Core (2014).", "notes": G["que_pide"]},

    {"eyebrow": "Acto II", "title": "M2M: sin humano para factorizar",
     "bullets": [
        ("El invocador es un microservicio ", "o job de CI."),
        ("No hay segundo factor: ", "el equivalente es mTLS."),
        ("Certificados X.509 ", "o Private Key JWT para firmado de peticiones."),
     ],
     "source": "RFC 8705 (2020); RFC 7523 (2015).", "notes": G["m2m"]},

    {"eyebrow": "Acto III", "title": "El ecosistema mobile: apps modificadas",
     "bullets": [
        ("Las apps están en manos del atacante: ", "modificables, descompilables."),
        ("Riesgo: ", "cliente Frankenstein que simula ser la app legítima."),
        ("Desactivan SSL pinning, ", "extraen secretos, llaman a la API."),
     ],
     "source": "OWASP Mobile Top 10 (2024).", "notes": G["acto3"]},

    {"eyebrow": "Acto III", "title": "PKCE: el candado del código",
     "bullets": [
        ("code_verifier: ", "string aleatorio generado por el cliente."),
        ("code_challenge: ", "hash del verifier, enviado al pedir el código."),
        ("Al canjear: ", "el verifier prueba la posesión."),
        ("Obligatorio hoy ", "en clientes públicos (RFC 9700)."),
     ],
     "source": "RFC 7636 (2015); RFC 9700 (2025).", "notes": G["pkce"]},

    {"eyebrow": "Acto III", "title": "App Attestation: prueba de integridad",
     "bullets": [
        ("Android: ", "Play Integrity API."),
        ("iOS: ", "DeviceCheck / App Attest."),
        ("Verifica el binario no fue modificado ", "y emite token de attestation."),
        ("La API lo verifica ", "antes de operaciones sensibles."),
     ],
     "source": "Google Play Integrity; Apple DeviceCheck.", "notes": G["attestation"]},

    {"eyebrow": "Acto III", "title": "Mobile: las tres capas juntas",
     "bullets": [
        ("App Attestation: ", "el binario es legítimo."),
        ("PKCE: ", "el código no se puede reutilizar."),
        ("DPoP: ", "el token no sirve en otro dispositivo."),
        ("Cliente Frankenstein: ", "sin binario legítimo, sin PKCE, sin DPoP."),
     ],
     "source": "Google; Apple; RFC 7636; RFC 9449.", "notes": G["acto3_final"]},

    {"eyebrow": "Comparativa", "title": "DPoP contra mTLS: la diferencia",
     "table": (
        ["Característica", "mTLS", "DPoP"],
        [
            ["Capa OSI", "Capa 4 (Transporte)", "Capa 7 (Aplicación)"],
            ["Mecanismo", "Certificado X.509 en TLS", "JWT firmado en header HTTP"],
            ["Gestión de claves", "Compleja (PKI)", "Sin PKI, par dinámico"],
            ["Ideal para", "M2M, microservicios", "SPAs, móviles"],
        ],
        [1.2, 1.3, 1.3],
     ),
     "tsize": 13,
     "source": "RFC 8705 (2020); RFC 9449 (2023).", "notes": G["dpop_vs_mtls"]},

    {"eyebrow": "Comparativa", "title": "DPoP: prueba de posesión en HTTP",
     "bullets": [
        ("Par de claves dinámico: ", "generado en el momento."),
        ("Token atado a la clave pública. ", "La privada permanece en el dispositivo."),
        ("Header DPoP en cada request: ", "JWT firmado con método y URL."),
        ("Funciona a través de proxies, WAFs ", "y terminaciones TLS."),
     ],
     "source": "RFC 9449 (2023).", "notes": G["dpop"]},

    {"eyebrow": "Comparativa", "title": "DPoP contra mTLS: resumen",
     "bullets": [
        ("mTLS: ", "capa 4, certificados, PKI, ideal M2M."),
        ("DPoP: ", "capa 7, headers HTTP, ideal clientes públicos."),
        ("Ambos atan el token ", "al cliente legítimo."),
        ("Robar el token ", "sin la prueba criptográfica: inútil."),
     ],
     "source": "RFC 8705 (2020); RFC 9449 (2023).", "notes": G["tabla_dpop"]},

    {"eyebrow": "Arquitectura", "title": "El ecosistema: TLS, Gateway, Zero Trust",
     "figure": "d_circles.png",
     "source": "OWASP API Security Top 10 (2023); NIST SP 800-207 (2020).", "notes": G["arquitectura"]},

    {"eyebrow": "Arquitectura", "title": "Canal seguro y gateway: sus límites",
     "bullets": [
        ("TLS: ", "protege en tránsito, no en el cliente."),
        ("Gateway: ", "throttling, WAF, validación de firma, revocación."),
        ("Error común: ", "microservicios confían ciegamente."),
        ("Zero Trust: ", "propagar claims, autorizar en cada capa."),
     ],
     "source": "OWASP API Top 10 (2023); NIST SP 800-207 (2020).", "notes": G["canal_seguro"]},

    {"eyebrow": "Caso Uruguay", "title": "ID Uruguay y el ecosistema local",
     "bullets": [
        ("OIDC con bearer tokens: ", "tokens de larga vida sin rotación."),
        ("SPAs con token en localStorage: ", "robo por XSS."),
        ("Mitigaciones: ", "DPoP, PKCE, Step-Up para operaciones sensibles."),
     ],
     "source": "AGESIC / ID Uruguay; OWASP.", "notes": G["caso_uruguay"]},

    {"eyebrow": "Cierre", "title": "Tres acciones para mañana",
     "bullets": [
        ("Uno: ", "auditar la vida de los tokens."),
        ("Dos: ", "revisar almacenamiento en clientes."),
        ("Tres: ", "identificar operaciones sensibles para Step-Up."),
     ],
     "source": "OWASP API Top 10 (2023); RFC 9700 (2025).", "notes": G["takeaways"]},

    {"eyebrow": "Cierre", "title": "El token se acaba. El riesgo no.",
     "bullets": [
        ("Autenticar es la puerta. ", "Autorizar es la cerradura."),
        ("El token bearer es el presente. ", "El sender-constrained es el siguiente paso."),
        ("La seguridad no está en el string: ", "está en el sistema."),
     ],
     "source": "OWASP; RFC 9449; RFC 9700.", "notes": G["cierre"]},
]


SHORT = {
    "El conflicto: el billete al portador": "El billete al portador",
    "El robo del token: casos documentados": "El robo del token",
    "Qué no cubre el bearer token": "Qué no cubre el bearer",
    "De Basic Auth al sender-constrained": "De Basic al sender-constrained",
    "Seguridad dinámica: MFA Step-Up": "Seguridad dinámica: Step-Up",
    "Step-Up: el flujo 401 y reintento": "Step-Up: flujo 401 y reintento",
    "Los claims acr y amr": "Claims acr y amr",
    "M2M: sin humano para factorizar": "M2M: sin factorizar",
    "El ecosistema mobile: apps modificadas": "Apps modificadas",
    "PKCE: el candado del código": "PKCE: candado del código",
    "App Attestation: prueba de integridad": "App Attestation",
    "Mobile: las tres capas juntas": "Mobile: tres capas",
    "DPoP contra mTLS: la diferencia": "DPoP vs mTLS",
    "DPoP: prueba de posesión en HTTP": "DPoP: prueba en HTTP",
    "DPoP contra mTLS: resumen": "DPoP vs mTLS: resumen",
    "El ecosistema: TLS, Gateway, Zero Trust": "TLS, Gateway, Zero Trust",
    "Canal seguro y gateway: sus límites": "Canal seguro: límites",
    "ID Uruguay y el ecosistema local": "ID Uruguay",
    "Tres acciones para mañana": "Tres acciones",
    "El token se acaba. El riesgo no.": "El token se acaba. El riesgo no.",
}


def build():
    prs = Presentation(TEMPLATE)
    new_cover(prs, COVER)
    page = 2
    for spec in DECK:
        new_content(prs, spec, page)
        page += 1
    for _ in range(4):
        delete_slide(prs, 0)
    prs.save(PPTX_OUT)
    print("OK pptx ->", PPTX_OUT, "| slides:", len(prs.slides._sldIdLst))
    return prs


def export_pdf(pptx_path, pdf_path):
    import pythoncom
    import win32com.client
    pptx_path = os.path.abspath(pptx_path)
    pdf_path = os.path.abspath(pdf_path)
    pythoncom.CoInitialize()
    app = win32com.client.DispatchEx("PowerPoint.Application")
    try:
        app.DisplayAlerts = 1
        pres = app.Presentations.Open(pptx_path, ReadOnly=True, Untitled=False, WithWindow=False)
        pres.SaveAs(pdf_path, 32)
        pres.Close()
        print("OK pdf  ->", pdf_path)
    finally:
        app.Quit()
        pythoncom.CoUninitialize()


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    build()
    export_pdf(PPTX_OUT, PDF_OUT)
