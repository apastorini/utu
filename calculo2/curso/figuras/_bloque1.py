# -*- coding: utf-8 -*-
"""Figuras del Bloque 1 (clases 5-8): Numeros complejos."""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, FancyArrowPatch

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


def complejo(ax, z, color=AZ, label=None, lw=2.2, ls="-"):
    ax.annotate("", xy=(z.real, z.imag), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, ls=ls,
                                shrinkA=0, shrinkB=0))
    if label:
        ax.text(z.real * 1.06 + 0.02, z.imag * 1.06 + 0.02, label,
                color=color, fontsize=12)


def ax_complejo(ax, lim=3):
    ax.axhline(0, color="gray", lw=1)
    ax.axvline(0, color="gray", lw=1)
    ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim)
    ax.set_aspect("equal")
    ax.set_xlabel("Re"); ax.set_ylabel("Im")


def fig_plano():
    fig, ax = plt.subplots(figsize=(5.8, 5.4))
    a, b = 2.0, 1.5
    z = complex(a, b)
    ax_complejo(ax, 3)
    # proyecciones
    ax.plot([a, a], [0, b], ls=":", color="gray")
    ax.plot([0, a], [b, b], ls=":", color="gray")
    complejo(ax, z, AZ, r"$z=a+bi$")
    complejo(ax, z.conjugate(), RO, r"$\bar z=a-bi$", lw=1.8, ls="--")
    # modulo y angulo
    ax.plot([0, a], [0, b], color=AZ, lw=0.8, alpha=0.4)
    ax.add_patch(Arc((0, 0), 1.6, 1.6, angle=0, theta1=0,
                     theta2=np.degrees(np.arctan2(b, a)), color=NA, lw=2))
    ax.text(1.0, 0.25, r"$\theta$", color=NA, fontsize=13)
    ax.text(a / 2, b / 2 + 0.18, r"$|z|=\rho$", color=VE, fontsize=12)
    ax.text(a, -0.35, "a", color="black", ha="center")
    ax.text(-0.35, b, "b", color="black", va="center")
    ax.set_title("Plano complejo: módulo, argumento y conjugado")
    save(fig, "b1_plano_complejo.png")


def fig_suma():
    fig, ax = plt.subplots(figsize=(5.8, 5.4))
    ax_complejo(ax, 4)
    z1, z2 = complex(2.4, 1.0), complex(1.0, 2.2)
    complejo(ax, z1, AZ, r"$z_1$")
    complejo(ax, z2, RO, r"$z_2$")
    complejo(ax, z1 + z2, PU, r"$z_1+z_2$")
    ax.plot([z1.real, (z1 + z2).real], [z1.imag, (z1 + z2).imag],
            ls="--", color=RO, alpha=0.6)
    ax.plot([z2.real, (z1 + z2).real], [z2.imag, (z1 + z2).imag],
            ls="--", color=AZ, alpha=0.6)
    ax.set_title("La suma de complejos es como sumar vectores")
    save(fig, "b1_suma.png")


def fig_polar_mult():
    fig, ax = plt.subplots(figsize=(5.8, 5.4))
    ax_complejo(ax, 4)
    r1, t1 = 1.6, np.radians(25)
    r2, t2 = 1.3, np.radians(40)
    z1 = r1 * np.exp(1j * t1); z2 = r2 * np.exp(1j * t2)
    z = z1 * z2
    complejo(ax, z1, AZ, r"$z_1=\rho_1e^{i\theta_1}$")
    complejo(ax, z2, RO, r"$z_2=\rho_2e^{i\theta_2}$")
    complejo(ax, z, VE, r"$z_1z_2$", lw=2.6)
    ax.add_patch(Arc((0, 0), 1.3, 1.3, theta1=0, theta2=np.degrees(t1), color=AZ, lw=1.6))
    ax.add_patch(Arc((0, 0), 1.9, 1.9, theta1=0, theta2=np.degrees(t2), color=RO, lw=1.6))
    ax.add_patch(Arc((0, 0), 2.6, 2.6, theta1=0, theta2=np.degrees(t1 + t2), color=VE, lw=1.6))
    ax.text(0.9, 0.35, r"$\theta_1$", color=AZ)
    ax.text(0.2, 1.15, r"$\theta_2$", color=RO)
    ax.text(0.45, 2.0, r"$\theta_1+\theta_2$", color=VE)
    ax.set_title(r"Producto: módulos se multiplican, ángulos se suman")
    save(fig, "b1_producto.png")


def fig_demoivre():
    fig, axs = plt.subplots(1, 2, figsize=(10.5, 5.0))
    for ax, r, titulo in [(axs[0], 1.12, r"$|z|>1$: espiral hacia afuera"),
                          (axs[1], 0.9, r"$|z|<1$: espiral hacia adentro")]:
        ax_complejo(ax, 3)
        th = np.linspace(0, 6 * np.pi / 5, 400)
        rr = r ** (th / (np.pi / 5))
        ax.plot(rr * np.cos(th), rr * np.sin(th), color="gray", lw=1, alpha=0.6)
        for k in range(0, 11):
            zk = r**k * np.exp(1j * k * np.pi / 5)
            ax.plot(zk.real, zk.imag, "o", color=AZ, ms=4)
        ax.set_title(titulo + "\n" + r"$z^k = r^k e^{ik\theta}$")
    save(fig, "b1_demoivre.png")


