# -*- coding: utf-8 -*-
"""Figuras del Bloque 0 (clases 1-4) del curso de Calculo en Varias Variables."""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "img")
os.makedirs(OUT, exist_ok=True)

plt.rcParams.update({
    "figure.dpi": 130,
    "savefig.dpi": 130,
    "font.size": 11,
    "axes.grid": True,
    "grid.alpha": 0.3,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "figure.autolayout": True,
})

AZ = "#1f4e79"     # azul
RO = "#c0392b"     # rojo
VE = "#1e8449"     # verde
NA = "#e67e22"     # naranja
PU = "#7d3c98"     # purpura


def save(fig, name):
    path = os.path.join(OUT, name)
    fig.savefig(path, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("OK", name)


# ---------------------------------------------------------------- Clase 1
def fig_limite_vs_valor():
    fig, ax = plt.subplots(figsize=(6.2, 4.2))
    x = np.linspace(-0.5, 4.5, 600)
    f = np.where(np.abs(x - 2) < 1e-9, np.nan, (x**2 - x - 2) / (x - 2))
    ax.plot(x, f, color=AZ, lw=2.4, label=r"$f(x)=\dfrac{x^2-x-2}{x-2}$")
    ax.plot([2], [3], "o", mfc="white", mec=RO, mew=2.4, ms=11,
            label=r"hueco: $f(2)$ no definido")
    ax.plot([2], [3], "o", color=RO, ms=4)
    ax.axvline(2, ls=":", color="gray")
    ax.axhline(3, ls=":", color="gray")
    ax.annotate(r"$\lim_{x\to 2} f(x)=3$", xy=(2, 3), xytext=(2.35, 2.1),
                color=RO, fontsize=12,
                arrowprops=dict(arrowstyle="->", color=RO))
    ax.set_xlim(-0.5, 4.5); ax.set_ylim(0.5, 6.2)
    ax.set_xlabel("x"); ax.set_ylabel("y")
    ax.set_title("El límite no depende del valor en el punto")
    ax.legend(loc="upper left")
    save(fig, "b0_limite_vs_valor.png")


def fig_discontinuidades():
    fig, axs = plt.subplots(1, 3, figsize=(11, 3.4))
    # evitable
    x = np.linspace(-2, 2, 600)
    f = np.where(np.abs(x) < 1e-9, np.nan, np.sin(x) / x)
    axs[0].plot(x, f, color=AZ, lw=2.2)
    axs[0].plot([0], [1], "o", mfc="white", mec=RO, mew=2.2, ms=9)
    axs[0].set_title("Evitable\n(límite existe, ≠ valor)")
    # salto
    x1 = np.linspace(-2, 0, 300); x2 = np.linspace(0, 2, 300)
    axs[1].plot(x1, x1 + 1, color=AZ, lw=2.2)
    axs[1].plot(x2, x2 + 2, color=PU, lw=2.2)
    axs[1].plot([0], [1], "o", mfc="white", mec=AZ, mew=2.2, ms=9)
    axs[1].plot([0], [2], "o", color=PU, ms=9)
    axs[1].set_title("Salto finito\n(límites laterales ≠)")
    # esencial
    x = np.linspace(-2, 2, 800)
    axs[2].plot(x, np.sin(1 / np.where(np.abs(x) < 1e-6, np.nan, x)),
                color=RO, lw=1.6)
    axs[2].set_ylim(-1.4, 1.4)
    axs[2].set_title("Esencial\n(no existe el límite)")
    for a in axs:
        a.axhline(0, color="gray", lw=0.8)
        a.axvline(0, color="gray", lw=0.8)
    save(fig, "b0_discontinuidades.png")


# ---------------------------------------------------------------- Clase 2
def fig_tangente():
    fig, ax = plt.subplots(figsize=(6.2, 4.4))
    f = lambda t: t**2
    x = np.linspace(-0.4, 3.6, 400)
    ax.plot(x, f(x), color=AZ, lw=2.4, label=r"$f(x)=x^2$")
    a, h = 1.0, 1.3
    ax.plot([a, a + h], [f(a), f(a + h)], color=NA, lw=2, label="secante")
    ax.plot([a, a], [f(a), f(a + h)], ls=":", color="gray")
    ax.plot([a + h, a + h], [f(a), f(a + h)], ls=":", color="gray")
    xa = np.array([-0.4, 3.6])
    ax.plot(xa, f(a) + 2 * a * (xa - a), color=RO, lw=2.2, label="tangente")
    ax.plot([a], [f(a)], "o", color=AZ, ms=8)
    ax.text(a + h, f(a + h) + 0.25, r"$(x_0+h,\ f(x_0+h))$", color=NA)
    ax.text(a - 0.05, f(a) - 0.9, r"$(x_0,\ f(x_0))$", color=AZ)
    ax.annotate("", xy=(a, f(a + h)), xytext=(a + h, f(a + h)),
                arrowprops=dict(arrowstyle="<->", color="gray"))
    ax.text(a + h / 2, f(a + h) - 0.35, "h", color="gray")
    ax.set_title(r"La derivada es la pendiente de la tangente: $f'(x_0)=\lim_{h\to0}\frac{f(x_0+h)-f(x_0)}{h}$")
    ax.set_xlabel("x"); ax.set_ylabel("y")
    ax.legend(loc="upper left")
    save(fig, "b0_tangente.png")


def fig_riemann():
    fig, ax = plt.subplots(figsize=(6.6, 4.2))
    f = lambda t: 1 + 0.6 * np.sin(1.6 * t) + 0.25 * t
    a, b, n = 0.5, 4.5, 10
    x = np.linspace(a, b, 500)
    ax.plot(x, f(x), color=AZ, lw=2.4, label=r"$y=f(x)$")
    xs = np.linspace(a, b, n + 1)
    ax.bar(xs[:-1], f(xs[:-1]), width=np.diff(xs), align="edge",
           color=NA, alpha=0.45, edgecolor=NA)
    ax.set_xlabel("x"); ax.set_ylabel("y")
    ax.set_title(r"Área bajo la curva $\approx$ suma de Riemann $\to \int_a^b f$")
    ax.legend(loc="upper left")
    save(fig, "b0_riemann.png")


def fig_tfc():
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    f = lambda t: 1 + 0.5 * np.sin(t) + 0.18 * t
    x = np.linspace(0, 5, 500)
    ax.plot(x, f(x), color=AZ, lw=2.4)
    a = 0.6
    xs = np.linspace(a, 3.6, 200)
    ax.fill_between(xs, 0, f(xs), color=VE, alpha=0.25)
    ax.text(2.0, 0.45, r"$A(x)=\int_a^x f(t)\,dt$", color=VE, fontsize=12)
    ax.annotate("", xy=(3.6, 0), xytext=(3.6, f(3.6)),
                arrowprops=dict(arrowstyle="<->", color=VE))
    ax.plot([3.6], [f(3.6)], "o", color=VE)
    ax.axvline(a, ls=":", color="gray")
    ax.set_xlabel("x"); ax.set_ylabel("y")
    ax.set_title(r"TFC: $A'(x)=f(x)$ (crece donde $f>0$)")
    save(fig, "b0_tfc.png")


# ---------------------------------------------------------------- Clase 3
def fig_sucesion_limite():
    fig, ax = plt.subplots(figsize=(7.0, 4.2))
    n = np.arange(1, 26)
    a = 1 + 1.0 / n
    L = 1.0
    ax.plot(n, a, "o", color=AZ, ms=5)
    ax.axhline(L, color=RO, lw=1.6)
    for e, al in [(0.3, 0.20), (0.15, 0.35)]:
        ax.axhspan(L - e, L + e, color=RO, alpha=al)
    ax.text(24.2, L + 0.25, r"$L=1$", color=RO)
    ax.annotate(r"$|a_n-L|<\varepsilon$", xy=(14, L + 0.15),
                xytext=(11, L + 0.5), color=RO,
                arrowprops=dict(arrowstyle="->", color=RO))
    ax.plot([6, 6], [L - 0.3, L + 0.3], ls="--", color="gray")
    ax.text(6, L - 0.42, r"$n_0$", color="gray", ha="center")
    ax.set_xlabel("n"); ax.set_ylabel(r"$a_n$")
    ax.set_title(r"$a_n \to L$: para todo $\varepsilon>0$ existe $n_0$ tal que $n\geq n_0$ implica $|a_n-L|<\varepsilon$")
    save(fig, "b0_sucesion_limite.png")


def fig_monotona_acotada():
    fig, ax = plt.subplots(figsize=(7.0, 4.0))
    n = np.arange(1, 30)
    a = 3 * (1 - 0.72**n)
    ax.plot(n, a, "o-", color=AZ, ms=4, lw=1.3)
    ax.axhline(3, color=RO, ls="--")
    ax.text(2, 3.08, r"cota superior $=3$", color=RO)
    ax.axhline(0, color=VE, ls="--")
    ax.text(2, -0.25, r"cota inferior $=0$", color=VE)
    ax.set_ylim(-0.6, 3.6)
    ax.set_xlabel("n"); ax.set_ylabel(r"$a_n$")
    ax.set_title("Creciente y acotada  ⟹  converge (PSMC)")
    save(fig, "b0_monotona_acotada.png")


# ---------------------------------------------------------------- Clase 4
def fig_vectores():
    fig, ax = plt.subplots(figsize=(6.0, 5.0))
    o = np.array([0, 0])
    u = np.array([3, 1]); v = np.array([1, 2.4])
    ax.quiver(*o, *u, angles="xy", scale_units="xy", scale=1, color=AZ)
    ax.quiver(*o, *v, angles="xy", scale_units="xy", scale=1, color=RO)
    ax.quiver(*u, *v, angles="xy", scale_units="xy", scale=1, color=VE, alpha=0.6)
    ax.quiver(*v, *u, angles="xy", scale_units="xy", scale=1, color=VE, alpha=0.6)
    ax.quiver(*o, *(u + v), angles="xy", scale_units="xy", scale=1, color=PU, width=0.012)
    ax.text(*u, r"$\vec u$", color=AZ, fontsize=13)
    ax.text(*v, r"$\vec v$", color=RO, fontsize=13)
    ax.text(*(u + v), r"$\vec u+\vec v$", color=PU, fontsize=13)
    # proyeccion
    p = (u @ v) / (u @ u) * u
    ax.plot([v[0], p[0]], [v[1], p[1]], ls=":", color="gray")
    ax.quiver(*o, *p, angles="xy", scale_units="xy", scale=1, color="black", alpha=0.6)
    ax.text(*p, r"proy$_{\vec u}\vec v$", color="black", fontsize=10)
    ax.set_xlim(-0.5, 4.6); ax.set_ylim(-0.5, 4.0)
    ax.axhline(0, color="gray", lw=0.8); ax.axvline(0, color="gray", lw=0.8)
    ax.set_aspect("equal")
    ax.set_title(r"Suma de vectores y proyección ($\vec u\cdot\vec v$)")
    save(fig, "b0_vectores.png")


def fig_recta_plano():
    fig = plt.figure(figsize=(10.5, 4.4))
    ax = fig.add_subplot(1, 2, 1, projection="3d")
    t = np.linspace(-2, 2, 100)
    p0 = np.array([1, 1, 1]); d = np.array([1, -1, 2])
    ax.plot(p0[0] + d[0] * t, p0[1] + d[1] * t, p0[2] + d[2] * t,
            color=AZ, lw=2.4)
    ax.quiver(*p0, *d, color=RO, length=2.2)
    ax.scatter(*p0, color="black", s=30)
    ax.text(*p0, r"$P_0$")
    ax.text(*(p0 + d * 2.0), r"$\vec d$", color=RO)
    ax.set_title(r"Recta: $P_0 + t\,\vec d$")
    ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_zlabel("z")
    ax.set_box_aspect((1, 1, 1))

    ax2 = fig.add_subplot(1, 2, 2, projection="3d")
    X, Y = np.meshgrid(np.linspace(-2, 2, 12), np.linspace(-2, 2, 12))
    Z = 1 - 0.4 * X - 0.4 * Y
    ax2.plot_surface(X, Y, Z, color=NA, alpha=0.55)
    nvec = np.array([0.4, 0.4, 1.0])
    ax2.quiver(0, 0, 1, *nvec, color=RO, length=1.6)
    ax2.set_title(r"Plano: $\vec n\cdot(\vec x-\vec P_0)=0$")
    ax2.set_xlabel("x"); ax2.set_ylabel("y"); ax2.set_zlabel("z")
    ax2.set_box_aspect((1, 1, 1))
    save(fig, "b0_recta_plano.png")


def fig_conicas():
    fig, axs = plt.subplots(2, 2, figsize=(8.2, 8.0))
    th = np.linspace(0, 2 * np.pi, 400)
    # circunferencia
    axs[0, 0].plot(np.cos(th), np.sin(th), color=AZ, lw=2.2)
    axs[0, 0].set_title(r"Circunferencia $x^2+y^2=r^2$")
    # elipse
    axs[0, 1].plot(2 * np.cos(th), np.sin(th), color=VE, lw=2.2)
    axs[0, 1].set_title(r"Elipse $\dfrac{x^2}{a^2}+\dfrac{y^2}{b^2}=1$")
    # parabola
    x = np.linspace(-2, 2, 300)
    axs[1, 0].plot(x, x**2, color=NA, lw=2.2)
    axs[1, 0].set_title(r"Parábola $y=x^2$")
    # hiperbola
    t = np.linspace(-2.2, 2.2, 400)
    axs[1, 1].plot(np.cosh(t), np.sinh(t), color=PU, lw=2.2)
    axs[1, 1].plot(-np.cosh(t), np.sinh(t), color=PU, lw=2.2)
    axs[1, 1].set_title(r"Hipérbola $x^2-y^2=1$")
    for a in axs.ravel():
        a.axhline(0, color="gray", lw=0.8); a.axvline(0, color="gray", lw=0.8)
        a.set_aspect("equal")
    save(fig, "b0_conicas.png")


def fig_cuadricas():
    fig = plt.figure(figsize=(10.5, 3.8))
    u = np.linspace(0, 2 * np.pi, 40)
    v = np.linspace(0, np.pi, 25)
    # esfera
    ax = fig.add_subplot(1, 3, 1, projection="3d")
    X = np.outer(np.cos(u), np.sin(v)); Y = np.outer(np.sin(u), np.sin(v)); Z = np.outer(np.ones_like(u), np.cos(v))
    ax.plot_surface(X, Y, Z, color=AZ, alpha=0.6)
    ax.set_title("Esfera")
    # paraboloide
    ax = fig.add_subplot(1, 3, 2, projection="3d")
    r = np.linspace(0, 1.3, 25); th = np.linspace(0, 2 * np.pi, 40)
    R, T = np.meshgrid(r, th)
    ax.plot_surface(R * np.cos(T), R * np.sin(T), R**2, color=VE, alpha=0.6)
    ax.set_title("Paraboloide")
    # hiperboloide
    ax = fig.add_subplot(1, 3, 3, projection="3d")
    zz = np.linspace(-1.3, 1.3, 25)
    R, T = np.meshgrid(np.linspace(0.3, 1.3, 15), np.linspace(0, 2 * np.pi, 40))
    Zr, Tr = np.meshgrid(zz, np.linspace(0, 2 * np.pi, 40))
    ax.plot_surface(np.sqrt(1 + Zr**2) * np.cos(Tr), np.sqrt(1 + Zr**2) * np.sin(Tr), Zr,
                    color=PU, alpha=0.6)
    ax.set_title("Hiperboloide")
    for a in fig.axes:
        a.set_box_aspect((1, 1, 1)); a.set_xticks([]); a.set_yticks([]); a.set_zticks([])
    save(fig, "b0_cuadricas.png")


if __name__ == "__main__":
    fig_limite_vs_valor()
    fig_discontinuidades()
    fig_tangente()
    fig_riemann()
    fig_tfc()
    fig_sucesion_limite()
    fig_monotona_acotada()
    fig_vectores()
    fig_recta_plano()
    fig_conicas()
    fig_cuadricas()
    print("Listo.")
