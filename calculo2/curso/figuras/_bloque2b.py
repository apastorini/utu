# -*- coding: utf-8 -*-
"""Figuras adicionales del Bloque 2 (clases 11, 12, 14, 15).
Genera: b2_factor_integrante, b2_rayos, b2_seleccion, b2_mapa2 (PNG en curso/img/)."""
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


# Clase 11: familia de soluciones y = k e^{sen x} (espacio de dimensión 1)
def factor_integrante():
    x = np.linspace(-3.5, 6.5, 600)
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    for k, col in [(-2, "tab:red"), (-1, "tab:orange"), (0, "gray"),
                   (1, "tab:blue"), (2, "tab:green")]:
        y = k * np.exp(np.sin(x))
        ax.plot(x, y, lw=2, color=col,
                label=(r"$k=0$ (función nula)" if k == 0 else rf"$k={k}$"))
    ax.axhline(0, color="k", lw=0.8)
    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$y=k\,e^{\sin x}$")
    ax.set_ylim(-6, 6)
    ax.set_title("Solución de $y'-\\cos(x)\\,y=0$: la familia $y=k\\,e^{\\sin x}$\n"
                 "todas son múltiplos de una misma base $\\Rightarrow$ espacio de dimensión 1",
                 fontsize=11)
    ax.legend(fontsize=8.5, loc="upper left")
    guardar(fig, "b2_factor_integrante")


# Clase 12: campo de pendientes de y' = f(y/x), constante a lo largo de cada rayo
def rayos():
    xs = np.linspace(0.25, 3.2, 22)
    ys = np.linspace(-3.2, 3.2, 26)
    X, Y = np.meshgrid(xs, ys)
    F = (Y ** 2 + X ** 2) / (X * Y)          # y' = (y^2 + x^2)/(x y)
    N = np.sqrt(1 + F ** 2)
    U, V = 1.0 / N, F / N
    fig, ax = plt.subplots(figsize=(6.6, 5.2))
    ax.quiver(X, Y, U, V, color="steelblue", alpha=0.55, pivot="mid")
    xr = np.linspace(0.05, 3.2, 50)
    for m, col in [(1, "tab:green"), (2, "tab:orange"), (-1, "tab:red")]:
        ax.plot(xr, m * xr, color=col, lw=2, label=rf"rayo $y={m}x$")
    ax.axhline(0, color="k", lw=0.8)
    ax.set_xlim(0, 3.3)
    ax.set_ylim(-3.3, 3.3)
    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$y$")
    ax.set_title(r"Campo de pendientes de $y'=\dfrac{y^2+x^2}{xy}$"
                 "\nla dirección es la misma sobre todo un rayo "
                 r"$y=mx$ ($\Rightarrow$ cambio $u=y/x$)", fontsize=10.5)
    ax.legend(fontsize=8.5, loc="upper right")
    guardar(fig, "b2_rayos")


# Clase 14: y = y_H + y_P  (particular parábola + homogénea oscilante)
def seleccion():
    x = np.linspace(0, 3.0, 600)
    yP = 3 * x ** 2 - 5 * x - 6
    yH = 7 * np.cos(x) + 5 * np.sin(x)
    y = yH + yP
    fig, ax = plt.subplots(figsize=(7.5, 4.6))
    ax.plot(x, yP, lw=2, color="tab:orange", label=r"$y_P=3x^2-5x-6$ (particular)")
    ax.plot(x, yH, lw=2, ls="--", color="tab:blue",
            label=r"$y_H=7\cos x+5\sin x$ (homogénea)")
    ax.plot(x, y, lw=2.6, color="black", label=r"$y=y_H+y_P$ (solución de $y''+y=3x^2-5x$)")
    ax.axhline(0, color="k", lw=0.7)
    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$y$")
    ax.set_title("Estructura de la solución no homogénea: $y=y_H+y_P$", fontsize=12)
    ax.legend(fontsize=8.5, loc="upper left")
    guardar(fig, "b2_seleccion")


# Clase 15: mapa del Bloque 2
def mapa2():
    fig, ax = plt.subplots(figsize=(8.8, 5.8))
    ax.axis("off")
    cajas = [
        (0.50, 0.94, "ECUACIÓN DIFERENCIAL\n(incógnita: una función)", "tab:blue"),
        (0.17, 0.74, "1.er ORDEN\n$y'=F(y)G(x)$\nseparables (c9/c10)", "tab:green"),
        (0.50, 0.74, "1.er ORDEN LINEAL\n$y'+a y=b$\nhomog. (c11) / factor (c12)", "tab:orange"),
        (0.83, 0.74, "1.er ORDEN $y'=f(y/x)$\n$u=y/x$ (c12)", "tab:red"),
        (0.33, 0.52, "2.º ORDEN HOMOGÉNEA\n$y''+ay'+by=0$\npolinomio car. (c13)", "tab:purple"),
        (0.72, 0.52, "2.º ORDEN NO HOM.\n$y_H+y_P$ (c14)", "tab:brown"),
        (0.50, 0.30, "APLICACIONES (c10)\ncaída, poblaciones,\nrepresa, decaimiento", "steelblue"),
        (0.50, 0.11, "EXAMEN: verificar = derivar y sustituir · elegir método · "
                     "condiciones iniciales", "firebrick"),
    ]
    for x, y, t, c in cajas:
        ax.add_patch(plt.Rectangle((x - 0.155, y - 0.075), 0.31, 0.15,
                                   fc=c, alpha=0.16, ec=c, lw=2, zorder=2))
        ax.text(x, y, t, ha="center", va="center", fontsize=8.2, zorder=3)
    flechas = [((0.5, 0.865), (0.17, 0.815)), ((0.5, 0.865), (0.50, 0.815)),
               ((0.5, 0.865), (0.83, 0.815)),
               ((0.17, 0.665), (0.30, 0.595)), ((0.50, 0.665), (0.33, 0.595)),
               ((0.50, 0.665), (0.70, 0.595)), ((0.83, 0.665), (0.74, 0.595)),
               ((0.50, 0.665), (0.5, 0.375)),
               ((0.33, 0.445), (0.45, 0.375)), ((0.72, 0.445), (0.55, 0.375))]
    for a, b in flechas:
        ax.annotate("", xy=b, xytext=a,
                    arrowprops=dict(arrowstyle="->", lw=1.4, color="gray"))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_title("Mapa del Bloque 2 — Ecuaciones diferenciales (clases 9 a 15)",
                 fontsize=13)
    guardar(fig, "b2_mapa2")


if __name__ == "__main__":
    factor_integrante()
    rayos()
    seleccion()
    mapa2()
    print("BLOQUE 2 (extra) LISTO")
