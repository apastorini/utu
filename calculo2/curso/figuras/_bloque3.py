# -*- coding: utf-8 -*-
"""Figuras del Bloque 3 (clases 16-20): Sucesiones."""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "img")
os.makedirs(OUT, exist_ok=True)

plt.rcParams.update({
    "figure.dpi": 130, "savefig.dpi": 130, "font.size": 11,
    "axes.grid": True, "grid.alpha": 0.3,
    "axes.spines.top": False, "axes.spines.right": False,
    "figure.autolayout": True,
})
AZ, RO, VE, NA, PU = "#1f4e79", "#c0392b", "#1e8449", "#e67e22", "#7d3c98"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("OK", name)


def fig_convergencia():
    """Definición eps-N: a partir de n0 todos los puntos caen en E(L,eps)."""
    fig, ax = plt.subplots(figsize=(7.2, 4.6))
    n = np.arange(1, 19)
    L = 2.0
    a = L + 1.3 * (-1.0) ** n / n + 0.9 / n * np.cos(n)
    eps = 0.5
    ax.axhspan(L - eps, L + eps, color=NA, alpha=0.15)
    ax.axhline(L, color=VE, lw=1.8, label=r"$L$")
    ax.axhline(L + eps, ls="--", color=NA, lw=1.2)
    ax.axhline(L - eps, ls="--", color=NA, lw=1.2)
    ax.plot(n, a, "o", color=AZ, ms=5)
    ax.vlines(n, L, a, color=AZ, lw=0.8, alpha=0.4)
    n0 = 6
    ax.axvline(n0, color=RO, ls=":", lw=1.6)
    ax.text(n0 + 0.1, L - eps - 0.55, r"$n_0$", color=RO)
    ax.text(17.6, L + eps + 0.12, r"$E(L,\varepsilon)$", color=NA, ha="right")
    ax.set_title(r"Convergencia: $\forall\varepsilon>0\ \exists n_0:\ a_n\in E(L,\varepsilon)\ \forall n\geq n_0$")
    ax.set_xlabel("n"); ax.set_ylabel(r"$a_n$")
    ax.legend(loc="upper right")
    save(fig, "b3_convergencia.png")


def fig_monotona():
    """Sucesión monótona y acotada: converge al supremo."""
    fig, ax = plt.subplots(figsize=(7.0, 4.4))
    n = np.arange(1, 16)
    M = 3.0
    a = M - 2.2 * (0.62) ** n          # creciente, acotada por M
    b = (0.55) ** n                    # decreciente, acotada inferiormente por 0
    ax.plot(n, a, "o-", color=AZ, lw=1.6, label=r"creciente, acotada $\to \sup$")
    ax.plot(n, b, "s-", color=VE, lw=1.6, label=r"decreciente, acotada $\to \inf$")
    ax.axhline(M, ls="--", color=AZ, lw=1.2)
    ax.text(14.9, M + 0.08, r"$\sup = M$", color=AZ, ha="right")
    ax.axhline(0, ls="--", color=VE, lw=1.2)
    ax.text(14.9, 0.08, r"$\inf = 0$", color=VE, ha="right")
    ax.set_title("Toda sucesión monótona y acotada converge")
    ax.set_xlabel("n"); ax.set_ylabel(r"$a_n$")
    ax.legend()
    save(fig, "b3_monotona.png")


def fig_no_convergente():
    """Comparación: (-1)^n acotada no convergente; n no acotada y divergente."""
    fig, axs = plt.subplots(1, 2, figsize=(12, 4.2))
    n = np.arange(1, 15)
    axs[0].plot(n, (-1.0) ** n, "o", color=RO, ms=6)
    axs[0].axhline(1, ls=":", color="gray", lw=1); axs[0].axhline(-1, ls=":", color="gray", lw=1)
    axs[0].set_ylim(-1.6, 1.6)
    axs[0].set_title(r"$a_n=(-1)^n$: acotada, pero NO converge")
    axs[0].set_xlabel("n"); axs[0].set_ylabel(r"$a_n$")
    axs[1].plot(n, n, "o-", color=AZ, lw=1.6)
    axs[1].set_title(r"$a_n=n$: converge? no, $a_n\to+\infty$")
    axs[1].set_xlabel("n"); axs[1].set_ylabel(r"$a_n$")
    save(fig, "b3_no_convergente.png")


