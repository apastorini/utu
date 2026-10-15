# -*- coding: utf-8 -*-
"""Figuras del Bloque 7 — Funciones de varias variables y continuidad (clases 34-36).
Genera: b7_mapa, b7_nivel_cuadrados, b7_silla, b7_dominio, b7_direccionales,
        b7_polares, b7_disco_agujereado, b7_weierstrass, b7_preimagen
(PNG en curso/img/)."""
import os
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Wedge, FancyArrowPatch

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


# 1. Mapa del bloque
def mapa():
    fig, ax = plt.subplots(figsize=(8.6, 5.6))
    ax.axis("off")
    cajas = [
        (0.50, 0.93, "FUNCIÓN $f: U\\subset\\mathbb{R}^n\\to\\mathbb{R}$\n(Bloque 7)", "tab:blue"),
        (0.16, 0.70, "CLASE 34:\nDOMINIO + CURVAS\nDE NIVEL + GRÁFICA", "tab:green"),
        (0.50, 0.70, "CLASE 35:\nLÍMITES: caminos,\nsucesiones, polares", "tab:orange"),
        (0.84, 0.70, "CLASE 36:\nCONTINUIDAD\nε–δ y sucesiones", "tab:red"),
        (0.50, 0.47, "$\\lim_{x\\to a}f(x)=f(a)$ (a acumulación)\n"
                     "$f(x_k)\\to f(a)$ $\\forall x_k\\to a$\n"
                     "LOS CAMINOS NO BASTAN: hay que probar $\\forall$", "tab:purple"),
        (0.16, 0.24, "DOMINIO:\nsin divisiones por 0,\nsin raíces de negativos,\n"
                     "argumento de $\\log$ positivo", "tab:olive"),
        (0.50, 0.24, "POLARES: $\\rho^{k}\\times$\nfactor acotado en $\\theta$\n$\\Rightarrow$ límite 0",
         "steelblue"),
        (0.84, 0.24, "WEIERSTRASS:\ncontinua + compacto\n$\\Rightarrow$ alcanza mín y máx",
         "firebrick"),
        (0.50, 0.05, "$\\varepsilon$–$\\delta$  ·  sucesiones  ·  direccionales  ·  polares  ·  "
                     "$f^{-1}(A)$ abierta $\\Leftrightarrow$ continua", "dimgray"),
    ]
    for x, y, t, c in cajas:
        ax.add_patch(plt.Rectangle((x - 0.145, y - 0.075), 0.29, 0.15, fc=c, alpha=0.16,
                                   ec=c, lw=2, zorder=2))
        ax.text(x, y, t, ha="center", va="center", fontsize=8.4, zorder=3)
    flechas = [((0.5, 0.855), (0.16, 0.775)), ((0.5, 0.855), (0.5, 0.775)),
               ((0.5, 0.855), (0.84, 0.775)), ((0.16, 0.625), (0.42, 0.545)),
               ((0.5, 0.625), (0.5, 0.545)), ((0.84, 0.625), (0.58, 0.545)),
               ((0.16, 0.165), (0.36, 0.125)), ((0.5, 0.165), (0.5, 0.125)),
               ((0.84, 0.165), (0.64, 0.125))]
    for a, b in flechas:
        ax.annotate("", xy=b, xytext=a, arrowprops=dict(arrowstyle="->", lw=1.4, color="gray"))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.set_title("Mapa del Bloque 7 — Funciones de varias variables y continuidad (34 a 36)",
                 fontsize=13)
    guardar(fig, "b7_mapa")


