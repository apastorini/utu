"""Limpia los .txt extraidos: quita headers/footers repetidos de pagina y deja markdown legible."""
import re, pathlib, sys

NOISE = [
    re.compile(r"Introducci[oó]n a las Redes de Computador\{?a?e?\}?s? y Comunicaci[oó]n de Datos", re.I),
    re.compile(r"Introducci[oó]n a las Redes de Computadoras y Comunicaci[oó]n de Datos", re.I),
    re.compile(r"P[aá]gina \d+/\d+"),
    re.compile(r"^\s*(El|Soluci[oó]n)\s*$"),
]

def clean(txt: str) -> str:
    out = []
    for line in txt.splitlines():
        s = line.rstrip()
        for rx in NOISE:
            if rx.search(s):
                s = ""
                break
        out.append(s)
    txt = "\n".join(out)
    txt = re.sub(r"\n{3,}", "\n\n", txt)
    txt = re.sub(r"[ \t]{2,}", " ", txt)
    return txt.strip() + "\n"

if __name__ == "__main__":
    src = pathlib.Path(sys.argv[1])
    for p in sorted(src.glob("*.txt")):
        t = p.read_text(encoding="utf-8")
        p.write_text(clean(t), encoding="utf-8")
        print("limpio:", p.name)
