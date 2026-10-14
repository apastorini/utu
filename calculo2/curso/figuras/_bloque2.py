# -*- coding: utf-8 -*-
"""Figuras del Bloque 2 (clases 9-15): Ecuaciones diferenciales."""
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


def campo(ax, f, xr, yr, n=14):
    xs = np.linspace(*xr, n)
    ys = np.linspace(*yr, n)
    X, Y = np.meshgrid(xs, ys)
    U = np.ones_like(X)
    V = f(X, Y)
    L = np.sqrt(U**2 + V**2)
    ax.quiver(X, Y, U / L, V / L, color="gray", alpha=0.55, scale=28,
              width=0.0035)


def fig_pendientes():
    fig, ax = plt.subplots(figsize=(6.4, 5.2))
    def f(x, y): return y  # y' = y
    campo(ax, f, (-2.2, 2.2), (-2.2, 2.2))
    xx = np.linspace(-2.2, 2.2, 200)
    for k in [-1.5, -1.0, -0.5, 0.5, 1.0, 1.5]:
        ax.plot(xx, k * np.exp(xx), color=AZ, lw=2.0)
    ax.set_title(r"Campo de pendientes de $y'=y$ con soluciones $ke^x$")
    ax.set_xlabel("x"); ax.set_ylabel("y")
    save(fig, "b2_pendientes.png")


def fig_crecimiento():
    fig, ax = plt.subplots(figsize=(6.4, 4.6))
    t = np.linspace(0, 3, 200)
    ax.plot(t, np.exp(0.8 * t), color=RO, lw=2.4, label=r"$k>0$: crece ($y(0)=1$)")
    ax.plot(t, np.exp(-0.8 * t), color=AZ, lw=2.4, label=r"$k<0$: decae ($y(0)=1$)")
    ax.axhline(1, ls=":", color="gray", lw=1)
    ax.set_title(r"$y'=ky$: crecimiento y decaimiento exponencial")
    ax.set_xlabel("t"); ax.set_ylabel("y")
    ax.legend()
    save(fig, "b2_crecimiento.png")


def fig_logistica():
    fig, ax = plt.subplots(figsize=(6.4, 4.6))
    A = 100.0
    t = np.linspace(0, 8, 300)
    for Ce, col in [(0.2, VE), (1.0, RO), (3.0, NA)]:
        x = A / (1 + Ce * np.exp(-A * t))
        ax.plot(t, x, color=col, lw=2.2, label=f"C = {Ce}")
    ax.axhline(A, ls="--", color="gray", lw=1)
    ax.text(7.6, A + 3, f"asíntota A = {A}", color="gray", ha="right")
    ax.set_title(r"Logística $x'=\alpha x(A-x)$: tiende a $A$")
    ax.set_xlabel("t"); ax.set_ylabel("x")
    ax.legend(title=r"$x(0)$ distinto")
    save(fig, "b2_logistica.png")


def fig_caida():
    fig, ax = plt.subplots(figsize=(6.4, 4.6))
    vinf, v0 = 10.0, 2.0
    k, m = 1.2, 1.0
    t = np.linspace(0, 6, 300)
    v = vinf + (v0 - vinf) * np.exp(-(k / m) * t)
    ax.plot(t, v, color=AZ, lw=2.6, label=r"$v(t)$")
    ax.axhline(vinf, ls="--", color=RO, lw=1.6)
    ax.text(5.7, vinf + 0.25, r"$v_\infty=\frac{mg}{k}$", color=RO, ha="right")
    ax.set_title("Caída con resistencia del aire: $mv'=mg-kv$")
    ax.set_xlabel("t"); ax.set_ylabel("v(t)")
    ax.legend()
    save(fig, "b2_caida.png")


def fig_reserva():
    fig, ax = plt.subplots(figsize=(6.4, 4.6))
    u0 = 2.0
    t = np.linspace(0, 12, 300)
    for lam, col in [(0.1, RO), (1 / 150, AZ), (0.05, VE)]:
        u = u0 / (1 + lam * u0 * t**2)
        ax.plot(t, u, color=col, lw=2.2, label=rf"$\lambda$={lam:g}")
    ax.set_title(r"Represa $u'=-2\lambda t\,u^2$: decae a 0")
    ax.set_xlabel("t (días)"); ax.set_ylabel("u (millones de hl)")
    ax.legend(title=rf"$u_0={u0}$")
    save(fig, "b2_reserva.png")


def fig_casos2do():
    fig, axs = plt.subplots(1, 3, figsize=(13, 4.2))
    x = np.linspace(-0.8, 2.6, 300)
    # caso 1: raíces reales distintas y''-5y'+6y=0 => e^{2x}, e^{3x}
    axs[0].plot(x, np.exp(2 * x), color=AZ, lw=2.2, label=r"$e^{2x}$")
    axs[0].plot(x, np.exp(3 * x), color=RO, lw=2.2, label=r"$e^{3x}$")
    axs[0].set_title("Raíces reales distintas\n$y_H=Ae^{2x}+Be^{3x}$")
    axs[0].legend(); axs[0].grid(True, alpha=0.3)
    # caso 2: raíz doble y''+2y'+y=0 => e^{-x}, xe^{-x}
    axs[1].plot(x, np.exp(-x), color=AZ, lw=2.2, label=r"$e^{-x}$")
    axs[1].plot(x, x * np.exp(-x), color=RO, lw=2.2, label=r"$xe^{-x}$")
    axs[1].set_title("Raíz doble\n$y_H=(A+Bx)e^{-x}$")
    axs[1].legend(); axs[1].grid(True, alpha=0.3)
    # caso 3: raíces complejas y''+2y'+5y=0 => e^{-x}cos(2x), e^{-x}sin(2x)
    axs[2].plot(x, np.exp(-x) * np.cos(2 * x), color=AZ, lw=2.2,
                label=r"$e^{-x}\cos 2x$")
    axs[2].plot(x, np.exp(-x) * np.sin(2 * x), color=RO, lw=2.2,
                label=r"$e^{-x}\sin 2x$")
    axs[2].set_title("Raíces complejas $\\alpha\\pm i\\beta$\n$y_H=e^{-x}(A\\cos 2x+B\\sin 2x)$")
    axs[2].legend(); axs[2].grid(True, alpha=0.3)
    save(fig, "b2_casos_2do.png")


def fig_oscilacion():
    fig, ax = plt.subplots(figsize=(6.8, 4.4))
    x = np.linspace(0, 2 * np.pi, 500)
    y = np.exp(-x) * np.sin(3 * x)
    ax.plot(x, y, color=AZ, lw=2.2)
    ax.plot(x, np.exp(-x), ls="--", color=RO, lw=1.4)
    ax.plot(x, -np.exp(-x), ls="--", color=RO, lw=1.4)
    ax.fill_between(x, -np.exp(-x), np.exp(-x), color=NA, alpha=0.08)
    ax.text(0.35, -1.15, "envolvente $\\pm e^{-x}$", color=RO)
    ax.set_title("Oscilación amortiguada $y=e^{-x}\\sin(3x)$")
    ax.set_xlabel("x"); ax.set_ylabel("y")
    save(fig, "b2_oscilacion.png")


if __name__ == "__main__":
    fig_pendientes(); fig_crecimiento(); fig_logistica(); fig_caida()
    fig_reserva(); fig_casos2do(); fig_oscilacion()
    print("Listo.")