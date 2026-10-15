# -*- coding: utf-8 -*-
"""Figuras del Bloque 8 — Diferenciabilidad (clases 37-41).
Genera: b8_plano_tangente, b8_corte_parcial, b8_gradiente_nivel,
        b8_campo_gradiente, b8_cadena, b8_jacobiano,
        b8_formas_cuadraticas, b8_mapa  (PNG en curso/img/)."""
import os
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

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


# 1. Plano tangente a una superficie
def plano_tangente():
    fig = plt.figure(figsize=(7, 5.4))
    ax = fig.add_subplot(111, projection="3d")
    x = np.linspace(-1.6, 2.6, 40)
    y = np.linspace(-1.6, 2.6, 40)
    X, Y = np.meshgrid(x, y)
    Z = X ** 2 + Y ** 2
    ax.plot_surface(X, Y, Z, cmap="viridis", alpha=0.85, linewidth=0,
                    antialiased=True, rstride=1, cstride=1)
    xt = np.linspace(0.0, 2.2, 2)
    yt = np.linspace(0.0, 2.2, 2)
    XT, YT = np.meshgrid(xt, yt)
    ZT = 2 + 2 * (XT - 1) + 2 * (YT - 1)   # plano tangente en (1,1)
    ax.plot_surface(XT, YT, ZT, color="tab:orange", alpha=0.5)
    ax.scatter([1], [1], [2], color="red", s=55, zorder=5)
    ax.text(1, 1, 2.4, r"$(1,1,2)$", color="red", fontsize=11)
    ax.set_xlabel(r"$x$"); ax.set_ylabel(r"$y$"); ax.set_zlabel(r"$z$")
    ax.set_title("Plano tangente: $z=f(x_0,y_0)+f_x(x_0,y_0)(x-x_0)$\n"
                 "$+\\,f_y(x_0,y_0)(y-y_0)$   para $f(x,y)=x^2+y^2$",
                 fontsize=12)
    ax.view_init(elev=24, azim=-58)
    ax.set_xlim(-1.6, 2.6); ax.set_ylim(-1.6, 2.6); ax.set_zlim(0, 13)
    guardar(fig, "b8_plano_tangente")


# 2. Corte parcial: la derivada parcial es una pendiente
def corte_parcial():
    fig = plt.figure(figsize=(11, 4.6))
    x = np.linspace(-2, 2, 50)
    y = np.linspace(-2, 2, 50)
    X, Y = np.meshgrid(x, y)
    Z = X ** 2 + Y ** 2

    ax = fig.add_subplot(121, projection="3d")
    ax.plot_surface(X, Y, Z, cmap="viridis", alpha=0.55, linewidth=0)
    y0 = 1.0
    ax.plot([-2, 2], [y0, y0], [0, 0], color="k", lw=1.5)  # base del corte
    xc = np.linspace(-2, 2, 100)
    ax.plot(xc, y0 * np.ones_like(xc), xc ** 2 + y0 ** 2,
            color="red", lw=2.6, label=r"$f(x,y_0)=x^2+1$")
    # recta tangente en x=1 dentro del plano del corte
    xt = np.linspace(0.2, 1.8, 2)
    ax.plot(xt, y0 * np.ones_like(xt), (1 + y0 ** 2) + 2 * (xt - 1),
            "k--", lw=2, label=r"pendiente $f_x=2$")
    ax.scatter([1], [y0], [1 + y0 ** 2], color="red", s=45, zorder=5)
    ax.set_xlabel(r"$x$"); ax.set_ylabel(r"$y$"); ax.set_zlabel(r"$z$")
    ax.set_title("Corte por $y=y_0$: la parcial $f_x$ es la pendiente\n"
                 "de la curva de intersección", fontsize=11)
    ax.legend(fontsize=8, loc="upper left")
    ax.view_init(elev=22, azim=-60)

    ax2 = fig.add_subplot(122)
    xx = np.linspace(-2, 2, 200)
    ax2.plot(xx, xx ** 2 + 1, lw=2.4, label=r"$g(x)=f(x,y_0)=x^2+1$")
    ax2.plot(xx, (1 + 1) + 2 * (xx - 1), "k--", lw=1.8,
             label=r"tangente en $x_0=1$")
    ax2.scatter([1], [2], color="red", zorder=5)
    ax2.annotate(r"$g'(1)=f_x(1,y_0)=2$", xy=(1, 2), xytext=(0.1, 4.2),
                 arrowprops=dict(arrowstyle="->", color="gray"), fontsize=10)
    ax2.set_xlabel(r"$x$"); ax2.set_ylabel(r"$g(x)$")
    ax2.set_title("En una variable: derivar la función de un corte", fontsize=11)
    ax2.legend(fontsize=9, loc="upper center")
    fig.suptitle("La derivada parcial mira UNA dirección: el corte vertical",
                 fontsize=13, y=1.02)
    guardar(fig, "b8_corte_parcial")


