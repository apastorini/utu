# -*- coding: utf-8 -*-
"""Figuras del Bloque 10 — Integrales múltiples (clases 45-48).
Genera: b10_fubini, b10_regiones, b10_inversion, b10_polares, b10_disco_corona,
        b10_cilindricas, b10_esfericas, b10_impropias, b10_mapa  (PNG en curso/img/)."""
import os
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, Wedge

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


# 1. Fubini sobre un rectangulo: cortes verticales y horizontales
def fubini():
    fig, pad = plt.subplots(1, 2, figsize=(10, 4.3))

    ax = pad[0]
    ax.set_xlim(-0.08, 1.12); ax.set_ylim(-0.14, 1.18)
    ax.set_aspect("equal"); ax.axis("off")
    ax.add_patch(Rectangle((0, 0), 1, 1, fc="none", ec="k", lw=2))
    for xi in np.arange(0.04, 0.96, 0.13):
        ax.add_patch(Rectangle((xi, 0), 0.085, 1, fc="tab:blue", alpha=0.25,
                               ec="tab:blue", lw=0.8))
    ax.annotate("", xy=(0.5, -0.07), xytext=(0.5, 0.07),
                arrowprops=dict(arrowstyle="<->", color="tab:blue", lw=2))
    ax.text(0.5, -0.11, "A(x) = $\\int_c^d f(x,y)\\,dy$", ha="center",
            color="tab:blue", fontsize=11)
    ax.text(0.5, 1.06, "cortes VERTICALES: $\\int_a^b\\!\\left(\\int_c^d f\\,dy\\right)dx$",
            ha="center", fontsize=10.5)
    ax.text(-0.04, 0.5, "$[a,b]\\times[c,d]$", rotation=90, va="center", fontsize=10)

    ax = pad[1]
    ax.set_xlim(-0.08, 1.12); ax.set_ylim(-0.14, 1.18)
    ax.set_aspect("equal"); ax.axis("off")
    ax.add_patch(Rectangle((0, 0), 1, 1, fc="none", ec="k", lw=2))
    for yi in np.arange(0.04, 0.96, 0.13):
        ax.add_patch(Rectangle((0, yi), 1, 0.085, fc="tab:orange", alpha=0.28,
                               ec="tab:orange", lw=0.8))
    ax.annotate("", xy=(-0.07, 0.5), xytext=(0.07, 0.5),
                arrowprops=dict(arrowstyle="<->", color="tab:orange", lw=2))
    ax.text(-0.09, 0.44, "$B(y)=\\int_a^b f\\,dx$", rotation=90, va="center",
            ha="right", color="tab:orange", fontsize=11)
    ax.text(0.5, 1.06, "cortes HORIZONTALES: $\\int_c^d\\!\\left(\\int_a^b f\\,dx\\right)dy$",
            ha="center", fontsize=10.5)
    fig.suptitle("Teorema de Fubini (v. I): el mismo volumen, dos recorridos",
                 fontsize=13, y=1.02)
    guardar(fig, "b10_fubini")


