import pathlib

P = pathlib.Path(r"C:\Utu\utu\redescomp\clases\clase-08-http.md")
t = P.read_text(encoding="utf-8")


def cut(start, end, label):
    global t
    i = t.index(start)
    j = t.index(end, i)
    print(label, j - i)
    t = t[:i] + t[j:]


cut("   ┌──────────── HTTP (capa 7)", "### (b) HTTP no es lo mismo", "1.2a-ascii")
cut("**b) ¿Qué hubiera pasado sin `If-None-Match`?**", "**c) ¿Cuánto se ahorró?**", "2.2-b")
cut("**d) ¿Y si el servidor hubiera respondido 200?**", "## 2.3 Ejercicio 3", "2.2-d")
cut("| Método | Qué hace | Seguro | Idempotente |", "## 1.4 El mensaje HTTP: la respuesta", "1.3-metodos")

P.write_text(t, encoding="utf-8", newline="")
print("TOTAL", len(t))