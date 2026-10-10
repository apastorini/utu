"""
Compila las clases .md a un PDF con Chrome/Edge headless.

Uso:
    python tools/build_pdf.py               # todo el curso
    python tools/build_pdf.py 21            # solo la clase 21
    python tools/build_pdf.py 21-23         # clases 21 a 23

Genera:
    pdf/Redes-Computadoras-Clase-NN.pdf   (una por clase)
    pdf/Introduccion-a-las-Redes-de-Computadoras.pdf  (libro completo)
    pdf/index.html                          (para imprimir desde el navegador)
"""
import re
import sys
import pathlib
import subprocess

import markdown

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import diagramas as DIAG
import figuras as FIG

ROOT = pathlib.Path(__file__).resolve().parent.parent
CLASES = ROOT / "clases"
PDF = ROOT / "pdf"
BUILD = ROOT / ".build"

CHROME_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]

CSS = """
@page {
  size: A4;
  margin: 18mm 16mm 20mm 16mm;
  @bottom-center {
    content: "página " counter(page) " de " counter(pages);
    font: 9pt sans-serif; color: #888;
  }
}
html { font-size: 10.5pt; }
body {
  font-family: "Segoe UI", "Noto Sans", sans-serif;
  line-height: 1.55; color: #1a1a1a; max-width: none;
}
h1 { font-size: 20pt; color: #0b3d5c; border-bottom: 3px solid #0b3d5c;
     padding-bottom: 5px; margin-top: 0; page-break-before: always; }
h1:first-of-type { page-break-before: avoid; }
h2 { font-size: 14.5pt; color: #0b3d5c; border-bottom: 1px solid #b8cfdb;
     padding-bottom: 3px; margin-top: 1.6em; page-break-after: avoid; }
h3 { font-size: 12pt; color: #14507a; margin-top: 1.3em; page-break-after: avoid; }
h4 { font-size: 11pt; color: #333; margin-top: 1.1em; page-break-after: avoid; }
p { margin: 0.55em 0; text-align: justify; }
strong { color: #000; }
a { color: #14507a; text-decoration: none; }
hr { border: none; border-top: 1px solid #d0d0d0; margin: 1.4em 0; }
blockquote {
  border-left: 4px solid #7aa7c4; background: #f2f7fa;
  margin: 0.9em 0; padding: 0.7em 1em; color: #333;
}
blockquote p { margin: 0.3em 0; }
code {
  font-family: "Cascadia Mono", "Consolas", monospace; font-size: 9pt;
  background: #eef2f5; padding: 1px 4px; border-radius: 3px;
}
pre {
  background: #fbfbfb; border: 1px solid #d8d8d8; border-radius: 4px;
  padding: 0.8em; overflow-x: auto; font-size: 8.8pt; line-height: 1.35;
  page-break-inside: avoid;
}
pre code { background: none; padding: 0; font-size: 8.8pt; }
svg {
  display: block; margin: 1.1em auto 1.3em; max-width: 100%;
  page-break-inside: avoid; page-break-after: avoid;
}
figure { margin: 1.2em 0; text-align: center; page-break-inside: avoid; }
figure svg { border: 1px solid #d8d8d8; border-radius: 6px; background: #fff; }
table {
  border-collapse: collapse; width: 100%; margin: 0.9em 0;
  font-size: 9.2pt; page-break-inside: avoid;
}
th, td { border: 1px solid #c5c5c5; padding: 4px 7px; text-align: left;
         vertical-align: top; }
th { background: #0b3d5c; color: white; font-weight: 600; }
tr:nth-child(even) td { background: #f7f9fa; }
ul, ol { margin: 0.5em 0; padding-left: 1.6em; }
li { margin: 0.25em 0; }
details { margin: 0.6em 0; border: 1px solid #d8d8d8; border-radius: 4px;
          padding: 0.5em 0.8em; background: #fcfcf7; }
summary { font-weight: 600; color: #0b3d5c; cursor: pointer; }
img { max-width: 100%; }
.clase-pagina { page-break-before: always; }
.portada { text-align: center; padding-top: 4cm; page-break-after: always; }
.portada h1 { border: none; page-break-before: avoid; font-size: 30pt; }
ol.toc-clase { list-style: none; padding-left: 0; column-count: 2;
               column-gap: 8mm; font-size: 9.5pt; }
ol.toc-clase li { break-inside: avoid; margin: 0.15em 0; }
ol.toc-clase li.toc-parte { font-weight: 700; color: #0b3d5c; margin-top: 0.7em;
                            border-bottom: 1px solid #b8cfdb; }
ol.toc-clase li.toc-item { padding-left: 5mm; color: #333; }
"""


