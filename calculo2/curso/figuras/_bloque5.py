# -*- coding: utf-8 -*-
"""Figuras del Bloque 5 — Integrales impropias (clases 26-29).
Genera: b5_area_infinito, b5_colas, b5_comparacion, b5_singularidad,
        b5_serie_integral, b5_torricelli, b5_gamma, b5_mapa  (PNG en curso/img/)."""
import os
import sys
import math
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


# 1. Area bajo 1/x^2 hasta el infinito (primera especie)
def area_infinito():
    x = np.linspace(1, 8, 400)
    fig, ax = plt.subplots(figsize=(7, 4.4))
    ax.plot(x, 1 / x ** 2, "tab:blue", lw=2.4, label=r"$f(x)=\dfrac{1}{x^{2}}$")
    xi = np.linspace(1, 8, 600)
    ax.fill_between(xi, 1 / xi ** 2, color="tab:blue", alpha=0.25)
    xf = np.linspace(8, 10.5, 300)
    ax.fill_between(xf, 1 / xf ** 2, color="tab:blue", alpha=0.08)
    ax.annotate("", xy=(10.3, 0.0), xytext=(8, 0.0),
                arrowprops=dict(arrowstyle="->", lw=1.6, color="gray"))
    ax.text(8.6, 0.12, "…hasta $+\\infty$\n$F(x)=1-\\frac{1}{x}\\to 1$", fontsize=9.5)
    ax.axhline(1, color="tab:red", ls="--", lw=1.3)
    ax.text(1.15, 1.02, r"$\int_1^{\infty}\frac{dx}{x^{2}}=1$  (CONVERGE)",
            color="tab:red", fontsize=11)
    ax.set_xlim(1, 10.5)
    ax.set_ylim(0, 1.25)
    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$f(x)$")
    ax.set_title("Primera especie: se integra hasta $b$ y se hace $b\\to+\\infty$"
                 "\n$\\int_1^{b}x^{-2}dx=1-\\frac{1}{b}\\to1$: el área satura en 1",
                 fontsize=11)
    ax.legend(loc="upper right")
    guardar(fig, "b5_area_infinito")


# 2. Colas: converge vs diverge
def colas():
    x = np.linspace(1, 9, 400)
    fig, pad = plt.subplots(1, 2, figsize=(10, 4.1))

    ax = pad[0]
    ax.plot(x, 1 / x ** 2, "tab:green", lw=2.4)
    ax.fill_between(x, 1 / x ** 2, color="tab:green", alpha=0.3)
    ax.set_title("Cola \"delgada\": $1/x^{2}$\n"
                 "$\\int_1^\\infty x^{-2}dx=1<\\infty$  →  CONVERGE", fontsize=10.5)
    ax.set_ylim(0, 1.15)
    ax.legend([r"cola de área finita"], fontsize=9, loc="upper right")

    ax = pad[1]
    ax.plot(x, 1 / x, "tab:red", lw=2.4)
    ax.fill_between(x, 1 / x, color="tab:red", alpha=0.3)
    ax.set_title("Cola \"gruesa\": $1/x$\n"
                 "$\\int_1^\\infty x^{-1}dx=\\infty$  →  DIVERGE", fontsize=10.5)
    ax.set_ylim(0, 1.15)
    ax.legend([r"cola de área infinita"], fontsize=9, loc="upper right")

    for a in pad:
        a.set_xlabel(r"$x$")
    fig.suptitle("Las dos funciones van a 0… pero la cola decide la convergencia",
                 fontsize=12.5, y=1.03)
    guardar(fig, "b5_colas")


# 3. Comparacion: por arriba converge / por abajo diverge
def comparacion():
    x = np.linspace(1, 6, 400)
    fig, pad = plt.subplots(1, 2, figsize=(10, 4.1))

    ax = pad[0]
    ax.fill_between(x, 0.6 / x ** 1.5, color="tab:blue", alpha=0.25)
    ax.plot(x, 0.6 / x ** 1.5, "tab:blue", lw=2.2, label=r"$f$ (chiquita)")
    ax.plot(x, 2.0 / x ** 1.5, "tab:red", lw=2.2, label=r"$g$ (grande, converge)")
    ax.set_title("Si $0\\leq f\\leq g$ y $\\int g<\\infty$:\n"
                 "→ $\\int f<\\infty$  (lo chico converge)", fontsize=10.5)
    ax.legend(fontsize=9, loc="upper right")

    ax = pad[1]
    ax.fill_between(x, 2.0 / x ** 0.8, color="tab:red", alpha=0.25)
    ax.plot(x, 2.0 / x ** 0.8, "tab:red", lw=2.2, label=r"$f$ (grande)")
    ax.plot(x, 0.6 / x ** 0.8, "tab:blue", lw=2.2, label=r"$g$ (chiquita, diverge)")
    ax.set_title("Si $0\\leq g\\leq f$ y $\\int g=\\infty$:\n"
                 "→ $\\int f=\\infty$  (lo grande diverge)", fontsize=10.5)
    ax.legend(fontsize=9, loc="upper right")

    for a in pad:
        a.set_xlabel(r"$x$")
        a.set_ylim(0, 2.3)
    fig.suptitle("Criterio de comparación (Prop. 4.6): las flechas importan, "
                 "como en series", fontsize=12.5, y=1.03)
    guardar(fig, "b5_comparacion")


