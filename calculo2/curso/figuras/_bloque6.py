# -*- coding: utf-8 -*-
"""Figuras del Bloque 6 — Topología en Rn (clases 30-33).
Genera: b6_bolas_normas, b6_bola_abierta_cerrada, b6_abiertos_cerrados,
        b6_interior_frontera, b6_acumulacion, b6_compacto,
        b6_conexo_disconexo, b6_mapa  (PNG en curso/img/)."""
import os
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

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


# 1. Bola unitaria segun la norma
def bolas_normas():
    t = np.linspace(0, 2 * np.pi, 400)
    fig, pad = plt.subplots(1, 3, figsize=(10.5, 3.6))
    datos = [
        (np.abs(np.cos(t)) + np.abs(np.sin(t)), "norma $\\|\\cdot\\|_1$",
         r"$|x|+|y|\leq 1$  (rombo)"),
        (np.ones_like(t), "norma $\\|\\cdot\\|_2$  (euclídea)",
         r"$x^2+y^2\leq 1$  (círculo)"),
        (np.maximum(np.abs(np.cos(t)), np.abs(np.sin(t))),
         "norma $\\|\\cdot\\|_\\infty$", r"$\max(|x|,|y|)\leq 1$  (cuadrado)"),
    ]
    for ax, (r, tit, sub) in zip(pad, datos):
        ax.plot(r * np.cos(t), r * np.sin(t), color="tab:blue", lw=2.2)
        ax.fill(r * np.cos(t), r * np.sin(t), color="tab:blue", alpha=0.15)
        ax.set_aspect("equal")
        ax.set_xlim(-1.4, 1.4); ax.set_ylim(-1.4, 1.4)
        ax.axhline(0, color="k", lw=0.7); ax.axvline(0, color="k", lw=0.7)
        ax.set_title(tit + "\n" + sub, fontsize=10)
        ax.set_xticks([-1, 0, 1]); ax.set_yticks([-1, 0, 1])
    fig.suptitle("Misma idea (\"estar a menos de 1 del origen\"), distinta distancia",
                 fontsize=12.5, y=1.03)
    guardar(fig, "b6_bolas_normas")


# 2. Bola abierta vs bola cerrada (y la bola B(p, delta2) de la Prop 5.8)
def bola_abierta_cerrada():
    t = np.linspace(0, 2 * np.pi, 400)
    fig, pad = plt.subplots(1, 2, figsize=(9.6, 4.2))

    ax = pad[0]
    ax.plot(np.cos(t), np.sin(t), "b--", lw=2)
    ax.fill(np.cos(t), np.sin(t), color="tab:blue", alpha=0.15)
    p = np.array([0.55, 0.35])
    d2 = 1.0 - np.hypot(*p)
    ax.plot(*p, "ko", ms=5)
    ax.plot(p[0] + d2 * np.cos(t), p[1] + d2 * np.sin(t), "-", color="tab:green", lw=1.8)
    ax.fill(p[0] + d2 * np.cos(t), p[1] + d2 * np.sin(t), color="tab:green", alpha=0.25)
    ax.annotate(r"$a$", (0, 0), fontsize=12, ha="right", va="bottom")
    ax.annotate(r"$p$", p, fontsize=11, ha="left", va="bottom")
    ax.annotate(r"$\delta_2=\delta-d(a,p)$", (p[0] + d2 * np.cos(0.9),
                p[1] + d2 * np.sin(0.9)), fontsize=9, color="tab:green")
    ax.set_title("Bola ABierta $B(a,\\delta)$: borde discontinuo,\n"
                 "y para cada $p$ entra $B(p,\\delta_2)$ (Prop. 5.8)", fontsize=10.5)
    ax.set_aspect("equal"); ax.set_xlim(-1.3, 1.5); ax.set_ylim(-1.3, 1.3)

    ax = pad[1]
    ax.plot(np.cos(t), np.sin(t), "r-", lw=2.2)
    ax.fill(np.cos(t), np.sin(t), color="tab:red", alpha=0.15)
    ax.annotate(r"$\bar{B}(a,\delta)$: $d(a,x)\leq\delta$", (0, 0), fontsize=10,
                ha="center", va="center")
    ax.set_title("Bola CERRADA $\\bar{B}(a,\\delta)$: borde sólido,\n"
                 "el círculo SÍ pertenece", fontsize=10.5)
    ax.set_aspect("equal"); ax.set_xlim(-1.3, 1.3); ax.set_ylim(-1.3, 1.3)
    fig.suptitle("En $\\mathbb{R}^2$ con la distancia euclídea: disco sin borde / disco con borde",
                 fontsize=12.5, y=1.02)
    guardar(fig, "b6_bola_abierta_cerrada")


