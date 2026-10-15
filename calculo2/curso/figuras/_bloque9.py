# -*- coding: utf-8 -*-
"""Figuras del Bloque 9 — Extremos e implícitas (clases 42-44).
Genera: b9_hessiana, b9_curvas_nivel, b9_absoluto_compacto, b9_convexa,
        b9_implicita, b9_superficie, b9_lagrange, b9_mapa  (PNG en curso/img/)."""
import os
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401  (habilita proyeccion 3d)

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


# 1. Clasificación por la Hessiana: mínimo, máximo y silla
def hessiana():
    x = np.linspace(-1.5, 1.5, 80)
    X, Y = np.meshgrid(x, x)
    casos = [
        (X ** 2 + Y ** 2, r"MINIMO: $\lambda_1,\lambda_2>0$", "tab:green"),
        (-X ** 2 - Y ** 2, r"MAXIMO: $\lambda_1,\lambda_2<0$", "tab:red"),
        (X ** 2 - Y ** 2, r"SILLA: $\lambda_1\lambda_2<0$", "tab:orange"),
    ]
    fig = plt.figure(figsize=(11.5, 3.9))
    for k, (Z, tit, col) in enumerate(casos):
        ax = fig.add_subplot(1, 3, k + 1, projection="3d")
        ax.plot_surface(X, Y, Z, cmap="viridis", alpha=0.85, linewidth=0)
        ax.scatter([0], [0], [0], color=col, s=55, zorder=6)
        ax.set_title(tit, fontsize=10.5)
        ax.set_xlabel(r"$x$"); ax.set_ylabel(r"$y$")
        ax.view_init(elev=22, azim=-60)
        ax.set_zlim(-3, 3)
    fig.suptitle("Criterio de la Hessiana en un punto critico: "
                 "det(H) y tr(H) deciden", fontsize=12.5, y=1.03)
    guardar(fig, "b9_hessiana")


# 2. Curvas de nivel y gradiente (que se anula en el crítico)
def curvas_nivel():
    x = np.linspace(-2, 2, 300)
    X, Y = np.meshgrid(x, x)
    fig, pad = plt.subplots(1, 2, figsize=(10.5, 4.5))

    ax = pad[0]
    Z = X ** 2 + Y ** 2
    ax.contour(X, Y, Z, levels=10, cmap="viridis")
    ax.quiver(X[::25, ::25], Y[::25, ::25], 2 * X[::25, ::25], 2 * Y[::25, ::25],
              color="gray", alpha=0.7, width=0.004)
    ax.plot(0, 0, "o", color="tab:green", ms=9)
    ax.set_title(r"$f=x^2+y^2$: $\nabla f=0$ en el minimo", fontsize=10.5)
    ax.set_xlabel(r"$x$"); ax.set_ylabel(r"$y$"); ax.set_aspect("equal")

    ax = pad[1]
    Z = X ** 2 - Y ** 2
    ax.contour(X, Y, Z, levels=12, cmap="coolwarm")
    ax.quiver(X[::25, ::25], Y[::25, ::25], 2 * X[::25, ::25], -2 * Y[::25, ::25],
              color="gray", alpha=0.7, width=0.004)
    ax.plot(0, 0, "o", color="tab:red", ms=9)
    ax.set_title(r"$f=x^2-y^2$: $\nabla f=0$ en la silla", fontsize=10.5)
    ax.set_xlabel(r"$x$"); ax.set_ylabel(r"$y$"); ax.set_aspect("equal")

    fig.suptitle("El gradiente es perpendicular a las curvas de nivel "
                 "y se anula en el punto critico", fontsize=12, y=1.02)
    guardar(fig, "b9_curvas_nivel")


