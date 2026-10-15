# -*- coding: utf-8 -*-
"""Figuras del Bloque 4 — Series numéricas (clases 21-25).
Genera: b4_reducidas, b4_comparacion, b4_pserie, b4_cociente, b4_alternada,
        b4_absoluta, b4_sierpinski, b4_mapa  (PNG en curso/img/)."""
import math
import os
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.stdout.reconfigure(encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, "..", "img"))
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"figure.dpi": 130, "font.size": 10,
                     "axes.grid": True, "grid.alpha": 0.3})


def guardar(fig, nombre):
    p = os.path.join(OUT, nombre + ".png")
    fig.savefig(p, bbox_inches="tight")
    plt.close(fig)
    print("OK", nombre)


def titulos(pad, sub, sup):
    pad.set_title(sub, fontsize=13, pad=pad)
    for a in pad:
        a.set_title(sup, fontsize=10)


# 1. La reducida: crecimientos
def reducidas():
    n = np.linspace(1, 6, 300)
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.plot(n, np.log(n), label=r"$\ln n$  (crece, pero chiquito)", lw=2.2)
    ax.plot(n, n ** 0.5, label=r"$n^{0.5}$", lw=2)
    ax.plot(n, n, label=r"$n$  (lineal)", lw=2)
    ax.plot(n, n * np.log(n), label=r"$n\ln n$", lw=2.2)
    ax.plot(n, n ** 2, label=r"$n^2$", lw=2)
    ax.plot(n, 1.2 ** n, label=r"$1.2^{n}$  (exponencial)", lw=2.4)
    ax.plot(n, [float(math.factorial(min(int(round(x)), 6))) for x in n],
            label=r"$n!$", lw=2.4)
    ax.plot(n, np.array([int(round(x)) for x in n]) ** np.array([int(round(x)) for x in n], dtype=float) * 0.02,
            label=r"$n^{n}$ (muy rápido)", lw=1.6, ls="--")
    ax.set_ylim(0, 400)
    ax.set_xlabel(r"$n$")
    ax.set_ylabel("crecimiento del término $a_n$")
    ax.set_title("La reducida de crecimientos: para la raíz, $n$ nunca gana",
                 fontsize=12)
    ax.legend(loc="upper left", fontsize=8.5, framealpha=0.95)
    guardar(fig, "b4_reducidas")


# 2. Comparacion con divergente
def comparacion():
    n = np.arange(1, 40)
    fig, ax = plt.subplots(figsize=(7, 4.2))
    ax.plot(n, 1.0 / n, "o-", ms=4, label=r"$\dfrac{1}{n}$  (Armónico, $\to 0$, serie diverge)",
            lw=1.8, alpha=0.85)
    ax.plot(n, 0.7 / n, "s-", ms=4, label=r"$\dfrac{0.7}{n}$  (¡va a 0 igual!)", lw=1.8, alpha=0.85)
    ax.plot(n, 1.0 / n ** 0.99, "^-", ms=4, label=r"$\dfrac{1}{n^{0.99}}$  (también va a 0)", lw=1.8, alpha=0.85)
    ax.set_xlabel(r"$n$")
    ax.set_ylabel(r"$a_n$")
    ax.set_ylim(0, 1.05)
    ax.set_title(r"Ir a cero $NO$ basta: $\sum 1/n$ y $\sum 0.7/n$ divergen igual"
                 "\n(porque $\sum 0.7/n = 0.7\sum 1/n = \infty$)", fontsize=11)
    ax.legend(fontsize=9, loc="upper right")
    guardar(fig, "b4_comparacion")


# 3. p-series
def pserie():
    fig, ax = plt.subplots(figsize=(7, 4.5))
    xs = np.linspace(1, 60, 600)
    for p, ls in [(0.5, "-"), (1.0, "-"), (1.5, "-"), (2.0, "-"), (3.0, "--")]:
        y = xs ** (-p)
        estado = "DIVERGE" if p <= 1 else "converge"
        ax.plot(xs, y, ls, lw=2, label=rf"$p={p}$  $\to$ {estado}")
    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$x^{-p}$")
    ax.set_title("Serie $p$: para $p\\leq 1$ la cola es demasiado gorda (área $=\\infty$)"
                 "\n$\\int_1^\\infty x^{-p}\\,dx = 1/(p-1)$ si $p>1$;   y   $+\\infty$ si $p\\leq 1$",
                 fontsize=11)
    ax.set_ylim(0, 1.6)
    ax.legend(fontsize=9, loc="upper right")
    guardar(fig, "b4_pserie")