# 3. Abiertos, cerrados y ni una cosa ni otra en R2
def abiertos_cerrados():
    t = np.linspace(0, 2 * np.pi, 400)
    fig, pad = plt.subplots(1, 3, figsize=(11.5, 3.8))

    ax = pad[0]                      # A1: rectangulo semi-cerrado
    ax.add_patch(plt.Rectangle((1, 1), 1, 2, fc="tab:blue", alpha=0.18))
    ax.plot([1, 1], [1, 3], "b-", lw=2.4)
    ax.plot([2, 2], [1, 3], "b-", lw=2.4)
    ax.plot([1, 2], [1, 1], "b--", lw=2.0)
    ax.plot([1, 2], [3, 3], "b--", lw=2.0)
    ax.plot([1, 2], [1, 1], "wx", ms=6); ax.plot([1, 2], [3, 3], "wx", ms=6)
    ax.set_xlim(0.6, 2.4); ax.set_ylim(0.6, 3.4)
    ax.set_title("$A_1=[1,2]\\times(1,3)$\nlados $x=1,2$ INCLUIDOS,\n"
                 "$y=1,3$ EXCLUIDOS $\\Rightarrow$ NI abierto\nNI cerrado (acotado, no compacto)",
                 fontsize=9.5)
    ax.set_aspect("equal")

    ax = pad[1]                      # A3: disco pinchado (abierto)
    ax.plot(np.cos(t), np.sin(t), "b--", lw=2)
    ax.fill(np.cos(t), np.sin(t), color="tab:blue", alpha=0.15)
    ax.plot(0, 0, "wo", mec="b", ms=7, mew=2)
    ax.set_xlim(-1.4, 1.4); ax.set_ylim(-1.4, 1.4)
    ax.set_aspect("equal")
    ax.set_title("$A_3=\\bar B(0,1)-\\{(0,0)\\}$\nABIERTO (todo punto es interior),\n"
                 "no cerrado: falta el $0$", fontsize=9.5)

    ax = pad[2]                      # A4: elipse abierta + recta
    ax.plot(np.cos(t) / np.sqrt(2), np.sin(t), "b--", lw=2)
    ax.fill(np.cos(t) / np.sqrt(2), np.sin(t), color="tab:blue", alpha=0.15)
    ax.plot([-1.6, 1.6], [-1.6, 1.6], "-", color="tab:orange", lw=2)
    ax.set_xlim(-1.7, 1.7); ax.set_ylim(-1.8, 1.8)
    ax.set_aspect("equal")
    ax.set_title("$A_4=\\{2x^2+y^2<1\\}\\cup\\{x=y\\}$\nla recta NO es interior y la\n"
                 "cara de la elipse NO está: NI abierto NI cerrado", fontsize=9.5)
    fig.suptitle("Tres estereotipos de conjuntos de $\\mathbb{R}^2$ "
                 "(Práctico 5, ej. 1)", fontsize=12.5, y=1.04)
    guardar(fig, "b6_abiertos_cerrados")


