# -*- coding: utf-8 -*-
"""
Genera una diapositiva suelta (.pptx) usando el formato del template
"Slides template - OWASP UY.pptx" (fondo OWASP UY + layout CUSTOM_1_2
'Title and body', subtítulo 32pt navy + barra azul + cuerpo con viñetas ●).

Uso:
    python make_slide_owasp_uy.py

Salida:
    diapositiva_15_(25 slides).pptx   -> slide 15 del prompt de 25
    diapositiva_15_(28 slides).pptx   -> slide 15 del prompt de 28
"""
import sys
from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

TEMPLATE = r"C:\Users\apast\Downloads\Slides template - OWASP UY.pptx"

NAVY = RGBColor(0x1B, 0x27, 0x38)   # color de texto del layout
BLUE = RGBColor(0x74, 0xAA, 0xDC)   # barra de acento
GRAY = RGBColor(0x7A, 0x7A, 0x7A)   # pie de fuente


def delete_slide(prs, index):
    """Borra una slide quitando su sldId y su relación."""
    sldIdLst = prs.slides._sldIdLst
    sldId = list(sldIdLst)[index]
    rId = sldId.get(
        "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"
    )
    prs.part.drop_rel(rId)
    sldIdLst.remove(sldId)


def get_ph(slide, ph_type=None, idx=None):
    for ph in slide.placeholders:
        if idx is not None and ph.placeholder_format.idx == idx:
            return ph
        if ph_type is not None and ph.placeholder_format.type == ph_type:
            return ph
    return None


def fill_body(ph, bullets):
    """Carga viñetas en el placeholder de cuerpo (hereda ● 26pt del layout).

    Se fija explícitamente Lato 26pt navy para que sea coherente con el
    título (el layout solo define Lato/navy en los subniveles; el nivel 0
    heredaría Arial negro del patrón).

    bullets: lista de tuplas (lead_bold, resto). lead_bold puede ser None.
    """
    tf = ph.text_frame
    tf.word_wrap = True
    for i, (lead, rest) in enumerate(bullets):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        # limpiar corridos residuales
        for r in list(p.runs):
            r._r.getparent().remove(r._r)
        for text, bold in ((lead, True), (rest, False)):
            if not text:
                continue
            r = p.add_run()
            r.text = text
            r.font.name = "Lato"
            r.font.size = Pt(26)
            r.font.bold = bold
            r.font.color.rgb = NAVY
    return tf


def add_footnote(slide, source, page_no, total):
    """Pie con la fuente (letra chica) y el número de slide."""
    left, top, width, height = Emu(571550), Emu(5830000), Emu(8250900), Emu(300000)
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    r = p.add_run()
    r.text = "Fuente: " + source
    r.font.size = Pt(9)
    r.font.name = "Lato"
    r.font.color.rgb = GRAY

    nb = slide.shapes.add_textbox(Emu(10700000), Emu(5830000), Emu(1000000), Emu(300000))
    ntf = nb.text_frame
    np_ = ntf.paragraphs[0]
    np_.alignment = PP_ALIGN.RIGHT
    nr = np_.add_run()
    nr.text = "%d / %d" % (page_no, total)
    nr.font.size = Pt(9)
    nr.font.name = "Lato"
    nr.font.color.rgb = GRAY


def build(spec, out_path):
    prs = Presentation(TEMPLATE)
    lay = prs.slide_layouts[3]            # CUSTOM_1_2 = "Title and body"
    slide = prs.slides.add_slide(lay)

    # título (placeholder 'subTitle', 32pt navy)
    title_ph = get_ph(slide, idx=1)
    ttf = title_ph.text_frame
    ttf.word_wrap = True
    ttf.paragraphs[0].text = spec["title"]

    # cuerpo (placeholder 'body', viñetas ● 26pt)
    body_ph = get_ph(slide, idx=2)
    fill_body(body_ph, spec["bullets"])

    # pie
    add_footnote(slide, spec["source"], spec["page"], spec["total"])

    # notas del ponente
    slide.notes_slide.notes_text_frame.text = spec["guion"]

    # borrar las 4 slides de muestra del template
    for _ in range(4):
        delete_slide(prs, 0)

    prs.save(out_path)
    print("OK ->", out_path)
    return prs


