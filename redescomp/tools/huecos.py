"""
Repara huecos dejados por la eliminacion de caracteres CJK o por backticks
borrados. Detecta "palabra + hueco + puntuacion" en prosa (fuera de bloques
de codigo) y hace los reemplazos de un diccionario curado.

NO intenta adivinar: cada hueco se declara explicitamente con su repuesto.
"""
import re
import sys
import pathlib

ROOT = pathlib.Path(r'C:\Utu\utu\redescomp\clases')


def huecos(linea):
    """Devuelve la lista de (inicio, fin) de huecos sospechosos.

    Un hueco es: caracter de palabra, seguido de 1-3 espacios, seguido de
    puntuacion suelta (, ; .) y despues fin de linea o espacio.
    Ejemplo: "puerto , "  ->  la palabra que estaba ahi se perdio.
    """
    out = []
    patron = re.compile(r"\w[ ]{1,3}[,;.](?:$|\s)")
    for m in patron.finditer(linea):
        out.append((m.start(), m.end()))
    return out


def main():
    args = sys.argv[1:]
    archivos = sorted(ROOT.glob("clase-*.md"))
    if args:
        nums = set()
        for a in args:
            if "-" in a:
                lo, hi = a.split("-")
                nums.update(range(int(lo), int(hi) + 1))
            else:
                nums.add(int(a))
        archivos = [p for p in archivos
                    if re.match(r"clase-(\d\d)", p.name)
                    and int(re.match(r"clase-(\d\d)", p.name).group(1)) in nums]

    for p in archivos:
        dentro = False
        for i, linea in enumerate(p.read_text(encoding="utf-8").split("\n"), 1):
            s = linea.strip()
            if s.startswith("```"):
                dentro = not dentro
                continue
            if dentro or not s:
                continue
            h = huecos(linea)
            if h:
                frag = linea[max(0, h[0][0] - 55):h[-1][1] + 55]
                print(f"{p.name}:L{i}  ({len(h)} hueco/s)")
                print(f"   ...{frag.strip()}...")
    print("\nfin")


if __name__ == "__main__":
    main()