# 4. Cociente y radius efectivo
def cociente():
    fig, pad = plt.subplots(1, 2, figsize=(10, 4.2))
    n = np.arange(1, 16)

    ax = pad[0]
    for c, col in [(0.5, "tab:green"), (0.9, "tab:blue"), (1.1, "tab:orange"), (1.5, "tab:red")]:
        ax.plot(n, c ** n, "o-", ms=4, color=col, lw=1.6,
                label=rf"$c={c}$  $L={'<1' if c<1 else '>1'}$")
    ax.set_yscale("log")
    ax.set_xlabel(r"$n$")
    ax.set_ylabel(r"$c^n$ (escala log)", rotation=90)
    ax.set_title("Cociente: $L<1$ colapsa, $L>1$ explota\n(raíz $=$ cociente de la potencia)",
                 fontsize=10.5)
    ax.legend(fontsize=8.5)

    ax = pad[1]
    xs = np.linspace(-4, 4, 400)
    for R, col, ls in [(1, "tab:red", "--"), (2, "tab:orange", "-"), (3, "tab:green", "-")]:
        ax.plot(xs, np.where(np.abs(xs) < R, np.abs(xs) ** 0 * (R - np.abs(xs)) / R, 0),
                color=col, lw=2, ls=ls, label=rf"radio $R={R}$")
    ax.axvline(0, color="k", lw=1)
    ax.scatter([0], [1], color="k", zorder=5)
    ax.annotate(r"$|z-z_0|=0$:\nsiempre $|w|^0=1$", (0, 1.06), fontsize=8.5, ha="center")
    ax.set_xlabel(r"$|z-z_0|$")
    ax.set_ylabel("contribución de la potencia")
    ax.set_ylim(-0.1, 1.3)
    ax.set_title("Radio de convergencia: adentro $|z-z_0|<R$ la potencia vence\n"
                 "a $|a_n|\\to\\infty$; afuera no hay chance", fontsize=10.5)
    ax.legend(fontsize=8.5)
    fig.suptitle("Cociente y raíz: el mismo test visto de dos formas", fontsize=13, y=1.02)
    guardar(fig, "b4_cociente")


# 5. Alternadas: acotacion
def alternada():
    n = np.arange(1, 20)
    fig, pad = plt.subplots(1, 2, figsize=(10, 4.2))

    ax = pad[0]
    b = 1.0 / np.sqrt(n)
    ax.plot(n, b, "o-", ms=4, color="tab:green", label=r"$b_n=1/\sqrt{n}$ decrece")
    ax.plot(n, -b, "s-", ms=4, color="tab:green")
    ax.fill_between(n, -b, b, color="tab:green", alpha=0.15)
    ax.axhline(0, color="k", lw=1)
    ax.set_title("Leibniz OK: $b_n\\downarrow 0$\nLa suma queda acotada en el corredor",
                 fontsize=10.5)
    ax.set_xlabel(r"$n$"); ax.set_ylabel(r"$a_n=(-1)^{n-1}b_n$")
    ax.legend(fontsize=9, loc="upper right")

    ax = pad[1]
    b2 = 1.0 + 1.0 / n          # NO va a cero
    ax.plot(n, b2, "o-", ms=4, color="tab:red", label=r"$b_n=1+1/n$ ¡NO va a 0!")
    ax.plot(n, -b2, "s-", ms=4, color="tab:red")
    ax.axhline(0, color="k", lw=1)
    ax.set_ylim(-2.6, 2.6)
    ax.set_title("Falla el 2.° condición: $b_n\\to1$\nLos términos no van a 0 (falla Necesaria)",
                 fontsize=10.5)
    ax.set_xlabel(r"$n$"); ax.set_ylabel(r"$a_n$")
    ax.legend(fontsize=9, loc="upper right")
    fig.suptitle("Serie alternada: se alternan signos y $b_n\\downarrow0$ ⇒ converge",
                 fontsize=13, y=1.02)
    guardar(fig, "b4_alternada")


# 6. Condicional vs absoluta
def absoluta():
    n = np.arange(1, 40)
    a = (-1.0) ** (n + 1) / n
    S = np.cumsum(a)
    Sabs = np.cumsum(np.abs(a))
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    ax.plot(n, S, "o-", ms=3.5, lw=1.5, color="tab:blue",
            label=r"$S_N=\sum_{n\leq N}(-1)^{n-1}/n$  $\to\ln 2\approx0{,}693$")
    ax.axhline(np.log(2), color="tab:blue", ls=":", lw=1.4, label=r"$\ln 2$")
    ax.plot(n, Sabs, "s-", ms=3.5, lw=1.5, color="tab:red",
            label=r"$\sum_{n\leq N}1/n$ (armónico) $\to\infty$")
    ax.set_xlabel(r"$N$")
    ax.set_ylabel("sumas parciales")
    ax.set_title("Armónico alternado: CONDICIONAL\nla serie converge pero $\sum|a_n|=\\infty$ "
                 "(no es $C^1$ de $p$)", fontsize=11)
    ax.legend(fontsize=9, loc="upper left")
    ax.set_ylim(-0.4, 3.2)
    guardar(fig, "b4_absoluta")


