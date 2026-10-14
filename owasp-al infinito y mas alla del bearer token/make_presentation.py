# -*- coding: utf-8 -*-
"""Genera la presentacion en PDF (16:9) a partir de prompt_slides_28.md,
incrustando los diagramas de img/ y un anexo con cada diagrama en pagina completa.
Salidas:
  presentacion.pdf        -> deck + anexo de diagramas, CON guion del ponente
  presentacion_limpia.pdf -> deck + anexo de diagramas, SIN guion (para proyectar)
  diagramas.pdf           -> solo los diagramas, uno por pagina
"""
import os
import re
import textwrap
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle
from matplotlib.backends.backend_pdf import PdfPages
from PIL import Image

BASE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(BASE, "img")

FW, FH = 13.333, 7.5
CT = 0.78  # borde superior del contenido (debajo del titulo)
DARK = "#12263a"; ACCENT = "#0b7285"; GRAY = "#495057"; LINE = "#d0d7de"
BAND = "#eef4f8"; RED = "#c92a2a"; GREEN = "#2b8a3e"

FIG_TITLES = {
    "01_timeline.png": "Línea de tiempo: de las credenciales al token atado",
    "02_token_family.png": "La familia de tokens y el flujo de emisión",
    "03_jwt_anatomy.png": "Anatomía de un JWT: firmado, no sellado",
    "04_transport.png": "Dónde viaja el token: cabecera, cookie o query",
    "05_mfa_timeline.png": "La MFA protege un instante; el token vive mucho más",
    "06_person_vs_system.png": "Persona vs. sistema: dos preguntas distintas",
    "07_sender_constrained.png": "Del bearer a los tokens sender-constrained",
    "08_oauth_flows.png": "Flujos de OAuth 2.0: cuáles usar y cuáles se retiraron",
    "09_protocol_stack.png": "Los protocolos involucrados, por capas",
    "10_lifecycle.png": "Ciclo de vida de un token",
    "11_owasp_top10.png": "OWASP API Security Top 10 (2023)",
    "12_reference_arch.png": "Arquitectura de referencia de una API segura",
    "13_circles.png": "Alrededor del token hay un sistema entero",
}

# slide -> diagrama
DIAGRAM = {
    4: "13_circles.png",
    8: "01_timeline.png",
    9: "02_token_family.png",
    11: "03_jwt_anatomy.png",
    13: "04_transport.png",
    14: "05_mfa_timeline.png",
    18: "06_person_vs_system.png",
    19: "11_owasp_top10.png",
    20: "12_reference_arch.png",
    23: "07_sender_constrained.png",
    24: "10_lifecycle.png",
}


def parse_slides(path):
    txt = open(path, encoding="utf-8").read()
    a = txt.index("ESTRUCTURA EXACTA")
    b = txt.index("\nREGLAS")
    lines = txt[a:b].splitlines()
    blocks, cur = [], None
    for l in lines[1:]:
        if re.match(r'^\d{1,2}\.\s', l):
            if cur:
                blocks.append(cur)
            cur = [l]
        elif cur is not None:
            cur.append(l)
    if cur:
        blocks.append(cur)

    labels = ["Título:", "Subtítulo:", "Bullets:", "Visual obligatorio:",
              "Visual:", "GUION:", "Fuente al pie:"]
    slides = []
    for blk in blocks:
        m = re.match(r'^(\d{1,2})\.\s+(.*)$', blk[0].strip())
        num, headtitle = int(m.group(1)), m.group(2)
        body = " ".join(x.strip() for x in blk[1:])
        pos = sorted((body.find(lab), lab) for lab in labels if body.find(lab) >= 0)
        d = {}
        for k, (i, lab) in enumerate(pos):
            j = pos[k + 1][0] if k + 1 < len(pos) else len(body)
            d[lab.rstrip(":")] = body[i + len(lab):j].strip()
        title = d.get("Título", headtitle).strip()
        subtitle = d.get("Subtítulo", "").strip()
        clean = lambda t: t.replace('"', "").replace("“", "").replace("”", "").strip().rstrip(".").strip()
        title = clean(title)
        subtitle = clean(subtitle)
        bullets_raw = d.get("Bullets", "")
        bullets = [x.strip(" .") for x in re.split(r'\s*[·;]\s*', bullets_raw) if x.strip()]
        slides.append({
            "num": num,
            "head": headtitle,
            "title": title,
            "subtitle": subtitle,
            "bullets": bullets[:5],
            "guion": clean(d.get("GUION", "")),
            "fuente": d.get("Fuente al pie", "").strip(),
        })
    return slides


def img_extent(ax, path, box):
    """Devuelve (x0,x1,y0,y1) para encajar la imagen en box=(bx,by,bw,bh) sin deformar."""
    bx, by, bw, bh = box
    w, h = Image.open(path).size
    ar = w / h
    box_ar = (bw * FW) / (bh * FH)
    if ar >= box_ar:
        ew = bw; eh = (ew * FW) / (ar * FH)
    else:
        eh = bh; ew = (eh * FH * ar) / FW
    x0 = bx + (bw - ew) / 2; y0 = by + (bh - eh) / 2
    return (x0, x0 + ew, y0, y0 + eh)