def fig_raices():
    """Raices cuartas de w = 1 - i*sqrt(3) (examen dic 2022)."""
    fig, ax = plt.subplots(figsize=(5.8, 5.4))
    ax_complejo(ax, 1.6)
    w = 1 - 1j * np.sqrt(3)
    rho0, th0 = 2.0, -np.pi / 3
    n = 4
    r = rho0 ** (1 / n)
    th = [(th0 + 2 * k * np.pi) / n for k in range(n)]
    xs = [r * np.cos(t) for t in th]; ys = [r * np.sin(t) for t in th]
    # circunferencia de radio r
    tt = np.linspace(0, 2 * np.pi, 200)
    ax.plot(r * np.cos(tt), r * np.sin(tt), ls="--", color="gray", lw=1)
    for k, (x, y) in enumerate(zip(xs, ys)):
        complejo(ax, complex(x, y), AZ if k else RO, rf"$z_{k}$")
    ax.plot(xs + [xs[0]], ys + [ys[0]], color=PU, lw=1.2, alpha=0.7)
    ax.set_title(r"Las 4 raíces cuartas de $1-i\sqrt{3}$ forman un cuadrado")
    save(fig, "b1_raices.png")


def fig_unidad():
    fig, ax = plt.subplots(figsize=(5.8, 5.4))
    ax_complejo(ax, 1.6)
    n = 7
    tt = np.linspace(0, 2 * np.pi, 300)
    ax.plot(np.cos(tt), np.sin(tt), ls="--", color="gray", lw=1)
    for k in range(n):
        z = np.exp(2j * np.pi * k / n)
        complejo(ax, z, AZ, rf"$\omega^{k}$" if k < 7 else None)
    ax.set_title(r"Las $n=7$ raíces $n$-ésimas de la unidad ($z^n=1$)")
    save(fig, "b1_raices_unidad.png")


def fig_euler():
    fig, ax = plt.subplots(figsize=(5.8, 5.4))
    ax_complejo(ax, 1.7)
    tt = np.linspace(0, 2 * np.pi, 300)
    ax.plot(np.cos(tt), np.sin(tt), color=AZ, lw=2)
    th = np.radians(50)
    z = np.exp(1j * th)
    ax.plot([0, z.real], [0, z.imag], color=RO, lw=2.2)
    ax.plot([z.real, z.real], [0, z.imag], ls=":", color="gray")
    ax.plot([0, z.real], [0, 0], color=VE, lw=2)
    ax.plot([0, 0], [0, z.imag], color=NA, lw=2)
    ax.text(z.real + 0.03, z.imag + 0.03, r"$e^{i\theta}=\cos\theta+i\sin\theta$",
            color=RO, fontsize=12)
    ax.text(z.real / 2, -0.22, r"$\cos\theta$", color=VE, ha="center")
    ax.text(-0.28, z.imag / 2, r"$i\,\sin\theta$", color=NA, ha="right")
    # puntos notables
    for zz, lab in [(-1, r"$e^{i\pi}=-1$"), (1j, r"$i$"), (-1j, r"$-i$"), (1, r"$1$")]:
        ax.plot([zz.real], [zz.imag], "o", color="black", ms=5)
        ax.text(zz.real + 0.05, zz.imag + 0.05, lab, fontsize=11)
    ax.set_title("Fórmula de Euler: la circunferencia unidad")
    save(fig, "b1_euler.png")


def fig_exp():
    """La exponencial compleja mapea franjas horizontales en sectores."""
    fig, ax = plt.subplots(figsize=(6.0, 5.4))
    ax_complejo(ax, 3)
    for b, col in [(0.0, VE), (np.pi / 3, AZ), (2 * np.pi / 3, NA), (np.pi, RO)]:
        rr = np.linspace(0, 1.1, 50)
        ax.plot(rr * np.cos(b), rr * np.sin(b), color=col, lw=1.8)
    th = np.linspace(0, np.pi, 100)
    for r, a in [(0.4, 0.25), (0.7, 0.18), (1.0, 0.12)]:
        ax.plot(r * np.cos(th), r * np.sin(th), color="gray", lw=1.2, alpha=a)
    ax.text(0.0, -0.25, r"$e^{a+bi}=e^a(\cos b+i\sin b)$", fontsize=12, color=AZ)
    ax.set_title("Parte real fija $a$: el rayo crece; parte imaginaria fija $b$: el ángulo")
    save(fig, "b1_exponencial.png")


if __name__ == "__main__":
    fig_plano(); fig_suma(); fig_polar_mult(); fig_demoivre()
    fig_raices(); fig_unidad(); fig_euler(); fig_exp()
    print("Listo.")