# 2. Region tipo-1 (entre curvas verticales) y tipo-2 (entre curvas horizontales)
def regiones():
    t = np.linspace(0, 1, 300)
    fig, pad = plt.subplots(1, 2, figsize=(10, 4.2))

    ax = pad[0]
    ax.fill_between(t, t ** 2, t, color="tab:green", alpha=0.30)
    for xi in [0.15, 0.35, 0.55, 0.75, 0.92]:
        ax.annotate("", xy=(xi, xi ** 2), xytext=(xi, xi),
                    arrowprops=dict(arrowstyle="-", color="tab:green", lw=2.4))
    ax.plot(t, t, "k-", lw=2, label="$y=x$ (techo)")
    ax.plot(t, t ** 2, "k--", lw=2, label="$y=\\alpha(x)=x^{2}$ (piso)")
    ax.set_xlim(-0.03, 1.1); ax.set_ylim(-0.03, 1.1)
    ax.set_xlabel("$x$"); ax.set_ylabel("$y$")
    ax.set_title("Tipo 1: $\\int_0^1\\!\\int_{x^2}^{x} f\\,dy\\,dx$\n"
                 "rebanadas VERTICALES (constantes afuera)", fontsize=10.5)
    ax.legend(fontsize=8.5, loc="lower right")

    ax = pad[1]
    ax.fill_between(t, t ** 2, t, color="tab:green", alpha=0.30)
    for yi in [0.12, 0.3, 0.5, 0.7, 0.88]:
        ax.annotate("", xy=(yi, yi), xytext=(np.sqrt(yi), yi),
                    arrowprops=dict(arrowstyle="-", color="tab:orange", lw=2.4))
    ax.plot(t, t ** 2, "k-", lw=2, label="$x=\\sqrt{y}$ (derecha)")
    ax.plot(t, t, "k--", lw=2, label="$x=y$ (izquierda)")
    ax.set_xlim(-0.03, 1.1); ax.set_ylim(-0.03, 1.1)
    ax.set_xlabel("$x$"); ax.set_ylabel("$y$")
    ax.set_title("Tipo 2: $\\int_0^1\\!\\int_{y}^{\\sqrt{y}} f\\,dx\\,dy$\n"
                 "rebanadas HORIZONTALES (constantes afuera)", fontsize=10.5)
    ax.legend(fontsize=8.5, loc="lower right")
    fig.suptitle("La misma región D: dos formas de recorrerla (Fubini v. II)",
                 fontsize=13, y=1.03)
    guardar(fig, "b10_regiones")


# 3. Inversion del orden: region del Ej. 3 del parcial 2025-1S
def inversion():
    t = np.linspace(0, 1, 400)
    circ = np.sqrt(np.clip(1 - t ** 2, 0, None))
    fig, pad = plt.subplots(1, 2, figsize=(10, 4.3))

    ax = pad[0]
    x1 = np.linspace(0, np.sqrt(2) / 2, 200)
    x2 = np.linspace(np.sqrt(2) / 2, 1, 200)
    ax.fill_between(x1, 0, x1, color="tab:blue", alpha=0.3)
    ax.fill_between(x2, 0, np.sqrt(1 - x2 ** 2), color="tab:blue", alpha=0.3)
    for xi in [0.1, 0.3, 0.5, 0.68, 0.85, 0.97]:
        ytop = xi if xi <= np.sqrt(2) / 2 else np.sqrt(max(1 - xi ** 2, 0))
        ax.annotate("", xy=(xi, 0), xytext=(xi, ytop),
                    arrowprops=dict(arrowstyle="-", color="tab:blue", lw=2.2))
    ax.plot(t, t, "k-", lw=1.8, label="$y=x$")
    ax.plot(t, circ, "k--", lw=1.8, label="$x^2+y^2=1$")
    ax.axvline(np.sqrt(2) / 2, color="gray", ls=":", lw=1.2)
    ax.text(np.sqrt(2) / 2 + 0.01, 0.06, "$\\frac{\\sqrt{2}}{2}$", fontsize=10)
    ax.set_xlim(-0.03, 1.08); ax.set_ylim(-0.06, 1.08)
    ax.set_xlabel("$x$"); ax.set_ylabel("$y$"); ax.set_aspect("equal")
    ax.set_title("Orden ORIGINAL dy dx: hay que partir\n"
                 "en dos tramos de $x$ (dos integrales)", fontsize=10.5)
    ax.legend(fontsize=9, loc="upper right")

    ax = pad[1]
    ax.fill_between(x1, 0, x1, color="tab:blue", alpha=0.3)
    ax.fill_between(x2, 0, np.sqrt(1 - x2 ** 2), color="tab:blue", alpha=0.3)
    for yi in [0.08, 0.25, 0.42, 0.58, 0.70]:
        ax.annotate("", xy=(yi, yi), xytext=(np.sqrt(1 - yi ** 2), yi),
                    arrowprops=dict(arrowstyle="-", color="tab:red", lw=2.2))
    ax.plot(t, t, "k-", lw=1.8, label="$y=x$")
    ax.plot(t, circ, "k--", lw=1.8, label="$x^2+y^2=1$")
    ax.set_xlim(-0.03, 1.08); ax.set_ylim(-0.06, 1.08)
    ax.set_xlabel("$x$"); ax.set_ylabel("$y$"); ax.set_aspect("equal")
    ax.set_title("Orden INVERTIDO dx dy: UNA sola integral\n"
                 "$\\int_0^{\\sqrt{2}/2}\\!\\int_y^{\\sqrt{1-y^2}} f\\,dx\\,dy$",
                 fontsize=10.5)
    ax.legend(fontsize=9, loc="upper right")
    fig.suptitle("Invertir el orden: dibujar R y releer los límites (parcial 2025, ej. 3)",
                 fontsize=13, y=1.02)
    guardar(fig, "b10_inversion")


