import pathlib, sys

t = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
lines = t.splitlines()
# limites: inicio de cada linea que empieza con '## ' o '# PARTE'
starts = [(i + 1, l.strip()) for i, l in enumerate(lines)
          if l.startswith("# PARTE") or l.startswith("## ") or l.startswith("## ✅")
          or l.startswith("## 🔗") or l.startswith("## 📌")]
acum = 0
for idx, (n, titulo) in enumerate(starts):
    fin = starts[idx + 1][0] if idx + 1 < len(starts) else len(lines) + 1
    seg = "\n".join(lines[n - 1:fin - 1])
    # quitar bloques de codigo para ver cuanto es prosa
    sin = []
    dentro = False
    for l in lines[n - 1:fin - 1]:
        if l.lstrip().startswith("```"):
            dentro = not dentro
            continue
        if not dentro:
            sin.append(l)
    prosa = len("\n".join(sin))
    print("%6d total %6d prosa  L%4d  %s" % (len(seg), prosa, n, titulo[:64]))
print("TOTAL", len(t))