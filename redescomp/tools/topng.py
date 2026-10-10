import pymupdf, pathlib, sys

src = pathlib.Path(sys.argv[1])
dst = pathlib.Path(sys.argv[2])
dst.mkdir(parents=True, exist_ok=True)
zoom = float(sys.argv[3]) if len(sys.argv) > 3 else 2.0

for pdf in sorted(src.glob("*.pdf")):
    doc = pymupdf.open(pdf)
    sel = range(doc.page_count)
    if ":" in str(src):
        a, b = str(src).split(":")[1].split("-")
        sel = range(int(a) - 1, min(int(b), doc.page_count))
    for i in sel:
        page = doc[i]
        pix = page.get_pixmap(matrix=pymupdf.Matrix(zoom, zoom))
        out = dst / f"{pdf.stem}-p{i+1:02d}.png"
        pix.save(out)
        print(out.name, pix.width, "x", pix.height)