# 2. Curvas de nivel: paraboloide vs silla
def nivel_cuadrados():
    fig, pad = plt.subplots(1, 2, figsize=(10, 4.6))

    ax = pad[0]
    ax.set_aspect("equal")
    for r in [0.5, 1.0, 1.5, 2.0]:
        th = np.linspace(0, 2 * np.pi, 300)
        ax.plot(r * np.cos(th), r * np.sin(th), lw=1.8, color="tab:blue")
        ax.annotate(f"$C_{{{r**2:.2f}}}$", (r * 0.71, r * 0.71), fontsize=9, color="tab:blue")
    ax.scatter([0], [0], s=30, color="tab:blue")
    ax.annotate("$C_0=\\{(0,0)\\}$", (0.15, -0.45), fontsize=9)
    ax.set_xlim(-2.4, 2.4); ax.set_ylim(-2.4, 2.4)
    ax.set_title("$f(x,y)=x^2+y^2$: $C_a$ = circunferencias\nconcéntricas ($a>0$), vacías si $a<0$",
                 fontsize=10.5)

    ax = pad[1]
    ax.set_aspect("equal")
    xs = np.linspace(-2.3, 2.3, 400)
    for m in (1, -1):
        ax.plot(xs, m * xs, "--", color="gray", lw=1.2)
    ys = np.linspace(-2.2, 2.2, 400)
    for c, col in [(0.5, "tab:red"), (1.5, "tab:red")]:     # a > 0: abre a izq/der
        ax.plot(np.sqrt(ys ** 2 + c), ys, color=col, lw=1.8)
        ax.plot(-np.sqrt(ys ** 2 + c), ys, color=col, lw=1.8)
    for c, col in [(0.5, "tab:green"), (1.5, "tab:green")]:  # a < 0: abre arriba/abajo
        ax.plot(xs, np.sqrt(xs ** 2 + c), color=col, lw=1.8)
        ax.plot(xs, -np.sqrt(xs ** 2 + c), color=col, lw=1.8)
    ax.annotate("$C_0$: $y=\\pm x$", (0.35, 1.35), fontsize=9, rotation=45, color="dimgray")
    ax.annotate("$a>0$", (1.9, 0.55), fontsize=9, color="tab:red")
    ax.annotate("$a<0$", (0.45, 1.85), fontsize=9, color="tab:green")
    ax.set_xlim(-2.4, 2.4); ax.set_ylim(-2.4, 2.4)
    ax.set_title("$g(x,y)=x^2-y^2$: $C_a$ = hipérbolas\n(asintotas $y=\\pm x$ en $a=0$)", fontsize=10.5)
    fig.suptitle("Mismas fórmulas, distinta gráfica: los conjuntos de nivel viven en el 'piso'",
                 fontsize=12, y=1.02)
    guardar(fig, "b7_nivel_cuadrados")


# 3. Silla de montar z = x^2 - y^2
def silla():
    from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
    x = np.linspace(-2.2, 2.2, 120)
    y = np.linspace(-2.2, 2.2, 120)
    X, Y = np.meshgrid(x, y)
    Z = X ** 2 - Y ** 2
    fig = plt.figure(figsize=(8, 5.4))
    ax = fig.add_subplot(111, projection="3d")
    ax.plot_surface(X, Y, Z, cmap="coolwarm", alpha=0.9, linewidth=0, antialiased=True)
    t = np.linspace(-2.2, 2.2, 100)
    ax.plot(t, t, t * 0, color="k", lw=2)        # corte z=0: y = x
    ax.plot(t, -t, t * 0, color="k", lw=2)       # corte z=0: y = -x
    ax.set_xlabel("$x$"); ax.set_ylabel("$y$"); ax.set_zlabel("$z$")
    ax.view_init(elev=24, azim=-118)
    ax.set_title("Silla de montar $z=x^2-y^2$ (Práctico 6, ej. 1b)\n"
                 "sube por el eje $x$ y baja por el eje $y$", fontsize=11.5)
    guardar(fig, "b7_silla")