def find_chrome() -> str:
    for c in CHROME_CANDIDATES:
        if pathlib.Path(c).exists():
            return c
    raise SystemExit("No encontre Chrome ni Edge.")


def slug(stem: str) -> int | None:
    m = re.match(r"clase-(\d+)", stem)
    return int(m.group(1)) if m else None


def indice_de_clase(md_text: str) -> str:
    """Indice interno de una clase: los PARTE y los ## de nivel superior."""
    items = []
    for linea in md_text.splitlines():
        m = re.match(r"^(#{1,3})\s+(.*)$", linea)
        if not m:
            continue
        nivel, txt = len(m.group(1)), m.group(2).strip()
        if nivel == 1:
            continue  # el titulo de la clase ya va en el h1
        if nivel == 2 and txt.startswith("#"):   # "## PARTE"
            items.append((0, txt.lstrip("# ").strip()))
        elif nivel == 2:
            items.append((1, txt))
    if not items:
        return ""
    html = ['<h1>Contenido de esta clase</h1><ol class="toc-clase">']
    for nivel, txt in items:
        clase = "toc-parte" if nivel == 0 else "toc-item"
        html.append(f'<li class="{clase}">{txt}</li>')
    html.append("</ol>")
    return "".join(html)


def render_html(md_text: str) -> str:
    body = markdown.markdown(
        md_text,
        extensions=["tables", "fenced_code", "codehilite", "sane_lists"],
        extension_configs={"codehilite": {"guess_lang": False, "noclasses": False}},
    )
    # nl2br rompe los diagramas ASCII: revertir dentro de <pre>
    body = re.sub(r"<pre><code([^>]*)>(.*?)<br\s*/?>", r"<pre><code\1>\2", body, flags=re.S)
    # <details>/<summary> crudos -> HTML nativo (el markdown no trae la extension)
    body = re.sub(r"<summary>(.*?)</summary>", r"<summary>\1</summary>", body, flags=re.S)
    return f"<!DOCTYPE html><html lang='es'><head><meta charset='utf-8'>" \
           f"<style>{CSS}</style></head><body>{body}</body></html>"


def chrome_to_pdf(chrome: str, src_html: pathlib.Path, out_pdf: pathlib.Path) -> None:
    profile = BUILD / "chrome-profile"
    profile.mkdir(parents=True, exist_ok=True)
    out_pdf.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        chrome,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--no-pdf-header-footer",
        "--run-all-compositor-stages-before-draw",
        "--virtual-time-budget=12000",
        f"--user-data-dir={profile}",
        f"--print-to-pdf={out_pdf}",
        src_html.as_uri(),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    if not out_pdf.exists():
        raise SystemExit(f"Chrome no genero el PDF.\n{r.stdout}\n{r.stderr}")