# 4. Cambio a polares: rectangulo en (rho, theta) -> corona sectorial en (x, y)
def polares():
    r1, r2, t1, t2 = 1.0, 2.0, np.pi / 4, np.pi
    fig, pad = plt.subplots(1, 2, figsize=(10, 4.4))

    ax = pad[0]
    ax.add_patch(Rectangle((t1, r1), t2 - t1, r2 - r1, fc="tab:purple", alpha=0.3,
                           ec="tab:purple", lw=2))
    for rr in [1.0, 1.33, 1.66, 2.0]:
        ax.plot([t1, t2], [rr, rr], color="tab:purple", lw=1)
    for tt in np.linspace(t1, t2, 6):
        ax.plot([tt, tt], [r1, r2], color="tab:purple", lw=1)
    ax.set_xlabel(r"$\theta$"); ax.set_ylabel(r"$\rho$")
    ax.set_xlim(0.2, 3.3); ax.set_ylim(0.4, 2.4)
    ax.set_title("Espacio de los $(\\rho,\\theta)$:\nun RECTÁNGULO simple", fontsize=10.5)
    ax.text((t1 + t2) / 2, 1.5, "$[\\pi/4,\\pi]\\times[1,2]$",
            ha="center", fontsize=10)

    ax = pad[1]
    ax.set_aspect("equal")
    ax.add_patch(Wedge((0, 0), r2, np.degrees(t1), np.degrees(t2),
                       fc="tab:purple", alpha=0.3, ec="tab:purple", lw=2))
    th = np.linspace(t1, t2, 300)
    for rr in [1.0, 1.33, 1.66, 2.0]:
        ax.plot(rr * np.cos(th), rr * np.sin(th), color="tab:purple", lw=1)
    for tt in np.linspace(t1, t2, 6):
        ax.plot([0, 2 * np.cos(tt)], [0, 2 * np.sin(tt)], color="tab:purple", lw=1)
    ax.plot([0], [0], "ko", ms=4)
    ax.set_xlim(-2.3, 2.3); ax.set_ylim(-0.4, 2.3)
    ax.set_xlabel("$x$"); ax.set_ylabel("$y$")
    ax.set_title("Plano $xy$: una CORONA sectorial\n$\\rho\\in[1,2]$, $\\theta\\in[\\pi/4,\\pi]$",
                 fontsize=10.5)
    fig.suptitle("Cambio a polares: el rectángulo de Fubini se vuelve una sección de anillo",
                 fontsize=13, y=1.02)
    guardar(fig, "b10_polares")


