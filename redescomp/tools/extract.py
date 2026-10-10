"""Extrae texto de los PDFs oficiales (examenes, practicos, teorico, libro)."""
import sys, pathlib, pymupdf

def dump(pdf: pathlib.Path, out: pathlib.Path):
    doc = pymupdf.open(pdf)
    parts = []
    for i, page in enumerate(doc):
        parts.append(f"\n===== [pag {i+1}] =====\n")
        parts.append(page.get_text("text"))
    out.write_text("".join(parts), encoding="utf-8")
    print(f"{pdf.name}: {doc.page_count} pag -> {out.name} ({out.stat().st_size} bytes)")

if __name__ == "__main__":
    src = pathlib.Path(sys.argv[1])
    dst = pathlib.Path(sys.argv[2])
    dst.mkdir(parents=True, exist_ok=True)
    for p in sorted(src.glob("*.pdf")):
        try:
            dump(p, dst / (p.stem + ".txt"))
        except Exception as e:
            print(f"ERROR {p.name}: {e}")