# 4. Dominios: disco agujereado y sectores
def dominio():
    fig, pad = plt.subplots(1, 2, figsize=(10, 4.4))

    ax = pad[0]
    ax.set_aspect("equal")
    circ = Circle((0, 0), 1, fc="tab:blue", alpha=0.18, ec="tab:blue", lw=2)
    ax.add_patch(circ)
    ax.plot(*zip(*[(np.cos(t), np.sin(t)) for t in np.linspace(0, 2 * np.pi, 300)]),
            color="tab:blue", lw=1.5)
    ax.scatter([0], [0], s=70, fc="white", ec="k", zorder=5)
    ax.annotate("no definida", (0.06, -0.02), fontsize=9.5)
    ax.annotate("$x^2+y^2=1$", (0.72, 0.72), fontsize=10, color="tab:blue")
    ax.set_xlim(-1.35, 1.35); ax.set_ylim(-1.35, 1.35)
    ax.set_title(r"$\log\!\left(\dfrac{1-x^2-y^2}{x^2+y^2}\right)$:" + "\n"
                 "disco unidad menos el origen ($0<r<1$)", fontsize=10.5)

    ax = pad[1]
    ax.set_aspect("equal")
    ax.add_patch(Wedge((0, 0), 2.2, 45, 90, fc="tab:green", alpha=0.20, ec="tab:green", lw=2))
    ax.add_patch(Wedge((0, 0), 2.2, 225, 270, fc="tab:green", alpha=0.20, ec="tab:green", lw=2))
    ax.plot([0, 1.9], [0, 1.9], "--", color="tab:green", lw=1.4)
    ax.plot([0, -1.9], [0, -1.9], "--", color="tab:green", lw=1.4)
    ax.annotate("$y=x$", (1.35, 1.15), fontsize=10, rotation=45, color="tab:green")
    ax.annotate("$0\\leq x\\leq y$", (0.15, 1.7), fontsize=10)
    ax.annotate("$y\\leq x\\leq 0$", (-0.35, -1.7), fontsize=10)
    ax.set_xlim(-2.4, 2.4); ax.set_ylim(-2.4, 2.4)
    ax.set_title(r"$\mathrm{arc}\cos\!\sqrt{x/y}$:" + "\n"
                 "sector entre $y=x$ y el eje $y$ (y su simétrico)", fontsize=10.5)
    fig.suptitle("Dominios: leer restricción por restricción y cruzar las condiciones",
                 fontsize=12, y=1.03)
    guardar(fig, "b7_dominio")


# 5. Limites direccionales: xy/(x^2+y^2)
def direccionales():
    fig, pad = plt.subplots(1, 2, figsize=(10, 4.3))

    ax = pad[0]
    m = np.linspace(-3, 3, 500)
    ax.plot(m, m / (1 + m ** 2), color="tab:orange", lw=2.2)
    for mm, col in [(0, "k"), (1, "tab:blue"), (-1, "tab:red"), (0.5, "tab:green")]:
        ax.scatter([mm], [mm / (1 + mm ** 2)], s=45, color=col, zorder=5)
        ax.annotate(f"$m={mm}$: {mm / (1 + mm ** 2):+.1f}".replace(".", ","),
                    (mm + 0.12, mm / (1 + mm ** 2) + (0.08 if mm >= 0 else -0.18)),
                    fontsize=9, color=col)
    ax.axhline(0, color="k", lw=0.8); ax.axvline(0, color="k", lw=0.8)
    ax.set_xlabel("pendiente $m$ de la recta $y=mx$")
    ax.set_ylabel(r"$\dfrac{m}{1+m^2}$")
    ax.set_ylim(-0.75, 0.75)
    ax.set_title("Límite por la recta $y=mx$: depende de $m$\n"
                 "$\\lim_{x\\to0}f(x,mx)=\\dfrac{m}{1+m^2}$", fontsize=10.5)

    ax = pad[1]
    ax.set_aspect("equal")
    for mm in [-2, -1, -0.5, 0.5, 1, 2]:
        v = mm / (1 + mm ** 2)
        col = "tab:red" if v < 0 else "tab:blue"
        xs = np.array([-1.6, 1.6])
        ax.plot(xs, mm * xs, color=col, lw=2, alpha=0.45 + 0.5 * abs(v))
    ax.annotate("", xy=(1.6, 1.6), xytext=(0, 0),
                arrowprops=dict(arrowstyle="->", lw=2, color="tab:blue"))
    ax.annotate("", xy=(-1.6, 1.6), xytext=(0, 0),
                arrowprops=dict(arrowstyle="->", lw=2, color="tab:red"))
    ax.annotate("valor $>0$", (0.75, 1.0), fontsize=9, color="tab:blue", rotation=45)
    ax.annotate("valor $<0$", (-1.35, 1.05), fontsize=9, color="tab:red", rotation=-45)
    ax.set_xlim(-1.8, 1.8); ax.set_ylim(-1.8, 1.8)
    ax.set_title("$f(x,y)=\\dfrac{xy}{x^2+y^2}$ cerca del origen:\n"
                 "cada recta da un valor distinto $\\Rightarrow$ no tiene límite", fontsize=10.5)
    guardar(fig, "b7_direccionales")