# 5. Region del Ej. 5 del parcial 2025-1S (disco unitario menos el disco (1,0))
def disco_corona():
    fig, ax = plt.subplots(figsize=(6.4, 4.6))
    ax.set_aspect("equal")
    th = np.linspace(0, 2 * np.pi, 500)
    ax.plot(np.cos(th), np.sin(th), "k-", lw=2, label="$x^2+y^2=1$  ($\\rho=1$)")
    ax.plot(1 + np.cos(th), np.sin(th), "k--", lw=2,
            label="$x^2-2x+y^2=0$  ($\\rho=2\\cos\\theta$)")
    # región: 0 <= theta <= pi/2, 2cos(theta) <= rho <= 1
    tt = np.linspace(np.pi / 3, np.pi / 2, 300)
    inner = 2 * np.cos(tt)
    ax.fill(np.concatenate([inner * np.cos(tt), np.cos(tt)[::-1]]),
            np.concatenate([inner * np.sin(tt), np.sin(tt)[::-1]]),
            color="tab:orange", alpha=0.45, label="R")
    for tt0 in np.linspace(np.pi / 3 + 0.05, np.pi / 2 - 0.05, 5):
        ax.plot([0, 1.05 * np.cos(tt0)], [0, 1.05 * np.sin(tt0)], color="gray",
                ls=":", lw=1.2)
    for rr in [2 * np.cos(t) for t in np.linspace(np.pi / 3 + 0.05, np.pi / 2 - 0.05, 5)]:
        tt2 = np.linspace(np.arccos(min(rr / 2, 1)), np.pi / 2, 100) if rr < 2 else []
        if len(tt2):
            ax.plot(rr * np.cos(tt2), rr * np.sin(tt2), color="gray", ls=":", lw=1.2)
    ax.annotate(r"$\theta=\frac{\pi}{3}$", xy=(0.62, 1.07), fontsize=11)
    ax.annotate(r"$\theta=\frac{\pi}{2}$", xy=(-0.16, 1.05), fontsize=11)
    ax.annotate(r"$\rho=1$", xy=(0.72, 0.72), fontsize=10, color="k")
    ax.annotate(r"$\rho=2\cos\theta$", xy=(1.35, 0.72), fontsize=10)
    ax.plot([0], [0], "ko", ms=4)
    ax.set_xlim(-0.35, 2.15); ax.set_ylim(-0.3, 1.45)
    ax.set_xlabel("$x$"); ax.set_ylabel("$y$")
    ax.set_title("Parcial 2 2025, ej. 5: $\\iint_R \\sqrt{x^2+y^2}\\,dx\\,dy$\n"
                 "$R=\\{(r,\\theta):\\ \\pi/3\\leq\\theta\\leq\\pi/2,\\ 2\\cos\\theta\\leq r\\leq 1\\}$",
                 fontsize=11)
    ax.legend(fontsize=9, loc="upper right")
    guardar(fig, "b10_disco_corona")


# 6. Solido en cilindricas: cono interior (Ejemplo 8.18) con una rebanada vertical
def cilindricas():
    fig = plt.figure(figsize=(7.6, 5.2))
    ax = fig.add_subplot(111, projection="3d")
    u = np.linspace(0, 2 * np.pi, 120)
    w = np.linspace(0, 1, 40)
    U, W = np.meshgrid(u, w)
    ax.plot_surface(W * np.cos(U), W * np.sin(U), W, color="tab:blue", alpha=0.16,
                    linewidth=0)
    th0, th1 = np.pi / 4, 3 * np.pi / 4
    # rebanada vertical a un angulo fijo (rho variable, z entre rho y 1)
    rr = np.linspace(0, 1, 60)
    tt = np.linspace(th0, th1, 60)
    R, T = np.meshgrid(rr, tt)
    ax.plot_surface(R * np.cos(T), R * np.sin(T), np.ones_like(R),
                    color="tab:orange", alpha=0.55, linewidth=0)
    for t0 in [th0, (th0 + th1) / 2, th1]:
        ax.plot(rr * np.cos(t0), rr * np.sin(t0), rr, color="tab:orange", lw=2.2)
        ax.plot([0, np.cos(t0)], [0, np.sin(t0)], [0, 0], color="k", lw=1.4)
    ax.plot(np.cos(np.linspace(th0, th1, 80)), np.sin(np.linspace(th0, th1, 80)),
            np.zeros(80), "k-", lw=2)
    ax.text(0.05, 0.05, 1.06, "$z=1$", fontsize=11)
    ax.text(1.02, 0.55, 0.5, "$z=\\rho$", fontsize=11, color="tab:blue")
    ax.text(-0.9, -0.75, 0.15, "$\\rho=1$", fontsize=11)
    ax.set_xlim(-1, 1); ax.set_ylim(-1, 1); ax.set_zlim(0, 1.1)
    ax.set_xlabel("$x$"); ax.set_ylabel("$y$"); ax.set_zlabel("$z$")
    ax.set_title("Cilíndricas: $x=\\rho\\cos\\theta$, $y=\\rho\\sin\\theta$, $z=z$;"
                 " Jacobiano $\\rho$\n"
                 "las cajas $(\\rho,\\theta,z)$ son sectores de cilindro", fontsize=11)
    guardar(fig, "b10_cilindricas")