# 3. Extremos absolutos sobre un compacto
def absoluto_compacto():
    r = np.linspace(0, 1, 60)
    t = np.linspace(0, 2 * np.pi, 120)
    R, T = np.meshgrid(r, t)
    X = R * np.cos(T); Y = R * np.sin(T)
    fig = plt.figure(figsize=(11, 4.2))

    ax = fig.add_subplot(1, 2, 1, projection="3d")
    Z = X ** 2 + Y ** 2
    ax.plot_surface(X, Y, Z, cmap="viridis", alpha=0.9, linewidth=0)
    ax.plot(np.cos(t), np.sin(t), np.ones_like(t), color="tab:red", lw=3,
            label="borde: maximo $=1$")
    ax.scatter([0], [0], [0], color="tab:green", s=60, label="centro: minimo $=0$")
    ax.set_title(r"$f=x^2+y^2$ en el disco cerrado", fontsize=10.5)
    ax.view_init(elev=25, azim=-60); ax.legend(fontsize=8)

    ax = fig.add_subplot(1, 2, 2, projection="3d")
    Z = X ** 2 - Y ** 2
    ax.plot_surface(X, Y, Z, cmap="coolwarm", alpha=0.9, linewidth=0)
    ax.plot(np.cos(t), np.sin(t), np.cos(2 * t), color="k", lw=2.5,
            label="borde: $\\cos 2\\theta\\in[-1,1]$")
    ax.scatter([0], [0], [0], color="tab:red", s=60, label="centro: silla")
    ax.set_title(r"$f=x^2-y^2$ en el disco cerrado", fontsize=10.5)
    ax.view_init(elev=25, azim=-60); ax.legend(fontsize=8)

    fig.suptitle("Weierstrass: continua sobre compacto alcanza maximo y minimo "
                 "(interior o borde)", fontsize=12, y=1.03)
    guardar(fig, "b9_absoluto_compacto")


# 4. Función convexa vs no convexa (cuerda por encima/debajo)
def convexa():
    fig, pad = plt.subplots(1, 2, figsize=(10.5, 4.2))

    ax = pad[0]
    x = np.linspace(-1.8, 1.8, 300)
    g = x ** 2
    ax.plot(x, g, lw=2.5, color="tab:blue", label=r"$g(x)=x^2$ (convexa)")
    xs, xe = -1.4, 1.4
    ax.plot([xs, xe], [xs ** 2, xe ** 2], "--", color="tab:red", lw=2,
            label="cuerda: queda ARRIBA del grafico")
    ax.plot([xs, xe], [xs ** 2, xe ** 2], "o", color="tab:red", ms=6)
    ax.set_title(r"Convexa: $g(\lambda x+(1-\lambda)y)\leq\lambda g(x)+(1-\lambda)g(y)$",
                 fontsize=9.5)
    ax.set_xlabel(r"$x$"); ax.set_ylabel(r"$g$")
    ax.legend(fontsize=8.5, loc="upper center")

    ax = pad[1]
    h = x ** 4 - 2 * x ** 2 + 0.5
    ax.plot(x, h, lw=2.5, color="tab:purple", label=r"$h(x)=x^4-2x^2$ (no convexa)")
    xs, xe = -1.35, 1.35
    ax.plot([xs, xe], [xs ** 4 - 2 * xs ** 2 + 0.5, xe ** 4 - 2 * xe ** 2 + 0.5],
            "--", color="tab:orange", lw=2, label="cuerda: corta el grafico")
    ax.plot([xs, xe], [xs ** 4 - 2 * xs ** 2 + 0.5, xe ** 4 - 2 * xe ** 2 + 0.5],
            "o", color="tab:orange", ms=6)
    ax.set_title("No convexa: la cuerda queda por debajo en algun tramo",
                 fontsize=9.5)
    ax.set_xlabel(r"$x$"); ax.set_ylabel(r"$h$")
    ax.legend(fontsize=8.5, loc="upper center")

    fig.suptitle("Convexidad: cuerdas por encima del grafico  "
                 "$\\Leftrightarrow$  $f''\\geq0$ (o Hessiana semidefinida)",
                 fontsize=12, y=1.03)
    guardar(fig, "b9_convexa")