def fig_subsucesiones():
    """Sucesión con dos puntos de aglomeración (subsucesiones convergentes)."""
    fig, ax = plt.subplots(figsize=(7.4, 4.6))
    n = np.arange(1, 21)
    # par -> tiende a 1, impar -> tiende a -1
    a = np.where(n % 2 == 0, 1.0 - 0.6 / n, -1.0 + 0.6 / n)
    ax.plot(n, a, "o", color=AZ, ms=5)
    pares = n[n % 2 == 0]; impares = n[n % 2 == 1]
    ax.plot(pares, a[pares - 1], "o", color=VE, ms=6, label=r"$a_{2n}\to 1$")
    ax.plot(impares, a[impares - 1], "o", color=RO, ms=6, label=r"$a_{2n+1}\to -1$")
    ax.axhline(1, ls="--", color=VE, lw=1.2)
    ax.axhline(-1, ls="--", color=RO, lw=1.2)
    ax.set_ylim(-1.6, 1.6)
    ax.set_title("Subsucesiones y puntos de aglomeración")
    ax.set_xlabel("n"); ax.set_ylabel(r"$a_n$")
    ax.legend()
    save(fig, "b3_subsucesiones.png")


def fig_bw():
    """Bolzano-Weierstrass: toda sucesión acotada tiene subsucesión convergente."""
    fig, ax = plt.subplots(figsize=(7.6, 4.4))
    n = np.arange(1, 26)
    a = np.sin(1.3 * n) + 0.3 * np.cos(0.7 * n)
    ax.plot(n, a, "o", color="#9aa6b2", ms=4, label=r"$(a_n)$ acotada")
    # marco la subsucesión que converge (por ejemplo las que pasan cerca de un max local)
    idx = [3, 9, 16, 22]
    ax.plot(n[idx], a[idx], "o-", color=RO, lw=1.6, ms=7,
            label=r"subsucesión convergente")
    ax.axhspan(a.min() - 0.1, a.max() + 0.1, color=NA, alpha=0.08)
    ax.set_title("Bolzano-Weierstrass: toda sucesión acotada tiene una subsucesión convergente")
    ax.set_xlabel("n"); ax.set_ylabel(r"$a_n$")
    ax.legend(loc="lower right")
    save(fig, "b3_bw.png")


def fig_recurrencia():
    """Telaraña (cobweb) de x_{n+1}=1+1/x_n: converge a (1+sqrt5)/2."""
    fig, ax = plt.subplots(figsize=(6.2, 5.8))
    f = lambda t: 1.0 + 1.0 / t
    L = (1 + 5 ** 0.5) / 2
    t = np.linspace(0.55, 2.2, 400)
    ax.plot(t, f(t), color=AZ, lw=2.0, label=r"$y=1+1/x$")
    ax.plot(t, t, color="gray", lw=1.2, ls=":", label=r"$y=x$")
    x = 1.0
    xs, ys = [x], []
    for _ in range(14):
        y = f(x)
        ys.append(y)
        xs.append(y)
    ax.plot(xs[:-1], ys, "-", color=RO, lw=1.2, alpha=0.8)
    ax.plot(xs[1:], ys, "-", color=RO, lw=1.2, alpha=0.8)
    ax.plot([L], [L], "o", color=VE, ms=8, label=r"$\varphi=1{,}618\ldots$")
    ax.set_xlim(0.55, 2.2); ax.set_ylim(0.55, 2.2)
    ax.set_aspect("equal")
    ax.set_title(r"Recurrencia $x_{n+1}=1+\frac{1}{x_n}$: telaraña y punto fijo")
    ax.set_xlabel(r"$x_n$"); ax.set_ylabel(r"$x_{n+1}$")
    ax.legend(loc="upper left")
    save(fig, "b3_recurrencia.png")


