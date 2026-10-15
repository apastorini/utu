# -*- coding: utf-8 -*-
"""
Genera el mazo completo (28 slides) en la plantilla "Slides template - OWASP UY.pptx"
y lo exporta a PDF con PowerPoint (COM).

Versión 2 — Enfoque: "Qué es y qué NO ES la seguridad con bearer token"
- Audiencia: desarrolladores y arquitectos (aunque asistan personas de seguridad)
- Cada slide tiene su guion en las notas del ponente
- Historia limitada a 3 slides (menos de 1/5 del total)
- Énfasis en qué aspectos cubre el bearer y cuáles NO
- Incluye OWASP API Top 10, MFA, mTLS, DPoP, PKCE, gateway vs API

Salida:
    presentacion_owasp_uy_v2.pptx
    presentacion_owasp_uy_v2.pdf
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
PPTX_OUT = os.path.join(HERE, "presentacion_owasp_uy_v2.pptx")
PDF_OUT = os.path.join(HERE, "presentacion_owasp_uy_v2.pdf")

NAVY = RGBColor(0x1B, 0x27, 0x38)
BLUE = RGBColor(0x74, 0xAA, 0xDC)
GRAY = RGBColor(0x7A, 0x7A, 0x7A)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT = RGBColor(0xEA, 0xF2, 0xFB)

# geometría (EMU), tomada de los layouts del template
SUB = (452438, 488075, 8489100, 543300)          # subtítulo (título visible)
BODY = (571550, 1524000, 8250900, 4167300)       # cuerpo
EYEBROW = (452438, 205000, 7600000, 260000)
FOOT = (452438, 5830000, 8600000, 240000)
PAGE = (11000000, 5830000, 900000, 240000)

TOTAL = 28


# ----------------------------------------------------------------- utilidades
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
    # Tamaño para que entre en UNA línea (ancho útil ~8.9in; Lato bold ~0.5 em).
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
    slide = prs.slides.add_slide(prs.slide_layouts[3])   # CUSTOM_1_2
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
    slide = prs.slides.add_slide(prs.slide_layouts[2])   # CUSTOM_1_1
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


# --------------------------------------------------------------------- guiones
G = {
  "cover": (
    "Buenas tardes. El título juega con «al infinito y más allá», y no es casual. "
    "Voy a hablar de algo que parece no acabarse nunca —un token que se emite una vez y parece "
    "vivir para siempre— y de lo que hay más allá de él. Pero sobre todo, vamos a hablar de algo "
    "que genera mucha confusión: qué es y qué NO es la seguridad con bearer token. No por tener "
    "un endpoint con bearer algo es seguro. Hay que entender qué aspects están contemplados y "
    "cuáles no."),
  "s2": (
    "Un bearer token es un artefacto de seguridad cuya posesión equivale a autorización. La palabra "
    "«bearer» viene del derecho mercantil: un instrumento al portador da derecho a quien lo tiene "
    "en la mano, sin acreditar identidad. Si perdés un billete, quien lo levanta lo gasta. Si se "
    "filtra un token, quien lo tiene lo usa. No es que el token esté mal hecho: está hecho así "
    "a propósito. Eso ES la seguridad con bearer: un sistema donde la posesión del artefacto es "
    "la única prueba."),
  "s3": (
    "Ahora, ¿qué NO es? Primero: el bearer token NO autentica al usuario. Autenticar fue el paso "
    "anterior, en el login. El token NO cifra los datos: si es un JWT, el payload está en base64, "
    "que cualquiera lee. NO autoriza por sí solo: la autorización es otro capítulo. NO es un "
    "mecanismo anti-replay: si lo interceptás, lo podés reutilizar. NO es MFA: la multifactor "
    "protege el momento de la emisión, no los treinta días siguientes. Tener esto claro es el "
    "punto de partida."),
  "s4": (
    "Nada de esto vive aislado. Alrededor del token hay un sistema entero: un gateway que enruta "
    "y aplica cuotas; un IAM que administra identidades; la MFA que protege el login; el rate "
    "limiting que frena la fuerza bruta; un WAF que filtra ataques; OAuth y OIDC como marco; el "
    "JWT como formato; los scopes y modelos como RBAC o ABAC; un secret manager para las claves; "
    "mTLS y DPoP para atar el token a su portador; la observabilidad para ver qué pasa; y Zero "
    "Trust como filosofía. Si miramos el token aislado, no entendemos nada. La seguridad de una "
    "API es la suma de todas estas piezas, no del token solo."),
  "s5": (
    "Antes de seguir, aclaremos una cosa: no todas las APIs son REST. REST trabaja con recursos y "
    "trae el riesgo de BOLA e IDOR. GraphQL expone un solo endpoint y trae consultas profundas y "
    "sobre-exposición de campos. gRPC es binario y rápido, pero los proxies y WAF no lo inspeccionan "
    "fácil. SOAP usa XML y arrastra XXE. WebSocket abre un canal persistente y suele autenticar "
    "solo al inicio. Y los webhooks y los eventos son push: si no los firmás y validás la URL, "
    "tenés SSRF y replay. La receta de REST no se copia y pega: cada estilo necesita su propio "
    "modelo de seguridad."),
  "s6": (
    "Todo empieza con HTTP sin estado. La primera solución fue mandar usuario y contraseña en cada "
    "petición: Basic, dentro del marco de autenticación de HTTP estandarizado en el RFC 2617, de "
    "junio de 1999. Basic codifica en Base64 —que no es cifrado— y Digest manda un hash con un "
    "nonce. Pero las credenciales siguen viajando en cada request. El segundo intentó fue no "
    "mandar credenciales, sino un identificador de sesión: la cookie, de Netscape (1996), que de "
    "hecho es anterior a la estandarización de Digest, y que recién se estandarizó en el RFC 6265, "
    "en abril de 2011. El estado queda en el servidor."),
  "s7": (
    "En el mundo enterprise, SAML 2.0, estándar OASIS de marzo de 2005, y WS-Security de 2004 "
    "usaban aserciones XML firmadas: eran, en rigor, más seguros que un bearer. El problema no "
    "era la seguridad, era el peso. Después llegó OAuth 1.0, especificación comunitaria de "
    "diciembre de 2007 y RFC 5849 en abril de 2010: no mandaba ningún token copiable, firmaba cada "
    "request con HMAC-SHA1. Robar una petición no servía. Pero canonicalizar parámetros y "
    "compartir secretos entre cada par de servicios era una pesadilla, sobre todo en móviles."),
  "s8": (
    "Este es el dato histórico que casi nadie cuenta: OAuth 2.0 no nació siendo solo bearer. RFC "
    "6749, de octubre de 2012, definía dos tipos: bearer y mac. El tipo mac firmaba componentes "
    "de cada request, igual que OAuth 1.0 o que DPoP después. Pero ese borrador nunca llegó a "
    "RFC: se abandonó. El ecosistema eligió la simplicidad, y con él llegó RFC 6750. La firma "
    "por request era técnicamente superior; el costo de implementación decidió la historia."),
  "s9": (
    "Un error común es hablar de «el token» como si fuera uno solo. En un flujo moderno nacen "
    "hasta cuatro artefactos distintos. El authorization code es un cupón de un solo uso que viaja "
    "por el navegador. El access token es el que se presenta ante la API: vida corta, alcance "
    "limitado. El refresh token es de vida larga y solo sirve contra el endpoint de token, nunca "
    "contra la API. Y el ID token, de OpenID Connect, dice quién es la persona y cómo se "
    "autenticó: no sirve para acceder a recursos. Confundir estos roles es el origen de la "
    "mayoría de las fallas."),
  "s10": (
    "Pongámoslo en una tabla. El código de autorización es de un solo uso y viaja por el "
    "navegador. El access token viaja en cada request a la API y debe vivir minutos u horas. "
    "El refresh token vive semanas o meses, pero solo se presenta al endpoint de token. El ID "
    "token va a la aplicación cliente, no a la API. Regla para escribir en grande: el refresh "
    "token jamás viaja a la API de recursos, y el access token jamás se usa para refrescar. Son "
    "mundos distintos: recursos contra emisión."),
  "s11": (
    "Un JWT son tres partes separadas por puntos, cada una en base64url. Cuidado con el error "
    "clásico: base64 no es cifrado, cualquiera lee el payload. Es como una credencial "
    "plastificada: firmada, no sellada; si necesitás confidencialidad, va JWE. El header lleva el "
    "algoritmo, y ahí nace una familia entera de ataques: si el receptor decide cómo verificar "
    "según lo que dice el token, un atacante elige el algoritmo. La regla, de RFC 8725 y de "
    "OWASP: la política de verificación sale de la configuración, nunca del mensaje."),
  "s12": (
    "Los claims son el contenido. iss dice quién lo emitió; hay que validarlo contra emisores "
    "confiables. aud dice para quién es: es el claim que responde a la pregunta de la norma, "
    "porque si validás aud estrictamente, un token robado emitido para otra app no te sirve. exp "
    "y nbf dicen si está vigente. scope dice qué puede hacer. Y amr y acr, de RFC 8176, dicen "
    "cómo se autenticó: son el puente entre «pasó la MFA» y «el token lo sabe»."),
  "s13": (
    "En 2012, RFC 6750 aceptaba tres transportes: cabecera, cuerpo y parámetro de query. Trece "
    "años después, RFC 9700, las mejores prácticas de enero de 2025, prohíbe transportar access "
    "tokens en URIs. ¿Por qué el cambio? Porque trece años de logs, de cabeceras Referer, de "
    "historiales y de CDN nos enseñaron dónde terminan los tokens que van en una URL. La cabecera "
    "no la manda el navegador sola: es inmune a CSRF. La cookie protege de XSS con HttpOnly, pero "
    "exige mitigar CSRF."),
  "s14": (
    "Esta es la idea que justifica el título. La autenticación multifactor no ocurre en la API: "
    "ocurre en el momento de la emisión. Después de la MFA, todo lo que la API recibe es un "
    "string. El flujo real es: contraseña, MFA en el servidor de autenticación, emisión de "
    "tokens y, al final, un access token. La API no sabe, y no puede saber, si hubo MFA; solo lo "
    "sabe si el emisor puso amr y acr en el token y el validador los revisa. La MFA protege la "
    "generación del artefacto, no su posesión posterior."),
  "s15": (
    "NIST, en su guía de identidad vigente de julio de 2025, dice algo clave: no todos los "
    "autenticadores dan la misma garantía, y el nivel debe ligarse al riesgo. AAL2 exige dos "
    "factores de tipos distintos; AAL3 exige prueba criptográfica de posesión de una clave en "
    "hardware. WebAuthn y las passkeys, recomendación W3C de 2019, resisten el phishing por "
    "diseño: el desafío está atado al origen. Un OTP se puede phishear en tiempo real, y el SMS "
    "es el más débil. Y el step-up, con acr y amr, permite pedir más garantía solo para la "
    "operación sensible."),
  "s16": (
    "Hay tres familias de ataque que la MFA no cubre, porque atacan después de la emisión. Uno: "
    "fatiga de MFA, o push bombing —MITRE lo cataloga como T1621—: el atacante ya tiene la "
    "contraseña y dispara pushes hasta que la víctima aprueba. Dos: phishing adversary-in-the-"
    "middle: ya no roba la contraseña, intercepta la sesión completa que resultó de la MFA. Tres: "
    "infostealers, malware que extrae cookies y tokens del navegador y los reutiliza en otro "
    "equipo; se llama pass-the-cookie. En los tres, la MFA hizo su trabajo; el problema es que el "
    "artefacto se reutiliza."),
  "s17": (
    "Ahora el otro lado, donde está la mayoría del tráfico real. Cuando la API la invoca un "
    "microservicio, un job de CI o un dispositivo, la pregunta «¿quién es el usuario?» no tiene "
    "respuesta, porque no hay usuario. Y no hay MFA aplicable: no hay segundo factor que mostrar. "
    "La pregunta correcta es: ¿qué workload es este, con qué credencial de ciclo de vida corto y "
    "bajo qué contexto habla? El equivalente funcional del MFA para un sistema no es un segundo "
    "factor puntual: es una identidad de workload fuerte, verificable y de vida corta."),
  "s18": (
    "Pongamos las dos columnas juntas. Para la persona probamos que un humano se autenticó ante "
    "un proveedor de identidad; el segundo factor es una passkey, un OTP o un push; el artefacto "
    "es una sesión más un access token corto; y el fallo típico es fatiga, AiTM o robo de sesión. "
    "Para el sistema probamos que un workload concreto pidió el token; no hay segundo factor; el "
    "artefacto es un token corto o una credencial efímera; y el fallo típico son secretos eternos "
    "en repos y CI. Aplicar el marco de uno al otro es el error más caro de la disciplina."),
  "s19": (
    "OWASP nos da el mapa de lo que puede salir mal. Arriba de todo, Api1: BOLA, autorización a "
    "nivel de objeto. Sigue Api2, autenticación rota; Api3, exposición de propiedades, también "
    "llamado mass assignment; Api4, consumo sin límites; Api5, autorización a nivel de función; "
    "Api6, flujos de negocio sensibles; Api7, SSRF; Api8, mala configuración; Api9, inventario "
    "impropio; y Api10, consumo inseguro de terceros. Ninguno de estos es «el token»: son el "
    "sistema alrededor del token. Por eso el token perfecto no alcanza."),
  "s20": (
    "El token resuelve la entrada, pero el edificio tiene más habitaciones. Primero, la "
    "autorización a nivel de objeto: que puedas ver el pedido 5678 y no solo el 1234. Segundo, "
    "la validación de entrada: inyección, SSRF, deserialización, mass assignment. Tercero, el "
    "gateway y el control de tráfico: cuotas, rate limiting y gestión de bots. Cuarto, el "
    "inventario: versiones viejas y APIs fantasma que siguen vivas. Quinto, la cadena de "
    "suministro: secretos en CI y dependencias de terceros. Y sexto, privacidad y cumplimiento: "
    "qué datos personales tratás y qué te exige la norma, incluida la de Uruguay. El token "
    "perfecto no tapa ninguna de estas habitaciones."),
  "s21": (
    "Los casos que siguen son divulgaciones públicas y responsables; no vamos a señalar a nadie, "
    "vamos a observar el modelo. Facebook, 2018: la función «View As» generó un access token del "
    "usuario consultado, no del espectador, y lo dejó embebido en el HTML; se resetearon unos 90 "
    "millones de cuentas. Okta y Cloudflare, 2023: en el ataque al sistema de soporte de Okta, "
    "un session token de un ticket se extrajo y siguió sirviendo, porque no se rotó ni se revocó "
    "a tiempo. En enero de 2022 Okta ya había sufrido otro incidente; en aquel caso Cloudflare no "
    "fue impactado gracias a sus llaves de hardware. Codecov, 2021: un script modificado exportó "
    "las variables de entorno del CI y con ellas los tokens y claves. En los tres, el token no "
    "falló: funcionó como fue diseñado."),
  "s22": (
    "Uber, 2022: credenciales de un contratista compradas en un foro, un SMS que simulaba al área "
    "de IT y la aprobación del push; la MFA protegió el instante, pero la sesión se reutilizó. "
    "BOLA: el atacante presenta su propio token, válido y con MFA si quieren, y cambia el "
    "identificador del objeto en la URL; funciona, y se estima que ronda el 40 % de los ataques "
    "a APIs. Y las clases de JWT mal validado: alg:none, confusión RS256 a HS256, inyección de "
    "kid. Ninguna es culpa del string: son fallas de emisión, autorización o verificación."),
  "s23": (
    "Si el problema es que cualquiera que tenga el token lo usa, la solución es exigir algo más "
    "que la posesión. Hay dos caminos estandarizados. mTLS más token atado al certificado, RFC "
    "8705 de 2020: el token queda ligado al certificado del cliente, así que robarlo no alcanza "
    "sin el par de claves. Y DPoP, RFC 9449 de octubre de 2023: el cliente firma cada request con "
    "su clave privada, con un jti único y los datos del método y la URL. No necesita PKI. Y "
    "esto ya no es opcional: RFC 9700, de 2025, recomienda tokens sender-constrained donde sea "
    "posible."),
  "s24": (
    "El refresh token es el que renueva sin volver a pedir permiso, y su mejor defensa es la "
    "rotación: cada vez que se usa, se emite uno nuevo y el viejo se invalida. Si un atacante lo "
    "usa, el legítimo lo delata en el siguiente intento. RFC 6749 lo sugería en 2012; RFC 9700 "
    "lo vuelve obligatorio para clientes públicos. Y para lo que hay que cortar antes de tiempo "
    "está la revocación, RFC 7009 de 2013; y para tokens opacos, la introspección, RFC 7662. "
    "Regla de oro: no podés tener a la vez un JWT de larga vida y la capacidad de revocarlo. "
    "Elegí uno."),
  "s25": (
    "Una pregunta común: ¿la seguridad va en el gateway o en la API? La respuesta es: en ambos, "
    "pero con roles distintos. El gateway es el portero: aplica rate limiting, WAF, "
    "autenticación básica y geolocalización. La API es el dueño de la casa: valida el token, "
    "verifica la autorización por objeto, aplica la lógica de negocio. Si todo lo delegás al "
    "gateway, la API queda desprotegida ante ataques internos. Si todo lo ponés en la API, "
    "repites lógica en cada servicio. La regla: el gateway filtra, la API decide."),
  "s26": (
    "Juntemos las prácticas. Vida corta y audiencia estricta para el access token; rotación y "
    "revocación para el refresh; scopes mínimos; y observabilidad: ¿este token se usa desde dos "
    "países a la vez? Para las máquinas, la regla es secreto en un secret manager, rotación "
    "automática y nada de claves eternas en repos ni en variables de entorno. Y recordá el dato "
    "que le da urgencia a todo esto: la mayoría de los secretos filtrados no son contraseñas de "
    "personas, son credenciales de sistemas, y más del 60 % de los secretos válidos detectados "
    "en 2022 seguían activos años después."),
  "s27": (
    "Ocho preguntas para llevarse. Uno: ¿el algoritmo de verificación sale de la configuración "
    "y no del token? Dos: ¿validás issuer, audiencia y expiración con tolerancia de reloj corta? "
    "Tres: ¿el access token vive lo que debe vivir? Cuatro: ¿hay rotación y revocación de "
    "refresh? Cinco: ¿la autorización a nivel de objeto está resuelta, o solo la autenticación? "
    "Seis: ¿el token viaja en cabecera y nunca en la URL? Siete: ¿las identidades de máquina "
    "usan credenciales de vida corta y rotación? Ocho: ¿qué queda en los logs? Si alguna respuesta "
    "te incomoda, ahí está tu próximo trabajo."),
  "s28": (
    "Cerremos con tres ideas. Primero: el bearer token es finito: se emite, se roba, se reutiliza "
    "y debe morir; medí su vida, rotalo, revocalo, porque la ausencia de expiración ya es una "
    "vulnerabilidad. Segundo: la MFA protege el momento de la emisión, no los treinta días "
    "siguientes; diseñá para el robo de artefactos, no solo para el robo de contraseñas; y si tu "
    "invocador es un sistema, no busques un MFA, buscá identidad de workload de vida corta. "
    "Tercero: autenticar es la puerta; autorizar es la cerradura; un token perfecto no impide "
    "BOLA. Al fin(ito) y más allá: la seguridad nunca estuvo en el string, estuvo siempre en el "
    "sistema. Gracias."),
}


COVER = {
    "type": "cover",
    "title": "Qué es (y qué NO es) la seguridad con bearer token",
    "subtitle": "Más allá del token: el sistema completo",
    "notes": G["cover"],
}

DECK = [
    {"eyebrow": "1 · ¿Qué es un bearer token?", "title": "Un token es un billete al portador: quien lo tiene, entra",
     "bullets": [
        ("Posesión = autorización. ", "No se verifica la identidad del portador."),
        ("«Bearer» viene del derecho mercantil: ", "instrumento al portador."),
        ("Si se pierde el billete, ", "quien lo levanta lo gasta."),
        ("Si se filtra el token, ", "quien lo tiene lo usa."),
     ],
     "source": "RFC 6750, Bearer Token Usage (octubre 2012).", "notes": G["s2"]},

    {"eyebrow": "1 · ¿Qué es un bearer token?", "title": "Qué NO es un bearer token (y por qué importa)",
     "bullets": [
        ("NO autentica al usuario: ", "eso fue el login, no el token."),
        ("NO cifra los datos: ", "el payload está en base64, no cifrado."),
        ("NO autoriza por sí solo: ", "la autorización es otro capítulo."),
        ("NO es anti-replay: ", "si lo interceptás, lo podés reutilizar."),
     ],
     "source": "RFC 6749; OWASP API Security Top 10 (2023).", "notes": G["s3"]},

    {"eyebrow": "2 · El sistema alrededor de la API", "title": "Alrededor del token hay un sistema entero",
     "figure": "d_circles.png",
     "source": "OWASP API Security Top 10 (2023).", "notes": G["s4"]},

    {"eyebrow": "2 · El sistema alrededor de la API", "title": "No todas las APIs son REST: cada estilo tiene su riesgo",
     "bullets": [
        ("REST — recursos. ", "Riesgo: BOLA / IDOR."),
        ("GraphQL — un endpoint. ", "Consultas profundas y sobre-exposición."),
        ("gRPC — binario. ", "Los WAF no lo inspeccionan fácil."),
        ("SOAP — XML. ", "Arrastra XXE."),
        ("WebSocket — canal. ", "Suele autenticar solo al inicio."),
        ("Webhooks y eventos — push. ", "SSRF y replay si no se firman."),
     ],
     "source": "OWASP API Security Top 10 (2023).", "notes": G["s5"]},

    {"eyebrow": "3 · De dónde venimos · 1/3", "title": "Primero mandábamos la contraseña; después, una cookie",
     "bullets": [
        ("HTTP sin estado: ", "hacía falta recordar quién sos."),
        ("Basic: ", "usuario y contraseña en Base64 en cada request."),
        ("Digest: ", "un hash con nonce; mejora el secreto, no el modelo."),
        ("Cookie (Netscape, 1996): ", "un identificador de sesión; el estado queda en el servidor."),
     ],
     "source": "RFC 2617 (1999) / RFC 7616 (2015); RFC 6265 (2011).", "notes": G["s6"]},

    {"eyebrow": "3 · De dónde venimos · 2/3", "title": "Lo firmado era más seguro; lo simple ganó igual",
     "bullets": [
        ("WS-Security (2004) y SAML 2.0 (2005): ", "aserciones XML firmadas."),
        ("OAuth 1.0 (RFC 5849, 2010): ", "firmaba cada request con HMAC-SHA1."),
        ("Robar una petición no servía.", ""),
        ("Pero canonicalizar y repartir secretos ", "era una pesadilla de integración."),
     ],
     "source": "SAML 2.0 (2005); WS-Security (2004); RFC 5849 (2010).", "notes": G["s7"]},

    {"eyebrow": "3 · De dónde venimos · 3/3", "title": "OAuth 2.0 nació con dos tipos de token; el mundo eligió uno",
     "bullets": [
        ("RFC 6749 (2012) ", "definía dos tipos: bearer y mac."),
        ("El tipo mac ", "firmaba componentes de cada request."),
        ("El borrador MAC se abandonó ", "en febrero de 2012."),
        ("Ganó la simplicidad: ", "con ella llegó RFC 6750."),
     ],
     "source": "RFC 6749 §7.1 (2012); borrador MAC (febrero 2012).", "notes": G["s8"]},

    {"eyebrow": "4 · Anatomía y familia de tokens", "title": "No hay «un token»: hay una familia con roles distintos",
     "figure": "d_family.png",
     "source": "RFC 6749 §4.1 y §5 (2012); OIDC Core (2014).", "notes": G["s9"]},

    {"eyebrow": "4 · Anatomía y familia de tokens", "title": "Cada token tiene su destinatario y su vida",
     "table": (
        ["Token", "Para qué", "Vida", "Dónde viaja"],
        [
            ["Authorization code", "Probar la autorización", "Un solo uso", "Navegador (front channel)"],
            ["Access token", "Llamar a la API", "Minutos u horas", "Cabecera, hacia la API"],
            ["Refresh token", "Renovar sin reautenticar", "Días o semanas", "Solo el endpoint de token"],
            ["ID token", "Decir quién y cómo", "Corto", "App cliente (no la API)"],
        ],
        [1.05, 1.25, 0.85, 1.35],
     ),
     "tsize": 12.5,
     "source": "RFC 6749 §1.5, §4.1, §5, §6 (2012); RFC 7009 (2013).", "notes": G["s10"]},

    {"eyebrow": "4 · Anatomía y familia de tokens", "title": "Está firmado, no sellado: el payload lo lee cualquiera",
     "figure": "d_jwt.png",
     "source": "RFC 7519 (2015); RFC 8725 (2020).", "notes": G["s11"]},

    {"eyebrow": "4 · Anatomía y familia de tokens", "title": "Un JWT bien validado responde cuatro preguntas",
     "bullets": [
        ("¿Quién lo emitió? ", "— iss"),
        ("¿Es para mí? ", "— aud"),
        ("¿Está vigente? ", "— exp / nbf"),
        ("¿Qué permiso tiene? ", "— scope"),
        ("¿Cómo se autenticó? ", "— amr / acr"),
     ],
     "source": "RFC 7519 (2015); RFC 8176 (2017); RFC 9068 (2021).", "notes": G["s12"]},

    {"eyebrow": "4 · Anatomía y familia de tokens", "title": "Trece años tardamos en prohibir el token en la URL",
     "figure": "d_transport.png",
     "source": "RFC 6750 §2 (2012); RFC 9700 (enero 2025).", "notes": G["s13"]},

    {"eyebrow": "5 · La MFA y el bearer", "title": "La MFA protege un instante; el token puede vivir 30 días",
     "figure": "d_mfa.png",
     "source": "NIST SP 800-63-4 (julio 2025); OIDC Core (2014).", "notes": G["s14"]},

    {"eyebrow": "5 · La MFA y el bearer", "title": "Passkeys: el único factor que sobrevive al phishing",
     "bullets": [
        ("NIST AAL1–AAL3: ", "la garantía se liga al riesgo."),
        ("AAL2: ", "dos factores de tipos distintos."),
        ("AAL3: ", "prueba criptográfica de una clave en hardware."),
        ("WebAuthn / passkeys (W3C, 2019): ", "el desafío va atado al origen."),
        ("TOTP se phishea en tiempo real; ", "SMS es el eslabón más débil."),
     ],
     "source": "NIST SP 800-63-4 (julio 2025); WebAuthn (W3C 2019).", "notes": G["s15"]},

    {"eyebrow": "5 · La MFA y el bearer", "title": "Tres modos en que la MFA no salva al bearer",
     "bullets": [
        ("Fatiga de push (MITRE T1621): ", "el atacante ya tiene la contraseña y dispara pushes."),
        ("Phishing AiTM: ", "intercepta la sesión completa que ya pasó la MFA."),
        ("Infostealers y pass-the-cookie: ", "roban y reutilizan el artefacto."),
        ("En los tres, la MFA hizo su trabajo; ", "lo que falla es la posesión."),
     ],
     "source": "MITRE ATT&CK T1621 · T1539; casos públicos.", "notes": G["s16"]},

    {"eyebrow": "5 · La MFA y el bearer", "title": "A una máquina no le podés pedir un segundo factor",
     "bullets": [
        ("El invocador ", "es un microservicio, un job de CI o un dispositivo."),
        ("No hay usuario: ", "no hay segundo factor que mostrar."),
        ("La pregunta correcta: ", "¿qué workload habla y con qué credencial?"),
        ("Mecanismos: ", "client credentials, private_key_jwt, mTLS, DPoP."),
        ("El MFA del sistema ", "es una identidad de vida corta y verificable."),
     ],
     "source": "RFC 6749 §4.4 (2012); RFC 7523 (2015); RFC 8705 (2020).", "notes": G["s17"]},

    {"eyebrow": "5 · La MFA y el bearer", "title": "Persona y sistema: dos preguntas distintas",
     "table": (
        ["", "Persona", "Sistema (M2M)"],
        [
            ["Qué se prueba", "Que un humano se autenticó", "Que un workload pidió el token"],
            ["Segundo factor", "Passkey / OTP / push", "No existe"],
            ["Artefacto", "Sesión + access token corto", "Token corto o credencial efímera"],
            ["Vida típica", "Minutos u horas", "Muy corta, rotada"],
            ["Fallo típico", "Fatiga, AiTM, robo de sesión", "Secretos eternos en repos y CI"],
            ["Revocación", "Cerrar sesión / revocar", "Rotar la credencial"],
        ],
        [1.1, 1.35, 1.5],
     ),
     "tsize": 13,
     "source": "NIST SP 800-63-4 (2025); GitGuardian (2026).", "notes": G["s18"]},

    {"eyebrow": "6 · El mapa del riesgo", "title": "El token es una puerta; los riesgos viven en todo el edificio",
     "figure": "d_owasp.png",
     "source": "OWASP API Security Top 10, edición 2023.", "notes": G["s19"]},

    {"eyebrow": "6 · El mapa del riesgo", "title": "El token es una puerta; el edificio tiene más habitaciones",
     "bullets": [
        ("Autorización a nivel de objeto. ", "Que puedas ver el pedido 5678 y no solo el 1234."),
        ("Validación de entrada: ", "inyección, SSRF, deserialización, mass assignment."),
        ("Gateway y tráfico: ", "cuotas, rate limiting y gestión de bots."),
        ("Inventario: ", "versiones viejas y APIs fantasma que siguen vivas."),
        ("Cadena de suministro: ", "secretos en CI y dependencias de terceros."),
        ("Privacidad y cumplimiento: ", "Ley 18.331, Decreto 66/025 y reporte a CERTuy."),
     ],
     "source": "OWASP API Top 10 (2023); NIST; AGESIC / CERTuy.", "notes": G["s20"]},

    {"eyebrow": "7 · Casos reales · 1/2", "title": "Se emitió mal, no se revocó, se filtró",
     "bullets": [
        ("Facebook «View As» (2018): ", "token emitido al usuario equivocado."),
        ("Okta / Cloudflare (2023): ", "una sesión robada que siguió sirviendo."),
        ("Codecov (2021): ", "tokens del CI exportados por un script modificado."),
        ("En los tres, ", "el token funcionó como fue diseñado."),
     ],
     "source": "Meta (2018); Cloudflare (2023); Codecov (2021).", "notes": G["s21"]},

    {"eyebrow": "7 · Casos reales · 2/2", "title": "Después de aceptarlo, todavía queda trabajo",
     "bullets": [
        ("Uber (2022): ", "la MFA no sobrevive al robo de sesión."),
        ("BOLA: ", "token válido, objeto ajeno (~40 % de los ataques a APIs)."),
        ("JWT mal validado: ", "alg:none, confusión HS/RS, inyección de kid."),
        ("Ninguna falla es del string: ", "son de emisión, autorización o verificación."),
     ],
     "source": "UpGuard / NYT (2022); OWASP (2023); RFC 8725 (2020).", "notes": G["s22"]},

    {"eyebrow": "8 · Del bearer hacia adelante", "title": "Si la posesión no basta, exijamos prueba de posesión",
     "figure": "d_pop.png",
     "source": "RFC 8705 (2020); RFC 9449 (2023); RFC 9700 (2025).", "notes": G["s23"]},

    {"eyebrow": "8 · Del bearer hacia adelante", "title": "La rotación vuelve el refresh un artefacto de un solo uso",
     "figure": "d_refresh.png",
     "source": "RFC 6749 §10.4 (2012); RFC 7009 (2013); RFC 9700 (2025).", "notes": G["s24"]},

    {"eyebrow": "8 · Del bearer hacia adelante", "title": "Gateway vs API: ¿dónde pongo la seguridad?",
     "bullets": [
        ("El gateway es el portero: ", "rate limiting, WAF, autenticación básica, geo."),
        ("La API es el dueño de la casa: ", "valida el token, verifica autorización por objeto."),
        ("Si todo lo delegás al gateway, ", "la API queda desprotegida ante ataques internos."),
        ("Si todo lo ponés en la API, ", "repites lógica en cada servicio."),
        ("La regla: ", "el gateway filtra, la API decide."),
     ],
     "source": "OWASP API Top 10 (2023); NIST SP 800-207 (Zero Trust).", "notes": G["s25"]},

    {"eyebrow": "8 · Del bearer hacia adelante", "title": "El token se acaba; el riesgo no",
     "bullets": [
        ("Access token: ", "vida corta y audiencia estricta."),
        ("Refresh token: ", "rotación y revocación."),
        ("Permisos: ", "mínimo privilegio en los scopes."),
        ("Detección de anomalías: ", "¿este token se usa desde dos países a la vez?"),
        ("Claves de máquina: ", "secret manager y rotación automática."),
     ],
     "source": "RFC 9700 (2025); RFC 7009 (2013); GitGuardian (2026).", "notes": G["s26"]},

    {"eyebrow": "9 · Cierre", "title": "Ocho preguntas antes de dar por segura una API",
     "bullets": [
        "¿El algoritmo de verificación sale de la configuración?",
        "¿Validás iss, aud y exp con tolerancia corta?",
        "¿El access token vive lo que debe?",
        "¿Hay rotación y revocación de refresh?",
        "¿La autorización por objeto está resuelta?",
        "¿El token viaja en cabecera y nunca en la URL?",
        "¿La identidad de máquina es de vida corta?",
        "¿Qué queda en los logs?",
     ],
     "source": "RFC 8725 (2020); RFC 9700 (2025); OWASP API Top 10 (2023).", "notes": G["s27"]},

    {"eyebrow": "9 · Cierre", "title": "Qué es y qué NO es: el resumen final",
     "bullets": [
        ("El token es finito: ", "emitir, rotar, revocar."),
        ("La MFA protege la emisión, ", "no la posesión."),
        ("Autenticar es la puerta; ", "autorizar es la cerradura."),
        ("La seguridad nunca estuvo en el string: ", "está en el sistema."),
     ],
     "source": "Bibliografía consolidada al final de la clase completa.", "notes": G["s28"]},
]


SHORT = {
    "Un token es un billete al portador: quien lo tiene, entra": "Un billete al portador: quien lo tiene, entra",
    "Qué NO es un bearer token (y por qué importa)": "Qué NO es un bearer token",
    "Alrededor del token hay un sistema entero": "Alrededor del token hay un sistema",
    "No todas las APIs son REST: cada estilo tiene su riesgo": "No todas las APIs son REST",
    "Primero mandábamos la contraseña; después, una cookie": "De la contraseña a la cookie",
    "Lo firmado era más seguro; lo simple ganó igual": "Firmar era seguro; ganó lo simple",
    "OAuth 2.0 nació con dos tipos de token; el mundo eligió uno": "OAuth 2.0 nació con dos tipos de token",
    "No hay «un token»: hay una familia con roles distintos": "No hay «un token»: hay una familia",
    "Cada token tiene su destinatario y su vida": "Cada token tiene destino y vida",
    "Está firmado, no sellado: el payload lo lee cualquiera": "Firmado, no sellado",
    "Un JWT bien validado responde cuatro preguntas": "Cuatro preguntas que valida un JWT",
    "Trece años tardamos en prohibir el token en la URL": "El token en la URL quedó prohibido",
    "La MFA protege un instante; el token puede vivir 30 días": "La MFA protege un instante, no 30 días",
    "Passkeys: el único factor que sobrevive al phishing": "Passkeys sobreviven al phishing",
    "Tres modos en que la MFA no salva al bearer": "Tres ataques que la MFA no cubre",
    "A una máquina no le podés pedir un segundo factor": "A una máquina no se le pide un 2FA",
    "Persona y sistema: dos preguntas distintas": "Persona y sistema: dos preguntas",
    "El token es una puerta; los riesgos viven en todo el edificio": "El token es una puerta, no el edificio",
    "El token es una puerta; el edificio tiene más habitaciones": "El edificio tiene más habitaciones",
    "Después de aceptarlo, todavía queda trabajo": "Después de aceptarlo, queda trabajo",
    "Si la posesión no basta, exijamos prueba de posesión": "Atar el token a su portador",
    "La rotación vuelve el refresh un artefacto de un solo uso": "Rotar el refresh lo vuelve de un solo uso",
    "Gateway vs API: ¿dónde pongo la seguridad?": "Gateway vs API: ¿dónde pongo la seguridad?",
    "El token se acaba; el riesgo no": "Vida corta, rotación y revocación",
    "Ocho preguntas antes de dar por segura una API": "Ocho preguntas antes de confiar",
    "Qué es y qué NO es: el resumen final": "Qué es y qué NO es: el resumen final",
}


def build():
    prs = Presentation(TEMPLATE)
    new_cover(prs, COVER)
    page = 2
    for spec in DECK:
        new_content(prs, spec, page)
        page += 1
    # borrar las 4 slides de muestra del template
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
        pres.SaveAs(pdf_path, 32)   # 32 = ppSaveAsPDF
        pres.Close()
        print("OK pdf  ->", pdf_path)
    finally:
        app.Quit()
        pythoncom.CoUninitialize()


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    build()
    export_pdf(PPTX_OUT, PDF_OUT)
