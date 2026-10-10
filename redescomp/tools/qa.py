"""
QA de las clases. Ignora el contenido dentro de vallas de codigo (los diagramas
ASCII tienen multiples espacios y camelCase legitimos a proposito).
Uso:
    python tools/qa.py            # todas
    python tools/qa.py 21 24      # solo esas
"""
import re
import sys
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
CLASES = ROOT / "clases"

MIN_CHARS = 15000
MAX_CHARS = 90000
IDEAL_MAX = 55000   # a partir de aca conviene partir la clase en dos

CJK = re.compile(r"[\u2e80-\u9fff\uf900-\ufaff\uff00-\uffef\u3040-\u30ff]")

# Solo heuristicas que no producen falsos positivos en prosa espanola.
# Antes de aplicarlas se borran los spans de codigo en linea (`...`),
# que tienen camelCase legitimo.
HEURISTICAS = [
    # Estas dos heuristicas solo aplican a PROSA. En codigo C, "socket()" es una
    # llamada a funcion legitima y "getCongWinSize" es un identificador: no son
    # errores. Por eso exigen que no haya backtick ni palabra alrededor.
    (re.compile(r"(?<![\w`])([a-záéíóúñ]{5,})([A-ZÁÉÍÓÚÑ][a-záéíóú]{5,})(?![\w`])"),
     "palabra pegada por casing"),
    (re.compile(r"\(\s{2,}\)"), "parentesis con hueco"),
    (re.compile(r"\bque\s{2,}"), "doble espacio tras 'que'"),
    (re.compile(r"\s+[,;](?=\s)"), "coma con espacio de mas"),
    (re.compile(r"\b(de|del|la|el|que|y|se|lo|en|un|una|por|con|sin|para|como)\s{2,}"),
     "doble espacio tras palabra funcional"),
    # tres o mas letras iguales seguidas (typo tipo "Prrequisito")
    (re.compile(r"[a-záéíóúñ]{3,}"), None),   # se filtra abajo
    (re.compile(r"https?://"), None),         # se ignora si hay URL
]

# Excepciones legitimas de tripled letters
TRIPLES_OK = {"ooo", "eee", "aaa", "iii", "ooo"}
URL = re.compile(r"https?://\S+")

SPAN_CODIGO = re.compile(r"`[^`]*`")


def sin_codigo(linea: str) -> list[str]:
    """Trocea la linea y devuelve solo los tramos FUERA de los backticks."""
    return [s for i, s in enumerate(SPAN_CODIGO.split(linea)) if i % 2 == 0]

SECCIONES = [
    (re.compile(r"^#\s+Clase\s+\d+", re.M), "titulo '# Clase NN'"),
    (re.compile(r"Al terminar esta clase", re.I), "objetivos"),
    (re.compile(r"Actualizaci[oó]n a 2026", re.I), "caja de actualizacion"),
    (re.compile(r"Prerequisito del examen", re.I), "prerequisito del examen"),
    (re.compile(r"[Rr]esumen"), "resumen"),
    (re.compile(r"Autoevaluaci[oó]n", re.I), "autoevaluacion"),
    (re.compile(r"Referencias"), "referencias"),
    (re.compile(r"\*\*Bloque:\*\*"), "bloque en el encabezado"),
]


def fuera_de_codigo(txt: str) -> list[tuple[int, str]]:
    """Devuelve (numero_de_linea, linea) solo fuera de las vallas ```."""
    out, dentro = [], False
    for i, linea in enumerate(txt.splitlines(), 1):
        if linea.lstrip().startswith("```"):
            dentro = not dentro
            continue
        if not dentro:
            out.append((i, linea))
    return out


def revisar(path: pathlib.Path):
    txt = path.read_text(encoding="utf-8")
    n = len(txt)
    problemas = []

    for i, linea in fuera_de_codigo(txt):
        if CJK.search(linea) or "\ufffd" in linea:
            problemas.append((i, f"caracter raro (CJK/U+FFFD): {linea.strip()[:100]}"))

    for rx, desc in HEURISTICAS:
        if desc is None:
            continue
        for i, linea in fuera_de_codigo(txt):
            for trozo in sin_codigo(linea):
                m = rx.search(trozo)
                if m:
                    frag = trozo[max(0, m.start() - 30):m.end() + 40]
                    problemas.append((i, f"{desc}: ...{frag.strip()}..."))

    # letra repetida 3+ veces (typo tipo "Prrequisito"), fuera de URLs
    rx3 = re.compile(r"\b\w*([a-záéíóúñ])\1\1\w*\b")
    for i, linea in fuera_de_codigo(txt):
        for trozo in URL.sub(" ", sin_url := " ".join(sin_codigo(linea))):
            m = rx3.search(trozo)
            if m and m.group(1) * 3 not in TRIPLES_OK:
                frag = trozo[max(0, m.start() - 25):m.end() + 25]
                problemas.append((i, f"letra repetida x3: ...{frag.strip()}..."))

    # CJK dentro de codigo tambien cuenta (ej: una cadena de un diagrama)
    for i, linea in enumerate(txt.splitlines(), 1):
        if (CJK.search(linea) or "\ufffd" in linea):
            if not any(i == j for j, _ in problemas):
                problemas.append((i, f"caracter raro en bloque: {linea.strip()[:100]}"))

    if txt.count("```") % 2 != 0:
        problemas.append((0, "vallas de codigo ``` desbalanceadas"))

    for rx, nombre in SECCIONES:
        if not rx.search(txt):
            problemas.append((0, f"falta la seccion obligatoria: {nombre}"))

    if n < MIN_CHARS:
        problemas.append((0, f"CORTO: {n} caracteres (minimo {MIN_CHARS})"))
    elif n > MAX_CHARS:
        problemas.append((0, f"MUY LARGO: {n} caracteres (maximo {MAX_CHARS})"))
    elif n > IDEAL_MAX:
        problemas.append((0, f"largo: {n} caracteres (a partir de {IDEAL_MAX} "
                             f"conviene dividirla en dos)"))

    if txt.count("```") < 16:
        problemas.append((0, f"pocos diagramas: {txt.count('```')//2} bloques de codigo"))

    return n, problemas


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    archivos = sorted(CLASES.glob("clase-*.md"))
    if args:
        nums = {int(a) for a in args}
        archivos = [p for p in archivos
                    if re.match(r"clase-(\d\d)", p.name)
                    and int(re.match(r"clase-(\d\d)", p.name).group(1)) in nums]
    if not archivos:
        print("No hay clases.")
        return

    total = con = 0
    for p in archivos:
        n, probs = revisar(p)
        num = re.match(r"clase-(\d\d)", p.name).group(1)
        if probs:
            con += 1
            total += len(probs)
            print(f"\n=== clase-{num}  ({n} chars) — {len(probs)} hallazgo(s)")
            for ln, x in probs[:16]:
                print(f"    L{ln or '-'}: {x}")
            if len(probs) > 16:
                print(f"    ... y {len(probs)-16} mas")
        else:
            print(f"OK   clase-{num}  ({n} chars)")

    print(f"\n{'='*62}\n{len(archivos)} clases · {con} con hallazgos · {total} total")


if __name__ == "__main__":
    main()