# 3. Gradiente perpendicular a las curvas de nivel
def gradiente_nivel():
    fig, ax = plt.subplots(figsize=(6.8, 5.6))
    x = np.linspace(-2.6, 2.6, 300)
    y = np.linspace(-2.6, 2.6, 300)
    X, Y = np.meshgrid(x, y)
    Z = X ** 2 + 2 * Y ** 2
    cs = ax.contour(X, Y, Z, levels=[0.5, 1, 2, 3.5, 5.5, 8],
                    cmap="Blues_r")
    ax.clabel(cs, inline=True, fontsize=8)
    pts = [(1.0, 0.5), (-1.0, 0.5), (0.6, -0.9), (-0.8, -0.6), (1.4, 0.3)]
    for px, py in pts:
        gx, gy = 2 * px, 4 * py
        n = np.hypot(gx, gy)
        # tangente a la curva de nivel (perpendicular al gradiente)
        tx, ty = -gy / n, gx / n
        ax.arrow(px, py, gx, gy, head_width=0.07, color="tab:red",
                 length_includes_head=True, lw=1.8, zorder=5)
        ax.plot([px - 0.28 * tx, px + 0.28 * tx],
                [py - 0.28 * ty, py + 0.28 * ty],
                color="tab:green", lw=2, zorder=4)
    ax.plot([], [], color="tab:red", lw=1.8, label=r"$\nabla f$")
    ax.plot([], [], color="tab:green", lw=2, label="tangente a $f=k$")
    ax.set_xlabel(r"$x$"); ax.set_ylabel(r"$y$")
    ax.set_title(r"$\nabla f$ es perpendicular a las curvas de nivel $f=k$"
                 "\n" r"(aquí $f(x,y)=x^2+2y^2$)", fontsize=12)
    ax.legend(fontsize=9, loc="upper right")
    ax.set_aspect("equal")
    guardar(fig, "b8_gradiente_nivel")


# 4. Campo gradiente
def campo_gradiente():
    fig, pad = plt.subplots(1, 2, figsize=(11, 4.8))
    for ax, (fx, fy, titulo, cmap) in zip(
        pad,
        [(lambda x, y: 2 * x, lambda x, y: 2 * y,
          r"$f=x^2+y^2$: todo apunta afuera", "viridis"),
         (lambda x, y: 2 * x, lambda x, y: -2 * y,
          r"$f=x^2-y^2$: sale por un lado, entra por otro", "coolwarm")]):
        x = np.linspace(-2, 2, 17)
        y = np.linspace(-2, 2, 17)
        X, Y = np.meshgrid(x, y)
        U, V = fx(X, Y), fy(X, Y)
        N = np.hypot(U, V); N[N == 0] = 1
        ax.quiver(X, Y, U / N, V / N, np.hypot(U, V), cmap=cmap,
                  pivot="mid", scale=22, width=0.004)
        xs = np.linspace(-2.2, 2.2, 250)
        ys = np.linspace(-2.2, 2.2, 250)
        XS, YS = np.meshgrid(xs, ys)
        F = XS ** 2 + YS ** 2 if cmap == "viridis" else XS ** 2 - YS ** 2
        ax.contour(XS, YS, F, levels=6, colors="gray",
                   linewidths=0.7, alpha=0.6)
        ax.set_title(titulo, fontsize=11)
        ax.set_xlabel(r"$x$"); ax.set_ylabel(r"$y$")
        ax.set_aspect("equal")
    fig.suptitle("Campo gradiente $\\nabla f$: en cada punto, la dirección "
                 "de máximo crecimiento", fontsize=13, y=1.02)
    guardar(fig, "b8_campo_gradiente")