# 4. Interior, frontera y clausura de A3 (disco pinchado)
def interior_frontera():
    t = np.linspace(0, 2 * np.pi, 400)
    fig, ax = plt.subplots(figsize=(6.4, 5.4))
    ax.fill(np.cos(t), np.sin(t), color="tab:purple", alpha=0.12)   # clausura
    ax.fill(np.cos(t), np.sin(t), color="tab:green", alpha=0.30)    # interior
    ax.plot(np.cos(t), np.sin(t), color="tab:red", lw=2.6)          # frontera
    ax.plot(0, 0, "wo", mec="k", ms=8, mew=2)
    ax.annotate("0: punto de acumulación\nque hay que agregar\na la clausura",
                (0, 0), textcoords="offset points", xytext=(28, -40), fontsize=9,
                arrowprops=dict(arrowstyle="->", lw=1.2))
    ax.annotate("frontera $\\partial A_3=S^1$", (0.7, 0.7), fontsize=10,
                color="tab:red")
    ax.annotate("interior (verde) $= A_3$\n(el disco abierto sin el $0$)",
                (-0.2, 0.25), fontsize=9.5, color="darkgreen")
    ax.annotate("clausura $\\bar A_3$ = disco CERRADO\n(agregá circunferencia y $0$)",
                (-1.25, -1.1), fontsize=9.5, color="tab:purple")
    ax.set_aspect("equal"); ax.set_xlim(-1.55, 1.55); ax.set_ylim(-1.55, 1.4)
    ax.set_title("$A_3=\\{(x,y): x^2+y^2<1,\\ (x,y)\\neq(0,0)\\}$\n"
                 "interior, frontera y clausura", fontsize=12)
    guardar(fig, "b6_interior_frontera")


# 5. Puntos de acumulacion de A5 (Practico 5, ej. 1)
def acumulacion():
    n = np.arange(1, 13)
    x = (-1.0) ** n + 1.0 / n
    fig, ax = plt.subplots(figsize=(8.2, 3.8))
    ax.axhline(1, color="gray", lw=1, ls=":")
    ax.plot(x, np.ones_like(n), "o", color="tab:blue", ms=6,
            label=r"$A_5=\{((-1)^n+\frac{1}{n},\,1):n\geq 1\}$ (todos aislados)")
    for xi, ni in zip(x, n):
        ax.annotate(f"$n={ni}$", (xi, 1), textcoords="offset points",
                    xytext=(0, 9 if ni % 2 else -16), fontsize=7.5, ha="center")
    ax.plot([-1, 1], [1, 1], "*", color="tab:red", ms=16,
            label=r"$A_5'=\{(-1,1),\,(1,1)\}$ (acumulación)")
    for c in (-1, 1):
        ax.add_patch(plt.Circle((c, 1), 0.13, fill=False, ls="--",
                                color="tab:red", lw=1.3))
    ax.annotate(r"$\frac{1}{n}\to 0$: los pares se acumulan en $1$"
                "\n" r"y los impares en $-1$", (0, 0.72), fontsize=9.5, ha="center")
    ax.set_xlim(-1.5, 1.9); ax.set_ylim(0.55, 1.25)
    ax.set_yticks([])
    ax.set_xlabel(r"$x$")
    ax.set_title("Cada punto de $A_5$ es aislado; los únicos de acumulación\n"
                 "están FUERA del conjunto $\\Rightarrow$ $A_5$ no es cerrado",
                 fontsize=11)
    ax.legend(fontsize=8.5, loc="upper right")
    guardar(fig, "b6_acumulacion")