# 6. Caminos en el plano: parabola vs rectas (polares)
def polares():
    fig, pad = plt.subplots(1, 2, figsize=(10, 4.3))

    ax = pad[0]
    x = np.linspace(-1.6, 1.6, 600)
    y = np.linspace(-0.3, 1.7, 400)
    X, Y = np.meshgrid(x, y)
    F = X * Y ** 2 / (X ** 2 + Y ** 4)
    F[X ** 2 + Y ** 4 < 1e-9] = np.nan
    cs = ax.contourf(X, Y, F, levels=np.linspace(-0.5, 0.5, 11), cmap="RdBu_r", alpha=0.85)
    fig.colorbar(cs, ax=ax, shrink=0.85)
    for mm in [0.5, 1.0]:
        ax.plot(x, mm * x, "--", color="k", lw=1.4)
    ax.annotate("rectas $y=mx$: $f=0$", (-1.5, 1.35), fontsize=9.5)
    ax.plot(x, x ** 2, color="tab:orange", lw=2.6)
    ax.annotate("parábola $y=x^2$: $f=\\frac{1}{2}$", (0.55, 1.35), fontsize=9.5, color="tab:orange")
    ax.set_xlabel("$x$"); ax.set_ylabel("$y$")
    ax.set_title(r"$f(x,y)=\dfrac{xy^2}{x^2+y^4}$ (Práctico 6, ej. 4c y notas, Ejemplo 6.12):" + "\n"
                 "todas las direcciones dan 0, la parábola da 1/2", fontsize=10.2)

    ax = pad[1]
    ax.set_aspect("equal")
    xx = np.linspace(0, 1.6, 300)
    ax.fill_between(xx, 0, xx ** 2, color="tab:purple", alpha=0.25)
    ax.plot(xx, xx ** 2, color="tab:purple", lw=2)
    ax.plot([0, 0], [0, 1.6], color="tab:purple", lw=2)
    ax.annotate("acá $f=1$", (0.75, 0.18), fontsize=10, color="tab:purple")
    ax.annotate("$0<y<x^2$", (1.05, 0.30), fontsize=10)
    ax.annotate("acá $f=0$", (1.2, 1.1), fontsize=10, color="dimgray")
    ax.annotate("", xy=(0.35, 0.12), xytext=(0.9, 0.05),
                arrowprops=dict(arrowstyle="->", lw=2, color="k"))
    ax.annotate("", xy=(0.02, 0.55), xytext=(0.45, 0.55),
                arrowprops=dict(arrowstyle="->", lw=2, color="k"))
    ax.set_xlim(-0.05, 1.6); ax.set_ylim(-0.05, 1.6)
    ax.set_title("$f=1$ si $0<y<x^2$, $f=0$ en otro caso:\n"
                 "por polares da 0 en todo $\\theta$, pero por dentro de la\n"
                 "región (p. ej. $y=x^2/2$) vale 1: recíproco falso", fontsize=9.6)
    guardar(fig, "b7_polares")