# 5. Regla de la cadena como composición
def cadena():
    fig, ax = plt.subplots(figsize=(9.4, 4.2))
    ax.axis("off")

    def caja(x, y, t, c, w=0.20, h=0.16):
        ax.add_patch(plt.Rectangle((x - w / 2, y - h / 2), w, h, fc=c,
                                   alpha=0.16, ec=c, lw=2, zorder=2))
        ax.text(x, y, t, ha="center", va="center", fontsize=9, zorder=3)

    caja(0.10, 0.62, "$t\\in\\mathbb{R}^k$", "tab:blue", 0.16, 0.14)
    caja(0.38, 0.62, "$g$", "tab:green", 0.10, 0.14)
    caja(0.62, 0.62, "$g(t)\\in\\mathbb{R}^n$", "tab:green", 0.20, 0.14)
    caja(0.88, 0.62, "$f$", "tab:red", 0.10, 0.14)
    caja(0.62, 0.24, "$f(g(t))\\in\\mathbb{R}^m$", "tab:purple", 0.26, 0.14)

    ax.annotate("", xy=(0.30, 0.62), xytext=(0.18, 0.62),
                arrowprops=dict(arrowstyle="->", lw=1.6, color="gray"))
    ax.annotate("", xy=(0.52, 0.62), xytext=(0.46, 0.62),
                arrowprops=dict(arrowstyle="->", lw=1.6, color="gray"))
    ax.annotate("", xy=(0.80, 0.62), xytext=(0.72, 0.62),
                arrowprops=dict(arrowstyle="->", lw=1.6, color="gray"))
    ax.annotate("", xy=(0.62, 0.33), xytext=(0.62, 0.53),
                arrowprops=dict(arrowstyle="->", lw=1.6, color="tab:purple"))

    ax.text(0.5, 0.90, "Regla de la cadena (composición de flechas)",
            ha="center", fontsize=13)
    ax.text(0.5, 0.06,
            r"$J_{f\circ g}(a)=J_f(g(a))\cdot J_g(a)$"
            "     (¡el orden importa!)",
            ha="center", fontsize=12,
            bbox=dict(boxstyle="round", fc="lightyellow", ec="gray"))
    ax.text(0.38, 0.70, "deriva $g$", ha="center", fontsize=8.5, color="gray")
    ax.text(0.88, 0.70, "deriva $f$", ha="center", fontsize=8.5, color="gray")
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    guardar(fig, "b8_cadena")


# 6. Matriz Jacobiana: cómo deforma el diferencial
def jacobiano():
    fig, pad = plt.subplots(1, 2, figsize=(10.4, 4.6))
    u = np.linspace(-1.5, 1.5, 20)
    v = np.linspace(-1.5, 1.5, 20)
    U, V = np.meshgrid(u, v)

    ax = pad[0]
    # transformación g(u,v) = (u+v, v - u)  con J = [[1,1],[-1,1]], det=2
    X, Y = U + V, V - U
    ax.plot(U[0, :], V[0, :], color="gray", lw=0.6)
    ax.plot(U[:, 0], V[:, 0], color="gray", lw=0.6)
    sq_u = np.array([0, 1, 1, 0, 0]); sq_v = np.array([0, 0, 1, 1, 0])
    ax.fill(sq_u, sq_v, color="tab:blue", alpha=0.35, ec="tab:blue", lw=2)
    ax.set_title("Dominio: cuadrado unitario", fontsize=11)
    ax.set_xlabel(r"$u$"); ax.set_ylabel(r"$v$"); ax.set_aspect("equal")

    ax = pad[1]
    ax.plot(X[0, :], Y[0, :], color="gray", lw=0.6)
    ax.plot(X[:, 0], Y[:, 0], color="gray", lw=0.6)
    sq_x = sq_u + sq_v; sq_y = sq_v - sq_u
    ax.fill(sq_x, sq_y, color="tab:red", alpha=0.35, ec="tab:red", lw=2)
    ax.set_title(r"Imagen: paralelogramo de área $|\det J_g|=2$", fontsize=11)
    ax.set_xlabel(r"$x$"); ax.set_ylabel(r"$y$"); ax.set_aspect("equal")
    fig.suptitle("La Jacobiana es la mejor aproximación lineal: manda "
                 "cuadraditos en paralelogramos", fontsize=12.5, y=1.03)
    guardar(fig, "b8_jacobiano")


