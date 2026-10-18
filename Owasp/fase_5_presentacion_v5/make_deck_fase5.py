# -*- coding: utf-8 -*-
"""
Presentación fase_5 — Bearer token al infinito y más allá
Tema: la falsa sensación de seguridad.
Imágenes integradas en el flujo, no como anexos.
Incluye todas las tecnologías anteriores a bearer token.
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
IMGDIR = os.path.join(HERE, "img")
IMGDIR2 = os.path.join(HERE, "img_deck")
PPTX_OUT = os.path.join(HERE, "presentacion_owasp_uy_fase5_v2.pptx")
PDF_OUT = os.path.join(HERE, "presentacion_owasp_uy_fase5_v2.pdf")

NAVY = RGBColor(0x1B, 0x27, 0x38)
BLUE = RGBColor(0x74, 0xAA, 0xDC)
GRAY = RGBColor(0x7A, 0x7A, 0x7A)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT = RGBColor(0xEA, 0xF2, 0xFB)

BODY = (571550, 1524000, 8250900, 4167300)
EYEBROW = (452438, 205000, 7600000, 260000)
FOOT = (452438, 5830000, 8600000, 240000)
PAGE = (11000000, 5830000, 900000, 240000)

TOTAL = 46


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
    elif spec.get("figure2"):
        drop_ph(slide, 2)
        add_picture_fit(slide, os.path.join(IMGDIR2, spec["figure2"]))
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
    "cover": "Buenas tardes. El título es «Bearer token al infinito y más allá». El infinito es lo que viene después del bearer. El más allá es la seguridad completa. El tema central: la falsa sensación de seguridad. Tener un endpoint con Authorization: Bearer no significa que seas seguro. Vamos a ver por qué, desde el principio.",
    "conflicto": "El conflicto. Cada tecnología resolvió algo y dejó algo abierto. Basic resolvió la autenticación mínima pero la credencial viaja en cada request. Cookies resolvieron el estado pero trajeron CSRF y XSS. OAuth 2.0 resolvió la delegación pero creó el bearer. La pregunta no es si el token es seguro, sino qué problema resuelve y qué no.",
    "basic": "HTTP Basic: RFC 2617, junio de 1999. Manda usuario y contraseña en Base64 en cada petición. Base64 no es cifrado: está codificado. Resuelve: autenticación mínima sin estado. No resuelve: la credencial viaja en cada request, no hay logout, no hay revocación. Se sigue usando: en sistemas internos y como client_secret_basic en OAuth.",
    "digest": "HTTP Digest: RFC 7616, agosto de 2015. Manda un hash con un nonce en lugar de la contraseña en claro. Resuelve: no mandar la contraseña en claro. No resuelve: el modelo sigue siendo credencial en cada request, no hay forma limpia de delegar. Se sigue usando: prácticamente en desuso.",
    "cookies": "Cookies: Netscape, 1996. RFC 6265, abril de 2011. Un identificador de sesión que el navegador guarda y reenvía. Resuelve: recordar quién sos sin repetir la contraseña. No resuelve: CSRF, robo de sesión por XSS, fijación de sesión. Se sigue usando: en navegadores, con HttpOnly, Secure y SameSite.",
    "api_keys": "API keys: AWS, 2006. Un secreto estático que identifica al cliente. Resuelve: identificar aplicaciones sin un servidor de identidad. No resuelve: no expira, no distingue permisos, si se filtra es impersonación directa. Se sigue usando: en servicios internos y APIs de terceros.",
    "saml": "SAML 2.0: OASIS, marzo de 2005. Aserciones XML firmadas para federación. Resuelve: SSO entre aplicaciones, identidad federada. No resuelve: XML pesado, difícil de implementar en móviles y SPAs. Se sigue usando: en banca, gobierno y SaaS corporativo.",
    "oauth1": "OAuth 1.0: RFC 5849, abril de 2010. Firmaba cada request con HMAC-SHA1. Resuelve: un request robado no se podía reutilizar. No resuelve: era muy difícil de implementar bien. Se sigue usando: prácticamente abandonado.",
    "bearer": "Bearer token: RFC 6749 y RFC 6750, octubre de 2012. Un string que se presenta en la cabecera Authorization. Resuelve: simplicidad, no hay que firmar cada request. No resuelve: quien tiene el token, lo usa. La falsa sensación de seguridad nace aquí: bearer no significa seguro, significa portador.",
    "falsa_seguridad": "La falsa sensación de seguridad. El bearer token resuelve la delegación de autorización. No resuelve: autorización, cifrado, anti-replay, MFA, gestión de sesión. Tener Authorization: Bearer no significa que la API es seguridad. Significa que quien tiene el token, entra.",
    "que_no_cubre": "Qué no cubre el bearer. No cifra el payload. No autoriza por sí solo. No previene replay. No verifica dispositivo. No es MFA. No protege contra XSS. El token solo responde una pregunta: ¿es válido? Nada más.",
    "jwt": "JWT: RFC 7519, mayo de 2015. Tres partes en base64url: header, payload, signature. Resuelve: claims autenticables sin estado. No resuelve: el payload no está cifrado, cualquiera lo lee. Y guarda una trampa: si el validador confía en el alg del token, el atacante elige el algoritmo.",
    "base64": "Base64 no es cifrado: es codificación. Muchos protocolos como HTTP, email SMTP o XML fueron diseñados para transportar texto de 7 bits (ASCII). No pueden transportar bytes arbitrarios directamente. Un byte 0xFF no es un carácter ASCII válido. Base64 convierte cualquier secuencia de bytes en texto ASCII de 7 bits, de modo que puede viajar por esos protocolos sin corromperse. Opera en grupos de 3 bytes (24 bits) y los divide en 4 grupos de 6 bits. Cada grupo se mapea a un carácter del alfabeto Base64: A-Z, a-z, 0-9, +, /. Cualquier sistema que solo entiende texto puede transportar una imagen sin problema. El receptor aplica Base64-decode y recupera los bytes originales. La diferencia: cifrado oculta información y requiere clave; codificación solo representa datos en otro formato, no requiere clave y es reversible por cualquiera. Base64 es como poner un sobre de papel transparente: cambia la presentación, no el contenido.",
    "linea_tiempo": "La línea de tiempo. Cada tecnología nació como respuesta a un problema. Basic, Digest, cookies, API keys, SAML, OAuth 1.0, bearer. Ninguna reemplazó a la anterior: se apilan. Cada capa sigue viva.",
    "acto2": "Acto II: la seguridad dinámica. La autenticación no es un interruptor. Es un flujo continuo. El usuario entra con contraseña, pero para operaciones sensibles la API debe exigir más. Ahí entra MFA Step-Up.",
    "paso_arriba": "MFA Step-Up: RFC 9470. La API evalúa la transacción: es sensible, el token dice autenticación simple. Responde 401 con WWW-Authenticate y acr_values. El frontend redirige al IdP. El usuario pasa segundo factor. Nuevo token con acr actualizado. Reintento exitoso.",
    "m2m": "Máquina a máquina: no hay humano para factorizar. Cuando el invocador es un microservicio, el equivalente es mTLS con certificados X.509 o firmado de peticiones con Private Key JWT.",
    "acto3": "Acto III: el ecosistema mobile. Las apps están en manos del atacante. Pueden modificar el APK, desactivar SSL pinning, extraer secretos. El cliente Frankenstein simula ser la app legítima.",
    "pkce": "PKCE: RFC 7636, agosto de 2015. El cliente genera un code_verifier, envía su hash como code_challenge, y prueba el verifier al canjear el código. Si un atacante intercepta el código, no lo puede canjear sin el verifier.",
    "attestation": "App Attestation: Play Integrity API en Android, DeviceCheck en iOS. Verifica que el binario no fue modificado y emite un token de attestation. La API lo verifica antes de operaciones sensibles.",
    "acto3_final": "Mobile: las tres capas juntas. App Attestation verifica la integridad del binario. PKCE protege el código. DPoP ata el token a una clave privada del dispositivo. El cliente Frankenstein se queda fuera.",
    "dpop_vs_mtls": "DPoP contra mTLS. mTLS opera en capa 4: certificado X.509 en el handshake TLS. DPoP opera en capa 7: JWT firmado en un header HTTP. mTLS es ideal para M2M. DPoP es ideal para clientes públicos.",
    "dpop": "DPoP: RFC 9449, octubre de 2023. El cliente genera un par de claves dinámicamente. El token se ata a la clave pública. Cada request incluye un JWT firmado con la clave privada. Sin PKI, funciona a través de proxies y WAFs.",
    "arquitectura": "Arquitectura: el token vive en el ecosistema. TLS protege en tránsito. Gateway valida firma, expiración y aud. Zero Trust: cada microservicio autoriza según su lógica de negocio.",
    "caso_uruguay": "El caso uruguayo. ID Uruguay usa OIDC con bearer tokens. Cualquier integración con tokens de larga vida sin rotación es un riesgo. Las mitigaciones de esta charla aplican igual: DPoP, PKCE, Step-Up.",
    "cierre": "El token se acaba. El riesgo no. La falsa sensación de seguridad es pensar que bearer significa seguro. Bearer significa portador. La seguridad está en el sistema: autorización, cifrado, anti-replay, MFA, gestión de sesión. Gracias.",
    "img_timeline": "La línea de tiempo completa. Cada tecnología con su RFC y su año. Ninguna reemplazó a la anterior: se apilan.",
    "img_token_family": "La familia de tokens. Authorization code, access token, refresh token e ID token. Cada uno con su destinatario y su vida.",
    "img_jwt": "Anatomía de un JWT. Header, payload, signature. Todo en base64url. El payload no está cifrado: está firmado.",
    "img_transport": "Dónde viaja el token. Cabecera, cuerpo o query. RFC 9700 prohíbe tokens en URIs.",
    "img_mfa": "La MFA protege un instante. Después, el token vive solo. Step-Up, DPoP y App Attestation son las respuestas para el uso.",
    "img_person_system": "Persona y sistema: dos preguntas distintas. Para la persona probamos que un humano se autenticó. Para el sistema probamos que un workload concreto pidió el token.",
    "img_sender": "Del bearer al sender-constrained. Token Binding (2018), mTLS (2020), DPoP (2023). La evolución es clara: atar el token a su portador.",
    "img_oauth": "Los flujos de OAuth. Authorization Code con PKCE es el recomendado para clientes públicos. Client Credentials es para M2M.",
    "img_protocol_stack": "La pila de protocolos. HTTP, TLS, OAuth/OIDC, JWT, JOSE. Cada capa resuelve un problema. Ninguna resuelve todos.",
    "img_lifecycle": "El ciclo de vida del token. Emisión, transporte, almacenamiento, uso, renovación, revocación, expiración. Defender una API es cubrir todas las etapas.",
    "img_owasp": "OWASP API Security Top 10. BOLA, Broken Authentication, BOPLA, Unrestricted Resource Consumption, BFLA, Sensitive Business Flows, SSRF, Misconfiguration, Improper Inventory, Unsafe Consumption.",
    "img_reference": "Arquitectura de referencia. Cliente, Gateway, IAM, Microservicios, Datos. Cada capa tiene su responsabilidad.",
    "img_circles": "Alrededor del token hay un sistema entero. Gateway, IAM, MFA, Rate Limiting, WAF, API Keys, OAuth/OIDC, JWT, Scopes, RBAC/ABAC, Secret Manager, mTLS/DPoP, Observabilidad, Zero Trust, BOLA.",
    "img_d_circles": "El ecosistema completo. Cada círculo es un componente que puede fallar. La seguridad de la API es la suma de todas las piezas.",
    "img_d_family": "La familia de tokens en detalle. Los cuatro artefactos con sus roles, vidas y destinos.",
    "img_d_jwt": "JWT en detalle. Validar todo: header, payload, signature. No solo la firma.",
    "img_d_mfa": "MFA en detalle. El segundo factor protege el momento de la emisión. Después, el token vive solo.",
    "img_d_owasp": "OWASP Top 10 en detalle. Cada riesgo con su forma de probarlo y su defensa.",
    "img_d_pop": "DPoP en detalle. El cliente firma cada request con su clave privada. El servidor valida la prueba y no acepta el token sin ella.",
    "img_d_refresh": "Refresh token en detalle. Rotación: cada uso emite uno nuevo y el viejo se invalida.",
    "img_d_transport": "Transporte del token en detalle. Cabecera es el lugar correcto. Query está prohibido por RFC 9700.",
}


COVER = {
    "type": "cover",
    "title": "Bearer token al infinito y más allá",
    "subtitle": "La falsa sensación de seguridad",
    "notes": G["cover"],
}

DECK = [
    {"eyebrow": "Conflicto", "title": "El conflicto: cada tecnología resuelve algo",
     "bullets": [
        ("Basic: ", "resuelve autenticación, no resuelve robo."),
        ("Cookies: ", "resuelve estado, no resuelve CSRF."),
        ("OAuth 2.0: ", "resuelve delegación, no resuelve posesión."),
        ("La pregunta: ", "¿qué problema resuelve y qué no?"),
     ],
     "source": "RFC 2617; RFC 6265; RFC 6749.", "notes": G["conflicto"]},

    {"eyebrow": "Antes del bearer", "title": "HTTP Basic: RFC 2617 (1999)",
     "bullets": [
        ("Qué resuelve: ", "autenticación mínima sin estado."),
        ("Qué no resuelve: ", "credencial viaja en cada request."),
        ("Base64 no es cifrado: ", "está codificado, cualquiera lo lee."),
        ("Se sigue usando: ", "sistemas internos, client_secret_basic."),
     ],
     "source": "RFC 2617 (1999); RFC 7616 (2015).", "notes": G["basic"]},

    {"eyebrow": "Antes del bearer", "title": "HTTP Digest: RFC 7616 (2015)",
     "bullets": [
        ("Qué resuelve: ", "no mandar la contraseña en claro."),
        ("Qué no resuelve: ", "el modelo de credencial en cada request."),
        ("Hash con nonce: ", "mejora el secreto, no el modelo."),
        ("Se sigue usando: ", "prácticamente en desuso."),
     ],
     "source": "RFC 7616 (2015).", "notes": G["digest"]},

    {"eyebrow": "Antes del bearer", "title": "Cookies: Netscape (1996) → RFC 6265 (2011)",
     "bullets": [
        ("Qué resuelve: ", "recordar quién sos sin repetir la contraseña."),
        ("Qué no resuelve: ", "CSRF, robo por XSS, fijación de sesión."),
        ("Atributos: ", "HttpOnly, Secure, SameSite."),
        ("Se sigue usando: ", "en navegadores web."),
     ],
     "source": "RFC 6265 (2011).", "notes": G["cookies"]},

    {"eyebrow": "Antes del bearer", "title": "API keys: AWS (2006)",
     "bullets": [
        ("Qué resuelve: ", "identificar aplicaciones sin servidor de identidad."),
        ("Qué no resuelve: ", "no expira, no distingue permisos."),
        ("Si se filtra: ", "impersonación directa."),
        ("Se sigue usando: ", "servicios internos, APIs de terceros."),
     ],
     "source": "AWS API keys (2006).", "notes": G["api_keys"]},

    {"eyebrow": "Antes del bearer", "title": "SAML 2.0: OASIS (2005)",
     "bullets": [
        ("Qué resuelve: ", "SSO, identidad federada, firmas."),
        ("Qué no resuelve: ", "XML pesado, difícil en móviles."),
        ("Se sigue usando: ", "banca, gobierno, SaaS corporativo."),
     ],
     "source": "SAML 2.0 (OASIS, 2005).", "notes": G["saml"]},

    {"eyebrow": "Antes del bearer", "title": "OAuth 1.0: RFC 5849 (2010)",
     "bullets": [
        ("Qué resuelve: ", "request robado no se puede reutilizar."),
        ("Qué no resuelve: ", "muy difícil de implementar bien."),
        ("Firmaba cada request: ", "HMAC-SHA1 con nonce y timestamp."),
        ("Se sigue usando: ", "prácticamente abandonado."),
     ],
     "source": "RFC 5849 (2010).", "notes": G["oauth1"]},

    {"eyebrow": "El bearer", "title": "Bearer token: RFC 6749 y 6750 (2012)",
     "bullets": [
        ("Qué resuelve: ", "simplicidad, no firmar cada request."),
        ("Qué no resuelve: ", "quien tiene el token, lo usa."),
        ("La falsa sensación: ", "bearer no significa seguro, significa portador."),
     ],
     "source": "RFC 6749; RFC 6750 (2012).", "notes": G["bearer"]},

    {"eyebrow": "La tesis", "title": "La falsa sensación de seguridad",
     "bullets": [
        ("Bearer resuelve: ", "delegación de autorización."),
        ("Bearer no resuelve: ", "autorización, cifrado, anti-replay, MFA."),
        ("Authorization: Bearer ", "no significa que la API sea segura."),
        ("Significa: ", "quien tiene el token, entra."),
     ],
     "source": "RFC 6749 §10.3 (2012).", "notes": G["falsa_seguridad"]},

    {"eyebrow": "La tesis", "title": "Qué no cubre el bearer token",
     "bullets": [
        ("No cifra: ", "JWT es base64, no cifrado."),
        ("No autoriza: ", "es otro capítulo."),
        ("No previene replay: ", "interceptado = reutilizado."),
        ("No es MFA: ", "la autenticación ya pasó."),
     ],
     "source": "RFC 6749 §10.3 (2012).", "notes": G["que_no_cubre"]},

    {"eyebrow": "JWT", "title": "JWT: RFC 7519 (2015)",
     "bullets": [
        ("Qué resuelve: ", "claims autenticables sin estado."),
        ("Qué no resuelve: ", "payload no está cifrado."),
        ("La trampa: ", "si el validador confía en el alg del token, el atacante elige."),
     ],
     "source": "RFC 7519 (2015); RFC 8725 (2020).", "notes": G["jwt"]},

    {"eyebrow": "Base64", "title": "Base64: codificación, no cifrado",
     "bullets": [
        ("El problema: ", "HTTP, SMTP y XML transportan texto de 7 bits (ASCII)."),
        ("La solución: ", "Base64 convierte bytes arbitrarios en texto ASCII."),
        ("Cómo funciona: ", "3 bytes → 4 grupos de 6 bits → caracteres Base64."),
        ("La diferencia: ", "cifrado oculta y requiere clave; codificación no."),
        ("La regla: ", "Base64 es un sobre transparente: cambia presentación, no contenido."),
     ],
     "source": "RFC 4648 (2006).", "notes": G["base64"]},

    {"eyebrow": "Línea de tiempo", "title": "La línea de tiempo",
     "figure": "01_timeline.png",
     "source": "OWASP; IETF; OASIS.", "notes": G["linea_tiempo"]},

    {"eyebrow": "Acto II", "title": "Seguridad dinámica: MFA Step-Up",
     "bullets": [
        ("La autenticación no es binaria: ", "es un flujo continuo."),
        ("Operaciones sensibles: ", "exigen re-autenticación."),
        ("Mecanismo: ", "RFC 9470, Step-Up Authentication Challenge."),
     ],
     "source": "RFC 9470 (2023).", "notes": G["acto2"]},

    {"eyebrow": "Acto II", "title": "Step-Up: el flujo 401 y reintento",
     "bullets": [
        ("1. La API evalúa: ", "transacción sensible, acr insuficiente."),
        ("2. Responde 401: ", "WWW-Authenticate con acr_values."),
        ("3. El frontend redirige al IdP ", "para segundo factor."),
        ("4. Nuevo token con acr actualizado. ", "Reintento exitoso."),
     ],
     "source": "RFC 9470 (2023).", "notes": G["paso_arriba"]},

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

    {"eyebrow": "Arquitectura", "title": "El ecosistema: TLS, Gateway, Zero Trust",
     "figure": "13_circles.png",
     "source": "OWASP API Security Top 10 (2023); NIST SP 800-207 (2020).", "notes": G["arquitectura"]},

    {"eyebrow": "Caso Uruguay", "title": "ID Uruguay y el ecosistema local",
     "bullets": [
        ("OIDC con bearer tokens: ", "tokens de larga vida sin rotación."),
        ("SPAs con token en localStorage: ", "robo por XSS."),
        ("Mitigaciones: ", "DPoP, PKCE, Step-Up para operaciones sensibles."),
     ],
     "source": "AGESIC / ID Uruguay; OWASP.", "notes": G["caso_uruguay"]},

    {"eyebrow": "Cierre", "title": "El token se acaba. El riesgo no.",
     "bullets": [
        ("La falsa sensación de seguridad: ", "pensar que bearer significa seguro."),
        ("Bearer significa: ", "portador."),
        ("La seguridad está en el sistema: ", "autorización, cifrado, anti-replay, MFA."),
     ],
     "source": "OWASP; RFC 9449; RFC 9700.", "notes": G["cierre"]},

    {"eyebrow": "Detalle", "title": "La familia de tokens",
     "figure": "02_token_family.png",
     "source": "RFC 6749 §4.1 y §5 (2012); OIDC Core (2014).", "notes": G["img_token_family"]},

    {"eyebrow": "Detalle", "title": "Anatomía de un JWT",
     "figure": "03_jwt_anatomy.png",
     "source": "RFC 7519 (2015); RFC 8725 (2020).", "notes": G["img_jwt"]},

    {"eyebrow": "Detalle", "title": "Dónde viaja el token",
     "figure": "04_transport.png",
     "source": "RFC 6750 §2 (2012); RFC 9700 (enero 2025).", "notes": G["img_transport"]},

    {"eyebrow": "Detalle", "title": "La MFA protege un instante",
     "figure": "05_mfa_timeline.png",
     "source": "NIST SP 800-63-4 (julio 2025); OIDC Core (2014).", "notes": G["img_mfa"]},

    {"eyebrow": "Detalle", "title": "Persona y sistema: dos preguntas",
     "figure": "06_person_vs_system.png",
     "source": "NIST SP 800-63-4 (2025); GitGuardian (2026).", "notes": G["img_person_system"]},

    {"eyebrow": "Detalle", "title": "Del bearer al sender-constrained",
     "figure": "07_sender_constrained.png",
     "source": "RFC 8471-8473 (2018); RFC 8705 (2020); RFC 9449 (2023).", "notes": G["img_sender"]},

    {"eyebrow": "Detalle", "title": "Los flujos de OAuth",
     "figure": "08_oauth_flows.png",
     "source": "RFC 6749 (2012); RFC 7636 (2015).", "notes": G["img_oauth"]},

    {"eyebrow": "Detalle", "title": "La pila de protocolos",
     "figure": "09_protocol_stack.png",
     "source": "OWASP; IETF.", "notes": G["img_protocol_stack"]},

    {"eyebrow": "Detalle", "title": "El ciclo de vida del token",
     "figure": "10_lifecycle.png",
     "source": "RFC 6749; RFC 7009; RFC 9700.", "notes": G["img_lifecycle"]},

    {"eyebrow": "Detalle", "title": "OWASP API Top 10",
     "figure": "11_owasp_top10.png",
     "source": "OWASP API Security Top 10, edición 2023.", "notes": G["img_owasp"]},

    {"eyebrow": "Detalle", "title": "Arquitectura de referencia",
     "figure": "12_reference_arch.png",
     "source": "OWASP; NIST SP 800-207.", "notes": G["img_reference"]},

    {"eyebrow": "Detalle", "title": "El ecosistema completo",
     "figure": "13_circles.png",
     "source": "OWASP API Security Top 10 (2023).", "notes": G["img_circles"]},

    {"eyebrow": "Detalle", "title": "El ecosistema en detalle",
     "figure2": "d_circles.png",
     "source": "OWASP API Security Top 10 (2023).", "notes": G["img_d_circles"]},

    {"eyebrow": "Detalle", "title": "La familia de tokens en detalle",
     "figure2": "d_family.png",
     "source": "RFC 6749 §4.1 y §5 (2012); OIDC Core (2014).", "notes": G["img_d_family"]},

    {"eyebrow": "Detalle", "title": "JWT en detalle",
     "figure2": "d_jwt.png",
     "source": "RFC 7519 (2015); RFC 8725 (2020).", "notes": G["img_d_jwt"]},

    {"eyebrow": "Detalle", "title": "MFA en detalle",
     "figure2": "d_mfa.png",
     "source": "NIST SP 800-63-4 (julio 2025); OIDC Core (2014).", "notes": G["img_d_mfa"]},

    {"eyebrow": "Detalle", "title": "OWASP Top 10 en detalle",
     "figure2": "d_owasp.png",
     "source": "OWASP API Security Top 10, edición 2023.", "notes": G["img_d_owasp"]},

    {"eyebrow": "Detalle", "title": "DPoP en detalle",
     "figure2": "d_pop.png",
     "source": "RFC 9449 (2023).", "notes": G["img_d_pop"]},

    {"eyebrow": "Detalle", "title": "Refresh token en detalle",
     "figure2": "d_refresh.png",
     "source": "RFC 6749 §10.4 (2012); RFC 7009 (2013); RFC 9700 (2025).", "notes": G["img_d_refresh"]},

    {"eyebrow": "Detalle", "title": "Transporte del token en detalle",
     "figure2": "d_transport.png",
     "source": "RFC 6750 §2 (2012); RFC 9700 (enero 2025).", "notes": G["img_d_transport"]},
]


SHORT = {
    "El conflicto: cada tecnología resuelve algo": "El conflicto",
    "HTTP Basic: RFC 2617 (1999)": "HTTP Basic (1999)",
    "HTTP Digest: RFC 7616 (2015)": "HTTP Digest (2015)",
    "Cookies: Netscape (1996) → RFC 6265 (2011)": "Cookies (1996-2011)",
    "API keys: AWS (2006)": "API keys (2006)",
    "SAML 2.0: OASIS (2005)": "SAML 2.0 (2005)",
    "OAuth 1.0: RFC 5849 (2010)": "OAuth 1.0 (2010)",
    "Bearer token: RFC 6749 y 6750 (2012)": "Bearer (2012)",
    "La falsa sensación de seguridad": "La falsa sensación de seguridad",
    "Qué no cubre el bearer token": "Qué no cubre el bearer",
    "JWT: RFC 7519 (2015)": "JWT (2015)",
    "Base64: codificación, no cifrado": "Base64: no es cifrado",
    "La línea de tiempo": "La línea de tiempo",
    "Seguridad dinámica: MFA Step-Up": "Seguridad dinámica: Step-Up",
    "Step-Up: el flujo 401 y reintento": "Step-Up: flujo 401 y reintento",
    "M2M: sin humano para factorizar": "M2M: sin factorizar",
    "El ecosistema mobile: apps modificadas": "Apps modificadas",
    "PKCE: el candado del código": "PKCE: candado del código",
    "App Attestation: prueba de integridad": "App Attestation",
    "Mobile: las tres capas juntas": "Mobile: tres capas",
    "DPoP contra mTLS: la diferencia": "DPoP vs mTLS",
    "DPoP: prueba de posesión en HTTP": "DPoP: prueba en HTTP",
    "El ecosistema: TLS, Gateway, Zero Trust": "TLS, Gateway, Zero Trust",
    "ID Uruguay y el ecosistema local": "ID Uruguay",
    "El token se acaba. El riesgo no.": "El token se acaba. El riesgo no.",
    "La familia de tokens": "La familia de tokens",
    "Anatomía de un JWT": "Anatomía de un JWT",
    "Dónde viaja el token": "Dónde viaja el token",
    "La MFA protege un instante": "La MFA protege un instante",
    "Persona y sistema: dos preguntas": "Persona y sistema",
    "Del bearer al sender-constrained": "Del bearer al sender-constrained",
    "Los flujos de OAuth": "Los flujos de OAuth",
    "La pila de protocolos": "La pila de protocolos",
    "El ciclo de vida del token": "El ciclo de vida del token",
    "OWASP API Top 10": "OWASP API Top 10",
    "Arquitectura de referencia": "Arquitectura de referencia",
    "El ecosistema completo": "El ecosistema completo",
    "El ecosistema en detalle": "El ecosistema en detalle",
    "La familia de tokens en detalle": "La familia de tokens en detalle",
    "JWT en detalle": "JWT en detalle",
    "MFA en detalle": "MFA en detalle",
    "OWASP Top 10 en detalle": "OWASP Top 10 en detalle",
    "DPoP en detalle": "DPoP en detalle",
    "Refresh token en detalle": "Refresh token en detalle",
    "Transporte del token en detalle": "Transporte del token en detalle",
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
