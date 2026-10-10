"""Recorta secciones por marcadores. Uso:
    python tools/trim.py <archivo.md> <inicio> <fin> [--out nuevo.md]
Elimina el texto desde <inicio> (inclusive) hasta <fin> (excluido).
Si no se pasa --out, escribe sobre el mismo archivo.
"""
import pathlib
import sys


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    out_idx = sys.argv.index("--out") if "--out" in sys.argv else -1
    if out_idx > 0:
        out = pathlib.Path(sys.argv[out_idx + 1])
        args = sys.argv[1:out_idx]
    else:
        out = pathlib.Path(args[0])
    path, start, end = pathlib.Path(args[0]), args[1], args[2]
    t = path.read_text(encoding="utf-8")
    i = t.index(start)
    j = t.index(end, i)
    removed = j - i
    out.write_text(t[:i] + t[j:], encoding="utf-8", newline="")
    print(f"quitados {removed} caracteres; quedan {len(t) - removed}")


if __name__ == "__main__":
    main()