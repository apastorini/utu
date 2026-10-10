"""Limpia artefactos de generacion: runs CJK sueltos y caracteres U+FFFD,
usando un diccionario de reemplazos contextuales."""
import re, sys, pathlib

# Secuencias CJK que se colaron, con su reemplazo en contexto.
FIXES = [
    ("comparte con 40，截止 los otros 39", "comparte con 40 personas, los otros 39"),
    ("lo que rompía la，是我们independencia", "lo que rompía la independencia"),
    ("de bytes确认. Cuando `rwnd`", "de bytes confirmados. Cuando `rwnd`"),
    ("con `long`足够 grande", "con `long` suficientemente grande"),
    ("la可靠可靠idad es", "la fiabilidad es"),
    ("tanques los", "tanques los"),
    ("y no lo es", "y no lo es"),
    ("TCP lo confunda", "TCP lo confunda"),
    ("una unidad de", "una unidad de"),
]

REPL = {
    "截止": ", ",
    "是我们": " es ",
    "确认": " confirmado",
    "足够": " lo bastante ",
    "可靠": " fiab",
    "经典": "clásicos",
    "的": " de ",
    "了": "",
    "是": " es ",
    "在": " en ",
    "和": " y ",
    "不": " no ",
    "有": " con ",
}

def fix_text(t: str) -> tuple[str, list[str]]:
    notes = []
    # 1. diccionario explicito
    for old, new in FIXES:
        if old in t:
            notes.append(f"fix: {old!r} -> {new!r}")
            t = t.replace(old, new)
    # 2. CJK suelto: eliminar (queda doble espacio) y limpiar
    cjk = re.compile(r'[\u2e80-\u9fff\uf900-\ufaff\uff00-\uffef]+')
    def drop(m):
        notes.append(f"cjk eliminado: {m.group(0)!r}")
        return ""
    t = cjk.sub(drop, t)
    # 3. U+FFFD
    if "\ufffd" in t:
        notes.append("U+FFFD encontrados")
        t = t.replace("\ufffd", "")
    # 4. limpiar espacios dobles SOLO fuera de los bloques de codigo.
    #    Los diagramas ASCII dependen de las columnas alineadas: comprimir
    #    los espacios multiples arruina las tablas de iteraciones de Dijkstra,
    #    los diagramas de trama y las tablas de campos. No se tocan.
    return "\n".join(_prosa(linea) for linea in t.split("\n")), notes


CODE_SPAN = re.compile(r"`[^`\n]*`")


def _prosa(linea: str) -> str:
    """Colapsa espacios multiples solo en los tramos fuera de `codigo`."""
    out = []
    for i, trozo in enumerate(CODE_SPAN.split(linea)):
        if i % 2:               # era un span de codigo: se deja intacto
            out.append(trozo)
            continue
        s = re.sub(r"[ \t]{2,}", " ", trozo)
        s = re.sub(r"\s+,", ",", s)
        s = re.sub(r",\s*,", ",", s)
        s = re.sub(r"\(\s+", "(", s)
        s = re.sub(r"\s+\)", ")", s)
        out.append(s)
    return "".join(out)

def main():
    root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else '.')
    total = 0
    for p in sorted(root.rglob('*.md')):
        if 'tools' in p.parts:
            continue
        raw = p.read_text(encoding='utf-8')
        if not re.search(r'[\u2e80-\u9fff\uff00-\uffef\ufffd]', raw):
            continue
        fixed, notes = fix_text(raw)
        p.write_text(fixed, encoding='utf-8', newline='\n')
        total += len(notes)
        print(f"{p.name}: {len(notes)} correcciones")
        for n in notes[:20]:
            print("   ", n)
    print(f"TOTAL correcciones: {total}")

if __name__ == '__main__':
    main()
