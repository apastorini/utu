"""Detecta diagramas ASCIIinalsados: dentro de vallas ```, una linea con
muchos espacios triples seguido de otra con menos es sospechosa de haber sido
comprimida. Compara la densidad de espacios por bloque."""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent / "clases"


def main():
    peor = []
    for p in sorted(ROOT.glob("clase-*.md")):
        txt = p.read_text(encoding="utf-8")
        bloques = re.findall(r"```[a-z]*\n(.*?)```", txt, re.S)
        peor_bloque = (0, "")
        for b in bloques:
            lineas = [l for l in b.split("\n") if l.strip()]
            if len(lineas) < 4:
                continue
            # diagramas con alineacion: >=8 lineas con 3+ espacios consecutivos
            con_esp = sum(1 for l in lineas if re.search(r"\S {3,}\S", l))
            ratio = con_esp / len(lineas)
            if ratio > peor_bloque[0]:
                peor_bloque = (ratio, b[:200])
        if peor_bloque[0] > 0:
            peor.append((peor_bloque[0], p.name, len(bloques)))
    peor.sort(reverse=True)
    print(f"{'clase':52} {'ratio':>6}  bloques")
    for r, n, nb in peor[:20]:
        marca = "  <-- REVISAR" if r < 0.15 and nb > 3 else ""
        print(f"{n:52} {r:6.2f}  {nb}{marca}")
    if not peor:
        print("ninguna clase tiene diagramas alineados (revisar a mano)")


if __name__ == "__main__":
    main()