def place_image(ax, path, box, z=1):
    x0, x1, y0, y1 = img_extent(ax, path, box)
    ax.imshow(plt.imread(path), extent=(x0, x1, y0, y1), aspect="auto", zorder=z)


def wrap(text, width):
    return textwrap.wrap(text, width=width) or [""]


def draw_bullets(ax, bullets, x, y_top, width, fontsize, color=DARK):
    lines = []
    for b in bullets:
        w = wrap(b, width)
        lines.append(("•", w[0]))
        for extra in w[1:]:
            lines.append((" ", extra))
    step = (fontsize / 72.0) * 1.7 / FH  # interlineado en fraccion de figura
    y = y_top
    for mark, txt in lines:
        if mark == "•":
            ax.text(x, y, "•", ha="left", va="top", fontsize=fontsize,
                    color=ACCENT, fontweight="bold", zorder=3)
        ax.text(x + 0.022, y, txt, ha="left", va="top", fontsize=fontsize,
                color=color, zorder=3)
        y -= step


def slide_frame(ax, num, title, fuente, guion, show_guion):
    ax.add_patch(Rectangle((0, 0.965), 1, 0.035, color=ACCENT, zorder=4))
    # numero
    ax.text(0.955, 0.925, f"{num}/28", ha="right", va="center", fontsize=11,
            color=ACCENT, fontweight="bold", zorder=4)
    # titulo
    tl = wrap(title, 46 if len(title) > 60 else 60)
    fs = 25 if len(tl) <= 2 else 21
    y = 0.905
    for ln in tl:
        ax.text(0.05, y, ln, ha="left", va="top", fontsize=fs, color=DARK,
                fontweight="bold", zorder=4)
        y -= (fs / 72.0) * 1.25 / FH
    ax.plot([0.05, 0.95], [y - 0.012, y - 0.012], color=LINE, lw=1.2, zorder=2)
    # fuente
    src = fuente.strip().lstrip("—").strip()
    if src:
        ax.text(0.05, 0.045, "Fuente: " + src, ha="left", va="center",
                fontsize=9, color=GRAY, style="italic", zorder=4)
    # guion
    if show_guion and guion:
        ax.add_patch(FancyBboxPatch((0.04, 0.075), 0.92, 0.185,
                     boxstyle="round,pad=0.004,rounding_size=0.01",
                     fc=BAND, ec=LINE, lw=1, zorder=1))
        ax.text(0.055, 0.245, "GUION DEL PONENTE", ha="left", va="top",
                fontsize=8, color=ACCENT, fontweight="bold", zorder=4)
        gl = wrap(guion, 172)
        fs = 8.2 if len(gl) <= 4 else 7.2
        y = 0.218
        for ln in gl[:6]:
            ax.text(0.055, y, ln, ha="left", va="top", fontsize=fs, color=GRAY, zorder=4)
            y -= (fs / 72.0) * 1.35 / FH
    return 0.29 if (show_guion and guion) else 0.09


def new_slide():
    fig = plt.figure(figsize=(FW, FH))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    return fig, ax