# 7. Bola reducida: epsilon-delta
def disco_agujereado():
    fig, pad = plt.subplots(1, 2, figsize=(9.6, 4.0))

    ax = pad[0]
    ax.set_aspect("equal")
    ax.add_patch(Circle((0, 0), 1.0, fc="tab:blue", alpha=0.10, ec="tab:blue", lw=1.8,
                        ls="--"))
    ax.scatter([0], [0], s=90, fc="white", ec="k", zorder=5)
    ax.annotate("$a$", (0.07, -0.28), fontsize=12, fontweight="bold")
    ax.annotate("$B^*(a,\\delta)\\cap D$  (sin $a$)", (0.12, 0.85), fontsize=10, color="tab:blue")
    for px, py in [(0.55, 0.2), (-0.4, 0.6), (0.1, -0.75), (-0.7, -0.3), (0.8, -0.45)]:
        ax.scatter([px], [py], s=26, color="tab:blue", zorder=6)
    ax.set_xlim(-1.35, 1.35); ax.set_ylim(-1.35, 1.35)
    ax.set_title("DOMINIO: cerca de $a$, pero sin el punto", fontsize=10.5)
    ax.set_xlabel("$x\\in\\mathbb{R}^n$"); ax.grid(False)

    ax = pad[1]
    ax.add_patch(plt.Rectangle((-1.5, -0.45), 3.0, 0.9, fc="tab:green", alpha=0.18))
    ax.axhline(0, color="k", lw=1)
    ax.axhline(0.45, color="tab:green", lw=1.2, ls="--")
    ax.axhline(-0.45, color="tab:green", lw=1.2, ls="--")
    ax.scatter([0], [0], s=55, color="k", zorder=5)
    ax.annotate("$L$", (0.05, 0.08), fontsize=12)
    ax.annotate("$L+\\varepsilon$", (0.9, 0.52), fontsize=10, color="tab:green")
    ax.annotate("$L-\\varepsilon$", (0.9, -0.72), fontsize=10, color="tab:green")
    ax.set_xlim(-1.6, 1.6); ax.set_ylim(-1.0, 1.0)
    ax.set_title("IMAGEN: todos los valores caen en $(L-\\varepsilon,\\,L+\\varepsilon)$",
                 fontsize=10.5)
    ax.set_xlabel("$f(x)\\in\\mathbb{R}$"); ax.grid(False)
    fig.suptitle("Definición 6.4 de las notas: $\\lim_{x\\to a}f(x)=L$ "
                 "$\\Leftrightarrow$ $\\forall\\varepsilon>0\\;\\exists\\delta>0$ tal que "
                 "$f(B^*(a,\\delta)\\cap D)\\subset B(L,\\varepsilon)$",
                 fontsize=11.5, y=1.04)
    guardar(fig, "b7_disco_agujereado")