# 5. Función implícita: curva de nivel y recta tangente
def implicita():
    th = np.linspace(0, 2 * np.pi, 400)
    fig, ax = plt.subplots(figsize=(6.6, 5.6))
    ax.plot(np.cos(th), np.sin(th), lw=2.2, color="tab:blue",
            label=r"$F(x,y)=x^2+y^2-1=0$")
    x0, y0 = 0.6, 0.8
    xs = np.linspace(-0.6, 1.5, 50)
    ys = (1 - x0 * xs) / y0              # recta tangente x0*x + y0*y = 1
    ax.plot(xs, ys, "--", color="tab:red", lw=2, label="recta tangente")
    ax.plot(x0, y0, "o", color="tab:red", ms=8)
    ax.annotate(r"$(x_0,y_0)$", (x0, y0), textcoords="offset points",
                xytext=(8, 8), fontsize=10)
    ax.quiver(x0, y0, 2 * x0, 2 * y0, color="black", scale=6, width=0.006,
              label=r"$\nabla F=(F_x,F_y)$")
    ax.plot([x0, x0 + 0.25], [y0, y0 + 0.25 * (-x0 / y0)], color="tab:green", lw=2)
    ax.text(x0 + 0.32, y0 + 0.25 * (-x0 / y0), r"pendiente $y'(x)=-F_x/F_y$",
            fontsize=9.5, color="tab:green")
    ax.axhline(0, color="gray", lw=0.8); ax.axvline(0, color="gray", lw=0.8)
    ax.set_aspect("equal")
    ax.set_xlabel(r"$x$"); ax.set_ylabel(r"$y$")
    ax.set_title("Teorema de la funcion implicita: $F(x,y)=0$ cerca de $y=y(x)$",
                 fontsize=11.5)
    ax.legend(fontsize=8.5, loc="lower left")
    guardar(fig, "b9_implicita")


# 6. Superficie de nivel y plano tangente (F(x,y,z)=0)
def superficie():
    fig = plt.figure(figsize=(6.8, 5.6))
    ax = fig.add_subplot(111, projection="3d")
    u = np.linspace(0, 2 * np.pi, 60)
    v = np.linspace(0, np.pi, 40)
    r = np.sqrt(3.0)
    X = r * np.outer(np.cos(u), np.sin(v))
    Y = r * np.outer(np.sin(u), np.sin(v))
    Z = r * np.outer(np.ones_like(u), np.cos(v))
    ax.plot_surface(X, Y, Z, cmap="Blues", alpha=0.45, linewidth=0, edgecolor="none")
    xl = np.linspace(-0.6, 2.6, 20)
    Xp, Yp = np.meshgrid(xl, xl)
    Zp = 3 - Xp - Yp
    ax.plot_surface(Xp, Yp, Zp, cmap="autumn", alpha=0.5, linewidth=0)
    ax.scatter([1], [1], [1], color="black", s=55, zorder=6)
    ax.text(1.05, 1.05, 1.35, r"$P=(1,1,1)$", fontsize=9)
    ax.quiver(1, 1, 1, 2, 2, 2, color="black", length=2.2, lw=1.6)
    ax.text(2.4, 2.4, 3.0, r"$\nabla F$", fontsize=10)
    ax.set_xlabel(r"$x$"); ax.set_ylabel(r"$y$"); ax.set_zlabel(r"$z$")
    ax.view_init(elev=18, azim=-55)
    ax.set_title("Superficie de nivel $x^2+y^2+z^2=3$\n"
                 "y plano tangente $x+y+z=3$ en $(1,1,1)$", fontsize=11)
    guardar(fig, "b9_superficie")


# 7. Multiplicadores de Lagrange: nivel tangente a la restricción
def lagrange():
    fig, ax = plt.subplots(figsize=(6.8, 6.2))
    x = np.linspace(-2, 2, 400)
    X, Y = np.meshgrid(x, x)
    Z = X * Y
    cs = ax.contour(X, Y, Z, levels=np.arange(-2, 2.01, 0.25), cmap="viridis",
                    alpha=0.85)
    ax.clabel(cs, inline=True, fontsize=7)
    th = np.linspace(0, 2 * np.pi, 400)
    ax.plot(np.cos(th), np.sin(th), color="tab:red", lw=2.6,
            label=r"restriccion $g=x^2+y^2-1=0$")
    a = 1 / np.sqrt(2)
    for px, py, col in [(a, a, "tab:green"), (-a, -a, "tab:green"),
                        (a, -a, "tab:purple"), (-a, a, "tab:purple")]:
        ax.plot(px, py, "o", color=col, ms=9, zorder=6)
        # direccion unitaria hacia afuera del punto
        ux, uy = px, py
        n = np.hypot(ux, uy)
        ux, uy = ux / n, uy / n
        ax.annotate("", xy=(px + 0.30 * ux, py + 0.30 * uy), xytext=(px, py),
                    arrowprops=dict(arrowstyle="-|>", color="black", lw=1.8), zorder=8)
        ax.annotate("", xy=(px + 0.50 * ux, py + 0.50 * uy), xytext=(px, py),
                    arrowprops=dict(arrowstyle="-|>", color="tab:red", lw=1.8), zorder=7)
    ax.text(a + 0.05, a + 0.05, r"$\max=\frac{1}{2}$", fontsize=10, color="tab:green")
    ax.text(-a - 0.55, -a - 0.18, r"$\min=-\frac{1}{2}$", fontsize=10, color="tab:green")
    ax.set_aspect("equal")
    ax.set_xlabel(r"$x$"); ax.set_ylabel(r"$y$")
    ax.set_title("Lagrange: en el extremo, $\\nabla f=\\lambda\\nabla g$\n"
                 "las curvas de nivel de $f=xy$ son tangentes a $g=0$",
                 fontsize=11)
    ax.legend(fontsize=8.5, loc="upper right")
    guardar(fig, "b9_lagrange")