# 6. Compacto = cerrado y acotado
def compacto():
    t = np.linspace(0, 2 * np.pi, 300)
    fig, pad = plt.subplots(2, 2, figsize=(8.6, 7.2))
    ejes = pad.ravel()

    ax = ejes[0]
    ax.plot(np.cos(t), np.sin(t), "b-", lw=2)
    ax.fill(np.cos(t), np.sin(t), color="tab:green", alpha=0.3)
    ax.set_title("Cerrado y acotado: $\\bar B(0,1)$\nCOMPACTO  ✓", fontsize=10.5,
                 color="darkgreen")
    ax.set_aspect("equal"); ax.set_xlim(-1.4, 1.4); ax.set_ylim(-1.4, 1.4)

    ax = ejes[1]
    ax.plot(np.cos(t), np.sin(t), "b--", lw=2)
    ax.fill(np.cos(t), np.sin(t), color="tab:red", alpha=0.18)
    ax.plot(0, 0, "wo", mec="b", ms=7, mew=2)
    ax.set_title("Acotado pero NO cerrado: $B(0,1)$\nNO compacto  ✗ (la sucesión\n"
                 "$x_n=(1-1/n,\\,0)$ se escapa)", fontsize=10.5, color="firebrick")
    ax.set_aspect("equal"); ax.set_xlim(-1.4, 1.4); ax.set_ylim(-1.4, 1.4)

    ax = ejes[2]
    xs = np.linspace(-2, 2, 100)
    ax.fill_between(xs, 0, 2, color="tab:red", alpha=0.18)
    ax.plot(xs, np.zeros_like(xs), "b-", lw=2)
    ax.set_title("Cerrado pero NO acotado: $\\{y\\geq 0\\}$\nNO compacto  ✗", fontsize=10.5,
                 color="firebrick")
    ax.set_xlim(-2.2, 2.2); ax.set_ylim(-0.6, 2.2)

    ax = ejes[3]
    k = np.arange(1, 9)
    ax.plot(k, 1.0 / k, "o-", color="tab:blue", ms=5,
            label=r"$x_n=(n,\frac{1}{n})$: se va al infinito")
    ax.axvline(6, color="gray", ls=":", lw=1)
    ax.set_title("Ni acotado: $(n,1/n)$\nNO compacto  ✗", fontsize=10.5,
                 color="firebrick")
    ax.set_xlabel(r"$n$"); ax.set_ylim(-0.2, 1.3)
    ax.legend(fontsize=8.5)
    fig.suptitle("Compacto (en $\\mathbb{R}^n$) = CERRADO + ACOTADO  "
                 "(Definición 5.21)", fontsize=13, y=1.0)
    guardar(fig, "b6_compacto")


# 7. Conexo vs disconexo
def conexo_disconexo():
    t = np.linspace(0, 2 * np.pi, 400)
    fig, pad = plt.subplots(1, 3, figsize=(11.5, 3.8))

    ax = pad[0]
    ax.fill(np.cos(t), np.sin(t), color="tab:green", alpha=0.35)
    ax.set_title("$B(0,1)$: CONEXO\nno hay forma de partirlo en dos\nabiertos disjuntos "
                 "(es convexo)", fontsize=10, color="darkgreen")
    ax.set_aspect("equal"); ax.set_xlim(-1.4, 1.4); ax.set_ylim(-1.4, 1.4)

    ax = pad[1]
    ax.fill(np.cos(t), np.sin(t), color="tab:green", alpha=0.28)
    ax.plot(np.cos(t), np.sin(t), "b--", lw=1.6)
    ax.plot(0, 0, "wo", mec="b", ms=8, mew=2)
    ax.annotate("¡aunque le falta el $0$,\nsigue siendo de una pieza!",
                (0, 0.64), fontsize=8.5, ha="center", color="darkgreen")
    ax.set_title("$A_3$ (disco pinchado): CONEXO\n"
                 "en $\\mathbb{R}^2$ sacar UN punto\nno lo parte en dos", fontsize=10,
                 color="darkgreen")
    ax.set_aspect("equal"); ax.set_xlim(-1.4, 1.4); ax.set_ylim(-1.4, 1.4)

    ax = pad[2]
    xs = np.linspace(-1.6, 1.6, 100)
    ax.plot(xs, xs / 2, "-", color="tab:blue", lw=2)
    ax.plot(xs, -xs / 2, "-", color="tab:orange", lw=2)
    ax.plot(0, 0, "wo", mec="k", ms=8, mew=2)
    ax.annotate("$E$", (1.1, 0.55), color="tab:blue", fontsize=11)
    ax.annotate("$F$", (1.1, -0.55), color="darkorange", fontsize=11)
    ax.set_title("$x^2-4y^2=0$ menos el origen: DESCONEXO\n"
                 "(parcial 2021-2S: las dos ramas quedan separadas)", fontsize=10)
    ax.set_aspect("equal"); ax.set_xlim(-1.7, 1.7); ax.set_ylim(-1.3, 1.3)
    fig.suptitle("Conexo = \"de una sola pieza\": no puede escribirse "
                 "$A=E\\cup F$ con $E,F$ abiertos, disjuntos y no vacíos",
                 fontsize=12, y=1.04)
    guardar(fig, "b6_conexo_disconexo")