# 7. Solido en esfericas: radio, angulos phi y theta
def esfericas():
    fig = plt.figure(figsize=(7.6, 5.2))
    ax = fig.add_subplot(111, projection="3d")
    p = np.linspace(0, np.pi, 60)
    t = np.linspace(0, 2 * np.pi, 90)
    P, T = np.meshgrid(p, t)
    ax.plot_surface(np.sin(P) * np.cos(T), np.sin(P) * np.sin(T), np.cos(P),
                    color="tab:purple", alpha=0.14, linewidth=0)
    r0, phi0, th0 = 1.0, np.deg2rad(55), np.deg2rad(40)
    P0 = np.array([r0 * np.sin(phi0) * np.cos(th0),
                   r0 * np.sin(phi0) * np.sin(th0), r0 * np.cos(phi0)])
    ax.plot([0, P0[0]], [0, P0[1]], [0, P0[2]], color="tab:red", lw=3)
    ax.scatter(*P0, color="tab:red", s=45)
    # arco de phi (en el plano vertical que pasa por P0)
    pp = np.linspace(0.001, phi0, 60)
    ax.plot(np.sin(pp) * np.cos(th0), np.sin(pp) * np.sin(th0), np.cos(pp),
            color="k", lw=2.2)
    ax.text(0.16 * np.cos(th0), 0.16 * np.sin(th0), 0.95, "$\\varphi$", fontsize=14)
    # proyeccion al plano xy y arco de theta
    ax.plot([P0[0], P0[0]], [P0[1], P0[1]], [P0[2], 0], color="gray", ls="--", lw=1.5)
    ax.plot([0, P0[0]], [0, P0[1]], [0, 0], color="gray", ls="--", lw=1.5)
    tt = np.linspace(0.001, th0, 60)
    ax.plot(0.55 * np.cos(tt), 0.55 * np.sin(tt), np.zeros(60), color="k", lw=2.2)
    ax.text(0.62 * np.cos(th0 / 2), 0.62 * np.sin(th0 / 2), 0.02, "$\\theta$", fontsize=14)
    ax.text(P0[0] * 0.55, P0[1] * 0.55, P0[2] * 0.55, "$r$", fontsize=13, color="tab:red")
    ax.plot([-1.2, 1.2], [0, 0], [0, 0], "k-", lw=1)
    ax.plot([0, 0], [-1.2, 1.2], [0, 0], "k-", lw=1)
    ax.plot([0, 0], [0, 0], [-1.2, 1.2], "k-", lw=1)
    ax.set_xlim(-1.1, 1.1); ax.set_ylim(-1.1, 1.1); ax.set_zlim(-1.1, 1.1)
    ax.set_xlabel("$x$"); ax.set_ylabel("$y$"); ax.set_zlabel("$z$")
    ax.set_title("Esféricas: $x=r\\sin\\varphi\\cos\\theta$, $y=r\\sin\\varphi\\sin\\theta$, "
                 "$z=r\\cos\\varphi$\n"
                 "$r\\geq0$, $0\\leq\\varphi\\leq\\pi$, $0\\leq\\theta<2\\pi$;"
                 " Jacobiano $r^2\\sin\\varphi$", fontsize=11)
    guardar(fig, "b10_esfericas")