# 7. Formas cuadráticas: definida / indefinida / semidefinida
def formas_cuadraticas():
    fig = plt.figure(figsize=(12, 4.3))
    x = np.linspace(-1.8, 1.8, 60)
    y = np.linspace(-1.8, 1.8, 60)
    X, Y = np.meshgrid(x, y)
    casos = [
        (X ** 2 + Y ** 2, r"$x^2+y^2$: definida positiva", "viridis"),
        (X ** 2 - Y ** 2, r"$x^2-y^2$: indefinida (silla)", "coolwarm"),
        (X ** 2, r"$x^2$: semidefinida (plana en $y$)", "plasma"),
    ]
    for k, (Z, titulo, cmap) in enumerate(casos, start=1):
        ax = fig.add_subplot(1, 3, k, projection="3d")
        ax.plot_surface(X, Y, Z, cmap=cmap, alpha=0.9, linewidth=0,
                        antialiased=True)
        ax.set_title(titulo, fontsize=10.5)
        ax.set_xlabel(r"$x$"); ax.set_ylabel(r"$y$"); ax.set_zlabel(r"$q$")
        ax.view_init(elev=26, azim=-58)
    fig.suptitle("Formas cuadráticas $q(v)=vHv^{\\!\\top}$: el signo de los "
                 "autovalores decide el paisaje", fontsize=13, y=1.05)
    guardar(fig, "b8_formas_cuadraticas")


# 8. Mapa del bloque
def mapa():
    fig, ax = plt.subplots(figsize=(8.8, 5.8))
    ax.axis("off")
    cajas = [
        (0.50, 0.93, "DIFERENCIABILIDAD\n(continuidad + aproximación lineal)",
         "tab:blue"),
        (0.17, 0.71, "DERIVADAS PARCIALES\ny DIRECCIONALES\n$\\partial f/\\partial x$,"
         " $\\partial f/\\partial v$, gradiente", "tab:green"),
        (0.50, 0.71, "PLANO TANGENTE\n$z=f(a)+\\nabla f(a)\\cdot(x-a)$\n"
         "condición suficiente: $C^1$", "tab:orange"),
        (0.83, 0.71, "REGLA DE LA CADENA\nmatriz Jacobiana\n$J_{f\\circ g}=J_f\\,J_g$",
         "tab:red"),
        (0.50, 0.47, "DEFINICIÓN CLAVE: $f(a+h)=f(a)+df_a(h)+r(h)$, "
         "$r(h)/\\|h\\|\\to0$", "tab:purple"),
        (0.17, 0.25, "ORDEN SUPERIOR\nClairaut: $f_{xy}=f_{yx}$\nmatriz Hessiana $H$",
         "tab:olive"),
        (0.50, 0.25, "TAYLOR DE ORDEN 2\n$q(v)=vHv^{\\!\\top}$\nformas cuadráticas",
         "steelblue"),
        (0.83, 0.25, "PARCIAL 2\nplano tangente,\ngradiente, Jacobiana", "firebrick"),
        (0.50, 0.05, "TODO SE APOYA EN: continuidad (cl. 36)  ·  límites y "
         "curvas de nivel (cl. 34-35)", "dimgray"),
    ]
    for x, y, t, c in cajas:
        ax.add_patch(plt.Rectangle((x - 0.155, y - 0.078), 0.31, 0.156,
                                   fc=c, alpha=0.16, ec=c, lw=2, zorder=2))
        ax.text(x, y, t, ha="center", va="center", fontsize=8.2, zorder=3)
    flechas = [((0.5, 0.85), (0.17, 0.79)), ((0.5, 0.85), (0.5, 0.79)),
               ((0.5, 0.85), (0.83, 0.79)),
               ((0.17, 0.63), (0.4, 0.55)), ((0.5, 0.63), (0.5, 0.55)),
               ((0.83, 0.63), (0.6, 0.55)),
               ((0.35, 0.47), (0.24, 0.33)), ((0.5, 0.40), (0.5, 0.33)),
               ((0.65, 0.47), (0.76, 0.33)),
               ((0.17, 0.17), (0.36, 0.13)), ((0.5, 0.17), (0.5, 0.13)),
               ((0.83, 0.17), (0.64, 0.13))]
    for a, b in flechas:
        ax.annotate("", xy=b, xytext=a,
                    arrowprops=dict(arrowstyle="->", lw=1.4, color="gray"))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.set_title("Mapa del Bloque 8 — Diferenciabilidad (clases 37 a 41)",
                 fontsize=13)
    guardar(fig, "b8_mapa")


if __name__ == "__main__":
    plano_tangente()
    corte_parcial()
    gradiente_nivel()
    campo_gradiente()
    cadena()
    jacobiano()
    formas_cuadraticas()
    mapa()
    n = len([f for f in os.listdir(OUT) if f.startswith("b8_")])
    print("BLOQUE 8 LISTO:", n, "figuras")