# 4. Singularidad en un punto (segunda especie)
def singularidad():
    x = np.linspace(0.015, 1, 400)
    fig, pad = plt.subplots(1, 2, figsize=(10, 4.1))

    ax = pad[0]
    ax.plot(x, 1 / np.sqrt(x), "tab:green", lw=2.4)
    ax.fill_between(x, 1 / np.sqrt(x), color="tab:green", alpha=0.3)
    ax.set_title("$\\dfrac{1}{\\sqrt{x}}$ explota en 0, pero $p=\\frac{1}{2}<1$:\n"
                 "$\\int_0^1 x^{-1/2}dx=2<\\infty$  →  CONVERGE", fontsize=10.5)
    ax.set_ylim(0, 9)

    ax = pad[1]
    ax.plot(x, 1 / x ** 2, "tab:red", lw=2.4)
    ax.fill_between(x, 1 / x ** 2, color="tab:red", alpha=0.3)
    ax.set_title("$\\dfrac{1}{x^{2}}$ también explota, pero $p=2\\geq1$:\n"
                 "$\\int_0^1 x^{-2}dx=\\infty$  →  DIVERGE", fontsize=10.5)
    ax.set_ylim(0, 90)

    for a in pad:
        a.set_xlabel(r"$x$")
        a.axvline(0, color="k", lw=1)
    fig.suptitle("Segunda especie: lo que decide es cuán rápido explota en el punto "
                 "($p<1$ converge, $p\\geq1$ diverge)", fontsize=12, y=1.03)
    guardar(fig, "b5_singularidad")


# 5. Criterio serie-integral: escaleras de Riemann
def serie_integral():
    n = np.arange(1, 11)
    f = lambda t: 1.0 / t ** 1.5
    x = np.linspace(1, 10.5, 500)
    fig, ax = plt.subplots(figsize=(7.6, 4.5))
    ax.plot(x, f(x), "k-", lw=2.4, label=r"$f(x)$ decreciente y positiva")
    # escalera inferior: altura f(n+1) en [n, n+1]
    for k in range(1, 10):
        ax.fill_between([k, k + 1], 0, f(k + 1), color="tab:blue", alpha=0.2)
    # escalera superior: altura f(n) en [n-1, n]
    for k in range(1, 10):
        ax.plot([k - 0.0, k + 1], [f(k), f(k)], color="tab:red", lw=1.2, alpha=0.8)
    ax.bar(n - 0.5, f(n), width=1.0, bottom=0, color="tab:red", alpha=0.12,
           edgecolor="tab:red", linewidth=0.8)
    ax.text(5.4, 0.32, "barras ROJAS: $\\sum_{n=1}^{9}f(n)$ (serie)\n"
                       "azules: $\\sum_{n=2}^{10}f(n)\\leq\\int_1^{10}f\\leq$ rojas",
            fontsize=9.5)
    ax.set_title(r"Teorema 4.11 (serie-integral): $f$ decreciente $\geq$0 $\Rightarrow$ "
                 r"$\sum f(n)$ y $\int f$ van juntos"
                 "\n"
                 r"(acotan la misma área con escaleras)",
                 fontsize=11)
    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$f(x)$")
    ax.set_ylim(0, 1.15)
    ax.legend(fontsize=9, loc="upper right")
    guardar(fig, "b5_serie_integral")


# 6. Trompeta de Torricelli
def torricelli():
    x = np.linspace(1, 9, 400)
    y = 1 / x
    fig, ax = plt.subplots(figsize=(8.2, 4.2))
    ax.plot(x, y, "tab:blue", lw=2.6, label=r"$f(x)=1/x$")
    ax.plot(x, -y, "tab:blue", lw=2.6)
    ax.fill_between(x, -y, y, color="tab:blue", alpha=0.12)
    # "secciones" elípticas que sugieren la revolución
    for k, w in [(1.0, 1.0), (2.0, 0.5), (3.0, 1 / 3), (4.5, 1 / 4.5), (6.5, 1 / 6.5)]:
        t = np.linspace(0, 2 * np.pi, 200)
        ax.plot(k + w * 0.35 * np.cos(t), w * np.sin(t), color="gray", lw=1.0, alpha=0.8)
    ax.axhline(0, color="k", lw=0.8)
    ax.set_xlim(0.5, 9.2)
    ax.set_ylim(-1.25, 1.25)
    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$y$")
    ax.set_title("Trompeta de Torricelli: $V=\\pi\\int_1^\\infty x^{-2}dx=\\pi$ (finito)\n"
                 "pero $A=2\\pi\\int_1^\\infty \\frac{\\sqrt{1+x^{-4}}}{x}dx\\geq "
                 "2\\pi\\int_1^\\infty\\frac{dx}{x}=\\infty$ (infinita)",
                 fontsize=11)
    ax.legend(loc="upper right")
    guardar(fig, "b5_torricelli")


