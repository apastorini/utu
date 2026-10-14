import os, sys
import pymupdf

base = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(base, "material")
out = os.path.join(base, "raw_text")
os.makedirs(out, exist_ok=True)

# also extract the notas de teorico
extra = [os.path.join(base, "notas_cdvv_2024.pdf")]

def extract(path):
    doc = pymupdf.open(path)
    parts = []
    for i, page in enumerate(doc):
        txt = page.get_text("text")
        parts.append(f"\n===== PAGE {i+1} =====\n" + txt)
    doc.close()
    return "".join(parts)

files = sorted(os.listdir(src)) if os.path.isdir(src) else []
files = [f for f in files if f.lower().endswith(".pdf")]
for f in files:
    p = os.path.join(src, f)
    try:
        t = extract(p)
        with open(os.path.join(out, f[:-4] + ".txt"), "w", encoding="utf-8") as fh:
            fh.write(t)
        print(f"OK  {f}  {len(t)} chars")
    except Exception as e:
        print(f"ERR {f}: {e}")

for p in extra:
    if os.path.exists(p):
        t = extract(p)
        name = "notas_cdvv_2024.txt"
        with open(os.path.join(out, name), "w", encoding="utf-8") as fh:
            fh.write(t)
        print(f"OK  {name}  {len(t)} chars")