def render_slide(pdf, s, show_guion):
    fig, ax = new_slide()
    num = s["num"]
    if num == 1:  # portada
        ax.add_patch(Rectangle((0, 0), 1, 1, color=DARK, zorder=0))
        ax.add_patch(Rectangle((0, 0), 0.012, 1, color=ACCENT, zorder=1))
        ax.text(0.08, 0.66, s["title"], ha="left", va="center", fontsize=34,
                color="white", fontweight="bold", zorder=2)
        ax.text(0.08, 0.52, s["subtitle"], ha="left", va="center", fontsize=18,
                color="#8ecae6", zorder=2)
        ax.text(0.08, 0.30, "Seguridad de APIs · de Basic al DPoP",
                ha="left", va="center", fontsize=13, color="#c9d6df", zorder=2)
        ax.text(0.08, 0.22, "2026 · charla técnica · 28 diapositivas",
                ha="left", va="center", fontsize=11, color="#6c8598", zorder=2)
        pdf.savefig(fig); plt.close(fig); return

    content_top = slide_frame(ax, num, s["title"], s["fuente"], s["guion"], show_guion)
    box = (0.05, content_top, 0.90, CT - content_top)
    img = DIAGRAM.get(num)
    if num == 3 and s["guion"]:
        # slide de cita
        ax.add_patch(FancyBboxPatch((0.09, content_top + 0.02), 0.82, CT - content_top - 0.05,
                     boxstyle="round,pad=0.01,rounding_size=0.02", fc="#f1f8f6",
                     ec=ACCENT, lw=2, zorder=1))
        quote = ("«La especificación no provee ningún método para que el servidor de recursos "
                 "se asegure de que un access token presentado por un cliente le fue emitido "
                 "realmente a ese cliente.»")
        ql = wrap(quote, 62)
        y = CT - 0.05
        for ln in ql:
            ax.text(0.5, y, ln, ha="center", va="top", fontsize=17, color=DARK,
                    style="italic", zorder=3)
            y -= 0.06
        ax.text(0.5, y - 0.01, "RFC 6749, §10.3 — octubre 2012", ha="center",
                va="top", fontsize=13, color=ACCENT, fontweight="bold", zorder=3)
    elif num == 5:
        # taxonomia: seis cuadros estilo -> falla
        items = [("REST", "recursos", "BOLA / IDOR"), ("GraphQL", "consultas", "query depth / sobre-exposición"),
                 ("gRPC", "binario", "WAF no inspecciona"), ("SOAP", "XML", "XXE"),
                 ("WebSocket", "canal", "auth solo al inicio"), ("Webhooks", "push", "SSRF / replay")]
        x = 0.05; w = 0.138; gap = 0.012
        for name, kind, risk in items:
            ax.add_patch(FancyBboxPatch((x, content_top + 0.03), w, 0.30,
                         boxstyle="round,pad=0.006,rounding_size=0.02",
                         fc="#e7f5ff", ec=ACCENT, lw=1.2, zorder=1))
            ax.text(x + w / 2, content_top + 0.29, name, ha="center", va="top",
                    fontsize=12, color=DARK, fontweight="bold", zorder=3)
            ax.text(x + w / 2, content_top + 0.22, kind, ha="center", va="top",
                    fontsize=9, color=GRAY, style="italic", zorder=3)
            for k, ln in enumerate(wrap(risk, 16)):
                ax.text(x + w / 2, content_top + 0.14 - k * 0.028, ln, ha="center",
                        va="top", fontsize=8.5, color=RED, zorder=3)
            x += w + gap
    elif img:
        if s["bullets"]:
            draw_bullets(ax, s["bullets"], 0.05, CT, 42, 14)
            place_image(ax, os.path.join(IMG, img), (0.50, content_top, 0.45, CT - content_top))
        else:
            place_image(ax, os.path.join(IMG, img), (0.05, content_top, 0.90, CT - content_top))
    elif s["bullets"]:
        draw_bullets(ax, s["bullets"], 0.05, CT, 72, 17)
    pdf.savefig(fig); plt.close(fig)


def render_diagram_page(pdf, name, title, subtitle=None):
    fig = plt.figure(figsize=(11, 8.5))
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    ax.add_patch(Rectangle((0, 0.955), 1, 0.045, color=ACCENT))
    ax.text(0.05, 0.925, title, ha="left", va="top", fontsize=15, color=DARK, fontweight="bold")
    place_image(ax, os.path.join(IMG, name), (0.04, 0.04, 0.92, 0.85))
    if subtitle:
        ax.text(0.05, 0.02, subtitle, ha="left", va="bottom", fontsize=8, color=GRAY, style="italic")
    pdf.savefig(fig); plt.close(fig)


def build_deck(path, show_guion, with_appendix=True):
    slides = parse_slides(os.path.join(BASE, "prompt_slides_28.md"))
    with PdfPages(path, metadata={"Title": "Al fin(ito) y más allá del bearer token",
                                  "Author": "Charla de seguridad de APIs"}) as pdf:
        for s in slides:
            render_slide(pdf, s, show_guion)
        if with_appendix:
            fig, ax = new_slide()
            ax.add_patch(Rectangle((0, 0), 1, 1, color=DARK))
            ax.text(0.5, 0.55, "ANEXO — DIAGRAMAS", ha="center", va="center",
                    fontsize=30, color="white", fontweight="bold")
            ax.text(0.5, 0.44, "13 diagramas en página completa", ha="center",
                    va="center", fontsize=14, color="#8ecae6")
            pdf.savefig(fig); plt.close(fig)
            for i, (name, title) in enumerate(FIG_TITLES.items(), 1):
                render_diagram_page(pdf, name, f"{i}. {title}")
    print("OK", path)


def build_diagrams_only(path):
    with PdfPages(path, metadata={"Title": "Diagramas — seguridad de APIs"}) as pdf:
        fig, ax = new_slide()
        ax.add_patch(Rectangle((0, 0), 1, 1, color=DARK))
        ax.text(0.5, 0.55, "DIAGRAMAS", ha="center", va="center", fontsize=34,
                color="white", fontweight="bold")
        ax.text(0.5, 0.44, "Seguridad de APIs · del bearer token a los protocolos",
                ha="center", va="center", fontsize=14, color="#8ecae6")
        pdf.savefig(fig); plt.close(fig)
        for i, (name, title) in enumerate(FIG_TITLES.items(), 1):
            render_diagram_page(pdf, name, f"{i}. {title}")
    print("OK", path)


if __name__ == "__main__":
    build_deck(os.path.join(BASE, "presentacion.pdf"), show_guion=True)
    build_deck(os.path.join(BASE, "presentacion_limpia.pdf"), show_guion=False)
    build_diagrams_only(os.path.join(BASE, "diagramas.pdf"))