# 8. Integral impropia multiple: Gauss sobre discos crecientes
def impropias():
    fig = plt.figure(figsize=(11, 4.2))

    ax = fig.add_subplot(121, projection="3d")
    xs = np.linspace(-2.6, 2.6, 160)
    X, Y = np.meshgrid(xs, xs)
    Z = np.exp(-(X ** 2 + Y ** 2))
    ax.plot_surface(X, Y, Z, cmap="viridis", alpha=0.85, linewidth=0)
    for R, c in [(1, "tab:red"), (2, "tab:orange"), (3, "tab:blue")]:
        tt = np.linspace(0, 2 * np.pi, 300)
        ax.plot(R * np.cos(tt), R * np.sin(tt), np.zeros(300), color=c, lw=2)
    ax.set_xlabel("$x$"); ax.set_ylabel("$y$"); ax.set_zlabel("$z$")
    ax.set_title("$e^{-(x^2+y^2)}$ sobre discos $x^2+y^2\\leq R^2$\n"
                 "disco rojo $R=1$, naranja $R=2$, azul $R=3$", fontsize=10.5)
    ax.view_init(elev=28, azim=-58)

    ax = fig.add_subplot(122)
    RR = np.linspace(0.001, 3.2, 400)
    val = np.pi * (1 - np.exp(-RR ** 2))
    ax.plot(RR, val, "k-", lw=2.4, label="$\\int_0^R\\!\\int_0^{2\\pi} e^{-\\rho^2}\\rho\\,d\\theta\\,d\\rho=\\pi(1-e^{-R^2})$")
    ax.axhline(np.pi, color="tab:red", ls="--", lw=1.6, label="$\\pi$ (límite $R\\to\\infty$)")
    ax.set_xlabel("$R$"); ax.set_ylabel("valor de la integral sobre el disco")
    ax.set_title("La cola no acotada: el límite existe\n"
                 "$\\iint_{\\mathbb{R}^2} e^{-(x^2+y^2)}=\\pi$", fontsize=10.5)
    ax.legend(fontsize=9, loc="lower right")
    guardar(fig, "b10_impropias")


# 9. Mapa del bloque 10
def mapa():
    fig, ax = plt.subplots(figsize=(8.6, 5.6))
    ax.axis("off")
    cajas = [
        (0.50, 0.93, "INTEGRALES MÚLTIPLES\n$\\iint_D f$, $\\iiint_D f$  (Bloque 10)", "tab:blue"),
        (0.16, 0.68, "CLASE 45\nFubini I y II:\niteradas + orden", "tab:green"),
        (0.50, 0.68, "CLASE 46\ncambio de variable\ny POLARES ($|J|=\\rho$)", "tab:orange"),
        (0.84, 0.68, "CLASE 47\nTRIPLES: cilíndricas\ny esféricas", "tab:red"),
        (0.33, 0.40, "CLASE 48\nimpropias múltiples\n(límites sobre cortes)", "tab:purple"),
        (0.72, 0.40, "SIMULACRO\nexámenes 2018–2022\n(5 ejercicios)", "firebrick"),
        (0.33, 0.14, "CLAVES: dibujar el dominio\n· constantes FUERA\n· $|\\det Jg|$ siempre", "olive"),
        (0.72, 0.14, "APLICACIONES\nárea, volumen, masas\ny centros de masa", "steelblue"),
        (0.50, 0.90, "", "white"),
    ]
    for x, y, t, c in cajas:
        if not t:
            continue
        ax.add_patch(plt.Rectangle((x - 0.15, y - 0.075), 0.30, 0.15, fc=c, alpha=0.16,
                                   ec=c, lw=2, zorder=2))
        ax.text(x, y, t, ha="center", va="center", fontsize=8.6, zorder=3)
    flechas = [((0.5, 0.855), (0.16, 0.755)), ((0.5, 0.855), (0.5, 0.755)),
               ((0.5, 0.855), (0.84, 0.755)),
               ((0.16, 0.605), (0.33, 0.475)), ((0.5, 0.605), (0.33, 0.475)),
               ((0.84, 0.605), (0.72, 0.475)),
               ((0.40, 0.325), (0.42, 0.215)), ((0.70, 0.325), (0.66, 0.215))]
    for a, b in flechas:
        ax.annotate("", xy=b, xytext=a, arrowprops=dict(arrowstyle="->", lw=1.4, color="gray"))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.set_title("Mapa del Bloque 10 — Integrales múltiples (clases 45 a 48)", fontsize=13)
    guardar(fig, "b10_mapa")


if __name__ == "__main__":
    fubini()
    regiones()
    inversion()
    polares()
    disco_corona()
    cilindricas()
    esfericas()
    impropias()
    mapa()
    print("BLOQUE 10 LISTO:", len([f for f in os.listdir(OUT) if f.startswith("b10_")]), "figuras")