# 8. Mapa del bloque
def mapa():
    fig, ax = plt.subplots(figsize=(8.8, 5.8))
    ax.axis("off")
    cajas = [
        (0.50, 0.93, "TOPOLOGÍA EN $\\mathbb{R}^n$\n(distancia, bolas)", "tab:blue"),
        (0.18, 0.70, "BOLAS $B(a,\\delta)$\n$B^*(a,\\delta)$ reducida\nsegún la norma", "tab:green"),
        (0.50, 0.70, "PUNTOS\ninterior · exterior\nfrontera", "tab:orange"),
        (0.82, 0.70, "CONJUNTOS\nabierto = todo interior\ncerrado = $A^c$ abierto", "tab:red"),
        (0.18, 0.45, "OPERACIONES\n$\\cup$ arbitraria de abiertos\n$\\cap$ finita de abiertos", "tab:purple"),
        (0.50, 0.45, "$\\mathring{A}$, $\\partial A$, $A'$, $\\bar A$\nabierto sii $A=\\mathring{A}$\ncerrado sii $A=\\bar A$", "olive"),
        (0.82, 0.45, "COMPACTO\ncerrado y acotado\n(Bolzano–Weierstrass)", "firebrick"),
        (0.30, 0.20, "SUCESIONES EN $\\mathbb{R}^n$\nconvergen coordenada a coordenada;\ncerrado sii cerrado por sucesiones",
         "steelblue"),
        (0.72, 0.20, "CONEXO\nno separable en dos abiertos\ndisjuntos (\"una pieza\")", "teal"),
        (0.50, 0.03, "PARCIAL/EXAMEN: clasificar conjuntos, hallar $\\mathring{A}$, $\\partial A$, $A'$, $\\bar A$ "
                     "y subsucesiones", "dimgray"),
    ]
    for x, y, t, c in cajas:
        ax.add_patch(plt.Rectangle((x - 0.155, y - 0.08), 0.31, 0.16, fc=c, alpha=0.16,
                                   ec=c, lw=2, zorder=2))
        ax.text(x, y, t, ha="center", va="center", fontsize=8.2, zorder=3)
    flechas = [((0.5, 0.85), (0.18, 0.78)), ((0.5, 0.85), (0.5, 0.78)),
               ((0.5, 0.85), (0.82, 0.78)), ((0.18, 0.62), (0.18, 0.53)),
               ((0.5, 0.62), (0.5, 0.53)), ((0.82, 0.62), (0.82, 0.53)),
               ((0.42, 0.45), (0.36, 0.28)), ((0.58, 0.45), (0.64, 0.28)),
               ((0.82, 0.37), (0.80, 0.28))]
    for a, b in flechas:
        ax.annotate("", xy=b, xytext=a, arrowprops=dict(arrowstyle="->", lw=1.4,
                    color="gray"))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.set_title("Mapa del Bloque 6 — Topología en $\\mathbb{R}^n$ (clases 30 a 33)",
                 fontsize=13)
    guardar(fig, "b6_mapa")


if __name__ == "__main__":
    bolas_normas()
    bola_abierta_cerrada()
    abiertos_cerrados()
    interior_frontera()
    acumulacion()
    compacto()
    conexo_disconexo()
    mapa()
    print("BLOQUE 6 LISTO:", len([f for f in os.listdir(OUT)
                                  if f.startswith("b6_")]), "figuras")