def main():
    BUILD.mkdir(exist_ok=True)
    PDF.mkdir(exist_ok=True)
    chrome = find_chrome()
    print("Navegador:", chrome)

    archivos = sorted(
        p for p in CLASES.glob("clase-*.md")
        if re.match(r"clase-\d\d", p.name) and slug(p.stem) is not None
    )
    archivos.sort(key=lambda p: slug(p.stem))
    if not archivos:
        raise SystemExit("No hay clases en clases/")

    sel = archivos
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    # --nofiguras desactiva los diagramas
    con_figuras = "--nofiguras" not in sys.argv
    args = [a for a in args]
    if args:
        nums = set()
        for a in args:
            if "-" in a:
                lo, hi = a.split("-")
                nums.update(range(int(lo), int(hi) + 1))
            else:
                nums.add(int(a))
        sel = [p for p in archivos if slug(p.stem) in nums]
        if not sel:
            raise SystemExit(f"Ninguna clase coincide con {args}")

    print(f"Compilando {len(sel)} clase/s...")
    uno_solo = len(sel) == 1
    total_figuras = 0
    for p in sel:
        n = slug(p.stem)
        md = p.read_text(encoding="utf-8")
        n_fig = 0
        if con_figuras:
            for nombre, linea in FIG.figuras_para(md):
                md = FIG.insertar(md, nombre, linea)
                n_fig += 1
        total_figuras += n_fig
        html_path = BUILD / f"{p.stem}.html"
        html_path.write_text(render_html(md), encoding="utf-8")
        if uno_solo:
            out = PDF / f"Redes-Computadoras-Clase-{n:02d}.pdf"
        else:
            out = PDF / f"{p.stem}.pdf"
        chrome_to_pdf(chrome, html_path, out)
        kb = out.stat().st_size / 1024
        marca = f"  [{n_fig} figura{'s' if n_fig != 1 else ''}]" if n_fig else ""
        print(f"  {out.name}  ({kb:.0f} KB){marca}")

    # libro completo + indice navegable
    if len(sel) > 1:
        partes = []
        for p in sel:
            n = slug(p.stem)
            md = p.read_text(encoding="utf-8")
            if con_figuras:
                for nombre, linea in FIG.figuras_para(md):
                    md = FIG.insertar(md, nombre, linea)
            partes.append(
                f'<div class="clase-pagina"><h1>Clase {n}</h1>'
                + indice_de_clase(md)
                + "</div>"
            )
            cuerpo = render_html(md).split("<body>")[1].rsplit("</body>", 1)[0]
            cuerpo = cuerpo.split("</h1>", 1)[-1]
            partes.append(cuerpo)
        portada = """
        <div class="portada">
          <h1>Introducción a las Redes de Computadoras</h1>
          <p style="font-size:14pt">Facultad de Ingeniería &mdash; Universidad de la República</p>
          <p style="font-size:12pt">Instituto de Computación (INCO)</p>
          <p style="font-size:12pt;color:#666">Material de estudio completo &mdash; 48 clases</p>
          <p style="font-size:11pt;color:#888">Basado en los exámenes oficiales 1998&ndash;2011,
          Tanenbaum &amp; Wetherall 5ª ed., y actualización a 2026</p>
        </div>"""
        # indice
        toc = "<h1>Índice</h1><ol>"
        for p in sel:
            titulo = re.search(r"^#\s+(.*)$", p.read_text(encoding="utf-8"), re.M)
            t = titulo.group(1).strip() if titulo else p.stem
            t = re.sub(r"^Clase\s+\d+\s*[—–-]\s*", "", t)
            toc += f"<li><b>Clase {slug(p.stem)}</b> &mdash; {t}</li>"
        toc += "</ol>"

        libro_html = (f"<!DOCTYPE html><html lang='es'><head><meta charset='utf-8'>"
                      f"<style>{CSS}</style></head><body>{portada}{toc}"
                      f"{''.join(partes)}</body></html>")
        lp = BUILD / "libro.html"
        lp.write_text(libro_html, encoding="utf-8")
        out = PDF / "Introduccion-a-las-Redes-de-Computadoras.pdf"
        chrome_to_pdf(chrome, lp, out)
        print(f"\nLIBRO: {out.name}  ({out.stat().st_size/1024/1024:.1f} MB)")


if __name__ == "__main__":
    main()