def fig_cauchy():
    """Criterio de Cauchy: los términos se acercan entre sí."""
    fig, ax = plt.subplots(figsize=(7.2, 4.4))
    n = np.arange(1, 40)
    a = 1.0 + 2.0 / n * np.sin(np.log(n + 1))
    ax.plot(n, a, "o", color=AZ, ms=4)
    ax.axhspan(1 - 0.15, 1 + 0.15, color=VE, alpha=0.12)
    ax.axhline(1, ls="--", color=VE, lw=1.4)
    for k in [25, 27]:
        ax.vlines(k, 1, a[k - 1], color=RO, lw=1.0, alpha=0.6)
    ax.annotate("", xy=(35, 1 + 0.15), xytext=(35, 1 - 0.15),
                arrowprops=dict(arrowstyle="<->", color=RO, lw=1.4))
    ax.text(35.4, 1.0, r"$|a_m-a_n|<\varepsilon$", color=RO, va="center")
    ax.set_title(r"Criterio de Cauchy: $|a_m-a_n|<\varepsilon$ para $m,n\geq n_0$")
    ax.set_xlabel("n"); ax.set_ylabel(r"$a_n$")
    save(fig, "b3_cauchy.png")


def fig_mapa():
    """Mapa visual del bloque: 6 comportamientos típicos de sucesiones."""
    fig, axs = plt.subplots(2, 3, figsize=(13, 7.4))
    n = np.arange(1, 31)

    a = axs[0, 0]
    a.plot(n, 1.0 / n, "o-", color=VE, ms=4, lw=1.4)
    a.axhline(0, ls="--", color="gray", lw=1.2)
    a.set_title(r"1) Convergente: $a_n=\frac{1}{n}\to0$")

    a = axs[0, 1]
    a.plot(n, n, "o-", color=RO, ms=4, lw=1.4)
    a.set_title(r"2) Divergente no acotada: $a_n=n\to+\infty$")

    a = axs[0, 2]
    a.plot(n, (-1.0) ** n, "o", color=PU, ms=5)
    a.axhline(1, ls=":", color="gray", lw=1.2)
    a.axhline(-1, ls=":", color="gray", lw=1.2)
    a.set_ylim(-1.6, 1.6)
    a.set_title(r"3) Acotada, no converge: $a_n=(-1)^n$")
    a.text(15, 0.05, r"puntos de aglomeración $1,-1$", ha="center", fontsize=9)

    a = axs[1, 0]
    a.plot(n, 3.0 - 2.0 * (0.7) ** n, "o-", color=AZ, ms=4, lw=1.4)
    a.axhline(3, ls="--", color=AZ, lw=1.2)
    a.set_title(r"4) Monótona y acotada $\to\sup$ (PSMC)")

    a = axs[1, 1]
    sub = n[1:10:2]
    a.plot(n, 2.0 + 0.8 * np.sin(n), "o", color="#9aa6b2", ms=4)
    a.plot(sub, 2.0 + 0.8 * np.sin(sub), "o-", color=RO, ms=6, lw=1.6)
    a.set_title(r"5) Subsucesión convergente (BW)")
    a.text(15, 1.1, "acotada $\\Rightarrow$ BW", ha="center", fontsize=9)

    a = axs[1, 2]
    m = np.arange(1, 26)
    a.plot(m, 1.0 + 1.5 / m, "o-", color=NA, ms=4, lw=1.4)
    for x in (18, 20):
        a.vlines(x, 1 + 1.5 / 26, 1 + 1.5 / x + 0.02, color=RO, lw=1.0)
    a.annotate("", xy=(23, 1.03), xytext=(23, 1.055),
               arrowprops=dict(arrowstyle="<->", color=RO, lw=1.4))
    a.text(24, 1.042, r"$|a_m-a_n|<\varepsilon$", va="center", fontsize=9, color=RO)
    a.set_title(r"6) Cauchy: $|a_m-a_n|\to0$")

    for a in axs.ravel():
        a.set_xlabel("n")
        a.set_ylabel(r"$a_n$")
    fig.suptitle("Mapa visual de comportamientos de sucesiones (Bloque 3)",
                 fontsize=13, y=1.0)
    save(fig, "b3_mapa.png")


if __name__ == "__main__":
    fig_convergencia(); fig_monotona(); fig_no_convergente()
    fig_subsucesiones(); fig_bw(); fig_recurrencia(); fig_cauchy()
    fig_mapa()
    print("Listo.")