# 8. Weierstrass en un compacto
def weierstrass():
    from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
    r = np.linspace(0, 2.5, 160)
    th = np.linspace(0, 2 * np.pi, 160)
    R, T = np.meshgrid(r, th)
    X, Y = R * np.cos(T), R * np.sin(T)
    Z = np.sin(X) * np.exp(-(X ** 2 + Y ** 2) / 8) + 0.6 * np.cos(Y) * np.exp(-(X ** 2 + Y ** 2) / 12)
    mask = R > 2.5
    Z = np.where(mask, np.nan, Z)
    imax = np.nanargmax(Z); imin = np.nanargmin(Z)
    xm, ym, zm = X.flat[imax], Y.flat[imax], Z.flat[imax]
    xM, yM, zM = X.flat[imin], Y.flat[imin], Z.flat[imin]
    fig = plt.figure(figsize=(8, 5.4))
    ax = fig.add_subplot(111, projection="3d")
    ax.plot_surface(X, Y, Z, cmap="viridis", alpha=0.92, linewidth=0, antialiased=True)
    ax.scatter([xm], [ym], [zm], color="red", s=70, zorder=6)
    ax.scatter([xM], [yM], [zM], color="yellow", ec="k", s=70, zorder=6)
    ax.text(xm, ym, zm + 0.25, "mín $f(x_m)$", color="red", fontsize=10, fontweight="bold")
    ax.text(xM, yM, zM + 0.3, "máx $f(x_M)$", color="k", fontsize=10, fontweight="bold")
    thc = np.linspace(0, 2 * np.pi, 200)
    ax.plot(2.5 * np.cos(thc), 2.5 * np.sin(thc), np.zeros_like(thc), "k--", lw=1.6)
    ax.set_xlabel("$x$"); ax.set_ylabel("$y$"); ax.set_zlabel("$z$")
    ax.view_init(elev=26, azim=-135)
    ax.set_title("Weierstrass (Teorema 6.20): $f$ continua en el disco cerrado $C$\n"
                 "$\\Rightarrow$ existe $x_m, x_M\\in C$ con $f(x_m)\\leq f(x)\\leq f(x_M)$",
                 fontsize=11)
    guardar(fig, "b7_weierstrass")


# 9. Preimagen de abierto: caracterizacion topologica
def preimagen():
    fig, pad = plt.subplots(1, 2, figsize=(9.6, 4.0))

    ax = pad[0]
    ax.set_aspect("equal"); ax.grid(False)
    ax.add_patch(plt.Rectangle((-2, -1.5), 4, 3, fc="none", ec="gray", lw=1.2))
    e1 = plt.Circle((-0.5, 0.15), 1.15, fc="tab:blue", alpha=0.18, ec="tab:blue", lw=2, ls="--")
    e2 = plt.Circle((0.9, -0.6), 0.85, fc="tab:blue", alpha=0.18, ec="tab:blue", lw=2, ls="--")
    ax.add_patch(e1); ax.add_patch(e2)
    ax.annotate("$f^{-1}(A)$: abierto", (-1.6, 1.35), fontsize=10.5, color="tab:blue")
    ax.set_xlim(-2.1, 2.1); ax.set_ylim(-1.6, 1.6)
    ax.set_title("DOMINIO $\\mathbb{R}^n$", fontsize=10.5)

    ax = pad[1]
    ax.set_aspect("equal"); ax.grid(False)
    ax.annotate("", xy=(1.7, 0), xytext=(-1.7, 0),
                arrowprops=dict(arrowstyle="->", lw=1.2, color="gray"))
    ax.text(0, 0.25, "$f$", fontsize=12, ha="center")
    ax.annotate("$A$: abierto", (-1.9, 1.25), fontsize=10.5, color="tab:green")
    ax.add_patch(plt.Rectangle((-1.4, -0.7), 2.9, 1.4, fc="tab:green", alpha=0.18,
                               ec="tab:green", lw=2, ls="--"))
    ax.set_xlim(-2.1, 2.1); ax.set_ylim(-1.6, 1.6)
    ax.set_title("CODOMINIO $\\mathbb{R}$", fontsize=10.5)
    fig.suptitle("Teorema: $f$ continua $\\Leftrightarrow$ $f^{-1}(A)$ es abierto para todo abierto $A$\n"
                 "(Práctico 6, ej. 15a; análogo con cerrados y $f^{-1}(C)$ cerrado)",
                 fontsize=11.5, y=1.05)
    guardar(fig, "b7_preimagen")


if __name__ == "__main__":
    mapa()
    nivel_cuadrados()
    silla()
    dominio()
    direccionales()
    polares()
    disco_agujereado()
    weierstrass()
    preimagen()
    print("BLOQUE 7 LISTO:", len([f for f in os.listdir(OUT) if f.startswith("b7_")]), "figuras")