# ---------------------------------------------------------------- contenido
SLIDE_25 = {
    "page": 15,
    "total": 25,
    "title": "La MFA cubre el login, no lo que pasa después",
    "bullets": [
        ("Fatiga de push (MITRE T1621) — ", "después de la emisión: el atacante ya tiene la contraseña y dispara push hasta que la víctima aprueba."),
        ("Phishing AiTM — ", "roba la sesión completa que ya pasó la MFA y la reutiliza."),
        ("Infostealers y pass-the-cookie — ", "malware extrae cookies y tokens del navegador y los usa en otro equipo."),
    ],
    "source": "MITRE ATT&CK T1621 · T1539; casos públicos 2022.",
    "guion": (
        "Hay tres familias de ataque que la MFA no cubre, porque atacan "
        "después de la emisión. Uno: fatiga de MFA, o push bombing —MITRE lo "
        "cataloga como T1621—: el atacante ya tiene la contraseña y dispara "
        "pushes hasta que la víctima aprueba. Dos: phishing "
        "adversary-in-the-middle: ya no roba la contraseña, intercepta la "
        "sesión completa que resultó de la MFA. Tres: infostealers, malware "
        "que extrae cookies y tokens del navegador y los reutiliza en otro "
        "equipo; se llama pass-the-cookie. En los tres, la MFA hizo su "
        "trabajo; el problema es que el artefacto se reutiliza."
    ),
}

SLIDE_28 = {
    "page": 15,
    "total": 28,
    "title": "Passkeys son el único factor que sobrevive al phishing",
    "bullets": [
        ("NIST AAL1–AAL3 — ", "el nivel de garantía se liga al riesgo; AAL2 pide dos factores de tipos distintos."),
        ("WebAuthn / passkeys — ", "recomendación W3C 2019: el desafío está atado al origen, resisten el phishing."),
        ("TOTP y SMS — ", "el OTP se phishea en tiempo real y el SMS es el más débil."),
        ("Step-up — ", "acr y amr (RFC 8176) piden más garantía solo en la operación sensible."),
    ],
    "source": "NIST SP 800-63-4 (jul. 2025); WebAuthn (2019); RFC 8176 (2017).",
    "guion": (
        "NIST, en su guía de identidad vigente de julio de 2025, dice algo "
        "clave: no todos los autenticadores dan la misma garantía, y el nivel "
        "debe ligarse al riesgo. AAL2 exige dos factores de tipos distintos; "
        "AAL3 exige prueba criptográfica de posesión de una clave en hardware. "
        "WebAuthn y las passkeys, recomendación W3C de 2019, resisten el "
        "phishing por diseño: el desafío está atado al origen. Un OTP se puede "
        "phishear en tiempo real, y el SMS es el más débil. Y el step-up, con "
        "acr y amr, permite pedir más garantía solo para la operación sensible."
    ),
}


if __name__ == "__main__":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

    def prn(*a):
        print(*a)

    build(SLIDE_25, r"diapositiva_15_(25 slides).pptx")
    prn("")
    prn("SLIDE 15 del prompt de 25  ->  diapositiva_15_(25 slides).pptx")
    prn("  Titulo:", SLIDE_25["title"])
    prn("  Nota: el guion completo esta en las notas del ponente.")
    prn("")
    build(SLIDE_28, r"diapositiva_15_(28 slides).pptx")
    prn("")
    prn("SLIDE 15 del prompt de 28  ->  diapositiva_15_(28 slides).pptx")
    prn("  Titulo:", SLIDE_28["title"])
    prn("  Nota: el guion completo esta en las notas del ponente.")