# 7. Funcion Gamma
def gamma():
    xs = np.linspace(0.25, 5, 500)
    ys = np.array([math.exp(math.lgamma(t)) for t in xs])
    fig, ax = plt.subplots(figsize=(7.4, 4.5))
    ax.plot(xs, ys, "tab:purple", lw=2.4, label=r"$\Gamma(x)=\int_0^\infty e^{-t}t^{x-1}dt$")
    marcas = [(n, math.factorial(n - 1)) for n in range(1, 6)]
    ax.plot([m[0] for m in marcas], [m[1] for m in marcas], "o", color="tab:red",
            label=r"$\Gamma(n)=(n-1)!$")
    for nx, fx in marcas:
        ax.annotate(rf"$\Gamma({nx})={fx}$" if fx < 100 else rf"$\Gamma({nx})$",
                    (nx, fx), textcoords="offset points",
                    xytext=(8, -4), fontsize=8.5, color="tab:red")
    ax.axvline(0, color="k", lw=1)
    ax.set_xlim(0, 5.3)
    ax.set_ylim(0, 8)
    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$\Gamma(x)$")
    ax.set_title("Función Gamma: una curva suave que pasa por los factoriales corridos\n"
                 "$\\Gamma(1)=1,\\ \\Gamma(2)=1,\\ \\Gamma(3)=2,\\ \\Gamma(4)=6,\\ "
                 "\\Gamma(5)=24$ (escala cortada)", fontsize=11)
    ax.legend(fontsize=9, loc="upper center")
    guardar(fig, "b5_gamma")


# 8. Mapa del bloque
def mapa():
    fig, ax = plt.subplots(figsize=(8.8, 5.8))
    ax.axis("off")
    cajas = [
        (0.50, 0.93, "INTEGRALES\nIMPROPIAS\n$\\int_a^b f$: $b=\\infty$ o $f$ no acotada", "tab:blue"),
        (0.16, 0.70, "1.ª ESPECIE (infinito)\n$F(x)=\\int_a^x f\\to L$\nDef. 4.1", "tab:green"),
        (0.50, 0.70, "2.ª ESPECIE (punto $a$)\n$\\lim_{x\\to a^+}\\int_x^b f$\nDef. 4.19", "tab:orange"),
        (0.84, 0.70, "MIXTAS\npartir en sumandos\ncon UN solo problema", "tab:red"),
        (0.16, 0.47, "CRITERIOS\ncomparación (4.6),\nequivalentes (4.8), abs.", "tab:purple"),
        (0.50, 0.47, "$\\int_1^\\infty x^{-\\alpha}$: conv. sii $\\alpha>1$\n$\\int_0^1 x^{-\\alpha}$: conv. sii $\\alpha<1$\n¡opuestos!", "tab:olive"),
        (0.84, 0.47, "SERIE-INTEGRAL (4.11)\n$\\sum f(n)\\leftrightarrow\\int f$\nmisma clase", "steelblue"),
        (0.30, 0.24, "TORRICELLI\nvolumen finito,\nárea infinita", "teal"),
        (0.70, 0.24, "GAMMA\n$\\Gamma(n)=(n-1)!$,\nGauss: $\\Gamma(1/2)=\\sqrt{\\pi}$", "firebrick"),
        (0.50, 0.05, "IDEA DE FONDO: como en series — construir una función acumulada y estudiar su límite "
                     "(converge / diverge / oscila)", "dimgray"),
    ]
    for x, y, t, c in cajas:
        ancho = 0.30 if y == 0.05 else 0.28
        ax.add_patch(plt.Rectangle((x - ancho / 2, y - 0.075), ancho, 0.15, fc=c, alpha=0.16,
                                   ec=c, lw=2, zorder=2))
        ax.text(x, y, t, ha="center", va="center", fontsize=8.3, zorder=3)
    flechas = [((0.5, 0.855), (0.16, 0.775)), ((0.5, 0.855), (0.5, 0.775)),
               ((0.5, 0.855), (0.84, 0.775)), ((0.16, 0.625), (0.16, 0.545)),
               ((0.5, 0.625), (0.5, 0.545)), ((0.84, 0.625), (0.84, 0.545)),
               ((0.5, 0.395), (0.32, 0.315)), ((0.5, 0.395), (0.68, 0.315)),
               ((0.30, 0.165), (0.47, 0.125)), ((0.70, 0.165), (0.53, 0.125))]
    for a, b in flechas:
        ax.annotate("", xy=b, xytext=a, arrowprops=dict(arrowstyle="->", lw=1.4, color="gray"))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_title("Mapa del Bloque 5 — Integrales impropias (clases 26 a 29)", fontsize=13)
    guardar(fig, "b5_mapa")


if __name__ == "__main__":
    area_infinito()
    colas()
    comparacion()
    singularidad()
    serie_integral()
    torricelli()
    gamma()
    mapa()
    print("BLOQUE 5 LISTO:", len([f for f in os.listdir(OUT) if f.startswith("b5_")]), "figuras")