# 8. Mapa del bloque
def mapa():
    fig, ax = plt.subplots(figsize=(8.8, 5.8))
    ax.axis("off")
    cajas = [
        (0.50, 0.93, "BLOQUE 9\nExtremos e implicitas", "tab:blue"),
        (0.17, 0.70, "RELATIVOS (clase 42)\n$\\nabla f=0$ + Hessiana\nmin / max / silla",
         "tab:green"),
        (0.50, 0.70, "ABSOLUTOS (clase 43)\nWeierstrass: compacto\ninterior + borde; convexidad",
         "tab:orange"),
        (0.83, 0.70, "IMPLICITAS (clase 44)\n$F=0$, inversa,\nLagrange",
         "tab:red"),
        (0.50, 0.47, "HERRAMIENTA COMUN: Taylor de orden 2  ·  gradiente\n"
                     "$\\nabla f$ perpendicular a las curvas/superficies de nivel", "tab:purple"),
        (0.17, 0.24, "Criterio 2x2:\ndet(H)&gt;0, tr(H)&gt;0 $\\to$ min\ndet(H)&lt;0 $\\to$ silla",
         "tab:olive"),
        (0.50, 0.24, "Convexa: Hessiana semidefinida\n$\\to$ todo critico es global",
         "steelblue"),
        (0.83, 0.24, "$\\nabla f=\\lambda\\nabla g$\nnivel tangente a restriccion", "firebrick"),
        (0.50, 0.05, "Si el diferencial 2do no alcanza (det=0 o caso frontera): "
                     "estudiar aparte", "dimgray"),
    ]
    for x, y, t, c in cajas:
        ax.add_patch(plt.Rectangle((x - 0.15, y - 0.075), 0.30, 0.15, fc=c, alpha=0.16,
                                   ec=c, lw=2, zorder=2))
        ax.text(x, y, t, ha="center", va="center", fontsize=8.3, zorder=3)
    flechas = [((0.50, 0.855), (0.17, 0.775)), ((0.50, 0.855), (0.50, 0.775)),
               ((0.50, 0.855), (0.83, 0.775)), ((0.17, 0.625), (0.40, 0.545)),
               ((0.50, 0.625), (0.50, 0.545)), ((0.83, 0.625), (0.60, 0.545)),
               ((0.34, 0.47), (0.24, 0.315)), ((0.50, 0.395), (0.50, 0.315)),
               ((0.66, 0.47), (0.76, 0.315)),
               ((0.17, 0.165), (0.36, 0.125)), ((0.50, 0.165), (0.50, 0.125)),
               ((0.83, 0.165), (0.64, 0.125))]
    for a, b in flechas:
        ax.annotate("", xy=b, xytext=a, arrowprops=dict(arrowstyle="->", lw=1.4, color="gray"))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.set_title("Mapa del Bloque 9 — Extremos e implicitas (clases 42 a 44)", fontsize=13)
    guardar(fig, "b9_mapa")


if __name__ == "__main__":
    hessiana()
    curvas_nivel()
    absoluto_compacto()
    convexa()
    implicita()
    superficie()
    lagrange()
    mapa()
    print("BLOQUE 9 LISTO:", len([f for f in os.listdir(OUT) if f.startswith("b9_")]),
          "figuras")
