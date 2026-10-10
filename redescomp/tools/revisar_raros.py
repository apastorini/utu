"""
Regla del proyecto: NUNCA correr limpiar.py sobre texto que contenga backticks
con identificadores, porque eliminar CJK dentro de un span de codigo puede
borrar el identificador entero.

Este script hace una COMPARACION SEGURA: escribe el resultado en un archivo
temporal y te dice exactamente que lineas cambiarian, para que las revises
antes de aplicar. No modifica nada.
"""
import re
import sys
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
CLASES = ROOT / "clases"

CJK = re.compile(r"[㐀-鿿豈-﫿＀-￯぀-ヿ]")
CODE_SPAN = re.compile(r"`[^`\n]*`")


def fuera_de_codigo(txt):
    dentro = False
    for i, linea in enumerate(txt.split("\n"), 1):
        if linea.lstrip().startswith("```"):
            dentro = not dentro
            yield i, linea, True
            continue
        yield i, linea, dentro


def main():
    cambios = 0
    for p in sorted(CLASES.glob("clase-*.md")):
        txt = p.read_text(encoding="utf-8")
        if not CJK.search(txt):
            continue
        print(f"\n=== {p.name}: TIENE CARACTERES CJK ===")
        for i, linea, dentro in fuera_de_codigo(txt):
            if CJK.search(linea) or "�" in linea:
                tag = "[dentro de codigo]" if dentro else "[prosa]"
                print(f"  L{i} {tag}: {linea.strip()[:120]}")
                cambios += 1
    print(f"\nTOTAL lineas con caracteres raros: {cambios}")
    if cambios:
        print("\nCorregilas a mano. NO corras limpiar.py: podria borrar backticks.")


if __name__ == "__main__":
    main()
