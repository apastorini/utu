# -*- coding: utf-8 -*-
"""
Presentación fase_6 — El arquetipo del bufón
La historia del bufón, su diferencia con el clown, y los paralelos con la seguridad.
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
PPTX_OUT = os.path.join(HERE, "presentacion_owasp_uy_fase6.pptx")
PDF_OUT = os.path.join(HERE, "presentacion_owasp_uy_fase6.pdf")

NAVY = RGBColor(0x1B, 0x27, 0x38)
BLUE = RGBColor(0x74, 0xAA, 0xDC)
GRAY = RGBColor(0x7A, 0x7A, 0x7A)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT = RGBColor(0xEA, 0xF2, 0xFB)

BODY = (571550, 1524000, 8250900, 4167300)
EYEBROW = (452438, 205000, 7600000, 260000)
FOOT = (452438, 5830000, 8600000, 240000)
PAGE = (11000000, 5830000, 900000, 240000)

TOTAL = 25


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
    "cover": "Buenas tardes. El arquetipo del bufón es uno de los más antiguos de la humanidad. No es un invento moderno: es una necesidad social de equilibrio. El rey necesitaba alguien que le dijera la verdad sin filtros. El bufón era el único que podía insultar al rey, siempre y cuando lo hiciera en rima o con una voltereta. Hoy vamos a recorrer esa historia y los paralelos con la seguridad.",
    "arquetipo": "El arquetipo del bufón está anclado históricamente en la Edad Media y el Renacimiento europeo, pero su raíz psicológica es el arquetipo del Trickster, el embaucador o payaso sagrado, presente en tribus indígenas desde hace milenios. No es un invento moderno, es una necesidad social de equilibrio.",
    "heyoka": "El Heyoka se clasifica en antropología como payaso sagrado de la cultura Lakota, no como bufón de corte. No opera desde el cinismo ni busca destruir la hipocresía política, sino que actúa por un mandato espiritual. Hace todo al revés para provocar la risa, y esa risa tiene un propósito de sanación. Es la esencia pura del clown, pero cumple un rol social bufonesco al mantener a raya el ego de los líderes.",
    "trickster": "En las mitologías indígenas de Norteamérica, la figura más cercana al bufón cínico y destructivo no es un humano, sino el arquetipo del Trickster, el dios Coyote o el Cuervo, que miente, roba, engaña y rompe los tabúes para enseñar lecciones a la fuerza.",
    "diferencia": "La diferencia teatral entre clown y bufón es clara. El clown es el niño eterno: trabaja desde la vulnerabilidad, el fracaso y la empatía. El bufón es el deforme, el paria, el cínico: trabaja desde la sátira, la parodia y la crítica social. El clown busca que lo quieras; el bufón busca incomodarte.",
    "triboulet": "Triboulet, bufón de Francisco I de Francia en el siglo XVI, es el bufón más icónico de la historia. Era brillante, afilado y cruzaba todos los límites. Una vez le dio una nalgada al rey en público. Francisco I lo condenó a muerte, pero le concedió el derecho de elegir cómo morir. Triboulet respondió: elijo morir de viejo. Al rey le causó tanta gracia que le perdonó la vida.",
    "sommers": "Will Sommers, bufón de Enrique VIII de Inglaterra, era el único hombre en toda Inglaterra que podía decirle la verdad, burlarse de su peso y calmar sus ataques de ira. Usaba una mezcla de clown y bufón para proteger a los cortesanos. Sobrevivió a Enrique VIII, conservó su puesto con sus sucesores y murió por causas naturales.",
    "stanczyk": "Stańczyk, bufón del rey Segismundo I de Polonia, era un bufón filósofo. Mientras la corte estaba de fiesta, él solía estar deprimido por las decisiones políticas del rey. Usaba la sátira para advertir sobre alianzas militares desastrosas. Hoy es recordado en Polonia como un símbolo de patriotismo e inteligencia política.",
    "armstrong": "Archibald Armstrong, bufón de Jacobo I y Carlos I de inglés, es el ejemplo del bufón que cruzó la línea. Se volvió rico, arrogante y empezó a insultar abiertamente a figuras intocables. Perdió el favor del rey, fue desterrado y terminó sus días viviendo en la desgracia fuera de los círculos de poder.",
    "darwin": "Darwin Desbocatti es la definición exacta de un bufón moderno. Opera desde la marginalidad, sin rostro visual en la radio, opinando desde fuera del establishment. Esto le otorga la inmunidad del bufón para decirle en la cara a políticos y empresarios las verdades más crudas. Su humor ácido y su sarcasmo son la rima del bufón medieval.",
    "actuales": "Los bufones actuales existen y son potentes. Ricky Gervais en sus monólogos de los Globos de Oro se par frente a los actores más poderosos de Hollywood para destrozar su hipocresía. Jon Stewart y John Oliver son bufones periodísticos que exponen la corrupción. Peter Capusotto en Argentina expone los extremos de la cultura rioplatense.",
    "edad_media": "La Edad Media abarca desde el año 476 hasta 1492 o 1453. El bufón de corte con su traje de cascabeles y su estatus de inmunidad institucionalizada alcanzó su edad de oro al final de la Edad Media y durante el Renacimiento, siglos XIII al XVII.",
    "cornisa": "El bufón caminaba por la cornisa más fina de la política: su trabajo era insultar al hombre que tenía el poder de ejecutarlo, y su única armadura era la gracia con la que lo hacía. Triboulet eligió morir de viejo y vivió. Armstrong perdió la gracia y terminó en la desgracia.",
    "paralelo": "El paralelismo con la seguridad es directo. El bufón era el único que podía decirle al rey que sus defensas eran débiles. En seguridad, el pentester es el bufón moderno: dice en la cara lo que los cortesanos no se atreven a mencionar. Su inmunidad es la autorización escrita.",
    "pentester": "El pentester moderno opera como el bufón de corte: entra al sistema, encuentra lo que nadie quiere ver, y lo dice en la cara. Su única armadura es la autorización por escrito. Sin esa autorización, el pentester no es un bufón: es un criminal. La gracia es el alcance definido.",
    "cierre": "El bufón nos enseña una lección de seguridad: la verdad incómoda dicha a tiempo vale más que la adulación silenciosa. En seguridad, como en la corte, el que dice la verdad sin filtros es incómodo hasta que se agradece. Gracias.",
    "img_timeline": "La línea de tiempo del bufón. Desde los payasos sagrados de las tribus ancestrales hasta los bufones de corte medievales y los satiristas modernos. El arquetipo no cambia: solo cambia el escenario.",
    "img_person_system": "El bufón y el sistema. El bufón opera desde fuera del establishment, igual que un pentester opera desde fuera del sistema. Ambos ven lo que los de dentro no pueden o no quieren ver.",
    "img_circles": "El ecosistema del bufón. En el centro, el rey. Alrededor, los cortesanos que adulan. Y en el borde, el bufón que dice la verdad. En seguridad: en el centro, el sistema. Alrededor, los desarrolladores que confían. Y en el borde, el pentester que encuentra la falla.",
    "img_sender": "Del bufón al sender-constrained. El bufón medieval tenía inmunidad institucionalizada: su traje de cascabeles era su certificado. DPoP es el traje de cascabeles del token: sin esa prueba criptográfica, el token no sirve.",
    "img_reference": "Arquitectura de referencia. El gateway es la puerta de la corte: valida y deja pasar. Los microservicios son las habitaciones del rey: cada una con sus propias reglas. El bufón entra donde quiere porque tiene la autorización del rey.",
    "img_d_owasp": "OWASP Top 10 visto por el bufón. BOLA: el rey mira el propio pedido y el del vecino. Broken Authentication: el rey confía en cualquier billete. SSRF: el rey mira hacia adentro cuando debería mirar hacia afuera. Cada vulnerabilidad es un bufón que nadie escuchó.",
}


COVER = {
    "type": "cover",
    "title": "El arquetipo del bufón",
    "subtitle": "De las tribus ancestrales a los cortesanos modernos",
    "notes": G["cover"],
}

DECK = [
    {"eyebrow": "El arquetipo", "title": "El bufón: uno de los arquetipos más antiguos",
     "bullets": [
        ("Raíz: ", "Trickster, el embaucador o payaso sagrado."),
        ("Historia: ", "Edad Media y Renacimiento europeo."),
        ("Función: ", "decir la verdad al poder sin filtros."),
     ],
     "source": "Antropología; historia del teatro.", "notes": G["arquetipo"]},

    {"eyebrow": "Tribus ancestrales", "title": "El Heyoka: payaso sagrado Lakota",
     "bullets": [
        ("Mandato: ", "espiritual, no cínico."),
        ("Comportamiento: ", "todo al revés, monta el caballo mirando atrás."),
        ("Propósito: ", "romper la tensión y abrir la mente de la tribu."),
        ("Rol: ", "mantener a raya el ego de los líderes."),
     ],
     "source": "Cultura Lakota; antropología.", "notes": G["heyoka"]},

    {"eyebrow": "Tribus ancestrales", "title": "El Trickster: el bufón cínico",
     "bullets": [
        ("Figura: ", "dios Coyote o Cuervo, no un humano."),
        ("Comportamiento: ", "miente, roba, engaña, rompe tabúes."),
        ("Propósito: ", "enseñar lecciones a la fuerza."),
     ],
     "source": "Mitología indígena norteamericana.", "notes": G["trickster"]},

    {"eyebrow": "Diferencia", "title": "Clown versus bufón",
     "bullets": [
        ("Clown: ", "el niño eterno, vulnerabilidad, fracaso, empatía."),
        ("Bufón: ", "el cínico, sátira, parodia, crítica social."),
        ("El clown busca que lo quieras. ", "El bufón busca incomodarte."),
     ],
     "source": "Historia del teatro; arquetipos de Jung.", "notes": G["diferencia"]},

    {"eyebrow": "Edad Media", "title": "Triboulet: bufón de Francisco I (s. XVI)",
     "bullets": [
        ("El más icónico: ", "inspiró Rigoletto de Verdi."),
        ("La hazaña: ", "le dio una nalgada al rey en público."),
        ("La condena: ", "muerte, pero eligió cómo morir."),
        ("La respuesta: ", "elijo morir de viejo. El rey se rió y lo desterró."),
     ],
     "source": "Historia de Francia; siglo XVI.", "notes": G["triboulet"]},

    {"eyebrow": "Edad Media", "title": "Will Sommers: bufón de Enrique VIII (s. XVI)",
     "bullets": [
        ("Único: ", "podía decirle la verdad a Enrique VIII."),
        ("Protección: ", "de cortesanos ante la furia del rey."),
        ("Final: ", "sobrevivió al rey, se retiró con pensión, murió de viejo."),
     ],
     "source": "Historia de Inglaterra; siglo XVI.", "notes": G["sommers"]},

    {"eyebrow": "Edad Media", "title": "Stańczyk: bufón de Segismundo I (s. XVI)",
     "bullets": [
        ("Filósofo: ", "deprimido mientras la corte festejaba."),
        ("Advertencia: ", "sobre alianzas militares desastrosas."),
        ("Legado: ", "símbolo de patriotismo e inteligencia política en Polonia."),
     ],
     "source": "Historia de Polonia; siglo XVI.", "notes": G["stanczyk"]},

    {"eyebrow": "Edad Media", "title": "Archibald Armstrong: el que cruzó la línea",
     "bullets": [
        ("Cargo: ", "bufón de Jacobo I y Carlos I de Inglaterra."),
        ("Error: ", "volverse rico, arrogante, insultar al Arzobispo."),
        ("Final: ", "desterrado, viviendo en la desgracia."),
     ],
     "source": "Historia de Inglaterra; siglo XVII.", "notes": G["armstrong"]},

    {"eyebrow": "Uruguay", "title": "Darwin Desbocatti: el bufón uruguayo",
     "bullets": [
        ("Marginalidad: ", "sin rostro visual, opina desde fuera del establishment."),
        ("Inmunidad: ", "el bufón moderno que dice la verdad."),
        ("Humor: ", "ácido, sarcástico, la rima del bufón medieval."),
     ],
     "source": "Radio uruguaya; cultura rioplatense.", "notes": G["darwin"]},

    {"eyebrow": "Actualidad", "title": "Bufones actuales",
     "bullets": [
        ("Ricky Gervais: ", "monólogos contra la hipocresía de Hollywood."),
        ("Jon Stewart y John Oliver: ", "bufones periodísticos contra la corrupción."),
        ("Peter Capusotto: ", "parodias grotescas de la cultura rioplatense."),
     ],
     "source": "Televisión; comedia satírica.", "notes": G["actuales"]},

    {"eyebrow": "Historia", "title": "La Edad Media: 476 a 1492/1453",
     "bullets": [
        ("Inicio: ", "caída del Imperio Romano de Occidente (476)."),
        ("Fin: ", "llegada a América (1492) o caída de Constantinopla (1453)."),
        ("Edad de oro del bufón: ", "siglos XIII al XVII."),
     ],
     "source": "Historia universal.", "notes": G["edad_media"]},

    {"eyebrow": "La lección", "title": "La cornisa más fina de la política",
     "bullets": [
        ("El trabajo: ", "insultar al hombre que podía ejecutarte."),
        ("La armadura: ", "la gracia con que lo hacías."),
        ("Triboulet: ", "mantuvo la gracia, murió de viejo."),
        ("Armstrong: ", "perdió la gracia, terminó desterrado."),
     ],
     "source": "Historia; paralelismo con seguridad.", "notes": G["cornisa"]},

    {"eyebrow": "Paralelo", "title": "El pentester: el bufón moderno",
     "bullets": [
        ("Entra al sistema, ", "encuentra lo que nadie quiere ver."),
        ("Lo dice en la cara, ", "sin filtros."),
        ("Su inmunidad: ", "la autorización por escrito."),
        ("Sin autorización, ", "no es un bufón: es un criminal."),
     ],
     "source": "OWASP; pentesting ético.", "notes": G["pentester"]},

    {"eyebrow": "Paralelo", "title": "El paralelismo con la seguridad",
     "bullets": [
        ("El bufón: ", "decía al rey que sus defensas eran débiles."),
        ("El pentester: ", "dice al CISO que sus APIs son inyectables."),
        ("La gracia del bufón: ", "la autorización escrita."),
     ],
     "source": "OWASP; historia del teatro.", "notes": G["paralelo"]},

    {"eyebrow": "Cierre", "title": "La lección del bufón",
     "bullets": [
        ("La verdad incómoda dicha a tiempo ", "vale más que la adulación silenciosa."),
        ("El bufón es incómodo ", "hasta que se agradece."),
        ("En seguridad, como en la corte, ", "el que dice la verdad es el que salva al rey."),
     ],
     "source": "Paralelismo histórico.", "notes": G["cierre"]},

    {"eyebrow": "Anexo", "title": "La línea de tiempo del bufón",
     "figure": "01_timeline.png",
     "source": "Antropología; historia del teatro.", "notes": G["img_timeline"]},

    {"eyebrow": "Anexo", "title": "El bufón y el sistema",
     "figure": "06_person_vs_system.png",
     "source": "OWASP; historia.", "notes": G["img_person_system"]},

    {"eyebrow": "Anexo", "title": "El ecosistema del bufón",
     "figure": "13_circles.png",
     "source": "OWASP; historia del teatro.", "notes": G["img_circles"]},

    {"eyebrow": "Anexo", "title": "Del bufón al sender-constrained",
     "figure": "07_sender_constrained.png",
     "source": "RFC 8705; RFC 9449.", "notes": G["img_sender"]},

    {"eyebrow": "Anexo", "title": "Arquitectura de referencia",
     "figure": "12_reference_arch.png",
     "source": "OWASP; NIST SP 800-207.", "notes": G["img_reference"]},

    {"eyebrow": "Anexo", "title": "OWASP Top 10 visto por el bufón",
     "figure2": "d_owasp.png",
     "source": "OWASP API Security Top 10 (2023).", "notes": G["img_d_owasp"]},
]


SHORT = {
    "El bufón: uno de los arquetipos más antiguos": "El bufón",
    "El Heyoka: payaso sagrado Lakota": "Heyoka: payaso sagrado",
    "El Trickster: el bufón cínico": "Trickster",
    "Clown versus bufón": "Clown vs bufón",
    "Triboulet: bufón de Francisco I (s. XVI)": "Triboulet (s. XVI)",
    "Will Sommers: bufón de Enrique VIII (s. XVI)": "Will Sommers (s. XVI)",
    "Stańczyk: bufón de Segismundo I (s. XVI)": "Stańczyk (s. XVI)",
    "Archibald Armstrong: el que cruzó la línea": "Armstrong",
    "Darwin Desbocatti: el bufón uruguayo": "Desbocatti",
    "Bufones actuales": "Bufones actuales",
    "La Edad Media: 476 a 1492/1453": "Edad Media",
    "La cornisa más fina de la política": "La cornisa",
    "El pentester: el bufón moderno": "Pentester: bufón moderno",
    "El paralelismo con la seguridad": "Paralelo con seguridad",
    "La lección del bufón": "La lección del bufón",
    "La línea de tiempo del bufón": "Línea de tiempo",
    "El bufón y el sistema": "Bufón y sistema",
    "El ecosistema del bufón": "Ecosistema del bufón",
    "Del bufón al sender-constrained": "Bufón al sender-constrained",
    "Arquitectura de referencia": "Arquitectura",
    "OWASP Top 10 visto por el bufón": "OWASP visto por el bufón",
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