# 7. Triangulo de Sierpinski
def sierpinski():
    def tri(v, nivel, lado):
        if nivel == 0:
            x = [p[0] for p in v] + [v[0][0]]
            y = [p[1] for p in v] + [v[0][1]]
            ax.fill(x, y, color="tab:blue", alpha=0.75)
            return
        m = [((v[0][0] + v[1][0]) / 2, (v[0][1] + v[1][1]) / 2),
             ((v[1][0] + v[2][0]) / 2, (v[1][1] + v[2][1]) / 2),
             ((v[2][0] + v[0][0]) / 2, (v[2][1] + v[0][1]) / 2)]
        tri([v[0], m[0], m[2]], nivel - 1, lado)
        tri([m[0], v[1], m[1]], nivel - 1, lado)
        tri([m[2], m[1], v[2]], nivel - 1, lado)

    fig, pad = plt.subplots(1, 4, figsize=(11, 3.1))
    for k, ax in enumerate(pad):
        ax.axis("off")
        ax.set_xlim(-0.05, 1.05); ax.set_ylim(-0.1, 1.1)
        ax.set_title(["nivel 0: $A=1$, $P=3$", "nivel 1: $A=(3/4)^1$",
                      "nivel 2: $A=(3/4)^2$", "nivel $k$: $A_k=(3/4)^k$"][k], fontsize=9.5)
        tri([(0, 0), (1, 0), (0.5, np.sqrt(3) / 2)], k, 1)
    fig.suptitle("Sierpiński (P3 ej.9): $A_k=(3/4)^k\\to0$   pero   "
                 "$P_k=3(3/2)^k\\to\\infty$", fontsize=12, y=1.06)
    guardar(fig, "b4_sierpinski")


# 8. Mapa del bloque
def mapa():
    fig, ax = plt.subplots(figsize=(8.6, 5.6))
    ax.axis("off")
    cajas = [
        (0.50, 0.93, "SERIE NUMÉRICA\n$\\sum a_n$  (Bloque 4)", "tab:blue"),
        (0.16, 0.70, "POSITIVOS ($a_n\\geq0$)\n$r$, $p$, comparación\ny equivalentes", "tab:green"),
        (0.50, 0.70, "ALTERNADAS\nLeibniz:\n$(-1)^n b_n$, $b_n\\downarrow0$", "tab:orange"),
        (0.84, 0.70, "ARBITRARIAS\n$\\sum|a_n|<\\infty\\Rightarrow$ abs.\nsino: ¿condicional?", "tab:red"),
        (0.50, 0.47, "CONVERGENCIA vs SUMA\nla suma NO es $\lim a_n$\n$\\sum\\frac{1}{2^n}=2$, "
                     "$\\sum\\frac{1}{n}=\\infty$", "tab:purple"),
        (0.16, 0.24, "PODEROSA de $n$:\n$n!\\gg a^n\\gg n^k$\n(raíz gana a todo)", "tab:olive"),
        (0.50, 0.24, "PROBLEMAS TÍPICOS\nabrir $|\\cdot|$, $b_n\\to0$,\nR de $\ln(1+z)$: $|z|<1$",
         "steelblue"),
        (0.84, 0.24, "PARCIAL/EXAMEN\nselectivas + numéricas\nde $S_N$", "firebrick"),
        (0.50, 0.05, "TEOREMA FUNDAMENTAL: $|a_n|\\to0$ (Necesaria)  ·  Leibniz  ·  "
                     "$r$ y $p$  ·  comparación de positivos", "dimgray"),
    ]
    for x, y, t, c in cajas:
        ax.add_patch(plt.Rectangle((x - 0.145, y - 0.075), 0.29, 0.15, fc=c, alpha=0.16,
                                   ec=c, lw=2, zorder=2))
        ax.text(x, y, t, ha="center", va="center", fontsize=8.4, zorder=3)
    flechas = [((0.5, 0.855), (0.16, 0.775)), ((0.5, 0.855), (0.5, 0.775)),
               ((0.5, 0.855), (0.84, 0.775)), ((0.16, 0.625), (0.4, 0.545)),
               ((0.5, 0.625), (0.5, 0.545)), ((0.84, 0.625), (0.6, 0.545)),
               ((0.34, 0.47), (0.24, 0.315)), ((0.5, 0.395), (0.5, 0.315)),
               ((0.66, 0.47), (0.76, 0.315)),
               ((0.16, 0.165), (0.36, 0.125)), ((0.5, 0.165), (0.5, 0.125)),
               ((0.84, 0.165), (0.64, 0.125))]
    for a, b in flechas:
        ax.annotate("", xy=b, xytext=a, arrowprops=dict(arrowstyle="->", lw=1.4, color="gray"))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.set_title("Mapa del Bloque 4 — Series numéricas (clases 21 a 25)", fontsize=13)
    guardar(fig, "b4_mapa")


if __name__ == "__main__":
    reducidas()
    comparacion()
    pserie()
    cociente()
    alternada()
    absoluta()
    sierpinski()
    mapa()
    print("BLOQUE 4 LISTO:", len([f for f in os.listdir(OUT) if f.startswith("b4_")]), "figuras")
