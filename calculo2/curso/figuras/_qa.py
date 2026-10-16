# -*- coding: utf-8 -*-
"""QA del curso: imagenes, enlaces internos, balance LaTeX, codificacion."""
import glob, os, re, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

d = r"C:\Utu\utu\calculo2\curso"
imgdir = os.path.join(d, "img")
have = set(os.listdir(imgdir))
files = sorted(os.path.basename(f) for f in glob.glob(os.path.join(d, "*.md")))
existing = set(files)

problems = []
used = set()

for name in files:
    t = open(os.path.join(d, name), encoding="utf-8").read()

    # 1. imagenes referenciadas existen
    for m in re.findall(r"!\[[^\]]*\]\((img/[^)]+)\)", t):
        b = os.path.basename(m)
        used.add(b)
        if b not in have:
            problems.append(f"{name}: IMAGEN FALTANTE {b}")

    # 2. enlaces internos a .md
    for link in re.findall(r"\]\(([\w]+\.md)\)", t):
        if link not in existing:
            problems.append(f"{name}: ENLACE ROTO -> {link}")

    # 3. balance de matematicas
    if t.count("$$") % 2:
        problems.append(f"{name}: $$ impar ({t.count('$$')})")
    # contar solo \left / \right de delimitadores, no \leftrightarrow / \leftarrow / \rightarrow
    n_left = len(re.findall(r"\\left(?![a-zA-Z])", t))
    n_right = len(re.findall(r"\\right(?![a-zA-Z])", t))
    if n_left != n_right:
        problems.append(f"{name}: \\left/\\right desbalanceado ({n_left}/{n_right})")
    if len(re.findall(r"\\begin\{", t)) != len(re.findall(r"\\end\{", t)):
        problems.append(f"{name}: \\begin/\\end desbalanceado")

    # 4. codificacion
    if "\ufffd" in t:
        problems.append(f"{name}: U+FFFD")
    if "\u20ac" in t or "\u00c3" in t:
        problems.append(f"{name}: mojibake")

# 5. figuras huerfanas
orphans = sorted(have - used)
print("PNG usados:", len(used), "| PNG totales:", len(have))
print("PNG sin usar en .md:", orphans if orphans else "ninguno")

# 6. inventario por clase
print("\n--- Inventario de clases (figuras / ejercicios) ---")
sin_fig = []
for name in files:
    if not name[:2].isdigit() or name[:2] == "00":
        continue
    t = open(os.path.join(d, name), encoding="utf-8").read()
    fig = len(re.findall(r"!\[[^\]]*\]\((img/[^)]+)\)", t))
    ej = len(re.findall(r"^### Ejercicio", t, flags=re.M))
    if fig == 0:
        sin_fig.append(name)
    print(f"{name:50s} figuras={fig} ejercicios={ej}")
if sin_fig:
    print("CLASES SIN FIGURAS:", sin_fig)

print("\nPROBLEMAS:", "\n".join(problems) if problems else "ninguno")
